-- ccm_link_pit.sql
-- Purpose: point-in-time CRSP-Compustat link valid at each June t formation
--          date (t = 1963..1990), used to attach fiscal-t-1 Compustat
--          accounting data to CRSP stocks. Filter (task spec / standard FF
--          link, references/COMPUSTAT.md): linktype IN ('LC','LU'),
--          linkprim IN ('P','C'), usedflag = 1, with PIT validity
--          linkdt <= 'YYYY-06-30' <= linkenddt (NULL linkenddt = still
--          active; 14,750 rows in this table).
--          Deduplicated to ONE gvkey per (fyr, permno) with priority
--          linkprim 'P' > 'C', then linktype 'LC' > 'LU' (argMax on the
--          priority tuple). Verified: after the standard filter there are no
--          overlapping links at a single date in this extract (0 multi-links
--          at 1975-06-30), so the dedup is a safety net.
-- Tables: crsp_202601.ccmxpf_linktable
-- Output columns:
--   fyr    Int32  formation year t
--   permno Int32  (= lpermno)
--   gvkey  String Compustat company id
-- Depends on: (none)
-- Note: lpermno / usedflag are stored as Nullable(Float64) in this extract —
--       cast lpermno to Int32 and test usedflag = 1 numerically.
WITH fy AS (SELECT CAST(arrayJoin(range(1963, 1991)), 'Int32') AS fyr)
SELECT
    f.fyr             AS fyr,
    toInt32(l.lpermno) AS permno,
    argMax(l.gvkey, tuple(l.linkprim = 'P', l.linktype = 'LC')) AS gvkey
FROM fy AS f
CROSS JOIN crsp_202601.ccmxpf_linktable AS l
WHERE l.lpermno IS NOT NULL
  AND l.gvkey IS NOT NULL AND l.gvkey != ''
  AND l.linktype IN ('LC', 'LU')
  AND l.linkprim IN ('P', 'C')
  AND l.usedflag = 1
  AND l.linkdt IS NOT NULL AND l.linkdt != ''
  AND l.linkdt <= concat(toString(f.fyr), '-06-30')
  AND (l.linkenddt IS NULL OR l.linkenddt = ''
       OR l.linkenddt >= concat(toString(f.fyr), '-06-30'))
GROUP BY f.fyr, permno
SETTINGS max_execution_time = 600;
