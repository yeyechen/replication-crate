"""
Replication of Lakonishok, Shleifer & Vishny (1994), "Contrarian Investment,
Extrapolation, and Risk" (JPE).

STAGE: data pipeline only. Builds the analysis-ready panel at
data/panel.parquet — one row per (permno, formation_year) — and prints a
diagnostic report. No results/*.md tables yet.

All substantive computation (PIT universe, CCM link, market equity, book equity,
E/P, C/P, S/P, D/P, B/M, sales-growth GS and its cross-sectional rank, size
deciles) is done in ClickHouse SQL under src/sql/. This file only reads those SQL
files, executes them, assembles the panel, computes the annual holding-year
returns (a 12-month compounding with the Assumption-A6 delisting gross-up, done
in pandas because the conditional compounding of -1 / missing returns is far more
robust there than via SQL aggregates), writes data/panel.parquet, and prints
diagnostics.

Run from the repo root:
    cd <internal>/rep-it-up && \
        uv run python replications/contrarian_investment/src/main.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

# --- repo root on sys.path so `from utils.paths import paper_layout` works ---
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(REPO_ROOT / ".env")

from clickhouse_driver import Client  # noqa: E402
from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402

# --- configuration ---------------------------------------------------------
# Pin the replications root to the resolved repo root so the script works from
# any working directory (not only when cwd == repo root).
LAYOUT = paper_layout("contrarian_investment",
                      replications_root=REPO_ROOT / "replications")
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")
DATA_PATH = LAYOUT.data_path("panel.parquet")
RULES = json.loads(LAYOUT.preparations_path("preprocessing_rules.json").read_text())

N_HOLD_YEARS = 5          # Years +1..+5 (var_annual_buy_hold_ew)
N_SIZE_DEC = 10           # Assumption A5
GS_WEIGHTS = [5, 4, 3, 2, 1]  # year -1..-5 (sort_gs_weighted_rank / A4)

_CFG = get_clickhouse_config()
TIMINGS: dict[str, float] = {}


def _client() -> Client:
    return Client(
        host=_CFG["host"], port=int(_CFG["port"]),
        user=_CFG["user"], password=_CFG["password"],
    )


def q(sql: str) -> pd.DataFrame:
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    t = time.time()
    df = q((SQL_DIR / name).read_text())
    TIMINGS[name] = time.time() - t
    print(f"  [{name}] {len(df):,} rows in {TIMINGS[name]:.1f}s")
    return df


# --- holding-year returns (Assumption A6) ----------------------------------
def compute_size_benchmarks_monthly(size_dec: pd.DataFrame,
                                    stock_ret: pd.DataFrame) -> pd.DataFrame:
    """EW monthly return per (fy, size_dec, mnum).

    Membership = formation-year size-decile members (A5 fixed assignment); in each
    month the EW return is the mean over members PRESENT that month (a delisted
    member earns coalesce(ret, dlret) in its delisting month and exits thereafter —
    already absorbed in stock_ret).
    """
    members = size_dec[["fy", "permno", "size_dec"]]
    j = members.merge(stock_ret, on="permno", how="inner")
    out = (
        j.groupby(["fy", "size_dec", "mnum"], as_index=False)["ret"]
        .mean()
        .rename(columns={"ret": "ew_ret"})
    )
    return out


def compute_holding_returns(panel_base: pd.DataFrame,
                            stock_ret: pd.DataFrame,
                            sizedec_monthly: pd.DataFrame,
                            delist: pd.DataFrame) -> pd.DataFrame:
    """Annual holding-year return for each (permno, fy, k=1..5).

    Holding year k spans May Y .. April Y+1 with Y = fy + k - 1 (12 months).
    Monthly return used in month j (1..12):
        * stock's own return (delret absorbed) for months up to and including the
          delisting month;
        * the stock's size-decile EW return for the months strictly after delisting
          (A6 gross-up: stock_ret_k = (1+r_stock_to_del)*(1+r_sizedec_rest) - 1).
    A stock delisted before the holding-year start is not a member (alive_k = 0).
    """
    base = panel_base[["fy", "permno", "size_dec"]].copy()

    # expand to (fy, permno, size_dec, k, j) grid
    ks = pd.DataFrame({"k": np.arange(1, N_HOLD_YEARS + 1)})
    js = pd.DataFrame({"j": np.arange(12)})
    grid = (
        base.assign(_k=1).merge(ks.assign(_k=1), on="_k").drop(columns="_k")
            .assign(_j=1).merge(js.assign(_j=1), on="_j").drop(columns="_j")
    )
    grid["start"] = (grid["fy"] + grid["k"] - 1) * 12 + 5      # May of Y (mnum)
    grid["mnum"] = grid["start"] + grid["j"]

    # stock monthly return (0 when absent — the NULL->0 rule, gaps/halts)
    grid = grid.merge(
        stock_ret.rename(columns={"ret": "stock_r"}),
        on=["permno", "mnum"], how="left",
    )
    grid["stock_r"] = grid["stock_r"].fillna(0.0)

    # size-decile monthly EW return (0 when missing)
    grid = grid.merge(
        sizedec_monthly.rename(columns={"ew_ret": "sd_r"}),
        on=["fy", "size_dec", "mnum"], how="left",
    )
    grid["sd_r"] = grid["sd_r"].fillna(0.0)

    # delisting month of the stock
    grid = grid.merge(delist[["permno", "dl_mnum"]], on="permno", how="left")

    in_year = (grid["dl_mnum"] >= grid["start"]) & (grid["dl_mnum"] <= grid["start"] + 11)
    grid["offset"] = np.where(in_year, grid["dl_mnum"] - grid["start"] + 1, np.nan)
    grid["alive"] = np.where(
        grid["dl_mnum"].isna() | (grid["dl_mnum"] >= grid["start"]), 1, 0
    )
    # effective monthly return: stock up to & incl. delisting month, sizedec after
    use_stock = grid["offset"].isna() | ((grid["j"] + 1) <= grid["offset"])
    grid["eff"] = np.where(use_stock, grid["stock_r"], grid["sd_r"])
    grid["one_eff"] = 1.0 + grid["eff"]
    grid["one_sd"] = 1.0 + grid["sd_r"]

    g = grid.groupby(["fy", "permno", "k"], sort=False)
    res = pd.DataFrame({
        "prod_eff": g["one_eff"].prod(),
        "prod_sd": g["one_sd"].prod(),
        "alive": g["alive"].max(),
        "size_dec": g["size_dec"].first(),
        "delist_offset": g["offset"].max(),
    }).reset_index()
    res["stock_ret"] = np.where(res["alive"] == 1, res["prod_eff"] - 1.0, np.nan)
    res["sizedec_ret"] = np.where(res["size_dec"].notna(), res["prod_sd"] - 1.0, np.nan)

    # pivot k=1..5 into wide columns
    wide = res.pivot(index=["fy", "permno"], columns="k")
    wide.columns = [f"{a}_{int(b)}" for a, b in wide.columns]
    wide = wide.reset_index()
    rename = {}
    for k in range(1, N_HOLD_YEARS + 1):
        rename[f"stock_ret_{k}"] = f"stock_ret_{k}"
        rename[f"sizedec_ret_{k}"] = f"sizedec_ret_{k}"
        rename[f"alive_{k}"] = f"alive_{k}"
        rename[f"delist_offset_{k}"] = f"delist_month_offset_{k}"
    wide = wide.rename(columns=rename)
    keep = ["fy", "permno"]
    for k in range(1, N_HOLD_YEARS + 1):
        keep += [f"stock_ret_{k}", f"sizedec_ret_{k}", f"alive_{k}",
                 f"delist_month_offset_{k}"]
    return wide[keep]


# --- diagnostics -----------------------------------------------------------
def print_diagnostics(panel: pd.DataFrame, coercion: pd.DataFrame,
                      delist: pd.DataFrame) -> None:
    print("\n" + "=" * 72)
    print("DIAGNOSTIC REPORT — contrarian_investment (LSV 1994) data pipeline")
    print("=" * 72)

    print(f"\n[1] Panel dimensions: {panel.shape[0]:,} rows x {panel.shape[1]} cols")
    nfy = panel.groupby("fy")["permno"].nunique()
    print("    N stocks per formation year:")
    print("    " + nfy.to_dict().__str__())
    low = nfy[nfy < 300]
    print(f"    formations with < 300 stocks: {dict(low) if len(low) else 'NONE'}")

    print("\n[2] Signal diagnostics")
    med_bm = panel[panel["be_valid"] == 1].groupby("fy")["bm"].median()
    print("    median B/M per formation (full sample, be_valid=1):")
    print("    " + med_bm.round(4).to_dict().__str__())
    cov = {
        "be_valid": panel["be_valid"].mean(),
        "ep_pos": panel["ep_pos"].mean(),
        "cp_pos": panel["cp_pos"].mean(),
        "gs_valid": panel["n_gs_years"].ge(1).mean(),
    }
    print("    avg fraction of universe (across all rows):")
    for c, v in cov.items():
        print(f"      {c:9s} = {v:.4f}")
    # distribution check at 1989: mean B/M of bottom vs top decile
    p89 = panel[(panel["fy"] == 1989) & (panel["be_valid"] == 1)].copy()
    p89["bm_dec"] = pd.qcut(p89["bm"], 10, labels=False) + 1
    ends = p89.groupby("bm_dec").agg(n=("bm", "size"), mean_bm=("bm", "mean"),
                                     mean_me=("me_apr", "mean"))
    d1, d10 = ends.loc[1], ends.loc[10]
    print(f"    1989 formation B/M deciles: dec1 mean_bm={d1['mean_bm']:.4f} "
          f"(mean_me={d1['mean_me']:.3e}), dec10 mean_bm={d10['mean_bm']:.4f} "
          f"(mean_me={d10['mean_me']:.3e})")

    print("\n[3] IBM check at formation 1989 (permno 12490, gvkey 006066)")
    ibm = panel[(panel["fy"] == 1989) & (panel["permno"] == 12490)]
    if len(ibm):
        r = ibm.iloc[0]
        print(f"    me_apr={r['me_apr']:.4e} (expect ~6.75e10)")
        print(f"    be={r['be']:.1f} (A2: ceq+txdb)  bm={r['bm']:.4f} "
              f"(A2 ~0.65; ceq-only ~0.59)")
        print(f"    earn={r['earn']:.1f}  ep={r['ep']:.4f} (expect ~0.081)")
        print(f"    cf={r['cf']:.1f}  cp={r['cp']:.4f} (expect ~0.139)")
        print(f"    n_gs_years={int(r['n_gs_years'])}  gs_wavg={r['gs_wavg']:.4f}  "
              f"gs_rank_frac={r['gs_rank_frac']:.4f}  size_dec={int(r['size_dec'])}")
        print(f"    NEW cols: sale_m6={r['sale_m6']} earn_m6={r['earn_m6']} "
              f"cf_m6={r['cf_m6']}  ret_m3_0={r['ret_m3_0']:.4f}")

    print("\n[3b] Panel extension check")
    print(f"    ret_m3_0 non-null = {panel['ret_m3_0'].notna().sum():,} / {len(panel):,}")
    print(f"    has _m6 cols: "
          f"{all(c in panel.columns for c in ['sale_m6','earn_m6','cf_m6','div_m6'])}")
    print(f"    panel shape = {panel.shape}")

    print("\n[4] Delisting replacement")
    for k in range(1, N_HOLD_YEARS + 1):
        n_del = panel[f"delist_month_offset_{k}"].notna().sum()
        n_alive0 = (panel[f"alive_{k}"] == 0).sum()
        print(f"    holding year +{k}: mid-year delistings={int(n_del):5d}  "
              f"(alive_{k}=0 i.e. delisted before year start: {int(n_alive0)})")
    print(f"    alive_1==1 for all rows: {bool((panel['alive_1'] == 1).all())} "
          f"(count alive_1==0: {int((panel['alive_1'] == 0).sum())})")
    print(f"    NULL monthly rets coerced: n_msf_null={int(coercion['n_msf_null'].iloc[0])}, "
          f"n_msf_sentinel={int(coercion['n_msf_sentinel'].iloc[0])} "
          f"(of {int(coercion['n_msf_total'].iloc[0])} msf rows)")

    print("\n[5] 1989-formation B/M decile market-cap check (glamour vs value)")
    print(f"    dec1 (low B/M, glamour) mean me_apr = {d1['mean_me']:.4e}")
    print(f"    dec10 (high B/M, value)  mean me_apr = {d10['mean_me']:.4e}")
    print(f"    ratio dec1/dec10 = {d1['mean_me'] / d10['mean_me']:.2f}x "
          f"(glamour should be much larger)")

    print("\n[6] Runtime per SQL step (seconds)")
    for name, t in TIMINGS.items():
        print(f"    {name:32s} {t:7.1f}s")
    print("=" * 72)


def compute_ret_m3_0(panel: pd.DataFrame, stock_ret: pd.DataFrame) -> pd.DataFrame:
    """Cumulative stock return over the 36 months May(t-3)..April(t).

    Uses every month present for the stock in that window (delret already absorbed
    in stock_ret). NULL when fewer than 12 months are present.
    """
    base = panel[["fy", "permno"]].drop_duplicates()
    js = pd.DataFrame({"j": np.arange(36)})
    grid = base.assign(_j=1).merge(js.assign(_j=1), on="_j").drop(columns="_j")
    grid["mnum"] = (grid["fy"] - 3) * 12 + 5 + grid["j"]   # May(t-3)+j
    grid = grid.merge(stock_ret.rename(columns={"ret": "r"}),
                      on=["permno", "mnum"], how="left")
    grid["one"] = 1 + grid["r"].fillna(0.0)
    g = grid.groupby(["fy", "permno"], sort=False)
    nmonths = g["r"].count()                 # non-null months present
    cum = g["one"].prod() - 1                # product over present months (NaN->1)
    out = pd.DataFrame({"n_months": nmonths, "ret_m3_0": cum}).reset_index()
    out.loc[out["n_months"] < 12, "ret_m3_0"] = np.nan
    return out[["fy", "permno", "ret_m3_0", "n_months"]]


def main() -> None:
    print("Loading SQL outputs from ClickHouse ...")
    formation = q_file("formation_dates.sql")
    signals = q_file("signals.sql")
    size_dec = q_file("size_deciles.sql")[["fy", "permno", "size_dec"]]
    stock_ret = q_file("stock_returns_monthly.sql")
    delist = q_file("delistings.sql")
    coercion = q_file("coercion_counts.sql")

    print("\nAssembling panel ...")
    # merge size decile onto the signal cross-section (one row per fy, permno)
    panel = signals.merge(size_dec, on=["fy", "permno"], how="left")
    n_no_sd = panel["size_dec"].isna().sum()
    print(f"  panel rows: {len(panel):,}; missing size_dec: {int(n_no_sd):,} "
          f"({100 * n_no_sd / len(panel):.2f}%)")

    # size-decile EW monthly benchmark (from decile members present each month)
    t = time.time()
    sizedec_monthly = compute_size_benchmarks_monthly(size_dec, stock_ret)
    TIMINGS["py_size_benchmarks_monthly"] = time.time() - t
    print(f"  sizedec_monthly: {len(sizedec_monthly):,} rows in "
          f"{TIMINGS['py_size_benchmarks_monthly']:.1f}s")

    # annual holding-year returns with delisting replacement
    t = time.time()
    holding = compute_holding_returns(panel, stock_ret, sizedec_monthly, delist)
    TIMINGS["py_holding_returns"] = time.time() - t
    print(f"  holding returns: {len(holding):,} rows in "
          f"{TIMINGS['py_holding_returns']:.1f}s")

    panel = panel.merge(holding, on=["fy", "permno"], how="left")

    # 3-year pre-formation cumulative stock return, May(t-3)..April(t) (36 months),
    # dlret absorbed in delisting months (already in stock_ret). NULL if <12 months
    # present in the window (e.g. stock listed mid-window or delisted early).
    t = time.time()
    ret30 = compute_ret_m3_0(panel, stock_ret)
    TIMINGS["py_ret_m3_0"] = time.time() - t
    panel = panel.merge(ret30, on=["fy", "permno"], how="left")
    n_null_r30 = panel["ret_m3_0"].isna().sum()
    print(f"  ret_m3_0: null (n_months<12 or no data) = {n_null_r30:,} in "
          f"{TIMINGS['py_ret_m3_0']:.1f}s")

    # order columns
    wide_acct = []
    for pre in ["sale", "earn", "cf", "div"]:
        for suf in ["m6", "m5", "m4", "m3", "m2", "m1", "p0", "p1", "p2", "p3", "p4"]:
            wide_acct.append(f"{pre}_{suf}")
    lead = ["permno", "fy", "form_date", "gvkey", "me_apr", "be", "be_valid", "bm",
            "earn", "cf", "ep", "cp", "sp", "dp_ratio", "ep_pos", "cp_pos",
            "gs_wavg", "gs_rank_frac", "n_gs_years", "size_dec",
            "sig_datadate", "sig_fyear"]
    ret_cols = ["ret_m3_0"]
    for k in range(1, N_HOLD_YEARS + 1):
        ret_cols += [f"stock_ret_{k}", f"sizedec_ret_{k}", f"alive_{k}",
                     f"delist_month_offset_{k}"]
    cols = lead + wide_acct + ret_cols
    cols = [c for c in cols if c in panel.columns]
    panel = panel[cols].sort_values(["fy", "permno"]).reset_index(drop=True)

    panel.to_parquet(DATA_PATH, index=False)
    print(f"\nWrote {DATA_PATH}  ({panel.shape[0]:,} rows x {panel.shape[1]} cols)")

    print_diagnostics(panel, coercion, delist)


if __name__ == "__main__":
    main()
