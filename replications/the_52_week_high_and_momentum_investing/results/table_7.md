# Table VII — George & Hwang (2004): Table V + Grinblatt-Han embedded-capital-gain dummies

Each month t (1963-07 .. 2001-12, 462) x formation lag j: one cross-sectional
OLS of R_{it}(%) on R_{i,t-1}(decimal), ln(mcap_$ at t-1), and 8 strategy
dummies (JH/JL<-jt_sig, MH/ML<-mg_sig, GH/GL<-g_gh, FHH/FHL<-wh_sig_dc). Dummies from 30/30 ordinal sorts at formation
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
| gh (g_gh) | 1013.0 | 1677.8 | 1960.2 | 3742.9 | 3763.2 |
| wh (wh_sig_dc) | 2037.9 | 3988.6 | 5495.1 | 6495.8 | 6265.7 |

## Pre-flight (s66_raw)

| row | ours janincl | paper janincl | ours janexcl |
|---|---:|---:|---:|
| intercept | 4.7743 (t 5.51) | 3.27 | 2.0209 (t 2.65) |
| r_lag1 | -6.0908 (t -15.41) | -7.06 | -5.2090 (t -14.90) |
| size | -0.1986 (t -4.63) | -0.17 | -0.0688 (t -1.80) |
| gh_winner | 0.2696 (t 6.05) | 0.13 | 0.2694 (t 5.84) |
| gh_loser | 0.3961 (t 4.72) | 0.10 | 0.2572 (t 3.42) |
| wh_spread | 0.5203 (t 3.19) | 0.51 | 0.8747 (t 5.96) |

## Diagnostics

- s66: avg sample 4803.6 (min 1962, max 7389), 2772 regressions, 0 empty months
- s612: avg sample 4803.6 (min 1962, max 7389), 5544 regressions, 0 empty months
- FF factors: 462 months aligned, 0 missing

## Overall hit rate (of 240)

**Tier 1: 122 / Tier 2: 102 / FAIL: 16**

### Per-column tally

| column | Tier 1 | Tier 2 | FAIL |
|---|---:|---:|---:|
| s66_raw_janincl | 14 | 14 | 2 |
| s66_raw_janexcl | 14 | 14 | 2 |
| s66_ra_janincl | 14 | 14 | 2 |
| s66_ra_janexcl | 15 | 13 | 2 |
| s612_raw_janincl | 17 | 13 | 0 |
| s612_raw_janexcl | 15 | 9 | 6 |
| s612_ra_janincl | 17 | 13 | 0 |
| s612_ra_janexcl | 16 | 12 | 2 |

_Tier 2 ⚠ = sign matches but |ours/paper| > 2 (magnitude far off; see audit1.md spot-check 10). FAIL cells with |paper| < 0.05 are rounding-boundary artifacts unless noted._

### Column: s66_raw_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 3.2700 | 4.7743 | +46.0% | Tier 2 | 5.7500 | 5.5146 | Tier 1 |
| r_lag1 | -7.0600 | -6.0908 | +13.7% | Tier 1 | -16.0400 | -15.4073 | Tier 1 |
| size | -0.1700 | -0.1986 | -16.8% | Tier 1 | -4.1600 | -4.6324 | Tier 1 |
| jt_winner | 0.1100 | 0.2491 | +126.5% | Tier 1 | 1.3600 | 3.4623 | Tier 2 ⚠ |
| jt_loser | -0.1900 | -0.2953 | -55.4% | Tier 2 | -3.7000 | -5.0668 | Tier 1 |
| mg_winner | 0.1300 | 0.1843 | +41.8% | Tier 1 | 2.1300 | 3.3858 | Tier 2 |
| mg_loser | -0.0700 | -0.2000 | -185.6% | Tier 2 ⚠ | -1.1900 | -3.4905 | Tier 2 ⚠ |
| gh_winner | 0.1300 | 0.2696 | +107.4% | Tier 2 ⚠ | 2.3500 | 6.0455 | Tier 2 ⚠ |
| gh_loser | 0.1000 | 0.3961 | +296.1% | Tier 2 ⚠ | 1.0600 | 4.7179 | Tier 2 ⚠ |
| wh_winner | 0.0900 | 0.1689 | +87.7% | Tier 1 | 1.9200 | 2.5135 | Tier 1 |
| wh_loser | -0.4100 | -0.3514 | +14.3% | Tier 1 | -4.0000 | -3.2953 | Tier 1 |
| wh_spread | 0.5100 | 0.5203 | +2.0% | Tier 1 | 3.7200 | 3.1881 | Tier 1 |
| jt_spread | 0.3000 | 0.5444 | +81.5% | Tier 2 | 3.1400 | 5.2637 | Tier 2 |
| mg_spread | 0.2000 | 0.3843 | +92.1% | Tier 2 | 2.5000 | 4.7585 | Tier 2 |
| gh_spread | 0.0300 | -0.1265 | -521.8% | FAIL | 0.2700 | -1.4529 | FAIL |

### Column: s66_raw_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.7200 | 2.0209 | +17.5% | Tier 1 | 3.3400 | 2.6518 | Tier 1 |
| r_lag1 | -6.0200 | -5.2090 | +13.5% | Tier 1 | -15.5900 | -14.9025 | Tier 1 |
| size | -0.0600 | -0.0688 | -14.7% | Tier 1 | -1.6700 | -1.7974 | Tier 1 |
| jt_winner | 0.0600 | 0.2415 | +302.5% | Tier 2 ⚠ | 0.6900 | 3.1841 | Tier 2 ⚠ |
| jt_loser | -0.2400 | -0.4070 | -69.6% | Tier 2 | -5.0200 | -7.8050 | Tier 2 |
| mg_winner | 0.1000 | 0.1817 | +81.7% | Tier 1 | 1.6400 | 3.2768 | Tier 2 |
| mg_loser | -0.0600 | -0.1793 | -198.8% | Tier 1 | -0.9600 | -3.0669 | Tier 2 ⚠ |
| gh_winner | 0.2500 | 0.2694 | +7.8% | Tier 1 | 4.7300 | 5.8429 | Tier 1 |
| gh_loser | -0.1900 | 0.2572 | +235.3% | FAIL | -2.3500 | 3.4211 | FAIL |
| wh_winner | 0.1300 | 0.2839 | +118.4% | Tier 2 ⚠ | 2.6500 | 4.4048 | Tier 2 |
| wh_loser | -0.6200 | -0.5908 | +4.7% | Tier 1 | -6.8500 | -6.3965 | Tier 1 |
| wh_spread | 0.7500 | 0.8747 | +16.6% | Tier 1 | 6.0500 | 5.9604 | Tier 1 |
| jt_spread | 0.2900 | 0.6485 | +123.6% | Tier 2 ⚠ | 2.9700 | 6.2043 | Tier 2 ⚠ |
| mg_spread | 0.1600 | 0.3609 | +125.6% | Tier 2 ⚠ | 1.9500 | 4.3260 | Tier 2 ⚠ |
| gh_spread | 0.4400 | 0.0123 | -97.2% | Tier 2 | 4.0900 | 0.1547 | Tier 2 |

### Column: s66_ra_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 2.2300 | 3.6109 | +61.9% | Tier 2 | 5.8900 | 5.3167 | Tier 1 |
| r_lag1 | -6.4600 | -5.6467 | +12.6% | Tier 1 | -15.2300 | -14.5474 | Tier 1 |
| size | -0.1400 | -0.1700 | -21.4% | Tier 1 | -4.5100 | -4.8827 | Tier 1 |
| jt_winner | 0.1000 | 0.2493 | +149.3% | Tier 2 ⚠ | 1.7100 | 4.5987 | Tier 2 ⚠ |
| jt_loser | -0.1800 | -0.3367 | -87.1% | Tier 2 | -3.4200 | -5.6558 | Tier 2 |
| mg_winner | 0.1200 | 0.1417 | +18.1% | Tier 1 | 1.8800 | 2.5602 | Tier 1 |
| mg_loser | -0.0800 | -0.2035 | -154.4% | Tier 2 ⚠ | -1.4100 | -3.7240 | Tier 2 ⚠ |
| gh_winner | 0.2300 | 0.2174 | -5.5% | Tier 1 | 4.2200 | 4.8750 | Tier 1 |
| gh_loser | -0.0900 | 0.1605 | +278.3% | FAIL | -1.0700 | 2.3394 | FAIL |
| wh_winner | 0.1400 | 0.2363 | +68.8% | Tier 2 | 3.5700 | 5.6452 | Tier 2 |
| wh_loser | -0.4400 | -0.3488 | +20.7% | Tier 1 | -5.4700 | -3.9803 | Tier 1 |
| wh_spread | 0.5800 | 0.5851 | +0.9% | Tier 1 | 5.9000 | 5.0066 | Tier 1 |
| jt_spread | 0.2700 | 0.5860 | +117.0% | Tier 2 ⚠ | 3.1000 | 5.9844 | Tier 2 |
| mg_spread | 0.2000 | 0.3452 | +72.6% | Tier 1 | 2.5200 | 4.2740 | Tier 2 |
| gh_spread | 0.3200 | 0.0569 | -82.2% | Tier 2 | 2.8800 | 0.7101 | Tier 2 |

### Column: s66_ra_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.4000 | 1.9200 | +37.1% | Tier 1 | 3.9800 | 3.1781 | Tier 1 |
| r_lag1 | -5.8200 | -5.1539 | +11.4% | Tier 1 | -15.2400 | -14.8944 | Tier 1 |
| size | -0.0700 | -0.0841 | -20.1% | Tier 1 | -2.5200 | -2.7097 | Tier 1 |
| jt_winner | 0.0700 | 0.2595 | +270.7% | Tier 2 ⚠ | 1.2600 | 4.7839 | Tier 2 ⚠ |
| jt_loser | -0.2300 | -0.4249 | -84.8% | Tier 2 | -4.9400 | -7.9834 | Tier 2 |
| mg_winner | 0.1100 | 0.1484 | +34.9% | Tier 1 | 1.7100 | 2.6668 | Tier 2 |
| mg_loser | -0.0700 | -0.1937 | -176.7% | Tier 1 | -1.1200 | -3.5796 | Tier 2 ⚠ |
| gh_winner | 0.2900 | 0.2278 | -21.5% | Tier 1 | 5.7100 | 4.9993 | Tier 1 |
| gh_loser | -0.2600 | 0.1302 | +150.1% | FAIL | -3.4600 | 2.0779 | FAIL |
| wh_winner | 0.1600 | 0.2884 | +80.3% | Tier 2 | 3.8700 | 7.3223 | Tier 2 |
| wh_loser | -0.6000 | -0.5369 | +10.5% | Tier 1 | -9.3500 | -7.5273 | Tier 1 |
| wh_spread | 0.7600 | 0.8254 | +8.6% | Tier 1 | 9.0900 | 8.4623 | Tier 1 |
| jt_spread | 0.3000 | 0.6844 | +128.1% | Tier 2 ⚠ | 3.4500 | 7.3548 | Tier 2 ⚠ |
| mg_spread | 0.1800 | 0.3422 | +90.1% | Tier 1 | 2.1800 | 4.1854 | Tier 2 |
| gh_spread | 0.5500 | 0.0976 | -82.3% | Tier 2 | 5.6200 | 1.3061 | Tier 2 |

### Column: s612_raw_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 3.0000 | 4.3926 | +46.4% | Tier 2 | 5.2300 | 5.0092 | Tier 1 |
| r_lag1 | -7.1100 | -6.0652 | +14.7% | Tier 1 | -16.0400 | -15.1065 | Tier 1 |
| size | -0.1400 | -0.1806 | -29.0% | Tier 1 | -3.5700 | -4.1848 | Tier 1 |
| jt_winner | 0.0200 | 0.1486 | +642.9% | Tier 2 ⚠ | 0.2100 | 2.2769 | Tier 2 ⚠ |
| jt_loser | -0.1700 | -0.1975 | -16.2% | Tier 1 | -4.6300 | -4.3656 | Tier 1 |
| mg_winner | 0.0700 | 0.1783 | +154.7% | Tier 2 ⚠ | 1.4400 | 3.7904 | Tier 2 ⚠ |
| mg_loser | -0.0600 | -0.0930 | -55.1% | Tier 1 | -1.3600 | -1.8735 | Tier 1 |
| gh_winner | 0.0700 | 0.2414 | +244.8% | Tier 2 ⚠ | 1.2100 | 5.7809 | Tier 2 ⚠ |
| gh_loser | 0.1800 | 0.3763 | +109.1% | Tier 2 ⚠ | 2.0000 | 4.6799 | Tier 2 ⚠ |
| wh_winner | 0.1100 | 0.1603 | +45.8% | Tier 1 | 2.5100 | 2.5098 | Tier 1 |
| wh_loser | -0.2600 | -0.1858 | +28.6% | Tier 1 | -2.7200 | -1.9387 | Tier 1 |
| wh_spread | 0.3600 | 0.3461 | -3.9% | Tier 1 | 2.9300 | 2.3003 | Tier 1 |
| jt_spread | 0.1900 | 0.3461 | +82.2% | Tier 1 | 2.3700 | 4.0326 | Tier 2 |
| mg_spread | 0.1300 | 0.2713 | +108.7% | Tier 2 ⚠ | 1.9100 | 3.9366 | Tier 2 ⚠ |
| gh_spread | -0.1100 | -0.1349 | -22.7% | Tier 1 | -0.9400 | -1.6834 | Tier 2 |

### Column: s612_raw_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.4100 | 1.5746 | +11.7% | Tier 1 | 2.7200 | 2.0540 | Tier 1 |
| r_lag1 | -6.0600 | -5.1711 | +14.7% | Tier 1 | -15.6300 | -14.5927 | Tier 1 |
| size | -0.0300 | -0.0478 | -59.4% | Tier 1 | -0.9500 | -1.2487 | Tier 1 |
| jt_winner | -0.0400 | 0.1323 | +430.8% | FAIL | -0.4900 | 1.9549 | FAIL |
| jt_loser | -0.2100 | -0.2947 | -40.3% | Tier 2 | -6.0000 | -7.1148 | Tier 1 |
| mg_winner | 0.0600 | 0.1788 | +198.0% | Tier 2 ⚠ | 1.1200 | 3.6917 | Tier 2 ⚠ |
| mg_loser | -0.0400 | -0.0647 | -61.7% | Tier 1 | -0.9400 | -1.2632 | Tier 1 |
| gh_winner | 0.1600 | 0.2406 | +50.4% | Tier 1 | 3.2200 | 5.5626 | Tier 2 |
| gh_loser | -0.0800 | 0.2498 | +412.3% | FAIL | -1.0100 | 3.4644 | FAIL |
| wh_winner | 0.1400 | 0.2683 | +91.7% | Tier 2 | 3.3900 | 4.3008 | Tier 1 |
| wh_loser | -0.4700 | -0.4143 | +11.8% | Tier 1 | -5.6800 | -5.0734 | Tier 1 |
| wh_spread | 0.6100 | 0.6826 | +11.9% | Tier 1 | 5.4700 | 5.0440 | Tier 1 |
| jt_spread | 0.1800 | 0.4270 | +137.2% | Tier 2 ⚠ | 2.1200 | 4.8128 | Tier 2 ⚠ |
| mg_spread | 0.1000 | 0.2435 | +143.5% | Tier 2 ⚠ | 1.4000 | 3.3650 | Tier 2 ⚠ |
| gh_spread | 0.2400 | -0.0092 | -103.8% | FAIL | 2.3900 | -0.1273 | FAIL |

### Column: s612_ra_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.8400 | 3.2295 | +75.5% | Tier 2 | 4.9200 | 4.6854 | Tier 1 |
| r_lag1 | -6.5300 | -5.6259 | +13.8% | Tier 1 | -15.2000 | -14.2670 | Tier 1 |
| size | -0.1000 | -0.1516 | -51.6% | Tier 1 | -3.4700 | -4.3084 | Tier 1 |
| jt_winner | 0.0400 | 0.1601 | +300.1% | Tier 2 ⚠ | 0.7500 | 3.6397 | Tier 2 ⚠ |
| jt_loser | -0.1800 | -0.2600 | -44.4% | Tier 2 | -4.7700 | -5.7426 | Tier 1 |
| mg_winner | 0.0900 | 0.1699 | +88.8% | Tier 1 | 1.8300 | 3.5242 | Tier 2 |
| mg_loser | -0.0900 | -0.1216 | -35.1% | Tier 1 | -2.0600 | -2.7319 | Tier 1 |
| gh_winner | 0.1300 | 0.1874 | +44.1% | Tier 1 | 2.6400 | 4.5688 | Tier 2 |
| gh_loser | 0.0100 | 0.1490 | +1389.9% | Tier 2 ⚠ | 0.0900 | 2.2749 | Tier 2 ⚠ |
| wh_winner | 0.1500 | 0.2176 | +45.1% | Tier 2 | 4.7300 | 6.0303 | Tier 1 |
| wh_loser | -0.2900 | -0.2086 | +28.1% | Tier 1 | -4.0100 | -2.6298 | Tier 1 |
| wh_spread | 0.4400 | 0.4262 | -3.1% | Tier 1 | 5.0900 | 4.0497 | Tier 1 |
| jt_spread | 0.2100 | 0.4201 | +100.0% | Tier 2 ⚠ | 3.1700 | 5.7325 | Tier 2 |
| mg_spread | 0.1800 | 0.2915 | +61.9% | Tier 1 | 2.7400 | 4.3194 | Tier 2 |
| gh_spread | 0.1300 | 0.0384 | -70.5% | Tier 1 | 1.2500 | 0.5217 | Tier 2 |

### Column: s612_ra_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.0100 | 1.4818 | +46.7% | Tier 1 | 2.9000 | 2.4334 | Tier 1 |
| r_lag1 | -5.8800 | -5.1215 | +12.9% | Tier 1 | -15.2200 | -14.6029 | Tier 1 |
| size | -0.0400 | -0.0633 | -58.2% | Tier 1 | -1.3600 | -2.0273 | Tier 2 |
| jt_winner | 0.0000 | 0.1610 | n/a | Tier 2 ⚠ | 0.0000 | 3.7112 | Tier 2 ⚠ |
| jt_loser | -0.2200 | -0.3332 | -51.5% | Tier 2 | -6.1700 | -8.0744 | Tier 1 |
| mg_winner | 0.0800 | 0.1721 | +115.1% | Tier 1 | 1.5600 | 3.4982 | Tier 2 ⚠ |
| mg_loser | -0.0700 | -0.1005 | -43.6% | Tier 1 | -1.6200 | -2.2331 | Tier 1 |
| gh_winner | 0.1900 | 0.1969 | +3.6% | Tier 1 | 3.8700 | 4.6938 | Tier 1 |
| gh_loser | -0.1400 | 0.1280 | +191.4% | FAIL | -1.9700 | 2.1233 | FAIL |
| wh_winner | 0.1700 | 0.2702 | +58.9% | Tier 2 | 5.2100 | 7.8900 | Tier 2 |
| wh_loser | -0.4500 | -0.3795 | +15.7% | Tier 1 | -7.8200 | -5.9832 | Tier 1 |
| wh_spread | 0.6200 | 0.6497 | +4.8% | Tier 1 | 8.6200 | 7.4939 | Tier 1 |
| jt_spread | 0.2200 | 0.4942 | +124.6% | Tier 2 ⚠ | 3.1800 | 6.9276 | Tier 2 ⚠ |
| mg_spread | 0.1500 | 0.2726 | +81.7% | Tier 1 | 2.2300 | 3.8822 | Tier 2 |
| gh_spread | 0.3300 | 0.0689 | -79.1% | Tier 2 | 3.5600 | 1.0088 | Tier 2 |