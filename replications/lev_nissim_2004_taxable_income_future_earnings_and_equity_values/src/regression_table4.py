"""
Replication of Lev & Nissim (2004) Table 4 — Cross-sectional
regressions of E/P* on tax/cash flow fundamentals + control
variables (Eq. 5).

  E/P* = α_indu + β_1 GROW + β_2 LNTA + β_3 BETA + β_4 VOL +
         β_5 LEV + β_6 PAY + β_7 R_TAX + β_8 R_DEF + β_9 R_CFO + ε

The paper reports 4 nested specifications per panel:
  Model 1: E/P* = α + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO                 (no controls)
  Model 2: E/P* = α + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO + β_4 GROW       (add GROW)
  Model 3: E/P* = α + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO + β_4 LNTA + β_5 LEV + β_6 PAY (add size, leverage, payout)
  Model 4: full set with GROW + LNTA + LEV + PAY + BETA + VOL

Industry FE on two-digit SIC.

Panels: A = pre-SFAS (paper: 1973-1992; ours: 1987-1992 because of
the pre-1987 data gap), B = post-SFAS (1993-2000).

Inputs:
  data/panel_crsp.parquet   — CRSP-linked panel from src/run_crsp_panel.py
                              (or src/sql/crsp_panel.sql directly)

Outputs:
  results/table_4.md
  results/table_4_cells.json

Per-iteration caveats (assumption #9): BETA, VOL, GROW are not
implemented in this iteration — the E/P regression uses LNTA, LEV,
PAY controls only. Documented in assumptions.md.
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
# Panel definitions — split at the SFAS No 109 effective year.
# Paper: Panel A = 1973-1992 (pre-SFAS 109); Panel B = 1993-2000 (post).
# Ours: Panel A = 1987-1992 (data gap per assumption #6); Panel B = 1993-2000.
# --------------------------------------------------------------------------

PANEL_A_YEARS = range(1987, 1993)
PANEL_B_YEARS = range(1993, 2001)

PANELS: dict[str, tuple[str, range]] = {
    "A": ("Pre-SFAS 109", PANEL_A_YEARS),
    "B": ("Post-SFAS 109", PANEL_B_YEARS),
}

# The paper runs 4 model specifications per panel. We replicate 3 nested
# ones (1, 3, 4) given that BETA/VOL/GROW are unavailable (assumption #9).
# `controls` lists the control x-vectors; the 3 R_* fundamentals are
# always present.
MODELS: dict[str, dict] = {
    "1": {
        "name": "Model 1 — R_TAX+R_DEF+R_CFO only (no controls)",
        "x_cols": ["r_tax", "r_def", "r_cfo"],
    },
    "2": {
        "name": "Model 2 — M1 + GROW (skipped; GROW unavailable)",
        "x_cols": ["r_tax", "r_def", "r_cfo"],
    },
    "3": {
        "name": "Model 3 — M1 + LNTA + LEV + PAY (size, leverage, payout)",
        "x_cols": ["r_tax", "r_def", "r_cfo", "ln_me_fye", "lev", "pay"],
    },
    "4": {
        "name": "Model 4 — M3 + BETA + VOL (BETA/VOL unavailable)",
        "x_cols": ["r_tax", "r_def", "r_cfo", "ln_me_fye", "lev", "pay"],
    },
}


# --------------------------------------------------------------------------
# Within-year winsorization (paper rule 24: 0.5%-99.5% per sample).
# Year-by-year application (paper applies to full sample) avoids future
# data leakage.
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

    Returns a dict with betas, R², n. Returns None if the design
    matrix is too thin or rank-deficient.
    """
    cols_to_wins = [y_col] + [c for c in x_cols if c in df_year.columns]
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

    fac_coefs = beta[: len(x_cols)]
    return {
        "betas": dict(zip(x_cols, [float(b) for b in fac_coefs])),
        "r2": float(r2),
        "n": int(n),
    }


# --------------------------------------------------------------------------
# Run one (panel, model) cell — annual fits + time-series average.
# --------------------------------------------------------------------------

def run_cell(
    panel_df: pd.DataFrame,
    panel_letter: str,
    model_id: str,
    y_col: str = "epstar_pct",
) -> dict:
    """Run one (panel, model) cell of Table 4.

    Returns a dict with per-year list and time-series mean/std/t-stat.
    """
    _, years = PANELS[panel_letter]
    x_cols = MODELS[model_id]["x_cols"]

    # Build industry dummies once per panel; keep reference stable.
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
# Run the full Table 4 grid
# --------------------------------------------------------------------------

def run_table4(panel_df: pd.DataFrame) -> dict:
    """Run Table 4: 4 models × 2 panels = 8 cells (we report 4: 1, 3, 4 in each panel)."""
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
    """Render Table 4 in markdown."""
    out: list[str] = []
    out.append("# Table 4 — Cross-Sectional Regressions of E/P*")
    out.append("")
    out.append(
        "E/P* = α_indu + β_1 GROW + β_2 LNTA + β_3 BETA + β_4 VOL + "
        "β_5 LEV + β_6 PAY + β_7 R_TAX + β_8 R_DEF + β_9 R_CFO + ε"
    )
    out.append("two-digit SIC industry fixed effects, annual cross-sections, "
               "time-series mean (t = mean / std across years).")
    out.append("")
    out.append(
        "Our sample period: fyear 1987-2000 (pre-1987 sparse per "
       "assumption #6). Panel A: 1987-1992 (paper: 1973-1992). "
       "Panel B: 1993-2000 (paper: 1993-2000)."
    )
    out.append("")
    out.append("**Assumption #9**: BETA, VOL, GROW are unavailable in this "
               "iteration. Model 2 (M1 + GROW) and Model 4 (M3 + BETA + VOL) "
               "are skipped or fall back to M1 / M3. See assumptions.md.")
    out.append("")
    out.append(
        "Each cell shows `mean(t-stat)`. R² and n are the time-series means "
        "of the per-year fit. Variables: β_1 = R_TAX, β_2 = R_DEF, β_3 = R_CFO, "
        "β_4 = LNTA (ln ME at FYE), β_5 = LEV, β_6 = PAY."
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
            "β LNTA | β LEV | β PAY | "
            "R² | n | # years used |"
        )
        sep = (
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
        )
        out.append(header)
        out.append(sep)
        for model_id in ("1", "3"):
            cell = results[panel_letter][model_id]
            mb = cell["mean_betas"]
            ts = cell["t_stats"]
            b_tax = _fmt(mb.get("r_tax"),    ts.get("r_tax"))
            b_def = _fmt(mb.get("r_def"),    ts.get("r_def"))
            b_cfo = _fmt(mb.get("r_cfo"),    ts.get("r_cfo"))
            b_lnta = _fmt(mb.get("ln_me_fye"), ts.get("ln_me_fye"))
            b_lev = _fmt(mb.get("lev"),      ts.get("lev"))
            b_pay = _fmt(mb.get("pay"),      ts.get("pay"))
            r2 = f"{cell['mean_r2']:.3f}" if not np.isnan(cell["mean_r2"]) else " - "
            n = cell["mean_n"]
            used = cell["n_periods_used"]
            m_short = {
                "1": "M1 (R_* only)",
                "2": "M2 (M1+GROW)",
                "3": "M3 (M1+LNTA+LEV+PAY)",
                "4": "M4 (M3+BETA+VOL)",
            }[model_id]
            out.append(
                f"| {m_short} | {b_tax} | {b_def} | {b_cfo} | "
                f"{b_lnta} | {b_lev} | {b_pay} | {r2} | {n:.0f} | {used} |"
            )
        out.append("")

    # Paper comparison spot checks
    out.append("## Paper-vs-replication spot checks")
    out.append("")
    out.append("| Cell | Paper | Ours |")
    out.append("|---|---:|---:|")
    paper_spots = [
        ("T4_A R_TAX spec 1 β (mean)", "-0.083",
         lambda r: r["A"]["1"]["mean_betas"].get("r_tax"),
         "coef"),
        ("T4_A R_TAX spec 1 t-stat", "-1.364",
         lambda r: r["A"]["1"]["t_stats"].get("r_tax"),
         "coef"),
        ("T4_A R_TAX spec 3 β (mean)", "-0.063",
         lambda r: r["A"]["3"]["mean_betas"].get("r_tax"),
         "coef"),
        ("T4_A R_TAX spec 3 t-stat", "-0.814",
         lambda r: r["A"]["3"]["t_stats"].get("r_tax"),
         "coef"),
        ("T4_A mean n", "535",
         lambda r: r["A"]["3"]["mean_n"],
         "n"),
        ("T4_B R_TAX spec 1 β (mean)", "-0.288",
         lambda r: r["B"]["1"]["mean_betas"].get("r_tax"),
         "coef"),
        ("T4_B R_TAX spec 1 t-stat", "-11.349",
         lambda r: r["B"]["1"]["t_stats"].get("r_tax"),
         "coef"),
        ("T4_B R_TAX spec 3 β (mean)", "-0.212",
         lambda r: r["B"]["3"]["mean_betas"].get("r_tax"),
         "coef"),
        ("T4_B R_TAX spec 3 t-stat", "-8.483",
         lambda r: r["B"]["3"]["t_stats"].get("r_tax"),
         "coef"),
        ("T4_B mean n", "911",
         lambda r: r["B"]["3"]["mean_n"],
         "n"),
    ]
    for label, paper_val, getter, kind in paper_spots:
        v = getter(results)
        if v is None or (isinstance(v, float) and np.isnan(v)):
            ours_str = " - "
        elif kind == "n":
            ours_str = f"{int(v):,}"
        else:
            ours_str = f"{v:+.3f}"
        out.append(f"| {label} | {paper_val} | {ours_str} |")
    out.append("")
    return "\n".join(out)


def _strip_per_year(cell: dict) -> dict:
    return {k: v for k, v in cell.items() if k != "per_year"}


def save_results(results: dict) -> tuple[Path, Path]:
    LAYOUT.ensure()
    md_path = LAYOUT.result_path("table_4.md")
    md_path.write_text(render_markdown(results))

    cells_path = LAYOUT.result_path("table_4_cells.json")
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

    print(f"\n[2/4] Running Table 4 cross-sectional regressions ...")
    print(f"      Models: {len(MODELS)}, Panels: 2 -> {len(MODELS) * 2} cells")
    results = run_table4(df)

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
        for model_id in ("1", "3"):
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
        ("T4_A spec 1 R_TAX β",   "paper=-0.083",
         results["A"]["1"]["mean_betas"].get("r_tax"),
         results["A"]["1"]["t_stats"].get("r_tax"),
         -0.083),
        ("T4_A spec 3 R_TAX β",   "paper=-0.063",
         results["A"]["3"]["mean_betas"].get("r_tax"),
         results["A"]["3"]["t_stats"].get("r_tax"),
         -0.063),
        ("T4_B spec 1 R_TAX β",   "paper=-0.288",
         results["B"]["1"]["mean_betas"].get("r_tax"),
         results["B"]["1"]["t_stats"].get("r_tax"),
         -0.288),
        ("T4_B spec 3 R_TAX β",   "paper=-0.212",
         results["B"]["3"]["mean_betas"].get("r_tax"),
         results["B"]["3"]["t_stats"].get("r_tax"),
         -0.212),
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