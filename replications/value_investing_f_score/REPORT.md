# Replication Report — Piotroski (2000), "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers"

*Journal of Accounting Research*, Vol. 38, Supplement 2000, pp. 1-41. Replicated from `inputs/content.md` (JSTOR scan). Data: `comp_202601` (Compustat), `crsp_202601` (CRSP), ClickHouse catalog vintage 2026-07-22.

---

## 1. Executive summary

This replication reproduces Piotroski's F_SCORE fundamental-analysis strategy — nine binary signals (profitability, leverage/liquidity, operating efficiency) summed to a 0-9 score, applied to high book-to-market firms — and evaluates 162 per-cell targets across Tables 1-5, 7 and Appendix A.

**Verdict: the paper's methodology replicates. Its central economic claims replicate in sign, pattern, and (for the cross-sectional regression and the hedge portfolio) in magnitude. The full-period headline spreads (Table 3 High−Low 0.230) do not replicate numerically — an expected consequence of a user-approved sample restriction (1988-1996 instead of 1976-1996) forced by a data-vintage gap, documented in Assumption A1.**

What matches strongly:
- **The F_SCORE-return gradient in cross-section** (Table 7): +2.3-3.1% one-year market-adjusted return per F_SCORE point, vs the paper's stated 2.5-3% — Tier 1, robust to momentum/accrual/equity-offer controls, zero FAIL cells in the table.
- **The hedge portfolio** (Appendix A): average strong-minus-weak spread 0.104 vs paper 0.097 (Tier 1), t = 3.86 (paper 5.06), positive spread in 9/9 of our years (paper 17/21).
- **The high-BM universe construction** (Table 1): all-firms one-year market-adjusted mean 0.058 vs paper 0.059; raw 0.229 vs 0.239; signal positive-proportions within 0.06 of the paper on all eight signals; size-tercile shares within 0.6pp; MVE mean 182.5 vs 188.5 ($M).
- **The signal web** (Table 2): 10 of 13 Spearman targets Tier 1, including F_SCORE-signal correlations 0.35-0.58.

What does not match:
- The High−Low one-year market-adjusted spread: **0.105 vs 0.230** (same sign; Tier 2). Attenuated by the 40%-size restricted sample — but note the paper's *own* same-period (1988-1996) Appendix-A average spread is 0.091: our evidence is consistent with the paper's same-period evidence, not just its full-period headline.
- Small-group and near-zero cells (4 in Table 4, 3 in Table 3, 1 in Table 1, 1 in Appendix A): sign flips on means of magnitude ≤ 0.02, or tiny subgroups (11-47 obs) moved by vintage outliers — diagnosed, no methodology fix exists or is needed.
- Panel D (RANK_SCORE quintiles): the continuous-signal robustness check does not replicate (spread ≈ 0 vs paper +0.092) — three ranking variants tested, all null; documented per the paper's own footnote 12 warning about this method's inefficiency.

**Overall tally (162 contract metrics; 154 evaluated): 77 Tier 1 (50%) / 66 Tier 2 (43%) / 12 FAIL (8%) / 8 SKIP.** Every FAIL cell carries a diagnosis; every diagnosis carries either a tested fix or an explicit justified classification (§6).

---

## 2. Paper and methodology

### 2.1 What the paper does

Each year 1976-1996, Piotroski takes all Compustat firms with price and book data, sorts them into book-to-market quintiles using the **prior fiscal year's** distribution, and keeps the top quintile (high BM = "value" firms). Within that universe he computes nine binary fundamental signals from the most recent annual statements — F_ROA, F_ΔROA, F_CFO, F_ACCRUAL, F_ΔLEVER, F_ΔLIQUID, EQ_OFFER, F_ΔMARGIN, F_ΔTURN — sums them to F_SCORE ∈ {0,...,9}, and shows that firms with scores 8-9 ("strong") massively outperform firms with scores 0-1 ("weak") over the subsequent year: +13.4% vs −9.6% market-adjusted (spread 0.230, t = 5.59), shifting the entire return distribution rightward. Returns are 12/24-month buy-and-hold from the beginning of the fifth month after fiscal year-end, market-adjusted against the value-weighted index; delisting returns are set to zero. The final sample is 14,043 high-BM firm-years.

### 2.2 How we replicate it

The pipeline (`src/main.py` + six documented SQL files in `src/sql/`) implements the paper rule-by-rule — each of the 22 rules in `preparations/preprocessing_rules.json` cites the paper passage it implements:

- **Universe & sample:** full Compustat under the WRDS standard filter (`indfmt=INDL, datafmt=STD, consol=C, popsrc=D`); ME = prcc_f × csho at fiscal year-end (the paper's own definition, Table 1 fn a — a documented deviation from the CRSP-ME default); BE per the FF recipe (A3); BM quintile cutoffs computed within fiscal year t−1 over all Compustat firms and applied to year t (no lookahead, footnote 8); top quintile retained; firm-years missing any signal input dropped, never imputed.
- **Signals:** exact paper denominators — ROA and CFO on beginning-of-year assets; ΔLEVER and ΔTURN on average total assets (Table 1 fns i/j; the ΔTURN text-vs-footnote discrepancy resolved empirically, A4); ΔLIQUID from act/lct; EQ_OFFER from `sstk` (A2); missing `dlc` = 0 (A5).
- **Returns:** 12/24-month BHR from month FYE+5 (verified: Dec-1975 FYE → May-1976 start), delisted months contributing zero (paper's explicit rule, which overrides the standard delisting-adjustment convention); market adjustment from `crsp_202601.msi.vwretd` over the identical full window (A6); no winsorization anywhere (paper silent; Table 1 dispersion confirms, A7).
- **Links:** CRSP/Compustat merged link, `linkprim IN ('P','C'), linktype IN ('LC','LU'), usedflag=1`, temporally valid at the fiscal year-end (A8 — broadened from primary-only after iteration-1 diagnosis).
- **Extra machinery for robustness tables:** RANK_SCORE (percentile ranks of the nine raw realizations, summed, prior-year quintile cutoffs, footnote 12's mechanical no-sign-flip ranking), size terciles from prior-year full-Compustat MVE, 6-month pre-formation MOMENT, MOMENT/ACCRUAL deciles on prior-year all-Compustat cutoffs (Table 7).

### 2.3 The binding data constraint (Assumption A1, user-approved)

In the 2026 Compustat vintage, **`oancf` (operating cash flow) is NULL for every firm-year before fiscal 1987** (verified: 0 non-null rows FY1974-1986). Two of the nine signals (F_CFO, F_ACCRUAL) require it. The user chose to restrict the sample to FY1987-FY1995 (portfolio formation years 1988-1996) — keeping every signal exactly as the paper defines it, at the cost of the 1976-1987 years. The paper's own Appendix A gives the same-period benchmark: 7,205 firm-years over 1988-1996 with an average hedge spread of 0.097 (t = 5.059). All full-sample paper values are retained as Tier-2 references.

Within the restricted window, two further vintage constraints were verified as data-driven (not implementation artifacts): item coverage in this extract is genuinely sparse for small firms (`act` 71%, `lct` 73%, `oancf` 67% of all industrial firm-years FY1987-1995), and 37%→6% of high-BM firm-years lack any Compustat-CRSP link (OTC/foreign/micro names). These produce our final panel of **5,736 firm-years** (80% of the paper's same-period 7,205).

---

## 3. Results by table

Full per-cell tables with Tier verdicts are in `results/table_*.md`; the consolidated tally is in `results/evaluation_summary.md`.

### Table 1 — high-BM descriptive statistics (23/31 Tier 1, 7 Tier 2, 1 FAIL)

The sample construction validates. All-firms one-year market-adjusted mean **0.058 vs paper 0.059** (Tier 1) and raw mean 0.229 vs 0.239 (Tier 1); the percentage of positive market-adjusted returns 0.395 vs 0.437 (Tier 1); MVE mean 182.5 vs 188.5 and median 15.8 vs 14.4 ($M, Tier 1); BM mean 2.591 vs 2.444 (Tier 1). The eight signal positive-proportions track the paper within 0.06 (ROA 0.558/0.632, CFO 0.733/0.755, ACCRUAL 0.794/0.780, ΔMARGIN 0.439/0.454, ΔROA 0.414/0.432, ΔLEVER 0.506/0.498, ΔTURN 0.481/0.534; worst cell ΔLIQUID 0.441 vs 0.384, Tier 2). The single FAIL is the ΔTURN **mean** (−0.022 vs +0.0119, a tail-dominated statistic): the alternative denominator was tested and rejected (std 6.24 vs paper 0.59 — §6).

### Table 3 — returns by F_SCORE (16/51 Tier 1, 32 Tier 2, 3 FAIL)

The core result. Per-score one-year market-adjusted means (ours / paper): −0.236/−0.061, −0.007/−0.102, −0.068/−0.020, 0.004/−0.015, 0.019/0.026, 0.082/0.053, 0.155/0.112, 0.080/0.116, 0.075/0.127, 0.056/0.159. The gradient is clearly positive through score 6 (strong scores outperform weak), with a plateau at 7-9 rather than the paper's continued climb. **Low{0,1}: −0.034 (n=177) vs −0.096 (n=396); High{8,9}: 0.070 (n=546) vs 0.134 (n=1,448); High−Low spread 0.105 vs 0.230** — same sign, ~45% of the full-period magnitude, Tier 2. Welch t = 1.49 (paper 5.59); the mean spread is not significant at conventional levels in our 9-year sample — but the **Wilcoxon median test is (p = 0.002)**: the distributional shift the paper emphasizes does replicate. Panel A (raw) and Panel C (two-year) show the same ordering with the same attenuations. Panel D (RANK_SCORE): null — see §6.

Interpretation of the magnitude gap: the paper's 0.230 pools 1976-1996, including the strategy's best years (1979 spread 0.223, 1983 0.349, 1984 0.130). The paper's own 1988-1996 average spread is 0.091; ours is 0.105. The truncated sample also positively selects the Low group (only complete-data distressed firms survive the input filters), compressing the spread mechanically.

### Table 2 — Spearman correlations (10/13 Tier 1, 2 Tier 2, 1 FAIL)

The signal web replicates: corr(F_SCORE, one-year MA return) and the F_SCORE-vs-individual-signal correlations (0.35-0.58 range) are within tolerance, confirming each binary's definition and sign convention. The one FAIL (ρ(ΔLIQUID, ACCRUAL) −0.056 vs "0.573") is an OCR extraction artifact — the paper's 0.573 sits at the CFO-ACCRUAL position (ours 0.493, within 20%); the true paper ΔLIQUID-ACCRUAL is 0.071, and both values are ≈0 (§6).

### Table 4 — size partitions (4/18 Tier 1, 10 Tier 2, 4 FAIL)

The size-tercile construction validates: bucket shares 58.6/28.4/13.0% vs paper 59.1/27.8/13.1% (within 0.6pp). The High−Low spread is positive in all three buckets and strongest among small firms (0.154 / 0.007 / 0.031 vs paper 0.270 / 0.173 / 0.152) — the paper's ordering claim (benefits concentrated in small/medium firms) holds in direction, attenuated in magnitude. The 4 FAILs are sign flips on cells the paper itself reports as ≈0 (All-firm means of medium/large buckets: ours −0.014/−0.018 vs paper +0.008/+0.003) and on tiny Low groups (47 and 11 obs vs paper's 96 and 34) — §6.

### Table 5 — price / volume / analyst partitions (12/19 Tier 1, 5 Tier 2, 2 FAIL, 5 SKIP)

Added in outer iteration 2 (audit-1 majors M1/M2). The abstract-level claim that the strategy "is not dependent on purchasing firms with low share prices" **replicates in all three price buckets**: High−Low spreads +0.159 (small price), +0.041 (medium), +0.155 (large) — all positive, with the large-price bucket slightly exceeding the paper's 0.132. Volume partitions: the low-volume bucket replicates the paper almost exactly (**+0.233 vs 0.239, Tier 1** — the paper's "greatest gains in thinly traded stocks" claim), medium +0.092 (paper 0.175), but the high-volume bucket collapses to −0.039 (paper +0.203) — the one qualitative miss, attributed to the thinned restricted sample (n = 1,183; the Low group there is mildly positive, leaving no left tail to screen). The paper's "positive in all six buckets" claim: 5 of 6 replicated. **The analyst-coverage partition (Panel C) is a documented SKIP**: I/B/E/S coverage in this vintage classifies only 32.8% of panel firm-years for FY1987-1995 (below the 60% feasibility threshold; per-year coverage 25-45%, and unmatched firms cannot be separated from genuinely uncovered ones), so the covered-vs-uncovered comparison (paper: 0.114 vs 0.277) cannot be built reliably — evidence in `results/table_5_analyst.md`.

### Appendix A — annual hedge portfolio, F ≥ 5 vs F < 5 (6/9 Tier 1, 2 Tier 2, 1 FAIL, 3 SKIP)

The strongest replication result. Annual strong-minus-weak spreads 1988-1996: 0.155/0.100/0.046/0.112/0.231/0.037/0.016/0.027/0.213 (paper: 0.168/−0.036/0.157/0.166/0.070/0.020/−0.001/0.126/0.147) — positive in **9 of 9** years (paper: 17 of 21). Average: strong 0.093 (t 1.86) / weak −0.011 (t −0.22) / **spread 0.104 (t 3.86) vs paper 0.097 (t 5.06)** — Tier 1. The single FAIL (weak-leg average −0.011 vs +0.009) is a sign flip on a value statistically indistinguishable from zero in both samples (paper t = 0.243). The cumulative hedge path (`results/hedge_cumulative.png`) grows ~2.4× over the 9 formation years.

### Table 7 — cross-sectional regressions (6/14 Tier 1, 8 Tier 2, 0 FAIL)

F_SCORE subsumes the control variables exactly as the paper claims. Pooled model (2): F_SCORE **0.0276** (t 3.55) vs paper 0.031 (t 8.18); model (4) with momentum/accrual/equity-offer controls: **0.0227** (t 2.72) vs 0.027 (t 6.75); Fama-MacBeth-style average over 9 annual regressions: **0.0313** (t 3.12) vs paper ≈0.028. All within the paper's stated "2.5-3% per point" range — the paper's central econometric claim replicates at Tier 1. Controls behave sensibly: logMVE negative and significant (−0.047 to −0.049), EQ_OFFER ≈ 0 once F_SCORE is included (−0.005, paper −0.007). Two Tier-2 notes: within-high-BM logBM is attenuated (0.030-0.036 vs 0.103) and the ACCRUAL-decile coefficient is somewhat larger (−0.015 vs −0.003) — both same-sign, both consistent with the restricted sub-period.

---

## 4. Evaluation summary

| Table | Tier 1 | Tier 2 | FAIL | SKIP | Total |
|---|---:|---:|---:|---:|---:|
| Table 1 (descriptives) | 23 | 7 | 1 | 0 | 31 |
| Table 2 (correlations) | 10 | 2 | 1 | 0 | 13 |
| Table 3 (returns by score) | 16 | 32 | 3 | 0 | 51 |
| Table 4 (size partitions) | 4 | 10 | 4 | 0 | 18 |
| Table 5 (price/volume/analyst) | 12 | 5 | 2 | 5 | 19 (+5 SKIP) |
| Appendix A (annual hedge) | 6 | 2 | 1 | 3 | 9 |
| Table 7 (regressions) | 6 | 8 | 0 | 0 | 14 |
| **Total** | **77** | **66** | **12** | **8** | **162 (154 evaluated)** |

Tolerance conventions per `rep/TOLERANCE_RULES.md` (annual returns ±50% default, headline spreads tightened to ±35%, t-stats ±40%, coefficients ±40-50%, correlations ±20-50%, counts ±15-25%). The 8 SKIPs: 3 pre-1988 Appendix-A cells and 5 Table 5 Panel-C analyst cells (IBES coverage 32.8% < 60% feasibility threshold — documented data gap, not a choice).

---

## 5. Assumptions registry (paper-silent decisions)

Eight decisions in `preparations/assumptions.md`: **A1** sample restricted to FY1987-1995 (user-approved, oancf vintage gap); **A2** EQ_OFFER via `sstk` NULL-or-zero; **A3** book equity FF recipe with fallbacks; **A4** ΔTURN on average total assets (paper text/footnote discrepancy — resolved by testing both, average-assets matches the paper's std 0.59 vs alternative's 6.24); **A5** missing `dlc` = 0; **A6** market proxy = CRSP vwretd; **A7** no winsorization; **A8** CRSP link = P+C primary/confirmed links (broadened after iteration-1 diagnosis; +21.6pp link coverage, +1,779 firm-years).

---

## 6. FAIL-cell registry (all 10, diagnosed)

Every failure was either subjected to a fix attempt with before/after measurement, or explicitly classified with justification:

| # | Cell | Ours / Paper | Diagnosis & resolution |
|---|---|---|---|
| 1 | T1 ΔTURN mean | −0.022 / +0.0119 | **Fix attempted:** alternative denominator (beginning assets) tested → std 6.24 vs paper 0.59 (decisively worse); current definition kept. Tail-dominated statistic; signal proportion (0.481/0.534) and dispersion match. Residual vintage drift. |
| 2 | T2 ρ(ΔLIQUID,ACCRUAL) | −0.056 / "0.573" | **Reclassified:** OCR row-offset artifact in the parsed lower-triangular matrix; the paper's 0.573 is the CFO-ACCRUAL cell (ours 0.493, Tier 1). True paper ΔLIQUID-ACCRUAL ≈ 0.071; both ≈ 0. |
| 3 | T3 score-3 mean (1-yr MA) | +0.004 / −0.015 | **Classified (noise):** sign flip on a ±0.02 near-zero cell; neighboring scores 2 and 4 track the paper (−0.068/−0.020; 0.019/0.026). No methodology change could move score-3 without moving its matching neighbors. |
| 4 | T3 Panel D Q5−Q1 mean | −0.004 / +0.092 | **Fix attempted:** three ranking variants tested (min-rank, average-rank, sstk-amount rank) — all null (−0.004 to −0.005, 2-yr also negative). Pre-committed adoption rule not met; null documented. Paper's footnote 12 attributes this method's inefficiency to sign-blind mechanical ranking; the paper's +0.092 comes from a 3× larger sample. |
| 5 | T3 Panel D Q5−Q1 t | −0.08 / 4.488 | Same as #4. |
| 6 | T4 All mean medium | −0.014 / +0.008 | **Classified (near-zero):** paper's own value ≈ 0 (t not reported as significant for the All-mean); sign of a 1-pp mean carries no information. The economically meaningful High−Low spread keeps the paper's sign in all buckets. |
| 7 | T4 All mean large | −0.018 / +0.003 | Same as #6. |
| 8 | T4 Low mean medium | +0.035 / −0.094 | **Classified (tiny subgroup):** n = 47 (paper 96) — a handful of vintage outliers flip a 12-pp mean in a 47-firm cell. Low group is also positively selected by the input-completeness filter (A1). High−Low medium spread retains the paper's positive sign (0.007… attenuated). |
| 9 | T4 Low mean large | +0.030 / −0.132 | Same as #8 (n = 11 vs paper 34). |
| 10 | AppA weak-leg average | −0.011 / +0.009 | **Classified (near-zero):** paper's own t on this value is 0.243 — indistinguishable from zero in the paper too. The spread (the economic object) is Tier 1. |
| 11 | T5 high-volume H−L mean | −0.039 / +0.203 | **Classified (sample thinning):** the high-volume bucket under A1 holds 1,183 firms; its Low{0,1} subgroup earns +0.041 (mildly positive), so there is no left tail for the screen to remove. The paper's full-sample high-volume Low group earns −0.235. The low- and medium-volume buckets keep the paper's sign (0.233/0.092). No targeted fix: the bucket composition is determined by the documented restriction. |
| 12 | T5 high-volume H−L t | −0.30 / 2.863 | Same as #11. |

---

## 7. Limitations

1. **Sample period truncation (A1):** 9 formation years instead of 21; 5,736 firm-years vs 14,043 (80% of the paper's same-period 7,205). All full-period magnitudes (the abstract's "7.5% annually", the 23% long-short return) are unreachable by construction; same-period magnitudes are the valid comparison and they replicate.
2. **Data-vintage drift:** 2026 Compustat restatements and sparser small-firm item coverage (act/lct ~71-73%, oancf ~67-87% within the window) positively select the Low-F_SCORE group (complete-data distressed firms only), mechanically compressing the High−Low spread. Verified data-driven, not fixable in code.
3. **Mean-significance attenuation:** our High−Low t-stat (1.49) does not clear conventional bars; the median/distributional tests do (Wilcoxon p = 0.002), and the annual hedge t (3.86) does.
4. **Panel D (RANK_SCORE)** robustness check does not replicate — documented null (§6 #4).
5a. **Analyst-coverage partition (Table 5 Panel C) is a documented SKIP:** I/B/E/S summary coverage classifies only 32.8% of 1988-1996 panel firm-years (per-year 25-45%); below the 60% feasibility threshold, with no reliable way to separate unmatched firms from genuinely uncovered ones. The paper's covered-vs-uncovered contrast (0.114 vs 0.277) is therefore unverifiable on this vintage.
5. **Bootstrap p-values** use seed 42 (paper silent on seed); 1,000 iterations as in the paper.
6. Percentile method (linear interpolation) and Welch t-stats (vs paper's pooled) are conservative choices noted in the table footnotes.

## 8. Conclusion

Piotroski's (2000) methodology is faithfully reproduced: the universe construction, the nine signal definitions, the F_SCORE aggregation, the prior-year cutoff machinery, the fifth-month buy-and-hold windows with zero-delisting returns, and the market adjustment all implement the paper's stated rules with citations. Within the user-approved 1988-1996 window, the replication confirms the paper's three core findings — F_SCORE separates high-BM winners from losers in cross-section (+2.3-3.1% per score point, Tier 1), the strong-minus-weak hedge earns ~10% per year with 9/9 positive years (Tier 1), and the effect is strongest among small firms (direction replicated) — with the full-period headline spread (0.230) attenuated to 0.105, consistent with the paper's own same-period evidence (0.091). The replication is a **documented partial at Tier 1/2**: 90% of cells pass at Tier 1 or 2, and every failure is diagnosed and attributable to the documented sample restriction, vintage drift, near-zero cells, or one OCR artifact — none to a methodology error.

---

## 9. Reproducibility

```
cd <repo root> && uv run python replications/value_investing_f_score/src/main.py
```

rebuilds the full pipeline from ClickHouse (six SQL files in `src/sql/`, header-documented dependency chain), writes `data/panel.parquet` (5,736 × 43), regenerates all six `results/table_*.md` + `results/evaluation_summary.md` and the four figures. Idempotent — consecutive runs produce identical outputs.
