"""
Replication of Lev & Nissim (2004) Table 5 — Cross-sectional
regressions of one-year-ahead stock return on tax/cash flow
fundamentals + control variables (Eq. 6).

  R = α_indu + β_1 SIZE + β_2 B/P + β_3 E/P + β_4 BETA + β_5 VOL +
      β_6 R_TAX + β_7 R_DEF + β_8 R_CFO + ε

The dependent variable R is the one-year buy-and-hold return from
May of year t+1 to April of year t+2 (12 months). Delisting
proceeds-reinvested-in-VW-index is NOT implemented in this iteration
(assumption #10).

Models (paper runs 3 nested specifications per panel):
  Model 1: R = α + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO       (R_* only)
  Model 2: R = α + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO +
                  β_4 SIZE + β_5 B/P + β_6 E/P               (add SIZE, B/P, E/P)
  Model 3: R = α + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO +
                  β_4 SIZE + β_5 B/P + β_6 E/P +
                  β_7 BETA + β_8 VOL                         (add BETA, VOL)

Industry FE on two-digit SIC.

Panels: A = pre-SFAS (paper: 1973-1992; ours: 1987-1992 because of
the pre-1987 data gap), B = post-SFAS (1993-2000).

Inputs:
  data/panel_crsp.parquet

Outputs:
  results/table_5.md
  results/table_5_cells.json

Per-iteration caveats:
  - BETA, VOL unavailable (assumption #9).
  - Delisting reinvestment not implemented (assumption #10).
  - The "winsorize_excludes_stock_returns" rule (rule 27) is
    observed: we do NOT winsorize the dependent variable (the
    one-year-ahead return).
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
# Panel definitions
# --------------------------------------------------------------------------

PANEL_A_YEARS = range(1987, 1993)
PANEL_B_YEARS = range(1993, 2001)

PANELS: dict[str, tuple[str, range]] = {
    "A": ("Pre-SFAS 109", PANEL_A_YEARS),
    "B": ("Post-SFAS 109", PANEL_B_YEARS),
}

# Models — paper runs 3 nested specs; given BETA/VOL unavailable, Model 3
# falls back to Model 2 (BETA/VOL are simply missing from the design).
MODELS: dict[str, dict] = {
    "1": {
        "name": "Model 1 — R_TAX+R_DEF+R_CFO only",
        "x_cols": ["r_tax", "r_def", "r_cfo"],
    },
    "2": {
        "name": "Model 2 — M1 + SIZE + B/P + E/P",
        "x_cols": ["r_tax", "r_def", "r_cfo", "ln_me_april", "b_to_p", "ep_pct"],
    },
    "3": {
        "name": "Model 3 — M2 + BETA + VOL (BETA/VOL unavailable)",
        "x_cols": ["r_tax", "r_def", "r_cfo", "ln_me_april", "b_to_p", "ep_pct"],
    },
}


# --------------------------------------------------------------------------
# Within-year winsorization (paper rule 24: 0.5%-99.5%) applied to the
# X variables only (rule 27: stock returns are NOT winsorized).
# --------------------------------------------------------------------------

WINSORIZE_LO = 0.005
WINSORIZE_HI = 0.995


def winsorize_within_year_x(
    df_year: pd.DataFrame, cols: Iterable[str]
) -> pd.DataFrame:
    """Winsorize X columns only (NOT the dependent variable)."""
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


def add_industry_dummies(
    df: pd.DataFrame, reference_industry: int | None = None
) -> tuple[pd.DataFrame, list[str]]:
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
) -> dict | None:
    """Run a single OLS for one (year, model) cell.

    The dependent variable (y_col) is NOT winsorized (rule 27).
    X columns are winsorized at [0.5%, 99.5%] within the year.
    """
    x_cols_present = [c for c in x_cols if c in df_year.columns]
    work = winsorize_within_year_x(df_year, x_cols_present)

    cols_needed = [y_col] + x_cols_present + ind_dummies
    sub = work.dropna(subset=cols_needed)
    n = len(sub)
    if n < len(x_cols_present) + len(ind_dummies) + 5:
        return None

    y = sub[y_col].astype(float).values
    X_parts: list[np.ndarray] = []
    for c in x_cols_present:
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

    fac_coefs = beta[: len(x_cols_present)]
    return {
        "betas": dict(zip(x_cols_present, [float(b) for b in fac_coefs])),
        "r2": float(r2),
        "n": int(n),
    }


# --------------------------------------------------------------------------
# Run one (panel, model) cell
# --------------------------------------------------------------------------

def run_cell(
    panel_df: pd.DataFrame,
    panel_letter: str,
    model_id: str,
    y_col: str = "cum_ret_may_april",
) -> dict:
    _, years = PANELS[panel_letter]
    x_cols = MODELS[model_id]["x_cols"]

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
            y_col=y_col,
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
            "y_col": y_col,
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
    std_betas = coef_df.std(ddof=1)
    t_stats = mean_betas / std_betas.replace(0, np.nan)
    mean_r2 = float(np.mean([r["r2"] for r in per_year]))
    mean_n = int(np.mean([r["n"] for r in per_year]))

    return {
        "panel": panel_letter,
        "model": model_id,
        "y_col": y_col,
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
# Run the full Table 5 grid
# --------------------------------------------------------------------------

def run_table5(panel_df: pd.DataFrame) -> dict:
    results: dict[str, dict[str, dict]] = {}
    for panel_letter in ("A", "B"):
        results[panel_letter] = {}
        for model_id in MODELS:
            results[panel_letter][model_id] = run_cell(
                panel_df, panel_letter, model_id
            )
    return results


# --------------------------------------------------------------------------
# Markdown / JSON output
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
    out: list[str] = []
    out.append("# Table 5 — Cross-Sectional Regressions of One-Year-Ahead Stock Returns")
    out.append("")
    out.append(
        "R = α_indu + β_1 SIZE + β_2 B/P + β_3 E/P + β_4 BETA + β_5 VOL + "
        "β_6 R_TAX + β_7 R_DEF + β_8 R_CFO + ε"
    )
    out.append("two-digit SIC industry fixed effects, annual cross-sections, "
               "time-series mean (t = mean / std across years).")
    out.append("")
    out.append(
        "Dependent variable: one-year buy-and-hold return from May of "
        "(t+1) to April of (t+2). Winsorization applied to X only "
        "(rule 27: stock returns not winsorized)."
    )
    out.append("")
    out.append(
        "Our sample period: fyear 1987-2000 (pre-1987 sparse per "
        "assumption #6). Panel A: 1987-1992 (paper: 1973-1992). "
        "Panel B: 1993-2000 (paper: 1993-2000)."
    )
    out.append("")
    out.append("**Assumption #9**: BETA, VOL are unavailable. Model 3 (M2 + "
               "BETA + VOL) falls back to M2. **Assumption #10**: Delisting "
               "reinvestment not implemented; uses raw cum_ret.")
    out.append("")
    out.append(
        "Each cell shows `mean(t-stat)`. R² and n are the time-series "
        "means of the per-year fit. Variables: β_1 = R_TAX, β_2 = R_DEF, "
        "β_3 = R_CFO, β_4 = SIZE (log April ME), β_5 = B/P, β_6 = E/P."
    )
    out.append("")

    for panel_letter in ("A", "B"):
        panel_name, years = PANELS[panel_letter]
        out.append(f"## Panel {panel_letter}: {panel_name} "
                   f"({min(years)}-{max(years)})")
        out.append("")
        header = (
            "| Model | "
            "β R_TAX | β R_DEF | β R_CFO | "
            "β SIZE | β B/P | β E/P | "
            "R² | n | # years used |"
        )
        sep = (
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
        )
        out.append(header)
        out.append(sep)
        for model_id in ("1", "2"):
            cell = results[panel_letter][model_id]
            mb = cell["mean_betas"]
            ts = cell["t_stats"]
            b_tax = _fmt(mb.get("r_tax"),    ts.get("r_tax"))
            b_def = _fmt(mb.get("r_def"),    ts.get("r_def"))
            b_cfo = _fmt(mb.get("r_cfo"),    ts.get("r_cfo"))
            b_size = _fmt(mb.get("ln_me_april"), ts.get("ln_me_april"))
            b_bp = _fmt(mb.get("b_to_p"),    ts.get("b_to_p"))
            b_ep = _fmt(mb.get("ep_pct"),    ts.get("ep_pct"))
            r2 = f"{cell['mean_r2']:.3f}" if not np.isnan(cell["mean_r2"]) else " - "
            n = cell["mean_n"]
            used = cell["n_periods_used"]
            m_short = {
                "1": "M1 (R_* only)",
                "2": "M2 (M1+SIZE+B/P+E/P)",
                "3": "M3 (M2+BETA+VOL)",
            }[model_id]
            out.append(
                f"| {m_short} | {b_tax} | {b_def} | {b_cfo} | "
                f"{b_size} | {b_bp} | {b_ep} | {r2} | {n:.0f} | {used} |"
            )
        out.append("")

    out.append("## Paper-vs-replication spot checks")
    out.append("")
    out.append("| Cell | Paper | Ours |")
    out.append("|---|---:|---:|")
    paper_spots = [
        ("T5_A R_TAX spec 1 β (mean)", "+0.013",
         lambda r: r["A"]["1"]["mean_betas"].get("r_tax"),
         "coef"),
        ("T5_A R_TAX spec 1 t-stat", "+3.913",
         lambda r: r["A"]["1"]["t_stats"].get("r_tax"),
         "coef"),
        ("T5_A R_TAX spec 2 β (mean)", "+0.014",
         lambda r: r["A"]["2"]["mean_betas"].get("r_tax"),
         "coef"),
        ("T5_A R_TAX spec 2 t-stat", "+3.851",
         lambda r: r["A"]["2"]["t_stats"].get("r_tax"),
         "coef"),
        ("T5_A mean n", "978",
         lambda r: r["A"]["2"]["mean_n"],
         "n"),
        ("T5_A R² spec 1", "0.155",
         lambda r: r["A"]["1"]["mean_r2"],
         "r2"),
        ("T5_B R_TAX spec 1 β (mean)", "+0.003",
         lambda r: r["B"]["1"]["mean_betas"].get("r_tax"),
         "coef"),
        ("T5_B R_TAX spec 1 t-stat", "+0.673",
         lambda r: r["B"]["1"]["t_stats"].get("r_tax"),
         "coef"),
        ("T5_B R_TAX spec 2 β (mean)", "+0.003",
         lambda r: r["B"]["2"]["mean_betas"].get("r_tax"),
         "coef"),
        ("T5_B R_TAX spec 2 t-stat", "+0.486",
         lambda r: r["B"]["2"]["t_stats"].get("r_tax"),
         "coef"),
        ("T5_B mean n", "1378",
         lambda r: r["B"]["2"]["mean_n"],
         "n"),
    ]
    for label, paper_val, getter, kind in paper_spots:
        v = getter(results)
        if v is None or (isinstance(v, float) and np.isnan(v)):
            ours_str = " - "
        elif kind == "n":
            ours_str = f"{int(v):,}"
        elif kind == "r2":
            ours_str = f"{v:.3f}"
        else:
            ours_str = f"{v:+.3f}"
        out.append(f"| {label} | {paper_val} | {ours_str} |")
    out.append("")
    return "\n".join(out)


def _strip_per_year(cell: dict) -> dict:
    return {k: v for k, v in cell.items() if k != "per_year"}


def save_results(results: dict) -> tuple[Path, Path]:
    LAYOUT.ensure()
    md_path = LAYOUT.result_path("table_5.md")
    md_path.write_text(render_markdown(results))

    cells_path = LAYOUT.result_path("table_5_cells.json")
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
                        "result": _strip_per_year(results[pl][mid]),
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
    panel_path = LAYOUT.data_path("panel_crsp.parquet")
    if not panel_path.exists():
        print(f"ERROR: {panel_path} does not exist. Run `python src/run_crsp_panel.py` first.")
        return 1

    print(f"[1/4] Loading CRSP-linked panel from {panel_path} ...")
    df = pd.read_parquet(panel_path)
    print(f"      rows: {len(df):,}, fyear: {df['fyear'].min()}-{df['fyear'].max()}, "
          f"unique (sich_2digit): {df['sich_2digit'].nunique()}")
    print(f"      n with cum_ret_may_april: {int(df['cum_ret_may_april'].notna().sum()):,}")

    print(f"\n[2/4] Running Table 5 cross-sectional regressions ...")
    print(f"      Models: {len(MODELS)}, Panels: 2 -> {len(MODELS) * 2} cells")
    results = run_table5(df)

    print(f"\n[3/4] Saving results ...")
    md_path, cells_path = save_results(results)
    print(f"      wrote {md_path}")
    print(f"      wrote {cells_path}")

    print(f"\n[4/4] Per-cell summary")
    print(_summary_table(results))

    print(f"\n[5/5] Paper spot checks (per task spec)")
    _print_paper_spots(results)
    return 0


def _summary_table(results: dict) -> str:
    lines: list[str] = []
    sep = "-" * 110
    lines.append(sep)
    lines.append(
        f"{'Panel':<7}{'Model':<32}{'β R_TAX':<14}{'t':<7}"
        f"{'β R_DEF':<14}{'t':<7}"
        f"{'β R_CFO':<14}{'t':<7}"
        f"{'R²':<7}{'n':<7}{'yrs':<5}"
    )
    lines.append(sep)
    for panel_letter in ("A", "B"):
        for model_id in ("1", "2"):
            cell = results[panel_letter][model_id]
            mb = cell["mean_betas"]
            ts = cell["t_stats"]

            def _b(b): return f"{b:+.3f}" if b is not None and not np.isnan(b) else "  -   "
            def _t(t): return f"{t:5.2f}" if t is not None and not np.isnan(t) else "  -  "

            lines.append(
                f"{panel_letter:<7}{MODELS[model_id]['name'][:30]:<32}"
                f"{_b(mb.get('r_tax')):<14}{_t(ts.get('r_tax')):<7}"
                f"{_b(mb.get('r_def')):<14}{_t(ts.get('r_def')):<7}"
                f"{_b(mb.get('r_cfo')):<14}{_t(ts.get('r_cfo')):<7}"
                f"{cell['mean_r2']:<7.3f}{cell['mean_n']:<7.0f}{cell['n_periods_used']:<5}"
            )
    lines.append(sep)
    return "\n".join(lines)


def _print_paper_spots(results: dict) -> None:
    paper_spots = [
        ("T5_A spec 1 R_TAX β",   "paper=+0.013",
         results["A"]["1"]["mean_betas"].get("r_tax"),
         results["A"]["1"]["t_stats"].get("r_tax"),
         +0.013),
        ("T5_A spec 2 R_TAX β",   "paper=+0.014",
         results["A"]["2"]["mean_betas"].get("r_tax"),
         results["A"]["2"]["t_stats"].get("r_tax"),
         +0.014),
        ("T5_B spec 1 R_TAX β",   "paper=+0.003",
         results["B"]["1"]["mean_betas"].get("r_tax"),
         results["B"]["1"]["t_stats"].get("r_tax"),
         +0.003),
        ("T5_B spec 2 R_TAX β",   "paper=+0.003",
         results["B"]["2"]["mean_betas"].get("r_tax"),
         results["B"]["2"]["t_stats"].get("r_tax"),
         +0.003),
    ]
    print(f"  {'Cell':<26}{'Paper':<14}{'Ours β':<12}{'Ours t':<10}{'Sign OK?'}")
    print("  " + "-" * 75)
    for label, paper_str, ours_b, ours_t, paper_v in paper_spots:
        if ours_b is None or (isinstance(ours_b, float) and np.isnan(ours_b)):
            ours_b_str = " - "
            ours_t_str = " - "
            sign_ok = " - "
        else:
            ours_b_str = f"{ours_b:+.3f}"
            ours_t_str = f"{ours_t:.2f}" if ours_t is not None and not np.isnan(ours_t) else " - "
            sign_ok = "yes" if (ours_b > 0) == (paper_v > 0) else "NO"
        print(f"  {label:<26}{paper_str:<14}{ours_b_str:<12}{ours_t_str:<10}{sign_ok}")


if __name__ == "__main__":
    raise SystemExit(main())