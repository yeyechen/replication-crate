==============================================================================
STRUCTURED REPORT — Share Issuance panel (Pontiff & Woodgate 2008)
==============================================================================

(a) PANEL DIMENSIONS
  rows            : 3,487,187
  columns         : 25
  unique permnos  : 26,913
  unique months   : 960 (1927-01-01 .. 2006-12-01)
  EWRETD months missing in grid: 0

(b) OBSERVATION COUNTS  (our vs paper)

  --- univ_all ---
  in-sample 1970-01..2003-12 total      : 2,409,708   (paper §I 2,494,343)
    per-decade avg firms/month           : {'1970s': 4010, '1980s': 5730, '1990s': 7445, '2000s': 7239}
  nonmissing ISSUE (regression, t-6/t-17): 2,203,273
  nonmissing ISSUE_contemp (Table I)     : 2,324,025   (paper Table I 2,312,597)
  nonmissing DT_ISSUE valid (dt_dum=1)   : 1,454,379
  nonmissing BM (bm_dum=1)               : 1,923,637
  nonmissing ME_june                     : 2,375,719
  nonmissing MOM                         : 2,367,675   (paper Table I 2,285,189)
  nonmissing R_{-11,0}                     : 2,272,644
  regr sample (issue & me_june & mom)    : 2,182,151   (paper Table III 2,155,945 over 396 mo)
  OOS Sep1932..Dec1969 total             : 503,063   (paper §I 568,449)
    per-decade avg firms/month           : {'1930s': 725, '1940s': 845, '1950s': 1033, '1960s': 1782}
  OOS nonmissing MOM                     : 497,200   (paper Table V 524,260)
  OOS nonmissing R_{-11,0}                 : 484,902   (paper Table V 528,200)
  OOS regr sample (issue & mom & r_11_0) : 472,979   (paper Table VI 373,590 over 444 mo)

  --- univ_common ---
  in-sample 1970-01..2003-12 total      : 2,084,351   (paper §I 2,494,343)
    per-decade avg firms/month           : {'1970s': 3771, '1980s': 5207, '1990s': 6168, '2000s': 5559}
  nonmissing ISSUE (regression, t-6/t-17): 1,913,669
  nonmissing ISSUE_contemp (Table I)     : 2,014,592   (paper Table I 2,312,597)
  nonmissing DT_ISSUE valid (dt_dum=1)   : 1,285,991
  nonmissing BM (bm_dum=1)               : 1,739,227
  nonmissing ME_june                     : 2,057,661
  nonmissing MOM                         : 2,047,889   (paper Table I 2,285,189)
  nonmissing R_{-11,0}                     : 1,967,777
  regr sample (issue & me_june & mom)    : 1,894,574   (paper Table III 2,155,945 over 396 mo)
  OOS Sep1932..Dec1969 total             : 488,446   (paper §I 568,449)
    per-decade avg firms/month           : {'1930s': 706, '1940s': 828, '1950s': 1011, '1960s': 1714}
  OOS nonmissing MOM                     : 483,034   (paper Table V 524,260)
  OOS nonmissing R_{-11,0}                 : 471,324   (paper Table V 528,200)
  OOS regr sample (issue & mom & r_11_0) : 459,910   (paper Table VI 373,590 over 444 mo)

  BM coverage (share bm_dum=1 among univ_common), by decade:
    1970s : 0.772
    1980s : 0.810
    1990s : 0.861
    2000s : 0.922

(c) TABLE I PANEL A PREVIEW  (1970-2003, monthly pool)
  Convention (reconciles to paper): base sample = universe AND ISSUE_contemp
  nonmissing (paper's widest Table I variable = 2,312,597). Within it, BM
  INCLUDES the bm_dum=0 zeros and DT-ISSUE is dummy-filled to 0 where the
  5-yr history is missing (paper reports these with dummy conventions); each
  other variable is shown over its own nonmissing obs (MOM is the narrowest).

  --- univ_all ---
  Table I base sample (ISSUE avail): 2,324,025   (paper 2,312,597)
  var                        n     mean      p25   median      p75      std   paper(mean/p25/med/p75/std)
  issue_contemp      2,324,025    0.044    0.000    0.002    0.027    0.230   0.04/0.00/0.00/0.03/0.15
  dt_issue_contemp   2,324,025    0.129    0.000    0.000    0.139    0.438   0.12/0.00/0.00/0.14/0.33
  bm                 2,324,025   -0.303   -0.783   -0.119    0.070    0.999   -0.34/-0.79/-0.07/0.00/0.94
  me_monthly         2,324,025   11.084    9.585   10.959   12.455    2.086   11.11/9.63/10.97/12.46/2.02
  mom                2,303,543    0.072   -0.160    0.025    0.216    0.481   0.06/-0.16/0.02/0.22/0.41
  r_11_0             2,270,492    0.149   -0.222    0.054    0.346    0.889   0.14/-0.23/0.05/0.34/0.88

  --- univ_common ---
  Table I base sample (ISSUE avail): 2,014,592   (paper 2,312,597)
  var                        n     mean      p25   median      p75      std   paper(mean/p25/med/p75/std)
  issue_contemp      2,014,592    0.044    0.000    0.002    0.026    0.181   0.04/0.00/0.00/0.03/0.15
  dt_issue_contemp   2,014,592    0.132    0.000    0.000    0.142    0.381   0.12/0.00/0.00/0.14/0.33
  bm                 2,014,592   -0.390   -0.847   -0.206    0.056    0.875   -0.34/-0.79/-0.07/0.00/0.94
  me_monthly         2,014,592   11.040    9.518   10.866   12.419    2.104   11.11/9.63/10.97/12.46/2.02
  mom                1,996,108    0.075   -0.168    0.022    0.227    0.488   0.06/-0.16/0.02/0.22/0.41
  r_11_0             1,967,669    0.154   -0.233    0.050    0.364    0.773   0.14/-0.23/0.05/0.34/0.88

  ISSUE_contemp sign proportions (univ_all, 1970-2003; paper 56.6/24.2/19.2):
    >0 : 56.5%   ==0 : 24.5%   <0 : 19.0%   (n=2,324,025)

(d) SHARES ERROR CORRECTION (paper L98)
  corrections applied : 2,172   (paper 2,189, 0.07%)

(e) AMBIGUITIES / SENTINELS / DEVIATIONS
  1. BM funda filter: task spec wrote consol='STD' AND popsrc='STD'; those
     values DO NOT EXIST in comp_202601.funda (consol in {C,P,R,D}; popsrc=D
     only). Implemented the correct WRDS-standard consol='C' AND popsrc='D'
     (indfmt='INDL', datafmt='STD'). Flagged for Replicator.
  2. BM units: Compustat ceq is $millions, CRSP me_dec is $thousands; bm uses
     ceq*1000/me_dec so the log ratio matches the paper (BM mean ~ -0.34).
     Without the x1000 the mean would be ~ -7.2.
  3. BM fallback is on MISSING ceq only (NULL -> use FY-2); a non-positive
     ceq at FY-1 is NOT fallen back (sets bm=0,bm_dum=0), per spec wording.
  4. Pre-July-1970 BM=0, bm_dum=0 (DFF book equity unavailable): logged
     limitation — the OOS Table V/VI BM is not available from Compustat.
  5. ClickHouse Date/toStartOfMonth clamps pre-1970 dates to the 1970 epoch;
     all month handling uses an integer midx (year*12+month-1) in SQL and
     pandas Timestamps in Python.
  6. Window/lag computations (ISSUE, MOM, forward returns) done in Python on
     a complete stock x month grid for exact calendar alignment (spec allows
     pandas here; row-based SQL lagInFrame would misalign around listing gaps).
  7. Holding-period windows past 2006-12 (t in 2004-2006) are NaN (no data /
     no EWRETD beyond the pull end); in-sample t<=2003-12 fully covered.
  8. r1 = raw month-t return; EWRETD-imputed series stored ONLY in r6/r12/
     r24_y2/r36_y3 (not in ret), per spec.
  9. Shares error correction (L98) implemented as a sequential pass on raw
     shrout (>20% jump, >=95% reversed within 3 months -> set to prior level).
     Count ~2,172 vs paper 2,189 (0.8% diff; vintage/processing detail). Paper
     states inference is unaffected by this 0.07%-of-obs correction.
 10. Universe counts run ~3% below the paper in-sample (2.41M vs 2.49M) and
     ~11% below OOS (0.50M vs 0.57M). Spec rule (b) defines first_msf_month as
     the first month with a NONMISSING return (implemented exactly); the paper
     likely counts from first CRSP appearance and/or uses retx-fallback, which
     raises counts (verified: first-appearance -> 2.45M; no 6-mo rule -> 2.54M).
 11. r_11_0 requires ALL 12 actual months per spec (no imputation), so its obs
     count is below MOM; the paper's R_{-11,0} count is >= MOM (2,312,597 range),
     implying the paper imputes R_{-11,0} with EWRETD. Implemented per spec
     (all-12-required); flag for Replicator if Table I/V R_{-11,0} must match.
 12. Table I BM/DT-ISSUE rows use the paper's dummy conventions (BM incl. the
     bm_dum=0 zeros; DT-ISSUE filled to 0 for <5yr history) over the ISSUE-
     available base sample, which reproduces the paper's reported quantiles.
==============================================================================
