# Table V — George & Hwang (2004): Fama-MacBeth dummy-variable regressions

Each month t (1963-07 .. 2001-12, 462) x formation lag j: one cross-sectional
OLS of R_{it}(%) on R_{i,t-1}(decimal), ln(mcap_$ at t-1), and 6 strategy
dummies (JH/JL<-jt_sig, MH/ML<-mg_sig, FHH/FHL<-wh_sig_dc). Dummies from 30/30 ordinal sorts at formation
f=t-j on the non-null signal cross-section (same convention as tables_1_3);
stocks un-rankable for a strategy get 0/0 dummies and stay in the sample.
(6,6): j=2..7 ; (6,12): j=2..13. c_{k,t}=mean_j b_{k,j,t}; raw=TS mean of c
with t-stat from the c series; RA=intercept of c (or spread) series on FF3.
Jan incl = all 462 t; Jan excl = month-of-year != 1.

Dependent variable R_it: panel column `ret_dl` (delisting-adjusted); R_{i,t-1} control, dummies, and sample rule on original ret.

## Rankable stocks per formation month (avg by decade, formation grid only)

| strategy | 1960s | 1970s | 1980s | 1990s | 2000s |
|---|---:|---:|---:|---:|---:|
| jt (jt_sig) | 1928.1 | 3738.5 | 5216.2 | 6204.1 | 6063.6 |
| mg (mg_sig) | 1928.1 | 3738.5 | 5216.2 | 6204.1 | 6063.6 |
| wh (wh_sig_dc) | 2037.9 | 3988.6 | 5495.1 | 6495.8 | 6265.7 |

## Pre-flight (s66_raw)

| row | ours janincl | paper janincl | ours janexcl |
|---|---:|---:|---:|
| intercept | 4.6407 (t 5.34) | 3.62 | 1.8758 (t 2.45) |
| r_lag1 | -6.0645 (t -15.21) | -6.50 | -5.1705 (t -14.69) |
| size | -0.1881 (t -4.38) | -0.20 | -0.0584 (t -1.52) |
| wh_spread | 0.4896 (t 3.02) | 0.65 | 0.8745 (t 6.12) |

## Diagnostics

- s66: avg sample 4803.6 (min 1962, max 7389), 2772 regressions, 0 empty months
- s612: avg sample 4803.6 (min 1962, max 7389), 5544 regressions, 0 empty months
- FF factors: 462 months aligned, 0 missing

## Overall hit rate (of 192)

**Tier 1: 150 / Tier 2: 42 / FAIL: 0**

### Per-column tally

| column | Tier 1 | Tier 2 | FAIL |
|---|---:|---:|---:|
| s66_raw_janincl | 21 | 3 | 0 |
| s66_raw_janexcl | 20 | 4 | 0 |
| s66_ra_janincl | 17 | 7 | 0 |
| s66_ra_janexcl | 18 | 6 | 0 |
| s612_raw_janincl | 20 | 4 | 0 |
| s612_raw_janexcl | 19 | 5 | 0 |
| s612_ra_janincl | 17 | 7 | 0 |
| s612_ra_janexcl | 18 | 6 | 0 |

_Tier 2 ⚠ = sign matches but |ours/paper| > 2 (magnitude far off; see audit1.md spot-check 10). FAIL cells with |paper| < 0.05 are rounding-boundary artifacts unless noted._

### Column: s66_raw_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 3.6200 | 4.6407 | +28.2% | Tier 1 | 6.0900 | 5.3351 | Tier 1 |
| r_lag1 | -6.5000 | -6.0645 | +6.7% | Tier 1 | -14.9000 | -15.2147 | Tier 1 |
| size | -0.2000 | -0.1881 | +6.0% | Tier 1 | -4.7000 | -4.3765 | Tier 1 |
| jt_winner | 0.1700 | 0.2664 | +56.7% | Tier 1 | 2.0700 | 3.6532 | Tier 2 |
| jt_loser | -0.2100 | -0.2630 | -25.3% | Tier 1 | -3.6000 | -4.4741 | Tier 1 |
| mg_winner | 0.1800 | 0.1993 | +10.7% | Tier 1 | 2.8000 | 3.5911 | Tier 1 |
| mg_loser | -0.0700 | -0.1810 | -158.6% | Tier 1 | -1.1400 | -3.1092 | Tier 2 ⚠ |
| wh_winner | 0.1600 | 0.1817 | +13.6% | Tier 1 | 3.0600 | 2.6687 | Tier 1 |
| wh_loser | -0.4800 | -0.3079 | +35.9% | Tier 1 | -4.0700 | -2.9231 | Tier 1 |
| wh_spread | 0.6500 | 0.4896 | -24.7% | Tier 1 | 4.0800 | 3.0233 | Tier 1 |
| jt_spread | 0.3800 | 0.5295 | +39.3% | Tier 1 | 3.7100 | 4.9576 | Tier 1 |
| mg_spread | 0.2500 | 0.3804 | +52.1% | Tier 1 | 2.8300 | 4.6207 | Tier 2 |

### Column: s66_raw_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.8700 | 1.8758 | +0.3% | Tier 1 | 3.5700 | 2.4526 | Tier 1 |
| r_lag1 | -5.5300 | -5.1705 | +6.5% | Tier 1 | -14.8900 | -14.6940 | Tier 1 |
| size | -0.0800 | -0.0584 | +27.0% | Tier 1 | -2.1300 | -1.5209 | Tier 1 |
| jt_winner | 0.1500 | 0.2629 | +75.3% | Tier 1 | 1.6900 | 3.4230 | Tier 2 ⚠ |
| jt_loser | -0.3100 | -0.3820 | -23.2% | Tier 1 | -6.2900 | -7.2274 | Tier 1 |
| mg_winner | 0.1700 | 0.1908 | +12.2% | Tier 1 | 2.5400 | 3.3824 | Tier 1 |
| mg_loser | -0.0500 | -0.1664 | -232.9% | Tier 2 ⚠ | -0.8400 | -2.8038 | Tier 2 ⚠ |
| wh_winner | 0.2700 | 0.3060 | +13.3% | Tier 1 | 5.2500 | 4.7312 | Tier 1 |
| wh_loser | -0.7900 | -0.5685 | +28.0% | Tier 1 | -7.7600 | -6.3840 | Tier 1 |
| wh_spread | 1.0600 | 0.8745 | -17.5% | Tier 1 | 7.6400 | 6.1224 | Tier 1 |
| jt_spread | 0.4600 | 0.6449 | +40.2% | Tier 1 | 4.3900 | 5.9609 | Tier 1 |
| mg_spread | 0.2200 | 0.3573 | +62.4% | Tier 1 | 2.4500 | 4.2135 | Tier 2 |

### Column: s66_ra_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 2.5800 | 3.4600 | +34.1% | Tier 1 | 5.9900 | 5.0616 | Tier 1 |
| r_lag1 | -5.9400 | -5.6203 | +5.4% | Tier 1 | -14.1700 | -14.3671 | Tier 1 |
| size | -0.1700 | -0.1601 | +5.8% | Tier 1 | -5.1100 | -4.5759 | Tier 1 |
| jt_winner | 0.1600 | 0.2658 | +66.1% | Tier 1 | 2.8000 | 4.7670 | Tier 2 |
| jt_loser | -0.2200 | -0.3175 | -44.3% | Tier 1 | -3.8500 | -5.2877 | Tier 1 |
| mg_winner | 0.1900 | 0.1495 | -21.3% | Tier 1 | 2.8500 | 2.6583 | Tier 1 |
| mg_loser | -0.0700 | -0.1906 | -172.3% | Tier 1 | -1.0900 | -3.4587 | Tier 2 ⚠ |
| wh_winner | 0.2700 | 0.2598 | -3.8% | Tier 1 | 6.4900 | 6.1389 | Tier 1 |
| wh_loser | -0.5900 | -0.3318 | +43.8% | Tier 2 | -6.3000 | -3.7348 | Tier 2 |
| wh_spread | 0.8600 | 0.5916 | -31.2% | Tier 1 | 7.2900 | 5.0184 | Tier 1 |
| jt_spread | 0.3800 | 0.5833 | +53.5% | Tier 2 | 4.0200 | 5.8304 | Tier 2 |
| mg_spread | 0.2500 | 0.3400 | +36.0% | Tier 1 | 2.9200 | 4.1393 | Tier 2 |

### Column: s66_ra_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.5500 | 1.7650 | +13.9% | Tier 1 | 4.0200 | 2.9052 | Tier 1 |
| r_lag1 | -5.3600 | -5.1211 | +4.5% | Tier 1 | -14.7800 | -14.7151 | Tier 1 |
| size | -0.0900 | -0.0741 | +17.7% | Tier 1 | -3.0900 | -2.3777 | Tier 1 |
| jt_winner | 0.1600 | 0.2785 | +74.0% | Tier 1 | 2.6900 | 4.9912 | Tier 2 |
| jt_loser | -0.3000 | -0.4091 | -36.4% | Tier 1 | -6.2800 | -7.5988 | Tier 1 |
| mg_winner | 0.1900 | 0.1551 | -18.4% | Tier 1 | 2.7600 | 2.7430 | Tier 1 |
| mg_loser | -0.0500 | -0.1849 | -269.7% | Tier 2 ⚠ | -0.8500 | -3.4019 | Tier 2 ⚠ |
| wh_winner | 0.3200 | 0.3142 | -1.8% | Tier 1 | 7.6600 | 7.9611 | Tier 1 |
| wh_loser | -0.8100 | -0.5294 | +34.6% | Tier 1 | -10.6500 | -7.4466 | Tier 1 |
| wh_spread | 1.1300 | 0.8436 | -25.3% | Tier 1 | 11.3500 | 8.7231 | Tier 1 |
| jt_spread | 0.4600 | 0.6875 | +49.5% | Tier 2 | 5.1300 | 7.2146 | Tier 2 |
| mg_spread | 0.2400 | 0.3399 | +41.6% | Tier 1 | 2.7200 | 4.1042 | Tier 2 |

### Column: s612_raw_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 3.4200 | 4.2765 | +25.0% | Tier 1 | 5.7300 | 4.8573 | Tier 1 |
| r_lag1 | -6.5600 | -6.0420 | +7.9% | Tier 1 | -14.8800 | -14.9335 | Tier 1 |
| size | -0.1900 | -0.1715 | +9.7% | Tier 1 | -4.2700 | -3.9674 | Tier 1 |
| jt_winner | 0.0500 | 0.1646 | +229.2% | Tier 2 ⚠ | 0.6000 | 2.5119 | Tier 2 ⚠ |
| jt_loser | -0.1900 | -0.1649 | +13.2% | Tier 1 | -4.6400 | -3.5416 | Tier 1 |
| mg_winner | 0.1000 | 0.1939 | +93.9% | Tier 1 | 1.8100 | 4.0319 | Tier 2 ⚠ |
| mg_loser | -0.0700 | -0.0720 | -2.8% | Tier 1 | -1.5300 | -1.4175 | Tier 1 |
| wh_winner | 0.1300 | 0.1708 | +31.4% | Tier 1 | 2.8300 | 2.6162 | Tier 1 |
| wh_loser | -0.2600 | -0.1383 | +46.8% | Tier 1 | -2.2900 | -1.4644 | Tier 1 |
| wh_spread | 0.3900 | 0.3091 | -20.8% | Tier 1 | 2.6300 | 2.0668 | Tier 1 |
| jt_spread | 0.2400 | 0.3295 | +37.3% | Tier 1 | 2.7400 | 3.6837 | Tier 1 |
| mg_spread | 0.1700 | 0.2659 | +56.4% | Tier 1 | 2.2300 | 3.7840 | Tier 2 |

### Column: s612_raw_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.6600 | 1.4511 | -12.6% | Tier 1 | 3.1700 | 1.8872 | Tier 2 |
| r_lag1 | -5.5800 | -5.1368 | +7.9% | Tier 1 | -14.9600 | -14.4006 | Tier 1 |
| size | -0.0600 | -0.0390 | +35.0% | Tier 1 | -1.6100 | -1.0167 | Tier 1 |
| jt_winner | 0.0200 | 0.1512 | +656.0% | Tier 2 ⚠ | 0.2200 | 2.2286 | Tier 2 ⚠ |
| jt_loser | -0.2700 | -0.2680 | +0.7% | Tier 1 | -7.5800 | -6.2195 | Tier 1 |
| mg_winner | 0.0900 | 0.1885 | +109.5% | Tier 1 | 1.5600 | 3.8113 | Tier 2 ⚠ |
| mg_loser | -0.0500 | -0.0491 | +1.9% | Tier 1 | -1.1600 | -0.9372 | Tier 1 |
| wh_winner | 0.2200 | 0.2873 | +30.6% | Tier 1 | 5.1900 | 4.5340 | Tier 1 |
| wh_loser | -0.5600 | -0.3858 | +31.1% | Tier 1 | -5.8700 | -4.9324 | Tier 1 |
| wh_spread | 0.7800 | 0.6731 | -13.7% | Tier 1 | 6.1400 | 5.1013 | Tier 1 |
| jt_spread | 0.2900 | 0.4192 | +44.6% | Tier 1 | 3.2500 | 4.5387 | Tier 1 |
| mg_spread | 0.1500 | 0.2376 | +58.4% | Tier 1 | 1.8100 | 3.2255 | Tier 2 |

### Column: s612_ra_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 2.3800 | 3.1079 | +30.6% | Tier 1 | 5.5600 | 4.4858 | Tier 1 |
| r_lag1 | -5.9900 | -5.6029 | +6.5% | Tier 1 | -14.1400 | -14.1054 | Tier 1 |
| size | -0.1600 | -0.1437 | +10.2% | Tier 1 | -4.5800 | -4.0667 | Tier 1 |
| jt_winner | 0.0500 | 0.1733 | +246.6% | Tier 2 ⚠ | 1.1000 | 3.8491 | Tier 2 ⚠ |
| jt_loser | -0.2100 | -0.2411 | -14.8% | Tier 1 | -5.2200 | -5.2436 | Tier 1 |
| mg_winner | 0.1400 | 0.1806 | +29.0% | Tier 1 | 2.4400 | 3.6686 | Tier 2 |
| mg_loser | -0.0900 | -0.1089 | -21.0% | Tier 1 | -1.9800 | -2.4328 | Tier 1 |
| wh_winner | 0.2300 | 0.2360 | +2.6% | Tier 1 | 6.8900 | 6.4282 | Tier 1 |
| wh_loser | -0.3700 | -0.1882 | +49.1% | Tier 2 | -4.2200 | -2.3500 | Tier 2 |
| wh_spread | 0.6000 | 0.4242 | -29.3% | Tier 1 | 5.6100 | 4.0010 | Tier 1 |
| jt_spread | 0.2700 | 0.4144 | +53.5% | Tier 2 | 3.7700 | 5.4966 | Tier 2 |
| mg_spread | 0.2200 | 0.2895 | +31.6% | Tier 1 | 3.1100 | 4.2253 | Tier 1 |

### Column: s612_ra_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.3400 | 1.3587 | +1.4% | Tier 1 | 3.5100 | 2.2215 | Tier 1 |
| r_lag1 | -5.4100 | -5.0922 | +5.9% | Tier 1 | -14.8200 | -14.4362 | Tier 1 |
| size | -0.0700 | -0.0554 | +20.9% | Tier 1 | -2.4400 | -1.7681 | Tier 1 |
| jt_winner | 0.0400 | 0.1767 | +341.8% | Tier 2 ⚠ | 0.7900 | 3.9838 | Tier 2 ⚠ |
| jt_loser | -0.2800 | -0.3159 | -12.8% | Tier 1 | -7.8200 | -7.4777 | Tier 1 |
| mg_winner | 0.1300 | 0.1803 | +38.7% | Tier 1 | 2.1700 | 3.5916 | Tier 2 |
| mg_loser | -0.0700 | -0.0898 | -28.3% | Tier 1 | -1.6500 | -1.9858 | Tier 1 |
| wh_winner | 0.2700 | 0.2905 | +7.6% | Tier 1 | 8.3900 | 8.4058 | Tier 1 |
| wh_loser | -0.5800 | -0.3663 | +36.8% | Tier 1 | -8.3300 | -5.8266 | Tier 1 |
| wh_spread | 0.8500 | 0.6569 | -22.7% | Tier 1 | 9.7300 | 7.6611 | Tier 1 |
| jt_spread | 0.3200 | 0.4926 | +53.9% | Tier 2 | 4.6500 | 6.7084 | Tier 2 |
| mg_spread | 0.2000 | 0.2701 | +35.0% | Tier 1 | 2.6600 | 3.7959 | Tier 2 |