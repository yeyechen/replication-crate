"""
Replication of Frazzini & Pedersen (2014) "Betting Against Beta" — Table 3 (v2).
=================================================================================
US-equity beta-sorted decile portfolios + the BAB factor.

This is the REVISED Table 3 implementation. Relative to ``table_3.py`` (v1) it
fixes the two known causes of the decile-alpha gap:

  Fix 1 — NYSE breakpoints.
    v1 sorted deciles on ALL-stock beta breakpoints (the panel carried no
    exchange code). The paper: "The ranked stocks are assigned to one of ten
    deciles portfolios based on NYSE breakpoints." (Table 3 description.)
    Here we merge a point-in-time exchange code (crsp_202601.dsenames, exchcd)
    onto the panel and set the decile breakpoints from NYSE stocks only
    (exchcd == 1), then assign ALL stocks to deciles on those breakpoints.

  Fix 2 — delisting returns.
    v1 used raw CRSP msf.ret, which omits the delisting return and biases
    high-beta returns upward (high-beta names delist for performance reasons
    more often). Here we merge crsp_202601.dsedelist and, for each stock's LAST
    month in the panel, combine the delisting return with that month's return:
        adjusted_ret = (1 + ret) * (1 + dlret_eff) - 1
    where dlret_eff is the reported dlret when valid (dlret > -1.0 and not
    NULL), and otherwise the Shumway (1997) / BMP (2007) imputation when the
    delisting is performance-related (dlstcd 500-599): -0.30 for NYSE/AMEX
    (exchcd 1,2), -0.55 for NASDAQ (exchcd 3).

    Two match cases are handled (see FLAG in the report):
      Case A — the delisting month EQUALS the stock's last panel month (the
               stock has a valid CRSP return in the delisting month).
      Case B — the delisting month is the month AFTER the last panel month
               (CRSP stored the delisting-month return as a missing sentinel,
               so the delisting return only lives in dsedelist). The terminal
               return is then attributed to the last holding month. This case
               dominates (17,012 vs 2,392) and is REQUIRED to capture most of
               the delisting bias.

Everything else is unchanged from v1: the BAB factor (median split + rank
weights, rescaled to unit beta — it does NOT use decile breakpoints), the
factor regressions (CAPM / FF3 / Carhart-4, standard iid t-stats with a
Newey-West supplement), and the reporting format. The BAB factor IS affected
by Fix 2 (its leg returns use the delisting-adjusted returns), which is
methodologically correct — the paper computes all returns with delistings.

Outputs (overwrite the v1 files):
  results/table_3.md
  results/decile_returns.png
  results/bab_cumulative.png

Usage:
    uv run python src/table_3_v2.py
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Pin repo root on sys.path so `import utils` resolves, and pin
# REPLICATIONS_PATH so paper_layout() finds this replication deterministically.
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
os.environ.setdefault("REPLICATIONS_PATH", str(_REPO_ROOT / "replications"))

import matplotlib
matplotlib.use("Agg")                       # headless — must be first mpl import
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from clickhouse_driver import Client

from utils.env import get_clickhouse_config
from utils.paths import paper_layout
from utils.portfolio import bin_returns
from utils.regressions import factor_alpha
from utils.metrics import performance_metrics
from utils.plot import plot_cumulative_returns

# ────────────────────────────────────────────────────────────────────────────
# Layout & configuration
# ────────────────────────────────────────────────────────────────────────────
SLUG = "betting_against_beta"
LAYOUT = paper_layout(SLUG)
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")
_CFG = get_clickhouse_config()

N_DECILES = 10           # [sort_decile_nyse_ew] ten decile portfolios
NYSE_MIN = 20            # min NYSE names/month to use NYSE breakpoints (else all-stock)
NW_LAGS = 6             # Newey-West lags for the supplementary HAC alpha t-stat
SHUMWAY_NYSE_AMX = -0.30  # Shumway (1997) imputation, NYSE/AMEX (exchcd 1,2)
SHUMWAY_NASDAQ = -0.55    # Shumway (1997) imputation, NASDAQ (exchcd 3)

# Paper validation values (Table 3, US equities). Returns/alphas in monthly %,
# volatility annualized %, Sharpe annualized, betas dimensionless.
PAPER = {
    "P1":  dict(excess_ret=0.91, capm_alpha=0.52, ff3_alpha=0.40, ff4_alpha=0.40,
                beta_exante=0.64, beta_realized=0.67, vol=15.70, sharpe=0.70),
    "P5":  dict(excess_ret=1.05, capm_alpha=0.34, ff3_alpha=0.13, ff4_alpha=0.18,
                beta_exante=1.05, beta_realized=1.22, vol=25.56, sharpe=0.49),
    "P10": dict(excess_ret=0.97, capm_alpha=-0.10, ff3_alpha=-0.49, ff4_alpha=-0.13,
                beta_exante=1.70, beta_realized=1.85, vol=41.68, sharpe=0.28),
    "BAB": dict(excess_ret=0.70, capm_alpha=0.73, ff3_alpha=0.73, ff4_alpha=0.55,
                beta_exante=0.00, beta_realized=-0.06, vol=10.75, sharpe=0.78),
}
# Per-metric tolerance (%) for pass/fail (from preparations/tables_to_replicate.json).
TOL = {
    "excess_ret": 15.0, "capm_alpha": 20.0, "ff3_alpha": 20.0, "ff4_alpha": 20.0,
    "beta_exante": 10.0, "beta_realized": 10.0, "vol": 10.0, "sharpe": 15.0,
}
# v1 (table_3.py) results for the headline cells — for the improvement report.
V1 = {
    "P1":  dict(excess_ret=0.95, capm_alpha=0.58, ff3_alpha=0.51, ff4_alpha=0.51,
                beta_exante=0.57, beta_realized=0.61, vol=15.13, sharpe=0.75),
    "P5":  dict(excess_ret=1.14, capm_alpha=0.42, ff3_alpha=0.27, ff4_alpha=0.34,
                beta_exante=1.00, beta_realized=1.19, vol=25.09, sharpe=0.55),
    "P10": dict(excess_ret=1.09, capm_alpha=-0.05, ff3_alpha=-0.31, ff4_alpha=0.08,
                beta_exante=1.78, beta_realized=1.88, vol=43.24, sharpe=0.30),
    "BAB": dict(excess_ret=0.73, capm_alpha=0.77, ff3_alpha=0.77, ff4_alpha=0.59,
                beta_exante=0.00, beta_realized=-0.06, vol=11.45, sharpe=0.77),
}
V1_PASS = 23  # v1 cells passing out of 32


# ────────────────────────────────────────────────────────────────────────────
# ClickHouse connection
# ────────────────────────────────────────────────────────────────────────────
def _client() -> Client:
    return Client(
        host=_CFG["host"], port=int(_CFG["port"]),
        user=_CFG["user"], password=_CFG["password"],
        database=_CFG.get("database", "default"),
        settings={"max_execution_time": 300},
    )


def q_file(name: str) -> pd.DataFrame:
    sql = (SQL_DIR / name).read_text().strip().rstrip(";")
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


# ────────────────────────────────────────────────────────────────────────────
# Fix 1: point-in-time exchange codes (NYSE breakpoints)
# ────────────────────────────────────────────────────────────────────────────
def merge_exchcd(panel: pd.DataFrame) -> pd.DataFrame:
    """Merge a PIT exchange code onto the panel via dsenames.

    For each (permno, month) we take the dsenames record whose validity window
    [namedt, nameendt] covers the month (the record with the latest
    namedt <= month, kept only if nameendt >= month). Adds column `exchcd`
    (1=NYSE, 2=AMEX, 3=NASDAQ, ...). Coverage is ~100% of panel rows.
    """
    names = q_file("exchcd.sql")
    names["permno"] = names["permno"].astype("int64")
    names["namedt"] = pd.to_datetime(names["namedt"], errors="coerce").astype("datetime64[ns]")
    names["nameendt"] = pd.to_datetime(names["nameendt"], errors="coerce").astype("datetime64[ns]")
    names = names.dropna(subset=["permno", "namedt", "exchcd"])
    names["nameendt"] = names["nameendt"].fillna(pd.Timestamp("2100-01-01"))  # NULL = still active
    names["exchcd"] = names["exchcd"].astype("int64")
    names = names.sort_values("namedt").reset_index(drop=True)

    p = panel.copy()
    p["month"] = p["month"].astype("datetime64[ns]")
    p["permno"] = p["permno"].astype("int64")
    p = p.sort_values("month").reset_index(drop=True)
    m = pd.merge_asof(p, names, left_on="month", right_on="namedt",
                      by="permno", direction="backward")
    m.loc[m["nameendt"] < m["month"], "exchcd"] = np.nan
    cov = m["exchcd"].notna().mean()
    nyse_pm = m[m["exchcd"] == 1].groupby("month")["permno"].nunique()
    print(f"      exchcd coverage: {cov:.4f}; NYSE stocks/month "
          f"min={nyse_pm.min()} median={int(nyse_pm.median())} max={nyse_pm.max()}")
    return m


# ────────────────────────────────────────────────────────────────────────────
# Fix 2: delisting-return adjustment
# ────────────────────────────────────────────────────────────────────────────
def build_delist_adjustment(panel: pd.DataFrame) -> pd.DataFrame:
    """Compute the per-stock delisting-return adjustment for the last panel month.

    Returns a DataFrame keyed (permno, month=last_month) with:
      dlret_eff : effective delisting return (reported or Shumway-imputed)
      matchA    : delisting month == last panel month
      matchB    : delisting month == last panel month + 1
    Rows with no usable dlret_eff are dropped. The caller decides which cases
    (A, B, or both) to apply.
    """
    dl = q_file("delisting.sql")
    dl["permno"] = dl["permno"].astype("int64")
    dl["dlstdt"] = pd.to_datetime(dl["dlstdt"], errors="coerce")
    dl = dl.dropna(subset=["permno", "dlstdt"])
    dl["dl_month"] = dl["dlstdt"].dt.to_period("M").dt.to_timestamp().astype("datetime64[ns]")
    # valid dlret: not NULL and > -1.0 (this vintage stores the -44/-55/... error
    # codes as NULL; -1.0 is CRSP's "worthless" flag, treated as missing per spec).
    dl["dlret_valid"] = dl["dlret"].notna() & (dl["dlret"] > -1.0)
    # one delisting record per permno, preferring a valid dlret, then latest date
    dl = dl.sort_values(["permno", "dlret_valid", "dlstdt"],
                        ascending=[True, False, False]).drop_duplicates("permno", keep="first")

    # last panel month per stock
    last = panel.groupby("permno")["month"].max().rename("last_month").reset_index()
    lm = last.merge(dl[["permno", "dl_month", "dlret", "dlret_valid", "dlstcd", "hexcd"]],
                    on="permno", how="inner")
    lm["lm_plus1"] = (lm["last_month"].dt.to_period("M") + 1).dt.to_timestamp()
    lm["matchA"] = lm["dl_month"] == lm["last_month"]
    lm["matchB"] = lm["dl_month"] == lm["lm_plus1"]
    lm = lm[lm["matchA"] | lm["matchB"]].copy()

    def _eff(r):
        if r["dlret_valid"]:
            return float(r["dlret"])
        if r["dlstcd"] is not None and 500 <= int(r["dlstcd"]) <= 599:
            ex = r["hexcd"]
            if ex in (1, 2):
                return SHUMWAY_NYSE_AMX
            if ex == 3:
                return SHUMWAY_NASDAQ
        return np.nan  # missing dlret, not performance-related -> no adjustment

    lm["dlret_eff"] = lm.apply(_eff, axis=1)
    lm = lm.dropna(subset=["dlret_eff"])
    n_a = int(lm["matchA"].sum())
    n_b = int((lm["matchB"] & ~lm["matchA"]).sum())
    n_shum = int((~lm["dlret_valid"]).sum())
    print(f"      delisting adjustments: {len(lm)} stock-months "
          f"(Case A={n_a}, Case B={n_b}; Shumway-imputed={n_shum}, "
          f"mean dlret_eff={lm['dlret_eff'].mean():.4f})")
    return lm.rename(columns={"last_month": "month"})[
        ["permno", "month", "dlret_eff", "matchA", "matchB"]
    ]


def apply_delist(panel: pd.DataFrame, adj: pd.DataFrame, mode: str) -> pd.DataFrame:
    """Return a copy of panel with delisting-adjusted returns.

    mode: 'none' -> no adjustment; 'A' -> Case A only; 'AB' -> Cases A and B.
    adjusted_ret = (1 + ret) * (1 + dlret_eff) - 1 on the stock's last month.
    """
    p = panel.copy()
    if mode == "none" or adj is None or len(adj) == 0:
        return p
    a = adj.copy()
    if mode == "A":
        a = a[a["matchA"]]
    elif mode == "AB":
        a = a[a["matchA"] | a["matchB"]]
    else:
        raise ValueError(f"unknown delist mode {mode!r}")
    a = a[["permno", "month", "dlret_eff"]]
    p = p.merge(a, on=["permno", "month"], how="left")
    mask = p["dlret_eff"].notna()
    p.loc[mask, "ret"] = (1.0 + p.loc[mask, "ret"]) * (1.0 + p.loc[mask, "dlret_eff"]) - 1.0
    n_adj = int(mask.sum())
    p = p.drop(columns=["dlret_eff"])
    print(f"      delist mode={mode}: adjusted {n_adj} rows")
    return p


# ────────────────────────────────────────────────────────────────────────────
# FF factors + excess returns (unchanged logic from v1)
# ────────────────────────────────────────────────────────────────────────────
def load_ff() -> tuple[pd.DataFrame, str]:
    """Load FF 4-factor monthly; return (df indexed by month Period[M], units note)."""
    raw = q_file("ff_factors.sql")
    raw["dt"] = pd.to_datetime(raw["dt"])
    raw["month"] = raw["dt"].dt.to_period("M").dt.to_timestamp()
    fac_cols = ["mkt_rf", "smb", "hml", "mom", "rf"]
    for c in fac_cols:
        raw[c] = pd.to_numeric(raw[c], errors="coerce")
    med = raw["mkt_rf"].abs().median()
    if med > 0.2:
        raw[fac_cols] = raw[fac_cols] / 100.0
        units = f"PERCENT in source (median |mkt_rf|={med:.3f}) -> divided by 100"
    else:
        units = f"DECIMAL in source (median |mkt_rf|={med:.4f}) -> used as-is"
    ff = raw.set_index(raw["month"].dt.to_period("M"))[fac_cols].sort_index()
    return ff, units


def build_excess(panel: pd.DataFrame, ff: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """Attach rf by month, compute excess_ret = ret - rf, drop null beta/ret."""
    rf_by_month = ff["rf"]
    mkey = panel["month"].dt.to_period("M")
    panel = panel.copy()
    panel["rf"] = mkey.map(rf_by_month).to_numpy()
    panel["excess_ret"] = panel["ret"] - panel["rf"]
    before = len(panel)
    df = panel.dropna(subset=["beta", "excess_ret", "ret"]).reset_index(drop=True)
    if verbose:
        print(f"      rows: {before:,} -> {len(df):,} after dropping null "
              f"beta/excess_ret/ret ({before - len(df):,} dropped)")
    return df


# ────────────────────────────────────────────────────────────────────────────
# Decile sorts with NYSE breakpoints (Fix 1)
# ────────────────────────────────────────────────────────────────────────────
def assign_deciles(df: pd.DataFrame, nyse: bool = True) -> tuple[pd.DataFrame, pd.Series]:
    """Assign beta deciles within each month using NYSE (exchcd==1) breakpoints.

    Breakpoints = 10th..90th percentiles of beta among NYSE stocks that month;
    ALL stocks are then assigned to deciles on those breakpoints. Falls back to
    all-stock breakpoints in any month with < NYSE_MIN NYSE names. With
    nyse=False, uses all-stock breakpoints throughout (the v1 behaviour).
    Returns (df with `decile`, ex-ante beta per decile).
    """
    df = df.copy()
    probs = list(np.linspace(0.0, 1.0, N_DECILES + 1)[1:-1])   # 0.1 .. 0.9
    bp_all = df.groupby("month")["beta"].quantile(probs).unstack()
    if nyse and "exchcd" in df.columns:
        ny = df[df["exchcd"] == 1]
        bp_nyse = ny.groupby("month")["beta"].quantile(probs).unstack()
        ny_n = ny.groupby("month")["beta"].size()
        use = (ny_n.reindex(bp_all.index) >= NYSE_MIN)
        bp = bp_all.copy()
        idx = use[use].index
        bp.loc[idx] = bp_nyse.reindex(idx)
        bp = bp.fillna(bp_all)
    else:
        bp = bp_all
    bp.columns = [f"bp{i}" for i in range(N_DECILES - 1)]

    df = df.merge(bp, left_on="month", right_index=True, how="left")
    cols = list(bp.columns)
    M = df[cols].to_numpy()
    b = df["beta"].to_numpy()[:, None]
    dec = (b > M).sum(axis=1) + 1                       # decile 1..10
    nan = np.isnan(M).any(axis=1) | np.isnan(df["beta"].to_numpy())
    dec = dec.astype(float)
    dec[nan] = np.nan
    df["decile"] = dec
    df = df.dropna(subset=["decile"]).reset_index(drop=True)
    df["decile"] = df["decile"].astype(int)

    monthly_beta = df.groupby(["month", "decile"])["beta"].mean()
    beta_exante = monthly_beta.groupby("decile").mean()
    return df, beta_exante


def decile_ew_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly EW excess returns per decile -> DataFrame (month Period[M] x decile)."""
    br = bin_returns(df, date_col="month", bin_col="decile",
                     ret_col="excess_ret", mcap_col="me")
    piv = br.pivot(index="month", columns="decile", values="EW").sort_index()
    piv.index = piv.index.to_period("M")
    return piv


# ────────────────────────────────────────────────────────────────────────────
# BAB factor (unchanged from v1; uses delisting-adjusted excess returns)
# ────────────────────────────────────────────────────────────────────────────
def bab_factor(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly BAB factor (excess, self-financing, zero-beta) — rank-weighted,
    rescaled to unit beta. Median split; does NOT use decile breakpoints."""
    d = df[["month", "beta", "excess_ret"]].copy()
    d["z"] = d.groupby("month")["beta"].rank(method="average")
    d["zbar"] = d.groupby("month")["z"].transform("mean")
    d["med"] = d.groupby("month")["beta"].transform("median")
    d["dev"] = d["z"] - d["zbar"]
    d["k"] = 2.0 / d.groupby("month")["dev"].transform(lambda s: s.abs().sum())
    low = d["beta"] < d["med"]
    high = d["beta"] > d["med"]
    d["wL"] = np.where(low, d["k"] * (d["zbar"] - d["z"]), 0.0)
    d["wH"] = np.where(high, d["k"] * (d["z"] - d["zbar"]), 0.0)
    d["wL_r"] = d["wL"] * d["excess_ret"]
    d["wH_r"] = d["wH"] * d["excess_ret"]
    d["wL_b"] = d["wL"] * d["beta"]
    d["wH_b"] = d["wH"] * d["beta"]
    agg = d.groupby("month").agg(
        rL=("wL_r", "sum"), rH=("wH_r", "sum"),
        bL=("wL_b", "sum"), bH=("wH_b", "sum"),
        wL_sum=("wL", "sum"), wH_sum=("wH", "sum"),
        n=("beta", "size"),
    )
    agg["bab"] = agg["rL"] / agg["bL"] - agg["rH"] / agg["bH"]
    agg.index = agg.index.to_period("M")
    return agg.sort_index()


# ────────────────────────────────────────────────────────────────────────────
# Metrics + factor regressions (unchanged from v1)
# ────────────────────────────────────────────────────────────────────────────
def _alpha(gross: pd.Series, ff: pd.DataFrame, factors: list[str], n_lags: int) -> dict:
    return factor_alpha(
        portfolio_returns=gross, factor_returns=ff, factors=factors,
        rf_col="rf", n_lags=n_lags, freq="M",
    )


def portfolio_row(label: str, excess: pd.Series, ff: pd.DataFrame,
                  beta_exante: float) -> dict:
    excess = excess.dropna().sort_index()
    rf = ff["rf"].reindex(excess.index)
    gross = (excess + rf).dropna()
    excess = excess.reindex(gross.index)
    n = len(excess)
    mean_ex = float(excess.mean())
    std_ex = float(excess.std(ddof=1))
    pm = performance_metrics(excess, freq="M")
    capm0 = _alpha(gross, ff, ["mkt_rf"], 0)
    capmN = _alpha(gross, ff, ["mkt_rf"], NW_LAGS)
    ff3_0 = _alpha(gross, ff, ["mkt_rf", "smb", "hml"], 0)
    ff3_N = _alpha(gross, ff, ["mkt_rf", "smb", "hml"], NW_LAGS)
    ff4_0 = _alpha(gross, ff, ["mkt_rf", "smb", "hml", "mom"], 0)
    ff4_N = _alpha(gross, ff, ["mkt_rf", "smb", "hml", "mom"], NW_LAGS)
    return {
        "label": label, "n": n,
        "excess_ret": mean_ex * 100.0,
        "t_excess": mean_ex / (std_ex / np.sqrt(n)),
        "capm_alpha": capm0["alpha_monthly"] * 100.0,
        "capm_t": capm0["t_alpha_newey_west"],
        "capm_t_nw": capmN["t_alpha_newey_west"],
        "ff3_alpha": ff3_0["alpha_monthly"] * 100.0,
        "ff3_t": ff3_0["t_alpha_newey_west"],
        "ff3_t_nw": ff3_N["t_alpha_newey_west"],
        "ff4_alpha": ff4_0["alpha_monthly"] * 100.0,
        "ff4_t": ff4_0["t_alpha_newey_west"],
        "ff4_t_nw": ff4_N["t_alpha_newey_west"],
        "beta_exante": beta_exante,
        "beta_realized": float(capm0["betas"]["mkt_rf"]),
        "vol": pm["annualized_vol"] * 100.0,
        "sharpe": pm["sharpe_ratio"],
    }


# ────────────────────────────────────────────────────────────────────────────
# One full analysis pass (used for the main run + ablations)
# ────────────────────────────────────────────────────────────────────────────
def run_analysis(panel_ex: pd.DataFrame, adj: pd.DataFrame, ff: pd.DataFrame,
                 nyse: bool, delist_mode: str, verbose: bool = True) -> dict:
    """Run decile sorts + BAB + regressions for one configuration.

    Returns dict with keys: rows, beta_exante, bab, df (sorted panel),
    dec_excess, n_pass, cells.
    """
    p = apply_delist(panel_ex, adj, delist_mode) if delist_mode != "none" else panel_ex
    df = build_excess(p, ff, verbose=verbose)
    df, beta_exante = assign_deciles(df, nyse=nyse)
    dec_excess = decile_ew_returns(df)
    bab = bab_factor(df)
    rows = []
    for d in range(1, N_DECILES + 1):
        rows.append(portfolio_row(f"P{d}", dec_excess[d], ff, float(beta_exante.loc[d])))
    rows.append(portfolio_row("BAB", bab["bab"], ff, beta_exante=0.0))
    _, val = validation_block(rows)
    return dict(rows=rows, beta_exante=beta_exante, bab=bab, df=df,
                dec_excess=dec_excess, n_pass=val["n_pass"], cells=val["cells"])


# ────────────────────────────────────────────────────────────────────────────
# Table output + validation + plots
# ────────────────────────────────────────────────────────────────────────────
def build_table(rows: list[dict]) -> str:
    labels = [r["label"] for r in rows]
    by = {r["label"]: r for r in rows}

    def fmt(label_key, r, dec=2):
        return f"{r[label_key]:.{dec}f}"

    def trow(t_key, r):
        return f"({r[t_key]:.2f})"

    header = "| Metric | " + " | ".join(labels) + " |"
    sep = "|" + "---|" * (len(labels) + 1)
    lines = [header, sep]
    specs = [
        ("Excess return",      "excess_ret",    "t_excess", 2),
        ("CAPM alpha",         "capm_alpha",    "capm_t",   2),
        ("3-factor alpha",     "ff3_alpha",     "ff3_t",    2),
        ("4-factor alpha",     "ff4_alpha",     "ff4_t",    2),
        ("Beta (ex ante)",     "beta_exante",   None,       2),
        ("Beta (realized)",    "beta_realized", None,       2),
        ("Volatility",         "vol",           None,       2),
        ("Sharpe ratio",       "sharpe",        None,       2),
    ]
    for disp, key, tkey, dec in specs:
        cells = [fmt(key, by[l], dec) for l in labels]
        lines.append(f"| {disp} | " + " | ".join(cells) + " |")
        if tkey:
            tcells = [trow(tkey, by[l]) for l in labels]
            lines.append(f"| _t-stat_ | " + " | ".join(tcells) + " |")
    return "\n".join(lines)


def validation_block(rows: list[dict]) -> tuple[str, dict]:
    by = {r["label"]: r for r in rows}
    out = ["| Portfolio | Metric | Ours | Paper | Tol % | Diff % | Pass |",
           "|---|---|---:|---:|---:|---:|:--:|"]
    results = {}
    for label, paper in PAPER.items():
        if label not in by:
            continue
        ours = by[label]
        for metric, pval in paper.items():
            oval = ours[metric]
            tol = TOL.get(metric, 15.0)
            if abs(pval) < 1e-9:
                diff_pct = abs(oval - pval)
                passed = abs(oval - pval) <= 0.05
                dp = f"{diff_pct:.3f} (abs)"
            else:
                diff_pct = 100.0 * abs(oval - pval) / abs(pval)
                passed = diff_pct <= tol
                dp = f"{diff_pct:.1f}"
            results[(label, metric)] = passed
            out.append(
                f"| {label} | {metric} | {oval:.3f} | {pval:.3f} | "
                f"{tol:.0f} | {dp} | {'PASS' if passed else 'FAIL'} |"
            )
    npass = sum(1 for v in results.values() if v)
    return "\n".join(out), {"n_pass": npass, "n_total": len(results), "cells": results}


def ablation_block(ablations: list[dict]) -> str:
    """Compact table: pass counts + headline cells across configurations."""
    metrics = ["ff3_alpha", "ff4_alpha", "capm_alpha", "beta_exante", "excess_ret"]
    labels = ["P1", "P5", "P10", "BAB"]
    head = "| Config | Pass/32 |"
    for lab in labels:
        for m in metrics:
            head += f" {lab}:{m} |"
    sep = "|---|---:|" + "---:|" * (len(labels) * len(metrics))
    lines = [head, sep]
    for a in ablations:
        by = {r["label"]: r for r in a["rows"]}
        row = f"| {a['name']} | {a['n_pass']}/32 |"
        for lab in labels:
            for m in metrics:
                row += f" {by[lab][m]:.2f} |"
        lines.append(row)
    return "\n".join(lines)


def plot_decile_returns(rows: list[dict], save_to: Path) -> None:
    dec_rows = sorted([r for r in rows if r["label"].startswith("P")],
                      key=lambda r: int(r["label"][1:]))
    labels = [r["label"] for r in dec_rows]
    ann_excess = [r["excess_ret"] * 12.0 for r in dec_rows]
    sharpe = [r["sharpe"] for r in dec_rows]
    x = np.arange(len(labels))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.bar(x, ann_excess, color="#4C72B0", alpha=0.85)
    ax1.axhline(0, color="k", lw=0.6)
    ax1.set_xticks(x); ax1.set_xticklabels(labels)
    ax1.set_xlabel("Beta decile (P1=low .. P10=high)")
    ax1.set_ylabel("Annualized excess return (%)")
    ax1.set_title("Excess return by beta decile (EW)")
    ax1.grid(True, alpha=0.3)
    ax2.bar(x, sharpe, color="#C44E52", alpha=0.85)
    ax2.axhline(0, color="k", lw=0.6)
    ax2.set_xticks(x); ax2.set_xticklabels(labels)
    ax2.set_xlabel("Beta decile (P1=low .. P10=high)")
    ax2.set_ylabel("Annualized Sharpe ratio")
    ax2.set_title("Sharpe ratio by beta decile (EW)")
    ax2.grid(True, alpha=0.3)
    fig.suptitle("Frazzini-Pedersen (2014) Table 3 — beta-sorted deciles, US equities "
                 "(v2: NYSE breakpoints + delisting returns)")
    fig.tight_layout()
    fig.savefig(save_to, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_bab_cumulative(bab: pd.DataFrame, save_to: Path) -> None:
    df = bab[["bab"]].copy()
    df["month"] = df.index.to_timestamp()
    df = df.reset_index(drop=True)
    plot_cumulative_returns(
        df[["month", "bab"]], index_col_name="month", ret_col_lst=["bab"],
        title="BAB factor — cumulative return (US equities, v2)", save_to=save_to,
    )


# ────────────────────────────────────────────────────────────────────────────
# main
# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    t0 = time.time()
    print("=" * 72)
    print("Frazzini-Pedersen (2014) 'Betting Against Beta' — Table 3 (US) v2")
    print("=" * 72)

    print("[1/7] load panel ...")
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = pd.to_datetime(panel["month"])
    print(f"      panel: {panel.shape[0]:,} rows x {panel.shape[1]} cols, "
          f"{panel['month'].nunique()} months, {panel['permno'].nunique()} permnos")

    print("[2/7] load FF factors ...")
    ff, ff_units = load_ff()
    print(f"      FF: {len(ff)} months, {ff.index.min()} .. {ff.index.max()}; {ff_units}")

    print("[3/7] merge PIT exchange codes (Fix 1) ...")
    panel_ex = merge_exchcd(panel)

    print("[4/7] build delisting-return adjustment (Fix 2) ...")
    adj = build_delist_adjustment(panel_ex)

    # ── Main v2 run: NYSE breakpoints + delisting (Cases A and B) ──
    print("[5/7] main analysis: NYSE breakpoints + delisting (A+B) ...")
    res = run_analysis(panel_ex, adj, ff, nyse=True, delist_mode="AB", verbose=True)
    rows = res["rows"]

    # ── Ablations (for the improvement report) ──
    print("[6/7] ablations ...")
    abl = []
    abl.append(dict(name="v1 (all-stock, no delist)", n_pass=V1_PASS, rows=[
        dict(label=l, **V1[l]) for l in V1]))  # v1 headline cells (from table_3.py)
    r_nyse = run_analysis(panel_ex, adj, ff, nyse=True, delist_mode="none", verbose=False)
    abl.append(dict(name="NYSE bp only", n_pass=r_nyse["n_pass"], rows=r_nyse["rows"]))
    r_delA = run_analysis(panel_ex, adj, ff, nyse=True, delist_mode="A", verbose=False)
    abl.append(dict(name="NYSE bp + delist A", n_pass=r_delA["n_pass"], rows=r_delA["rows"]))
    r_all = run_analysis(panel_ex, adj, ff, nyse=False, delist_mode="AB", verbose=False)
    abl.append(dict(name="all-stock bp + delist AB", n_pass=r_all["n_pass"], rows=r_all["rows"]))
    abl.append(dict(name="v2 (NYSE bp + delist AB)", n_pass=res["n_pass"], rows=rows))

    print("[7/7] write table + plots ...")
    table_md = build_table(rows)
    val_md, val = validation_block(rows)

    nw_lines = ["| Portfolio | CAPM t(NW) | FF3 t(NW) | FF4 t(NW) |", "|---|---:|---:|---:|"]
    for r in rows:
        if r["label"] not in ("P1", "P5", "P10", "BAB"):
            continue
        nw_lines.append(f"| {r['label']} | {r['capm_t_nw']:.2f} | "
                        f"{r['ff3_t_nw']:.2f} | {r['ff4_t_nw']:.2f} |")

    n_obs_note = {r["label"]: r["n"] for r in rows}
    abl_md = ablation_block(abl)
    df = res["df"]
    bab = res["bab"]

    doc = f"""# Table 3 — Beta-sorted decile portfolios and BAB factor (US equities) — v2

**Source:** Frazzini & Pedersen (2014), "Betting Against Beta", Table 3.
**Sample:** {df['month'].min().date()} .. {df['month'].max().date()}
({df['month'].nunique()} months; portfolios start when betas become estimable).
**Weighting:** equal-weighted within decile, rebalanced monthly.
**Returns & alphas:** monthly percent. **Volatility & Sharpe:** annualized.

## v2 fixes (vs table_3.py v1)
1. **NYSE breakpoints** — decile breakpoints are the 10th..90th percentiles of
   beta among **NYSE (exchcd==1) stocks only** each month (PIT exchange code
   merged from `crsp_202601.dsenames`); all stocks are then assigned to deciles
   on those breakpoints. (Paper: "assigned to one of ten deciles portfolios
   based on NYSE breakpoints.")
2. **Delisting returns** — each stock's last-month return is combined with its
   CRSP delisting return from `crsp_202601.dsedelist`:
   `adjusted = (1+ret)(1+dlret_eff)-1`. `dlret_eff` = reported `dlret` when
   valid (`dlret > -1.0`, not NULL), else the Shumway(1997)/BMP(2007) imputation
   for performance-related delistings (dlstcd 500-599): -0.30 NYSE/AMEX,
   -0.55 NASDAQ. Both Case A (delisting month == last panel month) and Case B
   (delisting month == last panel month + 1, i.e. the delisting-month CRSP
   return is a missing sentinel) are applied.

## FF factor units
{ff_units}. CRSP `ret` is decimal, so excess = ret - rf with no extra scaling.

## Table 3

{table_md}

_t-stats below each coefficient are **standard (iid)** time-series t-stats,
matching the paper's convention. The excess-return t-stat uses mean/(std/sqrt(n))._

### Newey-West (HAC, {NW_LAGS} lags) alpha t-stats — supplementary

{chr(10).join(nw_lines)}

## Validation vs paper (tolerance from tables_to_replicate.json)

{val_md}

**Cells passing: {val['n_pass']} / {val['n_total']} (v1 was {V1_PASS} / 32).**

## Ablation — effect of each fix (headline cells; full per-cell in validation above)

{abl_md}

Column key: `P1:ff3_alpha` = P1 3-factor alpha (monthly %), etc. Configs isolate
the breakpoint fix (NYSE bp only) and the delisting fix (delist A = Case A only;
delist AB = Cases A+B). v2 = NYSE bp + delist AB (the headline configuration).

## Observations per portfolio (months with a return)
{ {k: v for k, v in n_obs_note.items() if k in ('P1','P5','P10','BAB')} }

## Remaining limitations (see preparations/assumptions.md)
1. **5-factor alpha skipped** — Pastor-Stambaugh liquidity factor not in
   ClickHouse (covers 1968-2011 only).
2. **`dlret = -1.0` treated as missing** per the task spec (CRSP's Data
   Descriptions Guide flags -1.0 as the "worthless security" return = -100%;
   treating it as missing routes those cases to the Shumway imputation). 383
   performance-related delistings affected — second-order effect on decile means.
3. **Case B attributes the terminal return to the last holding month** (standard
   approximation; the true delisting month has no valid CRSP return to combine).

---
_Generated by src/table_3_v2.py — runtime {time.time() - t0:.1f}s._
"""

    out_md = LAYOUT.result_path("table_3.md")
    out_md.write_text(doc)
    print(f"      wrote {out_md}")
    plot_decile_returns(rows, LAYOUT.result_path("decile_returns.png"))
    print(f"      wrote {LAYOUT.result_path('decile_returns.png')}")
    plot_bab_cumulative(bab, LAYOUT.result_path("bab_cumulative.png"))
    print(f"      wrote {LAYOUT.result_path('bab_cumulative.png')}")

    # Console summary — headline cells vs paper + v1
    print("\n" + "=" * 72)
    print("SUMMARY — headline cells (v2 vs paper vs v1)")
    print("=" * 72)
    by = {r["label"]: r for r in rows}
    for label in ("P1", "P5", "P10", "BAB"):
        r = by[label]; p = PAPER[label]; v1 = V1[label]
        print(f"\n{label}:")
        for m in ("excess_ret", "capm_alpha", "ff3_alpha", "ff4_alpha",
                  "beta_exante", "beta_realized", "vol", "sharpe"):
            mark = "OK" if val["cells"].get((label, m), False) else "**OFF**"
            print(f"   {m:16s} v2={r[m]:8.3f}  paper={p[m]:8.3f}  "
                  f"v1={v1[m]:8.3f}  {mark}")
    print(f"\nCells passing: {val['n_pass']}/{val['n_total']} (v1 was {V1_PASS}/32)")
    print("\nAblation pass counts:")
    for a in abl:
        print(f"   {a['name']:32s} {a['n_pass']}/32")
    print(f"\ntotal runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
