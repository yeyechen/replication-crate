# Assumptions Registry — Do Industries Explain Momentum? (Moskowitz & Grinblatt 1999)

Paper-silent decisions made by the replicator. Paper-derived rules live in
`preparations/preprocessing_rules.json`. Updated every inner-loop iteration.

---

## Assumption 1: Share-code filter for the universe

**Decision:** Restrict the universe to CRSP share codes 10 and 11 (ordinary
common shares) with exchange codes 1/2/3 (NYSE/AMEX/NASDAQ), applied
point-in-time via `msenames`.
**Rationale:** Paper §I says only "maximize coverage of NYSE, AMEX, and
Nasdaq stocks" (L74) without a share-code filter. shrcd 10/11 is the
standard operationalization in `rep/PAPER_CONVENTIONS.md` and is what the
CRSP-based momentum literature (Jegadeesh-Titman 1993, which this paper
follows — L320) uses. The paper's total average stock count across the 20
industries is 4,609.69 (Table I, L162); our universe averages ~4,700 over
1963-1995, consistent.
**Impact:** Every cell in every table.

## Assumption 2: Point-in-time industry assignment

**Decision:** Industry membership comes from the CRSP `msenames` SIC time
series (paper: "The SIC codes are obtained from CRSP, which reports the
time-series of industry classification codes", L80), matched to month m by
`namedt <= m <= nameendt`. 2-digit SIC = floor(siccd/100), mapped to the 20
Table I groups; the ~0.1% of universe rows with missing/0/9999 SIC go to
industry 20 ("other").
**Rationale:** Paper explicitly uses CRSP's time-varying SIC codes. Interval
join is the documented correct pattern (references/CRSP.md §Gotchas).
**Impact:** All industry-level cells (Tables I, II-B/C, III, IV-free, VI ind_ vars).

## Assumption 3: Book equity definition

**Decision:** BE = ceq + txdb − pstkrv (when ceq > 0); fallback BE = seq;
fallback BE = at − dlc − dltt − pstkrv; keep observations only when BE > 0
and at > 0.
**Rationale:** Paper §V (L1454) defines BE/ME as "log of book value plus
deferred taxes and investment tax credits divided by market capitalization"
— i.e. common equity + deferred taxes − preferred. The fallback cascade and
positivity screen are the standard FF convention; the paper is silent on
fallbacks. Negative-BE firms are dropped from BE/ME sorts (they cannot be
logged for the FM BE/ME regressor).
**Impact:** DT adjustment (Tables I abnormal, II DGTW/SB columns), DGTW
adjustment, Table VI BE/ME regressor and dependent variable.

## Assumption 4: Compustat vintage filter codes

**Decision:** funda filter `indfmt='INDL' AND consol='C' AND popsrc='D'`
(prefer `datafmt='STD'`, fall back to 'SUMM_STD' when STD is absent, dedup
by gvkey/fyear keeping STD).
**Rationale:** This ClickHouse vintage (comp_202601) uses consolidation
code 'C' and population source 'D' rather than the classic 'CFS'/'STD'
(verified empirically: IBM gvkey 005086 carries consol='C', popsrc='D';
references/COMPUSTAT.md §486-495 documents the same).
**Impact:** All Compustat-dependent cells.

## Assumption 5: Book-equity availability lag

**Decision:** Fiscal-year-Y book equity is usable from July Y+1 through
June Y+2 (fiscal year-end + 6-month reporting lag).
**Rationale:** Paper is silent on BE timing. The 6-month lag is the
standard FF (1992) convention and avoids look-ahead. The paper's DT/DGTW
adjustment period starts January 1973, which implies FY1971 BE for the
first sorts (FY1972 data becomes available only mid-1973).
**Impact:** All DT/DGTW-adjusted cells (period Jan 1973–Jul 1995).

## Assumption 6: Market equity source

**Decision:** ME = |prc| × shrout × 1000 (dollars) from CRSP msf, measured
at month t−1 for sorts and value weights.
**Rationale:** Paper says "market capitalization" without a source. CRSP ME
is the convention in `rep/PAPER_CONVENTIONS.md`; Compustat prcc_f × csho is
fiscal year-end and stale for monthly sorts.
**Impact:** Value weights everywhere, size sorts, ln(Size) regressor.

## Assumption 7: Characteristic-sort breakpoints

**Decision:** DT 5×5 (size × BE/ME) sorts use all-universe quintile
breakpoints; DGTW 5×5×5 (size × BE/ME × prior 12-mo return) sorts use
NYSE-only (exchcd = 1) breakpoints.
**Rationale:** Footnote 17 (L592) explicitly states NYSE breakpoints for
DGTW. The paper is silent on the DT 5×5 breakpoints; all-stock quintiles
are the natural reading of footnote 5 (L111), which describes a plain
5×5 sort with no breakpoint restriction.
**Impact:** All SB- and DGTW-adjusted cells.

## Assumption 8: Weight dynamics within holding periods

**Decision:** Individual stock momentum (Tables II-A, II-C): membership and
value weights fixed at formation, held H months (Jegadeesh-Titman 1993
convention the paper adopts, L320-322). Industry portfolios (Tables I, II-B,
III): VW member weights rebalanced every month (industries "are formed
monthly", L74/L127) while the selection of top-3/bottom-3 industries is held
constant for H months.
**Rationale:** Footnote 11 (L352) mentions monthly rebalancing only for the
unreported equal-weighted robustness version, implying the reported VW
version holds formation weights for stocks. Table I/§I explicitly form
industry portfolios every month.
**Impact:** Tables II and III spread levels.

## Assumption 9: t-statistic convention and sample length

**Decision:** Time-series t = mean(monthly series) / (std / sqrt(T)), where
T is the number of monthly strategy observations in our data (≈385 for
July 1963–July 1995 raw; 271 for January 1973–July 1995 adjusted), applied
to the overlapping-portfolio averaged monthly series (Jegadeesh-Titman 1993
technique, L324).
**Rationale:** Paper reports T = 383 (L366) vs our ~385 months (inclusive
July 1963–July 1995 = 385); the 2-month difference (likely paper-specific
data endpoints) shifts t-stats by sqrt(385/383) ≈ 1.003 — negligible. The
t-stat convention is the standard one for overlapping momentum returns.
**Impact:** All t-stat cells.

## Assumption 10: Delisting returns

**Decision:** Use msf `ret` as reported by CRSP (includes delisting returns
where CRSP assigns them); no Shumway/BMP substitution.
**Rationale:** Paper is silent on delisting treatment (logged as
`delisting_paper_silent` in preprocessing_rules.json). Modern CRSP vintages
already incorporate delisting returns into `ret` where available.
**Impact:** Small; affects loser-portfolio returns near delisting events.

## Assumption 11: Beta estimation details

**Decision:** Beta = slope of 36-month rolling OLS of stock excess returns
(ret − rf) on a constant and CRSP VW index excess returns (msi vwretd − rf),
requiring ≥ 24 valid months; stocks ranked on pre-ranking beta into 100
groups and assigned the equal-weighted group-average beta.
**Rationale:** Footnote 25 (L1466) specifies the 36-month window, the CRSP
VW index, the 100 pre-ranking groups, and EW group averaging; it is silent
on the minimum-observation cutoff — 24/36 is the standard FF convention.
**Impact:** Table VI beta column.

## Assumption 12: Fama-MacBeth regression weighting

**Decision:** Monthly cross-sectional regressions are unweighted OLS;
coefficients time-series averaged with FM t-stats (mean / (std/sqrt(271))).
**Rationale:** Paper says "Fama and MacBeth (1973) cross-sectional
regressions ... on the universe of securities" (L1438, L1496) with no
weighting scheme; unweighted OLS is the FM default.
**Impact:** All Table VI cells.

## Assumption 13: Random-industry return replacement

**Decision:** Each month, rank all universe stocks ascending by past 6-month
return; replace stock j's return with (r_{j+1,t} + r_{j−1,t})/2 (endpoints:
j=1 → stock 2's return; j=N → stock N−1's return). Random-industry VW
returns use the true industry membership and weights with replaced returns;
the SB-minus-random-industry column subtracts the SB-adjusted random
industry return (VW of replaced r^sb within industry).
**Rationale:** Footnote 18 (L672) specifies the exact replacement rule and
endpoint handling. The SB-adjusted random-industry variant follows by
analogy with the SB-adjusted true-industry variant (L639).
**Impact:** Table II Panel A column 6, Panel B column 3.

## Assumption 14: FM past-return and industry-return variables

**Decision:** ret_{-L:-H} = cumulative product of (1+ret) over months t−L
to t−H minus 1; ret_{-6:+6} = equal-weighted average of the six 6-month
returns ret_{-11:-6} … ret_{-6:-1} (and analogously 12); ind_{-L:-H} uses
the stock's contemporaneous (month-t) industry membership; the skip-month
Panel D variables shift every window by one month (ret_{-L-1:-H-1}).
**Rationale:** §V defines ret_{-6:+6} explicitly (L1456) and ind_{-L:-H} as
"the industry return over the (L,H) time period to which each stock
belongs" (L1476) — contemporaneous membership is the natural reading; Panel
D's shift is defined at L2014.
**Impact:** All Table VI momentum-coefficient cells.

## Assumption 15: Risk-free rate

**Decision:** rf from `ff.four_factor_monthly` (monthly 3-month T-bill,
decimal), covering 1926-07 onward.
**Rationale:** Paper uses "the three-month Treasury bill rate" (L127) with
no source; the FF monthly rf series is the standard source.
**Impact:** All excess-return cells (Table I) and beta estimation.

---

## Assumption 16: Financial industry count gap is vintage drift, not a filter

**Decision:** Keep shrcd IN (10,11) (A1). Do not add shrcd 12 (REITs) or
other share codes to close the Financial industry gap (our 719.9 vs paper
891.56 average stocks).
**Rationale:** Empirical test (SQL, 1963-07..1995-07): adding shrcd 12
raises Financial by only +7.5 stocks/month (to 741.4) and the total
universe to 4,645 vs paper 4,610. SIC 60-69 at 1990-06 is 96% shrcd 10/11.
The ~170-stock gap is consistent with CRSP vintage drift: the paper's
~1997 file contained small NASDAQ banks and S&Ls later removed or
reclassified in our 2026 vintage. All five universe-date benchmarks
reproduce exactly and all 20 industry VW excess returns match the paper
within 14 bp, confirming the construction is otherwise correct. Financial
count/cap-share cells will be evaluated at Tier 2 with this justification.
**Impact:** Table I Financial row (count, cap share); negligible effect on
industry momentum spreads (value-weighted, dominated by cap, not count).

## Assumption 17: Table VI FM — plain iid t-stats, no winsorization; r_sb outlier sensitivity

**Decision:** Table VI Fama-MacBeth uses plain iid FM t-stats
(mean/(std/sqrt(271)), ddof=1) with NO Newey-West and NO winsorization of the
dependent variable or the regressors; the monthly OLS loop is implemented
directly (numpy lstsq) so no primitive default can inject HAC/winsorization.
Per-month cross-sections require >= 30 obs (all 271 months fit; none dropped).
**Rationale:** Task spec (iter 7) mandates plain FM. The `utils.fama_macbeth`
primitive applies 1% winsorization + 2-lag NW by default, so it was bypassed.
**Data observation (flagged, not acted on):** the frozen panel's r_sb has fat
tails (max +13.96; 2,009 obs with |r_sb|>1 over 1973-01..1995-07). Under plain
OLS the `ln_size` coefficient is significantly NEGATIVE (≈ −0.0006..−0.0010,
|t| 3-7) where the paper reports ≈ +0.0001 (n.s.); winsorizing r_sb 1/99 flips
it to ≈ +0.0004, i.e. the sign is outlier-driven. All 71 FAIL cells in
cells_table_6.json are control variables (32 ln_size_t, 15 beta_t, 9 be_me,
9 be_me_t, 6 ln_size); ZERO momentum cells (ret/ind/ret_1_1/ret_36_13/ind_1_1/
ind_36_13) FAIL — the paper's central industry-momentum result reproduces.
**Impact:** Table VI ln_size/beta_t/be_me cells (Tier2/FAIL); momentum cells
unaffected. r_sb left as-is (data/ frozen per spec).

## Assumption 18: Cross-sectional 1/99 winsorization in the Table VI FM regressions (iteration 8)

**Decision:** In each month's cross-section, BEFORE fitting the OLS, winsorize
the dependent variable (r_sb) AND every regressor column at the 1st/99th
percentiles computed within that month (clip to the percentiles, on exactly the
rows entering that regression). Everything else unchanged: plain iid FM t-stats
(A17), no Newey-West, >= 30 obs/month, T = 271, same 32 specs/windows.
Winsorization does not drop rows (avg obs/month unchanged; ~68 rows/month —
~2.0% of the cross-section — hit the caps, confirming the 1/99 cut engaged).
**Rationale:** The paper is silent on winsorization (logged as
`winsorize_paper_silent` in preprocessing_rules.json). The frozen panel's r_sb
has fat tails: 2,009 of 1.17M adjusted-window observations have |r_sb| > 1
(max +13.96) — microcap monthly return spikes the characteristic benchmark does
not absorb. Under plain OLS these outliers drive the ln_size slope significantly
negative (−0.0006..−0.0010, |t| 3-7) versus the paper's near-zero insignificant
+0.0001 (t 0.4-0.9); the 1/99 winsorize flips ln_size to ≈ +0.0004 (the paper's
sign) and clears all 38 ln_size/ln_size_t FAILs; ind coefficients move closer to
the paper (C (6,1) s1 ind 0.0462 → 0.0395 vs paper 0.0366). Per-cross-section
1/99 winsorization of FM variables is a standard convention in the
cross-sectional-return literature.
**Residual (not outlier-driven):** ret_1_1 (short-term reversal) is ~1.7× the
paper's magnitude (ours −0.076..−0.093, mean −0.082; paper −0.044..−0.054) and
does NOT move toward the paper under winsorization — a systematic vintage
difference (all 20 ret_1_1 cells Tier 2, same sign). Remaining 43 Table VI FAILs
are all near-zero control cells: 25 beta_t (both sides ≈ 0) + 18 be_me(±t).
ZERO momentum cells FAIL. Tally: Tier1 193→196, Tier2 152→177, FAIL 71→43.
**Impact:** Table VI control-variable cells (beta, ln_size, be_me) and
short-term-reversal cells; momentum-slope cells largely unaffected.

---

## Iteration entry — outer iteration 2 (2026-07-22), audit issue [M4]: long/short leg decomposition

**Diagnosis:** Audit 1 [M4] — the abstract-level corollary (inputs/content.md
L35: industry momentum predominantly long-driven; individual momentum largely
driven by selling past losers; §IV.B L1159: the (1,1) industry strategy
equally driven by both sides; §IV.A L1121: Wi−Mid 0.36%/mo vs Mid−Lo 0.07%/mo)
was computed in the engines (table_3.md Wi/Lo columns) but never decomposed
against the benchmark or reported.
**Next fix:** add src/legs_long_short.py — reuse the frozen engines from
src/tables_1_2_3.py (build_global_cohorts, individual_spread_series,
industry_selections, industry_cohort_returns/industry_strat_series, mean_t)
on data/panel.parquet + data/bin_rets.parquet only (no pipeline rerun);
compute W(t)/L(t) for the individual (6,6) via a leg-returning twin of the
spread engine (joint both-legs-valid mask, so W−L reproduces the spread
engine exactly), Wi(t)/Lo(t) for industry (6,6) and (1,1); benchmarks r̄ =
monthly EW mean of universe stock returns (L246, footnote 14; corr vs panel
ew_mkt = 0.999) and r̄_ind = monthly EW mean of the 20 industry VW returns;
write results/legs_long_short.md + results/cells_legs.json citing
L35/L1121/L1159. M1/M2/M3 untouched.
**Before metric:** corollary not computed.
**After metric (1963-07..1995-07, T=385):** r̄ = 0.012891/mo, r̄_ind =
0.010161/mo. Individual (6,6): W = 0.013067, L = 0.008931; long contrib
+0.000176 (t=0.11), short contrib +0.003959 (t=2.64) → loser-driven
(matches paper L35; agrees with the audit's independent +0.0040/+0.0002).
Industry (6,6): Wi = 0.012423, Lo = 0.008451; long contrib +0.002261
(t=2.34), short contrib +0.001711 (t=1.89) → long-driven (matches paper
L35); Wi−Mid 0.001473 / Mid−Lo 0.002499 vs paper 0.0036/0.0007 (both Tier2
same-sign; in this vintage Mid−Lo > Wi−Mid, reported honestly as a
vintage-magnitude finding, same family as the Table III Wi/Lo Tier-2 cells).
Industry (1,1): Wi = 0.015754, Lo = 0.003529; long contrib +0.005592
(t=5.09), short contrib +0.006632 (t=6.15), |long−short| = 0.0010 ≤ 0.002
→ balanced (matches paper L1159). Spread integrity: individual W−L =
0.004135/2.311 and industry Wi−Lo = 0.003972/2.359 both reproduced from the
legs (leg W−L series == individual_spread_series output to 2.8e-17;
recomputed cells == frozen cells_tables_1_2_3.json to <1e-12). cells_legs.json:
3/3 binary cells PASS (stk_66_loser_driven, ind_66_long_driven,
ind_11_balanced), 4 contribution cells corroborate_claim, 2 split cells Tier2.
**Status:** resolved (M4 computed and reported; results/legs_long_short.md +
results/cells_legs.json written; no change to frozen data/, tables, or
REPORT.md numbers).
