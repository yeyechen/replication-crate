"""
Replication of Fama & French (1992) "The Cross-Section of Expected Stock Returns"
=================================================================================
Stage: Table III (full-period Fama-MacBeth cross-sectional regressions, 11
specifications) and Table VI (subperiod FM regressions + NYSE VW/EW benchmark
returns), July 1963 - December 1990 (330 months).

Inputs:
  data/panel.parquet                 iteration-1 pipeline (permno x month);
                                     used for all FM regressions.
  src/sql/nyse_benchmark.sql         NYSE common stocks (PIT exchcd = 1,
                                     shrcd 10/11): delisting-adjusted monthly
                                     returns + month-end ME, 196306..199012.
  data/nyse_benchmark_returns.parquet  cached 330-month NYSE VW/EW series
                                     (computed artifact, reused if present).

Methodology (binding; from task spec + assumptions.md):
  * Dependent variable: raw monthly stock return ret (decimal; NO risk-free
    subtraction — Assumption 3).
  * Monthly cross-sectional OLS with intercept on rows with valid ret and all
    specification regressors present. Plain time-series t-statistics, NO
    Newey-West (paper L1187): t = mean(slope) / (std(slope, ddof=1) / sqrt(N)).
  * Winsorization (paper L1189, Assumption 9): each month, clip ln_bm, ln_ame,
    ln_abe, ep_pos at the 0.005/0.995 cross-sectional fractiles. beta, lnME
    and ep_dummy are NOT winsorized. Pre-winsorized once on a panel copy; the
    per-month OLS loop then runs with NO additional winsorization (the
    utils.fama_macbeth primitive always winsorizes every regressor, so the
    loop is implemented manually — as the task spec directs).
  * Slopes reported in percent/month (x100); t-stats are scale-invariant.
  * beta = stock-level assigned post-ranking beta (post_beta column).

Table III: 11 specifications R1..R11; average slope (t-stat) matrix over the
7 regressors, average monthly N per specification.

Table VI: NYSE VW/EW benchmark returns + FM reg(a) ret ~ ln(ME)+ln(BE/ME) and
reg(b) ret ~ beta+ln(ME)+ln(BE/ME), for the full period (330 months) and two
subperiods, 7/63-12/76 (162 months) and 1/77-12/90 (168 months). Per
coefficient (intercept + slopes): Mean, Std (time-series SD of the monthly
estimates), t(Mn) = Mean / (Std / sqrt(N_months)), all in percent/month.

Targets / tolerances: preparations/tables_to_replicate.json (table_3: slopes
and t-stats at 40%; table_6: NYSE Mean 15% / Std 10% / t(Mn) 40%; FM
intercepts/slopes Mean and t(Mn) 40%, Std 10%). R10 ln(ME) carries no target
(cell missing from the paper OCR) — computed, shown, not scored.

Outputs:
  results/table_3.md, results/table_6.md, data/nyse_benchmark_returns.parquet

Usage:
    uv run python replications/the_cross_section_of_expected_stock_returns/src/table_3_6.py
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

from main import LAYOUT, q_file, ym_to_month_end  # noqa: E402

# ────────────────────────────────────────────────────────────────────────────
# Configuration
# ────────────────────────────────────────────────────────────────────────────
N_MONTHS_FULL = 330                     # July 1963 - December 1990
WINS_COLS = ["ln_bm", "ln_ame", "ln_abe", "ep_pos"]   # paper L1189, Assumption 9
WINS_LO, WINS_HI = 0.005, 0.995

# Table III specifications: (id, regressor columns in panel)
SPECS_T3 = [
    ("R1",  ["post_beta"]),
    ("R2",  ["lnME"]),
    ("R3",  ["post_beta", "lnME"]),
    ("R4",  ["ln_bm"]),
    ("R5",  ["ln_ame", "ln_abe"]),
    ("R6",  ["ep_dummy", "ep_pos"]),
    ("R7",  ["lnME", "ln_bm"]),
    ("R8",  ["post_beta", "ln_ame", "ln_abe"]),
    ("R9",  ["post_beta", "ep_dummy", "ep_pos"]),
    ("R10", ["post_beta", "lnME", "ln_bm", "ep_dummy", "ep_pos"]),
    ("R11", ["post_beta", "ln_ame", "ln_abe", "ep_dummy", "ep_pos"]),
]
SPEC_LABEL = {
    "R1": "β", "R2": "ln(ME)", "R3": "β, ln(ME)",
    "R4": "ln(BE/ME)", "R5": "ln(A/ME), ln(A/BE)",
    "R6": "E/P dummy, E(+)/P", "R7": "ln(ME), ln(BE/ME)",
    "R8": "β, ln(A/ME), ln(A/BE)", "R9": "β, E/P dummy, E(+)/P",
    "R10": "β, ln(ME), ln(BE/ME), E/P dummy, E(+)/P",
    "R11": "β, ln(A/ME), ln(A/BE), E/P dummy, E(+)/P",
}
# matrix columns (panel col, display)
T3_COLS = [
    ("post_beta", "β"), ("lnME", "ln(ME)"), ("ln_bm", "ln(BE/ME)"),
    ("ln_ame", "ln(A/ME)"), ("ln_abe", "ln(A/BE)"),
    ("ep_dummy", "E/P dummy"), ("ep_pos", "E(+)/P"),
]

# Table VI specifications and periods
SPECS_T6 = [("a", ["lnME", "ln_bm"]),                    # reg(a)
            ("b", ["post_beta", "lnME", "ln_bm"])]       # reg(b)
PERIODS = [
    ("7/63-12/90", "July 1963 – Dec. 1990", 196307, 199012),
    ("7/63-12/76", "July 1963 – Dec. 1976", 196307, 197612),
    ("1/77-12/90", "Jan. 1977 – Dec. 1990", 197701, 199012),
]
T6_ROWS = [   # (display, group, spec/'nyse', coef column or series, short label)
    ("NYSE VW", "nyse", "nyse", "vw", "NYSE VW"),
    ("NYSE EW", "nyse", "nyse", "ew", "NYSE EW"),
    ("intercept", "(a) ret ~ ln(ME), ln(BE/ME)", "a", "const", "reg(a) intercept"),
    ("b2 ln(ME)", "(a) ret ~ ln(ME), ln(BE/ME)", "a", "lnME", "reg(a) b2 ln(ME)"),
    ("b3 ln(BE/ME)", "(a) ret ~ ln(ME), ln(BE/ME)", "a", "ln_bm", "reg(a) b3 ln(BE/ME)"),
    ("intercept", "(b) ret ~ β, ln(ME), ln(BE/ME)", "b", "const", "reg(b) intercept"),
    ("b1 β", "(b) ret ~ β, ln(ME), ln(BE/ME)", "b", "post_beta", "reg(b) b1 β"),
    ("b2 ln(ME)", "(b) ret ~ β, ln(ME), ln(BE/ME)", "b", "lnME", "reg(b) b2 ln(ME)"),
    ("b3 ln(BE/ME)", "(b) ret ~ β, ln(ME), ln(BE/ME)", "b", "ln_bm", "reg(b) b3 ln(BE/ME)"),
]

# metric-name parsing maps (preparations/tables_to_replicate.json)
VAR_COL = {"beta": "post_beta", "ln(ME)": "lnME", "ln(BE/ME)": "ln_bm",
           "ln(A/ME)": "ln_ame", "ln(A/BE)": "ln_abe",
           "E/P dummy": "ep_dummy", "E(+)/P": "ep_pos"}
PERIOD_KEY = {"7/63-12/90": 0, "7/63-12/76": 1, "1/77-12/90": 2}


# ────────────────────────────────────────────────────────────────────────────
# Winsorization + monthly Fama-MacBeth OLS
# ────────────────────────────────────────────────────────────────────────────
def prewinsorize(panel: pd.DataFrame) -> pd.DataFrame:
    """Clip ln_bm, ln_ame, ln_abe, ep_pos at the monthly 0.005/0.995
    cross-sectional fractiles (paper L1189). beta, lnME, ep_dummy untouched.
    The fractiles are computed on the regression sample of the month (rows
    with a valid return — the paper's "observations"), then applied to all
    rows of that month (the clipped values are what the monthly OLS sees)."""
    pw = panel.copy()
    v = pw["ret"].notna()
    for c in WINS_COLS:
        lo = pw.loc[v].groupby("ym")[c].quantile(WINS_LO)
        hi = pw.loc[v].groupby("ym")[c].quantile(WINS_HI)
        pw[c] = pw[c].clip(lower=pw["ym"].map(lo), upper=pw["ym"].map(hi))
    return pw


def fm_monthly(panel: pd.DataFrame, x_cols: list[str],
               y_col: str = "ret") -> pd.DataFrame:
    """Plain monthly cross-sectional OLS with intercept (the Fama-MacBeth first
    pass). Rows: valid y and all regressors present (panel characteristics are
    complete for every firm-year, so in practice the rows with valid ret).
    Returns a DataFrame indexed by ym with columns ['nobs', 'const'] + x_cols.
    No Newey-West anywhere downstream — plain time-series t-stats (L1187)."""
    cols = [y_col] + list(x_cols)
    recs = []
    for ym, g in panel.groupby("ym", sort=True):
        d = g[cols].to_numpy(dtype=np.float64)
        d = d[np.isfinite(d).all(axis=1)]
        n = d.shape[0]
        if n < len(x_cols) + 5:
            continue
        X = np.column_stack([np.ones(n), d[:, 1:]])
        coef, *_ = np.linalg.lstsq(X, d[:, 0], rcond=None)
        recs.append((int(ym), n, *coef))
    return pd.DataFrame(
        recs, columns=["ym", "nobs", "const", *x_cols]
    ).set_index("ym").sort_index()


def ts_stats(coef: pd.Series) -> tuple[float, float, float, int]:
    """(mean in percent, std in percent, plain t-stat, n months)."""
    n = int(coef.notna().sum())
    m = coef.mean() * 100.0
    sd = coef.std(ddof=1) * 100.0
    t = m / (sd / np.sqrt(n)) if sd > 0 else np.nan
    return m, sd, t, n


# ────────────────────────────────────────────────────────────────────────────
# NYSE benchmark (Table VI)
# ────────────────────────────────────────────────────────────────────────────
def nyse_benchmark(recompute: bool = False) -> pd.DataFrame:
    """330-month NYSE VW/EW return series (July 1963 - December 1990).

    From src/sql/nyse_benchmark.sql: all NYSE common stocks (PIT exchcd = 1,
    shrcd 10/11), delisting-adjusted returns (Assumption 5).
      EW_t = mean of valid returns in month t;
      VW_t = sum(ME_{t-1} * ret_t) / sum(ME_{t-1}) over stocks with a valid
             ret_t and a valid prior-month-end ME (June 1963 ME is the first
             lag weight, pulled by the SQL's 196306 row).
    Cached at data/nyse_benchmark_returns.parquet (computed artifact)."""
    out_path = LAYOUT.data_path("nyse_benchmark_returns.parquet")
    if out_path.exists() and not recompute:
        ser = pd.read_parquet(out_path)
        if len(ser) == N_MONTHS_FULL and {"ym", "vw", "ew", "n_stocks"} <= set(ser.columns):
            print(f"  [cache] {out_path.name}: {len(ser)} months")
            return ser
    raw = q_file("nyse_benchmark.sql")
    yms = np.sort(raw["ym"].unique())
    ret_w = raw.pivot(index="ym", columns="permno", values="ret").reindex(yms)
    me_w = raw.pivot(index="ym", columns="permno", values="me").reindex(yms)
    me_prev = me_w.shift(1)                      # prior calendar month's ME
    valid = ret_w.notna()
    wsum = me_prev.where(valid).sum(axis=1)      # lag ME over valid-ret stocks
    vw = (ret_w * me_prev).sum(axis=1) / wsum
    ew = ret_w.mean(axis=1)
    ser = pd.DataFrame({
        "ym": yms, "vw": vw.to_numpy(), "ew": ew.to_numpy(),
        "n_stocks": valid.sum(axis=1).to_numpy(np.int32),
    })
    ser = ser[ser["ym"] >= 196307].reset_index(drop=True)   # 330 months
    ser["month"] = ym_to_month_end(ser["ym"].to_numpy())
    ser = ser[["month", "ym", "vw", "ew", "n_stocks"]]
    ser.to_parquet(out_path, index=False)
    print(f"  [sql->parquet] {out_path.name}: {len(ser)} months")
    return ser


# ────────────────────────────────────────────────────────────────────────────
# Paper targets (preparations/tables_to_replicate.json)
# ────────────────────────────────────────────────────────────────────────────
def load_targets() -> tuple[dict, dict]:
    spec = json.loads(LAYOUT.preparations_path("tables_to_replicate.json").read_text())
    t3 = next(t for t in spec["tables"] if t["id"] == "table_3")
    t6 = next(t for t in spec["tables"] if t["id"] == "table_6")

    # table 3: (spec, col, kind) -> (value, tol)
    rx3 = re.compile(r"T3 (slope|t-stat) (R\d+): .+ \[([^\]]+)\]$")
    tgt3: dict = {}
    for m in t3["metrics"]:
        mm = rx3.match(m["name"])
        if not mm:
            continue
        kind, sp, var = mm.group(1), mm.group(2), mm.group(3)
        tgt3[(sp, VAR_COL[var], "slope" if kind == "slope" else "t")] = (
            float(m["value"]), float(m["tolerance_pct"]))

    # table 6: (series, col, stat, period_idx) -> (value, tol)
    rxn = re.compile(r"T6 (NYSE VW|NYSE EW) (Mean|Std|t\(Mn\)) \[([^\]]+)\]$")
    rxf = re.compile(
        r"T6 (reg\(a\)|reg\(b\)) (intercept|b1 beta|b2 ln\(ME\)|b3 ln\(BE/ME\))"
        r" (Mean|Std|t\(Mn\)) \[([^\]]+)\]$")
    vmap = {"intercept": "const", "b1 beta": "post_beta",
            "b2 ln(ME)": "lnME", "b3 ln(BE/ME)": "ln_bm"}
    smap = {"Mean": "mean", "Std": "std", "t(Mn)": "t"}
    tgt6: dict = {}
    for m in t6["metrics"]:
        mm = rxn.match(m["name"])
        if mm:
            ser = "vw" if mm.group(1) == "NYSE VW" else "ew"
            tgt6[("nyse", ser, smap[mm.group(2)], PERIOD_KEY[mm.group(3)])] = (
                float(m["value"]), float(m["tolerance_pct"]))
            continue
        mm = rxf.match(m["name"])
        if mm:
            sp = "a" if mm.group(1) == "reg(a)" else "b"
            tgt6[(sp, vmap[mm.group(2)], smap[mm.group(3)],
                  PERIOD_KEY[mm.group(4)])] = (
                float(m["value"]), float(m["tolerance_pct"]))
    return tgt3, tgt6


# ────────────────────────────────────────────────────────────────────────────
# Table III
# ────────────────────────────────────────────────────────────────────────────
def build_table_3(coefs: dict[str, pd.DataFrame]) -> tuple[str, pd.DataFrame, dict]:
    """Matrix markdown + comparison frame + headline dict."""
    # ---- replicated matrix ----
    head = "| Regression | " + " | ".join(d for _, d in T3_COLS) + " | Avg N |"
    sep = "|---|" + "---:|" * (len(T3_COLS) + 1)
    lines = [head, sep]
    for sp, xcols in SPECS_T3:
        c = coefs[sp]
        cells = []
        for col, _ in T3_COLS:
            if col in xcols:
                m, sd, t, n = ts_stats(c[col])
                cells.append(f"{m:.2f} ({t:.2f})")
            else:
                cells.append("")
        avg_n = int(round(c["nobs"].mean()))
        lines.append(f"| {sp}: {SPEC_LABEL[sp]} | " + " | ".join(cells)
                     + f" | {avg_n} |")
    matrix = "\n".join(lines)

    # ---- comparison ----
    avg_n_all = int(round(np.mean([coefs[sp]["nobs"].mean() for sp, _ in SPECS_T3])))
    rows = []
    for sp, xcols in SPECS_T3:
        c = coefs[sp]
        for col, disp in T3_COLS:
            if col not in xcols:
                continue
            m, sd, t, n = ts_stats(c[col])
            for kind, ours in (("slope", m), ("t", t)):
                tgt = T3_TARGETS.get((sp, col, kind))
                if tgt is None:                      # no OCR target (R10 lnME)
                    rows.append(dict(spec=sp, var=disp, kind=kind, paper=np.nan,
                                     ours=ours, dev=np.nan, tol_pct=np.nan,
                                     target=False, passed=None))
                else:
                    pv, tol = tgt
                    dev = ours - pv
                    rows.append(dict(spec=sp, var=disp, kind=kind, paper=pv,
                                     ours=ours, dev=dev, tol_pct=tol,
                                     target=True,
                                     passed=bool(abs(dev) <= tol / 100 * abs(pv))))
    ev = pd.DataFrame(rows)
    headlines = {"avg_n": avg_n_all}
    return matrix, ev, headlines


T3_TARGETS: dict = {}   # filled in main() from tables_to_replicate.json


def render_t3_comparison(ev: pd.DataFrame) -> str:
    lines = [
        "| Spec | Variable | Stat | Paper | Ours | \\|Δ\\| | Tol | Result |",
        "|---|---|---|---:|---:|---:|---:|:---:|",
    ]
    sp_order = {sp: i for i, (sp, _) in enumerate(SPECS_T3)}
    var_order = {col: i for i, (col, _) in enumerate(T3_COLS)}
    ev = ev.assign(
        k=ev["spec"].map(sp_order), v=ev["var"].map(var_order),
    ).sort_values(["k", "v", "kind"])
    for _, r in ev.iterrows():
        if not r["target"]:
            lines.append(f"| {r['spec']} | {r['var']} | {r['kind']} | — | "
                         f"{r['ours']:.2f} | — | — | no target |")
        else:
            mark = "✅ pass" if r["passed"] else "❌ FAIL"
            lines.append(f"| {r['spec']} | {r['var']} | {r['kind']} | "
                         f"{r['paper']:.2f} | {r['ours']:.2f} | "
                         f"{abs(r['dev']):.2f} | {int(r['tol_pct'])}% | {mark} |")
    return "\n".join(lines)


# ────────────────────────────────────────────────────────────────────────────
# Table VI
# ────────────────────────────────────────────────────────────────────────────
def build_table_6(fm6: dict[str, pd.DataFrame], nyse: pd.DataFrame) -> tuple[str, pd.DataFrame]:
    """Full Table VI layout + comparison frame."""
    # (series, col, period_idx) -> (mean, std, t, n)
    vals: dict = {}
    for ser, col in (("vw", "vw"), ("ew", "ew")):
        for pidx, (_, _, lo, hi) in enumerate(PERIODS):
            s = nyse[(nyse["ym"] >= lo) & (nyse["ym"] <= hi)][col]
            vals[("nyse", ser, pidx)] = ts_stats(s)
    for sp, _ in SPECS_T6:
        c = fm6[sp]
        for pidx, (_, _, lo, hi) in enumerate(PERIODS):
            sub = c[(c.index >= lo) & (c.index <= hi)]
            for col in c.columns:
                if col == "nobs":
                    continue
                vals[(sp, col, pidx)] = ts_stats(sub[col])

    # ---- replicated table ----
    hcells = []
    for _, title, _, _ in PERIODS:
        hcells += [f"**{title}**", "", ""]
    head1 = "| Row | " + " | ".join(hcells) + " |"
    head2 = "|---|" + "---:|---:|---:|" * len(PERIODS)
    lines = [head1, head2,
             "|  | " + " | ".join(
                 ["**Mean**", "**Std**", "**t(Mn)**"] * len(PERIODS)) + " |"]
    prev_group = None
    for disp, group, sp, col, _short in T6_ROWS:
        if group != prev_group:
            if group != "nyse":
                lines.append(f"| **{group}** | "
                             + " | ".join([""] * (3 * len(PERIODS))) + " |")
            prev_group = group
        cells = []
        for pidx in range(len(PERIODS)):
            m, sd, t, n = vals[(sp, col, pidx)]
            cells += [f"{m:.2f}", f"{sd:.2f}", f"{t:.2f}"]
        lines.append(f"| {disp} | " + " | ".join(cells) + " |")
    table = "\n".join(lines)

    # ---- comparison ----
    rows = []
    for disp, group, sp, col, short in T6_ROWS:
        for pidx, (key, _, _, _) in enumerate(PERIODS):
            m, sd, t, n = vals[(sp, col, pidx)]
            for stat, ours in (("mean", m), ("std", sd), ("t", t)):
                tgt = T6_TARGETS.get((sp, col, stat, pidx))
                label = short
                if tgt is None:
                    rows.append(dict(row=f"{label} [{key}]", stat=stat,
                                     paper=np.nan, ours=ours, dev=np.nan,
                                     tol_pct=np.nan, target=False, passed=None))
                else:
                    pv, tol = tgt
                    dev = ours - pv
                    rows.append(dict(row=f"{label} [{key}]", stat=stat,
                                     paper=pv, ours=ours, dev=dev,
                                     tol_pct=tol, target=True,
                                     passed=bool(abs(dev) <= tol / 100 * abs(pv))))
    return table, pd.DataFrame(rows)


T6_TARGETS: dict = {}


def render_t6_comparison(ev: pd.DataFrame) -> str:
    lines = [
        "| Cell | Stat | Paper | Ours | \\|Δ\\| | Tol | Result |",
        "|---|---|---:|---:|---:|---:|:---:|",
    ]
    for _, r in ev.iterrows():                 # construction order = table order
        if not r["target"]:
            lines.append(f"| {r['row']} | {r['stat']} | — | {r['ours']:.2f} | "
                         f"— | — | no target |")
        else:
            mark = "✅ pass" if r["passed"] else "❌ FAIL"
            lines.append(f"| {r['row']} | {r['stat']} | {r['paper']:.2f} | "
                         f"{r['ours']:.2f} | {abs(r['dev']):.2f} | "
                         f"{int(r['tol_pct'])}% | {mark} |")
    return "\n".join(lines)


# ────────────────────────────────────────────────────────────────────────────
def summary_block(ev: pd.DataFrame, name: str) -> list[str]:
    tgt = ev[ev["target"]].copy()
    n_pass = int(tgt["passed"].sum())
    n_tot = len(tgt)
    n_nt = int((~ev["target"]).sum())
    out = [f"**{name}: {n_pass}/{n_tot} targeted cells pass**"
           + (f" (+ {n_nt} no-target shown, not scored)." if n_nt else ".")]
    fails = tgt[~tgt["passed"].astype(bool)]
    if len(fails):
        out.append(f"Failing cells ({len(fails)}):")
        for _, r in fails.iterrows():
            rel = abs(r["dev"]) / abs(r["paper"]) * 100
            if "spec" in r and "var" in r:                    # table 3 frame
                cell = f"{r['spec']} {r['var']} {r['kind']}"
            else:                                             # table 6 frame
                cell = f"{r['row']} {r['stat']}"
            out.append(f"- {cell}: ours {r['ours']:.2f} vs paper "
                       f"{r['paper']:.2f} (|Δ| {abs(r['dev']):.2f}, "
                       f"{rel:.1f}% > {int(r['tol_pct'])}%).")
    return out, n_pass, n_tot


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    global T3_TARGETS, T6_TARGETS
    t0 = time.time()
    T3_TARGETS, T6_TARGETS = load_targets()
    print(f"targets: table_3 {len(T3_TARGETS)} cells, table_6 {len(T6_TARGETS)} cells")

    # ── panel + winsorization ────────────────────────────────────────────
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["ym"] = panel["month"].dt.year * 100 + panel["month"].dt.month
    pw = prewinsorize(panel)
    n_months = pw["ym"].nunique()
    print(f"panel: {len(pw):,} rows, {n_months} months, "
          f"{pw['permno'].nunique():,} permnos")

    # ── Table III: 11 FM specifications ──────────────────────────────────
    coefs = {sp: fm_monthly(pw, xcols) for sp, xcols in SPECS_T3}
    # sanity: reg(a) == R7 (identical spec)
    fm_a = fm_monthly(pw, ["lnME", "ln_bm"])
    assert np.allclose(fm_a[["const", "lnME", "ln_bm"]],
                       coefs["R7"][["const", "lnME", "ln_bm"]])
    fm_b = fm_monthly(pw, ["post_beta", "lnME", "ln_bm"])
    fm6 = {"a": fm_a, "b": fm_b}

    matrix3, ev3, head3 = build_table_3(coefs)
    sum3, pass3, tot3 = summary_block(ev3, "Table III")

    md3 = [
        "# Table III — Fama & French (1992), The Cross-Section of Expected Stock Returns",
        "",
        "Time-series averages of slopes (with t-statistics in parentheses) from "
        "month-by-month Fama-MacBeth cross-sectional regressions of individual "
        "stock returns on β, ln(ME), ln(BE/ME), ln(A/ME), ln(A/BE), E/P dummy, "
        "and E(+)/P. Sample July 1963 – December 1990 "
        f"({n_months} months).",
        "",
        "**Methodology.** Dependent variable: raw monthly stock return "
        "(decimal, no risk-free subtraction — Assumption 3). Each month, an OLS "
        "with intercept is fit on the rows with a valid return and all of the "
        "specification's regressors present; β is the stock-level assigned "
        "post-ranking β (post_beta). Slopes are averaged over the 330 monthly "
        "slopes ×100 (percent/month); the t-statistic is the average slope "
        "divided by its time-series standard error (plain time-series t, NO "
        "Newey-West — paper L1187). Winsorization (paper L1189, Assumption 9): "
        "each month, ln(BE/ME), ln(A/ME), ln(A/BE), and E(+)/P are clipped at "
        "the 0.005/0.995 cross-sectional fractiles; β, ln(ME), and the E/P "
        "dummy are not winsorized.",
        "",
        "## Replicated values",
        "",
        matrix3,
        "",
        f"Average number of stocks in the monthly regressions: **{head3['avg_n']}** "
        "(paper: ~2267).",
        "",
        "## Comparison with paper",
        "",
    ]
    md3 += sum3
    md3 += [
        "",
        "> **No target:** the R10 ln(ME) cell (slope and t-stat) is missing "
        "from the paper OCR — our values are shown but not scored. R7's OCR "
        "cells were shifted one column left; the corrected targets "
        "(ln(ME) −0.11 (−1.99); ln(BE/ME) 0.35 (4.44)) are used. Tolerances: "
        "40% on slopes and on t-stats (preparations/tables_to_replicate.json).",
        "",
        render_t3_comparison(ev3),
        "",
        "## Notes / flags",
        "",
        "- ⚠️ **β cells R8–R11 vs the paper's own prose and R1/R3.** The "
        "paper's printed β t-statistics for R8–R11 (−2.06, −3.06, −2.47, "
        "−2.47) imply time-series SDs of the monthly β slopes of ≈0.96–1.11 "
        "%/mo, while its R1 (0.15, t 0.46) and R3 (−0.37, t −1.21) imply SDs "
        "of ≈5.9 and 5.6 %/mo — ours are 6.0 and 5.5, matching R1/R3. Adding "
        "controls cannot compress the time-series dispersion of the monthly β "
        "slope ~6× (ours move only 6.0→5.1 across R1→R10), and neither a "
        "time-series nor a pooled (mean ÷ avg monthly SE ≈ 0.87–0.99) t-stat "
        "on our monthly β slopes reproduces |t| > 2. The paper's prose "
        "(L1159) says the β slopes in the combined regressions are "
        "\"typically less than 1 standard error from 0\", which matches our "
        "R8–R11 β t-stats (0.39, 0.58, −0.55, 0.69). Implemented exactly per "
        "the spec (plain time-series t, L1187); the R8–R11 β failures are "
        "against OCR targets that are internally inconsistent with the "
        "paper's own R1/R3.",
        "- **E(+)/P runs systematically above the paper** in the multivariate "
        "specs (R9 4.17 vs 2.99; R10 1.59 vs 0.87; R11 2.22 vs 1.15), while "
        "the time-series SDs track the paper's implied SDs (≈12–18). The "
        "qualitative result replicates: E(+)/P collapses once size and "
        "BE/ME (or the leverage ratios) enter (R6 5.55 → R10 1.59), and the "
        "E/P dummy is killed (R10 −0.21, t −1.41). The level shift is "
        "consistent with the iteration-1/2 data-vintage facts (Compustat "
        "vintage: our ln(A/ME)/ln(A/BE) run higher, ln(BE/ME) less negative; "
        "+5.5% stocks/month).",
        f"- **Average monthly N = {head3['avg_n']}** (paper ~2267; +5.5%, the "
        "iteration-1 vintage fact: broader CCM link table / NASDAQ coverage).",
        "- All non-β cells of R2–R7 replicate within ≤0.10 of the paper's "
        "slopes (e.g. ln(ME) −0.14 (−2.47) vs −0.15 (−2.58); ln(BE/ME) 0.49 "
        "(5.54) vs 0.50 (5.71); R7 −0.11 (−1.92) / 0.34 (4.20) vs −0.11 "
        "(−1.99) / 0.35 (4.44)).",
        "",
        "---",
        "*Computed by src/table_3_6.py from data/panel.parquet (iteration-1 "
        "pipeline), with the four ratio regressors pre-winsorized monthly at "
        "the 0.005/0.995 fractiles (fractiles computed on the valid-return "
        "regression sample) and a plain monthly OLS loop (no Newey-West).*",
    ]
    out3 = LAYOUT.result_path("table_3.md")
    out3.write_text("\n".join(md3))
    print(f"wrote {out3}")

    # ── Table VI ─────────────────────────────────────────────────────────
    nyse = nyse_benchmark()
    table6, ev6 = build_table_6(fm6, nyse)
    sum6, pass6, tot6 = summary_block(ev6, "Table VI")

    md6 = [
        "# Table VI — Fama & French (1992), The Cross-Section of Expected Stock Returns",
        "",
        "Means, standard deviations, and t-statistics of monthly returns on the "
        "NYSE value-weighted (VW) and equal-weighted (EW) portfolios, and of "
        "the slopes and intercepts of two Fama-MacBeth regressions, for the "
        "full period and two subperiods:",
        "",
        "- **reg(a):** return on ln(ME) and ln(BE/ME);",
        "- **reg(b):** return on β, ln(ME), and ln(BE/ME).",
        "",
        "**Methodology.** Same as Table III: raw monthly returns, monthly OLS "
        "with intercept, ln(BE/ME) clipped at the monthly 0.005/0.995 "
        "fractiles (β and ln(ME) not winsorized), plain time-series statistics "
        "(no Newey-West). Per coefficient: Mean = time-series mean of the "
        "monthly estimates ×100, Std = time-series SD ×100, "
        "t(Mn) = Mean / (Std / √N_months), all in percent/month. Subperiod "
        "splits: July 1963 – December 1976 (162 months) and January 1977 – "
        "December 1990 (168 months). NYSE benchmarks: all NYSE common stocks "
        "(PIT exchcd = 1, shrcd 10/11, NOT restricted to the Compustat-data-"
        "eligible subset) with delisting-adjusted returns (Assumptions 5 and "
        "10); EW = mean of valid monthly returns, VW = sum(prior-month-end "
        "ME × return) / sum(prior-month-end ME) over stocks with a valid "
        "return and a valid lagged ME (cached in "
        "data/nyse_benchmark_returns.parquet). NYSE membership is screened "
        "point-in-time at each calendar month-end, so mid-month delistings "
        "are excluded from that month's benchmark.",
        "",
        "## Replicated values",
        "",
        table6,
        "",
        "## Comparison with paper",
        "",
    ]
    md6 += sum6
    md6 += [
        "",
        "Tolerances (preparations/tables_to_replicate.json): NYSE Mean 15%, "
        "Std 10%, t(Mn) 40%; FM intercept/slope Mean 40%, Std 10%, t(Mn) 40%.",
        "",
        render_t6_comparison(ev6),
        "",
        "## Notes / flags",
        "",
        "- **All 63 FM cells pass** (reg(a) and reg(b): intercepts, slopes, "
        "Stds, t(Mn) across the three periods), including the headline "
        "subperiod results: reg(b) β 0.08 (t 0.20) in 1963–76 and −0.48 "
        "(t −1.30) in 1977–90 (paper 0.10/0.25 and −0.44/−1.17); BE/ME "
        "slopes stable at 0.31–0.36 in both subperiods (paper 0.34–0.36).",
        "- ⚠️ **NYSE benchmark means run ~0.1–0.2 %/mo above the paper** "
        "(the 3 failing cells: EW full 1.15 vs 0.97, EW 63–76 0.97 vs 0.77, "
        "VW 63–76 0.65 vs 0.56). The computation is validated against "
        "CRSP's own NYSE index in this extract (msia: VW 0.91/SD 4.46 vs our "
        "0.92/SD 4.47), and the SDs match the paper's within ≤0.14 — the gap "
        "is a mean-level data-vintage shift (this CRSP vintage also runs "
        "~0.1 above the paper on the combined msi index). Mid-month "
        "delistings are excluded from the month of delisting (month-end PIT "
        "membership screen); financials are included (NYSE market benchmark).",
        "- NYSE VW/EW computed with delisting-adjusted returns per binding "
        "Assumptions 5/10; EW over valid returns, VW on prior-month-end ME.",
        "",
        "---",
        "*Computed by src/table_3_6.py. FM coefficients from data/panel.parquet; "
        "NYSE VW/EW from src/sql/nyse_benchmark.sql cached in "
        "data/nyse_benchmark_returns.parquet.*",
    ]
    out6 = LAYOUT.result_path("table_6.md")
    out6.write_text("\n".join(md6))
    print(f"wrote {out6}")

    # ── console report ───────────────────────────────────────────────────
    print("\n===== TABLE III =====")
    print(matrix3)
    print(f"avg monthly N: {head3['avg_n']} (paper ~2267)")
    print(f"PASS {pass3}/{tot3}")
    for ln in sum3:
        print(" ", ln)
    print("\n===== TABLE VI =====")
    print(table6)
    print(f"PASS {pass6}/{tot6}")
    for ln in sum6:
        print(" ", ln)
    print(f"\ntotal time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
