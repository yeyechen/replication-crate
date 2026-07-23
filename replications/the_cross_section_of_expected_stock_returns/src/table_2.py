"""
Replication of Fama & French (1992) "The Cross-Section of Expected Stock Returns"
=================================================================================
Stage: Table II — properties of the 12 one-dimensional portfolios formed each
June on SIZE alone (Panel A) or on pre-ranking BETA alone (Panel B),
July 1963 - December 1990 (330 months; 28 formation years 1963-1990).

Columns (12 portfolios): 1A, 1B, 2, 3, 4, 5, 6, 7, 8, 9, 10A, 10B
    (2-9 are deciles; 1A/1B split the bottom decile, 10A/10B the top decile).
Rows: Return, beta, ln(ME), ln(BE/ME), ln(A/ME), ln(A/BE), E/P dummy,
      E(+)/P, Firms.

Inputs (built by src/main.py — NO ClickHouse re-query; analysis only):
  data/panel.parquet  one row per (permno, return-month) with columns
                      ret, post_beta, lnME, ln_bm, ln_ame, ln_abe, ep_pos,
                      ep_dummy, size12, beta12, month, ...

Aggregation conventions (paper Table II notes, L815/L817/L819), implemented
exactly as specified:
  * Return: monthly EW return = mean of VALID stock returns in the portfolio
    that month (stock-level, from the panel; NaN rets skipped); table value =
    time-series average over the 330 months x 100.
  * beta: per month, mean of the stock-level post_beta (the full-period
    post-ranking beta of each stock's size x pre-beta cell, assigned each
    June) over portfolio members; table value = time-series mean of those
    monthly means.
  * ln(ME), ln(BE/ME), ln(A/ME), ln(A/BE), E/P dummy, E(+)/P: per month, mean
    of the stock-level firm-year value over the members present that month;
    table value = time-series mean over the 330 months. (Variables are
    constant within a firm-year; monthly membership varies as stocks delist
    mid-year.)
  * Firms: average number of assigned members per month = mean over months of
    the count of panel rows per (month, portfolio) — counts members REGARDLESS
    of return validity.

Identity check: mean ln(A/ME) - mean ln(A/BE) == mean ln(BE/ME) per portfolio
(holds to machine precision — logged, not enforced).

Targets / tolerances come from preparations/tables_to_replicate.json
(table_2): Return 25%, beta 15%, ln-ratios 10%, E/P rows 30%, Firms 20%.
No-target cells (computed, shown, but not scored):
  * Panel A E(+)/P — row missing from the paper OCR.
  * Panel B Return — only 1A (1.20) and 10B (1.18) are prose-anchored; the
    interior cells lost one OCR cell, so they carry no target.

Outputs:
  results/table_2.md   both panels (2-decimal rounding; Firms integer) plus a
                       cell-by-cell comparison block per panel (ours vs paper,
                       |Δ|, tolerance, pass) and an overall summary.

Usage:
    uv run python replications/the_cross_section_of_expected_stock_returns/src/table_2.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

# --- path bootstrap: runnable from any CWD -------------------------------
SRC_DIR = Path(__file__).resolve().parent
REPO_ROOT = SRC_DIR.parents[2]
os.environ.setdefault("REPLICATIONS_PATH", str(REPO_ROOT / "replications"))
for _p in (str(SRC_DIR), str(REPO_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np
import pandas as pd

from main import LAYOUT  # noqa: E402  (resolved paper layout)

N_MONTHS = 330                         # July 1963 - December 1990
COLS = ["1A", "1B", "2", "3", "4", "5", "6", "7", "8", "9", "10A", "10B"]

# (display row, panel column to average, scale).  Firms is handled separately
# (row COUNT per month, not a mean of a stock-level column).
ROWS = [
    ("Return",    "ret",       100.0),
    ("β",         "post_beta", 1.0),
    ("ln(ME)",    "lnME",      1.0),
    ("ln(BE/ME)", "ln_bm",     1.0),
    ("ln(A/ME)",  "ln_ame",    1.0),
    ("ln(A/BE)",  "ln_abe",    1.0),
    ("E/P dummy", "ep_dummy",  1.0),
    ("E(+)/P",    "ep_pos",    1.0),
    ("Firms",     None,        None),
]
ROW_ORDER = [r[0] for r in ROWS]

# metric-row label in tables_to_replicate.json  ->  display row
METRIC_ROW_TO_DISPLAY = {
    "Return":    "Return",
    "beta":      "β",
    "ln(ME)":    "ln(ME)",
    "ln(BE/ME)": "ln(BE/ME)",
    "ln(A/ME)":  "ln(A/ME)",
    "ln(A/BE)":  "ln(A/BE)",
    "E/P dummy": "E/P dummy",
    "E(+)/P":    "E(+)/P",
    "Firms":     "Firms",
}

PANEL_COL = {"A": "size12", "B": "beta12"}     # grouping column per panel
PANEL_TITLE = {"A": "Panel A — portfolios formed on SIZE (ME)",
               "B": "Panel B — portfolios formed on pre-ranking β"}


# ────────────────────────────────────────────────────────────────────────────
# Computation
# ────────────────────────────────────────────────────────────────────────────
def compute_panel(panel: pd.DataFrame, portcol: str) -> dict[str, dict[str, float]]:
    """{display_row: {portfolio: full-precision value}} for one panel.

    Each statistic is a time-series mean (over months) of the monthly
    cross-sectional mean over the portfolio's members that month.  Firms is the
    time-series mean of the monthly member COUNT (rows per (month, portfolio),
    regardless of return validity)."""
    out: dict[str, dict[str, float]] = {}
    for disp, colname, scale in ROWS:
        if disp == "Firms":
            monthly = panel.groupby([portcol, "month"]).size()
        else:
            # .mean() skips NaN -> only valid members contribute each month
            monthly = panel.groupby([portcol, "month"])[colname].mean() * scale
        ts = monthly.groupby(level=0).mean()
        out[disp] = {c: float(ts.get(c, np.nan)) for c in COLS}
    return out


# ────────────────────────────────────────────────────────────────────────────
# Paper targets + tolerances (from preparations/tables_to_replicate.json)
# ────────────────────────────────────────────────────────────────────────────
def load_paper() -> dict[tuple, tuple[float, float]]:
    """{(panel, display_row, col): (paper_value, tolerance_pct)}."""
    spec = json.loads(LAYOUT.preparations_path("tables_to_replicate.json").read_text())
    t2 = next(t for t in spec["tables"] if t["id"] == "table_2")
    paper: dict[tuple, tuple[float, float]] = {}
    rx = re.compile(r"T2([AB])\s+(?:size|beta)-sorted\s+(.*?)\s+\[([^\]]+)\]")
    for m in t2["metrics"]:
        mm = rx.match(m["name"])
        if not mm:
            continue
        pan, mrow, col = mm.group(1), mm.group(2), mm.group(3)
        paper[(pan, METRIC_ROW_TO_DISPLAY[mrow], col)] = (
            float(m["value"]), float(m["tolerance_pct"]),
        )
    return paper


def evaluate(ours_by_panel: dict, paper: dict) -> pd.DataFrame:
    """One row per (panel, row, col): ours, paper, dev, tol, target?, pass?."""
    rows = []
    for pan in "AB":
        for disp in ROW_ORDER:
            for c in COLS:
                ours = ours_by_panel[pan][disp][c]
                tgt = paper.get((pan, disp, c))
                if tgt is None:                       # no paper target
                    rows.append(dict(panel=pan, row=disp, col=c, paper=np.nan,
                                     ours=ours, dev=np.nan, tol_pct=np.nan,
                                     target=False, passed=None))
                else:
                    pv, tol = tgt
                    dev = ours - pv
                    ok = abs(dev) <= (tol / 100.0) * abs(pv)
                    rows.append(dict(panel=pan, row=disp, col=c, paper=pv,
                                     ours=ours, dev=dev, tol_pct=tol,
                                     target=True, passed=bool(ok)))
    return pd.DataFrame(rows)


# ────────────────────────────────────────────────────────────────────────────
# Rendering helpers
# ────────────────────────────────────────────────────────────────────────────
def fmt_ours(disp: str, v: float) -> str:
    return f"{v:.0f}" if disp == "Firms" else f"{v:.2f}"


def fmt_paper(disp: str, v: float) -> str:
    return f"{v:.0f}" if disp == "Firms" else f"{v:.2f}"


def fmt_dev(disp: str, d: float) -> str:
    return f"{abs(d):.1f}" if disp == "Firms" else f"{abs(d):.3f}"


def render_main(vals: dict[str, dict[str, float]]) -> str:
    """The replicated 9x12 table (ours). 2-decimal rounding; Firms integer."""
    head = "| Portfolio | " + " | ".join(COLS) + " |"
    sep = "|" + "---|" + "---:|" * len(COLS)
    lines = [head, sep]
    for disp in ROW_ORDER:
        cells = [fmt_ours(disp, vals[disp][c]) for c in COLS]
        lines.append("| " + disp + " | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def render_comparison(ev: pd.DataFrame, pan: str) -> str:
    """Cell-by-cell comparison block for one panel (long form)."""
    sub = ev[ev["panel"] == pan].copy()
    sub["rowk"] = sub["row"].map({r: i for i, r in enumerate(ROW_ORDER)})
    sub["colk"] = sub["col"].map({c: i for i, c in enumerate(COLS)})
    sub = sub.sort_values(["rowk", "colk"])

    lines = [
        "| Row | Port | Paper | Ours | \\|Δ\\| | Tol | Result |",
        "|---|---|---:|---:|---:|---:|:---:|",
    ]
    for _, r in sub.iterrows():
        disp = r["row"]
        if not r["target"]:
            lines.append(
                f"| {disp} | {r['col']} | — | {fmt_ours(disp, r['ours'])} | "
                f"— | — | no target |"
            )
        else:
            mark = "✅" if r["passed"] else "❌"
            res = "pass" if r["passed"] else "FAIL"
            lines.append(
                f"| {disp} | {r['col']} | {fmt_paper(disp, r['paper'])} | "
                f"{fmt_ours(disp, r['ours'])} | {fmt_dev(disp, r['dev'])} | "
                f"{int(r['tol_pct'])}% | {mark} {res} |"
            )
    return "\n".join(lines)


def panel_summary_line(ev: pd.DataFrame, pan: str) -> str:
    sub = ev[(ev["panel"] == pan) & (ev["target"])]
    n_pass = int(sub["passed"].sum())
    n_tot = len(sub)
    no_target = int((~ev[ev["panel"] == pan]["target"]).sum())
    # largest |deviation| among targeted cells (relative, for the callout)
    sub = sub.assign(reldev=sub["dev"].abs() / sub["paper"].abs())
    big = sub.sort_values("reldev", ascending=False).head(3)
    bl = "; ".join(
        f"{r['row']} {r['col']}: ours {fmt_ours(r['row'], r['ours'])} vs "
        f"paper {fmt_paper(r['row'], r['paper'])} "
        f"(|Δ| {fmt_dev(r['row'], r['dev'])}, {r['reldev']*100:.1f}%)"
        for _, r in big.iterrows()
    )
    return (
        f"**Pass/fail: {n_pass}/{n_tot} targeted cells pass** "
        f"(+ {no_target} no-target cells shown but not scored).  "
        f"Largest relative deviations: {bl}."
    )


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    t0 = time.time()
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    n_months = panel["month"].nunique()

    # ── compute both panels ──────────────────────────────────────────────
    ours = {pan: compute_panel(panel, PANEL_COL[pan]) for pan in "AB"}
    paper = load_paper()
    ev = evaluate(ours, paper)

    # identity check: mean ln(A/ME) - mean ln(A/BE) == mean ln(BE/ME)
    id_max = 0.0
    for pan in "AB":
        for c in COLS:
            lhs = ours[pan]["ln(A/ME)"][c] - ours[pan]["ln(A/BE)"][c]
            id_max = max(id_max, abs(lhs - ours[pan]["ln(BE/ME)"][c]))

    # ── markdown ─────────────────────────────────────────────────────────
    md = []
    md.append("# Table II — Fama & French (1992), The Cross-Section of Expected Stock Returns")
    md.append("")
    md.append(
        "Properties of the 12 one-dimensional portfolios formed at the end of "
        "June each year on **size (ME)** (Panel A) or **pre-ranking β** "
        "(Panel B). Columns 2–9 are deciles of the ranking variable; 1A/1B "
        "split the bottom decile and 10A/10B split the top decile. NYSE "
        "breakpoints; equal-weighted; sample July 1963 – December 1990 "
        f"({n_months} months; 28 formation years, 1963–1990)."
    )
    md.append("")
    md.append(
        "**Averaging conventions (paper notes L815/L817/L819).** *Return*: "
        "time-series average (over the 330 months) of the monthly "
        "equal-weighted portfolio return ×100 (monthly EW = mean of valid "
        "stock returns in the portfolio that month). *β*: mean of the "
        "stock-level post-ranking βs (each stock carries the full-period "
        "post-ranking β of its size×pre-β cell, assigned each June) over "
        "members each month, then time-series mean. *ln(ME), ln(BE/ME), "
        "ln(A/ME), ln(A/BE), E/P dummy, E(+)/P*: mean of the stock-level "
        "firm-year value over the members present each month, then "
        "time-series mean over the 330 months. *Firms*: mean over months of "
        "the number of assigned members per month (panel rows per "
        "(month, portfolio), counted regardless of return validity)."
    )
    md.append("")

    for pan in "AB":
        md.append(f"## {PANEL_TITLE[pan]}")
        md.append("")
        md.append("### Replicated values")
        md.append("")
        md.append(render_main(ours[pan]))
        md.append("")
        md.append("### Comparison with paper")
        md.append("")
        md.append(panel_summary_line(ev, pan))
        md.append("")
        if pan == "A":
            md.append(
                "> **No target:** the E(+)/P row is missing from the paper OCR "
                "for Panel A — our values are shown but not scored."
            )
            md.append("")
        else:
            md.append(
                "> **No target:** for Panel B Return only 1A (1.20) and 10B "
                "(1.18) are prose-anchored; the interior Return cells lost one "
                "OCR cell and carry no target (computed and shown, not scored)."
            )
            md.append("")
        md.append(render_comparison(ev, pan))
        md.append("")

    # ── overall summary ──────────────────────────────────────────────────
    tgt = ev[ev["target"]].copy()
    tgt["passed"] = tgt["passed"].astype(bool)   # object->bool (safe ~ below)
    n_pass = int(tgt["passed"].sum())
    n_tot = len(tgt)
    md.append("## Overall summary")
    md.append("")
    md.append(f"- **Targeted cells: {n_pass}/{n_tot} pass** "
              f"(tolerances: Return 25%, β 15%, ln-ratios 10%, E/P rows 30%, "
              f"Firms 20%; from preparations/tables_to_replicate.json).")
    by_pan = tgt.groupby("panel")["passed"].agg(["sum", "count"])
    for pan in "AB":
        c = by_pan.loc[pan]
        md.append(f"  - Panel {pan}: {int(c['sum'])}/{int(c['count'])} pass.")
    n_notarget = int((~ev["target"]).sum())
    md.append(f"- No-target cells (shown, not scored): {n_notarget} "
              f"(Panel A E(+)/P ×12; Panel B interior Return ×10).")
    fails = tgt[~tgt["passed"]]
    if len(fails):
        md.append(f"- **Failing cells ({len(fails)}):**")
        for _, r in fails.iterrows():
            rel = abs(r["dev"]) / abs(r["paper"]) * 100
            md.append(
                f"  - Panel {r['panel']} {r['row']} {r['col']}: "
                f"ours {fmt_ours(r['row'], r['ours'])} vs paper "
                f"{fmt_paper(r['row'], r['paper'])} (|Δ| {fmt_dev(r['row'], r['dev'])}, "
                f"{rel:.1f}% > {int(r['tol_pct'])}%)."
            )
    else:
        md.append("- **No failing cells.**")
    md.append(f"- Identity check ln(A/ME)−ln(A/BE)=ln(BE/ME): max discrepancy "
              f"{id_max:.2e} across all 24 portfolio cells.")
    md.append(f"- Months covered: {n_months} (paper = 330).")
    md.append("")
    md.append("---")
    md.append(
        "*Computed by src/table_2.py from data/panel.parquet (iteration-1 "
        "pipeline). All statistics are time-series means of monthly "
        "cross-sectional portfolio means; Firms is the mean monthly member "
        "count. No-target cells reflect OCR gaps noted in "
        "preparations/tables_to_replicate.json.*"
    )

    out = LAYOUT.result_path("table_2.md")
    out.write_text("\n".join(md))
    print(f"wrote {out}")

    # ── console report ───────────────────────────────────────────────────
    print(f"\nmonths: {n_months} (paper: 330)")
    for pan in "AB":
        print(f"\n===== {PANEL_TITLE[pan]} =====")
        print(render_main(ours[pan]))
        print(panel_summary_line(ev, pan))
    print(f"\nidentity ln(A/ME)-ln(A/BE)=ln(BE/ME) max discrepancy: {id_max:.2e}")
    print(f"\nOVERALL: {n_pass}/{n_tot} targeted cells pass "
          f"(Panel A {int(by_pan.loc['A','sum'])}/{int(by_pan.loc['A','count'])}, "
          f"Panel B {int(by_pan.loc['B','sum'])}/{int(by_pan.loc['B','count'])})")
    print(f"no-target cells: {n_notarget}")
    if len(fails):
        print(f"FAILING CELLS ({len(fails)}):")
        for _, r in fails.iterrows():
            rel = abs(r["dev"]) / abs(r["paper"]) * 100
            print(f"  Panel {r['panel']} {r['row']} {r['col']}: "
                  f"ours {r['ours']:.3f} vs paper {r['paper']:.3f} "
                  f"(|Δ| {abs(r['dev']):.3f}, {rel:.1f}% > {int(r['tol_pct'])}%)")
    else:
        print("no failing cells")
    # top 5 relative deviations overall (targeted)
    top = tgt.assign(rel=tgt["dev"].abs() / tgt["paper"].abs()).sort_values(
        "rel", ascending=False).head(5)
    print("largest relative deviations (targeted):")
    for _, r in top.iterrows():
        print(f"  Panel {r['panel']} {r['row']} {r['col']}: "
              f"ours {r['ours']:.3f} vs paper {r['paper']:.3f} "
              f"(|Δ| {abs(r['dev']):.3f}, {r['rel']*100:.1f}%)")
    print(f"\ntotal time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
