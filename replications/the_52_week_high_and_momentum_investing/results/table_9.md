# Table IX — George & Hwang (2004): 52-week LOW replaces 52-week high (Table V layout)

Each month t (1963-07 .. 2001-12, 462) x formation lag j: one cross-sectional
OLS of R_{it}(%) on R_{i,t-1}(decimal), ln(mcap_$ at t-1), and 6 strategy
dummies (JH/JL<-jt_sig, MH/ML<-mg_sig, FLH/FLL<-wh_lo_sig). Dummies from 30/30 ordinal sorts at formation
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
| wl (wh_lo_sig) | 2037.9 | 3988.6 | 5495.1 | 6495.8 | 6265.7 |

## Pre-flight (s66_raw)

| row | ours janincl | paper janincl | ours janexcl |
|---|---:|---:|---:|
| intercept | 4.3213 (t 4.80) | 3.27 | 1.3899 (t 1.78) |
| r_lag1 | -6.0555 (t -15.11) | -6.50 | -5.1374 (t -14.74) |
| size | -0.1687 (t -3.81) | -0.18 | -0.0302 (t -0.78) |
| wl_spread | 0.1090 (t 0.79) | 0.13 | -0.0283 (t -0.20) |

## Diagnostics

- s66: avg sample 4803.6 (min 1962, max 7389), 2772 regressions, 0 empty months
- s612: avg sample 4803.6 (min 1962, max 7389), 5544 regressions, 0 empty months
- FF factors: 462 months aligned, 0 missing

## Overall hit rate (of 192)

**Tier 1: 126 / Tier 2: 58 / FAIL: 8**

### Per-column tally

| column | Tier 1 | Tier 2 | FAIL |
|---|---:|---:|---:|
| s66_raw_janincl | 18 | 6 | 0 |
| s66_raw_janexcl | 14 | 6 | 4 |
| s66_ra_janincl | 16 | 8 | 0 |
| s66_ra_janexcl | 14 | 10 | 0 |
| s612_raw_janincl | 17 | 7 | 0 |
| s612_raw_janexcl | 12 | 10 | 2 |
| s612_ra_janincl | 20 | 4 | 0 |
| s612_ra_janexcl | 15 | 7 | 2 |

_Tier 2 ⚠ = sign matches but |ours/paper| > 2 (magnitude far off; see audit1.md spot-check 10). FAIL cells with |paper| < 0.05 are rounding-boundary artifacts unless noted._

### Column: s66_raw_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 3.2700 | 4.3213 | +32.1% | Tier 1 | 5.1800 | 4.8012 | Tier 1 |
| r_lag1 | -6.5000 | -6.0555 | +6.8% | Tier 1 | -14.8200 | -15.1118 | Tier 1 |
| size | -0.1800 | -0.1687 | +6.3% | Tier 1 | -3.8600 | -3.8140 | Tier 1 |
| jt_winner | 0.2500 | 0.2930 | +17.2% | Tier 1 | 5.1800 | 5.8336 | Tier 1 |
| jt_loser | -0.4600 | -0.4163 | +9.5% | Tier 1 | -3.6300 | -3.6394 | Tier 1 |
| mg_winner | 0.1700 | 0.1874 | +10.2% | Tier 1 | 2.6900 | 3.4273 | Tier 1 |
| mg_loser | -0.0700 | -0.1919 | -174.2% | Tier 2 ⚠ | -1.0800 | -3.3655 | Tier 2 ⚠ |
| wl_winner | 0.0600 | 0.0238 | -60.4% | Tier 2 | 0.6100 | 0.2609 | Tier 2 |
| wl_loser | -0.0700 | -0.0853 | -21.8% | Tier 1 | -1.3700 | -1.5703 | Tier 1 |
| wl_spread | 0.1300 | 0.1090 | -16.1% | Tier 1 | 0.9500 | 0.7901 | Tier 1 |
| jt_spread | 0.7100 | 0.7093 | -0.1% | Tier 1 | 4.6100 | 4.6459 | Tier 1 |
| mg_spread | 0.2400 | 0.3793 | +58.0% | Tier 2 | 2.7400 | 4.7547 | Tier 2 |

### Column: s66_raw_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.3600 | 1.3899 | +2.2% | Tier 1 | 2.4800 | 1.7793 | Tier 1 |
| r_lag1 | -5.5000 | -5.1374 | +6.6% | Tier 1 | -14.9600 | -14.7370 | Tier 1 |
| size | -0.0400 | -0.0302 | +24.5% | Tier 1 | -1.0000 | -0.7761 | Tier 1 |
| jt_winner | 0.3000 | 0.3971 | +32.4% | Tier 1 | 6.3800 | 8.3552 | Tier 1 |
| jt_loser | -0.7500 | -0.7136 | +4.9% | Tier 1 | -6.9200 | -7.5695 | Tier 1 |
| mg_winner | 0.1600 | 0.1788 | +11.7% | Tier 1 | 2.4400 | 3.2156 | Tier 1 |
| mg_loser | -0.0500 | -0.1859 | -271.7% | Tier 2 ⚠ | -0.8200 | -3.2146 | Tier 2 ⚠ |
| wl_winner | 0.0200 | -0.0517 | -358.4% | FAIL | 0.2100 | -0.5501 | FAIL |
| wl_loser | -0.0900 | -0.0233 | +74.1% | Tier 2 | -1.9800 | -0.4266 | Tier 2 |
| wl_spread | 0.1200 | -0.0283 | -123.6% | FAIL | 0.8400 | -0.1995 | FAIL |
| jt_spread | 1.0500 | 1.1106 | +5.8% | Tier 1 | 7.9100 | 8.6459 | Tier 1 |
| mg_spread | 0.2100 | 0.3646 | +73.6% | Tier 2 | 2.4000 | 4.4736 | Tier 2 |

### Column: s66_ra_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 2.1600 | 3.0710 | +42.2% | Tier 2 | 4.7600 | 4.3420 | Tier 1 |
| r_lag1 | -5.9300 | -5.6125 | +5.4% | Tier 1 | -14.0900 | -14.2831 | Tier 1 |
| size | -0.1400 | -0.1367 | +2.3% | Tier 1 | -3.9000 | -3.7944 | Tier 1 |
| jt_winner | 0.3000 | 0.3281 | +9.4% | Tier 1 | 6.3500 | 6.6750 | Tier 1 |
| jt_loser | -0.5700 | -0.5140 | +9.8% | Tier 1 | -5.7500 | -5.2492 | Tier 1 |
| mg_winner | 0.1700 | 0.1346 | -20.8% | Tier 1 | 2.7500 | 2.4469 | Tier 1 |
| mg_loser | -0.0700 | -0.2021 | -188.6% | Tier 2 ⚠ | -1.0300 | -3.6434 | Tier 2 ⚠ |
| wl_winner | 0.0700 | 0.0404 | -42.2% | Tier 2 | 1.3000 | 0.6913 | Tier 2 |
| wl_loser | -0.0100 | -0.0280 | -179.8% | Tier 1 | -0.3200 | -0.7634 | Tier 2 ⚠ |
| wl_spread | 0.0900 | 0.0684 | -24.0% | Tier 1 | 1.0500 | 0.8143 | Tier 1 |
| jt_spread | 0.8700 | 0.8421 | -3.2% | Tier 1 | 6.8400 | 6.2808 | Tier 1 |
| mg_spread | 0.2400 | 0.3367 | +40.3% | Tier 2 | 2.8000 | 4.1584 | Tier 2 |

### Column: s66_ra_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.0100 | 1.2707 | +25.8% | Tier 1 | 2.5500 | 2.0465 | Tier 1 |
| r_lag1 | -5.3400 | -5.0928 | +4.6% | Tier 1 | -14.8600 | -14.7833 | Tier 1 |
| size | -0.0500 | -0.0456 | +8.8% | Tier 1 | -1.6000 | -1.4401 | Tier 1 |
| jt_winner | 0.3300 | 0.3916 | +18.7% | Tier 1 | 6.8200 | 8.3303 | Tier 1 |
| jt_loser | -0.7700 | -0.7250 | +5.8% | Tier 1 | -9.7500 | -9.2892 | Tier 1 |
| mg_winner | 0.1800 | 0.1400 | -22.2% | Tier 1 | 2.6700 | 2.5295 | Tier 1 |
| mg_loser | -0.0500 | -0.2031 | -306.1% | Tier 2 ⚠ | -0.7900 | -3.7260 | Tier 2 ⚠ |
| wl_winner | 0.0500 | 0.0003 | -99.4% | Tier 2 | 0.9500 | 0.0054 | Tier 2 |
| wl_loser | -0.0600 | -0.0099 | +83.5% | Tier 2 | -1.6400 | -0.2861 | Tier 2 |
| wl_spread | 0.1100 | 0.0102 | -90.7% | Tier 2 | 1.4700 | 0.1262 | Tier 2 |
| jt_spread | 1.1000 | 1.1166 | +1.5% | Tier 1 | 10.0600 | 9.9905 | Tier 1 |
| mg_spread | 0.2200 | 0.3431 | +56.0% | Tier 2 | 2.6300 | 4.2295 | Tier 2 |

### Column: s612_raw_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 3.2600 | 4.0940 | +25.6% | Tier 1 | 5.1400 | 4.5018 | Tier 1 |
| r_lag1 | -6.5600 | -6.0388 | +7.9% | Tier 1 | -14.8600 | -14.8773 | Tier 1 |
| size | -0.1700 | -0.1580 | +7.1% | Tier 1 | -3.6800 | -3.5560 | Tier 1 |
| jt_winner | 0.1300 | 0.1978 | +52.1% | Tier 2 | 3.5000 | 5.0039 | Tier 2 |
| jt_loser | -0.3200 | -0.2379 | +25.7% | Tier 1 | -2.9100 | -2.4617 | Tier 1 |
| mg_winner | 0.1000 | 0.1917 | +91.7% | Tier 2 | 1.7300 | 4.0761 | Tier 2 ⚠ |
| mg_loser | -0.0700 | -0.0727 | -3.8% | Tier 1 | -1.5600 | -1.4761 | Tier 1 |
| wl_winner | -0.0400 | -0.0225 | +43.7% | Tier 1 | -0.4500 | -0.2637 | Tier 2 |
| wl_loser | -0.1000 | -0.1013 | -1.3% | Tier 1 | -2.2600 | -1.7738 | Tier 1 |
| wl_spread | 0.0600 | 0.0788 | +31.4% | Tier 1 | 0.4500 | 0.5710 | Tier 1 |
| jt_spread | 0.4500 | 0.4357 | -3.2% | Tier 1 | 3.4800 | 3.4385 | Tier 1 |
| mg_spread | 0.1700 | 0.2643 | +55.5% | Tier 2 | 2.2300 | 3.9844 | Tier 2 |

### Column: s612_raw_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.3400 | 1.1129 | -17.0% | Tier 1 | 2.4300 | 1.4188 | Tier 2 |
| r_lag1 | -5.5700 | -5.1147 | +8.2% | Tier 1 | -15.0900 | -14.4778 | Tier 1 |
| size | -0.0300 | -0.0175 | +41.6% | Tier 1 | -0.7900 | -0.4503 | Tier 2 |
| jt_winner | 0.2000 | 0.2925 | +46.3% | Tier 2 | 5.6500 | 7.9913 | Tier 2 |
| jt_loser | -0.5900 | -0.5122 | +13.2% | Tier 1 | -6.1600 | -6.3947 | Tier 1 |
| mg_winner | 0.0900 | 0.1844 | +104.9% | Tier 2 ⚠ | 1.4800 | 3.8118 | Tier 2 ⚠ |
| mg_loser | -0.0500 | -0.0590 | -18.1% | Tier 1 | -1.1900 | -1.1614 | Tier 1 |
| wl_winner | -0.1000 | -0.1014 | -1.4% | Tier 1 | -1.0400 | -1.1599 | Tier 1 |
| wl_loser | -0.1100 | -0.0275 | +75.0% | Tier 2 | -2.4800 | -0.4820 | Tier 2 |
| wl_spread | 0.0100 | -0.0739 | -838.6% | FAIL | 0.0600 | -0.5270 | FAIL |
| jt_spread | 0.7900 | 0.8047 | +1.9% | Tier 1 | 7.0700 | 7.5463 | Tier 1 |
| mg_spread | 0.1400 | 0.2434 | +73.9% | Tier 2 | 1.8100 | 3.4933 | Tier 2 |

### Column: s612_ra_janincl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 2.1500 | 2.8661 | +33.3% | Tier 1 | 4.7400 | 4.0048 | Tier 1 |
| r_lag1 | -5.9800 | -5.5971 | +6.4% | Tier 1 | -14.1000 | -14.0565 | Tier 1 |
| size | -0.1300 | -0.1269 | +2.4% | Tier 1 | -3.7000 | -3.4934 | Tier 1 |
| jt_winner | 0.2000 | 0.2393 | +19.7% | Tier 1 | 5.7500 | 6.4721 | Tier 1 |
| jt_loser | -0.4400 | -0.3619 | +17.8% | Tier 1 | -5.3300 | -4.5699 | Tier 1 |
| mg_winner | 0.1300 | 0.1749 | +34.5% | Tier 1 | 2.3800 | 3.6641 | Tier 2 |
| mg_loser | -0.0800 | -0.1095 | -36.9% | Tier 1 | -1.9500 | -2.4468 | Tier 1 |
| wl_winner | -0.0400 | -0.0178 | +55.6% | Tier 1 | -0.7700 | -0.3404 | Tier 2 |
| wl_loser | -0.0500 | -0.0584 | -16.7% | Tier 1 | -1.4200 | -1.6256 | Tier 1 |
| wl_spread | 0.0100 | 0.0406 | +305.7% | Tier 2 ⚠ | 0.1200 | 0.5038 | Tier 2 ⚠ |
| jt_spread | 0.6400 | 0.6012 | -6.1% | Tier 1 | 6.2900 | 5.7313 | Tier 1 |
| mg_spread | 0.2200 | 0.2844 | +29.3% | Tier 1 | 3.0800 | 4.2883 | Tier 1 |

### Column: s612_ra_janexcl

| row | paper | ours | dev% | tier |  paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 0.9900 | 1.0135 | +2.4% | Tier 1 | 2.5100 | 1.6254 | Tier 1 |
| r_lag1 | -5.3900 | -5.0716 | +5.9% | Tier 1 | -14.9300 | -14.5233 | Tier 1 |
| size | -0.0400 | -0.0335 | +16.2% | Tier 1 | -1.3400 | -1.0557 | Tier 1 |
| jt_winner | 0.2300 | 0.2943 | +27.9% | Tier 1 | 6.7300 | 8.4391 | Tier 1 |
| jt_loser | -0.6300 | -0.5473 | +13.1% | Tier 1 | -9.3000 | -8.6047 | Tier 1 |
| mg_winner | 0.1200 | 0.1722 | +43.5% | Tier 2 | 2.0900 | 3.5390 | Tier 2 |
| mg_loser | -0.0700 | -0.0981 | -40.2% | Tier 2 | -1.5900 | -2.1667 | Tier 1 |
| wl_winner | -0.0700 | -0.0561 | +19.8% | Tier 1 | -1.4300 | -1.1127 | Tier 1 |
| wl_loser | -0.0800 | -0.0301 | +62.4% | Tier 2 | -2.5300 | -0.8960 | Tier 2 |
| wl_spread | 0.0100 | -0.0260 | -360.3% | FAIL | 0.1400 | -0.3414 | FAIL |
| jt_spread | 0.8600 | 0.8416 | -2.1% | Tier 1 | 9.9200 | 9.6346 | Tier 1 |
| mg_spread | 0.1900 | 0.2703 | +42.3% | Tier 2 | 2.6000 | 3.9187 | Tier 2 |

## Corollary verification (Table IX claims)

Claim 1: the 52-week-LOW spread is economically small and INSIGNIFICANT (|t| < 1.96).

| column | wl_spread ours | t | paper | paper_t | tier | insignificant? |
|---|---:|---:|---:|---:|---|---|
| s66_raw_janincl | 0.1090 | 0.79 | 0.13 | 0.95 | Tier 1 | YES |
| s66_raw_janexcl | -0.0283 | -0.20 | 0.12 | 0.84 | FAIL | YES |
| s66_ra_janincl | 0.0684 | 0.81 | 0.09 | 1.05 | Tier 1 | YES |
| s66_ra_janexcl | 0.0102 | 0.13 | 0.11 | 1.47 | Tier 2 | YES |
| s612_raw_janincl | 0.0788 | 0.57 | 0.06 | 0.45 | Tier 1 | YES |
| s612_raw_janexcl | -0.0739 | -0.53 | 0.01 | 0.06 | FAIL | YES |
| s612_ra_janincl | 0.0406 | 0.50 | 0.01 | 0.12 | Tier 2 ⚠ | YES |
| s612_ra_janexcl | -0.0260 | -0.34 | 0.01 | 0.14 | FAIL | YES |

Claim 2: JT spreads become LARGER than in Table V (low dummies absorb little, JT absorbs more).

| quantity | Table V (ours) | Table IX (ours) | paper T5 | paper T9 |
|---|---:|---:|---:|---:|
| jt_spread s66_raw_janexcl | 0.6449 | 1.1106 | 0.46 | 1.05 |
| jt_spread s66_raw_janincl | 0.5295 | 0.7093 | 0.38 | 0.71 |

- jt_spread s66_raw_janexcl: ours 1.1106 (t 8.65) vs Table V ours 0.6449 -> LARGER (matches paper); paper 0.46 (T5) -> 1.05 (T9).
- OCR correction (not a skip): size s612_raw_janincl t-stat '(3.68)' -> -3.68 (dropped minus; coef -0.17, Table V analog -4.27).
