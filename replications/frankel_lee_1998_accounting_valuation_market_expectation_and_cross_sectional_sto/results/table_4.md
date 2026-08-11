# Table 4 -- Bi-Dimensional Quintile 36-Month Buy-and-Hold Returns

**Replication of**: Frankel & Lee (1998) -- Table 4

**Sample period**: 1977-1992 (paper's Table 4 caption)
**Universe**: same as Table 3 (Compustat non-financial, fiscal year-end in [6,12], June price >= $1, I/B/E/S FY1 coverage)

Each firm-year is independently assigned to a quintile by V_f/P (rows) and by ME or B/P (columns) within each portfolio-formation year. Cells show the equally-weighted mean of 36-month buy-and-hold returns (Ret36) starting July of year t. The marginal rows/columns show the Q5-Q1 spread holding the other dimension fixed.

**Marginal Q5-Q1 interpretation**:
- The rightmost-column marginal (per row) shows the average Ret36 spread from V_f/P Q5 minus V_f/P Q1, holding the row's ME (Panel A) or B/P (Panel B) quintile fixed -- i.e., the **V_f/P effect controlling for ME/BP**.
- The bottom-row marginal (per column) shows the average Ret36 spread from ME/BP Q5 minus ME/BP Q1, holding the column's V_f/P quintile fixed -- i.e., the **ME/BP effect controlling for V_f/P**.

**Number of years averaged**: Panel A = 16, Panel B = 16.

## Panel A -- V_f/P x ME (in-sample size quintiles)

Years averaged: 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992

|  | ME Q1 | ME Q2 | ME Q3 | ME Q4 | ME Q5 | Marginal Q5-Q1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| V_f/P Q1 | 0.528 | 0.464 | 0.375 | 0.350 | 0.394 | -0.134 |
| V_f/P Q2 | 0.477 | 0.477 | 0.451 | 0.477 | 0.458 | -0.019 |
| V_f/P Q3 | 0.630 | 0.514 | 0.539 | 0.490 | 0.512 | -0.117 |
| V_f/P Q4 | 0.421 | 0.483 | 0.485 | 0.574 | 0.506 | +0.085 |
| V_f/P Q5 | 0.664 | 0.402 | 0.501 | 0.491 | 0.451 | -0.214 |
| **Marginal ME (Q5-Q1)** | **+0.136** | **-0.062** | **+0.127** | **+0.141** | **+0.057** | -- |

## Panel B -- V_f/P x B/P

Years averaged: 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992

|  | B/P Q1 | B/P Q2 | B/P Q3 | B/P Q4 | B/P Q5 | Marginal Q5-Q1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| V_f/P Q1 | 0.291 | 0.375 | 0.518 | 0.640 | 0.536 | +0.245 |
| V_f/P Q2 | 0.444 | 0.478 | 0.495 | 0.443 | 0.507 | +0.063 |
| V_f/P Q3 | 0.511 | 0.539 | 0.520 | 0.519 | 0.577 | +0.066 |
| V_f/P Q4 | 0.316 | 0.491 | 0.512 | 0.506 | 0.545 | +0.229 |
| V_f/P Q5 | 0.480 | 0.419 | 0.438 | 0.611 | 0.646 | +0.166 |
| **Marginal B/P (Q5-Q1)** | **+0.189** | **+0.044** | **-0.080** | **-0.030** | **+0.110** | -- |

## Per-cell comparison vs paper (committed cells)

Paper's Panel A Q1size_Q1VfP, Q1size_Q5VfP, Q1size_Q5Q1 correspond to ME=Q1 row, V_f/P=Q1 / V_f/P=Q5 / Q5-Q1 columns. The Q5size row is ME=Q5.
Paper's Panel B Q1BP / Q5BP rows correspond to B/P=Q1 / B/P=Q5 rows.

| Panel | Cell | Paper | Ours | Status |
| --- | --- | ---: | ---: | --- |
| A | A_Q1size_Q1VfP_Ret36 | +0.319 | +0.528 | FAIL (Δ=+0.209) |
| A | A_Q1size_Q5VfP_Ret36 | +0.590 | +0.664 | Tier 1 (Δ=+0.074) |
| A | A_Q1size_Q5Q1_Ret36 | +0.271 | +0.136 | Tier 2 (Δ=-0.135) |
| A | A_Q5size_Q1VfP_Ret36 | +0.350 | +0.394 | Tier 1 (Δ=+0.044) |
| A | A_Q5size_Q5VfP_Ret36 | +0.679 | +0.451 | Tier 2 (Δ=-0.228) |
| A | A_Q5size_Q5Q1_Ret36 | +0.329 | +0.057 | FAIL (Δ=-0.272) |
| B | B_Q1BP_Q1VfP_Ret36 | +0.316 | +0.291 | Tier 1 (Δ=-0.025) |
| B | B_Q1BP_Q5VfP_Ret36 | +0.634 | +0.480 | Tier 1 (Δ=-0.154) |
| B | B_Q1BP_Q5Q1_Ret36 | +0.318 | +0.189 | Tier 2 (Δ=-0.129) |
| B | B_Q5BP_Q1VfP_Ret36 | +0.263 | +0.536 | FAIL (Δ=+0.273) |
| B | B_Q5BP_Q5VfP_Ret36 | +0.732 | +0.646 | Tier 1 (Δ=-0.086) |
| B | B_Q5BP_Q5Q1_Ret36 | +0.469 | +0.110 | FAIL (Δ=-0.359) |

## Notes

**Aggregation**: each cell is the simple mean (across years) of the annual cell mean. We do not weight by cell-N to avoid over-weighting years with sparse coverage; the paper's exact aggregation is not documented but is consistent with simple means. Sign-conventions are preserved: Q5 > Q1 rows indicate positive V_f/P effect.

**V_f/P effect**: row marginal (right column) is the Q5-Q1 spread of V_f/P holding the column dimension (ME or B/P) fixed. The paper expects this spread to be positive in every row of both panels (i.e., high V_f/P firms earn higher 36-month returns even within size or B/P quintiles).
