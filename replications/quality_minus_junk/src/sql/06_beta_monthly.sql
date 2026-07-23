-- 06_beta_monthly.sql
-- Purpose: rolling 60-month CAPM market beta per (permno, month) for the
--          BAB safety variable (BAB = -beta). First-pass beta per the
--          task spec — the paper uses the Frazzini-Pedersen (2014)
--          1-year daily vol x 5-year 3-day correlation methodology; this
--          plain 60-month rolling OLS beta is the accepted first-pass
--          simplification (flagged for refinement).
--          beta = cov(R_i - R_f, R_m - R_f) / var(R_m - R_f), window =
--          trailing 60 stock-months (ROWS frame), minimum 36 nonmissing
--          months. R_m = CRSP value-weighted index (msi.vwretd), R_f =
--          ff.four_factor_monthly.rf (already a monthly decimal in this
--          instance).
-- Tables: write_yeye.qmj_univ_m, crsp_202601.msi, ff.four_factor_monthly
-- Output: write_yeye.qmj_beta (permno Int32, month Date, beta Float64)
-- Depends on: 05_universe_monthly.sql

CREATE OR REPLACE TABLE write_yeye.qmj_beta
ENGINE = MergeTree ORDER BY (permno, month) AS
WITH
rf AS (
    SELECT subtractDays(toDate32(dt), toDayOfMonth(toDate32(dt)) - 1) AS month, rf
    FROM ff.four_factor_monthly
    WHERE dt IS NOT NULL
),
mkt AS (
    SELECT subtractDays(toDate32(date), toDayOfMonth(toDate32(date)) - 1) AS month, vwretd
    FROM crsp_202601.msi
    WHERE date IS NOT NULL
),
x AS (
    SELECT
        u.permno     AS permno,
        u.month      AS month,
        u.ret - r.rf AS xi,      -- stock excess return
        k.vwretd - r.rf AS mi    -- market excess return
    FROM write_yeye.qmj_univ_m AS u
    INNER JOIN rf  AS r ON u.month = r.month
    INNER JOIN mkt AS k ON u.month = k.month
    WHERE u.ret IS NOT NULL AND k.vwretd IS NOT NULL
),
w AS (
    SELECT
        permno,
        month,
        count()       OVER wnd AS cnt,
        sum(xi)       OVER wnd AS sx,
        sum(mi)       OVER wnd AS sm,
        sum(xi * mi)  OVER wnd AS sxm,
        sum(mi * mi)  OVER wnd AS smm
    FROM x
    WINDOW wnd AS (PARTITION BY permno ORDER BY month
                   ROWS BETWEEN 59 PRECEDING AND CURRENT ROW)
)
SELECT
    permno,
    month,
    (sxm - sx * sm / cnt) / nullIf(smm - sm * sm / cnt, 0) AS beta
FROM w
WHERE cnt >= 36
SETTINGS allow_experimental_analyzer = 0,
         max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
