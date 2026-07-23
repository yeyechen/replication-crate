---
iteration: 2
verdict: PASS
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — asset_growth_and_the_cross_section_of_stock_returns

**Verdict:** PASS
**Date:** 2026-07-23
**Auditor notes:** The single actionable major from audit 1 (M1, ISSUANCE split-adjustment) is genuinely fixed and every iteration-2 claim reproduced under independent re-derivation from the cached data and ClickHouse. The auditor (a) confirmed the CRSP `cfacshr` convention on the documented split stock from raw CRSP data, (b) recomputed the four split-adjusted ISSUANCE cells from `data/issuance_split_adjusted.parquet` to the reported precision (0.0709/0.3921/0.3212/7.81) and confirmed they are strictly closer to the paper (0.88–1.45×) than the raw values (1.85–3.91×), (c) confirmed the other 49 Table I cells are byte-identical, (d) recomputed `within_2x` for every non-Tier-1 cell and reconciled the strict tally 76/33/10 and tolerance tally 76/40/3, (e) re-verified pre-1971 Compustat missingness in `comp_202601.funda`, (f) confirmed the path fix + orphan removal, (g) reproduced the −106.47% event-time spread from the new cache with a bit-exact overlap, and (h) re-confirmed the Year-1 EW/VW spreads and an FF3 alpha. No result value changed; no new blocker or actionable major. The replication is at PASS quality and may be declared complete.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All six checks still pass; M1 resolved the one remaining definitional gap — ISSUANCE is now the paper-consistent split-adjusted 5-year share change, with the `shrout×cfacshr`-continuous convention independently verified on permno 10032 from raw CRSP; residual documented deviations (NW3 for Table II, full-universe signal sort, monthly-portfolio event time) unchanged |
| Headline matching | 4 | EW spread −1.7128 vs −1.73 (1.0%, exact to the eval JSON), VW −1.0328 vs −1.05 (1.6%), EW perfectly monotonic; EW FF3 all-firm alpha re-derived −1.4917 (eval −1.4874, paper −1.63); only the raw FM ASSETG coefficient drifts ~30% (t within 18%, winsorized coefficient matches) |
| Data coverage | 4 | Exact period (Jul 1968–Jun 2003; event window to Jun 2007, now cached); same CRSP/Compustat/FF sources with one documented equivalent substitution; vintage-shifted universe composition is the documented driver of level shifts |
| Concrete result matching | 3 | 76/119 (63.9%) strict Tier-1 (+2 from M1), top of the 50–70% band; 109/119 (91.6%) sign/pattern-correct under the strict convention; the 10 strict FAILs are all documented non-actionable causes (3 noise-level nulls, 5 pre-1971 data coverage, 2 vintage-attenuated t-stats) |
| Signal strength | 3 | Central return spreads r = 0.98–0.99 (near-exact) and EW alpha r = 0.91, but VW FF3 alpha 0.80, raw FM coefficient 0.70, and VW-spread Sharpe 0.66 remain inside [0.5,2.0] yet outside [0.8,1.2]; the signal is unambiguously present and strong |
| Corollary | 4 | All central corollaries computed and mostly replicate (subperiods incl. the paper's lone 1968–80 VW exception, size groups, FF4/FF5, 5-yr event-time persistence now cache-derivable, winsorization, monthly dependence, predictor dominance, decomposition); M1 strengthens the issuance characteristic; minor documented deviations in large-cap VW and accrual-linked components |

## 2. Issues by severity

### Blockers (must fix)

_None._

### Major (should fix)

_None actionable._ Audit-1 issues M1, M2, m1 are resolved (verified below); M3 remains a genuine non-actionable external limitation (pre-1971 Compustat missingness, re-verified this audit).

- [M3, carried; actionable: false] Pre-1971 Compustat missingness attenuates the five accrual/current-assets/other-assets cells. Auditor re-verified directly in `comp_202601.funda`: `ch` 93.3–94.3% null and `txp` 44.5–61.5% null in FY1966–68 (vs ~13%/6% by FY1974–75); `act` is well-populated but accruals/ΔCurAsst use (act−ch), so the ~93%-null `ch` thins the early cross-sections. Now correctly labeled as FAIL-with-documented-external-cause (5 cells). No honest fix exists.

### Minor (cleanup)

- [m5, new; informational only — not actionable, fully disclosed] In `results/table_1_eval.json` the tolerance-convention `tally` block (19/32/2) is not a pure recount of the per-cell `tier_tolerance` fields (which give 19/33/1): the m1 relabel moved `Leverage_spread_10_1`'s `tier` to FAIL and updated `tally`, but retained `tier_tolerance=Tier 2` as the historical lenient grade. This is explicitly documented in the JSON's `tally_note` and in `evaluation_summary.md` §2 ("one discrepancy vs the previously stored Table I tally (19/33/1/0) … the m1 relabel … moved one cell"). The headline strict tally (76/33/10, derived from the `tier` field) is internally consistent. No action required; noted for transparency.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | Re-derived from panel.parquet (offsets 0–11): EW Year-1 means strictly decreasing D1→D10 (2.02→0.31 %/mo), matching the paper's "perfectly monotonic" claim |
| 2 | Headline-magnitude claim | ✓ | EW spread −1.7128 (paper −1.73, 1.0%; exact to eval JSON), VW −1.0328 (paper −1.05, 1.6%); iid t 8.64 (paper 8.45); EW FF3 all-firm alpha re-derived −1.4917 (eval −1.4874, paper −1.63) |
| 3 | Sample coverage ≥ 60% | ✓ | 104,006 formation firm-years over 35 cohorts; panel 1,203,865 firm-months over 420 months; split-adjusted ISSUANCE coverage 70.4% (documented; t-stat improved despite lower coverage) |
| 4 | Data-source choice justified | ✓ | CRSP/Compustat/FF identical to paper; FF3 = Mkt-RF/SMB/HML/RF subset of `ff.four_factor_monthly` (verified: columns `dt,mkt_rf,smb,hml,rf,mom`, 1926-07→2025-10); split-adjustment via CRSP `cfacshr` on the same PIT link |
| 5 | prep_validation.py exit 0 | ✓* | Only remaining layout error is the missing `logs/audit2.md` (this file); the prep contract itself validates clean. Re-run after writing this audit + SUMMARY.md |
| 6 | All committed tables have results files | ✓ | T1–T4 each have `results/table_<n>.md` + `table_<n>_eval.json`; Table V exclusion documented |
| 7 | SUMMARY.md/REPORT.md matches results | ✓ | Spot-checked: strict 76/33/10 and tolerance 76/40/3 tallies reconcile with the four eval-JSON `strict_tally`/`tally` blocks; EW/VW spreads, FF3 alphas, ISSUANCE 0.0709/0.3921/0.3212/7.81, −106.47% cumulative all trace to results/ files |
| 8 | No orphan folders | ✓ | The empty nested `replications/<slug>/` tree is deleted (verified gone); no literal-brace folders anywhere in the slug; `src/main.py` now uses `parents[3]` + cwd-independent `REPLICATIONS_PATH`, and imports/layout resolve correctly from inside the slug |
| 9 | Diagnoses paired with fix attempts | ✓ | assumptions.md iteration entries 6–9 (M1, m2, m4, M2+m1) each carry all five fields (Diagnosis / Next fix / Before / After / Status) with concrete before/after metrics |
| 10 | Tier 2 within 2× magnitude | ✓ | Under the strict convention every Tier-2 *pattern* cell (28) has 0.5≤\|ours/paper\|≤2.0 (auditor recomputed all ratios); the 5 special Tier-2 cells are documented subtypes (3 near-zero-target, 1 near-zero-spread, 1 units); the 13 audit-1 out-of-2× cells are now correctly split into Tier-1 (2 ISSUANCE via M1 + within 2×), Tier-2 subtypes (4), and FAIL-with-cause (7) |
| 11 | Corollary coverage | ✓ | Unchanged from audit 1: every central paper corollary has a computed, checkable result; the 5-year event-time persistence (−106.47%) is now re-derivable from cache |

### Iteration-2 claim verification (re-executed by auditor)

| Claim | Result | Evidence |
|---|---|---|
| M1 — cfacshr convention | ✓ | From raw `crsp_202601.msf`, permno 10032: 1997 2:1 split `7246×4.0=28984 → 14492×2.0=28984` (continuous); 2000 2:1 split `18404×2.0=36808 → 37054×1.0=37054` (genuine ~0.7% change vs raw 2.01× jump). `shrout×cfacshr` is split-continuous, so `csho×cfacshr` removes splits |
| M1 — 4 ISSUANCE cells | ✓ | Recomputed from `data/issuance_split_adjusted.parquet` (time-series mean of yearly decile medians; spread t over 35 yrs): D1=0.0709, D10=0.3921, spread=0.3212, t=7.8138 — exact to reported. Ratios vs paper 0.0803/0.3012/0.2209/8.36 = 0.88×/1.30×/1.45×/0.93× (all within ~1.5×) vs raw 1.85×/3.36×/3.91×/1.45× — strictly closer |
| M1 — other 49 cells unchanged | ✓ | Recomputed all 11 non-ISSUANCE Table I columns (+ MV-AVG) from `data/formation.parquet` (unchanged, dated Jul 22): every D1/D10/spread/t matches `results/table_1.md` exactly. `ISSUANCE_raw` in the new parquet ≡ `formation.ISSUANCE` (raw retained); decile keys identical |
| M1 — tier moves | ✓ | In `table_1_eval.json`: ISSUANCE_D1 → Tier 1, ISSUANCE_t_spread → Tier 1, ISSUANCE_D10 → Tier 2 (pattern, 1.30×), ISSUANCE_spread → Tier 2 (pattern, 1.45×); each carries `raw_csho_value` |
| M2 — within_2x recomputed | ✓ | Auditor recomputed `within_2x` for all 43 non-Tier-1 cells (T1/T3/T4). All match the stored flag except two that follow the *documented* convention: `Leverage_t_spread` (opposite sign → `within_2x=false`, magnitude moot) and `M1_MV` (units subtype → `within_2x` computed in $billions = 0.83×, not the raw 0.001× ratio). Both correct, not errors |
| M2 — strict tally reconciles | ✓ | From the four `strict_tally` blocks: T1 19/29/5, T2 33/3/0, T3 22/1/3, T4 2/0/2 → 76 Tier-1 / 33 Tier-2 / 10 FAIL (119). Subtypes 28 pattern + 3 near-zero-target + 1 near-zero-spread + 1 units = 33; causes 3 noise + 5 data-coverage + 2 vintage = 10. Per-cell `tier` recount matches. Tolerance tally 76/40/3 also reconciles |
| M2 — every FAIL has documented cause | ✓ | All 10 strict FAILs carry a `cause`: 3 noise-level nulls (Leverage spread + t; M3 5YSALESG t), 5 data-coverage (ACCRUALS_D10, M6 ACCRUALS ×2, dOthAssets_alone, dCurAsst_full), 2 vintage attenuation (L2ASSETG_t 0.47×, ROA_t 0.42×, both spreads within-2× patterns) |
| M2 — no value changed | ✓ | Table I `ours` values all match the unchanged foundation parquet; ISSUANCE_D10=0.39212 and ASSETG_D1=−0.18175 reproduce; relabeling added only tier metadata (`tier`,`tier_tolerance`,`ratio_ours_paper`,`within_2x`,`subtype`,`near_zero_target`,`cause`,`strict_tally`) |
| M3 — pre-1971 missingness | ✓ | Re-verified in `comp_202601.funda`: FY1966/67/68 `ch` null = 94.0/94.3/93.3%, `txp` null = 61.5/58.3/44.5%, falling to ~13%/6% by FY1974–75 |
| m1 — Leverage relabel | ✓ | `Leverage_spread_10_1` now `tier=FAIL` (noise-level null), `reason_tolerance` retained ("lenient ~0 target … opposite sign but ours −0.016 is small"), `within_2x=false` |
| m2 — path fix + orphan gone | ✓ | `src/main.py:40` = `parents[3]` with documented comment; `REPLICATIONS_PATH` set via `os.environ.setdefault` for cwd-independence; orphan `replications/` tree deleted (verified absent); no literal-brace folders; `parents[3]` resolves to rep-it-up root with `utils/`; `paper_layout().root` = correct slug root; `utils.*` imports + `formation.parquet` resolve from inside the slug |
| m4 — cache reproduces −106.47% | ✓ | From `data/event_time_returns.parquet` alone (no live query), following Convention C (time-series mean at each of 60 offsets; annual = product of 12 monthly means −1; cumulative = product of 60 −1): EW D1=195.86%, D10=89.38%, spread=**−106.47%** (eval −106.4718). Overlap with `panel.parquet` bit-exact: 1,203,865/1,203,865 pairs matched, max\|Δret\|=0 |
| Headline foundation intact | ✓ | Year-1 EW spread −1.7128 / VW −1.0328 recompute exactly; EW strictly monotonic; EW FF3 all-firm alpha spread −1.4917 (eval −1.4874); formation.parquet/panel.parquet unchanged |

## 4. Issues the agent should have caught (didn't)

1. The one blemish this iteration: the Table I tolerance `tally` block (19/32/2) and the per-cell `tier_tolerance` fields (19/33/1) disagree by the single m1-relabel cell. It is disclosed in `tally_note` and `evaluation_summary.md` §2, so it is a transparency nit rather than a hidden error — but a cleaner choice would have been either to keep `tally` a pure recount of `tier_tolerance` (19/33/1) or to also flip that cell's `tier_tolerance` to FAIL. Not worth another iteration.
2. Nothing else material. The agent's anti-gaming stance held (no screens/filters added; only the documented split adjustment), the relabeling was value-preserving, and all four iteration-2 work items were executed and are independently reproducible.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

**No further iteration is required.** `requires_iteration: false`. Audit 2 verified that the single actionable major (M1) and all minors (m1, m2, m4) from audit 1 are genuinely resolved, that the relabeling (M2) is honest and value-preserving, and that no new blocker or actionable major exists. The replicator may declare the run complete.

If a human nonetheless wishes to commission one more *optional, non-required* pass, the only remaining value-additive item is the unreported-in-the-paper $10M total-assets robustness screen (content.md L1570): running it on this vintage and reporting whether the raw ASSETG Fama–MacBeth coefficient moves toward the paper's −0.0922 would further corroborate Assumption 7's vintage-tail explanation. This is explicitly optional and is **not** a condition for completion. The non-actionable items (Table V's missing SEO/repurchase announcement data; pre-1971 Compustat missingness) cannot be closed with the available data and should remain documented as limitations.

## 6. Auditor's notes (free-form)

Iteration 2 did exactly what a clean closing iteration should: it executed the one genuinely fixable definitional gap and relabeled honestly, without touching the verified foundation or gaming any cell. The M1 fix is the strongest evidence of good faith — rather than paper over the 1.85–3.9× ISSUANCE overshoot, the agent diagnosed it as a split artifact, validated the `shrout×cfacshr`-continuous convention on a documented split stock, and the split-adjusted column lands within 0.88–1.45× of the paper (two cells to Tier 1). I confirmed every one of these numbers independently from the cached parquet and from raw CRSP. The strict relabeling is equally honest: the published 76/33/10 tally now reconciles cell-by-cell against a recomputed 2× bound, the 10 FAILs each carry a documented non-actionable cause, and — importantly — no result value changed, which I verified by recomputing the Table I cells from the (byte-identical) foundation and reproducing the stored `ours` values. The decisive structural evidence from audit 1 still holds: the Year-1 EW spread recomputes to −1.7128 (exact) and is perfectly monotonic, so the signal, universe, timing, weighting, and delisting treatment are correct. The only residue is genuine data-vintage attenuation (pre-1971 `ch` ~93% null, re-verified) and one fully-disclosed tally nit. This is a faithful methodology replication of Cooper, Gulen & Schill (2008) whose central claims reproduce closely; it is at PASS quality and should be declared complete.
