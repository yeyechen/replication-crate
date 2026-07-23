# Table 4 — Cumulative Average Residuals for Forecast Error Portfolios: All Observations Pooled

CAR (percent) = mean per-observation CAR by (fep, model). Stars from the
paper's TWO-STAGE empirical-distribution test (L1357-1363): 1,000 draws of 8,000
(firm, quarter) pairs without replacement from the full frame (firms in panel x 32
qlabels), keeping those present in the per-window availability pool; '*' iff observed
CAR < p1 (FEP1-5) or > p99 (FEP6-10) of the kept-set mean distribution. seed=42.

Frame = 3024 firms x 32 qlabels = 96768 pairs. Per-window kept-set size m1_0: 6298-6512 (mean 6406); m60_0: 6300-6531 (mean 6406); p1_60: 6289-6520 (mean 6406). Percentiles (p1/p99): m1_0: 0.077/0.370; m60_0: -0.338/0.553; p1_60: -0.721/0.225

| FEP | [-1, 0] M1 | [-1, 0] M2 | [-1, 0] M3 | [-1, 0] M4 | [-60, 0] M1 | [-60, 0] M2 | [-60, 0] M3 | [-60, 0] M4 | [+1, +60] M1 | [+1, +60] M2 | [+1, +60] M3 | [+1, +60] M4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | -1.85* | -1.51* | -7.34* | -1.89* | -5.70* | -4.26* | -7.13* | -23.10* | -2.28* | -1.34* | -0.90* | -0.40 |
| 2 | -1.20* | -0.98* | -3.93* | -1.06* | -3.52* | -3.12* | -3.46* | -15.58* | -1.57* | -1.70* | -0.25 | -0.45 |
| 3 | -0.58* | -0.79* | -2.52* | -0.64* | -1.47* | -2.28* | -1.82* | -11.03* | -1.43* | -1.08* | -0.49 | 0.18 |
| 4 | -0.22* | -0.42* | -1.33* | -0.29* | -0.78* | -0.88* | -0.93* | -7.08* | -0.62 | -0.80* | -0.67 | 0.05 |
| 5 | 0.13 | -0.01* | -0.42* | 0.13 | -0.04 | 0.13 | -0.34* | -3.00* | -0.47 | -0.14 | 0.01 | 0.16 |
| 6 | 0.46* | 0.40* | 0.47* | 0.46* | 0.87* | 1.02* | 0.71* | 1.17* | -0.09 | 0.39* | -0.40 | 0.12 |
| 7 | 0.88* | 0.83* | 1.44* | 0.77* | 1.81* | 1.85* | 1.38* | 5.47* | 0.49* | 0.31* | -0.38 | -0.87 |
| 8 | 1.38* | 1.18* | 2.64* | 1.16* | 3.12* | 2.46* | 2.17* | 10.13* | 1.28* | 0.92* | -0.26 | -0.19 |
| 9 | 1.96* | 1.40* | 4.34* | 1.53* | 4.40* | 3.28* | 3.66* | 15.85* | 1.75* | 1.43* | 0.51* | -0.08 |
| 10 | 1.37* | 1.95* | 9.03* | 2.07* | 3.31* | 4.54* | 7.05* | 28.17* | 1.22* | 1.79* | 0.50* | -0.93 |

Star pattern agreement with the paper: 110/120.

Mismatches (FEP, window, model, our CAR, our star, paper star):
- FEP1 p1_60 M3: -0.90 ours=* paper=-
- FEP4 p1_60 M1: -0.62 ours=- paper=*
- FEP5 m1_0 M2: -0.01 ours=* paper=-
- FEP5 m60_0 M1: -0.04 ours=- paper=*
- FEP5 p1_60 M1: -0.47 ours=- paper=*
- FEP6 m1_0 M1: 0.46 ours=* paper=-
- FEP6 m1_0 M4: 0.46 ours=* paper=-
- FEP6 p1_60 M1: -0.09 ours=- paper=*
- FEP9 p1_60 M3: 0.51 ours=* paper=-
- FEP10 p1_60 M3: 0.50 ours=* paper=-
