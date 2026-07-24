---
schema_version: 2
slug: the_other_side_of_value
iteration: 1
audit_verdict: PARTIAL
verdict: REPLICATED
overall: 4.17
methodology: 4
headline_matching: 5
data_coverage: 4
concrete_result: 4
signal_strength: 5
corollary: 3
generated_at: 2026-07-22T00:00:00Z
---

# Replication Summary

## The Other Side of Value: The Gross Profitability Premium (Novy-Marx 2013, JFE)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 4.17 / 5.00
**Audit state:** `PARTIAL`

The paper's central claim — that profitable firms (high gross-profits-to-assets) earn significantly higher returns than unprofitable firms despite being growth stocks — reproduces cleanly. The High-minus-Low GP/A quintile spread is 0.32%/month (t = 2.51) with a Fama-French three-factor alpha of 0.54%/month (t = 4.58) and a large negative HML loading (−0.45), all within ~5% of the paper. The result was independently recomputed during the legacy audit and freshly replayed on 2026-07-23 after fixing the total-loss return filter; restoring 274 valid −100% stock-month returns left the committed core table unchanged at every reported digit. The repository does not commit its generated cache, so replay still requires source-database access and the shared `rep-it-up` utilities. A binary `REPLICATED` verdict means the headline is faithful; it does not imply every committed table matched — three of four committed tables (the Fama-MacBeth regressions, the profitability×value double sorts, and the Fortune-500 strategy) remain for a later iteration.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | Signal, book equity, 6-month-lagged B/M, NYSE-breakpoint quintile sorts, June-rebalanced value-weighting, and FF3 time-series inference all follow the paper; the subtle choices (prior-month VW weights, July-row formation) are correct and documented. One data-forced substitution (PSTX→PSTK) keeps it off a perfect score. |
| Headline matching | 5/5 | H-L spread, FF3 alpha, negative HML loading, and the full quintile return shape (including the paper's Q3>Q4 dip) all match within ~5%. |
| Data coverage | 4/5 | Exact sample (Jul 1963–Dec 2010, 570 months); same CRSP/Compustat/CCM/FF sources; universe ~11–13% smaller per quintile than the paper, consistent with a newer Compustat vintage. |
| Concrete result matching | 4/5 | Table 2 Panel A is 90.9% Tier 1 (50/55 cells, 0 wrong-sign); Panel B is reported but not formally tiered and carries one out-of-bound near-zero cell, pulling the all-cell fraction into the 70–90% band. |
| Signal strength | 5/5 | Both headline cells (spread and alpha) sit at 1.02–1.04× the paper's values. |
| Corollary | 3/5 | The growth-strategy nature (negative HML), alpha exceeding the raw spread, and the value premium all replicate; but the paper's complementarity thesis (double sorts), the Fortune-500 strategy, the FM regressions, size, and international tests are not yet computed. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 2, Panel A (GP/A sorts) | H-L spread 0.32 [2.51] vs paper 0.31 [2.49]; alpha 0.54 [4.58] vs 0.52 [4.49]; HML −0.45 vs −0.44; quintile returns track the paper's profile almost exactly. | GP/A signal construction, non-financial universe, fiscal-year→month timing, NYSE-breakpoint VW sorting, and the headline gross-profitability premium. |
| Table 2, Panel B (B/M sorts) | Value spread H-L 0.38%/mo with HML loading 1.14 (paper 0.41, 0.91); returns rise monotonically low→high B/M. | The benchmark value premium and the B/M construction with 6-month-lagged market equity. |
| Portfolio characteristics | Low-quintile GP/A 0.10 and High 0.71 match the paper; high-GP/A firms have low B/M (0.27) and negative HML loading. | Profitability is a growth strategy that hedges value — the qualitative mechanism behind the paper's thesis. |

## Important gaps

- Tables 1 (Fama-MacBeth regressions), 6 (GP/A × B/M double sorts — the paper's central complementarity claim), and 7 (Fortune-500 combined strategy) were committed but not yet replicated; they are the main reason the audit state is `PARTIAL`. All are actionable next iteration — the panel already contains every required column.
- Universe runs ~11–13% below the paper's per-quintile firm counts, attributed to a newer Compustat vintage (comp_202601); this is a data-fidelity limitation rather than a methodology error and does not move the headline.
- The mid-quintile B/M characteristic profile is flatter than the paper's (Q3 0.58 vs 1.00), the largest single-cell deviation; it is a characteristic, not a return, and does not affect the premium.
