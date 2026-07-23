# Table V — Out-of-Sample Descriptive Statistics, Sep 1932 – Dec 1969
## (Pontiff & Woodgate 2008)

**Universe:** `univ_all` (A14).  **Base sample** = `univ_all` AND `issue_contemp` nonmissing within the OOS window = **492,793** firm-months. Conventions are identical to Table I: regressors (ISSUE, DT-ISSUE, ME, MOM) are **1%/99% per-month winsorized** (headline); `R_{-11,0}` is a dependent return and is reported **RAW** ("we do not transform the holding period returns", L132). `DT-ISSUE` is dummy-filled to 0 where the 5-year history is missing (paper dummy convention).

> 🚫 **BM is SKIP (A8).** The paper's pre-1970 book equity comes from the Davis-Fama-French (2000) file the authors obtained from Kenneth French (L2445), NOT Compustat (Compustat coverage is "limited or nonexistent" pre-1970 — the very reason they used DFF). No DFF-style book-equity table exists in ClickHouse, so the BM row is reported as SKIP with the reason, not computed from Compustat.

## Panel A — Simple statistics (headline = bold column)

| Variable | Conv. | N | Mean | P25 | Median | P75 | Std | Paper (mean/p25/med/p75/std) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **ISSUE** | **WINSOR (used)** | 492,793 | **0.01** | **0.00** | **0.00** | **0.00** | **0.06** | 0.01 / 0.00 / 0.00 / 0.00 / 0.07 |
| ISSUE | raw (alt) | 492,793 | 0.02 | 0.00 | 0.00 | 0.00 | 0.12 | — |
| **DT-ISSUE** | **WINSOR (used)** | 492,793 | **0.07** | **0.00** | **0.00** | **0.04** | **0.20** | 0.08 / 0.00 / 0.00 / 0.05 / 0.24 |
| DT-ISSUE | raw (alt) | 492,793 | 0.07 | 0.00 | 0.00 | 0.04 | 0.26 | — |
| **BM** | **SKIP** | — | — | — | — | — | — | SKIP — DFF book equity unavailable (A8) |
| **ME** | **WINSOR (used)** | 492,793 | **10.34** | **9.14** | **10.27** | **11.52** | **1.75** | 10.28 / 9.05 / 10.22 / 11.50 / 1.80 |
| ME | raw (alt) | 492,793 | 10.34 | 9.14 | 10.27 | 11.52 | 1.78 | — |
| **MOM** | **WINSOR (used)** | 489,607 | **0.10** | **-0.07** | **0.06** | **0.21** | **0.33** | 0.09 / -0.09 / 0.05 / 0.20 / 0.34 |
| MOM | raw (alt) | 489,607 | 0.10 | -0.07 | 0.06 | 0.21 | 0.36 | — |
| **R_{-11,0}** | **RAW (used)** | 484,827 | **0.21** | **-0.08** | **0.12** | **0.36** | **0.60** | 0.19 / -0.10 / 0.11 / 0.35 / 0.60 |

## Issuance-sign proportions (over base sample; paper 28.2 / 62.6 / 9.2)

| Share | Ours (%) | Paper (%) |
|---|---:|---:|
| ISSUE > 0  | 30.2 | 28.2 |
| ISSUE = 0  | 59.7 | 62.6 |
| ISSUE < 0  | 10.0 | 9.2 |

(n = 492,793)

## Observation counts

| Count | Ours | Paper |
|---|---:|---:|
| Base (ISSUE available) | 492,793 | (≈524–528K range) |
| MOM nonmissing | 489,607 | 524,260 |
| R_{-11,0} nonmissing | 484,827 | 528,200 |

> ⚠️ **OOS universe count runs ~7% below the paper** (known, documented in `panel_report.md` note 10): our `univ_all` counts from the first month with a nonmissing return and applies the ≥6-month listing rule, which the paper's OOS cross-section exceeds. Also our `R_{-11,0}` requires ALL 12 actual months (no EWRETD imputation, `panel_report.md` note 11), so it sits BELOW MOM here, whereas the paper's R_{-11,0} (528,200) exceeds its MOM (524,260) — implying the paper EWRETD-imputes R_{-11,0}. Both are documented spec decisions, not forced.

---

## Appendix — per-cell evaluation vs tables_to_replicate.json (T5)

**Tally:** Tier 1 = 15 · Tier 2 = 5 · FAIL = 0 · SKIP = 2

BM cells (oos_bm_mean, oos_bm_std) are SKIP (A8: DFF book equity unavailable).

| Metric | Paper | Ours | Tol% | Rel.dev | Status |
|---|---:|---:|---:|---:|---|
| oos_issue_mean | 0.01 | 0.01 | 20 | 48.0% | Tier 2 |
| oos_issue_p75 | 0.00 | 0.00 | 100 | 0.1% | Tier 1 |
| oos_issue_std | 0.07 | 0.06 | 15 | 11.9% | Tier 1 |
| oos_dt_issue_mean | 0.08 | 0.07 | 15 | 13.7% | Tier 1 |
| oos_dt_issue_p75 | 0.05 | 0.04 | 20 | 10.3% | Tier 1 |
| oos_dt_issue_std | 0.24 | 0.20 | 15 | 17.3% | Tier 2 |
| oos_bm_mean | -0.12 | — | 20 | — | SKIP |
| oos_bm_std | 0.94 | — | 10 | — | SKIP |
| oos_me_mean | 10.28 | 10.34 | 5 | 0.6% | Tier 1 |
| oos_me_p25 | 9.05 | 9.14 | 5 | 1.0% | Tier 1 |
| oos_me_median | 10.22 | 10.27 | 5 | 0.5% | Tier 1 |
| oos_me_p75 | 11.50 | 11.52 | 5 | 0.1% | Tier 1 |
| oos_me_std | 1.80 | 1.75 | 10 | 2.9% | Tier 1 |
| oos_mom_mean | 0.09 | 0.10 | 15 | 9.1% | Tier 1 |
| oos_mom_std | 0.34 | 0.33 | 10 | 2.9% | Tier 1 |
| oos_r_11_0_mean | 0.19 | 0.21 | 10 | 11.7% | Tier 2 |
| oos_r_11_0_std | 0.60 | 0.60 | 10 | 0.6% | Tier 1 |
| oos_pct_positive_issuance | 28.20 | 30.25 | 10 | 7.3% | Tier 1 |
| oos_pct_zero_issuance | 62.60 | 59.70 | 10 | 4.6% | Tier 1 |
| oos_pct_negative_issuance | 9.20 | 10.05 | 10 | 9.2% | Tier 1 |
| oos_n_obs_mom | 524260.00 | 489607.00 | 5 | 6.6% | Tier 2 |
| oos_n_obs_r_11_0 | 528200.00 | 484827.00 | 5 | 8.2% | Tier 2 |

