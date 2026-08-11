-- universe_monthly.sql
-- Purpose: PIT-filtered monthly CRSP returns with shrcd/exchcd from dsenames
-- Tables: crsp_202601.msf, crsp_202601.dsenames
-- Output columns: permno, date (Date32), month, ret, retx, prc, shrout, shrcd, exchcd
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge, max_execution_time=600
--
-- Note: dsenames is fetched in full (no date filter on namedt), then the
-- PIT join condition `d.date >= n.namedt AND d.date <= n.nameendt` selects
-- the correct name record per stock-month. Filtering namedt >= sample
-- start would silently exclude stocks listed before the sample window.
-- Sample window covers 1926-01 through 1988-06 (extends past 1987 for the
-- 60-month forward-looking R_bar_it window needed for Table I).

WITH
  -- Pre-filter the narrow sample window on the larger (msf) side, then
  -- PIT-join dsenames with the wide-history pattern. Date column cast to
  -- Date32 to avoid the pre-1970 clamp (Date clamps 1926-1969 to 1970).
  -- The aliased column is named date32 (not date) to avoid shadowing the
  -- raw string date column in the WHERE clause below.
  --
  -- Note on month-start computation: `toStartOfMonth(Date32)` returns
  -- Date and clamps pre-1970 to 1970-01-01. We compute month-start via
  -- `date - (dayOfMonth - 1) days` instead, which preserves Date32
  -- arithmetic through 1925-12-31.
  msf_filt AS (
    SELECT
      permno,
      toDate32OrNull(date)                                              AS date32,
      toDate32(toDate32OrNull(date) - toIntervalDay(dayOfMonth(toDate32OrNull(date)) - 1)) AS month,
      ret,
      retx,
      prc,
      shrout
    FROM crsp_202601.msf
    WHERE date IS NOT NULL
      AND toDate32OrNull(date) >= toDate32('1926-01-01')
      AND toDate32OrNull(date) <= toDate32('1988-12-31')
  )
SELECT
  m.permno                                                   AS permno,
  m.date32                                                   AS date,
  m.month                                                    AS month,
  m.ret                                                      AS ret,
  m.retx                                                     AS retx,
  m.prc                                                      AS prc,
  m.shrout                                                   AS shrout,
  n.shrcd                                                    AS shrcd,
  n.exchcd                                                   AS exchcd
FROM msf_filt AS m
INNER JOIN crsp_202601.dsenames AS n
  ON m.permno = n.permno
 AND m.date32 >= toDate32OrNull(n.namedt)
 AND m.date32 <= toDate32OrNull(n.nameendt)
WHERE n.shrcd IN (10, 11)
  AND n.exchcd IN (1, 2, 3)
SETTINGS max_execution_time = 600,
         join_algorithm = 'partial_merge'