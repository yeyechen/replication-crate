"""
Enrich the panel with NYSE/exchcd flags and the micro-cap dummy.

Steps:
1. Load universe_monthly.parquet (has nyse, exchcd) and merge onto the panel
   via (permno, month) — the panel is a subset of the universe (only firms
   with a gvkey/Compustat link survive).
2. Compute the micro-cap flag at each June Y:
   - For each June Y, compute the 20th percentile of size restricted to
     NYSE-only stocks (nyse=1).
   - micro = 1 if size < 20th percentile at that June.
   - The same micro status is used for the 12-month holding period
     (July Y to June Y+1).

The "size" used for the micro-cap definition is the snapshot size at June Y
= log(ME at June Y). The panel's `size` column is log(ME_lag1) which is
lagged by 1 month; we use log(me_dollars) instead so the micro-cap matches
the paper's "size at the June sort date" definition.

Outputs:
    data/panel_enriched.parquet — the panel with nyse, exchcd, micro_cap
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from utils.env import load_project_env
from utils.paths import paper_layout


load_project_env()
LAYOUT = paper_layout("belo_lin_bazdresch_2014_labor_hiring_investment_and_stock_return_predictability")
LAYOUT.ensure()


def enrich_panel() -> pd.DataFrame:
    """Load panel + universe, merge flags, compute micro-cap, save."""
    print("Loading panel.parquet ...")
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    print(f"  panel: {len(panel):,} rows, {panel['permno'].nunique():,} permnos")

    print("Loading universe_monthly.parquet ...")
    uni = pd.read_parquet(LAYOUT.data_path("universe_monthly.parquet"))
    print(f"  universe: {len(uni):,} rows")

    # 1. Merge nyse and exchcd onto the panel.
    # The panel is a strict subset of the universe (panel = universe ∩ Compustat).
    # Inner join on (permno, month) means we KEEP only panel rows; the panel's
    # row coverage is preserved.
    print("Merging nyse + exchcd from universe ...")
    panel["month"] = pd.to_datetime(panel["month"])
    uni["month"] = pd.to_datetime(uni["month"])
    panel = panel.merge(
        uni[["permno", "month", "nyse", "exchcd"]].drop_duplicates(["permno", "month"]),
        on=["permno", "month"], how="left",
    )
    # Diagnostic: ensure no missing nyse/exchcd
    miss = panel["nyse"].isna().sum()
    if miss > 0:
        print(f"  WARNING: {miss:,} panel rows have missing nyse/exchcd after merge "
              f"(out of {len(panel):,}); filling with 0")
        panel["nyse"] = panel["nyse"].fillna(0).astype("int64")
        panel["exchcd"] = panel["exchcd"].fillna(0).astype("int64")
    else:
        panel["nyse"] = panel["nyse"].astype("int64")
        panel["exchcd"] = panel["exchcd"].astype("int64")
    print(f"  NYSE=1: {panel['nyse'].sum():,}  NYSE=0: {(panel['nyse']==0).sum():,}")

    # 2. Compute the snapshot size at June Y = log(me_dollars / 1e6).
    # The paper's Table 2 reports Size in units of log(ME in $millions).
    # The panel's `me_dollars` is in USD; dividing by 1e6 gives $millions.
    # The panel's `size` column is log(ME_lag1) = log(ME at May Y), which is
    # NOT the snapshot size at June Y. We compute size_snapshot using current
    # ME at June Y (the snapshot date), expressed in $millions.
    panel["size_snapshot"] = np.log(panel["me_dollars"].clip(lower=1.0) / 1e6)

    # 3. Compute micro-cap flag at each June.
    # Strategy: for each June Y, compute the 20th percentile of size_snapshot
    # restricted to NYSE=1. Then mark all stocks at June Y as micro=1 if their
    # size_snapshot < 20th percentile. Propagate micro to all months from
    # July Y to June Y+1.
    panel["month_dt"] = panel["month"]
    panel["is_june"] = panel["month_dt"].dt.month == 6
    panel["year"] = panel["month_dt"].dt.year

    # Compute NYSE 20th percentile of size_snapshot at each June
    june_nyse = panel[panel["is_june"] & (panel["nyse"] == 1)]
    june_breaks = (
        june_nyse.groupby("year")["size_snapshot"]
        .quantile(0.20)
        .rename("size_june_p20")
        .reset_index()
    )
    print(f"  June NYSE 20th pct coverage: {len(june_breaks)} years "
          f"({june_breaks['year'].min()}-{june_breaks['year'].max()})")

    # Join breakpoints to all June rows (regardless of NYSE status)
    june_rows = panel[panel["is_june"]].merge(june_breaks, on="year", how="left")
    june_rows["micro"] = (june_rows["size_snapshot"] < june_rows["size_june_p20"]).astype("int64")
    snap_micro = june_rows[["permno", "year", "micro"]].copy()
    snap_micro = snap_micro.rename(columns={"year": "snap_year"})
    print(f"  micro=1 fraction at June: {snap_micro['micro'].mean():.3f}")

    # 4. Propagate micro to all months in the holding year.
    # Holding year Y = July Y to June Y+1.
    # micro flag at June Y is the holding year Y+1... wait.
    # The paper's micro flag at sort date June Y is for the holding year
    # July Y to June Y+1. The snap_year is the sort year.
    # We propagate so that each month m in holding year Y
    # (July Y to June Y+1) gets the micro flag from sort year Y.
    # sort year Y -> snap['year'] = Y -> holding year [July Y, June Y+1]
    # So for each row, if its calendar year is Y, it belongs to holding year Y
    # (Jan-Jun) or Y-1 (Jul-Dec). Let's compute the holding year.
    # holding_year = (July Y..June Y+1) -> July Y has year=Y, June Y+1 has year=Y+1.
    # So for a row with month=m (calendar year=CY):
    #   if month >= July (m.month >= 7): holding_year = CY
    #   else: holding_year = CY - 1 ... wait no.
    # Row at July 2000: holding year = 2000 (held since July 2000).
    # Row at December 2000: holding year = 2000.
    # Row at January 2001: holding year = 2001? No — it's still in the holding
    # period that started July 2000. So holding year = 2000.
    # Row at June 2001: holding year = 2000.
    # General: for month m,
    #   if m.month >= 7: holding_year = m.year
    #   else: holding_year = m.year  (Jan-Jun are still in the holding year
    #                                  that started July of the previous year)
    # Wait, that's wrong. Let me think again.
    # Holding year 2000 = July 2000 to June 2001.
    # Row at July 2000: belongs to holding year 2000.
    # Row at December 2000: belongs to holding year 2000.
    # Row at January 2001: belongs to holding year 2000.
    # Row at June 2001: belongs to holding year 2000.
    # Row at July 2001: belongs to holding year 2001.
    # So: for month m, holding_year = (m.year if m.month >= 7 else m.year-1)
    # Wait no:
    #   July 2000 -> m.month=7, m.year=2000 -> holding_year = 2000
    #   Dec 2000 -> m.month=12, m.year=2000 -> holding_year = 2000
    #   Jan 2001 -> m.month=1, m.year=2001 -> holding_year = 2000
    #   June 2001 -> m.month=6, m.year=2001 -> holding_year = 2000
    # So holding_year = m.year if m.month >= 7, else m.year - 1.
    # Hmm, but the spec says "the same micro status is used for the 12 months
    # of the holding period (July t to June t+1)". So for the holding year Y,
    # the micro status is from the sort at June Y.
    # Our snap_micro has snapshot_year = Y (the year of the June snapshot).
    # A row with month = July Y has holding_year = Y.
    # So we want: panel.holding_year = panel.snap_micro.snapshot_year
    # where snapshot_year = Y for sort at June Y.

    # Compute panel's holding year (the year "Y" of the "July Y to June Y+1" period).
    panel["hold_yr"] = np.where(
        panel["month_dt"].dt.month >= 7,
        panel["year"],
        panel["year"] - 1,
    )
    # The first month of the sample is July 1965, which has hold_yr = 1965.
    # The last month is June 2010, which has hold_yr = 2009.
    # We have snapshot years from 1965 to 2010 (45 years of June rows).
    # Snapshot at June Y -> micro for holding year Y.
    # So we need to merge panel with snap_micro on (permno, hold_yr = snap_year).
    snap_micro = snap_micro.rename(columns={"snap_year": "hold_yr"})
    panel = panel.merge(
        snap_micro[["permno", "hold_yr", "micro"]],
        on=["permno", "hold_yr"],
        how="left",
    )
    # For the first holding year (1965), panel may have no snap (June 1965 had
    # no prior June to define micro). For months outside the holding year
    # range (e.g., July 2009 to June 2010 is the last holding year, with snap
    # at June 2009), the merge should still work as long as we have June 2009.
    panel["micro"] = panel["micro"].fillna(0).astype("int64")
    print(f"  micro distribution (panel rows): "
          f"micro=1: {panel['micro'].sum():,}  micro=0: {(panel['micro']==0).sum():,}")

    # Cleanup
    panel = panel.drop(columns=["month_dt", "is_june", "year", "hold_yr"])
    panel["month"] = panel["month"].astype(str)  # restore string for parquet

    out = LAYOUT.data_path("panel_enriched.parquet")
    panel.to_parquet(out, index=False)
    print(f"Wrote {out} ({len(panel):,} rows, {panel.shape[1]} cols)")
    return panel


if __name__ == "__main__":
    enrich_panel()
