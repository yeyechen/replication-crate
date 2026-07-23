# Table 7 — Regression Statistics for CAR_j on FEP_j and FSQ_j (eq. 16)

50 portfolio observations (FEP 1-10 x quintile I-V); FSQ coding per L2102
(FEP1-5: I-V = 10,9,8,7,6; FEP6-10: I-V = 1,2,3,4,5). OLS with intercept via
statsmodels; rows with a missing Table-6 cell dropped. Reported: alpha, t(alpha),
b1/b2, t(b1/b2), adjusted R-squared.

### Model 1, window [-1, 0]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -1.59 | -9.95 | 0.31 | 12.15 | nan | nan | 0.750 |
| FSQ-only | 1.71 | 8.90 | nan | nan | -0.29 | -9.27 | 0.634 |
| FEP+FSQ | -0.42 | -1.13 | 0.22 | 6.19 | -0.12 | -3.38 | 0.794 |

### Model 1, window [-60, 0]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -4.87 | -12.16 | 0.88 | 13.62 | nan | nan | 0.790 |
| FSQ-only | 4.12 | 7.22 | nan | nan | -0.75 | -8.21 | 0.575 |
| FEP+FSQ | -2.88 | -2.88 | 0.72 | 7.59 | -0.21 | -2.16 | 0.805 |

### Model 1, window [+1, +60]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -2.24 | -11.43 | 0.37 | 11.61 | nan | nan | 0.732 |
| FSQ-only | 1.61 | 6.72 | nan | nan | -0.33 | -8.64 | 0.600 |
| FEP+FSQ | -0.98 | -2.09 | 0.27 | 5.95 | -0.13 | -2.88 | 0.767 |

### Model 2, window [-1, 0]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -1.58 | -10.86 | 0.31 | 13.29 | nan | nan | 0.782 |
| FSQ-only | 1.78 | 10.79 | nan | nan | -0.30 | -11.25 | 0.719 |
| FEP+FSQ | -0.15 | -0.48 | 0.20 | 6.84 | -0.15 | -5.08 | 0.856 |

### Model 2, window [-60, 0]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -4.41 | -12.42 | 0.82 | 14.29 | nan | nan | 0.806 |
| FSQ-only | 4.24 | 9.39 | nan | nan | -0.76 | -10.38 | 0.685 |
| FEP+FSQ | -1.32 | -1.67 | 0.58 | 7.64 | -0.32 | -4.25 | 0.857 |

### Model 2, window [+1, +60]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -1.94 | -10.71 | 0.33 | 11.45 | nan | nan | 0.726 |
| FSQ-only | 1.62 | 7.84 | nan | nan | -0.31 | -9.39 | 0.640 |
| FEP+FSQ | -0.55 | -1.31 | 0.22 | 5.63 | -0.14 | -3.59 | 0.781 |

### Model 3, window [-1, 0]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -6.86 | -15.17 | 1.28 | 17.53 | nan | nan | 0.862 |
| FSQ-only | 5.83 | 7.16 | nan | nan | -1.03 | -7.84 | 0.553 |
| FEP+FSQ | -5.46 | -4.70 | 1.17 | 10.54 | -0.14 | -1.31 | 0.864 |

### Model 3, window [-60, 0]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -6.13 | -14.64 | 1.11 | 16.40 | nan | nan | 0.845 |
| FSQ-only | 4.86 | 6.72 | nan | nan | -0.89 | -7.64 | 0.539 |
| FEP+FSQ | -4.96 | -4.60 | 1.02 | 9.86 | -0.12 | -1.17 | 0.847 |

### Model 3, window [+1, +60]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -0.94 | -6.61 | 0.12 | 5.39 | nan | nan | 0.364 |
| FSQ-only | 0.16 | 0.94 | nan | nan | -0.08 | -2.81 | 0.123 |
| FEP+FSQ | -1.35 | -3.68 | 0.16 | 4.45 | 0.04 | 1.21 | 0.370 |

### Model 4, window [-1, 0]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -1.72 | -10.86 | 0.34 | 13.35 | nan | nan | 0.783 |
| FSQ-only | 1.84 | 8.99 | nan | nan | -0.31 | -9.30 | 0.635 |
| FEP+FSQ | -0.59 | -1.59 | 0.25 | 7.08 | -0.12 | -3.27 | 0.820 |

### Model 4, window [-60, 0]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -25.29 | -20.08 | 4.60 | 22.64 | nan | nan | 0.913 |
| FSQ-only | 20.66 | 7.70 | nan | nan | -3.76 | -8.69 | 0.603 |
| FEP+FSQ | -19.04 | -6.06 | 4.11 | 13.70 | -0.65 | -2.16 | 0.919 |

### Model 4, window [+1, +60]  (n: fep=50 fsq=50 both=50)

| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |
|---|---|---|---|---|---|---|---|
| FEP-only | -0.18 | -0.93 | -0.02 | -0.67 | nan | nan | -0.011 |
| FSQ-only | -0.41 | -2.18 | nan | nan | 0.02 | 0.73 | -0.010 |
| FEP+FSQ | -0.33 | -0.66 | -0.01 | -0.18 | 0.02 | 0.33 | -0.030 |

