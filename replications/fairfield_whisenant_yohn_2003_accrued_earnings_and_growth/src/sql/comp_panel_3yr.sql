-- comp_panel_3yr.sql
-- Purpose: Audit breakout of panel.sql restricted to firm-years with non-null
--          required raw inputs at t-1, t, AND t+1. NO deflator or ratio math
--          happens here -- only the availability gate ("3-year panel").
-- Tables: comp_202601.funda (self-joined)
-- Output columns: gvkey, fyear, all raw levels, YoY changes, OA/OL/NOA, deflators.
-- Depends on: comp_accounting_vars.sql (same logic, inlined here for portability)
-- Settings: max_execution_time=300, partial_merge joins.

WITH base AS (
    SELECT gvkey, fyear,
           at, rect, invt, aco, ap, lco,
           ppent, intan, ao, lo, oiadp, dp, gdwl
    FROM comp_202601.funda
    WHERE fyear BETWEEN 1961 AND 1993
      AND indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
      AND (sich < 6000 OR sich > 6999 OR sich IS NULL)
      AND at IS NOT NULL AND at > 0
),
t_minus_2 AS (SELECT gvkey, fyear, at AS at_t_minus_2 FROM base)
SELECT
    t0.gvkey, t0.fyear,
    t0.oiadp AS oiadp_t, t0.at AS at_t,
    t0.rect AS rect_t, t0.invt AS invt_t, t0.aco AS aco_t,
    t0.ap AS ap_t, t0.lco AS lco_t,
    t0.ppent AS ppent_t, t0.intan AS intan_t,
    t0.ao AS ao_t, t0.lo AS lo_t,
    t0.dp AS depam_t, t0.gdwl AS gdwl_t,

    t1.at_t_minus_1, t1.rect_t_minus_1, t1.invt_t_minus_1, t1.aco_t_minus_1,
    t1.ap_t_minus_1, t1.lco_t_minus_1, t1.ppent_t_minus_1, t1.intan_t_minus_1,
    t1.ao_t_minus_1, t1.lo_t_minus_1, t1.gdwl_t_minus_1,

    t3.at_t_minus_2,
    t2.at_t_plus_1, t2.oiadp_t_plus_1,

    (t0.rect - t1.rect_t_minus_1) AS dAR_t,
    (t0.invt - t1.invt_t_minus_1) AS dINV_t,
    (t0.aco  - t1.aco_t_minus_1)  AS dCAO_t,
    (t0.ap   - t1.ap_t_minus_1)   AS dAP_t,
    (t0.lco  - t1.lco_t_minus_1)  AS dCLO_t,

    (t0.rect + t0.invt + t0.aco + t0.ppent + t0.intan + t0.ao) AS oa_t,
    (t0.ap + t0.lco + t0.lo)                                  AS ol_t,
    ((t0.rect + t0.invt + t0.aco + t0.ppent + t0.intan + t0.ao)
       - (t0.ap + t0.lco + t0.lo))                            AS noa_t,

    ((t1.rect_t_minus_1 + t1.invt_t_minus_1 + t1.aco_t_minus_1
        + t1.ppent_t_minus_1 + t1.intan_t_minus_1 + t1.ao_t_minus_1)
        - (t1.ap_t_minus_1 + t1.lco_t_minus_1 + t1.lo_t_minus_1)) AS noa_t_minus_1,

    (t0.at + t1.at_t_minus_1) / 2.0              AS avg_ta_t,
    (t3.at_t_minus_2 + t1.at_t_minus_1) / 2.0   AS avg_ta_t_lag

FROM base AS t0
INNER JOIN (
    SELECT gvkey, fyear,
           at AS at_t_minus_1, rect AS rect_t_minus_1, invt AS invt_t_minus_1,
           aco AS aco_t_minus_1, ap AS ap_t_minus_1, lco AS lco_t_minus_1,
           ppent AS ppent_t_minus_1, intan AS intan_t_minus_1,
           ao AS ao_t_minus_1, lo AS lo_t_minus_1, gdwl AS gdwl_t_minus_1
    FROM base
) AS t1 ON t0.gvkey = t1.gvkey AND t1.fyear = t0.fyear - 1
INNER JOIN (
    SELECT gvkey, fyear,
           at AS at_t_plus_1, oiadp AS oiadp_t_plus_1
    FROM base
) AS t2 ON t0.gvkey = t2.gvkey AND t2.fyear = t0.fyear + 1
INNER JOIN t_minus_2 AS t3 ON t0.gvkey = t3.gvkey AND t3.fyear = t0.fyear - 2

WHERE
    -- Output window restricted to the paper's 1963-1992 sample period.
    t0.fyear BETWEEN 1963 AND 1992
    -- 3-year-window non-null gate (paper §III L175 "sufficient financial
    -- disclosures"). GDWL is intentionally excluded -- it's only used by the
    -- goodwill filter, which only fires when both gdwl_t and gdwl_t-1 are
    -- non-null. Pre-1988 gdwl coverage in comp_202601 is essentially zero.
    AND t0.oiadp IS NOT NULL
    AND t0.at > 0
    AND t0.rect IS NOT NULL AND t0.invt IS NOT NULL AND t0.aco IS NOT NULL
    AND t0.ap   IS NOT NULL AND t0.lco  IS NOT NULL
    AND t0.ppent IS NOT NULL AND t0.intan IS NOT NULL
    AND t0.ao   IS NOT NULL AND t0.lo   IS NOT NULL
    AND t0.dp   IS NOT NULL
    AND t1.at_t_minus_1 > 0
    AND t1.rect_t_minus_1 IS NOT NULL AND t1.invt_t_minus_1 IS NOT NULL AND t1.aco_t_minus_1 IS NOT NULL
    AND t1.ap_t_minus_1   IS NOT NULL AND t1.lco_t_minus_1  IS NOT NULL
    AND t1.ppent_t_minus_1 IS NOT NULL AND t1.intan_t_minus_1 IS NOT NULL
    AND t1.ao_t_minus_1   IS NOT NULL AND t1.lo_t_minus_1   IS NOT NULL
    AND t2.at_t_plus_1 > 0 AND t2.oiadp_t_plus_1 IS NOT NULL
    AND t3.at_t_minus_2 > 0
SETTINGS max_execution_time = 300,
         max_rows_to_read = 1000000000,
         timeout_before_checking_execution_speed = 0,
         join_algorithm = 'partial_merge'
