# Consolidated Per-Cell Evaluation Summary (strict audit convention)

Asset Growth and the Cross-Section of Stock Returns (Cooper, Gulen, Schill 2008) — Tables I–IV.
Source: `results/table_{1..4}_eval.json` (read-only; relabeled in outer iteration 2 per audit1.md §2 M2 + m1). **No result value changed in the relabeling — only tier-classification metadata was added** (see §6).

**Convention (strict, audit1.md §2 M2):** every cell is regraded from the unchanged ours/paper values as
- **Tier 1** — within the cell's stated tolerance (unchanged);
- **Tier 2** — not Tier 1, correct sign, and either within the auditor's 2× magnitude bound (0.5 ≤ |ours/paper| ≤ 2.0, |paper| ≥ 0.05) → *pattern*; or a documented subtype: *near-zero-target* (|paper| < 0.05, ratio unreliable), *near-zero-spread* (a t-stat whose underlying spread is ≈0 and itself matches the paper), *units* (unit-dependent coefficient, within 2× in the paper's units with a Tier-1 t-stat);
- **FAIL** — opposite sign, or sign-matching ratio outside [0.5, 2.0] with |paper| ≥ 0.05 — each tagged exactly one documented cause;
- **SKIP** — not computed (none).

Each Tier-2/FAIL cell carries `within_2x`, a `subtype` (Tier 2) or `cause` (FAIL and special Tier-2 subtypes), and `near_zero_target: true` where |paper| < 0.05 (with `within_2x = null`, since division by ~0 makes the ratio unreliable). The original tolerance-based grade is retained per cell as `tier_tolerance`. For opposite-sign FAILs `within_2x` is false (the magnitude check is moot once the sign flips).

## 1. Overall tally (strict convention)

| Grade | Count |
|---|---:|
| Tier 1 | 76 |
| Tier 2 — pattern (within 2×) | 28 |
| Tier 2 — near-zero-target | 3 |
| Tier 2 — near-zero-spread | 1 |
| Tier 2 — units | 1 |
| **Tier 2 total** | **33** |
| FAIL — noise-level null (sign flip on a statistically zero coefficient/spread) | 3 |
| FAIL — data coverage (pre-1971 Compustat missingness, auditor-verified) | 5 |
| FAIL — vintage attenuation / dormant-shell dilution (Assumption 7) | 2 |
| **FAIL total** | **10** |
| SKIP | 0 |
| **Total cells** | **119** |

Sign/pattern-correct (Tier 1 + Tier 2) = **109 of 119** (91.6%); every FAIL is a documented non-actionable cause (§4), and 117 of 119 cells (98.3%) have the correct sign.

## 2. Per-table tally (strict convention)

| Table | Tier 1 | Tier 2 | (pattern / near-zero-target / near-zero-spread / units) | FAIL | (noise / data / vintage) | SKIP | Total |
|---|---:|---:|---|---:|---|---:|---:|
| Table I | 19 | 29 | 25 / 3 / 1 / 0 | 5 | 2 / 1 / 2 | 0 | 53 |
| Table II | 33 | 3 | 3 / 0 / 0 / 0 | 0 | 0 / 0 / 0 | 0 | 36 |
| Table III | 22 | 1 | 0 / 0 / 0 / 1 | 3 | 1 / 2 / 0 | 0 | 26 |
| Table IV | 2 | 0 | 0 / 0 / 0 / 0 | 2 | 0 / 2 / 0 | 0 | 4 |
| **All** | **76** | **33** | **28 / 3 / 1 / 1** | **10** | **3 / 5 / 2** | **0** | **119** |

_Cross-check: this recount matches the `strict_tally` block now stored in every eval JSON exactly (no discrepancies). Tolerance-convention tallies (`tally` blocks): Table I 19/32/2/0, Table II 33/3/0/0, Table III 22/3/1/0, Table IV 2/2/0/0 → 76/40/3/0 overall. One discrepancy vs the previously stored Table I tally (19/33/1/0): the m1 relabel of `Leverage_spread_10_1` (Tier 2 → FAIL) moved one cell; the stored tally was updated accordingly and the prior value is noted in the JSON's `tally_note`. Tables II–IV tolerance tallies are unchanged._

## 3. Tier-2 subtypes (detail)

- **Pattern (28):** sign correct and 0.5 ≤ |ours/paper| ≤ 2.0. Table I (25): ASSETG_D1 (0.86×), ASSETG_D5 (0.78×), ASSETG_D10 (1.37×), ASSETG_spread_10_1 (1.26×), ASSETG_t_spread (0.51×), L2ASSETG_D10 (1.47×), L2ASSETG_spread_10_1 (1.33×), ASSETS_D1 (1.41×), ASSETS_D10 (0.81×), ASSETS_spread_10_1 (0.54×), MV_D1 (1.33×), MV_AVG_D1 (1.31×), MV_AVG_spread_10_1 (0.67×), BM_D1 (1.10×), BM_spread_10_1 (1.23×), EP_D1 (0.66×), EP_spread_10_1 (0.70×), Leverage_D10 (0.83×), ROA_D10 (0.53×), ROA_spread_10_1 (0.52×), BHRET36_D10 (1.24×), ACCRUALS_spread_10_1 (1.51×), ACCRUALS_t_spread (0.66×), **ISSUANCE_D10 (1.30×)** and **ISSUANCE_spread_10_1 (1.45×)** — the latter two were 3.4×/3.9× pre-M1; with the split-adjusted share definition (M1) they are legitimate within-2× pattern matches. Table II (3): PanelA_ASSETG_year1_spread (1.26×), PanelA_ASSETG_year1_t (0.51×), VW_spread_Sharpe_annual (0.66×).
- **Near-zero-target (3):** |paper| < 0.05, ratio unreliable (division by ~0); sign matches, absolute difference modest. Table I: L2ASSETG_D1 (paper 0.0041; ours 0.0352), ROA_D1 (paper −0.0186; ours −0.0077), BHRET6_D10 (paper 0.0074; ours 0.0146).
- **Near-zero-spread (1):** Table I BHRET6_t_spread (t −3.68 vs paper −0.33, 11.2×) — the underlying BHRET6 spread is ≈0 (paper −0.0786) and matches ours (−0.0708, ~10% off, Tier 1); the t-stat differs only from cross-year variance on a tiny effect.
- **Units (1):** Table III M1_MV — the FM slope on MV is unit-dependent: ours is raw-$millions (−3.644e-06) vs the paper's $billions (−0.0044); in $B the coefficient is −0.003644 = 0.83× the paper (within 2×) and the scale-invariant t matches (−1.39 vs −1.57, Tier 1). A scaling note, not an economics gap.

## 4. Every FAIL cell, grouped by documented cause

### Noise-level null — sign flip on a statistically zero coefficient/spread (3)

| Table | Metric | Paper | Ours | Note |
|---|---|---:|---:|---|
| Table I | Leverage_spread_10_1 | +0.0165 | −0.0158 | sign flip on a ~0 spread; both \|spread\| < 0.02 (relabel [m1]; previously "Tier 2 lenient") |
| Table I | Leverage_t_spread | 1.17 | −1.2574 | t of that economically zero spread; \|t\| < 1.3 in both |
| Table III | M3_5YSALESG_t | −0.27 | +0.0777 | 5YSALESG coefficient insignificant in BOTH paper and ours (\|t\| < 0.3) |

### Data coverage — pre-1971 Compustat missingness (auditor-verified ch ~93% / txp ~53–56% null FY1966–68) (5)

| Table | Metric | Paper | Ours | Ratio | Note |
|---|---|---:|---:|---:|---|
| Table I | ACCRUALS_D10 | 0.0341 | 0.1065 | 3.12× | paper target also near-zero (`near_zero_target`); accruals (act−ch) rest on 13/15/19 firms in 1968–1970 |
| Table III | M6_ACCRUALS_ASSETG_t | −5.65 | −2.2268 | 0.39× | M6 includes ACCRUALS; dense-only (1971+) improves but does not close the gap |
| Table III | M6_ACCRUALS_t | −4.00 | −1.0715 | 0.27× | accruals slope attenuated by sparse pre-1971 cross-sections |
| Table IV | dOthAssets_alone_t | −3.34 | −0.3391 | 0.10× | other-assets component poorly measured pre-1971; sign correct |
| Table IV | dCurAsst_full_t | −3.74 | −1.0921 | 0.29× | ΔCurAsst (act−ch) sparse pre-1971; sign correct; ΔPPE (best-measured) replicates |

### Vintage attenuation / dormant-shell dilution (Assumption 7) (2)

| Table | Metric | Paper | Ours | Ratio | Note |
|---|---|---:|---:|---:|---|
| Table I | L2ASSETG_t_spread | 26.26 | 12.4658 | 0.47× | t on the 2-yr-lagged ASSETG spread; the spread itself is a within-2× pattern (1.33×) |
| Table I | ROA_t_spread | 20.64 | 8.7272 | 0.42× | t on the ROA spread; the spread itself is a within-2× pattern (0.52×) |

## 5. SKIP cells

_None._ (All committed cells were computed.)

## 6. Labeling only — no result value changed

This relabeling (outer iteration 2, M2 + m1) added/updated tier-classification metadata only (`tier`, `tier_tolerance`, `ratio_ours_paper`, `within_2x`, `subtype`, `near_zero_target`, `cause`, `cause_detail`, `strict_tally`). **Every `paper`/`ours` value and every `results`/`table`/`computed` block in all four eval JSONs is byte-identical to before the relabeling** (asserted programmatically; spot-checks: ASSETG_D1 −0.18174941506864697; ISSUANCE_D10 0.39212040977569895 (split-adjusted, from M1); M1_MV −3.644245897573218e-06; dCurAsst_full_t −1.092132968587469; EW_Y1_spread −1.7128466242864935 — all unchanged). The only status/reason field edits are the m1-mandated `Leverage_spread_10_1` (Tier 2 → FAIL; prior reason retained as `reason_tolerance`).

The original tolerance-based count (≈76 Tier-1 / 41 Tier-2 / 2 FAIL after M1; i.e. 76/40/3 once m1 is applied) and this strict-audit count (76 / 33 / 10) differ only because the audit imposes a 2× magnitude cap on pattern-matches: 7 sign-matching cells outside [0.5, 2.0] move from Tier 2 to FAIL-with-documented-cause (the five pre-1971 data-coverage cells plus the two vintage-attenuated t-stats), and the sign-flipped ~0 Leverage spread is labeled FAIL instead of "Tier 2 lenient" [m1] — while 4 of the audit's pre-M1 out-of-2× list remain Tier 2 under documented subtypes (near-zero-target: L2ASSETG_D1, ROA_D1; near-zero-spread: BHRET6_t_spread; units: M1_MV) and the two ISSUANCE cells return to Tier-2 pattern once M1's split-adjustment brought them within 2× (1.30×/1.45×). This also reconciles the audit's pre-M1 strict estimate (74/30/15): M1 moved ISSUANCE_D1 and ISSUANCE_t_spread to Tier 1 (+2 Tier 1), and the subtype exceptions above account for the remaining −5 FAIL / +3 Tier-2 difference. The Tier-1 set itself is unchanged by the 2× rule; two Tier-1 cells (M1_BHRET36 0.49×, M1_BHRET36_t 0.48×) are mechanically just outside 2× but sit inside their stated 60% tolerance and remain Tier 1 per convention (flagged `within_2x: false` for transparency).
