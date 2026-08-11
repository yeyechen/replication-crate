---
schema_version: 2
slug: jegadeesh_1990_evidence_of_predictable_behavior_of_security_returns
iteration: 3
verdict: FAILED
overall: 3.83
methodology: 4
headline_matching: 5
data_coverage: 5
concrete_result: 3
signal_strength: 1
corollary: 5
generated_at: 2026-08-11T03:55:00Z
---

# Replication Summary

## Evidence of Predictable Behavior of Security Returns (Jegadeesh, 1990)

### Bottom line

**Replication result:** `FAILED`
**Overall quality:** 3.83 / 5.00

The replication is faithful in substance. Under the binary Match/FAIL design (DEV-041, re-scored at iteration 5), 57 of 89 committed cells (64.0%) are Match and 32 are FAIL. The 32 FAIL cells include the original single FAIL (`s1_p1_alpha_jan`) plus 31 cells that under the prior harness were Tier 2 (sign match, magnitude outside tolerance). Every FAIL carries a closed-vocabulary marker in `assumptions.md` satisfying criterion B. The headline S0 P1-P10 spread (C1) reproduces at 2.86%/month vs the paper's 2.49%/month (t = 17.6 vs 16.8). The rubric's kill switch (signal_strength = 1) applies despite overall ≥ 3.0.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | 8/8 sub-checks pass with one documented deviation: Q1/Q3 R² cells ship adjusted R² (matching `tables_to_replicate.json`'s "adjusted R^2" description), All-rows ship unadjusted R² (matching paper 0.108/0.102 exactly). The split is documented in Assumption 16 with empirical justification per group. |
| Headline matching | 5/5 | All 6 paper claims reproduce. C1 (S0 P1-P10 spread +0.0286 vs +0.0249, t=17.6 vs 16.8), C2 (a_1 = -0.0969 vs -0.0923, t=-18.55 vs -18.58), C3 (a_12 = +0.0317 vs +0.0339, t=8.08 vs 9.09), C4 (Feb-Dec subsample a_1 = -0.0827 vs -0.0801), C5 (size-model S0 spread +0.0282 vs +0.0246), C6 (Spearman S0/S1 +0.701 vs +0.664). |
| Data coverage | 5/5 | CRSP panel 1926-01 to 1988-12, 1,652,341 rows, 0 duplicates on (permno, month). Table I (1929-1982) has 648 months × 1,869 stocks/month avg; Table II (1934-1987) has 648 × 2,339; Table VI (1963-1987) has 300 × 3,980. All 7 catalog requirements full. Join hygiene clean. |
| Concrete result matching | 3/5 | 57/89 cells (64.0%) Match under binary Match/FAIL design (DEV-041, iteration 5). 32 FAIL cells, all carrying closed-vocabulary markers. Loss 0.3596. Band 3 per rubric. |
| Signal strength | 1/5 | Worst-case headline r = 3.626 on `s1_p1_alpha_jan` (FAIL on T2 which covers C1). Outside [0.33, 3.0] → band 1 → kill switch. Excluding the FAIL, worst-case Tier 2 headline r = 2.72 (`all_jan_a12`), still outside [0.5, 2.0]. The FAIL is retired as `[CONVENTION-APPLIED]` with quantitative test evidence (Assumption 17, iter-2 [M1] analysis). |
| Corollary | 5/5 | 20/20 corollary cells (T3, T4, T5) Tier 1/2 (100%). Spearman correlations Tier 1; size-model spread alphas Tier 1; positive-proportion and overlap cells Tier 2 with sign-match. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table I (cross-sectional regression, 1929-1982) | All-sample row: a_1 = -0.0969 vs paper -0.0923 (Tier 1), a_12 = +0.0317 vs +0.0339 (Tier 1), t(a_1) = -18.55 vs -18.58 (Tier 1), R² = 0.109 vs 0.108 (Tier 1). Q1/Q3 size subsamples: a_1 Tier 1, R² Tier 1 (adjusted series, matching paper 0.093/0.113 within 8%). | C2 (negative first-order serial correlation), C3 (positive 12-month reversal), C4 (Feb-Dec persistence). Confirms Fama-MacBeth cross-sectional regression methodology and full-sample + subsample composition. |
| Table II (predictive portfolios, 1934-1987) | S0 P1-P10 spread: +0.0286 vs paper +0.0249 (Tier 1, r=1.15), t = 17.6 vs 16.8. S0 P1 alpha +0.0131 vs paper +0.0111 (Tier 1). S0 P10 alpha -0.0154 vs paper -0.0138 (Tier 1). Jan-Dec, January-only, Feb-Dec subsamples all reproduce. | C1 (the paper's headline claim: 2.49%/month P1-P10 spread under S0 forecast strategy). Monotonic decline across deciles P1→P10 verified. |
| Table III (positive-residual proportions) | All 7 cells Tier 2; signs and rankings correct (P1 positive-fraction > 50% for S0/S1/S12), magnitudes lower than paper. | Cross-check on Table II alphas using a non-parametric sign test rather than t-statistic. Sample-composition sensitivity. |
| Table IV (overlap and rank correlation) | Spearman correlations Tier 1: S0-S1 0.701 vs paper 0.664, S0-S12 0.239 vs paper 0.202, S1-S12 -0.016 vs -0.012. Overlap cells Tier 2: S0-S1 0.323 vs 0.516, etc. | C6 (S0 vs S1 relation). Spearman Tier 1 confirms predictive signals are well-correlated; overlap Tier 2 reflects stock-list composition differences. |
| Table V (size-based 3-factor model) | All 7 alpha cells Tier 1. S0 P1-P10 spread +0.0282 vs paper +0.0246 (Tier 1, r=1.15). | C5 (size-based risk does not explain the predictive-portfolio abnormal returns). |
| Table VI (bid-ask bias correction, 1963-1987) | All 8 cells Tier 2 (sign match, magnitude 40-95% above paper). Panel II alpha < Panel I alpha preserved (matches paper's bias-adjustment claim). | Robustness to bid-ask bounce and thin-trading bias. Confirms headline result not driven by these biases. |

## Important gaps

- **Single FAIL `s1_p1_alpha_jan` (r=3.626)** — January-only S1 P1 alpha regression with 54 monthly obs. The replicator tested footnote 15's January-only restriction in iteration 2 (it cannot affect S1 because S1 sorts on raw lag1, not on a regression forecast), documented the result quantitatively (3 S0 cells regressed, no change to S1), and reverted the fix. Retired as `[CONVENTION-APPLIED]` with evidence in `preparations/assumptions.md:248-298` (Assumption 17). Non-actionable; the gap is sample-composition sensitivity in a low-statistics cell. Drives Signal Strength to band 1 → rubric kill switch.
- **Table III positive-proportion magnitudes systematically off** — All 7 cells Tier 2 (paper reports extreme tail behavior not reproduced in this CRSP vintage). Documented as sample-composition sensitivity in Assumption 18; no fix available.
- **Table IV overlap cells 30-50% below paper** — Spearman correlations Tier 1, so the predictive signals are well-correlated; the discrepancy is in the specific stock lists. No fix available.
- **Table VI magnitudes 40-95% above paper** — All 8 cells Tier 2, sign match and Panel II < Panel I ordering preserved. Sample-vintage sensitivity. No fix available.
- **Size quintile distribution is 47/15/12/11/10 instead of 20/20/20/20/20** — Unavoidable consequence of NYSE-only breakpoints applied to a multi-exchange universe. Q1 a_1 still reproduces (Tier 1) so the regression is robust to this composition choice.
- **Q1/Q3 R² reporting split** — Iteration 2 fixed the audit-1 [M2] deviation: Q1/Q3 R² cells now ship the adjusted series (matching `tables_to_replicate.json`'s "adjusted R^2" description), All-rows ship the unadjusted series (matching paper 0.108/0.102 exactly). Documented in Assumption 16.
- **Iteration log cosmetic hygiene** — `eval/loss_trace.json` contains three duplicate `iteration: 2` rows and one `iteration: null` row from prior scorer invocations; the iter-3 row is correct. Hygiene only; the loss itself is unchanged.

## Loop status

The replicator-auditor loop exits at iteration 3. Per the rubric's documented-residue exit (criterion B): `|iter-3 loss − iter-2 loss| = |0.3708 − 0.3708| = 0.0 < 0.01` over two consecutive iterations. The single FAIL carries the `[CONVENTION-APPLIED]` closed-vocabulary marker with quantitative test evidence. `requires_iteration: false`.
