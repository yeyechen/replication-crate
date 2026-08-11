"""
Replication of Lev & Nissim (2004) Table 2 — Cross-sectional
regressions of future earnings growth on tax and cash flow
fundamentals (Eq. 4).

  G = α_indu + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO + ε

Where G ∈ {G1, G2, G3}, R_TAX / R_DEF / R_CFO are industry-year
quintile ranks (1..5). The paper runs four nested model variants
per panel (A: pre-SFAS 109, B: post-SFAS 109):
  Model 1: G = α + β_1 R_TAX                       (R_TAX only)
  Model 2: G = α + β_2 R_DEF                       (R_DEF only)
  Model 3: G = α + β_1 R_TAX + β_2 R_DEF           (R_TAX + R_DEF)
  Model 4: G = α + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO  (all three)

For each (model, G, year) combination we run a cross-sectional OLS
with industry (2-digit SIC) fixed effects, then time-series average
the annual coefficients across years within each panel. Per the
paper's footnote, t = mean(annual_coef) / std(annual_coef) — a
plain iid t-stat across years, NOT a HAC t-stat (this is the
fama_macbeth primitive with n_lags=0 in spirit).

Inputs:  data/panel.parquet  (the comp-side firm-year panel from
         src/sql/comp_panel.sql)
Outputs:
  - results/table_2.md           — markdown table of cell results
  - results/table_2_cells.json   — per-cell results (for the evaluator)
  - prints diagnostics to stdout

This module is importable and callable; main() runs the whole table.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import statsmodels.api as sm

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from utils.paths import paper_layout  # noqa: E402

SLUG = "lev_nissim_2004_taxable_income_future_earnings_and_equity_values"
LAYOUT = paper_layout(SLUG)


# --------------------------------------------------------------------------
# Panel definitions — paper splits at the SFAS No. 109 effective year.
# Paper: Panel A = 1973-1992 (pre-SFAS 109); Panel B = 1993-2000 (post).
# Ours: Panel A = 1987-1992 (data gap per assumption #6); Panel B = 1993-2000.
# --------------------------------------------------------------------------

PANEL_A_YEARS = range(1987, 1993)   # pre-SFAS 109 — paper used 1973-1992
PANEL_B_YEARS = range(1993, 2001)   # post-SFAS 109 — paper used 1993-2000

PANELS: dict[str, tuple[str, range]] = {
    "A": ("Pre-SFAS 109", PANEL_A_YEARS),
    "B": ("Post-SFAS 109", PANEL_B_YEARS),
}

GROWTH_VARS = ["g1", "g2", "g3"]
GROWTH_LABELS = {"g1": "G1", "g2": "G2", "g3": "G3"}

# Model definitions — each maps to the list of independent variable columns
# used in the cross-sectional OLS. Industry dummies are appended separately.
MODELS: dict[str, dict[str, list[str]]] = {
    "1": {"name": "Model 1 — R_TAX only",
          "x_cols": ["r_tax"]},
    "2": {"name": "Model 2 — R_DEF only",
          "x_cols": ["r_def"]},
    "3": {"name": "Model 3 — R_TAX + R_DEF",
          "x_cols": ["r_tax", "r_def"]},
    "4": {"name": "Model 4 — R_TAX + R_DEF + R_CFO",
          "x_cols": ["r_tax", "r_def", "r_cfo"]},
}


# --------------------------------------------------------------------------
# Industry fixed effects — one-hot on sich_2digit, drop one level.
# --------------------------------------------------------------------------

def add_industry_dummies(
    df: pd.DataFrame, reference_industry: int | None = None
) -> tuple[pd.DataFrame, list[str]]:
    """Add 2-digit SIC industry dummy columns to df.

    Drops the `reference_industry` level (the omitted category). If
    `reference_industry` is None, drops the level with the fewest
    firms (most stable baseline).

    Returns the augmented df and the list of dummy column names.
    """
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

WINSORIZE_LO = 0.005
WINSORIZE_HI = 0.995


def winsorize_within_year(
    df_year: pd.DataFrame, cols: Iterable[str]
) -> pd.DataFrame:
    """Clip each column to its [0.5%, 99.5%] range within this year.

    Implements paper's rule `winsorize_0p5_99p5` (rule 24) within each
    analysis year. The paper applies this across the full sample, but
    year-by-year winsorization is the conventional in-time analog that
    avoids using future-year quantiles to clip current-year data.
    """
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


def fit_year_regression(
    df_year: pd.DataFrame,
    y_col: str,
    x_cols: list[str],
    ind_dummies: list[str],
    winsorize: bool = True,
) -> dict | None:
    """Run a single OLS for one (year, model) cell.

    Returns a dict {betas: {var: coef}, r2: float, n: int} or None
    if the year does not have enough observations (or the design
    matrix is rank-deficient).

    If `winsorize` is True (default), each variable (y + x) is
    clipped to its within-year [0.5%, 99.5%] range before fitting.
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

    # No intercept — industry dummies absorb it.
    try:
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    except np.linalg.LinAlgError:
        return None

    yhat = X @ beta
    resid = y - yhat
    ss_res = float(resid @ resid)
    ss_tot = float((y - y.mean()) @ (y - y.mean()))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan

    # Coefficients are returned for the variables in x_cols (the
    # factors the paper reports). Industry dummies are not exposed.
    fac_coefs = beta[: len(x_cols)]
    return {
        "betas": dict(zip(x_cols, [float(b) for b in fac_coefs])),
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
    """Run one (panel, model, G) cell of Table 2.

    Returns a dict with:
      - per_year: list of {fyear, betas, r2, n}
      - mean_betas, std_betas, t_stats (pd.Series)
      - mean_r2, mean_n, n_periods_used, n_periods_skipped
    """
    _, years = PANELS[panel_letter]
    x_cols = MODELS[model_id]["x_cols"]

    # Build industry dummies once over the whole panel — keep the
    # reference industry stable across years within a panel.
    panel_with_dum, ind_dummies = add_industry_dummies(panel_df)

    per_year: list[dict] = []
    n_skipped = 0
    for fyear in years:
        sub_year = panel_with_dum[panel_with_dum["fyear"] == fyear]
        if sub_year.empty:
            n_skipped += 1
            continue
        result = fit_year_regression(
            df_year=sub_year,
            y_col=g_col,
            x_cols=x_cols,
            ind_dummies=ind_dummies,
        )
        if result is None:
            n_skipped += 1
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
            "per_year": [],
        }

    coef_df = pd.DataFrame([r["betas"] for r in per_year])
    mean_betas = coef_df.mean()
    std_betas = coef_df.std(ddof=1)  # sample std
    # Paper t-stat: mean / std (iid across years).
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
        "per_year": per_year,
    }


# --------------------------------------------------------------------------
# Run the full Table 2 grid
# --------------------------------------------------------------------------

def run_table2(panel_df: pd.DataFrame) -> dict:
    """Run Table 2: 4 models × 3 G-vars × 2 panels = 24 cells.

    Returns a nested dict:
      results[panel][model_id][g_col] = cell_dict
    """
    results: dict[str, dict[str, dict[str, dict]]] = {}
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
# Pretty-printing + JSON serialization helpers
# --------------------------------------------------------------------------

def _fmt_coef(coef: float | None, t_stat: float | None) -> str:
    if coef is None or (isinstance(coef, float) and np.isnan(coef)):
        return "  -    "
    s = f"{coef:+.3f}"
    if t_stat is not None and not np.isnan(t_stat):
        ts = f"{t_stat:5.2f}"
    else:
        ts = "  -  "
    return f"{s} ({ts})"


def render_markdown(results: dict) -> str:
    """Render the 12-row × 8-col Table 2 in markdown.

    Layout: 12 rows = 4 models × 3 G-vars. 8 cols = 4 columns per panel:
    β_1 (R_TAX), β_2 (R_DEF), β_3 (R_CFO), R².
    """
    out: list[str] = []
    out.append("# Table 2 — Cross-Sectional Regressions of Future Earnings Growth")
    out.append("")
    out.append(
        "G = α_indu + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO + ε, "
        "two-digit SIC industry fixed effects, annual cross-sections, "
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
        "Each cell shows `mean(t-stat)`. R² and n are the time-series "
        "means of the per-year fit. Variables: β_1 = R_TAX coefficient, "
        "β_2 = R_DEF, β_3 = R_CFO."
    )
    out.append("")

    # Paper Table 2 layout has two side-by-side panels. We render each
    # panel as its own block to keep the markdown readable.
    for panel_letter in ("A", "B"):
        panel_name, years = PANELS[panel_letter]
        out.append(f"## Panel {panel_letter}: {panel_name} ({min(years)}-{max(years)})")
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
            model_name = MODELS[model_id]["name"]
            for g_col in GROWTH_VARS:
                cell = results[panel_letter][model_id][g_col]
                mb = cell["mean_betas"]
                ts = cell["t_stats"]
                b1 = _fmt_coef(mb.get("r_tax"), ts.get("r_tax"))
                b2 = _fmt_coef(mb.get("r_def"), ts.get("r_def"))
                b3 = _fmt_coef(mb.get("r_cfo"), ts.get("r_cfo"))
                r2 = f"{cell['mean_r2']:.3f}" if not np.isnan(cell["mean_r2"]) else " - "
                n = cell["mean_n"]
                used = cell["n_periods_used"]
                # Compact model label (column 1)
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

    # Footnote: paper comparison
    out.append("## Paper-vs-replication spot checks")
    out.append("")
    out.append("| Cell | Paper | Ours |")
    out.append("|---|---:|---:|")
    paper_spots = [
        ("T2_A R_TAX-only G1 β_1 (mean)",
         "0.354",
         lambda r: r["A"]["1"]["g1"]["mean_betas"].get("r_tax")),
        ("T2_A R_TAX-only G1 t-stat",
         "10.36",
         lambda r: r["A"]["1"]["g1"]["t_stats"].get("r_tax")),
        ("T2_A R_TAX-only G3 β_1 (mean)",
         "0.545",
         lambda r: r["A"]["1"]["g3"]["mean_betas"].get("r_tax")),
        ("T2_A R_TAX-only G3 t-stat",
         "15.25",
         lambda r: r["A"]["1"]["g3"]["t_stats"].get("r_tax")),
        ("T2_A Full-model G3 β_1 (mean)",
         "0.618",
         lambda r: r["A"]["4"]["g3"]["mean_betas"].get("r_tax")),
        ("T2_A Full-model G3 t-stat",
         "14.46",
         lambda r: r["A"]["4"]["g3"]["t_stats"].get("r_tax")),
        ("T2_B R_TAX-only G1 β_1 (mean)",
         "0.534",
         lambda r: r["B"]["1"]["g1"]["mean_betas"].get("r_tax")),
        ("T2_B R_TAX-only G1 t-stat",
         "8.53",
         lambda r: r["B"]["1"]["g1"]["t_stats"].get("r_tax")),
    ]
    for label, paper_val, getter in paper_spots:
        v = getter(results)
        ours_str = f"{v:+.3f}" if v is not None and not np.isnan(v) else " - "
        out.append(f"| {label} | {paper_val} | {ours_str} |")
    out.append("")
    return "\n".join(out)


def _strip_per_year(cell: dict) -> dict:
    """Drop the verbose per-year records when serializing to JSON."""
    out = {k: v for k, v in cell.items() if k != "per_year"}
    return out


def save_results(results: dict) -> tuple[Path, Path]:
    """Write results/table_2.md and results/table_2_cells.json. Return paths."""
    LAYOUT.ensure()
    md_path = LAYOUT.result_path("table_2.md")
    md_path.write_text(render_markdown(results))

    cells_path = LAYOUT.result_path("table_2_cells.json")
    # Strip per-year detail to keep the JSON compact.
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

    print(f"[1/4] Loading panel from {panel_path} ...")
    df = pd.read_parquet(panel_path)
    print(f"      rows: {len(df):,}, fyear: {df['fyear'].min()}-{df['fyear'].max()}, "
          f"unique (sich_2digit): {df['sich_2digit'].nunique()}")

    print(f"\n[2/4] Running Table 2 cross-sectional regressions ...")
    print(f"      Models: {len(MODELS)}, G-vars: {len(GROWTH_VARS)}, "
          f"panels: 2 -> {len(MODELS) * len(GROWTH_VARS) * 2} cells")
    results = run_table2(df)

    print(f"\n[3/4] Saving results ...")
    md_path, cells_path = save_results(results)
    print(f"      wrote {md_path}")
    print(f"      wrote {cells_path}")

    print(f"\n[4/4] Per-cell summary")
    print(_summary_table(results))

    print(f"\n[5/5] Paper spot checks (per task spec)")
    paper_spots = [
        ("T2_A_R_TAX_only_G1",
         "beta_1 (R_TAX)",
         "0.354",
         results["A"]["1"]["g1"]["mean_betas"].get("r_tax"),
         results["A"]["1"]["g1"]["t_stats"].get("r_tax")),
        ("T2_A_R_TAX_only_G3",
         "beta_1 (R_TAX)",
         "0.545",
         results["A"]["1"]["g3"]["mean_betas"].get("r_tax"),
         results["A"]["1"]["g3"]["t_stats"].get("r_tax")),
        ("T2_A_full_model_G3",
         "beta_1 (R_TAX)",
         "0.618",
         results["A"]["4"]["g3"]["mean_betas"].get("r_tax"),
         results["A"]["4"]["g3"]["t_stats"].get("r_tax")),
        ("T2_B_R_TAX_only_G1",
         "beta_1 (R_TAX)",
         "0.534",
         results["B"]["1"]["g1"]["mean_betas"].get("r_tax"),
         results["B"]["1"]["g1"]["t_stats"].get("r_tax")),
    ]
    paper_t = {
        "T2_A_R_TAX_only_G1": "10.36",
        "T2_A_R_TAX_only_G3": "15.25",
        "T2_A_full_model_G3": "14.46",
        "T2_B_R_TAX_only_G1": "8.53",
    }
    print(f"  {'Cell':<26}{'Coefficient':<15}{'Paper':<10}{'Ours':<10}{'t-stat paper':<14}{'Ours':<10}{'Sign OK?'}")
    print("  " + "-" * 100)
    for label, var, paper_b, ours_b, ours_t in paper_spots:
        if ours_b is None or (isinstance(ours_b, float) and np.isnan(ours_b)):
            ours_b_str = " - "
            ours_t_str = " - "
            sign_ok = " - "
        else:
            ours_b_str = f"{ours_b:+.3f}"
            ours_t_str = f"{ours_t:.2f}" if ours_t is not None and not np.isnan(ours_t) else " - "
            sign_ok = "yes" if (ours_b > 0) == (float(paper_b) > 0) else "NO"
        print(
            f"  {label:<26}{var:<15}{paper_b:<10}{ours_b_str:<10}"
            f"{paper_t[label]:<14}{ours_t_str:<10}{sign_ok}"
        )
    return 0


def _summary_table(results: dict) -> str:
    """Compact per-cell summary printed at the end of the run."""
    lines: list[str] = []
    sep = "-" * 96
    lines.append(sep)
    lines.append(
        f"{'Panel':<8}{'Model':<25}{'G':<5}"
        f"{'β_1 R_TAX':<14}{'t':<8}"
        f"{'β_2 R_DEF':<14}{'t':<8}"
        f"{'β_3 R_CFO':<14}{'t':<8}"
        f"{'R²':<7}{'n':<7}{'yrs':<5}"
    )
    lines.append(sep)
    for panel_letter in ("A", "B"):
        for model_id in MODELS:
            model_name = MODELS[model_id]["name"]
            for g_col in GROWTH_VARS:
                cell = results[panel_letter][model_id][g_col]
                mb = cell["mean_betas"]
                ts = cell["t_stats"]
                b1 = mb.get("r_tax")
                t1 = ts.get("r_tax")
                b2 = mb.get("r_def")
                t2 = ts.get("r_def")
                b3 = mb.get("r_cfo")
                t3 = ts.get("r_cfo")
                r2 = cell["mean_r2"]
                n = cell["mean_n"]
                used = cell["n_periods_used"]

                def _b(b): return f"{b:+.3f}" if b is not None and not np.isnan(b) else "  -   "
                def _t(t): return f"{t:5.2f}" if t is not None and not np.isnan(t) else "  -  "

                lines.append(
                    f"{panel_letter:<8}{model_name:<25}{GROWTH_LABELS[g_col]:<5}"
                    f"{_b(b1):<14}{_t(t1):<8}"
                    f"{_b(b2):<14}{_t(t2):<8}"
                    f"{_b(b3):<14}{_t(t3):<8}"
                    f"{r2:<7.3f}{n:<7.0f}{used:<5}"
                )
    lines.append(sep)
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
