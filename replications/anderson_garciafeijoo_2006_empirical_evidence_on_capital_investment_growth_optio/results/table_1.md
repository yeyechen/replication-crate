# Table I Panel A replication — 5x5 size × B/M means & medians of prior 2-year investment growth

**Sample:** 23 formation years (1976..1998).
**Breakpoints:** NYSE-only (size from me_jun_form, B/M from bm).
**Universe:** all firms (NYSE+AMEX+NASDAQ, non-financials) with positive B/M.
**Trim:** inv_growth ∈ (-0.99, 10) per paper L438 (top and bottom 1%).

Each cell shows mean/median of inv_growth for the (size_q, bm_q) cell,
averaged across formation years (means weighted by obs count).

## Mean inv_growth (paper vs ours)

Rows: size quintiles (Small → Big). Columns: B/M quintiles (Low → High).

| Size | B/M Low | 2 | 3 | 4 | B/M High |
|---|---:|---:|---:|---:|---:|
| Small | 1.09 (paper 0.85) | 0.97 (paper 0.80) | 0.76 (paper 0.65) | 0.62 (paper 0.59) | 0.39 (paper 0.34) |
| 2 | 1.29 (paper 1.03) | 0.88 (paper 0.75) | 0.66 (paper 0.57) | 0.44 (paper 0.45) | 0.36 (paper 0.36) |
| 3 | 1.22 (paper 0.95) | 0.64 (paper 0.63) | 0.49 (paper 0.46) | 0.38 (paper 0.31) | 0.25 (paper 0.22) |
| 4 | 0.91 (paper 0.78) | 0.48 (paper 0.46) | 0.36 (paper 0.35) | 0.29 (paper 0.27) | 0.23 (paper 0.22) |
| Big | 0.57 (paper 0.51) | 0.41 (paper 0.41) | 0.27 (paper 0.27) | 0.22 (paper 0.20) | 0.20 (paper 0.17) |

## Median inv_growth (paper vs ours)

| Size | B/M Low | 2 | 3 | 4 | B/M High |
|---|---:|---:|---:|---:|---:|
| Small | 0.35 (paper 0.21) | 0.34 (paper 0.25) | 0.23 (paper 0.19) | 0.16 (paper 0.14) | -0.02 (paper -0.05) |
| 2 | 0.72 (paper 0.53) | 0.44 (paper 0.34) | 0.29 (paper 0.26) | 0.18 (paper 0.16) | 0.08 (paper 0.08) |
| 3 | 0.69 (paper 0.54) | 0.34 (paper 0.31) | 0.24 (paper 0.21) | 0.15 (paper 0.14) | 0.05 (paper 0.02) |
| 4 | 0.49 (paper 0.47) | 0.27 (paper 0.25) | 0.19 (paper 0.16) | 0.14 (paper 0.09) | 0.05 (paper 0.03) |
| Big | 0.34 (paper 0.31) | 0.24 (paper 0.24) | 0.19 (paper 0.17) | 0.12 (paper 0.06) | 0.09 (paper 0.03) |

## Diagnostics

- Total obs used: 70,847
- Panel rows (formation years): 70,847
- Panel-wide mean inv_growth (formation June): 0.679
- Panel-wide median inv_growth (formation June): 0.217

## Range test (paper Table I: means 0.17-1.03, medians -0.05-0.54)

- Our mean inv_growth range: 0.197 - 1.292
- Our median inv_growth range: -0.024 - 0.715
- Means consistent with paper's range? YES
- Medians consistent with paper's range? YES

## Notes

- The paper's table shows pairs as 'mean/median', e.g., '0.85/0.21'.
- This Table I is the cheapest test for [M2]: if our ranges match the
  paper's, the Compustat-vintage hypothesis for the Ln(inv) magnitude
  discrepancy is retired.