-- crsp_join.sql
-- Purpose: Build CRSP coverage flag — for each (gvkey, fyear), check whether
--          the firm has at least one CRSP daily return record in the 12
--          calendar months following fiscal year-end (datadate). This
--          implements the paper's "have contemporaneous and future return
--          data on CRSP" filter (paper L498, footnote 24).
-- Tables: comp_202601.funda (datadate), crsp_202601.ccmxpf_linktable
--         (gvkey -> permno PIT link), crsp_202601.dsf (daily returns)
-- Output columns: gvkey (String), fyear (Int32)
-- Depends on: (none — but consumed by panel.sql after the comp CTE chain)
-- Settings: max_execution_time=600, max_rows_to_read=5e8, join_algorithm=partial_merge
--
-- Strategy: For each (gvkey, fyear) in the compustat universe, look up
-- permnos via ccmxpf_linktable with PIT-validity check on fiscal year-end.
-- Require primary links only (linktype IN ('LC','LU'), linkprim IN ('P','C')).
-- Then check that dsf has at least one non-null return for any of those
-- permnos in the window (datadate+1month, datadate+12months].
--
-- Documented separately; the actual logic is folded into panel.sql.

WITH
  comp_dates AS (
    -- One row per (gvkey, fyear) with the fiscal year-end datadate.
    -- Filtered to the same universe as the comp_with_noa CTE in panel.sql.
    SELECT
      f.gvkey,
      f.fyear,
      toDate32OrNull(f.datadate) AS datadate
    FROM comp_202601.funda AS f
    WHERE f.indfmt = 'INDL' AND f.consol = 'C' AND f.popsrc = 'D'
      AND f.datafmt = 'STD'
      AND f.fyear BETWEEN 1984 AND 2002
  ),
  comp_dedup AS (
    -- If a (gvkey, fyear) appears in multiple datadate records, keep the
    -- latest. Same dedup convention as the comp_dedup CTE in panel.sql.
    SELECT *
    FROM (
      SELECT
        gvkey, fyear, datadate,
        row_number() OVER (PARTITION BY gvkey, fyear ORDER BY datadate DESC) AS rn
      FROM comp_dates
      WHERE datadate IS NOT NULL
    )
    WHERE rn = 1
  ),
  linked AS (
    -- PIT-join compustat to CRSP permnos. The link table uses linkenddt IS
    -- NULL to mark "still active" (not the '0000-00-00' sentinel).
    SELECT DISTINCT
      c.gvkey,
      c.fyear,
      c.datadate,
      toInt32(l.lpermno) AS permno
    FROM comp_dedup AS c
    INNER JOIN crsp_202601.ccmxpf_linktable AS l
      ON l.gvkey = c.gvkey
     AND l.linktype IN ('LC', 'LU')
     AND l.linkprim IN ('P', 'C')
     AND l.lpermno IS NOT NULL
     AND c.datadate >= toDate32OrNull(l.linkdt)
     AND (l.linkenddt IS NULL OR c.datadate <= toDate32OrNull(l.linkenddt))
  ),
  crsp_window AS (
    -- For each (gvkey, fyear) we need at least one daily return record
    -- in the 12 calendar months after fiscal year-end. dsf.date is a
    -- Nullable(String) — cast to Date32 for comparison.
    SELECT DISTINCT
      lk.gvkey,
      lk.fyear
    FROM linked AS lk
    INNER JOIN crsp_202601.dsf AS d
      ON d.permno = lk.permno
     AND toDate32OrNull(d.date) > lk.datadate
     AND toDate32OrNull(d.date) <= addMonths(lk.datadate, 12)
     AND d.ret IS NOT NULL
  )
SELECT gvkey, fyear
FROM crsp_window
SETTINGS max_execution_time = 600,
         max_rows_to_read = 500000000,
         timeout_before_checking_execution_speed = 0
