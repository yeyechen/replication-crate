"""
Heston & Sadka (2010), "Seasonality in the Cross Section of Stock Returns:
The International Evidence" — TABLE 1 (summary statistics) and TABLE 2
(cross-sectional return-response regressions).

Consumes the cached analysis-ready panel (data/panel.parquet, READ-ONLY;
columns gvkey, country, curcdd, month, ret_local, ret_usd, me_usd) and writes:

  results/table_1.md            — Table 1, our values with paper in parentheses
  results/table_2.md            — Table 2 full grid + feasible-month counts
  results/cells_t1_t2.json      — flat {metric_name: our_value} for all 282
                                  T1+T2 names in preparations/tables_to_replicate.json
  results/table2_lag_profile.png— gamma vs lag, 4 OLS samples + paper overlay

Methodology (fixed by the Replicator — see task spec + assumptions.md A5/A6/A8/A11):

Table 1 — window 1985-01-31 .. 2006-06-30 (the paper's 258 months). Per country:
  n_firms = unique gvkey in window; n_obs = panel rows (firm-months) in window;
  duration = panel rows per firm within the window, bucketed
  1-59 / 60-119 / 120-179 / >=180 months. Plus a pooled Total row.

Table 2 — for each month t in 1985-02..2006-06 (257 months) and lag k in
  {1..12, 24, 36, 48, 60}: observations = firms with ret_usd non-missing at
  BOTH t and t-k (paper's "all firms with returns available in month t and
  t-k" rule, L112; months with no feasible observations are skipped).
  Regression (eq. 1): r_{i,t} on r_{i,t-k} with country-dummy intercepts,
  implemented via Frisch-Waugh within each month t (country-demean y and x,
  gamma = sum(x* y*) / sum(x*^2)). This is EXACT OLS with country dummies
  (verified against statsmodels below); no per-month statsmodels loop.
  Samples: all_ols (14 countries), europe_ols (12, ex CAN/JPN), canada_ols,
  japan_ols. estimate = TS mean of gamma_{k,t}; tstat = mean / (std/sqrt(T))
  with T = feasible months (std = sample sd, ddof=1).

  WLS (A8): fixed country weights w_c = 1 / sigma2_c, sigma2_c = pooled
  variance of ret_usd over all (firm, month) rows of country c within
  1985-02..2006-06. Because w_c is constant within a (month, country) cell,
  the weighted country mean equals the plain country mean, so the demeaning
  is identical to OLS and gamma_w = sum(w_c * x* y*) / sum(w_c * x*^2) —
  i.e. per-(month,country) cross products simply scale by w_c. Samples:
  all_wls (14), europe_wls (12).

Usage:  python3 src/compute_t1_t2.py
"""
from __future__ import annotations

import json
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

# Paper country order (Table 1) and name/slug maps
COUNTRY_ORDER = ["AUT", "BEL", "CAN", "FIN", "FRA", "DEU", "ITA", "JPN",
                 "NLD", "NOR", "ESP", "SWE", "CHE", "GBR"]
COUNTRY_NAME = {
    "AUT": "Austria", "BEL": "Belgium", "CAN": "Canada", "FIN": "Finland",
    "FRA": "France", "DEU": "Germany", "ITA": "Italy", "JPN": "Japan",
    "NLD": "Netherlands", "NOR": "Norway", "ESP": "Spain", "SWE": "Sweden",
    "CHE": "Switzerland", "GBR": "United Kingdom",
}
COUNTRY_SLUG = {
    "AUT": "austria", "BEL": "belgium", "CAN": "canada", "FIN": "finland",
    "FRA": "france", "DEU": "germany", "ITA": "italy", "JPN": "japan",
    "NLD": "netherlands", "NOR": "norway", "ESP": "spain", "SWE": "sweden",
    "CHE": "switzerland", "GBR": "united_kingdom",
}

ALL14 = set(COUNTRY_ORDER)
EUROPE12 = ALL14 - {"CAN", "JPN"}

# Windows (month-end timestamps / month indices)
T1_START = pd.Timestamp("1985-01-31")
T1_END = pd.Timestamp("2006-06-30")
# month index = year*12 + (month-of-year); 1985-02 .. 2006-06 inclusive
T2_LO = 1985 * 12 + 2    # first regression month t (Feb 1985)
T2_HI = 2006 * 12 + 6    # last regression month t (Jun 2006) — 257 months

LAGS = list(range(1, 13)) + [24, 36, 48, 60]
SAMPLES_OLS = ["all_ols", "europe_ols", "canada_ols", "japan_ols"]
SAMPLES_WLS = ["all_wls", "europe_wls"]
SAMPLE_COUNTRIES = {
    "all_ols": ALL14,
    "europe_ols": EUROPE12,
    "canada_ols": {"CAN"},
    "japan_ols": {"JPN"},
    "all_wls": ALL14,
    "europe_wls": EUROPE12,
}


# ────────────────────────────────────────────────────────────────────────────
# Table 1 — summary statistics
# ────────────────────────────────────────────────────────────────────────────
def compute_table1(panel: pd.DataFrame) -> tuple[dict[str, int], list[dict]]:
    """Returns (cells {metric_name: int}, rows for the md table, Total last)."""
    w = panel[(panel["month"] >= T1_START) & (panel["month"] <= T1_END)].copy()

    def bucket(dur: int) -> str:
        if dur <= 59:
            return "dur_1_60"
        if dur <= 119:
            return "dur_60_120"
        if dur <= 179:
            return "dur_120_180"
        return "dur_180_plus"

    cells: dict[str, int] = {}
    rows: list[dict] = []
    tot = {"country": "Total", "n_firms": 0, "dur_1_60": 0, "dur_60_120": 0,
           "dur_120_180": 0, "dur_180_plus": 0, "n_obs": 0}

    # months-present per firm within the window (panel rows per gvkey)
    firm_dur = w.groupby(["country", "gvkey"]).size()
    firm_bucket = firm_dur.map(bucket)

    for cc in COUNTRY_ORDER:
        wc = w[w["country"] == cc]
        n_firms = int(wc["gvkey"].nunique())
        n_obs = int(len(wc))
        bc = firm_bucket[firm_bucket.index.get_level_values("country") == cc]
        counts = bc.value_counts().to_dict()
        d1, d2, d3, d4 = (int(counts.get(b, 0)) for b in
                          ("dur_1_60", "dur_60_120", "dur_120_180", "dur_180_plus"))
        slug = COUNTRY_SLUG[cc]
        cells[f"t1_{slug}_n_firms"] = n_firms
        cells[f"t1_{slug}_dur_1_60"] = d1
        cells[f"t1_{slug}_dur_60_120"] = d2
        cells[f"t1_{slug}_dur_120_180"] = d3
        cells[f"t1_{slug}_dur_180_plus"] = d4
        cells[f"t1_{slug}_n_obs"] = n_obs
        rows.append({"country": COUNTRY_NAME[cc], "n_firms": n_firms,
                     "dur_1_60": d1, "dur_60_120": d2, "dur_120_180": d3,
                     "dur_180_plus": d4, "n_obs": n_obs})
        tot["n_firms"] += n_firms   # gvkeys are disjoint across countries (F6)
        tot["dur_1_60"] += d1
        tot["dur_60_120"] += d2
        tot["dur_120_180"] += d3
        tot["dur_180_plus"] += d4
        tot["n_obs"] += n_obs

    # Total also verifiable directly:
    n_firms_all = int(w["gvkey"].nunique())
    assert n_firms_all == tot["n_firms"], "gvkey appears under >1 country!"
    assert len(w) == tot["n_obs"]
    cells["t1_total_n_firms"] = tot["n_firms"]
    cells["t1_total_dur_1_60"] = tot["dur_1_60"]
    cells["t1_total_dur_60_120"] = tot["dur_60_120"]
    cells["t1_total_dur_120_180"] = tot["dur_120_180"]
    cells["t1_total_dur_180_plus"] = tot["dur_180_plus"]
    cells["t1_total_n_obs"] = tot["n_obs"]
    rows.append(tot)
    return cells, rows


# ────────────────────────────────────────────────────────────────────────────
# Table 2 — cross-sectional return-response regressions (FWL, vectorized)
# ────────────────────────────────────────────────────────────────────────────
def compute_table2(panel: pd.DataFrame) -> tuple[dict, dict]:
    """Returns (cells {(lag,grp,kind): float}, T_counts {(lag,grp): int})."""
    d = panel.loc[panel["ret_usd"].notna(),
                  ["gvkey", "country", "month", "ret_usd"]].copy()
    d["m_idx"] = d["month"].dt.year * 12 + d["month"].dt.month

    # WLS country weights (A8): pooled variance over 1985-02..2006-06
    var_win = d[(d["m_idx"] >= T2_LO) & (d["m_idx"] <= T2_HI)]
    sigma2 = var_win.groupby("country")["ret_usd"].var(ddof=1)
    w_country = (1.0 / sigma2).to_dict()
    print("WLS country weights (1/sigma2_c):")
    for cc in COUNTRY_ORDER:
        print(f"  {cc}: sigma2={sigma2[cc]:.6f}  w={w_country[cc]:.4f}")

    cells: dict[tuple, float] = {}
    tcounts: dict[tuple, int] = {}

    for k in LAGS:
        # pair each row (firm, month t) with the same firm's ret at t-k
        src = d[["gvkey", "m_idx", "ret_usd"]].rename(
            columns={"ret_usd": "ret_lag", "m_idx": "m_src"})
        src["m_idx"] = src["m_src"] + k          # align to the t-side month
        m = d.merge(src[["gvkey", "m_idx", "ret_lag"]],
                    on=["gvkey", "m_idx"], how="inner")
        m = m[(m["m_idx"] >= T2_LO) & (m["m_idx"] <= T2_HI)]

        # Frisch-Waugh: country-demean y and x within each month t
        g = m.groupby(["m_idx", "country"])
        xs = m["ret_lag"] - g["ret_lag"].transform("mean")
        ys = m["ret_usd"] - g["ret_usd"].transform("mean")
        # per (month, country) cross products — the atomic block for every
        # sample (subsetting by country never changes the demeaning)
        mc = pd.DataFrame({
            "m_idx": m["m_idx"],
            "country": m["country"],
            "num": xs * ys,
            "den": xs * xs,
        }).groupby(["m_idx", "country"]).sum()
        # WLS: w_c constant within (month, country) => weighted country mean =
        # plain mean, so weighted cross products = w_c x OLS cross products
        mc["num_w"] = mc["num"] * mc.index.get_level_values("country").map(w_country)
        mc["den_w"] = mc["den"] * mc.index.get_level_values("country").map(w_country)

        for grp in SAMPLES_OLS + SAMPLES_WLS:
            cc_set = SAMPLE_COUNTRIES[grp]
            mcS = mc[mc.index.get_level_values("country").isin(cc_set)]
            num_col, den_col = ("num_w", "den_w") if grp.endswith("_wls") else ("num", "den")
            per_t = mcS.groupby("m_idx")[[num_col, den_col]].sum()
            per_t = per_t[per_t[den_col] > 0]     # feasible months only
            gamma = per_t[num_col] / per_t[den_col]
            T = int(len(gamma))
            tcounts[(k, grp)] = T
            if T >= 2:
                est = float(gamma.mean())
                tstat = float(est / (gamma.std(ddof=1) / np.sqrt(T)))
            elif T == 1:
                est = float(gamma.iloc[0])
                tstat = float("nan")
            else:
                est = float("nan")
                tstat = float("nan")
            cells[(k, grp, "est")] = est
            cells[(k, grp, "tstat")] = tstat
        print(f"lag {k:>2}: T(all_ols)={tcounts[(k,'all_ols')]:>3} "
              f"T(europe_ols)={tcounts[(k,'europe_ols')]:>3} "
              f"T(canada_ols)={tcounts[(k,'canada_ols')]:>3} "
              f"T(japan_ols)={tcounts[(k,'japan_ols')]:>3} "
              f"| est all_ols={cells[(k,'all_ols','est')]:+.4f}")
    return cells, tcounts


def verify_fwl_against_ols(panel: pd.DataFrame) -> None:
    """One-shot check: FWL gamma == statsmodels OLS with country dummies."""
    import statsmodels.formula.api as smf

    d = panel.loc[panel["ret_usd"].notna(),
                  ["gvkey", "country", "month", "ret_usd"]].copy()
    d["m_idx"] = d["month"].dt.year * 12 + d["month"].dt.month
    t_idx = 1990 * 12 + 1  # Jan 1990
    src = d[["gvkey", "m_idx", "ret_usd"]].rename(
        columns={"ret_usd": "ret_lag", "m_idx": "m_src"})
    src["m_idx"] = src["m_src"] + 1
    mm = d.merge(src[["gvkey", "m_idx", "ret_lag"]],
                 on=["gvkey", "m_idx"], how="inner")
    mt = mm[mm["m_idx"] == t_idx]
    # FWL
    gg = mt.groupby("country")
    xs = mt["ret_lag"] - gg["ret_lag"].transform("mean")
    ys = mt["ret_usd"] - gg["ret_usd"].transform("mean")
    gamma_fwl = float((xs * ys).sum() / (xs * xs).sum())
    # exact OLS with country dummies
    fit = smf.ols("ret_usd ~ ret_lag + C(country)", data=mt).fit()
    gamma_ols = float(fit.params["ret_lag"])
    print(f"[verify] t=1990-01 lag1: FWL gamma={gamma_fwl:.10f}  "
          f"statsmodels gamma={gamma_ols:.10f}  diff={abs(gamma_fwl-gamma_ols):.2e}  "
          f"n_obs={len(mt)}")
    assert abs(gamma_fwl - gamma_ols) < 1e-10, "FWL != exact OLS with dummies"


# ────────────────────────────────────────────────────────────────────────────
# Output writers
# ────────────────────────────────────────────────────────────────────────────
def load_paper_values() -> dict[str, float]:
    """Paper values keyed by metric name, straight from tables_to_replicate.json."""
    tables = json.loads(TABLES_JSON.read_text())["tables"]
    pv = {}
    names = []
    for t in tables:
        if t["id"] in ("T1", "T2"):
            for m in t["metrics"]:
                pv[m["name"]] = m["value"]
                names.append(m["name"])
    return pv, names


def write_table1_md(rows: list[dict], paper: dict) -> None:
    cols = ["n_firms", "dur_1_60", "dur_60_120", "dur_120_180",
            "dur_180_plus", "n_obs"]
    header = ("| Country | No. of Firms | 1 ≤ Months < 60 | 60 ≤ Months < 120 "
              "| 120 ≤ Months < 180 | Months ≥ 180 | Firm-Month Obs. |")
    sep = "|---" * 8 + "|"
    lines = ["# Table 1 — Summary Statistics of International Stock Returns",
             "",
             "Heston & Sadka (2010), Table 1. Window: 1985-01-31 .. 2006-06-30 "
             "(258 months). Our values with paper values in parentheses.",
             "Duration buckets = months present per firm within the window "
             "(1–59 / 60–119 / 120–179 / ≥180).",
             "", header, sep]
    name_to_slug = {v: COUNTRY_SLUG[k] for k, v in COUNTRY_NAME.items()}
    name_to_slug["Total"] = "total"
    for r in rows:
        slug = name_to_slug[r["country"]]
        cells = []
        for c in cols:
            pv = paper.get(f"t1_{slug}_{c}")
            cells.append(f"{r[c]:,} ({pv:,})")
        lines.append("| " + ("**" if r["country"] == "Total" else "")
                     + r["country"] + ("**" if r["country"] == "Total" else "")
                     + " | " + " | ".join(cells) + " |")
    (RESULTS_DIR / "table_1.md").write_text("\n".join(lines) + "\n")


def write_table2_md(cells: dict, tcounts: dict, paper: dict) -> None:
    groups = SAMPLES_OLS + SAMPLES_WLS
    titles = {"all_ols": "All countries (OLS)", "europe_ols": "Europe (OLS)",
              "canada_ols": "Canada (OLS)", "japan_ols": "Japan (OLS)",
              "all_wls": "All countries (WLS)", "europe_wls": "Europe (WLS)"}
    lines = ["# Table 2 — Cross-Sectional Regressions of Returns "
             "(Return Responses γₖ)",
             "",
             "Heston & Sadka (2010), Table 2. Monthly Fama-MacBeth regressions "
             "r_{i,t} on r_{i,t-k} with country-dummy intercepts (Frisch-Waugh "
             "demeaning = exact OLS), t ∈ 1985-02..2006-06 (257 months); "
             "observations = firms with ret_usd available at both t and t-k. "
             "WLS weights w_c = 1/σ²_c (pooled country variance, A8). "
             "Our values with paper values in parentheses.", ""]

    # Full grid: rows = lag, columns = sample × (est, tstat)
    hdr1 = "| Lag |" + "".join(f" {titles[g]} est | {titles[g]} t-stat |" for g in groups)
    hdr2 = "|---" * (1 + 2 * len(groups)) + "|"
    lines += [hdr1, hdr2]
    for k in LAGS:
        row = [str(k)]
        for g in groups:
            est, ts = cells[(k, g, "est")], cells[(k, g, "tstat")]
            pev = paper.get(f"t2_lag{k}_{g}_est")
            pts = paper.get(f"t2_lag{k}_{g}_tstat")
            row.append(f"{est:+.4f} ({pev:+.4f})")
            row.append(f"{ts:+.2f} ({pts:+.2f})")
        lines.append("| " + " | ".join(row) + " |")

    # Feasible-month counts T per (sample, lag) — A11: long lags start late
    lines += ["",
              "## Feasible months T per (sample, lag)",
              "",
              "Months with ≥1 firm-pair and positive within-country variation "
              "in x. Long lags start late for us (A11: priced Compustat data "
              "begins 1985-12 for the 13 global countries; Canada from 1984-01).",
              "",
              "| Lag | " + " | ".join(groups) + " |",
              "|---" * (1 + len(groups)) + "|"]
    for k in LAGS:
        lines.append("| " + " | ".join([str(k)] + [str(tcounts[(k, g)]) for g in groups]) + " |")
    (RESULTS_DIR / "table_2.md").write_text("\n".join(lines) + "\n")


def write_cells_json(t1_cells: dict, t2_cells: dict,
                     tcounts: dict, metric_names: list[str]) -> dict:
    """Flat {metric_name: value} covering EVERY T1/T2 name in the spec file."""
    out: dict = {}
    for name in metric_names:
        if name.startswith("t1_"):
            v = t1_cells[name]
            out[name] = int(v)
        else:
            m = name[3:]  # strip 't2_'
            # parse lag{k}_{grp}_{kind}; grp may contain underscores
            parts = m.split("_")
            k = int(parts[0].replace("lag", ""))
            kind = parts[-1]
            grp = "_".join(parts[1:-1])
            v = t2_cells[(k, grp, kind)]
            assert np.isfinite(v), f"non-finite T2 cell {name} = {v}"
            out[name] = float(v)
    (RESULTS_DIR / "cells_t1_t2.json").write_text(
        json.dumps(out, indent=2, allow_nan=False) + "\n")
    return out


def write_plot(cells: dict, paper: dict) -> None:
    fig, ax = plt.subplots(figsize=(9, 6))
    colors = {"all_ols": "#1f77b4", "europe_ols": "#ff7f0e",
              "canada_ols": "#2ca02c", "japan_ols": "#d62728"}
    for g in SAMPLES_OLS:
        ys = [cells[(k, g, "est")] for k in LAGS]
        ax.plot(LAGS, ys, marker="o", ms=4, color=colors[g], label=g)
    # paper's all_ols estimates as scatter overlay
    paper_ys = [paper[f"t2_lag{k}_all_ols_est"] for k in LAGS]
    ax.scatter(LAGS, paper_ys, marker="s", s=45, facecolors="none",
               edgecolors="black", linewidths=1.4, zorder=5,
               label="paper all_ols")
    ax.axhline(0.0, color="grey", lw=0.9, ls="--")
    ax.set_xlabel("Lag k (months)")
    ax.set_ylabel("γₖ estimate (return response)")
    ax.set_title("Heston & Sadka (2010) Table 2 — Return Responses by Lag\n"
                 "Lag-1 reversal, positive annual-lag continuation "
                 "(our replication vs paper)")
    ax.set_xticks(LAGS)
    ax.set_xticklabels(LAGS, rotation=45, ha="right")
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "table2_lag_profile.png", dpi=150)
    plt.close(fig)


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Loading panel: {PANEL_PATH}")
    panel = pd.read_parquet(PANEL_PATH)
    print(f"Panel: {len(panel):,} rows x {panel.shape[1]} cols, "
          f"months {panel['month'].min().date()}..{panel['month'].max().date()}")

    paper, metric_names = load_paper_values()
    n_t1 = sum(1 for n in metric_names if n.startswith("t1_"))
    n_t2 = sum(1 for n in metric_names if n.startswith("t2_"))
    print(f"Metric names from tables_to_replicate.json: {n_t1} T1 + {n_t2} T2 "
          f"= {len(metric_names)}")

    verify_fwl_against_ols(panel)

    print("\n=== Table 1 ===")
    t1_cells, t1_rows = compute_table1(panel)
    for r in t1_rows:
        print(f"  {r['country']:<15} firms={r['n_firms']:>6,} "
              f"obs={r['n_obs']:>9,} dur[{r['dur_1_60']}/{r['dur_60_120']}/"
              f"{r['dur_120_180']}/{r['dur_180_plus']}]")

    print("\n=== Table 2 ===")
    t2_cells, tcounts = compute_table2(panel)

    write_table1_md(t1_rows, paper)
    write_table2_md(t2_cells, tcounts, paper)
    out = write_cells_json(t1_cells, t2_cells, tcounts, metric_names)
    write_plot(t2_cells, paper)
    print(f"\nWrote: table_1.md, table_2.md, cells_t1_t2.json ({len(out)} names), "
          f"table2_lag_profile.png")


if __name__ == "__main__":
    main()
