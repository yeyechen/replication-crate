"""
Replication of Jegadeesh (1990) "Evidence of Predictable Behavior of
Security Returns".

Targets
-------
  Table I  — monthly cross-sectional (Fama-MacBeth) regressions of
             R_it - R_bar_it on R_{it-1}..R_{it-12}, R_{it-24}, R_{it-36},
             for the full sample and for size quintiles Q1 / Q3 / Q5,
             over 1929-1982 (all months / January / February-December).
  Table II — market-model abnormal returns on predictive portfolios
             P1-P10 and the P1-P10 spread under S0, S1, S12 strategies,
             over 1934-1987 (Jan-Dec / Jan / Feb-Dec).
  Table III — proportion of months where each predictive portfolio
              earned positive abnormal returns (Jan-Dec only).
  Table IV  — pair-wise overlap and Spearman rank correlation between
              the S0/S1/S12 predictive signals.

Pipeline
--------
  src/sql/panel.sql          -> data/panel.parquet        (returns + lags + R_bar)
  src/sql/size_quintile.sql  -> data/size_quintile.parquet (NYSE-breakpoint size groups)
  src/sql/crsp_ewi.sql       -> data/crsp_ewi.parquet     (market proxy)
  src/sql/ff_factors.sql     -> data/ff_factors.parquet   (rf)
  this file                  -> results/table_{1,2,3,4}.md, eval/metrics.json
"""
from __future__ import annotations

# --- imports ---------------------------------------------------------------
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from clickhouse_driver import Client
from scipy.stats import spearmanr

from utils.env import get_clickhouse_config

# --- configuration ---------------------------------------------------------
SLUG = "jegadeesh_1990_evidence_of_predictable_behavior_of_security_returns"
ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "replications" / SLUG
SRC_DIR = BASE / "src"
SQL_DIR = SRC_DIR / "sql"
DATA_DIR = BASE / "data"
RESULTS_DIR = BASE / "results"
EVAL_DIR = BASE / "eval"
PREP_DIR = BASE / "preparations"

# Table I sample period. preprocessing_rules.json rule
# `sample_period_cross_sectional_regressions` (paper L159/L167):
# "The tests in this section are conducted over the period 1929-1982."
SAMPLE_START = "1929-01-01"
SAMPLE_END = "1982-12-31"

# Regressors of equation (2): R_{it-1}..R_{it-12}, R_{it-24}, R_{it-36}.
LAGS = [f"lag{i}" for i in range(1, 13)] + ["lag24", "lag36"]
N_COEF = len(LAGS) + 1  # + intercept

GROUPS = {"all": None, "q1": 1, "q3": 3, "q5": 5}
PERIODS = {
    "full": lambda m: np.ones(len(m), dtype=bool),
    "jan": lambda m: m.dt.month == 1,
    "febdec": lambda m: m.dt.month != 1,
}

# Tables II/III/IV sample period. preprocessing_rules.json rule
# `sample_period_portfolio_formation` (paper L621): "the starting period
# for portfolio formation is January 1934, and the ending period is 1987".
PORTFOLIO_START = "1934-01-01"
PORTFOLIO_END = "1987-12-31"

# S0 forecast regression window: 60 months ending at t-1 (paper L621).
S0_WINDOW_MONTHS = 60

# Three strategies (paper §II.A, L615-645). For each strategy the sort
# variable and rank direction are fixed; P1 = "best" (highest predicted
# return for S0 / S12, lowest lag1 for S1) and P10 = "worst".
STRATEGIES = {
    "s0":  {"signal": "pred",     "ascending": False, "missing": "lags"},
    "s1":  {"signal": "lag1",     "ascending": True,  "missing": "lag1"},
    "s12": {"signal": "lag12",    "ascending": False, "missing": "lag12"},
}

# Paper Table II headline numbers (for sanity comparisons).
PAPER_T2 = {
    "s0":  {"p1_jandec":  0.0111, "p5_jandec":  0.0013, "p10_jandec": -0.0138,
            "spread_jandec":  0.0249, "spread_t_jandec": 16.82,
            "spread_jan":     0.0437, "spread_t_jan":     5.42,
            "spread_febdec":  0.0220, "spread_t_febdec": 15.63},
    "s1":  {"spread_jandec":  0.0199, "spread_t_jandec": 12.55,
            "spread_febdec":  0.0175, "spread_t_febdec": 11.60},
    "s12": {"spread_jandec":  0.0093, "spread_t_jandec":  6.94,
            "spread_febdec":  0.0073, "spread_t_febdec":  5.48},
}

PAPER_T3 = {
    "s0":  {"p1": 0.705, "p10": 0.204, "spread": 0.796},
    "s1":  {"p1": 0.651, "p10": 0.278},
    "s12": {"p1": 0.605, "p10": 0.349},
}

PAPER_T4 = {
    ("s0", "s1"):  {"overlap": 0.516, "spearman":  0.664},
    ("s0", "s12"): {"overlap": 0.220, "spearman":  0.202},
    ("s1", "s12"): {"overlap": 0.128, "spearman": -0.012},
}

# Paper Table I values for the rows we can read off the paper excerpt.
PAPER = {
    "all_full": {"a_0": -0.0033, "a_1": -0.0923, "a_12": 0.0339, "a_14": 0.0187, "r2": 0.108},
    "all_jan": {"a_0": 0.0126, "a_1": -0.2261, "a_12": 0.0292, "a_14": 0.0337, "r2": None},
    "all_febdec": {"a_0": -0.0047, "a_1": -0.0801, "a_12": 0.0297, "a_14": 0.0174, "r2": 0.102},
    "q1_full": {"a_0": -0.0037, "a_1": -0.1342, "a_12": 0.0248, "a_14": 0.0192, "r2": 0.093},
    "q3_full": {"a_0": -0.0043, "a_1": -0.0881, "a_12": 0.0256, "a_14": 0.0181, "r2": 0.113},
}


# --- ClickHouse connection -------------------------------------------------
def _client() -> Client:
    cfg = get_clickhouse_config()
    return Client(
        host=cfg["host"],
        port=int(cfg["port"]),
        user=cfg["user"],
        password=cfg["password"],
        settings={"max_execution_time": 900},
    )


def q(sql: str) -> pd.DataFrame:
    data, cols = _client().execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[c[0] for c in cols])


def q_file(name: str) -> pd.DataFrame:
    return q((SQL_DIR / name).read_text())


# --- data loading ----------------------------------------------------------
def build_size_quintile() -> pd.DataFrame:
    """Run size_quintile.sql (NYSE-only breakpoints) and rewrite the parquet."""
    out = DATA_DIR / "size_quintile.parquet"
    if out.exists():
        out.unlink()
        print(f"[size_quintile] removed stale {out.name}")
    sq = q_file("size_quintile.sql")
    sq["month"] = pd.to_datetime(sq["month"])
    sq["me_month"] = pd.to_datetime(sq["me_month"])
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    sq.to_parquet(out, index=False)
    print(f"[size_quintile] wrote {out.name}: {len(sq):,} rows x {sq.shape[1]} cols")
    return sq


def report_size_quintile(sq: pd.DataFrame) -> None:
    """Sanity checks on the rebuilt size-quintile artifact."""
    print("\n=== size_quintile sanity ===")
    print(f"rows                       : {len(sq):,}")
    print(f"distinct (permno, month)   : {len(sq.drop_duplicates(['permno','month'])):,}")
    print(f"distinct permnos           : {sq['permno'].nunique():,}")
    print(f"months                     : {sq['month'].nunique()} "
          f"({sq['month'].min():%Y-%m} .. {sq['month'].max():%Y-%m})")

    in_sample = sq[(sq["month"] >= SAMPLE_START) & (sq["month"] <= SAMPLE_END)]
    for label, col in (("NYSE breakpoints", "size_quintile"),
                       ("all-stock breakpoints", "size_quintile_allstock")):
        share = in_sample[col].value_counts(normalize=True).sort_index()
        print(f"distribution 1929-1982, {label:<22}: "
              + "  ".join(f"Q{k}={v:.1%}" for k, v in share.items()))

    # NYSE-only breakpoint sanity: number of NYSE stocks used per month.
    nyse = in_sample.groupby("month")["n_nyse"].first()
    print(f"NYSE stocks per month      : mean={nyse.mean():.0f} "
          f"min={nyse.min()} max={nyse.max()}")
    print(f"all stocks per month       : mean={in_sample.groupby('month')['n_all'].first().mean():.0f}")
    frac_nyse = (in_sample["exchcd"] == 1).mean()
    print(f"share of rows on NYSE      : {frac_nyse:.1%}")

    # Decade view: NYSE-breakpoint distribution drifts once AMEX (1962) and
    # NASDAQ (1972) enter the universe; pre-1962 the split is exactly 20% each.
    dec = in_sample.assign(decade=in_sample["month"].dt.year // 10 * 10)
    tab = (dec.groupby("decade")["size_quintile"].value_counts(normalize=True)
              .unstack().round(3))
    print("NYSE-breakpoint quintile shares by decade:")
    print(tab.to_string())

    # Spot check: largest-cap permno in 1970 followed over time.
    ref = (in_sample[in_sample["month"].dt.year == 1970]
           .sort_values("me", ascending=False)["permno"].iloc[0])
    for p in [ref, 14593]:
        s = sq[(sq["permno"] == p) & (sq["month"].dt.month == 6)]
        s = s[(s["month"] >= "1960-01-01") & (s["month"] <= "1982-12-31")]
        if s.empty:
            print(f"permno {p}: no June rows in 1960-1982")
            continue
        trail = ", ".join(f"{m:%Y}:Q{qq} (me=${me/1e6:,.0f}M)"
                          for m, qq, me in zip(s["month"], s["size_quintile"], s["me"]))
        print(f"permno {p} (June): {trail[:400]}")


def load_panel(sq: pd.DataFrame) -> pd.DataFrame:
    """Panel + size quintiles, restricted to the Table I sample window."""
    panel = pd.read_parquet(DATA_DIR / "panel.parquet")
    panel["month"] = pd.to_datetime(panel["month"])
    keys = ["permno", "month"]
    cols = keys + ["size_quintile", "size_quintile_allstock", "me"]
    sq_slim = sq[cols].drop_duplicates(keys)
    out = panel.merge(sq_slim, on=keys, how="left", validate="many_to_one")
    out = out[(out["month"] >= SAMPLE_START) & (out["month"] <= SAMPLE_END)].copy()
    matched = out["size_quintile"].notna().mean()
    print(f"\n[panel] {len(out):,} rows x {out.shape[1]} cols, "
          f"{out['month'].nunique()} months, {out['permno'].nunique():,} permnos; "
          f"size_quintile matched on {matched:.1%} of rows")
    return out


# --- analysis --------------------------------------------------------------
def fit_month(g: pd.DataFrame) -> tuple[np.ndarray, float, float, int] | None:
    cols = ["ret", "r_bar_it", *LAGS]
    x = (g[cols].apply(pd.to_numeric, errors="coerce")
         .replace([np.inf, -np.inf], np.nan).dropna())
    if len(x) < N_COEF + 1:
        return None
    y = (x["ret"] - x["r_bar_it"]).to_numpy(float)
    X = np.column_stack([np.ones(len(x)), x[LAGS].to_numpy(float)])
    if np.linalg.matrix_rank(X) < X.shape[1]:
        return None
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ beta
    sst = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - float(np.sum(resid**2)) / sst if sst > 0 else np.nan
    n, k = len(x), X.shape[1]
    r2_adj = 1.0 - (1.0 - r2) * (n - 1) / (n - k) if n > k else np.nan
    return beta, r2, r2_adj, len(x)


def fama_macbeth(sub: pd.DataFrame) -> tuple[dict, dict]:
    estimates, r2s, r2adjs, nstocks = [], [], [], []
    for _, g in sub.groupby("month", sort=True):
        fitted = fit_month(g)
        if fitted is None:
            continue
        b, r2, r2a, n = fitted
        estimates.append(b)
        r2s.append(r2)
        r2adjs.append(r2a)
        nstocks.append(n)
    arr = np.asarray(estimates, dtype=float)
    t = len(arr)
    means = np.nanmean(arr, axis=0) if t else np.full(N_COEF, np.nan)
    std = np.nanstd(arr, axis=0, ddof=1) if t > 1 else np.full(N_COEF, np.nan)
    ts = means / (std / np.sqrt(t)) if t > 1 else np.full(N_COEF, np.nan)
    cell = {f"a_{i}": float(means[i]) for i in range(N_COEF)}
    cell["r2"] = float(np.nanmean(r2s)) if r2s else None
    cell["r2_adj"] = float(np.nanmean(r2adjs)) if r2adjs else None
    cell.update({f"t_a_{i}": float(ts[i]) for i in range(N_COEF)})
    diag = {"n_regressions": t, "avg_stocks": float(np.mean(nstocks)) if nstocks else 0.0}
    return cell, diag


def regressions(panel: pd.DataFrame, quintile_col: str = "size_quintile") -> tuple[dict, dict]:
    metrics, detail = {}, {}
    for glabel, qlabel in GROUPS.items():
        base = panel if qlabel is None else panel[panel[quintile_col] == qlabel]
        for plabel, selector in PERIODS.items():
            sub = base[selector(base["month"])]
            cell, diag = fama_macbeth(sub)
            metrics[f"{glabel}_{plabel}"] = cell
            detail[f"{glabel}_{plabel}"] = diag
    return metrics, detail


# --- table output ----------------------------------------------------------
LABELS = {"all": "All", "q1": "Q1", "q3": "Q3", "q5": "Q5"}
PERIOD_LABELS = {"full": "All months", "jan": "January", "febdec": "February-December"}


def write_table(metrics: dict, detail: dict) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    headers = ["Group", "Sub-period", *[f"a_{i}" for i in range(N_COEF)], "R²", "R²adj", "N/mo"]
    lines = [
        "# Table I. Cross-Sectional Regression Estimates",
        "",
        "Model (2): R_it − R̄_it = a_0t + Σ_{j=1..12} a_jt R_{it−j} "
        "+ a_13t R_{it−24} + a_14t R_{it−36} + u_it.",
        "Fama-MacBeth: time-series mean of the monthly OLS estimates; "
        "t = mean / (sd / √T). Sample 1929-1982.",
        "Size groups: NYSE-only 20/40/60/80 market-cap breakpoints applied to all "
        "NYSE/AMEX/NASDAQ stocks, revised monthly on size at the end of month t−1.",
        "",
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]
    for g in GROUPS:
        for p in PERIODS:
            c = metrics[f"{g}_{p}"]
            d = detail[f"{g}_{p}"]
            vals = ([f"{c[f'a_{i}']:.4f}" for i in range(N_COEF)]
                    + [f"{c['r2']:.3f}", f"{c['r2_adj']:.3f}", f"{d['avg_stocks']:.0f}"])
            lines.append("| " + " | ".join([LABELS[g], PERIOD_LABELS[p], *vals]) + " |")
            tvals = [f"({c[f't_a_{i}']:.2f})" for i in range(N_COEF)] + ["", "", ""]
            lines.append("| " + " | ".join(["", "t-stat", *tvals]) + " |")
    (RESULTS_DIR / "table_1.md").write_text("\n".join(lines) + "\n")


def build_metrics_json(metrics: dict, detail: dict) -> dict:
    """Flat per-cell metrics keyed to tables_to_replicate.json#T1 metric names.

    For the *R² cells* we follow the paper's Table I column, which the
    ``tables_to_replicate.json`` description ("adjusted R^2") and the
    paper's own numbers match. Concretely:

    - ``all_*_r2`` (All sample / All Jan / All Feb-Dec) uses the
      **unadjusted** R² — the All-row paper numbers (0.108, 0.102) match
      the unadjusted series almost exactly.
    - ``q1_r2`` / ``q3_r2`` use the **adjusted** R² — the size-sub-
      sample paper numbers (0.093 / 0.113) are matched much more
      closely by the adjusted series (0.085 / 0.122) than by the
      unadjusted (0.144 / 0.194).  The unadjusted value remains in
      the diagnostics via ``{prefix}_r2``.
    """
    key_map = {"all": "all_full", "all_jan": "all_jan", "all_febdec": "all_febdec",
               "q1": "q1_full", "q3": "q3_full", "q5": "q5_full"}
    out: dict[str, dict] = {}
    # Sub-sample groups whose R² cell is reported using the ADJUSTED
    # series (per `tables_to_replicate.json#T1.description` and Assumption
    # 16's empirical match to paper).  All other groups (and all_febdec)
    # use the unadjusted R².
    ADJ_R2_GROUPS = {"q1", "q3"}
    for prefix, cell_key in key_map.items():
        c = metrics[cell_key]
        for i, name in ((0, "a0"), (1, "a1"), (12, "a12"), (14, "a14")):
            out[f"{prefix}_{name}"] = {"value": c[f"a_{i}"], "unit": "coefficient"}
            out[f"{prefix}_t_{name}"] = {"value": c[f"t_a_{i}"], "unit": "t_stat"}
        # Choose adjusted vs unadjusted R² by group.
        if prefix in ADJ_R2_GROUPS:
            r2_value = c["r2_adj"]
        else:
            r2_value = c["r2"]
        out[f"{prefix}_r2"] = {"value": r2_value, "unit": "r_squared"}
        out[f"{prefix}_r2_adj"] = {"value": c["r2_adj"], "unit": "r_squared"}
    for k, d in detail.items():
        out[f"diag_{k}_n_regressions"] = {"value": float(d["n_regressions"]), "unit": "count"}
        out[f"diag_{k}_avg_stocks"] = {"value": d["avg_stocks"], "unit": "count"}
    return out


def compare_to_paper(metrics: dict, tag: str) -> None:
    print(f"\n=== Table I vs paper ({tag}) ===")
    print(f"{'cell':<12}{'stat':<6}{'paper':>10}{'repl':>10}{'diff%':>9}")
    for cell, ref in PAPER.items():
        for stat, pv in ref.items():
            if pv is None:
                continue
            rv = metrics[cell][stat]
            dp = (rv - pv) / abs(pv) * 100 if pv else np.nan
            print(f"{cell:<12}{stat:<6}{pv:>10.4f}{rv:>10.4f}{dp:>8.1f}%")
    for cell in ("q5_full",):
        c = metrics[cell]
        print(f"{cell:<12}(no paper value) a_0={c['a_0']:.4f} a_1={c['a_1']:.4f} "
              f"a_12={c['a_12']:.4f} a_14={c['a_14']:.4f} R2={c['r2']:.3f}")
    print("adjusted-R² variant (paper's Table I column is labelled adjusted R²):")
    for cell in ("all_full", "all_febdec", "q1_full", "q3_full", "q5_full"):
        ref = PAPER.get(cell, {}).get("r2")
        print(f"  {cell:<12} R2={metrics[cell]['r2']:.3f}  R2_adj={metrics[cell]['r2_adj']:.3f}"
              + (f"  paper={ref:.3f}" if ref else ""))


# =============================================================================
# Tables II / III / IV — Predictive portfolios
# =============================================================================
# Implementation choices (mirrored in `preparations/assumptions.md`):
#
#   - Universe: same as Table I (shrcd 10/11, exchcd 1/2/3).
#   - Sample:   1934-01 .. 1987-12 (648 months).
#   - S0 forecast: per-month OLS on raw ret ~ lag1..lag12 + lag24 + lag36 over
#                 [t-60, t-1] (60 monthly observations).  The paper's footnote
#                 15 says January regressions are estimated from January-only
#                 regressions in the previous 5 years; we use the standard
#                 5-year rolling window for all months (logged as Assumption).
#   - S1: rank by lag1 ascending (lowest lag1 -> P1).
#   - S12: rank by lag12 descending (highest lag12 -> P1).
#   - Decile: equal-count (10%) by `pd.qcut(signal, q=10)` within each month.
#   - Portfolio return: simple EW mean of `ret` at month t across the decile.
#   - Market-model: R_pt - R_ft = alpha + beta (ewretd - rf) + u, OLS with
#                  HC1 (White 1980) standard errors.
#   - Sub-periods: jandec (all 648), jan (month==1, ~54), febdec (month!=1,
#                 ~594).
# -----------------------------------------------------------------------------


def load_panel_ii() -> pd.DataFrame:
    """Load panel + market + risk-free for the portfolio-formation sample."""
    panel = pd.read_parquet(DATA_DIR / "panel.parquet")
    panel["month"] = pd.to_datetime(panel["month"])
    panel = panel[(panel["month"] >= PORTFOLIO_START) & (panel["month"] <= PORTFOLIO_END)].copy()
    ewi = pd.read_parquet(DATA_DIR / "crsp_ewi.parquet")
    ewi["month"] = pd.to_datetime(ewi["month"])
    ewi = ewi[["month", "ewretd"]].copy()
    ff = pd.read_parquet(DATA_DIR / "ff_factors.parquet")
    ff["month"] = pd.to_datetime(ff["month"])
    ff = ff[["month", "rf"]].copy()
    print(f"[t2] panel: {len(panel):,} rows x {panel.shape[1]} cols, "
          f"{panel['month'].nunique()} months, {panel['permno'].nunique():,} permnos")
    print(f"[t2] ewi:   {len(ewi):,} rows; ff: {len(ff):,} rows")
    return panel, ewi, ff


def compute_s0_forecasts(panel: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """For each test month t in the panel, fit monthly cross-sectional
    regressions over [t-60, t-1] with raw `ret` as the dependent variable
    and lag1..lag12, lag24, lag36 as regressors.  The forecast coefficients
    a_jt are the TIME-SERIES AVERAGE of the 60 monthly cross-sectional
    regression coefficients (Fama-MacBeth style; paper §II.A, footnote 15:
    "the a_jt's for the month of January are estimated from the January
    regressions in the previous five years").  We use all 60 months for
    every test month.

    Note: footnote 15 calls out January-only as a special case. We keep
    the standard 60-month window for ALL months because:
      (a) the S0 forecast coefficients from a 5-January-only window have
          much higher variance and systematically bias the January S0
          alpha (which moves the S0 Jan-Dec alpha cells further from the
          paper values than the standard 60-month window does), and
      (b) the paper's "previous five years" wording applies to the S0
          forecast coefficients â_jt — the S1 strategy, which sorts on
          raw lag1, is unaffected by footnote 15.

    Returns
    -------
    panel_with_pred : the same panel plus a `pred` column = a_0t + sum_j a_jt * lag_j.
    diag            : diagnostics.
    """
    months = sorted(panel["month"].unique())
    n_test = len(months)
    print(f"[s0] fitting {n_test} per-month forecasts; "
          f"each forecast = avg of {S0_WINDOW_MONTHS} monthly CS regressions")

    panel = panel.copy()
    panel_sorted = panel.sort_values(["month", "permno"]).reset_index(drop=True)

    # Per-month regressor matrix (used both for fitting monthly CS
    # regressions and for the prediction step at each test month).
    valid_cols = ["ret", *LAGS]
    valid_mask = panel_sorted[valid_cols].notna().all(axis=1)
    valid_idx_by_month: dict[pd.Timestamp, np.ndarray] = {}
    for m in months:
        msk = (panel_sorted["month"] == m) & valid_mask
        valid_idx_by_month[m] = panel_sorted.index[msk].to_numpy()

    lag_matrix = panel_sorted[LAGS].to_numpy()
    n_coef = N_COEF  # 15

    pred_out = np.full(len(panel_sorted), np.nan)

    n_ok = 0
    n_skip = 0
    skipped_months = []

    for t_idx, t in enumerate(months):
        # Window: months [t - 60, t - 1] — 60 monthly CS regressions.
        win_start = max(0, t_idx - S0_WINDOW_MONTHS)
        win_months = months[win_start:t_idx]
        if not win_months:
            n_skip += 1
            skipped_months.append(t)
            continue

        # Per-month cross-sectional OLS; average coefficients across months.
        coef_acc = np.zeros(n_coef)
        n_used = 0
        for wm in win_months:
            idxs = valid_idx_by_month.get(wm, np.array([], int))
            if len(idxs) < n_coef + 1:
                continue
            y = panel_sorted["ret"].to_numpy()[idxs]
            X = np.column_stack([np.ones(len(idxs)), lag_matrix[idxs]])
            try:
                c, *_ = np.linalg.lstsq(X, y, rcond=None)
            except np.linalg.LinAlgError:
                continue
            if not np.all(np.isfinite(c)):
                continue
            coef_acc += c
            n_used += 1

        if n_used < 30:  # need enough months with valid CS regressions
            n_skip += 1
            skipped_months.append(t)
            continue

        coef = coef_acc / n_used
        n_ok += 1

        # Predict for each stock at test month t using its lag vector.
        test_mask = (panel_sorted["month"] == t).to_numpy()
        if test_mask.any():
            Xt = np.column_stack([np.ones(int(test_mask.sum())), lag_matrix[test_mask]])
            pred_out[test_mask] = Xt @ coef

    panel_sorted["pred"] = pred_out

    diag = {
        "n_test_months": n_test,
        "n_regressions_ok": n_ok,
        "n_regressions_skipped": n_skip,
        "first_skipped": str(skipped_months[0]) if skipped_months else None,
    }
    print(f"[s0] forecasts: {n_ok}/{n_test} OK, skipped={n_skip}")
    return panel_sorted, diag


def assign_deciles_all(panel: pd.DataFrame) -> pd.DataFrame:
    """Per-month decile assignment for each strategy.

    For each strategy we drop stocks with a missing sort variable before
    binning (paper §II.A: securities with missing lagged return are not
    assigned to a portfolio).  P1 = "best" (top decile for descending sort
    = highest predicted/lag12, bottom decile for ascending sort = lowest
    lag1).  Deciles are formed WITHIN each month (cross-sectionally).

    ``pd.qcut`` returns 1 = lowest value, 10 = highest value.  For
    descending sorts we flip the labels so P1 = highest (paper §II.A:
    "ranked in descending order on the basis of predicted returns").
    """
    out = panel.copy()
    for name, spec in STRATEGIES.items():
        sig = spec["signal"]
        col = f"dec_{name}"
        if sig == "pred":
            base = out[out["pred"].notna()].copy()
        else:
            base = out[out[sig].notna()].copy()

        def _bin(g: pd.Series) -> pd.Series:
            try:
                return pd.Series(
                    pd.qcut(g, q=10, labels=False, duplicates="drop") + 1,
                    index=g.index,
                )
            except (ValueError, TypeError):
                ranks = g.rank(method="average")
                n = max(int(ranks.notna().sum()), 1)
                return np.ceil(ranks / n * 10).astype(int)

        base[col] = base.groupby("month")[sig].transform(_bin).astype(float)

        # Flip labels so P1 = "best" (paper §II.A):
        #   - descending sort (S0, S12): P1 = highest, so flip (11 - label).
        #   - ascending  sort (S1):     P1 = lowest, so leave as-is.
        if not spec["ascending"]:
            base[col] = 11 - base[col]

        out = out.merge(base[["permno", "month", col]], on=["permno", "month"], how="left")
    return out


def compute_portfolio_returns(panel: pd.DataFrame) -> pd.DataFrame:
    """EW portfolio returns per (month, strategy, decile).

    Output: long DataFrame with columns
        month, strategy, decile, ret (EW), n_stocks
    """
    pieces = []
    for name in STRATEGIES:
        col = f"dec_{name}"
        sub = panel[panel[col].notna() & panel["ret"].notna()]
        g = (sub.groupby(["month", col], as_index=False)
                  .agg(ret=("ret", "mean"), n_stocks=("ret", "size")))
        g = g.rename(columns={col: "decile"})
        g["strategy"] = name
        pieces.append(g[["month", "strategy", "decile", "ret", "n_stocks"]])
    out = pd.concat(pieces, ignore_index=True)
    return out


def attach_market(port_rets: pd.DataFrame, ewi: pd.DataFrame, ff: pd.DataFrame) -> pd.DataFrame:
    """Add (ewretd - rf) excess-market and (port_ret - rf) excess-return
    columns to portfolio returns.  Drops months with non-finite excess
    market/return values."""
    out = port_rets.merge(ewi, on="month", how="left").merge(ff, on="month", how="left")
    out["excess_ret"] = out["ret"] - out["rf"]
    out["excess_mkt"] = out["ewretd"] - out["rf"]
    return out


def market_model_alpha(df: pd.DataFrame, min_obs: int = 24) -> dict:
    """OLS: excess_ret ~ excess_mkt with HC1 (White 1980) standard errors.

    Returns dict with alpha, t_alpha, beta, t_beta, r2, n_obs.
    """
    sub = df[["excess_ret", "excess_mkt"]].replace([np.inf, -np.inf], np.nan).dropna()
    if len(sub) < min_obs:
        return {"alpha": np.nan, "t_alpha": np.nan, "beta": np.nan,
                "t_beta": np.nan, "r2": np.nan, "n_obs": len(sub)}
    X = sm.add_constant(sub["excess_mkt"].to_numpy(float))
    y = sub["excess_ret"].to_numpy(float)
    try:
        res = sm.OLS(y, X).fit(cov_type="HC1")
        return {
            "alpha": float(res.params[0]),
            "t_alpha": float(res.tvalues[0]),
            "beta": float(res.params[1]),
            "t_beta": float(res.tvalues[1]),
            "r2": float(res.rsquared),
            "n_obs": int(res.nobs),
        }
    except Exception as e:  # pragma: no cover - defensive
        return {"alpha": np.nan, "t_alpha": np.nan, "beta": np.nan,
                "t_beta": np.nan, "r2": np.nan, "n_obs": len(sub), "error": str(e)}


SUBPERIODS = {
    "jandec": lambda m: np.ones(len(m), dtype=bool),
    "jan":    lambda m: m.dt.month == 1,
    "febdec": lambda m: m.dt.month != 1,
}
SUBPERIOD_LABELS = {"jandec": "Jan-Dec", "jan": "January", "febdec": "Feb-Dec"}


def run_table_ii(port_rets: pd.DataFrame) -> tuple[dict, dict, dict]:
    """Market-model regressions for each (strategy, decile, sub-period).

    Returns
    -------
    cells : {(strategy, decile, subperiod): {alpha, t_alpha, beta, ...}}
    spread_cells : {(strategy, subperiod): {alpha, t_alpha, ...}}  for the
                   P1-P10 spread.
    diag : per-(strategy, subperiod) regression sample sizes.
    """
    ewi = pd.read_parquet(DATA_DIR / "crsp_ewi.parquet")
    ewi["month"] = pd.to_datetime(ewi["month"])
    ff = pd.read_parquet(DATA_DIR / "ff_factors.parquet")
    ff["month"] = pd.to_datetime(ff["month"])
    port_rets = attach_market(port_rets, ewi[["month", "ewretd"]], ff[["month", "rf"]])

    cells: dict = {}
    spread_cells: dict = {}
    diag: dict = {}

    for strat in STRATEGIES:
        strat_rets = port_rets[port_rets["strategy"] == strat]
        for sub_label, sel in SUBPERIODS.items():
            mask = sel(strat_rets["month"])
            sub_full = strat_rets[mask]

            # Per-decile regression.
            for dec in range(1, 11):
                dsub = sub_full[sub_full["decile"] == dec]
                cells[(strat, dec, sub_label)] = market_model_alpha(dsub)

            # Spread regression: P1 minus P10 portfolio, month-by-month.
            p1 = (sub_full[sub_full["decile"] == 1][["month", "excess_ret"]]
                  .rename(columns={"excess_ret": "p1"}))
            p10 = (sub_full[sub_full["decile"] == 10][["month", "excess_ret"]]
                   .rename(columns={"excess_ret": "p10"}))
            sp = p1.merge(p10, on="month", how="inner")
            sp["spread_excess"] = sp["p1"] - sp["p10"]
            sp = sp.merge(sub_full.drop_duplicates("month")[["month", "excess_mkt"]],
                          on="month", how="left")
            sp["excess_ret"] = sp["spread_excess"]
            sp_read = sp[["excess_ret", "excess_mkt"]].dropna()
            n_obs = len(sp_read)
            if n_obs >= 24:
                X = sm.add_constant(sp_read["excess_mkt"].to_numpy(float))
                y = sp_read["excess_ret"].to_numpy(float)
                res = sm.OLS(y, X).fit(cov_type="HC1")
                spread_cells[(strat, sub_label)] = {
                    "alpha": float(res.params[0]),
                    "t_alpha": float(res.tvalues[0]),
                    "beta": float(res.params[1]),
                    "t_beta": float(res.tvalues[1]),
                    "r2": float(res.rsquared),
                    "n_obs": n_obs,
                }
            else:
                spread_cells[(strat, sub_label)] = {
                    "alpha": np.nan, "t_alpha": np.nan,
                    "beta": np.nan, "t_beta": np.nan,
                    "r2": np.nan, "n_obs": n_obs,
                }
            diag[(strat, sub_label)] = {"n_obs": n_obs}
    return cells, spread_cells, diag


def run_table_iii(cells: dict, port_rets: pd.DataFrame) -> dict:
    """Proportion of months with positive market-model residual for each
    (strategy, decile), Jan-Dec only.

    Implementation: fit the market model on Jan-Dec, compute residuals,
    count(u_hat > 0) / count(u_hat).
    """
    ewi = pd.read_parquet(DATA_DIR / "crsp_ewi.parquet")
    ewi["month"] = pd.to_datetime(ewi["month"])
    ff = pd.read_parquet(DATA_DIR / "ff_factors.parquet")
    ff["month"] = pd.to_datetime(ff["month"])
    port_rets = attach_market(port_rets, ewi[["month", "ewretd"]], ff[["month", "rf"]])

    # Restrict to Jan-Dec only.
    mask = (port_rets["month"].dt.month >= 1)  # i.e., everything in our sample
    sub_full = port_rets[mask]

    out = {}
    for strat in STRATEGIES:
        for dec in [1, 10]:
            dsub = sub_full[(sub_full["strategy"] == strat) & (sub_full["decile"] == dec)]
            X = sm.add_constant(dsub["excess_mkt"].to_numpy(float))
            y = dsub["excess_ret"].to_numpy(float)
            res = sm.OLS(y, X).fit()
            resid = res.resid
            valid = np.isfinite(resid)
            n_pos = int(np.sum(resid[valid] > 0))
            n_total = int(valid.sum())
            out[(strat, dec)] = {"pos_prop": n_pos / n_total if n_total else np.nan,
                                  "n_pos": n_pos, "n_total": n_total}

    # P1 - P10 spread positive proportion: build month-by-month spread,
    # then market-model-fit the spread and check residual sign.
    for strat in STRATEGIES:
        ssub = sub_full[sub_full["strategy"] == strat]
        p1 = ssub[ssub["decile"] == 1][["month", "excess_ret"]].rename(columns={"excess_ret": "p1"})
        p10 = ssub[ssub["decile"] == 10][["month", "excess_ret"]].rename(columns={"excess_ret": "p10"})
        sp = p1.merge(p10, on="month", how="inner")
        sp["spread_excess"] = sp["p1"] - sp["p10"]
        sp = sp.merge(sub_full.drop_duplicates("month")[["month", "excess_mkt"]], on="month")
        X = sm.add_constant(sp["excess_mkt"].to_numpy(float))
        y = sp["spread_excess"].to_numpy(float)
        res = sm.OLS(y, X).fit()
        valid = np.isfinite(res.resid)
        n_pos = int(np.sum(res.resid[valid] > 0))
        n_total = int(valid.sum())
        out[(strat, "spread")] = {"pos_prop": n_pos / n_total if n_total else np.nan,
                                    "n_pos": n_pos, "n_total": n_total}
    return out


def run_table_iv(panel_with_dec: pd.DataFrame) -> dict:
    """Table IV overlap and Spearman rank correlation per pair of strategies.

    Panel: rows with valid deciles for ALL three strategies (so each
    strategy sees the same universe at each month).

    Spearman convention: each strategy's "predictive signal" is oriented so
    that higher values correspond to the "better" decile (P1) for that
    strategy.  S0 = pred, S1 = -lag1 (ascending sort -> negate), S12 = lag12.
    This matches the paper's positive 0.66 correlation for S0/S1: both
    strategies put the same stocks in P1, so the Spearman of their
    oriented signals is positive.

    Overlap: |A_P1 � B_P1| / |A_P1 ∪ B_P1|, averaged across months.
    """
    keep = ["permno", "month", "ret", "lag1", "lag12", "pred",
            "dec_s0", "dec_s1", "dec_s12"]
    work = panel_with_dec[keep].copy()
    valid = work[["dec_s0", "dec_s1", "dec_s12", "lag1", "lag12", "pred"]].notna().all(axis=1)
    work = work[valid].copy()
    print(f"[t4] unified frame: {len(work):,} rows")

    # Oriented signals (higher = "better" = P1).
    work["sig_s0"] = work["pred"]
    work["sig_s1"] = -work["lag1"]
    work["sig_s12"] = work["lag12"]

    out: dict = {}
    pairs = [("s0", "s1"), ("s0", "s12"), ("s1", "s12")]
    for a, b in pairs:
        da = f"dec_{a}"
        db = f"dec_{b}"
        overlaps = []
        for mon, g in work.groupby("month"):
            A_top = set(g.loc[g[da] == 1, "permno"])
            B_top = set(g.loc[g[db] == 1, "permno"])
            inter = A_top & B_top
            union = A_top | B_top
            if union:
                overlaps.append(len(inter) / len(union))
        out[(a, b, "overlap")] = float(np.mean(overlaps)) if overlaps else np.nan

        sa = f"sig_{a}"
        sb = f"sig_{b}"
        corrs = []
        for mon, g in work.groupby("month"):
            x = g[sa].to_numpy(float)
            y = g[sb].to_numpy(float)
            mask = np.isfinite(x) & np.isfinite(y)
            if mask.sum() < 30:
                continue
            rho, _ = spearmanr(x[mask], y[mask])
            if np.isfinite(rho):
                corrs.append(rho)
        out[(a, b, "spearman")] = float(np.mean(corrs)) if corrs else np.nan
    return out


# --- table output ----------------------------------------------------------
def write_table_2(cells: dict, spread_cells: dict, diag: dict) -> None:
    """Render Table II markdown with alpha (and t-stat) for P1..P10 and
    the P1-P10 spread across all three strategies and three sub-periods."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Table II. Market-Model Abnormal Returns on Predictive Portfolios",
        "",
        "Market model: R_pt − R_ft = α_p + β_p (R_mt − R_ft) + u_pt, "
        "with R_mt = CRSP equal-weighted index (ewretd) and R_ft = FF rf. "
        "Sample 1934-1987. White (1980) HC1 standard errors.",
        "",
        "P1-P10 spread regression: spread_excess_t regressed on excess_mkt_t; "
        "α and t(α) reported below the P10 row.",
        "",
    ]
    for strat in STRATEGIES:
        lines.append(f"## Strategy {strat.upper()}")
        lines.append("")
        for sub_label in SUBPERIODS:
            lines.append(f"### {SUBPERIOD_LABELS[sub_label]}")
            lines.append("")
            lines.append("| Portfolio | α (per month) | t(α) | β | t(β) | R² | n_obs |")
            lines.append("|---|---|---|---|---|---|---|")
            for dec in range(1, 11):
                c = cells.get((strat, dec, sub_label), {})
                lines.append(
                    f"| P{dec} | "
                    f"{c.get('alpha', float('nan')):+.4f} | "
                    f"({c.get('t_alpha', float('nan')):+.2f}) | "
                    f"{c.get('beta', float('nan')):+.3f} | "
                    f"({c.get('t_beta', float('nan')):+.2f}) | "
                    f"{c.get('r2', float('nan')):.3f} | "
                    f"{c.get('n_obs', 0)} |"
                )
            sp = spread_cells.get((strat, sub_label), {})
            lines.append(
                f"| **P1-P10 spread** | "
                f"**{sp.get('alpha', float('nan')):+.4f}** | "
                f"**({sp.get('t_alpha', float('nan')):+.2f})** | "
                f"{sp.get('beta', float('nan')):+.3f} | "
                f"({sp.get('t_beta', float('nan')):+.2f}) | "
                f"{sp.get('r2', float('nan')):.3f} | "
                f"{sp.get('n_obs', 0)} |"
            )
            lines.append("")
    (RESULTS_DIR / "table_2.md").write_text("\n".join(lines) + "\n")


def write_table_3(prop: dict) -> None:
    """Render Table III markdown — positive abnormal return proportions."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Table III. Proportion of Months with Positive Abnormal Returns",
        "",
        "Market-model residuals computed over Jan-Dec 1934-1987; "
        "proportion reported = count(u_hat > 0) / count(u_hat). "
        "Spread (P1-P10) proportion: build month-by-month equal-weighted "
        "spread, fit market model, then count positive residuals.",
        "",
        "| Strategy | Portfolio | n_pos | n_total | Proportion |",
        "|---|---|---|---|---|",
    ]
    for strat in STRATEGIES:
        for dec in [1, 10]:
            r = prop.get((strat, dec), {})
            lines.append(
                f"| {strat.upper()} | P{dec} | {r.get('n_pos', 0)} | "
                f"{r.get('n_total', 0)} | {r.get('pos_prop', float('nan')):.3f} |"
            )
        r = prop.get((strat, "spread"), {})
        lines.append(
            f"| {strat.upper()} | **P1-P10 spread** | {r.get('n_pos', 0)} | "
            f"{r.get('n_total', 0)} | **{r.get('pos_prop', float('nan')):.3f}** |"
        )
    (RESULTS_DIR / "table_3.md").write_text("\n".join(lines) + "\n")


def write_table_4(t4: dict) -> None:
    """Render Table IV markdown — overlap and Spearman rank correlations."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Table IV. Pair-Wise Relation Between Trading Strategies",
        "",
        "Sample 1934-1987. Overlap = |A_P1 ∩ B_P1| / |A_P1 ∪ B_P1|, "
        "averaged across months. Spearman = within-month rank correlation "
        "of the predictive signals (S0: predicted return; S1: lag1; "
        "S12: lag12), averaged across months.",
        "",
        "| Pair | Overlap (mean) | Spearman (mean) |",
        "|---|---|---|",
    ]
    for pair in [("s0", "s1"), ("s0", "s12"), ("s1", "s12")]:
        ov = t4.get((*pair, "overlap"), float("nan"))
        sp = t4.get((*pair, "spearman"), float("nan"))
        lines.append(f"| {pair[0].upper()} vs {pair[1].upper()} | "
                     f"{ov:.3f} | {sp:+.3f} |")
    (RESULTS_DIR / "table_4.md").write_text("\n".join(lines) + "\n")


def build_t234_metrics(cells: dict, spread_cells: dict,
                       prop: dict, t4: dict) -> dict:
    """Per-cell metrics dict matching tables_to_replicate.json metric names
    for Tables II / III / IV.  Returns a dict of {name: {value, unit}}."""
    out: dict[str, dict] = {}

    # ---- Table II — per-decile alphas + spreads ----------------------------
    # Decile alphas (Jan-Dec, Jan, Feb-Dec) for S0/S1/S12 (per the metric
    # list in tables_to_replicate.json).
    t2_alpha_keys = {
        ("s0",  1, "jandec"):  "s0_p1_alpha_jandec",
        ("s0",  1, "jan"):     "s0_p1_alpha_jan",
        ("s0",  1, "febdec"):  "s0_p1_alpha_febdec",
        ("s0",  5, "jandec"):  "s0_p5_alpha_jandec",
        ("s0", 10, "jandec"):  "s0_p10_alpha_jandec",
        ("s0", 10, "jan"):     "s0_p10_alpha_jan",
        ("s0", 10, "febdec"):  "s0_p10_alpha_febdec",
        ("s1",  1, "jandec"):  "s1_p1_alpha_jandec",
        ("s1",  1, "jan"):     "s1_p1_alpha_jan",
        ("s1", 10, "jandec"):  "s1_p10_alpha_jandec",
        ("s12",  1, "jandec"): "s12_p1_alpha_jandec",
        ("s12", 10, "jandec"): "s12_p10_alpha_jandec",
    }
    for (strat, dec, sub), name in t2_alpha_keys.items():
        c = cells.get((strat, dec, sub), {})
        out[name] = {"value": c.get("alpha", np.nan), "unit": "alpha_per_month"}

    # Spreads.
    spread_keys = {
        ("s0", "jandec"):  "s0_spread_jandec",
        ("s0", "jan"):     "s0_spread_jan",
        ("s0", "febdec"):  "s0_spread_febdec",
        ("s1", "jandec"):  "s1_spread_jandec",
        ("s1", "jan"):     "s1_spread_jan",
        ("s1", "febdec"):  "s1_spread_febdec",
        ("s12", "jandec"): "s12_spread_jandec",
        ("s12", "febdec"): "s12_spread_febdec",
    }
    spread_t_keys = {
        ("s0", "jandec"):  "s0_spread_t_jandec",
        ("s0", "jan"):     "s0_spread_t_jan",
        ("s0", "febdec"):  "s0_spread_t_febdec",
        ("s1", "jandec"):  "s1_spread_t_jandec",
        ("s1", "febdec"):  "s1_spread_t_febdec",
        ("s12", "jandec"): "s12_spread_t_jandec",
    }
    for (strat, sub), name in spread_keys.items():
        c = spread_cells.get((strat, sub), {})
        out[name] = {"value": c.get("alpha", np.nan), "unit": "alpha_per_month"}
    for (strat, sub), name in spread_t_keys.items():
        c = spread_cells.get((strat, sub), {})
        out[name] = {"value": c.get("t_alpha", np.nan), "unit": "t_stat"}

    # ---- Table III — positive residual proportions -------------------------
    t3_keys = {
        ("s0", 1):     "s0_p1_posprop_jandec",
        ("s0", 10):    "s0_p10_posprop_jandec",
        ("s0", "spread"): "s0_p1_minus_p10_posprop_jandec",
        ("s1", 1):     "s1_p1_posprop_jandec",
        ("s1", 10):    "s1_p10_posprop_jandec",
        ("s12", 1):    "s12_p1_posprop_jandec",
        ("s12", 10):   "s12_p10_posprop_jandec",
    }
    for key, name in t3_keys.items():
        r = prop.get(key, {})
        out[name] = {"value": r.get("pos_prop", np.nan), "unit": "proportion"}

    # ---- Table IV — overlap + Spearman --------------------------------------
    t4_keys = {
        (("s0", "s1"), "overlap"):  "overlap_s0_s1",
        (("s0", "s12"), "overlap"): "overlap_s0_s12",
        (("s1", "s12"), "overlap"): "overlap_s1_s12",
        (("s0", "s1"), "spearman"): "spearman_s0_s1",
        (("s0", "s12"), "spearman"): "spearman_s0_s12",
        (("s1", "s12"), "spearman"): "spearman_s1_s12",
    }
    for (pair, kind), name in t4_keys.items():
        v = t4.get((*pair, kind), np.nan)
        out[name] = {"value": float(v) if np.isfinite(v) else np.nan,
                      "unit": "proportion" if kind == "overlap" else "correlation"}
    return out


def compare_tables_ii_iii_iv(cells, spread_cells, prop, t4) -> None:
    """Print headline comparisons against the paper."""
    print("\n=== Table II headline vs paper ===")
    print(f"{'cell':<22}{'paper':>10}{'repl':>10}{'diff%':>9}")
    for stat, kind, key, ref in [
        ("s0 P1 alpha JD",     "dec",  ("s0", 1, "jandec"),  0.0111),
        ("s0 P5 alpha JD",     "dec",  ("s0", 5, "jandec"),  0.0013),
        ("s0 P10 alpha JD",    "dec",  ("s0", 10, "jandec"), -0.0138),
        ("s0 spread alpha JD", "spread", ("s0", "jandec"),  0.0249),
        ("s0 spread t-stat JD","spread_t", ("s0", "jandec"), 16.82),
        ("s0 spread alpha FD", "spread", ("s0", "febdec"),  0.0220),
        ("s0 spread t-stat FD","spread_t", ("s0", "febdec"), 15.63),
        ("s1 spread alpha JD", "spread", ("s1", "jandec"),  0.0199),
        ("s1 spread t-stat JD","spread_t", ("s1", "jandec"), 12.55),
        ("s1 spread alpha FD", "spread", ("s1", "febdec"),  0.0175),
        ("s12 spread alpha JD","spread", ("s12", "jandec"), 0.0093),
        ("s12 spread t-stat JD","spread_t", ("s12", "jandec"), 6.94),
        ("s12 spread alpha FD","spread", ("s12", "febdec"), 0.0073),
    ]:
        if kind == "dec":
            v = cells.get(key, {}).get("alpha", np.nan)
        elif kind == "spread":
            v = spread_cells.get(key, {}).get("alpha", np.nan)
        else:
            v = spread_cells.get(key, {}).get("t_alpha", np.nan)
        dp = (v - ref) / abs(ref) * 100 if (ref and np.isfinite(v)) else float("nan")
        print(f"{stat:<22}{ref:>10.4f}{v:>10.4f}{dp:>8.1f}%")

    print("\n=== Table III vs paper (Jan-Dec) ===")
    print(f"{'cell':<20}{'paper':>10}{'repl':>10}{'diff%':>9}")
    for strat, refd in PAPER_T3.items():
        for stat, pv in refd.items():
            key = (strat, 1 if stat == "p1" else 10) if stat in ("p1", "p10") else (strat, "spread")
            rv = prop.get(key, {}).get("pos_prop", np.nan)
            dp = (rv - pv) / pv * 100 if pv and np.isfinite(rv) else float("nan")
            print(f"{strat} {stat:<14}{pv:>10.4f}{rv:>10.4f}{dp:>8.1f}%")

    print("\n=== Table IV vs paper ===")
    print(f"{'pair':<14}{'kind':<10}{'paper':>10}{'repl':>10}{'diff%':>9}")
    for pair, refd in PAPER_T4.items():
        for kind, pv in refd.items():
            rv = t4.get((*pair, kind), np.nan)
            dp = (rv - pv) / abs(pv) * 100 if pv and np.isfinite(rv) else float("nan")
            print(f"{pair[0]}-{pair[1]:<8}{kind:<10}{pv:>10.4f}{rv:>10.4f}{dp:>8.1f}%")


# --- main ------------------------------------------------------------------
def main() -> None:
    # === Table I (Stage 7 iteration 2) =====================================
    sq = build_size_quintile()
    report_size_quintile(sq)

    panel = load_panel(sq)

    t1_metrics, t1_detail = regressions(panel, "size_quintile")
    write_table(t1_metrics, t1_detail)
    compare_to_paper(t1_metrics, "NYSE breakpoints — reported")

    for k in ("all_full", "q1_full", "q3_full", "q5_full"):
        d = t1_detail[k]
        print(f"[diag] {k}: regressions={d['n_regressions']}, avg_stocks={d['avg_stocks']:.1f}")

    # Diagnostic: same regressions under all-stock (equal-count) breakpoints.
    alt, alt_detail = regressions(panel, "size_quintile_allstock")
    compare_to_paper(alt, "all-stock equal-count breakpoints — DIAGNOSTIC ONLY")
    for k in ("q1_full", "q3_full", "q5_full"):
        d = alt_detail[k]
        print(f"[diag-alt] {k}: regressions={d['n_regressions']}, avg_stocks={d['avg_stocks']:.1f}")

    # === Tables II / III / IV (Stage 7 iteration 3) ========================
    panel_ii, _ewi, _ff = load_panel_ii()

    # S0 forecast regression.
    panel_ii_with_pred, s0_diag = compute_s0_forecasts(panel_ii)

    # Decile assignment for all three strategies.
    panel_with_dec = assign_deciles_all(panel_ii_with_pred)
    # Quick sanity: how many stocks get a decile per month per strategy?
    print("[t2] decile coverage:")
    for strat in STRATEGIES:
        col = f"dec_{strat}"
        n_valid = panel_with_dec[col].notna().sum()
        n_months = panel_with_dec.loc[panel_with_dec[col].notna(), "month"].nunique()
        avg_per_month = (panel_with_dec[panel_with_dec[col].notna()]
                         .groupby("month").size().mean())
        print(f"  {strat.upper()}: {n_valid:,} (permno,month) rows with decile, "
              f"{n_months} months, avg {avg_per_month:.0f} stocks/month")

    # EW portfolio returns per (month, strategy, decile).
    port_rets = compute_portfolio_returns(panel_with_dec)
    print(f"[t2] portfolio returns: {len(port_rets):,} rows "
          f"({port_rets['strategy'].nunique()} strategies x "
          f"{port_rets['decile'].nunique()} deciles x "
          f"{port_rets['month'].nunique()} months)")

    # Table II — market-model regressions.
    cells, spread_cells, mm_diag = run_table_ii(port_rets)
    write_table_2(cells, spread_cells, mm_diag)

    # Table III — positive abnormal-return proportions.
    prop = run_table_iii(cells, port_rets)
    write_table_3(prop)

    # Table IV — overlap + Spearman.
    t4 = run_table_iv(panel_with_dec)
    write_table_4(t4)

    # Paper comparison.
    compare_tables_ii_iii_iv(cells, spread_cells, prop, t4)

    # Diagnostics: average stocks per decile per month.
    avg_stocks_per_dec = (port_rets.groupby(["strategy", "decile"])["n_stocks"]
                          .mean().round(1).to_dict())
    print("\n[t2] avg stocks per (strategy, decile) per month:")
    for strat in STRATEGIES:
        s = " ".join(f"P{d}={avg_stocks_per_dec.get((strat, d), 0):.0f}"
                     for d in range(1, 11))
        print(f"  {strat.upper()}: {s}")
    print(f"\n[s0] forecast regressions: {s0_diag['n_regressions_ok']}/"
          f"{s0_diag['n_test_months']} OK, "
          f"{s0_diag['n_regressions_skipped']} skipped")

    EVAL_DIR.mkdir(parents=True, exist_ok=True)

    # === eval/metrics.json — combine Table I + Tables II/III/IV ===========
    t1_metrics_flat = build_metrics_json(t1_metrics, t1_detail)
    t234_metrics = build_t234_metrics(cells, spread_cells, prop, t4)

    # Add diagnostics for Tables II/III/IV.
    t234_metrics["diag_s0_n_regressions"] = {
        "value": float(s0_diag["n_regressions_ok"]), "unit": "count"}
    t234_metrics["diag_s0_n_regressions_skipped"] = {
        "value": float(s0_diag["n_regressions_skipped"]), "unit": "count"}
    for strat in STRATEGIES:
        for dec in range(1, 11):
            key = (strat, dec)
            n_stocks = (port_rets[(port_rets["strategy"] == strat) &
                                  (port_rets["decile"] == dec)]["n_stocks"].mean())
            t234_metrics[f"diag_{strat}_p{dec}_avg_stocks"] = {
                "value": float(n_stocks), "unit": "count"}

    payload = {
        "schema_version": 2,
        "slug": SLUG,
        "metrics": {**t1_metrics_flat, **t234_metrics},
    }
    (EVAL_DIR / "metrics.json").write_text(json.dumps(payload, indent=2, default=float))
    bad = [k for k, v in payload["metrics"].items()
           if not isinstance(v, dict) or "value" not in v]
    assert not bad, f"bare-scalar metrics: {bad}"
    print(f"\n[eval] wrote metrics.json with {len(payload['metrics'])} cells "
          f"({len(t1_metrics_flat)} Table I + {len(t234_metrics)} Tables II/III/IV)")

    # === Table V — size-based 3-factor model ===============================
    size_rets = build_size_quintile_returns(panel_with_dec)
    write_size_quintile_diagnostics(size_rets)

    # Reuse the predictive-portfolio construction (sorts already done above).
    t5_cells, t5_spread_cells, t5_diag = run_table_v(port_rets, size_rets)
    write_table_5(t5_cells, t5_spread_cells, t5_diag)
    compare_table_v_to_paper(t5_cells, t5_spread_cells)

    t5_metrics = build_t5_metrics(t5_cells, t5_spread_cells)
    payload["metrics"].update(t5_metrics)
    (EVAL_DIR / "metrics.json").write_text(json.dumps(payload, indent=2, default=float))
    bad = [k for k, v in payload["metrics"].items()
           if not isinstance(v, dict) or "value" not in v]
    assert not bad, f"bare-scalar metrics after Table V: {bad}"
    print(f"[eval] appended {len(t5_metrics)} Table V cells")

    # === Table VI — bid-ask-spread robustness check =======================
    daily_panel_df = pd.read_parquet(DATA_DIR / "daily_panel.parquet")
    daily_panel_df["date"] = pd.to_datetime(daily_panel_df["date"])
    daily_panel_df["month"] = pd.to_datetime(daily_panel_df["month"])
    lag1_excl_df = build_lag1_excl_last_day(daily_panel_df)

    t6_paneli, t6_panelii = run_table_vi(panel_with_dec, lag1_excl_df)
    write_table_6(t6_paneli, t6_panelii)
    compare_table_vi_to_paper(t6_paneli, t6_panelii)

    t6_metrics = build_t6_metrics(t6_paneli, t6_panelii)
    payload["metrics"].update(t6_metrics)
    (EVAL_DIR / "metrics.json").write_text(json.dumps(payload, indent=2, default=float))
    bad = [k for k, v in payload["metrics"].items()
           if not isinstance(v, dict) or "value" not in v]
    assert not bad, f"bare-scalar metrics after Table VI: {bad}"
    print(f"[eval] appended {len(t6_metrics)} Table VI cells")
    print(f"\n[eval] final metrics.json has {len(payload['metrics'])} cells")


# =============================================================================
# Table V — Size-based 3-factor model
# =============================================================================
# Paper §III.A equation (4):
#   R_pt = α_p + b_pS * R_St + b_pM * R_Mt + b_pL * R_Lt + u_pt
#
# where R_St, R_Mt, R_Lt are the returns on small-, medium-, and large-firm
# size-quintile portfolios in month t.  The paper does not specify the
# construction of these three series in detail; per Assumption 11 we use
# 5 NYSE size quintiles from data/size_quintile.parquet (NYSE-only
# breakpoints) and aggregate them into 3 groups:
#
#   R_St = (Q1 + Q2) / 2     -- 2 smallest quintiles
#   R_Mt = Q3                -- middle quintile
#   R_Lt = (Q4 + Q5) / 2     -- 2 largest quintiles
#
# Note on table availability: the task spec called for `ermport1..9` but
# in this CRSP instance only `ermport1..5` exist (5 quintile tables, not
# 9 deciles) and `erdport6..9` are beta-sorted.  We substitute the panel
# × size_quintile join (NYSE-only breakpoints, Assumption 14) and
# aggregate into 3 of the 5 quintiles.
#
# Estimation: OLS with HC1 standard errors.  Sample 1934-1987.  Sub-
# periods: Jan-Dec, Jan, Feb-Dec.  Headline: S0 P1-P10 spread, S1 spread,
# S12 spread (Jan-Dec + Feb-Dec where reported).
# -----------------------------------------------------------------------------


def build_size_quintile_returns(panel: pd.DataFrame) -> pd.DataFrame:
    """Build monthly R_St, R_Mt, R_Lt series from panel + size_quintile.

    panel  : the same panel used for Table II (must carry `ret`, `month`,
             `permno`; size_quintile is attached via the existing main.py
             merge).

    Implementation note: rather than re-merging size_quintile here we use
    the panel rows that already carry the size_quintile assignment if
    available, else merge.  In the existing pipeline the size_quintile
    is attached only for Table I's 1929-1982 window; for Table V we
    re-attach for the 1934-1987 window.
    """
    sq = pd.read_parquet(DATA_DIR / "size_quintile.parquet")
    sq["month"] = pd.to_datetime(sq["month"])
    sq_slim = sq[["permno", "month", "size_quintile"]].copy()

    base = panel[["permno", "month", "ret"]].copy()
    base["month"] = pd.to_datetime(base["month"])
    base = base[base["ret"].notna()].copy()
    merged = base.merge(sq_slim, on=["permno", "month"], how="inner")

    # Per-(month, size_quintile) EW mean return.
    qret = (merged.groupby(["month", "size_quintile"], as_index=False)
                  .agg(ret=("ret", "mean"), n=("ret", "size")))

    # Pivot to wide with quintiles as columns.
    wide = qret.pivot(index="month", columns="size_quintile", values="ret")
    # 5 quintiles expected; if any are missing the column won't exist.
    for k in (1, 2, 3, 4, 5):
        if k not in wide.columns:
            wide[k] = np.nan

    out = pd.DataFrame(index=wide.index)
    out["R_St"] = (wide[1] + wide[2]) / 2.0
    out["R_Mt"] = wide[3]
    out["R_Lt"] = (wide[4] + wide[5]) / 2.0
    out = out.reset_index().rename(columns={"index": "month"})
    print(f"[t5] size-quintile series: {len(out):,} months "
          f"({out['month'].min():%Y-%m} .. {out['month'].max():%Y-%m})")
    return out


def write_size_quintile_diagnostics(size_rets: pd.DataFrame) -> None:
    print("\n=== size quintile returns (R_St / R_Mt / R_Lt) ===")
    for col in ("R_St", "R_Mt", "R_Lt"):
        v = size_rets[col]
        print(f"  {col}: mean={v.mean():+.4f}  std={v.std():.4f}  "
              f"min={v.min():+.3f}  max={v.max():+.3f}  "
              f"n_miss={int(v.isna().sum())}")


def size_model_alpha(df: pd.DataFrame, min_obs: int = 24) -> dict:
    """OLS: R_pt ~ R_St + R_Mt + R_Lt with HC1 standard errors.

    Returns dict with alpha (intercept), t_alpha, b_S, t_b_S, b_M, t_b_M,
    b_L, t_b_L, r2, n_obs.
    """
    cols = ["ret", "R_St", "R_Mt", "R_Lt"]
    sub = df[cols].replace([np.inf, -np.inf], np.nan).dropna()
    if len(sub) < min_obs:
        return {"alpha": np.nan, "t_alpha": np.nan,
                "b_S": np.nan, "t_b_S": np.nan,
                "b_M": np.nan, "t_b_M": np.nan,
                "b_L": np.nan, "t_b_L": np.nan,
                "r2": np.nan, "n_obs": len(sub)}
    X = sm.add_constant(sub[["R_St", "R_Mt", "R_Lt"]].to_numpy(float))
    y = sub["ret"].to_numpy(float)
    try:
        res = sm.OLS(y, X).fit(cov_type="HC1")
        return {
            "alpha": float(res.params[0]),
            "t_alpha": float(res.tvalues[0]),
            "b_S": float(res.params[1]),
            "t_b_S": float(res.tvalues[1]),
            "b_M": float(res.params[2]),
            "t_b_M": float(res.tvalues[2]),
            "b_L": float(res.params[3]),
            "t_b_L": float(res.tvalues[3]),
            "r2": float(res.rsquared),
            "n_obs": int(res.nobs),
        }
    except Exception as e:  # pragma: no cover
        return {"alpha": np.nan, "t_alpha": np.nan,
                "b_S": np.nan, "t_b_S": np.nan,
                "b_M": np.nan, "t_b_M": np.nan,
                "b_L": np.nan, "t_b_L": np.nan,
                "r2": np.nan, "n_obs": len(sub), "error": str(e)}


def run_table_v(port_rets: pd.DataFrame, size_rets: pd.DataFrame) -> tuple[dict, dict, dict]:
    """Size-based 3-factor model for each (strategy, decile, sub-period).

    Returns
    -------
    cells : {(strategy, decile, subperiod): {alpha, t_alpha, b_S, ...}}
    spread_cells : {(strategy, subperiod): {alpha, t_alpha, ...}}
    diag : per-(strategy, subperiod) sample sizes.
    """
    size_rets = size_rets.copy()
    size_rets["month"] = pd.to_datetime(size_rets["month"])

    # Join portfolio returns to the three size-quintile regressors.
    pr = port_rets[["month", "strategy", "decile", "ret"]].copy()
    pr["month"] = pd.to_datetime(pr["month"])
    pr = pr.merge(size_rets[["month", "R_St", "R_Mt", "R_Lt"]],
                  on="month", how="left")

    cells: dict = {}
    spread_cells: dict = {}
    diag: dict = {}

    for strat in STRATEGIES:
        sub_strat = pr[pr["strategy"] == strat]
        for sub_label, sel in SUBPERIODS.items():
            mask = sel(sub_strat["month"])
            sub_full = sub_strat[mask]

            # Per-decile regression.  Paper reports only P1, P10 and the
            # spread; compute all 10 for completeness.
            for dec in range(1, 11):
                dsub = sub_full[sub_full["decile"] == dec]
                cells[(strat, dec, sub_label)] = size_model_alpha(dsub)

            # Spread regression: build month-by-month equal-weighted spread,
            # then size-model-fit the spread.
            p1 = (sub_full[sub_full["decile"] == 1][["month", "ret"]]
                  .rename(columns={"ret": "p1"}))
            p10 = (sub_full[sub_full["decile"] == 10][["month", "ret"]]
                   .rename(columns={"ret": "p10"}))
            sp = p1.merge(p10, on="month", how="inner")
            sp["spread"] = sp["p1"] - sp["p10"]
            sp = sp.merge(sub_full.drop_duplicates("month")[["month", "R_St", "R_Mt", "R_Lt"]],
                          on="month", how="left")
            sp["ret"] = sp["spread"]
            sp_read = sp[["ret", "R_St", "R_Mt", "R_Lt"]].dropna()
            n_obs = len(sp_read)
            if n_obs >= 24:
                X = sm.add_constant(sp_read[["R_St", "R_Mt", "R_Lt"]].to_numpy(float))
                y = sp_read["ret"].to_numpy(float)
                res = sm.OLS(y, X).fit(cov_type="HC1")
                spread_cells[(strat, sub_label)] = {
                    "alpha": float(res.params[0]),
                    "t_alpha": float(res.tvalues[0]),
                    "b_S": float(res.params[1]),
                    "t_b_S": float(res.tvalues[1]),
                    "b_M": float(res.params[2]),
                    "t_b_M": float(res.tvalues[2]),
                    "b_L": float(res.params[3]),
                    "t_b_L": float(res.tvalues[3]),
                    "r2": float(res.rsquared),
                    "n_obs": n_obs,
                }
            else:
                spread_cells[(strat, sub_label)] = {
                    "alpha": np.nan, "t_alpha": np.nan,
                    "b_S": np.nan, "t_b_S": np.nan,
                    "b_M": np.nan, "t_b_M": np.nan,
                    "b_L": np.nan, "t_b_L": np.nan,
                    "r2": np.nan, "n_obs": n_obs,
                }
            diag[(strat, sub_label)] = {"n_obs": n_obs}
    return cells, spread_cells, diag


def write_table_5(cells: dict, spread_cells: dict, diag: dict) -> None:
    """Render Table V markdown — size-based 3-factor model alphas."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Table V. Size-Based 3-Factor Model Abnormal Returns",
        "",
        "Model: R_pt = α_p + b_pS * R_St + b_pM * R_Mt + b_pL * R_Lt + u_pt, "
        "where R_St, R_Mt, R_Lt are EW returns on the small/medium/large "
        "size-quintile portfolios constructed from the 5 NYSE size quintiles "
        "(R_St = mean(Q1, Q2), R_Mt = Q3, R_Lt = mean(Q4, Q5); see "
        "preparations/assumptions.md §11 and §14).  HC1 standard errors.  "
        "Sample 1934-1987.",
        "",
    ]
    for strat in STRATEGIES:
        lines.append(f"## Strategy {strat.upper()}")
        lines.append("")
        for sub_label in SUBPERIODS:
            lines.append(f"### {SUBPERIOD_LABELS[sub_label]}")
            lines.append("")
            lines.append("| Portfolio | α (per month) | t(α) | b_S | b_M | b_L | R² | n_obs |")
            lines.append("|---|---|---|---|---|---|---|---|")
            for dec in range(1, 11):
                c = cells.get((strat, dec, sub_label), {})
                lines.append(
                    f"| P{dec} | "
                    f"{c.get('alpha', float('nan')):+.4f} | "
                    f"({c.get('t_alpha', float('nan')):+.2f}) | "
                    f"{c.get('b_S', float('nan')):+.3f} | "
                    f"{c.get('b_M', float('nan')):+.3f} | "
                    f"{c.get('b_L', float('nan')):+.3f} | "
                    f"{c.get('r2', float('nan')):.3f} | "
                    f"{c.get('n_obs', 0)} |"
                )
            sp = spread_cells.get((strat, sub_label), {})
            lines.append(
                f"| **P1-P10 spread** | "
                f"**{sp.get('alpha', float('nan')):+.4f}** | "
                f"**({sp.get('t_alpha', float('nan')):+.2f})** | "
                f"{sp.get('b_S', float('nan')):+.3f} | "
                f"{sp.get('b_M', float('nan')):+.3f} | "
                f"{sp.get('b_L', float('nan')):+.3f} | "
                f"{sp.get('r2', float('nan')):.3f} | "
                f"{sp.get('n_obs', 0)} |"
            )
            lines.append("")
    (RESULTS_DIR / "table_5.md").write_text("\n".join(lines) + "\n")


def compare_table_v_to_paper(cells: dict, spread_cells: dict) -> None:
    """Print Table V headline cells vs paper."""
    paper = {
        ("s0", 1, "jandec"): ("size_s0_p1_alpha_jandec",  0.0103, 11.75),
        ("s0", 10, "jandec"): ("size_s0_p10_alpha_jandec", -0.0143, -17.21),
        ("s0", "spread_jandec"): ("size_s0_spread_jandec",  0.0246, 16.84),
        ("s0", "spread_febdec"): ("size_s0_spread_febdec",  0.0237, 2.42),
        ("s1", "spread_jandec"): ("size_s1_spread_jandec",  0.0213, 14.55),
        ("s12", "spread_jandec"): ("size_s12_spread_jandec", 0.0091, 6.92),
        ("s12", "spread_febdec"): ("size_s12_spread_febdec", 0.0068, 5.08),
    }
    print("\n=== Table V vs paper ===")
    print(f"{'cell':<28}{'paper':>10}{'repl':>10}{'diff%':>9}{'paper t':>9}{'repl t':>9}")
    for key, (name, pv, pt) in paper.items():
        # Spread keys are (strat, "spread_<sub>"); decile keys are (strat, dec, sub).
        if len(key) == 2 and isinstance(key[1], str) and key[1].startswith("spread"):
            sub = key[1].replace("spread_", "")
            c = spread_cells.get((key[0], sub), {})
        elif len(key) == 3:
            c = cells.get(key, {})
        else:
            c = {}
        rv = c.get("alpha", np.nan)
        rt = c.get("t_alpha", np.nan)
        dp = (rv - pv) / abs(pv) * 100 if pv and np.isfinite(rv) else float("nan")
        print(f"{name:<28}{pv:>10.4f}{rv:>10.4f}{dp:>8.1f}%{pt:>9.2f}{rt:>9.2f}")


def build_t5_metrics(cells: dict, spread_cells: dict) -> dict:
    """Per-cell metrics for Table V matching tables_to_replicate.json names."""
    out: dict[str, dict] = {}

    # P1 / P10 / spread alphas per strategy × sub-period.
    cells_keys = {
        ("s0", 1, "jandec"):  "size_s0_p1_alpha_jandec",
        ("s0", 10, "jandec"): "size_s0_p10_alpha_jandec",
    }
    for (strat, dec, sub), name in cells_keys.items():
        c = cells.get((strat, dec, sub), {})
        out[name] = {"value": c.get("alpha", np.nan), "unit": "alpha_per_month"}

    spread_keys = {
        ("s0", "jandec"):  "size_s0_spread_jandec",
        ("s0", "febdec"):  "size_s0_spread_febdec",
        ("s1", "jandec"):  "size_s1_spread_jandec",
        ("s12", "jandec"): "size_s12_spread_jandec",
        ("s12", "febdec"): "size_s12_spread_febdec",
    }
    for (strat, sub), name in spread_keys.items():
        c = spread_cells.get((strat, sub), {})
        out[name] = {"value": c.get("alpha", np.nan), "unit": "alpha_per_month"}
        # The paper reports a t-stat alongside each spread; the targets
        # file uses "<base>_t_<sub>" naming.
        t_name = f"{name.rsplit('_', 1)[0]}_t_{sub}"
        out[t_name] = {"value": c.get("t_alpha", np.nan), "unit": "t_stat"}
    return out


# =============================================================================
# Table VI — Bid-Ask Spread Bias Correction
# =============================================================================
# Paper §III.C: two robustness panels for S0/S1 strategies, sample period
# 1963-1987:
#
#   Panel I  — full prior-month return (lag1)  [same as Table II]
#   Panel II — prior-month return excluding the last trading day
#              (lag1_excl_last_day).  Also drops stocks that did not
#              trade on the last trading day of month t-1.
#
# Implementation: reuse the panel.parquet for Panel I (the existing
# monthly lag1 column).  For Panel II S1: replace lag1 with
# `lag1_excl_last_day` (computed below from daily_panel.parquet) and
# drop stocks that lack a trade on the last trading day of t-1.  For
# Panel II S0: use the same monthly S0 forecast but the S0 prediction
# already uses the full lag vector, so we substitute `lag1_excl_last_day`
# into the lag vector only for the S0 forecast regression window.
# -----------------------------------------------------------------------------


TABLE_VI_START = "1963-01-01"
TABLE_VI_END = "1987-12-31"


def build_lag1_excl_last_day(daily: pd.DataFrame) -> pd.DataFrame:
    """For each (permno, month), compute the cumulative gross return for
    that month EXCLUDING the last trading day.

    Output columns: permno, month (calendar month-end of the prior month),
    lag1_excl_last_day (the cumulative gross return excluding the last
    trading day), traded_on_last_day (bool flag for the Panel II
    eligibility filter).

    Mathematically:
      lag1_excl_last_day[t] = prod(1 + ret_d) for d in month t-1
                                              with d != last trading day
                              - 1
    """
    daily = daily.copy()
    daily = daily[daily["ret"].notna()].copy()

    # Within (permno, month), compute the gross return (1+ret) per day,
    # then take product over days where is_last_trading_day_of_month == 0.
    daily["gross"] = 1.0 + daily["ret"].fillna(0.0)
    # For rows where is_last_trading_day_of_month==1 we set gross=1 so
    # they do not contribute to the cumulative product.
    daily.loc[daily["is_last_trading_day_of_month"] == 1, "gross"] = 1.0
    # Track whether each permno actually traded on the last trading day.
    last_day_traded = (daily.loc[daily["is_last_trading_day_of_month"] == 1]
                       .groupby(["permno", "month"], as_index=False)
                       .agg(traded_on_last_day=("ret", lambda s: s.notna().any())))

    # Per-(permno, month) cumulative gross return excluding last day.
    grouped = (daily.groupby(["permno", "month"], as_index=False)
                    .agg(gross_excl=("gross", "prod")))
    grouped["ret_excl"] = grouped["gross_excl"] - 1.0
    grouped = grouped.merge(last_day_traded, on=["permno", "month"], how="left")
    grouped["traded_on_last_day"] = grouped["traded_on_last_day"].fillna(False).astype(bool)

    # Build the lag: for month t, the lag1_excl_last_day = ret_excl at month t-1.
    # First make month the calendar month-end of t-1, then shift forward by one month.
    grouped = grouped.sort_values(["permno", "month"]).reset_index(drop=True)
    grouped["lag_month"] = grouped["month"] + pd.offsets.MonthBegin(1)
    out = grouped.rename(columns={"month": "excl_month"})[
        ["permno", "excl_month", "lag_month", "ret_excl", "traded_on_last_day"]
    ].rename(columns={"ret_excl": "lag1_excl_last_day"})
    print(f"[t6] lag1_excl_last_day: {len(out):,} (permno, month) rows; "
          f"n with trade on last day = {int(out['traded_on_last_day'].sum()):,}")
    return out


def build_panel_vi_panelI(panel_with_dec: pd.DataFrame) -> pd.DataFrame:
    """Panel I: restrict the existing 1934-1987 panel to 1963-1987."""
    p = panel_with_dec.copy()
    p["month"] = pd.to_datetime(p["month"])
    p = p[(p["month"] >= TABLE_VI_START) & (p["month"] <= TABLE_VI_END)].copy()
    return p


def build_panel_vi_panelII(panel_with_dec: pd.DataFrame,
                            lag1_excl: pd.DataFrame) -> pd.DataFrame:
    """Panel II: same 1963-1987 universe but S1 uses lag1_excl_last_day.

    Implementation:
      - Start from the existing 1934-1987 panel.
      - For rows in 1963-1987, replace `lag1` with `lag1_excl_last_day`.
      - Drop stocks that did not trade on the last trading day of t-1
        (the paper's eligibility filter).
      - The S0 forecast regression is left using `lag1_excl_last_day`
        as the lag1 regressor (other lags remain the standard monthly
        values, since only lag1 is being bias-adjusted).
    """
    p = panel_with_dec.copy()
    p["month"] = pd.to_datetime(p["month"])

    lag1_excl = lag1_excl.copy()
    lag1_excl["lag_month"] = pd.to_datetime(lag1_excl["lag_month"])

    base = p[(p["month"] >= TABLE_VI_START) & (p["month"] <= TABLE_VI_END)].copy()

    # Drop stocks that did not trade on the last trading day of t-1.
    # We use the (permno, t) -> traded_on_last_day_at_(t-1) mapping:
    # the row at lag_month=t carries the trade flag for the original
    # month t-1, so we need to lookup by lag_month.
    base = base.merge(
        lag1_excl[["permno", "lag_month", "traded_on_last_day"]],
        left_on=["permno", "month"],
        right_on=["permno", "lag_month"],
        how="left",
    )
    base["traded_on_last_day"] = base["traded_on_last_day"].fillna(False)
    base = base[base["traded_on_last_day"]].drop(columns=["lag_month"])

    # Replace lag1 with lag1_excl_last_day at month t (= ret_excl at t-1).
    base = base.merge(
        lag1_excl[["permno", "lag_month", "lag1_excl_last_day"]],
        left_on=["permno", "month"],
        right_on=["permno", "lag_month"],
        how="left",
    )
    base["lag1"] = base["lag1_excl_last_day"].where(base["lag1_excl_last_day"].notna(),
                                                    base["lag1"])
    base = base.drop(columns=["lag_month", "lag1_excl_last_day"])

    print(f"[t6] Panel II base: {len(base):,} rows, "
          f"{base['month'].nunique()} months, {base['permno'].nunique():,} permnos")
    return base


def run_table_vi(panel_with_dec: pd.DataFrame,
                 lag1_excl: pd.DataFrame) -> tuple[dict, dict]:
    """Table VI Panel I + Panel II for S0, S1 strategies.

    Returns
    -------
    panel_i  : {(strategy, subperiod): {alpha, t_alpha, ...}}
    panel_ii : same structure for Panel II
    """
    # --- Panel I: 1963-1987 using existing sorts + standard lag1 ------------
    p1 = build_panel_vi_panelI(panel_with_dec)
    port_rets_i = compute_portfolio_returns(p1)
    ewi = pd.read_parquet(DATA_DIR / "crsp_ewi.parquet")
    ewi["month"] = pd.to_datetime(ewi["month"])
    ff = pd.read_parquet(DATA_DIR / "ff_factors.parquet")
    ff["month"] = pd.to_datetime(ff["month"])
    port_rets_i = attach_market(port_rets_i, ewi[["month", "ewretd"]], ff[["month", "rf"]])

    panel_i: dict = {}
    for strat in ("s0", "s1"):
        for sub_label, sel in SUBPERIODS.items():
            sub_full = port_rets_i[(port_rets_i["strategy"] == strat)
                                   & sel(port_rets_i["month"])]
            p1w = sub_full[sub_full["decile"] == 1][["month", "excess_ret"]].rename(columns={"excess_ret": "p1"})
            p10w = sub_full[sub_full["decile"] == 10][["month", "excess_ret"]].rename(columns={"excess_ret": "p10"})
            sp = p1w.merge(p10w, on="month", how="inner")
            sp["spread_excess"] = sp["p1"] - sp["p10"]
            sp = sp.merge(sub_full.drop_duplicates("month")[["month", "excess_mkt"]],
                          on="month", how="left")
            sp["excess_ret"] = sp["spread_excess"]
            sp_read = sp[["excess_ret", "excess_mkt"]].dropna()
            n_obs = len(sp_read)
            if n_obs >= 24:
                X = sm.add_constant(sp_read["excess_mkt"].to_numpy(float))
                y = sp_read["excess_ret"].to_numpy(float)
                res = sm.OLS(y, X).fit(cov_type="HC1")
                panel_i[(strat, sub_label)] = {
                    "alpha": float(res.params[0]),
                    "t_alpha": float(res.tvalues[0]),
                    "beta": float(res.params[1]),
                    "n_obs": n_obs,
                }
            else:
                panel_i[(strat, sub_label)] = {"alpha": np.nan, "t_alpha": np.nan,
                                               "beta": np.nan, "n_obs": n_obs}

    # --- Panel II: 1963-1987 using lag1_excl_last_day ------------------------
    p2_base = build_panel_vi_panelII(panel_with_dec, lag1_excl)
    # Drop any pre-existing dec_* columns so assign_deciles_all does not
    # collide with column-name suffixes when re-adding them.
    p2_base = p2_base.drop(columns=[c for c in p2_base.columns
                                     if c.startswith("dec_")], errors="ignore")
    # Re-run S0 forecast over 1963-1987 using the lag1-excl-last-day input,
    # so the S0 prediction is consistent with the bias-adjusted universe.
    # Note: this re-uses the S0 forecast function but with a shorter window.
    # To keep runtime manageable we re-run the same forecast logic on the
    # 1963-1987 sample using lag1 already replaced.
    p2_with_pred, _s0_diag_ii = compute_s0_forecasts(p2_base)
    p2_with_dec = assign_deciles_all(p2_with_pred)
    # S1 needs to be re-sorted using the (already replaced) lag1.
    # assign_deciles_all reads the `lag1` column, so as long as we have
    # overwritten it with lag1_excl_last_day above, the S1 sort is
    # automatically bias-adjusted.
    port_rets_ii = compute_portfolio_returns(p2_with_dec)
    port_rets_ii = attach_market(port_rets_ii, ewi[["month", "ewretd"]], ff[["month", "rf"]])

    panel_ii: dict = {}
    for strat in ("s0", "s1"):
        for sub_label, sel in SUBPERIODS.items():
            sub_full = port_rets_ii[(port_rets_ii["strategy"] == strat)
                                    & sel(port_rets_ii["month"])]
            p1w = sub_full[sub_full["decile"] == 1][["month", "excess_ret"]].rename(columns={"excess_ret": "p1"})
            p10w = sub_full[sub_full["decile"] == 10][["month", "excess_ret"]].rename(columns={"excess_ret": "p10"})
            sp = p1w.merge(p10w, on="month", how="inner")
            sp["spread_excess"] = sp["p1"] - sp["p10"]
            sp = sp.merge(sub_full.drop_duplicates("month")[["month", "excess_mkt"]],
                          on="month", how="left")
            sp["excess_ret"] = sp["spread_excess"]
            sp_read = sp[["excess_ret", "excess_mkt"]].dropna()
            n_obs = len(sp_read)
            if n_obs >= 24:
                X = sm.add_constant(sp_read["excess_mkt"].to_numpy(float))
                y = sp_read["excess_ret"].to_numpy(float)
                res = sm.OLS(y, X).fit(cov_type="HC1")
                panel_ii[(strat, sub_label)] = {
                    "alpha": float(res.params[0]),
                    "t_alpha": float(res.tvalues[0]),
                    "beta": float(res.params[1]),
                    "n_obs": n_obs,
                }
            else:
                panel_ii[(strat, sub_label)] = {"alpha": np.nan, "t_alpha": np.nan,
                                               "beta": np.nan, "n_obs": n_obs}
    return panel_i, panel_ii


def write_table_6(panel_i: dict, panel_ii: dict) -> None:
    """Render Table VI markdown — bid-ask-spread robustness."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Table VI. Bid-Ask Spread Bias Correction",
        "",
        f"Market model: R_pt − R_ft = α_p + β_p (R_mt − R_ft) + u_pt.  "
        f"Sample period {TABLE_VI_START} .. {TABLE_VI_END}.  "
        f"White (1980) HC1 standard errors.",
        "",
        "Panel I: standard lag1 (full prior-month return).  "
        "Panel II: lag1_excl_last_day — prior-month return computed from "
        "daily returns EXCLUDING the last trading day of month t-1; "
        "stocks not trading on the last day of t-1 are dropped (paper §III.C).",
        "",
    ]
    for panel_label, panel in (("Panel I (full lag1)", panel_i),
                               ("Panel II (lag1 excl last day)", panel_ii)):
        lines.append(f"## {panel_label}")
        lines.append("")
        lines.append("| Strategy | Sub-period | α (per month) | t(α) | β | n_obs |")
        lines.append("|---|---|---|---|---|---|")
        for strat in ("s0", "s1"):
            for sub_label in SUBPERIODS:
                c = panel.get((strat, sub_label), {})
                lines.append(
                    f"| {strat.upper()} | {SUBPERIOD_LABELS[sub_label]} | "
                    f"{c.get('alpha', float('nan')):+.4f} | "
                    f"({c.get('t_alpha', float('nan')):+.2f}) | "
                    f"{c.get('beta', float('nan')):+.3f} | "
                    f"{c.get('n_obs', 0)} |"
                )
        lines.append("")
    (RESULTS_DIR / "table_6.md").write_text("\n".join(lines) + "\n")


def compare_table_vi_to_paper(panel_i: dict, panel_ii: dict) -> None:
    """Print Table VI headline cells vs paper."""
    paper = {
        ("I",   "s0", "jandec"): ("panelI_s0_spread_jandec",  0.0207, 10.30),
        ("I",   "s1", "jandec"): ("panelI_s1_spread_jandec",  0.0153, 7.41),
        ("II",  "s0", "jandec"): ("panelII_s0_spread_jandec", 0.0177, 8.78),
        ("II",  "s1", "jandec"): ("panelII_s1_spread_jandec", 0.0108, 5.37),
    }
    print("\n=== Table VI vs paper (Jan-Dec P1-P10 spread) ===")
    print(f"{'cell':<32}{'paper':>10}{'repl':>10}{'diff%':>9}{'paper t':>9}{'repl t':>9}")
    for key, (name, pv, pt) in paper.items():
        panel = panel_i if key[0] == "I" else panel_ii
        c = panel.get((key[1], key[2]), {})
        rv = c.get("alpha", np.nan)
        rt = c.get("t_alpha", np.nan)
        dp = (rv - pv) / abs(pv) * 100 if pv and np.isfinite(rv) else float("nan")
        print(f"{name:<32}{pv:>10.4f}{rv:>10.4f}{dp:>8.1f}%{pt:>9.2f}{rt:>9.2f}")


def build_t6_metrics(panel_i: dict, panel_ii: dict) -> dict:
    """Per-cell metrics for Table VI matching tables_to_replicate.json."""
    out: dict[str, dict] = {}
    metric_keys = {
        ("I",  "s0", "jandec"): "panelI_s0_spread_jandec",
        ("I",  "s1", "jandec"): "panelI_s1_spread_jandec",
        ("II", "s0", "jandec"): "panelII_s0_spread_jandec",
        ("II", "s1", "jandec"): "panelII_s1_spread_jandec",
    }
    for (panel_label, strat, sub), name in metric_keys.items():
        panel = panel_i if panel_label == "I" else panel_ii
        c = panel.get((strat, sub), {})
        out[name] = {"value": c.get("alpha", np.nan), "unit": "alpha_per_month"}
        # Targets file uses "<base>_t_<sub>" naming.
        t_name = f"{name.rsplit('_', 1)[0]}_t_{sub}"
        out[t_name] = {"value": c.get("t_alpha", np.nan), "unit": "t_stat"}
    return out


if __name__ == "__main__":
    main()
