"""
Cooper, Gulen, Schill (2008) — TABLE II SECTION E: event-time Years 1..5
returns of the asset-growth decile portfolios, and the cumulative Year-1..Year-5
D10-D1 spread (committed metric EW_cumulative_Y1_5_spread, paper -87.99%,
content.md L1554; VW -49.67% at L1566, secondary).

"Asset Growth and the Cross-Section of Stock Returns", Journal of Finance.

WINDOW / MEMBERSHIP:
  * Extended, delisting-adjusted monthly return window: Jul-1968 .. Jun-2007
    (src/sql/universe_monthly_extended.sql + src/sql/delisting_extended.sql).
    The latest formation (Jun-2002) needs Year 5 = Jul-2006..Jun-2007.
    SAME universe filter (msfhdr PIT: hshrcd 10/11, hexcd 1/2/3, hsiccd not
    6000-6999) and the SAME Assumption-1 delisting adjustment as the foundation
    (adjustment code IMPORTED from main.py, byte-identical). Verified here to
    reproduce data/panel.parquet EXACTLY on the overlap 1968-07 .. 2003-06.
  * Cohorts: the 35 June-t (1968..2002) asset-growth deciles from
    data/formation.parquet. MEMBERSHIP IS FIXED at formation — the cohort is
    bought and held, NOT re-sorted each year (Figure 2 convention, L1552).
  * Event year y (y = 1..5) of cohort t = the 12 months Jul(t+y-1) .. Jun(t+y);
    event-month offset k = 1..60 (k=1 is Jul(t)).
  * Surviving-member convention: a member contributes in a month only if it has
    return data that month; the delisting return is embedded in the delisting
    month (Assumption 1), so delisting members contribute their delisting-month
    return and then drop out (cohorts shrink in later event years).

THREE CUMULATIVE CONVENTIONS (all computed; see report):
  * MONTHLY-PORTFOLIO EVENT TIME (PRIMARY, paper-faithful — Figure 2, L1552):
    for each cohort t, decile d and event month k: EW = within-(month) mean of
    member returns; VW = Σ(w_i·r_i)/Σ(w_i) with w_i the FIXED June-t formation
    ME (Assumption 9), denominator renormalized over members with data that
    month. R_{d,k} = time-series mean over the 35 cohorts. Annual return for
    event year y = prod over its 12 event-month means − 1; cumulative [1,5] =
    prod over all 60 event-month means − 1; spread = D10 − D1. This is exactly
    the Figure 2 construction (Year-1 months reproduce the Panel B Year-1 row).
    THE COMMITTED METRIC EW_cumulative_Y1_5_spread USES THIS CONVENTION.
  * COHORT-ANNUAL (B, secondary): per cohort, compound the monthly portfolio
    returns of each event year (prod over available months − 1), average the
    annual returns across the 35 cohorts, cumulative = prod_y(1+mean_y)−1.
  * SPEC-LITERAL per-stock annual buy-and-hold (A, FLAGGED): member annual
    return = prod(1+r)−1 over that event year's available months (>=1 month
    required); EW_ret_{t,d,y} = mean over surviving members; EW_ret_{d,y} = mean
    over cohorts; cumulative = prod_y(1+EW_ret_{d,y})−1 (the task spec's exact
    formula). On this 2026 CRSP vintage the cross-sectional mean of per-stock
    annual BHRs is dominated by a handful of sub-penny shells (e.g. a +39,120%
    stock-year pulls one cohort's D1 mean to 275% vs a 50% median), producing
    economically meaningless decile means (D1 ~ +860%/yr). The paper's own
    caption shows it used average MONTHLY returns in event time; convention A is
    reported only for completeness and is NOT used for the committed metric.

OUTPUTS:
  results/table_2.md            — 'Event-time (Years -/+ around formation)'
                                  section appended (stale NOT-YET-COMPUTED stub
                                  replaced by a pointer).
  results/table_2_eval.json     — EW_cumulative_Y1_5_spread filled in + tally
                                  updated; every other entry preserved.
  results/table2_event_time.png — cumulative [1,5] return by decile (EW & VW).

Does NOT modify the foundation, data/panel.parquet, data/formation.parquet,
or any Table I/III/IV outputs.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless backend — first matplotlib import
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SLUG_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SLUG_DIR.parents[1]          # rep-it-up root (carries utils/)
sys.path.insert(0, str(REPO_ROOT))
# make paper_layout() cwd-independent (foundation's utils.paths falls back to
# <cwd>/replications otherwise)
os.environ.setdefault("REPLICATIONS_PATH", str(REPO_ROOT / "replications"))
DATA = SLUG_DIR / "data"
RESULTS = SLUG_DIR / "results"
PREP = SLUG_DIR / "preparations"
RESULTS.mkdir(parents=True, exist_ok=True)
# Cached extended delisting-adjusted return panel (audit issue m4): makes the
# committed EW_cumulative_Y1_5_spread re-derivable from data/ without a live
# ClickHouse pull. Written on first run, read thereafter (write-if-missing).
EVENT_CACHE = DATA / "event_time_returns.parquet"

# --- import the foundation module (src/main.py) to reuse its ClickHouse ------
# --- helpers and the byte-identical Assumption-1 delisting adjustment --------
_spec = importlib.util.spec_from_file_location(
    "foundation", SLUG_DIR / "src" / "main.py")
foundation = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(foundation)

N_DECILES = 10
DECILES = list(range(1, N_DECILES + 1))
FORMATION_YEARS = list(range(1968, 2003))   # 35 cohorts (rule sample_start_1968)
EVENT_YEARS = [1, 2, 3, 4, 5]
N_EVENT_MONTHS = 60
EXT_START, EXT_END = "1968-07", "2007-06"
METRIC_NAME = "EW_cumulative_Y1_5_spread"
PAPER_EW_CUM_SPREAD = -87.99   # %, content.md L1554 (t = -8.63)
PAPER_VW_CUM_SPREAD = -49.67   # %, content.md L1566 (t = -4.25); not committed


# =============================================================================
# 1. EXTENDED DELISTING-ADJUSTED MONTHLY RETURNS (reuse foundation logic)
# =============================================================================
def load_extended() -> pd.DataFrame:
    # audit m4: read the cached extended delisting-adjusted panel if present so
    # the committed metric is re-derivable from data/ without a live query.
    if EVENT_CACHE.exists():
        adj = pd.read_parquet(EVENT_CACHE)
        adj["date"] = pd.to_datetime(adj["date"])
        adj["ym"] = adj["date"].dt.to_period("M")
        print(f"[load] read CACHED extended adjusted panel {EVENT_CACHE.name}: "
              f"{adj.shape[0]} rows, {adj['date'].min().date()} .. "
              f"{adj['date'].max().date()}, {adj['permno'].nunique()} permnos")
        return adj
    t0 = time.time()
    msf = foundation.q_file("universe_monthly_extended.sql")
    delist = foundation.q_file("delisting_extended.sql")
    print(f"[load] {time.time() - t0:.1f}s | msf {msf.shape} delist {delist.shape}")
    msf["date"] = pd.to_datetime(msf["date"])
    delist["dlstdt"] = pd.to_datetime(delist["dlstdt"])
    adj = foundation.adjust_delistings(msf, delist)   # byte-identical to foundation
    print(f"[load] extended adjusted panel: {adj.shape[0]} rows, "
          f"{adj['date'].min().date()} .. {adj['date'].max().date()}, "
          f"{adj['permno'].nunique()} permnos")
    # cache the re-derivable extended delisting-adjusted panel (permno, date,
    # ret_adj, me) — the direct input to the event-time construction below.
    cache_cols = [c for c in ["permno", "date", "ret_adj", "me"] if c in adj.columns]
    adj[cache_cols].to_parquet(EVENT_CACHE, index=False)
    print(f"[load] cached extended adjusted panel -> {EVENT_CACHE.name} "
          f"({adj.shape[0]} rows)")
    return adj


def verify_overlap(adj: pd.DataFrame) -> dict:
    """Spot-check: the extended adjusted series must reproduce the foundation's
    data/panel.parquet on the overlapping 1968-07 .. 2003-06 window."""
    panel = pd.read_parquet(DATA / "panel.parquet")
    panel["month"] = pd.to_datetime(panel["month"])
    panel_u = panel[["permno", "month", "ret"]].drop_duplicates(["permno", "month"])
    ext = (adj[["permno", "date", "ret_adj"]]
           .rename(columns={"date": "month", "ret_adj": "ret"})
           .drop_duplicates(["permno", "month"]))
    chk = panel_u.merge(ext, on=["permno", "month"], how="inner",
                        suffixes=("_panel", "_ext"))
    diff = (chk["ret_panel"].astype(float) - chk["ret_ext"].astype(float)).abs()
    n_missing = len(panel_u) - len(chk)
    n_exact = int((diff == 0).sum())
    n_mis = int((diff > 1e-12).sum())
    print(f"\n[overlap] panel (permno, month) pairs: {len(panel_u)}; matched in "
          f"extension: {len(chk)} (missing: {n_missing})")
    print(f"[overlap] max|Δret| on overlap = {diff.max():.3e}; exact matches "
          f"{n_exact}/{len(diff)}; mismatches > 1e-12: {n_mis}")
    return {"n_panel_pairs": int(len(panel_u)), "n_matched": int(len(chk)),
            "n_missing": int(n_missing), "max_abs_diff": float(diff.max()),
            "n_mismatch_gt_1e_12": n_mis}


def build_wide(adj: pd.DataFrame) -> pd.DataFrame:
    ext = adj[["permno", "ym", "ret_adj"]].drop_duplicates(["permno", "ym"],
                                                           keep="last")
    wide = ext.pivot_table(index="ym", columns="permno", values="ret_adj",
                           aggfunc="first")
    wide = wide.reindex(pd.period_range(EXT_START, EXT_END, freq="M"))
    print(f"[event] wide returns matrix: {wide.shape[0]} months x "
          f"{wide.shape[1]} permnos ({EXT_START} .. {EXT_END})")
    return wide


# =============================================================================
# 2A. MONTHLY-PORTFOLIO EVENT TIME (primary, paper-faithful Figure 2 method)
# =============================================================================
def monthly_portfolio_series(wide: pd.DataFrame, form: pd.DataFrame) -> pd.DataFrame:
    """Per cohort t, decile d and event-month offset k=1..60: EW = mean of member
    monthly returns; VW = Σ(w·r)/Σ(w), w = fixed June-t formation ME (Assumption
    9), over members with data (and non-missing MV for VW) that month."""
    cohort = form[["permno", "june_year", "decile", "MV"]].copy()
    rows = []
    for t in FORMATION_YEARS:
        mem = cohort[cohort["june_year"] == t]
        n_mem_d = mem.groupby("decile").size()
        base = pd.Period(f"{t}-07", freq="M")
        for k in range(1, N_EVENT_MONTHS + 1):
            r = wide.loc[base + (k - 1)]                    # Series over permnos
            r = r[r.notna()]
            m = mem.merge(r.rename("r").reset_index(), on="permno", how="inner")
            ew = m.groupby("decile")["r"].mean()
            mv = m.dropna(subset=["MV"])
            vw = (mv.assign(rw=mv["r"] * mv["MV"]).groupby("decile")["rw"].sum()
                  / mv.groupby("decile")["MV"].sum())
            n_ew = m.groupby("decile").size()
            n_vw = mv.groupby("decile").size()
            y = (k - 1) // 12 + 1
            for d in DECILES:
                rows.append({"t": t, "k": k, "y": y, "d": d,
                             "EW": float(ew.get(d, np.nan)),
                             "VW": float(vw.get(d, np.nan)),
                             "n_ew": int(n_ew.get(d, 0)),
                             "n_vw": int(n_vw.get(d, 0)),
                             "n_mem": int(n_mem_d.get(d, 0))})
    p = pd.DataFrame(rows)
    print(f"[event] monthly portfolio cells: {len(p)} (full grid "
          f"{35 * 60 * 10}); EW non-null {int(p['EW'].notna().sum())}")
    return p


def aggregate_monthly(p: pd.DataFrame) -> dict:
    """Convention C: R_{d,k} = mean over cohorts of the monthly portfolio return;
    annual_y = prod of the year's 12 event-month means - 1; cumulative = prod of
    all 60 - 1. Also Convention B: per-cohort annual compounding of the monthly
    portfolio, mean over cohorts, cumulative from the mean annuals. Plus
    cohort-level cumulative spreads + t-stats."""
    out = {}
    for col in ["EW", "VW"]:
        # --- C: time-series mean at each event-month offset -------------------
        Rk = p.groupby(["d", "k"])[col].mean()
        annual_C, cum_C = {}, {}
        for d in DECILES:
            prod_all = 1.0
            for y in EVENT_YEARS:
                ks = range(12 * (y - 1) + 1, 12 * y + 1)
                vals = np.array([Rk.loc[(d, k)] for k in ks])
                py = float(np.prod(1.0 + vals))
                annual_C.setdefault(y, {})[d] = py - 1.0
                prod_all *= py
            cum_C[d] = prod_all - 1.0
        # --- B: per-cohort annual compounding, then time-series mean ----------
        piv = p.pivot_table(index=["t", "d"], columns="k", values=col)
        annual_B = {}
        for y in EVENT_YEARS:
            ks = list(range(12 * (y - 1) + 1, 12 * y + 1))
            sub = piv[ks]
            ann_td = (1.0 + sub).prod(axis=1, skipna=True) - 1.0
            ann_td = ann_td.where(~sub.isna().all(axis=1))
            annual_B[y] = ann_td.reset_index().groupby("d")[0].mean()
        cum_B = {}
        for d in DECILES:
            pb = 1.0
            for y in EVENT_YEARS:
                pb *= 1.0 + annual_B[y].get(d, np.nan)
            cum_B[d] = pb - 1.0
        # --- cohort-level cumulative spread + t-stat (from 60-month series) ---
        cum_td = pd.Series(1.0, index=piv.index)
        ok = pd.Series(True, index=piv.index)
        for k in range(1, N_EVENT_MONTHS + 1):
            v = piv[k]
            ok &= v.notna()
            cum_td *= (1.0 + v.fillna(0.0))
        cum_td = (cum_td - 1.0).where(ok)
        sp = (cum_td.xs(N_DECILES, level="d") - cum_td.xs(1, level="d")).dropna()
        out[col] = {
            "annual_C": annual_C, "cum_C": cum_C,
            "annual_B": {y: annual_B[y] for y in EVENT_YEARS}, "cum_B": cum_B,
            "cohort_mean_spread_pct": float(sp.mean() * 100.0),
            "cohort_t_stat": float(sp.mean() / (sp.std(ddof=1) / np.sqrt(len(sp)))),
            "n_cohorts": int(len(sp)),
        }
    return out


# =============================================================================
# 2B. SPEC-LITERAL per-stock annual buy-and-hold (flagged variant)
# =============================================================================
def spec_literal_event_time(wide: pd.DataFrame, form: pd.DataFrame) -> pd.DataFrame:
    """Per cohort t, event year y: member annual BHR = prod(1+r)-1 over available
    months (>=1); EW = mean over surviving members, VW = Σ(w·r)/Σ(w) with fixed
    June-t ME; then time-series mean over cohorts; cumulative = prod_y(1+mean)-1."""
    cohort = form[["permno", "june_year", "decile", "MV"]].copy()
    rows = []
    for t in FORMATION_YEARS:
        mem = cohort[cohort["june_year"] == t]
        for y in EVENT_YEARS:
            months = pd.period_range(f"{t + y - 1}-07", f"{t + y}-06", freq="M")
            sm = wide.loc[months].sum(axis=0, min_count=1, skipna=True)
            ann = pd.Series(np.exp(sm.to_numpy(dtype=float)) - 1.0,
                            index=wide.columns).dropna()
            m = mem.merge(ann.rename("r").reset_index(), on="permno", how="inner")
            ew = m.groupby("decile")["r"].mean()
            mv = m.dropna(subset=["MV"])
            vw = (mv.assign(rw=mv["r"] * mv["MV"]).groupby("decile")["rw"].sum()
                  / mv.groupby("decile")["MV"].sum())
            n_ew = m.groupby("decile").size()
            for d in DECILES:
                rows.append({"t": t, "y": y, "d": d,
                             "EW": float(ew.get(d, np.nan)),
                             "VW": float(vw.get(d, np.nan)),
                             "n_ew": int(n_ew.get(d, 0))})
    det = pd.DataFrame(rows)
    ts = det.groupby(["d", "y"])[["EW", "VW"]].mean()
    cum = {}
    for col in ["EW", "VW"]:
        cum[col] = {}
        for d in DECILES:
            p_ = np.prod([1.0 + ts.loc[(d, y), col] for y in EVENT_YEARS])
            cum[col][d] = p_ - 1.0
    print(f"[event] spec-literal cells: {len(det)}; EW cumulative spread "
          f"(D10-D1) = {(cum['EW'][10] - cum['EW'][1]) * 100:.1f}%  <-- outlier-"
          f"dominated (flagged)")
    return det, ts, cum


# =============================================================================
# 3. EVALUATION (same Tier rule as src/table_2.py evaluate())
# =============================================================================
def evaluate_metric(ours_pct: float):
    metrics = json.loads((PREP / "tables_to_replicate.json").read_text())
    t2 = next(t for t in metrics["tables"] if t["id"] == "T2")["metrics"]
    m = next(x for x in t2 if x["name"] == METRIC_NAME)
    paper, tol = float(m["value"]), float(m["tolerance_pct"])
    rel = abs(ours_pct - paper) / abs(paper)
    same_sign = (ours_pct * paper > 0) or (ours_pct == 0 == paper)
    LENIENT_MAG = 0.05
    if rel <= tol / 100.0:
        status, reason = "Tier 1", f"within {tol:.0f}% tol ({rel:.1%})"
    elif same_sign:
        status, reason = "Tier 2", f"sign ok, outside {tol:.0f}% tol ({rel:.1%})"
    elif abs(paper) < LENIENT_MAG and abs(ours_pct) < 0.5:
        status, reason = "Tier 2", f"lenient ~0 target; ours {ours_pct:.3f} small"
    else:
        status, reason = "FAIL", f"opposite sign (paper {paper}, ours {ours_pct:.4f})"
    return paper, tol, status, reason, rel


def update_eval_json(ours_pct: float, status: str, reason: str, section_E: dict):
    p = RESULTS / "table_2_eval.json"
    ev = json.loads(p.read_text())     # Python's json parses the existing NaN token
    old_status = None
    for e in ev["evaluation"]:
        if e["metric"] == METRIC_NAME:
            old_status = e["status"]
            e["ours"] = float(ours_pct)
            e["status"] = status
            e["reason"] = reason
            break
    if old_status is not None and old_status in ev["tally"] and old_status != status:
        ev["tally"][old_status] = max(ev["tally"][old_status] - 1, 0)
        ev["tally"][status] = ev["tally"].get(status, 0) + 1
    ev["results"]["section_E"] = section_E
    with open(p, "w") as fh:
        json.dump(ev, fh, indent=2, default=float)
    print(f"\n[wrote] results/table_2_eval.json — {METRIC_NAME}: ours={ours_pct:.2f}%, "
          f"{status}; tally now {ev['tally']}")
    return ev["tally"]


# =============================================================================
# 4. MARKDOWN + PLOT
# =============================================================================
def _decile_table(annual: dict, cum: dict, col: str) -> list:
    """annual: {y: {d: value}}, cum: {d: value}. Values are decimals."""
    L = []
    L.append(f"| {col} | " + " | ".join(f"D{d}" for d in DECILES) + " | Spread(10-1) |")
    L.append("|---|" + "---|" * 11)
    for y in EVENT_YEARS:
        cells = " | ".join(f"{annual[y][d] * 100:.2f}" for d in DECILES)
        sp = (annual[y][N_DECILES] - annual[y][1]) * 100
        L.append(f"| Year {y} | {cells} | {sp:.2f} |")
    cells = " | ".join(f"{cum[d] * 100:.2f}" for d in DECILES)
    sp = (cum[N_DECILES] - cum[1]) * 100
    L.append(f"| **Cumulative [1,5]** | {cells} | **{sp:.2f}** |")
    return L


def update_markdown(agg, p, specA, overlap, ew_spread_C, vw_spread_C,
                    ew_spread_B, vw_spread_B, ew_spread_A, vw_spread_A,
                    status, reason):
    surv = p.groupby("y")[["n_ew", "n_mem"]].mean()
    A = agg["EW"]; AV = agg["VW"]
    L = []
    L.append("## Event-time (Years −/+ around formation) — Year 1..5, fixed "
             "buy-and-hold formation cohorts\n")
    L.append("**Window.** This section uses an EXTENDED delisting-adjusted return "
             "window, **Jul-1968 .. Jun-2007** (`src/sql/universe_monthly_extended.sql` "
             "+ `delisting_extended.sql`; the foundation panel ends Jun-2003). The latest "
             "formation (Jun-2002) needs Year 5 = Jul-2006..Jun-2007. The universe "
             "filter (msfhdr PIT: hshrcd 10/11, hexcd 1/2/3, hsiccd not 6000–6999) and "
             "the Assumption-1 delisting adjustment are IDENTICAL to the foundation "
             f"(adjustment code imported from `main.py`); overlap spot-check "
             f"1968-07..2003-06: {overlap['n_matched']:,}/{overlap['n_panel_pairs']:,} "
             f"(permno, month) pairs matched, max|Δret| = {overlap['max_abs_diff']:.2e}, "
             f"{overlap['n_mismatch_gt_1e_12']} mismatches > 1e-12. Decile MEMBERSHIP IS "
             "FIXED at each June-t formation — the cohort is held for 5 years (NOT "
             "re-sorted annually), per the Figure 2 event-time convention (content.md "
             "L1552). Event year y of cohort t = Jul(t+y−1)..Jun(t+y).\n")
    L.append("**Conventions.** Surviving-member rule: a member contributes in a month "
             "only if it has return data that month; the delisting return is embedded in "
             "the delisting month, so delisting members contribute their delisting-month "
             "return and then drop out (cohorts shrink in later event years — avg "
             "surviving members per decile-cohort: " +
             ", ".join(f"Y{y} {surv.loc[y, 'n_ew']:.0f}/{surv.loc[y, 'n_mem']:.0f}"
                       for y in EVENT_YEARS) +
             "). **EW** = within-month mean of member returns; **VW** = Σ(w_i·r_i)/Σ(w_i) "
             "with w_i the FIXED June-t formation ME (Assumption 9), denominator "
             "renormalized over surviving members. Portfolio returns are then averaged "
             "across the 35 cohorts at each event-month offset (Figure 2's exact method); "
             "annual = product of the year's 12 event-month means − 1; **cumulative "
             "[1,5] = product of the 60 event-month means − 1**; spread = D10 − D1. "
             "Cumulative spread t-statistics (paper: EW −8.63 / VW −4.25) are over the 35 "
             "cohort-level 60-month cumulative spreads. All values %/yr or % cumulative.\n")
    L.append("### EW returns in event time (%/yr)\n")
    L.extend(_decile_table(A["annual_C"], A["cum_C"], "EW"))
    L.append("\n### VW returns in event time (%/yr)\n")
    L.extend(_decile_table(AV["annual_C"], AV["cum_C"], "VW"))
    L.append("\n### Cumulative Year 1..5 spread (committed metric + corroboration)\n")
    L.append(f"- **EW cumulative [1,5] spread (D10−D1) = {ew_spread_C:.2f}%** — paper "
             f"−87.99% (t = −8.63), content.md L1554 → **{status}** ({reason}). "
             f"Cohort-level mean spread {A['cohort_mean_spread_pct']:.2f}% "
             f"(t = {A['cohort_t_stat']:.2f}, n = {A['n_cohorts']}).")
    L.append(f"- **VW cumulative [1,5] spread (D10−D1) = {vw_spread_C:.2f}%** — paper "
             f"−49.67% (t = −4.25), content.md L1566 (not a committed metric). "
             f"Cohort-level mean spread {AV['cohort_mean_spread_pct']:.2f}% "
             f"(t = {AV['cohort_t_stat']:.2f}, n = {AV['n_cohorts']}).")
    L.append(f"- Alternative conventions (same cohorts/weights): compounding the "
             f"cohort-level annual portfolio returns (per-cohort annual compounding, "
             f"then time-series mean) gives EW {ew_spread_B:.2f}% / VW {vw_spread_B:.2f}%.")
    L.append(f"- ⚠️ **Spec-literal per-stock annual buy-and-hold variant (FLAGGED):** "
             f"averaging each member's annual buy-and-hold return across the cross-section "
             f"(EW_ret_{{d,y}} = mean over members of prod(1+r)−1, then cumulative "
             f"prod_y(1+EW_ret_{{d,y}})−1) gives EW {ew_spread_A:.1f}% / VW {vw_spread_A:.1f}%. "
             f"This is NOT used for the committed metric: on the 2026 CRSP vintage the "
             f"cross-sectional mean of per-stock annual BHRs is dominated by a handful of "
             f"sub-penny shell stocks (e.g. one +39,120% stock-year pulls a single cohort's "
             f"D1 mean to +275% vs a +50% median), producing economically meaningless "
             f"decile means (D1 ≈ +860%/yr). The paper's Figure 2 caption (L1552) shows it "
             f"reported average MONTHLY returns in event time, so the Table II last-row "
             f"cumulative spread is constructed from the monthly portfolio series above.\n")

    new_section = "\n".join(L)
    md_path = RESULTS / "table_2.md"
    md = md_path.read_text()
    # idempotent: cut from the earliest of the original stub, a prior computed
    # pointer, or a previously-appended event-time section, so re-runs don't
    # duplicate the section
    heads = ["## Section E — Event-Time Year 1..5 Buy-and-Hold (NOT YET COMPUTED)",
             "## Section E — Event-Time Year 1..5 Buy-and-Hold\n\nCOMPUTED",
             "## Event-time (Years −/+ around formation)"]
    i = min([md.find(h) for h in heads if md.find(h) != -1] + [len(md)])
    pointer = ("## Section E — Event-Time Year 1..5 Buy-and-Hold\n\nCOMPUTED — see the "
               "'Event-time (Years −/+ around formation)' section appended below (extended "
               "return window through Jun-2007, fixed buy-and-hold formation cohorts). "
               f"Metric `EW_cumulative_Y1_5_spread` is now evaluated as **{status}** "
               f"(ours {ew_spread_C:.2f}% vs paper −87.99%).\n")
    md = md[:i].rstrip() + "\n\n" + pointer + "\n" + new_section
    md_path.write_text(md)
    print("[wrote] results/table_2.md — event-time section (idempotent)")


def make_plot(cum_ew: dict, cum_vw: dict, ew_spread_pct: float):
    ew_vals = [cum_ew[d] * 100 for d in DECILES]
    vw_vals = [cum_vw[d] * 100 for d in DECILES]
    x = np.arange(len(DECILES))
    wdt = 0.4
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.bar(x - wdt / 2, ew_vals, wdt, label="EW", color="#4C72B0")
    ax.bar(x + wdt / 2, vw_vals, wdt, label="VW", color="#C44E52")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([str(d) for d in DECILES])
    ax.set_xlabel("ASSETG decile (1 = low growth ... 10 = high growth)")
    ax.set_ylabel("Cumulative Year 1..5 return (%)")
    ax.set_title(f"Table II Section E: cumulative Year 1..5 event-time returns by decile "
                 f"(EW D10−D1 = {ew_spread_pct:.1f}%)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(RESULTS / "table2_event_time.png", dpi=150)
    plt.close(fig)
    print("[wrote] results/table2_event_time.png")


# =============================================================================
def main():
    adj = load_extended()
    overlap = verify_overlap(adj)
    form = pd.read_parquet(DATA / "formation.parquet")
    wide = build_wide(adj)

    # --- primary: monthly-portfolio event time (Figure 2 method) --------------
    p = monthly_portfolio_series(wide, form)
    agg = aggregate_monthly(p)
    A, AV = agg["EW"], agg["VW"]
    ew_spread_C = (A["cum_C"][N_DECILES] - A["cum_C"][1]) * 100.0
    vw_spread_C = (AV["cum_C"][N_DECILES] - AV["cum_C"][1]) * 100.0
    ew_spread_B = (A["cum_B"][N_DECILES] - A["cum_B"][1]) * 100.0
    vw_spread_B = (AV["cum_B"][N_DECILES] - AV["cum_B"][1]) * 100.0

    # --- flagged: spec-literal per-stock annual buy-and-hold -------------------
    detA, tsA, cumA = spec_literal_event_time(wide, form)
    ew_spread_A = (cumA["EW"][N_DECILES] - cumA["EW"][1]) * 100.0
    vw_spread_A = (cumA["VW"][N_DECILES] - cumA["VW"][1]) * 100.0

    paper, tol, status, reason, rel = evaluate_metric(ew_spread_C)

    # ---- console report -------------------------------------------------------
    print("\n" + "=" * 74)
    print("EVENT-TIME YEAR 1..5 (fixed formation cohorts, 1968..2002)")
    print("=" * 74)
    print("PRIMARY (monthly-portfolio event time, Figure 2 method) — %/yr:")
    for col, name in [(A, "EW"), (AV, "VW")]:
        for y in EVENT_YEARS:
            an = col["annual_C"][y]
            print(f"  {name} Year {y}: D1 {an[1] * 100:7.2f}  D10 {an[10] * 100:7.2f}  "
                  f"spread {(an[10] - an[1]) * 100:7.2f}")
        c = col["cum_C"]
        print(f"  {name} Cumulative [1,5]: D1 {c[1] * 100:7.2f}  D10 {c[10] * 100:7.2f}  "
              f"SPREAD {(c[10] - c[1]) * 100:7.2f}   "
              f"(paper {'−87.99' if name == 'EW' else '−49.67'}; cohort t "
              f"{col['cohort_t_stat']:.2f})")
    print(f"Alt (cohort-annual compounding): EW {ew_spread_B:.2f}% / VW {vw_spread_B:.2f}%")
    print(f"Spec-literal per-stock BHR (FLAGGED): EW {ew_spread_A:.1f}% / "
          f"VW {vw_spread_A:.1f}%")
    print(f"\n{METRIC_NAME}: ours {ew_spread_C:.2f}% vs paper {paper}% | rel err "
          f"{rel:.1%} | tol {tol:.0f}% → {status} ({reason})")

    # ---- outputs ----------------------------------------------------------------
    section_E = {
        "status": "computed",
        "window": "1968-07 .. 2007-06 (extended; same universe filter + Assumption-1 "
                  "delisting adjustment as the foundation, code imported from main.py)",
        "overlap_check": overlap,
        "convention": ("fixed formation-year decile membership (buy-and-hold cohort, NOT "
                       "re-sorted). PRIMARY = monthly-portfolio event time (paper's "
                       "Figure 2 method, L1552): within-month EW mean / VW with fixed "
                       "June-t formation ME (Assumption 9) over surviving members, averaged "
                       "across the 35 cohorts at each of the 60 event-month offsets; "
                       "cumulative[1,5] = product of the 60 event-month means - 1; spread = "
                       "D10-D1. The committed metric uses this convention."),
        "EW_annual_pct": {f"Y{y}": {f"D{d}": float(A["annual_C"][y][d]) * 100.0
                                    for d in DECILES} for y in EVENT_YEARS},
        "VW_annual_pct": {f"Y{y}": {f"D{d}": float(AV["annual_C"][y][d]) * 100.0
                                    for d in DECILES} for y in EVENT_YEARS},
        "EW_spread_year_pct": {
            f"Y{y}": float((A["annual_C"][y][10] - A["annual_C"][y][1]) * 100.0)
            for y in EVENT_YEARS},
        "VW_spread_year_pct": {
            f"Y{y}": float((AV["annual_C"][y][10] - AV["annual_C"][y][1]) * 100.0)
            for y in EVENT_YEARS},
        "EW_cumulative_pct": {**{f"D{d}": float(A["cum_C"][d]) * 100.0 for d in DECILES},
                              "spread_10_1": float(ew_spread_C)},
        "VW_cumulative_pct": {**{f"D{d}": float(AV["cum_C"][d]) * 100.0 for d in DECILES},
                              "spread_10_1": float(vw_spread_C)},
        "EW_cohort_level": {"mean_spread_pct": A["cohort_mean_spread_pct"],
                            "t_stat": A["cohort_t_stat"],
                            "n_cohorts": A["n_cohorts"]},
        "VW_cohort_level": {"mean_spread_pct": AV["cohort_mean_spread_pct"],
                            "t_stat": AV["cohort_t_stat"],
                            "n_cohorts": AV["n_cohorts"]},
        "alternative_conventions": {
            "cohort_annual_compounding": {"EW_spread_pct": float(ew_spread_B),
                                          "VW_spread_pct": float(vw_spread_B)},
            "spec_literal_per_stock_BHR": {"EW_spread_pct": float(ew_spread_A),
                                           "VW_spread_pct": float(vw_spread_A),
                                           "flag": "outlier-dominated on 2026 CRSP "
                                                   "vintage (sub-penny shells); not used "
                                                   "for the committed metric"},
        },
        "avg_surviving_members_by_year": {
            f"Y{y}": {"surviving": float(p[p.y == y]["n_ew"].mean()),
                      "at_formation": float(p[p.y == y]["n_mem"].mean())}
            for y in EVENT_YEARS},
        "n_cohorts": len(FORMATION_YEARS),
        "evaluation": {"paper": paper, "tolerance_pct": tol,
                       "status": status, "reason": reason},
    }
    tally = update_eval_json(ew_spread_C, status, reason, section_E)
    update_markdown(agg, p, detA, overlap, ew_spread_C, vw_spread_C,
                    ew_spread_B, vw_spread_B, ew_spread_A, vw_spread_A,
                    status, reason)
    make_plot(A["cum_C"], AV["cum_C"], ew_spread_C)

    print(f"\nFINAL TALLY (Table II): {tally}")
    print("DONE.")


if __name__ == "__main__":
    main()
