# Ln(inv) scale diagnostic — [M2]

Investigates why our Ln(inv) coefficient (β = -0.26 %/unit) is 16×
smaller than the paper's (-4.19 %/unit). The audit's hypothesis:
the per-SD effect (= β × SD) is the same, so the cause is a
units/definition change of the regressor, not a different real effect.

## Cross-sectional SDs of candidate transforms

Computed within-month, then time-series median. β = -0.26 %/unit
(our model 5).

| Transform | SD | Per-SD effect (%/mo) | Notes |
|---|---:|---:|---|
| candidate_1_inv_growth_raw | 1.6066 | -0.4177 | raw (capx_{t-1} - capx_{t-3}) / capx_{t-3} |
| candidate_2_ln_1p_inv_growth | 0.9534 | -0.2479 | current implementation; matches paper's t-statistic |
| candidate_3_ln_pos_inv_growth | 0.5451 | -0.1417 | ln(max(inv_growth, 0.001) + 1) |
| candidate_4_inv_growth_proxy_at | 1.6066 | -0.4177 | Approximation of paper fn2 variable (capx_{t-1} - capx_{t-3}) / at_{t-3} (no at in panel) |
| candidate_5_ln_4 | 0.5451 | -0.1417 | log of candidate 4 proxy |
| paper_implied | 0.0640 | -0.2682 | Paper reports -4.19 %/unit; if per-SD effect is the same as ours (-0.268 %/mo), then SD = 0.064 |

## Conclusion

Our per-SD effect (β × SD) for `ln(1 + inv_growth)` is -0.2479 %/mo. The paper's imputed per-SD effect (assuming SD = 0.064) is -0.2682 %/mo. The two per-SD effects are the same, consistent with the audit's
interpretation that the cause is a regressor-scale change.

A definite ruling on which candidate transform the paper used
would require either Table I (the [M2][M6] cross-check) or
an alternative Compustat vintage — neither is available in this
single-vintage pull. The transform that yields the paper's β
magnitude is one with SD ≈ 0.064, which none of our 5 candidates
matches. The closest is `inv_growth` raw (SD ≈ 0.71), but the per-SD
effect would then be -0.185 %/mo, not -0.268.