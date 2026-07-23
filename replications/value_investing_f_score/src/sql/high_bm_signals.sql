-- high_bm_signals.sql
-- Purpose: The high-BM sample (BM quintile 5, PRIOR-fyear cutoffs over the full
--          Compustat universe) for fyear {fy_signal_start}..{fy_end}, with all nine
--          raw signal realizations, the nine binary signals, F_SCORE (0-9), and the
--          has_all_inputs completeness flag ("sufficient financial statement data"
--          clause — missing inputs are flagged, NOT imputed; main.py drops them and
--          reports the binding-signal statistics).
-- Tables: comp_202601.funda
-- Output columns: gvkey, fyear, datadate, mve, be, bm, bm_q, size_bucket,
--                 at, at_l1, at_l2, ib, ib_l1, oancf, dltt, dlc, dltt_l1, dlc_l1,
--                 act, act_l1, lct, lct_l1, sale, sale_l1, cogs, cogs_l1, sstk,
--                 roa, cfo, droa, accrual, lever, lever_l1, dlever,
--                 cr, cr_l1, dliquid, gm, gm_l1, dmargin, turn, turn_l1, dturn,
--                 eq_issued, eq_offer, has_all_inputs,
--                 f_roa, f_droa, f_cfo, f_accrual, f_dlever, f_dliquid,
--                 f_dmargin, f_dturn, f_score
-- Depends on: recomputes funda_base.sql (standard filter + argMax dedup + ME/BE/BM +
--             t-1/t-2 lags) and bm_size_cutoffs.sql (BM quintiles over ME>0 & BE>0;
--             size terciles over ME>0) as CTEs so this file is standalone/auditable.
-- Signal definitions (FY t = signal year; l1 = t-1, l2 = t-2; all scaled
--   variables use exactly these denominators):
--   1. ROA = ib(t)/at(t-1);                        F_ROA     = 1[ib(t) > 0]
--   2. CFO = oancf(t)/at(t-1);                     F_CFO     = 1[oancf(t) > 0]
--   3. DROA = ib(t)/at(t-1) - ib(t-1)/at(t-2);     F_DROA    = 1[DROA > 0]
--   4. ACCRUAL = (ib(t) - oancf(t))/at(t-1);       F_ACCRUAL = 1[oancf(t) > ib(t)]
--   5. LEVER(t) = (ifNull(dltt,0)+ifNull(dlc,0)) / ((at(t)+at(t-1))/2)
--      (BOTH dltt and dlc missing -> NULL leverage -> dropped; A5: one missing -> 0);
--      DLEVER = LEVER(t) - LEVER(t-1);             F_DLEVER  = 1[DLEVER < 0]
--   6. CR(t) = act(t)/lct(t) (lct > 0 required); DLIQUID = CR(t) - CR(t-1);
--                                                   F_DLIQUID = 1[DLIQUID > 0]
--   7. EQ_OFFER = 1[sstk(t) IS NULL OR sstk(t) <= 0]; eq_issued = 1 - EQ_OFFER (A2)
--   8. GM(t) = (sale(t) - cogs(t))/sale(t) (sale > 0); DMARGIN = GM(t) - GM(t-1);
--                                                   F_DMARGIN = 1[DMARGIN > 0]
--   9. TURN(t) = sale(t)/((at(t)+at(t-1))/2) (average assets, Table 1 fn j, A4);
--      DTURN = TURN(t) - TURN(t-1);                F_DTURN   = 1[DTURN > 0]
--   F_SCORE = F_ROA + F_DROA + F_CFO + F_ACCRUAL + F_DMARGIN + F_DTURN
--           + F_DLEVER + F_DLIQUID + EQ_OFFER   (integer 0-9)
-- Settings: max_execution_time=600, max_rows_to_read=10e9

WITH funda_raw AS (
    SELECT gvkey, fyear, datadate,
           at, ib, oancf, dltt, dlc, act, lct, sale, cogs, sstk,
           prcc_f, csho, ceq, seq, txdb, pstkrv, pstk, lt
    FROM comp_202601.funda
    WHERE indfmt = 'INDL' AND datafmt = 'STD' AND consol = 'C' AND popsrc = 'D'
      AND fyear BETWEEN {fy_lag_start} AND {fy_end}
      AND gvkey IS NOT NULL AND fyear IS NOT NULL AND datadate IS NOT NULL
),
funda AS (
    -- Defensive dedup (verified no-op under the standard filter).
    -- (dd alias avoids ClickHouse alias shadowing of the raw datadate column
    --  inside the argMax weight arguments.)
    SELECT gvkey, fyear,
           max(datadate)            AS dd,
           argMax(at, datadate)     AS at,
           argMax(ib, datadate)     AS ib,
           argMax(oancf, datadate)  AS oancf,
           argMax(dltt, datadate)   AS dltt,
           argMax(dlc, datadate)    AS dlc,
           argMax(act, datadate)    AS act,
           argMax(lct, datadate)    AS lct,
           argMax(sale, datadate)   AS sale,
           argMax(cogs, datadate)   AS cogs,
           argMax(sstk, datadate)   AS sstk,
           argMax(prcc_f, datadate) AS prcc_f,
           argMax(csho, datadate)   AS csho,
           argMax(ceq, datadate)    AS ceq,
           argMax(seq, datadate)    AS seq,
           argMax(txdb, datadate)   AS txdb,
           argMax(pstkrv, datadate) AS pstkrv,
           argMax(pstk, datadate)   AS pstk,
           argMax(lt, datadate)     AS lt
    FROM funda_raw
    GROUP BY gvkey, fyear
),
funda_me AS (
    SELECT gvkey, fyear, dd AS datadate, at, ib, oancf, dltt, dlc, act, lct,
           sale, cogs, sstk,
           -- ME = prcc_f * csho at FY-end ($millions), require > 0.
           if(prcc_f IS NOT NULL AND csho IS NOT NULL AND prcc_f > 0 AND csho > 0,
              prcc_f * csho, CAST(NULL, 'Nullable(Float64)')) AS mve,
           -- BE per assumption A3; BM requires BE > 0.
           multiIf(
               ceq IS NOT NULL, ceq + ifNull(txdb, 0) - ifNull(pstkrv, 0),
               seq IS NOT NULL, seq - ifNull(coalesce(pstk, pstkrv), 0),
               at IS NOT NULL AND lt IS NOT NULL, at - lt - ifNull(pstk, 0),
               CAST(NULL, 'Nullable(Float64)')
           ) AS be
    FROM funda
),
funda_lag AS (
    SELECT t.gvkey AS gvkey, t.fyear AS fyear, t.datadate AS datadate,
           t.mve AS mve, t.be AS be,
           if(t.be IS NOT NULL AND t.be > 0 AND t.mve IS NOT NULL,
              t.be / t.mve, CAST(NULL, 'Nullable(Float64)')) AS bm,
           t.at AS at, f1.at AS at_l1, f2.at AS at_l2,
           t.ib AS ib, f1.ib AS ib_l1, t.oancf AS oancf,
           t.dltt AS dltt, t.dlc AS dlc, f1.dltt AS dltt_l1, f1.dlc AS dlc_l1,
           t.act AS act, f1.act AS act_l1, t.lct AS lct, f1.lct AS lct_l1,
           t.sale AS sale, f1.sale AS sale_l1, t.cogs AS cogs,
           f1.cogs AS cogs_l1, t.sstk AS sstk
    FROM funda_me AS t
    LEFT JOIN funda_me AS f1
           ON f1.gvkey = t.gvkey AND f1.fyear = t.fyear - 1
    LEFT JOIN funda_me AS f2
           ON f2.gvkey = t.gvkey AND f2.fyear = t.fyear - 2
),
-- BM quintile cutoffs: full Compustat, ME>0 AND BE>0, within fyear.
-- (cut_year alias: keeps `s.*` in `assigned` from colliding with the cutoff
--  tables' year column under the analyzer's qualified-wildcard expansion.)
bm_cut AS (
    SELECT fyear AS cut_year,
           quantileExact(0.2)(bm) AS bm_p20,
           quantileExact(0.4)(bm) AS bm_p40,
           quantileExact(0.6)(bm) AS bm_p60,
           quantileExact(0.8)(bm) AS bm_p80
    FROM funda_lag
    WHERE bm IS NOT NULL
    GROUP BY cut_year
),
-- Size tercile cutoffs: full Compustat, ME>0, within fyear.
size_cut AS (
    SELECT fyear AS cut_year,
           quantileExact(0.3333333)(mve) AS me_p33,
           quantileExact(0.6666667)(mve) AS me_p67
    FROM funda_lag
    WHERE mve IS NOT NULL
    GROUP BY cut_year
),
signals AS (
    SELECT *,
           -- 1. ROA
           if(at_l1 > 0 AND ib IS NOT NULL, ib / at_l1,
              CAST(NULL, 'Nullable(Float64)')) AS roa,
           -- 2. CFO
           if(at_l1 > 0 AND oancf IS NOT NULL, oancf / at_l1,
              CAST(NULL, 'Nullable(Float64)')) AS cfo,
           -- 3. ΔROA
           if(at_l1 > 0 AND at_l2 > 0 AND ib IS NOT NULL AND ib_l1 IS NOT NULL,
              ib / at_l1 - ib_l1 / at_l2, CAST(NULL, 'Nullable(Float64)')) AS droa,
           -- 4. ACCRUAL
           if(at_l1 > 0 AND ib IS NOT NULL AND oancf IS NOT NULL,
              (ib - oancf) / at_l1, CAST(NULL, 'Nullable(Float64)')) AS accrual,
           -- 5. LEVER (both dltt AND dlc missing -> NULL = drop)
           if(at > 0 AND at_l1 > 0 AND NOT (dltt IS NULL AND dlc IS NULL),
              (ifNull(dltt, 0) + ifNull(dlc, 0)) / ((at + at_l1) / 2),
              CAST(NULL, 'Nullable(Float64)')) AS lever,
           if(at_l1 > 0 AND at_l2 > 0 AND NOT (dltt_l1 IS NULL AND dlc_l1 IS NULL),
              (ifNull(dltt_l1, 0) + ifNull(dlc_l1, 0)) / ((at_l1 + at_l2) / 2),
              CAST(NULL, 'Nullable(Float64)')) AS lever_l1,
           -- 6. current ratio
           if(lct > 0 AND act IS NOT NULL, act / lct,
              CAST(NULL, 'Nullable(Float64)')) AS cr,
           if(lct_l1 > 0 AND act_l1 IS NOT NULL, act_l1 / lct_l1,
              CAST(NULL, 'Nullable(Float64)')) AS cr_l1,
           -- 7. equity issuance (sstk; A2: NULL/<=0 = no issuance = good signal)
           if(sstk IS NOT NULL AND sstk > 0, 1, 0) AS eq_issued,
           -- 8. gross margin
           if(sale > 0 AND cogs IS NOT NULL, (sale - cogs) / sale,
              CAST(NULL, 'Nullable(Float64)')) AS gm,
           if(sale_l1 > 0 AND cogs_l1 IS NOT NULL, (sale_l1 - cogs_l1) / sale_l1,
              CAST(NULL, 'Nullable(Float64)')) AS gm_l1,
           -- 9. asset turnover (average-assets denominator, footnote j / A4)
           if(at > 0 AND at_l1 > 0 AND sale IS NOT NULL,
              sale / ((at + at_l1) / 2), CAST(NULL, 'Nullable(Float64)')) AS turn,
           if(at_l1 > 0 AND at_l2 > 0 AND sale_l1 IS NOT NULL,
              sale_l1 / ((at_l1 + at_l2) / 2),
              CAST(NULL, 'Nullable(Float64)')) AS turn_l1,
           -- "sufficient financial statement data": every required input present.
           -- (sstk is NEVER a drop condition — NULL sstk = no issuance.)
           (at > 0 AND at_l1 > 0 AND at_l2 > 0
            AND ib IS NOT NULL AND ib_l1 IS NOT NULL AND oancf IS NOT NULL
            AND NOT (dltt IS NULL AND dlc IS NULL)
            AND NOT (dltt_l1 IS NULL AND dlc_l1 IS NULL)
            AND act IS NOT NULL AND act_l1 IS NOT NULL
            AND lct > 0 AND lct_l1 > 0
            AND sale > 0 AND sale_l1 > 0
            AND cogs IS NOT NULL AND cogs_l1 IS NOT NULL
           ) AS has_all_inputs
    FROM funda_lag
    WHERE fyear BETWEEN {fy_signal_start} AND {fy_end}
      AND bm IS NOT NULL
),
assigned AS (
    -- PRIOR-fyear cutoffs: fyear t classified on the fyear t-1 distribution.
    SELECT s.*,
           multiIf(s.bm > cb.bm_p80, 5,
                   s.bm > cb.bm_p60, 4,
                   s.bm > cb.bm_p40, 3,
                   s.bm > cb.bm_p20, 2,
                   1) AS bm_q,
           multiIf(s.mve > cs.me_p67, 3,
                   s.mve > cs.me_p33, 2,
                   1) AS size_bucket
    FROM signals AS s
    INNER JOIN bm_cut AS cb ON cb.cut_year = s.fyear - 1
    INNER JOIN size_cut AS cs ON cs.cut_year = s.fyear - 1
)
SELECT gvkey, fyear, datadate, mve, be, bm, bm_q, size_bucket,
       at, at_l1, at_l2, ib, ib_l1, oancf,
       dltt, dlc, dltt_l1, dlc_l1,
       act, act_l1, lct, lct_l1,
       sale, sale_l1, cogs, cogs_l1, sstk,
       roa, cfo, droa, accrual,
       lever, lever_l1, lever - lever_l1 AS dlever,
       cr, cr_l1, cr - cr_l1 AS dliquid,
       gm, gm_l1, gm - gm_l1 AS dmargin,
       turn, turn_l1, turn - turn_l1 AS dturn,
       eq_issued,
       1 - eq_issued AS eq_offer,
       has_all_inputs,
       -- Binary signals (NULL-safe: missing realization -> 0; f_score is only
       -- emitted for complete firm-years, so partial rows cannot contaminate it).
       if(ib > 0, 1, 0)            AS f_roa,
       if(droa > 0, 1, 0)          AS f_droa,
       if(oancf > 0, 1, 0)         AS f_cfo,
       if(oancf > ib, 1, 0)        AS f_accrual,
       if(lever - lever_l1 < 0, 1, 0)  AS f_dlever,
       if(cr - cr_l1 > 0, 1, 0)        AS f_dliquid,
       if(gm - gm_l1 > 0, 1, 0)        AS f_dmargin,
       if(turn - turn_l1 > 0, 1, 0)    AS f_dturn,
       if(has_all_inputs,
          (if(ib > 0, 1, 0) + if(droa > 0, 1, 0) + if(oancf > 0, 1, 0)
           + if(oancf > ib, 1, 0) + if(gm - gm_l1 > 0, 1, 0)
           + if(turn - turn_l1 > 0, 1, 0) + if(lever - lever_l1 < 0, 1, 0)
           + if(cr - cr_l1 > 0, 1, 0) + (1 - eq_issued)),
          CAST(NULL, 'Nullable(Int32)')) AS f_score
FROM assigned
WHERE bm_q = 5
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
