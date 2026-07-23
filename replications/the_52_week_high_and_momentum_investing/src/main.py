"""
Replication of George & Hwang (2004), "The 52-Week High and Momentum
Investing", Journal of Finance.

Task: build the analysis-ready monthly panel (Tables I-VII).

One row per (permno, month) for all CRSP common stocks (point-in-time
shrcd 10/11, all exchanges), months 1958-01 .. 2002-12, with all signals
computed at formation month f (no holding-period timing baked in):
  jt_sig(f)    6-month cumulative own return, months f-5..f
  wh_sig_hi(f) |prc(f)| / max(askhi) over f-11..f  (52-week high, monthly high)
  wh_sig_cl(f) |prc(f)| / max(|prc|) over f-11..f  (monthly-close variant)
  wh_sig_dc(f) |prc(f)| / max(max_daily_close) over f-11..f  (daily-close
               variant: max_daily_close = max of dsf daily |prc| per calendar
               month; the literal "highest price achieved" reading of L122;
               always <= 1 because the month-end close is one of the daily
               closes in its own month, so the window max >= |prc(f)|)
  wh_sig_hi_abs(f) |prc(f)| / max(|askhi|) over f-11..f  (abs-askhi adjudication
               variant for the Table I confirmation step; abs() removes the
               CRSP quote-sign artifact, keeps the askhi price series)
  mg_sig(f)    6-month cumulative value-weighted industry return (20 MG
               industries), months f-5..f
  g_gh(f)      GH (2002) embedded capital gain, 60-month turnover-weighted
               reference price (variant A: strict 60 consecutive non-null
               months of P and V; assumption A11)
  g_gh_b(f)    GH embedded gain, variant B (audit1.md [M2] adjudication):
               same weights w_s = V(f-s) * prod_{r=f-s+1..f}(1 - V(r)) and
               reference price R_f = sum(w_s P(f-s)) / sum(w_s), but summed
               only over USABLE lags s = 1..min(60, L) — L = length of the
               run of consecutive non-null V ending at f — with P(f-s)
               non-null (a missing price skips that lag instead of zeroing
               the whole signal); requires >= 24 usable lags, else NaN.
               Additive column: g_gh (variant A) is untouched.
  wh_lo_sig(f) |prc(f)| / min(min_daily_close) over f-11..f (52-week-LOW
               signal, audit1.md [M4] prep; min_daily_close = min of dsf
               daily |prc| per calendar month; always >= 1 because the
               month-end close is one of the daily closes in its own month,
               so the window min <= |prc(f)|)

Rolling signals are computed on the FULL msf history per permno (reindexed
to the full calendar month grid so gaps are missing months); the final
panel is then filtered to universe (PIT shrcd 10/11) rows only.

ret_dl (delisting-adjusted return, added after ALL signal computation):
for a stock-month matching an msedelist delisting event with valid dlret
(non-null, > -1), ret_dl = (1 + ret) * (1 + dlret) - 1 (or ret_dl = dlret
on the rare added rows where the msf row is absent in the delisting month);
otherwise ret_dl = ret. No Shumway/BMP imputation. Signals, industry
returns, and rankings stay on the ORIGINAL ret — ret_dl is for portfolio /
regression DEPENDENT variables only (experiment: src/delisting_experiment.py).

Sources: crsp_202601.msf + crsp_202601.dsenames + crsp_202601.dsf (for the
daily-close 52-week-high variant wh_sig_dc and the 52-week-low signal
wh_lo_sig; SQL in src/sql/).
Units verified: shrout in thousands of shares, vol in hundreds of shares.
"""
from __future__ import annotations

import json
import time

import numpy as np
import pandas as pd
from clickhouse_driver import Client

from utils.env import get_clickhouse_config
from utils.paths import paper_layout

# --- configuration -------------------------------------------------------

LAYOUT = paper_layout("the_52_week_high_and_momentum_investing")
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")

# Load the prep contract (paper-derived rules with verbatim quotes). The
# panel methodology constants below implement these rules; the JSON has no
# free numeric parameters (it is a list of quoted rules), so the operative
# values live here with rule-id references.
RULES = json.loads(LAYOUT.preparations_path("preprocessing_rules.json").read_text())
RULE_IDS = {r["rule_id"] for r in RULES}
for _required in ("universe_all_crsp", "var_mg_20_industries",
                  "var_mg_signal", "var_jt_past_return", "var_52wh_measure",
                  "var_gh_embedded_gain", "var_gh_turnover"):
    assert _required in RULE_IDS, f"preprocessing_rules.json missing {_required}"

SQL_START = "1957-12-01"   # Dec-1957 = lagged mcap for Jan-1958 ind_ret (in SQL WHERE)
SQL_END = "2002-12-31"     # (in SQL WHERE)
GRID_START = "1958-01-31"  # analysis grid: 1958-01 .. 2002-12 (month-ends)
GRID_END = "2002-12-31"
SIGNAL_WINDOW_START = "1963-01-31"  # Table-eligible formation window
SIGNAL_WINDOW_END = "2001-11-30"    # (1963-01 .. 2001-11)

GH_LAGS = 60       # GH reference price: 60-month turnover-weighted window
GH_B_MIN_USABLE = 24   # g_gh variant B (audit M2): minimum USABLE lags
                       # (available V-run lags with non-null P(f-s)) for the
                       # renormalized reference price; else the signal is NaN
JT_WINDOW = 6      # 6-month cumulative return formation (var_jt_past_return)
WH_WINDOW = 12     # 12-month high window (var_52wh_measure)

# 20 MG-style industries from 2-digit SIC (siccd // 100).
# MG (1999) Table I mapping (per Replicator: retrieved from the actual MG
# table; rule var_mg_20_industries). Explicit ranges first, default 20.
MG_INDUSTRY_NAMES = {
    1: "Mining", 2: "Food", 3: "Apparel", 4: "Paper", 5: "Chemical",
    6: "Petroleum", 7: "Construction", 8: "Prim. Metals", 9: "Fab. Metals",
    10: "Machinery", 11: "Electrical Eq.", 12: "Transport Eq.",
    13: "Manufacturing", 14: "Railroads", 15: "Other Transport.",
    16: "Utilities", 17: "Dept. Stores", 18: "Retail", 19: "Financial",
    20: "Other",
}


def _mg_lookup() -> np.ndarray:
    """LUT: 2-digit SIC code (0..99) -> MG industry 1..20, default 20."""
    lut = np.full(100, 20, dtype=np.int16)
    explicit = {
        1: range(10, 15),            # 10-14 Mining
        2: range(20, 21),            # 20    Food
        3: range(22, 24),            # 22-23 Apparel
        4: range(26, 27),            # 26    Paper
        5: range(28, 29),            # 28    Chemical
        6: range(29, 30),            # 29    Petroleum
        7: range(32, 33),            # 32    Construction (Stone/Clay/Glass)
        8: range(33, 34),            # 33    Primary Metals
        9: range(34, 35),            # 34    Fabricated Metals
        10: range(35, 36),           # 35    Machinery
        11: range(36, 37),           # 36    Electrical Equipment
        12: range(37, 38),           # 37    Transport Equipment
        13: range(38, 40),           # 38-39 Manufacturing
        14: range(40, 41),           # 40    Railroads
        15: range(41, 48),           # 41-47 Other Transportation
        16: range(49, 50),           # 49    Utilities
        17: range(53, 54),           # 53    Department Stores
        18: (*range(50, 53), *range(54, 60)),  # 50-52, 54-59 Retail
        19: range(60, 70),           # 60-69 Financial
    }
    for ind, codes in explicit.items():
        for c in codes:
            lut[c] = ind
    return lut  # everything else (00-09, 15-19, 21, 24-25, 27, 30-31, 48, 70-99) -> 20


MG_LUT = _mg_lookup()

PANEL_COLUMNS = [
    "permno", "month", "ret", "ret_dl", "abs_prc", "mcap", "vol", "shrout",
    "sic2", "industry", "jt_sig", "wh_sig_hi", "wh_sig_cl", "wh_sig_dc",
    "wh_lo_sig", "wh_sig_hi_abs", "mg_sig", "g_gh", "g_gh_b", "in_universe",
]

# Delisting-return experiment (see delisting_adjust below): "performance"
# delisting codes for the missing-dlret log (task definition: 5xx = delisted
# by the exchange; 580/584 = failure to meet listing requirements, reported
# separately).
PERF_DLRANGE = (500, 599)


# --- ClickHouse connection -------------------------------------------------

_CFG = get_clickhouse_config()


def _client() -> Client:
    return Client(
        host=_CFG["host"], port=int(_CFG["port"]),
        user=_CFG["user"], password=_CFG["password"],
        settings={"max_execution_time": 600},
    )


def q(sql: str) -> pd.DataFrame:
    """Execute a SQL query and return a DataFrame."""
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    """Execute a saved SQL file and return a DataFrame."""
    return q((SQL_DIR / name).read_text())


# --- data loading -----------------------------------------------------------

def load_msf() -> pd.DataFrame:
    """Filtered monthly CRSP rows (src/sql/msf_monthly.sql). The calendar
    month-end key is derived here (msf dates are last *trading* days, e.g.
    Feb 26/27; MonthEnd(0) snaps them to the calendar month-end)."""
    df = q_file("msf_monthly.sql")
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"] + pd.offsets.MonthEnd(0)
    df["permno"] = df["permno"].astype("int64")
    assert df["permno"].notna().all(), "NULL permno in msf"
    dup = df.duplicated(subset=["permno", "month"]).sum()
    assert dup == 0, f"{dup} duplicate (permno, month) rows in msf"
    return df.sort_values(["permno", "month"]).reset_index(drop=True)


def load_dsenames() -> pd.DataFrame:
    """PIT common-stock name records (src/sql/dsenames_common.sql)."""
    df = q_file("dsenames_common.sql")
    for col in ("namedt", "nameendt"):
        df[col] = pd.to_datetime(df[col])
    df["permno"] = df["permno"].astype("int64")
    assert df["nameendt"].notna().all(), "NULL nameendt present (unexpected)"
    return df.sort_values(["permno", "namedt"]).reset_index(drop=True)


def load_dsf_maxclose() -> pd.DataFrame:
    """Monthly max of DAILY |prc| per permno (src/sql/dsf_monthly_maxclose.sql).
    The SQL returns ym = 'YYYY-MM'; snap it to the calendar month-end here (same
    MonthEnd(0) convention as msf) so it aligns with the analysis grid."""
    df = q_file("dsf_monthly_maxclose.sql")
    df = df[df["permno"].notna()].copy()
    df["permno"] = df["permno"].astype("int64")
    df["month"] = pd.to_datetime(df["ym"] + "-01") + pd.offsets.MonthEnd(0)
    df["max_daily_close"] = df["max_daily_close"].astype("float64")
    dup = df.duplicated(subset=["permno", "month"]).sum()
    assert dup == 0, f"{dup} duplicate (permno, month) rows in dsf maxclose"
    return df[["permno", "month", "max_daily_close"]]


def load_dsf_minclose() -> pd.DataFrame:
    """Monthly MIN of DAILY |prc| per permno (src/sql/dsf_monthly_minclose.sql),
    the denominator series of the 52-week-LOW signal wh_lo_sig (audit M4 prep).
    Exact mirror of load_dsf_maxclose: the SQL returns ym = 'YYYY-MM'; snap it
    to the calendar month-end here (same MonthEnd(0) convention as msf) so it
    aligns with the analysis grid."""
    df = q_file("dsf_monthly_minclose.sql")
    df = df[df["permno"].notna()].copy()
    df["permno"] = df["permno"].astype("int64")
    df["month"] = pd.to_datetime(df["ym"] + "-01") + pd.offsets.MonthEnd(0)
    df["min_daily_close"] = df["min_daily_close"].astype("float64")
    dup = df.duplicated(subset=["permno", "month"]).sum()
    assert dup == 0, f"{dup} duplicate (permno, month) rows in dsf minclose"
    return df[["permno", "month", "min_daily_close"]]


def load_msedelist() -> pd.DataFrame:
    """Delisting events (src/sql/msedelist.sql): permno, dlstdt, dlstcd, dlret,
    dlretx with dlstdt in 1958-01-01 .. 2003-12-31. The month key = calendar
    month-end of dlstdt (same MonthEnd(0) convention as msf), so a delisting
    maps to the stock's final holding month. Verified: no NULL permno/dlstdt
    in the window, one row per permno, dlret missing = NULL only (no negative
    sentinels in this vintage)."""
    df = q_file("msedelist.sql")
    df = df[df["permno"].notna() & df["dlstdt"].notna()].copy()
    df["permno"] = df["permno"].astype("int64")
    df["dlstdt"] = pd.to_datetime(df["dlstdt"])
    df["month"] = df["dlstdt"] + pd.offsets.MonthEnd(0)
    df["dlstcd"] = df["dlstcd"].astype("float64")
    df["dlret"] = df["dlret"].astype("float64")
    df["dlretx"] = df["dlretx"].astype("float64")
    dup = df.duplicated(subset=["permno", "month"]).sum()
    assert dup == 0, f"{dup} duplicate (permno, month) rows in msedelist"
    return df.sort_values(["permno", "month"]).reset_index(drop=True)


# --- universe flag, SIC, industry -------------------------------------------

def attach_universe_and_sic(msf: pd.DataFrame, dsn: pd.DataFrame) -> pd.DataFrame:
    """PIT universe flag + point-in-time SIC per stock-month.

    A stock-month is in the universe iff some dsenames record with
    shrcd IN (10,11) covers the month-end (namedt <= month <= nameendt).
    Verified: dsenames validity intervals never overlap within a permno and
    nameendt is never NULL in this vintage, so a backward merge_asof on
    namedt + coverage check is exactly the "exists a covering record" test.
    """
    dsn_use = dsn[["permno", "namedt", "nameendt", "siccd"]].sort_values("namedt")
    # merge_asof needs the asof key globally sorted (within-by sorting is
    # not enough), so sort on the key, merge, then restore permno order.
    merged = pd.merge_asof(
        msf.sort_values("month"), dsn_use,
        left_on="month", right_on="namedt",
        by="permno", direction="backward", allow_exact_matches=True,
    )
    merged = merged.sort_values(["permno", "month"]).reset_index(drop=True)
    merged["in_universe"] = merged["nameendt"].notna() & (
        merged["month"] <= merged["nameendt"]
    )
    # SIC: dsenames.siccd (PIT), fallback msf.hsiccd; 4-digit -> 2-digit.
    sic = merged["siccd"].where(merged["siccd"].notna(), merged["hsiccd"])
    sic2 = np.where(
        sic.notna() & (sic >= 0) & (sic < 10000),
        np.floor(sic.fillna(0) / 100),
        np.nan,
    )
    merged["sic2"] = sic2.astype("float64")
    idx = np.where(np.isnan(sic2), 0, sic2).astype(int)
    industry = MG_LUT[idx].astype("float64")
    industry[np.isnan(sic2)] = np.nan
    merged["industry"] = industry
    return merged.drop(columns=["namedt", "nameendt", "siccd"])


def derive_fields(df: pd.DataFrame) -> pd.DataFrame:
    """abs_prc, mcap (dollars), turnover V (capped at 1). Units verified:
    shrout in THOUSANDS of shares, vol in HUNDREDS of shares."""
    df["abs_prc"] = df["prc"].abs()
    df["mcap"] = df["abs_prc"] * df["shrout"] * 1000.0
    raw = df["vol"] * 100.0 / (df["shrout"] * 1000.0)
    df["turnover_raw"] = raw  # pre-cap, for reporting
    df["turnover"] = np.minimum(raw, 1.0)  # LEAST(1, raw); NaN propagates
    return df


# --- delisting-adjusted returns (dependent-variable column only) -------------

def _universe_coverage(cands: pd.DataFrame, dsn: pd.DataFrame) -> pd.DataFrame:
    """Universe membership + PIT SIC for candidate (permno, month) rows, using
    the EXACT rule of attach_universe_and_sic: a dsenames record with
    shrcd IN (10,11) covering the month-end (namedt <= month <= nameendt)."""
    dsn_use = dsn[["permno", "namedt", "nameendt", "siccd"]].sort_values("namedt")
    merged = pd.merge_asof(
        cands.sort_values("month"), dsn_use,
        left_on="month", right_on="namedt",
        by="permno", direction="backward", allow_exact_matches=True,
    )
    merged["in_universe"] = merged["nameendt"].notna() & (
        merged["month"] <= merged["nameendt"]
    )
    return merged


def delisting_adjust(panel: pd.DataFrame, dl: pd.DataFrame,
                     dsn: pd.DataFrame, grid: pd.DatetimeIndex,
                     msf_long: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Add ret_dl = delisting-adjusted holding-period return to the panel.

    ONE change vs `ret`: the final month of a delisted stock folds in the
    delisting return. Rule (task spec, no Shumway/BMP imputation):
      - Event (permno, month) with VALID dlret (non-null and > -1; this also
        excludes CRSP negative sentinels — none in this vintage — and
        worthless-stock dlret = -1.0, left as-is):
          * panel row exists for (permno, month):
                ret_dl = (1 + ret) * (1 + dlret) - 1
          * NO panel row at the delisting month BUT the stock was an active
            holding (panel row in the PRIOR month): ADD a row with ret = NaN
            (so the `ret` variant stays bit-exactly unchanged — the row is
            inert under `ret`) and
                ret_dl = (1 + ret_msf) * (1 + dlret) - 1  if an msf row
                         exists for that month, else ret_dl = dlret
            (the msf row may be absent in the delisting month). Why most
            delisting months have no panel row in this vintage: dsenames
            nameendt = dlstdt < month-end, so the universe coverage test
            fails at the delisting month even though the stock trades
            through dlstdt (verified: 13,221 of 13,908 added rows DO have an
            msf return at the delisting month; 687 do not). Requiring the
            prior-month panel row restricts additions to stocks that were
            plausibly in a portfolio formed shortly before the delisting.
            Signals on added rows are NaN (no rankable price/return at f).
      - dlret NULL (or <= -1): ret_dl = ret (left as-is). NO new rows.

    Signals (jt_sig, mg_sig, wh_*, g_gh), industry returns, and rankings are
    NOT touched: ret_dl adjusts portfolio/regression DEPENDENT variables only.
    `ret` itself is never modified.
    """
    grid_vals = grid.to_numpy()
    ev = dl[dl["month"].isin(grid_vals)].copy()
    n_in_grid = len(ev)
    n_out_grid = len(dl) - n_in_grid  # e.g. dlstdt in 2003 -> month past grid
    ev["valid_dlret"] = ev["dlret"].notna() & (ev["dlret"] > -1.0)

    # defensive dedup (verified none in this vintage): per (permno, month)
    # prefer a valid dlret, then the latest dlstdt.
    ev = ev.sort_values(["permno", "month", "valid_dlret", "dlstdt"],
                        ascending=[True, True, False, False])
    ev = ev.drop_duplicates(subset=["permno", "month"], keep="first")

    panel_keys = set(zip(panel["permno"].to_numpy(),
                         panel["month"].to_numpy()))
    in_panel = np.fromiter(
        ((p, m) in panel_keys for p, m in zip(ev["permno"], ev["month"])),
        dtype=bool, count=len(ev),
    )

    # --- adjust existing rows -------------------------------------------------
    adj = ev.loc[in_panel & ev["valid_dlret"].to_numpy(),
                 ["permno", "month", "dlret"]]
    panel = panel.merge(adj, on=["permno", "month"], how="left")
    dlret_m = panel["dlret"].to_numpy(dtype="float64")
    ret_v = panel["ret"].to_numpy(dtype="float64")
    panel["ret_dl"] = np.where(
        np.isfinite(dlret_m),
        (1.0 + ret_v) * (1.0 + dlret_m) - 1.0,
        ret_v,
    )
    panel = panel.drop(columns=["dlret"])
    n_adj_existing = int(len(adj))

    # --- new rows: valid dlret, no panel row at m, active holding at m-1 ------
    cands = ev.loc[(~in_panel) & ev["valid_dlret"].to_numpy(),
                   ["permno", "month", "dlret"]].copy()
    n_new = 0
    n_new_with_msf = 0
    n_skipped_not_holding = 0
    if len(cands):
        cands["prev"] = cands["month"] - pd.offsets.MonthEnd(1)
        held = np.fromiter(
            ((p, pm) in panel_keys for p, pm in zip(cands["permno"], cands["prev"])),
            dtype=bool, count=len(cands),
        )
        n_skipped_not_holding = int((~held).sum())
        cands = cands.loc[held, ["permno", "month", "dlret"]]
        # msf return at the delisting month (universe flag irrelevant here:
        # msf_long holds ALL msf rows incl. universe-excluded stock-months)
        msf_lk = msf_long[["permno", "month", "ret"]].rename(
            columns={"ret": "ret_msf"})
        cands = cands.merge(msf_lk, on=["permno", "month"], how="left")
        rm = cands["ret_msf"].to_numpy(dtype="float64")
        dlr = cands["dlret"].to_numpy(dtype="float64")
        ret_dl_new = np.where(np.isfinite(rm),
                              (1.0 + rm) * (1.0 + dlr) - 1.0, dlr)
        n_new_with_msf = int(np.isfinite(rm).sum())
        # PIT SIC from the last covering dsenames record (coverage at m fails
        # by the nameendt = dlstdt convention; the backward merge still gives
        # the final record's siccd)
        cov = _universe_coverage(cands, dsn)
        sic = cov["siccd"].astype("float64")
        sic2 = np.where(
            sic.notna() & (sic >= 0) & (sic < 10000),
            np.floor(sic.fillna(0) / 100),
            np.nan,
        )
        idx = np.where(np.isnan(sic2), 0, sic2).astype(int)
        industry = MG_LUT[idx].astype("float64")
        industry[np.isnan(sic2)] = np.nan
        n = len(cov)
        new = pd.DataFrame({
            "permno": cov["permno"].astype("int64").to_numpy(),
            "month": cov["month"].to_numpy(),
            "ret": np.full(n, np.nan),
            "ret_dl": ret_dl_new,
            "abs_prc": np.full(n, np.nan),
            "mcap": np.full(n, np.nan),
            "vol": np.full(n, np.nan),
            "shrout": np.full(n, np.nan),
            "sic2": sic2,
            "industry": industry,
            "jt_sig": np.full(n, np.nan),
            "wh_sig_hi": np.full(n, np.nan),
            "wh_sig_cl": np.full(n, np.nan),
            "wh_sig_dc": np.full(n, np.nan),
            "wh_lo_sig": np.full(n, np.nan),
            "wh_sig_hi_abs": np.full(n, np.nan),
            "mg_sig": np.full(n, np.nan),
            "g_gh": np.full(n, np.nan),
            "g_gh_b": np.full(n, np.nan),
            "in_universe": np.ones(n, dtype=bool),
        })
        panel = pd.concat([panel, new], ignore_index=True)
        n_new = int(n)

    stats = {
        "dl_pulled": int(len(dl)),
        "dl_in_grid": n_in_grid,
        "dl_outside_grid": n_out_grid,
        "dl_valid": int(ev["valid_dlret"].sum()),
        "dl_null": int(ev["dlret"].isna().sum()),
        "dl_worthless": int((ev["dlret"] == -1.0).sum()),
        "dl_adj_existing": n_adj_existing,
        "dl_new_rows": n_new,
        "dl_new_with_msf": n_new_with_msf,
        "dl_new_msf_absent": n_new - n_new_with_msf,
        "dl_skipped_not_holding": n_skipped_not_holding,
        "dl_events": ev,  # in-grid event frame (for decade/mean stats)
    }
    return panel, stats


def delisting_event_stats(ev: pd.DataFrame) -> dict:
    """Summary stats over the in-grid delisting event frame (from
    delisting_adjust's stats['dl_events'], or recomputed by the experiment
    driver): dlret coverage, performance-delist (dlstcd 500-599) missing
    counts by decade, 580/584 detail, mean dlret."""
    valid = ev["valid_dlret"] if "valid_dlret" in ev.columns else (
        ev["dlret"].notna() & (ev["dlret"] > -1.0))
    perf = (ev["dlstcd"] >= PERF_DLRANGE[0]) & (ev["dlstcd"] <= PERF_DLRANGE[1])
    perf_ev = ev[perf]
    perf_valid = valid[perf]
    perf_null = ev["dlret"].isna()[perf]
    perf_worth = (ev["dlret"] == -1.0)[perf]

    by_decade = {}
    if len(perf_ev):
        dec = (perf_ev["month"].dt.year // 10 * 10)
        for d, g in perf_ev.groupby(dec):
            gv = perf_valid.loc[g.index]
            by_decade[int(d)] = {
                "n": int(len(g)),
                "missing": int(perf_null.loc[g.index].sum()),
                "worthless": int(perf_worth.loc[g.index].sum()),
                "valid": int(gv.sum()),
            }

    def _code_stats(code: int) -> dict:
        m = ev["dlstcd"] == code
        v = valid[m]
        return {
            "n": int(m.sum()),
            "missing": int(ev["dlret"].isna()[m].sum()),
            "valid": int(v.sum()),
            "mean_dlret": float(ev.loc[m, "dlret"][v[m]].mean()) if v.sum() else np.nan,
        }

    valid_dlret = ev.loc[valid, "dlret"]
    perf_v = perf_ev.loc[perf_valid, "dlret"]
    return {
        "n_events": int(len(ev)),
        "n_valid": int(valid.sum()),
        "frac_valid": float(valid.mean()) if len(ev) else np.nan,
        "n_null": int(ev["dlret"].isna().sum()),
        "n_worthless": int((ev["dlret"] == -1.0).sum()),
        "mean_dlret_valid": float(valid_dlret.mean()) if len(valid_dlret) else np.nan,
        "n_perf": int(perf.sum()),
        "perf_missing": int(perf_null.sum()),
        "perf_worthless": int(perf_worth.sum()),
        "perf_frac_valid": float(perf_valid.mean()) if perf.sum() else np.nan,
        "mean_dlret_perf": float(perf_v.mean()) if len(perf_v) else np.nan,
        "median_dlret_perf": float(perf_v.median()) if len(perf_v) else np.nan,
        "perf_by_decade": by_decade,
        "code_580": _code_stats(580),
        "code_584": _code_stats(584),
    }


# --- wide matrices on the month grid -----------------------------------------

def to_wide(df: pd.DataFrame, col: str, grid: pd.DatetimeIndex) -> pd.DataFrame:
    """Pivot one variable to a permno x month frame, reindexed to `grid`
    (months with no msf row -> NaN = missing month for rolling windows)."""
    w = df.pivot(index="permno", columns="month", values=col)
    return w.reindex(columns=grid)


def roll_sum_log(values: np.ndarray, window: int) -> np.ndarray:
    """Rolling prod(1+x)-1 over `window` months; NaN unless ALL `window`
    months present (min_periods=window counts non-NaN obs). A -1 month
    (log1p = -inf) zeroes the product -> signal -1."""
    with np.errstate(divide="ignore", invalid="ignore"):
        lt = np.log1p(values)
    out = pd.DataFrame(lt).T.rolling(window, min_periods=window).sum().T.values
    return np.exp(out) - 1.0


# --- signals -----------------------------------------------------------------

def jt_signal(ret_w: pd.DataFrame) -> np.ndarray:
    """jt_sig(f) = prod(1+ret) over f-5..f minus 1; 6 consecutive months."""
    return roll_sum_log(ret_w.values, JT_WINDOW)


def wh_signals(abs_prc_w: pd.DataFrame, askhi_w: pd.DataFrame):
    """wh_sig_hi(f) = |prc(f)| / max(askhi) over f-11..f (askhi gaps ignored
    in the max; NaN if no askhi in window or no |prc(f)|).
    wh_sig_cl(f) = |prc(f)| / max(|prc|) over f-11..f (always <= 1).
    wh_sig_hi_abs(f) = |prc(f)| / max(|askhi|) over f-11..f — adjudication
    variant: rolling max on ABS(askhi) instead of signed askhi (removes the
    quote-sign artifact, keeps the askhi price series; also <= 1).
    Inf ratios (askhi max == 0, a CRSP missing marker) are set to NaN;
    negative ratios (all-negative askhi windows, i.e. sub-$1 bid/ask
    notation throughout) are kept as computed for the signed variant."""
    p = abs_prc_w.values
    hi = askhi_w.T.rolling(WH_WINDOW, min_periods=1).max().T.values
    hi_abs = np.abs(askhi_w).T.rolling(WH_WINDOW, min_periods=1).max().T.values
    cl = abs_prc_w.T.rolling(WH_WINDOW, min_periods=1).max().T.values
    with np.errstate(divide="ignore", invalid="ignore"):
        wh_hi = p / hi
        wh_hi_abs = p / hi_abs
        wh_cl = p / cl
    for mat in (wh_hi, wh_hi_abs, wh_cl):
        mat[np.isnan(p)] = np.nan
        mat[~np.isfinite(mat)] = np.nan
    return wh_hi, wh_cl, wh_hi_abs


def wh_dc_signal(abs_prc_w: pd.DataFrame, maxdc_w: pd.DataFrame) -> np.ndarray:
    """wh_sig_dc(f) = |prc(f)| / max(max_daily_close) over f-11..f, where
    max_daily_close(m) = max of dsf daily |prc| in calendar month m.

    NaN semantics match wh_sig_cl EXACTLY: rolling 12-month max with
    min_periods=1 (window needs >= 1 non-null month), ratio set to NaN where
    |prc(f)| is missing or the ratio is non-finite. Because max_daily_close(f)
    >= |prc(f)| (the month-end close is one of the daily closes of month f) and
    the window includes month f, the ratio is always <= 1 where defined.
    """
    p = abs_prc_w.values
    dc = maxdc_w.T.rolling(WH_WINDOW, min_periods=1).max().T.values
    with np.errstate(divide="ignore", invalid="ignore"):
        wh_dc = p / dc
    wh_dc[np.isnan(p)] = np.nan
    wh_dc[~np.isfinite(wh_dc)] = np.nan
    return wh_dc


def wh_lo_signal(abs_prc_w: pd.DataFrame, mindc_w: pd.DataFrame) -> np.ndarray:
    """wh_lo_sig(f) = |prc(f)| / min(min_daily_close) over f-11..f, where
    min_daily_close(m) = min of dsf daily |prc| in calendar month m (the
    52-week-LOW signal, audit1.md [M4] prep; paper Table IX 52-low measure =
    P_{t-j} / min price over the trailing 12 months).

    NaN semantics match wh_sig_dc EXACTLY (same grid/NaN machinery, min
    instead of max): rolling 12-month min with min_periods=1 (window needs
    >= 1 non-null month), ratio set to NaN where |prc(f)| is missing or the
    ratio is non-finite. Because min_daily_close(f) <= |prc(f)| (the
    month-end close is one of the daily closes of month f) and the window
    includes month f, the ratio is always >= 1 where defined.
    """
    p = abs_prc_w.values
    dc = mindc_w.T.rolling(WH_WINDOW, min_periods=1).min().T.values
    with np.errstate(divide="ignore", invalid="ignore"):
        wh_lo = p / dc
    wh_lo[np.isnan(p)] = np.nan
    wh_lo[~np.isfinite(wh_lo)] = np.nan
    return wh_lo


def industry_returns(ret_m: np.ndarray, mcap_lag_m: np.ndarray,
                     ind_m: np.ndarray, uni_m: np.ndarray) -> np.ndarray:
    """VW industry returns per (industry, month):
    sum(ret * mcap_lag) / sum(mcap_lag) over universe members with
    mcap_lag > 0 and non-null ret. Returns array (21, n_months), rows 1..20."""
    valid = (
        uni_m
        & np.isfinite(ret_m)
        & np.isfinite(mcap_lag_m)
        & (mcap_lag_m > 0)
        & np.isfinite(ind_m)
    )
    n_months = ret_m.shape[1]
    out = np.full((21, n_months), np.nan)
    for k in range(1, 21):
        mask = valid & (ind_m == k)
        den = np.where(mask, mcap_lag_m, 0.0).sum(axis=0)
        num = np.where(mask, ret_m * mcap_lag_m, 0.0).sum(axis=0)
        np.divide(num, den, out=out[k], where=den > 0)
    return out


def mg_signal(ind_ret: np.ndarray, ind_m: np.ndarray) -> np.ndarray:
    """mg_sig(f) = prod(1 + ind_ret(i's industry at m)) over f-5..f minus 1;
    6 consecutive months required."""
    n, t = ind_m.shape
    j = np.where(np.isfinite(ind_m), ind_m, 0).astype(int)
    months = np.broadcast_to(np.arange(t), (n, t))
    stock_indret = ind_ret[j, months].astype("float64")
    stock_indret[~np.isfinite(ind_m)] = np.nan
    return roll_sum_log(stock_indret, JT_WINDOW)


def gh_signal(abs_prc_m: np.ndarray, turn_m: np.ndarray) -> np.ndarray:
    """GH (2002) embedded capital gain g(f) = (P(f) - R(f)) / P(f),
    R(f) = sum_{s=1..60} w_s P(f-s) / sum w_s,
    w_s  = V(f-s) * prod_{r=f-s+1..f} (1 - V(r)).

    Numerics: work in logs. With C = cumsum ln(1 - V) (V clipped to
    [0, 1-1e-12] inside the log ONLY so V == 1 months zero the weights via
    ~1e-12 factors instead of producing -inf arithmetic),
    log w_s = ln V(f-s) + C(f) - C(f-s) <= 0, so weights stay in [0, 1]
    (no overflow). V(f-s) == 0 -> ln = -inf -> weight 0 (correct: no
    turnover, no reference-price contribution). V == 1 inside the product
    range -> ~1e-12 weight factor (effectively 0). The (1 - V(f)) factor is
    common to all weights and cancels in R(f), so V(f) is not required.
    Missing P or V in f-60..f-1 is caught both by NaN propagation (for the
    f-s term) and by an explicit 60/60 non-null count mask (for interior
    product terms). Requires all 60 months of P and V in f-60..f-1
    non-null, plus P(f) non-null.
    """
    n, t = abs_prc_m.shape
    p = abs_prc_m
    v = turn_m
    tiny = 1e-12
    tlog = np.log(np.maximum(1.0 - np.clip(v, 0.0, 1.0 - tiny), tiny))
    c = np.cumsum(np.where(np.isnan(tlog), 0.0, tlog), axis=1)
    with np.errstate(divide="ignore"):
        ln_v = np.log(v)  # V==0 -> -inf (weight 0); NaN -> NaN
    num = np.zeros((n, t))
    den = np.zeros((n, t))
    for s in range(1, GH_LAGS + 1):
        lw = ln_v[:, : t - s] + (c[:, s:] - c[:, : t - s])
        w = np.exp(lw)  # in [0,1]; -inf -> 0; NaN -> NaN (missing V at f-s)
        num[:, s:] += w * p[:, : t - s]  # NaN if P(f-s) missing
        den[:, s:] += w
    with np.errstate(divide="ignore", invalid="ignore"):
        r = num / den
    r[den <= 0] = np.nan
    g = (p - r) / np.where(p > 0, p, np.nan)
    # explicit 60/60 non-null mask over f-60..f-1 for P and V
    def _win_count_ok(mat: np.ndarray) -> np.ndarray:
        present = np.where(np.isnan(mat), 0, 1)
        excl = np.concatenate(
            [np.zeros((n, 1)), np.cumsum(present, axis=1)[:, :-1]], axis=1
        )
        win = excl[:, GH_LAGS:] - excl[:, : t - GH_LAGS]  # cols f with idx>=60
        return win == GH_LAGS
    ok = _win_count_ok(p) & _win_count_ok(v) & np.isfinite(p[:, GH_LAGS:])
    g[:, :GH_LAGS] = np.nan
    g[:, GH_LAGS:][~ok] = np.nan
    return g


def gh_signal_b(abs_prc_m: np.ndarray, turn_m: np.ndarray) -> np.ndarray:
    """GH (2002) embedded capital gain, VARIANT B (audit1.md [M2]
    adjudication): the same 60-lag turnover-weighted reference price as
    variant A (gh_signal), but renormalized over the AVAILABLE lags instead
    of requiring all 60 months non-null. The paper's formula (2) writes 60
    terms but never states a minimum-coverage rule; variant A's strict
    60-consecutive-month requirement leaves 52.6% of stock-months null
    (1970s monthly-volume missingness ~40%) and breaks the Table VII GH
    dummies (16 FAILs under A).

    For each (permno, month f):
      L = length of the run of consecutive non-null V ENDING at f (same
          capped turnover series as variant A).
      Candidate lags s = 1..min(60, L). A lag is USABLE if P(f-s) is
          non-null and its weight is well-defined — V non-null over f-s..f,
          which the run guarantees for s < L; at s = L, V(f-L) is missing by
          definition of the run (or f-L is before the series start), so the
          weight is undefined and the lag drops out.
      w_s = V(f-s) * prod_{r=f-s+1..f}(1 - V(r)) — same log-space numerics
          as variant A (V clipped to [0, 1-1e-12] inside the log ONLY, so
          V == 1 months contribute ~1e-12 factors and V == 0 gives weight 0;
          a missing V in the product range cannot occur for candidate lags).
      R_f = sum_{usable} w_s P(f-s) / sum_{usable} w_s, computed iff the
          number of usable lags >= GH_B_MIN_USABLE (24); else NaN.
      g(f) = (P(f) - R_f) / P(f); NaN unless P(f) is non-null.

    Consistency with variant A: wherever A is non-null AND V(f) is non-null,
    all 60 lags are usable and B equals A exactly (same sums); B differs
    from A only on partial-coverage months (and on the rare A-defined months
    with V(f) missing, where L = 0 makes B NaN — the (1 - V(f)) factor
    cancels in R(f) mathematically, but the spec's run definition requires
    V(f) present). Variant A is untouched; both columns ship in the panel.
    """
    n, t = abs_prc_m.shape
    p = abs_prc_m
    v = turn_m
    tiny = 1e-12
    tlog = np.log(np.maximum(1.0 - np.clip(v, 0.0, 1.0 - tiny), tiny))
    c = np.cumsum(np.where(np.isnan(tlog), 0.0, tlog), axis=1)
    with np.errstate(divide="ignore"):
        ln_v = np.log(v)  # V==0 -> -inf (weight 0); NaN -> NaN
    # L(n, t): run length of consecutive non-null V ending at each month
    vnn = (~np.isnan(v)).astype(np.int64)
    L = np.zeros((n, t), dtype=np.int64)
    L[:, 0] = vnn[:, 0]
    for j in range(1, t):
        L[:, j] = vnn[:, j] * (L[:, j - 1] + 1)
    p_safe = np.where(np.isnan(p), 0.0, p)
    num = np.zeros((n, t))
    den = np.zeros((n, t))
    cnt = np.zeros((n, t), dtype=np.int64)
    for s in range(1, GH_LAGS + 1):
        lw = ln_v[:, : t - s] + (c[:, s:] - c[:, : t - s])
        w = np.exp(lw)  # in [0,1]; -inf -> 0; NaN -> NaN (missing V at f-s)
        # candidate lags: s <= min(60, L_f) (s <= 60 holds by the loop bound)
        cand = L[:, s:] >= s
        use = cand & (~np.isnan(p[:, : t - s])) & np.isfinite(w)
        w_safe = np.where(use, w, 0.0)
        num[:, s:] += w_safe * p_safe[:, : t - s]
        den[:, s:] += w_safe
        cnt[:, s:] += use
    with np.errstate(divide="ignore", invalid="ignore"):
        r = num / den
    r[den <= 0] = np.nan
    g = (p - r) / np.where(p > 0, p, np.nan)
    g[cnt < GH_B_MIN_USABLE] = np.nan
    return g


# --- panel assembly -----------------------------------------------------------

def build_panel() -> tuple[pd.DataFrame, dict]:
    t0 = time.perf_counter()
    stats: dict = {}

    msf = load_msf()
    dsn = load_dsenames()
    dsf_dc = load_dsf_maxclose()
    dsf_lo = load_dsf_minclose()
    dlel = load_msedelist()
    stats["load_s"] = time.perf_counter() - t0
    stats["msf_rows_fetched"] = len(msf)
    stats["msf_permnos_fetched"] = int(msf["permno"].nunique())
    stats["dsf_dc_rows_fetched"] = len(dsf_dc)
    stats["dsf_dc_permnos_fetched"] = int(dsf_dc["permno"].nunique())
    stats["dsf_lo_rows_fetched"] = len(dsf_lo)
    stats["dsf_lo_permnos_fetched"] = int(dsf_lo["permno"].nunique())
    stats["msedelist_rows_fetched"] = len(dlel)

    t1 = time.perf_counter()
    df = attach_universe_and_sic(msf, dsn)
    df = derive_fields(df)
    stats["merge_s"] = time.perf_counter() - t1

    grid = pd.date_range(GRID_START, GRID_END, freq="ME")          # 540 month-ends
    grid_ext = grid.insert(0, pd.Timestamp("1957-12-31"))          # + Dec-57 for mcap lag
    assert df["month"].isin(grid_ext).all(), "msf month outside grid"

    t1 = time.perf_counter()
    ret_w = to_wide(df, "ret", grid)
    prc_w = to_wide(df, "abs_prc", grid)
    ask_w = to_wide(df, "askhi", grid)
    vol_w = to_wide(df, "vol", grid)
    shr_w = to_wide(df, "shrout", grid)
    turn_w = to_wide(df, "turnover", grid)
    raw_turn_w = to_wide(df, "turnover_raw", grid)
    sic2_w = to_wide(df, "sic2", grid)
    mcap_ext_w = to_wide(df, "mcap", grid_ext)
    ind_w = to_wide(df, "industry", grid)
    uni_w = to_wide(df, "in_universe", grid).fillna(False).astype(bool)
    # Daily-close 52WH denominator: reindex the dsf permno x month frame onto
    # the grid (1958-01 .. 2002-12) and onto the msf permno index so it is
    # row/column-aligned with prc_w (dsf-only permnos drop, msf-only -> NaN).
    maxdc_w = to_wide(dsf_dc, "max_daily_close", grid).reindex(prc_w.index)
    # 52-week-LOW denominator (audit M4 prep): same reindex machinery.
    mindc_w = to_wide(dsf_lo, "min_daily_close", grid).reindex(prc_w.index)
    stats["pivot_s"] = time.perf_counter() - t1

    t1 = time.perf_counter()
    jt = jt_signal(ret_w)
    wh_hi, wh_cl, wh_hi_abs = wh_signals(prc_w, ask_w)
    wh_dc = wh_dc_signal(prc_w, maxdc_w)
    wh_lo = wh_lo_signal(prc_w, mindc_w)
    mcap_lag = mcap_ext_w.values[:, : len(grid)]  # col i = mcap of month i-1
    ind_ret = industry_returns(ret_w.values, mcap_lag, ind_w.values, uni_w.values)
    mg = mg_signal(ind_ret, ind_w.values)
    ggh = gh_signal(prc_w.values, turn_w.values)
    ggh_b = gh_signal_b(prc_w.values, turn_w.values)  # audit M2 variant B
    stats["signals_s"] = time.perf_counter() - t1

    # Long form, universe rows only (rolling signals were computed on the
    # full per-permno history before this filter).
    t1 = time.perf_counter()
    permnos = ret_w.index.to_numpy()
    n_p, n_m = len(permnos), len(grid)
    mask = uni_w.values.ravel()  # row-major: permno then month
    sel = lambda mat: mat.ravel()[mask]
    panel = pd.DataFrame({
        "permno": np.repeat(permnos, n_m)[mask],
        "month": np.tile(grid.to_numpy(), n_p)[mask],
        "ret": sel(ret_w.values),
        "abs_prc": sel(prc_w.values),
        "mcap": sel(mcap_ext_w.values[:, 1:]),  # drop the Dec-57 column
        "vol": sel(vol_w.values),
        "shrout": sel(shr_w.values),
        "sic2": sel(sic2_w.values),
        "industry": sel(ind_w.values),
        "jt_sig": sel(jt),
        "wh_sig_hi": sel(wh_hi),
        "wh_sig_cl": sel(wh_cl),
        "wh_sig_dc": sel(wh_dc),
        "wh_lo_sig": sel(wh_lo),
        "wh_sig_hi_abs": sel(wh_hi_abs),
        "mg_sig": sel(mg),
        "g_gh": sel(ggh),
        "g_gh_b": sel(ggh_b),
        "in_universe": np.ones(int(mask.sum()), dtype=bool),
    })
    # turnover (raw and capped) kept for the report only; not persisted.
    # Carried as temp columns so row alignment survives the delisting-row
    # append + re-sort below (new delisting rows -> NaN turnover).
    panel["_turn"] = sel(turn_w.values)
    panel["_turn_raw"] = sel(raw_turn_w.values)
    stats["assemble_s"] = time.perf_counter() - t1

    # ret_dl: fold dlret into the final month of delisted stocks. Runs AFTER
    # all signal computation — signals and industry returns stay on the
    # original ret; only the holding-period return column is adjusted.
    t1 = time.perf_counter()
    panel, dl_stats = delisting_adjust(panel, dlel, dsn, grid, df)
    dl_ev = dl_stats.pop("dl_events")
    stats["dl_stats"] = dl_stats
    stats["dl_event_stats"] = delisting_event_stats(dl_ev)
    stats["delist_s"] = time.perf_counter() - t1

    panel = panel.sort_values(["permno", "month"]).reset_index(drop=True)
    turn_panel = panel.pop("_turn").to_numpy(dtype="float64")
    raw_turn_panel = panel.pop("_turn_raw").to_numpy(dtype="float64")
    panel = panel[PANEL_COLUMNS]
    panel["permno"] = panel["permno"].astype("int64")
    panel["sic2"] = panel["sic2"].astype("Int16")
    panel["industry"] = panel["industry"].astype("Int16")
    panel["month"] = panel["month"].astype("datetime64[ns]")

    stats["turnover_raw_panel"] = raw_turn_panel
    stats["turnover_panel"] = turn_panel
    stats["total_s"] = time.perf_counter() - t0
    return panel, stats


# --- reporting ------------------------------------------------------------------

def fmt(x, nd=4):
    return f"{x:.{nd}f}" if np.isfinite(x) else "NaN"


def signal_summary(panel: pd.DataFrame) -> pd.DataFrame:
    win = panel[
        (panel["month"] >= SIGNAL_WINDOW_START) & (panel["month"] <= SIGNAL_WINDOW_END)
    ]
    sigs = ["jt_sig", "wh_sig_hi", "wh_sig_cl", "wh_sig_dc", "wh_lo_sig",
            "mg_sig", "g_gh", "g_gh_b"]
    rows = []
    for s in sigs:
        v = win[s].to_numpy(dtype="float64")
        nn = v[np.isfinite(v)]
        rows.append({
            "signal": s,
            "n_total": len(v),
            "null_frac": float(np.mean(~np.isfinite(v))),
            "mean": np.nanmean(nn) if nn.size else np.nan,
            "std": np.nanstd(nn, ddof=1) if nn.size > 1 else np.nan,
            "p01": np.percentile(nn, 1) if nn.size else np.nan,
            "p10": np.percentile(nn, 10) if nn.size else np.nan,
            "p50": np.percentile(nn, 50) if nn.size else np.nan,
            "p90": np.percentile(nn, 90) if nn.size else np.nan,
            "p99": np.percentile(nn, 99) if nn.size else np.nan,
        })
    return pd.DataFrame(rows).set_index("signal")


def report(panel: pd.DataFrame, stats: dict) -> str:
    L: list[str] = []
    L.append("# Panel build report — George & Hwang (2004)")
    L.append("")
    L.append("## 1. Dimensions")
    L.append(f"- rows x cols: {panel.shape[0]} x {panel.shape[1]}")
    L.append(f"- months: {panel['month'].nunique()} "
             f"({panel['month'].min().date()} .. {panel['month'].max().date()})")
    L.append(f"- distinct permnos: {panel['permno'].nunique()}")
    L.append(f"- total stock-months: {len(panel):,}")
    L.append("")
    L.append("## 2. Avg universe stocks/month")
    by_month = panel.groupby("month").size()
    for label, lo, hi in [
        ("1958", "1958-01-01", "1958-12-31"),
        ("1958s (1958-59)", "1958-01-01", "1959-12-31"),
        ("1963", "1963-01-01", "1963-12-31"),
        ("1970", "1970-01-01", "1970-12-31"),
        ("1980", "1980-01-01", "1980-12-31"),
        ("1990", "1990-01-01", "1990-12-31"),
        ("2001", "2001-01-01", "2001-12-31"),
    ]:
        sub = by_month[(by_month.index >= lo) & (by_month.index <= hi)]
        L.append(f"- {label}: {sub.mean():.1f} ({len(sub)} months)")
    L.append("")
    L.append("## 3. Signal summary over formation window "
             f"{SIGNAL_WINDOW_START} .. {SIGNAL_WINDOW_END}")
    summ = signal_summary(panel)
    L.append(summ.to_string(float_format=lambda x: fmt(x, 4)))
    L.append("")
    L.append("## 4. wh_sig_hi sanity (formation window)")
    wh = panel.loc[
        (panel["month"] >= SIGNAL_WINDOW_START)
        & (panel["month"] <= SIGNAL_WINDOW_END), "wh_sig_hi"
    ].to_numpy(dtype="float64")
    nn = wh[np.isfinite(wh)]
    L.append(f"- fraction > 1.005: {np.mean(nn > 1.005):.6f} "
             f"({int(np.sum(nn > 1.005))} of {nn.size})")
    L.append(f"- fraction <= 0 (negative-askhi windows): {np.mean(nn <= 0):.6f}")
    L.append(f"- p99: {np.percentile(nn, 99):.6f}, max: {nn.max():.6f}")
    L.append("")
    L.append("## 4b. wh_sig_dc sanity (daily-close variant, formation window)")
    win = panel[
        (panel["month"] >= SIGNAL_WINDOW_START) & (panel["month"] <= SIGNAL_WINDOW_END)
    ]
    dc = win["wh_sig_dc"].to_numpy(dtype="float64")
    cl = win["wh_sig_cl"].to_numpy(dtype="float64")
    dc_nn = dc[np.isfinite(dc)]
    cl_nn = cl[np.isfinite(cl)]
    L.append(f"- n non-null wh_sig_dc: {dc_nn.size:,} of {dc.size:,} "
             f"(null frac {np.mean(~np.isfinite(dc)):.6f})")
    L.append(f"- avg cross-section n at formation (non-null wh_sig_dc/month): "
             f"{dc_nn.size / win['month'].nunique():.1f}")
    L.append(f"- fraction > 1 (should be 0): {np.mean(dc_nn > 1):.6f} "
             f"({int(np.sum(dc_nn > 1))} of {dc_nn.size})")
    L.append(f"- fraction > 1 + 1e-9 (numerical tolerance): "
             f"{np.mean(dc_nn > 1 + 1e-9):.6f}")
    L.append(f"- wh_sig_dc: mean {np.mean(dc_nn):.6f}, p50 {np.median(dc_nn):.6f}, "
             f"std {np.std(dc_nn, ddof=1):.6f}, min {dc_nn.min():.6f}, "
             f"max {dc_nn.max():.6f}")
    L.append(f"- wh_sig_cl: mean {np.mean(cl_nn):.6f}, p50 {np.median(cl_nn):.6f} "
             "(daily max >= month-end max in the window, so wh_sig_dc mean "
             "should be <= wh_sig_cl mean)")
    L.append(f"- mean(wh_sig_dc) - mean(wh_sig_cl) = "
             f"{np.mean(dc_nn) - np.mean(cl_nn):+.6f} (expected <= 0)")
    L.append("")
    L.append("## 4c. wh_lo_sig sanity (52-week-LOW signal, audit M4 prep, "
             "formation window)")
    lo = win["wh_lo_sig"].to_numpy(dtype="float64")
    lo_nn = lo[np.isfinite(lo)]
    L.append(f"- n non-null wh_lo_sig: {lo_nn.size:,} of {lo.size:,} "
             f"(null frac {np.mean(~np.isfinite(lo)):.6f}; wh_sig_dc null "
             f"frac over the same window: {np.mean(~np.isfinite(dc)):.6f})")
    L.append(f"- avg cross-section n at formation (non-null wh_lo_sig/month): "
             f"{lo_nn.size / win['month'].nunique():.1f}")
    L.append(f"- fraction < 1 (should be 0; month-f close is inside its own "
             f"window): {np.mean(lo_nn < 1):.6f} "
             f"({int(np.sum(lo_nn < 1))} of {lo_nn.size})")
    L.append(f"- fraction < 1 - 1e-9 (numerical tolerance): "
             f"{np.mean(lo_nn < 1 - 1e-9):.6f}")
    L.append(f"- wh_lo_sig: min {lo_nn.min():.6f}, p50 "
             f"{np.percentile(lo_nn, 50):.6f}, p90 "
             f"{np.percentile(lo_nn, 90):.6f}, mean {np.mean(lo_nn):.6f}, "
             f"std {np.std(lo_nn, ddof=1):.6f}, max {lo_nn.max():.6f}")
    L.append("")
    L.append("## 5. Turnover")
    raw = stats["turnover_raw_panel"]
    cap = stats["turnover_panel"]
    have = np.isfinite(raw)
    L.append(f"- stock-months with computable V: {int(have.sum())} of {have.size} "
             f"({have.mean():.4f})")
    L.append(f"- fraction with raw V > 1 (capped): "
             f"{np.mean(raw[have] > 1):.6f} ({int((raw[have] > 1).sum())} months)")
    yr = panel["month"].dt.year.to_numpy()
    for label, lo, hi in [("1958-59", 1958, 1959), ("1960s", 1960, 1969),
                          ("1970s", 1970, 1979), ("1980s", 1980, 1989),
                          ("1990s", 1990, 1999), ("2000-02", 2000, 2002)]:
        m = (yr >= lo) & (yr <= hi) & np.isfinite(cap)
        med = np.median(cap[m]) if m.sum() else np.nan
        L.append(f"- median V {label}: {fmt(med, 4)} (n={int(m.sum()):,})")
    L.append("")
    L.append("## 6. Industry distribution, 1990-06 (MG Table I mapping)")
    m90 = panel.loc[
        panel["month"] == pd.Timestamp("1990-06-30"), "industry"
    ].dropna().astype(int)
    counts = m90.value_counts().sort_index()
    for k, v in counts.items():
        L.append(f"- {k:2d} {MG_INDUSTRY_NAMES.get(k, '?'):<18} {v:5d}")
    L.append(f"- {'':2} {'TOTAL':<18} {counts.sum():5d}")
    L.append("")
    L.append("## 7. Runtime")
    for k in ("load_s", "merge_s", "pivot_s", "signals_s", "assemble_s",
              "delist_s", "total_s"):
        L.append(f"- {k}: {stats[k]:.1f}")
    L.append("")
    L.append("## 7b. Delisting adjustment (ret_dl column; ret itself untouched)")
    dls = stats["dl_stats"]
    des = stats["dl_event_stats"]
    L.append(f"- msedelist rows pulled (dlstdt 1958-01-01..2003-12-31): "
             f"{dls['dl_pulled']:,}; in analysis grid (month <= 2002-12): "
             f"{dls['dl_in_grid']:,}; dropped (2003 months past grid): "
             f"{dls['dl_outside_grid']:,}")
    L.append(f"- in-grid events with valid dlret (non-null, > -1): "
             f"{dls['dl_valid']:,} ({des['frac_valid']:.4f}); dlret NULL: "
             f"{dls['dl_null']:,}; worthless (dlret = -1.0, left as-is): "
             f"{dls['dl_worthless']:,}")
    L.append(f"- existing panel rows adjusted ((1+ret)(1+dlret)-1): "
             f"{dls['dl_adj_existing']:,}")
    L.append(f"- NEW rows added (no panel row at the delisting month; stock "
             f"was an active holding at m-1; ret=NaN so the `ret` variant is "
             f"untouched): {dls['dl_new_rows']:,} — of which with an msf "
             f"return at m (ret_dl = (1+ret_msf)(1+dlret)-1): "
             f"{dls['dl_new_with_msf']:,}; msf row absent (ret_dl = dlret): "
             f"{dls['dl_new_msf_absent']:,}. Not added (valid dlret but no "
             f"panel row at m-1 either — not a plausible holding): "
             f"{dls['dl_skipped_not_holding']:,}")
    L.append("- WHY so many added rows: dsenames nameendt = dlstdt < "
             "month-end, so universe coverage fails at the delisting month "
             "for mid-month delistings; the final-month msf record usually "
             "exists but carries no usable return (see with-msf count), so "
             "the stock-month is absent from the universe panel either way.")
    L.append(f"- mean dlret over valid events: {des['mean_dlret_valid']:.4f}")
    L.append(f"- performance delistings (dlstcd 500-599): {des['n_perf']:,}; "
             f"missing dlret: {des['perf_missing']:,}; worthless: "
             f"{des['perf_worthless']:,}; valid: "
             f"{des['n_perf'] - des['perf_missing'] - des['perf_worthless']:,} "
             f"(frac {des['perf_frac_valid']:.4f})")
    L.append(f"- mean dlret of valid performance delistings: "
             f"{des['mean_dlret_perf']:.4f} (median {des['median_dlret_perf']:.4f})")
    L.append("- performance-delist missing-dlret by decade (n / missing / "
             "worthless / valid):")
    for d in sorted(des["perf_by_decade"]):
        b = des["perf_by_decade"][d]
        L.append(f"  - {d}s: {b['n']} / {b['missing']} / {b['worthless']} / {b['valid']}")
    for code in (580, 584):
        cs = des[f"code_{code}"]
        L.append(f"- dlstcd {code}: n {cs['n']}, missing {cs['missing']}, "
                 f"valid {cs['valid']}, mean dlret (valid) {fmt(cs['mean_dlret'])}")
    L.append("- NO Shumway/BMP imputation for missing dlret (post-paper "
             "methodology): missing/worthless events keep ret_dl = ret.")
    L.append("")
    L.append("## 7c. g_gh variant B vs variant A coverage (audit M2 "
             "adjudication; g_gh untouched, g_gh_b additive)")
    win2 = panel[
        (panel["month"] >= SIGNAL_WINDOW_START) & (panel["month"] <= SIGNAL_WINDOW_END)
    ]
    ga_all = panel["g_gh"].to_numpy(dtype="float64")
    gb_all = panel["g_gh_b"].to_numpy(dtype="float64")
    ga = win2["g_gh"].to_numpy(dtype="float64")
    gb = win2["g_gh_b"].to_numpy(dtype="float64")
    L.append(f"- null fraction, ALL panel rows: g_gh (A) "
             f"{np.mean(~np.isfinite(ga_all)):.4f} vs g_gh_b (B) "
             f"{np.mean(~np.isfinite(gb_all)):.4f}")
    L.append(f"- null fraction, formation window "
             f"{SIGNAL_WINDOW_START} .. {SIGNAL_WINDOW_END}: g_gh (A) "
             f"{np.mean(~np.isfinite(ga)):.4f} vs g_gh_b (B) "
             f"{np.mean(~np.isfinite(gb)):.4f}")
    L.append("- null fraction by decade (formation window):")
    dec = (win2["month"].dt.year // 10 * 10).to_numpy()
    for d in sorted(set(dec)):
        m = dec == d
        L.append(f"  - {d}s: A {np.mean(~np.isfinite(ga[m])):.4f} "
                 f"(n={int(m.sum()):,}) vs B {np.mean(~np.isfinite(gb[m])):.4f}")
    for label, v in (("g_gh (A)", ga), ("g_gh_b (B)", gb)):
        nn = v[np.isfinite(v)]
        L.append(f"- {label} distribution (formation window, "
                 f"n={nn.size:,}): mean {np.mean(nn):.4f}, p01 "
                 f"{np.percentile(nn, 1):.4f}, p10 "
                 f"{np.percentile(nn, 10):.4f}, p50 "
                 f"{np.percentile(nn, 50):.4f}, p90 "
                 f"{np.percentile(nn, 90):.4f}, p99 "
                 f"{np.percentile(nn, 99):.4f}, std {np.std(nn, ddof=1):.4f}, "
                 f"min {nn.min():.4f}, max {nn.max():.4f}")
    both = np.isfinite(ga) & np.isfinite(gb)
    n_both = int(both.sum())
    exact = bool(np.array_equal(ga[both], gb[both])) if n_both else True
    L.append(f"- consistency: {n_both:,} stock-months non-null under BOTH A "
             f"and B; values bit-identical: {exact} (B == A must hold "
             "wherever A is defined and V(f) is non-null — there all 60 lags "
             "are usable and the sums coincide)")
    L.append("")
    L.append("## Extra facts")
    L.append(f"- msf rows fetched (post hygiene filter, incl. 1957-12): "
             f"{stats['msf_rows_fetched']:,} across {stats['msf_permnos_fetched']:,} permnos")
    L.append(f"- dsf monthly max-close rows fetched (1957-01..2002-12): "
             f"{stats['dsf_dc_rows_fetched']:,} across "
             f"{stats['dsf_dc_permnos_fetched']:,} permnos")
    L.append(f"- dsf monthly min-close rows fetched (1957-01..2002-12): "
             f"{stats['dsf_lo_rows_fetched']:,} across "
             f"{stats['dsf_lo_permnos_fetched']:,} permnos")
    jul63 = by_month[by_month.index == pd.Timestamp("1963-07-31")]
    L.append(f"- Jul 1963 universe stocks: {int(jul63.iloc[0]) if len(jul63) else 'NA'}")
    mg58 = panel.loc[panel["month"].dt.year == 1958, "mg_sig"]
    L.append(f"- mg_sig non-null in 1958 (verifies Dec-1957 mcap lag feeds "
             f"Jan-1958 industry returns): {int(mg58.notna().sum())}")
    L.append("")
    L.append("## Data caveats (facts for the Replicator)")
    wh2 = panel["wh_sig_hi"].to_numpy(dtype="float64")
    L.append(f"- wh_sig_hi <= 0 overall: {np.mean(wh2[np.isfinite(wh2)] <= 0):.4f} "
             "— negative because CRSP stores askhi with the sign convention "
             "(negative = bid/ask quote, not trade high) for low-priced/"
             "pre-1983 NASDAQ stocks; windows with all-negative askhi give "
             "negative ratios. By decade: 1970s 0.404, 1980s 0.379, 1990s "
             "0.050, 2000s 0.0003.")
    vr = stats["turnover_raw_panel"]
    have = np.isfinite(vr)
    L.append(f"- vol/shrout missing (V not computable): {(~have).mean():.4f} of "
             "panel stock-months; concentrated in the 1970s (0.404) and "
             "1980s (0.136), ~0 elsewhere — drives g_gh null fraction "
             "(g_gh_b variant B renormalizes over available lags instead; "
             "see sec 7c).")
    L.append("- ClickHouse Date type cannot hold pre-1970 dates: all SQL "
             "date conversions use toDate32; month-end keys derived in "
             "pandas (date + MonthEnd(0)).")
    return "\n".join(L)


def verify_bitexact_vs_previous(new_panel: pd.DataFrame) -> str:
    """Rebuild guard: every (permno, month) row of the PREVIOUS panel.parquet
    must reproduce bit-exactly in the new panel for ALL pre-existing columns
    (ret untouched, signals untouched). The new panel may have EXTRA rows
    (delisting-month rows with ret NaN, ret_dl set). ret_dl is the
    experimental column: it is NOT part of the bit-exact assertion (its
    definition is what the experiment iterates on), but common-row changes
    are reported."""
    path = LAYOUT.data_path("panel.parquet")
    if not path.exists():
        return "no previous panel.parquet found — verification skipped"
    old = pd.read_parquet(path)
    # Core rows = pre-experiment rows: the original panel's ret is ALWAYS
    # finite (msf hygiene filter); delisting-experiment added rows carry
    # ret = NaN. The bit-exact assertion covers the core rows; experimental
    # rows may legitimately come and go as the ret_dl rule iterates.
    old_core = old[old["ret"].notna()]
    old_added = old[old["ret"].isna()]
    merged = new_panel.merge(old_core, on=["permno", "month"], how="right",
                             suffixes=("_new", "_old"), validate="one_to_one")
    bad = []
    for c in old_core.columns:
        if c in ("permno", "month", "ret_dl"):
            continue
        if not merged[f"{c}_new"].reset_index(drop=True).equals(
                merged[f"{c}_old"].reset_index(drop=True)):
            bad.append(c)
    assert not bad, f"bit-exact reproduction FAILED for columns: {bad}"
    n_extra = len(new_panel) - len(old)
    note = ""
    if "ret_dl" in old.columns:
        a = merged["ret_dl_new"].reset_index(drop=True)
        b = merged["ret_dl_old"].reset_index(drop=True)
        changed = int(((a != b) & ~(a.isna() & b.isna())).sum())
        note = f"; ret_dl changed on {changed:,} core rows (experimental column)"
    if len(old_added):
        new_keys = set(zip(new_panel["permno"], new_panel["month"]))
        kept = sum(1 for p, m in zip(old_added["permno"], old_added["month"])
                   if (p, m) in new_keys)
        note += (f"; previous experimental rows (ret NaN): {len(old_added):,}, "
                 f"of which {kept:,} still present")
    return (f"bit-exact OK: all {len(old_core):,} core rows x "
            f"{len(old_core.columns)} columns reproduce exactly except the "
            f"experimental ret_dl (ret untouched); new panel has {n_extra:+,} "
            f"rows vs previous{note}")


def main() -> None:
    panel, stats = build_panel()
    print(verify_bitexact_vs_previous(panel))
    out = LAYOUT.data_path("panel.parquet")
    panel.to_parquet(out, index=False)
    print(f"saved {out}: {panel.shape[0]:,} rows x {panel.shape[1]} cols")
    # delisting merge stats for src/delisting_experiment.py (avoids re-pulls)
    LAYOUT.data_path("delisting_stats.json").write_text(json.dumps(
        {"dl_stats": stats["dl_stats"],
         "dl_event_stats": stats["dl_event_stats"]}, indent=2))
    text = report(panel, stats)
    LAYOUT.result_path("panel_summary.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
