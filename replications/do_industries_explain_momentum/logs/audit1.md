---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 1
requires_iteration: true
---

# Audit Report 1 — do_industries_explain_momentum

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** A strong, methodologically faithful replication. The paper's unconditional results (industry construction, momentum means, horizon grid, DGTW adjustment) and its central Fama-MacBeth interaction all reproduce at Tier 1 and were independently re-verified from the frozen parquet. Its portfolio-level decomposition claim does NOT hold in the 2026 CRSP vintage — a genuine, thoroughly-diagnosed, non-actionable data limitation. One abstract-level corollary (long/short leg asymmetry) was computed in the data but never reported; it is the single actionable item.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | Every construction detail traces to the paper (PIT SIC industries, 30/30 JT overlapping cohorts, VW fixed formation weights, DT 5×5 + DGTW 5×5×5, plain-iid FM); the one spec error (DGTW window) was caught and fixed in iter 3; paper-silent choices (A1–A18) documented. No methodology bug found. |
| Headline matching | 4 | Raw individual (6,6) 0.0041 vs 0.0043 and industry (6,6) 0.0040 vs 0.0043 both within ~7%; FM industry coef 0.0395 vs 0.0366 within 8%. Sign/shape/magnitude class correct; t-stats ~½ the paper's and the portfolio decomposition claim diverges. |
| Data coverage | 5 | Period 1963-07..1995-07 exact; aggregate universe 4,468/mo vs 4,610 (−3.1%, within 5%); CRSP+Compustat+FF sources match the paper exactly. |
| Concrete result matching | 3 | Independent tally confirms 411 Tier 1 / 330 Tier 2 / 73 FAIL of 814. Pure Tier-1 rate = 50.5% (score-3 band). The agent's headline "91% T1+T2" uses a Tier-2 rule (sign-only) looser than the rubric's 2× bound — 101/330 Tier-2 cells exceed 2×; 2×-bounded T1+T2 = 78.6%. |
| Signal strength | 4 | Primary momentum magnitudes within [0.9,1.1] of the paper (r=0.93–0.95); industry FM coef r=1.08. SB-adjusted cell is 1.52× and significance is systematically ~½, so not all headline cells clear 10%. |
| Corollary | 3 | Horizon grid (T3), DGTW-adjusted industry momentum, random-industry placebo, and the FM interaction all replicate; DT absorption mechanism and the long/short leg asymmetry are gaps. |
| 7 | SUMMARY.md matches results/table_*.md | ✓ | REPORT/Table numbers reproduce from results/*.md and the frozen parquet (5 values spot-checked: 0.0041/2.31, 0.0039/3.00, 0.0040/2.36, FM ind 0.0395/6.95, tier tally). |

**Overall (mean of six):** 3.83 / 5.00 → **REPLICATED** (≥3.0, no dimension = 1).

## 2. Issues by severity

### Blockers (must fix)

None. (The two prep_validation.py layout errors — "no logs/audit*.md" and "SUMMARY.md missing" — are the expected pre-audit state and are resolved by this audit writing audit1.md and SUMMARY.md.)

### Major (should fix)

- [M1] Central portfolio-decomposition claim does not replicate. Industry adjustment does NOT eliminate individual momentum: industry-neutral (6,6) = 0.0039 (t=3.00) vs paper 0.0011 (t=1.01) [3.5×, re-verified by auditor]; excess-industry = +0.0027 vs −0.0007 and high-ind-losers-minus-low-ind-winners = −0.0004 vs +0.0030 are sign-flipped (table_2.md, cells_tables_1_2_3.json `pC_*`). The paper's headline "industries explain individual momentum at the portfolio level" is therefore unsupported in this vintage, even though the Fama-MacBeth version of the claim (Table VI) does replicate.
  - File: results/table_2.md:14-16; REPORT.md §2 (Table II), §6
  - Likely cause: documented 2026 CRSP vintage drift — the vintage contains ~3.5× stronger within-industry stock momentum (engine verified bit-exact; 18/20 industries positive; industry-FE absorbs only 31%; delisting/subperiod/rebalancing/breakpoint/NYSE-scope mechanisms ruled out in iters 4–7).
  - Specific fix: **actionable: false** — external data limitation already documented in assumptions.md (A16) and REPORT.md §5.3/§6. No reproducible construction choice separates the replication from the paper; re-trying chases vintage, not a bug. Keep documented.

- [M2] t-statistics are systematically ~½ the paper's across every strategy type (headline (6,6) t=2.31 vs 4.65; monthly spread std 0.0351 vs implied ~0.018, re-verified by auditor). Significance on marginal (t≈2) cells is materially weaker than the paper reports.
  - File: results/table_2.md:5; REPORT.md §4
  - Likely cause: documented CRSP-vintage variance difference (delisting substitution Δstd +0.0001; uniform across all three subperiods; insensitive to rebalancing, breakpoints, and NYSE/AMEX scope; the paper's own footnote-11 EW anchor reproduces at only 4.7%/yr vs 9.3% — the same ~2× gap in a different cell).
  - Specific fix: **actionable: false** — five construction mechanisms ruled out (iters 5–6); documented vintage limitation in REPORT.md §4.

- [M3] DT size/BE-ME adjustment absorbs none of the momentum spread: SB (6,6) = 0.0044 vs raw 0.0041 (paper: adjustment cuts 0.43→0.29, −14 bp; ours widens slightly); benchmark winner-minus-loser absorption = +0.2 bp (t=0.25) ≈ 0 vs paper +14 bp.
  - File: results/table_2.md:7; REPORT.md §5.2
  - Likely cause: documented vintage effect — the 5×5 sorts are healthy (value premium +1.03%/mo t=4.71; size +0.62% t=1.86) and absorption is statistically zero, not sign-flipped (which would indicate a leg/weight bug). Same family as M1/M2.
  - Specific fix: **actionable: false** — diagnosed as vintage (iter 5/6 diagnostics), documented in REPORT.md §5.2; the industry-level abnormal-return F-test (1.774 vs 1.686) confirms the adjustment works at the industry level.

- [M4] Abstract-level corollary "industry momentum is long-driven; individual momentum is loser-driven" is NOT reported as a result, though the data supports it. The auditor independently computed the individual (6,6) legs: short leg contributes +0.0040/mo (market−loser) vs long leg +0.0002/mo (winner−market) — i.e. individual momentum IS loser-driven, consistent with the paper. The winner/loser leg decomposition for the industry strategy was never produced or compared to the paper.
  - File: results/table_3.md (Wi/Lo columns exist but are never decomposed against the claim); inputs/content.md L35 (abstract bullet 5)
  - Likely cause: not computed — the replicator focused on spreads, not on the leg-level attribution the abstract sells.
  - Specific fix: **actionable: true** — the leg returns already exist in table_3.md / cohorts. Add `results/legs_long_short.md`: winner-leg and loser-leg monthly means for the individual (6,6) and industry (6,6) strategies, each measured against the equal-weighted market, and state which leg drives each spread. Cite abstract L35. The individual side is already verifiable from the cached cohorts.

### Minor (cleanup)

- [m1] Tier-2 labeling diverges from the rubric's 2× magnitude bound. `cell_status()` in src/table_6.py:229-244 (and the equivalent in tables_1_2_3.py) assigns Tier 2 on a **sign match only** (no 2× cap) for non-zero paper values. As a result 101/330 Tier-2 cells (31%) have |ours/paper| > 2, and REPORT.md's "91% sign-and-magnitude hit rate" is looser than the rubric definition. Of the 101, 70 are t-stat cells and 18 are near-zero (economically null) — but 13 are meaningful-magnitude return cells (e.g. pC_industry_neutral_mean 3.51×, pA_sb_minus_ind_mean 3.76×, pA_raw_minus_ind_mean 2.42×). Honest rates: Tier-1 only = 50.5%; Tier-1 + 2×-bounded Tier-2 = 78.6%.
  - File: src/table_6.py:229-244; REPORT.md:9
  - Likely cause: intentional sign-only Tier-2 rule; rubric Q1 (Tier-1-only vs T1+T2) left open.
  - Specific fix: enforce the 2× bound in `cell_status` (or report all three figures — Tier-1, bounded T1+T2, and sign-only T1+T2 — in REPORT.md so the reader can see the convention).

- [m2] Universe benchmark counts are overstated as "reproduce the vintage exactly." Independent recount from the frozen panel gives 1970-06=2,269, 1980-06=4,559, 1990-06=5,812, 1995-06=6,769 vs the claimed 2,270/4,632/5,818/6,775 (log1.md L44, REPORT.md §1). 1980-06 is off by 73 stocks (1.6%); the others by 1–6.
  - File: REPORT.md:20; logs/log1.md:44
  - Likely cause: benchmark measured at the SQL/msenames-join layer before panel deduplication/return filtering; frozen panel is slightly smaller.
  - Specific fix: reconcile (state the layer at which the benchmark was measured) or soften the wording to "within ~1.6%". The aggregate universe (−3.1%) and the coverage conclusion are unaffected.

- [m3] Assumption A18 is duplicated — two "Assumption 18" entries (the 1/99 winsorization decision) appear in assumptions.md.
  - File: preparations/assumptions.md:218-241 and 245-265
  - Specific fix: merge the two A18 entries into one.

- [m4] Sample coverage is borderline: only 59.1% of 1973–1995 panel rows have ALL eight Table-VI variables non-null (gated by Compustat-dependent r_sb/r_dgtw/ln_beme at 71–78%); just under the 60% guideline. This is informational, not a blocker — every monthly FM cross-section is healthy (3,190–3,657 obs; all 271 months fit), and the key signal mom6 is 92% non-null.
  - File: data/panel.parquet; table_6.md avg-obs lines
  - Specific fix: none required; note the Compustat-coverage gate in REPORT.md §1 if desired.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | Table III IM(L,H) grid: industry momentum strongest at L=1 (Wi-Lo 0.0122) and dissipating/reversing by H=24–36, matching the paper's horizon shape. |
| 2 | Headline-magnitude claim | ✓ | Auditor independently recomputed (6,6) raw W-L from panel.parquet: mean 0.0041, t 2.31, std 0.0351 — matches REPORT exactly; mean within 5% of paper's 0.0043. |
| 3 | Sample coverage ≥ 60% | ✓ (borderline) | Key signal mom6 = 92% non-null; FM cross-sections 3,190–3,657/mo. All-8-variable intersection = 59.1% (see [m4]). |
| 4 | Data-source choice justified | ✓ | CRSP msf/msenames/msi/linktable + Compustat funda + FF factors match the paper (L74); paper-silent choices (shrcd 10/11, 6-mo BE lag, breakpoints) documented in A1/A5/A7. |
| 5 | prep_validation.py exit 0 | ✗ → resolves | Pre-audit the validator reports exactly 2 errors (no audit file; no SUMMARY.md) — both are the auditor's own deliverables and clear once audit1.md + SUMMARY.md are written. No prep-contract violations. |
| 6 | All committed tables have results files | ✓ | T1/T2/T3/T6 in tables_to_replicate.json (134/24/240/416 metrics) ↔ results/table_{1,2,3,6}.md all present. |
| 7 | SUMMARY/REPORT match results/table_*.md | ✓ | Five numbers re-derived from the parquet/cells JSON (0.0041/2.31, 0.0039/3.00, 0.0040/2.36, FM ind 0.0395/6.95, full tier tally 411/330/73) — all reproduce. |
| 8 | No orphan folders | ✓ | Slug root clean; no literal-brace / shell-error directories. |
| 9 | Diagnoses paired with fix attempts | ✓ | Every inner-iteration log entry (iters 1–8) carries Diagnosis / Next fix / Before / After / Status; every diagnosed problem has a committed fix or mechanism test. |
| 10 | Tier 2 within 2× magnitude | ✗ | 101/330 Tier-2 cells exceed 2× (sign-only rule, see [m1]). 13 are meaningful-magnitude return cells; the rest are t-stats / near-zero. |

**Additional auditor recomputations (beyond the 10 patterns):**
- Within-industry (industry-neutral) (6,6): independently rebuilt → 0.0039 (t=3.00), confirming the 3.5× divergence is real and engine-exact, not a coding artifact.
- Table VI Panel C (6,1) s1: independently re-ran the monthly winsorized FM OLS → ret +0.0086 (3.91), ind +0.0395 (6.95), exact match to table_6.md; the industry-subsumes-individual interaction reproduces.
- Long/short legs: individual (6,6) short leg +0.0040/mo vs long leg +0.0002/mo → loser-driven (consistent with paper); see [M4].

## 4. Issues the agent should have caught (didn't)

1. **Tier-2 definition vs rubric.** The agent labeled 101 cells Tier 2 that the rubric's 2× bound would call FAIL, then headlined a "91% sign-and-magnitude hit rate." A careful reviewer flags that the honest Tier-1 rate is 50.5% and the 2×-bounded pass rate is 78.6%. The sign-only rule is defensible but should be stated, not implied.
2. **The long/short-leg corollary is in the data but unreported.** The paper sells it in the abstract; the winner/loser legs already exist in table_3.md, and the individual loser-driven result holds on recompute. This is a cheap win the agent left on the table.
3. **Benchmark-count wording.** Claiming the universe counts reproduce "exactly" when the frozen panel is off by up to 73 stocks (1980-06) overstates fidelity; the layer of measurement should be stated.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Do Industries Explain Momentum?" (Moskowitz & Grinblatt 1999) for slug `do_industries_explain_momentum`. The previous agent run completed with verdict **PARTIAL** (audit 1 at `replications/do_industries_explain_momentum/logs/audit1.md`). Read the audit first. Overall score 3.83/5.00 → REPLICATED. The unconditional results and the Fama-MacBeth interaction replicate at Tier 1 and were independently re-verified by the auditor. The portfolio-level decomposition claim does not hold in the 2026 CRSP vintage — this is accepted as a documented, non-actionable data limitation (do NOT re-litigate M1/M2/M3). One actionable item remains.

## Issues to address (priority order)

### [M4] — MAJOR (actionable) — fix this iteration
**Abstract-level corollary not reported.** The paper's abstract (inputs/content.md L35) claims "industry momentum is predominantly driven by long positions, while individual stock momentum is largely driven by selling past losers." You already compute winner-leg and loser-leg returns (table_3.md Wi/Lo columns) but never decompose them against this claim. The auditor re-computed the individual (6,6) legs from data/panel.parquet and found the short leg contributes +0.0040/mo vs the long leg +0.0002/mo — individual momentum IS loser-driven, consistent with the paper. Verify and report the industry strategy's legs too.

**Specific fix:**
1. Add `results/legs_long_short.md`: for the individual (6,6) and industry (6,6) strategies, report winner-leg and loser-leg monthly means measured against the equal-weighted market (winner − market; market − loser), over 1963-07..1995-07, with t-stats. Reuse the cohorts already built in `src/tables_1_2_3.py` (`build_global_cohorts` / `industry_selections`).
2. State explicitly which leg drives each spread and compare to the paper's claim (industry long-driven; individual loser-driven).
3. Add the corresponding cells to a results JSON and cite abstract L35.
4. Verification: the individual side should reproduce loser-driven (short ≫ long, as the auditor found +0.0040 vs +0.0002). Report the industry-side finding honestly whatever its sign.

### [m1] — MINOR — cleanup
Tier-2 labeling uses a sign-only rule (src/table_6.py:229-244), so 101/330 Tier-2 cells exceed the rubric's 2× bound and the "91%" headline is loose. Either enforce the 2× bound in `cell_status`, or report all three rates in REPORT.md (Tier-1 only = 50.5%; 2×-bounded T1+T2 = 78.6%; sign-only T1+T2 = 91.0%) so the convention is explicit.

### [m2] — MINOR — cleanup
REPORT.md §1 / log1.md L44 claim the 1970/1980/1990/1995-06 universe counts reproduce "exactly," but the frozen panel gives 2,269/4,559/5,812/6,769 vs claimed 2,270/4,632/5,818/6,775 (1980-06 off by 73, 1.6%). State the measurement layer (SQL/msenames-join vs frozen panel) or soften to "within ~1.6%". The aggregate (−3.1%) is unaffected.

### [m3] — MINOR — cleanup
Merge the two duplicate "Assumption 18" entries in preparations/assumptions.md (L218-241 and L245-265) into one.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop at 10 and escalate.
- **Do not touch M1/M2/M3.** The auditor has classified the decomposition failure, the t-stat gap, and the DT-absorption gap as documented CRSP-vintage limitations (non-actionable). They are correctly documented in REPORT.md §4–§6; leave them as written.

## Inputs you should read

- `replications/do_industries_explain_momentum/logs/audit1.md` — this audit (full context)
- `replications/do_industries_explain_momentum/inputs/content.md` — paper ground truth (abstract L35 for M4)
- `replications/do_industries_explain_momentum/results/table_3.md` — Wi/Lo legs already computed
- `replications/do_industries_explain_momentum/data/panel.parquet` — cached panel (recompute legs from here)

## What NOT to redo

- Do NOT re-run the full pipeline (stages 1–4) — the panel and tables are frozen and verified.
- Do NOT re-litigate the decomposition/t-stat/DT-absorption findings (M1/M2/M3) — documented vintage limitations.
- Skip re-running prep_validation.py except as a final gate.
- **DO** re-run any sanity check you add for the leg decomposition.

## Deliverables for this iteration

- `results/legs_long_short.md` (+ a cells JSON) — the M4 corollary result, citing abstract L35.
- `REPORT.md` — add the long/short corollary to §2/§5; make the Tier-rate convention explicit (m1); fix the benchmark-count wording (m2).
- `preparations/assumptions.md` — dedupe A18 (m3); append an iteration log entry for M4 (all five fields).
- `SUMMARY.md` — read-only; the auditor owns it.

## Stop conditions

- **[M4] computed and reported + minors addressed** → re-run prep_validation.py → if it passes, declare success; the next audit updates SUMMARY.md.
- If the industry-side leg result contradicts the paper, report it honestly as a vintage finding (do not force-fit).

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is a high-quality, honest replication. The inner-loop trace (9 iterations) is exemplary: every divergence was met with a committed fix or a mechanism test, two spec errors were caught by the worker and corrected (the DGTW momentum window; a mislabeled IBM permno), a non-determinism bug was found and fixed, and the agent resisted the temptation to tolerance-tune — the one substantive convention change (1/99 winsorization, A18) was justified by a concrete outlier diagnosis (r_sb fat tails flipping the ln_size slope), not by chasing a target. I independently re-derived the headline (6,6) spread (0.0041/2.31/0.0351), the within-industry momentum (0.0039/3.00), the Table VI Panel C interaction (ret +0.0086, ind +0.0395), and the full 411/330/73 tally — every number the agent claimed reproduced exactly from the frozen parquet. The substantive finding is that the paper's central portfolio-decomposition claim genuinely does not hold in the 2026 CRSP vintage, and the agent demonstrated this convincingly (engine bit-exact, 18/20 industries positive within-industry momentum, five construction mechanisms ruled out) rather than papering over it — that is exactly how a documented partial should be earned. The two things holding it back from a clean PASS are presentational, not analytical: the Tier-2 label is looser than the rubric's 2× bound (inflating the "91%" headline over a 50.5% pure Tier-1 rate), and one abstract-level corollary (long/short leg asymmetry) sits in the data unreported. Both are cheap to close, hence `requires_iteration: true` on a single actionable major, with the three vintage-driven majors explicitly marked non-actionable.
