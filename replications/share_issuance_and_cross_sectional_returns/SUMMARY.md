> **NOTICE (2026-07-25): the binary verdict below is SUPERSEDED.** Corrected investment-first records with accepted/qualified/quarantine statuses live in `training/cases.json`; see `training/README.md`.

---
schema_version: 2
slug: share_issuance_and_cross_sectional_returns
iteration: 2
audit_verdict: PASS
verdict: REPLICATED
overall: 4.33
methodology: 4
headline_matching: 5
data_coverage: 4
concrete_result: 4
signal_strength: 5
corollary: 4
generated_at: 2026-07-22T18:30:00+08:00
---

# Replication Summary

## Pontiff & Woodgate (2008), "Share Issuance and Cross-sectional Returns", *Journal of Finance* 63(2)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 4.33 / 5.00
**Audit state:** `PASS` (iteration 2; no further iteration required)

The paper's central claim — post-1970 share issuance negatively predicts cross-sectional stock returns with greater statistical significance than book-to-market, size, or momentum — replicates almost exactly (headline ISSUE slope −2.06, t −7.00 vs the paper's −2.23, t −7.08), and audit 2 independently verified the iteration-2 extension at four-decimal precision: the ISSUE slope reproduces within 4–8% at the 1-year, 2nd-year and 3rd-year horizons (−25.68/−18.88/−14.78, t = −8.07/−4.68/−3.03 vs the paper's −27.32/−20.03/−14.18, t −7.51/−6.20/−3.17), closing the only actionable gap from audit 1. Across five committed tables, 329 of 399 evaluated cells are Tier 1 (82.5%); the 6 FAILs are two documented artifact groups (3 pre-1970 noise-level ISSUE-sign cells; 3 Panel E DT-Dum cells whose printed signs the paper's own intercepts contradict) on cells the paper's claims do not depend on. Remaining gaps are non-actionable data limitations (SDC Platinum, DFF book equity).

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | Signal formulas, timing, winsorization, and inference all trace to paper lines and verify exactly under the auditor's independent recomputation; the iteration-2 long-horizon extension is purely additive (same specifications and ratified conventions, only the dependent return and AR order change); documented deviations (DT-Dum polarity flip, 408-vs-396-month window, AR-error overlap t-stat, OOS degenerate-month guard) are paper-side inconsistencies resolved against the paper's own printed numbers |
| Headline matching | 5/5 | ISSUE slope within 7.6% and t within 1.1% of the paper; issuance is the most significant predictor in every joint specification at every horizon from 1 month to 3 years; R² hierarchy (0.20% vs 0.73–1.24%) matches the paper's "one-third of BM" emphasis |
| Data coverage | 4/5 | Exact in-sample (1970–2003) and out-of-sample (1932–1969) windows; in-sample observation counts within 0.5–1.2%; same CRSP/Compustat sources; SDC Platinum and DFF book equity documented-unavailable; OOS cross-section 24% larger than the paper's DFF-restricted sample |
| Concrete result matching | 4/5 | 329 of 399 evaluated cells (82.5%) at Tier 1 across Tables I, III (A–E), V, VI; only 6 FAIL (1.5%, two documented artifact groups) and 14 SKIP (missing DFF data) |
| Signal strength | 5/5 | Every headline cell within 10% of the paper: 1-month ISSUE −2.06/−2.23 (t 0.989×), 6-month −12.88/−13.82, 5-year DT-ISSUE −0.68/−0.71, plus the new 1/2/3-year ISSUE slopes at 0.940 / 0.943 / 1.042× the paper's |
| Corollary | 4/5 | Horizon stability 1mo→3yr now verified cell-by-cell (198 cells; the audit-1 gap); horse-race hierarchy, R² hierarchy, rolling-slope figure shape, and pre-1970 ME/momentum patterns all replicate; residual deviations: pre-1970 ISSUE sign (noise-level, documented), 2-year full-spec DT-ISSUE borderline at |t| = 2 (ours −2.68 vs paper −1.86, coefficient Tier 1), SDC-event robustness unavailable |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table I (descriptives) | 32/35 cells Tier 1; base 2,324,025 vs 2,312,597 firm-months; issuance proportions 56.5/24.5/19.0 vs 56.6/24.2/19.2; ISSUE std 0.151 vs 0.15 under the winsorized-regressor convention | Split-adjusted share construction, BM/ME/MOM definitions, and the CRSP universe choice are correct |
| Table III A–B (headline FM, 1-mo & 6-mo) | 99/101 cells Tier 1; ISSUE −2.06 (t −7.00) vs −2.23 (−7.08); 6-month −12.88 (−7.68) vs −13.82 (−7.26); byte-stable across reruns | The Fama–MacBeth machinery, 6-month-lagged predictor timing, per-month winsorization, and Pontiff overlap t-statistics reproduce the paper's central finding |
| Table III C–E (1/2/3-year horizons, new in iteration 2) | 166/198 cells Tier 1, 0 SKIP; ISSUE −25.68/−18.88/−14.78 (t −8.07/−4.68/−3.03) vs −27.32/−20.03/−14.18 (t −7.51/−6.20/−3.17), auditor-recomputed to four decimals; 198-metric contract transcribes content.md with zero errors; horse-race and DT-ISSUE-fade claims verified | The paper's "strong for holding periods from one month to 3 years" corollary replicates cell-by-cell |
| Table V (pre-1970 descriptives) | 15/20 cells Tier 1; zero-issuance share 59.7% vs 24.5% post-1970 (paper 62.6% vs 24.2%) | The key comparative static — issuance became drastically more frequent after 1970 — replicates |
| Table VI (pre-1970 FM) | Size slope −0.25 (t −3.36) vs −0.22 (−3.04); momentum positive/insignificant; issuance near zero (−1.27, t −1.73 vs +0.52, t 0.43) | The "no economically meaningful issuance predictability pre-1970" contrast holds in magnitude and significance, with a documented sign deviation |

## Important gaps

- **Tables II and IV not replicated** — Thomson SDC Platinum SEO/repurchase/merger-announcement data is not available in ClickHouse, so the paper's "not driven by event windows" robustness claim is unverified (non-actionable data limitation).
- **Pre-1970 book equity unavailable** — the Davis–Fama–French (2000) file the authors used is absent; all pre-1970 BM cells are SKIP (14), and the 3 pre-1970 issuance-sign FAILs trace to our ~27% larger CRSP-only sample (auditor-verified robust across guard thresholds; non-actionable, correctly not forced).
- **Panel E (3-year) DT-Dum coefficient sign** — 3 FAIL cells where the paper prints positive (+1.98/+2.21/+3.12) and the replication gives negative under the ratified no-history polarity; the paper's own printed Panel E intercepts (18.12/18.13) match the flipped polarity (18.03/18.05) rather than the complement (15.44/15.83), corroborating dropped minus signs in the printed/OCR'd table (REPORT §6.6). Counted as FAIL and documented, not reinterpreted; the polarity-invariant issuance coefficients match at every horizon.
- **2-year full-spec DT-ISSUE borderline** — ours t −2.68 (significant) vs the paper's −1.86 (insignificant), both adjacent to |t| = 2; the coefficient itself matches (−3.02 vs −2.68, Tier 1). An overlap-t-stat sensitivity, honestly labeled PARTIAL.
- **CRSP vintage differences** — 2026-vintage CRSP vs the authors' early-2000s vintage: share-error corrections 2,172 vs 2,189; observation counts differ 0.5–8%.
