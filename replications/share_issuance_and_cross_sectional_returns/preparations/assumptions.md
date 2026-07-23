# Assumptions — Pontiff & Woodgate (2008) replication

Paper-silent decisions and iteration log. Paper-derived rules live in `preprocessing_rules.json`; this file records choices the paper does not fully specify, plus the Stage-7 iteration trace.

---

## Assumption 1: Universe filter — all CRSP securities vs common-stock filter

**Decision:** Build the panel both ways and reconcile against the paper's observation counts. Primary candidate: all CRSP securities (no shrcd/exchcd filter) with the paper's two stated conditions (nonmissing return at month t; ≥6 months in CRSP). Fallback: shrcd ∈ {10, 11}.
**Rationale:** The paper says "Our primary sample consists of all firm observations that are in the CRSP database as of January 1970" (L51) — no share-code or exchange filter is mentioned anywhere. The paper's counts (Table I: 2,285,189–2,312,597 over 408 months ≈ 5,600–5,668/mo; §I total sample 2,494,343 ≈ 6,113/mo) sit between the two candidates (sanity query: Jan-1990 no-filter = 6,757/mo vs shrcd 10/11 = 5,803/mo). The 6-month-listing and nonmissing-return rules remove recent IPOs and thin stocks, pulling the no-filter count down toward the paper's average. The reconciliation is empirical: whichever universe reproduces the paper's counts is the one they used.
**Impact:** Every observation count and every cell of Tables I, III, V, VI.

## Assumption 2: Table I/V descriptive statistics pool the full monthly panel

**Decision:** Compute Table I (1970–2003) and Table V (Sep 1932–Dec 1969) Panel A statistics by pooling all monthly cross-sections in the period, using the regression-ready variable definitions (June-held ME, July–June-held BM, contemporaneous ISSUE_{-11,0} and R_{-11,0} measured each month).
**Rationale:** The Table I caption says variables are "measured at the end of December" (L156), but the reported observation counts (2.29–2.31M for 1970–2003; 524–528K for 1932–1969) are only consistent with the monthly panel: 34 December cross-sections would give ~190K observations, not 2.3M. "Measured at the end of December" most plausibly describes the BM denominator's timing (December t−1 market cap, per L108), not the pooling frequency. Paper is otherwise silent on the pooling.
**Impact:** All Table I and Table V Panel A cells.

## Assumption 3: Regression dependent returns are in percent (×100)

**Decision:** Multiply all holding-period dependent returns by 100 before the Fama-MacBeth regressions.
**Rationale:** Table III Panel A intercepts (0.80–2.69) and slopes (BM 0.39, ISSUE −2.23) are two orders of magnitude larger than decimal-return equivalents; the mean monthly CRSP return is ~1%, so a BM-only intercept of 0.80 implies percent scaling. Table IV and Table VI show the same scale. The paper never states the scaling explicitly (paper silent), but the printed coefficients are unambiguous.
**Impact:** All Table III and Table VI coefficients and intercepts (not t-stats or R²).

## Assumption 4: Pontiff (1996) overlap adjustment — AR order n = k−1

**Decision:** For a k-month holding period, regress each slope's monthly time series on a constant plus k−1 of its own lags; use the intercept's standard error as the overlap-consistent SE of the mean slope. For k=1 (monthly), n=0, i.e., the plain FM t-stat.
**Rationale:** L134 says "an n-th order autoregressive process, with n equal to one minus the length of the holding period (in months)" — read literally n = 1−k, which is ≤0 for every holding period and cannot be the intended AR order; the natural reading consistent with overlap mechanics (k-month overlapping returns induce AR(k−1) in the slope series) and with k=1 giving the plain estimator is n = k−1. This is a typo-level OCR/typesetting issue, not a methodology choice. **Implementation form: see A16** — the AR(n) structure is on the RESIDUALS of a constant-only regression (GLSAR), per L134's exact wording ("the residuals of the process follow an n-th order AR process"); the AR-on-levels variant inflates |t| by ≈1/(1−Σρ) and does not reproduce the paper (Panel B ISSUE t −20.9 vs paper −7.26; GLSAR gives −7.68).
**Impact:** All multi-month t-statistics in Tables III and VI (6-month through 3rd-year panels).

## Assumption 5: Winsorization is per monthly cross-section — and Table I reports winsorized regressor statistics

**Decision:** Winsorize each right-hand-side variable at the 1%/99% percentiles within each month's cross-section (not pooled over the full sample). Table I/V descriptive statistics are computed on these winsorized regressors (returns stay raw).
**Rationale:** L132 says "we winsorize all right-hand-side variables by setting the smallest and largest 1% of the observations equal to the value of the observation at the respective 1% tail" without specifying pooled vs per-period. Per-period winsorization is the standard convention in monthly Fama-MacBeth estimation; the utils `fama_macbeth` primitive also winsorizes per period. The descriptive-statistics corollary was CONFIRMED in iteration 2: the paper's Table I stds match the winsorized series almost exactly and diverge sharply from raw — ISSUE 0.151 vs paper 0.15 (raw 0.230); DT-ISSUE 0.351 vs 0.33 (raw 0.438); BM 0.913 vs 0.94 (raw 0.999); MOM 0.404 vs 0.41 (raw 0.481); while R_{-11,0}, which is NOT a regressor, matches raw (0.889 vs 0.88). The selective pattern (every RHS variable, no returns) is the fingerprint of winsorized-regressor statistics.
**Impact:** All Table III and Table VI coefficients; Table I and Table V std columns.

## Assumption 6: Momentum window is months t−7 through t−2

**Decision:** MOM at regression month t = prod(1+ret) over months t−7..t−2 − 1 (six months, skipping the most recent month); NULL unless all six returns are present.
**Rationale:** L114: "The momentum proxy is the 6-month holding period return of the stock between month 1 and month 6. The momentum variable is lagged by 1 month to avoid losing predictive ability due to positive autocorrelation attributable to bid-ask bounce." With month 0 = the prediction month, months 1–6 are t−1..t−6, lagged one further month → t−2..t−7. This is the standard skip-one-month momentum convention (Jegadeesh-Titman). Requiring all six months explains why MOM has the fewest observations in Table I (2,285,189).
**Impact:** All MOM cells in Tables I, III, V, VI.

## Assumption 7: Holding-period windows start at the regression month; EWRETD imputation extends past delisting

**Decision:** At month t: R1 = ret_t; R6 over t..t+5; R12 (year 1) over t..t+11; year 2 over t+12..t+23; year 3 over t+24..t+35. Any missing monthly return inside a window — including all months after a stock's last CRSP observation (delisting) — is replaced by that month's CRSP EWRETD index return. The cross-section at t still requires a nonmissing ret_t.
**Rationale:** L116: "current returns (at time 0)" are the dependent variable, and "If return information is missing in CRSP for a given month, we construct the holding period return by replacing the missing stock return with the return of the CRSP equally weighted market portfolio with dividends reinvested (EWRETD)... Our holding period return represents the return from holding the stock until delisting and investing the remaining value in a CRSP equally weighted index." The post-delisting EWRETD continuation is stated explicitly.
**Impact:** All 6-month and multi-year dependent returns in Tables III and VI.

## Assumption 8: Pre-1970 book equity (DFF 2000) unavailable — BM rows are SKIP

**Decision:** For months before July 1970, set bm = 0 and bm_dum = 0; the BM-dependent cells of Tables V and VI are reported as SKIP (data limitation), not failures. All CRSP-only cells (ISSUE, DT-ISSUE, ME, MOM, and the BM-free specifications) are fully replicated.
**Rationale:** L2445: "We obtain data on the book value of equity from Kenneth French for our out-of-sample study, since COMPUSTAT coverage is limited or nonexistent during this time period. These data are identical to those used by Davis, Fama, and French (2000)." No DFF-style book-equity table exists in the ClickHouse catalog (verified: no table matching dff/book/beme/davis in any database; comp_202601.funda coverage begins ~1950s and is sparse pre-1970, which is exactly why the authors used DFF). Tables V/VI notes in tables_to_replicate.json document this conditional SKIP.
**Impact:** oos_bm_* cells (T5), BM rows/coefficients of Table VI (T6); none of T1/T3.

## Assumption 9: Tables II and IV are out of scope (SDC Platinum)

**Decision:** Do not replicate Table II (ISSUE regressed on SEO/repurchase/merger dummies) or Table IV (Table III with SDC event windows removed). Documented as a data limitation, not a methodology gap.
**Rationale:** Both tables require Thomson SDC Platinum event data (L341: 14,556 SEOs, 15,800 repurchase announcements, 36,683 merger announcements from SDC; L2168: removal of 3 years post-SEO/repurchase and 1 year post-merger observations). No SDC SEO/repurchase-announcement tables exist in ClickHouse (catalog check: only tr_sdc_ma merger tables, no repurchase announcements, and merger-consideration detail insufficient to reconstruct the paper's SMA/UMA dummies). The headline results (Table III) and the out-of-sample evidence (Tables V/VI) — the paper's three central findings — do not depend on SDC.
**Impact:** Tables II, IV not replicated; all four committed tables unaffected.

## Assumption 10: cfacshr convention — AdjustedShares = shrout × cfacshr

**Decision:** Paper equation (L63) AdjustedShares_t = SharesOutstanding_t / TotalFactor_t is implemented as adj_shares = shrout × cfacshr in ClickHouse.
**Rationale:** Verified empirically (see logs/log1.md, pre-spec sanity): across Apple's three 2:1 splits, shrout doubles while cfacshr halves, so shrout × cfacshr is split-invariant and shrout / cfacshr is not. ClickHouse cfacshr is the reciprocal of the paper's cumulative Total Factor (eq. 1). references/CRSP.md L707 states the same ("multiply shrout by cfacshr"). Since ISSUE is a log difference, the absolute normalization of the factor cancels.
**Impact:** ISSUE, DT-ISSUE and every downstream cell.

## Assumption 11: CCM link filter — WRDS-recommended set

**Decision:** Join Compustat to CRSP with linktype IN ('LC','LU'), linkprim IN ('P','C'), usedflag = 1, point-in-time on link date ranges.
**Rationale:** Paper is silent on the CRSP-Compustat link construction ("we use the annual COMPUSTAT book value of common equity (data60)", L108). The WRDS-recommended link set (per references/CRSP.md §Compustat-CRSP link) is the standard convention and the most defensible default.
**Impact:** BM cells in Tables I and III.

## Assumption 12: Shares-error correction — sequential pass on raw shrout

**Decision:** Implement the L98 rule as a sequential pass on raw shrout (>20% jump, ≥95% reversed within 3 months → set to the prior level), iterating to convergence; ISSUE/DT-ISSUE are then computed from the corrected split-adjusted series.
**Rationale:** Calibrated against the paper's reported count (2,189 corrections): sequential-iterative detection on raw shrout at the literal 0.95 reversal threshold yields 2,172 corrections (−0.8%); single-pass variants yield only 761–1,136. The paper's footnote-1 example (permno 85523) is a reporting error in raw shares, and the paper applies the rule to "shares outstanding" (L98). The paper states inference is unaffected by the correction either way.
**Impact:** 2,172 observations corrected (0.07%); negligible by the paper's own statement, implemented for fidelity.

## Assumption 13: Compustat funda filter values — consol='C', popsrc='D'

**Decision:** Filter comp_202601.funda with indfmt='INDL', datafmt='STD', consol='C', popsrc='D'.
**Rationale:** The WRDS-standard "STD/STD" labels in documentation map to the values actually stored in this Compustat vintage: consol ∈ {C, P, R, D} (C = consolidated, the 'STD' consolidation level) and popsrc = 'D' (actuals, the 'STD' population source). Verified empirically: consol='STD'/popsrc='STD' return zero rows; consol='C'/popsrc='D' give the expected coverage (77% bm_dum=1 in the 1970s rising to 92% in the 2000s among univ_common). Paper is silent on the exact filter values ("we use the annual COMPUSTAT book value of common equity (data60)", L108).
**Impact:** BM cells in Tables I and III.

## Assumption 14: Universe selected — all CRSP securities (univ_all), no share-code filter

**Decision:** Use univ_all (all CRSP securities with nonmissing ret at t and ≥6 months in CRSP) for every table; do not restrict to shrcd ∈ {10, 11}.
**Rationale:** Decided from iteration-1 count reconciliation: univ_all reproduces the paper's ISSUE-available base (2,324,025 vs 2,312,597, +0.5%), regression sample (2,182,151 vs 2,155,945, +1.2%), and issuance sign proportions (56.5/24.5/19.0 vs 56.6/24.2/19.2); univ_common undershoots every count by ~13%. The paper's text supports this: "Our primary sample consists of all firm observations that are in the CRSP database" (L51), with no share-code or exchange restriction stated.
**Impact:** Every cell of every table.

---

## Assumption 15 (Stage-7 analysis): DT-Dum polarity — panel stores L94 definition; paper's Table III implies the complement

**Decision:** The panel's `dt_dum` follows paper L94 verbatim (`dt_dum=1` for firms WITH a 5-year share history; `=0` for <5-yr listings). I run the Table III regressions with `dt_dum` **as given** (default `DT_DUM_FLIP=False`), which yields a **positive** DT-Dum slope (+0.50/+0.33/+0.35 in R6/R7/R8) — the OPPOSITE sign of the paper's printed **negative** values (−0.41/−0.31/−0.32) → 3 per-cell FAILs. A one-line switch `DT_DUM_FLIP=True` in `src/analyze_tables.py` adopts the complement dummy and reconciles the paper (see diagnostic in `results/table_3.md`).
**Rationale:** The paper is internally inconsistent on this dummy. L94 ("set the D-T dummy = 0 [for <5-yr firms]; otherwise = 1") matches our panel. But three independent lines of evidence show the paper's *reported numbers* use the complement (`dt_dum=1` = NO 5-year history): (1) the Table III caption parenthetical "DT-Dum is set to one if shares outstanding exists at t−65 (hence DT-ISSUE is zero)" only parses if DT-Dum=1 ⇔ DT-ISSUE=0 ⇔ no history; (2) flipping reproduces both the negative DT-Dum slopes AND the R6/R7 intercepts (as-built 1.02/1.19 → flipped 1.52/1.52 vs paper 1.48/1.48; verified by re-running); (3) economics — young/recently-listed firms (no history) underperform (new-issues puzzle), so a "no-history" dummy should load negative, exactly as the paper prints. A 0/1 dummy flip changes only the intercept (by +β_dt_dum) and its own coefficient's sign; all other coefficients (including ISSUE, DT-ISSUE) are identical under both polarities.
**Why default = as-built (not flipped):** polarity is a variable-definition (methodology) choice owned by the Replicator; L94 is explicit and the task passed `dt_dum` as-is. I implement the spec faithfully and surface the reconciliation with evidence rather than silently flipping. Set `DT_DUM_FLIP=True` to match the paper's printed Table III; the per-cell FAILs then become Tier 1.
**Impact:** Only the 3 DT-Dum coefficient cells (pA_r6/r7/r8_dt_dum) and their t-stats, plus the R6/R7/R8 intercepts (the flip also nudges the intercepts to match). All other T3 cells are unaffected.

## Assumption 16 (Stage-7 analysis): Pontiff (1996) overlap t-stat — AR-error (GLSAR) form, NOT AR-on-levels

**Decision:** Implement the Pontiff overlap t-stat as a constant-only regression of the monthly slope series b_t with AR(n=k−1) ERRORS (statsmodels `GLSAR(...).iterative_fit`), and report `t = mean(b) / SE(intercept)`. For n=0 (k=1, Panel A) this reduces to the plain FM t-stat (GLSAR with no AR = OLS).
**Rationale:** Paper L134: "a regression using each month's slope estimate where the **residuals** of the process follow an n-th order autoregressive process ... the standard error of the intercept from this estimation is used as the overlap-consistent standard error of our average slope coefficient." This is an AR-error model (intercept = the long-run mean), NOT an OLS of b_t on its own lags (an AR-on-levels model, where the intercept = mean·(1−Σρ)). The task text paraphrased L134 as "fit OLS of b_t on a constant and n lags; use the intercept SE" — but under that AR-on-levels model the literal formula `mean(b)/SE(intercept)` inflates |t| by ≈ 1/(1−Σρ) (here Σρ≈0.76 → ~4×: Panel B R5 ISSUE = −20.9 vs the paper's −7.26), because the AR-on-levels intercept's SE estimates SE of mean·(1−Σρ), not SE of the mean. The AR-error (GLSAR) form reproduces the paper (Panel B R5 ISSUE = −7.68 vs −7.26; Panel B R3 MOM = 4.99 vs 5.53; all Panel B t-stats land within tolerance). Panel A (n=0) is identical under both readings.
**Spec concern (flagged):** the task's literal AR-on-levels formula does not reproduce the paper's multi-month t-stats; the paper's own wording ("residuals follow an AR process") and its printed numbers require the AR-error form. Implemented the AR-error form to match the paper; the Newey-West(k−1) t-stat is also reported for reference (e.g. NW(5) R5 ISSUE = −8.98).
**Impact:** All multi-month (Panel B) t-stats; Panel A unchanged.

## Assumption 17 (Stage-7 analysis): Figure 1 — guard numerically degenerate cross-sections

**Decision:** In `results/issue_rolling_slope.png` (trailing-12m univariate FM slope of r1×100 on ISSUE over univ_all, 1933–2003), skip a month (record NaN) when the winsorized ISSUE cross-sectional std < 0.01 (`FIG_ISSUE_STD_MIN`) or n<30. Winsorization, univ_all, and the full period are otherwise unchanged.
**Rationale:** Pre-1950 issuance is near-universally zero; in some months (e.g. 1942-05) the 1%/99% winsorization collapses the cross-sectional spread to ~0 (winz std 0.0001), so `lstsq` divides by ~0 and returns a degenerate slope (−11648), which dominates the trailing-12m average and the ±2 SE band and hides the post-1950 negative tendency the figure is meant to show. The guard removes ~10 such months (small honest gaps) and yields a bounded figure matching the paper's described Figure 1: large positive variability around WWII (rolling mean up to +21) and a negative-tendency line hugging below zero post-1950 (mean −2.06, 86% of months negative). The figure is descriptive; the regression tables (Table III) are unaffected by this guard.
**Impact:** Figure 1 only.

## Assumption 18 (Stage-7 analysis): Regression month count 408 vs paper's printed 396

**Decision:** Run the Fama-MacBeth over every calendar month Jan 1970–Dec 2003 = **408** months (all have valid cross-sections in our panel).
**Rationale:** The paper prints "396 months from January 1970 to December 2003" (L1074), but Jan 1970–Dec 2003 inclusive is 408 calendar months; 396 = 33 yr is an internal inconsistency in the paper (it would correspond to Jan 1971–Dec 2003 or the exclusion of one year that the paper does not name). Our panel supports valid regressions in all 408 months, so we use 408 (the `n_months` per-cell metric is therefore Tier 2: 408 vs 396, +3% > the 1% tolerance, same sign). Time-series means of the coefficients are essentially unaffected by the 12-month difference (the per-cell coefficient/t-stat cells all match within tolerance regardless).
**Impact:** The `n_months` per-cell metric only; no coefficient cell.

---

## Assumption 19 (Stage-7 analysis): DT-Dum polarity RESOLVED — `DT_DUM_FLIP=True` ratified

**Decision (Replicator-ratified):** Adopt the COMPLEMENT DT-Dum (`dt_dum=1` = NO 5-year share history) as the HEADLINE for Tables III and VI (`DT_DUM_FLIP=True`, now the default in `src/analyze_tables.py`). This resolves A15: the 3 DT-Dum per-cell FAILs (pA_r6/r7/r8_dt_dum) become **Tier 1**, and the R6/R7 intercepts move 1.02/1.19 → **1.52/1.52** (paper 1.48/1.48, Tier 1). The as-built (L94) numbers are retained in the `table_3.md` diagnostic for transparency; only the intercept and DT-Dum coefficient change under the flip (every other coefficient is identical under both polarities).
**Rationale:** The three independent lines of evidence in A15 (caption parsing, numeric reconciliation of slopes+intercepts, new-issues economics) all favor the complement; the Replicator ratified it.
**Impact:** T3 pA_r6/r7/r8_dt_dum (+ their t-stats) and the R6/R7/R8 intercepts flip to the paper-consistent values; T3 FAIL count 3 → 0. T6 R6/R7 DT-Dum cells use the same flipped polarity (both ≈0 and insignificant pre-1970 regardless).

## Assumption 20 (Stage-7 analysis): OOS (Tables V & VI) sample, BM = SKIP, and the degenerate-ISSUE guard

**Decision:**
- **Table V** (descriptives, Sep 1932–Dec 1969): base = `univ_all` AND `issue_contemp` nonmissing; regressors (ISSUE, DT-ISSUE, ME, MOM) use the SAME 1%/99% per-month winsorized headline convention as Table I (A5), `R_{-11,0}` raw (dependent return, L132); `dt_issue_contemp` dummy-filled to 0 for <5-yr history; ME uses `me_monthly` (Table I convention — `me_june` is marginally closer to the paper's 10.28 mean but both are Tier 1). **BM cells are SKIP** (A8).
- **Table VI Panel A** (FM, 1-month, Sep 1932–Dec 1969): dependent `ret×100`, plain FM t-stats (k=1 ⇒ n=0, A4/A16). BM omitted from ALL eight specs (A8). PRIMARY (BM-free in the paper, fully comparable, in the Tier tally): R2, R3, R5, R6, R7. SECONDARY (BM-inclusive in the paper): R1/R4/R8 estimated without bm/bm_dum and labeled **pattern-only** — their non-BM cells are shown for pattern comparison but EXCLUDED from the Tier tally; R1 (const+BM+BM Dum) reduces to a constant-only row ⇒ SKIP.
- **Degenerate-ISSUE guard (A17 extension):** pre-1950, issuance is near-universally zero and in some months the 1%/99% winsorization collapses the ISSUE cross-sectional spread to ~0, so the FM slope divides by ~0 (one month reaches −11648; unguarded OOS R5 ISSUE = −29). ISSUE-containing specs (R5/R7/R8) drop months whose winsorized ISSUE std < `OOS_GUARD_ISSUE_STD = 0.01` (same threshold as the A17 figure guard): 448 → 438 months. This is a numerical safeguard, NOT a sample/universe change.
**Rationale:** The paper's OOS book equity is DFF (2000) (L2445), absent from ClickHouse ⇒ BM is SKIP and the BM-inclusive rows are not directly comparable. The paper's single OOS count (373,590 over 444 months) reflects DFF availability; our CRSP-only cross-section is larger (R8 ≈ 464,718; ~1,068 firms/mo vs the paper's ~841/mo) — documented, not forced. The degenerate guard is required for a finite, meaningful ISSUE slope and mirrors the ratified A17 figure guard.
**Impact:** All T5 cells (BM SKIP); all T6 cells; the `oos_n_months` metric is 438 (guarded R8) vs paper 444 (Tier 2, 1.4%).

## Assumption 21 (Stage-7 analysis): OOS ISSUE-slope sign deviation (documented, not forced)

**Decision:** Report the OOS 1-month ISSUE slopes AS ESTIMATED (guarded): R5 = −1.27 (t=−1.73), R7 = −1.56 (t=−2.54), R8 = −1.30 (t=−2.33) — weakly NEGATIVE, whereas the paper prints weakly POSITIVE and insignificant (0.52/0.27/0.84, all |t|<1). These are genuine per-cell FAILs on sign (R5/R7 issue; R7 issue_t) in the PRIMARY tally. No convention is changed to force the sign.
**Rationale:** The sign is robust to the guard threshold (negative for every threshold 0.005–0.05; monthly-slope median −1.43). The paper's central pre-1970 claim — ISSUE has essentially NO predictive power (vs −2.23, t=−7.08 post-1970) — is reproduced in MAGNITUDE (all |β| ≤ ~1.6) and in R5's insignificance (|t|=1.73<2), but not in sign, and our R7/R8 ISSUE are significant. The likely driver is the larger CRSP-only sample: the ~27% of extra firm-months the paper's DFF book-equity requirement excludes are small-cap firms with sparse issuance. The other two narrative claims verify cleanly: (ii) ME significantly negative in all specs (R2/R4/R8, |t|≥3.35); (iii) MOM positive in all and insignificant in R3/R4 (borderline-significant in R8, t=2.18).
**Impact:** T6 PRIMARY FAIL count = 3 (oos_pA_r5_issue, oos_pA_r7_issue, oos_pA_r7_issue_t); the ISSUE pattern claim (i) is reported as not-confirmed with the sample-composition explanation.

## Assumption 22 (Stage-7 analysis): Horizon-stability extension — Table III Panels C/D/E (1/2/3-year holding periods)

**Diagnosis:** Audit 1 [M1] — the paper's headline corollary "Our results remain strong for holding periods ranging from one month to 3 years" (content.md L31) and the horse-race / DT-ISSUE statements (L2128) were verified only at the 1-month (Panel A) and 6-month (Panel B) horizons. Panels C (1-year), D (2nd-year) and E (3rd-year) were not computed even though their targets are fully legible: Panel C at content.md L1501–1695, Panel D at L1698–1892, Panel E rows 1 at L1895–1935 and rows 2–8 on the page-14 continuation at L1952–2122. The earlier "OCR of those pages is ambiguous" justification (REPORT §6.5, T3 notes) was not supported — every one of the 24 rows × ≤9 cells is legible. The machinery (`run_fama_macbeth` with AR order n=k−1) and the verified return columns (`r12`, `r24_y2`, `r36_y3`, EWRETD-imputed for the year-2/year-3 windows per A7) already existed.

**Next fix:** Extended `src/analyze_tables.py` (additively — no existing computation path modified, the four existing table md files are byte-stable) to run the same eight horse-race SPECS on `r12×100` (k=12 → AR(11)), `r24_y2×100` (k=24 → AR(23)), `r36_y3×100` (k=36 → AR(35)) over the 408 in-sample months (Jan 1970–Dec 2003) with `DT_DUM_FLIP=True`, Pontiff GLSAR AR(k−1) t-stats and a Newey-West(k−1) cross-check. Added a `T3cde` contract entry (198 metrics = every legible coef/t/R² cell; ±40% coef/t, ±25% R², same schema/rules as T3). Wrote `results/table_3_cde.md` (ours-vs-paper grids, NW appendix, per-cell Tier evaluation) and verified the three paper claims explicitly. No convention was changed; the ratified A1–A21 stand.

**Before metric:** Long-horizon panels computed: 0 of 3 (C/D/E). Horizon-stability claim verified only at k=1, 6. Combined four-table tally 163 Tier 1 / 21 Tier 2 / 3 FAIL / 14 SKIP (201 cells).

**After metric:** All 3 panels computed. **T3cde: 166 Tier 1 / 29 Tier 2 / 3 FAIL / 0 SKIP (198 cells; 83.8% Tier 1).** ISSUE reproduces the paper closely at every horizon — C-R5 −25.68 (t −8.07) vs paper −27.32 (−7.51); D-R5 −18.88 (−4.68) vs −20.03 (−6.20); E-R5 −14.78 (−3.03) vs −14.18 (−3.17) (coefs within 4–8%, all Tier 1). **Combined five-table tally: 329 Tier 1 / 50 Tier 2 / 6 FAIL / 14 SKIP (399 cells).** Paper-claim verification: (i) ISSUE negative at all three horizons — **PASS**; (ii) |t_ISSUE| > |t_BM|,|t_ME|,|t_MOM| univariate at each horizon — **PASS** for our estimates at all three horizons (C 8.07>4.32/2.11/3.44; D 4.68>4.49/1.66/1.78; E 3.03>2.24/1.13/2.31), with an anomaly noted: the paper's OWN printed 3-year t-stats violate the claim (ISSUE |t|=3.17 < BM |t|=3.87, Panel E R1/R5); (iii) DT-ISSUE significant in the 1-year FULL (R8) but insignificant in the 2- and 3-year FULL (R8) — **PARTIAL**: confirmed at 1-year (ours t=−3.17, sig) and 3-year (ours t=−1.69, insig), but at 2-year OUR DT-ISSUE is borderline-significant (t=−2.68) where the paper prints insignificant (−1.86); both sit near |t|=2 (overlap-t-stat sensitivity) and the coefficient matches (−3.02 vs −2.68, Tier 1).

**Status:** RESOLVED — [M1] closed. The only sign deviations are the 3 Panel E DT-Dum *coefficient* cells (pE_r6/r7/r8_dt_dum: ours negative under the ratified flipped polarity, paper positive +1.98/+2.21/+3.12). This is the mirror image of the A15 finding and a paper-side DT-Dum polarity inconsistency at the 3-year horizon (Panels A–D require the flipped no-history sign; Panel E's printed DT-Dum sign matches the as-built polarity). It is documented, not forced: it touches no ratified convention and leaves the polarity-invariant ISSUE/DT-ISSUE coefficients and all other cells unaffected. REPORT.md was not edited this iteration (write scope for this run is src/ + results/ + preparations/{tables_to_replicate.json, assumptions.md}); the §6.5 "OCR ambiguous" statement and §6.3 parenthetical ([m2]/[m3]) should be corrected by the Replicator using the numbers above.
