# Table V (A13 rankable-only sensitivity) — George & Hwang (2004): FM cross-sections restricted to stocks rankable on jt AND mg AND wh simultaneously (audit1.md [M3])

Each month t (1963-07 .. 2001-12, 462) x formation lag j: one cross-sectional
OLS of R_{it}(%) on R_{i,t-1}(decimal), ln(mcap_$ at t-1), and 6 strategy
dummies (JH/JL<-jt_sig, MH/ML<-mg_sig, FHH/FHL<-wh_sig_dc (30/30 on the common rankable cross-section)). Dummies from 30/30 ordinal sorts at formation
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
| ALL THREE SIMULTANEOUSLY (restricted sample) | 1928.1 | 3738.5 | 5216.2 | 6204.1 | 6063.6 |

## Pre-flight (s66_raw)

| row | ours janincl | paper janincl | ours janexcl |
|---|---:|---:|---:|
| intercept | 4.8061 (t 5.58) | 3.62 | 2.0945 (t 2.76) |
| r_lag1 | -6.5075 (t -16.16) | -6.50 | -5.5475 (t -15.79) |
| size | -0.1915 (t -4.48) | -0.20 | -0.0633 (t -1.66) |
| wh_spread | 0.4831 (t 3.00) | 0.65 | 0.8670 (t 6.10) |

## Diagnostics

- s66: avg sample 4803.6 (min 1962, max 7389), 2772 regressions, 0 empty months
  - rankable-only restricted cross-section: avg 4422.1 (min 1090, max 7044) per (t,j) regression
- s612: avg sample 4803.6 (min 1962, max 7389), 5544 regressions, 0 empty months
  - rankable-only restricted cross-section: avg 4300.1 (min 1066, max 7044) per (t,j) regression
- FF factors: 462 months aligned, 0 missing

## Overall hit rate (of 192)

**Tier 1: 144 / Tier 2: 48 / FAIL: 0**

### Per-column tally

| column | Tier 1 | Tier 2 | FAIL |
|---|---:|---:|---:|
| s66_raw_janincl | 19 | 5 | 0 |
| s66_raw_janexcl | 19 | 5 | 0 |
| s66_ra_janincl | 15 | 9 | 0 |
| s66_ra_janexcl | 18 | 6 | 0 |
| s612_raw_janincl | 20 | 4 | 0 |
| s612_raw_janexcl | 18 | 6 | 0 |
| s612_ra_janincl | 17 | 7 | 0 |
| s612_ra_janexcl | 18 | 6 | 0 |

_Tier 2 ⚠ = sign matches but |ours/paper| > 2 (magnitude far off; see audit1.md spot-check 10). FAIL cells with |paper| < 0.05 are rounding-boundary artifacts unless noted._

### Column: s66_raw_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 3.6200 | 4.8061 | +32.8% | Tier 1 | 6.0900 | 5.5821 | Tier 1 |
| r_lag1 | -6.5000 | -6.5075 | -0.1% | Tier 1 | -14.9000 | -16.1624 | Tier 1 |
| size | -0.2000 | -0.1915 | +4.2% | Tier 1 | -4.7000 | -4.4841 | Tier 1 |
| jt_winner | 0.1700 | 0.2032 | +19.5% | Tier 1 | 2.0700 | 2.3216 | Tier 1 |
| jt_loser | -0.2100 | -0.3386 | -61.2% | Tier 2 | -3.6000 | -5.7402 | Tier 2 |
| mg_winner | 0.1800 | 0.1358 | -24.6% | Tier 1 | 2.8000 | 2.3318 | Tier 1 |
| mg_loser | -0.0700 | -0.2472 | -253.1% | Tier 2 ⚠ | -1.1400 | -4.7176 | Tier 2 ⚠ |
| wh_winner | 0.1600 | 0.1835 | +14.7% | Tier 1 | 3.0600 | 2.8015 | Tier 1 |
| wh_loser | -0.4800 | -0.2996 | +37.6% | Tier 1 | -4.0700 | -2.7809 | Tier 1 |
| wh_spread | 0.6500 | 0.4831 | -25.7% | Tier 1 | 4.0800 | 2.9997 | Tier 1 |
| jt_spread | 0.3800 | 0.5418 | +42.6% | Tier 1 | 3.7100 | 4.9421 | Tier 1 |
| mg_spread | 0.2500 | 0.3830 | +53.2% | Tier 1 | 2.8300 | 4.7068 | Tier 2 |

### Column: s66_raw_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.8700 | 2.0945 | +12.0% | Tier 1 | 3.5700 | 2.7557 | Tier 1 |
| r_lag1 | -5.5300 | -5.5475 | -0.3% | Tier 1 | -14.8900 | -15.7895 | Tier 1 |
| size | -0.0800 | -0.0633 | +20.8% | Tier 1 | -2.1300 | -1.6575 | Tier 1 |
| jt_winner | 0.1500 | 0.1880 | +25.3% | Tier 1 | 1.6900 | 2.0402 | Tier 1 |
| jt_loser | -0.3100 | -0.4702 | -51.7% | Tier 2 | -6.2900 | -9.1018 | Tier 2 |
| mg_winner | 0.1700 | 0.1131 | -33.5% | Tier 1 | 2.5400 | 1.8875 | Tier 1 |
| mg_loser | -0.0500 | -0.2471 | -394.3% | Tier 2 ⚠ | -0.8400 | -4.6502 | Tier 2 ⚠ |
| wh_winner | 0.2700 | 0.2970 | +10.0% | Tier 1 | 5.2500 | 4.8141 | Tier 1 |
| wh_loser | -0.7900 | -0.5700 | +27.8% | Tier 1 | -7.7600 | -6.1882 | Tier 1 |
| wh_spread | 1.0600 | 0.8670 | -18.2% | Tier 1 | 7.6400 | 6.1017 | Tier 1 |
| jt_spread | 0.4600 | 0.6582 | +43.1% | Tier 1 | 4.3900 | 5.9185 | Tier 1 |
| mg_spread | 0.2200 | 0.3603 | +63.8% | Tier 1 | 2.4500 | 4.2980 | Tier 2 |

### Column: s66_ra_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 2.5800 | 3.5831 | +38.9% | Tier 1 | 5.9900 | 5.4076 | Tier 1 |
| r_lag1 | -5.9400 | -6.0250 | -1.4% | Tier 1 | -14.1700 | -15.2789 | Tier 1 |
| size | -0.1700 | -0.1643 | +3.4% | Tier 1 | -5.1100 | -4.8060 | Tier 1 |
| jt_winner | 0.1600 | 0.2377 | +48.6% | Tier 1 | 2.8000 | 3.7462 | Tier 1 |
| jt_loser | -0.2200 | -0.3574 | -62.4% | Tier 2 | -3.8500 | -6.0536 | Tier 2 |
| mg_winner | 0.1900 | 0.1193 | -37.2% | Tier 1 | 2.8500 | 2.0092 | Tier 1 |
| mg_loser | -0.0700 | -0.2224 | -217.7% | Tier 2 ⚠ | -1.0900 | -4.1951 | Tier 2 ⚠ |
| wh_winner | 0.2700 | 0.2710 | +0.4% | Tier 1 | 6.4900 | 6.5469 | Tier 1 |
| wh_loser | -0.5900 | -0.3176 | +46.2% | Tier 2 | -6.3000 | -3.5465 | Tier 2 |
| wh_spread | 0.8600 | 0.5887 | -31.6% | Tier 1 | 7.2900 | 5.0568 | Tier 1 |
| jt_spread | 0.3800 | 0.5951 | +56.6% | Tier 2 | 4.0200 | 5.8117 | Tier 2 |
| mg_spread | 0.2500 | 0.3417 | +36.7% | Tier 1 | 2.9200 | 4.2061 | Tier 2 |

### Column: s66_ra_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.5500 | 1.9597 | +26.4% | Tier 1 | 4.0200 | 3.3151 | Tier 1 |
| r_lag1 | -5.3600 | -5.4760 | -2.2% | Tier 1 | -14.7800 | -15.7522 | Tier 1 |
| size | -0.0900 | -0.0806 | +10.4% | Tier 1 | -3.0900 | -2.6455 | Tier 1 |
| jt_winner | 0.1600 | 0.2355 | +47.2% | Tier 1 | 2.6900 | 3.6969 | Tier 1 |
| jt_loser | -0.3000 | -0.4651 | -55.0% | Tier 2 | -6.2800 | -8.9913 | Tier 2 |
| mg_winner | 0.1900 | 0.1082 | -43.0% | Tier 1 | 2.7600 | 1.7923 | Tier 1 |
| mg_loser | -0.0500 | -0.2336 | -367.2% | Tier 2 ⚠ | -0.8500 | -4.4494 | Tier 2 ⚠ |
| wh_winner | 0.3200 | 0.3159 | -1.3% | Tier 1 | 7.6600 | 8.2643 | Tier 1 |
| wh_loser | -0.8100 | -0.5242 | +35.3% | Tier 1 | -10.6500 | -7.2522 | Tier 1 |
| wh_spread | 1.1300 | 0.8401 | -25.7% | Tier 1 | 11.3500 | 8.8061 | Tier 1 |
| jt_spread | 0.4600 | 0.7006 | +52.3% | Tier 2 | 5.1300 | 7.1756 | Tier 1 |
| mg_spread | 0.2400 | 0.3418 | +42.4% | Tier 1 | 2.7200 | 4.1722 | Tier 2 |

### Column: s612_raw_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 3.4200 | 4.5365 | +32.6% | Tier 1 | 5.7300 | 5.2263 | Tier 1 |
| r_lag1 | -6.5600 | -6.5625 | -0.0% | Tier 1 | -14.8800 | -16.0292 | Tier 1 |
| size | -0.1900 | -0.1775 | +6.6% | Tier 1 | -4.2700 | -4.1443 | Tier 1 |
| jt_winner | 0.0500 | 0.0751 | +50.3% | Tier 1 | 0.6000 | 0.9072 | Tier 2 |
| jt_loser | -0.1900 | -0.2656 | -39.8% | Tier 1 | -4.6400 | -6.0316 | Tier 1 |
| mg_winner | 0.1000 | 0.1044 | +4.4% | Tier 1 | 1.8100 | 1.9623 | Tier 1 |
| mg_loser | -0.0700 | -0.1636 | -133.7% | Tier 2 ⚠ | -1.5300 | -4.0429 | Tier 2 ⚠ |
| wh_winner | 0.1300 | 0.1609 | +23.8% | Tier 1 | 2.8300 | 2.6755 | Tier 1 |
| wh_loser | -0.2600 | -0.1468 | +43.5% | Tier 1 | -2.2900 | -1.4856 | Tier 1 |
| wh_spread | 0.3900 | 0.3078 | -21.1% | Tier 1 | 2.6300 | 2.0726 | Tier 1 |
| jt_spread | 0.2400 | 0.3408 | +42.0% | Tier 1 | 2.7400 | 3.7335 | Tier 1 |
| mg_spread | 0.1700 | 0.2680 | +57.6% | Tier 1 | 2.2300 | 3.8789 | Tier 2 |

### Column: s612_raw_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.6600 | 1.7704 | +6.6% | Tier 1 | 3.1700 | 2.3299 | Tier 1 |
| r_lag1 | -5.5800 | -5.5789 | +0.0% | Tier 1 | -14.9600 | -15.7927 | Tier 1 |
| size | -0.0600 | -0.0468 | +22.0% | Tier 1 | -1.6100 | -1.2314 | Tier 1 |
| jt_winner | 0.0200 | 0.0500 | +149.9% | Tier 1 | 0.2200 | 0.5811 | Tier 2 ⚠ |
| jt_loser | -0.2700 | -0.3808 | -41.0% | Tier 2 | -7.5800 | -9.8139 | Tier 1 |
| mg_winner | 0.0900 | 0.0850 | -5.6% | Tier 1 | 1.5600 | 1.5349 | Tier 1 |
| mg_loser | -0.0500 | -0.1552 | -210.5% | Tier 2 ⚠ | -1.1600 | -3.7009 | Tier 2 ⚠ |
| wh_winner | 0.2200 | 0.2649 | +20.4% | Tier 1 | 5.1900 | 4.5838 | Tier 1 |
| wh_loser | -0.5600 | -0.4049 | +27.7% | Tier 1 | -5.8700 | -4.8552 | Tier 1 |
| wh_spread | 0.7800 | 0.6698 | -14.1% | Tier 1 | 6.1400 | 5.1104 | Tier 1 |
| jt_spread | 0.2900 | 0.4308 | +48.5% | Tier 1 | 3.2500 | 4.5622 | Tier 2 |
| mg_spread | 0.1500 | 0.2402 | +60.2% | Tier 1 | 1.8100 | 3.3181 | Tier 2 |

### Column: s612_ra_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 2.3800 | 3.3067 | +38.9% | Tier 1 | 5.5600 | 4.9867 | Tier 1 |
| r_lag1 | -5.9900 | -6.0645 | -1.2% | Tier 1 | -14.1400 | -15.1317 | Tier 1 |
| size | -0.1600 | -0.1504 | +6.0% | Tier 1 | -4.5800 | -4.3992 | Tier 1 |
| jt_winner | 0.0500 | 0.1278 | +155.5% | Tier 1 | 1.1000 | 2.3874 | Tier 2 ⚠ |
| jt_loser | -0.2100 | -0.2979 | -41.9% | Tier 2 | -5.2200 | -6.8604 | Tier 1 |
| mg_winner | 0.1400 | 0.1333 | -4.8% | Tier 1 | 2.4400 | 2.4933 | Tier 1 |
| mg_loser | -0.0900 | -0.1545 | -71.7% | Tier 1 | -1.9800 | -3.8192 | Tier 2 |
| wh_winner | 0.2300 | 0.2441 | +6.1% | Tier 1 | 6.8900 | 6.8665 | Tier 1 |
| wh_loser | -0.3700 | -0.1808 | +51.1% | Tier 2 | -4.2200 | -2.2067 | Tier 2 |
| wh_spread | 0.6000 | 0.4248 | -29.2% | Tier 1 | 5.6100 | 4.0332 | Tier 1 |
| jt_spread | 0.2700 | 0.4257 | +57.7% | Tier 2 | 3.7700 | 5.5795 | Tier 2 |
| mg_spread | 0.2200 | 0.2879 | +30.8% | Tier 1 | 3.1100 | 4.2643 | Tier 1 |

### Column: s612_ra_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.3400 | 1.6460 | +22.8% | Tier 1 | 3.5100 | 2.8031 | Tier 1 |
| r_lag1 | -5.4100 | -5.5018 | -1.7% | Tier 1 | -14.8200 | -15.7308 | Tier 1 |
| size | -0.0700 | -0.0650 | +7.1% | Tier 1 | -2.4400 | -2.1470 | Tier 1 |
| jt_winner | 0.0400 | 0.1134 | +183.6% | Tier 1 | 0.7900 | 2.1302 | Tier 2 ⚠ |
| jt_loser | -0.2800 | -0.3915 | -39.8% | Tier 1 | -7.8200 | -10.1488 | Tier 1 |
| mg_winner | 0.1300 | 0.1139 | -12.4% | Tier 1 | 2.1700 | 2.0657 | Tier 1 |
| mg_loser | -0.0700 | -0.1560 | -122.8% | Tier 2 ⚠ | -1.6500 | -3.7684 | Tier 2 ⚠ |
| wh_winner | 0.2700 | 0.2873 | +6.4% | Tier 1 | 8.3900 | 8.5790 | Tier 1 |
| wh_loser | -0.5800 | -0.3704 | +36.1% | Tier 1 | -8.3300 | -5.7123 | Tier 1 |
| wh_spread | 0.8500 | 0.6576 | -22.6% | Tier 1 | 9.7300 | 7.6963 | Tier 1 |
| jt_spread | 0.3200 | 0.5049 | +57.8% | Tier 2 | 4.6500 | 6.7861 | Tier 2 |
| mg_spread | 0.2000 | 0.2699 | +34.9% | Tier 1 | 2.6600 | 3.8504 | Tier 2 |

---

## Before/after vs the official sample (audit1.md [M3]; official = audit-verified data/fm_coefficients.parquet)

Anchor rows: wh_loser, wh_winner, wh_spread, jt_spread, mg_spread, intercept. Format: value (t-stat).

### Column: s66_raw_janincl

| row | official | rankable-only | paper |
|---|---:|---:|---:|
| wh_loser | -0.3079 (-2.92) | -0.2996 (-2.78) | -0.4800 |
| wh_winner | 0.1817 (2.67) | 0.1835 (2.80) | 0.1600 |
| wh_spread | 0.4896 (3.02) | 0.4831 (3.00) | 0.6500 |
| jt_spread | 0.5295 (4.96) | 0.5418 (4.94) | 0.3800 |
| mg_spread | 0.3804 (4.62) | 0.3830 (4.71) | 0.2500 |
| intercept | 4.6407 (5.34) | 4.8061 (5.58) | 3.6200 |

**Dominance ordering — s66_raw_janincl:** official JT>WH>MG | rankable-only JT>WH>MG | paper WH>JT>MG

### Column: s66_raw_janexcl

| row | official | rankable-only | paper |
|---|---:|---:|---:|
| wh_loser | -0.5685 (-6.38) | -0.5700 (-6.19) | -0.7900 |
| wh_winner | 0.3060 (4.73) | 0.2970 (4.81) | 0.2700 |
| wh_spread | 0.8745 (6.12) | 0.8670 (6.10) | 1.0600 |
| jt_spread | 0.6449 (5.96) | 0.6582 (5.92) | 0.4600 |
| mg_spread | 0.3573 (4.21) | 0.3603 (4.30) | 0.2200 |
| intercept | 1.8758 (2.45) | 2.0945 (2.76) | 1.8700 |

**Dominance ordering — s66_raw_janexcl:** official WH>JT>MG | rankable-only WH>JT>MG | paper WH>JT>MG

### Column: s66_ra_janincl

| row | official | rankable-only | paper |
|---|---:|---:|---:|
| wh_loser | -0.3318 (-3.73) | -0.3176 (-3.55) | -0.5900 |
| wh_winner | 0.2598 (6.14) | 0.2710 (6.55) | 0.2700 |
| wh_spread | 0.5916 (5.02) | 0.5887 (5.06) | 0.8600 |
| jt_spread | 0.5833 (5.83) | 0.5951 (5.81) | 0.3800 |
| mg_spread | 0.3400 (4.14) | 0.3417 (4.21) | 0.2500 |
| intercept | 3.4600 (5.06) | 3.5831 (5.41) | 2.5800 |

**Dominance ordering — s66_ra_janincl:** official WH>JT>MG | rankable-only JT>WH>MG | paper WH>JT>MG

### Column: s66_ra_janexcl

| row | official | rankable-only | paper |
|---|---:|---:|---:|
| wh_loser | -0.5294 (-7.45) | -0.5242 (-7.25) | -0.8100 |
| wh_winner | 0.3142 (7.96) | 0.3159 (8.26) | 0.3200 |
| wh_spread | 0.8436 (8.72) | 0.8401 (8.81) | 1.1300 |
| jt_spread | 0.6875 (7.21) | 0.7006 (7.18) | 0.4600 |
| mg_spread | 0.3399 (4.10) | 0.3418 (4.17) | 0.2400 |
| intercept | 1.7650 (2.91) | 1.9597 (3.32) | 1.5500 |

**Dominance ordering — s66_ra_janexcl:** official WH>JT>MG | rankable-only WH>JT>MG | paper WH>JT>MG

### Column: s612_raw_janincl

| row | official | rankable-only | paper |
|---|---:|---:|---:|
| wh_loser | -0.1383 (-1.46) | -0.1468 (-1.49) | -0.2600 |
| wh_winner | 0.1708 (2.62) | 0.1609 (2.68) | 0.1300 |
| wh_spread | 0.3091 (2.07) | 0.3078 (2.07) | 0.3900 |
| jt_spread | 0.3295 (3.68) | 0.3408 (3.73) | 0.2400 |
| mg_spread | 0.2659 (3.78) | 0.2680 (3.88) | 0.1700 |
| intercept | 4.2765 (4.86) | 4.5365 (5.23) | 3.4200 |

**Dominance ordering — s612_raw_janincl:** official JT>WH>MG | rankable-only JT>WH>MG | paper WH>JT>MG

### Column: s612_raw_janexcl

| row | official | rankable-only | paper |
|---|---:|---:|---:|
| wh_loser | -0.3858 (-4.93) | -0.4049 (-4.86) | -0.5600 |
| wh_winner | 0.2873 (4.53) | 0.2649 (4.58) | 0.2200 |
| wh_spread | 0.6731 (5.10) | 0.6698 (5.11) | 0.7800 |
| jt_spread | 0.4192 (4.54) | 0.4308 (4.56) | 0.2900 |
| mg_spread | 0.2376 (3.23) | 0.2402 (3.32) | 0.1500 |
| intercept | 1.4511 (1.89) | 1.7704 (2.33) | 1.6600 |

**Dominance ordering — s612_raw_janexcl:** official WH>JT>MG | rankable-only WH>JT>MG | paper WH>JT>MG

### Column: s612_ra_janincl

| row | official | rankable-only | paper |
|---|---:|---:|---:|
| wh_loser | -0.1882 (-2.35) | -0.1808 (-2.21) | -0.3700 |
| wh_winner | 0.2360 (6.43) | 0.2441 (6.87) | 0.2300 |
| wh_spread | 0.4242 (4.00) | 0.4248 (4.03) | 0.6000 |
| jt_spread | 0.4144 (5.50) | 0.4257 (5.58) | 0.2700 |
| mg_spread | 0.2895 (4.23) | 0.2879 (4.26) | 0.2200 |
| intercept | 3.1079 (4.49) | 3.3067 (4.99) | 2.3800 |

**Dominance ordering — s612_ra_janincl:** official WH>JT>MG | rankable-only JT>WH>MG | paper WH>JT>MG

### Column: s612_ra_janexcl

| row | official | rankable-only | paper |
|---|---:|---:|---:|
| wh_loser | -0.3663 (-5.83) | -0.3704 (-5.71) | -0.5800 |
| wh_winner | 0.2905 (8.41) | 0.2873 (8.58) | 0.2700 |
| wh_spread | 0.6569 (7.66) | 0.6576 (7.70) | 0.8500 |
| jt_spread | 0.4926 (6.71) | 0.5049 (6.79) | 0.3200 |
| mg_spread | 0.2701 (3.80) | 0.2699 (3.85) | 0.2000 |
| intercept | 1.3587 (2.22) | 1.6460 (2.80) | 1.3400 |

**Dominance ordering — s612_ra_janexcl:** official WH>JT>MG | rankable-only WH>JT>MG | paper WH>JT>MG

## Sample-size cost

- Official avg cross-section n per (t,j) regression: **4803.6** (per holding month; table_5.md diagnostic).
- Rankable-only avg restricted cross-section n per (t,j) regression: **4361.1** (min 1066, max 7044) = 90.8% of the official sample.
- Regressions actually fit: s66 2772/2772, s612 5544/5544 (official: all).
- All-three-rankable stocks / formation month (avg by decade): 1960s 1928.1 | 1970s 3738.5 | 1980s 5216.2 | 1990s 6204.1 | 2000s 6063.6

## Adoption checks (Replicator to ratify)

Rule: adopt the rankable-only sample as official iff ALL of:

1. WH > JT restored in BOTH Jan-included raw columns (s66, s612);
2. every wh_spread cell (8 columns, values) stays Tier 1;
3. the total Table V Tier-1 count does not degrade (official 150).

- [C1] s66_raw_janincl: rankable-only wh_spread 0.4831 vs jt_spread 0.5418 -> WH 0.4831 <= JT FAIL
- [C1] s612_raw_janincl: rankable-only wh_spread 0.3078 vs jt_spread 0.3408 -> WH 0.3078 <= JT FAIL
- [C2] wh_spread Tier-1 cells under rankable-only: 8/8 -> PASS
- [C3] total Tier-1: official 150 vs rankable-only 144 (T2 48, FAIL 0) -> FAIL

**Recommendation: KEEP the official sample; document the Jan-included raw inversion as a vintage effect (non-actionable)**

Hit rate under rankable-only: Tier 1 144 / Tier 2 48 / FAIL 0 of 192 (official: 150 / 42 / 0).

### Per-column tally (rankable-only)

| column | Tier 1 | Tier 2 | FAIL |
|---|---:|---:|---:|
| s66_raw_janincl | 19 | 5 | 0 |
| s66_raw_janexcl | 19 | 5 | 0 |
| s66_ra_janincl | 15 | 9 | 0 |
| s66_ra_janexcl | 18 | 6 | 0 |
| s612_raw_janincl | 20 | 4 | 0 |
| s612_raw_janexcl | 18 | 6 | 0 |
| s612_ra_janincl | 17 | 7 | 0 |
| s612_ra_janexcl | 18 | 6 | 0 |