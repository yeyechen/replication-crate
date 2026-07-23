-- ccm_link.sql
-- Purpose: CRSP-Compustat link intervals (gvkey <-> permno) using the standard
--          FF filter (linktype LC/LU, usedflag=1, linkprim P/C). linkdt/linkenddt
--          are returned as strings ('YYYY-MM-DD'); NULL linkenddt means the link
--          is still active (handled as far-future downstream).
-- Tables: crsp_202601.ccmxpf_linktable
-- Output columns: gvkey, permno, linkdt, linkenddt, linkprim
-- Depends on: (none)
-- Settings: max_execution_time=300
SELECT
    gvkey,
    lpermno AS permno,
    linkdt,
    linkenddt,
    linkprim
FROM crsp_202601.ccmxpf_linktable
WHERE linktype IN ('LC', 'LU')
  AND linkprim IN ('P', 'C')
  AND usedflag = 1
  AND lpermno IS NOT NULL
  AND gvkey IS NOT NULL
  AND gvkey != ''
SETTINGS max_execution_time = 300,
         max_rows_to_read = 1000000000,
         timeout_before_checking_execution_speed = 0
