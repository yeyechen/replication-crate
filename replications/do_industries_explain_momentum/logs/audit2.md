---
iteration: 2
verdict: PASS
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — do_industries_explain_momentum

**Verdict:** PASS
**Date:** 2026-07-22
**Auditor notes:** The single actionable major from audit 1 ([M4], the abstract-level long/short leg-asymmetry corollary) is resolved and independently re-verified: all three claims — individual momentum loser-driven, industry momentum long-driven, (1,1) industry strategy balanced — reproduce, with spread integrity locked to the frozen, auditor-verified spreads (0.004135/2.311; 0.003972/2.359). My own from-scratch recomputation of the industry legs (written independently from data/bin_rets.parquet, not reusing the replication's engines) matches the worker's numbers to six decimals. The Wi−Mid/Mid−Lo magnitude/ordering disagreement is disclosed honestly as a vintage finding. Minors m1–m3 are closed. The three vintage-driven majors (M1–M3) were correctly left untouched per the audit-1 classification. No new blockers or actionable majors. Corollary score moves 3 → 4; overall 3.83 → 4.00.

## 1. Scores

| Dimension | Score | Δ | Key finding |
|-----------|------:|---|-------------|
| Methodology | 4 | — | Unchanged from audit 1: every construction detail traces to the paper (PIT SIC industries, 30/30 JT overlapping cohorts, VW fixed formation weights, DT 5×5 + DGTW 5×5×5, plain-iid FM); paper-silent choices A1–A18 documented; no methodology bug. The M4 add-on reuses the same verified engines with the paper-grounded benchmark r̄ (L246; footnote 14), introducing no new deviation. |
| Headline matching | 4 | — | Raw individual (6,6) 0.0041 vs 0.0043 and industry (6,6) 0.0040 vs 0.0043 within ~7%; FM industry coef 0.0395 vs 0.0366 within 8%; sign/shape/magnitude class correct. The abstract's leg-asymmetry headline now also matches directionally, reinforcing but not changing the score (t-stats still ~½ the paper's; portfolio decomposition diverges). |
| Data coverage | 5 | — | Period 1963-07..1995-07 exact; aggregate universe 4,468/mo vs 4,610 (−3.1%, within 5%); CRSP+Compustat+FF sources match. The m2 fix now names the measurement layer (SQL/msenames-join exact; frozen panel 1–73 stocks lower per date), strengthening the documentation. |
| Concrete result matching | 3 | — | 411 Tier 1 / 330 Tier 2 / 73 FAIL of 814 (re-tallied by auditor: T1+T2+T3 = 215/153/30, T6 = 196/177/43). Pure Tier-1 rate 50.5% (50–70% band → score 3). REPORT now states all three conventions explicitly (50.5% / 80.7% with the audit's stricter 78.6% in parentheses / 91.0% sign-only) — transparency improved; the Tier-1-anchored band is unchanged. |
| Signal strength | 4 | — | Headline magnitude ratios 0.93–1.08 (within [0.8,1.2]); SB-adjusted cell 1.52× and significance systematically ~½, so not all headline cells clear 10%. The leg contributions corroborate the signal but are supporting, not headline, cells. |
| Corollary | 4 | +1 | Audit-1's two gaps were the DT-absorption mechanism and the leg asymmetry. The leg asymmetry is now closed — all three abstract-corollary claims verified (loser-driven +0.0040 vs +0.0002; long-driven +0.0023 vs +0.0017; balanced |Δ|=0.0010) — leaving one well-explained vintage deviation (DT absorption ≈0) plus one honestly-reported magnitude-level disagreement (Wi−Mid/Mid−Lo ordering). "Most replicate, 1–2 minor deviations, well-explained" → 4. |

**Overall (mean of six):** 4.00 / 5.00 → **REPLICATED** (≥3.0, no dimension = 1; up from 3.83 in audit 1).

## 2. Disposition of audit-1 items

### Majors

- **[M1] Portfolio-decomposition failure — NON-ACTIONABLE, correctly untouched.** Per the audit-1 classification (documented 2026 CRSP vintage drift), left as written. Frozen cells re-checked: industry-neutral (6,6) = 0.003858 (t=3.00) vs paper 0.0011 (t=1.01); excess-industry and high-ind-losers cells still sign-flipped (cells_tables_1_2_3.json `pC_*`, unchanged). REPORT §2/§5.3/§6 documentation intact.
- **[M2] Systematic t-stat gap — NON-ACTIONABLE, correctly untouched.** Headline (6,6) t=2.31 vs 4.65 unchanged; REPORT §4 documentation intact.
- **[M3] DT absorption ≈ 0 — NON-ACTIONABLE, correctly untouched.** REPORT §5.2 documentation intact; the remaining corollary gap is now the sole basis for the (improved) corollary assessment.
- **[M4] Leg-asymmetry corollary unreported — RESOLVED.** Verified by the auditor:
  - `results/legs_long_short.md` + `results/cells_legs.json` created; cite abstract L35, §IV.A L1121 (Wi−Mid 0.36 vs Mid−Lo 0.07), §IV.B L1159 (balanced (1,1)) — all three citations checked against inputs/content.md and accurate.
  - **Individual (6,6):** short leg r̄−L = +0.003959 (t=2.64) vs long leg W−r̄ = +0.000176 (t=0.11) → loser-driven, matching the paper and the audit-1 independent recompute (+0.0040/+0.0002).
  - **Industry (6,6):** Wi−r̄_ind = +0.002261 (t=2.34) vs r̄_ind−Lo = +0.001711 (t=1.89) → long-driven, matching the paper. **Auditor independently reimplemented the industry legs from bin_rets.parquet (own ranking/overlap code, not the replication's engines) and reproduced Wi=0.012423, Lo=0.008451, both contributions, and both t-stats to six decimals; r̄_ind = 0.010161 exact.**
  - **Industry (1,1):** long +0.005592 (t=5.09) vs short +0.006632 (t=6.15), |Δ| = 0.0010 ≤ 0.002 → balanced, matching §IV.B. Independently reproduced exactly.
  - **Integrity:** spread from legs = 0.004135/2.311 (individual) and 0.003972/2.359 (industry), asserted in-script and reproduced on the auditor's re-run of `src/legs_long_short.py` (deterministic); leg W−L equals the spread engine to 2.8e-17; Wi−Mid/Mid−Lo cells match cells_tables_1_2_3.json `pA_L6_H6_wimid/midlo` to <1e-12 (auditor confirmed the JSON values directly: 0.0014734 / 0.0024986).
  - **Honest caveat preserved:** the paper's buy/sell split ordering (Wi−Mid 0.0036 > Mid−Lo 0.0007) is reversed in this vintage (0.0015 < 0.0025; both same-sign Tier 2 under the replication's convention) — disclosed in legs_long_short.md, REPORT §2, log2, and assumptions.md as a magnitude-level vintage finding. The market-relative decomposition supports the paper's directional claim.
  - `cells_legs.json`: 3/3 binary claims PASS, 4 contribution cells corroborate, 2 split cells Tier 2.
  - assumptions.md iteration entry carries all five fields (Diagnosis / Next fix / Before / After / Status: resolved).

### Minors

- **[m1] Tier-rate convention — CLOSED (with residual note [n1]).** REPORT.md bottom line now states all three rates explicitly: Tier-1 only 50.5%; Tier-1 + 2×-bounded Tier-2 80.7% (657/814) with "the audit's stricter symmetric variant gives 78.6%"; sign-only 91.0%. Auditor re-tally: exactly 101 Tier-2 cells exceed 2× (70 t-stats + 18 near-zero controls at paper=0.0001 + 13 meaningful-magnitude returns — the same breakdown as audit 1), giving the strict rate 640/814 = 78.6%; counting the 27 paper-zero cells as bound-violations gives 75.3%. The worker's 84/80.7% sub-count excludes 17 of the 18 near-zero cells from the violation set, so its label ("magnitude stays within 2×") is slightly loose for those cells — but the verified strict figure (78.6%) is disclosed and attributed, which is what m1 asked for. See [n1].
- **[m2] Universe-count wording — CLOSED.** REPORT.md §1 now names the layer: counts match the vintage exactly at the SQL/msenames-join layer (2,270/4,632/5,818/6,775), and the frozen analysis panel runs 1–73 stocks lower per date (1980-06: 4,559, −1.6%). log1.md L44 carries an inline audit-1 correction bracket. Aggregate (−3.1%) unchanged.
- **[m3] Duplicate A18 — CLOSED.** Single A18 entry at preparations/assumptions.md:218 merging the winsorization decision, the fat-tail diagnosis, and the residual ret_1_1 finding; no second "Assumption 18" remains.
- **[m4] Compustat-coverage gate (informational) — no action required** per audit 1; left as is.

## 3. Issues by severity

### Blockers (must fix)

None. (prep_validation.py's single pre-audit error — "logs/audit2.md missing" — is the expected pre-audit state and clears with this file + the SUMMARY.md overwrite.)

### Major (should fix)

None actionable. M1–M3 remain documented, non-actionable CRSP-vintage limitations (claim-level partial on the portfolio decomposition; means and the FM interaction replicate).

### Minor (cleanup)

- **[n1] The "80.7%" 2×-bounded headline is marginally loose.** REPORT bottom line: "Tier 1 + Tier-2 cells whose magnitude stays within 2× the paper's value = 80.7% (657/814; the audit's stricter symmetric variant gives 78.6%)". Auditor's strict recount (|ours/paper| > 2 over all non-zero-paper Tier-2 cells, including the 18 paper=0.0001 control cells) gives 101 violations → 78.6%; the 80.7% count drops 17 near-zero cells from the violation set. Both figures are disclosed and the stricter one is attributed to the audit, so this is presentational, not substantive. Optional polish: anchor the middle figure on 78.6% and describe 80.7% as the "excluding economically-null (<5 bp) cells" variant.
- **[n2] Nested cwd-quirk directories persist** (`replications/do_industries_explain_momentum/logs/stage4_run.log`; empty `src/replications/do_industries_explain_momentum/`). Pre-existing harness artifacts of the `paper_layout` cwd-resolution quirk disclosed in REPORT §6 (pipeline must launch from repo root); not introduced by iteration 2. Optional hygiene: remove when the harness is fixed.
- **[n3] `cells_legs.json` Tier-2 labels for Wi−Mid/Mid−Lo use the replication's sign-only convention** (30% band → Tier2). Under the rubric's 2× bound, Mid−Lo (3.57×) would be FAIL; the ordering reversal is disclosed in prose everywhere it appears, so no reader is misled. Informational.

## 4. Verification spot-checks (recomputed by auditor, iteration 2)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | M4: individual (6,6) loser-driven | ✓ | Short +0.003959 (t=2.64) vs long +0.000176 (t=0.11); spread integrity 0.004135/2.311 asserted and reproduced on re-run; consistent with audit-1's independent +0.0040/+0.0002. Auditor's own naive implementation (different missing-return convention) also yields loser-driven (short +0.0064 vs long −0.0006), confirming the attribution is convention-robust. |
| 2 | M4: industry (6,6) long-driven | ✓ | **Auditor's fully independent implementation from bin_rets.parquet reproduces Wi=0.012423, Lo=0.008451, long +0.002261 (t=2.34), short +0.001711 (t=1.89), spread 0.003972 (t=2.359) to six decimals** under the formation-inclusive cohort convention (the skip-month variant does not reproduce the frozen spread, confirming the Panel-A convention used). |
| 3 | M4: industry (1,1) balanced | ✓ | Independent recompute exact: long +0.005592 (t=5.09), short +0.006632 (t=6.15), |Δ|=0.001040 ≤ 0.002; spread 0.012224 (t=6.72) matches Table III (1,1). |
| 4 | Benchmarks | ✓ | r̄ = cross-sectional EW mean = 0.012891/mo reproduced exactly (T=385; corr vs panel ew_mkt 0.9992); r̄_ind = 0.010161/mo reproduced exactly. |
| 5 | Paper citations | ✓ | inputs/content.md L35 (abstract leg-asymmetry bullet), L1121 (Wi−Mid 0.36 vs Mid−Lo 0.07; "mostly on the buy side"), L1159 ("equally driven by the long and the short sides") all match the replication's claims. |
| 6 | Internal consistency | ✓ | cells_legs Wi−Mid/Mid−Lo = cells_tables_1_2_3 pA_L6_H6_wimid/midlo (0.0014734/0.0024986); contributions sum to spreads (r̄ cancels); script asserts <1e-12 vs frozen cells and passes. |
| 7 | Determinism | ✓ | Auditor re-ran src/legs_long_short.py: identical outputs, all asserts (spread integrity, frozen-cell cross-check) pass. |
| 8 | Frozen tables unchanged | ✓ | Re-tallied 411/330/73 of 814 (T1+T2+T3 215/153/30; T6 196/177/43); per-table aggregates 105/18/11 · 10/8/6 · 100/127/13 · 196/177/43 reconcile. Iteration-2 touched only legs artifacts, REPORT.md, assumptions.md, log files. |
| 9 | Strict 2× recount | ✓ | 101 Tier-2 cells exceed 2× (70 t-stats + 18 near-zero + 13 returns) → strict 2×-bounded rate 78.6% (audit-1 figure verified to the cell); 75.3% if the 27 paper-zero cells also count as violations. REPORT discloses 78.6% alongside its 80.7% variant. |
| 10 | Audit-1 dispositions | ✓ | M1–M3 untouched and documented; m1–m3 closed (details in §2); assumptions.md M4 entry has all five fields; A18 single entry. |
| 11 | prep_validation.py | ✗ → resolves | Exactly 1 error pre-audit (missing audit2.md) — this audit's deliverable; clears on write + SUMMARY overwrite. No prep-contract violations. |
| 12 | Hygiene | ✓ | No SCORE.md; slug root otherwise clean; the two nested cwd-quirk directories are pre-existing disclosed harness artifacts ([n2]), not new. |

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are closing out the replication of "Do Industries Explain Momentum?" (Moskowitz & Grinblatt 1999) for slug `do_industries_explain_momentum`. Audit 2 (`replications/do_industries_explain_momentum/logs/audit2.md`) returned verdict **PASS**, overall **4.00/5.00 → REPLICATED**, blocker_count=0, actionable_major_count=0, requires_iteration=**false**. All actionable items from audit 1 are resolved and independently re-verified: the leg-asymmetry corollary (individual loser-driven; industry long-driven; (1,1) balanced) now reproduces with spread integrity locked to the frozen spreads, and minors m1–m3 are closed. M1–M3 remain documented, non-actionable CRSP-vintage limitations — do NOT re-litigate them.

**No further iteration is required.** If you are nonetheless invoked:

1. Read `logs/audit2.md` §3 for the three informational minors ([n1]–[n3]) — all optional polish, none blocking:
   - [n1] optionally anchor the middle pass-rate figure on the audit-verified 78.6% and label 80.7% as the "excluding economically-null cells" variant (REPORT.md bottom line).
   - [n2] optionally remove the nested cwd-quirk directories (`replications/do_industries_explain_momentum/` and `src/replications/` inside the slug) once the `paper_layout` cwd quirk is fixed at the harness level.
   - [n3] informational only (cells_legs.json Tier-2 labels follow the replication's sign-only convention; the reversal is disclosed in prose).
2. Do NOT re-run the pipeline or the frozen tables. Do NOT touch data/ or results/table_*.md / cells_*.json (cells_legs.json may be regenerated only via `src/legs_long_short.py`, which is deterministic).
3. After any optional edit, re-run `uv run python scripts/prep_validation.py do_industries_explain_momentum` from the repo root as the final gate; it must exit 0.
4. SUMMARY.md is auditor-owned — do not edit it.

**Stop condition:** no required work; declare success on entry unless an optional polish item is explicitly requested.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

Iteration 2 did exactly what the audit-1 prompt asked, with the right discipline: one worker spawn for the single actionable item (M4), no re-litigation of the vintage-driven majors, no pipeline rerun, and the minors closed by the replicator without a worker. The M4 execution is exemplary in the ways that matter for credibility. (1) The leg decomposition is not a new engine — it reuses the frozen cohorts and self-verifies against them, asserting bit-level equality of the leg-derived spread with the frozen Table II/III spreads (0.004135/2.311, 0.003972/2.359), so the corollary cannot drift away from the audited results. (2) The one place where the replication disagrees with the paper at the magnitude level — the (6,6) buy/sell split ordering, Wi−Mid 0.0015 < Mid−Lo 0.0025 vs the paper's 0.0036 > 0.0007 — is reported up front in every artifact as a vintage finding rather than buried or force-fit; the directional abstract claim is supported by the market-relative decomposition, and that distinction is stated precisely. (3) My own from-scratch recomputation of the industry legs — written independently from bin_rets.parquet with my own ranking and overlap logic — landed on the worker's numbers to six decimals, which is about as strong a verification as this corollary admits; and even my naive individual-leg implementation, which disagrees with the frozen engine on levels because of a different missing-return convention, still classifies individual momentum as loser-driven, so the attribution is convention-robust. The only blemish is presentational: the middle pass-rate figure (80.7%) is computed with a slightly looser exclusion than its label implies — the strict 2×-bounded rate is the 78.6% I verified in audit 1, cell for cell (70 t-stats + 18 near-zero + 13 returns over the bound) — but since both figures are disclosed and the stricter one is attributed to the audit, this is a wording note, not a finding that warrants another loop. Net: the replication closes at a documented claim-level partial (the portfolio decomposition genuinely does not hold in the 2026 CRSP vintage, demonstrated rather than papered over) with everything computable now computed and reported — PASS, requires_iteration=false.
