"""
Replication of Lev & Nissim (2004) Table 3 — Cross-sectional
regressions of future earnings growth on tax/cash flow fundamentals
plus nine standard earnings predictors (the augmented Eq. 4).

  G = α_indu + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO +
      γ_1 PRED_1 + ... + γ_9 PRED_9 + ε

The PRED_1..PRED_9 controls (per paper's Table 3 footnote 25 and the
preprocessing rule `var_pred_1_to_9`):
  PRED_1: ratio of earnings to total assets = ib / at
  PRED_2: current period earnings change / total assets = (ib - ib_{t-1}) / at
  PRED_3: avg change in earnings over last 3 years / at = ((ib - ib_{t-3}) / 3) / at
  PRED_4: avg change in earnings over last 5 years / at = ((ib - ib_{t-5}) / 5) / at
  PRED_5: dividends / total assets = dv / at
  PRED_6: R&D / sales = xrd / sale
  PRED_7: capital expenditures / sales = capx / sale
  PRED_8: earnings-price ratio = (ib / (prcc_f × csho)) × 100
  PRED_9: book-to-market = ceq / (prcc_f × csho)

For Table 3, the paper uses the current fiscal-year-end E/P ratio
(not the P*-based ratio used in Table 4/5).

Models (paper runs 4 nested specs per panel; we commit the headline R_TAX
and R_CFO cells from M1 and M4):
  Model 1: G = α + β_1 R_TAX                                          (R_TAX only)
  Model 2: G = α + β_2 R_DEF                                          (R_DEF only)
  Model 3: G = α + β_1 R_TAX + β_2 R_DEF                              (R_TAX + R_DEF)
  Model 4: G = α + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO +
                  γ_1 PRED_1 + ... + γ_9 PRED_9                        (full model)

Per the paper's footnote 25, the paper omits the nine PRED coefficients
from the published table for parsimony. We do the same.

Inputs:
  data/panel.parquet  (the comp-side panel from src/main.py)

Outputs:
  results/table_3.md
  results/table_3_cells.json

Per-iteration caveats:
  - PRED_3 (3-year lag) is only non-null for fyear >= 1990 (because the
    panel only has ib for fyear >= 1987). PRED_4 (5-year lag) is only
    non-null for fyear >= 1992. Both are documented as expected
    shrinkage of the panel at the early years.
  - For T3, the paper uses the current fiscal-year-end E/P ratio (PRED_8
    in the Table 3 PRED vector); we compute it the same way as the
    Table 4 paper definition but use prcc_f × csho (no P* adjustment).
  - The paper applies the 0.5%-99.5% winsorization to all the analysis
    variables. We follow the same convention and apply within-year
    winsorization to G, R_TAX, R_DEF, R_CFO, and the PRED controls.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from utils.paths import paper_layout  # noqa: E402

SLUG = "lev_nissim_2004_taxable_income_future_earnings_and_equity_values"
LAYOUT = paper_layout(SLUG)


# --------------------------------------------------------------------------
# Panel definitions (same as T2)
# --------------------------------------------------------------------------

PANEL_A_YEARS = range(1987, 1993)
PANEL_B_YEARS = range(1993, 2001)

PANELS: dict[str, tuple[str, range]] = {
    "A": ("Pre-SFAS 109", PANEL_A_YEARS),
    "B": ("Post-SFAS 109", PANEL_B_YEARS),
}

GROWTH_VARS = ["g1", "g3"]
GROWTH_LABELS = {"g1": "G1", "g3": "G3"}

# PRED columns (computed in `add_pred_columns`).
PRED_COLS = [
    "pred_1",
    "pred_2",
    "pred_3",
    "pred_4",
    "pred_5",
    "pred_6",
    "pred_7",
    "pred_8",
    "pred_9",
]

# Models — each maps to the list of independent variable columns.
# All models include two-digit SIC industry dummies (added separately).
MODELS: dict[str, dict] = {
    "1": {
        "name": "Model 1 — R_TAX only",
        "x_cols": ["r_tax"],
    },
    "2": {
        "name": "Model 2 — R_DEF only",
        "x_cols": ["r_def"],
    },
    "3": {
        "name": "Model 3 — R_TAX + R_DEF",
        "x_cols": ["r_tax", "r_def"],
    },
    "4": {
        "name": "Model 4 — Full model (R_TAX + R_DEF + R_CFO + PRED_1..9)",
        "x_cols": ["r_tax", "r_def", "r_cfo"] + PRED_COLS,
    },
}


# --------------------------------------------------------------------------
# PRED columns construction
# --------------------------------------------------------------------------

def add_pred_columns(panel_df: pd.DataFrame) -> pd.DataFrame:
    """Compute the nine PRED_1..PRED_9 columns and return the augmented df.

    Requires `lag_ib` (1-year lag of ib) to be present. Adds 3-year and
    5-year lags of ib via `groupby(gvkey).shift(k)` — these are NaN for
    the first 3 / 5 years of each firm's history.
    """
    df = panel_df.copy()
    df = df.sort_values(["gvkey", "fyear"]).reset_index(drop=True)

    # 3-year and 5-year lags of ib (computed from the same gvkey).
    df["lag_ib_3"] = df.groupby("gvkey")["ib"].shift(3)
    df["lag_ib_5"] = df.groupby("gvkey")["ib"].shift(5)
    # lag_ib is already 1-year lag in the panel.

    # PRED_1: ib / at (current earnings to total assets)
    df["pred_1"] = df["ib"] / df["at"]

    # PRED_2: (ib_t - ib_{t-1}) / at_t
    df["pred_2"] = (df["ib"] - df["lag_ib"]) / df["at"]

    # PRED_3: avg change in earnings over last 3 years / at_t
    # = ((ib_t - ib_{t-3}) / 3) / at_t
    df["pred_3"] = ((df["ib"] - df["lag_ib_3"]) / 3.0) / df["at"]

    # PRED_4: avg change in earnings over last 5 years / at_t
    # = ((ib_t - ib_{t-5}) / 5) / at_t
    df["pred_4"] = ((df["ib"] - df["lag_ib_5"]) / 5.0) / df["at"]

    # PRED_5: dividends / at
    df["pred_5"] = df["dv"] / df["at"]

    # PRED_6: R&D / sale
    df["pred_6"] = df["xrd"] / df["sale"]

    # PRED_7: capex / sale
    df["pred_7"] = df["capx"] / df["sale"]

    # PRED_8: E/P ratio at FYE, in percentage points
    # = (ib / (prcc_f × csho)) × 100
    me_fye = df["prcc_f"] * df["csho"]
    df["pred_8"] = (df["ib"] / me_fye) * 100.0

    # PRED_9: book-to-market = ceq / (prcc_f × csho)
    df["pred_9"] = df["ceq"] / me_fye

    return df


# --------------------------------------------------------------------------
# Within-year winsorization (paper rule 24: 0.5%-99.5%)
# --------------------------------------------------------------------------

WINSORIZE_LO = 0.005
WINSORIZE_HI = 0.995


def winsorize_within_year(
    df_year: pd.DataFrame, cols: Iterable[str]
) -> pd.DataFrame:
    """Clip each column to its [0.5%, 99.5%] within-year range."""
    out = df_year.copy()
    for c in cols:
        if c not in out.columns:
            continue
        s = out[c]
        if s.notna().sum() < 10:
            continue
        lo = float(s.quantile(WINSORIZE_LO))
        hi = float(s.quantile(WINSORIZE_HI))
        out[c] = s.clip(lower=lo, upper=hi)
    return out


# --------------------------------------------------------------------------
# Industry FE helpers
# --------------------------------------------------------------------------

def add_industry_dummies(
    df: pd.DataFrame, reference_industry: int | None = None
) -> tuple[pd.DataFrame, list[str]]:
    """Add 2-digit SIC industry dummy columns; drop one as reference."""
    out = df.copy()
    counts = out["sich_2digit"].value_counts()
    if reference_industry is None:
        reference_industry = int(counts.idxmin())
    dummies = pd.get_dummies(
        out["sich_2digit"].astype(int), prefix="ind", dtype=float
    )
    if f"ind_{reference_industry}" in dummies.columns:
        dummies = dummies.drop(columns=[f"ind_{reference_industry}"])
    out = pd.concat([out, dummies], axis=1)
    return out, list(dummies.columns)


# --------------------------------------------------------------------------
# Single cross-sectional regression per year per model
# --------------------------------------------------------------------------

def fit_year_regression(
    df_year: pd.DataFrame,
    y_col: str,
    x_cols: list[str],
    ind_dummies: list[str],
    winsorize: bool = True,
) -> dict | None:
    """Run a single OLS for one (year, model) cell.

    Returns a dict {betas: {var: coef}, r2: float, n: int} or None if
    the design matrix is too thin or rank-deficient.
    """
    cols_to_wins = [y_col] + list(x_cols)
    work = df_year
    if winsorize:
        work = winsorize_within_year(df_year, cols_to_wins)

    cols_needed = cols_to_wins + ind_dummies
    sub = work.dropna(subset=cols_needed)
    n = len(sub)
    if n < len(x_cols) + len(ind_dummies) + 5:
        return None

    y = sub[y_col].astype(float).values
    X_parts: list[np.ndarray] = []
    for c in x_cols:
        X_parts.append(sub[c].astype(float).values.reshape(-1, 1))
    for c in ind_dummies:
        X_parts.append(sub[c].astype(float).values.reshape(-1, 1))
    X = np.hstack(X_parts)

    try:
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    except np.linalg.LinAlgError:
        return None

    yhat = X @ beta
    resid = y - yhat
    ss_res = float(resid @ resid)
    ss_tot = float((y - y.mean()) @ (y - y.mean()))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan

    return {
        "betas": dict(zip(x_cols, [float(b) for b in beta[: len(x_cols)]])),
        "r2": float(r2),
        "n": int(n),
    }


# --------------------------------------------------------------------------
# Run one (panel, model, G) cell — annual fits + time-series average.
# --------------------------------------------------------------------------

def run_cell(
    panel_df: pd.DataFrame,
    panel_letter: str,
    model_id: str,
    g_col: str,
) -> dict:
    """Run one (panel, model, G) cell of Table 3."""
    _, years = PANELS[panel_letter]
    x_cols = MODELS[model_id]["x_cols"]

    panel_with_dum, ind_dummies = add_industry_dummies(panel_df)

    per_year: list[dict] = []
    n_skipped = 0
    skip_reasons: list[str] = []
    for fyear in years:
        sub_year = panel_with_dum[panel_with_dum["fyear"] == fyear]
        if sub_year.empty:
            n_skipped += 1
            skip_reasons.append(f"{fyear}: empty")
            continue
        result = fit_year_regression(
            df_year=sub_year,
            y_col=g_col,
            x_cols=x_cols,
            ind_dummies=ind_dummies,
        )
        if result is None:
            n_skipped += 1
            skip_reasons.append(f"{fyear}: too thin")
            continue
        per_year.append({"fyear": int(fyear), **result})

    if not per_year:
        return {
            "panel": panel_letter,
            "model": model_id,
            "g": g_col,
            "mean_betas": {},
            "std_betas": {},
            "t_stats": {},
            "mean_r2": float("nan"),
            "mean_n": 0,
            "n_periods_used": 0,
            "n_periods_skipped": len(list(years)),
            "n_periods_total": len(list(years)),
            "skip_reasons": skip_reasons,
            "per_year": [],
        }

    coef_df = pd.DataFrame([r["betas"] for r in per_year])
    mean_betas = coef_df.mean()
    std_betas = coef_df.std(ddof=1)
    t_stats = mean_betas / std_betas.replace(0, np.nan)
    mean_r2 = float(np.mean([r["r2"] for r in per_year]))
    mean_n = int(np.mean([r["n"] for r in per_year]))

    return {
        "panel": panel_letter,
        "model": model_id,
        "g": g_col,
        "mean_betas": mean_betas.to_dict(),
        "std_betas": std_betas.to_dict(),
        "t_stats": t_stats.to_dict(),
        "mean_r2": mean_r2,
        "mean_n": mean_n,
        "n_periods_used": len(per_year),
        "n_periods_skipped": n_skipped,
        "n_periods_total": len(list(years)),
        "skip_reasons": skip_reasons,
        "per_year": per_year,
    }


# --------------------------------------------------------------------------
# Run the full Table 3 grid
# --------------------------------------------------------------------------

def run_table3(panel_df: pd.DataFrame) -> dict:
    """Run Table 3: 4 models × 2 G-vars × 2 panels = 16 cells."""
    results: dict = {}
    for panel_letter in ("A", "B"):
        results[panel_letter] = {}
        for model_id in MODELS:
            results[panel_letter][model_id] = {}
            for g_col in GROWTH_VARS:
                results[panel_letter][model_id][g_col] = run_cell(
                    panel_df, panel_letter, model_id, g_col
                )
    return results


# --------------------------------------------------------------------------
# Pretty-printing helpers
# --------------------------------------------------------------------------

def _fmt(coef: float | None, t_stat: float | None) -> str:
    if coef is None or (isinstance(coef, float) and np.isnan(coef)):
        return "  -    "
    s = f"{coef:+.3f}"
    if t_stat is not None and not np.isnan(t_stat):
        ts = f"{t_stat:5.2f}"
    else:
        ts = "  -  "
    return f"{s} ({ts})"


def render_markdown(results: dict) -> str:
    """Render Table 3 in markdown.

    Per the paper's footnote 25, the nine PRED coefficients are omitted
    from the published table. We report only β_1 (R_TAX), β_2 (R_DEF),
    β_3 (R_CFO), R², and n.
    """
    out: list[str] = []
    out.append("# Table 3 — Cross-Sectional Regressions with Nine Earnings Predictors")
    out.append("")
    out.append(
        "G = α_indu + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO + "
        "γ_1 PRED_1 + ... + γ_9 PRED_9 + ε"
    )
    out.append("")
    out.append(
        "Two-digit SIC industry fixed effects, annual cross-sections, "
        "time-series mean (t = mean / std across years)."
    )
    out.append("")
    out.append(
        "Our sample period: fyear 1987-2000 (pre-1987 sparse per "
        "assumption #6). Panel A: 1987-1992 (paper: 1973-1992). "
        "Panel B: 1993-2000 (paper: 1993-2000)."
    )
    out.append("")
    out.append(
        "Per footnote 25, the nine PRED coefficients are omitted from "
        "the published table for parsimony. We report only β_1 (R_TAX), "
        "β_2 (R_DEF), β_3 (R_CFO), R², and n. The PRED_1..PRED_9 "
        "definitions are below."
    )
    out.append("")
    out.append("**PRED_1..PRED_9 definitions (paper footnote 25):**")
    out.append("")
    out.append(
        "- PRED_1: ratio of earnings to total assets = ib / at"
    )
    out.append(
        "- PRED_2: current period earnings change / at = (ib - ib_{t-1}) / at"
    )
    out.append(
        "- PRED_3: avg change in earnings over last 3 years / at = ((ib - ib_{t-3}) / 3) / at"
    )
    out.append(
        "- PRED_4: avg change in earnings over last 5 years / at = ((ib - ib_{t-5}) / 5) / at"
    )
    out.append(
        "- PRED_5: dividends / total assets = dv / at"
    )
    out.append(
        "- PRED_6: R&D / sales = xrd / sale"
    )
    out.append(
        "- PRED_7: capex / sales = capx / sale"
    )
    out.append(
        "- PRED_8: earnings-price ratio (FYE, percentage points) = 100 × ib / (prcc_f × csho)"
    )
    out.append(
        "- PRED_9: book-to-market = ceq / (prcc_f × csho)"
    )
    out.append("")

    for panel_letter in ("A", "B"):
        panel_name, years = PANELS[panel_letter]
        out.append(f"## Panel {panel_letter}: {panel_name} "
                   f"({min(years)}-{max(years)})")
        out.append("")
        header = (
            "| Model | DepVar | "
            "β_1 R_TAX | β_2 R_DEF | β_3 R_CFO | R² | n | "
            "# years used |"
        )
        sep = (
            "|---|---|---:|---:|---:|---:|---:|---:|"
        )
        out.append(header)
        out.append(sep)
        for model_id in MODELS:
            for g_col in GROWTH_VARS:
                cell = results[panel_letter][model_id][g_col]
                mb = cell["mean_betas"]
                ts = cell["t_stats"]
                b1 = _fmt(mb.get("r_tax"), ts.get("r_tax"))
                b2 = _fmt(mb.get("r_def"), ts.get("r_def"))
                b3 = _fmt(mb.get("r_cfo"), ts.get("r_cfo"))
                r2 = f"{cell['mean_r2']:.3f}" if not np.isnan(cell["mean_r2"]) else " - "
                n = cell["mean_n"]
                used = cell["n_periods_used"]
                m_short = {
                    "1": "M1 R_TAX",
                    "2": "M2 R_DEF",
                    "3": "M3 R_TAX+R_DEF",
                    "4": "M4 Full",
                }[model_id]
                out.append(
                    f"| {m_short} | {GROWTH_LABELS[g_col]} | "
                    f"{b1} | {b2} | {b3} | {r2} | {n:.0f} | {used} |"
                )
        out.append("")

    # Paper comparison spot checks
    out.append("## Paper-vs-replication spot checks")
    out.append("")
    out.append("| Cell | Paper | Ours |")
    out.append("|---|---:|---:|")
    paper_spots = [
        ("T3_A R_TAX-only G1 β_1 (mean)", "0.160",
         lambda r: r["A"]["1"]["g1"]["mean_betas"].get("r_tax")),
        ("T3_A R_TAX-only G1 t-stat", "4.905",
         lambda r: r["A"]["1"]["g1"]["t_stats"].get("r_tax")),
        ("T3_A R_TAX-only G3 β_1 (mean)", "0.223",
         lambda r: r["A"]["1"]["g3"]["mean_betas"].get("r_tax")),
        ("T3_A R_TAX-only G3 t-stat", "5.166",
         lambda r: r["A"]["1"]["g3"]["t_stats"].get("r_tax")),
        ("T3_A Full-model G3 β_1 (mean)", "0.222",
         lambda r: r["A"]["4"]["g3"]["mean_betas"].get("r_tax")),
        ("T3_A Full-model G3 t-stat", "4.016",
         lambda r: r["A"]["4"]["g3"]["t_stats"].get("r_tax")),
        ("T3_A Full-model G3 β_3 (R_CFO)", "0.201",
         lambda r: r["A"]["4"]["g3"]["mean_betas"].get("r_cfo")),
        ("T3_B R_TAX-only G1 β_1 (mean)", "0.278",
         lambda r: r["B"]["1"]["g1"]["mean_betas"].get("r_tax")),
        ("T3_B R_TAX-only G1 t-stat", "4.454",
         lambda r: r["B"]["1"]["g1"]["t_stats"].get("r_tax")),
        ("T3_B R_TAX-only G3 β_1 (mean)", "0.495",
         lambda r: r["B"]["1"]["g3"]["mean_betas"].get("r_tax")),
        ("T3_B R_TAX-only G3 t-stat", "10.993",
         lambda r: r["B"]["1"]["g3"]["t_stats"].get("r_tax")),
        ("T3_B Full-model G3 β_1 (mean)", "0.516",
         lambda r: r["B"]["4"]["g3"]["mean_betas"].get("r_tax")),
        ("T3_B Full-model G3 t-stat", "6.442",
         lambda r: r["B"]["4"]["g3"]["t_stats"].get("r_tax")),
        ("T3_B Full-model G3 β_3 (R_CFO)", "0.322",
         lambda r: r["B"]["4"]["g3"]["mean_betas"].get("r_cfo")),
    ]
    for label, paper_val, getter in paper_spots:
        v = getter(results)
        ours_str = f"{v:+.3f}" if v is not None and not np.isnan(v) else " - "
        out.append(f"| {label} | {paper_val} | {ours_str} |")
    out.append("")
    return "\n".join(out)


def _strip_per_year(cell: dict) -> dict:
    return {k: v for k, v in cell.items() if k != "per_year"}


def save_results(results: dict) -> tuple[Path, Path]:
    LAYOUT.ensure()
    md_path = LAYOUT.result_path("table_3.md")
    md_path.write_text(render_markdown(results))

    cells_path = LAYOUT.result_path("table_3_cells.json")
    compact = {
        "schema_version": 1,
        "slug": SLUG,
        "panels": {
            pl: {
                "label": PANELS[pl][0],
                "years": [int(y) for y in PANELS[pl][1]],
                "models": {
                    mid: {
                        "label": MODELS[mid]["name"],
                        "x_cols": MODELS[mid]["x_cols"],
                        "g_vars": {
                            g: _strip_per_year(results[pl][mid][g])
                            for g in GROWTH_VARS
                        },
                    }
                    for mid in MODELS
                },
            }
            for pl in ("A", "B")
        },
    }
    cells_path.write_text(json.dumps(compact, indent=2, default=float))
    return md_path, cells_path


# --------------------------------------------------------------------------
# CLI entrypoint
# --------------------------------------------------------------------------

def main() -> int:
    panel_path = LAYOUT.data_path("panel.parquet")
    if not panel_path.exists():
        print(f"ERROR: {panel_path} does not exist. Run `python src/main.py` first.")
        return 1

    print(f"[1/5] Loading panel from {panel_path} ...")
    df = pd.read_parquet(panel_path)
    print(f"      rows: {len(df):,}, fyear: {df['fyear'].min()}-{df['fyear'].max()}, "
          f"unique (sich_2digit): {df['sich_2digit'].nunique()}")

    print(f"\n[2/5] Adding PRED_1..PRED_9 columns ...")
    df = add_pred_columns(df)
    # PRED_3 / PRED_4 are sparse for early fyears. Print non-null counts.
    for c in PRED_COLS:
        n = int(df[c].notna().sum())
        print(f"      {c}: {n:,} non-null")
    # Per-year PRED_3/PRED_4 non-null counts.
    print("      PRED_3 (3-yr lag) per fyear non-null:")
    for fyear in range(1987, 2001):
        sub = df[df['fyear'] == fyear]
        if not sub.empty:
            n = int(sub['pred_3'].notna().sum())
            print(f"        fyear={fyear}: {n:,} / {len(sub):,}")
    print("      PRED_4 (5-yr lag) per fyear non-null:")
    for fyear in range(1987, 2001):
        sub = df[df['fyear'] == fyear]
        if not sub.empty:
            n = int(sub['pred_4'].notna().sum())
            print(f"        fyear={fyear}: {n:,} / {len(sub):,}")

    print(f"\n[3/5] Running Table 3 cross-sectional regressions ...")
    print(f"      Models: {len(MODELS)}, G-vars: {len(GROWTH_VARS)}, "
          f"panels: 2 -> {len(MODELS) * len(GROWTH_VARS) * 2} cells")
    results = run_table3(df)

    print(f"\n[4/5] Saving results ...")
    md_path, cells_path = save_results(results)
    print(f"      wrote {md_path}")
    print(f"      wrote {cells_path}")

    print(f"\n[5/5] Per-cell summary")
    print(_summary_table(results))

    return 0


def _summary_table(results: dict) -> str:
    lines: list[str] = []
    sep = "-" * 110
    lines.append(sep)
    lines.append(
        f"{'Panel':<8}{'Model':<30}{'G':<5}"
        f"{'β_1 R_TAX':<14}{'t':<8}"
        f"{'β_2 R_DEF':<14}{'t':<8}"
        f"{'β_3 R_CFO':<14}{'t':<8}"
        f"{'R²':<7}{'n':<7}{'yrs':<5}"
    )
    lines.append(sep)
    for panel_letter in ("A", "B"):
        for model_id in MODELS:
            for g_col in GROWTH_VARS:
                cell = results[panel_letter][model_id][g_col]
                mb = cell["mean_betas"]
                ts = cell["t_stats"]

                def _b(b): return f"{b:+.3f}" if b is not None and not np.isnan(b) else "  -   "
                def _t(t): return f"{t:5.2f}" if t is not None and not np.isnan(t) else "  -  "

                lines.append(
                    f"{panel_letter:<8}{MODELS[model_id]['name'][:28]:<30}{GROWTH_LABELS[g_col]:<5}"
                    f"{_b(mb.get('r_tax')):<14}{_t(ts.get('r_tax')):<8}"
                    f"{_b(mb.get('r_def')):<14}{_t(ts.get('r_def')):<8}"
                    f"{_b(mb.get('r_cfo')):<14}{_t(ts.get('r_cfo')):<8}"
                    f"{cell['mean_r2']:<7.3f}{cell['mean_n']:<7.0f}{cell['n_periods_used']:<5}"
                )
    lines.append(sep)
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
