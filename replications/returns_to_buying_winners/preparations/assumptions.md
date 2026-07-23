# Assumptions Registry — Returns to Buying Winners (Jegadeesh & Titman 1993)

Paper-silent decisions made by the replicator. Paper-derived rules live in
`preparations/preprocessing_rules.json` (verbatim quotes). Updated every
inner-loop iteration.

---

## Assumption 1: Share-code filter for the NYSE/AMEX universe

**Decision:** Restrict the universe to common shares, `shrcd IN (10, 11)`,
applied point-in-time via `crsp_202601.dsenames` validity windows
(`namedt`/`nameendt`), together with `exchcd IN (1, 2)` (NYSE + AMEX).
**Rationale:** The paper says "Our analysis of NYSE and AMEX stocks" (L85)
and "All stocks with available returns data in the J months preceding the
portfolio formation date are included" (L125) — it states the exchanges but
is silent on share codes. Restricting to ordinary common shares (10/11) is
the standard convention in `rep/PAPER_CONVENTIONS.md` and excludes ADRs,
closed-end funds, REITs, and units, whose return behavior is not what the
paper's decile sorts are about. PIT windows prevent the "ever-valid permno"
look-ahead error (a security that was a fund in the 1970s but a common
stock later must not enter the 1970s sample).
**Impact:** Universe composition for every cell of Tables I–VII.

## Assumption 2: No minimum-price filter (deviation from convention default)

**Decision:** Do NOT apply the conventional $5 minimum-price filter.
**Rationale:** `rep/PAPER_CONVENTIONS.md` defaults to a $5 floor when the
paper is silent, but this paper is not silent: L125 says *all* stocks with
available returns data are included, without a price screen. Adding a price
filter would drop exactly the small, volatile loser-decile stocks whose
behavior drives the January-effect and beta results; it would be an
invented rule (STUCK_AGENT_GUIDELINE Rule 1).
**Impact:** Loser-decile composition, Tables I–VII (especially Table IV
January cells, Table II P1 beta/mcap).

## Assumption 3: Delisting-return treatment

**Decision:** Monthly returns are compounded from daily returns; when a
stock delists mid-month, the month's compounded return is multiplied by
`(1 + dlret)` from `crsp_202601.dsedelist`. Where `dlret IS NULL` and
`dlstcd >= 500` (performance-related delisting), substitute −0.30 (the
NYSE/AMEX convention of Shumway 1997 / BMP 2007). No NASDAQ stocks are in
the universe, so the −0.55 NASDAQ case never applies.
**Rationale:** The paper is silent on delisting treatment (L139 only
describes the data source). Dropping delisted stocks without their
delisting return biases loser-decile returns upward (delistings
concentrate among past losers). The −0.30 fallback for missing
performance-delisting returns is the conservative literature standard;
the current CRSP vintage populates `dlret` for the large majority of
post-1962 performance delistings, so the fallback applies to few months.
**Impact:** Sell (loser) decile returns in every table; most visible in
Table I sell-portfolio means and Table VII year-2 returns.

## Assumption 4: Panel B "skip a week" implementation

**Decision:** For Panel B strategies, the first holding month's return of
each cohort is the compounded daily return from the 6th trading day of
that month to month end (skipping the first 5 trading days); all later
holding months are full calendar months, with equal-weight rebalancing at
each month start.
**Rationale:** The paper says portfolios "are formed 1 week after the
lagged returns used for forming these portfolios are measured" (L157) to
avoid bid-ask, price-pressure, and lagged-reaction effects at the
turn of the month (L109), but does not specify how the skip interacts
with calendar-month reporting and monthly rebalancing. Skipping the first
trading week of the first holding month implements the stated motivation
directly while preserving the calendar-month overlap aggregation used
throughout the paper. The alternative (off-calendar 21-trading-day
holding months) would break the calendar-month alignment of the reported
averages; the alternative (skip the entire first month) is a 1-month skip,
not a 1-week skip.
**Impact:** All 96 cells of Table I Panel B.

## Assumption 5: t-statistic convention for monthly strategy returns

**Decision:** t-statistics on average monthly returns are plain
`mean / (std / sqrt(n))` over the calendar months of the sample
(n = 300 for 1965–1989 full-sample statistics), i.e., OLS/iid standard
errors. Newey-West HAC standard errors are used ONLY for the cumulative
event-time returns in Table VII (footnote 16, L1264) and the
squared-market-return regression in Section III.D ("autocorrelation-
consistent", L526).
**Rationale:** The paper reports plain parenthesized t-stats in Tables
I/III/IV/VI and explicitly flags Newey-West only where overlapping
cumulative returns require it (L1264). Back-solving the paper's t-stats
(e.g., 6/6 buy-sell 0.0095, t = 3.07 → monthly std ≈ 0.0537) is
consistent with the iid formula over 300 months.
**Impact:** Every t-stat cell in Tables I, III, IV; cumulative-return
t-stats in Table VII.

## Assumption 6: Table II post-ranking beta estimation

**Decision:** For each decile (and the zero-cost P10–P1) portfolio of the
6-month/6-month strategy, build the calendar-month return series over
Jan 1965 – Dec 1989 (each month = average of the 6 overlapping cohorts'
decile returns, same series as Table I/III), and estimate beta as the
slope of an OLS regression of that series on the CRSP value-weighted
index return (from `crsp_202601.dsi.vwretd`) over the same months.
Average market capitalization is the time-series average, across cohort
formation months, of the equal-weighted average of member stocks'
end-of-formation-month market caps (|prc| × shrout × 1000, $ millions).
**Rationale:** The paper reports "post-ranking betas ... with respect to
the value-weighted index" (L396, L408) without specifying the estimation
window. Regressing the reported (overlapping) portfolio return series on
the market over the full sample is the interpretation consistent with
"post-ranking" (returns after portfolio formation) and with the paper's
use of the same monthly strategy series elsewhere; the cohort-by-cohort
alternative (6 observations per regression) is statistically degenerate.
**Impact:** All 21 cells of Table II.

## Assumption 7: Size-tercile formation frequency (Tables III–VI)

**Decision:** For the size-based subsamples (S1 small, S2 medium, S3
large), stocks are sorted into terciles of end-of-formation-month market
capitalization at EVERY monthly formation date (tercile breakpoints
recomputed each month from the in-universe cross-section).
**Rationale:** The paper says it implements the 6/6 strategy "on three
size-based subsamples (small, medium, and large)" (L542) and Table III's
caption defines S1–S3 (L603) but is silent on whether size sorts are
annual or monthly. Monthly sorts are the natural companion to a
monthly-formation strategy and use the same formation-date market cap
already computed for the signal; annual sorting would add an unbacked
convention. (If Table III cells miss tolerance, annual end-of-year
sorting is the first revision to try — logged here per STUCK guideline
Rule 3: the alternative is named before the first attempt.)
**Impact:** All S1/S2/S3 cells in Tables III and IV.

## Assumption 8: Scholes-Williams beta estimation (Table III beta subsamples)

**Decision:** At each formation month in calendar year Y, each stock's
Scholes-Williams beta is estimated from DAILY returns over the prior
calendar year (Y−1) against the CRSP value-weighted daily index:
beta_SW = (beta_lead + 2·beta_contemp + beta_lag) / 2, where the three
slopes come from regressions of the stock's daily return on the
contemporaneous, one-day-lagged, and one-day-led index return. Stocks
are then split into terciles (β1 low, β3 high) at each formation month.
**Rationale:** Table III's caption says the β-subsamples contain "the
firms with the smallest, medium, and the largest Scholes-Williams betas
estimated from the returns data in the calendar year prior to portfolio
formation" (L603). The Scholes-Williams (1977) lead-lag correction formula
is the estimator named; daily betas are confirmed by footnote 11
("obtained with daily betas", L552). The paper does not specify the
factor index — the value-weighted index is used throughout the paper as
the market proxy (L526), so it is used here.
**Impact:** All β1/β2/β3 cells in Table III.

## Assumption 9: Table III Panel B market-model regression

**Decision:** Panel B alphas are intercepts from OLS time-series
regressions of each portfolio's monthly return series (same overlapping
strategy series as Panels A) minus the risk-free rate on the CRSP
value-weighted index return minus the risk-free rate, over Jan 1965 –
Dec 1989 (300 monthly observations). The risk-free rate is
`ff.four_factor_monthly.rf` (1-month T-bill, decimal, verified available
from 1965-01). Reported values are the intercepts (monthly decimals);
t-stats are OLS.
**Rationale:** L564–567: "risk-adjusted returns are estimated as the
intercepts from the following market model regression:
r_pt − r_ft = α_p + β_p(r_mt − r_ft)". The value-weighted index is the
paper's market proxy (Panel B caption, L764). No HAC correction is
mentioned for these regressions, so plain OLS standard errors are
reported (consistent with Assumption 5).
**Impact:** All 161 cells of Table III Panel B.

## Assumption 10: Event-time cohort window (Table VII)

**Decision:** Event-time month m averages the zero-cost (buy − sell)
return of all formation cohorts formed Jan 1965 – Dec 1989 for which
month m of the holding window falls on or before Dec 1989 (i.e., cohort
formed at t contributes to event months 1..min(36, 1989-12 − t)).
Cumulative returns are ARITHMETIC sums of the average monthly event-time
returns (verified: paper's cumulative at t=2, 0.0099 = −0.0025 + 0.0124).
t-stats on monthly event returns are iid mean/(std/√n) over contributing
cohorts; t-stats on cumulative returns use Newey-West with lag
truncation per footnote 16 (L1264) — default lag = int(4·(T/100)^(2/9))
on the calendar-month series of cumulative-by-cohort values.
**Rationale:** The paper tracks "each of the 36 months following the
portfolio formation date" (L1254) over the 1965–1989 sample; since the
paper's data file ends Dec 1989, later cohorts simply have fewer
available horizons. Membership is fixed at formation and rebalanced
monthly to equal weights (L113: "the rebalanced returns ... are also
used in the event study presented in Section VI").
**Impact:** All 144 cells of Table VII.

## Assumption 11: Data vintage

**Decision:** Use `crsp_202601` (2026 CRSP vintage) for returns,
delistings, names, and indexes; monthly returns are RECOMPUTED by
compounding daily returns (not taken from `msf`), matching the paper's
"Monthly returns were obtained by compounding the daily returns" (L139).
**Rationale:** `crsp_202601` is the latest vintage per
`rep/PAPER_CONVENTIONS.md`; the paper's 1990 vintage is unavailable.
CRSP return histories for 1962–1989 are stable across vintages (the
catalog notes stock-file stability within recent vintages), so residual
vintage differences are expected to be small and fall within the
per-cell tolerances.
**Impact:** All cells; magnitude of any residual vintage drift is
quantified in REPORT.md.

---

## Iteration log (Stage 7 inner loop)

(filled in as iterations run — each entry: Problem / Diagnosis / Next fix
/ Before metric / After metric / Status)

### Inner iteration 2 — Table I (rep-worker, 2026-07-22)

**Problem:** Table I computed end-to-end; central cell PA 6/6 buy-sell =
0.0125 vs paper 0.0095 (+31.7%).

**Diagnosis (characterization, no construction change — per task spec):**
- Construction integrity verified: hand-computed 1979-12 J=6 cohort
  (decile cutoffs, sizes, next-month EW returns) matches the pipeline to
  < 1e-12; every one of the 300 months has exactly K contributing cohorts
  in all 32 (panel, J, K) grids; PA 6/6 buy t-stat = 4.3297 vs paper 4.33
  (−0.0%) on 300 months.
- Deviation is entirely on the SELL side and has the signature of the
  Assumption A3 delisting-return adjustment (whose stated Impact is
  "most visible in Table I sell-portfolio means"):
  - Buy side: all 32 means within ±16% (median |dev| 6.2%); all 32
    t-stats within ±5% median. PA 6/6 buy 0.01766 vs 0.0174 (+1.5%).
  - Sell side: systematically LOW, shortfall monotonically DECREASING in
    K (PA: −53% at J3/K3 → −35% at J6/K6 → −9% at J12/K12) — fresh loser
    portfolios carry the most delisting losses; the drag decays as the
    fixed membership drifts. Panel B sell is lower still at K=3 (the
    skip removes the turn-of-month loser bounce — direction matches the
    paper's PA→PB drop, magnitude larger).
  - Sell std matches (0.0842 vs ≈0.0868); only the mean is low — a
    location shift, not a variance/construction problem.
  - Order-of-magnitude check: 2,511 dlret adjustments + 355 × (−0.30)
    fallbacks over 330 months, concentrated in loser deciles (~216
    stocks/decile), imply ≈ 0.002–0.003/month drag on the sell mean —
    the size of the gap (0.0079 − 0.0051 = 0.0028).
- Literature context: JT93's 1990 CRSP vintage pre-dates systematic
  dlret incorporation; Shumway (1997) / Shumway-Warther (1999) document
  that unadjusted CRSP loser-decile returns are biased UPWARD by
  ≈ this magnitude. Our A3-adjusted series removes that bias, which
  raises buy-sell spreads (ours above the paper everywhere, largest at
  short K).

**Next fix (Replicator's decision, not the worker's):** A3 is a
registered methodology assumption; options are (a) keep A3 and accept
the sell-mean deviations as the documented cost of delisting adjustment
(buy side and all long-horizon spreads already replicate), or (b) add a
no-dlret variant of `ret` to the panel and report Table I with it. The
construction machinery (ranking, deciles, overlap, rebalancing, t-stats)
is validated either way.

**Status:** 192/192 metrics computed and written. Within ±10%: 82/192;
within ±30%: 144/192 (buy-side cells and long-K spreads cluster tight;
short-K sell cells drag the count).

---

## Panel-stage implementation notes (rep-worker, 2026-07-22)

Implementation-level resolutions under Assumptions 1–4 above (no new
methodology; flags for the Replicator):

- **P1 (Assumption 3, verified):** on this CRSP vintage `dsf.ret` does NOT
  embed `dlret` — for 3 month-end delistings with msf rows, `msf.ret`
  equals the raw daily compound (|M−D| ≤ 2e-6) and differs from
  `(1+D)(1+dlret)−1` by the full dlret. The multiplicative adjustment
  therefore does not double count. Also note `msf.ret` in this vintage
  EXCLUDES dlret (unlike some older conventions).
- **P2 (Assumption 3):** `dlret < -1.0` (CRSP sentinels) → NULL before the
  adjustment; 0 sentinels found in 1962-07..1989-12 (2,042 genuine NULLs).
  2,882 in-universe delisting stock-months: 2,511 dlret applied, 355
  −0.30 fallback (dlstcd ≥ 500, missing dlret), 16 missing-dlret
  non-performance cases (dlstcd < 500) adjusted by 0.
- **P3 (Assumption 4):** `ret_skip5` carries NO delisting adjustment
  (spec: plain daily product from the 6th trading day). If a cohort stock
  delists after day 5 of its first Panel B holding month, that month's
  skip-5 return omits dlret. Small population; flagged.
- **P4 (Assumption 4):** the day-rank for the skip is over valid-return
  days (sentinel/missing-return days excluded before ranking), i.e. rank
  k = k-th day with a valid return for that permno-month.
- **P5 (Assumption 1):** universe counts peak at 2,449 stocks/month (1975;
  range 1,955–2,534) — above the 1,200–2,100 rough band but NYSE + AMEX
  *combined*; NYSE alone would be ~1,300–1,700. PIT join verified 1:1 at
  (permno, date); no dsenames-window duplication in the period.
- **P6:** the panel keeps a "ghost" row (ret/me NaN, cumret present) for
  the month after a stock leaves the universe, so formation cross-sections
  stay complete per L125 (3,172 rows, 0.44%). Downstream sorts should key
  on cumret_J; NaN holding returns drop out of EW averages.
- **P7:** missing daily returns (CRSP sentinels in `dsf.ret`, i.e. values
  < −1) are dropped before compounding — equivalent to 0% on those days,
  the standard convention.
- **P8 (data gotcha):** ClickHouse `Date` saturates pre-1970 dates to
  1970-01-01 (and `toStartOfMonth(toDate32(x))` returns `Date`, also
  saturated) — all month keys in `src/sql/*.sql` are `'YYYY-MM'` strings;
  the parquet `month` is converted to datetime64 in Python.
- **P9 (units, verified):** `dsi.totval` is in thousands of dollars
  (3.306e9 on 1989-12-29 = $3.306T vs $3.357T from
  sum(abs(prc)*shrout*1000) over all dsf stocks, 1.52% gap) — confirms
  `me_millions = abs(prc)*shrout*1000/1e6`.
- **P10 (Assumption 5, Table I stage):** the iid t-statistics are
  computed directly as `mean/(std(ddof=1)/sqrt(n))` in `src/main.py`
  (`iid_tstat`). `utils.metrics.tstat_newey_west(s, n_lags=0)` is NOT
  bit-identical: statsmodels' HAC kernel omits the n/(n−1) df
  correction, so its 0-lag t-stat is larger by sqrt(n/(n−1)) (verified:
  2.6238 vs 2.6194 at n=300, +0.17%). For Table VII's autocorrelation-
  consistent t-stats the NW primitive with n_lags per footnote 16 IS
  the right tool.

---

## Assumption 3 — REVISION (Replicator, inner iteration 3): delisting treatment

**Decision (revised):** The PRIMARY analysis uses UNADJUSTED monthly
returns — daily compounds with NO `dlret` applied and NO −0.30 fallback —
for BOTH the formation signal (`cumret_J`) and the holding returns. The
delisting-adjusted series (`ret_adj`, `cumret_J_adj`) is retained in the
panel and reported as a sensitivity analysis in REPORT.md.

**Before metric:** adjusted series — PA 6/6 sell 0.005143 (paper 0.0079,
−34.9%); buy 0.017656 (paper 0.0174, +1.5%); buy-sell 0.012513 (paper
0.0095, +31.7%). Discrepancy is a pure sell-side LOCATION shift: sell std
0.0842 ≈ paper 0.0868; buy side matches at <2%; shortfall monotonically
DECREASES in K (−53% at J3/K3 → −9% at J12/K12) — the exact signature of
delisting drag concentrated in fresh loser portfolios.

**Rationale (evidence chain):**
1. The paper compounded daily returns to monthly ("Monthly returns were
   obtained by compounding the daily returns recorded in this data set",
   L139) on the 1990 CRSP vintage, where dlret codes were systematically
   missing for performance delistings — Shumway (1997) and
   Shumway–Warther (1999) document precisely this upward bias in THIS
   paper's loser portfolios. The paper never mentions delisting
   adjustment; it could not have applied one with its data.
2. Empirically verified on our vintage (inner iteration 1, P1): CRSP's
   OWN monthly compounding (`msf.ret`) excludes `dlret` — for 3 month-end
   delistings, `msf.ret` equals the raw daily compound to 2e-6 and differs
   from `(1+D)(1+dlret)−1` by the full dlret. The unadjusted daily
   compound is the series consistent with both the paper's stated
   procedure and CRSP's own monthly file.
3. The −0.30 fallback (355 events) and dlret application (2,511 events)
   impose a modern correction the paper's numbers never contained —
   keeping it as PRIMARY would replicate what the paper SHOULD have
   computed, not what it DID compute. The replication target is the
   paper's reported values.

**Impact:** every sell-side and buy-sell cell in all 5 tables (primary
series now unadjusted). The delisting bias remains quantified: the
adjusted-vs-unadjusted difference on the 6/6 series is reported in
REPORT.md as the magnitude of the known CRSP delisting bias in our
vintage (Shumway correction context).

**Status:** fix committed; re-run Table I on the unadjusted series in
inner iteration 3 (one change; before/after metrics in logs/log1.md).

---

## Panel-stage implementation note P11 (rep-worker, inner iteration 3, 2026-07-22)

- **P11 (A3-revision):** `data/panel.parquet` now carries BOTH delisting
  treatments (728,207 rows × 15 cols): `ret_raw` = plain
  `exp(sum(log(1+ret)))−1` over the month's valid days, no dlret; `cumret_J_raw`
  compounded from `ret_raw` (same `count=J` window semantics); `ret_skip5_raw`
  = `ret_skip5` by construction (skip5 never carried the adjustment — P3),
  carried as its own column so the raw column set is self-contained.
  Verified: `ret_raw` nulls = `ret` nulls = 3,172 (≤ holds with equality);
  `cumret_J_raw` null% identical to `cumret_J` null% for J=3/6/9/12
  (2.1112 / 4.2059 / 6.2754 / 8.3171%). STUCK Rule 2 discipline: 5 random
  stock-months captured BEFORE rebuild (seed=7) — `ret`, `ret_skip5`,
  `cumret_3/6/9/12`, `me_millions` all bit-identical after rebuild
  (max|diff| = 0.0 on every column); only new `*_raw` columns were added.
  Ranking stability: at formation 1979-12, ranking on `cumret_J_raw` instead
  of `cumret_J` moves 0/2,209 (J=6), 0/2,174 (J=12), 2/2,223 (J=3),
  2/2,184 (J=9) stocks across deciles (0.00–0.09%) — membership is
  essentially invariant to the treatment. `ensure_panel` now cache-busts on
  missing required columns; `main.py` re-runs load the cached panel without
  touching ClickHouse.

### Inner iteration 3 — Table I on the raw (unadjusted) series (rep-worker, 2026-07-22)

**Fix:** one change — Table I PRIMARY recomputed on the unadjusted column set
(`cumret_{J}_raw` signal, `ret_raw` holding returns, `ret_skip5_raw` Panel B
first month). Machinery (formation_deciles / cohort_decile_returns /
strategy_monthly / compute_table1) parameterized by column set; adjusted
series retained and recomputed as the PA 6/6 sensitivity. No tuning.

**Before metric (adjusted, recomputed this iteration, same machinery):**
PA 6/6 sell 0.005143 (t=1.06; paper 0.0079, −34.9%); buy 0.017656 (t=4.33;
+1.5%); buy-sell 0.012513 (t=4.53; paper 0.0095, +31.7%).

**After metric (raw, PRIMARY):** PA 6/6 sell 0.006227 (t=1.28; −21.2%);
buy 0.017757 (t=4.36; +2.1%); buy-sell 0.011530 (t=4.17; +21.4%).
STOP-probe passed: |dev| improved +31.7% → +21.4% on the central cell.
Cohort-count invariant still exact (K cohorts in all 300 months, all 32
(panel, J, K) grids). Hand-check on RAW columns (formation 1979-12, J=6,
h=1): decile 1 EW next-month ret_raw = +0.100402, decile 10 = +0.120862,
both match the pipeline to < 1e-12.

**Delisting-bias measurement (adjusted − raw on PA 6/6 monthly means):**
sell −0.001085; buy −0.000101; buy-sell +0.000983 (sell-side concentrated,
as predicted by the A3-revision evidence chain; sell stds 0.084229 vs
0.084205 — variance untouched, pure location shift).

**192-metric tally:** within ±10%: 82 → 116; within ±30%: 144 → 162.
By side (raw): sell 28/64 (±10%), 50/64 (±30%); buy 59/64, 64/64;
buy-sell 29/64, 48/64. Sell shortfall now monotonically decreasing in K
(PA: −44% at J3/K3 → −21% at J6/K6 → 0% at J6/K12) and Panel B short-K
sell cells remain the worst (−54% to −64% at K=3) — the residual sell
gap is no longer explained by delisting adjustment (removed); remaining
candidates for the Replicator: vintage drift in small-loser daily returns
and/or the paper's undisclosed treatment of months with few valid days.
Short-K buy-sell t-stats run HIGH (+36% at PA 6/6) because our buy-sell
monthly std (0.0479) is BELOW the paper-implied 0.0537 even though the
mean is above — a variance-side counterpart of the same residual.

**Status:** 192/192 metrics recomputed on the PRIMARY series;
`results/computed_values.json` overwritten (192 keys, 6 dp), `table_1.md`
rewritten with the A3-revision header. Adjusted series reported as
sensitivity (side-by-side in the iteration-3 log / REPORT.md).

---

## Inner iteration 4 — Tables VII/II/IV + PART 0 sell diagnostic (rep-worker, 2026-07-22)

Implementation-level notes for the Tables 2/4/5 build (no new methodology;
flags for the Replicator). All work lives in `src/main.py`
(`sell_diagnostic`, `compute_table5`, `compute_table2`, `compute_table4`,
shared `merge_computed_values` / `load_targets` / `nw_tstat_hac`) plus three
new SQL files (`market_index_monthly.sql`, and the DIAGNOSTIC-only
`msf_month_coverage.sql`, `universe_sensitivity.sql`). `data/` still holds
ONLY `panel.parquet`; the Table I path is untouched (cohort_decile_returns
was refactored to expose `_cohort_decile_returns_from_base` — behavior
bit-identical; Table I metrics re-verified: 192/192, same values).

- **P12 (PART 0, partial-month hypothesis test):** 1,406,859 msf
  (permno, month) rows have ret non-NULL over 1965-02..1990-06 (the task's
  "~5M" estimate was high). Of PA 6/6 sell-decile member stock-months with
  ret_raw non-NULL, 3,250/375,938 (0.865%) are ABSENT from that set; their
  mean ret_raw = −0.0359 vs +0.0063 for present ones. Excluding them from
  the decile means lifts the PA 6/6 sell EW series 0.006227 → 0.006625
  (t 1.28→1.36), buy-sell 0.011530 → 0.011132: **23.7% of the residual sell
  shortfall vs the paper is attributable to partial-month stock-months**
  (direction as hypothesized; ~0.0013/mo residual remains). Buy decile:
  3,840/363,357 (1.057%) absent but mean +0.0157 ≈ present +0.0172 → effect
  on the buy mean negligible, as expected. Universe sensitivity (1980
  month-end PIT counts): exchcd∈(1,2) only = 2,382.8 stocks/mo vs
  + shrcd∈(10,11) = 2,208.8 → the shrcd filter removes 174.0 names/mo
  (7.30% of the exch-only universe: ADR/fund/unit shrcds).
- **P13 (PART 0, spec reconciliation):** the PA 6/6 CALENDAR-MONTH series
  (1965-01..1989-12) draws on cohorts formed 1964-07..1989-11 (6 overlapping
  per month), not "formed 1965-01..1989-12" — the recomputation in step 3
  uses the full strategy cohort set so its base reproduces the Table I
  0.006227 exactly (the spec's cohort window was used verbatim for the
  step-2 scan). 2,321 Jan-1965 member stock-months fall OUTSIDE the spec's
  msf coverage window (1965-02..1990-06): unevaluable, kept in both means.
- **P14 (Table VII):** of the 300 cohorts formed 1965-01..1989-12, the
  1989-12 cohort's holding months (1990-01..) all fall after the panel end,
  so it contributes to NO event month (A10 window f+h ≤ 1989-12): n_1=299,
  n_12=288, n_36=264. At h=1 the NW cumulative t (4.11, L=5) differs from
  the iid monthly t (3.60) by +14% — fully explained by the cross-cohort
  series' lag-1..3 autocorrelations (−0.065, −0.074, −0.074), which make the
  Bartlett kernel estimate var_nw/var_iid = 0.77 (at h=12 the ratio is 1.00).
  C_h is the arithmetic sum of event-month means per spec (C_12=0.1007); the
  mean of per-cohort cumulative sums (0.0933 at h=12, 0.0395 at h=36) differs
  because later event months average over fewer, earlier cohorts — both are
  reported in table_5.md. STOP-probe judgment: the probe gates on the
  HEADLINE anchor C_12 (0.0951, t 3.67 — the §VI result): ours +5.9% → pass.
  The endpoint C_36 is +71.7% (0.0697 vs 0.0406): flagged as an ANOMALY in
  table_5.md rather than stopped — the construction is hand-verified to
  <1e-12 (formation 1979-12, h=1/2/12), the path shape matches (hump 1-12,
  negative 13-24, flat 25-36), and the gap widens monotonically in the same
  direction as the documented Table I sell-side residual (ours decays
  −0.0024/mo over h=13..24 vs paper −0.0033; month 1 ours +0.0120 vs paper
  −0.0025 — the elevated short-horizon spread again).
- **P15 (Table II):** betas all within ±3.7% of the paper (P1 1.39 vs 1.36,
  P10 1.32 vs 1.28, P10−P1 −0.069 vs −0.08); all 21 cells within ±30%.
  Average mcaps run systematically LOW (−8.6%..−28.5%; P1 172 vs 208, P10
  367 vs 495) with the paper's U-shape preserved (peak P7 693 vs 738). The
  uniform downward shift is consistent with a vintage/scope difference in
  |prc|×shrout (e.g., the paper's 1990 file's shrout convention or a
  CRSP-universe scope difference — our me_millions units were verified
  against dsi.totval at the panel stage, P9). Reported, not tuned.
- **P16 (Table IV):** the All group zero-cost series is BIT-IDENTICAL to
  the Table I PA 6/6 buy_sell series (max|diff|=0.0, asserted). Size
  terciles ranked per formation month on stocks with cumret_6_raw AND
  me_millions non-NULL (324 formation months; floor-rank/permno-tie
  convention as the deciles), deciles formed WITHIN each tercile, holding
  returns from the full panel. F_a All 8.12 (p 0.000) vs paper 7.90; F_b
  2.30 (p 0.013) vs 2.04; January All −0.0574 (t −3.69) vs −0.0686 (−3.52);
  Apr 0.0307 vs 0.0333; Feb–Dec 0.0178 vs 0.0166. 47/112 within ±10%,
  91/112 within ±30%; the worst cells are small-magnitude summer months
  (Aug All 0.0054 vs 0.0027) and the S1 Dec t-stat.

## Assumption 12: Residual sell-side shortfall classified as CRSP vintage drift

**Decision:** Keep the raw daily-compound primary series unchanged;
document the remaining sell-side shortfall (≈0.0013%/mo at 6/6 after the
A3 revision) as a data-vintage effect, with Tier-2 (pattern-level)
acceptance for short-K sell cells.
**Rationale:** The fix attempt was made and quantified (inner iteration
4): excluding stock-months absent from CRSP's own monthly file (the
paper-era availability proxy) moves the 6/6 sell mean 0.006227 → 0.006625
— closing only 23.7% of the gap to the paper's 0.0079. Adopting it would
add an unsupported hybrid treatment for a quarter of the gap. The
remaining deviation has the signature of vintage drift: (i) the buy side
matches the paper at <2% across all 32 cells — the sorting/overlap/
rebalancing machinery is correct; (ii) the shortfall is concentrated in
the loser decile and decays monotonically in K, where the 1990 and 2026
CRSP vintages differ most (small distressed stocks' daily returns were
revised across three decades of CRSP updates); (iii) the direction is
consistent with Shumway (1997), whose delisting-bias correction moves
loser returns the same way our A3 revision did. Partial-month exclusion
diagnostic numbers: 3,250/375,938 sell-member stock-months absent from
msf, mean ret −0.0359 vs +0.0063 for present months.
**Impact:** short-K sell cells in Table I (Tier 2), T5 months-13..36
cumulative decay (C_36 +71.7%; C_12 headline +5.9% Tier 1), T4 January
(+16% on the mean, t-stat within 5%). All documented in REPORT.md with
the evidence chain.

---

## Inner iteration 5 — Table III (T3) implementation notes P17–P20 (rep-worker, 2026-07-22)

Table III: 6/6 strategy within size (S1–S3) and Scholes-Williams beta
(β1–β3) subsamples, Panels A (raw returns) + B (market-model alphas), 322
metrics, all in `src/main.py::compute_table3()`; new SQL:
`src/sql/sw_beta_yearly.sql` (SW betas) and `src/sql/rf_monthly.sql`
(risk-free rate). The beta table is computed fresh each run (~5 s) and
held IN MEMORY only — `data/` still holds ONLY `panel.parquet`.

- **P17 (A8, SW beta minimum-days choice):** the paper is silent on a
  minimum number of daily observations for the yearly beta slopes.
  `sw_beta_yearly.sql` requires n ≥ 50 valid index-paired trading days per
  (permno, year) for EACH of the three slopes (contemporaneous/lag/lead),
  else beta_sw = NULL — 50 days is permissive enough to keep most
  NYSE/AMEX stocks while excluding thin traders. Impact: 1,192 of 60,225
  (permno, year) rows are NULL (1.98%); coverage 98.02%. Median SW beta by
  year runs 0.717 (1988) .. 1.612 (1969). Slopes verified against direct
  numpy polyfit for permno 10006 / year 1969: beta_sw identical to 4e-16
  (n0=nl=nd=250; β0=0.989, β_lag=0.583, β_lead=0.217). Lead/lag days are
  taken from the index's own trading-day sequence (lagInFrame/leadInFrame
  over ordered dsi dates 1963-12-01..1990-02-28 joined onto stock days),
  so year-boundary stock days use the adjacent index day in the
  neighboring calendar year, per A8.
- **P18 (A9, zero-cost Panel B alpha — spec-reading resolution):** the
  Panel B P10−P1 alpha regresses the zero-cost return WITHOUT subtracting
  rf: a zero-investment portfolio earns and pays no risk-free rate, so its
  alpha equals α(P10) − α(P1), which is mathematically the intercept of
  the zero-cost return on (1, r_m − rf). The paper's printed values satisfy
  P10−P1 = P10 − P1 EXACTLY in all 7 groups (e.g. All: 0.0070 − (−0.0030)
  = 0.0100; S1: 0.0077 − (−0.0029) = 0.0106; β3: 0.0048 − (−0.0062) =
  0.0110 ≈ 0.0111), identifying the intended quantity. The literal
  r_p − rf reading (subtracting rf from the zero-cost series) gives
  P10-1_all_pB = 0.0061 (−39% vs the 0.0100 anchor); the implemented
  reading gives 0.0118 (+17.7%, the residual being the documented Table I
  spread deviation). The ten DECILE rows use (r_p − rf) as specified.
- **P19 (A8, beta-group month counts):** SW betas are computed for years
  1964..1989 and formations in year Y use beta_year Y−1, so the first
  beta-eligible formation is 1965-01 (1964-07..1964-12 formations would
  need 1963 betas — not computed; extending the beta window to 1963 would
  require index data from 1962-12, beyond the A8 spec). Consequence: the
  β1/β2/β3 reporting series run 1965-02..1989-12 (n = 299; 1965-01 has
  zero beta-eligible cohorts; months 1965-02..1965-06 average 1..5
  overlapping cohorts each; 1965-07..1989-12 the full 6). All/S groups:
  300 months. Means and t-stats are over the n months available per group;
  the Panel A/B F-stats use the months with all ten deciles present (same
  n). All 299 β-group months have all ten deciles non-NULL (asserted).
- **P20 (anomalies flagged, not tuned):**
  1. Footnote-11 cross-check VALIDATES the SW tercile construction: EW
     monthly stock return within prior-year beta terciles, time-series
     mean 1965-01..1989-12 = 1.53% / 1.42% / 1.08% (low/medium/high) vs
     paper 1.48% / 1.39% / 1.16% (dev +3.2% / +2.4% / −6.6%; 300/300
     months, mean 2,133 beta-eligible stocks/month).
  2. Panel A F-stats (spec construction: stacked 10×n monthly decile
     returns on intercept + 9 dummies) run FAR below the paper's (All
     0.73 vs 2.83; range ours 0.44..0.98 vs paper 1.69..4.51) while Panel
     B F-stats are close (All 4.90 vs 5.29, −7.5%; s2 4.96 vs 8.37,
     −41%). Alternative constructions were evaluated on our data and
     match the paper no better: per-cohort holding-period ANOVA (All 3.62;
     range 2.18..4.15) and multivariate time-series Wald with the full
     decile covariance (All 4.12; range 1.88..4.67). The paper's exact
     Panel A F-test construction is unidentified; the spec's was
     implemented verbatim and the deviations reported (paper p-values
     print as 0.00, ours 0.45..0.91 — a Tier-2 pattern-level deviation on
     a secondary statistic).
  3. Subsample P10−P1 (Panel A) deviations (+5.9%..+36.2%) carry the same
     signature as the documented Table I spread deviation (our zero-cost
     means run above the paper's, t-stats higher because our monthly
     spread std 0.048 < paper-implied 0.054): the worst is β2 +36.2%.
     Construction validated: beta1 group at formation 1979-12 — tercile
     split 721/720/720 (beta cutoff [−0.92, 1.05] for β1), within-β1
     decile 1/10 next-month EW returns hand-computed from the panel match
     the pipeline to < 1e-12. The All column is BIT-IDENTICAL to the
     Table I PA 6/6 decile series (max|diff| = 0.0 across all ten
     deciles, asserted; STOP-probe threshold 1e-12).
  4. Near-zero Panel B alphas: two cells print as 0.0000 in the paper
     (P2_s3_pB, P4_b3_pB — undefined percentage tolerance; ours
     +0.000244 / −0.000143) and their t-stats show large percentage
     deviations (small-denominator noise: paper ±0.01..0.03 vs ours
     −0.06..+0.21 on ~0.000-magnitude alphas).

---

## Outer iteration 2 — Table VIII back-test panel extension: implementation notes P21 (rep-worker, 2026-07-22)

Implementation-level notes for the audit-1 M1/M4/m2 work (no changes to any
existing treatment A1–A12/P1–P20; the A3 delisting revision is untouched).
All work lives in `src/main.py` (extended `ensure_panel` snapshot gate,
`group_zero_cost_series` extracted from the Table IV path, new
`compute_table8_backtest` / `compute_table_v_winrates` /
`compute_table_vi_subperiods` / `compute_primary_diagnostics`) and one new
SQL file (`src/sql/ff5_monthly.sql`). `data/` still holds ONLY
`panel.parquet` (the rebuilt extended panel).

- **P21 (M1, pre-1962 universe — VERIFIED SOUND, no fallback needed):** the
  daily window was extended 1962-07-01 → **1926-07-01** (DAILY_START;
  DAILY_END 1989-12-31 unchanged) so 6-month formations start at 1927-01
  (cumret_6 over 1926-07..1926-12 — first cumret_3 at 1926-10, first
  cumret_12 at 1927-07, as expected). Pre-flight checks of the dsenames PIT
  windows pre-1962 (the task's conditional-fallback trigger) found them
  SOUND, so the A1 primary universe is kept for the whole period:
  1. **Match rate:** 96.5–98.1% of dsf stocks with a valid daily return
     match a shrcd∈(10,11)/exchcd∈(1,2) dsenames window in EVERY year
     1926–1961 — the same rate as 1962–1964 (95.9–96.1%). The ~2–3% gap is
     non-common shrcds, exactly as post-1962.
  2. **Counts by decade (rebuilt panel, stocks/month with ret non-NULL):**
     1926–35 mean 656 (min 528 in 1926, the first half-year), 1936–45 mean
     776, 1946–55 mean 978, 1956–65 mean 1,400 (step at 1962-07), 1966–75
     mean 2,307, 1976–85 mean 2,223, 1986–89 mean 2,009. Smooth monotone
     growth — no zeros, no wild jumps pre-1940; consistent with historical
     NYSE+AMEX common-stock listings.
  3. **The 1962-07 step is CRSP's daily-file start, documented and clean:**
     the pre-daily-era windows (namedt ≤ 1962-06) have a namedt
     distribution of 496 windows starting 1925 (CRSP's beginning) +
     20–130/year new listings; exactly **1,121** of them end at 1962-07,
     and **1,128** permnos carry BOTH an old (namedt ≤ 1962-06) and a new
     (namedt ≥ 1962-07) shrcd/exchcd window — the continuity across the
     split is total (counts go 1,121/mo at 1962-06-30 → 1,969 at
     1962-12-31; the 1965–1989 counts are unchanged from the pre-extension
     panel: 2,075.5 in 1965, 2,449.4 in 1975 — P5).
  4. **Decision:** keep the dsenames PIT universe (A1) for 1926-07..1989-12.
     The dsfhdr header-level shrcd/exchcd fallback for pre-1962 was NOT
     invoked (task condition not met — counts plausible). Documented here
     per the task's P21 requirement.
- **P21b (M1, bit-identity of the 1962-07..1989-12 region):** STUCK Rule 2
  snapshot gate extended for this rebuild: **201** random stock-months
  (67/year × 1965/1975/1985, seed=7) captured BEFORE the rebuild; AFTER,
  ALL **13** pre-existing numeric columns (ret, ret_raw, ret_skip5,
  ret_skip5_raw, cumret_3/6/9/12, cumret_3/6/9/12_raw, me_millions) are
  bit-identical on all 201 rows (**max|diff| = 0.000e+00** on every
  column). Panel 728,207 → 1,097,807 rows × 15 cols (113.0 MB). The ONLY
  cells that can differ from the old panel are warm-up cumrets at
  1962-07..1963-06 (the ROWS-based window frame was truncated at the old
  grid start; it is complete now) — no table uses months before 1964-07,
  and the Table I/VII series were verified unchanged end-to-end (PA 6/6
  buy-sell 0.011530, sell 0.006227, buy 0.017757 — identical to the
  audit-1-verified values; cohort counts K in all 300 months; T5 C_12
  0.1007, +5.9% — same as audit 1). `ensure_panel` now also cache-busts on
  earliest-month != DAILY_START (idempotent re-runs load the cache).
- **P22 (M1, Table VIII n-cohort windows):** cohorts contribute to event
  month h while f+h ≤ the panel's END month (1940-12 for Panel A, 1964-12
  for Panel B — same f+h ≤ 1989-12 convention as A10). n-cohorts: Panel A
  168 formations (1927-01..1940-12) → n_1 = 167, n_12 = 156, n_36 = 132;
  Panel B 288 formations (1941-01..1964-12) → n_1 = 287, n_12 = 276,
  n_36 = 252 (all as the task expected; n_h = n_form − h for contiguous
  formations). Completeness asserted inside the valid windows (0 missing
  zero-cost cohort cells on either panel).
- **P23 (M1, Table VIII results — honest deviations, no tuning):** Panel A
  (SIGN/PATTERN target, per the task's expectation management): month 1
  −0.0138 vs paper −0.0495 (+72% — correct negative SIGN, ~¼ the
  magnitude; 1927–1940 is the most vintage-sensitive part of CRSP), month
  2 −0.0113 vs −0.0143 (+21%), C_12 −0.0512 vs −0.1012 (+49%; t −1.37 vs
  −1.27 = −7.6%), C_24 −0.2375 vs −0.3241 (−27%), C_36 −0.3029 vs −0.4081
  (+26% — 'cumulative strongly negative' pattern holds); cumulative t at
  h=36 ours −4.66 vs paper −2.01 (our cross-cohort cumulative series is
  less autocorrelated — NW SE smaller). Tally: 11/144 within ±10%, 67/144
  within ±30%. Panel B (MAGNITUDE target): C_12 +0.0583 vs +0.0583
  (**+0.1%**, t 3.68 vs 3.40), months 2–8 mean +0.0074 (paper:
  'significantly positive 2..8' holds), C_24 +0.0172 vs +0.0050 and C_36
  +0.0125 vs −0.0030 (dissipation pattern present — 71% of C_12 dissipated
  by month 24 — but weaker than the paper's ~100%; all post-month-12 cells
  are statistically nil on both sides: paper |t| ≤ 0.60, ours |t| ≤ 0.37).
  Panel B month 1 +0.0088 vs −0.0035: the SAME short-horizon anomaly
  documented for Table VII (event_t1 ours +0.0120 vs paper −0.0025) — the
  vintage residual appears at the shortest event months; both values are
  small (paper t −1.04). Tally: 15/144 within ±10%, 43/144 within ±30%.
  Overall T8: 26/288 within ±10%, 110/288 within ±30%; exact contract
  name-set equality (288). Single-cohort hand checks match the pipeline to
  <1e-12 on BOTH panels (formations 1935-06 and 1955-06, h=1/2/12).
- **P24 (M4, Tables V/VI — zero new data):** both tables draw on
  `group_zero_cost_series()` — extracted from the Table IV path (same code,
  same series objects): All + S1/S2/S3 300-month zero-cost series, with the
  All group asserted BIT-IDENTICAL to the Table I PA 6/6 buy_sell series in
  all three consumers (max|diff| = 0.0, printed as `[t4]`/`[t6]`/`[t7]`).
  Table V (T6, 56 metrics): positive-month proportions over 25
  same-calendar-month obs / 275 Feb–Dec / 300 all-months; anchors exact or
  near-exact — prop_jan_all 0.24 (0.0%), prop_apr_all 0.96 (0.0%),
  prop_feb_dec_all 0.7127 (+0.4%), prop_all_months_all 0.6733 (+0.5%, the
  paper's L907 headline 0.67), prop_jan_s3 0.48 vs 0.44 (+9.1%); tally
  48/56 ±10%, 55/56 ±30% (the one >30% cell is prop_jan_s1 0.24 vs 0.16 —
  6/25 vs 4/25 Januaries). Table VI (T7, 120 metrics): 5-year subperiod
  slices × {All months (60 obs), Jan. (5), Feb.–Dec. (55)}; anchors:
  sp_all_all_6569 0.0108 vs 0.0123 (−12.1%, t 1.85 vs 1.94); sp_all_jan_7074
  −0.1005 vs −0.1070 (+6.1%, t −2.538 vs −2.540 = **+0.1%**); sp_s1_jan_8589
  −0.0943 vs −0.1064 (+11.4%); sp_s3_feb_dec_8589 0.0063 vs 0.0052
  (+20.2%); sp_s2_all_6569 0.0160 vs 0.0177 (−9.5%); tally 49/120 ±10%,
  92/120 ±30%.
- **P25 (M4/P23, the 1975–79 subperiod cell — anomaly flag, not tuned):**
  sp_all_all_7579 = +0.0003 vs paper −0.0044 — the paper's ONLY negative
  full-period cell; ours is ≈ 0 (+0.03%/mo, t +0.05 vs paper −0.51 — nil on
  both sides; |diff| = 0.0047/mo). Direction consistent with the documented
  Table I sell-side residual (A12): our buy-sell spreads run slightly ABOVE
  the paper's (ours 0.01153 vs 0.0095, +21.4%), so a −0.0044 paper subperiod
  mean lands at ≈ 0 in our vintage. Flagged in t7_table_vi.md, not tuned.
- **P26 (m2, §3 diagnostics persisted — all match the auditor's values):**
  11 diag_* keys on the PA 6/6 RAW zero-cost series (same t1_pa66_buy_sell
  series as Tables I/IV/V/VI): mean 0.011530; iid t 4.1665; Sharpe_ann
  0.8333 (REPORT 0.83); total_return_pct 2077.96 (2078.0%); max_drawdown_pct
  −41.91 (−41.9%); arithmetic_ann_pct 13.84; geometric_ann_pct 13.1155
  (13.12%); FF5 alpha = intercept of the RAW zero-cost return on
  mkt_rf/smb/hml/rmw/cma from ff.five_factor_monthly (zero-cost convention
  per P18: rf NOT subtracted) = 16.8417%/yr (16.84%), t 4.8648 (4.86),
  R² 0.1348 (0.13); rf-subtracted documentation variant (zc − rf on the 5
  factors) = 10.0461%/yr (10.05%), t 2.89. All within rounding of the
  audit-1 independently recomputed values (asserted at run time). Written
  to results/primary_diagnostics.md WITH the spec stated (the m2 ask);
  merged into computed_values.json (11 extra keys — allowed; contract
  name-set equality is asserted only for T1–T8).

---

## Outer iteration 2 — issue log entries (rep-worker, 2026-07-22)

(each entry: Problem / Diagnosis / Next fix / Before metric / After metric /
Status — per the audit-1 iteration discipline)

### [M1] Table VIII back-test 1927–1964 (288 metrics)

**Problem:** corollary back-test (§VII, Table VIII) absent from artifacts
(audit 1 M1, actionable; data verified feasible — dsf/dsi from 1925-12-31).

**Diagnosis:** not a mismatch diagnosis — a missing table. One conditional
decision was investigated: the task's fallback trigger (dsenames PIT windows
unusable pre-1962 → dsfhdr header-level shrcd/exchcd). Pre-flight queries
found the PIT windows SOUND (P21: 96.5–98.1% yearly match rate 1926–1961,
same as post-1962; smooth counts 528/mo in 1926 → ~770 by 1940; the 1962-07
step is CRSP's daily-file start with 1,128 permnos carrying both window
eras) — fallback NOT invoked, A1 kept for the whole period.

**Next fix:** extend the daily window to 1926-07-01 (762-month grid);
rebuild the panel behind the extended STUCK-Rule-2 snapshot gate (201 rows ×
13 cols, max|diff| = 0 on the 1965/1975/1985 span); reuse the Table VII
event-time machinery (J=6, H=36, variant A, RAW columns, A10 conventions:
event-month mean over cohorts with f+h ≤ window end; arithmetic cumulative;
iid monthly t; NW cumulative t with L = int(4·(T/100)^(2/9))) for cohorts
formed 1927-01..1940-12 (Panel A, window end 1940-12) and 1941-01..1964-12
(Panel B, window end 1964-12).

**Before metric:** 0/288 Table VIII metrics in artifacts; panel daily window
1962-07-01..1989-12 (728,207 rows).

**After metric:** 288/288 computed, exact T8 contract name-set equality,
merged (total keys 791 → 1,079); panel 1,097,807 rows; bit-identity
verified (P21b). Cohort counts exactly as specified (A: n_1=167/n_12=156/
n_36=132; B: 287/276/252). Anchors — Panel A (sign/pattern target): month 1
−0.0138 vs −0.0495 (+72%; negative sign holds, magnitude vintage-sensitive
as the task warned), month 2 −0.0113 vs −0.0143 (+21%), C_12 −0.0512 vs
−0.1012 (+49%; t −1.37 vs −1.27), C_36 −0.3029 vs −0.4081 (+26%, 'strongly
negative' holds); Panel B (magnitude target): C_12 +0.0583 vs +0.0583
(+0.1%; t 3.68 vs 3.40), months 2–8 mean +0.0074 (positive as claimed),
C_24 +0.0172 vs +0.0050 / C_36 +0.0125 vs −0.0030 (dissipation present,
weaker than the paper's; all statistically nil), month 1 +0.0088 vs −0.0035
(same short-horizon anomaly as Table VII). Tallies: overall 26/288 ±10%,
110/288 ±30%; A 11/67; B 15/43. Hand checks < 1e-12 on both panels.
Results in results/t8_table_viii.md with the expectation-management note.

**Status:** complete; documented deviations (no tuning — Panel A magnitude
is the known vintage-sensitive region; Panel B's post-month-12 cells and
month-1 sign flip are statistically nil cells carrying the documented
Table I residual).

### [M4] Tables V + VI win rates and subperiods (176 metrics, zero new data)

**Problem:** corollary stability tables absent (audit 1 M4, actionable;
'requires zero new data or machinery').

**Diagnosis:** not a mismatch diagnosis — missing tables that fall out of
the already-computed, bit-identical calendar-month series (audit 1 §4.3:
'understates how cheap they are').

**Next fix:** extract `group_zero_cost_series()` from the Table IV path
(identical code; All group asserted bit-identical to the Table I PA 6/6
buy_sell series in every consumer, max|diff| = 0.0); Table V = positive-month
proportions per calendar month (25 obs), Feb.–Dec. (275), All months (300)
× 4 groups; Table VI = 5-year subperiod slices {6569..8589} × {All months
(60), Jan. (5), Feb.–Dec. (55)} × 4 groups with iid t (A5).

**Before metric:** 0/176 Table V/VI metrics in artifacts.

**After metric:** T6 56/56 and T7 120/120 computed, exact contract name-set
equality, merged (1,079 → 1,255 keys). T6: ±10% 48/56, ±30% 55/56; anchors
prop_jan_all 0.24 (+0.0%), prop_apr_all 0.96 (+0.0%), prop_feb_dec_all
0.7127 (+0.4%), prop_all_months_all 0.6733 (+0.5% — the L907 headline),
prop_jan_s3 0.48 vs 0.44 (+9.1%). T7: ±10% 49/120, ±30% 92/120; anchors
sp_all_all_6569 0.0108 vs 0.0123 (−12.1%, t 1.85 vs 1.94), sp_all_jan_7074
−0.1005 vs −0.1070 (+6.1%, t −2.538 vs −2.540 = +0.1%), sp_s1_jan_8589
−0.0943 vs −0.1064 (+11.4%), sp_s3_feb_dec_8589 +0.0063 vs +0.0052
(+20.2%), sp_s2_all_6569 0.0160 vs 0.0177 (−9.5%). Anomaly flagged (P25):
sp_all_all_7579 +0.0003 vs −0.0044 — the paper's only negative full-period
cell; ours ≈ 0 (nil t on both sides), direction = the documented A12
sell-side residual. Results in results/t6_table_v.md + t7_table_vi.md.

**Status:** complete.

### [m2] persist the REPORT §3 diagnostics

**Problem:** the §3 diagnostics were verified exact by the auditor but not
persisted in computed_values.json or any table md (audit 1 m2).

**Diagnosis:** persistence gap only (values already correct).

**Next fix:** `compute_primary_diagnostics()` — 11 diag_* keys on the PA 6/6
RAW zero-cost series; FF5 spec stated explicitly (intercept of the RAW
zero-cost return on mkt_rf/smb/hml/rmw/cma, rf NOT subtracted per P18; the
rf-subtracted variant computed and printed for documentation), written to
results/primary_diagnostics.md with run-time assertions vs the audit-1
values.

**Before metric:** 0 diag_* keys in computed_values.json (791 keys total).

**After metric:** 11 diag_* keys merged (1,255 → 1,266 total); all match
REPORT §3 / auditor values within rounding (asserted): Sharpe 0.8333
(0.83), total return 2077.96% (2078.0%), MDD −41.91% (−41.9%), arithmetic
ann. 13.84%, geometric ann. 13.1155% (13.12%), FF5 α 16.8417%/yr (16.84%)
t 4.8648 (4.86) R² 0.1348 (0.13), rf-sub α 10.0461% (10.05%, t 2.89).

**Status:** complete.

---

## Outer iteration 2 (spawn 2) — audit-1 M3 (§III decomposition) + M2 (Table IX): implementation notes P27–P28 (rep-worker, 2026-07-22)

Implementation-level notes for the audit-1 M3/M2 work (no changes to any
existing treatment A1–A12/P1–P26; the panel is READ-ONLY this spawn — not
touched). New code in `src/main.py` (`compute_decomposition`,
`compute_table9_earnings` + helpers) and two new SQL files
(`src/sql/index_monthly_1964.sql`, `src/sql/earnings_announcements.sql`).
`data/` still holds ONLY `panel.parquet`.

- **P27 (M2, Table IX data path — five paper-silent conventions):**
  1. **CRSP↔Compustat link.** The CCM link table is
     `crsp_202601.ccmxpf_linktable` (the catalog has NO ccmxpf_linktable in
     `comp_202601` — only in the crsp_* databases; 92,711 rows). permno =
     `lpermno` (Nullable(Float64) → Int32); `usedflag` is Nullable(Float64)
     with 1.0 = used (−1.0 = not); `linkdt`/`linkenddt` are 'YYYY-MM-DD'
     strings (empty-string linkenddt → '2100-01-01' so open links stay
     valid). PIT: linkdt ≤ rdq ≤ linkenddt (string compare = chronological).
     Filter usedflag = 1, linktype IN ('LU','LC','LS','LX'), lpermno
     non-NULL. NOTE: every LX row has usedflag = −1, so the linktype filter
     reduces to LU/LC/LS in practice (all usedflag = 1). **Dedupe to one
     gvkey per (permno, rdq):** prefer linkprim = 'P', then earliest linkdt
     (`row_number() OVER (PARTITION BY permno, rdq ORDER BY linkprim='P'
     DESC, linkdt ASC)`, rk = 1). Verified counts: 192,653 (permno, rdq,
     gvkey) rows before dedupe → 192,442 distinct (permno, rdq) after (211
     multi-link collisions resolved).
  2. **Announcements (indfmt choice).** `comp_202601.fundq`, deduped to ONE
     rdq per (gvkey, fyearq, fqtr) = min(rdq) (min aliased to `min_rdq` —
     a same-name alias shadows the column in ClickHouse), rdq window
     1980-02-01 .. 1992-12-31 (36 months past the last 1989-12 formation).
     On this vintage **100% of rdq rows in-window are indfmt = 'INDL'**
     (199,456 all = 199,456 INDL) → the INDL filter matches the paper's
     "quarterly industrial database" and is a NO-OP here; used as primary
     (the all-formats choice is identical).
  3. **Day-0 convention (paper silent).** Day 0 = the FIRST dsf trading day
     ON OR AFTER rdq, capped within 5 calendar days (else the announcement
     drops — 33 of 192,442 have no day0); days −1, −2 = the two trading days
     immediately preceding day0 (no backward calendar-day cap — a halt just
     pushes them back). 3-day return = prod(1 + dsf.ret) over days −2..0,
     `ret` the plain daily return (ret_raw; delisting adjustment is not
     meaningful over 3 days); drop if any of the 3 days has a missing/
     sentinel return (816 of 192,409 day0-matched announcements → NULL
     ret3). dsf is one row per (permno, date) (verified: 21,204,457 rows =
     21,204,457 distinct keys in 1980-1993, no de-dupe needed). Hand-checked
     one case (permno 47715, rdq 1985-01-24): day0=1985-01-24 (ret 0.01835),
     day−1=1985-01-23, day−2=1985-01-22 → ret3 = 0.01835 = pipeline value.
  4. **Coverage / vintage.** Paper: 429.2 announcements/month. Ours:
     **12,434.8** per post-formation month (winner+loser summed over the 120
     cohorts, averaged over m=1..36); 103.6 per (cohort × post-month) cell;
     n_w ≈ 6,000–7,200 and n_l similar per group per month. The 2026
     Compustat vintage carries far more matched quarterly announcements for
     1980s NYSE/AMEX stocks than the paper's 1990 quarterly file. Each
     (permno, rdq) is counted ONCE per post-month m: since m = rdq_ord −
     f_ord, a fixed (m, rdq_ord) fixes a UNIQUE cohort f, so there is no
     within-month double-count (the same announcement contributes to
     DIFFERENT m's via different cohorts — the paper's own overlapping-cohort
     design). Consequence: our Welch t-stats scale with the higher √n and
     run above the paper's (documented, not tuned — the task's Welch-over-
     announcement-level formula is applied verbatim).
  5. **Result:** 72/72 T9 metrics, EXACT contract name-set equality; the
     sign PATTERN replicates (months 1–7 mean +0.0063, 6/6 positive and
     6/6 significant; months 8–20 negative in 12/13; months 11–18 mean
     −0.0047 ≈ the paper's −0.7%; months 21–36 −0.0030 near zero). Magnitude
     cells carry the documented Table I/vintage residual; the near-zero
     months 21–36 and the inflated t-stats drive the raw ±-tolerance count
     (12/72 ±10%, 23/72 ±30%) — pattern-level acceptance per the task's
     abstract-level framing.

- **P28 (M3, §III decomposition — five paper-silent conventions):**
  1. **WRSS period choice.** 50 non-overlapping semiannual periods = the
     returns over 1965-H1 .. 1989-H2; formation ORDINALS 1964-12, 1965-06,
     …, 1989-06 (NOT the task's "1965-01 … 1989-07"). Rationale: the forward
     (holding) window is [f+1, f+6] so it (a) coincides with the 6/6 holding
     window — required for the 0.95 correlation anchor — and (b) keeps the
     last period 1989-07..1989-12 inside the panel (the task's
     "1965-01 … 1989-07" + forward [f+1, f+6] would need 1990-01 for the last
     formation, which the panel lacks). Both conventions enumerate the SAME
     50 return half-years; the past window is [f−6, f−1] (the EW-index past
     return from dsi.ewretd compounded).
  2. **WRSS profit normalization.** The task's LITERAL formula
     "cross-sectional mean of weight × forward return" = the raw
     cross-sectional covariance = **+0.0021** (t 0.95) — a COVARIANCE on the
     0.002 scale, ~20× below the paper's "4.5% per dollar long" portfolio-
     return anchor. Because the paper's wording ("4.5% per dollar long
     semiannually") and the 0.95 correlation anchor (against the 6/6
     PORTFOLIO returns) require a portfolio-return-scale quantity, the
     PRIMARY dec_wrss_mean = the dollar-neutral weighted long-short return
     (weighted winner return − weighted loser return, w_i = past_i − EW-index
     past) = **+0.0342** (t 1.82), which correlates **+0.971** with the 6/6
     single-cohort semiannual zero-cost returns y_f (matches the 0.95 anchor;
     the calendar-time semiannual-compound alternative correlates +0.860).
     Raw covariance reported in the md for transparency. Mean/t run below
     the paper's (per-$-long profit and its dispersion are vintage-sensitive;
     the correlation anchor IS replicated).
  3. **EW-index serial covariance (A2).** The paper's decomposition (eq. 4,
     L437–444) is over NON-OVERLAPPING 6-month periods, so the anchor-
     comparable value is the semiannual serial covariance Cov(R_p, R_{p−1})
     over the 50 half-years (49 pairs) = **−0.0061** (paper −0.0028; same
     sign, ~2× magnitude). The overlapping-monthly Cov(R_t, R_{t−1}) (299
     pairs) = **+0.0299** is MECHANICALLY positive (consecutive overlapping
     6-month windows share 5 of 6 months) and is NOT the quantity the paper
     reports as −0.0028; printed for transparency.
  4. **Residual serial covariance (A3).** Market model per stock on the
     overlapping 6-month returns (1965-01..1989-12, 300 obs, ≥ 60
     non-missing) vs the VW market (primary, L526). The period-level serial
     covariance Cov(e_it, e_{it−1}) of consecutive NON-overlapping periods =
     **lag 6** in the monthly-indexed residual series (lag 1 is mechanically
     inflated to ~0.07 by the 5-month overlap). Cross-sectional AVERAGE over
     3,196 stocks = **+0.00120** — matches the paper's +0.0012 to 4 dp.
     EW-market alternative = −0.00030 (3,196 stocks).
  5. **Squared-market regression (A4).** x_f uses the VW-index 6-month
     return over the LOOKBACK window [f−6, f−1] (the paper's L526 "months
     t−6 … t−1", identical to the panel's cumret_6_raw ranking window),
     demeaned by the FULL-sample mean of the 294-formation series; the task's
     [f−5, f] variant gives θ −1.41 (vs −1.86 for [f−6, f−1], the closer of
     the two to the paper's −2.29). y_f = the cohort's 6-month zero-cost
     CUMULATIVE return (compounded decile10 − decile1, h=1..6). OLS y on
     (1, x²) with Newey-West HAC t (Bartlett; full L=5, halves L=4).
     **θ = −1.86** (t −3.18) full; h1 −1.69 (t −1.86); h2 −2.04 (t −5.60).
     Sign matches everywhere; our |t| run ABOVE the paper's because our y_f
     series is less autocorrelated — the SAME NW-SE effect documented for
     Table VII (P14). Half-sample ordering differs from the paper's
     (our |h2| > |h1| vs paper |h1| > |h2|) — flagged, not tuned.

---

## Outer iteration 2 (spawn 2) — issue log entries (rep-worker, 2026-07-22)

(each entry: Problem / Diagnosis / Next fix / Before metric / After metric /
Status — per the audit-1 iteration discipline)

### [M3] §III profit-decomposition statistics (11 dec_* keys)

**Problem:** the four in-text statistics underpinning the paper's causal
claim (WRSS profit 4.5%/half-year t 2.99; EW-index 6-month serial covariance
−0.0028; avg market-model-residual serial covariance +0.0012; squared-
lagged-market θ −2.29, halves −2.55/−1.83) were absent from the artifacts
(audit-1 M3, actionable).

**Diagnosis:** not a mismatch — a missing block. Five paper-silent
conventions had to be pinned down and each was validated against its anchor
BEFORE integration (P28): (i) the WRSS forward window must coincide with the
6/6 holding window ([f+1, f+6], formations 1964-12..1989-06) to reach the
0.95 correlation and stay in-panel; (ii) the paper's "per dollar long" 0.045
anchor is a portfolio-return scale, not the raw cross-sectional covariance
(the task's literal formula gives +0.0021) — the dollar-neutral weighted
long-short return (+0.0342) is the matching quantity and correlates +0.971;
(iii) the EW serial covariance anchor −0.0028 is the NON-overlapping
semiannual value (overlapping is mechanically +0.0299); (iv) the residual
serial covariance anchor +0.0012 is the lag-6 (consecutive non-overlapping
period) value (lag-1 overlapping is mechanically ~0.07) — reproduced EXACTLY
(+0.00120); (v) the θ-regression lookback window is [f−6, f−1] (the paper's
"months t−6..t−1" = the panel's ranking window), closer to −2.29 than the
task's [f−5, f].

**Next fix:** `compute_decomposition()` + `src/sql/index_monthly_1964.sql`
(EW+VW monthly indexes 1964-01..1989-12); 11 dec_* keys merged (the
transparency alternatives — raw covariance, overlap serial cov, EW-market
residual, [f−5,f] θ — stay in the md/console, NOT in computed_values.json);
`results/table_8_decomposition.md` with all four statistics + a plain-
language verdict on the three causal claims.

**Before metric:** 0 decomposition statistics in artifacts (1,266 keys total;
no dec_* keys; no table_8_decomposition.md).

**After metric:** 11 dec_* keys merged (1,327 → 1,338; 1,349 with diag).
A1 WRSS per-$-long mean +0.0342 (paper 0.045, −24%), t 1.82 (2.99, −39%),
corr +0.971 (0.95, **+2.2%** — anchor replicated); A2 EW serial cov −0.0061
(−0.0028, same sign); A3 avg residual serial cov **+0.00120** (+0.0012,
**−0.0%**, exact); A4 θ −1.86 (−2.29, +19%, sign matches), h1 −1.69 / h2
−2.04 (signs match). Verdicts: factor-timing REJECTED (EW serial cov
negative), idiosyncratic underreaction SUPPORTED (residual serial cov
positive), lead-lag REJECTED (θ negative). Results in
results/table_8_decomposition.md.

**Status:** complete; documented deviations (no tuning — A1 mean/t and A2
magnitude are vintage/dispersion-sensitive; A3 exact; A4 sign matches with
the documented NW-SE |t| inflation, same mechanism as Table VII P14).

### [M2] Table IX earnings-announcement returns (72 metrics, T9)

**Problem:** the §VIII earnings-announcement corollary (Table IX: winners
earn higher 3-day announcement returns months 1–7, losers higher months
8–20, esp. 11–18 ≈ −0.7%) was absent from the artifacts (audit-1 M2,
actionable; data verified feasible — fundq.rdq + ccmxpf_linktable present).

**Diagnosis:** not a mismatch — a missing table requiring a brand-new
COMPUSTAT data path (entirely distinct from the CRSP-only Tables I–VIII).
Five paper-silent conventions pinned down and documented (P27): the link
table is `crsp_202601.ccmxpf_linktable` (permno = lpermno, usedflag is
Float64=1.0) with PIT linkdt ≤ rdq ≤ linkenddt and a linkprim='P'-then-
earliest-linkdt dedupe (192,653 → 192,442 distinct (permno, rdq)); fundq is
100% indfmt='INDL' in-window (the paper's "industrial" filter is a no-op);
day 0 = first dsf trading day on/after rdq within 5 days, days −2/−1 the two
preceding trading days, 3-day prod(1+ret_raw), drop if any day missing
(816/192,409 → NULL).

**Next fix:** `src/sql/earnings_announcements.sql` (fundq dedupe + PIT link +
dedupe + 3-day dsf return, one row per distinct (permno, rdq)) — SQL-first,
runs in ~15 s; `compute_table9_earnings()` does the cohort filter (deciles
1/10 at the 120 monthly formations 1980-01..1989-12, ranked on cumret_6_raw)
+ the (permno, rdq)→(cohort, post-month m) match + the per-m winner/loser
Welch aggregation. 72 ea_t{n}[_t] keys merged with EXACT T9 name-set
equality; `results/table_7_earnings.md`.

**Before metric:** 0/72 Table IX metrics in artifacts (no COMPUSTAT path).

**After metric:** 72/72 computed, exact T9 contract name-set equality, merged
(1,151 → … part of the 1,327 contract + 22 extra = 1,349 total). Coverage
12,434.8 announcements/post-month (paper 429.2 — 2026 Compustat vintage has
far more matched announcements; inflates our Welch t-stats via √n). PATTERN
REPLICATED: months 1–7 mean +0.0063 (6/6 positive, 6/6 significant), months
8–20 negative in 12/13, months 11–18 mean −0.0047 (paper ~−0.7%), months
21–36 −0.0030 (near zero). Anchors: ea_t1 +0.0094 (paper 0.0055), ea_t4
+0.0063 (0.0090), ea_t11 −0.0037 (−0.0039), ea_t16 −0.0053 (−0.0097), ea_t18
−0.0035 (−0.0060), ea_t36 −0.0013 (−0.0059) — signs match, magnitudes carry
the documented vintage residual. Tally 12/72 ±10%, 23/72 ±30% (near-zero
months 21–36 and the √n-inflated t-stats dominate the misses; the pattern is
the deliverable per the task's abstract-level framing). Hand-checked 3-day
return (permno 47715, rdq 1985-01-24) matches dsf to <1e-6.

**Status:** complete; documented deviations (no tuning — coverage/vintage
drives both the magnitude residual and the inflated t-stats; the task's
Welch-over-announcement-level formula applied verbatim).

---

## Assumption 13: Formation/holding timing — no skipped month (outer iteration 2, inner iteration 3)

**Decision:** Formation month f is ranked on `cumret_J_raw` at calendar month
f+1 — i.e., on the J-month compounded return over **[f−(J−1), f]** — and holds
months **f+1 .. f+K**. Month f is the LAST signal month; the holding period
begins at f+1. There is NO gap between the signal window and the holding
window.

**Rationale:** The paper is explicit (content.md L111, L157): portfolios are
"formed immediately after the lagged returns are measured", rank on the return
over [t−6, t−1], and HOLD [t, t+K−1] — Panel A has no skip-week (only Panel B
skips the first trading week). The pre-A13 implementation ranked formation f on
cumret_J_raw(f) = [f−6, f−1] and held f+1..f+K, which left month f in NEITHER
the signal (which ended at f−1) NOR the holding (which started at f+1) — an
implicit one-month skip contradicting the paper. Mapping the paper's formation
time t to our formation month f = t−1 (last signal month), the correct signal
is cumret_J_raw(f+1) = [f−5, f] and the holding is f+1..f+K = the paper's
[t, t+K−1]. Replicator's rule: methodology over numbers — accept whatever
numbers result (the buy side was already <2% off under the skipped variant
because 6-month momentum signals are smooth; the sell side improved markedly
under the correction — see the iteration entry).

**Impact:** decile membership for EVERY table (I–IX) — all of it flows from
`formation_deciles`. Downstream knock-ons, all implemented:
- WRSS past window (A1) → [f−5, f] (aligned with the corrected signal).
- Squared-market regression x (A4) → VW 6-month return over [f−5, f] (= the
  paper's "months t−6..t−1" under t=f+1; the pre-A13 [f−6, f−1] was an
  artifact of the old timing).
- Table IX earnings formations → f = 1979-12 .. 1989-11 (the paper's ranking
  dates t = 1980-01 .. 1989-12 = f+1).
- A2/A3 (EW-index and market-model-residual serial covariances) are statistics
  on consecutive NON-overlapping periods — NOT affected by the decile timing
  (unchanged).
- The run_table1 A3 raw-vs-adjusted STOP probe is RETIRED to a non-blocking
  note: it arbitrated the now-SETTLED raw-PRIMARY decision, and after A13 the
  adjusted series lands slightly closer on the PA 6/6 spread only because its
  delisting drag partially offsets the now-small raw gap (a coincidence, not
  grounds to abandon the settled methodology).

## P29 — A13 timing-correction implementation notes (rep-worker, inner iteration 3, 2026-07-22)

- **Core change (formation_deciles):** the cumret value at panel month m is the
  signal for formation f = m−1 (`f_ord = month_ord(m) − 1`; returned
  `month`/`f_ord` are the FORMATION month). Implemented as an explicit
  month-mapping, NOT a positional `groupby('permno')[sig].shift(-1)`, because a
  positional shift would skip trading gaps for suspended stocks (the month
  mapping is gap-robust). A first attempt that assigned
  `base["month"] = _ord_to_ts(f_ord)` directly produced a label-aligned
  DatetimeIndex on the non-contiguous frame index (corrupt month column, 2121
  rows / 1963 permnos at 1979-12) — fixed by assigning the positional
  `np.asarray(...)` after a `reset_index(drop=True)`.
- **Boundary effects (verified):** the first valid formation moves to 1926-12
  (cumret at 1927-01) and the LAST formation becomes 1989-11 (1989-12 drops —
  its shifted signal is cumret at 1990-01, off the panel end). Reporting months
  1965-01..1989-12 stay COMPLETE: all 32 (panel, J, K) grids have exactly K
  contributing cohorts in all 300 months (every reporting cohort ≥ 1964-07 has
  a valid shifted signal); T5 n_1 stays 299; earnings stays 120 cohorts.
- **Count-assertion updates forced by the boundary shift:** Table II mcap now
  averages 299 formations (1989-12 dropped, was 300); the Table VIII back-test
  base filter gains a lower bound `>= 1927-01` to keep the 456 back-test
  formations (1926-12 is valid under A13 but precedes Panel A and is used by
  neither panel — the per-panel asserts 168/288 are unchanged).
- **Hand-verification (<1e-12):** the paper's Jan-1980 portfolio = formation
  f=1979-12 ranks on cumret_6_raw@1980-01 = compound [1979-07 .. 1979-12]
  (signal vs cumret_6_raw@1980-01: max|diff| = 0.0 over 2,205 ranked stocks),
  and holds from 1980-01; decile 1 / decile 10 next-month (1980-01) EW returns
  hand-computed from the panel match the pipeline to <1e-12.
- **Earnings matching unchanged mechanically:** post-month m of cohort f =
  calendar month f+m; with f = 1979-12..1989-11 the paper's month t = (f+1)+(m−1),
  so the (permno, rdq)→(cohort, m) join and the once-per-post-month counting are
  unaffected; the rdq window (1980-02..1992-12) is unchanged (1992-12 rdqs now
  fall in m=37 of cohort 1989-11 and are unused; 1980-01 rdqs — month 1 of
  cohort 1979-12 — predate the rdq window).

---

## Inner iteration 3 (outer iteration 2) — A13 timing correction: issue log entry (rep-worker, 2026-07-22)

(Problem / Diagnosis / Next fix / Before metric / After metric / Status)

### [A13] Formation/holding timing — remove the implicit 1-month skip

**Problem:** the formation/holding timing had an implicit 1-month skip that
contradicts the paper. `cumret_J_raw(m)` compounds [m−6, m−1] and
`cohort_decile_returns` ranked formation f on cumret(f) and held f+1..f+K, so
month f was in NEITHER the signal (ends f−1) NOR the holding (starts f+1). The
paper (L111, L157) ranks on [t−6, t−1] and holds [t, t+K−1] with no gap
(replicator-diagnosed; verified by code inspection).

**Diagnosis:** mapping the paper's formation time t to our formation month
f = t−1 (last signal month), the correct signal is cumret_J_raw(f+1) = [f−5, f]
and the holding is f+1..f+K = [t, t+K−1]. The single source of the skip was
`formation_deciles` ranking on the contemporaneous (not next-month) cumret.

**Next fix (one minimal change + forced knock-ons):**
1. `formation_deciles` ranks formation f on cumret at month f+1
   (`f_ord = month_ord(m) − 1`; gap-robust month mapping, not a positional
   shift). Holding unchanged (h=1..K). Everything downstream flows from the
   decile membership.
2. Earnings formations → f = 1979-12..1989-11 (paper ranking dates t = f+1).
3. A1 WRSS past window → [f−5, f]; A4 θ x-window → VW over [f−5, f] (= paper's
   t−6..t−1 under t=f+1). A2/A3 unchanged (non-overlapping-period statistics).
4. Count-assert updates forced by the boundary (1989-12 loses its shifted
   signal = cumret at 1990-01, off-panel): Table II mcap 300→299; Table VIII
   base filter gains `>= 1927-01` (keeps 456; 1926-12 valid under A13 but
   precedes Panel A and is unused).
5. Two methodology-obsolete guards retired to non-blocking notes (both were
   bound to the PRE-A13 series): (a) the run_table1 raw-vs-adjusted STOP probe
   (A3 raw-PRIMARY is SETTLED; after A13 the adjusted series lands slightly
   closer on the PA 6/6 spread only because its delisting drag partially
   offsets the now-small raw gap — coincidence, not grounds to switch);
   (b) the compute_primary_diagnostics assert vs REPORT §3 / audit-1 values
   (those were recomputed on the pre-A13 series; the diagnostics are now
   persisted on the A13 series and reported as deviations; REPORT.md untouched
   per rep-worker scope).

**Before metric (pre-A13, skipped-month variant):** PA 6/6 sell 0.006227
(t 1.28; paper 0.0079, **−21.2%**), buy 0.017757 (t 4.36; +2.1%), buy-sell
0.011530 (t 4.17; **+21.4%**); PA 12/3 b-s 0.013748; PB 12/3 b-s 0.013780;
T5 C_12 0.100746 / C_36 0.069722; T8 PA C_36 −0.302927 / PB C_12 0.058344;
T9 months 1–7 mean +0.006278 / months 11–18 mean −0.004704; A1 WRSS mean
0.034179 / corr 0.970970; A4 θ −1.8585 (h1 −1.6880, h2 −2.0388); T1 tally
116/192 ±10%, 162/192 ±30%; T8 tally 26/288 ±10%, 110/288 ±30%.

**After metric (A13 corrected):**
- **PA 6/6 sell 0.008110 (t 1.62; paper 0.0079/1.56 → +2.7%/+3.5%)** — the
  documented A12 sell-side shortfall is RESOLVED (−21.2% → +2.7%). buy 0.016908
  (t 4.22; −2.8%), **buy-sell 0.008797 (t 2.91; paper 0.0095/3.07 → −7.4%/−5.3%)**,
  was +21.4%. PA 12/3 b-s 0.012297 (t 3.58); PB 12/3 b-s 0.014534 (t 4.92).
- **T1 tally 152/192 ±10% (was 116), 187/192 ±30% (was 162)** — sell side
  42/64 ±10% (was 28), buy 57/64, buy-sell 53/64.
- T5 C_12 0.102072 (t 4.40; paper 0.0951, +7.3%) / C_36 0.069595 (t 1.17;
  paper 0.0406, +71.4% — noisy endpoint, WARN-flagged as before). T5 tally
  41/144 ±10%, 90/144 ±30%.
- **T8 PA C_36 −0.341976** (paper −0.4081, +16.2%, was +26%) / **PB C_12
  0.062140** (paper 0.0583, +6.6%). **T8 tally 56/288 ±10% (was 26), 151/288
  ±30% (was 110)**.
- T9 months 1–7 mean **+0.007187** (paper ~+0.007; was +0.006278) — 6/6
  positive & significant; months 11–18 mean −0.004792 (paper ~−0.007);
  coverage 12,528/post-month (vintage). T9 tally 12/72 ±10%, 26/72 ±30%.
- A1 WRSS per-$-long mean **0.021149** (paper 0.045, −53% — the [f−5,f]
  alignment moved it FURTHER from the anchor than the pre-A13 [f−6,f−1]
  0.034; reported honestly) / **corr 0.962590** (paper 0.95 — the
  discriminating anchor IS matched). A2 −0.006100 (unchanged); **A3 +0.001199
  (unchanged, exact)**. **A4 θ −1.9807** (paper −2.29, +13.5%, was +18.8%),
  **h1 −2.2076** (−2.55, +13.4%, was +33.8%), h2 −1.5783 (−1.83, +13.8%) —
  the corrected [f−5,f] window moved θ and h1 CLOSER to the paper.
- Per-table tallies (after): T2 13/21 ±10%, 20/21 ±30%; T3 165/322 ±10%,
  264/322 ±30%; T4 66/112 ±10%, 97/112 ±30%; T6 52/56 ±10%, 56/56 ±30%;
  T7 61/120 ±10%, 98/120 ±30%.
- **Cohort-count invariants (all asserted post-fix):** every (panel, J, K)
  grid has exactly K contributing cohorts in all 300 reporting months; T5
  n_1=299 (n_12=288, n_36=264); T8 Panel A 168 formations (n_1=167/n_36=132),
  Panel B 288 (n_1=287/n_36=252); earnings 120 cohorts; key count 1,349
  (1,327 contract T1–T9 + 11 dec_* + 11 diag_*); data/ = ['panel.parquet'].
- **Hand-verify (corrected cohort, <1e-12):** formation f=1979-12 (paper's
  Jan-1980 portfolio) ranks on cumret_6_raw@1980-01 = compound [1979-07..1979-12]
  (max|diff| 0.0 over 2,205 stocks) and holds from 1980-01; decile 1/10
  next-month EW match the pipeline to <1e-12. Full run exit code 0.

**Status:** complete; the timing correction is a net improvement across nearly
all tables (sell-side shortfall resolved; T1 116→152, T8 26→56 at ±10%; A4 θ
and T9 months 1–7 closer). The A1 WRSS MEAN moved away from its anchor under
the mandated [f−5,f] alignment (corr still matches at 0.963); reported
honestly per methodology-over-numbers. The two retired guards and the
now-stale REPORT §3 diagnostic figures are flagged for the replicator
(REPORT.md untouched per scope).

---

## Post-audit-2 cleanup (replicator, m1 + m3)

### Cleanup — Problem: audit-2 minors m1 (stale REPORT numbers) and m3 (undocumented classification rule)
- Diagnosis (audit-2 §2/§4): REPORT.md §4 prose re-used four PRE-A13
  anchor numbers (T6 January proportion 0.24, T7 Jan-70–74 −10.1% and
  75–79 −0.33%/mo, T1 PA 3/3 0.0038) and §3 had an arithmetic slip
  ((1.008797)¹²−1 written as 11.13%, actually 11.08%); the per-cell
  classification rule (Tier 1 = within tolerance; Tier 2 = same sign +
  ≤200% deviation; FAIL otherwise) was applied but stated nowhere.
- Next fix: replace the five REPORT values from computed_values.json
  (prop_jan_all 0.20; sp_all_jan_7074 −0.112865 (t −2.467);
  sp_all_all_7579 −0.006356 (t −0.826); PA_J3_buy_sell_K3 0.002333;
  11.08%); add the classification-rule statement to REPORT §4 (m3) with
  the note that 54 nil cells shift Tier 2→FAIL under the strict
  symmetric ratio reading while Tier 1 (1,127) is unchanged.
- Before metric: audit-2 row 7 ✗ (SUMMARY/REPORT mismatch on 4 values +
  1 slip); rule undocumented.
- After metric: all five stale strings verified gone (grep count 0);
  rule stated in REPORT §4 and in src/classify.py's docstring (m2/m3
  committed by rep-worker). No computed value changed.
- Status: resolved

(Companion m2/m4 cleanup — committed src/classify.py generator for
results/cell_classification.json with per-table tier counts in the table
md files, and updated the primary_diagnostics.md comparison constants to
post-A13 values — performed by the rep-worker; see its entry above/below.)

---

## Post-audit-2 cleanup (rep-worker, m2 + m4)

### Cleanup — Problem: uncommitted classifier (m2) + stale pre-A13 diagnostics comparison column (m4)
- Problem: `results/cell_classification.json` had no committed generator in
  the repo (audit-1 m4 / audit-2 m2 — per-table tier counts were surfaced
  only in the JSON; the artifact was not regenerable from committed code),
  and `results/primary_diagnostics.md` still printed the PRE-A13 REPORT §3
  comparison constants (0.011530 / t 4.17 / Sharpe 0.83 / total 2078.0% /
  MDD −41.9% / FF5 16.84% t 4.86 / R² 0.13 / arithmetic 13.84% / geometric
  13.12%), so every row showed "within tol: False" next to the correct
  post-A13 diagnostics.
- Next fix: commit `src/classify.py` (contract + computed_values.json →
  regenerated `cell_classification.json` + per-table tier counts, with the
  classification rule stated in the module docstring per audit-2 m3: Tier 1
  = within tolerance_pct; Tier 2 = same sign & ≤200% deviation, i.e. |ours|
  ≤ 3×|paper|; FAIL = opposite sign / >200% / paper = 0; ours = None →
  SKIP), idempotently appending a one-line per-cell evaluation to each of
  the nine contract-table results mds plus an anchor-statistics line to
  `table_8_decomposition.md`; update `DIAG_REPORT_ANCHORS` and the
  comparison rows in `src/main.py`'s `compute_primary_diagnostics` to the
  post-A13 REPORT §3 values read off the diag_* keys (mean 0.008797, t 2.91,
  Sharpe 0.58, total 786.5%, MDD −60.2%, arithmetic 10.56%, geometric 9.12%,
  FF5 α 14.50%, FF5 t 3.88, R² 0.16, rf-sub 7.70%) and add a within-tol
  column to the md table.
- Before: audit2.md §2 flagged m2/m4 (requires_iteration: false); classifier
  uncommitted, no tier lines in the table mds, diagnostics comparison column
  pre-A13 → 11/11 rows "within tol: False".
- After: `src/classify.py` committed and its regeneration is BYTE-IDENTICAL
  to the existing artifact (md5 b3453adc752006be0aea6a97dc9982cb before and
  after; the rule reproduces 1327/1327 cells — GRAND 1127 Tier 1 / 130
  Tier 2 / 70 FAIL / 0 SKIP); tier lines appended to all nine
  contract-table mds + the decomposition md, verified idempotent (second
  run is a no-op, md5s unchanged); full main.py re-run exits 0 with the
  comparison column post-A13 → 11/11 rows "within tol: True";
  `computed_values.json` (md5 f712686b5cc1073353b1cd086e8957b2),
  `panel.parquet` (md5 ced63e88f8b38043675e9458bd099d3d),
  `cell_classification.json` and every other results artifact md5-identical
  after the re-run (primary_diagnostics.md / sell_diagnostic.md carry
  Generated: timestamps — the documented exception). No computed value moved.
- Status: resolved
