"""
George & Hwang (2004) — DELISTING-RETURN EXPERIMENT (one committed change:
the holding-period return series).

Runs ALL five tables under BOTH return columns now in data/panel.parquet:
  - ret     : original msf returns (current official variant)
  - ret_dl  : delisting-adjusted — final month of a delisted stock folds in
              msedelist.dlret: (1+ret)(1+dlret)-1 where a panel/msf return
              exists for that month, else dlret alone (added delisting-month
              rows carry ret=NaN so this variant is the ONLY thing that
              changes). NULL/worthless dlret left as-is, NO Shumway/BMP
              imputation.

Signals/rankings/industry returns stay on the ORIGINAL ret in both runs —
only portfolio/regression DEPENDENT variables switch (tables_1_3.run and
tables_5.run_table take a RET_COL parameter; default "ret").

Writes results/delisting_experiment.md:
  1. delisting merge stats (events, dlret coverage, performance-delist
     missing counts by decade + 580/584, mean dlret);
  2. before/after hit-rate table (T1/T2/FAIL per table under each variant);
  3. KEY cells side by side: Table I losers (3 strategies), Table V
     wh/jt/mg_loser (s66_raw, both Jan columns), Table VII gh_loser +
     gh_spread (all 8 columns), Table III hit-rate;
  4. the diagnostic anchors vs paper;
  5. RECOMMENDATION with the quantified margin (criterion: total Tier-1
     cell count across all 5 tables; tie-breakers: fewer FAILs, then lower
     summed |deviation| over finite cells).

Then regenerates the OFFICIAL outputs (results/table_*.md +
results/intermediate/strategy_returns.parquet +
results/intermediate/fm_coefficients*.parquet) under the
better variant ONLY, after the comparison md is written.

Run AFTER src/main.py (panel must carry both ret and ret_dl):
    python main.py && python delisting_experiment.py
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

import tables_1_3 as t13
from tables_5 import CFG_V, COLS, run_table
from tables_7 import CFG_VII
from utils.paths import paper_layout

LAYOUT = paper_layout("the_52_week_high_and_momentum_investing")

VARIANTS = ("ret", "ret_dl")

# Diagnostic anchors from the task (paper values for reference)
ANCHORS = [
    ("Table V wh_loser (s66_raw_janincl)", "T5", "s66_raw_janincl", "wh_loser", -0.48, -0.29),
    ("Table VII gh_loser (s66_raw_janexcl)", "T7", "s66_raw_janexcl", "gh_loser", -0.19, 0.26),
    ("Table I jt_loser (all months)", "T1", None, "jt_loser", 1.05, 1.089),
    ("Table I mg_loser (all months)", "T1", None, "mg_loser", 1.03, 0.977),
]


# --- helpers ------------------------------------------------------------------

def fmt(x, nd=4) -> str:
    return f"{x:.{nd}f}" if np.isfinite(x) else "NaN"


def gather(ret_col: str) -> dict:
    """Run T1/T2/T3 + T5 + T7 under one return column (no file writes)."""
    b13 = t13.run(ret_col=ret_col, write_outputs=False, verbose=False)
    b5 = run_table(CFG_V, ret_col=ret_col, write_outputs=False,
                   enforce_gate=False, verbose=False)
    b7 = run_table(CFG_VII, ret_col=ret_col, write_outputs=False,
                   enforce_gate=False, verbose=False)
    return {"t13": b13, "t5": b5, "t7": b7}


def fm_cell(fm_bundle: dict, col: str, row: str) -> tuple[float, float, str]:
    v, paper, tol, tr = fm_bundle["results"][(col, row, "val")]
    return v, paper, tr


def t1_cell(b13: dict, name: str) -> tuple[float, float]:
    for r in b13["rows1"]:
        if r["name"] == name:
            return r["ours"], r["paper"]
    raise KeyError(name)


def hit_line(counts: dict) -> str:
    return (f"{counts['Tier 1']}/{counts['Tier 2']}/{counts['FAIL']}")


def total_counts(res: dict) -> dict:
    tot = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0}
    for b in (res["t13"]["counts1"], res["t13"]["counts2_combined"],
              res["t13"]["counts3"], res["t5"]["counts"], res["t7"]["counts"]):
        for k in tot:
            tot[k] += b[k]
    return tot


def sum_abs_dev(res: dict) -> float:
    """Sum of |ours - paper| over all finite metric cells of all 5 tables
    (mixed units: returns %, t-stats, FM coefficients — informational
    tie-breaker only)."""
    tot = 0.0
    for rows in (res["t13"]["rows1"], res["t13"]["rowsA"], res["t13"]["rowsB"],
                 res["t13"]["rows3"]):
        for r in rows:
            if np.isfinite(r["ours"]):
                tot += abs(r["ours"] - r["paper"])
    for fm in (res["t5"], res["t7"]):
        for (col, row, kind), (v, paper, tol, tr) in fm["results"].items():
            if np.isfinite(v):
                tot += abs(v - paper)
    return tot


# --- section builders -----------------------------------------------------------

def merge_stats_md(panel: pd.DataFrame) -> tuple[list[str], dict]:
    """Section 1 from data/delisting_stats.json (written by main.py), with
    panel-side cross-checks of the adjusted/added row counts."""
    st = json.loads(LAYOUT.data_path("delisting_stats.json").read_text())
    dls, es = st["dl_stats"], st["dl_event_stats"]

    # panel-side cross-checks (exact; includes dlret == 0 adjustments, which
    # leave ret_dl == ret, via an event-frame-free count from the panel)
    n_adj_rows = int((panel["ret"].notna()
                      & ((panel["ret_dl"] - panel["ret"]).abs() > 0)).sum())
    n_new = int((panel["ret"].isna() & panel["ret_dl"].notna()).sum())
    assert n_new == dls["dl_new_rows"], (
        f"added-row count mismatch: panel {n_new} vs build stats "
        f"{dls['dl_new_rows']}")
    # n_adj_rows <= dl_adj_existing: events with dlret == 0 adjust to the
    # same value and are invisible in the panel
    assert n_adj_rows <= dls["dl_adj_existing"]

    L = [
        "## 1. Delisting merge statistics",
        "",
        f"- msedelist events pulled (dlstdt 1958-01-01 .. 2003-12-31): "
        f"**{dls['dl_pulled']:,}**",
        f"- events mapping to an analysis-grid month (1958-01 .. 2002-12): "
        f"**{es['n_events']:,}** (dropped, 2003 months past the grid: "
        f"{dls['dl_outside_grid']:,})",
        f"- with valid dlret (non-NULL and > -1): **{es['n_valid']:,}** "
        f"(fraction {es['frac_valid']:.4f}); NULL dlret: {es['n_null']:,}; "
        f"worthless (dlret = -1.0, left as-is per spec): {es['n_worthless']:,}",
        f"- merged onto existing panel rows ((1+ret)(1+dlret)-1): "
        f"**{dls['dl_adj_existing']:,}** ({n_adj_rows} visible as "
        f"ret_dl != ret; the rest have dlret = 0 exactly)",
        f"- NEW panel rows added (no panel row at the delisting month; stock "
        f"was an active holding at m-1; ret=NaN, so the `ret` variant is "
        f"untouched): **{dls['dl_new_rows']:,}** — with an msf return at m "
        f"(ret_dl = (1+ret_msf)(1+dlret)-1): {dls['dl_new_with_msf']:,}; msf "
        f"row absent (ret_dl = dlret): {dls['dl_new_msf_absent']:,}",
        f"- valid events NOT actioned (no panel row at m-1 either — not a "
        f"plausible portfolio holding): {dls['dl_skipped_not_holding']:,}; "
        f"NULL/worthless events left as-is: {es['n_null'] + es['n_worthless']:,}",
        f"- WHY most delisting months lack a panel row in this vintage: "
        f"dsenames nameendt = dlstdt < month-end, so universe coverage fails "
        f"at the delisting month for mid-month delistings; the final-month "
        f"msf RECORD exists (all {dls['dl_new_rows']:,} added rows have one) "
        f"but its return/price is usually missing — only "
        f"{dls['dl_new_with_msf']:,} pass the ret>-1 / valid-prc hygiene "
        f"filter (verified by direct ClickHouse spot check)",
        f"- mean dlret over ALL valid in-grid events: "
        f"**{es['mean_dlret_valid']:.4f}**",
        "",
        "### Performance delistings (dlstcd 500-599)",
        "",
        f"- events: **{es['n_perf']:,}**; missing dlret (NULL): "
        f"**{es['perf_missing']:,}**; worthless (dlret = -1.0): "
        f"{es['perf_worthless']:,}; valid: "
        f"{es['n_perf'] - es['perf_missing'] - es['perf_worthless']:,} "
        f"(coverage {es['perf_frac_valid']:.4f})",
        f"- mean dlret of valid performance delistings: "
        f"**{es['mean_dlret_perf']:.4f}** (median {es['median_dlret_perf']:.4f})",
        "",
        "| decade | n events | missing dlret | worthless (-1) | valid |",
        "|---|---:|---:|---:|---:|",
    ]
    for d in sorted(es["perf_by_decade"], key=int):
        b = es["perf_by_decade"][d]
        L.append(f"| {d}s | {b['n']} | {b['missing']} | {b['worthless']} | "
                 f"{b['valid']} |")
    L += [
        "",
        "| dlstcd | n | missing dlret | valid | mean dlret (valid) |",
        "|---|---:|---:|---:|---:|",
    ]
    for code in (580, 584):
        cs = es[f"code_{code}"]
        L.append(f"| {code} | {cs['n']} | {cs['missing']} | {cs['valid']} | "
                 f"{fmt(cs['mean_dlret'])} |")
    L += [
        "",
        "- No Shumway/BMP imputation applied (post-paper methodology): "
        "NULL-dlret and worthless events keep ret_dl = ret.",
    ]
    return L, {**es, **dls}


def hit_rate_md(res: dict) -> list[str]:
    r0, r1 = res["ret"], res["ret_dl"]
    table_rows = [
        ("Table I", r0["t13"]["counts1"], r1["t13"]["counts1"]),
        ("Table II (combined)", r0["t13"]["counts2_combined"],
         r1["t13"]["counts2_combined"]),
        ("Table II Panel A", r0["t13"]["countsA"], r1["t13"]["countsA"]),
        ("Table II Panel B", r0["t13"]["countsB"], r1["t13"]["countsB"]),
        ("Table III", r0["t13"]["counts3"], r1["t13"]["counts3"]),
        ("Table V", r0["t5"]["counts"], r1["t5"]["counts"]),
        ("Table VII", r0["t7"]["counts"], r1["t7"]["counts"]),
    ]
    L = [
        "## 2. Hit rates per table (Tier 1 / Tier 2 / FAIL)",
        "",
        "| table | n | ret | ret_dl | Δ Tier 1 |",
        "|---|---:|---|---|---:|",
    ]
    for name, c0, c1 in table_rows:
        n = sum(c0.values())
        d = c1["Tier 1"] - c0["Tier 1"]
        L.append(f"| {name} | {n} | {hit_line(c0)} | {hit_line(c1)} | {d:+d} |")
    t0, t1 = total_counts(r0), total_counts(r1)
    L.append(f"| **ALL (T1+T2+T3+T5+T7)** | {sum(t0.values())} | "
             f"**{hit_line(t0)}** | **{hit_line(t1)}** | "
             f"**{t1['Tier 1'] - t0['Tier 1']:+d}** |")
    return L


def key_cells_md(res: dict) -> list[str]:
    r0, r1 = res["ret"], res["ret_dl"]
    L = ["## 3. Key cells side by side (paper | ret | ret_dl)", ""]

    # --- Table I losers
    L += ["### Table I losers (avg monthly return %, all 462 months)", "",
          "| strategy | paper | ret | ret_dl | Δ(ret_dl−ret) |",
          "|---|---:|---:|---:|---:|"]
    for name in ("jt_loser", "mg_loser", "wh_loser"):
        v0, paper = t1_cell(r0["t13"], name)
        v1, _ = t1_cell(r1["t13"], name)
        L.append(f"| {name} | {fmt(paper, 2)} | {fmt(v0)} | {fmt(v1)} | "
                 f"{v1 - v0:+.4f} |")
    L.append("")

    # --- Table V loser dummies
    L += ["### Table V loser dummies (FM coefficient, %/month)", "",
          "| row | column | paper | ret | ret_dl | Δ(ret_dl−ret) | tier ret | tier ret_dl |",
          "|---|---|---:|---:|---:|---:|---|---|"]
    for row in ("wh_loser", "jt_loser", "mg_loser"):
        for col in ("s66_raw_janincl", "s66_raw_janexcl"):
            v0, paper, tr0 = fm_cell(r0["t5"], col, row)
            v1, _, tr1 = fm_cell(r1["t5"], col, row)
            L.append(f"| {row} | {col} | {fmt(paper, 2)} | {fmt(v0)} | "
                     f"{fmt(v1)} | {v1 - v0:+.4f} | {tr0} | {tr1} |")
    L.append("")

    # --- Table VII gh cells, all 8 columns
    L += ["### Table VII gh_loser and gh_spread (all 8 columns)", "",
          "| row | column | paper | ret | ret_dl | Δ(ret_dl−ret) | tier ret | tier ret_dl |",
          "|---|---|---:|---:|---:|---:|---|---|"]
    for row in ("gh_loser", "gh_spread"):
        for col in COLS:
            v0, paper, tr0 = fm_cell(r0["t7"], col, row)
            v1, _, tr1 = fm_cell(r1["t7"], col, row)
            L.append(f"| {row} | {col} | {fmt(paper, 2)} | {fmt(v0)} | "
                     f"{fmt(v1)} | {v1 - v0:+.4f} | {tr0} | {tr1} |")
    return L


def anchors_md(res: dict) -> list[str]:
    r0, r1 = res["ret"], res["ret_dl"]
    L = [
        "## 4. Diagnostic anchors (before/after vs paper)",
        "",
        "| anchor | paper | before (ret) | after (ret_dl) | move | closer to paper? |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for label, tab, col, row, paper, _before in ANCHORS:
        if tab == "T1":
            v0, _ = t1_cell(r0["t13"], row)
            v1, _ = t1_cell(r1["t13"], row)
        else:
            v0, _, _ = fm_cell(r0["t7" if tab == "T7" else "t5"], col, row)
            v1, _, _ = fm_cell(r1["t7" if tab == "T7" else "t5"], col, row)
        closer = abs(v1 - paper) < abs(v0 - paper)
        L.append(f"| {label} | {fmt(paper, 2)} | {fmt(v0)} | {fmt(v1)} | "
                 f"{v1 - v0:+.4f} | {'YES' if closer else 'no'} "
                 f"(|err| {abs(v0 - paper):.4f} → {abs(v1 - paper):.4f}) |")
    return L


def diag_md(res: dict) -> list[str]:
    r0, r1 = res["ret"], res["ret_dl"]
    L = ["## 5. Diagnostics and gate status per variant", ""]
    for name, r in (("ret", r0), ("ret_dl", r1)):
        d5, d7 = r["t5"]["diag"], r["t7"]["diag"]
        L.append(f"### variant `{name}`")
        L.append(f"- T5 regression sample: s66 avg {d5['s66']['avg_sample']:.1f} "
                 f"(min {d5['s66']['min_sample']}), s612 avg "
                 f"{d5['s612']['avg_sample']:.1f} (min {d5['s612']['min_sample']})")
        L.append(f"- T7 regression sample: s66 avg {d7['s66']['avg_sample']:.1f} "
                 f"(min {d7['s66']['min_sample']}), s612 avg "
                 f"{d7['s612']['avg_sample']:.1f} (min {d7['s612']['min_sample']})")
        gp5 = r["t5"]["gate_problems"]
        gp7 = r["t7"]["gate_problems"]
        L.append(f"- T5 pre-flight gate: {'PASS' if not gp5 else 'PROBLEMS: ' + '; '.join(gp5)}")
        L.append(f"- T7 pre-flight gate: {'PASS' if not gp7 else 'PROBLEMS: ' + '; '.join(gp7)}")
        L.append(f"- Table I min cohorts available per holding month: "
                 f"{r['t13']['min_avail']}")
        L.append("")
    return L


def recommend(res: dict) -> tuple[str, list[str]]:
    t0, t1 = total_counts(res["ret"]), total_counts(res["ret_dl"])
    s0, s1 = sum_abs_dev(res["ret"]), sum_abs_dev(res["ret_dl"])
    reasons = [
        f"- Total Tier 1 across all 5 tables: ret {t0['Tier 1']} vs ret_dl "
        f"{t1['Tier 1']} (margin {t1['Tier 1'] - t0['Tier 1']:+d}).",
        f"- Total FAIL: ret {t0['FAIL']} vs ret_dl {t1['FAIL']} "
        f"({t1['FAIL'] - t0['FAIL']:+d}).",
        f"- Sum of |deviation| over all finite cells (mixed units, "
        f"informational): ret {s0:.2f} vs ret_dl {s1:.2f} ({s1 - s0:+.2f}).",
    ]
    if t1["Tier 1"] != t0["Tier 1"]:
        better = "ret_dl" if t1["Tier 1"] > t0["Tier 1"] else "ret"
        reason = f"total Tier-1 count ({t1['Tier 1'] - t0['Tier 1']:+d} cells)"
    elif t1["FAIL"] != t0["FAIL"]:
        better = "ret_dl" if t1["FAIL"] < t0["FAIL"] else "ret"
        by = abs(t1["FAIL"] - t0["FAIL"])
        reason = f"fewer FAIL cells (−{by})"
    else:
        better = "ret_dl" if s1 < s0 else "ret"
        reason = "lower summed |deviation| (Tier-1 and FAIL counts tied)"
    head = (f"## 6. Recommendation: **adopt `{better}`** as the official "
            f"holding-period return column, by {reason}.")
    L = [head, "",
         "Criterion (pre-registered by the task): overall cell hit-rate "
         "(total Tier 1 across Tables I, II, III, V, VII).", ""] + reasons
    L += [
        "",
        f"The official outputs (results/table_*.md,",
        f"results/intermediate/strategy_returns.parquet,",
        f"results/intermediate/fm_coefficients*.parquet) were regenerated under",
        f"`{better}` by this script AFTER writing this comparison.",
    ]
    return better, L


# --- main ------------------------------------------------------------------------

def main() -> None:
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    assert "ret_dl" in panel.columns, (
        "panel.parquet has no ret_dl column — run src/main.py first")

    print(f"panel: {panel.shape[0]:,} rows x {panel.shape[1]} cols")
    res = {}
    for rc in VARIANTS:
        print(f"--- running all tables under `{rc}` ---")
        res[rc] = gather(rc)
        tc = total_counts(res[rc])
        print(f"    totals: {hit_line(tc)} of {sum(tc.values())}")

    stats_lines, stats = merge_stats_md(panel)

    L = [
        "# Delisting-return experiment — George & Hwang (2004)",
        "",
        "ONE committed change: the holding-period return series. `ret_dl` folds",
        "msedelist.dlret into the final month of delisted stocks; `ret` is the",
        "original msf series. Signals, industry returns, and rankings are on the",
        "ORIGINAL ret under BOTH variants (dependent variables only). No",
        "Shumway/BMP imputation. The paper is silent on delisting treatment; the",
        "leading hypothesis is that missing delisting returns bias loser",
        "portfolios upward (delisting returns are mostly negative and",
        "concentrated in losers).",
        "",
        f"Panel: {panel.shape[0]:,} rows x {panel.shape[1]} cols; "
        f"rows where ret_dl differs from ret (visible adjustments): "
        f"{int((panel['ret'].notna() & ((panel['ret_dl'] - panel['ret']).abs() > 0)).sum()):,}; "
        f"added delisting-month rows (ret NaN, ret_dl set): "
        f"{int((panel['ret'].isna() & panel['ret_dl'].notna()).sum()):,} "
        f"(plus events with dlret = 0 exactly, adjusted to the same value).",
        "",
        *stats_lines,
        "",
        *hit_rate_md(res),
        "",
        *key_cells_md(res),
        "",
        *anchors_md(res),
        "",
        *diag_md(res),
        "",
    ]
    better, rec_lines = recommend(res)
    L += rec_lines

    out = LAYOUT.result_path("delisting_experiment.md")
    out.write_text("\n".join(L))
    print(f"\nwrote {out}")

    # --- regenerate official outputs under the better variant ----------------
    print(f"\n=== regenerating OFFICIAL outputs under `{better}` ===")
    t13.run(ret_col=better, write_outputs=True, verbose=True)
    run_table(CFG_V, ret_col=better, write_outputs=True,
              enforce_gate=False, verbose=True)
    run_table(CFG_VII, ret_col=better, write_outputs=True,
              enforce_gate=False, verbose=True)
    print(f"official outputs regenerated under `{better}`")


if __name__ == "__main__":
    main()
