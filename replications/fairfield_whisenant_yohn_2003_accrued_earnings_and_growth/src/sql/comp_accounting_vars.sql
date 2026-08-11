-- comp_accounting_vars.sql
-- Purpose: Per-firm-year raw-level + YoY-change computation, with self-joins
--          to t-1, t+1, t-2. Audit breakout of the same logic inlined in
--          panel.sql. GDWL is included only to enable the goodwill filter in
--          panel.sql; the seven accounting aggregates do not need GDWL.
-- Tables: comp_202601.funda (self-joined t, t-1, t+1, t-2)
-- Output columns: gvkey, fyear, raw levels at t/t-1/t+1/t-2, YoY changes.
-- Depends on: (none -- self-contained)
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
)
SELECT
    t0.gvkey,
    t0.fyear,

    -- Raw levels at t
    t0.oiadp   AS oiadp_t,
    t0.at      AS at_t,
    t0.rect    AS rect_t,
    t0.invt    AS invt_t,
    t0.aco     AS aco_t,
    t0.ap      AS ap_t,
    t0.lco     AS lco_t,
    t0.ppent   AS ppent_t,
    t0.intan   AS intan_t,
    t0.ao      AS ao_t,
    t0.lo      AS lo_t,
    t0.dp      AS depam_t,
    t0.gdwl    AS gdwl_t,

    -- Lagged levels at t-1
    t1.at_t_minus_1,
    t1.rect_t_minus_1,
    t1.invt_t_minus_1,
    t1.aco_t_minus_1,
    t1.ap_t_minus_1,
    t1.lco_t_minus_1,
    t1.ppent_t_minus_1,
    t1.intan_t_minus_1,
    t1.ao_t_minus_1,
    t1.lo_t_minus_1,
    t1.gdwl_t_minus_1,

    -- t-2 (for the lagged deflator in eqs. 5-6)
    t3.at_t_minus_2,

    -- Forward levels at t+1
    t2.at_t_plus_1,
    t2.oiadp_t_plus_1,

    -- YoY changes in working-capital components (paper L227-228)
    (t0.rect - t1.rect_t_minus_1)        AS dAR_t,
    (t0.invt - t1.invt_t_minus_1)        AS dINV_t,
    (t0.aco  - t1.aco_t_minus_1)         AS dCAO_t,
    (t0.ap   - t1.ap_t_minus_1)          AS dAP_t,
    (t0.lco  - t1.lco_t_minus_1)         AS dCLO_t,

    -- OA, OL, NOA at t (paper L272-296)
    (t0.rect + t0.invt + t0.aco + t0.ppent + t0.intan + t0.ao)  AS oa_t,
    (t0.ap + t0.lco + t0.lo)                                     AS ol_t,
    ((t0.rect + t0.invt + t0.aco + t0.ppent + t0.intan + t0.ao)
       - (t0.ap + t0.lco + t0.lo))                               AS noa_t,

    -- Lagged NOA at t-1 (for GrNOA_t = NOA_t - NOA_{t-1}, paper L137)
    ((t1.rect_t_minus_1 + t1.invt_t_minus_1 + t1.aco_t_minus_1
        + t1.ppent_t_minus_1 + t1.intan_t_minus_1 + t1.ao_t_minus_1)
       - (t1.ap_t_minus_1 + t1.lco_t_minus_1 + t1.lo_t_minus_1)) AS noa_t_minus_1,

    -- Deflator at t (paper L194): AVG(TA_{t-1} + TA_t)
    (t0.at + t1.at_t_minus_1) / 2.0        AS avg_ta_t,

    -- Lagged deflator for eqs. 5-6 (paper L403-419): AVG(TA_{t-2} + TA_{t-1})
    (t3.at_t_minus_2 + t1.at_t_minus_1) / 2.0 AS avg_ta_t_lag

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
INNER JOIN (
    SELECT gvkey, fyear, at AS at_t_minus_2
    FROM base
) AS t3 ON t0.gvkey = t3.gvkey AND t3.fyear = t0.fyear - 2
SETTINGS max_execution_time = 300,
         max_rows_to_read = 1000000000,
         timeout_before_checking_execution_speed = 0,
         join_algorithm = 'partial_merge'
