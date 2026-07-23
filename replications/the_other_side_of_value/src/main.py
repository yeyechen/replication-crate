"""
Replication of Novy-Marx (2013), "The Other Side of Value: The Gross
Profitability Premium".  Data pipeline stage.

Signal: GP/A = (REVT - COGS, fallback GP item) / AT — gross
profits-to-assets.  Sample July 1963 - December 2010, NYSE/AMEX/NASDAQ
ordinary common shares (shrcd 10/11, exchcd 1/2/3, PIT via dsenames),
financials (SIC 6xx) excluded.  Accounting data for fiscal year y is
used from the end of June y+1 (FF 1992 convention).

Targets: Table 2 — excess returns to portfolios sorted on gross
profits-to-assets (Panel A) and book-to-market (Panel B): quintile
sorts, NYSE breakpoints, annual June rebalancing, value-weighted,
FF3 time-series alphas, portfolio characteristics.

Produces data/panel.parquet — the analysis-ready monthly panel:
    permno, month, ret, me_crsp ($), prc, hexcd, hsiccd,
    r_1_0, r_12_2,                       <- CRSP monthly (SQL windows)
    fyear, gvkey, sich, at,
    gp_a, book_equity, earnings_be, fcf_be,   <- Compustat funda
    me_dec ($), bm, log_bm,              <- B/M with 6-month-lagged ME
    me_june ($), log_me                  <- formation-June ME (log $M)
plus data/ff_factors.parquet (Fama-French 4-factor + momentum, monthly).

SQL lives in src/sql/*.sql (executed via q_file).  The panel assembly
(fiscal-year mapping, CCM link, December/June ME joins, delisting
adjustment) is done in pandas — see src/sql/panel.sql for the
documented merge logic.
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# --- repo root on path so `utils` imports regardless of cwd ---
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from clickhouse_driver import Client  # noqa: E402
from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402

# ----------------------------------------------------------------------------
# Configuration (single source of truth: preparations/preprocessing_rules.json)
# ----------------------------------------------------------------------------
SLUG = "the_other_side_of_value"
LAYOUT = paper_layout(SLUG)
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")

RULES = json.loads(LAYOUT.preparations_path("preprocessing_rules.json").read_text())
_RULE_IDS = {r["rule_id"] for r in RULES}
_REQUIRED_RULES = {
    "universe_exclude_financials", "sample_period", "sample_fiscal_year_mapping",
    "sort_quintile_nyse_breaks", "sort_value_weighted", "winsorize_1pct_99pct",
    "var_gp_a", "var_book_equity", "var_bm", "var_earnings", "var_fcf",
    "fm_regression_spec",
}
_MISSING = _REQUIRED_RULES - _RULE_IDS
if _MISSING:
    print(f"[WARN] preprocessing_rules.json missing expected rule ids: {_MISSING}")

# Sample: July 1963 - December 2010 (rule: sample_period, L119).
SAMPLE_START = pd.Timestamp("1963-07-01")
SAMPLE_END = pd.Timestamp("2010-12-01")          # month-start label
# Universe (rule: universe_exclude_financials + standard CRSP filters).
SHRCD_FILTER = (10, 11)
EXCHCD_FILTER = (1, 2, 3)
# Analysis-stage parameters (documented here; not applied to the panel):
N_BINS = 5            # rule: sort_quintile_nyse_breaks (NYSE breakpoints, VW)
WINSORIZE_PCT = 0.01  # rule: winsorize_1pct_99pct — FM regressions ONLY

# ----------------------------------------------------------------------------
# ClickHouse connection
# ----------------------------------------------------------------------------
_CFG = get_clickhouse_config()


def _client() -> Client:
    return Client(host=_CFG["host"], port=int(_CFG["port"]),
                  user=_CFG["user"], password=_CFG["password"],
                  settings={"max_execution_time": 900})


def q(sql: str) -> pd.DataFrame:
    """Execute a SQL string, return a DataFrame."""
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    """Execute a saved SQL file from src/sql/, return a DataFrame."""
    sql = (SQL_DIR / name).read_text()
    print(f"[SQL] executing {name} ...", flush=True)
    df = q(sql)
    print(f"[SQL] {name}: {df.shape[0]:,} rows x {df.shape[1]} cols", flush=True)
    return df


# ----------------------------------------------------------------------------
# Component pulls (each = one SQL file under src/sql/)
# ----------------------------------------------------------------------------
def build_monthly() -> pd.DataFrame:
    """PIT-universe monthly returns with ME and r_1_0 / r_12_2 lags."""
    df = q_file("crsp_monthly.sql")
    df["month"] = pd.to_datetime(df["month"])
    df["permno"] = pd.to_numeric(df["permno"], errors="coerce").astype("int64")
    for col in ("ret", "me", "prc", "r_1_0", "r_12_2"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # Safety: dsenames windows can overlap for a few permnos -> dedup
    n_dup = int(df.duplicated(["permno", "month"]).sum())
    if n_dup:
        print(f"[WARN] dropping {n_dup:,} duplicate (permno, month) rows "
              f"from the msf x dsenames join")
        df = df.drop_duplicates(["permno", "month"], keep="first")
    return df.sort_values(["permno", "month"]).reset_index(drop=True)


def build_funda() -> pd.DataFrame:
    """Filtered annual fundamentals (GP/A, BE, earnings/BE, FCF/BE)."""
    df = q_file("compustat_funda.sql")
    df["datadate"] = pd.to_datetime(df["datadate"])
    for col in ("at", "gp_a", "book_equity", "earnings_be", "fcf_be"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def build_link() -> pd.DataFrame:
    """CCM link table (gvkey -> permno) with PIT windows."""
    df = q_file("ccm_link.sql")
    df["linkdt"] = pd.to_datetime(df["linkdt"], errors="coerce")
    df["linkenddt"] = pd.to_datetime(df["linkenddt"], errors="coerce")
    df["permno"] = pd.to_numeric(df["permno"], errors="coerce").astype("int64")
    return df


def build_ff() -> pd.DataFrame:
    """Fama-French four-factor + momentum, monthly (decimals)."""
    df = q_file("ff_factors.sql")
    df["month"] = pd.to_datetime(df["month"])
    for col in ("mkt_rf", "smb", "hml", "rf", "mom"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


# ----------------------------------------------------------------------------
# Delisting adjustment (paper silent -> standard CRSP convention,
# preprocessing rule "delisting_paper_silent")
# ----------------------------------------------------------------------------
_DELIST_SQL = """
    SELECT permno, dlstcd, toDate32(dlstdt) AS dlstdt, dlret
    FROM crsp_202601.dsedelist
    WHERE permno IS NOT NULL AND dlstcd IS NOT NULL
    SETTINGS max_execution_time = 120
"""


def build_delist() -> pd.DataFrame:
    dl = q(_DELIST_SQL)
    dl["dlret"] = pd.to_numeric(dl["dlret"], errors="coerce")
    # sentinels (-44/-55/-66/-77/-88/-99, i.e. < -1) -> missing;
    # -1.0 ("worthless") is a valid return and is kept
    dl.loc[dl["dlret"] < -1.0, "dlret"] = np.nan
    dl = dl.dropna(subset=["dlstcd"]).copy()
    return dl


def apply_delist_returns(monthly: pd.DataFrame) -> pd.DataFrame:
    # Per assumptions.md Assumption 1 (Replicator): use dlret when
    # available; NO imputation for missing dlret.
    dl = build_delist()
    dl["dlstdt"] = pd.to_datetime(dl["dlstdt"], errors="coerce")
    dl = dl.dropna(subset=["dlstdt"])
    # only in-sample delistings (a stock still trading at the sample end
    # has its last in-sample month in Dec 2010 — its later delisting
    # return must NOT be folded into that month)
    dl = dl[dl["dlstdt"] <= SAMPLE_END + pd.offsets.MonthEnd(1)]
    dl["dlret_use"] = dl["dlret"]
    dl = dl.dropna(subset=["dlret_use"])
    if dl.empty:
        return monthly
    # one delisting event per permno (the last)
    dl = dl.sort_values("dlstdt").groupby("permno", as_index=False).tail(1)
    dl["dlmonth"] = dl["dlstdt"].dt.to_period("M").dt.to_timestamp()

    monthly = monthly.merge(dl[["permno", "dlret_use", "dlmonth"]],
                            on="permno", how="left")
    last_month = monthly.groupby("permno")["month"].transform("max")
    is_last = monthly["month"] == last_month
    # apply only when the delisting event coincides with the stock's last
    # monthly row (delisting month, or the month right after the last
    # traded month — CRSP sometimes ends the msf record one month early)
    prev_month = monthly["dlmonth"] - pd.DateOffset(months=1)
    match = is_last & monthly["dlret_use"].notna() & (
        (last_month == monthly["dlmonth"]) | (last_month == prev_month)
    )
    r = monthly["ret"]
    adj = (1 + r.fillna(0)) * (1 + monthly["dlret_use"]) - 1
    monthly.loc[match & r.notna(), "ret"] = adj[match & r.notna()]
    monthly.loc[match & r.isna(), "ret"] = monthly.loc[match & r.isna(), "dlret_use"]
    n_adj = int(match.sum())
    n_last = int(is_last.sum())
    print(f"[DELIST] adjusted last-month return for {n_adj:,} of {n_last:,} "
          f"terminal permnos (dlret used where available, no imputation "
          f"per assumptions.md #1; delistings after {SAMPLE_END.date()} "
          f"excluded)")
    return monthly.drop(columns=["dlret_use", "dlmonth"])


# ----------------------------------------------------------------------------
# Panel assembly (steps M1-M6 documented in src/sql/panel.sql)
# ----------------------------------------------------------------------------
def assemble_panel(monthly: pd.DataFrame, funda: pd.DataFrame,
                   link: pd.DataFrame) -> pd.DataFrame:
    # ---- M1: temporal CCM link (linkdt <= datadate <= linkenddt) ----
    m = funda.merge(link, on="gvkey", how="inner")
    n_pre = len(m)
    m = m[(m["datadate"] >= m["linkdt"]) & (m["datadate"] <= m["linkenddt"])]
    print(f"[LINK] funda x link: {n_pre:,} -> {len(m):,} rows after temporal filter")

    # ---- M2: one firm-year per (permno, calyear) — keep largest AT ----
    m = m.sort_values("at").drop_duplicates(["permno", "calyear"], keep="last")
    annual = m.drop(columns=["datadate", "linkdt", "linkenddt"])
    print(f"[LINK] firm-years after (permno, calyear) dedup: {len(annual):,}")

    # ---- M3: B/M with December-t ME (6-month-lagged) ----
    dec = monthly.loc[monthly["month"].dt.month == 12,
                      ["permno", "month", "me"]].copy()
    dec["calyear"] = dec["month"].dt.year
    dec = dec.rename(columns={"me": "me_dec"}).drop(columns=["month"])
    annual = annual.merge(dec, on=["permno", "calyear"], how="left")
    # BE in $M (Compustat native); ME in $ -> convert ME to $M.
    # Negative/zero book equity -> B/M undefined (excluded from B/M).
    annual["bm"] = np.where(
        (annual["book_equity"] > 0) & (annual["me_dec"] > 0),
        annual["book_equity"] / (annual["me_dec"] / 1e6),
        np.nan,
    )
    annual["log_bm"] = np.log(annual["bm"])

    # ---- M5 source: formation-June ME ----
    jun = monthly.loc[monthly["month"].dt.month == 6,
                      ["permno", "month", "me"]].copy()
    jun["fyr"] = jun["month"].dt.year
    jun = jun.rename(columns={"me": "me_june"}).drop(columns=["month"])

    # ---- M4: fiscal-year -> holding period mapping ----
    # accounting data for fiscal year y is used July y+1 - June y+2
    panel = monthly[(monthly["month"] >= SAMPLE_START)
                    & (monthly["month"] <= SAMPLE_END)].copy()
    yr = panel["month"].dt.year
    mo = panel["month"].dt.month
    panel["calyear_used"] = np.where(mo >= 7, yr - 1, yr - 2)   # M4
    panel["fyr"] = np.where(mo >= 7, yr, yr - 1)                # M5 formation yr

    ann_cols = ["permno", "calyear", "fyear", "gvkey", "sich", "at",
                "gp_a", "book_equity", "earnings_be", "fcf_be",
                "me_dec", "bm", "log_bm"]
    panel = panel.merge(annual[ann_cols], how="left",
                        left_on=["permno", "calyear_used"],
                        right_on=["permno", "calyear"])
    panel = panel.merge(jun, on=["permno", "fyr"], how="left")
    panel["log_me"] = np.where(panel["me_june"] > 0,
                               np.log(panel["me_june"] / 1e6), np.nan)
    panel = panel.drop(columns=["calyear_used", "calyear", "fyr"])
    panel = panel.rename(columns={"me": "me_crsp"})

    cols = ["permno", "month", "ret", "me_crsp", "prc", "hexcd", "hsiccd",
            "r_1_0", "r_12_2", "fyear", "gvkey", "sich", "at", "gp_a",
            "book_equity", "earnings_be", "fcf_be", "me_dec", "bm",
            "log_bm", "me_june", "log_me"]
    return panel[cols].sort_values(["permno", "month"]).reset_index(drop=True)


# ----------------------------------------------------------------------------
# Diagnostics
# ----------------------------------------------------------------------------
def _stats(s: pd.Series) -> dict:
    s = s.dropna()
    return dict(n=int(s.shape[0]), mean=float(s.mean()),
                median=float(s.median()), std=float(s.std()),
                min=float(s.min()), max=float(s.max()))


def print_diagnostics(panel: pd.DataFrame, funda: pd.DataFrame) -> None:
    print("\n" + "=" * 72)
    print("Novy-Marx (2013) — panel diagnostics")
    print("=" * 72)
    months = panel["month"].nunique()
    print(f"Panel dimensions : {panel.shape[0]:,} rows x {panel.shape[1]} cols")
    print(f"Columns          : {list(panel.columns)}")
    print(f"Months           : {months} "
          f"({panel['month'].min().date()} .. {panel['month'].max().date()})")
    print(f"Unique permnos   : {panel['permno'].nunique():,}")
    print(f"Avg obs/month    : {panel.shape[0] / months:,.1f}")

    print("\n-- Signal summary stats (non-missing rows) --")
    for col in ("gp_a", "bm", "log_bm", "log_me", "earnings_be", "fcf_be",
                "r_1_0", "r_12_2"):
        st = _stats(panel[col])
        print(f"  {col:<12} N={st['n']:>9,}  mean={st['mean']:>9.4f}  "
              f"median={st['median']:>9.4f}  std={st['std']:>9.4f}  "
              f"min={st['min']:>10.4f}  max={st['max']:>12.4f}")

    print("\n-- Coverage (% of panel rows non-missing) --")
    for col in ("gp_a", "bm", "log_me", "r_1_0", "r_12_2", "earnings_be",
                "fcf_be"):
        cov = 100.0 * panel[col].notna().mean()
        print(f"  {col:<12} {cov:6.2f}%")

    # June-formation cross-sections (FM-regression sample proxy: July rows
    # carry the formation variables; report both June and July counts).
    june = panel[panel["month"].dt.month == 6]
    july = panel[panel["month"].dt.month == 7]
    print("\n-- Formation cross-sections (avg stocks with non-missing signal) --")
    print(f"  June rows with gp_a : "
          f"{june['gp_a'].notna().groupby(june['month']).sum().mean():,.0f}")
    print(f"  July rows with gp_a : "
          f"{july['gp_a'].notna().groupby(july['month']).sum().mean():,.0f}")

    print("\n-- Compustat firm-years (compustat_funda.sql output) --")
    print(f"  total firm-years         : {len(funda):,}")
    print(f"  with non-missing gp_a    : {int(funda['gp_a'].notna().sum()):,}")
    print(f"  with book_equity > 0     : "
          f"{int((funda['book_equity'] > 0).sum()):,}")
    print(f"  with non-missing fcf_be  : {int(funda['fcf_be'].notna().sum()):,}")

    # single-firm sanity check: IBM (gvkey 006066), fiscal 2009
    ibm = funda[(funda["gvkey"] == "006066") & (funda["calyear"] == 2009)]
    if not ibm.empty:
        r = ibm.iloc[0]
        print("\n-- Sanity check: IBM (gvkey 006066), fiscal year ending 2009 --")
        print(f"  at={r['at']:,.0f}  gp_a={r['gp_a']:.4f}  "
              f"book_equity={r['book_equity']:,.0f}  "
              f"earnings_be={r['earnings_be']:.4f}")
        p = panel[(panel["gvkey"] == "006066")
                  & (panel["month"] == pd.Timestamp("2010-07-01"))]
        if not p.empty:
            pr = p.iloc[0]
            print(f"  panel 2010-07 (permno {pr['permno']}): gp_a={pr['gp_a']:.4f}  "
                  f"bm={pr['bm']:.4f}  log_bm={pr['log_bm']:.4f}  "
                  f"log_me={pr['log_me']:.4f}  "
                  f"me_crsp=${pr['me_crsp']/1e9:,.1f}bn  "
                  f"me_dec=${pr['me_dec']/1e9:,.1f}bn")
    print("=" * 72)


# ----------------------------------------------------------------------------
# Table 2 — excess returns to portfolios sorted on profitability (Panel A,
# GP/A) and book-to-market (Panel B, B/M).
#
# Methodology (rules: sort_quintile_nyse_breaks L652, sort_value_weighted
# L329, sample_fiscal_year_mapping L119, factor_ff3 L329):
#   * Annual sorts at the end of June into N_BINS = 5 quintiles; quintile
#     breakpoints from NYSE stocks ONLY (hexcd == 1), applied to ALL stocks.
#   * The formation cross-section for the June-t sort is taken from the
#     July-t rows — the first month of holding year July t - June t+1 is
#     the row carrying fiscal-year t-1 accounting data, i.e. the data
#     available at the end of June t (assumptions.md Flag E: June rows
#     carry the PRIOR portfolio year's data, and no June-1963 row exists,
#     so literal June-row formation would both use stale signals and drop
#     the paper's first holding year).  A literal June-row variant is run
#     as a diagnostic below.
#   * Portfolios are NOT rebalanced monthly: membership fixed over the
#     12-month holding year.  Monthly returns are value-weighted with
#     PRIOR-MONTH market equity (me_crsp lagged one month — the standard
#     FF value-weighting convention: a cap-weighted index return is
#     defined on beginning-of-period weights).
#     ⚠️ Spec deviation (flagged in report + assumptions.md Flag I): the
#     task text said "me_crsp at each month" (contemporaneous).  Weights
#     dated t over the month-t return bias every portfolio UP by the
#     weighted cross-sectional return variance (+0.6-0.7%/mo here — a
#     mechanical ~+8%/yr), inflating every r^e and alpha while leaving
#     spreads/loadings intact.  Contemporaneous weights give Low r^e
#     0.99 / High 1.19 (paper: 0.31 / 0.62); prior-month weights give
#     0.30 / 0.62.  Prior-month is also the only reading consistent with
#     the paper's published values.  Where the lag is unavailable (a
#     stock's first panel month — July 1963 for all stocks since the
#     panel starts there, and each stock's IPO month) the weight falls
#     back to contemporaneous me_crsp.  The contemporaneous-weights
#     variant is preserved as a diagnostic in run_table2().
#   * Excess return = VW return - rf (ff.four_factor_monthly, DECIMALS).
#   * FF3 alpha: time-series OLS of monthly excess returns on
#     mkt_rf, smb, hml; plain OLS t-statistics (paper convention).
#   * Characteristics: time-series averages of monthly portfolio-level
#     GP/A (= Sum(GP)/Sum(AT)) and B/M (= Sum(BE)/Sum(ME), BE > 0 firms),
#     ME ($M, per-firm average), and number of firms (Flag J).
# ----------------------------------------------------------------------------
FF3_FACTORS = ("mkt_rf", "smb", "hml")
ROW_LABELS = ["Low", "2", "3", "4", "High"]

# Paper-reported values, Table 2 Panel A (task spec / L356-489).
PAPER_PANEL_A = {
    "Low":  {"re": 0.31, "alpha": -0.18, "mkt": 0.94, "smb": 0.04, "hml": 0.15,
             "gp_a": 0.10, "bm": 1.10, "me": 748.0, "n": 771.0},
    "2":    {"re": 0.41, "alpha": -0.11, "mkt": 1.03, "smb": -0.07, "hml": 0.20,
             "gp_a": 0.20, "bm": 0.98, "me": 1100.0, "n": 598.0},
    "3":    {"re": 0.52, "alpha": 0.02, "mkt": 1.02, "smb": -0.00, "hml": 0.12,
             "gp_a": 0.30, "bm": 1.00, "me": 1114.0, "n": 670.0},
    "4":    {"re": 0.41, "alpha": 0.05, "mkt": 1.01, "smb": 0.04, "hml": -0.24,
             "gp_a": 0.42, "bm": 0.53, "me": 1114.0, "n": 779.0},
    "High": {"re": 0.62, "alpha": 0.34, "mkt": 0.92, "smb": -0.04, "hml": -0.29,
             "gp_a": 0.68, "bm": 0.33, "me": 1096.0, "n": 938.0},
    "H-L":  {"re": 0.31, "alpha": 0.52, "mkt": -0.03, "smb": -0.08, "hml": -0.44},
    "H-L t": {"re": 2.49, "alpha": 4.49, "mkt": -0.99, "smb": -2.15, "hml": -10.8},
}
# Tier-1 tolerances (fraction of |paper value|), per tables_to_replicate.json.
TOL = {"re": 0.30, "alpha": 0.50, "mkt": 0.40, "smb": 0.40, "hml": 0.40,
       "gp_a": 0.30, "bm": 0.30, "me": 0.30, "n": 0.30}
TOL_TSTAT = 0.40


def _form_year(month: pd.Series) -> np.ndarray:
    """Formation year per month: July-Dec of year y and Jan-Jun of y+1
    both belong to the June-y formation (holding year Jul y - Jun y+1)."""
    return np.where(month.dt.month >= 7, month.dt.year, month.dt.year - 1)


def build_quintile_assignments(panel: pd.DataFrame, signal_col: str,
                               n_bins: int = N_BINS,
                               form_month: int = 7) -> pd.DataFrame:
    """Annual NYSE-breakpoint quintile assignments.

    form_month = 7 (default): formation cross-section = July-t rows (the
    rows carrying the FY t-1 data available at end of June t; first
    formation July 1963 covers the full sample).
    form_month = 6: literal June-t-row variant (stale FY t-2 data; first
    formation June 1964) — diagnostic only, see assumptions.md Flag E.
    """
    years = sorted(panel.loc[panel["month"].dt.month == form_month, "month"]
                   .dt.year.unique())
    frames = []
    for t in years:
        cs = panel[panel["month"] == pd.Timestamp(year=t, month=form_month, day=1)]
        cs = cs.dropna(subset=[signal_col])
        nyse = cs.loc[cs["hexcd"] == 1, signal_col]
        if nyse.shape[0] < 2 * n_bins:
            continue
        breaks = nyse.quantile(np.arange(1, n_bins) / n_bins).to_numpy()
        if not np.all(np.diff(breaks) > 0):
            continue                       # degenerate breakpoints
        q = np.searchsorted(breaks, cs[signal_col].to_numpy(), side="left") + 1
        frames.append(pd.DataFrame({"permno": cs["permno"].to_numpy(),
                                    "form_year": t, "q": q.astype(int)}))
    return pd.concat(frames, ignore_index=True)


def attach_portfolios(panel: pd.DataFrame, assigns: pd.DataFrame) -> pd.DataFrame:
    """Merge quintile assignments onto the holding-year stock-months.

    Adds me_w, the VW weight: me_crsp lagged one month (standard FF
    value-weighting — beginning-of-month weights). Falls back to
    contemporaneous me_crsp where the lag is unavailable (a stock's
    first panel month — July 1963 for every stock, and IPO months).
    """
    p = panel.sort_values(["permno", "month"]).copy()
    p["me_w"] = p.groupby("permno")["me_crsp"].shift(1)
    p["me_w"] = p["me_w"].fillna(p["me_crsp"])
    p["form_year"] = _form_year(p["month"])
    return p.merge(assigns, on=["permno", "form_year"], how="inner")


def vw_excess_returns(members: pd.DataFrame, ff_ms: pd.DataFrame,
                      weight_col: str = "me_w") -> pd.DataFrame:
    """Monthly VW excess returns per (month, q). Default weights:
    prior-month me_crsp (me_w); fixed membership, evolving weights."""
    ok = members.dropna(subset=["ret"])
    ok = ok[ok[weight_col] > 0]
    agg = (ok.assign(wret=ok["ret"] * ok[weight_col])
             .groupby(["month", "q"])
             .agg(num=("wret", "sum"), den=(weight_col, "sum"))
             .reset_index())
    agg["vw"] = agg["num"] / agg["den"]
    agg = agg.merge(ff_ms[["month", "rf"]], on="month", how="left")
    agg["re"] = agg["vw"] - agg["rf"]
    return agg[["month", "q", "vw", "re"]]


def portfolio_characteristics(members: pd.DataFrame) -> pd.DataFrame:
    """Monthly portfolio-level characteristics per (month, q), then
    time-series averaged downstream.

    GP/A and B/M are PORTFOLIO-LEVEL aggregates: GP/A = Sum(GP)/Sum(AT)
    (GP = gp_a * at, both $M) and B/M = Sum(book equity)/Sum(ME) over
    firms with book equity > 0 — the literal reading of "portfolio-level
    GP/A, B/M".  The aggregate convention reproduces the paper's Low
    quintile GP/A (0.10; the equal-weighted firm average is ~0.02
    because the Low quintile holds many microcaps with negative gross
    profits).  Alternative conventions are reported in the worker report
    for the Replicator (see assumptions.md Flag J).
    ME = per-firm average market equity ($M); n = number of member firms.
    """
    n = members.groupby(["month", "q"]).size().rename("n").reset_index()
    gpa_src = members.dropna(subset=["gp_a", "at"])
    gpa = (gpa_src.assign(gp=gpa_src["gp_a"] * gpa_src["at"])
           .groupby(["month", "q"]).agg(sgp=("gp", "sum"), sat=("at", "sum")))
    gpa["gp_a"] = gpa["sgp"] / gpa["sat"]
    bm_src = members[(members["book_equity"] > 0) & (members["me_crsp"] > 0)]
    bm = bm_src.groupby(["month", "q"]).agg(
        sbe=("book_equity", "sum"), sme=("me_crsp", "sum"))
    bm["bm"] = bm["sbe"] / (bm["sme"] / 1e6)
    me = (members[members["me_crsp"] > 0]
          .groupby(["month", "q"])["me_crsp"].mean() / 1e6).rename("me")
    chars = (n.set_index(["month", "q"])
             .join(gpa[["gp_a"]]).join(bm[["bm"]]).join(me)
             .reset_index())
    return chars


def ff3_time_series(excess: pd.Series, ff_ms: pd.DataFrame) -> dict:
    """OLS of monthly excess returns (decimals) on FF3 factors.
    Returns alpha in %/month, unitless loadings, plain OLS t-statistics."""
    import statsmodels.api as sm
    d = excess.to_frame("re").join(ff_ms.set_index("month"), how="inner").dropna()
    x = sm.add_constant(d[list(FF3_FACTORS)].astype(float))
    fit = sm.OLS(d["re"].astype(float), x).fit()
    out = {"nobs": int(fit.nobs), "r2": float(fit.rsquared),
           "alpha": float(fit.params["const"]) * 100.0,
           "alpha_t": float(fit.tvalues["const"])}
    for f in FF3_FACTORS:
        out[f] = float(fit.params[f])
        out[f"{f}_t"] = float(fit.tvalues[f])
    return out


def run_sort_panel(panel: pd.DataFrame, ff_ms: pd.DataFrame, signal_col: str,
                   form_month: int = 7, weight_col: str = "me_w") -> dict:
    """Full quintile-sort analysis for one signal (Table 2 panel).
    weight_col = "me_w" (prior-month ME, default) or "me_crsp"
    (contemporaneous ME — biased diagnostic variant)."""
    assigns = build_quintile_assignments(panel, signal_col, form_month=form_month)
    members = attach_portfolios(panel, assigns)
    vw = vw_excess_returns(members, ff_ms, weight_col=weight_col)
    chars = portfolio_characteristics(members)

    pivot = vw.pivot(index="month", columns="q", values="re").sort_index()
    spread = (pivot[N_BINS] - pivot[1]).dropna()
    regs = {q: ff3_time_series(pivot[q].dropna(), ff_ms)
            for q in range(1, N_BINS + 1)}
    return {
        "signal": signal_col,
        "form_month": form_month,
        "n_formations": int(assigns["form_year"].nunique()),
        "n_member_rows": int(len(members)),
        "n_months": int(pivot.shape[0]),
        "avg_form_size": float(assigns.groupby("form_year").size().mean()),
        "re": vw.groupby("q")["re"].mean() * 100.0,
        "hl_re": float(spread.mean() * 100.0),
        "hl_t": float(spread.mean()
                      / (spread.std(ddof=1) / np.sqrt(len(spread)))),
        "regs": regs,
        "hl_reg": ff3_time_series(spread, ff_ms),
        "chars": chars.groupby("q")[["gp_a", "bm", "me", "n"]].mean(),
    }


def _panel_rows(res: dict) -> dict:
    """Collect reporting-unit values per table row label."""
    out = {}
    for i, label in enumerate(ROW_LABELS, start=1):
        reg = res["regs"][i]
        out[label] = {"re": float(res["re"][i]), "alpha": reg["alpha"],
                      "mkt": reg["mkt_rf"], "smb": reg["smb"], "hml": reg["hml"],
                      "gp_a": float(res["chars"].loc[i, "gp_a"]),
                      "bm": float(res["chars"].loc[i, "bm"]),
                      "me": float(res["chars"].loc[i, "me"]),
                      "n": float(res["chars"].loc[i, "n"])}
    hl = res["hl_reg"]
    out["H-L"] = {"re": res["hl_re"], "alpha": hl["alpha"],
                  "mkt": hl["mkt_rf"], "smb": hl["smb"], "hml": hl["hml"]}
    out["H-L t"] = {"re": res["hl_t"], "alpha": hl["alpha_t"],
                    "mkt": hl["mkt_rf_t"], "smb": hl["smb_t"], "hml": hl["hml_t"]}
    return out


def format_panel_md(title: str, rows: dict) -> list:
    lines = [f"## {title}", "",
             "| Portfolio | r^e | alpha | MKT | SMB | HML | GP/A | B/M | ME($M) | n |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for label in ROW_LABELS:
        r = rows[label]
        lines.append(
            f"| {label} | {r['re']:.2f} | {r['alpha']:.2f} | {r['mkt']:.2f} | "
            f"{r['smb']:.2f} | {r['hml']:.2f} | {r['gp_a']:.2f} | {r['bm']:.2f} | "
            f"{r['me']:,.0f} | {r['n']:,.0f} |")
    h, t = rows["H-L"], rows["H-L t"]
    lines.append(f"| H-L | {h['re']:.2f} | {h['alpha']:.2f} | {h['mkt']:.2f} | "
                 f"{h['smb']:.2f} | {h['hml']:.2f} | | | | |")
    lines.append(f"| H-L t | [{t['re']:.2f}] | [{t['alpha']:.2f}] | "
                 f"[{t['mkt']:.2f}] | [{t['smb']:.2f}] | [{t['hml']:.2f}] | | | | |")
    return lines


def _tier(paper: float, ours: float, tol: float) -> tuple:
    """(tier, deviation string). Tier 1 within tol, Tier 2 sign match,
    FAIL sign wrong. Paper values ~0 handled by absolute closeness."""
    if abs(paper) < 0.005:
        if abs(ours) <= 0.05:
            return "Tier 1", f"{ours:+.3f} (paper ~0)"
        return "Tier 2", f"{ours:+.3f} (paper ~0)"
    dev = (ours - paper) / abs(paper)
    if abs(dev) <= tol:
        return "Tier 1", f"{dev * 100:+.1f}%"
    if (ours > 0) == (paper > 0):
        return "Tier 2", f"{dev * 100:+.1f}%"
    return "FAIL", f"{dev * 100:+.1f}%"


def compare_panel_a(ours_rows: dict) -> tuple:
    lines = ["| Row | Metric | Paper | Ours | Deviation | Tier |",
             "|---|---|---|---|---|---|"]
    counts = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0}
    for row, metrics in PAPER_PANEL_A.items():
        tol_map_t = TOL_TSTAT if row == "H-L t" else None
        for metric, paper_val in metrics.items():
            tol = tol_map_t if tol_map_t is not None else TOL[metric]
            our_val = ours_rows[row][metric]
            tier, dev = _tier(paper_val, our_val, tol)
            counts[tier] += 1
            lines.append(f"| {row} | {metric} | {paper_val:g} | "
                         f"{our_val:.3f} | {dev} | {tier} |")
    return "\n".join(lines), counts


def plot_quintile_bars(res: dict, save_to) -> None:
    """Bar chart of quintile VW excess returns, Table 2 Panel A."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    vals = [float(res["re"][q]) for q in range(1, N_BINS + 1)]
    hl = float(res["hl_re"])
    labels = ROW_LABELS + ["H-L"]
    x = np.arange(len(labels))
    colors = ["#4C72B0"] * N_BINS + ["#C44E52"]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(x, vals + [hl], color=colors, alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Quintile portfolio (sorted on gross profits-to-assets)")
    ax.set_ylabel("Average VW excess return (%/month)")
    ax.set_title("Novy-Marx (2013) Table 2, Panel A — "
                 "quintile VW excess returns (Jul 1963 – Dec 2010)")
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.grid(True, axis="y", alpha=0.3)
    for b, v in zip(bars, vals + [hl]):
        ax.annotate(f"{v:.2f}", (b.get_x() + b.get_width() / 2.0, v),
                    ha="center", va="bottom" if v >= 0 else "top", fontsize=9)
    fig.tight_layout()
    fig.savefig(save_to, dpi=150)
    plt.close(fig)


def run_table2(panel: pd.DataFrame, ff: pd.DataFrame) -> None:
    print("\n" + "=" * 72)
    print("Novy-Marx (2013) — Table 2: quintile sorts on GP/A and B/M")
    print("=" * 72)
    # FF factor months are month-end; align to the panel's month-start.
    ff_ms = ff.copy()
    ff_ms["month"] = ff_ms["month"].dt.to_period("M").dt.to_timestamp()

    res_a = run_sort_panel(panel, ff_ms, "gp_a", form_month=7)
    res_b = run_sort_panel(panel, ff_ms, "bm", form_month=7)

    for tag, res in (("A (GP/A)", res_a), ("B (B/M)", res_b)):
        print(f"[TABLE2] Panel {tag}: {res['n_formations']} formations "
              f"(avg {res['avg_form_size']:,.0f} stocks/form), "
              f"{res['n_months']} months, {res['n_member_rows']:,} "
              f"stock-months in portfolios")
        print(f"[TABLE2] Panel {tag} r^e (%/mo): "
              + "  ".join(f"{label}={float(res['re'][q]):.2f}"
                          for q, label in enumerate(ROW_LABELS, 1))
              + f"  H-L={res['hl_re']:.2f} (t={res['hl_t']:.2f})")

    # ---------- markdown table ----------
    rows_a, rows_b = _panel_rows(res_a), _panel_rows(res_b)
    md = [
        "# Table 2 — Excess returns to portfolios sorted on profitability "
        "and book-to-market",
        "",
        "Novy-Marx (2013), Table 2. Monthly value-weighted average excess "
        "returns (%/month) to quintile portfolios sorted on gross "
        "profits-to-assets (Panel A) and book-to-market (Panel B). NYSE "
        "breakpoints; annual rebalancing at the end of June; portfolios "
        "held July t – June t+1. Sample July 1963 – December 2010 "
        f"({res_a['n_months']} months). Alpha and factor loadings from "
        "time-series OLS of portfolio excess returns on the Fama-French "
        "three factors (MKT, SMB, HML); t-statistics in brackets. "
        "Characteristics are time-series averages of monthly portfolio-"
        "level values: GP/A = Sum(GP)/Sum(AT); B/M = Sum(book equity)/"
        "Sum(ME) (firms with positive book equity); ME = per-firm market "
        "equity in $millions; n = number of firms.",
        "",
    ]
    md += format_panel_md("Panel A: Portfolios sorted on gross profits-to-assets (GP/A)",
                          rows_a)
    md += ["", ]
    md += format_panel_md("Panel B: Portfolios sorted on book-to-market (B/M)",
                          rows_b)
    md += ["",
           "## Panel A vs paper (per-cell comparison)",
           "",
           "Tier 1 = within tolerance (returns 30%, alphas 50%, loadings "
           "and t-stats 40%, characteristics 30%); Tier 2 = correct sign "
           "but outside tolerance; FAIL = wrong sign.",
           ""]
    cmp_md, counts = compare_panel_a(rows_a)
    md += [cmp_md, "",
           f"**Summary: {counts['Tier 1']} Tier 1, {counts['Tier 2']} Tier 2, "
           f"{counts['FAIL']} FAIL (of {sum(counts.values())} cells).**", ""]
    out = LAYOUT.result_path("table_2.md")
    out.write_text("\n".join(md))
    print(f"[SAVE] {out}")

    # ---------- plot ----------
    png = LAYOUT.result_path("table2_decile_spread.png")
    plot_quintile_bars(res_a, png)
    print(f"[SAVE] {png}")

    # ---------- console comparison + diagnostic ----------
    print("\n-- Panel A vs paper --")
    print(cmp_md)
    print(f"[TABLE2] Panel A comparison: {counts}")

    diag = run_sort_panel(panel, ff_ms, "gp_a", form_month=6)
    print("\n-- DIAGNOSTIC: literal June-row formation (stale FY t-2 signal, "
          "first formation June 1964) --")
    print(f"[TABLE2-DIAG] {diag['n_formations']} formations, "
          f"{diag['n_months']} months")
    print("[TABLE2-DIAG] r^e (%/mo): "
          + "  ".join(f"{label}={float(diag['re'][q]):.2f}"
                      for q, label in enumerate(ROW_LABELS, 1))
          + f"  H-L={diag['hl_re']:.2f} (t={diag['hl_t']:.2f})")

    diag_w = run_sort_panel(panel, ff_ms, "gp_a", form_month=7,
                            weight_col="me_crsp")
    print("\n-- DIAGNOSTIC: contemporaneous me_crsp weights (literal spec "
          "wording; biased +cross-sectional variance, see Flag I) --")
    print("[TABLE2-DIAG] r^e (%/mo): "
          + "  ".join(f"{label}={float(diag_w['re'][q]):.2f}"
                      for q, label in enumerate(ROW_LABELS, 1))
          + f"  H-L={diag_w['hl_re']:.2f} (t={diag_w['hl_t']:.2f}), "
          + "alphas: "
          + "  ".join(f"{label}={diag_w['regs'][q]['alpha']:.2f}"
                      for q, label in enumerate(ROW_LABELS, 1)))
    print("=" * 72)


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------
def main() -> None:
    panel_path = LAYOUT.data_path("panel.parquet")
    ff_path = LAYOUT.data_path("ff_factors.parquet")
    if "--rebuild" in sys.argv or not (panel_path.exists() and ff_path.exists()):
        monthly = build_monthly()
        funda = build_funda()
        link = build_link()
        ff = build_ff()

        # M6: delisting adjustment on the full monthly universe (pre-panel)
        monthly = apply_delist_returns(monthly)

        panel = assemble_panel(monthly, funda, link)

        panel.to_parquet(panel_path, index=False)
        print(f"\n[SAVE] {panel_path}  ({panel.shape[0]:,} rows)")

        ff.to_parquet(ff_path, index=False)
        print(f"[SAVE] {ff_path}  ({ff.shape[0]:,} months, "
              f"{ff['month'].min().date()} .. {ff['month'].max().date()})")

        print_diagnostics(panel, funda)
    else:
        print("[CACHE] loading existing data/panel.parquet + "
              "data/ff_factors.parquet (pass --rebuild to re-extract)")
        panel = pd.read_parquet(panel_path)
        ff = pd.read_parquet(ff_path)

    run_table2(panel, ff)


if __name__ == "__main__":
    main()
