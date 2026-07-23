---
iteration: 2
verdict: PASS
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — earnings_releases_anomalies

**Verdict:** PASS
**Date:** 2026-07-22
**Auditor notes:** Audit-1's single actionable major [M1] is remediated and
independently verified: Tables 5, 8, 9 are committed as per-cell-evaluated
tables (390 new cells, all 390 paper values re-parsed programmatically from
`inputs/content.md` and matched to the registry with zero transcription
errors), and the full 1,188-cell tally re-derives exactly (916 T1 / 54 T2 /
218 FAIL / 0 SKIP) with the CSV name set equal to the registry in order. All
four minors m1–m4 are closed. The corollary claims the paper makes on top of
its main result now have committed evidence and hold: drift survives the
eq. 17 market benchmark (T8), the size confound replicates exactly
(T9 quintile V negative for 10/10 FEPs in both windows), and the bad-news
drift persists across all three subperiods (T5). The core FE/sigma/alignment
logic is demonstrably untouched — the old five tables reproduce audit-1's
independently-verified 608/49/141/0 tally cell-for-cell. Remaining gaps are
three trivial documentation nits and the previously-established
non-actionable magnitude attenuation. No further iteration is warranted.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | Core logic unchanged (old-5 tallies identical to audit-1's verified 608/49/141/0). The eq. 17 mirror is faithful: u_M = ret − ewretd (dsi = the paper's L3023 EW NYSE+AMEX index); Models 3–4 FE *and* CAR recomputed on u_M per footnote L3029 while Models 1–2 keep earnings-based FEPs; same σ windows ([−251,−2]/[−311,−61]), same ≥100-day floors, same prior-quarter cutoff assignment, two-stage stars reapplied under u_M; subperiod splits match L1776 exactly (10/10/12 quarters). Deviations remain the documented minor ones (σ floors, Dimson β for the unstated SW variant, 251-day M4 window, M2 σ from 1974Q1 — the latter two now logged per m4). No methodology bug. |
| Headline matching | 3 | Unchanged and re-confirmed: sign, shape, and R² hierarchy match; headline drift magnitudes attenuated to ~0.44–0.65 of the paper. T8 shows the same attenuation profile under market adjustment (M2 endpoints −1.77/+1.51 vs paper −3.46/+2.32), consistent with the diagnosed vintage cause. |
| Data coverage | 3 | Exact period (1974Q1–1981Q4), same sources (fundq + dsf + dsenames + ccmxpf_lnkhist + dsi), zero substitutions; universe +47% (3,024 vs 2,053 firms) — a documented vintage/survivorship effect the paper itself tested and found immaterial (L288). |
| Concrete result matching | 4 | 916/1,188 = 77.1% Tier 1 (81.6% Tier 1+2), 218 FAIL — independently re-derived with the agent's exact tier function; per-table breakdowns (T1 191/7/2 · T3 15/15/0 · T4 90/3/27 · T5 97/0/23 · T6 174/6/64 · T7 138/18/48 · T8 94/2/24 · T9 117/3/30) reproduce exactly; all 54 Tier-2 cells satisfy the Tier-2 definition. |
| Signal strength | 3 | The paper's most-promoted statistic (81% R²) replicates at 0.726 (r = 0.90); β₁ r = 0.49; extreme drift cells r = 0.44–0.55. Worst-cell reading is borderline 2/3; sign, significance, and shape are unambiguous, and the attenuation is a diagnosed external (data-vintage) effect, so 3 stands (consistent with audit 1). |
| Corollary | 4 | All four identified corollaries now have committed per-cell evidence and hold: subsample stability (T5, M1/M2 bad-news drift in all three subperiods; M3/M4 no FEP-gradient), market-adjusted robustness (T8, drift survives; M3/M4 flat, M4 FEP10 [−60,0] 29.47 vs 28.72 validating the u_M rebuild), size confound (T9, quintile V 10/10 negative in both windows), and cross-sectional size variation (T6, prior). Deviations are 1–2 minor, well-explained ones (T5 s1 count levels; T8/T9 magnitude attenuation — both in the documented vintage family). |

## 2. Issues by severity

### Blockers (must fix)

- None.

### Major (should fix)

- None. Audit-1 [M1] is closed (see §3 spot-checks 1–5).

### Minor (cleanup; none warrants another iteration)

- [n1] Endpoint-vs-range notation in the T8/T9 summaries.
  - File: `logs/log2.md:64-70` and `REPORT.md:158-169` ("M2 −1.77…+1.51", "M3/M4 flat ([−0.97, +0.81] / [−1.11, −0.85])", quintile V "(−4.99…−1.34) and (−3.05…−2.05)").
  - Evidence: these pairs are the FEP1→FEP10 *endpoints*, not min/max. True extrema (verified from the CSV): T8 M2 [+1,+60] = [−2.09, +1.51] (min at FEP2); T8 M4 [+1,+60] = [−1.11, +0.62] (the M3 bracket happens to be a true range); T9 quintile V [−60,0] = [−5.62, −1.34] (min at FEP2), [+1,+60] = [−3.61, −2.05] (min at FEP4). All qualitative claims (drift intact; M3/M4 flat; V negative for all ten FEPs) are unaffected — this is notation precision only.
  - Specific fix (optional): say "FEP1→FEP10" explicitly, or quote true ranges. No code change.
- [n2] Stale assumption count in REPORT.md.
  - File: `REPORT.md:243` — "Sixteen paper-silent decisions are logged … (A1–A17)"; with A17 added there are seventeen.
  - Specific fix: "Seventeen".
- [n3] No Iteration-4 entry in assumptions.md for the T5/T8/T9 additions.
  - File: `preparations/assumptions.md` (ends at the Iteration-3 entries + m4 notes). Audit-1's deliverables list mentioned an Iteration-4 entry.
  - Evidence: the full trace is in `logs/log2.md` and the exit gate (every diagnosis paired with a fix attempt or non-actionable classification) is satisfied, so this is hygiene only. The additions were scope extension, not a debug cycle.
  - Specific fix (optional): append a short Iteration-4 entry (task/before/after: registry 798→1,188 cells, tally 608/49/141 → 916/54/218, all five audit-1 issues closed).

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Registry transcription of the 390 new paper values | ✓ | Parsed the paper's Table 5/8/9 HTML blocks from `inputs/content.md` programmatically; all 120 + 120 + 150 registry values match exactly (0 mismatches). Tolerances (T5: 100% throughout — justified, counts are vintage-sensitive; T8/T9: 50/100 mix mirroring T4/T6) and paper line refs (L1820+, L3071+, L3280+) are sensible. |
| 2 | Tier tally over all 1,188 cells | ✓ | Independent re-implementation of the tier rule + the T7 positional naming reproduces 916/54/218/0 and every per-table count exactly; CSV (table_id, metric_name) set equals the registry in order; all 54 Tier-2 cells satisfy sign-match + ratio ∈ [0.5, 2.0] (or the paper=0 convention), 0 violations. |
| 3 | Core logic untouched | ✓ | Old five tables tally 191+15+90+174+138 = 608 T1 / 49 T2 / 141 FAIL — identical to audit-1's independently re-verified tally, i.e. the committed values for T1/T3/T4/T6/T7 are unchanged; the new sections in `src/tables.py` are additive (Tasks A–C). |
| 4 | Table 5 independent recompute + claim | ✓ | Recomputed negative-quarter counts from `panel.parquet`: max deviation from CSV = 0.0. Subperiod splits match L1776 (7401–7602 / 7603–7804 / 7901–8104 = 10/10/12 q). M2 FEP1 = [5,10,10] vs paper [9,9,12]; FEP10 = [1,1,2] vs [1,0,0]; M1 FEP1 = [10,7,11] (bad-news drift in every subperiod). M3/M4 s1 means 7.70/7.40 vs paper 5.20/5.00 (uniformly high across all FEPs — 1974–76 bear-market vintage effect, not an FEP gradient; s2/s3 means ≈ paper: 4.50/4.20 vs 4.20/3.70, 5.10/5.80 vs 6.20/6.20), consistent with the paper's "found … for Models 1 and 2 but not for Models 3 and 4". |
| 5 | Tables 8–9 independent recompute + claims | ✓ | Recomputed all T8/T9 cells from `data/cache/market_adjusted.parquet` + panel FEPs: max deviation ≈ 4e-15. T8: M1 [+1,+60] FEP1→FEP10 = −1.49→+2.38 (paper −2.69→+3.78), M2 −1.77→+1.51 (−3.46→+2.32) — drift survives; M3 true range [−0.97,+0.81], M4 [−1.11,+0.62] vs paper M4 [−1.09,+0.37] — flat. Anchor M4 FEP10 [−60,0] = 29.47 vs paper 28.72 (ratio 1.03) — externally validates the u_M recomputation including the M3/M4 FE rebuild. T9: quintile V negative for 10/10 FEPs in [−60,0] ([−5.62,−1.34]) and 10/10 in [+1,+60] ([−3.61,−2.05]); FEP10-V = −1.34/−2.05 vs paper −1.98/−0.78 — the L3027 confound claim replicates exactly. |
| 6 | eq. 17 methodology fidelity | ✓ | `market_index.sql` pulls `crsp_202601.dsi.ewretd` — the paper's "equally weighted return on CRSP daily file (NYSE and ASE firms)" (L3023, A13). Models 1–2 keep earnings-based FEPs; Models 3–4 recompute FE and CAR on u_M per footnote L3029, with the same σ windows ([−251,−2] / [−311,−61]) and ≥100-day floors as the main pipeline (`src/main.py:456-472` vs `src/tables.py:535-544`), and the identical prior-quarter cutoff algorithm (same CUTOFF_Q0/Q1, same lexsort edge construction; 1973Q4 cutoff obs recovered from obs_id). T4↔T8 coherence is sensible (M4 FEP10 [−60,0]: 28.17 size-adjusted vs 29.47 market-adjusted — large firms; M2 p1_60 endpoints shift modestly, as expected). |
| 7 | Audit-1 minors closed | ✓ | m1: both Iteration-2 after-metrics filled (Dimson 1.35→0.91, 0 FAIL; stars 109→110/120), statuses `resolved`, Iteration-3 entry present with all five fields. m2: A17 added with decision/rationale/impact (`assumptions.md:143-147`). m3: REPORT.md §3.3 now says "near-monotone … the only deviations are at the zero-crossing portfolios (M2 FEP5, M1 FEP6) and M1 FEP10<FEP9" — verified against the CSV (M2 FEP5 = −0.14 vs +0.22; M1 FEP6 = −0.09 vs +0.55; M1 FEP10 1.22 < FEP9 1.75). m4: both one-line notes present (`assumptions.md:157-161`). |
| 8 | REPORT/README ↔ results consistency | ✓ | Sampled: 110/120 stars (`table_4.md:24`); M2 [+1,+60] eq. 16 FEP R² 0.726 / FSQ 0.640 / both 0.781, β₁ 0.33 (t 11.45), β₂ −0.31 (t −9.39) (`table_7.md:48-54`); the §3 tally table matches my re-derivation exactly (incl. the 77%/5%/18% percentages). All eight `table_*.md` files present; slug root clean (data, inputs, logs, preparations, results, src, REPORT.md, SUMMARY.md). |
| 9 | prep_validation.py | ✗ → ✓ | Fails before this audit on exactly one expected layout rule ("log2.md exists but audit2.md is missing"); resolved by this audit. |
| 10 | Magnitude diagnosis still stands | ✓ | The 218 FAILs decompose into the same documented families as iteration 1 (drift-magnitude attenuation in T4/T6/T7/T8/T9; near-zero sign flips on paper-insignificant cells; M3 mild spurious structure, now also visible in T5/T8; T5 s1 bear-market inflation; the m1_fep3_p1_60 paper anomaly). No new undiagnosed failure class; audit-1's falsification chain (asymmetric FE tails, σ-free M1 persistence also attenuated, announcement window *not* attenuated, CRSP-only Table 3 near-exact) is untouched and the new tables corroborate it: the attenuation reappears under a completely different benchmark (T8), exactly as a restated-earnings cause predicts and a benchmark-construction bug would not. |

## 4. Issues the agent should have caught (didn't)

1. The endpoint-vs-range notation ([n1]): the series were computed in full, so a self-check of "−4.99…−1.34" against the actual quintile-V column (min −5.62 at FEP2) would have flagged that these are FEP1→FEP10 endpoints. Harmless, but "…" reads as min/max.
2. The stale "Sixteen … (A1–A17)" count in REPORT.md §5 ([n2]).

Both are cosmetic; neither affects any committed cell or claim.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are looking at the replication of "Earnings Releases, Anomalies, and the
Behavior of Security Returns" (Foster, Olsen & Shevlin 1984), slug
`earnings_releases_anomalies`. Audit 2
(`replications/earnings_releases_anomalies/logs/audit2.md`) returned verdict
**PASS**, blocker_count 0, actionable_major_count 0,
**requires_iteration: false**. The replicator-auditor loop is COMPLETE — do
NOT start another iteration.

**No code or data changes are needed.** The replication stands at 1,188
committed cells (77% Tier 1 / 82% Tier 1+2), every qualitative claim
verified, the drift-magnitude attenuation documented as a non-actionable
data-vintage effect, and all corollary tables (T5 subperiod stability,
T8/T9 market-adjusted robustness and size confound) committed and holding.
Do NOT try to improve the drift magnitudes — tuning the sample to hit the
paper's numbers would be gaming (A16).

If — and only if — a human explicitly asks for a final documentation polish,
the three optional nits are (docs only, no code, no pipeline re-run):

- [n1] In `logs/log2.md:64-70` and `REPORT.md:158-169`, the T8/T9 "range"
  quotes (M2 "−1.77…+1.51", M4 "[−1.11, −0.85]", quintile V "(−4.99…−1.34)"
  / "(−3.05…−2.05)") are FEP1→FEP10 endpoints, not min/max. True extrema:
  T8 M2 [+1,+60] [−2.09, +1.51]; T8 M4 [+1,+60] [−1.11, +0.62]; T9 qV
  [−60,0] [−5.62, −1.34], [+1,+60] [−3.61, −2.05]. Say "FEP1→FEP10" or quote
  true ranges.
- [n2] `REPORT.md:243`: "Sixteen paper-silent decisions … (A1–A17)" →
  "Seventeen".
- [n3] Optionally append an Iteration-4 entry to
  `preparations/assumptions.md` mirroring `logs/log2.md` (registry
  798→1,188 cells; tally 608/49/141 → 916/54/218; audit-1 issues closed).

If you make any of those edits, re-run `scripts/prep_validation.py
earnings_releases_anomalies` and confirm exit 0. The auditor-owned
`SUMMARY.md` must NOT be edited.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This iteration did exactly what audit 1 prescribed — no more, no less — and
it did it cleanly. The three corollary tables are the right ones (the paper's
own Table 5 and the eq. 17 appendix Tables 8–9, not ad-hoc robustness), every
one of the 390 new paper values was transcribed without error, the Models-3/4
FE/CAR rebuild under u_M follows the paper's footnote L3029 literally, and
the pipeline extension is strictly additive: the old five tables' 608/49/141
tally — which I re-verified cell-by-cell in audit 1 — reproduces identically,
so nothing previously audited was disturbed. The new evidence also
*strengthens* the deviation diagnosis: the same ~0.5 attenuation reappears
under the market benchmark (T8), which a benchmark-construction bug could not
produce, and the M4 FEP10 [−60,0] = 29.47 vs 28.72 anchor (ratio 1.03)
independently validates the u_M recomputation end-to-end. The honest handling
continues throughout: the T5 s1 bear-market inflation and the M3 spurious
structure are surfaced rather than buried, and the paper's −7.58 anomaly is
still counted as a FAIL. Corollary moves 3→4 and overall 3.33→3.50; the
replication is REPLICATED by the bright line (mean ≥ 3.0, no dimension at 1)
and the audit loop closes with verdict PASS. The residual magnitude gap is a
property of the 2026 Compustat tape, not of this replication.
