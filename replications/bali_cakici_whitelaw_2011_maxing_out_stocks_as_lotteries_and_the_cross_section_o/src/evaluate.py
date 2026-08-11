"""
Per-cell evaluator for Bali, Cakici, Whitelaw (2011) replication.

Reads:
  - preparations/tables_to_replicate.json (targets with tolerance_pct)
  - data/table_1_metrics.json (replicated values for Table 1)

For each target cell, computes:
  - Tier 1 (MATCH): |replicated - paper| / |paper| <= tolerance_pct / 100
  - Tier 2 (PATTERN): sign matches but magnitude outside tolerance
  - FAIL: sign is opposite (or near-zero disagreement)
  - SKIP: missing on either side

Prints per-cell table and aggregate tally. Per rep/TOLERANCE_RULES.md,
this evaluation is COMPUTED, not written — the auditor re-runs this script.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path("/home/ra_alan_mike_share/rep-it-up")
sys.path.insert(0, str(PROJECT_ROOT))

from utils.paths import paper_layout  # noqa: E402

LAYOUT = paper_layout(
    "bali_cakici_whitelaw_2011_maxing_out_stocks_as_lotteries_and_the_cross_section_o"
)


def load_targets() -> dict:
    """Load targets JSON keyed by table id."""
    with open(LAYOUT.preparations_path("tables_to_replicate.json")) as f:
        targets_all = json.load(f)
    return targets_all


def load_replicated_t1() -> dict:
    """Load replicated Table 1 metrics."""
    with open(LAYOUT.data_path("table_1_metrics.json")) as f:
        return json.load(f)


def cell_value_and_unit(metric: dict) -> tuple[float, str]:
    """Paper's reported value (always percent in our case)."""
    return float(metric["value"]), metric.get("unit", "percent_per_month")


def compute_status(
    paper_val: float, ours_val: float | None, tolerance_pct: float,
    zero_band: float = 0.0,
    cap_magnitude: float = 2.0,
) -> str:
    """Compute Tier 1 / Tier 2 / FAIL per rep/TOLERANCE_RULES.md.

    cap_magnitude: cells whose magnitude is more than this multiple of
    paper magnitude (sign matches) are FAIL, not Tier 2. Aligns with
    audit rubric Spot-check 10 / RUBRIC.md "Tier 2 within 2× of paper".
    """
    if ours_val is None:
        return "SKIP"

    # Sign check first
    paper_sign = 1 if paper_val > zero_band else (-1 if paper_val < -zero_band else 0)
    ours_sign = 1 if ours_val > zero_band else (-1 if ours_val < -zero_band else 0)

    if paper_sign == 0 and ours_sign == 0:
        # Both near zero — pass if both within zero_band
        return "Tier 1" if abs(ours_val) <= zero_band else "Tier 2"

    # Sign disagreement (and paper is not near zero) → FAIL
    if paper_sign != 0 and ours_sign != 0 and paper_sign != ours_sign:
        return "FAIL"

    # Near-zero paper case
    if paper_sign == 0:
        # Paper near zero, ours not — FAIL
        if abs(ours_val) > zero_band:
            return "FAIL"
        return "Tier 1"

    # Sign matches (or ours is near zero while paper is not).
    if ours_sign == 0:
        # Paper non-zero, ours ~0 — magnitude drift; Tier 2 only if
        # within cap. Outside the cap (|ours/paper| > cap_magnitude)
        # would imply sign-match by construction (ours=0 vs paper≠0),
        # so the cap is moot — call Tier 2.
        return "Tier 2"

    # Both have same sign — compute relative error
    rel_err = abs(ours_val - paper_val) / abs(paper_val)
    if rel_err <= tolerance_pct / 100:
        return "Tier 1"
    # Cap: magnitudes >cap_magnitude of paper → FAIL
    if rel_err > cap_magnitude:
        return "FAIL"
    return "Tier 2"


def evaluate_table_t1(
    targets_for_t1: dict, replicated: dict, zero_band: float = 0.005,
) -> tuple[list[dict], dict]:
    """
    Evaluate Table 1 cells.

    replicated is the JSON output of main.py — deciles keyed D1..D10 and
    a 'spread' dict.
    """
    rows = []
    counts = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "SKIP": 0}

    for metric in targets_for_t1["metrics"]:
        name = metric["name"]
        paper_val, unit = cell_value_and_unit(metric)
        tol = float(metric["tolerance_pct"])

        # Map metric name → replicated value
        ours_val = _lookup_replicated(name, replicated)

        status = compute_status(paper_val, ours_val, tol, zero_band=zero_band)
        counts[status] += 1

        rel_err = None
        if ours_val is not None and paper_val != 0:
            rel_err = (ours_val - paper_val) / abs(paper_val) * 100

        rows.append({
            "name": name,
            "paper": paper_val,
            "ours": ours_val,
            "tolerance_pct": tol,
            "rel_err_pct": rel_err,
            "status": status,
            "location": metric.get("paper_location", ""),
        })

    return rows, counts


def _lookup_replicated(name: str, replicated: dict) -> float | None:
    """Map target cell name to replicated value (converted to percent).

    Replicated values are stored as decimals in table_1_metrics.json; the
    targets are in percent_per_month. Convert by *100 for returns/alphas/avg_max.
    """
    spread = replicated.get("spread", {})
    deciles = replicated.get("deciles", {})

    # Spread cells — paper prints percent; ours are decimal
    if name == "vw_ret_diff":
        return spread.get("vw_ret_diff") * 100 if spread.get("vw_ret_diff") is not None else None
    if name == "vw_alpha_diff":
        return spread.get("vw_alpha_diff") * 100 if spread.get("vw_alpha_diff") is not None else None
    if name == "ew_ret_diff":
        return spread.get("ew_ret_diff") * 100 if spread.get("ew_ret_diff") is not None else None
    if name == "ew_alpha_diff":
        return spread.get("ew_alpha_diff") * 100 if spread.get("ew_alpha_diff") is not None else None
    if name == "vw_ret_tstat":
        return spread.get("vw_ret_tstat")
    if name == "vw_alpha_tstat":
        return spread.get("vw_alpha_tstat")
    if name == "ew_ret_tstat":
        return spread.get("ew_ret_tstat")
    if name == "ew_alpha_tstat":
        return spread.get("ew_alpha_tstat")

    # Per-decile cells — name looks like D{1..10}_{vw|ew}_{ret|alpha|avg_max}
    if name.startswith("D") and len(name) > 3:
        # E.g., D1_vw_ret  →  parts=["D1", "vw", "ret"]
        # E.g., D1_avg_max →  parts=["D1", "avg", "max"]
        parts = name.split("_")
        if len(parts) >= 3 and parts[1] in {"vw", "ew", "avg"}:
            dec_key = f"D{parts[0][1:]}"
            metric = "_".join(parts[1:])
            d = deciles.get(dec_key, {})
            v = d.get(metric)
            # All replicated values are stored as decimals; paper prints percent
            return v * 100 if v is not None else None

    return None


def print_table(rows: list[dict], title: str) -> None:
    print(f"\n## {title}")
    print()
    print("| Cell | Paper | Ours | Rel Err % | Tolerance | Status | Location |")
    print("| --- | ---: | ---: | ---: | ---: | :---: | :--- |")
    for r in rows:
        ours_str = "—" if r["ours"] is None else f"{r['ours']:.2f}"
        rel_err_str = "—" if r["rel_err_pct"] is None else f"{r['rel_err_pct']:.1f}"
        print(
            f"| {r['name']} | {r['paper']:.2f} | {ours_str} | "
            f"{rel_err_str} | {r['tolerance_pct']:.0f}% | {r['status']} | "
            f"{r['location']} |"
        )


def main():
    targets_all = load_targets()
    replicated = load_replicated_t1()

    tables = {t["id"]: t for t in targets_all["tables"]}
    t1 = tables.get("T1")
    if t1 is None:
        print("ERROR: T1 not in tables_to_replicate.json")
        sys.exit(1)

    rows, counts = evaluate_table_t1(t1, replicated, zero_band=0.005)

    print("=" * 80)
    print("Bali, Cakici, Whitelaw (2011) — Replication Evaluator")
    print("=" * 80)
    print()
    print(f"Table 1: {t1['description']}")
    print(f"Sample: 1962-07 → 2005-12, N months = {replicated['n_months']}")
    print(f"N observations: {replicated['n_obs_total']:,}")
    print()

    print_table(rows, "Per-cell evaluation — Table 1")

    total = sum(counts.values())
    print()
    print("=" * 80)
    print(f"Aggregate tally (N = {total} cells)")
    print(f"  Tier 1 (numerical match):   {counts['Tier 1']:>3} / {total}  ({counts['Tier 1']/total*100:.0f}%)")
    print(f"  Tier 2 (pattern match):     {counts['Tier 2']:>3} / {total}  ({counts['Tier 2']/total*100:.0f}%)")
    print(f"  FAIL (sign disagreement):   {counts['FAIL']:>3} / {total}  ({counts['FAIL']/total*100:.0f}%)")
    print(f"  SKIP (missing):             {counts['SKIP']:>3} / {total}  ({counts['SKIP']/total*100:.0f}%)")
    print("=" * 80)


if __name__ == "__main__":
    main()