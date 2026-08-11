"""
Replication evaluator — Fairfield, Whisenant & Yohn (2003).

Reads the firm-year panel, recomputes the per-cell replicated metrics
(using the same aggregation logic as src/build_tables.py), applies the
per-cell Tier-1 / Tier-2 / FAIL / SKIP ladder from `rep/TOLERANCE_RULES.md`
against the per-cell paper targets in
`preparations/tables_to_replicate.json`, and prints a per-cell block plus
an aggregate tally and weighted loss number.

The Tier ladder:
    Tier 1  |replicated - paper| / |paper| <= tolerance_pct / 100
                       (or in the `zero_band` if set)
    Tier 2  sign matches, magnitude outside tolerance
    FAIL    sign disagreement (unless `insignificant: true` and
            inference_cell is set -- then enforce sign match loosely and
            report as "no_effect")
    SKIP    no value computed

Usage:
    python replications/fairfield_v2/src/evaluate.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

from utils.paths import paper_layout

# Reuse the build_tables code for deterministic recomputation.
LAYOUT = paper_layout("fairfield_v2").ensure()
SRC_DIR = LAYOUT.src_path
sys.path.insert(0, str(LAYOUT.root))  # for utils import; the build_tables
sys.path.insert(0, str(Path(__file__).resolve().parent))  # for build_tables

from build_tables import (  # noqa: E402
    load_panel,
    table_1,
    table_2,
    table_3,
    table_4,
    table_5,
    table_6,
    table_7,
)

PREP_DIR = LAYOUT.preparations_dir
TABLES_JSON = PREP_DIR / "tables_to_replicate.json"
LOSS_JSON = PREP_DIR / "loss_function.json"


def _sign(v: float) -> int:
    """Return +1, -1, or 0 (for near-zero)."""
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return 0
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0


def _classify(
    paper_val: float,
    ours_val: float,
    tol_pct: float,
    zero_band: float = None,
    insignificant: bool = False,
) -> Tuple[str, str]:
    """Classify a single cell into Tier 1 / Tier 2 / FAIL / SKIP / no_effect.

    Returns (status, detail_string).

    The detail string includes the deviation description used for reporting.
    """
    if ours_val is None or (isinstance(ours_val, float) and np.isnan(ours_val)):
        return ("SKIP", "no value computed")
    if paper_val is None:
        return ("SKIP", "no paper target")

    # Use absolute band if zero_band is set and paper value is at or below band.
    use_abs = (zero_band is not None) and (abs(paper_val) <= zero_band)

    diff = abs(ours_val - paper_val)
    if use_abs:
        # Tier 1 if |diff| <= zero_band; otherwise min(|diff|-zero_band, 2.0).
        if diff <= zero_band:
            return ("Tier 1", f"|diff|={diff:.4g} within zero_band={zero_band}")
        # magnitude miss (no sign FAIL — diff already excludes sign).
        return ("Tier 2", f"|diff|={diff:.4g} exceeds zero_band={zero_band}")

    # Relative rule.
    rel = diff / abs(paper_val) if paper_val != 0 else np.inf
    tol = tol_pct / 100.0

    # Sign comparison: use paper_sign=0 for "near-zero paper values" where
    # the printed value is at the precision floor (don't penalize opposite-
    # signed near-zeros as sign disagreement).
    paper_sign = _sign(paper_val)
    ours_sign = _sign(ours_val)
    sign_disagreement = (paper_sign != 0 and ours_sign != 0
                         and paper_sign != ours_sign)

    if rel <= tol:
        return ("Tier 1", f"|rel_err|={rel:.3%} within tol={tol:.3%}")

    if insignificant:
        # Magnitude is untestable. Enforce sign loosely; report as no_effect.
        return ("no_effect",
                f"|rel_err|={rel:.3%} exceeds tol={tol:.3%}; paper insignificant, "
                "magnitude untestable")

    if sign_disagreement:
        return ("FAIL",
                f"|rel_err|={rel:.3%}; sign disagreement (ours={ours_val:+.4g}, "
                f"paper={paper_val:+.4g})")

    return ("Tier 2", f"|rel_err|={rel:.3%} exceeds tol={tol:.3%}; sign matches")


def _load_targets() -> Tuple[Dict[str, Dict[str, Any]], List[Dict[str, Any]]]:
    """Return (metric_index_by_name, cells_list).

    metric_index_by_name: dict {cell_name -> {paper, tol_pct, zero_band,
                                              insignificant, table_id,
                                              paper_location, ...}}
    cells_list: list of dicts preserving the iteration order.

    The `insignificant` flag and `inference_cell` come from the loss
    function (which has them per-cell) rather than from the targets JSON
    (which only carries paper value + tolerance).
    """
    targets = json.loads(TABLES_JSON.read_text())
    loss = json.loads(LOSS_JSON.read_text())
    # Index loss cells by name to retrieve the per-cell `insignificant` flag.
    loss_cells = {c["name"]: c for c in loss["cells"]}

    metric_index: Dict[str, Dict[str, Any]] = {}
    cells_list: List[Dict[str, Any]] = []
    for tbl in targets["tables"]:
        for m in tbl["metrics"]:
            loss_entry = loss_cells.get(m["name"], {})
            entry = {
                "paper": m["value"],
                "tol_pct": m["tolerance_pct"],
                "zero_band": m.get("zero_band"),
                "insignificant": loss_entry.get("insignificant", False),
                "inference_cell": loss_entry.get("inference_cell"),
                "table_id": tbl["id"],
                "paper_location": m.get("paper_location", ""),
                "unit": m.get("unit", ""),
            }
            metric_index[m["name"]] = entry
            cells_list.append({"name": m["name"], **entry})
    return metric_index, cells_list


def _load_loss_weights() -> Dict[str, Dict[str, Any]]:
    loss = json.loads(LOSS_JSON.read_text())
    return {c["name"]: c for c in loss["cells"]}


def _recompute_metrics(panel: pd.DataFrame) -> Dict[str, float]:
    """Run the same SQL/Python aggregation logic as build_tables.py.

    Deterministic — no RNG, no timestamps. The values returned must match
    `results/all_metrics.json` byte-for-byte.
    """
    return {
        **table_1(panel),
        **table_2(panel),
        **table_3(panel),
        **table_4(panel),
        **table_5(panel),
        **table_6(panel),
        **table_7(panel),
    }


def _format_value(v: Any) -> str:
    """Compact value formatter for the per-cell output table."""
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    if isinstance(v, float):
        return f"{v:.4f}"
    return str(v)


def _deviation_str(paper_val: float, ours_val: float) -> str:
    """One-line deviation annotation."""
    if ours_val is None or (isinstance(ours_val, float) and np.isnan(ours_val)):
        return "—"
    if paper_val == 0:
        return f"abs diff = {ours_val - paper_val:+.4g}"
    rel = (ours_val - paper_val) / abs(paper_val)
    return f"{rel:+.1%}"


def main() -> int:
    # ---- recompute replicated metrics from panel ----
    panel = load_panel()
    metrics = _recompute_metrics(panel)

    # ---- load targets + weights ----
    metric_index, cells_list = _load_targets()
    weights = _load_loss_weights()

    # ---- per-cell classification ----
    rows: List[Dict[str, Any]] = []
    for cell in cells_list:
        name = cell["name"]
        paper = cell["paper"]
        tol = cell["tol_pct"]
        zb = cell["zero_band"]
        insig = cell["insignificant"]
        ours = metrics.get(name)
        status, detail = _classify(paper, ours, tol, zb, insig)
        rows.append({
            "table_id": cell["table_id"],
            "name": name,
            "paper": paper,
            "ours": ours,
            "status": status,
            "detail": detail,
        })

    # ---- print per-cell block ----
    print(f"\n{'Table':<6} {'Cell':<45} {'Paper':>10} {'Ours':>10} {'Status':<10}")
    print("-" * 90)
    for r in rows:
        print(f"{r['table_id']:<6} {r['name']:<45} "
              f"{_format_value(r['paper']):>10} {_format_value(r['ours']):>10} "
              f"{r['status']:<10} ({r['detail']})")

    # ---- aggregate tally ----
    tally: Dict[str, int] = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "SKIP": 0,
                             "no_effect": 0}
    for r in rows:
        tally[r["status"]] = tally.get(r["status"], 0) + 1
    total = len(rows)

    print("\n" + "=" * 70)
    print(f"Tier 1: {tally['Tier 1']} | "
          f"Tier 2: {tally['Tier 2']} | "
          f"FAIL: {tally['FAIL']} | "
          f"SKIP: {tally['SKIP']} | "
          f"no_effect: {tally['no_effect']} | "
          f"Total: {total}")

    # ---- weighted loss ----
    total_weight = 0.0
    weighted_err = 0.0
    for r in rows:
        name = r["name"]
        paper = r["paper"]
        ours = r["ours"]
        w = weights.get(name, {}).get("weight", 1)
        # Use the ladder err per the closed vocabulary.
        status = r["status"]
        if status == "Tier 1":
            err = 0.0
        elif status == "SKIP":
            err = 0.0
            w = 0  # SKIP cells do not contribute to the loss.
        elif status in ("Tier 2", "no_effect"):
            zb = metric_index[name].get("zero_band")
            if zb is not None and abs(paper) <= zb:
                err = max(min(abs(ours - paper) - zb, 2.0), 0.0)
            else:
                rel = abs(ours - paper) / abs(paper) if paper else float("inf")
                err = max(min(rel - metric_index[name]["tol_pct"] / 100.0, 2.0), 0.0)
        else:  # FAIL
            err = 3.0
        total_weight += w
        weighted_err += w * err

    loss = weighted_err / total_weight if total_weight > 0 else 0.0
    print(f"Loss: {loss:.4f}")

    # ---- additional diagnostic: list of FAIL/no_effect cells ----
    fails = [r for r in rows if r["status"] == "FAIL"]
    if fails:
        print("\nFAIL cells:")
        for r in fails:
            print(f"  {r['table_id']}.{r['name']}: paper={r['paper']}, "
                  f"ours={r['ours']:.4f}")
    no_effs = [r for r in rows if r["status"] == "no_effect"]
    if no_effs:
        print("\nno_effect cells (paper insignificant, magnitude untestable):")
        for r in no_effs:
            print(f"  {r['table_id']}.{r['name']}: paper={r['paper']}, "
                  f"ours={r['ours']:.4f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())