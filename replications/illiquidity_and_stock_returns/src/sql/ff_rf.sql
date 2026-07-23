-- ff_rf.sql
-- Purpose: Monthly risk-free rate (one-month T-bill) for Amihud (2002)
--          Tables 3-4, 1963-01 .. 1996-12. Decimal: in THIS instance
--          ff.four_factor_monthly.rf is already in decimal (verified:
--          1963-01 rf = 0.00220, matches crsp_202601.mcti.t30ret =
--          0.00251) — no /100 conversion needed. Backup source if ever
--          required: crsp_202601.mcti.t30ret.
-- Tables: ff.four_factor_monthly (dt is a 'YYYY-MM-DD' string)
-- Output columns: month (Date32 first-of-month), rf
-- Depends on: (none)
SELECT
    toDate32(dt) AS month,
    rf           AS rf
FROM ff.four_factor_monthly
WHERE dt >= '1963-01-01' AND dt <= '1996-12-31'
ORDER BY dt
SETTINGS max_execution_time = 60
