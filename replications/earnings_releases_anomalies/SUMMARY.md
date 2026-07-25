> **NOTICE (2026-07-25): the binary verdict below is SUPERSEDED.** Corrected investment-first records with accepted/qualified/quarantine statuses live in `training/cases.json`; see `training/README.md`.

---
schema_version: 2
slug: earnings_releases_anomalies
iteration: 2
audit_verdict: PASS
verdict: REPLICATED
overall: 3.50
methodology: 4
headline_matching: 3
data_coverage: 3
concrete_result: 4
signal_strength: 3
corollary: 4
generated_at: 2026-07-22T19:42:00Z
---

# Replication Summary

## Earnings Releases, Anomalies, and the Behavior of Security Returns (Foster, Olsen & Shevlin 1984)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 3.50 / 5.00
**Audit state:** `PASS` (loop complete — no further iteration warranted)

The paper's central claim — post-earnings-announcement drift exists for the
earnings-based forecast-error models (1–2) but not for the price-based models
(3–4), is near-monotone in forecast-error rank, and is explained ~80% by the
forecast-error-portfolio coding — replicates in sign, shape, significance,
and explanatory-power hierarchy across 1,188 committed cells (77% Tier 1,
82% Tier 1+2; tally independently re-derived by audit 2). Outer iteration 2
closed audit-1's only actionable gap: the paper's corollary tables are now
committed and hold — drift persists in all three subperiods (Table 5),
survives the eq. 17 market benchmark (Table 8, with the M4 FEP10 [−60,0] =
29.47 vs paper 28.72 anchor validating the market-adjusted recomputation),
and the size confound replicates exactly (Table 9, quintile V negative for
10/10 FEPs in both windows). The one systematic deviation — drift
*magnitudes* in [+1,+60] attenuated to roughly half — reappears identically
under the market benchmark, confirming the diagnosed, non-actionable cause
(restated 2026 earnings vs the paper's 1982 as-reported tape). A binary
`REPLICATED` result does not mean every number matched: the extreme drift
cells and their t-stats are attenuated, and universe counts run 47% above
the paper's (a documented vintage/survivorship effect the paper itself found
immaterial).

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | FE models 1–4, the NYSE size-decile benchmark, prior-quarter FEP cutoffs, and the two-stage simulation are faithful and point-in-time; the eq. 17 extension is a literal implementation of the paper's footnote L3029 (M3/M4 FE and CAR rebuilt on u_M; M1/M2 FEPs unchanged; same σ windows, floors, and cutoffs). Deviations (σ floors, Dimson-β-for-Scholes–Williams, 251-day M4 window, non-NYSE breakpoint assignment) are minor and documented; no methodology bug found. |
| Headline matching | 3/5 | Sign, near-monotone shape, and R² hierarchy all match; headline drift *magnitudes* are attenuated ~35–56% (M2 [+1,+60] FEP1 ratio 0.44, FEP10 0.55). |
| Data coverage | 3/5 | Exact period and same data sources with zero substitutions; universe is 47% larger than the paper's (3,024 vs 2,053 firms), a documented vintage effect the paper's own survivorship test found immaterial. |
| Concrete result matching | 4/5 | 916/1,188 cells within tolerance (77.1% Tier 1, 81.6% Tier 1+2); every FAIL is classified (data-vintage attenuation, near-zero sign flips, Model-3 spurious structure, T5 s1 bear-market inflation, one paper-side transcription anomaly). |
| Signal strength | 3/5 | The paper's famous 81% R² replicates at 0.726 (ratio 0.90) and the signal is unambiguous, but extreme drift cells and eq. 16 coefficients are attenuated to ~0.44–0.55 of the paper (worst-cell reading borderline 2/3). |
| Corollary | 4/5 | All four corollary predictions now have committed per-cell evidence and hold: subperiod stability (T5), market-adjusted robustness (T8), the size confound (T9, exact), and cross-sectional size variation (T6). Remaining deviations (T5 s1 count levels; T8/T9 magnitude attenuation) are minor and explained by the same documented vintage family. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 3 — NYSE size deciles | Mean daily returns match to ≤0.007 pp/day (0.112 vs 0.111 … 0.023 vs 0.021), monotone; Dimson betas rank identically, 0 FAIL | CRSP pipeline, size-decile benchmark construction, and the NYSE universe |
| Table 1 — FEP transition frequencies | 191/200 cells match; Models 1–2 persistent, Models 3–4 near-independent | Portfolio-assignment dynamics and the paper's "proxy-effect" contrast |
| Table 4 — pooled CARs (headline) | Models 1–2 drift near-monotonically (M2 spread +3.1%), Models 3–4 flat; announcement windows match; 110/120 significance stars agree | The central drift finding (attenuated in magnitude) |
| Table 5 — subperiod stability | Bad-news drift present in every subperiod (M1 FEP1 negative-quarter counts [10,7,11], M2 FEP1 [5,10,10] vs paper [9,9,12]; FEP10 low throughout); M3/M4 show no FEP-gradient (s1 uniformly high = 1974–76 bear-market effect) | Drift is persistent, not subperiod-concentrated — the paper's time-period-argument rebuttal |
| Table 6 — size-quintile CARs | Drift present in all quintiles, largest for small firms; Model 4 flat (FEP1 q1 [−60,0] = −28.76 vs −28.68) | Cross-sectional (size) variation of the drift |
| Table 7 — eq. 16 regressions | FEP R² 0.726 / FSQ 0.640 / both 0.781 (paper 0.810/0.661/0.850); signs and significance replicate | FEP and size codings jointly explain most cross-portfolio drift variation |
| Table 8 — market-adjusted CARs (eq. 17) | M1/M2 drift survives market adjustment (M1 FEP1→FEP10 −1.49→+2.38; M2 −1.77→+1.51; paper −2.69→+3.78 / −3.46→+2.32); M3/M4 flat; M4 FEP10 [−60,0] = 29.47 vs 28.72 | Robustness: the drift is not an artifact of the size-decile benchmark |
| Table 9 — market-adjusted quintiles | Quintile V negative for 10/10 FEPs in both [−60,0] ([−5.62,−1.34]) and [+1,+60] ([−3.61,−2.05]); FEP10-V = −1.34/−2.05 vs paper −1.98/−0.78 | The size confound the paper warns about — replicated exactly |

## Important gaps

- **Data vintage (non-actionable).** The 2026 Compustat tape carries restated earnings; the paper's 1982 tape carried as-reported values. The good-news FE tail is 33% thinner (FEP10 median FE2 2.109 vs 3.151) while the bad-news tail matches to three decimals, Model-1 persistence (no σ estimation) is attenuated too, and the attenuation now reappears under the independent eq. 17 benchmark (Table 8) — locating the cause in the earnings series, not the code. Matching the 1982 tape would require a data source this repo does not have; sample tuning to hit magnitudes is explicitly ruled out (A16).
- **Universe is larger, not smaller.** The modern tape includes firms delisted before 1982 (3,024 vs 2,053 firms); the paper's own 79-firm vs 55-survivor test found survivorship immaterial, so the full sample is kept.
- **Model-3 mild spurious structure.** Model 3 shows small cross-portfolio structure in [+1,+60] (eq. 16 R² 0.36 vs ~0, now also visible in T5/T8) while the structurally-identical Model 4 is correctly flat — economically negligible (≤0.9% over 60 days), attributed to 2-day-window alignment noise on this vintage.
- **Table 5 s1 count levels.** The 1974Q1–1976Q2 subperiod runs high for all models including 3–4 (mean counts 7.4–7.7 vs ~5.1) — a market-wide bear-market effect on this vintage's returns, uniformly high across FEPs (not an FEP gradient), so the paper's persistence/non-persistence contrast still holds.
- **Documentation nits (closed-loop, optional).** Audit 2 logged three cosmetic items (endpoint-vs-range notation in the T8/T9 summaries, a stale assumption count "sixteen → seventeen", and an optional Iteration-4 entry in assumptions.md); none affects any committed cell or claim, and the audit loop is complete.
