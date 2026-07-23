"""
Replication of Frazzini & Pedersen (2014) "Betting Against Beta" — Table 3.
=============================================================================
US-equity beta-sorted decile portfolios + the BAB factor.

Reads the analysis-ready panel built by ``main.py`` (``data/panel.parquet``,
columns [permno, month, ret, beta, me, log_me]) and produces Table 3 of the
paper:

  * 10 beta-sorted decile portfolios (P1 = lowest beta .. P10 = highest),
    equal-weighted, rebalanced monthly, sorted on the PRIOR month's beta (the
    panel's ``beta`` is already lagged by construction — see Assumption 3).
  * The BAB factor: a self-financing, zero-beta portfolio that is long the
    rank-weighted low-beta portfolio and short the rank-weighted high-beta
    portfolio, each rescaled to unit beta at formation (paper §3.2).

For each portfolio we report:
  Excess return (monthly %, mean of monthly excess returns)
  CAPM / FF3 / Carhart-4 alphas (monthly %, time-series intercepts)
  Beta (ex ante)  = mean formation beta of the portfolio
  Beta (realized) = realized market loading from the CAPM time-series regression
  Volatility      = annualized std of monthly returns (std * sqrt(12), %)
  Sharpe ratio    = annualized (mean_monthly / std_monthly) * sqrt(12)

Outputs
-------
results/table_3.md       — Table 3 in the paper's format + validation vs paper
results/decile_returns.png — excess return & Sharpe by decile (bar charts)
results/bab_cumulative.png — cumulative BAB factor return over time

Units / conventions
-------------------
* FF factors and RF come from ``ff.four_factor_monthly``. This ClickHouse
  vintage stores them in DECIMAL (verified live: mkt_rf median |x| ~ 0.03,
  rf median ~ 0.0022), NOT percent as the task spec assumed. The loader
  auto-detects the scale at runtime and converts only if the data is in
  percent. CRSP ``ret`` is already decimal, so excess = ret - rf directly.
* Returns & alphas are reported in MONTHLY PERCENT (decimal x 100).
* Volatilities & Sharpe ratios are ANNUALIZED.

Assumptions implemented (documented in preparations/assumptions.md)
-------------------------------------------------------------------
* Breakpoints use ALL stocks (the panel has no exchcd). The paper uses NYSE
  breakpoints; with ~2,400+ stocks/month the all-stock approximation is close.
  (Assumption 14 — flagged for the Replicator.)
* 5-factor alpha (Pastor-Stambaugh liquidity) is skipped: PS factor is not in
  ClickHouse and covers only 1968-2011. (Assumption 2.)
* Monthly returns are raw CRSP msf.ret; delisting returns are NOT in the panel
  (pipeline flag). This can bias high-beta decile returns slightly upward.

Usage
-----
    uv run python src/table_3.py
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Make the script runnable from any cwd / invocation style: pin the repo root
# (3 levels up from replications/<slug>/src/) on sys.path so `import utils`
# resolves, and pin REPLICATIONS_PATH so paper_layout() finds this replication
# deterministically (utils.env falls back to cwd/replications otherwise).
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
os.environ.setdefault("REPLICATIONS_PATH", str(_REPO_ROOT / "replications"))

import matplotlib
matplotlib.use("Agg")                       # headless — must be first mpl import
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from clickhouse_driver import Client

from utils.env import get_clickhouse_config
from utils.paths import paper_layout
from utils.quantile import assign_quantiles
from utils.portfolio import bin_returns
from utils.regressions import factor_alpha
from utils.metrics import performance_metrics
from utils.plot import plot_cumulative_returns

# ────────────────────────────────────────────────────────────────────────────
# Layout & configuration
# ────────────────────────────────────────────────────────────────────────────
SLUG = "betting_against_beta"
LAYOUT = paper_layout(SLUG)
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")
_CFG = get_clickhouse_config()

N_DECILES = 10           # [sort_decile_nyse_ew] ten decile portfolios
NW_LAGS = 6             # Newey-West lags for the supplementary HAC alpha t-stat

# Paper validation values (Table 3, US equities). Returns/alphas in monthly %,
# volatility in annualized %, Sharpe annualized, betas dimensionless.
PAPER = {
    "P1":  dict(excess_ret=0.91, capm_alpha=0.52, ff3_alpha=0.40, ff4_alpha=0.40,
                beta_exante=0.64, beta_realized=0.67, vol=15.70, sharpe=0.70),
    "P5":  dict(excess_ret=1.05, capm_alpha=0.34, ff3_alpha=0.13, ff4_alpha=0.18,
                beta_exante=1.05, beta_realized=1.22, vol=25.56, sharpe=0.49),
    "P10": dict(excess_ret=0.97, capm_alpha=-0.10, ff3_alpha=-0.49, ff4_alpha=-0.13,
                beta_exante=1.70, beta_realized=1.85, vol=41.68, sharpe=0.28),
    "BAB": dict(excess_ret=0.70, capm_alpha=0.73, ff3_alpha=0.73, ff4_alpha=0.55,
                beta_exante=0.00, beta_realized=-0.06, vol=10.75, sharpe=0.78),
}
# Per-metric tolerance (%) for pass/fail (from preparations/tables_to_replicate.json).
TOL = {
    "excess_ret": 15.0, "capm_alpha": 20.0, "ff3_alpha": 20.0, "ff4_alpha": 20.0,
    "beta_exante": 10.0, "beta_realized": 10.0, "vol": 10.0, "sharpe": 15.0,
}


# ────────────────────────────────────────────────────────────────────────────
# ClickHouse connection
# ────────────────────────────────────────────────────────────────────────────
def _client() -> Client:
    return Client(
        host=_CFG["host"], port=int(_CFG["port"]),
        user=_CFG["user"], password=_CFG["password"],
        database=_CFG.get("database", "default"),
        settings={"max_execution_time": 300},
    )


def q_file(name: str) -> pd.DataFrame:
    sql = (SQL_DIR / name).read_text().strip().rstrip(";")
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


# ────────────────────────────────────────────────────────────────────────────
# Step 1: Load panel + FF factors, build excess returns
# ────────────────────────────────────────────────────────────────────────────
def load_ff() -> tuple[pd.DataFrame, str]:
    """Load FF 4-factor monthly; return (df indexed by month Period[M], units note).

    Auto-detects whether the factors are stored in percent or decimal and
    normalizes to DECIMAL. ff columns: mkt_rf, smb, hml, mom, rf (+ month idx).
    """
    raw = q_file("ff_factors.sql")
    raw["dt"] = pd.to_datetime(raw["dt"])
    raw["month"] = raw["dt"].dt.to_period("M").dt.to_timestamp()
    fac_cols = ["mkt_rf", "smb", "hml", "mom", "rf"]
    for c in fac_cols:
        raw[c] = pd.to_numeric(raw[c], errors="coerce")

    # Scale auto-detection: monthly market excess is ~0.03 in decimal, ~3 in
    # percent. A median |mkt_rf| above 0.2 implies percent storage.
    med = raw["mkt_rf"].abs().median()
    if med > 0.2:
        raw[fac_cols] = raw[fac_cols] / 100.0
        units = f"PERCENT in source (median |mkt_rf|={med:.3f}) -> divided by 100"
    else:
        units = f"DECIMAL in source (median |mkt_rf|={med:.4f}) -> used as-is"

    ff = raw.set_index(raw["month"].dt.to_period("M"))[fac_cols].sort_index()
    return ff, units


def build_excess(panel: pd.DataFrame, ff: pd.DataFrame) -> pd.DataFrame:
    """Attach rf by month and compute excess_ret = ret - rf. Drop null beta.

    Returns a filtered copy with columns incl. excess_ret, rf, ready for sorts.
    """
    rf_by_month = ff["rf"]                                  # PeriodIndex[M]
    mkey = panel["month"].dt.to_period("M")
    panel = panel.copy()
    panel["rf"] = mkey.map(rf_by_month).to_numpy()
    panel["excess_ret"] = panel["ret"] - panel["rf"]
    before = len(panel)
    df = panel.dropna(subset=["beta", "excess_ret", "ret"]).reset_index(drop=True)
    print(f"  rows: {before:,} -> {len(df):,} after dropping null "
          f"beta/excess_ret/ret ({before - len(df):,} dropped)")
    print(f"  sample months: {df['month'].min().date()} .. {df['month'].max().date()} "
          f"({df['month'].nunique()} months)")
    return df


# ────────────────────────────────────────────────────────────────────────────
# Step 2: Decile portfolio sorts (EW, monthly rebalanced)
# ────────────────────────────────────────────────────────────────────────────
def decile_sort(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Assign deciles on beta within each month; return (df w/ decile, ex-ante beta).

    Breakpoints use ALL stocks in the cross-section (panel has no exchcd) — the
    paper uses NYSE breakpoints (Assumption 14). ``assign_quantiles`` bins on
    beta within each month; since ``beta`` is already the prior-month estimate,
    binning within month t and averaging month-t returns is the no-look-ahead
    calendar-time sort the paper describes.
    """
    df = df.copy()
    df["decile"] = assign_quantiles(
        df, date_col="month", signal_col="beta",
        n_bins=N_DECILES, warn_fallback=False,
    )
    df = df.dropna(subset=["decile"]).reset_index(drop=True)
    df["decile"] = df["decile"].astype(int)

    # ex-ante beta: mean formation beta within (month, decile), then mean over t.
    monthly_beta = df.groupby(["month", "decile"])["beta"].mean()
    beta_exante = monthly_beta.groupby("decile").mean()
    return df, beta_exante


def decile_ew_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly EW excess returns per decile. Returns DataFrame indexed by month
    (Period[M]) with one column per decile (1..10)."""
    br = bin_returns(df, date_col="month", bin_col="decile",
                     ret_col="excess_ret", mcap_col="me")
    piv = br.pivot(index="month", columns="decile", values="EW").sort_index()
    piv.index = piv.index.to_period("M")
    return piv


# ────────────────────────────────────────────────────────────────────────────
# Step 3: BAB factor (rank-weighted, rescaled to unit beta)
# ────────────────────────────────────────────────────────────────────────────
def bab_factor(df: pd.DataFrame) -> pd.DataFrame:
    """Construct the monthly BAB factor return (excess, self-financing, zero-beta).

    Per month (paper §3.2, eqs. for w_L, w_H):
      z_i  = rank(beta_i) across all stocks (ascending); z_bar = mean(z)
      k    = 2 / sum_i |z_i - z_bar|          (normalizer; makes each leg sum to 1)
      w_L  = k * (z_bar - z_i)  for beta_i < median   (low-beta leg, > 0)
      w_H  = k * (z_i - z_bar)  for beta_i > median   (high-beta leg, > 0)
      r_L  = sum w_L * excess_ret ;  beta_L = sum w_L * beta
      r_H  = sum w_H * excess_ret ;  beta_H = sum w_H * beta
      BAB  = (1/beta_L) * r_L - (1/beta_H) * r_H     (both legs -> unit beta)

    Fully vectorized via groupby transforms (no per-month Python loop).
    Returns a DataFrame indexed by month (Period[M]) with columns:
      bab (excess return), rL, rH, bL, bH, wL_sum, wH_sum.
    """
    d = df[["month", "beta", "excess_ret"]].copy()
    d["z"] = d.groupby("month")["beta"].rank(method="average")   # ascending ranks
    d["zbar"] = d.groupby("month")["z"].transform("mean")
    d["med"] = d.groupby("month")["beta"].transform("median")
    d["dev"] = d["z"] - d["zbar"]
    # per-month sum of |z - z_bar|, broadcast back to every row -> normalizer k
    d["k"] = 2.0 / d.groupby("month")["dev"].transform(lambda s: s.abs().sum())

    low = d["beta"] < d["med"]
    high = d["beta"] > d["med"]
    d["wL"] = np.where(low, d["k"] * (d["zbar"] - d["z"]), 0.0)
    d["wH"] = np.where(high, d["k"] * (d["z"] - d["zbar"]), 0.0)
    d["wL_r"] = d["wL"] * d["excess_ret"]
    d["wH_r"] = d["wH"] * d["excess_ret"]
    d["wL_b"] = d["wL"] * d["beta"]
    d["wH_b"] = d["wH"] * d["beta"]

    agg = d.groupby("month").agg(
        rL=("wL_r", "sum"), rH=("wH_r", "sum"),
        bL=("wL_b", "sum"), bH=("wH_b", "sum"),
        wL_sum=("wL", "sum"), wH_sum=("wH", "sum"),
        n=("beta", "size"),
    )
    agg["bab"] = agg["rL"] / agg["bL"] - agg["rH"] / agg["bH"]
    agg.index = agg.index.to_period("M")
    return agg.sort_index()


# ────────────────────────────────────────────────────────────────────────────
# Step 4 & 5: metrics + factor regressions per portfolio
# ────────────────────────────────────────────────────────────────────────────
def _alpha(gross: pd.Series, ff: pd.DataFrame, factors: list[str], n_lags: int) -> dict:
    """Time-series alpha of a portfolio's GROSS returns on `factors`.

    ``factor_alpha`` internally computes y = gross - rf and regresses on the
    factor returns; the intercept is the alpha, the mkt_rf loading is the
    realized beta. n_lags=0 -> standard (iid) t-stat (the paper's convention);
    n_lags>0 -> Newey-West HAC t-stat.
    """
    return factor_alpha(
        portfolio_returns=gross, factor_returns=ff, factors=factors,
        rf_col="rf", n_lags=n_lags, freq="M",
    )


def portfolio_row(label: str, excess: pd.Series, ff: pd.DataFrame,
                  beta_exante: float) -> dict:
    """Compute all Table 3 metrics for one portfolio's monthly excess returns."""
    excess = excess.dropna().sort_index()
    # gross return series = excess + rf (so factor_alpha's internal `- rf`
    # recovers the excess return as the regression dependent variable).
    rf = ff["rf"].reindex(excess.index)
    gross = (excess + rf).dropna()
    excess = excess.reindex(gross.index)

    n = len(excess)
    mean_ex = float(excess.mean())
    std_ex = float(excess.std(ddof=1))
    pm = performance_metrics(excess, freq="M")             # annualized vol/sharpe

    capm0 = _alpha(gross, ff, ["mkt_rf"], 0)
    capmN = _alpha(gross, ff, ["mkt_rf"], NW_LAGS)
    ff3_0 = _alpha(gross, ff, ["mkt_rf", "smb", "hml"], 0)
    ff3_N = _alpha(gross, ff, ["mkt_rf", "smb", "hml"], NW_LAGS)
    ff4_0 = _alpha(gross, ff, ["mkt_rf", "smb", "hml", "mom"], 0)
    ff4_N = _alpha(gross, ff, ["mkt_rf", "smb", "hml", "mom"], NW_LAGS)

    return {
        "label": label,
        "n": n,
        "excess_ret": mean_ex * 100.0,
        "t_excess": mean_ex / (std_ex / np.sqrt(n)),
        "capm_alpha": capm0["alpha_monthly"] * 100.0,
        "capm_t": capm0["t_alpha_newey_west"],          # n_lags=0 -> standard
        "capm_t_nw": capmN["t_alpha_newey_west"],
        "ff3_alpha": ff3_0["alpha_monthly"] * 100.0,
        "ff3_t": ff3_0["t_alpha_newey_west"],
        "ff3_t_nw": ff3_N["t_alpha_newey_west"],
        "ff4_alpha": ff4_0["alpha_monthly"] * 100.0,
        "ff4_t": ff4_0["t_alpha_newey_west"],
        "ff4_t_nw": ff4_N["t_alpha_newey_west"],
        "beta_exante": beta_exante,
        "beta_realized": float(capm0["betas"]["mkt_rf"]),
        "vol": pm["annualized_vol"] * 100.0,
        "sharpe": pm["sharpe_ratio"],
    }


# ────────────────────────────────────────────────────────────────────────────
# Step 6: table output + plots + validation
# ────────────────────────────────────────────────────────────────────────────
def build_table(rows: list[dict]) -> str:
    """Render Table 3 (values + t-stats) as a markdown table."""
    labels = [r["label"] for r in rows]
    by = {r["label"]: r for r in rows}

    def fmt(label_key, r, dec=2):
        v = r[label_key]
        return f"{v:.{dec}f}"

    def trow(t_key, r):
        return f"({r[t_key]:.2f})"

    header = "| Metric | " + " | ".join(labels) + " |"
    sep = "|" + "---|" * (len(labels) + 1)
    lines = [header, sep]

    # metric rows: (display, value_key, t_key or None, decimals)
    specs = [
        ("Excess return",      "excess_ret",    "t_excess", 2),
        ("CAPM alpha",         "capm_alpha",    "capm_t",   2),
        ("3-factor alpha",     "ff3_alpha",     "ff3_t",    2),
        ("4-factor alpha",     "ff4_alpha",     "ff4_t",    2),
        ("Beta (ex ante)",     "beta_exante",   None,       2),
        ("Beta (realized)",    "beta_realized", None,       2),
        ("Volatility",         "vol",           None,       2),
        ("Sharpe ratio",       "sharpe",        None,       2),
    ]
    for disp, key, tkey, dec in specs:
        cells = [fmt(key, by[l], dec) for l in labels]
        lines.append(f"| {disp} | " + " | ".join(cells) + " |")
        if tkey:
            tcells = [trow(tkey, by[l]) for l in labels]
            lines.append(f"| _t-stat_ | " + " | ".join(tcells) + " |")
    return "\n".join(lines)


def validation_block(rows: list[dict]) -> tuple[str, dict]:
    """Compare our cells vs the paper for P1/P5/P10/BAB; return (md, results)."""
    by = {r["label"]: r for r in rows}
    out = []
    out.append("| Portfolio | Metric | Ours | Paper | Tol % | Diff % | Pass |")
    out.append("|---|---|---:|---:|---:|---:|:--:|")
    results = {}
    for label, paper in PAPER.items():
        if label not in by:
            continue
        ours = by[label]
        for metric, pval in paper.items():
            oval = ours[metric]
            tol = TOL.get(metric, 15.0)
            if abs(pval) < 1e-9:                       # e.g. BAB ex-ante beta = 0
                diff_pct = abs(oval - pval)
                passed = abs(oval - pval) <= 0.05      # within 0.05 absolute
                dp = f"{diff_pct:.3f} (abs)"
            else:
                diff_pct = 100.0 * abs(oval - pval) / abs(pval)
                passed = diff_pct <= tol
                dp = f"{diff_pct:.1f}"
            results[(label, metric)] = passed
            out.append(
                f"| {label} | {metric} | {oval:.3f} | {pval:.3f} | "
                f"{tol:.0f} | {dp} | {'PASS' if passed else 'FAIL'} |"
            )
    npass = sum(1 for v in results.values() if v)
    return "\n".join(out), {"n_pass": npass, "n_total": len(results), "cells": results}


def plot_decile_returns(rows: list[dict], save_to: Path) -> None:
    """Two-panel bar chart: annualized excess return & Sharpe by decile."""
    dec_rows = [r for r in rows if r["label"].startswith("P")]
    dec_rows = sorted(dec_rows, key=lambda r: int(r["label"][1:]))
    labels = [r["label"] for r in dec_rows]
    # annualized excess return (%) for visual comparability with Sharpe panel
    ann_excess = [r["excess_ret"] * 12.0 for r in dec_rows]
    sharpe = [r["sharpe"] for r in dec_rows]
    x = np.arange(len(labels))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.bar(x, ann_excess, color="#4C72B0", alpha=0.85)
    ax1.axhline(0, color="k", lw=0.6)
    ax1.set_xticks(x); ax1.set_xticklabels(labels)
    ax1.set_xlabel("Beta decile (P1=low .. P10=high)")
    ax1.set_ylabel("Annualized excess return (%)")
    ax1.set_title("Excess return by beta decile (EW)")
    ax1.grid(True, alpha=0.3)

    ax2.bar(x, sharpe, color="#C44E52", alpha=0.85)
    ax2.axhline(0, color="k", lw=0.6)
    ax2.set_xticks(x); ax2.set_xticklabels(labels)
    ax2.set_xlabel("Beta decile (P1=low .. P10=high)")
    ax2.set_ylabel("Annualized Sharpe ratio")
    ax2.set_title("Sharpe ratio by beta decile (EW)")
    ax2.grid(True, alpha=0.3)

    fig.suptitle("Frazzini-Pedersen (2014) Table 3 — beta-sorted deciles, US equities")
    fig.tight_layout()
    fig.savefig(save_to, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_bab_cumulative(bab: pd.DataFrame, save_to: Path) -> None:
    """Cumulative return of the BAB factor over time."""
    df = bab[["bab"]].copy()
    df["month"] = df.index.to_timestamp()
    df = df.reset_index(drop=True)
    plot_cumulative_returns(
        df[["month", "bab"]], index_col_name="month", ret_col_lst=["bab"],
        title="BAB factor — cumulative return (US equities)", save_to=save_to,
    )


# ────────────────────────────────────────────────────────────────────────────
# main
# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    t0 = time.time()
    print("=" * 72)
    print("Frazzini-Pedersen (2014) 'Betting Against Beta' — Table 3 (US)")
    print("=" * 72)

    print("[1/6] load panel + FF factors ...")
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = pd.to_datetime(panel["month"])
    ff, ff_units = load_ff()
    print(f"      FF factors: {len(ff)} months, {ff.index.min()} .. {ff.index.max()}")
    print(f"      FF units: {ff_units}")

    print("[2/6] excess returns (ret - rf), drop null beta ...")
    df = build_excess(panel, ff)

    print("[3/6] decile sorts (EW, all-stock breakpoints) ...")
    df, beta_exante = decile_sort(df)
    dec_excess = decile_ew_returns(df)
    print(f"      decile EW returns: {dec_excess.shape[0]} months x "
          f"{dec_excess.shape[1]} deciles")
    print("      ex-ante beta by decile:",
          {int(k): round(float(v), 3) for k, v in beta_exante.items()})

    print("[4/6] BAB factor (rank-weighted, unit-beta rescaled) ...")
    bab = bab_factor(df)
    print(f"      BAB months: {len(bab)}; mean leverage long 1/bL="
          f"{(1.0 / bab['bL']).mean():.3f}, short 1/bH={(1.0 / bab['bH']).mean():.3f}")
    print(f"      (paper: long $1.40, short $0.70)")
    print(f"      mean wL_sum={bab['wL_sum'].mean():.4f}, wH_sum={bab['wH_sum'].mean():.4f} "
          f"(each leg should ~= 1)")

    print("[5/6] metrics + factor regressions ...")
    rows = []
    for d in range(1, N_DECILES + 1):
        ex = dec_excess[d]
        rows.append(portfolio_row(f"P{d}", ex, ff, float(beta_exante.loc[d])))
    # BAB: ex-ante beta is exactly 0 by construction (unit-beta long - unit-beta short)
    rows.append(portfolio_row("BAB", bab["bab"], ff, beta_exante=0.0))

    print("[6/6] write table + plots ...")
    table_md = build_table(rows)
    val_md, val = validation_block(rows)

    # NW supplementary block (spec asks for Newey-West; paper uses standard)
    nw_lines = ["| Portfolio | CAPM t(NW) | FF3 t(NW) | FF4 t(NW) |", "|---|---:|---:|---:|"]
    for r in rows:
        if r["label"] not in ("P1", "P5", "P10", "BAB"):
            continue
        nw_lines.append(
            f"| {r['label']} | {r['capm_t_nw']:.2f} | {r['ff3_t_nw']:.2f} | "
            f"{r['ff4_t_nw']:.2f} |"
        )

    n_obs_note = {r["label"]: r["n"] for r in rows}

    doc = f"""# Table 3 — Beta-sorted decile portfolios and BAB factor (US equities)

**Source:** Frazzini & Pedersen (2014), "Betting Against Beta", Table 3.
**Sample:** {df['month'].min().date()} .. {df['month'].max().date()}
({df['month'].nunique()} months; beta-sorted portfolios start when betas become
estimable — first valid beta {df['month'].min().date()}).
**Weighting:** equal-weighted within decile, rebalanced monthly.
**Returns & alphas:** monthly percent. **Volatility & Sharpe:** annualized.

## FF factor units
{ff_units}. CRSP `ret` is decimal, so excess = ret - rf with no extra scaling.

## Table 3

{table_md}

_t-stats below each coefficient are **standard (iid)** time-series t-stats,
matching the paper's convention ("t-statistics are shown below the coefficient
estimates"). The excess-return t-stat uses mean/(std/sqrt(n))._

### Newey-West (HAC, {NW_LAGS} lags) alpha t-stats — supplementary
The paper reports standard t-stats; the task spec requested Newey-West. Both are
provided. NW corrects for autocorrelation and is typically a bit smaller.

{chr(10).join(nw_lines)}

## Validation vs paper (tolerance from tables_to_replicate.json)

{val_md}

**Cells passing: {val['n_pass']} / {val['n_total']}.**

## Observations per portfolio (months with a return)
{ {k: v for k, v in n_obs_note.items() if k in ('P1','P5','P10','BAB')} }

## Key assumptions / limitations (see preparations/assumptions.md)
1. **Breakpoints use ALL stocks**, not NYSE-only (panel has no exchcd). Paper
   uses NYSE breakpoints; with ~2,400+ stocks/month the approximation is close.
2. **5-factor alpha skipped** — Pastor-Stambaugh liquidity factor not in
   ClickHouse (covers 1968-2011 only).
3. **Monthly returns are raw CRSP msf.ret; delisting returns are NOT included**
   (panel pipeline flag). Can bias high-beta decile returns slightly upward.
4. **FF factors are DECIMAL in this ClickHouse vintage** (verified), not percent
   as the task spec assumed — auto-detected at runtime.

---
_Generated by src/table_3.py — runtime {time.time() - t0:.1f}s._
"""

    out_md = LAYOUT.result_path("table_3.md")
    out_md.write_text(doc)
    print(f"      wrote {out_md}")

    plot_decile_returns(rows, LAYOUT.result_path("decile_returns.png"))
    print(f"      wrote {LAYOUT.result_path('decile_returns.png')}")
    plot_bab_cumulative(bab, LAYOUT.result_path("bab_cumulative.png"))
    print(f"      wrote {LAYOUT.result_path('bab_cumulative.png')}")

    # Console summary — headline cells vs paper
    print("\n" + "=" * 72)
    print("SUMMARY — headline cells (ours vs paper)")
    print("=" * 72)
    by = {r["label"]: r for r in rows}
    for label in ("P1", "P5", "P10", "BAB"):
        r = by[label]
        p = PAPER[label]
        print(f"\n{label}:")
        for m in ("excess_ret", "capm_alpha", "ff3_alpha", "ff4_alpha",
                  "beta_exante", "beta_realized", "vol", "sharpe"):
            mark = "OK" if val["cells"].get((label, m), False) else "**OFF**"
            print(f"   {m:16s} ours={r[m]:8.3f}  paper={p[m]:8.3f}  {mark}")
    print(f"\nCells passing: {val['n_pass']}/{val['n_total']}")
    print(f"total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
