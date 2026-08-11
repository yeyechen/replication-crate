"""
evaluate.py — Per-cell tier classifier for Jegadeesh (1990) replication.

Loads:
  - eval/metrics.json          : replicated values (this run)
  - inputs/tables_to_replicate.json : per-cell targets (paper value,
                                     tolerance_pct, paper_location,
                                     optional zero_band)

For each metric in every table, classifies the replicated value vs the
paper value:

  - |delta| <= tolerance_pct * |paper| / 100   →  Tier 1
  - sign matches AND magnitude within 2x      →  Tier 2
  - otherwise                                  →  FAIL
  - replicated value is missing                →  MISSING

If the metric carries a `zero_band` extension, the absolute-deviation
check is used in place of the relative check (paper cells near zero
have unreliable relative errors).  The implementation mirrors
`scripts/score_replication.py:_classify_tier`.

Output
------
A per-cell table with columns: Table | Cell | Paper | Ours | Status
followed by the aggregate tally Tier 1 / Tier 2 / FAIL / MISSING.

This is the orchestrator's tool — it prints the table and tally when
run.  No filesystem writes are performed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Resolve repo root so we can use utils.paths.
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from utils.paths import paper_layout  # noqa: E402

SLUG = "jegadeesh_1990_evidence_of_predictable_behavior_of_security_returns"
LAYOUT = paper_layout(SLUG)

CAP_MAGNITUDE = 2.0
SIGN_FAIL_EPS = 1e-12


def _sign(x: float) -> int:
    if x > SIGN_FAIL_EPS:
        return 1
    if x < -SIGN_FAIL_EPS:
        return -1
    return 0


def _classify(
    paper_value: float | None,
    ours: float | None,
    tolerance_pct: float,
    zero_band: float | None,
) -> tuple[str, float | None]:
    """Return (status, rel_err_or_abs_err) for one cell.

    `rel_err` is the relative error `|ours - paper| / |paper|`
    (or the zero_band-relative equivalent when `zero_band` is given).
    Returned only for display — not used to choose Tier.
    """
    if paper_value is None:
        return ("SKIP", None)
    if ours is None:
        return ("MISSING", None)

    if zero_band is not None:
        abs_dev = abs(ours - paper_value)
        if abs_dev <= zero_band:
            return ("Tier 1", 0.0)
        # Outside the band; classify by zero_band-scaled magnitude.
        mag_err = max(0.0, abs_dev - zero_band) / max(zero_band, 1e-12)
        paper_sign = _sign(paper_value)
        ours_sign = _sign(ours)
        sign_match = paper_sign == ours_sign or paper_sign == 0 or ours_sign == 0
        if not sign_match:
            return ("FAIL", mag_err)
        tol = tolerance_pct / 100.0
        if mag_err <= tol:
            return ("Tier 1", mag_err)
        if mag_err > CAP_MAGNITUDE:
            return ("FAIL", mag_err)
        return ("Tier 2", mag_err)

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
    metrics_path = LAYOUT.eval_path("metrics.json")
    targets_path = LAYOUT.input_path("tables_to_replicate.json")

    if not metrics_path.exists():
        print(f"ERROR: {metrics_path} does not exist.  Run src/main.py first.")
        return 1
    if not targets_path.exists():
        print(f"ERROR: {targets_path} does not exist.")
        return 1

    metrics = json.loads(metrics_path.read_text()).get("metrics", {})
    tables = json.loads(targets_path.read_text())

    # Flatten targets:  name -> {table_id, value, tolerance_pct, paper_location,
    #                            unit, zero_band}
    targets: dict[str, dict] = {}
    for tbl in tables.get("tables", []):
        tid = tbl.get("id", "?")
        for m in tbl.get("metrics", []):
            name = m.get("name")
            if not name:
                continue
            targets[name] = {
                "table_id": tid,
                "value": m.get("value"),
                "tolerance_pct": float(m.get("tolerance_pct", 0)),
                "paper_location": m.get("paper_location"),
                "unit": m.get("unit"),
                "zero_band": m.get("zero_band"),
            }

    # Per-cell classification.
    rows: list[tuple[str, str, float | None, float | None, str]] = []
    counts: dict[str, int] = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "MISSING": 0, "SKIP": 0}
    for name in sorted(targets):
        t = targets[name]
        entry = metrics.get(name)
        ours = entry.get("value") if isinstance(entry, dict) else None
        status, _ = _classify(
            paper_value=t["value"],
            ours=ours,
            tolerance_pct=t["tolerance_pct"],
            zero_band=t["zero_band"],
        )
        if status in counts:
            counts[status] += 1
        else:
            counts.setdefault(status, 0)
        rows.append((t["table_id"], name, t["value"], ours, status))

    # Print the per-cell table.
    print(f"# evaluate.py — per-cell tier table for {SLUG}")
    print(f"# metrics.json: {metrics_path} ({len(metrics)} entries)")
    print(f"# targets: {targets_path} ({len(targets)} cells across "
          f"{len({t['table_id'] for t in targets.values()})} tables)")
    print()
    print("| Table | Cell | Paper | Ours | Status |")
    print("|-------|------|-------|------|--------|")
    for tbl, name, paper, ours, status in rows:
        paper_s = f"{paper:+.4f}" if paper is not None else "—"
        ours_s = f"{ours:+.4f}" if ours is not None else "—"
        print(f"| {tbl} | {name} | {paper_s} | {ours_s} | {status} |")

    # Aggregate.
    print()
    print("Aggregate:")
    for tier in ("Tier 1", "Tier 2", "FAIL", "MISSING", "SKIP"):
        c = counts.get(tier, 0)
        if c:
            print(f"  {tier}: {c}")

    # Quick win-rate.
    n_eval = counts["Tier 1"] + counts["Tier 2"] + counts["FAIL"] + counts["MISSING"]
    n_t1 = counts["Tier 1"] + counts["Tier 2"]
    if n_eval:
        print(f"\n  Tier 1+Tier 2 / evaluated : {n_t1}/{n_eval} = "
              f"{n_t1 / n_eval:.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
