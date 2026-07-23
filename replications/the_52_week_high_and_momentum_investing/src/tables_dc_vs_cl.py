"""
George & Hwang (2004) — FOCUSED diagnostic: 52-week-high signal granularity.

Compares the two 52-week-high price-series granularities for the Table I 52WH
rows (4 metrics) and the FULL Table III (48 cells):
  - wh_sig_cl : |prc(f)| / max of MSF MONTH-END closes over f-11..f
  - wh_sig_dc : |prc(f)| / max of DSF DAILY closes over f-11..f
                (the literal "highest price achieved during the 12-month
                period" reading of L122)

EVERYTHING ELSE is held identical: same jt_sig outer rankings, same 30/40/30
sorts, same (6,6) timing, same nonempty-cell W-L rule (footnote 6). The only
thing that changes is the inner 52WH ranking signal. Reuses all machinery from
tables_1_3.py (this file imports it; it does not re-implement the sorts).

Writes results/table_3_dc_vs_cl.md: side-by-side per-cell comparison
(paper | cl | dc | |err_cl| | |err_dc| | tier_cl | tier_dc), per-variant
hit-rate summaries, total |deviation| across the 48+4 cells, and a
recommendation for which variant to lock as the single primary 52WH signal.

This script does NOT modify tables_1_3.py's outputs (table_1/2/3.md); those
are regenerated separately under whichever variant is locked.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import tables_1_3 as t13

CL = "wh_sig_cl"
DC = "wh_sig_dc"


def cohorts_for(panel: pd.DataFrame, grid, sig: str):
    months, pnos, sigs = t13.formation_rows(panel, sig)
    cohorts, _ = t13.build_cohorts(months, pnos, sigs, grid)
    return cohorts


def t1_wh_rows(cohorts: dict, f0, n_f, hold0, n_hold, permnos, ret_mat,
               mask_all, t1) -> list[dict]:
    """The 4 Table I 52WH metrics (winner, loser, w_minus_l, w_minus_l_tstat)
    under a given 52WH signal's cohorts."""
    s = t13.strategy_pair(cohorts, f0, n_f, hold0, n_hold, permnos, ret_mat)
    return [
        {"name": "wh_winner", "paper": t1["wh_winner"][0],
         "ours": t13.mean_pct(s["w"], mask_all), "tol": t1["wh_winner"][1]},
        {"name": "wh_loser", "paper": t1["wh_loser"][0],
         "ours": t13.mean_pct(s["l"], mask_all), "tol": t1["wh_loser"][1]},
        {"name": "wh_w_minus_l", "paper": t1["wh_w_minus_l"][0],
         "ours": t13.mean_pct(s["wl"], mask_all), "tol": t1["wh_w_minus_l"][1]},
        {"name": "wh_w_minus_l_tstat", "paper": t1["wh_w_minus_l_tstat"][0],
         "ours": t13.tstat(s["wl"][mask_all] * 100),
         "tol": t1["wh_w_minus_l_tstat"][1]},
    ]


def table3_rows(jt_coh: dict, wh_coh: dict, f_indices, f0, n_f, hold0, n_hold,
                permnos, ret_mat, mask_all, mask_exjan, t3) -> list[dict]:
    """All 48 Table III cells under a given 52WH signal's cohorts, in the SAME
    order as tables_1_3.main() (Panel A then Panel B)."""
    cells = t13.intersection_cells(jt_coh, wh_coh, f_indices)
    cell_ser = {
        key: t13.cell_series(members, f0, n_f, hold0, n_hold, permnos, ret_mat)
        for key, members in cells.items()
    }

    def cell_mean(jg, wg, mask):
        return t13.mean_pct(cell_ser[(jg, wg)][0], mask)

    rows: list[dict] = []
    for outer in ("W", "M", "L"):
        o_name = {"W": "winner", "M": "middle", "L": "loser"}[outer]
        for col, inner in (("winner", "W"), ("loser", "L")):
            for suffix, mask in (("all", mask_all), ("exjan", mask_exjan)):
                nm = f"pa_{o_name}_{col}_{suffix}"
                rows.append({"name": nm, "paper": t3[nm][0],
                             "ours": cell_mean(outer, inner, mask), "tol": t3[nm][1]})
        for suffix, mask in (("all", mask_all), ("exjan", mask_exjan)):
            nm = f"pa_{o_name}_w_minus_l_{suffix}"
            m, t_v, _, _ = t13.wl_row_pair(cell_ser, (outer, "W"), (outer, "L"), mask)
            rows.append({"name": nm, "paper": t3[nm][0], "ours": m, "tol": t3[nm][1]})
            rows.append({"name": nm + "_tstat", "paper": t3[nm + "_tstat"][0],
                         "ours": t_v, "tol": t3[nm + "_tstat"][1]})

    for outer in ("W", "M", "L"):
        o_name = {"W": "winner", "M": "middle", "L": "loser"}[outer]
        for col, inner in (("winner", "W"), ("loser", "L")):
            for suffix, mask in (("all", mask_all), ("exjan", mask_exjan)):
                nm = f"pb_{o_name}_{col}_{suffix}"
                rows.append({"name": nm, "paper": t3[nm][0],
                             "ours": cell_mean(inner, outer, mask), "tol": t3[nm][1]})
        for suffix, mask in (("all", mask_all), ("exjan", mask_exjan)):
            nm = f"pb_{o_name}_w_minus_l_{suffix}"
            m, t_v, _, _ = t13.wl_row_pair(cell_ser, ("W", outer), ("L", outer), mask)
            rows.append({"name": nm, "paper": t3[nm][0], "ours": m, "tol": t3[nm][1]})
            rows.append({"name": nm + "_tstat", "paper": t3[nm + "_tstat"][0],
                         "ours": t_v, "tol": t3[nm + "_tstat"][1]})
    return rows


def tier_counts(rows: list[dict]) -> dict:
    c = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0}
    for r in rows:
        c[t13.tier(r["paper"], r["ours"], r["tol"])] += 1
    return c


def main() -> None:
    targets = t13.load_targets()
    t1, t3 = targets["T1"], targets["T3"]

    panel, grid, permnos, ret_mat = t13.load_matrices()
    f0 = int(np.searchsorted(grid, t13.FORM_START.to_datetime64()))
    hold0 = int(np.searchsorted(grid, t13.HOLD_START.to_datetime64()))
    hold_end_i = int(np.searchsorted(grid, t13.HOLD_END.to_datetime64()))
    n_hold = hold_end_i - hold0 + 1
    n_f = n_hold + t13.J - 1
    assert n_hold == 462 and n_f == 467

    hold_months = pd.DatetimeIndex(grid[hold0: hold_end_i + 1])
    mo = hold_months.month.to_numpy()
    mask_all = np.ones(n_hold, dtype=bool)
    mask_exjan = mo != 1

    # cohorts: jt outer ranking + both 52WH inner rankings
    jt_coh = cohorts_for(panel, grid, "jt_sig")
    cl_coh = cohorts_for(panel, grid, CL)
    dc_coh = cohorts_for(panel, grid, DC)
    f_indices = [f0 + k for k in range(n_f)]

    # ---- Table I 52WH rows under both variants -----------------------------
    t1_cl = t1_wh_rows(cl_coh, f0, n_f, hold0, n_hold, permnos, ret_mat, mask_all, t1)
    t1_dc = t1_wh_rows(dc_coh, f0, n_f, hold0, n_hold, permnos, ret_mat, mask_all, t1)

    # ---- Table III under both variants -------------------------------------
    rows3_cl = table3_rows(jt_coh, cl_coh, f_indices, f0, n_f, hold0, n_hold,
                           permnos, ret_mat, mask_all, mask_exjan, t3)
    rows3_dc = table3_rows(jt_coh, dc_coh, f_indices, f0, n_f, hold0, n_hold,
                           permnos, ret_mat, mask_all, mask_exjan, t3)
    assert len(rows3_cl) == 48 and len(rows3_dc) == 48
    assert [r["name"] for r in rows3_cl] == [r["name"] for r in rows3_dc]

    # ---- assemble side-by-side rows (Table III first, then Table I 52WH) ----
    combined: list[dict] = []
    for rc, rd in zip(rows3_cl, rows3_dc):
        combined.append({"name": rc["name"], "paper": rc["paper"],
                         "cl": rc["ours"], "dc": rd["ours"], "tol": rc["tol"]})
    for rc, rd in zip(t1_cl, t1_dc):
        combined.append({"name": "T1_" + rc["name"], "paper": rc["paper"],
                         "cl": rc["ours"], "dc": rd["ours"], "tol": rc["tol"]})

    # ---- totals across 48 + 4 cells ----------------------------------------
    tot_cl = sum(abs(r["cl"] - r["paper"]) for r in combined)
    tot_dc = sum(abs(r["dc"] - r["paper"]) for r in combined)
    t3_tot_cl = sum(abs(r["cl"] - r["paper"]) for r in combined[:48])
    t3_tot_dc = sum(abs(r["dc"] - r["paper"]) for r in combined[:48])
    t1_tot_cl = sum(abs(r["cl"] - r["paper"]) for r in combined[48:])
    t1_tot_dc = sum(abs(r["dc"] - r["paper"]) for r in combined[48:])

    # ---- tier counts (Table III 48, and combined 52) -----------------------
    cnt3_cl = tier_counts(rows3_cl)
    cnt3_dc = tier_counts(rows3_dc)
    comb_rows_cl = [{"paper": r["paper"], "ours": r["cl"], "tol": r["tol"]} for r in combined]
    comb_rows_dc = [{"paper": r["paper"], "ours": r["dc"], "tol": r["tol"]} for r in combined]
    cnt52_cl = tier_counts(comb_rows_cl)
    cnt52_dc = tier_counts(comb_rows_dc)

    winner = DC if tot_dc < tot_cl else CL
    margin = abs(tot_cl - tot_dc)

    # ---- write the comparison markdown -------------------------------------
    L: list[str] = []
    L.append("# 52-week-high signal granularity: wh_sig_dc (daily close) vs "
             "wh_sig_cl (month-end close)")
    L.append("")
    L.append("George & Hwang (2004). Side-by-side per-cell comparison for the "
             "48 Table III cells + the 4 Table I 52WH metrics. The ONLY thing "
             "that differs between the two columns is the 52WH price series "
             "used for the inner ranking:")
    L.append("- `cl` = wh_sig_cl = |prc(f)| / max of MSF month-end closes over f-11..f")
    L.append("- `dc` = wh_sig_dc = |prc(f)| / max of DSF daily closes over "
             "f-11..f (literal 'highest price achieved', L122)")
    L.append("")
    L.append("Everything else identical: same jt_sig outer rankings, 30/40/30 "
             "sorts, (6,6) timing, nonempty-cell W-L rule. |err| and tiers are "
             "vs the paper value. Tiers use each metric's tolerance_pct from "
             "tables_to_replicate.json.")
    L.append("")
    L.append("| cell name | paper | cl | dc | \\|err_cl\\| | \\|err_dc\\| | tier_cl | tier_dc |")
    L.append("|---|---:|---:|---:|---:|---:|---|---|")
    for r in combined:
        tcl = t13.tier(r["paper"], r["cl"], r["tol"])
        tdc = t13.tier(r["paper"], r["dc"], r["tol"])
        L.append(
            f"| {r['name']} | {t13.fmt(r['paper'])} | {t13.fmt(r['cl'])} | "
            f"{t13.fmt(r['dc'])} | {abs(r['cl'] - r['paper']):.4f} | "
            f"{abs(r['dc'] - r['paper']):.4f} | {tcl} | {tdc} |"
        )
    L.append("")
    L.append("## Hit-rate summaries")
    L.append("")
    L.append("**Table III (48 cells):**")
    L.append(f"- cl (wh_sig_cl): {cnt3_cl['Tier 1']} Tier 1 / {cnt3_cl['Tier 2']} "
             f"Tier 2 / {cnt3_cl['FAIL']} FAIL")
    L.append(f"- dc (wh_sig_dc): {cnt3_dc['Tier 1']} Tier 1 / {cnt3_dc['Tier 2']} "
             f"Tier 2 / {cnt3_dc['FAIL']} FAIL")
    L.append("")
    L.append("**Combined (48 Table III + 4 Table I 52WH = 52 cells):**")
    L.append(f"- cl (wh_sig_cl): {cnt52_cl['Tier 1']} Tier 1 / {cnt52_cl['Tier 2']} "
             f"Tier 2 / {cnt52_cl['FAIL']} FAIL")
    L.append(f"- dc (wh_sig_dc): {cnt52_dc['Tier 1']} Tier 1 / {cnt52_dc['Tier 2']} "
             f"Tier 2 / {cnt52_dc['FAIL']} FAIL")
    L.append("")
    L.append("## Total |deviation| from paper (sum of |ours - paper|)")
    L.append("")
    L.append("| scope | cl (wh_sig_cl) | dc (wh_sig_dc) | better |")
    L.append("|---|---:|---:|---|")
    L.append(f"| Table III (48 cells) | {t3_tot_cl:.4f} | {t3_tot_dc:.4f} | "
             f"{'dc' if t3_tot_dc < t3_tot_cl else 'cl'} |")
    L.append(f"| Table I 52WH (4 metrics) | {t1_tot_cl:.4f} | {t1_tot_dc:.4f} | "
             f"{'dc' if t1_tot_dc < t1_tot_cl else 'cl'} |")
    L.append(f"| **All 48 + 4 = 52 cells** | **{tot_cl:.4f}** | **{tot_dc:.4f}** | "
             f"**{'dc' if tot_dc < tot_cl else 'cl'}** |")
    L.append("")
    L.append("## Recommendation")
    L.append("")
    L.append(f"- **Lock `{winner}` as the single primary 52WH signal** for all "
             f"remaining tables.")
    L.append(f"- Margin (total |deviation| across 52 cells): cl {tot_cl:.4f} vs "
             f"dc {tot_dc:.4f} -> {'dc' if winner == DC else 'cl'} better by "
             f"{margin:.4f} ({margin / max(tot_cl, tot_dc) * 100:.1f}% lower total error).")
    L.append(f"- Table III only: cl {t3_tot_cl:.4f} vs dc {t3_tot_dc:.4f} "
             f"(margin {abs(t3_tot_cl - t3_tot_dc):.4f}).")

    t13.LAYOUT.result_path("table_3_dc_vs_cl.md").write_text("\n".join(L))

    # ---- console report ----------------------------------------------------
    print("=" * 78)
    print("52WH GRANULARITY DIAGNOSTIC: wh_sig_dc (daily) vs wh_sig_cl (month-end)")
    print()
    print("TABLE I 52WH (4 metrics)")
    for rc, rd in zip(t1_cl, t1_dc):
        print(f"  {rc['name']:22s} paper {rc['paper']:7.4f}  cl {rc['ours']:9.4f} "
              f"(|err| {abs(rc['ours'] - rc['paper']):.4f})  dc {rd['ours']:9.4f} "
              f"(|err| {abs(rd['ours'] - rd['paper']):.4f})")
    print()
    print("HIT RATES")
    print(f"  Table III cl: {cnt3_cl['Tier 1']}/{cnt3_cl['Tier 2']}/{cnt3_cl['FAIL']} "
          f"(T1/T2/FAIL of 48)")
    print(f"  Table III dc: {cnt3_dc['Tier 1']}/{cnt3_dc['Tier 2']}/{cnt3_dc['FAIL']} "
          f"(T1/T2/FAIL of 48)")
    print(f"  Combined  cl: {cnt52_cl['Tier 1']}/{cnt52_cl['Tier 2']}/{cnt52_cl['FAIL']} "
          f"(of 52)")
    print(f"  Combined  dc: {cnt52_dc['Tier 1']}/{cnt52_dc['Tier 2']}/{cnt52_dc['FAIL']} "
          f"(of 52)")
    print()
    print("TOTAL |DEVIATION|")
    print(f"  Table III (48): cl {t3_tot_cl:.4f}  dc {t3_tot_dc:.4f}")
    print(f"  Table I (4):    cl {t1_tot_cl:.4f}  dc {t1_tot_dc:.4f}")
    print(f"  All 52:         cl {tot_cl:.4f}  dc {tot_dc:.4f}")
    print()
    print("PREVIOUSLY-MISSING CELLS (ours-dc vs paper)")
    focus = ["pa_loser_w_minus_l_all", "pa_loser_w_minus_l_exjan",
             "pb_winner_w_minus_l_all", "pb_winner_w_minus_l_exjan",
             "pb_loser_w_minus_l_all", "pb_loser_w_minus_l_exjan",
             "pb_middle_w_minus_l_exjan"]
    by_name = {r["name"]: r for r in combined}
    for nm in focus:
        r = by_name[nm]
        print(f"  {nm:30s} paper {r['paper']:7.4f}  dc {r['dc']:9.4f} "
              f"(cl was {r['cl']:9.4f})")
    print()
    print(f"RECOMMENDATION: lock {winner}; margin {margin:.4f} "
          f"({margin / max(tot_cl, tot_dc) * 100:.1f}% lower total |err| over 52 cells)")
    print(f"wrote {t13.LAYOUT.result_path('table_3_dc_vs_cl.md')}")


if __name__ == "__main__":
    main()
