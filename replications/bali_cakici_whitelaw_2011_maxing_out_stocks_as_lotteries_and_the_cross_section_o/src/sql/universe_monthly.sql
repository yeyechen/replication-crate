-- universe_monthly.sql
-- Purpose: Monthly stock returns from CRSP msf with the same PIT universe
--          filter as universe_daily.sql (shrcd 10/11, exchcd 1/2/3).
--          Computes ME = abs(prc) * shrout (in thousands of dollars;
--          multiply by 1000 to convert to total dollars).
--          Returns missing-return sentinels filtered out.
-- Tables: crsp_202601.msf, crsp_202601.dsenames
-- Output columns: permno, month, ret, mcap, prc, shrout, hexcd
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge, max_execution_time=600
SELECT m.permno                              AS permno,
       toStartOfMonth(toDate32OrNull(m.date)) AS month,
       toDate32OrNull(m.date)               AS date,
       m.ret                                 AS ret,
       abs(m.prc) * m.shrout                 AS mcap,           -- in thousands of dollars
       m.prc                                 AS prc,
       m.shrout                              AS shrout,
       m.hexcd                               AS hexcd
FROM crsp_202601.msf AS m
INNER JOIN crsp_202601.dsenames AS n
    ON m.permno = n.permno
   AND m.date >= n.namedt
   AND m.date <= if(n.nameendt = '', '9999-12-31', n.nameendt)
WHERE n.shrcd IN (10, 11)
  AND n.exchcd IN (1, 2, 3)
  AND m.date BETWEEN '1962-01-01' AND '2006-06-30'
  AND m.ret IS NOT NULL
  AND m.ret > -0.5
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
