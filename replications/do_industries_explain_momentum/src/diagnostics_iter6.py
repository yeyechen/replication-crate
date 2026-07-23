"""Iteration 6 DIAGNOSTIC-ONLY script for do_industries_explain_momentum.

Sensitivity experiments on the weighting convention (COMPUTE-AND-REPORT).

READS   data/panel.parquet ONLY (48 cols, frozen). Nothing else is read,
        nothing in data/ is written.
WRITES  results/diagnostics_iter6.json
DOES NOT modify src/main.py, src/tables_1_2_3.py, src/add_fundamentals.py,
or any parquet.

Experiments:
  A. EW 30/30, monthly rebalanced (footnote-11 reproduction: ~9.3%/yr)
     + EW 30/30 with fixed formation equal weights (comparison).
  B. VW 30/30 with MONTHLY-REBALANCED value weights (weights = me_lag1(tau),
     renormalized within the leg each holding month; membership fixed):
     - headline spread stats + leg components (full + ADJ window);
     - monthly-rebalanced VW engine applied to the six Table-II-A return
       series;
     - Panel C industry-neutral and high-ind-losers strategies with
       monthly-rebalanced VW legs (excess-industry stays EW, as paper).
  C. DT 5x5 absorption with NYSE-only breakpoints (1973-01..1995-07).

Engines reuse tables_1_2_3.py for cohorts (build_global_cohorts), the
fixed-weight spread engine (individual_spread_series), cohort averaging
(_cohort_average), industry VW matrices (vw_by_month_ind) and the random
replacement returns (add_replacement_returns). t-stats: mean/(std/sqrt(T)),
ddof=1 (A9), identical to iteration 4/5.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
_REPO_ROOT = _SRC.parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import tables_1_2_3 as t123  # noqa: E402  (engine functions, import only)
from utils.paths import paper_layout  # noqa: E402

SLUG = "do_industries_explain_momentum"
LAYOUT = paper_layout(SLUG, replications_root=_SRC.parents[1])

RAW_START = pd.Period("1963-07", "M")
RAW_END = pd.Period("1995-07", "M")
ADJ_START = pd.Period("1973-01", "M")
ADJ_END = pd.Period("1995-07", "M")

# reference values (from task spec / paper / iteration-4-5 outputs)
PAPER_IIA = {"ret": (0.0043, 4.65), "r_dgtw": (0.0009, 1.56),
             "r_sb": (0.0029, 3.34), "ret_minus_ind": (0.0013, 2.04),
             "sb_minus_ind": (0.0008, 0.91), "sb_minus_randind": (0.0027, 2.77)}
FIXED_IIA = {"ret": (0.0041, 2.31), "r_dgtw": (0.0007, 1.15),
             "r_sb": (0.0044, 2.61), "ret_minus_ind": (0.0031, 2.43),
             "sb_minus_ind": (0.0030, 2.55), "sb_minus_randind": (0.0047, 2.88)}
PAPER_PC = {"neutral": (0.0011, 1.01), "excess": (-0.0007, -0.83),
            "highlow": (0.0030, 2.66)}
FIXED_PC = {"neutral": (0.0039, 3.00), "excess": (0.0027, 1.68),
            "highlow": (-0.0004, -0.34)}

OUT = {}


def stats(series: pd.Series) -> dict:
    s = pd.Series(series).dropna().to_numpy(dtype="float64")
    T = len(s)
    if T < 2:
        return dict(mean=np.nan, std=np.nan, t=np.nan, T=T)
    m = float(np.mean(s))
    sd = float(np.std(s, ddof=1))
    t = m / (sd / np.sqrt(T)) if sd > 0 else np.nan
    return dict(mean=m, std=sd, t=t, T=T)


# ---------------------------------------------------------------------------
# monthly-rebalanced leg engine (A + B)
# ---------------------------------------------------------------------------

def rebalanced_leg_series(ret_wide: pd.DataFrame, me_wide: pd.DataFrame | None,
                          cohorts: dict, hold: int = 6,
                          mode: str = "vw_rebal"):
    """Monthly W-leg / L-leg series (overlapping 6-cohort average) with
    membership fixed over f..f+5 and weights chosen by mode:
      vw_rebal  weight_j(tau) = me_lag1_j(tau), renormalized within the leg
                over members available at tau (ret & me_lag1 non-null, >0);
      ew_rebal  equal weight across available members at tau
                (= simple mean of available member returns);
      ew_fixed  formation weights 1/N_f, renormalized over available members
                at tau (algebraically identical to ew_rebal; reported as a
                check)."""
    months_idx = ret_wide.index
    month_pos = {m: i for i, m in enumerate(months_idx)}
    col_pos = {c: j for j, c in enumerate(ret_wide.columns.to_numpy())}
    R = ret_wide.to_numpy(dtype="float64")
    M = me_wide.to_numpy(dtype="float64") if me_wide is not None else None
    cohort_fs = sorted(cohorts.keys())
    f_pos = {f: i for i, f in enumerate(cohort_fs)}
    nC, nM = len(cohort_fs), len(months_idx)
    W_mat = np.full((nC, nM), np.nan)
    L_mat = np.full_like(W_mat, np.nan)

    def leg(rrow, mrow, cols):
        if mode == "ew_rebal":
            v = rrow[cols]
            v = v[~np.isnan(v)]
            return float(v.mean()) if len(v) else np.nan
        if mode == "ew_fixed":
            v = rrow[cols]
            w = np.full(len(cols), 1.0 / len(cols))
            msk = ~np.isnan(v)
            den = w[msk].sum()
            return float(np.nansum(v * w) / den) if den > 0 else np.nan
        # vw_rebal
        v = rrow[cols]
        w = mrow[cols]
        msk = ~np.isnan(v) & ~np.isnan(w) & (w > 0.0)
        if not msk.any():
            return np.nan
        vv, ww = v[msk], w[msk]
        den = ww.sum()
        return float((vv * ww).sum() / den) if den > 0 else np.nan

    for f, (wp, _ww, lp, _lw) in cohorts.items():
        fi = f_pos[f]
        wcols = np.array([col_pos[p] for p in wp], dtype=np.int64)
        lcols = np.array([col_pos[p] for p in lp], dtype=np.int64)
        for k in range(hold):
            ri = month_pos.get(f + k)
            if ri is None:
                continue
            W_mat[fi, ri] = leg(R[ri], M[ri] if M is not None else None, wcols)
            L_mat[fi, ri] = leg(R[ri], M[ri] if M is not None else None, lcols)

    W = t123._cohort_average(W_mat, f_pos, months_idx, hold=hold)
    L = t123._cohort_average(L_mat, f_pos, months_idx, hold=hold)
    return W, L


# ---------------------------------------------------------------------------
# Panel C with monthly-rebalanced VW legs (B)
# ---------------------------------------------------------------------------

def panelC_neutral_rebalanced(panel: pd.DataFrame, ret_wide: pd.DataFrame,
                              me_wide: pd.DataFrame) -> pd.Series:
    """Industry-neutral (6,6) like t123.panelC_industry_neutral, but each
    industry leg is VW with me_lag1(tau) rebalanced monthly (membership
    fixed f..f+5); EW across industries; overlapping cohort average."""
    months_idx = ret_wide.index
    month_pos = {m: i for i, m in enumerate(months_idx)}
    col_pos = {c: j for j, c in enumerate(ret_wide.columns.to_numpy())}
    R = ret_wide.to_numpy(dtype="float64")
    M = me_wide.to_numpy(dtype="float64")

    cohort_fs, spread_by_f = [], {}
    for f, g in panel.groupby("month", sort=True):
        cs = g[g["mom6"].notna() & g["me"].notna() & (g["me"] > 0)]
        if len(cs) < 20:
            continue
        ind_blocks = []
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
            ind_blocks.append((
                np.array([col_pos[p] for p in w["permno"].to_numpy()]),
                np.array([col_pos[p] for p in l["permno"].to_numpy()]),
            ))
        cohort_fs.append(f)
        spread_by_f[f] = ind_blocks

    def vw_rebal(rrow, mrow, cols):
        v = rrow[cols]
        w = mrow[cols]
        msk = ~np.isnan(v) & ~np.isnan(w) & (w > 0.0)
        if not msk.any():
            return np.nan
        den = w[msk].sum()
        return float((v[msk] * w[msk]).sum() / den) if den > 0 else np.nan

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
                wc, lc = b
                Wr = vw_rebal(R[ri], M[ri], wc)
                Lr = vw_rebal(R[ri], M[ri], lc)
                if not (np.isnan(Wr) or np.isnan(Lr)):
                    spreads.append(Wr - Lr)
            if spreads:
                spread_mat[fi, ri] = float(np.mean(spreads))
    return t123._cohort_average(spread_mat, f_pos, months_idx, hold=6)


def panelC_high_low_rebalanced(panel: pd.DataFrame, ret_wide: pd.DataFrame,
                               me_wide: pd.DataFrame,
                               ind_sig: pd.DataFrame) -> pd.Series:
    """High-ind losers - low-ind winners (6,6) like t123.panelC_high_low,
    but each industry-block leg is VW with me_lag1(tau) rebalanced monthly
    (membership fixed); EW across the 3 industry blocks per leg; overlapping
    cohort average."""
    months_idx = ret_wide.index
    month_pos = {m: i for i, m in enumerate(months_idx)}
    col_pos = {c: j for j, c in enumerate(ret_wide.columns.to_numpy())}
    R = ret_wide.to_numpy(dtype="float64")
    M = me_wide.to_numpy(dtype="float64")

    cohort_fs, members = [], {}
    for f, g in panel.groupby("month", sort=True):
        if f not in ind_sig.index:
            continue
        row = ind_sig.loc[f].to_numpy()
        valid = ~np.isnan(row)
        if valid.sum() < 6:
            continue
        order = sorted(np.arange(1, 21)[valid], key=lambda i: row[i - 1],
                       reverse=True)
        high_inds, low_inds = order[:3], order[-3:]
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
                blocks.append(np.array(
                    [col_pos[p] for p in sel["permno"].to_numpy()]))
            return blocks

        long_blocks = leg_blocks(high_inds, "lo")
        short_blocks = leg_blocks(low_inds, "hi")
        if all(b is None for b in long_blocks) or \
                all(b is None for b in short_blocks):
            continue
        cohort_fs.append(f)
        members[f] = (long_blocks, short_blocks)

    def vw_rebal(rrow, mrow, cols):
        v = rrow[cols]
        w = mrow[cols]
        msk = ~np.isnan(v) & ~np.isnan(w) & (w > 0.0)
        if not msk.any():
            return np.nan
        den = w[msk].sum()
        return float((v[msk] * w[msk]).sum() / den) if den > 0 else np.nan

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
                v = vw_rebal(R[ri], M[ri], b)
                if not np.isnan(v):
                    longs.append(v)
            for b in short_blocks:
                if b is None:
                    continue
                v = vw_rebal(R[ri], M[ri], b)
                if not np.isnan(v):
                    shorts.append(v)
            if longs and shorts:
                spread_mat[fi, ri] = float(np.mean(longs) - np.mean(shorts))
    return t123._cohort_average(spread_mat, f_pos, months_idx, hold=6)


# ---------------------------------------------------------------------------
# experiment C: DT 5x5 matched returns with NYSE-only breakpoints
# ---------------------------------------------------------------------------

def r_sb_nyse(panel_adj: pd.DataFrame) -> tuple[pd.Series, dict]:
    """r_sb with NYSE-only (exchcd==1) 5x5 size x BE/ME breakpoints applied
    to ALL stocks; VW 25 portfolios (me_lag1 weights). Same conventions as
    add_fundamentals.dt_adjust_month except the breakpoint population
    (all-universe -> NYSE). Returns (r_sb_nyse per row, coverage info)."""
    out = pd.Series(np.nan, index=panel_adj.index, dtype="float64")
    nyse_n, valid_n, months_n = [], [], 0
    for _m, g in panel_adj.groupby("month", sort=True):
        months_n += 1
        valid = g[(g["me_lag1"] > 0) & (g["bm_sort"] > 0)]
        valid_n.append(len(valid))
        if len(valid) < 25:
            continue
        nyse = valid[valid["exchcd"] == 1]
        nyse_n.append(len(nyse))
        if len(nyse) < 25:
            continue
        size_bp = nyse["me_lag1"].quantile([0.2, 0.4, 0.6, 0.8]).to_numpy()
        vdf = valid[["me_lag1", "bm_sort", "ret"]].copy()
        vdf["size_q"] = np.digitize(vdf["me_lag1"].to_numpy(), size_bp) + 1
        nyse2 = nyse.copy()
        nyse2["size_q"] = np.digitize(nyse2["me_lag1"].to_numpy(), size_bp) + 1
        bm_bp = {}
        for s in range(1, 6):
            sub = nyse2[nyse2["size_q"] == s]
            if len(sub) < 5:
                continue
            bm_bp[s] = sub["bm_sort"].quantile([0.2, 0.4, 0.6, 0.8]).to_numpy()
        vdf["bm_q"] = np.nan
        for s, bp in bm_bp.items():
            idx = vdf.index[vdf["size_q"] == s]
            if len(idx):
                vdf.loc[idx, "bm_q"] = np.digitize(
                    vdf.loc[idx, "bm_sort"].to_numpy(), bp) + 1
        vdf = vdf[vdf["bm_q"].notna()].copy()
        if len(vdf) == 0:
            continue
        vdf["bm_q"] = vdf["bm_q"].astype(int)
        vdf["port"] = vdf["size_q"] * 10 + vdf["bm_q"]
        w = vdf[vdf["ret"].notna() & (vdf["me_lag1"] > 0)]
        if len(w) == 0:
            continue
        num = w.assign(wr=w["me_lag1"] * w["ret"]).groupby("port")["wr"].sum()
        den = w.groupby("port")["me_lag1"].sum()
        port_ret = (num / den).replace(0.0, np.nan)
        matched = vdf["port"].map(port_ret)
        ok = matched.notna()
        out.loc[vdf.index[ok]] = (g.loc[vdf.index[ok], "ret"].to_numpy()
                                  - matched[ok].to_numpy())
    info = dict(months=int(months_n),
                avg_nyse_per_month=float(np.mean(nyse_n)) if nyse_n else np.nan,
                avg_valid_per_month=float(np.mean(valid_n)),
                coverage_nonnull=float(out.notna().mean()))
    return out, info


# ---------------------------------------------------------------------------

def main() -> int:
    t0 = time.time()
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = panel["date"].dt.to_period("M")
    print(f"[load] panel {panel.shape}; months {panel['month'].min()} .. "
          f"{panel['month'].max()}; permnos {panel['permno'].nunique():,}")

    ret_wide = panel.pivot(index="month", columns="permno", values="ret")
    me_wide = panel.pivot(index="month", columns="permno", values="me_lag1")
    me_wide = me_wide.reindex(index=ret_wide.index, columns=ret_wide.columns)
    cohorts = t123.build_global_cohorts(panel)
    print(f"[cohorts] global 30/30 (mom6 nn, me>0): {len(cohorts)} formable; "
          f"ret_wide {ret_wide.shape}")

    OUT["panel_info"] = dict(shape=list(panel.shape),
                             months=[str(panel["month"].min()),
                                     str(panel["month"].max())],
                             permnos=int(panel["permno"].nunique()),
                             n_cohorts_30_30=len(cohorts))

    # ------------------------------------------------------------------
    # EXPERIMENT A — EW 30/30, monthly rebalanced (footnote 11)
    # ------------------------------------------------------------------
    print("\n========== EXPERIMENT A: EW 30/30 monthly-rebalanced ==========")
    W_er, L_er = rebalanced_leg_series(ret_wide, None, cohorts,
                                       mode="ew_rebal")
    spr_er = W_er - L_er
    W_ef, L_ef = rebalanced_leg_series(ret_wide, None, cohorts,
                                       mode="ew_fixed")
    spr_ef = W_ef - L_ef

    A = {}
    for name, a, b in [("full_1963-07_1995-07", RAW_START, RAW_END),
                       ("adj_1973-01_1995-07", ADJ_START, ADJ_END)]:
        s_r = t123.restrict(spr_er, a, b)
        s_f = t123.restrict(spr_ef, a, b)
        st_r = stats(s_r)
        st_f = stats(s_f)
        st_r["mean_pct_mo"] = st_r["mean"] * 100.0
        st_r["annualized_mean_pct"] = st_r["mean"] * 12.0 * 100.0
        st_f["mean_pct_mo"] = st_f["mean"] * 100.0
        st_f["annualized_mean_pct"] = st_f["mean"] * 12.0 * 100.0
        A[name] = dict(ew_rebalanced=st_r, ew_fixed_weights=st_f)
        print(f"A {name}:")
        print(f"   EW monthly-rebalanced: mean={st_r['mean_pct_mo']:.4f}%/mo "
              f"std={st_r['std']:.6f} t={st_r['t']:.3f} T={st_r['T']} "
              f"annualized={st_r['annualized_mean_pct']:.2f}%/yr "
              f"(footnote 11: 9.3%/yr = 0.775%/mo)")
        print(f"   EW fixed formation wts: mean={st_f['mean_pct_mo']:.4f}%/mo "
              f"t={st_f['t']:.3f} T={st_f['T']} "
              f"annualized={st_f['annualized_mean_pct']:.2f}%/yr")
    same = t123.restrict(spr_er, RAW_START, RAW_END) - \
        t123.restrict(spr_ef, RAW_START, RAW_END)
    A["max_abs_diff_rebal_vs_fixed"] = float(np.nanmax(np.abs(same.to_numpy())))
    print(f"   max |EW-rebal - EW-fixed| over full period = "
          f"{A['max_abs_diff_rebal_vs_fixed']:.3e} "
          f"(identical by construction: 1/N renormalized == simple mean)")
    fn11 = 0.093 / 12.0
    m_full = A["full_1963-07_1995-07"]["ew_rebalanced"]["mean"]
    A["footnote11_rel_err_full"] = float((m_full - fn11) / fn11)
    m_adj = A["adj_1973-01_1995-07"]["ew_rebalanced"]["mean"]
    A["footnote11_rel_err_adj"] = float((m_adj - fn11) / fn11)
    A["footnote11_within_25pct_full"] = bool(abs(A["footnote11_rel_err_full"]) <= 0.25)
    A["footnote11_within_25pct_adj"] = bool(abs(A["footnote11_rel_err_adj"]) <= 0.25)
    OUT["A"] = A

    # ------------------------------------------------------------------
    # EXPERIMENT B — VW 30/30 with monthly-rebalanced value weights
    # ------------------------------------------------------------------
    print("\n========== EXPERIMENT B: VW 30/30 monthly-rebalanced ==========")
    W_rb, L_rb = rebalanced_leg_series(ret_wide, me_wide, cohorts,
                                       mode="vw_rebal")
    spr_rb = W_rb - L_rb
    B = {}

    # headline stats
    for name, a, b in [("full_1963-07_1995-07", RAW_START, RAW_END),
                       ("adj_1973-01_1995-07", ADJ_START, ADJ_END)]:
        st = stats(t123.restrict(spr_rb, a, b))
        B[name] = st
        print(f"B VW-rebal W-L {name}: mean={st['mean']:.6f} "
              f"std={st['std']:.6f} t={st['t']:.3f} T={st['T']}")
    print(f"   (fixed-weight baseline: 0.004135 / 0.035115 / t=2.311; "
          f"paper: 0.0043 / 0.0178 / t=4.65)")

    # component stats (full window, matching iter5 1e window)
    Wf = t123.restrict(W_rb, RAW_START, RAW_END)
    Lf = t123.restrict(L_rb, RAW_START, RAW_END)
    sW = float(Wf.std(ddof=1))
    sL = float(Lf.std(ddof=1))
    rho = float(Wf.corr(Lf))
    B["components_full"] = dict(
        std_W=sW, std_L=sL, corr_WL=rho,
        mean_W=float(Wf.mean()), mean_L=float(Lf.mean()),
        implied_std_WminusL=float(np.sqrt(sW**2 + sL**2 - 2 * rho * sW * sL)))
    print(f"B components (full): std(W)={sW:.4f} std(L)={sL:.4f} "
          f"corr(W,L)={rho:.4f} mean(W)={B['components_full']['mean_W']:.6f} "
          f"mean(L)={B['components_full']['mean_L']:.6f}")
    print(f"   (fixed-weight components: 0.0495 / 0.0561 / 0.786)")

    # ---- B2: six Table-II-A series through the monthly-rebalanced engine ----
    print("\nB Table-II-A series with monthly-rebalanced VW weights:")
    R_sb_ind = t123.vw_by_month_ind(panel, "r_sb")            # me_lag1 weights
    panel2 = t123.add_replacement_returns(panel)
    R_sb_rand_ind = t123.vw_by_month_ind(panel2, "r_repl_sb")
    pan = panel.merge(R_sb_ind.stack().rename("R_sb_ind").reset_index(),
                      on=["month", "ind"], how="left")
    pan = pan.merge(R_sb_rand_ind.stack().rename("R_sb_rand_ind").reset_index(),
                    on=["month", "ind"], how="left")
    pan["ret_minus_ind"] = pan["ret"] - pan["ind_ret_vw"]
    pan["sb_minus_ind"] = pan["r_sb"] - pan["R_sb_ind"]
    pan["sb_minus_randind"] = pan["r_sb"] - pan["R_sb_rand_ind"]

    specs = [("ret", "full_1963-07_1995-07", RAW_START, RAW_END),
             ("r_dgtw", "adj_1973-01_1995-07", ADJ_START, ADJ_END),
             ("r_sb", "adj_1973-01_1995-07", ADJ_START, ADJ_END),
             ("ret_minus_ind", "full_1963-07_1995-07", RAW_START, RAW_END),
             ("sb_minus_ind", "adj_1973-01_1995-07", ADJ_START, ADJ_END),
             ("sb_minus_randind", "adj_1973-01_1995-07", ADJ_START, ADJ_END)]
    B["table_IIA_rebalanced"] = {}
    for col, win, a, b in specs:
        wide = pan.pivot(index="month", columns="permno", values=col)
        if col == "ret":
            Wc, Lc = W_rb, L_rb
        else:
            Wc, Lc = rebalanced_leg_series(wide, me_wide, cohorts,
                                           mode="vw_rebal")
        st = stats(t123.restrict(Wc - Lc, a, b))
        pm, pt = PAPER_IIA[col]
        fm, ft = FIXED_IIA[col]
        B["table_IIA_rebalanced"][col] = dict(
            window=win, **st, paper_mean=pm, paper_t=pt,
            fixed_mean=fm, fixed_t=ft)
        print(f"   {col:<16s} [{win}]: mean={st['mean']:+.6f} "
              f"t={st['t']:+.3f} T={st['T']} | paper {pm:+.4f}/{pt:.2f} | "
              f"fixed {fm:+.4f}/{ft:.2f}")
    del pan, panel2

    # ---- B3: Panel C with monthly-rebalanced VW legs ----
    print("\nB Panel C with monthly-rebalanced VW legs:")
    ind_sig = (panel.drop_duplicates(["month", "ind"])
               .set_index(["month", "ind"])["ind_mom6"]
               .unstack("ind").reindex(columns=np.arange(1, 21)))
    neut_rb = panelC_neutral_rebalanced(panel, ret_wide, me_wide)
    st = stats(t123.restrict(neut_rb, RAW_START, RAW_END))
    pm, pt = PAPER_PC["neutral"]
    fm, ft = FIXED_PC["neutral"]
    B["panelC_neutral_rebalanced"] = dict(**st, paper_mean=pm, paper_t=pt,
                                          fixed_mean=fm, fixed_t=ft)
    print(f"   industry-neutral (rebal VW legs, EW across industries): "
          f"mean={st['mean']:+.6f} t={st['t']:+.3f} T={st['T']} | "
          f"paper {pm:+.4f}/{pt:.2f} | fixed {fm:+.4f}/{ft:.2f}")

    hl_rb = panelC_high_low_rebalanced(panel, ret_wide, me_wide, ind_sig)
    st = stats(t123.restrict(hl_rb, RAW_START, RAW_END))
    pm, pt = PAPER_PC["highlow"]
    fm, ft = FIXED_PC["highlow"]
    B["panelC_highlow_rebalanced"] = dict(**st, paper_mean=pm, paper_t=pt,
                                          fixed_mean=fm, fixed_t=ft)
    print(f"   high-ind losers - low-ind winners (rebal VW legs): "
          f"mean={st['mean']:+.6f} t={st['t']:+.3f} T={st['T']} | "
          f"paper {pm:+.4f}/{pt:.2f} | fixed {fm:+.4f}/{ft:.2f}")

    exc_ew = t123.panelC_excess_industry(panel, ret_wide)
    st = stats(t123.restrict(exc_ew, RAW_START, RAW_END))
    pm, pt = PAPER_PC["excess"]
    fm, ft = FIXED_PC["excess"]
    B["panelC_excess_ew_unchanged"] = dict(**st, paper_mean=pm, paper_t=pt,
                                           fixed_mean=fm, fixed_t=ft)
    print(f"   excess-industry (EW, unchanged per paper): "
          f"mean={st['mean']:+.6f} t={st['t']:+.3f} T={st['T']} | "
          f"paper {pm:+.4f}/{pt:.2f} | fixed {fm:+.4f}/{ft:.2f}")
    OUT["B"] = B

    # ------------------------------------------------------------------
    # EXPERIMENT C — DT absorption with NYSE breakpoints
    # ------------------------------------------------------------------
    print("\n========== EXPERIMENT C: NYSE-breakpoint DT absorption ==========")
    adj = panel[(panel["month"] >= ADJ_START) &
                (panel["month"] <= ADJ_END)].copy()
    rsb_nyse, cov = r_sb_nyse(adj)
    print(f"C r_sb_nyse coverage: {cov['months']} months, avg NYSE "
          f"breakpoint stocks/month = {cov['avg_nyse_per_month']:.0f}, "
          f"avg eligible/month = {cov['avg_valid_per_month']:.0f}, "
          f"nonnull fraction = {cov['coverage_nonnull']:.4f}")

    wide_nyse = adj.assign(r_sb_nyse=rsb_nyse).pivot(
        index="month", columns="permno", values="r_sb_nyse")
    wide_nyse = wide_nyse.reindex(index=ret_wide.index,
                                  columns=ret_wide.columns)
    bench_nyse = t123.individual_spread_series(wide_nyse, cohorts, hold=6)
    bench_nyse_adj = t123.restrict(bench_nyse, ADJ_START, ADJ_END)
    st_bench = stats(bench_nyse_adj)

    # same-engine references: raw W-L over ADJ and all-universe r_sb benchmark
    raw_spread = t123.individual_spread_series(ret_wide, cohorts, hold=6)
    raw_adj = t123.restrict(raw_spread, ADJ_START, ADJ_END)
    st_raw = stats(raw_adj)
    sb_all_wide = panel.pivot(index="month", columns="permno", values="r_sb")
    sb_all_wide = sb_all_wide.reindex(index=ret_wide.index,
                                      columns=ret_wide.columns)
    bench_all = t123.individual_spread_series(sb_all_wide, cohorts, hold=6)
    bench_all_adj = t123.restrict(bench_all, ADJ_START, ADJ_END)
    st_bench_all = stats(bench_all_adj)

    absorb_nyse = (raw_adj - bench_nyse_adj).dropna()
    absorb_all = (raw_adj - bench_all_adj).dropna()
    st_abs_nyse = stats(absorb_nyse)
    st_abs_all = stats(absorb_all)

    C = dict(
        coverage=cov,
        sb_WminusL_NYSE_bp=st_bench,
        sb_WminusL_alluniverse=st_bench_all,
        raw_WminusL_ADJ=st_raw,
        absorption_raw_minus_sb_NYSE=st_abs_nyse,
        absorption_raw_minus_sb_alluniverse=st_abs_all,
        paper_sb_WminusL=(0.0029, 3.34),
        paper_implied_absorption_bp=14.0,
    )
    OUT["C"] = C
    print(f"C SB W-L (NYSE breakpoints) ADJ: mean={st_bench['mean']:.6f} "
          f"({st_bench['mean'] * 1e4:+.2f}bp) t={st_bench['t']:.3f} "
          f"T={st_bench['T']} (paper 0.0029/3.34; all-universe "
          f"{st_bench_all['mean']:.6f}/t={st_bench_all['t']:.3f})")
    print(f"C raw W-L ADJ: mean={st_raw['mean']:.6f} t={st_raw['t']:.3f} "
          f"T={st_raw['T']}")
    print(f"C absorption (raw - benchmark) NYSE: "
          f"mean={st_abs_nyse['mean']:.6f} "
          f"({st_abs_nyse['mean'] * 1e4:+.2f}bp) t={st_abs_nyse['t']:.3f} "
          f"T={st_abs_nyse['T']} (paper-implied +14bp)")
    print(f"C absorption (raw - benchmark) all-universe: "
          f"mean={st_abs_all['mean']:.6f} "
          f"({st_abs_all['mean'] * 1e4:+.2f}bp) t={st_abs_all['t']:.3f} "
          f"T={st_abs_all['T']} (iter5: -1.76bp / t=-0.25)")

    # ------------------------------------------------------------------
    # decision-rule inputs
    # ------------------------------------------------------------------
    OUT["decision_rule"] = dict(
        footnote11_target_per_month=fn11,
        A_ew_rebal_mean_full=m_full,
        A_ew_rebal_mean_adj=m_adj,
        A_within_25pct_full=A["footnote11_within_25pct_full"],
        A_within_25pct_adj=A["footnote11_within_25pct_adj"],
        B_vw_rebal_t_full=B["full_1963-07_1995-07"]["t"],
        B_fixed_weight_t=2.311,
        B_t_above_fixed=bool(B["full_1963-07_1995-07"]["t"] > 2.311),
    )

    jpath = LAYOUT.result_path("diagnostics_iter6.json")
    jpath.write_text(json.dumps(OUT, indent=1, default=str))
    print(f"\n[wrote] {jpath}")
    print(f"[total time] {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
