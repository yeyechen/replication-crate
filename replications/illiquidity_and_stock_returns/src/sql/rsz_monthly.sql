-- rsz_monthly.sql
-- Purpose: CRSP monthly size-decile portfolio returns (RSZ_i series for
--          Amihud 2002 Tables 3-4) plus the CRSP EW market index,
--          1963-01 .. 1996-12. Decimals. Verified: decret1 = smallest
--          firms, decret10 = largest.
-- Tables: crsp_202601.msib (caldt is a 'YYYY-MM-DD' string)
-- Output columns: month (Date32 first-of-month), decret1..decret10,
--                 ewretd_msib
-- Depends on: (none)
SELECT
    toDate32(caldt) AS month,
    decret1, decret2, decret3, decret4, decret5,
    decret6, decret7, decret8, decret9, decret10,
    ewretd AS ewretd_msib
FROM crsp_202601.msib
WHERE caldt >= '1963-01-01' AND caldt <= '1996-12-31'
ORDER BY caldt
SETTINGS max_execution_time = 60
