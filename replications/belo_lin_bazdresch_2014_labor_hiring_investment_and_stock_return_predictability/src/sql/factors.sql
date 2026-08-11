-- factors.sql
-- Purpose: Fetch Fama-French 3-factor monthly returns (Mkt-RF, SMB, HML, RF)
--          for the sample window (July 1965 - June 2010).
--          Project dt (month-end) to first-of-month to match the panel's
--          month column (which is first-of-month).
--          WORKAROUND: use manual formula instead of toStartOfMonth
--          because of a ClickHouse bug where toStartOfMonth clamps
--          pre-1970 Date32 values to 1970-01-01.
-- Tables:  ff.five_factor_monthly
-- Output columns: month (first-of-month), mkt_rf, smb, hml, rf
-- Depends on: (none)
-- Settings: max_execution_time=60

SELECT
    addDays(toDate32OrNull(dt), -toDayOfMonth(toDate32OrNull(dt)) + 1) AS month,
    mkt_rf,
    smb,
    hml,
    rf
FROM ff.five_factor_monthly
WHERE toDate32OrNull(dt) >= toDate32('1965-07-01')
  AND toDate32OrNull(dt) <= toDate32('2010-06-30')
  AND mkt_rf IS NOT NULL
  AND smb   IS NOT NULL
  AND hml   IS NOT NULL
  AND rf    IS NOT NULL
SETTINGS max_execution_time = 60
