# Table 5 — F_SCORE Strategy Returns within Share-Price, Trading-Volume, and Analyst-Following Partitions (One-Year Market-Adjusted)

**5,736 Firm-Year Observations between 1988 and 1996** (paper: 14,043 between 1976 and 1996; restriction per assumptions.md A1). Share-price (Panel A) and trading-volume (Panel B) terciles use PRIOR-fyear full-Compustat cutoffs — the same no-lookahead machinery as the Table 4 size terciles — assigned on the existing frozen panel (it is NOT rebuilt). Groups: All Firms = bucket; Low = F_SCORE in {0,1}; High = F_SCORE in {8,9}. High−Low t-statistics are Welch; median significance is a Wilcoxon rank-sum p.

Definitions (content.md L2524-2526): **share price** = `prcc_f` at the fiscal year-end preceding formation (the panel row's `fyear`); **trading volume** = share turnover = shares traded over the firm's fiscal year ÷ average shares outstanding (`sum(vol)*100 / avg(shrout*1000)` over the 12 month-ends ending at the FY-end — CRSP `vol` is in hundreds of shares in this vintage, verified by spot check; the factor is ranking-invariant for tercile assignment). Price cutoff universe = all standard-filter firms with `prcc_f > 0`; volume cutoff universe = the full linked-Compustat population with turnover available (the MOMENT/ACCRUAL-decile population). Both cutoffs are quantileExact terciles over fyear t−1, applied to fyear t.

Tiers are evaluated on the table_5 contract cells (tables_to_replicate.json): Panel A = 11 cells, Panel B = 8 cells; Panel C (analyst) = 5 cells, all **SKIP** (M2 — see results/table_5_analyst.md). Per the contract `notes`, the paper's values are FULL-PERIOD 1976-1996 references; under the A1 restriction cells are evaluated on **sign + magnitude plausibility**, and counts are Tier 2 (A1 gap).

## Panel A — Share Price (prior-year full-Compustat terciles)

### Small price (price_bucket = 1)

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | 0.1066 | 0.0920 | 0.0146 | Tier 1 |
| All Firms | median | -0.1362 | -0.0950 | -0.0412 | — |
| All Firms | n | 3,230 | 7,250 | -4,020 | Tier 2 (A1 gap) |
| Low Score {0,1} | mean | -0.0413 | -0.0920 | 0.0507 | Tier 1 |
| Low Score {0,1} | median | -0.1951 | — | — | — |
| Low Score {0,1} | n | 122 | — | — | — |
| High Score {8,9} | mean | 0.1177 | 0.1540 | -0.0363 | Tier 1 |
| High Score {8,9} | median | -0.0706 | — | — | — |
| High Score {8,9} | n | 276 | — | — | — |
| High − Low | Δ mean | 0.1590 | 0.2460 | -0.0870 | Tier 1 |
| High − Low | t-stat (Welch) | 1.585 | 4.533 | -2.948 | Tier 2 |
| High − Low | Δ median | 0.1245 | n/r | n/r | — |
| High − Low | median Wilcoxon p | 0.0057 | n/r | n/r | — |
| Bucket share | % of partition | 0.563 | n/r | n/r | — |

### Medium price (price_bucket = 2)

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | 0.0075 | 0.0180 | -0.0105 | Tier 1 |
| All Firms | median | -0.0992 | -0.0460 | -0.0532 | — |
| All Firms | n | 1,729 | 4,493 | -2,764 | — |
| Low Score {0,1} | mean | 0.0031 | -0.0990 | 0.1021 | — |
| Low Score {0,1} | median | -0.1253 | — | — | — |
| Low Score {0,1} | n | 48 | — | — | — |
| High Score {8,9} | mean | 0.0437 | 0.1590 | -0.1153 | — |
| High Score {8,9} | median | -0.0480 | — | — | — |
| High Score {8,9} | n | 169 | — | — | — |
| High − Low | Δ mean | 0.0406 | 0.2580 | -0.2174 | Tier 2 |
| High − Low | t-stat (Welch) | 0.414 | 3.573 | -3.159 | Tier 2 |
| High − Low | Δ median | 0.0773 | n/r | n/r | — |
| High − Low | median Wilcoxon p | 0.4999 | n/r | n/r | — |
| Bucket share | % of partition | 0.301 | n/r | n/r | — |

### Large price (price_bucket = 3)

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | -0.0285 | 0.0650 | -0.0935 | — |
| All Firms | median | -0.0610 | 0.0020 | -0.0630 | — |
| All Firms | n | 777 | 2,300 | -1,523 | — |
| Low Score {0,1} | mean | -0.1704 | -0.1240 | -0.0464 | — |
| Low Score {0,1} | median | -0.3074 | — | — | — |
| Low Score {0,1} | n | 7 | — | — | — |
| High Score {8,9} | mean | -0.0152 | 0.0080 | -0.0232 | — |
| High Score {8,9} | median | -0.0610 | — | — | — |
| High Score {8,9} | n | 101 | — | — | — |
| High − Low | Δ mean | 0.1551 | 0.1320 | 0.0231 | Tier 1 |
| High − Low | t-stat (Welch) | 0.845 | 1.852 | -1.007 | Tier 1 |
| High − Low | Δ median | 0.2464 | n/r | n/r | — |
| High − Low | median Wilcoxon p | 0.2053 | n/r | n/r | — |
| Bucket share | % of partition | 0.135 | n/r | n/r | — |

## Panel B — Trading Volume / Turnover (prior-year linked-Compustat terciles)

### Low volume (volume_bucket = 1)

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | 0.0959 | 0.1010 | -0.0051 | Tier 1 |
| All Firms | median | -0.0937 | -0.0440 | -0.0497 | — |
| All Firms | n | 2,611 | 7,661 | -5,050 | — |
| Low Score {0,1} | mean | -0.1523 | -0.0720 | -0.0803 | Tier 2 |
| Low Score {0,1} | median | -0.2566 | — | — | — |
| Low Score {0,1} | n | 53 | — | — | — |
| High Score {8,9} | mean | 0.0811 | 0.1670 | -0.0859 | Tier 1 |
| High Score {8,9} | median | -0.0689 | — | — | — |
| High Score {8,9} | n | 317 | — | — | — |
| High − Low | Δ mean | 0.2334 | 0.2390 | -0.0056 | Tier 1 |
| High − Low | t-stat (Welch) | 2.437 | 4.417 | -1.980 | Tier 1 |
| High − Low | Δ median | 0.1877 | n/r | n/r | — |
| High − Low | median Wilcoxon p | 0.0012 | n/r | n/r | — |
| Bucket share | % of partition | 0.455 | n/r | n/r | — |

### Medium volume (volume_bucket = 2)

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | 0.0412 | 0.0110 | 0.0302 | — |
| All Firms | median | -0.1077 | -0.0920 | -0.0157 | — |
| All Firms | n | 1,939 | 3,664 | -1,725 | — |
| Low Score {0,1} | mean | -0.0146 | -0.1080 | 0.0934 | — |
| Low Score {0,1} | median | -0.1839 | — | — | — |
| Low Score {0,1} | n | 56 | — | — | — |
| High Score {8,9} | mean | 0.0770 | 0.0670 | 0.0100 | — |
| High Score {8,9} | median | -0.0349 | — | — | — |
| High Score {8,9} | n | 170 | — | — | — |
| High − Low | Δ mean | 0.0916 | 0.1750 | -0.0834 | Tier 1 |
| High − Low | t-stat (Welch) | 0.626 | 2.050 | -1.424 | — |
| High − Low | Δ median | 0.1491 | n/r | n/r | — |
| High − Low | median Wilcoxon p | 0.0322 | n/r | n/r | — |
| Bucket share | % of partition | 0.338 | n/r | n/r | — |

### High volume (volume_bucket = 3)

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | 0.0049 | 0.0280 | -0.0231 | — |
| All Firms | median | -0.1494 | -0.0330 | -0.1164 | — |
| All Firms | n | 1,183 | 2,718 | -1,535 | — |
| Low Score {0,1} | mean | 0.0413 | -0.1490 | 0.1903 | — |
| Low Score {0,1} | median | -0.1121 | — | — | — |
| Low Score {0,1} | n | 68 | — | — | — |
| High Score {8,9} | mean | 0.0022 | 0.0540 | -0.0518 | — |
| High Score {8,9} | median | -0.0508 | — | — | — |
| High Score {8,9} | n | 57 | — | — | — |
| High − Low | Δ mean | -0.0391 | 0.2030 | -0.2421 | FAIL |
| High − Low | t-stat (Welch) | -0.301 | 2.863 | -3.164 | FAIL |
| High − Low | Δ median | 0.0612 | n/r | n/r | — |
| High − Low | median Wilcoxon p | 1.0000 | n/r | n/r | — |
| Bucket share | % of partition | 0.206 | n/r | n/r | — |

¹ **Dropped from Panel B:** 3 panel rows have no prior-fiscal-year turnover (no CRSP trading months in the FY window) and are excluded from the volume partition (Panel B denominator n = 5,733 of 5,736; all 5,736 rows carry a price bucket in Panel A).

## Qualitative claim — positive High−Low spread in ALL six buckets

Paper claim (content.md §4.4.1): the F_SCORE High−Low spread is "statistically and economically significant" in all three share-price buckets and both reported volume buckets — the strategy "is not dependent on purchasing firms with low share prices" or thin trading.

| Partition | Bucket | High−Low (ours) | t (Welch) | Paper H−L | Sign matches? |
|---|---|---:|---:|---:|---|
| Price | Small price | +0.1590 | 1.585 | +0.246 | ✓ positive |
| Price | Medium price | +0.0406 | 0.414 | +0.258 | ✓ positive |
| Price | Large price | +0.1551 | 0.845 | +0.132 | ✓ positive |
| Volume | Low volume | +0.2334 | 2.437 | +0.239 | ✓ positive |
| Volume | Medium volume | +0.0916 | 0.626 | +0.175 | ✓ positive |
| Volume | High volume | -0.0391 | -0.301 | +0.203 | ✗ non-positive |

**Result: FAIL** — the High−Low spread is positive in 3/3 price buckets and 2/3 volume buckets under A1 (paper: all six positive and significant).

## Panel C — Analyst Following (SKIP — IBES feasibility < 60%)

See results/table_5_analyst.md for the feasibility evidence. Reference paper values (content.md L2550) shown for context only; all Panel C contract cells are SKIP.

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| Coverage share | covered / all | SKIP | 0.378 | — | SKIP (IBES coverage < 60% threshold, M2) |
| No following | All mean | SKIP | 0.1010 | — | SKIP (IBES coverage < 60% threshold, M2) |
| No following | High − Low mean | SKIP | 0.2770 | — | SKIP (IBES coverage < 60% threshold, M2) |
| No following | High − Low t | SKIP | 5.298 | — | SKIP (IBES coverage < 60% threshold, M2) |
| With following | High − Low mean | SKIP | 0.1140 | — | SKIP (IBES coverage < 60% threshold, M2) |

## Tally (contract targets in tables_to_replicate.json, + † task text)

| Tier | Count |
|---|---:|
| Tier 1 (match) | 12 |
| Tier 2 (pattern / A1 gap) | 5 |
| FAIL (sign flip / unreachable) | 2 |
| SKIP (year outside restricted sample, A1) | 5 |
| **Total targeted cells** | **19** (+5 SKIP) |

### FAIL cells (diagnosis)

- **Panel B High volume High−Low** (ours -0.0391, t -0.301 vs paper +0.203, t 2.863): the most-traded bucket's spread collapses to ≈ 0 and flips sign under A1 → FAIL on the mean and its t. This is the one bucket where the F_SCORE differentiation does not survive the restricted sub-period; the bucket is the smallest (n = 1,183, 20.6% of the partition) and its Low group mean is slightly positive (+0.041), leaving no left tail for F_SCORE to screen out. The other five buckets keep the paper's positive sign (the low-volume bucket replicates the paper's 0.239 almost exactly: +0.233, Tier 1).

## Interpretation

The price/volume partitions are NEW corollary results computed this iteration on the frozen 5,736-row panel (audit1 [M1]); the paper's values are full-period 1976-1996 references, so under the A1 restriction each cell is read for sign + magnitude plausibility and counts are Tier 2 (A1 gap). The headline qualitative claim — the F_SCORE High−Low spread is positive in every price bucket and every volume bucket — does NOT fully hold under A1 (positive in 3/3 price and 2/3 volume buckets; see the claim table above).

Bucket shares vs the paper (of 14,043; price 51.6/32.0/16.4%, volume 54.6/26.1/19.4%): ours are small/medium/large price 56.3%/30.1%/13.5% and low/medium/high volume 45.5%/33.8%/20.6%. The paper's central point — that ~48% of high-BM firms are NOT in the lowest-price bucket and the strategy is not merely a low-share-price effect — is assessed against these shares and the sign of the high-price-bucket spread.

Panel B excludes 3 panel rows with no prior-fiscal-year turnover (footnote ¹); Panel A retains all 5,736 rows. Panel C (analyst following) is a documented SKIP: only 32.8% of panel firm-years are classifiable on I/B/E/S (1,881 of 5,736), below the 60% threshold — see results/table_5_analyst.md and the assumptions.md entry.
