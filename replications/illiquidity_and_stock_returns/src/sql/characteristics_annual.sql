-- characteristics_annual.sql
-- Purpose: Annual stock characteristics for Amihud (2002), characteristic
--          years Y = 1963..1996, one row per (permno, Y). Subsumes the
--          logical steps universe_daily + illiq_annual + controls_annual
--          in a single dsf scan (the NYSE PIT universe join is the costly
--          part; all characteristics derive from the same daily rows).
-- Universe: NYSE ordinary common stocks, shrcd IN (10,11) AND exchcd = 1,
--          point-in-time via crsp_202601.dsfhdr (hshrcd/hexcd with
--          begdat/enddat validity windows, joined on permno + date).
-- Variables (all for year Y):
--   illiq        ILLIQ_iY = 1e6 * mean over valid days of |ret|/(|prc|*vol).
--                Valid day: ret non-null AND ret > -1 (drops CRSP missing
--                sentinels -55/-66/-77/-88/-99) AND vol > 0 AND |prc| > 0.
--                Days with |prc| = 0 are excluded from the mean via nullIf.
--                NO x100 volume adjustment: vol verified in shares for all
--                years in this vintage.
--   n_days       D_iY = count of valid days (ret valid AND vol > 0 AND
--                |prc| > 0); admission criterion (i) requires > 200.
--   n_retdays    count of days with a valid return (>= n_days).
--   sdret        SDRET_iY = 100 * stddevSamp(daily ret) over valid-return
--                days (percent units).
--   r100         R100_iY = prod(1+ret)-1 over the LAST 100 valid-return
--                days of Y (decimal); NULL if fewer than 100 valid days.
--   r100yr       R100YR_iY = prod(1+ret)-1 over valid-return days of Y
--                excluding the last 100 (decimal); NULL if none.
--   price_end    |prc| on the last dsf trading day of Y (any return status).
--   shrout_end   shrout (thousands of shares) on the last trading day of Y.
--   size_end_kusd  |prc| * shrout on the last trading day of Y = market cap
--                in $thousands (CRSP shrout is in thousands). Convert:
--                $millions = size_end_kusd/1000; $ = size_end_kusd*1000.
--   listed_dec   1 if the stock has a dsf observation in December of Y
--                (with a valid return), else 0. Part of criterion (i)
--                ("listed at the end of year Y").
--   last_date    last dsf trading date of Y.
-- Tables: crsp_202601.dsf, crsp_202601.dsfhdr
-- Output columns: permno, y, illiq, n_days, n_retdays, sdret, r100, r100yr,
--                 price_end, shrout_end, size_end_kusd, listed_dec, last_date
-- Depends on: (none)
-- Note: all date casts use toDate32 — ClickHouse Date saturates pre-1970
--       dates to 1970-01-01; Date32 covers 1900-2299.
WITH univ AS (
    SELECT
        d.permno                AS permno,
        toDate32(d.date)        AS date32,
        d.ret                   AS ret,
        abs(d.prc)              AS abs_prc,
        d.vol                   AS vol,
        d.shrout                AS shrout,
        (d.ret IS NOT NULL AND d.ret > -1) AS rv  -- valid return
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsfhdr AS h
        ON d.permno = h.permno
    WHERE h.hshrcd IN (10, 11)
      AND h.hexcd = 1
      AND d.date >= '1963-01-01' AND d.date <= '1996-12-31'
      AND toDate32(d.date) >= toDate32(h.begdat)
      AND toDate32(d.date) <= toDate32(h.enddat)
),
-- year-end snapshot + December listing flag (all dsf days, any return status)
ann_raw AS (
    SELECT
        permno,
        toYear(date32)                       AS y,
        argMax(abs_prc, date32)              AS price_end,
        argMax(shrout, date32)               AS shrout_end,
        argMax(abs_prc * shrout, date32)     AS size_end_kusd,
        maxIf(1, toMonth(date32) = 12)       AS listed_dec,
        max(date32)                          AS last_date
    FROM univ
    GROUP BY permno, y
),
-- valid-return days ranked within (permno, y), most recent first (for R100)
ranked AS (
    SELECT
        permno,
        toYear(date32) AS y,
        date32,
        ret,
        abs_prc,
        vol,
        (vol IS NOT NULL AND vol > 0 AND abs_prc > 0) AS iv,  -- valid ILLIQ day
        row_number() OVER (PARTITION BY permno, toYear(date32)
                           ORDER BY date32 DESC) AS rn_desc
    FROM univ
    WHERE rv
),
ann_ret AS (
    SELECT
        permno,
        y,
        if(countIf(iv) > 0,
           1e6 * avgIf(abs(ret) / nullIf(abs_prc * vol, 0), iv),
           NULL)                                             AS illiq,
        countIf(iv)                                          AS n_days,
        count()                                              AS n_retdays,
        if(count() > 1, 100 * stddevSamp(ret), NULL)         AS sdret,
        if(countIf(rn_desc <= 100) >= 100,
           exp(sumIf(log(1 + ret), rn_desc <= 100)) - 1,
           NULL)                                             AS r100,
        if(countIf(rn_desc > 100) > 0,
           exp(sumIf(log(1 + ret), rn_desc > 100)) - 1,
           NULL)                                             AS r100yr
    FROM ranked
    GROUP BY permno, y
)
SELECT
    r.permno        AS permno,
    r.y             AS y,
    t.illiq         AS illiq,
    t.n_days        AS n_days,
    t.n_retdays     AS n_retdays,
    t.sdret         AS sdret,
    t.r100          AS r100,
    t.r100yr        AS r100yr,
    r.price_end     AS price_end,
    r.shrout_end    AS shrout_end,
    r.size_end_kusd AS size_end_kusd,
    r.listed_dec    AS listed_dec,
    r.last_date     AS last_date
FROM ann_raw AS r
LEFT JOIN ann_ret AS t ON r.permno = t.permno AND r.y = t.y
ORDER BY r.permno, r.y
SETTINGS max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
