---
schema_version: 2
slug: returns_to_buying_winners
iteration: 2
audit_verdict: PARTIAL
verdict: REPLICATED
overall: 4.17
methodology: 4
headline_matching: 4
data_coverage: 4
concrete_result: 4
signal_strength: 5
corollary: 4
generated_at: 2026-07-22T20:55:00+00:00
---

# Replication Summary

## Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 4.17 / 5.00
**Audit state:** `PARTIAL`

Jegadeesh & Titman's (1993) central claim — that buying past winners
and selling past losers earns significant positive returns over
1965–1989 — replicates: the 6/6 strategy earns 0.88%/month
(t 2.91) against the paper's 0.95% (t 3.07), −7.4%, with the sell and
buy legs each within 3% of the paper and all 32 strategies positive.
The strongest evidence is the auditor's independent recomputation of
the headline series, the Tables V/VI/VII/VIII results, and all four
§III decomposition statistics from the cached panel to essentially
exact agreement, plus a bit-identical pipeline re-run. A binary
`REPLICATED` verdict does not mean every one of the 1,327 cells
matched: 84.9% are Tier 1 and the 70 fails are all cells the paper
itself prints as statistically nil.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | The iteration-2 timing correction (A13: rank formation f on the 6-month signal ending at f, hold from f+1 — the paper's [t−6, t−1]/[t, t+K−1] with no skipped month) is verified correct by independent recomputation and a Jan-1980-cohort hand check; every convention (delisting-unadjusted primary, EW deciles, K-cohort overlap, iid/NW inference) is documented with paper citations. The only unverifiable element is the paper's overlapping-series F-stat construction (7 secondary cells; three variants reported). |
| Headline matching | 4/5 | Sign, shape, significance, and magnitude class replicate across all 32 strategies, the January effect, the event-time inverted-U (C₁₂ +7.3%), and 4-of-5 subperiods; the central cell is within 7.4%. The noisy C₃₆ endpoint (+71%, paper t 0.67) and the crash-era Panel A magnitude keep this at 4. |
| Data coverage | 4/5 | Exact 1965–1989 reporting window plus a verified 1926–1964 extension for the back-test; CRSP daily, dsi indexes, Compustat fundq, CCM link, and FF factors as in the paper, with one documented substitution (2026 vs 1990 data vintages) whose effects are quantified. |
| Concrete result matching | 4/5 | 1,127/1,327 cells Tier 1 (84.9%), 94.7% Tier 1+2 under the stated tolerances; every fail is a statistically nil cell in the paper (|t| ≤ 1.13 or |value| ≤ 0.3%/mo). Tallies independently reproduced from the contract. |
| Signal strength | 5/5 | The paper's headline numbers (0.95%/month, t 3.07, 12.01%/yr) map to ours at ratios 0.93, 0.95, and 0.92 — all within 10%. |
| Corollary | 4/5 | All four previously-missing corollaries now computed and checked: the 1927–1964 back-test (Panel B C₁₂ +6.6% of the paper; Panel A sign/shape with vintage-scaled magnitude), earnings-announcement returns (the abstract pattern: winners > losers in months 1–7, losers > winners in 11 of months 8–20), the §III decomposition (all three causal verdicts, one statistic exact to 4 dp, WRSS correlation +1.3%), and Tables V/VI win rates and subperiods. Deviations are documented vintage effects. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table I (32 strategies) | 192/192 cells Tier 1; 6/6 buy-sell 0.88% vs 0.95%/mo (t 2.91 vs 3.07), sell/buy legs within ±3% (auditor-recomputed exactly) | Universe, daily→monthly compounding, the corrected formation/holding timing, EW decile sorts, overlapping K-month holding |
| Tables II–IV | Post-ranking betas within ±4% (P10−P1 −0.07 vs −0.08); size/SW-beta subsample spreads all positive and significant; January −5.5% vs −6.86%, Feb–Dec +1.7% vs +1.66% | Risk characterization, subsample construction, calendar-month alignment and the January effect |
| Tables V–VI | Positive-month proportions 0.96 (Apr, exact), 0.71 (Feb–Dec), 0.67 (All); 5-year subperiod means and t-stats match (Jan 1970–74 −11.3% vs −10.7%, t −2.47 vs −2.54) | Distributional stability and subperiod stability of the profits |
| Table VII (event time) | C₁₂ 10.21% vs 9.51% (+7.3%); inverted-U shape (positive 2–12, negative 13–24, flat 25–36) | The post-formation return path and its year-2/3 partial reversal |
| Table VIII (back-test) | Panel B C₁₂ 0.0621 vs 0.0583 (+6.6%), dissipating by month 24 as claimed; Panel A month-1 −5.0% vs −4.95%, C₃₆ −34.2% vs −40.8% (sign/shape, vintage-scaled magnitude) | Out-of-sample validity on a second data era |
| Table IX (earnings) | Months 1–7 mean +0.72%/announcement (7/7 positive, significant), months 11–18 mean −0.48%; sign pattern 31/36 months | The abstract-level earnings-announcement reversal (Compustat data path) |
| §III decomposition | Residual serial covariance +0.001199 vs +0.0012 (exact); corr(WRSS, 6/6) 0.963 vs 0.95; EW serial covariance negative; θ −1.98 vs −2.29 — all three causal verdicts reproduce | The paper's central causal claim: profits from idiosyncratic underreaction, not risk, factor timing, or lead-lag |

## Important gaps

- **Data vintages are 2026, not the paper's 1990** (CRSP and Compustat): the 1990 files are unavailable, so vintage-driven deviations — crash-era Panel A magnitudes (~¾ of the paper), Table IX t-statistics (√n-inflated by richer coverage), NW t-stats systematically larger than the paper's — cannot be falsified and are documented as earned partials.
- **Market-cap levels (Table II) run uniformly 9–26% below the paper's** with shape preserved — a CRSP share-count revision across vintages, not a construction error; units validated against dsi.totval.
- **The paper's Panel A F-stat construction on overlapping monthly series is unidentified** (ours 0.4–1.0 vs 1.7–4.5; three variants reported); the decile means the tests are about do replicate.
- **Actionable cleanup (no recomputation needed):** REPORT.md prose carries four stale pre-A13 numbers and one arithmetic slip while the underlying artifacts are correct (audit-2 m1), and the per-cell classification harness is not committed to the repo (m2/m3).
