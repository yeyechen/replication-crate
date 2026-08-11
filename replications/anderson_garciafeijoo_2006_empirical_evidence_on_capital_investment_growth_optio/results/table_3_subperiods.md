# Table III Panel A subperiod robustness — Fama-MacBeth on 3 month masks

Three month masks (paper §II, content.md L186-196):
  - 1976-07 to 1987-06 (subperiod 1)
  - 1987-07 to 1999-06 (subperiod 2)
  - 1976-07 to 1999-06 with January excluded (Feb-Dec)

For each mask, the headline models are:
  - ret ~ ln_inv
  - ret ~ ln_size + ln_bm + ln_inv

Paper targets (per `inputs/content.md`):
  - 1976-1987: ln(inv) -3.96 (t -3.57), 4-var spec -2.94 (t -2.97)
  - 1987-1999: ln(inv) -4.40 (t -5.03), 4-var spec -4.06 (t -5.05)
  - Feb-Dec (full sample): ln(inv) -4.28 (t -5.84), 4-var spec -3.49 (t -5.25)

## Mask: subperiod_1976_1987 (132 months, 416,478 obs)

### model5_ln_inv

| Variable | Coef (%/unit) | t-stat |
|---|---:|---:|
| ln_inv | -0.24 | -5.15 |
| Avg R² | 0.0017 | |

### model6_ln_size_ln_bm_ln_inv

| Variable | Coef (%/unit) | t-stat |
|---|---:|---:|
| ln_me | -0.13 | -2.01 |
| ln_bm | 0.37 | 3.03 |
| ln_inv | -0.15 | -3.65 |
| Avg R² | 0.0194 | |

## Mask: subperiod_1987_1999 (144 months, 549,502 obs)

### model5_ln_inv

| Variable | Coef (%/unit) | t-stat |
|---|---:|---:|
| ln_inv | -0.28 | -4.85 |
| Avg R² | 0.0015 | |

### model6_ln_size_ln_bm_ln_inv

| Variable | Coef (%/unit) | t-stat |
|---|---:|---:|
| ln_me | -0.08 | -1.03 |
| ln_bm | 0.33 | 3.24 |
| ln_inv | -0.21 | -4.53 |
| Avg R² | 0.0140 | |

## Mask: feb_dec (253 months, 885,872 obs)

### model5_ln_inv

| Variable | Coef (%/unit) | t-stat |
|---|---:|---:|
| ln_inv | -0.23 | -6.16 |
| Avg R² | 0.0016 | |

### model6_ln_size_ln_bm_ln_inv

| Variable | Coef (%/unit) | t-stat |
|---|---:|---:|
| ln_me | 0.02 | 0.39 |
| ln_bm | 0.40 | 4.98 |
| ln_inv | -0.17 | -5.16 |
| Avg R² | 0.0148 | |
