-- universe_monthly.sql
-- Purpose: PIT universe-filtered monthly CRSP panel for Moskowitz & Grinblatt
--          (1999) "Do Industries Explain Momentum?". Months 1962-01 .. 1995-07
--          (1962-63 warmup feeds formation windows for strategies starting
--          July 1963; Table VI FM signals need 36 months before Jan 1973).
--          Universe: a stock-month is kept iff an msenames record satisfies
--          namedt <= date <= nameendt AND shrcd IN (10,11) AND exchcd IN (1,2,3).
--          Overlapping name records: the one with the latest namedt wins
--          (argMax on namedt). Carries shrcd/exchcd/siccd (PIT SIC time series
--          from CRSP, per paper footnote 3).
--          me = abs(prc) * shrout * 1000 (dollars; shrout is in thousands).
--          dollar_vol = abs(prc) * vol.
-- Tables: crsp_202601.msf, crsp_202601.msenames
-- Output columns: permno, date (month-end), ret, vol, me, dollar_vol,
--                 shrcd, exchcd, siccd
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge (large PIT interval join),
--           max_execution_time=600
-- Notes: dates cast with toDate32 (handles pre-1970 dates and any
--        '9999-12-31'-style open-ended nameendt sentinels via clamping);
--        numerics cast to Nullable(Float64) so Decimal columns come back as
--        floats; ret sentinels (< -1) are cleaned downstream in Python.
WITH names AS (
    SELECT
        permno,
        if(namedt IS NULL OR namedt = '' OR namedt < '1900-01-01',
           toDate32('1900-01-01'), toDate32(namedt)) AS namedt,
        if(nameendt IS NULL OR nameendt = '' OR nameendt = '0000-00-00'
             OR nameendt > '2299-01-01',
           toDate32('2299-12-31'), toDate32(nameendt)) AS nameendt,
        shrcd,
        exchcd,
        siccd
    FROM crsp_202601.msenames
    WHERE shrcd IN (10, 11)
      AND exchcd IN (1, 2, 3)
),
msf_f AS (
    SELECT
        permno,
        toDate32(date) AS date,
        CAST(ret AS Nullable(Float64))      AS ret,
        CAST(vol AS Nullable(Float64))      AS vol,
        CAST(prc AS Nullable(Float64))      AS prc,
        CAST(shrout AS Nullable(Float64))   AS shrout
    FROM crsp_202601.msf
    WHERE toDate32(date) >= toDate32('1962-01-01')
      AND toDate32(date) <= toDate32('1995-07-31')
),
joined AS (
    SELECT
        m.permno                            AS permno,
        m.date                              AS date,
        any(m.ret)                          AS ret,
        any(m.vol)                          AS vol,
        abs(any(m.prc)) * any(m.shrout) * 1000.0 AS me,
        abs(any(m.prc)) * any(m.vol)        AS dollar_vol,
        argMax(n.shrcd, n.namedt)           AS shrcd,
        argMax(n.exchcd, n.namedt)          AS exchcd,
        argMax(n.siccd, n.namedt)           AS siccd
    FROM msf_f AS m
    INNER JOIN names AS n
        ON m.permno = n.permno
       AND m.date >= n.namedt
       AND m.date <= n.nameendt
    GROUP BY m.permno, m.date
)
SELECT permno, date, ret, vol, me, dollar_vol, shrcd, exchcd, siccd
FROM joined
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
