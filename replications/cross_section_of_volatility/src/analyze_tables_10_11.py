"""
Tables X and XI analysis — Ang, Hodrick, Xing, Zhang (2006), "The
Cross-Section of Volatility and Expected Returns".

Table X — L/M/N strategies (FF-3 alphas of IVOL quintile portfolios):
    L = formation period (months of daily data for IVOL)
    M = skip period (months skipped between formation and holding)
    N = holding period (months)

    The panel stores IVOL from 1 month of daily data only (L=1).
    * 1/0/1 (Table VI): signal at month t, hold month t+1.
    * 1/1/1: signal at month t-1, skip month t, hold month t+1
      == sort on signal_m, earn the return realized in calendar month
      m+2 (lag the signal by 2 months instead of 1). IMPLEMENTED.
    * 1/1/12, 12/1/1, 12/1/12: require IVOL computed from multi-month
      (12-month) daily data and/or multi-month holding returns with
      overlapping cohorts — NOT available in the current panel
      (documented as a limitation in results/table_10.md).

Table XI — subsample analysis with the 1/0/1 strategy (FF-3 alphas):
    a) Jul 1963 – Dec 1970      e) NBER expansions
    b) Jan 1971 – Dec 1980      f) NBER recessions
    c) Jan 1981 – Dec 1990      g) stable months (lowest 20% |MKT|RF|)
    d) Jan 1991 – Dec 2000      h) volatile months (highest 20% |MKT|RF|)

    Subsample membership is defined on the HOLDING month (the month the
    portfolio return is realized). Quintile portfolios are formed each
    month on the full cross-section (sorting is NOT redone within
    subsamples); the monthly VW return time series is then split.

Conventions (same as analyze_table6.py / assumptions.md):
    * FF factors are DECIMAL (no /100); final alphas x100 for percent.
    * Breakpoints: simple quintile cuts (20/40/60/80 pctiles) of ALL
      stocks with a valid signal + ME each month.
    * Portfolio excess return = VW TOTAL return - rf; the 5-1 spread is
      zero-investment (no rf subtraction).
    * Newey-West (1987) t-statistics with 4 lags (task spec; paper
      silent on lag count — assumption A15).

Outputs:
    results/table_10.md
    results/table_11.md
"""
from __future__ import annotations

import numpy as np
import pandas as pd

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

NW_LAGS = 4     # Newey-West lags for alpha / spread t-stats (task spec)
N_BINS = 5      # quintile portfolios
SAMPLE_START = pd.Timestamp("1963-07-01")  # first holding month
SAMPLE_END = pd.Timestamp("2000-12-01")    # last holding month

# Paper values (AHXZ 2006 Table X — FF-3 alphas, %/month)
PAPER_T10 = {
    "1/1/1":   [0.06, 0.04, 0.09, -0.18, -0.82, -0.88],
    "1/1/12":  [0.03, 0.02, -0.02, -0.17, -0.64, -0.67],
    "12/1/1":  [0.04, 0.08, -0.01, -0.29, -1.08, -1.12],
    "12/1/12": [0.04, 0.04, -0.02, -0.35, -0.73, -0.77],
}

# Paper values (AHXZ 2006 Table XI — FF-3 alphas, %/month; Q5 and 5-1)
PAPER_T11 = {
    "Jul 1963 – Dec 1970":  {"Q5": -0.94, "5-1": -1.00},
    "Jan 1971 – Dec 1980":  {"Q5": -1.02, "5-1": -0.77},
    "Jan 1981 – Dec 1990":  {"Q5": -2.08, "5-1": -2.23},
    "Jan 1991 – Dec 2000":  {"Q5": -1.39, "5-1": -1.55},
    "NBER Expansions":      {"Q5": -1.19, "5-1": -1.25},
    "NBER Recessions":      {"Q5": -1.88, "5-1": -1.79},
    "Stable periods":       {"Q5": -1.66, "5-1": -1.71},
    "Volatile periods":     {"Q5": -0.93, "5-1": -0.89},
}

# NBER recession dates (peak to trough, inclusive), from the task spec
NBER_RECESSIONS = [
    ("1969-12-01", "1970-11-01"),
    ("1973-11-01", "1975-03-01"),
    ("1980-01-01", "1980-07-01"),
    ("1981-07-01", "1982-11-01"),
    ("1990-07-01", "1991-03-01"),
    ("2001-03-01", "2001-11-01"),  # partially in sample (sample ends 2000-12)
]


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
def attach_holding_return(panel: pd.DataFrame, months_ahead: int) -> pd.DataFrame:
    """Pair signal at month m with the stock's return in calendar month
    m + months_ahead (explicit calendar-month merge, no per-stock shift).

    months_ahead=1 -> 1/0/1 (M=0): sort on signal_m, earn ret_{m+1}.
    months_ahead=2 -> 1/1/1 (M=1): sort on signal_m, skip m+1, earn ret_{m+2}.
    """
    nxt = panel[["permno", "month", "ret"]].rename(
        columns={"month": "month_hold", "ret": "ret_hold"})
    df = panel.copy()
    df["month_hold"] = df["month"] + pd.DateOffset(months=months_ahead)
    df = df.merge(nxt, on=["permno", "month_hold"], how="left")
    return df.drop(columns=["month_hold"])


def vw_quintile_series(df: pd.DataFrame, signal: str,
                       hold_offset: int) -> tuple[dict, float]:
    """Monthly VW total returns per quintile, indexed by HOLDING month.

    Forms quintiles each month on `signal` over all stocks with a valid
    signal + ME; VW return = sum(me*ret_hold)/sum(me) within (month, q).
    The time-series index is the holding month = formation month +
    hold_offset. Returns (dict {1..5, '5-1': Series}, avg_stocks)."""
    sub = df.dropna(subset=[signal, "me", "ret_hold"]).copy()
    sub["q"] = assign_quantiles(sub, "month", signal, n_bins=N_BINS,
                                warn_fallback=False)

    # months that did not produce all 5 quintiles (ties)
    nq = sub.groupby("month")["q"].nunique()
    n_incomplete = int((nq < N_BINS).sum())
    if n_incomplete:
        print(f"  [warn] {signal}: {n_incomplete} months with <{N_BINS} quintiles")

    sub["_rw"] = sub["ret_hold"] * sub["me"]
    agg = sub.groupby(["month", "q"], as_index=False).agg(
        rw=("_rw", "sum"), me=("me", "sum"))
    agg["ret"] = agg["rw"] / agg["me"]
    piv = agg.pivot(index="month", columns="q", values="ret")
    piv.index = piv.index + pd.DateOffset(months=hold_offset)  # holding month
    piv = piv.sort_index()

    rets = {q: piv[q].dropna() for q in range(1, N_BINS + 1)}
    common = rets[N_BINS].index.intersection(rets[1].index).sort_values()
    rets["5-1"] = rets[N_BINS].loc[common] - rets[1].loc[common]

    avg_stocks = sub.groupby("month")["permno"].count().mean()
    return rets, avg_stocks


def subset_series(rets: dict, months) -> dict:
    """Restrict each quintile series to `months` (holding-month set);
    recompute the 5-1 spread on the common index."""
    mset = set(months)
    out = {q: rets[q][rets[q].index.isin(mset)] for q in range(1, N_BINS + 1)}
    common = out[N_BINS].index.intersection(out[1].index).sort_values()
    out["5-1"] = out[N_BINS].loc[common] - out[1].loc[common]
    return out


def ff3_alphas(rets: dict, ff: pd.DataFrame) -> dict:
    """Per-quintile FF-3 alphas (%/month, NW(4) t-stats) + mean total
    return; 5-1 spread treated as zero-investment (no rf subtraction).

    NOTE: factor_alpha subtracts rf INTERNALLY (utils/regressions.py
    line ~587: y = ret - rf_col), so pass the TOTAL return series —
    pre-subtracting rf would double-adjust (shifts every alpha down by
    ~mean rf ≈ 0.5%/month). Portfolio return at holding month t is
    regressed on the factors of the SAME month t (correct alignment)."""
    out = {}
    for q in range(1, N_BINS + 1):
        r = rets[q]
        res = factor_alpha(r, ff.loc[r.index],
                           factors=["mkt_rf", "smb", "hml"], n_lags=NW_LAGS)
        out[q] = {
            "Mean": r.mean() * 100,
            "FF3": res["alpha_monthly"] * 100,
            "FF3_t": res["t_alpha_newey_west"],
            "n_months": int(res["n_obs"]),
        }
    s = rets["5-1"]
    nw = tstat_newey_west(s, n_lags=NW_LAGS)
    ff0 = ff.loc[s.index].copy()
    ff0["rf"] = 0.0  # zero-investment spread
    res = factor_alpha(s, ff0, factors=["mkt_rf", "smb", "hml"],
                       n_lags=NW_LAGS)
    out["5-1"] = {
        "Mean": s.mean() * 100,
        "Mean_t": nw["t_stat"],
        "FF3": res["alpha_monthly"] * 100,
        "FF3_t": res["t_alpha_newey_west"],
        "n_months": int(res["n_obs"]),
    }
    return out


# ── subsample month sets (defined on holding months) ────────────────
def stable_volatile_sets(ff: pd.DataFrame, classify_on: str = "holding"):
    """(stable, volatile, lo, hi): two sets of HOLDING months whose
    |MKT|RF| is in the bottom / top 20% of the in-sample months, plus the
    20th/80th-pctile thresholds used.

    classify_on='holding' (PRIMARY, paper convention): classify each month
    of the portfolio return series by its OWN |mkt_rf| (L2074: "months with
    the lowest and highest 20% absolute value of the market return"). The
    return series is indexed by holding month, so this is the natural read.
    classify_on='formation' (SENSITIVITY, issue M4): classify by the
    |mkt_rf| of the FORMATION month (holding − 1), then map each classified
    formation month forward to its holding month (+1). Both give exactly 90
    stable + 90 volatile months (450 × 0.20)."""
    all_hold = pd.date_range(SAMPLE_START, SAMPLE_END, freq="MS")
    if classify_on == "holding":
        cls_months = all_hold
    else:  # formation
        cls_months = all_hold - pd.DateOffset(months=1)
    abs_mkt = ff.loc[cls_months, "mkt_rf"].abs().dropna()
    lo, hi = abs_mkt.quantile([0.20, 0.80])
    stable = set(abs_mkt[abs_mkt <= lo].index)
    volatile = set(abs_mkt[abs_mkt >= hi].index)
    if classify_on == "formation":
        stable = set(pd.Timestamp(m) + pd.DateOffset(months=1) for m in stable)
        volatile = set(pd.Timestamp(m) + pd.DateOffset(months=1) for m in volatile)
    return stable, volatile, lo, hi


def build_subsamples(ff: pd.DataFrame,
                     classify_on: str = "holding") -> tuple[dict, float, float]:
    """(Dict subsample_name -> set of holding months, 20th/80th pctile
    thresholds of |MKT|RF| used for the stable/volatile split)."""
    all_hold = pd.date_range(SAMPLE_START, SAMPLE_END, freq="MS")

    rec_months: set = set()
    for peak, trough in NBER_RECESSIONS:
        rec_months |= set(pd.date_range(peak, trough, freq="MS"))
    rec_in = rec_months & set(all_hold)
    exp_in = set(all_hold) - rec_in

    # stable / volatile: |MKT|RF| over the in-sample months (see
    # stable_volatile_sets for the holding-vs-formation convention)
    stable, volatile, lo, hi = stable_volatile_sets(ff, classify_on)

    return {
        "Jul 1963 – Dec 1970": set(pd.date_range("1963-07-01", "1970-12-01", freq="MS")),
        "Jan 1971 – Dec 1980": set(pd.date_range("1971-01-01", "1980-12-01", freq="MS")),
        "Jan 1981 – Dec 1990": set(pd.date_range("1981-01-01", "1990-12-01", freq="MS")),
        "Jan 1991 – Dec 2000": set(pd.date_range("1991-01-01", "2000-12-01", freq="MS")),
        "NBER Expansions": exp_in,
        "NBER Recessions": rec_in,
        "Stable periods": stable,
        "Volatile periods": volatile,
    }, lo, hi


# ── output ──────────────────────────────────────────────────────────
def _fmt(x, nd=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    return f"{x:.{nd}f}"


def write_table10(res_111: dict, n_months: int, first: pd.Timestamp,
                  last: pd.Timestamp, avg_stocks: float) -> None:
    paper = PAPER_T10["1/1/1"]
    labels = ["Q1", "Q2", "Q3", "Q4", "Q5", "5-1"]
    keys = [1, 2, 3, 4, 5, "5-1"]
    lines = [
        "# Table X — FF-3 Alphas for L/M/N Strategies",
        "## Ang, Hodrick, Xing, Zhang (2006), \"The Cross-Section of Volatility and Expected Returns\"",
        "",
        "Value-weighted quintile portfolios sorted on idiosyncratic volatility",
        "(relative to FF-3). L = formation months of daily data, M = skip months,",
        "N = holding months. Alphas in percent per month from FF-3 time-series",
        "regressions; Newey–West (1987) t-statistics (4 lags) in parentheses.",
        "",
        "### 1/1/1 strategy (L=1, M=1, N=1)",
        "",
        f"Sort on IVOL from month-t daily data, skip 1 month, hold for 1 month:",
        f"signal at month m paired with the return realized in month m+2.",
        f"Sample: {first:%Y-%m} to {last:%Y-%m} ({n_months} holding months).",
        f"Average stocks per formation month: {avg_stocks:,.0f}.",
        "",
        "| Portfolio | FF-3 α | (t) | Mean (ref.) |",
        "|---|---:|---:|---:|",
    ]
    for label, k in zip(labels, keys):
        r = res_111[k]
        lines.append(
            f"| {label} | {_fmt(r['FF3'])} | ({_fmt(r['FF3_t'])}) "
            f"| {_fmt(r['Mean'])} |"
        )
    lines += [
        "",
        "**Paper values (1/1/1, FF-3 alphas):**",
        "",
        "| Portfolio | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |",
        "|---|---:|---:|---:|---:|---:|---:|",
        "| Paper | " + " | ".join(_fmt(v) for v in paper) + " |",
        "",
        "### Other L/M/N strategies",
        "",
        "| Strategy | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 | Status |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for strat in ["1/1/12", "12/1/1", "12/1/12"]:
        p = PAPER_T10[strat]
        note = ("requires recomputing IVOL from multi-month daily data — "
                "not available in current panel")
        lines.append(
            f"| {strat} | " + " | ".join(_fmt(v) for v in p)
            + f" | {note} |"
        )
    lines += [
        "",
        "## Notes",
        "",
        "- 1/0/1 (the Table VI Panel B strategy) is the baseline; 1/1/1 adds",
        "  a 1-month skip between formation and holding. Both use the panel's",
        "  L=1 IVOL (daily data from the most recent month only).",
        "- The 12/1/1, 1/1/12 and 12/1/12 strategies require IVOL computed",
        "  from 12 months of daily data (L=12), which is not stored in the",
        "  panel; replicating them requires a new daily-data pipeline pass.",
        "- Mean (ref.) is the mean monthly VW TOTAL return in percent",
        "  (not reported in the paper's Table X, which shows alphas only).",
        "- 5-1 spread regression is zero-investment (no rf subtraction).",
        "- FF factors from ff.four_factor_monthly (decimal).",
        "",
    ]
    path = LAYOUT.result_path("table_10.md")
    path.write_text("\n".join(lines))
    print(f"Wrote {path}")


def write_table11(full_res: dict, sub_res: dict, sub_n: dict,
                  lo: float, hi: float, avg_stocks: float,
                  sens: dict | None = None, lo_f: float | None = None,
                  hi_f: float | None = None) -> None:
    lines = [
        "# Table XI — FF-3 Alphas Across Subsamples (1/0/1 Strategy)",
        "## Ang, Hodrick, Xing, Zhang (2006), \"The Cross-Section of Volatility and Expected Returns\"",
        "",
        "Value-weighted quintile portfolios sorted on idiosyncratic volatility",
        "(relative to FF-3), 1/0/1 strategy (sort on month-t IVOL, hold month",
        f"t+1). Alphas in percent per month; Newey–West (1987) t-statistics",
        "(4 lags) in parentheses. Quintile portfolios are formed each month on",
        "the full cross-section; subsamples split the resulting monthly return",
        "series by HOLDING month.",
        f"Average stocks per formation month: {avg_stocks:,.0f}.",
        "",
        "### Full sample (Jul 1963 – Dec 2000)",
        "",
        "| Portfolio | FF-3 α | (t) | Mean |",
        "|---|---:|---:|---:|",
    ]
    for label, k in zip(["Q1", "Q2", "Q3", "Q4", "Q5", "5-1"],
                        [1, 2, 3, 4, 5, "5-1"]):
        r = full_res[k]
        lines.append(f"| {label} | {_fmt(r['FF3'])} | ({_fmt(r['FF3_t'])}) "
                     f"| {_fmt(r['Mean'])} |")

    lines += [
        "",
        "### Subsample alphas",
        "",
        "| Subsample | n | Q1 α | Q2 α | Q3 α | Q4 α | Q5 α | (t) | 5-1 α | (t) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name in PAPER_T11:
        r = sub_res[name]
        n = sub_n[name]
        lines.append(
            f"| {name} | {n} "
            f"| {_fmt(r[1]['FF3'])} | {_fmt(r[2]['FF3'])} | {_fmt(r[3]['FF3'])} "
            f"| {_fmt(r[4]['FF3'])} | {_fmt(r[5]['FF3'])} | ({_fmt(r[5]['FF3_t'])}) "
            f"| {_fmt(r['5-1']['FF3'])} | ({_fmt(r['5-1']['FF3_t'])}) |"
        )
    lines += [
        "",
        "**Paper values (Q5 α and 5-1 α, FF-3):**",
        "",
        "| Subsample | Q5 α (paper) | 5-1 α (paper) |",
        "|---|---:|---:|",
    ]
    for name, p in PAPER_T11.items():
        lines.append(f"| {name} | {_fmt(p['Q5'])} | {_fmt(p['5-1'])} |")
    lines += [
        "",
        "## Notes",
        "",
        "- Decade subsamples (a–d) and NBER cycle subsamples (e–f) use holding",
        "  months in the given ranges. NBER recessions (peak–trough, inclusive):",
        "  1969-12–1970-11, 1973-11–1975-03, 1980-01–1980-07, 1981-07–1982-11,",
        "  1990-07–1991-03, 2001-03–2001-11 (the last falls after the sample",
        "  end 2000-12 and contributes 0 months). Expansions = all other",
        "  in-sample months.",
        f"- Stable/volatile subsamples: months with |MKT|RF| (ff.four_factor_monthly",
        f"  mkt_rf, decimal) in the lowest/highest 20% of in-sample holding months",
        f"  (20th pctile = {lo*100:.3f}%, 80th pctile = {hi*100:.3f}%); exactly 90",
        f"  months in each (450 × 0.20).",
        "- 5-1 spread regression is zero-investment (no rf subtraction).",
        "- FF factors from ff.four_factor_monthly (decimal).",
        "",
    ]
    # Issue M4 sensitivity: classify stable/volatile on the formation month
    if sens is not None:
        vs = sens["Volatile periods"]
        ss = sens["Stable periods"]
        s_51 = _fmt(PAPER_T11["Stable periods"]["5-1"])
        v_51 = _fmt(PAPER_T11["Volatile periods"]["5-1"])
        lines += [
            "### Sensitivity — stable/volatile classified on the FORMATION month",
            "",
            "Issue M4: the paper (L2074) classifies months by |MKT|RF|. The return "
            "series is indexed by the HOLDING month, so the primary table classifies "
            "on the holding month. As a sensitivity, classifying on the FORMATION "
            f"month (holding − 1; 20th pctile = {(lo_f or 0)*100:.3f}%, 80th pctile = "
            f"{(hi_f or 0)*100:.3f}%) gives:",
            "",
            "| Subsample | n | Q5 α | 5-1 α | (t) | Paper 5-1 |",
            "|---|---:|---:|---:|---:|---:|",
            f"| Stable (formation) | {ss[5]['n_months']} | {_fmt(ss[5]['FF3'])} "
            f"| {_fmt(ss['5-1']['FF3'])} | ({_fmt(ss['5-1']['FF3_t'])}) "
            f"| {s_51} |",
            f"| Volatile (formation) | {vs[5]['n_months']} | {_fmt(vs[5]['FF3'])} "
            f"| {_fmt(vs['5-1']['FF3'])} | ({_fmt(vs['5-1']['FF3_t'])}) "
            f"| {v_51} |",
            "",
            "The formation-month convention moves the volatile-period 5-1 closer to "
            "the paper (less attenuated) but makes stable ≈ volatile (both near "
            f"{_fmt(vs['5-1']['FF3'])}), destroying the paper's stable-vs-volatile "
            f"contrast (paper stable {s_51} vs volatile {v_51}). The holding-month "
            "convention (primary table) reproduces that contrast and matches the "
            "stable period well. The volatile-period 5-1 is attenuated under BOTH "
            "conventions and is highly sensitive to the exact 90-month set — a "
            "small-sample limitation.",
            "",
        ]
    path = LAYOUT.result_path("table_11.md")
    path.write_text("\n".join(lines))
    print(f"Wrote {path}")


# ── main ────────────────────────────────────────────────────────────
def run() -> None:
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = pd.to_datetime(panel["month"])
    print(f"Panel: {len(panel):,} rows, {panel['month'].nunique()} months, "
          f"{panel['permno'].nunique():,} permnos")

    print("Loading monthly FF factors (ff_monthly.sql)…")
    ff = load_ff_monthly()
    print(f"  {len(ff)} factor months, {ff.index.min():%Y-%m} .. "
          f"{ff.index.max():%Y-%m}")

    # ── Table X: 1/1/1 (signal_m -> ret_{m+2}) ─────────────────────
    print("Table X — 1/1/1 strategy (lag signal by 2 months)…")
    df2 = attach_holding_return(panel, months_ahead=2)
    rets_111, avg_stocks_111 = vw_quintile_series(df2, "ivol", hold_offset=2)
    res_111 = ff3_alphas(rets_111, ff)
    hold_m = rets_111[1].index
    print(f"  holding months: {hold_m.min():%Y-%m} .. {hold_m.max():%Y-%m} "
          f"({len(hold_m)})")
    for q in range(1, 6):
        print(f"    Q{q}: FF3={res_111[q]['FF3']:6.2f} "
              f"(t={res_111[q]['FF3_t']:5.2f})")
    print(f"    5-1: FF3={res_111['5-1']['FF3']:6.2f} "
          f"(t={res_111['5-1']['FF3_t']:5.2f})")
    write_table10(res_111, n_months=len(hold_m),
                  first=hold_m.min(), last=hold_m.max(),
                  avg_stocks=avg_stocks_111)

    # ── Table XI: 1/0/1 (signal_m -> ret_{m+1}) ────────────────────
    print("Table XI — 1/0/1 strategy (standard IVOL sort)…")
    df1 = attach_holding_return(panel, months_ahead=1)
    rets_101, avg_stocks_101 = vw_quintile_series(df1, "ivol", hold_offset=1)

    # alignment sanity gate (same as analyze_table6.py): the all-stock
    # VW holding return must track the FF market in the HOLDING month
    chk = df1.dropna(subset=["ret_hold", "me"]).query("me > 0")
    vw = ((chk["ret_hold"] * chk["me"]).groupby(chk["month"]).sum()
          / chk["me"].groupby(chk["month"]).sum())
    vw.index = vw.index + pd.DateOffset(months=1)  # label by holding month
    mkt = ff["mkt_rf"] + ff["rf"]
    both = pd.concat([vw, mkt], axis=1, sort=True).dropna()
    corr = both.iloc[:, 0].corr(both.iloc[:, 1])
    print(f"  alignment check: VW all-stock vs FF market corr = {corr:.4f} "
          f"(must be ~1)")
    assert corr > 0.98, "signal/return alignment broken (corr < 0.98)"
    print(f"  holding months: {rets_101[1].index.min():%Y-%m} .. "
          f"{rets_101[1].index.max():%Y-%m} ({len(rets_101[1].index)})")

    full_res = ff3_alphas(rets_101, ff)
    for q in range(1, 6):
        print(f"    full-sample Q{q}: FF3={full_res[q]['FF3']:6.2f} "
              f"(t={full_res[q]['FF3_t']:5.2f})")
    print(f"    full-sample 5-1: FF3={full_res['5-1']['FF3']:6.2f} "
          f"(t={full_res['5-1']['FF3_t']:5.2f})")

    subsamples, lo, hi = build_subsamples(ff, classify_on="holding")
    sub_res, sub_n = {}, {}
    for name, months in subsamples.items():
        sub = subset_series(rets_101, months)
        sub_res[name] = ff3_alphas(sub, ff)
        sub_n[name] = sub_res[name][5]["n_months"]
        p = PAPER_T11[name]
        r = sub_res[name]
        print(f"  {name}: n={sub_n[name]:3d}  "
              f"Q5={r[5]['FF3']:6.2f} (paper {p['Q5']:6.2f})  "
              f"5-1={r['5-1']['FF3']:6.2f} (paper {p['5-1']:6.2f})")

    # Issue M4 sensitivity: classify stable/volatile on the FORMATION month's
    # |mkt_rf| instead of the holding month's (see stable_volatile_sets).
    print("  [M4 sensitivity] stable/volatile classified on FORMATION month:")
    sub_form, lo_f, hi_f = build_subsamples(ff, classify_on="formation")
    sens = {}
    for name in ("Stable periods", "Volatile periods"):
        sub = subset_series(rets_101, sub_form[name])
        sens[name] = ff3_alphas(sub, ff)
        p = PAPER_T11[name]
        r = sens[name]
        print(f"    {name}: n={r[5]['n_months']:3d}  "
              f"Q5={r[5]['FF3']:6.2f} (paper {p['Q5']:6.2f})  "
              f"5-1={r['5-1']['FF3']:6.2f} (t={r['5-1']['FF3_t']:5.2f}) "
              f"(paper {p['5-1']:6.2f})")

    write_table11(full_res, sub_res, sub_n, lo, hi, avg_stocks_101,
                  sens=sens, lo_f=lo_f, hi_f=hi_f)


if __name__ == "__main__":
    run()
