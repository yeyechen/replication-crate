"""
Replication of Fama & French (1992) "The Cross-Section of Expected Stock Returns"
=================================================================================
Stage: Table I — average monthly returns (Panel A), post-ranking betas
(Panel B) and average size ln(ME) (Panel C) for the 100 portfolios formed on
size (rows, decile 1 = Small-ME .. decile 10 = Large-ME) then pre-ranking
beta (columns, group 1 = Low-beta .. group 10 = High-beta), July 1963 -
December 1990 (330 months; 28 formation years 1963-1990).

Inputs (built by src/main.py, inner iteration 1 — NO ClickHouse re-query
except the market index):
  data/panel.parquet              one row per permno x return-month
  data/portfolio_returns.parquet  100 size x beta cells x 330 monthly EW rets
  src/sql/market_index_monthly.sql -> msi.vwretd (market proxy for betas)

Method (exactly as specified):
  Panel A — time-series average of monthly EW portfolio returns x 100.
    * 100 cells: mean of each cell's 330 monthly EW returns
      (data/portfolio_returns.parquet).
    * "All" COLUMN (size-decile portfolios), "All" ROW (beta-group
      portfolios), All/All (grand portfolio): STOCK-level EW from the panel
      (mean ret per month over the pooled stocks, then time-series average)
      — NOT averages of the 10 cell returns (cells have different stock
      counts).
  Panel B — full-sample (330-month) Dimson sum-betas (slopes on current +
    1-lagged msi.vwretd, helper grouped_dimson_beta from src/main.py) of the
    SAME EW series. The 100 cell betas are cross-checked against the panel's
    post_beta column (one value per cell).
  Panel C — time-series average of the June-formation cross-sectional means
    of lnME (panel deduplicated to firm-years; 28 formation years).

Outputs:
  results/table_1.md                 three 11x11 matrices + paper comparison
  data/agg_portfolio_returns.parquet 10 size-decile + 10 beta-group + grand
                                     EW monthly series (330 obs each;
                                     columns series, ym, month, n_stocks,
                                     ret), reused by Tables II/VI

Usage:
    uv run python replications/the_cross_section_of_expected_stock_returns/src/table_1.py
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

# reuse the iteration-1 helpers (Dimson beta, month-key lag, SQL loader,
# resolved layout) rather than re-implementing them
from main import grouped_dimson_beta, ym_prev, q_file, LAYOUT  # noqa: E402

FIRST_T, LAST_T = 1963, 1990          # formation years (28)
N_MONTHS = 330                        # July 1963 - December 1990

# 11x11 layout: rows = size, columns = pre-ranking beta
ROW_LABELS = ["All", "Small-ME"] + [f"ME-{d}" for d in range(2, 10)] + ["Large-ME"]
COL_LABELS = ["All", "Low-β"] + [f"β-{b}" for b in range(2, 10)] + ["High-β"]

# tolerances for the pass/fail evaluation (preparations/tables_to_replicate.json)
TOL = {"A": 0.25, "B": 0.15, "C": 0.10}

# paper values for the comparison section (task spec / inputs/content.md).
# Keyed (panel, row-label, col-label).
PAPER = {
    # Panel A — All column (size deciles, %/mo)
    ("A", "All", "All"): 1.25,
    ("A", "Small-ME", "All"): 1.52, ("A", "ME-2", "All"): 1.29,
    ("A", "ME-3", "All"): 1.24, ("A", "ME-4", "All"): 1.25,
    ("A", "ME-5", "All"): 1.29, ("A", "ME-6", "All"): 1.17,
    ("A", "ME-7", "All"): 1.07, ("A", "ME-8", "All"): 1.10,
    ("A", "ME-9", "All"): 0.95, ("A", "Large-ME", "All"): 0.89,
    # Panel A — All row (beta groups)
    ("A", "All", "Low-β"): 1.34, ("A", "All", "β-2"): 1.29,
    ("A", "All", "β-3"): 1.36, ("A", "All", "β-4"): 1.31,
    ("A", "All", "β-5"): 1.33, ("A", "All", "β-6"): 1.28,
    ("A", "All", "β-7"): 1.24, ("A", "All", "β-8"): 1.21,
    ("A", "All", "β-9"): 1.25, ("A", "All", "High-β"): 1.14,
    # Panel A — corners
    ("A", "Small-ME", "Low-β"): 1.71, ("A", "Small-ME", "High-β"): 1.42,
    ("A", "Large-ME", "High-β"): 0.56,
    # Panel B — All column
    ("B", "Small-ME", "All"): 1.44, ("B", "ME-2", "All"): 1.39,
    ("B", "ME-3", "All"): 1.35, ("B", "ME-4", "All"): 1.34,
    ("B", "ME-5", "All"): 1.25, ("B", "ME-6", "All"): 1.23,
    ("B", "ME-7", "All"): 1.17, ("B", "ME-8", "All"): 1.09,
    ("B", "ME-9", "All"): 1.03, ("B", "Large-ME", "All"): 0.92,
    # Panel B — corners
    ("B", "Small-ME", "Low-β"): 1.05, ("B", "Small-ME", "High-β"): 1.79,
    ("B", "Large-ME", "Low-β"): 0.57, ("B", "Large-ME", "High-β"): 1.32,
    ("B", "ME-8", "Low-β"): 0.53,   # paper's overall minimum
    # Panel C — All column
    ("C", "Small-ME", "All"): 2.24, ("C", "ME-2", "All"): 3.63,
    ("C", "ME-3", "All"): 4.10, ("C", "ME-4", "All"): 4.50,
    ("C", "ME-5", "All"): 4.89, ("C", "ME-6", "All"): 5.30,
    ("C", "ME-7", "All"): 5.73, ("C", "ME-8", "All"): 6.24,
    ("C", "ME-9", "All"): 6.82, ("C", "Large-ME", "All"): 7.93,
    # Panel C — All row
    ("C", "All", "All"): 4.11,
    ("C", "All", "Low-β"): 3.86, ("C", "All", "β-2"): 4.26,
    ("C", "All", "β-3"): 4.33, ("C", "All", "β-4"): 4.41,
    ("C", "All", "β-5"): 4.27, ("C", "All", "β-6"): 4.32,
    ("C", "All", "β-7"): 4.26, ("C", "All", "β-8"): 4.19,
    ("C", "All", "β-9"): 4.03, ("C", "All", "High-β"): 3.77,
    # Panel C — corners
    ("C", "Small-ME", "Low-β"): 2.12, ("C", "Large-ME", "Low-β"): 7.94,
    ("C", "Large-ME", "High-β"): 7.62,
}


# ────────────────────────────────────────────────────────────────────────────
# Label <-> key maps ('all' or int 1..10)
# ────────────────────────────────────────────────────────────────────────────
def row_key(label: str):
    if label == "All":
        return "all"
    if label == "Small-ME":
        return 1
    if label == "Large-ME":
        return 10
    return int(label.removeprefix("ME-"))


def col_key(label: str):
    if label == "All":
        return "all"
    if label == "Low-β":
        return 1
    if label == "High-β":
        return 10
    return int(label.removeprefix("β-"))


ROW_KEY = {lab: row_key(lab) for lab in ROW_LABELS}
COL_KEY = {lab: col_key(lab) for lab in COL_LABELS}


# ────────────────────────────────────────────────────────────────────────────
# Aggregated EW series (stock level) — size deciles, beta groups, grand
# ────────────────────────────────────────────────────────────────────────────
def build_agg_series(panel: pd.DataFrame) -> pd.DataFrame:
    """Monthly EW returns of the 10 size-decile portfolios, the 10 beta-group
    portfolios and the grand portfolio, computed at STOCK level from the panel
    (mean ret per month over the pooled stocks; NaN rets skipped, exactly as
    in src/main.py's per-cell EW computation). 330 obs per series."""
    p = panel[["month", "size_decile", "beta_group", "ret"]].copy()
    p["ym"] = p["month"].dt.year * 100 + p["month"].dt.month

    size_g = (
        p.groupby(["size_decile", "ym", "month"])
        .agg(ret=("ret", "mean"), n_stocks=("ret", "count"))
        .reset_index()
    )
    size_g["series"] = "size_" + size_g["size_decile"].astype(int).astype(str)

    beta_g = (
        p.groupby(["beta_group", "ym", "month"])
        .agg(ret=("ret", "mean"), n_stocks=("ret", "count"))
        .reset_index()
    )
    beta_g["series"] = "beta_" + beta_g["beta_group"].astype(int).astype(str)

    grand_g = (
        p.groupby(["ym", "month"])
        .agg(ret=("ret", "mean"), n_stocks=("ret", "count"))
        .reset_index()
    )
    grand_g["series"] = "grand"

    cols = ["series", "ym", "month", "n_stocks", "ret"]
    out = (
        pd.concat([size_g[cols], beta_g[cols], grand_g[cols]], ignore_index=True)
        .sort_values(["series", "ym"])
        .reset_index(drop=True)
    )
    out["ym"] = out["ym"].astype(np.int64)
    return out


# ────────────────────────────────────────────────────────────────────────────
# Dimson sum-betas (current + 1-lagged msi.vwretd) of EW return series
# ────────────────────────────────────────────────────────────────────────────
def market_with_lag(mkt: pd.DataFrame) -> pd.DataFrame:
    m = mkt.copy()
    m["ym"] = pd.to_numeric(m["ym"], errors="coerce").astype(np.int64)
    m["vwretd"] = pd.to_numeric(m["vwretd"], errors="coerce")
    m = m.dropna(subset=["vwretd"]).sort_values("ym")
    vmap = dict(zip(m["ym"], m["vwretd"]))
    m["x1"] = [vmap.get(p, np.nan) for p in ym_prev(m["ym"].to_numpy())]
    return m.rename(columns={"vwretd": "x0"})[["ym", "x0", "x1"]]


def dimson_betas(series_long: pd.DataFrame, mkt_lag: pd.DataFrame) -> pd.DataFrame:
    """[series, ym, ret] -> [series, beta, n_obs] Dimson sum-betas."""
    reg = series_long.merge(mkt_lag, on="ym", how="inner")
    reg = reg.dropna(subset=["ret", "x0", "x1"])
    return grouped_dimson_beta(
        reg.rename(columns={"ret": "y"}), group_col="series", min_obs=1
    )


# ────────────────────────────────────────────────────────────────────────────
# The three panels
# ────────────────────────────────────────────────────────────────────────────
def panel_a(port: pd.DataFrame, agg: pd.DataFrame) -> dict:
    """Average monthly EW returns, percent. 100 cells from
    portfolio_returns.parquet; All column / All row / All-All from the
    stock-level EW series."""
    vals = {}
    cell = (
        port.groupby(["size_decile", "beta_group"])["ret"].mean().reset_index()
    )
    for _, r in cell.iterrows():
        vals[(int(r["size_decile"]), int(r["beta_group"]))] = r["ret"] * 100.0

    ser = agg.groupby("series")["ret"].mean()
    for d in range(1, 11):
        vals[(d, "all")] = ser[f"size_{d}"] * 100.0
    for b in range(1, 11):
        vals[("all", b)] = ser[f"beta_{b}"] * 100.0
    vals[("all", "all")] = ser["grand"] * 100.0
    return vals


def panel_b(port: pd.DataFrame, agg: pd.DataFrame, mkt_lag: pd.DataFrame,
            panel: pd.DataFrame) -> tuple[dict, pd.DataFrame, float]:
    """Post-ranking Dimson sum-betas of the EW series. Returns the matrix
    values, the 100-cell beta table, and the max |diff| against the panel's
    post_beta (cross-check of the iteration-1 stored values)."""
    cells_long = port[["size_decile", "beta_group", "ym", "ret"]].copy()
    cells_long["series"] = (
        cells_long["size_decile"].astype(int).astype(str)
        + "_" + cells_long["beta_group"].astype(int).astype(str)
    )
    betas = dimson_betas(cells_long, mkt_lag)

    vals = {}
    cell_tbl = []
    for _, r in betas.iterrows():
        d, b = (int(x) for x in r["series"].split("_"))
        vals[(d, b)] = r["beta"]
        cell_tbl.append({"size_decile": d, "beta_group": b,
                         "beta": r["beta"], "n_obs": int(r["n_obs"])})
    cell_tbl = pd.DataFrame(cell_tbl)

    ser_betas = dimson_betas(agg[["series", "ym", "ret"]], mkt_lag)
    smap = dict(zip(ser_betas["series"], ser_betas["beta"]))
    for d in range(1, 11):
        vals[(d, "all")] = smap[f"size_{d}"]
    for b in range(1, 11):
        vals[("all", b)] = smap[f"beta_{b}"]
    vals[("all", "all")] = smap["grand"]

    # cross-check against the panel's stored post_beta (one per cell)
    pb = panel.drop_duplicates(["size_decile", "beta_group"])[
        ["size_decile", "beta_group", "post_beta"]
    ].copy()
    pb["size_decile"] = pb["size_decile"].astype(int)
    pb["beta_group"] = pb["beta_group"].astype(int)
    chk = pb.merge(cell_tbl[["size_decile", "beta_group", "beta"]],
                   on=["size_decile", "beta_group"], how="inner")
    max_diff = float((chk["post_beta"] - chk["beta"]).abs().max()) if len(chk) else np.nan
    return vals, cell_tbl, max_diff


def panel_c(panel: pd.DataFrame) -> tuple[dict, int, int]:
    """Average size ln(ME): time-series average of the June-formation
    cross-sectional means. Returns matrix values, number of formation years,
    and the minimum number of formation years any of the 100 cells appears in."""
    fy = panel.drop_duplicates(["fyr", "permno"])
    n_years = int(fy["fyr"].nunique())

    cell_year = (
        fy.groupby(["fyr", "size_decile", "beta_group"])["lnME"]
        .mean().reset_index()
    )
    cell_avg = cell_year.groupby(["size_decile", "beta_group"])["lnME"].mean()
    vals = {(int(d), int(b)): float(v) for (d, b), v in cell_avg.items()}
    yrs_per_cell = (
        cell_year.groupby(["size_decile", "beta_group"]).size().min()
    )

    allcol = (
        fy.groupby(["fyr", "size_decile"])["lnME"].mean()
        .groupby("size_decile").mean()
    )
    allrow = (
        fy.groupby(["fyr", "beta_group"])["lnME"].mean()
        .groupby("beta_group").mean()
    )
    for d in range(1, 11):
        vals[(d, "all")] = allcol[d]
    for b in range(1, 11):
        vals[("all", b)] = allrow[b]
    vals[("all", "all")] = fy.groupby("fyr")["lnME"].mean().mean()
    return vals, n_years, int(yrs_per_cell)


# ────────────────────────────────────────────────────────────────────────────
# Rendering
# ────────────────────────────────────────────────────────────────────────────
def render_matrix(vals: dict) -> str:
    lines = [
        "| Size \\ β | " + " | ".join(COL_LABELS) + " |",
        "|" + "---|" * (len(COL_LABELS) + 1),
    ]
    for rl in ROW_LABELS:
        rk = ROW_KEY[rl]
        cells = [f"{vals[(rk, COL_KEY[cl])]:.2f}" for cl in COL_LABELS]
        lines.append("| " + rl + " | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def eval_against_paper(vals_by_panel: dict) -> pd.DataFrame:
    """Compare ours vs paper for every metric in
    preparations/tables_to_replicate.json (table_1), with the per-metric
    tolerance. Returns one row per metric with pass/fail."""
    metrics_path = LAYOUT.preparations_path("tables_to_replicate.json")
    spec = json.loads(metrics_path.read_text())
    metrics = [t for t in spec["tables"] if t["id"] == "table_1"][0]["metrics"]

    rows = []
    seen = set()
    for m in metrics:
        mm = re.match(r"T1([ABC]) [^[]+\[([^\]]+)\]", m["name"])
        if not mm:
            continue
        pan, cell = mm.group(1), mm.group(2)
        row_s, col_s = [x.strip() for x in cell.split("x")]
        # metric labels use ASCII 'b' for beta ('Low-b', 'b-2', 'High-b')
        rl = row_s
        cl = (col_s.replace("Low-b", "Low-β").replace("High-b", "High-β")
              .replace("b-", "β-"))
        key = (pan, ROW_KEY[rl], COL_KEY[cl])
        if key in seen:          # the JSON lists All/All-type cells twice
            continue
        seen.add(key)
        paper = float(m["value"])
        ours = float(vals_by_panel[pan][(ROW_KEY[rl], COL_KEY[cl])])
        tol = float(m["tolerance_pct"]) / 100.0
        dev = ours - paper
        rows.append({
            "panel": pan, "row": rl, "col": cl,
            "paper": paper, "ours": ours, "dev": dev,
            "tol_pct": float(m["tolerance_pct"]),
            "pass": abs(dev) <= tol * abs(paper),
        })
    return pd.DataFrame(rows)


def comparison_section(vals_by_panel: dict) -> str:
    """The 'Comparison with paper' markdown: All column + All row + noted
    corners of each panel (paper values from PAPER, hardcoded from the task
    spec / inputs/content.md), with absolute deviations and pass/fail at the
    tables_to_replicate.json tolerances (A 25%, B 15%, C 10%)."""
    # ordered comparison cells per panel: All column, All row, corners
    size_rows = ["Small-ME"] + [f"ME-{d}" for d in range(2, 10)] + ["Large-ME"]
    beta_cols = ["Low-β"] + [f"β-{b}" for b in range(2, 10)] + ["High-β"]
    cells = {
        "A": [("All", "All")] + [(r, "All") for r in size_rows]
             + [("All", c) for c in beta_cols]
             + [("Small-ME", "Low-β"), ("Small-ME", "High-β"),
                ("Large-ME", "High-β")],
        "B": [(r, "All") for r in size_rows]   # paper gives no All/All value
             + [("Small-ME", "Low-β"), ("Small-ME", "High-β"),
                ("Large-ME", "Low-β"), ("Large-ME", "High-β"),
                ("ME-8", "Low-β")],
        "C": [("All", "All")] + [(r, "All") for r in size_rows]
             + [("All", c) for c in beta_cols]
             + [("Small-ME", "Low-β"), ("Large-ME", "Low-β"),
                ("Large-ME", "High-β")],
    }
    titles = {
        "A": "Panel A — average monthly returns (%/month)",
        "B": "Panel B — post-ranking β",
        "C": "Panel C — average size ln(ME)",
    }
    parts = []
    for pan in "ABC":
        lines = [
            f"### {titles[pan]}",
            "",
            "| Cell | Paper | Ours | \\|Δ\\| | Tol | Pass |",
            "|---|---:|---:|---:|---:|:---:|",
        ]
        for rl, cl in cells[pan]:
            paper = PAPER[(pan, rl, cl)]
            ours = float(vals_by_panel[pan][(ROW_KEY[rl], COL_KEY[cl])])
            dev = ours - paper
            tol = TOL[pan]
            ok = abs(dev) <= tol * abs(paper)
            lines.append(
                f"| {rl} × {cl} | {paper:.2f} | {ours:.2f} | "
                f"{abs(dev):.3f} | {int(tol*100)}% | "
                f"{'✅' if ok else '❌'} |"
            )
        parts.append("\n".join(lines))

    # Panel B 100-cell min/max cross-check (paper: min 0.53 at ME-8×Low-β,
    # max 1.79 at Small-ME×High-β)
    bvals = vals_by_panel["B"]
    interior = {(r, c): v for (r, c), v in bvals.items()
                if r != "all" and c != "all"}
    (rmin, cmin), vmin = min(interior.items(), key=lambda kv: kv[1])
    (rmax, cmax), vmax = max(interior.items(), key=lambda kv: kv[1])
    rl_of = {v: k for k, v in ROW_KEY.items()}
    cl_of = {v: k for k, v in COL_KEY.items()}
    parts.append(
        "### Panel B — 100-cell range cross-check\n\n"
        f"- Paper: min 0.53 (ME-8 × Low-β), max 1.79 (Small-ME × High-β).\n"
        f"- Ours: min {vmin:.2f} ({rl_of[rmin]} × {cl_of[cmin]}), "
        f"max {vmax:.2f} ({rl_of[rmax]} × {cl_of[cmax]})."
    )
    return "\n\n".join(parts)


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    t0 = time.time()
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    port = pd.read_parquet(LAYOUT.data_path("portfolio_returns.parquet"))
    mkt = q_file("market_index_monthly.sql")

    n_months = panel["month"].nunique()

    # aggregated EW series (stock level) — saved for Tables II/VI reuse
    agg = build_agg_series(panel)
    agg_path = LAYOUT.data_path("agg_portfolio_returns.parquet")
    agg.to_parquet(agg_path, index=False)
    obs_ok = (agg.groupby("series")["ym"].count() == N_MONTHS).all()
    print(f"agg series: {agg['series'].nunique()} series x months; "
          f"all have {N_MONTHS} obs: {obs_ok}")

    mkt_lag = market_with_lag(mkt)

    A = panel_a(port, agg)
    B, cell_tbl, post_diff = panel_b(port, agg, mkt_lag, panel)
    C, n_years, min_cell_years = panel_c(panel)
    vals_by_panel = {"A": A, "B": B, "C": C}

    # ── markdown output ───────────────────────────────────────────────────
    comp_md = comparison_section(vals_by_panel)
    ev = eval_against_paper(vals_by_panel)

    md = []
    md.append("# Table I — Fama & French (1992), The Cross-Section of Expected Stock Returns")
    md.append("")
    md.append(
        f"Average monthly returns, post-ranking βs and average size for the 100 "
        f"portfolios formed on size (rows: Small-ME = decile 1 … Large-ME = "
        f"decile 10) then pre-ranking β (columns: Low-β = group 1 … High-β = "
        f"group 10). Sample: July 1963 – December 1990 ({n_months} months; "
        f"{n_years} formation years, 1963–1990). All portfolios equal-weighted; "
        f"βs are full-sample Dimson sum-betas on current + 1-lagged CRSP "
        f"value-weighted returns; ln(ME) uses June market equity in $ millions."
    )
    md.append("")
    md.append("## Panel A — Average monthly returns (percent)")
    md.append("")
    md.append(render_matrix(A))
    md.append("")
    md.append("## Panel B — Post-ranking βs")
    md.append("")
    md.append(render_matrix(B))
    md.append("")
    md.append("## Panel C — Average size ln(ME)")
    md.append("")
    md.append(render_matrix(C))
    md.append("")
    md.append("## Comparison with paper")
    md.append("")
    md.append(
        "Paper values from Fama & French (1992) Table I "
        "(inputs/content.md). Pass = |Δ| within tolerance "
        "(returns 25%, βs 15%, ln(ME) 10%, per "
        "preparations/tables_to_replicate.json)."
    )
    md.append("")
    md.append(comp_md)
    md.append("")

    # pass/fail over the FULL metric list in tables_to_replicate.json
    counts = ev.groupby("panel")["pass"].agg(["sum", "count"])
    md.append("### Pass/fail vs preparations/tables_to_replicate.json (all targeted cells)")
    md.append("")
    md.append("| Panel | Pass | Total |")
    md.append("|---|---:|---:|")
    for pan in "ABC":
        c = counts.loc[pan]
        md.append(f"| {pan} | {int(c['sum'])} | {int(c['count'])} |")
    md.append(f"| **All** | **{int(ev['pass'].sum())}** | **{len(ev)}** |")
    fails = ev[~ev["pass"]]
    md.append("")
    if len(fails):
        md.append("Failing metrics:")
        md.append("")
        md.append("| Panel | Cell | Paper | Ours | Dev | Tol |")
        md.append("|---|---|---:|---:|---:|---:|")
        for _, r in fails.iterrows():
            md.append(
                f"| {r['panel']} | {r['row']} × {r['col']} | {r['paper']:.2f} | "
                f"{r['ours']:.2f} | {r['dev']:+.3f} | {r['tol_pct']:.0f}% |"
            )
    else:
        md.append("No failing metrics.")
    md.append("")
    md.append("---")
    md.append(
        f"*Computed by src/table_1.py from data/panel.parquet and "
        f"data/portfolio_returns.parquet (iteration-1 pipeline). The 100 cell "
        f"betas above reproduce the panel's stored post_beta to "
        f"{post_diff:.1e}. Aggregated EW series saved to "
        f"data/agg_portfolio_returns.parquet (21 series × {N_MONTHS} months).*"
    )

    out = LAYOUT.result_path("table_1.md")
    out.write_text("\n".join(md))
    print(f"wrote {out}")

    # ── console report ────────────────────────────────────────────────────
    print(f"\nmonths: {n_months} (paper: 330) | formation years: {n_years} (paper: 28)")
    print(f"post_beta cross-check max |diff| vs recomputation: {post_diff:.2e}")
    print(f"min formation years any 100-cell appears in: {min_cell_years}")
    for pan, title in (("A", "PANEL A — avg returns (%)"),
                       ("B", "PANEL B — post-ranking betas"),
                       ("C", "PANEL C — avg ln(ME)")):
        print(f"\n{title}")
        print(render_matrix(vals_by_panel[pan]))
    print("\npass/fail vs tables_to_replicate.json:")
    for pan in "ABC":
        c = counts.loc[pan]
        print(f"  Panel {pan}: {int(c['sum'])}/{int(c['count'])} pass")
    print(f"  TOTAL: {int(ev['pass'].sum())}/{len(ev)} pass")
    if len(fails):
        print("  failing:")
        for _, r in fails.iterrows():
            print(f"    {r['panel']} {r['row']} × {r['col']}: "
                  f"paper {r['paper']:.2f}, ours {r['ours']:.2f} "
                  f"(dev {r['dev']:+.3f}, tol {r['tol_pct']:.0f}%)")
    biggest = ev.reindex(ev["dev"].abs().sort_values(ascending=False).index).head(5)
    print("  biggest |deviations|:")
    for _, r in biggest.iterrows():
        print(f"    {r['panel']} {r['row']} × {r['col']}: "
              f"paper {r['paper']:.2f}, ours {r['ours']:.2f} (dev {r['dev']:+.3f})")
    print(f"\ntotal time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
