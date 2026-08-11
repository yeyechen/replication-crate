"""Per-cell evaluation for Soliman (2007) replication.

Reads targets from `preparations/tables_to_replicate.json` and replicated
values from `eval/metrics.json`. Computes per-cell status per
`rep/TOLERANCE_RULES.md`:

- Tier 1: numerical match within tolerance_pct (or zero_band for near-zero cells)
- Tier 2: pattern match (same sign AND within the 2x magnitude cap)
- FAIL: numerical mismatch outside tolerance, with no pattern justification
- SKIP: cell intentionally not replicated

The magnitude cap is 2.0 — the same cap the canonical scorer
(`scripts/score_replication.py`) applies. Audit-2 [m1] flagged that this
file previously used 4.0, which made the local tally disagree with the
canonical one by 2-7 cells per tier. The canonical scorer remains
authoritative; this script is a convenience layer that should now agree
with it.

Besides printing the grid to stdout, this script APPENDS a per-cell
evaluation block to each `results/table_<id>.md` (audit-2 [m2]), so the
labels can be verified by reading the markdown alone.

Usage:
    uv run python src/evaluate.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

SLUG = Path(__file__).resolve().parent.parent
TARGETS_PATH = SLUG / "preparations" / "tables_to_replicate.json"
METRICS_PATH = SLUG / "eval" / "metrics.json"
RESULTS_DIR = SLUG / "results"

# Magnitude cap for Tier 2 — must match scripts/score_replication.py.
TIER2_MAGNITUDE_CAP = 2.0

# table id in tables_to_replicate.json -> results/<file>
TABLE_FILES = {
    "T1": "table_1.md",
    "T2": "table_3_panel_b.md",
    "T3": "table_4.md",
    "T4": "table_7.md",
    "T5": "table_8.md",
    "T6": "table_9.md",
}

EVAL_BLOCK_HEADER = "## Per-cell evaluation (Tier 1 / Tier 2 / FAIL)"


def load_targets(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def load_metrics(path: Path) -> dict:
    with open(path) as f:
        m = json.load(f)
    return m.get("metrics", {})


def _sign(x: float) -> int:
    return (x > 0) - (x < 0)


def within_tolerance(ours: float, paper: float, tol_pct: float,
                     zero_band: float | None = None) -> str:
    """Classify one cell, mirroring `scripts/score_replication.py::_classify_tier`.

    Sign disagreements are FAIL; magnitudes inside `tolerance_pct` are
    Tier 1; magnitudes outside tolerance but same-sign are Tier 2 provided
    the relative (or zero_band-scaled) error is within the 2x magnitude cap.
    Beyond the cap a sign-matching cell is FAIL.

    Audit-2 [m1]: this function previously used a 4x cap and a stricter
    zero_band rule, which made the local tally disagree with the canonical
    scorer by 2-7 cells per tier. It is now a line-for-line mirror.
    """
    if ours is None or paper is None:
        return "MISSING"
    tol = tol_pct / 100.0

    if zero_band is not None:
        abs_dev = abs(ours - paper)
        if abs_dev <= zero_band:
            return "Tier 1"
        mag_err = max(0.0, abs_dev - zero_band) / max(zero_band, 1e-12)
        if not (_sign(paper) == _sign(ours) or _sign(paper) == 0
                or _sign(ours) == 0):
            return "FAIL"
        if mag_err <= tol:
            return "Tier 1"
        return "FAIL" if mag_err > TIER2_MAGNITUDE_CAP else "Tier 2"

    if paper == 0:
        rel = abs(ours) if tol == 0 else min(abs(ours) / max(tol, 1e-12), 100.0)
    else:
        rel = abs(ours - paper) / abs(paper)

    if not (_sign(paper) == _sign(ours) or _sign(paper) == 0
            or _sign(ours) == 0):
        return "FAIL"
    if rel <= tol:
        return "Tier 1"
    return "FAIL" if rel > TIER2_MAGNITUDE_CAP else "Tier 2"


def evaluate(targets: dict, metrics: dict) -> list[dict]:
    """Return one record per target cell."""
    rows: list[dict] = []
    for table in targets["tables"]:
        tid = table["id"]
        for m in table["metrics"]:
            name = m["name"]
            paper_val = m["value"]
            tol = m.get("tolerance_pct", 10)
            zero_band = m.get("zero_band", None)
            # Look up: try literal key, then with T<N>_ prefix
            measured = metrics.get(name, {}).get("value")
            if measured is None:
                measured = metrics.get(f"{tid}_{name}", {}).get("value")
            rows.append({
                "table": tid,
                "cell": name,
                "paper": paper_val,
                "ours": measured,
                "tol": tol,
                "zero_band": zero_band,
                "status": within_tolerance(measured, paper_val, tol, zero_band),
            })
    return rows


def _rel_err(r: dict) -> float | None:
    if r["ours"] is None or r["paper"] is None or r["paper"] == 0:
        return None
    return abs(r["ours"] - r["paper"]) / abs(r["paper"])


def write_table_blocks(rows: list[dict]) -> list[Path]:
    """Append (or replace) the per-cell evaluation block in each table md."""
    written: list[Path] = []
    by_table: dict[str, list[dict]] = {}
    for r in rows:
        by_table.setdefault(r["table"], []).append(r)

    for tid, trows in by_table.items():
        fname = TABLE_FILES.get(tid)
        if fname is None:
            continue
        path = RESULTS_DIR / fname
        if not path.exists():
            print(f"[evaluate] WARNING: {path} does not exist — skipping block")
            continue

        n1 = sum(r["status"] == "Tier 1" for r in trows)
        n2 = sum(r["status"] == "Tier 2" for r in trows)
        nf = sum(r["status"] == "FAIL" for r in trows)
        nm = sum(r["status"] == "MISSING" for r in trows)

        block = [
            EVAL_BLOCK_HEADER,
            "",
            f"Generated by `src/evaluate.py` from `eval/metrics.json` and "
            f"`preparations/tables_to_replicate.json`. Tier 1 = within the "
            f"cell's `tolerance_pct` (or `zero_band`); Tier 2 = same sign and "
            f"relative error within the {TIER2_MAGNITUDE_CAP:g}x magnitude cap "
            f"used by the canonical scorer; FAIL otherwise.",
            "",
            f"**Tally for this table: Tier 1 = {n1}, Tier 2 = {n2}, "
            f"FAIL = {nf}, MISSING = {nm} (of {len(trows)} cells).**",
            "",
            "| Cell | Paper | Replicated | Tol % | Rel. err | Status |",
            "|---|---:|---:|---:|---:|---|",
        ]
        for r in sorted(trows, key=lambda x: x["cell"]):
            ours = "MISSING" if r["ours"] is None else f"{r['ours']:.4f}"
            paper = "—" if r["paper"] is None else f"{r['paper']:.4f}"
            rel = _rel_err(r)
            rel_s = "—" if rel is None else f"{rel:.2f}"
            block.append(
                f"| `{r['cell']}` | {paper} | {ours} | {r['tol']:.0f} | "
                f"{rel_s} | {r['status']} |"
            )
        block.append("")

        text = path.read_text()
        # Replace an existing block (idempotent re-runs) or append.
        marker = re.escape(EVAL_BLOCK_HEADER)
        text = re.sub(rf"\n{marker}\n.*\Z", "\n", text, flags=re.S)
        path.write_text(text.rstrip("\n") + "\n\n" + "\n".join(block))
        written.append(path)
    return written


def main() -> None:
    targets = load_targets(TARGETS_PATH)
    metrics = load_metrics(METRICS_PATH)

    print("=" * 84)
    print(f"Per-cell evaluation for {SLUG.name}")
    print("=" * 84)
    print(f"Targets: {len(targets['tables'])} tables, "
          f"{sum(len(t['metrics']) for t in targets['tables'])} cells")
    print(f"Metrics file: {METRICS_PATH}")
    print(f"Loaded {len(metrics)} replicated metric values")
    print(f"Tier-2 magnitude cap: {TIER2_MAGNITUDE_CAP:g}x "
          f"(matches scripts/score_replication.py)")
    print()

    rows = evaluate(targets, metrics)

    print(f"{'Table':<8}{'Cell':<40}{'Paper':>12}{'Ours':>12}{'Tol%':>6}  Status")
    print("-" * 84)
    for r in rows:
        ours_str = "MISSING" if r["ours"] is None else f"{r['ours']:>10.4f}"
        paper_str = f"{r['paper']:>10.4f}" if r["paper"] is not None else "    —"
        marker = "  <- needs review" if r["status"] == "FAIL" else ""
        print(f"{r['table']:<8}{r['cell']:<40}{paper_str:>12}{ours_str:>12}"
              f"{r['tol']:>6.0f}  {r['status']}{marker}")

    n_tier1 = sum(r["status"] == "Tier 1" for r in rows)
    n_tier2 = sum(r["status"] == "Tier 2" for r in rows)
    n_fail = sum(r["status"] == "FAIL" for r in rows)
    n_missing = sum(r["status"] == "MISSING" for r in rows)
    n_skip = len(rows) - n_tier1 - n_tier2 - n_fail - n_missing

    written = write_table_blocks(rows)
    print()
    for p in written:
        print(f"[evaluate] appended per-cell block to {p}")

    print()
    print("=" * 84)
    print("AGGREGATE TALLY (Tier 1 within tolerance, Tier 2 pattern match, "
          "FAIL, MISSING, SKIP)")
    print(f"  Tier 1:  {n_tier1}")
    print(f"  Tier 2:  {n_tier2}")
    print(f"  FAIL:    {n_fail}")
    print(f"  MISSING: {n_missing}")
    print(f"  SKIP:    {n_skip}")
    total = len(rows)
    if total > 0:
        # Same loss form as scripts/score_replication.py:
        # weight 0 for Tier 1, 1 for Tier 2, 2 for FAIL/MISSING.
        loss = (n_tier2 + 2 * n_fail + 2 * n_missing) / total
        print(f"  T1+T2 rate: {(n_tier1 + n_tier2) / total:.1%}")
        print(f"  Loss L ((n_Tier2 + 2·(n_FAIL + n_MISSING)) / total): {loss:.4f}")
    print("=" * 84)


if __name__ == "__main__":
    main()
