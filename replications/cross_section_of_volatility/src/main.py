"""
Replication of Ang, Hodrick, Xing, Zhang (2006) "The Cross-Section of
Volatility and Expected Returns" — idiosyncratic-volatility analysis
(Tables VI-XI).

Stage 7 — Data pipeline. Builds the analysis-ready monthly cross-section
`data/panel.parquet` (one row per permno per month, June 1963 - Dec 2000).

Signals / controls (per permno, per month t; all contemporaneous at t —
the analysis code lags signals one month before pairing with returns):
    ret         monthly stock return (CRSP msf, delisting-adjusted)
    ret_excess  ret - monthly rf
    me          market equity, $ millions = abs(prc)*shrout/1000
    ivol        std of daily FF3 regression residuals (n>=17)
    tvol        std of daily raw returns (n>=17)
    size        log(me in $millions)
    bm          book equity / December ME (FF convention, BE>0)
    mom         cumret(t-12 .. t-2)
    volume      mean daily dollar volume ($ millions) over month t
    turnover    mean daily vol/(shares outstanding) over month t
    leverage    total assets / book equity
    coskew      coskewness of stock return with market factor (month t)
    n_obs       # daily obs used for ivol
    hexcd       exchange code (for NYSE-only sorts / NYSE breakpoints)

Pipeline (SQL-first; see src/sql/*.sql):
    monthly_returns.sql     msf x dsenames -> ret, me, hexcd, size, mom
    daily_stats.sql         dsf x dsenames x ff.three_factor -> per-(permno,
                            month) sufficient statistics (NOT raw daily rows)
    compustat_controls.sql  funda x link x Dec-ME -> bm, leverage
    ff_monthly.sql          monthly rf (+ factors) for ret_excess
    delisting_returns.sql   effective delisting returns
    main.py                 solve per-stock FF3 regression in closed form
                            from the sufficient statistics; assemble panel.

Key data facts verified live (see preparations/assumptions.md):
    * ff.three_factor is DAILY and in DECIMAL (NOT percent) -> no /100.
    * Daily rf is used directly for daily excess returns.
    * CRSP dsf.vol is in SHARES -> dollar volume = abs(prc)*vol (no *1000).
"""
from __future__ import annotations

import argparse
import time

import numpy as np
import pandas as pd
from clickhouse_driver import Client

from utils.env import get_clickhouse_config, load_project_env
from utils.paths import paper_layout

# ── paths / env ─────────────────────────────────────────────────────
load_project_env()
SLUG = "cross_section_of_volatility"
LAYOUT = paper_layout(SLUG)
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")
CFG = get_clickhouse_config()

MIN_OBS = 17  # paper: "more than 17 daily observations" (L177)


# ── ClickHouse helpers ──────────────────────────────────────────────
def _client() -> Client:
    return Client(
        host=CFG["host"],
        port=int(CFG["port"]),
        user=CFG["user"],
        password=CFG["password"],
        database=CFG["database"],
        settings={
            "max_execution_time": 1200,
            "max_rows_to_read": 10_000_000_000,
            "timeout_before_checking_execution_speed": 0,
        },
    )


def q(sql: str) -> pd.DataFrame:
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    return q((SQL_DIR / name).read_text())


# ── daily signals from sufficient statistics ────────────────────────
def compute_daily_signals(stats: pd.DataFrame) -> pd.DataFrame:
    """Solve the per-(permno, month) FF3 regression in closed form from
    the sufficient statistics produced by daily_stats.sql, and derive
    ivol, tvol, coskew, volume, turnover. Fully vectorised (no per-group
    apply): the 4x4 normal equations are stacked and solved in one
    np.linalg.solve call.
    """
    stats = stats.copy()
    stats["month"] = pd.to_datetime(stats["month"])
    n = stats["n_obs"].to_numpy(dtype=np.float64)
    N = len(stats)

    ivol = np.full(N, np.nan)
    tvol = np.full(N, np.nan)
    coskew = np.full(N, np.nan)

    # ---- IVOL: FF3 regression y = a + b1*mkt + b2*smb + b3*hml + eps ----
    valid = n >= MIN_OBS
    if valid.any():
        v = np.where(valid)[0]
        nv = n[v]
        XtX = np.empty((len(v), 4, 4), dtype=np.float64)
        sm = stats["sum_m"].to_numpy(); ss = stats["sum_s"].to_numpy()
        sh = stats["sum_h"].to_numpy()
        XtX[:, 0, 0] = nv
        XtX[:, 0, 1] = XtX[:, 1, 0] = sm[v]
        XtX[:, 0, 2] = XtX[:, 2, 0] = ss[v]
        XtX[:, 0, 3] = XtX[:, 3, 0] = sh[v]
        XtX[:, 1, 1] = stats["sum_m2"].to_numpy()[v]
        XtX[:, 1, 2] = XtX[:, 2, 1] = stats["sum_ms"].to_numpy()[v]
        XtX[:, 1, 3] = XtX[:, 3, 1] = stats["sum_mh"].to_numpy()[v]
        XtX[:, 2, 2] = stats["sum_s2"].to_numpy()[v]
        XtX[:, 2, 3] = XtX[:, 3, 2] = stats["sum_sh"].to_numpy()[v]
        XtX[:, 3, 3] = stats["sum_h2"].to_numpy()[v]
        Xty = np.stack([
            stats["sum_y"].to_numpy()[v],
            stats["sum_ym"].to_numpy()[v],
            stats["sum_ys"].to_numpy()[v],
            stats["sum_yh"].to_numpy()[v],
        ], axis=1)
        try:
            # b must be (M,4,1) for a batched (M,4,4) solve; squeeze back.
            b = np.linalg.solve(XtX, Xty[:, :, None])[:, :, 0]
        except np.linalg.LinAlgError:
            # Degenerate group fallback: per-row least squares.
            b = np.full((len(v), 4), np.nan)
            for i in range(len(v)):
                try:
                    b[i], *_ = np.linalg.lstsq(XtX[i], Xty[i], rcond=None)
                except np.linalg.LinAlgError:
                    b[i] = np.nan
        sse = stats["sum_y2"].to_numpy()[v] - np.einsum("ij,ij->i", b, Xty)
        sse = np.clip(sse, 0.0, None)
        ivol[v] = np.sqrt(sse / (nv - 1.0))

    # ---- TVOL: std of daily raw returns ----
    if valid.any():
        v = np.where(valid)[0]
        nv = n[v]
        sum_ri = stats["sum_ri"].to_numpy()[v]
        sum_ri2 = stats["sum_ri2"].to_numpy()[v]
        var = (sum_ri2 - sum_ri * sum_ri / nv) / (nv - 1.0)
        tvol[v] = np.sqrt(np.clip(var, 0.0, None))

    # ---- Coskewness (Harvey-Siddique): E[ei*em^2] / (sd_i * var_m) ----
    sum_ri = stats["sum_ri"].to_numpy()
    sum_ri2 = stats["sum_ri2"].to_numpy()
    sum_m = stats["sum_m"].to_numpy()
    sum_m2 = stats["sum_m2"].to_numpy()
    sum_ri_m = stats["sum_ri_m"].to_numpy()
    sum_ri_m2 = stats["sum_ri_m2"].to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        S_ii = sum_ri2 - sum_ri * sum_ri / n
        S_mm = sum_m2 - sum_m * sum_m / n
        rbar_m = sum_m / n
        S_im2 = (sum_ri_m2 - 2.0 * rbar_m * sum_ri_m
                 + rbar_m * rbar_m * sum_ri - (sum_ri / n) * S_mm)
        cs = S_im2 * np.sqrt(n) / (np.sqrt(S_ii) * S_mm)
    ok = (n >= 3) & (S_ii > 0) & (S_mm > 0)
    coskew[ok] = cs[ok]

    # ---- Volume ($ millions) and turnover ----
    # Averaged over the same n_obs sample days as ivol/tvol/coskew
    # (non-trading days count as zero volume). See assumptions.md A13 for
    # the denominator ambiguity (n_obs vs trading-days).
    with np.errstate(divide="ignore", invalid="ignore"):
        volume = np.where(n > 0, stats["sum_dvol_million"].to_numpy() / n, np.nan)
        turnover = np.where(n > 0, stats["sum_turn"].to_numpy() / n, np.nan)

    return pd.DataFrame({
        "permno": stats["permno"].to_numpy(),
        "month": stats["month"].to_numpy(),
        "ivol": ivol,
        "tvol": tvol,
        "coskew": coskew,
        "volume": volume,
        "turnover": turnover,
        "n_obs": n,
    })


# ── delisting adjustment ────────────────────────────────────────────
def apply_delisting(panel: pd.DataFrame, delist: pd.DataFrame) -> pd.DataFrame:
    """Compound the effective delisting return into the stock's LAST
    trading-month return (A1, A12). dlret_eff comes from
    delisting_returns.sql.

    CRSP records dlstdt in the month of (or just after) the last trade —
    in this data the gap (dlstdt month - last panel month) is 0-1 months
    for ~91% of events. So the delisting return is attached to the last
    panel month for events whose dlstdt is 0-6 months after it; stale
    records (gap > 6 months, ~6% of events, max 222 months — data
    artifacts) are dropped.
    """
    delist = delist.copy()
    delist["dlstdt"] = pd.to_datetime(delist["dlstdt"])
    delist["target_month"] = delist["dlstdt"].dt.to_period("M").dt.to_timestamp()

    last = (panel.groupby("permno")["month"].max()
            .reset_index().rename(columns={"month": "last_month"}))
    d = delist.merge(last, on="permno", how="inner")
    gap = ((d["target_month"].dt.year - d["last_month"].dt.year) * 12
           + (d["target_month"].dt.month - d["last_month"].dt.month))
    d = d[(gap >= 0) & (gap <= 6)].copy()
    d = d.drop_duplicates("permno", keep="last")

    merged = panel.merge(
        d[["permno", "last_month", "dlret_eff"]],
        left_on=["permno", "month"],
        right_on=["permno", "last_month"],
        how="left",
    )
    mask = merged["dlret_eff"].notna()
    n_adj = int(mask.sum())
    n_nonzero = int((merged.loc[mask, "dlret_eff"] != 0).sum())
    merged.loc[mask, "ret"] = (
        (1.0 + merged.loc[mask, "ret"]) * (1.0 + merged.loc[mask, "dlret_eff"]) - 1.0
    )
    print(f"  Applied delisting adjustment to {n_adj:,} last-month rows "
          f"({n_nonzero:,} with non-zero dlret_eff)")
    return merged.drop(columns=["last_month", "dlret_eff"])


# ── summary report ──────────────────────────────────────────────────
def summarize(panel: pd.DataFrame) -> str:
    num_cols = ["ret", "ret_excess", "me", "ivol", "tvol", "size", "bm",
                "mom", "volume", "turnover", "leverage", "coskew", "n_obs"]
    lines = []
    for c in num_cols:
        if c not in panel.columns:
            continue
        x = panel[c]
        if x.notna().any():
            q05, q25, q75, q95 = (x.quantile(q) for q in (0.05, 0.25, 0.75, 0.95))
            lines.append(
                f"| {c} | {x.count():,} | {x.mean():.5f} | {x.median():.5f} | "
                f"{x.std():.5f} | {x.min():.5f} | {q05:.5f} | {q25:.5f} | "
                f"{q75:.5f} | {q95:.5f} | {x.max():.5f} | {x.isna().sum():,} |"
            )
    n_rows = len(panel)
    n_months = panel["month"].nunique()
    n_perms = panel["permno"].nunique()
    avg_per_month = n_rows / max(1, n_months)

    # stocks per month over time (per year: mean #rows and #with ivol per month)
    yr = panel["month"].dt.year
    yearly = panel.assign(_y=yr, _hasivol=panel["ivol"].notna().astype(int))
    yt = (yearly.groupby("_y")
          .agg(n_stocks=("permno", "count"), n_ivol=("_hasivol", "sum"),
               n_months=("month", "nunique")))
    yt["n_stocks"] = (yt["n_stocks"] / yt["n_months"]).round().astype(int)
    yt["n_ivol"] = (yt["n_ivol"] / yt["n_months"]).round().astype(int)
    yt_lines = "\n".join(
        f"| {y} | {int(r.n_stocks):,} | {int(r.n_ivol):,} |"
        for y, r in yt.iterrows()
    )

    return f"""# Panel summary — Ang, Hodrick, Xing, Zhang (2006), IVOL analysis

- Rows: **{n_rows:,}**
- Unique permnos: **{n_perms:,}**
- Unique months: **{n_months:,}**
- First month: **{panel['month'].min():%Y-%m-%d}** (first formation month; first holding return = 1963-07)
- Last month:  **{panel['month'].max():%Y-%m-%d}**
- Average obs/month: **{avg_per_month:,.0f}**
- Columns: {', '.join(panel.columns.tolist())}

## Signal / control summary statistics

| column | count | mean | median | std | min | p5 | p25 | p75 | p95 | max | null |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(lines)}

## Stocks per month over time (yearly average)

| year | avg stocks/month | avg with IVOL/month |
|---|---:|---:|
{yt_lines}

## Notes
- FF factors verified DECIMAL (no /100); daily rf used for daily excess returns.
- IVOL/TVOL require n_obs >= {MIN_OBS}. volume = mean(abs(prc)*vol)/1e6 ($M); turnover = mean(vol/(shrout*1000)).
- All variables contemporaneous at month t; analysis lags signals 1 month for sorting (see assumptions.md A8).
"""


# ── build panel ─────────────────────────────────────────────────────
def build_panel() -> None:
    out_panel = LAYOUT.data_path("panel.parquet")
    out_summary = LAYOUT.result_path("panel_summary.md")

    print("Pulling monthly returns (monthly_returns.sql)…")
    t0 = time.time()
    panel = q_file("monthly_returns.sql")
    panel["month"] = pd.to_datetime(panel["month"])
    print(f"  {len(panel):,} rows in {time.time() - t0:.1f}s")

    print("Applying delisting-return adjustment…")
    delist = q_file("delisting_returns.sql")
    panel = apply_delisting(panel, delist)

    print("Pulling monthly FF factors (ff_monthly.sql)…")
    ff = q_file("ff_monthly.sql")
    ff["month"] = pd.to_datetime(ff["month"])
    panel = panel.merge(ff[["month", "rf"]], on="month", how="left")
    panel["ret_excess"] = panel["ret"] - panel["rf"]
    panel = panel.drop(columns=["rf"])

    print("Pulling Compustat controls (compustat_controls.sql)…")
    t0 = time.time()
    comp = q_file("compustat_controls.sql")
    comp["month"] = pd.to_datetime(comp["month"])
    comp = comp.drop_duplicates(["permno", "month"], keep="first")
    panel = panel.merge(comp[["permno", "month", "bm", "leverage"]],
                        on=["permno", "month"], how="left")
    print(f"  merged bm/leverage in {time.time() - t0:.1f}s")

    print("Pulling daily sufficient statistics (daily_stats.sql)… [heavy]")
    t0 = time.time()
    stats = q_file("daily_stats.sql")
    print(f"  {len(stats):,} (permno, month) groups in {time.time() - t0:.1f}s")

    print("Solving per-stock FF3 regressions (closed form)…")
    t0 = time.time()
    daily = compute_daily_signals(stats)
    print(f"  computed ivol/tvol/coskew/volume/turnover in {time.time() - t0:.1f}s")

    panel = panel.merge(daily, on=["permno", "month"], how="left")

    final_cols = ["permno", "month", "ret", "ret_excess", "me", "ivol", "tvol",
                  "size", "bm", "mom", "volume", "turnover", "leverage",
                  "coskew", "n_obs", "hexcd"]
    final_cols = [c for c in final_cols if c in panel.columns]
    panel = panel[final_cols].sort_values(["permno", "month"]).reset_index(drop=True)

    out_panel.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(out_panel, index=False)
    print(f"  Wrote {len(panel):,} rows x {panel.shape[1]} cols -> {out_panel}")

    summary = summarize(panel)
    out_summary.parent.mkdir(parents=True, exist_ok=True)
    out_summary.write_text(summary)
    print(f"  Wrote summary -> {out_summary}")

    # console quick stats
    print()
    print("Quick stats:")
    print(f"  rows={len(panel):,}  permnos={panel['permno'].nunique():,}  "
          f"months={panel['month'].nunique():,}")
    for sig in ("ivol", "tvol", "size", "bm", "mom", "volume", "turnover",
                "leverage", "coskew", "n_obs"):
        if sig in panel.columns:
            x = panel[sig]
            print(f"  {sig:9s}: mean={x.mean():.5f} median={x.median():.5f} "
                  f"std={x.std():.5f} null={x.isna().sum():,}")


def main() -> None:
    parser = argparse.ArgumentParser(description="AHXZ (2006) IVOL data pipeline")
    parser.add_argument("--build-panel", action="store_true",
                        help="(default action) rebuild data/panel.parquet from ClickHouse")
    parser.add_argument("--table-6", action="store_true",
                        help="run the Table VI analysis (quintile sorts on "
                             "tvol/ivol) on the existing data/panel.parquet; "
                             "writes results/table_6.md and "
                             "results/ivol_quintile_returns.png")
    args = parser.parse_args()
    if args.table_6:
        # Analysis lives in its own module (reads data/panel.parquet +
        # pulls monthly FF factors from ClickHouse via src/sql/ff_monthly.sql).
        from analyze_table6 import run_table6
        run_table6()
    else:
        build_panel()


if __name__ == "__main__":
    main()
