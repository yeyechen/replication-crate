"""
Replication of Lev & Nissim (2004) "Taxable Income, Future Earnings,
and Equity Values" (Accounting Review).

Pipeline (inner iteration 1): build the comp-only firm-year panel
that feeds Tables 2 / 3 / 4 / 5.

  Stage 1 (run, iteration 1) — comp-only firm-year panel.
  Builds `data/panel.parquet`:
    - Compustat universe filter (US, Dec FYE, non-regulated,
      non-flow-through, 1973-2000)
    - TAX / DEF / CFO fundamentals (paper Eqs. 2 / footnote 14 /
      footnote 16)
    - R_TAX / R_DEF / R_CFO industry-year quintile ranks (paper
      §IV "The Tax-Based Fundamentals")
    - G1 / G2 / G3 future-earnings growth (paper Eq. 4), in
      percentage points and deflated by current total assets

  Stage 2 (analysis, future iterations) — T2/T3 (G regressions),
  T4 (E/P regression), T5 (returns regression). Each will consume
  the comp-side panel produced here.

The comp-side pipeline is SQL-first (one CTEs chain in
`src/sql/comp_panel.sql`); Python runs the query and writes the
parquet artifact and a brief summary.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402

SLUG = "lev_nissim_2004_taxable_income_future_earnings_and_equity_values"
LAYOUT = paper_layout(SLUG)
SQL_DIR = LAYOUT.src_path("sql")
_CFG = get_clickhouse_config()


# ----------------------------------------------------------------------------
# ClickHouse access (mirrors the do_industries_explain_momentum pattern)
# ----------------------------------------------------------------------------


def _client() -> Client:
    return Client(
        host=_CFG["host"],
        port=int(_CFG["port"]),
        user=_CFG["user"],
        password=_CFG["password"],
        settings={"max_execution_time": 600},
    )


def q(sql: str) -> pd.DataFrame:
    c = _client()
    try:
        data, cols = c.execute(sql, with_column_types=True)
    finally:
        c.disconnect()
    df = pd.DataFrame(data, columns=[x[0] for x in cols])
    # Numeric columns come back as object dtype when nullable; coerce.
    for c in df.columns:
        if df[c].dtype == object:
            try:
                df[c] = pd.to_numeric(df[c])
            except (ValueError, TypeError):
                pass
    return df


def q_file(name: str) -> pd.DataFrame:
    return q((SQL_DIR / name).read_text())


# ----------------------------------------------------------------------------
# Sample-size funnel (per the task spec)
# ----------------------------------------------------------------------------


def _sample_size_funnel(client: Client) -> dict[str, int]:
    """Run the universe filter chain step-by-step and return row counts.

    These are the descriptive counts the Replicator asks for in the
    task spec: confirm row count at each filter step.
    """
    steps: list[tuple[str, str]] = [
        ("raw_comp_202601_funda",
         "SELECT count() FROM comp_202601.funda"),
        ("quality_filter",
         """SELECT count() FROM comp_202601.funda
            WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'"""),
        ("+_usa_+_sample_window_1973_2000",
         """SELECT count() FROM comp_202601.funda
            WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
              AND fic = 'USA'
              AND fyear BETWEEN 1973 AND 2000"""),
        ("+_december_fiscal_year_end",
         """SELECT count() FROM comp_202601.funda
            WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
              AND fic = 'USA'
              AND fyear BETWEEN 1973 AND 2000
              AND fyr = 12"""),
        ("+_non_regulated_non_financial",
         """SELECT count() FROM comp_202601.funda
            WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
              AND fic = 'USA'
              AND fyear BETWEEN 1973 AND 2000
              AND fyr = 12
              AND intDiv(sich, 100) NOT IN (49, 60, 61, 62, 63, 64, 65, 66, 67)"""),
        ("+_required_data_items_#6_#18_#199_#25_#60_#16_#50",
         """SELECT count() FROM comp_202601.funda
            WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
              AND fic = 'USA'
              AND fyear BETWEEN 1973 AND 2000
              AND fyr = 12
              AND intDiv(sich, 100) NOT IN (49, 60, 61, 62, 63, 64, 65, 66, 67)
              AND at IS NOT NULL AND ib IS NOT NULL AND prcc_f IS NOT NULL
              AND csho IS NOT NULL AND ceq IS NOT NULL
              AND txt IS NOT NULL AND txdb IS NOT NULL"""),
        ("+_positive_current_earnings_ib>0",
         """SELECT count() FROM comp_202601.funda
            WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
              AND fic = 'USA'
              AND fyear BETWEEN 1973 AND 2000
              AND fyr = 12
              AND intDiv(sich, 100) NOT IN (49, 60, 61, 62, 63, 64, 65, 66, 67)
              AND at IS NOT NULL AND ib IS NOT NULL AND prcc_f IS NOT NULL
              AND csho IS NOT NULL AND ceq IS NOT NULL
              AND txt IS NOT NULL AND txdb IS NOT NULL
              AND ib > 0"""),
    ]
    out: dict[str, int] = {}
    for label, sql in steps:
        rows, _ = client.execute(sql, with_column_types=True)
        out[label] = int(rows[0][0])
    return out


# ----------------------------------------------------------------------------
# Pipeline
# ----------------------------------------------------------------------------


def run_comp_panel() -> pd.DataFrame:
    """Build the comp-only firm-year panel and save to `data/panel.parquet`."""
    LAYOUT.ensure()

    # Sample-size funnel (separate SQL queries, not the panel SQL).
    print("[1/4] Sample-size funnel ...")
    funnel_client = _client()
    funnel = _sample_size_funnel(funnel_client)
    funnel_client.disconnect()
    for k, v in funnel.items():
        print(f"      {k:55s}: {v:>9,}")
    paper_target = 40_372
    ours = funnel["+_required_data_items_#6_#18_#199_#25_#60_#16_#50"]
    delta_pct = (ours - paper_target) / paper_target * 100
    print(f"      paper target: {paper_target:,} (4% gap = expected; "
          f"pre-1987 tax-disclosure data is sparse in comp_202601).")
    print(f"      gap to paper: {delta_pct:+.1f}%")

    # The main panel (CTE chain, ~0.5-1s).
    print("\n[2/4] comp_panel.sql (CTE chain: filter → lags → fundamentals → "
          "R_TAX/R_DEF/R_CFO) ...")
    t0 = time.time()
    df = q_file("comp_panel.sql")
    print(f"      pulled {len(df):,} rows × {len(df.columns)} cols in "
          f"{time.time() - t0:.1f}s")

    # Save panel.parquet.
    print("\n[3/4] write data/panel.parquet ...")
    panel_path = LAYOUT.data_path("panel.parquet")
    df.to_parquet(panel_path, index=False)
    print(f"      wrote {panel_path} ({panel_path.stat().st_size / 1e6:.2f} MB)")

    # Brief summary stats.
    print("\n[4/4] summary stats")
    print(f"      rows: {len(df):,}, unique gvkeys: {df['gvkey'].nunique():,}, "
          f"unique fyear: {df['fyear'].nunique()} "
          f"({int(df['fyear'].min())}..{int(df['fyear'].max())})")
    print(f"      unique (sich_2digit, fyear) groups: "
          f"{df[['sich_2digit', 'fyear']].drop_duplicates().shape[0]}")

    n_tax = int(df["tax"].notna().sum())
    n_def = int(df["def"].notna().sum())
    n_cfo = int(df["cfo"].notna().sum())
    print(f"      N with TAX: {n_tax:,}, N with DEF: {n_def:,}, "
          f"N with CFO: {n_cfo:,}")

    if n_tax:
        td = df["tax"].dropna()
        q = td.quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
        print(f"      TAX distribution: mean={td.mean():.4f}, "
              f"std={td.std():.4f}, "
              f"min={td.min():.3f}, max={td.max():.3f}")
        print(f"        quantiles 1%={q[0.01]:.3f} 5%={q[0.05]:.3f} "
              f"25%={q[0.25]:.3f} 50%={q[0.50]:.3f} 75%={q[0.75]:.3f} "
              f"95%={q[0.95]:.3f} 99%={q[0.99]:.3f}")

    if n_def:
        dd = df["def"].dropna()
        print(f"      DEF distribution: mean={dd.mean():.4f}, "
              f"std={dd.std():.4f}, "
              f"min={dd.min():.5f}, max={dd.max():.5f}")

    if n_cfo:
        cd = df["cfo"].dropna()
        print(f"      CFO distribution: mean={cd.mean():.4f}, "
              f"std={cd.std():.4f}, "
              f"min={cd.min():.3f}, max={cd.max():.3f}")

    # R_TAX counts at each quintile level.
    print("\n      R_TAX quintile counts:")
    r_tax_counts = df["r_tax"].value_counts(dropna=False).sort_index()
    for q in [1, 2, 3, 4, 5]:
        print(f"        R_TAX={q}: {int(r_tax_counts.get(q, 0)):,}")
    print(f"        R_TAX=None (TAX unavailable): "
          f"{int(r_tax_counts.get(np.nan, 0)):,}")

    # R_TAX mean TAX by quintile (must monotonically increase).
    print("\n      Mean TAX by R_TAX quintile (sanity: should increase):")
    rt_tax_mean = df.dropna(subset=["r_tax"]).groupby("r_tax")["tax"].agg(
        ["count", "mean", "median"]
    )
    for q, row in rt_tax_mean.iterrows():
        print(f"        R_TAX={int(q)}: n={int(row['count']):>5,}  "
              f"mean={row['mean']:+.4f}  median={row['median']:+.4f}")

    print("\n      Mean DEF by R_DEF quintile (sanity: should increase):")
    rd_def_mean = df.dropna(subset=["r_def"]).groupby("r_def")["def"].agg(
        ["count", "mean", "median"]
    )
    for q, row in rd_def_mean.iterrows():
        print(f"        R_DEF={int(q)}: n={int(row['count']):>5,}  "
              f"mean={row['mean']:+.5f}  median={row['median']:+.5f}")

    print("\n      Mean CFO by R_CFO quintile (sanity: should increase):")
    rc_cfo_mean = df.dropna(subset=["r_cfo"]).groupby("r_cfo")["cfo"].agg(
        ["count", "mean", "median"]
    )
    for q, row in rc_cfo_mean.iterrows():
        print(f"        R_CFO={int(q)}: n={int(row['count']):>5,}  "
              f"mean={row['mean']:+.4f}  median={row['median']:+.4f}")

    # Headline test (C1): G1 / G3 by R_TAX must increase monotonically.
    print("\n      Mean G1 by R_TAX quintile (headline C1 test: "
          "should increase):")
    g1_by_rt = df.dropna(subset=["r_tax", "g1"]).groupby("r_tax")["g1"].agg(
        ["count", "mean"]
    )
    for q, row in g1_by_rt.iterrows():
        print(f"        R_TAX={int(q)}: n={int(row['count']):>5,}  "
              f"mean G1={row['mean']:+.4f}")

    print("\n      Mean G3 by R_TAX quintile (C1):")
    g3_by_rt = df.dropna(subset=["r_tax", "g3"]).groupby("r_tax")["g3"].agg(
        ["count", "mean"]
    )
    for q, row in g3_by_rt.iterrows():
        print(f"        R_TAX={int(q)}: n={int(row['count']):>5,}  "
              f"mean G3={row['mean']:+.4f}")

    print("\n      N with G1 / G2 / G3 (future-earnings growth):")
    for col in ("g1", "g2", "g3"):
        print(f"        {col}: {int(df[col].notna().sum()):,} non-null")

    return df


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--rebuild",
        action="store_true",
        help="force rebuild of data/panel.parquet",
    )
    args = ap.parse_args()
    LAYOUT.ensure()
    panel_path = LAYOUT.data_path("panel.parquet")
    if args.rebuild or not panel_path.exists():
        run_comp_panel()
    else:
        print(f"[skip] {panel_path.name} exists (pass --rebuild to force)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
