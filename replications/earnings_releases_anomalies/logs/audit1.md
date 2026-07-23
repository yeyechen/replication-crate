---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 1
requires_iteration: true
---

# Audit Report 1 — earnings_releases_anomalies

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** Faithful, well-documented PEAD replication (Foster–Olsen–Shevlin 1984). All central qualitative claims independently reproduce from the cached parquet; 76% of 798 committed cells are Tier 1 and 82% Tier 1+2 (tally re-verified cell-by-cell). The single systematic deviation — drift magnitudes in [+1,+60] attenuated to ~0.50 of the paper — is correctly diagnosed as a data-vintage (restated-earnings) effect; I stress-tested that diagnosis against actionable alternatives (σ-window, FEP-assignment, alignment, aggregation bugs) and it holds. The one actionable gap is that the paper's subsample-stability (Table 5) and market-adjusted robustness (Tables 8–9, eq. 17) corollaries were not committed as per-cell tables.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | FE models 1–4 (eqs. 8–13), u = R_i − R_p (eq. 15), CAR sum (eq. 18), prior-quarter FEP cutoffs, two-stage simulation — all traced and point-in-time; no look-ahead; deviations (σ floors, Dimson-β-for-SW, non-NYSE breakpoint assignment, 251-day M4 window) are minor and documented. No methodology bug found. |
| Headline matching | 3 | Sign, shape, and R² hierarchy all match (drift in M1/M2, none in M3/M4; FEP R² 0.726 vs 0.810 = within 10%); but the headline drift *magnitude* is attenuated ~50% (M2 [+1,+60] spread 3.13 vs 6.31; β₁ 0.33 vs 0.67). |
| Data coverage | 3 | Exact period (1974Q1–1981Q4, 32 quarters), same sources (Compustat fundq + CRSP dsf/dsenames/ccmxpf_lnkhist/dsi), zero substitutions; but universe is +47% larger (3,024 vs 2,053 firms), a documented vintage/survivorship effect. |
| Concrete result matching | 4 | 608/798 = 76.2% Tier 1 (82.3% Tier 1+2), 141 FAIL — independently reproduced with the agent's exact tier function; every FAIL is classified (vintage / near-zero sign flip / M3 spurious / one paper anomaly). |
| Signal strength | 3 | Signal is unambiguous (sign, significance, monotonicity, R² hierarchy all replicate; paper's famous 81% R² within 10%); extreme drift cells attenuated to ratio ~0.44–0.50 (borderline 2/3). |
| Corollary | 3 | Cross-sectional size variation replicates (Table 6, committed); subsample/temporal stability holds (both subperiods spread ≈3.0–3.2%, 26/27 quarters positive) but the paper's Table 5 is not committed cell-by-cell; market-adjusted robustness (Tables 8–9) not computed. |

Spot-check 7 (SUMMARY/REPORT ↔ results): ✓ — every REPORT.md number I checked (M2 [+1,+60] series, eq.16 R²/β, FE tails, Table 3 decile returns, tier tally) reproduces exactly from `data/panel.parquet` / `results/cells_iter2.csv`.

## 2. Issues by severity

### Blockers (must fix)

- None. The replication is trustworthy on its headline claims; no methodology bug, no coverage failure, no fabricated numbers.

### Major (should fix)

- [M1] Corollary / robustness predictions not computed as committed per-cell tables. (actionable: true)
  - File: `preparations/tables_to_replicate.json` (committed ids = T1, T3, T4, T6, T7 only); `results/` has no `table_5.md` or `table_8*.md`/`table_9*.md`.
  - Evidence: the paper's **Table 5** (subperiod stability: drift persists across 1974–77 vs 1978–81 subperiods) and **Tables 8–9** (robustness under the equally-weighted market benchmark, eq. 17) are secondary predictions that follow from the main result. Subsample stability *holds substantively* — I recomputed the M2 [+1,+60] FEP10−FEP1 spread for 1974Q1–1977Q4 (= 3.02) and 1978Q1–1981Q4 (= 3.21), both positive, and 26/27 quarters have a positive spread; `results/quarterly_car_m2.png` covers the same claim graphically — but it is not a committed, per-cell-evaluated table. Market-adjusted robustness (eq. 17) is entirely uncomputed.
  - Likely cause: table selection (Stage 4) scoped five tables and treated subperiod/robustness checks as out of scope (A13 notes the eq. 17 benchmark is "not in the selected replication set").
  - Specific fix: add the paper's Table 5 (split the 32 quarters into the paper's reported subperiods, compute pooled M1/M2 CARs for [−1,0]/[−60,0]/[+1,+60], compare cell-by-cell to the paper) → `results/table_5.md`; and, since `crsp_202601.dsi.ewretd` is already verified available (`data_verification.json`, A13), compute the eq. 17 market-adjusted CAR (u = R_i − R_M) for Tables 8–9 → `results/table_8_9.md`. Register both in `tables_to_replicate.json` with paper targets + tolerances and extend `cells_iter2.csv`.

### Minor (cleanup)

- [m1] `preparations/assumptions.md` iteration log not closed out for inner iteration 3.
  - File: `preparations/assumptions.md:119-133` (the two Iteration-2 entries — SW-beta and stars — still carry `After metric: (iteration 3)` unfilled and `Status: partially-resolved`); no Iteration-3 entry exists (the Dimson fix, two-stage stars, Tables 6 & 7, and the T7/T6 name-collision regeneration are recorded only in `logs/log1.md`).
  - Likely cause: the loop closed after iteration 3 without back-filling assumptions.md; `log1.md` claims "exit gate satisfied," but the gate literally walks assumptions.md, which is incomplete.
  - Specific fix: fill the two after-metrics (SW/Dimson 1.35→0.91, 0 FAIL; stars 109/120 → 110/120), flip both statuses to `resolved`, and append an Iteration-3 entry (Diagnosis/Next fix/Before/After/Status) covering Tables 6 & 7 and the registry regeneration.
- [m2] REPORT.md references an assumption that does not exist in the registry.
  - File: `REPORT.md:211` cites "A17 (Dimson β as the SW implementation)" but `preparations/assumptions.md` contains only A1–A16 (no A17 entry).
  - Specific fix: add the A17 entry (decision/rationale/impact for the Dimson-β choice) to assumptions.md, or correct REPORT.md to say A1–A16.
- [m3] Strict-monotonicity / "sign order" claim is slightly overstated.
  - File: `REPORT.md:99` ("all ten portfolios in the paper's sign order") and `logs/log1.md:63-65`.
  - Evidence: in [+1,+60], M2 FEP5 = −0.14 vs paper +0.22 and M1 FEP6 = −0.09 vs paper +0.55 flip sign at the zero-crossing, and M1 FEP10 (1.22) < FEP9 (1.75). The overall upward drift is intact (and the paper's own M1 is non-monotone because of the −7.58 anomaly), but "all ten in sign order" is not literally true.
  - Specific fix: soften to "near-monotone; the only deviations are at the zero-crossing portfolios (FEP5/FEP6) and M1 FEP10, all economically negligible."
- [m4] Two economically-negligible methodology details are not separately logged.
  - File: `src/main.py:457` (Model-4 σ window is `[−311,−61]` = 251 days vs the paper's 250) and `src/main.py:173,201` (Model-2 σ accumulates forecast errors only from 1974Q1, so the first five M2 quarters have <5 priors and drop; pre-1974 errors are not used).
  - Evidence: both are immaterial (one extra day in a 250-day σ; ~5 of 32 quarters affected for M2, and the M1 attenuation — which has no σ — is equally large, so neither can drive the headline attenuation). A9/A11 cover the floors but not these specifics.
  - Specific fix: one-line note each in assumptions.md for auditability (verification-only; no code change warranted).

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | M1/M2 [+1,+60] rise from strongly negative (FEP1) to positive (FEP10); spreads +3.51 (M1), +3.13 (M2). Minor near-zero violations only (M2 FEP2<FEP1, FEP7<FEP6; M1 FEP10<FEP9); the paper's own M1 is non-monotone (−7.58 anomaly). |
| 2 | Headline-magnitude claim | ✗ (vs paper) | Table values reproduce from `panel.parquet` *exactly* (max deviation 0.000), but vs the paper the [+1,+60] drift is attenuated to ~0.50 (M2 spread 3.13 vs 6.31); eq.16 R² is within 10% (0.726 vs 0.810). |
| 3 | Sample coverage ≥ 60% | ✓ | 77,492 obs; non-null FEP share 78.5% (M2) to 99.9% (M3/M4); obs/quarter 1,965–2,527, above the paper's 1,495–1,978. |
| 4 | Data-source choice justified | ✓ | Same sources as the paper (fundq + dsf + dsenames + ccmxpf_lnkhist + dsi); documented choices: consol='C' (A2), rdq = announcement date (A3), Dimson β for the unstated SW variant (A13/A17), NYSE-breakpoint assignment of non-NYSE firms (A16, justified: dropping them falls below the paper's 1,495 minimum). |
| 5 | prep_validation.py exit 0 | ✗ → ✓ | Exit 1 *before* this audit, on two auditor-owned layout errors (missing `logs/audit*.md` and `SUMMARY.md`). Resolved by this audit; see note below. |
| 6 | All committed tables have results files | ✓ | T1/T3/T4/T6/T7 → `table_1.md`, `table_3.md`, `table_4.md`, `table_6.md`, `table_7.md`, all present. |
| 7 | SUMMARY/REPORT matches results | ✓ | Every REPORT number I sampled reproduces from `cells_iter2.csv`/`panel.parquet` (M2 series, R², β, FE tails, Table 3 returns, 608/49/141 tally). |
| 8 | No orphan folders | ✓ | Slug root clean: data, inputs, logs, preparations, results, src, REPORT.md. |
| 9 | Diagnoses paired with fix attempts | ✗ | Iteration-1 entry complete; the two Iteration-2 entries have unfilled after-metrics and Iteration 3 is absent from assumptions.md (documented in log1.md). See [m1]. |
| 10 | Tier 2 within 2× magnitude | ✓ | Re-running the agent's exact `tier()` (`src/tables.py:109-118`) reproduces 608/49/141/0 exactly; all 49 Tier-2 cells satisfy sign-match + ratio ∈ [0.5, 2.0] (or paper=0, \|ours\|≤0.25). A stricter pure-[0.5,2.0] reading gives 608/44/146 — the 5-cell difference is the paper=0 convention, not mislabeling. |
| 11 | Corollary coverage | ✗ | Size variation ✓ (Table 6 committed, 174/244 Tier 1); temporal stability holds on recompute but paper's Table 5 not committed; market-adjusted robustness (Tables 8–9) not computed → [M1]. |

**Note on the magnitude diagnosis (the load-bearing question).** I tried to falsify the replicator's "restated-earnings vintage" explanation with four actionable alternatives, and each is ruled out by the cached data:
- *Symmetric σ-window bug* → ruled out: the FE2 bad-news tail matches the paper to three decimals (FEP1 median −2.244 = −2.244) while only the good-news tail is thin (FEP10 2.109 vs 3.151, 33% thinner). A σ bug would shrink both tails.
- *FEP-assignment / cutoff bug* → ruled out: unconditional frequencies are ≈0.10 for all 40 cells, persistence matches (M1 FEP1 lag-1 0.248 vs 0.334), and the same FEP assignments produce announcement-window CARs that match well.
- *Alignment / day-0 bug* → ruled out: Model 4 (same alignment, longer window) is correctly flat (R² = −0.011), Table 3 CRSP-only returns are near-exact, and [−1,0] matches.
- *Aggregation / units bug* → ruled out: Table 3 uses the same aggregation and matches to 0.007 pp/day.
The decisive cross-check: the announcement window [−1,0] is **not** attenuated (FEP10 ratio 1.55 — ours is *larger*), while the drift [+1,+60] is attenuated (ratio ~0.55 at FEP10, 0.44 at FEP1). If the signal were generally weak, [−1,0] would be weak too; the attenuation is drift-specific, exactly as restatement smoothing (which compresses the persistence/extremeness that drives underreaction, not the announcement surprise) predicts. The residual FAIL taxonomy supports this: 68 sign-flips of which 62 are |paper|≤1.0% (the 6 with |paper|>1.0 are all near-median, largest-quintile, or Model-4-noise cells), plus same-sign attenuation concentrated in M1/M2 [+1,+60] and a known paper-side anomaly (m1_fep3_p1_60: paper −7.58 breaks its own monotone pattern; ours −1.43 is monotone). The only residual I cannot fully close is Model-3's mild spurious structure (eq.16 R² = 0.36 vs ~0), but Model-4's flatness rules out a shared pipeline bug and the effect is ≤0.9% — economically negligible. Conclusion: the attenuation is non-actionable data vintage, not a fixable bug.

## 4. Issues the agent should have caught (didn't)

1. The exit-gate claim "every diagnosis has a fix attempt or non-actionable classification (exit gate satisfied)" is not backed by `assumptions.md` itself: two Iteration-2 entries still have blank after-metrics and Iteration 3 is missing from that file. The substance is in `log1.md`, but the gate the SKILL defines walks `assumptions.md`.
2. `REPORT.md` cites assumption "A17," which does not exist in the assumptions registry (A1–A16 only).
3. The monotonicity claim ("all ten portfolios in the paper's sign order") is overstated — FEP5 (M2) and FEP6 (M1) flip sign at the zero-crossing, and M1 FEP10 < FEP9. A careful reviewer states "near-monotone with zero-crossing deviations."

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Earnings Releases, Anomalies, and the
Behavior of Security Returns" (Foster, Olsen & Shevlin 1984) for slug
`earnings_releases_anomalies`. The previous agent run completed with verdict
**PARTIAL** (audit 1 at
`replications/earnings_releases_anomalies/logs/audit1.md`). Read the audit first.

The replication is in good shape: 798 committed cells, 76% Tier 1 / 82%
Tier 1+2, every central qualitative claim verified, and the ~0.50 attenuation
of [+1,+60] drift magnitudes is a confirmed non-actionable data-vintage effect
(restated 2026 earnings vs the paper's 1982 as-reported tape). **Do NOT try to
"fix" the drift magnitudes by tuning the sample — that would be gaming, and the
audit independently confirmed no methodology bug.** This iteration is a
corollary + cleanup pass.

## Issues to address (priority order)

### [M1] — MAJOR — fix first: commit the missing corollary / robustness tables
The paper's subsample-stability (Table 5) and market-adjusted robustness
(Tables 8–9, eq. 17) predictions are not committed as per-cell tables, even
though the underlying claim holds (I recomputed the M2 [+1,+60] FEP10−FEP1
spread for 1974–77 = 3.02 and 1978–81 = 3.21, both positive; 26/27 quarters
positive).

**Specific fix:**
1. Add the paper's Table 5: split the 32 quarters into the paper's reported
   subperiods, compute pooled M1/M2 CARs for [−1,0]/[−60,0]/[+1,+60], and
   compare cell-by-cell to the paper → `results/table_5.md`. The data is already
   in `data/panel.parquet` (group by `fep1`/`fep2` × `car_*` within each
   subperiod); no new pipeline run needed.
2. Compute the eq. 17 market-adjusted robustness (Tables 8–9): replace
   u = R_i − R_p with u = R_i − R_M using `crsp_202601.dsi.ewretd` (already
   verified available in `preparations/data_verification.json`, A13) and
   recompute the pooled CARs → `results/table_8_9.md`.
3. Register both in `preparations/tables_to_replicate.json` with paper targets +
   tolerances and extend `results/cells_iter2.csv`; re-run the per-cell Tier tally.
4. Verification: the subperiod drift spreads should both be positive and
   monotone (you should see ≈3.0 and ≈3.2); the eq. 17 robustness should still
   show M1/M2 drift and M3/M4 no-drift (the paper's point is that the result is
   not an artifact of the size-decile benchmark).

### [m1] — MINOR — close out assumptions.md
Fill the two Iteration-2 after-metrics in `preparations/assumptions.md`
(SW/Dimson 1.35→0.91 with 0 FAIL; stars 109/120 → 110/120), flip both statuses
to `resolved`, and append an Iteration-3 entry (Diagnosis/Next fix/Before/After/
Status) covering Tables 6 & 7 and the T7/T6 registry regeneration (currently only
in `logs/log1.md`).

### [m2] — MINOR — fix the A17 reference
`REPORT.md:211` cites "A17 (Dimson β as the SW implementation)" but the registry
has only A1–A16. Add the A17 entry to `preparations/assumptions.md` (or correct
REPORT.md).

### [m3] — MINOR — soften the monotonicity wording
In `REPORT.md:99` / `logs/log1.md:63-65`, replace "all ten portfolios in the
paper's sign order" with "near-monotone; the only deviations are the
zero-crossing portfolios (M2 FEP5, M1 FEP6) and M1 FEP10<FEP9, all economically
negligible." (The paper's own M1 is non-monotone because of the −7.58 FEP3
anomaly.)

### [m4] — MINOR — note two negligible methodology details
Add one-line notes in `preparations/assumptions.md`: Model-4 σ window is
[−311,−61] = 251 days vs the paper's 250 (`src/main.py:457`); Model-2 σ uses
forecast errors from 1974Q1 onward only, dropping the first five M2 quarters
(`src/main.py:173,201`). No code change — verification only.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration-log entry in
  `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric,
  After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop and escalate.
- **Do not chase the drift magnitudes.** The audit confirmed the attenuation is
  external (data vintage) and that all signs/ordering/significance/R²-hierarchy
  replicate. Tuning the sample to hit the paper's numbers is explicitly
  discouraged (A16).

## Inputs you should read

- `replications/earnings_releases_anomalies/logs/audit1.md` — this audit
- `replications/earnings_releases_anomalies/inputs/content.md` — paper ground
  truth (Tables 5, 8, 9 and eq. 17)
- `replications/earnings_releases_anomalies/preparations/` — prep contract
- `replications/earnings_releases_anomalies/src/tables.py` — table computation
  (extend, do not rewrite the pipeline)
- `replications/earnings_releases_anomalies/data/panel.parquet` — cached panel
  (subperiod table is a groupby, no pipeline re-run needed)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- Skip re-running `scripts/prep_validation.py` unless you change a prep artifact
  (you will, when you add Table 5 / Tables 8–9 to the registry — then re-run it).
- Skip re-doing the ClickHouse catalog scan — `data_verification.json` is current.
- Do NOT modify the FE/sigma/alignment logic — the audit verified it is correct.
- **DO** re-run the per-cell Tier tally after extending `cells_iter2.csv`.

## Deliverables for this iteration

- `results/table_5.md` and `results/table_8_9.md` — the two corollary/robustness
  tables with per-cell evaluation blocks citing the paper line numbers.
- `preparations/tables_to_replicate.json` — extended with Table 5 / Tables 8–9
  targets + tolerances; `results/cells_iter2.csv` extended accordingly.
- `preparations/assumptions.md` — closed-out Iteration-2 entries, new Iteration-3
  and Iteration-4 entries, A17 added, the two [m4] notes.
- `REPORT.md` — updated; lead with the data-quality summary and add the
  corollary tables to the results summary; fix the monotonicity wording.
- `SUMMARY.md` — read the latest assessment; do NOT edit (the auditor owns it).

## Stop conditions

- **[M1] done and verified, all minors closed** → re-run `prep_validation.py`
  and the Tier tally → declare success (the magnitude attenuation remains a
  documented non-actionable limitation); the next audit updates `SUMMARY.md`.
- **10-iteration cap reached** → escalate and write a partial `REPORT.md`.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is an unusually disciplined replication. The pipeline is faithful to the
paper at every construction step I traced (FE models 1–4, the NYSE size-decile
benchmark u = R_i − R_p, prior-quarter FEP cutoffs with no look-ahead, the
paper's own two-stage simulation for significance, and the eq. 16 codings), and
the agent caught and fixed its own real bugs (the structurally-incapable
Scholes–Williams formula and the one-stage significance draw) rather than
papering over them. What sets it apart is the deviation analysis: instead of
declaring "Tier 2 partial" and moving on, the agent built a falsifiable evidence
chain for the magnitude attenuation (asymmetric FE tails, σ-free Model-1
persistence also attenuated, announcement window *not* attenuated, CRSP-only
Table 3 near-exact, Model-4 flat while Model-3 shows only negligible structure),
and that chain survived my independent attempts to break it. The honest handling
of the paper's own −7.58 transcription anomaly (counted as a FAIL, flagged, and
shown to break the paper's own monotone pattern) is exactly the right call. The
replication falls short of PASS only on corollary coverage — the paper's
subperiod-stability and market-adjusted-robustness tables were scoped out — and
on some iteration-log hygiene in assumptions.md. Both are genuinely actionable
and low-cost, hence `requires_iteration: true`; but neither touches the headline
result, which replicates. If the next iteration adds those two tables and closes
the documentation gaps, this is a clean PASS.
