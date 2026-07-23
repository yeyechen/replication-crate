-- rf_monthly.sql
-- Purpose: monthly US risk-free rate (1-month T-bill) used to compute daily
--          excess returns for ALL instruments (assumption A1).
--          NOTE: ff.four_factor_monthly stores rf (and mkt_rf/smb/hml/mom)
--          already as DECIMALS in this ClickHouse build — verified:
--          1926-07 rf = 0.002503 (~3%/yr annualized), 2009 rf = 0.0.
--          Do NOT divide by 100.
-- Tables: ff.four_factor_monthly
-- Output columns: dt (month-end 'YYYY-MM-DD'), rf (decimal monthly rate)
-- Depends on: (none)
-- Settings: max_execution_time=60
SELECT dt, rf
FROM ff.four_factor_monthly
WHERE dt >= '1964-01-01'
  AND dt <= '2010-03-31'
  AND rf IS NOT NULL
ORDER BY dt
SETTINGS max_execution_time = 60
