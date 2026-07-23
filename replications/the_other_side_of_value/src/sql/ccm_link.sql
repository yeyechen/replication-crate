-- ccm_link.sql
-- Purpose: CRSP-Compustat link (gvkey -> lpermno) with point-in-time
--          validity windows, for merging Compustat fundamentals onto
--          CRSP permnos.
-- Tables: crsp_202601.ccmxpf_linktable
-- Output columns: gvkey, permno, linkdt, linkenddt
-- Depends on: (none)
-- Notes:
--   * Standard FF link filter: usedflag = 1, linkprim IN ('P','C'),
--     linktype IN ('LC','LU'). lpermno IS NOT NULL (unresolved links
--     carry NULL lpermno).
--   * linkdt / linkenddt returned as ISO strings; the temporal merge
--     (datadate BETWEEN linkdt AND linkenddt) is done in main.py.
--   * lpermno is Nullable(Float64) -> cast to Int32.
SELECT
    gvkey,
    toInt32(lpermno) AS permno,
    linkdt,
    ifNull(linkenddt, '2099-12-31') AS linkenddt
FROM crsp_202601.ccmxpf_linktable
WHERE usedflag = 1
  AND linkprim IN ('P', 'C')
  AND linktype IN ('LC', 'LU')
  AND lpermno IS NOT NULL
SETTINGS max_execution_time = 120
