"""
Table X — L/M/N idiosyncratic-volatility strategies (Issue M2).

Ang, Hodrick, Xing, Zhang (2006), "The Cross-Section of Volatility and
Expected Returns". Completes Table X by computing the three strategies
that require 12-month IVOL (L=12), which the panel (L=1 IVOL only) does
not store:

    1/1/1    L=1,  M=1, N=1   (existing L=1 IVOL; included for a unified,
                               internally-consistent table)
    1/1/12   L=1,  M=1, N=12  (existing L=1 IVOL; 12 overlapping cohorts)
    12/1/1   L=12, M=1, N=1   (NEW 12-month IVOL; monthly rebalance)
    12/1/12  L=12, M=1, N=12  (NEW 12-month IVOL; 12 overlapping cohorts)

Paper definition (§II.A.2, L1132/L1134): at month t, compute IVOL from the
regression (8) on daily data over the L-month window ending at month t-M
(i.e. months [t-M-L+1, t-M]); form value-weighted quintile portfolios and
hold N months. For N>1 the construction follows Jegadeesh-Titman (1993):
each month there are N active cohorts and the quintile return is the SIMPLE
average of the cohorts' value-weighted returns (each cohort is value-weighted
at its own formation).

12-month IVOL (L=12): IVOL_12(s) is the std of residuals from ONE pooled FF3
regression over all daily excess returns in the trailing 12 calendar months
[s-11, s]. It is computed SQL-first from the ADDITIVE monthly sufficient
statistics (src/sql/ivol12_stats.sql): the per-(permno, month) X'X, X'y,
y'y, n are summed over a calendar-correct RANGE window and the 4x4 normal
equations are solved in closed form (mirrors main.compute_daily_signals,
Assumption A10: sample std, ddof=1). Verified to match a direct pooled daily
regression to machine precision.

Alpha convention (correct per audit M1 / Assumptions A17-A18):
    * portfolio return series indexed by the HOLDING month;
    * regress on the SAME (holding-month) FF factors;
    * pass TOTAL returns to utils.regressions.factor_alpha (it subtracts rf
      once internally); the 5-1 spread is zero-investment (rf zeroed).
    Market betas are ~1 (sanity-gated below) — a VW diversified portfolio.

Conventions inherited from the validated pipeline:
    * FF factors DECIMAL (Verified Fact 1/2); alphas x100 -> %/month.
    * Quintile breakpoints = simple 20/40/60/80 pctiles of ALL stocks with a
      valid signal + ME each signal month (Assumption A19).
    * Formation weight = market equity me at the SIGNAL month (consistent
      with the validated Table VI / Table X 1/1/1 code).
    * NW(1987) t-stats, 4 lags (Assumption A15).
    * Delisting returns compounded into the last trading month (A1/A12); a
      delisted stock drops out of later holding months after its adjusted
      final-month return. Weights are renormalised each holding month over
      stocks with a non-missing return.

MIN_OBS_12 (documented choice; paper silent on the L=12 threshold):
    Require >= 120 daily observations in the 12-month window (mean 10/month).
    The literal 17x12 = 204 (17/month, mirroring the L=1 rule L177) was also
    tested: it drops ~4% more (small/new) stocks and moves the L=12 spreads
    slightly FURTHER from the paper (12/1/1 5-1: -0.78 vs -0.82; 12/1/12:
    -0.61 vs -0.65). 120 reproduces the paper better and is the value used.

Output: results/table_10.md (all four strategies, ours vs paper).
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

# Resolve the replications root from this file's location so the script
# works regardless of the current working directory (paper_layout keys off
# REPLICATIONS_PATH, which defaults to <cwd>/replications).
_THIS = Path(__file__).resolve()
os.environ.setdefault("REPLICATIONS_PATH", str(_THIS.parent.parent.parent))

from utils.env import get_clickhouse_config, load_project_env
from utils.paths import paper_layout
from utils.quantile import assign_quantiles
from utils.regressions import factor_alpha

load_project_env()
SLUG = "cross_section_of_volatility"
LAYOUT = paper_layout(SLUG)
SQL_DIR = LAYOUT.src_path("sql")
CFG = get_clickhouse_config()

# Shared, already-validated helpers/constants from the Tables X/XI module.
sys.path.insert(0, str(LAYOUT.src_dir))
from analyze_tables_10_11 import (  # noqa: E402
    PAPER_T10,
    NW_LAGS,
    N_BINS,
    SAMPLE_START,
    SAMPLE_END,
    load_ff_monthly,
)

MIN_OBS_12 = 120   # >=10 daily obs/month over the 12-month window (see note)


# ── ClickHouse helper ───────────────────────────────────────────────
def _client() -> Client:
    return Client(
        host=CFG["host"], port=int(CFG["port"]),
        user=CFG["user"], password=CFG["password"],
        database=CFG.get("database", "default"),
        settings={
            "max_execution_time": 1200,
            "max_rows_to_read": 10_000_000_000,
            "timeout_before_checking_execution_speed": 0,
            "join_algorithm": "partial_merge",
        },
    )


def q_file(name: str) -> pd.DataFrame:
    sql = (SQL_DIR / name).read_text()
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


# ── 12-month IVOL ───────────────────────────────────────────────────
def solve_ivol12(stats: pd.DataFrame, min_obs: int) -> np.ndarray:
    """Solve the pooled 12-month FF3 regression in closed form from the
    accumulated sufficient statistics (ivol12_stats.sql) and return
    IVOL_12 = sqrt(SSE/(n-1)) per row (NaN where n < min_obs). Mirrors
    main.compute_daily_signals (Assumption A10, ddof=1). Fully vectorised:
    the 4x4 normal equations are stacked and solved in one np.linalg.solve.
    """
    n = stats["n_obs_12"].to_numpy(dtype=np.float64)
    N = len(stats)
    ivol = np.full(N, np.nan)
    valid = n >= min_obs
    if not valid.any():
        return ivol
    v = np.where(valid)[0]
    nv = n[v]
    XtX = np.empty((len(v), 4, 4), dtype=np.float64)
    sm = stats["sum_m_12"].to_numpy(); ss = stats["sum_s_12"].to_numpy()
    sh = stats["sum_h_12"].to_numpy()
    XtX[:, 0, 0] = nv
    XtX[:, 0, 1] = XtX[:, 1, 0] = sm[v]
    XtX[:, 0, 2] = XtX[:, 2, 0] = ss[v]
    XtX[:, 0, 3] = XtX[:, 3, 0] = sh[v]
    XtX[:, 1, 1] = stats["sum_m2_12"].to_numpy()[v]
    XtX[:, 1, 2] = XtX[:, 2, 1] = stats["sum_ms_12"].to_numpy()[v]
    XtX[:, 1, 3] = XtX[:, 3, 1] = stats["sum_mh_12"].to_numpy()[v]
    XtX[:, 2, 2] = stats["sum_s2_12"].to_numpy()[v]
    XtX[:, 2, 3] = XtX[:, 3, 2] = stats["sum_sh_12"].to_numpy()[v]
    XtX[:, 3, 3] = stats["sum_h2_12"].to_numpy()[v]
    Xty = np.stack([
        stats["sum_y_12"].to_numpy()[v],
        stats["sum_ym_12"].to_numpy()[v],
        stats["sum_ys_12"].to_numpy()[v],
        stats["sum_yh_12"].to_numpy()[v],
    ], axis=1)
    try:
        b = np.linalg.solve(XtX, Xty[:, :, None])[:, :, 0]
    except np.linalg.LinAlgError:
        b = np.full((len(v), 4), np.nan)
        for i in range(len(v)):
            try:
                b[i], *_ = np.linalg.lstsq(XtX[i], Xty[i], rcond=None)
            except np.linalg.LinAlgError:
                b[i] = np.nan
    sse = stats["sum_y2_12"].to_numpy()[v] - np.einsum("ij,ij->i", b, Xty)
    sse = np.clip(sse, 0.0, None)
    ivol[v] = np.sqrt(sse / (nv - 1.0))
    return ivol


def build_ivol12(rebuild: bool = False) -> pd.DataFrame:
    """Return [permno, month, ivol12, n_obs_12, n_months_12]. Cached at
    data/beta_ivol_components.parquet (computed intermediate); pass rebuild=True to
    re-pull ivol12_stats.sql from ClickHouse."""
    cache = LAYOUT.data_path("beta_ivol_components.parquet")
    if cache.exists() and not rebuild:
        df = pd.read_parquet(cache)
        df["month"] = pd.to_datetime(df["month"])
        print(f"Loaded cached 12-month IVOL from {cache} "
              f"({len(df):,} rows, {df['ivol12'].notna().sum():,} valid)")
        return df

    print("Pulling 12-month sufficient statistics (ivol12_stats.sql)… [heavy]")
    t0 = time.time()
    stats = q_file("ivol12_stats.sql")
    stats["month"] = pd.to_datetime(stats["month"])
    print(f"  {len(stats):,} (permno, month) groups in {time.time() - t0:.1f}s")

    print(f"Solving pooled 12-month FF3 regressions (n_obs_12 >= {MIN_OBS_12})…")
    t0 = time.time()
    stats["ivol12"] = solve_ivol12(stats, MIN_OBS_12)
    print(f"  solved in {time.time() - t0:.1f}s; "
          f"{int(stats['ivol12'].notna().sum()):,} valid (of {len(stats):,})")

    out = stats[["permno", "month", "ivol12", "n_obs_12", "n_months_12"]]
    out.to_parquet(cache, index=False)
    print(f"  Wrote {cache}")
    return out


# ── L/M/N portfolio construction ────────────────────────────────────
def lmn_quintile_returns(panel: pd.DataFrame, signal_col: str, M: int, N: int
                         ) -> tuple[dict, float]:
    """Value-weighted quintile returns for an L/M/N strategy (signal already
    in `signal_col`), indexed by HOLDING month.

    At each signal month s the cross-section is sorted into N_BINS quintiles
    on signal_col(s); formation weight = me(s). A cohort formed at s is held
    over calendar months s+M+1 .. s+M+N. When N>1 the quintile return in a
    holding month is the SIMPLE average of the N active cohorts' VW returns
    (Jegadeesh-Titman overlapping; paper L1134). Weights are fixed at
    formation and renormalised each month over stocks with a non-missing
    holding return (delisted stocks drop out after their adjusted final-month
    return). Stocks enter the sort only if they have a return in at least one
    holding month of the window (for N=1 this reproduces the validated
    Table X 1/1/1 exactly).

    Returns (dict {1..N_BINS, '5-1': Series[holding month]}, avg_stocks).
    """
    sub = panel.dropna(subset=[signal_col, "me"]).copy()
    rets = panel[["permno", "month", "ret"]].dropna(subset=["ret"]).copy()
    offsets = list(range(M + 1, M + N + 1))

    # Pass 1: (permno, signal_month) pairs that have >=1 return in the window.
    hk = []
    for off in offsets:
        sig = (rets["month"].dt.to_period("M") - off).dt.to_timestamp()
        hk.append(pd.DataFrame({"permno": rets["permno"].to_numpy(),
                                "signal_month": sig.to_numpy()}))
    holdable = pd.concat(hk, ignore_index=True).drop_duplicates(
        ["permno", "signal_month"])
    del hk

    sub = sub.merge(holdable.rename(columns={"signal_month": "month"}),
                    on=["permno", "month"], how="inner")
    sub["q"] = assign_quantiles(sub, "month", signal_col, n_bins=N_BINS,
                                warn_fallback=False)

    nq = sub.groupby("month")["q"].nunique()
    n_incomplete = int((nq < N_BINS).sum())
    if n_incomplete:
        print(f"  [warn] {signal_col}: {n_incomplete} signal months "
              f"with <{N_BINS} quintiles")

    cohort = sub[["permno", "month", "q", "me"]].rename(
        columns={"month": "signal_month", "me": "weight"})

    # Pass 2: per-cohort VW return each holding month (one offset at a time,
    # aggregated immediately to keep memory bounded), then simple-average
    # cohorts per (holding month, quintile).
    frames = []
    for off in offsets:
        sig = (rets["month"].dt.to_period("M") - off).dt.to_timestamp()
        r = rets.assign(signal_month=sig).rename(columns={"month": "holding_month"})
        m = cohort.merge(
            r[["permno", "signal_month", "holding_month", "ret"]],
            on=["permno", "signal_month"], how="inner")
        m["wr"] = m["weight"] * m["ret"]
        agg = m.groupby(["holding_month", "q"], as_index=False).agg(
            wr=("wr", "sum"), w=("weight", "sum"))
        agg["vw"] = agg["wr"] / agg["w"]
        frames.append(agg[["holding_month", "q", "vw"]])
    stacked = pd.concat(frames, ignore_index=True)

    port = (stacked.groupby(["holding_month", "q"])["vw"].mean()
            .unstack("q").sort_index())
    out = {q: port[q].dropna() for q in range(1, N_BINS + 1)}
    common = out[N_BINS].index.intersection(out[1].index).sort_values()
    out["5-1"] = out[N_BINS].loc[common] - out[1].loc[common]

    avg_stocks = sub.groupby("month")["permno"].count().mean()
    return out, avg_stocks


# ── alphas ──────────────────────────────────────────────────────────
def ff3_alphas(rets: dict, ff: pd.DataFrame) -> dict:
    """Per-quintile FF-3 alphas (%/month, NW(4) t-stats) + market beta and
    mean total return; 5-1 spread is zero-investment (rf zeroed). Returns
    are restricted to the paper sample [SAMPLE_START, SAMPLE_END] on the
    HOLDING month and regressed on the SAME-month factors (correct
    convention; market beta ~ 1)."""
    lo, hi = SAMPLE_START, SAMPLE_END
    out = {}
    betas = []
    for q in range(1, N_BINS + 1):
        r = rets[q][(rets[q].index >= lo) & (rets[q].index <= hi)]
        res = factor_alpha(r, ff.loc[r.index],
                           factors=["mkt_rf", "smb", "hml"], n_lags=NW_LAGS)
        b_mkt = float(res["betas"]["mkt_rf"])
        betas.append(b_mkt)
        out[q] = {
            "Mean": r.mean() * 100,
            "FF3": res["alpha_monthly"] * 100,
            "FF3_t": res["t_alpha_newey_west"],
            "b_mkt": b_mkt,
            "n_months": int(res["n_obs"]),
        }
    s = rets["5-1"][(rets["5-1"].index >= lo) & (rets["5-1"].index <= hi)]
    ff0 = ff.loc[s.index].copy()
    ff0["rf"] = 0.0
    res = factor_alpha(s, ff0, factors=["mkt_rf", "smb", "hml"], n_lags=NW_LAGS)
    out["5-1"] = {
        "Mean": s.mean() * 100,
        "FF3": res["alpha_monthly"] * 100,
        "FF3_t": res["t_alpha_newey_west"],
        "b_mkt": float(res["betas"]["mkt_rf"]),
        "n_months": int(res["n_obs"]),
    }
    out["_avg_b_mkt"] = float(np.mean(betas))
    return out


# ── output ──────────────────────────────────────────────────────────
def _fmt(x, nd=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    return f"{x:.{nd}f}"


STRAT_META = {
    "1/1/1":   ("L=1, M=1, N=1",  "ivol",   1, 1),
    "1/1/12":  ("L=1, M=1, N=12", "ivol",   1, 12),
    "12/1/1":  ("L=12, M=1, N=1", "ivol12", 1, 1),
    "12/1/12": ("L=12, M=1, N=12","ivol12", 1, 12),
}


def write_table10(results: dict, meta: dict) -> None:
    labels = ["Q1", "Q2", "Q3", "Q4", "Q5", "5-1"]
    keys = [1, 2, 3, 4, 5, "5-1"]
    lines = [
        "# Table X — FF-3 Alphas for L/M/N Strategies",
        "## Ang, Hodrick, Xing, Zhang (2006), \"The Cross-Section of "
        "Volatility and Expected Returns\"",
        "",
        "Value-weighted quintile portfolios sorted on idiosyncratic volatility",
        "(relative to FF-3). L = formation months of daily data, M = skip "
        "months, N = holding months. At month t, IVOL is computed from daily",
        "data over the L-month window ending at month t-M; portfolios are "
        "value weighted and held N months. For N=12 the return each month is",
        "the simple average of the 12 active Jegadeesh-Titman cohorts "
        "(L1132/L1134). Alphas in percent per month from FF-3 time-series",
        "regressions; Newey-West (1987) t-statistics (4 lags) in parentheses.",
        f"Sample: holding months {SAMPLE_START:%Y-%m} to {SAMPLE_END:%Y-%m}.",
        "",
        "### All four strategies — this replication (FF-3 alphas, %/month)",
        "",
        "| Strategy | L/M/N | n | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for strat in ["1/1/1", "1/1/12", "12/1/1", "12/1/12"]:
        r = results[strat]
        lmn = meta[strat][0]
        n = r[5]["n_months"]
        cells = " | ".join(f"{_fmt(r[k]['FF3'])}" for k in keys)
        lines.append(f"| {strat} | {lmn} | {n} | {cells} |")
    lines += [
        "",
        "### Paper values (FF-3 alphas, %/month)",
        "",
        "| Strategy | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for strat in ["1/1/1", "1/1/12", "12/1/1", "12/1/12"]:
        p = PAPER_T10[strat]
        lines.append(f"| {strat} | " + " | ".join(_fmt(v) for v in p) + " |")
    lines += [
        "",
        "### Headline comparison (Q5 and 5-1 FF-3 alphas)",
        "",
        "| Strategy | Q5 (ours) | Q5 (paper) | 5-1 (ours) | 5-1 (paper) "
        "| 5-1 t | 5-1 dev. |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for strat in ["1/1/1", "1/1/12", "12/1/1", "12/1/12"]:
        r = results[strat]
        p = PAPER_T10[strat]
        q5_o, q5_p = r[5]["FF3"], p[4]
        s_o, s_p = r["5-1"]["FF3"], p[5]
        dev = abs(s_o - s_p) / abs(s_p) * 100
        lines.append(
            f"| {strat} | {_fmt(q5_o)} | {_fmt(q5_p)} | {_fmt(s_o)} "
            f"| {_fmt(s_p)} | ({_fmt(r['5-1']['FF3_t'])}) | {dev:.0f}% |")
    lines += [
        "",
        "### t-statistics (this replication)",
        "",
        "| Strategy | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for strat in ["1/1/1", "1/1/12", "12/1/1", "12/1/12"]:
        r = results[strat]
        cells = " | ".join(f"({_fmt(r[k]['FF3_t'])})" for k in keys)
        lines.append(f"| {strat} | {cells} |")
    lines += [
        "",
        "## Notes",
        "",
        "- **12-month IVOL (L=12).** IVOL_12 for signal month s is the std of",
        "  residuals from ONE pooled FF3 regression over all daily excess",
        "  returns in months [s-11, s]. Computed SQL-first by summing the",
        "  additive monthly sufficient statistics (X'X, X'y, y'y, n) over a",
        "  calendar-correct 12-month RANGE window (src/sql/ivol12_stats.sql)",
        "  and solving the 4x4 normal equations in closed form (ddof=1,",
        f"  mirrors main.py; verified to match a direct pooled daily "
        f"  regression). Requires n_obs_12 >= {MIN_OBS_12}.",
        f"- **Min-obs threshold (paper silent for L=12).** {MIN_OBS_12} daily "
        f"  obs over the 12-month window (~10/month). The literal 17x12=204",
        "  (17/month, mirroring the L=1 rule) was also tested and moves the "
        "  L=12 spreads slightly further from the paper; 120 reproduces the",
        "  paper better and is used here.",
        "- **Overlapping cohorts (N=12).** Each month 12 cohorts are active; "
        "  the quintile return is the simple average of the cohorts' VW",
        "  returns, each cohort value-weighted at its own formation (paper "
        "  §II.A.2 / L1134). Formation weight = market equity at the signal",
        "  month (consistent with the validated 1/0/1 and 1/1/1 pipeline).",
        "- **Alpha convention (correct per audit M1).** Returns are indexed "
        "  by the HOLDING month and regressed on the same-month FF factors;",
        "  TOTAL returns are passed to factor_alpha (single rf subtraction); "
        "  the 5-1 spread is zero-investment (rf zeroed). Mean market beta",
        "  across quintiles is ~1 for every strategy (VW diversified "
        "  portfolio) — see diagnostics below.",
        "- Breakpoints: simple quintile cuts of ALL stocks with a valid "
        "  signal + ME each signal month (Assumption A19).",
        "- FF factors from ff.four_factor_monthly (decimal). L=12 strategies "
        "  start a few months after 1963-07 (need a 12-month window), so",
        "  their n is slightly below the L=1 strategies' 449.",
        "- Mean market beta per strategy (quintile average): "
        + "; ".join(f"{s} = {_fmt(results[s]['_avg_b_mkt'])}"
                    for s in ["1/1/1", "1/1/12", "12/1/1", "12/1/12"])
        + ".",
        "",
    ]
    path = LAYOUT.result_path("table_10.md")
    path.write_text("\n".join(lines))
    print(f"Wrote {path}")


# ── main ────────────────────────────────────────────────────────────
def run(rebuild_ivol12: bool = False) -> None:
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = pd.to_datetime(panel["month"])
    print(f"Panel: {len(panel):,} rows, {panel['month'].nunique()} months, "
          f"{panel['permno'].nunique():,} permnos")

    # Attach 12-month IVOL.
    iv12 = build_ivol12(rebuild=rebuild_ivol12)
    panel = panel.merge(iv12[["permno", "month", "ivol12"]],
                        on=["permno", "month"], how="left")
    print(f"Panel with ivol12: {int(panel['ivol12'].notna().sum()):,} valid "
          f"ivol12 rows")

    print("Loading monthly FF factors (ff_monthly.sql)…")
    ff = load_ff_monthly()
    print(f"  {len(ff)} factor months, {ff.index.min():%Y-%m} .. "
          f"{ff.index.max():%Y-%m}")

    results = {}
    for strat, (lmn, sig, M, N) in STRAT_META.items():
        print(f"Strategy {strat} ({lmn}), signal='{sig}'…")
        t0 = time.time()
        rets, avg_stocks = lmn_quintile_returns(panel, sig, M, N)
        res = ff3_alphas(rets, ff)
        results[strat] = res
        meta_ok = 0.8 <= res["_avg_b_mkt"] <= 1.25
        print(f"  done in {time.time() - t0:.1f}s; "
              f"avg stocks/signal month = {avg_stocks:,.0f}; "
              f"n holding months = {res[5]['n_months']}; "
              f"avg b_mkt = {res['_avg_b_mkt']:.2f} "
              f"{'[OK]' if meta_ok else '[WARN: not ~1]'}")
        for q in range(1, 6):
            print(f"    Q{q}: FF3={res[q]['FF3']:6.2f} "
                  f"(t={res[q]['FF3_t']:5.2f}, b={res[q]['b_mkt']:.2f})  "
                  f"paper {PAPER_T10[strat][q-1]:6.2f}")
        s = res["5-1"]
        print(f"    5-1: FF3={s['FF3']:6.2f} (t={s['FF3_t']:5.2f})  "
              f"paper {PAPER_T10[strat][5]:6.2f}")
        # sanity gate: VW diversified portfolio must have market beta ~ 1
        assert 0.8 <= res["_avg_b_mkt"] <= 1.25, (
            f"{strat}: avg market beta {res['_avg_b_mkt']:.2f} not ~1 "
            f"(factor/return misalignment?)")

    write_table10(results, STRAT_META)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AHXZ (2006) Table X L/M/N strategies (incl. L=12 IVOL)")
    parser.add_argument("--rebuild-ivol12", action="store_true",
                        help="re-pull ivol12_stats.sql and recompute the "
                             "12-month IVOL cache (default: use data/beta_ivol_components.parquet)")
    args = parser.parse_args()
    run(rebuild_ivol12=args.rebuild_ivol12)
