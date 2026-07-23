"""
Replication of Frazzini & Pedersen (2014) "Betting Against Beta" — US equities.
================================================================================
Data pipeline (Stage: build the analysis-ready panel).

Produces  data/panel.parquet  — a monthly cross-section of US common stocks
with Frazzini-Pedersen ex-ante betas, monthly returns, and market equity,
ready for portfolio sorting.

Panel columns
-------------
permno : CRSP permanent security identifier
month  : first-of-month (Date32), the calendar month the row describes
ret    : decimal monthly return realized during `month` (from msf)
beta   : FP shrunk ex-ante beta, estimated using daily data through the LAST
         trading day of the PRIOR month (no look-ahead). beta = 0.6*beta_TS + 0.4.
me     : market equity in $ MILLIONS (abs(prc) * shrout * 1000 / 1e6)
log_me : ln(me)

Beta methodology (FP 2014, §3.1)
--------------------------------
beta_TS = rho * (sigma_i / sigma_m)
  sigma_i, sigma_m : 1-year (252 trading-day) rolling std of 1-day LOG returns
  rho              : 5-year (1260 trading-day) rolling Pearson correlation
                     between the stock's and the market's overlapping 3-day log
                     returns, to control for nonsynchronous trading.
  min data         : >=120 days for volatility, >=750 days for correlation.
  shrinkage        : beta = 0.6 * beta_TS + 0.4 * 1.0  (w=0.6, beta_XS=1).
  market           : CRSP value-weighted index (dsi.vwretd).

Implementation notes
--------------------
* All filtering / PIT universe construction / aggregation is pushed into SQL
  (src/sql/*.sql). Only the rolling beta estimation runs in Python because the
  5-year rolling correlation with overlapping 3-day returns is impractical in a
  single SQL pass over ~68M daily rows.
* The 3-day overlapping log return is built BACKWARD-LOOKING,
  b_t = lr_t + lr_{t-1} + lr_{t-2}, which is the same set of overlapping returns
  as FP's forward form r^{3d}_t = lr_t + lr_{t+1} + lr_{t+2} but indexed by its
  END date, so a correlation window ending at estimation date T uses only data
  through T (no 2-day look-ahead at the window boundary). The correlation value
  is identical; only the date alignment differs.
* Rolling sums are computed with cumulative sums on a dense (dates x permnos)
  matrix, chunked over stocks to bound memory.

CRSP gotchas handled: ret sentinels filtered (ret > -1.0); prc signed -> abs();
shrout in thousands; date columns are ISO strings; month built as Date32 (the
`Date` type clamps pre-1970 dates to the epoch, which would corrupt half the
1926-2012 sample).

Usage
-----
    uv run python src/main.py             # run the full pipeline
    uv run python src/main.py --selftest  # validate beta primitives, no DB
"""
from __future__ import annotations

import gc
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

from utils.env import get_clickhouse_config
from utils.paths import paper_layout

# ────────────────────────────────────────────────────────────────────────────
# Layout & configuration
# ────────────────────────────────────────────────────────────────────────────
SLUG = "betting_against_beta"
LAYOUT = paper_layout(SLUG)
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")
_CFG = get_clickhouse_config()

# Numeric beta parameters. preparations/preprocessing_rules.json stores the
# paper QUOTES (see rule_ids below) rather than a numeric parameter map, so the
# numbers are pinned here exactly as specified in the task / paper §3.1.
VOL_WINDOW = 252        # 1-year rolling std window (trading days)  [var_beta_vol_window]
VOL_MIN = 120           # min days for volatility (6 months)        [var_beta_min_data]
CORR_WINDOW = 1260      # 5-year rolling correlation window         [var_beta_vol_window]
CORR_MIN = 750          # min days for correlation (3 years)        [var_beta_min_data]
SHRINK_W = 0.6          # weight on time-series beta               [var_beta_shrinkage]
SHRINK_XS = 1.0         # cross-sectional shrinkage target          [var_beta_shrinkage]
OVERLAP_DAYS = 3        # overlapping log-return horizon            [var_beta_3day_returns]

# Period. CRSP daily data in this instance start 1925-12-31 (there is NO
# pre-1926 lookback available), so beta for the earliest months is NaN until
# enough history accumulates (~120 trading days for vol, ~750 for corr).
DAILY_START = "1925-12-31"
PANEL_START = "1926-01-01"
PANEL_END = "2012-03-31"

CHUNK_YEARS = 5         # date-range chunks for the daily pull
STOCK_CHUNK = 2500      # permnos per rolling-window batch
STAGE_TABLE = "write_yeye.bab_beta_stage"


# ────────────────────────────────────────────────────────────────────────────
# ClickHouse connection
# ────────────────────────────────────────────────────────────────────────────
def _client() -> Client:
    return Client(
        host=_CFG["host"], port=int(_CFG["port"]),
        user=_CFG["user"], password=_CFG["password"],
        database=_CFG.get("database", "default"),
        settings={"max_execution_time": 900},
    )


def q(sql: str, params: dict | None = None) -> pd.DataFrame:
    """Execute a SQL query (string) and return a DataFrame.

    Trailing ';' is stripped (clickhouse_driver takes a single statement).
    """
    c = _client()
    data, cols = c.execute(
        sql.strip().rstrip(";"), params=params or {}, with_column_types=True
    )
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str, params: dict | None = None) -> pd.DataFrame:
    """Execute a saved SQL file and return a DataFrame."""
    sql = (SQL_DIR / name).read_text()
    return q(sql, params=params)


def _year_chunks(start: str, end: str, step: int = CHUNK_YEARS):
    """Yield (chunk_start, chunk_end) ISO date strings spanning [start, end]."""
    sy, ey = int(start[:4]), int(end[:4])
    y = sy
    while y <= ey:
        cs = start if y == sy else f"{y}-01-01"
        ce = end if (y + step - 1) >= ey else f"{y + step - 1}-12-31"
        yield cs, ce
        y += step


# ────────────────────────────────────────────────────────────────────────────
# Rolling-window primitives (cumulative-sum based, NaN-aware)
# ────────────────────────────────────────────────────────────────────────────
def rolling_sum(A: np.ndarray, W: int) -> np.ndarray:
    """Rolling sum over a trailing window of up to W rows (axis 0).

    Matches ``pandas.rolling(W, min_periods=...)`` window geometry: at row t the
    window is ``[max(0, t-W+1), t]``. For the first W-1 rows the window is
    *truncated* (all data seen so far), so a statistic can be produced as soon
    as the caller's min-periods count is met — this is what lets betas appear
    once a stock has >=750 correlation days / >=120 volatility days, rather than
    waiting for a full 5-year / 1-year window. A may be 1-D (D,) or 2-D (D, K).
    NaN entries in A must already be replaced by 0 where a sum is wanted.
    """
    D = A.shape[0]
    CS = np.empty((D + 1,) + A.shape[1:], dtype=np.float64)
    CS[0] = 0.0
    np.cumsum(A, axis=0, out=CS[1:])
    out = np.empty(A.shape, dtype=np.float64)
    # Truncated windows for the first W-1 rows: out[t] = sum of rows [0..t].
    n_part = min(W - 1, D)
    if n_part > 0:
        out[:n_part] = CS[1:n_part + 1]
    # Full W-row windows from row W-1 on: out[t] = CS[t+1] - CS[t+1-W].
    if D >= W:
        out[W - 1:] = CS[W:] - CS[:-W]
    return out


def rolling_std(A: np.ndarray, W: int, minp: int) -> np.ndarray:
    """Rolling SAMPLE std (ddof=1) of non-NaN values over the last W rows."""
    valid = ~np.isnan(A)
    X = np.where(valid, A, 0.0)
    n = rolling_sum(valid.astype(np.float64), W)
    s1 = rolling_sum(X, W)
    s2 = rolling_sum(X * X, W)
    with np.errstate(invalid="ignore", divide="ignore"):
        var = (s2 - s1 * s1 / np.maximum(n, 1)) / np.maximum(n - 1, 1)
        std = np.sqrt(np.maximum(var, 0.0))
    return np.where(n >= minp, std, np.nan)


def rolling_corr(x: np.ndarray, y: np.ndarray, W: int, minp: int) -> np.ndarray:
    """Rolling Pearson correlation of columns of x (D,K) with y (D,).

    Over the last W rows, counting only rows where BOTH x and y are non-NaN.
    Requires >= minp valid pairs; returns NaN otherwise.
    """
    yb = y[:, None]
    valid = (~np.isnan(x)) & (~np.isnan(yb))
    xz = np.where(valid, x, 0.0)
    yz = np.where(valid, yb, 0.0)
    n = rolling_sum(valid.astype(np.float64), W)
    sx = rolling_sum(xz, W)
    sx2 = rolling_sum(xz * xz, W)
    sxy = rolling_sum(xz * yz, W)
    sy = rolling_sum(yz, W)
    sy2 = rolling_sum(yz * yz, W)
    num = n * sxy - sx * sy
    denx = np.maximum(n * sx2 - sx * sx, 0.0)
    deny = np.maximum(n * sy2 - sy * sy, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        corr = num / np.sqrt(denx * deny)
    return np.where((n >= minp) & (denx > 0) & (deny > 0), corr, np.nan)


def overlap_logret(LR: np.ndarray, k: int = OVERLAP_DAYS) -> np.ndarray:
    """Backward-looking overlapping k-day log return: b_t = sum_{j=0}^{k-1} lr_{t-j}.

    Same overlapping returns as FP's forward form, indexed by the END date so a
    window ending at T never uses data after T. Works for 1-D (D,) or 2-D
    (D, K) input. The first k-1 rows are NaN. NaN propagates: if any of the k
    component days is NaN, b_t is NaN (numpy add propagates NaN).
    """
    out = np.full(LR.shape, np.nan, dtype=np.float64)
    out[k - 1:] = LR[k - 1:]
    for j in range(1, k):
        out[k - 1:] = out[k - 1:] + LR[k - 1 - j:LR.shape[0] - j]
    return out


# ────────────────────────────────────────────────────────────────────────────
# Data loading
# ────────────────────────────────────────────────────────────────────────────
def load_market_calendar() -> tuple[list[str], np.ndarray]:
    """Return (market_dates ISO strings, market 1-day log returns aligned)."""
    c = _client()
    rows = c.execute(
        "SELECT date, vwretd FROM crsp_202601.dsi "
        "WHERE date >= %(s)s AND date <= %(e)s ORDER BY date",
        params={"s": DAILY_START, "e": PANEL_END},
    )
    dates = [r[0] for r in rows]
    vw = np.array([np.nan if r[1] is None else float(r[1]) for r in rows], dtype=np.float64)
    with np.errstate(invalid="ignore", divide="ignore"):
        lr = np.where(vw > -1.0, np.log1p(vw), np.nan)
    return dates, lr


def load_universe_permnos() -> list[int]:
    """Distinct permnos that ever pass the PIT universe filter in the window."""
    sql = """
    SELECT DISTINCT d.permno AS permno
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsenames AS n
        ON d.permno = n.permno AND d.date >= n.namedt AND d.date <= n.nameendt
    WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2, 3)
      AND d.date >= %(s)s AND d.date <= %(e)s
    ORDER BY permno
    SETTINGS join_algorithm = 'partial_merge', max_execution_time = 900
    """
    c = _client()
    rows = c.execute(sql.strip(), params={"s": DAILY_START, "e": PANEL_END})
    return sorted(int(r[0]) for r in rows)


def build_LR_matrix(market_dates, permnos) -> tuple[np.ndarray, dict]:
    """Fill the dense (dates x permnos) daily log-return matrix from SQL chunks.

    Returns (LR, stats). LR is np.float64 with NaN where a stock did not trade.
    Row/col indices come from ``pd.Index.get_indexer`` (hash-based, returns -1
    for a value not in the grid — no pandas deprecation warnings).
    """
    D, K = len(market_dates), len(permnos)
    date_index = pd.Index(market_dates)          # ISO strings, sorted
    permno_index = pd.Index(np.asarray(permnos, dtype=np.int64))
    LR = np.full((D, K), np.nan, dtype=np.float64)
    sql = (SQL_DIR / "universe_daily.sql").read_text().strip().rstrip(";")
    unmapped_dates = 0
    unmapped_permnos = 0
    total_rows = 0
    t0 = time.time()
    for cs, ce in _year_chunks(DAILY_START, PANEL_END):
        tc = time.time()
        c = _client()
        data, _ = c.execute(sql, params={"dstart": cs, "dend": ce}, with_column_types=True)
        n = len(data)
        total_rows += n
        if n == 0:
            continue
        # columnar unpack (fast): permno, date, logret (skip mkt_logret col 3)
        pn = np.fromiter((r[0] for r in data), dtype=np.int64, count=n)
        dt = np.array([r[1] for r in data], dtype=object)
        lv = np.fromiter((np.nan if r[2] is None else r[2] for r in data), dtype=np.float64, count=n)
        rows = date_index.get_indexer(dt)
        cols = permno_index.get_indexer(pn)
        valid = (rows >= 0) & (cols >= 0)
        unmapped_dates += int((rows < 0).sum())
        unmapped_permnos += int((cols < 0).sum())
        LR[rows[valid], cols[valid]] = lv[valid]
        print(f"    chunk {cs}..{ce}: {n:>9,} rows  ({time.time()-tc:4.1f}s)", flush=True)
        del data, pn, dt, lv, rows, cols, valid
        gc.collect()
    print(f"  daily pull done: {total_rows:,} rows, "
          f"{unmapped_dates} unmapped dates / {unmapped_permnos} unmapped permnos "
          f"skipped, {time.time()-t0:.0f}s total", flush=True)
    return LR, {"total_rows": total_rows, "unmapped_dates": unmapped_dates,
                "unmapped_permnos": unmapped_permnos}


# ────────────────────────────────────────────────────────────────────────────
# Beta estimation
# ────────────────────────────────────────────────────────────────────────────
def _month_end_positions(market_dates) -> tuple[np.ndarray, pd.DatetimeIndex]:
    """For each calendar month, the row index of its LAST market date, and the
    first-of-month date of the FOLLOWING month (the month the beta is assigned
    to — no look-ahead)."""
    dt = pd.to_datetime(np.array(market_dates, dtype="datetime64[D]"))
    periods = dt.to_period("M")
    pos = pd.DataFrame({"pos": np.arange(len(dt)), "period": periods})
    last = pos.groupby("period")["pos"].max()
    month_end_pos = last.to_numpy()
    assigned = (last.index + 1).to_timestamp()  # first day of next month
    return month_end_pos, assigned


def compute_betas(LR: np.ndarray, mkt_lr: np.ndarray, market_dates, permnos) -> pd.DataFrame:
    """Compute FP shrunk betas; return long DataFrame [permno, month, beta].

    Betas are sampled at each market month-end and assigned to the FOLLOWING
    month. Only estimable betas (meeting the min-data requirements) are kept.
    """
    D, K = LR.shape
    # market overlapping 3-day log return and market rolling volatility
    y = overlap_logret(mkt_lr, OVERLAP_DAYS)
    std_m = rolling_std(mkt_lr, VOL_WINDOW, VOL_MIN)  # (D,)

    month_end_pos, assigned = _month_end_positions(market_dates)

    beta_chunks = []
    t0 = time.time()
    for c0 in range(0, K, STOCK_CHUNK):
        tc = time.time()
        c1 = min(c0 + STOCK_CHUNK, K)
        chunk_pnos = permnos[c0:c1]
        LRc = LR[:, c0:c1]
        x = overlap_logret(LRc, OVERLAP_DAYS)                 # (D, Kc) 3-day log ret
        corr = rolling_corr(x, y, CORR_WINDOW, CORR_MIN)      # (D, Kc)
        std_i = rolling_std(LRc, VOL_WINDOW, VOL_MIN)         # (D, Kc)
        with np.errstate(invalid="ignore", divide="ignore"):
            beta_ts = corr * (std_i / std_m[:, None])
        beta = SHRINK_W * beta_ts + (1.0 - SHRINK_W) * SHRINK_XS
        # sample at month-ends, assign to the following month; keep only
        # estimable (non-NaN) betas
        beta_me = beta[month_end_pos, :]                       # (n_months, Kc)
        pno_arr = np.array(chunk_pnos, dtype=np.int64)
        assigned_arr = assigned.to_numpy()
        ii, jj = np.nonzero(~np.isnan(beta_me))                # month idx, stock idx
        long = pd.DataFrame({
            "month": assigned_arr[ii],
            "permno": pno_arr[jj],
            "beta": beta_me[ii, jj],
        })
        beta_chunks.append(long)
        print(f"    stock chunk [{c0:>5}:{c1:>5}]: {len(long):>9,} valid betas "
              f"({time.time()-tc:4.1f}s)", flush=True)
        del LRc, x, corr, std_i, beta_ts, beta, beta_me, long, ii, jj
        gc.collect()

    beta_all = pd.concat(beta_chunks, ignore_index=True)
    beta_all = beta_all[["permno", "month", "beta"]]
    beta_all["permno"] = beta_all["permno"].astype(np.int64)
    beta_all["month"] = pd.to_datetime(beta_all["month"])
    print(f"  beta done: {len(beta_all):,} (permno, month) estimates, "
          f"{time.time()-t0:.0f}s total", flush=True)
    return beta_all


# ────────────────────────────────────────────────────────────────────────────
# Staging + final panel assembly (SQL)
# ────────────────────────────────────────────────────────────────────────────
def stage_betas(beta_all: pd.DataFrame) -> None:
    """Load computed betas into the ClickHouse staging table used by panel.sql."""
    c = _client()
    c.execute(f"DROP TABLE IF EXISTS {STAGE_TABLE}")
    c.execute(
        f"CREATE TABLE {STAGE_TABLE} ("
        "permno Int32, month Date32, beta Float64"
        ") ENGINE = MergeTree ORDER BY (month, permno)"
    )
    recs = list(zip(
        beta_all["permno"].astype(np.int32).tolist(),
        beta_all["month"].dt.date.tolist(),
        beta_all["beta"].astype(np.float64).tolist(),
    ))
    c.execute(f"INSERT INTO {STAGE_TABLE} (permno, month, beta) VALUES", recs)
    n = c.execute(f"SELECT count() FROM {STAGE_TABLE}")[0][0]
    print(f"  staged {n:,} betas into {STAGE_TABLE}", flush=True)


def drop_stage() -> None:
    try:
        _client().execute(f"DROP TABLE IF EXISTS {STAGE_TABLE}")
    except Exception:
        pass


# ────────────────────────────────────────────────────────────────────────────
# Reporting
# ────────────────────────────────────────────────────────────────────────────
def summarize(panel: pd.DataFrame) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("PANEL SUMMARY  (data/panel.parquet)")
    lines.append("=" * 70)
    lines.append(f"Dimensions      : {panel.shape[0]:,} rows x {panel.shape[1]} columns")
    lines.append(f"Columns         : {list(panel.columns)}")
    lines.append(f"Unique months   : {panel['month'].nunique()}")
    lines.append(f"Unique permnos  : {panel['permno'].nunique()}")
    lines.append(f"Date range      : {panel['month'].min().date()} .. {panel['month'].max().date()}")
    obs = panel.groupby("month").size()
    lines.append(f"Avg obs / month : {obs.mean():,.1f}  (min {obs.min()}, max {obs.max()})")
    nbeta = int(panel["beta"].notna().sum())
    lines.append(f"Non-null beta   : {nbeta:,} / {panel.shape[0]:,} "
                 f"({100*nbeta/panel.shape[0]:.1f}%)")

    b = panel["beta"].dropna()
    lines.append("-" * 70)
    lines.append("BETA (shrunk) distribution — non-null:")
    lines.append(f"  mean   = {b.mean():.4f}    median = {b.median():.4f}    std = {b.std():.4f}")
    lines.append(f"  min    = {b.min():.4f}    max    = {b.max():.4f}")
    lines.append(f"  p5     = {b.quantile(0.05):.4f}    p95    = {b.quantile(0.95):.4f}")

    m = panel["me"].dropna()
    lines.append("-" * 70)
    lines.append("ME ($ millions) distribution — non-null:")
    lines.append(f"  mean   = {m.mean():,.2f}    median = {m.median():,.2f}")
    lines.append(f"  p5     = {m.quantile(0.05):,.2f}    p95    = {m.quantile(0.95):,.2f}")
    lines.append("=" * 70)
    return "\n".join(lines)


# ────────────────────────────────────────────────────────────────────────────
# Self-test (no DB): validate the rolling primitives against pandas
# ────────────────────────────────────────────────────────────────────────────
def selftest() -> None:
    rng = np.random.default_rng(0)
    D = 1400
    mkt = rng.normal(0.0005, 0.01, D)
    stocks = np.column_stack([mkt, 2 * mkt, -mkt, mkt + rng.normal(0, 0.01, D)])
    # introduce some missing days in stock 3 to exercise NaN handling
    stocks[50:60, 3] = np.nan
    x = overlap_logret(stocks, OVERLAP_DAYS)
    y = overlap_logret(mkt, OVERLAP_DAYS)
    corr = rolling_corr(x, y, CORR_WINDOW, CORR_MIN)
    std_i = rolling_std(stocks, VOL_WINDOW, VOL_MIN)

    # FULL-SERIES equivalence vs pandas rolling(window, min_periods) — this
    # validates both the truncated early windows and the steady-state windows.
    for k in range(stocks.shape[1]):
        pcorr = (pd.Series(x[:, k]).rolling(CORR_WINDOW, min_periods=CORR_MIN)
                 .corr(pd.Series(y))).to_numpy()
        pstd = (pd.Series(stocks[:, k]).rolling(VOL_WINDOW, min_periods=VOL_MIN)
                .std(ddof=1)).to_numpy()
        mask = ~np.isnan(pcorr)
        assert np.allclose(corr[:, k][mask], pcorr[mask], atol=1e-9), ("corr", k)
        # NaN positions must match too (min-periods cutoffs)
        assert np.array_equal(np.isnan(corr[:, k]), np.isnan(pcorr)), ("corr NaN", k)
        mask2 = ~np.isnan(pstd)
        assert np.allclose(std_i[:, k][mask2], pstd[mask2], atol=1e-9), ("std", k)
        assert np.array_equal(np.isnan(std_i[:, k]), np.isnan(pstd)), ("std NaN", k)

    t = D - 1
    for k, expected in [(0, 1.0), (1, 1.0), (2, -1.0)]:
        assert abs(corr[t, k] - expected) < 1e-6, (k, corr[t, k], expected)
    std_m = rolling_std(mkt, VOL_WINDOW, VOL_MIN)
    beta_ts = corr[t, :] * std_i[t, :] / std_m[t]
    beta = SHRINK_W * beta_ts + (1 - SHRINK_W) * SHRINK_XS
    assert abs(beta[0] - 1.0) < 1e-6 and abs(beta[1] - 1.6) < 1e-6 \
        and abs(beta[2] - (-0.2)) < 1e-6, beta[:3]
    # confirm truncated-window betas exist before a full 5y window (min-periods)
    first_valid = np.argmax(~np.isnan(corr[:, 0]))
    assert first_valid < CORR_WINDOW, first_valid
    print(f"selftest PASSED: rolling corr/std match pandas rolling(W,min_periods) "
          f"on the FULL series (incl. truncated early windows); first valid corr at "
          f"row {first_valid} (< {CORR_WINDOW}); shrunk betas = {np.round(beta[:3], 4)}")


# ────────────────────────────────────────────────────────────────────────────
# main
# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    t_start = time.time()
    print("=" * 70)
    print("Frazzini-Pedersen (2014) 'Betting Against Beta' — US panel pipeline")
    print("=" * 70)

    print("[1/6] market calendar + market log returns ...")
    market_dates, mkt_lr = load_market_calendar()
    print(f"      {len(market_dates)} market dates "
          f"({market_dates[0]} .. {market_dates[-1]})")

    print("[2/6] universe permnos ...")
    permnos = load_universe_permnos()
    print(f"      {len(permnos)} unique universe permnos")

    print("[3/6] build daily log-return matrix (chunked SQL pull) ...")
    LR, pull_stats = build_LR_matrix(market_dates, permnos)
    print(f"      LR matrix shape = {LR.shape}  "
          f"({LR.size * 8 / 1e9:.2f} GB)")

    print("[4/6] estimate FP betas (rolling vol x rolling corr + shrinkage) ...")
    beta_all = compute_betas(LR, mkt_lr, market_dates, permnos)
    del LR, mkt_lr
    gc.collect()

    print("[5/6] stage betas + assemble final panel (panel.sql) ...")
    stage_betas(beta_all)
    panel = q_file("panel.sql", params={"mstart": PANEL_START, "mend": PANEL_END})
    drop_stage()
    panel["month"] = pd.to_datetime(panel["month"])
    panel = panel.sort_values(["permno", "month"]).reset_index(drop=True)
    panel = panel[["permno", "month", "ret", "beta", "me", "log_me"]]

    out = LAYOUT.data_path("panel.parquet")
    panel.to_parquet(out, index=False)
    print(f"      wrote {out}  ({panel.shape[0]:,} rows)")

    print("[6/6] summary ...")
    report = summarize(panel)
    print(report)
    LAYOUT.data_path("pipeline_summary.txt").write_text(
        report + f"\n\ntotal runtime: {time.time()-t_start:.0f}s\n"
        + f"pull_stats: {pull_stats}\n"
    )
    print(f"total runtime: {time.time()-t_start:.0f}s")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        main()
