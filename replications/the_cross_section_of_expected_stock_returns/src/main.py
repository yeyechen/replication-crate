"""
Replication of Fama & French (1992) "The Cross-Section of Expected Stock Returns"
=================================================================================
Stage: build the analysis-ready data pipeline -> data/panel.parquet.

Panel grain: one row per (permno, return_month), July 1963 - December 1990
(330 months), for stocks meeting the paper's per-firm-year data requirements
in formation year t (t = 1963..1990):
  1. valid CRSP price (abs(prc) > 0) at December t-1 AND June t;
  2. >= 24 valid monthly returns in the 60 months July t-5 .. June t;
  3. Compustat (funda, FF filter) data for the latest fiscal year ending in
     calendar year t-1: A = at > 0, BE available, E available (ib present),
     linked via ccmxpf_linktable (LC/LU, P/C, usedflag=1, PIT at June t);
  4. BE > 0 (negative-BE firms excluded from the tests, paper L1350).

Universe: CRSP common shares (shrcd 10/11) on NYSE/AMEX/NASDAQ (exchcd 1/2/3),
point-in-time as of the June t formation date (dsenames validity windows),
excluding financial firms (SIC 6000-6999, binding Assumption 4). NO minimum
price filter (binding Assumption 1).

Variables (per firm-year, formation June t):
  ME_jun / ME_dec (dollars), lnME = ln(ME_jun/1e6),
  bm = BE/ME_dec, ame = A/ME_dec, abe = A/BE, ep = E/ME_dec
  (A/BE/E converted from Compustat $ millions to $ in compustat_funda.sql so
  all ratios are unit-consistent with CRSP dollar ME),
  ln_bm / ln_ame / ln_abe, ep_pos / ep_dummy (Assumption 11),
  pre_beta = Dimson sum-beta (slopes on current + 1-lagged msi.vwretd,
             24-60 monthly returns July t-5 .. June t; Assumption 7).

Sorts (assignments stored per firm-year):
  A. size_decile 1..10   : NYSE ME_jun decile breakpoints over ALL NYSE common
                           stocks (shrcd 10/11, exchcd 1, PIT June t — not
                           restricted to data-qualified / Compustat-linked).
  B. beta_group 1..10    : pre_beta deciles WITHIN each size decile,
                           breakpoints over NYSE data-qualified stocks.
  C. size12 / beta12     : 12 one-dimensional portfolios (1A/1B/2-9/10A/10B);
                           NYSE breakpoints (ME over all NYSE common; beta
                           over NYSE data-qualified).
  D. beme12 / ep13       : formed at end of year t-1 on bm (12 portfolios) and
                           ep (13: portfolio 0 = E <= 0); breakpoints over ALL
                           data-qualified stocks (all three exchanges).
  E. size_beme "s_b"     : 10x10 size x BE/ME; within each size decile, 10
                           BE/ME groups with breakpoints over ALL
                           data-qualified stocks in the decile (Assumption 8).

Post-ranking betas: equal-weighted monthly returns of the 100 size x pre-beta
portfolios, July 1963 - December 1990 (330 months), then Dimson sum-beta of
each portfolio series on current + 1-lagged msi.vwretd. Each stock gets the
post_beta of the size x pre-beta portfolio it is in as of June t.

Returns: msf.ret (decimal, with dividends) with delisting adjustment per
binding Assumption 5 (see src/sql/monthly_returns_delist.sql).

Outputs:
  data/panel.parquet            - the analysis-ready panel
  data/portfolio_returns.parquet- monthly EW returns of the 100 size x
                                  pre-beta portfolios (computed intermediate,
                                  reused for post-ranking betas / Table I)

Implementation: all filtering / aggregation / PIT joins run in ClickHouse
(src/sql/*.sql, read at runtime). Python does sorts, beta regressions
(vectorized grouped OLS with closed-form normal equations) and assembly.

CRSP gotchas handled: ret sentinels (-44/-55/-66/-77/-88/-99 are < -1.0)
filtered via ret > -1.0; prc signed -> abs(); shrout in 1000s -> ME in
dollars = abs(prc)*shrout*1000; month keys via toDate32 (ClickHouse `Date`
clamps pre-1970 dates to the epoch).

Usage:
    uv run python src/main.py
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

from utils.env import get_clickhouse_config
from utils.paths import paper_layout

# ────────────────────────────────────────────────────────────────────────────
# Layout & configuration
# ────────────────────────────────────────────────────────────────────────────
SLUG = "the_cross_section_of_expected_stock_returns"
LAYOUT = paper_layout(SLUG)
# NOTE: do NOT call LAYOUT.ensure() at import time — importing this module
# from other scripts (table_*.py, evaluate.py, plots.py) must never create
# directories (audit-2 [m1]: import-time ensure() recreated stray layout
# skeletons). The layout is ensured in main() below.
SQL_DIR = LAYOUT.src_path("sql")
_CFG = get_clickhouse_config()

# preprocessing_rules.json stores paper QUOTES, not a numeric parameter map,
# so the numeric constants are pinned here with their rule_ids.
FIRST_T = 1963            # first formation year          [sample_period]
LAST_T = 1990             # last formation year           [sample_return_period]
RETURN_END_YM = 199012    # last return month: post-ranking window is July
                          # 1963 - December 1990 = 330 months (L171), so the
                          # final formation year (1990) contributes only
                          # July-December 1990   [sample_return_period]
MIN_RET_MONTHS = 24       # min valid months for pre-beta [sample_preranking_return_requirement]
PRE_WINDOW_MONTHS = 60    # 5-year pre-ranking window     [var_preranking_beta_estimation]
DECILE_PCTS = np.arange(10, 100, 10)          # decile breakpoints (10..90)
LABELS_12 = ["1A", "1B", "2", "3", "4", "5", "6", "7", "8", "9", "10A", "10B"]

# sanity: the rules file must exist (single source of truth for methodology)
RULES_PATH = LAYOUT.preparations_path("preprocessing_rules.json")
RULES = json.loads(RULES_PATH.read_text()) if RULES_PATH.exists() else []


# ────────────────────────────────────────────────────────────────────────────
# ClickHouse connection
# ────────────────────────────────────────────────────────────────────────────
def _client() -> Client:
    return Client(
        host=_CFG["host"], port=int(_CFG["port"]),
        user=_CFG["user"], password=_CFG["password"],
        settings={"max_execution_time": 900},
    )


def q(sql: str) -> pd.DataFrame:
    """Execute a SQL SELECT and return a DataFrame."""
    c = _client()
    data, cols = c.execute(sql.rstrip().rstrip(";"), with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    """Execute a saved SQL file and return a DataFrame."""
    sql = (SQL_DIR / name).read_text()
    t0 = time.time()
    df = q(sql)
    print(f"  [sql] {name}: {len(df):,} rows in {time.time() - t0:.1f}s")
    return df


# ────────────────────────────────────────────────────────────────────────────
# Date helpers (months are integer YYYYMM keys; dates pre-1970 so no datetime
# arithmetic inside ClickHouse — see SQL headers)
# ────────────────────────────────────────────────────────────────────────────
def ym_prev(ym: np.ndarray) -> np.ndarray:
    """Previous calendar month key, vectorized (196301 -> 196212)."""
    y, m = np.divmod(np.asarray(ym, dtype=np.int64), 100)
    return np.where(m > 1, ym - 1, (y - 1) * 100 + 12)


def ym_to_month_end(ym: np.ndarray) -> pd.DatetimeIndex:
    """YYYYMM keys -> month-end Timestamps."""
    ym = np.asarray(ym, dtype=np.int64)
    y, m = np.divmod(ym, 100)
    return (
        pd.to_datetime({"year": y, "month": m, "day": 1})
        + pd.offsets.MonthEnd(0)
    )


def fyr_months(fyr: int) -> list[int]:
    """The return-month keys July t .. June t+1 for formation year t,
    truncated at RETURN_END_YM (December 1990) — the paper's post-ranking
    window ends December 1990 (330 months), so formation year 1990
    contributes only July-December 1990."""
    months = [fyr * 100 + mo for mo in range(7, 13)] + [
        (fyr + 1) * 100 + mo for mo in range(1, 7)
    ]
    return [m for m in months if m <= RETURN_END_YM]


# ────────────────────────────────────────────────────────────────────────────
# Grouped Dimson sum-beta (closed-form normal equations, vectorized)
#
# Regression of y on [1, x0, x1] per group; beta = slope(x0) + slope(x1).
# Each group supplies n, sum(y), sum(x0*y), sum(x1*y) and the 3x3 Gram matrix
# of its own (x0, x1) rows (groups can miss different months).
# ────────────────────────────────────────────────────────────────────────────
def grouped_dimson_beta(
    df: pd.DataFrame,
    group_col: str,
    min_obs: int,
) -> pd.DataFrame:
    """Return DataFrame[group_col, beta, n_obs] with Dimson sum-betas.

    `df` must have columns [group_col, x0, x1, y] and contain only complete
    rows (no NaNs in x0/x1/y).
    """
    g = df.groupby(group_col)
    n = g.size()
    keep = n[n >= min_obs].index
    sub = df[df[group_col].isin(keep)]
    g = sub.groupby(group_col)
    n = g.size().to_numpy(dtype=np.float64)
    sy = g["y"].sum().to_numpy(dtype=np.float64)
    sx0y = (sub["x0"] * sub["y"]).groupby(sub[group_col]).sum().to_numpy(dtype=np.float64)
    sx1y = (sub["x1"] * sub["y"]).groupby(sub[group_col]).sum().to_numpy(dtype=np.float64)
    sx0 = g["x0"].sum().to_numpy(dtype=np.float64)
    sx1 = g["x1"].sum().to_numpy(dtype=np.float64)
    sx00 = (sub["x0"] * sub["x0"]).groupby(sub[group_col]).sum().to_numpy(dtype=np.float64)
    sx01 = (sub["x0"] * sub["x1"]).groupby(sub[group_col]).sum().to_numpy(dtype=np.float64)
    sx11 = (sub["x1"] * sub["x1"]).groupby(sub[group_col]).sum().to_numpy(dtype=np.float64)

    k = len(n)
    A = np.zeros((k, 3, 3))
    A[:, 0, 0] = n
    A[:, 0, 1] = A[:, 1, 0] = sx0
    A[:, 0, 2] = A[:, 2, 0] = sx1
    A[:, 1, 1] = sx00
    A[:, 1, 2] = A[:, 2, 1] = sx01
    A[:, 2, 2] = sx11
    b = np.column_stack([sy, sx0y, sx1y])
    try:
        coef = np.linalg.solve(A, b[:, :, None])[:, :, 0]
    except np.linalg.LinAlgError:  # singular Gram for some group -> lstsq
        coef = np.array([np.linalg.lstsq(Ai, bi, rcond=None)[0] for Ai, bi in zip(A, b)])
    beta = coef[:, 1] + coef[:, 2]  # sum of the two slopes (Dimson 1979)
    idx = g.size().index
    return pd.DataFrame({group_col: idx, "beta": beta, "n_obs": n.astype(int)})


# ────────────────────────────────────────────────────────────────────────────
# Sort primitives
# ────────────────────────────────────────────────────────────────────────────
def decile_breakpoints(vals: np.ndarray) -> np.ndarray:
    """9 decile breakpoints (10th..90th percentiles, linear interpolation)."""
    return np.percentile(vals, DECILE_PCTS)


def split12_breakpoints(vals: np.ndarray, dec_bp: np.ndarray) -> np.ndarray:
    """11 breakpoints for the 12-portfolio layout: median split of the bottom
    and top NYSE deciles around the 9 decile breakpoints.
    Bins: 1A (<=lo), 1B, 2..9, 10A, 10B (>hi)."""
    lo = np.median(vals[vals <= dec_bp[0]])
    hi = np.median(vals[vals >= dec_bp[8]])
    return np.concatenate([[lo], dec_bp, [hi]])


def assign_bins(x: np.ndarray, bps: np.ndarray) -> np.ndarray:
    """Right-closed bins: value exactly at a breakpoint falls in the lower
    bin (searchsorted side='left'). Returns 1..len(bps)+1."""
    return np.searchsorted(bps, x, side="left") + 1


# ────────────────────────────────────────────────────────────────────────────
# Pipeline
# ────────────────────────────────────────────────────────────────────────────
def load_data() -> dict:
    print("Loading data from ClickHouse (src/sql/*.sql):")
    return {
        "mkt": q_file("market_index_monthly.sql"),
        "rets": q_file("monthly_returns_delist.sql"),
        "me": q_file("me_formation.sql"),
        "names": q_file("universe_pit_june.sql"),
        "comp": q_file("compustat_funda.sql"),
        "link": q_file("ccm_link_pit.sql"),
    }


def build_universe(names: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Data-qualified universe (shrcd 10/11, exchcd 1/2/3, non-financial SIC,
    PIT at June t) and the NYSE breakpoint universe (shrcd 10/11, exchcd 1 —
    ALL NYSE common stocks on CRSP, per sort-A spec; financials included,
    see Issues)."""
    names = names.copy()
    for col in ("permno", "shrcd", "exchcd", "siccd", "fyr"):
        names[col] = pd.to_numeric(names[col], errors="coerce")
    names = names.dropna(subset=["permno", "fyr"])
    names["permno"] = names["permno"].astype(np.int64)
    names["fyr"] = names["fyr"].astype(np.int32)

    common = names["shrcd"].isin([10, 11])
    exch = names["exchcd"].isin([1, 2, 3])
    fin = names["siccd"].between(6000, 6999)

    univ = names[common & exch & ~fin][["fyr", "permno", "exchcd"]].copy()
    univ["is_nyse"] = (univ["exchcd"] == 1).astype(bool)
    univ = univ[["fyr", "permno", "is_nyse"]]

    nyse_bp = names[common & (names["exchcd"] == 1)][["fyr", "permno"]].copy()
    nyse_bp["nyse_bp"] = True
    return univ, nyse_bp


def build_firm_years(data: dict, univ: pd.DataFrame, nyse_bp: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Apply the per-firm-year data requirements and attach accounting data.
    Returns the qualified firm-year table and a requirement-count ledger."""
    me = data["me"].copy()
    me["permno"] = pd.to_numeric(me["permno"], errors="coerce").astype(np.int64)
    me["ym"] = pd.to_numeric(me["ym"], errors="coerce").astype(np.int64)
    me["me"] = pd.to_numeric(me["me"], errors="coerce")
    me_dec = me[me["ym"] % 100 == 12].rename(columns={"me": "ME_dec"})[["permno", "ym", "ME_dec"]]
    me_jun = me[me["ym"] % 100 == 6].rename(columns={"me": "ME_jun"})[["permno", "ym", "ME_jun"]]
    me_dec["fyr"] = (me_dec["ym"] // 100 + 1).astype(np.int32)
    me_jun["fyr"] = (me_jun["ym"] // 100).astype(np.int32)

    # --- requirement 2: >= 24 valid monthly returns in July t-5 .. June t ---
    rets = data["rets"].copy()
    rets["permno"] = pd.to_numeric(rets["permno"], errors="coerce").astype(np.int64)
    rets["ym"] = pd.to_numeric(rets["ym"], errors="coerce").astype(np.int64)
    rets["ret"] = pd.to_numeric(rets["ret"], errors="coerce")
    counts = []
    for t in range(FIRST_T, LAST_T + 1):
        lo, hi = (t - 5) * 100 + 7, t * 100 + 6
        w = rets[(rets["ym"] >= lo) & (rets["ym"] <= hi)]
        c = w.loc[w["ret"].notna()].groupby("permno").size().rename("n_ret")
        counts.append(pd.DataFrame({"fyr": np.int32(t), "permno": c.index, "n_ret": c.to_numpy()}))
    nret = pd.concat(counts, ignore_index=True)

    # --- requirement 3: Compustat link + accounting ---
    link = data["link"].copy()
    link["permno"] = pd.to_numeric(link["permno"], errors="coerce").astype(np.int64)
    link["fyr"] = pd.to_numeric(link["fyr"], errors="coerce").astype(np.int32)
    link["gvkey"] = link["gvkey"].astype(str)

    comp = data["comp"].copy()
    for col in ("A", "BE", "E"):
        comp[col] = pd.to_numeric(comp[col], errors="coerce")
    comp["fyear"] = pd.to_numeric(comp["fyear"], errors="coerce").astype(np.int32)
    comp["gvkey"] = comp["gvkey"].astype(str)
    comp = comp[["gvkey", "fyear", "A", "BE", "E"]]

    ledger: dict[str, int] = {}
    fy = univ.copy()
    ledger["universe_firm_years"] = len(fy)

    fy = fy.merge(me_jun[["fyr", "permno", "ME_jun"]], on=["fyr", "permno"], how="left")
    fy = fy.merge(me_dec[["fyr", "permno", "ME_dec"]], on=["fyr", "permno"], how="left")
    ledger["drop_missing_ME_jun"] = int((fy["ME_jun"].isna() | (fy["ME_jun"] <= 0)).sum())
    ledger["drop_missing_ME_dec"] = int((fy["ME_dec"].isna() | (fy["ME_dec"] <= 0)).sum())
    fy = fy[(fy["ME_jun"] > 0) & (fy["ME_dec"] > 0)]

    fy = fy.merge(nret, on=["fyr", "permno"], how="left")
    ledger["drop_lt_24_returns"] = int((fy["n_ret"].isna() | (fy["n_ret"] < MIN_RET_MONTHS)).sum())
    fy = fy[fy["n_ret"] >= MIN_RET_MONTHS]

    fy = fy.merge(link[["fyr", "permno", "gvkey"]], on=["fyr", "permno"], how="left")
    ledger["drop_no_compustat_link"] = int(fy["gvkey"].isna().sum())
    fy = fy.dropna(subset=["gvkey"])

    comp_r = comp.rename(columns={"fyear": "cfyear"})
    comp_r["fyr"] = (comp_r["cfyear"] + 1).astype(np.int32)  # fyear = t-1
    fy = fy.merge(comp_r[["fyr", "gvkey", "A", "BE", "E"]], on=["fyr", "gvkey"], how="left")
    no_rec = fy[["A", "BE", "E"]].isna().all(axis=1)
    ledger["drop_no_comp_year"] = int(no_rec.sum())
    fy = fy[~no_rec]

    ledger["drop_A_missing_or_nonpositive"] = int((fy["A"].isna() | (fy["A"] <= 0)).sum())
    ledger["drop_BE_unavailable"] = int(fy["BE"].isna().sum())
    ledger["drop_E_missing"] = int(fy["E"].isna().sum())
    fy = fy[(fy["A"] > 0) & fy["BE"].notna() & fy["E"].notna()]

    # requirement 4: BE > 0 (negative/zero book equity excluded, paper L1350)
    ledger["drop_BE_nonpositive"] = int((fy["BE"] <= 0).sum())
    fy = fy[fy["BE"] > 0]

    ledger["qualified_firm_years"] = len(fy)
    return fy, ledger


def add_variables(fy: pd.DataFrame) -> pd.DataFrame:
    fy = fy.copy()
    fy["lnME"] = np.log(fy["ME_jun"] / 1e6)          # ME in $ millions
    fy["bm"] = fy["BE"] / fy["ME_dec"]
    fy["ame"] = fy["A"] / fy["ME_dec"]
    fy["abe"] = fy["A"] / fy["BE"]
    fy["ep"] = fy["E"] / fy["ME_dec"]
    fy["ln_bm"] = np.log(fy["bm"])                    # bm > 0 (BE > 0, ME_dec > 0)
    fy["ln_ame"] = np.log(fy["ame"])                  # A > 0, ME_dec > 0
    fy["ln_abe"] = np.log(fy["abe"])                  # A > 0, BE > 0
    pos = fy["E"] > 0
    fy["ep_pos"] = np.where(pos, fy["ep"], 0.0)
    fy["ep_dummy"] = (~pos).astype(np.int8)           # 1 when E <= 0 (Assumption 11)
    return fy


def add_pre_beta(fy: pd.DataFrame, data: dict) -> pd.DataFrame:
    """Pre-ranking Dimson sum-betas, one regression per (fyr, permno) over the
    24-60 valid monthly returns in July t-5 .. June t."""
    mkt = data["mkt"].copy()
    mkt["ym"] = pd.to_numeric(mkt["ym"], errors="coerce").astype(np.int64)
    mkt["vwretd"] = pd.to_numeric(mkt["vwretd"], errors="coerce")
    mkt = mkt.dropna(subset=["vwretd"]).sort_values("ym")
    vmap = dict(zip(mkt["ym"], mkt["vwretd"]))
    mkt["vwretd_lag"] = mkt["ym"].to_numpy()
    mkt["vwretd_lag"] = [vmap.get(p, np.nan) for p in ym_prev(mkt["ym"].to_numpy())]
    mkt = mkt.dropna(subset=["vwretd_lag"])[["ym", "vwretd", "vwretd_lag"]]

    rets = data["rets"].dropna(subset=["ret"])[["permno", "ym", "ret"]]
    out = []
    for t in range(FIRST_T, LAST_T + 1):
        lo, hi = (t - 5) * 100 + 7, t * 100 + 6
        w = rets[(rets["ym"] >= lo) & (rets["ym"] <= hi)].merge(mkt, on="ym", how="inner")
        if w.empty:
            continue
        b = grouped_dimson_beta(
            w.rename(columns={"vwretd": "x0", "vwretd_lag": "x1", "ret": "y"}),
            group_col="permno", min_obs=MIN_RET_MONTHS,
        )
        b["fyr"] = np.int32(t)
        out.append(b.rename(columns={"beta": "pre_beta"}))
    pre = pd.concat(out, ignore_index=True)[["fyr", "permno", "pre_beta", "n_obs"]]
    return fy.merge(pre, on=["fyr", "permno"], how="left")


def run_sorts(fy: pd.DataFrame, nyse_bp: pd.DataFrame, me_jun_all: pd.DataFrame) -> pd.DataFrame:
    """All five sorts (A-E). Operates per formation year.

    `me_jun_all` = June ME for ALL stocks with an msf record (from
    me_formation.sql); merged with the NYSE breakpoint universe so the size
    breakpoints cover ALL NYSE common stocks on CRSP — NOT restricted to the
    data-qualified subset (paper L151, task spec Sort A)."""
    fy = fy.copy()
    fy["size_decile"] = pd.Series(pd.NA, index=fy.index, dtype="Int32")
    fy["beta_group"] = pd.Series(pd.NA, index=fy.index, dtype="Int32")
    fy["size12"] = pd.NA
    fy["beta12"] = pd.NA
    fy["beme12"] = pd.NA
    fy["ep13"] = pd.NA
    fy["size_beme"] = pd.NA

    nyse_bp_me = nyse_bp.merge(me_jun_all, on=["fyr", "permno"], how="inner")
    nyse_bp_me = nyse_bp_me[nyse_bp_me["ME_jun"] > 0]

    for t, g in fy.groupby("fyr"):
        idx = g.index
        nyse_mask = g["is_nyse"].to_numpy(dtype=bool)
        me_jun = g["ME_jun"].to_numpy(dtype=np.float64)
        beta = g["pre_beta"].to_numpy(dtype=np.float64)
        bm = g["bm"].to_numpy(dtype=np.float64)
        ep = g["ep"].to_numpy(dtype=np.float64)
        ep_pos_mask = g["ep_dummy"].to_numpy() == 0

        # --- A. size deciles: NYSE breakpoints over ALL NYSE common stocks ---
        bp_me_nyse = nyse_bp_me.loc[nyse_bp_me["fyr"] == t, "ME_jun"].to_numpy()
        dec_me = decile_breakpoints(bp_me_nyse)
        size_dec = assign_bins(me_jun, dec_me)
        fy.loc[idx, "size_decile"] = pd.array(size_dec, dtype="Int32")

        # --- C. size12: 12 portfolios on ME, NYSE breakpoints ---
        bp12_me = split12_breakpoints(bp_me_nyse, dec_me)
        fy.loc[idx, "size12"] = [LABELS_12[i] for i in assign_bins(me_jun, bp12_me) - 1]

        # --- C. beta12: 12 portfolios on pre_beta, NYSE data-qualified breakpoints ---
        beta_nyse = beta[nyse_mask & np.isfinite(beta)]
        dec_beta = decile_breakpoints(beta_nyse)
        bp12_beta = split12_breakpoints(beta_nyse, dec_beta)
        fy.loc[idx, "beta12"] = [LABELS_12[i] for i in assign_bins(beta, bp12_beta) - 1]

        # --- B. beta deciles within each size decile (NYSE data-qualified bps) ---
        bg = np.full(len(g), np.nan)
        for d in range(1, 11):
            in_d = size_dec == d
            bp_src = beta[nyse_mask & in_d & np.isfinite(beta)]
            bp_d = decile_breakpoints(bp_src)
            bg[in_d] = assign_bins(beta[in_d], bp_d)
        fy.loc[idx, "beta_group"] = pd.array(bg, dtype="Int32")

        # --- D. beme12 / ep13: breakpoints over ALL data-qualified stocks ---
        dec_bm = decile_breakpoints(bm[np.isfinite(bm)])
        bp12_bm = split12_breakpoints(bm[np.isfinite(bm)], dec_bm)
        fy.loc[idx, "beme12"] = [LABELS_12[i] for i in assign_bins(bm, bp12_bm) - 1]

        ep13 = np.full(len(g), "0", dtype=object)
        ep_pos = ep[ep_pos_mask]
        dec_ep = decile_breakpoints(ep_pos[np.isfinite(ep_pos)])
        bp12_ep = split12_breakpoints(ep_pos[np.isfinite(ep_pos)], dec_ep)
        bins_ep = assign_bins(ep, bp12_ep)
        ep13[ep_pos_mask] = [LABELS_12[i - 1] for i in bins_ep[ep_pos_mask]]
        fy.loc[idx, "ep13"] = ep13

        # --- E. size x BE/ME 10x10: within-decile bps over ALL data-qualified ---
        sb = np.full(len(g), None, dtype=object)
        for d in range(1, 11):
            in_d = size_dec == d
            bp_b = decile_breakpoints(bm[in_d & np.isfinite(bm)])
            gb = assign_bins(bm[in_d], bp_b)
            sb[in_d] = [f"{d}_{b}" for b in gb]
        fy.loc[idx, "size_beme"] = sb

    return fy


def build_portfolio_returns(
    fy: pd.DataFrame, rets: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Expand firm-years to the 12 return months, attach delisting-adjusted
    returns, and compute EW monthly returns of the 100 size x pre-beta
    portfolios (July 1963 - December 1990)."""
    months = pd.DataFrame(
        [(t, ym) for t in range(FIRST_T, LAST_T + 1) for ym in fyr_months(t)],
        columns=["fyr", "ym"],
    )
    long = fy.merge(months, on="fyr", how="inner")
    long = long.merge(rets[["permno", "ym", "ret"]], on=["permno", "ym"], how="left")

    port = (
        long.dropna(subset=["size_decile", "beta_group"])
        .groupby(["size_decile", "beta_group", "ym"])
        .agg(ret=("ret", "mean"), n_stocks=("ret", "count"))
        .reset_index()
    )
    port["size_decile"] = port["size_decile"].astype(np.int32)
    port["beta_group"] = port["beta_group"].astype(np.int32)
    port["month"] = ym_to_month_end(port["ym"].to_numpy())
    port = port[["size_decile", "beta_group", "ym", "month", "n_stocks", "ret"]]
    port = port.sort_values(["size_decile", "beta_group", "ym"]).reset_index(drop=True)
    return long, port


def add_post_beta(fy: pd.DataFrame, port: pd.DataFrame, data: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Post-ranking Dimson sum-betas of the 100 size x pre-beta portfolio EW
    return series (330 months, July 1963 - December 1990) on current and
    1-lagged msi.vwretd; assigned to each stock as of June t via its cell."""
    mkt = data["mkt"].copy()
    mkt["ym"] = pd.to_numeric(mkt["ym"], errors="coerce").astype(np.int64)
    mkt["vwretd"] = pd.to_numeric(mkt["vwretd"], errors="coerce")
    mkt = mkt.dropna(subset=["vwretd"]).sort_values("ym")
    vmap = dict(zip(mkt["ym"], mkt["vwretd"]))
    mkt["vwretd_lag"] = [vmap.get(p, np.nan) for p in ym_prev(mkt["ym"].to_numpy())]
    mkt = mkt[["ym", "vwretd", "vwretd_lag"]]

    reg = port.merge(mkt, on="ym", how="inner").dropna(subset=["ret", "vwretd_lag"])
    reg["cell"] = reg["size_decile"].astype(int) * 100 + reg["beta_group"].astype(int)
    post = grouped_dimson_beta(
        reg.rename(columns={"vwretd": "x0", "vwretd_lag": "x1", "ret": "y"}),
        group_col="cell", min_obs=1,
    )
    post["size_decile"] = (post["cell"] // 100).astype(np.int32)
    post["beta_group"] = (post["cell"] % 100).astype(np.int32)
    post = post.rename(columns={"beta": "post_beta"})[
        ["size_decile", "beta_group", "post_beta", "n_obs"]
    ]

    fy = fy.merge(post[["size_decile", "beta_group", "post_beta"]],
                  on=["size_decile", "beta_group"], how="left")
    return fy, post


def assemble_panel(fy: pd.DataFrame, long: pd.DataFrame) -> pd.DataFrame:
    """One row per (permno, return_month) with firm-year signals and sort
    assignments."""
    cols_fy = [
        "permno", "fyr", "ME_jun", "lnME", "bm", "ln_bm", "ame", "ln_ame",
        "abe", "ln_abe", "ep", "ep_pos", "ep_dummy", "pre_beta", "post_beta",
        "size_decile", "beta_group", "size12", "beta12", "beme12", "ep13",
        "size_beme", "is_nyse",
    ]
    panel = long[["permno", "fyr", "ym", "ret"]].merge(
        fy[cols_fy], on=["permno", "fyr"], how="left"
    )
    panel["month"] = ym_to_month_end(panel["ym"].to_numpy())
    panel = panel.drop(columns=["ym"])
    order = [
        "permno", "month", "fyr", "ret", "ME_jun", "lnME", "bm", "ln_bm",
        "ame", "ln_ame", "abe", "ln_abe", "ep", "ep_pos", "ep_dummy",
        "pre_beta", "size_decile", "beta_group", "post_beta", "size12",
        "beta12", "beme12", "ep13", "size_beme", "is_nyse",
    ]
    panel = panel[order].sort_values(["permno", "month"]).reset_index(drop=True)
    panel["permno"] = panel["permno"].astype(np.int32)
    panel["fyr"] = panel["fyr"].astype(np.int32)
    panel["ep_dummy"] = panel["ep_dummy"].astype(np.int8)
    panel["size_decile"] = panel["size_decile"].astype("Int32")
    panel["beta_group"] = panel["beta_group"].astype("Int32")
    return panel


# ────────────────────────────────────────────────────────────────────────────
# Reporting
# ────────────────────────────────────────────────────────────────────────────
def report(panel: pd.DataFrame, fy: pd.DataFrame, ledger: dict, post: pd.DataFrame,
           port: pd.DataFrame) -> None:
    print("\n" + "=" * 78)
    print("REPORT — Fama & French (1992) panel construction")
    print("=" * 78)

    months = panel["month"].drop_duplicates().sort_values()
    print(f"\nPanel dimensions: {len(panel):,} rows x {panel.shape[1]} cols")
    print(f"  months covered : {len(months)} "
          f"({months.iloc[0].date()} .. {months.iloc[-1].date()}; paper = 330)")
    print(f"  distinct permno: {panel['permno'].nunique():,}")
    print(f"  columns        : {list(panel.columns)}")

    obs_per_month = panel.groupby("month")["ret"].count()
    print(f"\nAvg obs/month (valid ret): {obs_per_month.mean():.1f} (paper FM regressions: ~2267)")
    rows_per_month = panel.groupby("month").size()
    print(f"Avg rows/month (panel)   : {rows_per_month.mean():.1f}")
    print(f"Avg firms/formation year : {fy.groupby('fyr')['permno'].nunique().mean():.1f}")

    print("\nSignal summary stats (firm-year level):")
    sigs = ["lnME", "ln_bm", "ln_ame", "ln_abe", "ep_pos", "pre_beta", "post_beta"]
    stats = fy[sigs].agg(["mean", "median", "std"])
    print(stats.round(4).to_string())

    print("\nRequirement ledger (firm-years):")
    for k, v in ledger.items():
        print(f"  {k:36s}: {v:,}")
    print(f"  {'negative-BE firm-years dropped':36s}: {ledger['drop_BE_nonpositive']:,}")

    print("\nFirms per formation year (1963..1990):")
    per_year = fy.groupby("fyr")["permno"].nunique()
    for t, n in per_year.items():
        print(f"  {t}: {n:,}", end="   " if (t - 1963) % 6 != 5 else "\n")
    print()

    print(f"\nPost-ranking betas across the 100 size x pre-beta portfolios:")
    print(f"  cells estimated : {len(post)}")
    print(f"  range           : {post['post_beta'].min():.3f} .. {post['post_beta'].max():.3f}"
          f"  (paper: 0.53 .. 1.79)")
    print(f"  obs per cell    : min {int(post['n_obs'].min())}, max {int(post['n_obs'].max())}"
          f" (full sample = 330)")

    small = port[port["size_decile"] == 1].groupby("beta_group")["n_stocks"].mean()
    print(f"\nAvg stocks/month in smallest size decile's size-beta portfolios:")
    print(f"  range across the 10 beta portfolios: {small.min():.1f} .. {small.max():.1f}"
          f"  (paper: 70 .. 177)")
    print(f"  per beta group: {small.round(1).to_dict()}")


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    t0 = time.time()
    LAYOUT.ensure()
    data = load_data()

    univ, nyse_bp = build_universe(data["names"])
    fy, ledger = build_firm_years(data, univ, nyse_bp)
    fy = add_variables(fy)
    fy = add_pre_beta(fy, data)

    missing_beta = int(fy["pre_beta"].isna().sum())
    if missing_beta:
        print(f"  [warn] {missing_beta} qualified firm-years without pre_beta "
              f"(singular/short windows) — dropped from sorts/panel")
        fy = fy.dropna(subset=["pre_beta"])

    # June ME for ALL stocks (me_formation.sql has no universe filter)
    me = data["me"].copy()
    me["permno"] = pd.to_numeric(me["permno"], errors="coerce").astype(np.int64)
    me["ym"] = pd.to_numeric(me["ym"], errors="coerce").astype(np.int64)
    me["me"] = pd.to_numeric(me["me"], errors="coerce")
    me_jun_all = (
        me[me["ym"] % 100 == 6][["permno", "ym", "me"]]
        .assign(fyr=(me[me["ym"] % 100 == 6]["ym"] // 100).astype(np.int32))
        .rename(columns={"me": "ME_jun"})[["fyr", "permno", "ME_jun"]]
    )

    fy = run_sorts(fy, nyse_bp, me_jun_all)
    long, port = build_portfolio_returns(fy, data["rets"])
    fy, post = add_post_beta(fy, port, data)
    panel = assemble_panel(fy, long)

    out_panel = LAYOUT.data_path("panel.parquet")
    out_port = LAYOUT.data_path("portfolio_returns.parquet")
    panel.to_parquet(out_panel, index=False)
    port.to_parquet(out_port, index=False)
    print(f"\nWrote {out_panel} ({len(panel):,} rows)")
    print(f"Wrote {out_port} ({len(port):,} rows)")

    report(panel, fy, ledger, post, port)
    print(f"\nTotal time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
