---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 6
requires_iteration: true
---

# Audit Report 1 — the_52_week_high_and_momentum_investing

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** A methodologically careful replication whose committed five tables (I, II, III, V, VII; 516 cells) are independently reproducible end-to-end from the cached panels and coefficient series (every raw + risk-adjusted cell I recomputed matches the reported value to 4 dp), but which (a) leaves the paper's abstract-level long-term-non-reversal claim and the 52-week-low robustness without any artifact, (b) ships the Table VII GH-dummy side broken (16 FAILs) with a pre-committed fix never run, (c) lets the central dominance margin collapse / invert in the two Jan-included raw FM columns because the WH-loser dummy is ~64% of the paper while JT/MG run 1.4-1.6x hot, and (d) fails `prep_validation.py` on a parquet allowlist. Numbers are trustworthy; scope and a few diagnostic follow-throughs are not yet complete.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | Signal formulas, timing (no-skip I-IV, skip j=2..7/2..13 V+), EW 30/30, FF3-RA intercepts, FM t-stats from the c-series, delisting ratification, daily-close-max 52WH all trace to paper lines with documented rationale; only minor documented deviations (daily-close vs intraday high; 60-lag min for GH; MG ordinal tie-break). No methodology bug. |
| Headline matching | 3 | All shapes/signs/orderings reproduce (January anatomy, nested winner+middle dominance, Table VII wh-spread 16/16 Tier 1, ex-Jan + RA dominance ordering), but Table V pure-52WH spreads run 0.69-0.83x of the paper (RA janincl 0.59 vs 0.86 = -31%) and the WH-vs-JT ordering inverts in the two Jan-included raw columns the paper leads with. |
| Data coverage | 4 | Exact 462-month period 1963-07..2001-12; same CRSP+FF sources; Jul-1963 universe 1,977 matches the all-CRSP era pattern; GH rankable coverage only 38-62% (1970s volume missing) is the one sub-60% signal but is documented and tied to M2. |
| Concrete result matching | 3 | 338/516 Tier 1 = 65.5% (band 3). (Alternative Tier1+Tier2-within-2x = 410/516 = 79.5%, band 4; the repo's Tier-2 = sign-match-only, so 88/160 Tier-2 cells exceed the rubric's 2x bound — see spot-check 10.) |
| Signal strength | 3 | Worst headline ratio r = 0.688 (Table V RA janincl WH spread); Table I WH W-L 0.94x, Table VII WH spread 1.02-1.09x, but Table V WH 0.69-0.83x and MG 1.28-1.62x put it outside [0.8,1.2]. All within [0.5,2.0]. |
| Corollary | 3 | January stability + (6,12) robustness replicate; but the abstract's long-term non-reversal (Table VI) and the 52-week-low (Table IX) corollaries have no artifact and were not surfaced as gaps; GH-dominance-over-JT/MG computed but not reproduced; nested-loser dominance partial. |
| **Overall** | **3.33** | REPLICATED by the bright line (mean >= 3.0, no dimension = 1); audit verdict PARTIAL with requires_iteration: true. |

## 2. Issues by severity

### Blockers (must fix)

None. Every committed cell I recomputed from the cached `strategy_returns.parquet`, `fm_coefficients.parquet`, and `fm_coefficients_gh.parquet` (raw means/t-stats and, against ClickHouse `ff.four_factor_monthly`, the FF3 risk-adjusted intercepts) matches the reported value to 4 decimals; the scientific replication is sound. The `prep_validation.py` non-zero below is a layout/allowlist hygiene gap, not a broken replication.

### Major (should fix)

- [M1] Corollary "52-week-high profits do NOT reverse in the long run" (Tables VI/VIII) has no artifact — this is the paper's 3rd abstract claim, yet it is absent from `results/` and was never listed as a gap by the replicator.
  - File: inputs/content.md:981-1005 (Table VI), 1283-1289 (text); preparations/tables_to_replicate.json (no T6/T8 entry).
  - Likely cause: scope was frozen at the prep stage to 5 tables; the persistence tables were recognized in `candidate_assessment.json` but not committed.
  - Specific fix: extend the existing FM engine in `src/tables_5.py` (it already does (6,12) with j=2..13) to a (6,k,12) layout at k=12,24,36,48 with RA-only columns, identical dummies; write `results/table_6.md`. Verify JT/MG winner dummies turn negative/significant while 52WH winner+loser stay near zero (paper ex-Jan (6,~12,12) WH spread 0.16 t 1.93; JT winner -0.18 t -4.76).
  - actionable: true

- [M2] Table VII GH-dummy side is broken and the pre-committed fix was never run: 16 FAILs (all GH sign flips + one tiny jt cell), gh_spread ~0 (e.g. s66 raw ex-Jan 0.012 vs paper 0.44), gh_loser +0.26..+0.40 vs paper -0.09..-0.26 in 5 of 8 columns. log1.md iteration 5 explicitly deferred "GH variant B (reference price renormalized over AVAILABLE lags, min 24 months)" to outer iteration 2 "if the auditor flags it actionable" — it is now flagged.
  - File: results/table_7.md:75-215 (the gh_* rows); src/tables_7.py + src/main.py g_gh recursion (assumption A11, preparations/assumptions.md:68-72); log1.md:250-258.
  - Likely cause: the strict 60-consecutive-month requirement + 40% 1970s volume missingness makes early GH bins a thin NYSE-heavy subset; the paper may have renormalized the 60-term reference price over available months (paper silent on a minimum).
  - Specific fix: implement g_gh variant B (denominator = sum of available nonzero weights over whatever lags exist, min 24 months), rebuild `data/panel.parquet` and re-run Table VII (and re-confirm Tables I/V unchanged on wh_*); adopt B iff total GH Tier-1 rises AND wh_spread stays Tier 1; else keep strict-60 and document. Expected before/after anchor: gh_spread s66_raw_janexcl 0.0123 -> toward 0.44; gh_loser s66_raw_janexcl +0.2572 -> toward -0.19.
  - actionable: true

- [M3] The paper's single most-cited dominance cell inverts, and the pre-registered A13 sensitivity was never run. In (6,6) raw Jan-included the paper reports WH 0.65 > JT 0.38 > MG 0.25; ours is JT 0.5295 > WH 0.4896 > MG 0.3804. Same inversion in (6,12) raw Jan-included (JT 0.3295 > WH 0.3091). Cause is two-sided: wh_loser dummy is only ~0.64x paper (s66 raw janincl -0.3079 vs -0.48) while jt_spread/mg_spread run +39%..+62% (1.39x/1.52x). `assumptions.md` A13 pre-registered a fix-on-miss sensitivity ("re-estimate restricting the sample to stocks rankable on all three signals"); Table V partially misses on wh_loser, yet the sensitivity was not run.
  - File: results/table_5.md:56-69 (s66_raw_janincl) and 122-137 (s612_raw_janincl); preparations/assumptions.md:80-83.
  - Likely cause: all-exchange/2026-vintage small-cap January inflates JT/MG loser dummies; the FM cross-section keeps un-rankable stocks as 0/0 dummies (dilutes wh_loser).
  - Specific fix: (a) run the A13 sensitivity — re-estimate Table V on the cross-section rankable on jt AND mg AND wh signals; report before/after for wh_loser, wh_spread, intercept in all 8 columns; (b) report the dominance ordering per column explicitly so the inversion is visible, not glossed; (c) if the rankable-only sample does not restore the WH>JT margin in raw Jan-incl, document the inversion as a vintage effect (then reclassify as non-actionable).
  - actionable: true

- [M4] Corollary "52-week-LOW strategy is not profitable" (Table IX) has no artifact — a robustness / cross-sectional-variation corollary the paper uses to argue against the symmetric GH proposition; absent from `results/` and not surfaced as a gap.
  - File: inputs/content.md:1335, 2460-2464 (Table IX text); paper's 52-low measure = P_{t-j}/min price over t-j-12..t-j.
  - Specific fix: add a `wh_lo_sig` = abs(prc_f)/min over f-11..f of daily |close| to the panel; run one FM table (Table V layout with the 52-low dummies replacing the 52-high dummies) as `results/table_9.md`; verify the 52-low spread is insignificant (paper (6,6) raw janincl 0.13, t insignificant) while JT/MG stay significant.
  - actionable: true

- [M5] MG spread runs +28%..+62% (Tier-1 by tolerance, but the largest systematic offset in the replication) and the tie-handling choice that likely drives part of it was never sensitivity-tested. A8 ranks individual stocks by their industry's cumulative return and splits 30/30 by permno ordinal tie-break, so stocks inside the boundary industry are arbitrarily split across winner/middle/loser; the intended MG reading is ranking the 20 industries and taking the top/bottom 6.
  - File: src/tables_1_3.py + src/tables_5.py sort logic; preparations/assumptions.md:50-53 (A8).
  - Likely cause: ordinal tie-break at the 30th-percentile boundary + a SIC-vintage shift in the "Financial" industry (ours 1,294 vs MG's ~891 in 1990-06, panel_summary.md:71; hsiccd gives 778 — still off).
  - Specific fix: add an industry-level MG cutoff variant (winner = stocks in the 6 highest-return industries, loser = 6 lowest) and report before/after for mg_w_minus_l (Table I 0.5747 vs 0.45) and mg_spread (s66 raw janincl 0.3804 vs 0.25); adopt iff it closes the MG gap without hurting the MG ordering (MG must remain the weakest strategy everywhere).
  - actionable: true (lower priority)

- [M6] `scripts/prep_validation.py` exits non-zero: `data/` holds three derived caches — `fm_coefficients.parquet`, `fm_coefficients_gh.parquet`, `strategy_returns.parquet` — that are not in the validator's closed parquet allowlist (it enumerates panel/bin_rets/ls_ew/ls_vw/cop_p_factor/amihud_daily/delisting_returns/panel_maxn/mom_components/beta_ivol_components/compustat_book_equity only). The other two validator errors (missing `logs/audit*.md` and `SUMMARY.md`) are expected pre-audit and clear once this audit is written; the parquet error does not.
  - File: results/REPORT.md:180-183 (documents these as the official caches); scripts/prep_validation.py:578-606 (closed allowlist).
  - Likely cause: the validator allowlist was relaxed for intermediate signal parquets (commits bc9bb0a, c8b7aa6) but not extended to this paper's FM/strategy caches; the pipeline design intentionally exposes these c-series to the auditor.
  - Specific fix (auditor cannot edit the repo validator): relocate the three derived caches out of `data/` (e.g. to `results/intermediate/` or `results/`) and update the read paths in `src/tables_5.py`, `src/tables_7.py`, `src/tables_1_3.py`, `src/plots.py`, OR — if the repo maintainer agrees the allowlist should cover named derived caches — have the validator's allowlist extended. Then re-run `scripts/prep_validation.py <slug-path>` and confirm exit 0.
  - actionable: true

### Non-actionable majors (documented; do not loop on)

- [N1] Table III nested W-L spreads inside LOSER outer groups are ~45-55% of the paper (e.g. pa_loser_w_minus_l_exjan 0.4431 vs 0.98). actionable: false — paper footnote 6 (inputs/content.md:574) flags these cells as unbalanced ("in some months it has none") and supersedes them with the regression tables; the signal-granularity diagnostic (wh_sig_dc, log1.md iter 3) already moved them toward the paper and the residual is small-cell January/CRSP-vintage noise. Documented in REPORT.md sec 5.
- [N2] Jan-included FM intercepts run +25%..+46% (s66 raw janincl 4.64 vs 3.62; s66 RA janincl 3.46 vs 2.58). actionable: false — driven by stronger small-cap January in the all-exchange/2026-vintage universe; ex-January intercepts match within ~18% and the Table II January cells reproduce (JT loser 11.33% vs 11.2%, WH 11.76% vs 12.11%), which is the same phenomenon.

### Minor (cleanup)

- [m1] Orphan nested empty tree `replications/the_52_week_high_and_momentum_investing/{data,src,results,logs,inputs,preparations}/` under the slug root (a copy artifact; all subdirs empty). Specific fix: delete the nested `replications/` directory.
- [m2] Tier-2 boundary is defined repo-wide as "sign match only" (TOLERANCE_RULES.md), so 88 of the 160 Tier-2 cells have |ours/paper| outside the rubric's 2x bound (e.g. pb_winner_w_minus_l_exjan 1.0682/0.24 = 4.45x; s612_raw_janexcl jt_winner 0.1512/0.02 = 7.6x; the GH t-stats >10x). Mostly tiny-magnitude dummies/t-stats and the broken GH columns. Specific fix: annotate cells with |ratio|>2 (e.g. an extra flag column or a note) so a human reader is not misled by "Tier 2" on a 7x cell; no value change.
- [m3] `results/table_3_dc_vs_cl.md` is the inner-iteration-3 signal-granularity diagnostic and is not listed in REPORT.md sec 6's file inventory. Specific fix: list it as a diagnostic artifact (or move under results/diagnostics/).
- [m4] `logs/log1.md` has out-of-order edits: the iteration-6 task spec was overwritten by the delisting-experiment note and re-appended at the file end (lines 302-316), and iterations 4-5 still carry "(pending)" placeholders above their appended results. Readable but untidy. Specific fix: linearize the iteration-4/5/6 blocks (task spec -> worker report -> decision in order).
- [m5] REPORT.md sec 4 figures caption reads `cumulative_wl.png ... (52WH dominates; ...)`, but the figure's own legend shows MG 11.88x > JT 5.12x > WH 3.44x (the all-months EW compound, where Table I means are within 0.03pp, so compounding puts MG on top). The figure is honest; the caption claim is wrong. Specific fix: relabel the caption to "all-months EW cumulative value (MG>JT>WH); the 52WH dominance lives in the ex-January and regression columns (figs 2-3)" — matching log1.md iteration 7's own honest flag.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Dominance / direction claim | partial | WH>JT>MG holds in 6/8 (6,6)+(6,12) columns (all ex-Jan + both RA); INVERTS to JT>WH in both Jan-included RAW columns — including the paper's lead cell (paper 0.65>0.38, ours 0.49<0.53). January anatomy + nested winner/middle dominance + Table VII wh 16/16 all correct. |
| 2 | Headline-magnitude claim | partial | Table I WH W-L 0.94x, Table VII WH 1.02-1.09x, Table II ex-Jan 0.96x (tight); Table V pure-WH 0.69-0.83x and MG 1.28-1.62x exceed the 20% band. |
| 3 | Sample coverage >= 60% | partial | jt/mg/wh signals non-null 94-99%; g_gh non-null only 47.4% (below 60%) — documented (60-lag + 1970s vol missing), tied to M2. |
| 4 | Data-source choice justified | pass | CRSP msf/dsf/dsenames/msedelist + FF; 2026 vintage documented; daily-close-max 52WH justified by askhi quote-sign contamination (20% non-positive, 1970s 40%). |
| 5 | prep_validation.py exit 0 | fail | 3 derived caches outside the closed parquet allowlist (M6); the 2 missing-file errors clear once this audit writes audit1.md + SUMMARY.md. |
| 6 | All committed tables have results files | pass | T1,T2,T3,T5,T7 all present (T3 = JT x 52WH as committed; T4/T6/T8/T9 intentionally out of scope). |
| 7 | REPORT/SUMMARY values match artifacts | partial | All numeric claims I checked reproduce from the caches; BUT the cumulative_wl.png caption "(52WH dominates)" contradicts the figure (MG on top) — m5. |
| 8 | No orphan folders | fail | nested empty `replications/<slug>/` tree — m1. |
| 9 | Diagnoses paired with fix attempts | partial | delisting experiment + wh_sig_dc diagnostic have full before/after; but the GH variant B fix (log1.md iter 5) and the A13 rankable-only sensitivity (assumptions.md) were diagnosed/pre-registered and NOT run this iteration -> M2, M3. |
| 10 | Tier 2 within 2x magnitude | partial | By the repo's TOLERANCE_RULES (Tier 2 = sign match) tiering is internally consistent; by the rubric's 2x bound, 88/160 Tier-2 cells exceed it -> m2. |
| 11 | Corollary coverage | partial | January stability + (6,12) robustness replicate; long-term non-reversal (Table VI) + 52-week-low (Table IX) silently absent and not surfaced by the replicator -> M1, M4; GH-dominance computed but broken -> M2. Surfaced now as majors, so coverage is closed for this audit. |

Recomputation evidence (auditor, from cached parquets): Table I from `strategy_returns.parquet` (n=462): jt_wl 0.4720 t 2.2505, mg_wl 0.5747 t 4.5364, wh_wl 0.4233 t 1.7568 — exact match to results/table_1.md; Table II Panel A wh_wl 1.1812 t 6.5247, Panel B jt_wl -6.2650 t -4.3012 — exact. Table V raw (all 96 cells) recomputed from `fm_coefficients.parquet` c-series mean/(std/sqrt(T)) — exact match to results/table_5.md (e.g. s66_raw_janexcl wh_spread 0.8745 t 6.1224). Table V RA (FF3 from ClickHouse `ff.four_factor_monthly`, 462 months, 0 missing) recomputed as OLS intercept of the c-series on {mkt_rf,smb,hml} — exact match (s66_ra_janexcl wh_spread 0.8436 t 8.7231, intercept 1.7650 t 2.9052). Table VII raw + RA from `fm_coefficients_gh.parquet` likewise exact (s66_raw_janincl wh_spread 0.5203 t 3.1881; gh_loser 0.3961 t 4.7179; gh_spread -0.1265). Panel 2,387,326 x 18, 540 months, 0 dup keys; Jul-1963 universe 1,977 (ret non-null) = 1,985 incl 8 added delisting rows; wh_sig_dc in (0,1] with 0 nulls beyond 0.6%. Aggregate tier tally 338/160/18 of 516 confirmed (per-file 12/24/48/192/240; the +6 over a naive text-grep is the "| Tier 1 | Tier 2 | FAIL |" header row in the per-column tally tables of T5/T7).

## 4. Issues the agent should have caught (didn't)

1. The paper's most-cited dominance cell — Table V (6,6) raw Jan-included WH 0.65 > JT 0.38 — inverts in the replication (JT 0.53 > WH 0.49). REPORT.md sec 4 mentions the inversion only for the (6,6) raw Jan-incl column in passing and frames the JT/MG overshoot and the WH shortfall as two separate, harmless vintage effects; their COMBINED effect on the headline dominance margin/ordering (and that it hits the paper's lead numbers) is never named, and the pre-registered A13 sensitivity that targets exactly this was not run.
2. The abstract's long-term-non-reversal claim (Table VI) and the 52-week-low robustness (Table IX) were dropped at the prep stage and never re-surfaced as scope gaps; `candidate_assessment.json` even lists them as known tables. A careful peer reviewer expects either the table or an explicit "intentionally out of scope, here is why" note in REPORT.md.
3. REPORT.md's `cumulative_wl.png` caption asserts "52WH dominates" while the figure's legend shows MG ~3.5x the WH cumulative value — an internal caption/figure contradiction the agent's own iteration-7 worker had honestly flagged in the log but did not propagate to the report caption.
4. `prep_validation.py` was apparently not re-run after the FM caches were written to `data/`; the allowlist failure is a one-line-of-thought fix (relocate the caches) that the agent never saw because it stopped checking the validator.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "The 52-Week High and Momentum Investing" (George & Hwang 2004, JF) for slug `the_52_week_high_and_momentum_investing`. The previous run completed with audit verdict **PARTIAL** (audit 1 at `replications/the_52_week_high_and_momentum_investing/logs/audit1.md`). Read that audit first; it independently re-verified every raw + risk-adjusted cell of Tables I, II, III, V, VII from the cached parquets (and FF3 from ClickHouse), so the numbers are trustworthy — your job this iteration is to CLOSE SCOPE and the diagnostic follow-throughs, not to redo verified machinery.

## Issues to address (priority order)

### [M1] — MAJOR — abstract claim with no artifact; do first
The paper's 3rd abstract claim — "future returns forecast using the 52-week high do not reverse in the long run" (Tables VI/VIII, inputs/content.md:981-1005, 1283-1289) — has no result file and was never listed as a gap.
**Specific fix:**
1. In `src/tables_5.py` (the FM engine already does (6,12) with j=2..13), add a (6,k,12) persistence layout at k in {12,24,36,48}: same cross-sectional OLS as Table V with the dummies drawn from formation f = t-k-j; RA-only columns (intercept of the c-series on FF3).
2. Write `results/table_6.md` with per-cell ours-vs-paper + tier (paper values inputs/content.md:1007-1095, 1134-1268).
3. Verification: JT/MG winner dummies should turn negative and significant (paper ex-Jan (6,~12,12) JT winner -0.18 t -4.76; MG winner -0.12 t -2.76), while the 52-week-high winner+loser stay near zero / insignificant and the WH spread stays ~0 (paper ex-Jan (6,~12,12) WH spread 0.16 t 1.93). Append an assumptions.md entry (Diagnosis / Next fix / Before metric / After metric / Status).

### [M2] — MAJOR — run the GH coverage fix you already committed to
Table VII GH side is broken (16 FAILs; gh_spread s66 raw ex-Jan 0.012 vs paper 0.44; gh_loser sign-flips in 5 columns). log1.md iteration 5 deferred "variant B" to the next iteration if flagged — it is flagged.
**Specific fix:**
1. In `src/main.py` add g_gh variant B: reference price = sum of nonzero weighted prices / sum of nonzero weights over AVAILABLE lags with a 24-month minimum (instead of the strict 60-consecutive-month requirement, assumption A11). Keep strict-60 as variant A.
2. Rebuild `data/panel.parquet`, re-run Tables I, V, VII under B; confirm wh_spread and jt/mg columns are unchanged-or-better (wh_spread must stay Tier 1).
3. Adopt B iff total Table VII Tier-1 count rises and gh_spread s66_raw_janexcl moves from 0.0123 toward 0.44; else keep A and write a one-paragraph justification in REPORT.md sec 5 (data-coverage limitation). Before/after anchors: gh_loser s66_raw_janexcl +0.2572 -> toward -0.19; gh_spread s66_ra_janexcl 0.0976 -> toward 0.55.

### [M3] — MAJOR — run the pre-registered A13 sensitivity and surface the dominance inversion
In the two Jan-included RAW FM columns the WH-vs-JT ordering inverts vs the paper (paper (6,6) raw janincl WH 0.65 > JT 0.38; yours JT 0.5295 > WH 0.4896), because wh_loser is ~0.64x paper while jt/mg spreads are 1.39-1.52x. assumptions.md A13 pre-registered a fix-on-miss sensitivity that was never run.
**Specific fix:**
1. Re-estimate Table V restricting the FM cross-section to stocks rankable on jt AND mg AND wh signals simultaneously; report before/after for wh_loser, wh_spread, and the intercept in all 8 columns (write to results/table_5.md as a sensitivity block).
2. Add an explicit "dominance ordering per column" row so the WH>JT>MG vs JT>WH status is visible in every column; if the rankable-only sample restores the margin in raw Jan-incl, update the official Table V, else document the inversion as a vintage effect (then it becomes non-actionable).

### [M4] — MAJOR — compute the 52-week-low corollary (Table IX)
inputs/content.md:1335, 2460-2464: a 52-week-LOW strategy should be unprofitable (paper (6,6) raw janincl WH-low spread 0.13, insignificant). No artifact exists.
**Specific fix:**
1. Add `wh_lo_sig` = abs(prc_f) / min over f-11..f of daily |close| to the panel.
2. Run one FM table (Table V layout, 52-low dummies replacing 52-high dummies) as `results/table_9.md`; verify the 52-low spread is insignificant while JT/MG stay significant and positive.

### [M5] — MAJOR (low priority) — test MG industry-level cutoff
MG spreads run +28%..+62% everywhere; A8's permno-ordinal tie-break splits the boundary industry's stocks across winner/middle/loser, which is not the intended MG reading (rank the 20 industries; top/bottom 6).
**Specific fix:**
1. Add an industry-level MG variant (winner = stocks in the 6 highest past-6m industry returns; loser = 6 lowest).
2. Report before/after for mg_w_minus_l (0.5747 vs paper 0.45) and mg_spread s66 raw janincl (0.3804 vs 0.25); adopt only if the MG gap shrinks AND MG remains the weakest strategy in every column.

### [M6] — MAJOR — make prep_validation.py exit 0
`data/` holds 3 derived caches (fm_coefficients.parquet, fm_coefficients_gh.parquet, strategy_returns.parquet) the repo validator's closed parquet allowlist rejects. You cannot edit the repo validator.
**Specific fix:**
1. Move the three derived caches out of `data/` (e.g. `results/intermediate/`) and update the read paths in src/tables_5.py, src/tables_7.py, src/tables_1_3.py, src/plots.py (and any path constant). Keep `data/panel.parquet` in place (it IS allowlisted).
2. Re-run `python scripts/prep_validation.py replications/the_52_week_high_and_momentum_investing` and confirm exit 0. (The two missing-file errors from audit 1 will already be gone because logs/audit1.md and SUMMARY.md now exist.)

### Minors (cleanup, do after the majors)
- m1: delete the empty nested `replications/the_52_week_high_and_momentum_investing/{...}/` tree at the slug root.
- m2: in results/table_*.md, annotate Tier-2 cells whose |ours/paper| > 2 (e.g. an extra note/flag) so "Tier 2" on a 7x cell doesn't mislead; no value change.
- m3: list results/table_3_dc_vs_cl.md as a diagnostic artifact in REPORT.md sec 6 (or move to results/diagnostics/).
- m4: linearize log1.md iteration-4/5/6 blocks (remove the out-of-order append at lines 302-316 and the "(pending)" placeholders).
- m5: fix the cumulative_wl.png caption in REPORT.md sec 4 — the figure shows MG 11.88x > JT 5.12x > WH 3.44x (all-months EW compound), so "(52WH dominates)" is wrong; reword to note the WH dominance lives in the ex-January/regression columns (figs 2-3).

## Iteration discipline reminders

- **Diagnose -> commit-fix -> fix -> verify.** Every new assumptions.md entry must carry all five fields (Diagnosis, Next fix, Before metric, After metric, Status). M2 and M3 already have a diagnosis and a stated Next fix from the previous run — your exit gate is to actually RUN them and record the After metric.
- **Read rep/STUCK_AGENT_GUIDELINE.md** on your first debug cycle.
- **10-iteration cap per problem**; a documented partial (as N1/N2 already are) beats a false success.
- **Re-run `scripts/prep_validation.py`** at the end and confirm exit 0 (M6).

## Inputs you should read

- replications/the_52_week_high_and_momentum_investing/logs/audit1.md (this audit)
- replications/the_52_week_high_and_momentum_investing/inputs/content.md (paper; Table VI L981-1095/1134-1268, Table IX L2176-2464)
- replications/the_52_week_high_and_momentum_investing/preparations/ (assumptions.md A11, A13; tables_to_replicate.json)
- replications/the_52_week_high_and_momentum_investing/src/tables_5.py (the FM engine to extend for M1/M4), src/main.py (g_gh for M2), src/tables_1_3.py (MG sort for M5)
- replications/the_52_week_high_and_momentum_investing/data/ (recompute spot-checks; do not rewrite the verified c-series values)

## What NOT to redo

- Do NOT re-derive the verified Tables I/II/III/V/VII numbers — the audit recomputed every cell from the caches (and FF3 from ClickHouse) and they match to 4 dp. Only CHANGE Table V if M3's rankable-only sensitivity justifies it, and only change the panel for M2/M4/M5 with a before/after guard that keeps the audited wh_* values stable.
- Skip re-reading SKILL.md and the ClickHouse catalog scan (data_verification.json is current).
- DO re-run any sanity check you add or modify — they are the regression gate.

## Deliverables for this iteration

- src/tables_5.py extended for (6,k,12) persistence -> results/table_6.md (M1)
- src/main.py g_gh variant B + regenerated panel + results/table_7.md (M2); results/table_9.md (M4)
- results/table_5.md with the rankable-only sensitivity + per-column dominance-ordering row (M3)
- MG industry-level cutoff sensitivity in results/table_1.md/table_5.md (M5)
- derived caches relocated + prep_validation exit 0 (M6)
- minors m1-m5 cleaned
- preparations/assumptions.md: a five-field log entry per addressed issue
- REPORT.md: lead with the data-quality summary and an explicit corollary-evaluated-this-iteration line (Table VI, Table IX, GH variant B, A13 sensitivity)
- Do NOT edit SUMMARY.md (the auditor owns it); the next audit rewrites it.

## Stop conditions

- All six majors addressed/verified and prep_validation exit 0 -> the next audit updates SUMMARY.md.
- If M2's variant B does not improve GH, keep strict-60 and document (non-actionable); if M3's sensitivity does not restore the Jan-incl margin, document the inversion (non-actionable). Documented partials are acceptable; do not loop past the 10-cap.
- If a blocker is ever found, stop and write a partial REPORT.md; do not edit SUMMARY.md.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is, on the engineering and documentation side, one of the more careful replications I have reviewed: the iteration log records genuine pre-registered adjudications (the wh_sig_dc lock via a 52-cell total-deviation comparison; the ret-vs-ret_dl delisting experiment with a transparent +6 Tier-1 criterion), every signal is brute-force-recomputed for sample permnos, and the c-series are deliberately exposed so an auditor can recompute any cell — which I did, and they all match. The weaknesses are scope and follow-through, not arithmetic: the agent committed to five tables at prep time and then treated the paper's third abstract claim (long-term non-reversal) and the 52-week-low robustness as if they didn't exist, and it left two of its own pre-committed fixes (GH variant B; the A13 rankable-only sensitivity) on the table. The net effect is that the paper's single most-cited dominance cell (Table V (6,6) raw Jan-included, WH 0.65 > JT 0.38) silently inverts in the replication — a fact the report mentions only in passing and never frames as the headline issue it is. None of this is a blocker (the committed cells are correct), but it is exactly the gap an outer iteration is for: add the two missing corollary tables, run the two deferred sensitivities, and make the validator green. I scored headline and signal strength at 3 rather than 4 to reflect the 25-31% shortfall on the Table V risk-adjusted WH spreads and the Jan-included ordering inversion; concrete results at 3 reflects the 65.5% Tier-1 rate under the committed per-cell tolerances (which are themselves loose on the small-magnitude dummies). The binary replication verdict is REPLICATED by the bright line; the audit verdict is PARTIAL with requires_iteration: true.
