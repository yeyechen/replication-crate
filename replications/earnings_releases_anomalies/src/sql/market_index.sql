-- market_index.sql
-- Purpose: CRSP equal-weighted NYSE+AMEX daily market index (ewretd) for the
--          Table 3 annual market-model betas (A13, var_beta_annual_regression)
--          and the Scholes-Williams estimator (needs betas for y-1, y, y+1, so
--          SW over 1974-1981 requires annual betas for 1973-1982).
-- Tables: crsp_202601.dsi
-- Output columns: date (Date), ewretd (Float64)
-- Depends on: (none)
SELECT
    toDate(date) AS date,
    ewretd
FROM crsp_202601.dsi
WHERE date BETWEEN '1973-01-01' AND '1982-12-31'
  AND ewretd IS NOT NULL
SETTINGS max_execution_time = 120,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0;
