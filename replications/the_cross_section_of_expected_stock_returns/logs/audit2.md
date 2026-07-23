---
iteration: 2
verdict: PASS
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — the_cross_section_of_expected_stock_returns

**Verdict:** PASS
**Date:** 2026-07-22
**Auditor notes:** Finishing iteration fully verified. [M1] January-seasonality corollary recomputed independently from `data/panel.parquet` — all 12 reported values reproduce to rounding and all three L2186 claim elements PASS; [m1] 2× magnitude bound is real (unit-tested: hypothetical 3× same-sign non-null cells FAIL) with a correctly-documented near-null exception covering exactly the three flagged cells, counts re-verified unchanged (Tier-1 692 = 107/168/30/199/110/78, Tier-2 86, FAIL 2) and `evaluation_summary.md` is byte-identical to the current code output; [m3] validator allowlist extended and the data/ check passes; [m4] 780-vs-783 clarification verified against the JSON (3 exact-duplicate T1C cells). Two residuals, both cosmetic: [m2] the orphan skeleton RECURRED at a new path (`<slug>/<slug>/`, created 18:22 during this iteration — log2's "slug root clean" claim was false) and was removed by the auditor; three stale wording fragments in REPORT.md/assumptions.md. No methodology change; main tables byte-stable. Zero blockers, zero actionable majors → no further iteration required.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | Frozen this iteration (auditor-verified end-to-end in audit 1); `results/table_1.md … table_6.md` and the five plots are byte-stable (mtimes 16:06–17:50, untouched); `data/` unchanged (16:36). Documented deviations unchanged and justified → 4 not 5, as before. |
| Headline matching | 4.5 | Unchanged from audit 1: all four claims match shape/sign; core coefficients within ~10%; E(+)/P level drift +0.7–1.1 in multivariate specs (documented vintage shift). |
| Data coverage | 4 | Unchanged: exact 330-month period; 2,393 obs/mo vs 2,267 (+5.5%, 5–15% band); same sources with one documented substitute. |
| Concrete result matching | 4 | Auditor re-ran `evaluate.compute_all()` non-destructively: Tier-1 692/780 = 88.7% (107/168/30/199/110/78 exactly), Tier-2 86, FAIL 2 — identical to the regenerable on-disk summary; 70–90% band → 4. |
| Signal strength | 4 | Unchanged: priced-variable headline cells all within 20% of the paper; β null replicates as a null. |
| Corollary | 4.5 | Up from 4: the January-seasonality corollary (L2186) is now computed, surfaced, and auditor-verified 3/3 (Jan 0.606 vs Feb–Dec 0.318 = 1.91×; Feb–Dec t 3.85; gap 0.024); all other in-scope corollaries replicate (subperiod stability 63/63, β ordering, leverage identity, E/P absorption, Table V gradients). Only the documented appendix AI–AIV scope exclusion (different NYSE-only/CRSP-only sample) keeps this below 5. |

**Overall: 4.17 / 5 → REPLICATED** (mean ≥ 3.0 and no dimension = 1).

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

None — [M1] from audit 1 is resolved and verified (see spot-check 11); [M2] (appendix AI–AIV) remains non-actionable (different-sample scope boundary, documented in Assumption 12).

### Minor (cleanup)

- [m1] Orphan skeleton RECURRED at a new path (audit-1 [m2] partially). Actionable: false (already cleaned by auditor).
  - The exact tree from audit 1 (`<slug>/replications/…`) was deleted ✓ (verified: no `replications/` entry at slug root). But a NEW empty skeleton `<slug>/the_cross_section_of_expected_stock_returns/{data,inputs,logs,preparations,results,src}` (0 files) was created at 2026-07-22 18:22:00 — during this iteration, after the claimed cleanup — so log2's "After: slug root clean" is factually false as written.
  - Likely cause: `src/main.py` line 90 calls `LAYOUT.ensure()` at import time; any process run with `REPLICATIONS_PATH` resolving to the slug root itself (e.g. a relative value from CWD = slug root) recreates `<slug>/<slug>/`.
  - Auditor action: removed the empty tree with `rmdir` (verified 0 files first). Slug root is now actually clean.
  - Optional root-cause fix (not required): move `LAYOUT.ensure()` from module top level into `main()` in `src/main.py`, or guard it so importing `main` never creates directories.
- [m2] Three stale wording fragments. Actionable: false (cosmetic; none affects a claim or count).
  - `REPORT.md` §6: "prep_validation.py's name allowlist flags them as unexpected but exits 0" — no longer true after audit-1 [m3]: the allowlist (scripts/prep_validation.py:597–599) now covers all three intermediates and the data/ check passes.
  - `REPORT.md` §5: "plus per-iteration implementation logs (iterations 1–6)" — `preparations/assumptions.md` now has iterations 1–7.
  - `preparations/assumptions.md`: the backfilled Iteration-6 entry (line 407) sits AFTER the Iteration-7 entry (line 339) — chronological order inverted (content is fine; both entries complete).
  - Specific fix if ever touched: update the two REPORT.md sentences; optionally reorder the two assumption entries.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | [M1] January decomposition values | ✓ | Auditor's OWN from-scratch implementation (own monthly 0.005/0.995 winsorization of ln_bm on the valid-return sample, own monthly OLS ret ~ 1 + lnME + ln_bm) from `data/panel.parquet`: Jan 0.6059 (sd 1.8888, t 1.667, n 27), Feb–Dec 0.3178 (sd 1.4357, t 3.853, n 303), full year 0.3414 (sd 1.4766, t 4.200, n 330), ratio 1.9065, gap 0.0236, avg N 2392.9. All 12 values in `results/table_6_january.md` match to rounding; no `src/` code imported. |
| 2 | [M1] Three L2186 claim elements | ✓ | (a) Jan/Feb–Dec = 1.91 ≈ "about twice"; (b) Feb–Dec t = 3.85 ≈ "about 4 standard errors"; (c) gap 0.024 < 0.05 "within 0.05 of the whole year". All three PASS on auditor-recomputed numbers; the quoted claim text matches `inputs/content.md` L2186 verbatim. |
| 3 | [M1] Internal consistency | ✓ | reg(a) == R7 verified (assert in `table_3_6.py`; full-year 0.341/1.477/4.20 = `table_6.md` reg(a) row 0.34/1.48/4.20 = `table_3.md` R7 0.34 (4.20)); `src/table_6_january.py` imports `prewinsorize`/`fm_monthly`/`ts_stats` (no re-implementation); reads only `panel.parquet`. Corollary is in the `evaluation_summary.md` headline section citing L2186. |
| 4 | [m1] 2× bound is real | ✓ | `classify()` unit tests: same-sign 3.0 vs paper 1.0 → FAIL; 2.4 vs 1.0 → FAIL; 1.5 vs 1.0 → TIER2; sign flip on \|paper\|≤0.05 → TIER2; sign flip non-null → FAIL. A hypothetical 3× same-sign non-null cell fails the rule, as required. |
| 5 | [m1] Near-null exception minimal + documented | ✓ | Exhaustive scan of all 86 Tier-2 cells: exactly 2 same-sign cells with \|paper\| > 0.10 beyond 2× — `NEAR_NULL_TARGETS` members R9 E/P dummy t (1.363 vs 0.38) and R11 E(+)/P t (3.190 vs 1.57); R9 E/P dummy slope (0.289 vs 0.06) covered by the \|paper\| ≤ 0.10 threshold. The worker's spec-error flag is correct (the t cells are NOT ≤ 0.10); exception documented in code (evaluate.py:82–99), flags section, and assumptions.md iter-7, with the literal alternative (Tier-2 84 / FAIL 4) spelled out. |
| 6 | [m1] Counts unchanged | ✓ | Auditor re-ran `evaluate.compute_all()` (non-destructive): OVERALL TIER1 692 / TIER2 86 / FAIL 2 / SKIP 280; per-table TIER1 107/168/30/199/110/78 exactly. FAIL list: only Table III R11 E/P dummy slope/t (−0.08/−0.56 vs +0.066/+0.390; \|t\| < 0.6 both sides). Tier-2 citations: vintage-composition 69, boundary-near-zero 10, ocr-inconsistent 7, zero `other`. |
| 7 | [m1] Summary regenerated | ✓ | `results/evaluation_summary.md` (mtime 18:42:37, after the evaluate.py edit) is byte-identical to `build_summary(*compute_all())` output from the current code. |
| 8 | [m2] Orphan directory | ✗→✓ | Audit-1 tree `<slug>/replications/…` deleted ✓; NEW empty skeleton `<slug>/<slug>/` created 18:22 during this iteration (0 files) — removed by the auditor with rmdir; slug root now clean. See [m1] above. |
| 9 | [m3] Validator | ✓ | `scripts/prep_validation.py` allowlist extended (lines 597–599: `portfolio_returns.parquet`, `agg_portfolio_returns.parquet`, `nyse_benchmark_returns.parquet`, with a comment explaining they are agent-computed intermediates); validator run: data/ check passes, exit 0; only remaining layout note was the missing `audit2.md` (this file). |
| 10 | [m4] 780 unique targets | ✓ | `tables_to_replicate.json` has 783 metric entries (110/194/52/225/121/81); exactly 3 exact-duplicate names (T1C avg ln(ME) [All x All], [Small-ME x All], [Large-ME x All]) → 780 unique; REPORT.md §1 now states this. January corollary in REPORT.md §3 with values consistent with the artifacts; §6 documents the three intermediates. |
| 11 | Iteration discipline + no regression | ✓ | assumptions.md iter-7 entry has all five fields for both [M1] and [m1] (incl. the spec-error flag and the literal-alternative counts); iter-6 backfilled with a retroactive note. `results/table_{1..6}.md` and all 5 plots byte-stable from iteration 1; `data/` untouched; ClickHouse reachable in this audit (market-index query executed in 0.0s), so `evaluate.py` ran end-to-end — unlike audit 1, the full evaluator path was executed, not just inspected. |

## 4. Issues the agent should have caught (didn't)

1. The orphan skeleton recurrence. The log claims "After: slug root clean (data, inputs, logs, preparations, results, src, REPORT.md, SUMMARY.md)" — a post-fix `ls` of the slug root would have shown the new `<slug>/the_cross_section_of_expected_stock_returns/` tree created at 18:22 (i.e., by the very iteration doing the cleanup) and falsified the claim. The root cause (import-time `LAYOUT.ensure()` in `src/main.py`) was undiagnosed, which is why deletion alone didn't stick.
2. The two stale REPORT.md sentences (§5 "iterations 1–6"; §6 "allowlist flags them … exits 0") — both directly contradicted by this iteration's own changes ([m3] allowlist extension; iter-7 entry).
3. The inverted iter-7/iter-6 ordering in assumptions.md (cosmetic, but visible on any read-through of the iteration log).

## 5. Next-iteration prompt

**No further iteration is required.** `requires_iteration: false`. All audit-1 issues are resolved and verified; the residuals (two stale REPORT.md sentences, inverted assumptions.md entry order, optional `LAYOUT.ensure()` import-time guard) are cosmetic and do not affect any claim, count, or artifact value. If the replication is ever reopened for an unrelated reason, the optional cleanups are:

1. REPORT.md §6: replace "prep_validation.py's name allowlist flags them as unexpected but exits 0" with "prep_validation.py's allowlist covers these names (scripts/prep_validation.py) and the data/ check passes".
2. REPORT.md §5: "iterations 1–6" → "iterations 1–7".
3. preparations/assumptions.md: move the backfilled Iteration-6 entry above Iteration-7 for chronological order.
4. src/main.py: move `LAYOUT.ensure()` out of module import time (into `main()`) so importing the module can never recreate stray layout skeletons.

## 6. Auditor's notes (free-form)

The finishing iteration did exactly what it should: one additive artifact, one documented rule clarification, zero methodology changes. Two pieces of work deserve specific credit. First, `src/table_6_january.py` imports the existing `prewinsorize`/`fm_monthly`/`ts_stats` machinery rather than re-implementing it — the corollary is therefore guaranteed to use the identical winsorization and reg(a) specification as Tables III/VI, and the auditor's independent recomputation (own winsorization, own OLS, panel-only) reproduces all 12 reported numbers to rounding; the 3/3 claim-element PASS is robust. Second, the rep-worker caught a genuine spec error in the audit-1 suggested fix: the |paper| ≤ 0.10 near-null threshold does not cover the two t-stat cells (|paper| = 0.38 and 1.57), and the replicator's resolution — an explicit `NEAR_NULL_TARGETS` set with precedent (`OCR_BETA_T_SPECS`), full documentation in the flags section, and the literal alternative's counts (Tier-2 84 / FAIL 4) spelled out — is the right call; I confirm the exception set is minimal (an exhaustive scan of all 86 Tier-2 cells finds exactly those two same-sign beyond-2× cells) and that no claim is affected either way. The evaluator counts were verified more strongly than in audit 1: ClickHouse was reachable in this audit, so `compute_all()` (including the Table-I post-ranking-β market-index query) ran end-to-end, and the on-disk `evaluation_summary.md` is byte-identical to the current code's output. The only blemish is the recurring orphan skeleton — deleted by the auditor this time; the durable fix is the one-line `LAYOUT.ensure()` relocation noted above. Final state: 692/780 Tier-1 (88.7%), 86 Tier-2 (all cited, all now within the enforced 2× bound or the documented near-null exception), 2 FAIL (sign flips on a null), four central claims plus the January-seasonality corollary replicated, and every deviation group (vintage composition, NYSE mean shift, R8–R11 β OCR inconsistency) still evidenced as in audit 1. This replication is complete.
