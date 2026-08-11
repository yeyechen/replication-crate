"""
Replication of Balakrishnan, Bartov, Faurel (2009)
"Post Loss/Profit Announcement Drift"
Table 1 (Sample Selection).

The paper documents a market under-reaction to quarterly earnings
announcements, with a 21% annualized long-short return spread between
extreme-loss and extreme-profit portfolios. Table 1 reports the
firm-quarter and distinct-firm counts at successive sample-selection
stages:

  Primary (Compustat+CRSP merge):
    a) All firm-quarters with ibq/atq/rdq non-missing
    b) After price > $1 five days prior to rdq

  Supplementary (additional data requirements, applied on top of b):
    c) SUE — epspxq non-missing at q and q-12
    d) BM  — ceqq, cshoq, prccq non-missing at q
    e) Accruals — ibq, oancfy, xidocy non-missing at q, atq non-missing
       at q and q-1, AND rdq >= 1988-01-01

Pipeline:
  src/sql/comp_fundamentals.sql — base Compustat pull
  src/sql/ccm_link.sql          — fundq + CCM linktable PIT join
  src/sql/panel.sql             — final panel (with price 5d prior +
                                  q-12 / q-1 self-joins)

Output:
  data/panel.parquet            — analysis-ready firm-quarter panel
  results/table_1.md            — replicated Table 1 (counts only)

Iteration: 1 (Table 1 sample selection only). Table 2 (BHAR by
earnings decile) is the next iteration.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402

SLUG = "balakrishnan_v2"
LAYOUT = paper_layout(SLUG)
SQL_DIR = LAYOUT.src_path("sql")
_CFG = get_clickhouse_config()

# Sample window (from preprocessing_rules.json + paper §2.1):
PANEL_START = "1976-01-01"
PANEL_END = "2005-12-31"
ACCRUALS_START = "1988-01-01"  # cash-flow data starts in 1988
PRICE_FILTER = 1.0  # $1 floor on price 5 trading days prior to rdq

# Paper targets (from preparations/tables_to_replicate.json, ±2%):
TARGETS = {
    "primary_all_firmqtrs":           471_997,
    "primary_all_distinct_firms":      15_261,
    "primary_after_price1_firmqtrs":  458_693,
    "primary_after_price1_firms":      15_143,
    "supp1_sue_firmqtrs":             359_909,
    "supp1_sue_distinct_firms":        12_824,
    "supp2_bm_firmqtrs":              448_500,
    "supp2_bm_distinct_firms":         15_101,
    "supp3_accruals_firmqtrs":        267_416,
    "supp3_accruals_distinct_firms":   10_695,
}
TOLERANCE_PCT = 2.0


# ----------------------------------------------------------------------------
# ClickHouse access
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
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    return q((SQL_DIR / name).read_text())


# ----------------------------------------------------------------------------
# Sample selection
# ----------------------------------------------------------------------------


def _price_filter_pass(df: pd.DataFrame) -> pd.Series:
    """Return a boolean Series: True when the 5-trading-day-prior price
    is available and strictly > $1.

    Drops rows where prc_5d_prior is NULL (no trading day in the 14-day
    look-back window), which is a stricter filter than the paper text
    but consistent with "stock price five days prior to the quarterly
    earnings announcement date above $1" — a firm-quarter with no
    available prior price fails the filter by construction.
    """
    return df["prc_5d_prior"].notna() & (df["prc_5d_prior"] > PRICE_FILTER)


def _sue_eligible(df: pd.DataFrame) -> pd.Series:
    """SUE supplementary: epspxq non-missing at q AND at q-12.

    Simplifying assumption (per task spec): we require epspxq at q
    AND at q-12, rather than all 13 consecutive quarters. The paper's
    SUE computation requires 13 consecutive quarters of epspxxq;
    see preparations/assumptions.md for the gap this introduces.
    """
    return df["epspxq"].notna() & df["epspxq_q12"].notna()


def _bm_eligible(df: pd.DataFrame) -> pd.Series:
    """BM supplementary: ceqq, cshoq, prccq non-missing at q."""
    return (
        df["ceqq"].notna()
        & df["cshoq"].notna()
        & df["prccq"].notna()
    )


def _accruals_eligible(df: pd.DataFrame) -> pd.Series:
    """Accruals supplementary: ibq, oancfy, xidocy at q; atq at q AND q-1;
    rdq >= 1988-01-01."""
    rdq_ok = pd.to_datetime(df["rdq"]) >= pd.Timestamp(ACCRUALS_START)
    return (
        df["ibq"].notna()
        & df["oancfy"].notna()
        & df["xidocy"].notna()
        & df["atq"].notna()
        & df["atq_q1"].notna()
        & rdq_ok
    )


# ----------------------------------------------------------------------------
# Stage counts
# ----------------------------------------------------------------------------


def stage_counts(df: pd.DataFrame) -> dict[str, tuple[int, int]]:
    """Return per-stage (firm_quarters, distinct_gvkeys) for each
    filter stage, matching Table 1 columns.
    """
    primary = df.copy()
    primary_n = len(primary)
    primary_firms = int(primary["gvkey"].nunique())

    after_price = primary[_price_filter_pass(primary)]
    price_n = len(after_price)
    price_firms = int(after_price["gvkey"].nunique())

    sue = after_price[_sue_eligible(after_price)]
    sue_n = len(sue)
    sue_firms = int(sue["gvkey"].nunique())

    bm = after_price[_bm_eligible(after_price)]
    bm_n = len(bm)
    bm_firms = int(bm["gvkey"].nunique())

    accr = after_price[_accruals_eligible(after_price)]
    accr_n = len(accr)
    accr_firms = int(accr["gvkey"].nunique())

    return {
        "primary_all":          (primary_n, primary_firms),
        "primary_after_price1": (price_n, price_firms),
        "supp1_sue":            (sue_n, sue_firms),
        "supp2_bm":             (bm_n, bm_firms),
        "supp3_accruals":       (accr_n, accr_firms),
    }


def _compare_to_targets(stage_counts_: dict[str, tuple[int, int]]) -> pd.DataFrame:
    """Build a comparison grid: ours vs paper target, abs diff, pct diff,
    within-tolerance flag."""
    rows = []
    key_map = {
        "primary_all":          "primary_all_firmqtrs",
        "primary_after_price1": "primary_after_price1_firmqtrs",
        "supp1_sue":            "supp1_sue_firmqtrs",
        "supp2_bm":             "supp2_bm_firmqtrs",
        "supp3_accruals":       "supp3_accruals_firmqtrs",
    }
    firms_key_map = {
        "primary_all":          "primary_all_distinct_firms",
        "primary_after_price1": "primary_after_price1_firms",
        "supp1_sue":            "supp1_sue_distinct_firms",
        "supp2_bm":             "supp2_bm_distinct_firms",
        "supp3_accruals":       "supp3_accruals_distinct_firms",
    }
    for stage, (n_ours, nfirms_ours) in stage_counts_.items():
        n_paper = TARGETS[key_map[stage]]
        nfirms_paper = TARGETS[firms_key_map[stage]]
        rows.append({
            "stage": stage + " (firm-quarters)",
            "ours": n_ours,
            "paper": n_paper,
            "abs_diff": n_ours - n_paper,
            "pct_diff_pct": (n_ours - n_paper) / n_paper * 100.0,
            "within_tol": abs((n_ours - n_paper) / n_paper) <= TOLERANCE_PCT / 100.0,
        })
        rows.append({
            "stage": stage + " (distinct firms)",
            "ours": nfirms_ours,
            "paper": nfirms_paper,
            "abs_diff": nfirms_ours - nfirms_paper,
            "pct_diff_pct": (nfirms_ours - nfirms_paper) / nfirms_paper * 100.0,
            "within_tol": abs((nfirms_ours - nfirms_paper) / nfirms_paper)
                          <= TOLERANCE_PCT / 100.0,
        })
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------
# Table 1 markdown output
# ----------------------------------------------------------------------------


def render_table_1_markdown(
    stage_counts_: dict[str, tuple[int, int]],
    cmp_df: pd.DataFrame,
    panel_meta: dict,
) -> str:
    """Render Table 1 as a markdown file with our counts and a
    side-by-side comparison vs the paper."""
    def _row(label: str, stage: str) -> str:
        n, nf = stage_counts_[stage]
        n_p = TARGETS[
            "primary_all_firmqtrs" if stage == "primary_all"
            else "primary_after_price1_firmqtrs" if stage == "primary_after_price1"
            else "supp1_sue_firmqtrs" if stage == "supp1_sue"
            else "supp2_bm_firmqtrs" if stage == "supp2_bm"
            else "supp3_accruals_firmqtrs"
        ]
        nf_p = TARGETS[
            "primary_all_distinct_firms" if stage == "primary_all"
            else "primary_after_price1_firms" if stage == "primary_after_price1"
            else "supp1_sue_distinct_firms" if stage == "supp1_sue"
            else "supp2_bm_distinct_firms" if stage == "supp2_bm"
            else "supp3_accruals_distinct_firms"
        ]
        flag_n = "OK" if abs((n - n_p) / n_p) <= TOLERANCE_PCT / 100.0 else "GAP"
        flag_nf = "OK" if abs((nf - nf_p) / nf_p) <= TOLERANCE_PCT / 100.0 else "GAP"
        return (f"| {label} | {n:,} | {n_p:,} | {flag_n} | "
                f"{nf:,} | {nf_p:,} | {flag_nf} |")

    lines = []
    lines.append("# Table 1: Sample Selection (Replication)")
    lines.append("")
    lines.append(
        f"**Paper:** Balakrishnan, Bartov, Faurel (2009) — "
        f"*Post Loss/Profit Announcement Drift*"
    )
    lines.append(f"**Period:** fiscal years {PANEL_START[:4]}-{PANEL_END[:4]} "
                 f"(120 fiscal quarters per paper)")
    lines.append(f"**Tolerance:** ±{TOLERANCE_PCT:.0f}% on each count")
    lines.append("")
    lines.append("## Replicated counts vs paper targets")
    lines.append("")
    lines.append(
        "| Stage | Firm-quarters (ours) | Firm-quarters (paper) | "
        "FQ flag | Distinct firms (ours) | Distinct firms (paper) | Firms flag |"
    )
    lines.append("|---|---:|---:|:---:|---:|---:|:---:|")
    lines.append(_row(
        "All firm-quarters with required quarterly data on Compustat "
        "and return data on CRSP during sample period 1976-2005",
        "primary_all"))
    lines.append(_row(
        "With stock price five days prior to the quarterly earnings "
        "announcement date above $1",
        "primary_after_price1"))
    lines.append(_row(
        "Primary tests sample with additional data constraints to compute "
        "SUE (epspxq at q and q-12)",
        "supp1_sue"))
    lines.append(_row(
        "Primary tests sample with additional data constraints to compute "
        "book-to-market (ceqq, cshoq, prccq)",
        "supp2_bm"))
    lines.append(_row(
        "Primary tests sample with additional data constraints to compute "
        "accruals (ibq, oancfy, xidocy, atq at q and q-1, rdq >= 1988)",
        "supp3_accruals"))
    lines.append("")
    lines.append("## Panel metadata")
    lines.append("")
    for k, v in panel_meta.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    lines.append("## Per-cell comparison")
    lines.append("")
    lines.append(cmp_df.to_markdown(index=False, floatfmt=".2f"))
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def run_table1() -> dict:
    """Build the panel and report Table 1 sample-selection counts."""
    LAYOUT.ensure()
    rules = json.loads(LAYOUT.preparations_path("preprocessing_rules.json").read_text())
    print(f"[config] {len(rules)} preprocessing rules registered for {SLUG}")

    # ---- 1. Build panel via panel.sql ------------------------------------
    print("[1/4] building panel via panel.sql ...")
    df = q_file("panel.sql")
    df["rdq"] = pd.to_datetime(df["rdq"])
    df["datadate"] = pd.to_datetime(df["datadate"])
    panel_path = LAYOUT.data_path("panel.parquet")
    df.to_parquet(panel_path, index=False)
    print(f"      wrote {panel_path.name}: {len(df):,} rows x "
          f"{len(df.columns)} cols")

    # ---- 2. Per-stage counts ---------------------------------------------
    print("[2/4] computing per-stage counts ...")
    counts = stage_counts(df)

    # ---- 3. Compare to paper targets -------------------------------------
    print("[3/4] comparing to paper targets ...")
    cmp_df = _compare_to_targets(counts)
    n_within_tol = int(cmp_df["within_tol"].sum())
    n_total = len(cmp_df)

    # ---- 4. Render Table 1 markdown --------------------------------------
    panel_meta = {
        "panel rows":               f"{len(df):,}",
        "panel cols":               f"{len(df.columns)}",
        "distinct gvkeys (raw panel)": f"{df['gvkey'].nunique():,}",
        "distinct permnos (raw panel)": f"{df['permno'].nunique():,}",
        "rdq range":                f"{df['rdq'].min().date()} .. {df['rdq'].max().date()}",
        "cells within tolerance":   f"{n_within_tol}/{n_total}",
    }
    out_path = LAYOUT.result_path("table_1.md")
    out_path.write_text(render_table_1_markdown(counts, cmp_df, panel_meta))
    print(f"      wrote {out_path}")

    # ---- Console summary -------------------------------------------------
    print("\n=== Per-stage counts ===")
    for stage, (n, nf) in counts.items():
        print(f"  {stage:<24s}  rows={n:>9,}  firms={nf:>7,}")
    print(f"\n=== Side-by-side vs paper (tolerance ±{TOLERANCE_PCT:.0f}%) ===")
    for _, r in cmp_df.iterrows():
        flag = "PASS" if r["within_tol"] else "FAIL"
        print(f"  [{flag}] {r['stage']:<46s} "
              f"ours={r['ours']:>9,}  paper={r['paper']:>9,}  "
              f"diff={r['pct_diff_pct']:+6.2f}%")
    return {
        "counts": counts,
        "comparison": cmp_df,
        "n_within_tol": n_within_tol,
        "n_total": n_total,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--rebuild",
        action="store_true",
        help="rebuild panel even if data/panel.parquet exists",
    )
    args = ap.parse_args()

    LAYOUT.ensure()
    panel_path = LAYOUT.data_path("panel.parquet")
    if not args.rebuild and panel_path.exists():
        print(f"[panel] loading cached {panel_path.name} "
              "(pass --rebuild to re-run the SQL pipeline)")
        df = pd.read_parquet(panel_path)
        # Re-run the stage-count logic without rebuilding the panel.
        LAYOUT.ensure()
        rules = json.loads(
            LAYOUT.preparations_path("preprocessing_rules.json").read_text()
        )
        print(f"[config] {len(rules)} preprocessing rules registered for {SLUG}")
        counts = stage_counts(df)
        cmp_df = _compare_to_targets(counts)
        n_within_tol = int(cmp_df["within_tol"].sum())
        n_total = len(cmp_df)
        panel_meta = {
            "panel rows":               f"{len(df):,}",
            "panel cols":               f"{len(df.columns)}",
            "distinct gvkeys (raw panel)": f"{df['gvkey'].nunique():,}",
            "distinct permnos (raw panel)": f"{df['permno'].nunique():,}",
            "rdq range":                f"{df['rdq'].min().date()} .. {df['rdq'].max().date()}",
            "cells within tolerance":   f"{n_within_tol}/{n_total}",
        }
        out_path = LAYOUT.result_path("table_1.md")
        out_path.write_text(render_table_1_markdown(counts, cmp_df, panel_meta))
        print(f"[panel] wrote {out_path}")

        print("\n=== Per-stage counts ===")
        for stage, (n, nf) in counts.items():
            print(f"  {stage:<24s}  rows={n:>9,}  firms={nf:>7,}")
        print(f"\n=== Side-by-side vs paper (tolerance ±{TOLERANCE_PCT:.0f}%) ===")
        for _, r in cmp_df.iterrows():
            flag = "PASS" if r["within_tol"] else "FAIL"
            print(f"  [{flag}] {r['stage']:<46s} "
                  f"ours={r['ours']:>9,}  paper={r['paper']:>9,}  "
                  f"diff={r['pct_diff_pct']:+6.2f}%")
        return 0

    run_table1()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
