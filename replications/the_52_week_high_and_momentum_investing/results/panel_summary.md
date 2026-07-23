# Panel build report — George & Hwang (2004)

## 1. Dimensions
- rows x cols: 2387326 x 20
- months: 540 (1958-01-31 .. 2002-12-31)
- distinct permnos: 21108
- total stock-months: 2,387,326

## 2. Avg universe stocks/month
- 1958: 1042.8 (12 months)
- 1958s (1958-59): 1044.5 (24 months)
- 1963: 1974.8 (12 months)
- 1970: 2263.2 (12 months)
- 1980: 4560.1 (12 months)
- 1990: 5797.6 (12 months)
- 2001: 5992.8 (12 months)

## 3. Signal summary over formation window 1963-01-31 .. 2001-11-30
           n_total  null_frac    mean    std     p01     p10     p50    p90    p99
signal                                                                            
jt_sig     2247714     0.0542  0.0737 0.4781 -0.7117 -0.3600  0.0236 0.5000 1.6265
wh_sig_hi  2247714     0.0059  0.2869 1.2169 -2.3830 -1.1159  0.6923 0.9627 1.0000
wh_sig_cl  2247714     0.0059  0.7746 0.2170  0.1653  0.4503  0.8321 1.0000 1.0000
wh_sig_dc  2247714     0.0059  0.7253 0.2195  0.1373  0.4000  0.7742 0.9732 1.0000
wh_lo_sig  2247714     0.0059  1.5761 2.3483  1.0000  1.0324  1.2917 2.1260 5.3333
mg_sig     2247714     0.0542  0.0676 0.1489 -0.2960 -0.1178  0.0660 0.2502 0.4435
g_gh       2247714     0.5264 -0.3333 1.4073 -4.4241 -0.9842 -0.0760 0.2532 0.4710
g_gh_b     2247714     0.3230 -0.3928 1.5883 -5.1419 -1.1095 -0.0932 0.2506 0.4723

## 4. wh_sig_hi sanity (formation window)
- fraction > 1.005: 0.001821 (4069 of 2234471)
- fraction <= 0 (negative-askhi windows): 0.215858
- p99: 1.000000, max: 19.428571

## 4b. wh_sig_dc sanity (daily-close variant, formation window)
- n non-null wh_sig_dc: 2,234,471 of 2,247,714 (null frac 0.005892)
- avg cross-section n at formation (non-null wh_sig_dc/month): 4784.7
- fraction > 1 (should be 0): 0.000000 (0 of 2234471)
- fraction > 1 + 1e-9 (numerical tolerance): 0.000000
- wh_sig_dc: mean 0.725328, p50 0.774194, std 0.219523, min 0.001902, max 1.000000
- wh_sig_cl: mean 0.774616, p50 0.832095 (daily max >= month-end max in the window, so wh_sig_dc mean should be <= wh_sig_cl mean)
- mean(wh_sig_dc) - mean(wh_sig_cl) = -0.049288 (expected <= 0)

## 4c. wh_lo_sig sanity (52-week-LOW signal, audit M4 prep, formation window)
- n non-null wh_lo_sig: 2,234,471 of 2,247,714 (null frac 0.005892; wh_sig_dc null frac over the same window: 0.005892)
- avg cross-section n at formation (non-null wh_lo_sig/month): 4784.7
- fraction < 1 (should be 0; month-f close is inside its own window): 0.000000 (0 of 2234471)
- fraction < 1 - 1e-9 (numerical tolerance): 0.000000
- wh_lo_sig: min 1.000000, p50 1.291680, p90 2.125984, mean 1.576056, std 2.348300, max 543.941980

## 5. Turnover
- stock-months with computable V: 2090400 of 2387326 (0.8756)
- fraction with raw V > 1 (capped): 0.002347 (4906 months)
- median V 1958-59: 0.0129 (n=25,037)
- median V 1960s: 0.0159 (n=217,039)
- median V 1970s: 0.0164 (n=285,159)
- median V 1980s: 0.0315 (n=569,857)
- median V 1990s: 0.0490 (n=779,492)
- median V 2000-02: 0.0620 (n=213,816)

## 6. Industry distribution, 1990-06 (MG Table I mapping)
-  1 Mining               322
-  2 Food                 119
-  3 Apparel               91
-  4 Paper                 46
-  5 Chemical             281
-  6 Petroleum             28
-  7 Construction          41
-  8 Prim. Metals          73
-  9 Fab. Metals          122
- 10 Machinery            396
- 11 Electrical Eq.       435
- 12 Transport Eq.         92
- 13 Manufacturing        361
- 14 Railroads             11
- 15 Other Transport.      87
- 16 Utilities            234
- 17 Dept. Stores          37
- 18 Retail               555
- 19 Financial           1294
- 20 Other               1185
-    TOTAL               5810

## 7. Runtime
- load_s: 16.3
- merge_s: 2.5
- pivot_s: 8.9
- signals_s: 55.5
- assemble_s: 1.0
- delist_s: 4.5
- total_s: 90.3

## 7b. Delisting adjustment (ret_dl column; ret itself untouched)
- msedelist rows pulled (dlstdt 1958-01-01..2003-12-31): 18,071; in analysis grid (month <= 2002-12): 17,472; dropped (2003 months past grid): 599
- in-grid events with valid dlret (non-null, > -1): 16,948 (0.9700); dlret NULL: 163; worthless (dlret = -1.0, left as-is): 361
- existing panel rows adjusted ((1+ret)(1+dlret)-1): 1,214
- NEW rows added (no panel row at the delisting month; stock was an active holding at m-1; ret=NaN so the `ret` variant is untouched): 13,908 — of which with an msf return at m (ret_dl = (1+ret_msf)(1+dlret)-1): 536; msf row absent (ret_dl = dlret): 13,372. Not added (valid dlret but no panel row at m-1 either — not a plausible holding): 1,826
- WHY so many added rows: dsenames nameendt = dlstdt < month-end, so universe coverage fails at the delisting month for mid-month delistings; the final-month msf record usually exists but carries no usable return (see with-msf count), so the stock-month is absent from the universe panel either way.
- mean dlret over valid events: -0.0431
- performance delistings (dlstcd 500-599): 7,580; missing dlret: 151; worthless: 357; valid: 7,072 (frac 0.9330)
- mean dlret of valid performance delistings: -0.1516 (median -0.0861)
- performance-delist missing-dlret by decade (n / missing / worthless / valid):
  - 1950s: 16 / 1 / 0 / 15
  - 1960s: 206 / 8 / 14 / 184
  - 1970s: 910 / 26 / 93 / 791
  - 1980s: 2250 / 87 / 152 / 2011
  - 1990s: 2986 / 25 / 97 / 2864
  - 2000s: 1212 / 4 / 1 / 1207
- dlstcd 580: n 887, missing 12, valid 818, mean dlret (valid) -0.1328
- dlstcd 584: n 750, missing 6, valid 692, mean dlret (valid) -0.2881
- NO Shumway/BMP imputation for missing dlret (post-paper methodology): missing/worthless events keep ret_dl = ret.

## 7c. g_gh variant B vs variant A coverage (audit M2 adjudication; g_gh untouched, g_gh_b additive)
- null fraction, ALL panel rows: g_gh (A) 0.5337 vs g_gh_b (B) 0.3210
- null fraction, formation window 1963-01-31 .. 2001-11-30: g_gh (A) 0.5264 vs g_gh_b (B) 0.3230
- null fraction by decade (formation window):
  - 1960s: A 0.4703 (n=174,021) vs B 0.2177
  - 1970s: A 0.5810 (n=480,450) vs B 0.4839
  - 1980s: A 0.6455 (n=663,491) vs B 0.4034
  - 1990s: A 0.4276 (n=784,737) vs B 0.2071
  - 2000s: A 0.4032 (n=145,015) vs B 0.1770
- g_gh (A) distribution (formation window, n=1,064,442): mean -0.3333, p01 -4.4241, p10 -0.9842, p50 -0.0760, p90 0.2532, p99 0.4710, std 1.4073, min -233.4356, max 0.9766
- g_gh_b (B) distribution (formation window, n=1,521,590): mean -0.3928, p01 -5.1419, p10 -1.1095, p50 -0.0932, p90 0.2506, p99 0.4723, std 1.5883, min -233.4356, max 0.9843
- consistency: 1,064,415 stock-months non-null under BOTH A and B; values bit-identical: True (B == A must hold wherever A is defined and V(f) is non-null — there all 60 lags are usable and the sums coincide)

## Extra facts
- msf rows fetched (post hygiene filter, incl. 1957-12): 2,709,847 across 24,632 permnos
- dsf monthly max-close rows fetched (1957-01..2002-12): 2,766,488 across 24,745 permnos
- dsf monthly min-close rows fetched (1957-01..2002-12): 2,766,488 across 24,745 permnos
- Jul 1963 universe stocks: 1985
- mg_sig non-null in 1958 (verifies Dec-1957 mcap lag feeds Jan-1958 industry returns): 7215

## Data caveats (facts for the Replicator)
- wh_sig_hi <= 0 overall: 0.2034 — negative because CRSP stores askhi with the sign convention (negative = bid/ask quote, not trade high) for low-priced/pre-1983 NASDAQ stocks; windows with all-negative askhi give negative ratios. By decade: 1970s 0.404, 1980s 0.379, 1990s 0.050, 2000s 0.0003.
- vol/shrout missing (V not computable): 0.1244 of panel stock-months; concentrated in the 1970s (0.404) and 1980s (0.136), ~0 elsewhere — drives g_gh null fraction (g_gh_b variant B renormalizes over available lags instead; see sec 7c).
- ClickHouse Date type cannot hold pre-1970 dates: all SQL date conversions use toDate32; month-end keys derived in pandas (date + MonthEnd(0)).