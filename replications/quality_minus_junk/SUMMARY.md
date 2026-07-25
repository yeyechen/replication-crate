> **NOTICE (2026-07-25): the binary verdict below is SUPERSEDED.** Corrected investment-first records with accepted/qualified/quarantine statuses live in `training/cases.json`; see `training/README.md`.

---
schema_version: 2
slug: quality_minus_junk
iteration: 1
audit_verdict: PARTIAL
verdict: REPLICATED
overall: 3.17
methodology: 3
headline_matching: 3
data_coverage: 4
concrete_result: 4
signal_strength: 3
corollary: 2
generated_at: 2026-07-22T16:29:28Z
---

# Replication Summary

## Quality minus junk (Asness, Frazzini, Pedersen 2019)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 3.17 / 5.00
**Audit state:** `PARTIAL`

The paper's central claim — that a Quality-minus-Junk (QMJ) factor going long
high-quality stocks and short junk stocks earns significant positive
risk-adjusted returns — replicates for the U.S. Long Sample (June 1957 –
December 2016). The independently recomputed QMJ four-factor alpha is 0.46%/mo
(t ≈ 8.1) versus the paper's 0.60, the quality-sorted deciles rise from junk to
quality with a positive high-minus-low spread, and high-quality stocks carry
lower market betas (H-L beta -0.35 vs -0.36). The strongest evidence is that
every reported number reproduces exactly from the cached panel, and the
Profitability factor matches the paper almost exactly (0.49 vs 0.50). A binary
`REPLICATED` result means the headline finding holds; it does not mean every
reported cell matched — headline magnitudes sit at roughly 77% of the paper and
two documented score simplifications plus a missing robustness table leave clear
gaps.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 3/5 | Universe filter, FF(1992) timing, delisting rule, rank z-scores, composites, QMJ 2×3 sort, and Newey-West convention all match; two documented deviations (plain CAPM beta instead of Frazzini-Pedersen 2014; growth not per-share) weaken the Safety and Growth sub-scores. |
| Headline matching | 3/5 | Sign and shape all correct (QMJ positive/significant, returns rise with quality, quality is safer); magnitudes ~23–29% below the paper on the headline cells. |
| Data coverage | 4/5 | Exact sample period; universe 4,380 stocks/month vs the paper's ~4,585 (within 4.5%); CRSP + Compustat North America + Fama-French all match, with one documented filter substitution (consol='C'). |
| Concrete result matching | 4/5 | 30 of 39 committed cells across Tables 3 and 4 fall within the paper's tolerances (77%); the committed Table 9 spanning test has no results file. |
| Signal strength | 3/5 | Headline cells all within 2× of the paper (QMJ 4F alpha at 77%, H-L return at 72%, QMJ 3F alpha essentially exact), but none inside the ±20% band. |
| Corollary | 2/5 | Factor loadings mostly replicate (negative MKT/SMB/HML), though the UMD loading flips sign; subsample stability and FF5/6-factor robustness were not computed. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 3 — quality deciles | Returns rise P1→P10 (0.38→0.68) with a positive H-L spread (0.30 vs paper 0.42); H-L 4-factor alpha 0.81 vs 1.05; beta spread -0.35 vs -0.36. | The composite quality score is constructed correctly end-to-end and prices returns as the paper claims, though the interior beta gradient is flatter than the paper's. |
| Table 4 — QMJ factor | QMJ 4-factor alpha 0.46 (t≈8.1) vs 0.60; 3-factor alpha 0.52 vs 0.51 (near-exact); negative MKT/SMB/HML loadings confirmed; adj-R² 0.51 vs 0.50. | QMJ is a significant, safer-than-junk factor; the Profitability sub-factor matches the paper almost exactly (0.49 vs 0.50). |

## Important gaps

- **Frazzini-Pedersen (2014) beta not implemented** — a plain 60-month CAPM beta is used, flattening the Table 3 beta gradient and pulling the Safety alpha (0.36 vs 0.51) and QMJ market loading (-0.16 vs -0.20) below the paper. Actionable next iteration.
- **Growth measures not per-share** — weakens the Growth sub-factor (0.28 vs 0.46). Actionable next iteration.
- **Committed Table 9 (spanning) not produced** — the test that QMJ is a distinct factor is missing. Actionable next iteration.
- **Corollary tests not computed** — subsample stability (Fig. 2 / Table 15) and FF5/6-factor robustness (Table 5) were not run.
- **QMJ momentum (UMD) loading flips sign** (+0.07 vs -0.09), so the factor's momentum tilt is not captured.
- **Global Broad Sample (Panel B, 24 countries) is out of scope** for this run — a documented data-complexity limitation, not a defect in the U.S. replication.
