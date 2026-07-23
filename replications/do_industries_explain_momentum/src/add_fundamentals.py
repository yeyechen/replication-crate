"""
Stage 2 (inner-loop iteration 2) for Moskowitz & Grinblatt (1999).

READS  data/panel.parquet (iteration-1 CRSP panel, 41 cols), enriches it with
       Compustat book equity and the characteristic-adjusted returns + beta the
       paper needs, and REWRITES data/panel.parquet (48 cols).

Added columns:
  be_dollars      book equity ($) available at month m (6-mo reporting lag, A5)
  bm_sort         be_dollars(m-1) / me(m-1); Daniel-Titman size/BE-ME sort var
  ln_beme         log(bm_sort), the Table VI BE/ME regressor (prev period)
  r_sb            ret - matched 5x5 (size x BE/ME) VW portfolio return, A7 all-
                  universe breakpoints (footnote 5)
  r_dgtw          ret - matched 5x5x5 (size x BE/ME x prior-12mo) VW portfolio
                  return, NYSE breakpoints (footnote 17)
  beta_raw        36-mo rolling OLS slope of stock exret on VW-index exret,
                  >=24 obs, window m-36..m-1 (footnote 25, A11)
  beta_smoothed   pre-ranking 100-group equal-weighted average of beta_raw

Idempotent: re-running recomputes and overwrites the 7 enrichment columns and
leaves every iteration-1 column untouched (row count is preserved exactly).

SCALE NOTE (verified empirically against this ClickHouse vintage): funda
monetary items are in MILLIONS of dollars. Verified via IBM (gvkey 006066 ->
permno 12490): csho(millions of shares) x prcc_f($) x 1e6 matches CRSP
|prc|*shrout*1000 within <1% at FY1971/1989/1994 year-ends. (The task's "billions
x1e9" hypothesis came from gvkey 005086, which is GENERAL SHALE PRODUCTS, not
IBM.) So BE is converted to dollars with *1e6.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402

SLUG = "do_industries_explain_momentum"
LAYOUT = paper_layout(SLUG)
SQL_DIR = LAYOUT.src_path("sql")
_CFG = get_clickhouse_config()

BE_SCALE = 1e6  # funda monetary items are in MILLIONS of dollars (see module doc)
MIN_BE_OBS_DT = 25  # 5x5 / 5x5x5 sorts need at least this many valid stocks


# ----------------------------------------------------------------------------
# ClickHouse access
# ----------------------------------------------------------------------------
def _client() -> Client:
    return Client(
        host=_CFG["host"],
        port=int(_CFG["port"]),
        user=_CFG["user"],
        password=_CFG["password"],
        settings={"max_execution_time": 600},
    )


def q(sql: str) -> pd.DataFrame:
    c = _client()
    try:
        data, cols = c.execute(sql, with_column_types=True)
    finally:
        c.disconnect()
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    return q((SQL_DIR / name).read_text())


def month_ord(ts: pd.Series) -> np.ndarray:
    """year*12 + (month-1): a monotone integer month index for asof merging."""
    return ts.dt.year.to_numpy() * 12 + ts.dt.month.to_numpy() - 1


# ----------------------------------------------------------------------------
# Step 1: book equity cascade (in dollars)
# ----------------------------------------------------------------------------
def book_equity(funda: pd.DataFrame) -> pd.DataFrame:
    """Apply the A3 BE cascade to deduped funda items; return
    (gvkey, fyear, datadate, be_dollars) with be>0 and at>0."""
    df = funda.copy()
    df["datadate"] = pd.to_datetime(df["datadate"], errors="coerce")
    for c in ["at", "ceq", "txdb", "pstkrv", "seq", "dlc", "dltt"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df[df["datadate"].notna()].copy()

    pstk = df["pstkrv"].fillna(0.0)
    txdb = df["txdb"].fillna(0.0)

    be1 = df["ceq"] + txdb - pstk                       # primary: ceq + txdb - pref
    cond1 = df["ceq"].notna() & (be1 > 0)
    be2 = df["seq"]                                      # fallback: seq
    cond2 = (~cond1) & df["seq"].notna() & (be2 > 0)
    be3 = df["at"] - df["dlc"].fillna(0.0) - df["dltt"].fillna(0.0) - pstk  # fallback
    cond3 = (~cond1) & (~cond2) & (be3 > 0)

    be = pd.Series(np.nan, index=df.index, dtype="float64")
    be[cond1] = be1[cond1]
    be[cond2] = be2[cond2]
    be[cond3] = be3[cond3]

    df["be"] = be
    # positivity + total-assets screen (A3)
    df = df[(df["be"] > 0) & (df["at"] > 0)].copy()
    df["be_dollars"] = df["be"] * BE_SCALE
    return df[["gvkey", "fyear", "datadate", "be_dollars"]].reset_index(drop=True)


# ----------------------------------------------------------------------------
# Step 2: link + availability -> be_dollars available at each (permno, month)
# ----------------------------------------------------------------------------
def build_be_avail(be_fy: pd.DataFrame, link: pd.DataFrame) -> pd.DataFrame:
    """Return (permno, avail_ord, be_dollars, linkend_ord) — one row per
    (permno, availability-month). avail = fiscal-year-end + 6 months (A5),
    clipped below by the link start; a (gvkey,permno) link is active at month m
    iff linkdt <= m <= linkenddt (NULL linkenddt = far future)."""
    be = be_fy.copy()
    # availability month = datadate + 6 months (period arithmetic)
    avail_p = be["datadate"].dt.to_period("M") + 6
    be["avail_ord"] = (avail_p.dt.year * 12 + avail_p.dt.month - 1).to_numpy()

    lk = link.copy()
    lk["permno"] = pd.to_numeric(lk["permno"], errors="coerce").astype("Int64")
    lk = lk[lk["permno"].notna()].copy()
    lk["permno"] = lk["permno"].astype("int64")
    linkdt = pd.to_datetime(lk["linkdt"], errors="coerce").fillna(
        pd.Timestamp("1900-01-01")
    )
    linkend = pd.to_datetime(lk["linkenddt"], errors="coerce").fillna(
        pd.Timestamp("2099-12-31")
    )
    lk["link_start_ord"] = linkdt.dt.year.to_numpy() * 12 + linkdt.dt.month.to_numpy() - 1
    lk["linkend_ord"] = linkend.dt.year.to_numpy() * 12 + linkend.dt.month.to_numpy() - 1
    lk["prim_rank"] = np.where(lk["linkprim"].to_numpy() == b"P", 0,
                               np.where(lk["linkprim"].to_numpy() == "P", 0, 1))

    j = be.merge(
        lk[["gvkey", "permno", "link_start_ord", "linkend_ord", "prim_rank"]],
        on="gvkey",
        how="inner",
    )
    # BE usable only once BOTH the FY is published (avail) AND the link is active
    j["usable_ord"] = np.maximum(j["avail_ord"].to_numpy(), j["link_start_ord"].to_numpy())
    j = j[["permno", "gvkey", "usable_ord", "fyear", "be_dollars",
           "linkend_ord", "prim_rank"]]

    # dedupe per (permno, usable month): latest fyear, then primary link 'P',
    # then gvkey as a deterministic tiebreaker (a permno can carry several
    # gvkey links; without gvkey here, drop_duplicates keep='first' would
    # depend on the non-deterministic SQL row order -> run-to-run drift).
    j = j.sort_values(
        ["permno", "usable_ord", "fyear", "prim_rank", "gvkey"],
        ascending=[True, True, False, True, True],
    ).drop_duplicates(["permno", "usable_ord"], keep="first")
    j = j.rename(columns={"usable_ord": "avail_ord"})
    return j[["permno", "avail_ord", "be_dollars", "linkend_ord"]].sort_values(
        ["permno", "avail_ord"]
    ).reset_index(drop=True)


def attach_be_avail(panel: pd.DataFrame, be_avail: pd.DataFrame) -> pd.Series:
    """be_dollars available at each panel (permno, month), forward-filled per
    permno (asof on month ordinal), respecting linkenddt."""
    p = panel[["permno"]].copy()
    p["month_ord"] = month_ord(panel["date"]).astype("int64")
    p = p.sort_values("month_ord", kind="stable").reset_index()  # keep orig idx
    be = be_avail.rename(columns={"be_dollars": "_be"}).copy()
    be["avail_ord"] = be["avail_ord"].astype("int64")
    be["linkend_ord"] = be["linkend_ord"].astype("int64")
    be = be.sort_values("avail_ord", kind="stable")
    m = pd.merge_asof(
        p, be, left_on="month_ord", right_on="avail_ord",
        by="permno", direction="backward",
    )
    # invalidate once the (gvkey,permno) link has ended
    valid = m["month_ord"].to_numpy() <= m["linkend_ord"].to_numpy()
    be_vals = np.where(valid, m["_be"].to_numpy(dtype="float64"), np.nan)
    out = pd.Series(np.nan, index=panel.index, dtype="float64")
    out.loc[m["index"].to_numpy()] = be_vals
    return out


# ----------------------------------------------------------------------------
# Steps 4/5: Daniel-Titman 5x5 and DGTW 5x5x5 characteristic adjustments
# ----------------------------------------------------------------------------
def _quint_breaks(x: pd.Series) -> np.ndarray | None:
    if len(x) < 5:
        return None
    return x.quantile([0.2, 0.4, 0.6, 0.8]).to_numpy()


def dt_adjust_month(g: pd.DataFrame) -> pd.Series:
    """r_sb for one month: 5x5 (size x BE/ME) ALL-universe breakpoints, VW
    portfolios (weights me_lag1). NaN where bm_sort missing or portfolio empty."""
    out = pd.Series(np.nan, index=g.index, dtype="float64")
    valid = g[(g["size_sort"] > 0) & (g["bm_sort"] > 0)]
    if len(valid) < MIN_BE_OBS_DT:
        return out
    size_bp = _quint_breaks(valid["size_sort"])
    if size_bp is None:
        return out
    vdf = valid[["size_sort", "bm_sort", "me_lag1", "ret"]].copy()
    vdf["size_q"] = np.digitize(vdf["size_sort"].to_numpy(), size_bp) + 1
    vdf["bm_q"] = np.nan
    for s in range(1, 6):
        sub = vdf[vdf["size_q"] == s]
        bp = _quint_breaks(sub["bm_sort"])
        if bp is None:
            continue
        vdf.loc[sub.index, "bm_q"] = np.digitize(sub["bm_sort"].to_numpy(), bp) + 1
    vdf = vdf[vdf["bm_q"].notna()].copy()
    if len(vdf) == 0:
        return out
    vdf["bm_q"] = vdf["bm_q"].astype(int)
    vdf["port"] = vdf["size_q"] * 10 + vdf["bm_q"]
    w = vdf[vdf["ret"].notna() & (vdf["me_lag1"] > 0)]
    if len(w) == 0:
        return out
    num = w.assign(wr=w["me_lag1"] * w["ret"]).groupby("port")["wr"].sum()
    den = w.groupby("port")["me_lag1"].sum()
    port_ret = (num / den).replace(0.0, np.nan)
    matched = vdf["port"].map(port_ret)
    ok = matched.notna()
    out.loc[vdf.index[ok]] = g.loc[vdf.index[ok], "ret"].to_numpy() - matched[ok].to_numpy()
    return out


def dgtw_adjust_month(g: pd.DataFrame) -> pd.Series:
    """r_dgtw for one month: 5x5x5 (size x BE/ME x prior-12mo) with NYSE-only
    (exchcd==1) breakpoints applied to ALL stocks; VW portfolios (me_lag1)."""
    out = pd.Series(np.nan, index=g.index, dtype="float64")
    base = (g["size_sort"] > 0) & (g["bm_sort"] > 0) & g["mom_sort"].notna()
    valid = g[base]
    nyse = valid[valid["exchcd"] == 1]
    if len(valid) == 0 or len(nyse) == 0:
        return out

    size_bp = _quint_breaks(nyse["size_sort"])
    if size_bp is None:
        return out
    nyse = nyse.copy()
    nyse["size_q"] = np.digitize(nyse["size_sort"].to_numpy(), size_bp) + 1

    # NYSE bm breakpoints within each size bin, and mom within each (size,bm)
    nyse["bm_q"] = np.nan
    bm_bp = {}
    for s in range(1, 6):
        sub = nyse[nyse["size_q"] == s]
        bp = _quint_breaks(sub["bm_sort"])
        if bp is None:
            continue
        bm_bp[s] = bp
        nyse.loc[sub.index, "bm_q"] = np.digitize(sub["bm_sort"].to_numpy(), bp) + 1
    nyse = nyse[nyse["bm_q"].notna()].copy()
    nyse["bm_q"] = nyse["bm_q"].astype(int)
    mom_bp = {}
    for (s, b), sub in nyse.groupby(["size_q", "bm_q"]):
        bp = _quint_breaks(sub["mom_sort"])
        if bp is not None:
            mom_bp[(int(s), int(b))] = bp

    # apply breakpoints to ALL valid stocks
    vdf = valid[["size_sort", "bm_sort", "mom_sort", "me_lag1", "ret"]].copy()
    vdf["size_q"] = np.digitize(vdf["size_sort"].to_numpy(), size_bp) + 1
    vdf["bm_q"] = np.nan
    for s, bp in bm_bp.items():
        idx = vdf.index[vdf["size_q"] == s]
        if len(idx):
            vdf.loc[idx, "bm_q"] = np.digitize(vdf.loc[idx, "bm_sort"].to_numpy(), bp) + 1
    vdf = vdf[vdf["bm_q"].notna()].copy()
    if len(vdf) == 0:
        return out
    vdf["bm_q"] = vdf["bm_q"].astype(int)
    vdf["mom_q"] = np.nan
    for (s, b), bp in mom_bp.items():
        idx = vdf.index[(vdf["size_q"] == s) & (vdf["bm_q"] == b)]
        if len(idx):
            vdf.loc[idx, "mom_q"] = np.digitize(vdf.loc[idx, "mom_sort"].to_numpy(), bp) + 1
    vdf = vdf[vdf["mom_q"].notna()].copy()
    if len(vdf) == 0:
        return out
    vdf["mom_q"] = vdf["mom_q"].astype(int)
    vdf["port"] = vdf["size_q"] * 10000 + vdf["bm_q"] * 100 + vdf["mom_q"]
    w = vdf[vdf["ret"].notna() & (vdf["me_lag1"] > 0)]
    if len(w) == 0:
        return out
    num = w.assign(wr=w["me_lag1"] * w["ret"]).groupby("port")["wr"].sum()
    den = w.groupby("port")["me_lag1"].sum()
    port_ret = (num / den).replace(0.0, np.nan)
    matched = vdf["port"].map(port_ret)
    ok = matched.notna()
    out.loc[vdf.index[ok]] = g.loc[vdf.index[ok], "ret"].to_numpy() - matched[ok].to_numpy()
    return out


def characteristic_adjustments(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    months = df["date"].dt.to_period("M")
    r_sb = pd.Series(np.nan, index=df.index, dtype="float64")
    r_dgtw = pd.Series(np.nan, index=df.index, dtype="float64")
    key = df[["permno"]].copy()
    key["_m"] = months
    n_months = months.nunique()
    for i, (m, gidx) in enumerate(df.groupby(key["_m"], sort=True).groups.items()):
        g = df.loc[gidx]
        r_sb.loc[gidx] = dt_adjust_month(g)
        r_dgtw.loc[gidx] = dgtw_adjust_month(g)
        if (i + 1) % 50 == 0:
            print(f"      sorts: {i + 1}/{n_months} months")
    return r_sb, r_dgtw


# ----------------------------------------------------------------------------
# Step 6: beta (raw 36-mo rolling OLS + pre-ranking 100-group smoothing)
# ----------------------------------------------------------------------------
def compute_beta(df: pd.DataFrame) -> pd.DataFrame:
    """df must be sorted by (permno, date) with a RangeIndex. Returns a
    DataFrame indexed like df with beta_raw, beta_smoothed."""
    grp = df["permno"].to_numpy()
    x = (df["vw_mkt"].to_numpy(dtype="float64") - df["rf"].to_numpy(dtype="float64"))
    y = df["exret"].to_numpy(dtype="float64")
    mask = ~np.isnan(x) & ~np.isnan(y)
    xm = pd.Series(np.where(mask, x, np.nan), index=df.index)
    ym = pd.Series(np.where(mask, y, np.nan), index=df.index)
    xx = xm * xm
    xy = xm * ym
    ones = pd.Series(np.where(mask, 1.0, np.nan), index=df.index)

    W, MP = 36, 24
    n = ones.groupby(grp).rolling(W, min_periods=MP).count().droplevel(0)
    Sx = xm.groupby(grp).rolling(W, min_periods=MP).sum().droplevel(0)
    Sy = ym.groupby(grp).rolling(W, min_periods=MP).sum().droplevel(0)
    Sxx = xx.groupby(grp).rolling(W, min_periods=MP).sum().droplevel(0)
    Sxy = xy.groupby(grp).rolling(W, min_periods=MP).sum().droplevel(0)
    denom = n * Sxx - Sx * Sx
    slope = (n * Sxy - Sx * Sy) / denom
    # window is m-36..m-1 -> shift the rolling estimate forward one month
    beta_raw = slope.groupby(grp).shift(1).reindex(df.index)

    # pre-ranking smoothing: 100 groups by rank, EW (simple mean) beta per group
    beta_smoothed = pd.Series(np.nan, index=df.index, dtype="float64")
    month = df["date"].dt.to_period("M")
    for m, gidx in df.groupby(month, sort=True).groups.items():
        b = beta_raw.loc[gidx].dropna()
        if len(b) == 0:
            continue
        rank = b.rank(method="first")
        g = np.ceil(rank / len(b) * 100).clip(upper=100).astype(int)
        means = b.groupby(g).mean()
        beta_smoothed.loc[b.index] = g.map(means).to_numpy()
    return pd.DataFrame({"beta_raw": beta_raw, "beta_smoothed": beta_smoothed},
                        index=df.index)


# ----------------------------------------------------------------------------
# Orchestration
# ----------------------------------------------------------------------------
def enrich_panel(panel_path: Path | None = None) -> pd.DataFrame:
    panel_path = panel_path or LAYOUT.data_path("panel.parquet")
    print(f"[s2] reading {panel_path.name} ...")
    df = pd.read_parquet(panel_path)
    n0 = len(df)
    cols0 = list(df.columns)
    sum_ret0 = float(df["ret"].sum())
    print(f"      rows={n0:,}, cols={len(cols0)}; sum(ret)={sum_ret0:.6f}")

    # -- Step 1: book equity -------------------------------------------------
    print("[s2] comp_book_equity.sql (funda items, deduped) ...")
    funda = q_file("comp_book_equity.sql")
    print(f"      funda rows (deduped, 1961-1994): {len(funda):,}")
    be_fy = book_equity(funda)
    print(f"      firm-years with be>0 & at>0: {len(be_fy):,}")

    # -- Step 2: link + availability -----------------------------------------
    print("[s2] ccm_link.sql (linktype LC/LU, usedflag=1, linkprim P/C) ...")
    link = q_file("ccm_link.sql")
    print(f"      link rows: {len(link):,}, permnos: {link['permno'].nunique():,}")
    be_avail = build_be_avail(be_fy, link)
    print(f"      (permno, avail-month) BE records: {len(be_avail):,}")

    df = df.sort_values(["permno", "date"]).reset_index(drop=True)
    df["be_dollars"] = attach_be_avail(df, be_avail)

    # -- Step 3: sort-month characteristics (info at m-1) --------------------
    gb = df.groupby("permno")
    df["be_lag1"] = gb["be_dollars"].shift(1)
    df["size_sort"] = df["me_lag1"]
    df["bm_sort"] = np.where(
        (df["me_lag1"] > 0) & (df["be_lag1"] > 0),
        df["be_lag1"] / df["me_lag1"],
        np.nan,
    )
    df["ln_beme"] = np.where(df["bm_sort"] > 0, np.log(df["bm_sort"]), np.nan)
    # DGTW sorts on the 12-month PRIOR return measured at t-1 (footnote 17):
    # cum(m-12..m-1) = the mom12 column itself. Window ends at m-1, so r_m is
    # NOT in the window -> no look-ahead. (No skip-month shift here.)
    df["mom_sort"] = df["mom12"]

    # -- Steps 4/5: DT 5x5 and DGTW 5x5x5 adjustments ------------------------
    print("[s2] Daniel-Titman 5x5 (r_sb) and DGTW 5x5x5 (r_dgtw) ...")
    df["r_sb"], df["r_dgtw"] = characteristic_adjustments(df)

    # -- Step 6: beta --------------------------------------------------------
    print("[s2] beta_raw (36-mo rolling) + beta_smoothed (100 pre-rank groups) ...")
    beta = compute_beta(df)
    df["beta_raw"] = beta["beta_raw"].to_numpy()
    df["beta_smoothed"] = beta["beta_smoothed"].to_numpy()

    # -- Step 7: write back (41 + 7 = 48 cols) -------------------------------
    new_cols = ["be_dollars", "bm_sort", "ln_beme", "r_sb", "r_dgtw",
                "beta_raw", "beta_smoothed"]
    # idempotent: drop any enrichment cols already present (from a prior run)
    # so the output is exactly base(41) + new(7) = 48 columns, no duplicates.
    base_cols = [c for c in cols0 if c not in new_cols]
    out = df[base_cols + new_cols].copy()
    out = out.sort_values(["permno", "date"]).reset_index(drop=True)
    assert len(out) == n0, f"row count changed: {n0} -> {len(out)}"
    assert abs(float(out["ret"].sum()) - sum_ret0) < 1e-6 * max(1.0, abs(sum_ret0)), \
        "ret column altered!"
    out.to_parquet(panel_path, index=False)
    print(f"[s2] wrote {panel_path.name}: {len(out):,} rows x {len(out.columns)} cols")

    report(df, panel_path)
    return out


# ----------------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------------
def report(df: pd.DataFrame, panel_path: Path) -> None:
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M")
    df["year"] = df["date"].dt.year

    print("\n=== S2-R1: BE coverage (distinct permnos with be_dollars) by year ===")
    for y in [1965, 1973, 1980, 1990, 1995]:
        yy = df[df["year"] == y]
        # report for June when available else whole-year distinct
        mj = yy[yy["month"] == pd.Period(f"{y}-06", "M")]
        if len(mj) == 0:
            mj = yy
        n_be = int(mj["be_dollars"].notna().sum())
        print(f"  {y}: {n_be} / {len(mj)} panel rows have be_dollars "
              f"({n_be / max(1, len(mj)) * 100:.1f}%) [month={mj['month'].iloc[0]}]")

    print("\n=== S2-R2: non-null counts at key dates ===")
    cols = ["r_sb", "r_dgtw", "beta_smoothed", "ln_beme"]
    for m in ["1973-01", "1980-06", "1990-06", "1995-06"]:
        sub = df[df["month"] == pd.Period(m, "M")]
        parts = ", ".join(f"{c}={int(sub[c].notna().sum())}" for c in cols)
        print(f"  {m}: n={len(sub)} | {parts}")

    print("\n=== S2-R3: cross-sectional (EW) mean r_dgtw by year (should be ~0) ===")
    for y in [1973, 1980, 1985, 1990, 1995]:
        sub = df[(df["year"] == y) & df["r_dgtw"].notna()]
        if len(sub):
            print(f"  {y}: EW mean r_dgtw = {sub['r_dgtw'].mean():.6f} "
                  f"(n obs={len(sub):,})")
    # time-series average of the monthly cross-sectional EW mean over the
    # contracted Jan-1973..Jul-1995 period (paper: r*_bar ~ 0.0003, t=0.31)
    contracted = (df["month"] >= pd.Period("1973-01", "M")) & (
        df["month"] <= pd.Period("1995-07", "M"))
    for col in ["r_dgtw", "r_sb"]:
        mon = (df[contracted].dropna(subset=[col])
               .groupby("month")[col].mean())
        if len(mon):
            tstat = mon.mean() / (mon.std(ddof=1) / np.sqrt(len(mon)))
            print(f"  TS avg monthly EW {col} (1973-01..1995-07, "
                  f"T={len(mon)}): {mon.mean():.6f}, t={tstat:.2f}")

    print("\n=== S2-R4: beta_smoothed distribution at 1990-06 ===")
    p90 = df[df["month"] == pd.Period("1990-06", "M")]
    bs = p90["beta_smoothed"].dropna()
    if len(bs):
        print(f"  n={len(bs)} mean={bs.mean():.4f} median={bs.median():.4f} "
              f"p25={bs.quantile(0.25):.4f} p75={bs.quantile(0.75):.4f}")

    print("\n=== S2-R5: FM-readiness at 1990-06 ===")
    fm_cols = ["r_sb", "beta_smoothed", "ln_size", "ln_beme", "mom6", "mom1",
               "ret_36_13", "ind_mom6", "ind_mom1", "ind_ret_36_13", "ind_ret_6_6"]
    fm_cols = [c for c in fm_cols if c in p90.columns]
    ready = int(p90[fm_cols].notna().all(axis=1).sum())
    print(f"  stocks with ALL of {fm_cols} non-null: {ready}")

    print("\n=== S2-R6: IBM (permno 12490) single-stock checks ===")
    ibm = df[df["permno"] == 12490]
    if len(ibm):
        r = ibm[ibm["month"] == pd.Period("1973-06", "M")]
        if len(r):
            r = r.iloc[0]
            print(f"  1973-06: be_dollars={r['be_dollars']:,.0f}, "
                  f"be_lag1={r['be_lag1']:,.0f}, me_lag1={r['me_lag1']:,.0f}, "
                  f"bm_sort={r['bm_sort']:.4f}, ln_beme={r['ln_beme']:.4f}")
            print(f"           bm_sort in (0.05,2)? "
                  f"{0.05 < r['bm_sort'] < 2}")
        r2 = ibm[ibm["month"] == pd.Period("1973-01", "M")]
        if len(r2):
            print(f"  1973-01: r_sb={r2.iloc[0]['r_sb']}")
    else:
        print("  permno 12490 not in panel")

    print("\n=== S2-R7: panel integrity (written file) ===")
    wr = pd.read_parquet(panel_path)
    print(f"  rows={len(wr):,} (expect 1,750,472), cols={len(wr.columns)} "
          f"(expect 48 = 41 + 7)")
    print(f"  sum(ret)={wr['ret'].sum():.6f} (must equal pre-enrich value)")
    print(f"  columns: {list(wr.columns)}")
    added = [c for c in wr.columns if c not in cols0_written()]
    print(f"  added enrichment cols: {added}")


def cols0_written() -> list[str]:
    """The 41 iteration-1 column names (for diffing against the final panel)."""
    return [
        "permno", "date", "ret", "exret", "me", "me_lag1", "vol", "dollar_vol",
        "shrcd", "exchcd", "siccd", "sic2", "ind", "rf", "vw_mkt", "ew_mkt",
        "mom1", "mom6", "mom12", "ret_11_6", "ret_36_13", "ret_6_6",
        "ret_12_12", "ret_7_2", "ret_12_2", "ret_6_6s", "ret_12_12s",
        "ln_size", "ind_ret_vw", "ind_ret_ew", "ind_mom1", "ind_mom6",
        "ind_mom12", "ind_ret_11_6", "ind_ret_36_13", "ind_ret_6_6",
        "ind_ret_12_12", "ind_ret_7_2", "ind_ret_12_2", "ind_ret_6_6s",
        "ind_ret_12_12s",
    ]


if __name__ == "__main__":
    enrich_panel()
