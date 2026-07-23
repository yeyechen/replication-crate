"""
Replication of Moskowitz & Grinblatt (1999) "Do Industries Explain Momentum?"

Two-stage pipeline (orchestrated by main()):

  Stage 1 (run_stage1, inner-loop iteration 1) — CRSP-based data pipeline.
  Builds two analysis-ready artifacts:
    data/panel.parquet            — monthly stock panel, 1962-01 .. 1995-07,
                                    universe-filtered (shrcd 10/11, exchcd 1/2/3,
                                    PIT via msenames), with ME, return signals,
                                    and industry-level series merged on (41 cols).
    data/bin_rets.parquet           — 20 MG industry bins, monthly VW/EW
                                    returns, stock counts, total ME, and
                                    industry-level past-return signals.
  Expensive (~20 min); skipped when data/panel.parquet exists unless --rebuild.

  Stage 2 (add_fundamentals.enrich_panel, inner-loop iteration 2) — always runs.
  Reads the 41-col panel, enriches it with Compustat book equity (be_dollars,
  bm_sort, ln_beme), Daniel-Titman 5x5 adjusted returns (r_sb), DGTW 5x5x5
  adjusted returns (r_dgtw), and pre-ranking-smoothed market beta (beta_raw,
  beta_smoothed), and rewrites data/panel.parquet (48 cols). Idempotent.

  Stage 3 (tables_1_2_3.run, inner-loop iteration 4) — always runs after stage 2.
  Reads the 48-col panel + bin_rets, runs the individual (6,6) and
  industry IM(L,H) momentum-strategy engines, and writes results/table_{1,2,3}.md,
  three plots, and results/cells_tables_1_2_3.json (per-cell ours-vs-paper).

  Stage 4 (table_6.run, inner-loop iteration 7) — always runs after stage 3.
  Reads the 48-col panel, runs the paper's 32 monthly Fama-MacBeth regressions
  (Table VI, Panels A-D; Jan 1973-Jul 1995, T=271) of r_sb on beta/log size/log
  BE-ME + individual/industry past-return variables (plain iid FM, no Newey-West,
  no winsorization), and writes results/table_6.md, results/cells_table_6.json
  (416 cells), results/fm_interaction.png, plus a report-only NYSE/AMEX-only
  (6,6) raw diagnostic.

Stage-1 pipeline is SQL-first (msf x msenames PIT join + filters + ME in
ClickHouse; see src/sql/*.sql). Rolling return-signal windows are computed in
pandas on a complete monthly grid per permno using a NaN-aware cumulative
log-return trick (segment-id + cumsum), so a missing month anywhere inside a
window propagates NaN (strict window requirement).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402

SLUG = "do_industries_explain_momentum"
LAYOUT = paper_layout(SLUG)
SQL_DIR = LAYOUT.src_path("sql")
_CFG = get_clickhouse_config()

# Sample window (spec; also documented in preparations/assumptions.md):
# months 1962-01 .. 1995-07 inclusive (1962-63 = warmup).
PANEL_START = "1962-01"
PANEL_END = "1995-07"
# Paper sample for Table-I-style averages: July 1963 .. July 1995 (T = 383).
SAMPLE_START = "1963-07"
SAMPLE_END = "1995-07"

# ----------------------------------------------------------------------------
# ClickHouse access
# ----------------------------------------------------------------------------


def _client() -> Client:
    # No database= : all queries use fully-qualified table names
    # (crsp_202601.*, ff.*). write_yeye is only needed for server-side writes.
    return Client(
        host=_CFG["host"],
        port=int(_CFG["port"]),
        user=_CFG["user"],
        password=_CFG["password"],
        settings={"max_execution_time": 600},
    )


def q(sql: str) -> pd.DataFrame:
    c = _client()
    try:
        data, cols = c.execute(sql, with_column_types=True)
    finally:
        c.disconnect()
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    return q((SQL_DIR / name).read_text())


# ----------------------------------------------------------------------------
# Industry mapping (Table I of the paper) — sic2 = floor(siccd / 100)
# ----------------------------------------------------------------------------

SIC2_GROUPS = {
    1: [10, 11, 12, 13, 14],          # Mining
    2: [20],                           # Food
    3: [22, 23],                       # Apparel
    4: [26],                           # Paper
    5: [28],                           # Chemical
    6: [29],                           # Petroleum
    7: [32],                           # Construction
    8: [33],                           # Prim Metals
    9: [34],                           # Fab Metals
    10: [35],                          # Machinery
    11: [36],                          # Electrical Eq
    12: [37],                          # Transport Eq
    13: [38, 39],                      # Manufacturing
    14: [40],                          # Railroads
    15: list(range(41, 48)),           # Other Transport (41-47)
    16: [49],                          # Utilities
    17: [53],                          # Dept Stores
    18: [50, 51, 52, 54, 55, 56, 57, 58, 59],  # Retail
    19: list(range(60, 70)),           # Financial (60-69)
}
SIC2_TO_IND = {s: ind for ind, lst in SIC2_GROUPS.items() for s in lst}
IND_NAMES = {
    1: "Mining", 2: "Food", 3: "Apparel", 4: "Paper", 5: "Chemical",
    6: "Petroleum", 7: "Construction", 8: "Prim.Metals", 9: "Fab.Metals",
    10: "Machinery", 11: "Elec.Eq", 12: "Transp.Eq", 13: "Manuf",
    14: "Railroads", 15: "OtherTransp", 16: "Utilities", 17: "Dept.Stores",
    18: "Retail", 19: "Financial", 20: "Other",
}


def assign_industry(siccd: pd.Series) -> pd.Series:
    """siccd (4-digit, PIT) -> MG industry 1..20; missing/0/9999 -> 20."""
    sic2 = (siccd // 100).where(siccd.notna() & (siccd > 0))
    return sic2.map(SIC2_TO_IND).fillna(20).astype(int)


# ----------------------------------------------------------------------------
# Return-window signals (NaN-aware, strict windows)
# ----------------------------------------------------------------------------
# Window definitions, expressed as (a, b) offset pairs meaning
# cum(t-b .. t-a) = prod_{k=a}^{b} (1 + ret_{t-k}) - 1.
CUM6_WINDOWS = [(6, 11), (5, 10), (4, 9), (3, 8), (2, 7), (1, 6)]
CUM12_WINDOWS = [(1 + j, 12 + j) for j in range(12)]
CUM6S_WINDOWS = CUM6_WINDOWS[:5]                     # excl. cum(t-6..t-1)
CUM12S_WINDOWS = [(2 + j, 13 + j) for j in range(11)]


class WindowSignals:
    """Compute strict-window cumulative return signals on a complete
    monthly grid (one row per id x month; missing months = NaN rows).

    Uses ln(1+ret) with segment ids that increment at every NaN: within a
    segment the cumsum cs is continuous, and
        cum(t-b .. t-a) = exp(cs.shift(a) - cs.shift(b+1)) - 1
    is valid iff both endpoints fall in the same segment (i.e. no missing
    month inside the window); otherwise it is NaN. Out-of-grid positions
    (shift past the start) are also NaN. This is O(n) per window instead of
    O(n * w) for rolling-apply products.
    """

    def __init__(self, ret: pd.Series, group: np.ndarray):
        ln1p = np.log1p(ret.to_numpy(dtype="float64"))
        self._n = len(ret)
        self._group = group
        isna = np.isnan(ln1p)
        self._seg = (
            pd.Series(isna, index=ret.index).groupby(group).cumsum().to_numpy()
        )
        safe = np.where(isna, 0.0, ln1p)
        self._cs = (
            pd.Series(safe, index=ret.index)
            .groupby([group, self._seg])
            .cumsum()
            .to_numpy()
        )
        self._cs_s = pd.Series(self._cs, index=ret.index)
        self._seg_s = pd.Series(self._seg, index=ret.index)

    def shift(self, k: int) -> pd.Series:
        """k-period lag within group (k=0 -> the series itself)."""
        if k == 0:
            return pd.Series(self._cs, index=self._cs_s.index)
        return self._cs_s.groupby(self._group).shift(k)

    def lag_ret(self, ret: pd.Series, k: int) -> pd.Series:
        return ret.groupby(self._group).shift(k)

    def cumwin(self, a: int, b: int) -> np.ndarray:
        """cum(t-b .. t-a); NaN unless every month in the window exists."""
        ca = self._cs_s.groupby(self._group).shift(a).to_numpy()
        cb = self._cs_s.groupby(self._group).shift(b + 1).to_numpy()
        sa = self._seg_s.groupby(self._group).shift(a).to_numpy()
        sb = self._seg_s.groupby(self._group).shift(b + 1).to_numpy()
        with np.errstate(over="ignore", invalid="ignore"):
            out = np.exp(ca - cb) - 1.0
        same_seg = (sa == sb) & ~np.isnan(sa) & ~np.isnan(sb)
        out = np.where(same_seg, out, np.nan)
        return out

    def cumwin_mean(self, windows: list[tuple[int, int]]) -> np.ndarray:
        """Equal-weighted mean of several cumwins; NaN propagates."""
        stack = np.column_stack([self.cumwin(a, b) for a, b in windows])
        return stack.mean(axis=1)  # mean propagates NaN


def stock_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Compute mom1, me_lag1 and all return-window signals per permno on a
    complete monthly grid, then merge back onto df (inner on permno/month).
    """
    df = df.copy()
    if "month" not in df.columns:
        df["month"] = df["date"].dt.to_period("M")
    months = pd.period_range(df["month"].min(), df["month"].max(), freq="M")
    permnos = np.sort(df["permno"].unique())
    idx = pd.MultiIndex.from_product([permnos, months], names=["permno", "month"])

    base = df.set_index(["permno", "month"]).sort_index()
    ret = base["ret"].reindex(idx)
    me = base["me"].reindex(idx)
    group = idx.get_level_values(0).to_numpy()

    ws = WindowSignals(ret, group)
    mom1 = ws.lag_ret(ret, 1).to_numpy()
    me_lag1 = me.groupby(group).shift(1).to_numpy()

    mom6 = ws.cumwin(1, 6)
    mom12 = ws.cumwin(1, 12)
    ret_11_6 = ws.cumwin(6, 11)
    ret_36_13 = ws.cumwin(13, 36)
    ret_7_2 = ws.cumwin(2, 7)
    ret_12_2 = ws.cumwin(2, 13)
    ret_6_6 = ws.cumwin_mean(CUM6_WINDOWS)
    ret_12_12 = ws.cumwin_mean(CUM12_WINDOWS)
    ret_6_6s = ws.cumwin_mean(CUM6S_WINDOWS)
    ret_12_12s = ws.cumwin_mean(CUM12S_WINDOWS)

    sig = pd.DataFrame(
        {
            "mom1": mom1,
            "me_lag1": me_lag1,
            "mom6": mom6,
            "mom12": mom12,
            "ret_11_6": ret_11_6,
            "ret_36_13": ret_36_13,
            "ret_6_6": ret_6_6,
            "ret_12_12": ret_12_12,
            "ret_7_2": ret_7_2,
            "ret_12_2": ret_12_2,
            "ret_6_6s": ret_6_6s,
            "ret_12_12s": ret_12_12s,
        },
        index=idx,
    ).reset_index()
    return df.merge(sig, on=["permno", "month"], how="left")


def industry_signals(ind_ret: pd.DataFrame, months: pd.PeriodIndex) -> pd.DataFrame:
    """Industry-level past-return signals from ind_ret_vw, same window
    definitions as the stock-level signals. ind_ret: long frame with
    columns [ind, month, ind_ret_vw]; reindexed to a complete ind x month
    grid so missing industry-months propagate NaN."""
    inds = np.arange(1, 21)
    idx = pd.MultiIndex.from_product([inds, months], names=["ind", "month"])
    full = (
        ind_ret.set_index(["ind", "month"])["ind_ret_vw"]
        .reindex(idx)
        .astype("float64")
    )
    group = idx.get_level_values(0).to_numpy()
    ws = WindowSignals(full, group)

    out = pd.DataFrame(
        {
            "ind_mom1": ws.lag_ret(full, 1).to_numpy(),
            "ind_mom6": ws.cumwin(1, 6),
            "ind_mom12": ws.cumwin(1, 12),
            "ind_ret_11_6": ws.cumwin(6, 11),
            "ind_ret_36_13": ws.cumwin(13, 36),
            "ind_ret_6_6": ws.cumwin_mean(CUM6_WINDOWS),
            "ind_ret_12_12": ws.cumwin_mean(CUM12_WINDOWS),
            "ind_ret_7_2": ws.cumwin(2, 7),
            "ind_ret_12_2": ws.cumwin(2, 13),
            "ind_ret_6_6s": ws.cumwin_mean(CUM6S_WINDOWS),
            "ind_ret_12_12s": ws.cumwin_mean(CUM12S_WINDOWS),
        },
        index=idx,
    ).reset_index()
    return out


# ----------------------------------------------------------------------------
# Pipeline
# ----------------------------------------------------------------------------


def run_stage1() -> int:
    """CRSP pipeline (iteration 1): build data/panel.parquet (41 cols) and
    data/bin_rets.parquet from ClickHouse. Expensive (~20 min); the
    orchestrator skips it when the panel already exists unless --rebuild."""
    LAYOUT.ensure()
    # preprocessing_rules.json is a rule registry (list of paper-derived
    # rules); the sample window is pinned by the task spec / SQL files.
    rules = json.loads(LAYOUT.preparations_path("preprocessing_rules.json").read_text())
    print(f"[config] {len(rules)} preprocessing rules registered for {SLUG}")

    # -- 1. Pull universe monthly panel from ClickHouse (SQL-first) ----------
    print("[1/7] universe_monthly.sql (msf x msenames PIT join) ...")
    df = q_file("universe_monthly.sql")
    df["date"] = pd.to_datetime(df["date"])
    # Nullable(Int32) columns come back as object arrays of Python ints/None.
    df["permno"] = df["permno"].astype("int64")
    df["shrcd"] = df["shrcd"].astype("Int64")
    df["exchcd"] = df["exchcd"].astype("Int64")
    df["siccd"] = df["siccd"].astype("Int64")
    for c in ["ret", "vol", "me", "dollar_vol"]:
        df[c] = df[c].astype("float64")
    # msf dates are LAST-TRADING-day of month (e.g. '1964-05-28'), while
    # ff/msi dates are CALENDAR month ends — so all cross-table merges are
    # done by year-month, never by exact date.
    df["month"] = df["date"].dt.to_period("M")
    print(f"      pulled {len(df):,} rows, "
          f"{df['permno'].nunique():,} permnos, "
          f"{df['date'].min().date()} .. {df['date'].max().date()}")
    day_counts = df["date"].dt.day.value_counts().head(3)
    print(f"      day-of-month distribution (top 3): "
          f"{day_counts.to_dict()}")

    # -- validation: benchmark universe counts (pure PIT + shrcd/exchcd) ----
    chk = q_file("universe_count_check.sql")
    chk["month"] = chk["ym"].map(
        lambda v: pd.Period(f"{v // 100}-{v % 100:02d}", "M")
    )
    expect = {"1963-07": 3478, "1970-06": 2270, "1980-06": 4632,
              "1990-06": 5818, "1995-06": 6775}
    print("      benchmark universe counts (SQL, PIT join only):")
    for m, n in expect.items():
        got = int(chk.loc[chk["month"] == pd.Period(m, "M"), "n"].iloc[0]) \
            if (chk["month"] == pd.Period(m, "M")).any() else None
        print(f"        {m}: got {got} | expected {n} | "
              f"{'MATCH' if got == n else 'MISMATCH'}")

    # -- 2. Clean returns, build ME panel ------------------------------------
    # CRSP missing-return sentinels (-44/-55/-66/-77/-88/-99) appear as
    # non-NULL floats < -1; no true monthly return can be below -100%, so
    # ret < -1 is set to NaN (data cleaning, not a methodology screen).
    n_sent = int((df["ret"] < -1.0).sum())
    df.loc[df["ret"] < -1.0, "ret"] = np.nan
    n_univ = len(df)  # universe rows (me may still be missing)
    df = df[df["me"].notna()].copy()
    print(f"[2/7] ret sentinels (< -1) set to NaN: {n_sent:,} "
          f"({n_sent / n_univ * 100:.3f}% of universe rows)")
    print(f"      rows dropped for missing prc/shrout (no me): "
          f"{n_univ - len(df):,} -> panel rows: {len(df):,}")

    df = df.sort_values(["permno", "date"]).reset_index(drop=True)
    df["sic2"] = (df["siccd"] // 100).astype("Int64").where(df["siccd"].notna())
    df["ind"] = assign_industry(df["siccd"])

    # -- 3. Merge rf and market index returns; exret -------------------------
    print("[3/7] rf_monthly.sql + market_index_monthly.sql ...")
    rf = q_file("rf_monthly.sql")
    rf["month"] = pd.to_datetime(rf["date"]).dt.to_period("M")
    msi = q_file("market_index_monthly.sql")
    msi["month"] = pd.to_datetime(msi["date"]).dt.to_period("M")
    df = df.merge(rf[["month", "rf"]], on="month", how="left").merge(
        msi[["month", "vw_mkt", "ew_mkt"]], on="month", how="left"
    )
    df["exret"] = df["ret"] - df["rf"]
    print(f"      rf months: {len(rf)} ({rf['month'].min()} .. "
          f"{rf['month'].max()}); rf null in panel: "
          f"{int(df['rf'].isna().sum())}; vw_mkt null in panel: "
          f"{int(df['vw_mkt'].isna().sum())}; msi months: {len(msi)}")

    # -- 4. Stock-level signals on the complete monthly grid -----------------
    print("[4/7] stock-level signals (strict windows, NaN propagation) ...")
    df = stock_signals(df)
    df["ln_size"] = np.log(df["me_lag1"].where(df["me_lag1"] > 0))

    # -- 5. Industry monthly series ------------------------------------------
    print("[5/7] bin_rets (industry monthly) aggregation + industry signals ...")
    months_all = pd.period_range(
        df["date"].dt.to_period("M").min(),
        df["date"].dt.to_period("M").max(),
        freq="M",
    )
    month_date = df.groupby("month")["date"].max()

    # VW weights = beginning-of-month ME (me_lag1 > 0), ret nonmissing.
    elig = df[df["ret"].notna() & df["me_lag1"].notna() & (df["me_lag1"] > 0)].copy()
    wsum = (
        elig.assign(w=elig["me_lag1"] * elig["ret"])
        .groupby(["month", "ind"])["w"].sum()
        / elig.groupby(["month", "ind"])["me_lag1"].sum()
    ).rename("ind_ret_vw")
    g_all = elig.groupby(["month", "ind"])
    ind = pd.DataFrame({"ind_ret_vw": wsum})
    ind["ind_ret_ew"] = g_all["ret"].mean()
    ind["n_stocks"] = g_all.size().astype(int)
    ind = ind.reset_index()

    univ_counts = (
        df.groupby(["month", "ind"]).size().rename("n_stocks_univ").reset_index()
    )
    total_me = (
        df.groupby(["month", "ind"])["me"].sum().rename("total_me").reset_index()
    )
    ind = ind.merge(univ_counts, on=["month", "ind"], how="outer").merge(
        total_me, on=["month", "ind"], how="outer"
    )

    # industry signals from ind_ret_vw (complete 1..20 x months grid)
    ind_sig = industry_signals(ind[["ind", "month", "ind_ret_vw"]], months_all)
    ind = ind.merge(ind_sig, on=["ind", "month"], how="outer")
    ind = ind.sort_values(["ind", "month"]).reset_index(drop=True)
    ind["date"] = ind["month"].map(month_date)

    ind_cols_out = [
        "date", "ind", "ind_ret_vw", "ind_ret_ew", "n_stocks",
        "n_stocks_univ", "total_me", "ind_mom1", "ind_mom6", "ind_mom12",
        "ind_ret_11_6", "ind_ret_36_13", "ind_ret_6_6", "ind_ret_12_12",
        "ind_ret_7_2", "ind_ret_12_2", "ind_ret_6_6s", "ind_ret_12_12s",
    ]
    ind_path = LAYOUT.data_path("bin_rets.parquet")
    ind[ind_cols_out].to_parquet(ind_path, index=False)
    print(f"      wrote {ind_path.name}: {len(ind):,} rows x "
          f"{len(ind_cols_out)} cols")

    # -- 6. Merge industry series onto the panel; write panel.parquet --------
    print("[6/7] merge industry series onto panel; write panel.parquet ...")
    df = df.merge(ind[["month", "ind"] + [c for c in ind_cols_out
                                          if c not in ("date", "ind")]],
                  on=["month", "ind"], how="left")

    final_cols = [
        "permno", "date", "ret", "exret", "me", "me_lag1", "vol", "dollar_vol",
        "shrcd", "exchcd", "siccd", "sic2", "ind", "rf", "vw_mkt", "ew_mkt",
        "mom1", "mom6", "mom12", "ret_11_6", "ret_36_13", "ret_6_6",
        "ret_12_12", "ret_7_2", "ret_12_2", "ret_6_6s", "ret_12_12s",
        "ln_size", "ind_ret_vw", "ind_ret_ew", "ind_mom1", "ind_mom6",
        "ind_mom12", "ind_ret_11_6", "ind_ret_36_13", "ind_ret_6_6",
        "ind_ret_12_12", "ind_ret_7_2", "ind_ret_12_2", "ind_ret_6_6s",
        "ind_ret_12_12s",
    ]
    panel = df[final_cols].sort_values(["permno", "date"]).reset_index(drop=True)
    panel_path = LAYOUT.data_path("panel.parquet")
    panel.to_parquet(panel_path, index=False)
    print(f"      wrote {panel_path.name}: {len(panel):,} rows x "
          f"{len(panel.columns)} cols")

    # -- 7. Report ------------------------------------------------------------
    print("[7/7] report")
    panel["month"] = panel["date"].dt.to_period("M")
    samp = (panel["month"] >= pd.Period(SAMPLE_START, "M")) & (
        panel["month"] <= pd.Period(SAMPLE_END, "M")
    )
    psamp = panel[samp]
    n_months_samp = psamp["month"].nunique()

    print("\n=== R1: panel dimensions ===")
    print(f"rows={len(panel):,}, cols={len(panel.columns)}, "
          f"permnos={panel['permno'].nunique():,}, "
          f"months={panel['month'].nunique()}, "
          f"range {panel['date'].min().date()} .. {panel['date'].max().date()}")
    print("columns:", list(panel.columns))

    print("\n=== R2: universe counts ===")
    cnt_by_month = panel.groupby("month").size()
    for m in ["1963-07", "1970-06", "1980-06", "1990-06", "1995-06"]:
        print(f"  panel count {m}: {int(cnt_by_month.get(pd.Period(m, 'M'), 0))}")
    print(f"  avg monthly panel count {SAMPLE_START}..{SAMPLE_END}: "
          f"{cnt_by_month[(cnt_by_month.index >= pd.Period(SAMPLE_START, 'M')) & (cnt_by_month.index <= pd.Period(SAMPLE_END, 'M'))].mean():.1f} "
          f"(paper Table I total ~4609.7)")
    # n_stocks_univ averaged across industries per month = panel count; also
    # report avg n_stocks (ret + me_lag1 eligible) for comparison.
    ind_samp = ind[(ind["month"] >= pd.Period(SAMPLE_START, "M")) &
                   (ind["month"] <= pd.Period(SAMPLE_END, "M"))]
    per_month_nuniv = ind_samp.groupby("month")["n_stocks_univ"].sum()
    per_month_n = ind_samp.groupby("month")["n_stocks"].sum()
    print(f"  avg sum(n_stocks_univ)/month over industries: {per_month_nuniv.mean():.1f}")
    print(f"  avg sum(n_stocks)/month over industries: {per_month_n.mean():.1f}")

    print("\n=== R3: per-industry avg n_stocks / n_univ / cap share "
          f"({SAMPLE_START}..{SAMPLE_END}, {n_months_samp} months) ===")
    tot_me_all = ind_samp.groupby("month")["total_me"].sum()
    ind_samp = ind_samp.assign(
        cap_share=ind_samp["total_me"] / ind_samp["month"].map(tot_me_all)
    )
    agg = ind_samp.groupby("ind").agg(
        avg_n=("n_stocks", "mean"),
        avg_n_univ=("n_stocks_univ", "mean"),
        avg_cap_share=("cap_share", "mean"),
    )
    for i in range(1, 21):
        r = agg.loc[i]
        print(f"  {i:2d} {IND_NAMES[i]:<13s} n={r.avg_n:7.2f} "
              f"n_univ={r.avg_n_univ:7.2f} share={r.avg_cap_share * 100:5.2f}%")

    print("\n=== R4: per-industry avg monthly EXCESS return (ind_ret_vw - rf) ===")
    rf_by_month = panel.drop_duplicates("month").set_index("month")["rf"]
    exc = ind_samp.merge(
        rf_by_month.rename("rf"), left_on="month", right_index=True, how="left"
    )
    exc["exc"] = exc["ind_ret_vw"] - exc["rf"]
    for i in range(1, 21):
        m = exc.loc[exc["ind"] == i, "exc"].mean()
        print(f"  {i:2d} {IND_NAMES[i]:<13s} {m:.4f}")

    print("\n=== R5: signal summary at 1990-06 ===")
    p90 = panel[panel["month"] == pd.Period("1990-06", "M")]
    m6 = p90["mom6"]
    print(f"  n stocks: {len(p90)}")
    print(f"  mom6: mean={m6.mean():.4f}, median={m6.median():.4f}, "
          f"std={m6.std():.4f}, null%={m6.isna().mean() * 100:.2f}%")
    print(f"  ret_36_13 null%: {p90['ret_36_13'].isna().mean() * 100:.2f}%")
    sig_cols = ["mom1", "mom6", "mom12", "ret_11_6", "ret_36_13", "ret_6_6",
                "ret_12_12", "ret_7_2", "ret_12_2", "ret_6_6s", "ret_12_12s"]
    all_sig = p90[sig_cols + ["ln_size"]].notna().all(axis=1).sum()
    fm_sig = p90[["mom1", "ret_36_13", "ret_6_6", "ln_size"]].notna().all(axis=1).sum()
    print(f"  stocks with ALL 11 signals + ln_size non-null: {all_sig}")
    print(f"  stocks with Table-VI FM signals (mom1, ret_36_13, ret_6_6, "
          f"ln_size) non-null: {fm_sig}")
    print("  panel-wide signal null% (all months):")
    for c in sig_cols:
        print(f"    {c:<11s} {panel[c].isna().mean() * 100:6.2f}%")

    # IBM = CRSP permno 12490 (Compustat gvkey 006066). NOTE: permno 14593 is
    # APPLE INC (gvkey 001690) — an earlier draft mislabeled it as IBM.
    print("\n=== R6: IBM (permno 12490) ===")
    ibm = panel[panel["permno"] == 12490]
    if len(ibm):
        inds_1990s = ibm[(ibm["date"] >= "1990-01-01") &
                         (ibm["date"] <= "1995-07-31")]["ind"].unique()
        print(f"  IBM rows: {len(ibm)}, ind values in 1990-1995: "
              f"{sorted(inds_1990s)}")
        r = ibm[ibm["month"] == pd.Period("1994-06", "M")]
        if len(r):
            r = r.iloc[0]
            print(f"  IBM @ 1994-06: ind={r['ind']}, siccd={r['siccd']}, "
                  f"mom6={r['mom6']:.4f}, mom12={r['mom12']:.4f}, "
                  f"me=${r['me']:,.0f}")
        else:
            print("  IBM @ 1994-06: not in panel")
    else:
        print("  permno 12490 not in panel")

    # industry-level signal null rates over the sample
    print("\n=== extra: industry signal null% over "
          f"{SAMPLE_START}..{SAMPLE_END} ===")
    isig_cols = [c for c in ind_cols_out if c.startswith("ind_")
                 and c not in ("ind_ret_vw", "ind_ret_ew")]
    for c in isig_cols:
        print(f"    {c:<14s} {ind_samp[c].isna().mean() * 100:6.2f}%")
    print(f"  industry file: {len(ind)} rows; ind_ret_vw null: "
          f"{int(ind['ind_ret_vw'].isna().sum())} (of {len(ind)})")
    return 0


def main() -> int:
    """Orchestrate the two-stage pipeline.

    Stage 1 (CRSP, ~20 min) builds data/panel.parquet (41 cols) and is run only
    if the panel is missing or --rebuild is passed. Stage 2 (Compustat
    fundamentals + characteristic adjustments) always runs and is idempotent: it
    reads the 41-col panel, recomputes and overwrites the 7 enrichment columns
    (48 cols total), leaving every iteration-1 column untouched.
    """
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--rebuild",
        action="store_true",
        help="force re-run of the CRSP stage 1 even if data/panel.parquet exists",
    )
    args = ap.parse_args()

    LAYOUT.ensure()
    panel_path = LAYOUT.data_path("panel.parquet")
    if args.rebuild or not panel_path.exists():
        print(f"[stage 1] building CRSP panel "
              f"({'--rebuild' if args.rebuild else 'panel missing'}) ...")
        run_stage1()
    else:
        print(f"[stage 1] skipped — {panel_path.name} exists "
              f"(pass --rebuild to re-run the ~20 min CRSP stage)")

    print("[stage 2] enriching panel with Compustat fundamentals, r_sb, "
          "r_dgtw, beta ...")
    import add_fundamentals

    add_fundamentals.enrich_panel(panel_path)

    print("[stage 3] momentum-strategy engines + Tables I/II/III + plots ...")
    import tables_1_2_3

    tables_1_2_3.run()

    print("[stage 4] Table VI Fama-MacBeth regressions (Panels A-D) ...")
    import table_6

    table_6.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
