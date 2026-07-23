"""
Table 3 replication — Quality-sorted decile portfolios, US Long Sample
(Asness, Frazzini, Pedersen 2019, Panel A, 7/1957-12/2016).

Method (paper §5.1, rules sort_deciles / sort_weighting_vw):
  * each month, rank stocks into 10 quality deciles using NYSE
    breakpoints (hexcd_eom == 1), assign ALL stocks against them;
  * value-weighted (mcap) next-month excess returns per decile;
  * H-L = P10 (high quality) - P1 (low quality);
  * time-series regressions on FF CAPM / 3-factor / 4-factor models;
  * report excess returns, alphas (monthly %), CAPM beta, annualized
    Sharpe, annualized IR (4F alpha / 4F residual std), adj R2 (4F).

Outputs: results/table_3.md, results/decile_spread.png,
         results/decile_hl_cumulative.png

Usage: uv run python src/table3.py
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")

import numpy as np
import pandas as pd

from qmj_common import (
    LAYOUT, load_panel, load_ff, nyse_deciles, vw_returns,
    realized_month, portfolio_stats,
)
from utils.plot import plot_decile_spread, plot_cumulative_returns

# Paper values, Table 3 Panel A (monthly %, t-stats in parentheses)
PAPER = {
    "excess":  {"P1": 0.28, "P2": 0.43, "P3": 0.43, "P4": 0.51, "P5": 0.55,
                "P6": 0.53, "P7": 0.48, "P8": 0.62, "P9": 0.52, "P10": 0.70,
                "H-L": 0.42},
    "capm":    {"P1": -0.44, "P2": -0.17, "P3": -0.13, "P4": -0.02, "P5": 0.03,
                "P6": 0.03, "P7": -0.01, "P8": 0.12, "P9": 0.01, "P10": 0.20,
                "H-L": 0.64},
    "ff3":     {"P1": -0.57, "P2": -0.28, "P3": -0.21, "P4": -0.10, "P5": -0.03,
                "P6": -0.02, "P7": -0.02, "P8": 0.10, "P9": 0.05, "P10": 0.31,
                "H-L": 0.88},
    "ff4":     {"P1": -0.59, "P2": -0.39, "P3": -0.28, "P4": -0.19, "P5": -0.11,
                "P6": -0.12, "P7": -0.10, "P8": 0.11, "P9": 0.07, "P10": 0.46,
                "H-L": 1.05},
    "beta":    {"P1": 1.28, "P2": 1.16, "P3": 1.10, "P4": 1.06, "P5": 1.04,
                "P6": 1.00, "P7": 0.97, "P8": 0.97, "P9": 0.97, "P10": 0.92,
                "H-L": -0.36},
    "sharpe":  {"P1": 0.14, "P2": 0.27, "P3": 0.30, "P4": 0.37, "P5": 0.41,
                "P6": 0.41, "P7": 0.38, "P8": 0.48, "P9": 0.40, "P10": 0.53,
                "H-L": 0.33},
    "ir":      {"P1": -0.88, "P2": -0.83, "P3": -0.64, "P4": -0.50, "P5": -0.27,
                "P6": -0.34, "P7": -0.25, "P8": 0.29, "P9": 0.22, "P10": 1.20,
                "H-L": 1.31},
    "adj_r2":  {"P1": 0.88, "P2": 0.91, "P3": 0.92, "P4": 0.90, "P5": 0.92,
                "P6": 0.91, "P7": 0.91, "P8": 0.93, "P9": 0.91, "P10": 0.59,
                "H-L": 0.59},
}


def build_decile_returns(panel: pd.DataFrame) -> pd.DataFrame:
    """Monthly VW (+EW) returns for the 10 NYSE-breakpoint quality
    deciles, indexed by REALIZATION month (t+1)."""
    work = panel[panel["quality"].notna()].copy()
    work["decile"] = nyse_deciles(work, "quality", n_bins=10)
    work = work.dropna(subset=["decile"])
    work["decile"] = work["decile"].astype(int)
    br = vw_returns(work, "decile")
    br["month"] = realized_month(br["month"])
    n_assigned = work.groupby("month")["decile"].size()
    print(f"[table3] stock-months sorted: {len(work):,} "
          f"(avg {n_assigned.mean():.0f}/month), "
          f"months: {br['month'].nunique()}")
    return br


def fmt_cell(val: float, t: float | None = None) -> str:
    if t is None:
        return f"{val:.2f}"
    return f"{val:.2f} ({t:.2f})"


def render_markdown(stats: dict[str, dict], nobs0: int) -> str:
    cols = [f"P{i}" for i in range(1, 11)] + ["H-L"]
    rows = [
        ("Excess return", "excess_pct", "excess_t_iid", 100.0),
        ("CAPM alpha", "capm_alpha_pct", "capm_alpha_t", 100.0),
        ("3-factor alpha", "ff3_alpha_pct", "ff3_alpha_t", 100.0),
        ("4-factor alpha", "ff4_alpha_pct", "ff4_alpha_t", 100.0),
    ]
    lines = []
    lines.append("# Table 3 — Quality-sorted portfolios (Panel A: US Long Sample, 7/1957–12/2016)")
    lines.append("")
    lines.append("Replication of Asness, Frazzini, Pedersen (2019). Value-weighted, "
                 "NYSE-breakpoint quality deciles; next-month excess returns over T-bills. "
                 f"N = {nobs0} months. Returns/alphas in monthly %. "
                 "Excess-return t-stats are iid; alpha t-stats are Newey-West (60 lags). "
                 "Beta = CAPM market loading; IR = annualized 4-factor alpha / 4-factor "
                 "residual std; Adjusted R2 from the 4-factor regression.")
    lines.append("")
    header = "| | " + " | ".join(cols) + " |"
    sep = "|" + "---|" * (len(cols) + 1)
    lines += [header, sep]
    for label, key, tkey, _ in rows:
        cells = []
        for c in cols:
            s = stats[c]
            cells.append(fmt_cell(s[key], s[tkey]))
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    for label, key in [("Beta", "beta"), ("Sharpe Ratio", "sharpe"),
                       ("Information Ratio", "ir"), ("Adjusted R2", "adj_r2")]:
        cells = [fmt_cell(stats[c][key]) for c in cols]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")

    # comparison with the paper
    lines += ["", "## Comparison with paper (replicated vs paper)", ""]
    lines += [header, sep]
    keymap = [("Excess return", "excess_pct", "excess"),
              ("CAPM alpha", "capm_alpha_pct", "capm"),
              ("3-factor alpha", "ff3_alpha_pct", "ff3"),
              ("4-factor alpha", "ff4_alpha_pct", "ff4"),
              ("Beta", "beta", "beta"),
              ("Sharpe Ratio", "sharpe", "sharpe"),
              ("Information Ratio", "ir", "ir"),
              ("Adjusted R2", "adj_r2", "adj_r2")]
    for label, key, pkey in keymap:
        cells = [f"{stats[c][key]:.2f} / {PAPER[pkey][c]:.2f}" for c in cols]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    LAYOUT.ensure()
    panel = load_panel()
    ff = load_ff()
    print(f"[table3] panel: {len(panel):,} rows, "
          f"{panel['month'].nunique()} formation months; "
          f"ff: {len(ff)} months ({ff.index.min().date()}..{ff.index.max().date()})")

    br = build_decile_returns(panel)
    wide_vw = br.pivot(index="month", columns="decile", values="VW").sort_index()
    wide_ew = br.pivot(index="month", columns="decile", values="EW").sort_index()

    stats: dict[str, dict] = {}
    for d in range(1, 11):
        stats[f"P{d}"] = portfolio_stats(wide_vw[d], ff)
    hl = (wide_vw[10] - wide_vw[1]).dropna()
    stats["H-L"] = portfolio_stats(hl, ff)

    nobs0 = stats["P1"]["nobs"]
    print(f"[table3] regression N = {nobs0} months "
          f"({wide_vw.index.min().date()} .. {wide_vw.index.max().date()})")
    print("\n[table3] key results (monthly %):")
    print(f"  excess:  P1={stats['P1']['excess_pct']:.2f} "
          f"P10={stats['P10']['excess_pct']:.2f} H-L={stats['H-L']['excess_pct']:.2f}")
    print(f"  4F alpha: P1={stats['P1']['ff4_alpha_pct']:.2f} "
          f"P10={stats['P10']['ff4_alpha_pct']:.2f} H-L={stats['H-L']['ff4_alpha_pct']:.2f}")
    print(f"  beta:    P1={stats['P1']['beta']:.2f} "
          f"P10={stats['P10']['beta']:.2f} H-L={stats['H-L']['beta']:.2f}")

    # --- outputs ---
    md = render_markdown(stats, nobs0)
    out_md = LAYOUT.result_path("table_3.md")
    out_md.write_text(md)
    print(f"[save] {out_md}")

    # bar chart: mean decile returns (EW + VW), monthly %
    per_bin = pd.DataFrame({
        "bin": [f"P{d}" for d in range(1, 11)],
        "EW": [wide_ew[d].mean() * 100 for d in range(1, 11)],
        "VW": [wide_vw[d].mean() * 100 for d in range(1, 11)],
    })
    plot_decile_spread(per_bin, bin_col="bin",
                       save_to=LAYOUT.result_path("decile_spread.png"))
    print(f"[save] {LAYOUT.result_path('decile_spread.png')}")

    # cumulative H-L spread (VW)
    hl_df = hl.rename("HL_VW").reset_index()
    plot_cumulative_returns(hl_df, index_col_name="month",
                            ret_col_lst=["HL_VW"],
                            title="Quality decile spread P10–P1 (VW, cumulative)",
                            save_to=LAYOUT.result_path("decile_hl_cumulative.png"))
    print(f"[save] {LAYOUT.result_path('decile_hl_cumulative.png')}")


if __name__ == "__main__":
    main()
