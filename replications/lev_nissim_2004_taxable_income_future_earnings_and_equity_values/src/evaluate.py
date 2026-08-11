"""
evaluate.py — Read eval/metrics.json and print the per-cell tier table.

Closes Spot-check 10 (re-runnable per-cell evaluation) and prints a
human-readable summary of the current iteration's tier classification.

Each row shows:
  - cell name (target metric)
  - paper value (from `tables_to_replicate.json`)
  - ours value (from `eval/metrics.json`)
  - rel_err (|ours - paper| / |paper|)
  - tier (Tier 1 / Tier 2 / FAIL / MISSING / SKIP / no_effect)

The tier ladder follows `rep/TOLERANCE_RULES.md`:
  - Tier 1: within per-cell tolerance_pct
  - Tier 2: magnitude within 2x of paper (per the canonical scorer
            CAP_MAGNITUDE = 2.0)
  - FAIL: sign mismatch OR magnitude > 2x
  - MISSING: paper target exists but ours is absent
  - SKIP: no paper target
  - no_effect: paper itself marks the effect as insignificant

Usage:
    python src/evaluate.py                          # default run
    python src/evaluate.py --tier FAIL --tier MISSING  # filter
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from utils.paths import paper_layout  # noqa: E402

SLUG = "lev_nissim_2004_taxable_income_future_earnings_and_equity_values"
LAYOUT = paper_layout(SLUG)

# Mirror the canonical scorer's tier ladder.
CAP_MAGNITUDE = 2.0
SIGN_FAIL_EPS = 1e-12


def _sign(x: float) -> int:
    if x > SIGN_FAIL_EPS:
        return 1
    if x < -SIGN_FAIL_EPS:
        return -1
    return 0


def _classify_tier(
    paper_value: float, ours: float, tolerance_pct: float
) -> tuple[str, float | None]:
    """Independent of the canonical scorer — for printing in this tool."""
    tol = tolerance_pct / 100.0
    if paper_value == 0:
        rel_err = abs(ours) if tol == 0 else min(abs(ours) / max(tol, 1e-12), 100.0)
    else:
        rel_err = abs(ours - paper_value) / abs(paper_value)

    paper_sign = _sign(paper_value)
    ours_sign = _sign(ours)
    sign_match = paper_sign == ours_sign or paper_sign == 0 or ours_sign == 0

    if not sign_match:
        return ("FAIL", rel_err)
    if rel_err <= tol:
        return ("Tier 1", rel_err)
    if rel_err > CAP_MAGNITUDE:
        return ("FAIL", rel_err)
    return ("Tier 2", rel_err)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--tier",
        action="append",
        default=None,
        help="Filter to only show cells with these tiers (repeatable).",
    )
    ap.add_argument(
        "--table",
        action="append",
        default=None,
        help="Filter to only show cells in these tables (repeatable).",
    )
    args = ap.parse_args()

    metrics_path = LAYOUT.eval_path("metrics.json")
    if not metrics_path.exists():
        print(f"ERROR: {metrics_path} does not exist. Run src/assemble_metrics.py first.")
        return 1

    metrics = json.loads(metrics_path.read_text())["metrics"]
    tables = json.loads(LAYOUT.preparations_path("tables_to_replicate.json").read_text())

    # Build a name → table_id map.
    name_to_table: dict[str, str] = {}
    for tbl in tables["tables"]:
        for m in tbl["metrics"]:
            name_to_table[m["name"]] = tbl["id"]

    # Print all cells.
    print(f"# evaluate.py — per-cell tier table for {SLUG}")
    print(f"# metrics.json: {metrics_path} ({len(metrics)} entries)")
    print()

    rows: list[tuple[str, str, float, float | None, float, float | None, str]] = []
    for name in sorted(name_to_table):
        if name not in metrics:
            continue
        e = metrics[name]
        paper = e["paper"]
        ours = e["value"]
        tol = e["tolerance_pct"]
        if paper is None:
            tier = "SKIP"
            rel_err = None
        elif ours is None:
            tier = "MISSING"
            rel_err = None
        else:
            tier, rel_err = _classify_tier(paper, ours, tol)
        rows.append((name, name_to_table[name], paper, ours, tol, rel_err, tier))

    # Apply filters.
    if args.tier:
        rows = [r for r in rows if r[6] in args.tier]
    if args.table:
        rows = [r for r in rows if r[1] in args.table]

    # Print header.
    print(f"{'cell':<34} {'table':<6} {'paper':>12} {'ours':>12} {'tol%':>6} {'rel_err':>9} {'tier':<10}")
    print("-" * 96)
    for name, tbl, paper, ours, tol, rel_err, tier in rows:
        paper_s = f"{paper:.4f}" if paper is not None else "—"
        ours_s = f"{ours:.4f}" if ours is not None else "—"
        rel_s = f"{rel_err:.4f}" if rel_err is not None else "—"
        print(f"{name:<34} {tbl:<6} {paper_s:>12} {ours_s:>12} {tol:>6.1f} {rel_s:>9} {tier:<10}")

    # Counts.
    print()
    counts: dict[str, int] = {}
    for _, _, _, _, _, _, tier in rows:
        counts[tier] = counts.get(tier, 0) + 1
    for tier in ("Tier 1", "Tier 2", "FAIL", "MISSING", "SKIP", "no_effect"):
        if counts.get(tier, 0):
            print(f"  {tier:<10}: {counts[tier]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
