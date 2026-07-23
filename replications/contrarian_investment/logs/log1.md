---
iteration: 1
slug: contrarian_investment
inner_iterations: 5
worker_spawns: 5
---

# Outer Iteration 1 — Reasoning Trace

Paper: Lakonishok, Shleifer, Vishny (1994), "Contrarian Investment,
Extrapolation, and Risk," Journal of Finance 49(5), 1541–1578.
22 annual end-of-April formations (1968–1989), NYSE/AMEX common stocks,
equal-weighted 5-year buy-and-hold portfolios sorted on B/M, C/P, E/P,
past sales growth (GS), and their two-dimensional intersections.

Prep summary (Stages 1–6): parsed paper → candidate assessment
(replicable, empirical_cross_sectional) → 27 preprocessing rules across
all 8 categories with line-cited paper quotes → 8 tables selected
(I–VIII; Table VII GNP panels out of scope, external BEA data) →
1,290 per-cell targets transcribed from the paper's own tables →
data verification verdict=ready, 7/7 requirements full
(crsp_202601, comp_202601.funda, ff). prep_validation.py exit 0.

Pre-loop sanity checks (run by replicator against live ClickHouse,
2026-07-22):
- April month-end trading dates exist in msf for every year 1963–1995
  (1968-04-30 ... 1989-04-28); 2,104 NYSE/AMEX common stocks at
  1968-04-30, 1,968 at 1989-04-28 (shrcd 10/11, exchcd 1/2 PIT).
- funda filter indfmt='INDL', consol='C', popsrc='D', datafmt='STD'
  is the dominant combo (593,432 rows); coverage: 2,572 firms FY1962
  → 6,612 FY1974 (the paper's own 1978 Compustat expansion, L118) →
  9,343 FY1989.
- Units verified via IBM (permno 12490, gvkey 006066): at 1989-04-28
  prc=114.0, shrout=592,127 (thousands) → ME≈$67.5B; funda FY1988
  ib=5,491 dp=3,871 sale=59,681 ceq=39,509 ($M). CCM primary link
  (linkprim='P', linktype='LC') covers 1962–present.
- dsedelist dlret present; msi vwretd/ewretd from 1925; ff rf from
  1926-07.

Assumptions A1–A12 seeded in preparations/assumptions.md before the
first spawn (share codes, book-equity hierarchy, fiscal-year
alignment, GS missing-year normalization, size-decile population,
delisting-replacement formula, vintages, positive-ratio sort
restriction, Table IV cross-section, Table VII month states, Table VIII
betas, Hansen-Hodrick SEs).

## Inner iteration 1: data pipeline

**Task spec → rep-worker:**
Build data/panel.parquet — one row per (permno, formation year) for the
22 April formations 1968–1989 — with: universe PIT membership
(shrcd 10/11, exchcd 1/2); formation-date ME (|prc|×shrout×1000);
BE = coalesce(ceq+coalesce(txdb,0), seq−coalesce(pstkrv,0),
at−lt−coalesce(pstkrv,0)) from FY datadate∈[t−1−01−01, t−03−31],
be_valid = BE>0; bm, ep, cp, sp, dp_ratio with ep_pos/cp_pos flags;
GS = weight-normalized 5/4/3/2/1 average of valid sales-growth years
(both-year positive sales), cross-sectional fractional rank per
formation; size_dec from December t−1 universe ME deciles (fixed for
all 5 holding years); stock annual buy-and-hold returns R1..R5 with
mid-year delisting replacement (realized return to delisting month
with dlret absorbed, then grossed by the EW size-decile return for the
remaining months, per A6); sizedec_ret_1..5 for SAAR; alive_1..5; wide
accounting columns sale/earn/cf/div for FY t−5..t+4 (Table V per-$1
machinery); CCM link PIT (linkprim='P', linktype LC/LU). All heavy
lifting in saved src/sql/*.sql; main.py only assembles and writes the
panel + diagnostics. Also save (not fully execute) monthly_returns.sql
and size_benchmarks_monthly.sql for Table VII. Report: dimensions, N
per formation, signal diagnostics, IBM check (ME≈6.75e10, ep≈0.081,
cp≈0.139), delisting/NULL counts.

**rep-worker report:**
Pipeline complete, ~10 s total runtime. Deliverables: 10 documented
SQL files (all cross-sectional computation in ClickHouse; annual
compounding + A6 delisting gross-up assembled in pandas, re-verified
to 6 decimals against an independent recompute), src/main.py
(cwd-independent), data/panel.parquet (48,994 rows × 82 cols).
- N per formation: 1968=2,104 → peak 2,530 (1973) → 1,968 (1989); no
  formation below 300. The hump shape matches the paper's own account
  of the 1978 Compustat expansion (L118).
- Signal coverage (formation-averaged): be_valid 76.6%, ep_pos 70.3%,
  cp_pos 70.9%, gs_valid 76.8%, CCM-linked 78.3%. Early-year thinness
  is the expected vintage-coverage effect (A7) — first suspect if
  early-formation cells drift.
- B/M: formation medians 0.47-0.48 (1968-69) → 1.44 (1975) → 0.70
  (1989); 1989 decile-1 mean B/M 0.197 vs decile-10 mean 2.462
  (paper Table V glamour/value averages: 0.225 / 1.998 — consistent).
- IBM 1989: me_apr 6.7502e10 ✓, ep 0.0813 ✓, cp 0.1387 ✓, bm 0.654
  (A2 ceq+txdb), gs_rank_frac 0.388, size_dec 10. Worker flagged my
  task-spec hint "bm ≈ 0.59" as the ceq-only variant — A2 implemented
  exactly; hint error acknowledged, no methodology change.
- Delisting replacement events per holding year: +1 2,373 / +2 2,270 /
  +3 2,182 / +4 2,066 / +5 1,977 (of ~44k live rows); 28 rows delist
  exactly on the formation date (alive_1=0, excluded). 19,998 NULL
  monthly returns coerced, 0 sentinels (of 747,935 rows).
- 1989 glamour (B/M D1) mean ME = 4.75× value (D10) mean ME ✓.
- ClickHouse quirks documented: string dates (lexicographic compare),
  interval-overlap joins via CROSS JOIN+WHERE over the 22-row
  formation set; funda deduped by latest datadate per (gvkey, fyear).

**Replicator decision:** ACCEPT. Diagnostics are consistent with the
paper's universe, variable definitions, and known magnitudes. The
be_valid/ep_pos/cp_pos coverage (~71-77%) is the main vintage gap vs
the authors' early-1990s Compustat and is already logged under A7
(Tier 2 fallback if magnitudes drift while patterns hold). Proceed to
Tables I-III.

## Inner iteration 2: Tables I, II, III (+ Figure 1)

**Task spec → rep-worker:**
Compute the three portfolio-return tables from data/panel.parquet
(details in spawn prompt): Table I univariate decile sorts (B/M, C/P,
E/P ascending on positive/valid subsets; GS ascending via
gs_rank_frac), EW member averages of R1-R5, AR = mean(R1..R5), CR5 =
formation-mean of product(1+Rk)-1, SAAR = formation-mean of
(1/5)Σk(portfolio Rk − EW-member sizedec_ret_k). Table II independent
30/40/30 sorts with per-variable 30/70 breakpoints on the valid
subsets, 9 intersections per pair. Table III = Table II machinery on
the largest-50%-by-me_apr subsample, re-sorted within the subsample.
Deliver results/table_1.md, table_2.md, table_3.md (paper-format
tables), table_I_cells.json / table_II_cells.json / table_III_cells.json
keyed by the exact target names in tables_to_replicate.json, and
results/figure_1.png (C/P×GS CR5 bars).

**rep-worker report:**
Tables I-III + Figure 1 complete (src/sortlib.py shared sort machinery;
src/tables.py). All cells JSONs fully emitted (316/316, 366/366,
140/140). Headline spreads: Table I AR spreads B/M +0.108, C/P +0.113,
E/P +0.083, GS −0.055 (paper +0.105/+0.110/+0.076/−0.068); SAAR B/M
−0.040→+0.036 (paper −0.043→+0.035). Table II-A AR 0.109 vs 0.213
(paper 0.114/0.221), SAAR spread 0.080 (paper 0.087). Table III-A AR
0.103 vs 0.186 (paper 0.106/0.184), SAAR −0.037/+0.048 corners (value
corner 0.035 vs paper 0.048 — modest drift). Monotonicity: B/M, C/P,
E/P perfectly increasing; GS decreasing with 2 tiny wobbles. 10/10
deciles and 9/9 cells non-empty in every formation; cell-size pattern
matches L1213 (negative-correlation corners largest).
⚠ Flags: E/P D10 dip (paper 0.162 < D9 0.193) does NOT reproduce
(ours 0.195 ≥ 0.193, monotone) — modern restated vintage lacks the
distressed-firm concentration in the top E/P decile.

**Replicator decision:** ACCEPT with evaluator run. Independent
per-cell evaluation (evaluate_cells.py): 798 MATCH / 13 PATTERN /
11 FAIL / 468 SKIP-of-remaining-tables (98.7% hit rate on scored).
ALL 11 FAILs are near-zero SAAR cells (|paper| ≤ 0.031, |rep−paper| ≤
0.019, sign flips) — concentrated in the vintage-sensitive
size-benchmark component; raw-return cells pass. Diagnosis: SAAR =
portfolio AR − size-decile-benchmark AR; AR cells match, so the
residual is the benchmark, which depends on CRSP vintage (paper used
early-1990s CRSP; we use 2026). Next fix attempt (inner iteration 3):
recompute the 11 failing cells under the alternative A5 reading
(size deciles reassigned at each December within the holding period —
"decile at the end of the previous year" could apply per holding
year); adopt only if failing cells improve without degrading headline
corners; otherwise classify as vintage residual with justification.

## Inner iteration 3: Table VI + Figure 2 + SAAR diagnostic

**Task spec → rep-worker:**
Year-by-year V−G spreads for 3 panels × 1/3/5-yr horizons with the
paper's April-1990 sample boundary (22/20/18 obs), pooled (9,10)−(1,2)
deciles for P1/P3 and C/P×GS corners for P2; Hansen-Hodrick t-stats per
A12; Figure 2 with NBER recession + EW-decline markers; SAAR diagnostic
recomputing the 11 failing cells + 6 headline corners under the
alternative A5 reading (December reassignment each holding year),
report-only.

**rep-worker report:**
table_6.md + table_VI_cells.json (197/197) + figure_2.png +
saar_diagnostic.py. Averages vs paper: P1 0.087/0.383/0.910 (paper
0.079/0.357/0.841); P2 0.125/0.524/1.111 (0.102/0.464/1.073); P3
0.074/0.387/0.980 (0.063/0.344/0.842). t-stats all within 24% (A12
verified to reproduce the paper's t's; textbook MA(H−1) truncation
unstable at T=18 — P1 5-yr → 18.3). Year grid 145/180 within 50% —
misses all near-zero paper cells (|abs dev| ≤ 0.1). "Value beats
glamour in every 5-yr window": TRUE 18/18 in all three panels.
⚠ Worker overrode my P3 spec (single deciles, per caption) with the
pooled (9,10)−(1,2) reading after empirical test: 1968 pooled 0.104 ≈
paper 0.098; single D10−D1 = 0.043 (56% off). Paper's header (L2220)
and body (L2278) use pooled; caption (L2210) is the inconsistent part.
SAAR diagnostic: reassigned moves 6/7 full-sample failing cells toward
the paper (e.g. GS D1 0.008→0.017 vs paper 0.022) but also drifts
headline corners (B/M D10 0.036→0.044 vs paper 0.035) and worsens 2/3
Table III failing cells; parity on T3 rows clouded by
benchmark-construction differences. Recommendation: do not switch.

**Replicator decision:** ACCEPT Table VI as-is. Two decisions:
(1) A5 NOT switched — the reassignment evidence is mixed (6/7 on
full-sample near-zero cells vs headline-corner drift + Table III
harm); switching would be tuning a convention to fit near-zero cells.
The 11 SAAR FAILs are classified as vintage residuals WITH fix
attempted and measured (exit-gate satisfied): all |deviation| ≤ 1.9pp
on cells where |paper| ≤ 3.1pp; every SAAR claim the paper actually
makes (glamour negative / value positive adjustments; 7.8-8.8pp
spreads) replicates. (2) The worker's pooled-P3 override is ratified
and logged as Assumption 13 — evidence over caption.

## Inner iteration 4: Table V (fundamentals & growth rates)

**Task spec → rep-worker:**
Extend the panel (FY t−6 accounting cols; monthly returns back to May
1963; ret_m3_0 pre-formation cumulative return) and rebuild; compute
Table V: Panel A EW portfolio ratios (E/P, C/P, S/P, D/P, B/M, SIZE;
negatives included per A8) and Panels B/C per-$-invested growth rates
(formation-averaged per-$ series, sign-preserving geometric root) +
RETURN(−3,0). Emit table_5.md + table_V_cells.json (63 targets).

**rep-worker report:**
Panel rebuilt 48,994 × 87; N per formation bit-identical, IBM row
unchanged + new cols verified. 63/63 targets emitted. Panel A ratios
track the paper (E/P .023/.049 vs .029/.054 glamour; D/P exact; B/M
.245/2.556 vs .225/1.998); RETURN(−3,0) +1.576/−0.055 vs +1.455/−0.119
(B/M), +1.357/+0.237 vs +1.390/+0.225 (CPGS) ✓. Internal consistency:
CPGS glamour C/P 0.076 grown at ACG(0,5) → 0.136 = paper's 0.136 ✓.
Formal pass-rate 36/63 (avg-Q-first). Failure clusters: (i) SIZE
1.7-2× paper (mean vs likely-median pattern); (ii) earnings-growth
blowups on B/M value (−1.57, −2.77, +1.90) from zero-crossing of
formation-averaged earnings under the restated vintage; (iii) cash-
flow/sales growth match in sign+direction at ~2× magnitude (vintage).
perFy-first alternative: 31/63, avoids blowups but matches less.

**Replicator decision:** ACCEPT. Ratify avg-Q-first as default (paper's
explicit method L160 + higher pass-rate) and mean SIZE (direct
reading; median NOT adopted — would be tuning to fit). Log both as
Assumptions 14-15. Remaining Table V fails classified as vintage
residuals with evidence: the table's qualitative claims (glamour
fundamentals vs value fundamentals; past-growth gap; non-persistence
of glamour growth; RETURN(−3,0) glamour run-up) all replicate.

## Inner iteration 5: Tables IV, VII, VIII

**Task spec → rep-worker:**
Table IV: 9-spec Fama-MacBeth on R1 with GS, B/M, SIZE=ln(ME$M),
E/P+, DE/P, C/P+, DC/P (negatives kept via dummies per A9), FM
mean ± time-series t over 22 formations. Table VII: monthly_returns
over May 1968-Apr 1995; states W25/N88/P122/B25 from the EW index
(verify 25/88/122/25); active cohort per month = most recent April
formation; 1A 9 cells + EW index; 1B deciles + pooled (9,10)−(1,2)
spread + t; 91 targets. Table VIII: per-portfolio 22-obs annual R1
series → beta vs (VW − rf), std, saar_std; EW-index row; 54 targets
(P2 portfolio cells and P3 D7-10 computed but unscored per OCR notes).

**rep-worker report:**
- Table IV: 63/63 emitted, 38 MATCH/15 PATTERN/10 FAIL. Key claim
  holds: B/M collapses in specs 6/8 (coef +0.009/+0.005, t 0.82/0.55)
  with GS (t −3.3/−2.7) and C/P+ (t 2.1/2.4) significant. Fails =
  E/P+/C/P+ magnitudes ~½ paper (signs/significance correct).
  Bug fixed: clip(lower=0) left NaN→NaN making specs singular; fixed
  via fillna(0) + requiring raw ep/cp non-null while keeping zero
  numerators so DE/P/DC/P vary.
- Table VII: 91/91 emitted, 82 MATCH/8 PATTERN/1 FAIL. Counts
  25/88/122/25 resolved: they sum to 260 (paper's EW window), so
  semantic classification over 324 months (64 moderate months
  unclassified) — the only reading matching counts AND neg/pos
  labels. Claim holds: value loses less in W25 and N88 for both
  classifications (1A W25 value −0.086 = paper exactly).
- Table VIII: 54/54 emitted, 50 MATCH/3 PATTERN/1 FAIL. rf verified
  DECIMAL in this extract (annual ~0.08; my task-spec /100 hint was
  wrong — worker corrected empirically, betas land at paper's ~1.3).
  Betas/stds all pass incl. EW index (1.339/0.268 vs 1.304/0.250).
  Value−glamour beta gap −0.05 (paper +0.1): trivial magnitude,
  paper's "can't explain the spread" conclusion holds either way.
  1 FAIL = glamour D1 saar_std (same fixed-benchmark mechanism as
  the iter-3 SAAR residual).

**Replicator decision:** ACCEPT all three. Classify remaining FAIL
clusters under A7 (vintage), A14/A15 (Table V), A5 (SAAR benchmark),
each with the cross-table evidence (consistent 15-25% ratio-level
drift; early-formation thin coverage). No further fix iterations:
every FAIL cluster has diagnosis + evidence + classification, and
the only candidate convention change (December-reassigned size
deciles) was tested in iter 3 and rejected as tuning-to-fit.

## Assumption decisions this iteration
- A1–A15 as seeded/extended (see preparations/assumptions.md).
- Worker corrections ratified: rf decimal units (Table VIII);
  semantic state classification (Table VII); pooled P3 (A13).

## Per-cell evaluation (final, evaluation_iter5.json)
| Table | MATCH | PATTERN | FAIL | Total |
|-------|-------|---------|------|-------|
| I     | 309   | 4       | 3    | 316   |
| II    | 359   | 2       | 5    | 366   |
| III   | 130   | 7       | 3    | 140   |
| IV    | 38    | 15      | 10   | 63    |
| V     | 36    | 7       | 20   | 63    |
| VI    | 163   | 11      | 23   | 197   |
| VII   | 82    | 8       | 1    | 91    |
| VIII  | 50    | 3       | 1    | 54    |
| **All** | **1,167** | **57** | **66** | **1,290** |

Tier 1+2 hit rate: **94.9%**. FAIL clusters (REPORT.md §5): (a) 15
near-zero SAAR/saar_std cells; (b) 30 fundamentals-level & FM-magnitude
cells (vintage fingerprint); (c) 21 early-formation/near-zero year
spreads + 1 noise t-stat. All diagnosed with evidence; all paper
claims replicate (REPORT.md §1).

## Summary
All 8 tables + 2 figures replicated from raw CRSP/Compustat in 5 inner
iterations (pipeline → I-III → VI+diagnostic → V → IV/VII/VIII).
1,290 per-cell targets: 90.5% Tier-1 match, 4.4% Tier-2 pattern,
5.1% documented vintage residual. Paper's five central claims all
replicate (value-glamour spreads 8-11pp/yr; large-cap robustness;
extrapolation errors in fundamentals; consistency incl. 18/18 5-yr
windows; no downside risk; B/M subsumed by C/P+GS). Ready for audit.
