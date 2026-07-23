"""
Heston & Sadka (2010), "Seasonality in the Cross Section of Stock Returns:
The International Evidence" — TABLE 3 (top-minus-bottom decile spread
strategies, intra/inter decomposition).

Consumes the cached analysis-ready panel (data/panel.parquet, READ-ONLY;
columns gvkey, country, curcdd, month, ret_local, ret_usd, me_usd) and writes:

  results/table_3.md                  — four blocks (EW/VW x PanelA/PanelB),
                                        our values with paper in parentheses,
                                        plus T (feasible months) per row.
  results/cells_t3.json               — flat {metric_name: our_value} for all
                                        288 T3 names in tables_to_replicate.json.
  results/table3_ew_panelA_bars.png   — grouped bars: EW Panel A TOTAL spreads
                                        (nonannual/annual/difference) per strategy
                                        group, ours vs paper.

Methodology (fixed by the Replicator — see task spec + assumptions.md
A5/A6/A7/A9/A11):

All definitions on USD returns (ret_usd).

  Country EW benchmark  rbar[c,t] = simple mean of ret_usd over firms of
                        country c in month t.
  Arithmetic excess     ex[i,t] = ret_usd[i,t] - rbar[country(i),t]   (A5)

Strategy lag sets (A6; lag k measured from the sort month t, i.e. month t-k):
  Year 1    annual={12};        nonannual={1..11};         all={1..12}
  Years 2-3 annual={24,36};     nonannual={13..23,25..35}; all={13..36}
  Years 4-5 annual={48,60};     nonannual={37..47,49..59}; all={37..60}

Signals (computed at each sort month t):
  Panel A signal = mean of ex[i,t-k]     over k in the lag set (average over the
                   lags that are non-missing; if NONE available -> signal missing).
  Panel B signal = mean of ret_usd[i,t-k] over k in the lag set (same rule).

Sort (A7): for each month t in 1985-02..2006-06, firms with non-missing signal
  AND non-missing ret_usd[t]; rank ascending by signal (average ranks for ties);
  decile = ceil(10*rank/N) clipped to [1,10] (decile 1 = lowest signal, 10 = highest).

Monthly spread series (per panel, per weighting):
  EW Total[t] = mean(ret_usd[t] in D10) - mean(ret_usd[t] in D1)
  VW Total[t] = me_usd[t-1]-weighted mean of ret_usd[t] in D10 minus D1
                (weights require non-missing and >0; firms without a valid prior
                month me_usd are dropped from the VW weighting set only — they
                stay in the signal-based decile assignment).
  Intra[t]    = same as Total but using ex[i,t] (EW and VW variants).
  Inter[t]    = Total[t] - Intra[t]   (exact, per A5 additivity).

Reported rows per strategy group (nonannual, annual, difference, all):
  nonannual/annual/all: time-series mean of the monthly spread series;
                tstat = mean/(std/sqrt(T)), T = months where the spread was
                computable (both deciles non-empty; for VW both deciles must
                also have a firm with a valid weight).
  difference: monthly series diff[t] = annual[t] - nonannual[t] over months
                where BOTH exist; report mean and t-stat of the diff series.

Four blocks EW x PanelA, EW x PanelB, VW x PanelA, VW x PanelB, each with
columns total / intra / inter => 4 blocks x 3 groups x 4 rows x 3 components
= 144 return cells + 144 t-stat cells = 288 metrics.

Performance: per sort month t and per panel, gather the lag months t-1..t-60
once into a wide (gvkey x 60) block, then compute each lag-set signal vectorized
(nansum / non-NaN count). A 257-month loop with vectorized within-month ops.

Usage:  python3 src/compute_t3.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ────────────────────────────────────────────────────────────────────────────
# Paths & constants
# ────────────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
PANEL_PATH = ROOT / "data" / "panel.parquet"
RESULTS_DIR = ROOT / "results"
TABLES_JSON = ROOT / "preparations" / "tables_to_replicate.json"

# Sort-month window 1985-02 .. 2006-06 inclusive (257 months), month-index
# encoding mi = year*12 + month-of-year.
SORT_LO = 1985 * 12 + 2
SORT_HI = 2006 * 12 + 6

WEIGHTINGS = ["ew", "vw"]
PANELS = ["panelA", "panelB"]
GROUPS = ["y1", "y23", "y45"]
COMPONENTS = ["total", "intra", "inter"]
STRATEGIES = ["nonannual", "annual", "all"]   # 'difference' is derived

# Strategy lag sets (A6). Lag k => month t-k.
LAG_SETS: dict[str, dict[str, list[int]]] = {
    "y1": {
        "nonannual": list(range(1, 12)),                    # 1..11
        "annual":    [12],
        "all":       list(range(1, 13)),                    # 1..12
    },
    "y23": {
        "nonannual": list(range(13, 24)) + list(range(25, 36)),  # 13..23, 25..35
        "annual":    [24, 36],
        "all":       list(range(13, 37)),                   # 13..36
    },
    "y45": {
        "nonannual": list(range(37, 48)) + list(range(49, 60)),  # 37..47, 49..59
        "annual":    [48, 60],
        "all":       list(range(37, 61)),                   # 37..60
    },
}
# column offset within the 60-wide lag block (index k-1 holds lag k)
LAG_COLS: dict[str, dict[str, list[int]]] = {
    g: {s: [k - 1 for k in lags] for s, lags in strat.items()}
    for g, strat in LAG_SETS.items()
}

GROUP_LABEL = {"y1": "Year 1", "y23": "Years 2-3", "y45": "Years 4-5"}
ROW_LABEL = {"nonannual": "nonannual", "annual": "annual",
             "difference": "difference", "all": "all"}


# ────────────────────────────────────────────────────────────────────────────
# Data prep — build (gvkey x month-index) matrices for ret_usd, excess, me_usd
# ────────────────────────────────────────────────────────────────────────────
def build_matrices(panel: pd.DataFrame) -> dict:
    """Returns dict with numpy matrices R (ret_usd), E (arithmetic excess),
    ME (me_usd) indexed [gvkey-row x month-col], plus axis maps."""
    d = panel[["gvkey", "country", "month", "ret_usd", "me_usd"]].copy()
    d["mi"] = d["month"].dt.year * 12 + d["month"].dt.month

    # Country EW benchmark rbar[c,t] = mean ret_usd over firms of c in month t
    # (groupby.mean skips NaN). ex[i,t] = ret_usd[i,t] - rbar[country(i),t].
    rbar = d.groupby(["country", "mi"])["ret_usd"].transform("mean")
    d["ex"] = d["ret_usd"] - rbar

    gvkeys = pd.Index(pd.unique(d["gvkey"]))
    row_of = {g: i for i, g in enumerate(gvkeys)}
    mi_min = int(d["mi"].min())
    mi_max = int(d["mi"].max())
    n_month = mi_max - mi_min + 1
    n_firm = len(gvkeys)

    def to_matrix(value_col: str) -> np.ndarray:
        m = np.full((n_firm, n_month), np.nan)
        rows = d["gvkey"].map(row_of).to_numpy()
        cols = (d["mi"].to_numpy() - mi_min)
        vals = d[value_col].to_numpy(dtype=float)
        m[rows, cols] = vals
        return m

    R = to_matrix("ret_usd")
    E = to_matrix("ex")
    ME = to_matrix("me_usd")

    # sanity: no duplicate (gvkey, mi) wrote over a distinct value silently
    n_written = d["ret_usd"].notna().sum() + d["ret_usd"].isna().sum()
    assert n_written == len(d)

    print(f"Matrices: {n_firm:,} gvkeys x {n_month} months "
          f"(mi {mi_min}..{mi_max} = {mi_min//12}-{mi_min%12:02d} .. "
          f"{mi_max//12}-{mi_max%12:02d})")
    print(f"  ret_usd non-missing cells: {np.isfinite(R).sum():,}")
    print(f"  ex      non-missing cells: {np.isfinite(E).sum():,}")
    print(f"  me_usd  non-missing cells: {np.isfinite(ME).sum():,}")

    return dict(R=R, E=E, ME=ME, mi_min=mi_min, mi_max=mi_max,
                n_month=n_month, n_firm=n_firm)


# ────────────────────────────────────────────────────────────────────────────
# Per-sort spread computation
# ────────────────────────────────────────────────────────────────────────────
def _wmean(w: np.ndarray, x: np.ndarray) -> float:
    sw = w.sum()
    return float((w * x).sum() / sw) if sw > 0 else float("nan")


def sort_spreads(signal: np.ndarray, ret_t: np.ndarray, ex_t: np.ndarray,
                 w_t: np.ndarray) -> dict | None:
    """Given per-firm arrays (aligned rows), sort candidates (non-missing
    signal AND ret_t) into deciles and return EW/VW total/intra/inter spreads
    plus the cross-section size N. Returns None if fewer than 2 candidates."""
    cand = np.isfinite(signal) & np.isfinite(ret_t)
    idx = np.where(cand)[0]
    N = int(idx.size)
    if N < 2:
        return None
    sig = signal[idx]
    # ascending ranks, average ranks for ties; decile = ceil(10*rank/N) in [1,10]
    ranks = pd.Series(sig).rank(method="average").to_numpy()
    decile = np.clip(np.ceil(10.0 * ranks / N), 1, 10).astype(int)

    rt = ret_t[idx]
    et = ex_t[idx]
    wt = w_t[idx]
    m1 = decile == 1
    m10 = decile == 10

    out: dict = {"N": N, "ew": {}, "vw": {}}

    # EW — both candidates have finite ret_t and ex_t by construction
    if m1.any() and m10.any():
        ew_tot = float(rt[m10].mean() - rt[m1].mean())
        ew_intra = float(et[m10].mean() - et[m1].mean())
        out["ew"] = {"total": ew_tot, "intra": ew_intra,
                     "inter": ew_tot - ew_intra}
    else:
        out["ew"] = {"total": np.nan, "intra": np.nan, "inter": np.nan}

    # VW — require a valid prior-month me_usd (>0) within each decile
    validw = np.isfinite(wt) & (wt > 0)
    v1 = m1 & validw
    v10 = m10 & validw
    if v1.any() and v10.any():
        vw_tot = _wmean(wt[v10], rt[v10]) - _wmean(wt[v1], rt[v1])
        vw_intra = _wmean(wt[v10], et[v10]) - _wmean(wt[v1], et[v1])
        out["vw"] = {"total": vw_tot, "intra": vw_intra,
                     "inter": vw_tot - vw_intra}
    else:
        out["vw"] = {"total": np.nan, "intra": np.nan, "inter": np.nan}

    return out


# ────────────────────────────────────────────────────────────────────────────
# Main computation — loop over sort months, accumulate monthly spread series
# ────────────────────────────────────────────────────────────────────────────
def compute_table3(mat: dict) -> tuple[dict, dict, dict]:
    """Returns:
      series[(w,panel,group,strategy,component)] = {month_idx: spread}
      T[(w,panel,group,row)] = feasible month count (row incl. 'difference')
      N_by_group[group] = list of per-sort cross-section sizes N
    """
    R, E, ME = mat["R"], mat["E"], mat["ME"]
    mi_min, mi_max = mat["mi_min"], mat["mi_max"]
    n_firm, n_month = mat["n_firm"], mat["n_month"]

    # Append a sentinel all-NaN column so out-of-range lag lookups map to it.
    sentinel = n_month
    R_s = np.concatenate([R, np.full((n_firm, 1), np.nan)], axis=1)
    E_s = np.concatenate([E, np.full((n_firm, 1), np.nan)], axis=1)

    def lag_index(t: int, k: int) -> int:
        c = t - k
        return (c - mi_min) if (mi_min <= c <= mi_max) else sentinel

    series: dict = defaultdict(dict)
    N_by_group: dict = defaultdict(list)

    sort_months = list(range(SORT_LO, SORT_HI + 1))
    for n, t in enumerate(sort_months):
        # column index of the holding month t and the prior month t-1 (weights)
        t_col = (t - mi_min) if (mi_min <= t <= mi_max) else None
        if t_col is None:
            continue
        ret_t = R[:, t_col]
        ex_t = E[:, t_col]
        w_t = ME[:, (t - 1 - mi_min)] if (mi_min <= t - 1 <= mi_max) \
            else np.full(n_firm, np.nan)

        # index vector for lags 1..60 -> block columns (gather once per panel)
        idx60 = np.array([lag_index(t, k) for k in range(1, 61)], dtype=int)
        block_R = R_s[:, idx60]   # Panel B source (ret_usd lags)
        block_E = E_s[:, idx60]   # Panel A source (excess lags)

        for panel in PANELS:
            block = block_E if panel == "panelA" else block_R
            for group in GROUPS:
                for strategy in STRATEGIES:
                    cols = LAG_COLS[group][strategy]
                    sub = block[:, cols]
                    nanmask = np.isnan(sub)
                    cnt = sub.shape[1] - nanmask.sum(axis=1)
                    s = np.where(nanmask, 0.0, sub).sum(axis=1)
                    signal = np.where(cnt > 0, s / np.maximum(cnt, 1), np.nan)

                    res = sort_spreads(signal, ret_t, ex_t, w_t)
                    if res is None:
                        continue
                    N_by_group[group].append(res["N"])
                    for w in WEIGHTINGS:
                        for comp in COMPONENTS:
                            val = res[w][comp]
                            if np.isfinite(val):
                                series[(w, panel, group, strategy, comp)][t] = val

        if (n + 1) % 50 == 0:
            print(f"  processed {n + 1}/{len(sort_months)} sort months")

    # Feasible-month counts T per (block, group, row). total/intra/inter share
    # the same feasible months within a (block, group, strategy), so use 'total'.
    T: dict = {}
    for w in WEIGHTINGS:
        for panel in PANELS:
            for group in GROUPS:
                for strategy in STRATEGIES:
                    T[(w, panel, group, strategy)] = len(
                        series[(w, panel, group, strategy, "total")])
                ann = series[(w, panel, group, "annual", "total")]
                non = series[(w, panel, group, "nonannual", "total")]
                T[(w, panel, group, "difference")] = len(
                    set(ann.keys()) & set(non.keys()))

    return series, T, N_by_group


# ────────────────────────────────────────────────────────────────────────────
# Time-series stats + cells assembly
# ────────────────────────────────────────────────────────────────────────────
def ts_stats(vals: dict) -> tuple[float, float, int]:
    """mean, iid t-stat (mean/(std/sqrt(T))), T over the month->value dict."""
    arr = np.array(list(vals.values()), dtype=float)
    T = int(arr.size)
    if T == 0:
        return float("nan"), float("nan"), 0
    m = float(arr.mean())
    if T < 2:
        return m, float("nan"), T
    sd = float(arr.std(ddof=1))
    tstat = float(m / (sd / np.sqrt(T))) if sd > 0 else float("nan")
    return m, tstat, T


def assemble_cells(series: dict) -> dict[str, float]:
    """Build the flat {metric_name: value} dict for all 288 T3 metrics."""
    cells: dict[str, float] = {}
    for w in WEIGHTINGS:
        for panel in PANELS:
            for group in GROUPS:
                for comp in COMPONENTS:
                    for strategy in STRATEGIES:
                        m, tstat, _ = ts_stats(
                            series[(w, panel, group, strategy, comp)])
                        cells[f"t3_{w}_{panel}_{group}_{strategy}_{comp}_ret"] = m
                        cells[f"t3_{w}_{panel}_{group}_{strategy}_{comp}_tstat"] = tstat
                    # difference row: annual - nonannual over common months
                    ann = series[(w, panel, group, "annual", comp)]
                    non = series[(w, panel, group, "nonannual", comp)]
                    common = set(ann.keys()) & set(non.keys())
                    diff = {mo: ann[mo] - non[mo] for mo in common}
                    m, tstat, _ = ts_stats(diff)
                    cells[f"t3_{w}_{panel}_{group}_difference_{comp}_ret"] = m
                    cells[f"t3_{w}_{panel}_{group}_difference_{comp}_tstat"] = tstat
    return cells


# ────────────────────────────────────────────────────────────────────────────
# Output writers
# ────────────────────────────────────────────────────────────────────────────
def load_paper_values() -> tuple[dict, list[str]]:
    tables = json.loads(TABLES_JSON.read_text())["tables"]
    pv, names = {}, []
    for t in tables:
        if t["id"] == "T3":
            for m in t["metrics"]:
                pv[m["name"]] = m["value"]
                names.append(m["name"])
    return pv, names


def write_table3_md(cells: dict, T: dict, N_by_group: dict, paper: dict) -> None:
    lines = [
        "# Table 3 — Seasonality: Top-minus-Bottom Decile Spread Strategies",
        "",
        "Heston & Sadka (2010), Table 3. Monthly decile spreads (D10 - D1) on",
        "USD returns, sorted each month t in 1985-02..2006-06 on the lag-set",
        "average of arithmetic country-excess returns (Panel A) or total USD",
        "returns (Panel B). EW = equal-weighted; VW = value-weighted with",
        "prior-month (t-1) me_usd. Intra = within-country (excess) component;",
        "Inter = Total - Intra (exact, A5). Our values with paper values in",
        "parentheses. t-stat = mean/(std/sqrt(T)), T = feasible months per row.",
        "",
    ]

    block_titles = {
        ("ew", "panelA"): "Block 1 — Equal-Weighted, Panel A (excess-return sorts)",
        ("ew", "panelB"): "Block 2 — Equal-Weighted, Panel B (total-return sorts)",
        ("vw", "panelA"): "Block 3 — Value-Weighted, Panel A (excess-return sorts)",
        ("vw", "panelB"): "Block 4 — Value-Weighted, Panel B (total-return sorts)",
    }
    header = ("| Strategy group | Row | Total ret | Total t | Intra ret | Intra t "
              "| Inter ret | Inter t | T |")
    sep = "|---" * 9 + "|"

    for w in WEIGHTINGS:
        for panel in PANELS:
            lines += ["", f"## {block_titles[(w, panel)]}", "", header, sep]
            for group in GROUPS:
                for row in ["nonannual", "annual", "difference", "all"]:
                    cells_row = []
                    for comp in COMPONENTS:
                        our_r = cells[f"t3_{w}_{panel}_{group}_{row}_{comp}_ret"]
                        our_t = cells[f"t3_{w}_{panel}_{group}_{row}_{comp}_tstat"]
                        p_r = paper.get(f"t3_{w}_{panel}_{group}_{row}_{comp}_ret")
                        p_t = paper.get(f"t3_{w}_{panel}_{group}_{row}_{comp}_tstat")
                        cells_row.append(f"{our_r:+.4f} ({p_r:+.4f})")
                        cells_row.append(f"{our_t:+.2f} ({p_t:+.2f})")
                    Tval = T[(w, panel, group, row)]
                    gl = GROUP_LABEL[group] if row == "nonannual" else ""
                    lines.append(f"| {gl} | {ROW_LABEL[row]} | "
                                 + " | ".join(cells_row) + f" | {Tval} |")

    # cross-section size distribution N per strategy group
    lines += ["", "## Cross-section size N per sort (firms with signal & ret_usd[t])",
              "",
              "| Strategy group | sorts | min N | median N | max N |",
              "|---|---|---|---|---|"]
    for group in GROUPS:
        arr = np.array(N_by_group[group])
        lines.append(f"| {GROUP_LABEL[group]} | {arr.size} | {arr.min()} | "
                     f"{int(np.median(arr))} | {arr.max()} |")

    (RESULTS_DIR / "table_3.md").write_text("\n".join(lines) + "\n")


def write_cells_json(cells: dict, metric_names: list[str]) -> dict:
    """Emit flat {metric_name: value} covering EVERY T3 name in the spec file."""
    out: dict = {}
    for name in metric_names:
        v = cells[name]
        assert np.isfinite(v), f"non-finite T3 cell {name} = {v}"
        out[name] = float(v)
    (RESULTS_DIR / "cells_t3.json").write_text(
        json.dumps(out, indent=2, allow_nan=False) + "\n")
    return out


def write_plot(cells: dict, paper: dict) -> None:
    rows = ["nonannual", "annual", "difference"]
    groups = GROUPS
    x = np.arange(len(groups))
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 6))

    row_colors = {"nonannual": "#1f77b4", "annual": "#2ca02c",
                  "difference": "#d62728"}
    for i, row in enumerate(rows):
        ours = [cells[f"t3_ew_panelA_{g}_{row}_total_ret"] for g in groups]
        paps = [paper[f"t3_ew_panelA_{g}_{row}_total_ret"] for g in groups]
        pos = x + (i - 1) * width
        ax.bar(pos, ours, width, color=row_colors[row], alpha=0.85,
               label=f"{row} (ours)", edgecolor="black", linewidth=0.4)
        ax.scatter(pos, paps, marker="D", s=55, facecolors="none",
                   edgecolors=row_colors[row], linewidths=1.8, zorder=5,
                   label=f"{row} (paper)")

    ax.axhline(0.0, color="grey", lw=0.9, ls="--")
    ax.set_xticks(x)
    ax.set_xticklabels([GROUP_LABEL[g] for g in groups])
    ax.set_ylabel("D10 - D1 monthly spread (total, decimal)")
    ax.set_title("EW Panel A decile spreads (ours vs paper)")
    ax.legend(ncol=2, fontsize=8, loc="best")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "table3_ew_panelA_bars.png", dpi=150)
    plt.close(fig)


def write_y23_outputs(series: dict) -> pd.DataFrame:
    """REPORT.md visual: export the MONTHLY pooled EW Panel A Years-2-3 Total
    spread series (annual, nonannual, difference) over t = 1985-02..2006-06 to
    results/ew_panelA_y23_monthly.csv (one row per sort month, NaN where a side
    is unavailable), and plot their cumulative sums (simple cumsum, missing
    months skipped) to results/cumulative_y23_spreads.png. Returns the cumsum
    frame (final row = sum of available monthly spreads)."""
    ann = series[("ew", "panelA", "y23", "annual", "total")]
    non = series[("ew", "panelA", "y23", "nonannual", "total")]

    months = list(range(SORT_LO, SORT_HI + 1))
    recs = []
    for t in months:
        year = (t - 1) // 12
        moy = (t - 1) % 12 + 1
        a = ann.get(t, np.nan)
        n = non.get(t, np.nan)
        d = (a - n) if (np.isfinite(a) and np.isfinite(n)) else np.nan
        recs.append({"month": f"{year}-{moy:02d}-01",
                     "annual": a, "nonannual": n, "difference": d})
    df = pd.DataFrame(recs)
    csv_path = RESULTS_DIR / "ew_panelA_y23_monthly.csv"
    df.to_csv(csv_path, index=False, na_rep="")

    # cumulative sums (skipna treats missing months as contributing 0)
    cols = ["annual", "nonannual", "difference"]
    cum = df[cols].cumsum(skipna=True)
    dates = pd.to_datetime(df["month"])

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {"nonannual": "#1f77b4", "annual": "#2ca02c",
              "difference": "#d62728"}
    for col in cols:
        ax.plot(dates, cum[col], label=col, color=colors[col], lw=1.6)
    ax.axhline(0.0, color="grey", lw=0.9, ls="--")
    ax.set_xlabel("Year")
    ax.set_ylabel("Cumulative return (sum of monthly spreads)")
    ax.set_title("EW Panel A Years 2-3 decile spreads — cumulative "
                 "(pooled 14 countries)")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "cumulative_y23_spreads.png", dpi=150)
    plt.close(fig)

    print(f"\n=== EW Panel A Years 2-3 cumulative (sum of monthly spreads) ===")
    for col in cols:
        n_avail = int(df[col].notna().sum())
        print(f"  {col:10s} final cumsum={cum[col].iloc[-1]:+.4f} "
              f"(over {n_avail} months)")
    return cum


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Loading panel: {PANEL_PATH}")
    panel = pd.read_parquet(PANEL_PATH)
    print(f"Panel: {len(panel):,} rows x {panel.shape[1]} cols, "
          f"months {panel['month'].min().date()}..{panel['month'].max().date()}")

    paper, metric_names = load_paper_values()
    print(f"T3 metric names from tables_to_replicate.json: {len(metric_names)}")
    assert len(metric_names) == 288, len(metric_names)

    mat = build_matrices(panel)

    print("\n=== Table 3 — sorting + spreads ===")
    series, T, N_by_group = compute_table3(mat)

    cells = assemble_cells(series)
    out = write_cells_json(cells, metric_names)
    write_table3_md(cells, T, N_by_group, paper)
    write_plot(cells, paper)
    write_y23_outputs(series)

    # ---- console spot checks ----
    print("\n=== EW Panel A headline (total): ours vs paper ===")
    for g in GROUPS:
        for row in ["nonannual", "annual", "difference", "all"]:
            our_r = cells[f"t3_ew_panelA_{g}_{row}_total_ret"]
            our_t = cells[f"t3_ew_panelA_{g}_{row}_total_tstat"]
            p_r = paper[f"t3_ew_panelA_{g}_{row}_total_ret"]
            p_t = paper[f"t3_ew_panelA_{g}_{row}_total_tstat"]
            print(f"  {g} {row:10s} ret={our_r:+.4f} ({p_r:+.4f})  "
                  f"t={our_t:+.2f} ({p_t:+.2f})  T={T[('ew','panelA',g,row)]}")

    # additivity check
    mx = 0.0
    for w in WEIGHTINGS:
        for panel_ in PANELS:
            for g in GROUPS:
                for row in STRATEGIES + ["difference"]:
                    tr = cells[f"t3_{w}_{panel_}_{g}_{row}_total_ret"]
                    ir = cells[f"t3_{w}_{panel_}_{g}_{row}_intra_ret"]
                    nr = cells[f"t3_{w}_{panel_}_{g}_{row}_inter_ret"]
                    mx = max(mx, abs(tr - ir - nr))
    print(f"\nAdditivity max |Total - Intra - Inter| (our ret cells): {mx:.2e}")

    print(f"\nWrote: table_3.md, cells_t3.json ({len(out)} names), "
          f"table3_ew_panelA_bars.png, ew_panelA_y23_monthly.csv, "
          f"cumulative_y23_spreads.png")


if __name__ == "__main__":
    main()
