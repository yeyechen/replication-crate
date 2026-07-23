-- crsp_comp_link.sql
-- Purpose: Point-in-time CRSP <-> Compustat link (primary links only).
--          Maps CRSP permno to Compustat gvkey with a validity window so the
--          correct gvkey is used at each June-t formation date.
-- Tables: crsp_202601.ccmxpf_linktable
-- Output columns: gvkey, permno, linkdt, linkenddt
-- Depends on: (none)
-- Notes:
--   * Standard academic filter (data_verification crsp_comp_link):
--     linkprim='P', linktype IN ('LU','LC'), usedflag=1.
--   * lpermno is stored as Float64 -> cast to Int32 to match msf.permno.
--   * linkenddt NULL = open-ended link -> set to '2099-12-31' for the PIT join
--     (linkdt <= date AND linkenddt >= date).
--   * DATES ARE ISO STRINGS (some linkdt = '1900-01-01', pre-1970 -> cannot use
--     toDate()). The point-in-time merge is done in Python.
SELECT
    gvkey,
    toInt32(lpermno) AS permno,
    linkdt AS linkdt,
    if(linkenddt IS NULL, '2099-12-31', linkenddt) AS linkenddt
FROM crsp_202601.ccmxpf_linktable
WHERE linkprim = 'P'
  AND linktype IN ('LU', 'LC')
  AND usedflag = 1
  AND lpermno IS NOT NULL
  AND gvkey IS NOT NULL
  AND linkdt IS NOT NULL
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
