-- 03_ccm_link.sql
-- Purpose: CRSP-Compustat link (Step 2 of the pipeline). Standard FF link
--          filter: linktype IN ('LU','LC'), linkprim IN ('P','C'),
--          usedflag = 1. Normalizes linkdt/linkenddt to Date with
--          open-ended links (NULL linkenddt -> 2099-12-31) for the PIT
--          condition linkdt <= datadate AND (linkenddt >= datadate OR
--          linkenddt IS NULL).
-- Tables: crsp_202601.ccmxpf_linktable
-- Output: write_yeye.qmj_link (gvkey String, permno Int32, linkdt Date,
--         linkenddt Date) — 33,324 rows
-- Depends on: (none)

CREATE OR REPLACE TABLE write_yeye.qmj_link
ENGINE = MergeTree ORDER BY (gvkey, permno) AS
SELECT
    assumeNotNull(gvkey)            AS gvkey,
    assumeNotNull(toInt32(lpermno)) AS permno,
    toDate32(linkdt)                  AS linkdt,
    ifNull(toDate32(linkenddt), toDate32('2099-12-31')) AS linkenddt
FROM crsp_202601.ccmxpf_linktable
WHERE linktype IN ('LU', 'LC')
  AND linkprim IN ('P', 'C')
  AND usedflag = 1
  AND lpermno IS NOT NULL
  AND gvkey IS NOT NULL
SETTINGS allow_experimental_analyzer = 0,
         max_execution_time = 300
