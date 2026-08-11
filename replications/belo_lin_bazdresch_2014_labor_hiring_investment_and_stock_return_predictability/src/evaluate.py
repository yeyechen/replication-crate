"""
Evaluate the replicated tables against the paper's targets.

Reads:
    - inputs/tables_to_replicate.json (per-cell targets with `tolerance_pct`)
    - data/tables_results.json (per-cell replicated values from tables.py)
    - results/table_*.md (the markdown reports)

Computes:
    - Per-cell tier (Tier 1 / Tier 2 / FAIL / SKIP)
    - Aggregate tally

Per rep/TOLERANCE_RULES.md:
    status = "Tier 1" (MATCH)   if |replicated - paper| / |paper| <= tolerance_pct / 100
            "Tier 2" (PATTERN)  if sign matches but magnitude outside tolerance
            "FAIL"              if sign is opposite
            "SKIP"              if either side is missing

Usage:
    python -u src/evaluate.py
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from utils.env import load_project_env
from utils.paths import paper_layout


load_project_env()
LAYOUT = paper_layout("belo_lin_bazdresch_2014_labor_hiring_investment_and_stock_return_predictability")


def _cell_value(name: str, results: dict) -> Optional[float]:
    """Look up a replicated value in the results dict by metric name."""
    # Direct mappings
    if name in results:
        return results[name]
    # Try without prefix
    for k, v in results.items():
        if k == name:
            return v
    return None


def evaluate_metric(metric: dict, results: dict) -> Dict[str, Any]:
    """Evaluate a single metric against the replicated value.

    Returns a dict with:
        - name: the metric name
        - paper_value: the paper's value
        - paper_location: the paper's location
        - tolerance_pct: the tolerance
        - replicated: the replicated value (or None if missing)
        - tier: 'Tier 1' / 'Tier 2' / 'FAIL' / 'SKIP'
        - abs_err: |replicated - paper|
        - rel_err: |replicated - paper| / |paper| (or None if paper = 0)
    """
    name = metric["name"]
    paper_value = metric["value"]
    paper_location = metric.get("paper_location", "")
    tolerance_pct = metric["tolerance_pct"]
    rep_value = _cell_value(name, results)

    if rep_value is None or (isinstance(rep_value, float) and np.isnan(rep_value)):
        return {
            "name": name, "paper_value": paper_value, "paper_location": paper_location,
            "tolerance_pct": tolerance_pct, "replicated": None,
            "tier": "SKIP", "abs_err": None, "rel_err": None,
        }

    abs_err = abs(rep_value - paper_value)
    if paper_value == 0:
        rel_err = None
    else:
        rel_err = abs_err / abs(paper_value)

    # Sign check: FAIL if signs disagree (and both are non-zero)
    if paper_value != 0 and rep_value != 0:
        same_sign = (paper_value > 0) == (rep_value > 0)
        if not same_sign:
            tier = "FAIL"
            return {
                "name": name, "paper_value": paper_value, "paper_location": paper_location,
                "tolerance_pct": tolerance_pct, "replicated": rep_value,
                "tier": tier, "abs_err": abs_err, "rel_err": rel_err,
            }

    # Magnitude check
    if rel_err is None:
        # Paper value is 0; just check if abs_err is small
        if abs_err <= 0.01:
            tier = "Tier 1"
        else:
            tier = "Tier 2"
    else:
        threshold = tolerance_pct / 100
        if rel_err <= threshold:
            tier = "Tier 1"
        else:
            tier = "Tier 2"

    return {
        "name": name, "paper_value": paper_value, "paper_location": paper_location,
        "tolerance_pct": tolerance_pct, "replicated": rep_value,
        "tier": tier, "abs_err": abs_err, "rel_err": rel_err,
    }


def collect_replicated_values() -> Dict[str, float]:
    """Collect all replicated values in a flat dict keyed by metric name.

    Maps the metric names in tables_to_replicate.json to the values stored
    in data/tables_results.json.
    """
    results_path = LAYOUT.data_path("tables_results.json")
    if not results_path.exists():
        print(f"WARNING: {results_path} does not exist")
        return {}
    data = json.loads(results_path.read_text())
    flat = {}

    # ----- Table 1 -----
    t1 = data.get("table_1", {})
    cells = t1.get("cells", [])
    mae = t1.get("mae", {})
    # Build a lookup: (weighting, bin_label) -> cell
    cell_lookup = {}
    for c in cells:
        weighting = c["weighting"]
        bin_label = c["bin"]
        cell_lookup[(weighting, bin_label)] = c

    weight_map = {"EW": "ew_all", "EW_nomicro": "ew_nomicro", "VW": "vw_all"}
    for weighting, abbrev in weight_map.items():
        # Map bin numbers (1, 2, 5, 9, 10, "L-H") to the right paper labels
        bin_map = {1: "low", 2: "2", 5: "5", 9: "9", 10: "high", "L-H": "LH"}
        for bin_idx, bin_label in bin_map.items():
            cell = cell_lookup.get((weighting, bin_idx))
            if cell is None:
                continue
            # r^e
            name = f"T1.re_{abbrev}_{bin_label}"
            flat[name] = cell["ann_re"]
            # t-stat
            name_t = f"T1.t_{abbrev}_{bin_label}"
            flat[name_t] = cell["t_re"]
            # Sharpe
            if bin_label in ("LH",):
                name_sr = f"T1.SR_{abbrev}_{bin_label}"
                flat[name_sr] = cell["sr"]
            # CAPM alpha + t
            if bin_label in ("low", "2", "5", "9", "high", "LH"):
                name_a = f"T1.capm_alpha_{abbrev}_{bin_label}"
                flat[name_a] = cell["capm_alpha"]
                name_at = f"T1.t_capm_{abbrev}_{bin_label}"
                flat[name_at] = cell["capm_t"]
            # CAPM beta (for VW only)
            if weighting == "VW" and bin_label in ("low", "high", "LH"):
                name_b = f"T1.capm_b_{abbrev}_{bin_label}"
                flat[name_b] = cell["capm_b"]
            # FF3 alpha + t
            if bin_label in ("low", "2", "5", "9", "high", "LH"):
                name_fa = f"T1.ff3_alpha_{abbrev}_{bin_label}"
                flat[name_fa] = cell["ff3_alpha"]
                name_ft = f"T1.t_ff3_{abbrev}_{bin_label}"
                flat[name_ft] = cell["ff3_t"]
        # m.a.e.
        key_mae_capm = (weighting, "capm")
        key_mae_ff3 = (weighting, "ff3")
        weight_mae_map = {"EW": "ew_all", "EW_nomicro": "ew_nomicro", "VW": "vw_all"}
        abbrev = weight_mae_map[weighting]
        flat[f"T1.capm_mae_{abbrev}"] = mae.get(f"('{weighting}', 'capm')", np.nan)
        flat[f"T1.ff3_mae_{abbrev}"] = mae.get(f"('{weighting}', 'ff3')", np.nan)

    # ----- Table 2 -----
    t2 = data.get("table_2", {})
    ts_avg_list = t2.get("ts_avg", [])
    ts_avg = {}
    for row in ts_avg_list:
        var = row["var"]
        label = row["label"]
        bin_idx = row["bin"]
        # Normalize bin_idx to int or "L-H"
        if bin_idx == "L-H":
            norm_bin = "L-H"
        else:
            norm_bin = int(bin_idx)
        ts_avg[(var, label, norm_bin)] = row["median"]

    t2_map = {"t": "t", "t1": "t1"}
    var_map = {"hn": "HN", "ik": "IK", "roa": "ROA", "km": "KM", "size": "Size"}
    for var, abbrev in var_map.items():
        for label, abbrev_time in t2_map.items():
            for bin_idx in [1, 2, 5, 9, 10, "L-H"]:
                bin_label_map = {1: "low", 2: "2", 5: "5", 9: "9", 10: "high", "L-H": "LH"}
                bin_label = bin_label_map[bin_idx]
                val = ts_avg.get((var, label, bin_idx), np.nan)
                flat[f"T2.{abbrev}_{abbrev_time}_{bin_label}"] = val

    # ----- Table 3 -----
    t3 = data.get("table_3", {})
    cells = t3.get("cells", [])
    cell_lookup = {}
    for c in cells:
        weighting = c["weighting"]
        ik_bin = c["ik_bin"]
        hn_bin = c["hn_bin"]
        cell_lookup[(weighting, ik_bin, hn_bin)] = c

    # Map weighting to paper label
    weight_map = {"EW": "ew_all", "EW_nomicro": "ew_nomicro", "VW": "vw_all"}
    # Map cell (ik_bin, hn_bin) to paper label
    ik_map = {1: "L", 2: "M", 3: "H"}
    hn_map = {1: "L", 2: "M", 3: "H"}
    for weighting, abbrev in weight_map.items():
        for i in [1, 2, 3]:
            for j in [1, 2, 3]:
                cell = cell_lookup.get((weighting, i, j))
                if cell is None:
                    continue
                name = f"T3.re_{abbrev}_{ik_map[i]}{hn_map[j]}"
                flat[name] = cell["ann_re"]
                name_t = f"T3.t_{abbrev}_{ik_map[i]}{hn_map[j]}"
                flat[name_t] = cell["t_re"]
                name_capm = f"T3.capm_alpha_{abbrev}_{ik_map[i]}{hn_map[j]}"
                flat[name_capm] = cell["capm_alpha"]
                name_ff3 = f"T3.ff3_alpha_{abbrev}_{ik_map[i]}{hn_map[j]}"
                flat[name_ff3] = cell["ff3_alpha"]
        # Row L-H (HN within IK bin) - paper uses HL_minus_LH_row for the highest IK bin
        for i in [1, 2, 3]:
            cell = cell_lookup.get((weighting, i, "L-H"))
            if cell is None:
                continue
            # Paper convention: HL_minus_LH_row is the L-H spread in the highest IK bin
            # (i.e., IK_3 / HL_minus_LH_row). For earlier bins, we use the IK-prefix.
            if i == 3:
                name = f"T3.re_{abbrev}_HL_minus_LH_row"
                name_capm = f"T3.capm_alpha_{abbrev}_HL_minus_LH_row"
                name_ff3 = f"T3.ff3_alpha_{abbrev}_HL_minus_LH_row"
            else:
                # Map i to paper bin label: 1 -> L, 2 -> M, 3 -> H
                ik_label = ik_map[i]
                name = f"T3.re_{abbrev}_{ik_label}_L_minus_H"
                name_capm = f"T3.capm_alpha_{abbrev}_{ik_label}_L_minus_H"
                name_ff3 = f"T3.ff3_alpha_{abbrev}_{ik_label}_L_minus_H"
            flat[name] = cell["ann_re"]
            flat[name_capm] = cell.get("capm_alpha")
            flat[name_ff3] = cell.get("ff3_alpha")
        # Column L-H (IK within HN bin) - paper uses LH_col for the L-IK to H-IK column
        for j in [1, 2, 3]:
            cell = cell_lookup.get((weighting, "L-H", j))
            if cell is None:
                continue
            # Paper convention: LH_col is the L-H spread in the lowest HN bin
            hn_label = hn_map[j]
            if j == 1:
                name = f"T3.re_{abbrev}_LH_col"
                name_capm = f"T3.capm_alpha_{abbrev}_LH_col"
                name_ff3 = f"T3.ff3_alpha_{abbrev}_LH_col"
            else:
                name = f"T3.re_{abbrev}_L_minus_H_{hn_label}"
                name_capm = f"T3.capm_alpha_{abbrev}_L_minus_H_{hn_label}"
                name_ff3 = f"T3.ff3_alpha_{abbrev}_L_minus_H_{hn_label}"
            flat[name] = cell["ann_re"]
            flat[name_capm] = cell.get("capm_alpha")
            flat[name_ff3] = cell.get("ff3_alpha")
        # m.a.e.
        flat[f"T3.capm_mae_{abbrev}"] = t3.get("mae", {}).get(f"('{weighting}', 'capm')", np.nan)
        flat[f"T3.ff3_mae_{abbrev}"] = t3.get("mae", {}).get(f"('{weighting}', 'ff3')", np.nan)

    # ----- Table 4 -----
    t4 = data.get("table_4", {})
    fm = t4.get("fm", {})
    ols = t4.get("ols", {})

    # FM specs (1-4)
    var_map = {"hn": "HN", "ik": "IK", "micro": "Micro",
               "micro_hn": "MicroHN", "micro_ik": "MicroIK"}
    spec_map = {"spec1": 1, "spec2": 2, "spec3": 3, "spec4": 4}
    for spec_id, spec_num in spec_map.items():
        fm_spec = fm.get(spec_id)
        if fm_spec is None:
            continue
        for var, name in var_map.items():
            coef = fm_spec.get("mean", {}).get(var)
            tval = fm_spec.get("t_stat", {}).get(var)
            if coef is not None:
                flat[f"T4.fm_{name}_spec{spec_num}"] = coef
            if tval is not None:
                flat[f"T4.fm_t{name}_spec{spec_num}"] = tval

    # OLS specs (5-8)
    spec_map = {"spec5": 5, "spec6": 6, "spec7": 7, "spec8": 8}
    for spec_id, spec_num in spec_map.items():
        ols_spec = ols.get(spec_id)
        if ols_spec is None:
            continue
        for var, name in var_map.items():
            coef = ols_spec.get("params", {}).get(var)
            tval = ols_spec.get("tvalues", {}).get(var)
            if coef is not None:
                flat[f"T4.ols_{name}_spec{spec_num}"] = coef
            if tval is not None:
                flat[f"T4.ols_t{name}_spec{spec_num}"] = tval

    # N
    flat["T4.N_fm"] = t4.get("n_fm_obs", 0)
    flat["T4.N_ols"] = t4.get("n_ols_obs", 0)

    return flat


def main():
    # Load targets
    targets = json.loads(LAYOUT.preparations_path("tables_to_replicate.json").read_text())

    # Load replicated values
    flat = collect_replicated_values()

    # Write flat dict to data/metrics.json (canonical score-input artifact
    # per scripts/score_replication.py). Schema v2: each metric entry is
    # {"value": <number>, "unit": "..."} keyed by metric name.
    metrics_path = LAYOUT.data_path("metrics.json")
    serializable = {}
    for k, v in flat.items():
        if isinstance(v, float) and np.isnan(v):
            serializable[k] = {"value": None, "unit": ""}
        else:
            serializable[k] = {"value": v, "unit": ""}
    metrics_payload = {
        "schema_version": 2,
        "slug": LAYOUT.slug,
        "metrics": serializable,
    }
    metrics_path.write_text(json.dumps(metrics_payload, indent=2, sort_keys=True))
    print(f"Wrote {metrics_path} ({len(serializable)} cells)")

    # Build per-cell results
    cells = []
    for table in targets["tables"]:
        for metric in table["metrics"]:
            res = evaluate_metric(metric, flat)
            res["table"] = table["id"]
            cells.append(res)

    # Print per-cell table
    print("=" * 120)
    print("PER-CELL RESULTS")
    print("=" * 120)
    print()
    print(f"{'Table':<8}{'Metric':<35}{'Paper':<12}{'Replicated':<14}{'Tier':<10}{'RelErr':<12}{'Note':<20}")
    print("-" * 120)
    for c in cells:
        rep = f"{c['replicated']:.2f}" if c["replicated"] is not None else "—"
        rel = f"{c['rel_err']*100:.1f}%" if c["rel_err"] is not None else "—"
        print(f"{c['table']:<8}{c['name']:<35}{c['paper_value']:<12.2f}{rep:<14}{c['tier']:<10}{rel:<12}{c['paper_location']:<20}")

    # Aggregate tally
    print()
    print("=" * 120)
    print("AGGREGATE TALLY")
    print("=" * 120)
    tally = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "SKIP": 0}
    for c in cells:
        tally[c["tier"]] += 1
    print(f"Tier 1 (MATCH):     {tally['Tier 1']}")
    print(f"Tier 2 (PATTERN):   {tally['Tier 2']}")
    print(f"FAIL:               {tally['FAIL']}")
    print(f"SKIP:               {tally['SKIP']}")
    print(f"Total scored:       {sum(tally.values())}")
    total = sum(tally.values())
    if total > 0:
        hit_rate = (tally["Tier 1"] + tally["Tier 2"]) / total
        print(f"Hit rate (Tier 1 + Tier 2): {hit_rate:.1%}")

    # Per-table summary
    print()
    print("=" * 120)
    print("PER-TABLE SUMMARY")
    print("=" * 120)
    by_table = {}
    for c in cells:
        by_table.setdefault(c["table"], []).append(c)
    for tbl_id, items in by_table.items():
        t1 = sum(1 for c in items if c["tier"] == "Tier 1")
        t2 = sum(1 for c in items if c["tier"] == "Tier 2")
        fl = sum(1 for c in items if c["tier"] == "FAIL")
        sk = sum(1 for c in items if c["tier"] == "SKIP")
        print(f"{tbl_id}: Tier 1={t1}, Tier 2={t2}, FAIL={fl}, SKIP={sk} (total {len(items)})")


if __name__ == "__main__":
    main()
