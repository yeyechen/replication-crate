---
iteration: 2
slug: returns_to_buying_winners
inner_iterations: 3
worker_spawns: 3
---

# Outer Iteration 2 — Reasoning Trace

Audit 1 (logs/audit1.md): verdict PARTIAL, overall 3.83/5, verdict
REPLICATED, requires_iteration=true — 0 blockers, 4 actionable majors
(all uncomputed paper corollaries with verified-available data), 2
non-actionable majors (M5 F-stat construction ambiguity; M6 vintage
residual — classification endorsed by the auditor), 5 minors.

**Scope of this iteration:** M1 (Table VIII back-test 1927–1964),
M2 (Table IX earnings announcements), M3 (§III decomposition stats),
M4 (Tables V/VI win rates + subperiods), minors m1–m3. Contract extended
to 9 tables / 1,327 cells (T6 Table V 56, T7 Table VI 120, T8 Table VIII
288, T9 Table IX 72).

**Replicator decisions:**
- m1 (classification hygiene): fixed in the replicator's evaluation
  harness — sign-opposite cells are now FAIL regardless of magnitude
  (consistent with rep/TOLERANCE_RULES.md); near-zero noise cells flip
  from Tier 2 → FAIL cosmetically (grand totals → 680/92/19).
- M6 universe-scope bounding test: SKIPPED this iteration (attribution
  only; priority is the four corollaries; documented in REPORT).
- M5 (F-stats): no revisit (three variants reported; paper-side
  ambiguity; per audit guidance).
- Delisting treatment stays as-is (A3 revision; auditor-endorsed).

## Inner iteration 1 (iter 2): M1 backtest + M4 Tables V/VI + m2 diagnostics

**Task spec → rep-worker:** extend panel to 1926-07 (bit-identity gate on
the 1965–89 region); compute Table VIII event-time for cohorts formed
1927–1940 (A) and 1941–1964 (B); Tables V/VI from existing series;
persist §3 diagnostics (m2).

**rep-worker report:**
- Panel extended to 1,097,807 rows; pre-1962 universe SOUND (dsf↔PIT
  match 96.5–98.1%/yr; stocks/month: 1927 559 → 1941 781 → 1960 1,081 →
  1965 2,075; smooth monotone, no dsfhdr fallback needed — P21).
  Bit-identity: 201 snapshot rows × 13 columns, max|diff| = 0.000e+00;
  Tables I–VII unchanged (PA 6/6 0.011530, C_12 +5.9%, T3 pivot ≡ T1).
- **M1 / T8 (288 cells):** Panel A — month 1 −0.0138 vs −0.0495 (sign ✓,
  magnitude ≈¼ of paper — vintage-sensitive crash era, as pre-managed);
  C_36 −0.3029 vs −0.4081 (+26%, strongly negative ✓, t −4.66). Panel B —
  **C_12 0.0583 vs 0.0583 (+0.1%)** — exact; months 2–8 mean +0.0074 ✓;
  71% dissipated by month 24 (paper ~100%); post-month-12 cells nil both
  sides. Tally 26/288 ±10%, 110/288 ±30%. Hand checks <1e-12 (1935-06,
  1955-06 formations).
- **M4 / T6 Table V (56 cells):** 48/56 ±10%, 55/56 ±30%. Headline
  proportions EXACT: Jan 0.24 (0.0%), Apr 0.96 (0.0%), Feb–Dec 0.7127
  (+0.4%), all-months 0.6733 (+0.5% — the L907 "67%"). Only outlier:
  prop_jan_s1 0.24 vs 0.16 (6/25 vs 4/25 Januaries — 2 Januarys).
- **M4 / T7 Table VI (120 cells):** 49/120 ±10%, 92/120 ±30%. Anchors:
  65–69 All 0.0108 vs 0.0123 (−12%); Jan 70–74 −0.1005 vs −0.1070 with
  **t −2.538 vs −2.540 (+0.1%)**; the paper's only negative full-period
  cell (All 75–79 −0.0044) comes in at +0.0003 (nil both sides, |diff|
  0.0047/mo — the A12 residual direction, P25).
- **m2:** 11 diag_* keys persisted (Sharpe 0.8333, total 2077.96%, MDD
  −41.91%, arithmetic 13.84%, geometric 13.1155%, FF5 α 16.8417% t 4.8648
  R² 0.1348; rf-sub variant 10.05% t 2.89) — all match auditor-recomputed
  values; asserted vs REPORT §3 at run time.
- Determinism: 3 full runs, md5-identical artifacts (timestamp exception
  noted: primary_diagnostics.md, same convention as existing diagnostics).

**Replicator decision:** ACCEPT all three. M1 Panel A magnitude deviation
is the expected vintage effect (documented, pattern holds); Panel B is an
exact headline match. M4 replicates. Diagnostics persisted. Proceed to
M3 + M2 (inner iteration 2 of this outer iteration).

### Iteration — Problem: pre-1962 universe availability for the back-test
- Diagnosis: dsenames PIT windows cover the full CRSP daily era (match
  rate 96.5–98.1% 1926–1961); counts grow smoothly 528→2,534; the 1962-07
  step is the daily file's start (1,121 windows end there).
- Next fix: none needed — extend DAILY_START to 1926-07-01, keep the PIT
  join; gate on 1965–89 bit-identity.
- Before metric: panel 728,207 rows (1962-07 start).
- After metric: 1,097,807 rows (1926-07 start); 1965–89 region max|diff|
  = 0 across all 13 columns; Tables I–VII bit-identical.
- Status: resolved

## Inner iteration 2 (iter 2): M3 decomposition + M2 earnings

**Task spec → rep-worker:** four §III decomposition statistics (WRSS
profit + corr, EW-index serial covariance, residual serial covariance,
squared-market θ regression with NW t); Table IX earnings-announcement
returns (fundq.rdq → CCM PIT link → 3-day dsf returns days −2..0 →
winner−loser by post-formation month, 72 contract cells).

**rep-worker report:**
- **M3:** residual serial covariance **+0.00120 vs paper +0.0012 —
  EXACT** (anchor is the lag-6 / consecutive-non-overlapping-period
  covariance; overlapping lag-1 is mechanically ~0.07). WRSS dollar-
  neutral weighted L/S +0.0342 vs 0.045 (−24%); **corr(WRSS, 6/6) =
  0.971 vs 0.95 ✓** (raw cross-sectional covariance 0.0021 also reported
  — the paper's "per dollar long" wording identifies the portfolio-scale
  quantity). EW-index 6m serial covariance −0.0061 vs −0.0028 (same
  sign; non-overlapping; overlapping +0.030 mechanical). θ = −1.86 vs
  −2.29 (+19%, sign ✓; halves −1.69/−2.04 vs −2.55/−1.83, signs ✓; our
  |t| 3.18 > paper's 1.74 — the P14 NW-SE effect). Paper's three causal
  verdicts all reproduce: factor-timing REJECTED (EW serial cov < 0),
  idiosyncratic underreaction SUPPORTED (residual serial cov > 0, exact),
  lead-lag REJECTED (θ < 0).
- **M2 / T9 (72 cells):** **abstract-level PATTERN REPLICATED** — months
  1–7 mean +0.0063 (6/6 positive and significant), months 8–20 negative
  in 12/13, months 11–18 mean −0.0047 (paper ≈ −0.7%), months 21–36 near
  zero; sign match 33/35 diff cells (94%). Anchors: ea_t11 −0.0037 vs
  −0.0039 (+4.5%). Coverage 12,435 announcements/post-month vs paper's
  429.2 (2026 Compustat vintage >> 1990 file; inflates Welch t via √n;
  documented P27). Tally ±10% 12/71, ±30% 23/71 — misses dominated by
  near-zero months 21–36 and √n-inflated t-stats; the pattern is the
  deliverable (Tier 2 with justification).
- Implementation notes P27–P28 (link dedupe, day-0 convention, WRSS
  period/normalization choices, serial-covariance conventions). Key
  count 1,349 = 1,327 contract (T1–T9) + 11 dec + 11 diag. Clean exit,
  idempotent re-run verified; data/ = ['panel.parquet'].
- Worker correctly overrode two spec inconsistencies against the paper
  (WRSS normalization; A2 overlapping-vs-non-overlapping), documented.

**Replicator decision:** ACCEPT M2+M3. Both audit-1 majors delivered with
honest vintage-attributed deviations. Proceed to the timing fix
(iteration 3, diagnosed below) — the last open methodology issue.

## Inner iteration 3 (iter 2): timing fix (1-month skip removal)

**Task spec → rep-worker (continuation of worker #2):** rank formation f
on cumret_J_raw at row f+1 (signal [f−5, f]); holding h=1..K unchanged;
align earnings window to f=1979-12..1989-11, WRSS past window and θ
x-window to [f−5, f]; re-run everything; report before/after; no tuning.

**rep-worker report:**
- Fix applied (gap-robust month mapping in formation_deciles); hand-
  verified the paper's Jan-1980 portfolio (f=1979-12 ranking on
  [1979-07, 1979-12], holding from 1980-01) to <1e-12.
- **Before/After (the fix resolved the apparent A12 residual):**
  | metric | before (skip) | after (A13) | paper |
  |---|---|---|---|
  | PA 6/6 sell | 0.006227 (−21.2%) | **0.008110 (+2.7%)** | 0.0079 |
  | PA 6/6 buy | 0.017757 (+2.1%) | 0.016908 (−2.8%) | 0.0174 |
  | PA 6/6 buy-sell | 0.011530 (+21.4%) | **0.008797 (−7.4%)** | 0.0095 |
  | T5 C_12 / C_36 | 0.1007 / 0.0697 | 0.1021 (+7.3%) / 0.0696 | 0.0951 / 0.0406 |
  | T8 PA C_36 / PB C_12 | −0.3029 / 0.0583 | −0.3420 (+16%) / 0.0621 (+6.6%) | −0.4081 / 0.0583 |
  | T9 m1–7 / m11–18 mean | +0.0063 / −0.0047 | +0.0072 / −0.0048 | ~+0.007 / ~−0.007 |
  | A1 WRSS mean / corr | 0.0342 / 0.971 | 0.0211 (−53%) / **0.963** | 0.045 / 0.95 |
  | A4 θ full / h1 / h2 | −1.86 / −1.69 / −2.04 | −1.98 / −2.21 / −1.58 | −2.29 / −2.55 / −1.83 |
  | T1 tally ±10%/±30% | 116 / 162 | **152 / 187** | — |
  | T8 tally ±10%/±30% | 26 / 110 | **56 / 151** | — |
- A1 WRSS mean moved AWAY under the mandated [f−5,f] alignment —
  reported honestly; the discriminating correlation anchor matches
  (0.963 vs 0.95). A3 residual serial covariance stays EXACT
  (+0.001199 vs +0.0012).
- Two methodology-obsolete guards retired to non-blocking notes (the
  raw-vs-adjusted STOP probe — A3 raw-PRIMARY is settled; the
  diagnostics-vs-REPORT§3 assert — §3 figures were pre-A13).
- A13/P29 + five-field iteration entry appended to assumptions.md.
- Key count 1,349; data/ = ['panel.parquet']; invariants re-asserted
  (K cohorts in all 300 reporting months × 32 grids; T5 n_1=299; T8
  168/288 formations; earnings 120 cohorts).

**Replicator decision:** ACCEPT. The timing correction was the dominant
error source behind the previously-documented sell-side "vintage
residual" — after the fix the 6/6 buy-sell is within −7.4% and all 192
Table I cells are Tier 1. A12 reframed in REPORT.md accordingly. Inner
loop CONVERGED (3 iterations, cap 10).

### Iteration 3 — Problem: implicit 1-month skip (resolution)
- Diagnosis: as logged above (signal [f−6,f−1] + holding f+1..f+K = gap month f).
- Next fix: rank formation f on cumret_J_raw at row f+1 → signal [f−5, f].
- Before metric: PA 6/6 sell 0.006227; buy-sell 0.011530 (+21.4%).
- After metric: PA 6/6 sell 0.008110 (+2.7%); buy-sell 0.008797 (−7.4%);
  T1 192/192 Tier 1.
- Status: resolved

## Per-cell evaluation (final, all 1,327 contract cells, post-A13)

| Table | Ref | cells | Tier1 | Tier2 | FAIL | hit% |
|-------|-----|------:|------:|------:|-----:|------:|
| T1 | Table I | 192 | 192 | 0 | 0 | 100.0% |
| T2 | Table II | 21 | 18 | 3 | 0 | 100.0% |
| T3 | Table III | 322 | 294 | 22 | 6 | 98.1% |
| T4 | Table IV | 112 | 105 | 5 | 2 | 98.2% |
| T5 | Table VII | 144 | 118 | 18 | 8 | 94.4% |
| T6 | Table V | 56 | 56 | 0 | 0 | 100.0% |
| T7 | Table VI | 120 | 110 | 8 | 2 | 98.3% |
| T8 | Table VIII | 288 | 195 | 61 | 32 | 88.9% |
| T9 | Table IX | 72 | 39 | 13 | 20 | 72.2% |
| **GRAND** | | **1,327** | **1,127 (84.9%)** | **130 (9.8%)** | **70 (5.3%)** | **94.7%** |

All 70 FAILs are cells the paper itself reports as statistically nil
(paper |t| ≤ 1.4, most ≤ 0.6) or crash-era month cells: mid-decile ≈0
alphas (T3: 6), nil calendar cells (T4: 2), year-2/3 event months
(T5: 8, T7: 2, T8: 32, T9: 20). No economically meaningful cell fails.

## Summary

Outer iteration 2 converged after 3 inner iterations. All four audit-1
actionable majors delivered (M1 Table VIII, M2 Table IX, M3 §III
decomposition, M4 Tables V/VI) plus the methodology-defining A13 timing
correction, which retroactively explained the bulk of the previously
documented sell-side deviation. Final state: 1,327 contract cells —
84.9% Tier 1, 94.7% Tier 1+2; headline 6/6 buy-sell within −7.4% with
sell/buy legs within ±3%; all of the paper's qualitative claims
replicate (positive significant spreads across all 32 strategies;
January effect; subsample stability; event-time inverted-U; 1941–1964
back-test similarity; crash-era Panel A sign/shape; earnings-
announcement winner/loser reversal; the three §III causal verdicts with
one exact-match statistic). Remaining deviations are vintage/measurement
differences documented with evidence in REPORT.md §5.3. Proceeding to
REPORT.md update + audit 2.

### Iteration 3 — Problem: implicit 1-month skip in formation/holding timing (DIAGNOSED, FIX COMMITTED)
- Diagnosis (replicator code inspection of src/main.py + src/sql/monthly_panel.sql):
  cumret_6_raw(m) compounds months [m−6, m−1] (window `ROWS BETWEEN 6
  PRECEDING AND 1 PRECEDING`), and cohort_decile_returns holds months
  f+1..f+K. Month f is therefore in NEITHER the signal (ends f−1) NOR the
  holding period (starts f+1) — the implemented strategy is the paper's
  strategy with a 1-month skip inserted between signal and holding. The
  paper is explicit (L111, L157): portfolios formed at t rank on returns
  [t−6, t−1] and hold [t, t+K−1] — Panel A is "formed immediately after
  the lagged returns are measured", no gap. Verified against the
  iteration-1 hand check (formation 1979-12 used signal [1979-06, 1979-11]
  and held from 1980-01; the paper's Jan-1980 portfolio uses signal
  [1979-07, 1979-12]). The miss went unnoticed because 6-month momentum
  signals are smooth across adjacent months (Table I buy side matched at
  <2% despite the misalignment).
- Next fix (committed): in formation_deciles, rank formation month f on
  cumret_J_raw evaluated at row f+1 (per-permno shift of the signal one
  month earlier), i.e. signal = [f−5, f]; holding stays h = 1..K (first
  holding month f+1 = paper's t). Downstream machinery (Panel B skip-5 at
  h=1, strategy_monthly cohort window, event-time indexing) all unchanged.
  Boundary effects: earliest formation 1963-06 (was 1963-07; reporting
  cohort counts unchanged — all reporting cohorts ≥ 1964-07 have valid
  signals); latest formation 1989-11 (cohort 1989-12 contributed no
  holding months anyway, n_1 = 299 unchanged); back-test formations
  1927-01 need cumret at 1927-02 = [1926-08, 1927-01] ✓ available;
  earnings cohorts become f = 1979-12..1989-11 = paper's t = 1980-01..
  1989-12 (120 cohorts ✓). Re-run ALL tables after the fix; accept
  whatever numbers result (methodology faithfulness > number matching).
- Before metric: PA 6/6 buy-sell 0.011530 (paper 0.0095, +21.4%); buy
  0.017757 (+2.1%); T5 C_12 0.100746 (+5.9%).
- After metric: (pending fix run)
- Status: unresolved (fix committed, awaiting worker #2 completion →
  spawn fix task)
