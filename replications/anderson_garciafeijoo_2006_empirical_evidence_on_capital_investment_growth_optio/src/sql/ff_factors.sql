-- ff_factors.sql
-- Purpose: Pull Fama-French 5-factor monthly returns (MKT-RF, SMB, HML,
--          RMW, CMA, RF) for the sample window 1976-07 .. 2000-12 (which
--          covers cohort year0 1976..1998 + 1999 holdings).
-- Tables:  ff.five_factor_monthly
-- Output columns: date, month, mkt_rf, smb, hml, rmw, cma, rf
-- Depends on: (none)
-- Settings: max_execution_time=60

SELECT
    toDate32OrNull(dt)                              AS date,
    toStartOfMonth(toDate32OrNull(dt))              AS month,
    mkt_rf,
    smb,
    hml,
    rmw,
    cma,
    rf
FROM ff.five_factor_monthly
WHERE toDate32OrNull(dt) BETWEEN toDate32('1976-07-01') AND toDate32('2000-12-31')
SETTINGS max_execution_time = 60,
         max_rows_to_read = 1000000,
         timeout_before_checking_execution_speed = 0
