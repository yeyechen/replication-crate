# Table VII — event-time average monthly and cumulative zero-cost returns

Jegadeesh & Titman (1993), Table VII. J=6 formation cohorts, Jan 1965 – Dec 1989
(300 cohorts); event month h averages the zero-cost (buy − sell) return across
cohorts with holding month h on or before Dec 1989 (n_1 = 299, n_36 = 264). PRIMARY = RAW series (A3-revision):
signal cumret_6_raw, holding ret_raw; membership fixed at formation, rebalanced
monthly to equal weights (A10). Monthly t: iid across cohorts (A5). Cumulative:
arithmetic sum of event-month means; t-stat = Newey-West (Bartlett,
L = int(4·(n/100)^(2/9)); L=5 at n≈300) on the cross-cohort cumulative series
s_f = Σ_{k≤h} zc_{f,k}, cohorts ordered by formation date (footnote 16 / A10).

## Months 1–12

| t | Monthly ret | (t-stat) | Cumulative ret | (NW t-stat) |
|--:|------------:|---------:|---------------:|------------:|
| 1 | -0.0024 | (-0.63) | -0.0024 | (-0.62) |
| 2 | +0.0120 | (+3.59) | +0.0096 | (+1.47) |
| 3 | +0.0122 | (+3.66) | +0.0218 | (+2.40) |
| 4 | +0.0119 | (+3.84) | +0.0337 | (+2.99) |
| 5 | +0.0104 | (+3.45) | +0.0441 | (+3.34) |
| 6 | +0.0101 | (+3.62) | +0.0541 | (+3.60) |
| 7 | +0.0141 | (+5.70) | +0.0682 | (+4.13) |
| 8 | +0.0124 | (+4.97) | +0.0806 | (+4.51) |
| 9 | +0.0095 | (+3.64) | +0.0902 | (+4.70) |
| 10 | +0.0054 | (+2.00) | +0.0956 | (+4.68) |
| 11 | +0.0051 | (+1.84) | +0.1007 | (+4.64) |
| 12 | +0.0014 | (+0.48) | +0.1021 | (+4.40) |

## Months 13–24

| t | Monthly ret | (t-stat) | Cumulative ret | (NW t-stat) |
|--:|------------:|---------:|---------------:|------------:|
| 13 | -0.0034 | (-1.11) | +0.0987 | (+3.96) |
| 14 | -0.0041 | (-1.48) | +0.0946 | (+3.59) |
| 15 | -0.0031 | (-1.20) | +0.0915 | (+3.31) |
| 16 | -0.0033 | (-1.31) | +0.0881 | (+3.08) |
| 17 | -0.0046 | (-1.76) | +0.0836 | (+2.85) |
| 18 | -0.0048 | (-1.95) | +0.0788 | (+2.61) |
| 19 | -0.0006 | (-0.28) | +0.0781 | (+2.54) |
| 20 | -0.0020 | (-0.82) | +0.0762 | (+2.43) |
| 21 | -0.0020 | (-0.83) | +0.0742 | (+2.28) |
| 22 | -0.0024 | (-1.00) | +0.0718 | (+2.14) |
| 23 | +0.0000 | (+0.01) | +0.0718 | (+2.06) |
| 24 | +0.0006 | (+0.24) | +0.0724 | (+2.01) |

## Months 25–36

| t | Monthly ret | (t-stat) | Cumulative ret | (NW t-stat) |
|--:|------------:|---------:|---------------:|------------:|
| 25 | -0.0028 | (-1.08) | +0.0696 | (+1.85) |
| 26 | -0.0006 | (-0.24) | +0.0690 | (+1.76) |
| 27 | -0.0013 | (-0.55) | +0.0677 | (+1.64) |
| 28 | -0.0017 | (-0.73) | +0.0659 | (+1.57) |
| 29 | -0.0025 | (-1.10) | +0.0634 | (+1.41) |
| 30 | -0.0019 | (-0.84) | +0.0616 | (+1.30) |
| 31 | +0.0015 | (+0.74) | +0.0631 | (+1.29) |
| 32 | +0.0010 | (+0.49) | +0.0641 | (+1.27) |
| 33 | +0.0022 | (+1.01) | +0.0662 | (+1.29) |
| 34 | +0.0011 | (+0.48) | +0.0673 | (+1.25) |
| 35 | +0.0022 | (+0.97) | +0.0694 | (+1.25) |
| 36 | +0.0002 | (+0.07) | +0.0696 | (+1.17) |

## Anchor checks (ours vs paper)

| metric | ours | paper | deviation |
|--------|-----:|------:|----------:|
| event_t1_monthly | -0.002370 | -0.0025 | +5.2% |
| event_t1_monthly_t | -0.630090 | -0.59 | -6.8% |
| event_t2_monthly | 0.011999 | 0.0124 | -3.2% |
| event_t2_monthly_t | 3.590234 | 3.29 | +9.1% |
| event_t6_monthly | 0.010073 | 0.0091 | +10.7% |
| event_t6_monthly_t | 3.618663 | 2.94 | +23.1% |
| event_t12_monthly | 0.001404 | 0.0013 | +8.0% |
| event_t12_monthly_t | 0.481634 | 0.43 | +12.0% |
| event_t12_cumulative | 0.102072 | 0.0951 | +7.3% |
| event_t12_cumulative_t | 4.404484 | 3.67 | +20.0% |
| event_t18_monthly | -0.004799 | -0.0056 | +14.3% |
| event_t18_monthly_t | -1.947959 | -2.19 | +11.1% |
| event_t18_cumulative | 0.078755 | 0.0701 | +12.3% |
| event_t18_cumulative_t | 2.610376 | 2.68 | -2.6% |
| event_t24_cumulative | 0.072402 | 0.0556 | +30.2% |
| event_t24_cumulative_t | 2.011186 | 1.69 | +19.0% |
| event_t36_monthly | 0.000154 | -0.0005 | +130.9% |
| event_t36_monthly_t | 0.069055 | -0.24 | +128.8% |
| event_t36_cumulative | 0.069595 | 0.0406 | +71.4% |
| event_t36_cumulative_t | 1.165732 | 0.67 | +74.0% |

## Diagnostics and anomaly flags

⚠️ ANOMALY: the endpoint cumulative C_36 is +71.4% vs the paper (ours 0.0696 vs 0.0406) while the headline C_12 is +7.3% (ours 0.1021 vs 0.0951). The gap widens monotonically over h=13..36 (ours decays less: block means above) and month 1 is elevated (ours -0.0024 vs paper −0.0025) — the same direction as the documented Table I sell-side residual (our loser-decile returns run below the paper's 1990 vintage, largest at the shortest horizons), extended into event time. The construction itself is validated below (hand check exact; cohort counts n_1=299, n_36=264; shape matches: hump 1-12, negative 13-24, flat 25-36). No tuning applied.

- Event-month means: min=-0.004799 (h=18), max=+0.014052 (h=7), mean=+0.001933; C_36=+0.069595. Block means: h=1..12 +0.008506/mo (paper 0.0951/12=+0.007925), h=13..24 -0.002473/mo (paper −0.003292), h=25..36 -0.000234/mo (paper −0.001250).
- Cross-cohort zc distribution (all valid f,h): n=10,134 mean=0.002050 median=0.005263 std=0.044432 min=-0.549167 max=0.163476 p1=-0.146615 p99=0.095933
- h=12: C_h (arithmetic sum of event-month means) = 0.102072 vs mean of per-cohort cumulative sums = 0.094107 (n=288; they differ because later event months average over fewer, earlier cohorts).
- h=36: C_h (arithmetic sum of event-month means) = 0.069595 vs mean of per-cohort cumulative sums = 0.039574 (n=264; they differ because later event months average over fewer, earlier cohorts).
- Single-cohort hand check (formation 1979-12, straight from the panel; h=1,2,12, deciles 1 & 10):
    h=1  (1980-01) decile  1: hand=+0.111969 pipeline=+0.111969 match=True
    h=1  (1980-01) decile 10: hand=+0.123485 pipeline=+0.123485 match=True
    h=2  (1980-02) decile  1: hand=-0.038745 pipeline=-0.038745 match=True
    h=2  (1980-02) decile 10: hand=+0.003413 pipeline=+0.003413 match=True
    h=12 (1980-12) decile  1: hand=-0.038162 pipeline=-0.038162 match=True
    h=12 (1980-12) decile 10: hand=-0.039729 pipeline=-0.039729 match=True

**Per-cell evaluation:** 144 cells — 118 Tier 1 / 18 Tier 2 / 8 FAIL (rule: within tolerance = Tier 1; same sign & ≤2× deviation = Tier 2; else FAIL).
