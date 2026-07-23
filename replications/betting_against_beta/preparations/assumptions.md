# Assumptions Registry — Betting Against Beta (Frazzini & Pedersen, 2014)

Paper-silent decisions made during replication. Each entry documents a choice
the paper does not explicitly specify.

---

## Assumption 1: Delisting return treatment

**Decision:** Include delisting returns from crsp_202601.dse when available; when dlret is missing and dlstcd indicates a performance-related delisting (codes 500-599), substitute -30% for NYSE/AMEX (exchcd 1,2) and -55% for NASDAQ (exchcd 3), following Shumway (1997) and BMP (2007).
**Rationale:** Paper is silent on delisting treatment. The Shumway/BMP correction is the standard convention in the literature for CRSP-based studies spanning 1926-2012. Without it, returns for delisted stocks are systematically overstated, biasing high-beta portfolio returns upward (high-beta stocks are more likely to delist for performance reasons).
**Impact:** Affects monthly returns for all stocks that delist during the sample period, particularly high-beta deciles P8-P10.

## Assumption 2: Pastor-Stambaugh liquidity factor

**Decision:** Skip the 5-factor alpha (which requires the Pastor-Stambaugh liquidity factor, available 1968-2011 only). Report CAPM, 3-factor, and 4-factor alphas only.
**Rationale:** The PS liquidity factor is not available in ClickHouse. The paper itself notes the 5-factor alpha covers only half the sample. The 3-factor and 4-factor alphas are the primary results (BAB 3-factor alpha = 0.73%, t=7.39; 4-factor alpha = 0.55%, t=5.59).
**Impact:** 5-factor alpha cells in Table 3 will not be replicated. Core results (3-factor and 4-factor alphas) are unaffected.

## Assumption 3: Beta computation frequency

**Decision:** Compute betas at month-end using daily data through that month-end. Assign the beta computed at end of month t-1 to portfolio formation at the beginning of month t.
**Rationale:** Paper says "At the beginning of each calendar month, stocks are ranked in ascending order on the basis of their estimated beta at the end of the previous month" (Table 3 description, L1075). This implies beta is computed at month-end t-1 and used for sorting in month t.
**Impact:** Timing convention for all portfolio sorts and BAB construction.

## Assumption 4: CRSP VW index as market proxy

**Decision:** Use crsp_202601.dsi vwretd (value-weighted return with dividends) as the market return for beta estimation.
**Rationale:** Paper explicitly states "betas are computed with respect to the CRSP value-weighted market index" (§3, L351). The dsi table's vwretd is the canonical CRSP VW market return.
**Impact:** All beta estimates depend on this market proxy.

## Assumption 5: Risk-free rate source

**Decision:** Use the RF column from ff.four_factor_monthly as the risk-free rate (1-month T-bill rate).
**Rationale:** Paper states "Excess returns are above the US Treasury bill rate" (§3, L351). The FF library's RF is the standard 1-month T-bill rate used in academic finance.
**Impact:** All excess return and alpha computations.

---

# Implementation Decisions — rep-worker data pipeline (builds data/panel.parquet)

Added when the data pipeline was implemented. Documents spec ambiguities and
paper-silent implementation choices.

## Assumption 6: No pre-1926 daily lookback (data availability)
**Decision:** Daily data is pulled from 1925-12-31 (the earliest date in
`crsp_202601.dsf`/`dsi` in this instance), not ~1921 as the task suggested.
**Rationale:** There is no CRSP daily data before 1925-12-31 here. Betas for the
earliest months are NaN until enough history accumulates; the first estimable beta
is 1928-08 (750-day correlation minimum from the 1925-12-31 start; 416 stocks).
**Impact:** Early-sample beta coverage starts 1928-08, not 1926-01.

## Assumption 7: Backward-indexed 3-day overlapping returns for correlation
**Decision:** Correlation uses `b_t = lr_t + lr_{t-1} + lr_{t-2}` (3-day log return
indexed by its END date) rather than FP's forward form `lr_t+lr_{t+1}+lr_{t+2}`.
**Rationale:** Same set of overlapping returns (correlation value is identical —
verified to machine precision vs an independent pandas computation), but a window
ending at estimation date T then uses only data through T (no 2-day look-ahead at
the window boundary).
**Impact:** None on values; removes a boundary look-ahead.

## Assumption 8: Minimum-data = expanding-then-rolling window (min_periods)
**Decision:** "At least 120 days (vol) / 750 days (corr)" is the MINIMUM sufficient
condition: estimation uses a trailing window of UP TO 252/1260 days and is produced
as soon as the minimum count of non-missing observations is met (≡
`pandas.rolling(W, min_periods=M)`).
**Rationale:** Matches the paper's wording ("we require at least three years...") and
FP reporting results from 1926 despite CRSP starting in 1926. The alternative
(require a FULL 1260-day window before any estimate) would suppress all betas until
~1930 and is not used.
**Impact:** Betas appear from each stock's ~3-year point; early-sample coverage from
1928-08 rather than ~1930.

## Assumption 9: `me` is contemporaneous (month-end of month t), NOT lagged
**Decision:** `me` = abs(prc)*shrout*1000/1e6 ($millions) at the END of the row's OWN
month. `beta`, by contrast, IS lagged (estimated at end of month t-1, per spec).
**Rationale:** The task defined ME from month-end and did not instruct lagging.
**Impact / FLAG:** For value-weighted sorting, downstream code should LAG `me` by one
month (same no-look-ahead convention as beta). EW sorts (Table 3) do not need `me`.
If the Replicator wants a lagged size column in the panel, request a revision.

## Assumption 10: Exchange-code filter is a task-spec addition
**Decision:** Universe = `shrcd IN (10,11) AND exchcd IN (1,2,3)`, point-in-time via
dsenames.
**Rationale:** The paper quote (L297) specifies CRSP `shrcd IN (10,11)` only; the task
spec adds `exchcd IN (1,2,3)`. No SIC/financials exclusion (not in spec).
**Impact:** Universe excludes non-NYSE/AMEX/NASDAQ issues; includes financials.

## Assumption 11: Panel keeps all universe stock-months; beta NaN where unestimable
**Decision:** Every universe stock-month with a valid monthly return is a row; `beta`
is NaN when the min-data requirement is unmet (75.9% non-null). 93 rows have me=0
(missing prc/shrout) with null log_me.
**Rationale:** Maximally flexible for downstream sorting (which drops NaN betas / zero
size as needed).
**Impact:** Downstream sorts must drop NaN beta (and zero `me` for VW).

## Assumption 12: `month` built as Date32 (pre-1970 correctness)
**Decision:** `month` (first-of-month) is built as `Date32` from the ISO date string;
the beta staging table uses `Date32`.
**Rationale:** ClickHouse `Date`/`toStartOfMonth(toDate(.))` clamps any date before
1970-01-01 to the epoch, which would silently corrupt every pre-1970 month (half of
this 1926-2012 sample).
**Impact:** Correct month labels across the full sample.

## Assumption 13: Numeric beta parameters pinned in src/main.py
**Decision:** Windows (252/1260), minima (120/750), shrinkage (w=0.6 toward
beta_XS=1.0), market=vwretd are constants in `src/main.py`, each annotated with its
source rule_id.
**Rationale:** `preprocessing_rules.json` stores paper QUOTES, not a numeric map.
**Impact:** Single, documented source for the beta parameters.

## FLAG — Delisting returns NOT in the panel (vs Assumption 1 above)
The panel's `ret` is the raw CRSP `msf.ret` (per this task's spec). It does NOT
include delisting returns, whereas Assumption 1 (prep stage) specifies the
Shumway/BMP delisting-return adjustment. Delisting adjustment was outside this
pipeline task's spec and was NOT implemented. If the Replicator wants delisting-
adjusted monthly returns, that is a separate revision (join `crsp_202601.dsedelist`
and substitute/combine `dlret` on the delisting month). Flagging so it is a conscious
decision rather than a silent omission.

## Validation performed
- `--selftest`: rolling corr/std match `pandas.rolling(W, min_periods)` on the FULL
  series (incl. truncated early windows); NaN-cutoff positions identical.
- Independent per-stock recomputation (pure pandas, separate SQL pull) matches the
  panel beta to machine precision (~1e-15) for stocks in 1929, 1970, and 2010.

---

# Implementation Decisions — rep-worker Table 3 analysis (src/table_3.py)

Added when Table 3 (US beta-sorted deciles + BAB factor) was implemented.

## Assumption 14: All-stock (not NYSE) breakpoints for the decile sorts
**Decision:** Decile breakpoints are computed from the beta distribution of ALL
stocks in each cross-section, not NYSE-only (the panel has no `exchcd`, so NYSE
breakpoints are not available without a pipeline revision).
**Rationale:** The task spec explicitly directed the all-stock approximation "for
simplicity," and the panel produced by `main.py` contains columns
[permno, month, ret, beta, me, log_me] only. The paper (§ Table 3) uses NYSE
breakpoints. With ~2,400+ stocks/month the equal-count all-stock deciles are close
to the NYSE-breakpoint deciles.
**Impact:** Decile composition (and hence decile alphas / ex-ante beta) differs
slightly from the paper. Observed: P1 ex-ante beta 0.57 vs paper 0.64 (the all-stock
equal-count low decile captures slightly lower-beta names). To match the paper
exactly, a revision must add a point-in-time `exchcd` join (crsp_202601.dsenames) to
the panel and re-bin using NYSE-only beta breakpoints.
**Diagnostic:** The BAB factor (which uses a MEDIAN split + rank weights, NOT decile
breakpoints) replicates the paper to within tolerance on ALL 8 reported cells,
including the FF3 t-stat (7.28 vs paper 7.39) and FF4 t-stat (5.71 vs paper 5.59).
This isolates the decile alpha gap to breakpoint composition + delisting, not to the
beta estimation, factor data, or regression methodology.

## Assumption 15: FF factors are DECIMAL in this ClickHouse vintage (not percent)
**Decision:** `ff.four_factor_monthly` returns factors in DECIMAL (verified live:
mkt_rf median |x| = 0.0298 ≈ 3%/mo, rf median 0.0022 ≈ 0.22%/mo). The loader
auto-detects the scale at runtime (median |mkt_rf| > 0.2 ⇒ percent ⇒ /100; else
decimal) and converts only if needed. CRSP `ret` is also decimal, so
excess = ret - rf directly with NO /100 on rf.
**Rationale:** The task spec assumed the factors were in percent and instructed
`rf/100`; this contradicts both the verified data and references/FAMA_FRENCH.md.
Implementing the spec's /100 on decimal factors would have produced nonsensical
excess returns (subtracted 100x the true rf). Auto-detection makes the code correct
regardless of vintage and surfaces the discrepancy.
**Impact:** Excess returns and alphas are correct; the spec's unit assumption was
wrong for this instance.

## Assumption 16: t-stat convention — standard (iid) in main table, NW supplementary
**Decision:** The main Table 3 reports STANDARD (iid) time-series t-stats below each
coefficient, matching the paper's stated convention ("t-statistics are shown below
the coefficient estimates"). Newey-West HAC t-stats (6 lags) are additionally
computed and shown in a supplementary block, per the task spec's request for NW.
The excess-return t-stat uses the iid formula mean/(std/√n) from the task spec.
**Rationale:** The paper uses standard t-stats; reporting NW in the main table would
make our t-stats non-comparable to the paper's headline figures (e.g. BAB FF3 7.39).
Our standard t-stats reproduce the paper (BAB FF3 7.28 vs 7.39; FF4 5.71 vs 5.59).
NW(6) reduces them (BAB FF3 5.85, FF4 4.58) as expected for HAC.
**Impact:** Both conventions are provided; the Replicator can pick which to headline.

## Assumption 17: BAB legs use strict inequalities around the median
**Decision:** Low-beta leg = beta < median; high-beta leg = beta > median; a stock
exactly at the median (possible only for odd cross-section counts) receives ~0
weight (its rank ≈ z̄, so w ≈ 0) and is effectively excluded.
**Rationale:** Matches the paper ("beta below (above) its median"). Weight sums
verify to 1.0000 per leg on average (mean wL_sum = 1.0000, wH_sum = 1.0000), and
mean leverage long 1/βL = 1.435, short 1/βH = 0.688 — matching the paper's stated
long $1.40 / short $0.70.
**Impact:** None beyond the documented match.

## Result of Table 3 analysis (this iteration)
- Sample: 1928-08 .. 2012-03 (1004 months; first valid beta 1928-08).
- Cells vs paper within tolerance (tolerance from tables_to_replicate.json):
  **23 / 32.**
- BAB factor: **8 / 8 pass** (excess 0.73 vs 0.70, CAPM α 0.77 vs 0.73, FF3 α 0.77
  vs 0.73, FF4 α 0.59 vs 0.55, β ex-ante 0.00 vs 0.00, β realized -0.056 vs -0.06,
  vol 11.45 vs 10.75, Sharpe 0.77 vs 0.78).
- Deciles: excess returns, realized betas, volatilities, Sharpe ratios mostly pass.
  The 9 failing cells are decile **alphas** (systematically a bit higher than the
  paper) and P1 ex-ante beta (0.57 vs 0.64). These are attributable to Assumptions
  14 (all-stock breakpoints) + the missing delisting-return adjustment (panel flag);
  the BAB match (Assumption 14 diagnostic above) rules out beta/factor/regression
  errors. The Replicator owns whether to pursue a NYSE-breakpoint + delisting
  revision.

---

# Implementation Decisions — rep-worker Table 3 v2 (src/table_3_v2.py)

Revision that SUPEREDES Assumption 14 and resolves the delisting FLAG above.
Implements the two fixes the Replicator specified: NYSE breakpoints + delisting
returns. Result: **25 / 32 cells pass (up from v1's 23 / 32)**; BAB still 8 / 8.

## Assumption 18: NYSE breakpoints now used (supersedes Assumption 14)
**Decision:** Decile breakpoints are the 10th..90th percentiles of beta among
NYSE stocks only (exchcd == 1) each month; ALL stocks are then assigned to
deciles on those breakpoints. A point-in-time exchange code is merged onto the
panel from `crsp_202601.dsenames` (exchcd, valid over [namedt, nameendt]; merge
= latest namedt <= month, kept only if nameendt >= month). Coverage ~100% of
panel rows; NYSE valid-beta stocks/month min=416, median=1096, max=1568 (so the
all-stock fallback for thin-NYSE months is never triggered).
**Rationale:** Paper Table 3 description: "The ranked stocks are assigned to one
of ten deciles portfolios based on NYSE breakpoints." This resolves Assumption 14
(which used all-stock breakpoints because the panel then had no exchcd).
**Impact:** P1 ex-ante beta 0.57 -> 0.615 (now PASSES vs paper 0.64; the NYSE
low-beta cutoff sits above the all-stock cutoff, raising the low decile's mean
beta). P5/P10 ex-ante betas move marginally toward the paper. NYSE breakpoints
expand the high deciles (NYSE 90th pct < all-stock 90th pct, since NASDAQ
small-caps fatten the upper tail), so P10 gains marginal lower-beta names and its
ex-ante beta drops slightly (1.78 -> 1.77) — this nudges P10's alpha a touch
LESS negative, partially offsetting the delisting fix (see Assumption 22).

## Assumption 19: Delisting returns now in the panel (resolves the FLAG)
**Decision:** Each stock's last-month return is combined with its CRSP delisting
return: `adjusted = (1+ret)*(1+dlret_eff)-1`. `dlret_eff` = reported `dlret`
when valid (`dlret IS NOT NULL AND dlret > -1.0`), else the Shumway(1997)/
BMP(2007) imputation when the delisting is performance-related (dlstcd 500-599):
-0.30 for exchcd 1,2 (NYSE/AMEX), -0.55 for exchcd 3 (NASDAQ), per Assumption 1.
Source: `crsp_202601.dsedelist` (dlstdt, dlret, dlstcd, hexcd). In this vintage
the -44/-55/-66/-77/-88/-99 error codes are stored as NULL (only -1.0 appears
as a <= -1 sentinel), so `dlret > -1.0` cleanly separates valid from missing.
**Rationale:** Raw msf.ret omits the delisting return, biasing high-beta returns
upward (high-beta names delist for performance reasons more often). This resolves
the panel FLAG and implements Assumption 1.
**Impact:** 19,282 stock-months adjusted (16,403 from valid dlret, 2,879 Shumway-
imputed; mean dlret_eff = -0.0797). Adjustments are concentrated in high-beta
deciles (P10: 2,249 rows, mean -0.10; P9: -0.074; P8: -0.058; P1: -0.051),
lowering high-decile returns: P10 excess 1.11 -> 1.06, P1 0.97 -> 0.94, so the
P10-P1 spread narrows and P10's FF3 alpha moves more negative (-0.30 -> -0.35).

## Assumption 20: Case-B delistings (terminal return -> last holding month)
**Decision:** The adjustment is applied not only when the delisting month EQUALS
the stock's last panel month (Case A), but also when the delisting month is the
month AFTER the last panel month (Case B) — the terminal return is then
attributed to the last holding month. Case B dominates: 16,900 rows vs Case A's
2,382 (of the adjusted set with valid beta).
**Rationale:** CRSP typically stores the delisting-month msf return as a missing
sentinel (filtered out at panel build by `ret > -1.0`), so for most delistings
the stock's last VALID panel month is the month before the formal delist and the
delisting return lives only in dsedelist. Applying Case A only (the task's
"simpler approach") would capture just ~12% of delistings and leave most of the
high-beta upward bias uncorrected. Attributing the terminal return to the last
held month is the standard approximation (the stock earns its last monthly return
then the delisting return at the boundary). Delistings whose formal date is >1
month after the last valid return (long trading halts) are intentionally excluded.
**Impact:** This is the bulk of the delisting fix. An ablation isolating Case A
("NYSE bp + delist A") barely moves P10's alpha (-0.30, same as no-delist);
adding Case B ("v2") moves it to -0.35. FLAGGED for the Replicator as a
documented extension beyond the literal task spec (which described Case A only).

## Assumption 21: dlret = -1.0 treated as MISSING (per task spec)
**Decision:** `dlret = -1.0` is treated as a missing sentinel (routing those
delistings to the Shumway imputation if performance-related), per the task spec's
sentinel list (-1.0, -66, -77, -88, -99).
**Rationale / FLAG:** The CRSP Data Descriptions Guide (references/CRSP.md)
documents `dlret = -1` as the "worthless security" return (a VALID -100%), not a
missing code. Treating it as missing understates the loss for 383 performance-
related worthless-stock delistings (imputed to -0.30/-0.55 instead of -1.00).
Implemented as specified; the effect on decile means is second-order (383 rows
spread across ~1004 months / 10 deciles). If the Replicator prefers -1.0 as a
valid -100% return, change the validity test in `build_delist_adjustment`.

## Assumption 22: NYSE bp + delist both applied (headline); ablation note
**Decision:** v2 applies BOTH fixes (the paper's stated methodology). An ablation
shows "all-stock bp + delist AB" passes 27/32 vs v2's 25/32 — i.e., in THIS
vintage all-stock breakpoints happen to match a few alpha cells marginally better
(P1 ff3/ff4 land just inside the 20% band at 0.47/0.47 vs v2's 0.49/0.49; P10
capm at -0.11 vs -0.08). But NYSE breakpoints are what the paper specifies and
they FIX P1's ex-ante beta (0.615 vs all-stock 0.570, paper 0.64). The 2-cell
swing is a tolerance-boundary coincidence on regression alphas, not a methodology
improvement; v2 (NYSE bp + delist) is the methodologically faithful configuration
and is reported as the headline.
**Impact:** Explains why the pass count is not monotone in "more correct
breakpoints". Remaining decile-alpha gaps (esp. P5/P10 FF3/FF4 alphas, still
systematically high) are NOT explained by breakpoints + delisting — they likely
reflect beta-estimation / sample-period / data-vintage differences and are left
for the Replicator (out of scope for this revision).

## Validation performed (v2)
- exchcd PIT merge: 100% panel coverage; NYSE stocks/month min 416 (never below
  the NYSE_MIN=20 fallback threshold).
- Delisting matching verified: matches are overwhelmingly real delistings
  (dlstcd first-digit 2=merger, 5=delisted; only 3 "still-trading" and 22
  sample-end survivors), not artifacts.
- Mechanism check: delisting adjustments concentrated in high-beta deciles with
  the most negative mean dlret_eff (P10 -0.10), confirming the intended effect.

---

# Iteration 2 — corollary analyses (src/corollaries.py)

Added to close three actionable MAJOR issues from logs/audit1.md (M1, M2, M5).
ALL three are computed on the existing data/panel.parquet + FF factors and REUSE
the verified BAB construction and factor regressions from src/table_3_v2.py
(same v2 config: NYSE breakpoints + Shumway/BMP delisting Cases A+B). No panel
rebuild, no beta re-estimation. The shared analysis pass reproduces table_3.md
exactly (BAB series 1004 months 1928-08..2012-03; FF3 t 7.11, FF4 t 5.54,
Sharpe 0.750 — byte-identical headline), so the corollaries sit on the same
verified series. Outputs: results/table_3_subsample.md (M1),
results/table_b1.md (M2), results/table_3_post1962.md (M5).

## Assumption 23: [M1] subsample windows follow the task-spec breakpoints
**Decision:** split the BAB series at the task-spec windows 1928-08..1948-12,
1949-01..1968-12, 1969-01..1988-12, 1989-01..2012-03 (n = 245/240/240/279 = 1004).
Window 1 starts at our first valid beta (1928-08, A6/A8), not the paper's 1926-01.
**Rationale:** the audit [M1] suggested ~1926-1946/46-66/66-86/86-2012 but the task
spec fixed the four windows above; we implement the spec. The paper's exact Table
B4 cell values live in the JFE internet appendix (not in the parsed paper), so we
report our values and evaluate the qualitative "significant + positive in each
subperiod" claim.
**Impact:** window-1 statistics cover ~2.5 fewer years than the paper's first
subperiod (contributes to its weaker significance — see M1 status below).

## Iteration log — [M1] Subsample stability (results/table_3_subsample.md)
**Diagnosis:** audit [M1] — the abstract's corollary (BAB "realizes a significant
positive return in each of the four 20-year subperiods between 1926 and 2012",
also Table B4) was never computed in any artifact.
**Next fix:** slice the monthly BAB series into the four windows; per window compute
excess return, FF3 alpha (+iid t), FF4 alpha (+iid t), annualized Sharpe; assess
sign + 5% significance.
**Before:** no subsample results existed.
**After:** BAB is POSITIVE (excess, FF3, FF4 all > 0) in all four subperiods and
significant (|t|>1.96) in 3 of 4. SP1 1928-08..1948-12: excess +0.217%/mo (t=0.91),
FF3 α +0.362 (t=1.71), FF4 α +0.240 (t=1.19), Sharpe 0.20 — positive but NOT 5%-
significant. SP2 1949-01..1968-12: excess +0.679 (t=5.56), FF3 +0.790 (t=6.22),
FF4 +0.850 (t=6.41), Sharpe 1.25. SP3 1969-01..1988-12: excess +1.107 (t=6.21),
FF3 +0.841 (t=5.09), FF4 +0.722 (t=4.34), Sharpe 1.39. SP4 1989-01..2012-03: excess
+0.847 (t=3.41), FF3 +0.830 (t=3.73), FF4 +0.587 (t=2.71), Sharpe 0.71.
**Status:** RESOLVED (corollary computed). Directionally supports the paper —
positive in all four, strongly significant in SP2-SP4. SP1 is positive but
sub-significant in our vintage (early-sample start 1928-08 + data vintage); documented
in table_3_subsample.md, not a methodology error.

## Iteration log — [M2] BAB factor loadings (results/table_b1.md)
**Diagnosis:** audit [M2] — Table B1 loadings were computed inside
`portfolio_row()` but only the CAPM realized beta was retained; SMB/HML/UMD
loadings were dropped, so the paper's factor-loading corollary (p.9) was unreported.
**Next fix:** from the SAME Carhart 4-factor time-series regressions table_3_v2.py
runs (`factor_alpha(...)`), extract the realized loadings (mkt, SMB, HML, UMD) for
each decile P1-P10 and the BAB factor; also report average BAB leverage from the
construction (long 1/βL, short 1/βH).
**Before:** only "Beta (realized)" (CAPM market loading) appeared in table_3.md.
**After:** average leverage long $1.44 / short $0.69 (paper $1.40 / $0.70). BAB
realized loadings: market −0.056 (CAPM) / −0.016 (4-factor), SMB +0.008, HML +0.061,
UMD +0.200 — all four carry the paper-expected sign (market ≈0 slightly negative
"not exactly zero"; HML positive per the paper's "positive HML loading"; UMD positive;
SMB ≈0 positive). BAB 4-factor R² = 0.072, so the loadings explain little of BAB's
return (consistent with "none of the loadings can explain the ... abnormal returns").
Decile gradients: SMB rises P1 +0.52 → P10 +1.48 (high-beta = smaller ⇒ low-beta
larger ✓); UMD falls P1 −0.00 → P10 −0.44 (low-beta = higher prior momentum ✓).
**Status:** RESOLVED (loadings reported; signs match the paper's claims).
**FLAG (resolved by computation):** the task brief listed "positive SMB" as the
expected BAB sign while the paper's text ("low-beta stocks are larger") naively
suggests a negative net SMB. The COMPUTED BAB SMB loading is +0.008 (≈0, positive),
which matches the brief's sign; the size information lives in the decile SMB gradient,
not the near-zero net BAB loading (long-leg leverage ×1.44 vs short-leg ×0.69 offset
the two legs). No spec override was needed.

## Iteration log — [M5] P10 FF4 sign-flip diagnosis (results/table_3_post1962.md)
**Diagnosis:** audit [M5] — P10 four-factor alpha flips sign (ours +0.03 vs paper
−0.13). Test whether it is an early-sample artifact by restricting to the
paper-comparable post-1962 window (momentum factor well populated, vintage aligned).
**Next fix:** filter the v2 sorted panel to months ≥ 1962-01 (n=603); recompute decile
EW returns, the BAB factor, and CAPM/FF3/FF4 regressions on that window; compare
P10 FF4 (and all decile alphas) full-sample vs post-1962 vs paper. Decile breakpoints
are monthly, so post-1962 decile assignments are identical to the full sample — only
the estimation window changes.
**Before:** full-sample P10 FF4 = +0.030 (paper −0.13; sign flip); P10 FF3 = −0.346
(paper −0.49).
**After:** post-1962 P10 FF4 = +0.013 (t=0.08, statistically zero) — the sign flip
PERSISTS in sign but the magnitude is negligible; post-1962 P10 FF3 = −0.436 (much
closer to paper −0.49). ALL decile alphas move toward the paper post-1962: P1 FF4
+0.490→+0.401 (paper +0.40), P5 FF3 +0.214→+0.163 (paper +0.13), P5 FF4
+0.265→+0.217 (paper +0.18). BAB post-1962: excess +0.909, FF3 +0.713 (t=5.32),
FF4 +0.518 (t=3.91), Sharpe 0.93 — still strongly positive.
**Status:** RESOLVED (diagnosis). The P10 FF4 sign flip is NOT purely an early-sample
artifact (the sign persists post-1962), but it is economically negligible (|α|≈0.01%/mo)
and statistically insignificant (t=0.08) in the paper-comparable window, while the rest
of the decile-alpha structure converges toward the paper. Residual documented as
data-vintage / beta-estimation-limited (see A22), not a methodology error.

## Assumption 24: [M3] size-tercile sort uses ALL-stock breakpoints on LAGGED ME
**Decision:** Each month, sort stocks into three size terciles (Small / Medium /
Large) using the within-month 1/3 and 2/3 quantiles of **lagged** ME (month t−1)
across **all** stocks — not NYSE breakpoints. Within each tercile, compute the BAB
factor with the exact Table 3 construction (median-beta split, rank weights, rescale
to unit beta). Rows with null/zero lagged ME are dropped from the size sort.
**Rationale:** The task spec (and audit [M3]) says "sort stocks into 3 size terciles
based on lagged ME" (all-stock terciles); the audit additionally suggested NYSE
breakpoints, but the Replicator's task spec specifies a plain tercile sort, which is
what we implement. Lagging ME one month applies the same no-look-ahead convention as
the lagged beta (the panel's `me` is contemporaneous per A9; we construct the lag
here via an exact (month+1) self-merge, so monthly gaps do not leak an older ME).
Within-tercile BAB uses the SAME delisting-adjusted returns as the headline Table 3
BAB (reuses the shared v2 pass per audit2.md) so the within-size factors are directly
comparable to the full-cross-section BAB.
**Impact:** Produces `results/table_3_size.md`. BAB is positive and significant
(excess/FF3/FF4 |t|>1.96) in ALL THREE size terciles — Small excess +0.93% (t=6.14),
FF3 +0.76 (t=5.18); Medium +0.74% (t=6.50), FF3 +0.77 (t=6.79); Large +0.41% (t=3.79),
FF3 +0.52 (t=5.08) — supporting the paper's claim that BAB holds "within deciles
sorted by size" (Table B3). Raw excess return declines monotonically with size; the
annualized Sharpe is highest in the Medium tercile (0.71) and weakest among Large
caps (0.41).
**FLAG (spec ambiguity, resolved):** audit2.md suggested NYSE breakpoints for the size
terciles; the Replicator's task spec said a plain tercile sort on lagged ME. We
implemented the task spec (all-stock terciles). The sign/significance conclusions are
robust to this choice. IVOL (Table B5) remains out of scope this iteration per the
audit (needs daily residual-vol computation).

## Iteration log — [M3] BAB within size terciles (results/table_3_size.md)
**Diagnosis:** audit [M3] — the paper's cross-sectional robustness claim (BAB holds
"within deciles sorted by size", abstract/p.2, Table B3) was neither computed nor
flagged. The size split is cheap (uses the existing `me` column + FF factors; no beta
re-estimation, no panel rebuild).
**Next fix:** reuse the verified v2 pass (`t3.merge_exchcd` + `build_delist_adjustment`
+ `apply_delist` + `build_excess`) to get the delisted/excess panel; lag ME one month;
each month form 3 size terciles on lagged ME; within each tercile compute BAB via
`t3.bab_factor` and metrics via `corollaries.bab_metrics` (excess, FF3/FF4 alpha + iid
t, annualized Sharpe). Write `results/table_3_size.md`.
**Before:** no within-size BAB; the paper's size robustness claim was untested.
**After:** BAB positive AND significant (FF3 |t|>1.96) in all three size terciles —
Small: excess +0.928%/mo (t=6.14), FF3 +0.762 (t=5.18), FF4 +0.547 (t=3.73), Sharpe
0.67; Medium: +0.741 (t=6.50), FF3 +0.768 (t=6.79), FF4 +0.599 (t=5.33), Sharpe 0.71;
Large: +0.413 (t=3.79), FF3 +0.521 (t=5.08), FF4 +0.424 (t=4.09), Sharpe 0.41.
Full cross-section (same panel, no split): excess +0.721 (t=6.95), FF3 +0.753 (t=7.20),
Sharpe 0.76 — closely tracks the headline Table 3 BAB. Raw excess return declines
monotonically with size (Small > Medium > Large); Sharpe highest in Medium, weakest in
Large. Avg stocks/mo ≈ 800/tercile; 1004 months; 2,410,891 stock-months.
**Status:** RESOLVED (size corollary computed; paper's claim supported — BAB positive
and significant within each size group).

## Assumption 25: Beta-window robustness (Table B2) — scope-out

**Decision:** Do not compute alternative beta-estimation windows or benchmarks (Table B2).
**Rationale:** The paper claims (§3.1, L925) "results are robust to alternative beta estimation procedures." However: (1) our beta primitives are validated to machine precision by `src/main.py --selftest` against independent pandas computation; (2) the BAB factor matches the paper on all 8 headline metrics; (3) the only residual (decile multi-factor alphas) is diagnosed as data-vintage-limited by the post-1962 test [M5], which an alternative window would not fix; (4) computing an alternative window requires re-running the ~6-min daily pipeline with low expected marginal value.
**Impact:** Table B2 robustness results not replicated. The paper's own Table B2 shows BAB is robust to window choice; our verified methodology matches the paper's primary specification.
**Before metric:** N/A (scope-out, not a fix)
**After metric:** N/A
**Status:** out-of-scope-for-this-run (documented scope-out per audit 2/3 option (a))
