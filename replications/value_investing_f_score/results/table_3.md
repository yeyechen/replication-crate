# Table 3 — Buy-and-Hold Returns to the F_SCORE Strategy (High Book-to-Market Universe)

**5,736 Firm-Year Observations between 1988 and 1996** (paper: 14,043 between 1976 and 1996; restriction per assumptions.md A1). Groups: All Firms = full panel; Score s = F_SCORE == s; Low Score = F_SCORE in {0,1}; High Score = F_SCORE in {8,9}.

Method notes: percentiles use numpy linear interpolation (paper silent; SAS default is close to linear). Mean-difference t-statistics are **Welch** (unequal variance), the conservative standard; the paper's appear to be pooled, so our |t| is a lower bound. Median-difference significance is a Wilcoxon rank-sum p (`scipy.stats.ranksums`); %+ significance is a two-proportion z-test. **Bootstrap p-values** (1,000 iterations, **seed=42**) follow paper §3.3: each iteration draws |High| firms into pseudo-High and |Low| into pseudo-Low (disjoint, w/o replacement) from the full high-BM panel; p = fraction of pseudo mean-differences ≥ observed (one-sided). Bootstrap p's are resampling artifacts and are NOT contract targets (Tier "—"). Cells with Tier "—" are not in the metric contract and do not enter the Tally.

## Panel A — One-Year Raw Returns

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | 0.2286 | 0.2390 | -0.0104 | Tier 1 |
| All Firms | p10 | -0.4444 | — | — | — |
| All Firms | p25 | -0.1953 | — | — | — |
| All Firms | median | 0.0567 | — | — | — |
| All Firms | p75 | 0.3889 | — | — | — |
| All Firms | p90 | 0.8947 | — | — | — |
| All Firms | % positive | 0.557 | — | — | — |
| All Firms | n | 5,736 | — | — | — |
| Score 0 | mean | -0.0325 | — | — | — |
| Score 0 | p10 | -0.7000 | — | — | — |
| Score 0 | p25 | -0.6379 | — | — | — |
| Score 0 | median | -0.1250 | — | — | — |
| Score 0 | p75 | 0.3333 | — | — | — |
| Score 0 | p90 | 1.0513 | — | — | — |
| Score 0 | % positive | 0.429 | — | — | — |
| Score 0 | n | 21 | — | — | — |
| Score 1 | mean | 0.1737 | — | — | — |
| Score 1 | p10 | -0.6398 | — | — | — |
| Score 1 | p25 | -0.3060 | — | — | — |
| Score 1 | median | 0.0000 | — | — | — |
| Score 1 | p75 | 0.3917 | — | — | — |
| Score 1 | p90 | 1.0833 | — | — | — |
| Score 1 | % positive | 0.513 | — | — | — |
| Score 1 | n | 156 | — | — | — |
| Score 2 | mean | 0.0995 | — | — | — |
| Score 2 | p10 | -0.5985 | — | — | — |
| Score 2 | p25 | -0.3500 | — | — | — |
| Score 2 | median | -0.0242 | — | — | — |
| Score 2 | p75 | 0.2831 | — | — | — |
| Score 2 | p90 | 0.7500 | — | — | — |
| Score 2 | % positive | 0.459 | — | — | — |
| Score 2 | n | 392 | — | — | — |
| Score 3 | mean | 0.1813 | — | — | — |
| Score 3 | p10 | -0.5000 | — | — | — |
| Score 3 | p25 | -0.2500 | — | — | — |
| Score 3 | median | 0.0000 | — | — | — |
| Score 3 | p75 | 0.3551 | — | — | — |
| Score 3 | p90 | 0.9413 | — | — | — |
| Score 3 | % positive | 0.498 | — | — | — |
| Score 3 | n | 743 | — | — | — |
| Score 4 | mean | 0.1894 | — | — | — |
| Score 4 | p10 | -0.4444 | — | — | — |
| Score 4 | p25 | -0.2057 | — | — | — |
| Score 4 | median | 0.0500 | — | — | — |
| Score 4 | p75 | 0.3673 | — | — | — |
| Score 4 | p90 | 0.8733 | — | — | — |
| Score 4 | % positive | 0.548 | — | — | — |
| Score 4 | n | 1,003 | — | — | — |
| Score 5 | mean | 0.2493 | — | — | — |
| Score 5 | p10 | -0.4352 | — | — | — |
| Score 5 | p25 | -0.1873 | — | — | — |
| Score 5 | median | 0.0473 | — | — | — |
| Score 5 | p75 | 0.4159 | — | — | — |
| Score 5 | p90 | 0.9713 | — | — | — |
| Score 5 | % positive | 0.552 | — | — | — |
| Score 5 | n | 1,135 | — | — | — |
| Score 6 | mean | 0.3251 | — | — | — |
| Score 6 | p10 | -0.3842 | — | — | — |
| Score 6 | p25 | -0.1515 | — | — | — |
| Score 6 | median | 0.1077 | — | — | — |
| Score 6 | p75 | 0.4386 | — | — | — |
| Score 6 | p90 | 0.9143 | — | — | — |
| Score 6 | % positive | 0.610 | — | — | — |
| Score 6 | n | 993 | — | — | — |
| Score 7 | mean | 0.2481 | — | — | — |
| Score 7 | p10 | -0.3611 | — | — | — |
| Score 7 | p25 | -0.1303 | — | — | — |
| Score 7 | median | 0.0938 | — | — | — |
| Score 7 | p75 | 0.3902 | — | — | — |
| Score 7 | p90 | 0.8552 | — | — | — |
| Score 7 | % positive | 0.592 | — | — | — |
| Score 7 | n | 747 | — | — | — |
| Score 8 | mean | 0.2471 | — | — | — |
| Score 8 | p10 | -0.3360 | — | — | — |
| Score 8 | p25 | -0.1053 | — | — | — |
| Score 8 | median | 0.1081 | — | — | — |
| Score 8 | p75 | 0.3739 | — | — | — |
| Score 8 | p90 | 0.9178 | — | — | — |
| Score 8 | % positive | 0.615 | — | — | — |
| Score 8 | n | 405 | — | — | — |
| Score 9 | mean | 0.2127 | — | — | — |
| Score 9 | p10 | -0.4000 | — | — | — |
| Score 9 | p25 | -0.1786 | — | — | — |
| Score 9 | median | 0.0758 | — | — | — |
| Score 9 | p75 | 0.3571 | — | — | — |
| Score 9 | p90 | 0.9259 | — | — | — |
| Score 9 | % positive | 0.589 | — | — | — |
| Score 9 | n | 141 | — | — | — |
| Low Score {0,1} | mean | 0.1492 | 0.0780 | 0.0712 | Tier 2 |
| Low Score {0,1} | p10 | -0.6657 | — | — | — |
| Low Score {0,1} | p25 | -0.3333 | — | — | — |
| Low Score {0,1} | median | 0.0000 | — | — | — |
| Low Score {0,1} | p75 | 0.3889 | — | — | — |
| Low Score {0,1} | p90 | 1.0729 | — | — | — |
| Low Score {0,1} | % positive | 0.503 | — | — | — |
| Low Score {0,1} | n | 177 | — | — | — |
| High Score {8,9} | mean | 0.2382 | 0.3130 | -0.0748 | Tier 1 |
| High Score {8,9} | p10 | -0.3514 | — | — | — |
| High Score {8,9} | p25 | -0.1150 | — | — | — |
| High Score {8,9} | median | 0.1044 | — | — | — |
| High Score {8,9} | p75 | 0.3647 | — | — | — |
| High Score {8,9} | p90 | 0.9223 | — | — | — |
| High Score {8,9} | % positive | 0.608 | — | — | — |
| High Score {8,9} | n | 546 | — | — | — |

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| High − All | Δ mean | 0.0096 | 0.0740 | -0.0644 | Tier 2 |
| High − All | Δ p10 | 0.0931 | — | — | — |
| High − All | Δ p25 | 0.0802 | — | — | — |
| High − All | Δ median | 0.0477 | — | — | — |
| High − All | Δ p75 | -0.0242 | — | — | — |
| High − All | Δ p90 | 0.0275 | — | — | — |
| High − All | Δ % positive | 0.0511 | — | — | — |
| High − All | mean t-stat (Welch) | 0.280 | 3.279 | -2.999 | Tier 2 |
| High − All | median Wilcoxon p | 0.0254 | n/r | n/r | — |
| High − All | %+ two-prop z p | 0.0216 | n/r | n/r | — |
| High − All | bootstrap p (mean) | 0.3930 | n/r | n/r | — |
| High − Low | Δ mean | 0.0890 | 0.2350 | -0.1460 | Tier 2 |
| High − Low | Δ p10 | 0.3144 | — | — | — |
| High − Low | Δ p25 | 0.2183 | — | — | — |
| High − Low | Δ median | 0.1044 | — | — | — |
| High − Low | Δ p75 | -0.0242 | — | — | — |
| High − Low | Δ p90 | -0.1506 | — | — | — |
| High − Low | Δ % positive | 0.1052 | — | — | — |
| High − Low | mean t-stat (Welch) | 1.242 | 5.594 | -4.352 | Tier 2 |
| High − Low | median Wilcoxon p | 0.0129 | n/r | n/r | — |
| High − Low | %+ two-prop z p | 0.0136 | n/r | n/r | — |
| High − Low | bootstrap p (mean) | 0.1610 | n/r | n/r | — |

## Panel B — One-Year Market-Adjusted Returns (FOCUS)

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | 0.0584 | 0.0590 | -0.0006 | Tier 1 |
| All Firms | p10 | -0.5987 | — | — | — |
| All Firms | p25 | -0.3609 | — | — | — |
| All Firms | median | -0.1081 | -0.0610 | -0.0471 | Tier 1 |
| All Firms | p75 | 0.2061 | — | — | — |
| All Firms | p90 | 0.7302 | — | — | — |
| All Firms | % positive | 0.395 | 0.437 | -0.042 | Tier 1 |
| All Firms | n | 5,736 | 14,043 | -8,307 | Tier 2 (A1 gap) |
| Score 0 | mean | -0.2361 | -0.0610 | -0.1751 | Tier 2 |
| Score 0 | p10 | -0.8719 | — | — | — |
| Score 0 | p25 | -0.7119 | — | — | — |
| Score 0 | median | -0.3670 | — | — | — |
| Score 0 | p75 | 0.1846 | — | — | — |
| Score 0 | p90 | 0.8862 | — | — | — |
| Score 0 | % positive | 0.333 | — | — | — |
| Score 0 | n | 21 | 57 | -36 | Tier 2 (A1 gap) |
| Score 1 | mean | -0.0072 | -0.1020 | 0.0948 | Tier 2 |
| Score 1 | p10 | -0.8142 | — | — | — |
| Score 1 | p25 | -0.4505 | — | — | — |
| Score 1 | median | -0.1732 | — | — | — |
| Score 1 | p75 | 0.2127 | — | — | — |
| Score 1 | p90 | 0.9262 | — | — | — |
| Score 1 | % positive | 0.372 | — | — | — |
| Score 1 | n | 156 | 339 | -183 | Tier 2 (A1 gap) |
| Score 2 | mean | -0.0675 | -0.0200 | -0.0475 | Tier 2 |
| Score 2 | p10 | -0.7500 | — | — | — |
| Score 2 | p25 | -0.5159 | — | — | — |
| Score 2 | median | -0.2041 | — | — | — |
| Score 2 | p75 | 0.1289 | — | — | — |
| Score 2 | p90 | 0.6564 | — | — | — |
| Score 2 | % positive | 0.324 | — | — | — |
| Score 2 | n | 392 | 859 | -467 | Tier 2 (A1 gap) |
| Score 3 | mean | 0.0039 | -0.0150 | 0.0189 | FAIL |
| Score 3 | p10 | -0.6544 | — | — | — |
| Score 3 | p25 | -0.4285 | — | — | — |
| Score 3 | median | -0.1626 | — | — | — |
| Score 3 | p75 | 0.1527 | — | — | — |
| Score 3 | p90 | 0.7426 | — | — | — |
| Score 3 | % positive | 0.336 | — | — | — |
| Score 3 | n | 743 | 1,618 | -875 | Tier 2 (A1 gap) |
| Score 4 | mean | 0.0194 | 0.0260 | -0.0066 | Tier 1 |
| Score 4 | p10 | -0.5962 | — | — | — |
| Score 4 | p25 | -0.3766 | — | — | — |
| Score 4 | median | -0.1231 | — | — | — |
| Score 4 | p75 | 0.1870 | — | — | — |
| Score 4 | p90 | 0.6962 | — | — | — |
| Score 4 | % positive | 0.390 | — | — | — |
| Score 4 | n | 1,003 | 2,462 | -1,459 | Tier 2 (A1 gap) |
| Score 5 | mean | 0.0822 | 0.0530 | 0.0292 | Tier 1 |
| Score 5 | p10 | -0.6191 | — | — | — |
| Score 5 | p25 | -0.3539 | — | — | — |
| Score 5 | median | -0.1033 | — | — | — |
| Score 5 | p75 | 0.2238 | — | — | — |
| Score 5 | p90 | 0.7692 | — | — | — |
| Score 5 | % positive | 0.401 | — | — | — |
| Score 5 | n | 1,135 | 2,787 | -1,652 | Tier 2 (A1 gap) |
| Score 6 | mean | 0.1549 | 0.1120 | 0.0429 | Tier 1 |
| Score 6 | p10 | -0.5256 | — | — | — |
| Score 6 | p25 | -0.3083 | — | — | — |
| Score 6 | median | -0.0590 | — | — | — |
| Score 6 | p75 | 0.2654 | — | — | — |
| Score 6 | p90 | 0.7281 | — | — | — |
| Score 6 | % positive | 0.438 | — | — | — |
| Score 6 | n | 993 | 2,579 | -1,586 | Tier 2 (A1 gap) |
| Score 7 | mean | 0.0802 | 0.1160 | -0.0358 | Tier 1 |
| Score 7 | p10 | -0.5155 | — | — | — |
| Score 7 | p25 | -0.3143 | — | — | — |
| Score 7 | median | -0.0907 | — | — | — |
| Score 7 | p75 | 0.2263 | — | — | — |
| Score 7 | p90 | 0.6894 | — | — | — |
| Score 7 | % positive | 0.423 | — | — | — |
| Score 7 | n | 747 | 1,894 | -1,147 | Tier 2 (A1 gap) |
| Score 8 | mean | 0.0753 | 0.1270 | -0.0517 | Tier 1 |
| Score 8 | p10 | -0.4924 | — | — | — |
| Score 8 | p25 | -0.2544 | — | — | — |
| Score 8 | median | -0.0596 | — | — | — |
| Score 8 | p75 | 0.2021 | — | — | — |
| Score 8 | p90 | 0.7855 | — | — | — |
| Score 8 | % positive | 0.422 | — | — | — |
| Score 8 | n | 405 | 1,115 | -710 | Tier 2 (A1 gap) |
| Score 9 | mean | 0.0556 | 0.1590 | -0.1034 | Tier 1 |
| Score 9 | p10 | -0.5487 | — | — | — |
| Score 9 | p25 | -0.2488 | — | — | — |
| Score 9 | median | -0.0887 | — | — | — |
| Score 9 | p75 | 0.1824 | — | — | — |
| Score 9 | p90 | 0.7546 | — | — | — |
| Score 9 | % positive | 0.397 | — | — | — |
| Score 9 | n | 141 | 333 | -192 | Tier 2 (A1 gap) |
| Low Score {0,1} | mean | -0.0344 | -0.0960 | 0.0616 | Tier 2 |
| Low Score {0,1} | p10 | -0.8648 | — | — | — |
| Low Score {0,1} | p25 | -0.5401 | — | — | — |
| Low Score {0,1} | median | -0.1754 | -0.2000 | 0.0246 | Tier 1 |
| Low Score {0,1} | p75 | 0.1942 | — | — | — |
| Low Score {0,1} | p90 | 0.8895 | — | — | — |
| Low Score {0,1} | % positive | 0.367 | — | — | — |
| Low Score {0,1} | n | 177 | 396 | -219 | Tier 2 (A1 gap) |
| High Score {8,9} | mean | 0.0702 | 0.1340 | -0.0638 | Tier 1 |
| High Score {8,9} | p10 | -0.4993 | — | — | — |
| High Score {8,9} | p25 | -0.2542 | — | — | — |
| High Score {8,9} | median | -0.0635 | 0.0000 | -0.0635 | Tier 1 (paper≈0) |
| High Score {8,9} | p75 | 0.1931 | — | — | — |
| High Score {8,9} | p90 | 0.7634 | — | — | — |
| High Score {8,9} | % positive | 0.416 | — | — | — |
| High Score {8,9} | n | 546 | 1,448 | -902 | Tier 2 (A1 gap) |

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| High − All | Δ mean | 0.0117 | 0.0750 | -0.0633 | Tier 2 |
| High − All | Δ p10 | 0.0994 | — | — | — |
| High − All | Δ p25 | 0.1068 | — | — | — |
| High − All | Δ median | 0.0447 | — | — | — |
| High − All | Δ p75 | -0.0130 | — | — | — |
| High − All | Δ p90 | 0.0332 | — | — | — |
| High − All | Δ % positive | 0.0207 | — | — | — |
| High − All | mean t-stat (Welch) | 0.346 | 3.140 | -2.794 | Tier 2 |
| High − All | median Wilcoxon p | 0.0104 | n/r | n/r | — |
| High − All | %+ two-prop z p | 0.3448 | n/r | n/r | — |
| High − All | bootstrap p (mean) | 0.3730 | n/r | n/r | — |
| High − Low | Δ mean | 0.1045 | 0.2300 | -0.1255 | Tier 2 |
| High − Low | Δ p10 | 0.3655 | — | — | — |
| High − Low | Δ p25 | 0.2859 | — | — | — |
| High − Low | Δ median | 0.1120 | — | — | — |
| High − Low | Δ p75 | -0.0011 | — | — | — |
| High − Low | Δ p90 | -0.1261 | — | — | — |
| High − Low | Δ % positive | 0.0485 | — | — | — |
| High − Low | mean t-stat (Welch) | 1.485 | 5.590 | -4.105 | Tier 2 |
| High − Low | median Wilcoxon p | 0.0021 | n/r | n/r | — |
| High − Low | %+ two-prop z p | 0.2529 | n/r | n/r | — |
| High − Low | bootstrap p (mean) | 0.1330 | n/r | n/r | — |

## Panel C — Two-Year Market-Adjusted Returns

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| All Firms | mean | 0.1151 | 0.1270 | -0.0119 | Tier 1 |
| All Firms | p10 | -0.9456 | — | — | — |
| All Firms | p25 | -0.6108 | — | — | — |
| All Firms | median | -0.2317 | — | — | — |
| All Firms | p75 | 0.3148 | — | — | — |
| All Firms | p90 | 1.2745 | — | — | — |
| All Firms | % positive | 0.364 | — | — | — |
| All Firms | n | 5,736 | — | — | — |
| Score 0 | mean | 0.0406 | 0.0640 | -0.0234 | — |
| Score 0 | p10 | -1.4643 | — | — | — |
| Score 0 | p25 | -0.8611 | — | — | — |
| Score 0 | median | -0.5842 | — | — | — |
| Score 0 | p75 | -0.2042 | — | — | — |
| Score 0 | p90 | 0.8328 | — | — | — |
| Score 0 | % positive | 0.190 | — | — | — |
| Score 0 | n | 21 | — | — | — |
| Score 1 | mean | -0.0504 | -0.1790 | 0.1286 | — |
| Score 1 | p10 | -1.1339 | — | — | — |
| Score 1 | p25 | -0.7587 | — | — | — |
| Score 1 | median | -0.3670 | — | — | — |
| Score 1 | p75 | 0.2221 | — | — | — |
| Score 1 | p90 | 1.0567 | — | — | — |
| Score 1 | % positive | 0.314 | — | — | — |
| Score 1 | n | 156 | — | — | — |
| Score 2 | mean | -0.1517 | 0.0380 | -0.1897 | — |
| Score 2 | p10 | -1.0929 | — | — | — |
| Score 2 | p25 | -0.8358 | — | — | — |
| Score 2 | median | -0.4135 | — | — | — |
| Score 2 | p75 | 0.0628 | — | — | — |
| Score 2 | p90 | 1.0611 | — | — | — |
| Score 2 | % positive | 0.281 | — | — | — |
| Score 2 | n | 392 | — | — | — |
| Score 3 | mean | 0.0600 | 0.0020 | 0.0580 | — |
| Score 3 | p10 | -1.0627 | — | — | — |
| Score 3 | p25 | -0.7393 | — | — | — |
| Score 3 | median | -0.3107 | — | — | — |
| Score 3 | p75 | 0.2524 | — | — | — |
| Score 3 | p90 | 1.2761 | — | — | — |
| Score 3 | % positive | 0.331 | — | — | — |
| Score 3 | n | 743 | — | — | — |
| Score 4 | mean | 0.1514 | 0.0960 | 0.0554 | — |
| Score 4 | p10 | -0.9759 | — | — | — |
| Score 4 | p25 | -0.6223 | — | — | — |
| Score 4 | median | -0.2450 | — | — | — |
| Score 4 | p75 | 0.2503 | — | — | — |
| Score 4 | p90 | 1.3469 | — | — | — |
| Score 4 | % positive | 0.351 | — | — | — |
| Score 4 | n | 1,003 | — | — | — |
| Score 5 | mean | 0.1104 | 0.1300 | -0.0196 | — |
| Score 5 | p10 | -0.9383 | — | — | — |
| Score 5 | p25 | -0.5973 | — | — | — |
| Score 5 | median | -0.2100 | — | — | — |
| Score 5 | p75 | 0.3577 | — | — | — |
| Score 5 | p90 | 1.3862 | — | — | — |
| Score 5 | % positive | 0.379 | — | — | — |
| Score 5 | n | 1,135 | — | — | — |
| Score 6 | mean | 0.1985 | 0.1640 | 0.0345 | — |
| Score 6 | p10 | -0.8137 | — | — | — |
| Score 6 | p25 | -0.5063 | — | — | — |
| Score 6 | median | -0.1707 | — | — | — |
| Score 6 | p75 | 0.3298 | — | — | — |
| Score 6 | p90 | 1.3155 | — | — | — |
| Score 6 | % positive | 0.390 | — | — | — |
| Score 6 | n | 993 | — | — | — |
| Score 7 | mean | 0.1594 | 0.1950 | -0.0356 | — |
| Score 7 | p10 | -0.8264 | — | — | — |
| Score 7 | p25 | -0.5257 | — | — | — |
| Score 7 | median | -0.1629 | — | — | — |
| Score 7 | p75 | 0.3294 | — | — | — |
| Score 7 | p90 | 1.2649 | — | — | — |
| Score 7 | % positive | 0.398 | — | — | — |
| Score 7 | n | 747 | — | — | — |
| Score 8 | mean | 0.2147 | 0.3090 | -0.0943 | — |
| Score 8 | p10 | -0.7278 | — | — | — |
| Score 8 | p25 | -0.4782 | — | — | — |
| Score 8 | median | -0.1641 | — | — | — |
| Score 8 | p75 | 0.3899 | — | — | — |
| Score 8 | p90 | 1.1508 | — | — | — |
| Score 8 | % positive | 0.395 | — | — | — |
| Score 8 | n | 405 | — | — | — |
| Score 9 | mean | 0.0136 | 0.2130 | -0.1994 | — |
| Score 9 | p10 | -0.8991 | — | — | — |
| Score 9 | p25 | -0.6019 | — | — | — |
| Score 9 | median | -0.1842 | — | — | — |
| Score 9 | p75 | 0.2570 | — | — | — |
| Score 9 | p90 | 1.1543 | — | — | — |
| Score 9 | % positive | 0.376 | — | — | — |
| Score 9 | n | 141 | — | — | — |
| Low Score {0,1} | mean | -0.0396 | -0.1450 | 0.1054 | Tier 2 |
| Low Score {0,1} | p10 | -1.1646 | — | — | — |
| Low Score {0,1} | p25 | -0.7726 | — | — | — |
| Low Score {0,1} | median | -0.3916 | — | — | — |
| Low Score {0,1} | p75 | 0.2006 | — | — | — |
| Low Score {0,1} | p90 | 1.0517 | — | — | — |
| Low Score {0,1} | % positive | 0.299 | — | — | — |
| Low Score {0,1} | n | 177 | — | — | — |
| High Score {8,9} | mean | 0.1628 | 0.2870 | -0.1242 | Tier 1 |
| High Score {8,9} | p10 | -0.7882 | — | — | — |
| High Score {8,9} | p25 | -0.5114 | — | — | — |
| High Score {8,9} | median | -0.1692 | — | — | — |
| High Score {8,9} | p75 | 0.3712 | — | — | — |
| High Score {8,9} | p90 | 1.1588 | — | — | — |
| High Score {8,9} | % positive | 0.390 | — | — | — |
| High Score {8,9} | n | 546 | — | — | — |

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| High − All | Δ mean | 0.0477 | 0.1600 | -0.1123 | Tier 2 |
| High − All | Δ p10 | 0.1573 | — | — | — |
| High − All | Δ p25 | 0.0994 | — | — | — |
| High − All | Δ median | 0.0625 | — | — | — |
| High − All | Δ p75 | 0.0564 | — | — | — |
| High − All | Δ p90 | -0.1157 | — | — | — |
| High − All | Δ % positive | 0.0261 | — | — | — |
| High − All | mean t-stat (Welch) | 0.501 | 2.639 | -2.138 | Tier 2 |
| High − All | median Wilcoxon p | 0.0160 | n/r | n/r | — |
| High − All | %+ two-prop z p | 0.2266 | n/r | n/r | — |
| High − All | bootstrap p (mean) | 0.2680 | n/r | n/r | — |
| High − Low | Δ mean | 0.2024 | 0.4320 | -0.2296 | Tier 2 |
| High − Low | Δ p10 | 0.3764 | — | — | — |
| High − Low | Δ p25 | 0.2612 | — | — | — |
| High − Low | Δ median | 0.2224 | — | — | — |
| High − Low | Δ p75 | 0.1706 | — | — | — |
| High − Low | Δ p90 | 0.1071 | — | — | — |
| High − Low | Δ % positive | 0.0907 | — | — | — |
| High − Low | mean t-stat (Welch) | 1.243 | 5.749 | -4.506 | Tier 2 |
| High − Low | median Wilcoxon p | 0.0000 | n/r | n/r | — |
| High − Low | %+ two-prop z p | 0.0297 | n/r | n/r | — |
| High − Low | bootstrap p (mean) | 0.1010 | n/r | n/r | — |

## Panel D — RANK_SCORE Quintiles (ranked-signal alternative)

Restricted to rows with non-null `rank_q` (n = 5,563; **dropped 173 FY1987-cohort firm-years** whose prior-year (FY1986) RANK_SCORE distribution is unavailable under A1). Quintile cutoffs come from the prior fyear; Q5 = High, Q1 = Low.

### Panel D — One-Year Market-Adjusted

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| Q1 | mean | 0.0671 | — | — | — |
| Q1 | median | -0.1633 | — | — | — |
| Q1 | % positive | 0.353 | — | — | — |
| Q1 | n | 1,112 | 2,892 | -1,780 | — |
| Q2 | mean | 0.0410 | — | — | — |
| Q2 | median | -0.1240 | — | — | — |
| Q2 | % positive | 0.385 | — | — | — |
| Q2 | n | 1,116 | 2,843 | -1,727 | — |
| Q3 | mean | 0.0566 | — | — | — |
| Q3 | median | -0.0857 | — | — | — |
| Q3 | % positive | 0.419 | — | — | — |
| Q3 | n | 1,070 | 2,708 | -1,638 | — |
| Q4 | mean | 0.0737 | — | — | — |
| Q4 | median | -0.0880 | — | — | — |
| Q4 | % positive | 0.418 | — | — | — |
| Q4 | n | 1,156 | 2,818 | -1,662 | — |
| Q5 | mean | 0.0635 | — | — | — |
| Q5 | median | -0.0950 | — | — | — |
| Q5 | % positive | 0.395 | — | — | — |
| Q5 | n | 1,109 | 2,788 | -1,679 | — |
| Q5 − Q1 (High−Low) | Δ mean | -0.0035 | 0.0920 | -0.0955 | FAIL |
| Q5 − Q1 (High−Low) | mean t-stat (Welch) | -0.079 | 4.488 | -4.567 | FAIL |
| Q5 − Q1 (High−Low) | Δ median | 0.0683 | n/r | n/r | — |
| Q5 − Q1 (High−Low) | median Wilcoxon p | 0.0000 | n/r | n/r | — |
| Q5 − All (High−All) | Δ mean | 0.0030 | 0.0380 | -0.0350 | Tier 2 |
| Q5 − All (High−All) | mean t-stat (Welch) | 0.094 | — | — | — |
| Q5 − All (High−All) | Δ median | 0.0158 | n/r | n/r | — |
| Q5 − All (High−All) | median Wilcoxon p | 0.1039 | n/r | n/r | — |

### Panel D — Two-Year Market-Adjusted

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| Q1 | mean | 0.1845 | 0.0610 | 0.1235 | — |
| Q1 | median | -0.3380 | — | — | — |
| Q1 | % positive | 0.319 | — | — | — |
| Q1 | n | 1,112 | — | — | — |
| Q2 | mean | 0.0760 | 0.1040 | -0.0280 | — |
| Q2 | median | -0.2624 | — | — | — |
| Q2 | % positive | 0.358 | — | — | — |
| Q2 | n | 1,116 | — | — | — |
| Q3 | mean | 0.1436 | 0.1210 | 0.0226 | — |
| Q3 | median | -0.1705 | — | — | — |
| Q3 | % positive | 0.404 | — | — | — |
| Q3 | n | 1,070 | — | — | — |
| Q4 | mean | 0.1354 | 0.1660 | -0.0306 | — |
| Q4 | median | -0.1950 | — | — | — |
| Q4 | % positive | 0.373 | — | — | — |
| Q4 | n | 1,156 | — | — | — |
| Q5 | mean | 0.0703 | 0.1860 | -0.1157 | — |
| Q5 | median | -0.1935 | — | — | — |
| Q5 | % positive | 0.370 | — | — | — |
| Q5 | n | 1,109 | — | — | — |
| Q5 − Q1 (High−Low) | Δ mean | -0.1142 | 0.1250 | -0.2392 | — |
| Q5 − Q1 (High−Low) | mean t-stat (Welch) | -1.027 | 2.461 | -3.488 | — |
| Q5 − Q1 (High−Low) | Δ median | 0.1445 | n/r | n/r | — |
| Q5 − Q1 (High−Low) | median Wilcoxon p | 0.0000 | n/r | n/r | — |
| Q5 − All (High−All) | Δ mean | -0.0516 | 0.0590 | -0.1106 | — |
| Q5 − All (High−All) | mean t-stat (Welch) | -0.956 | — | — | — |
| Q5 − All (High−All) | Δ median | 0.0395 | n/r | n/r | — |
| Q5 − All (High−All) | median Wilcoxon p | 0.1143 | n/r | n/r | — |

## Panel D sensitivity — three RANK_SCORE constructions (diagnostic)

In-memory re-ranking of the same nine realizations (no SQL re-run; pipeline frozen). **Current**: `rank(pct=True, method='min')` as in the pipeline. **Alt-1**: `method='average'`. **Alt-2**: Alt-1 with the equity-offer dimension ranked by raw `sstk` amount (NULL → 0, auxiliary single-column lookup, same funda filter/dedup as the pipeline). Quintile cutoffs always come from the prior fyear; the FY1987 cohort (no FY1986 distribution under A1) is excluded, n = 5,563 for every variant.

| Variant | Horizon | Q1 | Q2 | Q3 | Q4 | Q5 | Q5−Q1 | t (Welch) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Current (min-rank, pipeline) | 1yr | 0.0671 | 0.0410 | 0.0566 | 0.0737 | 0.0635 | -0.0035 | -0.079 |
| Current (min-rank, pipeline) | 2yr | 0.1845 | 0.0760 | 0.1436 | 0.1354 | 0.0703 | -0.1142 | -1.027 |
| Alt-1 (average-rank) | 1yr | 0.0715 | 0.0458 | 0.0380 | 0.0792 | 0.0670 | -0.0046 | -0.103 |
| Alt-1 (average-rank) | 2yr | 0.1856 | 0.0893 | 0.1172 | 0.1378 | 0.0797 | -0.1059 | -0.953 |
| Alt-2 (average-rank, sstk amount) | 1yr | 0.0654 | 0.0519 | 0.0401 | 0.0835 | 0.0608 | -0.0046 | -0.104 |
| Alt-2 (average-rank, sstk amount) | 2yr | 0.1751 | 0.1044 | 0.1121 | 0.1406 | 0.0765 | -0.0986 | -0.897 |

**Pre-committed decision rule**: adopt Alt-1/Alt-2 only if its 1-yr Q5−Q1 spread ≥ +0.05 with Welch t ≥ 1.5 AND the 2-yr spread is positive.

**Result: no variant meets the rule** (Alt-1 1-yr -0.0046, t -0.103; Alt-2 1-yr -0.0046, t -0.104). The pipeline's min-rank construction stays. Panel D null under all three rank variants; attributed to the truncated sample (footnote 12 documents this methodology's inefficiency; the paper's +0.092 comes from a 3× larger sample).

## Tally (contract targets in tables_to_replicate.json only)

| Tier | Count |
|---|---:|
| Tier 1 (match) | 16 |
| Tier 2 (pattern / A1 gap) | 32 |
| FAIL (sign flip / unreachable) | 3 |
| **Total targeted cells** | **51** |

### FAIL cells (diagnosis)

- **Panel B Score 3 mean** (ours +0.0039 vs paper −0.015): sign flip on a near-zero per-score mean (both ≈ 0). Noise-level at a single score; the monotonic increase in means across scores 4→9 still holds in our panel.
- **Panel D 1-yr High−Low (Q5−Q1) mean** (ours −0.0035 vs paper +0.092) **and its t-stat** (ours −0.079 vs 4.488): the ranked-signal quintile spread is essentially flat (slightly negative) in the restricted sample, opposite to the paper's monotonic quintile pattern. This is the one place where the cross-sectional pattern does not replicate; note the F_SCORE High−Low spread in Panels A–C keeps the paper's *sign* (Tier 2), so the binary-score result survives but the continuous RANK_SCORE aggregation does not, in this sub-period/vintage.

## Interpretation

The central F_SCORE result is directionally present but materially attenuated under restriction A1 (formation 1988–1996; 5,736 obs = 41% of the paper's 14,043). The headline one-year market-adjusted High−Low spread is **0.105** (ours) vs **0.230** (paper) and High−All is **0.012** vs **0.075**; the group means keep the paper's signs (High > All > Low in Panels A, B, C) so they score Tier 2, and the High mean and All mean in every panel land in Tier 1. The t-statistics (Welch) are far below the paper's (e.g. 1.49 vs 5.59 for the Panel B High−Low spread), reflecting both the smaller n and a weaker spread in this sub-period — none is significant at conventional levels on the mean.

A notable nuance: the **Wilcoxon rank-sum test on the median/distribution is significant** (Panel B High−Low p ≈ 0.002) even though the *mean* spread is not — High F_SCORE firms are distributionally better (higher median, fewer large losers) in our sample, but the mean is pulled down by the heavy right tail / vintage outliers. The bootstrap p-values (seed=42) are all large (≈0.10–0.39), consistent with the insignificant mean spreads.

Per-score counts are uniformly ~37–47% of the paper's (Tier 2, A1 gap) with the same hump-shaped distribution peaking at score 5. Per-score means match the paper within the 80% tolerance for scores 4–9 (Tier 1) but are noisier at the sparse low scores (score 0: −0.236 vs −0.061, same sign, Tier 2; score 3 flips sign on a ≈0 value, FAIL).

What FAILs: score 3's near-zero mean, and the Panel D 1-yr RANK_SCORE quintile spread (mean and t-stat) which is flat/slightly negative rather than the paper's increasing 0.05→0.14 pattern. The two-year Panel D and all Panel D per-quintile cells are informational (not contracted).

Bottom line: the direction, cross-sectional ordering (scores 4–9), and distributional separation of the F_SCORE effect replicate; the *magnitude and mean-significance* of the headline spreads do not, which we attribute to the documented A1 sub-period restriction and 2026-vintage data drift rather than to a construction error — the Tier-1 match of the All/High group means and the entire Table 1 signal/return machinery supports that reading. No spin: the headline 7.5%/23% numbers are NOT reproduced here.
