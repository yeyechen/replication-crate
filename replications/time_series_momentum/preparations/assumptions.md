# Assumptions Registry — Time Series Momentum (Moskowitz, Ooi, Pedersen 2012)

Paper-silent decisions made by the replicator. Each entry: Decision / Rationale / Impact.
Paper-derived rules live in `preprocessing_rules.json` (verbatim quotes); this file is for
choices the paper does not specify, plus per-iteration diagnostics.

---

# Assumption A1: Currency of the risk-free rate for excess returns

**Decision:** Use the US 1-month T-bill rate (`ff.four_factor_monthly.rf`) for ALL instruments —
equity indexes, bonds, currencies, and commodities — accruing it daily at a constant within-month
rate: daily rf = (1 + monthly rf)^(1/n_trading_days) − 1; daily excess = (1 + r_fut)/(1 + rf_daily) − 1.
**Rationale:** Paper is silent on which T-bill rate defines excess returns. §2.1 says equity index
returns are "in excess of the Treasury bill rate" without specifying currency; §6.3's price-change
definition subtracts "the risk-free interest rate over the 12-month period" without specifying
currency. The factors used (FF SMB/HML/UMD) are US-based, and the Ken French rf is the US T-bill —
the available, consistent choice. Magnitude: rf averages ~0.3–0.4%/month over 1985–2009 vs instrument
volatilities of 2–15%/month, so the choice barely affects signal signs (12-month cumulative) or
volatility scaling; it shifts annualized mean returns down by ~4 pp/year uniformly.
Considered alternatives: local-currency T-bills per instrument (theoretically correct for local
bond/currency returns, but no T-bill series per currency in ClickHouse — would require external data).
**Impact:** All instruments' excess returns (T1 mean cells shift ~−4 pp/yr; volatilities essentially
unaffected), all signals, all alphas. Direction of any bias is known and uniform.

# Assumption A2: Passive asset-class benchmark proxies in the alpha regressions

**Decision:** The paper's Eq. (4) controls for MKT (MSCI World), BOND (Lehman/Barclays Aggregate),
and GSCI (S&P GSCI) — none of which exist in ClickHouse (verified: `tr_ds_equities_202303.wrds_ds_indexmerged`
contains only S&P/FTSE country and sector indexes; no MSCI World, GSCI, or Barclays Aggregate series
anywhere in the catalog). Substitute each with an equal-weighted portfolio of monthly excess returns
of the paper's OWN futures within that asset class (9 equity index futures for MKT, 13 bond futures
for BOND, 24 commodity futures for GSCI). SMB/HML/UMD are used exactly, from `ff.four_factor_monthly`.
**Rationale:** The paper itself constructs "diversified passive long positions in all instruments"
within and across asset classes (Fig. 3, Fig. 4, Table 4) — the proxy is the paper's own object.
The regressors' job is to absorb passive asset-class exposure; the paper's reported betas on
MKT/BOND/GSCI are small (0.09/… Table 3A), so residual differences between MSCI World and an EW of 9
developed-index futures are second-order for the intercept. Logged prominently in Table 2/Table 3 notes.
**Impact:** T2 alpha t-statistics (all cells), T3 coefficients. Expected intercept drift small;
will be measured in the iteration log (diagnostic: alpha with vs. without passive controls).

# Assumption A3: No pre-futures index splicing

**Decision:** Each instrument's return series starts when its Datastream continuous futures series
has data — no splice to MSCI country indexes (equities before futures listing) or JPM bond indexes
(bonds), and no Citigroup/IBOR-based currency construction before 1989.
**Rationale:** The spliced index series (MSCI country, JPM government bond, Citigroup forward rates)
are not in ClickHouse. Datastream continuous futures series start at exchange listing (e.g., CME S&P
500 futures: 1982-04 vs paper's spliced Jan-65 start). The paper's strategy evaluation window is
Jan 1985–Dec 2009 (§3.2), chosen precisely because "a comprehensive set of instruments have data" —
most instruments have live futures by 1985. Instruments listed after 1985 (natural gas 1990, nickel
1993, euro-zone Schatz/Buxl, etc.) enter the cross-section when available, matching the paper's
"all S_t securities that are available at time t" convention.
**Impact:** Table 1 start dates differ from the paper for instruments the paper spliced back before
their futures listing (esp. equity indexes and the S&P 500, bonds, some currencies); Table 1 means
and volatilities computed over a shorter window than the paper's 1965–2009 for those instruments.
The TSMOM factor S_t counts in the late 1970s/early 1980s are lower; post-1985 overlap is strong.

# Assumption A4: Instrument-to-Datastream-series mapping rules

**Decision:** For each of the 58 instruments, select the `wrds_cseries_info` calc series matching:
(a) the exchange named in Appendix A (e.g., CME for live cattle, ICE/CSCE for cocoa, LME for aluminum,
EUREX for Euro-Bund, LIFFE for Long Gilt, CBT/ECBOT for corn); (b) `positionfwddesc = 'First'` (front
contract — the paper's "nearest or next nearest-to-delivery"); (c) roll method among {volume-based
roll ("Switch over when 2nd month future volume exceeds 1st"), weighted-volume, first-day-of-month,
nearest-with-switch-after-last-trading-day} — implementing "the most liquid futures contract";
EXCLUDE roll methods "Average of all futures", "As a price index", and "Reuters Continuation Record"
(not a single-contract series). When several series survive, prefer the one with the longest
1965–2009 coverage and the series without "DEAD" suffix if coverage is equal. The full mapping is
audited in `data/instrument_map.csv`.
**Rationale:** The paper does not publish Datastream mnemonics. The criteria follow §2.1 verbatim
("most liquid … typically the nearest or next nearest-to-delivery contract") and Appendix A's
exchange assignments.
**Impact:** Everything downstream. Mapping errors would show up first in Table 1 mean/vol mismatches.

# Assumption A5: Bond duration scaling

**Decision:** Scale each bond futures' daily excess return by target_duration / contract_duration,
with targets {2y: 2, 3y: 2, 5y: 4, 10y: 7, 30y: 20} per Appendix A.2. Contract duration is proxied
from the futures curve data when available; if no duration field is obtainable from the catalog,
bond futures returns are used UNSCALED and the deviation is logged here with a measured sensitivity
(paper's Table 1 bond vols — e.g. 2y US 1.86% vs 30y US 18.56% — partly reflect unscaled contract
volatility; scaling compresses long-bond vol toward the 2–9% range).
**Rationale:** The paper states targets but not the source of the divisor ("We scale daily returns
to a constant duration of 2 years … 4 years … 7 years … 20 years"). `wrds_fut_series.life` gives
days-to-expiry of the front contract, not duration; a duration proxy from the generic series is the
closest available. The rep-worker will check what is available before choosing.
**Impact:** All bond statistics (T1 bond rows), bond panels (T2 Panel D), bond weight in T3/T4/T5.

# Assumption A6: Currency instruments from Datastream futures

**Decision:** Construct currency returns from Datastream continuous futures series (CME/IMM currency
futures for AUD, CAD, DEM→EUR splice, JPY, GBP, CHF, NZD; LIFFE/other exchange series for NOK, SEK
where available), using the same front-contract, volume-roll selection as A4. The paper's
spot+forward-interest-rate construction (Citigroup forwards from 1989; Datastream spot + Bloomberg
IBOR before) is not replicable with ClickHouse contents.
**Rationale:** Covered-interest parity makes IMM futures returns ≈ forward FX returns; the paper's
Appendix A.3 itself moves across data sources over time, so series construction is already
splice-based. Where no continuous futures series exists for an instrument (possibly NOK, SEK,
EUR crosses), the instrument is excluded and the exclusion listed in `data/instrument_map.csv`.
**Impact:** Table 1 FX rows, FX cells in T2/T4/T5; possible reduction from 12 to ~9–10 currency
instruments.

# Assumption A7: Factor and risk-free rate units in this ClickHouse build

**Decision:** `ff.four_factor_monthly` columns (mkt_rf, smb, hml, mom, rf) are stored as DECIMALS in
this database build (verified: 2008-10 mkt_rf = −0.1721, rf = 0.0 throughout 2009), not in percent as
in the raw Ken French text files. Do NOT divide by 100. All strategy returns are computed in
decimals; paper comparisons multiply by 100 at reporting time.
**Rationale:** Empirical verification of the actual data overrides the raw-file convention.
**Impact:** All factor regressions (T2 alphas, T3, T5) — scale only; no inference change.

# Assumption A8: Precious-metals series splicing around the Datastream delivery hole

**Decision:** NYMEX/COMEX gold and silver continuous series in this Datastream delivery have a hard
coverage hole (gold: COMEX/CBT series end 1987-09 / 1999-06 / 2002-05; NYL series start 2004-10;
silver: COMEX ends 2001-07; NYL starts 2004-10) — verified across all ~200 gold and ~100 silver
series in the catalog. To keep both instruments in the cross-section across 1985–2009:
- GOLD = CME-GOLD 100 OZ (1979-01→) + CBT-GOLD 1 KILOGRAM (→2002-05) + TOCOM-GOLD CONT. VOL
  (2002-05→2009-12), back-adjusted to level continuity at each joint. TOCOM gold is yen/gram, so
  post-2002-05 returns embed USDJPY drift (a slow drift, not a TSMOM signal — sign of 12-month
  momentum is robust to it; the 2000s gold bull dominates JPY noise).
- SILVER = COMEX silver (→2001-07) + NYL-SILVER 5000 OZ CONT. VOL (2004-10→), back-adjusted at the
  join; the actual silver move over the 2001-07→2004-10 hole is lost.
**Rationale:** Dropping gold from 2000–2009 would remove the strongest commodity trend of the sample
and corrupt every commodity-aggregate cell (T2 Panel B, T3, T4, T5); a documented contaminated
series is preferable to a silent absence. TOCOM is a legitimate gold futures market (the paper's own
Appendix A.4 sources platinum from TOCOM).
**Impact:** T1 GOLD/SILVER cells (means/vols will deviate — Tier 2 expected), commodity-aggregate
statistics (directionally preserved). Cross-joint 12-month returns approximate.

# Assumption A9: Roll-artifact series selection criterion

**Decision:** Where several Datastream continuous series exist for one instrument differing only in
roll method, prefer the series whose roll method minimizes spurious price discontinuities
(volume/weighted-volume roll over first-of-month roll) — diagnosed by counting |daily return| > 10%
days at known contract-conversion dates. Selection is by data-quality diagnostics (roll-gap
frequency), NOT by closeness to paper statistics. Instruments with residual artifacts (e.g., SFE
Australian bonds over-smoothing, NATGAS seasonal roll gaps if no clean variant exists) are kept and
their cells evaluated at Tier 2 with this justification.
**Rationale:** The paper's "most liquid contract" instruction (§2.1) maps naturally to volume-based
rolls; roll discontinuities are pure measurement error in the instrument's return series.
**Impact:** NATGAS, HOGS, COTTON, HEATOIL, UNLEADED (diagnosed in inner iteration 2).

---

# Assumption A10: Newey-West correction for overlapping holding periods (Table 2)

**Decision:** The t-statistics of the alphas in Table 2 use Newey-West standard errors with h−1
lags for holding period h (0 lags = plain OLS for h=1).
**Rationale:** The paper does not specify the correction, but for h>1 the monthly strategy return is
the average of h active cohorts, mechanically inducing MA(h−1) autocorrelation; plain OLS standard
errors would be anti-conservative. The paper's reported t-stats DECREASE from h=1 to h=3 for k=12
(6.61 → 5.60) — consistent with an overlap correction rather than plain OLS. NW(h−1) is the standard
treatment for Jegadeesh-Titman-style overlapping portfolios (utils/tstat_newey_west convention).
**Impact:** All 232 Table 2 cells at h>1.

# Assumption A11: Cross-sectional momentum (XSMOM) construction for Table 5

**Decision:** XSMOM per asset class and over all assets: at formation month t, rank the available
instruments by cumulative excess return over months t−12..t−2 (the 12-month formation with the most
recent month skipped, per footnote 10 following AMP 2010 — the paper notes results do not depend on
the skip); weight w_{s,t} = (rank_s − median rank) / Σ_i |rank_i − median rank| (Σ|w| = 1, long side
= short side = 1 in absolute weight, proportional to distance from the median rank per §5.1); each
instrument's contribution is volatility-scaled exactly like TSMOM (40%/σ_{s,t}). XSMOM return at
t+1 = Σ_s w_{s,t} × (40%/σ_{s,t}) × ret_{s,t+1}, equal to the number of instruments available.
XSMOM US stocks uses the FF UMD factor itself (the paper's individual-stock momentum).
**Rationale:** §5.1 specifies "long or short the assets in proportion to their ranks relative to the
median rank" and footnote 10 the skip-month convention; the paper is silent on exact normalization.
Σ|w|=1 normalization makes XSMOM risk-comparable to the TSMOM factor (paper: beta of TSMOM on XSMOM =
0.66 ≈ their correlation √0.44 = 0.66 — consistent with equal aggregate exposure).
**Impact:** T5 cells (XSMOM ALL/COM/EQ/FI/FX regressions on TSMOM).

---

# Worker notes (data-pipeline iteration, 2026-07-22) — implementation-level decisions

- **W1 (rf units):** `ff.four_factor_monthly.rf` in this ClickHouse build is already a DECIMAL
  (1926-07 = 0.002503 ≈ 3%/yr; 2009 = 0.0), NOT percent. The task instruction "divide by 100"
  was NOT applied (would make rf ~0). Mean rf 1985–2009 = 0.356%/month.
- **W2 (A5 confirmed):** no duration field exists anywhere in `wrds_fut_series`
  (`life` = days-to-expiry of the front contract; ext-table items are session prices/yield only).
  Bond returns are UNSCALED per A5. This explains most of the bond vol gaps vs Table 1
  (e.g. USLONG 10.9% vs 18.56% paper — the paper scales 30y to 20y duration).
- **W3 (FX quote direction):** FINEX US$/NW KRONE (NUKCS00) and US$-SWEDISH KRONA (NSKCS00) are
  quoted domestic-currency-per-USD; inverted (1/P) to the paper's USD-per-foreign convention.
  CME/IMM currencies and FINEX euro series are already USD-per-unit.
- **W4 (quote-scale artifacts back-adjusted):** AEX (1996-06-19 contract re-spec +118%,
  1998-12-01 guilder→euro −57%), CAN10Y (1989-10-06 +21.5%, 1999-05-21 +20.5%), GILT
  (1988-06-01 −20.3%) had permanent quote-scale jumps in the raw series; all prices before each
  jump were multiplied by post/pre for continuity (see `adjust=` in src/main.py). Volatilities
  moved into line with the paper after this (AEX 20.29% vs 19.18%).
- **W5 (spliced instruments):** GASOIL (IPE→ICE), CAC40 (MATIF→MONEP), FTSEMIB (MIB30→FTSE MIB),
  EURO5Y/10Y (DTB→EUREX), EURO30Y (Buxl DEAD→live), UNLEADED (NY unleaded→RBOB, per the paper's
  own "RBOB spliced with Unleaded"), EURUSD (DEM→EUR via FINEX euro futures, the paper's
  "Germany spliced with the Euro") are multi-leg series, back-adjusted to level continuity at
  each joint. Single-series selection (A4 wording) was impossible for these without large holes.
- **W6 (coverage gaps — no acceptable series exists):** GOLD = CBT-COMEX 1989-12→1999-06 only
  (CME-GOLD ends 1987-09; NYL-GOLD starts 2004-10 with an unbridgeable 1999–2004 gap);
  SILVER = CBT-COMEX 1989-11→2001-07 only (NYL-SILVER starts 2004-10; 2001–2004 gap);
  NOKUSD = FINEX 2000-05→2008-03 only; SEKUSD starts 2008-11 (≈13 months in-window).
- **W7 (bad marks):** 4 isolated misrecorded settlements removed (HEATOIL 2009-10-06/07 quoted
  $/barrel instead of $/gallon; 2 FINEX euro one-day 2x spikes) via a 50%-median-neighbour
  filter. Real extreme days (1987 crash, 1991 Gulf war gasoline, 2005 Katrina) are preserved.
- **W8 (roll gaps kept):** non-adjusted continuous series include front-contract roll
  discontinuities (e.g. HOGS contract conversions +33% in 1996/1998, NATGAS seasonal gaps,
  SOYMEAL 2009-09 −22% squeeze roll). These follow directly from A4's roll-method selection;
  they likely explain NATGAS mean +17.8% vs paper −9.74% and the COTTON/HOGS/HEATOIL/UNLEADED
  vol flags.
- **W9 (SFE bond quality):** SFE Australian 3y/10y settlement series are over-smoothed
  (ann. vol 1.5–1.6% vs paper 2.57/8.53%; GFC-period daily sd 0.12% vs realistic ~0.5%).
  No alternative SFE 10y series exists in this delivery (AGB* series hold only 2023+ data).
  Kept and flagged in instrument_map.csv.
- **W10 (3 currency instruments missing):** the paper lists 12 cross-currency pairs; the source
  extraction of Table 1 is truncated at CHF/USD, so the 3 non-USD-based pairs cannot be
  identified and are marked NOT FOUND (FXCROSS1-3 in instrument_map.csv).
- **W11 (rf accrual):** rf_daily = (1+rf_monthly)^(1/n)−1 with n = the instrument's own
  settlement-day count in the month (spec's "n_trading_days_in_month", matching panel n_days).

# Worker notes (inner iteration 2, 2026-07-22) — mapping revisions per coordinator calls

- **GOLD (W6 superseded):** 3-leg splice CME-GOLD 100 OZ (716, USD/oz, → 1983-04-11) →
  CBT-GOLD 1 KILOGRAM (3581, USD/kg, 1983-04-12 → 2002-05-06) → TOCOM-GOLD TRc3/VOL
  (16416, JPY/gram, used from 2002-05-07). Back-adjusted at joints (levels continuous; verified).
  Post-2002-05 returns embed USDJPY drift. Panel: 1985-2009 mean/vol −7.63/11.39 (1990-99 only)
  → +0.28/15.03; full sample vol 21.75% vs paper 21.37%. GOLD now present Dec 2009.
- **SILVER (W6 superseded):** 3-leg splice CBT-SILVER 1000 OZ (5277, 1981-06-25 → 1989-12-26;
  front extension found, same $/oz quote) → CBT-SILVER 5000 OZ (5727, → 2001-07-30) → NYL-SILVER
  5000 OZ VOL (11171, 2004-10-06 →). The 2001-08 → 2004-10 hole is unbridgeable — the actual price
  move over those 29 months is LOST (joint back-adjusted flat). 1985-2009: −3.77/21.53 → +1.51/25.77
  (paper 3.17/31.11). SILVER now present Dec 2009.
- **NATGAS:** switched 3372 (LTDT) → 18339 (TRc3, 'switch when 2nd month volume exceeds').
  Diagnosis 1990-2009: 26 one-day |r|>15% discontinuities (LTDT) vs 12 (TRc3); no WVOL variant
  exists. Mean +18.90→+11.91 (raw daily basis), panel 1985-2009 17.81/58.51 → 9.18/44.08
  (paper −9.74/53.30; selected on roll quality, not paper-mean closeness).
- **HEATOIL:** switched 18327 (TRc1) → 18328 (TRc3). 1980-2009: 35 one-day |r|>10% roll gaps →
  4; panel 7.24/38.90 → 5.15/32.32 (paper 33.78 — flag cleared).
- **UNLEADED:** switched to WVOL family: 2494 (1995-01-03 → 2006-12-28) + 18146 (RBOB WVOL).
  1985-2009: 40 one-day |r|>10% moves → 4 (remaining: 2001-09-24, 2003-09-02, Katrina, Rita — all
  genuine). Panel 8.77/44.53 → 13.41/40.80 (paper 15.92/37.36). Cost: 1984-1994 history dropped
  (starts 1995-07 after burn-in; UNLEADED leaves the Jan-1990 cross-section).
- **HOGS:** kept 8646 (CS00). Diagnosis: 30 one-day |r|>10% moves 1995-2009, concentrated on
  contract-conversion/roll dates (1996-12-02, 1998-12-01, 1999-04-01, 2002-08-01, first-of-month
  rolls); WVOL (3138) has identical vol (37.06%) and VOL (7902) has MORE >10% days (32) — the
  artifacts are contract conversions present in all variants; CS00 retained for 1979-1994 coverage.
- **COTTON:** kept 8697 (CS00). Diagnosis: only 4 one-day |r|>10% moves 1995-2009, all genuine
  price spikes (1995-07-05, 2001-06-25, 2003-03-03, 2009-07-01), not conversions; VOL/WVOL remove
  nothing material (-1.5pp vol at the cost of 1979-1994). Flag vs paper 24.35% remains (30.70%).
- **S_t after revisions:** Jan 1985 25→27, Jan 1990 35→36, Jan 2000 50→51, Dec 2009 52→54
  (still absent: NOK); avg obs/month 1985-2009: 44.8→45.4; panel 15,022 → 15,312 rows.

# Worker notes (inner iteration 3, 2026-07-22) — strategy engine + Table 1/2 evaluation

- **Engine validation:** §4.1 k=12,h=1 factor (Eq. 5, 40%/σ): +1.315%/mo, 12.65% annual vol,
  Sharpe 1.25 (paper: ~1.5%/mo, ~12%). Panel A all-assets alpha t (7-factor) k12h1 = 5.33
  (paper 6.61); intercept-only t = 6.24. Signature pattern present in Panel A (positive k≤12,
  decay k≥24) and in Panel D bonds (positive throughout, ours systematically stronger).
- **T1 (106 cells):** vols 34 Tier 1 / 19 Tier 2 / 0 FAIL (vol pipeline validated);
  means 3 Tier 1 / 21 Tier 2 / 29 FAIL (sign flips). The 29 mean flips are the documented A1
  artifact (US T-bill rf applied to all instruments; the paper's bond/FX means are consistent
  with local-currency rfs — shift ≈ −4pp/yr: e.g. US10Y −3.16 vs +3.80, JPYUSD −1.33 vs +1.35)
  plus window effects (TOPIX −6.61 vs +2.29: our series starts at the 1988 bubble peak, A3)
  and roll methodology (NATGAS +9.68 vs −9.74, A9). Flagged for inspection per instruction.
- **T2 (232 cells):** Panel A 56/64 Tier 1 (88%), 2 FAIL (k24 h36/h48: paper −0.09/−0.33,
  near-zero noise); Panel D bonds 15/40 Tier 1, 0 FAIL (ours +3..+5 vs paper +1..+3.5 —
  direction and significance match; strength likely from unscaled A5 bond vols); Panel C
  equities 12/64 Tier 1, 23 FAIL (ours positive k≥6 but ~1.0-1.9 vs paper 2-4; k≥24 small-value
  sign noise); Panel B commodities 15/64 Tier 1, 33 FAIL (ours short-lookback alphas negative —
  short-term reversal in our commodity series — and weak at long horizons).
- **A2 proxy check (Panel B):** the EW-commodity GSCI proxy does NOT absorb the commodity
  strategy (beta 0.19, corr 0.04 at k12h1; intercept-only t +2.14 → full-model +1.89). Panel B
  shortfall is signal-level (roll gaps W8, series differences), not a regression artifact.
- **Artifacts for iteration 4:** data/strategy_artifacts.parquet — per-instrument k=12 Eq.(5)
  returns (tsmom_*, passive_*), diversified + per-class TSMOM/PASSIVE factors, MKT/BOND/GSCI
  proxies, 300 months (1985-01..2009-12).

# Worker notes (inner iteration 4, 2026-07-22) — Tables 3/4/5, figures, strict recount

- **Strict recount:** eval_t1.csv / eval_t2.csv rewritten with the per-cell committed
  tolerance_pct column. Counts unchanged from iteration 3 (evaluate.py already applied
  per-metric tolerances from the JSON — T2: 40% for |paper t|≥2, 200% for noise cells).
- **T3 Panel A (22 cells: 14 Tier 1 / 2 Tier 2 / 6 FAIL):** alpha +1.198%/mo t 5.85
  (paper 1.58, t 7.99 — Tier 1); quarterly +3.492%/qtr t 5.22 (4.75, 7.73); UMD beta
  0.229/0.326 (t 5.39/4.15) Tier 1; MKT-proxy beta 0.032 (t 0.72) Tier 1 (paper 0.09, t 1.89);
  R² 0.116/0.204 Tier 1. The 6 FAILs are SMB/HML coefficient + t-stat cells — insignificant
  in BOTH paper and ours (all |t| ≤ 2.0); near-zero sign instability, not signal disagreement.
- **T4 (20 cells: 14/3/3):** within-class TSMOM correlations match (com 0.086/0.07, eq
  0.488/0.37, fi 0.296/0.38, fx 0.228/0.10) as do passive eq/fi/com (0.67/0.54/0.15 vs
  0.60/0.63/0.19). 3 FAILs are passive-FX cells: ours positive (+0.44 within, +0.31 vs com)
  vs paper −0.04/−0.12 — A6 artifact (IMM futures carry common USD-funding dynamics absent
  from the paper's spot+IBOR forward construction).
- **T5 Panel C (40 cells: 17/15/8):** XSMOM_ALL on TSMOM beta 0.716 (t 16.28), R² 0.471
  (paper 0.66, 15.17, 0.44 — all Tier 1; A11 normalization validated at the aggregate).
  UMD beta 0.413 (5.64) Tier 1 (paper 0.49/6.56); HML row all Tier 1. Per-class XSMOM betas
  weaker than paper (COM 0.45 vs 0.65; EQ 0.10 vs 0.39; FI 0.09 vs 0.37; FX 0.24 vs 0.75 —
  Tier 2; within-class cross-sectional momentum is weaker in the futures-only universe).
  8 FAILs are near-zero alpha/beta cells (SMB row ×4, UMD alpha ×2, XSMOM_FI alpha ×2),
  insignificant on both sides.
- **Figures:** results/tsmom_factor_vs_passive.png (Fig. 3; TSMOM dominates passive),
  sharpe_by_instrument.png (Fig. 2; 49/54 signal-bearing instruments positive vs paper's
  58/58; the 5 negatives are CATTLE −0.10, COTTON −0.17, GILT −0.09, SOYMEAL −0.05,
  USLONG −0.03 — all documented W8/W9/A5 instruments; SEKUSD has no 12-month signal),
  tsmom_smile.png (Fig. 4; positive quadratic curvature +0.0044 = straddle/smile pattern;
  2008Q4 annotated: SP500 futures deep-negative quarter, TSMOM strongly positive).

---

## Iteration log (Stage 7 inner loop)

(populated per inner iteration)
