"""Outer iteration 2 — [M4] long/short leg decomposition.

Paper claim (inputs/content.md L35, abstract): "Profitability of industry
strategies over intermediate horizons is predominantly driven by the long
positions. By contrast, the profitability of individual stock momentum
strategies is largely driven by selling past losers..." Paper §IV.A (L1121)
reports the industry (6,6) buy-side/sell-side evidence: Wi-Mid = 0.36%/mo,
Mid-Lo = 0.07%/mo. Paper §IV.B (L1159): the (1,1) industry strategy is
"equally driven by the long and the short sides."

Reads ONLY data/panel.parquet and data/bin_rets.parquet (plus a read-only
cross-check against results/cells_tables_1_2_3.json). Reuses the frozen
cohort engines from src/tables_1_2_3.py — build_global_cohorts,
individual_spread_series, industry_selections, industry_cohort_returns,
industry_strat_series, mean_t, restrict. Does NOT re-run the pipeline.

Outputs:
  results/legs_long_short.md — compact table + verdicts (cites L35/L1121/L1159)
  results/cells_legs.json    — per-metric ours/paper/status cells
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import tables_1_2_3 as t123  # noqa: E402  (engines, LAYOUT, RAW_START/END, mean_t)

LAYOUT = t123.LAYOUT
RAW_START, RAW_END = t123.RAW_START, t123.RAW_END
restrict, mean_t = t123.restrict, t123.mean_t


# ---------------------------------------------------------------------------
# individual (6,6) leg engine — same cohorts/weights as Table II raw
# ---------------------------------------------------------------------------

def individual_leg_series(ret_wide: pd.DataFrame, cohorts: dict,
                          hold: int = 6) -> tuple[pd.Series, pd.Series]:
    """Monthly overlapping winner-leg W(t) and loser-leg L(t) series from the
    shared cohorts/weights. Identical engine to
    tables_1_2_3.individual_spread_series (VW, fixed formation weights,
    renormalize on missing holding-month returns, average over the <=hold
    active cohorts at each t); a cohort-month counts only when BOTH legs have
    positive denominator, so W(t) - L(t) equals the spread engine exactly."""
    months_idx = ret_wide.index
    month_pos = {m: i for i, m in enumerate(months_idx)}
    col_pos = {c: j for j, c in enumerate(ret_wide.columns.to_numpy())}
    arr = ret_wide.to_numpy(dtype="float64")

    cohort_fs = sorted(cohorts.keys())
    f_pos = {f: i for i, f in enumerate(cohort_fs)}
    W_mat = np.full((len(cohort_fs), len(months_idx)), np.nan)
    L_mat = np.full((len(cohort_fs), len(months_idx)), np.nan)

    for f, (wp, ww, lp, lw) in cohorts.items():
        fi = f_pos[f]
        wcols = np.array([col_pos[p] for p in wp], dtype=np.int64)
        lcols = np.array([col_pos[p] for p in lp], dtype=np.int64)
        for k in range(hold):
            ri = month_pos.get(f + k)
            if ri is None:
                continue
            Rw = arr[ri, wcols]
            denw = ww[~np.isnan(Rw)].sum()
            Wret = float(np.nansum(Rw * ww) / denw) if denw > 0 else np.nan
            Rl = arr[ri, lcols]
            denl = lw[~np.isnan(Rl)].sum()
            Lret = float(np.nansum(Rl * lw) / denl) if denl > 0 else np.nan
            if not (np.isnan(Wret) or np.isnan(Lret)):
                W_mat[fi, ri] = Wret
                L_mat[fi, ri] = Lret

    def _cohort_avg(mat: np.ndarray) -> pd.Series:
        out = np.full(len(months_idx), np.nan)
        for ti in range(len(months_idx)):
            t = months_idx[ti]
            vals = []
            for k in range(hold):
                fi = f_pos.get(t - k)
                if fi is None:
                    continue
                v = mat[fi, ti]
                if not np.isnan(v):
                    vals.append(v)
            if vals:
                out[ti] = float(np.mean(vals))
        return pd.Series(out, index=months_idx)

    return _cohort_avg(W_mat), _cohort_avg(L_mat)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def contribution(leg: pd.Series, bench: pd.Series) -> pd.Series:
    """leg minus EW benchmark, aligned on the leg's month index."""
    return leg - bench.reindex(leg.index)


def tier_status(ours: float, paper: float, tol_pct: float) -> str:
    """Tier1 within tol_pct of paper; Tier2 same sign; FAIL opposite sign."""
    if abs(paper) < 1e-12:
        return "Tier1" if abs(ours) <= tol_pct / 100.0 else (
            "Tier2" if (ours >= 0) == (paper >= 0) else "FAIL")
    rel = abs(ours - paper) / abs(paper)
    if rel <= tol_pct / 100.0:
        return "Tier1"
    return "Tier2" if (ours >= 0) == (paper >= 0) else "FAIL"


def fmt_mt(m: float, t: float) -> str:
    return f"{m:.6f} (t={t:.3f})"


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def run() -> int:
    panel, ind = t123.load_data()
    print(f"panel {panel.shape}, bin_rets {ind.shape}")

    # ---- 1. market benchmarks ------------------------------------------------
    # r̄_t: monthly equal-weighted average of universe stock returns
    # (paper L246: "cross-sectional or equal-weighted average return";
    # footnote 14: ≈ EW index, 0.95 correlation)
    rbar = panel.groupby("month")["ret"].mean()
    rbar_raw = restrict(rbar, RAW_START, RAW_END)
    rbar_mean = float(rbar_raw.mean())
    # informational cross-check vs the panel's ew_mkt column (footnote 14)
    ew_mkt = panel.drop_duplicates("month").set_index("month")["ew_mkt"]
    ew_corr = float(rbar_raw.corr(ew_mkt.reindex(rbar_raw.index)))

    # r̄_ind_t: EW average of the 20 industry VW returns each month (fn 14)
    ind_vw_mat = ind.pivot(index="month", columns="ind",
                           values="ind_ret_vw").reindex(columns=np.arange(1, 21))
    months_idx = ind_vw_mat.index
    rbar_ind = ind_vw_mat.mean(axis=1)
    rbar_ind_raw = restrict(rbar_ind, RAW_START, RAW_END)
    rbar_ind_mean = float(rbar_ind_raw.mean())

    print(f"r_bar mean 1963-07..1995-07: {rbar_mean:.6f} "
          f"(corr vs ew_mkt {ew_corr:.4f}, T={len(rbar_raw)})")
    print(f"r_bar_ind mean: {rbar_ind_mean:.6f} (T={len(rbar_ind_raw)})")

    # ---- 2. individual (6,6) legs --------------------------------------------
    cohorts = t123.build_global_cohorts(panel)
    print(f"{len(cohorts)} formable individual cohorts")
    ret_wide = panel.pivot(index="month", columns="permno", values="ret")
    W, L = individual_leg_series(ret_wide, cohorts, hold=6)
    spread_ref = t123.individual_spread_series(ret_wide, cohorts, hold=6)

    W_r = restrict(W, RAW_START, RAW_END)
    L_r = restrict(L, RAW_START, RAW_END)
    spr_r = restrict(W - L, RAW_START, RAW_END)

    # integrity: leg spread == frozen Table II-A raw spread, bit-for-bit
    ref_r = restrict(spread_ref, RAW_START, RAW_END)
    max_dev = float((spr_r - ref_r).abs().max())
    assert max_dev < 1e-10, f"leg W-L deviates from spread engine: {max_dev}"
    spr_m, spr_t, T_spr = mean_t(spr_r)
    assert round(spr_m, 6) == 0.004135 and round(spr_t, 3) == 2.311, (
        f"individual spread integrity failed: {spr_m:.6f}/{spr_t:.3f}")

    stk_long = restrict(contribution(W, rbar), RAW_START, RAW_END)
    stk_short = restrict(contribution(rbar, L), RAW_START, RAW_END)
    stk_long_m, stk_long_t, T_stk = mean_t(stk_long)
    stk_short_m, stk_short_t, _ = mean_t(stk_short)
    W_m, W_t, _ = mean_t(W_r)
    L_m, L_t, _ = mean_t(L_r)
    stk_loser_driven = 1 if stk_short_m > stk_long_m else 0
    stk_verdict = "loser-driven" if stk_loser_driven else "long-driven"
    print(f"individual (6,6): W={W_m:.6f} L={L_m:.6f} | "
          f"long {stk_long_m:.6f} (t={stk_long_t:.3f}) | "
          f"short {stk_short_m:.6f} (t={stk_short_t:.3f}) | "
          f"spread {spr_m:.6f} (t={spr_t:.3f}) -> {stk_verdict}")

    # ---- 3. industry (6,6) legs ------------------------------------------------
    sig6 = ind.pivot(index="month", columns="ind",
                     values="ind_mom6").reindex(columns=np.arange(1, 21))
    sels6 = t123.industry_selections(sig6)
    Wi, Mid, Lo, f_list, f_pos = t123.industry_cohort_returns(
        sels6, ind_vw_mat, months_idx, max_hold=6)
    wi_s = t123.industry_strat_series(Wi, f_list, f_pos, months_idx, 6, "A")
    lo_s = t123.industry_strat_series(Lo, f_list, f_pos, months_idx, 6, "A")
    mid_s = t123.industry_strat_series(Mid, f_list, f_pos, months_idx, 6, "A")

    ind_spr_r = restrict(wi_s - lo_s, RAW_START, RAW_END)
    ind_spr_m, ind_spr_t, T_ind = mean_t(ind_spr_r)
    assert round(ind_spr_m, 6) == 0.003972 and round(ind_spr_t, 3) == 2.359, (
        f"industry spread integrity failed: {ind_spr_m:.6f}/{ind_spr_t:.3f}")

    ind_long = restrict(contribution(wi_s, rbar_ind), RAW_START, RAW_END)
    ind_short = restrict(contribution(rbar_ind, lo_s), RAW_START, RAW_END)
    ind_long_m, ind_long_t, _ = mean_t(ind_long)
    ind_short_m, ind_short_t, _ = mean_t(ind_short)
    wi_m, wi_t, _ = mean_t(restrict(wi_s, RAW_START, RAW_END))
    lo_m, lo_t, _ = mean_t(restrict(lo_s, RAW_START, RAW_END))
    ind_long_driven = 1 if ind_long_m > ind_short_m else 0
    ind_verdict = "long-driven" if ind_long_driven else "loser-driven"

    # Wi-Mid / Mid-Lo vs paper (L1121: 0.0036 / 0.0007)
    wimid_r = restrict(wi_s - mid_s, RAW_START, RAW_END)
    midlo_r = restrict(mid_s - lo_s, RAW_START, RAW_END)
    wimid_m, wimid_t, _ = mean_t(wimid_r)
    midlo_m, midlo_t, _ = mean_t(midlo_r)
    wimid_status = tier_status(wimid_m, 0.0036, 30.0)
    midlo_status = tier_status(midlo_m, 0.0007, 30.0)
    print(f"industry (6,6): Wi={wi_m:.6f} Lo={lo_m:.6f} | "
          f"long {ind_long_m:.6f} (t={ind_long_t:.3f}) | "
          f"short {ind_short_m:.6f} (t={ind_short_t:.3f}) | "
          f"spread {ind_spr_m:.6f} (t={ind_spr_t:.3f}) -> {ind_verdict}")
    print(f"industry (6,6) Wi-Mid={wimid_m:.6f} (paper 0.0036, {wimid_status}); "
          f"Mid-Lo={midlo_m:.6f} (paper 0.0007, {midlo_status})")

    # ---- 4. industry (1,1) legs (paper §IV.B L1159) ----------------------------
    sig1 = ind.pivot(index="month", columns="ind",
                     values="ind_mom1").reindex(columns=np.arange(1, 21))
    sels1 = t123.industry_selections(sig1)
    Wi1, Mid1, Lo1, fl1, fp1 = t123.industry_cohort_returns(
        sels1, ind_vw_mat, months_idx, max_hold=1)
    wi1_s = t123.industry_strat_series(Wi1, fl1, fp1, months_idx, 1, "A")
    lo1_s = t123.industry_strat_series(Lo1, fl1, fp1, months_idx, 1, "A")

    ind11_spr_r = restrict(wi1_s - lo1_s, RAW_START, RAW_END)
    ind11_spr_m, ind11_spr_t, T_11 = mean_t(ind11_spr_r)
    ind11_long = restrict(contribution(wi1_s, rbar_ind), RAW_START, RAW_END)
    ind11_short = restrict(contribution(rbar_ind, lo1_s), RAW_START, RAW_END)
    ind11_long_m, ind11_long_t, _ = mean_t(ind11_long)
    ind11_short_m, ind11_short_t, _ = mean_t(ind11_short)
    wi1_m, _, _ = mean_t(restrict(wi1_s, RAW_START, RAW_END))
    lo1_m, _, _ = mean_t(restrict(lo1_s, RAW_START, RAW_END))
    ind11_balanced = 1 if abs(ind11_long_m - ind11_short_m) <= 0.002 else 0
    ind11_verdict = ("balanced (long≈short)" if ind11_balanced else
                     ("long-driven" if ind11_long_m > ind11_short_m
                      else "loser-driven"))
    print(f"industry (1,1): Wi={wi1_m:.6f} Lo={lo1_m:.6f} | "
          f"long {ind11_long_m:.6f} (t={ind11_long_t:.3f}) | "
          f"short {ind11_short_m:.6f} (t={ind11_short_t:.3f}) | "
          f"spread {ind11_spr_m:.6f} (t={ind11_spr_t:.3f}) -> {ind11_verdict}")

    # ---- cross-check recomputed Wi-Mid/Mid-Lo vs frozen cells JSON -------------
    cells_path = LAYOUT.result_path("cells_tables_1_2_3.json")
    frozen = {c["metric"]: c["ours"]
              for c in json.loads(cells_path.read_text())}
    for label, ours_v, key in [("Wi-Mid", wimid_m, "pA_L6_H6_wimid"),
                               ("Mid-Lo", midlo_m, "pA_L6_H6_midlo"),
                               ("stk spread", spr_m, "pA_raw_mean"),
                               ("ind spread", ind_spr_m, "pB_raw_industry_mean")]:
        ref_v = frozen.get(key)
        assert ref_v is not None and abs(ours_v - ref_v) < 1e-12, (
            f"{label} mismatch vs frozen cells: {ours_v} vs {ref_v}")
    print("cross-check vs results/cells_tables_1_2_3.json: exact match")

    # ---- 6. cells_legs.json ----------------------------------------------------
    stk_status = ("corroborates_claim" if stk_loser_driven
                  else "contradicts_claim")
    ind_status = ("corroborates_claim" if ind_long_driven
                  else "contradicts_claim")
    cells = [
        dict(metric="stk_66_long_contrib", ours=stk_long_m, paper=None,
             unit="monthly return", status=stk_status),
        dict(metric="stk_66_short_contrib", ours=stk_short_m, paper=None,
             unit="monthly return", status=stk_status),
        dict(metric="stk_66_loser_driven", ours=stk_loser_driven, paper=1,
             unit="binary", status="PASS" if stk_loser_driven == 1 else "FAIL"),
        dict(metric="ind_66_long_contrib", ours=ind_long_m, paper=None,
             unit="monthly return", status=ind_status),
        dict(metric="ind_66_short_contrib", ours=ind_short_m, paper=None,
             unit="monthly return", status=ind_status),
        dict(metric="ind_66_long_driven", ours=ind_long_driven, paper=1,
             unit="binary", status="PASS" if ind_long_driven == 1 else "FAIL"),
        dict(metric="ind_11_balanced", ours=ind11_balanced, paper=1,
             unit="binary", status="PASS" if ind11_balanced == 1 else "FAIL"),
        dict(metric="ind_66_wimid", ours=wimid_m, paper=0.0036,
             unit="monthly return", status=wimid_status),
        dict(metric="ind_66_midlo", ours=midlo_m, paper=0.0007,
             unit="monthly return", status=midlo_status),
    ]
    out_json = LAYOUT.result_path("cells_legs.json")
    out_json.write_text(json.dumps(cells, indent=1))

    # ---- 5. results/legs_long_short.md -----------------------------------------
    def match_str(ours_ok: bool) -> str:
        return "YES — matches paper" if ours_ok else "NO — contradicts paper"

    def match_phrase(ours_ok: bool) -> str:
        return ("matching the paper's claim" if ours_ok
                else "contradicting the paper's claim")

    md = []
    md.append("# Long/short leg decomposition — audit issue [M4] "
              "(Moskowitz & Grinblatt 1999)")
    md.append("")
    md.append("**Paper claim (abstract, inputs/content.md L35):** "
              "\"Profitability of industry strategies over intermediate "
              "horizons is predominantly driven by the long positions. By "
              "contrast, the profitability of individual stock momentum "
              "strategies is largely driven by selling past losers...\"")
    md.append("")
    md.append("Paper §IV.A (L1121): industry (6,6) buy-side Wi−Mid = 0.36%/mo "
              "vs sell-side Mid−Lo = 0.07%/mo — \"industry momentum strategies "
              "appear to profit mostly on the buy side.\" Paper §IV.B (L1159): "
              "the (1,1) industry strategy is \"equally driven by the long and "
              "the short sides,\" unlike the (6,6).")
    md.append("")
    md.append(f"Window: 1963-07..1995-07 (T={T_spr} monthly observations). "
              "Benchmarks: r̄ = monthly equal-weighted average of universe "
              f"stock returns (L246; footnote 14 — corr vs EW index = "
              f"{ew_corr:.3f} in our panel), mean = {rbar_mean:.6f}/mo; "
              "r̄_ind = monthly EW average of the 20 industry VW returns "
              f"(footnote 14), mean = {rbar_ind_mean:.6f}/mo.")
    md.append("")
    md.append("Engines reused unchanged from src/tables_1_2_3.py (frozen "
              "panel; cohorts identical to Table II raw: 30/30 on mom6, VW, "
              "fixed formation weights, 6-cohort overlapping average; industry "
              "top-3/bottom-3 by ind_mom, EW across the 3 industries, held H "
              "months, overlapping average of monthly VW industry returns). "
              "Leg contributions: long = leg − benchmark; short = benchmark − "
              "loser leg; t-stats are time-series t on the monthly "
              "contribution series (A9).")
    md.append("")
    md.append("## Main table")
    md.append("")
    md.append("| Strategy | Long leg mean | Short leg mean | Long contrib "
              "(t) | Short contrib (t) | Spread (t) | Driver (ours) | Paper "
              "claim | Matches? |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    md.append(f"| Individual (6,6) VW | W = {W_m:.6f} | L = {L_m:.6f} | "
              f"{stk_long_m:+.6f} (t={stk_long_t:.2f}) | "
              f"{stk_short_m:+.6f} (t={stk_short_t:.2f}) | "
              f"{spr_m:.6f} (t={spr_t:.2f}) | **{stk_verdict}** "
              f"(short {'>' if stk_loser_driven else '≤'} long) | "
              f"loser-driven | {match_str(bool(stk_loser_driven))} |")
    md.append(f"| Industry (6,6) | Wi = {wi_m:.6f} | Lo = {lo_m:.6f} | "
              f"{ind_long_m:+.6f} (t={ind_long_t:.2f}) | "
              f"{ind_short_m:+.6f} (t={ind_short_t:.2f}) | "
              f"{ind_spr_m:.6f} (t={ind_spr_t:.2f}) | **{ind_verdict}** "
              f"(long {'>' if ind_long_driven else '≤'} short) | "
              f"long-driven | {match_str(bool(ind_long_driven))} |")
    md.append(f"| Industry (1,1) | Wi = {wi1_m:.6f} | Lo = {lo1_m:.6f} | "
              f"{ind11_long_m:+.6f} (t={ind11_long_t:.2f}) | "
              f"{ind11_short_m:+.6f} (t={ind11_short_t:.2f}) | "
              f"{ind11_spr_m:.6f} (t={ind11_spr_t:.2f}) | "
              f"**{ind11_verdict}** (|long−short| = "
              f"{abs(ind11_long_m - ind11_short_m):.6f} "
              f"{'≤' if ind11_balanced else '>'} 0.002) | balanced "
              f"(equal-drive) | {match_str(bool(ind11_balanced))} |")
    md.append("")
    md.append("Contributions sum to the spread: long + short = mean(W) − "
              "mean(L) by construction (monthly r̄ cancels).")
    md.append("")
    md.append("## Industry (6,6) buy-side vs sell-side vs paper (L1121)")
    md.append("")
    md.append("| Split | Ours mean (t) | Paper | Status |")
    md.append("|---|---|---|---|")
    md.append(f"| Wi−Mid (buy side) | {wimid_m:.6f} (t={wimid_t:.2f}) | "
              f"0.0036 | {wimid_status} (30% band) |")
    md.append(f"| Mid−Lo (sell side) | {midlo_m:.6f} (t={midlo_t:.2f}) | "
              f"0.0007 | {midlo_status} (30% band) |")
    md.append("")
    ours_buyside_leads = wimid_m > midlo_m
    md.append(f"In our vintage the buy side ({wimid_m:.4f}) "
              f"{'exceeds' if ours_buyside_leads else 'does not exceed'} the "
              f"sell side ({midlo_m:.4f}); the paper's ordering is "
              f"Wi−Mid 0.0036 > Mid−Lo 0.0007 (buy-side-dominated). "
              + ("The direction of the split matches the paper."
                 if ours_buyside_leads else
                 "The magnitudes/ordering differ from the paper — reported "
                 "honestly as a vintage finding (same family as the Table III "
                 "Wi/Lo-level Tier-2 cells)."))
    md.append("")
    md.append("## Verdicts")
    md.append("")
    md.append(f"1. **Individual (6,6):** the short leg (r̄ − L) contributes "
              f"{stk_short_m:+.6f}/mo (t={stk_short_t:.2f}) vs the long leg "
              f"(W − r̄) {stk_long_m:+.6f}/mo (t={stk_long_t:.2f}) — "
              f"individual momentum is **{stk_verdict}**, "
              f"{match_phrase(bool(stk_loser_driven))} (abstract L35). "
              f"Consistent with the audit's independent recompute "
              f"(short ≈ +0.0040 vs long ≈ +0.0002).")
    md.append(f"2. **Industry (6,6):** the long leg contributes "
              f"{ind_long_m:+.6f}/mo (t={ind_long_t:.2f}) vs the short leg "
              f"{ind_short_m:+.6f}/mo (t={ind_short_t:.2f}) — industry "
              f"momentum is **{ind_verdict}**, "
              f"{match_phrase(bool(ind_long_driven))} (abstract L35).")
    md.append(f"3. **Industry (1,1):** long {ind11_long_m:+.6f} vs short "
              f"{ind11_short_m:+.6f} — **{ind11_verdict}**; paper §IV.B "
              f"(L1159) claims equal drive — "
              f"{match_phrase(bool(ind11_balanced))}.")
    md.append("")
    md.append("## Integrity checks (reproduce frozen results)")
    md.append("")
    md.append(f"- Individual (6,6) spread from legs: {spr_m:.6f} / t={spr_t:.3f} "
              "(frozen Table II raw: 0.004135 / 2.311) — reproduced; leg "
              f"W−L series equals individual_spread_series output (max dev "
              f"{max_dev:.2e}).")
    md.append(f"- Industry (6,6) spread: {ind_spr_m:.6f} / t={ind_spr_t:.3f} "
              "(frozen Table II-B/III: 0.003972 / 2.359) — reproduced.")
    md.append("- Recomputed Wi−Mid / Mid−Lo and both spreads match "
              "results/cells_tables_1_2_3.json to <1e-12.")
    md.append("")
    (LAYOUT.result_path("legs_long_short.md")).write_text("\n".join(md) + "\n")

    # ---- stdout -----------------------------------------------------------------
    print("\n=== cells_legs.json ===")
    print(json.dumps(cells, indent=1))
    summary = (f"VERDICT: individual (6,6) {stk_verdict} "
               f"(short {stk_short_m:+.4f} vs long {stk_long_m:+.4f}; paper "
               f"loser-driven -> {'PASS' if stk_loser_driven else 'FAIL'}); "
               f"industry (6,6) {ind_verdict} (long {ind_long_m:+.4f} vs "
               f"short {ind_short_m:+.4f}; paper long-driven -> "
               f"{'PASS' if ind_long_driven else 'FAIL'}); industry (1,1) "
               f"{ind11_verdict} (|Δ|={abs(ind11_long_m - ind11_short_m):.4f}"
               f"; paper balanced -> "
               f"{'PASS' if ind11_balanced else 'FAIL'})")
    print(summary)
    print(f"wrote {out_json.name} and legs_long_short.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
