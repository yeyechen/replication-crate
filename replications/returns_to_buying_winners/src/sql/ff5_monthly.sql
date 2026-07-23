-- ff5_monthly.sql
-- Purpose: Fama-French five factors + rf, monthly, DECIMAL, 1965-01 .. 1989-12
--          (300 months), for the REPORT §3 / audit-1 m2 primary-portfolio
--          diagnostics: diag_ff5_alpha_* = intercept of the RAW PA 6/6
--          zero-cost return on (mkt_rf, smb, hml, rmw, cma) — zero-cost
--          convention per P18 (rf NOT subtracted from the zero-cost series);
--          the rf-subtracted documentation variant subtracts rf from the
--          left-hand side. ff.five_factor_monthly starts 1963-07-31, so the
--          full 300-month window is covered.
-- Tables: ff.five_factor_monthly
-- Output columns: month ('YYYY-MM' string), mkt_rf, smb, hml, rmw, cma, rf
-- Depends on: (none)
SELECT
    substring(dt, 1, 7) AS month,
    mkt_rf,
    smb,
    hml,
    rmw,
    cma,
    rf
FROM ff.five_factor_monthly
WHERE dt >= '1965-01-01' AND dt <= '1989-12-31'
  AND mkt_rf IS NOT NULL AND smb IS NOT NULL AND hml IS NOT NULL
  AND rmw IS NOT NULL AND cma IS NOT NULL AND rf IS NOT NULL
ORDER BY month
SETTINGS max_execution_time = 300,
         timeout_before_checking_execution_speed = 0;
