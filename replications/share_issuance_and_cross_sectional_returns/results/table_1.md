# Table I — Descriptive Statistics, 1970–2003 (Pontiff & Woodgate 2008)

**Universe:** `univ_all` (all CRSP, nonmissing return at t, ≥6 months listed; assumptions A14).  **Base sample** = `univ_all` AND `issue_contemp` nonmissing = **2,324,025** firm-months (paper 2,312,597).

Each variable is shown over its own nonmissing observations within the base sample. `DT-ISSUE` is dummy-filled to 0 where the 5-year history is missing; `BM` includes the `bm_dum=0` zeros (paper dummy conventions).

## Headline convention — WINSORIZED regressors (confirmed)

**Diagnostic (iteration-2 hypothesis): the paper's Table I standard deviations were computed on 1%/99% per-month winsorized regressors.** This is CONFIRMED: winsorization reproduces the paper's stds almost exactly while raw stds are far too large (ISSUE 0.230 raw → 0.151 winsorized vs paper 0.15; MOM 0.481 → 0.404 vs 0.41). Means/percentiles are essentially unaffected by winsorization. `R_{-11,0}` is a dependent return (NOT a regressor) and is reported RAW per L132 ("We do not transform the holding period returns").

**Headline choice:** winsorized for ISSUE, DT-ISSUE, BM, ME, MOM; raw for R_{-11,0}. Both conventions are shown below.

## Panel A — Simple statistics (headline = bold column)

| Variable | Conv. | N | Mean | P25 | Median | P75 | Std | Paper (mean/p25/med/p75/std) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **ISSUE** | **WINSOR (used)** | 2,324,025 | **0.04** | **0.00** | **0.00** | **0.03** | **0.15** | 0.04 / 0.00 / 0.00 / 0.03 / 0.15 |
| ISSUE | raw (alt) | 2,324,025 | 0.04 | 0.00 | 0.00 | 0.03 | 0.23 | — |
| **DT-ISSUE** | **WINSOR (used)** | 2,324,025 | **0.13** | **0.00** | **0.00** | **0.14** | **0.35** | 0.12 / 0.00 / 0.00 / 0.14 / 0.33 |
| DT-ISSUE | raw (alt) | 2,324,025 | 0.13 | 0.00 | 0.00 | 0.14 | 0.44 | — |
| **BM** | **WINSOR (used)** | 2,324,025 | **-0.31** | **-0.78** | **-0.12** | **0.07** | **0.91** | -0.34 / -0.79 / -0.07 / 0.00 / 0.94 |
| BM | raw (alt) | 2,324,025 | -0.30 | -0.78 | -0.12 | 0.07 | 1.00 | — |
| **ME** | **WINSOR (used)** | 2,324,025 | **11.08** | **9.58** | **10.96** | **12.46** | **2.06** | 11.11 / 9.63 / 10.97 / 12.46 / 2.02 |
| ME | raw (alt) | 2,324,025 | 11.08 | 9.58 | 10.96 | 12.46 | 2.09 | — |
| **MOM** | **WINSOR (used)** | 2,303,543 | **0.06** | **-0.16** | **0.02** | **0.22** | **0.40** | 0.06 / -0.16 / 0.02 / 0.22 / 0.41 |
| MOM | raw (alt) | 2,303,543 | 0.07 | -0.16 | 0.02 | 0.22 | 0.48 | — |
| **R_{-11,0}** | **RAW (used)** | 2,270,492 | **0.15** | **-0.22** | **0.05** | **0.35** | **0.89** | 0.14 / -0.23 / 0.05 / 0.34 / 0.88 |

## Issuance-sign proportions (over base sample; paper 56.6 / 24.2 / 19.2)

| Share | Ours (%) | Paper (%) |
|---|---:|---:|
| ISSUE > 0  | 56.5 | 56.6 |
| ISSUE = 0  | 24.5 | 24.2 |
| ISSUE < 0  | 19.0 | 19.2 |

(n = 2,324,025)

## Observation counts

| Count | Ours | Paper |
|---|---:|---:|
| Base (ISSUE available) | 2,324,025 | 2,312,597 |
| MOM nonmissing | 2,303,543 | 2,285,189 |
| R_{-11,0} nonmissing | 2,270,492 | (≤ 2,312,597) |

---

## Appendix — per-cell evaluation (Tier 1 / Tier 2 / FAIL / SKIP)

**Tally:** Tier 1 = 32 · Tier 2 = 3 · FAIL = 0 · SKIP = 0

Rules: Tier 1 if |ours−paper|/|paper| ≤ tol (zero paper cell → Tier 1 iff our value rounds to 0.00); Tier 2 if sign matches (magnitude outside tol); FAIL if sign flips; SKIP if either side missing.

| Metric | Paper | Ours | Tol% | Rel.dev | Status |
|---|---:|---:|---:|---:|---|
| issue_mean | 0.04 | 0.04 | 10 | 9.2% | Tier 1 |
| issue_p25 | 0.00 | 0.00 | 100 | 0.0% | Tier 1 |
| issue_median | 0.00 | 0.00 | 100 | 0.2% | Tier 1 |
| issue_p75 | 0.03 | 0.03 | 20 | 11.3% | Tier 1 |
| issue_std | 0.15 | 0.15 | 10 | 0.8% | Tier 1 |
| dt_issue_mean | 0.12 | 0.13 | 10 | 8.0% | Tier 1 |
| dt_issue_p25 | 0.00 | 0.00 | 100 | 0.0% | Tier 1 |
| dt_issue_median | 0.00 | 0.00 | 100 | 0.0% | Tier 1 |
| dt_issue_p75 | 0.14 | 0.14 | 20 | 0.5% | Tier 1 |
| dt_issue_std | 0.33 | 0.35 | 10 | 6.2% | Tier 1 |
| bm_mean | -0.34 | -0.31 | 10 | 9.0% | Tier 1 |
| bm_p25 | -0.79 | -0.78 | 20 | 0.8% | Tier 1 |
| bm_median | -0.07 | -0.12 | 20 | 69.6% | Tier 2 |
| bm_p75 | 0.00 | 0.07 | 100 | 7.0% | Tier 2 |
| bm_std | 0.94 | 0.91 | 10 | 2.9% | Tier 1 |
| me_mean | 11.11 | 11.08 | 5 | 0.2% | Tier 1 |
| me_p25 | 9.63 | 9.58 | 5 | 0.5% | Tier 1 |
| me_median | 10.97 | 10.96 | 5 | 0.1% | Tier 1 |
| me_p75 | 12.46 | 12.46 | 5 | 0.0% | Tier 1 |
| me_std | 2.02 | 2.06 | 10 | 1.8% | Tier 1 |
| mom_mean | 0.06 | 0.06 | 10 | 6.0% | Tier 1 |
| mom_p25 | -0.16 | -0.16 | 20 | 0.2% | Tier 1 |
| mom_median | 0.02 | 0.02 | 20 | 22.7% | Tier 2 |
| mom_p75 | 0.22 | 0.22 | 20 | 1.8% | Tier 1 |
| mom_std | 0.41 | 0.40 | 10 | 1.6% | Tier 1 |
| r_11_0_mean | 0.14 | 0.15 | 10 | 6.2% | Tier 1 |
| r_11_0_p25 | -0.23 | -0.22 | 20 | 3.4% | Tier 1 |
| r_11_0_median | 0.05 | 0.05 | 20 | 7.3% | Tier 1 |
| r_11_0_p75 | 0.34 | 0.35 | 20 | 1.8% | Tier 1 |
| r_11_0_std | 0.88 | 0.89 | 10 | 1.0% | Tier 1 |
| pct_positive_issuance | 56.60 | 56.51 | 10 | 0.2% | Tier 1 |
| pct_zero_issuance | 24.20 | 24.47 | 10 | 1.1% | Tier 1 |
| pct_negative_issuance | 19.20 | 19.02 | 10 | 0.9% | Tier 1 |
| n_obs_mom | 2285189.00 | 2303543.00 | 5 | 0.8% | Tier 1 |
| n_obs_issue | 2312597.00 | 2324025.00 | 5 | 0.5% | Tier 1 |

