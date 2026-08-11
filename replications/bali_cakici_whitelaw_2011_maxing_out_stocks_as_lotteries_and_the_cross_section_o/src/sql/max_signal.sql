-- max_signal.sql
-- Purpose: Compute MAX = max(ret) per (permno, month) from the PIT-filtered
--          daily returns. Uses toStartOfMonth(date) to bucket daily dates
--          into calendar months.
-- Tables: depends on universe_daily.sql output (or crsp_202601.dsf directly
--         re-filtered; here we use the daily returns table directly).
-- Output columns: permno, month, max_signal
-- Depends on: (none) - re-applies the universe filter for modularity.
-- Settings: max_execution_time=600
SELECT permno,
       toStartOfMonth(toDate32OrNull(d.date)) AS month,
       max(d.ret)              AS max_signal
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
GROUP BY permno, month
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
