"""table_4.py — Bi-dimensional quintile 36-month buy-and-hold returns.

Replication of Frankel & Lee (1998) Table 4:
  - Panel A: V_f/P quintile x ME (in-sample) quintile -> mean Ret36
  - Panel B: V_f/P quintile x B/P quintile -> mean Ret36

For each portfolio-formation year t in 1977-1992, independently assign
quintiles Q1..Q5 by V_f/P, by ME (in-sample), and by B/P. For each
(V_f/P q, ME q) cell (Panel A) and (V_f/P q, B/P q) cell (Panel B)
compute the equally-weighted mean of Ret36 across all firm-years in
that cell. Aggregate across years by simple mean of annual cell means.

Output: a 5x5 grid per panel with marginal Q5-Q1 spreads reported as:
  - Row "Marginal V_f/P (Q5-Q1)": average Ret36 at V_f/P=Q5 minus V_f/P=Q1,
    averaging across the 5 ME/B/P rows (= V_f/P effect controlling for ME/BP).
  - Column "Marginal ME/BP (Q5-Q1)": average Ret36 at ME/BP=Q5 minus
    ME/BP=Q1, averaging across the 5 V_f/P rows (= ME/BP effect
    controlling for V_f/P).
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd

TABLE_4_YEAR_START = 1977
TABLE_4_YEAR_END = 1992


def _assign_quintiles(values: np.ndarray) -> np.ndarray:
    """Assign 1..5 quintiles to a 1D array using in-sample breakpoints.
    Returns an int array (1..5)."""
    valid = ~np.isnan(values)
    out = np.full(len(values), np.nan)
    if valid.sum() < 5:
        return out
    edges = np.quantile(values[valid], np.linspace(0, 1, 6))
    edges[0] -= 1e-9
    edges[-1] += 1e-9
    out[valid] = np.digitize(values[valid], edges[1:-1], right=False) + 1
    out[valid] = np.clip(out[valid], 1, 5)
    return out


def _cell_mean(df_year: pd.DataFrame, col_row: str, col_col: str,
               val_col: str) -> np.ndarray:
    """Return 5x5 matrix of mean(val_col) indexed by (row_q, col_q).
    Missing cells = NaN."""
    mat = np.full((5, 5), np.nan)
    for r in range(1, 6):
        for c in range(1, 6):
            sub = df_year[(df_year[col_row] == r) & (df_year[col_col] == c)]
            if len(sub) >= 3:
                mat[r - 1, c - 1] = sub[val_col].mean()
    return mat


def compute_table_4(panel_with_v: pd.DataFrame, bhar: pd.DataFrame) -> dict:
    """Compute Panel A and Panel B 5x5 grids of mean Ret36.

    Returns:
        {
          'panel_a': {'annual': [matrices], 'mean': 5x5 matrix, 'years': [years]},
          'panel_b': {...}
        }
    """
    df = panel_with_v.copy()
    df = df.merge(
        bhar[["permno", "year_t", "ret36"]],
        on=["permno", "year_t"], how="left",
    )
    df["b_per_share"] = df["ceq"] / df["csho"]
    df["b_over_p"] = df["b_per_share"] / df["prc"]
    df = df[(df["year_t"] >= TABLE_4_YEAR_START) &
            (df["year_t"] <= TABLE_4_YEAR_END)].copy()
    df = df.dropna(subset=["v_f_p_t3", "me_june_t", "b_over_p", "ret36"])

    annual_a = []
    annual_b = []
    years = []
    for year_t, g in df.groupby("year_t"):
        if len(g) < 25:
            continue
        g = g.copy()
        g["vf_q"] = _assign_quintiles(g["v_f_p_t3"].values)
        g["me_q"] = _assign_quintiles(g["me_june_t"].values)
        g["bp_q"] = _assign_quintiles(g["b_over_p"].values)
        mat_a = _cell_mean(g, "vf_q", "me_q", "ret36")
        mat_b = _cell_mean(g, "vf_q", "bp_q", "ret36")
        annual_a.append(mat_a)
        annual_b.append(mat_b)
        years.append(int(year_t))

    mean_a = np.nanmean(np.stack(annual_a, axis=0), axis=0) if annual_a else np.full((5, 5), np.nan)
    mean_b = np.nanmean(np.stack(annual_b, axis=0), axis=0) if annual_b else np.full((5, 5), np.nan)

    return {
        "panel_a": {"annual": annual_a, "mean": mean_a, "years": years},
        "panel_b": {"annual": annual_b, "mean": mean_b, "years": years},
    }


def _format_grid(label_rows: str, label_cols: str, mat: np.ndarray,
                 row_labels: list[str], col_labels: list[str]) -> list[str]:
    """Render a 5x5 grid as a markdown table with row labels and
    column labels. Returns lines (without trailing newline).

    Cells are Ret36 means (3 decimals). Empty cells if NaN.

    Also adds two marginal rows:
      - "Marginal {label_rows} (Q5-Q1)": per-column Q5-Q1 spread
      - "Marginal {label_cols} (Q5-Q1)": per-row Q5-Q1 spread
    """
    lines = []
    header = ["Quintile (cell)"] + col_labels + ["Marginal Q5-Q1"]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "|".join(["---"] * len(header)) + "|")
    for r in range(5):
        row = [row_labels[r]]
        for c in range(5):
            v = mat[r, c]
            row.append(f"{v:.3f}" if not np.isnan(v) else "")
        # Row marginal: Q5 - Q1 (across columns)
        if not (np.isnan(mat[r, 4]) or np.isnan(mat[r, 0])):
            row.append(f"{mat[r, 4] - mat[r, 0]:+.3f}")
        else:
            row.append("")
        lines.append("| " + " | ".join(row) + " |")
    # Marginal row label (across rows): for each column, Q5 - Q1
    marginal_row = [f"Marginal {label_cols} (Q5-Q1)"]
    for c in range(5):
        if not (np.isnan(mat[4, c]) or np.isnan(mat[0, c])):
            marginal_row.append(f"{mat[4, c] - mat[0, c]:+.3f}")
        else:
            marginal_row.append("")
    marginal_row.append("--")
    lines.append("| " + " | ".join(marginal_row) + " |")
    return lines


def render_table_4_md(t4: dict) -> str:
    """Render Table 4 as Markdown."""
    rows_pa = t4["panel_a"]
    rows_pb = t4["panel_b"]
    years_a = rows_pa["years"]
    years_b = rows_pb["years"]
    n_years_a = len(years_a)
    n_years_b = len(years_b)
    mean_a = rows_pa["mean"]
    mean_b = rows_pb["mean"]

    vfp_labels = ["V_f/P Q1", "V_f/P Q2", "V_f/P Q3", "V_f/P Q4", "V_f/P Q5"]
    me_labels = ["ME Q1", "ME Q2", "ME Q3", "ME Q4", "ME Q5"]
    bp_labels = ["B/P Q1", "B/P Q2", "B/P Q3", "B/P Q4", "B/P Q5"]

    lines = []
    lines.append("# Table 4 -- Bi-Dimensional Quintile 36-Month Buy-and-Hold Returns")
    lines.append("")
    lines.append("**Replication of**: Frankel & Lee (1998) -- Table 4")
    lines.append("")
    lines.append("**Sample period**: 1977-1992 (paper's Table 4 caption)")
    lines.append("**Universe**: same as Table 3 (Compustat non-financial, fiscal year-end in [6,12], June price >= $1, I/B/E/S FY1 coverage)")
    lines.append("")
    lines.append("Each firm-year is independently assigned to a quintile by V_f/P (rows) and by ME or B/P (columns) within each portfolio-formation year. Cells show the equally-weighted mean of 36-month buy-and-hold returns (Ret36) starting July of year t. The marginal rows/columns show the Q5-Q1 spread holding the other dimension fixed.")
    lines.append("")
    lines.append("**Marginal Q5-Q1 interpretation**:")
    lines.append("- The rightmost-column marginal (per row) shows the average Ret36 spread from V_f/P Q5 minus V_f/P Q1, holding the row's ME (Panel A) or B/P (Panel B) quintile fixed -- i.e., the **V_f/P effect controlling for ME/BP**.")
    lines.append("- The bottom-row marginal (per column) shows the average Ret36 spread from ME/BP Q5 minus ME/BP Q1, holding the column's V_f/P quintile fixed -- i.e., the **ME/BP effect controlling for V_f/P**.")
    lines.append("")
    lines.append(f"**Number of years averaged**: Panel A = {n_years_a}, Panel B = {n_years_b}.")
    lines.append("")

    # ---- Panel A ----
    lines.append("## Panel A -- V_f/P x ME (in-sample size quintiles)")
    lines.append("")
    lines.append(f"Years averaged: {', '.join(str(y) for y in years_a)}")
    lines.append("")
    lines.append("|  | ME Q1 | ME Q2 | ME Q3 | ME Q4 | ME Q5 | Marginal Q5-Q1 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for r in range(5):
        row = [vfp_labels[r]]
        for c in range(5):
            v = mean_a[r, c]
            row.append(f"{v:.3f}" if not np.isnan(v) else "")
        if not (np.isnan(mean_a[r, 4]) or np.isnan(mean_a[r, 0])):
            row.append(f"{mean_a[r, 4] - mean_a[r, 0]:+.3f}")
        else:
            row.append("")
        lines.append("| " + " | ".join(row) + " |")
    marginal_row = ["**Marginal ME (Q5-Q1)**"]
    for c in range(5):
        if not (np.isnan(mean_a[4, c]) or np.isnan(mean_a[0, c])):
            marginal_row.append(f"**{mean_a[4, c] - mean_a[0, c]:+.3f}**")
        else:
            marginal_row.append("")
    marginal_row.append("--")
    lines.append("| " + " | ".join(marginal_row) + " |")
    lines.append("")

    # ---- Panel B ----
    lines.append("## Panel B -- V_f/P x B/P")
    lines.append("")
    lines.append(f"Years averaged: {', '.join(str(y) for y in years_b)}")
    lines.append("")
    lines.append("|  | B/P Q1 | B/P Q2 | B/P Q3 | B/P Q4 | B/P Q5 | Marginal Q5-Q1 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for r in range(5):
        row = [vfp_labels[r]]
        for c in range(5):
            v = mean_b[r, c]
            row.append(f"{v:.3f}" if not np.isnan(v) else "")
        if not (np.isnan(mean_b[r, 4]) or np.isnan(mean_b[0, 0])):
            # Need to recompute - actually the row marginal is Q5-Q1 of v_f/P
            pass
        if not (np.isnan(mean_b[r, 4]) or np.isnan(mean_b[r, 0])):
            row.append(f"{mean_b[r, 4] - mean_b[r, 0]:+.3f}")
        else:
            row.append("")
        lines.append("| " + " | ".join(row) + " |")
    marginal_row = ["**Marginal B/P (Q5-Q1)**"]
    for c in range(5):
        if not (np.isnan(mean_b[4, c]) or np.isnan(mean_b[0, c])):
            marginal_row.append(f"**{mean_b[4, c] - mean_b[0, c]:+.3f}**")
        else:
            marginal_row.append("")
    marginal_row.append("--")
    lines.append("| " + " | ".join(marginal_row) + " |")
    lines.append("")

    # ---- Per-cell comparison block (paper vs ours) ----
    paper_a = {
        ("Q1size", "Q1VfP"): 0.319, ("Q1size", "Q5VfP"): 0.590,
        ("Q1size", "Q5Q1"): 0.271,
        ("Q5size", "Q1VfP"): 0.350, ("Q5size", "Q5VfP"): 0.679,
        ("Q5size", "Q5Q1"): 0.329,
    }
    paper_b = {
        ("Q1BP", "Q1VfP"): 0.316, ("Q1BP", "Q5VfP"): 0.634,
        ("Q1BP", "Q5Q1"): 0.318,
        ("Q5BP", "Q1VfP"): 0.263, ("Q5BP", "Q5VfP"): 0.732,
        ("Q5BP", "Q5Q1"): 0.469,
    }
    lines.append("## Per-cell comparison vs paper (committed cells)")
    lines.append("")
    lines.append("Paper's Panel A Q1size_Q1VfP, Q1size_Q5VfP, Q1size_Q5Q1 correspond to ME=Q1 row, V_f/P=Q1 / V_f/P=Q5 / Q5-Q1 columns. The Q5size row is ME=Q5.")
    lines.append("Paper's Panel B Q1BP / Q5BP rows correspond to B/P=Q1 / B/P=Q5 rows.")
    lines.append("")
    lines.append("| Panel | Cell | Paper | Ours | Status |")
    lines.append("| --- | --- | ---: | ---: | --- |")
    # Panel A: ME Q1 row (row index 0 of mean_a) and ME Q5 row (row index 4)
    cells_a = [
        ("A", "A_Q1size_Q1VfP_Ret36", mean_a[0, 0], paper_a[("Q1size", "Q1VfP")], 0.30),
        ("A", "A_Q1size_Q5VfP_Ret36", mean_a[4, 0], paper_a[("Q1size", "Q5VfP")], 0.30),
        ("A", "A_Q1size_Q5Q1_Ret36", mean_a[4, 0] - mean_a[0, 0], paper_a[("Q1size", "Q5Q1")], 0.30),
        ("A", "A_Q5size_Q1VfP_Ret36", mean_a[0, 4], paper_a[("Q5size", "Q1VfP")], 0.30),
        ("A", "A_Q5size_Q5VfP_Ret36", mean_a[4, 4], paper_a[("Q5size", "Q5VfP")], 0.30),
        ("A", "A_Q5size_Q5Q1_Ret36", mean_a[4, 4] - mean_a[0, 4], paper_a[("Q5size", "Q5Q1")], 0.30),
        ("B", "B_Q1BP_Q1VfP_Ret36", mean_b[0, 0], paper_b[("Q1BP", "Q1VfP")], 0.30),
        ("B", "B_Q1BP_Q5VfP_Ret36", mean_b[4, 0], paper_b[("Q1BP", "Q5VfP")], 0.30),
        ("B", "B_Q1BP_Q5Q1_Ret36", mean_b[4, 0] - mean_b[0, 0], paper_b[("Q1BP", "Q5Q1")], 0.30),
        ("B", "B_Q5BP_Q1VfP_Ret36", mean_b[0, 4], paper_b[("Q5BP", "Q1VfP")], 0.30),
        ("B", "B_Q5BP_Q5VfP_Ret36", mean_b[4, 4], paper_b[("Q5BP", "Q5VfP")], 0.30),
        ("B", "B_Q5BP_Q5Q1_Ret36", mean_b[4, 4] - mean_b[0, 4], paper_b[("Q5BP", "Q5Q1")], 0.30),
    ]
    for panel, name, ours_v, paper_v, tol in cells_a:
        if np.isnan(ours_v):
            status = "NaN"
        else:
            d = ours_v - paper_v
            if abs(d) <= tol * abs(paper_v):
                status = f"Tier 1 (Δ={d:+.3f})"
            elif abs(d) <= 2 * tol * abs(paper_v):
                status = f"Tier 2 (Δ={d:+.3f})"
            else:
                status = f"FAIL (Δ={d:+.3f})"
        ours_s = f"{ours_v:+.3f}" if not np.isnan(ours_v) else "NaN"
        lines.append(f"| {panel} | {name} | {paper_v:+.3f} | {ours_s} | {status} |")
    lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("**Aggregation**: each cell is the simple mean (across years) of the annual cell mean. We do not weight by cell-N to avoid over-weighting years with sparse coverage; the paper's exact aggregation is not documented but is consistent with simple means. Sign-conventions are preserved: Q5 > Q1 rows indicate positive V_f/P effect.")
    lines.append("")
    lines.append("**V_f/P effect**: row marginal (right column) is the Q5-Q1 spread of V_f/P holding the column dimension (ME or B/P) fixed. The paper expects this spread to be positive in every row of both panels (i.e., high V_f/P firms earn higher 36-month returns even within size or B/P quintiles).")
    lines.append("")

    return "\n".join(lines)


def extract_table_4_metrics(t4: dict) -> dict[str, float]:
    """Extract Table 4 metric values keyed by metric name."""
    mean_a = t4["panel_a"]["mean"]
    mean_b = t4["panel_b"]["mean"]
    metrics: dict[str, float] = {}
    cells = [
        ("A_Q1size_Q1VfP_Ret36", mean_a[0, 0]),
        ("A_Q1size_Q5VfP_Ret36", mean_a[4, 0]),
        ("A_Q1size_Q5Q1_Ret36", mean_a[4, 0] - mean_a[0, 0]),
        ("A_Q5size_Q1VfP_Ret36", mean_a[0, 4]),
        ("A_Q5size_Q5VfP_Ret36", mean_a[4, 4]),
        ("A_Q5size_Q5Q1_Ret36", mean_a[4, 4] - mean_a[0, 4]),
        ("B_Q1BP_Q1VfP_Ret36", mean_b[0, 0]),
        ("B_Q1BP_Q5VfP_Ret36", mean_b[4, 0]),
        ("B_Q1BP_Q5Q1_Ret36", mean_b[4, 0] - mean_b[0, 0]),
        ("B_Q5BP_Q1VfP_Ret36", mean_b[0, 4]),
        ("B_Q5BP_Q5VfP_Ret36", mean_b[4, 4]),
        ("B_Q5BP_Q5Q1_Ret36", mean_b[4, 4] - mean_b[0, 4]),
    ]
    for name, v in cells:
        if not np.isnan(v):
            metrics[name] = float(v)
    return metrics
