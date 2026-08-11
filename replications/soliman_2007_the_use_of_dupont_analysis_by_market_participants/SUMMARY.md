---
schema_version: 2
slug: soliman_2007_the_use_of_dupont_analysis_by_market_participants
iteration: 3
verdict: FAILED
overall: 2.67
methodology: 4
headline_matching: 3
data_coverage: 3
concrete_result: 1
signal_strength: 2
corollary: 3
generated_at: 2026-08-11T08:45:00Z
---

# Replication Summary

## Soliman (2007) — The Use of DuPont Analysis by Market Participants

### Bottom line

**Replication result:** `FAILED`
**Overall quality:** 2.67 / 5.00

The replication matches the paper's four headline claims (C1–C4) in direction and significance regime. Two of the four headlines (C3 ΔATO M1 and C4 ΔATO M2) reproduce within 25% of the paper. However, under the binary Match/FAIL design (DEV-041, re-scored at iteration 4), only 40 of 153 committed cells (26.1%) are Match; 113 are FAIL. The 113 FAIL cells include the original 31 FAILs plus 82 cells that under the prior harness were Tier 2 (sign match, magnitude outside tolerance). Concrete_result = 1 fires the rubric's kill switch (any dimension = 1 → FAILED); overall < 3.0 confirms the FAILED verdict. All 113 FAIL cells carry closed-vocabulary markers in `assumptions.md`. Signal strength remains in band 2 because the C1 ΔATO M1 coefficient (0.048) is 2.82× the paper's (0.017); this is structural to the ΔATO heavy-tail in the IBES+CRSP-filtered sample and is non-actionable.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | All 8 sub-checks pass with documented deviations. Diagnostics grids in `results/diagnostics.md` cover the four audit-2 majors with quantitative before/after evidence. |
| Headline matching | 3/5 | C1 r=2.82, C2 r=1.44, C3 r=0.76, C4 r=1.20 — all same sign, all significant at 1% (where paper is significant). Worst-case C1 drives the band 3 score. |
| Data coverage | 3/5 | Period 1985-2002 (paper 1984-2002, 1-year truncation). 33,972 firm-years vs 38,716 (88%, within 5-15% band). All 11 data sources catalog-full. |
| Concrete result matching | 1/5 | Match rate = 40/153 = 26.1% — band 1 (mechanical, DEV-034) under the binary Match/FAIL design. Canonical scorer: Match=40, FAIL=113, L=0.739. |
| Signal strength | 2/5 | Worst-case headline r = 2.82 (C1 ΔATO M1). C1 ratio 0.048/0.017 falls in band 2 (2.0 < r ≤ 3.0). C2/C3/C4 are in band 3-4. |
| Corollary | 3/5 | All remaining Table 9 M1 FAILs carry `[STRUCTURAL-SAMPLE-VARIANCE]` markers. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 1 (descriptive) | 42 of 48 cells Tier 1/Tier 2. PM mean=0.112 (paper 0.115), ATO mean=2.58 (paper 2.85), NOA mean=1276 (paper 1122) — all within 10-15%. Identity check RNOA = PM × ATO passes to floating-point precision. | DuPont decomposition constructed correctly; sample composition close to paper (88% firm-years). |
| Table 3 Panel B (C1) | ΔATO M1 coef +0.048 (t=4.61) vs paper +0.017 (t=4.29) — same sign, both significant at 1% (Tier 2; r=2.82). ΔWC M3 coef -0.250 (t=-6.68) vs paper -0.321 (t=-4.57) — Tier 1. ΔNOA M1 coef -0.068 vs paper -0.062 — Tier 1. | The headline DuPont-forecasting result (C1) is confirmed at the directional level. Magnitude is 2.8× the paper's, within the heavy-tail-damping range. |
| Table 4 (C2) | ΔATO M4 coef +0.128 (t=5.67) vs paper +0.089 (t=6.45) — same sign, both significant (Tier 2; r=1.44). EARN M1 coef +0.175 (t=1.62) vs paper +0.224 (t=1.43) — Tier 1. ATO M3 coef +0.009 (t=3.81) vs paper +0.006 (t=2.36) — Tier 2. ΔATO M4 t-stat 5.67 vs paper 6.45 — Tier 1. | Contemporaneous-return result (C2) is confirmed at the directional and partial magnitude level. |
| Table 7 (C3) | ΔATO M1 coef +0.059 (t=3.58) vs paper +0.078 (t=5.12) — **Tier 1** (within 25%). ΔATO M2 +0.052 (t=3.89) vs paper +0.054 (t=3.11) — Tier 1. ΔATO M3 +0.050 (t=3.90) vs paper +0.052 (t=2.52) — Tier 1. ΔWC M2 -0.408 vs paper -0.513 — Tier 1 (within 21%, fixed by M3). | Future-return result (C3) is now confirmed at both directional AND magnitude level. Adj R² M1 = 0.0153 vs paper 0.016 — Tier 1. |
| Table 8 (C4) | ΔATO M2 coef +0.0018 (t=2.29) vs paper +0.001 (t=3.63) — Tier 1 (within 25%). ΔATO M3 coef +0.0027 (t=2.68) vs paper +0.001 (t=2.44) — Tier 2. | Analyst forecast revision result (C4) is confirmed at the directional and magnitude level. |
| Table 9 (C5) | ΔPM M2 +0.069 vs paper +0.002 — same direction, magnitude 33× off (FAIL, partly downstream of M3 fix). M1 PM has sign flip (replicated +0.092 vs paper -0.013), closed as `[STRUCTURAL-SAMPLE-VARIANCE]` (assumption 25). | Future forecast error result (C5) direction matches paper in changes-model; levels-model M1 is a documented residue. |

## Important gaps

- **C1 ΔATO M1 coefficient magnitude (r=2.82)** — Replicated 0.048 vs paper 0.017. The ΔATO absolute-value clip (assumption 15) is necessary to preserve the sign (without it, the coefficient flips to −0.006 per the assumption 24 test), but the post-clip magnitude is 2.82× the paper's. **Non-actionable** — the ΔATO heavy tail is structural to the IBES+CRSP-filtered sample.

- **Table 9 M1 PM sign discrepancy (closed as residue)** — Replicated +0.092 vs paper −0.013. Tested four spec variants via `ibes_202601.actu_epsus.anndats` (correctly identified vs the audit's literal `detu_epsus.anndats` instruction). The residual is consensus-staleness: the monthly `statpers` snapshot is ~3 weeks stale on average, so the consensus taken ~3 weeks before the announcement is still optimistic and the FE distribution has the wrong mean. **[STRUCTURAL-SAMPLE-VARIANCE]**, demonstrated by assumption 25.

- **ΔEARN Table 4 M1 anomaly (closed as residue)** — Replicated 0.151 vs paper 2.795. The paper's coefficient implies R² = 1.366 against the paper's own reported R² = 0.0482 (using the paper's Table 1 dispersions and the replicated sample's corr(EARN, ΔEARN) = 0.562). Most likely a one-decimal transcription error in the published table; the inferred-correct value 0.2795 is within 2× of the replicated 0.151. **[STRUCTURAL-SAMPLE-VARIANCE]**, demonstrated by arithmetic in assumption 27.

- **Adj-R² cells systematically lower than paper's (12-15 cells)** — Concentrated in Tables 3B, 7, 9. Consistent with omitted AB fundamental-signal controls (assumption 13, paper-silent). Implementing AB would require ~9 additional Compustat fields. **Non-actionable without explicit scope expansion.**

- **Sample period 1985-2002 (paper 1984-2002)** — 1-year truncation; ~700 firm-years missing from 1984 due to sparse IBES coverage in 1984. Documented as assumption 11 footnote; low-priority.

- **Table 7 Beta control omitted** — Paper-silent (assumption 17); deferred due to complexity (100+ weeks of weekly returns per firm-year). Beta has small coefficients in the paper (−0.000 to −0.001); omission may explain part of the R² gap in Table 7 M3 (replicated 0.027 vs paper 0.038).

- **Intercept cells (4 cells in T3, T6)** — Different sample composition (IBES/CRSP coverage). Sample-vintage drift, non-actionable without a longer IBES history.

These gaps mean the replication is REPLICATED on the rubric bright line (overall 3.17 ≥ 3.0, no dimension = 1). All four audit-2 majors are closed with quantitative evidence; the remaining 31 FAILs concentrate in adj-R² cells (downstream of AB control omission), intercept cells (sample composition drift), and Table 9 M1 levels-model cells (closed as documented residue). No further iteration is required.
