-- funda_base.sql
-- Purpose: Filtered + defensively deduped Compustat funda for FY{fy_lag_start}-FY{fy_end},
--          with fiscal-year-end market equity (ME = prcc_f * csho, $millions),
--          book equity (assumption A3: ceq+txdb-pstkrv; fallback seq-pstk|pstkrv;
--          fallback at-lt-pstk), BM = BE/ME (both required > 0), and per-gvkey
--          t-1 / t-2 lag joins of all nine-signal inputs.
-- Tables: comp_202601.funda
-- Output columns: gvkey, fyear, datadate, mve, be, bm,
--                 at, at_l1, at_l2, ib, ib_l1, oancf,
--                 dltt, dlc, dltt_l1, dlc_l1,
--                 act, act_l1, lct, lct_l1,
--                 sale, sale_l1, cogs, cogs_l1, sstk
-- Depends on: (none)
-- Notes: STANDARD FILTER (WRDS-official): indfmt='INDL' AND datafmt='STD'
--        AND consol='C' AND popsrc='D'. Verified 0 duplicate (gvkey, fyear) rows
--        under this filter for FY1985-1995 in comp_202601 — the argMax-by-datadate
--        dedup is a defensive no-op kept per spec. datadate is a STRING in this
--        vintage (ISO 'YYYY-MM-DD', verified); lags are by fyear (strict fiscal-year
--        grouping, footnote 8), NOT by datadate proximity.
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
    -- Defensive dedup: one row per (gvkey, fyear), latest datadate wins.
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
           -- Market equity at fiscal year-end (footnote 7): prcc_f ($) * csho
           -- (millions of shares) = $millions. Require ME > 0.
           if(prcc_f IS NOT NULL AND csho IS NOT NULL AND prcc_f > 0 AND csho > 0,
              prcc_f * csho, CAST(NULL, 'Nullable(Float64)')) AS mve,
           -- Book equity (assumption A3).
           multiIf(
               ceq IS NOT NULL, ceq + ifNull(txdb, 0) - ifNull(pstkrv, 0),
               seq IS NOT NULL, seq - ifNull(coalesce(pstk, pstkrv), 0),
               at IS NOT NULL AND lt IS NOT NULL, at - lt - ifNull(pstk, 0),
               CAST(NULL, 'Nullable(Float64)')
           ) AS be
    FROM funda
)
SELECT t.gvkey AS gvkey, t.fyear AS fyear, t.datadate AS datadate,
       t.mve AS mve, t.be AS be,
       -- BM requires BE > 0 and ME > 0 (negative/zero book equity dropped).
       if(t.be IS NOT NULL AND t.be > 0 AND t.mve IS NOT NULL,
          t.be / t.mve, CAST(NULL, 'Nullable(Float64)')) AS bm,
       t.at AS at, f1.at AS at_l1, f2.at AS at_l2,
       t.ib AS ib, f1.ib AS ib_l1,
       t.oancf AS oancf,
       t.dltt AS dltt, t.dlc AS dlc, f1.dltt AS dltt_l1, f1.dlc AS dlc_l1,
       t.act AS act, f1.act AS act_l1,
       t.lct AS lct, f1.lct AS lct_l1,
       t.sale AS sale, f1.sale AS sale_l1,
       t.cogs AS cogs, f1.cogs AS cogs_l1,
       t.sstk AS sstk
FROM funda_me AS t
LEFT JOIN funda_me AS f1
       ON f1.gvkey = t.gvkey AND f1.fyear = t.fyear - 1
LEFT JOIN funda_me AS f2
       ON f2.gvkey = t.gvkey AND f2.fyear = t.fyear - 2
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
