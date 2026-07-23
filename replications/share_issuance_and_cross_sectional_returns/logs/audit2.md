---
iteration: 2
verdict: PASS
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — share_issuance_and_cross_sectional_returns

**Verdict:** PASS
**Date:** 2026-07-22
**Auditor notes:** The single actionable major from audit 1 ([M1], Table III Panels C–E uncomputed) is resolved and independently verified. My own Fama–MacBeth implementation on `data/panel.parquet` reproduces the new R5 ISSUE slopes at all three horizons and the full Panel C R8 row to four decimals, the 198-metric T3cde contract transcribes content.md with zero errors (machine-parsed), the three paper horizon-claims verify, and all prior outputs are byte-stable. The Panel E DT-Dum FAIL treatment is honest — new intercept evidence makes the paper-side-artifact diagnosis stronger than the agent even claimed. No actionable issues remain; the three standing majors are the auditor-confirmed non-actionable data limitations.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All six checks pass; the long-horizon extension is purely additive (same SPECS, same ratified conventions, only the dependent return and AR order change); all documented deviations (DT-Dum flip, 408 vs 396 months, GLSAR AR-error form, OOS degenerate-month guard) remain paper-side inconsistencies resolved against the paper's own numbers |
| Headline matching | 5 | Headline ISSUE slope within 7.6% and t within 1.1% of the paper (unchanged, byte-stable); ISSUE is the most significant predictor in every joint spec at every horizon |
| Data coverage | 4 | Exact in-sample and OOS periods; in-sample counts within 0.5–1.2%; same CRSP/Compustat sources; SDC and DFF book equity documented-unavailable; OOS cross-section 24% larger than the paper's DFF-restricted sample |
| Concrete result matching | 4 | 329/399 evaluated cells Tier 1 (82.5%) across five tables; 6 FAIL (1.5%, two documented artifact groups); 14 SKIP (DFF) |
| Signal strength | 5 | All headline cells within [0.9, 1.1]: A-R5 ISSUE 0.924 / t 0.989; B-R5 0.932 / t 1.058; R6 DT-ISSUE 0.958; the new long-horizon ISSUE slopes are 0.940 / 0.943 / 1.042 of the paper's |
| Corollary | 4 | Horizon stability 1mo→3yr now verified cell-by-cell (the audit-1 gap); horse-race hierarchy, R² hierarchy, Figure 1 shape, OOS ME/MOM patterns all replicate; residual deviations: OOS ISSUE sign (noise-level, documented), 2-year R8 DT-ISSUE borderline (ours t −2.68 vs paper −1.86, both adjacent to |t|=2), SDC robustness unavailable |

**Overall: 4.33 / 5.00 — REPLICATED** (mean ≥ 3.0, no dimension at 1; up from 4.17 — corollary 3→4)

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

- [M1] — RESOLVED this iteration. See §3 checks 1–3.

- [M2] Pre-1970 ISSUE sign deviation (3 FAIL cells, Table VI). NON-ACTIONABLE (standing, auditor-confirmed in audit 1). DFF book equity not in ClickHouse; the sign is robustly negative at every guard threshold in our ~27% larger CRSP-only sample; correctly documented, not forced.
- [M3] Tables II and IV not replicated (Thomson SDC Platinum unavailable). NON-ACTIONABLE (standing).
- [M4] Pre-1970 BM cells SKIP (DFF 2000 book equity unavailable; 14 SKIP cells). NON-ACTIONABLE (standing).
- [M5] Panel E (3-year) DT-Dum coefficient sign (3 FAIL cells: pE_r6/r7/r8_dt_dum, ours −2.59/−2.21/−1.88 under the ratified flip vs paper +1.98/+2.21/+3.12). NON-ACTIONABLE — paper-side artifact, verified below. No legitimate fix exists short of reinterpreting printed signs per-horizon, which would be fitting to the target.
  - Why it is paper-side (auditor's new evidence): flipping a 0/1 dummy changes ONLY the intercept and the DT-Dum coefficient, with intercept_as-built = intercept_flipped + coef_flipped. The paper's OWN printed Panel E intercepts pin the polarity: E-R6 18.12 and E-R7 18.13 match our FLIPPED intercepts (18.03 / 18.05, ≤0.5% dev), NOT the as-built intercepts my recomputation gives (15.44 / 15.83, ~15% dev). Yet the printed DT-Dum coefficients carry the as-built sign — and for R7 the magnitude is IDENTICAL to ours (|−2.2135| = 2.21 to the printed 2.21). A printed row whose intercept implies one polarity and whose DT-Dum sign implies the other is internally inconsistent; the only coherent explanation is dropped/flipped minus signs on the printed/OCR'd Panel E DT-Dum cells, exactly as REPORT §6.6 states. R8 is noisier (paper DT-Dum 3.12 vs our |1.88| either polarity; intercept 21.90 between our 21.34/23.22) but the polarity-invariant ISSUE/DT-ISSUE coefficients match (−9.42 vs −9.00; −1.74 vs −2.14).
  - Honesty assessment: the agent kept ONE ratified polarity across all five horizons, counted the 3 cells FAIL, did not reinterpret, and the diagnosis is now corroborated by the paper's own numbers. This is the opposite of target-fitting.

### Minor (cleanup)

- [m1] REPORT.md §5 header reads "full registry: preparations/assumptions.md, A1–A21" but A22 was added this iteration (22 entries). Specific fix: "A1–A22".
- [m2] REPORT.md §7 file list omits `results/table_3_cde.md` ("results/table_{1,3,5,6}.md, …"). Specific fix: add table_3_cde.md to the list.
- [m3] (informational, no action required) `results/issue_rolling_slope.png` bytes differ between the worker's build environment and the auditor's environment (matplotlib font-cache dependent; same 165,678-byte size, deterministic "Software" metadata only), while all six result markdown files are byte-identical across three consecutive auditor reruns (md5-verified). The pipeline is deterministic within a fixed environment; the tables that carry the evidence are fully byte-stable.
- [m4] (carried from audit 1, accepted as-is) optional noise-level annotation of near-zero OOS cells — no score impact.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | **[M1] fix — R5 ISSUE slopes, independent recomputation** | ✓ | Auditor's own FM code on `data/panel.parquet` (408 months, univ_all, 1%/99% per-month winsorization, GLSAR AR(k−1)-error, DT-Dum flipped): C-R5 ISSUE = **−25.6768 (t −8.0675)** vs table_3_cde.md −25.68 (−8.07) vs paper −27.32 (−7.51); D-R5 = **−18.8774 (t −4.6842)** vs −18.88 (−4.68) vs paper −20.03 (−6.20); E-R5 = **−14.7759 (t −3.0343)** vs −14.78 (−3.03) vs paper −14.18 (−3.17). Exact 4-decimal agreement with the agent's output at every horizon; coefs within 4–8% of the paper |
| 2 | **[M1] fix — full R8 row, independent recomputation** | ✓ | Panel C R8 (all 7 regressors): intercept 33.3866 (3.9025), BM 2.5630 (2.5261), BM Dum 5.6853 (5.5237), ME −1.6879 (−2.6914), MOM 6.8846 (3.1011), ISSUE −15.3977 (−8.1275), DT-ISSUE −3.6166 (−3.1717), DT-Dum −2.8692 (−2.2245), R² 4.49, N = 2,182,151, 408 months — every cell matches table_3_cde.md exactly; D/E R8 DT-ISSUE t = −2.6801 / −1.6923 also match |
| 3 | **T3cde contract (198 metrics) transcription** | ✓ | Auditor parsed all four source HTML tables out of content.md (Panel C L1503, Panel D L1698, Panel E rows 1 L1897 + rows 2–8 page-14 continuation L1952) and compared every one of the 198 contract metrics: **0 mismatches**. The `PAPER_CDE` dict in analyze_tables.py: 0 mismatches vs parsed source. The rendered "Paper targets" grids in table_3_cde.md: 198/198 cells match the parsed source. The full chain content.md → contract → code → results file is exact |
| 4 | **Paper claim (i): ISSUE negative at all horizons** | ✓ | My estimates: −25.68 / −18.88 / −14.78 (t −8.07 / −4.68 / −3.03); also negative in R7/R8 at every horizon |
| 5 | **Paper claim (ii): \|t_ISSUE\| > \|t_BM\|, \|t_ME\|, \|t_MOM\| univariate** | ✓ | My estimates at all three horizons: C 8.07 > 4.32/2.11/3.44; D 4.68 > 4.49/1.66/1.78; E 3.03 > 2.24/1.13/2.31. The paper's OWN printed 3-year values violate their claim (ISSUE \|t\| 3.17 < BM \|t\| 3.87, verified from parsed content.md) — honestly flagged in table_3_cde.md and REPORT §3 |
| 6 | **Paper claim (iii): DT-ISSUE significance pattern in full (R8) specs** | ✓ (partial, honest) | 1-yr R8 t = −3.17 (significant, paper −2.60 significant); 3-yr R8 t = −1.69 (insignificant, paper −1.27 insignificant); 2-yr R8 t = −2.68 where the paper prints −1.86 — both adjacent to \|t\| = 2 (overlap-t-stat sensitivity), the coefficient matches (−3.0171 vs −2.68, 12.6%, Tier 1). Labeled ⚠️ PARTIAL, not forced |
| 7 | **Existing tables byte-stable** | ✓ | md5 of table_1.md / table_3.md / table_3_cde.md / table_5.md / table_6.md / panel_report.md identical across three consecutive reruns of `src/analyze_tables.py`; console tally reproduces 32/3/0/0 + 99/2/0/0 + 166/29/3/0 + 15/5/0/2 + 17/11/3/12 = **329/50/6/14 over 399 cells** exactly as REPORT §1 claims. PNG figure stable across consecutive runs (one-off cross-environment byte difference — [m3]) |
| 8 | **Panel E DT-Dum FAIL honesty** | ✓ | See [M5]: one ratified polarity everywhere; 3 cells counted FAIL; intercept evidence (paper 18.12/18.13 ≈ flipped 18.03/18.05, not as-built 15.44/15.83) and the R7 exact-magnitude sign flip (2.2135 vs +2.21) corroborate a paper-side dropped-minus-sign artifact. No target-fitting |
| 9 | **A22 assumption entry** | ✓ | All five fields present (Diagnosis / Next fix / Before: 163/21/3/14 over 201 cells, 0/3 panels / After: 166/29/3/0 T3cde, 329/50/6/14 over 399, 3/3 panels / Status: RESOLVED); before/after metrics match the rerun console |
| 10 | **Audit-1 minors closed** | ✓ | [m1] nested `replications/` skeleton deleted (no longer exists; no empty or literal-brace dirs anywhere in the slug); [m2] §6.3 now reads "our 464,718 firm-months vs their 373,590"; [m3] §6.5 "OCR ambiguous" claim replaced with the computed C–E results and a new §6.6 |
| 11 | **Tier classification spot-checks (T3cde)** | ✓ | pC_r8_issue_t: paper −5.61 vs ours −8.13 (44.9% > 40%, same significance class) → Tier 2 ✓; pD_r8_dt_dum: −0.80 vs −2.49 (same sign) → Tier 2 ✓; pE_r6_dt_dum: +1.98 vs −2.59 (sign flip, coefficient metric) → FAIL ✓; pE_r5_issue: −14.18 vs −14.78 (4.2%) → Tier 1 ✓ |
| 12 | **prep_validation.py** | ✓ (after deliverables) | Fails before this audit writes audit2.md (log2.md has no matching audit — the loop's own integrity check); passes after audit2.md + SUMMARY.md are written |

**Additional independent micro-checks (auditor's own code, this iteration):**
- As-built polarity on Panel E R6/R7/R8: DT-Dum = +2.5908 (t 0.90) / +2.2135 (t 0.86) / +1.8792 (t 1.64) with intercepts 15.44 / 15.83 / 21.34 — confirming the flip identity (as-built intercept = flipped intercept + flipped DT-Dum coef) and that the paper's printed intercepts follow the flipped polarity at the 3-year horizon too ✓
- Horse-race t-stats recomputed independently for R1/R2/R3 at all three horizons; claim (ii) holds on my numbers at every horizon ✓
- R5 observation count 2,203,273 and R8 count 2,182,151 reproduced exactly at all three horizons ✓

## 4. Issues the agent should have caught (didn't)

1. **Stale cross-references after adding A22/table_3_cde.md** — REPORT §5 still says "A1–A21" (22 entries now exist) and the §7 reproducibility file list omits `results/table_3_cde.md` ([m1]/[m2]). Cosmetic; no iteration required.
2. Nothing substantive — the worker correctly declined the stretch goal (OOS multi-horizon Panels B–E) under its stability mandate, and the decision is documented with a defensible rationale in log2.md.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are closing out the replication of "Share Issuance and Cross-sectional Returns" (Pontiff & Woodgate 2008), slug `share_issuance_and_cross_sectional_returns`. Audit 2 (`replications/share_issuance_and_cross_sectional_returns/logs/audit2.md`) returned verdict **PASS** (4.33/5.00, REPLICATED, 0 blockers, 0 actionable majors, `requires_iteration: false`). The single actionable major from audit 1 (Table III Panels C–E) was resolved last iteration and independently verified by the auditor at four-decimal precision.

**No further replication work is required.** Apply only these two cosmetic REPORT.md fixes and stop:

1. REPORT.md §5 header: change "full registry: preparations/assumptions.md, A1–A21" → "A1–A22" (A22 was added in outer iteration 2).
2. REPORT.md §7 file list: add `results/table_3_cde.md` to the results-file bullet (currently lists only `table_{1,3,5,6}.md`).

### Do NOT touch (verified, ratified, byte-stable)

- `src/main.py`, `src/sql/`, `data/panel.parquet` — panel build verified exact at the security level.
- `src/analyze_tables.py` — all five tables reproduce byte-identically across reruns; the auditor's independent Fama–MacBeth matches the new Panels C/D/E to four decimals.
- `preparations/tables_to_replicate.json` — the 198-metric T3cde entry transcribes content.md with zero errors (auditor machine-parsed the source HTML).
- Conventions A1–A22, the 329/50/6/14 tally, and the documented limitations (OOS ISSUE sign, SDC Tables II/IV, DFF book equity, Panel E DT-Dum paper-side artifact) — all confirmed correct and honestly handled; do not attempt sample restrictions or per-horizon sign reinterpretations.

### Iteration discipline reminders

- If you touch REPORT.md, re-run `python scripts/prep_validation.py replications/share_issuance_and_cross_sectional_returns/` and confirm exit 0.
- SUMMARY.md is auditor-owned — do not edit it.
- This is the terminal iteration unless a future audit reopens the slug.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This iteration is exactly how the loop is supposed to work. The replicator accepted the audit-1 finding without defensiveness, correctly identified that its own earlier "OCR ambiguous" claim was wrong, and closed the gap additively — no ratified convention was touched, the four existing table files are byte-identical, and the new 198-cell contract transcribes the source with zero errors (I verified this by parsing the HTML out of content.md myself rather than trusting the agent's tables). The results are genuinely strong: the ISSUE slope reproduces within 4–8% at every horizon from 1 month to 3 years (t = −8.07/−4.68/−3.03 vs the paper's −7.51/−6.20/−3.17), and the horse-race claim holds on our estimates even at 3 years, where the paper's own printed t-stats marginally violate it — a paper-side anomaly the agent flagged rather than hid.

The judgment call worth recording is the Panel E DT-Dum FAIL group. My independent recomputation makes the agent's §6.6 diagnosis stronger than the agent itself argued: the paper's printed Panel E intercepts (18.12/18.13) match the ratified flipped-polarity intercepts (18.03/18.05) and are ~15% away from the as-built ones (15.44/15.83), while the printed DT-Dum coefficients carry the opposite sign — with R7's magnitude identical to ours (2.2135 vs +2.21). A table row cannot be internally consistent with both polarities; the coherent reading is dropped minus signs on the printed/OCR'd Panel E DT-Dum cells. The agent kept one polarity everywhere, counted the cells FAIL, and refused to reinterpret per-horizon — the disciplined choice, and the opposite of fitting to the target.

What keeps this from a perfect score is not the agent's work but the data: SDC Platinum and the DFF book-equity file are genuinely absent, the pre-1970 ISSUE sign deviates at noise level in our larger sample (correctly not forced), and the 2-year DT-ISSUE t-stat lands one side of the |t| = 2 line where the paper lands on the other — an overlap-adjustment sensitivity honestly labeled PARTIAL. The two stale REPORT cross-references ([m1]/[m2]) are cosmetic. Verdict: PASS, no further iteration required.
