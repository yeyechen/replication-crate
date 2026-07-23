---
iteration: 2
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 2
requires_iteration: true
---

# Audit Report 2 — betting_against_beta

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** Iteration 2 addressed 3 of the 5 actionable majors from audit 1 ([M1] subsample stability, [M2] factor loadings, [M5] decile-alpha diagnosis) and all 4 minors. I **independently re-derived every new number** (own window-slicing + own statsmodels excess-on-factor regressions) and every figure in `table_3_subsample.md`, `table_b1.md`, and `table_3_post1962.md` reproduces **exactly**; all three files regenerate **byte-identical** from `src/corollaries.py`, and the shared analysis pass leaves the audit-1-verified `table_3.md` unchanged (still 25/32, BAB FF3 α 0.748 / t 7.11 / Sharpe 0.75). No blockers. The headline result and the two now-computed corollaries are trustworthy and honestly reported. Two named corollaries the paper sells remain uncomputed — [M3] size/IVOL splits and [M4] beta-window robustness — so the loop stays open. The bright line is cleared (`REPLICATED`); `requires_iteration: true` is driven only by those two residual corollary gaps. One new minor ([m5]) was introduced by the [m2] fix.

## 1. Scores

| Dimension | Score (it.1 → it.2) | Key finding |
|-----------|:---:|-------------|
| Methodology | 4 → **4/5** | Unchanged pipeline; this iteration I independently confirmed the factor-regression convention is correct (`factor_alpha` regresses portfolio **excess** returns on factors, intercept = alpha; iid t primary, NW(6) supplementary). Beta estimation, BAB construction (Eq. 16/17), delisting, and PIT filters all verified in audit 1 and reused unchanged. Deviations (Shumway/BMP delisting, PIT exchcd filter, `dlret=-1.0` as missing, Case-B timing) remain paper-silent and documented — no methodology bug. |
| Headline matching | 5 → **5/5** | BAB within ~5% on all 8 cells (FF3 α 0.748 vs 0.73; Sharpe 0.75 vs 0.78; leverage 1.44/0.69 vs 1.40/0.70); flat SML and monotonic Sharpe/alpha decline reproduce in shape and sign. |
| Data coverage | 4 → **4/5** | Universe 23,407 vs 23,538 (0.6%); CRSP dsf/msf/dsi/dsenames/dsedelist + FF all match; effective start 1928-08 vs 1926-01 (750-day beta warmup). |
| Concrete result matching | 4 → **4/5** | Still **25/32 Tier 1 (78.1%)** — this iteration added corollary evidence, not new Table 3 cells. The 7 fails (P1/P5/P10 FF3 & FF4, P10 CAPM alphas) persist; P10 FF4 still flips sign (+0.03 vs −0.13). Post-1962 test moves all of them toward the paper but does not change the committed full-sample table. |
| Signal strength | 5 → **5/5** | Headline cells r=|ours/paper|: BAB FF3 α 1.025, FF4 α 1.047, Sharpe 0.962, excess 1.021 — all in [0.9,1.1]. |
| Corollary | 2 → **3/5** | **Improved.** [M2] factor loadings now fully replicate (all 4 BAB loadings carry the paper-predicted sign; decile SMB gradient P1 +0.52→P10 +1.48; UMD −0.00→−0.44). [M1] subsample stability computed but **partial** — positive in all four 20-yr windows, significant in only 3 of 4 (SP1 1928-1948 positive but sub-significant: excess t=0.91, FF3 t=1.71). [M3] size/IVOL splits and [M4] beta-window robustness still **not computed** → notable gaps. Exactly the rubric's "some replicate, notable gaps (subsample stability partial)". |

**Overall: 4.17 / 5.00 → binary verdict `REPLICATED`** (mean ≥ 3.0, no dimension scored 1). Up from 4.00 in iteration 1, driven by corollary 2→3.

## 2. Issues by severity

### Blockers (must fix)

None. `prep_validation.py` currently exits 1 **only** because `logs/audit2.md` does not yet exist (created by this audit); the contract is otherwise clean and will pass after this write + the SUMMARY.md overwrite.

### Major (should fix) — 2 remaining, both carried over from audit 1

- [M3] Corollary 'cross-sectional variation' still not computed (size / idiosyncratic-vol splits) — **PRIORITY (cheap)**
  - File: `inputs/content.md` Table B3 (size splits), Table B5 (IVOL control); abstract/p.2 ("consistent … within deciles sorted by size, and within deciles sorted by idiosyncratic risk").
  - Paper claim: BAB holds within size deciles and after controlling for idiosyncratic volatility.
  - Status: explicitly not addressed in iteration 2 (documented as remaining gap in `log2.md`).
  - Specific fix: add `results/table_3_size.md` computing BAB α/Sharpe within large/mid/small size terciles from the existing `me` column (lag `me` one month to avoid look-ahead — see A9). The size split is computable from the existing panel + FF factors with **no beta re-estimation** (the cheap, high-value half). Flag IVOL (Table B5) as out-of-scope this iteration if the daily residual-vol computation is not reachable, but the size terciles must be produced.
  - actionable: true

- [M4] Corollary 'robustness specs' still not computed (beta windows / benchmark) — **lower priority (expensive: needs a panel rebuild)**
  - File: `inputs/content.md` Table B2 (different beta window lengths, local vs global benchmarks); §3.1 ("results are robust to alternative beta estimation procedures").
  - Paper claim: BAB is robust to alternative beta-estimation windows and benchmark choice.
  - Status: explicitly not addressed in iteration 2 (documented as remaining gap in `log2.md`).
  - Specific fix: parameterize `CORR_WINDOW`/`VOL_WINDOW` in `src/main.py`, rebuild **one** alternative beta (e.g., a shorter correlation window), and report the BAB α/Sharpe delta in `results/table_3_robustness.md`. Note this is the only remaining item that requires re-estimating betas (the ~6-min daily pipeline); the agent should weigh cost/benefit and, if it genuinely exceeds the iteration budget, may document a rigorous scope-out with justification — but [M3] must still be completed.
  - actionable: true

Resolved this iteration (independently verified — see §3):
- [M1] Subsample stability — **RESOLVED (directional)**. `results/table_3_subsample.md`: BAB positive in all four 20-yr subperiods, significant (|t|>1.96) in 3 of 4. SP1 (1928-08..1948-12) is positive but sub-significant (excess +0.217, t=0.91; FF3 +0.362, t=1.71); honestly attributed to the 1928-08 series start (A6/A8, ~2.5 yr short of the paper's 1926 window) + data vintage. Not a literal "significant in each" but directionally consistent and honestly reported.
- [M2] Factor loadings — **RESOLVED (full)**. `results/table_b1.md`: leverage long $1.435 / short $0.688 (paper $1.40/$0.70); BAB realized loadings market −0.056 (CAPM) / −0.016 (4-factor) ≈0 ("not exactly zero" ✓), SMB +0.008 (≈0 ✓), HML +0.061 (positive ✓, paper's "positive HML loading"), UMD +0.200 (positive ✓, "higher prior 12-mo return"); BAB 4-factor R²=0.072 (loadings don't explain the alpha ✓). Decile SMB gradient +0.52→+1.48 (low-beta larger ✓), UMD −0.00→−0.44 (low-beta higher momentum ✓).
- [M5] Decile-alpha diagnosis — **RESOLVED (diagnosis)**. `results/table_3_post1962.md`: post-1962 (n=603) every decile alpha moves toward the paper — P1 FF4 +0.490→+0.401 (paper +0.40, **exact match**), P5 FF3 +0.214→+0.163 (paper +0.13), P10 FF3 −0.346→−0.436 (paper −0.49). The P10 FF4 sign flip technically **persists** (+0.030→+0.013 vs paper −0.13) but is statistically zero (t=0.08) and economically negligible; BAB post-1962 stays strongly positive (FF3 +0.713, t=5.32; Sharpe 0.93). Honestly documented as data-vintage/beta-estimation-limited (A22), not a methodology error. Note: this diagnoses the anomaly but does **not** change the committed full-sample table (still 25/32), so the concrete-result score is unchanged.

Non-actionable (data-limited — do NOT block the loop, unchanged from audit 1):
- 5-factor alpha (Pastor-Stambaugh liquidity factor not in ClickHouse; A2).
- International equities (Tables 4-5) — Xpressfeed Global not in catalog.
- Other asset classes (Tables 6-8) — proprietary data unavailable.
- TED time-series (Table 9, Prop 3) and beta-compression (Prop 4) — TED series likely unavailable.
- Constrained-investor holdings (Prop 5, Tables 10) — mutual-fund/brokerage/13F data unavailable.

### Minor (cleanup)

- [m5] **NEW — the [m2] fix corrected the iid t-stats but left stale v1 Newey-West values in REPORT.md.** `REPORT.md:48` now reads "FF3 t-statistic is 7.11 … Newey-West: 5.85 … FF4 t-statistic is 5.54 … Newey-West: 4.58". The iid values (7.11 / 5.54) correctly match the final `table_3.md`, but the parenthetical NW values (5.85 / 4.58) are the **v1** NW(6) figures (they pair with v1 iid 7.28 / 5.71 and are recorded as such in `assumptions.md:176`). The final `table_3.md:54` NW block shows BAB **FF3 NW 5.71, FF4 NW 4.44**. So REPORT.md pairs v2 iid with v1 NW — internally inconsistent and inconsistent with the committed table.
  - Specific fix: change REPORT.md §2 NW parentheticals from (5.85 / 4.58) to (5.71 / 4.44) to match `table_3.md`. (The `assumptions.md:176` values are fine — they are correctly labeled as the v1 record.)

Confirmed fixed from audit 1:
- [m1] Orphan pipeline deleted — `results/panel_diagnostics.md`, `src/build_panel.py`, `logs/build_panel_run*.log` all absent; no `bab_*.sql` references remain. ✓
- [m2] REPORT.md iid BAB t-stats corrected to v2 (7.28→7.11, 5.71→5.54) — ✓ for the iid values (the NW parentheticals are the new [m5] above).
- [m3] `results/table_1.md` added — 5/5 committed Table 1 metrics pass (stocks 23,407 vs 23,538 = −0.6%; mean stocks/yr 3,073 vs 3,182 = −3.4%; June mean firm ME 0.996 vs 0.99 $B = +0.6%; start 1926 / end 2012 exact). ✓ (Minor wording nit: the notes say mean ME is "averaged across all stock-months (not June-only)" then cite the June-only 0.996 — the reported metric value is correct; only the explanatory sentence is slightly self-contradictory.)
- [m4] `data_verification.json` delisting `matched_table` corrected `crsp_202601.dse` → `crsp_202601.dsedelist` (line 62). ✓

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Determinism of new corollaries | ✓ | Backed up the 3 new files + `table_3.md`, re-ran `src/corollaries.py` (exit 0, 18.7s). All three (`table_3_subsample.md`, `table_b1.md`, `table_3_post1962.md`) **byte-identical** to committed; the shared v2 pass left `table_3.md` byte-identical (BAB series 1004 months, 1928-08..2012-03). |
| 2 | [M1] subsample numbers — independent | ✓ | Own window-slicing + own statsmodels OLS of **excess** on factors reproduces every cell exactly: SP1 ex +0.217(t0.91)/FF3 +0.362(t1.71)/FF4 +0.240(t1.19); SP2 +0.679/0.790/0.850; SP3 +1.107/0.841/0.722; SP4 +0.847/0.830/0.587; window n sum to 1004. Conclusion "positive in all 4, significant in 3/4" verified; SP1 sub-significance honestly flagged. |
| 3 | [M1] full-sample internal consistency | ✓ | Subsample "Full sample" row = excess 0.715(t6.85)/FF3 0.748(t7.11)/FF4 0.576(t5.54)/Sharpe 0.750 = exactly `table_3.md` BAB cells (the audit-1-verified series). |
| 4 | [M2] loadings + leverage — independent | ✓ | Own 4-factor regressions: BAB mkt(CAPM) −0.056, mkt(4f) −0.016, SMB +0.008, HML +0.061, UMD +0.200, R² 0.072 — all exact. Leverage (1/β̄) long 1.435 / short 0.688 exact. Decile SMB gradient P1 0.522 / P5 0.730 / P10 1.480 exact. All 4 signs match the paper's p.9 claims. |
| 5 | [M5] post-1962 alphas — independent | ✓ | Filtered the v2 sorted panel to ≥1962-01 (n=603), recomputed decile/BAB regressions: P1 FF4 +0.401 (paper +0.40, exact), P10 FF3 −0.436 (paper −0.49), P10 FF4 +0.013 (t0.08, paper −0.13 — sign persists, negligible), BAB FF3 +0.713 (t5.32), BAB FF4 +0.518 (t3.91) — all exact. |
| 6 | Regression convention correct | ✓ | Inspected `utils/regressions.py:factor_alpha` (line 587): `y = portfolio_returns − rf`, so alpha = intercept of **excess** on factors (standard FF time-series alpha); iid t primary, NW(6) supplementary. My first independent attempt regressed *gross* on factors and came out ~mean(rf) too high — confirming their excess convention is the correct one. |
| 7 | All committed tables have results files | ✓ | T3→`table_3.md`, T1→`table_1.md` (new). audit-1 gap closed. |
| 8 | prep_validation.py contract | ✗ (expected) | Exits 1 solely because `logs/audit2.md` is absent (created here). No data/layout/contract errors otherwise. |
| 9 | SUMMARY.md consistency with results | ✓ | SUMMARY.md overwritten this audit to iteration-2 scores (corollary 2→3) and the new corollary evidence; no stale v1 t-stats carried forward. |
| 10 | Orphan files / folders | ✓ | audit-1 orphans removed; no new stray files. |
| 11 | 5-field iteration logs present | ✓ | `assumptions.md` A23 + three iteration-log blocks ([M1]/[M2]/[M5]) each carry Diagnosis / Next fix / Before / After / Status. |
| 12 | Conservative tier labeling | ✓ | Agent still labels the 7 out-of-tolerance decile alphas FAIL (no Tier-2 inflation); the post-1962 "convergence" is framed as diagnosis, not as a pass-count change. Honest. |

## 4. Issues the agent should have caught (didn't)

1. **The [m2] fix introduced/left a stale NW pair in REPORT.md.** The agent correctly swapped the iid t-stats to v2 (7.11/5.54) but the adjacent "Newey-West: 5.85 / 4.58" are the v1 NW(6) figures (they pair with v1 iid 7.28/5.71 and are recorded as v1 in `assumptions.md:176`). The final `table_3.md:54` NW block reads 5.71 / 4.44. Anyone re-reading the final table against REPORT.md §2 would trip on the NW mismatch — the same class of error audit 1 flagged as [m2]. This is [m5] above; trivial to fix.
2. **`table_1.md` note is self-contradictory on June vs all-months ME.** The notes say the mean ME is "averaged across all stock-months (not June-only as the paper describes)" and then state "the June-only mean firm ME is 0.996 $B, matching the paper." The reported value (0.996, the June figure) is correct; the explanatory sentence should just say the metric is the June mean. Minor wording.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Betting against beta" (Frazzini &
Pedersen, 2014) for slug `betting_against_beta`. The previous agent run
completed with audit verdict **PARTIAL** (audit 2 at
`replications/betting_against_beta/logs/audit2.md`). Read that audit first.

State of play — the replication is strong and **already clears the bright
line (`REPLICATED`, overall 4.17/5)**. The headline US BAB factor replicates
within tolerance on all 8 Table 3 metrics (FF3 α 0.748 vs 0.73, iid t 7.11;
Sharpe 0.75 vs 0.78; leverage 1.44/0.69 vs 1.40/0.70), the run is
deterministic, and iteration 2 closed three corollary majors that the auditor
independently re-derived number-for-number: subsample stability ([M1],
positive in all four 20-yr windows, significant in 3/4), factor loadings
([M2], all four signs match the paper), and the post-1962 decile-alpha
diagnosis ([M5], P1 FF4 matches the paper exactly post-1962; P10 FF4 flip is
statistically zero). This iteration closes the **two remaining named
corollaries** so the corollary dimension can move 3→4/5. Do **NOT** rebuild
the panel or re-derive the BAB factor for [M3] — they are verified.

## Issues to address (priority order)

### [M3] — MAJOR — cross-sectional variation: size split (Table B3) — PRIORITY, CHEAP
Paper (abstract/p.2): BAB holds "within deciles sorted by size" (Table B3);
also controls for idiosyncratic volatility (Table B5).

**Specific fix:**
1. Add `results/table_3_size.md`. Using the existing `me` column in
   `data/panel.parquet`, form large / mid / small **size terciles each month**
   (NYSE breakpoints on lagged `me` — lag `me` one month to avoid look-ahead,
   per assumptions A9), and compute the BAB factor's excess return, FF3/FF4
   alpha (+ iid t), and Sharpe **within each size group**, citing Table B3.
2. Reuse `src/corollaries.py`'s shared v2 pass (it already loads the panel,
   merges exchcd, builds the delisting adjustment, and runs
   `t3.run_analysis(...)`); subset the sorted panel `df` by size tercile and
   recompute BAB on each subset. No beta re-estimation needed.
3. Evaluate the paper's claim: BAB should be positive and significant within
   each size group (it is typically strongest among small caps). Report signs
   + significance per tercile vs the paper.
4. **Flag IVOL (Table B5) as out-of-scope this iteration** if the daily
   residual-vol computation is not cheaply reachable — but the size terciles
   must be produced.

### [M4] — MAJOR — beta-estimation robustness (Table B2) — LOWER PRIORITY, EXPENSIVE
Paper (§3.1, Table B2): BAB is "robust to alternative beta estimation
procedures" (different window lengths; local vs global benchmark).

**Specific fix:**
1. Parameterize `CORR_WINDOW`/`VOL_WINDOW` in `src/main.py` and rebuild **one**
   alternative beta (e.g., a 3-year correlation window instead of 5-year, or a
   non-overlapping daily window). This is the ONLY remaining item that needs
   the ~6-min daily beta pipeline.
2. Re-run the BAB factor on the alternative beta and report the α/Sharpe delta
   in `results/table_3_robustness.md`, citing Table B2.
3. If this genuinely exceeds the iteration budget, you may document a rigorous
   scope-out (which window, why it is expected to be immaterial, pointer to the
   paper's own robustness claim) — but only after completing [M3].

### Minor — cleanup
- [m5] Fix REPORT.md §2 NW parentheticals from (FF3 5.85 / FF4 4.58) to the
  final-table values (FF3 5.71 / FF4 4.44) to match `results/table_3.md:54`.
  The iid values (7.11 / 5.54) are already correct — leave them.
- (nit) In `results/table_1.md` notes, state the mean-ME metric is the June
  mean (remove the contradictory "averaged across all stock-months" clause).

## Iteration discipline reminders
- **Diagnose → commit-fix → fix → verify.** Every iteration-log entry in
  `assumptions.md` must keep all five fields: Diagnosis, Next fix, Before
  metric, After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop at 10 and escalate.
- **Do not re-derive the BAB factor / beta pipeline** for [M3] — reuse the
  cached panel + shared v2 pass. Only [M4] needs new betas.

## Inputs you should read
- `replications/betting_against_beta/logs/audit2.md` — this audit
- `replications/betting_against_beta/inputs/content.md` — paper (Tables B3/B5,
  abstract size/IVOL claim; Table B2 beta-window claim)
- `replications/betting_against_beta/src/corollaries.py` — reuse the shared v2
  pass (`t3.run_analysis`, `t3.bab_factor`, `bab_metrics`) for [M3]
- `replications/betting_against_beta/data/panel.parquet` — cached panel (`me`
  column for the size split)
- `replications/betting_against_beta/results/table_3.md` — current Table 3

## What NOT to redo
- Skip re-reading `SKILL.md`.
- Skip re-running `scripts/prep_validation.py` unless you change a prep
  artifact (after this audit it should pass).
- Do not recompute [M1]/[M2]/[M5] — they are verified and byte-stable.
- Do not rebuild the panel for [M3].

## Deliverables for this iteration
- `results/table_3_size.md` ([M3], citing Table B3) and, if reached,
  `results/table_3_robustness.md` ([M4], citing Table B2).
- `preparations/assumptions.md` — append a 5-field iteration-log entry for
  every issue addressed (A24+).
- `REPORT.md` — update §4 corollary evidence with the size split; fix the NW
  parentheticals ([m5]).
- Do NOT edit `SUMMARY.md` (auditor-owned).

## Stop conditions
- **[M3] computed and verified** (BAB within size terciles) → re-run
  prep_validation.py; declare success or note [M4] as the only remaining major.
- **[M4]**: complete one alternative beta window, OR document a rigorous
  scope-out if it exceeds the iteration budget (after [M3] is done).
- **Data-limited gaps (5-factor, international, other asset classes, TED,
  Prop-5 holdings)** are NON-actionable — document, do not loop.
- **10-iteration cap** on a single problem → escalate, write a partial
  REPORT.md; do not edit SUMMARY.md.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This was a clean, honest follow-up iteration. The standout is that the agent
did exactly what audit 1 asked on the three corollaries it tackled: it reused
the verified v2 series rather than re-deriving anything, the new code
(`src/corollaries.py`) is thin and readable, and — crucially — I could
reproduce **every** new number independently (my own slicing + my own
statsmodels regressions) to the last decimal, with byte-identical regeneration
and an unchanged headline table. That is the gold standard for corollary work:
cheap, additive, and auditable.

Two things keep this at PARTIAL rather than closing the loop. First, the two
named corollaries the paper still sells — cross-sectional variation by size
(abstract, Table B3) and beta-window robustness (§3.1, Table B2) — remain
uncomputed, which is exactly why the corollary dimension is 3/5. The size
split is cheap (the `me` column is already in the panel) and should be the
unambiguous priority; beta-window robustness needs a panel rebuild and is
legitimately more expensive, so it can be scoped down to one alternative
window or, failing that, rigorously documented. Second, the agent re-committed
the precise class of slip audit 1 flagged: the [m2] fix corrected the iid
t-stats but left the adjacent Newey-West values in REPORT.md at their v1
figures (5.85/4.58) instead of the final table's (5.71/4.44). It is trivial to
fix but is a reproducibility-paper-cut that a careful reader would catch.

On the decile alphas: the post-1962 diagnosis ([M5]) is the right, cheap test
and it did its job — it shows the decile-alpha structure converges toward the
paper (P1 FF4 matches to the decimal) and that the P10 FF4 sign flip is
economically negligible (t=0.08) even though its sign technically persists.
The agent is commendably honest that this is "not purely an early-sample
artifact" and refuses to overclaim. But it remains a genuine residual: 7
decile multi-factor alphas are still outside Tier 1 and the committed table is
still 25/32, so the concrete-result score rightly holds at 4/5. The honest
framing (data-vintage / beta-estimation-limited, A22) is the correct landing
spot for a replication whose headline (the BAB factor itself) is rock-solid.

Bottom line: `REPLICATED`, overall 4.17/5 (up from 4.00), with two addressable
corollary gaps and one trivial reporting fix standing between this and a 4-5/5
corollary score.
