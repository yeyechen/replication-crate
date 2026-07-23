"""
George & Hwang (2004), "The 52-Week High and Momentum Investing", JF —
Table V: Fama-MacBeth dummy-variable regressions. ALSO the shared engine
for Table VII (src/tables_7.py imports run_table / TableConfig from here).

Reads data/panel.parquet (built by src/main.py) + FF factors (src/sql/ff_factors.sql).
Kept SEPARATE from the panel builder: editing this file does NOT rebuild the panel.

Design (paper §II.B, L561-570; Table V caption L625-631; Table VII L1327-1349):
  Each month t in 1963-07 .. 2001-12 (462), for each formation lag j, ONE
  cross-sectional OLS:

    Table V:   R_{it}(%) = b0 + b1*R_{i,t-1} + b2*ln(mcap_$ at t-1)
               + b3*JH + b4*JL + b5*MH + b6*ML + b7*FHH + b8*FHL + e
    Table VII: same, + b7*GH + b8*GL inserted before FHH/FHL (10 dummies).

  (6,6):  j = 2..7   (6 regressions/month,  formation f = t-j)
  (6,12): j = 2..13  (12 regressions/month, formation f = t-j)

  Dummies at formation f come from 30/30 ordinal ranks on the NON-NULL signal
  cross-section at f, using the SAME convention as tables_1_3.py: sort by
  (signal asc, permno asc); bottom int(0.3n) = loser, top int(0.3n) = winner.
    JH/JL  <- jt_sig ;  MH/ML <- mg_sig ;  FHH/FHL <- wh_sig_dc (LOCKED primary)
    GH/GL  <- g_gh   (Table VII only; g_gh is null for ~52% of stock-months —
             early-sample GH dummies are sparse; un-rankable stocks get GH=GL=0
             and STAY in the sample, same convention as the other strategies).

  Regression sample at (t,j): universe rows with ret(t), ret(t-1), mcap(t-1)
  all non-null (mcap>0). Stocks un-rankable for a strategy at f get 0/0 dummies
  for that strategy but STAY in the sample (Assumption 13).

Units: dependent = ret*100 (percent); R_{t-1} = ret (decimal);
       size = ln(mcap column) (panel mcap is already DOLLARS).

Aggregation (Table V/VII reporting convention, L631):
  c_{k,t} = mean of b_{k,j,t} over j (2..7 for (6,6); 2..13 for (6,12)).
  Raw cell  = time-series mean of c_{k,t} over t;
              t-stat = mean / (std(ddof=1)/sqrt(T)).
    Jan incl: all 462 t.  Jan excl: t with month-of-year != 1 (T, std from subset).
  Spread rows (wh/jt/mg/gh_spread): difference SERIES c_{W,t}-c_{L,t}, then same
              mean/t-stat (t-stat from the difference series, NOT diff of t-stats).
  Risk-adjusted columns: regress c_{k,t} on contemporaneous FF3 (mkt_rf, smb,
              hml, DECIMALS in CH -> *100 to percent; merge on month t). Report
              the OLS intercept + its t-stat. Jan incl/excl = run the time-series
              regression on all months / non-Jan months only.

Outputs (per table):
  - results/intermediate/fm_coefficients[_gh].parquet
                                       (the c_{k,t} series, one column per
                                        k x horizon + spread series; also
                                        consumed by the auditor; relocated out
                                        of data/ by audit1.md [M6])
  - results/table_5.md / table_7.md    (rows x 8 cols, values + t-stats + hit rate)
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from clickhouse_driver import Client

from utils.env import get_clickhouse_config
from utils.paths import paper_layout

from tables_1_3 import industry_rank_groups   # industry-level MG cutoff (M5)

LAYOUT = paper_layout("the_52_week_high_and_momentum_investing")
SQL_DIR = LAYOUT.src_path("sql")


def intermediate_path(name: str):
    """Relocated derived caches (audit1.md [M6]): the 8 non-allowlisted
    fm_coefficients*/strategy_returns parquets live under results/intermediate/
    (results/ is validator-clean) instead of data/ (closed parquet allowlist).
    One-line auditable relocation — every cache read/write routes through here.
    panel.parquet + delisting_stats.json stay in data/ (allowlisted / non-parquet)."""
    d = LAYOUT.result_path("intermediate")
    d.mkdir(parents=True, exist_ok=True)
    return d / name


HOLD_START = pd.Timestamp("1963-07-31")
HOLD_END = pd.Timestamp("2001-12-31")
FRAC = 0.30

# LOCKED primary 52WH signal (see Assumption 4 / tables_1_3.py header).
PRIMARY_WH = "wh_sig_dc"

# Strategy -> panel signal column (winner/loser dummies at formation f).
STRAT_SIG = {"jt": "jt_sig", "mg": "mg_sig", "wh": PRIMARY_WH}

# (6,6) and (6,12) formation-lag lists
JLIST = {"s66": list(range(2, 8)), "s612": list(range(2, 14))}

COLS = ["s66_raw_janincl", "s66_raw_janexcl", "s66_ra_janincl", "s66_ra_janexcl",
        "s612_raw_janincl", "s612_raw_janexcl", "s612_ra_janincl", "s612_ra_janexcl"]

TOL = 1e-12

# Order in which spread rows are reported (only strategies present apply).
# "wl" (52-week LOW, Table IX) sits in the wh slot — additive entry, does not
# change Table V/VII row order (they contain wh/jt/mg[/gh] only).
SPREAD_ORDER = ("wh", "wl", "jt", "mg", "gh")


@dataclass(frozen=True)
class TableConfig:
    """One Fama-MacBeth dummy-regression table (Table V or Table VII)."""
    table_id: str                     # "T5" / "T7" in tables_to_replicate.json
    strat_sig: dict                   # ordered strat name -> panel signal column;
                                      # dict order = dummy-column order in X
    coeff_parquet: str                # data/ output name for the c_{k,t} series
    md_name: str                      # results/ output name
    title: str                        # first markdown line
    dummy_pairs: str                  # human-readable dummy<-signal list for the blurb
    preflight_rows: tuple             # s66_raw_janincl rows checked before the grid
    paper_preflight: dict             # row name -> paper anchor (s66_raw_janincl)
    preflight_gate: object = None     # callable(pf, pf_excl) -> list[str] problems
    k_offset: int = 0                 # persistence gap k (Table VI: formation
                                      # f = t-k-j instead of t-j); 0 keeps the
                                      # Table V/VII timing bit-identical


def coef_names(strat_sig: dict) -> list:
    """Regression coefficient order: intercept, r_lag1, size, then per strategy
    (winner, loser) in strat_sig insertion order."""
    out = ["intercept", "r_lag1", "size"]
    for s in strat_sig:
        out += [f"{s}_winner", f"{s}_loser"]
    return out


def make_rows(strat_sig: dict) -> list:
    """Reporting rows: base coefficients, per-strategy winner/loser, then spread
    rows in SPREAD_ORDER (only strategies present)."""
    I = {name: k for k, name in enumerate(coef_names(strat_sig))}
    rows = [("intercept", ("coef", I["intercept"])),
            ("r_lag1", ("coef", I["r_lag1"])),
            ("size", ("coef", I["size"]))]
    for s in strat_sig:
        rows.append((f"{s}_winner", ("coef", I[f"{s}_winner"])))
        rows.append((f"{s}_loser", ("coef", I[f"{s}_loser"])))
    for s in SPREAD_ORDER:
        if s in strat_sig:
            rows.append((f"{s}_spread",
                         ("spread", I[f"{s}_winner"], I[f"{s}_loser"])))
    return rows


# --- Table V configuration (module-level, for `python tables_5.py`) ------------

CFG_V = TableConfig(
    table_id="T5",
    strat_sig=STRAT_SIG,
    coeff_parquet="fm_coefficients.parquet",
    md_name="table_5.md",
    title="# Table V — George & Hwang (2004): Fama-MacBeth dummy-variable regressions",
    dummy_pairs="JH/JL<-jt_sig, MH/ML<-mg_sig, FHH/FHL<-wh_sig_dc",
    preflight_rows=("intercept", "r_lag1", "size", "wh_spread"),
    paper_preflight={"intercept": 3.62, "r_lag1": -6.50, "size": -0.20,
                     "wh_spread": 0.65},
)


# --- targets -----------------------------------------------------------------

def load_targets(table_id: str) -> dict:
    tabs = json.loads(
        LAYOUT.preparations_path("tables_to_replicate.json").read_text()
    )["tables"]
    for t in tabs:
        if t["id"] == table_id:
            return {
                m["name"]: (float(m["value"]), float(m["tolerance_pct"]))
                for m in t["metrics"]
            }
    raise KeyError(f"{table_id} not found in tables_to_replicate.json")


# --- ClickHouse / FF factors ---------------------------------------------------

_CFG = get_clickhouse_config()


def _client() -> Client:
    return Client(host=_CFG["host"], port=int(_CFG["port"]),
                  user=_CFG["user"], password=_CFG["password"],
                  settings={"max_execution_time": 120})


def load_ff() -> pd.DataFrame:
    """FF3 monthly (mkt_rf, smb, hml) in PERCENT, indexed by month-end."""
    sql = (SQL_DIR / "ff_factors.sql").read_text()
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    ff = pd.DataFrame(data, columns=[x[0] for x in cols])
    ff["month"] = pd.to_datetime(ff["dt"])
    for col in ("mkt_rf", "smb", "hml"):
        ff[col] = ff[col].astype("float64") * 100.0   # decimals -> percent
    return ff[["month", "mkt_rf", "smb", "hml"]].sort_values("month").reset_index(drop=True)


# --- panel matrices -------------------------------------------------------------

def load_panel_matrices(ret_col: str = "ret"):
    """Panel -> (grid, permnos, dep_mat, ctrl_mat, mcap_mat) on the clean
    month grid. dep_mat = `ret_col` — the regression DEPENDENT variable R_it
    ("ret" original, "ret_dl" delisting-adjusted); ctrl_mat = ALWAYS the
    ORIGINAL ret (the R_{i,t-1} control and the sample rule stay on
    unadjusted returns: the experiment changes the one return series used as
    the dependent variable, nothing else). NaN where no panel row / null."""
    assert ret_col in ("ret", "ret_dl"), f"unknown return column {ret_col}"
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    grid = pd.date_range(panel["month"].min(), panel["month"].max(), freq="ME")
    uniq = np.sort(panel["month"].unique())
    assert (grid.to_numpy() == uniq).all(), "panel months are not a clean grid"
    permnos = np.sort(panel["permno"].unique())
    M, P = len(grid), len(permnos)

    mi = np.searchsorted(grid.to_numpy(), panel["month"].to_numpy())
    pi = np.searchsorted(permnos, panel["permno"].to_numpy())

    dep_mat = np.full((M, P), np.nan)
    ctrl_mat = np.full((M, P), np.nan)
    mcap_mat = np.full((M, P), np.nan)
    dep_mat[mi, pi] = panel[ret_col].to_numpy(dtype="float64")
    ctrl_mat[mi, pi] = panel["ret"].to_numpy(dtype="float64")
    mcap_mat[mi, pi] = panel["mcap"].to_numpy(dtype="float64")

    return panel, grid.to_numpy(), permnos, dep_mat, ctrl_mat, mcap_mat


def build_rank_sets(panel, grid, permnos, strat_sig=None, rankable_only=False):
    """Per strategy: (Wmat, Lmat) boolean matrices (M x P). Wmat[f] / Lmat[f]
    mark the winner / loser permno indices from the 30/30 ordinal sort on the
    non-null signal cross-section at formation month f.

    Ranking convention (identical to tables_1_3.split_30_30): sort by
    (signal asc, permno asc); bottom int(0.3n) = loser, top int(0.3n) = winner.

    rankable_only (audit1.md [M3], A13 sensitivity; default False = official,
    bit-identical): restrict EACH strategy's ranking cross-section at f to
    stocks on which ALL signals in strat_sig are non-null simultaneously at f
    (the 30/30 split then runs on that common rankable set per strategy).
    """
    if strat_sig is None:
        strat_sig = STRAT_SIG
    if rankable_only:
        keep = np.ones(len(panel), dtype=bool)
        for col in strat_sig.values():
            keep &= panel[col].notna().to_numpy()
        panel = panel.loc[keep]
    M, P = len(grid), len(permnos)
    out = {}
    for strat, sig_col in strat_sig.items():
        sub = panel[["month", "permno", sig_col]].dropna(subset=[sig_col])
        midx = np.searchsorted(grid, sub["month"].to_numpy())
        sig = sub[sig_col].to_numpy(dtype="float64")
        pno = sub["permno"].to_numpy()
        # sort by (month asc, signal asc, permno asc); midx is primary (last key)
        order = np.lexsort((pno, sig, midx))
        midx_s = midx[order]
        pno_s = pno[order]
        bounds = np.concatenate(
            [[0], np.flatnonzero(np.diff(midx_s)) + 1, [len(midx_s)]]
        )
        Wmat = np.zeros((M, P), dtype=bool)
        Lmat = np.zeros((M, P), dtype=bool)
        for a, b in zip(bounds[:-1], bounds[1:]):
            n = b - a
            k = int(FRAC * n)
            f = int(midx_s[a])
            loser_pnos = pno_s[a:a + k]
            winner_pnos = pno_s[b - k:b] if k > 0 else pno_s[a:a]
            if loser_pnos.size:
                Lmat[f, np.searchsorted(permnos, loser_pnos)] = True
            if winner_pnos.size:
                Wmat[f, np.searchsorted(permnos, winner_pnos)] = True
        out[strat] = (Wmat, Lmat)
    return out


def build_rank_sets_industry(grid, permnos, ind_cum: np.ndarray,
                             ind_w: np.ndarray, n_top: int = 6, n_bot: int = 6):
    """Industry-level MG variant (audit1.md [M5]) -> (Wmat, Lmat, diag).

    FM dummy construction under the MG-intended reading: at each formation f,
    rank the 20 INDUSTRIES by their 6-month cumulative VW return (ind_cum,
    from tables_1_3.industry_cum_returns) and set winner dummies for stocks
    in the top `n_top` industries AT f, loser dummies for the bottom
    `n_bot` — instead of the official A8 ordinal split of individual stocks,
    which arbitrarily divides the boundary industry (tables_1_3.
    industry_rank_groups; boundary-tied industries stay in wholesale).
    Rankable = industry(f) defined AND that industry's cumret finite;
    un-rankable stocks get 0/0 dummies (same convention as the official
    engine). `ind_w` is the (P, M) wide industry matrix on `permnos` order.

    diag: {grid_idx: (n_industries, n_tie_w, n_tie_l)} over all grid months;
    months with < n_top + n_bot defined industries get no dummies.
    """
    M, P = len(grid), len(permnos)
    assert ind_cum.shape == (21, M), "ind_cum grid mismatch"
    assert ind_w.shape == (P, M), "ind_w permno/month mismatch"
    Wmat = np.zeros((M, P), dtype=bool)
    Lmat = np.zeros((M, P), dtype=bool)
    diag: dict = {}
    for f in range(M):
        win, lose, n_ind, tw, tl = industry_rank_groups(ind_cum[:, f],
                                                        n_top, n_bot)
        diag[f] = (n_ind, tw, tl)
        if win is None:
            continue
        inds = ind_w[:, f]
        rankable = np.isfinite(inds)
        Wmat[f] = rankable & np.isin(inds, win)
        Lmat[f] = rankable & np.isin(inds, lose)
    return Wmat, Lmat, diag


def rankable_by_decade(panel, grid, strat_sig, f_lo: int, f_hi: int,
                       intersect_key: str | None = None) -> dict:
    """Avg non-null signal count per formation month, by decade, over the
    formation grid f_lo..f_hi actually used by the regressions (f = t-j).
    intersect_key (audit1.md [M3]): when set, ALSO report the count of stocks
    non-null on ALL signals simultaneously, under that key."""
    fmonths = pd.DatetimeIndex(grid[f_lo:f_hi + 1])
    out = {}
    for s, col in strat_sig.items():
        cnt = panel.dropna(subset=[col]).groupby("month")[col].size()
        cnt = cnt.reindex(fmonths, fill_value=0)
        grp = cnt.groupby(cnt.index.year // 10).mean()
        out[s] = {f"{dec * 10}s": float(v) for dec, v in grp.items()}
    if intersect_key is not None:
        sub = panel.dropna(subset=list(strat_sig.values()))
        cnt = sub.groupby("month").size().reindex(fmonths, fill_value=0)
        grp = cnt.groupby(cnt.index.year // 10).mean()
        out[intersect_key] = {f"{dec * 10}s": float(v) for dec, v in grp.items()}
    return out


# --- OLS -------------------------------------------------------------------------

def ols_coef(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """OLS coefficients via the normal equations; lstsq fallback if singular."""
    XtX = X.T @ X
    Xty = X.T @ y
    try:
        return np.linalg.solve(XtX, Xty)
    except np.linalg.LinAlgError:
        return np.linalg.lstsq(X, y, rcond=None)[0]


def run_horizon(jlist, hold_idx, dep_mat, ctrl_mat, mcap_mat, ranks, strat_order,
                k_offset: int = 0, sample_mat=None):
    """Run all cross-sectional regressions for one horizon and return the
    c_{k,t} matrix (n_hold x n_coef) plus diagnostics.

    dep_mat supplies the DEPENDENT variable R_it (ret or ret_dl); ctrl_mat
    supplies the R_{i,t-1} control (always original ret).

    k_offset: persistence gap (Table VI (6,k,12) layout). Dummies are drawn
    from formation f = t - k_offset - j; the default 0 recovers the Table V/
    VII timing f = t - j exactly (bit-identical outputs).

    sample_mat (audit1.md [M3], A13 sensitivity; default None = official,
    bit-identical): an M x P boolean matrix (e.g. "rankable on ALL signals at
    formation f"). When given, the regression sample at (t, j) is the
    official base sample INTERSECTED with sample_mat[f], f = t - k_offset - j
    — i.e. the cross-section restriction varies with the formation lag j, and
    the c_{k,t} average runs only over the j for which the restricted sample
    can still fit all coefficients (NaN rows drop from the mean).

    n_coef = 3 + 2*len(strat_order); dummy columns appear per strategy as
    (winner, loser) in strat_order. c[t_pos, k] = mean over j of b_{k, j, t}.

    Returns (c, sample_sizes, n_reg, reg_sizes): sample_sizes = per-t BASE
    sample (official diagnostic); reg_sizes = per-(t,j) sample actually used
    ([] on the official path, where the two coincide).
    """
    strat_order = list(strat_order)
    n_coef = 3 + 2 * len(strat_order)
    n_hold = len(hold_idx)
    n_j = len(jlist)
    c = np.full((n_hold, n_coef), np.nan)
    sample_sizes = np.zeros(n_hold, dtype="int64")
    reg_sizes: list = []
    n_reg = 0

    if sample_mat is None:
        # ===== OFFICIAL PATH (unchanged; default sample_mat=None) =====
        for pos, a in enumerate(hold_idx):
            # regression sample: dep(t), ret(t-1), mcap(t-1) all non-null, mcap>0
            rt = dep_mat[a]
            rt1 = ctrl_mat[a - 1]
            mc1 = mcap_mat[a - 1]
            sample = (np.isfinite(rt) & np.isfinite(rt1)
                      & np.isfinite(mc1) & (mc1 > 0))
            idx = np.nonzero(sample)[0]
            n = idx.size
            sample_sizes[pos] = n
            if n < n_coef:                  # cannot fit all coefficients
                continue
            y = rt[idx] * 100.0             # percent
            x1 = rt1[idx]                   # decimal
            x2 = np.log(mc1[idx])           # ln(dollars)
            base = np.column_stack([np.ones(n), x1, x2])

            B = np.empty((n_j, n_coef))
            for jj, j in enumerate(jlist):
                f = a - k_offset - j        # formation month grid index
                dummy_cols = []
                for s in strat_order:
                    Ws, Ls = ranks[s]
                    dummy_cols.append(Ws[f, idx].astype("float64"))
                    dummy_cols.append(Ls[f, idx].astype("float64"))
                X = np.column_stack([base, *dummy_cols])
                B[jj] = ols_coef(X, y)
                n_reg += 1
            c[pos] = B.mean(axis=0)         # average over j
        return c, sample_sizes, n_reg, reg_sizes

    # ===== RANKABLE-ONLY PATH (audit1.md [M3], A13 sensitivity) =====
    # The cross-section restriction depends on j through f = t - k_offset - j,
    # so the sample is re-built per (t, j) and the j-average skips lags whose
    # restricted sample cannot fit all coefficients.
    for pos, a in enumerate(hold_idx):
        rt = dep_mat[a]
        rt1 = ctrl_mat[a - 1]
        mc1 = mcap_mat[a - 1]
        base_sample = (np.isfinite(rt) & np.isfinite(rt1)
                       & np.isfinite(mc1) & (mc1 > 0))
        sample_sizes[pos] = int(base_sample.sum())   # unrestricted reference
        B = np.full((n_j, n_coef), np.nan)
        for jj, j in enumerate(jlist):
            f = a - k_offset - j
            idx = np.nonzero(base_sample & sample_mat[f])[0]
            reg_sizes.append(idx.size)
            if idx.size < n_coef:
                continue
            y = rt[idx] * 100.0
            x1 = rt1[idx]
            x2 = np.log(mc1[idx])
            base = np.column_stack([np.ones(idx.size), x1, x2])
            dummy_cols = []
            for s in strat_order:
                Ws, Ls = ranks[s]
                dummy_cols.append(Ws[f, idx].astype("float64"))
                dummy_cols.append(Ls[f, idx].astype("float64"))
            X = np.column_stack([base, *dummy_cols])
            B[jj] = ols_coef(X, y)
            n_reg += 1
        with np.errstate(invalid="ignore"):
            c[pos] = np.nanmean(B, axis=0)   # mean over the j that fitted
        if np.all(~np.isfinite(B[:, 0])):
            c[pos] = np.nan                  # no lag fit this month

    return c, sample_sizes, n_reg, reg_sizes


# --- time-series statistics -------------------------------------------------------

def raw_mean_tstat(series: np.ndarray, mask: np.ndarray):
    x = series[mask]
    x = x[np.isfinite(x)]
    if x.size < 2:
        return np.nan, np.nan
    m = float(x.mean())
    sd = float(x.std(ddof=1))
    t = m / (sd / np.sqrt(x.size)) if sd > 0 else np.nan
    return m, t


def ra_intercept_tstat(series: np.ndarray, ff: np.ndarray, mask: np.ndarray):
    """Intercept + t-stat from regressing `series` on FF3 (ff: n x 3, percent),
    using the months where mask is True and all inputs are finite."""
    ok = mask & np.isfinite(series) & np.all(np.isfinite(ff), axis=1)
    yy = series[ok]
    T = yy.size
    if T < 5:                           # need > 4 params for a t-stat
        return np.nan, np.nan
    X = np.column_stack([np.ones(T), ff[ok]])   # T x 4
    b = ols_coef(X, yy)
    resid = yy - X @ b
    k = X.shape[1]
    s2 = float(resid @ resid) / (T - k)
    try:
        XtX_inv = np.linalg.inv(X.T @ X)
    except np.linalg.LinAlgError:
        return float(b[0]), np.nan
    se0 = float(np.sqrt(s2 * XtX_inv[0, 0]))
    t = float(b[0] / se0) if se0 > 0 else np.nan
    return float(b[0]), t


def row_series(c: np.ndarray, spec) -> np.ndarray:
    kind = spec[0]
    if kind == "coef":
        return c[:, spec[1]]
    return c[:, spec[1]] - c[:, spec[2]]   # spread = winner - loser


# --- tier / formatting -------------------------------------------------------------

def tier(paper: float, ours: float, tol_pct: float) -> str:
    if not np.isfinite(ours):
        return "FAIL"
    if abs(ours - paper) <= abs(paper) * tol_pct / 100.0 + TOL:
        return "Tier 1"
    if paper == 0 or (paper > 0) == (ours > 0):
        return "Tier 2"
    return "FAIL"


TIER2_WARN = "Tier 2 ⚠"


def tier_display(paper: float, ours: float, tol_pct: float) -> str:
    """Tier-COLUMN render string (audit1.md m2). Tier-2 cells whose magnitude
    is far off (|ours/paper| > 2; paper == 0 with a non-zero ours counts as an
    infinite ratio) are flagged 'Tier 2 ⚠'. The underlying tier assignment and
    the hit-rate tally are UNCHANGED — only the displayed tier-column string
    differs (a sign match can still hide a >2x magnitude gap)."""
    tr = tier(paper, ours, tol_pct)
    if tr == "Tier 2" and (paper == 0 or abs(ours / paper) > 2):
        return TIER2_WARN
    return tr


# One-line legend printed under each table's hit-rate summary (audit1.md m2).
TIER2_LEGEND = (
    "Tier 2 ⚠ = sign matches but |ours/paper| > 2 (magnitude far off; see "
    "audit1.md spot-check 10). FAIL cells with |paper| < 0.05 are "
    "rounding-boundary artifacts unless noted."
)


def fmt(x, nd=4) -> str:
    return f"{x:.{nd}f}" if np.isfinite(x) else "NaN"


def dev_pct(paper: float, ours: float) -> str:
    if paper == 0 or not np.isfinite(ours):
        return "n/a"
    return f"{(ours - paper) / abs(paper) * 100:+.1f}%"


# --- shared driver --------------------------------------------------------------------

def run_table(cfg: TableConfig, ret_col: str = "ret_dl",
              write_outputs: bool = True, enforce_gate: bool = True,
              verbose: bool = True, rankable_only: bool = False) -> dict:
    """Full Fama-MacBeth dummy-regression pipeline for one table config.

    ret_col: panel column for the DEPENDENT variable R_it ("ret" original,
    "ret_dl" delisting-adjusted). DEFAULT `ret_dl` = the OFFICIAL dependent
    adopted by the delisting experiment, so `python tables_5.py` /
    `python tables_7.py` reproduce the official artifacts bit-exactly. The
    R_{i,t-1} control, size, dummies (ranked on the original signals), sample
    rule, and FF adjustment are UNCHANGED — only the dependent return series
    switches.

    rankable_only (audit1.md [M3], A13 sensitivity; default False = official,
    bit-identical): restrict EACH (t,j) cross-section to stocks rankable on
    ALL signals in cfg.strat_sig simultaneously at formation f = t-k-j
    (dummies re-built on that common rankable cross-section, same 30/30
    convention; controls, dependent, j-averaging, Jan split and FF3 RA
    unchanged).

    Writes results/intermediate/<cfg.coeff_parquet> + results/<cfg.md_name>
    when write_outputs, prints the console report when verbose.
    enforce_gate=True raises on pre-flight gate failure; False records the
    problems in the bundle ("gate_problems") and continues (used by the
    delisting experiment). Returns the bundle (results, counts, per_col, diag,
    preflight, rankable, c_by_horizon)."""
    targets = load_targets(cfg.table_id)
    rows = make_rows(cfg.strat_sig)
    coef = coef_names(cfg.strat_sig)
    I = {name: k for k, name in enumerate(coef)}
    n_coef = len(coef)

    panel, grid, permnos, dep_mat, ctrl_mat, mcap_mat = load_panel_matrices(ret_col)
    ranks = build_rank_sets(panel, grid, permnos, cfg.strat_sig,
                            rankable_only=rankable_only)

    # A13 rankable-only: sample matrix = stocks non-null on ALL signals at f
    sample_mat = None
    if rankable_only:
        M, P = len(grid), len(permnos)
        keep = np.ones(len(panel), dtype=bool)
        for col in cfg.strat_sig.values():
            keep &= panel[col].notna().to_numpy()
        sample_mat = np.zeros((M, P), dtype=bool)
        mi = np.searchsorted(grid, panel["month"].to_numpy()[keep])
        pi = np.searchsorted(permnos, panel["permno"].to_numpy()[keep])
        sample_mat[mi, pi] = True

    hold0 = int(np.searchsorted(grid, HOLD_START.to_datetime64()))
    hold_end_i = int(np.searchsorted(grid, HOLD_END.to_datetime64()))
    hold_idx = np.arange(hold0, hold_end_i + 1)
    n_hold = len(hold_idx)
    assert n_hold == 462, f"expected 462 holding months, got {n_hold}"
    assert grid[hold0] == np.datetime64(HOLD_START)
    assert grid[hold_end_i] == np.datetime64(HOLD_END)

    # formation grid actually used: f = t-k_offset-j, j in 2..13, t in hold
    f_lo = hold0 - cfg.k_offset - 13
    f_hi = hold_end_i - cfg.k_offset - 2
    rankable = rankable_by_decade(
        panel, grid, cfg.strat_sig, f_lo, f_hi,
        intersect_key=("all3" if rankable_only else None))
    # free the long-form panel; everything below uses the wide matrices
    del panel

    hold_months = pd.DatetimeIndex(grid[hold_idx])
    mo = hold_months.month.to_numpy()
    mask_all = np.ones(n_hold, dtype=bool)
    mask_exjan = mo != 1

    # FF factors aligned to the 462 holding months (percent)
    ff = load_ff()
    ff_aligned = ff.set_index("month").reindex(hold_months)
    ff_arr = ff_aligned[["mkt_rf", "smb", "hml"]].to_numpy(dtype="float64")
    n_ff_missing = int(np.any(~np.isfinite(ff_arr), axis=1).sum())
    assert n_ff_missing == 0, f"{n_ff_missing} holding months missing FF factors"

    # ---- run both horizons -----------------------------------------------------
    c_by_horizon = {}
    diag = {}
    for hz, jlist in JLIST.items():
        c, ss, nreg, rsizes = run_horizon(
            jlist, hold_idx, dep_mat, ctrl_mat, mcap_mat,
            ranks, list(cfg.strat_sig),
            k_offset=cfg.k_offset, sample_mat=sample_mat)
        assert c.shape[1] == n_coef
        c_by_horizon[hz] = c
        diag[hz] = {"avg_sample": float(ss.mean()), "min_sample": int(ss.min()),
                    "max_sample": int(ss.max()), "n_reg": int(nreg),
                    "n_months_empty": int((ss < n_coef).sum())}
        if rsizes:   # rankable-only path: per-(t,j) restricted sample sizes
            rs = np.asarray(rsizes)
            diag[hz]["avg_reg_sample"] = float(rs.mean())
            diag[hz]["min_reg_sample"] = int(rs.min())
            diag[hz]["max_reg_sample"] = int(rs.max())

    # ---- c_{k,t} parquet --------------------------------------------------------
    coeff = pd.DataFrame({"month": hold_months})
    for hz, c in c_by_horizon.items():
        for k, name in enumerate(coef):
            coeff[f"{hz}_{name}"] = c[:, k]
        for s in SPREAD_ORDER:
            if s in cfg.strat_sig:
                coeff[f"{hz}_{s}_spread"] = (c[:, I[f"{s}_winner"]]
                                             - c[:, I[f"{s}_loser"]])
    if write_outputs:
        coeff.to_parquet(intermediate_path(cfg.coeff_parquet), index=False)

    # ---- pre-flight (s66_raw_janincl / janexcl) ---------------------------------
    c66 = c_by_horizon["s66"]
    row_specs = dict(rows)
    pf = {}       # row -> (mean, tstat) Jan-incl
    pf_excl = {}  # row -> (mean, tstat) Jan-excl
    for rname in cfg.preflight_rows:
        s = row_series(c66, row_specs[rname])
        pf[rname] = raw_mean_tstat(s, mask_all)
        pf_excl[rname] = raw_mean_tstat(s, mask_exjan)
    if verbose:
        print("=" * 78)
        print(f"PRE-FLIGHT CHECK [{cfg.table_id}] — s66_raw, dependent `{ret_col}` "
              f"(must be sane before trusting the full grid)")
        for rname in cfg.preflight_rows:
            m, t = pf[rname]
            me, te = pf_excl[rname]
            print(f"  {rname:10s}  janincl {m:8.4f} (t {t:6.2f})  janexcl {me:8.4f} "
                  f"(t {te:6.2f})   paper_janincl {cfg.paper_preflight[rname]:6.2f}")
        print("=" * 78)

    gate_problems = []
    if cfg.preflight_gate is not None:
        gate_problems = cfg.preflight_gate(pf, pf_excl)
        if gate_problems:
            msg = (f"PRE-FLIGHT GATE FAILED [{cfg.table_id}] "
                   f"(dependent `{ret_col}`):\n - " + "\n - ".join(gate_problems))
            if enforce_gate:
                raise RuntimeError(msg + "\nstop and diagnose")
            print(f"WARNING: {msg}\n(enforce_gate=False — continuing)")

    # ---- build the full results grid (value + tstat) ----------------------------
    # results[(col, row, kind)] = (ours, paper, tol, tier)
    results = {}
    counts = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0}
    per_col = {col: {"Tier 1": 0, "Tier 2": 0, "FAIL": 0} for col in COLS}

    for hz in ("s66", "s612"):
        c = c_by_horizon[hz]
        for rname, spec in rows:
            s = row_series(c, spec)
            for flavor in ("raw", "ra"):
                for jan, mask in (("janincl", mask_all), ("janexcl", mask_exjan)):
                    col = f"{hz}_{flavor}_{jan}"
                    if flavor == "raw":
                        val, t = raw_mean_tstat(s, mask)
                    else:
                        val, t = ra_intercept_tstat(s, ff_arr, mask)
                    for kind, v in (("val", val), ("tstat", t)):
                        mname = f"{col}_{rname}" + ("_tstat" if kind == "tstat" else "")
                        paper, tol = targets[mname]
                        tr = tier(paper, v, tol)
                        counts[tr] += 1
                        per_col[col][tr] += 1
                        results[(col, rname, kind)] = (v, paper, tol, tr)

    total = sum(counts.values())
    expected = len(rows) * len(COLS) * 2
    assert total == expected, f"expected {expected} metrics, got {total}"

    # ---- write results md --------------------------------------------------------
    n_dummies = 2 * len(cfg.strat_sig)
    L = [
        cfg.title,
        "",
        "Each month t (1963-07 .. 2001-12, 462) x formation lag j: one cross-sectional",
        f"OLS of R_{{it}}(%) on R_{{i,t-1}}(decimal), ln(mcap_$ at t-1), and {n_dummies} strategy",
        f"dummies ({cfg.dummy_pairs}). Dummies from 30/30 ordinal sorts at formation",
        "f=t-j on the non-null signal cross-section (same convention as tables_1_3);",
        "stocks un-rankable for a strategy get 0/0 dummies and stay in the sample.",
        "(6,6): j=2..7 ; (6,12): j=2..13. c_{k,t}=mean_j b_{k,j,t}; raw=TS mean of c",
        "with t-stat from the c series; RA=intercept of c (or spread) series on FF3.",
        "Jan incl = all 462 t; Jan excl = month-of-year != 1.",
        "",
        f"Dependent variable R_it: panel column `{ret_col}`"
        + (" (delisting-adjusted)" if ret_col == "ret_dl" else "")
        + "; R_{i,t-1} control, dummies, and sample rule on original ret.",
        "",
        "## Rankable stocks per formation month (avg by decade, formation grid only)",
        "",
    ]
    decades = sorted({d for v in rankable.values() for d in v})
    L.append("| strategy | " + " | ".join(decades) + " |")
    L.append("|---|" + "---:|" * len(decades))
    rank_labels = [(s, f"{s} ({cfg.strat_sig[s]})") for s in cfg.strat_sig]
    if rankable_only:
        rank_labels.append(("all3", "ALL THREE SIMULTANEOUSLY (restricted sample)"))
    for key, label in rank_labels:
        vals = rankable[key]
        L.append(f"| {label} | "
                 + " | ".join(f"{vals.get(d, 0.0):.1f}" for d in decades) + " |")
    L += [
        "",
        "## Pre-flight (s66_raw)",
        "",
        "| row | ours janincl | paper janincl | ours janexcl |",
        "|---|---:|---:|---:|",
    ]
    for rname in cfg.preflight_rows:
        m, t = pf[rname]
        me, te = pf_excl[rname]
        L.append(f"| {rname} | {fmt(m)} (t {fmt(t,2)}) | "
                 f"{cfg.paper_preflight[rname]:.2f} | {fmt(me)} (t {fmt(te,2)}) |")
    L += ["", "## Diagnostics", ""]
    for hz in ("s66", "s612"):
        d = diag[hz]
        L.append(f"- {hz}: avg sample {d['avg_sample']:.1f} "
                 f"(min {d['min_sample']}, max {d['max_sample']}), "
                 f"{d['n_reg']} regressions, {d['n_months_empty']} empty months")
        if "avg_reg_sample" in d:
            L.append(f"  - rankable-only restricted cross-section: avg "
                     f"{d['avg_reg_sample']:.1f} (min {d['min_reg_sample']}, "
                     f"max {d['max_reg_sample']}) per (t,j) regression")
    L.append(f"- FF factors: {ff_arr.shape[0]} months aligned, {n_ff_missing} missing")
    L += ["", f"## Overall hit rate (of {total})", ""]
    L.append(f"**Tier 1: {counts['Tier 1']} / Tier 2: {counts['Tier 2']} / "
             f"FAIL: {counts['FAIL']}**")
    L += ["", "### Per-column tally", "",
          "| column | Tier 1 | Tier 2 | FAIL |", "|---|---:|---:|---:|"]
    for col in COLS:
        cc = per_col[col]
        L.append(f"| {col} | {cc['Tier 1']} | {cc['Tier 2']} | {cc['FAIL']} |")
    L += ["", f"_{TIER2_LEGEND}_"]

    # detailed per-column tables (values, then t-stats)
    for col in COLS:
        L += ["", f"### Column: {col}", "",
              "| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |",
              "|---|---:|---:|---:|---|---:|---:|---|"]
        for rname, _ in rows:
            v, pv, tol, tr = results[(col, rname, "val")]
            vt, pt, tolt, trt = results[(col, rname, "tstat")]
            L.append(f"| {rname} | {fmt(pv)} | {fmt(v)} | {dev_pct(pv, v)} "
                     f"| {tier_display(pv, v, tol)} "
                     f"| {fmt(pt)} | {fmt(vt)} | {tier_display(pt, vt, tolt)} |")

    if write_outputs:
        LAYOUT.result_path(cfg.md_name).write_text("\n".join(L))

    # ---- console report ----------------------------------------------------------
    spread_rows = [f"{s}_spread" for s in SPREAD_ORDER if s in cfg.strat_sig]
    if verbose:
        print()
        print(f"[{cfg.table_id}] dependent `{ret_col}`")
        print("RANKABLE STOCKS / FORMATION MONTH (avg by decade)")
        for key, label in rank_labels:
            vals = rankable[key]
            print(f"  {label}: " + "  ".join(f"{d} {vals.get(d, 0.0):7.1f}"
                                             for d in decades))
        print()
        print("DIAGNOSTICS")
        for hz in ("s66", "s612"):
            d = diag[hz]
            print(f"  {hz}: avg sample {d['avg_sample']:.1f} (min {d['min_sample']}, "
                  f"max {d['max_sample']}), {d['n_reg']} regressions, "
                  f"{d['n_months_empty']} empty months")
            if "avg_reg_sample" in d:
                print(f"       rankable-only restricted cross-section: avg "
                      f"{d['avg_reg_sample']:.1f} (min {d['min_reg_sample']}, "
                      f"max {d['max_reg_sample']}) per (t,j) regression")
        print()
        print("PER-COLUMN TALLY")
        for col in COLS:
            cc = per_col[col]
            print(f"  {col:22s} T1 {cc['Tier 1']:2d}  T2 {cc['Tier 2']:2d}  "
                  f"FAIL {cc['FAIL']:2d}")
        print()
        print(f"OVERALL: T1 {counts['Tier 1']} / T2 {counts['Tier 2']} / "
              f"FAIL {counts['FAIL']} of {total}")
        print()
        print("SPREAD / STRATEGY CELLS (ours vs paper)")
        for hz in ("s66", "s612"):
            for flavor in ("raw", "ra"):
                for jan in ("janincl", "janexcl"):
                    col = f"{hz}_{flavor}_{jan}"
                    for rname in spread_rows:
                        v, pv, tol, tr = results[(col, rname, "val")]
                        vt, pt, tolt, trt = results[(col, rname, "tstat")]
                        print(f"  {col:18s} {rname:10s}  val {v:7.4f} (paper {pv:6.2f}) "
                              f"{tr:6s} | t {vt:6.2f} (paper {pt:6.2f}) {trt}")

    return {"results": results, "counts": counts, "per_col": per_col,
            "diag": diag, "pf": pf, "pf_excl": pf_excl, "rankable": rankable,
            "c_by_horizon": c_by_horizon, "rows": rows, "total": total,
            "coeff": coeff, "ret_col": ret_col,
            "gate_problems": gate_problems}


def main() -> None:
    run_table(CFG_V)


if __name__ == "__main__":
    main()
