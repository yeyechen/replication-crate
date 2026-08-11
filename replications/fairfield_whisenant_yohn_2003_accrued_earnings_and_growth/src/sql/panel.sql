-- panel.sql
-- Purpose: Final firm-year panel for Fairfield-Whisenant-Yohn (2003).
--          Single-shot pipeline: universe + financial-services exclusion
--          + footnote-code approximation + CRSP-coverage gate + goodwill
--          filter + 3-year-window non-null gate + deflated-ratio derivation.
-- Tables: comp_202601.funda, comp_202601.funda_fncd,
--         crsp_202601.ccmxpf_linktable, crsp_202601.msf
-- Output columns: gvkey, fyear, datadate, sich, fic, plus all the raw levels
--                 (at, rect, invt, aco, ap, lco, ppent, intan, ao, lo, dp,
--                 gdwl) at t and their *_t_minus_1 / *_t_plus_1 lags/leads,
--                 YoY changes (dAR..dCLO), OA/OL/NOA at t and t-1, the four
--                 deflators (avg_ta_t, avg_ta_t_lag, avg_ta_t_plus_1), and
--                 the seven deflated ratios (roa_t, grwc_t, depam_t, acc_t,
--                 cfo_t, grnoa_t, grltnoa_t, roa_t_plus_1, opinc_t_plus_1_per_lag_def).
-- Depends on: (none -- self-contained.)
-- Settings: max_execution_time=600, partial_merge joins, max_rows_to_read=2e9

WITH
  -- ---------------------------------------------------------------
  -- 1. Universe (universe filter + financial-services exclusion)
  -- The base CTE pulls fyear 1961-1993 so that the t-1, t+1, t-2 self-joins
  -- are all satisfiable for the paper's 1963-1992 sample window. The output
  -- below then restricts to fyear 1963-1992 in the final WHERE.
  -- ---------------------------------------------------------------
  base AS (
      SELECT gvkey, fyear, toDate32OrNull(datadate) AS datadate,
             sich, fic,
             at, rect, invt, aco, ap, lco,
             ppent, intan, ao, lo, oiadp, dp, gdwl
      FROM comp_202601.funda
      WHERE fyear BETWEEN 1961 AND 1993
        AND indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
        AND (sich < 6000 OR sich > 6999 OR sich IS NULL)
        AND at IS NOT NULL AND at > 0
  ),
  -- Footnote codes restricted to the same filter mask (1961-1993).
  fnd AS (
      SELECT gvkey, fyear,
             at_fn, recta_fn AS rect_fn, invt_fn, ap_fn, dp_fn
      FROM comp_202601.funda_fncd
      WHERE fyear BETWEEN 1961 AND 1993
        AND indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
  ),
  -- Pre-footnote / pre-goodwill-filter firm-year table.
  filtered AS (
      SELECT b.gvkey, b.fyear, b.datadate, b.sich, b.fic,
             b.at, b.rect, b.invt, b.aco, b.ap, b.lco,
             b.ppent, b.intan, b.ao, b.lo, b.oiadp, b.dp, b.gdwl
      FROM base AS b
      LEFT JOIN fnd AS fn ON b.gvkey = fn.gvkey AND b.fyear = fn.fyear
      WHERE fn.at_fn   IS NULL
        AND fn.rect_fn IS NULL
        AND fn.invt_fn IS NULL
        AND fn.ap_fn   IS NULL
        AND fn.dp_fn   IS NULL
  ),
  -- ---------------------------------------------------------------
  -- 1b. CRSP-coverage gate (paper L187: "sufficient stock price data").
  -- Sub-CRT 1: pick the primary, active CRSP-Compustat link per (gvkey, fyear).
  --   Standard FF link filter: linktype IN ('LC','LU'), linkprim IN ('P','C'),
  --   usedflag = 1. Linkdt <= calendar-year-end and linkenddt >= calendar-
  --   year-end (or NULL) gives a PIT link for the fiscal year.
  -- Sub-CRT 2: that permno must have at least one msf row in calendar year
  --   `fyear` (firm traded during fiscal year t).
  -- Sub-CRT 3: that permno must have at least one msf row in calendar year
  --   `fyear+1` (firm traded during forward-looking year, which supplies the
  --   ROA_{t+1} numerator for regressions eqs. 1-3).
  -- Calendar-year alignment is approximate for non-Dec fiscal year-ends
  -- (the paper's "current, prior, and subsequent year" language suggests a
  -- calendar-year interpretation, which is what we use).
  -- ---------------------------------------------------------------
  link_range AS (
      SELECT
          gvkey,
          toFloat64(lpermno) AS permno,
          -- Clamp link dates to our 1962-1993 window; treat missing/blank as open-ended.
          if(linkdt = '' OR linkdt IS NULL, 1962,
             greatest(1962, toYear(toDate32OrNull(linkdt)))) AS link_start_yr,
          if(linkenddt = '' OR linkenddt IS NULL, 1993,
             least(1993, toYear(toDate32OrNull(linkenddt))))  AS link_end_yr
      FROM crsp_202601.ccmxpf_linktable
      WHERE linktype IN ('LC', 'LU')
        AND linkprim IN ('P', 'C')
        AND usedflag = 1
        AND lpermno IS NOT NULL
  ),
  msf_cov AS (
      SELECT DISTINCT
          toFloat64(permno) AS permno,
          toYear(toDate32OrNull(date)) AS cyear
      FROM crsp_202601.msf
      WHERE toYear(toDate32OrNull(date)) BETWEEN 1962 AND 1993
  ),
  crsp_covered AS (
      -- (gvkey, fyear) is CRSP-covered iff there exists a (link, permno)
      -- combination whose link PIT window covers [fyear, fyear+1] AND whose
      -- permno has msf rows in BOTH calendar years fyear and fyear+1.
      -- Use CROSS JOIN + WHERE for the range filter (ClickHouse cannot
      -- use partial_merge with non-equi JOIN ON expressions).
      SELECT DISTINCT lr.gvkey, fy.fyear
      FROM link_range AS lr
      CROSS JOIN (SELECT DISTINCT fyear FROM filtered) AS fy
      INNER JOIN msf_cov AS m1 ON m1.permno = lr.permno AND m1.cyear = fy.fyear
      INNER JOIN msf_cov AS m2 ON m2.permno = lr.permno AND m2.cyear = fy.fyear + 1
      WHERE fy.fyear BETWEEN lr.link_start_yr AND lr.link_end_yr
  ),
  -- ---------------------------------------------------------------
  -- 2. Self-joins for t-1, t+1, t-2 -- a single pass through `filtered`
  -- ---------------------------------------------------------------
  t_minus_1 AS (
      SELECT gvkey, fyear,
             datadate AS datadate_t_minus_1,
             at AS at_t_minus_1, rect AS rect_t_minus_1, invt AS invt_t_minus_1,
             aco AS aco_t_minus_1, ap AS ap_t_minus_1, lco AS lco_t_minus_1,
             ppent AS ppent_t_minus_1, intan AS intan_t_minus_1,
             ao AS ao_t_minus_1, lo AS lo_t_minus_1,
             gdwl AS gdwl_t_minus_1
      FROM filtered
  ),
  t_plus_1 AS (
      SELECT gvkey, fyear,
             datadate AS datadate_t_plus_1,
             at AS at_t_plus_1, oiadp AS oiadp_t_plus_1,
             rect AS rect_t_plus_1, invt AS invt_t_plus_1,
             aco AS aco_t_plus_1, ap AS ap_t_plus_1, lco AS lco_t_plus_1,
             ppent AS ppent_t_plus_1, intan AS intan_t_plus_1,
             ao AS ao_t_plus_1, lo AS lo_t_plus_1
      FROM filtered
  ),
  t_minus_2 AS (
      SELECT gvkey, fyear, datadate AS datadate_t_minus_2,
             at AS at_t_minus_2
      FROM filtered
  )
SELECT
    f.gvkey,
    f.fyear,
    f.datadate,
    f.sich,
    f.fic,

    -- Raw levels at t
    f.oiadp  AS oiadp_t,
    f.at     AS at_t,
    f.rect   AS rect_t,
    f.invt   AS invt_t,
    f.aco    AS aco_t,
    f.ap     AS ap_t,
    f.lco    AS lco_t,
    f.ppent  AS ppent_t,
    f.intan  AS intan_t,
    f.ao     AS ao_t,
    f.lo     AS lo_t,
    f.dp     AS depam_t,
    f.gdwl   AS gdwl_t,
    t1.gdwl_t_minus_1,

    -- Deflators (paper L194, L403-419, L116-117)
    (f.at + t1.at_t_minus_1) / 2.0              AS avg_ta_t,
    (t3.at_t_minus_2 + t1.at_t_minus_1) / 2.0   AS avg_ta_t_lag,
    (f.at + t2.at_t_plus_1) / 2.0               AS avg_ta_t_plus_1,

    -- YoY changes (paper L227-228)
    (f.rect - t1.rect_t_minus_1) AS dAR_t,
    (f.invt - t1.invt_t_minus_1) AS dINV_t,
    (f.aco  - t1.aco_t_minus_1)  AS dCAO_t,
    (f.ap   - t1.ap_t_minus_1)   AS dAP_t,
    (f.lco  - t1.lco_t_minus_1)  AS dCLO_t,

    -- Operating-asset / liability aggregates (paper L272-296)
    (f.rect + f.invt + f.aco + f.ppent + f.intan + f.ao) AS oa_t,
    (f.ap + f.lco + f.lo)                                  AS ol_t,
    ((f.rect + f.invt + f.aco + f.ppent + f.intan + f.ao)
       - (f.ap + f.lco + f.lo))                            AS noa_t,

    -- NOA_t_minus_1 (for GrNOA = NOA_t - NOA_{t-1}, paper L137)
    ((t1.rect_t_minus_1 + t1.invt_t_minus_1 + t1.aco_t_minus_1
       + t1.ppent_t_minus_1 + t1.intan_t_minus_1 + t1.ao_t_minus_1)
       - (t1.ap_t_minus_1 + t1.lco_t_minus_1 + t1.lo_t_minus_1)) AS noa_t_minus_1,

    -- Forward-year raw levels (at_t+1 and oiadp_t+1 are required)
    t2.at_t_plus_1,
    t2.oiadp_t_plus_1,

    -- Derived variables: all deflated by avg_ta_t (paper L297, contemporaneous deflator).
    -- Deflators are in $millions; the variables are also in $millions so the ratios are scale-free.
    f.oiadp / ((f.at + t1.at_t_minus_1) / 2.0)                                  AS roa_t,
    ((f.rect - t1.rect_t_minus_1) + (f.invt - t1.invt_t_minus_1)
       + (f.aco  - t1.aco_t_minus_1) - (f.ap   - t1.ap_t_minus_1)
       - (f.lco  - t1.lco_t_minus_1)) / ((f.at + t1.at_t_minus_1) / 2.0)         AS grwc_t,
    f.dp / ((f.at + t1.at_t_minus_1) / 2.0)                                      AS depam_over_avg_ta_t,
    ((((f.rect - t1.rect_t_minus_1) + (f.invt - t1.invt_t_minus_1)
        + (f.aco  - t1.aco_t_minus_1) - (f.ap   - t1.ap_t_minus_1)
        - (f.lco  - t1.lco_t_minus_1))
       - f.dp) / ((f.at + t1.at_t_minus_1) / 2.0))                              AS acc_t,
    (f.oiadp / ((f.at + t1.at_t_minus_1) / 2.0))
        - ((((f.rect - t1.rect_t_minus_1) + (f.invt - t1.invt_t_minus_1)
            + (f.aco  - t1.aco_t_minus_1) - (f.ap   - t1.ap_t_minus_1)
            - (f.lco  - t1.lco_t_minus_1))
           - f.dp) / ((f.at + t1.at_t_minus_1) / 2.0))                           AS cfo_t,
    (((f.rect + f.invt + f.aco + f.ppent + f.intan + f.ao)
        - (f.ap + f.lco + f.lo))
       - ((t1.rect_t_minus_1 + t1.invt_t_minus_1 + t1.aco_t_minus_1
            + t1.ppent_t_minus_1 + t1.intan_t_minus_1 + t1.ao_t_minus_1)
            - (t1.ap_t_minus_1 + t1.lco_t_minus_1 + t1.lo_t_minus_1)))
        / ((f.at + t1.at_t_minus_1) / 2.0)                                       AS grnoa_t,
    ((((f.rect + f.invt + f.aco + f.ppent + f.intan + f.ao)
         - (f.ap + f.lco + f.lo))
       - ((t1.rect_t_minus_1 + t1.invt_t_minus_1 + t1.aco_t_minus_1
            + t1.ppent_t_minus_1 + t1.intan_t_minus_1 + t1.ao_t_minus_1)
            - (t1.ap_t_minus_1 + t1.lco_t_minus_1 + t1.lo_t_minus_1)))
        - ((((f.rect - t1.rect_t_minus_1) + (f.invt - t1.invt_t_minus_1)
            + (f.aco  - t1.aco_t_minus_1) - (f.ap   - t1.ap_t_minus_1)
            - (f.lco  - t1.lco_t_minus_1))
           - f.dp))) / ((f.at + t1.at_t_minus_1) / 2.0)                          AS grltnoa_t,

    -- Forward-year deflated ratios
    t2.oiadp_t_plus_1 / ((f.at + t2.at_t_plus_1) / 2.0)                          AS roa_t_plus_1,
    t2.oiadp_t_plus_1 / ((t1.at_t_minus_1 + f.at) / 2.0)                          AS opinc_t_plus_1_per_lag_def

FROM filtered AS f
INNER JOIN t_minus_1 AS t1
        ON f.gvkey = t1.gvkey
       AND t1.fyear = f.fyear - 1
       -- f is the later year: dateDiff(date_{t-1}, date_t) is positive.
       -- The CTE dates are already parsed as Nullable(Date32) in `base`.
       AND dateDiff('day', t1.datadate_t_minus_1, f.datadate)
           BETWEEN 300 AND 430
INNER JOIN t_plus_1 AS t2
        ON f.gvkey = t2.gvkey
       AND t2.fyear = f.fyear + 1
       -- Forward adjacency uses dateDiff(date_t, date_{t+1}).
       AND dateDiff('day', f.datadate, t2.datadate_t_plus_1)
           BETWEEN 300 AND 430
INNER JOIN t_minus_2 AS t3
        ON f.gvkey = t3.gvkey
       AND t3.fyear = f.fyear - 2
       -- Two consecutive annual gaps, allowing 600--860 days in total.
       AND dateDiff('day', t3.datadate_t_minus_2, f.datadate)
           BETWEEN 600 AND 860
-- CRSP-coverage gate: paper L187 "sufficient stock price data". Filtered rows
-- must have a valid primary, active CRSP-Compustat link whose permno has msf
-- data in both calendar years fyear and fyear+1.
INNER JOIN crsp_covered AS cc ON f.gvkey = cc.gvkey AND cc.fyear = f.fyear

WHERE
    -- Restrict the output to the paper's 1963-1992 sample window.
    f.fyear BETWEEN 1963 AND 1992
    -- 3-year-window non-null gate: every variable needed to construct the
    -- seven accounting aggregates (ROA, ACC, CFO, GrNOA, GrWC, DEPAM, GrLTNOA)
    -- must be non-null at t-1 AND t. ROA_{t+1} additionally needs oiadp and at
    -- non-null at t+1. AVG(TA_{t-2}, TA_{t-1}) in eqs. 5-6 needs at_t_minus_2.
    -- This is "sufficient financial disclosures" per paper §III L175.
    -- GDWL is NOT required (it's only used in the goodwill filter, which
    -- only fires when gdwl is non-null at both t-1 and t; pre-1988 firm-
    -- years have gdwl ≈ always NULL).
    AND f.oiadp   IS NOT NULL
    AND f.at   IS NOT NULL AND f.at > 0
    AND f.rect IS NOT NULL
    AND f.invt IS NOT NULL
    AND f.aco  IS NOT NULL
    AND f.ap   IS NOT NULL
    AND f.lco  IS NOT NULL
    AND f.ppent IS NOT NULL
    AND f.intan IS NOT NULL
    AND f.ao    IS NOT NULL
    AND f.lo    IS NOT NULL
    AND f.dp    IS NOT NULL
    AND t1.at_t_minus_1        IS NOT NULL AND t1.at_t_minus_1        > 0
    AND t1.rect_t_minus_1      IS NOT NULL
    AND t1.invt_t_minus_1      IS NOT NULL
    AND t1.aco_t_minus_1       IS NOT NULL
    AND t1.ap_t_minus_1        IS NOT NULL
    AND t1.lco_t_minus_1       IS NOT NULL
    AND t1.ppent_t_minus_1     IS NOT NULL
    AND t1.intan_t_minus_1     IS NOT NULL
    AND t1.ao_t_minus_1        IS NOT NULL
    AND t1.lo_t_minus_1        IS NOT NULL
    AND t2.at_t_plus_1         IS NOT NULL AND t2.at_t_plus_1         > 0
    AND t2.oiadp_t_plus_1      IS NOT NULL
    AND t3.at_t_minus_2        IS NOT NULL AND t3.at_t_minus_2        > 0
    -- Goodwill filter (paper footnote 9 step 3): drop only if BOTH
    -- gdwl_t and gdwl_t-1 are non-null AND gdwl_t > gdwl_t-1.
    AND NOT (f.gdwl IS NOT NULL AND t1.gdwl_t_minus_1 IS NOT NULL
             AND f.gdwl > t1.gdwl_t_minus_1)
SETTINGS max_execution_time = 600,
         max_rows_to_read = 2000000000,
         timeout_before_checking_execution_speed = 0,
         join_algorithm = 'partial_merge'