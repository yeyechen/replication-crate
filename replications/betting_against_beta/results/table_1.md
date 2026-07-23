# Table 1 — Summary Statistics: US Equities

**Source:** Frazzini & Pedersen (2014), Table 1 (US row only).
**Data:** CRSP daily stock files (shrcd 10/11), 1926–2012.

## Validation

| Metric | Ours | Paper | Diff | Status |
|--------|------|-------|------|--------|
| Total stocks | 23,407 | 23,538 | -0.6% | ✅ PASS (5% tol) |
| Mean stocks/year | 3,073 | 3,182 | -3.4% | ✅ PASS (5% tol) |
| Mean ME (firm, $B) | 0.996 | 0.99 | +0.6% | ✅ PASS (10% tol) |
| Start year | 1926 | 1926 | 0% | ✅ PASS |
| End year | 2012 | 2012 | 0% | ✅ PASS |

**All 5 committed Table 1 metrics pass.**

## Notes

- Total stocks (23,407 vs 23,538): 0.6% difference likely due to data vintage
  (crsp_202601 vs the paper's CRSP extract) and the exchcd filter
  (paper cites shrcd only; we also filter exchcd 1/2/3).
- Mean ME computed from month-end abs(prc) × shrout × 1000 / 1e9 ($B),
  averaged across June observations as the paper describes ("as of June of
  each year"). The June mean firm ME is 0.996 $B, matching the paper's 0.99 $B.
- International rows not replicated (requires Xpressfeed Global data).

---
_Computed from data/panel.parquet (3,180,822 rows, 23,407 unique permnos)._
