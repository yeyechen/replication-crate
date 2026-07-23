"""
Replication of Heston & Sadka (2010, JFQA) "Seasonality in the Cross Section of
Stock Returns: The International Evidence" — DATA PIPELINE.
================================================================================
Builds the analysis-ready MONTHLY INTERNATIONAL EQUITY PANEL and writes it to
data/panel.parquet. This is the Stage-7 data pipeline only; downstream tables
(T1, T2, T3, T7) consume the panel.

Panel columns (exact schema, fixed by the Replicator)
-----------------------------------------------------
gvkey     : Compustat company identifier (String)
country   : ISO3 domicile — 13 global countries via g_company.loc, plus 'CAN'
curcdd    : data currency of the security at month-end (String)
month     : last-day-of-month Date the row describes
ret_local : monthly LOCAL total return = (prccd/ajexdi)_t / (prccd/ajexdi)_{t-1} - 1
ret_usd   : monthly USD return = (1+ret_local) * (usd_per_x_t / usd_per_x_{t-1}) - 1
me_usd    : market equity in USD = prccd * cshoc(ff) * usd_per_x_t

Universe (two data sources, union)
----------------------------------
GLOBAL (13 countries): comp_202601.g_secd INNER JOIN g_company
       ON s.gvkey=co.gvkey AND s.iid=co.prirow  (primary issue, one per firm)
       WHERE co.loc IN (AUT,BEL,FIN,FRA,DEU,ITA,JPN,NLD,NOR,ESP,SWE,CHE,GBR)
CANADA: comp_202601.secd INNER JOIN security
       ON s.gvkey=sec.gvkey AND s.iid=sec.iid  WHERE sec.excntry='CAN'

Data window: datadate 1979-12-01 .. 2006-06-30 (panel starts 1979-12 so the
lag-60 signal for the first reported month, Feb 1985, is available).

FX convention (verified against the Replicator's sanity anchors)
----------------------------------------------------------------
g_exrt_dly stores GBP-base cross rates (fromcurd='GBP', tocurd=X,
exratd = units of X per 1 GBP). usd_per_x = USD price of 1 unit of X
= rate(GBP->USD) / rate(GBP->X). See the "Spec concern" note in the report:
the task prose wrote the fraction as rate(GBP->X)/rate(GBP->USD), which is its
reciprocal; the verified NTT anchor (me_usd 2000-06-30 ~ 2.1e11 USD) and
assumptions.md A4 / log1.md require usd_per_x = rate(GBP->USD)/rate(GBP->X),
which is what is implemented.

Implementation
--------------
All filtering, month-end aggregation, return lags, cshoc carry-forward, and the
FX join are pushed into ClickHouse SQL (src/sql/*.sql). main.py orchestrates:
  1. materialize month_end_prices.sql -> write_yeye.hs_month_end  (CTAS)
  2. materialize fx_gbp_cross.sql     -> write_yeye.hs_fx          (CTAS)
  3. run panel.sql (joins the two, computes ret_usd / me_usd) -> pandas
  4. write data/panel.parquet (the ONLY parquet)
  5. compute report diagnostics + verify anchors, write results/diagnostics.md
  6. drop scratch tables (unless --keep-stage)

Usage
-----
    uv run python src/main.py                # full pipeline
    uv run python src/main.py --keep-stage   # keep write_yeye scratch tables
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

from utils.env import get_clickhouse_config
from utils.paths import paper_layout

# ────────────────────────────────────────────────────────────────────────────
# Layout & configuration
# ────────────────────────────────────────────────────────────────────────────
SLUG = "seasonality_international_evidence"
LAYOUT = paper_layout(SLUG)
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")
_CFG = get_clickhouse_config()

# Paper parameters (fixed by the Replicator; see preparations/assumptions.md A1–A4
# and preprocessing_rules.json rule_ids universe_countries_14 / sample_period_1985_2006).
DATA_START = "1979-12-01"          # panel start (month-end 1979-12) for lag-60
DATA_END = "2006-06-30"            # panel end (month-end 2006-06)
REPORT_START = "1985-02-28"        # first reported month (Feb 1985) for diagnostics
COUNTRIES_13 = ["AUT", "BEL", "FIN", "FRA", "DEU", "ITA", "JPN",
                "NLD", "NOR", "ESP", "SWE", "CHE", "GBR"]

# Scratch (intermediate) ClickHouse tables — NOT parquets; dropped at the end.
T_ME = "write_yeye.hs_month_end"
T_FX = "write_yeye.hs_fx"

# Paper Table 1 reference values (for comparison only)
PAPER_FIRMS_TOTAL = 18117
PAPER_FIRMS_BY_COUNTRY = {"JPN": 4452, "GBR": 3938, "CAN": 2714,
                          "DEU": 1471, "FRA": 1512, "AUT": 192}
PAPER_FIRM_MONTHS = 2440681


# ────────────────────────────────────────────────────────────────────────────
# ClickHouse connection
# ────────────────────────────────────────────────────────────────────────────
def _client(exec_time: int = 2400) -> Client:
    return Client(
        host=_CFG["host"], port=int(_CFG["port"]),
        user=_CFG["user"], password=_CFG["password"],
        database=_CFG.get("database", "default"),
        settings={"max_execution_time": exec_time},
    )


def q(sql: str, exec_time: int = 2400) -> pd.DataFrame:
    """Execute a SQL string; return a DataFrame. Strips a trailing ';'."""
    c = _client(exec_time)
    data, cols = c.execute(sql.strip().rstrip(";"), with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str, exec_time: int = 2400) -> pd.DataFrame:
    """Execute a saved SQL file; return a DataFrame."""
    return q((SQL_DIR / name).read_text(), exec_time=exec_time)


def run_ctas(table: str, sql_file: str, exec_time: int = 2400) -> None:
    """Materialize a SQL file's SELECT into a scratch ClickHouse table (CTAS).

    The .sql file carries its own trailing SETTINGS; ClickHouse accepts them
    inside `CREATE TABLE ... AS SELECT ... SETTINGS ...` (verified).
    """
    sql = (SQL_DIR / sql_file).read_text().strip().rstrip(";")
    c = _client(exec_time)
    c.execute(f"DROP TABLE IF EXISTS {table}")
    t0 = time.time()
    c.execute(f"CREATE TABLE {table} AS {sql}")
    n = c.execute(f"SELECT count() FROM {table}")[0][0]
    print(f"  [stage] {table}: {n:,} rows in {time.time()-t0:.1f}s")


# ────────────────────────────────────────────────────────────────────────────
# Pipeline
# ────────────────────────────────────────────────────────────────────────────
def build_stage_tables() -> None:
    print("Step 1/2: materializing month-end price panel (large daily scan)...")
    run_ctas(T_ME, "month_end_prices.sql", exec_time=2400)
    print("Step 2/2: materializing FX conversion factors...")
    run_ctas(T_FX, "fx_gbp_cross.sql", exec_time=300)


def build_panel() -> pd.DataFrame:
    print("Assembling final panel (FX join, ret_usd, me_usd)...")
    t0 = time.time()
    panel = q_file("panel.sql", exec_time=900)
    print(f"  pulled {len(panel):,} rows x {panel.shape[1]} cols in {time.time()-t0:.1f}s")
    # column order + names (exact schema)
    panel = panel[["gvkey", "country", "curcdd", "month",
                   "ret_local", "ret_usd", "me_usd"]]
    panel["month"] = pd.to_datetime(panel["month"])
    for col in ["ret_local", "ret_usd", "me_usd"]:
        panel[col] = pd.to_numeric(panel[col], errors="coerce")
    panel = panel.sort_values(["gvkey", "month"]).reset_index(drop=True)
    return panel


# ────────────────────────────────────────────────────────────────────────────
# Diagnostics (computed from the scratch stage tables + final panel)
# ────────────────────────────────────────────────────────────────────────────
def stage_diagnostics() -> dict:
    """Diagnostics that need the (gvkey, iid)-level month-end stage table."""
    out: dict = {}
    # distinct currencies actually appearing at month-end, by source
    out["curcdd_counts"] = q(f"""
        SELECT curcdd, count() AS n_rows, uniqExact(gvkey) AS n_gvkey
        FROM {T_ME} GROUP BY curcdd ORDER BY n_rows DESC
        SETTINGS max_execution_time=300, max_rows_to_read=100000000,
                 timeout_before_checking_execution_speed=0
    """)
    # ajexdi / cshoc data quality at month-end
    out["field_quality"] = q(f"""
        SELECT
          count() AS n_rows,
          countIf(ajexdi IS NULL OR ajexdi <= 0) AS ajexdi_bad,
          countIf(cshoc  IS NULL OR cshoc  <= 0) AS cshoc_bad,
          countIf(ret_local IS NOT NULL) AS n_ret_local
        FROM {T_ME}
        SETTINGS max_execution_time=300, max_rows_to_read=100000000,
                 timeout_before_checking_execution_speed=0
    """)
    # unique securities / firms overall (stage keeps iid)
    out["ids"] = q(f"""
        SELECT uniqExact(concat(gvkey,'_',iid)) AS n_sec,
               uniqExact(gvkey) AS n_gvkey,
               count() AS n_rows
        FROM {T_ME}
        SETTINGS max_execution_time=300, max_rows_to_read=100000000,
                 timeout_before_checking_execution_speed=0
    """)
    # Canadian multi-issue duplication: (gvkey, month) with >1 iid
    out["canada_dup"] = q(f"""
        SELECT countIf(n_iid > 1) AS gvkey_month_dup, count() AS gvkey_month_total,
               sum(n_iid) AS total_rows
        FROM (
          SELECT gvkey, month, uniqExact(iid) AS n_iid
          FROM {T_ME} WHERE country = 'CAN'
          GROUP BY gvkey, month
        )
        SETTINGS max_execution_time=300, max_rows_to_read=100000000,
                 timeout_before_checking_execution_speed=0
    """)
    out["canada_ids"] = q(f"""
        SELECT uniqExact(gvkey) AS n_gvkey,
               uniqExact(concat(gvkey,'_',iid)) AS n_sec
        FROM {T_ME} WHERE country = 'CAN'
        SETTINGS max_execution_time=300, max_rows_to_read=100000000,
                 timeout_before_checking_execution_speed=0
    """)
    # FX currencies present vs currencies covered by the FX table
    out["fx_currencies"] = q(f"""
        SELECT cur, count() AS n_months, min(month) AS first_m, max(month) AS last_m
        FROM {T_FX} GROUP BY cur ORDER BY cur
        SETTINGS max_execution_time=120, max_rows_to_read=1000000,
                 timeout_before_checking_execution_speed=0
    """)
    return out


def firm_counts(panel: pd.DataFrame) -> dict:
    """Unique gvkey per country (full period) and for selected years."""
    df = panel[["gvkey", "country", "month"]].copy()
    df["year"] = df["month"].dt.year
    by_country_full = (df.groupby("country")["gvkey"].nunique()
                       .reindex(COUNTRIES_13 + ["CAN"]).rename("n_firms"))
    years = [1985, 1990, 1995, 2000, 2005]
    by_year_country = {}
    for y in years:
        sub = df[df["year"] == y]
        by_year_country[y] = sub.groupby("country")["gvkey"].nunique()
    by_year_total = {y: int(df[df["year"] == y]["gvkey"].nunique()) for y in years}
    by_year_table = pd.DataFrame(by_year_country).reindex(COUNTRIES_13 + ["CAN"])
    by_year_table.loc["TOTAL"] = [by_year_total[y] for y in years]
    return {"by_country_full": by_country_full, "by_year_table": by_year_table,
            "total_unique_gvkey": int(df["gvkey"].nunique())}


def report_diagnostics(panel: pd.DataFrame) -> dict:
    out: dict = {}
    out["n_rows"] = int(len(panel))
    out["month_min"] = str(panel["month"].min().date())
    out["month_max"] = str(panel["month"].max().date())
    out["n_months"] = int(panel["month"].nunique())
    out["n_gvkey"] = int(panel["gvkey"].nunique())
    # monthly cross-section size over 1985-02 .. 2006-06 (non-missing ret_usd)
    rep = panel[(panel["month"] >= REPORT_START) & (panel["month"] <= DATA_END)]
    xs = rep[rep["ret_usd"].notna()].groupby("month").size()
    out["xs_n_months"] = int(xs.shape[0])
    out["xs_min"] = int(xs.min()) if len(xs) else 0
    out["xs_mean"] = float(xs.mean()) if len(xs) else 0.0
    out["xs_max"] = int(xs.max()) if len(xs) else 0
    out["firm_months_report"] = int(len(rep))
    # ret_usd summary
    r = panel["ret_usd"]
    out["ret_usd"] = {
        "mean": float(r.mean()), "std": float(r.std()),
        "p1": float(r.quantile(0.01)), "p5": float(r.quantile(0.05)),
        "p50": float(r.quantile(0.50)), "p95": float(r.quantile(0.95)),
        "p99": float(r.quantile(0.99)),
        "null_frac": float(r.isna().mean()),
        "min": float(r.min()), "max": float(r.max()),
    }
    out["ret_usd_beyond"] = int(((r < -0.99) | (r > 10)).sum())
    # ret_local summary (for anomaly comparison)
    rl = panel["ret_local"]
    out["ret_local_beyond"] = int(((rl < -0.99) | (rl > 10)).sum())
    out["ret_local_null_frac"] = float(rl.isna().mean())
    # me_usd summary
    m = panel["me_usd"]
    out["me_usd"] = {
        "mean": float(m.mean()), "median": float(m.median()),
        "p10": float(m.quantile(0.10)), "p90": float(m.quantile(0.90)),
        "null_frac": float(m.isna().mean()),
    }
    return out


def verify_anchors(panel: pd.DataFrame) -> dict:
    """Verify the Replicator's sanity anchors on the built panel."""
    out: dict = {}
    # NTT (gvkey 007908) me_usd at 2000-06-30 ~ 2.1e11 USD
    ntt = panel[(panel["gvkey"] == "007908") & (panel["month"] == "2000-06-30")]
    if len(ntt):
        out["ntt_me_usd_2000_06"] = float(ntt["me_usd"].iloc[0])
        out["ntt_curcdd"] = str(ntt["curcdd"].iloc[0])
    else:
        out["ntt_me_usd_2000_06"] = None
    # JPY/USD around Jan 2000 from the FX table (~105-107)
    fx = q(f"""
        SELECT month, usd_per_x FROM {T_FX}
        WHERE cur='JPY' AND month BETWEEN '1999-12-31' AND '2000-01-31'
        ORDER BY month
        SETTINGS max_execution_time=60, max_rows_to_read=1000000,
                 timeout_before_checking_execution_speed=0
    """)
    if len(fx):
        # usd_per_x = USD/JPY; JPY/USD = 1/usd_per_x
        fx["jpy_per_usd"] = 1.0 / fx["usd_per_x"].astype(float)
        out["jpy_per_usd_2000_01"] = fx.to_dict("records")
    return out


# ────────────────────────────────────────────────────────────────────────────
# Reporting
# ────────────────────────────────────────────────────────────────────────────
def write_diagnostics_md(rep: dict, firms: dict, stage: dict,
                         anchors: dict, panel: pd.DataFrame) -> None:
    L: list[str] = []
    A = L.append
    A("# Panel diagnostics — seasonality_international_evidence (Heston & Sadka 2010)\n")
    A(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    A("\n## 1. Panel dimensions")
    A(f"- rows: {rep['n_rows']:,}")
    A(f"- month range: {rep['month_min']} .. {rep['month_max']}")
    A(f"- unique months: {rep['n_months']}")
    A(f"- unique firms (gvkey): {rep['n_gvkey']:,}")
    ids = stage["ids"].iloc[0]
    A(f"- unique securities (gvkey,iid) [stage]: {int(ids['n_sec']):,}")
    A(f"- unique gvkey [stage]: {int(ids['n_gvkey']):,}")
    A(f"- firm-month obs over 1985-02..2006-06: {rep['firm_months_report']:,} "
      f"(paper Table 1: {PAPER_FIRM_MONTHS:,})")

    A("\n## 2. Unique firms (gvkey) per country — full period vs paper Table 1")
    A("| country | this panel | paper Table 1 |")
    A("|---|---:|---:|")
    bf = firms["by_country_full"]
    for ctry in COUNTRIES_13 + ["CAN"]:
        mine = int(bf.get(ctry, 0))
        paper = PAPER_FIRMS_BY_COUNTRY.get(ctry, "—")
        A(f"| {ctry} | {mine:,} | {paper} |")
    A(f"| **TOTAL** | **{firms['total_unique_gvkey']:,}** | **{PAPER_FIRMS_TOTAL:,}** |")

    A("\n### Firms in sample per year (unique gvkey with a month-end obs that year)")
    A(firms["by_year_table"].to_markdown())

    A("\n## 3. Monthly cross-section size (non-missing ret_usd), 1985-02..2006-06")
    A(f"- months: {rep['xs_n_months']}")
    A(f"- min/mean/max stocks per month: {rep['xs_min']:,} / "
      f"{rep['xs_mean']:,.0f} / {rep['xs_max']:,}")

    A("\n## 4. ret_usd summary stats")
    ru = rep["ret_usd"]
    A(f"- mean={ru['mean']:.5f} std={ru['std']:.5f}")
    A(f"- p1={ru['p1']:.4f} p5={ru['p5']:.4f} p50={ru['p50']:.4f} "
      f"p95={ru['p95']:.4f} p99={ru['p99']:.4f}")
    A(f"- min={ru['min']:.4f} max={ru['max']:.4f}")
    A(f"- null fraction={ru['null_frac']:.4f}")
    A(f"- ret_usd beyond [-0.99, 10]: {rep['ret_usd_beyond']:,}")
    A(f"- ret_local beyond [-0.99, 10]: {rep['ret_local_beyond']:,} "
      f"(ret_local null frac={rep['ret_local_null_frac']:.4f})")

    A("\n## 5. me_usd summary stats (USD)")
    mu = rep["me_usd"]
    A(f"- mean={mu['mean']:.3e} median={mu['median']:.3e}")
    A(f"- p10={mu['p10']:.3e} p90={mu['p90']:.3e}")
    A(f"- null fraction={mu['null_frac']:.4f}")

    A("\n## 6. FX coverage & anomalies")
    A("### Currencies appearing at month-end (curcdd)")
    A(stage["curcdd_counts"].to_markdown(index=False))
    A("\n### Month-end field quality")
    A(stage["field_quality"].to_markdown(index=False))
    A("\n### FX table currencies (usd_per_x coverage)")
    A(stage["fx_currencies"].to_markdown(index=False))
    # currencies in curcdd lacking FX coverage
    panel_curs = set(panel["curcdd"].dropna().unique())
    fx_curs = set(stage["fx_currencies"]["cur"])
    missing_fx = sorted(panel_curs - fx_curs)
    A(f"\n- curcdd values with NO FX series in the panel window: {missing_fx}")
    cd = stage["canada_dup"].iloc[0]
    ci = stage["canada_ids"].iloc[0]
    A(f"\n### Canada multi-issue duplication (output has gvkey only, no iid)")
    A(f"- Canadian (gvkey, month) groups with >1 iid: {int(cd['gvkey_month_dup']):,} "
      f"of {int(cd['gvkey_month_total']):,}")
    A(f"- extra rows from multi-issue firms: "
      f"{int(cd['total_rows'])-int(cd['gvkey_month_total']):,}")
    A(f"- Canadian unique gvkey: {int(ci['n_gvkey']):,}; "
      f"unique (gvkey,iid): {int(ci['n_sec']):,}")

    A("\n## 7. Anchor verification")
    A(f"- NTT (007908) me_usd @ 2000-06-30 = {anchors.get('ntt_me_usd_2000_06')} "
      f"(curcdd={anchors.get('ntt_curcdd')}); expected ~2.1e11 USD")
    jp = anchors.get("jpy_per_usd_2000_01")
    if jp:
        for row in jp:
            A(f"- FX {row['month']}: USD/JPY={row['usd_per_x']:.6f} "
              f"=> JPY/USD={row['jpy_per_usd']:.2f} (expected ~105-107)")

    (LAYOUT.result_path("diagnostics.md")).write_text("\n".join(L))
    print("  wrote results/diagnostics.md")


# ────────────────────────────────────────────────────────────────────────────
# main
# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    keep_stage = "--keep-stage" in sys.argv
    t_start = time.time()

    build_stage_tables()

    print("Computing stage diagnostics...")
    stage = stage_diagnostics()

    panel = build_panel()

    out_path = LAYOUT.data_path("panel.parquet")
    panel.to_parquet(out_path, index=False)
    print(f"  wrote {out_path}  ({len(panel):,} rows x {panel.shape[1]} cols)")

    print("Computing report diagnostics...")
    rep = report_diagnostics(panel)
    firms = firm_counts(panel)
    anchors = verify_anchors(panel)

    write_diagnostics_md(rep, firms, stage, anchors, panel)

    if not keep_stage:
        c = _client(120)
        c.execute(f"DROP TABLE IF EXISTS {T_ME}")
        c.execute(f"DROP TABLE IF EXISTS {T_FX}")
        print("  dropped scratch tables (use --keep-stage to retain)")

    print(f"\nDONE in {time.time()-t_start:.1f}s")
    print(json.dumps({
        "n_rows": rep["n_rows"], "n_gvkey": rep["n_gvkey"],
        "months": [rep["month_min"], rep["month_max"]],
        "xs_mean": round(rep["xs_mean"], 1),
        "ret_usd_mean": round(rep["ret_usd"]["mean"], 5),
        "me_usd_median": rep["me_usd"]["median"],
        "ntt_me_usd_2000_06": anchors.get("ntt_me_usd_2000_06"),
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
