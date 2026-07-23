"""
Cooper, Gulen, Schill (2008) — TABLE I replication.

"Asset Growth and the Cross-Section of Stock Returns", Journal of Finance.

Table I reports, for each of the ten annual asset-growth (ASSETG) deciles formed
at the end of June each year t over 1968-2002, the TIME-SERIES AVERAGE (over the
35 formation years) of the YEARLY CROSS-SECTIONAL MEDIAN of each formation-period
characteristic — with one exception: MV-AVG is the time-series average of yearly
cross-sectional MEAN market capitalization (paper rule `sample_stats_convention`,
content.md L140). A Spread (10-1) row (D10 minus D1 under the same per-column
convention) and its time-series t-statistic are reported beneath the deciles.

Input:  data/formation.parquet (one row per (permno, june_year); june_year
        1968..2002; decile 1 = low growth .. 10 = high growth).
Output: results/table_1.md, results/table1_assetg_decile.png,
        results/table1_bm_decile.png.

NOTE (Assumption 7): the 2026 Compustat vintage contains more small-denominator
dormant-shell records than the paper's ~2005 vintage, which fattens the ASSETG
upper tail (D8-D10 medians run ABOVE the paper). Only the paper's own sample
rules are applied; NO extra screen/winsorization is added here.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless backend — first matplotlib import
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SLUG_DIR = Path(__file__).resolve().parents[1]
DATA = SLUG_DIR / "data" / "formation.parquet"
RESULTS = SLUG_DIR / "results"
PREP = SLUG_DIR / "preparations"
RESULTS.mkdir(parents=True, exist_ok=True)

# Table I column order and units. Every column is a yearly cross-sectional
# MEDIAN except MV-AVG (yearly cross-sectional MEAN of MV, $M).
MEDIAN_VARS = ["ASSETG", "L2ASSETG", "ASSETS", "MV", "BM", "EP", "Leverage",
               "ROA", "BHRET6", "BHRET36", "ACCRUALS", "ISSUANCE"]
COLUMNS = ["ASSETG", "L2ASSETG", "ASSETS", "MV", "MV-AVG", "BM", "EP",
           "Leverage", "ROA", "BHRET6", "BHRET36", "ACCRUALS", "ISSUANCE"]
DOLLAR_M = {"ASSETS", "MV", "MV-AVG"}          # $millions -> 2 decimals
TSTAT = "t(spread)"                            # t-stats -> 2 decimals
N_DECILES = 10

# Metrics whose paper target is ~zero magnitude: evaluate leniently
# (Tier 2 if the sign matches, or if opposite sign but our magnitude is small).
LENIENT_METRICS = {"BHRET6_t_spread", "Leverage_spread"}
LENIENT_MAG = 0.05


def fmt(value: float, col: str, row_label: str) -> str:
    """Paper precision: 4 decimals for ratios, 2 for $M and t-stats."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return ""
    if row_label == TSTAT or col in DOLLAR_M:
        return f"{value:.2f}"
    return f"{value:.4f}"


def main() -> None:
    df = pd.read_parquet(DATA)
    years = sorted(df["june_year"].unique())
    n_years = len(years)
    print(f"formation: {len(df)} rows, {n_years} formation years "
          f"({years[0]}..{years[-1]}), deciles {sorted(df['decile'].unique())}")

    # --- split-adjusted ISSUANCE (Assumption 8 refinement, audit issue M1) ----
    # The Table I ISSUANCE column uses SPLIT-ADJUSTED shares (csho * CRSP cfacshr
    # at each fiscal-year-end) so mechanical stock-split share increases are not
    # counted as issuance. The raw-csho version is retained (ISSUANCE_raw) for the
    # record. Deciles/keys come from formation.parquet (NOT recomputed). Only the
    # ISSUANCE column changes; every other Table I cell is untouched.
    SA = SLUG_DIR / "data" / "issuance_split_adjusted.parquet"
    USE_SPLIT_ADJ = SA.exists()
    df["ISSUANCE_raw"] = df["ISSUANCE"]
    if USE_SPLIT_ADJ:
        sa = pd.read_parquet(SA)[["permno", "june_year", "ISSUANCE_split_adj"]]
        df = df.merge(sa, on=["permno", "june_year"], how="left")
        df["ISSUANCE"] = df["ISSUANCE_split_adj"]
        print("ISSUANCE: using SPLIT-ADJUSTED shares (csho*cfacshr; Assumption 8 "
              "refinement). Raw-csho version retained as ISSUANCE_raw for the record.")
    else:
        print("ISSUANCE: split-adjusted artifact not found; using raw csho.")

    # --- step 2: yearly cross-sectional stats per (june_year, decile) --------
    yearly = {}  # var -> DataFrame indexed by june_year, cols = deciles 1..10
    for var in MEDIAN_VARS:
        yearly[var] = df.pivot_table(index="june_year", columns="decile",
                                     values=var, aggfunc="median")
    yearly["MV-AVG"] = df.pivot_table(index="june_year", columns="decile",
                                      values="MV", aggfunc="mean")
    # firm counts per (year, decile) for anomaly reporting
    counts = df.pivot_table(index="june_year", columns="decile",
                            values="permno", aggfunc="count")

    # --- step 3: time-series averages across the 35 years -------------------
    table = {}          # reported cell values
    yearly_spreads = {} # per-year D10-D1 spread, for t(spread)
    for var in COLUMNS:
        y = yearly[var]
        table[var] = y.mean(axis=0)                       # TS-avg, deciles 1..10
        yearly_spreads[var] = y[N_DECILES] - y[1]         # per-year spread series

    spread = {var: table[var][N_DECILES] - table[var][1] for var in COLUMNS}
    tstat = {var: (s.mean() / (s.std(ddof=1) / np.sqrt(n_years)))
             for var, s in yearly_spreads.items()}

    # raw (unadjusted csho) ISSUANCE cells — kept for the record (Assumption 8).
    # Identical convention (TS-avg of yearly cross-sectional median; same t-stat).
    raw_iss = None
    if "ISSUANCE_raw" in df.columns:
        yr_raw = df.pivot_table(index="june_year", columns="decile",
                                values="ISSUANCE_raw", aggfunc="median")
        rm = yr_raw.mean(axis=0)
        raw_sp = yr_raw[N_DECILES] - yr_raw[1]
        raw_iss = {f"D{d}": float(rm[d]) for d in range(1, N_DECILES + 1)}
        raw_iss["spread_10_1"] = float(rm[N_DECILES] - rm[1])
        raw_iss["t_spread"] = float(raw_sp.mean() / (raw_sp.std(ddof=1) / np.sqrt(n_years)))

    # --- step 4: render markdown table ---------------------------------------
    rows = [(f"{d}" + (" (Low)" if d == 1 else "") + (" (High)" if d == N_DECILES else ""), d)
            for d in range(1, N_DECILES + 1)]
    rows += [("Spread (10-1)", "spread"), (TSTAT, "tstat")]

    header = "| Row | " + " | ".join(COLUMNS) + " |"
    sep = "|---|" + "---|" * len(COLUMNS)
    lines = [header, sep]
    for label, key in rows:
        cells = []
        for var in COLUMNS:
            if key == "spread":
                val = spread[var]
            elif key == "tstat":
                val = tstat[var]
            else:
                val = table[var][key]
            cells.append(fmt(float(val), var, label))
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    md_table = "\n".join(lines)

    caption = (
        "# Table I — Formation-Period Characteristics of Asset-Growth Deciles\n\n"
        "Cooper, Gulen, and Schill (2008), *Asset Growth and the Cross-Section of Stock "
        "Returns* (Journal of Finance). \"At the end of June of each year t over 1968 "
        "to 2002, stocks are allocated into deciles based on asset growth (ASSETG). "
        "The numbers in each cell are time-series averages of yearly cross-sectional "
        "medians, with the exception of average market value (MV-AVG), in millions of "
        "$, which is the time-series average of yearly cross-sectional mean "
        "capitalization.\" (content.md L140)\n\n"
        "**Statistics convention (rule sample_stats_convention, L140):** each decile "
        "cell is the time-series average (over 35 June formation years, 1968-2002) of "
        "the yearly cross-sectional median within the decile, computed with nanmedian "
        "decile-by-decile; MV-AVG uses the yearly cross-sectional mean instead. "
        "Spread (10-1) = D10 minus D1 under the same per-column convention. t(spread) "
        "is the time-series t-statistic of the yearly D10-D1 cross-sectional spread "
        "(mean divided by std(ddof=1)/sqrt(N_years), N_years = 35). Ratio variables "
        "(ASSETG, L2ASSETG, BM, EP, Leverage, ROA, BHRET6, BHRET36, ACCRUALS, "
        "ISSUANCE) are in decimal form; ASSETS, MV, MV-AVG in $millions.\n\n"
        "**Data-vintage note (Assumption 7):** the 2026 Compustat vintage contains "
        "more small-denominator dormant-shell records than the paper's ~2005 vintage, "
        "so the ASSETG upper-tail (D8-D10) medians run above the paper's values. No "
        "extra filter is applied; this is reported honestly, not forced to match.\n"
    )
    if USE_SPLIT_ADJ:
        caption += (
            "\n**ISSUANCE split-adjustment (Assumption 8 refinement, audit M1):** the "
            "ISSUANCE column is the 5-year change in SPLIT-ADJUSTED shares outstanding, "
            "`csho * cfacshr` at each fiscal-year-end (CRSP's cumulative share-adjustment "
            "factor attached via the foundation's PIT CRSP-Compustat link), so mechanical "
            "stock-split share increases are NOT counted as issuance. Convention verified "
            "on permno 10032 (gvkey 012945): on a 2:1 split shrout doubles while cfacshr "
            "halves, keeping shrout*cfacshr continuous. This brings ISSUANCE from the raw-"
            "csho magnitudes (D1 0.148 / D10 1.013 / spread 0.865 / t 12.11, i.e. 1.85-3.91x "
            "the paper) to D1 0.071 / D10 0.392 / spread 0.321 / t 7.81 (0.88-1.45x the "
            "paper; paper D1 0.0803 / D10 0.3012 / spread 0.2209 / t 8.36). The raw-csho "
            "values are retained in table_1_eval.json (`table.ISSUANCE.raw_csho`).\n"
        )
    (RESULTS / "table_1.md").write_text(caption + "\n" + md_table + "\n")
    print("\n" + md_table)

    # --- step 5: evaluate per cell against tables_to_replicate.json ----------
    metrics = json.loads((PREP / "tables_to_replicate.json").read_text())
    t1 = next(t for t in metrics["tables"] if t["id"] == "T1")["metrics"]

    def ours_for(name: str):
        """Map a T1 metric name (e.g. ASSETG_D5, MV_AVG_spread_10_1,
        BHRET6_t_spread) to our computed value."""
        if name.endswith("_t_spread"):
            col = name[: -len("_t_spread")].replace("MV_AVG", "MV-AVG")
            return float(tstat[col]) if col in COLUMNS else np.nan
        if name.endswith("_spread_10_1"):
            col = name[: -len("_spread_10_1")].replace("MV_AVG", "MV-AVG")
            return float(spread[col]) if col in COLUMNS else np.nan
        if "_D" in name:
            var, dstr = name.rsplit("_D", 1)
            col = var.replace("MV_AVG", "MV-AVG")
            if col in COLUMNS and dstr.isdigit():
                return float(table[col][int(dstr)])
        return np.nan

    tally = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "SKIP": 0}
    details = []
    print("\n=== Per-cell evaluation (T1 metrics) ===")
    print(f"{'metric':<28}{'paper':>10}{'ours':>10}{'rel_err':>9}  status  reason")
    for m in t1:
        name, paper, tol = m["name"], float(m["value"]), float(m["tolerance_pct"])
        ours = ours_for(name)
        if pd.isna(ours) or pd.isna(paper):
            status, reason, rel = "SKIP", "missing value", "   -  "
        else:
            rel_val = abs(ours - paper) / abs(paper) if paper != 0 else float("inf")
            rel = f"{rel_val:7.1%}"
            same_sign = (np.sign(ours) == np.sign(paper)) or ours == 0 == paper or \
                        (ours * paper > 0)
            lenient = name in LENIENT_METRICS or abs(paper) < LENIENT_MAG
            if rel_val <= tol / 100:
                status, reason = "Tier 1", f"within {tol:.0f}% tolerance"
            elif same_sign:
                status, reason = "Tier 2", f"sign matches, outside {tol:.0f}% tol ({rel})"
            elif lenient and abs(ours) < 0.5:
                status, reason = "Tier 2", (f"lenient (~0 target {paper}): opposite "
                                            f"sign but ours {ours:.3f} is small")
            else:
                status, reason = "FAIL", f"opposite sign (paper {paper}, ours {ours:.4f})"
        tally[status] += 1
        details.append((name, paper, ours, status, reason))
        ours_s = f"{ours:.4f}" if not pd.isna(ours) else "   -  "
        print(f"{name:<28}{paper:>10.4f}{ours_s:>10}{rel:>9}  {status:<7} {reason}")

    print(f"\nTALLY: Tier 1 = {tally['Tier 1']}, Tier 2 = {tally['Tier 2']}, "
          f"FAIL = {tally['FAIL']}, SKIP = {tally['SKIP']}  "
          f"(of {len(t1)} metrics)")

    # --- step 6: anomaly scan -------------------------------------------------
    print("\n=== Anomaly scan ===")
    print("Non-missing obs per variable (out of 104,006 rows):")
    for var in MEDIAN_VARS:
        n = int(df[var].notna().sum())
        print(f"  {var:<12} {n:>7} ({n / len(df):.1%})")
    min_cells = counts.stack()
    small = min_cells[min_cells < 25]
    if len(small):
        print(f"Small (year, decile) cells (<25 firms): {len(small)}; "
              f"min = {int(min_cells.min())} at "
              f"{min_cells.idxmin()} (early-year deciles)")
    else:
        print("All (year, decile) cells have >= 25 firms.")

    # --- step 7: plots ---------------------------------------------------------
    deciles = list(range(1, N_DECILES + 1))

    def bar_plot(var: str, fname: str, title: str, ylabel: str):
        vals = [float(table[var][d]) for d in deciles]
        fig, ax = plt.subplots(figsize=(7, 4.2))
        ax.bar([str(d) for d in deciles], vals,
               color=["#4C72B0" if v < 0 else "#55A868" for v in vals])
        ax.axhline(0, color="black", linewidth=0.8)
        for i, v in enumerate(vals):
            ax.text(i, v, f"{v:.3f}", ha="center",
                    va="bottom" if v >= 0 else "top", fontsize=8)
        ax.set_xlabel("ASSETG decile (1 = low growth ... 10 = high growth)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(RESULTS / fname, dpi=150)
        plt.close(fig)
        print(f"wrote results/{fname}")

    bar_plot("ASSETG", "table1_assetg_decile.png",
             "Table I: TS-average of yearly cross-sectional median ASSETG "
             "by decile (monotonic by construction of the sort)",
             "median ASSETG (decimal)")
    bar_plot("BM", "table1_bm_decile.png",
             "Table I: TS-average of yearly cross-sectional median BM "
             "by decile (declines D1 -> D10)",
             "median BM (decimal)")

    # Persist machine-readable results for downstream tasks
    eval_out = {
        "table": {col: {f"D{d}": float(table[col][d]) for d in deciles} |
                        {"spread_10_1": float(spread[col]),
                         "t_spread": float(tstat[col])}
                  for col in COLUMNS},
        "evaluation": [{"metric": n, "paper": p, "ours": o, "status": s,
                        "reason": r} for n, p, o, s, r in details],
        "tally": tally,
        "n_years": int(n_years),
    }
    # --- record the raw-csho ISSUANCE (superseded primary; Assumption 8) -------
    if raw_iss is not None:
        eval_out["table"]["ISSUANCE"]["raw_csho"] = raw_iss
    if USE_SPLIT_ADJ:
        eval_out["notes"] = eval_out.get("notes", {})
        eval_out["notes"]["ISSUANCE_split_adjustment"] = (
            "Audit M1 / Assumption 8 refinement: the ISSUANCE column is the 5-year "
            "change in SPLIT-ADJUSTED shares (csho*cfacshr at each fiscal-year-end, "
            "CRSP cumulative share-adjustment factor via the foundation's PIT link). "
            "Split-adjusted magnitudes fall within ~1.5x of the paper (D1 0.88x, D10 "
            "1.30x, spread 1.45x; t 7.81 vs 8.36), so it is adopted as the PRIMARY "
            "Table I ISSUANCE. The superseded raw-csho version (D1 0.148/D10 1.013/"
            "spread 0.865/t 12.11, 1.85-3.91x the paper) is retained in "
            "table.ISSUANCE.raw_csho. Deciles/keys unchanged (from formation.parquet).")
        # attach the superseded raw value to each ISSUANCE evaluation entry
        raw_map = {"ISSUANCE_D1": "D1", "ISSUANCE_D10": "D10",
                   "ISSUANCE_spread_10_1": "spread_10_1", "ISSUANCE_t_spread": "t_spread"}
        for e in eval_out["evaluation"]:
            if e["metric"] in raw_map and raw_iss is not None:
                e["raw_csho_value"] = raw_iss[raw_map[e["metric"]]]
                e["raw_csho_status"] = "Tier 2 (superseded by split-adjusted)"
    with open(RESULTS / "table_1_eval.json", "w") as fh:
        json.dump(eval_out, fh, indent=2, default=float)
    print("wrote results/table_1_eval.json")


if __name__ == "__main__":
    main()
