> **NOTICE (2026-07-25): the binary verdict below is SUPERSEDED.** Corrected investment-first records with accepted/qualified/quarantine statuses live in `training/cases.json`; see `training/README.md`.

---
schema_version: 2
slug: do_industries_explain_momentum
iteration: 2
audit_verdict: PASS
verdict: REPLICATED
overall: 4.00
methodology: 4
headline_matching: 4
data_coverage: 5
concrete_result: 3
signal_strength: 4
corollary: 4
generated_at: 2026-07-22T19:40:00Z
---

# Replication Summary

## Do Industries Explain Momentum? (Moskowitz & Grinblatt, 1999)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 4.00 / 5.00 (up from 3.83 in audit 1; corollary 3 → 4)
**Audit state:** `PASS` (iteration 2; 0 blockers, 0 actionable majors, no further iteration required)

The paper's claim that a strong industry momentum accounts for much of individual stock momentum is **partially reproduced**. The unconditional pillars — the 20-industry construction, the ~0.4%/mo individual and industry momentum profits, the DGTW adjustment, the full horizon grid, and the central Fama-MacBeth result that industry momentum subsumes 6-month individual momentum while 12-month momentum survives — all replicate at Tier 1 and were independently re-verified from the cached data. **Since audit 1, the abstract's long/short leg-asymmetry corollary has been computed, reported, and independently re-verified by the auditor**: individual momentum is loser-driven (short leg +0.40%/mo, t=2.64 vs long +0.02%, t=0.11), industry momentum is long-driven (+0.23%, t=2.34 vs +0.17%, t=1.89), and the (1,1) industry strategy is balanced (|Δ| = 0.10 pp) — all three claims match the paper, with the leg-derived spreads reproducing the frozen Table II/III values to machine precision. The portfolio-level decomposition claim (industry adjustment *eliminates* individual momentum) does not hold in the 2026 CRSP vintage, which contains ~3.5× stronger within-industry momentum; this is a documented external data limitation, not an implementation error. A binary `REPLICATED` verdict means the headline numbers and central econometric result reproduce — not that every one of the 814 reported cells matched exactly (half are exact Tier-1 matches; the rest are near-zero controls and documented vintage-driven divergences).

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | Faithful to the paper: point-in-time SIC industries, Jegadeesh-Titman 30/30 overlapping cohorts with fixed formation weights, DT 5×5 and DGTW 5×5×5 adjustments, plain-iid Fama-MacBeth with correct timing (no look-ahead). Paper-silent choices documented (A1–A18); the one spec error was caught and fixed in iteration 1; no methodology bug found. The iteration-2 leg decomposition reuses the same verified engines with the paper-grounded EW-market benchmark (L246/fn 14). |
| Headline matching | 4/5 | Raw individual (0.0041 vs 0.0043) and industry (0.0040 vs 0.0043) momentum and the industry Fama-MacBeth coefficient (0.0395 vs 0.0366) are all within ~8% with correct sign and shape; the abstract's leg-asymmetry headline now also matches directionally. t-statistics are ~½ the paper's and the portfolio-decomposition claim diverges. |
| Data coverage | 5/5 | Exact period (1963-07..1995-07); aggregate universe 4,468 vs 4,610 stocks/mo (−3.1%, within 5%); CRSP + Compustat + Fama-French sources match the paper. Benchmark counts now stated by measurement layer (exact at the SQL/msenames-join layer; frozen panel 1–73 stocks lower per date). |
| Concrete result matching | 3/5 | 411 Tier 1 / 330 Tier 2 / 73 FAIL of 814 cells (re-tallied by the auditor). Pure Tier-1 rate is 50.5% (50–70% band → 3). REPORT now discloses all three conventions: 50.5% Tier-1 only; 78.6% under the strict 2× bound (auditor-verified: 101 Tier-2 cells exceed 2×) alongside the replication's 80.7% near-zero-excluding variant; 91.0% sign-only. FAILs are concentrated in near-zero control coefficients and industry-conditioned alternatives. |
| Signal strength | 4/5 | Primary momentum magnitudes within ~10% of the paper (ratio 0.93–1.08). The size/BE-ME-adjusted cell is 1.5× off and statistical significance is systematically weaker, so not every headline cell clears 10%. |
| Corollary | 4/5 | Horizon pattern, DGTW-adjusted industry momentum, random-industry placebo, the Fama-MacBeth interaction, and now all three leg-asymmetry claims (loser-driven / long-driven / balanced, auditor-reproduced to six decimals on the industry side) replicate. Residual deviations: DT size/BE-ME absorption ≈ 0 (documented vintage effect) and the (6,6) buy/sell split ordering (Wi−Mid 0.0015 < Mid−Lo 0.0025 vs paper 0.0036 > 0.0007), both well-explained. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table I — industry summary stats | 18/20 industry counts and all 20 cap shares match within ~5%/0.9pp; excess means within 1–14 bp; both multivariate F-tests match (all-equal 0.874 vs 0.825; all-zero abnormal 1.774 vs 1.686). | The 20-industry construction, point-in-time SIC assignment, and value-weighting are correct. |
| Table II — momentum decomposition | Individual (6,6) 0.0041 vs 0.0043; industry 0.0040 vs 0.0043; DGTW individual 0.0007/0.0009 and DGTW industry 0.0024/0.0020 all Tier 1. | Individual and industry momentum exist at the paper's magnitude; DGTW risk adjustment behaves as reported. |
| Table III — IM(L,H) horizon grid | All 30 winner-minus-loser means across horizons track the paper, including the strongest 1-month (0.0122 vs 0.0105) and dissipation/reversal at long horizons. | Industry momentum is real, strongest short-term, and decays like the paper — the horizon shape replicates. |
| Table VI — Fama-MacBeth | Industry momentum subsumes 6-month individual momentum (Panel C (6,1): ret +0.0086 vs ind +0.0395, t=7.0) while 12-month momentum survives (ret +0.0127, t=7.8); zero momentum-cell FAILs. | The paper's central econometric result — industry momentum prices the cross-section beyond individual momentum — reproduces. |
| Abstract corollary — long/short leg asymmetry (new in iteration 2) | Individual (6,6): short leg +0.0040 (t=2.64) vs long +0.0002 (t=0.11) → loser-driven. Industry (6,6): long +0.0023 (t=2.34) vs short +0.0017 (t=1.89) → long-driven. Industry (1,1): +0.0056 vs +0.0066, |Δ|=0.10 pp → balanced. Leg-derived spreads reproduce the frozen 0.004135/2.311 and 0.003972/2.359; industry legs independently re-derived by the auditor to six decimals (results/legs_long_short.md). | All three abstract-level attribution claims (L35; §IV.A L1121; §IV.B L1159) hold in this vintage. |

## Important gaps

- **Central portfolio-decomposition claim does not replicate (documented data limitation, non-actionable).** Industry adjustment does not eliminate individual momentum here (industry-neutral spread 0.0039 vs 0.0011; two industry-conditioned strategies sign-flip). The 2026 CRSP vintage genuinely contains ~3.5× stronger within-industry momentum; the engine was verified bit-exact and five construction mechanisms were ruled out.
- **Systematic variance/t-stat gap (data limitation, non-actionable).** Monthly long-short spread volatility is ~2× the paper's, so t-statistics are ~half (2.31 vs 4.65) across every strategy type; inferences on marginal cells are weaker.
- **Size/BE-ME absorption ≈ 0 (data limitation, non-actionable).** The Daniel-Titman adjustment absorbs none of the momentum spread (vs the paper's −14 bp), though the benchmark sorts are healthy. Same vintage family as above.
- **Buy/sell split ordering at (6,6) (magnitude-level, disclosed).** The market-relative legs support the paper's long-driven claim, but the within-spread split is reversed in this vintage (Wi−Mid 0.0015 < Mid−Lo 0.0025 vs paper 0.0036 > 0.0007; both same-sign, Tier 2). Reported honestly as a vintage finding.
- **Presentation notes (closed/informational).** Pass rates are now stated under all three conventions (50.5% / 78.6% strict 2×-bounded, auditor-verified / 80.7% variant / 91.0% sign-only); the universe-count wording names the measurement layer; the duplicate A18 assumption was merged. Remaining informational items (audit 2 [n1]–[n3]): the 80.7% label is marginally loose for 17 near-zero cells; pre-existing cwd-quirk directories persist inside the slug; cells_legs.json Tier-2 labels follow the sign-only convention.
