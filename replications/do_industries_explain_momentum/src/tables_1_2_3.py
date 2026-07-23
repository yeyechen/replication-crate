"""Stage 3 — Moskowitz & Grinblatt (1999) "Do Industries Explain Momentum?"

Momentum-strategy engines + Tables I, II, III with per-cell comparison to the
paper. Reads the frozen artifacts data/panel.parquet (48 cols) and
data/bin_rets.parquet; writes results/table_{1,2,3}.md, three plots,
and results/cells_tables_1_2_3.json.

Engines (all conventions follow preparations/assumptions.md):
  * Individual (6,6) W-Lo  — A8 fixed formation weights w_j=me_j(f)/Σme(f),
    membership fixed over f..f+5, renormalize on missing holding-month
    returns; overlapping cohort average (A9/L324) at each month t over the 6
    cohorts f∈{t-5..t}.
  * Industry IM(L,H)       — rank 20 industries by past-L VW return, top3/bot3
    = Wi/Lo, ranks 4-6 = Mid; hold selection H months (Panel A f..f+H-1,
    Panel B f+1..f+H); industry member weights are the pre-computed monthly
    VW series (monthly rebalanced), EW across the 3 industries; monthly
    strategy return = average over the H active formable cohorts.
  * t = mean/(std/sqrt(T)), ddof=1 (A9). Raw series 1963-07..1995-07 (T=385);
    size/BE/DGTW-adjusted series 1973-01..1995-07 (T=271).
  * Random-industry replacement (A13): each month rank universe ascending by
    mom6, r_repl_j = (r_{j+1}+r_{j-1})/2, endpoints -> single neighbor.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
# replications/ root (parents[2]) pinned explicitly so this module is
# cwd-independent (paper_layout otherwise resolves REPLICATIONS_PATH vs cwd).
_REPLICATIONS_ROOT = Path(__file__).resolve().parents[2]

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from utils.paths import paper_layout  # noqa: E402
from utils import plot_cumulative_returns  # noqa: E402

SLUG = "do_industries_explain_momentum"
LAYOUT = paper_layout(SLUG, replications_root=_REPLICATIONS_ROOT)

RAW_START = pd.Period("1963-07", "M")
RAW_END = pd.Period("1995-07", "M")
ADJ_START = pd.Period("1973-01", "M")
ADJ_END = pd.Period("1995-07", "M")

IND_NAMES = {
    1: "Mining", 2: "Food", 3: "Apparel", 4: "Paper", 5: "Chemical",
    6: "Petroleum", 7: "Construction", 8: "Prim.Metals", 9: "Fab.Metals",
    10: "Machinery", 11: "Elec.Eq", 12: "Transp.Eq", 13: "Manuf",
    14: "Railroads", 15: "OtherTransp", 16: "Utilities", 17: "Dept.Stores",
    18: "Retail", 19: "Financial", 20: "Other",
}
# metric-name prefix used in preparations/tables_to_replicate.json (Table I)
T1_PREFIX = {
    1: "mining", 2: "food", 3: "apparel", 4: "paper", 5: "chemical",
    6: "petroleum", 7: "construction", 8: "prim_metals", 9: "fab_metals",
    10: "machinery", 11: "electrical_eq", 12: "transport_eq",
    13: "manufacturing", 14: "railroads", 15: "other_transport",
    16: "utilities", 17: "dept_stores", 18: "retail", 19: "financial",
    20: "other",
}


# ---------------------------------------------------------------------------
# statistics helpers
# ---------------------------------------------------------------------------

def mean_t(series) -> tuple[float, float, int]:
    """(mean, t-stat, T) of a monthly series; t = mean/(std/sqrt(T)), ddof=1."""
    s = pd.Series(series).dropna().to_numpy(dtype="float64")
    T = len(s)
    if T < 2:
        return (np.nan, np.nan, T)
    m = float(np.mean(s))
    sd = float(np.std(s, ddof=1))
    t = m / (sd / np.sqrt(T)) if sd > 0 else np.nan
    return (m, t, T)


def restrict(series: pd.Series, start: pd.Period, end: pd.Period) -> pd.Series:
    return series[(series.index >= start) & (series.index <= end)]


# ---------------------------------------------------------------------------
# data loading
# ---------------------------------------------------------------------------

def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = panel["date"].dt.to_period("M")
    ind = pd.read_parquet(LAYOUT.data_path("bin_rets.parquet"))
    ind["month"] = ind["date"].dt.to_period("M")
    return panel, ind


# ---------------------------------------------------------------------------
# random-industry replacement returns (A13) + industry auxiliary VW series
# ---------------------------------------------------------------------------

def add_replacement_returns(panel: pd.DataFrame) -> pd.DataFrame:
    """r_repl_raw / r_repl_sb per (permno, month): rank universe ascending by
    mom6 (mom6 & ret non-null); r_repl_j = (r_{j+1}+r_{j-1})/2, endpoints use
    the single neighbor; NaN if a neighbor's return is missing."""
    panel = panel.copy()
    panel["r_repl_raw"] = np.nan
    panel["r_repl_sb"] = np.nan
    mask = panel["mom6"].notna() & panel["ret"].notna()
    sub = panel.loc[mask].sort_values(["month", "mom6"])
    g = sub.groupby("month", sort=False)
    cnt = g.cumcount()
    n = g["mom6"].transform("size")
    ret_p = g["ret"].shift(1)
    ret_n = g["ret"].shift(-1)
    sb_p = g["r_sb"].shift(1)
    sb_n = g["r_sb"].shift(-1)
    rr = (ret_p + ret_n) / 2.0
    rr = rr.where(cnt != 0, ret_n)          # first -> next
    rr = rr.where(cnt != n - 1, ret_p)      # last  -> prev
    rs = (sb_p + sb_n) / 2.0
    rs = rs.where(cnt != 0, sb_n)
    rs = rs.where(cnt != n - 1, sb_p)
    panel.loc[rr.index, "r_repl_raw"] = rr.to_numpy()
    panel.loc[rs.index, "r_repl_sb"] = rs.to_numpy()
    return panel


def vw_by_month_ind(panel: pd.DataFrame, retcol: str,
                    wcol: str = "me_lag1") -> pd.DataFrame:
    """Monthly-rebalanced VW industry return: index=month, cols=ind(1..20)."""
    d = panel[panel[retcol].notna() & panel[wcol].notna() & (panel[wcol] > 0)]
    wr = d[wcol] * d[retcol]
    num = wr.groupby([d["month"], d["ind"]]).sum()
    den = d[wcol].groupby([d["month"], d["ind"]]).sum()
    vw = (num / den).unstack("ind")
    vw = vw.reindex(columns=np.arange(1, 21))
    return vw


# ---------------------------------------------------------------------------
# individual momentum cohorts (A8): global 30/30 on mom6, weights = me(f)
# ---------------------------------------------------------------------------

def build_global_cohorts(panel: pd.DataFrame) -> dict:
    """formation month f -> (win_permnos, win_weights, los_permnos, los_weights).
    Universe at f: mom6 non-null & me>0. Winners mom6>=p70, losers mom6<=p30.
    Weights me_j(f)/Σme(f), fixed over holding months."""
    cohorts = {}
    for f, g in panel.groupby("month", sort=True):
        cs = g[g["mom6"].notna() & g["me"].notna() & (g["me"] > 0)]
        if len(cs) < 20:
            continue
        mom = cs["mom6"].to_numpy()
        p30 = np.quantile(mom, 0.30)
        p70 = np.quantile(mom, 0.70)
        win = cs[mom >= p70]
        los = cs[mom <= p30]
        if len(win) == 0 or len(los) == 0:
            continue
        wm = win["me"].to_numpy(dtype="float64")
        lm = los["me"].to_numpy(dtype="float64")
        cohorts[f] = (
            win["permno"].to_numpy(), wm / wm.sum(),
            los["permno"].to_numpy(), lm / lm.sum(),
        )
    return cohorts


def individual_spread_series(ret_wide: pd.DataFrame, cohorts: dict,
                             hold: int = 6) -> pd.Series:
    """Monthly overlapping (6,6) W-Lo spread series from a month×permno return
    matrix using the shared cohorts/weights. renormalizes on missing returns."""
    months_idx = ret_wide.index
    month_pos = {m: i for i, m in enumerate(months_idx)}
    col_pos = {c: j for j, c in enumerate(ret_wide.columns.to_numpy())}
    arr = ret_wide.to_numpy(dtype="float64")

    cohort_fs = sorted(cohorts.keys())
    f_pos = {f: i for i, f in enumerate(cohort_fs)}
    spread_mat = np.full((len(cohort_fs), len(months_idx)), np.nan)

    for f, (wp, ww, lp, lw) in cohorts.items():
        fi = f_pos[f]
        wcols = np.array([col_pos[p] for p in wp], dtype=np.int64)
        lcols = np.array([col_pos[p] for p in lp], dtype=np.int64)
        for k in range(hold):
            ri = month_pos.get(f + k)
            if ri is None:
                continue
            Rw = arr[ri, wcols]
            mw = ~np.isnan(Rw)
            denw = ww[mw].sum()
            Wret = float(np.nansum(Rw * ww) / denw) if denw > 0 else np.nan
            Rl = arr[ri, lcols]
            ml = ~np.isnan(Rl)
            denl = lw[ml].sum()
            Lret = float(np.nansum(Rl * lw) / denl) if denl > 0 else np.nan
            spread_mat[fi, ri] = Wret - Lret

    strat = np.full(len(months_idx), np.nan)
    for ti in range(len(months_idx)):
        t = months_idx[ti]
        vals = []
        for k in range(hold):
            fi = f_pos.get(t - k)
            if fi is None:
                continue
            v = spread_mat[fi, ti]
            if not np.isnan(v):
                vals.append(v)
        if vals:
            strat[ti] = float(np.mean(vals))
    return pd.Series(strat, index=months_idx)


# ---------------------------------------------------------------------------
# industry momentum engine (Tables II-B, III)
# ---------------------------------------------------------------------------

def industry_selections(signal_mat: pd.DataFrame) -> dict:
    """formation month f -> (winners[3], mids[3], losers[3]) industry labels,
    ranked descending by signal; formable iff >=6 industries have signal."""
    sels = {}
    inds = np.arange(1, 21)
    for f in signal_mat.index:
        row = signal_mat.loc[f].to_numpy()
        valid = ~np.isnan(row)
        if valid.sum() < 6:
            continue
        order = sorted(inds[valid], key=lambda i: row[i - 1], reverse=True)
        sels[f] = (order[:3], order[3:6], order[-3:])
    return sels


def industry_cohort_returns(sels: dict, ret_mat: pd.DataFrame,
                            months_idx: pd.DatetimeIndex | pd.PeriodIndex,
                            max_hold: int = 36):
    """For each return matrix build Wi/Lo/Mid cohort×month return matrices.
    cohort f filled for tau in [f, f+max_hold]."""
    month_pos = {m: i for i, m in enumerate(months_idx)}
    f_list = sorted(sels.keys())
    f_pos = {f: i for i, f in enumerate(f_list)}
    nM = len(months_idx)
    Wi = np.full((len(f_list), nM), np.nan)
    Lo = np.full((len(f_list), nM), np.nan)
    Mid = np.full((len(f_list), nM), np.nan)
    R = ret_mat.reindex(months_idx).reindex(columns=np.arange(1, 21)).to_numpy()

    def _mn(x):
        x = x[~np.isnan(x)]
        return float(x.mean()) if len(x) else np.nan

    for f, (w, m, l) in sels.items():
        fi = f_pos[f]
        wc = [i - 1 for i in w]
        mc = [i - 1 for i in m]
        lc = [i - 1 for i in l]
        for k in range(max_hold + 1):
            ri = month_pos.get(f + k)
            if ri is None:
                continue
            Wi[fi, ri] = _mn(R[ri, wc])
            Mid[fi, ri] = _mn(R[ri, mc])
            Lo[fi, ri] = _mn(R[ri, lc])
    return Wi, Mid, Lo, f_list, f_pos


def industry_strat_series(cohort_mat: np.ndarray, f_list, f_pos,
                          months_idx, H: int, panelAB: str) -> pd.Series:
    """monthly strategy return = average over the H active formable cohorts."""
    nM = len(months_idx)
    out = np.full(nM, np.nan)
    for ti in range(nM):
        t = months_idx[ti]
        if panelAB == "A":
            fs = [t - k for k in range(H)]            # f..f+H-1 -> f in [t-H+1, t]
        else:
            fs = [t - k for k in range(1, H + 1)]     # f+1..f+H -> f in [t-H, t-1]
        vals = []
        for f in fs:
            fi = f_pos.get(f)
            if fi is None:
                continue
            v = cohort_mat[fi, ti]
            if not np.isnan(v):
                vals.append(v)
        if vals:
            out[ti] = float(np.mean(vals))
    return pd.Series(out, index=months_idx)


# ---------------------------------------------------------------------------
# Table I
# ---------------------------------------------------------------------------

def hotelling_f(X: np.ndarray) -> tuple[float, float]:
    """Hotelling T^2 test that all means = 0. X: T×N. Returns (F, p)."""
    T, N = X.shape
    xbar = X.mean(axis=0)
    S = np.cov(X, rowvar=False, ddof=1)
    T2 = T * float(xbar @ np.linalg.solve(S, xbar))
    F = (T - N) / (N * (T - 1)) * T2
    p = float(stats.f.sf(F, N, T - N))
    return float(F), p


def hotelling_f_equal(X: np.ndarray) -> tuple[float, float]:
    """Hotelling test all means equal, via N-1 spreads vs last series."""
    S19 = X[:, :19] - X[:, 19:20]
    T, N = S19.shape  # N = 19
    xbar = S19.mean(axis=0)
    S = np.cov(S19, rowvar=False, ddof=1)
    T2 = T * float(xbar @ np.linalg.solve(S, xbar))
    F = (T - N) / (N * (T - 1)) * T2
    p = float(stats.f.sf(F, N, T - N))
    return float(F), p


def compute_table_1(panel: pd.DataFrame, ind: pd.DataFrame,
                    R_sb_ind: pd.DataFrame) -> dict:
    """Per-industry Table-I stats + F-tests. Returns ours dict + detail df."""
    samp = ind[(ind["month"] >= RAW_START) & (ind["month"] <= RAW_END)].copy()
    rf_by_month = panel.drop_duplicates("month").set_index("month")["rf"]
    samp = samp.merge(rf_by_month.rename("rf"), left_on="month",
                      right_index=True, how="left")
    samp["exc"] = samp["ind_ret_vw"] - samp["rf"]
    tot_me = samp.groupby("month")["total_me"].sum()
    samp["cap_share"] = samp["total_me"] / samp["month"].map(tot_me)

    rows = []
    for i in range(1, 21):
        gi = samp[samp["ind"] == i]
        avg_n = gi["n_stocks_univ"].mean()
        min_n = gi["n_stocks_univ"].min()
        pct = gi["cap_share"].mean() * 100.0
        excess = gi["exc"].mean()
        # abnormal: monthly R_sb_ind series over adj window
        abn_series = restrict(R_sb_ind[i], ADJ_START, ADJ_END)
        abn_m, abn_t, _ = mean_t(abn_series)
        rows.append(dict(ind=i, avg_n=avg_n, min_n=min_n, pct_mktcap=pct,
                         excess=excess, abnormal=abn_m, abnormal_t=abn_t))
    detail = pd.DataFrame(rows).set_index("ind")

    ours = {}
    for i in range(1, 21):
        pre = f"{T1_PREFIX[i]}_"
        r = detail.loc[i]
        ours[pre + "avg_stocks"] = float(r.avg_n)
        ours[pre + "min_stocks"] = float(r.min_n)
        ours[pre + "pct_mktcap"] = float(r.pct_mktcap)
        ours[pre + "excess_ret"] = float(r.excess)
        ours[pre + "abnormal_ret"] = float(r.abnormal)
        ours[pre + "abnormal_t"] = float(r.abnormal_t)
    # average row = mean of the 20 per-industry stats
    for stat, key in [("avg_n", "avg_stocks"), ("min_n", "min_stocks"),
                      ("pct_mktcap", "pct_mktcap"), ("excess", "excess_ret"),
                      ("abnormal", "abnormal_ret"), ("abnormal_t", "abnormal_t")]:
        ours[f"average_{key}"] = float(detail[stat].mean())

    # F-tests
    exc_mat = samp.pivot(index="month", columns="ind", values="exc")
    exc_mat = exc_mat.reindex(columns=np.arange(1, 21)).dropna()
    exc_mat = exc_mat[(exc_mat.index >= RAW_START) & (exc_mat.index <= RAW_END)]
    f_zero_e, p_zero_e = hotelling_f(exc_mat.to_numpy())
    f_same_e, p_same_e = hotelling_f_equal(exc_mat.to_numpy())

    abn_mat = R_sb_ind.reindex(columns=np.arange(1, 21))
    abn_mat = abn_mat[(abn_mat.index >= ADJ_START) & (abn_mat.index <= ADJ_END)].dropna()
    f_zero_a, p_zero_a = hotelling_f(abn_mat.to_numpy())
    f_same_a, p_same_a = hotelling_f_equal(abn_mat.to_numpy())

    ours["f_all_zero_excess"] = f_zero_e
    ours["p_all_zero_excess"] = p_zero_e
    ours["f_all_zero_abnormal"] = f_zero_a
    ours["p_all_zero_abnormal"] = p_zero_a
    ours["f_all_same_excess"] = f_same_e
    ours["p_all_same_excess"] = p_same_e
    ours["f_all_same_abnormal"] = f_same_a
    ours["p_all_same_abnormal"] = p_same_a

    return ours, detail, dict(f_zero_e=f_zero_e, p_zero_e=p_zero_e,
                              f_same_e=f_same_e, p_same_e=p_same_e,
                              f_zero_a=f_zero_a, p_zero_a=p_zero_a,
                              f_same_a=f_same_a, p_same_a=p_same_a,
                              T_exc=len(exc_mat), T_abn=len(abn_mat))


# ---------------------------------------------------------------------------
# Table II
# ---------------------------------------------------------------------------

def compute_table_2(panel, ind, aux_mats, cohorts) -> dict:
    """Returns ours dict + a bundle of series needed for plots/report."""
    R_sb_ind = aux_mats["R_sb_ind"]
    R_sb_rand_ind = aux_mats["R_sb_rand_ind"]
    R_dgtw_ind = aux_mats["R_dgtw_ind"]
    R_rand_ind = aux_mats["R_rand_ind"]
    ind_vw_mat = aux_mats["ind_vw_mat"]
    sig6 = aux_mats["ind_mom6"]

    ours = {}
    bundle = {}

    # ---- Panel A: individual (6,6), shared cohorts ----
    # per-row adjusted return columns
    pan = panel.merge(
        R_sb_ind.stack().rename("R_sb_ind").reset_index(),
        on=["month", "ind"], how="left")
    pan = pan.merge(
        R_sb_rand_ind.stack().rename("R_sb_rand_ind").reset_index(),
        on=["month", "ind"], how="left")
    pan["ret_minus_ind"] = pan["ret"] - pan["ind_ret_vw"]
    pan["sb_minus_ind"] = pan["r_sb"] - pan["R_sb_ind"]
    pan["sb_minus_randind"] = pan["r_sb"] - pan["R_sb_rand_ind"]

    pa_cols = [
        ("pA_raw", "ret", "raw"),
        ("pA_dgtw", "r_dgtw", "adj"),
        ("pA_sb", "r_sb", "adj"),
        ("pA_raw_minus_ind", "ret_minus_ind", "raw"),
        ("pA_sb_minus_ind", "sb_minus_ind", "adj"),
        ("pA_sb_minus_randind", "sb_minus_randind", "adj"),
    ]
    pa_series = {}
    for name, col, kind in pa_cols:
        wide = pan.pivot(index="month", columns="permno", values=col)
        s = individual_spread_series(wide, cohorts, hold=6)
        pa_series[name] = s
        if kind == "raw":
            s_use = restrict(s, RAW_START, RAW_END)
        else:
            s_use = restrict(s, ADJ_START, ADJ_END)
        m, t, T = mean_t(s_use)
        ours[f"{name}_mean"] = m
        ours[f"{name}_t"] = t
    bundle["pa_raw_series"] = restrict(pa_series["pA_raw"], RAW_START, RAW_END)
    del pan

    # ---- Panel B: industry (6,6) = IM(6,6) Panel-A convention ----
    sels6 = industry_selections(sig6)
    months_idx = ind_vw_mat.index
    # raw industry
    Wi, Mid, Lo, f_list, f_pos = industry_cohort_returns(
        sels6, ind_vw_mat, months_idx, max_hold=6)
    wi_s = industry_strat_series(Wi, f_list, f_pos, months_idx, 6, "A")
    lo_s = industry_strat_series(Lo, f_list, f_pos, months_idx, 6, "A")
    wilo_raw = restrict(wi_s - lo_s, RAW_START, RAW_END)
    m, t, _ = mean_t(wilo_raw)
    ours["pB_raw_industry_mean"] = m
    ours["pB_raw_industry_t"] = t
    bundle["pb_raw_series"] = wilo_raw
    # DGTW industry (same selections)
    Wi_d, Mid_d, Lo_d, _, _ = industry_cohort_returns(
        sels6, R_dgtw_ind, months_idx, max_hold=6)
    wilo_d = restrict(
        industry_strat_series(Wi_d, f_list, f_pos, months_idx, 6, "A")
        - industry_strat_series(Lo_d, f_list, f_pos, months_idx, 6, "A"),
        ADJ_START, ADJ_END)
    m, t, _ = mean_t(wilo_d)
    ours["pB_dgtw_industry_mean"] = m
    ours["pB_dgtw_industry_t"] = t
    # random industry (same selections)
    Wi_r, Mid_r, Lo_r, _, _ = industry_cohort_returns(
        sels6, R_rand_ind, months_idx, max_hold=6)
    wilo_r = restrict(
        industry_strat_series(Wi_r, f_list, f_pos, months_idx, 6, "A")
        - industry_strat_series(Lo_r, f_list, f_pos, months_idx, 6, "A"),
        RAW_START, RAW_END)
    m, t, _ = mean_t(wilo_r)
    ours["pB_raw_random_industry_mean"] = m
    ours["pB_raw_random_industry_t"] = t

    # ---- Panel C ----
    ret_wide = panel.pivot(index="month", columns="permno", values="ret")
    pc_neut = panelC_industry_neutral(panel, ret_wide)
    m, t, _ = mean_t(restrict(pc_neut, RAW_START, RAW_END))
    ours["pC_industry_neutral_mean"] = m
    ours["pC_industry_neutral_t"] = t

    pc_exc = panelC_excess_industry(panel, ret_wide)
    m, t, _ = mean_t(restrict(pc_exc, RAW_START, RAW_END))
    ours["pC_excess_industry_mean"] = m
    ours["pC_excess_industry_t"] = t

    pc_hl = panelC_high_low(panel, ret_wide, ind)
    m, t, _ = mean_t(restrict(pc_hl, RAW_START, RAW_END))
    ours["pC_high_ind_losers_low_ind_winners_mean"] = m
    ours["pC_high_ind_losers_low_ind_winners_t"] = t

    return ours, bundle


def _vw_arr(arr_row, cols, weights):
    R = arr_row[cols]
    m = ~np.isnan(R)
    den = weights[m].sum()
    return float(np.nansum(R * weights) / den) if den > 0 else np.nan


def _ew_arr(arr_row, cols):
    R = arr_row[cols]
    R = R[~np.isnan(R)]
    return float(R.mean()) if len(R) else np.nan


def panelC_industry_neutral(panel: pd.DataFrame, ret_wide: pd.DataFrame) -> pd.Series:
    """Industry-neutral (6,6): within each industry winners>=p70/losers<=p30
    (mom6), VW me(f) fixed f..f+5; EW across the 20 industry spreads (skip
    empty legs); overlapping cohort average."""
    months_idx = ret_wide.index
    month_pos = {m: i for i, m in enumerate(months_idx)}
    col_pos = {c: j for j, c in enumerate(ret_wide.columns.to_numpy())}
    arr = ret_wide.to_numpy(dtype="float64")

    cohort_fs = []
    spread_by_f = {}
    for f, g in panel.groupby("month", sort=True):
        cs = g[g["mom6"].notna() & g["me"].notna() & (g["me"] > 0)]
        if len(cs) < 20:
            continue
        ind_blocks = []
        ok = True
        for i in range(1, 21):
            ci = cs[cs["ind"] == i]
            if len(ci) < 4:
                ind_blocks.append(None)
                continue
            mom = ci["mom6"].to_numpy()
            p30 = np.quantile(mom, 0.30)
            p70 = np.quantile(mom, 0.70)
            w = ci[mom >= p70]
            l = ci[mom <= p30]
            if len(w) == 0 or len(l) == 0:
                ind_blocks.append(None)
                continue
            wm = w["me"].to_numpy(dtype="float64")
            lm = l["me"].to_numpy(dtype="float64")
            ind_blocks.append((
                np.array([col_pos[p] for p in w["permno"].to_numpy()]),
                wm / wm.sum(),
                np.array([col_pos[p] for p in l["permno"].to_numpy()]),
                lm / lm.sum(),
            ))
        cohort_fs.append(f)
        spread_by_f[f] = ind_blocks

    f_pos = {f: i for i, f in enumerate(cohort_fs)}
    spread_mat = np.full((len(cohort_fs), len(months_idx)), np.nan)
    for f, blocks in spread_by_f.items():
        fi = f_pos[f]
        for k in range(6):
            ri = month_pos.get(f + k)
            if ri is None:
                continue
            spreads = []
            for b in blocks:
                if b is None:
                    continue
                wc, ww, lc, lw = b
                Wr = _vw_arr(arr[ri], wc, ww)
                Lr = _vw_arr(arr[ri], lc, lw)
                if not (np.isnan(Wr) or np.isnan(Lr)):
                    spreads.append(Wr - Lr)
            if spreads:
                spread_mat[fi, ri] = float(np.mean(spreads))

    return _cohort_average(spread_mat, f_pos, months_idx, hold=6)


def panelC_excess_industry(panel: pd.DataFrame, ret_wide: pd.DataFrame) -> pd.Series:
    """Excess-industry (6,6): signal = mom6 - ind_mom6, global top/bottom 30%
    EQUAL-weight, fixed membership f..f+5, overlapping cohort average."""
    months_idx = ret_wide.index
    month_pos = {m: i for i, m in enumerate(months_idx)}
    col_pos = {c: j for j, c in enumerate(ret_wide.columns.to_numpy())}
    arr = ret_wide.to_numpy(dtype="float64")
    panel = panel.copy()
    panel["xs_sig"] = panel["mom6"] - panel["ind_mom6"]

    cohort_fs = []
    members = {}
    for f, g in panel.groupby("month", sort=True):
        cs = g[g["xs_sig"].notna() & g["me"].notna() & (g["me"] > 0)]
        if len(cs) < 20:
            continue
        sig = cs["xs_sig"].to_numpy()
        p30 = np.quantile(sig, 0.30)
        p70 = np.quantile(sig, 0.70)
        w = cs[sig >= p70]
        l = cs[sig <= p30]
        if len(w) == 0 or len(l) == 0:
            continue
        cohort_fs.append(f)
        members[f] = (
            np.array([col_pos[p] for p in w["permno"].to_numpy()]),
            np.array([col_pos[p] for p in l["permno"].to_numpy()]),
        )

    f_pos = {f: i for i, f in enumerate(cohort_fs)}
    spread_mat = np.full((len(cohort_fs), len(months_idx)), np.nan)
    for f, (wc, lc) in members.items():
        fi = f_pos[f]
        for k in range(6):
            ri = month_pos.get(f + k)
            if ri is None:
                continue
            Wr = _ew_arr(arr[ri], wc)
            Lr = _ew_arr(arr[ri], lc)
            if not (np.isnan(Wr) or np.isnan(Lr)):
                spread_mat[fi, ri] = Wr - Lr
    return _cohort_average(spread_mat, f_pos, months_idx, hold=6)


def panelC_high_low(panel: pd.DataFrame, ret_wide: pd.DataFrame,
                    ind: pd.DataFrame) -> pd.Series:
    """High-ind losers - low-ind winners (6,6): top3/bot3 industries by
    ind_mom6; within each, bottom-30% (long) / top-30% (short) by mom6 VW by
    me(f); EW across the 3 industry portfolios per leg; overlapping avg."""
    months_idx = ret_wide.index
    month_pos = {m: i for i, m in enumerate(months_idx)}
    col_pos = {c: j for j, c in enumerate(ret_wide.columns.to_numpy())}
    arr = ret_wide.to_numpy(dtype="float64")

    # industry-level ind_mom6 by month
    ind_sig = ind.drop_duplicates(["month", "ind"]).set_index(
        ["month", "ind"])["ind_mom6"].unstack("ind").reindex(columns=np.arange(1, 21))

    cohort_fs = []
    members = {}
    for f, g in panel.groupby("month", sort=True):
        if f not in ind_sig.index:
            continue
        row = ind_sig.loc[f].to_numpy()
        valid = ~np.isnan(row)
        if valid.sum() < 6:
            continue
        order = sorted(np.arange(1, 21)[valid], key=lambda i: row[i - 1],
                       reverse=True)
        high_inds = order[:3]
        low_inds = order[-3:]
        cs = g[g["mom6"].notna() & g["me"].notna() & (g["me"] > 0)]

        def leg_blocks(inds, want):
            blocks = []
            for i in inds:
                ci = cs[cs["ind"] == i]
                if len(ci) < 4:
                    blocks.append(None)
                    continue
                mom = ci["mom6"].to_numpy()
                p30 = np.quantile(mom, 0.30)
                p70 = np.quantile(mom, 0.70)
                sel = ci[mom <= p30] if want == "lo" else ci[mom >= p70]
                if len(sel) == 0:
                    blocks.append(None)
                    continue
                sm = sel["me"].to_numpy(dtype="float64")
                blocks.append((
                    np.array([col_pos[p] for p in sel["permno"].to_numpy()]),
                    sm / sm.sum(),
                ))
            return blocks

        long_blocks = leg_blocks(high_inds, "lo")   # losers of high industries
        short_blocks = leg_blocks(low_inds, "hi")    # winners of low industries
        if all(b is None for b in long_blocks) or all(b is None for b in short_blocks):
            continue
        cohort_fs.append(f)
        members[f] = (long_blocks, short_blocks)

    f_pos = {f: i for i, f in enumerate(cohort_fs)}
    spread_mat = np.full((len(cohort_fs), len(months_idx)), np.nan)
    for f, (long_blocks, short_blocks) in members.items():
        fi = f_pos[f]
        for k in range(6):
            ri = month_pos.get(f + k)
            if ri is None:
                continue
            longs, shorts = [], []
            for b in long_blocks:
                if b is None:
                    continue
                v = _vw_arr(arr[ri], b[0], b[1])
                if not np.isnan(v):
                    longs.append(v)
            for b in short_blocks:
                if b is None:
                    continue
                v = _vw_arr(arr[ri], b[0], b[1])
                if not np.isnan(v):
                    shorts.append(v)
            if longs and shorts:
                spread_mat[fi, ri] = float(np.mean(longs) - np.mean(shorts))
    return _cohort_average(spread_mat, f_pos, months_idx, hold=6)


def _cohort_average(spread_mat, f_pos, months_idx, hold=6) -> pd.Series:
    nM = len(months_idx)
    out = np.full(nM, np.nan)
    for ti in range(nM):
        t = months_idx[ti]
        vals = []
        for k in range(hold):
            fi = f_pos.get(t - k)
            if fi is None:
                continue
            v = spread_mat[fi, ti]
            if not np.isnan(v):
                vals.append(v)
        if vals:
            out[ti] = float(np.mean(vals))
    return pd.Series(out, index=months_idx)


# ---------------------------------------------------------------------------
# Table III
# ---------------------------------------------------------------------------

def compute_table_3(aux_mats) -> dict:
    ind_vw_mat = aux_mats["ind_vw_mat"]
    R_dgtw_ind = aux_mats["R_dgtw_ind"]
    months_idx = ind_vw_mat.index
    sig_mats = {1: aux_mats["ind_mom1"], 6: aux_mats["ind_mom6"],
                12: aux_mats["ind_mom12"]}
    Hs = [1, 6, 12, 24, 36]
    ours = {}
    grid = {}   # (panelAB, L, H) -> dict(metric->(mean,t))
    for L in (1, 6, 12):
        sels = industry_selections(sig_mats[L])
        Wi, Mid, Lo, f_list, f_pos = industry_cohort_returns(
            sels, ind_vw_mat, months_idx, max_hold=36)
        Wi_d, Mid_d, Lo_d, _, _ = industry_cohort_returns(
            sels, R_dgtw_ind, months_idx, max_hold=36)
        for panelAB in ("A", "B"):
            for H in Hs:
                wi = industry_strat_series(Wi, f_list, f_pos, months_idx, H, panelAB)
                lo = industry_strat_series(Lo, f_list, f_pos, months_idx, H, panelAB)
                mid = industry_strat_series(Mid, f_list, f_pos, months_idx, H, panelAB)
                wid = industry_strat_series(Wi_d, f_list, f_pos, months_idx, H, panelAB)
                lod = industry_strat_series(Lo_d, f_list, f_pos, months_idx, H, panelAB)
                wilo = restrict(wi - lo, RAW_START, RAW_END)
                wimid = restrict(wi - mid, RAW_START, RAW_END)
                midlo = restrict(mid - lo, RAW_START, RAW_END)
                wir = restrict(wi, RAW_START, RAW_END)
                lor = restrict(lo, RAW_START, RAW_END)
                dgtw = restrict(wid - lod, ADJ_START, ADJ_END)
                d = {}
                d["wi"] = (mean_t(wir)[0], mean_t(wir)[1])
                d["lo"] = (mean_t(lor)[0], mean_t(lor)[1])
                d["wilo"] = (mean_t(wilo)[0], mean_t(wilo)[1])
                d["wimid"] = (mean_t(wimid)[0], mean_t(wimid)[1])
                d["midlo"] = (mean_t(midlo)[0], mean_t(midlo)[1])
                d["dgtw"] = (mean_t(dgtw)[0], mean_t(dgtw)[1])
                grid[(panelAB, L, H)] = d
                pre = f"p{panelAB}_L{L}_H{H}_"
                ours[pre + "wi"] = d["wi"][0]
                ours[pre + "lo"] = d["lo"][0]
                ours[pre + "wilo"] = d["wilo"][0]
                ours[pre + "wilo_t"] = d["wilo"][1]
                ours[pre + "wimid"] = d["wimid"][0]
                ours[pre + "wimid_t"] = d["wimid"][1]
                ours[pre + "midlo"] = d["midlo"][0]
                ours[pre + "midlo_t"] = d["midlo"][1]
                ours[pre + "dgtw"] = d["dgtw"][0]
                ours[pre + "dgtw_t"] = d["dgtw"][1]
    return ours, grid


# ---------------------------------------------------------------------------
# per-cell comparison JSON
# ---------------------------------------------------------------------------

def cell_status(ours, paper, tol_pct) -> str:
    if ours is None or (isinstance(ours, float) and np.isnan(ours)):
        return "SKIP"
    if abs(paper) < 0.0005:
        if abs(ours - paper) <= 0.001:
            return "Tier1"
        if (ours >= 0) == (paper >= 0):
            return "Tier2"
        if abs(ours) < 0.0005:
            return "Tier2"
        return "FAIL"
    rel = abs(ours - paper) / abs(paper)
    if rel <= tol_pct / 100.0:
        return "Tier1"
    if (ours >= 0) == (paper >= 0):
        return "Tier2"
    return "FAIL"


def build_cells(contract: dict, ours_by_table: dict) -> list[dict]:
    cells = []
    for t in contract["tables"]:
        tid = t["id"]
        if tid not in ("T1", "T2", "T3"):
            continue
        ours = ours_by_table[tid]
        for m in t["metrics"]:
            name = m["name"]
            paper = float(m["value"])
            tol = float(m["tolerance_pct"])
            o = ours.get(name, np.nan)
            st = cell_status(o, paper, tol)
            cells.append(dict(table=tid, metric=name, paper=paper,
                              ours=(None if (isinstance(o, float) and np.isnan(o))
                                    else float(o)),
                              tol_pct=tol, status=st))
    return cells


# ---------------------------------------------------------------------------
# markdown writers
# ---------------------------------------------------------------------------

def write_table_1_md(detail, ftests, paper_t1):
    p = {m["name"]: m["value"] for m in paper_t1}
    lines = ["# Table I — Industry characteristics, excess & abnormal returns",
             "", "Period: excess/raw 1963-07..1995-07 (T=%d); abnormal "
             "1973-01..1995-07 (T=%d)." % (ftests["T_exc"], ftests["T_abn"]), ""]
    hdr = ("| Ind | Industry | avg_n (Ours/Paper/Diff) | min_n | pct_mktcap | "
           "excess | abnormal | abn_t |")
    lines.append(hdr)
    lines.append("|" + "---|" * 8)
    stat_keys = [("avg_n", "avg_stocks"), ("min_n", "min_stocks"),
                 ("pct_mktcap", "pct_mktcap"), ("excess", "excess_ret"),
                 ("abnormal", "abnormal_ret"), ("abnormal_t", "abnormal_t")]
    for i in range(1, 21):
        r = detail.loc[i]
        pre = f"{T1_PREFIX[i]}_"
        cells = [str(i), IND_NAMES[i]]
        for col, key in stat_keys:
            o = float(r[col])
            pv = p.get(pre + key, np.nan)
            cells.append(f"{o:.4f} / {pv:.4f} / {o - pv:+.4f}")
        lines.append("| " + " | ".join(cells) + " |")
    # average row
    avg = {col: detail[col].mean() for col, _ in stat_keys}
    cells = ["", "Average"]
    for col, key in stat_keys:
        o = avg[col]
        pv = p.get("average_" + key, np.nan)
        cells.append(f"{o:.4f} / {pv:.4f} / {o - pv:+.4f}")
    lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## F-tests (Hotelling T²)")
    lines.append("| Test | Ours F (p) | Paper F (p) |")
    lines.append("|---|---|---|")
    rows = [
        ("all=0 excess", "f_zero_e", "p_zero_e",
         "f_all_zero_excess", "p_all_zero_excess"),
        ("all-equal excess", "f_same_e", "p_same_e",
         "f_all_same_excess", "p_all_same_excess"),
        ("all=0 abnormal", "f_zero_a", "p_zero_a",
         "f_all_zero_abnormal", "p_all_zero_abnormal"),
        ("all-equal abnormal", "f_same_a", "p_same_a",
         "f_all_same_abnormal", "p_all_same_abnormal"),
    ]
    for label, fk, pk, ppf, ppp in rows:
        lines.append(f"| {label} | {ftests[fk]:.3f} ({ftests[pk]:.3f}) | "
                     f"{p.get(ppf, float('nan')):.3f} ({p.get(ppp, float('nan')):.3f}) |")
    (LAYOUT.result_path("table_1.md")).write_text("\n".join(lines) + "\n")


def write_table_2_md(ours, paper_t2):
    p = {m["name"]: m["value"] for m in paper_t2}
    order = [
        ("Panel A: Raw", "pA_raw"), ("Panel A: DGTW", "pA_dgtw"),
        ("Panel A: SB", "pA_sb"), ("Panel A: Raw-Industry", "pA_raw_minus_ind"),
        ("Panel A: SB-Industry", "pA_sb_minus_ind"),
        ("Panel A: SB-Random Industry", "pA_sb_minus_randind"),
        ("Panel B: Raw Industry", "pB_raw_industry"),
        ("Panel B: DGTW Industry", "pB_dgtw_industry"),
        ("Panel B: Raw Random Industry", "pB_raw_random_industry"),
        ("Panel C: Industry-neutral", "pC_industry_neutral"),
        ("Panel C: Excess-industry", "pC_excess_industry"),
        ("Panel C: High-ind losers - low-ind winners",
         "pC_high_ind_losers_low_ind_winners"),
    ]
    lines = ["# Table II — Momentum profits, individual vs industry (6,6)", "",
             "| Strategy | Ours mean | Paper mean | Ours t | Paper t |",
             "|---|---|---|---|---|"]
    for label, key in order:
        om = ours.get(key + "_mean", float("nan"))
        ot = ours.get(key + "_t", float("nan"))
        pm = p.get(key + "_mean", float("nan"))
        pt = p.get(key + "_t", float("nan"))
        lines.append(f"| {label} | {om:.4f} | {pm:.4f} | {ot:.2f} | {pt:.2f} |")
    (LAYOUT.result_path("table_2.md")).write_text("\n".join(lines) + "\n")


def write_table_3_md(grid, paper_t3):
    p = {m["name"]: m["value"] for m in paper_t3}
    Hs = [1, 6, 12, 24, 36]
    lines = ["# Table III — Industry momentum IM(L,H) grid", "",
             "Each cell: Ours mean (t) / Paper mean. DGTW over "
             "1973-01..1995-07; others over 1963-07..1995-07.", ""]
    metrics = [("wi", "Wi", False), ("lo", "Lo", False),
               ("wilo", "Wi-Lo", True), ("wimid", "Wi-Mid", True),
               ("midlo", "Mid-Lo", True), ("dgtw", "DGTW[Wi-Lo]", True)]
    for panelAB in ("A", "B"):
        lines.append(f"## Panel {panelAB}")
        for L in (1, 6, 12):
            lines.append(f"### L = {L}")
            lines.append("| Metric | " + " | ".join(f"H={h}" for h in Hs) + " |")
            lines.append("|" + "---|" * (len(Hs) + 1))
            for mkey, mlabel, has_t in metrics:
                cells = [mlabel]
                for H in Hs:
                    d = grid[(panelAB, L, H)][mkey]
                    o_m, o_t = d
                    pname = f"p{panelAB}_L{L}_H{H}_{mkey}"
                    pm = p.get(pname, float("nan"))
                    if has_t:
                        cells.append(f"{o_m:.4f}({o_t:.2f})/{pm:.4f}")
                    else:
                        cells.append(f"{o_m:.4f}/{pm:.4f}")
                lines.append("| " + " | ".join(cells) + " |")
            lines.append("")
    (LAYOUT.result_path("table_3.md")).write_text("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# plots
# ---------------------------------------------------------------------------

def make_plots(bundle, grid):
    res = LAYOUT.result_path
    # 1. raw individual vs raw industry cumulative PnL
    raw_ind = bundle["pa_raw_series"]
    raw_industry = bundle["pb_raw_series"]
    df = pd.DataFrame({
        "individual_raw_VW": raw_ind.reindex(
            raw_ind.index.union(raw_industry.index)).reindex(raw_ind.index),
        "industry_raw": raw_industry,
    })
    # align to common months
    common = raw_ind.index.intersection(raw_industry.index)
    df = pd.DataFrame({
        "month": common.to_timestamp(),
        "individual_raw": raw_ind.reindex(common).to_numpy(),
        "industry_raw": raw_industry.reindex(common).to_numpy(),
    })
    plot_cumulative_returns(
        df, index_col_name="month",
        ret_col_lst=["individual_raw", "industry_raw"],
        title="Cumulative PnL: individual (6,6) raw W-Lo vs industry (6,6) raw W-Lo",
        save_to=res("pnl_raw_vs_industry.png"))

    # 2. grouped bar of Wi-Lo vs H for Panel A and B at L=6
    Hs = [1, 6, 12, 24, 36]
    a = [grid[("A", 6, H)]["wilo"][0] for H in Hs]
    b = [grid[("B", 6, H)]["wilo"][0] for H in Hs]
    x = np.arange(len(Hs))
    wbar = 0.38
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - wbar / 2, a, wbar, label="Panel A (no gap)", color="#1e88e5")
    ax.bar(x + wbar / 2, b, wbar, label="Panel B (month skipped)", color="#f31d36")
    ax.set_xticks(x)
    ax.set_xticklabels([f"H={h}" for h in Hs])
    ax.set_ylabel("Wi-Lo mean monthly return")
    ax.set_title("Industry momentum Wi-Lo (L=6) by holding period")
    ax.axhline(0, color="k", lw=0.7)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(res("im_grid_L6.png"), dpi=130)
    plt.close(fig)

    # 3. Table-I excess scatter ours vs paper
    contract = json.loads(LAYOUT.preparations_path(
        "tables_to_replicate.json").read_text())
    paper_t1 = {m["name"]: m["value"] for t in contract["tables"]
                if t["id"] == "T1" for m in t["metrics"]}
    ours_t1 = bundle["ours_t1"]
    xs, ys, labs = [], [], []
    for i in range(1, 21):
        pre = f"{T1_PREFIX[i]}_"
        o = ours_t1.get(pre + "excess_ret")
        pv = paper_t1.get(pre + "excess_ret")
        if o is None or pv is None:
            continue
        xs.append(o); ys.append(pv); labs.append(IND_NAMES[i])
    xs = np.array(xs); ys = np.array(ys)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(xs, ys, s=35)
    lo = min(xs.min(), ys.min()); hi = max(xs.max(), ys.max())
    ax.plot([lo, hi], [lo, hi], "k--", lw=0.8, label="45°")
    for x_, y_, l_ in zip(xs, ys, labs):
        ax.annotate(l_, (x_, y_), fontsize=6, alpha=0.7)
    ax.set_xlabel("Our avg monthly excess return")
    ax.set_ylabel("Paper avg monthly excess return")
    ax.set_title("Table I: industry excess returns, ours vs paper")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(res("table1_excess_scatter.png"), dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

def run() -> int:
    t0 = time.time()
    LAYOUT.ensure()
    print("[stage 3] Tables I/II/III + plots + per-cell JSON")

    panel, ind = load_data()
    print(f"  panel {panel.shape}, bin_rets {ind.shape}")

    print("  [3.1] replacement returns + industry auxiliary VW series ...")
    panel = add_replacement_returns(panel)
    R_sb_ind = vw_by_month_ind(panel, "r_sb")
    R_rand_ind = vw_by_month_ind(panel, "r_repl_raw")
    R_sb_rand_ind = vw_by_month_ind(panel, "r_repl_sb")
    R_dgtw_ind = vw_by_month_ind(panel, "r_dgtw")

    # industry return / signal matrices (month x 20) from bin_rets
    ind_vw_mat = ind.pivot(index="month", columns="ind",
                           values="ind_ret_vw").reindex(columns=np.arange(1, 21))
    def _sig(c):
        return ind.pivot(index="month", columns="ind",
                         values=c).reindex(columns=np.arange(1, 21))
    aux = dict(R_sb_ind=R_sb_ind, R_rand_ind=R_rand_ind,
               R_sb_rand_ind=R_sb_rand_ind, R_dgtw_ind=R_dgtw_ind,
               ind_vw_mat=ind_vw_mat, ind_mom1=_sig("ind_mom1"),
               ind_mom6=_sig("ind_mom6"), ind_mom12=_sig("ind_mom12"))

    print("  [3.2] Table I ...")
    ours_t1, detail, ftests = compute_table_1(panel, ind, R_sb_ind)

    print("  [3.3] global individual cohorts ...")
    cohorts = build_global_cohorts(panel)
    print(f"        {len(cohorts)} formable cohorts")

    print("  [3.4] Table II ...")
    ours_t2, bundle = compute_table_2(panel, ind, aux, cohorts)
    bundle["ours_t1"] = ours_t1

    print("  [3.5] Table III ...")
    ours_t3, grid = compute_table_3(aux)

    # contract + cells
    contract = json.loads(LAYOUT.preparations_path(
        "tables_to_replicate.json").read_text())
    paper_by = {t["id"]: t for t in contract["tables"]}
    cells = build_cells(contract, dict(T1=ours_t1, T2=ours_t2, T3=ours_t3))
    out_json = LAYOUT.result_path("cells_tables_1_2_3.json")
    out_json.write_text(json.dumps(cells, indent=1))
    print(f"  [3.6] wrote {out_json.name}: {len(cells)} cells")

    # tally
    tally = {}
    for c in cells:
        tally.setdefault(c["table"], {}).setdefault(c["status"], 0)
        tally[c["table"]][c["status"]] += 1
    print("\n=== per-cell tally ===")
    for tid in ("T1", "T2", "T3"):
        d = tally.get(tid, {})
        tot = sum(d.values())
        print(f"  {tid}: total={tot}  Tier1={d.get('Tier1',0)}  "
              f"Tier2={d.get('Tier2',0)}  FAIL={d.get('FAIL',0)}  "
              f"SKIP={d.get('SKIP',0)}")
        fails = [c["metric"] for c in cells
                 if c["table"] == tid and c["status"] == "FAIL"]
        if fails:
            print(f"      FAIL cells: {fails}")

    # markdown + plots
    print("  [3.7] markdown tables ...")
    write_table_1_md(detail, ftests, paper_by["T1"]["metrics"])
    write_table_2_md(ours_t2, paper_by["T2"]["metrics"])
    write_table_3_md(grid, paper_by["T3"]["metrics"])
    print("  [3.8] plots ...")
    make_plots(bundle, grid)

    print(f"\n[stage 3] done in {time.time() - t0:.1f}s")
    # return key objects for reporting
    run.ours_t1 = ours_t1
    run.ours_t2 = ours_t2
    run.ours_t3 = ours_t3
    run.grid = grid
    run.detail = detail
    run.ftests = ftests
    run.cells = cells
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
