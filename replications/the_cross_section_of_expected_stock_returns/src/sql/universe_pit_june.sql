-- universe_pit_june.sql
-- Purpose: point-in-time CRSP universe attributes at each June t formation
--          date, t = 1963..1990. For every permno, the shrcd / exchcd / siccd
--          from the crsp_202601.dsenames record whose validity window
--          [namedt, nameendt] covers 'YYYY-06-30' (calendar month-end of the
--          June formation date). Downstream in Python:
--            * data-qualified universe: shrcd IN (10,11), exchcd IN (1,2,3),
--              NOT SIC 6000-6999 (financial exclusion, binding Assumption 4,
--              PIT record valid at the formation date);
--            * NYSE breakpoint universe (size sorts): shrcd IN (10,11),
--              exchcd = 1 (all NYSE common stocks on CRSP, paper L151).
-- Tables: crsp_202601.dsenames
-- Output columns:
--   fyr    Int32  formation year t
--   permno Int32
--   shrcd  Nullable(Int32) share code at June t
--   exchcd Nullable(Int32) exchange code at June t
--   siccd  Nullable(Int32) SIC code at June t
-- Depends on: (none)
-- Note: dsenames has exactly one valid record per (permno, date) in this
--       extract (0 overlapping windows at 1975-06-30); argMax(namedt) is a
--       safety net. Do NOT filter dsenames by namedt range (references/CRSP.md
--       gotcha) — the PIT predicate below is the window-coverage test.
WITH fy AS (SELECT CAST(arrayJoin(range(1963, 1991)), 'Int32') AS fyr)
SELECT
    f.fyr                        AS fyr,
    n.permno                     AS permno,
    argMax(n.shrcd, n.namedt)    AS shrcd,
    argMax(n.exchcd, n.namedt)   AS exchcd,
    argMax(n.siccd, n.namedt)    AS siccd
FROM fy AS f
CROSS JOIN crsp_202601.dsenames AS n
WHERE n.permno IS NOT NULL
  AND n.namedt IS NOT NULL AND n.namedt != ''
  AND n.namedt <= concat(toString(f.fyr), '-06-30')
  AND (n.nameendt IS NULL OR n.nameendt = ''
       OR n.nameendt >= concat(toString(f.fyr), '-06-30'))
GROUP BY f.fyr, n.permno
SETTINGS max_execution_time = 600;
