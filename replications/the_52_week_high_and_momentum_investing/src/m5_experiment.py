"""
M5 adjudication experiment (audit1.md [M5], outer iteration 2 / inner 3):
MG industry-level cutoff sensitivity. The official MG sort (A8) ranks
individual stocks by their industry's 6-month cumulative VW return with a
permno-ordinal tie-break, arbitrarily splitting the boundary industry's
stocks across winner/middle/loser. The MG-intended reading: rank the 20
INDUSTRIES by their 6-month VW returns; winner = stocks in the top 6
industries, loser = stocks in the bottom 6 (boundary ties keep all members
of the tied industries).

The variant is implemented ADDITIVELY as:
  - tables_1_3.industry_cum_returns / industry_rank_groups /
    build_cohorts_industry (Table I EW machinery), and
  - tables_5.build_rank_sets_industry (FM dummy construction).
Industry cumrets are recomputed from the panel with the SAME VW formula as
the official pipeline (A7). The independent recompute differs from the
official per-stock mg_sig by <= 1e-3 in 4.6% of (industry, month) cells —
a switcher-membership artifact (stocks that change MG industry inside the
6-month window carry a mixed path in mg_sig); it cannot move the ranking
of the 20 industries (adjacent-industry cumret gaps are orders of
magnitude larger) and is immaterial to the variant.

Official defaults are untouched; this driver runs the variant and compares.

Run:
    cd <repo-root>
    REPLICATIONS_PATH=$PWD/replications \
    PYTHONPATH=$PWD:replications/the_52_week_high_and_momentum_investing/src \
    python3 replications/the_52_week_high_and_momentum_investing/src/m5_experiment.py

Outputs (additive only):
  - data/fm_coefficients_mg_ind.parquet   (industry-variant FM c_{k,t} series)
  - results/table_1_sensitivity_mg.md     (Table I under both MG variants,
                                           full grid + tie frequency + FM
                                           mg_spread before/after + adoption
                                           checks)

Official artifacts are NOT touched (results/table_1.md, table_5.md,
data/strategy_returns.parquet, data/fm_coefficients.parquet). The official
Tables I and V machinery is re-run IN MEMORY (write_outputs=False) as a
regression gate and compared bit-exactly against the on-disk official
caches (proves the additive functions leave the official path unchanged).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import tables_1_3
from m2_experiment import cells_from_coeff, tally
from tables_1_3 import (FORM_END, FORM_START, HOLD_END, HOLD_START, J,
                        build_cohorts, build_cohorts_industry,
                        formation_rows, industry_cum_returns, load_matrices,
                        mean_pct, strategy_pair, tstat)
from tables_5 import (CFG_V, COLS, JLIST, LAYOUT, PRIMARY_WH, SPREAD_ORDER,
                      build_rank_sets, build_rank_sets_industry, coef_names,
                      fmt, intermediate_path, load_ff, load_panel_matrices,
                      make_rows, ra_intercept_tstat, raw_mean_tstat, row_series,
                      run_horizon, run_table, tier)

N_TOP = N_BOT = 6          # MG: top/bottom 6 of the 20 industries
RET_COL = "ret_dl"         # official dependent (Table I + Table V)
T1_MG = ("mg_winner", "mg_loser", "mg_w_minus_l", "mg_w_minus_l_tstat")


# --- Table I under the industry-level variant --------------------------------

def table_i_variant(panel, grid, permnos, ret_mat, ind_cum, ind_w, f0, n_f,
                    hold0, n_hold, mask_all):
    cohorts, diag = build_cohorts_industry(panel, grid, ind_cum, ind_w,
                                           permnos, N_TOP, N_BOT)
    short = [(idx, n) for idx, n, _w, _l in diag if n < N_TOP + N_BOT]
    assert not short, f"formation months with <{N_TOP + N_BOT} industries: {short[:5]}"
    ser = strategy_pair(cohorts, f0, n_f, hold0, n_hold, permnos, ret_mat)
    sizes = {g: np.array([len(cohorts.get(f0 + k, {}).get(g, []))
                          for k in range(n_f)]) for g in "WML"}
    metrics = {
        "mg_winner": mean_pct(ser["w"], mask_all),
        "mg_loser": mean_pct(ser["l"], mask_all),
        "mg_w_minus_l": mean_pct(ser["wl"], mask_all),
        "mg_w_minus_l_tstat": tstat(ser["wl"][mask_all] * 100),
    }
    return ser, metrics, diag, sizes


# --- FM under the industry-level MG dummies -----------------------------------

def run_fm_variant(ind_cum, ind_w):
    """Table V engine with the mg slot replaced by the industry-level dummies
    (jt/wh official, same dependent ret_dl, same controls/sample/averaging)."""
    strat_sig = CFG_V.strat_sig
    coef = coef_names(strat_sig)
    I = {name: k for k, name in enumerate(coef)}
    rows = make_rows(strat_sig)
    targets = tables_1_3.load_targets()["T5"]

    panel, grid, permnos, dep_mat, ctrl_mat, mcap_mat = load_panel_matrices(RET_COL)
    ranks_off = build_rank_sets(panel, grid, permnos,
                                {"jt": "jt_sig", "wh": PRIMARY_WH})
    W_ind, L_ind, tie_diag = build_rank_sets_industry(grid, permnos, ind_cum,
                                                      ind_w, N_TOP, N_BOT)
    ranks = {"jt": ranks_off["jt"], "mg": (W_ind, L_ind), "wh": ranks_off["wh"]}

    hold0 = int(np.searchsorted(grid, HOLD_START.to_datetime64()))
    hold_end_i = int(np.searchsorted(grid, HOLD_END.to_datetime64()))
    hold_idx = np.arange(hold0, hold_end_i + 1)
    assert len(hold_idx) == 462
    hold_months = pd.DatetimeIndex(grid[hold_idx])
    mo = hold_months.month.to_numpy()
    mask_all = np.ones(len(hold_idx), dtype=bool)
    mask_exjan = mo != 1

    ff = load_ff()
    ff_arr = ff.set_index("month").reindex(hold_months)[
        ["mkt_rf", "smb", "hml"]].to_numpy(dtype="float64")
    assert np.isfinite(ff_arr).all()

    c_by_horizon, diag = {}, {}
    for hz, jlist in JLIST.items():
        c, ss, nreg, _rs = run_horizon(jlist, hold_idx, dep_mat, ctrl_mat,
                                       mcap_mat, ranks, list(strat_sig))
        assert c.shape[1] == len(coef)
        c_by_horizon[hz] = c
        diag[hz] = {"avg_sample": float(ss.mean()), "n_reg": int(nreg)}

    coeff = pd.DataFrame({"month": hold_months})
    for hz, c in c_by_horizon.items():
        for k, name in enumerate(coef):
            coeff[f"{hz}_{name}"] = c[:, k]
        for s in SPREAD_ORDER:
            if s in strat_sig:
                coeff[f"{hz}_{s}_spread"] = (c[:, I[f"{s}_winner"]]
                                             - c[:, I[f"{s}_loser"]])
    coeff.to_parquet(intermediate_path("fm_coefficients_mg_ind.parquet"),
                     index=False)

    gridM = {}
    for hz in ("s66", "s612"):
        c = c_by_horizon[hz]
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
                        gridM[(col, rname, kind)] = (v, paper, tol,
                                                     tier(paper, v, tol))
    return gridM, diag, tie_diag, hold0, hold_end_i


def main() -> None:
    # 0. official caches
    pre_sr = pd.read_parquet(intermediate_path("strategy_returns.parquet"))
    pre_V = pd.read_parquet(intermediate_path("fm_coefficients.parquet"))
    t1 = tables_1_3.load_targets()["T1"]
    targets5 = tables_1_3.load_targets()["T5"]
    gridA = cells_from_coeff(pre_V, CFG_V.strat_sig, targets5)
    tallA = tally(gridA)
    assert tallA["total"] == {"Tier 1": 150, "Tier 2": 42, "FAIL": 0}, tallA

    # 1. regression gates: official Tables I and V reproduce bit-exactly in
    #    memory after the additive edits (new functions, official defaults)
    print("=" * 78)
    b1 = tables_1_3.run(ret_col=RET_COL, write_outputs=False, verbose=False)
    ser = b1["series"]
    sr_new = pd.DataFrame({
        "month": pre_sr["month"].to_numpy(),
        "jt_w": ser["jt"]["w"] * 100, "jt_l": ser["jt"]["l"] * 100,
        "jt_wl": ser["jt"]["wl"] * 100,
        "mg_w": ser["mg"]["w"] * 100, "mg_l": ser["mg"]["l"] * 100,
        "mg_wl": ser["mg"]["wl"] * 100,
        "wh_w": ser["wh"]["w"] * 100, "wh_l": ser["wh"]["l"] * 100,
        "wh_wl": ser["wh"]["wl"] * 100,
    })
    sr_same = sr_new.equals(pre_sr)
    print(f"REGRESSION GATE: Table I strategy_returns bit-identical: {sr_same}")
    assert sr_same, "Table I changed after the additive edit; diagnose"
    b5 = run_table(CFG_V, ret_col=RET_COL, write_outputs=False, verbose=False)
    v_same = b5["coeff"].reset_index(drop=True).equals(pre_V.reset_index(drop=True))
    print(f"REGRESSION GATE: Table V fm_coefficients bit-identical: {v_same}")
    assert v_same, "Table V changed after the additive edit; diagnose"
    print("=" * 78)

    off_mg = {r["name"]: r for r in b1["rows1"] if r["name"].startswith("mg_")}

    # 2. industry cumrets (recomputed from the panel; A7 VW formula) + Table I
    panel, grid, permnos, ret_mat = load_matrices(RET_COL)
    ind_cum, ind_w = industry_cum_returns(panel, grid)
    f0 = int(np.searchsorted(grid, FORM_START.to_datetime64()))
    hold0 = int(np.searchsorted(grid, HOLD_START.to_datetime64()))
    hold_end_i = int(np.searchsorted(grid, HOLD_END.to_datetime64()))
    n_hold = hold_end_i - hold0 + 1
    n_f = n_hold + J - 1
    mask_all = np.ones(n_hold, dtype=bool)

    ser_ind, met_ind, diag_ind, sizes_ind = table_i_variant(
        panel, grid, permnos, ret_mat, ind_cum, ind_w, f0, n_f, hold0,
        n_hold, mask_all)

    # official mg cohort sizes (30/30 ordinal split) for comparison
    months, pnos, sigs = formation_rows(panel, "mg_sig")
    coh_off, _ = build_cohorts(months, pnos, sigs, grid)
    sizes_off = {g: np.array([len(coh_off.get(f0 + k, {}).get(g, []))
                              for k in range(n_f)]) for g in "WML"}

    # rankable-set overlap: variant (industry(f) + cumret finite) vs official
    # (mg_sig non-null), over the 467 formation months
    mg_w = np.full((len(permnos), len(grid)), np.nan)
    mi = np.searchsorted(np.asarray(grid), panel["month"].to_numpy())
    pi = np.searchsorted(permnos, panel["permno"].to_numpy())
    mg_w[pi, mi] = panel["mg_sig"].to_numpy(dtype="float64")
    n_var = n_off = n_both = 0
    for k in range(n_f):
        f = f0 + k
        var = np.isfinite(ind_w[:, f]) & np.isfinite(ind_cum[np.where(np.isfinite(ind_w[:, f]), ind_w[:, f], 0).astype(int), f])
        off = np.isfinite(mg_w[:, f])
        n_var += int(var.sum()); n_off += int(off.sum())
        n_both += int((var & off).sum())
    overlap = n_both / max(n_var, 1)

    n_tie_w_t1 = sum(1 for _i, _n, w, _l in diag_ind if w > 0)
    n_tie_l_t1 = sum(1 for _i, _n, _w, l in diag_ind if l > 0)
    min_ind_t1 = min(n for _i, n, _w, _l in diag_ind)
    n_industries_t1 = float(np.mean([n for _i, n, _w, _l in diag_ind]))

    print("\nTABLE I — MG official (ordinal 30/30) vs industry-level "
          "(top/bottom 6 of 20)")
    for name in T1_MG:
        paper, tol = t1[name][0], t1[name][1]
        o = off_mg[name]["ours"]
        v = met_ind[name]
        print(f"  {name:22s} paper {paper:7.4f}  official {o:8.4f} "
              f"({tier(paper, o, tol)})  industry {v:8.4f} ({tier(paper, v, tol)})")
    print(f"  industry-tie frequency (467 formation months): winner-boundary "
          f"ties {n_tie_w_t1}, loser-boundary ties {n_tie_l_t1}; industries "
          f"per month mean {n_industries_t1:.1f}, min {min_ind_t1}")
    print(f"  rankable-set overlap (formation window): variant {n_var / n_f:.0f}/mo "
          f"vs official {n_off / n_f:.0f}/mo; {overlap * 100:.1f}% of the "
          f"variant set also mg_sig-rankable")
    print(f"  avg cohort size: official W {sizes_off['W'].mean():.1f} / L "
          f"{sizes_off['L'].mean():.1f}; industry W {sizes_ind['W'].mean():.1f} "
          f"/ M {sizes_ind['M'].mean():.1f} / L {sizes_ind['L'].mean():.1f}")

    # 3. FM under the industry-level MG dummies
    gridM, fm_diag, fm_tie_diag, fm_hold0, fm_hold_end_i = run_fm_variant(
        ind_cum, ind_w)
    fm_f = list(range(fm_hold0 - 13, fm_hold_end_i - 2 + 1))
    fm_months_tied = sum(1 for f in fm_f
                         if fm_tie_diag[f][1] > 0 or fm_tie_diag[f][2] > 0)
    fm_short = [f for f in fm_f if fm_tie_diag[f][0] < N_TOP + N_BOT]
    print(f"\nFM formation grid ({len(fm_f)} months): tie-boundary months "
          f"{fm_months_tied}; months with <12 industries: {len(fm_short)}")

    print("\nFM mg_spread before/after")
    for col in ("s66_raw_janincl", "s66_raw_janexcl"):
        a, at = (gridA[(col, "mg_spread", "val")][0],
                 gridA[(col, "mg_spread", "tstat")][0])
        m, mt = (gridM[(col, "mg_spread", "val")][0],
                 gridM[(col, "mg_spread", "tstat")][0])
        p = gridA[(col, "mg_spread", "val")][1]
        print(f"  {col:18s} official {a:7.4f} (t {at:5.2f})  industry "
              f"{m:7.4f} (t {mt:5.2f})  paper {p:5.2f}")

    # 4. MG-weakest check in every column (official + variant)
    weak = {}
    print("\nMG-WEAKEST CHECK (mg_spread < jt_spread AND mg_spread < wh_spread)")
    for col in COLS:
        oa = {s: gridA[(col, f"{s}_spread", "val")][0] for s in ("wh", "jt", "mg")}
        va = {s: gridM[(col, f"{s}_spread", "val")][0] for s in ("wh", "jt", "mg")}
        o_weak = oa["mg"] < min(oa["wh"], oa["jt"])
        v_weak = va["mg"] < min(va["wh"], va["jt"])
        weak[col] = (o_weak, v_weak)
        print(f"  {col:18s} official WH {oa['wh']:+.4f} JT {oa['jt']:+.4f} "
              f"MG {oa['mg']:+.4f} MG-weakest {o_weak} | industry WH "
              f"{va['wh']:+.4f} JT {va['jt']:+.4f} MG {va['mg']:+.4f} "
              f"MG-weakest {v_weak}")
    v_weak_all = all(w[1] for w in weak.values())
    o_weak_all = all(w[0] for w in weak.values())

    # 5. adoption checks
    wl_paper = t1["mg_w_minus_l"][0]
    wl_off = off_mg["mg_w_minus_l"]["ours"]
    wl_ind = met_ind["mg_w_minus_l"]
    gap_off = abs(wl_off - wl_paper)
    gap_ind = abs(wl_ind - wl_paper)
    c1_ok = gap_ind < gap_off
    c2_ok = v_weak_all
    adopt = c1_ok and c2_ok
    print("\nADOPTION CHECKS (adopt the industry-level variant iff BOTH hold)")
    print(f"  [C1] |mg_w_minus_l - paper|: official {gap_off:.4f} vs industry "
          f"{gap_ind:.4f} -> {'PASS (gap shrinks)' if c1_ok else 'FAIL'}")
    print(f"  [C2] MG weakest in all 8 columns under the variant: "
          f"{v_weak_all} (official: {o_weak_all}) -> "
          f"{'PASS' if c2_ok else 'FAIL'}")
    print(f"  => {'ADOPT the industry-level MG variant' if adopt else 'KEEP the official ordinal MG sort (A8)'}")

    # 6. write results/table_1_sensitivity_mg.md
    jt_rows = {r["name"]: r for r in b1["rows1"] if r["name"].startswith("jt_")}
    wh_rows = {r["name"]: r for r in b1["rows1"] if r["name"].startswith("wh_")}
    L = [
        "# Table I sensitivity — MG industry-level cutoff variant (audit1.md [M5])",
        "",
        "Official MG sort (A8): rank individual STOCKS by their industry's 6-month",
        "cumulative VW return with a permno-ordinal tie-break -> the boundary",
        "industry's stocks are arbitrarily split across winner/middle/loser.",
        f"Variant (MG-intended reading): rank the 20 INDUSTRIES by their 6-month",
        f"cumulative VW return; winner = stocks in the top {N_TOP} industries, loser =",
        f"stocks in the bottom {N_BOT}; boundary ties keep ALL members of the tied",
        "industries (inclusive cutoffs). Industry cumrets recomputed from the panel",
        "with the same VW formula as the official pipeline (A7, lagged-mcap weights,",
        "6 consecutive months). Same EW (6,6) machinery, dependent `ret_dl`.",
        "",
        "Note: the independent recompute of industry cumrets differs from the",
        "official per-stock mg_sig by <= 1e-3 in 4.6% of (industry, month) cells —",
        "a switcher-membership artifact (stocks changing MG industry inside the",
        "6-month window carry a mixed path in mg_sig); immaterial to the ranking of",
        "the 20 industries (adjacent-industry cumret gaps are orders of magnitude",
        "larger). Official mg pipeline untouched.",
        "",
        "## Table I full grid — both MG variants (jt/wh rows identical by construction)",
        "",
        "| metric | paper | official (ordinal 30/30) | tier | industry-level | tier |",
        "|---|---:|---:|---|---:|---|",
    ]
    for name, r in {**jt_rows, **off_mg, **wh_rows}.items():
        paper, tol, o = r["paper"], r["tol"], r["ours"]
        to = tier(paper, o, tol)
        if name.startswith("mg_"):
            v = met_ind[name]
            L.append(f"| {name} | {fmt(paper)} | {fmt(o)} | {to} | {fmt(v)} "
                     f"| {tier(paper, v, tol)} |")
        else:
            L.append(f"| {name} | {fmt(paper)} | {fmt(o)} | {to} | {fmt(o)} | {to} |")
    L += [
        "",
        "## Industry-tie frequency and cohort sizes",
        "",
        f"- Table I formation window ({FORM_START.date()} .. {FORM_END.date()}, "
        f"467 months): winner-boundary ties in **{n_tie_w_t1}** months, "
        f"loser-boundary ties in **{n_tie_l_t1}** months (a boundary tie = an "
        "industry exactly tied with the 6th-ranked industry; all its members stay in).",
        f"- Industries ranked per formation month: mean {n_industries_t1:.1f}, "
        f"min {min_ind_t1} (20 = all MG industries present).",
        f"- FM formation grid ({len(fm_f)} months, f = t-j, j=2..13): "
        f"**{fm_months_tied}** months with a boundary tie; {len(fm_short)} months "
        f"with <{N_TOP + N_BOT} industries.",
        f"- Avg cohort members: official ordinal split W {sizes_off['W'].mean():.1f} "
        f"/ M {sizes_off['M'].mean():.1f} / L {sizes_off['L'].mean():.1f} (forced "
        f"30/30); industry-level W {sizes_ind['W'].mean():.1f} / M "
        f"{sizes_ind['M'].mean():.1f} / L {sizes_ind['L'].mean():.1f} (members of "
        f"6/8/6 industries).",
        f"- Rankable-set overlap: variant (industry at f defined + cumret finite) "
        f"{n_var / n_f:.0f} stocks/month vs official (mg_sig non-null) "
        f"{n_off / n_f:.0f}; {overlap * 100:.1f}% of the variant set is also "
        f"mg_sig-rankable (the remainder = stocks that switch industry inside the "
        f"window, rankable at f but not over the full 6 months).",
        "",
        "## FM mg_spread before/after (industry-level variant; Table V layout, "
        "dependent `ret_dl`, all 8 columns)",
        "",
        "| column | official (A8 ordinal) | industry-level | paper |",
        "|---|---:|---:|---:|",
    ]
    for col in COLS:
        a, at = (gridA[(col, "mg_spread", "val")][0],
                 gridA[(col, "mg_spread", "tstat")][0])
        m, mt = (gridM[(col, "mg_spread", "val")][0],
                 gridM[(col, "mg_spread", "tstat")][0])
        p = gridA[(col, "mg_spread", "val")][1]
        L.append(f"| {col} | {fmt(a)} (t {fmt(at,2)}) | {fmt(m)} (t {fmt(mt,2)}) "
                 f"| {fmt(p)} |")
    L += [
        "",
        "Anchors: s66_raw_janincl official 0.3804 vs paper 0.25; s66_raw_janexcl "
        "official 0.3573 vs paper 0.22.",
        "",
        "## MG-weakest check (mg_spread < jt_spread AND mg_spread < wh_spread, "
        "all 8 columns)",
        "",
        "| column | official WH/JT/MG | MG weakest? | industry WH/JT/MG | MG weakest? |",
        "|---|---|---|---|---|",
    ]
    for col in COLS:
        oa = {s: gridA[(col, f"{s}_spread", "val")][0] for s in ("wh", "jt", "mg")}
        va = {s: gridM[(col, f"{s}_spread", "val")][0] for s in ("wh", "jt", "mg")}
        L.append(f"| {col} | {oa['wh']:+.4f} / {oa['jt']:+.4f} / {oa['mg']:+.4f} "
                 f"| {'yes' if weak[col][0] else 'NO'} | {va['wh']:+.4f} / "
                 f"{va['jt']:+.4f} / {va['mg']:+.4f} | "
                 f"{'yes' if weak[col][1] else 'NO'} |")
    L += [
        "",
        "NOTE: the FM regression is JOINT — changing the mg dummies shifts the "
        "jt/wh coefficients slightly (Frisch-Waugh; same effect as the M2 "
        "variant-B note), so the industry-column WH/JT values differ marginally "
        "from the official table_5.md.",
        "",
        "## Adoption checks (Replicator to ratify)",
        "",
        "Rule: adopt the industry-level variant iff BOTH:",
        "",
        f"1. the MG gap vs the paper shrinks: |mg_w_minus_l − {wl_paper:.2f}| "
        f"official {gap_off:.4f} vs industry {gap_ind:.4f} -> "
        f"{'PASS' if c1_ok else 'FAIL'};",
        f"2. MG remains the weakest strategy in EVERY Table V column under the "
        f"variant ({'8/8' if v_weak_all else 'NOT all 8'}) -> "
        f"{'PASS' if c2_ok else 'FAIL'}.",
        "",
        f"**Recommendation: {'ADOPT the industry-level MG variant (Replicator '
        'regenerates the official tables)' if adopt else 'KEEP the official '
        'ordinal MG sort (A8); document the MG offset as a tie-break/SIC-vintage '
        'effect (non-actionable)'}**",
        "",
        "Official artifacts untouched: results/table_1.md, results/table_5.md, "
        "data/strategy_returns.parquet, data/fm_coefficients.parquet. Variant "
        "c-series: data/fm_coefficients_mg_ind.parquet.",
    ]
    out = LAYOUT.result_path("table_1_sensitivity_mg.md")
    out.write_text("\n".join(L))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
