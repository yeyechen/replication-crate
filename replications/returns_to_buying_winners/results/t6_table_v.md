# Table V — Proportion of months with positive returns for the 6/6 zero-cost strategy

Jegadeesh & Titman (1993), Table V (L1080–1100; audit-1 M4). Zero-cost buy-minus-sell 6/6 strategy, Jan 1965 – Dec 1989 (300 months): for each calendar month (25 obs), Feb.–Dec. (275 obs) and All months (300 obs), the proportion of months with a strictly positive return. PRIMARY = RAW series (A3-revision); the All column is bit-identical to the Table I PA 6/6 buy-sell series (max|diff| = 0.0, asserted). Size subsamples (A7) as in Table IV — deciles formed WITHIN each monthly size tercile.

| Month | All | S1 (small) | S2 (medium) | S3 (large) |
|-------|:---:|:----------:|:-----------:|:----------:|
| Jan. | 0.20 (5/25) | 0.16 (4/25) | 0.20 (5/25) | 0.48 (12/25) |
| Feb. | 0.64 (16/25) | 0.60 (15/25) | 0.72 (18/25) | 0.72 (18/25) |
| Mar. | 0.76 (19/25) | 0.72 (18/25) | 0.72 (18/25) | 0.72 (18/25) |
| Apr. | 0.96 (24/25) | 0.92 (23/25) | 0.88 (22/25) | 0.76 (19/25) |
| May | 0.68 (17/25) | 0.68 (17/25) | 0.68 (17/25) | 0.56 (14/25) |
| Jun. | 0.76 (19/25) | 0.64 (16/25) | 0.72 (18/25) | 0.72 (18/25) |
| Jul. | 0.60 (15/25) | 0.64 (16/25) | 0.56 (14/25) | 0.52 (13/25) |
| Aug. | 0.48 (12/25) | 0.60 (15/25) | 0.48 (12/25) | 0.48 (12/25) |
| Sep. | 0.68 (17/25) | 0.64 (16/25) | 0.76 (19/25) | 0.64 (16/25) |
| Oct. | 0.68 (17/25) | 0.60 (15/25) | 0.60 (15/25) | 0.56 (14/25) |
| Nov. | 0.88 (22/25) | 0.84 (21/25) | 0.84 (21/25) | 0.64 (16/25) |
| Dec. | 0.68 (17/25) | 0.72 (18/25) | 0.72 (18/25) | 0.44 (11/25) |
| Feb.–Dec. | 0.71 (195/275) | 0.69 (190/275) | 0.70 (192/275) | 0.61 (169/275) |
| All months | 0.67 (200/300) | 0.65 (194/300) | 0.66 (197/300) | 0.60 (181/300) |

Paper headline (L907): the strategy earns positive returns in 0.67 of all months and 0.71 of the non-January months.

## Anchor checks (ours vs paper)

| metric | ours | paper | deviation |
|--------|-----:|------:|----------:|
| prop_jan_all | 0.200000 | 0.24 | -16.7% |
| prop_apr_all | 0.960000 | 0.96 | +0.0% |
| prop_feb_dec_all | 0.709091 | 0.71 | -0.1% |
| prop_all_months_all | 0.666667 | 0.67 | -0.5% |
| prop_jan_s3 | 0.480000 | 0.44 | +9.1% |
| prop_jan_s1 | 0.160000 | 0.16 | +0.0% |
| prop_feb_dec_s3 | 0.614545 | 0.61 | +0.7% |
| prop_all_months_s3 | 0.603333 | 0.6 | +0.6% |

**Per-cell evaluation:** 56 cells — 56 Tier 1 / 0 Tier 2 / 0 FAIL (rule: within tolerance = Tier 1; same sign & ≤2× deviation = Tier 2; else FAIL).
