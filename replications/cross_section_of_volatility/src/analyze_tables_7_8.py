"""
Tables VII & VIII — Ang, Hodrick, Xing, Zhang (2006), "The Cross-Section
of Volatility and Expected Returns".

Robustness of the idiosyncratic-volatility (IVOL) anomaly to cross-sectional
controls via DEPENDENT DOUBLE SORTS.

    Table VII  — IVOL quintile portfolios controlling for size, book-to-market,
                 leverage, volume, turnover, coskewness (each a dependent double
                 sort), plus an NYSE-only single sort and a 5x5 Size detail grid.
    Table VIII — IVOL quintile portfolios controlling for past returns
                 (Panel A: past 1/6/12-month momentum double sorts;
                  Panel B: 5x5 past-12-month x IVOL detail grid).

Methodology (per the task spec + paper §II.C):
    For each control C (dependent double sort), each formation month t:
      1. Sort ALL stocks with a valid C into quintiles on C (outer sort).
      2. Within each C-quintile, sort stocks into quintiles on IVOL (inner sort).
      3. Value-weight each (C-q, IVOL-q) cell by month-t market equity, using the
         month-(t+1) return as the holding return.
      4. For each IVOL quintile, AVERAGE the cell returns across the 5 C-quintiles
         (equal-weight the control quintiles) -> one monthly return series per
         IVOL quintile.
      5. FF-3 alpha = intercept of (R - rf) ~ MKT-RF + SMB + HML, Newey-West(4).

    NYSE Stocks Only: restrict the universe to hexcd == 1, single IVOL sort.

Timing (matches analyze_table6.py, verified to reproduce Table VI):
    * Panel row t stores all signals contemporaneously at month t.
    * Sort on the row-t signal, earn the return in month t+1
      (attach_next_month_return). First holding month = 1963-07, last = 2000-12.
    * Momentum controls (Table VIII) are measured on the windows the task
      specifies, expressed relative to the signal row t:
          past1  = ret_t                 (FORMATION-month return; issue M3)
          past6  = cumret(t-6  .. t-1)
          past12 = cumret(t-12 .. t-1)
      past1 uses the formation-month return (portfolios are formed at the end
      of month t, so "past 1-month return" includes month t). past6/past12
      include the most recent completed month (t-1) and do NOT skip it
      (unlike the panel's `mom` = cumret(t-12 .. t-2), which skips t-1).

Conventions:
    * FF factors from ff.four_factor_monthly are DECIMAL (no /100); alphas are
      multiplied by 100 to report percent per month.
    * Breakpoints use ALL stocks (simple 20/40/60/80 pctile cuts), consistent
      with the Table VI pipeline (task silent on NYSE breakpoints for controls).
    * Stocks missing a given control are dropped from THAT control's sort only
      (each control is an independent sort).

Outputs:
    results/table_7.md
    results/table_8.md
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_hac

from clickhouse_driver import Client

from utils.env import get_clickhouse_config, load_project_env
from utils.paths import paper_layout
from utils.quantile import assign_quantiles

# ── paths / env ─────────────────────────────────────────────────────
load_project_env()
SLUG = "cross_section_of_volatility"
LAYOUT = paper_layout(SLUG)
SQL_DIR = LAYOUT.src_path("sql")
CFG = get_clickhouse_config()

NW_LAGS = 4          # Newey-West lags for alpha t-stats (task spec)
N_Q = 5              # quintiles


# ── Paper values (AHXZ 2006), FF-3 alphas in %/month ────────────────
# Table VII rows: [Q1, Q2, Q3, Q4, Q5, 5-1]
PAPER_7 = {
    "NYSE Stocks Only":        [0.06, 0.04, 0.02, -0.04, -0.60, -0.66],
    "Controlling for Size":    [0.11, 0.18, 0.09, -0.15, -0.93, -1.04],
    "Controlling for B/M":     [0.61, 0.69, 0.71, 0.50, -0.19, -0.80],
    "Controlling for Leverage":[0.11, 0.11, 0.08, -0.24, -1.12, -1.23],
    "Controlling for Volume":  [-0.03, 0.02, -0.01, -0.39, -1.25, -1.22],
    "Controlling for Turnover":[0.11, 0.03, -0.11, -0.49, -1.34, -1.46],
    "Controlling for Coskew":  [-0.02, -0.00, 0.01, -0.37, -1.40, -1.38],
}
# Table VII Size detail grid: rows = size quintile, [Q1..Q5, 5-1]
PAPER_7_SIZE = {
    "Small 1": [0.11, 0.26, 0.31, 0.06, -0.43, -0.55],
    "2":       [0.19, 0.20, -0.07, -0.65, -1.73, -1.91],
    "3":       [0.12, 0.21, 0.03, -0.27, -1.49, -1.61],
    "4":       [0.03, 0.22, 0.17, -0.03, -0.82, -0.86],
    "Large 5": [0.09, 0.04, 0.03, 0.14, -0.17, -0.26],
}
# Table VIII Panel A: [Q1, Q2, Q3, Q4, Q5, 5-1]
PAPER_8A = {
    "Past 1 month":  [0.07, 0.08, 0.09, -0.05, -0.59, -0.66],
    "Past 6 months": [-0.01, -0.12, -0.28, -0.45, -1.11, -1.10],
    "Past 12 months":[0.01, -0.05, -0.28, -0.64, -1.21, -1.22],
}
# Table VIII Panel B: 5x5 past-12-month x IVOL grid, [Q1..Q5, 5-1]
PAPER_8B = {
    "Losers 1":  [-0.41, -0.83, -1.44, -2.11, -2.66, -2.25],
    "2":         [-0.08, -0.24, -0.64, -1.09, -1.70, -1.62],
    "3":         [-0.06, -0.11, -0.26, -0.48, -1.03, -0.97],
    "4":         [0.15, 0.07, 0.23, -0.03, -0.65, -0.80],
    "Winners 5": [0.45, 0.85, 0.71, 0.52, -0.03, -0.48],
}


# ── FF factors ──────────────────────────────────────────────────────
def load_ff_monthly() -> pd.DataFrame:
    """Monthly FF4 factors + rf (DECIMAL) from ff.four_factor_monthly."""
    sql = (SQL_DIR / "ff_monthly.sql").read_text()
    c = Client(host=CFG["host"], port=int(CFG["port"]), user=CFG["user"],
               password=CFG["password"], settings={"max_execution_time": 60})
    data, cols = c.execute(sql, with_column_types=True)
    ff = pd.DataFrame(data, columns=[x[0] for x in cols])
    ff["month"] = pd.to_datetime(ff["month"])
    return ff.set_index("month").sort_index()


# ── timing helpers ──────────────────────────────────────────────────
def attach_next_month_return(panel: pd.DataFrame) -> pd.DataFrame:
    """Row (permno, month=t) gets ret_next = that stock's return in month
    t+1 (explicit calendar-month merge, identical to analyze_table6.py)."""
    nxt = panel[["permno", "month", "ret"]].rename(
        columns={"month": "month_hold", "ret": "ret_next"})
    df = panel.copy()
    df["month_hold"] = df["month"] + pd.DateOffset(months=1)
    df = df.merge(nxt, on=["permno", "month_hold"], how="left")
    return df.drop(columns=["month_hold"])


def compute_momentum(panel: pd.DataFrame) -> pd.DataFrame:
    """Past-return signals (relative to signal row t) for Table VIII:
        past1  = ret_t            (FORMATION-month return — same month as IVOL;
                                   outer iteration 2 / issue M3 convention)
        past6  = cumret(t-6  .. t-1)   (includes most recent completed month t-1)
        past12 = cumret(t-12 .. t-1)
    past1 uses the formation-month return ret_t: portfolios are formed at the
    END of month t using month-t data, so "past 1-month return" at formation
    naturally includes month t's return (the same month the IVOL signal is
    measured from). past6/past12 keep the window ending at t-1 (assumption
    A18: that convention matches the paper's past-6 and past-12 best).

    NOTE (issue M3 result): empirically ret_t does NOT attenuate the IVOL 5-1
    toward the paper's -0.66 (it gives -1.25 vs -1.15 for ret_{t-1}); the
    paper's strong attenuation (-1.31 -> -0.66) is not reproduced under
    either convention. Implemented as the formation-month convention per the
    task spec; flagged for the Replicator (see assumptions.md A21)."""
    df = panel.sort_values(["permno", "month"]).reset_index(drop=True).copy()
    lr = np.log1p(df["ret"].clip(lower=-0.999999))
    df["logret"] = lr
    grp = df.groupby("permno", sort=False)["logret"]

    def _cumret_lag(s: pd.Series, w: int) -> pd.Series:
        # rolling sum of logrets over window w ending at current row,
        # then shift(1) so the window ends at t-1 -> cumret(t-w .. t-1)
        return np.expm1(s.rolling(w, min_periods=w).sum().shift(1))

    df["past1"] = df["ret"]  # formation-month return (month t)
    df["past6"] = grp.transform(lambda s: _cumret_lag(s, 6))
    df["past12"] = grp.transform(lambda s: _cumret_lag(s, 12))
    return df.drop(columns=["logret"])


# ── portfolio construction ──────────────────────────────────────────
def _qcut5(s: pd.Series) -> pd.Series:
    """Quintile labels 1..5 with a rank fallback for tie-heavy groups."""
    try:
        return pd.qcut(s, N_Q, labels=False, duplicates="drop") + 1
    except (ValueError, TypeError):
        n = int(s.notna().sum())
        return np.ceil(s.rank(method="first") / max(n, 1) * N_Q)


def dependent_double_sort(df: pd.DataFrame, control: str) -> pd.DataFrame:
    """Monthly dependent double sort: outer = control, inner = IVOL.
    Returns cell-level VW returns: columns [month, cq, iq, VW]."""
    cols = ["month", "permno", "ivol", "me", "ret_next", control]
    sub = df[cols].dropna().copy()
    sub["cq"] = assign_quantiles(sub, "month", control, n_bins=N_Q,
                                 warn_fallback=False)
    sub["iq"] = (sub.groupby(["month", "cq"], group_keys=False)["ivol"]
                 .transform(_qcut5))
    sub = sub.dropna(subset=["iq"]).copy()
    sub["iq"] = sub["iq"].astype(int)
    sub["rw"] = sub["ret_next"] * sub["me"]
    cell = (sub.groupby(["month", "cq", "iq"], as_index=False)
            .agg(rw=("rw", "sum"), me=("me", "sum"), n=("permno", "count")))
    cell["VW"] = cell["rw"] / cell["me"]
    return cell


def single_sort_vw(df: pd.DataFrame) -> dict:
    """NYSE-only single IVOL sort. Returns {iq: monthly VW return Series}."""
    sub = df[["month", "permno", "ivol", "me", "ret_next"]].dropna().copy()
    sub["iq"] = assign_quantiles(sub, "month", "ivol", n_bins=N_Q,
                                 warn_fallback=False)
    sub = sub.dropna(subset=["iq"]).copy()
    sub["iq"] = sub["iq"].astype(int)
    sub["rw"] = sub["ret_next"] * sub["me"]
    agg = (sub.groupby(["month", "iq"], as_index=False)
           .agg(rw=("rw", "sum"), me=("me", "sum")))
    agg["VW"] = agg["rw"] / agg["me"]
    piv = agg.pivot(index="month", columns="iq", values="VW")
    return {q: piv[q].dropna().sort_index() for q in range(1, N_Q + 1)}


def average_over_control(cell: pd.DataFrame) -> dict:
    """Average cell VW returns across the control quintiles (equal-weight)
    for each IVOL quintile -> {iq: monthly return Series}."""
    p = cell.groupby(["month", "iq"])["VW"].mean()
    piv = p.unstack("iq")
    return {q: piv[q].dropna().sort_index() for q in range(1, N_Q + 1)}


# ── alpha estimation ────────────────────────────────────────────────
def ff3_alpha(r: pd.Series, ff: pd.DataFrame, subtract_rf: bool = True):
    """FF-3 alpha (%/month) + NW(4) t-stat. r = TOTAL return series indexed
    by FORMATION month t (its value is the return earned in the HOLDING month
    t+1). Regress (r - rf) on MKT-RF, SMB, HML. For a zero-investment spread,
    pass subtract_rf=False.

    CRITICAL alignment: the return earned in month t+1 must be regressed on
    the factors of month t+1 (contemporaneous), not month t. We therefore
    relabel the series to the holding month (t -> t+1) before merging with
    the factor frame. Failing to do so pairs each month's return with the
    PRIOR month's factors, driving factor betas to ~0 and collapsing the
    "alpha" toward the mean excess return (verified against Table VI: with
    this relabeling, baseline IVOL Q1..Q5 alphas = -0.00, 0.08, 0.09, -0.29,
    -1.17 vs paper 0.04, 0.09, 0.08, -0.32, -1.27; market betas ~1.0)."""
    r = r.copy()
    r.index = r.index + pd.DateOffset(months=1)  # formation month -> holding month
    d = pd.concat([r.rename("r"), ff], axis=1, join="inner").dropna()
    if len(d) < 12:
        return (np.nan, np.nan, int(len(d)))
    y = d["r"] - d["rf"] if subtract_rf else d["r"]
    X = sm.add_constant(d[["mkt_rf", "smb", "hml"]].astype(float))
    m = sm.OLS(y, X).fit()
    try:
        se = float(np.sqrt(cov_hac(m, nlags=NW_LAGS)[0, 0]))
    except Exception:
        se = float(m.bse["const"])
    a = float(m.params["const"])
    return (a * 100.0, a / se if se > 0 else np.nan, int(len(d)))


def port_alphas(ports: dict, ff: pd.DataFrame) -> dict:
    """FF-3 alphas + t-stats for IVOL quintiles 1..5 and the 5-1 spread."""
    out = {}
    for q in range(1, N_Q + 1):
        a, t, n = ff3_alpha(ports[q], ff, subtract_rf=True)
        out[q] = {"alpha": a, "t": t, "n": n}
    common = ports[5].index.intersection(ports[1].index).sort_values()
    spread = ports[5].loc[common] - ports[1].loc[common]
    a, t, n = ff3_alpha(spread, ff, subtract_rf=False)
    out["5-1"] = {"alpha": a, "t": t, "n": n}
    return out


def cell_alphas(cell: pd.DataFrame, ff: pd.DataFrame) -> dict:
    """FF-3 alpha + t for every (cq, iq) cell and the within-cq 5-1 spread."""
    piv = cell.pivot_table(index="month", columns=["cq", "iq"], values="VW")
    grid = {}
    for cq in range(1, N_Q + 1):
        row = {}
        ports = {}
        for iq in range(1, N_Q + 1):
            if (cq, iq) in piv.columns:
                r = piv[(cq, iq)].dropna().sort_index()
                ports[iq] = r
                a, t, n = ff3_alpha(r, ff, subtract_rf=True)
                row[iq] = {"alpha": a, "t": t, "n": n}
            else:
                row[iq] = {"alpha": np.nan, "t": np.nan, "n": 0}
        if 5 in ports and 1 in ports:
            common = ports[5].index.intersection(ports[1].index).sort_values()
            spread = ports[5].loc[common] - ports[1].loc[common]
            a, t, n = ff3_alpha(spread, ff, subtract_rf=False)
            row["5-1"] = {"alpha": a, "t": t, "n": n}
        else:
            row["5-1"] = {"alpha": np.nan, "t": np.nan, "n": 0}
        grid[cq] = row
    return grid


# ── formatting / comparison ─────────────────────────────────────────
def _f(x, nd=2):
    if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
        return "—"
    return f"{x:.{nd}f}"


def row_from_alphas(alphas: dict) -> list:
    """[Q1..Q5, 5-1] alpha point estimates from a port_alphas dict."""
    return [alphas[k]["alpha"] for k in (1, 2, 3, 4, 5, "5-1")]


def row_from_alphas_t(alphas: dict) -> list:
    return [alphas[k]["t"] for k in (1, 2, 3, 4, 5, "5-1")]


def build_control_row(df: pd.DataFrame, ff: pd.DataFrame, control: str,
                      label: str, paper: list) -> dict:
    cell = dependent_double_sort(df, control)
    ports = average_over_control(cell)
    alphas = port_alphas(ports, ff)
    ours = row_from_alphas(alphas)
    return {"label": label, "ours": ours, "t": row_from_alphas_t(alphas),
            "paper": paper, "alphas": alphas,
            "n_stocks_avg": _avg_stocks(df, control),
            "n_months": alphas["5-1"]["n"]}


def _avg_stocks(df: pd.DataFrame, control: str) -> float:
    sub = df[["month", "permno", "ivol", "me", "ret_next", control]].dropna()
    return sub.groupby("month")["permno"].count().mean()


def compare_block(title: str, rows: list) -> str:
    """Markdown: replication vs paper, with abs diff for each cell."""
    head = ("| Control | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |",
            "|---|---:|---:|---:|---:|---:|---:|")
    lines = [f"### {title}", "", head[0], head[1]]
    for r in rows:
        lines.append(f"| {r['label']} (rep) | " +
                     " | ".join(_f(v) for v in r["ours"]) + " |")
        lines.append(f"| {r['label']} (paper) | " +
                     " | ".join(_f(v) for v in r["paper"]) + " |")
    lines.append("")
    lines.append("**Absolute differences (rep − paper):**")
    lines.append("")
    lines.append(head[0].replace(" Q1", " ΔQ1").replace("| Control", "| Control"))
    lines.append(head[1])
    for r in rows:
        diffs = [a - b for a, b in zip(r["ours"], r["paper"])]
        lines.append(f"| {r['label']} | " +
                     " | ".join(_f(v) for v in diffs) + " |")
    return "\n".join(lines)


# ── main ────────────────────────────────────────────────────────────
def run() -> None:
    print("Loading panel…")
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = pd.to_datetime(panel["month"])
    print(f"  {len(panel):,} rows, {panel['month'].nunique()} months, "
          f"{panel['permno'].nunique():,} permnos")

    print("Loading monthly FF factors…")
    ff = load_ff_monthly()
    print(f"  {len(ff)} factor months, {ff.index.min():%Y-%m} .. "
          f"{ff.index.max():%Y-%m}; mean rf = {ff['rf'].mean()*100:.3f}%/mo")

    print("Attaching next-month returns (signal_t -> ret_{t+1})…")
    df = attach_next_month_return(panel)
    print("Computing momentum signals (past1, past6, past12)…")
    df = compute_momentum(df)

    # ── Table VII ──
    print("\n=== Table VII ===")
    controls_7 = [
        ("size",     "Controlling for Size",     PAPER_7["Controlling for Size"]),
        ("bm",       "Controlling for B/M",      PAPER_7["Controlling for B/M"]),
        ("leverage", "Controlling for Leverage", PAPER_7["Controlling for Leverage"]),
        ("volume",   "Controlling for Volume",   PAPER_7["Controlling for Volume"]),
        ("turnover", "Controlling for Turnover", PAPER_7["Controlling for Turnover"]),
        ("coskew",   "Controlling for Coskew",   PAPER_7["Controlling for Coskew"]),
    ]
    rows_7 = []
    # NYSE-only single sort
    nyse = df[df["hexcd"] == 1]
    nyse_ports = single_sort_vw(nyse)
    nyse_alphas = port_alphas(nyse_ports, ff)
    nyse_row = {"label": "NYSE Stocks Only",
                "ours": row_from_alphas(nyse_alphas),
                "t": row_from_alphas_t(nyse_alphas),
                "paper": PAPER_7["NYSE Stocks Only"], "alphas": nyse_alphas,
                "n_stocks_avg": _avg_stocks_nyse(nyse),
                "n_months": nyse_alphas["5-1"]["n"]}
    rows_7.append(nyse_row)
    _print_row(nyse_row)

    for col, label, paper in controls_7:
        r = build_control_row(df, ff, col, label, paper)
        rows_7.append(r)
        _print_row(r)

    # Size detail 5x5
    print("\n  Size detail (5x5):")
    size_cell = dependent_double_sort(df, "size")
    size_grid = cell_alphas(size_cell, ff)
    for cq in range(1, N_Q + 1):
        vals = [size_grid[cq][k]["alpha"] for k in (1, 2, 3, 4, 5, "5-1")]
        print(f"    size Q{cq}: " + " ".join(_f(v) for v in vals))

    # ── Table VIII ──
    print("\n=== Table VIII Panel A (momentum controls) ===")
    controls_8 = [
        ("past1",  "Past 1 month",   PAPER_8A["Past 1 month"]),
        ("past6",  "Past 6 months",  PAPER_8A["Past 6 months"]),
        ("past12", "Past 12 months", PAPER_8A["Past 12 months"]),
    ]
    rows_8a = []
    for col, label, paper in controls_8:
        r = build_control_row(df, ff, col, label, paper)
        rows_8a.append(r)
        _print_row(r)

    print("\n  Panel B: past-12-month x IVOL detail (5x5):")
    p12_cell = dependent_double_sort(df, "past12")
    p12_grid = cell_alphas(p12_cell, ff)
    for cq in range(1, N_Q + 1):
        vals = [p12_grid[cq][k]["alpha"] for k in (1, 2, 3, 4, 5, "5-1")]
        print(f"    past12 Q{cq}: " + " ".join(_f(v) for v in vals))

    # ── write outputs ──
    write_table_7(rows_7, size_grid, ff)
    write_table_8(rows_8a, p12_grid, ff)
    print("\nDone.")


def _avg_stocks_nyse(df_nyse: pd.DataFrame) -> float:
    sub = df_nyse[["month", "permno", "ivol", "me", "ret_next"]].dropna()
    return sub.groupby("month")["permno"].count().mean()


def _print_row(r: dict) -> None:
    print(f"  {r['label']:26s} | rep: " +
          " ".join(f"{v:6.2f}" for v in r["ours"]) +
          f"  | n_stk={r['n_stocks_avg']:.0f} n_mo={r['n_months']}")
    print(f"  {'':26s} | pap: " +
          " ".join(f"{v:6.2f}" for v in r["paper"]))


# ── markdown writers ────────────────────────────────────────────────
_SIZE_LABELS = {1: "Small 1", 2: "2", 3: "3", 4: "4", 5: "Large 5"}
_P12_LABELS = {1: "Losers 1", 2: "2", 3: "3", 4: "4", 5: "Winners 5"}


def _grid_md(grid: dict, labels: dict, paper: dict) -> str:
    head = ("| Quintile | IVOL 1 | 2 | 3 | 4 | 5 | 5-1 |",
            "|---|---:|---:|---:|---:|---:|---:|")
    lines = [head[0], head[1]]
    for cq in range(1, N_Q + 1):
        vals = [grid[cq][k]["alpha"] for k in (1, 2, 3, 4, 5, "5-1")]
        lines.append(f"| {labels[cq]} (rep) | " +
                     " | ".join(_f(v) for v in vals) + " |")
        lines.append(f"| {labels[cq]} (paper) | " +
                     " | ".join(_f(v) for v in paper[labels[cq]]) + " |")
    return "\n".join(lines)


def write_table_7(rows_7: list, size_grid: dict, ff: pd.DataFrame) -> None:
    comp = compare_block("Dependent double sorts (FF-3 alphas, %/month)", rows_7)
    # t-stats table
    tlines = ["### Newey–West(4) t-statistics (replication)", "",
              "| Control | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for r in rows_7:
        tlines.append(f"| {r['label']} | " +
                      " | ".join(f"({_f(v)})" for v in r["t"]) + " |")
    size_md = _grid_md(size_grid, _SIZE_LABELS, PAPER_7_SIZE)
    n_stk = ", ".join(f"{r['label']}={r['n_stocks_avg']:.0f}" for r in rows_7)
    md = f"""# Table VII — Alphas of IVOL Portfolios Controlling for Cross-Sectional Effects
## Ang, Hodrick, Xing, Zhang (2006), "The Cross-Section of Volatility and Expected Returns"

Dependent double sorts. Each formation month, stocks are first sorted into
quintiles on the control characteristic, then within each control quintile
into quintiles on IVOL (relative to FF-3); cell returns are value-weighted by
month-t market equity and earned in month t+1. The five IVOL portfolios are
then averaged (equal-weighted) across the five control quintiles. Reported:
FF-3 alphas in percent per month; Newey–West(4) t-statistics in parentheses.
"NYSE Stocks Only" restricts the universe to hexcd == 1 (single IVOL sort).
Breakpoints use all stocks (20/40/60/80 pctiles). Holding months 1963-07 to
2000-12. FF factors from ff.four_factor_monthly (decimal).

{comp}

{chr(10).join(tlines)}

### Size Quintiles detail (5×5: size × IVOL, FF-3 alphas, %/month)

Within each size quintile, stocks are sorted into IVOL quintiles; the cell
FF-3 alphas are reported (NOT averaged across size quintiles).

{size_md}

## Notes
- Average stocks/month per control sort: {n_stk}.
- Stocks missing a given control are dropped from that control's sort only.
- Book-to-market and leverage use Compustat-matched firms (financial firms
  with only FS-format records have missing bm/leverage → fewer stocks).
- Coskewness computed following Harvey & Siddique (2000) in the data pipeline.
"""
    path = LAYOUT.result_path("table_7.md")
    path.write_text(md)
    print(f"Wrote {path}")


def write_table_8(rows_8a: list, p12_grid: dict, ff: pd.DataFrame) -> None:
    comp = compare_block("Panel A: Controlling for Momentum (FF-3 alphas, %/month)",
                         rows_8a)
    tlines = ["### Newey–West(4) t-statistics (replication, Panel A)", "",
              "| Control | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for r in rows_8a:
        tlines.append(f"| {r['label']} | " +
                      " | ".join(f"({_f(v)})" for v in r["t"]) + " |")
    grid_md = _grid_md(p12_grid, _P12_LABELS, PAPER_8B)
    n_stk = ", ".join(f"{r['label']}={r['n_stocks_avg']:.0f} (n_mo={r['n_months']})"
                      for r in rows_8a)
    md = f"""# Table VIII — Alphas of IVOL Portfolios Controlling for Past Returns
## Ang, Hodrick, Xing, Zhang (2006), "The Cross-Section of Volatility and Expected Returns"

Dependent double sorts controlling for past returns (momentum). Each formation
month, stocks are first sorted into quintiles on a past-return signal, then
within each momentum quintile into quintiles on IVOL; cell returns are
value-weighted and earned in month t+1. The five IVOL portfolios are averaged
(equal-weighted) across the five momentum quintiles (Panel A). Panel B reports
the full 5×5 past-12-month × IVOL grid of FF-3 alphas. Alphas in percent per
month; Newey–West(4) t-statistics in parentheses.

Past-return signals (relative to signal row t): past 1 month = ret_{{t}} (the
FORMATION-month return — portfolios are formed at the end of month t, so
"past 1-month return" includes month t; issue M3 convention); past 6 months =
cumret(t-6..t-1); past 12 months = cumret(t-12..t-1). The 6/12-month windows
include the most recent completed month (t-1), unlike the panel's `mom`
(= cumret(t-12..t-2), which skips t-1).

{comp}

{chr(10).join(tlines)}

### Panel B: Past 12-Month Return × IVOL detail (5×5, FF-3 alphas, %/month)

{grid_md}

## Notes
- Average stocks/month (and # holding months) per momentum sort: {n_stk}.
- Momentum windows need lookback before the panel's 1963-06 start, so the
  effective sample is shorter than July-1963: past-1 starts ~1963-08,
  past-6 ~1964-01, past-12 ~1964-07 (holding months). This is a data
  limitation (the panel starts at the first IVOL formation month).
"""
    path = LAYOUT.result_path("table_8.md")
    path.write_text(md)
    print(f"Wrote {path}")


if __name__ == "__main__":
    run()
