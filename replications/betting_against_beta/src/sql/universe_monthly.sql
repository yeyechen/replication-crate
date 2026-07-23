-- universe_monthly.sql
-- Purpose: PIT-filtered MONTHLY returns and market equity for US common
--          stocks. This is the monthly cross-section the estimated betas are
--          merged onto to form the final panel.
-- Tables: crsp_202601.msf, crsp_202601.dsenames
-- Output columns: permno (Int32), month (Date32 = first-of-month), ret (Float64,
--                 decimal monthly return), me (Float64, market equity in
--                 $ MILLIONS), log_me (Float64)
-- Parameters: %(mstart)s, %(mend)s — ISO-8601 date bounds for msf (inclusive).
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge, max_execution_time=600
--
-- CRSP gotchas handled here:
--   * ret sentinels filtered with `ret IS NOT NULL AND ret > -1.0`.
--   * prc is SIGNED (negative for bid/ask averages) -> abs(prc) for ME.
--   * shrout is in THOUSANDS of shares, so:
--         ME ($)        = abs(prc) * shrout * 1000
--         ME ($millions)= abs(prc) * shrout * 1000 / 1000000
--                       = abs(prc) * shrout / 1000
--   * Universe is point-in-time via dsenames (namedt <= date <= nameendt,
--     shrcd IN (10,11), exchcd IN (1,2,3)).
--   * GROUP BY (permno, month) collapses the rare case where one msf stock-day
--     matches more than one dsenames validity window (keeps the panel unique
--     per permno-month; ret/prc/shrout come from msf so are identical across
--     the duplicated joins).
--   * log_me = ln(me) where me > 0, else NULL.
--   * month is first-of-month built as Date32 from the ISO date STRING. We
--     CANNOT use toStartOfMonth(toDate(date)): ClickHouse `Date` clamps any
--     date before 1970-01-01 to the epoch, which would silently corrupt every
--     pre-1970 month (half of this 1926-2012 sample). Date32 holds 1900+.
SELECT
    permno,
    month,
    max(ret)    AS ret,
    max(me)     AS me,
    max(log_me) AS log_me
FROM (
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
SETTINGS join_algorithm = 'partial_merge', max_execution_time = 600;
