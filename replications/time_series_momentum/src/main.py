"""
Replication of Moskowitz, Ooi, Pedersen (2012) "Time Series Momentum",
JFE 104: 228-250 — DATA PIPELINE stage.

Builds data/panel.parquet with columns:
    instrument, asset_class, month (month-end date), ret, sigma, n_days

Definitions (per preparations/preprocessing_rules.json and the task spec):
  * ret   : monthly EXCESS return. Daily futures return compounded over the
            trading days of the month, with daily excess return
                (1 + r_fut) / (1 + rf_daily) - 1
            where rf_daily = (1 + rf_monthly)^(1/n_trading_days_in_month) - 1,
            rf_monthly = ff.four_factor_monthly.rf (US 1-month T-bill,
            assumption A1; already stored as a DECIMAL in ClickHouse — do not
            divide by 100), and n_trading_days_in_month = the instrument's
            own number of daily observations in that month (panel n_days).
  * sigma : ex ante annualized volatility, Eq. (1). EWMA of daily excess
            returns with delta = 60/61 (center of mass 60 days):
                m_t = delta*m_{t-1} + (1-delta)*r_{t-1}
                v_t = delta*v_{t-1} + (1-delta)*(r_{t-1} - m_{t-1})^2
                sigma_t = sqrt(261 * v_t)
            initialized with the mean/variance of the first 120 daily excess
            returns (burn-in; months before burn-in completes are dropped).
            LAGGED ONE MONTH: the sigma attached to month t is the sigma at
            the last trading day of month t-1 (var_vol_lag_one).
  * n_days: trading days in the month with settlement data.

Universe: 58 instruments (24 commodities, 9 equity indexes, 13 bond futures,
12 currency pairs). Each instrument maps to ONE Datastream continuous calc
series (wrds_cseries_info: positionfwddesc='First'; roll method among the four
single-contract roll conventions) selected for longest 1985-2009 coverage
(assumption A4) — see data/instrument_map.csv. Where the front-contract series
migrated venue/product without a gap (e.g., DTB -> EUREX Bund, IPE -> ICE gas
oil, unleaded -> RBOB, DEM -> euro futures per the paper's "Germany spliced
with the Euro"), legs are spliced with back-adjustment; where no acceptable
continuous futures series exists for part of the window (gold 2000-2009,
silver 2002-2009, NOK 2008-2009), the longest-coverage single series is used
and the gap is logged. Bonds are UNSCALED (assumption A5: no duration field
available in wrds_fut_series; life = days-to-expiry, not duration).
"""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# --- project plumbing ---------------------------------------------------
_SRC_DIR = Path(__file__).resolve().parent
_SLUG_ROOT = _SRC_DIR.parent
_PROJECT_ROOT = _SLUG_ROOT.parents[1]
sys.path.insert(0, str(_PROJECT_ROOT))

from clickhouse_driver import Client  # noqa: E402

from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402

LAYOUT = paper_layout("time_series_momentum")
SQL_DIR = LAYOUT.src_path("sql")

# --- configuration (task spec + Table 1 of the paper) -------------------
DELTA = 60.0 / 61.0          # EWMA decay; center of mass delta/(1-delta) = 60 days
BURN_IN = 120                # days used to initialize the EWMA variance/mean
ANNUALIZE = 261.0            # trading days per year (paper Eq. 1)
PULL_START = "1964-01-01"    # series start (CAD/GBP futures begin 1972)
PULL_END = "2010-03-31"      # a few months past 2009-12-31 is harmless
PANEL_END = pd.Timestamp("2009-12-31")

# legs: (calcseriescode, last date used (inclusive), or None for the final leg).
# Multiple legs = venue/product migration splice, back-adjusted at each joint.
# paper_stats: (annualized mean %, annualized vol %) from Table 1 (None if the
# extracted table is truncated there).
INSTRUMENTS: dict[str, dict] = {
    # ---------------- commodities (24) ----------------
    "ALUMINUM":  dict(asset_class="commodity", paper_start="Jan-79", paper_stats=(0.97, 23.50),
                      legs=[(11895, None)],
                      notes="LME aluminium front; series starts 1993-07-12 (paper Jan-79 used LME spot splice, not replicable per A3)"),
    "BRENTOIL":  dict(asset_class="commodity", paper_start="Apr-89", paper_stats=(13.87, 32.51),
                      legs=[(12984, None)],
                      notes="ICE Brent crude; starts 1988-12-07 (paper Apr-89)"),
    "CATTLE":    dict(asset_class="commodity", paper_start="Jan-65", paper_stats=(4.52, 17.14),
                      legs=[(370, None)],
                      notes="CME live cattle; data 1979-01-02 -> 2015-07-10 (paper Jan-65 spliced)"),
    "COCOA":     dict(asset_class="commodity", paper_start="Jan-65", paper_stats=(5.61, 32.38),
                      legs=[(275, None)],
                      notes="CSCE (ICE) cocoa; data from 1979-01-02"),
    "COFFEE":    dict(asset_class="commodity", paper_start="Mar-74", paper_stats=(5.72, 38.62),
                      legs=[(9560, None)],
                      notes="CSCE (ICE) coffee C; data from 1979-01-02"),
    "COPPER":    dict(asset_class="commodity", paper_start="Jan-77", paper_stats=(8.90, 27.39),
                      legs=[(5937, None)],
                      notes="LME copper; starts 1993-07-12 (paper Jan-77 spliced)"),
    "CORN":      dict(asset_class="commodity", paper_start="Jan-65", paper_stats=(-3.19, 24.37),
                      legs=[(6162, None)],
                      notes="CBT corn; data 1979-01-04 -> 2015-07-10"),
    "COTTON":    dict(asset_class="commodity", paper_start="Aug-67", paper_stats=(1.41, 24.35),
                      legs=[(8697, None)],
                      notes="CSCE (ICE) cotton #2; data from 1979-01-02. Roll-quality diagnosis: only 4 one-day >10% moves 1995-2009, all genuine price spikes (1995-07-05, 2001-06-25, 2003-03-03, 2009-07-01), not contract conversions; VOL/WVOL variants offer no artifact removal (-1.5pp vol at the cost of 1979-1994 coverage), so CS00 kept"),
    "CRUDE":     dict(asset_class="commodity", paper_start="Mar-83", paper_stats=(11.61, 34.72),
                      legs=[(28020, None)],
                      notes="NYMEX (NYM) WTI light crude TRc1 (nearest w/ switch after last trading day); starts 1983-03-30, matches paper Mar-83; no plain-CS00 NYMEX WTI series exists in the catalog"),
    "GASOIL":    dict(asset_class="commodity", paper_start="Oct-84", paper_stats=(11.95, 33.18),
                      legs=[(11363, "2003-09-05"), (769, None)],
                      notes="Splice IPE gas oil (1981-04-06 -> 2003-09-05) -> ICE gas oil (2003-09-08 -> ); identical settlements in overlap, back-adjusted"),
    "GOLD":      dict(asset_class="commodity", paper_start="Dec-69", paper_stats=(5.36, 21.37),
                      legs=[(716, "1983-04-11"), (3581, "2002-05-06"), (16416, None)],
                      notes="3-leg splice across the COMEX delivery hole (no COMEX series is contiguous 1986->2026): CME-GOLD 100 OZ (USD/oz, -> 1983-04-11) -> CBT-GOLD 1 KILOGRAM (USD/kg, 1983-04-12 -> 2002-05-06) -> TOCOM-GOLD TRc3/VOL (JPY/gram, 1986-06-27 -> , used from 2002-05-07); back-adjusted for level continuity at each joint. Post-2002-05 returns embed USDJPY drift (yen/gram vs USD/oz); cross-joint 12-month returns are approximate"),
    "HEATOIL":   dict(asset_class="commodity", paper_start="Dec-78", paper_stats=(9.79, 33.78),
                      legs=[(18328, None)],
                      notes="NYMEX NY Harbor ULSD TRc3 (= heating oil, renamed; roll = 'switch over when 2nd month volume exceeds 1st'); starts 1980-01-02. Chosen over TRc1/LTDT (35 one-day >10% roll gaps 1980-2009): TRc3 has 4; WVOL TRc2 has 11. ICE-HEATING OIL series only starts 2006-04-21"),
    "HOGS":      dict(asset_class="commodity", paper_start="Feb-66", paper_stats=(3.39, 26.01),
                      legs=[(8646, None)],
                      notes="CME lean hogs (incl. predecessor live hogs); data 1979-01-02 -> 2015-07-10. Roll-quality diagnosis: first-of-month/conversion jumps (1996-12-02, 1998-12-01, 1999-04-01, 2002-08-01, ...) persist in the WVOL/VOL variants too (WVOL vol identical 37.1%, VOL has MORE >10% days); kept CS00 to retain 1979-1994 coverage"),
    "NATGAS":    dict(asset_class="commodity", paper_start="Apr-90", paper_stats=(-9.74, 53.30),
                      legs=[(18339, None)],
                      notes="NYMEX natural gas TRc3 (roll = 'switch over when 2nd month volume exceeds 1st'); starts 1990-04-03, matches paper Apr-90. Chosen over TRc1/LTDT after diagnosis: 12 one-day >15% discontinuities 1990-2009 vs 26 for LTDT (no WVOL variant exists). Selected on roll quality, not closeness to the paper mean"),
    "NICKEL":    dict(asset_class="commodity", paper_start="Jan-93", paper_stats=(12.69, 35.76),
                      legs=[(1514, None)],
                      notes="LME nickel; starts 1993-07-12 (paper Jan-93)"),
    "PLATINUM":  dict(asset_class="commodity", paper_start="Jan-92", paper_stats=(13.15, 20.95),
                      legs=[(16698, None)],
                      notes="TOCOM platinum (JPLCS00); starts 1984-01-26"),
    "SILVER":    dict(asset_class="commodity", paper_start="Jan-65", paper_stats=(3.17, 31.11),
                      legs=[(5277, "1989-12-26"), (5727, "2001-07-30"), (11171, None)],
                      notes="3-leg splice: CBT-SILVER 1000 OZ (1981-06-25 -> 1989-12-26, extends front; same $/oz quote as the 5000 oz contract) -> CBT-SILVER 5000 OZ (-> 2001-07-30) -> NYL-SILVER 5000 OZ VOL (2004-10-06 ->); back-adjusted for level continuity at each joint. The 2001-08 -> 2004-10 delivery hole is UNBRIDGEABLE: the actual price move over those 29 months is LOST (joint back-adjusted to continuity)"),
    "SOYBEANS":  dict(asset_class="commodity", paper_start="Jan-65", paper_stats=(5.57, 27.26),
                      legs=[(2912, None)],
                      notes="CBT soybeans; data 1979-01-02 -> 2015-07-02"),
    "SOYMEAL":   dict(asset_class="commodity", paper_start="Sep-83", paper_stats=(6.14, 24.59),
                      legs=[(2249, None)],
                      notes="CBT soybean meal; data 1979-01-02 -> 2015-07-10"),
    "SOYOIL":    dict(asset_class="commodity", paper_start="Oct-90", paper_stats=(1.07, 25.39),
                      legs=[(13331, None)],
                      notes="CBT soybean oil; data 1979-01-02 -> 2015-07-10"),
    "SUGAR":     dict(asset_class="commodity", paper_start="Jan-65", paper_stats=(4.44, 42.87),
                      legs=[(3238, None)],
                      notes="CSCE (ICE) sugar #11; data from 1979-01-02"),
    "UNLEADED":  dict(asset_class="commodity", paper_start="Dec-84", paper_stats=(15.92, 37.36),
                      legs=[(2494, "2006-12-28"), (18146, None)],
                      notes="Splice per paper 'RBOB spliced with Unleaded': NYM NY unleaded gasoline WVOL (1995-01-03 -> 2006-12-28) -> NYMEX RBOB gasoline WVOL TRc2 (2007-01-02 -> ); back-adjusted at joint. Roll-quality diagnosis: WVOL removes the first-of-month roll gaps (4 one-day >10% moves 1985-2009, all genuine events, vs 40 for CS00); cost: the CS00-only 1984-1994 history is dropped (series starts 1995-01)"),
    "WHEAT":     dict(asset_class="commodity", paper_start="Jan-65", paper_stats=(-1.84, 25.11),
                      legs=[(10511, None)],
                      notes="CBT wheat; data 1978-01-05 -> 2015-07-02"),
    "ZINC":      dict(asset_class="commodity", paper_start="Jan-91", paper_stats=(1.98, 24.76),
                      legs=[(10437, None)],
                      notes="LME zinc; starts 1993-07-12 (paper Jan-91 spliced)"),
    # ---------------- equity indexes (9) ----------------
    "SPI200":    dict(asset_class="equity", paper_start="Jan-77", paper_stats=(7.25, 18.33),
                      legs=[(2089, None)],
                      notes="SFE SPI 200 weighted-volume roll variant (AAPCS02): the plain CS00 variant (AAPCS00) has no data before 2023-11; starts 2000-05-02 (paper Jan-77 spliced to MSCI)"),
    "CAC40":     dict(asset_class="equity", paper_start="Jan-75", paper_stats=(6.73, 20.87),
                      legs=[(9796, "1999-01-07"), (11049, None)],
                      notes="Splice MATIF CAC 40 (1988-10-03 -> 1999-01-07) -> MONEP CAC 40 (1999-01-08 -> )"),
    "DAX":       dict(asset_class="equity", paper_start="Jan-75", paper_stats=(6.33, 20.41),
                      legs=[(7187, None)],
                      notes="EUREX DAX; starts 1990-11-23 (paper Jan-75 spliced)"),
    "FTSE100":   dict(asset_class="equity", paper_start="Jan-75", paper_stats=(6.97, 17.77),
                      legs=[(568, None)],
                      notes="LIFFE FTSE 100; starts 1984-05-03 (FTSE 100 futures listing)"),
    "AEX":       dict(asset_class="equity", paper_start="Jan-75", paper_stats=(7.72, 19.18),
                      legs=[(5225, None)],
                      adjust=[("1996-06-19", 559.9299 / 256.3450),    # quote-scale change, +118% raw jump
                              ("1998-12-01", 475.3347 / 1100.2698)],  # guilder->euro redenomination, -57% raw jump
                      notes="AEX index futures; starts 1988-10-25; two quote-scale jumps (1996-06-19 contract re-spec, 1998-12-01 guilder->euro) back-adjusted for continuity"),
    "IBEX35":    dict(asset_class="equity", paper_start="Jan-80", paper_stats=(9.37, 21.84),
                      legs=[(12744, None)],
                      notes="MEFF 'IBEX 35 PLUS' (MBXCS00) — the only standard-size IBEX 35 continuous series in the catalog (no plain 'IBEX 35 INDEX'); starts 1992-04-20 (MEFF listing)"),
    "FTSEMIB":   dict(asset_class="equity", paper_start="Jun-78", paper_stats=(6.13, 24.59),
                      legs=[(7345, "2004-03-19"), (12663, None)],
                      notes="Splice MIF MIB 30 (1994-11-28 -> 2004-03-19) -> IDEM FTSE MIB (2004-03-22 -> ), the Italian index future's own migration"),
    "TOPIX":     dict(asset_class="equity", paper_start="Jul-76", paper_stats=(2.29, 18.66),
                      legs=[(9692, None)],
                      notes="OSE (OSX) TOPIX; starts 1988-09-05 (TOPIX futures listing)"),
    "SP500":     dict(asset_class="equity", paper_start="Jan-65", paper_stats=(3.47, 15.45),
                      legs=[(12144, None)],
                      notes="CME S&P 500 (ISPCS00); data 1982-04-23 -> 2025-12-19; anchor verified: settlement 1401.0 on 2000-01-31"),
    # ---------------- bond futures (13; UNSCALED per A5) ----------------
    "AUS3Y":     dict(asset_class="bond", paper_start="Jan-92", paper_stats=(1.34, 2.57),
                      legs=[(54, None)],
                      notes="SFE Australian 3y treasury bond (ATYCS01 LTDT variant: plain CS00 ATYCS00 has no data before 2023-11); starts 1988-05-17; UNSCALED (A5)"),
    "AUS10Y":    dict(asset_class="bond", paper_start="Dec-85", paper_stats=(3.83, 8.53),
                      legs=[(29408, None)],
                      notes="SFE Australian 10y treasury bond DAY session (AGDCS00): the AGB* 10y series have no data before 2023-11; starts 1984-12-05; UNSCALED (A5)"),
    "EURO2Y":    dict(asset_class="bond", paper_start="Mar-97", paper_stats=(1.02, 1.53),
                      legs=[(772, None)],
                      notes="EUREX Euro-Schatz; starts 1998-10-05 (paper Mar-97 = DTB Schatz GTBCS00 1997-03 -> 1999-12, shorter coverage); UNSCALED (A5)"),
    "EURO5Y":    dict(asset_class="bond", paper_start="Jan-93", paper_stats=(2.56, 3.22),
                      legs=[(3555, "1998-10-02"), (5833, None)],
                      notes="Splice DTB Bobl (1991-10-04 -> 1998-10-02) -> EUREX Euro-Bobl (1998-10-05 -> ); UNSCALED (A5)"),
    "EURO10Y":   dict(asset_class="bond", paper_start="Dec-79", paper_stats=(2.40, 5.74),
                      legs=[(12272, "1998-10-02"), (2970, None)],
                      notes="Splice DTB Bund (1990-11-23 -> 1998-10-02) -> EUREX Euro-Bund (1998-10-05 -> ); UNSCALED (A5)"),
    "EURO30Y":   dict(asset_class="bond", paper_start="Dec-98", paper_stats=(4.71, 11.70),
                      legs=[(3014, "2005-09-08"), (6928, None)],
                      notes="Splice EUREX Euro-Buxl DEAD (1998-10-02 -> 2005-09-08) -> Euro-Buxl live (2005-09-09 -> ); UNSCALED (A5)"),
    "CAN10Y":    dict(asset_class="bond", paper_start="Dec-84", paper_stats=(4.04, 7.36),
                      legs=[(12515, None)],
                      adjust=[("1989-10-06", 96.61 / 79.5389),   # quote-scale change, +21.5% raw jump
                              ("1999-05-21", 123.65 / 102.5797)], # quote-scale change, +20.5% raw jump
                      notes="Montreal Exchange (ME) 10y Canadian govt bond; starts 1989-09-15 (CBT Canadian govt bond series is a 1994-1995 stub only); two quote-scale jumps back-adjusted; UNSCALED (A5)"),
    "JGB10Y":    dict(asset_class="bond", paper_start="Dec-81", paper_stats=(3.66, 5.40),
                      legs=[(9846, None)],
                      notes="TSE 10y JGB; starts 1986-12-01; UNSCALED (A5)"),
    "GILT":      dict(asset_class="bond", paper_start="Dec-79", paper_stats=(3.00, 9.12),
                      legs=[(12626, None)],
                      adjust=[("1988-06-01", 95.8125 / 120.1875)],  # quote-scale change, -20.3% raw jump
                      notes="LIFFE long gilt; starts 1982-11-18; one quote-scale jump (1988-06-01) back-adjusted; UNSCALED (A5)"),
    "US2Y":      dict(asset_class="bond", paper_start="Apr-96", paper_stats=(1.65, 1.86),
                      legs=[(3632, None)],
                      notes="CBT 2y US T-note (CTUCS00, data 1990-06-22 -> 2015-07-10) preferred over ECBOT CZTCS00 (1998-10 -> ) on 1985-2009 coverage; UNSCALED (A5)"),
    "US5Y":      dict(asset_class="bond", paper_start="Jan-90", paper_stats=(3.17, 4.25),
                      legs=[(10984, None)],
                      notes="CBT 5y US T-note (CFVCS00, 1988-05-20 -> 2015-07-10); UNSCALED (A5)"),
    "US10Y":     dict(asset_class="bond", paper_start="Dec-79", paper_stats=(3.80, 9.30),
                      legs=[(12855, None)],
                      notes="CBT 10y US T-note (CTYCS00, 1982-05-03 -> 2015-07-10); UNSCALED (A5)"),
    "USLONG":    dict(asset_class="bond", paper_start="Jan-90", paper_stats=(9.50, 18.56),
                      legs=[(11512, None)],
                      notes="CBT 30y US T-bond (CUSCS00, 1977-10-03 -> 2015-07-10); UNSCALED (A5)"),
    # ---------------- currencies (9 futures-based of the paper's 12) ----------------
    "AUDUSD":    dict(asset_class="currency", paper_start="Mar-72", paper_stats=(1.85, 10.86),
                      legs=[(3876, None)],
                      notes="CME (IMM) Australian dollar front; data 1987-03-18 -> 2015-07-10; USD per AUD quote"),
    "CADUSD":    dict(asset_class="currency", paper_start="Mar-72", paper_stats=(0.60, 6.29),
                      legs=[(5301, None)],
                      notes="CME (IMM) Canadian dollar front; data 1972-05-16 -> 2015-07-10; USD per CAD quote"),
    "EURUSD":    dict(asset_class="currency", paper_start="Sep-71", paper_stats=(1.57, 11.21),
                      legs=[(167, "2001-12-14"), (2831, "2007-12-17"), (11075, None)],
                      notes="Paper's 'Germany spliced with the Euro': CME Deutsche Mark (1976-04-29 -> 2001-12-14, USD/DEM) -> FINEX Euro/US$ large (-> 2007-12-17, its last traded day; daily returns correlate 0.995 with the standard contract) -> FINEX Euro/US$ (-> 2011-09-22); back-adjusted at joints (DEM->EUR factor ~1.949 observed vs 1.95583 official)"),
    "JPYUSD":    dict(asset_class="currency", paper_start="Sep-71", paper_stats=(1.35, 11.66),
                      legs=[(10574, None)],
                      notes="CME (IMM) Japanese yen front; data 1976-08-18 -> 2015-07-10; USD per JPY quote"),
    "GBPUSD":    dict(asset_class="currency", paper_start="Sep-71", paper_stats=(None, None),
                      legs=[(11147, None)],
                      notes="CME (IMM) British pound front; data 1972-05-16 -> 2015-07-10; USD per GBP quote; paper Table 1 row truncated in source extraction (stats unverifiable)"),
    "CHFUSD":    dict(asset_class="currency", paper_start="Sep-71", paper_stats=(1.34, None),
                      legs=[(4592, None)],
                      notes="CME (IMM) Swiss franc front; data 1976-03-16 -> 2015-07-10; USD per CHF quote; paper vol truncated in source extraction"),
    "NZDUSD":    dict(asset_class="currency", paper_start="Feb-78", paper_stats=(2.31, 12.01),
                      legs=[(11685, None)],
                      notes="CME (IMM) New Zealand dollar front; starts 1997-05-07 (CME NZD listing; paper Feb-78 used spot/forward data)"),
    "NOKUSD":    dict(asset_class="currency", paper_start="Feb-78", paper_stats=(1.37, 10.56),
                      legs=[(2312, None)], invert=True,
                      notes="FINEX (NYFE) US$/Norwegian krone, quoted NOK-per-USD -> inverted to USD-per-NOK (paper's NOK/USD convention); 2000-05-12 -> 2008-03-17 (longest-coverage acceptable series; BSE-US$/NOK starts 2005 only); NOK ABSENT 2008-04 -> 2009-12"),
    "SEKUSD":    dict(asset_class="currency", paper_start="Feb-78", paper_stats=(-0.05, 11.06),
                      legs=[(19478, None)], invert=True,
                      notes="FINEX (NYFE) US$/Swedish krona, quoted SEK-per-USD -> inverted to USD-per-SEK (paper's SEK/USD convention); starts 2008-11-20 — only ~13 months inside 1985-2009; kept per A6 (series exists)"),
    # ---- NOT FOUND: the paper's 3 remaining currency instruments ----
    "FXCROSS1":  dict(asset_class="currency", paper_start="?", paper_stats=(None, None), legs=[],
                      notes="NOT FOUND: the paper lists 12 cross-currency pairs from 9 underlying currencies; the 3 pairs beyond the 9 USD-based futures above cannot be identified (Table 1 currency rows truncated in the source extraction at CHF/USD) and are not single-exchange instruments mappable under A4/A6; excluded"),
    "FXCROSS2":  dict(asset_class="currency", paper_start="?", paper_stats=(None, None), legs=[],
                      notes="NOT FOUND: see FXCROSS1"),
    "FXCROSS3":  dict(asset_class="currency", paper_start="?", paper_stats=(None, None), legs=[],
                      notes="NOT FOUND: see FXCROSS1"),
}


# --- ClickHouse connection ----------------------------------------------
def _client() -> Client:
    cfg = get_clickhouse_config()
    return Client(
        host=os.getenv("CLICKHOUSE_HOST", cfg["host"]),
        port=int(os.getenv("CLICKHOUSE_PORT", cfg["port"])),
        user=os.getenv("CLICKHOUSE_USER", cfg["user"]),
        password=os.getenv("CLICKHOUSE_PASSWORD", cfg["password"]),
        settings={"max_execution_time": 900},
    )


def q(sql: str) -> pd.DataFrame:
    cli = _client()
    data, cols = cli.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[c[0] for c in cols])


def q_file(name: str, **fmt) -> pd.DataFrame:
    sql = (SQL_DIR / name).read_text()
    if fmt:
        sql = sql.format(**fmt)
    return q(sql)


# --- pipeline steps ------------------------------------------------------
def build_spliced_series(daily: pd.DataFrame, legs: list[tuple[int, str | None]],
                         adjust: list[tuple[str, float]] = (),
                         invert: bool = False) -> pd.Series:
    """Stitch front-contract legs into one price series, back-adjusted.

    Dates are assigned to legs PURELY by cutoff: leg i covers
    (end_{i-1}, end_i]. A date whose primary leg has no valid settlement is
    simply absent (the next return spans the gap — the same treatment as a
    holiday), which avoids pulling later-leg levels into earlier ranges.
    At each joint, all earlier prices are multiplied by
    price_next(first day) / price_prev(last day) so the one-day return
    across the splice is ~0 (level continuity; the alternative — keeping the
    raw gap — would inject the contract-conversion spread as a fake return).
    `adjust` events (date, factor) multiply all prices BEFORE `date` by
    `factor`, fixing documented quote-scale changes (euro redenomination,
    CME convention changes) observed in the raw series. `invert` takes 1/P
    for series quoted as domestic currency per USD (FINEX NOK/SEK), making
    them USD-per-unit returns like the paper's currency forwards.
    """
    by_code = {
        code: grp.set_index("date_")["settlement"].sort_index()
        for code, _ in legs
        for grp in [daily[daily["calcseriescode"] == code]]
        if len(daily[daily["calcseriescode"] == code])
    }
    combined: dict[pd.Timestamp, tuple[float, int]] = {}
    prev_end = None
    for i, (code, end) in enumerate(legs):
        if code not in by_code:
            prev_end = pd.Timestamp(end) if end else prev_end
            continue
        end_ts = pd.Timestamp(end) if end else None
        for d, p in by_code[code].items():
            if prev_end is not None and d <= prev_end:
                continue                       # belongs to an earlier leg's range
            if end_ts is not None and d > end_ts:
                continue                       # belongs to a later leg's range
            combined.setdefault(d, (float(p), i))
        prev_end = end_ts if end_ts is not None else prev_end
    if not combined:
        return pd.Series(dtype="float64")
    s = pd.Series({d: v[0] for d, v in combined.items()}).sort_index()
    src = pd.Series({d: v[1] for d, v in combined.items()}).sort_index()
    # back-adjust at each joint (leg i-1 -> i): make the joint continuous
    for i in range(1, len(legs)):
        prev_days = s.index[src < i]
        next_days = s.index[src >= i]
        if len(prev_days) == 0 or len(next_days) == 0:
            continue
        last_prev, first_next = prev_days[-1], next_days[0]
        if s[last_prev] > 0:
            s.loc[:last_prev] *= s[first_next] / s[last_prev]
    # documented quote-scale changes: multiply everything before `date`
    for when, factor in sorted(adjust):
        before = s.index < pd.Timestamp(when)
        s.loc[before] *= factor
    if invert:
        s = 1.0 / s
    return s


def drop_bad_marks(s: pd.Series, thresh: float = 0.5) -> pd.Series:
    """Remove isolated misrecorded settlement marks.

    A day is dropped when its price deviates by more than `thresh` from the
    median of its four neighbours (2 before, 2 after). Real one-day moves in
    this universe top out around 30-40% (crash days, hurricane days), which
    deviate from the neighbour median by < thresh; the documented bad marks
    (HEATOIL 2009-10-06/07 quoted in $/barrel instead of $/gallon; FINEX
    euro 1999/2001 one-day ~2x spikes) deviate by 70-4000%.
    """
    p = s.to_numpy(dtype=float)
    keep = np.ones(len(p), dtype=bool)
    for t in range(len(p)):
        nbrs = [p[t + o] for o in (-2, -1, 1, 2) if 0 <= t + o < len(p)]
        if len(nbrs) < 2:
            continue
        med = float(np.median(nbrs))
        if med > 0 and abs(p[t] / med - 1.0) > thresh:
            keep[t] = False
    return s[keep]


def ewma_sigma(excess: np.ndarray) -> np.ndarray:
    """Eq. (1): EWMA annualized volatility on daily excess returns.

    Returns sigma aligned to `excess`; entries before the 120-day burn-in are
    NaN. sigma[t] uses returns through day t-1 (no same-day information);
    initialized with mean/variance of the first BURN_IN observations.
    """
    n = len(excess)
    sigma = np.full(n, np.nan)
    if n < BURN_IN + 1:
        return sigma
    d = DELTA
    m = float(np.mean(excess[:BURN_IN]))
    v = float(np.var(excess[:BURN_IN], ddof=1))
    sigma[BURN_IN] = math.sqrt(ANNUALIZE * v)
    for t in range(BURN_IN + 1, n):
        r_lag = excess[t - 1]
        v = d * v + (1.0 - d) * (r_lag - m) ** 2
        m = d * m + (1.0 - d) * r_lag
        sigma[t] = math.sqrt(ANNUALIZE * v)
    return sigma


def build_instrument(name: str, spec: dict, daily: pd.DataFrame, rf: pd.DataFrame) -> pd.DataFrame:
    """One instrument -> month-level frame (month, ret, sigma, n_days)."""
    if not spec["legs"]:  # NOT FOUND
        return pd.DataFrame(columns=["month", "ret", "sigma", "n_days"])
    prices = build_spliced_series(daily, spec["legs"],
                                  adjust=spec.get("adjust", ()),
                                  invert=spec.get("invert", False))
    n_dropped = len(prices)
    prices = drop_bad_marks(prices)
    n_dropped -= len(prices)
    if n_dropped:
        print(f"  [{name}] dropped {n_dropped} isolated bad settlement mark(s)")
    if len(prices) < 2:
        return pd.DataFrame(columns=["month", "ret", "sigma", "n_days"])
    df = pd.DataFrame({"settlement": prices})
    df["ret_fut"] = df["settlement"].pct_change()
    n_days_all = df.groupby(df.index.to_period("M"))["settlement"].size()
    df = df.iloc[1:].copy()                      # first day has no return
    df["month"] = df.index.to_period("M")
    # daily risk-free accrual: (1 + rf_monthly)^(1/n_trading_days) - 1
    rf_m = rf.copy()
    rf_m["month"] = rf_m["dt"].dt.to_period("M")
    rf_m = rf_m.set_index("month")["rf"]
    df["n"] = df["month"].map(n_days_all)        # settlement days in month
    df["rf_m"] = df["month"].map(rf_m)
    bad = df["rf_m"].isna()
    if bad.any():
        df = df[~bad]
    df["rf_d"] = (1.0 + df["rf_m"]) ** (1.0 / df["n"]) - 1.0
    df["excess"] = (1.0 + df["ret_fut"]) / (1.0 + df["rf_d"]) - 1.0
    excess = df["excess"].to_numpy()
    df["sigma_daily"] = ewma_sigma(excess)
    # monthly excess return = product of daily (1 + excess) - 1
    monthly_ret = (
        df.assign(one_plus=df["excess"] + 1.0)
        .groupby("month")["one_plus"].prod() - 1.0
    )
    n_days = n_days_all.reindex(monthly_ret.index)
    # sigma lagged one month: sigma at the last trading day of month t-1
    sig_by_month = df.dropna(subset=["sigma_daily"]).groupby("month")["sigma_daily"].last()
    months = monthly_ret.index.sort_values()
    rows = []
    for m in months:
        prev = m - 1
        s = sig_by_month.get(prev, np.nan)
        if np.isnan(s):  # fallback: most recent sigma on/before end of m-1
            older = sig_by_month.index[sig_by_month.index <= prev]
            s = sig_by_month[older[-1]] if len(older) else np.nan
        rows.append((m, monthly_ret[m], s, int(n_days[m])))
    out = pd.DataFrame(rows, columns=["month", "ret", "sigma", "n_days"])
    out = out[out["sigma"].notna()]              # drop pre-burn-in months
    out = out[out["month"].dt.to_timestamp("M") <= PANEL_END]
    return out


# --- main ----------------------------------------------------------------
def main() -> None:
    LAYOUT.ensure()
    rules_path = LAYOUT.preparations_path("preprocessing_rules.json")
    if rules_path.exists():  # single source of truth check (params are paper quotes)
        import json
        _rules = json.loads(rules_path.read_text())
        print(f"Loaded {len(_rules)} preprocessing rules from {rules_path.name}")

    # 1. daily settlements for every selected leg -------------------------
    # Deduped + filtered pull cache (~330k rows; SQL does the GROUP BY dedup
    # and settlement>0 filter): avoids re-scanning the 301M-row
    # wrds_fut_series on every re-run. Kept in data/ as a computed
    # intermediate (relaxed layout policy — only raw SELECT * dumps are
    # banned). Delete data/cache_daily_futures.parquet to force a fresh pull.
    codes = sorted({code for spec in INSTRUMENTS.values() for code, _ in spec["legs"]})
    cache_daily = LAYOUT.data_path("cache_daily_futures.parquet")
    cache_rf = LAYOUT.data_path("cache_rf_monthly.parquet")
    codes_file = LAYOUT.data_path("cache_codes.txt")
    cached_codes = codes_file.read_text().split() if codes_file.exists() else []
    if cache_daily.exists() and cached_codes == [str(c) for c in codes]:
        daily = pd.read_parquet(cache_daily)
        print(f"Loaded cached daily futures ({len(daily):,} rows) from {cache_daily.name}")
    else:
        print(f"Pulling daily futures data for {len(codes)} calc series "
              f"({PULL_START} -> {PULL_END}) ...")
        daily = q_file("daily_futures.sql",
                       codes=",".join(str(c) for c in codes),
                       start_date=PULL_START, end_date=PULL_END)
        daily["calcseriescode"] = daily["calcseriescode"].astype(int)
        daily = daily.rename(columns={"settle": "settlement"})
        daily["date_"] = pd.to_datetime(daily["date_"])
        daily = daily.sort_values(["calcseriescode", "date_"]).reset_index(drop=True)
        daily.to_parquet(cache_daily, index=False)
        codes_file.write_text(" ".join(str(c) for c in codes))
    print(f"  daily rows: {len(daily):,} "
          f"({daily['date_'].min().date()} -> {daily['date_'].max().date()})")

    # 2. risk-free rate ----------------------------------------------------
    if cache_rf.exists():
        rf = pd.read_parquet(cache_rf)
    else:
        rf = q_file("rf_monthly.sql")
        rf["dt"] = pd.to_datetime(rf["dt"])
        rf = rf.sort_values("dt").reset_index(drop=True)
        rf.to_parquet(cache_rf, index=False)
    print(f"  rf months: {len(rf)} ({rf['dt'].min().date()} -> {rf['dt'].max().date()}); "
          f"mean rf 1985-2009 = "
          f"{rf.loc[(rf['dt'] >= '1985-01-01') & (rf['dt'] <= '2009-12-31'), 'rf'].mean():.5f} "
          f"per month (DECIMAL — ff table already stores decimals in this build)")

    # 3. series metadata for instrument_map.csv ----------------------------
    info = q_file("series_info.sql", codes=",".join(str(c) for c in codes))
    info["calcseriescode"] = info["calcseriescode"].astype(int)
    info = info.set_index("calcseriescode")
    cov = daily.groupby("calcseriescode")["date_"].agg(["min", "max"])

    # 4. per-instrument panels + instrument map ----------------------------
    panels, map_rows = [], []
    for name, spec in INSTRUMENTS.items():
        panel = build_instrument(name, spec, daily, rf)
        if len(panel):
            panel.insert(0, "instrument", name)
            panel.insert(1, "asset_class", spec["asset_class"])
            panels.append(panel)
        leg_codes = [code for code, _ in spec["legs"]]
        if leg_codes:
            iinfo = info.loc[[c for c in leg_codes if c in info.index]]
            map_rows.append({
                "instrument": name,
                "asset_class": spec["asset_class"],
                "calcseriescode": "+".join(str(c) for c in leg_codes),
                "dsmnem": "+".join(str(iinfo.loc[c, "dsmnem"]) for c in leg_codes if c in iinfo.index),
                "calcseriesname": " -> ".join(str(iinfo.loc[c, "calcseriesname"]) for c in leg_codes if c in iinfo.index),
                "rollmethoddesc": "; ".join(str(iinfo.loc[c, "rollmethoddesc"]) for c in leg_codes if c in iinfo.index),
                "first_date": str(cov.loc[[c for c in leg_codes if c in cov.index], "min"].min().date())
                if any(c in cov.index for c in leg_codes) else "",
                "last_date": str(cov.loc[[c for c in leg_codes if c in cov.index], "max"].max().date())
                if any(c in cov.index for c in leg_codes) else "",
                "paper_start": spec["paper_start"],
                "notes": spec["notes"],
            })
        else:
            map_rows.append({
                "instrument": name, "asset_class": spec["asset_class"],
                "calcseriescode": "", "dsmnem": "", "calcseriesname": "",
                "rollmethoddesc": "", "first_date": "", "last_date": "",
                "paper_start": spec["paper_start"], "notes": spec["notes"],
            })

    pd.DataFrame(map_rows).to_csv(LAYOUT.data_path("instrument_map.csv"), index=False)
    print(f"Wrote {LAYOUT.data_path('instrument_map.csv')} ({len(map_rows)} rows)")

    panel = (pd.concat(panels, ignore_index=True)
             if panels else pd.DataFrame(
                 columns=["instrument", "asset_class", "month", "ret", "sigma", "n_days"]))
    panel["month"] = panel["month"].map(lambda p: p.to_timestamp("M"))
    panel = panel.sort_values(["instrument", "month"]).reset_index(drop=True)
    panel = panel.astype({"instrument": "string", "asset_class": "string",
                          "ret": "float64", "sigma": "float64", "n_days": "int32"})
    panel.to_parquet(LAYOUT.data_path("panel.parquet"), index=False)

    # 5. run summary --------------------------------------------------------
    print("\n" + "=" * 72)
    print("RUN SUMMARY")
    print("=" * 72)
    n_inst = panel["instrument"].nunique()
    print(f"panel: {len(panel):,} rows x {panel.shape[1]} cols | "
          f"instruments: {n_inst} | months: {panel['month'].nunique()} "
          f"({panel['month'].min().date()} -> {panel['month'].max().date()})")
    print(f"null%: ret = {panel['ret'].isna().mean():.2%}, "
          f"sigma = {panel['sigma'].isna().mean():.2%} "
          f"(pre-burn-in months dropped)")
    w85 = panel[(panel["month"] >= "1985-01-01") & (panel["month"] <= "2009-12-01")]
    print(f"avg obs/month 1985-2009: {len(w85) / max(1, w85['month'].nunique()):.1f}")
    for mth in ["1985-01-31", "1990-01-31", "2000-01-31", "2009-12-31"]:
        m = pd.Timestamp(mth)
        s_t = panel[(panel["month"] == m) & panel["ret"].notna() & panel["sigma"].notna()]
        print(f"S_t {m.strftime('%b %Y')}: {len(s_t)} instruments")

    # 6. Table 1 preview vs paper -------------------------------------------
    print("\nTable 1 preview (ann. mean% / vol% ; ours full-sample | ours 1985-2009 | paper)")
    print(f"{'instrument':<10} {'full mean':>9} {'full vol':>9} | {'8509 mean':>9} {'8509 vol':>9} | "
          f"{'paper mean':>10} {'paper vol':>9} | {'start':>10}  flag")
    t1_rows = []
    for name, spec in INSTRUMENTS.items():
        sub = panel[panel["instrument"] == name]
        if not len(sub):
            continue
        f_mean, f_vol = sub["ret"].mean() * 12 * 100, sub["ret"].std(ddof=1) * math.sqrt(12) * 100
        s2 = sub[(sub["month"] >= "1985-01-01") & (sub["month"] <= "2009-12-01")]
        if len(s2) > 2:
            b_mean, b_vol = s2["ret"].mean() * 12 * 100, s2["ret"].std(ddof=1) * math.sqrt(12) * 100
        else:
            b_mean = b_vol = float("nan")
        pm, pv = spec["paper_stats"]
        flag = ""
        if pv is not None and not math.isnan(b_vol) and abs(b_vol - pv) > 5.0:
            flag = "VOL>5pp"
        start = sub["month"].min().strftime("%Y-%m")
        t1_rows.append((name, f_mean, f_vol, b_mean, b_vol, pm, pv, start, flag))
        print(f"{name:<10} {f_mean:>9.2f} {f_vol:>9.2f} | "
              f"{(b_mean if b_mean == b_mean else float('nan')):>9.2f} "
              f"{(b_vol if b_vol == b_vol else float('nan')):>9.2f} | "
              f"{(pm if pm is not None else float('nan')):>10.2f} "
              f"{(pv if pv is not None else float('nan')):>9.2f} | {start:>10}  {flag}")
    pd.DataFrame(t1_rows, columns=["instrument", "full_mean", "full_vol", "mean_8509",
                                   "vol_8509", "paper_mean", "paper_vol", "our_start",
                                   "flag"]).to_csv(LAYOUT.data_path("t1_preview.csv"), index=False)
    print(f"\nWrote {LAYOUT.data_path('panel.parquet')} ({len(panel):,} rows)")


if __name__ == "__main__":
    main()
