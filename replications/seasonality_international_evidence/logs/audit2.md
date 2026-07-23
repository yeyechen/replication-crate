---
iteration: 2
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — seasonality_international_evidence

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** All four audit-1 actionable majors (M1–M4) are genuinely
closed and all seven minors are fixed. Every new number I spot-checked —
T4/T5/T11/T12 spot cells, the full sensitivity battery, and both tier
schemes over all 1,613 cells — reproduced **bit-exactly** (Δ = 0.00) under
a fresh pure-pandas implementation written for this audit, from the cached
`data/panel.parquet` alone. Pre-existing Table 1/2/3/7 artifacts are
byte-identical to audit-1's verified state (file mtimes predate audit1.md
and were never rewritten; values recomputed exactly). No methodology
regression. Four wording/cleanup minors remain (m8–m11); the only
substantive gap left — Tables 6 and 8–10 — is externally data-blocked and
documented (A14, M5). The replication loop can exit.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All construction choices match the paper (eq. 1 FWL, lag sets, EW/VW deciles, intra/inter, calendar/size/correlation/bin-count mechanics); filter semantics now pinned (M4). Auditor's independent pure-pandas reimplementation of 30+ cells across all eight tables matches the committed values to Δ = 0.00. Deviations (data substitution, WLS inverse-variance reading of L112, no winsorization) documented and justified (A1–A14). |
| Headline matching | 3 | Central claim (annual − nonannual > 1%/mo at Years 2–5) replicates with correct sign/shape/significance at 66–75% of paper magnitude (Y23 diff +1.35% t 4.59 vs +1.80% t 8.25; Y45 diff +0.67% vs +1.01%); lag-1 reversal replicates in sign (Japan within 11%); Year-1 momentum still flips sign (−0.53% vs +1.21%/mo). Unchanged from audit 1 — the new tables do not touch the central claim. |
| Data coverage | 3 | Effective vintage start 1986-01 vs 1985-01 (A11, within ±1–2 yr); firms 19,685 vs 18,117 (+9%); firm-months 1.95M vs 2.44M (−20%); one documented all-encompassing source substitution (FactSet → Compustat Global+NA daily), all alternatives verified unavailable live. Unchanged — the panel was correctly left untouched. |
| Concrete result matching | 3 | Now measured transparently under both schemes by committed code: repo rules 613 T1 / 713 T2 / 287 FAIL; rubric 2× rules 613 / 299 / 701 over 1,613 cells (independently recomputed — exact). Tier 1 share 38% (was 35% over 906 cells); rubric T1+T2 56.5% (was 55.5%), scoring on the rubric's open T1+T2 choice per audit-1 precedent (Tier-1-only would be 2). The 9 audit-1 anchor assertions reproduce exactly. |
| Signal strength | 3 | Headline difference-strategy cells r = 0.66–0.75 (within [0.5, 2.0]); long-horizon nonannual levels r = 0.93–1.06; Y45 all exact; Japan lag-1 r = 1.11. Year-1 nonannual remains a sign flip, excluded from the headline set per the paper's own framing (the annual-vs-nonannual difference is the central claim). |
| Corollary | 4 | Big improvement (was 2): all six computable corollaries now computed and verified — calendar robustness (nonannual negative 11/12 months; Feb–Dec difference +1.13%/mo t 3.77, significant), size groups (Y23 difference positive 6/6; Y23/Y45 nonannual negative 6/6; Y1/Y45 annual positive 6/6), cross-country correlations (mean ρ 0.111/0.052/0.015, declining with horizon — the abstract's claim), bin-count robustness (11/12 rows keep the decile sign), plus the audit-1 intra-country/breadth results. Deviations: annual-row weakness across T4/T5 (disclosed per table), CHE-AUT y45 pair −0.04 vs paper −0.19; liquidity (T6) and risk factors (T8–10) remain blocked by unavailable fields/factors (A14, M5). |
| 7 | SUMMARY.md matches results/table_*.md | ✓ | ~25 headline numbers across REPORT §4.1–4.8 verified against `results/cells_*.json`, `evaluation_summary.json`, and my own recomputation; two new wording slips found (m8, m9). |

## 2. Issues by severity

### Blockers (must fix)

None. No fabricated or unverifiable numbers found. Every audited claim
reproduced.

### Major (should fix)

- [M5] (carried from audit 1, **non-actionable**) Risk-factor corollaries
  (Tables 8–10: alphas on global/local market, SMB, and French international
  BM/EP/CEP/DP factors) not computed.
  - File: paper §IV.C L1832–1856; REPORT §8; the catalog's
    `ff.global_factors` carries only daily mktrf/smb/hml/rmw/cma from
    1990-07, not the paper's bespoke factor set.
  - Likely cause: external data limitation — French's international value
    factors are not in the catalog.
  - Specific fix: none available in this loop — stays documented in
    REPORT §8 and assumptions.md.
  - actionable: false

No *new* actionable majors. Verification of the audit-1 majors:

- **[M1] CLOSED — verified.** `src/compute_t4_t5.py` consumes the cached
  panel and imports the verified Table 3 engine. I independently
  recomputed 9 T4 cells (incl. y23 nonannual Feb–Dec −0.01265/t −4.641 and
  y23 difference Jan +0.03687) and 12 T5 cells (incl. y23 difference
  intra-small +0.00778 and y45 annual inter-large +0.00303/t 1.80) from
  `data/panel.parquet` with a fresh implementation: **all match the
  committed cells to Δ = 0.00**. The qualitative claims check out from the
  cells: y23 nonannual negative in 11/12 months; y23 difference positive in
  10/12 months; y23 difference positive in all 6 size columns; y23/y45
  nonannual negative 6/6; y1/y45 annual positive 6/6. Table 6 deferred as
  A14 (panel lacks price/volume) — the option audit 1 explicitly offered.
- **[M2] CLOSED — verified.** `src/compute_t11_t12.py`: I recomputed the
  per-country annual-strategy correlation machinery from scratch — mean
  pairwise ρ = +0.111 (y1) / +0.052 (y23) / +0.015 (y45), exactly the
  reported values; |ρ|>0.12 counts 39/25/11 of 91; FRA-DEU y1 +0.387
  (paper 0.43) and FRA-UK y1 +0.390 (paper 0.34) reproduce; the NLD-GBR y23
  artifact is real (ρ = +0.900; dropping 2002-12 gives −0.077) and no
  committed metric uses it. T12: I recomputed 6 quintile/tricile cells
  (y23 difference q5−q1 +0.01160 vs paper +0.0139; y1 nonannual q5−q1
  −0.00284 — the documented Y1 flip; y45 difference t3−t1 +0.00603 vs
  +0.0072), all Δ = 0.00; the 11/12 sign-robustness claim checks out (sole
  exception y23 annual, all three bin counts noise-level: −0.0010/+0.0010/
  +0.0009). Committed paper values for T11/T12 verified against content.md
  (L3140+, L3599, L3639+) incl. the 5−1 = Q5−Q1 internal consistency
  (0 violations across all 240 T12 cells).
- **[M3] CLOSED — verified.** I re-ran `src/evaluate.py` (all 9 anchor
  assertions PASS: repo 319/143 with per-table FAIL 0/21/52/70; rubric
  319/184/403) and separately reimplemented both classification schemes
  from `tables_to_replicate.json` + `cells_*.json`: repo rules
  613/713/287, rubric rules 613/299/701 over 1,613 cells — **exact match
  per table and total** with `evaluation_summary.json`. The near-zero
  paper-value rule (7 cells) is documented and reproduces the audit-1
  convention. REPORT §4 now reports both pass rates (82% sign-consistent;
  57% rubric T1+T2) and the T2x label is gone. Cell coverage: 1,613/1,613
  committed names present in the cells JSONs, 0 missing, 0 extra.
- **[M4] CLOSED — verified.** `src/sensitivity_y1.py` pins the filter
  semantics (primary = recompute-in-filtered-universe; secondary =
  full-universe benchmark, membership-only) in code and prose. My
  independent engine reproduces all five primary variants **exactly**:
  baseline −0.0053/t −1.62/T 257; drop-Canada +0.0002/+0.06/245;
  |ret|>100% +0.0058/+2.26; |ret|>60% +0.0149/+6.79; top-50% cap
  +0.0066/+1.77/245. Row-drop counts verified from the panel (6,675 over
  |ret|>100%; 22,522 over |ret|>60%; 415,120 Canada; 1,086,203 cap). The
  REPORT §6.3 table now carries the committed numbers, and the
  anti-tweaking decision (no filter adopted) stands.

### Minor (cleanup)

- [m8] REPORT §4.6 magnitude range understates two size columns.
  - File: `REPORT.md` §4.6 ("positive in all six columns … at 46–89% of
    paper magnitude"). Auditor-recomputed ratios from `cells_t5.json` vs
    paper: intra_small 0.46, intra_medium 0.89, **intra_large 1.12**,
    inter_small 0.53, inter_medium 0.87, **inter_large 1.30** — the true
    range is 46–130%, and two columns *exceed* the paper.
  - Specific fix: "at 46–130% of paper magnitude (the two large-cap
    columns slightly exceed the paper; the two small-cap columns are
    roughly half)".

- [m9] REPORT §4.1 "399 Canada-only observations" is off by one BEL row.
  - File: `REPORT.md` §4.1 ("adding 399 Canada-only observations for
    1,950,889"). Auditor-recomputed from the panel: the 399 January-1985
    rows are 398 CAN + 1 BEL (Belgium's priced data starts 1983-12). The
    counts (1,950,490 / 1,950,889 / 399) are correct.
  - Specific fix: "adding 399 January-1985 observations (398 Canadian, 1
    Belgian)".

- [m10] Orphan nested directory tree from an iteration-1 CWD slip.
  - File: `replications/seasonality_international_evidence/replications/
    seasonality_international_evidence/{data,src,results,logs,inputs,
    preparations}` — six empty subdirectories created 2026-07-22 15:52
    (relative-path brace expansion run from inside the slug). Audit 1's
    spot-check 8 predated it or missed it; it is still on disk.
  - Specific fix: `rm -rf` the nested `replications/` subtree (32K, all
    empty).

- [m11] The consolidated `m1–m7` entry in the assumptions.md iteration-2
  issue log carries only a Status line.
  - File: `preparations/assumptions.md` ("### Iteration 2 — minors
    m1-m7"). The four major entries (M1–M4) correctly carry all five
    fields (Diagnosis / Next fix / Before metric / After metric /
    Status); the minors batch does not. A14 correctly uses the
    Decision/Rationale/Impact format shared by A1–A13.
  - Specific fix: optionally expand the batch into per-minor Before/After
    lines, or leave as-is — the individual fixes are all verifiable in
    REPORT.md / data_verification.json / log1.md (this audit confirmed
    each).

All seven audit-1 minors verified fixed: m1 (§4.1 counts clarified —
1,950,490 vs 1,950,889, modulo m9's wording nit), m2 (§4.2 acknowledges
the lag-3 All-OLS miss at 0.0110/t 2.03; my recompute confirms ours
−0.0005/t −0.14), m3 (§4.4 reworded with the paper's significant Canada
Y45 +0.0167/t 2.12), m4 (§2 now "57 … 68 two-tailed" — both counts
reproduced exactly from the panel; the 253-obs/68%-Canadian/$5.93M-vs-
$121M figures in §6.3 also reproduce exactly), m5 (`data_verification.json`
no longer mentions qunit; the market_cap_for_weighting requirement now
states "No qunit rescaling: A3 verified…"), m6 (§4.4 qualified "14/14 sign
match; 7 of 14 within 30% tolerance; three small markets below half", and
log1.md carries an explicit iteration-2 correction block), m7
(`src/evaluate.py` committed and anchor-asserting).

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Direction claims (lag profile; annual vs nonannual; breadth; new corollaries) | ✓ (long-horizon, breadth, calendar, size, bin-count) / ✗ (Y1; annual rows) | Independently recomputed: y23 nonannual negative 11/12 months; y23 difference positive 10/12; T5 direction claims 6/6 across all four rows checked; T12 signs match deciles in 11/12 rows (sole exception y23 annual, noise-level at all bin counts). Y1 and annual-row weakness unchanged and disclosed. |
| 2 | Headline-magnitude claim | ✓ | Y23 difference +0.0135 vs +0.0180 (75%, t recomputed 4.59); Y45 difference 66%; Y23 nonannual 106%; Y45 all exact (−0.0042); all recomputed from the parquet to Δ = 0.00 vs committed cells. |
| 3 | Sample coverage ≥ 60% | ✓ | Firm-months 1,950,490 = 80% of paper's 2,440,681; firms 109%; monthly cross-section mean 7,465 (79%). Recomputed from the panel. |
| 4 | Data-source choice justified | ✓ | Unchanged from audit 1 (A1–A4 live-verified; NTT $211,025,085,888 anchor re-confirmed in run_main.log; JPY/USD 107; euro cancellation). |
| 5 | prep_validation.py exit 0 | ✓ | The single reported layout error is the missing `audit2.md` — i.e., this file, written by this audit (same self-referential situation as audit 1). Exits 0 once audit2.md exists. |
| 6 | All committed tables have results files | ✓ | 8/8 tables in `tables_to_replicate.json` (90+192+288+336+312+144+11+240 = 1,613 metrics) have md + cells coverage; 1,613/1,613 names present, 0 missing, 0 extra. |
| 7 | REPORT.md matches results/table_*.md | ✓ (core) | ~25 numbers verified across §4.1–4.8; §4's 8-table tier grid matches `evaluation_summary.json` per table and total; two new wording slips (m8, m9). |
| 8 | No orphan folders | ✗ | Nested `replications/seasonality_international_evidence/replications/…` with six empty subdirs (iteration-1 CWD slip) — m10. `src/__pycache__` harmless. |
| 9 | Diagnoses paired with fix attempts | ✓ | M1–M4 issue-log entries carry all five fields with before/after metrics; A14 (Table 6 deferral) follows the A1–A13 Decision/Rationale/Impact format; the m1–m7 batch is consolidated (m11, cosmetic). |
| 10 | Tier 2 within 2× magnitude | ✓ | Now explicitly dual-scheme: `rubric_rules` IS the 2× rule ([0.5, 2.0], independently recomputed to an exact per-table match); `repo_rules` disclosed as the looser any-sign-match definition. Both reported in REPORT §4. |
| 11 | Corollary coverage | ✓ | Calendar (T4), size (T5), cross-country correlation (T11), bin-count (T12) computed and verified; intra-country dominance and 14/14 breadth from iteration 1; liquidity (T6) data-blocked under A14; risk factors (T8–10) blocked under M5 (non-actionable). Nothing silently skipped. |
| 12 | No methodology regression (T1/2/3/7 byte-stable) | ✓ | File mtimes: panel.parquet (16:12), cells_t1_t2/table_1/table_2 (16:27), cells_t7/table_7 (17:02), cells_t3/table_3 (17:12) all predate audit1.md (17:35) and were never rewritten; all iteration-2 files are 17:57+. Pre-existing scripts unmodified in iteration 2 (mtimes 16:27/17:01/17:11 are iteration-1). Auditor recompute from the current panel: T2 lag-1 All −0.048472 (t −8.83), Japan −0.056797, Europe −0.023543, Canada −0.064735, lag-3 All −0.000541; T3 EW Panel A y23 nonannual −0.015135/t −5.72, y23 difference +0.013522/t 4.59, y45 all −0.004160; T7 Japan +0.014679/t 4.50, Canada +0.025423/t 4.36 — all Δ = 0.00 vs committed. |

## 4. Issues the agent should have caught (didn't)

1. **§4.6 magnitude range** (m8): the six Y23-difference size-column
   ratios are 0.46–1.30, not 46–89%; two columns exceed the paper. The
   cells were all computed — the prose summary just wasn't re-checked
   against them.
2. **§4.1 "Canada-only"** (m9): the 399 January-1985 rows include one
   Belgian firm-month; a one-line `value_counts()` would have caught it.
3. **The nested empty `replications/` tree** (m10) from an iteration-1
   CWD slip survived both audits until now.
4. Worth crediting: the agent *did* catch and disclose its own artifacts
   this iteration — the NLD-GBR single-month correlation spike (with the
   leave-one-month ρ = −0.08 and the excluded-pair panel mean) and the
   "named pair is NOT the matrix extremum" flags in table_11 are exactly
   the kind of self-skeptical reporting that earns the Tier labels trust.

## 5. Next-iteration prompt

Not required — `requires_iteration: false`. All audit-1 actionable majors
are closed and verified; the remaining issues are four cosmetic minors
(m8–m11) and two externally data-blocked gaps (A14 Table 6; M5 Tables
8–10) that a future run could address by rebuilding the panel with
price/volume columns — neither blocks exit.

## 6. Auditor's notes (free-form)

This iteration did exactly what audit 1 asked, and did it cleanly. The
strongest evidence is the bit-exactness: my independent reimplementation
was written from the docstrings and paper, uses a completely different
code path (pure pandas groupby/rank vs the agent's numpy matrix engine),
and still matched 40+ committed cells to Δ = 0.00 — including t-stats and
calendar-month subsets. That level of determinism means the tier counts,
the corollary tables, and the sensitivity battery are properties of the
cached panel, not of any particular script. The M4 fix is the best kind
of closure: rather than picking one filter semantics and hiding the
ambiguity, the committed script documents both readings (primary
recompute-in-filtered-universe, secondary membership-only), reproduces my
audit-1 numbers exactly under the primary, and approximates the
iteration-1 ad hoc numbers under the secondary — the disagreement audit 1
found is fully explained. The dual-scheme evaluator (M3) resolves the
Tier-2-definition dispute honestly: 82% sign-consistent under repo rules,
57% under the rubric's 2× rule, both in the REPORT with the T2x bucket
retired. The one honest blemish on the numbers themselves is systematic
and well-understood: the annual-lag strategies attenuate everywhere
(5/12 positive months in T4; 4/6 size columns for y23 annual in T5; the
T11 named-pair anchors miss where the extremal pairs differ from the
paper's), while everything built on annual-minus-nonannual differences
and long-horizon reversals replicates — the clean signature of a universe
composition difference, not a methodology defect. The replication's
limiting factor remains what it was at audit 1: FactSet's absence. No
further iteration can improve the 43% rubric-FAIL rate without that
vintage; the loop should exit with a documented partial that now covers
eight tables, 1,613 committed cells, and every computable corollary the
paper reports.
