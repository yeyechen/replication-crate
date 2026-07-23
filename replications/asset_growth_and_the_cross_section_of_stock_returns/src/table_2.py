"""
Cooper, Gulen, Schill (2008) — TABLE II replication.

"Asset Growth and the Cross-Section of Stock Returns", Journal of Finance.

Table II reports, for the ten annual asset-growth (ASSETG) deciles formed at the
end of June each year t over 1968-2002 (held July t -> June t+1, rebalanced
annually), the Year-1 portfolio return statistics in event time:

  Panel A  — formation-period annual ASSETG rates (the sort variable; identical
             to Table I; reproduced here from data/formation.parquet).
  Panel B  — Year-1 average MONTHLY raw returns, EW (B.1) and VW (B.2): all 10
             deciles + the D10-D1 spread and its t-stat (this module's Section A),
             plus the annual-return consistency / Sharpe / annualized stats
             (Section B).
  Panel C  — Year-1 three-factor (Fama-French 1993) alphas, EW (C.1) and VW (C.2),
             for all firms and for the NYSE 30/70 small/medium/large size groups
             (Section C).
  (robustness) — Carhart (1997) four-factor spread alpha (Section D).
  Panel D  — decade-subperiod three-factor spread alphas (Section F).
  Panel B last rows — cumulative Year 1..5 buy-and-hold spread (Section E).

Inputs:
  data/panel.parquet      one row per (permno, month[CRSP last-trading-day],
                          ret[delisting-adjusted], me[$], formation_year,
                          decile[1..10], size_group). 420 months 1968-07..2003-06.
  data/formation.parquet  one row per (permno, june_year); carries MV ($M, June-t
                          market equity) used as the FIXED value weight, decile,
                          size_group, ASSETG.
  src/sql/ff_factors_monthly.sql  monthly FF factors (merged in Python).

Outputs:
  results/table_2.md, results/table_2_eval.json,
  results/table2_year1_decile_returns.png, results/table2_spread_pnl.png,
  results/table2_annual_spread.png.

CONVENTIONS (stated explicitly):
  * Year-1 == the full monthly series. Every month in the panel belongs to the
    YEAR-1 holding period of its formation_year (annual July-t rebalance), so the
    420-month series IS the Year-1 return series (no separate construction).
  * Spread == D10 - D1 (high-growth minus low-growth), reported NEGATIVE. The P&L
    / annual / Sharpe plots use the long-short D1 - D10 (low minus high, positive).
  * EW = mean(ret) within (month, decile). VW = sum(ret*me_june)/sum(me_june) using
    the FIXED June-t formation market equity (MV from formation.parquet) as the
    weight — NOT the contemporaneous monthly me. (Using same-month me biases VW up
    by ~1.3pp/mo because weight is correlated with the same-month return; the
    paper's rule `sample_me_timing`, L87, uses June-t ME. June weights reproduce
    the paper's VW D1=1.48/D10=0.43 exactly; contemporaneous weights give 2.77/1.83.)
  * t-stats: Newey-West (HAC) with NW_LAGS = 3 on the relevant monthly series —
    the spread return series for raw returns, and the intercept of the spread
    (D10-D1) regressed on the factors for alphas. The paper's extreme-decile alpha
    t-stat uses a GMM/delta-method joint test with an HAC covariance (footnote 12,
    L1574); a Newey-West t-stat on the spread series is the accepted approximation.
    iid (n_lags=0) values are reported alongside for transparency.
  * Three-factor alpha = intercept of (portfolio_ret - rf) on (mkt_rf, smb, hml),
    x100 (%/month). Spread alpha = alpha_D10 - alpha_D1 == intercept of the
    (D10-D1) return (a zero-investment portfolio, so rf is NOT subtracted) on the
    factors. FF3/Carhart factors from ff.four_factor_monthly (Assumption 5).
  * Data-vintage note (Assumption 7): the 2026 Compustat vintage fattens the ASSETG
    upper tail, so Panel A ASSETG upper-decile cells run above the paper. No extra
    screen is applied; affected Panel A cells are Tier 2, as in Table I.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless backend — first matplotlib import
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_hac

# --- repo / layout -----------------------------------------------------------
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from clickhouse_driver import Client          # noqa: E402
from utils.env import get_clickhouse_config   # noqa: E402
from utils.metrics import tstat_newey_west    # noqa: E402
from utils.plot import plot_cumulative_returns  # noqa: E402
from utils.regressions import factor_alpha    # noqa: E402

SLUG_DIR = Path(__file__).resolve().parents[1]
DATA = SLUG_DIR / "data"
RESULTS = SLUG_DIR / "results"
PREP = SLUG_DIR / "preparations"
SQL_DIR = SLUG_DIR / "src" / "sql"
RESULTS.mkdir(parents=True, exist_ok=True)

N_DECILES = 10
NW_LAGS = 3                       # primary Newey-West lag convention
FF3 = ["mkt_rf", "smb", "hml"]
FF4 = ["mkt_rf", "smb", "hml", "mom"]
SIZE_GROUPS = ["small", "medium", "large"]
# Decade subperiods keyed on formation_year (Year-1 months follow the cohort).
SUBPERIODS = [("1968-1980", 1968, 1979),
              ("1981-1990", 1980, 1989),
              ("1991-2003", 1990, 2002)]

_CFG = get_clickhouse_config()


def _client() -> Client:
    return Client(host=_CFG["host"], port=int(_CFG["port"]),
                  user=_CFG["user"], password=_CFG["password"],
                  database=_CFG["database"], settings={"max_execution_time": 300})


def q_file(name: str) -> pd.DataFrame:
    c = _client()
    data, cols = c.execute((SQL_DIR / name).read_text(), with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


# =============================================================================
# helpers
# =============================================================================
def port_returns(df: pd.DataFrame, wcol: str, keys: list) -> pd.DataFrame:
    """EW = mean(ret); VW = sum(ret*w)/sum(w), per group `keys`.
    Returns long DataFrame (index = keys, cols EW/VW). NaN ret rows dropped;
    VW additionally drops NaN-weight rows."""
    d = df.dropna(subset=["ret"])
    ew = d.groupby(keys)["ret"].mean()
    dv = d.dropna(subset=[wcol])
    vw = (dv.assign(_rw=dv["ret"] * dv[wcol]).groupby(keys)["_rw"].sum()
          / dv.groupby(keys)[wcol].sum())
    return pd.DataFrame({"EW": ew, "VW": vw})


def wide(mat: pd.DataFrame, weighting: str) -> pd.DataFrame:
    """index = month Period, columns = decile 1..10."""
    return mat[weighting].unstack("decile")


def fy_of(period_index) -> np.ndarray:
    """formation_year of each month (Jul t..Jun t+1 -> t)."""
    return np.array([p.year if p.month >= 7 else p.year - 1 for p in period_index])


def annualize(mat: pd.DataFrame) -> pd.DataFrame:
    """Compound the 12 monthly portfolio returns of each formation year.
    Input: index = month Period, cols = deciles. Output: index = fy, cols deciles."""
    d = mat.copy()
    d["fy"] = fy_of(d.index)
    cols = [c for c in d.columns if c != "fy"]
    ann = d.groupby("fy")[cols].apply(lambda g: (1 + g).prod() - 1)
    return ann


def spread_alpha(r_hi: pd.Series, r_lo: pd.Series, ff: pd.DataFrame,
                 factors: list, n_lags: int):
    """Alpha (and NW t) of the zero-investment D10-D1 spread: regress the spread
    return (NO rf subtraction) on the factors with an intercept. Intercept ==
    alpha_hi - alpha_lo. Returns (alpha_pct, t, nobs)."""
    sp = (r_hi - r_lo).to_frame("__sp").dropna()
    m = sp.join(ff[factors], how="inner").dropna()
    X = sm.add_constant(m[factors].astype(float))
    res = sm.OLS(m["__sp"].astype(float), X).fit()
    se = (float(np.sqrt(cov_hac(res, nlags=n_lags)[0, 0])) if n_lags > 0
          else float(res.bse["const"]))
    a = float(res.params["const"])
    return a * 100.0, a / se, int(res.nobs)


def decile_alpha(ret_series: pd.Series, ff: pd.DataFrame, factors: list,
                 n_lags: int) -> float:
    """3-/4-factor alpha (%/month) of a single long-only decile portfolio."""
    res = factor_alpha(ret_series, ff, factors=factors, rf_col="rf", n_lags=n_lags)
    return float(res["alpha_monthly"]) * 100.0


# =============================================================================
# load
# =============================================================================
def load():
    panel = pd.read_parquet(DATA / "panel.parquet")
    form = pd.read_parquet(DATA / "formation.parquet")
    panel["month"] = pd.to_datetime(panel["month"])
    panel["ym"] = panel["month"].dt.to_period("M")
    # FIXED June-t formation market equity ($M) as the VW weight
    w = form[["permno", "june_year", "MV"]].rename(
        columns={"june_year": "formation_year", "MV": "me_june"})
    panel = panel.merge(w, on=["permno", "formation_year"], how="left")

    ff = q_file("ff_factors_monthly.sql")
    ff["ym"] = pd.to_datetime(ff["month"]).dt.to_period("M")
    ff = ff.set_index("ym")[["mkt_rf", "smb", "hml", "mom", "rf"]].astype(float)
    ff = ff.sort_index()
    return panel, form, ff


# =============================================================================
def main():
    panel, form, ff = load()
    print(f"panel {panel.shape}, months {panel['ym'].nunique()}, "
          f"factors {ff.shape} ({ff.index.min()}..{ff.index.max()})")

    # ---- monthly portfolio returns: all firms + per size group --------------
    all_pr = port_returns(panel, "me_june", ["ym", "decile"])
    ew = wide(all_pr, "EW")           # index ym, cols 1..10
    vw = wide(all_pr, "VW")
    n_months = len(ew)

    sg_ew, sg_vw = {}, {}
    for sg in SIZE_GROUPS:
        pr = port_returns(panel[panel["size_group"] == sg], "me_june", ["ym", "decile"])
        sg_ew[sg] = wide(pr, "EW")
        sg_vw[sg] = wide(pr, "VW")

    R = {}   # results dict for the eval json

    # =========================================================================
    # SECTION A — Year-1 monthly raw returns (Panel B Year-1 row)
    # =========================================================================
    secA = {}
    for wname, mat in [("EW", ew), ("VW", vw)]:
        means = mat.mean() * 100.0
        spread = mat[N_DECILES] - mat[1]                 # D10 - D1 (negative)
        t_nw = tstat_newey_west(spread, n_lags=NW_LAGS)["t_stat"]
        t_iid = tstat_newey_west(spread, n_lags=0)["t_stat"]
        secA[wname] = {
            "deciles": {f"D{d}": float(means[d]) for d in range(1, N_DECILES + 1)},
            "spread_10_1": float(spread.mean() * 100.0),
            "spread_t_nw": float(t_nw), "spread_t_iid": float(t_iid),
        }
    R["section_A"] = secA

    # =========================================================================
    # SECTION B — annual Year-1 returns: consistency, Sharpe, annualized
    # =========================================================================
    ew_ann = annualize(ew)          # index fy (35), cols deciles
    vw_ann = annualize(vw)
    n_years = len(ew_ann)
    months_per_yr = ew.groupby(fy_of(ew.index)).size()
    assert (months_per_yr == 12).all(), "every formation year must have 12 months"

    ew_cons = float((ew_ann[1] > ew_ann[N_DECILES]).mean() * 100.0)
    vw_cons = float((vw_ann[1] > vw_ann[N_DECILES]).mean() * 100.0)
    vw_spread_ann = vw_ann[1] - vw_ann[N_DECILES]        # low minus high, positive
    vw_sharpe = float(vw_spread_ann.mean() / vw_spread_ann.std(ddof=1))
    ew_spread_ann = ew_ann[1] - ew_ann[N_DECILES]
    ew_sharpe = float(ew_spread_ann.mean() / ew_spread_ann.std(ddof=1))

    def annzd(monthly_mean):
        return float(((1 + monthly_mean) ** 12 - 1) * 100.0)

    secB = {
        "n_years": int(n_years),
        "EW_pct_years_low_beats_high": ew_cons,
        "VW_pct_years_low_beats_high": vw_cons,
        "VW_spread_Sharpe_annual": vw_sharpe,
        "EW_spread_Sharpe_annual": ew_sharpe,
        # mean of the 35 annual returns (%/yr)
        "EW_D1_annual_mean": float(ew_ann[1].mean() * 100),
        "EW_D10_annual_mean": float(ew_ann[N_DECILES].mean() * 100),
        "VW_D1_annual_mean": float(vw_ann[1].mean() * 100),
        "VW_D10_annual_mean": float(vw_ann[N_DECILES].mean() * 100),
        # annualized monthly mean (%/yr)
        "EW_D1_annualized": annzd(ew[1].mean()),
        "EW_D10_annualized": annzd(ew[N_DECILES].mean()),
        "VW_D1_annualized": annzd(vw[1].mean()),
        "VW_D10_annualized": annzd(vw[N_DECILES].mean()),
    }
    R["section_B"] = secB

    # =========================================================================
    # SECTION C — three-factor alphas (all firms + size groups)
    # =========================================================================
    def alpha_block(mat):
        """Per-decile 3-factor alpha + the D10-D1 spread alpha and t (NW + iid)."""
        alphas = {f"D{d}": decile_alpha(mat[d], ff, FF3, NW_LAGS)
                  for d in range(1, N_DECILES + 1)}
        sp_pct, t_nw, n = spread_alpha(mat[N_DECILES], mat[1], ff, FF3, NW_LAGS)
        _, t_iid, _ = spread_alpha(mat[N_DECILES], mat[1], ff, FF3, 0)
        alphas.update({"spread_10_1": float(sp_pct),
                       "spread_t_nw": float(t_nw), "spread_t_iid": float(t_iid),
                       "n_obs": n})
        return alphas

    secC = {"EW_all": alpha_block(ew), "VW_all": alpha_block(vw), "size_groups": {}}
    for sg in SIZE_GROUPS:
        secC["size_groups"][sg] = {"EW": alpha_block(sg_ew[sg]),
                                   "VW": alpha_block(sg_vw[sg])}
    R["section_C"] = secC

    # =========================================================================
    # SECTION D — Carhart four-factor robustness (all-firm spread)
    # =========================================================================
    secD = {}
    for wname, mat in [("EW", ew), ("VW", vw)]:
        sp_pct, t_nw, n = spread_alpha(mat[N_DECILES], mat[1], ff, FF4, NW_LAGS)
        _, t_iid, _ = spread_alpha(mat[N_DECILES], mat[1], ff, FF4, 0)
        secD[wname] = {"spread_10_1": float(sp_pct),
                       "spread_t_nw": float(t_nw), "spread_t_iid": float(t_iid),
                       "n_obs": n}
    R["section_D"] = secD

    # =========================================================================
    # SECTION F — decade subperiod three-factor spread alphas
    # =========================================================================
    fy = fy_of(ew.index)
    secF = {}
    for label, a, b in SUBPERIODS:
        mask = (fy >= a) & (fy <= b)
        row = {"n_months": int(mask.sum())}
        for wname, mat in [("EW", ew), ("VW", vw)]:
            sp_pct, t_nw, n = spread_alpha(mat[N_DECILES][mask], mat[1][mask],
                                           ff, FF3, NW_LAGS)
            _, t_iid, _ = spread_alpha(mat[N_DECILES][mask], mat[1][mask], ff, FF3, 0)
            row[wname] = {"spread_10_1": float(sp_pct),
                          "spread_t_nw": float(t_nw), "spread_t_iid": float(t_iid)}
        secF[label] = row
    R["section_F"] = secF

    # =========================================================================
    # PANEL A — formation-period ASSETG (== Table I; the sort variable)
    # =========================================================================
    cs = form.groupby(["june_year", "decile"])["ASSETG"].median()
    tsavg = cs.groupby("decile").mean()
    yearly_spread = (cs.unstack("decile")[N_DECILES]
                     - cs.unstack("decile")[1])
    pa_spread = float(tsavg[N_DECILES] - tsavg[1])
    pa_t = float(yearly_spread.mean() / (yearly_spread.std(ddof=1) / np.sqrt(n_years)))
    R["panel_A"] = {"ASSETG_year1_spread": pa_spread, "ASSETG_year1_t": pa_t,
                    "D1": float(tsavg[1]), "D10": float(tsavg[N_DECILES])}

    # =========================================================================
    # SECTION E — event-time Year 1..5 buy-and-hold (NOT YET COMPUTED)
    # =========================================================================
    R["section_E"] = {
        "status": "not_yet_computed",
        "note": ("Years 2-5 buy-and-hold requires the fixed formation-decile "
                 "membership's monthly returns through Jun 2007 (cohort 2002 Year 5), "
                 "which lies OUTSIDE the foundation window (universe_monthly.sql ends "
                 "2003-12) and needs a fresh CRSP msf pull with consistent delisting "
                 "adjustment. Skipped per task priority (A-D + F first)."),
    }

    # =========================================================================
    # markdown
    # =========================================================================
    write_markdown(R, ew, vw, ew_ann, vw_ann)

    # =========================================================================
    # evaluate vs T2 metrics
    # =========================================================================
    eval_details, tally = evaluate(R, ew_ann, vw_ann)

    # persist eval json
    eval_out = {"results": R,
                "evaluation": [{"metric": n, "paper": p, "ours": o,
                                "status": s, "reason": r}
                               for n, p, o, s, r in eval_details],
                "tally": tally, "n_months": int(n_months), "n_years": int(n_years)}
    with open(RESULTS / "table_2_eval.json", "w") as fh:
        json.dump(eval_out, fh, indent=2, default=float)
    print(f"\nwrote results/table_2_eval.json")

    # =========================================================================
    # plots
    # =========================================================================
    make_plots(ew, vw, ew_ann, vw_ann)

    print("\nDONE.")


# =============================================================================
def write_markdown(R, ew, vw, ew_ann, vw_ann):
    A, B, C, D, F, PA = (R["section_A"], R["section_B"], R["section_C"],
                         R["section_D"], R["section_F"], R["panel_A"])
    L = []
    L.append("# Table II — Asset Growth Decile Portfolio Returns and "
             "Three-Factor Alphas in Event Time\n")
    L.append("Cooper, Gulen, and Schill (2008), *Asset Growth and the Cross-Section "
             "of Stock Returns* (Journal of Finance). Caption (content.md L401): "
             "\"Equal- and value-weighted portfolios are formed based on June(t) asset "
             "growth decile cutoffs. The portfolios are held for 1 year, from July of "
             "year t to June of year t+1, and then rebalanced. ... Panel C.1 reports "
             "three-factor alphas of the equal-weighted portfolios and Panel C.2 reports "
             "three-factor alphas of the value-weighted portfolios for all firms and for "
             "three size-sorted groups.\" The size groups use the 30th and 70th NYSE "
             "market-equity percentiles in June of year t (Assumption 4).\n")
    L.append("**Conventions.** Year-1 = the full 420-month series (every month is in the "
             "Year-1 holding period of its formation_year; annual July-t rebalance). "
             "Spread = D10 − D1 (high minus low, reported negative). EW = within-(month,"
             "decile) mean of delisting-adjusted returns; VW = Σ(ret·me_June)/Σ(me_June) "
             "using the FIXED June-t formation market equity as the weight (paper rule "
             "`sample_me_timing`; contemporaneous monthly me biases VW up ~1.3pp/mo). "
             "Three-factor alpha = intercept of (ret − rf) on (Mkt-RF, SMB, HML) ×100 "
             "(%/month); factors from `ff.four_factor_monthly` (Assumption 5). Spread alpha "
             "= intercept of the D10−D1 return (zero-investment, rf NOT subtracted) on the "
             "factors = α_D10 − α_D1. t-stats are Newey-West (HAC), n_lags=3, on the spread "
             "series (raw) / on the spread-regression intercept (alpha); the paper's "
             "extreme-decile alpha t uses a GMM/delta-method HAC joint test (footnote 12, "
             "L1574) — the NW spread t is the accepted approximation. iid (n_lags=0) t-stats "
             "are shown in parentheses.\n")

    # Panel A
    L.append("## Panel A — Formation-Period Asset Growth (the sort variable; == Table I)\n")
    L.append(f"ASSETG spread (D10−D1), time-series avg of yearly cross-sectional medians: "
             f"**{PA['ASSETG_year1_spread']:.4f}** (t = {PA['ASSETG_year1_t']:.2f}); "
             f"D1 = {PA['D1']:.4f}, D10 = {PA['D10']:.4f}. Paper: spread 1.0471 (t 15.60). "
             f"Upper-tail vintage gap (Assumption 7) -> Tier 2, as in Table I.\n")

    # Panel B Year-1 raw returns
    L.append("## Panel B — Year-1 Average Monthly Raw Returns (%/month)\n")
    hdr = "| Portfolio | " + " | ".join(f"D{d}" for d in range(1, 11)) + " | Spread(10-1) | t(NW3) | t(iid) |"
    sep = "|---|" + "---|" * 13
    L.append(hdr); L.append(sep)
    for wn in ["EW", "VW"]:
        cells = " | ".join(f"{A[wn]['deciles'][f'D{d}']:.2f}" for d in range(1, 11))
        L.append(f"| {wn} | {cells} | {A[wn]['spread_10_1']:.2f} | "
                 f"{A[wn]['spread_t_nw']:.2f} | {A[wn]['spread_t_iid']:.2f} |")
    L.append("\nPaper (Panel B Year 1): EW D1=1.99, D10=0.26, spread=−1.73, t=−8.45 "
             "(D2=1.76, D9=0.85); VW D1=1.48, D10=0.43, spread=−1.05, t=−5.04.\n")

    # Section B annual stats
    L.append("## Section B — Annual Year-1 Statistics (35 formation years)\n")
    L.append(f"- Consistency (% of 35 yrs with annual D1 > D10): **EW {B['EW_pct_years_low_beats_high']:.0f}%** "
             f"(paper 91), **VW {B['VW_pct_years_low_beats_high']:.0f}%** (paper 71).")
    L.append(f"- Sharpe of the VW annual spread (D1−D10): **{B['VW_spread_Sharpe_annual']:.3f}** "
             f"(paper 1.07). [EW spread Sharpe {B['EW_spread_Sharpe_annual']:.3f}.]")
    L.append(f"- Annualized high-growth (D10) return: **VW {B['VW_D10_annualized']:.1f}%/yr** "
             f"(paper 5.2), **EW {B['EW_D10_annualized']:.1f}%/yr** (paper 3.1) — "
             f"(1+mean_monthly)^12−1.")
    L.append(f"- Annualized low-growth (D1) return: **VW {B['VW_D1_annualized']:.1f}%/yr** "
             f"(paper ≈18), EW {B['EW_D1_annualized']:.1f}%/yr.")
    L.append(f"- (Mean of the 35 annual returns: VW D1 {B['VW_D1_annual_mean']:.1f} / D10 "
             f"{B['VW_D10_annual_mean']:.1f}; EW D1 {B['EW_D1_annual_mean']:.1f} / D10 "
             f"{B['EW_D10_annual_mean']:.1f} %/yr.)\n")

    # Panel C all firms
    L.append("## Panel C — Year-1 Three-Factor Alphas (%/month), All Firms\n")
    hdr = "| Weighting | " + " | ".join(f"D{d}" for d in range(1, 11)) + " | Spread(10-1) | t(NW3) | t(iid) |"
    L.append(hdr); L.append(sep)
    for wn in ["EW", "VW"]:
        blk = C[f"{wn}_all"]
        cells = " | ".join(f"{blk[f'D{d}']:.2f}" for d in range(1, 11))
        L.append(f"| {wn} | {cells} | {blk['spread_10_1']:.2f} | "
                 f"{blk['spread_t_nw']:.2f} | {blk['spread_t_iid']:.2f} |")
    L.append("\nPaper: EW D1 α=0.76 (t 3.28), D10=−0.87 (t −5.81), spread=−1.63 (t −8.33); "
             "VW D1=0.24 (1.65), D10=−0.46 (−3.74), spread=−0.70 (−3.84).\n")

    # Panel C size groups
    L.append("## Panel C — Three-Factor Spread Alphas by Size Group (D10−D1, %/month)\n")
    L.append("| Size | EW spread | EW t(NW3) | VW spread | VW t(NW3) |")
    L.append("|---|---|---|---|---|")
    for sg in SIZE_GROUPS:
        e = C["size_groups"][sg]["EW"]; v = C["size_groups"][sg]["VW"]
        L.append(f"| {sg} | {e['spread_10_1']:.2f} | {e['spread_t_nw']:.2f} | "
                 f"{v['spread_10_1']:.2f} | {v['spread_t_nw']:.2f} |")
    L.append("\nPaper: EW small −1.77 (−9.12), medium −0.60 (−2.85), large −0.86 (−3.12); "
             "VW small −1.14 (−6.46), medium −0.55 (−2.45), large −0.81 (−2.91).\n")

    # Section D 4-factor
    L.append("## Section D — Carhart Four-Factor Robustness (all-firm D10−D1 spread)\n")
    L.append("| Weighting | Spread α | t(NW3) | t(iid) |")
    L.append("|---|---|---|---|")
    for wn in ["EW", "VW"]:
        L.append(f"| {wn} | {D[wn]['spread_10_1']:.2f} | {D[wn]['spread_t_nw']:.2f} | "
                 f"{D[wn]['spread_t_iid']:.2f} |")
    L.append("\nPaper: EW −1.48 (t −7.45); VW −0.60 (t −2.84).\n")

    # Section F subperiods
    L.append("## Section F (Panel D) — Decade-Subperiod Three-Factor Spread Alphas "
             "(D10−D1, %/month; split on formation_year)\n")
    L.append("| Subperiod | n months | EW spread | EW t(NW3) | VW spread | VW t(NW3) |")
    L.append("|---|---|---|---|---|---|")
    for label, _, _ in SUBPERIODS:
        r = F[label]
        L.append(f"| {label} | {r['n_months']} | {r['EW']['spread_10_1']:.2f} | "
                 f"{r['EW']['spread_t_nw']:.2f} | {r['VW']['spread_10_1']:.2f} | "
                 f"{r['VW']['spread_t_nw']:.2f} |")
    L.append("\nPaper: all subperiod spreads negative & significant except VW 1968–1980 "
             "= −0.35 (t −1.69).\n")

    # Section E
    L.append("## Section E — Event-Time Year 1..5 Buy-and-Hold (NOT YET COMPUTED)\n")
    L.append(R["section_E"]["note"] + " Metric `EW_cumulative_Y1_5_spread` (paper −87.99%) "
             "is evaluated as SKIP.\n")

    (RESULTS / "table_2.md").write_text("\n".join(L))
    print("wrote results/table_2.md")


# =============================================================================
def evaluate(R, ew_ann, vw_ann):
    A, B, C, D, F, PA = (R["section_A"], R["section_B"], R["section_C"],
                         R["section_D"], R["section_F"], R["panel_A"])
    metrics = json.loads((PREP / "tables_to_replicate.json").read_text())
    t2 = next(t for t in metrics["tables"] if t["id"] == "T2")["metrics"]

    def ours(name):
        if name == "PanelA_ASSETG_year1_spread":
            return PA["ASSETG_year1_spread"]
        if name == "PanelA_ASSETG_year1_t":
            return PA["ASSETG_year1_t"]
        if name.startswith("EW_Y1_") or name.startswith("VW_Y1_"):
            wn = "EW" if name.startswith("EW") else "VW"
            blk = A[wn]
            if name.endswith("_D1_ret"):
                return blk["deciles"]["D1"]
            if name.endswith("_D10_ret"):
                return blk["deciles"]["D10"]
            if name.endswith("_spread_10_1"):
                return blk["spread_10_1"]
            if name.endswith("_spread_t"):
                return blk["spread_t_nw"]
        if name.startswith("EW_alpha_all") or name.startswith("VW_alpha_all"):
            wn = "EW" if name.startswith("EW") else "VW"
            blk = C[f"{wn}_all"]
            if name.endswith("_low"):
                return blk["D1"]
            if name.endswith("_high"):
                return blk["D10"]
            if name.endswith("_spread_t"):
                return blk["spread_t_nw"]
            if name.endswith("_spread"):
                return blk["spread_10_1"]
        for sg in SIZE_GROUPS:
            tag = f"alpha_{sg}_spread"
            if name.startswith("EW_") and name == f"EW_{tag}":
                return C["size_groups"][sg]["EW"]["spread_10_1"]
            if name.startswith("VW_") and name == f"VW_{tag}":
                return C["size_groups"][sg]["VW"]["spread_10_1"]
        if name == "EW_4factor_Y1_spread":
            return D["EW"]["spread_10_1"]
        if name == "EW_4factor_Y1_spread_t":
            return D["EW"]["spread_t_nw"]
        if name == "VW_4factor_Y1_spread":
            return D["VW"]["spread_10_1"]
        if name == "VW_4factor_Y1_spread_t":
            return D["VW"]["spread_t_nw"]
        if name == "VW_spread_Sharpe_annual":
            return B["VW_spread_Sharpe_annual"]
        if name == "VW_high_growth_annualized_ret":
            return B["VW_D10_annualized"]
        if name == "EW_high_growth_annualized_ret":
            return B["EW_D10_annualized"]
        if name == "EW_pct_years_low_beats_high":
            return B["EW_pct_years_low_beats_high"]
        if name == "VW_pct_years_low_beats_high":
            return B["VW_pct_years_low_beats_high"]
        if name == "VW_alpha_1968_1980_spread":
            return F["1968-1980"]["VW"]["spread_10_1"]
        if name == "VW_alpha_1968_1980_spread_t":
            return F["1968-1980"]["VW"]["spread_t_nw"]
        if name == "EW_cumulative_Y1_5_spread":
            return np.nan    # Section E not yet computed -> SKIP
        return np.nan

    LENIENT_MAG = 0.05
    tally = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "SKIP": 0}
    details = []
    print("\n=== Per-cell evaluation (T2 metrics, primary = Newey-West n_lags=3) ===")
    print(f"{'metric':<32}{'paper':>10}{'ours':>10}{'rel_err':>9}  status  reason")
    for m in t2:
        name, paper, tol = m["name"], float(m["value"]), float(m["tolerance_pct"])
        o = ours(name)
        if o is None or (isinstance(o, float) and np.isnan(o)):
            status, reason, rel = "SKIP", "not computed (Section E)", "   -  "
        else:
            rel_val = abs(o - paper) / abs(paper) if paper != 0 else float("inf")
            rel = f"{rel_val:7.1%}"
            same_sign = (o * paper > 0) or (o == 0 == paper)
            lenient = abs(paper) < LENIENT_MAG
            if rel_val <= tol / 100:
                status, reason = "Tier 1", f"within {tol:.0f}% tol"
            elif same_sign:
                status, reason = "Tier 2", f"sign ok, outside {tol:.0f}% tol ({rel})"
            elif lenient and abs(o) < 0.5:
                status, reason = "Tier 2", f"lenient ~0 target; ours {o:.3f} small"
            else:
                status, reason = "FAIL", f"opposite sign (paper {paper}, ours {o:.4f})"
        tally[status] += 1
        details.append((name, paper, float(o) if not (o is None or (isinstance(o, float) and np.isnan(o))) else np.nan, status, reason))
        os_ = f"{o:.4f}" if not (isinstance(o, float) and np.isnan(o)) else "   -  "
        print(f"{name:<32}{paper:>10.4f}{os_:>10}{rel:>9}  {status:<7} {reason}")
    print(f"\nTALLY: Tier 1 = {tally['Tier 1']}, Tier 2 = {tally['Tier 2']}, "
          f"FAIL = {tally['FAIL']}, SKIP = {tally['SKIP']}  (of {len(t2)} metrics)")
    return details, tally


# =============================================================================
def make_plots(ew, vw, ew_ann, vw_ann):
    deciles = list(range(1, N_DECILES + 1))

    # (1) grouped bar: EW & VW Year-1 monthly returns by decile
    ew_vals = [float(ew[d].mean() * 100) for d in deciles]
    vw_vals = [float(vw[d].mean() * 100) for d in deciles]
    x = np.arange(len(deciles)); wdt = 0.4
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.bar(x - wdt / 2, ew_vals, wdt, label="EW", color="#4C72B0")
    ax.bar(x + wdt / 2, vw_vals, wdt, label="VW", color="#C44E52")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x); ax.set_xticklabels([str(d) for d in deciles])
    ax.set_xlabel("ASSETG decile (1 = low growth ... 10 = high growth)")
    ax.set_ylabel("Year-1 avg monthly return (%/month)")
    ax.set_title("Table II Panel B: Year-1 raw returns decline monotonically D1 -> D10")
    ax.legend(); fig.tight_layout()
    fig.savefig(RESULTS / "table2_year1_decile_returns.png", dpi=150)
    plt.close(fig); print("wrote results/table2_year1_decile_returns.png")

    # (2) cumulative P&L of the monthly D1-D10 spread (EW & VW), full sample
    pnl = pd.DataFrame({
        "month": ew.index.to_timestamp(),
        "spread_D1_mD10_EW": (ew[1] - ew[N_DECILES]).values,
        "spread_D1_mD10_VW": (vw[1] - vw[N_DECILES]).values,
    })
    plot_cumulative_returns(
        pnl, index_col_name="month",
        ret_col_lst=["spread_D1_mD10_EW", "spread_D1_mD10_VW"],
        title="Table II: cumulative P&L of the monthly low-minus-high (D1-D10) spread",
        save_to=RESULTS / "table2_spread_pnl.png")
    print("wrote results/table2_spread_pnl.png")

    # (3) 35 annual Year-1 spread values (D1-D10, EW & VW) — Figure 3 analog
    yrs = ew_ann.index.astype(int)
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.plot(yrs, ew_ann[1] - ew_ann[N_DECILES], "o-", color="#4C72B0", label="EW D1-D10")
    ax.plot(yrs, vw_ann[1] - vw_ann[N_DECILES], "s-", color="#C44E52", label="VW D1-D10")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Formation year"); ax.set_ylabel("Annual Year-1 spread (low - high)")
    ax.set_title("Table II / Figure 3: annual Year-1 D1-D10 spread by formation year")
    ax.legend(); fig.tight_layout()
    fig.savefig(RESULTS / "table2_annual_spread.png", dpi=150)
    plt.close(fig); print("wrote results/table2_annual_spread.png")


if __name__ == "__main__":
    main()
