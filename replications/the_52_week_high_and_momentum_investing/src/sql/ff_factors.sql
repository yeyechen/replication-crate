-- ff_factors.sql
-- Purpose: Fama-French 3-factor monthly realizations for Table V/VII
--          risk adjustment (Mkt-RF, SMB, HML). Values are DECIMALS in the
--          source table; the Python caller multiplies by 100 to percent.
-- Tables: ff.four_factor_monthly
-- Output columns: dt, mkt_rf, smb, hml
-- Depends on: (none)
-- Settings: max_execution_time=120
SELECT
    dt,
    mkt_rf,
    smb,
    hml
FROM ff.four_factor_monthly
WHERE dt >= '1963-07-01'
  AND dt <= '2001-12-31'
  AND mkt_rf IS NOT NULL
  AND smb IS NOT NULL
  AND hml IS NOT NULL
ORDER BY dt
SETTINGS max_execution_time = 120;
