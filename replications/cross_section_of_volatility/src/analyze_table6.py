"""
Table VI analysis — Ang, Hodrick, Xing, Zhang (2006), "The Cross-Section
of Volatility and Expected Returns".

Headline idiosyncratic-volatility portfolio sorts:
    Panel A — quintile portfolios sorted on TOTAL volatility (tvol)
    Panel B — quintile portfolios sorted on IDIOSYNCRATIC volatility
              relative to the FF-3 model (ivol)

Strategy (1/0/1):
    At the END of month t, sort all stocks into quintiles on the signal
    computed from month-t daily data (n_obs >= 17); hold the value-weighted
    portfolio for month t+1; rebalance monthly. The panel stores signals
    and returns CONTEMPORANEOUSLY at month t (see assumptions.md A8), so
    the next-month return is attached via an explicit (permno, month+1)
    merge — sort on signal_t, earn ret_{t+1}.

Reported per quintile (time-series averages over 450 holding months,
1963-07 .. 2000-12):
    Mean        mean of monthly VW TOTAL simple returns, percent
    Std. Dev.   std of monthly VW total returns (ddof=1), percent
    % Mkt Share mean monthly share of total (sorted-universe) ME, percent
    Size        mean monthly cross-sectional mean of firm log ME ($M)
    B/M         mean monthly cross-sectional mean of firm book-to-market
    CAPM Alpha  Jensen's alpha (percent/month) of portfolio excess return
                on MKT, Newey-West t-stat with 4 lags
    FF3 Alpha   Jensen's alpha (percent/month) on MKT, SMB, HML, NW(4)
    5-1         Q5 - Q1; NW(4) t-stats for the return spread and for the
                spread-portfolio alphas

Conventions (verified in the data pipeline — see assumptions.md):
    * FF factors are DECIMAL (no /100); final alphas x100 for percent.
    * Breakpoints use ALL stocks (NYSE/AMEX/NASDAQ), simple quintile cuts
      (20/40/60/80 percentiles) — per the task spec.
    * Monthly factors/rf come from ff.four_factor_monthly via
      src/sql/ff_monthly.sql (MKT = mkt_rf is already an excess return).
    * Alpha regression (fixed in outer iteration 2, issue M1): the monthly
      VW TOTAL return series is relabeled from the formation month t to the
      HOLDING month t+1 and regressed on the factors of that same holding
      month. factor_alpha subtracts rf internally, so TOTAL returns are
      passed (a single rf adjustment). The 5-1 spread is zero-investment
      (no rf subtraction). Sanity gate: market-cap-weighted average market
      beta across quintiles ~ 1.0 (betas ~0 would flag broken alignment).

Outputs:
    results/table_6.md
    results/ivol_quintile_returns.png
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from clickhouse_driver import Client

from utils.env import get_clickhouse_config, load_project_env
from utils.paths import paper_layout
from utils.quantile import assign_quantiles
from utils.metrics import tstat_newey_west
from utils.regressions import factor_alpha

# ── paths / env ─────────────────────────────────────────────────────
load_project_env()
SLUG = "cross_section_of_volatility"
LAYOUT = paper_layout(SLUG)
SQL_DIR = LAYOUT.src_path("sql")
CFG = get_clickhouse_config()

NW_LAGS = 4  # Newey-West lags for alpha / spread t-stats (task spec)

# Paper values (AHXZ 2006 Table VI) for comparison
PAPER = {
    "tvol": {  # Panel A
        "Mean":   [1.06, 1.15, 1.22, 0.99, 0.09, -0.97],
        "Std":    [3.71, 4.48, 5.63, 7.15, 8.30, None],
        "CAPM":   [0.14, 0.13, 0.07, -0.28, -1.21, -1.35],
        "FF3":    [0.03, 0.08, 0.12, -0.17, -1.16, -1.19],
    },
    "ivol": {  # Panel B
        "Mean":   [1.04, 1.16, 1.20, 0.87, -0.02, -1.06],
        "Std":    [3.83, 4.74, 5.85, 7.13, 8.16, None],
        "CAPM":   [0.11, 0.11, 0.04, -0.38, -1.27, -1.38],
        "FF3":    [0.04, 0.09, 0.08, -0.32, -1.27, -1.31],
    },
}


# ── ClickHouse helper ───────────────────────────────────────────────
def load_ff_monthly() -> pd.DataFrame:
    """Monthly FF4 factors + rf (decimal) from ff.four_factor_monthly."""
    sql = (SQL_DIR / "ff_monthly.sql").read_text()
    c = Client(
        host=CFG["host"], port=int(CFG["port"]),
        user=CFG["user"], password=CFG["password"],
        settings={"max_execution_time": 60},
    )
    data, cols = c.execute(sql, with_column_types=True)
    ff = pd.DataFrame(data, columns=[x[0] for x in cols])
    ff["month"] = pd.to_datetime(ff["month"])
    return ff.set_index("month").sort_index()


# ── portfolio formation ─────────────────────────────────────────────
def attach_next_month_return(panel: pd.DataFrame) -> pd.DataFrame:
    """Pair signal at month t with the stock's return in month t+1
    (explicit calendar-month merge — no per-stock shift, so a trading
    gap can never pair signal_t with ret_{t+k}, k>1).

    Row (permno, month=t) gets ret_next = that stock's panel return in
    month t+1: merge the row's holding month (t+1) onto the raw return
    month (which IS the calendar month the return was realized)."""
    nxt = panel[["permno", "month", "ret"]].rename(
        columns={"month": "month_hold", "ret": "ret_next"})
    df = panel.copy()
    df["month_hold"] = df["month"] + pd.DateOffset(months=1)
    df = df.merge(nxt, on=["permno", "month_hold"], how="left")
    return df.drop(columns=["month_hold"])


def monthly_quintile_stats(df: pd.DataFrame, signal: str) -> pd.DataFrame:
    """For each month t and quintile: VW total return over t+1,
    market-cap share, and firm-level characteristics at formation t."""
    sub = df.dropna(subset=[signal, "me", "ret_next"]).copy()
    sub["q"] = assign_quantiles(sub, "month", signal, n_bins=5,
                                warn_fallback=False)

    # months that did not produce all 5 quintiles (ties)
    nq = sub.groupby("month")["q"].nunique()
    n_incomplete = int((nq < 5).sum())
    if n_incomplete:
        print(f"  [warn] {signal}: {n_incomplete} months with <5 quintiles")

    # weighted numerators (NaN characteristics contribute 0 weight)
    sub["_rw"] = sub["ret_next"] * sub["me"]
    sub["_sz_w"] = np.where(sub["size"].notna(), sub["size"] * sub["me"], 0.0)
    sub["_sz_m"] = np.where(sub["size"].notna(), sub["me"], 0.0)
    sub["_bm_w"] = np.where(sub["bm"].notna(), sub["bm"] * sub["me"], 0.0)
    sub["_bm_m"] = np.where(sub["bm"].notna(), sub["me"], 0.0)

    agg = sub.groupby(["month", "q"], as_index=False).agg(
        me=("me", "sum"),
        rw=("_rw", "sum"),
        size_simple=("size", "mean"),
        bm_simple=("bm", "mean"),
        sz_w=("_sz_w", "sum"),
        sz_m=("_sz_m", "sum"),
        bm_w=("_bm_w", "sum"),
        bm_m=("_bm_m", "sum"),
        n=("permno", "count"),
    )
    agg["ret"] = agg["rw"] / agg["me"]
    agg["size_vw"] = agg["sz_w"] / agg["sz_m"]
    agg["bm_vw"] = np.where(agg["bm_m"] > 0, agg["bm_w"] / agg["bm_m"], np.nan)
    total_me = agg.groupby("month")["me"].transform("sum")
    agg["mkt_share"] = 100.0 * agg["me"] / total_me
    return agg


def quintile_time_series(agg: pd.DataFrame, ff: pd.DataFrame) -> dict:
    """Per-quintile time-series stats + CAPM / FF3 alphas, plus 5-1
    spread with NW(4) t-stats.

    CRITICAL convention (matches analyze_tables_10_11.py, fixes two
    offsetting bugs from outer iteration 1):
      * The VW return in `agg` is realized in the HOLDING month (t+1) but
        is indexed by the FORMATION month t. We relabel the series to the
        holding month (t -> t+1) so the return is regressed on the factors
        of the SAME (holding) month. Regressing on formation-month factors
        pairs each return with the PRIOR month's factors and drives market
        betas to ~0 (should be ~1 for a VW portfolio).
      * factor_alpha subtracts rf INTERNALLY (utils/regressions.py:
        y = ret - rf_col). We therefore pass the TOTAL return series —
        pre-subtracting rf (as the old code did) double-adjusts and shifts
        every alpha down by ~mean rf (~0.5%/month)."""
    out = {}
    rets = {}  # quintile -> monthly VW TOTAL return series (holding-month index)
    chars = ["ret", "mkt_share", "size_simple", "size_vw", "bm_simple", "bm_vw"]
    ts = {c: agg.pivot(index="month", columns="q", values=c) for c in chars}
    for q in range(1, 6):
        r = ts["ret"][q].dropna().sort_index()
        r.index = r.index + pd.DateOffset(months=1)  # formation -> holding month
        rets[q] = r
        capm = factor_alpha(r, ff.loc[r.index], factors=["mkt_rf"],
                            n_lags=NW_LAGS)
        ff3 = factor_alpha(r, ff.loc[r.index],
                           factors=["mkt_rf", "smb", "hml"], n_lags=NW_LAGS)
        out[q] = {
            "Mean": r.mean() * 100,
            "Std": r.std(ddof=1) * 100,
            "MktShare": ts["mkt_share"][q].mean(),
            "Size": ts["size_simple"][q].mean(),
            "Size_vw": ts["size_vw"][q].mean(),
            "BM": ts["bm_simple"][q].mean(),
            "BM_vw": ts["bm_vw"][q].mean(),
            "CAPM": capm["alpha_monthly"] * 100,
            "CAPM_t": capm["t_alpha_newey_west"],
            "CAPM_beta": float(capm["betas"]["mkt_rf"]),
            "FF3": ff3["alpha_monthly"] * 100,
            "FF3_t": ff3["t_alpha_newey_west"],
            "n_months": int(len(r)),
        }

    # 5-1 spread
    common = rets[5].index.intersection(rets[1].index).sort_values()
    spread = rets[5].loc[common] - rets[1].loc[common]
    nw = tstat_newey_west(spread, n_lags=NW_LAGS)
    ff0 = ff.loc[common].copy()
    ff0["rf"] = 0.0  # zero-investment spread: no rf subtraction
    s_capm = factor_alpha(spread, ff0, factors=["mkt_rf"], n_lags=NW_LAGS)
    s_ff3 = factor_alpha(spread, ff0, factors=["mkt_rf", "smb", "hml"],
                         n_lags=NW_LAGS)
    out["5-1"] = {
        "Mean": spread.mean() * 100,
        "Mean_t": nw["t_stat"],
        "Std": spread.std(ddof=1) * 100,
        "CAPM": s_capm["alpha_monthly"] * 100,
        "CAPM_t": s_capm["t_alpha_newey_west"],
        "FF3": s_ff3["alpha_monthly"] * 100,
        "FF3_t": s_ff3["t_alpha_newey_west"],
        "n_months": int(len(spread)),
    }
    return out


# ── output ──────────────────────────────────────────────────────────
def _fmt(x, nd=2):
    return "—" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{nd}f}"


def format_panel(title: str, signal: str, res: dict) -> str:
    paper = PAPER[signal]
    rows = ["Q1", "Q2", "Q3", "Q4", "Q5", "5-1"]
    keys = [1, 2, 3, 4, 5, "5-1"]
    head = ("| Portfolio | Mean | Std. Dev. | % Mkt Share | Size | B/M "
            "| CAPM α | (t) | FF-3 α | (t) |")
    sep = "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
    lines = [f"### {title}", "", head, sep]
    for i, (label, k) in enumerate(zip(rows, keys)):
        r = res[k]
        if k == "5-1":
            lines.append(
                f"| 5-1 | {_fmt(r['Mean'])} | {_fmt(r['Std'])} |  |  |  "
                f"| {_fmt(r['CAPM'])} | ({_fmt(r['CAPM_t'])}) "
                f"| {_fmt(r['FF3'])} | ({_fmt(r['FF3_t'])}) |"
            )
        else:
            lines.append(
                f"| {label} | {_fmt(r['Mean'])} | {_fmt(r['Std'])} "
                f"| {_fmt(r['MktShare'])} | {_fmt(r['Size'])} | {_fmt(r['BM'])} "
                f"| {_fmt(r['CAPM'])} | ({_fmt(r['CAPM_t'])}) "
                f"| {_fmt(r['FF3'])} | ({_fmt(r['FF3_t'])}) |"
            )
    # paper comparison block
    lines += ["", f"**Paper values ({title}):**", "",
              "| Portfolio | Mean | Std. Dev. | CAPM α | FF-3 α |",
              "|---|---:|---:|---:|---:|"]
    for i, label in enumerate(rows):
        lines.append(
            f"| {label} | {_fmt(paper['Mean'][i])} | {_fmt(paper['Std'][i])} "
            f"| {_fmt(paper['CAPM'][i])} | {_fmt(paper['FF3'][i])} |"
        )
    return "\n".join(lines)


def write_results(res_tvol: dict, res_ivol: dict, n_months: int,
                  first: pd.Timestamp, last: pd.Timestamp,
                  avg_stocks: float) -> None:
    md = f"""# Table VI — Portfolios Sorted on Volatility
## Ang, Hodrick, Xing, Zhang (2006), "The Cross-Section of Volatility and Expected Returns"

Value-weighted quintile portfolios, formed monthly on the signal measured
from month-t daily data and held for month t+1 (1/0/1 strategy).
Sample: {first:%Y-%m} to {last:%Y-%m} ({n_months} holding months).
Breakpoints: simple quintile cuts (20/40/60/80 pctiles) of ALL stocks.
Mean / Std. Dev. are monthly TOTAL simple returns in percent.
CAPM / FF-3 alphas in percent per month; robust Newey–West (1987)
t-statistics (4 lags) in parentheses.
Average stocks per formation month: {avg_stocks:,.0f}.

{format_panel("Panel A: Total Volatility", "tvol", res_tvol)}

{format_panel("Panel B: Idiosyncratic Volatility (relative to FF-3)", "ivol", res_ivol)}

## Notes

- Size = time-series average of the monthly cross-sectional SIMPLE mean of
  firm log market capitalization ($ millions), per the paper's wording
  ("average log market capitalization for firms within the portfolio").
  Value-weighted alternatives: Panel A Size(VW) =
  {res_tvol[1]['Size_vw']:.2f}, {res_tvol[2]['Size_vw']:.2f}, {res_tvol[3]['Size_vw']:.2f},
  {res_tvol[4]['Size_vw']:.2f}, {res_tvol[5]['Size_vw']:.2f}; Panel B Size(VW) =
  {res_ivol[1]['Size_vw']:.2f}, {res_ivol[2]['Size_vw']:.2f}, {res_ivol[3]['Size_vw']:.2f},
  {res_ivol[4]['Size_vw']:.2f}, {res_ivol[5]['Size_vw']:.2f}.
- B/M = time-series average of the monthly cross-sectional SIMPLE mean of
  firm book-to-market (firms with missing B/M excluded from the average).
  Value-weighted alternatives: Panel A B/M(VW) =
  {res_tvol[1]['BM_vw']:.2f}, {res_tvol[2]['BM_vw']:.2f}, {res_tvol[3]['BM_vw']:.2f},
  {res_tvol[4]['BM_vw']:.2f}, {res_tvol[5]['BM_vw']:.2f}; Panel B B/M(VW) =
  {res_ivol[1]['BM_vw']:.2f}, {res_ivol[2]['BM_vw']:.2f}, {res_ivol[3]['BM_vw']:.2f},
  {res_ivol[4]['BM_vw']:.2f}, {res_ivol[5]['BM_vw']:.2f}.
- % Mkt Share is relative to the total market cap of the sorted universe
  (stocks with a valid signal and ME) each month; quintile shares sum to 100%.
- FF factors from ff.four_factor_monthly (decimal); portfolio excess return
  = VW total return − monthly rf.
- Delisting returns are compounded into each stock's last trading-month
  return upstream (data pipeline, assumption A12).
"""
    path = LAYOUT.result_path("table_6.md")
    path.write_text(md)
    print(f"Wrote {path}")


def plot_quintile_returns(res_tvol: dict, res_ivol: dict) -> None:
    qs = np.arange(1, 6)
    ours_t = [res_tvol[q]["Mean"] for q in qs]
    ours_i = [res_ivol[q]["Mean"] for q in qs]
    pap_t = PAPER["tvol"]["Mean"][:5]
    pap_i = PAPER["ivol"]["Mean"][:5]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
    for ax, ours, pap, title in (
        (axes[0], ours_t, pap_t, "Panel A: Total Volatility"),
        (axes[1], ours_i, pap_i, "Panel B: Idiosyncratic Volatility (FF-3)"),
    ):
        x = np.arange(5)
        bars = ax.bar(x, ours, width=0.6, color="#4c72b0",
                      label="Replication")
        ax.plot(x, pap, "D--", color="crimson", ms=6,
                label="Paper (AHXZ 2006)")
        for xi, v in zip(x, ours):
            ax.text(xi, v + (0.06 if v >= 0 else -0.14), f"{v:.2f}",
                    ha="center", fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels([f"Q{i}" for i in qs])
        ax.set_xlabel("Volatility quintile (1 = lowest, 5 = highest)")
        ax.axhline(0, color="black", lw=0.6)
        ax.set_title(title, fontsize=10)
        ax.legend(fontsize=8)
    axes[0].set_ylabel("Mean monthly total return (%)")
    fig.suptitle("Table VI — Mean returns of volatility-sorted quintile "
                 "portfolios (VW, 1963-07 to 2000-12)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    path = LAYOUT.result_path("ivol_quintile_returns.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Wrote {path}")


# ── main ────────────────────────────────────────────────────────────
def run_table6() -> None:
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = pd.to_datetime(panel["month"])
    print(f"Panel: {len(panel):,} rows, {panel['month'].nunique()} months, "
          f"{panel['permno'].nunique():,} permnos")

    print("Loading monthly FF factors (ff_monthly.sql)…")
    ff = load_ff_monthly()
    print(f"  {len(ff)} factor months, {ff.index.min():%Y-%m} .. "
          f"{ff.index.max():%Y-%m}")

    print("Attaching next-month returns (signal_t -> ret_{t+1})…")
    df = attach_next_month_return(panel)

    # Sanity gate: the VW all-stock holding return must track the FF
    # market in the HOLDING month (catches signal/return misalignment).
    chk = df.dropna(subset=["ret_next", "me"]).query("me > 0")
    vw = ((chk["ret_next"] * chk["me"]).groupby(chk["month"]).sum()
          / chk["me"].groupby(chk["month"]).sum())
    vw.index = vw.index + pd.DateOffset(months=1)  # label by holding month
    mkt = ff["mkt_rf"] + ff["rf"]
    both = pd.concat([vw, mkt], axis=1, sort=True).dropna()
    corr = both.iloc[:, 0].corr(both.iloc[:, 1])
    print(f"  alignment check: VW all-stock vs FF market corr = {corr:.4f} "
          f"(must be ~1); mean VW = {both.iloc[:, 0].mean()*100:.2f}% vs "
          f"mkt = {both.iloc[:, 1].mean()*100:.2f}%")
    assert corr > 0.98, "signal/return alignment broken (corr < 0.98)"

    results = {}
    for signal, label in (("tvol", "Panel A (total volatility)"),
                          ("ivol", "Panel B (idiosyncratic volatility)")):
        print(f"Sorting on {label}…")
        agg = monthly_quintile_stats(df, signal)
        res = quintile_time_series(agg, ff)
        results[signal] = res
        print(f"  holding months per quintile: {res[1]['n_months']}; "
              f"5-1 mean = {res['5-1']['Mean']:.2f}% "
              f"(t = {res['5-1']['Mean_t']:.2f})")
        for q in range(1, 6):
            print(f"    Q{q}: mean={res[q]['Mean']:6.2f}%  "
                  f"std={res[q]['Std']:5.2f}%  "
                  f"b_mkt={res[q]['CAPM_beta']:5.2f}  "
                  f"CAPM={res[q]['CAPM']:6.2f} (t={res[q]['CAPM_t']:5.2f})  "
                  f"FF3={res[q]['FF3']:6.2f} (t={res[q]['FF3_t']:5.2f})")
        # Sanity gate (M1 fix): the return/factor alignment is correct iff
        # the portfolios load on the market. In the broken version betas
        # were ~0 (returns regressed on the PRIOR month's factors). Here
        #   (a) every quintile beta must be clearly positive (not ~0), and
        #   (b) the market-cap-weighted average beta must be ~1.0 (±0.3),
        #       since the all-stock VW portfolio tracks the market.
        # Individual quintile betas rise with the volatility sort (high-vol
        # stocks have higher beta), so a per-quintile ±0.3 gate would be
        # wrong; the weighted average is the meaningful "~1" check.
        betas = [res[q]["CAPM_beta"] for q in range(1, 6)]
        shares = [res[q]["MktShare"] for q in range(1, 6)]
        wavg_beta = sum(b * s for b, s in zip(betas, shares)) / sum(shares)
        for q, b in zip(range(1, 6), betas):
            assert b > 0.5, (
                f"{label}: Q{q} market beta = {b:.3f} ~ 0 — the holding-month "
                f"relabel is missing (returns regressed on formation-month "
                f"factors)."
            )
        assert abs(wavg_beta - 1.0) <= 0.3, (
            f"{label}: mkt-cap-weighted avg beta = {wavg_beta:.3f}, "
            f"expected ~1.0 (±0.3)."
        )
        print(f"    market betas Q1..Q5 = " +
              ", ".join(f"{b:.2f}" for b in betas) +
              f"  (mkt-cap-wtd avg = {wavg_beta:.2f}, sanity gate passed)")

    # diagnostics for the results file
    sub = df.dropna(subset=["tvol", "me", "ret_next"])
    avg_stocks = sub.groupby("month")["permno"].count().mean()
    holding_months = sorted(sub["month"].unique() + pd.DateOffset(months=1))
    write_results(results["tvol"], results["ivol"],
                  n_months=len(holding_months),
                  first=pd.Timestamp(holding_months[0]),
                  last=pd.Timestamp(holding_months[-1]),
                  avg_stocks=avg_stocks)
    plot_quintile_returns(results["tvol"], results["ivol"])


if __name__ == "__main__":
    run_table6()
