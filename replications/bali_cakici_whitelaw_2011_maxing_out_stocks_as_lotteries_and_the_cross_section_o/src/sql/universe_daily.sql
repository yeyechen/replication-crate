-- universe_daily.sql
-- Purpose: PIT-filtered daily returns for MAX signal construction.
--          Common shares (shrcd IN (10,11)) on NYSE/AMEX/Nasdaq (exchcd IN (1,2,3))
--          for the sample window Jan 1962 - Jun 2006 (we need to form portfolios
--          through end of Dec 2005). Missing-return sentinels filtered out.
-- Tables: crsp_202601.dsf, crsp_202601.dsenames
-- Output columns: permno, date, ret
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge, max_execution_time=600
SELECT d.permno                AS permno,
       toDate32OrNull(d.date)  AS date,
       d.ret                   AS ret
FROM crsp_202601.dsf AS d
INNER JOIN crsp_202601.dsenames AS n
    ON d.permno = n.permno
   AND d.date >= n.namedt
   AND d.date <= if(n.nameendt = '', '9999-12-31', n.nameendt)
WHERE n.shrcd IN (10, 11)
  AND n.exchcd IN (1, 2, 3)
  AND d.date BETWEEN '1962-01-01' AND '2006-06-30'
  AND d.ret IS NOT NULL
  AND d.ret > -0.5
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
