# Delisting-return experiment — George & Hwang (2004)

ONE committed change: the holding-period return series. `ret_dl` folds
msedelist.dlret into the final month of delisted stocks; `ret` is the
original msf series. Signals, industry returns, and rankings are on the
ORIGINAL ret under BOTH variants (dependent variables only). No
Shumway/BMP imputation. The paper is silent on delisting treatment; the
leading hypothesis is that missing delisting returns bias loser
portfolios upward (delisting returns are mostly negative and
concentrated in losers).

Panel: 2,387,326 rows x 18 cols; rows where ret_dl differs from ret (visible adjustments): 1,161; added delisting-month rows (ret NaN, ret_dl set): 13,908 (plus events with dlret = 0 exactly, adjusted to the same value).

## 1. Delisting merge statistics

- msedelist events pulled (dlstdt 1958-01-01 .. 2003-12-31): **18,071**
- events mapping to an analysis-grid month (1958-01 .. 2002-12): **17,472** (dropped, 2003 months past the grid: 599)
- with valid dlret (non-NULL and > -1): **16,948** (fraction 0.9700); NULL dlret: 163; worthless (dlret = -1.0, left as-is per spec): 361
- merged onto existing panel rows ((1+ret)(1+dlret)-1): **1,214** (1161 visible as ret_dl != ret; the rest have dlret = 0 exactly)
- NEW panel rows added (no panel row at the delisting month; stock was an active holding at m-1; ret=NaN, so the `ret` variant is untouched): **13,908** — with an msf return at m (ret_dl = (1+ret_msf)(1+dlret)-1): 536; msf row absent (ret_dl = dlret): 13,372
- valid events NOT actioned (no panel row at m-1 either — not a plausible portfolio holding): 1,826; NULL/worthless events left as-is: 524
- WHY most delisting months lack a panel row in this vintage: dsenames nameendt = dlstdt < month-end, so universe coverage fails at the delisting month for mid-month delistings; the final-month msf RECORD exists (all 13,908 added rows have one) but its return/price is usually missing — only 536 pass the ret>-1 / valid-prc hygiene filter (verified by direct ClickHouse spot check)
- mean dlret over ALL valid in-grid events: **-0.0431**

### Performance delistings (dlstcd 500-599)

- events: **7,580**; missing dlret (NULL): **151**; worthless (dlret = -1.0): 357; valid: 7,072 (coverage 0.9330)
- mean dlret of valid performance delistings: **-0.1516** (median -0.0861)

| decade | n events | missing dlret | worthless (-1) | valid |
|---|---:|---:|---:|---:|
| 1950s | 16 | 1 | 0 | 15 |
| 1960s | 206 | 8 | 14 | 184 |
| 1970s | 910 | 26 | 93 | 791 |
| 1980s | 2250 | 87 | 152 | 2011 |
| 1990s | 2986 | 25 | 97 | 2864 |
| 2000s | 1212 | 4 | 1 | 1207 |

| dlstcd | n | missing dlret | valid | mean dlret (valid) |
|---|---:|---:|---:|---:|
| 580 | 887 | 12 | 818 | -0.1328 |
| 584 | 750 | 6 | 692 | -0.2881 |

- No Shumway/BMP imputation applied (post-paper methodology): NULL-dlret and worthless events keep ret_dl = ret.

## 2. Hit rates per table (Tier 1 / Tier 2 / FAIL)

| table | n | ret | ret_dl | Δ Tier 1 |
|---|---:|---|---|---:|
| Table I | 12 | 12/0/0 | 12/0/0 | +0 |
| Table II (combined) | 24 | 23/1/0 | 23/1/0 | +0 |
| Table II Panel A | 12 | 12/0/0 | 12/0/0 | +0 |
| Table II Panel B | 12 | 11/1/0 | 11/1/0 | +0 |
| Table III | 48 | 30/16/2 | 31/15/2 | +1 |
| Table V | 192 | 148/44/0 | 150/42/0 | +2 |
| Table VII | 240 | 119/107/14 | 122/102/16 | +3 |
| **ALL (T1+T2+T3+T5+T7)** | 516 | **332/168/16** | **338/160/18** | **+6** |

## 3. Key cells side by side (paper | ret | ret_dl)

### Table I losers (avg monthly return %, all 462 months)

| strategy | paper | ret | ret_dl | Δ(ret_dl−ret) |
|---|---:|---:|---:|---:|
| jt_loser | 1.05 | 1.0890 | 1.0504 | -0.0386 |
| mg_loser | 1.03 | 0.9771 | 0.9494 | -0.0277 |
| wh_loser | 1.06 | 1.0850 | 1.0447 | -0.0403 |

### Table V loser dummies (FM coefficient, %/month)

| row | column | paper | ret | ret_dl | Δ(ret_dl−ret) | tier ret | tier ret_dl |
|---|---|---:|---:|---:|---:|---|---|
| wh_loser | s66_raw_janincl | -0.48 | -0.2873 | -0.3079 | -0.0206 | Tier 1 | Tier 1 |
| wh_loser | s66_raw_janexcl | -0.79 | -0.5591 | -0.5685 | -0.0094 | Tier 1 | Tier 1 |
| jt_loser | s66_raw_janincl | -0.21 | -0.2481 | -0.2630 | -0.0150 | Tier 1 | Tier 1 |
| jt_loser | s66_raw_janexcl | -0.31 | -0.3728 | -0.3820 | -0.0092 | Tier 1 | Tier 1 |
| mg_loser | s66_raw_janincl | -0.07 | -0.1725 | -0.1810 | -0.0085 | Tier 1 | Tier 1 |
| mg_loser | s66_raw_janexcl | -0.05 | -0.1663 | -0.1664 | -0.0001 | Tier 2 | Tier 2 |

### Table VII gh_loser and gh_spread (all 8 columns)

| row | column | paper | ret | ret_dl | Δ(ret_dl−ret) | tier ret | tier ret_dl |
|---|---|---:|---:|---:|---:|---|---|
| gh_loser | s66_raw_janincl | 0.10 | 0.3973 | 0.3961 | -0.0012 | Tier 2 | Tier 2 |
| gh_loser | s66_raw_janexcl | -0.19 | 0.2555 | 0.2572 | +0.0016 | FAIL | FAIL |
| gh_loser | s66_ra_janincl | -0.09 | 0.1647 | 0.1605 | -0.0042 | FAIL | FAIL |
| gh_loser | s66_ra_janexcl | -0.26 | 0.1306 | 0.1302 | -0.0005 | FAIL | FAIL |
| gh_loser | s612_raw_janincl | 0.18 | 0.3769 | 0.3763 | -0.0005 | Tier 2 | Tier 2 |
| gh_loser | s612_raw_janexcl | -0.08 | 0.2474 | 0.2498 | +0.0024 | FAIL | FAIL |
| gh_loser | s612_ra_janincl | 0.01 | 0.1524 | 0.1490 | -0.0034 | Tier 2 | Tier 2 |
| gh_loser | s612_ra_janexcl | -0.14 | 0.1277 | 0.1280 | +0.0003 | FAIL | FAIL |
| gh_spread | s66_raw_janincl | 0.03 | -0.1125 | -0.1265 | -0.0140 | FAIL | FAIL |
| gh_spread | s66_raw_janexcl | 0.44 | 0.0247 | 0.0123 | -0.0124 | Tier 2 | Tier 2 |
| gh_spread | s66_ra_janincl | 0.32 | 0.0658 | 0.0569 | -0.0089 | Tier 2 | Tier 2 |
| gh_spread | s66_ra_janexcl | 0.55 | 0.1059 | 0.0976 | -0.0083 | Tier 2 | Tier 2 |
| gh_spread | s612_raw_janincl | -0.11 | -0.1246 | -0.1349 | -0.0104 | Tier 1 | Tier 1 |
| gh_spread | s612_raw_janexcl | 0.24 | 0.0012 | -0.0092 | -0.0104 | Tier 2 | FAIL |
| gh_spread | s612_ra_janincl | 0.13 | 0.0445 | 0.0384 | -0.0061 | Tier 1 | Tier 1 |
| gh_spread | s612_ra_janexcl | 0.33 | 0.0759 | 0.0689 | -0.0071 | Tier 2 | Tier 2 |

## 4. Diagnostic anchors (before/after vs paper)

| anchor | paper | before (ret) | after (ret_dl) | move | closer to paper? |
|---|---:|---:|---:|---:|---|
| Table V wh_loser (s66_raw_janincl) | -0.48 | -0.2873 | -0.3079 | -0.0206 | YES (|err| 0.1927 → 0.1721) |
| Table VII gh_loser (s66_raw_janexcl) | -0.19 | 0.2555 | 0.2572 | +0.0016 | no (|err| 0.4455 → 0.4472) |
| Table I jt_loser (all months) | 1.05 | 1.0890 | 1.0504 | -0.0386 | YES (|err| 0.0390 → 0.0004) |
| Table I mg_loser (all months) | 1.03 | 0.9771 | 0.9494 | -0.0277 | no (|err| 0.0529 → 0.0806) |

## 5. Diagnostics and gate status per variant

### variant `ret`
- T5 regression sample: s66 avg 4774.9 (min 1957), s612 avg 4774.9 (min 1957)
- T7 regression sample: s66 avg 4774.9 (min 1957), s612 avg 4774.9 (min 1957)
- T5 pre-flight gate: PASS
- T7 pre-flight gate: PASS
- Table I min cohorts available per holding month: 6

### variant `ret_dl`
- T5 regression sample: s66 avg 4803.6 (min 1962), s612 avg 4803.6 (min 1962)
- T7 regression sample: s66 avg 4803.6 (min 1962), s612 avg 4803.6 (min 1962)
- T5 pre-flight gate: PASS
- T7 pre-flight gate: PASS
- Table I min cohorts available per holding month: 6


## 6. Recommendation: **adopt `ret_dl`** as the official holding-period return column, by total Tier-1 count (+6 cells).

Criterion (pre-registered by the task): overall cell hit-rate (total Tier 1 across Tables I, II, III, V, VII).

- Total Tier 1 across all 5 tables: ret 332 vs ret_dl 338 (margin +6).
- Total FAIL: ret 16 vs ret_dl 18 (+2).
- Sum of |deviation| over all finite cells (mixed units, informational): ret 395.61 vs ret_dl 386.10 (-9.51).

The official outputs (results/table_*.md, data/strategy_returns.parquet,
data/fm_coefficients*.parquet) were regenerated under `ret_dl` by this
script AFTER writing this comparison.