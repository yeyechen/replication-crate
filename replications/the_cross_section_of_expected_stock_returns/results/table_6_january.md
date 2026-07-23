# Table VI Corollary — January seasonality of the ln(BE/ME) slope

Fama & French (1992), *The Cross-Section of Expected Stock Returns*. Decomposition of the 330 monthly Fama-MacBeth **reg(a)** ln(BE/ME) slopes (ret ~ ln(ME) + ln(BE/ME)) into January vs February-December, testing the paper's January-seasonality corollary.

> **Paper claim (`inputs/content.md` L2186):** "The average January slopes for ln(BE/ME) are about twice those for February to December. ... the average monthly February-to-December slopes for ln(BE/ME) are about 4 standard errors from 0, and they are close to (within 0.05 of) the average slopes for the whole year."

**Methodology.** Identical to `src/table_3_6.py` (imported, not re-implemented): `prewinsorize` clips ln(BE/ME), ln(A/ME), ln(A/BE), E(+)/P at each month's 0.005/0.995 cross-sectional fractiles (fractiles on the valid-return sample; beta, ln(ME), E/P dummy untouched — paper L1189, Assumption 9); `fm_monthly` fits a plain monthly cross-sectional OLS with intercept on the rows with a valid return; slopes are the time-series mean of the 330 monthly estimates x100 (%/month); the t-statistic is the mean divided by its time-series standard error (plain time-series t, NO Newey-West — paper L1187). reg(a) is the SAME specification Table VI reports (verified identical to R7). Reads only `data/panel.parquet`.

## Decomposition of the monthly ln(BE/ME) slopes

| Group | N months | Mean (%/mo) | Std (%/mo) | t-stat |
|---|---:|---:|---:|---:|
| January | 27 | 0.606 | 1.889 | 1.67 |
| February-December | 303 | 0.318 | 1.436 | 3.85 |
| **Full year (Jul 1963 - Dec 1990)** | 330 | 0.341 | 1.477 | 4.20 |

## Three-way comparison

- **Jan vs Feb-Dec:** Jan mean 0.606 %/mo is **1.91x** the Feb-Dec mean 0.318 %/mo ("about twice").
- **Feb-Dec significance:** the Feb-Dec slope is **3.85** standard errors from 0 ("about 4").
- **Feb-Dec vs full year:** the gap |full-year - Feb-Dec| = **0.024** (full 0.341, Feb-Dec 0.318), within the paper's 0.05 bound.

## Claim-element verdicts (L2186)

| Claim element (L2186) | Our value | Threshold | Verdict |
|---|---|---|:---:|
| (a) January slopes ~ 2x Feb-Dec | Jan/Feb-Dec = 1.91 (Jan 0.61, Feb-Dec 0.32) | ratio in [1.5, 2.5] | **PASS** |
| (b) Feb-Dec slope ~ 4 SE from 0 | Feb-Dec t = 3.85 | t in [3.0, 5.0] | **PASS** |
| (c) \|full-year - Feb-Dec\| < 0.05 | gap = 0.024 (full 0.34, Feb-Dec 0.32) | gap < 0.05 | **PASS** |

**Overall: 3/3 claim elements PASS.** The January-seasonality corollary replicates: there is a January seasonal in the BE/ME effect (January slopes about twice Feb-Dec), but the positive BE/ME relation is strong throughout the year (Feb-Dec ~4 SE from 0 and within 0.05 of the full-year mean).

## Notes

- The January t-statistic (1.67, N = 27 months) is NOT reported as a claim element; the paper's claim concerns the *magnitude* of the January slopes relative to Feb-Dec, and the *significance* of the Feb-Dec slopes. The wide January standard deviation (1.889) over only 27 Januaries is why the January mean, though larger, is itself less precisely estimated than the Feb-Dec mean.
- reg(a) ln(ME) (size) slopes are not decomposed here; the corollary (L2186) is specifically about the BE/ME effect, contrasting it with the well-known January seasonality of the size effect (Roll 1983; Keim 1983).
- Panel: 330 months (Jul 1963 - Dec 1990), 7,733 permnos; reg(a) fit on the valid-return rows each month, same as Tables III/VI.

---
*Computed by src/table_6_january.py from data/panel.parquet, importing prewinsorize + fm_monthly + ts_stats from src/table_3_6.py (same winsorization, same reg(a) = [ln(ME), ln(BE/ME)] specification, plain monthly OLS).*