---
iteration: 1
slug: earnings_releases_anomalies
inner_iterations: 3
worker_spawns: 3
---

# Outer Iteration 1 — Reasoning Trace

Paper: Foster, Olsen & Shevlin (1984), "Earnings Releases, Anomalies, and the
Behavior of Security Returns", The Accounting Review LIX(4), 574-603.

Selected tables: T1 (FEP transition frequencies), T3 (NYSE size deciles
1973-1981), T4 (pooled CARs, the headline table), T6 (size-quintile CARs,
Model 2/4), T7 (eq. 16 cross-sectional regressions — the 81%/66%/85%
headline). 798 per-cell targets total.

## Global-check plan (before any per-cell drilling)

1. Sample period: events 1974Q1-1981Q4 (32 quarters), earnings file from 1970Q2.
2. Universe size: paper 2,053 firms; 1,495-1,978 obs/quarter (our vintage will
   differ — A4 documents why; Tier 2 for counts).
3. Preprocessing: all 41 rules from preprocessing_rules.json wired in
   (10-consecutive screen, announcement dates, FE models 1-4, prior-quarter
   cutoffs, size-decile benchmark u = R_i − R_p, eq. 18 aggregation).
4. Weighting/aggregation: equal-weighted portfolios; CAR = mean over obs of
   sum of daily u; units = percent.

## Pre-spec sanity checks (replicator, before worker spawn)

- ClickHouse reachable; dsf Jan-1974 = 121,031 rows.
- fundq: consol='C' (NOT 'CSTD' — first query returned 0 rows until fixed),
  dates ISO strings, (gvkey,fyearq,fqtr) unique (160,360 keys, no restatement
  dups), rdq coverage 87-90% for FY1974-1981, NULL pre-1971.
- Units verified: epspxq in $/share, ibq in $M (3.675/0.95 = 3.87M shares ≈
  CRSP shrout 3,798 thousand for permno 12087, 1974-12-31); dsf ret decimal,
  shrout thousands, prc signed.
- ccmxpf_lnkhist uses lpermno (not permno); linkprim/linktype/liid present.
- dsi.ewretd = EW NYSE+AMEX daily return (for Table 3 betas, A13).

## Inner iteration 1: Build the data pipeline

**Task spec → rep-worker:**

Build the event-study data pipeline producing: (1) observation-level panel
(gvkey, permno, fiscal quarter, rdq, day0, Q, fe1-fe4, fep1-fep4, size decile,
size quintile, year-start ME); (2) daily NYSE size-decile EW returns
1973-1982; (3) per-observation event-time daily returns with u = R_i − R_p
for event days [-311, +60]. Methodology per assumptions A1-A15. Report: firm
counts vs paper 2,053; obs/quarter vs paper 1,495-1,978; rdq loss rates; FE
summary stats; unconditional FEP frequencies (Table 1 column 1 preview);
decile mean daily returns (Table 3 preview).

**rep-worker report:**

Pipeline complete, runs end-to-end in ~70s. panel.parquet: 77,492 obs × 25
cols; 3,024 firms; 32 quarters (19741..19814). Firm counts: Screen 1 → 3,271
(paper 2,213); Screen 2 + rdq → 3,025 (paper 2,053). Obs/quarter: 1,965-2,527
(paper 1,495-1,978). Decile mean daily returns 1973-1981 near-exact vs Table 3
(0.112/0.111, 0.090/0.084, ..., 0.023/0.021). Unconditional FEP freqs ≈ 0.10
for all four models. FEP1 median FE2 = -2.244 = paper exactly; FEP10 = 2.109
vs paper 3.151. Model 2 CAR[+1,+60] by FEP = [-1.34, -1.70, -1.08, -0.80,
-0.14, 0.39, 0.31, 0.92, 1.43, 1.79]% vs paper [-3.08, -2.73, -1.78, -0.92,
0.22, 0.79, 1.32, 1.70, 2.21, 3.23]%. CAR[-1,0] tracks well (FEP1 -1.51 vs
-1.34; FEP10 1.95 vs 1.26). Models 3/4: no drift in [+1,+60] as in the paper.
IBM (006066) 1975Q2 FE1 hand-computation matches. Also cached
decile_returns.parquet (25,270 rows) and event_returns.parquet (29.65M rows,
event days -311..+60). Flag: non-NYSE firms breakpoint-assigned to NYSE
deciles (their rationale: drop-interpretation falls below the paper's min
1,495 obs/quarter).

**Replicator decision:** ACCEPT (with A16 logged). Independently recomputed
M2 CARs and conditional frequencies from panel.parquet — worker's numbers
reproduce. Magnitude attenuation (CAR[+1,+60] ~45-55% of paper) diagnosed as
data vintage, NOT methodology: (1) FEP10 median FE2 = 2.109 vs 3.151 — the
good-news tail is 33% thinner on the restated modern tape while the bad-news
tail matches to 3 decimals; (2) Model 1 (no σ estimation) persistence is also
attenuated (FEP1 lag-1 conditional 0.247 vs 0.334), locating the cause in the
earnings series itself (restatement smoothing) rather than in our σ windows.
Countervailing correctness evidence: Table 3 decile returns near-exact,
[-1,0] window matches, M3/M4 correctly show no drift. Counts above paper
(3,024 vs 2,053 firms) are the expected direction per A4 (modern tape
includes delisted firms; 1982 tape was survivor-biased). Per-cell evaluation
deferred to the table iterations; Tier 2 with documented justification is the
anticipated outcome for magnitude cells (logged in assumptions.md Iteration 1).

## Inner iteration 2: Compute Tables 1, 3, 4

**Task spec → rep-worker:**

Table 3 (decile mean daily returns + 9-year avg OLS betas + Scholes-Williams
betas via dsi.ewretd), Table 1 (200 unconditional/conditional FEP
frequencies), Table 4 (120 pooled CAR cells + the paper's own 1,000-trial
empirical-distribution significance stars). Deliverables: results/table_{1,3,4}.md,
results/cells_iter2.csv (350 cells, names matching tables_to_replicate.json),
three plots (drift bars, event-time CAR Figure-1 style, quarterly CAR
Figure-2 style). Per-cell Tier tally vs tolerances.

**rep-worker report:**

350 cells computed in ~8s. Table 1: 191 Tier 1 / 7 Tier 2 / 2 FAIL (both M2
FEP10 conditional freqs — the FE2 upper-tail vintage effect). Table 3: mean
daily returns all Tier 1 (0.112 vs 0.111 ... 0.023 vs 0.021); OLS betas all
Tier 2 (1.32→1.06 vs paper 1.11→0.92, uniform +0.15-0.25 shift, ranking
preserved); SW betas all FAIL — 2.35-2.93 vs paper 0.83-1.16. Table 4: 90
Tier 1 / 3 Tier 2 / 27 FAIL; headline reproduced (M1/M2 monotone drift, M3/M4
none); stars 109/120 matching the paper's. Files: src/sql/market_index.sql,
src/tables.py, results/table_{1,3,4}.md, results/cells_iter2.csv, three plots
(drift bars, event-time Figure-1 style, quarterly Figure-2 style). Worker
flagged the SW formula as structurally incapable (numerator ≈4β) and verified
arithmetic per Rule 2/4 — the spec, not the code, was wrong.

**Replicator decision:** ACCEPT T1/T4; REVISE T3-SW (my spec error). Two
committed fixes + new tables in iteration 3 (below). The 27 T4 FAILs are
assessed as: vintage attenuation on M1/M2 [+1,+60] magnitudes (A4/A16
diagnosis, signs + monotonicity intact), near-zero M3/M4 [+1,+60] sign flips
(|CAR| ≤ 0.9% — the paper's "no drift" inference holds), and the paper's own
anomalous M1 FEP3 [+1,+60] = -7.58 cell. Tier 2 with documented justification
is the expected outcome for the magnitude cells; the pattern-level claims
(drift exists for Models 1-2, not 3-4; persists across subperiods) replicate.

## Inner iteration 3: SW-beta fix, two-stage stars, Tables 6 & 7

**Task spec → rep-worker:**

(A) Replace SW estimator with Dimson (1979) summed-beta (b_lag + b_contemp +
b_lead from one annual regression on r_{m,t-1}, r_{m,t}, r_{m,t+1}; avg
1974-1981). (B) Two-stage significance draw per L1357-1363 (8,000 from the
full firm×quarter frame, keep available, 1,000 trials). (C) Table 6: Model 2
& Model 4 CARs, 10 FEP × 5 quintiles × 3 windows (150 cells). (D) Table 7:
eq. 16 OLS (FEP only / FSQ only / both) for 4 models × 3 windows on the 50
quintile CARs, with the L2102 FSQ coding (204 cells). Deliverables: updated
table_3/4.md, new table_6/7.md, cells_iter2.csv extended to 702 cells,
full 798-cell Tier tally.

**rep-worker report:**

All four tasks done; tables.py runs end-to-end in ~9 s.
- Task A (Dimson SW): Table 3 now FAIL=0 — Dimson betas 1.35→0.91 vs paper
  1.16→0.83, same monotone ranking, all within tolerance (T3: 15 T1 / 15 T2).
- Task B (two-stage stars): 110/120 star agreement (was 109); kept-sets
  ~6,406/trial; residual mismatches magnitude-driven, not test-driven.
- Task C (Table 6): 244 registry cells; M2 q1 [-1,0] [-2.34…3.22] vs paper
  [-1.83…2.58] (signs/monotone match), M2 q1 [+1,+60] attenuated [-1.85…2.50]
  vs [-3.34…5.00]; M4 FEP1 q1 [-60,0] = -28.76 vs paper -28.68 near-exact.
  T6: 174 T1 / 6 T2 / 64 FAIL.
- Task D (Table 7): M2 [+1,+60] FEP-only R²=0.726 (paper 0.810), FSQ-only
  0.640 (0.661), both 0.781 (0.850); β1=0.33 t=11.45 (paper 0.67, 14.48),
  β2=-0.31 t=-9.39 (paper -0.60, -9.83) — signs + significance replicate,
  magnitudes ~half (A16). M4 [+1,+60] FEP R²=-0.011 (paper 0.028) ✓ flat;
  M3 R²=0.364 (paper ~0) spurious (§4.3 of REPORT). T7: 138 T1 / 18 T2 / 48 FAIL.
- Registry T7 name-collision bug diagnosed by worker; replicator regenerated
  tables_to_replicate.json with unique variant-aware names (values and paper
  line references unchanged, re-verified line-by-line); CSV name set asserted
  equal to registry (204 unique).
- Two code bugs found and fixed by worker: Table 7 needed all-4-model quintile
  CARs; T6 window-token underscore parse (was → all SKIP).
- Total over 798 cells: 608 T1 / 49 T2 / 141 FAIL / 0 SKIP.

**Replicator decision:** ACCEPT. Independent re-evaluation of cells_iter2.csv
against the registry (separate script) reproduces the identical tally
(608/49/141/0) and the FAIL taxonomy: ~57 magnitude-attenuation cells (A16),
14 attenuated t-stats, ~45 near-zero sign flips (paper-insignificant cells),
16 M3 p1_60 spurious-structure cells, 25 T6-M4 mixed near-zero/attenuated,
2 M2 FE2-tail persistence cells, 1 paper transcription anomaly
(m1_fep3_p1_60 = -7.58 breaks the paper's own monotone pattern; ours -1.43
is monotone). Every diagnosis in assumptions.md has a fix attempt or an
evidence-based non-actionable classification (exit gate satisfied). Inner
loop closed after 3 iterations; no actionable code-level issues remain —
residual FAILs are external (data vintage) or paper-side. Proceeding to
REPORT.md and the auditor.

## Summary

Pipeline + five tables complete: 798 committed cells, 82% pass (Tier 1+2).
All paper claims replicate qualitatively; CRSP-only Table 3 and the
announcement-window CARs replicate near-exactly; drift magnitudes in
[+1,+60] attenuated to ~half — diagnosed as restated-earnings vintage effect
(A4/A16), non-actionable. REPORT.md written. Next: auditor (Step 4).

