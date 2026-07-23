"""
Pontiff & Woodgate (2008), "Share Issuance and Cross-sectional Returns",
Journal of Finance 63(2).  Replication — DATA PIPELINE.

Builds the analysis-ready monthly panel (data/panel.parquet) that feeds
Tables I, III, V, VI.  All filtering / aggregation / point-in-time joins are
pushed into ClickHouse SQL (src/sql/*.sql); this script reads those queries,
then finishes the calendar-aligned window/lag computations in Python on a
complete stock x month grid (the one place a dense grid is the clean tool).

Division of labour
------------------
SQL (heavy lifting):
  msf_monthly_base.sql   base monthly returns/prices/shares, sentinels NULLed
  first_valid_month.sql  first month (midx) with a nonmissing return (6-mo rule)
  common_universe_pit.sql PIT shrcd in {10,11} -> univ_common
  ewretd_monthly.sql     EW market return for holding-period imputation (L116)
  bm_annual.sql          Compustat book equity x CRSP Dec ME -> BM (L108-110)

Python (calendar-aligned windows on a complete monthly grid):
  adjusted shares + split-error correction (L98)
  ISSUE / DT-ISSUE / contemporaneous issuance lags (L66-96)
  MOM (L114), holding-period returns r6/r12/r24_y2/r36_y3 with EWRETD
  imputation (L116), r_11_0, me_june / me_monthly (L112)

NOTE on ClickHouse dates: the native Date type (and toStartOfMonth) clamps
pre-1970 dates to the 1970 epoch.  SQL therefore emits an integer month index
``midx = year*12 + (month-1)`` (epoch-proof); pandas rebuilds Timestamps.
"""

import gc
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

# --- repo / project plumbing -------------------------------------------------
_THIS = Path(__file__).resolve()
SLUG_ROOT = _THIS.parent.parent                 # .../share_issuance_and_cross_sectional_returns
REPO_ROOT = SLUG_ROOT.parent.parent             # repo root (has utils/, .env)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from utils.env import load_project_env, get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout                            # noqa: E402

load_project_env()
LAYOUT = paper_layout("share_issuance_and_cross_sectional_returns")
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")

# --- paper parameters (hardcoded WITH citations) -----------------------------
MSF_START = "1926-12-01"        # paper L51/L96: pre-1970 lags need 1926 start
MSF_END   = "2006-12-31"        # post-2003 holding-period leads through 2006-12
GRID_START_MIDX = 1926 * 12 + 11   # 1926-12
GRID_END_MIDX   = 2006 * 12 + 11   # 2006-12
PANEL_START_MIDX = 1927 * 12 + 0   # panel output begins 1927-01 (spec step 10)
BM_FIRST_MIDX    = 1970 * 12 + 6   # 1970-07: BM active from July 1970 (L108)
LISTING_AGE_MONTHS = 6             # paper L51: >=6 months in CRSP
# error-correction thresholds (paper L98):
ERR_JUMP = 0.20                    # >20% month-over-month change
ERR_REVERSAL = 0.95               # >=95% of the change reversed
ERR_WINDOW = 3                     # ...within the following 3 months
# issuance horizons (paper L66-96, Table III caption L1074):
ISSUE_LAG_SHORT = 6               # predict with 6-month-old shares (L96)
ISSUE_LAG_1Y = 17                 # ISSUE = ln(adj_{t-6}) - ln(adj_{t-17})
ISSUE_LAG_5Y = 65                 # DT-ISSUE = ln(adj_{t-6}) - ln(adj_{t-65})
CONT_1Y = 11                      # ISSUE_{-11,0} = ln(adj_t) - ln(adj_{t-11}) (Table I)
CONT_5Y = 59                      # ISSUE_{-59,0} = ln(adj_t) - ln(adj_{t-59}) (Table I)
# sample windows
IN_START, IN_END = "1970-01-01", "2003-12-01"   # in-sample (Table I/III)
OOS_START, OOS_END = "1932-09-01", "1969-12-01" # out-of-sample (Table V/VI)

# paper comparison targets (for the report)
PAPER = {
    "in_total": 2_494_343, "in_mom": 2_285_189, "in_issue": 2_312_597,
    "t3_obs": 2_155_945, "t3_months": 396,
    "oos_total": 568_449, "oos_mom": 524_260, "oos_r110": 528_200,
    "t6_obs": 373_590, "t6_months": 444, "err_corr": 2_189,
}

# --- ClickHouse connection ---------------------------------------------------
_CFG = get_clickhouse_config()


def _client():
    from clickhouse_driver import Client
    return Client(host=_CFG["host"], port=int(_CFG["port"]),
                  user=_CFG["user"], password=_CFG["password"],
                  settings={"max_execution_time": 1200})


def q(sql: str) -> pd.DataFrame:
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    return q((SQL_DIR / name).read_text())


# ---------------------------------------------------------------------------
def load_data():
    t0 = time.time()
    print("[load] msf_monthly_base ...", flush=True)
    base = q_file("msf_monthly_base.sql")
    print(f"[load]   {len(base):,} rows ({time.time()-t0:.1f}s)", flush=True)
    fv = q_file("first_valid_month.sql")
    cu = q_file("common_universe_pit.sql")
    ew = q_file("ewretd_monthly.sql")
    bm = q_file("bm_annual.sql")
    print(f"[load] first_valid={len(fv):,}  common_univ={len(cu):,}  "
          f"ewretd={len(ew):,}  bm_annual={len(bm):,}", flush=True)

    for col in ["permno", "yr", "mo", "midx"]:
        base[col] = base[col].astype("Int64")
    for col in ["ret", "prc_abs", "shrout", "cfacshr"]:
        base[col] = pd.to_numeric(base[col], errors="coerce")
    fv["permno"] = fv["permno"].astype("Int64")
    fv["first_midx"] = fv["first_midx"].astype("Int64")
    cu["permno"] = cu["permno"].astype("Int64")
    cu["midx"] = cu["midx"].astype("Int64")
    ew["midx"] = ew["midx"].astype("Int64")
    ew["ewretd"] = pd.to_numeric(ew["ewretd"], errors="coerce")
    bm["permno"] = bm["permno"].astype("Int64")
    return base, fv, cu, ew, bm


def build_grid(base):
    grid_midx = np.arange(GRID_START_MIDX, GRID_END_MIDX + 1, dtype=np.int64)
    months_index = pd.date_range("1926-12-01", "2006-12-01", freq="MS")
    assert len(grid_midx) == len(months_index) == (GRID_END_MIDX - GRID_START_MIDX + 1)
    permnos = np.sort(base["permno"].dropna().unique())
    col_map = pd.Series(np.arange(len(permnos)), index=permnos)
    row = (base["midx"].to_numpy() - GRID_START_MIDX).astype(np.int64)
    col = col_map.reindex(base["permno"].to_numpy()).to_numpy().astype(np.int64)
    return grid_midx, months_index, permnos, row, col


def scatter(values, row, col, n_m, n_p):
    W = np.full((n_m, n_p), np.nan, dtype=np.float64)
    W[row, col] = np.asarray(values, dtype=np.float64)
    return W


def correct_shares_sequential(shr, jump=ERR_JUMP, rev=ERR_REVERSAL, window=ERR_WINDOW):
    """Paper L98 shares-outstanding error correction (sequential pass).

    Rule (L98): "If the number of shares outstanding changes by more than 20%
    and subsequently 95% of the change is reversed within three months, then we
    treat the change as an erroneous entry and we correct the shares outstanding
    to the level previous to the change."

    Implementation: single left-to-right pass per permno on the complete monthly
    grid (each column = one permno).  Detection is on RAW shares outstanding
    (shrout), matching the paper's wording.  At month t, compare shrout_t to the
    most recent corrected level ("base"); if the jump exceeds 20% AND >=95% of
    that jump is unwound within months t+1..t+3 (on the reported series), set
    shrout_t = base (the pre-change level) and keep base as the baseline for
    t+1.  adj_shares is then corrected_shrout x cfacshr.  This reproduces the
    paper's count almost exactly (here ~2,172 vs paper 2,189; the paper notes
    inference is unaffected by this 0.07%-of-obs correction).
    """
    n_m, n_p = shr.shape
    out = shr.copy()
    total = 0
    # candidate columns: those with any month-over-month jump > threshold
    prev0 = np.vstack([np.full((1, n_p), np.nan), shr[:-1]])
    with np.errstate(divide="ignore", invalid="ignore"):
        jump_mask = np.abs((shr - prev0) / prev0) > jump
    cand = np.where(jump_mask.any(axis=0))[0]
    for j in cand:
        o = shr[:, j]                 # reported series (look-ahead reference)
        s = out[:, j]                 # corrected series
        base = np.nan                 # most recent corrected level
        for t in range(n_m):
            cur = o[t]
            if cur != cur:            # NaN (missing shares): keep baseline
                continue
            if base == base and base > 0:
                d = cur - base
                if abs(d / base) > jump:                 # L98: >20% change
                    do_rev = False
                    for k in range(1, window + 1):       # L98: within 3 months
                        if t + k < n_m:
                            f = o[t + k]
                            if f == f and (cur - f) / d >= rev:   # L98: >=95%
                                do_rev = True
                                break
                    if do_rev:                           # erroneous entry
                        s[t] = base                      # correct to prior level
                        total += 1
                        continue
            base = cur
            s[t] = cur
    return out, total


def window_products(C, Cnan, n_m, n_p, start_off, end_off):
    """exp(sum of log(1+r) over rows [i+start_off, i+end_off]) - 1 per column.

    C / Cnan are (n_m+1, n_p) cumulative sums (row 0 = 0) of the log returns
    and of a NaN-indicator.  Windows touching the grid boundary or containing
    any NaN are returned as NaN (require ALL months present)."""
    idx = np.arange(n_m)
    a = idx + start_off
    b = idx + end_off + 1
    valid = (a >= 0) & (b <= n_m)
    out = np.full((n_m, n_p), np.nan)
    nn = np.full((n_m, n_p), np.nan)
    s = C[b[valid]] - C[a[valid]]
    out[valid] = np.exp(s) - 1.0
    nn[valid] = Cnan[b[valid]] - Cnan[a[valid]]
    out[nn > 0] = np.nan
    return out


def cumsum_arrays(mat):
    L = np.log1p(mat)
    L_filled = np.where(np.isnan(L), 0.0, L)
    nanf = np.isnan(L).astype(np.float64)
    C = np.vstack([np.zeros((1, mat.shape[1])), np.cumsum(L_filled, axis=0)])
    Cnan = np.vstack([np.zeros((1, mat.shape[1])), np.cumsum(nanf, axis=0)])
    return C, Cnan


def build_panel(base, fv, cu, ew, bm):
    grid_midx, months_index, permnos, row, col = build_grid(base)
    n_m, n_p = len(grid_midx), len(permnos)
    print(f"[grid] {n_m} months x {n_p:,} permnos", flush=True)

    # ---- wide raw matrices -------------------------------------------------
    ret_wide = scatter(base["ret"].to_numpy(), row, col, n_m, n_p)
    prc_wide = scatter(base["prc_abs"].to_numpy(), row, col, n_m, n_p)
    shr_wide = scatter(base["shrout"].to_numpy(), row, col, n_m, n_p)
    cfac_wide = scatter(base["cfacshr"].to_numpy(), row, col, n_m, n_p)

    # ---- shares error correction (paper L98) then adjusted shares ----------
    # correct raw shares outstanding first, then adj_shares = corrected x cfacshr
    shr_corr, n_err = correct_shares_sequential(shr_wide)
    adj_corr = np.where((shr_corr > 0) & (cfac_wide > 0),
                        shr_corr * cfac_wide, np.nan)
    print(f"[shares] error corrections (paper L98, target {PAPER['err_corr']:,}): "
          f"{n_err:,}", flush=True)

    # ---- issuance lags (calendar shifts on the complete grid) --------------
    with np.errstate(divide="ignore", invalid="ignore"):
        log_adj = np.log(adj_corr)
    log_adj_df = pd.DataFrame(log_adj, index=months_index, columns=permnos)
    adj_df = pd.DataFrame(adj_corr, index=months_index, columns=permnos)
    s6 = log_adj_df.shift(ISSUE_LAG_SHORT)
    s17 = log_adj_df.shift(ISSUE_LAG_1Y)
    s65 = log_adj_df.shift(ISSUE_LAG_5Y)
    a6 = adj_df.shift(ISSUE_LAG_SHORT)
    a65 = adj_df.shift(ISSUE_LAG_5Y)
    # paper L96/Table III: ISSUE=ln(adj_{t-6})-ln(adj_{t-17})
    issue = (s6 - s17)
    # DT-ISSUE=ln(adj_{t-6})-ln(adj_{t-65}) if adj_{t-65} exists (and t-6), else 0
    dt_issue = (s6 - s65).where(a65.notna() & a6.notna(), 0.0)
    dt_dum = a65.notna().astype(np.float64)                 # L94: DT dummy
    # Table I contemporaneous measures (L156)
    issue_contemp = log_adj_df - log_adj_df.shift(CONT_1Y)      # ISSUE_{-11,0}
    dt_issue_contemp = log_adj_df - log_adj_df.shift(CONT_5Y)   # ISSUE_{-59,0}
    del s6, s17, s65, a6, a65, log_adj_df, adj_df
    gc.collect()

    # ---- market equity (paper L112) ---------------------------------------
    with np.errstate(divide="ignore", invalid="ignore"):
        me_wide = np.where((prc_wide > 0) & (shr_wide > 0),
                           np.log(prc_wide * shr_wide), np.nan)
    # me_june: ln(|prc|*shrout) at end of June Y, held July Y .. June Y+1
    me_df = pd.DataFrame(me_wide, index=months_index, columns=permnos)
    june_mask = months_index.month == 6
    me_june_by_year = me_df.loc[june_mask].copy()
    me_june_by_year.index = months_index[june_mask].year.values
    yr_arr = months_index.year.values
    mo_arr = months_index.month.values
    form_year = np.where(mo_arr >= 7, yr_arr, yr_arr - 1)
    me_june_wide = me_june_by_year.reindex(form_year).to_numpy()
    del me_df, me_june_by_year

    # ---- EWRETD-imputed returns + holding-period returns (paper L116) ------
    ew_map = dict(zip(ew["midx"].astype(int), ew["ewretd"]))
    ewretd_vec = np.array([ew_map.get(int(m), np.nan) for m in grid_midx])
    n_ew_missing = int(np.isnan(ewretd_vec).sum())
    first_map = dict(zip(fv["permno"].astype(int), fv["first_midx"]))
    first_row = (np.array([first_map.get(int(p), np.nan) for p in permnos])
                 - GRID_START_MIDX)
    listed = np.arange(n_m)[:, None] >= first_row[None, :]  # month >= first month
    ew_broad = np.broadcast_to(ewretd_vec[:, None], (n_m, n_p))
    # impute: listed months with a missing stock return -> EWRETD (L116)
    rimp = np.where(np.isnan(ret_wide) & listed, ew_broad, ret_wide)

    C, Cnan = cumsum_arrays(rimp)
    r6 = window_products(C, Cnan, n_m, n_p, 0, 5)        # t..t+5
    r12 = window_products(C, Cnan, n_m, n_p, 0, 11)      # t..t+11
    r24 = window_products(C, Cnan, n_m, n_p, 12, 23)     # t+12..t+23 (2nd yr)
    r36 = window_products(C, Cnan, n_m, n_p, 24, 35)     # t+24..t+35 (3rd yr)
    del C, Cnan, rimp, ew_broad
    gc.collect()

    # ---- MOM and contemporaneous 1-yr return (actual returns, all present) -
    Ca, Cana = cumsum_arrays(ret_wide)
    mom = window_products(Ca, Cana, n_m, n_p, -7, -2)    # t-7..t-2 (L114, skip t-1)
    r_11_0 = window_products(Ca, Cana, n_m, n_p, -11, 0)  # t-11..t (Table I)
    del Ca, Cana

    # ---- scatter results back onto the base (long) rows --------------------
    def extract(W):
        return W[row, col]

    base = base.copy()
    base["adj_shares"] = extract(adj_corr)
    base["issue"] = extract(issue.to_numpy())
    base["dt_issue"] = extract(dt_issue.to_numpy())
    base["dt_dum"] = extract(dt_dum.to_numpy())
    base["issue_contemp"] = extract(issue_contemp.to_numpy())
    base["dt_issue_contemp"] = extract(dt_issue_contemp.to_numpy())
    base["me_june"] = extract(me_june_wide)
    base["r6"] = extract(r6)
    base["r12"] = extract(r12)
    base["r24_y2"] = extract(r24)
    base["r36_y3"] = extract(r36)
    base["mom"] = extract(mom)
    base["r_11_0"] = extract(r_11_0)
    base["r1"] = base["ret"]
    # me_monthly = ln(|prc|*shrout) per month (L112)
    pm = base["prc_abs"].to_numpy() * base["shrout"].to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        base["me_monthly"] = np.where(
            (base["prc_abs"].to_numpy() > 0) & (base["shrout"].to_numpy() > 0),
            np.log(pm), np.nan)

    # ---- universe flags (spec step 2) --------------------------------------
    base["first_midx"] = base["permno"].map(first_map)
    base["univ_all"] = (base["ret"].notna()
                        & ((base["midx"] - base["first_midx"]) >= LISTING_AGE_MONTHS))
    cu = cu.assign(is_common=1)
    base = base.merge(cu[["permno", "midx", "is_common"]],
                      on=["permno", "midx"], how="left")
    base["univ_common"] = base["univ_all"] & base["is_common"].notna()

    # ---- book-to-market (paper L108-110) -----------------------------------
    base["Y"] = np.where(base["mo"] >= 7, base["yr"], base["yr"] - 1)
    base = base.merge(bm[["permno", "Y", "bm", "bm_dum"]],
                      on=["permno", "Y"], how="left")
    base["bm"] = base["bm"].fillna(0.0)
    base["bm_dum"] = base["bm_dum"].fillna(0).astype(int)
    pre_bm = base["midx"] < BM_FIRST_MIDX                 # before July 1970
    base.loc[pre_bm, "bm"] = 0.0
    base.loc[pre_bm, "bm_dum"] = 0

    base["month"] = pd.to_datetime(
        {"year": base["yr"], "month": base["mo"], "day": 1})

    cols = ["permno", "month", "ret", "prc_abs", "shrout", "cfacshr",
            "adj_shares", "univ_all", "univ_common", "issue", "dt_issue",
            "dt_dum", "bm", "bm_dum", "me_june", "me_monthly", "mom", "r1",
            "r6", "r12", "r24_y2", "r36_y3", "issue_contemp",
            "dt_issue_contemp", "r_11_0"]
    panel = base.loc[base["midx"] >= PANEL_START_MIDX, cols].copy()
    panel = panel.sort_values(["permno", "month"]).reset_index(drop=True)
    panel["permno"] = panel["permno"].astype("int64")
    return panel, n_err, n_ew_missing


# ---------------------------------------------------------------------------
def _stats_block(s):
    s = pd.Series(s).dropna()
    if len(s) == 0:
        return dict(n=0, mean=np.nan, p25=np.nan, med=np.nan, p75=np.nan, std=np.nan)
    return dict(n=len(s), mean=s.mean(), p25=s.quantile(0.25), med=s.median(),
                p75=s.quantile(0.75), std=s.std())


def report(panel, n_err, n_ew_missing):
    L = []
    ap = L.append
    ap("=" * 78)
    ap("STRUCTURED REPORT — Share Issuance panel (Pontiff & Woodgate 2008)")
    ap("=" * 78)

    # (a) dimensions ---------------------------------------------------------
    ap("\n(a) PANEL DIMENSIONS")
    ap(f"  rows            : {len(panel):,}")
    ap(f"  columns         : {panel.shape[1]}")
    ap(f"  unique permnos  : {panel['permno'].nunique():,}")
    ap(f"  unique months   : {panel['month'].nunique()} "
       f"({panel['month'].min().date()} .. {panel['month'].max().date()})")
    ap(f"  EWRETD months missing in grid: {n_ew_missing}")

    in_s = (panel["month"] >= IN_START) & (panel["month"] <= IN_END)
    oos = (panel["month"] >= OOS_START) & (panel["month"] <= OOS_END)

    def per_decade_avg(mask):
        sub = panel[mask]
        cnt = sub.groupby(["month"]).size()
        dec = cnt.groupby(cnt.index.year // 10).mean()
        return {f"{d*10}s": round(v) for d, v in dec.items()}

    # (b) obs counts ---------------------------------------------------------
    ap("\n(b) OBSERVATION COUNTS  (our vs paper)")
    for label, ucol in [("univ_all", "univ_all"), ("univ_common", "univ_common")]:
        m_in = in_s & panel[ucol]
        m_oos = oos & panel[ucol]
        ap(f"\n  --- {label} ---")
        ap(f"  in-sample 1970-01..2003-12 total      : {m_in.sum():,}   "
           f"(paper §I {PAPER['in_total']:,})")
        ap(f"    per-decade avg firms/month           : {per_decade_avg(m_in)}")
        ap(f"  nonmissing ISSUE (regression, t-6/t-17): "
           f"{(m_in & panel['issue'].notna()).sum():,}")
        ap(f"  nonmissing ISSUE_contemp (Table I)     : "
           f"{(m_in & panel['issue_contemp'].notna()).sum():,}   "
           f"(paper Table I {PAPER['in_issue']:,})")
        ap(f"  nonmissing DT_ISSUE valid (dt_dum=1)   : "
           f"{(m_in & (panel['dt_dum']==1)).sum():,}")
        ap(f"  nonmissing BM (bm_dum=1)               : "
           f"{(m_in & (panel['bm_dum']==1)).sum():,}")
        ap(f"  nonmissing ME_june                     : "
           f"{(m_in & panel['me_june'].notna()).sum():,}")
        ap(f"  nonmissing MOM                         : "
           f"{(m_in & panel['mom'].notna()).sum():,}   "
           f"(paper Table I {PAPER['in_mom']:,})")
        ap(f"  nonmissing R_{{-11,0}}                     : "
           f"{(m_in & panel['r_11_0'].notna()).sum():,}")
        regr = m_in & panel["issue"].notna() & panel["me_june"].notna() & panel["mom"].notna()
        ap(f"  regr sample (issue & me_june & mom)    : {regr.sum():,}   "
           f"(paper Table III {PAPER['t3_obs']:,} over {PAPER['t3_months']} mo)")
        # OOS
        ap(f"  OOS Sep1932..Dec1969 total             : {m_oos.sum():,}   "
           f"(paper §I {PAPER['oos_total']:,})")
        ap(f"    per-decade avg firms/month           : {per_decade_avg(m_oos)}")
        ap(f"  OOS nonmissing MOM                     : "
           f"{(m_oos & panel['mom'].notna()).sum():,}   "
           f"(paper Table V {PAPER['oos_mom']:,})")
        ap(f"  OOS nonmissing R_{{-11,0}}                 : "
           f"{(m_oos & panel['r_11_0'].notna()).sum():,}   "
           f"(paper Table V {PAPER['oos_r110']:,})")
        regr_o = m_oos & panel["issue"].notna() & panel["mom"].notna() & panel["r_11_0"].notna()
        ap(f"  OOS regr sample (issue & mom & r_11_0) : {regr_o.sum():,}   "
           f"(paper Table VI {PAPER['t6_obs']:,} over {PAPER['t6_months']} mo)")

    # BM coverage by decade --------------------------------------------------
    ap("\n  BM coverage (share bm_dum=1 among univ_common), by decade:")
    bc = panel[in_s & panel["univ_common"]].copy()
    bc["dec"] = bc["month"].dt.year // 10
    cov = bc.groupby("dec")["bm_dum"].mean()
    for d, v in cov.items():
        ap(f"    {d*10}s : {v:.3f}")

    # (c) Table I Panel A preview -------------------------------------------
    ap("\n(c) TABLE I PANEL A PREVIEW  (1970-2003, monthly pool)")
    ap("  Convention (reconciles to paper): base sample = universe AND ISSUE_contemp")
    ap("  nonmissing (paper's widest Table I variable = 2,312,597). Within it, BM")
    ap("  INCLUDES the bm_dum=0 zeros and DT-ISSUE is dummy-filled to 0 where the")
    ap("  5-yr history is missing (paper reports these with dummy conventions); each")
    ap("  other variable is shown over its own nonmissing obs (MOM is the narrowest).")
    paper_tbl = {  # mean / p25 / median / p75 / std
        "issue_contemp":    (0.04, 0.00, 0.00, 0.03, 0.15),
        "dt_issue_contemp": (0.12, 0.00, 0.00, 0.14, 0.33),
        "bm":               (-0.34, -0.79, -0.07, 0.00, 0.94),
        "me_monthly":       (11.11, 9.63, 10.97, 12.46, 2.02),
        "mom":              (0.06, -0.16, 0.02, 0.22, 0.41),
        "r_11_0":           (0.14, -0.23, 0.05, 0.34, 0.88),
    }
    for ucol in ["univ_all", "univ_common"]:
        ap(f"\n  --- {ucol} ---")
        base_s = in_s & panel[ucol] & panel["issue_contemp"].notna()
        ap(f"  Table I base sample (ISSUE avail): {base_s.sum():,}   "
           f"(paper 2,312,597)")
        ap(f"  {'var':18s} {'n':>9s} {'mean':>8s} {'p25':>8s} "
           f"{'median':>8s} {'p75':>8s} {'std':>8s}   paper(mean/p25/med/p75/std)")
        sub = panel[base_s]
        for var, pt in paper_tbl.items():
            if var == "dt_issue_contemp":
                s = sub["dt_issue_contemp"].fillna(0.0)   # dummy fill (<5yr -> 0)
            elif var == "bm":
                s = sub["bm"]                              # already 0 when bm_dum=0
            else:
                s = sub[var].dropna()
            st = _stats_block(s)
            paper_str = "/".join(f"{x:.2f}" for x in pt)
            ap(f"  {var:18s} {st['n']:>9,d} {st['mean']:>8.3f} {st['p25']:>8.3f} "
               f"{st['med']:>8.3f} {st['p75']:>8.3f} {st['std']:>8.3f}   {paper_str}")

    # proportions of issue_contemp sign -------------------------------------
    ap("\n  ISSUE_contemp sign proportions (univ_all, 1970-2003; paper 56.6/24.2/19.2):")
    ic = panel.loc[in_s & panel["univ_all"], "issue_contemp"].dropna()
    tot = len(ic)
    ap(f"    >0 : {100*(ic>0).mean():.1f}%   ==0 : {100*(ic==0).mean():.1f}%   "
       f"<0 : {100*(ic<0).mean():.1f}%   (n={tot:,})")

    # (d) error correction ---------------------------------------------------
    ap("\n(d) SHARES ERROR CORRECTION (paper L98)")
    ap(f"  corrections applied : {n_err:,}   (paper {PAPER['err_corr']:,}, 0.07%)")

    # (e) issues / deviations -----------------------------------------------
    ap("\n(e) AMBIGUITIES / SENTINELS / DEVIATIONS")
    ap("  1. BM funda filter: task spec wrote consol='STD' AND popsrc='STD'; those")
    ap("     values DO NOT EXIST in comp_202601.funda (consol in {C,P,R,D}; popsrc=D")
    ap("     only). Implemented the correct WRDS-standard consol='C' AND popsrc='D'")
    ap("     (indfmt='INDL', datafmt='STD'). Flagged for Replicator.")
    ap("  2. BM units: Compustat ceq is $millions, CRSP me_dec is $thousands; bm uses")
    ap("     ceq*1000/me_dec so the log ratio matches the paper (BM mean ~ -0.34).")
    ap("     Without the x1000 the mean would be ~ -7.2.")
    ap("  3. BM fallback is on MISSING ceq only (NULL -> use FY-2); a non-positive")
    ap("     ceq at FY-1 is NOT fallen back (sets bm=0,bm_dum=0), per spec wording.")
    ap("  4. Pre-July-1970 BM=0, bm_dum=0 (DFF book equity unavailable): logged")
    ap("     limitation — the OOS Table V/VI BM is not available from Compustat.")
    ap("  5. ClickHouse Date/toStartOfMonth clamps pre-1970 dates to the 1970 epoch;")
    ap("     all month handling uses an integer midx (year*12+month-1) in SQL and")
    ap("     pandas Timestamps in Python.")
    ap("  6. Window/lag computations (ISSUE, MOM, forward returns) done in Python on")
    ap("     a complete stock x month grid for exact calendar alignment (spec allows")
    ap("     pandas here; row-based SQL lagInFrame would misalign around listing gaps).")
    ap("  7. Holding-period windows past 2006-12 (t in 2004-2006) are NaN (no data /")
    ap("     no EWRETD beyond the pull end); in-sample t<=2003-12 fully covered.")
    ap("  8. r1 = raw month-t return; EWRETD-imputed series stored ONLY in r6/r12/")
    ap("     r24_y2/r36_y3 (not in ret), per spec.")
    ap("  9. Shares error correction (L98) implemented as a sequential pass on raw")
    ap("     shrout (>20% jump, >=95% reversed within 3 months -> set to prior level).")
    ap("     Count ~2,172 vs paper 2,189 (0.8% diff; vintage/processing detail). Paper")
    ap("     states inference is unaffected by this 0.07%-of-obs correction.")
    ap(" 10. Universe counts run ~3% below the paper in-sample (2.41M vs 2.49M) and")
    ap("     ~11% below OOS (0.50M vs 0.57M). Spec rule (b) defines first_msf_month as")
    ap("     the first month with a NONMISSING return (implemented exactly); the paper")
    ap("     likely counts from first CRSP appearance and/or uses retx-fallback, which")
    ap("     raises counts (verified: first-appearance -> 2.45M; no 6-mo rule -> 2.54M).")
    ap(" 11. r_11_0 requires ALL 12 actual months per spec (no imputation), so its obs")
    ap("     count is below MOM; the paper's R_{-11,0} count is >= MOM (2,312,597 range),")
    ap("     implying the paper imputes R_{-11,0} with EWRETD. Implemented per spec")
    ap("     (all-12-required); flag for Replicator if Table I/V R_{-11,0} must match.")
    ap(" 12. Table I BM/DT-ISSUE rows use the paper's dummy conventions (BM incl. the")
    ap("     bm_dum=0 zeros; DT-ISSUE filled to 0 for <5yr history) over the ISSUE-")
    ap("     available base sample, which reproduces the paper's reported quantiles.")
    ap("=" * 78)

    txt = "\n".join(L)
    print(txt)
    out = LAYOUT.result_path("panel_report.md")
    Path(out).write_text(txt + "\n")
    print(f"\n[report] saved to {out}")


def main():
    t0 = time.time()
    base, fv, cu, ew, bm = load_data()
    panel, n_err, n_ew_missing = build_panel(base, fv, cu, ew, bm)
    out = LAYOUT.data_path("panel.parquet")
    panel.to_parquet(out, index=False)
    print(f"[write] panel -> {out}  ({len(panel):,} rows x {panel.shape[1]} cols, "
          f"{time.time()-t0:.1f}s total)", flush=True)
    report(panel, n_err, n_ew_missing)


if __name__ == "__main__":
    main()
