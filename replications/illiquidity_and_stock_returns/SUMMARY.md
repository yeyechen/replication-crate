---
schema_version: 2
slug: illiquidity_and_stock_returns
iteration: 2
audit_verdict: PASS
verdict: REPLICATED
overall: 3.83
methodology: 4
headline_matching: 4
data_coverage: 4
concrete_result: 3
signal_strength: 4
corollary: 4
generated_at: 2026-07-22T18:30:00
---

# Replication Summary

## Amihud (2002), "Illiquidity and stock returns: cross-section and time-series effects"

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 3.83 / 5.00
**Audit state:** `PASS`

The paper's central claims replicate within tolerance: illiquidity is priced in the cross-section (k_ILLIQMA = 0.166, t 6.56, vs 0.162, t 6.55; positive in 63.2% of months vs 63.4%), expected market illiquidity raises ex ante excess return (annual g1 14.17 vs 10.23, t 3.17; monthly 0.845 vs 0.712, positive in all six subperiods), and unexpected illiquidity lowers contemporaneous returns (annual g2 −24.24 vs −23.57; monthly −4.18 vs −5.52, negative in all six subperiods with mean −7.48 vs the paper's −7.09), with the size gradient SZ2 strictly monotone in both tables. Every headline number was independently recomputed by the auditor from the cached artifacts — twice (audit 1 and again, on the relocated parquets, in audit 2) — and matches to the printed digit. Audit 2 verified all three audit-1 fixes: dual tier tallies (repo rule 199/86/10; rubric-strict 199/52/44, recomputed exactly from the per-cell tables), the §3.3 six-subperiod corollary with Chow stability tests, and a validator-clean data layout. A binary `REPLICATED` does not mean every cell matched: 199 of 295 cells are Tier 1 (67.5%) under either convention, Table 5 was out of scope for data reasons, and a few secondary patterns (strict SZ1 monotonicity, dividend-yield magnitudes, Table 4 intercepts, subperiod g1 mean) are documented partials.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | Construction traces to the paper line-by-line (universe, admission, ILLIQ/ILLIQMA, Shumway delisting, Scholes–Williams betas, AR(1)+Kendall, FM iid t / White / NW); two documented deviations (annual Rf substitute — now with an on-record sensitivity showing slopes are nearly invariant; NW maxlags=0 chosen by lag sweep to reproduce the paper's bracketed t) and two paper-silent universe choices resolved by diagnose-then-fix with a pre-registered adoption rule. No methodology bugs on independent recompute. |
| Headline matching | 4/5 | Sign, significance and shape match on every headline claim; magnitudes within ~20% except annual g1(market) +38.5% (t-stat within 18%) and monthly g2(market) −24%. k_ILLIQMA and annual g2 match to ≤3%; monthly R² 0.143 vs 0.144. |
| Data coverage | 4/5 | Exact 1963–1996/1964–1997 period; CRSP + Fama–French sources match with one documented Rf substitute. Admitted counts 1,047–1,771 sit inside the paper's 1,061–2,291 range in 33/34 years but never approach the 1990s upper bound (documented CRSP-vintage drift; filter verified not-too-tight). |
| Concrete result matching | 3/5 | 199/295 cells Tier 1 (67.5%) under both conventions — repo rule: 86 Tier 2 / 10 FAIL; rubric-strict 2× bound: 52 Tier 2 / 44 FAIL (both tallies now reported per table and auditor-recomputed exactly). The 34 reclassified cells are statistically vacuous in the paper (paper \|t\| ≤ 1) or documented A13/A15/A16 vintage/paper-side gaps — no unexplained discrepancies; every headline cell is Tier 1. |
| Signal strength | 4/5 | Flagship coefficient ratios vs paper: k 1.02, g2-annual 1.03, g1-monthly 1.19, g2-monthly 0.76, g1-annual 1.39; all t-stat ratios within [0.82, 1.18]. Two coefficients break the ±20% band (worst-cell reading would be 3; combined reading scored 4 with the caveat on record). |
| Corollary | 4/5 | Most corollaries replicate with minor, well-explained deviations: the §3.3 six-subperiod check now computed — g1 positive 6/6 and g2 negative 6/6 as in the paper, g2 mean −7.48 vs −7.09 (−5.5%) / median −6.45 vs −5.98 (−7.8%) against the paper's sharper subperiod benchmark; both Chow tests fail to reject AR(1) stability (p = 0.917 annual, p = 0.110 monthly), consistent with the paper; Table 2 window stability, strict SZ2 in both tables, and the AR(1)+Kendall dynamics all replicate. Remaining deviations: SZ1 is directional only (3/4 and 2/4 adjacent pairs), size-portfolio JANDUM/R² magnitudes are inflated, and the subperiod g1 mean is +66% above the paper (reported, not chased — adoption rule locked). |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 1 — summary statistics | ILLIQ mean 0.347 vs 0.337, SIZE/SDRET stats within 5%; 15/24 cells Tier 1 (DIVYLD row −18% is documented CRSP-vintage composition) | Universe, admission criteria, and variable construction are correct |
| Table 2 — Fama–MacBeth cross-sections | k_ILLIQMA 0.166 (t 6.56) vs 0.162 (6.55); all 16 ILLIQMA coef/t cells Tier 1 across all four windows; 63.2% positive vs 63.4% | Illiquidity is priced in the cross-section; lag structure, delisting adjustment, and FM machinery are sound |
| Table 3 — annual time series | H-1 (g1 > 0) and H-2 (g2 < 0, \|t\| ≥ 4) hold in all six columns; g2(market) −24.24 vs −23.57; AR(1) slope 0.715 vs 0.768; SZ2 strictly monotone; Rf-sensitivity slopes invariant | Expected illiquidity raises ex ante return; unexpected illiquidity lowers prices; the open-NYSE AILLIQ aggregate reproduces the paper's dynamics |
| Table 4 — monthly time series | g1 Tier 1 in all six columns (market 0.845 vs 0.712); all 18 g2 cells Tier 1 (market −4.18 vs −5.52); R² 0.143 vs 0.144; JANDUM(market) 4.98 vs 5.28 | The annual findings hold at monthly frequency under the open-universe MILLIQ; intercepts are documented paper-side anomalies |
| §3.3 six-subperiod robustness | g1 positive 6/6, g2 negative 6/6 (paper 6/6); g2 mean −7.482 vs −7.089 (−5.5%); Chow AR(1) stability not rejected (p = 0.917 / 0.110), consistent with the paper | The time-series effects are stable across the sample, as the paper claims |

## Important gaps

- **Table 5 not replicated** — its BAA/AAA/long-Treasury yield series (source: Basic Economics) do not exist anywhere in the ClickHouse catalog; the "illiquidity survives bond-yield controls" result is unverified here (non-actionable data limitation).
- **Dividend yield −18% and Table 4 intercepts** — CRSP-vintage composition for DIVYLD (two candidate fixes tested and rejected); the monthly AR intercept and the g0 cluster are paper-side reporting inconsistencies (the paper's printed intercept 0.313 with slope 0.945 implies a series level, e^5.7, contradicting its own Table 1), with the replication's internally consistent values retained.
- **Secondary magnitudes** — SZ1 strict monotonicity holds directionally only; size-portfolio JANDUM/R² and the subperiod g1 mean (+66%) run above the paper's, consistent with our CRSP-vintage small deciles being more illiquidity-sensitive; signs, significance and the g2 side replicate.
