"""
Table 4 replication — Quality minus junk: returns (Panel A: US Long
Sample, 7/1957-12/2016; Asness, Frazzini, Pedersen 2019).

Method (paper §5.2, rules sort_qmj_construction / sort_qmj_top_bottom_30 /
sort_qmj_formula):
  * each month, two size groups with breakpoint = median NYSE market
    equity; conditional sort: within each size group, quality deciles
    from the NYSE stocks of that group (fallback: in-group breakpoints
    if < 20 NYSE names);
  * Quality = deciles 8-10 (top 30%), Junk = deciles 1-3 (bottom 30%),
    value-weighted;
  * QMJ = 1/2 (Small Quality + Big Quality) - 1/2 (Small Junk + Big Junk);
  * sub-component factors (Profitability-MJ, Safety-MJ, Growth-MJ) built
    identically on the profitability / safety / growth scores;
  * time-series regressions on CAPM / FF3 / FF4; report excess returns,
    alphas (monthly %), 4-factor loadings, Sharpe, IR, adj R2.

Outputs: results/table_4.md, results/qmj_cumulative.png

Usage: uv run python src/table4.py
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")

import pandas as pd

from qmj_common import (
    LAYOUT, load_panel, load_ff, qmj_factor, portfolio_stats,
)
from utils.plot import plot_cumulative_returns

SIGNALS = [("QMJ", "quality"), ("Profitability", "profitability"),
           ("Safety", "safety"), ("Growth", "growth")]

# Paper values, Table 4 Panel A (monthly %, t-stats in parentheses)
PAPER = {
    "QMJ": {"excess": 0.29, "capm": 0.39, "ff3": 0.51, "ff4": 0.60,
            "mkt": -0.20, "smb": -0.26, "hml": -0.37, "umd": -0.09,
            "sharpe": 0.47, "ir": 1.40, "adj_r2": 0.50},
    "Profitability": {"excess": 0.25, "capm": 0.32, "ff3": 0.40, "ff4": 0.50,
                      "mkt": -0.12, "smb": -0.22, "hml": -0.29, "umd": -0.10,
                      "sharpe": 0.48, "ir": 1.17, "adj_r2": 0.34},
    "Safety": {"excess": 0.23, "capm": 0.40, "ff3": 0.52, "ff4": 0.51,
               "mkt": -0.32, "smb": -0.30, "hml": -0.28, "umd": 0.01,
               "sharpe": 0.32, "ir": 1.18, "adj_r2": 0.62},
    "Growth": {"excess": 0.17, "capm": 0.16, "ff3": 0.28, "ff4": 0.46,
               "mkt": -0.04, "smb": -0.04, "hml": -0.49, "umd": -0.16,
               "sharpe": 0.32, "ir": 1.16, "adj_r2": 0.46},
}


def render_markdown(results: dict[str, dict]) -> str:
    cols = [name for name, _ in SIGNALS]
    lines = []
    lines.append("# Table 4 — Quality minus junk: returns (Panel A: US Long Sample, 7/1957–12/2016)")
    lines.append("")
    lines.append("Replication of Asness, Frazzini, Pedersen (2019). QMJ = 1/2(Small Quality + "
                 "Big Quality) − 1/2(Small Junk + Big Junk); size split at median NYSE market "
                 "equity; conditional quality deciles within each size group, top 30% (deciles "
                 "8–10) = Quality, bottom 30% (deciles 1–3) = Junk; value-weighted. Sub-component "
                 "factors sort on profitability / safety / growth scores. Returns/alphas in "
                 "monthly %; excess-return t-stats iid, alpha/loading t-stats Newey-West (60 lags). "
                 "IR = annualized 4-factor alpha / 4-factor residual std.")
    lines.append("")
    header = "| | " + " | ".join(cols) + " |"
    sep = "|" + "---|" * (len(cols) + 1)
    lines += [header, sep]

    def row(label, valfn, tfn=None):
        cells = []
        for c in cols:
            r = results[c]
            cells.append(f"{valfn(r):.2f} ({tfn(r):.2f})" if tfn
                         else f"{valfn(r):.2f}")
        lines.append(f"| {label} | " + " | ".join(cells) + " |")

    row("Excess Returns", lambda r: r["excess_pct"], lambda r: r["excess_t_iid"])
    row("CAPM-alpha", lambda r: r["capm_alpha_pct"], lambda r: r["capm_alpha_t"])
    row("3-factor alpha", lambda r: r["ff3_alpha_pct"], lambda r: r["ff3_alpha_t"])
    row("4-factor alpha", lambda r: r["ff4_alpha_pct"], lambda r: r["ff4_alpha_t"])
    row("MKT", lambda r: r["loadings"]["mkt_rf"], lambda r: r["loading_t"]["mkt_rf"])
    row("SMB", lambda r: r["loadings"]["smb"], lambda r: r["loading_t"]["smb"])
    row("HML", lambda r: r["loadings"]["hml"], lambda r: r["loading_t"]["hml"])
    row("UMD", lambda r: r["loadings"]["mom"], lambda r: r["loading_t"]["mom"])
    row("Sharpe Ratio", lambda r: r["sharpe"])
    row("Information Ratio", lambda r: r["ir"])
    row("Adjusted R2", lambda r: r["adj_r2"])

    # comparison with the paper
    lines += ["", "## Comparison with paper (replicated / paper)", ""]
    lines += [header, sep]
    comp = [("Excess Returns", "excess_pct", "excess"),
            ("CAPM-alpha", "capm_alpha_pct", "capm"),
            ("3-factor alpha", "ff3_alpha_pct", "ff3"),
            ("4-factor alpha", "ff4_alpha_pct", "ff4"),
            ("MKT", None, "mkt"), ("SMB", None, "smb"),
            ("HML", None, "hml"), ("UMD", None, "umd"),
            ("Sharpe Ratio", "sharpe", "sharpe"),
            ("Information Ratio", "ir", "ir"),
            ("Adjusted R2", "adj_r2", "adj_r2")]
    loadkey = {"mkt": "mkt_rf", "smb": "smb", "hml": "hml", "umd": "mom"}
    for label, key, pkey in comp:
        cells = []
        for c in cols:
            if key:
                rep = results[c][key]
            else:
                rep = results[c]["loadings"][loadkey[pkey]]
            cells.append(f"{rep:.2f} / {PAPER[c][pkey]:.2f}")
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    LAYOUT.ensure()
    panel = load_panel()
    ff = load_ff()
    print(f"[table4] panel: {len(panel):,} rows, "
          f"{panel['month'].nunique()} formation months; ff: {len(ff)} months")

    results: dict[str, dict] = {}
    series: dict[str, pd.Series] = {}
    for name, sig in SIGNALS:
        f = qmj_factor(panel, sig)
        series[name] = f
        results[name] = portfolio_stats(f, ff)
        r = results[name]
        print(f"[table4] {name:<14} n={r['nobs']} excess={r['excess_pct']:.2f}% "
              f"CAPM={r['capm_alpha_pct']:.2f} 3F={r['ff3_alpha_pct']:.2f} "
              f"4F={r['ff4_alpha_pct']:.2f} Sharpe={r['sharpe']:.2f} IR={r['ir']:.2f}")

    md = render_markdown(results)
    out_md = LAYOUT.result_path("table_4.md")
    out_md.write_text(md)
    print(f"[save] {out_md}")

    # cumulative QMJ: raw excess + 4-factor-adjusted (alpha + residual,
    # as in the paper's Fig. 2)
    qmj = series["QMJ"].rename("QMJ_raw_excess")
    r4 = results["QMJ"]
    adj = (r4["ff4_resid"] + r4["ff4_alpha_dec"]).rename("QMJ_4F_adjusted")
    df_plot = pd.concat([qmj, adj], axis=1).reset_index()
    plot_cumulative_returns(df_plot, index_col_name="month",
                            ret_col_lst=["QMJ_raw_excess", "QMJ_4F_adjusted"],
                            title="QMJ factor, US Long Sample (cumulative, monthly decimals)",
                            save_to=LAYOUT.result_path("qmj_cumulative.png"))
    print(f"[save] {LAYOUT.result_path('qmj_cumulative.png')}")


if __name__ == "__main__":
    main()
