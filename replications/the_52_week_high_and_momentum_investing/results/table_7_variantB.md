# Table VII (variant B adjudication) — George & Hwang (2004): GH dummies from g_gh_b (available-lag reference price, min 24 usable lags; audit1.md [M2])

Each month t (1963-07 .. 2001-12, 462) x formation lag j: one cross-sectional
OLS of R_{it}(%) on R_{i,t-1}(decimal), ln(mcap_$ at t-1), and 8 strategy
dummies (JH/JL<-jt_sig, MH/ML<-mg_sig, GH/GL<-g_gh_b, FHH/FHL<-wh_sig_dc). Dummies from 30/30 ordinal sorts at formation
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
| gh (g_gh_b) | 1573.7 | 2066.5 | 3298.8 | 5185.5 | 5201.6 |
| wh (wh_sig_dc) | 2037.9 | 3988.6 | 5495.1 | 6495.8 | 6265.7 |

## Pre-flight (s66_raw)

| row | ours janincl | paper janincl | ours janexcl |
|---|---:|---:|---:|
| intercept | 4.6560 (t 5.42) | 3.27 | 1.9585 (t 2.58) |
| r_lag1 | -6.1014 (t -15.47) | -7.06 | -5.2231 (t -14.95) |
| size | -0.1929 (t -4.55) | -0.17 | -0.0659 (t -1.73) |
| gh_winner | 0.3031 (t 7.14) | 0.13 | 0.3172 (t 7.36) |
| gh_loser | 0.4172 (t 4.71) | 0.10 | 0.2126 (t 2.79) |
| wh_spread | 0.5238 (t 3.22) | 0.51 | 0.8404 (t 5.62) |

## Diagnostics

- s66: avg sample 4803.6 (min 1962, max 7389), 2772 regressions, 0 empty months
- s612: avg sample 4803.6 (min 1962, max 7389), 5544 regressions, 0 empty months
- FF factors: 462 months aligned, 0 missing

## Overall hit rate (of 240)

**Tier 1: 118 / Tier 2: 108 / FAIL: 14**

### Per-column tally

| column | Tier 1 | Tier 2 | FAIL |
|---|---:|---:|---:|
| s66_raw_janincl | 13 | 15 | 2 |
| s66_raw_janexcl | 12 | 16 | 2 |
| s66_ra_janincl | 15 | 13 | 2 |
| s66_ra_janexcl | 14 | 14 | 2 |
| s612_raw_janincl | 16 | 14 | 0 |
| s612_raw_janexcl | 15 | 11 | 4 |
| s612_ra_janincl | 18 | 12 | 0 |
| s612_ra_janexcl | 15 | 13 | 2 |

_Tier 2 ⚠ = sign matches but |ours/paper| > 2 (magnitude far off; see audit1.md spot-check 10). FAIL cells with |paper| < 0.05 are rounding-boundary artifacts unless noted._

### Column: s66_raw_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 3.2700 | 4.6560 | +42.4% | Tier 2 | 5.7500 | 5.4206 | Tier 1 |
| r_lag1 | -7.0600 | -6.1014 | +13.6% | Tier 1 | -16.0400 | -15.4720 | Tier 1 |
| size | -0.1700 | -0.1929 | -13.5% | Tier 1 | -4.1600 | -4.5460 | Tier 1 |
| jt_winner | 0.1100 | 0.2225 | +102.3% | Tier 1 | 1.3600 | 3.2367 | Tier 2 ⚠ |
| jt_loser | -0.1900 | -0.3135 | -65.0% | Tier 2 | -3.7000 | -5.4883 | Tier 2 |
| mg_winner | 0.1300 | 0.1749 | +34.6% | Tier 1 | 2.1300 | 3.2283 | Tier 2 |
| mg_loser | -0.0700 | -0.2068 | -195.5% | Tier 2 ⚠ | -1.1900 | -3.5980 | Tier 2 ⚠ |
| gh_winner | 0.1300 | 0.3031 | +133.1% | Tier 2 ⚠ | 2.3500 | 7.1354 | Tier 2 ⚠ |
| gh_loser | 0.1000 | 0.4172 | +317.2% | Tier 2 ⚠ | 1.0600 | 4.7071 | Tier 2 ⚠ |
| wh_winner | 0.0900 | 0.1458 | +62.0% | Tier 1 | 1.9200 | 2.1472 | Tier 1 |
| wh_loser | -0.4100 | -0.3780 | +7.8% | Tier 1 | -4.0000 | -3.5867 | Tier 1 |
| wh_spread | 0.5100 | 0.5238 | +2.7% | Tier 1 | 3.7200 | 3.2170 | Tier 1 |
| jt_spread | 0.3000 | 0.5360 | +78.7% | Tier 2 | 3.1400 | 5.3834 | Tier 2 |
| mg_spread | 0.2000 | 0.3818 | +90.9% | Tier 2 | 2.5000 | 4.7050 | Tier 2 |
| gh_spread | 0.0300 | -0.1141 | -480.5% | FAIL | 0.2700 | -1.2016 | FAIL |

### Column: s66_raw_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.7200 | 1.9585 | +13.9% | Tier 1 | 3.3400 | 2.5756 | Tier 1 |
| r_lag1 | -6.0200 | -5.2231 | +13.2% | Tier 1 | -15.5900 | -14.9517 | Tier 1 |
| size | -0.0600 | -0.0659 | -9.8% | Tier 1 | -1.6700 | -1.7319 | Tier 1 |
| jt_winner | 0.0600 | 0.2092 | +248.7% | Tier 2 ⚠ | 0.6900 | 2.8856 | Tier 2 ⚠ |
| jt_loser | -0.2400 | -0.4152 | -73.0% | Tier 2 | -5.0200 | -8.0423 | Tier 2 |
| mg_winner | 0.1000 | 0.1735 | +73.5% | Tier 1 | 1.6400 | 3.1450 | Tier 2 |
| mg_loser | -0.0600 | -0.1843 | -207.1% | Tier 2 ⚠ | -0.9600 | -3.1452 | Tier 2 ⚠ |
| gh_winner | 0.2500 | 0.3172 | +26.9% | Tier 1 | 4.7300 | 7.3603 | Tier 2 |
| gh_loser | -0.1900 | 0.2126 | +211.9% | FAIL | -2.3500 | 2.7926 | FAIL |
| wh_winner | 0.1300 | 0.2516 | +93.5% | Tier 2 | 2.6500 | 3.8200 | Tier 2 |
| wh_loser | -0.6200 | -0.5888 | +5.0% | Tier 1 | -6.8500 | -6.2985 | Tier 1 |
| wh_spread | 0.7500 | 0.8404 | +12.0% | Tier 1 | 6.0500 | 5.6157 | Tier 1 |
| jt_spread | 0.2900 | 0.6244 | +115.3% | Tier 2 ⚠ | 2.9700 | 6.1973 | Tier 2 ⚠ |
| mg_spread | 0.1600 | 0.3578 | +123.6% | Tier 2 ⚠ | 1.9500 | 4.2721 | Tier 2 ⚠ |
| gh_spread | 0.4400 | 0.1046 | -76.2% | Tier 2 | 4.0900 | 1.2247 | Tier 2 |

### Column: s66_ra_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 2.2300 | 3.5375 | +58.6% | Tier 2 | 5.8900 | 5.2866 | Tier 1 |
| r_lag1 | -6.4600 | -5.6583 | +12.4% | Tier 1 | -15.2300 | -14.6150 | Tier 1 |
| size | -0.1400 | -0.1667 | -19.0% | Tier 1 | -4.5100 | -4.8553 | Tier 1 |
| jt_winner | 0.1000 | 0.2200 | +120.0% | Tier 2 ⚠ | 1.7100 | 4.2367 | Tier 2 ⚠ |
| jt_loser | -0.1800 | -0.3482 | -93.4% | Tier 2 | -3.4200 | -5.9651 | Tier 2 |
| mg_winner | 0.1200 | 0.1359 | +13.3% | Tier 1 | 1.8800 | 2.4618 | Tier 1 |
| mg_loser | -0.0800 | -0.2075 | -159.4% | Tier 2 ⚠ | -1.4100 | -3.8018 | Tier 2 ⚠ |
| gh_winner | 0.2300 | 0.2673 | +16.2% | Tier 1 | 4.2200 | 6.1765 | Tier 2 |
| gh_loser | -0.0900 | 0.1601 | +277.9% | FAIL | -1.0700 | 2.1407 | FAIL |
| wh_winner | 0.1400 | 0.2066 | +47.6% | Tier 1 | 3.5700 | 5.0180 | Tier 2 |
| wh_loser | -0.4400 | -0.3544 | +19.5% | Tier 1 | -5.4700 | -4.1790 | Tier 1 |
| wh_spread | 0.5800 | 0.5610 | -3.3% | Tier 1 | 5.9000 | 4.9469 | Tier 1 |
| jt_spread | 0.2700 | 0.5682 | +110.4% | Tier 2 ⚠ | 3.1000 | 5.9797 | Tier 2 |
| mg_spread | 0.2000 | 0.3434 | +71.7% | Tier 1 | 2.5200 | 4.2387 | Tier 2 |
| gh_spread | 0.3200 | 0.1071 | -66.5% | Tier 1 | 2.8800 | 1.2551 | Tier 2 |

### Column: s66_ra_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.4000 | 1.8865 | +34.8% | Tier 1 | 3.9800 | 3.1577 | Tier 1 |
| r_lag1 | -5.8200 | -5.1662 | +11.2% | Tier 1 | -15.2400 | -14.9386 | Tier 1 |
| size | -0.0700 | -0.0828 | -18.3% | Tier 1 | -2.5200 | -2.6956 | Tier 1 |
| jt_winner | 0.0700 | 0.2244 | +220.6% | Tier 2 ⚠ | 1.2600 | 4.3060 | Tier 2 ⚠ |
| jt_loser | -0.2300 | -0.4286 | -86.4% | Tier 2 | -4.9400 | -8.1373 | Tier 2 |
| mg_winner | 0.1100 | 0.1421 | +29.2% | Tier 1 | 1.7100 | 2.5602 | Tier 2 |
| mg_loser | -0.0700 | -0.1976 | -182.3% | Tier 2 ⚠ | -1.1200 | -3.6638 | Tier 2 ⚠ |
| gh_winner | 0.2900 | 0.2940 | +1.4% | Tier 1 | 5.7100 | 6.7901 | Tier 1 |
| gh_loser | -0.2600 | 0.0881 | +133.9% | FAIL | -3.4600 | 1.3191 | FAIL |
| wh_winner | 0.1600 | 0.2519 | +57.5% | Tier 2 | 3.8700 | 6.4568 | Tier 2 |
| wh_loser | -0.6000 | -0.5249 | +12.5% | Tier 1 | -9.3500 | -7.4564 | Tier 1 |
| wh_spread | 0.7600 | 0.7768 | +2.2% | Tier 1 | 9.0900 | 8.0446 | Tier 1 |
| jt_spread | 0.3000 | 0.6530 | +117.7% | Tier 2 ⚠ | 3.4500 | 7.1966 | Tier 2 ⚠ |
| mg_spread | 0.1800 | 0.3397 | +88.7% | Tier 1 | 2.1800 | 4.1487 | Tier 2 |
| gh_spread | 0.5500 | 0.2059 | -62.6% | Tier 2 | 5.6200 | 2.6351 | Tier 2 |

### Column: s612_raw_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 3.0000 | 4.2903 | +43.0% | Tier 2 | 5.2300 | 4.9174 | Tier 1 |
| r_lag1 | -7.1100 | -6.0737 | +14.6% | Tier 1 | -16.0400 | -15.1559 | Tier 1 |
| size | -0.1400 | -0.1758 | -25.5% | Tier 1 | -3.5700 | -4.1034 | Tier 1 |
| jt_winner | 0.0200 | 0.1287 | +543.6% | Tier 2 ⚠ | 0.2100 | 2.0497 | Tier 2 ⚠ |
| jt_loser | -0.1700 | -0.2155 | -26.8% | Tier 1 | -4.6300 | -4.8714 | Tier 1 |
| mg_winner | 0.0700 | 0.1715 | +145.0% | Tier 2 ⚠ | 1.4400 | 3.6534 | Tier 2 ⚠ |
| mg_loser | -0.0600 | -0.0993 | -65.6% | Tier 1 | -1.3600 | -1.9905 | Tier 2 |
| gh_winner | 0.0700 | 0.2617 | +273.8% | Tier 2 ⚠ | 1.2100 | 6.9517 | Tier 2 ⚠ |
| gh_loser | 0.1800 | 0.4142 | +130.1% | Tier 2 ⚠ | 2.0000 | 4.8481 | Tier 2 ⚠ |
| wh_winner | 0.1100 | 0.1435 | +30.5% | Tier 1 | 2.5100 | 2.2102 | Tier 1 |
| wh_loser | -0.2600 | -0.2201 | +15.4% | Tier 1 | -2.7200 | -2.3319 | Tier 1 |
| wh_spread | 0.3600 | 0.3636 | +1.0% | Tier 1 | 2.9300 | 2.4183 | Tier 1 |
| jt_spread | 0.1900 | 0.3442 | +81.2% | Tier 1 | 2.3700 | 4.1672 | Tier 2 |
| mg_spread | 0.1300 | 0.2709 | +108.4% | Tier 2 ⚠ | 1.9100 | 3.8998 | Tier 2 ⚠ |
| gh_spread | -0.1100 | -0.1526 | -38.7% | Tier 1 | -0.9400 | -1.7316 | Tier 2 |

### Column: s612_raw_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.4100 | 1.5176 | +7.6% | Tier 1 | 2.7200 | 1.9795 | Tier 1 |
| r_lag1 | -6.0600 | -5.1816 | +14.5% | Tier 1 | -15.6300 | -14.6290 | Tier 1 |
| size | -0.0300 | -0.0453 | -50.9% | Tier 1 | -0.9500 | -1.1867 | Tier 1 |
| jt_winner | -0.0400 | 0.1081 | +370.1% | FAIL | -0.4900 | 1.6597 | FAIL |
| jt_loser | -0.2100 | -0.3031 | -44.3% | Tier 2 | -6.0000 | -7.4295 | Tier 1 |
| mg_winner | 0.0600 | 0.1725 | +187.6% | Tier 2 ⚠ | 1.1200 | 3.5724 | Tier 2 ⚠ |
| mg_loser | -0.0400 | -0.0689 | -72.3% | Tier 1 | -0.9400 | -1.3408 | Tier 2 |
| gh_winner | 0.1600 | 0.2734 | +70.9% | Tier 2 | 3.2200 | 7.1182 | Tier 2 ⚠ |
| gh_loser | -0.0800 | 0.2315 | +389.3% | FAIL | -1.0100 | 3.1779 | FAIL |
| wh_winner | 0.1400 | 0.2437 | +74.0% | Tier 2 | 3.3900 | 3.8002 | Tier 1 |
| wh_loser | -0.4700 | -0.4233 | +9.9% | Tier 1 | -5.6800 | -5.1393 | Tier 1 |
| wh_spread | 0.6100 | 0.6670 | +9.3% | Tier 1 | 5.4700 | 4.8267 | Tier 1 |
| jt_spread | 0.1800 | 0.4112 | +128.4% | Tier 2 ⚠ | 2.1200 | 4.8088 | Tier 2 ⚠ |
| mg_spread | 0.1000 | 0.2415 | +141.5% | Tier 1 | 1.4000 | 3.3150 | Tier 2 ⚠ |
| gh_spread | 0.2400 | 0.0419 | -82.5% | Tier 1 | 2.3900 | 0.5432 | Tier 2 |

### Column: s612_ra_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.8400 | 3.1749 | +72.5% | Tier 2 | 4.9200 | 4.6560 | Tier 1 |
| r_lag1 | -6.5300 | -5.6340 | +13.7% | Tier 1 | -15.2000 | -14.3149 | Tier 1 |
| size | -0.1000 | -0.1493 | -49.3% | Tier 1 | -3.4700 | -4.2875 | Tier 1 |
| jt_winner | 0.0400 | 0.1392 | +248.0% | Tier 2 ⚠ | 0.7500 | 3.2792 | Tier 2 ⚠ |
| jt_loser | -0.1800 | -0.2702 | -50.1% | Tier 2 | -4.7700 | -6.0640 | Tier 1 |
| mg_winner | 0.0900 | 0.1666 | +85.2% | Tier 1 | 1.8300 | 3.4590 | Tier 2 |
| mg_loser | -0.0900 | -0.1253 | -39.2% | Tier 1 | -2.0600 | -2.8204 | Tier 1 |
| gh_winner | 0.1300 | 0.2202 | +69.4% | Tier 1 | 2.6400 | 5.7650 | Tier 2 ⚠ |
| gh_loser | 0.0100 | 0.1635 | +1534.6% | Tier 2 ⚠ | 0.0900 | 2.2863 | Tier 2 ⚠ |
| wh_winner | 0.1500 | 0.1955 | +30.3% | Tier 1 | 4.7300 | 5.4710 | Tier 1 |
| wh_loser | -0.2900 | -0.2214 | +23.7% | Tier 1 | -4.0100 | -2.8919 | Tier 1 |
| wh_spread | 0.4400 | 0.4169 | -5.3% | Tier 1 | 5.0900 | 4.0763 | Tier 1 |
| jt_spread | 0.2100 | 0.4094 | +95.0% | Tier 2 | 3.1700 | 5.7403 | Tier 2 |
| mg_spread | 0.1800 | 0.2920 | +62.2% | Tier 1 | 2.7400 | 4.3085 | Tier 2 |
| gh_spread | 0.1300 | 0.0567 | -56.4% | Tier 1 | 1.2500 | 0.7223 | Tier 2 |

### Column: s612_ra_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.0100 | 1.4552 | +44.1% | Tier 1 | 2.9000 | 2.4099 | Tier 1 |
| r_lag1 | -5.8800 | -5.1300 | +12.8% | Tier 1 | -15.2200 | -14.6316 | Tier 1 |
| size | -0.0400 | -0.0624 | -56.0% | Tier 1 | -1.3600 | -2.0152 | Tier 2 |
| jt_winner | 0.0000 | 0.1351 | n/a | Tier 2 ⚠ | 0.0000 | 3.2208 | Tier 2 ⚠ |
| jt_loser | -0.2200 | -0.3375 | -53.4% | Tier 2 | -6.1700 | -8.2573 | Tier 1 |
| mg_winner | 0.0800 | 0.1680 | +110.0% | Tier 1 | 1.5600 | 3.4202 | Tier 2 ⚠ |
| mg_loser | -0.0700 | -0.1043 | -49.0% | Tier 1 | -1.6200 | -2.3252 | Tier 2 |
| gh_winner | 0.1900 | 0.2456 | +29.2% | Tier 1 | 3.8700 | 6.3891 | Tier 2 |
| gh_loser | -0.1400 | 0.1119 | +179.9% | FAIL | -1.9700 | 1.7546 | FAIL |
| wh_winner | 0.1700 | 0.2419 | +42.3% | Tier 2 | 5.2100 | 7.0494 | Tier 1 |
| wh_loser | -0.4500 | -0.3788 | +15.8% | Tier 1 | -7.8200 | -6.0825 | Tier 1 |
| wh_spread | 0.6200 | 0.6206 | +0.1% | Tier 1 | 8.6200 | 7.2206 | Tier 1 |
| jt_spread | 0.2200 | 0.4726 | +114.8% | Tier 2 ⚠ | 3.1800 | 6.7764 | Tier 2 ⚠ |
| mg_spread | 0.1500 | 0.2723 | +81.5% | Tier 1 | 2.2300 | 3.8663 | Tier 2 |
| gh_spread | 0.3300 | 0.1337 | -59.5% | Tier 2 | 3.5600 | 1.8931 | Tier 2 |
---

## Before/after: variant A (g_gh, official) vs variant B (g_gh_b)

Variant A cells recomputed from the official `data/fm_coefficients_gh.parquet` with the identical engine functions (the auditor independently verified that cache -> 4dp in audit1.md; the reconstruction above also reproduces the official tally 122/102/16); variant B from this run (dependent `ret_dl`, same as the official Table VII).

### Per-column tally (A vs B)

| column | A: T1/T2/FAIL | B: T1/T2/FAIL |
|---|---|---|
| s66_raw_janincl | 14/14/2 | 13/15/2 |
| s66_raw_janexcl | 14/14/2 | 12/16/2 |
| s66_ra_janincl | 14/14/2 | 15/13/2 |
| s66_ra_janexcl | 15/13/2 | 14/14/2 |
| s612_raw_janincl | 17/13/0 | 16/14/0 |
| s612_raw_janexcl | 15/9/6 | 15/11/4 |
| s612_ra_janincl | 17/13/0 | 18/12/0 |
| s612_ra_janexcl | 16/12/2 | 15/13/2 |
| **total** | **122/102/16** | **118/108/14** |

### gh_* cells — all 8 columns (A vs B vs paper; values + t-stats)

| column | row | paper | A | B | paper_t | A_t | B_t | tier_B | tier_t_B |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| s66_raw_janincl | gh_winner | 0.1300 | 0.2696 | 0.3031 | 2.3500 | 6.0455 | 7.1354 | Tier 2 | Tier 2 |
| s66_raw_janincl | gh_loser | 0.1000 | 0.3961 | 0.4172 | 1.0600 | 4.7179 | 4.7071 | Tier 2 | Tier 2 |
| s66_raw_janincl | gh_spread | 0.0300 | -0.1265 | -0.1141 | 0.2700 | -1.4529 | -1.2016 | FAIL | FAIL |
| s66_raw_janexcl | gh_winner | 0.2500 | 0.2694 | 0.3172 | 4.7300 | 5.8429 | 7.3603 | Tier 1 | Tier 2 |
| s66_raw_janexcl | gh_loser | -0.1900 | 0.2572 | 0.2126 | -2.3500 | 3.4211 | 2.7926 | FAIL | FAIL |
| s66_raw_janexcl | gh_spread | 0.4400 | 0.0123 | 0.1046 | 4.0900 | 0.1547 | 1.2247 | Tier 2 | Tier 2 |
| s66_ra_janincl | gh_winner | 0.2300 | 0.2174 | 0.2673 | 4.2200 | 4.8750 | 6.1765 | Tier 1 | Tier 2 |
| s66_ra_janincl | gh_loser | -0.0900 | 0.1605 | 0.1601 | -1.0700 | 2.3394 | 2.1407 | FAIL | FAIL |
| s66_ra_janincl | gh_spread | 0.3200 | 0.0569 | 0.1071 | 2.8800 | 0.7101 | 1.2551 | Tier 1 | Tier 2 |
| s66_ra_janexcl | gh_winner | 0.2900 | 0.2278 | 0.2940 | 5.7100 | 4.9993 | 6.7901 | Tier 1 | Tier 1 |
| s66_ra_janexcl | gh_loser | -0.2600 | 0.1302 | 0.0881 | -3.4600 | 2.0779 | 1.3191 | FAIL | FAIL |
| s66_ra_janexcl | gh_spread | 0.5500 | 0.0976 | 0.2059 | 5.6200 | 1.3061 | 2.6351 | Tier 2 | Tier 2 |
| s612_raw_janincl | gh_winner | 0.0700 | 0.2414 | 0.2617 | 1.2100 | 5.7809 | 6.9517 | Tier 2 | Tier 2 |
| s612_raw_janincl | gh_loser | 0.1800 | 0.3763 | 0.4142 | 2.0000 | 4.6799 | 4.8481 | Tier 2 | Tier 2 |
| s612_raw_janincl | gh_spread | -0.1100 | -0.1349 | -0.1526 | -0.9400 | -1.6834 | -1.7316 | Tier 1 | Tier 2 |
| s612_raw_janexcl | gh_winner | 0.1600 | 0.2406 | 0.2734 | 3.2200 | 5.5626 | 7.1182 | Tier 2 | Tier 2 |
| s612_raw_janexcl | gh_loser | -0.0800 | 0.2498 | 0.2315 | -1.0100 | 3.4644 | 3.1779 | FAIL | FAIL |
| s612_raw_janexcl | gh_spread | 0.2400 | -0.0092 | 0.0419 | 2.3900 | -0.1273 | 0.5432 | Tier 1 | Tier 2 |
| s612_ra_janincl | gh_winner | 0.1300 | 0.1874 | 0.2202 | 2.6400 | 4.5688 | 5.7650 | Tier 1 | Tier 2 |
| s612_ra_janincl | gh_loser | 0.0100 | 0.1490 | 0.1635 | 0.0900 | 2.2749 | 2.2863 | Tier 2 | Tier 2 |
| s612_ra_janincl | gh_spread | 0.1300 | 0.0384 | 0.0567 | 1.2500 | 0.5217 | 0.7223 | Tier 1 | Tier 2 |
| s612_ra_janexcl | gh_winner | 0.1900 | 0.1969 | 0.2456 | 3.8700 | 4.6938 | 6.3891 | Tier 1 | Tier 2 |
| s612_ra_janexcl | gh_loser | -0.1400 | 0.1280 | 0.1119 | -1.9700 | 2.1233 | 1.7546 | FAIL | FAIL |
| s612_ra_janexcl | gh_spread | 0.3300 | 0.0689 | 0.1337 | 3.5600 | 1.0088 | 1.8931 | Tier 2 | Tier 2 |

### wh_spread identity assertion (A vs B, 16 cells)

**NOT bit-identical: 16/16 cells differ; max |A-B| = 0.417717.** Spec flag: the task expected identity since the WH signal does not use g_gh — the WH dummy matrix IS identical, but the FM regression is joint (GH/GL dummies are regressors in the same cross-sectional OLS), so by Frisch-Waugh the WH coefficients shift when the GH columns change. Substantive check: 16/16 wh_spread cells are Tier 1 under B.

| column | kind | A | B | \|A-B\| | identical | tier_B |
|---|---|---:|---:|---:|---|---|
| s66_raw_janincl | wh_spread val | 0.5203 | 0.5238 | 3.52e-03 | False | Tier 1 |
| s66_raw_janincl | wh_spread tstat | 3.1881 | 3.2170 | 2.89e-02 | False | Tier 1 |
| s66_raw_janexcl | wh_spread val | 0.8747 | 0.8404 | 3.44e-02 | False | Tier 1 |
| s66_raw_janexcl | wh_spread tstat | 5.9604 | 5.6157 | 3.45e-01 | False | Tier 1 |
| s66_ra_janincl | wh_spread val | 0.5851 | 0.5610 | 2.41e-02 | False | Tier 1 |
| s66_ra_janincl | wh_spread tstat | 5.0066 | 4.9469 | 5.98e-02 | False | Tier 1 |
| s66_ra_janexcl | wh_spread val | 0.8254 | 0.7768 | 4.86e-02 | False | Tier 1 |
| s66_ra_janexcl | wh_spread tstat | 8.4623 | 8.0446 | 4.18e-01 | False | Tier 1 |
| s612_raw_janincl | wh_spread val | 0.3461 | 0.3636 | 1.75e-02 | False | Tier 1 |
| s612_raw_janincl | wh_spread tstat | 2.3003 | 2.4183 | 1.18e-01 | False | Tier 1 |
| s612_raw_janexcl | wh_spread val | 0.6826 | 0.6670 | 1.57e-02 | False | Tier 1 |
| s612_raw_janexcl | wh_spread tstat | 5.0440 | 4.8267 | 2.17e-01 | False | Tier 1 |
| s612_ra_janincl | wh_spread val | 0.4262 | 0.4169 | 9.32e-03 | False | Tier 1 |
| s612_ra_janincl | wh_spread tstat | 4.0497 | 4.0763 | 2.65e-02 | False | Tier 1 |
| s612_ra_janexcl | wh_spread val | 0.6497 | 0.6206 | 2.91e-02 | False | Tier 1 |
| s612_ra_janexcl | wh_spread tstat | 7.4939 | 7.2206 | 2.73e-01 | False | Tier 1 |

### Adoption criteria (audit1.md [M2])

Adopt variant B iff ALL hold:

1. Total Table VII Tier-1 count rises above A's 122: **B = 118** -> FAIL.
2. gh_spread s66_raw_janexcl moves from 0.0123 toward 0.44 (closer in absolute terms): **B = 0.1046**, |B-paper| = 0.3354 vs |A-paper| = 0.4277 -> PASS.
3. All 16 wh_spread cells remain Tier 1: **16/16** -> PASS.

Anchors:
- gh_loser s66_raw_janexcl: A +0.2572 -> B +0.2126 (t 2.79; paper -0.19).
- gh_spread s66_ra_janexcl: A 0.0976 -> B 0.2059 (t 2.64; paper 0.55).

**Recommendation: KEEP variant A** (worker implements the pre-committed rule; the Replicator ratifies).
