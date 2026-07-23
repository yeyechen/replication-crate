---
schema_version: 2
slug: seasonality_international_evidence
iteration: 2
audit_verdict: PARTIAL
verdict: REPLICATED
overall: 3.33
methodology: 4
headline_matching: 3
data_coverage: 3
concrete_result: 3
signal_strength: 3
corollary: 4
generated_at: 2026-07-22T18:58:00Z
---

# Replication Summary

## Seasonality in the Cross Section of Stock Returns: The International Evidence (Heston & Sadka 2010, JFQA)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 3.33 / 5.00
**Audit state:** `PARTIAL`

The paper's central claim — decile spreads formed on annual-lag returns
outperform nonannual-lag spreads by over 1% per month at Years 2–5 across
14 non-U.S. markets — replicates with the correct sign, shape, and
significance (Years 2–3 difference +1.35%/mo, t 4.59, against the paper's
+1.80%, t 8.25), alongside strong lag-1 reversal, long-horizon reversals
at near-paper magnitudes, positive Year-2-3 differences in all 14
countries, and — newly added this iteration — calendar-month, size-group,
cross-country-correlation, and bin-count robustness, all verified
bit-exactly by the auditor against the cached data. Year-1 momentum flips
sign and the annual-only strategies are attenuated, traced to the
Compustat-for-FactSet universe substitution and deliberately left
un-"fixed" (adopting the filter that restores them would be
tweaking-to-fit). A binary `REPLICATED` verdict does not mean every cell
matched: under the audit rubric's strict 2× rule, 57% of the 1,613
committed cells are Tier 1 or 2.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | Every construction choice (FWL regressions, lag sets, EW/VW deciles, intra/inter decomposition, calendar/size/correlation/bin-count mechanics) matches the paper; the auditor's independent from-scratch reimplementation of 40+ cells across all eight tables matched to machine precision. Data substitution and the WLS-weight convention are documented deviations, not bugs. |
| Headline matching | 3/5 | The annual-vs-nonannual difference — the paper's headline — replicates at 66–75% of paper magnitude with full significance; lag-1 reversal replicates in sign. Year-1 momentum flips sign (documented, root-caused). |
| Data coverage | 3/5 | Sample starts 1986 instead of 1985 (the substitute source's vintage limit); 80% of the paper's firm-months, 109% of its firms; one fully documented data-source substitution after every alternative was verified unavailable. |
| Concrete result matching | 3/5 | 613/1,613 cells Tier 1 (38%), 912/1,613 Tier 1+2 (57%) under the strict rubric rule; 82% sign-consistent under repo rules — both schemes now reported transparently by committed, anchor-asserting code. FAILs concentrate in Year-1 rows, weak annual rows, and thin small-market cells. |
| Signal strength | 3/5 | Headline difference and long-horizon cells sit at 0.66–1.11× the paper (inside the [0.5, 2] band); the Year-1 flip is excluded from the headline set per the paper's own framing. |
| Corollary | 4/5 | All six computable corollaries now computed and verified: not-a-January effect, size-group persistence, low and horizon-declining cross-country correlations, quintile/tricile sign robustness, intracountry dominance, 14/14 country breadth. Liquidity subsamples and risk-factor alphas remain blocked by unavailable data (documented). |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 1 (summary stats) | Country size ordering replicates (Japan/UK/Canada largest; Austria smallest within 2%); firm-months at 80% of the paper | Universe construction, country assignment, panel assembly |
| Table 2 (return responses) | Lag-1 reversal in all four samples (Japan within 11%); positive responses at annual lags 12–60 | Cross-sectional regression machinery, lag structure |
| Table 3 (decile spreads) | Years 2–5 annual-minus-nonannual differences significant (+1.35%/mo t 4.59; +0.67%/mo t 2.67); long-horizon reversals within 6% of the paper; intra/inter additivity exact | The paper's central claim and the intra/inter decomposition |
| Table 7 (per-country) | Years 2–3 difference positive in 14/14 countries; Japan and the UK near-exact | Cross-country breadth, not a single-market effect |
| Table 4 (calendar months) | Nonannual reversal negative in 11/12 months; Feb–Dec difference +1.13%/mo (t 3.77) vs paper +1.55% (7.12) | "Not a January effect" corollary |
| Table 5 (size groups) | Years 2–3 difference positive in all six 30/40/30 size columns; Years 4–5 annual inter-large near-exact (+0.0030 vs +0.0031) | Size-independence of the pattern |
| Table 11 (correlations) | Mean pairwise strategy correlation +0.11 / +0.05 / +0.02, declining with horizon | "Strategies are not highly correlated across countries" (abstract) |
| Table 12 (bin counts) | 11/12 rows keep the decile signs at quintile and tricile granularity; long-horizon spreads within ±15% | Robustness to portfolio granularity |
| Year-1 sensitivity battery | Committed code: trimming Canadian microcaps moves the Year-1 spread from −0.53% toward the paper's +1.21% — diagnosis confirmed, filter deliberately not adopted | The Year-1 failure is universe composition, not methodology |

## Important gaps

- **Year-1 momentum flips sign** (−0.53%/mo vs the paper's +1.21%): traced
  to Canadian TSX-V penny-stock contamination of the Compustat universe;
  restoring it would require an unpapered microcap filter, which the
  replication declines to apply (documented, with a committed sensitivity
  trail).
- **Annual-only strategy magnitudes are attenuated** across every table —
  the systematic signature of the Compustat-vs-FactSet universe
  difference; the annual-minus-nonannual differences are unaffected.
- **Table 6 (liquidity subsamples)** not computed — the panel lacks price
  and volume fields (documented deferral; actionable only with a panel
  rebuild).
- **Tables 8–10 (risk-factor alphas)** not computable — French's bespoke
  international BM/EP/CEP/DP factors are not in the data catalog
  (external data limitation, non-actionable).
- **43% rubric-FAIL cell rate** is driven by the universe substitution,
  not by methodology; it cannot improve without the paper's proprietary
  FactSet vintage.
