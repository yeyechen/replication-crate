---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 4
requires_iteration: true
---

# Audit Report 1 — seasonality_international_evidence

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** High-integrity data-substitution replication. Every load-bearing
number the REPORT claims was independently reproduced from `data/panel.parquet`
with a fresh implementation (Table 2 lag-1 in all four samples, Table 3 headline
cells, Table 7 Japan/UK/Canada, the full A13 sensitivity battery). The Tier 1/2/FAIL
tallies are honestly computed — the 143 FAIL count is exactly the sign-flip count —
but the "Tier 2" label is broader than the rubric's 2× definition, and several
computable paper corollaries (Tables 4–6, 11, 12) were not produced.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All construction choices match the paper (eq. 1 FWL, lag sets, EW/VW deciles, intra/inter, difference); FWL verified exact vs OLS-with-dummies (identical to 6 dp); deviations (data substitution, WLS inverse-variance reading of L112 vs literal L122, daily→monthly aggregation) documented and justified. |
| Headline matching | 3 | Central claim (annual − nonannual > 1%/mo at Years 2–5) replicates with correct sign/shape at 66–75% of paper magnitude (Y23 diff +1.35% t 4.59 vs +1.80% t 8.25); lag-1 reversal replicates in sign (1.66× paper magnitude); Year-1 momentum flips sign (−0.53% vs +1.21%). |
| Data coverage | 3 | Effective vintage start 1986-01 vs paper 1985-01 (A11, within ±1–2 yr); firms 19,685 vs 18,117 (+9%), firm-months 1.95M vs 2.44M (−20%); one documented all-encompassing source substitution (FactSet → Compustat Global+NA daily), all alternatives verified unavailable live. |
| Concrete result matching | 3 | Tier 1 = 319/906 (35%) verified exact; strict-rubric Tier 1+2 = 55.5%; agent's scheme (looser Tier 2, separate T2x bucket) gives 77% sign-consistent. All statistically significant paper findings replicate; FAILs concentrate in Y1 contamination (A13), noise-level cells, and thin small-market annual cells. |
| Signal strength | 3 | Headline difference-strategy cells r = 0.66–0.75 (within [0.5, 2.0]); long-horizon nonannual levels r = 0.93–1.06; Japan lag-1 r = 1.11. Year-1 nonannual is a sign flip (excluded from the headline set per the paper's own framing, where the annual-vs-nonannual difference is the central claim). |
| Corollary | 2 | Intracountry dominance (intra/inter decomposition) and cross-country breadth (14/14 sign match, Table 7) replicate exactly. January/size/liquidity/cross-country-correlation/decile-count corollaries (Tables 4, 5, 6, 11, 12) not computed — four are computable from the existing panel; risk-factor corollaries (Tables 8–10) blocked by unavailable French international factors (documented, non-actionable). |
| 7 | SUMMARY.md matches results/table_*.md | ✓ | ~30 headline numbers in REPORT.md verified against `results/cells_*.json` and recomputed from the parquet; four wording-level inaccuracies flagged as minors (m1–m4). |

## 2. Issues by severity

### Blockers (must fix)

None. The replication's claims are substantiated: no fabricated or unverifiable
numbers were found. All spot-checked values reproduce.

### Major (should fix)

- [M1] Corollaries 'calendar-month stability' (Table 4), 'size-group variation'
  (Table 5), and 'liquidity variation' (Table 6) not computed in artifacts,
  though Tables 4 and 5 are computable from `data/panel.parquet` as-is.
  - File: `preparations/tables_to_replicate.json` (committed set is T1/T2/T3/T7 only); paper §IV L1133+ (Table 4), §IV Table 5 description L1218 ("3 different size groups... bottom 30%, top 30%... reevaluated in the beginning of every month"), Table 6.
  - Likely cause: scope limited to pattern documentation + breadth; REPORT §8 documents the exclusion but the size/calendar checks need no external data.
  - Specific fix: extend `src/compute_t3.py` (or add `compute_t45.py`) to emit (a) per-calendar-month Y23 annual/nonannual/difference EW Panel A spreads → `results/table_4.md`; (b) monthly-rebalanced 30/40/30 USD size groups (within-country and pooled) for the Y23/Y45 difference → `results/table_5.md`; Table 6 needs daily volume (`g_secd.vol`) which the panel lacks — either extend the panel SQL with volume or document Table 6 as data-blocked (actionable: false) in `assumptions.md`.
  - actionable: true (Tables 4 and 5; Table 6 conditional on volume availability)

- [M2] Corollaries 'low cross-country correlation of strategy returns'
  (abstract L11; Table 11) and 'decile-count robustness' (Table 12) not computed.
  - File: paper abstract "the strategies are not highly correlated across countries"; Table 12 (5 vs 10 deciles); neither appears in `results/`.
  - Likely cause: the 14/14 country breadth result and the intra/inter decomposition partially substitute for Table 11, but the correlation matrix itself is missing; Table 12 is a one-line variant of the Table 3 sort.
  - Specific fix: from the per-country monthly Y23 difference series already produced by `src/compute_t7.py`, compute the 14×14 correlation matrix and mean pairwise correlation (paper reports ~0.1–0.2) → `results/table_11_correlations.md`; re-run the Table 3 EW Panel A engine with 5 quantiles → `results/table_12_quintiles.md`.
  - actionable: true

- [M3] Tier classification deviates from the rubric's Tier 2 definition and the
  REPORT's pass-rate headline is only valid under the looser repo definition.
  - File: `results/evaluation_summary.json` (T2 = 379 includes cells with magnitude ratio up to 3× and cells below ½ the paper value; T2x = 65 cells with ratio > 3× labeled "Tier 2 (>2×)"); `REPORT.md` §4 "76% of cells pass at pattern level or better".
  - Verified: the tally is internally honest — 143 = exact sign-flip count (per table 0/21/52/70 reproduced), 319 = exact within-tolerance count. But the repo's `rep/TOLERANCE_RULES.md` defines Tier 2 as any sign match, while the audit rubric requires magnitude within 2× (ratio in [0.5, 2]). Under strict rubric rules the split is Tier 1 = 319 (35%), Tier 2 = 184 (20%), FAIL = 403 (45%) — 195 cells the agent calls T2 are rubric-FAIL (ratio > 2 up to 3, or ratio < 0.5), and the 65 "T2x" cells are also rubric-FAIL.
  - Specific fix: recompute `evaluation_summary.json` reporting BOTH schemes (repo-rule tiers and rubric 2× tiers) side by side; replace "76% pass" in REPORT §4 with both numbers (77% sign-consistent under repo rules; 55% Tier 1+2 under the rubric's 2× rule); rename the T2x column so it is not labeled "Tier 2".
  - actionable: true

- [M4] The A13 sensitivity battery (REPORT §6.3) is not committed code — its exact
  numbers are not reproducible, and my independent re-implementation lands on
  somewhat different t-stats for two variants.
  - File: no script in `src/` produces the battery; REPORT §6.3 table claims drop-|ret|>100% → +0.0055 (t 1.91) and drop-|ret|>60% → +0.0119 (t 4.72); auditor's fresh implementation gives +0.0058 (t 2.26) and +0.0149 (t 6.79). Baseline (−0.0053, t −1.62), drop-Canada (+0.0002, t 0.06), and top-50%-cap (+0.0056 vs claimed +0.0059) reproduce near-exactly; the qualitative story is fully confirmed, but the filter-application details (whether excess returns are recomputed after dropping firm-months) are not pinned down.
  - Specific fix: commit `src/sensitivity_y1.py` implementing the four battery variants with the exact filter semantics, emitting the table to `results/sensitivity_y1.md`; the next audit will re-run it.
  - actionable: true

- [M5] Risk-factor corollaries (Tables 8–10: alphas on global/local market, SMB,
  and French international BM/EP/CEP/DP factors) not computed.
  - File: paper §IV.C L1832–1834; REPORT §8 documents the block (catalog `ff.global_factors` carries only daily mktrf/smb/hml/rmw/cma from 1990-07, not the paper's factor set).
  - Likely cause: external data limitation — French's bespoke international value factors are not in the catalog.
  - Specific fix: none available — keep documented in `assumptions.md` and REPORT §8 (this major is non-actionable; a partial factor adjustment using available global mktrf/smb/hml could optionally be added as a supplementary check, but cannot close the paper's spec).
  - actionable: false

### Minor (cleanup)

- [m1] Firm-month count inconsistency between REPORT and table_1.md.
  - File: `REPORT.md` §4.1 ("Firm-months 1985-02..2006-06: 1,950,490") vs `results/table_1.md` Total row (1,950,889 over the 258-month window incl. Jan 1985). Auditor-verified: the 399-row difference is exactly the January-1985 observations.
  - Specific fix: state in REPORT §4.1 that Table 1's total covers 1985-01..2006-06 (1,950,889) while 1,950,490 is the Feb-1985-onwards count matching the paper's regression window.

- [m2] REPORT §4.2 mischaracterizes one T2 FAIL as noise-vs-noise.
  - File: `REPORT.md` §4.2 ("The 21 FAILs are lag-2/3/8 coefficients that are statistically insignificant in the paper itself (|t| ≤ 1.7 ...)"). The paper's lag-3 All-OLS estimate (0.0110, t 2.03, L157) IS significant; ours is −0.0005. Verified: of the 21 flips this is the only flip of a paper-significant All-sample coefficient.
  - Specific fix: amend the sentence to acknowledge the lag-3 All-OLS miss (a genuine single-coefficient deviation, plausibly A11 early-window driven).

- [m3] REPORT §4.4 "noise level" characterization of the Canada Y4-5 difference flip is one-sided.
  - File: `REPORT.md` §4.4 ("Canada flips at noise level: −0.0030, t −0.46; the paper's Belgium/Switzerland cells are ≈0 as well"). Our Canada Y45 difference estimate is indeed noise-level, but the paper's Canada value is +0.0167 (t 2.12) — significant in the paper.
  - Specific fix: reword: "our Canada Y45 difference is −0.0030 (t −0.46) against the paper's +0.0167 (t 2.12) — a genuine miss in the one large market where the paper's Years 4–5 difference is significant."

- [m4] REPORT §2 extreme-return count conflates two sets.
  - File: `REPORT.md` §2 ("68 monthly returns above +1,000%"). Auditor-verified from the parquet: ret_usd > +1,000% = 57 obs; 68 is the two-tailed count beyond [−0.99, 10]. Separately, "68% Canadian" in §6.3 refers to the 253-obs set (ret > 5 or < −0.99) — verified exactly (68.0% Canadian, median ME $5.93M vs $121M panel median).
  - Specific fix: "57 monthly returns above +1,000% (68 beyond [−99%, +1,000%] across both tails)".

- [m5] Prep artifact doc inconsistency on qunit.
  - File: `preparations/data_verification.json` ("prccd x cshoc x qunit") vs `preparations/assumptions.md` A3 (verified `cshoc` is actual shares; NTT $211bn anchor confirms no qunit rescaling).
  - Specific fix: delete "x qunit" from the data_verification description.

- [m6] "Zero FAILs in the Years 2-3 difference row" is true only in the sign-flip sense.
  - File: `logs/log1.md` inner-iteration-2 decision; `REPORT.md` §4.4. Auditor-verified: all 14 countries sign-match, but Austria (+0.0069 vs +0.0226), Spain (+0.0056 vs +0.0217), and Switzerland (+0.0010 vs +0.0070) are below half the paper magnitude — rubric-FAIL (Tier 2 requires ratio ≥ 0.5). The sign claim (14/14) stands.
  - Specific fix: qualify the claim: "14/14 sign match; 7 of 14 within 30% tolerance; 3 small markets (AUT/ESP/CHE) below half the paper magnitude."

- [m7] Tier counts in `evaluation_summary.json` are not produced by any committed code.
  - File: `src/*.py` contains no evaluation logic (grep for "tier" returns nothing); the JSON was produced ad hoc. Auditor reproduced the counts, so this is an auditability gap, not an integrity issue.
  - Specific fix: add a small `src/evaluate.py` that emits `evaluation_summary.json` from `tables_to_replicate.json` + `cells_*.json` (see M3 for the dual-scheme requirement).

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Direction claims (lag profile; annual vs nonannual; breadth) | ✓ (long-horizon & breadth) / ✗ (Y1) | Auditor-recomputed: lag-1 negative in All/Japan/Canada; Y23/Y45 nonannual negative, annual-minus-nonannual positive and significant; Y23 difference positive in 14/14 countries. Year-1 nonannual flips sign (−0.0053 vs +0.0121), documented and root-caused. |
| 2 | Headline-magnitude claim | ✓ | Y23 difference +0.0135 vs +0.0180 (75%); Y45 difference 66%; Y23 nonannual 106%; Y45 all exact (−0.0042/−0.0042); Japan lag-1 within 11%. All recomputed independently from the parquet. |
| 3 | Sample coverage ≥ 60% | ✓ | Firm-months 1,950,490 = 80% of paper's 2,440,681; unique firms 109%; monthly cross-section mean 7,465 vs paper's ~9,500 (79%). |
| 4 | Data-source choice justified | ✓ | A1 documents live-verified unavailability of Datastream (index-only), TRTH (code tables), g_secm (starts 2007); substitution anchored empirically (NTT $211bn; JPY/USD 107.04; euro redenomination cancellation verified in-panel: eurozone Jan-99 ret_usd min −0.47). |
| 5 | prep_validation.py exit 0 | ✓ | Exit 0. Two reported layout errors are the auditor-owned files (audit1.md, SUMMARY.md) written by this audit. |
| 6 | All committed tables have results files | ✓ | T1/T2/T3/T7 each have `results/table_<n>.md` + cells JSON; 906/906 metric names present, 0 missing, 0 extra. Four PNGs present and non-trivial. |
| 7 | REPORT.md matches results/table_*.md | ✓ (core) | ~30 headline values verified against cells JSONs and recomputed; four wording-level slips (m1–m4). Cumulative spreads +333%/−389% verified from `ew_panelA_y23_monthly.csv` (sum of monthly spreads +3.33/−3.89; labeled as a sum, not compounded — acceptable). |
| 8 | No orphan folders | ✓ | Clean tree (only `src/__pycache__`, harmless). |
| 9 | Diagnoses paired with fix attempts | ✓ | A1–A13 each have Decision/Rationale/Impact; F1–F7 carry before/after metrics; A13's "no fix adopted" is a deliberate anti-tweaking decision with a full sensitivity battery and a rejected alternative justification (volatility calibration — auditor-verified: CAN xs-std 0.299 vs paper 0.259; European countries 0.09–0.16 vs paper 0.106–0.19, so the claim holds). |
| 10 | Tier 2 within 2× magnitude | ✗ | Agent's Tier 2 band = sign match + relative error ≤ 200% (ratios up to 3×, and ratios below 0.5); rubric requires [0.5, 2]. 195 agent-T2 cells and all 65 T2x cells are rubric-FAIL. Sign-flip FAIL count (143) is exact under both definitions. See M3. |
| 11 | Corollary coverage | ✗ | Intracountry dominance (intra/inter) ✓ replicates; breadth ✓. Tables 4/5/6/11/12 silently absent from results — M1/M2 for the computable ones, M5 for the factor-blocked ones. |

## 4. Issues the agent should have caught (didn't)

1. **Rubric-vs-repo Tier 2 definition.** The agent invented a "Tier 2 (>2×)"
   bucket without noting that under the audit rubric's 2× rule the honest
   FAIL rate is 45%, not 16%. A careful peer reviewer reports both
   classifications; the REPORT reports only the flattering one (mitigated
   by full disclosure of the T2x column and exact sign-flip counts).
2. **Lag-3 All-OLS is paper-significant** (t 2.03) yet flips sign in the
   replication; the REPORT's "|t| ≤ 1.7" blanket characterization papers
   over this one genuine miss (m2).
3. **Canada Y45 difference** is significant in the paper (+0.0167, t 2.12);
   calling the flip "noise level" without that qualifier misreads the
   paper's own table (m3).
4. **Extreme-return arithmetic**: 57 returns above +1,000%, not 68 (m4).
5. **Sensitivity battery not committed**: the single most load-bearing
   diagnostic for the Y1 failure exists only as prose; two of its four
   t-stats do not reproduce exactly under an equally valid filter
   implementation (M4).
6. **Computable corollaries skipped without gap markers**: Tables 4/5/11/12
   need nothing beyond the existing panel and per-country series; REPORT §8
   frames them as scope decisions rather than flagged gaps (M1/M2).

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Seasonality in the Cross Section of
Stock Returns: The International Evidence" (Heston & Sadka 2010, JFQA) for
slug `seasonality_international_evidence`. The previous agent run completed
with verdict **PARTIAL** (audit 1 at
`replications/seasonality_international_evidence/logs/audit1.md`). Read the
audit first.

The audit independently verified the pipeline: every headline number
reproduced from `data/panel.parquet` with a fresh implementation (Table 2
lag-1 in all four samples; Table 3 EW Panel A cells; Table 7 Japan/UK/Canada;
the A13 battery direction and approximate magnitudes). DO NOT re-derive the
panel or change methodology — it is sound. The remaining work is corollary
tables, evaluation transparency, and wording fixes.

## Issues to address (priority order)

### [M1] — MAJOR — computable corollaries: Tables 4 and 5 (and 6 if feasible)

The paper's Section IV corollaries — not-January (Table 4), size-group
stability (Table 5), liquidity stability (Table 6) — are absent from
`results/`. Tables 4 and 5 are computable from `data/panel.parquet` today.

**Specific fix:**
1. Add `src/compute_t4_t5.py` consuming `data/panel.parquet`.
2. Table 4: per-calendar-month (Jan..Dec) EW Panel A Y23 annual, nonannual,
   and difference spreads (pooled), each with t-stat; compare to the paper's
   claim that the effect is not confined to January (paper Table 4, §IV).
   Emit `results/table_4.md` + cells block appended to a new
   `results/cells_t4.json`; add the metrics (paper values from content.md
   Table 4) to `preparations/tables_to_replicate.json`.
3. Table 5: monthly-rebalanced 30/40/30 USD-size groups (bottom 30% / middle
   40% / top 30% by me_usd, reevaluated each month, per the paper L1218),
   within each country and pooled, for the Y23 and Y45 difference strategies;
   the paper claims the effect persists across size groups. Emit
   `results/table_5.md`.
4. Table 6 (liquidity): needs daily volume; the panel lacks `vol`. Either
   extend `src/sql/month_end_prices.sql` to carry monthly volume (g_secd.vol)
   and compute the paper's turnover/zero-trade sorts, or log a documented
   data-blocked decision in `assumptions.md` (A14) and mark actionable: false.
5. Verify: January's difference-spread contribution should not dominate;
   small/mid/large group spreads should all be positive for Y23 difference.

### [M2] — MAJOR — corollaries: cross-country correlations (Table 11) and quintile robustness (Table 12)

**Specific fix:**
1. From the per-country monthly Y23 difference series already computed in
   `src/compute_t7.py`, compute the 14×14 correlation matrix and mean
   pairwise correlation; the paper/abstract claims strategies "are not
   highly correlated across countries" (expect mean ρ ~0.1–0.2). Emit
   `results/table_11_correlations.md`.
2. Re-run the EW Panel A Table 3 engine with 5 quantiles (top-minus-bottom
   quintile spreads) for the three year groups; the paper (Table 12) reports
   the pattern is robust to decile count. Emit `results/table_12_quintiles.md`.
3. Verify: mean pairwise correlation well below 0.5; quintile spreads keep
   the same signs as decile spreads.

### [M3] — MAJOR — dual-scheme tier evaluation

`results/evaluation_summary.json` uses a Tier 2 band (sign match + relative
error ≤ 200%) that is looser than the audit rubric's 2× rule. The counts are
honest (143 = exact sign-flip count, verified), but the rubric-classified
split is Tier 1 = 319 (35%), Tier 2 = 184 (20%), FAIL = 403 (45%).

**Specific fix:**
1. Write `src/evaluate.py` that recomputes tiers from
   `preparations/tables_to_replicate.json` + `results/cells_*.json` under
   BOTH schemes: (a) repo rules (`rep/TOLERANCE_RULES.md`: Tier 2 = any sign
   match); (b) rubric rules (Tier 2 = sign match AND |ours/paper| in
   [0.5, 2]). Emit both to `results/evaluation_summary.json`
   (`repo_rules` and `rubric_rules` blocks).
2. Update REPORT §4 to report both pass rates (77% sign-consistent under
   repo rules; 55% Tier 1+2 under rubric rules) and rename the T2x column
   so it is not labeled "Tier 2".
3. Verify: repo-rule counts reproduce 319/379/65/143; rubric-rule counts
   reproduce 319/184/403.

### [M4] — MAJOR — commit the A13 sensitivity battery

REPORT §6.3's battery is prose-only; the auditor's fresh re-implementation
matches direction and approximate magnitude but not two t-stats exactly
(drop-|ret|>100%: +0.0058/t 2.26 vs claimed +0.0055/t 1.91;
drop-|ret|>60%: +0.0149/t 6.79 vs claimed +0.0119/t 4.72) because the filter
semantics were never pinned down.

**Specific fix:**
1. Write `src/sensitivity_y1.py` computing the EW Panel A Y1 nonannual
   spread under: baseline, drop-Canada, drop firm-months with |ret_usd|
   above {100%, 60%} (state explicitly whether excess returns are
   recomputed after dropping — the auditor recomputed them), and top-50%
   market-cap subsample. Emit `results/sensitivity_y1.md`.
2. Update REPORT §6.3 numbers to the committed script's output.
3. Verify: baseline −0.0053 (t −1.62); drop-Canada ≈ +0.0002;
   |ret|>60% restores a spread in the +0.012..+0.015 range with t > 4.

### [m1–m7] — MINOR — cleanup

1. m1: REPORT §4.1 — clarify 1,950,490 (Feb-1985-onwards, regression window)
   vs 1,950,889 (Table 1's 258-month window incl. Jan 1985; diff = 399
   January-1985 obs).
2. m2: REPORT §4.2 — acknowledge the lag-3 All-OLS flip is a paper-significant
   cell (0.0110, t 2.03), not noise-vs-noise.
3. m3: REPORT §4.4 — the paper's Canada Y45 difference (+0.0167, t 2.12) is
   significant; reword the "noise level" qualifier to apply to our estimate.
4. m4: REPORT §2 — 57 returns above +1,000% (68 is the two-tailed count
   beyond [−99%, +1,000%]).
5. m5: `preparations/data_verification.json` — delete "x qunit" (A3 verified
   it is unnecessary).
6. m6: qualify "zero FAILs in the Years 2-3 difference row": 14/14 sign
   match, but AUT/ESP/CHE are below half the paper magnitude.
7. m7: covered by M3 (the committed `src/evaluate.py`).

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in
  `assumptions.md` must have all five fields: Diagnosis, Next fix, Before
  metric, After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop at 10 and escalate.
- **Do NOT adopt a microcap filter for Year-1 momentum.** The audit
  endorses A13: the ±60% filter reproduces the paper's cell only because
  it was selected to do so. Keep the documented partial.
- **Do NOT touch the panel or the Table 1/2/3/7 computations** — the audit
  verified them end-to-end. New work is additive (Tables 4/5/11/12,
  sensitivity script, evaluation script, wording fixes).

## Inputs you should read

- `replications/seasonality_international_evidence/logs/audit1.md` — this audit
- `replications/seasonality_international_evidence/inputs/content.md` — paper
  (Table 4 ~L640+; Table 5 L1218; Table 11 abstract L11; Table 12 §IV)
- `replications/seasonality_international_evidence/preparations/` — prep
  contract (extend `tables_to_replicate.json` with the new tables' paper
  values before computing)
- `replications/seasonality_international_evidence/src/compute_t3.py`,
  `compute_t7.py` — reuse the verified sort engines
- `replications/seasonality_international_evidence/data/panel.parquet` —
  cached panel (read-only)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- Skip re-running `scripts/prep_validation.py` until you change a prep
  artifact (you will, when you add tables to `tables_to_replicate.json` —
  then re-run it).
- Skip the ClickHouse catalog scan — `data_verification.json` is current
  (except the qunit wording, m5).
- **DO** re-run any sanity checks you add — they are the gate that catches
  regressions.

## Deliverables for this iteration

- `replications/seasonality_international_evidence/src/compute_t4_t5.py`,
  `src/evaluate.py`, `src/sensitivity_y1.py` (+ Table 11/12 script or
  extension)
- `replications/seasonality_international_evidence/results/table_4.md`,
  `table_5.md`, `table_11_correlations.md`, `table_12_quintiles.md`,
  `sensitivity_y1.md`; updated `evaluation_summary.json` (dual scheme)
- `replications/seasonality_international_evidence/preparations/tables_to_replicate.json`
  — append metrics (paper values + tolerances) for the new tables
- `replications/seasonality_international_evidence/preparations/assumptions.md`
  — append iteration-2 log entries for every issue addressed (Diagnosis,
  Next fix, Before metric, After metric, Status); add A14 if Table 6 is
  data-blocked
- `replications/seasonality_international_evidence/REPORT.md` — updated with
  the wording fixes (m1–m4, m6), the dual-scheme pass rates, and the new
  corollary results; keep the data-quality lead
- `replications/seasonality_international_evidence/SUMMARY.md` — read it for
  the auditor's verdict and scores; do NOT edit (auditor-owned)

## Stop conditions

- **All four majors addressed and verified** → re-run `prep_validation.py`
  and your new sanity checks → declare success or note any remaining gaps
  in REPORT.md; the next audit updates SUMMARY.md.
- **10-iteration cap reached** on a single problem → escalate to the human
  with a partial REPORT.md.
- **M5 (risk factors) cannot be closed** — it is a documented external data
  limitation; keep it in REPORT §8 and exit on the other majors.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is one of the more carefully executed replications in the repo, made
harder than usual by the total absence of the paper's data source. Three
things stand out. First, the methodological discipline is exemplary: the
FX inversion caught by the worker (F1), the euro-redenomination handling
(F2), the NTT/$211bn and JPY/USD anchors, the FWL-vs-OLS exactness check,
and the brute-force cross-validation of both decile engines all reproduce
under independent re-execution — I recomputed a dozen cells from scratch
and every one matched to the reported precision. Second, the A13 decision
to NOT adopt the ±60% filter is exactly the right call: my independent
re-implementation confirms the battery (baseline −0.53%/mo → +1.2–1.5%/mo
once Canadian microcaps are trimmed), which simultaneously proves the
contamination diagnosis and proves that "fixing" Year-1 momentum would be
tweaking-to-fit. The long-horizon cells replicating at Tier 1 under the
identical, filter-free pipeline is the cleanest possible evidence that the
methodology is right and the universe is the problem. Third, the honesty
issues are presentational, not substantive: the 143 FAIL count is the exact
sign-flip count, the T2x bucket is disclosed, and the Tier 1 count is exact;
but the "Tier 2" label is stretched beyond the rubric's 2× bound, and the
report's prose rounds a few edges in the agent's favor (lag-3 significance,
Canada Y45, the extreme-return count). The replication's real limitation —
a 45% rubric-FAIL rate driven by a fundamentally different universe
composition — cannot be fixed without FactSet, and the next iteration's
value is in the computable corollaries (Tables 4/5/11/12) and evaluation
transparency, not in chasing the Year-1 cells.
