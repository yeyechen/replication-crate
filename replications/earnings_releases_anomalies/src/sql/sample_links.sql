-- sample_links.sql
-- Purpose: CRSP-Compustat links for the Screen-1 gvkeys (A6): linkprim IN ('P','C'),
--          linktype IN ('LU','LC'). PIT validity per announcement (rdq within
--          [linkdt, COALESCE(linkenddt,'2100-01-01')]) and multi-link preference
--          (P first, then earliest linkdt) are resolved in Python.
-- Tables: crsp_202601.ccmxpf_lnkhist
-- Output columns: gvkey, permno (Int32), linkprim, linkdt (Date), linkenddt (Date)
-- Depends on: earnings.sql ({GVKEY_LIST} = comma-separated quoted gvkeys,
--             substituted at runtime by main.py)
SELECT
    gvkey,
    toInt32(lpermno) AS permno,
    linkprim,
    ifNull(toDateOrNull(nullIf(linkdt, '')), toDate('1900-01-01')) AS linkdt,
    ifNull(toDateOrNull(nullIf(linkenddt, '')), toDate('2100-01-01')) AS linkenddt
FROM crsp_202601.ccmxpf_lnkhist
WHERE linkprim IN ('P', 'C')
  AND linktype IN ('LU', 'LC')
  AND lpermno IS NOT NULL
  AND gvkey IN ({GVKEY_LIST})
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0;
