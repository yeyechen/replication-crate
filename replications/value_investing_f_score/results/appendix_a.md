# Appendix A — One-Year Market-Adjusted Returns by Formation Year (Strong vs Weak F_SCORE Hedge)

Hedge portfolio: long **strong** F_SCORE (≥ 5), short **weak** F_SCORE (< 5), within the high-BM universe; returns are the one-year market-adjusted BHR (`ma_ret1`) grouped by `formation_year`, 1988–1996. **4 observations formed in 1987 are excluded** (FY1987 firms with mid-year fiscal year-ends; they match no printed paper year-row and are outside the paper's calendar-year tabulation). t-statistics = mean / (std / √9) on the 9-observation annual series (ddof=1). Paper: 21 years 1976–1996, positive spread in 17 of 21; ours: positive spread in **9 of 9** years (not a contract target — shown for completeness).

## Annual returns

| Year | Strong (ours) | Weak (ours) | Spread (ours) | Spread (paper) | n (ours) | n (paper) |
|---|---:|---:|---:|---:|---:|---:|
| 1988 | 0.0166 | -0.1385 | 0.1550 | 0.168 | 211 | 684 |
| 1989 | -0.0563 | -0.1561 | 0.0997 | -0.036 | 609 | 765 |
| 1990 | -0.0173 | -0.0630 | 0.0457 | 0.157 | 696 | 1,256 |
| 1991 | 0.2561 | 0.1441 | 0.1120 | 0.166 | 1,068 | 569 |
| 1992 | 0.3513 | 0.1208 | 0.2305 | 0.070 | 476 | 622 |
| 1993 | 0.2498 | 0.2131 | 0.0368 | 0.020 | 535 | 602 |
| 1994 | 0.0575 | 0.0412 | 0.0164 | -0.001 | 591 | 1,116 |
| 1995 | 0.0045 | -0.0219 | 0.0265 | 0.126 | 902 | 876 |
| 1996 | -0.0248 | -0.2380 | 0.2131 | 0.147 | 644 | 715 |
| **Average** | **0.0931** | **-0.0109** | **0.1040** | — | — | — |
| t-statistic | 1.855 | -0.215 | 3.861 | — | — | — |
| Paper avg (t), full 1976-1996 | 0.106 (t 3.360) | 0.009 (t 0.243) | 0.097 (t 5.059) | — | — | — |
| **Paper avg, same-period 1988-1996 ‡** | — | — | **0.1040** | **0.091** | — | — |

‡ Paper same-period (1988-1996) average spread, computed from the paper's printed annual rows: (0.168−0.036+0.157+0.166+0.070+0.020−0.001+0.126+0.147)/9 = 0.091. Ours (same 9 years) = 0.1040 — the like-for-like benchmark for this A1-restricted replication, next to the full-period 0.097 target above (which is structurally unreachable under A1). This row is informational, not a contract target (the contract's avg_spread_mean is the full-period 0.097).

## Contract-cell evaluation

| Cell | Ours | Paper | Δ | Tier |
|---|---:|---:|---:|---|
| Average strong return | 0.0931 | 0.106 | -0.0129 | Tier 1 |
| Average strong t-stat | 1.8548 | 3.360 | -1.5052 | Tier 2 |
| Average weak return | -0.0109 | 0.009 | -0.0199 | FAIL |
| Average spread | 0.1040 | 0.097 | +0.0070 | Tier 1 |
| Average spread t-stat | 3.8606 | 5.059 | -1.1984 | Tier 1 |
| Spread 1990 | 0.0457 | 0.157 | -0.1113 | Tier 1 |
| Spread 1996 | 0.2131 | 0.147 | +0.0661 | Tier 1 |
| n 1990 | 696 | 1,256 | -560 | Tier 2 (A1 gap) |
| n 1996 † | 644 | 715 | -71 | Tier 1 |
| Spread 1976 | — | -0.004 | — | SKIP — year outside restricted sample (A1) |
| Spread 1983 | — | 0.349 | — | SKIP — year outside restricted sample (A1) |
| n 1976 | — | 383 | — | SKIP — year outside restricted sample (A1) |

† n_1996 is a target per the task text; it is absent from tables_to_replicate.json and carries the conventional count tolerance (±25%, per n_1990).

## Tally (contract targets in tables_to_replicate.json, + † task text)

| Tier | Count |
|---|---:|
| Tier 1 (match) | 6 |
| Tier 2 (pattern / A1 gap) | 2 |
| FAIL (sign flip / unreachable) | 1 |
| SKIP (year outside restricted sample, A1) | 3 |
| **Total targeted cells** | **9** (+3 SKIP) |

### FAIL cells (diagnosis)

- **Average weak return** (ours -0.0109 vs paper +0.009): sign flip on a value statistically indistinguishable from zero in BOTH samples (paper t = 0.243; ours t = -0.215). The weak portfolio earns ≈ 0 either way; the economic object — the Strong−Weak spread — replicates (0.1040 vs 0.097, Tier 1; t 3.861 vs 5.059, Tier 1).

## Interpretation

The annual hedge economics replicate: average spread 0.1040 vs 0.097 (Tier 1) with t = 3.861 vs 5.059 (Tier 1), average strong return 0.0931 vs 0.106 (Tier 1; t 1.855 vs 3.360 is Tier 2), and the spread is positive in **9 of 9** years (paper: 17 of 21) — the time-series robustness claim survives the restriction, on fewer annual draws. The single FAIL is the average weak return (diagnosed above): both point estimates are within ±0.011 of zero.

Per-year spreads (0.155/0.100/0.046/0.112/0.231/0.037/0.016/0.026/0.213 vs the paper's 0.168/−0.036/0.157/0.166/0.070/0.020/−0.001/0.126/0.147) scatter around the paper's — our years are uniformly positive where the paper has two negatives (1989, 1994), and the two targeted years are Tier 1 (1990: 0.046 vs 0.157, inside the ±80% band; 1996: 0.213 vs 0.147). Per-year counts run 31–188% of the paper's (the 1991 and 1995 cohorts are LARGER than the paper's 569/876 — the 2026 vintage's CCM link recovers small firms the 1990s CUSIP match missed, while the early cohorts shrink under A1): n_1990 is Tier 2 (A1 gap, 55% of 1,256) while n_1996 lands Tier 1 (644 vs 715, within 10%) — the FY1995 cohort survives the oancf restriction almost intact. The 1976/1983 spread and 1976 count are SKIP by construction (pre-restriction years under A1).
