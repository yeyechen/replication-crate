"""
Heston & Sadka (2010), "Seasonality in the Cross Section of Stock Returns:
The International Evidence" — TABLE 7 (top-minus-bottom EW decile spread
strategies computed SEPARATELY WITHIN EACH of the 14 countries).

Consumes the cached analysis-ready panel (data/panel.parquet, READ-ONLY;
columns gvkey, country, curcdd, month, ret_local, ret_usd, me_usd) and writes:

  results/table_7.md                        — three panels (A/B/C = Years 1 /
                                              2-3 / 4-5), rows nonannual/annual/
                                              difference/all with ret + t-stat,
                                              columns = 14 countries; our values
                                              with paper in parentheses; plus a
                                              T-per-country table (feasible months
                                              for the y23 difference row).
  results/cells_t7.json                     — flat {metric_name: our_value} for
                                              all 336 T7 names.
  results/table7_y23_difference_by_country.png — one bar per country for the
                                              Panel B (Years 2-3) difference row
                                              (ours) with paper markers overlaid.

Methodology (fixed by the Replicator — task spec + assumptions.md A5/A6/A7/A11/A13):

All definitions on USD returns (ret_usd); EW only (no VW, no intra/inter split).

  Country EW benchmark  rbar[c,t] = simple mean of ret_usd over firms of country
                        c in month t.
  Arithmetic excess     ex[i,t] = ret_usd[i,t] - rbar[country(i),t]   (A5)

Table 7's three PANELS are the three year groups, each using the EXCESS-return
signal (the paper's Panel A sorts), computed within a single country:
  Panel A (y1)   annual={12};    nonannual={1..11};          all={1..12}
  Panel B (y23)  annual={24,36}; nonannual={13..23,25..35};  all={13..36}
  Panel C (y45)  annual={48,60}; nonannual={37..47,49..59};  all={37..60}

Signal at sort month t for firm i = mean of ex[i,t-k] over k in the lag set
(average over the lags that are non-missing; if NONE available -> signal missing).

Within-country sort (A7): for each month t in 1985-02..2006-06 and country c,
  take firms of country c with non-missing signal AND non-missing ret_usd[t];
  rank ascending (average ranks for ties); decile = ceil(10*rank/N) clipped to
  [1,10] (decile 1 = lowest signal, 10 = highest).
  Spread[c,t] = mean(ret_usd[t] in D10) - mean(ret_usd[t] in D1), EW only.
  (Within a single country this equals the excess-return spread since rbar[c,t]
   is constant across the country's firms in month t.)

Reported per (panel, country):
  nonannual / annual / all : time-series mean of Spread[c,t];
                tstat = mean/(std/sqrt(T)), T = months where BOTH deciles were
                non-empty.
  difference : monthly series annual[t] - nonannual[t] over months where BOTH
                exist; report mean + t-stat of that series.

3 panels x 4 rows x 14 countries x 2 (ret/tstat) = 336 metrics.

Performance: signals are computed vectorized across ALL firms and months per
lag set (shifted-copy accumulation), then a 257-month x 9 (group,strategy) x
14-country within-country sort loop (scipy.stats.rankdata, ~32k sorts).

Usage:  python3 src/compute_t7.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata

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

# Table 7 panels are the three year groups; all use the excess-return signal.
GROUPS = ["y1", "y23", "y45"]
PANEL_OF_GROUP = {"y1": "panelA", "y23": "panelB", "y45": "panelC"}
GROUP_OF_PANEL = {v: k for k, v in PANEL_OF_GROUP.items()}
STRATEGIES = ["nonannual", "annual", "all"]     # 'difference' is derived
ROWS = ["nonannual", "annual", "difference", "all"]

# Strategy lag sets (A6). Lag k => month t-k.
LAG_SETS: dict[str, dict[str, list[int]]] = {
    "y1": {
        "nonannual": list(range(1, 12)),                          # 1..11
        "annual":    [12],
        "all":       list(range(1, 13)),                          # 1..12
    },
    "y23": {
        "nonannual": list(range(13, 24)) + list(range(25, 36)),   # 13..23, 25..35
        "annual":    [24, 36],
        "all":       list(range(13, 37)),                         # 13..36
    },
    "y45": {
        "nonannual": list(range(37, 48)) + list(range(49, 60)),   # 37..47, 49..59
        "annual":    [48, 60],
        "all":       list(range(37, 61)),                         # 37..60
    },
}

# Countries in PAPER ORDER. Panel country codes -> metric-name slug + label.
COUNTRY_ORDER = [
    ("AUT", "austria",     "Austria"),
    ("BEL", "belgium",     "Belgium"),
    ("CAN", "canada",      "Canada"),
    ("FIN", "finland",     "Finland"),
    ("FRA", "france",      "France"),
    ("DEU", "germany",     "Germany"),
    ("ITA", "italy",       "Italy"),
    ("JPN", "japan",       "Japan"),
    ("NLD", "netherlands", "Netherlands"),
    ("NOR", "norway",      "Norway"),
    ("ESP", "spain",       "Spain"),
    ("SWE", "sweden",      "Sweden"),
    ("CHE", "switzerland", "Switzerland"),
    ("GBR", "uk",          "United Kingdom"),
]
CODE_OF_SLUG = {slug: code for code, slug, _ in COUNTRY_ORDER}
SLUG_OF_CODE = {code: slug for code, slug, _ in COUNTRY_ORDER}
LABEL_OF_SLUG = {slug: label for _, slug, label in COUNTRY_ORDER}
COUNTRY_CODES = [code for code, _, _ in COUNTRY_ORDER]
COUNTRY_SLUGS = [slug for _, slug, _ in COUNTRY_ORDER]

GROUP_LABEL = {"y1": "Year 1 (Panel A)", "y23": "Years 2-3 (Panel B)",
               "y45": "Years 4-5 (Panel C)"}


# ────────────────────────────────────────────────────────────────────────────
# Data prep — build (gvkey x month-index) matrices for ret_usd and excess,
# plus the within-country row index sets.
# ────────────────────────────────────────────────────────────────────────────
def build_matrices(panel: pd.DataFrame) -> dict:
    """Returns dict with numpy matrices R (ret_usd) and E (arithmetic excess)
    indexed [gvkey-row x month-col], plus per-country row index arrays."""
    d = panel[["gvkey", "country", "month", "ret_usd"]].copy()
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

    # gvkey -> country map (A12: each gvkey lives under exactly one country).
    g_country = d.groupby("gvkey")["country"].unique()
    assert (g_country.str.len() == 1).all(), "gvkey under >1 country"
    country_row: dict[str, np.ndarray] = {c: [] for c in COUNTRY_CODES}
    for i, g in enumerate(gvkeys):
        c = g_country.loc[g][0]
        if c in country_row:
            country_row[c].append(i)
    country_rows = {c: np.array(v, dtype=int) for c, v in country_row.items()}

    print(f"Matrices: {n_firm:,} gvkeys x {n_month} months "
          f"(mi {mi_min}..{mi_max} = {mi_min//12}-{mi_min%12:02d} .. "
          f"{mi_max//12}-{mi_max%12:02d})")
    print(f"  ret_usd non-missing cells: {np.isfinite(R).sum():,}")
    print(f"  ex      non-missing cells: {np.isfinite(E).sum():,}")
    print("  per-country firm counts: " + ", ".join(
        f"{SLUG_OF_CODE[c]}={len(country_rows[c])}" for c in COUNTRY_CODES))

    return dict(R=R, E=E, mi_min=mi_min, mi_max=mi_max,
                n_month=n_month, n_firm=n_firm, country_rows=country_rows)


# ────────────────────────────────────────────────────────────────────────────
# Signal matrices — vectorized across all firms and months per lag set.
# ────────────────────────────────────────────────────────────────────────────
def compute_signals(E: np.ndarray) -> dict[tuple[str, str], np.ndarray]:
    """For each (group, strategy), the excess-signal matrix SIG[i,t] = mean of
    ex[i,t-k] over k in the lag set (over available lags; NaN if none)."""
    n_firm, n_month = E.shape
    SIG: dict[tuple[str, str], np.ndarray] = {}
    for group in GROUPS:
        for strategy in STRATEGIES:
            lags = LAG_SETS[group][strategy]
            num = np.zeros((n_firm, n_month), dtype=float)
            cnt = np.zeros((n_firm, n_month), dtype=float)
            for k in lags:
                if k >= n_month:          # lag longer than available history
                    continue
                shifted = np.full((n_firm, n_month), np.nan)
                shifted[:, k:] = E[:, :n_month - k]
                fin = np.isfinite(shifted)
                num += np.where(fin, shifted, 0.0)
                cnt += fin
            sig = np.where(cnt > 0, num / np.maximum(cnt, 1.0), np.nan)
            SIG[(group, strategy)] = sig
            print(f"  signal {group}/{strategy:9s} ({len(lags):2d} lags): "
                  f"non-missing signal cells = {np.isfinite(sig).sum():,}")
    return SIG


# ────────────────────────────────────────────────────────────────────────────
# Within-country decile spread for one cross-section.
# ────────────────────────────────────────────────────────────────────────────
def country_spread(sig: np.ndarray, ret_t: np.ndarray) -> tuple[float, int, int, int] | None:
    """Sort candidates (non-missing signal AND ret_t) within one country into
    deciles; return (spread, N, n_D1, n_D10) or None if either extreme decile
    is empty."""
    cand = np.isfinite(sig) & np.isfinite(ret_t)
    idx = np.where(cand)[0]
    N = int(idx.size)
    if N < 2:
        return None
    s = sig[idx]
    ranks = rankdata(s, method="average")
    decile = np.clip(np.ceil(10.0 * ranks / N), 1, 10).astype(int)
    m1 = decile == 1
    m10 = decile == 10
    if not (m1.any() and m10.any()):
        return None
    rt = ret_t[idx]
    spread = float(rt[m10].mean() - rt[m1].mean())
    return spread, N, int(m1.sum()), int(m10.sum())


# ────────────────────────────────────────────────────────────────────────────
# Main computation — loop over sort months, accumulate per-country spread series
# ────────────────────────────────────────────────────────────────────────────
def compute_table7(mat: dict, SIG: dict) -> tuple[dict, dict, dict]:
    """Returns:
      series[(group,strategy,country_code)] = {month_idx: spread}
      T[(group,row,country_code)] = feasible month count (row incl. 'difference')
      fill[(group,country_code)] = dict(min_N, min_D1, min_D10) over all sorts
    """
    R = mat["R"]
    mi_min, mi_max = mat["mi_min"], mat["mi_max"]
    country_rows = mat["country_rows"]

    series: dict = defaultdict(dict)
    fill: dict = {
        (g, c): {"min_N": np.inf, "min_D1": np.inf, "min_D10": np.inf}
        for g in GROUPS for c in COUNTRY_CODES
    }

    sort_months = list(range(SORT_LO, SORT_HI + 1))
    for n, t in enumerate(sort_months):
        t_col = t - mi_min
        if not (0 <= t_col < R.shape[1]):
            continue
        ret_t = R[:, t_col]

        for group in GROUPS:
            for strategy in STRATEGIES:
                sig = SIG[(group, strategy)][:, t_col]
                for code in COUNTRY_CODES:
                    rows = country_rows[code]
                    if rows.size == 0:
                        continue
                    res = country_spread(sig[rows], ret_t[rows])
                    if res is None:
                        continue
                    spread, N, nD1, nD10 = res
                    series[(group, strategy, code)][t] = spread
                    f = fill[(group, code)]
                    f["min_N"] = min(f["min_N"], N)
                    f["min_D1"] = min(f["min_D1"], nD1)
                    f["min_D10"] = min(f["min_D10"], nD10)

        if (n + 1) % 50 == 0:
            print(f"  processed {n + 1}/{len(sort_months)} sort months")

    # Feasible-month counts T per (group, row, country).
    T: dict = {}
    for group in GROUPS:
        for code in COUNTRY_CODES:
            for strategy in STRATEGIES:
                T[(group, strategy, code)] = len(series[(group, strategy, code)])
            ann = series[(group, "annual", code)]
            non = series[(group, "nonannual", code)]
            T[(group, "difference", code)] = len(set(ann.keys()) & set(non.keys()))

    return series, T, fill


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
    """Build the flat {metric_name: value} dict for all 336 T7 metrics."""
    cells: dict[str, float] = {}
    for group in GROUPS:
        panel = PANEL_OF_GROUP[group]
        for code in COUNTRY_CODES:
            slug = SLUG_OF_CODE[code]
            for strategy in STRATEGIES:
                m, tstat, _ = ts_stats(series[(group, strategy, code)])
                cells[f"t7_{panel}_{group}_{strategy}_{slug}_ret"] = m
                cells[f"t7_{panel}_{group}_{strategy}_{slug}_tstat"] = tstat
            # difference row: annual - nonannual over common months
            ann = series[(group, "annual", code)]
            non = series[(group, "nonannual", code)]
            common = set(ann.keys()) & set(non.keys())
            diff = {mo: ann[mo] - non[mo] for mo in common}
            m, tstat, _ = ts_stats(diff)
            cells[f"t7_{panel}_{group}_difference_{slug}_ret"] = m
            cells[f"t7_{panel}_{group}_difference_{slug}_tstat"] = tstat
    return cells


# ────────────────────────────────────────────────────────────────────────────
# Output writers
# ────────────────────────────────────────────────────────────────────────────
def load_paper_values() -> tuple[dict, list[str]]:
    tables = json.loads(TABLES_JSON.read_text())["tables"]
    pv, names = {}, []
    for t in tables:
        if t["id"] == "T7":
            for m in t["metrics"]:
                pv[m["name"]] = m["value"]
                names.append(m["name"])
    return pv, names


def write_table7_md(cells: dict, T: dict, fill: dict, paper: dict) -> None:
    lines = [
        "# Table 7 — Seasonality by Country: EW Top-minus-Bottom Decile Spreads",
        "",
        "Heston & Sadka (2010), Table 7. Within-country EW decile spreads",
        "(D10 - D1) on USD returns, sorted each month t in 1985-02..2006-06 on",
        "the lag-set average of arithmetic country-excess returns, computed",
        "SEPARATELY within each of the 14 countries. Panel A = Year 1, Panel B =",
        "Years 2-3, Panel C = Years 4-5. Our values with paper values in",
        "parentheses. t-stat = mean/(std/sqrt(T)); for the difference row the",
        "series is annual[t] - nonannual[t] over months where both exist.",
        "",
    ]

    col_header = "| Row | " + " | ".join(LABEL_OF_SLUG[s] for s in COUNTRY_SLUGS) + " |"
    sep = "|---" * (len(COUNTRY_SLUGS) + 1) + "|"

    for group in GROUPS:
        panel = PANEL_OF_GROUP[group]
        lines += ["", f"## {GROUP_LABEL[group]}", "", col_header, sep]
        for row in ROWS:
            r_cells = []
            t_cells = []
            for slug in COUNTRY_SLUGS:
                our_r = cells[f"t7_{panel}_{group}_{row}_{slug}_ret"]
                our_t = cells[f"t7_{panel}_{group}_{row}_{slug}_tstat"]
                p_r = paper.get(f"t7_{panel}_{group}_{row}_{slug}_ret")
                p_t = paper.get(f"t7_{panel}_{group}_{row}_{slug}_tstat")
                r_cells.append(f"{our_r:+.4f} ({p_r:+.4f})")
                t_cells.append(f"{our_t:+.2f} ({p_t:+.2f})")
            lines.append(f"| {row} ret | " + " | ".join(r_cells) + " |")
            lines.append(f"| {row} t   | " + " | ".join(t_cells) + " |")

    # T (feasible months) for the y23 difference row, per country.
    lines += ["",
              "## Feasible months T — Panel B (Years 2-3) difference row, per country",
              "",
              "| Country | T (difference) | min N | min D1 | min D10 |",
              "|---|---|---|---|---|"]
    for code in COUNTRY_CODES:
        slug = SLUG_OF_CODE[code]
        Tval = T[("y23", "difference", code)]
        f = fill[("y23", code)]
        mn = int(f["min_N"]) if np.isfinite(f["min_N"]) else 0
        md1 = int(f["min_D1"]) if np.isfinite(f["min_D1"]) else 0
        md10 = int(f["min_D10"]) if np.isfinite(f["min_D10"]) else 0
        lines.append(f"| {LABEL_OF_SLUG[slug]} | {Tval} | {mn} | {md1} | {md10} |")

    (RESULTS_DIR / "table_7.md").write_text("\n".join(lines) + "\n")


def write_cells_json(cells: dict, metric_names: list[str]) -> dict:
    """Emit flat {metric_name: value} covering EVERY T7 name in the spec file."""
    out: dict = {}
    nonfinite = []
    for name in metric_names:
        v = cells.get(name, float("nan"))
        if not np.isfinite(v):
            nonfinite.append(name)
        out[name] = float(v) if np.isfinite(v) else None
    (RESULTS_DIR / "cells_t7.json").write_text(
        json.dumps(out, indent=2) + "\n")
    if nonfinite:
        print(f"  WARNING: {len(nonfinite)} non-finite T7 cells -> null: "
              f"{nonfinite[:10]}{'...' if len(nonfinite) > 10 else ''}")
    return out


def write_plot(cells: dict, paper: dict) -> None:
    # Panel B (Years 2-3) difference row, one bar per country, paper overlaid.
    ours = [cells[f"t7_panelB_y23_difference_{s}_ret"] for s in COUNTRY_SLUGS]
    paps = [paper[f"t7_panelB_y23_difference_{s}_ret"] for s in COUNTRY_SLUGS]
    x = np.arange(len(COUNTRY_SLUGS))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x, ours, width=0.6, color="#1f77b4", alpha=0.85,
           label="ours", edgecolor="black", linewidth=0.4)
    ax.scatter(x, paps, marker="D", s=60, facecolors="none",
               edgecolors="#d62728", linewidths=1.8, zorder=5, label="paper")
    ax.axhline(0.0, color="grey", lw=0.9, ls="--")
    ax.set_xticks(x)
    ax.set_xticklabels([LABEL_OF_SLUG[s] for s in COUNTRY_SLUGS],
                       rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("Annual-minus-nonannual D10-D1 monthly spread (decimal)")
    ax.set_title("Years 2-3 annual-minus-nonannual spread by country "
                 "(ours vs paper)")
    ax.legend(ncol=2, fontsize=9, loc="best")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "table7_y23_difference_by_country.png", dpi=150)
    plt.close(fig)


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Loading panel: {PANEL_PATH}")
    panel = pd.read_parquet(PANEL_PATH)
    print(f"Panel: {len(panel):,} rows x {panel.shape[1]} cols, "
          f"months {panel['month'].min().date()}..{panel['month'].max().date()}")

    paper, metric_names = load_paper_values()
    print(f"T7 metric names from tables_to_replicate.json: {len(metric_names)}")
    assert len(metric_names) == 336, len(metric_names)

    mat = build_matrices(panel)

    print("\n=== Table 7 — signals (excess-return, vectorized) ===")
    SIG = compute_signals(mat["E"])

    print("\n=== Table 7 — within-country sorting + spreads ===")
    series, T, fill = compute_table7(mat, SIG)

    cells = assemble_cells(series)
    out = write_cells_json(cells, metric_names)
    write_table7_md(cells, T, fill, paper)
    write_plot(cells, paper)

    # ---- console spot checks ----
    def show(panel, group, row, slug):
        our_r = cells[f"t7_{panel}_{group}_{row}_{slug}_ret"]
        our_t = cells[f"t7_{panel}_{group}_{row}_{slug}_tstat"]
        p_r = paper.get(f"t7_{panel}_{group}_{row}_{slug}_ret")
        p_t = paper.get(f"t7_{panel}_{group}_{row}_{slug}_tstat")
        code = CODE_OF_SLUG[slug]
        Tval = T[(group, row, code)]
        print(f"  {panel} {group} {row:10s} {slug:12s} "
              f"ret={our_r:+.4f} ({p_r:+.4f})  t={our_t:+.2f} ({p_t:+.2f})  T={Tval}")

    print("\n=== Panel A Y1 annual + nonannual (spot countries) ===")
    for slug in ["japan", "germany", "canada", "uk", "austria"]:
        show("panelA", "y1", "annual", slug)
        show("panelA", "y1", "nonannual", slug)

    print("\n=== Panel B Y23 difference (all countries): ours vs paper ===")
    for slug in COUNTRY_SLUGS:
        show("panelB", "y23", "difference", slug)

    print("\n=== Panel C Y45 difference (all countries): ours vs paper ===")
    for slug in COUNTRY_SLUGS:
        show("panelC", "y45", "difference", slug)

    # T range for y23 difference; min within-country decile fills
    t_y23 = [T[("y23", "difference", c)] for c in COUNTRY_CODES]
    print(f"\ny23 difference T across countries: min={min(t_y23)} "
          f"max={max(t_y23)}  (per country: "
          + ", ".join(f"{SLUG_OF_CODE[c]}={T[('y23','difference',c)]}"
                      for c in COUNTRY_CODES) + ")")
    print("min within-country decile fills (over all sorts), per group:")
    for group in GROUPS:
        minD1 = min(int(fill[(group, c)]["min_D1"]) for c in COUNTRY_CODES
                    if np.isfinite(fill[(group, c)]["min_D1"]))
        minD10 = min(int(fill[(group, c)]["min_D10"]) for c in COUNTRY_CODES
                     if np.isfinite(fill[(group, c)]["min_D10"]))
        minN = min(int(fill[(group, c)]["min_N"]) for c in COUNTRY_CODES
                   if np.isfinite(fill[(group, c)]["min_N"]))
        print(f"  {group}: min N={minN}, min D1={minD1}, min D10={minD10}")

    n_nonfinite = sum(1 for v in out.values() if v is None)
    print(f"\nWrote: table_7.md, cells_t7.json ({len(out)} names, "
          f"{n_nonfinite} null), table7_y23_difference_by_country.png")


if __name__ == "__main__":
    main()
