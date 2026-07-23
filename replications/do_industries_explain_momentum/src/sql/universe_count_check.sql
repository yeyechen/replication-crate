-- universe_count_check.sql
-- Purpose: validation query — distinct universe stock counts at five
--          benchmark months (1963-07, 1970-06, 1980-06, 1990-06, 1995-06).
--          Universe = msf x msenames PIT interval join with
--          shrcd IN (10,11) AND exchcd IN (1,2,3), no other screens.
--          Expected: 3478, 2270, 4632, 5818, 6775.
-- Tables: crsp_202601.msf, crsp_202601.msenames
-- Output columns: ym (YYYYMM), n
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge, max_execution_time=300
WITH names AS (
    SELECT
        permno,
        if(namedt IS NULL OR namedt = '' OR namedt < '1900-01-01',
           toDate32('1900-01-01'), toDate32(namedt)) AS namedt,
        if(nameendt IS NULL OR nameendt = '' OR nameendt = '0000-00-00'
             OR nameendt > '2299-01-01',
           toDate32('2299-12-31'), toDate32(nameendt)) AS nameendt
    FROM crsp_202601.msenames
    WHERE shrcd IN (10, 11)
      AND exchcd IN (1, 2, 3)
),
-- NB: group by toYYYYMM, NOT toStartOfMonth — toStartOfMonth(Date32)
-- returns Date and saturates pre-1970 dates to 1970-01-01, which would
-- silently drop the 1963-07 benchmark.
msf_f AS (
    SELECT permno, toDate32(date) AS date,
           toYYYYMM(toDate32(date)) AS ym
    FROM crsp_202601.msf
    WHERE toYYYYMM(toDate32(date)) IN (196307, 197006, 198006, 199006, 199506)
)
SELECT
    toYYYYMM(m.date)    AS ym,
    uniqExact(m.permno) AS n
FROM msf_f AS m
INNER JOIN names AS n
    ON m.permno = n.permno
   AND m.date >= n.namedt
   AND m.date <= n.nameendt
GROUP BY ym
ORDER BY ym
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
