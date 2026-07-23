-- ff_factors.sql
-- Purpose: Fama-French 4-factor monthly returns (US) for time-series
--          alpha regressions (Tables 3 and 4).
-- Tables: ff.four_factor_monthly
-- Output columns: dt, mkt_rf, smb, hml, mom, rf
-- Depends on: (none)
-- NOTE: in this ClickHouse instance ALL columns (incl. rf) are stored
-- as monthly DECIMALS (e.g. Sep-2008 mkt_rf = -0.0935), NOT in percent.
-- Verified against known crisis-month values. No rescaling applied.
SELECT
    dt,
    mkt_rf,
    smb,
    hml,
    mom,
    rf
FROM ff.four_factor_monthly
WHERE dt IS NOT NULL
  AND dt >= '1957-01-31'
  AND dt <= '2017-06-30'
ORDER BY dt
SETTINGS max_execution_time = 60,
         max_rows_to_read = 100000,
         timeout_before_checking_execution_speed = 0
