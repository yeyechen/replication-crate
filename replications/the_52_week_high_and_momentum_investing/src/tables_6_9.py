"""
George & Hwang (2004), "The 52-Week High and Momentum Investing", JF —
Tables VI and IX (audit1.md corollary items [M1] and [M4]).

TABLE VI — Persistence of Profits (risk-adjusted), (6, k, 12) strategies.
  Paper §II.C (L981-1005), values L1007-1095 + L1134-1268. The paper's 3rd
  abstract claim: JT / MG momentum REVERSES at long horizons (winner dummies
  turn negative) while 52-week-high profits do NOT reverse.

  For each k in {12, 24, 36, 48}, each month t = 1963-07 .. 2001-12 (462),
  each formation lag j = 2..13 (12 lags, matching the (6,.,12) holding
  length), ONE cross-sectional OLS:

    R_it(%) = b0 + b1*R_{i,t-1}(decimal, original ret) + b2*ln(mcap_$ at t-1)
            + b3*JH + b4*JL + b5*MH + b6*ML + b7*FHH + b8*FHL + e

  with the dummies drawn from formation f = t - k - j (k-offset; the shared
  tables_5.run_horizon engine, extended additively with k_offset). Same 30/30
  ordinal ranks as Table V (jt_sig / mg_sig / wh_sig_dc). c_{k,t} = mean over
  j=2..13 of b_{k,j,t}. The paper reports RISK-ADJUSTED ONLY: intercept + t-stat
  of the OLS of c_{k,t} on contemporaneous FF3 (mkt_rf, smb, hml x100), Jan-incl
  (all 462 t) and Jan-excl (t != January).

  12 rows (intercept, r_lag1, size, jt_winner, jt_loser, mg_winner, mg_loser,
  wh_winner, wh_loser, wh_spread, jt_spread, mg_spread) x 8 columns
  (k12/k24/k36/k48 x {Jan incl, Jan excl}) = 96 values + 96 t-stats = 192 cells.

TABLE IX — 52-week LOW replaces 52-week high.
  Paper spec L2173-2176, values L2178-2444. "Table IX is identical to Table V
  except that a strategy based on the 52-week low is used instead of the
  52-week high." Runs the EXACT tables_5.run_table machinery (new TableConfig)
  with FLH/FLL dummies from wh_lo_sig (top 30% = winners = farthest ABOVE the
  52-week low; bottom 30% = losers = nearest the low) REPLACING FHH/FHL. JT/MG
  identical to Table V. Both horizons (6,6)+(6,12), raw + RA, Jan incl/excl:
  12 rows x 8 cols x 2 = 192 cells.

  The paper's claim: the 52-week-LOW spread is economically small and
  INSIGNIFICANT ((6,6) raw Jan-incl 0.13, t 0.95) while JT spreads become
  LARGER than in Table V (jt_spread (6,6) raw Jan-excl 1.05, t 7.91 vs 0.46).

Outputs:
  - results/intermediate/fm_coefficients_persist.parquet  (Table VI c_{k,t} series)
  - results/intermediate/fm_coefficients_low.parquet      (Table IX c_{k,t} series)
    (relocated out of data/ by audit1.md [M6])
  - results/table_6.md / table_9.md

The official Table V artifacts (fm_coefficients.parquet, table_5.md) are NOT
touched; the engine extension (k_offset, "wl" spread slot) is additive with a
default that keeps Table V/VII outputs bit-identical (verified by
verify_identity()).
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from tables_5 import (COLS, LAYOUT, PRIMARY_WH, SPREAD_ORDER, STRAT_SIG,
                      TableConfig, coef_names, dev_pct, fmt, intermediate_path,
                      load_ff, load_panel_matrices, build_rank_sets,
                      load_targets, make_rows, ra_intercept_tstat,
                      rankable_by_decade, raw_mean_tstat, row_series,
                      run_horizon, run_table, tier, tier_display,
                      TIER2_LEGEND)
from utils.paths import paper_layout

LAYOUT = paper_layout("the_52_week_high_and_momentum_investing")

HOLD_START = pd.Timestamp("1963-07-31")
HOLD_END = pd.Timestamp("2001-12-31")
KLIST = (12, 24, 36, 48)
JLIST_PERSIST = list(range(2, 14))   # j = 2..13 (12 lags)

# Table VI columns: k-value x {Jan incl, Jan excl} (RA only).
COLS6 = [f"k{k}_{j}" for k in KLIST for j in ("janincl", "janexcl")]

RET_COL = "ret_dl"   # official holding return (dependent variable)


# --- paper transcription ----------------------------------------------------
# Each entry: row -> (values[8], tstats[8]) in column order.

T6_ROWS = ["intercept", "r_lag1", "size", "jt_winner", "jt_loser",
           "mg_winner", "mg_loser", "wh_winner", "wh_loser",
           "wh_spread", "jt_spread", "mg_spread"]

# Table VI (RA only), column order = COLS6
# [k12_janincl, k12_janexcl, k24_janincl, k24_janexcl,
#  k36_janincl, k36_janexcl, k48_janincl, k48_janexcl]
T6_PAPER = {
    "intercept": ([1.73, 0.62, 1.6, 0.5, 1.41, 0.3, 1.28, 0.14],
                  [3.96, 1.62, 3.59, 1.29, 3.17, 0.77, 2.96, 0.37]),
    "r_lag1": ([-6.05, -5.41, -6.10, -5.43, -6.16, -5.47, -6.25, -5.57],
               [-13.85, -14.56, -13.86, -14.45, -13.98, -14.27, -13.93, -14.01]),
    "size": ([-0.09, -0.01, -0.08, 0.00, -0.07, 0.02, -0.05, 0.03],
             [-2.63, -0.17, -2.27, 0.16, -2.00, 0.58, -1.56, 1.20]),
    "jt_winner": ([-0.15, -0.18, -0.08, -0.11, -0.06, -0.10, -0.09, -0.13],
                  [-3.80, -4.76, -2.06, -2.90, -1.54, -2.73, -2.23, -3.36]),
    "jt_loser": ([-0.02, -0.06, -0.02, -0.03, 0.00, -0.02, 0.02, 0.02],
                 [-0.86, -2.26, -0.72, -1.27, -0.08, -0.76, 0.68, 0.77]),
    "mg_winner": ([-0.11, -0.12, -0.08, -0.09, 0.05, 0.02, 0.06, 0.06],
                  [-2.42, -2.76, -2.04, -2.43, 1.16, 0.49, 1.37, 1.42]),
    "mg_loser": ([-0.03, -0.01, -0.11, -0.10, 0.00, 0.00, -0.03, -0.02],
                 [-0.72, -0.21, -2.67, -2.50, 0.04, 0.01, -0.75, -0.43]),
    "wh_winner": ([0.03, 0.06, 0.02, 0.06, 0.00, 0.01, -0.02, -0.01],
                  [1.00, 2.15, 0.74, 1.91, -0.07, 0.51, -0.70, -0.34]),
    "wh_loser": ([0.05, -0.10, 0.08, -0.03, 0.06, -0.03, -0.01, -0.08],
                 [0.67, -1.51, 1.19, -0.42, 0.99, -0.51, -0.16, -1.62]),
    "wh_spread": ([-0.02, 0.16, -0.06, 0.08, -0.07, 0.04, -0.01, 0.07],
                  [-0.23, 1.93, -0.70, 1.00, -0.82, 0.60, -0.15, 1.11]),
    "jt_spread": ([-0.13, -0.12, -0.06, -0.07, -0.05, -0.08, -0.10, -0.14],
                  [-2.65, -2.66, -1.24, -1.62, -1.29, -1.85, -2.20, -3.16]),
    "mg_spread": ([-0.08, -0.11, 0.02, 0.01, 0.04, 0.02, 0.09, 0.08],
                  [-1.33, -1.91, 0.45, 0.16, 0.91, 0.39, 1.76, 1.54]),
}

# Table IX, column order = COLS (same as Table V)
# [s66_raw_janincl, s66_raw_janexcl, s66_ra_janincl, s66_ra_janexcl,
#  s612_raw_janincl, s612_raw_janexcl, s612_ra_janincl, s612_ra_janexcl]
T9_ROWS = ["intercept", "r_lag1", "size", "jt_winner", "jt_loser",
           "mg_winner", "mg_loser", "wl_winner", "wl_loser",
           "wl_spread", "jt_spread", "mg_spread"]
T9_PAPER = {
    "intercept": ([3.27, 1.36, 2.16, 1.01, 3.26, 1.34, 2.15, 0.99],
                  [5.18, 2.48, 4.76, 2.55, 5.14, 2.43, 4.74, 2.51]),
    "r_lag1": ([-6.50, -5.50, -5.93, -5.34, -6.56, -5.57, -5.98, -5.39],
               [-14.82, -14.96, -14.09, -14.86, -14.86, -15.09, -14.10, -14.93]),
    # NOTE: s612_raw_janincl size t-stat OCR'd as "(3.68)"; the coefficient is
    # -0.17 (negative), and Table V's analog is -4.27, so the sign is a dropped
    # minus -> transcribed as -3.68 (OCR correction, not a magnitude guess).
    "size": ([-0.18, -0.04, -0.14, -0.05, -0.17, -0.03, -0.13, -0.04],
             [-3.86, -1.00, -3.90, -1.60, -3.68, -0.79, -3.70, -1.34]),
    "jt_winner": ([0.25, 0.30, 0.30, 0.33, 0.13, 0.20, 0.20, 0.23],
                  [5.18, 6.38, 6.35, 6.82, 3.50, 5.65, 5.75, 6.73]),
    "jt_loser": ([-0.46, -0.75, -0.57, -0.77, -0.32, -0.59, -0.44, -0.63],
                 [-3.63, -6.92, -5.75, -9.75, -2.91, -6.16, -5.33, -9.30]),
    "mg_winner": ([0.17, 0.16, 0.17, 0.18, 0.10, 0.09, 0.13, 0.12],
                  [2.69, 2.44, 2.75, 2.67, 1.73, 1.48, 2.38, 2.09]),
    "mg_loser": ([-0.07, -0.05, -0.07, -0.05, -0.07, -0.05, -0.08, -0.07],
                 [-1.08, -0.82, -1.03, -0.79, -1.56, -1.19, -1.95, -1.59]),
    "wl_winner": ([0.06, 0.02, 0.07, 0.05, -0.04, -0.10, -0.04, -0.07],
                  [0.61, 0.21, 1.30, 0.95, -0.45, -1.04, -0.77, -1.43]),
    "wl_loser": ([-0.07, -0.09, -0.01, -0.06, -0.10, -0.11, -0.05, -0.08],
                 [-1.37, -1.98, -0.32, -1.64, -2.26, -2.48, -1.42, -2.53]),
    "wl_spread": ([0.13, 0.12, 0.09, 0.11, 0.06, 0.01, 0.01, 0.01],
                  [0.95, 0.84, 1.05, 1.47, 0.45, 0.06, 0.12, 0.14]),
    "jt_spread": ([0.71, 1.05, 0.87, 1.10, 0.45, 0.79, 0.64, 0.86],
                  [4.61, 7.91, 6.84, 10.06, 3.48, 7.07, 6.29, 9.92]),
    "mg_spread": ([0.24, 0.21, 0.24, 0.22, 0.17, 0.14, 0.22, 0.19],
                  [2.74, 2.40, 2.80, 2.63, 2.23, 1.81, 3.08, 2.60]),
}

# OCR cells that were unreadable / skipped (none for Table VI; Table IX size
# s612_raw_janincl t-stat corrected, documented above). Kept explicit for the
# report.
SKIPPED_CELLS = []   # (table, col, row, kind, note)


def _tol(paper_value: float) -> float:
    """Tolerance rule (task spec): RA/FM coefficients and t-stats +/-40%;
    near-zero cells (|paper| < 0.05) -> 200%."""
    return 200.0 if abs(paper_value) < 0.05 else 40.0


def patch_targets_json() -> None:
    """Idempotently add T6 and T9 metric entries (transcribed above) to
    preparations/tables_to_replicate.json so the shared load_targets() and
    tier machinery work unchanged."""
    path = LAYOUT.preparations_path("tables_to_replicate.json")
    doc = json.loads(path.read_text())
    by_id = {t["id"]: t for t in doc["tables"]}

    def metrics_for(paper: dict, cols: list, rows: list, loc: str) -> list:
        out = []
        for ci, col in enumerate(cols):
            for row in rows:
                vals, tstats = paper[row]
                v, t = vals[ci], tstats[ci]
                out.append({"name": f"{col}_{row}", "value": v,
                            "unit": "percent_per_month",
                            "tolerance_pct": _tol(v), "paper_location": loc})
                out.append({"name": f"{col}_{row}_tstat", "value": t,
                            "unit": "t_stat",
                            "tolerance_pct": _tol(t), "paper_location": loc})
        return out

    if "T6" not in by_id:
        doc["tables"].append({
            "id": "T6", "table_ref": "Table VI",
            "description": ("Persistence of profits from JT, MG, and 52-week "
                            "high strategies - risk-adjusted returns, (6,k,12) "
                            "strategies k=12,24,36,48."),
            "replication_meaning": ("Tests the paper's 3rd abstract claim: JT/MG "
                                    "momentum reverses at long horizons while "
                                    "52-week-high profits do not."),
            "paper_quote": ("Table VI presents regression results for "
                            "risk-adjusted returns... (L985)"),
            "metrics": metrics_for(T6_PAPER, COLS6, T6_ROWS, "L1007-1268"),
            "notes": None,
        })
    if "T9" not in by_id:
        doc["tables"].append({
            "id": "T9", "table_ref": "Table IX",
            "description": ("Table V with a 52-week-LOW strategy (wh_lo_sig) "
                            "replacing the 52-week high; (6,6) and (6,12), raw "
                            "and risk-adjusted."),
            "replication_meaning": ("Robustness/cross-sectional corollary: the "
                                    "52-week-low spread is insignificant while "
                                    "JT spreads grow, arguing against the "
                                    "symmetric GH proposition."),
            "paper_quote": ("Table IX is identical to Table V except that a "
                            "strategy based on the 52-week low is used instead "
                            "of the 52-week high. (L2176)"),
            "metrics": metrics_for(T9_PAPER, COLS, T9_ROWS, "L2178-2444"),
            "notes": ("size s612_raw_janincl t-stat OCR '(3.68)' corrected to "
                      "-3.68 (dropped minus; coef -0.17, Table V analog -4.27)."),
        })
    if "T6" not in by_id or "T9" not in by_id:
        path.write_text(json.dumps(doc, indent=2))
        print(f"patched {path}: added T6/T9 target entries")
    else:
        print(f"{path}: T6/T9 already present")


# --- Table VI driver --------------------------------------------------------

def run_table_6(write_outputs: bool = True, verbose: bool = True) -> dict:
    targets = load_targets("T6")
    rows = make_rows(STRAT_SIG)                 # 12 rows (jt/mg/wh + spreads)
    coef = coef_names(STRAT_SIG)
    I = {name: k for k, name in enumerate(coef)}
    n_coef = len(coef)

    panel, grid, permnos, dep_mat, ctrl_mat, mcap_mat = load_panel_matrices(RET_COL)
    ranks = build_rank_sets(panel, grid, permnos, STRAT_SIG)

    hold0 = int(np.searchsorted(grid, HOLD_START.to_datetime64()))
    hold_end_i = int(np.searchsorted(grid, HOLD_END.to_datetime64()))
    hold_idx = np.arange(hold0, hold_end_i + 1)
    n_hold = len(hold_idx)
    assert n_hold == 462, f"expected 462 holding months, got {n_hold}"

    hold_months = pd.DatetimeIndex(grid[hold_idx])
    mo = hold_months.month.to_numpy()
    mask_all = np.ones(n_hold, dtype=bool)
    mask_exjan = mo != 1

    ff = load_ff()
    ff_arr = ff.set_index("month").reindex(hold_months)[
        ["mkt_rf", "smb", "hml"]].to_numpy(dtype="float64")
    assert int(np.any(~np.isfinite(ff_arr), axis=1).sum()) == 0

    # ---- run the (6,k,12) grid for each k ----------------------------------
    c_by_k, diag, rankable = {}, {}, {}
    for k in KLIST:
        c, ss, nreg, _rs = run_horizon(JLIST_PERSIST, hold_idx, dep_mat, ctrl_mat,
                                       mcap_mat, ranks, list(STRAT_SIG), k_offset=k)
        assert c.shape[1] == n_coef
        c_by_k[k] = c
        diag[k] = {"avg_sample": float(ss.mean()), "min_sample": int(ss.min()),
                   "max_sample": int(ss.max()), "n_reg": int(nreg),
                   "n_months_empty": int((ss < n_coef).sum())}
        f_lo = hold0 - k - max(JLIST_PERSIST)
        f_hi = hold_end_i - k - min(JLIST_PERSIST)
        rankable[k] = rankable_by_decade(panel, grid, STRAT_SIG, f_lo, f_hi)
    del panel

    # ---- c_{k,t} parquet ----------------------------------------------------
    coeff = pd.DataFrame({"month": hold_months})
    for k, c in c_by_k.items():
        for kk, name in enumerate(coef):
            coeff[f"k{k}_{name}"] = c[:, kk]
        for s in SPREAD_ORDER:
            if s in STRAT_SIG:
                coeff[f"k{k}_{s}_spread"] = (c[:, I[f"{s}_winner"]]
                                             - c[:, I[f"{s}_loser"]])
    if write_outputs:
        coeff.to_parquet(intermediate_path("fm_coefficients_persist.parquet"),
                         index=False)

    # ---- RA cells + tier ----------------------------------------------------
    results = {}
    counts = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0}
    per_col = {col: {"Tier 1": 0, "Tier 2": 0, "FAIL": 0} for col in COLS6}
    for k in KLIST:
        c = c_by_k[k]
        for rname, spec in rows:
            s = row_series(c, spec)
            for jan, mask in (("janincl", mask_all), ("janexcl", mask_exjan)):
                col = f"k{k}_{jan}"
                val, t = ra_intercept_tstat(s, ff_arr, mask)
                for kind, v in (("val", val), ("tstat", t)):
                    mname = f"{col}_{rname}" + ("_tstat" if kind == "tstat" else "")
                    paper, tol = targets[mname]
                    tr = tier(paper, v, tol)
                    counts[tr] += 1
                    per_col[col][tr] += 1
                    results[(col, rname, kind)] = (v, paper, tol, tr)

    total = sum(counts.values())
    assert total == len(T6_ROWS) * len(COLS6) * 2 == 192, total

    # ---- reversal-pattern check (Jan-excl, by k) ---------------------------
    # Paper claim: jt_winner & mg_winner turn NEGATIVE (reversal); wh_winner &
    # wh_spread stay near zero / NOT significantly negative (no reversal).
    rev_rows = ["jt_winner", "mg_winner", "wh_winner", "wh_spread"]
    rev = {}
    for k in KLIST:
        col = f"k{k}_janexcl"
        rev[k] = {}
        for rname in rev_rows:
            v, pv, _, _ = results[(col, rname, "val")]
            t, pt, _, _ = results[(col, rname, "tstat")]
            rev[k][rname] = {"ours_v": v, "ours_t": t, "paper_v": pv, "paper_t": pt}

    # ---- write md -----------------------------------------------------------
    if write_outputs:
        L = [
            "# Table VI — George & Hwang (2004): Persistence of Profits "
            "(risk-adjusted, (6,k,12) strategies)",
            "",
            "Each month t (1963-07 .. 2001-12, 462) x formation lag j=2..13 x gap "
            "k in {12,24,36,48}: one cross-sectional OLS of R_{it}(%) on "
            "R_{i,t-1}(decimal), ln(mcap_$ at t-1), and 6 strategy dummies "
            "(JH/JL<-jt_sig, MH/ML<-mg_sig, FHH/FHL<-wh_sig_dc). Dummies from "
            "30/30 ordinal sorts at formation f=t-k-j (k-offset; shared "
            "tables_5.run_horizon engine). c_{k,t}=mean_j b_{k,j,t}. "
            "RISK-ADJUSTED ONLY: intercept + t-stat of c_{k,t} on FF3.",
            "Jan incl = all 462 t; Jan excl = month-of-year != 1.",
            "",
            f"Dependent variable R_it: panel column `{RET_COL}` "
            "(delisting-adjusted); R_{i,t-1} control, dummies, and sample rule "
            "on original ret.",
            "",
            "## Rankable stocks per formation month (avg by decade, per k)",
            "",
        ]
        decades = sorted({d for kv in rankable.values()
                          for v in kv.values() for d in v})
        L.append("| k | strategy | " + " | ".join(decades) + " |")
        L.append("|---:|---|" + "---:|" * len(decades))
        for k in KLIST:
            for s in STRAT_SIG:
                vals = rankable[k][s]
                L.append(f"| {k} | {s} ({STRAT_SIG[s]}) | "
                         + " | ".join(f"{vals.get(d, 0.0):.1f}" for d in decades)
                         + " |")
        L += ["", "## Diagnostics", ""]
        for k in KLIST:
            d = diag[k]
            L.append(f"- k={k}: avg sample {d['avg_sample']:.1f} "
                     f"(min {d['min_sample']}, max {d['max_sample']}), "
                     f"{d['n_reg']} regressions, {d['n_months_empty']} empty months")
        L += ["", f"## Overall hit rate (of {total})", ""]
        L.append(f"**Tier 1: {counts['Tier 1']} / Tier 2: {counts['Tier 2']} / "
                 f"FAIL: {counts['FAIL']}**")
        L += ["", "### Per-column tally", "",
              "| column | Tier 1 | Tier 2 | FAIL |", "|---|---:|---:|---:|"]
        for col in COLS6:
            cc = per_col[col]
            L.append(f"| {col} | {cc['Tier 1']} | {cc['Tier 2']} | {cc['FAIL']} |")
        L += ["", f"_{TIER2_LEGEND}_"]

        # detailed per-column tables
        for col in COLS6:
            L += ["", f"### Column: {col} (risk-adjusted)", "",
                  "| row | paper | ours | dev% | tier | paper_t | ours_t | tier_t |",
                  "|---|---:|---:|---:|---|---:|---:|---|"]
            for rname, _ in rows:
                v, pv, tol, tr = results[(col, rname, "val")]
                vt, pt, tolt, trt = results[(col, rname, "tstat")]
                L.append(f"| {rname} | {fmt(pv)} | {fmt(v)} | {dev_pct(pv, v)} "
                         f"| {tier_display(pv, v, tol)} | {fmt(pt)} | {fmt(vt)} "
                         f"| {tier_display(pt, vt, tolt)} |")

        # reversal-pattern check table
        L += ["", "## Reversal-pattern check (Jan-excl, by k)", "",
              "Paper claim: JT/MG winner dummies turn NEGATIVE (momentum "
              "reverses); 52-week-high winner + spread stay near zero / NOT "
              "significantly negative (no reversal). sig = |t| >= 1.96.", "",
              "| k | row | ours_v | ours_t | paper_v | paper_t | sign match | "
              "sig(ours) | sig(paper) |",
              "|---:|---|---:|---:|---:|---:|---|---|---|"]
        for k in KLIST:
            for rname in rev_rows:
                r = rev[k][rname]
                sm = (np.sign(r["ours_v"]) == np.sign(r["paper_v"])) or r["paper_v"] == 0
                so = abs(r["ours_t"]) >= 1.96
                sp = abs(r["paper_t"]) >= 1.96
                L.append(f"| {k} | {rname} | {fmt(r['ours_v'])} | {fmt(r['ours_t'],2)} "
                         f"| {fmt(r['paper_v'],2)} | {fmt(r['paper_t'],2)} "
                         f"| {'Y' if sm else 'NO'} | {'Y' if so else 'n'} "
                         f"| {'Y' if sp else 'n'} |")

        if SKIPPED_CELLS:
            L += ["", "## OCR-skipped cells", ""]
            for t, c, r, kd, note in SKIPPED_CELLS:
                if t == "T6":
                    L.append(f"- {c}/{r}/{kd}: {note}")

        LAYOUT.result_path("table_6.md").write_text("\n".join(L))

    if verbose:
        print()
        print(f"[T6] dependent `{RET_COL}`  OVERALL: T1 {counts['Tier 1']} / "
              f"T2 {counts['Tier 2']} / FAIL {counts['FAIL']} of {total}")
        print("REVERSAL-PATTERN (Jan-excl):")
        for k in KLIST:
            for rname in rev_rows:
                r = rev[k][rname]
                print(f"  k={k:2d} {rname:10s}  ours {r['ours_v']:7.4f} "
                      f"(t {r['ours_t']:6.2f})  paper {r['paper_v']:6.2f} "
                      f"(t {r['paper_t']:6.2f})")

    return {"results": results, "counts": counts, "per_col": per_col,
            "diag": diag, "rankable": rankable, "rev": rev, "coeff": coeff,
            "rows": rows, "total": total, "c_by_k": c_by_k}


# --- Table IX config --------------------------------------------------------

STRAT_SIG_IX = {"jt": "jt_sig", "mg": "mg_sig", "wl": "wh_lo_sig"}

CFG_IX = TableConfig(
    table_id="T9",
    strat_sig=STRAT_SIG_IX,
    coeff_parquet="fm_coefficients_low.parquet",
    md_name="table_9.md",
    title=("# Table IX — George & Hwang (2004): 52-week LOW replaces "
           "52-week high (Table V layout)"),
    dummy_pairs="JH/JL<-jt_sig, MH/ML<-mg_sig, FLH/FLL<-wh_lo_sig",
    preflight_rows=("intercept", "r_lag1", "size", "wl_spread"),
    paper_preflight={"intercept": 3.27, "r_lag1": -6.50, "size": -0.18,
                     "wl_spread": 0.13},
    preflight_gate=None,
)


def run_table_9(verbose: bool = True) -> dict:
    bundle = run_table(CFG_IX, ret_col=RET_COL, write_outputs=True,
                       enforce_gate=False, verbose=verbose)
    results = bundle["results"]

    # ---- corollary verification: wl_spread insignificant; jt_spread > T5 ----
    # Table V jt_spread (ours) from the official fm_coefficients.parquet.
    t5 = pd.read_parquet(intermediate_path("fm_coefficients.parquet"))
    mask_exjan = pd.DatetimeIndex(t5["month"]).month.to_numpy() != 1
    t5_jt_excl = float(t5["s66_jt_spread"].to_numpy()[mask_exjan].mean())
    t5_jt_incl = float(t5["s66_jt_spread"].mean())

    checks = []
    for col in COLS:
        v, pv, _, tr = results[(col, "wl_spread", "val")]
        t, pt, _, _ = results[(col, "wl_spread", "tstat")]
        checks.append((col, "wl_spread", v, t, pv, pt, tr, abs(t) < 1.96))
    jt_excl_v, jt_excl_pv = (results[("s66_raw_janexcl", "jt_spread", "val")][i]
                             for i in (0, 1))
    jt_excl_t = results[("s66_raw_janexcl", "jt_spread", "tstat")][0]

    extra = [
        "",
        "",
        "## Corollary verification (Table IX claims)",
        "",
        "Claim 1: the 52-week-LOW spread is economically small and "
        "INSIGNIFICANT (|t| < 1.96).",
        "",
        "| column | wl_spread ours | t | paper | paper_t | tier | insignificant? |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for col, _, v, t, pv, pt, tr, insig in checks:
        _, _, tol, _ = results[(col, "wl_spread", "val")]
        extra.append(f"| {col} | {fmt(v)} | {fmt(t,2)} | {fmt(pv,2)} "
                     f"| {fmt(pt,2)} | {tier_display(pv, v, tol)} "
                     f"| {'YES' if insig else 'no'} |")
    extra += [
        "",
        "Claim 2: JT spreads become LARGER than in Table V (low dummies absorb "
        "little, JT absorbs more).",
        "",
        "| quantity | Table V (ours) | Table IX (ours) | paper T5 | paper T9 |",
        "|---|---:|---:|---:|---:|",
        f"| jt_spread s66_raw_janexcl | {t5_jt_excl:.4f} | {jt_excl_v:.4f} "
        f"| 0.46 | {jt_excl_pv:.2f} |",
        f"| jt_spread s66_raw_janincl | {t5_jt_incl:.4f} | "
        f"{results[('s66_raw_janincl','jt_spread','val')][0]:.4f} | 0.38 | "
        f"{results[('s66_raw_janincl','jt_spread','val')][1]:.2f} |",
        "",
        f"- jt_spread s66_raw_janexcl: ours {jt_excl_v:.4f} (t {jt_excl_t:.2f}) "
        f"vs Table V ours {t5_jt_excl:.4f} -> "
        f"{'LARGER (matches paper)' if jt_excl_v > t5_jt_excl else 'not larger'}; "
        f"paper 0.46 (T5) -> 1.05 (T9).",
    ]
    if SKIPPED_CELLS:
        extra += ["", "## OCR-skipped / corrected cells", ""]
        for tb, c, r, kd, note in SKIPPED_CELLS:
            if tb == "T9":
                extra.append(f"- {c}/{r}/{kd}: {note}")
    extra.append("- OCR correction (not a skip): size s612_raw_janincl t-stat "
                 "'(3.68)' -> -3.68 (dropped minus; coef -0.17, Table V analog "
                 "-4.27).")

    out = LAYOUT.result_path("table_9.md")
    out.write_text(out.read_text() + "\n".join(extra) + "\n")

    if verbose:
        print()
        print("[T9] wl_spread insignificance + jt_spread>TableV checks:")
        for col, _, v, t, pv, pt, tr, insig in checks:
            print(f"  {col:18s} wl_spread {v:7.4f} (t {t:6.2f}) paper {pv:5.2f} "
                  f"(t {pt:5.2f}) {tr}  insig={insig}")
        print(f"  jt_spread s66_raw_janexcl: T9 {jt_excl_v:.4f} (t {jt_excl_t:.2f}) "
              f"vs T5 {t5_jt_excl:.4f}  -> larger={jt_excl_v > t5_jt_excl}")

    return bundle


# --- engine identity guard (Table V/VII unchanged by the additive edits) -----

def verify_identity(verbose: bool = True) -> dict:
    """Re-run CFG_V and CFG_VII under ret_dl (how the official caches were
    produced) with the CURRENT (edited) engine, in memory, and confirm the
    c_{k,t} series reproduce the official data/fm_coefficients*.parquet
    bit-exactly. Does NOT write any official artifact."""
    import hashlib

    from tables_5 import CFG_V
    from tables_7 import CFG_VII

    out = {}
    for cfg, fname in ((CFG_V, "fm_coefficients.parquet"),
                       (CFG_VII, "fm_coefficients_gh.parquet")):
        bundle = run_table(cfg, ret_col=RET_COL, write_outputs=False,
                           enforce_gate=False, verbose=False)
        new = bundle["coeff"].reset_index(drop=True)
        path = intermediate_path(fname)
        old = pd.read_parquet(path)
        # value-level bit identity (column set may be a superset for gh)
        common = [c for c in old.columns if c in new.columns]
        same = old[common].reset_index(drop=True).equals(new[common])
        # sha256 of the official file (before == after; file untouched) and of
        # a re-serialization of the freshly computed frame.
        sha_file = hashlib.sha256(path.read_bytes()).hexdigest()
        tmp = intermediate_path(f"_identity_{fname}")
        new.to_parquet(tmp, index=False)
        sha_new = hashlib.sha256(tmp.read_bytes()).hexdigest()
        tmp.unlink()
        out[fname] = {"values_identical": bool(same), "sha256_official": sha_file,
                      "sha256_recomputed": sha_new,
                      "byte_identical": sha_file == sha_new}
        if verbose:
            print(f"[identity] {fname}: values_identical={same} "
                  f"byte_identical={sha_file == sha_new}")
            print(f"           official  sha256 {sha_file}")
            print(f"           recomputed sha256 {sha_new}")
    return out


# --- main -------------------------------------------------------------------

def main() -> None:
    patch_targets_json()
    print("=" * 70)
    print("ENGINE IDENTITY GUARD (Table V/VII must be unchanged)")
    print("=" * 70)
    verify_identity()
    print("=" * 70)
    print("TABLE VI — persistence (6,k,12)")
    print("=" * 70)
    run_table_6()
    print("=" * 70)
    print("TABLE IX — 52-week low")
    print("=" * 70)
    run_table_9()


if __name__ == "__main__":
    main()
