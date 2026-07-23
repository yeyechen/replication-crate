"""
Shared helpers for the QMJ (Asness, Frazzini, Pedersen 2019) return
analysis — Tables 3 and 4, US Long Sample.

Conventions (paper §5.1 / §5.2 and table captions):
- Portfolios formed at the end of month t on quality (etc.), evaluated
  on the next-month excess return (panel ``ret_next``, already in
  decimal, excess over T-bills). Reported return month = t+1.
- Paper window: realized returns 7/1957 .. 12/2016 -> formation months
  1957-06 .. 2016-11 (714 months).
- Returns and alphas reported in monthly PERCENT.
- "Beta" = realized CAPM market loading (Table 3 caption).
- Information ratio = 4-factor alpha / std(4-factor residuals),
  annualized (x sqrt(12)).
- Excess-return t-stats are plain iid (reproduces the paper's arithmetic
  exactly: QMJ t = 3.62 = monthly Sharpe x sqrt(714)); alpha / loading
  t-stats use Newey-West HAC with 60 lags (the paper's 5-year convention;
  the paper's QMJ 4F-alpha t of 9.95 is below the iid 10.8, consistent
  with NW adjustment).
- ff.four_factor_monthly columns are monthly DECIMALS in this
  ClickHouse instance (verified: Sep-2008 mkt_rf = -0.0935). No /100.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC_FILE = Path(__file__).resolve()
_REPO_ROOT = str(_SRC_FILE.parents[3])
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import numpy as np
import pandas as pd
from clickhouse_driver import Client

from utils.env import get_clickhouse_config
from utils.paths import paper_layout

LAYOUT = paper_layout("quality_minus_junk",
                      replications_root=_SRC_FILE.parents[2])
SQL_DIR = LAYOUT.src_path("sql")

# Paper sample: realized returns 7/1957-12/2016 (rule sample_end_date,
# Table 3 caption L1878) -> formation months 1957-06 .. 2016-11.
FIRST_FORMATION = pd.Timestamp("1957-06-01")
LAST_FORMATION = pd.Timestamp("2016-11-01")

FACTORS_1 = ["mkt_rf"]
FACTORS_3 = ["mkt_rf", "smb", "hml"]
FACTORS_4 = ["mkt_rf", "smb", "hml", "mom"]
NW_LAGS = 60  # 5-year HAC, paper convention (fm_annual_regression rule)


# --- data loading -----------------------------------------------------------


def load_panel() -> pd.DataFrame:
    """Load data/panel.parquet and restrict to the Table 3/4 sample:
    formation months 1957-06 .. 2016-11 (realized returns 7/1957-12/2016),
    non-NaN ret_next and mcap > 0 (value weights)."""
    df = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    df["month"] = pd.to_datetime(df["month"])
    df = df[(df["month"] >= FIRST_FORMATION) & (df["month"] <= LAST_FORMATION)]
    df = df[df["ret_next"].notna() & df["mcap"].notna() & (df["mcap"] > 0)]
    return df.reset_index(drop=True)


def load_ff() -> pd.DataFrame:
    """FF 4-factor monthly (US) indexed by month-start, monthly decimals."""
    cfg = get_clickhouse_config()
    c = Client(host=cfg["host"], port=int(cfg["port"]),
               user=cfg["user"], password=cfg["password"],
               settings={"max_execution_time": 60})
    sql = (SQL_DIR / "ff_factors.sql").read_text()
    data, cols = c.execute(sql, with_column_types=True)
    ff = pd.DataFrame(data, columns=[x[0] for x in cols])
    # dt is end-of-month ('1957-07-31') -> month-start
    ff["month"] = pd.to_datetime(ff["dt"]).dt.to_period("M").dt.to_timestamp()
    ff = ff.drop(columns=["dt"]).set_index("month").sort_index()
    for col in ["mkt_rf", "smb", "hml", "mom", "rf"]:
        ff[col] = ff[col].astype(float)
    return ff


def realized_month(series: pd.Series) -> pd.Series:
    """Formation month t -> realization month t+1 (the month ret_next is
    earned)."""
    return (series.dt.to_period("M") + 1).dt.to_timestamp()


# --- portfolio construction --------------------------------------------------


def nyse_deciles(df: pd.DataFrame, signal: str, n_bins: int = 10,
                 nyse_col: str = "hexcd_eom",
                 date_col: str = "month") -> pd.Series:
    """Assign 1..n_bins deciles each month using NYSE breakpoints:
    breakpoints are the signal quantiles among NYSE stocks (hexcd_eom==1)
    of that month; ALL stocks are assigned against those breakpoints.
    Falls back to full-cross-section breakpoints in a month if fewer than
    20 NYSE stocks have a non-NaN signal (never triggers in the US long
    sample; min NYSE count is ~900)."""
    qs = np.linspace(0, 1, n_bins + 1)[1:-1]

    def _assign(g: pd.DataFrame) -> pd.Series:
        nyse = g.loc[g[nyse_col] == 1, signal].dropna()
        base = nyse if len(nyse) >= 20 else g[signal].dropna()
        if len(base) < n_bins:
            return pd.Series(np.nan, index=g.index)
        bp = np.unique(base.quantile(qs).to_numpy())
        bins = [-np.inf, *bp, np.inf]
        # pd.cut is (a, b]: a stock exactly at a breakpoint joins the
        # upper bin; decile 1 = lowest quality (junk).
        return pd.cut(g[signal], bins=bins, labels=False) + 1

    return pd.concat(
        [_assign(g) for _, g in df.groupby(date_col)]
    ).sort_index()


def vw_returns(df: pd.DataFrame, bin_col: str,
               ret_col: str = "ret_next", weight_col: str = "mcap",
               date_col: str = "month") -> pd.DataFrame:
    """Per (month, bin) value-weighted return. Returns long DataFrame
    [month, bin, VW, EW, n_stocks]."""
    work = df[[date_col, bin_col, ret_col, weight_col]].dropna()
    w = work[weight_col]
    out = (work.assign(wxr=w * work[ret_col])
           .groupby([date_col, bin_col], observed=True)
           .agg(wxr=("wxr", "sum"), w=(weight_col, "sum"),
                EW=(ret_col, "mean"), n_stocks=(ret_col, "size")))
    out["VW"] = out["wxr"] / out["w"]
    return out.drop(columns=["wxr", "w"]).reset_index()


def size_group(df: pd.DataFrame, date_col: str = "month") -> pd.Series:
    """Two size groups per month: breakpoint = median NYSE market equity
    (rule sort_qmj_construction). 'Small' if mcap <= median."""
    def _grp(g: pd.DataFrame) -> pd.Series:
        med = g.loc[g["hexcd_eom"] == 1, "mcap"].median()
        return pd.Series(np.where(g["mcap"] <= med, "Small", "Big"),
                         index=g.index)
    return pd.concat([_grp(g) for _, g in df.groupby(date_col)]).sort_index()


def conditional_quality_deciles(df: pd.DataFrame, signal: str,
                                n_bins: int = 10,
                                min_nyse: int = 20) -> pd.Series:
    """Within each (month, size_group) cell, decile breakpoints from the
    NYSE stocks of that cell (conditional NYSE breakpoints); fall back to
    all stocks in the cell if fewer than ``min_nyse`` NYSE names."""
    qs = np.linspace(0, 1, n_bins + 1)[1:-1]

    def _assign(g: pd.DataFrame) -> pd.Series:
        nyse = g.loc[g["hexcd_eom"] == 1, signal].dropna()
        base = nyse if len(nyse) >= min_nyse else g[signal].dropna()
        if len(base) < n_bins:
            return pd.Series(np.nan, index=g.index)
        bp = np.unique(base.quantile(qs).to_numpy())
        return pd.cut(g[signal], bins=[-np.inf, *bp, np.inf],
                      labels=False) + 1

    return pd.concat(
        [_assign(g) for _, g in df.groupby(["month", "size"],
                                           observed=True)]
    ).sort_index()


def qmj_factor(df: pd.DataFrame, signal: str) -> pd.Series:
    """QMJ-style factor for a quality-type signal (rules
    sort_qmj_construction, sort_qmj_top_bottom_30, sort_qmj_formula):
    2 size groups x quality deciles; Quality = deciles 8-10 (top 30%),
    Junk = deciles 1-3 (bottom 30%), VW; factor = 1/2(SQ + BQ) -
    1/2(SJ + BJ). Indexed by REALIZATION month (t+1)."""
    work = df[df[signal].notna()].copy()
    work["size"] = size_group(work)
    work["qdec"] = conditional_quality_deciles(work, signal)
    work = work.dropna(subset=["size", "qdec"])
    work["leg"] = pd.Series(np.nan, index=work.index, dtype=object)
    work.loc[work["qdec"] >= 8, "leg"] = "Quality"   # top 30%
    work.loc[work["qdec"] <= 3, "leg"] = "Junk"      # bottom 30%
    work = work.dropna(subset=["leg"])

    w = work["mcap"]
    agg = (work.assign(wxr=w * work["ret_next"])
           .groupby(["month", "size", "leg"], observed=True)
           .agg(wxr=("wxr", "sum"), w=("mcap", "sum")))
    agg["VW"] = agg["wxr"] / agg["w"]
    wide = agg["VW"].unstack(["size", "leg"])
    qmj = 0.5 * (wide[("Small", "Quality")] + wide[("Big", "Quality")]) \
        - 0.5 * (wide[("Small", "Junk")] + wide[("Big", "Junk")])
    qmj.index = realized_month(pd.Series(qmj.index, name="month")).values
    qmj = qmj.dropna().rename(signal)
    qmj.index.name = "month"
    return qmj


# --- time-series regressions ---------------------------------------------------


def ts_regression(y: pd.Series, ff: pd.DataFrame, factors: list[str],
                  nw_lags: int = NW_LAGS) -> dict:
    """OLS of portfolio excess returns on factor returns (both decimal).
    Returns alpha (decimal, monthly), NW HAC t-stats, loadings, residuals,
    R2 and adjusted R2."""
    import statsmodels.api as sm
    from statsmodels.stats.sandwich_covariance import cov_hac

    d = pd.concat([y.rename("__y"), ff[factors]], axis=1).dropna()
    X = sm.add_constant(d[factors].astype(float))
    model = sm.OLS(d["__y"].astype(float), X).fit()
    try:
        cov = cov_hac(model, nlags=min(nw_lags, int(model.nobs) - len(X.columns) - 1))
        t_nw = model.params / np.sqrt(np.diag(cov))
    except Exception:
        t_nw = model.tvalues
    resid = model.resid
    return {
        "alpha": float(model.params["const"]),
        "alpha_t_nw": float(t_nw["const"]),
        "betas": model.params.drop("const"),
        "beta_t_nw": pd.Series(t_nw).drop("const"),
        "resid": resid,
        "sigma_resid": float(resid.std(ddof=1)),
        "r2": float(model.rsquared),
        "adj_r2": float(model.rsquared_adj),
        "nobs": int(model.nobs),
    }


def portfolio_stats(rets: pd.Series, ff: pd.DataFrame) -> dict:
    """Full metric row for one portfolio/factor series (rets decimal,
    indexed by realization month): excess return, CAPM/3F/4F alphas with
    NW t-stats, CAPM beta, Sharpe, IR (4F), adj R2 (4F)."""
    r = rets.dropna()
    mean, sd, n = r.mean(), r.std(ddof=1), len(r)
    capm = ts_regression(r, ff, FACTORS_1)
    ff3 = ts_regression(r, ff, FACTORS_3)
    ff4 = ts_regression(r, ff, FACTORS_4)
    return {
        "excess_pct": mean * 100,
        "excess_t_iid": mean / (sd / np.sqrt(n)),
        "capm_alpha_pct": capm["alpha"] * 100,
        "capm_alpha_t": capm["alpha_t_nw"],
        "ff3_alpha_pct": ff3["alpha"] * 100,
        "ff3_alpha_t": ff3["alpha_t_nw"],
        "ff4_alpha_pct": ff4["alpha"] * 100,
        "ff4_alpha_t": ff4["alpha_t_nw"],
        "beta": capm["betas"]["mkt_rf"],
        "sharpe": mean / sd * np.sqrt(12),
        "ir": ff4["alpha"] / ff4["sigma_resid"] * np.sqrt(12),
        "adj_r2": ff4["adj_r2"],
        "nobs": n,
        "loadings": ff4["betas"],
        "loading_t": ff4["beta_t_nw"],
        "ff4_resid": ff4["resid"],
        "ff4_alpha_dec": ff4["alpha"],
    }
