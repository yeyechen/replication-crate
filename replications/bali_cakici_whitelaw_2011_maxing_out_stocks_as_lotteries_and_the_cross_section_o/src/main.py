"""
Replication of Bali, Cakici, Whitelaw (2011)
"Maxing Out: Stocks as Lotteries and the Cross-Section of Expected Returns"

Signal: MAX = max daily return per stock-month
Target: Table 1 — MAX-sorted decile portfolios, VW/EW returns, FF-Carhart 4-factor alphas

This script builds the monthly stock panel (via the CTE pipeline in
`src/sql/panel.sql`) and computes the Table 1 univariate decile sort.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

# --- Add project root to sys.path so utils/ is importable ---
PROJECT_ROOT = Path("/home/ra_alan_mike_share/rep-it-up")
sys.path.insert(0, str(PROJECT_ROOT))

from utils.paths import paper_layout  # noqa: E402
from utils.quantile import assign_quantiles  # noqa: E402
from utils.portfolio import bin_returns, forward_returns  # noqa: E402
from utils.regressions import factor_alpha  # noqa: E402
from utils.metrics import tstat_newey_west  # noqa: E402
from utils.env import load_project_env  # noqa: E402

# Load .env so CLICKHOUSE_* env vars are available
load_project_env()


# --- Configuration ---

LAYOUT = paper_layout(
    "bali_cakici_whitelaw_2011_maxing_out_stocks_as_lotteries_and_the_cross_section_o"
)
LAYOUT.ensure()

# Sample window for portfolios (paper §2.2)
SAMPLE_START = pd.Timestamp("1962-07-01")
SAMPLE_END = pd.Timestamp("2005-12-31")

N_BINS = 10

# Newey-West lag for the FF alpha t-stat and the D10-D1 spread t-stat.
# Per SKILL.md guidance: n_lags=4 is reasonable for monthly portfolios with
# mild autocorrelation (MAX is correlated with prior month's REV).
NW_LAGS_ALPHA = 4
NW_LAGS_SPREAD = 4


# --- ClickHouse connection ---

def _client() -> Client:
    host = os.environ.get("CLICKHOUSE_HOST", "")
    if not host:
        raise RuntimeError(
            "CLICKHOUSE_HOST is not set — ensure .env is loaded."
        )
    return Client(
        host=host,
        port=int(os.environ.get("CLICKHOUSE_PORT", "9000")),
        user=os.environ.get("CLICKHOUSE_USER", "default"),
        password=os.environ.get("CLICKHOUSE_PASSWORD", ""),
        database=os.environ.get("CLICKHOUSE_DATABASE", "default"),
        settings={"max_execution_time": 600},
    )


def q(sql: str) -> pd.DataFrame:
    """Execute a SQL query and return a pandas DataFrame."""
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    """Execute a saved SQL file and return a pandas DataFrame."""
    sql = (LAYOUT.src_path("sql") / name).read_text()
    return q(sql)


# --- Data loading ---

def load_panel() -> pd.DataFrame:
    """Load the monthly panel via the panel.sql CTE pipeline."""
    cache = LAYOUT.data_path("panel.parquet")
    if cache.exists():
        df = pd.read_parquet(cache)
        # Ensure datetime column
        if "month" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["month"]):
            df["month"] = pd.to_datetime(df["month"])
        return df
    df = q_file("panel.sql")
    # Coerce types
    if "month" in df.columns:
        df["month"] = pd.to_datetime(df["month"])
    # Cast permno to int (ClickHouse returns it as int but be safe)
    if "permno" in df.columns:
        df["permno"] = df["permno"].astype("int64")
    df.to_parquet(cache, index=False)
    return df


# --- Table 1 ---

def table_1(panel: pd.DataFrame) -> dict:
    """
    Compute Table 1:
      - 10 decile bins by MAX, each month
      - Per-decile EW and VW average returns
      - Per-decile FF-Carhart 4-factor alpha
      - D10-D1 spread (raw return + alpha) and t-stats
      - Average MAX per decile
    Returns a dict with the metrics, formatted for results/table_1.md
    """
    df = panel.copy()

    # --- Step 1: Forward-shift ret to pair MAX_t with ret_t+1 ---
    # Paper convention: "MAX over the past one month" predicts future returns.
    # In our panel, max_signal at month t is the MAX over calendar month t;
    # the matching return is the next-month return (ret_t+1).
    # Use forward_returns to shift ret by 1 month (overwrite in place).
    df = forward_returns(
        df, signal_col="max_signal", date_col="month",
        ret_col="ret", n_lags=1,
    )

    # --- Step 2: Bin stocks cross-sectionally by MAX ---
    df["bin"] = assign_quantiles(
        df, date_col="month", signal_col="max_signal",
        n_bins=N_BINS, warn_fallback=False,
    )
    df = df.dropna(subset=["bin"])
    df["bin"] = df["bin"].astype(int)

    # --- Step 3: Per-decile EW + VW returns ---
    bin_rets = bin_returns(
        df, date_col="month", bin_col="bin",
        ret_col="ret", mcap_col="mcap_lag1",
    )
    # bin_rets columns: ["month", "bin", "EW", "VW"]

    # --- Step 4: Average MAX per decile (mean of MAX across stocks in each
    #     decile-month, then time-series mean) ---
    avg_max = (
        df.groupby(["month", "bin"])["max_signal"].mean()
        .reset_index()
        .groupby("bin")["max_signal"].mean()
    )

    # --- Step 5: Compute D10-D1 spread time series (for t-stat) ---
    # VW: D10 - D1
    spread_vw = (
        bin_rets.loc[bin_rets["bin"] == N_BINS].set_index("month")["VW"]
        - bin_rets.loc[bin_rets["bin"] == 1].set_index("month")["VW"]
    ).rename("ret")
    # EW: D10 - D1
    spread_ew = (
        bin_rets.loc[bin_rets["bin"] == N_BINS].set_index("month")["EW"]
        - bin_rets.loc[bin_rets["bin"] == 1].set_index("month")["EW"]
    ).rename("ret")

    # --- Step 6: t-stats for raw returns spread ---
    vw_tstat = tstat_newey_west(spread_vw, n_lags=NW_LAGS_SPREAD)
    ew_tstat = tstat_newey_west(spread_ew, n_lags=NW_LAGS_SPREAD)

    # --- Step 7: FF-Carhart 4-factor alpha per decile ---
    # Align factors: panel already carries mkt_rf/smb/hml/mom/rf.
    # Per-decile: excess_decile_ret = decile_ret - rf
    # Regress (excess_decile_ret) on mkt_rf, smb, hml, mom.
    factor_cols = ["mkt_rf", "smb", "hml", "mom"]
    alphas_vw: dict[int, dict] = {}
    alphas_ew: dict[int, dict] = {}

    for b in range(1, N_BINS + 1):
        for w_label, w_col in [("vw", "VW"), ("ew", "EW")]:
            # Per-decile monthly series merged with factors
            sub = bin_rets.loc[bin_rets["bin"] == b, ["month", w_col]].copy()
            sub = sub.rename(columns={w_col: "ret"})
            sub = sub.set_index("month")

            # Pull factors
            ff = (
                df[["month"] + factor_cols + ["rf"]]
                .drop_duplicates(subset=["month"])
                .set_index("month")
            )
            merged = sub.join(ff, how="inner").dropna()
            if len(merged) < 24:
                continue

            result = factor_alpha(
                portfolio_returns=merged["ret"],
                factor_returns=ff,
                factors=factor_cols,
                rf_col="rf",
                ret_col="ret",
                n_lags=NW_LAGS_ALPHA,
                freq="M",
            )
            if w_label == "vw":
                alphas_vw[b] = result
            else:
                alphas_ew[b] = result

    # --- Step 8: D10-D1 alpha spread and t-stat ---
    # Build per-month alpha spread series (alpha_t = D10_alpha_t - D1_alpha_t).
    # Approach: regress each month's excess return series... but factor_alpha
    # returns ONE number (the time-series average). For a per-month alpha
    # series we'd need a rolling window approach. Instead, follow the paper
    # convention: compute the spread series by subtracting per-month alphas
    # implied from running factor regressions on the spread.
    #
    # Easier: build a single factor_alpha run on each spread series directly
    # (this gives the spread alpha), then get t-stat for both spread and alpha.

    # Spread alpha: regress (D10_VW - D1_VW) on FF factors.
    spread_vw_aligned = spread_vw.to_frame("ret").join(
        df[["month", "mkt_rf", "smb", "hml", "mom", "rf"]]
            .drop_duplicates(subset=["month"])
            .set_index("month"),
        how="inner"
    ).dropna()
    spread_ew_aligned = spread_ew.to_frame("ret").join(
        df[["month", "mkt_rf", "smb", "hml", "mom", "rf"]]
            .drop_duplicates(subset=["month"])
            .set_index("month"),
        how="inner"
    ).dropna()

    factor_returns_vw = spread_vw_aligned[factor_cols + ["rf"]].copy()
    factor_returns_ew = spread_ew_aligned[factor_cols + ["rf"]].copy()

    # Use factor_alpha on the spread series to get its alpha and t-stat.
    vw_alpha_result = factor_alpha(
        portfolio_returns=spread_vw_aligned["ret"],
        factor_returns=factor_returns_vw,
        factors=factor_cols,
        rf_col="rf",
        ret_col="ret",
        n_lags=NW_LAGS_ALPHA,
        freq="M",
    )
    ew_alpha_result = factor_alpha(
        portfolio_returns=spread_ew_aligned["ret"],
        factor_returns=factor_returns_ew,
        factors=factor_cols,
        rf_col="rf",
        ret_col="ret",
        n_lags=NW_LAGS_ALPHA,
        freq="M",
    )

    # --- Step 9: Average returns per decile (for Table 1 row values) ---
    avg_vw_ret = bin_rets.groupby("bin")["VW"].mean()
    avg_ew_ret = bin_rets.groupby("bin")["EW"].mean()

    # --- Assemble results ---
    table = {
        "n_months": int(bin_rets["month"].nunique()),
        "n_obs_total": int(len(df)),
        "avg_obs_per_month": float(len(df) / bin_rets["month"].nunique()),
        "deciles": {},
        "spread": {
            "vw_ret_diff": float(avg_vw_ret.loc[N_BINS] - avg_vw_ret.loc[1]),
            "ew_ret_diff": float(avg_ew_ret.loc[N_BINS] - avg_ew_ret.loc[1]),
            "vw_alpha_diff": float(vw_alpha_result["alpha_monthly"]),
            "ew_alpha_diff": float(ew_alpha_result["alpha_monthly"]),
            "vw_ret_tstat": float(vw_tstat["t_stat"]),
            "ew_ret_tstat": float(ew_tstat["t_stat"]),
            "vw_alpha_tstat": float(vw_alpha_result["t_alpha_newey_west"]),
            "ew_alpha_tstat": float(ew_alpha_result["t_alpha_newey_west"]),
            "vw_alpha_tstat_mean_lags": NW_LAGS_ALPHA,
            "vw_spread_tstat_nlags": NW_LAGS_SPREAD,
        },
    }
    for b in range(1, N_BINS + 1):
        table["deciles"][b] = {
            "vw_ret": float(avg_vw_ret.loc[b]) if b in avg_vw_ret.index else None,
            "ew_ret": float(avg_ew_ret.loc[b]) if b in avg_ew_ret.index else None,
            "vw_alpha": float(alphas_vw[b]["alpha_monthly"]) if b in alphas_vw else None,
            "ew_alpha": float(alphas_ew[b]["alpha_monthly"]) if b in alphas_ew else None,
            "avg_max": float(avg_max.loc[b]) if b in avg_max.index else None,
        }
    return table


def render_table_md(table: dict) -> str:
    """Render the Table 1 results as Markdown."""
    lines = []
    lines.append("# Table 1 — MAX-Sorted Decile Portfolios")
    lines.append("")
    lines.append("**Replication of**: Bali, Cakici, Whitelaw (2011) — Table 1")
    lines.append("**Sample period**: July 1962 – December 2005 (monthly)")
    lines.append("**Universe**: NYSE/AMEX/Nasdaq common shares (shrcd 10/11, exchcd 1/2/3)")
    lines.append(f"**N months**: {table['n_months']}")
    lines.append(f"**N observations (stock-months)**: {table['n_obs_total']:,}")
    lines.append(f"**Avg obs/month**: {table['avg_obs_per_month']:.1f}")
    lines.append("")
    lines.append("Returns and alphas are in **percent per month**. MAX is in **percent**.")
    lines.append("")

    # Header
    header_cols = [
        "Decile", "VW Ret", "VW Alpha", "EW Ret", "EW Alpha", "Avg MAX",
    ]
    lines.append("| " + " | ".join(header_cols) + " |")
    lines.append("|" + "|".join(["---"] * len(header_cols)) + "|")
    for b in range(1, N_BINS + 1):
        d = table["deciles"][b]
        lines.append(
            f"| D{b} | "
            f"{d['vw_ret']*100:.2f} | "
            f"{d['vw_alpha']*100:.2f} | "
            f"{d['ew_ret']*100:.2f} | "
            f"{d['ew_alpha']*100:.2f} | "
            f"{d['avg_max']*100:.2f} |"
        )

    spread = table["spread"]
    lines.append("| --- | --- | --- | --- | --- | --- |")
    lines.append(
        f"| **D10 - D1** | "
        f"{spread['vw_ret_diff']*100:.2f} | "
        f"{spread['vw_alpha_diff']*100:.2f} | "
        f"{spread['ew_ret_diff']*100:.2f} | "
        f"{spread['ew_alpha_diff']*100:.2f} | "
        f"  |"
    )
    lines.append("")
    lines.append("## t-statistics (Newey-West)")
    lines.append("")
    lines.append(f"Newey-West lags for D10-D1 raw return spread: "
                 f"n_lags = {spread['vw_spread_tstat_nlags']}")
    lines.append(f"Newey-West lags for FF-Carhart alpha t-stat: "
                 f"n_lags = {spread['vw_alpha_tstat_mean_lags']}")
    lines.append("")
    lines.append("| Spread | t-stat |")
    lines.append("| --- | --- |")
    lines.append(f"| VW raw return | {spread['vw_ret_tstat']:.2f} |")
    lines.append(f"| EW raw return | {spread['ew_ret_tstat']:.2f} |")
    lines.append(f"| VW FF-Carhart alpha | {spread['vw_alpha_tstat']:.2f} |")
    lines.append(f"| EW FF-Carhart alpha | {spread['ew_alpha_tstat']:.2f} |")
    lines.append("")
    return "\n".join(lines)


def table_6_size(panel: pd.DataFrame) -> dict:
    """Wrapper for SIZE control. SIZE = log(mcap_lag1)."""
    df = panel.copy()
    df["size"] = np.log(df["mcap_lag1"] + 1e-6)
    return _bivariate_sort(df, control_col="size")


def _bivariate_sort(df: pd.DataFrame, control_col: str) -> dict:
    """
    Generic dependent-sort helper for Table 6: control for `control_col`, sort by MAX.

    Within each month:
      1. Assign deciles by `control_col` (cross-sectional, dropna).
      2. Within each control decile, assign deciles by `max_signal`.
      3. Average each MAX decile's VW return across the 10 control deciles.
    Then compute D10-D1 spread + 4-factor alpha + Newey-West t-stats.
    """
    # Forward-shift ret to pair MAX_t with ret_t+1
    df = forward_returns(df, signal_col="max_signal", date_col="month",
                         ret_col="ret", n_lags=1)
    df = df.dropna(subset=["ret", control_col])

    # Within month: assign control deciles
    df["ctl_decile"] = assign_quantiles(
        df, date_col="month", signal_col=control_col,
        n_bins=N_BINS, warn_fallback=False,
    )
    df = df.dropna(subset=["ctl_decile"])
    df["ctl_decile"] = df["ctl_decile"].astype(int)

    # Within (month, ctl_decile): assign MAX deciles
    df["max_decile"] = (
        df.groupby(["month", "ctl_decile"])["max_signal"]
        .transform(
            lambda x: pd.qcut(x, N_BINS, labels=False, duplicates="drop")
        )
    ) + 1
    df = df.dropna(subset=["max_decile"])
    df["max_decile"] = df["max_decile"].astype(int)

    # Per-(month, ctl_decile, max_decile): VW return
    cell_vw = (
        df.groupby(["month", "ctl_decile", "max_decile"])
        .apply(
            lambda g: pd.Series({
                "VW": (g["ret"] * g["mcap_lag1"]).sum() / g["mcap_lag1"].sum(),
            }),
            include_groups=False,
        ).reset_index()
    )

    # Average each MAX decile across the 10 control deciles per month
    avg_vw = (
        cell_vw.groupby(["month", "max_decile"])["VW"].mean().reset_index()
    )
    pivot_vw = avg_vw.pivot(index="month", columns="max_decile", values="VW")

    avg_per_decile = pivot_vw.mean() * 100  # convert to percent

    spread_vw = pivot_vw[N_BINS] - pivot_vw[1]
    avg_spread_vw = spread_vw.mean() * 100

    # FF-Carhart alpha on the spread series
    factor_cols = ["mkt_rf", "smb", "hml", "mom"]
    ff = (
        df[["month"] + factor_cols + ["rf"]]
        .drop_duplicates(subset=["month"])
        .set_index("month")
    )
    spread_aligned = spread_vw.to_frame("ret").join(ff, how="inner").dropna()
    factor_returns = spread_aligned[factor_cols + ["rf"]].copy()
    spread_alpha = factor_alpha(
        portfolio_returns=spread_aligned["ret"],
        factor_returns=factor_returns,
        factors=factor_cols, rf_col="rf", ret_col="ret",
        n_lags=NW_LAGS_ALPHA, freq="M",
    )

    spread_tstat = tstat_newey_west(spread_vw, n_lags=NW_LAGS_SPREAD)

    return {
        "per_decile_vw": {b: float(avg_per_decile.get(b, np.nan)) for b in range(1, N_BINS + 1)},
        "spread_vw": float(avg_spread_vw),
        "spread_alpha": float(spread_alpha["alpha_monthly"] * 100),
        "spread_vw_tstat": float(spread_tstat["t_stat"]),
        "spread_alpha_tstat": float(spread_alpha["t_alpha_newey_west"]),
    }


def table_6_bm(panel: pd.DataFrame) -> dict:
    """Table 6 BM control. Uses `bm` column already in panel (FF B/M ratio)."""
    df = panel.copy()
    return _bivariate_sort(df, control_col="bm")


def table_6_rev(panel: pd.DataFrame) -> dict:
    """Table 6 REV control. REV = monthly return at t-1 (1-month lagged return)."""
    df = panel.copy()
    df = df.sort_values(["permno", "month"]).reset_index(drop=True)
    df["rev"] = df.groupby("permno")["ret"].shift(1)
    return _bivariate_sort(df, control_col="rev")


def table_6_mom(panel: pd.DataFrame) -> dict:
    """Table 6 MOM control. MOM = cumulative return from month t-12 to t-2 (skip t-1)."""
    df = panel.copy()
    df = df.sort_values(["permno", "month"]).reset_index(drop=True)
    # Compute (1+ret) product over rolling 11-month window ending at t-2.
    # Use a transform with a shift to align: log(1+r) sum over [t-12, t-2].
    log_ret = np.log1p(df["ret"].fillna(0.0))
    df["log_ret"] = log_ret
    # 11-month rolling sum (t-12 to t-2 inclusive is 11 months)
    df["mom_log"] = (
        df.groupby("permno")["log_ret"]
        .transform(lambda s: s.shift(2).rolling(window=11, min_periods=11).sum())
    )
    df["mom"] = np.expm1(df["mom_log"])  # cumulative return
    return _bivariate_sort(df, control_col="mom")


def table_6_illiq(panel: pd.DataFrame) -> dict:
    """Table 6 ILLIQ control. ILLIQ = Amihud-style: mean(|ret|/vol) over daily returns in month."""
    df = panel.copy()
    return _bivariate_sort(df, control_col="illiq")


def render_table_6_md(tables: dict) -> str:
    """Render Table 6 bivariate sorts as markdown (multiple controls)."""
    lines = []
    lines.append("# Table 6 Panel A — Bivariate Sorts: MAX controlling for SIZE / BM / REV")
    lines.append("")
    lines.append("**Replication of**: Bali, Cakici, Whitelaw (2011) — Table 6 Panel A")
    lines.append("**Sample period**: July 1962 – December 2005")
    lines.append("**Method**: Independent sort — first by control variable into deciles,")
    lines.append("then within each control decile sort by MAX into deciles. Average each")
    lines.append("MAX decile's VW return across the 10 control deciles.")
    lines.append("")
    paper = {
        "SIZE": {1: 1.47, 2: 1.60, 3: 1.69, 4: 1.65, 5: 1.57,
                  6: 1.49, 7: 1.29, 8: 1.20, 9: 0.93, 10: 0.25,
                  "ret_diff": -1.22, "alpha_diff": -1.19,
                  "ret_tstat": -4.49, "alpha_tstat": -5.98},
        "BM":   {1: 1.51, 2: 1.49, 3: 1.42, 4: 1.30, 5: 1.32,
                  6: 1.17, 7: 1.06, 8: 1.06, 9: 0.95, 10: 0.58,
                  "ret_diff": -0.93, "alpha_diff": -1.06,
                  "ret_tstat": -3.23, "alpha_tstat": -4.87},
        "REV":  {1: 1.45, 2: 1.43, 3: 1.39, 4: 1.36, 5: 1.23,
                  6: 1.26, 7: 1.10, 8: 1.13, 9: 0.94, 10: 0.64,
                  "ret_diff": -0.81, "alpha_diff": -0.98,
                  "ret_tstat": -2.70, "alpha_tstat": -5.37},
        "MOM":  {1: 1.27, 2: 1.18, 3: 1.18, 4: 1.16, 5: 1.13,
                  6: 1.07, 7: 1.04, 8: 1.05, 9: 0.96, 10: 0.62,
                  "ret_diff": -0.65, "alpha_diff": -0.70,
                  "ret_tstat": -3.18, "alpha_tstat": -5.30},
        "ILLIQ": {"ret_diff": -1.11, "alpha_diff": -1.12,
                  "ret_tstat": -4.07, "alpha_tstat": -5.74},
    }
    for ctrl in ("SIZE", "BM", "REV", "MOM", "ILLIQ"):
        lines.append(f"## Controlling for {ctrl}")
        lines.append("")
        lines.append(f"| Decile | VW Ret (paper / ours) |")
        lines.append("|---|---|")
        t = tables[ctrl]
        for b in range(1, N_BINS + 1):
            paper_str = f"{paper[ctrl].get(b, 0.0):.2f}" if b in paper[ctrl] else "—"
            lines.append(f"| D{b} | {paper_str} / {t['per_decile_vw'][b]:.2f} |")
        lines.append(f"| **D10-D1** | **{paper[ctrl]['ret_diff']:.2f}** / **{t['spread_vw']:.2f}** |")
        lines.append("")
        lines.append("| Spread stat | Paper | Ours | t-stat (paper / ours) |")
        lines.append("|---|---|---|---|")
        lines.append(f"| VW raw return | {paper[ctrl]['ret_diff']:.2f} | {t['spread_vw']:.2f} | "
                     f"{paper[ctrl]['ret_tstat']:.2f} / {t['spread_vw_tstat']:.2f} |")
        lines.append(f"| VW 4-factor alpha | {paper[ctrl]['alpha_diff']:.2f} | {t['spread_alpha']:.2f} | "
                     f"{paper[ctrl]['alpha_tstat']:.2f} / {t['spread_alpha_tstat']:.2f} |")
        lines.append("")
    return "\n".join(lines)


def main():
    print("[1/3] Loading panel from ClickHouse (via src/sql/panel.sql)")
    panel = load_panel()
    print(f"      Panel: {len(panel):,} rows × {panel.shape[1]} cols")
    print(f"      Months: {panel['month'].min().date()} → {panel['month'].max().date()}")
    print(f"      Avg stocks/month: {panel.groupby('month').size().mean():.0f}")

    print("[2/3] Computing Tables 1 and 6 (SIZE, BM, REV, MOM, ILLIQ controls)")
    table1 = table_1(panel)
    table6_size_r = table_6_size(panel)
    table6_bm_r = table_6_bm(panel)
    table6_rev_r = table_6_rev(panel)
    table6_mom_r = table_6_mom(panel)
    table6_illiq_r = table_6_illiq(panel)

    print("[3/3] Writing results/table_1.md and results/table_6.md")
    out1 = LAYOUT.result_path("table_1.md")
    out6 = LAYOUT.result_path("table_6.md")
    out1.write_text(render_table_md(table1))
    out6.write_text(render_table_6_md({
        "SIZE": table6_size_r,
        "BM": table6_bm_r,
        "REV": table6_rev_r,
        "MOM": table6_mom_r,
        "ILLIQ": table6_illiq_r,
    }))

    # Also dump a small JSON for downstream audit use
    metrics = {
        "n_months": table1["n_months"],
        "n_obs_total": table1["n_obs_total"],
        "avg_obs_per_month": table1["avg_obs_per_month"],
        "deciles": {
            f"D{b}": {
                "vw_ret": table1["deciles"][b]["vw_ret"],
                "vw_alpha": table1["deciles"][b]["vw_alpha"],
                "ew_ret": table1["deciles"][b]["ew_ret"],
                "ew_alpha": table1["deciles"][b]["ew_alpha"],
                "avg_max": table1["deciles"][b]["avg_max"],
            }
            for b in range(1, N_BINS + 1)
        },
        "spread": table1["spread"],
    }
    (LAYOUT.data_path("table_1_metrics.json")).write_text(
        json.dumps(metrics, indent=2, default=str)
    )
    (LAYOUT.data_path("table_6_metrics.json")).write_text(
        json.dumps({
            "SIZE": table6_size_r,
            "BM": table6_bm_r,
            "REV": table6_rev_r,
        }, indent=2, default=str)
    )

    # Emit canonical data/metrics.json — flat dict keyed by metric name,
    # values in DECIMAL units. Format consumed by scripts/score_replication.py.
    canonical_metrics: dict[str, dict] = {}
    for b in range(1, N_BINS + 1):
        d = table1["deciles"][b]
        # Convert decimal → percent to match paper's printed units
        canonical_metrics[f"D{b}_vw_ret"] = {"value": d["vw_ret"] * 100, "unit": "percent_per_month"}
        canonical_metrics[f"D{b}_vw_alpha"] = {"value": d["vw_alpha"] * 100, "unit": "percent_per_month"}
        canonical_metrics[f"D{b}_ew_ret"] = {"value": d["ew_ret"] * 100, "unit": "percent_per_month"}
        canonical_metrics[f"D{b}_ew_alpha"] = {"value": d["ew_alpha"] * 100, "unit": "percent_per_month"}
        canonical_metrics[f"D{b}_avg_max"] = {"value": d["avg_max"] * 100, "unit": "percent_per_month"}
    canonical_metrics["vw_ret_diff"] = {"value": table1["spread"]["vw_ret_diff"] * 100, "unit": "percent_per_month"}
    canonical_metrics["vw_alpha_diff"] = {"value": table1["spread"]["vw_alpha_diff"] * 100, "unit": "percent_per_month"}
    canonical_metrics["ew_ret_diff"] = {"value": table1["spread"]["ew_ret_diff"] * 100, "unit": "percent_per_month"}
    canonical_metrics["ew_alpha_diff"] = {"value": table1["spread"]["ew_alpha_diff"] * 100, "unit": "percent_per_month"}
    canonical_metrics["vw_ret_tstat"] = {"value": table1["spread"]["vw_ret_tstat"], "unit": "t_stat"}
    canonical_metrics["vw_alpha_tstat"] = {"value": table1["spread"]["vw_alpha_tstat"], "unit": "t_stat"}
    canonical_metrics["ew_ret_tstat"] = {"value": table1["spread"]["ew_ret_tstat"], "unit": "t_stat"}
    canonical_metrics["ew_alpha_tstat"] = {"value": table1["spread"]["ew_alpha_tstat"], "unit": "t_stat"}
    # Table 6 SIZE-control bivariate sort
    for b in range(1, N_BINS + 1):
        canonical_metrics[f"SIZE_D{b}_vw"] = {
            "value": table6_size_r["per_decile_vw"][b],
            "unit": "percent_per_month",
        }
    canonical_metrics["SIZE_vw_ret_diff"] = {"value": table6_size_r["spread_vw"], "unit": "percent_per_month"}
    canonical_metrics["SIZE_vw_alpha_diff"] = {"value": table6_size_r["spread_alpha"], "unit": "percent_per_month"}
    canonical_metrics["SIZE_vw_ret_tstat"] = {"value": table6_size_r["spread_vw_tstat"], "unit": "t_stat"}
    canonical_metrics["SIZE_vw_alpha_tstat"] = {"value": table6_size_r["spread_alpha_tstat"], "unit": "t_stat"}
    # Table 6 BM-control bivariate sort
    for b in range(1, N_BINS + 1):
        canonical_metrics[f"BM_D{b}_vw"] = {
            "value": table6_bm_r["per_decile_vw"][b],
            "unit": "percent_per_month",
        }
    canonical_metrics["BM_vw_ret_diff"] = {"value": table6_bm_r["spread_vw"], "unit": "percent_per_month"}
    canonical_metrics["BM_vw_alpha_diff"] = {"value": table6_bm_r["spread_alpha"], "unit": "percent_per_month"}
    canonical_metrics["BM_vw_ret_tstat"] = {"value": table6_bm_r["spread_vw_tstat"], "unit": "t_stat"}
    canonical_metrics["BM_vw_alpha_tstat"] = {"value": table6_bm_r["spread_alpha_tstat"], "unit": "t_stat"}
    # Table 6 REV-control bivariate sort
    for b in range(1, N_BINS + 1):
        canonical_metrics[f"REV_D{b}_vw"] = {
            "value": table6_rev_r["per_decile_vw"][b],
            "unit": "percent_per_month",
        }
    canonical_metrics["REV_vw_ret_diff"] = {"value": table6_rev_r["spread_vw"], "unit": "percent_per_month"}
    canonical_metrics["REV_vw_alpha_diff"] = {"value": table6_rev_r["spread_alpha"], "unit": "percent_per_month"}
    canonical_metrics["REV_vw_ret_tstat"] = {"value": table6_rev_r["spread_vw_tstat"], "unit": "t_stat"}
    canonical_metrics["REV_vw_alpha_tstat"] = {"value": table6_rev_r["spread_alpha_tstat"], "unit": "t_stat"}
    # Table 6 MOM-control bivariate sort
    for b in range(1, N_BINS + 1):
        canonical_metrics[f"MOM_D{b}_vw"] = {
            "value": table6_mom_r["per_decile_vw"][b],
            "unit": "percent_per_month",
        }
    canonical_metrics["MOM_vw_ret_diff"] = {"value": table6_mom_r["spread_vw"], "unit": "percent_per_month"}
    canonical_metrics["MOM_vw_alpha_diff"] = {"value": table6_mom_r["spread_alpha"], "unit": "percent_per_month"}
    canonical_metrics["MOM_vw_ret_tstat"] = {"value": table6_mom_r["spread_vw_tstat"], "unit": "t_stat"}
    canonical_metrics["MOM_vw_alpha_tstat"] = {"value": table6_mom_r["spread_alpha_tstat"], "unit": "t_stat"}
    # Table 6 ILLIQ-control bivariate sort
    canonical_metrics["ILLIQ_vw_ret_diff"] = {"value": table6_illiq_r["spread_vw"], "unit": "percent_per_month"}
    canonical_metrics["ILLIQ_vw_alpha_diff"] = {"value": table6_illiq_r["spread_alpha"], "unit": "percent_per_month"}
    canonical_metrics["ILLIQ_vw_ret_tstat"] = {"value": table6_illiq_r["spread_vw_tstat"], "unit": "t_stat"}
    canonical_metrics["ILLIQ_vw_alpha_tstat"] = {"value": table6_illiq_r["spread_alpha_tstat"], "unit": "t_stat"}
    # Canonical format: wrapped in {schema_version, slug, metrics: {name: {value, unit}}}
    canonical_payload = {
        "schema_version": 2,
        "slug": LAYOUT.slug,
        "metrics": canonical_metrics,
    }
    (LAYOUT.data_path("metrics.json")).write_text(
        json.dumps(canonical_payload, indent=2, default=str)
    )
    print(f"      Wrote {out1}")
    print(f"      Wrote {out6}")
    print("Done.")


if __name__ == "__main__":
    main()
