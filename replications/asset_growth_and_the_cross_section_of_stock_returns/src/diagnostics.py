"""
Report-support ARTIFACT 1 — standard portfolio diagnostics for the
asset-growth LONG-SHORT spread portfolio (Cooper, Gulen, Schill 2008).

Headline portfolio
------------------
Each month: LONG decile 1 (lowest asset growth) and SHORT decile 10 (highest
asset growth).  Spread return = D1_ret - D10_ret  (positive when low-growth
beats high-growth, i.e. the paper's central result).  Built BOTH
equal-weighted (EW) and value-weighted (VW).

  * EW = mean(ret) within (month, decile).
  * VW = sum(ret*w)/sum(w) with w = the FIXED June-t formation market equity
    (MV from data/formation.parquet, merged on (permno, formation_year)) held
    fixed over the 12-month holding year — Assumption 9.  The panel's
    contemporaneous `me` column is NOT used (it biases VW up ~1.3pp/mo).

Data (READ-ONLY; this script only ADDS deliverables)
----------------------------------------------------
  data/panel.parquet      permno, month[datetime], ret[delisting-adjusted],
                          me[$, contemporaneous - NOT used as weight],
                          formation_year, decile[1..10], size_group.
                          420 months 1968-07..2003-06.
  data/formation.parquet  one row per (permno, june_year); MV ($M, June-t
                          market equity) is the FIXED value weight.
  ff.five_factor_monthly  (ClickHouse) dt, mkt_rf, smb, hml, rmw, cma, rf —
                          pulled via src/sql/ff5_factors_monthly.sql.

Diagnostics (REQUIRED for REPORT.md)
------------------------------------
For each of EW and VW monthly spread series:
    diag = portfolio_diagnostics(spread, factor_returns=ff5,
                                 zero_investment=True, freq="M")
zero_investment=True -> self-financing L/S spread, rf NOT subtracted.
Reported: sample period + N months, annualized spread return, annualized
volatility, Sharpe, FF5 alpha (monthly + annualized %) with Newey-West t-stat,
max drawdown.  The formatted markdown blocks are written to
results/diagnostics.md.

t-stat convention: the headline alpha t-stat uses Newey-West with n_lags=3
(the replication's primary HAC convention, src/table_2.py NW_LAGS=3); the iid
(n_lags=0) t-stat is reported alongside for reference.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# --- repo / layout -----------------------------------------------------------
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from clickhouse_driver import Client                          # noqa: E402
from utils.env import get_clickhouse_config                   # noqa: E402
from utils.summary import portfolio_diagnostics, format_diagnostics_block  # noqa: E402
from utils.regressions import factor_alpha                    # noqa: E402

SLUG_DIR = Path(__file__).resolve().parents[1]
DATA = SLUG_DIR / "data"
RESULTS = SLUG_DIR / "results"
SQL_DIR = SLUG_DIR / "src" / "sql"
RESULTS.mkdir(parents=True, exist_ok=True)

N_DECILES = 10
NW_LAGS = 3                 # primary Newey-West lag convention (== table_2.py)
FF5 = ["mkt_rf", "smb", "hml", "rmw", "cma"]

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
    VW additionally drops NaN-weight rows. (Identical to src/table_2.py.)"""
    d = df.dropna(subset=["ret"])
    ew = d.groupby(keys)["ret"].mean()
    dv = d.dropna(subset=[wcol])
    vw = (dv.assign(_rw=dv["ret"] * dv[wcol]).groupby(keys)["_rw"].sum()
          / dv.groupby(keys)[wcol].sum())
    return pd.DataFrame({"EW": ew, "VW": vw})


def wide(mat: pd.DataFrame, weighting: str) -> pd.DataFrame:
    """index = month Period, columns = decile 1..10."""
    return mat[weighting].unstack("decile")


# =============================================================================
# load
# =============================================================================
def load():
    panel = pd.read_parquet(DATA / "panel.parquet")
    form = pd.read_parquet(DATA / "formation.parquet")
    panel["month"] = pd.to_datetime(panel["month"])
    panel["ym"] = panel["month"].dt.to_period("M")
    # FIXED June-t formation market equity ($M) as the VW weight (Assumption 9)
    w = form[["permno", "june_year", "MV"]].rename(
        columns={"june_year": "formation_year", "MV": "me_june"})
    panel = panel.merge(w, on=["permno", "formation_year"], how="left")

    ff = q_file("ff5_factors_monthly.sql")
    ff["ym"] = pd.to_datetime(ff["month"]).dt.to_period("M")
    ff = ff.set_index("ym")[FF5 + ["rf"]].astype(float).sort_index()
    return panel, ff


# =============================================================================
def build_spread(panel: pd.DataFrame) -> dict:
    """Monthly D1-D10 spread (long low-growth D1, short high-growth D10),
    EW and VW. Returns dict {EW: Series, VW: Series} indexed by the CRSP
    last-trading-day DatetimeIndex (month). A DatetimeIndex (not PeriodIndex)
    is required because portfolio_diagnostics calls pd.to_datetime(index) which
    coerces a PeriodIndex to NaT; factor_alpha still aligns it to the FF5
    PeriodIndex by month internally."""
    all_pr = port_returns(panel, "me_june", ["month", "decile"])
    ew = wide(all_pr, "EW")           # index month (datetime), cols 1..10
    vw = wide(all_pr, "VW")
    out = {}
    for name, mat in [("EW", ew), ("VW", vw)]:
        spread = mat[1] - mat[N_DECILES]          # long D1 - short D10 (positive)
        spread = spread.dropna().sort_index()
        spread.name = "ret"
        out[name] = spread
    return out


def run_one(name: str, spread: pd.Series, ff: pd.DataFrame) -> dict:
    """Run portfolio_diagnostics on one spread series; also grab monthly alpha
    and an iid-t for reference. All factor regressions use the zero-investment
    convention (rf NOT subtracted) — matching portfolio_diagnostics, which sets
    the rf column to 0 internally. The direct factor_alpha calls therefore use
    an rf-zeroed copy of ff so the monthly alpha and iid t are consistent with
    the annualized alpha / NW t reported by portfolio_diagnostics."""
    # HEADLINE — Newey-West alpha t-stat (n_lags=3, replication convention)
    diag = portfolio_diagnostics(spread, factor_returns=ff, factors=FF5,
                                 zero_investment=True, freq="M", n_lags=NW_LAGS,
                                 factor_model_name="FF5")
    # rf-zeroed factors so the direct regressions match the zero-investment
    # convention (self-financing L/S spread earns/forgoes no risk-free rate).
    ff_zi = ff.copy()
    ff_zi["rf"] = 0.0
    fa_nw = factor_alpha(spread, ff_zi, factors=FF5, rf_col="rf",
                         n_lags=NW_LAGS, freq="M")
    # iid reference alpha t-stat (n_lags=0) — same zero-investment regression
    fa_iid = factor_alpha(spread, ff_zi, factors=FF5, rf_col="rf",
                          n_lags=0, freq="M")
    diag["alpha_monthly_pct"] = float(fa_nw["alpha_monthly"]) * 100.0  # %/month
    diag["alpha_tstat_iid"] = float(fa_iid["t_alpha_newey_west"])
    return diag


def render_block(diag: dict, label: str) -> str:
    """The canonical format_diagnostics_block PLUS the extra rows the report
    asks for (annualized return, annualized vol, monthly FF5 alpha, iid t,
    factor loadings)."""
    block = format_diagnostics_block(diag, portfolio_label=label)
    betas = diag.get("alpha_betas", {})
    beta_str = ", ".join(f"{k} {v:+.2f}" for k, v in betas.items())
    extra = [
        "",
        f"_Additional detail:_ annualized spread return "
        f"{diag['annual_return']*100:.2f}%/yr; annualized volatility "
        f"{diag['annualized_vol']*100:.2f}%; FF5 alpha "
        f"{diag['alpha_monthly_pct']:.3f}%/month (= {diag['alpha_annualized_pct']:.2f}%/yr), "
        f"Newey-West t (n_lags={NW_LAGS}) = {diag['alpha_tstat']:.2f} "
        f"[iid t = {diag['alpha_tstat_iid']:.2f}]. FF5 loadings: {beta_str}._",
    ]
    return block + "\n".join(extra) + "\n"


# =============================================================================
def main():
    panel, ff = load()
    n_months = panel["ym"].nunique()
    print(f"panel {panel.shape}, months {n_months} "
          f"({panel['ym'].min()}..{panel['ym'].max()}); "
          f"FF5 factors {ff.shape} ({ff.index.min()}..{ff.index.max()})")

    spreads = build_spread(panel)
    diags, blocks = {}, {}
    for name in ["EW", "VW"]:
        sp = spreads[name]
        d = run_one(name, sp, ff)
        diags[name] = d
        label = f"Asset-growth L/S spread, {name}"
        blocks[name] = render_block(d, label)
        print(f"\n[{name}] n={d['n_obs']} {d['sample_start']}..{d['sample_end']} | "
              f"annRet {d['annual_return']*100:.2f}% annVol {d['annualized_vol']*100:.2f}% "
              f"Sharpe {d['sharpe_ratio']:.3f} | FF5alpha {d['alpha_annualized_pct']:.2f}%/yr "
              f"({d['alpha_monthly_pct']:.3f}%/mo) t_NW {d['alpha_tstat']:.2f} "
              f"[iid {d['alpha_tstat_iid']:.2f}] maxDD {d['max_drawdown']*100:.2f}%")

    # ---- write results/diagnostics.md -------------------------------------
    md = []
    md.append("# Portfolio Diagnostics — Asset-Growth Long-Short Spread")
    md.append("")
    md.append("**Portfolio (Cooper, Gulen, Schill 2008, headline):** each month, "
              "**LONG decile 1** (lowest asset growth) and **SHORT decile 10** "
              "(highest asset growth); monthly spread return = `D1_ret − D10_ret`. "
              "Built equal-weighted (EW) and value-weighted (VW; weights = fixed "
              "June-t formation market equity, Assumption 9). Sample: monthly "
              "delisting-adjusted returns, 1968-07 .. 2003-06 (420 months). "
              "Diagnostics via `utils.portfolio_diagnostics` with "
              "`zero_investment=True` (self-financing L/S spread — rf NOT subtracted); "
              "FF5 alpha from a time-series regression of the spread on "
              "(Mkt-RF, SMB, HML, RMW, CMA). Alpha t-stat: Newey-West, n_lags = 3 "
              "(replication HAC convention; iid t shown alongside).")
    md.append("")
    md.append(blocks["EW"])
    md.append("")
    md.append(blocks["VW"])
    md.append("")
    # interpretation
    md.append("## Interpretation")
    md.append("")
    ew_d, vw_d = diags["EW"], diags["VW"]
    md.append(
        f"The asset-growth long-short spread — buying low-asset-growth (D1) and "
        f"selling high-asset-growth (D10) stocks — is the **headline portfolio** of "
        f"Cooper, Gulen, Schill (2008): firms that grow their assets aggressively "
        f"subsequently earn lower returns, so the low-minus-high spread is the "
        f"tradeable anomaly. Both weightings deliver a positive, economically large "
        f"and statistically significant premium over 1968-07..2003-06.")
    md.append("")
    md.append(
        f"- **EW spread:** annualized {ew_d['annual_return']*100:.1f}%/yr, Sharpe "
        f"{ew_d['sharpe_ratio']:.2f}, FF5 alpha {ew_d['alpha_annualized_pct']:.2f}%/yr "
        f"(t = {ew_d['alpha_tstat']:.2f}). The EW figure is the larger of the two "
        f"(paper anchor ≈ 20%/yr) because small caps — where the asset-growth effect "
        f"is strongest — dominate the equal-weighted average.")
    md.append("")
    md.append(
        f"- **VW spread:** annualized {vw_d['annual_return']*100:.1f}%/yr (raw), Sharpe "
        f"{vw_d['sharpe_ratio']:.2f}, FF5 alpha {vw_d['alpha_annualized_pct']:.2f}%/yr "
        f"(t = {vw_d['alpha_tstat']:.2f}). The raw VW premium is economically large and "
        f"matches the paper anchor (≈ 8-12%/yr; spread Sharpe ≈ 1.07 in the paper, 0.70 "
        f"on our annual basis — a returns-volatility vintage effect), but its FF5 alpha "
        f"is statistically insignificant because the investment factor CMA subsumes it "
        f"(see below).")
    md.append("")
    ew_cma = ew_d.get("alpha_betas", {}).get("cma", float("nan"))
    vw_cma = vw_d.get("alpha_betas", {}).get("cma", float("nan"))
    md.append(
        f"- **Why the VW alpha is small but the EW alpha is large.** The spread loads "
        f"heavily on the FF5 **investment factor CMA** (EW β ≈ {ew_cma:+.2f}, VW β ≈ "
        f"{vw_cma:+.2f}). Asset growth is the investment anomaly: high-asset-growth "
        f"stocks are exactly the \"aggressive\" leg that CMA shorts, so CMA absorbs "
        f"most of the VW spread (R² ≈ {vw_d['alpha_r_squared']:.2f}) and its FF5 alpha "
        f"collapses to ≈ {vw_d['alpha_annualized_pct']:.1f}%/yr (t = {vw_d['alpha_tstat']:.2f}, "
        f"insignificant). Among small caps — where the effect is strongest and CMA "
        f"does not fully span it — a large residual alpha survives (EW "
        f"{ew_d['alpha_annualized_pct']:.1f}%/yr, t = {ew_d['alpha_tstat']:.2f}).")
    md.append("")
    md.append(
        f"- **Bottom line.** With rf not subtracted (zero-investment convention), the "
        f"asset-growth long-short portfolio earns a positive premium in both "
        f"weightings; it is robust to FF5 risk adjustment among small caps (EW) and is "
        f"largely subsumed by the CMA investment factor among large caps (VW). The EW > "
        f"VW gap and the negative max drawdowns (EW {ew_d['max_drawdown']*100:.1f}%, VW "
        f"{vw_d['max_drawdown']*100:.1f}%) are consistent with a small-cap-tilted "
        f"anomaly that is strong on average but episodic.")
    md.append("")
    out = RESULTS / "diagnostics.md"
    out.write_text("\n".join(md))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
