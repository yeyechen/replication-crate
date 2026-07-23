# Table 2 — Excess returns to portfolios sorted on profitability and book-to-market

Novy-Marx (2013), Table 2. Monthly value-weighted average excess returns (%/month) to quintile portfolios sorted on gross profits-to-assets (Panel A) and book-to-market (Panel B). NYSE breakpoints; annual rebalancing at the end of June; portfolios held July t – June t+1. Sample July 1963 – December 2010 (570 months). Alpha and factor loadings from time-series OLS of portfolio excess returns on the Fama-French three factors (MKT, SMB, HML); t-statistics in brackets. Characteristics are time-series averages of monthly portfolio-level values: GP/A = Sum(GP)/Sum(AT); B/M = Sum(book equity)/Sum(ME) (firms with positive book equity); ME = per-firm market equity in $millions; n = number of firms.

## Panel A: Portfolios sorted on gross profits-to-assets (GP/A)

| Portfolio | r^e | alpha | MKT | SMB | HML | GP/A | B/M | ME($M) | n |
|---|---|---|---|---|---|---|---|---|---|
| Low | 0.30 | -0.21 | 0.95 | 0.03 | 0.17 | 0.10 | 0.88 | 838 | 680 |
| 2 | 0.39 | -0.12 | 1.02 | -0.08 | 0.15 | 0.21 | 0.73 | 1,175 | 561 |
| 3 | 0.52 | 0.04 | 1.02 | 0.06 | 0.04 | 0.32 | 0.58 | 1,107 | 615 |
| 4 | 0.41 | 0.06 | 1.02 | 0.02 | -0.24 | 0.45 | 0.40 | 1,257 | 673 |
| High | 0.62 | 0.34 | 0.92 | -0.04 | -0.28 | 0.71 | 0.27 | 1,193 | 780 |
| H-L | 0.32 | 0.54 | -0.03 | -0.07 | -0.45 | | | | |
| H-L t | [2.51] | [4.58] | [-1.07] | [-1.85] | [-10.58] | | | | |

## Panel B: Portfolios sorted on book-to-market (B/M)

| Portfolio | r^e | alpha | MKT | SMB | HML | GP/A | B/M | ME($M) | n |
|---|---|---|---|---|---|---|---|---|---|
| Low | 0.37 | 0.13 | 1.00 | -0.09 | -0.43 | 0.46 | 0.23 | 2,095 | 809 |
| 2 | 0.47 | 0.01 | 1.00 | 0.04 | 0.01 | 0.32 | 0.47 | 1,378 | 585 |
| 3 | 0.53 | 0.02 | 0.94 | 0.02 | 0.18 | 0.27 | 0.68 | 885 | 544 |
| 4 | 0.65 | 0.02 | 0.95 | 0.11 | 0.44 | 0.22 | 0.91 | 685 | 562 |
| High | 0.75 | -0.06 | 1.00 | 0.25 | 0.71 | 0.19 | 1.43 | 426 | 717 |
| H-L | 0.38 | -0.19 | 0.01 | 0.34 | 1.14 | | | | |
| H-L t | [2.44] | [-2.33] | [0.34] | [12.89] | [38.74] | | | | |

## Panel A vs paper (per-cell comparison)

Tier 1 = within tolerance (returns 30%, alphas 50%, loadings and t-stats 40%, characteristics 30%); Tier 2 = correct sign but outside tolerance; FAIL = wrong sign.

| Row | Metric | Paper | Ours | Deviation | Tier |
|---|---|---|---|---|---|
| Low | re | 0.31 | 0.303 | -2.4% | Tier 1 |
| Low | alpha | -0.18 | -0.207 | -14.8% | Tier 1 |
| Low | mkt | 0.94 | 0.951 | +1.2% | Tier 1 |
| Low | smb | 0.04 | 0.034 | -14.6% | Tier 1 |
| Low | hml | 0.15 | 0.174 | +15.9% | Tier 1 |
| Low | gp_a | 0.1 | 0.102 | +1.7% | Tier 1 |
| Low | bm | 1.1 | 0.882 | -19.8% | Tier 1 |
| Low | me | 748 | 837.825 | +12.0% | Tier 1 |
| Low | n | 771 | 680.112 | -11.8% | Tier 1 |
| 2 | re | 0.41 | 0.388 | -5.5% | Tier 1 |
| 2 | alpha | -0.11 | -0.122 | -10.7% | Tier 1 |
| 2 | mkt | 1.03 | 1.018 | -1.1% | Tier 1 |
| 2 | smb | -0.07 | -0.079 | -13.5% | Tier 1 |
| 2 | hml | 0.2 | 0.153 | -23.4% | Tier 1 |
| 2 | gp_a | 0.2 | 0.211 | +5.5% | Tier 1 |
| 2 | bm | 0.98 | 0.725 | -26.0% | Tier 1 |
| 2 | me | 1100 | 1174.802 | +6.8% | Tier 1 |
| 2 | n | 598 | 561.228 | -6.1% | Tier 1 |
| 3 | re | 0.52 | 0.525 | +1.0% | Tier 1 |
| 3 | alpha | 0.02 | 0.044 | +118.9% | Tier 2 |
| 3 | mkt | 1.02 | 1.015 | -0.5% | Tier 1 |
| 3 | smb | -0 | 0.057 | +0.057 (paper ~0) | Tier 2 |
| 3 | hml | 0.12 | 0.035 | -70.7% | Tier 2 |
| 3 | gp_a | 0.3 | 0.318 | +6.1% | Tier 1 |
| 3 | bm | 1 | 0.585 | -41.5% | Tier 2 |
| 3 | me | 1114 | 1106.729 | -0.7% | Tier 1 |
| 3 | n | 670 | 614.788 | -8.2% | Tier 1 |
| 4 | re | 0.41 | 0.414 | +1.0% | Tier 1 |
| 4 | alpha | 0.05 | 0.060 | +21.0% | Tier 1 |
| 4 | mkt | 1.01 | 1.017 | +0.7% | Tier 1 |
| 4 | smb | 0.04 | 0.019 | -51.4% | Tier 2 |
| 4 | hml | -0.24 | -0.241 | -0.3% | Tier 1 |
| 4 | gp_a | 0.42 | 0.449 | +6.8% | Tier 1 |
| 4 | bm | 0.53 | 0.403 | -23.9% | Tier 1 |
| 4 | me | 1114 | 1256.854 | +12.8% | Tier 1 |
| 4 | n | 779 | 672.854 | -13.6% | Tier 1 |
| High | re | 0.62 | 0.619 | -0.1% | Tier 1 |
| High | alpha | 0.34 | 0.336 | -1.2% | Tier 1 |
| High | mkt | 0.92 | 0.921 | +0.2% | Tier 1 |
| High | smb | -0.04 | -0.038 | +6.1% | Tier 1 |
| High | hml | -0.29 | -0.279 | +3.7% | Tier 1 |
| High | gp_a | 0.68 | 0.709 | +4.3% | Tier 1 |
| High | bm | 0.33 | 0.270 | -18.2% | Tier 1 |
| High | me | 1096 | 1193.470 | +8.9% | Tier 1 |
| High | n | 938 | 779.784 | -16.9% | Tier 1 |
| H-L | re | 0.31 | 0.317 | +2.1% | Tier 1 |
| H-L | alpha | 0.52 | 0.543 | +4.3% | Tier 1 |
| H-L | mkt | -0.03 | -0.030 | +0.6% | Tier 1 |
| H-L | smb | -0.08 | -0.072 | +10.4% | Tier 1 |
| H-L | hml | -0.44 | -0.453 | -3.0% | Tier 1 |
| H-L t | re | 2.49 | 2.506 | +0.6% | Tier 1 |
| H-L t | alpha | 4.49 | 4.582 | +2.1% | Tier 1 |
| H-L t | mkt | -0.99 | -1.074 | -8.5% | Tier 1 |
| H-L t | smb | -2.15 | -1.846 | +14.1% | Tier 1 |
| H-L t | hml | -10.8 | -10.583 | +2.0% | Tier 1 |

**Summary: 50 Tier 1, 5 Tier 2, 0 FAIL (of 55 cells).**
