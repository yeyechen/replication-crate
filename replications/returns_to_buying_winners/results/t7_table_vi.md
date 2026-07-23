# Table VI — Subperiod average returns of the 6/6 zero-cost strategy

Jegadeesh & Titman (1993), Table VI (L1120–1238; audit-1 M4). Zero-cost buy-minus-sell 6/6 strategy sliced into 5-year subperiods; each cell: average monthly return with the iid t-statistic beneath (n = 60 for All months, 5 for Jan., 55 for Feb.–Dec.). PRIMARY = RAW series (A3-revision); the All column is bit-identical to the Table I PA 6/6 buy-sell series (max|diff| = 0.0, asserted). Size subsamples (A7) as in Table IV.

## All

| Months | 1965–69 | 1970–74 | 1975–79 | 1980–84 | 1985–89 |
|--------|:---:|:---:|:---:|:---:|:---:|
| All months | +0.0116<br>(+1.82) | +0.0091<br>(+1.02) | -0.0064<br>(-0.83) | +0.0130<br>(+2.80) | +0.0166<br>(+3.37) |
| Jan. | -0.0552<br>(-1.31) | -0.1129<br>(-2.47) | -0.0990<br>(-1.50) | -0.0290<br>(-1.95) | -0.0569<br>(-2.72) |
| Feb.–Dec. | +0.0177<br>(+3.32) | +0.0202<br>(+2.73) | +0.0021<br>(+0.41) | +0.0168<br>(+3.67) | +0.0233<br>(+5.81) |

## S1 (small)

| Months | 1965–69 | 1970–74 | 1975–79 | 1980–84 | 1985–89 |
|--------|:---:|:---:|:---:|:---:|:---:|
| All months | +0.0061<br>(+0.86) | +0.0099<br>(+1.25) | -0.0112<br>(-1.24) | +0.0163<br>(+2.69) | +0.0198<br>(+2.66) |
| Jan. | -0.0885<br>(-1.61) | -0.0942<br>(-2.09) | -0.1079<br>(-1.31) | -0.0197<br>(-1.15) | -0.1039<br>(-4.29) |
| Feb.–Dec. | +0.0147<br>(+3.01) | +0.0193<br>(+3.04) | -0.0024<br>(-0.41) | +0.0195<br>(+3.12) | +0.0311<br>(+5.33) |

## S2 (medium)

| Months | 1965–69 | 1970–74 | 1975–79 | 1980–84 | 1985–89 |
|--------|:---:|:---:|:---:|:---:|:---:|
| All months | +0.0169<br>(+2.95) | +0.0095<br>(+1.32) | +0.0000<br>(+0.01) | +0.0168<br>(+3.46) | +0.0126<br>(+3.04) |
| Jan. | -0.0228<br>(-0.88) | -0.0453<br>(-1.64) | -0.0742<br>(-1.19) | -0.0135<br>(-0.74) | -0.0078<br>(-0.35) |
| Feb.–Dec. | +0.0206<br>(+3.64) | +0.0145<br>(+2.03) | +0.0068<br>(+1.54) | +0.0195<br>(+3.98) | +0.0145<br>(+3.59) |

## S3 (large)

| Months | 1965–69 | 1970–74 | 1975–79 | 1980–84 | 1985–89 |
|--------|:---:|:---:|:---:|:---:|:---:|
| All months | +0.0142<br>(+2.87) | +0.0096<br>(+1.36) | +0.0025<br>(+0.49) | +0.0070<br>(+1.35) | +0.0020<br>(+0.42) |
| Jan. | -0.0077<br>(-0.36) | -0.0181<br>(-0.53) | -0.0312<br>(-0.72) | -0.0082<br>(-0.30) | -0.0149<br>(-0.79) |
| Feb.–Dec. | +0.0162<br>(+3.23) | +0.0121<br>(+1.71) | +0.0055<br>(+1.40) | +0.0084<br>(+1.64) | +0.0036<br>(+0.72) |

Paper's qualitative claims: profits are positive in 4 of the 5 subperiods; the single negative full-period cell is 1975–79 (paper −0.0044, t −0.51), driven by the small-firm January effect (S1 Jan 1975–79 paper −0.1107).

## Anchor checks (ours vs paper)

| metric | ours | paper | deviation |
|--------|-----:|------:|----------:|
| sp_all_all_6569 | 0.011650 | 0.0123 | -5.3% |
| sp_all_all_6569_t | 1.823701 | 1.94 | -6.0% |
| sp_all_all_7579 | -0.006356 | -0.0044 | -44.5% |
| sp_all_all_7579_t | -0.825575 | -0.51 | -61.9% |
| sp_all_jan_7074 | -0.112865 | -0.107 | -5.5% |
| sp_all_jan_7074_t | -2.467153 | -2.54 | +2.9% |
| sp_s1_jan_8589 | -0.103946 | -0.1064 | +2.3% |
| sp_s1_jan_8589_t | -4.286074 | -4.45 | +3.7% |
| sp_s3_feb_dec_8589 | 0.003557 | 0.0052 | -31.6% |
| sp_s3_feb_dec_8589_t | 0.715156 | 1.04 | -31.2% |
| sp_s2_all_6569 | 0.016940 | 0.0177 | -4.3% |
| sp_s2_all_6569_t | 2.950926 | 3.08 | -4.2% |

**Per-cell evaluation:** 120 cells — 110 Tier 1 / 8 Tier 2 / 2 FAIL (rule: within tolerance = Tier 1; same sign & ≤2× deviation = Tier 2; else FAIL).
