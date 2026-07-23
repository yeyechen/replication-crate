# Piotroski (2000) pipeline — global sanity checks
Restricted sample: FY1987-FY1995 (formation years 1988-1996), assumptions.md A1 (oancf NULL for FY<1987 in comp_202601).

## 1. Panel dimensions / columns / dtypes
rows x cols: 5,736 x 43
unique gvkey: 2,361; fyears: [1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995]; formation years: [1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996]
```
gvkey                   str
permno                Int32
fyear                 int64
datadate                str
formation_year        int64
mve                 float64
assets              float64
be                  float64
bm                  float64
bm_q                  int64
size_bucket           int64
roa                 float64
cfo                 float64
droa                float64
accrual             float64
dlever              float64
dliquid             float64
dmargin             float64
dturn               float64
eq_issued             int64
f_roa                 int64
f_droa                int64
f_cfo                 int64
f_accrual             int64
f_dlever              int64
f_dliquid             int64
f_dmargin             int64
f_dturn               int64
eq_offer              int64
f_score               int64
rank_score          float64
rank_q              float64
raw_ret1            float64
mkt_ret1            float64
ma_ret1             float64
n_months_traded1      int64
raw_ret2            float64
mkt_ret2            float64
ma_ret2             float64
n_months_traded2      int64
moment              float64
moment_decile       float64
accrual_decile      float64
```

## 2. Counts by formation_year (paper Appendix A, same years)
| formation_year | ours | paper | delta |
|---|---:|---:|---:|
| 1987 | 4 | n/a | n/a |
| 1988 | 211 | 684 | -473 |
| 1989 | 609 | 765 | -156 |
| 1990 | 696 | 1,256 | -560 |
| 1991 | 1,068 | 569 | +499 |
| 1992 | 476 | 622 | -146 |
| 1993 | 535 | 602 | -67 |
| 1994 | 591 | 1,116 | -525 |
| 1995 | 902 | 876 | +26 |
| 1996 | 644 | 715 | -71 |
| **total** | **5,736** | **7,205** | **-1,469** |
(formation 1987 rows = FY1987 firms with Jun/Jul-1987 fiscal year-ends, whose +5-month window starts in Nov/Dec 1987; the paper's Appendix A calendar-year labeling would place these in 1987 too. The task's 1988-1996 comparison list assumes December-FYE firms.)

## 3. F_SCORE distribution (paper full sample 1976-1996)
| score | ours | paper |
|---|---:|---:|
| 0 | 21 | 57 |
| 1 | 156 | 339 |
| 2 | 392 | 859 |
| 3 | 743 | 1,618 |
| 4 | 1,003 | 2,462 |
| 5 | 1,135 | 2,787 |
| 6 | 993 | 2,579 |
| 7 | 747 | 1,894 |
| 8 | 405 | 1,115 |
| 9 | 141 | 333 |
Low {0,1}: 177 (paper 396); High {8,9}: 546 (paper 1,448)

## 4. Signal proportions (good-signal share vs paper Table 1)
| signal | ours | paper | delta |
|---|---:|---:|---:|
| roa | 0.558 | 0.632 | -0.074 |
| droa | 0.414 | 0.432 | -0.018 |
| dmargin | 0.439 | 0.454 | -0.015 |
| cfo | 0.733 | 0.755 | -0.022 |
| dliquid | 0.441 | 0.384 | +0.057 |
| dlever | 0.506 | 0.498 | +0.008 |
| dturn | 0.481 | 0.534 | -0.053 |
| accrual | 0.794 | 0.780 | +0.014 |
(EQ_OFFER share (no issuance): 0.611; eq_issued share: 0.389)

## 5. Summary stats vs paper Table 1
MVE  ($M): mean 182.48 (paper 188.5); median 15.819 (paper 14.365)
BM       : mean 2.591 (paper 2.444); median 1.532 (paper 1.721)
ROA      : mean -0.0195 (paper -0.0054); median 0.0060 (paper 0.0128)
ASSETS   : mean 620.83 (paper 1043.99)

## 6. Returns (paper Table 1 Panel B / Table 3 'All Firms')
raw_ret1 mean 0.229 (paper 0.239); pct positive 0.557 (paper 0.610)
ma_ret1  mean 0.058 (paper 0.059); median -0.108 (paper -0.061); pct positive 0.395 (paper 0.437)
raw_ret2 mean 0.498 (paper 0.479)
ma_ret2  mean 0.115 (paper 0.127); pct positive 0.364 (paper 0.432)
1-yr windows with <12 traded months (delisted/gaps): 543 (9.5%)

## 7. Size bucket counts (paper: small 8,302 / medium 3,906 / large 1,835)
small 3,363 (58.6%) | medium 1,630 (28.4%) | large 743 (13.0%)

## 8. Drop statistics (high-BM Q5 firm-years)
funda firm-years FY1987-1995 with valid BM (ME>0, BE>0): 58,972
classified high-BM (Q5, prior-year cutoffs): 12,038
dropped for missing signal inputs: 5,755 (47.8% of Q5)
dropped for missing CRSP link (no P/C permno): 547
final panel: 5,736

Per-signal missing counts among dropped (NON-exclusive — a firm-year can
miss several inputs; eq_offer never binds, sstk NULL = no issuance):
| signal | firm-years missing inputs |
|---|---:|
| roa | 603 |
| cfo | 3,732 |
| droa | 1,437 |
| accrual | 3,732 |
| dlever | 1,509 |
| dliquid | 3,623 |
| dmargin | 1,117 |
| dturn | 1,549 |

First-binding-signal attribution (paper signal order roa→cfo→droa→accrual→dlever→dliquid→dmargin→dturn):
| binding signal | firm-years |
|---|---:|
| roa | 603 |
| cfo | 3,129 |
| droa | 348 |
| accrual | 0 |
| dlever | 0 |
| dliquid | 1,546 |
| dmargin | 129 |
| dturn | 0 |

## 9. Anomalies, ambiguities, deviations
- SAMPLE SCOPE (user-approved, A1): FY1987-1995 only; all paper full-sample counts (14,043; per-score n's; size n's) are Tier-2 references, not numeric targets.
- rank_q is NaN for the FY1987 cohort (173 rows): its prior-year (FY1986) RANK_SCORE distribution cannot be computed — oancf is NULL for FY<1987, so the CFO/ACCRUAL signals (hence RANK_SCORE) do not exist for FY1986. Consequence of A1; fyear 1988+ cohorts use normal prior-year cutoffs.
- accrual_decile for the FY1987 cohort would use FY1986 all-Compustat accrual breakpoints, but FY1986 has 0 universe firm-years with accrual available (oancf is NULL for all FY<1987) — accrual_decile is NaN for all 173 FY1987 panel rows. FY1987 breakpoints (used by fyear 1988+) come from 909 universe firm-years.
- 4 panel rows carry formation_year 1987 (FY1987 firms with mid-year fiscal year-ends); excluded from the paper's 1988-1996 Appendix A comparison.
- 0 panel rows had missing market-window BHRs (expected 0 — msi is continuous).
- No-link drops (547) are firm-years the paper would also lose (returns are CRSP-based); they are excluded from the panel, not kept with NULL returns.
- BM/size cutoffs use quantileExact (empirical percentiles) over the full Compustat universe; RANK_SCORE/decile cutoffs use the same convention (numpy linear / quantileExact). The paper's SAS percentile definition is unspecified; boundary ties affect a few firms per year at most.
- RANK_SCORE ranks the nine realizations mechanically with NO sign flip (footnote 12), including eq_issued (1 = issued) as specified.
- msf returned no sentinel rows (ret <= -1) in 1985-1999 (verified); the ret > -1 filter and greatest(ret, -0.9999) guard remain as defense.
- ΔTURN uses average total assets (Table 1 footnote j, A4), not beginning-of-year assets (text L246) — documented paper discrepancy.

## rank_q distribution (extra)
```
rank_q
1.0    1112
2.0    1116
3.0    1070
4.0    1156
5.0    1109
NaN     173
```