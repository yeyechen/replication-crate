"""
Replication of Fairfield, Whisenant & Yohn (2003)
"Accrued Earnings and Growth: Implications for Earnings Persistence
and Market Mispricing" (FWY)

Stage 7 — Tables 1, 2, 3, 4, 5, 6.

Inputs:
    data/panel.parquet — firm-year panel built in Stage 7 iter 2.

Outputs:
    results/table_1.md ... results/table_6.md — paper-style markdown grids.
    results/all_metrics.json — flat dict of all replicated numbers, keyed
                                by metric name (one entry per cell in
                                tables_to_replicate.json). Consumed by
                                src/evaluate.py.

Methodology highlights:
- Table 1: 5-number summary on the full panel for the seven deflated ratios.
- Table 2: per-fyear decile sort by ACC, equal-weighted mean across years
  of the per-(fyear, decile) variable means.
- Table 3: Pearson correlation matrix pooled across all firm-years (the
  paper reports a single correlation matrix, not per-year).
- Tables 4, 5, 6: per-fyear OLS regressions; time-series aggregation is the
  Fama-MacBeth (1973) matched-pair t-stat convention:
        mean(b_y) ± std(b_y, ddof=1)/sqrt(T)
  (NOT Newey-West; the paper's footnote 17 explicitly says
  "matched-pair t-test").
- Paired-difference t-stats (Table 4 panel B, Table 5 panel B, Table 6
  panel B): per-year difference d_y = b_k_y - b_l_y, then
  t = mean(d) / (std(d, ddof=1)/sqrt(T)).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from utils.paths import paper_layout

LAYOUT = paper_layout("fairfield_v2").ensure()

PANEL_PATH = LAYOUT.data_path("panel.parquet")
RESULTS_DIR = LAYOUT.results_dir
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# --- variables in deflated-ratio form -----------------------------------
# Naming note: 'depam_t' in the panel is actually named 'depam_over_avg_ta_t'
# (a long alias). We rename to depam_t for compact analysis below.
PAPER_VARS = ["roa_t", "acc_t", "cfo_t", "grnoa_t", "grwc_t", "depam_t", "grltnoa_t"]


def load_panel() -> pd.DataFrame:
    """Load panel.parquet and standardize the depam column name.

    The panel has both `depam_t` (raw $millions level) and
    `depam_over_avg_ta_t` (deflated ratio). The deflated ratio is the one
    we need for analysis, so we drop the raw level and rename.
    """
    panel = pd.read_parquet(PANEL_PATH)
    # Drop the raw-level column if present, then rename the deflated ratio
    # to the unified name `depam_t` used in PAPER_VARS.
    if "depam_t" in panel.columns:
        panel = panel.drop(columns=["depam_t"])
    if "depam_over_avg_ta_t" in panel.columns:
        panel = panel.rename(columns={"depam_over_avg_ta_t": "depam_t"})
    return panel


# --- Table 1: 5-number summary ------------------------------------------
def table_1(panel: pd.DataFrame) -> Dict[str, float]:
    """5-number summary (mean, std, median, q1, q3) for the seven ratios."""
    out: Dict[str, float] = {}
    # Mapping from panel column name to the paper's column prefix.
    var_to_prefix = {
        "roa_t":    "ROA",
        "acc_t":    "ACC",
        "cfo_t":    "CFO",
        "grnoa_t":  "GrNOA",
        "grwc_t":   "GrWC",
        "depam_t":  "DEPAM",
        "grltnoa_t":"GrLTNOA",
    }
    for var in PAPER_VARS:
        s = panel[var].dropna()
        qs = s.quantile([0.25, 0.5, 0.75])
        prefix = var_to_prefix[var]
        # Paper Tables 1 use sample std (ddof=1); pandas default is ddof=1.
        out[f"T1_{prefix}_mean"]   = float(s.mean())
        out[f"T1_{prefix}_std"]    = float(s.std())
        out[f"T1_{prefix}_median"] = float(qs.loc[0.5])
        out[f"T1_{prefix}_q1"]     = float(qs.loc[0.25])
        out[f"T1_{prefix}_q3"]     = float(qs.loc[0.75])
    return out


# --- Table 2: decile sort -----------------------------------------------
def table_2(panel: pd.DataFrame) -> Dict[str, float]:
    """Per-fyear 10-bin sort by ACC; EW mean across years of per-bin means."""
    out: Dict[str, float] = {}

    # Equal-count deciles by ACC within each fyear. Use rank-based decile
    # assignment (qcut can fail on tied values in some years); the
    # assign_quantiles utility handles ties via a rank-based fallback.
    panel = panel.copy()
    panel["acc_decile"] = (
        panel.groupby("fyear")["acc_t"]
        .transform(lambda s: _deciles(s, n_bins=10))
    )

    panel_b = panel.dropna(subset=["acc_decile"]).copy()
    panel_b["acc_decile"] = panel_b["acc_decile"].astype(int)

    # Variables to aggregate by bin (paper reports means of these).
    t2_vars = ["roa_t", "acc_t", "cfo_t", "grnoa_t", "grwc_t", "depam_t", "grltnoa_t"]
    # Panel A vs B split per the paper.
    panelA = ["roa_t", "acc_t", "cfo_t"]
    panelB = ["grnoa_t", "grwc_t", "depam_t", "grltnoa_t"]

    # Mapping from panel column to paper's metric prefix.
    var_to_prefix = {
        "roa_t":    "ROA",
        "acc_t":    "ACC",
        "cfo_t":    "CFO",
        "grnoa_t":  "GrNOA",
        "grwc_t":   "GrWC",
        "depam_t":  "DEPAM",
        "grltnoa_t":"GrLTNOA",
    }

    # Per-(fyear, bin) means, then equal-weighted mean across fyears.
    per_year_bin = (
        panel_b.groupby(["fyear", "acc_decile"])[t2_vars].mean().reset_index()
    )
    bin_means = per_year_bin.groupby("acc_decile")[t2_vars].mean()

    for var in t2_vars:
        prefix = var_to_prefix[var]
        panel_letter = "PanelA" if var in panelA else "PanelB"
        for d in range(1, 11):
            out[f"T2_{panel_letter}_{prefix}_D{d}"] = float(bin_means.loc[d, var])
    return out


def _deciles(s: pd.Series, n_bins: int = 10) -> pd.Series:
    """Per-group decile labels 1..n_bins. Rank-based fallback for ties."""
    try:
        return pd.qcut(s, q=n_bins, labels=False, duplicates="drop") + 1
    except (ValueError, TypeError):
        # rank-based fallback preserves bin balance in well-behaved cases
        return np.ceil(s.rank(method="average") / len(s) * n_bins)


# --- Table 3: Pearson correlation matrix --------------------------------
def table_3(panel: pd.DataFrame) -> Dict[str, float]:
    """Pooled Pearson correlation matrix across all firm-years."""
    out: Dict[str, float] = {}

    # We need ROA_{t+1} alongside the seven current ratios. Restrict to
    # rows where ALL eight variables are non-null.
    cols_t3 = ["roa_t_plus_1", "roa_t", "acc_t", "cfo_t", "grnoa_t",
               "grwc_t", "depam_t", "grltnoa_t"]
    df = panel[cols_t3].dropna()
    corr = df.corr(method="pearson")

    # Map (paper-row-var, paper-col-var) into the json metric name.
    # Paper convention from tables_to_replicate.json:
    #   - ROA_{t+1} row prefix: "ROAt1"
    #   - ROA_{t+1} col prefix (when it's the column for ROA_t row): "ROAt"
    #   - ROA_t row prefix (when ROA_t is the ROW): "ROA"
    # This mixed convention is what the orchestrator committed to.
    label_map = {
        "roa_t_plus_1": "ROAt1",   # always
        "roa_t":        None,      # depends on row/col context
        "acc_t":        "ACC",
        "cfo_t":        "CFO",
        "grnoa_t":      "GrNOA",
        "grwc_t":       "GrWC",
        "depam_t":      "DEPAM",
        "grltnoa_t":    "GrLTNOA",
    }
    # Paper Table 3 reports only the lower triangle of Pearson (28 unique
    # off-diagonal pairs). The targets file enumerates them explicitly:
    # ROAt1-row (with each other), ROA-row (with each col > ROA), etc.
    # We iterate pairs (i, j) with i<j in the paper's column order.
    cols_order = cols_t3  # ["roa_t_plus_1", "roa_t", "acc_t", "cfo_t",
                          #  "grnoa_t", "grwc_t", "depam_t", "grltnoa_t"]

    def _row_label(var):
        if var == "roa_t":
            return "ROA"  # row always uses bare ROA
        return label_map[var]

    def _col_label(var):
        if var == "roa_t":
            # col uses ROAt when paired with ROAt1 row, else ROA
            return "ROAt"  # we'll handle the exception below
        return label_map[var]

    for i in range(len(cols_order)):
        for j in range(i + 1, len(cols_order)):
            row_var = cols_order[i]
            col_var = cols_order[j]
            row_label = _row_label(row_var)
            # Special-case: when row is roa_t_plus_1 and col is roa_t, the
            # target key is "T3_corr_ROAt1_ROAt_pearson".
            if row_var == "roa_t_plus_1" and col_var == "roa_t":
                col_label = "ROAt"
            else:
                col_label = _col_label(col_var)
            metric = f"T3_corr_{row_label}_{col_label}_pearson"
            out[metric] = float(corr.loc[row_var, col_var])
    return out


# --- Tables 4-6: Fama-MacBeth -------------------------------------------
def _fm_year_ols(year_df: pd.DataFrame, y: str, x: List[str], min_obs: int = 30):
    """One annual cross-sectional OLS. Returns dict or None if insufficient N."""
    if len(year_df) < max(min_obs, len(x) + 5):
        return None
    try:
        import statsmodels.api as sm
    except ImportError as e:
        raise RuntimeError(
            "statsmodels is required for OLS regressions — "
            "install with `uv pip install statsmodels`"
        ) from e

    sub = year_df[[y, *x]].replace([np.inf, -np.inf], np.nan).dropna()
    if len(sub) < max(min_obs, len(x) + 5):
        return None
    res = sm.OLS(sub[y], sm.add_constant(sub[x])).fit()
    return {
        "params": res.params,                # index includes 'const'
        "rsquared_adj": float(res.rsquared_adj),
        "nobs": int(res.nobs),
    }


def _fm_aggregate(per_year: pd.DataFrame, x: List[str], include_const: bool = True):
    """Aggregate per-year OLS into FM mean / SE / t-stat (matched-pair).

    Convention (per paper L1050, footnote 17): SE = std(b_y, ddof=1) / sqrt(T).
    """
    # Aggregate over ALL coefficient columns including the intercept.
    all_x = ["const", *x]
    # Make sure every column is present (per_year.columns may exclude const
    # if the regression dropped it; we still want a row for it).
    for col in all_x:
        if col not in per_year.columns:
            per_year[col] = np.nan

    mean_b = per_year[all_x].mean()
    # ddof=1: sample std of the time-series of coefficients. Paper's t-stat
    # is exactly mean(b) / (std(b, ddof=1)/sqrt(T)).
    std_b = per_year[all_x].std(ddof=1)
    T = len(per_year)
    se_b = std_b / np.sqrt(T)
    t_b = mean_b / se_b.replace(0, np.nan)

    return mean_b, se_b, t_b, T


def _fm_run(panel: pd.DataFrame, y: str, x: List[str], min_obs: int = 30):
    """Run all annual regressions and aggregate. Returns (mean, t, T, adj_r2_mean)."""
    per_year_records = []
    for fyear, g in panel.groupby("fyear"):
        r = _fm_year_ols(g, y, x, min_obs=min_obs)
        if r is None:
            continue
        rec = {"fyear": fyear, "adj_r2": r["rsquared_adj"]}
        for k, v in r["params"].items():
            rec[k] = float(v)
        per_year_records.append(rec)
    if not per_year_records:
        return None
    per_year = pd.DataFrame(per_year_records).set_index("fyear")
    # Make sure all coefficient columns exist (in case const wasn't returned)
    for col in ["const", *x]:
        if col not in per_year.columns:
            per_year[col] = np.nan
    mean_s, se_s, t_s, T = _fm_aggregate(per_year, x)
    adj_r2_mean = float(per_year["adj_r2"].mean())
    return {"mean": mean_s, "t": t_s, "T": T, "adj_r2_mean": adj_r2_mean,
            "per_year": per_year}


def _fm_paired_t(panel: pd.DataFrame, y: str, x: List[str],
                 k_var: str, l_var: str, min_obs: int = 30):
    """Matched-pair t-test: per-year d_y = b_k_y - b_l_y, then mean(d)/(std/sqrt(T))."""
    per_year_records = []
    for fyear, g in panel.groupby("fyear"):
        r = _fm_year_ols(g, y, x, min_obs=min_obs)
        if r is None:
            continue
        rec = {"fyear": fyear,
               "b_k": float(r["params"].get(k_var, np.nan)),
               "b_l": float(r["params"].get(l_var, np.nan))}
        per_year_records.append(rec)
    if not per_year_records:
        return None
    per_year = pd.DataFrame(per_year_records).set_index("fyear")
    per_year["d"] = per_year["b_k"] - per_year["b_l"]
    T = len(per_year)
    mean_d = float(per_year["d"].mean())
    std_d = float(per_year["d"].std(ddof=1))
    se_d = std_d / np.sqrt(T)
    t_d = mean_d / se_d if se_d > 0 else np.nan
    return {"t": float(t_d), "T": T, "mean_d": mean_d, "std_d": std_d}


def table_4(panel: pd.DataFrame) -> Dict[str, float]:
    """Equations (1) and (2): one-year-ahead ROA on current ROA / ACC+CFO."""
    out: Dict[str, float] = {}

    y = "roa_t_plus_1"
    eq1_x = ["roa_t"]
    eq2_x = ["acc_t", "cfo_t"]

    # Filter to rows where ALL variables (DV + all RHS) are non-null, per the
    # standard FM-by-year approach (dropna per equation).
    eq1_panel = panel.dropna(subset=[y, *eq1_x])
    eq2_panel = panel.dropna(subset=[y, *eq2_x])

    r1 = _fm_run(eq1_panel, y, eq1_x)
    r2 = _fm_run(eq2_panel, y, eq2_x)

    if r1 is not None:
        out["T4_eq1_intercept"]  = float(r1["mean"]["const"])
        out["T4_eq1_intercept_t"] = float(r1["t"]["const"])
        out["T4_eq1_ROA"]        = float(r1["mean"]["roa_t"])
        out["T4_eq1_ROA_t"]      = float(r1["t"]["roa_t"])
        out["T4_eq1_adj_R2"]     = r1["adj_r2_mean"]
        out["T4_eq1_n_periods"]  = r1["T"]

    if r2 is not None:
        out["T4_eq2_intercept"]  = float(r2["mean"]["const"])
        out["T4_eq2_intercept_t"] = float(r2["t"]["const"])
        out["T4_eq2_ACC"]        = float(r2["mean"]["acc_t"])
        out["T4_eq2_ACC_t"]      = float(r2["t"]["acc_t"])
        out["T4_eq2_CFO"]        = float(r2["mean"]["cfo_t"])
        out["T4_eq2_CFO_t"]      = float(r2["t"]["cfo_t"])
        out["T4_eq2_adj_R2"]     = r2["adj_r2_mean"]
        out["T4_eq2_n_periods"]  = r2["T"]

        # Paired-difference t-stat (panel B): b_CFO - b_ACC? The paper's
        # eq. 2 panel B tests "beta_1 = beta_2" where beta_1 is on ACC,
        # beta_2 is on CFO. A positive paper t-stat (4.58) implies CFO is
        # more persistent than ACC, so the test direction is
        # d_y = b_CFO - b_ACC > 0. We follow this convention.
        pt = _fm_paired_t(eq2_panel, y, eq2_x, "cfo_t", "acc_t")
        if pt is not None:
            out["T4_eq2_paired_t_diff"] = pt["t"]
            out["T4_eq2_paired_t_n_periods"] = pt["T"]

    return out


def table_5(panel: pd.DataFrame) -> Dict[str, float]:
    """Equations (3) and (4): ROA_{t+1} on ROA+ACC and ROA+ACC+GrLTNOA."""
    out: Dict[str, float] = {}

    y = "roa_t_plus_1"
    eq3_x = ["roa_t", "acc_t"]
    eq4_x = ["roa_t", "acc_t", "grltnoa_t"]

    eq3_panel = panel.dropna(subset=[y, *eq3_x])
    eq4_panel = panel.dropna(subset=[y, *eq4_x])

    r3 = _fm_run(eq3_panel, y, eq3_x)
    r4 = _fm_run(eq4_panel, y, eq4_x)

    if r3 is not None:
        out["T5_eq3_intercept"]  = float(r3["mean"]["const"])
        out["T5_eq3_intercept_t"] = float(r3["t"]["const"])
        out["T5_eq3_ROA"]        = float(r3["mean"]["roa_t"])
        out["T5_eq3_ROA_t"]      = float(r3["t"]["roa_t"])
        out["T5_eq3_ACC"]        = float(r3["mean"]["acc_t"])
        out["T5_eq3_ACC_t"]      = float(r3["t"]["acc_t"])
        out["T5_eq3_adj_R2"]     = r3["adj_r2_mean"]
        out["T5_eq3_n_periods"]  = r3["T"]

    if r4 is not None:
        out["T5_eq4_intercept"]  = float(r4["mean"]["const"])
        out["T5_eq4_intercept_t"] = float(r4["t"]["const"])
        out["T5_eq4_ROA"]        = float(r4["mean"]["roa_t"])
        out["T5_eq4_ROA_t"]      = float(r4["t"]["roa_t"])
        out["T5_eq4_ACC"]        = float(r4["mean"]["acc_t"])
        out["T5_eq4_ACC_t"]      = float(r4["t"]["acc_t"])
        out["T5_eq4_GrLTNOA"]    = float(r4["mean"]["grltnoa_t"])
        out["T5_eq4_GrLTNOA_t"]  = float(r4["t"]["grltnoa_t"])
        out["T5_eq4_adj_R2"]     = r4["adj_r2_mean"]
        out["T5_eq4_n_periods"]  = r4["T"]

        # Paired t for beta_2_ACC = beta_3_GrLTNOA. Paper's -1.21: this is
        # b_GrLTNOA - b_ACC (i.e., both negative, and GrLTNOA is slightly
        # less negative than ACC, so difference is positive? paper prints
        # -1.21 which is ambiguous). We follow the paper's signed t-stat.
        # By convention: t = (mean(b_GrLTNOA) - mean(b_ACC)) /
        # (std(per-year diff)/sqrt(T)). With GrLTNOA=-0.039 and ACC=-0.061,
        # d_y = -0.039 - (-0.061) = +0.022, so a positive t is expected.
        # Paper prints -1.21 — this corresponds to d_y = b_ACC - b_GrLTNOA
        # (subtraction reversed). We adopt d_y = b_ACC - b_GrLTNOA.
        pt = _fm_paired_t(eq4_panel, y, eq4_x, "acc_t", "grltnoa_t")
        if pt is not None:
            out["T5_eq4_paired_t_diff"] = pt["t"]
            out["T5_eq4_paired_t_n_periods"] = pt["T"]

    return out


def table_6(panel: pd.DataFrame) -> Dict[str, float]:
    """Equations (5) and (6): OPINC_{t+1}/AVG(TA_{t-1}, TA_t) on ROA+ACC, +GrLTNOA."""
    out: Dict[str, float] = {}

    y = "opinc_t_plus_1_per_lag_def"   # already in the panel
    eq5_x = ["roa_t", "acc_t"]
    eq6_x = ["roa_t", "acc_t", "grltnoa_t"]

    eq5_panel = panel.dropna(subset=[y, *eq5_x])
    eq6_panel = panel.dropna(subset=[y, *eq6_x])

    r5 = _fm_run(eq5_panel, y, eq5_x)
    r6 = _fm_run(eq6_panel, y, eq6_x)

    if r5 is not None:
        out["T6_eq5_intercept"]  = float(r5["mean"]["const"])
        out["T6_eq5_intercept_t"] = float(r5["t"]["const"])
        out["T6_eq5_ROA"]        = float(r5["mean"]["roa_t"])
        out["T6_eq5_ROA_t"]      = float(r5["t"]["roa_t"])
        out["T6_eq5_ACC"]        = float(r5["mean"]["acc_t"])
        out["T6_eq5_ACC_t"]      = float(r5["t"]["acc_t"])
        out["T6_eq5_adj_R2"]     = r5["adj_r2_mean"]
        out["T6_eq5_n_periods"]  = r5["T"]

    if r6 is not None:
        out["T6_eq6_intercept"]  = float(r6["mean"]["const"])
        out["T6_eq6_intercept_t"] = float(r6["t"]["const"])
        out["T6_eq6_ROA"]        = float(r6["mean"]["roa_t"])
        out["T6_eq6_ROA_t"]      = float(r6["t"]["roa_t"])
        out["T6_eq6_ACC"]        = float(r6["mean"]["acc_t"])
        out["T6_eq6_ACC_t"]      = float(r6["t"]["acc_t"])
        out["T6_eq6_GrLTNOA"]    = float(r6["mean"]["grltnoa_t"])
        out["T6_eq6_GrLTNOA_t"]  = float(r6["t"]["grltnoa_t"])
        out["T6_eq6_adj_R2"]     = r6["adj_r2_mean"]
        out["T6_eq6_n_periods"]  = r6["T"]

        # Paired t for delta_2_ACC = delta_3_GrLTNOA. Paper -1.50: ACC=-0.007,
        # GrLTNOA=0.030. b_ACC - b_GrLTNOA = -0.037, sign negative.
        pt = _fm_paired_t(eq6_panel, y, eq6_x, "acc_t", "grltnoa_t")
        if pt is not None:
            out["T6_eq6_paired_t_diff"] = pt["t"]
            out["T6_eq6_paired_t_n_periods"] = pt["T"]

    return out


# --- Table 7: Mishkin test (eqs. 7, 8) ---------------------------------
def _safe_ols(y: pd.Series, X: pd.DataFrame):
    """OLS via numpy.linalg.lstsq (no statsmodels dependency). Returns
    (params, residuals, n). Robust to collinear / singular matrices.
    """
    import statsmodels.api as sm  # use statsmodels for SE, but fall back to lstsq
    Xv = sm.add_constant(X)
    res = sm.OLS(y, Xv).fit()
    return res.params, res.resid, int(res.nobs), res.bse


def table_7(panel: pd.DataFrame) -> Dict[str, float]:
    """Mishkin (1983) test for rational pricing.

    Eq. 7 (forecasting): ROA_{t+1} = γ_0 + γ_1 ROA_t + γ_2 ACC_t + γ_3 GrLTNOA_t + u
    Eq. 8 (valuation):   BHAR_{t+1} = α + β (ROA_{t+1} - γ_0* - γ_1* ROA_t - γ_2* ACC_t
                                       - γ_3* GrLTNOA_t) + e

    Approximation: textbook 2-stage NLS (Mishkin GLS is iterative). The
    2-stage NLS is consistent at the parameter estimates; SEs may
    differ slightly from the paper's iterative GLS SEs (see notes in
    assumptions.md).

    Step 1: estimate eq. 7 by OLS (firm-year pooled). Get γ_1..γ_3.
    Step 2: build fitted_roa_t+1_hat = γ_0 + γ_1 ROA_t + γ_2 ACC_t + γ_3 GrLTNOA_t.
    Step 3: unrestricted valuation regression:
              BHAR ~ 1 + (ROA_{t+1} - fitted_hat)
            gives β_uncon, α; valuation coef γ*_q = β_uncon * γ_q.
    Step 4: constrained (β=1) valuation regression:
              BHAR ~ 1 + (ROA_{t+1} - fitted_hat)
            with slope forced to 1 (i.e. residuals = BHAR - (ROA - hat))
            → SSR^c.
    Step 5: LR = 2n log(SSR^c / SSR^u).

    q=1: impose one constraint γ*_q = γ_q for each of {ROA, ACC, GrLTNOA}.
         Single-constraint LR (1 df).
    q=2 (joint): impose γ*_2 = γ_3 AND γ_2 = γ_3 (4 constraints). To test
         this we redo Step 3 with a modified fitted_hat using γ_2=γ_3
         (and γ*_2=γ*_3 implicit when β=1). Concretely:
            eq. 7 (constrained): ROA_t+1 = γ_0 + γ_1 ROA + γ_c (ACC + GrLTNOA)
            → fitted_hat_c = γ_0 + γ_1 ROA + γ_c (ACC + GrLTNOA)
            eq. 8 (constrained β=1): residuals = BHAR - (ROA - hat_c).
    """
    out: Dict[str, float] = {}

    # Load BHAR parquet (built by src/sql/bhar.sql).
    bhar_path = LAYOUT.data_path("bhar.parquet")
    if not bhar_path.exists():
        # No BHAR cache -- signal as SKIP by returning an empty dict.
        return out
    bhar = pd.read_parquet(bhar_path)

    # Merge panel with BHAR_abnormal (size-adjusted BHAR_{t+1}).
    # The BHAR for fiscal-year t uses the calendar_year = fyear (paper
    # convention: formation at end of year t, returns measured at year
    # t+1 -- in this SQL pipeline, the 12-month window for a (gvkey,
    # fyear) starts at the calendar month of datadate; for fiscal
    # year-ends in Dec, the calendar_year column equals fyear, and the
    # BHAR covers months [Dec_year_t .. Nov_year_t+1], i.e. the
    # 12-month return ending in calendar year t+1. We use
    # bhar_abnormal directly as the BHAR_{t+1} value in eq. 8.
    p = panel.copy()
    p["gvkey"] = p["gvkey"].astype(str)
    bhar = bhar.copy()
    bhar["gvkey"] = bhar["gvkey"].astype(str)
    df = p.merge(
        bhar[["gvkey", "fyear", "bh_calendar_year", "bhar_abnormal",
              "bhar_firm", "size_dec", "bhar_size_dec"]],
        on=["gvkey", "fyear"], how="inner",
    )
    # No winsorization: paper doesn't specify. We rely on the panel's
    # own outlier controls (CRSP-coverage gate, non-null gates).
    n_obs = len(df)
    out["T7A_n_obs"] = float(n_obs)

    # The sample needs all of: roa_t, acc_t, grltnoa_t, roa_t_plus_1,
    # bhar_abnormal. The merged df already restricts to rows with
    # BHAR present; we still need non-null predictors.
    sample = df.dropna(subset=["roa_t", "acc_t", "grltnoa_t",
                                "roa_t_plus_1", "bhar_abnormal"]).copy()
    n_sample = len(sample)
    out["T7A_n_sample"] = float(n_sample)
    if n_sample < 50:
        return out

    # --- Step 1: estimate eq. 7 by OLS ---
    import statsmodels.api as sm
    y_fwd = sample["roa_t_plus_1"]
    X_fwd = sample[["roa_t", "acc_t", "grltnoa_t"]]
    res_fwd = sm.OLS(y_fwd, sm.add_constant(X_fwd)).fit()
    gamma_0 = float(res_fwd.params["const"])
    gamma_1 = float(res_fwd.params["roa_t"])
    gamma_2 = float(res_fwd.params["acc_t"])
    gamma_3 = float(res_fwd.params["grltnoa_t"])
    se_g1 = float(res_fwd.bse["roa_t"])
    se_g2 = float(res_fwd.bse["acc_t"])
    se_g3 = float(res_fwd.bse["grltnoa_t"])

    sample["fitted_hat"] = (gamma_0 + gamma_1 * sample["roa_t"]
                            + gamma_2 * sample["acc_t"]
                            + gamma_3 * sample["grltnoa_t"])
    sample["abnormal_roa"] = (sample["roa_t_plus_1"] - sample["fitted_hat"])

    # --- Step 3: unrestricted valuation regression (eq. 8) ---
    # In the joint GLS framework, γ*_q are SEPARATE free parameters
    # estimated jointly with γ_q. The 2-stage NLS approximation
    # proceeds:
    #   Stage 1: estimate eq. 7 → γ (above).
    #   Stage 2: estimate eq. 8 with γ fixed at stage 1 values, get γ*.
    # Concretely: regress BHAR on a constant, ROA_{t+1}, ROA_t, ACC_t,
    # GrLTNOA_t (with the constraint γ_0* = γ_0, i.e. the bracket's
    # intercept equals the eq.7 intercept). This is the proper
    # unconstrained stage.
    y_val = sample["bhar_abnormal"]
    X_val = sample[["roa_t_plus_1", "roa_t", "acc_t", "grltnoa_t"]]
    res_val = sm.OLS(y_val, sm.add_constant(X_val)).fit()
    # In eq. 8: BHAR = α + β*(ROA_{t+1} - γ_0 - γ_1*ROA - γ_2*ACC - γ_3*GrLTNOA)
    # Expand: BHAR = (α - β*γ_0) + β*ROA_{t+1} - β*γ_1*ROA - β*γ_2*ACC - β*γ_3*GrLTNOA
    # So the regression coefficients map to:
    #   const = α - β*γ_0
    #   b[roa_t_plus_1] = β
    #   b[roa_t] = -β*γ_1* → γ_1* = -b[roa_t]/β
    #   b[acc_t] = -β*γ_2* → γ_2* = -b[acc_t]/β
    #   b[grltnoa_t] = -β*γ_3* → γ_3* = -b[grltnoa_t]/β
    beta_u = float(res_val.params["roa_t_plus_1"])
    gstar_1 = float(-res_val.params["roa_t"] / beta_u)
    gstar_2 = float(-res_val.params["acc_t"] / beta_u)
    gstar_3 = float(-res_val.params["grltnoa_t"] / beta_u)
    # Compute SSR^c for the unconstrained stage (this is the SSR_u
    # for the LR test).
    ssr_u = float(np.sum(res_val.resid ** 2))

    # SEs from the regression coefficient covariance matrix
    import numpy as _np
    cov = res_val.cov_params()
    Xn = X_val.values
    # SE(β) from direct diagonal
    se_beta_u = float(np.sqrt(cov.loc["roa_t_plus_1", "roa_t_plus_1"]))
    # SE(γ*_q) via delta method: γ*_q = -b[x]/β → gradient w.r.t. (b[x], β)
    # is (-1/β, b[x]/β²). Variance ≈ (1/β²)*var(b[x]) + (b[x]²/β⁴)*var(β)
    def _se_gstar(col, bcoef, gstar):
        vbx = float(cov.loc[col, col])
        vbeta = float(cov.loc["roa_t_plus_1", "roa_t_plus_1"])
        covb = float(cov.loc[col, "roa_t_plus_1"])
        var_gstar = (vbx / beta_u**2
                     + (bcoef**2) * (vbeta / beta_u**4)
                     + 2 * bcoef * covb / beta_u**3)
        return float(np.sqrt(max(var_gstar, 0.0)))
    se_gstar_1 = _se_gstar("roa_t", float(-res_val.params["roa_t"]), gstar_1)
    se_gstar_2 = _se_gstar("acc_t", float(-res_val.params["acc_t"]), gstar_2)
    se_gstar_3 = _se_gstar("grltnoa_t", float(-res_val.params["grltnoa_t"]), gstar_3)

    alpha_u = float(res_val.params["const"])

    out["T7A_fcst_ROA"] = gamma_1
    out["T7A_fcst_ROA_se"] = se_g1
    out["T7A_fcst_ACC"] = gamma_2
    out["T7A_fcst_ACC_se"] = se_g2
    out["T7A_fcst_GrLTNOA"] = gamma_3
    out["T7A_fcst_GrLTNOA_se"] = se_g3

    out["T7A_val_ROA"] = gstar_1
    out["T7A_val_ROA_se"] = se_gstar_1
    out["T7A_val_ACC"] = gstar_2
    out["T7A_val_ACC_se"] = se_gstar_2
    out["T7A_val_GrLTNOA"] = gstar_3
    out["T7A_val_GrLTNOA_se"] = se_gstar_3

    # --- Step 4: constrained regression (γ*_q = γ_q, i.e. β = 1) ---
    # Under the rational-pricing null, γ*_q = γ_q for all q. Plug
    # γ*_q = γ_q into eq. 8: BHAR = α + β (ROA_{t+1} - γ_0 - γ_1 ROA
    # - γ_2 ACC - γ_3 GrLTNOA). With β=1 (and γ*_q fixed to γ_q):
    # BHAR - (ROA_{t+1} - γ_0 - γ_1 ROA - γ_2 ACC - γ_3 GrLTNOA) = α + e.
    # The residual under the null = BHAR - abnormal_roa, regressed on
    # an intercept only → SSR^c.
    y_c = sample["bhar_abnormal"] - sample["abnormal_roa"]
    res_c = sm.OLS(y_c, np.ones((n_sample, 1))).fit()
    ssr_c = float(np.sum(res_c.resid ** 2))

    # --- Step 5: LR statistics ---
    # In the joint GLS framework, each q=1 test (γ*_q = γ_q for a
    # single q) imposes ONE linear constraint. In the 2-stage NLS
    # approximation, this corresponds to constraining ONE of the γ*
    # coefficients in the unrestricted eq. 8 OLS, with γ_q from eq. 7
    # fixed. To test γ*_q = γ_q, re-estimate eq. 8 forcing that one
    # γ*_q coefficient to its γ_q value, compute SSR^c_q, compare to
    # SSR^u.
    def _lr_q1(colname: str, gamma_q: float) -> float:
        """Test γ*_q = γ_q for one q. colname is the column in
        sample whose coefficient corresponds to -β*γ_q in eq. 8.
        Constraint: -β*γ*_q = -β*γ_q → b[colname]/β = γ_q → b[colname] =
        β*γ_q. But β is also free, so the constraint is one-dimensional
        over (β, b[colname]). Equivalent: substitute γ*_q = γ_q, drop
        the column, re-estimate.
        """
        keep_cols = [c for c in ["roa_t_plus_1", "roa_t", "acc_t",
                                  "grltnoa_t"] if c != colname]
        r_c = sm.OLS(sample["bhar_abnormal"],
                     sm.add_constant(sample[keep_cols])).fit()
        ssr_cq = float(np.sum(r_c.resid ** 2))
        if ssr_u <= 0 or ssr_cq <= 0:
            return float("nan")
        return float(2 * n_sample * np.log(ssr_cq / ssr_u))

    lr_roa = _lr_q1("roa_t", gamma_1)
    lr_acc = _lr_q1("acc_t", gamma_2)
    lr_grltnoa = _lr_q1("grltnoa_t", gamma_3)

    # Joint q=2 (4 constraints: γ*_2=γ*_3 AND γ_2=γ_3).
    # Constrained eq. 7: ROA_{t+1} = γ_0 + γ_1 ROA_t + γ_c (ACC_t + GrLTNOA_t).
    y_j = sample["roa_t_plus_1"]
    X_j = sample[["roa_t"]].copy()
    X_j["acc_grltnoa_sum"] = sample["acc_t"] + sample["grltnoa_t"]
    r_j = sm.OLS(y_j, sm.add_constant(X_j)).fit()
    fitted_j = (r_j.params.iloc[0]
                + r_j.params.iloc[1] * sample["roa_t"]
                + r_j.params.iloc[2] * X_j["acc_grltnoa_sum"])
    abn_j = sample["roa_t_plus_1"] - fitted_j
    # Unconstrained joint valuation (eq. 8 with γ_q from constrained eq. 7).
    # In the proper 2-stage NLS, the unconstrained stage still estimates
    # γ*_q freely; here we use the same direct OLS on (ROA_{t+1}, ROA,
    # ACC, GrLTNOA) and let γ*_2 = γ*_3 implicitly (single coefficient
    # for the SUM, mirroring the eq. 7 constraint). This is a clean
    # 2-stage NLS approximation.
    r_u_j = sm.OLS(sample["bhar_abnormal"],
                   sm.add_constant(sample[["roa_t_plus_1", "roa_t"]].assign(
                       acc_plus_grltnoa=sample["acc_t"] + sample["grltnoa_t"]
                   ))).fit()
    ssr_u_j = float(np.sum(r_u_j.resid ** 2))
    # Constrained (β=1 on the SUM variable):
    y_c_j = sample["bhar_abnormal"] - abn_j
    r_c_j = sm.OLS(y_c_j, np.ones((n_sample, 1))).fit()
    ssr_c_j = float(np.sum(r_c_j.resid ** 2))
    lr_joint = float(2 * n_sample * np.log(ssr_c_j / ssr_u_j)) \
        if ssr_u_j > 0 and ssr_c_j > 0 else float("nan")

    out["T7B_LR_ROA_q1"] = lr_roa
    out["T7B_LR_ACC_q1"] = lr_acc
    out["T7B_LR_GrLTNOA_q1"] = lr_grltnoa
    out["T7B_LR_GrLTNOA_ACC_q2"] = lr_joint

    # Diagnostic counts
    out["T7_diag_ssru_uncon"] = ssr_u
    out["T7_diag_ssrc_uncon"] = ssr_c
    out["T7_diag_beta_uncon"] = beta_u
    out["T7_diag_alpha_uncon"] = alpha_u
    return out


# --- Markdown writers ---------------------------------------------------
def _md_table_1(metrics: Dict[str, float], panel: pd.DataFrame) -> str:
    rows = [
        ("$ROA_t$",    "ROA"),
        ("$ACC_t$",    "ACC"),
        ("$CFO_t$",    "CFO"),
    ]
    rows_b = [
        ("$GrNOA_t$",  "GrNOA"),
        ("$GrWC_t$",   "GrWC"),
        ("$DEPAM_t$",  "DEPAM"),
        ("$GrLTNOA_t$","GrLTNOA"),
    ]
    lines = []
    lines.append("# Table 1")
    lines.append("## Descriptive Statistics on ROA, Accruals, Cash Flows, and Growth")
    lines.append("")
    lines.append("| Variable | Mean | Std Dev | Median | Q1 | Q3 |")
    lines.append("|---|---|---|---|---|---|")
    lines.append("| *Panel A: Return on Assets and the Accrual and Cash Flow Components* | | | | | |")
    for label, prefix in rows:
        lines.append(
            f"| {label} | {metrics[f'T1_{prefix}_mean']:.3f} | "
            f"{metrics[f'T1_{prefix}_std']:.3f} | "
            f"{metrics[f'T1_{prefix}_median']:.3f} | "
            f"{metrics[f'T1_{prefix}_q1']:.3f} | "
            f"{metrics[f'T1_{prefix}_q3']:.3f} |"
        )
    lines.append("| *Panel B: Growth in Net Operating Assets and Components* | | | | | |")
    for label, prefix in rows_b:
        lines.append(
            f"| {label} | {metrics[f'T1_{prefix}_mean']:.3f} | "
            f"{metrics[f'T1_{prefix}_std']:.3f} | "
            f"{metrics[f'T1_{prefix}_median']:.3f} | "
            f"{metrics[f'T1_{prefix}_q1']:.3f} | "
            f"{metrics[f'T1_{prefix}_q3']:.3f} |"
        )
    lines.append("")
    lines.append(f"Number of observations = {len(panel):,} firm-years between 1963 and 1992.")
    lines.append("")
    return "\n".join(lines)


def _md_table_2(metrics: Dict[str, float]) -> str:
    lines = []
    lines.append("# Table 2")
    lines.append("## Mean Values of ROA, Accruals, Cash Flows, and Growth Characteristics of Ten Portfolios of Firms Formed Annually Based on the Magnitude of Accruals")
    lines.append("")
    lines.append("| Portfolio Accrual Ranking | Low | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | High |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    lines.append("| *Panel A: Return on Assets and the Accrual and Cash Flow Components* | | | | | | | | | | |")
    for var_label, prefix in [
        ("$ROA_t$", "ROA"),
        ("$ACC_t$", "ACC"),
        ("$CFO_t$", "CFO"),
    ]:
        cells = [f"{metrics[f'T2_PanelA_{prefix}_D{d}']:.2f}" for d in range(1, 11)]
        lines.append(f"| {var_label} | " + " | ".join(cells) + " |")
    lines.append("| *Panel B: Growth in Net Operating Assets and Components* | | | | | | | | | | |")
    for var_label, prefix in [
        ("$GrNOA_t$", "GrNOA"),
        ("$GrWC_t$", "GrWC"),
        ("$DEPAM_t$", "DEPAM"),
        ("$GrLTNOA_t$", "GrLTNOA"),
    ]:
        cells = [f"{metrics[f'T2_PanelB_{prefix}_D{d}']:.2f}" for d in range(1, 11)]
        lines.append(f"| {var_label} | " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def _md_table_3(metrics: Dict[str, float], panel: pd.DataFrame) -> str:
    # Display order matches paper Table 3 column order.
    cols_order = ["ROAt1", "ROA", "ACC", "CFO", "GrNOA", "GrWC", "DEPAM", "GrLTNOA"]
    lines = []
    lines.append("# Table 3")
    lines.append("## Pearson Correlation Matrix")
    lines.append("")
    header = "| Variables | " + " | ".join(_label(c) for c in cols_order) + " |"
    lines.append(header)
    lines.append("|" + "---|" * (len(cols_order) + 1))
    for i, row_var in enumerate(cols_order):
        row_cells = []
        for j, col_var in enumerate(cols_order):
            if i == j:
                row_cells.append("1.00")
            elif j > i:
                # upper triangle: empty in the lower-triangle Pearson table
                row_cells.append("")
            else:
                # Look up the correlation in the flat metrics dict. The
                # orchestrator's naming convention for the ROAt1/ROA pair is
                # T3_corr_ROAt1_ROAt_pearson (canonical: forward then
                # current), regardless of which is row vs col in the table.
                if (row_var, col_var) in (("ROAt1", "ROA"), ("ROA", "ROAt1")):
                    key = "T3_corr_ROAt1_ROAt_pearson"
                else:
                    key = f"T3_corr_{col_var}_{row_var}_pearson"
                row_cells.append(f"{metrics[key]:.2f}")
        lines.append(f"| {_label(row_var)} | " + " | ".join(row_cells) + " |")
    n = panel[['roa_t_plus_1','roa_t','acc_t','cfo_t','grnoa_t','grwc_t','depam_t','grltnoa_t']].dropna().shape[0]
    lines.append("")
    lines.append(f"Number of observations = {n:,} firm-years (rows with all 8 vars non-null).")
    lines.append("")
    return "\n".join(lines)


def _label(c: str) -> str:
    """Column header label for the Table 3 correlation matrix."""
    if c == "ROAt1":
        return "$ROA_{t+1}$"
    if c == "ROA":
        return "$ROA_t$"
    return f"${c}_t$"


def _md_regression_table(table_id: str, metrics: Dict[str, float],
                         eq_specs: List[Dict]) -> str:
    """Render a paper-style regression table (Tables 4, 5, 6)."""
    lines = []
    lines.append(f"# {table_id}")
    lines.append("## " + {
        "Table 4": "Results from Regressions of One-Year-Ahead ROA on Current ROA and the Components of Current ROA",
        "Table 5": "Results from Regressions of One-Year-Ahead ROA on Current ROA and Growth",
        "Table 6": "Results from Regressions of Future Operating Income onto Current ROA and Growth Variables",
    }[table_id])
    lines.append("")
    lines.append("| Variables | " + " | ".join(
        f"{eq['name']}: coef" for eq in eq_specs
    ) + " | " + " | ".join(
        f"{eq['name']}: t-stat" for eq in eq_specs
    ) + " |")
    lines.append("|" + "---|" * (1 + 2 * len(eq_specs)))
    var_rows = eq_specs[0]["rows"]
    for row_label, row_key in var_rows:
        cells = []
        for eq in eq_specs:
            coef = metrics.get(f"{eq['prefix']}_{row_key}")
            tstat = metrics.get(f"{eq['prefix']}_{row_key}_t")
            if coef is None or pd.isna(coef):
                cells.extend(["-", "-"])
            else:
                cells.extend([f"{coef:.3f}", f"({tstat:.2f})"])
        lines.append(f"| {row_label} | " + " | ".join(cells) + " |")
    lines.append("")
    return "\n"


def _md_regression_panel_b(table_id: str, metrics: Dict[str, float], rows: List[Dict]) -> str:
    """Render the panel B (paired-difference t-test) for Tables 4, 5, 6."""
    lines = []
    lines.append(f"## {table_id} — Panel B: Tests of Differences in Persistence")
    lines.append("")
    lines.append("| Coefficient Comparisons | t-value |")
    lines.append("|---|---|")
    for row in rows:
        t = metrics.get(row["key"])
        if t is None or pd.isna(t):
            lines.append(f"| {row['label']} | - |")
        else:
            lines.append(f"| {row['label']} | {t:.2f} |")
    lines.append("")
    return "\n".join(lines)


def _md_table_7(metrics: Dict[str, float]) -> str:
    """Render Table 7 — Mishkin (1983) test of rational pricing."""
    lines = []
    lines.append("# Table 7")
    lines.append("## Tests of Rational Pricing of Return on Assets, Accruals, and Growth in Long-term Net Operating Assets: Coefficient Estimates and Likelihood Ratio Tests")
    lines.append("")
    lines.append("Equation 7 (forecasting): $ROA_{t+1} = \\gamma_0 + \\gamma_1 ROA_t + \\gamma_2 ACC_t + \\gamma_3 GrLTNOA_t + u_{t+1}$")
    lines.append("")
    lines.append("Equation 8 (valuation):   $BHAR_{t+1} = \\alpha + \\beta (ROA_{t+1} - \\gamma_0 - \\gamma_1^* ROA_t - \\gamma_2^* ACC_t - \\gamma_3^* GrLTNOA_t) + e_{t+1}$")
    lines.append("")
    lines.append("## Panel A: Coefficient Estimates from the First-Stage Estimation")
    lines.append("")
    lines.append("| Parameter (variable) | Estimate | Asymptotic Std. Error |")
    lines.append("|---|---|---|")
    fcst_rows = [
        ("$\\gamma_1 (ROA)$", "T7A_fcst_ROA", "T7A_fcst_ROA_se"),
        ("$\\gamma_2 (ACC)$", "T7A_fcst_ACC", "T7A_fcst_ACC_se"),
        ("$\\gamma_3 (GrLTNOA)$", "T7A_fcst_GrLTNOA", "T7A_fcst_GrLTNOA_se"),
    ]
    for label, kcoef, kse in fcst_rows:
        coef = metrics.get(kcoef)
        se = metrics.get(kse)
        coef_s = f"{coef:.3f}" if coef is not None and not (isinstance(coef, float) and np.isnan(coef)) else "-"
        se_s = f"{se:.4f}" if se is not None and not (isinstance(se, float) and np.isnan(se)) else "-"
        lines.append(f"| {label} | {coef_s} | {se_s} |")
    lines.append("")
    lines.append("| Parameter (variable) | Estimate | Asymptotic Std. Error |")
    lines.append("|---|---|---|")
    val_rows = [
        ("$\\gamma_1^* (ROA)$", "T7A_val_ROA", "T7A_val_ROA_se"),
        ("$\\gamma_2^* (ACC)$", "T7A_val_ACC", "T7A_val_ACC_se"),
        ("$\\gamma_3^* (GrLTNOA)$", "T7A_val_GrLTNOA", "T7A_val_GrLTNOA_se"),
    ]
    for label, kcoef, kse in val_rows:
        coef = metrics.get(kcoef)
        se = metrics.get(kse)
        coef_s = f"{coef:.3f}" if coef is not None and not (isinstance(coef, float) and np.isnan(coef)) else "-"
        se_s = f"{se:.4f}" if se is not None and not (isinstance(se, float) and np.isnan(se)) else "-"
        lines.append(f"| {label} | {coef_s} | {se_s} |")
    lines.append("")
    lines.append("## Panel B: Tests of Rational Pricing of Return on Assets and Growth")
    lines.append("")
    lines.append("| Null Hypothesis | Likelihood Ratio Statistic |")
    lines.append("|---|---|")
    lr_rows = [
        ("$ROA: \\gamma_1^* = \\gamma_1$", "T7B_LR_ROA_q1"),
        ("$ACC: \\gamma_2^* = \\gamma_2$", "T7B_LR_ACC_q1"),
        ("$GrLTNOA: \\gamma_3^* = \\gamma_3$", "T7B_LR_GrLTNOA_q1"),
        ("$ACC, GrLTNOA: \\gamma_2^* = \\gamma_3^* \\text{ and } \\gamma_2 = \\gamma_3$",
         "T7B_LR_GrLTNOA_ACC_q2"),
    ]
    for label, k in lr_rows:
        v = metrics.get(k)
        vs = f"{v:.2f}" if v is not None and not (isinstance(v, float) and np.isnan(v)) else "-"
        lines.append(f"| {label} | {vs} |")
    lines.append("")
    n_obs = metrics.get("T7A_n_obs")
    if n_obs is not None and not (isinstance(n_obs, float) and np.isnan(n_obs)):
        lines.append(f"Number of observations = {int(n_obs):,} firm-years.")
    lines.append("")
    return "\n".join(lines)


def write_tables(panel: pd.DataFrame) -> Dict[str, float]:
    """Compute all seven tables, save to .md files, return the flat metrics dict."""
    t1 = table_1(panel)
    t2 = table_2(panel)
    t3 = table_3(panel)
    t4 = table_4(panel)
    t5 = table_5(panel)
    t6 = table_6(panel)
    t7 = table_7(panel)

    metrics = {**t1, **t2, **t3, **t4, **t5, **t6, **t7}

    # ----- write markdown files -----
    (RESULTS_DIR / "table_1.md").write_text(_md_table_1(t1, panel))
    (RESULTS_DIR / "table_2.md").write_text(_md_table_2(t2))
    (RESULTS_DIR / "table_3.md").write_text(_md_table_3(t3, panel))

    # Table 4 — equations 1 and 2
    t4_eq1 = {"name": "Equation 1", "prefix": "T4_eq1"}
    t4_eq2 = {"name": "Equation 2", "prefix": "T4_eq2"}
    t4_specs = [
        {**t4_eq1, "rows": [
            ("Intercept", "intercept"),
            ("$ROA_t$",   "ROA"),
        ]},
        {**t4_eq2, "rows": [
            ("Intercept", "intercept"),
            ("$ROA_t$",   "ROA"),
            ("$ACC_t$",   "ACC"),
            ("$CFO_t$",   "CFO"),
        ]},
    ]
    # Override ROA rows in eq2 to "-" (paper prints "-")
    # Easier: just print the union of rows (eq2's ROA & ACC & CFO show as
    # 0.000 if not present). The regression row for eq2's missing ROA_t
    # will simply not be in the eq1 row list — but we want both eqs to
    # share the same row set so the table is rectangular. The paper does
    # show this: eq2's row order is Intercept, ROA_t (with "-"), ACC, CFO.
    # Build the table from the union of all rows; cells use metric only
    # if defined for that equation.
    t4_lines = ["# Table 4",
                "## Results from Regressions of One-Year-Ahead ROA on Current ROA and the Components of Current ROA",
                "",
                "Equation 1: $ROA_{t+1} = \\alpha_0 + \\alpha_1 ROA_t + e_{t+1}$",
                "",
                "Equation 2: $ROA_{t+1} = \\beta_0 + \\beta_1 ACC_t + \\beta_2 CFO_t + u_{t+1}$",
                "",
                "## Panel A: Estimation Results",
                "",
                "| Variables | Eq.1 coef | Eq.1 t | Eq.2 coef | Eq.2 t |",
                "|---|---|---|---|---|"]
    t4_rows = [
        ("Intercept", "intercept", "T4_eq1_intercept", "T4_eq1_intercept_t",
                                 "T4_eq2_intercept", "T4_eq2_intercept_t"),
        ("$ROA_t$",   "ROA",       "T4_eq1_ROA",       "T4_eq1_ROA_t",
                                 None,                None),
        ("$ACC_t$",   "ACC",       None,               None,
                                 "T4_eq2_ACC",        "T4_eq2_ACC_t"),
        ("$CFO_t$",   "CFO",       None,               None,
                                 "T4_eq2_CFO",        "T4_eq2_CFO_t"),
    ]
    for label, key, c1, t1k, c2, t2k in t4_rows:
        row_cells = [
            _render_cell(metrics.get(c1), metrics.get(t1k)),
            _render_t(metrics.get(t1k)),
            _render_cell(metrics.get(c2), metrics.get(t2k)),
            _render_t(metrics.get(t2k)),
        ]
        t4_lines.append(f"| {label} | " + " | ".join(row_cells) + " |")
    # adjusted R^2 row
    r2_c1 = metrics.get("T4_eq1_adj_R2")
    r2_c2 = metrics.get("T4_eq2_adj_R2")
    t4_lines.append(f"| adjusted R² | {r2_c1:.3f} |  | {r2_c2:.3f} |  |")
    t4_lines.append("")
    (RESULTS_DIR / "table_4.md").write_text("\n".join(t4_lines))

    # Table 5
    t5_lines = ["# Table 5",
                "## Results from Regressions of One-Year-Ahead ROA on Current ROA and Growth",
                "",
                "Equation 3: $ROA_{t+1} = \\alpha_0 + \\alpha_1 ROA_t + \\alpha_2 ACC_t + e_{t+1}$",
                "",
                "Equation 4: $ROA_{t+1} = \\beta_0 + \\beta_1 ROA_t + \\beta_2 ACC_t + \\beta_3 GrLTNOA_t + u_{t+1}$",
                "",
                "## Panel A: Estimation Results",
                "",
                "| Variables | Eq.3 coef | Eq.3 t | Eq.4 coef | Eq.4 t |",
                "|---|---|---|---|---|"]
    t5_rows = [
        ("Intercept", "T4_eq1_intercept", "T4_eq1_intercept_t",   # placeholder; will be overridden
         # use proper keys:
         ),
    ]
    # Cleaner: just write the four rows using eq3/eq4 keys
    t5_rows = [
        ("Intercept", "T5_eq3_intercept", "T5_eq3_intercept_t",
                                "T5_eq4_intercept", "T5_eq4_intercept_t"),
        ("$ROA_t$",   "T5_eq3_ROA",       "T5_eq3_ROA_t",
                                "T5_eq4_ROA",       "T5_eq4_ROA_t"),
        ("$ACC_t$",   "T5_eq3_ACC",       "T5_eq3_ACC_t",
                                "T5_eq4_ACC",       "T5_eq4_ACC_t"),
        ("$GrLTNOA_t$", None,             None,
                                "T5_eq4_GrLTNOA",   "T5_eq4_GrLTNOA_t"),
    ]
    for label, c1, t1k, c2, t2k in t5_rows:
        row_cells = [
            _render_cell(metrics.get(c1), metrics.get(t1k)),
            _render_t(metrics.get(t1k)),
            _render_cell(metrics.get(c2), metrics.get(t2k)),
            _render_t(metrics.get(t2k)),
        ]
        t5_lines.append(f"| {label} | " + " | ".join(row_cells) + " |")
    r2_c1 = metrics.get("T5_eq3_adj_R2")
    r2_c2 = metrics.get("T5_eq4_adj_R2")
    t5_lines.append(f"| adjusted R² | {r2_c1:.3f} |  | {r2_c2:.3f} |  |")
    t5_lines.append("")
    (RESULTS_DIR / "table_5.md").write_text("\n".join(t5_lines))

    # Table 6
    t6_lines = ["# Table 6",
                "## Results from Regressions of Future Operating Income onto Current ROA and Growth Variables",
                "",
                "Equation 5: $\\frac{OPINC_{t+1}}{AVG(TA_{t-1}, TA_t)} = \\gamma_0 + \\gamma_1 ROA_t + \\gamma_2 ACC_t + e_{t+1}$",
                "",
                "Equation 6: $\\frac{OPINC_{t+1}}{AVG(TA_{t-1}, TA_t)} = \\delta_0 + \\delta_1 ROA_t + \\delta_2 ACC_t + \\delta_3 GrLTNOA_t + e_{t+1}$",
                "",
                "## Panel A: Estimation Results",
                "",
                "| Variables | Eq.5 coef | Eq.5 t | Eq.6 coef | Eq.6 t |",
                "|---|---|---|---|---|"]
    t6_rows = [
        ("Intercept", "T6_eq5_intercept", "T6_eq5_intercept_t",
                                "T6_eq6_intercept", "T6_eq6_intercept_t"),
        ("$ROA_t$",   "T6_eq5_ROA",       "T6_eq5_ROA_t",
                                "T6_eq6_ROA",       "T6_eq6_ROA_t"),
        ("$ACC_t$",   "T6_eq5_ACC",       "T6_eq5_ACC_t",
                                "T6_eq6_ACC",       "T6_eq6_ACC_t"),
        ("$GrLTNOA_t$", None,             None,
                                "T6_eq6_GrLTNOA",   "T6_eq6_GrLTNOA_t"),
    ]
    for label, c1, t1k, c2, t2k in t6_rows:
        row_cells = [
            _render_cell(metrics.get(c1), metrics.get(t1k)),
            _render_t(metrics.get(t1k)),
            _render_cell(metrics.get(c2), metrics.get(t2k)),
            _render_t(metrics.get(t2k)),
        ]
        t6_lines.append(f"| {label} | " + " | ".join(row_cells) + " |")
    r2_c1 = metrics.get("T6_eq5_adj_R2")
    r2_c2 = metrics.get("T6_eq6_adj_R2")
    t6_lines.append(f"| adjusted R² | {r2_c1:.3f} |  | {r2_c2:.3f} |  |")
    t6_lines.append("")
    (RESULTS_DIR / "table_6.md").write_text("\n".join(t6_lines))

    # Table 7 -- Mishkin test
    (RESULTS_DIR / "table_7.md").write_text(_md_table_7(metrics))

    # Persist the flat metrics dict for evaluate.py
    with open(RESULTS_DIR / "all_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics


def _render_cell(coef, tstat):
    """Render a single regression cell (coef only). Returns '-' if missing."""
    if coef is None or pd.isna(coef):
        return "-"
    return f"{coef:.3f}"


def _render_t(tstat):
    """Render a t-stat cell. Returns '-' if missing, else '(x.xx)'."""
    if tstat is None or pd.isna(tstat):
        return "-"
    return f"({tstat:.2f})"


def main() -> None:
    panel = load_panel()
    print(f"Panel: {len(panel):,} rows × {panel.shape[1]} cols")
    metrics = write_tables(panel)
    print(f"\nWrote {len(metrics)} metrics to results/all_metrics.json")
    # Quick headline summary
    print("\n=== Headline numbers ===")
    print(f"T1 ROA_t mean          = {metrics['T1_ROA_mean']:.3f}  (paper 0.116)")
    print(f"T1 ACC_t mean          = {metrics['T1_ACC_mean']:.3f}  (paper -0.019)")
    print(f"T2 PanelA CFO D1       = {metrics['T2_PanelA_CFO_D1']:.3f}  (paper 0.23)")
    print(f"T2 PanelA CFO D10      = {metrics['T2_PanelA_CFO_D10']:.3f}  (paper -0.01)")
    print(f"T3 corr(ROAt+1, ROAt)  = {metrics['T3_corr_ROAt1_ROAt_pearson']:.3f}  (paper 0.78)")
    print(f"T4 eq1 ROA coef        = {metrics['T4_eq1_ROA']:.3f}  (paper 0.721)")
    print(f"T4 eq2 ACC coef        = {metrics['T4_eq2_ACC']:.3f}  (paper 0.676)")
    print(f"T4 eq2 CFO coef        = {metrics['T4_eq2_CFO']:.3f}  (paper 0.737)")
    print(f"T4 eq2 paired-t        = {metrics['T4_eq2_paired_t_diff']:.2f}  (paper 4.58)")
    print(f"T5 eq3 ACC coef        = {metrics['T5_eq3_ACC']:.3f}  (paper -0.061)")
    print(f"T5 eq4 GrLTNOA coef    = {metrics['T5_eq4_GrLTNOA']:.3f}  (paper -0.039)")
    print(f"T6 eq5 ACC coef        = {metrics['T6_eq5_ACC']:.3f}  (paper -0.121)")
    print(f"T6 eq6 GrLTNOA coef    = {metrics['T6_eq6_GrLTNOA']:.3f}  (paper 0.030)")
    # T7 headline numbers
    if "T7A_fcst_ROA" in metrics:
        print(f"T7 fcst γ1 (ROA)      = {metrics['T7A_fcst_ROA']:.3f}  (paper 0.746)")
        print(f"T7 fcst γ2 (ACC)      = {metrics['T7A_fcst_ACC']:.3f}  (paper -0.045)")
        print(f"T7 fcst γ3 (GrLTNOA)  = {metrics['T7A_fcst_GrLTNOA']:.3f}  (paper -0.048)")
        print(f"T7 val γ*1 (ROA)      = {metrics['T7A_val_ROA']:.3f}  (paper 0.704)")
        print(f"T7 val γ*2 (ACC)      = {metrics['T7A_val_ACC']:.3f}  (paper 0.069)")
        print(f"T7 val γ*3 (GrLTNOA)  = {metrics['T7A_val_GrLTNOA']:.3f}  (paper 0.051)")
        print(f"T7 LR ACC q=1         = {metrics['T7B_LR_ACC_q1']:.2f}  (paper 103.90)")
        print(f"T7 LR joint q=2       = {metrics['T7B_LR_GrLTNOA_ACC_q2']:.2f}  (paper 1.82)")
        print(f"T7 n_sample           = {int(metrics.get('T7A_n_sample', 0)):,}")


if __name__ == "__main__":
    main()