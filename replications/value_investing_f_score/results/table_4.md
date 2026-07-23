# Table 4 — F_SCORE Strategy Returns within Size Partitions (One-Year Market-Adjusted)

**5,736 Firm-Year Observations between 1988 and 1996** (paper: 14,043 between 1976 and 1996; restriction per assumptions.md A1). Size buckets 1/2/3 = Small/Medium/Large terciles from the full-Compustat prior-year MVE distribution (already assigned on the panel). Bucket counts: small 3,363 / medium 1,630 / large 743 (paper 8,302 / 3,906 / 1,835). Groups: All Firms = bucket; Low = F_SCORE in {0,1}; High = F_SCORE in {8,9}. Mean-difference t-statistics are Welch; median-difference significance is a Wilcoxon rank-sum p.

Tiers are evaluated only on the contract cells (tables_to_replicate.json `table_4`: bucket n's, All/Low/High means, High−Low mean + t per bucket). High−All differences are shown against the paper's values for context but carry no contract entry (no tolerance defined) → Tier "—", not tallied. Per-score rows are ours only (not parsed from the paper) and are informational.

## Small-cap portfolio (size_bucket = 1)

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | 0.1103 | 0.0910 | 0.0193 | Tier 1 |
| All Firms | median | -0.1202 | — | — | — |
| All Firms | n | 3,363 | 8,302 | -4,939 | Tier 2 (A1 gap) |
| Score 0 | mean | -0.1519 | — | — | — |
| Score 0 | n | 15 | — | — | — |
| Score 1 | mean | -0.0558 | — | — | — |
| Score 1 | n | 104 | — | — | — |
| Score 2 | mean | -0.0385 | — | — | — |
| Score 2 | n | 266 | — | — | — |
| Score 3 | mean | 0.0181 | — | — | — |
| Score 3 | n | 472 | — | — | — |
| Score 4 | mean | 0.0473 | — | — | — |
| Score 4 | n | 590 | — | — | — |
| Score 5 | mean | 0.1402 | — | — | — |
| Score 5 | n | 636 | — | — | — |
| Score 6 | mean | 0.2851 | — | — | — |
| Score 6 | n | 555 | — | — | — |
| Score 7 | mean | 0.1924 | — | — | — |
| Score 7 | n | 405 | — | — | — |
| Score 8 | mean | 0.0900 | — | — | — |
| Score 8 | n | 230 | — | — | — |
| Score 9 | mean | 0.0760 | — | — | — |
| Score 9 | n | 90 | — | — | — |
| Low Score {0,1} | mean | -0.0679 | -0.0910 | 0.0231 | Tier 1 |
| Low Score {0,1} | median | -0.1754 | — | — | — |
| Low Score {0,1} | n | 119 | 266 | -147 | — |
| High Score {8,9} | mean | 0.0860 | 0.1790 | -0.0930 | Tier 1 |
| High Score {8,9} | median | -0.0810 | — | — | — |
| High Score {8,9} | n | 320 | 895 | -575 | — |
| High − All | Δ mean | -0.0243 | 0.0880 | -0.1123 | — |
| High − All | mean t-stat (Welch) | -0.472 | 2.456 | -2.928 | — |
| High − All | Δ median | 0.0392 | n/r | n/r | — |
| High − All | median Wilcoxon p | 0.0894 | n/r | n/r | — |
| High − Low | Δ mean | 0.1539 | 0.2700 | -0.1161 | Tier 2 |
| High − Low | mean t-stat (Welch) | 1.689 | 4.709 | -3.020 | Tier 2 |
| High − Low | Δ median | 0.0945 | n/r | n/r | — |
| High − Low | median Wilcoxon p | 0.0065 | n/r | n/r | — |

## Medium-cap portfolio (size_bucket = 2)

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | -0.0138 | 0.0080 | -0.0218 | FAIL |
| All Firms | median | -0.1138 | — | — | — |
| All Firms | n | 1,630 | 3,906 | -2,276 | Tier 2 (A1 gap) |
| Score 0 | mean | -0.3803 | — | — | — |
| Score 0 | n | 5 | — | — | — |
| Score 1 | mean | 0.0849 | — | — | — |
| Score 1 | n | 42 | — | — | — |
| Score 2 | mean | -0.1220 | — | — | — |
| Score 2 | n | 97 | — | — | — |
| Score 3 | mean | -0.0276 | — | — | — |
| Score 3 | n | 194 | — | — | — |
| Score 4 | mean | -0.0400 | — | — | — |
| Score 4 | n | 286 | — | — | — |
| Score 5 | mean | 0.0184 | — | — | — |
| Score 5 | n | 340 | — | — | — |
| Score 6 | mean | 0.0016 | — | — | — |
| Score 6 | n | 287 | — | — | — |
| Score 7 | mean | -0.0403 | — | — | — |
| Score 7 | n | 222 | — | — | — |
| Score 8 | mean | 0.0636 | — | — | — |
| Score 8 | n | 123 | — | — | — |
| Score 9 | mean | -0.0356 | — | — | — |
| Score 9 | n | 34 | — | — | — |
| Low Score {0,1} | mean | 0.0354 | -0.0940 | 0.1294 | FAIL |
| Low Score {0,1} | median | -0.2132 | — | — | — |
| Low Score {0,1} | n | 47 | 96 | -49 | — |
| High Score {8,9} | mean | 0.0421 | 0.0790 | -0.0369 | Tier 1 |
| High Score {8,9} | median | -0.0216 | — | — | — |
| High Score {8,9} | n | 157 | 392 | -235 | — |
| High − All | Δ mean | 0.0559 | 0.0710 | -0.0151 | — |
| High − All | mean t-stat (Welch) | 1.155 | 2.870 | -1.715 | — |
| High − All | Δ median | 0.0922 | n/r | n/r | — |
| High − All | median Wilcoxon p | 0.0723 | n/r | n/r | — |
| High − Low | Δ mean | 0.0067 | 0.1730 | -0.1663 | Tier 2 |
| High − Low | mean t-stat (Welch) | 0.051 | 2.870 | -2.819 | Tier 2 |
| High − Low | Δ median | 0.1916 | n/r | n/r | — |
| High − Low | median Wilcoxon p | 0.2363 | n/r | n/r | — |

## Large-cap portfolio (size_bucket = 3)

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | -0.0178 | 0.0030 | -0.0208 | FAIL |
| All Firms | median | -0.0583 | — | — | — |
| All Firms | n | 743 | 1,835 | -1,092 | Tier 2 (A1 gap) |
| Score 0 | mean | -0.7794 | — | — | — |
| Score 0 | n | 1 | — | — | — |
| Score 1 | mean | 0.1107 | — | — | — |
| Score 1 | n | 10 | — | — | — |
| Score 2 | mean | -0.1512 | — | — | — |
| Score 2 | n | 29 | — | — | — |
| Score 3 | mean | -0.0042 | — | — | — |
| Score 3 | n | 77 | — | — | — |
| Score 4 | mean | 0.0235 | — | — | — |
| Score 4 | n | 127 | — | — | — |
| Score 5 | mean | -0.0133 | — | — | — |
| Score 5 | n | 159 | — | — | — |
| Score 6 | mean | -0.0322 | — | — | — |
| Score 6 | n | 151 | — | — | — |
| Score 7 | mean | -0.0753 | — | — | — |
| Score 7 | n | 120 | — | — | — |
| Score 8 | mean | 0.0378 | — | — | — |
| Score 8 | n | 52 | — | — | — |
| Score 9 | mean | 0.1297 | — | — | — |
| Score 9 | n | 17 | — | — | — |
| Low Score {0,1} | mean | 0.0298 | -0.1320 | 0.1618 | FAIL |
| Low Score {0,1} | median | 0.0965 | — | — | — |
| Low Score {0,1} | n | 11 | 34 | -23 | — |
| High Score {8,9} | mean | 0.0604 | 0.0200 | 0.0404 | Tier 2 |
| High Score {8,9} | median | -0.0422 | — | — | — |
| High Score {8,9} | n | 69 | 161 | -92 | — |
| High − All | Δ mean | 0.0783 | 0.0170 | 0.0613 | — |
| High − All | mean t-stat (Welch) | 1.393 | 0.872 | 0.521 | — |
| High − All | Δ median | 0.0161 | n/r | n/r | — |
| High − All | median Wilcoxon p | 0.3277 | n/r | n/r | — |
| High − Low | Δ mean | 0.0306 | 0.1520 | -0.1214 | Tier 2 |
| High − Low | mean t-stat (Welch) | 0.144 | 1.884 | -1.740 | Tier 2 |
| High − Low | Δ median | -0.1388 | n/r | n/r | — |
| High − Low | median Wilcoxon p | 0.9610 | n/r | n/r | — |

## Tally (contract targets in tables_to_replicate.json only)

| Tier | Count |
|---|---:|
| Tier 1 (match) | 4 |
| Tier 2 (pattern / A1 gap) | 10 |
| FAIL (sign flip / unreachable) | 4 |
| **Total targeted cells** | **18** |

### FAIL cells (diagnosis)

- **All-mean Medium** (ours -0.0138 vs paper +0.008) and **All-mean Large** (-0.0178 vs +0.003): sign flips on means the paper itself reports as ≈ 0 (±0.02 either way) — a sign-of-a-near-zero-mean artifact of the truncated sub-period, not a directional error.
- **Low-mean Medium** (+0.0354 vs −0.094) and **Low-mean Large** (+0.0298 vs −0.132): sign flips on groups of 47 and 11 observations (paper 96 / 34), where a few vintage outliers move the group mean; the paper's sign is kept in the one bucket with a sizeable Low group (small: -0.0679 vs −0.091, Tier 1).

## Interpretation

The size partition keeps the paper's shape at A1-thinned counts — 3,363 / 1,630 / 743 vs 8,302 / 3,906 / 1,835 (all Tier 2, A1 gap; each ≥ 30% of the paper count), with the same 59/28/13% tercile shares. The High portfolio is positive in every bucket (0.086 / 0.042 / 0.060 vs 0.179 / 0.079 / 0.020; Tier 1 in small and medium), and the High−Low spread keeps the paper's positive sign in all three: 0.154 (t 1.69) / 0.007 (t 0.05) / 0.031 (t 0.14) vs 0.270 (4.709) / 0.173 (2.870) / 0.152 (1.884).

The paper's central cross-sectional claim — the strategy works in small/medium firms, differentiation is weak among the largest — holds directionally (small spread 0.154 > large 0.031; the small-cap distributional separation is significant on the Wilcoxon test, p = 0.0065), but the medium/large mean spreads collapse toward zero and no bucket's mean spread is t-significant here. The four FAILs are all sign flips of near-zero or tiny-n group means (diagnosed above), not of the strategy spreads. No spin: the small-cap 0.270 (t 4.709) headline is NOT reproduced; the restricted sample delivers roughly half the spread at a third of the significance.
