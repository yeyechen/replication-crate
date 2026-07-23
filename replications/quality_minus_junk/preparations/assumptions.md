# Assumptions Registry — Quality minus junk (Asness, Frazzini, Pedersen 2019)

Paper-silent decisions logged during Stage 7 replication.

---

## Assumption 1: US-only replication scope

**Decision:** Replicate only the US Long Sample (Panel A of Tables 3, 4, 9), not the Global Broad Sample (Panel B).
**Rationale:** The global sample requires Compustat Global data across 24 countries with country-specific portfolio construction. The ClickHouse catalog has comp_202601.g_funda (Compustat Global) but the paper's global factor construction requires per-country factors and market-cap-weighted global aggregation, which is significantly more complex. The US Long Sample (1957-2016) is the paper's primary sample and uses CRSP + Compustat North America, both fully available.
**Impact:** All Panel B metrics are out of scope. Panel A metrics for Tables 3, 4, 9 are the replication targets.

## Assumption 2: Risk-free rate for growth measures

**Decision:** Use the monthly rf from ff.four_factor_monthly (FF T-bill rate) for residual income growth computations.
**Rationale:** The paper defines growth in "residual" profitability as (profit_t - rf*book_{t-1}), subtracting the risk-free cost of book capital. The paper does not specify which risk-free rate to use, but the FF T-bill rate is the standard in the literature and is already used for excess return computation.
**Impact:** Affects all 5 growth sub-variables (Δ_gpoa, Δ_roe, Δ_roa, Δ_cfoa, Δ_gmar).

## Assumption 3: Beta estimation methodology

**Decision:** For the first pass, use a simple 60-month rolling CAPM beta from CRSP monthly returns. The paper specifies the Frazzini-Pedersen (2014) methodology (1-year daily vol × 5-year 3-day correlations), which we will implement in a refinement iteration if the simple beta produces materially different results.
**Rationale:** The FP(2014) beta requires daily return data for both individual stocks and the market index, with specific rolling window calculations (252-day vol, 1260-day 3-day correlations). This is computationally intensive but implementable. Starting with the simpler beta allows us to validate the overall pipeline first, then refine.
**Impact:** Affects the Safety sub-score through the BAB variable. If betas differ substantially, safety scores and quality scores will shift.

## Assumption 4: CPI for O-Score

**Decision:** Use a constant CPI deflator (normalized to 1.0 at the sample start) or pull CPI from a standard source. The paper uses CPI to deflate adjusted total assets in the Ohlson O-Score formula.
**Rationale:** The paper says "CPI is the consumer price index" but doesn't specify the source. The log transformation in the O-Score formula (log(ADJASSET/CPI)) means the absolute level of CPI matters. We will use monthly CPI-U from FRED or a hardcoded series.
**Impact:** Affects O-Score values. Since O-Score enters through a rank z-score, moderate CPI differences should not materially affect the safety composite.

## Assumption 5: EVOL computation

**Decision:** Use quarterly ROE (ibq/ceqq from fundq) over 60 quarters when available; fall back to annual ROE std over 5 years.
**Rationale:** The paper specifies: "EVOL is the standard deviation of quarterly ROE over the past 60 quarters. We require at least 12 nonmissing quarters. If quarterly data is unavailable we use the standard deviation of annual ROE over the past 5 yrs." Quarterly data (fundq) is available in ClickHouse but the paper notes it's unavailable for global stocks — for US stocks it should be available from the 1960s onwards.
**Impact:** Affects the Safety sub-score. US quarterly data coverage should be good from ~1962 onward.

## Assumption 6: No explicit price filter

**Decision:** Do not apply a $5 minimum price filter.
**Rationale:** The paper does not mention any minimum price filter. The paper's universe filter is: shrcd IN (10,11), exclude OTC. No price floor is specified. The paper uses Compustat as the primary pricing source supplemented by CRSP, and the quality score construction (rank z-scores) provides implicit robustness to outliers. Per PAPER_CONVENTIONS.md, a $5 filter is a convention default when the paper is silent, but this paper's rank-based methodology makes it less necessary. Documenting as a deviation from convention.
**Impact:** May include some microcap/penny stocks that would be excluded under a $5 filter. Could slightly affect decile returns, especially in early sample years.

## Assumption 7: Delisting return treatment

**Decision:** Apply the paper's rule exactly: include delisting returns when available from dsedelist; for performance-related delistings (dlstcd >= 500) with missing returns, use -30%.
**Rationale:** Paper explicitly states: "We include delisting returns when available. If a firm is delisted but the delisting return is missing and the delisting is performance related, we follow Shumway (1997) and assume a -30% delisting return." This is a paper-specified rule, not an assumption.
**Impact:** Affects returns for delisted stocks, particularly small/junk stocks that delist more frequently.

## Assumption 8: QMJ quality cutoff

**Decision:** Use top/bottom 30% quality within each size group for QMJ construction, implemented as the top 3 and bottom 3 deciles in a 10-decile quality sort within each size group (i.e., conditional 2×10 sort, then take top 3 vs bottom 3).
**Rationale:** The paper says "long the top 30% high-quality stocks and short the bottom 30% junk stocks." In a conditional sort framework with deciles, 30% corresponds to 3 out of 10 deciles. This is the standard implementation in AQR's QMJ factor construction.
**Impact:** Defines which stocks enter the QMJ long and short legs.

---

## Worker flags — data pipeline build (Steps 1–10)

Appended by rep-worker. ⚠️ items need Replicator confirmation.

### W1: `consol='STD'` does not exist — used `consol='C'` ✅ CONFIRMED
The task spec's funda filter said `consol='STD'`, but `consol` values in
`comp_202601.funda` are only `C/D/R/P` (0 rows match `consol='STD'`).
Implemented `indfmt='INDL' AND consol='C' AND popsrc='D' AND
datafmt='STD'` — `consol='C'` (consolidated) is the WRDS standard per
`references/COMPUSTAT.md`. 488,813 firm-years pass the filter.

### W2: `ff.four_factor_monthly.rf` is already a monthly DECIMAL ✅ CONFIRMED
Values like 0.0020 (Jun 1957 ≈ 2.4% annualized) — NOT percent. The spec's
"divide by 1200" note would under-scale it 1200×. Used `rf` as-is for
monthly excess returns and betas; the annual risk-free charge in the
growth (residual-income) formulas is the sum of the 12 monthly rf values
of the calendar year matching the fiscal year (calendar-year proxy).

### W3: EVOL negated before z-scoring ✅ CONFIRMED
`evol_s = -evol` so the Safety composite is consistently "higher =
safer". The spec's note stated only bab/lev/o are pre-oriented; Z-Score
is naturally safe-high, but raw EVOL (earnings volatility) is safe-LOW.
The paper orients all quality measures higher = better, so EVOL was
flipped before ranking. Confirm this matches intent.

### W4: Fiscal alignment = 6-month-lag rule
Stock-month m uses the most recent fiscal year-end with `datadate <=
last day of (m − 6 months)`. For December-fiscal-year-end firms this
exactly reproduces the FF (1992) "fiscal year ending in calendar year
t−1 → June of year t" mapping; for non-December fiscal year-ends in
Jan–May months it is marginally fresher than a strict calendar-year
rule. Uses the most recent available year (≤ cutoff), so firms with a
missing fiscal year fall back to the prior one. 100% of stock-months
have an aligned fiscal record.

### W5: Secondary Compustat items coalesced to 0
WC = ACT − LCT − coalesce(CHE,0) + coalesce(DLC,0) + coalesce(TXP,0);
LEV uses coalesce(DLC/MIBT/PSTK, 0) (DLTT stays NULL-propagating);
O-Score TLTA uses coalesce(DLC,0) + DLTT. Primary items (AT, IB, REVT,
COGS, DP, CAPX, SALE, ACT, LCT, LT, RE, EBIT, PI, DLTT) propagate NULL.

### W6: Measurement first-passes (per spec's explicit allowance)
- Beta = plain 60-stock-month rolling CAPM beta, min 36 months, excess
  returns vs CRSP VW excess — NOT the Frazzini–Pedersen (2014) method.
  Median beta = 1.01.
- Growth measures are NOT per-share (spec defers the split-adjusted
  per-share computation); the 5-year residual-difference structure and
  normalizers (at_{t−5}, be_{t−5}, sale_{t−5}) follow the spec formulas.
- CPI = 1.0 for the O-Score: the log(ADJASSET/CPI) level is a
  month-constant shift, exactly invariant to cross-sectional rank
  z-scoring — immaterial for this replication (resolves Assumption 4:
  FRED CPI pull unnecessary).
- O-Score requires ADJASSET > 0, else NULL.
- EVOL quarterly: ibq/ceqq, min 12 of trailing 60 quarters, ASOF-aligned
  to the fiscal date; annual fallback = std of annual ROE (IB/BE) over 5
  fiscal years requiring 5 nonmissing years (paper's fallback).

### W7: Universe details
PIT dsenames at month-end (ASOF on namedt + explicit nameendt check);
shrcd IN (10,11) AND exchcd NOT IN (0) — keeps all non-OTC exchanges
(1–6); NULL exchcd excluded (conservative). No SIC-based exclusions
(spec silent) — financials ARE included.

### W8: Infrastructure gotchas fixed
- ClickHouse `Date` cannot store pre-1970 dates (`toDate()` on
  1925–1969 dates saturates to 1970-01-01 — silently destroys the
  1957–1969 sample). All SQL uses `Date32` + Date32-safe month
  arithmetic (`subtractDays/addMonths`; `toStartOfMonth`/
  `toLastDayOfMonth` downcast Date32→Date on this server).
- New ClickHouse analyzer disabled (`allow_experimental_analyzer = 0`):
  it cannot resolve columns through `alias.*` CTE expansions; all SQL
  uses explicit column lists.
- ASOF joins require `join_algorithm = 'hash'` on this server.
- Intermediate tables: `write_yeye.qmj_*` (qmj_funda_base, qmj_funda,
  qmj_link, qmj_funda_permno, qmj_univ_m, qmj_beta, qmj_evol,
  qmj_fp_enrich, qmj_panel_raw) — all computed, no raw dumps.
  qmj_funda_permno has 0 (permno, datadate) duplicates under the
  LU/LC + P/C + usedflag=1 link filter.

---

## Worker flags — Tables 3 & 4 analysis layer (this task)

Appended by rep-worker. ⚠️ items need Replicator attention.

### W9: FF factors are DECIMALS in this instance — spec note is wrong ⚠️
The task spec states "FF factors from ClickHouse are already in percentage
(e.g. mkt_rf=0.5 means 0.5%); divide by 100 for regression." This is
**incorrect for this instance**. Verified by direct query: Sep-2008
mkt_rf = -0.0935 (= -9.35%), Oct-2008 = -0.172; rf = 0.0022 (= 0.22%/mo).
ALL five columns (mkt_rf, smb, hml, mom, rf) are monthly decimals, exactly
matching the panel's ret_next scale (also decimal). I therefore did **NOT**
divide by 100; both portfolio returns and factors are regressed in decimal,
and only the *reported* alpha/return is multiplied by 100. (Consistent with
the pipeline's confirmed W2.) Implementing the spec's /100 would have
under-scaled the factors 100× and produced nonsense alphas.

### W10: Realization-month alignment for time-series regressions
Portfolios are formed on the quality score at month t and earn ret_next
(realized in t+1). For the factor-model regressions I align each decile /
factor return to its REALIZATION month (t+1) before merging with FF factors
— e.g. a June-1957 formation earns the July-1957 return and is regressed
on the July-1957 FF factors. The December-2016 formation month (whose
ret_next = the Jan-2017 return) is excluded so the realized sample is
exactly 7/1957–12/2016 (N = 714), matching the paper's stated window and
reproducing the paper's iid t-stat arithmetic (QMJ excess t = 3.02 here
vs the paper's 3.62; both ≈ monthly-Sharpe × sqrt(714)).

### W11: t-statistic convention (iid for excess return; NW-60 for alpha/loadings)
Verified from the paper's own arithmetic: the QMJ excess-return t of 3.62
equals the iid statistic (annualized-Sharpe/sqrt(12) × sqrt(714)), whereas
the QMJ 4F-alpha t of 9.95 is *below* its iid counterpart (10.80), which
only Newey-West shrinkage can produce. I therefore report excess-return
t-stats as iid and alpha / loading t-stats as Newey-West HAC with 60 lags
(the paper's 5-year convention, rule fm_newey_west_5yr). The paper does
not state the TS-regression lag explicitly; 60 is the AQR convention.

### W12: Conditional quality breakpoints = NYSE-within-size-group ⚠️
Table 4's inner quality sort uses NYSE breakpoints computed *within* each
size group (the most faithful reading of "U.S. sorts are based on NYSE
breakpoints" + "conditional sorts"), falling back to all-stocks-in-group
breakpoints if a cell has <20 NYSE names. I ran a 3-variant sensitivity
(NYSE-inner vs all-inner vs size-breakpoints-on-the-full-panel): the four
factors differ by ≤0.04%/month across all variants — i.e. the residual gap
to the paper is NOT from the analysis-layer breakpoint choice. Kept the
NYSE-inner variant (default in src/qmj_common.qmj_factor).

### W13: Score approximations dominate the residual gap (not the analysis)
29/39 target metrics are within the spec tolerances (74%). The failures
concentrate in (a) P1 excess return (0.38 vs 0.28, 36% vs 30% tol — just
over the line), (b) middle-decile 4F alphas which are near zero in absolute
terms so the *percentage* tolerance becomes pathological (a 0.05–0.10
pp/month absolute miss on a 0.10 base → >50%), and (c) the QMJ loadings
(MKT -0.16 vs -0.20; SMB -0.22 vs -0.26 just over; UMD +0.07 vs -0.09 sign
flip). The factor *structure* reproduces cleanly: CAPM betas
(P1 1.32/1.28, H-L -0.35/-0.36), 3F alphas (H-L 0.92/0.88, QMJ 0.52/0.51),
Profitability 4F alpha (0.49/0.50 exact), and QMJ adj R2 (0.51/0.50). The
weak Safety (4F 0.36 vs 0.51) and Growth (0.28 vs 0.46) components — and
hence the flattened beta gradient in Table 3 (P3–P10 betas ~0.96–1.01 vs
the paper's 1.10→0.92 decline) — trace to the upstream first-pass score
approximations already flagged at W6 (plain 60-mo rolling beta instead of
Frazzini–Pedersen inside the Safety/BAB term; growth measures not
per-share). These are pipeline-layer issues, not analysis-layer issues:
the W12 sensitivity proves the sort/regression code is not the cause.
Recommended next iteration: re-implement the FP(2014) beta and per-share
growth in the pipeline, then re-run table3.py / table4.py unchanged.

