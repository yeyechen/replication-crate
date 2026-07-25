> **NOTICE (2026-07-25): the binary verdict below is SUPERSEDED.** Corrected investment-first records with accepted/qualified/quarantine statuses live in `training/cases.json`; see `training/README.md`.

---
schema_version: 2
slug: value_investing_f_score
iteration: 2
audit_verdict: PARTIAL
verdict: REPLICATED
overall: 3.17
methodology: 4
headline_matching: 3
data_coverage: 2
concrete_result: 3
signal_strength: 3
corollary: 4
generated_at: 2026-07-23T04:56:00Z
---

# Replication Summary

## Piotroski (2000), "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers Among Value Stocks" (Journal of Accounting Research, Vol. 38)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 3.17 / 5.00
**Audit state:** `PARTIAL`

Piotroski's F_SCORE strategy — nine binary fundamental signals summed to a 0–9 score within the high book-to-market universe — was replicated rule-by-rule and independently re-verified by the auditor from the cached panel and live data. The central econometric claim replicates at Tier 1 (one-year market-adjusted return rises +2.3–3.1% per F_SCORE point vs the paper's stated 2.5–3%, robust to momentum/accrual/equity-offer controls), and the annual strong-minus-weak hedge earns 10.4% vs the paper's own same-period 9.1–9.7% (t = 3.86, positive in 9 of 9 years). This second iteration closed the two audit-1 gaps: the abstract-level share-price partition now replicates (High−Low positive in all three price buckets), and the analyst-coverage partition is a justified, evidence-based SKIP. A binary `REPLICATED` verdict does not mean every number matched: under a user-approved restriction to 1988–1996 (operating cash flow is NULL for all pre-1987 firm-years in the 2026 Compustat vintage), the full-period headline spreads attenuate to 16–45% of the abstract's numbers, consistent with the paper's own same-period evidence rather than a methodology error.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | Every construction traces to a paper passage with citation; the new price/volume partitions reuse the validated prior-year full-Compustat cutoff machinery (no lookahead), the CRSP volume unit fix is verified and ranking-invariant, and the I/B/E/S join was re-derived by the auditor. Deviations (sample restriction, equity-offer source, link broadening, Welch t) are documented and, where testable, empirically validated. |
| Headline matching | 3/5 | Sign and shape of all central claims hold (positive F_SCORE gradient, positive hedge, significant rightward distribution shift, Wilcoxon p = 0.002); magnitudes match the paper's same-period benchmarks within ~15% but sit far below the full-period abstract numbers. |
| Data coverage | 2/5 | 9 of 21 formation years (user-approved, data-forced truncation) and 5,736 firm-years — 41% of the paper's 14,043 but 80% of its same-period 7,205 — from the same Compustat/CRSP sources with a documented vintage difference. |
| Concrete result matching | 3/5 | 77 of 154 evaluated cells Tier 1 (50%); 93% at Tier 1+2 with only 12 FAILs (8%), each diagnosed and independently verified. The strict-Tier-1 shortfall is driven by count cells structurally unreachable under the documented sample restriction. |
| Signal strength | 3/5 | The signal is real and significant (hedge t = 3.86; regression t = 2.7–3.6) and matches the paper's same-period magnitude (ratio 1.07–1.15), but only 16–45% of the full-period headline spreads. |
| Corollary | 4/5 | Most corollaries replicate: time-series (9/9 positive years), Table 7 controls (zero FAILs), two-year horizon, size direction, and — new this iteration — the share-price partition (positive in all three buckets) and the low-volume bucket (+0.233 ≈ paper 0.239, Tier 1). Two well-explained deviations: the high-volume bucket's sign flip (verified A1 sample-thinning) and the RANK_SCORE null; plus one justified data-gap SKIP (analyst coverage, 32.8% < 60%). |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 1 (descriptives) | All-firm one-year market-adjusted mean 0.058 ≈ paper 0.059; signal positive-proportions within 0.06 on eight of nine signals | Universe construction, the nine signal definitions, and the return machinery are faithful |
| Table 2 (correlations) | 10 of 13 Spearman targets Tier 1; all eight F_SCORE–signal correlations within 16% of the paper | Each binary's definition and sign convention, independent of returns |
| Table 3 (returns by score) | Positive gradient through score 6 with a 7–9 plateau; High−Low 0.105 (same sign, 45% of the paper's 0.230); distributional shift significant (Wilcoxon p = 0.002) | The core result holds in direction and distribution, attenuated in mean magnitude by the restricted sample |
| Table 4 (size partitions) | Bucket shares 58.6/28.4/13.0% vs paper 59.1/27.8/13.1%; High−Low positive in all three buckets, strongest among small firms | The "benefits concentrated in small firms" claim holds in direction |
| Table 5 (price / volume / analyst) | High−Low positive in all three price buckets (+0.159/+0.041/+0.155); low-volume bucket +0.233 ≈ paper 0.239 (Tier 1); high-volume flips sign (−0.039, diagnosed); analyst panel SKIP (32.8% I/B/E/S coverage) | The abstract claim "not dependent on purchasing firms with low share prices" replicates; the thin-trading claim holds in 2 of 3 volume buckets |
| Appendix A (annual hedge) | Average strong-minus-weak spread 0.104 vs paper 0.091–0.097 (Tier 1), t = 3.86, positive in 9 of 9 years; same-period benchmark now printed in the artifact | Time-series robustness — the strongest single piece of evidence |
| Table 7 (regressions) | F_SCORE coefficient 0.0276 (pooled) / 0.0313 (annual average) vs paper 0.027–0.031, zero FAIL cells; controls keep the paper's signs | The central econometric claim — ~2.5–3% per signal point — replicates at Tier 1 |

## Important gaps

- **Sample restriction (non-actionable):** 9 of 21 formation years and 80% of the paper's same-period universe — forced by a verified data-vintage gap (operating cash flow NULL pre-1987), user-approved. All full-period headline magnitudes (the abstract's "7.5% annually", the 23% long-short return) are unreachable by construction; the same-period comparison (hedge 0.104 vs 0.091) is the valid benchmark and it replicates.
- **High-volume bucket sign flip (non-actionable):** the most-traded bucket's High−Low collapses to −0.039 (paper +0.203) because the restricted sample's low-score group there is mildly positive (+0.041), leaving no left tail to screen — verified from the raw data; the other five buckets keep the paper's sign.
- **Mean-significance attenuation (non-actionable):** the High−Low mean spread is not t-significant in the 9-year sample (Welch 1.49 vs paper 5.59); significance survives in the median test and the annual hedge.
- **RANK_SCORE robustness check (non-actionable):** the continuous-signal alternative (Table 3 Panel D) is null under three pre-tested ranking variants, consistent with the paper's own footnote-12 caveat.
- **Analyst-coverage partition (non-actionable data gap):** I/B/E/S summary coverage classifies only 32.8% of 1988–1996 panel firm-years (below the 60% feasibility threshold), with no reliable way to separate unmatched firms from genuinely uncovered ones — the paper's covered-vs-uncovered contrast (0.114 vs 0.277) is unverifiable on this vintage.
- **Quarterly earnings-announcement corollary (out of contract):** the abstract's announcement-return claim (Table 8) needs Compustat quarterly tape and daily announcement-window returns not present in the catalog; never committed and not computable here.
