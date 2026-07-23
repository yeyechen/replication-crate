"""Iteration 5 DIAGNOSTIC-ONLY script for do_industries_explain_momentum.

READS   data/panel.parquet (48 cols, frozen), data/bin_rets.parquet,
        and ONE in-memory SQL pull of (permno, ym, retx) from crsp_202601.msf
        for 1962-01..1995-07 (retx is not in the panel; nothing is written
        to data/).
WRITES  results/diagnostics_iter5.md (+ results/diagnostics_iter5.json).
DOES NOT modify src/main.py, src/tables_1_2_3.py, src/add_fundamentals.py,
or any parquet.

Diagnostics:
  1a-1f: (6,6) W-L spread volatility decomposition (raw VW 30/30, EW 10/10
         JT93-style variant, retx vs ret, subperiods, leg components,
         loser delisting proxy).
  2a-2d: DT 5x5 adjustment characterization (5x5 VW table, benchmark
         absorption series, winner/loser characteristic profiles, r_sb/ret
         correlation).
  3a-3f: Panel C within-industry strategies (engine verification at
         1990-06, per-industry W-L series, subperiods, EW vs VW industry
         signal sensitivity, high-ind losers leg decomposition, FM
         regression with/without industry FE).
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
from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402

SLUG = "do_industries_explain_momentum"
LAYOUT = paper_layout(SLUG, replications_root=_SRC.parents[1])

RAW_START = pd.Period("1963-07", "M")
RAW_END = pd.Period("1995-07", "M")
ADJ_START = pd.Period("1973-01", "M")
ADJ_END = pd.Period("1995-07", "M")

IND_NAMES = t123.IND_NAMES

OUT = {}   # collects everything for the JSON dump


def mean_t(series):
    return t123.mean_t(series)


def restrict(series, start, end):
    return t123.restrict(series, start, end)


def leg_series(ret_wide: pd.DataFrame, cohorts: dict, hold: int = 6,
               equal_weight: bool = False):
    """Monthly W-leg and L-leg series (overlapping cohort average), same
    engine as t123.individual_spread_series but returning both legs.
    Renormalizes fixed formation weights over available members; with
    equal_weight=True uses 1/N over available members."""
    months_idx = ret_wide.index
    month_pos = {m: i for i, m in enumerate(months_idx)}
    col_pos = {c: j for j, c in enumerate(ret_wide.columns.to_numpy())}
    arr = ret_wide.to_numpy(dtype="float64")
    cohort_fs = sorted(cohorts.keys())
    f_pos = {f: i for i, f in enumerate(cohort_fs)}
    W_mat = np.full((len(cohort_fs), len(months_idx)), np.nan)
    L_mat = np.full_like(W_mat, np.nan)

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
            if equal_weight:
                W_mat[fi, ri] = float(Rw[mw].mean()) if mw.any() else np.nan
            else:
                denw = ww[mw].sum()
                W_mat[fi, ri] = (float(np.nansum(Rw * ww) / denw)
                                 if denw > 0 else np.nan)
            Rl = arr[ri, lcols]
            ml = ~np.isnan(Rl)
            if equal_weight:
                L_mat[fi, ri] = float(Rl[ml].mean()) if ml.any() else np.nan
            else:
                denl = lw[ml].sum()
                L_mat[fi, ri] = (float(np.nansum(Rl * lw) / denl)
                                 if denl > 0 else np.nan)

    def _avg(mat):
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

    return _avg(W_mat), _avg(L_mat)


def build_cohorts_generic(panel, lo_q=0.30, hi_q=0.70):
    """Global mom6 cohorts: universe mom6 non-null & me>0; winners mom6>=p_hi,
    losers mom6<=p_lo; weights me(f)/sum (used unless equal_weight legs)."""
    cohorts = {}
    for f, g in panel.groupby("month", sort=True):
        cs = g[g["mom6"].notna() & g["me"].notna() & (g["me"] > 0)]
        if len(cs) < 20:
            continue
        mom = cs["mom6"].to_numpy()
        plo = np.quantile(mom, lo_q)
        phi = np.quantile(mom, hi_q)
        win = cs[mom >= phi]
        los = cs[mom <= plo]
        if len(win) == 0 or len(los) == 0:
            continue
        wm = win["me"].to_numpy(dtype="float64")
        lm = los["me"].to_numpy(dtype="float64")
        cohorts[f] = (win["permno"].to_numpy(), wm / wm.sum(),
                      los["permno"].to_numpy(), lm / lm.sum())
    return cohorts


# ---------------------------------------------------------------------------
# load
# ---------------------------------------------------------------------------

def load():
    t0 = time.time()
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = panel["date"].dt.to_period("M")
    ind = pd.read_parquet(LAYOUT.data_path("bin_rets.parquet"))
    ind["month"] = ind["date"].dt.to_period("M")
    print(f"[load] panel {panel.shape}, ind {ind.shape} in "
          f"{time.time() - t0:.1f}s")
    return panel, ind


# ---------------------------------------------------------------------------
# DIAGNOSTIC 1
# ---------------------------------------------------------------------------

def diag1(panel, ret_wide, cohorts):
    print("\n========== DIAGNOSTIC 1: (6,6) W-L spread volatility ==========")
    res = {}

    # 1a. raw VW 30/30 W-L (exact iteration-4 engine + leg decomposition)
    spread = t123.individual_spread_series(ret_wide, cohorts, hold=6)
    spread_s = restrict(spread, RAW_START, RAW_END)
    W, L = leg_series(ret_wide, cohorts)
    W_s, L_s = restrict(W, RAW_START, RAW_END), restrict(L, RAW_START, RAW_END)
    m, sd = float(spread_s.mean()), float(spread_s.std(ddof=1))
    T = int(spread_s.notna().sum())
    t = m / (sd / np.sqrt(T))
    res["1a"] = dict(mean=m, std=sd, t=t, T=T,
                     paper_mean=0.0043, paper_t=4.65,
                     iter4_mean=0.004135, iter4_t=2.311)
    print(f"1a raw VW 30/30 W-L 1963-07..1995-07: mean={m:.6f} std={sd:.6f} "
          f"t={t:.3f} T={T}  (paper 0.0043/t=4.65; iter4 0.004135/t=2.311)")

    # 1b. EW 10/10 JT93-style variant
    cohorts10 = build_cohorts_generic(panel, lo_q=0.10, hi_q=0.90)
    W10, L10 = leg_series(ret_wide, cohorts10, equal_weight=True)
    spr10 = restrict(W10 - L10, RAW_START, RAW_END)
    m10, t10, T10 = mean_t(spr10)
    res["1b"] = dict(mean=m10, std=float(spr10.std(ddof=1)), t=t10, T=T10,
                     n_cohorts=len(cohorts10),
                     avg_winners=float(np.mean([len(c[0]) for c in cohorts10.values()])),
                     avg_losers=float(np.mean([len(c[2]) for c in cohorts10.values()])))
    print(f"1b EW 10/10 W-L: mean={m10:.6f} std={res['1b']['std']:.6f} "
          f"t={t10:.3f} T={T10} ({len(cohorts10)} cohorts, avg "
          f"{res['1b']['avg_winners']:.0f} winners / "
          f"{res['1b']['avg_losers']:.0f} losers per cohort)")

    # 1c. retx (ex-distribution/ex-delisting) holding returns, same cohorts
    print("1c pulling retx from crsp_202601.msf (in-memory only) ...")
    cfg = get_clickhouse_config()
    from clickhouse_driver import Client
    c = Client(host=cfg["host"], port=int(cfg["port"]), user=cfg["user"],
               password=cfg["password"],
               settings={"max_execution_time": 600})
    try:
        data = c.execute(
            "SELECT permno, substr(date, 1, 7) AS ym, "
            "CAST(retx AS Nullable(Float64)) AS retx "
            "FROM crsp_202601.msf "
            "WHERE toDate32(date) >= toDate32('1962-01-01') "
            "AND toDate32(date) <= toDate32('1995-07-31') "
            "SETTINGS max_rows_to_read = 10000000000, "
            "timeout_before_checking_execution_speed = 0")
    finally:
        c.disconnect()
    rx = pd.DataFrame(data, columns=["permno", "ym", "retx"])
    rx["permno"] = rx["permno"].astype("int64")
    rx["retx"] = rx["retx"].astype("float64")
    n_sent = int((rx["retx"] < -1.0).sum())
    rx.loc[rx["retx"] < -1.0, "retx"] = np.nan
    rx["month"] = rx["ym"].map(pd.Period)
    print(f"   retx rows: {len(rx):,}; sentinels (<-1) -> NaN: {n_sent:,}; "
          f"null: {int(rx['retx'].isna().sum()):,}")
    retx_wide = (rx.pivot_table(index="month", columns="permno",
                                values="retx", aggfunc="first")
                 .reindex(index=ret_wide.index, columns=ret_wide.columns))
    # overlap of retx with panel ret (both non-null) in sample
    j = pd.concat([ret_wide.stack().rename("ret"),
                   retx_wide.stack().rename("retx")], axis=1).dropna()
    res["1c_overlap"] = dict(n_joint=int(len(j)),
                             corr=float(j["ret"].corr(j["retx"])),
                             mean_diff=float((j["ret"] - j["retx"]).mean()))
    del rx, j

    res["1c_coverage"] = dict(
        frac_panel_ret_cells_with_retx=float(
            retx_wide.notna().sum().sum() / ret_wide.notna().sum().sum()))
    Wx, Lx = leg_series(retx_wide, cohorts)
    sprx = restrict(Wx - Lx, RAW_START, RAW_END)
    mx, tx, Tx = mean_t(sprx)
    res["1c"] = dict(mean=mx, std=float(sprx.std(ddof=1)), t=tx, T=Tx,
                     std_ret=res["1a"]["std"],
                     delta_std=float(res["1a"]["std"] - sprx.std(ddof=1)),
                     delta_mean=float(res["1a"]["mean"] - mx))
    print(f"1c VW 30/30 W-L with retx: mean={mx:.6f} "
          f"std={res['1c']['std']:.6f} t={tx:.3f} T={Tx} | "
          f"ret-std {res['1a']['std']:.6f} -> retx-std "
          f"{res['1c']['std']:.6f} (delta ret-retx = "
          f"{res['1c']['delta_std']:.6f}); mean delta (ret-retx) = "
          f"{res['1c']['delta_mean']:.6f}")

    # 1d. subperiod stats of raw VW 30/30 W-L
    subs = [("1963-07..1972-12", RAW_START, pd.Period("1972-12", "M")),
            ("1973-01..1984-12", pd.Period("1973-01", "M"), pd.Period("1984-12", "M")),
            ("1985-01..1995-07", pd.Period("1985-01", "M"), RAW_END)]
    res["1d"] = {}
    for name, a, b in subs:
        s = restrict(spread_s, a, b)
        mm, tt, TT = mean_t(s)
        res["1d"][name] = dict(mean=mm, std=float(s.std(ddof=1)), t=tt, T=TT)
        print(f"1d {name}: mean={mm:.6f} std={s.std(ddof=1):.6f} t={tt:.3f} T={TT}")

    # 1e. component stats
    sW = float(W_s.std(ddof=1)); sL = float(L_s.std(ddof=1))
    rho = float(W_s.corr(L_s))
    implied = float(np.sqrt(sW**2 + sL**2 - 2 * rho * sW * sL))
    res["1e"] = dict(std_W=sW, std_L=sL, corr_WL=rho,
                     implied_std_WminusL=implied,
                     direct_std_WminusL=res["1a"]["std"],
                     mean_W=float(W_s.mean()), mean_L=float(L_s.mean()))
    print(f"1e std(W)={sW:.6f} std(L)={sL:.6f} corr(W,L)={rho:.4f} -> "
          f"implied std(W-L)={implied:.6f} vs direct {res['1a']['std']:.6f}")
    print(f"   mean(W)={res['1e']['mean_W']:.6f} mean(L)={res['1e']['mean_L']:.6f}")

    # 1f. loser-leg check
    last_month = panel.groupby("permno")["month"].max()
    n_los, n_win = [], []
    frac_los_del, frac_win_del = [], []
    for f, (wp, ww, lp, lw) in cohorts.items():
        end = f + 5
        n_los.append(len(lp)); n_win.append(len(wp))
        fl = last_month.reindex(lp)
        frac_los_del.append(float((fl <= end).mean()))
        fw = last_month.reindex(wp)
        frac_win_del.append(float((fw <= end).mean()))
    res["1f"] = dict(
        n_cohorts=len(cohorts),
        avg_losers_per_cohort=float(np.mean(n_los)),
        avg_winners_per_cohort=float(np.mean(n_win)),
        frac_losers_delist_in_window=float(np.mean(frac_los_del)),
        frac_winners_delist_in_window=float(np.mean(frac_win_del)),
    )
    print(f"1f cohorts={len(cohorts)}; avg losers/cohort="
          f"{res['1f']['avg_losers_per_cohort']:.1f} (winners "
          f"{res['1f']['avg_winners_per_cohort']:.1f}); "
          f"frac losers with last panel row <= f+5 = "
          f"{res['1f']['frac_losers_delist_in_window']:.4f} "
          f"(winners: {res['1f']['frac_winners_delist_in_window']:.4f})")
    return res, W_s, L_s, spread_s, Wx, Lx


# ---------------------------------------------------------------------------
# DIAGNOSTIC 2
# ---------------------------------------------------------------------------

def diag2(panel, ret_wide, cohorts, raw_spread, W_leg, L_leg):
    print("\n========== DIAGNOSTIC 2: DT 5x5 adjustment ==========")
    res = {}
    adj = panel[(panel["month"] >= ADJ_START) & (panel["month"] <= ADJ_END)]
    elig = adj[adj["ret"].notna() & adj["me_lag1"].notna() &
               (adj["me_lag1"] > 0) & adj["bm_sort"].notna()].copy()
    print(f"2a eligible rows 1973-01..1995-07 (ret, me_lag1>0, bm_sort): "
          f"{len(elig):,}; bm_sort null% in ADJ panel: "
          f"{adj['bm_sort'].isna().mean() * 100:.2f}%; avg elig/month: "
          f"{len(elig) / elig['month'].nunique():.0f}")

    cell_ret = {}   # (sz, bm) -> {month: VW return}
    months = sorted(elig["month"].unique())
    for mon in months:
        g = elig[elig["month"] == mon]
        sz = g["me_lag1"].to_numpy()
        sb = np.quantile(sz, [0.2, 0.4, 0.6, 0.8])
        szbin = np.searchsorted(sb, sz, side="left") + 1   # 1=small .. 5=large
        for s in range(1, 6):
            gs = g.loc[szbin == s]
            if len(gs) == 0:
                continue
            bmb = np.quantile(gs["bm_sort"].to_numpy(), [0.2, 0.4, 0.6, 0.8])
            bmbin = np.searchsorted(bmb, gs["bm_sort"].to_numpy(),
                                    side="left") + 1
            for b in range(1, 6):
                gc = gs.loc[bmbin == b]
                if len(gc) == 0:
                    continue
                w = gc["me_lag1"].to_numpy(dtype="float64")
                r = gc["ret"].to_numpy(dtype="float64")
                cell_ret.setdefault((s, b), {})[mon] = float(
                    (w * r).sum() / w.sum())

    table = np.full((5, 5), np.nan)
    for (s, b), v in cell_ret.items():
        table[s - 1, b - 1] = float(np.mean(list(v.values()))) * 100.0
    print("2a 5x5 VW monthly mean returns (%/mo), rows=size 1(small)..5(large),"
          " cols=BM 1(low)..5(high):")
    hdr = "      " + "".join(f"{'BM'+str(b):>9s}" for b in range(1, 6))
    print(hdr)
    for s in range(1, 6):
        print(f"  SZ{s} " + "".join(f"{table[s-1, b-1]:9.4f}" for b in range(1, 6)))

    # value premium: per month avg over size of (BM5 - BM1);
    # size premium: per month avg over BM of (SZ1 - SZ5)
    vp, sp_sz = [], []
    for mon in months:
        hi = np.array([cell_ret.get((s, 5), {}).get(mon, np.nan)
                       for s in range(1, 6)], float)
        lo = np.array([cell_ret.get((s, 1), {}).get(mon, np.nan)
                       for s in range(1, 6)], float)
        vp.append(np.nanmean(hi - lo))
        sm = np.array([cell_ret.get((1, b), {}).get(mon, np.nan)
                       for b in range(1, 6)], float)
        lg = np.array([cell_ret.get((5, b), {}).get(mon, np.nan)
                       for b in range(1, 6)], float)
        sp_sz.append(np.nanmean(sm - lg))
    vp_s = pd.Series(vp, index=months).dropna()
    sp_s = pd.Series(sp_sz, index=months).dropna()
    vpm, vpt, vpT = mean_t(vp_s)
    spm, spt, spT = mean_t(sp_s)
    res["2a"] = dict(
        table_pct=(np.round(table, 4)).tolist(),
        value_premium_pct=dict(mean=float(vpm * 100), t=float(vpt), T=int(vpT)),
        size_premium_pct=dict(mean=float(spm * 100), t=float(spt), T=int(spT)),
        n_elig_rows=int(len(elig)),
        avg_elig_per_month=float(len(elig) / elig["month"].nunique()),
        bm_null_pct_adj=float(adj["bm_sort"].isna().mean() * 100),
    )
    print(f"   hiBM-loBM (value premium): {vpm * 100:.4f}%/mo, t={vpt:.2f}, T={vpT}")
    print(f"   small-large (size premium): {spm * 100:.4f}%/mo, t={spt:.2f}, T={spT}")

    # 2b. benchmark absorption: W-L of DT matched returns (r_sb), same cohorts
    sb_wide = panel.pivot(index="month", columns="permno", values="r_sb")
    sb_wide = sb_wide.reindex(index=ret_wide.index, columns=ret_wide.columns)
    bench = t123.individual_spread_series(sb_wide, cohorts, hold=6)
    bench_adj = restrict(bench, ADJ_START, ADJ_END)
    bm, bt, bT = mean_t(bench_adj)
    raw_series = raw_spread
    raw_adj = restrict(raw_series, ADJ_START, ADJ_END)
    rm, rt, rT = mean_t(raw_adj)
    absorb = (raw_adj - bench_adj).dropna()
    am, at, aT = mean_t(absorb)
    res["2b"] = dict(
        benchmark_WminusL_adj=dict(mean=bm, t=bt, T=bT),
        raw_WminusL_adj=dict(mean=rm, t=rt, T=rT),
        absorption_raw_minus_benchmark=dict(mean=am, t=at, T=aT),
        paper_benchmark_implication=0.0014,
        iter4_pA_sb_mean=0.0044466,
    )
    print(f"2b DT benchmark W-L (r_sb) 1973-01..1995-07: mean={bm:.6f} t={bt:.3f} "
          f"T={bT} (paper implication +0.0014)")
    print(f"   raw W-L over same ADJ window: mean={rm:.6f} t={rt:.3f} T={rT}")
    print(f"   absorption (raw - benchmark): mean={am:.6f} t={at:.3f} T={aT}")

    # 2c. characteristic profiles at formation (cohorts formed in ADJ window)
    rows_prof = []
    fmin, fmax = ADJ_START, ADJ_END
    pf = panel.set_index(["permno", "month"], drop=False)
    for f, (wp, ww, lp, lw) in cohorts.items():
        if f < fmin or f > fmax:
            continue
        wrows = pf.loc[list(zip(wp, [f] * len(wp)))]
        lrows = pf.loc[list(zip(lp, [f] * len(lp)))]
        rows_prof.append(dict(
            f=str(f),
            w_lnsize=wrows["ln_size"].mean(), l_lnsize=lrows["ln_size"].mean(),
            w_lnbeme=wrows["ln_beme"].mean(), l_lnbeme=lrows["ln_beme"].mean(),
            w_lnmeF=np.log(wrows["me"]).mean(), l_lnmeF=np.log(lrows["me"]).mean(),
            w_lnbeme_cov=wrows["ln_beme"].notna().mean(),
            l_lnbeme_cov=lrows["ln_beme"].notna().mean(),
        ))
    prof = pd.DataFrame(rows_prof)
    res["2c"] = dict(
        n_cohorts=int(len(prof)),
        mean_ln_size_W=float(prof["w_lnsize"].mean()),
        mean_ln_size_L=float(prof["l_lnsize"].mean()),
        mean_ln_beme_W=float(prof["w_lnbeme"].mean()),
        mean_ln_beme_L=float(prof["l_lnbeme"].mean()),
        mean_ln_me_at_f_W=float(prof["w_lnmeF"].mean()),
        mean_ln_me_at_f_L=float(prof["l_lnmeF"].mean()),
        mean_ln_beme_coverage_W=float(prof["w_lnbeme_cov"].mean()),
        mean_ln_beme_coverage_L=float(prof["l_lnbeme_cov"].mean()),
    )
    print(f"2c over {len(prof)} ADJ cohorts: mean ln(size, me_lag1) W="
          f"{res['2c']['mean_ln_size_W']:.4f} L={res['2c']['mean_ln_size_L']:.4f}"
          f" (W-L={res['2c']['mean_ln_size_W'] - res['2c']['mean_ln_size_L']:+.4f});"
          f" mean ln(me@f) W={res['2c']['mean_ln_me_at_f_W']:.4f} "
          f"L={res['2c']['mean_ln_me_at_f_L']:.4f}")
    print(f"   mean ln(BE/ME) W={res['2c']['mean_ln_beme_W']:.4f} "
          f"L={res['2c']['mean_ln_beme_L']:.4f} "
          f"(W-L={res['2c']['mean_ln_beme_W'] - res['2c']['mean_ln_beme_L']:+.4f});"
          f" ln_beme coverage W={res['2c']['mean_ln_beme_coverage_W'] * 100:.1f}%"
          f" L={res['2c']['mean_ln_beme_coverage_L'] * 100:.1f}%")

    # 2d. corr(leg r_sb, leg ret)
    Wsb, Lsb = leg_series(sb_wide, cohorts)
    def _corr(a, b, s0, s1):
        a, b = restrict(a, s0, s1), restrict(b, s0, s1)
        m = a.notna() & b.notna()
        return float(a[m].corr(b[m]))
    W_ret, L_ret = W_leg, L_leg   # passed in from diag1 (same engine)
    res["2d"] = dict(
        corr_W_sb_ret_ADJ=_corr(Wsb, W_ret, ADJ_START, ADJ_END),
        corr_L_sb_ret_ADJ=_corr(Lsb, L_ret, ADJ_START, ADJ_END),
        corr_W_sb_ret_RAW=_corr(Wsb, W_ret, RAW_START, RAW_END),
        corr_L_sb_ret_RAW=_corr(Lsb, L_ret, RAW_START, RAW_END),
    )
    print(f"2d corr(W_sb, W_ret): ADJ={res['2d']['corr_W_sb_ret_ADJ']:.4f}, "
          f"RAW={res['2d']['corr_W_sb_ret_RAW']:.4f}; "
          f"corr(L_sb, L_ret): ADJ={res['2d']['corr_L_sb_ret_ADJ']:.4f}, "
          f"RAW={res['2d']['corr_L_sb_ret_RAW']:.4f}")
    return res


# ---------------------------------------------------------------------------
# DIAGNOSTIC 3
# ---------------------------------------------------------------------------

def within_industry_blocks(cs):
    """Per-industry cohort blocks at formation: list of 20 entries, each
    (wpermnos, wweights, lpermnos, lweights) or None. Mirrors
    t123.panelC_industry_neutral eligibility (len(cs)<20 skip cohort,
    len(ci)<4 skip industry)."""
    blocks = [None] * 20
    counts = []
    for i in range(1, 21):
        ci = cs[cs["ind"] == i]
        if len(ci) < 4:
            counts.append((i, len(ci), 0, 0))
            continue
        mom = ci["mom6"].to_numpy()
        p30 = np.quantile(mom, 0.30)
        p70 = np.quantile(mom, 0.70)
        w = ci[mom >= p70]
        l = ci[mom <= p30]
        counts.append((i, len(ci), len(w), len(l)))
        if len(w) == 0 or len(l) == 0:
            continue
        wm = w["me"].to_numpy(dtype="float64")
        lm = l["me"].to_numpy(dtype="float64")
        blocks[i - 1] = (w["permno"].to_numpy(), wm / wm.sum(),
                         l["permno"].to_numpy(), lm / lm.sum())
    return blocks, counts


def diag3(panel, ret_wide, ind):
    print("\n========== DIAGNOSTIC 3: Panel C within-industry ==========")
    res = {}
    months_idx = ret_wide.index
    month_pos = {m: i for i, m in enumerate(months_idx)}
    col_pos = {c: j for j, c in enumerate(ret_wide.columns.to_numpy())}
    arr = ret_wide.to_numpy(dtype="float64")

    # 3a. engine verification at f = 1990-06
    f0 = pd.Period("1990-06", "M")
    g0 = panel[panel["month"] == f0]
    cs0 = g0[g0["mom6"].notna() & g0["me"].notna() & (g0["me"] > 0)]
    _, counts0 = within_industry_blocks(cs0)
    print(f"3a f=1990-06: universe eligible (mom6 nn & me>0) = {len(cs0)}")
    print("   ind | n_elig | n_win | n_los | win/elig | los/elig")
    a_rows = []
    for i, n, nw, nl in counts0:
        a_rows.append(dict(ind=i, name=IND_NAMES[i], n_elig=int(n),
                           n_win=int(nw), n_los=int(nl),
                           win_ratio=(nw / n if n else np.nan),
                           los_ratio=(nl / n if n else np.nan)))
        print(f"   {i:3d} {IND_NAMES[i]:<13s} {n:6d} {nw:7d} {nl:7d} "
              f"{(nw / n if n else 0):8.3f} {(nl / n if n else 0):8.3f}")
    res["3a"] = a_rows

    # ---- per-industry within-industry (6,6) engine (3b) ----
    cohort_fs, blocks_by_f = [], {}
    for f, g in panel.groupby("month", sort=True):
        cs = g[g["mom6"].notna() & g["me"].notna() & (g["me"] > 0)]
        if len(cs) < 20:
            continue
        blocks, _ = within_industry_blocks(cs)
        cohort_fs.append(f)
        blocks_by_f[f] = blocks
    f_pos = {f: i for i, f in enumerate(cohort_fs)}
    nC, nM = len(cohort_fs), len(months_idx)
    sp_ind = [np.full((nC, nM), np.nan) for _ in range(20)]
    for f, blocks in blocks_by_f.items():
        fi = f_pos[f]
        for k in range(6):
            ri = month_pos.get(f + k)
            if ri is None:
                continue
            for i, b in enumerate(blocks):
                if b is None:
                    continue
                wp, ww, lp, lw = b
                Wr = t123._vw_arr(arr[ri], np.array([col_pos[p] for p in wp]), ww)
                Lr = t123._vw_arr(arr[ri], np.array([col_pos[p] for p in lp]), lw)
                if not (np.isnan(Wr) or np.isnan(Lr)):
                    sp_ind[i][fi, ri] = Wr - Lr

    def cohort_avg(mat):
        out = np.full(nM, np.nan)
        for ti in range(nM):
            t = months_idx[ti]
            vals = []
            for k in range(6):
                fi = f_pos.get(t - k)
                if fi is None:
                    continue
                v = mat[fi, ti]
                if not np.isnan(v):
                    vals.append(v)
            if vals:
                out[ti] = float(np.mean(vals))
        return pd.Series(out, index=months_idx)

    ind_series = {i + 1: cohort_avg(sp_ind[i]) for i in range(20)}

    # 3b. per-industry W-L means/t + cross-industry average
    print("\n3b per-industry within-industry (6,6) W-L, 1963-07..1995-07:")
    b_rows = {}
    pos = 0
    means = []
    for i in range(1, 21):
        s = restrict(ind_series[i], RAW_START, RAW_END)
        m, t, T = mean_t(s)
        b_rows[i] = dict(mean=m, t=t, T=T)
        means.append(m)
        pos += int(m > 0)
        print(f"   {i:2d} {IND_NAMES[i]:<13s} mean={m:+.6f} t={t:+.2f} T={T}")
    # industry-neutral reconstruction: monthly EW average of per-industry series
    neut_df = pd.DataFrame(ind_series)
    neut_recon = restrict(neut_df.mean(axis=1), RAW_START, RAW_END)
    nm, nt, nT = mean_t(neut_recon)
    # engine-exact industry-neutral series for comparison
    neut_exact = restrict(t123.panelC_industry_neutral(panel, ret_wide),
                          RAW_START, RAW_END)
    nem, net, neT = mean_t(neut_exact)
    res["3b"] = dict(
        per_industry=b_rows,
        n_positive=int(pos),
        cross_industry_avg_mean=float(np.mean(means)),
        neutral_reconstructed_EW_of_ind_series=dict(mean=nm, t=nt, T=nT),
        neutral_engine_exact=dict(mean=nem, t=net, T=neT),
        iter4_pC_industry_neutral=0.0038575,
    )
    print(f"   {pos}/20 positive; cross-industry average of means="
          f"{np.mean(means):+.6f}")
    print(f"   neutral (EW of 20 per-industry monthly series): mean={nm:+.6f} "
          f"t={nt:.3f}; engine-exact neutral: mean={nem:+.6f} t={net:.3f}")

    # 3c. subperiods: neutral + excess
    exc_exact = t123.panelC_excess_industry(panel, ret_wide)
    res["3c"] = {}
    for name, a, b in [("1963-07..1972-12", RAW_START, pd.Period("1972-12", "M")),
                       ("1973-01..1995-07", ADJ_START, RAW_END)]:
        ns = restrict(neut_exact, a, b)
        es = restrict(exc_exact, a, b)
        nm_, nt_, nT_ = mean_t(ns)
        em, et, eT = mean_t(es)
        res["3c"][name] = dict(neutral=dict(mean=nm_, t=nt_, T=nT_),
                               excess=dict(mean=em, t=et, T=eT))
        print(f"3c {name}: neutral mean={nm_:+.6f} t={nt_:.3f} T={nT_} | "
              f"excess mean={em:+.6f} t={et:.3f} T={eT}")

    # 3d. excess-industry with EW industry signal
    ind_ew = ind.pivot(index="month", columns="ind", values="ind_ret_ew")
    ind_ew = ind_ew.reindex(columns=np.arange(1, 21))
    ind_mom6_ew = (
        (1.0 + ind_ew).rolling(6, min_periods=6)
        .apply(np.prod, raw=True).shift(1) - 1.0
    )
    # strict-window check vs VW ind_mom6 (pooled correlation of the two)
    ind_vw_sig = ind.pivot(index="month", columns="ind", values="ind_mom6")
    cj = pd.concat([ind_mom6_ew.stack().rename("ew"),
                    ind_vw_sig.stack().rename("vw")], axis=1).dropna()
    cchk = float(cj["ew"].corr(cj["vw"]))
    mom6_ew_long = ind_mom6_ew.stack().rename("ind_mom6_ew").reset_index()
    pan2 = panel.merge(mom6_ew_long, on=["month", "ind"], how="left")
    pan2["xs_ew"] = pan2["mom6"] - pan2["ind_mom6_ew"]
    pan2["xs_vw"] = pan2["mom6"] - pan2["ind_mom6"]

    def excess_engine(sig_panel, sig_col):
        """panelC_excess_industry clone parameterized on signal column."""
        cohort_fs2, members = [], {}
        for f, g in sig_panel.groupby("month", sort=True):
            cs = g[g[sig_col].notna() & g["me"].notna() & (g["me"] > 0)]
            if len(cs) < 20:
                continue
            sig = cs[sig_col].to_numpy()
            p30 = np.quantile(sig, 0.30)
            p70 = np.quantile(sig, 0.70)
            w = cs[sig >= p70]
            l = cs[sig <= p30]
            if len(w) == 0 or len(l) == 0:
                continue
            cohort_fs2.append(f)
            members[f] = (
                np.array([col_pos[p] for p in w["permno"].to_numpy()]),
                np.array([col_pos[p] for p in l["permno"].to_numpy()]),
            )
        fp2 = {f: i for i, f in enumerate(cohort_fs2)}
        mat = np.full((len(cohort_fs2), nM), np.nan)
        for f, (wc, lc) in members.items():
            fi = fp2[f]
            for k in range(6):
                ri = month_pos.get(f + k)
                if ri is None:
                    continue
                Wr = t123._ew_arr(arr[ri], wc)
                Lr = t123._ew_arr(arr[ri], lc)
                if not (np.isnan(Wr) or np.isnan(Lr)):
                    mat[fi, ri] = Wr - Lr
        out = np.full(nM, np.nan)
        for ti in range(nM):
            t = months_idx[ti]
            vals = []
            for k in range(6):
                fi = fp2.get(t - k)
                if fi is None:
                    continue
                v = mat[fi, ti]
                if not np.isnan(v):
                    vals.append(v)
            if vals:
                out[ti] = float(np.mean(vals))
        return pd.Series(out, index=months_idx)

    exc_vw_sig = restrict(excess_engine(pan2, "xs_vw"), RAW_START, RAW_END)
    exc_ew_sig = restrict(excess_engine(pan2, "xs_ew"), RAW_START, RAW_END)
    vm, vt, vT = mean_t(exc_vw_sig)
    em2, et2, eT2 = mean_t(exc_ew_sig)
    # exact engine baseline for reference
    exc_base = restrict(exc_exact, RAW_START, RAW_END)
    bm2, bt2, bT2 = mean_t(exc_base)
    res["3d"] = dict(
        corr_ind_mom6_EW_vs_VW=float(cchk),
        excess_with_VW_ind_mom6_clone=dict(mean=vm, t=vt, T=vT),
        excess_engine_exact_VW=dict(mean=bm2, t=bt2, T=bT2),
        excess_with_EW_ind_mom6=dict(mean=em2, t=et2, T=eT2),
    )
    print(f"3d corr(ind_mom6_EW, ind_mom6_VW) pooled = {cchk:.4f}")
    print(f"   excess (VW signal, clone): mean={vm:+.6f} t={vt:.3f}; "
          f"engine exact: mean={bm2:+.6f} t={bt2:.3f}")
    print(f"   excess (EW signal):        mean={em2:+.6f} t={et2:.3f} T={eT2}")

    # 3e. high-ind losers: f=1990-06 snapshot + separate legs full period
    ind_sig = (ind.drop_duplicates(["month", "ind"])
               .set_index(["month", "ind"])["ind_mom6"].unstack("ind")
               .reindex(columns=np.arange(1, 21)))
    row0 = ind_sig.loc[f0].to_numpy()
    order0 = sorted(np.arange(1, 21)[~np.isnan(row0)],
                    key=lambda i: row0[i - 1], reverse=True)
    hi3, lo3 = order0[:3], order0[-3:]
    print("3e f=1990-06 industry ranking by ind_mom6 (top3 / bottom3):")
    print("   TOP3 (winner industries -> short leg uses their top-30%):")
    for i in hi3:
        print(f"     ind {i:2d} {IND_NAMES[i]:<13s} ind_mom6={row0[i-1]:+.4f}")
    print("   BOTTOM3 (loser industries -> long leg uses their bottom-30%):")
    for i in lo3:
        print(f"     ind {i:2d} {IND_NAMES[i]:<13s} ind_mom6={row0[i-1]:+.4f}")
    snap = {"f": str(f0), "top3": [], "bottom3": []}
    for i in hi3 + lo3:
        ci = cs0[cs0["ind"] == i]
        mom = ci["mom6"].to_numpy()
        p30 = np.quantile(mom, 0.30)
        p70 = np.quantile(mom, 0.70)
        nb = int((mom <= p30).sum())
        nt_ = int((mom >= p70).sum())
        rec = dict(ind=int(i), name=IND_NAMES[i],
                   ind_mom6=float(row0[i - 1]), n_elig=int(len(ci)),
                   n_bottom30=nb, n_top30=nt_)
        if i in hi3:
            snap["top3"].append(rec)
            print(f"     ind {i:2d}: bottom-30% (LONG leg here) n={nb}, "
                  f"top-30% n={nt_}, n_elig={len(ci)}")
        else:
            snap["bottom3"].append(rec)
            print(f"     ind {i:2d}: top-30% (SHORT leg here) n={nt_}, "
                  f"bottom-30% n={nb}, n_elig={len(ci)}")

    # full-period separate legs (panelC_high_long clone with leg outputs)
    cohort_fs3, members3 = [], {}
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
            out = []
            for i in inds:
                ci = cs[cs["ind"] == i]
                if len(ci) < 4:
                    out.append(None)
                    continue
                mom = ci["mom6"].to_numpy()
                p30 = np.quantile(mom, 0.30)
                p70 = np.quantile(mom, 0.70)
                sel = ci[mom <= p30] if want == "lo" else ci[mom >= p70]
                if len(sel) == 0:
                    out.append(None)
                    continue
                sm = sel["me"].to_numpy(dtype="float64")
                out.append((np.array([col_pos[p] for p in sel["permno"].to_numpy()]),
                            sm / sm.sum()))
            return out

        lb = leg_blocks(high_inds, "lo")
        sbk = leg_blocks(low_inds, "hi")
        if all(b is None for b in lb) or all(b is None for b in sbk):
            continue
        cohort_fs3.append(f)
        members3[f] = (lb, sbk)

    fp3 = {f: i for i, f in enumerate(cohort_fs3)}
    LONG = np.full((len(cohort_fs3), nM), np.nan)
    SHORT = np.full_like(LONG, np.nan)
    for f, (lb, sbk) in members3.items():
        fi = fp3[f]
        for k in range(6):
            ri = month_pos.get(f + k)
            if ri is None:
                continue
            longs, shorts = [], []
            for b in lb:
                if b is None:
                    continue
                v = t123._vw_arr(arr[ri], b[0], b[1])
                if not np.isnan(v):
                    longs.append(v)
            for b in sbk:
                if b is None:
                    continue
                v = t123._vw_arr(arr[ri], b[0], b[1])
                if not np.isnan(v):
                    shorts.append(v)
            if longs:
                LONG[fi, ri] = float(np.mean(longs))
            if shorts:
                SHORT[fi, ri] = float(np.mean(shorts))
    long_s = restrict(cohort_avg(LONG), RAW_START, RAW_END)
    short_s = restrict(cohort_avg(SHORT), RAW_START, RAW_END)
    lm, lt, lT = mean_t(long_s)
    smm, smt, smT = mean_t(short_s)
    spr_hl = restrict(cohort_avg(LONG) - cohort_avg(SHORT), RAW_START, RAW_END)
    hm, ht, hT = mean_t(spr_hl)
    res["3e"] = dict(snapshot=snap,
                     long_leg=dict(mean=lm, t=lt, T=lT),
                     short_leg=dict(mean=smm, t=smt, T=smT),
                     spread_long_minus_short=dict(mean=hm, t=ht, T=hT),
                     iter4_spread=-0.0004357)
    print(f"   full period: LONG (bottom-30% of top3 industries) mean={lm:+.6f} "
          f"t={lt:.3f} T={lT}")
    print(f"              SHORT (top-30% of bottom3 industries) mean={smm:+.6f} "
          f"t={smt:.3f} T={smT}")
    print(f"              spread L-S mean={hm:+.6f} t={ht:.3f} "
          f"(iter4 = -0.000436; paper +0.0030)")

    # 3f. FM regression next-month ret on mom6, with/without industry FE
    print("3f FM cross-sectional regressions (next-month ret on mom6) ...")
    p = panel[["permno", "month", "ret", "mom6", "ind"]].copy()
    p = p.sort_values(["permno", "month"])
    p["next_ret"] = p.groupby("permno")["ret"].shift(-1)
    sub = p[(p["month"] >= RAW_START) & (p["month"] <= RAW_END)
            & p["mom6"].notna() & p["next_ret"].notna()]
    sub = sub.sort_values("month")
    mom_v = sub["mom6"].to_numpy()
    y = sub["next_ret"].to_numpy()
    codes = sub["ind"].to_numpy() - 1          # industries 1..20 -> 0..19
    mon = sub["month"].to_numpy()
    positions = pd.Series(np.arange(len(sub)), index=mon).groupby(level=0)
    coef_b, coef_fe, t_months, cs_sizes = [], [], [], []
    for m, pos_s in positions:
        pos = pos_s.to_numpy()
        ncs = len(pos)
        cs_sizes.append(ncs)
        if ncs < 30:   # keep FE regressions full-rank-safe
            continue
        xb = np.column_stack([np.ones(ncs), mom_v[pos]])
        D = np.eye(20)[codes[pos]][:, :19]     # ind 20 = reference
        xf = np.column_stack([xb, D])
        bb = np.linalg.lstsq(xb, y[pos], rcond=None)[0]
        bf = np.linalg.lstsq(xf, y[pos], rcond=None)[0]
        coef_b.append(float(bb[1]))
        coef_fe.append(float(bf[1]))
        t_months.append(m)
    cb = pd.Series(coef_b, index=t_months)
    cf = pd.Series(coef_fe, index=t_months)
    mb, tb, Tb = mean_t(cb)
    mf, tf, Tf = mean_t(cf)
    res["3f"] = dict(
        no_FE=dict(mom6_coef=mb, t=tb, T=Tb),
        with_industry_FE=dict(mom6_coef=mf, t=tf, T=Tf),
        n_cross_sections=int(Tb),
        avg_stocks_per_cs=float(len(sub) / max(Tb, 1)),
        min_cs_size=int(min(cs_sizes)), max_cs_size=int(max(cs_sizes)),
        n_cs_dropped_below_30=int(sum(n < 30 for n in cs_sizes)),
    )
    print(f"   no FE:        mom6 coef = {mb:.6f} (t={tb:.2f}, T={Tb})")
    print(f"   industry FE:  mom6 coef = {mf:.6f} (t={tf:.2f}, T={Tf})")
    print(f"   FE absorbs {((mb - mf) / mb * 100) if mb else float('nan'):.1f}% "
          f"of the raw slope; avg stocks/cs = {len(sub) / Tb:.0f}")
    return res


# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    panel, ind = load()
    print(f"panel months: {panel['month'].min()} .. {panel['month'].max()}, "
          f"permnos {panel['permno'].nunique():,}")

    ret_wide = panel.pivot(index="month", columns="permno", values="ret")
    print(f"ret_wide {ret_wide.shape}")
    cohorts = t123.build_global_cohorts(panel)
    print(f"global cohorts (30/30, me>0, mom6 nn): {len(cohorts)}")

    OUT["panel_info"] = dict(
        shape=list(panel.shape),
        months=[str(panel["month"].min()), str(panel["month"].max())],
        permnos=int(panel["permno"].nunique()),
        retx_in_panel=False,
        n_cohorts_30_30=len(cohorts),
    )

    r1, W_s, L_s, spread_s, Wx, Lx = diag1(panel, ret_wide, cohorts)
    OUT["diag1"] = r1
    r2 = diag2(panel, ret_wide, cohorts, spread_s, W_s, L_s)
    OUT["diag2"] = r2
    r3 = diag3(panel, ret_wide, ind)
    OUT["diag3"] = r3

    jpath = LAYOUT.result_path("diagnostics_iter5.json")
    jpath.write_text(json.dumps(OUT, indent=1, default=str))
    print(f"\n[wrote] {jpath}")
    print(f"[total time] {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
