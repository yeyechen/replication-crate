"""Stage 4 — Moskowitz & Grinblatt (1999) Table VI Fama-MacBeth regressions.

Inner-loop iteration 7. Reads the frozen 48-col data/panel.parquet and runs the
paper's 32 monthly cross-sectional Fama-MacBeth regressions (Panels A-D,
January 1973-July 1995, T = 271 months) of the Daniel-Titman size/BE-ME-adjusted
return r_sb on beta, log size, log BE/ME, and individual (ret) / industry (ind)
past-return variables.

Methodology (assumptions A11/A12/A14/A18):
  * Each month: ONE unweighted OLS cross-section of r_sb on the spec's
    regressors + a constant. Rows with any NaN in the dependent variable or any
    regressor of that spec are dropped; a month needs >= 30 observations to fit
    (dropped months are reported).
  * Winsorization (A18, iteration 8): BEFORE fitting each month's regression,
    the dependent variable (r_sb) AND every regressor column are winsorized at
    the 1st/99th percentiles computed WITHIN that month's cross-section (clipped
    to the percentiles), on exactly the rows entering that regression. This
    tames the fat tails in r_sb (max +13.96 in the raw panel) that otherwise
    flip the ln_size slope. Winsorization does not drop rows.
  * Coefficients are time-series averaged over the 271 monthly estimates.
  * FM t-stat = mean / (std / sqrt(T)), std with ddof=1 — PLAIN iid FM t-stats.
    No Newey-West (the monthly OLS loop is implemented directly with numpy
    lstsq so no primitive default can inject HAC).

Outputs:
  results/table_6.md          — four panel tables (strategy x spec rows;
                                beta/ln_size/be_me/ret/ret_1_1/ret_36_13/ind/
                                ind_1_1/ind_36_13 columns), each cell
                                "ours mean (t) / paper mean (t)", + avg-obs line.
  results/cells_table_6.json  — all 416 contracted cells
                                {table:"T6", metric, paper, ours, tol_pct,
                                status} with Tier1/Tier2/FAIL/SKIP tallies.
  results/fm_interaction.png  — grouped bar of Panel-C s1 ret_{L,H} vs ind_{L,H}
                                coefficients across the four strategies.
  + a closing NYSE/AMEX-only (6,6) raw VW diagnostic (report-only).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
# replications/ root (parents[2]) pinned explicitly so this module is
# cwd-independent (paper_layout otherwise resolves REPLICATIONS_PATH vs cwd).
_REPLICATIONS_ROOT = Path(__file__).resolve().parents[2]

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from utils.paths import paper_layout  # noqa: E402

SLUG = "do_industries_explain_momentum"
LAYOUT = paper_layout(SLUG, replications_root=_REPLICATIONS_ROOT)

# FM sample window: January 1973 .. July 1995 (T = 271 months).
FM_START = pd.Period("1973-01", "M")
FM_END = pd.Period("1995-07", "M")
MIN_OBS = 30          # per-month cross-section size required to fit
DEPENDENT = "r_sb"    # DT size/BE-ME-adjusted return at month t
# Winsorization percentiles (A18): clip dep + each regressor to the within-month
# cross-sectional 1st/99th percentiles before fitting each monthly OLS.
WIN_LO = 0.01
WIN_HI = 0.99

# ---------------------------------------------------------------------------
# regressor -> panel-column mapping
# ---------------------------------------------------------------------------
# Fixed regressors (metric variable name -> panel column).
FIXED = {
    "beta": "beta_smoothed",
    "ln_size": "ln_size",
    "be_me": "ln_beme",          # paper's "BE/ME" column is log BE/ME (L1454)
    "ret_1_1": "mom1",           # individual short-term (1,1)
    "ret_36_13": "ret_36_13",    # individual long-term (36,13)
    "ind_1_1": "ind_mom1",       # industry short-term (1,1)
    "ind_36_13": "ind_ret_36_13",  # industry long-term (36,13)
}

# Strategy key -> (individual ret column, industry ind column).
STRAT_COLS = {
    # Panels A/B/C — no skip month
    "6_1": ("mom6", "ind_mom6"),
    "6_6": ("ret_6_6", "ind_ret_6_6"),
    "12_1": ("mom12", "ind_mom12"),
    "12_12": ("ret_12_12", "ind_ret_12_12"),
    # Panel D — month skipped (every window shifted one month)
    "7_2": ("ret_7_2", "ind_ret_7_2"),
    "6_6s": ("ret_6_6s", "ind_ret_6_6s"),
    "12_2": ("ret_12_2", "ind_ret_12_2"),
    "12_12s": ("ret_12_12s", "ind_ret_12_12s"),
}

# Panel -> strategies, and the regressor pattern (metric var names) per spec.
PANEL_STRATS = {
    "A": ["6_1", "6_6", "12_1", "12_12"],
    "B": ["6_1", "6_6", "12_1", "12_12"],
    "C": ["6_1", "6_6", "12_1", "12_12"],
    "D": ["7_2", "6_6s", "12_2", "12_12s"],
}
REG_PATTERN = {
    "A": {"s1": ["beta", "ln_size", "be_me", "ret"],
          "s2": ["beta", "ln_size", "be_me", "ret", "ret_1_1", "ret_36_13"]},
    "B": {"s1": ["beta", "ln_size", "be_me", "ind"],
          "s2": ["beta", "ln_size", "be_me", "ind", "ind_1_1", "ind_36_13"]},
    "C": {"s1": ["beta", "ln_size", "be_me", "ret", "ret_1_1", "ret_36_13", "ind"],
          "s2": ["beta", "ln_size", "be_me", "ret", "ret_1_1", "ret_36_13",
                 "ind", "ind_1_1", "ind_36_13"]},
    "D": {"s1": ["beta", "ln_size", "be_me", "ret", "ret_1_1", "ret_36_13", "ind"],
          "s2": ["beta", "ln_size", "be_me", "ret", "ret_1_1", "ret_36_13",
                 "ind", "ind_1_1", "ind_36_13"]},
}
# Fixed column display order for the markdown tables.
COL_ORDER = ["beta", "ln_size", "be_me", "ret", "ret_1_1", "ret_36_13",
             "ind", "ind_1_1", "ind_36_13"]


def resolve_cols(panel: str, strat: str, spec: str) -> list[tuple[str, str]]:
    """Return [(metric_var_name, panel_column), ...] for one regression."""
    ret_col, ind_col = STRAT_COLS[strat]
    out = []
    for var in REG_PATTERN[panel][spec]:
        if var == "ret":
            out.append((var, ret_col))
        elif var == "ind":
            out.append((var, ind_col))
        else:
            out.append((var, FIXED[var]))
    return out


# ---------------------------------------------------------------------------
# Fama-MacBeth — monthly unweighted OLS, plain iid t-stats (no NW, no winsor.)
# ---------------------------------------------------------------------------

def run_fm(month_groups: dict, months: pd.PeriodIndex,
           x_pairs: list[tuple[str, str]]) -> dict:
    """One Fama-MacBeth regression.

    x_pairs: [(metric_var_name, panel_column), ...]. Returns a dict with
    per-variable mean/t-stat, average observations/month, T (fitted months),
    the list of dropped months (month, n_valid_obs), and dep_clip_avg (average
    per-month count of dependent-variable rows clipped by the 1/99 winsorizer).
    """
    x_vars = [v for v, _ in x_pairs]
    x_cols = [c for _, c in x_pairs]
    all_cols = [DEPENDENT] + x_cols
    coef_rows = []
    nobs = []
    fitted = []
    dropped = []
    dep_clips = []
    for m in months:
        g = month_groups.get(m)
        if g is None:
            dropped.append((m, 0))
            continue
        d = g[all_cols].dropna()
        if len(d) < MIN_OBS:
            dropped.append((m, len(d)))
            continue
        # Winsorize (A18): clip the dependent AND each regressor to the
        # within-month cross-sectional 1st/99th percentiles, on exactly the
        # rows entering this regression. Does not drop rows.
        d = d.copy()
        dep = d[DEPENDENT]
        dep_lo, dep_hi = dep.quantile([WIN_LO, WIN_HI])
        n_clip = int(((dep < dep_lo) | (dep > dep_hi)).sum())
        for c in all_cols:
            lo, hi = d[c].quantile([WIN_LO, WIN_HI])
            d[c] = d[c].clip(lower=lo, upper=hi)
        y = d[DEPENDENT].to_numpy(dtype="float64")
        X = np.column_stack([np.ones(len(d)), d[x_cols].to_numpy(dtype="float64")])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        coef_rows.append(beta)
        nobs.append(len(d))
        fitted.append(m)
        dep_clips.append(n_clip)

    cdf = pd.DataFrame(coef_rows, columns=["const"] + x_vars, index=fitted)
    T = len(fitted)
    if T >= 2:
        means = cdf.mean(axis=0)
        stds = cdf.std(axis=0, ddof=1)
        tstats = means / (stds / np.sqrt(T))
    else:
        means = cdf.mean(axis=0)
        tstats = pd.Series(np.nan, index=means.index)

    return {
        "mean": {v: float(means[v]) for v in x_vars},
        "t": {v: float(tstats[v]) for v in x_vars},
        "avg_obs": float(np.mean(nobs)) if nobs else np.nan,
        "T": T,
        "dropped": dropped,
        "dep_clip_avg": float(np.mean(dep_clips)) if dep_clips else np.nan,
    }


def run_all(month_groups: dict, months: pd.PeriodIndex) -> tuple[dict, dict]:
    """Run all 32 regressions. Returns (results_by_key, ours_by_metric)."""
    results = {}
    ours = {}
    for panel in ("A", "B", "C", "D"):
        for strat in PANEL_STRATS[panel]:
            for spec in ("s1", "s2"):
                x_pairs = resolve_cols(panel, strat, spec)
                res = run_fm(month_groups, months, x_pairs)
                key = (panel, strat, spec)
                results[key] = res
                pre = f"p{panel}_{strat}_{spec}_"
                for var in [v for v, _ in x_pairs]:
                    ours[pre + var] = res["mean"][var]
                    ours[pre + var + "_t"] = res["t"][var]
    return results, ours


# ---------------------------------------------------------------------------
# per-cell comparison status (spec rule for T6)
# ---------------------------------------------------------------------------

def cell_status(ours, paper, tol_pct) -> str:
    if ours is None or (isinstance(ours, float) and np.isnan(ours)):
        return "SKIP"
    if abs(paper) < 0.0005:
        d = abs(ours - paper)
        if d <= 0.0002:
            return "Tier1"
        if d <= 0.001 or (ours >= 0) == (paper >= 0):
            return "Tier2"
        return "FAIL"
    rel = abs(ours - paper) / abs(paper)
    if rel <= tol_pct / 100.0:
        return "Tier1"
    if (ours >= 0) == (paper >= 0):
        return "Tier2"
    return "FAIL"


def build_cells(contract: dict, ours: dict) -> list[dict]:
    cells = []
    for t in contract["tables"]:
        if t["id"] != "T6":
            continue
        for m in t["metrics"]:
            name = m["name"]
            paper = float(m["value"])
            tol = float(m["tolerance_pct"])
            o = ours.get(name, np.nan)
            st = cell_status(o, paper, tol)
            cells.append(dict(
                table="T6", metric=name, paper=paper,
                ours=(None if (isinstance(o, float) and np.isnan(o)) else float(o)),
                tol_pct=tol, status=st))
    return cells


# ---------------------------------------------------------------------------
# markdown
# ---------------------------------------------------------------------------

def _cell(ours, paper_by, panel, strat, spec, var):
    """Format 'ours mean (t) / paper mean (t)' for one variable cell."""
    pre = f"p{panel}_{strat}_{spec}_"
    om = ours.get(pre + var)
    ot = ours.get(pre + var + "_t")
    pm = paper_by.get(pre + var)
    pt = paper_by.get(pre + var + "_t")
    if om is None or (isinstance(om, float) and np.isnan(om)):
        o_str = "—"
    else:
        o_str = f"{om:+.4f}({ot:+.2f})"
    if pm is None:
        p_str = "—"
    else:
        p_str = f"{pm:+.4f}({pt:+.2f})"
    return f"{o_str} / {p_str}"


def write_table_6_md(results, ours, paper_by):
    lines = [
        "# Table VI — Fama-MacBeth regressions of r_sb on controls and "
        "past-return variables",
        "",
        f"Sample: {FM_START} .. {FM_END} (T = 271 months). Dependent variable: "
        "r_sb (DT size/BE-ME-adjusted return). Monthly unweighted OLS, plain "
        "iid FM t-stats (no Newey-West). Winsorization (A18): dependent + every "
        "regressor clipped to the within-month 1st/99th percentiles before each "
        "monthly fit. Each cell: **ours mean (t) / paper mean (t)**.",
        "",
    ]
    panel_titles = {
        "A": "Panel A — Individual past-return variables",
        "B": "Panel B — Industry past-return variables",
        "C": "Panel C — Individual + industry past-return variables",
        "D": "Panel D — Month skipped (individual + industry)",
    }
    strat_labels = {
        "6_1": "(6,1)", "6_6": "(6,6)", "12_1": "(12,1)", "12_12": "(12,12)",
        "7_2": "(7,2)", "6_6s": "(6,6*)", "12_2": "(12,2)",
        "12_12s": "(12,12*)",
    }
    for panel in ("A", "B", "C", "D"):
        lines.append(f"## {panel_titles[panel]}")
        header = "| Strategy | Spec | " + " | ".join(COL_ORDER) + " |"
        sep = "|" + "---|" * (len(COL_ORDER) + 2)
        lines.append(header)
        lines.append(sep)
        for strat in PANEL_STRATS[panel]:
            for spec in ("s1", "s2"):
                row = [strat_labels[strat], spec]
                for var in COL_ORDER:
                    # blank the variable if it is not in this spec's pattern
                    if var not in REG_PATTERN[panel][spec]:
                        row.append("·")
                    else:
                        row.append(_cell(ours, paper_by, panel, strat, spec, var))
                lines.append("| " + " | ".join(row) + " |")
        # avg-obs-per-month line (per regression)
        obs = []
        for strat in PANEL_STRATS[panel]:
            for spec in ("s1", "s2"):
                r = results[(panel, strat, spec)]
                obs.append(f"{strat_labels[strat]} {spec}: {r['avg_obs']:.0f}")
        lines.append("")
        lines.append(f"**Avg obs/month** — " + "; ".join(obs) + ".")
        lines.append("")
    (LAYOUT.result_path("table_6.md")).write_text("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# plot — Panel C s1 interaction (ret vs ind across the four strategies)
# ---------------------------------------------------------------------------

def make_interaction_plot(ours):
    strats = ["6_1", "6_6", "12_1", "12_12"]
    labels = ["(6,1)", "(6,6)", "(12,1)", "(12,12)"]
    ret_coef = [ours[f"pC_{s}_s1_ret"] for s in strats]
    ind_coef = [ours[f"pC_{s}_s1_ind"] for s in strats]
    ret_t = [ours[f"pC_{s}_s1_ret_t"] for s in strats]
    ind_t = [ours[f"pC_{s}_s1_ind_t"] for s in strats]
    x = np.arange(len(strats))
    w = 0.38
    fig, ax = plt.subplots(figsize=(10, 6))
    b1 = ax.bar(x - w / 2, ret_coef, w, label="individual ret$_{L,H}$",
                color="#1e88e5")
    b2 = ax.bar(x + w / 2, ind_coef, w, label="industry ind$_{L,H}$",
                color="#f31d36")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Momentum strategy (L,H)")
    ax.set_ylabel("Panel C s1 Fama-MacBeth coefficient")
    ax.set_title("Table VI Panel C (s1): individual vs industry momentum "
                 "coefficients\n(industry momentum subsumes individual "
                 "momentum at 6 months)")
    ax.axhline(0, color="k", lw=0.7)
    ax.grid(True, alpha=0.3)
    for bars, ts in ((b1, ret_t), (b2, ind_t)):
        for rect, tv in zip(bars, ts):
            h = rect.get_height()
            ax.annotate(f"t={tv:+.1f}", xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 3 if h >= 0 else -10),
                        textcoords="offset points", ha="center", fontsize=8)
    ax.legend()
    fig.tight_layout()
    out = LAYOUT.result_path("fm_interaction.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# closing diagnostic — NYSE/AMEX-only raw VW (6,6) W-L
# ---------------------------------------------------------------------------

def nyse_amex_diagnostic(panel: pd.DataFrame) -> dict:
    """Raw VW 30/30 (6,6) W-L over 1963-07..1995-07, full universe vs
    NYSE/AMEX-only (exchcd IN (1,2), formation + holding restricted). Same
    engine as iteration 4's raw series (tables_1_2_3)."""
    import tables_1_2_3 as T

    def _series(p):
        cohorts = T.build_global_cohorts(p)
        wide = p.pivot(index="month", columns="permno", values="ret")
        s = T.individual_spread_series(wide, cohorts, hold=6)
        return T.restrict(s, T.RAW_START, T.RAW_END)

    full = _series(panel)
    fm, ft, fT = T.mean_t(full)
    fstd = float(full.dropna().std(ddof=1))

    ny = panel[panel["exchcd"].isin([1, 2])].copy()
    nys = _series(ny)
    nm, nt, nT = T.mean_t(nys)
    nstd = float(nys.dropna().std(ddof=1))

    return {
        "full": dict(mean=fm, std=fstd, t=ft, T=fT,
                     n_permnos=int(panel["permno"].nunique())),
        "nyse_amex": dict(mean=nm, std=nstd, t=nt, T=nT,
                          n_permnos=int(ny["permno"].nunique()),
                          n_rows=int(len(ny))),
    }


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

def run() -> int:
    t0 = time.time()
    LAYOUT.ensure()
    print("[stage 4] Table VI Fama-MacBeth regressions (Panels A-D, 32 regs)")

    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = panel["date"].dt.to_period("M")
    print(f"  panel {panel.shape}")

    # restrict to the FM sample window
    samp = panel[(panel["month"] >= FM_START) & (panel["month"] <= FM_END)].copy()
    months = pd.period_range(FM_START, FM_END, freq="M")
    month_groups = {m: g for m, g in samp.groupby("month")}
    print(f"  FM sample: {len(samp):,} rows over {samp['month'].nunique()} months "
          f"({FM_START}..{FM_END})")

    print("  [4.1] running 32 Fama-MacBeth regressions ...")
    results, ours = run_all(month_groups, months)

    # report avg obs + dropped months + winsorizer clip counts
    print("\n  === avg obs/month, dropped months, dep-clip count (A18) ===")
    any_dropped = []
    for panel_l in ("A", "B", "C", "D"):
        for strat in PANEL_STRATS[panel_l]:
            for spec in ("s1", "s2"):
                r = results[(panel_l, strat, spec)]
                tag = f"p{panel_l}_{strat}_{spec}"
                print(f"    {tag:<16s} avg_obs={r['avg_obs']:7.0f}  "
                      f"T={r['T']}  dropped={len(r['dropped'])}  "
                      f"dep_clip/mo={r['dep_clip_avg']:5.1f}")
                if r["dropped"]:
                    any_dropped.append((tag, r["dropped"]))
    if any_dropped:
        print("\n  *** DROPPED MONTHS (<30 obs): ***")
        for tag, dl in any_dropped:
            print(f"    {tag}: " + ", ".join(f"{m}({n})" for m, n in dl))
    else:
        print("\n  No months dropped (all 271 months fit >=30 obs in every spec).")
    clip_avgs = [results[(p, s, sp)]["dep_clip_avg"]
                 for p in ("A", "B", "C", "D") for s in PANEL_STRATS[p]
                 for sp in ("s1", "s2")]
    print(f"  Winsorizer engaged: dep clipped on {np.mean(clip_avgs):.1f} rows/month "
          f"on average (~{np.mean(clip_avgs) / np.mean([results[(p,s,sp)]['avg_obs'] for p in ('A','B','C','D') for s in PANEL_STRATS[p] for sp in ('s1','s2')]) * 100:.1f}% "
          f"of the cross-section; expect ~2% for a 1/99 cut).")

    # contract + cells
    contract = json.loads(LAYOUT.preparations_path(
        "tables_to_replicate.json").read_text())
    # name -> value lookup (means and t-stats are both stored under their own
    # names in tables_to_replicate.json, e.g. pA_6_1_s1_beta and ..._beta_t).
    paper_lookup = {m["name"]: m["value"] for t in contract["tables"]
                    if t["id"] == "T6" for m in t["metrics"]}

    cells = build_cells(contract, ours)
    out_json = LAYOUT.result_path("cells_table_6.json")
    out_json.write_text(json.dumps(cells, indent=1))

    tally = {}
    for c in cells:
        tally[c["status"]] = tally.get(c["status"], 0) + 1
    print(f"\n  [4.2] wrote {out_json.name}: {len(cells)} cells")
    print(f"  === T6 tally (n={len(cells)}) ===")
    print(f"    Tier1={tally.get('Tier1',0)}  Tier2={tally.get('Tier2',0)}  "
          f"FAIL={tally.get('FAIL',0)}  SKIP={tally.get('SKIP',0)}")
    fails = [c["metric"] for c in cells if c["status"] == "FAIL"]
    if fails:
        print(f"    FAIL cells ({len(fails)}):")
        for fn in fails:
            print(f"      {fn}")
    else:
        print("    No FAIL cells.")

    # markdown + plot
    print("  [4.3] writing table_6.md ...")
    write_table_6_md(results, ours, paper_lookup)
    print("  [4.4] writing fm_interaction.png ...")
    make_interaction_plot(ours)

    # closing diagnostic
    print("  [4.5] NYSE/AMEX-only (6,6) raw diagnostic ...")
    diag = nyse_amex_diagnostic(panel)
    f = diag["full"]; n = diag["nyse_amex"]
    print(f"    full universe : mean={f['mean']:.6f} std={f['std']:.6f} "
          f"t={f['t']:.3f} (T={f['T']}, {f['n_permnos']} permnos) "
          f"[ref 0.004135/0.035115/2.311]")
    print(f"    NYSE/AMEX only: mean={n['mean']:.6f} std={n['std']:.6f} "
          f"t={n['t']:.3f} (T={n['T']}, {n['n_permnos']} permnos, "
          f"{n['n_rows']:,} rows) [paper 0.0043/~0.0178/4.65]")

    print(f"\n[stage 4] done in {time.time() - t0:.1f}s")
    run.results = results
    run.ours = ours
    run.cells = cells
    run.tally = tally
    run.fails = fails
    run.diag = diag
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
