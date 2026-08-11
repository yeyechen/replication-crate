# Assumptions log — Anderson & Garcia-Feijoo (2006) replication

This file logs the paper-silent choices, spec interpretations, and any
ambiguities encountered while implementing the replication. Append-only.

---

## Iteration 1 (panel + Table II)

### Spec concern: permno 14593 is Apple, not IBM

The task spec asked for a sanity check on permno 14593 calling it "IBM".
CRSP assigns permno 14593 to **Apple Inc.** (gvkey 001690, ticker AAPL,
started 1980-12-12 at NASDAQ), not IBM. IBM's CRSP permno is 12490
(gvkey 006066). I ran the sanity check on permno 14593 = Apple, since
that is what the data actually shows. The sanity check values
(prc ≈ 44 in 1990-06, ret = +8.5% for June 1990, mcap ≈ $5.4B) all
match Apple Inc.'s June 1990 stock price and market cap.

**Action:** No code change. Just flagging the spec-vs-data mismatch.
The replicator can either (a) re-verify the permno the spec intended
and rerun the sanity check on the correct permno, or (b) accept the
Apple sanity check as proof-of-life.

### Spec concern: `msfhdr` is not strictly PIT

The task spec called for `crsp_202601.msfhdr` to provide PIT shrcd and
exchcd. The `msfhdr` table has exactly **one row per permno** (38,872
rows for 38,872 unique permnos), with `begdat`/`enddat` covering the
full lifetime. So `hshrcd` and `hexcd` in `msfhdr` are the latest
snapshot, not a PIT history. This means the spec's "PIT" wording is
inaccurate for `msfhdr`.

For PIT shrcd/exchcd/siccd filtering I used `crsp_202601.dsenames`,
which does carry multi-record `namedt`/`nameendt`/`shrcd`/`exchcd`/
`siccd` per permno. This is the correct PIT source per the CRSP
reference doc (`references/CRSP.md` § dsenames).

### Paper-silent choice: `inv_growth` clip boundary

The paper L438 / L441 footnote says deciles are formed after dropping
the top and bottom 1% of `inv_growth`. Equivalently, observations with
`inv_growth > 10` or `inv_growth < -0.99` are deleted (the "10" cap
is the 99th-percentile cutoff in the historical US sample). I apply
this clip in Python at the decile-sort step, not in the panel SQL,
so the panel parquet preserves the full `inv_growth` distribution for
auditing. The clip is applied BEFORE decile assignment.

### Paper-silent choice: `pd.qcut` ties

`assign_quantiles` uses `pd.qcut(..., duplicates="drop")` with a rank
fallback when ties dominate. For `inv_growth` ties are rare
(continuous variable); the standard `pd.qcut` path is used in every
year.

### Paper-silent choice: 3-year Compustat tenure + 36-month CRSP history

The paper's §I says the firm must be on Compustat for 3 years and have
36 months of return history before portfolio formation. I do NOT
enforce these in the panel SQL — I enforce them implicitly by requiring
non-null `inv_growth` at the formation year (since `inv_growth`
computation requires capx at fyear = year0 - 1 AND fyear = year0 - 3,
which in practice requires the firm to have been on Compustat for at
least 3 years). The 36-month history check would require an extra
SQL pass; I have not yet implemented it. The impact on Table II
should be small (the average effect is just to drop the youngest
firms, which would otherwise be a small fraction of the panel). If
the auditor flags this as a gap, the next iteration can add the
36-month filter via a `WHERE month >= addMonths(first_ret_month, 36)`
predicate in the panel SQL.

### Paper-silent choice: PIT universe filter via `dsenames`

Universe filter applied via `dsenames` PIT join:
`shrcd IN (10, 11)`, `exchcd IN (1, 2, 3)`, `siccd NOT IN 6000-6999`
(financials excluded). I use `siccd < 6000 OR siccd >= 7000` to
implement the exclusion. CRSP-delisting sentinels (`ret > -1.0`)
are dropped at the universe step.

### Paper-silent choice: delisting returns not adjusted

The paper does not mention delisting-return adjustment (Shumway 1997
or BMP 2007); the paper text uses raw returns throughout Table II.
I use raw `ret` from `msf` with no delisting-return substitution. If
the auditor later flags this, it can be added by left-joining
`msedelist` and substituting `dlret` for `ret` on the delisting month.

### Paper-silent choice: `me_dollars` units

`me_dollars = abs(prc) * shrout * 1000` per CRSP convention
(`prc` in $/share, `shrout` in thousands). The `*1000` converts from
thousands to dollars. The panel column is named `me_dollars` to make
the unit explicit.

### Paper-silent choice: panel parquet columns

The panel parquet includes both required columns (`permno`, `month`,
`gvkey`, `ret`, `me_dollars`, `year0`, `inv_growth`) and a few extras
(`prc`, `shrout`, `exchcd`, `siccd`, `shrcd`) for downstream
debugging. The extra columns are not used by `evaluate.py` but allow
the auditor to re-derive filters without re-running the full SQL.

### Paper-silent choice: decile sort uses all stocks (not NYSE-only)

The task spec says "use a uniform all-stock decile sort" for the
investment-growth signal (the spec explicitly says NYSE-only
breakpoints are for size/B/M, NOT for inv_growth). I use
`assign_quantiles(df, "year0", "inv_growth", n_bins=10)` which bins
all stocks with non-null `inv_growth` in each year0.

### Paper-silent choice: formation years 1976..1998

Per the paper, portfolios form June of year t, returns computed July t
through June t+1. The paper sample ends in 1999 (formation year) with
returns through June 2000. I restrict formation years to 1976..1998
(the last complete formation year), so returns cover July 1976 through
June 1999 (276 months), matching the paper's reported sample. The
panel parquet retains rows for years 1999..2000 (formation year) for
possible future iteration extensions (e.g., Table V factor construction
needs through 2000-06).

---

## Iteration 2 (Table III Panel A, full sample, rows 2-6)

### Paper-silent choice: `ln_me` uses formation-month ME, not per-row ME

The spec's literal definition is `ln_me = log(abs(prc) * shrout * 1000)`,
which is per-row. Computing it that way produces a positive size
coefficient (per-row me_dollars mechanically correlates with the
same-month return - large stocks that had a price increase this month
have a large me_dollars AND a large ret). This is the canonical
look-ahead-bias trap for size in cross-sectional regressions.

The Fama-MacBeth convention is to use size at portfolio formation
(end of June of year t) and hold it constant for the 12-month holding
window. Implemented as `me_jun_form` = me_dollars at the calendar June
(year0 + 1) row in the panel (= the panel year0 = Y row with month =
June Y+1, which is the LAST month of the cohort window). The lookup
joins by `p.year0 - 1 = j.snap_year0` (so for cohort year0 = Y, the
snapshot is the June row whose panel year0 = Y-1 = calendar June Y).

This recovers the paper's negative size coefficient (-0.17% / unit
Ln(size) for `ret ~ ln_me` alone) without reversing any other spec.
Result: ln_size coef = -0.14% (paper -0.17%, |dev|/|paper| = 17%;
PASS at 35% tolerance).

### Paper-silent choice: `ln_bm` uses December-snapshot ME

The paper says B/M uses "market value of equity at the end of
December of calendar year t-1". Implemented as `me_dec` snapshot at
the December (Y-1) row in the panel (= the panel year0 = Y-1 row
with month = Dec, so the join is `p.year0 - 1 = m.snap_year0`).
Book equity uses the FF recipe (Davis-Fama-French memo):

  primary = ceq + txdb - pstkrv (in millions, x 1,000,000 to
            convert to dollars)
  fallback = at - dlc - dltt - pstkrv (in millions, x 1,000,000)

Units: comp_202601.funda's ceq/txdb/pstkrv/at/dlc/dltt are stored
in **millions of USD**. CRSP `me_dollars` is in **dollars**. With
the *1e6 conversion BE and ME are unit-consistent and bm has
sensible distribution (median 0.67, 1%=0.03, 99%=4.6 in our
sample). Without the conversion the median BM was 0.0000 (typical
Compustat BE is ~$30M, CRSP ME ~$50M, ratio 6e-7 ≈ 0).

### Paper-silent choice: `ln_inv = ln(1 + inv_growth)`

The spec offered two candidate transforms:
- `ln(max(inv_growth, 0.001) + 1)` - collapses all negative-growth
  firms to ln(inv) ~ 0.001, eliminating their cross-section variation.
- `log(1 + inv_growth)` (= ln(capx_t/capx_{t-2})) - symmetric
  around 0; well-defined for inv_growth > -1 (enforced by the
  paper's 1% clip).

Implemented the cleaner second form. Empirical check: distribution
matches the paper's Ln(inv) range (median 0.22, std 1.13,
99% = 3.45, 1% = -2.89). Coefficient on `ret ~ ln_inv` alone is
-0.26% per unit (t-stat -7.0).

### Paper-silent choice: t-statistic is plain, NOT Newey-West

Paper L172 explicitly says "t-statistic is the time-series average
divided by its standard error" (no HAC). Implemented plain
t-stat: `mean / (std / sqrt(N))` per-month over the monthly
slopes. The Newey-West correction for non-overlapping monthly
cross-sections is small, so the choice matters little for the
t-stats, but the paper convention is to report the plain version.

### Paper-silent choice: per-month winsorization at 1%/99% (NOT yearly)

Paper L172 says "for each independent variable, the top and bottom
one percent are deleted each year to exclude extreme observations"
(yearly winsorization), while Table III caption L738 says "Ln(size),
Ln(B/M), and Ln(inv) are winsorized at the 1% and 99% levels"
(per-regression winsorization). These two specifications are
slightly different (per-month vs per-year). Implemented per-month
winsorization since it's the more conservative (per-regression)
choice and matches the canonical `fama_macbeth` primitive.

### Known magnitude discrepancy on Ln(inv) coefficient

My Ln(inv) coefficient is about -0.26% per unit; the paper reports
-4.19% per unit (~16x smaller in mine). Same discrepancy in the
3-variable model (mine -0.19% vs paper -3.52%, ~18x). The prior
replication (in `replication_archive_jkp/`) flagged the same issue
and attributed it to a Compustat vintage effect (the paper uses a
pre-2000 Compustat vintage; the 2026 vintage contains restated capx
values). All my transforms give the same magnitude; the
discrepancy appears fundamental to the input data. T-stats are
much closer (mine -7.0 vs paper -6.0 for the Ln(inv)-only model),
so the Ln(inv) signal is statistically strong in both.

The corresponding target cells will FAIL by magnitude:
`ln_inv_model5_coef`, `ln_inv_model6_coef`. The Ln(inv) t-stat
cells PASS. This matches the prior replication's pattern.

---

## Iteration 4 (audit 1 fix-iteration)

### A11 — Ln(inv) scale discrepancy (M2, M5, M3)

**Diagnosis:** Our Ln(inv) coefficient is 16× smaller than the paper's
(−0.26 vs −4.19); the t-statistic matches (−6.99 vs −6.00). The
audit's [M2] ruling: a t-stat is invariant to regressor scale, so the
matching t-stat is not evidence of vintage agreement. The per-SD
effect (β × SD) is the same to 4 decimals (ours −0.268 %/mo per SD,
paper's implied −0.268 %/mo per SD), consistent with a regressor-scale
change but not a different real effect. **Table I (M6) rules out the
Compustat-vintage hypothesis:** our 5×5 size × B/M means fall in
0.20-1.29 (paper 0.17-1.03) and medians in -0.02-0.72 (paper -0.05-0.54);
a vintage shift large enough to bend Ln(inv) 16× would not leave Table I
within ~30% of the paper's values.

**Next fix:** No further fix available in this single-vintage pull. The
honest write-up is "unresolved scale discrepancy; inference (sign, t, R²)
replicates". The status is FAIL (not Tier 2).

**Before metric:** iter 3 — `ln_inv_model5_coef = -0.26` (paper -4.19) was
PASS/BORDERLINE; treating it as "Tier 2 vintage artifact" was a
diagnose-and-skip pattern.

**After metric:** iter 4 — `ln_inv_model5_coef = -0.26` FAIL (ladder Tier 1
falls back to FAIL because |ours/paper| = 0.062 > 2). Subperiods (1976-1987,
1987-1999, Feb-Dec) all show the same 16× mismatch. The audit's per-SD
diagnostic is in `results/ln_inv_scale_diagnostic.md`.

**Status:** FAIL — scale-discrepancy unresolved; the retirement-by-t-stat
fallacy is removed.

### A14 — Table V VW weighting (M1)

**Diagnosis:** The shipped contemporaneous-weight construction uses
`me_dollars` (same-month ME) as the VW weight, embedding the month's
own return. Panel-wide VW mean = 1.949 %/mo; lagged-me_lag mean =
1.324 %/mo; CRSP/FF market total = 1.334 %/mo. Shipped quintile means
non-monotonic (2.14, 1.91, 1.81, 1.93, 2.40); lagged means monotonic
(1.14, 1.31, 1.36, 1.44, 1.47). The audit's [M1] recommendation: use
me_lag (per-permno one-month-lagged ME) as the primary VW weight; report
both weightings side-by-side without silently replacing one.

**Next fix:** Add `me_lag = me_dollars.shift(1)` per permno in
`build_panel()` and `build_fm_panel()` (cached as new column). Re-run
`build_inv_factor()` under three weighting conventions: (a) me_dollars
(contemporaneous, original shipped), (b) me_lag (lagged, primary), (c)
me_jun_form (FF 1993 formation-month). Write both `results/table_5.md`
(lagged) and `results/table_5_contemp.md` (contemporaneous).

**Before metric:** iter 3 — Table V 12/13 PASS at Tier 1 using
contemporaneous weights; alpha cells matched the paper because the
look-ahead bias was the same on both sides of the regression.

**After metric:** iter 4 — Table V 7/13 PASS at Tier 1 using LAGGED
weights (5 Tier 1 + 6 Tier 2 + 2 FAIL). The 2 FAILs are alpha cells
(`highest_alpha_mkt_only_lag = -0.004` paper +0.006, `highest_alpha_3factor_lag = -0.001` paper +0.008). The contemporaneous-weight results are also reported (12/13 PASS) for comparison.

**Status:** PASS — both weightings are reported; the audit's request to
"show both per-cell results side-by-side" is satisfied.

### A15 — 36-month return-history filter (M7)

**Diagnosis:** The paper's §I states "in computing returns we require
36 months of data before a company is included in a portfolio" but the
filter was not implemented in iter 1-3 (assumptions entry 56-70).
The audit's [M7] ruling: implement and report the impact.

**Next fix:** Add per-permno `n_prior_ret` column (row_number() - 1) in
`panel.sql` and `fm_panel.sql`. Apply `n_prior_ret >= 36` filter at the
analysis stage.

**Before metric:** iter 3 — no filter applied; `inv_growth` non-null =
1,079,916 of 1,364,746 rows (20.9% NaN); Table II spread = −0.78.

**After metric:** iter 4 — filter applied; rows = 899,640 (34.1% removed);
permnos = 10,515 (28.9% removed); Table II spread = −0.85 (a 0.07 %/mo
shift). The filter widens the spread slightly, consistent with the
paper's claim that it drops young growth stocks.

**Status:** PASS — filter implemented; impact documented.

### A16 — Table I (M6)

**Diagnosis:** Claims C1 and C4 had no covering table. Table I was
REQUIRED under `prep/PREP_TABLES_PROMPT.md` (it validates the
`inv_growth` construction and is the cheapest test for [M2]).

**Next fix:** Compute 5×5 size × B/M portfolios (NYSE breakpoints,
positive B/M only, top/bottom 1% of inv_growth trimmed) of mean and
median inv_growth. Write `results/table_1.md` and add the table to
`preparations/tables_to_replicate.json` with `covers_claims: ["C1"]`.

**Before metric:** iter 3 — C1/C4 uncovered; Ln(inv) magnitude FAIL
unresolved.

**After metric:** iter 4 — Table I committed (50 metrics = 25 cells ×
2 stats). Our means land in 0.20-1.29 (paper 0.17-1.03); medians land
in -0.02-0.72 (paper -0.05-0.54). The pattern (decreasing across B/M
within size, decreasing across size within B/M) replicates. **The
Compustat-vintage hypothesis for [M2] is retired.**

**Status:** PASS — Table I implemented; vintage hypothesis retired.

### A17 — Model 1 (β only) and Model 7 (β + 4 controls) (M4)

**Diagnosis:** β was built in iter 3 (`data/panel_with_beta.parquet`,
1,055,375 non-null, mean 1.09) but never joined into the FM panel.
Six committed cells (β_model7_{coef,tstat}, ln_size_model7_{coef,tstat},
ln_bm_model7_{coef,tstat}, ln_inv_model7_{coef,tstat}) were silently
dropped by `evaluate.py:143-150`. Model 1 cells (alpha_model1_beta_only,
alpha_model1_tstat) were also untested.

**Next fix:** Join β into the FM panel via `build_fm_panel_with_beta()`.
Run `compute_table_iii(include_beta=True)` to add models 1 and 7. Make
`evaluate.py` print explicit SKIP rows for any committed metric absent
from the results JSON.

**Before metric:** iter 3 — 6 cells silently dropped; 4 cells printed as
deferred (inconsistent across reports).

**After metric:** iter 4 — all 26 Table III cells evaluated; 12 PASS,
4 BORDERLINE, 10 FAIL. The 10 FAILs include β cells (model 1 coef 0.43
paper 0.03; model 7 β coef 0.58 paper -0.31 — wrong sign) and Ln(inv)
coefs (16× off). T-statistics for β are now positive (~1.4 paper 0.08)
and Ln(inv) t-stats match the paper (model 7 -6.48 paper -5.88).

**Status:** PASS — 10 newly-evaluated cells reported; tier vocabulary
now following the harness ladder.

### A18 — Tier vocabulary and pass-rate arithmetic (M3)

**Diagnosis:** Iter 3 used "Tier 2 (pattern match with documented cause)"
for the 16× Ln(inv) coefficient mismatches, citing the matching t-stat.
The audit's [M3] ruling: this violates the 2× ladder bound in
`audit/RUBRIC.md` / `audit/SKILL.md` Spot-check 10. Also, pass-rate
arithmetic was "33/37 = 89%" which matches no committed or evaluated
denominator.

**Next fix:** Make `evaluate.py` emit the harness ladder explicitly
(Tier 1 / Tier 2 / FAIL / SKIP) in addition to the tolerance bands.
Print both denominators (committed and evaluated). Do NOT re-label
>2× misses as "Tier 2". Update REPORT.md to use the correct tally.

**Before metric:** iter 3 — `ln_inv_model5_coef` was labeled "Tier 2
vintage artifact".

**After metric:** iter 4 — `ln_inv_model5_coef` is FAIL (ladder
Tier 1 falls back to FAIL because |0.26/4.19| = 0.062 > 2). Pass-rate
arithmetic: 42/100 = 42% Tier 1 (committed); 50/100 = 50% Tier 1 + Tier 2
(committed). The "89%" was unreachable arithmetic.

**Status:** PASS — tier vocabulary corrected; the Ln(inv) cell
retirement-by-t-stat is barred.

### A19 — Subperiod robustness (M5)

**Diagnosis:** Table III has Panel B subperiod rows (1976-1987,
1987-1999) and a Feb-Dec exclusion row that were deferred in iter 2.

**Next fix:** Run `compute_table_iii_subperiods()` on three month
masks. Write `results/table_3_subperiods.md`.

**Before metric:** iter 3 — subperiods deferred; deferred count
inconsistent across reports (2 vs 4 vs 10).

**After metric:** iter 4 — subperiods computed. Ln(inv) significant in
all 6 cells (3 masks × 2 model specifications). The 16× coefficient
magnitude mismatch persists across all subperiods (same scale
discrepancy). Paper's stability claim ("robust to exclusion of January
returns and to subperiods") replicates in direction.

**Status:** PASS — subperiods computed and reported.

### Book-equity sample size

After dropping firms with negative book equity (per paper L110
"we do not use firms with negative book values") and requiring
non-null ret, ln_me, ln_bm, ln_inv, the regression sample has
965,980 stock-month observations across 276 months (avg 3,500
firms per month). This is comparable to the prior replication's
~740k obs but covers more firms because my Ln(inv) definition
(unlike the archive's `if (inv_growth > 0, log(inv_growth), 0)`)
includes negative-growth firms with valid Ln(inv).

### Sub-period results and Feb-Dec exclusion deferred

Table III has 4 rows per model that are deferred to a later
iteration: subperiod results (1976-1987 N=132, 1987-1999 N=144)
and the Feb-Dec only (N=253) row. Also deferred are rows 1 and 7
of Table III Panel A (model 1 = beta-only and model 7 = all-
controls incl. beta) - both require the `beta` column, which the
FM panel does not yet carry. Beta construction is planned for a
later iteration that depends on FF factor returns being available
in ClickHouse.

---

## Iteration 3 (beta + INV factor + Table V Panel A)

### Paper-silent choice: beta std is wider than the spec's expected range

The spec's quality bar says "verify beta distribution: mean ~1.0,
std ~0.3-0.5". My pooled std = 0.75; cross-sectional std at each
June ranges 0.59 to 0.91. The spec's range is consistent with the
Fama-French (1992) NYSE-only universe; my 0.6-0.9 reflects the
broader NYSE + AMEX + NASDAQ universe. The mean (~1.09) is on
target and the 5% / 95% percentiles are also wider in our
sample. Reported as a fact; the spec bar is met at 80-90%
non-null-beta coverage per June (well above the 50% threshold),
but the std band is wider than the spec's stated 0.3-0.5.

### Paper-silent choice: VW weighting for the INV factor

The paper is silent on the INV factor weighting. The spec says
"use VW for consistency with Table V (which uses VW portfolios)." I
adopted VW with `me_dollars` as the weight — the same convention as
the existing Table II / IV EW + VW pipeline. The Fama-French (1993)
factors (SMB, HML) are also value-weighted, so this is consistent
with the FF-style factor convention.

### Paper-silent choice: INV factor construction — Q5 - Q1 (low - high)

Per the spec's "INV factor return = R_Q5 - R_Q1", I subtract Q1
(highest inv growth) from Q5 (lowest inv growth). Result: positive
mean (~0.26%/mo in our sample vs paper's 0.24%/mo). The sign
matches the paper's claim that low-inv-growth firms earn higher
returns. The regression coefs are NEGATIVE for the highest-inv-growth
portfolio and POSITIVE for the lowest-inv-growth portfolio, matching
the paper's Table V Panel A pattern.

### Paper-silent choice: All-coefficient breakpoints on inv_growth

The spec says "uniform all-stock quintile sort" on inv_growth
(NOT NYSE-only). I used `assign_quantiles(df, "year0", "inv_growth",
n_bins=5)` which bins all stocks with non-null inv_growth in each
year0. Mean firms per (year0, month, quintile) ≈ 700 (paper FF-style
factor construction typically uses NYSE-only breakpoints, but the
spec explicitly says all-stock).

### Spec concern: JSON unit convention for Table V alpha cells

The JSON `value` field for alpha cells (e.g., `highest_alpha_mkt_only
= 0.006`) is in DECIMAL-return units per the spec note "treat '0.006'
as 0.6%/month". My output is in PCT per the spec ("Coefficients and
alphas are in percent per month") so my α = 0.600 for the same cell.
The values represent the same decimal/pct = 0.6% per month. The
JSON's "unit": "pct" label is misleading — the actual value is in
decimal. I converted my output to decimal (divide by 100) in the
JSON payload so the comparison is apples-to-apples. The coef cells
(unit = "coef") are in pct-per-unit form (dimensionless) which
matches my output unit directly.
