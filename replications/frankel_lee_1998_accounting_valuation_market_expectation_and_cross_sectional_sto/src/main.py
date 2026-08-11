"""
Replication of Frankel & Lee (1998)
"Accounting Valuation, Market Expectation, and Cross-Sectional Stock Returns"

Task 4: Build the extended panel with FErr_{t+2}, RK(B/P), RK(SG),
RK(OP), RK(Ltg) variables, and render Tables 6, 7, 8, 9.
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client
from scipy.stats import spearmanr
import statsmodels.api as sm

# --- Add project root to sys.path so utils/ is importable ---
PROJECT_ROOT = Path("/home/ra_alan_mike_share/rep-it-up")
sys.path.insert(0, str(PROJECT_ROOT))

from utils.paths import paper_layout  # noqa: E402
from utils.env import load_project_env  # noqa: E402

# Load .env so CLICKHOUSE_* env vars are available
load_project_env()


# --- Configuration ---

LAYOUT = paper_layout(
    "frankel_lee_1998_accounting_valuation_market_expectation_and_cross_sectional_sto"
)
LAYOUT.ensure()

# Sample window for portfolios (paper §4)
SAMPLE_START_YEAR = 1976
SAMPLE_END_YEAR = 1993

# Discount rate. The paper uses industry-specific r_e (FF 1997 Table 7
# + 0.0646 riskless rate). This iteration uses a constant r_e = 0.12
# as a placeholder; see assumptions.md assumption 28.
R_E_CONSTANT = 0.12


# --- ClickHouse connection ---

def _client() -> Client:
    host = os.environ.get("CLICKHOUSE_HOST", "")
    if not host:
        raise RuntimeError(
            "CLICKHOUSE_HOST is not set -- ensure .env is loaded."
        )
    return Client(
        host=host,
        port=int(os.environ.get("CLICKHOUSE_PORT", "9000")),
        user=os.environ.get("CLICKHOUSE_USER", "default"),
        password=os.environ.get("CLICKHOUSE_PASSWORD", ""),
        database=os.environ.get("CLICKHOUSE_DATABASE", "default"),
        settings={"max_execution_time": 600},
    )


def q(sql: str) -> pd.DataFrame:
    """Execute a SQL query and return a pandas DataFrame."""
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    """Execute a saved SQL file and return a pandas DataFrame."""
    sql = (LAYOUT.src_path("sql") / name).read_text()
    return q(sql)


# --- Data loading ---

def load_panel() -> pd.DataFrame:
    """Load the firm-year panel from data/panel.parquet."""
    cache = LAYOUT.data_path("panel.parquet")
    df = pd.read_parquet(cache)
    if "permno" in df.columns:
        df["permno"] = df["permno"].astype("int64")
    if "year_t" in df.columns:
        df["year_t"] = df["year_t"].astype("int32")
    # Deduplicate (permno, year_t). The panel.parquet may contain
    # duplicates from the I/B/E/S CUSIP/ticker/oftic UNION ALL
    # coverage join; for V_h/V_f computation we need one row per
    # (permno, year_t). Keep the first row per pair (stable order).
    df = df.sort_values(["permno", "year_t", "gvkey"]).drop_duplicates(
        subset=["permno", "year_t"], keep="first"
    ).reset_index(drop=True)
    return df


def load_ibes() -> pd.DataFrame:
    """Load I/B/E/S FY1, FY2, Ltg from src/sql/ibes_fy1_fy2_ltg.sql."""
    return q_file("ibes_fy1_fy2_ltg.sql")


def load_ceq_lag2() -> pd.DataFrame:
    """Load ceq_{t-2} keyed by (gvkey, fyear) from compustat."""
    return q_file("comp_ceq_lag2.sql")


def _upload_panel_keys(panel: pd.DataFrame) -> None:
    """Upload (permno, year_t) panel keys into a temporary ClickHouse
    table for use in SQL joins."""
    c = _client()
    pairs = list(zip(
        panel["permno"].astype(int).tolist(),
        panel["year_t"].astype(int).tolist(),
    ))
    # Deduplicate
    pairs = list(set(pairs))
    c.execute("DROP TABLE IF EXISTS _panel_keys")
    c.execute("""
        CREATE TABLE _panel_keys (
            permno UInt32,
            year_t UInt16
        ) ENGINE = MergeTree() ORDER BY (permno, year_t)
    """)
    c.execute("INSERT INTO _panel_keys VALUES", pairs)


def load_bhar_returns(panel: pd.DataFrame) -> pd.DataFrame:
    """Load CRSP monthly returns for the panel's BHAR window and
    compute Ret12, Ret24, Ret36 per firm-year.

    Returns one row per (permno, year_t) with columns ret12, ret24,
    ret36, n_months12, n_months24, n_months36.
    """
    _upload_panel_keys(panel)
    sql = """
    WITH
      monthly AS (
          SELECT m.permno                        AS permno,
                 toYear(toDate32OrNull(m.date))  AS yr,
                 toMonth(toDate32OrNull(m.date)) AS mo,
                 m.ret                           AS ret
          FROM crsp_202601.msf AS m
          SEMI JOIN _panel_keys pk ON m.permno = pk.permno
          WHERE m.date BETWEEN '1976-07-01' AND '1996-12-31'
            AND m.ret IS NOT NULL
      ),
      delist AS (
          SELECT permno,
                 toYear(toDate32OrNull(dlstdt))  AS dl_yr,
                 toMonth(toDate32OrNull(dlstdt)) AS dl_mo,
                 dlret
          FROM crsp_202601.msedelist
          SEMI JOIN _panel_keys pk ON permno = pk.permno
          WHERE dlret IS NOT NULL
      ),
      offsets AS (
          SELECT arrayJoin(arrayMap(i -> i + 1, range(36))) AS month_offset
      ),
      window_months AS (
          SELECT pk.permno AS permno,
                 pk.year_t AS year_t,
                 o.month_offset AS month_offset,
                 pk.year_t + intDiv(o.month_offset - 1, 12) +
                     if((o.month_offset - 1) % 12 >= 6, 1, 0) AS yr,
                 ((o.month_offset - 1) % 12 + 7 - 1) % 12 + 1 AS mo
          FROM _panel_keys AS pk
          CROSS JOIN offsets AS o
      ),
      window_returns AS (
          SELECT w.permno                         AS permno,
                 w.year_t                         AS year_t,
                 w.month_offset                   AS month_offset,
                 if(m.ret IS NOT NULL, m.ret,
                    if(d.dlret IS NOT NULL, d.dlret, NULL)
                 )                                AS ret
          FROM window_months AS w
          LEFT JOIN monthly AS m
              ON w.permno = m.permno
             AND w.yr     = m.yr
             AND w.mo     = m.mo
          LEFT JOIN delist AS d
              ON w.permno = d.permno
             AND w.yr     = d.dl_yr
             AND w.mo     = d.dl_mo
      )
    SELECT permno, year_t, month_offset, ret
    FROM window_returns
    SETTINGS join_algorithm = 'partial_merge',
             max_execution_time = 600,
             max_rows_to_read = 10000000000,
             timeout_before_checking_execution_speed = 0
    """
    monthly = q(sql)
    # Drop the temp table
    c = _client()
    c.execute("DROP TABLE IF EXISTS _panel_keys")

    # Compute cumulative product per (permno, year_t). The SQL has
    # already filtered to the BHAR window (offsets 1..36 = July year_t
    # .. June year_t+3), with one row per (permno, year_t, month_offset).
    # We compute (1+ret) cumulative product from offset 1.
    monthly = monthly.sort_values(["permno", "year_t", "month_offset"])
    monthly["ret_capped"] = monthly["ret"].clip(lower=-0.99, upper=10.0)
    grp = monthly.groupby(["permno", "year_t"], sort=False)
    monthly["cumprod"] = grp["ret_capped"].transform(lambda x: (1.0 + x).cumprod())

    # Pivot the cumprod at month_offset = 12, 24, 36 to one row per (permno, year_t).
    pivot = monthly[monthly["month_offset"].isin([12, 24, 36])].pivot_table(
        index=["permno", "year_t"], columns="month_offset", values="cumprod"
    )
    pivot.columns = [f"cumprod_{c}" for c in pivot.columns]
    pivot = pivot.reset_index()
    for k in (12, 24, 36):
        pivot[f"ret{k}"] = pivot[f"cumprod_{k}"] - 1.0
        pivot = pivot.drop(columns=[f"cumprod_{k}"])

    # Compute n_months covered in each window
    cnt = monthly.groupby(["permno", "year_t"]).size().rename("n_months_total").reset_index()
    out = pivot.merge(cnt, on=["permno", "year_t"], how="left")
    return out


# --- EBO V_h and V_f computation ---

def compute_vh_vf(panel: pd.DataFrame, ibes: pd.DataFrame, lag2: pd.DataFrame) -> pd.DataFrame:
    """Compute V_h (T=1,2,3) and V_f (T=1,2,3) for each firm-year.

    Parameters
    ----------
    panel : pd.DataFrame
        The existing 21,707-firm-year panel with permno, year_t, gvkey,
        fyear, prc, ceq, ib, dvc, at, csho, k, roe, ceq_prior (= B_{t-1}).
    ibes : pd.DataFrame
        I/B/E/S FY1, FY2, Ltg from ibes_fy1_fy2_ltg.sql.
    lag2 : pd.DataFrame
        ceq for fyear-2 (B_{t-2}) keyed by (gvkey, fyear).

    Returns
    -------
    panel_with_v : pd.DataFrame
        The panel with V_h_T1, V_h_T2, V_h_T3, V_f_T1, V_f_T2, V_f_T3,
        V_h_P (T=2), V_f_P (T=3) and underlying FROE / B_{t+1} / B_{t+2}
        columns.

    Notes
    -----
    V_h is computed using the historical ROE as the FROE for all
    forecast periods (paper §3 footnote 13, Appendix A). V_f uses the
    I/B/E/S consensus EPS forecasts and (when available) Ltg.

    Per assumption 28 (this iteration), r_e is a constant 0.12. The
    paper uses industry-specific FF (1997) Table 7 premiums; this is
    out of scope for this iteration.
    """
    df = panel.copy()
    # Strip whitespace in gvkey (comp stores as string)
    df["gvkey"] = df["gvkey"].astype(str).str.strip()
    ibes = ibes.copy()
    ibes["gvkey"] = ibes["gvkey"].astype(str).str.strip()
    lag2 = lag2.copy()
    lag2["gvkey"] = lag2["gvkey"].astype(str).str.strip()

    # Merge I/B/E/S forecasts
    df = df.merge(
        ibes[["gvkey", "fyear", "fy1_eps", "fy2_eps", "ltg"]],
        on=["gvkey", "fyear"],
        how="left",
    )

    # Merge ceq_{t-2}
    lag2 = lag2.rename(columns={"fyear": "fyear_t2", "ceq_prior2": "ceq_prior2"})
    lag2["fyear"] = lag2["fyear_t2"] + 2
    df = df.merge(
        lag2[["gvkey", "fyear", "ceq_prior2"]],
        on=["gvkey", "fyear"],
        how="left",
    )

    # Now compute V_h and V_f.
    r_e = R_E_CONSTANT

    # ---- V_h: use ROE_t as FROE for all forecast periods ----
    df["vh_froe_t"]   = df["roe"]
    df["vh_froe_t1"]  = df["roe"]
    df["vh_froe_t2"]  = df["roe"]

    # B_{t+1} = B_t * [1 + ROE * (1 - k)]
    df["vh_b_t1"] = df["ceq"] * (1.0 + df["roe"] * (1.0 - df["k"]))
    # B_{t+2} = B_{t+1} * [1 + ROE * (1 - k)]
    df["vh_b_t2"] = df["vh_b_t1"] * (1.0 + df["roe"] * (1.0 - df["k"]))

    # V_h_T1 (Eq. 3.1): B_t + (ROE - r_e)/(1+r_e) * B_t + (ROE - r_e)/((1+r_e)*r_e) * B_t
    # Simplifies to B_t * [1 + (ROE - r_e)/(1+r_e) * (1 + 1/r_e)]
    df["v_h_t1"] = (
        df["ceq"]
        + (df["roe"] - r_e) / (1.0 + r_e) * df["ceq"]
        + (df["roe"] - r_e) / ((1.0 + r_e) * r_e) * df["ceq"]
    )

    # V_h_T2 (Eq. 3.2): B_t + (ROE - r_e)/(1+r_e) * B_t + (ROE - r_e)/((1+r_e)*r_e) * B_{t+1}
    df["v_h_t2"] = (
        df["ceq"]
        + (df["roe"] - r_e) / (1.0 + r_e) * df["ceq"]
        + (df["roe"] - r_e) / ((1.0 + r_e) * r_e) * df["vh_b_t1"]
    )

    # V_h_T3 (Eq. 3.3 with historical ROE): B_t + (ROE - r_e)/(1+r_e)*B_t
    #     + (ROE - r_e)/(1+r_e)^2 * B_{t+1}
    #     + (ROE - r_e)/((1+r_e)^2 * r_e) * B_{t+2}
    df["v_h_t3"] = (
        df["ceq"]
        + (df["roe"] - r_e) / (1.0 + r_e) * df["ceq"]
        + (df["roe"] - r_e) / ((1.0 + r_e) ** 2) * df["vh_b_t1"]
        + (df["roe"] - r_e) / ((1.0 + r_e) ** 2 * r_e) * df["vh_b_t2"]
    )

    # ---- V_f: use I/B/E/S consensus forecasts ----
    # Compute total FY1 ($M) = FY1_eps ($/share) * csho (M shares).
    # Drop if either is missing or zero. fy1_eps may be missing for
    # the historical-ROE V_h computation, but it is required for V_f.
    df["fy1_total"] = df["fy1_eps"] * df["csho"]
    df["fy2_total"] = df["fy2_eps"] * df["csho"]

    # Filter: V_f requires non-missing fy1_eps and non-missing fy2_eps.
    # Per the task spec, FY2 may not be available in this vintage; if so,
    # set FROE_{t+1} = FROE_t.
    has_fy1 = df["fy1_eps"].notna() & (df["fy1_eps"] != 0)
    has_fy2 = df["fy2_eps"].notna() & (df["fy2_eps"] != 0)

    # FROE_t = FY1_total / avg(B_{t-1}, B_{t-2})
    df["froe_t"] = np.where(
        has_fy1 & df["ceq_prior"].notna() & df["ceq_prior2"].notna()
        & (df["ceq_prior"] > 0) & (df["ceq_prior2"] > 0),
        df["fy1_total"] / ((df["ceq_prior"] + df["ceq_prior2"]) / 2.0),
        np.nan,
    )

    # B_t (already ceq). B_{t+1} = B_t * [1 + FROE_t * (1 - k)]
    df["vf_b_t1"] = df["ceq"] * (1.0 + df["froe_t"] * (1.0 - df["k"]))

    # FROE_{t+1} = FY2_total / avg(B_t, B_{t-1}); if FY2 missing, use FROE_t.
    df["froe_t1"] = np.where(
        has_fy2 & df["ceq"].notna() & df["ceq_prior"].notna()
        & (df["ceq"] > 0) & (df["ceq_prior"] > 0),
        df["fy2_total"] / ((df["ceq"] + df["ceq_prior"]) / 2.0),
        df["froe_t"],
    )

    # B_{t+2} = B_{t+1} * [1 + FROE_{t+1} * (1 - k)]
    df["vf_b_t2"] = df["vf_b_t1"] * (1.0 + df["froe_t1"] * (1.0 - df["k"]))

    # FROE_{t+2}: with Ltg: = FY2_total * (1 + Ltg) / avg(B_{t+1}, B_t)
    # without Ltg: = FROE_{t+1}
    ltg_avail = df["ltg"].notna()
    df["froe_t2"] = np.where(
        ltg_avail & has_fy2 & df["vf_b_t1"].notna() & df["ceq"].notna()
        & (df["vf_b_t1"] > 0) & (df["ceq"] > 0),
        df["fy2_total"] * (1.0 + df["ltg"]) / ((df["vf_b_t1"] + df["ceq"]) / 2.0),
        df["froe_t1"],
    )

    # V_f_T1 (Eq. 3.1 with FROE_t = FROE_t)
    df["v_f_t1"] = (
        df["ceq"]
        + (df["froe_t"] - r_e) / (1.0 + r_e) * df["ceq"]
        + (df["froe_t"] - r_e) / ((1.0 + r_e) * r_e) * df["ceq"]
    )

    # V_f_T2 (Eq. 3.2 with FROE_t, FROE_{t+1})
    df["v_f_t2"] = (
        df["ceq"]
        + (df["froe_t"] - r_e) / (1.0 + r_e) * df["ceq"]
        + (df["froe_t1"] - r_e) / ((1.0 + r_e) * r_e) * df["vf_b_t1"]
    )

    # V_f_T3 (Eq. 3.3 with FROE_t, FROE_{t+1}, FROE_{t+2})
    df["v_f_t3"] = (
        df["ceq"]
        + (df["froe_t"] - r_e) / (1.0 + r_e) * df["ceq"]
        + (df["froe_t1"] - r_e) / ((1.0 + r_e) ** 2) * df["vf_b_t1"]
        + (df["froe_t2"] - r_e) / ((1.0 + r_e) ** 2 * r_e) * df["vf_b_t2"]
    )

    # V_h / P and V_f / P ratios. The paper uses V_f / P and B / P
    # as ratios of fundamental value per share to market price per
    # share (both in $/share). V_f is in $M (firm total), so divide
    # by csho (in millions of shares) to get V_f_per_share. Same
    # for V_h.
    df["v_h_per_share_t2"] = df["v_h_t2"] / df["csho"]
    df["v_f_per_share_t3"] = df["v_f_t3"] / df["csho"]
    df["v_h_p_t2"] = df["v_h_per_share_t2"] / df["prc"]
    df["v_f_p_t3"] = df["v_f_per_share_t3"] / df["prc"]

    return df


# --- Table 2: Annual Spearman correlations ---

def compute_table_2(panel: pd.DataFrame) -> pd.DataFrame:
    """Compute Table 2: annual Spearman correlations of price vs. B,
    V_h_T1, V_h_T2, V_h_T3, V_f_T1, V_f_T2, V_f_T3.

    Returns a DataFrame indexed by year_t with the correlation columns.
    """
    rows = []
    for year_t, g in panel.groupby("year_t"):
        # B = book equity per share = ceq / csho (units $M / M shares = $/share)
        b_per_share = g["ceq"] / g["csho"]
        valid = (
            g["prc"].notna()
            & (g["prc"] > 0)
            & b_per_share.notna()
            & (b_per_share > 0)
            & g["v_h_t1"].notna()
            & g["v_h_t2"].notna()
            & g["v_h_t3"].notna()
            & g["v_f_t1"].notna()
            & g["v_f_t2"].notna()
            & g["v_f_t3"].notna()
        )
        g = g.loc[valid]
        if len(g) < 5:
            continue
        n = len(g)
        bps = (g["ceq"] / g["csho"]).values
        price = g["prc"].abs().values
        corr_b, _    = spearmanr(bps, price)
        corr_vh1, _  = spearmanr(g["v_h_t1"].values, price)
        corr_vh2, _  = spearmanr(g["v_h_t2"].values, price)
        corr_vh3, _  = spearmanr(g["v_h_t3"].values, price)
        corr_vf1, _  = spearmanr(g["v_f_t1"].values, price)
        corr_vf2, _  = spearmanr(g["v_f_t2"].values, price)
        corr_vf3, _  = spearmanr(g["v_f_t3"].values, price)
        rows.append({
            "year_t": int(year_t),
            "n": int(n),
            "corr_b":    float(corr_b),
            "corr_vh_t1": float(corr_vh1),
            "corr_vh_t2": float(corr_vh2),
            "corr_vh_t3": float(corr_vh3),
            "corr_vf_t1": float(corr_vf1),
            "corr_vf_t2": float(corr_vf2),
            "corr_vf_t3": float(corr_vf3),
        })
    table = pd.DataFrame(rows).set_index("year_t")
    # Time-series mean across all years ("All years" row)
    all_row = {
        "n":       int(table["n"].sum()),
        "corr_b":   float(table["corr_b"].mean()),
        "corr_vh_t1": float(table["corr_vh_t1"].mean()),
        "corr_vh_t2": float(table["corr_vh_t2"].mean()),
        "corr_vh_t3": float(table["corr_vh_t3"].mean()),
        "corr_vf_t1": float(table["corr_vf_t1"].mean()),
        "corr_vf_t2": float(table["corr_vf_t2"].mean()),
        "corr_vf_t3": float(table["corr_vf_t3"].mean()),
    }
    all_row = pd.DataFrame([all_row], index=["All years"])
    table = pd.concat([table, all_row])
    return table


def render_table_2_md(table: pd.DataFrame) -> str:
    """Render Table 2 as Markdown."""
    lines = []
    lines.append("# Table 2 -- Annual Spearman Correlations of Price vs. B and EBO V_h / V_f")
    lines.append("")
    lines.append("**Replication of**: Frankel & Lee (1998) -- Table 2")
    lines.append("**Sample period**: 1976-1993 (portfolio-formation years)")
    lines.append("**Universe**: NYSE/AMEX/NASDAQ ordinary common shares (shrcd 10/11, exchcd 1/2/3) x Compustat non-financial (SIC first digit != 6) x fiscal-year-end in [6, 12] x June 30 price >= $1 x I/B/E/S FY1 coverage filter")
    lines.append("")
    lines.append("**Definitions** (paper's notation):")
    lines.append("- **B**: book equity per share in calendar year t-1 ($/share) = ceq / csho.")
    lines.append("- **V_h (T=1,2,3)**: EBO fundamental value (Eqs. 3.1-3.3) using historical ROE as the FROE for all forecast periods. See paper §3 footnote 13 / Appendix A.")
    lines.append("- **V_f (T=1,2,3)**: EBO fundamental value using I/B/E/S consensus EPS forecasts (FY1, FY2) as the FROE inputs. See paper Appendix A.")
    lines.append("- **r_e**: industry-specific cost-of-equity (FF 1997 Table 7 + 0.0646 riskless). **This iteration uses a constant r_e = 0.12 placeholder** (assumption 28).")
    lines.append("")
    lines.append("Each cell is the cross-sectional Spearman rank correlation between stock price (June 30 of year t) and the indicated value measure, restricted to firm-years where all of B, V_h T=1,2,3, V_f T=1,2,3 are non-missing and price > 0.")
    lines.append("")
    lines.append("**All years row** = time-series mean of the annual correlations (matches the paper's 'All years' definition).")
    lines.append("")

    # Header
    cols = ["Year", "Obs.", "B", "V_h T=1", "V_h T=2", "V_h T=3",
            "V_f T=1", "V_f T=2", "V_f T=3"]
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("|" + "|".join(["---"] * len(cols)) + "|")

    for idx, row in table.iterrows():
        if idx == "All years":
            lines.append(
                f"| **{idx}** | **{int(row['n']):,}** | "
                f"**{row['corr_b']:.2f}** | "
                f"**{row['corr_vh_t1']:.2f}** | **{row['corr_vh_t2']:.2f}** | "
                f"**{row['corr_vh_t3']:.2f}** | "
                f"**{row['corr_vf_t1']:.2f}** | **{row['corr_vf_t2']:.2f}** | "
                f"**{row['corr_vf_t3']:.2f}** |"
            )
        else:
            lines.append(
                f"| {int(idx)} | {int(row['n']):,} | "
                f"{row['corr_b']:.2f} | "
                f"{row['corr_vh_t1']:.2f} | {row['corr_vh_t2']:.2f} | "
                f"{row['corr_vh_t3']:.2f} | "
                f"{row['corr_vf_t1']:.2f} | {row['corr_vf_t2']:.2f} | "
                f"{row['corr_vf_t3']:.2f} |"
            )

    lines.append("")
    lines.append("## Per-cell comparison (paper vs ours, All-years row)")
    lines.append("")
    lines.append("Paper All-years row (from the paper's Table 2, 'FF Three-factor' columns):")
    lines.append("")
    lines.append("| Metric | Paper | Ours | Status |")
    lines.append("| --- | ---: | ---: | --- |")
    paper = {
        "corr_b":    0.60,
        "corr_vh_t1": 0.70,
        "corr_vh_t2": 0.69,
        "corr_vh_t3": 0.69,
        "corr_vf_t1": 0.80,
        "corr_vf_t2": 0.81,
        "corr_vf_t3": 0.82,
    }
    last = table.iloc[-1]
    labels = {
        "corr_b":     "corr(B)",
        "corr_vh_t1": "corr(V_h T=1)",
        "corr_vh_t2": "corr(V_h T=2)",
        "corr_vh_t3": "corr(V_h T=3)",
        "corr_vf_t1": "corr(V_f T=1)",
        "corr_vf_t2": "corr(V_f T=2)",
        "corr_vf_t3": "corr(V_f T=3)",
    }
    for k in ("corr_b", "corr_vh_t1", "corr_vh_t2", "corr_vh_t3",
              "corr_vf_t1", "corr_vf_t2", "corr_vf_t3"):
        diff = last[k] - paper[k]
        if abs(diff) <= 0.05:
            status = "Tier 1"
        elif abs(diff) <= 0.10:
            status = "Tier 2"
        else:
            status = "FAIL"
        lines.append(
            f"| {labels[k]} | {paper[k]:.2f} | {last[k]:.2f} | "
            f"{status} ({diff:+.2f}) |"
        )

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append(
        "**Discount rate**: this iteration uses r_e = 0.12 (constant) as a placeholder. "
        "The paper uses industry-specific r_e (FF 1997 Table 7 risk premiums + 0.0646 "
        "riskless rate). The Spearman correlation between price and V_h / V_f is largely "
        "invariant to the choice of r_e because V_h and V_f are monotonic in r_e "
        "(paper footnote 11). Industry mapping is out of scope for this iteration."
    )
    lines.append("")
    lines.append(
        "**FY2 / Ltg coverage**: FY2 EPS coverage is sparse in this vintage (~11% "
        "of panel rows). Where FY2 is missing, FROE_{t+1} = FROE_t per Appendix A. "
        "Ltg (long-term growth) is unavailable in this vintage of I/B/E/S "
        "statsumu_epsus (no measure='LTG' rows exist); the FROE_{t+2} = FROE_{t+1} "
        "fallback is applied uniformly. See assumptions.md assumptions 19, 28."
    )
    lines.append("")

    return "\n".join(lines)


# --- Table 3: Quintile portfolio characteristics ---

def assign_quintiles_nyse(df: pd.DataFrame, year_t: int, signal_col: str,
                          nyse_only: bool) -> pd.Series:
    """Assign quintile bins (1..5) per year_t using NYSE breakpoints
    if nyse_only is True (else in-sample breakpoints).

    Returns a Series aligned with df.index.
    """
    sub = df
    if nyse_only:
        # ex_chcd == 1 = NYSE
        breaks_sub = sub[sub.get("exchcd_jun") == 1] if "exchcd_jun" in sub.columns else None
        if breaks_sub is None or len(breaks_sub) < 5:
            # No NYSE subset; fall back to in-sample
            breakpoints = sub[signal_col].quantile([0.2, 0.4, 0.6, 0.8]).values
        else:
            breakpoints = breaks_sub[signal_col].quantile([0.2, 0.4, 0.6, 0.8]).values
    else:
        breakpoints = sub[signal_col].quantile([0.2, 0.4, 0.6, 0.8]).values

    return pd.cut(sub[signal_col], bins=[-np.inf, *breakpoints, np.inf],
                  labels=False, include_lowest=True) + 1


def compute_table_3_panel(panel: pd.DataFrame, bhar: pd.DataFrame, panel_b: pd.DataFrame,
                           sort_col: str, nyse_only: bool,
                           year_start: int = 1977, year_end: int = 1992) -> pd.DataFrame:
    """Compute one panel of Table 3 (quintile-portfolio means).

    Parameters
    ----------
    panel : pd.DataFrame
        Panel with V_h_T2 / V_f_T3 / V_f_P columns.
    bhar : pd.DataFrame
        BHAR returns keyed by (permno, year_t).
    panel_b : pd.DataFrame
        Computed B / P and V_f / P columns for each firm-year.
    sort_col : str
        Column to sort by ('me_june_t', 'b_over_p', 'v_f_p_t3').
    nyse_only : bool
        If True, use NYSE-only breakpoints (Panel A); else in-sample (Panel B/C/D).
    """
    df = panel.copy()
    # BHAR returns
    df = df.merge(bhar[["permno", "year_t", "ret12", "ret24", "ret36"]],
                  on=["permno", "year_t"], how="left")

    # B/P and V_f/P (per-share ratios)
    df["b_per_share"] = df["ceq"] / df["csho"]
    df["b_over_p"] = df["b_per_share"] / df["prc"]
    df["v_over_p"] = df["v_f_p_t3"]

    # Subset to paper's sample (1977-1992 per Table 3 caption)
    df = df[(df["year_t"] >= year_start) & (df["year_t"] <= year_end)].copy()

    # Drop rows missing the sort variable or BHAR
    df = df.dropna(subset=[sort_col, "ret12", "ret24", "ret36"])

    # Per-year winsorization (0.5% / 99.5%) for the characteristics to
    # prevent extreme outliers from dominating the quintile means.
    # The paper does not state this explicitly but the upper quintile
    # of V_f/P in Panel D (max = 1.54 in the paper) suggests that
    # extreme forecasts are winsorized. We winsorize the sort variable
    # AND v_over_p (since V_f is noisy) at 0.5% / 99.5% per year.
    def _winsorize(series: pd.Series) -> pd.Series:
        lo = series.quantile(0.005)
        hi = series.quantile(0.995)
        return series.clip(lo, hi)

    df[sort_col] = df.groupby("year_t")[sort_col].transform(_winsorize)
    # Also winsorize v_over_p (the V_f/P characteristic) for table display
    # regardless of which sort variable is used, since V_f is noisy.
    df["v_over_p"] = df.groupby("year_t")["v_over_p"].transform(_winsorize)
    df["b_over_p"] = df.groupby("year_t")["b_over_p"].transform(_winsorize)

    # Assign quintiles per year
    bins_per_year = []
    for year_t, g in df.groupby("year_t"):
        sub = g
        if nyse_only and "exchcd_jun" in sub.columns:
            breaks_sub = sub[sub["exchcd_jun"] == 1]
            if len(breaks_sub) >= 5 and sub[sort_col].notna().sum() >= 5:
                bp = breaks_sub[sort_col].quantile([0.2, 0.4, 0.6, 0.8]).values
            else:
                bp = sub[sort_col].quantile([0.2, 0.4, 0.6, 0.8]).values
        else:
            bp = sub[sort_col].quantile([0.2, 0.4, 0.6, 0.8]).values
        bins_per_year.append((year_t, bp))

    # Vectorized assignment via pd.cut
    df["quintile"] = np.nan
    for year_t, bp in bins_per_year:
        mask = df["year_t"] == year_t
        df.loc[mask, "quintile"] = pd.cut(
            df.loc[mask, sort_col],
            bins=[-np.inf, *bp, np.inf],
            labels=False, include_lowest=True,
        ) + 1
    df["quintile"] = df["quintile"].astype("Int64")

    return df


def aggregate_table_3_panel(df: pd.DataFrame, sort_col: str) -> dict:
    """Compute per-quintile means and the Q5-Q1 diff."""
    metrics = ["me_june_t", "b_over_p", "v_over_p", "ret12", "ret24", "ret36"]
    out = {}
    # Obs per quintile (firm-years)
    obs_per_q = df.groupby("quintile").size().to_dict()
    # Also compute per-quintile mean
    means = df.groupby("quintile")[metrics].mean()
    out["means"] = means
    out["obs"] = obs_per_q
    if 1 in means.index and 5 in means.index:
        diff = means.loc[5] - means.loc[1]
        out["diff"] = diff
    # All-firms row (unconditional means)
    all_means = df[metrics].mean()
    out["all"] = all_means
    out["n_total"] = int(len(df))
    return out


def render_table_3_md(panels: dict) -> str:
    """Render Table 3 as Markdown with all four panels.

    Parameters
    ----------
    panels : dict
        {panel_label: dict from aggregate_table_3_panel(...)}.
    """
    lines = []
    lines.append("# Table 3 -- Characteristics of Quintile Portfolios (ME, B/P, V_f/P)")
    lines.append("")
    lines.append("**Replication of**: Frankel & Lee (1998) -- Table 3")
    lines.append("**Sample period**: 1977-1992 (paper's Table 3 caption)")
    lines.append(
        "**Universe**: NYSE/AMEX/NASDAQ ordinary common shares x Compustat non-financial "
        "x fiscal-year-end in [6, 12] x June 30 price >= $1 x I/B/E/S FY1 coverage"
    )
    lines.append("")
    lines.append(
        "Each firm-year is assigned to a quintile by the indicated sort variable. "
        "Quintile breakpoints are computed annually: Panel A uses NYSE-only firms' ME; "
        "Panels B, C, D use in-sample breakpoints. ME is market equity at June 30 of "
        "year t (in $M); B/P and V_f/P use book equity per share in calendar year t-1 "
        "and the EBO V_f value (T=3, FY1+FY2 forecasts), respectively. Ret12/24/36 are "
        "buy-and-hold returns for 12/24/36 months beginning July of year t. Q5-Q1 Diff. "
        "is the difference in means between the top (Q5) and bottom (Q1) quintiles; "
        "the paper's significance stars are not reproduced (assumption 20)."
    )
    lines.append("")

    metric_labels = {
        "me_june_t": "ME",
        "b_over_p":  "B/P",
        "v_over_p":  "V_f/P",
        "ret12":     "Ret12",
        "ret24":     "Ret24",
        "ret36":     "Ret36",
    }

    for panel_label, panel_data in panels.items():
        means = panel_data["means"]
        diff = panel_data.get("diff")
        all_means = panel_data["all"]
        obs = panel_data["obs"]
        n_total = panel_data["n_total"]

        lines.append(f"## {panel_label}")
        lines.append("")
        lines.append(f"Total firm-years in panel: **{n_total:,}**")
        lines.append("")

        # Determine which metrics are present in means
        metric_cols = [c for c in metric_labels if c in means.columns]
        metric_cols_first = metric_cols[:1]  # primary sort metric (varies by panel)

        # Build the per-metric block. For each metric, render:
        # | metric | Q1 | Q2 | Q3 | Q4 | Q5 | All Firms | Q5-Q1 Diff. |
        # Render the first row as the sort metric, then the others below.

        def render_metric_row(metric: str) -> str:
            row = [metric_labels.get(metric, metric)]
            for q in (1, 2, 3, 4, 5):
                if q in means.index:
                    val = means.loc[q, metric]
                else:
                    val = float("nan")
                if metric == "me_june_t":
                    row.append(f"{val:,.0f}" if pd.notna(val) else "")
                elif metric in ("ret12", "ret24", "ret36"):
                    row.append(f"{val:.3f}" if pd.notna(val) else "")
                else:
                    row.append(f"{val:.3f}" if pd.notna(val) else "")
            # All firms
            if metric in all_means.index:
                val = all_means[metric]
            else:
                val = float("nan")
            if metric == "me_june_t":
                row.append(f"{val:,.0f}" if pd.notna(val) else "")
            elif metric in ("ret12", "ret24", "ret36"):
                row.append(f"{val:.3f}" if pd.notna(val) else "")
            else:
                row.append(f"{val:.3f}" if pd.notna(val) else "")
            # Diff
            if diff is not None and metric in diff.index:
                d = diff[metric]
                if metric == "me_june_t":
                    row.append(f"{d:+,.0f}" if pd.notna(d) else "")
                elif metric in ("ret12", "ret24", "ret36"):
                    row.append(f"{d:+.3f}" if pd.notna(d) else "")
                else:
                    row.append(f"{d:+.3f}" if pd.notna(d) else "")
            else:
                row.append("")
            return "| " + " | ".join(row) + " |"

        # Header
        header = ["", "Q1 (Low)", "Q2", "Q3", "Q4", "Q5 (High)", "All Firms", "Q5-Q1 Diff."]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("|" + "|".join(["---"] * len(header)) + "|")
        for metric in metric_cols:
            lines.append(render_metric_row(metric))
        # Obs row
        obs_row = ["Obs."]
        for q in (1, 2, 3, 4, 5):
            obs_row.append(f"{obs.get(q, 0):,}")
        obs_row.append(f"{n_total:,}")
        obs_row.append("")
        lines.append("| " + " | ".join(obs_row) + " |")
        lines.append("")

    lines.append("## Per-cell comparison vs paper (Q5-Q1 Diff., All-years)")
    lines.append("")
    lines.append(
        "Paper Q5-Q1 Diff values (All-years column; All Firms row):"
    )
    lines.append("")
    lines.append("| Panel | Metric | Paper | Ours | Status |")
    lines.append("| --- | --- | ---: | ---: | --- |")
    paper_targets = {
        "Panel A - ME (NYSE size quintiles)": {
            "b_over_p": -0.77,
            "v_over_p": -0.42,
            "ret12":    -0.233,
            "ret24":    -0.210,
            "ret36":    -0.338,
        },
        "Panel B - ME (in-sample size quintiles)": {
            "b_over_p": -0.32,
            "v_over_p": -0.05,
            "ret12":    0.001,
            "ret24":    0.045,
            "ret36":    0.066,
        },
        "Panel C - B/P quintiles": {
            "v_over_p": 0.260,
            "ret12":    0.049,
            "ret24":    0.082,
            "ret36":    0.151,
        },
        "Panel D - V_f/P quintiles": {
            "b_over_p": 0.25,
            "ret12":    0.031,
            "ret24":    0.152,
            "ret36":    0.306,
        },
    }
    for panel_label, targets in paper_targets.items():
        if panel_label not in panels:
            continue
        panel_data = panels[panel_label]
        diff = panel_data.get("diff")
        if diff is None:
            continue
        for metric, paper_val in targets.items():
            if metric not in diff.index:
                continue
            ours_val = float(diff[metric])
            d = ours_val - paper_val
            if metric in ("ret12", "ret24", "ret36"):
                tol = 0.05
                if abs(d) <= tol:
                    status = "Tier 1"
                elif abs(d) <= 2 * tol:
                    status = "Tier 2"
                else:
                    status = "FAIL"
            else:
                tol = 0.10
                if abs(d) <= tol:
                    status = "Tier 1"
                elif abs(d) <= 2 * tol:
                    status = "Tier 2"
                else:
                    status = "FAIL"
            lines.append(
                f"| {panel_label} | {metric_labels.get(metric, metric)} | "
                f"{paper_val:+.3f} | {ours_val:+.3f} | {status} ({d:+.3f}) |"
            )
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append(
        "**NYSE-only breakpoints (Panel A)**: Panel A uses breakpoints computed from "
        "NYSE-only firms (exchcd=1) per FF (1992, 1993). When a firm's exchange "
        "code is missing or the NYSE subset is too small, we fall back to in-sample "
        "breakpoints."
    )
    lines.append("")
    lines.append(
        "**Beta**: per the task spec, beta is skipped in this iteration. "
        "The paper estimates beta using monthly returns over the next 36 months "
        "(post-formation). Beta is in Table 3 Panel A-D but does not drive a "
        "claim; it is included for completeness in a future iteration."
    )
    lines.append("")
    return "\n".join(lines)


# --- Task 4: Tables 6, 7, 8, 9 (extended panel + FErr + regressions) ---

# Sample windows for tables (per task spec).
TABLE_6_7_YEAR_START = 1982   # need sales at year_t-6
TABLE_6_7_YEAR_END   = 1990   # paper's 15 years; we use 9
TABLE_8_YEAR_START   = 1979   # need PErr (requires FErr_{t-1})
TABLE_8_YEAR_END     = 1991
TABLE_9_YEAR_START   = 1978
TABLE_9_YEAR_END     = 1991


def _upload_gvkey_year_t(panel: pd.DataFrame) -> None:
    """Upload (gvkey, year_t) from the panel to ClickHouse as
    _panel_gvkeys for use in SQL joins."""
    c = _client()
    pairs = list(set(zip(
        panel["gvkey"].astype(str).str.strip().tolist(),
        panel["year_t"].astype(int).tolist(),
    )))
    c.execute("DROP TABLE IF EXISTS _panel_gvkeys")
    c.execute("""
        CREATE TABLE _panel_gvkeys (
            gvkey String,
            year_t UInt16
        ) ENGINE = MergeTree() ORDER BY (gvkey, year_t)
    """)
    c.execute("INSERT INTO _panel_gvkeys VALUES", pairs)


def load_comp_actual_roe_sg(panel: pd.DataFrame) -> pd.DataFrame:
    """Pull comp rows for ROE_{t+2} (IB and ceq at fyear = year_t+1)
    and SG (sale at year_t-6 and year_t-1).

    Uses the panel-gvkey-scoped query `comp_actual_roe_for_panel.sql`
    (the safety fix vs. iteration 4's Cartesian join) instead of
    `comp_actual_roe_and_sg.sql` which joined on c.gvkey = pk.gvkey
    without a year filter and produced ~25 rows per panel row.
    """
    _upload_gvkey_year_t(panel)
    df = q_file("comp_actual_roe_for_panel.sql")
    c = _client()
    c.execute("DROP TABLE IF EXISTS _panel_gvkeys")
    return df


def compute_extended_panel(panel_with_v: pd.DataFrame,
                           comp_extra: pd.DataFrame) -> pd.DataFrame:
    """Compute FErr_{t+2}, B/P, SG, OP, Ltg and their RK(.) ranks for
    each firm-year. Returns the extended panel."""
    df = panel_with_v.copy()
    df["gvkey"] = df["gvkey"].astype(str).str.strip()
    comp_extra = comp_extra.copy()
    comp_extra["gvkey"] = comp_extra["gvkey"].astype(str).str.strip()
    comp_extra["fyear"] = comp_extra["fyear"].astype(int)

    # For each needed offset, merge from comp_extra:
    df["_fo_t2"]   = df["year_t"] + 1
    df["_fo_t1"]   = df["year_t"]
    df["_fo_tm6"]  = df["year_t"] - 6
    df["_fo_tm1"]  = df["year_t"] - 1

    # IB + ceq at fyear = year_t + 1
    c_t2 = comp_extra.rename(columns={
        "ib": "ib_t2", "ceq": "ceq_t2", "fyear": "fyear_t2",
        "sale": "sale_t2_unused",
    })[["gvkey", "fyear_t2", "ib_t2", "ceq_t2"]]
    df = df.merge(c_t2, left_on=["gvkey", "_fo_t2"],
                  right_on=["gvkey", "fyear_t2"], how="left")
    df = df.drop(columns=["fyear_t2", "_fo_t2"], errors="ignore")

    # ceq at fyear = year_t (= B_{t+1} in paper's notation)
    c_t1 = comp_extra.rename(columns={
        "ceq": "ceq_t1", "fyear": "fyear_t1",
        "ib": "ib_t1_unused", "sale": "sale_t1_unused",
    })[["gvkey", "fyear_t1", "ceq_t1"]]
    df = df.merge(c_t1, left_on=["gvkey", "_fo_t1"],
                  right_on=["gvkey", "fyear_t1"], how="left")
    df = df.drop(columns=["fyear_t1", "_fo_t1"], errors="ignore")

    # sale at fyear = year_t - 6
    c_tm6 = comp_extra.rename(columns={
        "sale": "sale_tminus6", "fyear": "fyear_tm6",
        "ib": "ib_tm6_unused", "ceq": "ceq_tm6_unused",
    })[["gvkey", "fyear_tm6", "sale_tminus6"]]
    df = df.merge(c_tm6, left_on=["gvkey", "_fo_tm6"],
                  right_on=["gvkey", "fyear_tm6"], how="left")
    df = df.drop(columns=["fyear_tm6", "_fo_tm6"], errors="ignore")

    # sale at fyear = year_t - 1
    c_tm1 = comp_extra.rename(columns={
        "sale": "sale_tminus1", "fyear": "fyear_tm1",
        "ib": "ib_tm1_unused", "ceq": "ceq_tm1_unused",
    })[["gvkey", "fyear_tm1", "sale_tminus1"]]
    df = df.merge(c_tm1, left_on=["gvkey", "_fo_tm1"],
                  right_on=["gvkey", "fyear_tm1"], how="left")
    df = df.drop(columns=["fyear_tm1", "_fo_tm1"], errors="ignore")

    # --- ROE_{t+2} = IB_t2 / avg(ceq_t1, ceq_t2) ---
    valid_roe = (
        df["ib_t2"].notna()
        & df["ceq_t1"].notna()
        & df["ceq_t2"].notna()
        & (df["ceq_t1"] > 0)
        & (df["ceq_t2"] > 0)
    )
    df["roe_t2"] = np.where(
        valid_roe,
        df["ib_t2"] / ((df["ceq_t1"] + df["ceq_t2"]) / 2.0),
        np.nan,
    )

    # --- FErr_{t+2} = ROE_{t+2} - FROE_{t+2} ---
    # FROE_{t+2} is already in panel_with_v as `froe_t2`
    df["ferr_t2"] = df["roe_t2"] - df["froe_t2"]

    # --- B/P = book equity per share / price ---
    df["b_per_share"] = df["ceq"] / df["csho"]
    df["b_over_p"] = df["b_per_share"] / df["prc"]

    # --- SG = 5-year cumulative sales growth (t-6 -> t-1) ---
    valid_sg = (
        df["sale_tminus6"].notna()
        & df["sale_tminus1"].notna()
        & (df["sale_tminus6"] > 0)
        & (df["sale_tminus1"] > 0)
    )
    df["sg"] = np.where(
        valid_sg,
        (df["sale_tminus1"] / df["sale_tminus6"]) - 1.0,
        np.nan,
    )

    # --- OP = (V_f - V_h) / |V_h| using T=2 horizon ---
    df["op"] = np.where(
        df["v_h_t2"].notna()
        & (np.abs(df["v_h_t2"]) > 1e-6)
        & df["v_f_t2"].notna(),
        (df["v_f_t2"] - df["v_h_t2"]) / np.abs(df["v_h_t2"]),
        np.nan,
    )

    # --- Ltg proxy: FROE_{t+1} (Ltg data unavailable in I/B/E/S vintage) ---
    df["ltg_proxy"] = df["froe_t1"]

    # --- Within-year percentile ranks (RK) ---
    def _pct_rank(group: pd.Series) -> pd.Series:
        return group.rank(method="average", pct=True)

    df["rk_bp"] = df.groupby("year_t")["b_over_p"].transform(_pct_rank)
    df["rk_sg"] = df.groupby("year_t")["sg"].transform(_pct_rank)
    df["rk_op"] = df.groupby("year_t")["op"].transform(_pct_rank)
    df["rk_lt"] = df.groupby("year_t")["ltg_proxy"].transform(_pct_rank)

    return df


# --- OLS and Newey-West helpers ---

def ols_regression(y: np.ndarray, X: np.ndarray) -> tuple:
    """OLS via statsmodels. X is n x k (no intercept). Returns
    (beta_with_intercept, residuals, r2, f_stat)."""
    X_full = sm.add_constant(X, has_constant="add")
    model = sm.OLS(y, X_full)
    res = model.fit()
    beta = res.params
    r2 = float(res.rsquared)
    n = len(y)
    k = X.shape[1]
    df_reg = k
    df_res = n - k - 1
    if df_res > 0 and res.ssr > 0:
        f_stat = float((res.ess / df_reg) / (res.ssr / df_res))
    else:
        f_stat = np.nan
    return beta, res.resid, r2, f_stat


def newey_west_tstat(x: np.ndarray, max_lag: int = 2) -> float:
    """Newey-West HAC t-stat for H0: mean(x) = 0."""
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 3:
        return np.nan
    x_dm = x - x.mean()
    gamma_0 = (x_dm ** 2).sum() / n
    var_lr = gamma_0
    for lag in range(1, max_lag + 1):
        gamma_l = (x_dm[lag:] * x_dm[:-lag]).sum() / n
        w = 1.0 - lag / (max_lag + 1)
        var_lr += 2 * w * gamma_l
    if var_lr <= 0:
        return np.nan
    se = math.sqrt(var_lr / n)
    if se == 0:
        return np.nan
    return float(x.mean() / se)


# --- Table 6 ---

def compute_table_6(extended: pd.DataFrame) -> dict:
    """Annual cross-sectional regressions of FErr_{t+2} on each RK(X)."""
    iv_cols = ["rk_bp", "rk_sg", "rk_op", "rk_lt"]
    label_map = {
        "rk_bp": "RK(B/P)",
        "rk_sg": "RK(SG)",
        "rk_op": "RK(OP)",
        "rk_lt": "RK(Ltg)",
    }

    annual = {iv: [] for iv in iv_cols}
    for year_t, g in extended.groupby("year_t"):
        valid = g["ferr_t2"].notna()
        for iv in iv_cols:
            valid = valid & g[iv].notna()
        g = g.loc[valid]
        if len(g) < 10:
            continue
        y = g["ferr_t2"].values
        for iv in iv_cols:
            X = g[iv].values.reshape(-1, 1)
            beta, _, r2, _ = ols_regression(y, X)
            annual[iv].append({
                "year_t": int(year_t),
                "n": int(len(g)),
                "beta": float(beta[1]),
                "R2": float(r2),
            })

    summary_rows = []
    for iv in iv_cols:
        df = pd.DataFrame(annual[iv])
        if len(df) == 0:
            mean_beta = np.nan
            tstat = np.nan
            n_years = 0
        else:
            mean_beta = float(df["beta"].mean())
            tstat = newey_west_tstat(df["beta"].values, max_lag=2)
            n_years = len(df)
        summary_rows.append({
            "Variable": label_map[iv],
            "Mean coef": mean_beta,
            "NW t-stat (2 lags)": tstat,
            "n years": n_years,
        })
    summary = pd.DataFrame(summary_rows).set_index("Variable")

    return {
        "coefs": {iv: pd.DataFrame(annual[iv]).set_index("year_t") for iv in iv_cols},
        "summary": summary,
    }


def render_table_6_md(t6: dict) -> str:
    summary = t6["summary"]
    model_label = {
        "RK(B/P)": "M1: RK(B/P)",
        "RK(SG)": "M2: RK(SG)",
        "RK(OP)": "M3: RK(OP)",
        "RK(Ltg)": "M4: RK(Ltg)",
    }
    paper_targets = {
        "RK(B/P)": (-0.025, -2.69),
        "RK(SG)":  ( 0.043,  7.00),
        "RK(OP)":  ( 0.070,  5.01),
        "RK(Ltg)": ( 0.073,  6.57),
    }
    tolerance_pct = {
        "RK(B/P)": 30,
        "RK(SG)": 25,
        "RK(OP)": 30,
        "RK(Ltg)": 30,
    }

    lines = []
    lines.append("# Table 6 -- Annual Cross-Sectional Regressions of FErr_{t+2} on RK(X)")
    lines.append("")
    lines.append("**Replication of**: Frankel & Lee (1998) -- Table 6")
    lines.append("")
    lines.append("**Sample period**: 1982-1990 (per paper, 15 annual regressions; we use 9 years where all four RK variables AND FErr_{t+2} are computable)")
    lines.append("**Universe**: same as Table 2/3")
    lines.append("")
    lines.append("**Definitions**:")
    lines.append("- **FErr_{t+2} = ROE_{t+2} - FROE_{t+2}**: per paper footnote 21.")
    lines.append("- **ROE_{t+2} = IB_{t+2} / avg(ceq_{t+1}, ceq_{t+2})** where IB and ceq are from comp_202601.funda at fyear = year_t+1 and year_t.")
    lines.append("- **FROE_{t+2}**: from panel_with_v (Eq. A.3).")
    lines.append("- **B/P = (ceq / csho) / prc**: B at fiscal year ending in calendar year (year_t - 1).")
    lines.append("- **SG = sale_{t-1}/sale_{t-6} - 1**: 5-year cumulative sales growth.")
    lines.append("- **OP = (V_f^2 - V_h^2) / |V_h^2|**: T=2 EBO horizon.")
    lines.append("- **Ltg = FROE_{t+1} (proxy)**: Ltg unavailable in this I/B/E/S vintage (assumption 19).")
    lines.append("- **RK(X)**: within-year percentile rank (rank / (n-1) in [0, 1]).")
    lines.append("")
    lines.append("**Annual OLS** per (year_t, IV): FErr_{t+2} = α + β × RK(X_{t}) + ε.")
    lines.append("**Time-series aggregation**: Mean coef = time-series mean of annual β's; NW t-stat with 2 lags (per assumption 24).")
    lines.append("")

    lines.append("## Time-series summary")
    lines.append("")
    lines.append("| Model | Mean coef | NW t-stat (2 lags) | n years | Paper mean coef | Paper t-stat | Status |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- |")
    for label, row in summary.iterrows():
        mean_c = row["Mean coef"]
        t_stat = row["NW t-stat (2 lags)"]
        n_yrs = int(row["n years"])
        paper_mean, paper_t = paper_targets[label]
        tol = tolerance_pct[label] / 100.0
        d_mean = mean_c - paper_mean
        if pd.isna(mean_c):
            status = "MISSING"
        elif abs(d_mean) <= tol * abs(paper_mean):
            status = "Tier 1"
        elif abs(d_mean) <= 2 * tol * abs(paper_mean):
            status = "Tier 2"
        else:
            status = "FAIL"
        lines.append(
            f"| {model_label[label]} | {mean_c:+.4f} | {t_stat:+.2f} | {n_yrs} | "
            f"{paper_mean:+.4f} | {paper_t:+.2f} | {status} (Δcoef={d_mean:+.4f}) |"
        )

    lines.append("")
    lines.append("## Per-year coefficients (β on RK(X))")
    lines.append("")
    iv_to_label = {
        "rk_bp": "M1: RK(B/P)",
        "rk_sg": "M2: RK(SG)",
        "rk_op": "M3: RK(OP)",
        "rk_lt": "M4: RK(Ltg)",
    }
    for iv in ["rk_bp", "rk_sg", "rk_op", "rk_lt"]:
        coef_df = t6["coefs"][iv]
        if len(coef_df) == 0:
            continue
        lines.append(f"### {iv_to_label[iv]}")
        lines.append("")
        lines.append("| Year | n | β | R² |")
        lines.append("| --- | ---: | ---: | ---: |")
        for year_t, row in coef_df.iterrows():
            lines.append(f"| {int(year_t)} | {int(row['n'])} | {row['beta']:+.4f} | {row['R2']:.4f} |")
        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("**Sample window**: paper reports 15 annual regressions; we obtain 9 years (1982-1990) where all inputs are computable from this data vintage. The paper's sample is 1976-1990, but actual ROE_{t+2} requires comp data at fyear = year_t+1 (we cover year_t up to 1993); SG requires sale at year_t-6 (year_t ≥ 1982).")
    lines.append("")
    lines.append("**Ltg proxy**: per task spec we use FROE_{t+1} as a proxy for Ltg (assumption 19).")
    lines.append("")
    lines.append("**OP horizon**: paper §5.4 uses V_h^2 / V_f^2 (T=2 horizon); we follow this convention.")
    lines.append("")
    return "\n".join(lines)


# --- Table 7 ---

def compute_table_7(extended: pd.DataFrame) -> dict:
    """Multiple regression of FErr_{t+2} on RK(SG), RK(B/P), RK(OP), RK(Ltg)."""
    iv_cols = ["rk_sg", "rk_bp", "rk_op", "rk_lt"]

    annual_rows = []
    for year_t, g in extended.groupby("year_t"):
        valid = g["ferr_t2"].notna()
        for iv in iv_cols:
            valid = valid & g[iv].notna()
        g = g.loc[valid]
        if len(g) < 10:
            continue
        y = g["ferr_t2"].values
        X = g[iv_cols].values
        beta, _, r2, f_stat = ols_regression(y, X)
        annual_rows.append({
            "year_t": int(year_t),
            "n": int(len(g)),
            "beta_sg": float(beta[1]),
            "beta_bp": float(beta[2]),
            "beta_op": float(beta[3]),
            "beta_lt": float(beta[4]),
            "R2": float(r2),
            "F_stat": float(f_stat) if pd.notna(f_stat) else np.nan,
        })

    df = pd.DataFrame(annual_rows)
    if len(df) > 0:
        summary = pd.DataFrame({
            "Mean coef": [
                float(df["beta_sg"].mean()),
                float(df["beta_bp"].mean()),
                float(df["beta_op"].mean()),
                float(df["beta_lt"].mean()),
            ],
            "NW t-stat (2 lags)": [
                newey_west_tstat(df["beta_sg"].values, max_lag=2),
                newey_west_tstat(df["beta_bp"].values, max_lag=2),
                newey_west_tstat(df["beta_op"].values, max_lag=2),
                newey_west_tstat(df["beta_lt"].values, max_lag=2),
            ],
        }, index=["RK(SG)", "RK(B/P)", "RK(OP)", "RK(Ltg)"])
    else:
        summary = pd.DataFrame()

    return {"annual": df, "summary": summary}


def render_table_7_md(t7: dict) -> str:
    df = t7["annual"]
    summary = t7["summary"]
    paper_targets = {
        "RK(SG)":   (0.035, 5.94),
        "RK(B/P)":  (0.010, 1.16),
        "RK(OP)":   (0.051, 3.55),
        "RK(Ltg)":  (0.050, 4.26),
    }
    tolerance_pct = {
        "RK(SG)": 30,
        "RK(B/P)": 50,
        "RK(OP)": 30,
        "RK(Ltg)": 30,
    }
    paper_r2 = 0.074

    lines = []
    lines.append("# Table 7 -- Multiple Regression of FErr_{t+2} on RK(SG), RK(B/P), RK(OP), RK(Ltg)")
    lines.append("")
    lines.append("**Replication of**: Frankel & Lee (1998) -- Table 7")
    lines.append("")
    lines.append("**Sample period**: 1982-1990 (same as Table 6)")
    lines.append("")
    lines.append("**Annual OLS** per year_t: FErr_{t+2} = α + β1 RK(SG_t) + β2 RK(B/P_t) + β3 RK(OP_t) + β4 RK(Ltg_t) + ε.")
    lines.append("")
    lines.append("## Per-year estimates")
    lines.append("")
    lines.append("| Year | n | β(SG) | β(B/P) | β(OP) | β(Ltg) | R² | F-stat |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for _, row in df.iterrows():
        f = row["F_stat"]
        f_str = f"{f:.2f}" if pd.notna(f) else "NaN"
        lines.append(
            f"| {int(row['year_t'])} | {int(row['n'])} | "
            f"{row['beta_sg']:+.4f} | {row['beta_bp']:+.4f} | "
            f"{row['beta_op']:+.4f} | {row['beta_lt']:+.4f} | "
            f"{row['R2']:.4f} | {f_str} |"
        )

    lines.append("")
    lines.append("## Time-series summary")
    lines.append("")
    lines.append("| Variable | Mean coef | NW t-stat (2 lags) | Paper mean coef | Paper t-stat | Status |")
    lines.append("| --- | ---: | ---: | ---: | ---: | --- |")
    for label in ["RK(SG)", "RK(B/P)", "RK(OP)", "RK(Ltg)"]:
        if label not in summary.index:
            continue
        mean_c = summary.loc[label, "Mean coef"]
        t_stat = summary.loc[label, "NW t-stat (2 lags)"]
        paper_mean, paper_t = paper_targets[label]
        tol = tolerance_pct[label] / 100.0
        d_mean = mean_c - paper_mean
        if pd.isna(mean_c):
            status = "MISSING"
        elif abs(d_mean) <= tol * abs(paper_mean):
            status = "Tier 1"
        elif abs(d_mean) <= 2 * tol * abs(paper_mean):
            status = "Tier 2"
        else:
            status = "FAIL"
        lines.append(
            f"| {label} | {mean_c:+.4f} | {t_stat:+.2f} | "
            f"{paper_mean:+.4f} | {paper_t:+.2f} | {status} (Δcoef={d_mean:+.4f}) |"
        )

    if len(df) > 0:
        mean_r2 = float(df["R2"].mean())
        d_r2 = mean_r2 - paper_r2
        tol = 0.30
        if abs(d_r2) <= tol * paper_r2:
            s = "Tier 1"
        elif abs(d_r2) <= 2 * tol * paper_r2:
            s = "Tier 2"
        else:
            s = "FAIL"
        lines.append(f"| Avg R² | {mean_r2:.4f} | -- | {paper_r2:.4f} | -- | {s} (Δ={d_r2:+.4f}) |")

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("**Same window as Table 6.** The paper uses 15 years (1976-1990); we use 9 years (1982-1990). The paper's Table 7 reports joint R² averaging 0.074; our replication target range is 0.05-0.10.")
    lines.append("")
    return "\n".join(lines)


# --- Table 8: PErr + decile-rank return regressions ---

def compute_perr(extended: pd.DataFrame) -> pd.DataFrame:
    """Compute PErr_t for each (permno, year_t).

    Per task spec:
      - For portfolio year t (t >= TABLE_8_YEAR_START):
        DV = FErr_{t-1}
        IV = RK(X_{t-4})
        Run OLS cross-section at year t-1 (using IVs at year t-4)
      - PErr_t = α̂ + β̂ × RK(X_{t-4})
      - Then assign deciles 1-10 (low to high) and scale to 0-1.

    Returns extended panel augmented with `perr` column.
    """
    df = extended.copy()
    # Build a lagged-RK lookup keyed by (permno, year_t).
    # For each (permno, year_t), we need:
    #   - FErr_{t-1}: from a row with (permno, year_t - 1)
    #   - RK(X_{t-4}): from rows with (permno, year_t - 4)
    # First, build a (permno, year_t) -> {ferr_t2, rk_*} map.
    src_cols = ["permno", "year_t", "ferr_t2", "rk_sg", "rk_bp", "rk_op", "rk_lt"]
    src = df[src_cols].copy()

    # FErr_{t-1} = FErr_t2 of the firm-year with year_t = (this year_t) - 1
    # RK(X_{t-4}) = RK(X) of the firm-year with year_t = (this year_t) - 4
    ferr_lag1 = src[["permno", "year_t", "ferr_t2"]].rename(
        columns={"ferr_t2": "ferr_lag1", "year_t": "ferr_year_t"}
    )
    ferr_lag1["year_t"] = ferr_lag1["ferr_year_t"] + 1
    ferr_lag1 = ferr_lag1.drop(columns=["ferr_year_t"])

    rk_lag4 = src[["permno", "year_t", "rk_sg", "rk_bp", "rk_op", "rk_lt"]].rename(
        columns={
            "year_t": "rk_year_t",
            "rk_sg": "rk_sg_l4",
            "rk_bp": "rk_bp_l4",
            "rk_op": "rk_op_l4",
            "rk_lt": "rk_lt_l4",
        }
    )
    rk_lag4["year_t"] = rk_lag4["rk_year_t"] + 4
    rk_lag4 = rk_lag4.drop(columns=["rk_year_t"])

    df = df.merge(ferr_lag1, on=["permno", "year_t"], how="left")
    df = df.merge(rk_lag4, on=["permno", "year_t"], how="left")

    # Compute PErr per year_t via annual OLS.
    iv_cols = ["rk_sg_l4", "rk_bp_l4", "rk_op_l4", "rk_lt_l4"]
    perr_rows = []
    for year_t, g in df.groupby("year_t"):
        valid = g["ferr_lag1"].notna()
        for iv in iv_cols:
            valid = valid & g[iv].notna()
        g_v = g.loc[valid]
        if len(g_v) < 10:
            continue
        y = g_v["ferr_lag1"].values
        X = g_v[iv_cols].values
        beta, _, _, _ = ols_regression(y, X)
        # Compute PErr for ALL firms in df[year_t == year_t] using their
        # rk_lag4 values.
        g_full = df[df["year_t"] == year_t]
        X_full = g_full[iv_cols].values
        # PErr = β0 + β1*X1 + ... + β4*X4
        X_full_with_const = sm.add_constant(X_full, has_constant="add")
        valid_full = ~np.isnan(X_full_with_const).any(axis=1)
        perr = np.full(len(g_full), np.nan)
        perr[valid_full] = X_full_with_const[valid_full] @ beta
        for i, idx in enumerate(g_full.index):
            perr_rows.append({"idx": idx, "perr_raw": perr[i]})

    perr_df = pd.DataFrame(perr_rows).set_index("idx")
    df = df.join(perr_df, how="left")

    # Decile-rank scaling: assign deciles 1-10 from low to high within
    # each year_t, then scale to [0, 1] = (decile - 1) / 9.
    # We use np.searchsorted on per-year breakpoints.
    df["perr_decile"] = np.nan
    df["perr"] = np.nan
    for year_t, g in df.groupby("year_t"):
        valid = g["perr_raw"].notna()
        if valid.sum() < 10:
            continue
        vals = g.loc[valid, "perr_raw"].values
        # 10-bin breakpoints (decile edges)
        edges = np.quantile(vals, np.linspace(0, 1, 11))
        edges[0] -= 1e-9
        edges[-1] += 1e-9
        deciles = np.digitize(vals, edges[1:-1], right=False) + 1
        # Clamp to 1..10
        deciles = np.clip(deciles, 1, 10)
        df.loc[g.index[valid], "perr_decile"] = deciles
        df.loc[g.index[valid], "perr"] = (deciles - 1) / 9.0

    return df


def compute_table_8(extended_with_perr: pd.DataFrame) -> dict:
    """Table 8: decile-rank regression of 1-yr (Panel A) and 3-yr
    (Panel B) buy-and-hold returns on BP, ME, V_f/P, PErr.

    6 models each panel. Coefficients are mean coef and NW t-stat.
    """
    # Merge BHAR returns
    bhar_path = LAYOUT.data_path("bhar_returns.parquet")
    bhar = pd.read_parquet(bhar_path)
    df = extended_with_perr.merge(
        bhar[["permno", "year_t", "ret12", "ret36"]], on=["permno", "year_t"], how="left"
    )

    # Compute decile ranks for BP, ME, V_f/P within each year_t.
    for col in ["b_over_p", "me_june_t", "v_f_p_t3"]:
        df[f"{col}_decile"] = np.nan

    for year_t, g in df.groupby("year_t"):
        for col in ["b_over_p", "me_june_t", "v_f_p_t3"]:
            valid = g[col].notna()
            if valid.sum() < 10:
                continue
            vals = g.loc[valid, col].values
            edges = np.quantile(vals, np.linspace(0, 1, 11))
            edges[0] -= 1e-9
            edges[-1] += 1e-9
            deciles = np.digitize(vals, edges[1:-1], right=False) + 1
            deciles = np.clip(deciles, 1, 10)
            df.loc[g.index[valid], f"{col}_decile"] = (deciles - 1) / 9.0

    # Run 6 models per panel
    models_panel_a = [
        ["b_over_p_decile"],
        ["me_june_t_decile"],
        ["v_f_p_t3_decile"],
        ["perr"],
        ["b_over_p_decile", "me_june_t_decile"],
        ["b_over_p_decile", "me_june_t_decile", "v_f_p_t3_decile", "perr"],
    ]
    models_panel_b = models_panel_a

    results_a = _run_panel_models(df, "ret12", models_panel_a, "Panel A (1-yr BHAR)")
    results_b = _run_panel_models(df, "ret36", models_panel_b, "Panel B (3-yr BHAR)")

    return {"panel_a": results_a, "panel_b": results_b}


def _run_panel_models(df: pd.DataFrame, dv_col: str, models: list, label: str) -> dict:
    """Run a list of regression models per year and aggregate."""
    n_models = len(models)
    coef_names = [f"model_{i+1}" for i in range(n_models)]
    annual_results = []

    for year_t, g in df.groupby("year_t"):
        valid = g[dv_col].notna()
        for m in models:
            for iv in m:
                valid = valid & g[iv].notna()
        g_v = g.loc[valid]
        if len(g_v) < 10:
            continue
        y = g_v[dv_col].values
        for i, m in enumerate(models):
            X = g_v[m].values
            if X.shape[1] == 0:
                continue
            beta, _, r2, _ = ols_regression(y, X)
            row = {"year_t": int(year_t), "n": int(len(g_v))}
            row[f"b0_m{i+1}"] = float(beta[0])
            for j, iv in enumerate(m):
                row[f"b_{iv}_m{i+1}"] = float(beta[j + 1])
            row[f"r2_m{i+1}"] = float(r2)
            annual_results.append(row)

    if not annual_results:
        return {"annual": pd.DataFrame(), "summary": {}}

    annual = pd.DataFrame(annual_results)

    # Aggregate by mean coef and NW t-stat for each model coefficient
    summary = {}
    for i, m in enumerate(models):
        summary[f"model_{i+1}"] = {"IVs": m, "coefs": {}, "r2": np.nan}
        intercept_key = f"b0_m{i+1}"
        if intercept_key in annual.columns:
            vals = annual[intercept_key].dropna().values
            summary[f"model_{i+1}"]["coefs"]["intercept"] = {
                "mean": float(np.mean(vals)) if len(vals) > 0 else np.nan,
                "t": newey_west_tstat(vals, max_lag=2),
            }
        for iv in m:
            key = f"b_{iv}_m{i+1}"
            if key in annual.columns:
                vals = annual[key].dropna().values
                summary[f"model_{i+1}"]["coefs"][iv] = {
                    "mean": float(np.mean(vals)) if len(vals) > 0 else np.nan,
                    "t": newey_west_tstat(vals, max_lag=2),
                }
        r2_key = f"r2_m{i+1}"
        if r2_key in annual.columns:
            summary[f"model_{i+1}"]["r2"] = float(annual[r2_key].mean())

    return {"annual": annual, "summary": summary, "label": label, "dv_col": dv_col, "models": models}


def render_table_8_md(t8: dict) -> str:
    """Render Table 8 as Markdown with both panels."""
    lines = []
    lines.append("# Table 8 -- Decile-Rank Regression of Returns on BP, ME, V_f/P, PErr")
    lines.append("")
    lines.append("**Replication of**: Frankel & Lee (1998) -- Table 8")
    lines.append("")
    lines.append("**Sample period**: 1979-1991 (PErr-eligible window per paper §5.6: 1979-1992)")
    lines.append("")
    lines.append("**Definitions**:")
    lines.append("- **BP**, **ME**, **V_f/P** are decile-ranked 0-1 within each year_t.")
    lines.append("- **PErr** = α̂ + β̂1 RK(SG_{t-4}) + β̂2 RK(BP_{t-4}) + β̂3 RK(OP_{t-4}) + β̂4 RK(Ltg_{t-4}), where the β̂'s come from annual OLS of FErr_{t-1} on RK(X_{t-4}); then PErr is decile-ranked 0-1.")
    lines.append("- **Ret12** / **Ret36**: 1-year / 3-year buy-and-hold returns starting July of year_t.")
    lines.append("")

    paper_targets_panel_a = {
        "model_1": {"intercept": (0.151, None), "b_over_p_decile": (0.051, None)},
        "model_3": {"v_f_p_t3_decile": (0.042, None)},
        "model_4": {"perr": (-0.040, None)},
        "model_6": {"intercept": (0.176, None), "perr": (-0.035, None), "r2": (0.19, None)},
    }
    paper_targets_panel_b = {
        "model_1": {"intercept": (0.468, None), "b_over_p_decile": (0.168, None)},
        "model_3": {"v_f_p_t3_decile": (0.370, None)},
        "model_4": {"perr": (-0.277, None)},
        "model_5": {"v_f_p_t3_decile": (0.352, None)},
        "model_6": {"intercept": (0.539, None), "v_f_p_t3_decile": (0.343, None), "perr": (-0.241, None), "r2": (2.47, None)},
    }

    for panel_key, paper_targets in [
        ("panel_a", paper_targets_panel_a),
        ("panel_b", paper_targets_panel_b),
    ]:
        results = t8[panel_key]
        lines.append(f"## {results['label']}")
        lines.append("")
        lines.append(f"DV: `{results['dv_col']}`")
        lines.append("")
        lines.append("| Model | IVs | Coef name | Mean coef | NW t-stat (2 lags) | Paper value | Status |")
        lines.append("| --- | --- | --- | ---: | ---: | ---: | --- |")
        for i, m in enumerate(results["models"]):
            model_key = f"model_{i+1}"
            sm = results["summary"].get(model_key, {})
            coefs = sm.get("coefs", {})
            iv_str = ", ".join(m) if m else "(none)"
            # Intercept
            if "intercept" in coefs:
                v = coefs["intercept"]
                target = paper_targets.get(model_key, {}).get("intercept", (None, None))
                paper_v = target[0]
                if paper_v is not None:
                    tol = 0.15
                    d = v["mean"] - paper_v
                    if abs(d) <= tol * abs(paper_v):
                        s = "Tier 1"
                    elif abs(d) <= 2 * tol * abs(paper_v):
                        s = "Tier 2"
                    else:
                        s = "FAIL"
                    status = f"{s} (Δ={d:+.4f})"
                    paper_str = f"{paper_v:+.4f}"
                else:
                    status = "no target"
                    paper_str = "--"
                lines.append(
                    f"| M{i+1} | {iv_str} | intercept | "
                    f"{v['mean']:+.4f} | {v['t']:+.2f} | {paper_str} | {status} |"
                )
            # IVs
            for iv in m:
                if iv in coefs:
                    v = coefs[iv]
                    target = paper_targets.get(model_key, {}).get(iv, (None, None))
                    paper_v = target[0]
                    if paper_v is not None:
                        tol = 0.30 if iv != "b_over_p_decile" else 0.30
                        d = v["mean"] - paper_v
                        if abs(d) <= tol * abs(paper_v):
                            s = "Tier 1"
                        elif abs(d) <= 2 * tol * abs(paper_v):
                            s = "Tier 2"
                        else:
                            s = "FAIL"
                        status = f"{s} (Δ={d:+.4f})"
                        paper_str = f"{paper_v:+.4f}"
                    else:
                        status = "no target"
                        paper_str = "--"
                    lines.append(
                        f"| M{i+1} | {iv_str} | {iv} | "
                        f"{v['mean']:+.4f} | {v['t']:+.2f} | {paper_str} | {status} |"
                    )
            # R²
            r2 = sm.get("r2", np.nan)
            target_r2 = paper_targets.get(model_key, {}).get("r2", (None, None))
            paper_r2 = target_r2[0]
            if paper_r2 is not None:
                tol = 0.50
                d = r2 - paper_r2
                if abs(d) <= tol * abs(paper_r2):
                    s = "Tier 1"
                elif abs(d) <= 2 * tol * abs(paper_r2):
                    s = "Tier 2"
                else:
                    s = "FAIL"
                status = f"{s} (Δ={d:+.4f})"
                paper_str = f"{paper_r2:+.4f}"
            else:
                status = "no target"
                paper_str = "--"
            lines.append(
                f"| M{i+1} | {iv_str} | R² | "
                f"{r2:+.4f} | -- | {paper_str} | {status} |"
            )

        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("**Decile scaling**: 10-bin breakpoints within each year_t, scaled to 0-1 = (decile-1)/9, so β = long-short spread.")
    lines.append("")
    lines.append("**PErr construction**: per task spec, regress FErr_{t-1} on RK(X_{t-4}) annually (OLS). PErr_t = α̂ + β̂ × RK(X_{t-4}). Decile-rank the resulting PErr across firms.")
    lines.append("")
    return "\n".join(lines)


# --- Table 9: year-by-year BHAR for strategies ---

def compute_table_9(extended: pd.DataFrame) -> dict:
    """Year-by-year BHAR for 4 strategies:
       A: B/P high - low (Q5 - Q1)
       B: PErr low - high (Q1 - Q5)
       C: V_f/P high - low (Q5 - Q1)
       D: Combined: long (top V_f/P AND bottom PErr); short (bottom V_f/P AND top PErr)
    """
    bhar_path = LAYOUT.data_path("bhar_returns.parquet")
    bhar = pd.read_parquet(bhar_path)
    df = extended.merge(
        bhar[["permno", "year_t", "ret12", "ret36"]], on=["permno", "year_t"], how="left"
    )

    # Assign quintiles per year for b_over_p, v_f_p_t3, perr
    for col in ["b_over_p", "v_f_p_t3", "perr"]:
        df[f"{col}_q"] = np.nan

    for year_t, g in df.groupby("year_t"):
        for col in ["b_over_p", "v_f_p_t3", "perr"]:
            valid = g[col].notna()
            if valid.sum() < 10:
                continue
            vals = g.loc[valid, col].values
            edges = np.quantile(vals, np.linspace(0, 1, 6))
            edges[0] -= 1e-9
            edges[-1] += 1e-9
            quintiles = np.digitize(vals, edges[1:-1], right=False) + 1
            quintiles = np.clip(quintiles, 1, 5)
            df.loc[g.index[valid], f"{col}_q"] = quintiles

    # For each year, compute the strategy BHAR as the equally-weighted
    # mean return within the relevant quintile(s).
    annual_rows = []
    for year_t, g in df.groupby("year_t"):
        if year_t < TABLE_9_YEAR_START or year_t > TABLE_9_YEAR_END:
            continue
        row = {"year_t": int(year_t)}
        # Panel A: B/P Q5 - Q1
        q5 = g[g["b_over_p_q"] == 5]
        q1 = g[g["b_over_p_q"] == 1]
        if len(q5) > 0 and len(q1) > 0:
            row["PanelA_ret12"] = float(q5["ret12"].mean() - q1["ret12"].mean())
            row["PanelA_ret36"] = float(q5["ret36"].mean() - q1["ret36"].mean())
        # Panel B: PErr Q1 - Q5 (per assumption 23: long bottom, short top)
        q1p = g[g["perr_q"] == 1]
        q5p = g[g["perr_q"] == 5]
        if len(q1p) > 0 and len(q5p) > 0:
            row["PanelB_ret12"] = float(q1p["ret12"].mean() - q5p["ret12"].mean())
            row["PanelB_ret36"] = float(q1p["ret36"].mean() - q5p["ret36"].mean())
        # Panel C: V_f/P Q5 - Q1
        q5v = g[g["v_f_p_t3_q"] == 5]
        q1v = g[g["v_f_p_t3_q"] == 1]
        if len(q5v) > 0 and len(q1v) > 0:
            row["PanelC_ret12"] = float(q5v["ret12"].mean() - q1v["ret12"].mean())
            row["PanelC_ret36"] = float(q5v["ret36"].mean() - q1v["ret36"].mean())
        # Panel D: Combined (V_f/P top & PErr bottom) - (V_f/P bottom & PErr top)
        long_d = g[(g["v_f_p_t3_q"] == 5) & (g["perr_q"] == 1)]
        short_d = g[(g["v_f_p_t3_q"] == 1) & (g["perr_q"] == 5)]
        if len(long_d) > 0 and len(short_d) > 0:
            row["PanelD_ret12"] = float(long_d["ret12"].mean() - short_d["ret12"].mean())
            row["PanelD_ret36"] = float(long_d["ret36"].mean() - short_d["ret36"].mean())
        annual_rows.append(row)

    annual = pd.DataFrame(annual_rows).set_index("year_t") if annual_rows else pd.DataFrame()

    # Time-series summary
    summary = {}
    for panel in ["PanelA", "PanelB", "PanelC", "PanelD"]:
        for ret in ["ret12", "ret36"]:
            col = f"{panel}_{ret}"
            if col in annual.columns:
                vals = annual[col].dropna().values
                summary[col] = {
                    "mean": float(np.mean(vals)) if len(vals) > 0 else np.nan,
                    "t": newey_west_tstat(vals, max_lag=2),
                    "n": int(len(vals)),
                }

    return {"annual": annual, "summary": summary}


def render_table_9_md(t9: dict) -> str:
    """Render Table 9 as Markdown."""
    annual = t9["annual"]
    summary = t9["summary"]
    paper_targets = {
        "PanelA_ret12_mean": (None, None),  # no specific target
        "PanelA_ret36_mean": (0.228, 3.32),
        "PanelB_ret36_mean": (0.263, 3.55),
        "PanelC_ret36_mean": (0.349, 4.06),
        "PanelD_ret36_mean": (0.457, 5.40),
    }

    lines = []
    lines.append("# Table 9 -- Year-by-Year BHAR for 4 Strategies")
    lines.append("")
    lines.append("**Replication of**: Frankel & Lee (1998) -- Table 9")
    lines.append("")
    lines.append("**Sample period**: 1978-1991")
    lines.append("")
    lines.append("**Strategies**:")
    lines.append("- **Panel A**: B/P high - low (Q5 mean - Q1 mean)")
    lines.append("- **Panel B**: PErr low - high (Q1 mean - Q5 mean; per assumption 23, long low-PErr firms, short high-PErr firms)")
    lines.append("- **Panel C**: V_f/P high - low (Q5 mean - Q1 mean)")
    lines.append("- **Panel D**: Combined = (top V_f/P AND bottom PErr) - (bottom V_f/P AND top PErr)")
    lines.append("")

    lines.append("## Per-year BHAR")
    lines.append("")
    if len(annual) > 0:
        cols = sorted([c for c in annual.columns])
        header = "| Year | " + " | ".join(cols) + " |"
        sep = "| --- |" + "|".join(["---:"] * len(cols)) + "|"
        lines.append(header)
        lines.append(sep)
        for year_t, row in annual.iterrows():
            vals = []
            for c in cols:
                v = row[c]
                if pd.isna(v):
                    vals.append("")
                else:
                    vals.append(f"{v:+.3f}")
            lines.append(f"| {int(year_t)} | " + " | ".join(vals) + " |")

    lines.append("")
    lines.append("## Time-series summary")
    lines.append("")
    lines.append("| Panel | Mean BHAR | NW t-stat (2 lags) | n years | Paper mean | Paper t-stat | Status |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- |")
    paper_targets_full = {
        "PanelA_ret12": (None, None, "no target"),
        "PanelA_ret36": (0.228, 3.32, 0.30),
        "PanelB_ret12": (None, None, "no target"),
        "PanelB_ret36": (0.263, 3.55, 0.30),
        "PanelC_ret12": (None, None, "no target"),
        "PanelC_ret36": (0.349, 4.06, 0.30),
        "PanelD_ret12": (None, None, "no target"),
        "PanelD_ret36": (0.457, 5.40, 0.30),
    }
    for col in ["PanelA_ret12", "PanelA_ret36", "PanelB_ret12", "PanelB_ret36",
                "PanelC_ret12", "PanelC_ret36", "PanelD_ret12", "PanelD_ret36"]:
        if col not in summary:
            continue
        s = summary[col]
        paper_v, paper_t, tol_pct = paper_targets_full[col]
        if paper_v is None:
            lines.append(
                f"| {col} | {s['mean']:+.3f} | {s['t']:+.2f} | {s['n']} | "
                f"-- | -- | no target |"
            )
        else:
            tol = tol_pct
            d = s["mean"] - paper_v
            if abs(d) <= tol * abs(paper_v):
                status = "Tier 1"
            elif abs(d) <= 2 * tol * abs(paper_v):
                status = "Tier 2"
            else:
                status = "FAIL"
            lines.append(
                f"| {col} | {s['mean']:+.3f} | {s['t']:+.2f} | {s['n']} | "
                f"{paper_v:+.3f} | {paper_t:+.2f} | {status} (Δ={d:+.3f}) |"
            )

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("**Strategy construction**: quintiles per year; equally-weighted mean BHAR within each quintile. PErr uses the lag-4 RK(X) construction from Tables 6/8.")
    lines.append("")
    return "\n".join(lines)


# --- Main ---

def main():
    print("[1/8] Loading panel_with_v from data/panel_with_v.parquet")
    panel_with_v = pd.read_parquet(LAYOUT.data_path("panel_with_v.parquet"))
    # Deduplicate (permno, year_t)
    if "permno" in panel_with_v.columns and "year_t" in panel_with_v.columns:
        panel_with_v["permno"] = panel_with_v["permno"].astype("int64")
        panel_with_v["year_t"] = panel_with_v["year_t"].astype("int32")
        panel_with_v = panel_with_v.sort_values(
            ["permno", "year_t", "gvkey"]
        ).drop_duplicates(subset=["permno", "year_t"], keep="first").reset_index(drop=True)
    print(f"      Panel+V: {len(panel_with_v):,} rows x {panel_with_v.shape[1]} cols")

    print("[2/8] Loading BHAR returns from data/bhar_returns.parquet")
    bhar = pd.read_parquet(LAYOUT.data_path("bhar_returns.parquet"))
    print(f"      BHAR rows: {len(bhar):,}")

    print("[3/8] Pulling comp rows for actual ROE_{t+2} and SG from ClickHouse")
    comp_extra = load_comp_actual_roe_sg(panel_with_v)
    print(f"      Comp extra rows: {len(comp_extra):,}")

    print("[4/8] Computing extended panel (FErr, B/P, SG, OP, Ltg, RKs)")
    extended = compute_extended_panel(panel_with_v, comp_extra)
    print(f"      Extended: {len(extended):,} rows x {extended.shape[1]} cols")
    print(f"      FErr non-null: {extended['ferr_t2'].notna().sum():,}")
    print(f"      RK(B/P) non-null: {extended['rk_bp'].notna().sum():,}")
    print(f"      RK(SG) non-null: {extended['rk_sg'].notna().sum():,}")
    print(f"      RK(OP) non-null: {extended['rk_op'].notna().sum():,}")
    print(f"      RK(Ltg proxy) non-null: {extended['rk_lt'].notna().sum():,}")

    # Save the extended panel as a checkpoint
    extended.to_parquet(LAYOUT.data_path("extended_panel.parquet"), index=False)

    print("[5a/8] Rendering Table 4 (bi-dimensional quintile Ret36)")
    from table_4 import compute_table_4, render_table_4_md, extract_table_4_metrics
    t4 = compute_table_4(panel_with_v, bhar)
    out_4 = LAYOUT.result_path("table_4.md")
    out_4.write_text(render_table_4_md(t4))
    t4_metrics = extract_table_4_metrics(t4)
    print(f"      Wrote {out_4} ({len(t4_metrics)} committed-cell metrics)")

    print("[5b/8] Rendering Table 6 (annual single-IV regressions)")
    t6 = compute_table_6(extended)
    out_6 = LAYOUT.result_path("table_6.md")
    out_6.write_text(render_table_6_md(t6))
    t6_metrics = _extract_table_6_metrics(t6)
    print(f"      Wrote {out_6} ({len(t6_metrics)} committed-cell metrics)")

    print("[5c/8] Rendering Table 7 (annual multiple regressions)")
    t7 = compute_table_7(extended)
    out_7 = LAYOUT.result_path("table_7.md")
    out_7.write_text(render_table_7_md(t7))
    t7_metrics = _extract_table_7_metrics(t7)
    print(f"      Wrote {out_7} ({len(t7_metrics)} committed-cell metrics)")

    print("[6/8] Computing PErr and rendering Table 8 (decile-rank return regressions)")
    extended_with_perr = compute_perr(extended)
    # Save extended with PErr
    extended_with_perr.to_parquet(LAYOUT.data_path("extended_panel_with_perr.parquet"), index=False)
    t8 = compute_table_8(extended_with_perr)
    out_8 = LAYOUT.result_path("table_8.md")
    out_8.write_text(render_table_8_md(t8))
    print(f"      Wrote {out_8}")

    print("[7/8] Rendering Table 9 (year-by-year strategy BHAR)")
    t9 = compute_table_9(extended_with_perr)
    out_9 = LAYOUT.result_path("table_9.md")
    out_9.write_text(render_table_9_md(t9))
    print(f"      Wrote {out_9}")

    # [8/8] Emit data/metrics.json with every committed cell's value.
    # Tables 1-3 are parsed from the per-cell comparison blocks of
    # their MD files (hand-curated). Tables 4, 6, 7 are computed
    # above; Table 8, 9 metrics are not emitted this iteration
    # (out of scope for this task).
    print("[8/8] Emitting data/metrics.json")
    from metrics_writer import write_metrics
    additional = {}
    additional.update(t4_metrics)
    additional.update(t6_metrics)
    additional.update(t7_metrics)
    payload = write_metrics(additional_metrics=additional)
    print(f"      Wrote {LAYOUT.data_path('metrics.json')} with "
          f"{len(payload['metrics'])} metric values "
          f"(+{len(additional)} from Tables 4/6/7)")

    print("Done.")


def _extract_table_6_metrics(t6: dict) -> dict[str, float]:
    """Pull committed metric values for Table 6."""
    summary = t6["summary"]
    label_to_metric = {
        "RK(B/P)": "M1_mean_coef_BP",
        "RK(SG)":  "M2_mean_coef_SG",
        "RK(OP)":  "M3_mean_coef_OP",
        "RK(Ltg)": "M4_mean_coef_Ltg",
    }
    tstat_to_metric = {
        "RK(B/P)": "M1_tstat_BP",
        "RK(SG)":  "M2_tstat_SG",
        "RK(OP)":  "M3_tstat_OP",
        "RK(Ltg)": "M4_tstat_Ltg",
    }
    metrics: dict[str, float] = {}
    for label, row in summary.iterrows():
        coef = row["Mean coef"]
        tstat = row["NW t-stat (2 lags)"]
        if label in label_to_metric and not (isinstance(coef, float) and np.isnan(coef)):
            metrics[label_to_metric[label]] = float(coef)
        if label in tstat_to_metric and not (isinstance(tstat, float) and np.isnan(tstat)):
            metrics[tstat_to_metric[label]] = float(tstat)
    return metrics


def _extract_table_7_metrics(t7: dict) -> dict[str, float]:
    """Pull committed metric values for Table 7."""
    summary = t7["summary"]
    label_to_metric = {
        "RK(SG)":   "mean_coef_SG",
        "RK(B/P)":  "mean_coef_BP",
        "RK(OP)":   "mean_coef_OP",
        "RK(Ltg)":  "mean_coef_Ltg",
    }
    tstat_to_metric = {
        "RK(SG)":   "tstat_SG",
        "RK(B/P)":  "tstat_BP",
        "RK(OP)":   "tstat_OP",
        "RK(Ltg)":  "tstat_Ltg",
    }
    metrics: dict[str, float] = {}
    for label, row in summary.iterrows():
        coef = row["Mean coef"]
        tstat = row["NW t-stat (2 lags)"]
        if label in label_to_metric and not (isinstance(coef, float) and np.isnan(coef)):
            metrics[label_to_metric[label]] = float(coef)
        if label in tstat_to_metric and not (isinstance(tstat, float) and np.isnan(tstat)):
            metrics[tstat_to_metric[label]] = float(tstat)
    # Avg R^2 from annual
    annual = t7["annual"]
    if len(annual) > 0 and "R2" in annual.columns:
        mean_r2 = float(annual["R2"].mean())
        if not np.isnan(mean_r2):
            metrics["mean_R2"] = mean_r2
    return metrics


if __name__ == "__main__":
    main()

