"""
Heston & Sadka (2010), "Seasonality in the Cross Section of Stock Returns:
The International Evidence" — TABLE 11 (cross-country correlations of the
annual-strategy return series) and TABLE 12 (quintile/tricile robustness of
the EW Panel A strategy returns).

Consumes the cached analysis-ready panel (data/panel.parquet, READ-ONLY;
columns gvkey, country, curcdd, month, ret_local, ret_usd, me_usd) and writes:

  results/table_11_correlations.md — three 14x14 Pearson correlation matrices
                           (Year 1 / Years 2-3 / Years 4-5, 2 dp) of the
                           per-country EW Panel A ANNUAL-strategy monthly
                           spread series, the mean pairwise (off-diagonal)
                           correlation per panel, the fraction of pairs with
                           |rho| > 0.12 (the paper's 5% level, L3105), and the
                           paper's named-pair anchors.
  results/cells_t11.json — flat {metric_name: our_value} for the 11 committed
                           T11 names (named pairs from the matrices, the
                           text-reported extremes, and the 0.12 threshold).
  results/table_12_quintiles.md — three year-group panels with quintile
                           (Q1..Q5 + Q5-Q1) and tricile (T1..T3 + T3-T1)
                           EW Panel A bin means and spreads, ours with paper
                           in parentheses, plus the decile-sign robustness
                           check (paper L3601-3603).
  results/cells_t12.json — flat {metric_name: our_value} for all 240 T12 names.

Methodology (fixed by the Replicator — task spec + assumptions.md A5-A7/A11).
Both tables reuse the VERIFIED engines:

  Table 11 reuses src/compute_t7.py mechanics (imported below — build_matrices
  for R/E and the per-country row sets, country_spread for the within-country
  decile mechanics). Per-country monthly series = EW Panel A ANNUAL-strategy
  top-minus-bottom decile spread of ret_usd, deciles formed within each
  country exactly as Table 7 (ascending average ranks, ceil(10*rank/N)). The
  14x14 matrix entries are Pearson correlations over common (pairwise-
  complete) months.

  Table 12 reuses src/compute_t3.py mechanics (imported below — build_matrices
  for R/E, the lag sets, ts_stats): pooled EW Panel A sorts with n_bins in
  {5, 3}, bin = ceil(n_bins*rank/N) clipped to [1, n_bins], the same
  ascending average-rank ordering as compute_t3.sort_spreads. Reported items:
  the average ret_usd of each bin (Q1..Q5 / T1..T3) and the top-minus-bottom
  spreads (Q5-Q1 / T3-T1), for rows nonannual/annual/difference/all in each
  year-group panel (Panel A = Year 1, Panel B = Years 2-3, Panel C =
  Years 4-5); the difference row is annual[t] - nonannual[t] on common months,
  for bin means and spreads alike. t-stat = mean/(std/sqrt(T)).

Usage:  python3 src/compute_t11_t12.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import compute_t3 as t3  # verified engine: matrices, lag sets, ts_stats
import compute_t7 as t7  # verified engine: per-country matrices + spread

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
LAG_SETS = t3.LAG_SETS
LAG_COLS = t3.LAG_COLS
ROWS = ["nonannual", "annual", "difference", "all"]

PANEL_OF_GROUP = {"y1": "panela", "y23": "panelb", "y45": "panelc"}
GROUP_LABEL = {"y1": "Panel A — Year 1", "y23": "Panel B — Years 2-3",
               "y45": "Panel C — Years 4-5"}

COUNTRY_CODES = t7.COUNTRY_CODES          # paper order, 14 countries
COUNTRY_LABELS = [t7.LABEL_OF_SLUG[s] for s in t7.COUNTRY_SLUGS]

SIG_THRESHOLD = 0.12                      # paper's 5% level (L3105)
TOKEN_TO_CODE = {"bel": "BEL", "aut": "AUT", "can": "CAN", "fin": "FIN",
                 "fra": "FRA", "ger": "DEU", "uk": "GBR", "swe": "SWE",
                 "che": "CHE"}

QUINT_ITEMS = ["q1", "q2", "q3", "q4", "q5", "q5_q1"]
TRIC_ITEMS = ["t1", "t2", "t3", "t3_t1"]
ITEMS = QUINT_ITEMS + TRIC_ITEMS


# ────────────────────────────────────────────────────────────────────────────
# Table 11 — per-country EW Panel A ANNUAL spread series + correlations
# ────────────────────────────────────────────────────────────────────────────
def compute_annual_signals(E: np.ndarray) -> dict:
    """Annual-strategy excess-signal matrices, same mechanics as
    t7.compute_signals (shifted-copy accumulation, average over available
    lags, NaN if none) restricted to the annual lag sets."""
    n_firm, n_month = E.shape
    SIG: dict = {}
    for group in GROUPS:
        lags = LAG_SETS[group]["annual"]
        num = np.zeros((n_firm, n_month), dtype=float)
        cnt = np.zeros((n_firm, n_month), dtype=float)
        for k in lags:
            if k >= n_month:
                continue
            shifted = np.full((n_firm, n_month), np.nan)
            shifted[:, k:] = E[:, :n_month - k]
            fin = np.isfinite(shifted)
            num += np.where(fin, shifted, 0.0)
            cnt += fin
        SIG[group] = np.where(cnt > 0, num / np.maximum(cnt, 1.0), np.nan)
        print(f"  annual signal {group}: non-missing cells = "
              f"{np.isfinite(SIG[group]).sum():,}")
    return SIG


def compute_country_annual_series(mat: dict, SIG: dict) -> dict:
    """series[(group, country_code)] = {month_idx: EW annual-strategy spread},
    computed exactly as t7.compute_table7 (within-country deciles via
    t7.country_spread), restricted to the annual strategy."""
    R = mat["R"]
    mi_min, mi_max = mat["mi_min"], mat["mi_max"]
    country_rows = mat["country_rows"]

    series: dict = defaultdict(dict)
    sort_months = list(range(SORT_LO, SORT_HI + 1))
    for n, t in enumerate(sort_months):
        t_col = t - mi_min
        if not (0 <= t_col < R.shape[1]):
            continue
        ret_t = R[:, t_col]
        for group in GROUPS:
            sig = SIG[group][:, t_col]
            for code in COUNTRY_CODES:
                rows = country_rows[code]
                if rows.size == 0:
                    continue
                res = t7.country_spread(sig[rows], ret_t[rows])
                if res is None:
                    continue
                series[(group, code)][t] = res[0]
        if (n + 1) % 50 == 0:
            print(f"  processed {n + 1}/{len(sort_months)} sort months")
    return series


def correlation_matrices(series: dict) -> dict:
    """Pearson correlation matrix per year group over common (pairwise-
    complete) months — DataFrame.corr on the 14 country series."""
    corr: dict = {}
    for group in GROUPS:
        df = pd.DataFrame({code: pd.Series(series[(group, code)])
                           for code in COUNTRY_CODES})
        corr[group] = df.corr()
        n_common = df.notna().sum()
        print(f"  {group}: per-country series lengths "
              f"min={int(n_common.min())} max={int(n_common.max())}")
    return corr


def offdiag_stats(c: pd.DataFrame) -> tuple[float, float, int]:
    """Mean pairwise (upper-triangle) correlation, fraction with |rho| > 0.12,
    and the number of pairs."""
    n = c.shape[0]
    iu = np.triu_indices(n, k=1)
    pairs = c.to_numpy()[iu]
    return float(pairs.mean()), float((np.abs(pairs) > SIG_THRESHOLD).mean()), \
        int(pairs.size)


def artifact_pairs(series: dict, group: str,
                   threshold: float = 0.6) -> list[dict]:
    """Detect pairwise correlations beyond `threshold` and identify the month
    driving them (leave-one-out): a pair is single-month-driven if dropping
    one common month brings |rho| below 0.3."""
    df = pd.DataFrame({code: pd.Series(series[(group, code)])
                       for code in COUNTRY_CODES})
    c = df.corr()
    iu = np.triu_indices(len(COUNTRY_CODES), k=1)
    arr = c.to_numpy()
    out = []
    for i, j in zip(*iu):
        rho = arr[i, j]
        if abs(rho) <= threshold:
            continue
        a = df.iloc[:, i].dropna()
        b = df.iloc[:, j].dropna()
        common = a.index.intersection(b.index)
        loo = {}
        for t in common:
            idx = common.drop(t)
            loo[t] = float(np.corrcoef(a.loc[idx], b.loc[idx])[0, 1])
        t_min = min(loo, key=lambda t: abs(loo[t]))
        out.append({"pair": f"{COUNTRY_CODES[i]}-{COUNTRY_CODES[j]}",
                    "rho": float(rho),
                    "driver": t_min,
                    "rho_excl_driver": loo[t_min],
                    "single_month_driven": abs(loo[t_min]) < 0.3})
    return out


def mean_pairwise_excl(c: pd.DataFrame, c1: str, c2: str) -> float:
    """Mean off-diagonal correlation excluding one named pair."""
    codes = list(c.index)
    i, j = codes.index(c1), codes.index(c2)
    iu = np.triu_indices(len(codes), k=1)
    arr = c.to_numpy()
    keep = ~(((iu[0] == i) & (iu[1] == j)) | ((iu[0] == j) & (iu[1] == i)))
    return float(arr[iu][keep].mean())


# ────────────────────────────────────────────────────────────────────────────
# Table 12 — pooled EW Panel A quintile/tricile sorts
# ────────────────────────────────────────────────────────────────────────────
def compute_table12(mat: dict) -> dict:
    """series[(group, strategy, item)] = {month_idx: value}, item in
    q1..q5/q5_q1/t1..t3/t3_t1. Same pooled EW Panel A mechanics as
    compute_t3 (same signal, same ascending average ranks); bins formed with
    ceil(n_bins*rank/N)."""
    R, E = mat["R"], mat["E"]
    mi_min, mi_max = mat["mi_min"], mat["mi_max"]
    n_firm, n_month = mat["n_firm"], mat["n_month"]

    sentinel = n_month
    E_s = np.concatenate([E, np.full((n_firm, 1), np.nan)], axis=1)

    def lag_index(t: int, k: int) -> int:
        c = t - k
        return (c - mi_min) if (mi_min <= c <= mi_max) else sentinel

    series: dict = defaultdict(dict)
    sort_months = list(range(SORT_LO, SORT_HI + 1))
    for n, t in enumerate(sort_months):
        t_col = (t - mi_min) if (mi_min <= t <= mi_max) else None
        if t_col is None:
            continue
        ret_t = R[:, t_col]
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

                cand = np.isfinite(signal) & np.isfinite(ret_t)
                idx = np.where(cand)[0]
                N = int(idx.size)
                if N < 3:
                    continue
                sig = signal[idx]
                rt = ret_t[idx]
                # ascending ranks with average ties — same as
                # compute_t3.sort_spreads.
                ranks = pd.Series(sig).rank(method="average").to_numpy()
                for n_bins, pref in ((5, "q"), (3, "t")):
                    bins = np.clip(np.ceil(n_bins * ranks / N), 1,
                                   n_bins).astype(int)
                    means = {}
                    for k in range(1, n_bins + 1):
                        mk = bins == k
                        if mk.any():
                            means[k] = float(rt[mk].mean())
                            series[(group, strategy, f"{pref}{k}")][t] = \
                                means[k]
                    if 1 in means and n_bins in means:
                        series[(group, strategy,
                                f"{pref}{n_bins}_{pref}1")][t] = \
                            means[n_bins] - means[1]

        if (n + 1) % 50 == 0:
            print(f"  processed {n + 1}/{len(sort_months)} sort months")
    return series


def difference_series(ann: dict, non: dict) -> dict:
    common = set(ann.keys()) & set(non.keys())
    return {mo: ann[mo] - non[mo] for mo in common}


def assemble_t12_cells(series: dict) -> dict[str, float]:
    cells: dict[str, float] = {}
    for group in GROUPS:
        panel = PANEL_OF_GROUP[group]
        for row in ROWS:
            for item in ITEMS:
                s = (difference_series(series[(group, "annual", item)],
                                       series[(group, "nonannual", item)])
                     if row == "difference" else series[(group, row, item)])
                mean, tstat, _ = t3.ts_stats(s)
                cells[f"t12_{panel}_{group}_{row}_{item}_ret"] = mean
                cells[f"t12_{panel}_{group}_{row}_{item}_tstat"] = tstat
    return cells


# ────────────────────────────────────────────────────────────────────────────
# Cells for Table 11 (11 committed names)
# ────────────────────────────────────────────────────────────────────────────
def assemble_t11_cells(corr: dict, metric_names: list[str]) -> dict[str, float]:
    cells: dict[str, float] = {}
    for name in metric_names:
        parts = name.split("_")
        if name == "t11_text_sig_threshold":
            cells[name] = SIG_THRESHOLD       # paper's stated constant
            continue
        # t11_panela_<group>_<c1>_<c2> | t11_text_<group>_<c1>_<c2>[_max|_min]
        assert parts[0] == "t11" and parts[1] in ("panela", "text"), name
        group = parts[2]
        assert group in GROUPS, name
        c1 = TOKEN_TO_CODE[parts[3]]
        c2 = TOKEN_TO_CODE[parts[4]]
        cells[name] = float(corr[group].loc[c1, c2])
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
# Table 11 markdown
# ────────────────────────────────────────────────────────────────────────────
def write_table11_md(corr: dict, cells: dict, paper: dict,
                     series: dict) -> None:
    lines = [
        "# Table 11 — Cross-Country Correlations of Annual-Strategy Returns",
        "",
        "Heston & Sadka (2010), Table 11. Pairwise Pearson correlations across",
        "the 14 countries of the monthly EW Panel A ANNUAL-strategy top-minus-",
        "bottom decile spread series (within-country deciles, identical engine",
        "to Table 7), computed over common (pairwise-complete) months,",
        "t = 1985-02..2006-06. Three panels: Year 1, Years 2-3, Years 4-5.",
        f"The paper's 5% significance level for these correlations is "
        f"|rho| > {SIG_THRESHOLD:.2f} (L3105).",
        "",
    ]
    header = "| Country | " + " | ".join(COUNTRY_CODES) + " |"
    sep = "|---" * (len(COUNTRY_CODES) + 1) + "|"

    stats: dict = {}
    for group in GROUPS:
        c = corr[group]
        mean_pair, frac_sig, n_pairs = offdiag_stats(c)
        stats[group] = (mean_pair, frac_sig, n_pairs)
        lines += ["", f"## {GROUP_LABEL[group]}", "", header, sep]
        arr = c.to_numpy()
        for i, code in enumerate(COUNTRY_CODES):
            row = " | ".join(f"{arr[i, j]:+.2f}" for j in range(len(COUNTRY_CODES)))
            lines.append(f"| {code} | {row} |")
        lines += ["",
                  f"Mean pairwise (off-diagonal) correlation: **{mean_pair:+.3f}** "
                  f"over {n_pairs} pairs; fraction with |rho| > "
                  f"{SIG_THRESHOLD:.2f}: **{frac_sig:.2%}** "
                  f"({int(round(frac_sig * n_pairs))}/{n_pairs}).", ""]

    # Paper anchors.
    lines += ["## Paper anchors vs ours",
              "",
              "| Pair | Panel | Paper | Ours |",
              "|---|---|---|---|"]
    anchors = [
        ("France-Germany", "y1", "t11_panela_y1_ger_fra"),
        ("France-UK", "y1", "t11_text_y1_fra_uk"),
        ("Sweden-France (paper: max of Years 2-3)", "y23",
         "t11_text_y23_swe_fra_max"),
        ("Switzerland-Austria (paper: min of Years 4-5)", "y45",
         "t11_text_y45_che_aut_min"),
    ]
    for label, group, name in anchors:
        lines.append(f"| {label} | {GROUP_LABEL[group]} | "
                     f"{paper.get(name, float('nan')):+.2f} | "
                     f"{cells[name]:+.2f} |")
    # Are the named pairs actually the max/min of our matrices?
    for group, tok_i, tok_j, role in [("y23", "SWE", "FRA", "maximum"),
                                      ("y45", "CHE", "AUT", "minimum")]:
        arr = corr[group].to_numpy()
        iu = np.triu_indices(arr.shape[0], k=1)
        vals = arr[iu]
        our = arr[COUNTRY_CODES.index(tok_i), COUNTRY_CODES.index(tok_j)]
        extreme = vals.max() if role == "maximum" else vals.min()
        lines.append(f"- {GROUP_LABEL[group]}: {tok_i}-{tok_j} = {our:+.3f}; "
                     f"matrix {role} = {extreme:+.3f} "
                     f"(is the named pair the {role}: "
                     f"{np.isclose(our, extreme)}).")
    for group in GROUPS:
        mean_pair, frac_sig, n_pairs = stats[group]
        lines.append(f"- {GROUP_LABEL[group]}: mean pairwise {mean_pair:+.3f}, "
                     f"{int(round(frac_sig * n_pairs))}/{n_pairs} pairs beyond "
                     f"the {SIG_THRESHOLD:.2f} significance level.")

    # Single-month-driven outlier cells (unwinsorized panel, A9).
    lines += ["", "## Data-artifact note (single-month-driven cells)",
              "",
              "Pairs with |rho| > 0.6 are inspected with a leave-one-out over",
              "common months; the panel is unwinsorized (A9), so a single",
              "extreme penny-stock month can dominate one country's spread",
              "series and inflate its correlations mechanically.", ""]
    any_artifact = False
    for group in GROUPS:
        for ap in artifact_pairs(series, group):
            any_artifact = True
            t = ap["driver"]
            yr, mo = (t - 1) // 12, (t - 1) % 12 + 1
            c1, c2 = ap["pair"].split("-")
            excl = mean_pairwise_excl(corr[group], c1, c2)
            base = stats[group][0]
            lines.append(
                f"- {GROUP_LABEL[group]}: {ap['pair']} rho = {ap['rho']:+.3f}; "
                f"dropping {yr}-{mo:02d} alone gives rho = "
                f"{ap['rho_excl_driver']:+.3f} "
                f"({'single-month-driven' if ap['single_month_driven'] else 'NOT single-month-driven'}); "
                f"panel mean pairwise excluding this pair = {excl:+.3f} "
                f"(vs {base:+.3f} with it).")
    if not any_artifact:
        lines.append("- No pair exceeds |rho| > 0.6 in any panel.")
    (RESULTS_DIR / "table_11_correlations.md").write_text(
        "\n".join(lines) + "\n")


# ────────────────────────────────────────────────────────────────────────────
# Table 12 markdown
# ────────────────────────────────────────────────────────────────────────────
def write_table12_md(cells: dict, paper: dict) -> None:
    lines = [
        "# Table 12 — Quintile and Tricile Robustness of the EW Panel A Strategies",
        "",
        "Heston & Sadka (2010), Table 12. The EW Panel A Table-3 engine re-run",
        "with 5 bins (quintiles) and 3 bins (triciles): bin = ceil(n_bins*rank/N)",
        "on the same ascending average ranks as the decile sorts. Bin columns",
        "report the average ret_usd of each bin; Q5-Q1 and T3-T1 are the top-",
        "minus-bottom spreads. Rows nonannual/annual/difference/all in each",
        "year-group panel (A = Year 1, B = Years 2-3, C = Years 4-5); the",
        "difference row is annual[t] - nonannual[t] on common months for bin",
        "means and spreads alike. Our values with paper values in parentheses.",
        "t-stat = mean/(std/sqrt(T)).",
        "",
    ]
    cols = QUINT_ITEMS + TRIC_ITEMS
    header = "| Row | " + " | ".join(c.upper() for c in cols) + " |"
    sep = "|---" * (len(cols) + 1) + "|"

    for group in GROUPS:
        panel = PANEL_OF_GROUP[group]
        lines += ["", f"## {GROUP_LABEL[group]}", ""]
        for stat, stat_label in [("ret", "Average monthly return"),
                                 ("tstat", "t-statistic")]:
            lines += [f"### {stat_label}", "", header, sep]
            for row in ROWS:
                row_cells = []
                for item in cols:
                    our = cells[f"t12_{panel}_{group}_{row}_{item}_{stat}"]
                    pap = paper.get(f"t12_{panel}_{group}_{row}_{item}_{stat}")
                    if pap is None:
                        row_cells.append(f"{our:+.4f}")
                    else:
                        row_cells.append(f"{our:+.4f} ({pap:+.4f})")
                lines.append(f"| {row} | " + " | ".join(row_cells) + " |")
            lines.append("")

    # Robustness check — paper L3601-3603: pattern robust to bin count.
    lines += ["## Robustness check (paper L3601-3603): do quintile/tricile "
              "spreads keep the decile signs?",
              "",
              "Signs compared against our decile spreads "
              "(`results/cells_t3.json`, t3_ew_panelA_<group>_<row>_total_ret).",
              "",
              "| Panel | Row | Decile D10-D1 | Q5-Q1 | T3-T1 | Quintile sign "
              "= decile | Tricile sign = decile |",
              "|---|---|---|---|---|---|---|"]
    dec_path = RESULTS_DIR / "cells_t3.json"
    dec_cells = json.loads(dec_path.read_text()) if dec_path.exists() else {}
    for group in GROUPS:
        panel = PANEL_OF_GROUP[group]
        for row in ROWS:
            q = cells[f"t12_{panel}_{group}_{row}_q5_q1_ret"]
            tr = cells[f"t12_{panel}_{group}_{row}_t3_t1_ret"]
            dec = dec_cells.get(f"t3_ew_panelA_{group}_{row}_total_ret")
            if dec is None:
                lines.append(f"| {GROUP_LABEL[group]} | {row} | n/a | "
                             f"{q:+.4f} | {tr:+.4f} | n/a | n/a |")
                continue
            same_q = (np.sign(q) == np.sign(dec))
            same_t = (np.sign(tr) == np.sign(dec))
            lines.append(f"| {GROUP_LABEL[group]} | {row} | {dec:+.4f} | "
                         f"{q:+.4f} | {tr:+.4f} | {'yes' if same_q else 'NO'} "
                         f"| {'yes' if same_t else 'NO'} |")
    (RESULTS_DIR / "table_12_quintiles.md").write_text(
        "\n".join(lines) + "\n")


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Loading panel: {PANEL_PATH}")
    panel = pd.read_parquet(PANEL_PATH)
    print(f"Panel: {len(panel):,} rows x {panel.shape[1]} cols, "
          f"months {panel['month'].min().date()}..{panel['month'].max().date()}")

    paper_t11, names_t11 = load_table("T11")
    paper_t12, names_t12 = load_table("T12")
    print(f"T11 committed names: {len(names_t11)}; T12 committed names: "
          f"{len(names_t12)}")
    assert len(names_t11) == 11 and len(names_t12) == 240

    # Shared matrices: t7.build_matrices provides R, E and per-country row
    # sets (Table 12 needs only R, E).
    mat = t7.build_matrices(panel)

    print("\n=== Table 11 — per-country EW Panel A annual spread series ===")
    SIG_ann = compute_annual_signals(mat["E"])
    series11 = compute_country_annual_series(mat, SIG_ann)
    corr = correlation_matrices(series11)
    cells_t11 = assemble_t11_cells(corr, names_t11)
    out11 = write_cells_json(cells_t11, names_t11,
                             RESULTS_DIR / "cells_t11.json", "cells_t11")
    write_table11_md(corr, cells_t11, paper_t11, series11)

    print("\n=== Table 12 — pooled EW Panel A quintile/tricile sorts ===")
    series12 = compute_table12(mat)
    cells_t12 = assemble_t12_cells(series12)
    out12 = write_cells_json(cells_t12, names_t12,
                             RESULTS_DIR / "cells_t12.json", "cells_t12")
    write_table12_md(cells_t12, paper_t12)

    # ---- console spot checks vs paper ----
    def show(cells, paper, name):
        p = paper.get(name)
        ps = f"({p:+.4f})" if p is not None else "(   n/a)"
        print(f"  {name:46s} {cells[name]:+.4f} {ps}")

    print("\n=== T11 cells (ours vs paper) ===")
    for name in names_t11:
        show(cells_t11, paper_t11, name)
    for group in GROUPS:
        mean_pair, frac_sig, n_pairs = offdiag_stats(corr[group])
        print(f"  {group} mean pairwise corr = {mean_pair:+.3f}; "
              f"|rho|>0.12: {int(round(frac_sig*n_pairs))}/{n_pairs} "
              f"({frac_sig:.1%})")

    print("\n=== T12 spot checks (ours vs paper) ===")
    for name in ["t12_panela_y1_nonannual_q5_q1_ret",
                 "t12_panela_y1_nonannual_q5_q1_tstat",
                 "t12_panela_y1_nonannual_q1_ret",
                 "t12_panela_y1_nonannual_q5_ret",
                 "t12_panelb_y23_difference_q5_q1_ret",
                 "t12_panelb_y23_difference_q5_q1_tstat",
                 "t12_panelb_y23_difference_q1_ret",
                 "t12_panelb_y23_difference_q5_ret",
                 "t12_panelb_y23_difference_t3_t1_ret",
                 "t12_panelb_y23_difference_t3_t1_tstat",
                 "t12_panelc_y45_difference_q5_q1_ret",
                 "t12_panelc_y45_difference_t3_t1_ret",
                 "t12_panelc_y45_all_t3_t1_ret",
                 "t12_panelc_y45_all_t3_t1_tstat"]:
        show(cells_t12, paper_t12, name)

    print("\n=== T12 q5_q1 / t3_t1 per panel & row (ours vs paper) ===")
    for group in GROUPS:
        panel = PANEL_OF_GROUP[group]
        for row in ROWS:
            q = cells_t12[f"t12_{panel}_{group}_{row}_q5_q1_ret"]
            qt = cells_t12[f"t12_{panel}_{group}_{row}_q5_q1_tstat"]
            tr = cells_t12[f"t12_{panel}_{group}_{row}_t3_t1_ret"]
            tt = cells_t12[f"t12_{panel}_{group}_{row}_t3_t1_tstat"]
            pq = paper_t12[f"t12_{panel}_{group}_{row}_q5_q1_ret"]
            pt = paper_t12[f"t12_{panel}_{group}_{row}_t3_t1_ret"]
            print(f"  {panel} {row:10s} q5_q1={q:+.4f} ({pq:+.4f}) "
                  f"t={qt:+.2f} | t3_t1={tr:+.4f} ({pt:+.4f}) t={tt:+.2f}")

    print(f"\nWrote: table_11_correlations.md, cells_t11.json ({len(out11)} "
          f"names), table_12_quintiles.md, cells_t12.json ({len(out12)} names)")


if __name__ == "__main__":
    main()
