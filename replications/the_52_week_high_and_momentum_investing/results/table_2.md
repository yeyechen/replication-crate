# Table II — George & Hwang (2004): (6,6) strategies split by calendar month of the HOLDING month t

Panel A: months t with month-of-year != 1 (424 months). Panel B: January only (38 months). Same machinery as Table I.

Holding-period returns: panel column `ret_dl` (delisting-adjusted); ranking signals always on original ret.

## Panel A (excluding January)

| cell name | paper value | our value | deviation pp | deviation % | tier |
|---|---:|---:|---:|---:|---|
| pA_jt_winner | 1.2300 | 1.2048 | -0.0252 | -2.1% | Tier 1 |
| pA_jt_loser | 0.1600 | 0.1290 | -0.0310 | -19.4% | Tier 1 |
| pA_jt_w_minus_l | 1.0700 | 1.0758 | +0.0058 | +0.5% | Tier 1 |
| pA_jt_tstat | 6.9700 | 6.7869 | -0.1831 | -2.6% | Tier 1 |
| pA_mg_winner | 0.9900 | 1.0370 | +0.0470 | +4.7% | Tier 1 |
| pA_mg_loser | 0.5000 | 0.3930 | -0.1070 | -21.4% | Tier 1 |
| pA_mg_w_minus_l | 0.5000 | 0.6440 | +0.1440 | +28.8% | Tier 1 |
| pA_mg_tstat | 3.9200 | 5.2865 | +1.3665 | +34.9% | Tier 1 |
| pA_wh_winner | 1.3000 | 1.2651 | -0.0349 | -2.7% | Tier 1 |
| pA_wh_loser | 0.0700 | 0.0839 | +0.0139 | +19.9% | Tier 1 |
| pA_wh_w_minus_l | 1.2300 | 1.1812 | -0.0488 | -4.0% | Tier 1 |
| pA_wh_tstat | 7.0600 | 6.5247 | -0.5353 | -7.6% | Tier 1 |

**Hit rate: 12 Tier 1 / 0 Tier 2 / 0 FAIL out of 12**

_Tier 2 ⚠ = sign matches but |ours/paper| > 2 (magnitude far off; see audit1.md spot-check 10). FAIL cells with |paper| < 0.05 are rounding-boundary artifacts unless noted._

## Panel B (January only)

| cell name | paper value | our value | deviation pp | deviation % | tier |
|---|---:|---:|---:|---:|---|
| pB_jt_winner | 4.9600 | 5.0663 | +0.1063 | +2.1% | Tier 1 |
| pB_jt_loser | 11.2000 | 11.3313 | +0.1313 | +1.2% | Tier 1 |
| pB_jt_w_minus_l | -6.2900 | -6.2650 | +0.0250 | +0.4% | Tier 1 |
| pB_jt_tstat | -4.4800 | -4.3012 | +0.1788 | +4.0% | Tier 1 |
| pB_mg_winner | 7.0000 | 6.9580 | -0.0420 | -0.6% | Tier 1 |
| pB_mg_loser | 7.0900 | 7.1566 | +0.0666 | +0.9% | Tier 1 |
| pB_mg_w_minus_l | -0.0900 | -0.1987 | -0.1087 | -120.8% | Tier 1 |
| pB_mg_tstat | -0.1200 | -0.2754 | -0.1554 | -129.5% | Tier 2 ⚠ |
| pB_wh_winner | 3.8400 | 3.7320 | -0.1080 | -2.8% | Tier 1 |
| pB_wh_loser | 12.1100 | 11.7648 | -0.3452 | -2.9% | Tier 1 |
| pB_wh_w_minus_l | -8.2700 | -8.0328 | +0.2372 | +2.9% | Tier 1 |
| pB_wh_tstat | -5.4900 | -5.0708 | +0.4192 | +7.6% | Tier 1 |

**Hit rate: 11 Tier 1 / 1 Tier 2 / 0 FAIL out of 12**

_Tier 2 ⚠ = sign matches but |ours/paper| > 2 (magnitude far off; see audit1.md spot-check 10). FAIL cells with |paper| < 0.05 are rounding-boundary artifacts unless noted._

## January-collapse sanity check (loser returns, percent/month)

| strategy | loser Table I (all) | loser Panel A (ex-Jan) | loser Panel B (Jan) |
|---|---:|---:|---:|
| JT | 1.0504 | 0.1290 | 11.3313 |
| MG | 0.9494 | 0.3930 | 7.1566 |
| WH | 1.0447 | 0.0839 | 11.7648 |

- Expected: losers collapse from Table I to Panel A (January rebound removed), especially JT/52WH; Panel B losers ~11-12%.