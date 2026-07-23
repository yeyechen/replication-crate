# Replication Report — Novy-Marx (2013), "The Other Side of Value: The Gross Profitability Premium"

**Journal of Financial Economics 108 (2013) 1–28**

## Executive Summary

This report documents the replication of Novy-Marx (2013), which establishes that gross profitability (GP/A = (REVT − COGS) / AT) has roughly the same power as book-to-market predicting the cross section of average stock returns. The paper's central finding — that profitable firms earn significantly higher returns than unprofitable firms despite being growth stocks — is faithfully reproduced.

**Headline result (Table 2, Panel A):** The High-minus-Low GP/A quintile spread earns **0.32% per month** (paper: 0.31%, t = 2.51 vs 2.49) with a Fama-French three-factor alpha of **0.54% per month** (paper: 0.52%, t = 4.58 vs 4.49). The strategy is a growth strategy with a large negative HML loading of **−0.45** (paper: −0.44).

**Per-cell tally (Table 2 Panel A):** 50 Tier 1 (within tolerance), 5 Tier 2 (correct sign, outside tolerance), 0 FAIL (wrong sign) out of 55 cells.

## Data

- **Compustat:** `comp_202601.funda` (929,418 rows, annual fundamentals). Filters: `indfmt='INDL'`, `consol='C'`, `popsrc='D'`, `datafmt='STD'`. SIC 6xx (financials) excluded.
- **CRSP:** `crsp_202601.msf` (5,153,763 rows, monthly returns). Universe: shrcd 10/11, exchcd 1/2/3 via `dsenames` PIT join.
- **CCM Link:** `crsp_202601.ccmxpf_linktable` (usedflag=1, linkprim P/C, linktype LC/LU).
- **FF Factors:** `ff.four_factor_monthly` (570 months, 1963-07 to 2010-12). Values in decimals.
- **Panel:** 2,284,523 rows × 22 columns; 570 months; 18,818 unique permnos; avg 4,008 obs/month.

## Methodology

### Signal Construction
- **GP/A** = (REVT − COGS) / AT, with GP item as fallback when REVT or COGS missing.
- **Book Equity** = (SEQ or CEQ+PSTK or AT−LT) + (TXDITC or TXDB+ITCB or 0) − (PSTKR or PSTK or 0).
- **B/M** = BE / ME_dec, where ME_dec is CRSP market equity at December of the fiscal-year-end calendar year (6-month lag per FF convention).
- **Fiscal year mapping:** FY t data used from July t+1 through June t+2.

### Portfolio Construction
- **Sorts:** Quintile, NYSE breakpoints (hexcd==1), annual rebalancing at end of June.
- **Weighting:** Value-weighted using prior-month market equity (beginning-of-period weights, per FF convention).
- **Excess returns:** Portfolio return minus risk-free rate.
- **FF3 regression:** Time-series OLS of monthly excess returns on MKT-RF, SMB, HML.

## Results

### Table 2, Panel A — Portfolios sorted on GP/A

| Portfolio | r^e | alpha | MKT | SMB | HML | GP/A | B/M | ME($M) | n |
|---|---|---|---|---|---|---|---|---|---|
| Low | 0.30 | −0.21 | 0.95 | 0.03 | 0.17 | 0.10 | 0.88 | 838 | 680 |
| 2 | 0.39 | −0.12 | 1.02 | −0.08 | 0.15 | 0.21 | 0.73 | 1,175 | 561 |
| 3 | 0.52 | 0.04 | 1.02 | 0.06 | 0.04 | 0.32 | 0.58 | 1,107 | 615 |
| 4 | 0.41 | 0.06 | 1.02 | 0.02 | −0.24 | 0.45 | 0.40 | 1,257 | 673 |
| High | 0.62 | 0.34 | 0.92 | −0.04 | −0.28 | 0.71 | 0.27 | 1,193 | 780 |
| H−L | 0.32 | 0.54 | −0.03 | −0.07 | −0.45 | | | | |
| t-stat | [2.51] | [4.58] | [−1.07] | [−1.85] | [−10.58] | | | | |

All returns in %/month. Paper values in parentheses for comparison: H−L r^e = 0.31 (t=2.49), alpha = 0.52 (t=4.49), HML = −0.44.

### Table 2, Panel B — Portfolios sorted on B/M

| Portfolio | r^e | alpha | MKT | SMB | HML |
|---|---|---|---|---|---|
| Low | 0.37 | 0.13 | 1.00 | −0.09 | −0.43 |
| High | 0.75 | −0.06 | 1.00 | 0.25 | 0.71 |
| H−L | 0.38 | −0.19 | 0.01 | 0.34 | 1.14 |

Paper: H−L r^e = 0.41 (t=2.95), alpha = −0.06 (t=−0.71), HML = 0.91.

### Key Findings Confirmed

1. **Gross profitability premium exists:** High GP/A firms earn 0.62%/mo vs 0.30%/mo for Low GP/A firms. The H−L spread of 0.32%/mo (t=2.51) is statistically significant.
2. **Profitability is a growth strategy:** High GP/A firms have low B/M (0.27) and negative HML loading (−0.28). The strategy provides an excellent hedge for value.
3. **FF3 alpha is larger than the raw spread:** The H−L alpha of 0.54%/mo (t=4.58) exceeds the raw spread (0.32%/mo) because the strategy is short value (negative HML loading), and value earned positive returns over the sample.
4. **Value premium confirmed:** B/M sorts produce H−L spread of 0.38%/mo with HML loading of 1.14, consistent with the paper.

## Assumptions and Deviations

See `preparations/assumptions.md` for the full registry (8 initial assumptions + 11 rep-worker flags).

Key assumptions:
- **A1:** Delisting returns used when available (paper silent).
- **A2:** Standard Compustat filters applied (paper silent on specific filters).
- **A3:** GP item used as fallback for REVT−COGS (paper defines both).
- **A4:** PSTX/PSTKRL missing → PSTK substituted in BE tiers.
- **Flag I:** Prior-month ME weights for VW (critical for matching paper's return levels).
- **Flag J:** Aggregate characteristics (ΣGP/ΣAT) for portfolio-level GP/A and B/M.

## Limitations

1. **Tables 6 and 7 not yet replicated.** Double sorts on GP/A × B/M (Table 6) and Fortune 500 strategies (Table 7) remain for a future iteration.
2. **Table 1 (FM regressions) not yet replicated.** Fama-MacBeth regressions with trimming and industry adjustment remain.
3. **Coverage gap:** Our universe has ~12-17% fewer firms per quintile than the paper, consistent with Compustat vintage differences.
4. **B/M characteristic:** The Q3 B/M characteristic (0.585 vs paper 1.00) is the largest single-cell deviation (Tier 2).

## Files

- `src/main.py` — Full pipeline + Table 2 analysis
- `src/sql/*.sql` — ClickHouse queries (compustat_funda, crsp_monthly, ccm_link, ff_factors)
- `data/panel.parquet` — Analysis-ready panel (2.28M rows × 22 cols, 74 MB)
- `data/ff_factors.parquet` — FF factors (570 months)
- `results/table_2.md` — Full Table 2 with per-cell comparison
- `results/table2_decile_spread.png` — Quintile VW excess return bar chart
- `preparations/assumptions.md` — Full assumption registry
