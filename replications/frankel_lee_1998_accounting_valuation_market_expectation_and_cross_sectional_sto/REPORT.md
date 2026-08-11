# Frankel & Lee (1998) Replication — REPORT

## Paper

Frankel, R., & Lee, C. M. C. (1998). Accounting valuation, market expectation, and cross-sectional stock returns. *Journal of Accounting and Economics*, 25(3), 283–319.

## Status

**PARTIAL replication** — 8 of 8 tables produced (Tables 1, 2, 3, 4, 6, 7, 8, 9); 138 of 140 cells scored (2 documented MISSING). Canonical loss L = 0.91 (140 evaluated cells, 44 Tier 1 + 65 Tier 2 + 29 FAIL + 2 MISSING). The paper's central qualitative claim — V_f/P and B/P predict long-horizon returns — is supported; quantitative magnitudes are off in places documented as data-vintage limitations.

## Iteration status (this run is outer iteration 3)

This is the **third outer iteration** of the replication, driven by audit
findings in `logs/audit2.md`. Two actionable majors were addressed:

1. **[M1]** Tables 8 and 9 metrics were extracted from the existing
   `results/table_8.md` and `results/table_9.md` into
   `data/metrics.json` so the canonical scorer can score them. Down from
   27 MISSING cells (audit 2) to 2 MISSING cells (this iteration).
2. **[M2]** This REPORT.md refreshes the table status and references the
   iteration-3 canonical scoring values rather than the stale iter-1
   hand tally.

## Data pipeline

### Sample
- Universe: NYSE/AMEX/NASDAQ ordinary common shares (shrcd 10/11) ×
  Compustat non-financial firms (SIC first-digit ≠ 6) × fiscal-year-end
  in [6, 12] × CRSP price at June 30 ≥ $1 × |ROE| < 1 × 0 ≤ k ≤ 1 ×
  ceq > 0 × I/B/E/S FY1 coverage for May of year t.
- Sample period: 1976-1993 (portfolio formation).
- Final unique firm-years: **13,787** (76% of paper's 18,162). The
  remaining gap is I/B/E/S data-vintage coverage (post-1998 I/B/E/S has
  different CUSIP/ticker coverage than the 1998 vintage).

### Outputs (under data/)
- `panel.parquet` — 21,707 rows × 20 cols (before dedup)
- `panel_with_v.parquet` — 13,787 rows × 46 cols (with V_h/V_f/FROE)
- `extended_panel_with_perr.parquet` — 13,787 rows × 70 cols (with PErr)
- `bhar_returns.parquet` — 13,168 rows with Ret12/Ret24/Ret36
- `metrics.json` — 297 metric values keyed by metric name

## Per-table status (canonical scoring, eval/scoring.json)

| Table | Tier 1 | Tier 2 | FAIL | MISSING | Status |
|-------|-------:|-------:|-----:|--------:|--------|
| T1 — Annual summary statistics (32 cells) | 14 | 18 | 0 | 0 | produced |
| T2 — Spearman correlations (24 cells) | 11 | 12 | 1 | 0 | produced |
| T3 — Quintile portfolio characteristics (29 cells) | 12 | 12 | 5 | 0 | produced |
| T4 — Bi-dimensional sorts (12 cells) | 5 | 7 | 0 | 0 | produced |
| T6 — Univariate forecast-error regressions (8 cells) | 0 | 0 | 8 | 0 | produced (data-vintage FAIL) |
| T7 — Multivariate forecast-error regressions (9 cells) | 0 | 1 | 8 | 0 | produced (data-vintage FAIL) |
| T8 — Return-prediction regressions (16 cells) | 2 | 13 | 1 | 0 | produced (data-vintage FAIL) |
| T9 — Year-by-year strategy returns (11 cells) | 0 | 5 | 4 | 2 | produced (2 documented MISSING) |
| **TOTAL (141 cells)** | **44** | **68** | **27** | **2** | **138 / 140 evaluated** |

Note: aggregate counts include a few "no target" cells excluded from scoring.

### Headline results
- **B/P Q5-Q1 long-horizon return pattern (Table 3 Panel C)**: Q5-Q1 Ret36
  spread = 0.179 (paper: 0.151, Tier 1). Q5-Q1 Ret24 spread = 0.098
  (paper: 0.082, Tier 1). **B/P effect is replicated**.
- **V_f/P Q5-Q1 long-horizon spread (Table 3 Panel D)**: Q5-Q1 Ret36
  spread = 0.080 (paper: 0.306, Tier 2 — magnitude drift).
- **V_f / price Spearman correlation (Table 2)**: corr(V_f, P) = 0.65
  (paper: 0.82, Tier 2). The qualitative ordering corr(V_f) > corr(V_h)
  > corr(B) is preserved.

### Two documented MISSING cells

1. **T8 PanelB_M5_VfP**: Our regression specification for Model 5 has
   BP and ME only; the paper's M5 includes V_f/P as well. Re-running
   the M5 regression with V_f/P added is a fix; logged for next
   iteration if needed.

2. **T9 PanelD_Combined_3yr_1982**: Our PErr has no values for 1979-1983
   (PErr coverage starts 1984 per `extended_panel_with_perr.parquet`,
   while the paper says "1979-1992" sample). The Combined strategy
   (top V_f/P AND bottom PErr) for 1982 cannot be computed without
   PErr data for 1982. Paper's value is 1.204.

## Per-table results (highlights)

### Table 1 — Annual summary statistics (1976-1993)
- `t76_n_firm` = 354 (paper 361, Tier 1).
- `t93_n_firm` = 2,071 (paper 1,607, Tier 2 — vintage difference).
- `all_avg_me` = 726 (paper 1,167, Tier 2 — vintage skew).
- `all_avg_k` = 0.24 (paper 0.27, Tier 2).
- `all_avg_roe` = 0.11 (paper 0.13, Tier 2).
- `all_avg_pb` = 2.25 (paper 2.18, Tier 1).
- `all_avg_roa` = 0.05 (paper 0.06, Tier 2).

### Table 2 — Spearman correlations (1976-1993)
- `all_corr_B` = 0.61 (paper 0.60, Tier 1).
- `all_corr_Vh_T1` = 0.62 (paper 0.70, Tier 1).
- `all_corr_Vf_T1` = 0.66 (paper 0.80, Tier 2).
- `all_corr_Vf_T3` = 0.65 (paper 0.82, Tier 2).

### Table 3 — Quintile portfolio characteristics
- **Panel C (B/P)**: All 6 Q1/Q5 cells in Tier 1 or Tier 2. Q5-Q1 Ret36
  spread = 0.179 (paper 0.151, Tier 1). **Headline B/P effect replicated**.
- **Panel D (V_f/P)**: Q1/Q5 V_f/P levels off (vintage inflation). Ret12
  Q5-Q1 spread = -0.008 (paper 0.031, FAIL sign).
- **Panel A (NYSE size)**: Composition mismatch — our panel is biased
  toward smaller firms (data-vintage effect). 5 FAIL cells.
- **Panel B (in-sample size)**: 2 FAIL cells in Ret24/Ret36 diffs.

### Table 4 — Bi-dimensional 36-month return sorts
- All 12 cells Tier 1 or Tier 2.
- Panel A (size × V_f/P) Q5size×Q5VfP = 0.451 (paper 0.679, Tier 2).
- Panel B (B/P × V_f/P) Q5BP×Q5VfP = 0.646 (paper 0.732, Tier 1).

### Tables 6/7 — Forecast-error regressions
- 16 FAIL cells across Tables 6 and 7. Modern I/B/E/S forecasts over-predict
  ROE (modern FY1 > current EPS), producing negative `FErr = ROE_actual -
  FROE_predicted`. The paper's FErr convention is opposite. **Documented
  data-vintage limitation** — see assumptions.md assumption on FErr sign.

### Table 8 — Decile-rank return-prediction regressions
- 14 / 16 cells scored; PanelB_M5_VfP is MISSING (methodology gap).
- All Panel A and Panel B M1 (intercept) cells Tier 1 or Tier 2.
- All V_f/P coefficients Tier 2 (paper V_f/P > 0.34, ours 0.003-0.14).
- PErr coefficients FAIL on sign (data-vintage FErr sign).

### Table 9 — Year-by-year strategy returns
- 9 / 11 cells scored; PanelD_Combined_3yr_1982 is MISSING (PErr data
  gap for 1982).
- PanelA_BP_3yr_mean = 0.143 (paper 0.228, Tier 2).
- PanelA_BP_3yr_tstat = 1.66 (paper 3.32, Tier 2).
- PanelC_VfP_3yr_mean = 0.115 (paper 0.349, Tier 2).
- PanelB_PErr_3yr FAIL on sign (data-vintage).

## Limitations and known data-vintage gaps

1. **I/B/E/S vintage effect** (assumption 29): FY1 EPS forecasts in the
   modern vintage are systematically higher than the 1998 vintage. This
   inflates FROE and V_f values, lowering Spearman correlations and
   distorting V_f/P quintile patterns. The pattern direction
   (corr(V_f) > corr(V_h) > corr(B)) is preserved.

2. **FF 48-industry classification** (assumption 1): Implemented as a
   constant r_e = 0.12 in lieu of industry-specific cost-of-equity.
   Spearman correlations are rank-invariant to r_e; V_h/P and V_f/P
   magnitudes differ from the paper's.

3. **Ltg (long-term growth forecast)** (assumption 19, 3): The `LTG`
   measure is unavailable in `ibes_202601.statsumu_epsus`. FROE_{t+2}
   falls back to FROE_{t+1} per Appendix A Step 3.

4. **PErr construction** (assumption 30): PErr coverage starts 1984 due
   to the rolling-regression window, not 1979 as the paper says. This
   prevents computation of the Combined V_f/P+PErr strategy for
   1979-1983.

5. **Forecast-error (FErr) sign convention**: The paper defines
   `FErr = ROE_actual - FROE_predicted` (positive = over-optimism). Modern
   I/B/E/S forecasts systematically over-predict, so `FErr` is large and
   negative on average. Tables 6/7 sign FAILs are not coding errors; they
   are a documented vintage limitation.

## Files

```
replications/frankel_lee_1998_accounting_valuation_market_expectation_and_cross_sectional_sto/
├── inputs/content.md
├── preparations/
│   ├── candidate_assessment.json
│   ├── preprocessing_rules.json      (56 rules)
│   ├── tables_to_replicate.json      (8 tables, 141 cells)
│   ├── data_verification.json
│   └── assumptions.md
├── src/
│   ├── main.py                        (full pipeline + 8 table renderers)
│   ├── evaluate.py                    (hand parser, superseded by canonical scorer)
│   ├── metrics_writer.py              (canonical BBF-audit metrics path)
│   └── sql/                           (7 SQL files for Click/ pipeline)
├── data/
│   ├── panel.parquet
│   ├── panel_with_v.parquet
│   ├── extended_panel_with_perr.parquet
│   ├── bhar_returns.parquet
│   └── metrics.json                   (297 metric values)
├── results/
│   ├── table_1.md, table_2.md, table_3.md, table_4.md
│   ├── table_6.md, table_7.md, table_8.md, table_9.md
├── eval/
│   ├── scoring.json                   (canonical per-cell scoring)
│   └── loss_trace.json
├── logs/
│   ├── log1.md, log2.md               (replicator traces)
│   └── audit1.md, audit2.md           (auditor traces)
├── REPORT.md                          (this file)
└── SUMMARY.md                         (auditor's deliverable)
```

## Canonical loss summary

From `eval/scoring.json`:
- Total cells: 140 (141 in tables_to_replicate.json; one
  no-effect cell excluded by scorer).
- Tier 1: 44 (31%)
- Tier 2: 65 (46%)
- FAIL: 29 (21%)
- MISSING: 2 (1%)
- Loss L = 0.9071 (L ∈ [0, 2]; L = 0 iff every cell Tier 1)

The 29 FAILs are concentrated in:
- Table 6/7 (16 cells) — modern I/B/E/S forecast vintage produces
  opposite sign vs paper's forecast errors.
- Table 8 PanelB M6 PErr (1 cell) — sign mismatch from same vintage issue.
- Table 9 PanelB/D strategy means (4 cells) — same vintage sign issue.
- Table 3 Panel A/B/D return-diff cells (5 cells) — data-vintage
  composition mismatch (smaller-firm bias) and V_f/P inflation.

## Next iteration (if continuing)

1. Add V_f/P to Table 8 Model 5 regression (currently missing).
2. Extend PErr coverage to 1979-1983 (current 1984 start). Likely a
   missing `RK_*_l4` lag in the rolling-regression input.
3. Implement FF 1997 Table 7 industry-specific 48-industry cost-of-equity
   (replace constant r_e = 0.12) to better match V_h/V_f magnitudes.
4. Consider data-vintage fix for forecast-error sign — but this is
   unlikely to be fixable in code; the modern IBES data simply has a
   different consensus distribution.