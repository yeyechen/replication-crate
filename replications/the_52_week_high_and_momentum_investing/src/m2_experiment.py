"""
M2 adjudication experiment (audit1.md [M2], outer iteration 2): run Table VII
under the g_gh VARIANT B (available-lag reference price, min 24 usable lags;
panel column g_gh_b) and compare against the official VARIANT A run
(strict-60, panel column g_gh) WITHOUT overwriting any official artifact.

Run AFTER src/main.py has rebuilt data/panel.parquet with g_gh_b + wh_lo_sig:
    cd <repo-root>
    REPLICATIONS_PATH=$PWD/replications \
    PYTHONPATH=$PWD:replications/the_52_week_high_and_momentum_investing/src \
    python3 replications/the_52_week_high_and_momentum_investing/src/m2_experiment.py

Outputs (additive only):
  - data/fm_coefficients_gh_variantB.parquet  (variant-B c_{k,t} series)
  - results/table_7_variantB.md               (full 15x8 grid in table_7.md
                                               format + A-vs-B before/after
                                               block + adoption criteria)

Official artifacts are NOT touched:
  - results/table_7.md, data/fm_coefficients_gh.parquet stay variant A;
  - Tables I and V do not use g_gh: they are RE-RUN in memory
    (write_outputs=False, dependent ret_dl as official) and compared
    bit-exactly against data/strategy_returns.parquet and
    data/fm_coefficients.parquet (the pre-experiment official caches,
    produced from the pre-rebuild panel). The panel rebuild guard already
    asserted every pre-existing column reproduces bit-exactly, so these
    checks MUST pass (they are the regression gate for this experiment).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import tables_1_3
from tables_5 import (CFG_V, COLS, LAYOUT, PRIMARY_WH, TableConfig, coef_names,
                      fmt, intermediate_path, load_ff, load_targets, make_rows,
                      ra_intercept_tstat, raw_mean_tstat, row_series,
                      run_table, tier)
from tables_7 import CFG_VII, vii_preflight_gate

GH_ROWS = ("gh_winner", "gh_loser", "gh_spread")

# Table VII pointed at g_gh_b instead of g_gh. Everything else identical to
# the official CFG_VII (same dummy order jt, mg, gh, wh; same preflight;
# different output files so the official variant-A artifacts stay intact).
CFG_VII_B = TableConfig(
    table_id="T7",
    strat_sig={"jt": "jt_sig", "mg": "mg_sig", "gh": "g_gh_b", "wh": PRIMARY_WH},
    coeff_parquet="fm_coefficients_gh_variantB.parquet",
    md_name="table_7_variantB.md",
    title=("# Table VII (variant B adjudication) — George & Hwang (2004): "
           "GH dummies from g_gh_b (available-lag reference price, "
           "min 24 usable lags; audit1.md [M2])"),
    dummy_pairs=("JH/JL<-jt_sig, MH/ML<-mg_sig, GH/GL<-g_gh_b, "
                 "FHH/FHL<-wh_sig_dc"),
    preflight_rows=CFG_VII.preflight_rows,
    paper_preflight=CFG_VII.paper_preflight,
    preflight_gate=vii_preflight_gate,
)


# --- variant-A grid reconstruction from the official cache -------------------

def cells_from_coeff(coeff_df: pd.DataFrame, strat_sig: dict,
                     targets: dict) -> dict:
    """Recompute the full (col, row, kind) -> (val, paper, tol, tier) grid from
    a c_{k,t} parquet using the IDENTICAL engine functions run_table uses
    (raw_mean_tstat / ra_intercept_tstat / row_series / tier). For the
    variant-A cache this reproduces the official results/table_7.md numbers
    (the auditor independently verified that cache -> 4dp)."""
    coef = coef_names(strat_sig)
    rows = make_rows(strat_sig)
    ff = load_ff()
    hold_months = pd.DatetimeIndex(coeff_df["month"])
    ff_aligned = ff.set_index("month").reindex(hold_months)
    ff_arr = ff_aligned[["mkt_rf", "smb", "hml"]].to_numpy(dtype="float64")
    assert np.isfinite(ff_arr).all(), "FF factors missing on hold grid"
    mo = hold_months.month.to_numpy()
    mask_all = np.ones(len(hold_months), dtype=bool)
    mask_exjan = mo != 1
    out = {}
    for hz in ("s66", "s612"):
        c = np.column_stack([
            coeff_df[f"{hz}_{name}"].to_numpy(dtype="float64") for name in coef
        ])
        for rname, spec in rows:
            s = row_series(c, spec)
            for flavor in ("raw", "ra"):
                for jan, mask in (("janincl", mask_all), ("janexcl", mask_exjan)):
                    col = f"{hz}_{flavor}_{jan}"
                    if flavor == "raw":
                        val, t = raw_mean_tstat(s, mask)
                    else:
                        val, t = ra_intercept_tstat(s, ff_arr, mask)
                    for kind, v in (("val", val), ("tstat", t)):
                        mname = (f"{col}_{rname}"
                                 + ("_tstat" if kind == "tstat" else ""))
                        paper, tol = targets[mname]
                        out[(col, rname, kind)] = (v, paper, tol,
                                                   tier(paper, v, tol))
    return out


def tally(grid: dict) -> dict:
    counts = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0}
    per_col = {col: {"Tier 1": 0, "Tier 2": 0, "FAIL": 0} for col in COLS}
    for (col, _row, _kind), (_v, _p, _tol, tr) in grid.items():
        counts[tr] += 1
        per_col[col][tr] += 1
    return {"total": counts, "per_col": per_col}


# --- bit-exact regression gates (Tables I and V) ------------------------------

def check_table_i(pre_sr: pd.DataFrame) -> tuple[bool, str]:
    """Re-run Tables I-III in memory under the official config (ret_dl) and
    compare the strategy-return series bit-exactly against the pre-experiment
    official data/strategy_returns.parquet."""
    b = tables_1_3.run(ret_col="ret_dl", write_outputs=False, verbose=False)
    ser = b["series"]
    sr_new = pd.DataFrame({
        "month": pre_sr["month"].to_numpy(),
        "jt_w": ser["jt"]["w"] * 100, "jt_l": ser["jt"]["l"] * 100,
        "jt_wl": ser["jt"]["wl"] * 100,
        "mg_w": ser["mg"]["w"] * 100, "mg_l": ser["mg"]["l"] * 100,
        "mg_wl": ser["mg"]["wl"] * 100,
        "wh_w": ser["wh"]["w"] * 100, "wh_l": ser["wh"]["l"] * 100,
        "wh_wl": ser["wh"]["wl"] * 100,
    })
    same = sr_new.equals(pre_sr)
    # Table I headline cells (percent; W-L mean + t-stat) for the report
    anchors = {}
    for k in ("jt_wl", "mg_wl", "wh_wl"):
        v = sr_new[k].to_numpy(dtype="float64")
        v = v[np.isfinite(v)]
        anchors[k] = (float(v.mean()),
                      float(v.mean() / (v.std(ddof=1) / np.sqrt(v.size))))
    return same, anchors


def check_table_v(pre_V: pd.DataFrame) -> tuple[bool, pd.DataFrame]:
    """Re-run Table V in memory under the official config (ret_dl) and return
    (bit-identical?, regenerated coeff frame)."""
    b = run_table(CFG_V, ret_col="ret_dl", write_outputs=False,
                  enforce_gate=True, verbose=False)
    new = b["coeff"].reset_index(drop=True)
    old = pre_V.reset_index(drop=True)
    same = new.equals(old)
    return same, new


# --- main -----------------------------------------------------------------------

def main() -> None:
    # 0. load the pre-experiment OFFICIAL caches (variant A; pre-rebuild panel)
    pre_sr = pd.read_parquet(intermediate_path("strategy_returns.parquet"))
    pre_V = pd.read_parquet(intermediate_path("fm_coefficients.parquet"))
    pre_VII = pd.read_parquet(intermediate_path("fm_coefficients_gh.parquet"))
    targets = load_targets("T7")

    # 1. regression gates: Tables I and V must be bit-identical (no g_gh use)
    print("=" * 78)
    print("BIT-EXACT REGRESSION GATES (Tables I and V; neither uses g_gh)")
    sr_same, t1_anchors = check_table_i(pre_sr)
    print(f"  Table I  strategy_returns.parquet bit-identical: {sr_same}")
    for k, (m, t) in t1_anchors.items():
        print(f"    {k}: mean {m:.4f} (t {t:.4f})")
    v_same, _ = check_table_v(pre_V)
    print(f"  Table V  fm_coefficients.parquet bit-identical: {v_same}")
    assert sr_same, ("Table I strategy_returns changed after the panel "
                     "rebuild — pre-existing columns are NOT bit-exact; "
                     "stop and diagnose")
    assert v_same, ("Table V fm_coefficients changed after the panel "
                    "rebuild — pre-existing columns are NOT bit-exact; "
                    "stop and diagnose")
    print("=" * 78)

    # 2. variant-A grid from the official cache (+ reconstruction validation)
    gridA = cells_from_coeff(pre_VII, CFG_VII.strat_sig, targets)
    tallA = tally(gridA)
    print(f"  variant A reconstruction: Tier 1 {tallA['total']['Tier 1']} / "
          f"Tier 2 {tallA['total']['Tier 2']} / FAIL {tallA['total']['FAIL']} "
          f"(official table_7.md: 122 / 102 / 16)")
    assert tallA["total"] == {"Tier 1": 122, "Tier 2": 102, "FAIL": 16}, (
        f"variant-A reconstruction does not match the official table_7.md "
        f"tally: {tallA['total']}")

    # 3. run Table VII under variant B (official dependent ret_dl; gate
    #    non-enforcing: the gate's GH-sign expectations are variant-A anchors)
    bundleB = run_table(CFG_VII_B, ret_col="ret_dl", write_outputs=True,
                        enforce_gate=False, verbose=True)
    gridB = bundleB["results"]
    tallB = {"total": bundleB["counts"], "per_col": bundleB["per_col"]}
    if bundleB["gate_problems"]:
        print("  variant-B preflight gate problems (recorded, not enforced):")
        for p in bundleB["gate_problems"]:
            print(f"    - {p}")

    # 4. wh_spread identity assertion (A vs B, 16 cells = 8 cols x val+tstat)
    wh_cells = []
    for col in COLS:
        for kind in ("val", "tstat"):
            a = gridA[(col, "wh_spread", kind)][0]
            b = gridB[(col, "wh_spread", kind)][0]
            wh_cells.append((col, kind, a, b))
    wh_identical = all(a == b for _c, _k, a, b in wh_cells)
    wh_maxdiff = max(abs(a - b) for _c, _k, a, b in wh_cells)
    wh_t1_B = sum(1 for col in COLS for kind in ("val", "tstat")
                  if gridB[(col, "wh_spread", kind)][3] == "Tier 1")
    print()
    print(f"WH_SPREAD IDENTITY (A vs B): bit-identical {wh_identical}; "
          f"max |A-B| = {wh_maxdiff:.3e}; Tier-1 cells under B: {wh_t1_B}/16")
    if not wh_identical:
        print("  NOTE (spec flag): the task spec expected identity because "
              "the WH signal does not use g_gh. The WH dummy MATRIX is indeed "
              "identical across A and B, but the FM regression is JOINT "
              "(GH/GL dummies are regressors in the same cross-sectional "
              "OLS), so by Frisch-Waugh the WH coefficients shift when the "
              "GH columns change. The substantive check is criterion 3 "
              "(all 16 cells stay Tier 1).")

    # 5. adoption criteria
    a1 = tallB["total"]["Tier 1"]
    a1_ok = a1 > tallA["total"]["Tier 1"]
    ghse_A = gridA[("s66_raw_janexcl", "gh_spread", "val")][0]
    ghse_B = gridB[("s66_raw_janexcl", "gh_spread", "val")][0]
    paper_ghse = gridB[("s66_raw_janexcl", "gh_spread", "val")][1]
    a2_ok = abs(ghse_B - paper_ghse) < abs(ghse_A - paper_ghse)
    a3_ok = wh_t1_B == 16
    adopt = a1_ok and a2_ok and a3_ok
    gl_A = gridA[("s66_raw_janexcl", "gh_loser", "val")][0]
    gl_B = gridB[("s66_raw_janexcl", "gh_loser", "val")][0]
    gl_t_B = gridB[("s66_raw_janexcl", "gh_loser", "tstat")][0]
    gsr_A = gridA[("s66_ra_janexcl", "gh_spread", "val")][0]
    gsr_B = gridB[("s66_ra_janexcl", "gh_spread", "val")][0]
    gsr_t_B = gridB[("s66_ra_janexcl", "gh_spread", "tstat")][0]

    print()
    print("ADOPTION CRITERIA (adopt B iff ALL hold)")
    print(f"  (1) total Table VII Tier 1: A {tallA['total']['Tier 1']} -> "
          f"B {a1}  -> {'PASS' if a1_ok else 'FAIL'}")
    print(f"  (2) gh_spread s66_raw_janexcl: A {ghse_A:.4f} -> B {ghse_B:.4f} "
          f"(paper {paper_ghse:.2f}); |B-paper| {abs(ghse_B - paper_ghse):.4f} "
          f"vs |A-paper| {abs(ghse_A - paper_ghse):.4f} "
          f"-> {'PASS' if a2_ok else 'FAIL'}")
    print(f"  (3) wh_spread cells Tier 1 under B: {wh_t1_B}/16 "
          f"-> {'PASS' if a3_ok else 'FAIL'}")
    print(f"  anchors: gh_loser s66_raw_janexcl {gl_A:+.4f} -> {gl_B:+.4f} "
          f"(t {gl_t_B:.2f}; paper -0.19); gh_spread s66_ra_janexcl "
          f"{gsr_A:.4f} -> {gsr_B:.4f} (t {gsr_t_B:.2f}; paper 0.55)")
    print(f"  RECOMMENDATION: {'ADOPT variant B' if adopt else 'KEEP variant A'}")

    # 6. append the before/after block to results/table_7_variantB.md
    L = ["", "---", "",
         "## Before/after: variant A (g_gh, official) vs variant B (g_gh_b)",
         "",
         "Variant A cells recomputed from the official "
         "`data/fm_coefficients_gh.parquet` with the identical engine "
         "functions (the auditor independently verified that cache -> 4dp in "
         "audit1.md; the reconstruction above also reproduces the official "
         f"tally {tallA['total']['Tier 1']}/{tallA['total']['Tier 2']}/"
         f"{tallA['total']['FAIL']}); variant B from this run "
         "(dependent `ret_dl`, same as the official Table VII).", ""]
    L += ["### Per-column tally (A vs B)", "",
          "| column | A: T1/T2/FAIL | B: T1/T2/FAIL |", "|---|---|---|"]
    for col in COLS:
        ca, cb = tallA["per_col"][col], tallB["per_col"][col]
        L.append(f"| {col} | {ca['Tier 1']}/{ca['Tier 2']}/{ca['FAIL']} "
                 f"| {cb['Tier 1']}/{cb['Tier 2']}/{cb['FAIL']} |")
    L.append(f"| **total** | **{tallA['total']['Tier 1']}/"
             f"{tallA['total']['Tier 2']}/{tallA['total']['FAIL']}** "
             f"| **{tallB['total']['Tier 1']}/{tallB['total']['Tier 2']}/"
             f"{tallB['total']['FAIL']}** |")

    L += ["", "### gh_* cells — all 8 columns (A vs B vs paper; values + t-stats)",
          "",
          "| column | row | paper | A | B | paper_t | A_t | B_t | tier_B | tier_t_B |",
          "|---|---|---:|---:|---:|---:|---:|---:|---|---|"]
    for col in COLS:
        for rname in GH_ROWS:
            va, pa, _t, _tra = gridA[(col, rname, "val")]
            vb, _pb, _tol, trb = gridB[(col, rname, "val")]
            vat, pat, _tt, _trat = gridA[(col, rname, "tstat")]
            vbt, _pt2, _tolt, trbt = gridB[(col, rname, "tstat")]
            L.append(f"| {col} | {rname} | {fmt(pa)} | {fmt(va)} | {fmt(vb)} "
                     f"| {fmt(pat)} | {fmt(vat)} | {fmt(vbt)} | {trb} "
                     f"| {trbt} |")

    L += ["", "### wh_spread identity assertion (A vs B, 16 cells)", ""]
    if wh_identical:
        L.append(f"**All 16 wh_spread cells are bit-identical between A and "
                 f"B (max |A-B| = {wh_maxdiff:.3e}).**")
    else:
        L.append(f"**NOT bit-identical: {sum(1 for _c, _k, a, b in wh_cells if a != b)}/16 "
                 f"cells differ; max |A-B| = {wh_maxdiff:.6f}.** Spec flag: "
                 "the task expected identity since the WH signal does not use "
                 "g_gh — the WH dummy matrix IS identical, but the FM "
                 "regression is joint (GH/GL dummies are regressors in the "
                 "same cross-sectional OLS), so by Frisch-Waugh the WH "
                 "coefficients shift when the GH columns change. Substantive "
                 f"check: {wh_t1_B}/16 wh_spread cells are Tier 1 under B.")
    L += ["", "| column | kind | A | B | \\|A-B\\| | identical | tier_B |",
          "|---|---|---:|---:|---:|---|---|"]
    for col, kind, a, b in wh_cells:
        trb = gridB[(col, "wh_spread", kind)][3]
        L.append(f"| {col} | wh_spread {kind} | {fmt(a)} | {fmt(b)} "
                 f"| {abs(a - b):.2e} | {a == b} | {trb} |")

    L += ["", "### Adoption criteria (audit1.md [M2])", "",
          "Adopt variant B iff ALL hold:", "",
          f"1. Total Table VII Tier-1 count rises above A's "
          f"{tallA['total']['Tier 1']}: **B = {a1}** "
          f"-> {'PASS' if a1_ok else 'FAIL'}.",
          f"2. gh_spread s66_raw_janexcl moves from {ghse_A:.4f} toward "
          f"{paper_ghse:.2f} (closer in absolute terms): **B = {ghse_B:.4f}**, "
          f"|B-paper| = {abs(ghse_B - paper_ghse):.4f} vs |A-paper| = "
          f"{abs(ghse_A - paper_ghse):.4f} -> {'PASS' if a2_ok else 'FAIL'}.",
          f"3. All 16 wh_spread cells remain Tier 1: **{wh_t1_B}/16** "
          f"-> {'PASS' if a3_ok else 'FAIL'}.", "",
          "Anchors:",
          f"- gh_loser s66_raw_janexcl: A {gl_A:+.4f} -> B {gl_B:+.4f} "
          f"(t {gl_t_B:.2f}; paper -0.19).",
          f"- gh_spread s66_ra_janexcl: A {gsr_A:.4f} -> B {gsr_B:.4f} "
          f"(t {gsr_t_B:.2f}; paper 0.55).", "",
          f"**Recommendation: {'ADOPT variant B' if adopt else 'KEEP variant A'}** "
          "(worker implements the pre-committed rule; the Replicator ratifies).",
          ""]
    if bundleB["gate_problems"]:
        L += ["Preflight gate problems under B (recorded, not enforced — the "
              "gate's GH anchors are variant-A Jan-incl expectations):", ""]
        for p in bundleB["gate_problems"]:
            L.append(f"- {p}")
        L.append("")

    md_path = LAYOUT.result_path(CFG_VII_B.md_name)
    md_path.write_text(md_path.read_text() + "\n".join(L))
    print(f"\nappended before/after block to {md_path}")


if __name__ == "__main__":
    main()
