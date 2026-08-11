"""
Replication of Fairfield, Whisenant & Yohn (2003)
"Accrued Earnings and Growth: Implications for Earnings Persistence
and Market Mispricing" (FWY)

This Stage 7 inner-iteration builds the firm-year panel (data/panel.parquet)
that downstream Stages 7-8 (descriptive statistics Table 1; decile sorts
Table 2; correlation matrix Table 3; regressions eqs. 1-6; Mishkin test
Table 7) will operate on.

Pipeline (SQL-driven, Python only for plumbing):
    src/sql/comp_funda_filter.sql   -- universe + footnote filter (audit breakout)
    src/sql/comp_accounting_vars.sql -- self-joins + WC changes (audit breakout)
    src/sql/comp_panel_3yr.sql      -- 3-year-panel non-null gate (audit breakout)
    src/sql/panel.sql               -- final assembly with all deflated ratios
                                     (includes the CRSP-coverage gate for
                                     "sufficient stock price data", paper L187)

Targets (paper Table 1 footnote, L687): 33,080 firm-years.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from clickhouse_driver import Client
from utils.env import get_clickhouse_config, get_replications_path
from utils.paths import paper_layout


# --- configuration (read from the per-replication layout) ---------------
LAYOUT = paper_layout("fairfield_v2").ensure()
SQL_DIR = LAYOUT.src_path("sql")

_CFG = get_clickhouse_config()


# --- ClickHouse connection ----------------------------------------------
def _client() -> Client:
    return Client(
        host=_CFG["host"],
        port=int(_CFG["port"]),
        user=_CFG["user"],
        password=_CFG["password"],
        database="default",  # use fully-qualified table refs
        settings={"max_execution_time": 600},
    )


def q(sql: str) -> pd.DataFrame:
    """Execute a SQL query (string) and return a DataFrame.
    Uses native clickhouse_driver; returns proper Python None for NULL.
    """
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    """Execute a saved SQL file from src/sql/."""
    sql = (SQL_DIR / name).read_text()
    return q(sql)


# --- data loading -------------------------------------------------------
def build_panel() -> pd.DataFrame:
    """Build the analysis-ready firm-year panel from the SQL pipeline."""
    df = q_file("panel.sql")
    # ClickHouse keeps the table-prefix alias in the column name
    # (e.g. "f.gvkey", "f.fyear"). Rename them to clean identifiers
    # so downstream analyses can write `df["gvkey"]` without escaping.
    df = df.rename(columns=lambda c: c.split(".", 1)[-1] if "." in c else c)
    return df


def _ratio_summary(s: pd.Series) -> str:
    """Compact 5-number summary for a deflated-ratio column."""
    if s.dropna().empty:
        return "(no non-null observations)"
    qs = s.quantile([0.25, 0.5, 0.75])
    return (
        f"mean={s.mean(): .4f}  std={s.std(): .4f}  "
        f"min={s.min(): .4f}  q1={qs.loc[0.25]: .4f}  "
        f"median={qs.loc[0.5]: .4f}  q3={qs.loc[0.75]: .4f}  "
        f"max={s.max(): .4f}  N={int(s.notna().sum()):,}"
    )


def summarize(panel: pd.DataFrame) -> None:
    """Print a coverage / sanity summary used in the worker's report."""
    # ---- panel shape
    print(f"\n=== PANEL SHAPE ===")
    print(f"panel_n_rows     = {len(panel):,}   (target ~33,080, ±5,000)")
    print(f"panel_n_columns  = {panel.shape[1]}")
    print(f"unique gvkey     = {panel['gvkey'].nunique():,}")
    print(f"fyear range      = {panel['fyear'].min()} .. {panel['fyear'].max()}")

    # ---- coverage by fyear
    cov = panel.groupby("fyear").size().reset_index(name="n")
    print(f"\n=== COVERAGE BY FYEAR ===")
    print(cov.to_string(index=False))

    # ---- deflated-ratio summary stats (paper Table 1, L607-687)
    print(f"\n=== DEFLATED-RATIO SUMMARIES ===")
    print(f"Paper targets: ROA_t mean~0.116 std~0.117; ACC_t mean~-0.019 std~0.103;"
          f" GrNOA_t mean~0.072; GrLTNOA_t mean~0.091.")
    for col in ["roa_t", "acc_t", "cfo_t", "grnoa_t", "grltnoa_t",
                "grwc_t", "roa_t_plus_1", "opinc_t_plus_1_per_lag_def"]:
        if col in panel.columns:
            print(f"  {col:<28} {_ratio_summary(panel[col])}")

    # ---- paper-quoted anchor: rows with min ROA_t > -1
    min_roa = panel["roa_t"].min()
    print(f"\n=== CONTAMINATION CHECK ===")
    print(f"min(ROA_t) = {min_roa:.4f}   (paper's CRSP coverage would have"
          f" removed the -67.3 outlier seen in iter 1)")
    print(f"rows with ROA_t > -1: {(panel['roa_t'] > -1).sum():,}"
          f" of {len(panel):,} ({100 * (panel['roa_t'] > -1).mean():.1f}%)")

    # ---- non-null gates
    required = ["acc_t", "grltnoa_t", "roa_t", "roa_t_plus_1", "opinc_t_plus_1_per_lag_def"]
    avail = panel[required].notna().all(axis=1).sum()
    print(f"\nrows with all of {required} non-null: {avail:,}")
    inferred_cols = ["at_t", "oiadp_t", "oa_t", "ol_t", "noa_t",
                     "roa_t_plus_1", "opinc_t_plus_1_per_lag_def"]
    strict = panel[inferred_cols].notna().all(axis=1).sum()
    print(f"rows with all of {inferred_cols} non-null (t, t+1): {strict:,}")

    # ---- Rule 4 sanity check: IBM gvkey='006066' for fyear=1985
    print(f"\n=== SANITY CHECK (IBM gvkey='006066', fyear=1985) ===")
    ibm = panel[(panel["gvkey"] == "006066") & (panel["fyear"] == 1985)]
    if len(ibm) == 1:
        r = ibm.iloc[0]
        print(f"  roa_t              = {r['roa_t']:.4f}")
        print(f"  acc_t              = {r['acc_t']:.4f}")
        print(f"  cfo_t              = {r['cfo_t']:.4f}")
        print(f"  grnoa_t            = {r['grnoa_t']:.4f}")
        print(f"  grltnoa_t          = {r['grltnoa_t']:.4f}")
        print(f"  roa_t_plus_1       = {r['roa_t_plus_1']:.4f}")
        print(f"  at_t               = {r['at_t']:.2f}  (millions $)")
        print(f"  oiadp_t            = {r['oiadp_t']:.2f}  (millions $)")
        print(f"  roa_t * avg_ta_t ~= oiadp_t? {r['roa_t'] * (r['at_t'] / 2 + r['at_t'] / 2):.2f}")
    elif len(ibm) == 0:
        print("  (no row for IBM 1985 -- either gvkey differs or the row was"
              " dropped by some filter)")
    else:
        print(f"  (unexpected: {len(ibm)} rows for IBM 1985)")


# --- main ---------------------------------------------------------------
def main() -> None:
    panel = build_panel()
    panel.to_parquet(LAYOUT.data_path("panel.parquet"), index=False)
    print(f"Wrote panel.parquet: {panel.shape[0]:,} rows x {panel.shape[1]} cols")
    summarize(panel)


if __name__ == "__main__":
    main()