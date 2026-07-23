# Table IV — Calendar-month average returns of the 6/6 zero-cost strategy

Jegadeesh & Titman (1993), Table IV. Zero-cost buy-minus-sell 6/6 strategy; each
cell: average return over that calendar month across 1965–1989 (25 Januaries etc.),
with the iid t-statistic beneath. Feb.–Dec.: the 275 non-January months. PRIMARY =
RAW series (A3-revision); the All column is bit-identical to the Table I PA 6/6
buy-sell series. Size subsamples (A7): at each formation month, stocks with
cumret_6_raw AND me_millions non-NULL are split into terciles of me_millions
(equal counts, floor-rank convention, ties by permno) — S1 smallest, S3 largest —
and deciles are formed WITHIN each tercile. F_a: Wald F that the 12 monthly means
are jointly equal (11 Feb..Dec dummies, intercept = January mean, 300 obs); F_b:
same on the 275 Feb–Dec obs (10 Mar..Dec dummies, intercept = February mean).
p-values in parentheses; p-values are NOT metrics (contract note).

| Month | All | S1 (small) | S2 (medium) | S3 (large) |
|-------|:---:|:----------:|:-----------:|:----------:|
| Jan. | -0.0706<br>(-3.85) | -0.0828<br>(-3.83) | -0.0327<br>(-2.16) | -0.0160<br>(-1.27) |
| Feb. | +0.0041<br>(+0.55) | +0.0033<br>(+0.31) | +0.0131<br>(+2.31) | +0.0101<br>(+1.43) |
| Mar. | +0.0103<br>(+1.45) | +0.0187<br>(+2.35) | +0.0093<br>(+1.32) | +0.0102<br>(+1.37) |
| Apr. | +0.0304<br>(+6.94) | +0.0263<br>(+4.68) | +0.0339<br>(+6.82) | +0.0212<br>(+4.56) |
| May | +0.0091<br>(+1.15) | +0.0016<br>(+0.17) | +0.0079<br>(+1.08) | +0.0090<br>(+1.36) |
| Jun. | +0.0226<br>(+3.91) | +0.0222<br>(+3.16) | +0.0226<br>(+3.27) | +0.0181<br>(+2.72) |
| Jul. | +0.0077<br>(+1.00) | +0.0116<br>(+1.54) | +0.0088<br>(+1.04) | +0.0032<br>(+0.37) |
| Aug. | +0.0037<br>(+0.50) | +0.0088<br>(+1.09) | -0.0044<br>(-0.57) | -0.0049<br>(-0.61) |
| Sep. | +0.0101<br>(+0.94) | +0.0079<br>(+0.70) | +0.0138<br>(+1.29) | +0.0049<br>(+0.58) |
| Oct. | +0.0148<br>(+1.44) | +0.0168<br>(+1.58) | +0.0140<br>(+1.37) | +0.0017<br>(+0.15) |
| Nov. | +0.0368<br>(+5.40) | +0.0332<br>(+4.73) | +0.0302<br>(+3.86) | +0.0218<br>(+2.41) |
| Dec. | +0.0266<br>(+2.82) | +0.0306<br>(+3.11) | +0.0176<br>(+2.44) | +0.0055<br>(+0.79) |
| Feb.–Dec. | +0.0160<br>(+6.57) | +0.0165<br>(+6.15) | +0.0152<br>(+6.34) | +0.0092<br>(+3.84) |
| F (12 months equal) | 8.65<br>(0.000) | 8.44<br>(0.000) | 3.95<br>(0.000) | 1.67<br>(0.080) |
| F (Feb–Dec equal) | 2.02<br>(0.031) | 1.51<br>(0.137) | 1.90<br>(0.045) | 1.14<br>(0.333) |

## Anchor checks (ours vs paper)

| metric | ours | paper | deviation |
|--------|-----:|------:|----------:|
| jan_all_t4 | -0.070586 | -0.0686 | -2.9% |
| jan_all_t4_t | -3.852813 | -3.52 | -9.5% |
| apr_all_t4 | 0.030386 | 0.0333 | -8.8% |
| apr_all_t4_t | 6.941929 | 7.39 | -6.1% |
| feb_dec_all_t4 | 0.016014 | 0.0166 | -3.5% |
| feb_dec_all_t4_t | 6.572556 | 6.67 | -1.5% |
| jan_s1_t4 | -0.082846 | -0.0797 | -3.9% |
| jan_s1_t4_t | -3.827953 | -3.36 | -13.9% |
| jan_s3_t4 | -0.016020 | -0.0161 | +0.5% |
| jan_s3_t4_t | -1.274556 | -1.28 | +0.4% |
| f_a_all_t4 | 8.646596 | 7.9 | +9.5% |
| f_b_all_t4 | 2.024001 | 2.04 | -0.8% |

**Per-cell evaluation:** 112 cells — 105 Tier 1 / 5 Tier 2 / 2 FAIL (rule: within tolerance = Tier 1; same sign & ≤2× deviation = Tier 2; else FAIL).
