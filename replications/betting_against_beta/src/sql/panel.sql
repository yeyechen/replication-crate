-- panel.sql
-- Purpose: FINAL monthly panel assembly. Merges the PIT-filtered monthly
--          returns + market equity with the Frazzini-Pedersen shrunk betas
--          that main.py computes in Python and stages in
--          write_yeye.bab_beta_stage (permno, month, beta).
-- Tables: crsp_202601.msf, crsp_202601.dsenames, write_yeye.bab_beta_stage
-- Output columns: permno (Int32), month (Date32 = first-of-month), ret (Float64,
--                 decimal monthly return), beta (Float64, FP shrunk beta
--                 estimated at the END OF THE PRIOR month — no look-ahead),
--                 me (Float64, $millions), log_me (Float64)
-- Parameters: %(mstart)s, %(mend)s — ISO-8601 date bounds for msf (inclusive).
-- Depends on: universe_monthly (embedded as the monthly_uni CTE below),
--             write_yeye.bab_beta_stage (populated by main.py before this runs)
-- Settings: join_algorithm=partial_merge, max_execution_time=600,
--           join_use_nulls=1 (so a stock-month with no estimable beta ->
--           NULL beta -> NaN in pandas, rather than 0)
--
-- Timing convention (no look-ahead): the beta in a row for calendar month t
-- is the FP beta estimated using daily data through the LAST trading day of
-- month t-1. main.py assigns each month-end beta estimate to the FOLLOWING
-- month before staging, so the join key (permno, month) lines up correctly.
WITH monthly_uni AS (
    SELECT
        permno,
        month,
        max(ret)    AS ret,
        max(me)     AS me,
        max(log_me) AS log_me
    FROM (
        -- month is first-of-month as Date32, built from the ISO date string.
        -- (toStartOfMonth(toDate(.)) clamps pre-1970 dates to the epoch.)
        SELECT
            m.permno                                  AS permno,
            toDate32(concat(substring(m.date, 1, 7), '-01')) AS month,
            m.ret                                     AS ret,
            abs(m.prc) * m.shrout * 1000 / 1000000    AS me,
            if(abs(m.prc) * m.shrout > 0,
               log(abs(m.prc) * m.shrout / 1000),
               NULL)                                  AS log_me
        FROM crsp_202601.msf AS m
        INNER JOIN crsp_202601.dsenames AS n
            ON m.permno = n.permno
           AND m.date >= n.namedt
           AND m.date <= n.nameendt
        WHERE n.shrcd IN (10, 11)
          AND n.exchcd IN (1, 2, 3)
          AND m.date >= %(mstart)s
          AND m.date <= %(mend)s
          AND m.ret IS NOT NULL
          AND m.ret > -1.0
    )
    GROUP BY permno, month
)
SELECT
    mu.permno   AS permno,
    mu.month    AS month,
    mu.ret      AS ret,
    b.beta      AS beta,
    mu.me       AS me,
    mu.log_me   AS log_me
FROM monthly_uni AS mu
LEFT JOIN write_yeye.bab_beta_stage AS b
    ON mu.permno = b.permno
   AND mu.month  = b.month
ORDER BY mu.permno, mu.month
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         join_use_nulls = 1;
