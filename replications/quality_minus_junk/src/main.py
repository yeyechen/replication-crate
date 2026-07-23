"""
Replication of Asness, Frazzini, Pedersen (2019) "Quality Minus Junk".

Data pipeline (this file): builds the analysis-ready monthly panel for the
US Long Sample (June 1957 - December 2016).

  Steps 1-9 run as ClickHouse SQL (src/sql/01..09, intermediate tables in
  write_yeye.qmj_*): Compustat funda fundamentals -> CCM link -> PIT
  universe (shrcd 10/11, non-OTC) -> FF(1992) fiscal alignment (most recent
  fiscal year-end >= 6 months before the month) -> profitability, growth,
  and safety sub-variables -> merge with CRSP monthly returns (delisting
  adjusted) and excess returns.

  Step 8 (this file): monthly cross-sectional rank z-scores and the
  Profitability / Growth / Safety / Quality composites, averaging
  available measures per the paper's missing-data rule. Saves
  data/panel.parquet.

This file builds the data pipeline only. The return analysis is in
separate scripts that read data/panel.parquet:
  * src/table3.py  — Table 3 quality-sorted decile portfolios (Panel A)
  * src/table4.py  — Table 4 QMJ + sub-component factors (Panel A)
  * src/qmj_common.py — shared panel/FF loading, NYSE-breakpoint sorts,
    time-series regression helpers (statsmodels OLS + Newey-West HAC).

Usage:
  uv run python src/main.py [--skip-sql]    # build data/panel.parquet
  uv run python src/table3.py               # results/table_3.md + plots
  uv run python src/table4.py               # results/table_4.md + plot
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# project root on sys.path so `utils` imports resolve
_SRC_FILE = Path(__file__).resolve()
_REPO_ROOT = str(_SRC_FILE.parents[3])
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import numpy as np
import pandas as pd
from clickhouse_driver import Client

from utils.env import get_clickhouse_config
from utils.paths import paper_layout

# --- layout & configuration -------------------------------------------------

# replications root derived from this file's location so the script works
# from any cwd (no reliance on REPLICATIONS_PATH)
LAYOUT = paper_layout("quality_minus_junk",
                      replications_root=_SRC_FILE.parents[2])
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")

RULES = json.loads(LAYOUT.preparations_path("preprocessing_rules.json").read_text())

# Paper parameters (cited rule_ids from preprocessing_rules.json):
#   sample_long_period  — first date June 1957 (L316)
#   sample_end_date     — long sample ends December 2016 (L1878)
#   universe_common_stock / universe_otc_exclusion — shrcd 10/11, drop OTC
#   sample_fiscal_alignment — FF (1992) convention (L314)
#   winsorize_rank_zscore / var_zscore_methodology — rank z-scoring (L350)
#   var_missing_data_averaging — average the remaining measures (L376)
SAMPLE_START = "1957-06-01"   # rule: sample_long_period
SAMPLE_END = "2016-12-01"     # rule: sample_end_date

# Composite constituents (rule ids: var_profitability_composite,
# var_growth_composite, var_safety_composite, var_quality_composite).
# All oriented so that higher = better quality: bab = -beta, lev = -debt/
# assets, oscore = -Ohlson logit come pre-negated from SQL; EVOL (earnings
# volatility) is negated here so higher = safer, matching the paper's
# orientation of every quality measure (flagged for the Replicator).
PROF_VARS = ["gpoa", "roe", "roa", "cfoa", "gmar", "acc"]
GROWTH_VARS = ["d_gpoa", "d_roe", "d_roa", "d_cfoa", "d_gmar"]
SAFETY_VARS = [("bab", "bab"), ("lev", "lev"), ("oscore", "oscore"),
               ("zscore", "zscore"), ("evol", "evol_s")]

DDL_STEPS = [
    "01_funda_base.sql",
    "02_funda_annual.sql",
    "03_ccm_link.sql",
    "04_funda_permno.sql",
    "05_universe_monthly.sql",
    "06_beta_monthly.sql",
    "07_evol_quarterly.sql",
    "08_funda_enriched.sql",
    "09_panel_align.sql",
]
PULL_STEP = "10_panel_pull.sql"

# --- ClickHouse connection ---------------------------------------------------

_CFG = get_clickhouse_config()


def _client() -> Client:
    return Client(
        host=_CFG["host"], port=int(_CFG["port"]),
        user=_CFG["user"], password=_CFG["password"],
        settings={
            "max_execution_time": 1800,
            "max_rows_to_read": 10000000000,
            "timeout_before_checking_execution_speed": 0,
        },
    )


def q(sql: str) -> pd.DataFrame:
    """Execute a SQL query and return a DataFrame."""
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    return q((SQL_DIR / name).read_text())


def run_ddl(name: str) -> None:
    c = _client()
    t0 = time.time()
    c.execute((SQL_DIR / name).read_text())
    print(f"[sql] {name}: {time.time() - t0:.1f}s")


# --- rank z-scoring and composites (Step 8) ----------------------------------


def rank_zscore(panel: pd.DataFrame, col: str, out: str,
                date_col: str = "month") -> pd.DataFrame:
    """Cross-sectional rank z-score per the paper (Appendix 1):
    r_x = rank(x) ascending; z(x) = (r - mu_r)/sigma_r with cross-sectional
    mean/std of the ranks. NaN inputs stay NaN (excluded from the ranks)."""
    g = panel.groupby(date_col)[col]
    r = g.rank(method="average")  # ascending, NaN kept
    tmp = pd.DataFrame({date_col: panel[date_col], "r": r})
    stats = tmp.groupby(date_col)["r"].agg(mu="mean", sd="std", n="count")
    z = (r - stats["mu"].reindex(panel[date_col]).values) / \
        stats["sd"].reindex(panel[date_col]).values
    panel[out] = np.where(stats["n"].reindex(panel[date_col]).values >= 2,
                          z, np.nan)
    return panel


def composite(panel: pd.DataFrame, zcols: list[str], out: str,
              date_col: str = "month") -> pd.DataFrame:
    """Average the available z-scores (paper's missing-data rule), then
    z-score the average cross-sectionally."""
    avg = panel[zcols].mean(axis=1, skipna=True)  # all-NaN row -> NaN
    panel[out + "_raw"] = avg
    panel[f"n_{out}"] = panel[zcols].notna().sum(axis=1)
    return rank_zscore(panel, out + "_raw", out, date_col=date_col)


def build_quality(panel: pd.DataFrame) -> pd.DataFrame:
    """Step 8: rank z-scores + Profitability/Growth/Safety/Quality."""
    # EVOL sign: higher volatility = lower quality -> negate so that the
    # safety composite is consistently "higher = safer" (paper orients
    # every quality measure this way; bab/lev/oscore arrive pre-negated).
    panel["evol_s"] = -panel["evol"]

    all_vars = [(v, v) for v in PROF_VARS + GROWTH_VARS] + SAFETY_VARS
    for src, name in all_vars:
        panel = rank_zscore(panel, src, f"z_{name}")

    z_prof = [f"z_{v}" for v in PROF_VARS]
    z_grow = [f"z_{v}" for v in GROWTH_VARS]
    z_safe = [f"z_{name}" for _, name in SAFETY_VARS]

    panel = composite(panel, z_prof, "profitability")
    panel = composite(panel, z_grow, "growth")
    panel = composite(panel, z_safe, "safety")
    panel = composite(panel, ["profitability", "growth", "safety"], "quality")
    return panel


# --- main ---------------------------------------------------------------------


def main() -> None:
    skip_sql = "--skip-sql" in sys.argv

    # Steps 1-9: ClickHouse SQL pipeline
    if not skip_sql:
        for step in DDL_STEPS:
            run_ddl(step)

    # Pull the merged panel
    t0 = time.time()
    panel = q_file(PULL_STEP)
    print(f"[sql] {PULL_STEP}: pull {len(panel):,} rows in {time.time() - t0:.1f}s")

    panel["month"] = pd.to_datetime(panel["month"])
    panel["datadate"] = pd.to_datetime(panel["datadate"])
    panel = panel[(panel["month"] >= SAMPLE_START) &
                  (panel["month"] <= SAMPLE_END)].copy()
    panel = panel.sort_values(["permno", "month"]).reset_index(drop=True)

    # Step 8: rank z-scores and composites
    panel = build_quality(panel)

    # Order columns: identifiers, scores, sub-variables, diagnostics
    score_cols = ["quality", "profitability", "growth", "safety"]
    zcols = [c for c in panel.columns if c.startswith("z_")]
    raw_cols = PROF_VARS + GROWTH_VARS + ["lev", "oscore", "zscore",
                                          "evol", "evol_s", "beta", "bab"]
    diag_cols = ["n_profitability", "n_growth", "n_safety", "n_quality",
                 "datadate", "fyear", "hexcd_eom", "beta", "at", "be",
                 "me_m", "mcap", "ret", "rf", "ret_excess", "ret_next"]
    keep = (["permno", "month"] + score_cols + zcols +
            [c for c in raw_cols if c not in zcols] + diag_cols)
    panel = panel[[c for c in dict.fromkeys(keep) if c in panel.columns]]

    out = LAYOUT.data_path("panel.parquet")
    panel.to_parquet(out, index=False)
    print(f"[save] {out}")

    report(panel)


def report(panel: pd.DataFrame) -> None:
    q_ = panel["quality"].dropna()
    obs = panel.groupby("month").size()
    obs_q = panel.dropna(subset=["quality"]).groupby("month").size()
    print("\n" + "=" * 64)
    print("PANEL REPORT")
    print("=" * 64)
    print(f"rows x columns:      {panel.shape[0]:,} x {panel.shape[1]}")
    print(f"unique months:       {panel['month'].nunique()} "
          f"({panel['month'].min().date()} .. {panel['month'].max().date()})")
    print(f"unique permnos:      {panel['permno'].nunique():,}")
    print(f"avg obs/month:       {obs.mean():.0f} "
          f"(with non-NaN quality: {obs_q.mean():.0f})")
    print(f"quality: n={len(q_):,} mean={q_.mean():.4f} "
          f"median={q_.median():.4f} std={q_.std():.4f}")
    print("\nvariable coverage (non-NaN rows / %):")
    for col in PROF_VARS + GROWTH_VARS + ["bab", "lev", "oscore", "zscore",
                                          "evol", "quality", "ret_next",
                                          "mcap"]:
        n = panel[col].notna().sum()
        print(f"  {col:<10} {n:>10,}  {n / len(panel) * 100:5.1f}%")
    print("\ncomposite summary stats:")
    print(panel[["quality", "profitability", "growth", "safety"]]
          .describe().loc[["mean", "50%", "std", "count"]].round(4))


if __name__ == "__main__":
    main()
