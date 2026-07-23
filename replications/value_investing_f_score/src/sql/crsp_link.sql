-- crsp_link.sql
-- Purpose: One CRSP permno per Compustat gvkey-fyear, via the point-in-time
--          CRSP/Compustat link. Standard FF link filter (references/COMPUSTAT.md):
--          linkprim IN ('P','C') — primary + Compustat-confirmed secondary links —
--          linktype IN ('LC','LU'), usedflag=1, temporal validity at the fiscal
--          year-end datadate: linkdt <= datadate AND (linkenddt >= datadate OR
--          linkenddt IS NULL). Tie-break when several links are active at
--          datadate: argMax by (P-priority, linkdt) — a primary ('P') link ALWAYS
--          beats a secondary ('C') link; within the same class the most recently
--          started link wins. This file is the single source of CRSP permnos for
--          the whole pipeline (panel merge, MOMENT/ACCRUAL decile universe, and
--          returns_windows.sql via the staged scratch table).
-- Tables: comp_202601.funda (gvkey/datadate universe), crsp_202601.ccmxpf_linktable
-- Output columns: gvkey, fyear, datadate, permno
-- Depends on: (none)
-- Notes: linktable columns are strings/floats in this vintage — lpermno is
--        Nullable(Float64) with integer values (verified), cast to Int32;
--        linkdt/linkenddt/datadate are ISO 'YYYY-MM-DD' strings (verified), so
--        lexicographic comparison is chronological. Covers funda FY{fy_lag_start}..
--        FY{fy_end}; gvkeys with no valid P/C link at datadate produce no row.
-- Settings: max_execution_time=300, max_rows_to_read=10e9

WITH comp_gv AS (
    -- dd alias: max(datadate) cannot be aliased `datadate` here — ClickHouse
    -- would resolve the alias (an aggregate) inside the JOIN predicate below.
    SELECT gvkey, fyear, max(datadate) AS dd
    FROM comp_202601.funda
    WHERE indfmt = 'INDL' AND datafmt = 'STD' AND consol = 'C' AND popsrc = 'D'
      AND fyear BETWEEN {fy_lag_start} AND {fy_end}
      AND gvkey IS NOT NULL AND fyear IS NOT NULL AND datadate IS NOT NULL
    GROUP BY gvkey, fyear
),
link AS (
    SELECT gvkey,
           toInt32(lpermno) AS permno,
           linkdt,
           linkenddt,
           linkprim
    FROM crsp_202601.ccmxpf_linktable
    WHERE linkprim IN ('P', 'C')
      AND linktype IN ('LC', 'LU')
      AND usedflag = 1
      AND gvkey IS NOT NULL
      AND lpermno IS NOT NULL
      AND linkdt IS NOT NULL
)
SELECT c.gvkey AS gvkey,
       c.fyear AS fyear,
       c.dd AS datadate,
       -- Tie-break: (P-priority, linkdt) — primary beats secondary, then the
       -- most recently started link.
       argMax(l.permno, (if(l.linkprim = 'P', 1, 0), l.linkdt)) AS permno
FROM comp_gv AS c
INNER JOIN link AS l
        ON l.gvkey = c.gvkey
       AND l.linkdt <= c.dd
       AND (l.linkenddt >= c.dd OR l.linkenddt IS NULL)
GROUP BY c.gvkey, c.fyear, c.dd
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
