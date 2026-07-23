---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 2
requires_iteration: true
---

# Audit Report 1 — value_investing_f_score

**Verdict:** PARTIAL
**Date:** 2026-07-23
**Auditor notes:** Methodologically faithful, independently verified replication of Piotroski (2000) under a user-approved 1988–1996 sample restriction (A1). The cross-sectional regression claim and the annual hedge replicate at Tier 1 against the paper's own same-period benchmark; full-period headline magnitudes attenuate to 16–45% of the paper's abstract numbers (structural, not a bug). Zero blockers; two actionable corollary gaps (Table 5 price/volume partition never computed; analyst-coverage partition feasibility unchecked) trigger the next iteration.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All six checks pass (formulas cited to paper footnotes, prior-year cutoffs, FYE+5-month BHR with zero-delisting rule, standard filter, no lookahead, documented statistical conventions); deviations (A1–A8) documented with justification; no methodology bug found on independent recomputation. Not 5: link broadening (A8) and Welch-vs-pooled t are real, if justified, deviations. |
| Headline matching | 3 | Sign and rough shape of every central claim hold (positive F_SCORE gradient scores 4–6 with a 7–9 plateau, positive hedge, Wilcoxon-significant rightward distribution shift, p = 0.002). Magnitudes match the paper's *same-period* evidence (hedge 0.104 vs 0.091–0.097; F_SCORE coef 0.023–0.031 within the paper's "2.5–3%" claim) but are 16–45% of the full-period abstract numbers (High−All 0.012 vs 0.075; High−Low 0.105 vs 0.230). |
| Data coverage | 2 | Period 9 of 21 formation years (43%, user-approved A1 after oancf verified NULL for all FY<1987 in the comp_202601 vintage); universe 5,736 vs 14,043 (41% of full sample; 80% of the paper's same-period 7,205); same data sources (Compustat/CRSP), vintage difference documented. Not 1: data fully verified, same universe restricted to a sub-period the paper itself reports. |
| Concrete result matching | 3 | Strict Tier 1 = 65/136 = 47.8% (score-2 band); Tier 1+2 = 92.6%; FAIL 10/136 = 7.4%, every FAIL diagnosed. The gap between readings is ~18 structurally unreachable count cells under A1 plus attenuated spreads. Midpoint score, both readings documented. |
| Signal strength | 3 | Signal present and significant (annual hedge t = 3.86, 9/9 positive years; Wilcoxon p = 0.002; Table 7 F_SCORE t = 2.7–3.6). Ratios vs paper: same-period hedge 1.07–1.15 (5-band), FM coefficient 1.12 (4-band), full-period High−Low 0.45 (2-band), full-period High−All 0.16 (1-band). Net 3 — the signal replicates against the valid same-period benchmark but not against the abstract's full-period magnitudes. |
| Corollary | 3 | Replicate: time-series robustness (9/9 positive years), Table 7 control robustness (0 FAILs), two-year horizon (Panel C), size cross-section in direction (small > large; small-cap Wilcoxon p = 0.0065). Fail: Panel D RANK_SCORE (null across 3 pre-tested variants, diagnosed per footnote 12). Never computed: Table 5 share-price/volume partitions (abstract-level claim, fully computable — [M1]) and analyst-coverage partition (IBES is in the ClickHouse catalog, feasibility never checked — [M2]). |

**Overall: (4+3+2+3+3+3)/6 = 3.00 → `REPLICATED`** (bright line: mean ≥ 3.0 and no dimension = 1; met exactly).

## 2. Issues by severity

### Blockers (must fix)

None. All load-bearing claims reproduced from `data/panel.parquet` by the auditor (see §3); no methodology bug found.

### Major (should fix)

- [M1] Corollary 'share-price / trading-volume partitions' not computed in artifacts (actionable: true)
  - File: paper `inputs/content.md:2293-2337` (§4.4.1) and `inputs/content.md:58` (abstract: "not dependent on purchasing firms with low share prices"); missing `results/table_5.md`
  - Likely cause: prep scoped 6 of 8 paper tables (`preparations/tables_to_replicate.json` has table_1/2/3/4/7/appendix_a only) even though `preparations/candidate_assessment.json` declared "Tables 1-8 and Appendix A … all quantitative and reproducible". The price/volume partition needs no data beyond what the pipeline already uses (`prcc_f` is in `funda_base.sql`; `prc`/`vol` verified present in `crsp_202601.msf` per `data_verification.json` req_crsp_monthly_returns).
  - Paper claims: High−Low F_SCORE spreads of 0.246 (low price), 0.258 (medium), 0.132 (high price) — all significant; ~48.4% of high-BM firms in medium/high price buckets.
  - Specific fix: build prior-year full-Compustat price and volume terciles (share price at the FYE *preceding* formation, content.md:2524), partition the existing 5,736-row panel, compute All/Low/High means + High−Low spreads with Welch t per bucket, write `results/table_5.md` with per-cell tiers against the paper's 0.246/0.258/0.132 (full-period reference; same-period = Tier-2 reference under A1).

- [M2] Corollary 'analyst-coverage partition' feasibility never checked (actionable: true)
  - File: paper `inputs/content.md:2550` (no-coverage High−Low 0.277 vs coverage 0.114; 37.8% of firms covered, 1999 I/B/E/S tape); no IBES requirement in `preparations/data_verification.json`
  - Likely cause: assumed unavailable without checking — but `grep` of `references/CLICKHOUSE_CATALOG.json` shows `ibes`, `ibes_*`, `ibesticker` tables exist in the catalog.
  - Specific fix: verify IBES coverage for FY1986–FY1995 in this vintage (non-null analyst counts on the high-BM universe). If ≥60% of panel firm-years are classifiable (covered/not), compute the covered-vs-uncovered High−Low partition as `results/table_5_analyst.md`; if coverage is sparse pre-1990, document the gap in `assumptions.md` as a non-actionable data limitation and mark the corollary SKIP with the verification evidence.

- [M3] Full-period headline magnitudes do not replicate: High−All 0.0117 vs 0.075 (16%), High−Low 0.1045 vs 0.230 (45%), pooled t 1.485 vs 5.590 (actionable: false)
  - File: `results/table_3.md:252-273` (Panel B High−All / High−Low rows); `REPORT.md` §3, §7
  - Likely cause: structural — the user-approved A1 restriction removes the strategy's strongest years (paper's 1979/1983/1984 spreads 0.223/0.349/0.130) and positively selects the Low group through input-completeness filtering; verified data-driven (`results/sanity_checks.md` §8: cfo/dliquid binding drops; A1 impact in `assumptions.md`).
  - Why non-actionable: same comparison made against the paper's own same-period evidence — paper 1988–96 Appendix-A average spread = 0.091 (auditor-computed from the paper's printed annual rows: (0.168−0.036+0.157+0.166+0.070+0.020−0.001+0.126+0.147)/9), ours 0.104 (ratio 1.15, Tier 1). Re-trying cannot move structurally-bound cells; documented in assumptions.md A1 and REPORT.md §7.

- [M4] Panel D RANK_SCORE quintile spread null (−0.0035 vs +0.092) while the paper reports a significant monotonic pattern (actionable: false)
  - File: `results/table_3.md:437-494` (Panel D + sensitivity block)
  - Likely cause: tested — three ranking variants (min-rank, average-rank, sstk-amount rank) all null under a pre-committed adoption rule; paper's footnote 12 attributes this aggregation's inefficiency to sign-blind mechanical ranking; paper's +0.092 draws on a 2.5× larger sample.
  - Why non-actionable: fix attempted with before/after measurement and a pre-committed rule (exactly the iteration discipline the loop requires); further variants would chase noise in a truncated sub-period.

### Minor (cleanup)

- [m1] Tier-2 labels vs the auditor's 2× magnitude bound: the repo's `rep/TOLERANCE_RULES.md` defines Tier 2 as "sign matches but magnitude outside tolerance" (no upper bound), while `audit/SKILL.md` spot-check 10 caps Tier 2 at 2× the paper. Applied strictly, ~20–25 contract cells (e.g., Table 3 Panel B Score-0 mean −0.236 vs −0.061 = 3.87×; High−All means at 0.13–0.30×; most count cells at ~0.4×) would reclassify from Tier 2 to FAIL, raising FAIL from 10 to ~30+ without changing any Tier-1 count (65/136 either way).
  - File: `results/evaluation_summary.md:3` (Tier-2 definition line)
  - Specific fix: add a one-line footnote in `evaluation_summary.md` stating that A1-structural cells are Tier-2-by-construction under the repo definition and would exceed a 2× pattern-match bound; no reclassification needed.

- [m2] Target-count bookkeeping is opaque: the contract has 138 metrics; `results/evaluation_summary.md:13` prints "Total 136 (+3 SKIP)"; log1/REPORT say "139 targets" (138 contract + the task-text `n_1996`, which `results/appendix_a.md:39` correctly flags as outside the contract).
  - File: `results/evaluation_summary.md:13`
  - Specific fix: state the denominator explicitly ("138 contract metrics → 135 evaluated + 3 SKIP, plus 1 task-text extra (n_1996) = 136 tallied").

- [m3] `scripts/prep_validation.py value_investing_f_score` currently exits 1 on exactly two layout errors: missing `logs/audit*.md` and missing `SUMMARY.md` — both created by this audit; re-verified exit 0 after writing (see §3, check 5).

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ (qualified) | Auditor recomputed per-score ma_ret1 means from `data/panel.parquet`: gradient positive and increasing scores 4→6 (0.019/0.082/0.155), plateau at 7–9 (0.080/0.075/0.056) instead of the paper's continued climb; score 0 worst (−0.236). Sign/shape correct, top-end shape attenuated — disclosed in `results/table_3.md`. |
| 2 | Headline-magnitude claim | ✓ | From parquet: All-firms ma_ret1 mean 0.0584 (paper 0.059); raw 0.2286 (0.239); High 0.0702 (n 546) / Low −0.0344 (n 177); spread 0.1045; Welch t 1.485; Wilcoxon p 0.0021; hedge avg spread 0.1040, t 3.861, 9/9 positive years; M2 F_SCORE 0.0276 (t 3.55), M4 0.0227 (t 2.72), FM avg by formation year 0.0313 (t 3.12), M4 FM 0.0282 (t 2.42) — every value matches the results files to the printed precision. |
| 3 | Sample coverage ≥ 60% | ✗ (justified) | Final panel 5,736 = 41% of the paper's 14,043 (below the 60% screen) but 80% of the paper's same-period 7,205; the gap is verified item-coverage sparsity (cfo 3,129 / dliquid 1,546 first-binding drops, `results/sanity_checks.md` §8) plus 547 no-link drops, under the user-approved A1 restriction. Documented, external, not a pipeline defect. |
| 4 | Data-source choice justified | ✓ | ME = prcc_f×csho cites the paper's own Table 1 fn a; market proxy vwretd (A6) cites L314/L560; EQ_OFFER via sstk (A2) cites footnote 16 (L2745); link P+C (A8) cites references/COMPUSTAT.md § CCM with measured before/after coverage (66.9% → 88.5%); all in `preparations/assumptions.md`. |
| 5 | prep_validation.py exit 0 | ✓ (after audit writes) | Pre-audit exit 1 with exactly two errors (missing audit file, missing SUMMARY.md) — the auditor-owned artifacts; re-run after writing this file + SUMMARY.md passes. |
| 6 | All committed tables have results files | ✓ | Contract ids table_1/2/3/4/appendix_a/table_7 ↔ `results/table_1.md`, `table_2.md`, `table_3.md`, `table_4.md`, `appendix_a.md`, `table_7.md` all present with per-cell tier blocks. |
| 7 | SUMMARY/REPORT values match results/table_*.md | ✓ | Spot-checked 8 numbers across REPORT.md §1/§3 against results files + parquet: All-firm mean 0.058, hedge 0.104 (t 3.86), T7 coefs 0.0276/0.0227/0.0313, size shares 58.6/28.4/13.0, Wilcoxon 0.002, signal proportions 0.558/0.733/0.794 — all consistent, no fabricated values. |
| 8 | No orphan folders | ✓ | Slug root contains only data/, inputs/, logs/, preparations/, results/, src/, REPORT.md. |
| 9 | Diagnoses paired with fix attempts | ✓ | The two iteration-born decisions carry full before/after evidence: A4 (average-assets mean −0.0011/std 0.473 vs beginning-assets std 6.238 vs paper 0.5851 → alternative rejected) and A8 (3,957 → 5,736 rows; All-firm mean 0.0805 → 0.0584 ≈ paper 0.059). Registry format (Decision/Rationale/Impact) rather than the five-field log, but substance complete; prep-stage assumptions (A1–A3, A5–A7) are decisions, not diagnosis cycles. |
| 10 | Tier 2 within 2× magnitude | ✗ (qualified) | Tier-2 labels follow the repo's authoritative `rep/TOLERANCE_RULES.md` definition (sign match, no cap) consistently with each contract cell's `tolerance_pct` (auditor re-derived tiers for 9 contract cells — all consistent). But ~20–25 A1-attenuated cells exceed the SKILL's 2× heuristic (see [m1]); FAIL count under strict 2× would be ~30+, Tier 1 unchanged at 65/136. |

**Corollary coverage (spot-check 11):** ✓ every paper corollary is either checked or surfaced as a Major — time-series (Appendix A, ✓), controls (Table 7, ✓), two-year horizon (Panel C, ✓), size cross-section (Table 4, direction ✓ / magnitude attenuated), RANK_SCORE alternative (Panel D, ✗ diagnosed = [M4]), price/volume partition (✗ not computed = [M1]), analyst coverage (✗ feasibility unchecked = [M2]), earnings-announcement returns (Table 8, not committed — Compustat Quarterly tape not in `data_verification.json`; noted in §4, not a Major since the underlying data source is plausibly absent from the catalog).

## 4. Issues the agent should have caught (didn't)

1. **The Table 5 price/volume partition was dropped silently at prep.** `candidate_assessment.json` declared Tables 1–8 "all quantitative and reproducible", then `tables_to_replicate.json` committed to only six — and the price partition is an *abstract-level* claim ("not dependent on purchasing firms with low share prices") requiring only `prcc_f` (already in the funda base) and CRSP `vol` (verified available). No assumptions.md entry records the scoping decision.
2. **IBES availability was never checked.** The analyst-coverage corollary was implicitly treated as out of scope, yet the ClickHouse catalog contains `ibes`/`ibes_*`/`ibesticker` tables. A five-minute catalog grep + coverage query would have settled computability.
3. **The Tier-2 definitional tension was never flagged.** Cells like Panel B Score-0 mean (3.87× the paper) are labeled "Tier 2" without noting they exceed any pattern-match magnitude bound; a one-line footnote ([m1]) would have made the convention explicit and pre-empted this audit finding.
4. **The paper's own same-period spread (0.091) — the single most important benchmark for this restricted replication — appears only in REPORT.md prose**, computed from the paper's printed annual rows. It should be a printed row in `results/appendix_a.md` so the Tier-1 hedge claim is anchored to the like-for-like number inside the artifact itself.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers Among Value Stocks" (Piotroski 2000, JAR) for slug `value_investing_f_score`. The previous agent run completed with verdict **PARTIAL** (audit 1 at `replications/value_investing_f_score/logs/audit1.md`). Read the audit first.

The replication is methodologically verified — the auditor independently reproduced every headline number from `data/panel.parquet` (All-firm mean 0.0584, hedge 0.1040/t 3.86, F_SCORE coefs 0.0276/0.0227/0.0313, Wilcoxon p 0.0021). **Do not touch the frozen pipeline** (`src/main.py`, `src/sql/*`); this iteration adds two missing corollary results and two documentation footnotes.

## Issues to address (priority order)

### [M1] — MAJOR — corollary 'share-price / trading-volume partitions' not computed

The paper claims (abstract + §4.4.1, `inputs/content.md:2293-2337`) that the F_SCORE strategy "is not dependent on purchasing firms with low share prices": High−Low spreads of 0.246 (low-price bucket), 0.258 (medium), 0.132 (high price), all significant; ~48.4% of high-BM firms sit in medium/high price buckets. Share price is measured at the FYE preceding formation (`content.md:2524`); volume partitions use prior-year trading volume, cutoffs from the full Compustat universe independent of BM assignment (`content.md:2295`). No `results/table_5.md` exists.

**Specific fix:**
1. Add price/volume tercile cutoffs computed over the prior-fyear full-Compustat universe (same pattern as `src/sql/bm_size_cutoffs.sql`), using `prcc_f` (already selected in `src/sql/funda_base.sql`) for price and CRSP `vol` (verified present per `preparations/data_verification.json` req_crsp_monthly_returns) or funda `csho`-based turnover for volume. Assign buckets on the existing 5,736-row panel — do NOT rebuild the panel.
2. Compute per bucket: All/Low{0,1}/High{8,9} one-year market-adjusted means, High−Low spread + Welch t, bucket shares (paper: 48.4% medium/high price).
3. Write `results/table_5.md` with a per-cell tier block against the paper's 0.246/0.258/0.132 (full-period reference; under A1 these are Tier-2 references — evaluate sign + same-period plausibility, and say so in the notes).
4. Verification: the paper's qualitative claim is "positive and significant in ALL three price buckets" — check whether the High−Low spread keeps the paper's sign in each bucket and whether the high-price bucket remains positive.

### [M2] — MAJOR — corollary 'analyst-coverage partition' feasibility unchecked

The paper claims (`content.md:2550`) High−Low spreads of 0.277 (no analyst coverage) vs 0.114 (coverage), with only 37.8% of firms covered (1999 I/B/E/S tape). `preparations/data_verification.json` has no IBES requirement, but the ClickHouse catalog (`references/CLICKHOUSE_CATALOG.json`) contains `ibes`, `ibes_*`, `ibesticker` tables — availability for FY1986–FY1995 was never verified.

**Specific fix:**
1. Inspect the catalog tables' schemas and query coverage: count non-null prior-year analyst counts for the high-BM panel firm-years (FY1987–FY1995 formation).
2. If ≥60% of panel firm-years are classifiable as covered/uncovered, compute the two-group High−Low partition (All/Low/High means + spreads + Welch t) and write `results/table_5_analyst.md` citing `content.md:2550`.
3. If coverage is sparse (expected: IBES coverage of small high-BM firms in the late 1980s may be thin), record the verification query and counts as a new assumption entry (Diagnosis / Next fix / Before metric = coverage share / After metric = n/a / Status = non-actionable data gap) and mark the corollary SKIP with evidence in `results/table_5_analyst.md`. Either outcome closes the major.

### [m1] — MINOR — Tier-2 definitional footnote

Add a one-line footnote to `results/evaluation_summary.md` stating that A1-structural cells (counts, attenuated spreads) are Tier-2-by-construction under `rep/TOLERANCE_RULES.md` (sign match, no magnitude cap) and would exceed the auditor's 2× pattern-match bound; Tier-1 count (65/136) is unaffected.

### [m2] — MINOR — target-count bookkeeping

Fix the `results/evaluation_summary.md` total line to state the denominator explicitly: 138 contract metrics → 135 evaluated + 3 SKIP, plus the 1 task-text extra (n_1996) = 136 tallied cells.

### [audit-4] — MINOR — anchor the same-period benchmark in the artifact

Add one printed row to `results/appendix_a.md`: "Paper same-period (1988–1996) average spread, computed from the paper's printed annual rows = 0.091" next to the 0.097 full-period target, so the Tier-1 hedge claim is anchored to the like-for-like number inside the results file itself.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status. A diagnosis without a Next fix is incomplete — do not move on.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.** Don't rediscover failures that are already documented.
- **10-iteration cap per problem.** Hard stop at 10 and escalate to the human. A documented partial is more valuable than a paper-claiming success that does not actually replicate.
- **Diagnoses must be paired with fix attempts (exit gate).** Before declaring `partial`, walk `assumptions.md` and verify every diagnosed problem has at least one log entry with a non-empty `Next fix` line and a before/after metric.
- **Frozen-pipeline discipline:** [M3]/[M4] in audit 1 are non-actionable (A1-structural attenuation; pre-tested Panel D null). Do NOT re-attempt the High−Low spread magnitude or RANK_SCORE variants — report them as carried limitations in REPORT.md only.

## Inputs you should read

- `replications/value_investing_f_score/logs/audit1.md` — this audit (full context)
- `replications/value_investing_f_score/inputs/content.md` — paper ground truth (§4.4.1 at L2293–2337; analyst claim at L2550; price definition at L2524)
- `replications/value_investing_f_score/preparations/` — prep contract (rules, tables selected, data verification, assumptions registry)
- `replications/value_investing_f_score/src/main.py` — current code (extend with table builders; do not alter pipeline outputs)
- `replications/value_investing_f_score/data/panel.parquet` — cached 5,736×43 panel (recompute corollary stats from this + new cutoff queries)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- Skip re-running `scripts/prep_validation.py` — already passed in the previous run (unless you changed a prep artifact).
- Skip re-doing the clickhouse catalog scan — `data_verification.json` is current (extend it with the IBES requirement when you verify M2).
- Skip re-running the full pipeline — `data/panel.parquet` is idempotent and verified; only add the price/volume cutoff query and table builders.
- **DO** re-run any sanity checks you add or modify — they are the gate that catches regressions.

## Deliverables for this iteration

- `replications/value_investing_f_score/src/main.py` — extended with the Table 5 price/volume partition builder (and analyst partition if M2 feasibility passes), logged per issue above
- `replications/value_investing_f_score/results/table_5.md` — new: price/volume partition with per-cell tiers citing content.md L2293–2337
- `replications/value_investing_f_score/results/table_5_analyst.md` — new: analyst partition OR documented feasibility-SKIP with the coverage query evidence
- `replications/value_investing_f_score/results/evaluation_summary.md` — updated tallies + the [m1]/[m2] footnotes; `results/appendix_a.md` — the [audit-4] same-period row
- `replications/value_investing_f_score/preparations/assumptions.md` — append a new iteration log entry for every issue addressed (Diagnosis, Next fix, Before metric, After metric, Status), plus the IBES feasibility finding
- `replications/value_investing_f_score/SUMMARY.md` — read the latest combined assessment to understand the auditor's verdict and score; do NOT edit (the auditor owns this file)
- `replications/value_investing_f_score/REPORT.md` — updated; lead with the data-quality summary (sample period 1988–1996, universe 5,736 vs 14,043 / 7,205 same-period, signal proportions vs paper, headline-magnitude comparison, table count 7, corollaries evaluated this iteration)

## Stop conditions

- **All blockers fixed and verified** → re-run prep_validation.py and any sanity checks → if both pass, declare success or note remaining majors in `REPORT.md`; the next audit updates `SUMMARY.md`.
- **10-iteration cap reached** on a single problem → escalate to the human and write a partial `REPORT.md`; do not edit `SUMMARY.md`.
- **All blockers fixed but majors remain** → declare partial and document the gap in `REPORT.md`. The auditor's `SUMMARY.md` verdict (REPLICATED / FAILED) is independent of this loop decision.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is an unusually disciplined replication record. The inner-loop trace in `logs/log1.md` shows the right instincts in the right order: iteration 1 built and validated the machinery, then *diagnosed before fixing* (two direct replicator-side queries isolating real item sparsity from an overly strict link criterion), committed exactly one structural fix (A8), measured before/after (All-firm mean 0.0805 → 0.0584, landing on the paper's 0.059), and froze the pipeline thereafter. The A4 post-test (beginning-assets ΔTURN std 6.24 vs paper 0.59 → alternative rejected) and the pre-committed Panel D adoption rule are textbook examples of fix attempts that protect against self-deception. Every FAIL cell in §6 of REPORT.md carries an honest diagnosis — including the ones that are genuinely bad news (the 7–9 plateau, the insignificant mean t-stats, the Panel D null), which are stated without spin ("No spin: the headline 7.5%/23% numbers are NOT reproduced here"). Where the replication lands at PARTIAL rather than PASS is a mix of the irreparable and the overlooked: the A1 truncation and its magnitude attenuation are genuinely external (the oancf gap is verified, user-approved, and the same-period benchmark replicates at Tier 1), but the Table 5 price/volume corollary — an abstract-level claim computable from data already in hand — was silently dropped at prep, and IBES availability was assumed away without a catalog check. The next iteration is cheap: two corollary tables and three footnotes, no pipeline changes. The bright-line verdict (REPLICATED at exactly 3.00) is earned on the methodology, the regression evidence, and the annual hedge; it should not be read as endorsing the full-period headline numbers, which this sample cannot reach by construction.
