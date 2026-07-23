# Table VI — George & Hwang (2004): Persistence of Profits (risk-adjusted, (6,k,12) strategies)

Each month t (1963-07 .. 2001-12, 462) x formation lag j=2..13 x gap k in {12,24,36,48}: one cross-sectional OLS of R_{it}(%) on R_{i,t-1}(decimal), ln(mcap_$ at t-1), and 6 strategy dummies (JH/JL<-jt_sig, MH/ML<-mg_sig, FHH/FHL<-wh_sig_dc). Dummies from 30/30 ordinal sorts at formation f=t-k-j (k-offset; shared tables_5.run_horizon engine). c_{k,t}=mean_j b_{k,j,t}. RISK-ADJUSTED ONLY: intercept + t-stat of c_{k,t} on FF3.
Jan incl = all 462 t; Jan excl = month-of-year != 1.

Dependent variable R_it: panel column `ret_dl` (delisting-adjusted); R_{i,t-1} control, dummies, and sample rule on original ret.

## Rankable stocks per formation month (avg by decade, per k)

| k | strategy | 1950s | 1960s | 1970s | 1980s | 1990s | 2000s |
|---:|---|---:|---:|---:|---:|---:|---:|
| 12 | jt (jt_sig) | 0.0 | 1829.3 | 3738.5 | 5216.2 | 6204.1 | 6236.6 |
| 12 | mg (mg_sig) | 0.0 | 1829.3 | 3738.5 | 5216.2 | 6204.1 | 6236.6 |
| 12 | wh (wh_sig_dc) | 0.0 | 1929.2 | 3988.6 | 5495.1 | 6495.8 | 6525.5 |
| 24 | jt (jt_sig) | 0.0 | 1749.0 | 3738.5 | 5216.2 | 6202.8 | 0.0 |
| 24 | mg (mg_sig) | 0.0 | 1749.0 | 3738.5 | 5216.2 | 6202.8 | 0.0 |
| 24 | wh (wh_sig_dc) | 0.0 | 1841.1 | 3988.6 | 5495.1 | 6494.0 | 0.0 |
| 36 | jt (jt_sig) | 1032.7 | 1719.7 | 3738.5 | 5216.2 | 6160.3 | 0.0 |
| 36 | mg (mg_sig) | 1032.7 | 1719.7 | 3738.5 | 5216.2 | 6160.3 | 0.0 |
| 36 | wh (wh_sig_dc) | 1051.0 | 1808.7 | 3988.6 | 5495.1 | 6461.4 | 0.0 |
| 48 | jt (jt_sig) | 1030.1 | 1719.7 | 3738.5 | 5216.2 | 6055.9 | 0.0 |
| 48 | mg (mg_sig) | 1030.1 | 1719.7 | 3738.5 | 5216.2 | 6055.9 | 0.0 |
| 48 | wh (wh_sig_dc) | 1042.8 | 1808.7 | 3988.6 | 5495.1 | 6357.8 | 0.0 |

## Diagnostics

- k=12: avg sample 4803.6 (min 1962, max 7389), 5544 regressions, 0 empty months
- k=24: avg sample 4803.6 (min 1962, max 7389), 5544 regressions, 0 empty months
- k=36: avg sample 4803.6 (min 1962, max 7389), 5544 regressions, 0 empty months
- k=48: avg sample 4803.6 (min 1962, max 7389), 5544 regressions, 0 empty months

## Overall hit rate (of 192)

**Tier 1: 73 / Tier 2: 64 / FAIL: 55**

### Per-column tally

| column | Tier 1 | Tier 2 | FAIL |
|---|---:|---:|---:|
| k12_janincl | 11 | 6 | 7 |
| k12_janexcl | 11 | 7 | 6 |
| k24_janincl | 9 | 9 | 6 |
| k24_janexcl | 8 | 5 | 11 |
| k36_janincl | 8 | 12 | 4 |
| k36_janexcl | 9 | 10 | 5 |
| k48_janincl | 8 | 7 | 9 |
| k48_janexcl | 9 | 8 | 7 |

_Tier 2 ⚠ = sign matches but |ours/paper| > 2 (magnitude far off; see audit1.md spot-check 10). FAIL cells with |paper| < 0.05 are rounding-boundary artifacts unless noted._

### Column: k12_janincl (risk-adjusted)

| row | paper | ours | dev% | tier | paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.7300 | 2.3088 | +33.5% | Tier 1 | 3.9600 | 3.1667 | Tier 1 |
| r_lag1 | -6.0500 | -5.5743 | +7.9% | Tier 1 | -13.8500 | -13.5649 | Tier 1 |
| size | -0.0900 | -0.1024 | -13.8% | Tier 1 | -2.6300 | -2.7805 | Tier 1 |
| jt_winner | -0.1500 | -0.0589 | +60.7% | Tier 2 | -3.8000 | -1.7253 | Tier 2 |
| jt_loser | -0.0200 | 0.0690 | +445.0% | FAIL | -0.8600 | 1.7652 | FAIL |
| mg_winner | -0.1100 | 0.0459 | +141.8% | FAIL | -2.4200 | 1.0733 | FAIL |
| mg_loser | -0.0300 | 0.1061 | +453.8% | FAIL | -0.7200 | 2.1215 | FAIL |
| wh_winner | 0.0300 | 0.1101 | +267.0% | Tier 2 ⚠ | 1.0000 | 2.8301 | Tier 2 ⚠ |
| wh_loser | 0.0500 | 0.0908 | +81.7% | Tier 2 | 0.6700 | 1.4806 | Tier 2 ⚠ |
| wh_spread | -0.0200 | 0.0193 | +196.4% | Tier 1 | -0.2300 | 0.2245 | FAIL |
| jt_spread | -0.1300 | -0.1279 | +1.6% | Tier 1 | -2.6500 | -2.2819 | Tier 1 |
| mg_spread | -0.0800 | -0.0602 | +24.8% | Tier 1 | -1.3300 | -0.9332 | Tier 1 |

### Column: k12_janexcl (risk-adjusted)

| row | paper | ours | dev% | tier | paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 0.6200 | 0.3913 | -36.9% | Tier 1 | 1.6200 | 0.6203 | Tier 2 |
| r_lag1 | -5.4100 | -5.0321 | +7.0% | Tier 1 | -14.5600 | -13.8878 | Tier 1 |
| size | -0.0100 | -0.0068 | +31.7% | Tier 1 | -0.1700 | -0.2122 | Tier 1 |
| jt_winner | -0.1800 | -0.0675 | +62.5% | Tier 2 | -4.7600 | -2.0862 | Tier 2 |
| jt_loser | -0.0600 | 0.0403 | +167.2% | FAIL | -2.2600 | 1.1252 | FAIL |
| mg_winner | -0.1200 | 0.0506 | +142.2% | FAIL | -2.7600 | 1.2435 | FAIL |
| mg_loser | -0.0100 | 0.1365 | +1465.0% | FAIL | -0.2100 | 2.8256 | FAIL |
| wh_winner | 0.0600 | 0.1670 | +178.4% | Tier 2 ⚠ | 2.1500 | 4.5241 | Tier 2 ⚠ |
| wh_loser | -0.1000 | -0.0105 | +89.5% | Tier 2 | -1.5100 | -0.1998 | Tier 2 |
| wh_spread | 0.1600 | 0.1776 | +11.0% | Tier 1 | 1.9300 | 2.3854 | Tier 1 |
| jt_spread | -0.1200 | -0.1078 | +10.2% | Tier 1 | -2.6600 | -2.0298 | Tier 1 |
| mg_spread | -0.1100 | -0.0859 | +21.9% | Tier 1 | -1.9100 | -1.3890 | Tier 1 |

### Column: k24_janincl (risk-adjusted)

| row | paper | ours | dev% | tier | paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.6000 | 2.3331 | +45.8% | Tier 2 | 3.5900 | 3.1062 | Tier 1 |
| r_lag1 | -6.1000 | -5.5419 | +9.1% | Tier 1 | -13.8600 | -13.3704 | Tier 1 |
| size | -0.0800 | -0.1030 | -28.8% | Tier 1 | -2.2700 | -2.7141 | Tier 1 |
| jt_winner | -0.0800 | 0.0001 | +100.2% | FAIL | -2.0600 | 0.0048 | FAIL |
| jt_loser | -0.0200 | 0.0992 | +596.0% | FAIL | -0.7200 | 2.7171 | FAIL |
| mg_winner | -0.0800 | 0.0041 | +105.1% | FAIL | -2.0400 | 0.0952 | FAIL |
| mg_loser | -0.1100 | -0.0164 | +85.1% | Tier 2 | -2.6700 | -0.3515 | Tier 2 |
| wh_winner | 0.0200 | 0.1106 | +452.8% | Tier 2 ⚠ | 0.7400 | 2.5294 | Tier 2 ⚠ |
| wh_loser | 0.0800 | 0.1519 | +89.9% | Tier 2 | 1.1900 | 2.7915 | Tier 2 ⚠ |
| wh_spread | -0.0600 | -0.0414 | +31.0% | Tier 1 | -0.7000 | -0.5288 | Tier 1 |
| jt_spread | -0.0600 | -0.0991 | -65.1% | Tier 2 | -1.2400 | -1.9816 | Tier 2 |
| mg_spread | 0.0200 | 0.0205 | +2.3% | Tier 1 | 0.4500 | 0.3618 | Tier 1 |

### Column: k24_janexcl (risk-adjusted)

| row | paper | ours | dev% | tier | paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 0.5000 | 0.3440 | -31.2% | Tier 1 | 1.2900 | 0.5329 | Tier 2 |
| r_lag1 | -5.4300 | -4.9976 | +8.0% | Tier 1 | -14.4500 | -13.7004 | Tier 1 |
| size | 0.0000 | -0.0045 | n/a | Tier 2 ⚠ | 0.1600 | -0.1366 | FAIL |
| jt_winner | -0.1100 | 0.0029 | +102.6% | FAIL | -2.9000 | 0.0914 | FAIL |
| jt_loser | -0.0300 | 0.0980 | +426.6% | FAIL | -1.2700 | 2.7965 | FAIL |
| mg_winner | -0.0900 | 0.0273 | +130.4% | FAIL | -2.4300 | 0.6269 | FAIL |
| mg_loser | -0.1000 | 0.0019 | +101.9% | FAIL | -2.5000 | 0.0411 | FAIL |
| wh_winner | 0.0600 | 0.1698 | +183.1% | Tier 2 ⚠ | 1.9100 | 4.2236 | Tier 2 ⚠ |
| wh_loser | -0.0300 | 0.0886 | +395.2% | FAIL | -0.4200 | 1.7567 | FAIL |
| wh_spread | 0.0800 | 0.0813 | +1.6% | Tier 1 | 1.0000 | 1.1144 | Tier 1 |
| jt_spread | -0.0700 | -0.0951 | -35.8% | Tier 1 | -1.6200 | -1.8991 | Tier 1 |
| mg_spread | 0.0100 | 0.0254 | +154.4% | Tier 1 | 0.1600 | 0.4522 | Tier 2 ⚠ |

### Column: k36_janincl (risk-adjusted)

| row | paper | ours | dev% | tier | paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.4100 | 2.3590 | +67.3% | Tier 2 | 3.1700 | 3.0954 | Tier 1 |
| r_lag1 | -6.1600 | -5.4952 | +10.8% | Tier 1 | -13.9800 | -13.2200 | Tier 1 |
| size | -0.0700 | -0.1048 | -49.7% | Tier 2 | -2.0000 | -2.7275 | Tier 1 |
| jt_winner | -0.0600 | 0.0057 | +109.5% | FAIL | -1.5400 | 0.1897 | FAIL |
| jt_loser | 0.0000 | 0.0927 | n/a | Tier 2 ⚠ | -0.0800 | 2.7328 | FAIL |
| mg_winner | 0.0500 | 0.0685 | +37.0% | Tier 1 | 1.1600 | 1.6194 | Tier 1 |
| mg_loser | 0.0000 | 0.0311 | n/a | Tier 2 ⚠ | 0.0400 | 0.6663 | Tier 2 ⚠ |
| wh_winner | 0.0000 | 0.0944 | n/a | Tier 2 ⚠ | -0.0700 | 2.2859 | FAIL |
| wh_loser | 0.0600 | 0.1216 | +102.6% | Tier 2 ⚠ | 0.9900 | 2.5197 | Tier 2 ⚠ |
| wh_spread | -0.0700 | -0.0271 | +61.3% | Tier 2 | -0.8200 | -0.3885 | Tier 2 |
| jt_spread | -0.0500 | -0.0870 | -73.9% | Tier 2 | -1.2900 | -1.9716 | Tier 2 |
| mg_spread | 0.0400 | 0.0374 | -6.5% | Tier 1 | 0.9100 | 0.7504 | Tier 1 |

### Column: k36_janexcl (risk-adjusted)

| row | paper | ours | dev% | tier | paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 0.3000 | 0.3414 | +13.8% | Tier 1 | 0.7700 | 0.5226 | Tier 1 |
| r_lag1 | -5.4700 | -4.9508 | +9.5% | Tier 1 | -14.2700 | -13.5281 | Tier 1 |
| size | 0.0200 | -0.0051 | -125.5% | Tier 1 | 0.5800 | -0.1528 | FAIL |
| jt_winner | -0.1000 | -0.0064 | +93.6% | Tier 2 | -2.7300 | -0.2152 | Tier 2 |
| jt_loser | -0.0200 | 0.1018 | +609.0% | FAIL | -0.7600 | 3.0759 | FAIL |
| mg_winner | 0.0200 | 0.1112 | +456.0% | Tier 2 ⚠ | 0.4900 | 2.7942 | Tier 2 ⚠ |
| mg_loser | 0.0000 | 0.0726 | n/a | Tier 2 ⚠ | 0.0100 | 1.6264 | Tier 2 ⚠ |
| wh_winner | 0.0100 | 0.1382 | +1281.7% | Tier 2 ⚠ | 0.5100 | 3.4459 | Tier 2 ⚠ |
| wh_loser | -0.0300 | 0.0736 | +345.4% | FAIL | -0.5100 | 1.6370 | FAIL |
| wh_spread | 0.0400 | 0.0645 | +61.4% | Tier 1 | 0.6000 | 0.9807 | Tier 2 |
| jt_spread | -0.0800 | -0.1082 | -35.2% | Tier 1 | -1.8500 | -2.4474 | Tier 1 |
| mg_spread | 0.0200 | 0.0386 | +93.1% | Tier 1 | 0.3900 | 0.7686 | Tier 2 |

### Column: k48_janincl (risk-adjusted)

| row | paper | ours | dev% | tier | paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 1.2800 | 2.3841 | +86.3% | Tier 2 | 2.9600 | 3.1101 | Tier 1 |
| r_lag1 | -6.2500 | -5.4873 | +12.2% | Tier 1 | -13.9300 | -13.1103 | Tier 1 |
| size | -0.0500 | -0.1057 | -111.5% | Tier 2 ⚠ | -1.5600 | -2.7342 | Tier 2 |
| jt_winner | -0.0900 | 0.0048 | +105.4% | FAIL | -2.2300 | 0.1428 | FAIL |
| jt_loser | 0.0200 | 0.0973 | +386.6% | Tier 2 ⚠ | 0.6800 | 3.0434 | Tier 2 ⚠ |
| mg_winner | 0.0600 | 0.0900 | +49.9% | Tier 2 | 1.3700 | 2.0401 | Tier 2 |
| mg_loser | -0.0300 | 0.0246 | +181.8% | Tier 1 | -0.7500 | 0.5045 | FAIL |
| wh_winner | -0.0200 | 0.1126 | +663.0% | FAIL | -0.7000 | 2.8493 | FAIL |
| wh_loser | -0.0100 | 0.0869 | +969.0% | FAIL | -0.1600 | 2.1161 | FAIL |
| wh_spread | -0.0100 | 0.0257 | +356.9% | FAIL | -0.1500 | 0.4327 | FAIL |
| jt_spread | -0.1000 | -0.0925 | +7.5% | Tier 1 | -2.2000 | -1.9521 | Tier 1 |
| mg_spread | 0.0900 | 0.0654 | -27.3% | Tier 1 | 1.7600 | 1.0745 | Tier 1 |

### Column: k48_janexcl (risk-adjusted)

| row | paper | ours | dev% | tier | paper_t | ours_t | tier_t |
|---|---:|---:|---:|---|---:|---:|---|
| intercept | 0.1400 | 0.3464 | +147.4% | Tier 2 ⚠ | 0.3700 | 0.5281 | Tier 2 |
| r_lag1 | -5.5700 | -4.9425 | +11.3% | Tier 1 | -14.0100 | -13.4268 | Tier 1 |
| size | 0.0300 | -0.0045 | -115.1% | Tier 1 | 1.2000 | -0.1357 | FAIL |
| jt_winner | -0.1300 | -0.0061 | +95.3% | Tier 2 | -3.3600 | -0.1842 | Tier 2 |
| jt_loser | 0.0200 | 0.1212 | +505.9% | Tier 2 ⚠ | 0.7700 | 3.9453 | Tier 2 ⚠ |
| mg_winner | 0.0600 | 0.1248 | +108.0% | Tier 2 ⚠ | 1.4200 | 2.8696 | Tier 2 ⚠ |
| mg_loser | -0.0200 | 0.0351 | +275.3% | FAIL | -0.4300 | 0.7223 | FAIL |
| wh_winner | -0.0100 | 0.1432 | +1531.5% | FAIL | -0.3400 | 3.6465 | FAIL |
| wh_loser | -0.0800 | 0.0563 | +170.4% | FAIL | -1.6200 | 1.4261 | FAIL |
| wh_spread | 0.0700 | 0.0868 | +24.0% | Tier 1 | 1.1100 | 1.4666 | Tier 1 |
| jt_spread | -0.1400 | -0.1273 | +9.1% | Tier 1 | -3.1600 | -2.7778 | Tier 1 |
| mg_spread | 0.0800 | 0.0898 | +12.2% | Tier 1 | 1.5400 | 1.4815 | Tier 1 |

## Reversal-pattern check (Jan-excl, by k)

Paper claim: JT/MG winner dummies turn NEGATIVE (momentum reverses); 52-week-high winner + spread stay near zero / NOT significantly negative (no reversal). sig = |t| >= 1.96.

| k | row | ours_v | ours_t | paper_v | paper_t | sign match | sig(ours) | sig(paper) |
|---:|---|---:|---:|---:|---:|---|---|---|
| 12 | jt_winner | -0.0675 | -2.09 | -0.18 | -4.76 | Y | Y | Y |
| 12 | mg_winner | 0.0506 | 1.24 | -0.12 | -2.76 | NO | n | Y |
| 12 | wh_winner | 0.1670 | 4.52 | 0.06 | 2.15 | Y | Y | Y |
| 12 | wh_spread | 0.1776 | 2.39 | 0.16 | 1.93 | Y | Y | n |
| 24 | jt_winner | 0.0029 | 0.09 | -0.11 | -2.90 | NO | n | Y |
| 24 | mg_winner | 0.0273 | 0.63 | -0.09 | -2.43 | NO | n | Y |
| 24 | wh_winner | 0.1698 | 4.22 | 0.06 | 1.91 | Y | Y | n |
| 24 | wh_spread | 0.0813 | 1.11 | 0.08 | 1.00 | Y | n | n |
| 36 | jt_winner | -0.0064 | -0.22 | -0.10 | -2.73 | Y | n | Y |
| 36 | mg_winner | 0.1112 | 2.79 | 0.02 | 0.49 | Y | Y | n |
| 36 | wh_winner | 0.1382 | 3.45 | 0.01 | 0.51 | Y | Y | n |
| 36 | wh_spread | 0.0645 | 0.98 | 0.04 | 0.60 | Y | n | n |
| 48 | jt_winner | -0.0061 | -0.18 | -0.13 | -3.36 | Y | n | Y |
| 48 | mg_winner | 0.1248 | 2.87 | 0.06 | 1.42 | Y | Y | n |
| 48 | wh_winner | 0.1432 | 3.65 | -0.01 | -0.34 | NO | Y | n |
| 48 | wh_spread | 0.0868 | 1.47 | 0.07 | 1.11 | Y | n | n |