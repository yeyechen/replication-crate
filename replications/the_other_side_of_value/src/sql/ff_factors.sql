-- ff_factors.sql
-- Purpose: Fama-French four-factor (Mkt-RF, SMB, HML, RF) plus momentum
--          (MOM), monthly, July 1963 - December 2010. For time-series
--          factor regressions of the portfolios (Tables 2-8).
-- Tables: ff.four_factor_monthly
-- Output columns: month, mkt_rf, smb, hml, rf, mom
-- Depends on: (none)
-- Notes:
--   * dt is a YYYY-MM-DD string; parsed to Date32 (pre-1970 safe;
--     `Date` clamps to 1970-01-01).
--   * Values are in DECIMALS in this ClickHouse instance (verified
--     live: mkt_rf = -0.0472 for 2000-01, rf = 0.0040 = 40 bps/month).
--     Do NOT divide by 100.
SELECT
    toDate32(dt) AS month,
    mkt_rf,
    smb,
    hml,
    rf,
    mom
FROM ff.four_factor_monthly
WHERE dt >= '1963-07-01' AND dt <= '2010-12-31'
SETTINGS max_execution_time = 120
