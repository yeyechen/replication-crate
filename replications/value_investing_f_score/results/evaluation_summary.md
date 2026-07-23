# Evaluation Summary — Consolidated Tier Tally

Per-table contract-target tallies re-read from the Tally block of each results file (Tables 1–5, Appendix A, Table 7). Tier definitions per `rep/TOLERANCE_RULES.md` (Tier 1 = within contract tolerance; Tier 2 = same sign / A1-gap pattern; FAIL = sign flip; SKIP = pre-restriction cell under assumptions.md A1, or an infeasible corollary). Sample restricted to formation years 1988–1996 (A1: `oancf` NULL for FY<1987 in the `comp_202601` vintage); full-sample paper values are Tier-2 references by construction.

**Contract metrics: 162 = 138 (tables 1–4, 7, appendix_a) + 24 (table_5, added this iteration).** Of these, **154 are evaluated** (Tier 1 + Tier 2 + FAIL) and **8 are SKIP** — 3 pre-1988 Appendix-A cells under A1 and 5 Table-5 Panel-C analyst cells (M2: I/B/E/S coverage below the 60%-classifiable threshold, documented in results/table_5_analyst.md). 154 evaluated + 8 SKIP = 162 contract metrics. [m2] The per-file 'Evaluated' column sums to 155 (one more) because appendix_a.md ALSO tallies the 1 task-text extra cell `n_1996` (flagged †), which is outside the JSON contract and not part of the 162.

| Table | Tier1 | Tier2 | FAIL | SKIP | Evaluated | notes |
|---|---:|---:|---:|---:|---:|---|
| Table 1 | 23 | 7 | 1 | 0 | 31 | financial/return characteristics; 1 FAIL = ΔTURN mean (tiny-mean sign flip) |
| Table 2 | 10 | 2 | 1 | 0 | 13 | Spearman correlations; 1 FAIL = OCR row-attribution artifact (ρ ΔLIQUID×ACCRUAL) |
| Table 3 | 16 | 32 | 3 | 0 | 51 | F-score group returns; 3 FAILs = score-3 mean + Panel D RANK_SCORE spread/t |
| Table 4 | 4 | 10 | 4 | 0 | 18 | size partitions; 4 FAILs = near-zero/tiny-n group means (strategy spreads keep sign) |
| Table 5 | 12 | 5 | 2 | 5 | 19 | price/volume partitions (added iter-2, M1); +5 SKIP Panel C analyst cells (M2: IBES coverage < 60%) |
| Appendix A | 6 | 2 | 1 | 3 | 9 | annual strong−weak hedge; 1 FAIL = avg weak return (≈0 in both samples); +3 SKIP pre-1988 cells |
| Table 7 | 6 | 8 | 0 | 0 | 14 | cross-sectional regressions; no FAILs — F_SCORE coefs Tier 1, pooled t-stats Tier 2 (A1 sample) |
| **Total** | **77** | **66** | **12** | **8** | **155** | 154 contract cells evaluated (+1 n_1996 extra) + 8 SKIP = 162 contract metrics |

¹ **[m1] Tier-2 convention.** A1-structural cells — the full-sample counts (~0.41× the paper, since our 5,736 obs are 41% of 14,043) and the attenuated full-period spreads — are Tier-2-by-construction under `rep/TOLERANCE_RULES.md` (Tier 2 = sign matches, no magnitude cap). Applied strictly, roughly 20–25 of these cells would exceed the audit's 2× pattern-match spot-check bound (e.g. Table 3 Panel B score-0 mean −0.236 vs −0.061 = 3.87×; most count cells ≈ 0.4×); reclassifying them would raise FAIL from 10 toward ~30+ **without changing any Tier-1 count (Tier 1 = 77, unaffected)**. The labels below follow the repo definition consistently with each cell's `tolerance_pct`; no reclassification is performed.
