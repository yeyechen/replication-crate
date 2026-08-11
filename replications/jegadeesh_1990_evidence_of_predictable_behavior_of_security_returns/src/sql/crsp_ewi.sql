-- crsp_ewi.sql
-- Purpose: CRSP monthly equal-weighted index (market proxy for market model)
-- Tables: crsp_202601.msi
-- Output columns: date (Date32), month (Date32), vwretd, vwretx, ewretd, ewretx
-- Depends on: (none)
-- Settings: max_execution_time=60
--
-- The paper uses the equal-weighted index (ewretd) as the market proxy
-- for the market-model alpha regressions (paper L653).
--
-- Note: the inner cast is aliased `date32` (not `date`) so the
-- `toDate32OrNull(date)` call on the next line does not error
-- (ClickHouse's `toDate32OrNull` requires a String argument; shadowing
-- the source column with a same-named Date32 alias causes the
-- "Illegal type Date32" error).

SELECT
  toDate32OrNull(date)                                       AS date32,
  toDate32(toDate32OrNull(date) - toIntervalDay(dayOfMonth(toDate32OrNull(date)) - 1)) AS month,
  vwretd                                                     AS vwretd,
  vwretx                                                     AS vwretx,
  ewretd                                                     AS ewretd,
  ewretx                                                     AS ewretx
FROM crsp_202601.msi
WHERE date IS NOT NULL
SETTINGS max_execution_time = 60