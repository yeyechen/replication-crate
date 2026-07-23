---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 1
requires_iteration: true
---

# Audit Report 1 — time_series_momentum

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** Substantively strong replication. Every computational claim I re-checked independently reproduces — the TSMOM engine rebuild matches the replicator's artifact series with max |Δ| = 0.0, an independent from-scratch rebuild of SP500 from raw daily settlements matches the panel exactly over 326 months, and Tables 3/4/5 recompute to the reported values. The paper's central claims (pervasive 12-month TSMOM, diversified factor with ~12% vol and Sharpe > 1, large factor-model alpha, continuation-then-decay horizon signature, TSMOM subsuming XSMOM, straddle-like payoffs) all replicate in shape, sign, and magnitude class. The PARTIAL verdict is driven by (a) a 25–45% cell FAIL rate concentrated in documented data-constraint areas (commodity roll-gap series, US-T-bill rf for non-US instruments, FX futures vs forwards), and (b) one actionable report-accuracy defect: REPORT.md §4 misquotes several Table 5C cells that are *correct* in `results/table_5.md` / `eval_t5.csv`. No methodology bugs found. No blockers.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | Engine verified exact end-to-end (signal, §2.4 EWMA σ with 1-month lag, §3.2 cohort aggregation, NW(h−1), Eq. 4/5 timing). Deviations A1 (US rf for all), A2 (passive-class proxies), A5 (unscaled bonds), A6 (FX futures) are all data-forced, documented, and justified; no bugs. |
| Headline matching | 4 | All central claims match shape/sign; factor vol 12.65% vs "~12%" and Sharpe 1.25 vs ">1" nearly exact; alpha 1.20%/mo (t 5.85) vs 1.58% (7.99) is −24%/−27%; UMD loading within 18%. |
| Data coverage | 4 | Strategy window exactly 1985–2009; 55/58 instruments (94.8%); same primary source (Datastream futures) + exact FF factors; documented substitutions (A2 proxies, A6 FX futures) and truncated per-instrument Table 1 windows (A3). |
| Concrete result matching | 3 | Committed Tier 1 = 180/420 (43%); rubric-strict Tier 1+2 = 229/420 (55%). T3 14/22 and T4 14/20 Tier 1; T2 Panel A 56/64 Tier 1. FAILs concentrate in documented-constraint cells. |
| Signal strength | 3 | Headline ratios \|ours/paper\|: mean 0.92, worst 0.73 (alpha t-stat); all within [0.5, 2.0] but two cells below 0.8. |
| Corollary | 3 | Horizon signature, smile/straddle (+0.0044 curvature; 2008Q4 TSMOM +10.2% vs S&P −23%), correlation structure, TSMOM-beats-passive, bond panel, XSMOM-ALL all replicate; commodity Panel B (33/64 FAIL), per-class XSMOM betas, and passive-FX correlations do not. |

**Overall: 3.50 / 5 → binary verdict REPLICATED** (mean ≥ 3.0, no dimension = 1).

## 2. Issues by severity

### Blockers (must fix)

None. Every computational artifact independently verifies; committed paper values verified against `inputs/content.md`; no methodology gap invalidates downstream metrics; sample coverage well above threshold.

### Major (should fix)

- [M1] REPORT.md §4 (Table 5C table) and §1 misstate several *correct* computed values — report prose contradicts the replicator's own artifacts.
  - File: `REPORT.md:161-171` (Table 5C block) and `REPORT.md:20-23` (§1 first bullet); ground truth in `results/eval_t5.csv`, `results/table_5.md`.
  - Evidence (auditor-recomputed from `data/panel.parquet` + `data/strategy_artifacts.parquet`, matching `eval_t5.csv` to 3 decimals):
    - XSMOM_ALL α: report "−0.03 (t −0.22)"; actual **−0.39% (t −2.28)** → the report's derived claim "insignificant alpha … replicated at Tier 1" is wrong; the alpha is marginally *significant* (|t| > 2) and negative. It is Tier 1 only under the committed 200% tolerance on a near-zero paper value.
    - XSMOM_COM α: report "−0.02"; actual **−0.82% (t −3.52)**; R²: report "20%"; actual **15.7%**.
    - XSMOM_FX α: report "+0.05"; actual **−0.37%**; R²: report "6%"; actual **2.9%**.
    - HML row: report "−0.13 (t −2.35) / +0.38 (t 2.02) / R² 2%"; actual **−0.14 (t −2.92) / +0.54 (t 2.88) / R² 2.8%** (matches `table_5.md`, not the report prose).
    - §1 first bullet quotes the factor as "+1.20%/month, 12.65% vol, Sharpe 1.25" — the raw factor mean is **+1.315%/month** (verified); +1.20% is the Table 3A regression intercept. Sharpe 1.25 requires the 1.315% mean, so the bullet is internally inconsistent.
  - Likely cause: transcription/rounding errors when hand-copying cells into REPORT.md prose (digit swaps: −0.39 → −0.03, −2.28 → −0.22, −0.82 → −0.02).
  - Specific fix: regenerate the §4 Table 5C table and the §1 factor bullet directly from `results/eval_t5.csv` and the diagnostics numbers (raw mean +1.315%/mo; intercept +1.20%/mo labeled as such); replace "insignificant alpha" with "small negative alpha (t −2.28), Tier 1 under the committed 200% near-zero tolerance". No re-estimation needed.

### Minor (cleanup)

- [m1] REPORT.md §2 / log describe "S_t: 27 (Jan 1985) → 36 → 51 → 54 (Dec 2009), avg 45.4" — these are *panel availability* counts. The actual factor cross-section (signal + σ available) is **25 / 32 / 49 / 53, mean 44.2** (auditor-recomputed). File: `REPORT.md:73`. Fix: label as availability, or report the factor cross-section.
- [m2] REPORT.md says Table 1 stats are computed "1985–2009" (`REPORT.md:68` preview; §4 "our 1985-2009 vs paper"); `evaluate.py` actually computes them over each instrument's full panel window (futures listing → 2009-12; e.g., SP500 from 1982-04, n=326; GOLD from 1979/1983, n=351). `table_1.md`'s header ("full sample, panel window") is correct; align the report prose.
- [m3] Smile narrative: REPORT.md says "SP500 futures −22% on the quarter" in 2008Q4; auditor recompute = **−23.0%** (`REPORT.md:190`). Rounding only.
- [m4] `data/cache_daily_futures.parquet` and `data/cache_rf_monthly.parquet` are raw ClickHouse pulls cached in `data/`; `prep_validation.py` flags this ("cache raw pulls elsewhere"). Move caches outside `data/` (or rename per layout policy).
- [m5] The report's "49 of 54 signal-bearing instruments" is consistent with the figure's "49/55" once SEKUSD (no 12-month signal in-window) is excluded — state this exclusion explicitly where the 49/54 first appears (`REPORT.md:37`).

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Horizon signature (continuation k≤12, decay k≥24) | ✓ | Panel A h=1 column by k: +3.6/+4.4/+3.0/+3.2/+5.3/+3.0/+1.8/+1.6 — reproduced; 56/64 cells Tier 1 (tally verified). |
| 2 | Headline magnitudes (factor vol/Sharpe, alpha, UMD, XSMOM) | ✓ | Sharpe 1.248, vol 12.65%, raw mean +1.315%/mo; α 1.198% (t 5.85) vs 1.58 (7.99) r=0.76; UMD β 0.229 vs 0.28 r=0.82; XSMOM_ALL β 0.716/R² 0.471 vs 0.66/0.44 r≈1.08. |
| 3 | Sample coverage ≥ 60% | ✓ | 55/58 instruments mapped (94.8%); factor cross-section mean 44.2/58 (76%); window exactly 1985-01→2009-12 (300 months). |
| 4 | Data-source choice justified | ✓ | Datastream futures = paper's own source; FF factors exact and verified decimal in this build (2008-10 mkt_rf = −0.1721 ✓ A7/W1). A2/A6 substitutions verified unavailable in catalog and documented. |
| 5 | prep_validation.py exit 0 | ✓ | Exit 0; 3 layout warnings (cached raw pulls in data/, missing audit — this file — and missing SUMMARY — written with this audit). |
| 6 | All committed tables have results files | ✓ | table_1..5.md + eval_t1..5.csv present; 420 committed cells all evaluated, 0 SKIP. |
| 7 | SUMMARY/results consistency | ✗ | `eval_t*.csv`/`table_*.md` mutually consistent and independently verified, but REPORT.md §4 Table 5C prose contradicts them [M1]. |
| 8 | No orphan folders | ✓ | Clean tree; `src/__pycache__` only. |
| 9 | Diagnoses paired with fix attempts | ✓ | GOLD/SILVER splices, NATGAS/HEATOIL/UNLEADED roll-quality switches — all with before/after extreme-day counts; selection by diagnostics, not by fit. |
| 10 | Tier 2 within 2× magnitude | ✗ | Committed Tier 2 = any sign match (looser than rubric's 2×). E.g., beta_hml_monthly −0.14 vs −0.01 (14×) counted Tier 2; XSMOM_EQ β 0.10 vs 0.39 (0.26×) also. Rubric-strict recount: T1 180 (43%) / T2 49 (12%) / FAIL 191 (45%). |
| 11 | Pipeline end-to-end (SP500 from raw daily cache) | ✓ | Independent rebuild: monthly excess returns and EWMA σ match panel over all 326 months, max |Δ| = 0.0; Jan-2000 return −5.9825% and σ 17.605% match the claimed hand-check; settlement 1401.0 on 2000-01-31 ✓. |
| 12 | Engine rebuild (TSMOM_ALL, §4.1 Eq. 5) | ✓ | Auditor's independent implementation matches `strategy_artifacts.parquet` TSMOM_ALL exactly (max |Δ| = 0.0, n=300). Diagnostics block verified: total 4046.6%, maxDD −20.6%, FF5 α 15.95%/yr (t 6.01, R² 0.049) against `ff.five_factor_monthly`. |
| 13 | Table 2 t-stats (16 cells, 4 panels) | ✓ | Independent 7-factor + NW(h−1) recomputation: max |Δ| = 0.17 (bond k1h1), median Δ ≈ 0.03. |
| 14 | Tables 3/4/5 recompute | ✓ | T3 monthly/quarterly match (±0.02 from 1-obs regression-window diff); T4 all 20 cells match to 3 decimals; T5 all 8 rows match to 3 decimals (incl. XSMOM construction per A11). |
| 15 | Committed paper values vs paper text | ✓ | Spot-checked T1 (9 instruments), T2 Panels A/B/D grids, T3A, T4, T5C against `inputs/content.md` — all committed values faithful to the OCR'd paper. |
| 16 | Committed tier tallies | ✓ | 180/136/104 (43/32/25%) verified cell-by-cell; per-table breakdown matches report exactly. |
| 17 | Look-ahead / timing conventions | ✓ | σ at month m = last EWMA day of m−1 (verified in panel rebuild); position sized at formation month; signal R(k) requires all k months; XSMOM skips most recent month (t−12..t−2). |

## 4. Issues the agent should have caught (didn't)

1. **The Table 5C transcription errors [M1]** — the agent validated its engine rigorously but hand-copied cell values into REPORT.md prose without cross-checking against its own `eval_t5.csv`. A self-review pass comparing every number in REPORT.md tables against the eval CSVs would have caught all five discrepancies (they are digit swaps, not judgment calls).
2. **The "insignificant alpha" characterization of XSMOM_ALL on TSMOM** — the actual t is −2.28, i.e., marginally significant and negative. The agent's narrative ("insignificant alpha … replicated at Tier 1") relied on the misquoted −0.03 (−0.22). The honest statement: the paper's −0.16% (−1.17) vs our −0.39% (−2.28) both small negatives; Tier 1 only under the 200% near-zero tolerance.
3. **S_t labeling [m1]** — the report presents panel availability (45.4/month) as the strategy cross-section; the factor averages 44.2 instruments/month (25 in Jan-1985, not 27). Trivial to compute correctly since the artifacts already contain it.
4. **Tier-2 leniency disclosure** — the committed Tier 2 = sign-match convention admits cells up to 14× off (HML monthly beta). The report's "every FAIL has a named cause" framing is honest, but it never flags that its Tier 2 bucket is far looser than the standard 2× definition, which flatters the 75% Tier-1+2 figure (rubric-strict T1+2 is 55%).

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Time Series Momentum" (Moskowitz, Ooi & Pedersen 2012) for slug `time_series_momentum`. The previous agent run completed with verdict **PARTIAL** (audit 1 at `replications/time_series_momentum/logs/audit1.md`). Read the audit first.

**Context:** the auditor independently verified the entire computational chain — the TSMOM engine, the panel pipeline (SP500 rebuilt from raw daily data matches to 1e-15), Tables 1–5 values, the diagnostics block, and the tier tallies all reproduce. No re-estimation is required. This is a **report-accuracy and cleanup iteration**: the remaining defects are in `REPORT.md` prose, which contradicts the (correct) artifacts.

## Issues to address (priority order)

### [M1] — MAJOR — fix first
REPORT.md §4 (Table 5C block, lines ~161–171) and §1 (first bullet, lines ~20–23) misquote cells that are correct in `results/eval_t5.csv` / `results/table_5.md`.

**Specific fix:**
1. Replace the §4 Table 5C markdown table with values regenerated from `results/eval_t5.csv` (XSMOM_ALL α −0.39% (t −2.28), XSMOM_COM α −0.82% (t −3.52) R² 15.7%, XSMOM_FX α −0.37% R² 2.9%, HML −0.14 (t −2.92) / +0.54 (t 2.88) / R² 2.8% — same values as `table_5.md`).
2. Delete the "insignificant alpha" claim for XSMOM_ALL; state: small negative alpha −0.39% (t −2.28) vs paper −0.16% (−1.17); Tier 1 only under the committed 200% near-zero tolerance; the replicated claim is β ≈ 0.72 (paper 0.66) and R² ≈ 47% (paper 44%).
3. Fix the §1 first bullet: raw diversified-factor mean is +1.315%/month (Sharpe 1.25 = 1.315×√12/12.65); +1.20%/month is the Table 3A regression intercept — label them distinctly.
4. Verification: `grep` every number in REPORT.md tables 3/5 against `results/eval_t3.csv` and `results/eval_t5.csv`; every figure must match to the displayed precision.

### [m1] — MINOR — cleanup
`REPORT.md:73` and `logs/log1.md` quote S_t = 27/36/51/54 (mean 45.4) — that is panel *availability*. The factor cross-section (signal + σ present) is 25/32/49/53 (mean 44.2). Label accordingly.

### [m2] — MINOR — cleanup
REPORT.md §2/§4 describe Table 1 stats as "our 1985–2009"; `evaluate.py` computes them over each instrument's full panel window (futures listing → 2009-12; SP500 from 1982-04, n=326). Align prose with `table_1.md`'s "full sample, panel window" header.

### [m3] — MINOR — cleanup
2008Q4 S&P 500 futures quarterly return is −23.0%, not −22% (`REPORT.md:190`).

### [m4] — MINOR — cleanup
Move `data/cache_daily_futures.parquet` and `data/cache_rf_monthly.parquet` out of `data/` (raw ClickHouse pulls; `prep_validation.py` flags them). Update the cache paths in `src/main.py` accordingly and re-run `python3 scripts/prep_validation.py time_series_momentum` — expect 0 layout errors after this and after audit1.md/SUMMARY.md exist.

### [m5] — MINOR — cleanup
State the SEKUSD exclusion where "49 of 54 signal-bearing instruments" first appears (55 instruments mapped; SEKUSD has no 12-month signal in-window → 54 signal-bearing).

## Iteration discipline reminders

- **No re-estimation.** Do not rebuild the panel or re-run `evaluate.py` / `eval_tables345.py` — the auditor verified them exactly. If you touch code for [m4], re-run the affected script and confirm `eval_t*.csv` are byte-identical (same values) afterward.
- Every assumption change goes in `preparations/assumptions.md` with Diagnosis / Next fix / Before / After / Status — here, none are expected; this is a documentation pass.
- After fixes, update REPORT.md's header (outer iteration 2) and append the iteration to `logs/log2.md`.
- Do not create or modify SCORE.md. The auditor re-scores into SUMMARY.md.

--- END COPY HERE ---
