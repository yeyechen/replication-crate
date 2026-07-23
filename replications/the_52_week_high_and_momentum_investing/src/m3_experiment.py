"""
M3 adjudication experiment (audit1.md [M3], outer iteration 2 / inner 3):
the pre-registered A13 sensitivity — re-estimate Table V restricting EACH
(t,j) cross-section to stocks rankable on jt_sig AND mg_sig AND wh_sig_dc
SIMULTANEOUSLY at formation f = t-j (dummies re-built on that common
rankable cross-section with the same 30/30 ordinal convention; controls,
dependent `ret_dl`, j-averaging, Jan split and FF3 RA unchanged). Compare
against the OFFICIAL run WITHOUT overwriting any official artifact.

Run:
    cd <repo-root>
    REPLICATIONS_PATH=$PWD/replications \
    PYTHONPATH=$PWD:replications/the_52_week_high_and_momentum_investing/src \
    python3 replications/the_52_week_high_and_momentum_investing/src/m3_experiment.py

Outputs (additive only):
  - data/fm_coefficients_rankable.parquet     (rankable-only c_{k,t} series)
  - results/table_5_sensitivity_rankable.md   (full 12x8 grid under the
                                               restricted sample + before/
                                               after anchor block + dominance
                                               ordering + adoption checks)

Official artifacts are NOT touched (results/table_5.md and
data/fm_coefficients.parquet stay the audit-verified official run). The
official Table V is re-run IN MEMORY (write_outputs=False) as a regression
gate and compared bit-exactly against the on-disk official cache — this
proves the additive engine changes (build_rank_sets/rankable_only,
run_horizon/sample_mat) leave the official path bit-identical.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from m2_experiment import cells_from_coeff, tally
from tables_5 import (CFG_V, COLS, LAYOUT, TableConfig, fmt, intermediate_path,
                      load_targets, run_table)

# Table V under the A13 rankable-only restriction. Everything identical to
# CFG_V except the output names (official artifacts stay intact) and the
# rankable_only flag handled by run_table/run_horizon/build_rank_sets.
CFG_V_RANK = TableConfig(
    table_id="T5",
    strat_sig=CFG_V.strat_sig,
    coeff_parquet="fm_coefficients_rankable.parquet",
    md_name="table_5_sensitivity_rankable.md",
    title=("# Table V (A13 rankable-only sensitivity) — George & Hwang (2004): "
           "FM cross-sections restricted to stocks rankable on jt AND mg AND "
           "wh simultaneously (audit1.md [M3])"),
    dummy_pairs=("JH/JL<-jt_sig, MH/ML<-mg_sig, FHH/FHL<-wh_sig_dc "
                 "(30/30 on the common rankable cross-section)"),
    preflight_rows=CFG_V.preflight_rows,
    paper_preflight=CFG_V.paper_preflight,
)

ANCHORS = ["wh_loser", "wh_winner", "wh_spread", "jt_spread", "mg_spread",
           "intercept"]
SPREADS = ("wh_spread", "jt_spread", "mg_spread")


def ordering(grid: dict, col: str) -> str:
    """Dominance ordering string (e.g. 'JT>WH>MG') from the spread values."""
    vals = {s.split("_")[0]: grid[(col, s, "val")][0] for s in SPREADS}
    return ">".join(k.upper() for k, _ in sorted(vals.items(),
                                                 key=lambda kv: -kv[1]))


def main() -> None:
    targets = load_targets("T5")

    # 0. official cache -> official grid (the audit verified this cache -> 4dp)
    pre_V = pd.read_parquet(intermediate_path("fm_coefficients.parquet"))
    gridA = cells_from_coeff(pre_V, CFG_V.strat_sig, targets)
    tallA = tally(gridA)
    print("=" * 78)
    print(f"OFFICIAL reconstruction from cache: Tier 1 {tallA['total']['Tier 1']} "
          f"/ Tier 2 {tallA['total']['Tier 2']} / FAIL {tallA['total']['FAIL']} "
          f"(official table_5.md: 150 / 42 / 0)")
    assert tallA["total"] == {"Tier 1": 150, "Tier 2": 42, "FAIL": 0}, tallA
    print("=" * 78)

    # 1. regression gate: official Table V must reproduce bit-exactly in
    #    memory after the additive engine edits (default-off parameters)
    b_off = run_table(CFG_V, ret_col="ret_dl", write_outputs=False,
                      verbose=False)
    same = b_off["coeff"].reset_index(drop=True).equals(pre_V.reset_index(drop=True))
    print(f"REGRESSION GATE: official CFG_V in-memory coeff bit-identical to "
          f"on-disk fm_coefficients.parquet: {same}")
    assert same, ("official Table V changed after the engine edit — the "
                  "additive parameters are NOT default-off; stop and diagnose")

    # 2. the A13 rankable-only re-estimation (writes the NEW parquet + md)
    b_rk = run_table(CFG_V_RANK, ret_col="ret_dl", write_outputs=True,
                     verbose=True, rankable_only=True)
    gridR = b_rk["results"]
    tallR = {"total": b_rk["counts"], "per_col": b_rk["per_col"]}

    # 3. sample-size cost
    off_avg = b_off["diag"]["s66"]["avg_sample"]
    rk_avg = np.mean([b_rk["diag"][hz]["avg_reg_sample"] for hz in ("s66", "s612")])
    rk_min = min(b_rk["diag"][hz]["min_reg_sample"] for hz in ("s66", "s612"))
    rk_max = max(b_rk["diag"][hz]["max_reg_sample"] for hz in ("s66", "s612"))
    n_reg_rk = {hz: b_rk["diag"][hz]["n_reg"] for hz in ("s66", "s612")}
    print(f"\nSAMPLE-SIZE COST: official avg cross-section {off_avg:.1f} -> "
          f"rankable-only avg {rk_avg:.1f} (min {rk_min}, max {rk_max}) per "
          f"(t,j) regression; {rk_avg / off_avg * 100:.1f}% retained")
    all3 = b_rk["rankable"].get("all3", {})
    print("  all-three-rankable stocks / formation month (avg by decade): "
          + "  ".join(f"{d} {v:7.1f}" for d, v in sorted(all3.items())))

    # 4. adoption checks
    c1_cols = ["s66_raw_janincl", "s612_raw_janincl"]
    c1 = {col: (gridR[(col, "wh_spread", "val")][0],
                gridR[(col, "jt_spread", "val")][0]) for col in c1_cols}
    c1_ok = all(wh > jt for wh, jt in c1.values())
    wh_t1_R = sum(1 for col in COLS
                  if gridR[(col, "wh_spread", "val")][3] == "Tier 1")
    c2_ok = wh_t1_R == len(COLS)
    c3_ok = tallR["total"]["Tier 1"] >= tallA["total"]["Tier 1"]
    adopt = c1_ok and c2_ok and c3_ok

    print("\nADOPTION CHECKS (adopt rankable-only iff ALL hold)")
    for col in c1_cols:
        wh, jt = c1[col]
        print(f"  [C1] {col}: WH {wh:.4f} {'>' if wh > jt else '<='} JT "
              f"{jt:.4f} -> {'PASS' if wh > jt else 'FAIL'}")
    print(f"  [C2] wh_spread Tier-1 cells under rankable-only: {wh_t1_R}/8 "
          f"-> {'PASS' if c2_ok else 'FAIL'}")
    print(f"  [C3] total Tier-1: official {tallA['total']['Tier 1']} vs "
          f"rankable-only {tallR['total']['Tier 1']} -> "
          f"{'PASS' if c3_ok else 'FAIL'}")
    print(f"  => {'ADOPT rankable-only as official' if adopt else 'KEEP the official sample'}")

    # 5. extend the md (run_table already wrote the standard 12x8 grid)
    md_path = LAYOUT.result_path(CFG_V_RANK.md_name)
    L = [md_path.read_text(),
         "",
         "---",
         "",
         "## Before/after vs the official sample (audit1.md [M3]; official = "
         "audit-verified data/fm_coefficients.parquet)",
         "",
         "Anchor rows: wh_loser, wh_winner, wh_spread, jt_spread, mg_spread, "
         "intercept. Format: value (t-stat).",
         ""]
    for col in COLS:
        L += [f"### Column: {col}", "",
              "| row | official | rankable-only | paper |",
              "|---|---:|---:|---:|"]
        for rname in ANCHORS:
            a = gridA[(col, rname, "val")][0]
            at = gridA[(col, rname, "tstat")][0]
            r = gridR[(col, rname, "val")][0]
            rt = gridR[(col, rname, "tstat")][0]
            p = gridA[(col, rname, "val")][1]
            L.append(f"| {rname} | {fmt(a)} ({fmt(at,2)}) | {fmt(r)} ({fmt(rt,2)}) "
                     f"| {fmt(p)} |")
        off_o = ordering(gridA, col)
        rk_o = ordering(gridR, col)
        pp = {s.split("_")[0]: gridA[(col, s, "val")][1] for s in SPREADS}
        paper_o = ">".join(k.upper() for k, _ in sorted(pp.items(),
                                                        key=lambda kv: -kv[1]))
        L += ["",
              f"**Dominance ordering — {col}:** official {off_o} | "
              f"rankable-only {rk_o} | paper {paper_o}",
              ""]

    L += ["## Sample-size cost", "",
          f"- Official avg cross-section n per (t,j) regression: **{off_avg:.1f}** "
          f"(per holding month; table_5.md diagnostic).",
          f"- Rankable-only avg restricted cross-section n per (t,j) regression: "
          f"**{rk_avg:.1f}** (min {rk_min}, max {rk_max}) = "
          f"{rk_avg / off_avg * 100:.1f}% of the official sample.",
          f"- Regressions actually fit: s66 {n_reg_rk['s66']}/2772, "
          f"s612 {n_reg_rk['s612']}/5544 (official: all).",
          "- All-three-rankable stocks / formation month (avg by decade): "
          + " | ".join(f"{d} {v:.1f}" for d, v in sorted(all3.items())),
          "",
          "## Adoption checks (Replicator to ratify)",
          "",
          "Rule: adopt the rankable-only sample as official iff ALL of:",
          "",
          "1. WH > JT restored in BOTH Jan-included raw columns (s66, s612);",
          "2. every wh_spread cell (8 columns, values) stays Tier 1;",
          "3. the total Table V Tier-1 count does not degrade "
          f"(official {tallA['total']['Tier 1']}).",
          ""]
    for col in c1_cols:
        wh, jt = c1[col]
        L.append(f"- [C1] {col}: rankable-only wh_spread {fmt(wh)} vs jt_spread "
                 f"{fmt(jt)} -> WH {fmt(wh)} {'>' if wh > jt else '<='} JT "
                 f"{'PASS' if wh > jt else 'FAIL'}")
    L.append(f"- [C2] wh_spread Tier-1 cells under rankable-only: {wh_t1_R}/8 -> "
             f"{'PASS' if c2_ok else 'FAIL'}")
    L.append(f"- [C3] total Tier-1: official {tallA['total']['Tier 1']} vs "
             f"rankable-only {tallR['total']['Tier 1']} (T2 "
             f"{tallR['total']['Tier 2']}, FAIL {tallR['total']['FAIL']}) -> "
             f"{'PASS' if c3_ok else 'FAIL'}")
    L += ["",
          f"**Recommendation: {'ADOPT the rankable-only sample as official '
          '(Replicator regenerates table_5.md)' if adopt else 'KEEP the '
          'official sample; document the Jan-included raw inversion as a '
          'vintage effect (non-actionable)'}**",
          "",
          f"Hit rate under rankable-only: Tier 1 {tallR['total']['Tier 1']} / "
          f"Tier 2 {tallR['total']['Tier 2']} / FAIL {tallR['total']['FAIL']} "
          f"of 192 (official: {tallA['total']['Tier 1']} / "
          f"{tallA['total']['Tier 2']} / {tallA['total']['FAIL']}).",
          "",
          "### Per-column tally (rankable-only)",
          "",
          "| column | Tier 1 | Tier 2 | FAIL |",
          "|---|---:|---:|---:|"]
    for col in COLS:
        cc = tallR["per_col"][col]
        L.append(f"| {col} | {cc['Tier 1']} | {cc['Tier 2']} | {cc['FAIL']} |")
    md_path.write_text("\n".join(L))
    print(f"\nwrote {md_path}")


if __name__ == "__main__":
    main()
