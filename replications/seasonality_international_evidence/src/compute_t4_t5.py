"""
Heston & Sadka (2010), "Seasonality in the Cross Section of Stock Returns:
The International Evidence" — TABLE 4 (calendar-month decomposition of the
EW Panel A decile-spread series) and TABLE 5 (EW Panel A decile spreads
within monthly 30/40/30 USD size groups, intracountry and intercountry
breakpoints).

Consumes the cached analysis-ready panel (data/panel.parquet, READ-ONLY;
columns gvkey, country, curcdd, month, ret_local, ret_usd, me_usd) and writes:

  results/table_4.md     — three panels (A = Year 1, B = Years 2-3, C = Years
                           4-5), rows nonannual/annual/difference/all, columns
                           Jan..Dec plus Feb-Dec; our values with paper values
                           in parentheses (returns, then t-stats), plus the
                           paper's L1178-1182 corollary check.
  results/cells_t4.json  — flat {metric_name: our_value} for all 312 T4 names.
  results/table_5.md     — three year-group panels, rows nonannual/annual/
                           difference/all, six size columns (intra/inter x
                           small/medium/large); our values with paper in
                           parentheses, plus the paper's L1204 claim check.
  results/cells_t5.json  — flat {metric_name: our_value} for all 144 T5 names.

Methodology (fixed by the Replicator — task spec + assumptions.md A5-A7/A11).
Both tables reuse the VERIFIED pooled EW Panel A decile-sort engine of
src/compute_t3.py (imported below — build_matrices for R/E/ME, the lag sets,
and sort_spreads for the rank/decile/spread mechanics); nothing in
compute_t3.py is modified.

All definitions on USD returns (ret_usd).

  Country EW benchmark  rbar[c,t] = simple mean of ret_usd over firms of
                        country c in month t.
  Arithmetic excess     ex[i,t] = ret_usd[i,t] - rbar[country(i),t]     (A5)
  Panel A signal at sort month t = mean of ex[i,t-k] over k in the lag set
                        (average over non-missing lags; missing if none).
  Pooled decile sort (A7): candidates = non-missing signal AND ret_usd[t];
  ascending ranks (average ranks for ties); decile = ceil(10*rank/N) in
  [1,10]; EW spread[t] = mean(ret_usd[t] in D10) - mean(ret_usd[t] in D1).

Strategy lag sets (A6) and the difference row (annual[t] - nonannual[t] on
common months) are exactly Table 3's.

TABLE 4: for each (year-group panel) x (row), the monthly spread series
spread[t] over t = 1985-02..2006-06 is averaged SEPARATELY per calendar
month: Jan..Dec columns (all sort months with that month-of-year), plus a
Feb-Dec column (all months except January). Each column reports the mean and
iid t-stat (mean/(std/sqrt(T)), T = available months in that calendar-month
subset). 3 panels x 4 rows x 13 columns x 2 (ret/tstat) = 312 metrics.
Panel convention: Panel A = Year 1, Panel B = Years 2-3, Panel C = Years 4-5
(the paper's Table 4 layout).

TABLE 5: monthly 30/40/30 USD size groups, re-evaluated at the beginning of
every month (paper L1218): at sort month t, size = me_usd at month t-1
(non-missing and > 0; firms without a valid prior-month size are not size-
classified that month). Two breakpoint conventions, both computed:
  intra  — bottom 30% / middle 40% / top 30% of me_usd WITHIN each country
           (per-country 30th/70th percentiles at t-1; small: me <= q30,
           medium: q30 < me <= q70, large: me > q70).
  inter  — the same 30/40/30 quantiles of the POOLED cross-section at t-1.
Within each size group (per convention), the EW Panel A decile sorts are run
on the firms of that group, deciles formed within the month's size group and
pooled across countries, producing nonannual/annual/difference/all spread
series for each year-group panel. 3 panels x 4 rows x 6 size columns x 2
(ret/tstat) = 144 metrics.

Usage:  python3 src/compute_t4_t5.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import compute_t3 as t3  # verified engine: matrices, lag sets, sort mechanics

# ────────────────────────────────────────────────────────────────────────────
# Paths & constants
# ────────────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
PANEL_PATH = ROOT / "data" / "panel.parquet"
RESULTS_DIR = ROOT / "results"
TABLES_JSON = ROOT / "preparations" / "tables_to_replicate.json"

SORT_LO = t3.SORT_LO                      # 1985-02
SORT_HI = t3.SORT_HI                      # 2006-06
GROUPS = t3.GROUPS                        # ["y1", "y23", "y45"]
STRATEGIES = t3.STRATEGIES                # ["nonannual", "annual", "all"]
LAG_COLS = t3.LAG_COLS
ROWS = ["nonannual", "annual", "difference", "all"]

# Table 4/5 panel convention (paper layout): Panel A = Year 1, etc.
PANEL_OF_GROUP = {"y1": "panela", "y23": "panelb", "y45": "panelc"}
GROUP_LABEL = {"y1": "Panel A — Year 1", "y23": "Panel B — Years 2-3",
               "y45": "Panel C — Years 4-5"}

MONTH_TOKEN = {1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "jun",
               7: "jul", 8: "aug", 9: "sep", 10: "oct", 11: "nov", 12: "dec"}
MONTH_TOKENS = [MONTH_TOKEN[m] for m in range(1, 13)] + ["feb_dec"]
MONTH_COL_LABEL = {**{MONTH_TOKEN[m]: MONTH_TOKEN[m].capitalize()
                      for m in range(1, 13)},
                   "feb_dec": "Feb-Dec"}

SIZE_TOKEN = {0: "small", 1: "medium", 2: "large"}
SIZE_COLS = ["intra_small", "intra_medium", "intra_large",
             "inter_small", "inter_medium", "inter_large"]

COUNTRY_CODES = ["AUT", "BEL", "CAN", "FIN", "FRA", "DEU", "ITA", "JPN",
                 "NLD", "NOR", "ESP", "SWE", "CHE", "GBR"]


def moy_of(t: int) -> int:
    """Month-of-year of month-index t = year*12 + moy."""
    return (t - 1) % 12 + 1


# ────────────────────────────────────────────────────────────────────────────
# Per-country row index (same mechanics as compute_t7.build_matrices)
# ────────────────────────────────────────────────────────────────────────────
def build_country_rows(panel: pd.DataFrame, gvkeys: pd.Index) -> dict:
    g_country = panel.groupby("gvkey")["country"].unique()
    assert (g_country.str.len() == 1).all(), "gvkey under >1 country"
    country_row: dict[str, list[int]] = {c: [] for c in COUNTRY_CODES}
    for i, g in enumerate(gvkeys):
        c = g_country.loc[g][0]
        if c in country_row:
            country_row[c].append(i)
    return {c: np.array(v, dtype=int) for c, v in country_row.items()}


# ────────────────────────────────────────────────────────────────────────────
# Size classes at month t from me_usd at t-1 (30/40/30 breakpoints)
# ────────────────────────────────────────────────────────────────────────────
def size_classes(me_prev: np.ndarray, country_rows: dict,
                 n_firm: int) -> tuple[np.ndarray, np.ndarray]:
    """Return (cls_intra, cls_inter), each an int array of length n_firm with
    0=small, 1=medium, 2=large, -1=not classifiable (me_usd at t-1 missing or
    <= 0). Intra breakpoints are per-country 30/70 percentiles; inter
    breakpoints are the pooled-cross-section 30/70 percentiles. Assignment:
    small: me <= q30; medium: q30 < me <= q70; large: me > q70
    (np.searchsorted([q30, q70], me, side='left'))."""
    cls_intra = np.full(n_firm, -1, dtype=int)
    cls_inter = np.full(n_firm, -1, dtype=int)

    for code in COUNTRY_CODES:
        rows = country_rows[code]
        if rows.size == 0:
            continue
        v = me_prev[rows]
        valid = np.isfinite(v) & (v > 0)
        if valid.sum() < 2:
            continue
        q30, q70 = np.percentile(v[valid], [30, 70])
        cls = np.searchsorted([q30, q70], v, side="left")
        assign = rows[valid]
        cls_intra[assign] = cls[valid]

    valid = np.isfinite(me_prev) & (me_prev > 0)
    if valid.sum() >= 2:
        q30, q70 = np.percentile(me_prev[valid], [30, 70])
        cls_inter[valid] = np.searchsorted([q30, q70], me_prev[valid],
                                           side="left")
    return cls_intra, cls_inter


# ────────────────────────────────────────────────────────────────────────────
# Main computation — one loop over sort months feeding both tables
# ────────────────────────────────────────────────────────────────────────────
def compute_tables(mat: dict, country_rows: dict) -> tuple[dict, dict]:
    """Returns:
      series_t4[(group,strategy)] = {month_idx: pooled EW Panel A total spread}
      series_t5[(conv,size,group,strategy)] = {month_idx: EW spread within the
                                               (convention, size group) pool}
    Identical EW Panel A mechanics to compute_t3.compute_table3 (same signal
    construction, same sort_spreads call), EW/total only.
    """
    R, E, ME = mat["R"], mat["E"], mat["ME"]
    mi_min, mi_max = mat["mi_min"], mat["mi_max"]
    n_firm, n_month = mat["n_firm"], mat["n_month"]

    # Sentinel all-NaN column so out-of-range lag lookups map to NaN.
    sentinel = n_month
    E_s = np.concatenate([E, np.full((n_firm, 1), np.nan)], axis=1)

    def lag_index(t: int, k: int) -> int:
        c = t - k
        return (c - mi_min) if (mi_min <= c <= mi_max) else sentinel

    series_t4: dict = defaultdict(dict)
    series_t5: dict = defaultdict(dict)
    w_nan = np.full(n_firm, np.nan)     # VW unused: NaN weights -> VW = NaN

    sort_months = list(range(SORT_LO, SORT_HI + 1))
    for n, t in enumerate(sort_months):
        t_col = (t - mi_min) if (mi_min <= t <= mi_max) else None
        if t_col is None:
            continue
        ret_t = R[:, t_col]
        ex_t = E[:, t_col]

        # Size classes from me_usd at t-1 (A5/Table 5, monthly re-evaluation).
        me_prev = (ME[:, (t - 1 - mi_min)] if (mi_min <= t - 1 <= mi_max)
                   else np.full(n_firm, np.nan))
        cls_intra, cls_inter = size_classes(me_prev, country_rows, n_firm)

        # Panel A lag block (lags 1..60 -> columns), exactly as compute_t3.
        idx60 = np.array([lag_index(t, k) for k in range(1, 61)], dtype=int)
        block_E = E_s[:, idx60]

        for group in GROUPS:
            for strategy in STRATEGIES:
                cols = LAG_COLS[group][strategy]
                sub = block_E[:, cols]
                nanmask = np.isnan(sub)
                cnt = sub.shape[1] - nanmask.sum(axis=1)
                s = np.where(nanmask, 0.0, sub).sum(axis=1)
                signal = np.where(cnt > 0, s / np.maximum(cnt, 1), np.nan)

                # Table 4: pooled 14-country sort (== compute_t3 EW total).
                res = t3.sort_spreads(signal, ret_t, ex_t, w_nan)
                if res is not None and np.isfinite(res["ew"]["total"]):
                    series_t4[(group, strategy)][t] = res["ew"]["total"]

                # Table 5: sorts within each (convention, size group), pooled
                # across countries; same rank/decile mechanics via sort_spreads.
                for conv, cls in (("intra", cls_intra), ("inter", cls_inter)):
                    for sz in (0, 1, 2):
                        idx = np.where(np.isfinite(signal) & np.isfinite(ret_t)
                                       & (cls == sz))[0]
                        if idx.size < 2:
                            continue
                        r = t3.sort_spreads(signal[idx], ret_t[idx],
                                            ex_t[idx], w_nan[: idx.size])
                        if r is not None and np.isfinite(r["ew"]["total"]):
                            series_t5[(conv, sz, group, strategy)][t] = \
                                r["ew"]["total"]

        if (n + 1) % 50 == 0:
            print(f"  processed {n + 1}/{len(sort_months)} sort months")

    return series_t4, series_t5


def difference_series(ann: dict, non: dict) -> dict:
    common = set(ann.keys()) & set(non.keys())
    return {mo: ann[mo] - non[mo] for mo in common}


# ────────────────────────────────────────────────────────────────────────────
# Cells assembly
# ────────────────────────────────────────────────────────────────────────────
def calendar_stats(vals: dict, month: int | None) -> tuple[float, float, int]:
    """Mean + iid t-stat over the subset of months with month-of-year == month
    (month=None => all months except January, the Feb-Dec column)."""
    if month is None:
        sub = {t: v for t, v in vals.items() if moy_of(t) != 1}
    else:
        sub = {t: v for t, v in vals.items() if moy_of(t) == month}
    return t3.ts_stats(sub)


def assemble_t4_cells(series_t4: dict) -> dict[str, float]:
    cells: dict[str, float] = {}
    for group in GROUPS:
        panel = PANEL_OF_GROUP[group]
        for row in ROWS:
            s = (difference_series(series_t4[(group, "annual")],
                                   series_t4[(group, "nonannual")])
                 if row == "difference" else series_t4[(group, row)])
            for m in range(1, 13):
                mean, tstat, _ = calendar_stats(s, m)
                cells[f"t4_{panel}_{group}_{row}_{MONTH_TOKEN[m]}_ret"] = mean
                cells[f"t4_{panel}_{group}_{row}_{MONTH_TOKEN[m]}_tstat"] = tstat
            mean, tstat, _ = calendar_stats(s, None)   # Feb-Dec
            cells[f"t4_{panel}_{group}_{row}_feb_dec_ret"] = mean
            cells[f"t4_{panel}_{group}_{row}_feb_dec_tstat"] = tstat
    return cells


def assemble_t5_cells(series_t5: dict) -> dict[str, float]:
    cells: dict[str, float] = {}
    for group in GROUPS:
        panel = PANEL_OF_GROUP[group]
        for conv, sz in [("intra", 0), ("intra", 1), ("intra", 2),
                         ("inter", 0), ("inter", 1), ("inter", 2)]:
            col = f"{conv}_{SIZE_TOKEN[sz]}"
            for row in ROWS:
                s = (difference_series(series_t5[(conv, sz, group, "annual")],
                                       series_t5[(conv, sz, group, "nonannual")])
                     if row == "difference"
                     else series_t5[(conv, sz, group, row)])
                mean, tstat, _ = t3.ts_stats(s)
                cells[f"t5_{panel}_{group}_{row}_{col}_ret"] = mean
                cells[f"t5_{panel}_{group}_{row}_{col}_tstat"] = tstat
    return cells


# ────────────────────────────────────────────────────────────────────────────
# Spec loading, coverage check, JSON output
# ────────────────────────────────────────────────────────────────────────────
def load_table(tid: str) -> tuple[dict, list[str]]:
    tables = json.loads(TABLES_JSON.read_text())["tables"]
    pv, names = {}, []
    for t in tables:
        if t["id"] == tid:
            for m in t["metrics"]:
                pv[m["name"]] = m["value"]
                names.append(m["name"])
    return pv, names


def write_cells_json(cells: dict, metric_names: list[str], path: Path,
                     label: str) -> dict:
    """Coverage check (set-diff vs committed names) + finiteness assertion +
    flat JSON write."""
    committed = set(metric_names)
    produced = set(cells.keys())
    missing = committed - produced
    extra = produced - committed
    assert not missing, f"{label}: missing cells {sorted(missing)[:10]}"
    assert not extra, f"{label}: extra cells {sorted(extra)[:10]}"
    out: dict = {}
    for name in metric_names:
        v = cells[name]
        assert np.isfinite(v), f"non-finite {label} cell {name} = {v}"
        out[name] = float(v)
    path.write_text(json.dumps(out, indent=2, allow_nan=False) + "\n")
    print(f"  {label}: coverage OK — {len(out)}/{len(metric_names)} committed "
          f"names, 0 missing, 0 extra, all finite")
    return out


# ────────────────────────────────────────────────────────────────────────────
# Table 4 markdown
# ────────────────────────────────────────────────────────────────────────────
def write_table4_md(cells: dict, paper: dict) -> None:
    lines = [
        "# Table 4 — Seasonality by Calendar Month: EW Panel A Decile Spreads",
        "",
        "Heston & Sadka (2010), Table 4. The monthly pooled EW Panel A decile",
        "spread series (D10 - D1 on USD returns, sorted on the lag-set average",
        "of arithmetic country-excess returns; identical engine to Table 3),",
        "averaged SEPARATELY per calendar month over t = 1985-02..2006-06.",
        "Feb-Dec = all months except January. Panel A = Year 1, Panel B =",
        "Years 2-3, Panel C = Years 4-5. Our values with paper values in",
        "parentheses. t-stat = mean/(std/sqrt(T)), T = available months in the",
        "calendar-month subset.",
        "",
    ]
    header = "| Row | " + " | ".join(MONTH_COL_LABEL[m] for m in MONTH_TOKENS) + " |"
    sep = "|---" * (len(MONTH_TOKENS) + 1) + "|"

    for group in GROUPS:
        panel = PANEL_OF_GROUP[group]
        lines += ["", f"## {GROUP_LABEL[group]}", ""]
        for stat, stat_label in [("ret", "Average monthly spread"),
                                 ("tstat", "t-statistic")]:
            lines += [f"### {stat_label}", "", header, sep]
            for row in ROWS:
                row_cells = []
                for m in MONTH_TOKENS:
                    our = cells[f"t4_{panel}_{group}_{row}_{m}_{stat}"]
                    pap = paper.get(f"t4_{panel}_{group}_{row}_{m}_{stat}")
                    if pap is None:
                        row_cells.append(f"{our:+.4f}")
                    else:
                        row_cells.append(f"{our:+.4f} ({pap:+.4f})")
                lines.append(f"| {row} | " + " | ".join(row_cells) + " |")
            lines.append("")

    # Corollary check — paper L1178-1182.
    lines += ["## Corollary check (paper L1178-1182)",
              "",
              "Paper claim: the Years 2-3 and Years 4-5 ANNUAL spreads are",
              "positive in almost every calendar month; the NONANNUAL spreads",
              "are negative in most months; the Feb-Dec column is significant",
              "(i.e. the pattern is not a January/turn-of-year effect).",
              "",
              "| Panel | Row | Months positive (of 12) | Months negative "
              "(of 12) | Feb-Dec ret (t) |",
              "|---|---|---|---|---|"]
    for group in ["y23", "y45"]:
        panel = PANEL_OF_GROUP[group]
        for row in ["annual", "nonannual", "difference"]:
            rets = [cells[f"t4_{panel}_{group}_{row}_{MONTH_TOKEN[m]}_ret"]
                    for m in range(1, 13)]
            n_pos = sum(r > 0 for r in rets)
            n_neg = sum(r < 0 for r in rets)
            fd_r = cells[f"t4_{panel}_{group}_{row}_feb_dec_ret"]
            fd_t = cells[f"t4_{panel}_{group}_{row}_feb_dec_tstat"]
            lines.append(f"| {GROUP_LABEL[group]} | {row} | {n_pos} | {n_neg} "
                         f"| {fd_r:+.4f} ({fd_t:+.2f}) |")
    (RESULTS_DIR / "table_4.md").write_text("\n".join(lines) + "\n")


# ────────────────────────────────────────────────────────────────────────────
# Table 5 markdown
# ────────────────────────────────────────────────────────────────────────────
def write_table5_md(cells: dict, paper: dict) -> None:
    lines = [
        "# Table 5 — Seasonality by Size Group: EW Panel A Decile Spreads",
        "",
        "Heston & Sadka (2010), Table 5. Monthly 30/40/30 USD size groups",
        "(market cap in USD), re-evaluated at the beginning of every month:",
        "at sort month t, size = me_usd at t-1 (non-missing, > 0). Intra =",
        "bottom 30% / middle 40% / top 30% of me_usd WITHIN each country",
        "(per-country 30th/70th percentiles at t-1); Inter = the same 30/40/30",
        "quantiles of the POOLED cross-section. Within each size group, the EW",
        "Panel A decile sorts (identical signals/mechanics to Table 3) are run",
        "on the group's firms, deciles formed within the size group and pooled",
        "across countries. Panel A = Year 1, Panel B = Years 2-3, Panel C =",
        "Years 4-5. Our values with paper values in parentheses. t-stat =",
        "mean/(std/sqrt(T)); for the difference row the series is annual[t] -",
        "nonannual[t] over months where both exist.",
        "",
    ]
    header = "| Row | " + " | ".join(SIZE_COLS) + " |"
    sep = "|---" * (len(SIZE_COLS) + 1) + "|"

    for group in GROUPS:
        panel = PANEL_OF_GROUP[group]
        lines += ["", f"## {GROUP_LABEL[group]}", ""]
        for stat, stat_label in [("ret", "Average monthly spread"),
                                 ("tstat", "t-statistic")]:
            lines += [f"### {stat_label}", "", header, sep]
            for row in ROWS:
                row_cells = []
                for col in SIZE_COLS:
                    our = cells[f"t5_{panel}_{group}_{row}_{col}_{stat}"]
                    pap = paper.get(f"t5_{panel}_{group}_{row}_{col}_{stat}")
                    if pap is None:
                        row_cells.append(f"{our:+.4f}")
                    else:
                        row_cells.append(f"{our:+.4f} ({pap:+.4f})")
                lines.append(f"| {row} | " + " | ".join(row_cells) + " |")
            lines.append("")

    # Claim check — paper L1204.
    lines += ["## Claim check (paper L1204)",
              "",
              "Paper claim: all NONANNUAL strategies lose money in every size",
              "group; all ANNUAL strategies earn money in every group; the",
              "Years 4-5 annual strategy is slightly stronger in large stocks.",
              "",
              "| Panel | Row | # of 6 size groups with positive spread | "
              "Groups negative |",
              "|---|---|---|---|"]
    for group in GROUPS:
        panel = PANEL_OF_GROUP[group]
        for row in ["nonannual", "annual"]:
            rets = {col: cells[f"t5_{panel}_{group}_{row}_{col}_ret"]
                    for col in SIZE_COLS}
            n_pos = sum(v > 0 for v in rets.values())
            neg = [c for c, v in rets.items() if v < 0]
            lines.append(f"| {GROUP_LABEL[group]} | {row} | {n_pos}/6 | "
                         f"{', '.join(neg) if neg else '—'} |")
    # Y45 annual: large vs smaller groups, per convention.
    lines += ["", "Years 4-5 annual spread by size (ours):", ""]
    for conv in ["intra", "inter"]:
        s = cells[f"t5_panelc_y45_annual_{conv}_small_ret"]
        m = cells[f"t5_panelc_y45_annual_{conv}_medium_ret"]
        l = cells[f"t5_panelc_y45_annual_{conv}_large_ret"]
        lines.append(f"- {conv}: small {s:+.4f}, medium {m:+.4f}, "
                     f"large {l:+.4f} (large stronger than small+medium mean: "
                     f"{l > (s + m) / 2})")
    (RESULTS_DIR / "table_5.md").write_text("\n".join(lines) + "\n")


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Loading panel: {PANEL_PATH}")
    panel = pd.read_parquet(PANEL_PATH)
    print(f"Panel: {len(panel):,} rows x {panel.shape[1]} cols, "
          f"months {panel['month'].min().date()}..{panel['month'].max().date()}")

    paper_t4, names_t4 = load_table("T4")
    paper_t5, names_t5 = load_table("T5")
    print(f"T4 committed names: {len(names_t4)}; T5 committed names: "
          f"{len(names_t5)}")
    assert len(names_t4) == 312 and len(names_t5) == 144

    mat = t3.build_matrices(panel)
    # Row order in the matrices built by compute_t3.build_matrices is
    # pd.unique over the panel's gvkey column; replicate exactly so the
    # per-country row indices align with the matrix rows.
    gvkeys = pd.Index(pd.unique(panel["gvkey"]))
    country_rows = build_country_rows(panel, gvkeys)

    print("\n=== Tables 4 & 5 — EW Panel A pooled + size-group sorts ===")
    series_t4, series_t5 = compute_tables(mat, country_rows)

    cells_t4 = assemble_t4_cells(series_t4)
    cells_t5 = assemble_t5_cells(series_t5)
    out4 = write_cells_json(cells_t4, names_t4, RESULTS_DIR / "cells_t4.json",
                            "cells_t4")
    out5 = write_cells_json(cells_t5, names_t5, RESULTS_DIR / "cells_t5.json",
                            "cells_t5")
    write_table4_md(cells_t4, paper_t4)
    write_table5_md(cells_t5, paper_t5)

    # ---- console spot checks vs paper ----
    def show(cells, paper, name):
        p = paper.get(name)
        ps = f"({p:+.4f})" if p is not None else "(   n/a)"
        print(f"  {name:52s} {cells[name]:+.4f} {ps}")

    print("\n=== T4 spot checks (ours vs paper) ===")
    for name in ["t4_panela_y1_nonannual_jan_ret",
                 "t4_panela_y1_nonannual_jan_tstat",
                 "t4_panela_y1_nonannual_feb_dec_ret",
                 "t4_panela_y1_nonannual_feb_dec_tstat",
                 "t4_panelb_y23_nonannual_jan_ret",
                 "t4_panelb_y23_nonannual_jan_tstat",
                 "t4_panelb_y23_annual_jan_ret",
                 "t4_panelb_y23_annual_jan_tstat",
                 "t4_panelc_y45_annual_jan_ret",
                 "t4_panelc_y45_annual_jan_tstat"]:
        show(cells_t4, paper_t4, name)

    print("\n=== T4 y23 Feb-Dec rows (ours vs paper) ===")
    for row in ["nonannual", "annual", "difference", "all"]:
        r, tt = (cells_t4[f"t4_panelb_y23_{row}_feb_dec_ret"],
                 cells_t4[f"t4_panelb_y23_{row}_feb_dec_tstat"])
        pr, pt = (paper_t4[f"t4_panelb_y23_{row}_feb_dec_ret"],
                  paper_t4[f"t4_panelb_y23_{row}_feb_dec_tstat"])
        print(f"  y23 {row:10s} Feb-Dec ret={r:+.4f} ({pr:+.4f})  "
              f"t={tt:+.2f} ({pt:+.2f})")

    print("\n=== T5 spot checks (ours vs paper) ===")
    for name in ["t5_panela_y1_nonannual_intra_small_ret",
                 "t5_panela_y1_nonannual_intra_small_tstat",
                 "t5_panela_y1_nonannual_intra_medium_ret",
                 "t5_panela_y1_nonannual_intra_medium_tstat",
                 "t5_panelb_y23_difference_intra_small_ret",
                 "t5_panelb_y23_difference_intra_small_tstat",
                 "t5_panelb_y23_difference_inter_large_ret",
                 "t5_panelb_y23_difference_inter_large_tstat",
                 "t5_panelc_y45_annual_inter_large_ret",
                 "t5_panelc_y45_annual_inter_large_tstat"]:
        show(cells_t5, paper_t5, name)

    print("\n=== T5 y23 difference across six size columns (ours vs paper) ===")
    for col in SIZE_COLS:
        r = cells_t5[f"t5_panelb_y23_difference_{col}_ret"]
        tt = cells_t5[f"t5_panelb_y23_difference_{col}_tstat"]
        pr = paper_t5[f"t5_panelb_y23_difference_{col}_ret"]
        pt = paper_t5[f"t5_panelb_y23_difference_{col}_tstat"]
        print(f"  {col:13s} ret={r:+.4f} ({pr:+.4f})  t={tt:+.2f} ({pt:+.2f})")

    print(f"\nWrote: table_4.md, cells_t4.json ({len(out4)} names), "
          f"table_5.md, cells_t5.json ({len(out5)} names)")


if __name__ == "__main__":
    main()
