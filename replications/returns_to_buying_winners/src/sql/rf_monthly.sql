-- rf_monthly.sql
-- Purpose: monthly risk-free rate (1-month T-bill, DECIMAL) for the Table III
--          Panel B market-model regressions (Assumption A9): rf from
--          ff.four_factor_monthly, dt = month-end 'YYYY-MM-DD' string,
--          1965-01 .. 1989-12 (300 months).
-- Tables: ff.four_factor_monthly
-- Output columns: month ('YYYY-MM' string), rf
-- Depends on: (none)
SELECT
    substring(dt, 1, 7) AS month,
    rf
FROM ff.four_factor_monthly
WHERE dt >= '1965-01-01' AND dt <= '1989-12-31'
  AND rf IS NOT NULL
ORDER BY month
SETTINGS max_execution_time = 300,
         timeout_before_checking_execution_speed = 0;
