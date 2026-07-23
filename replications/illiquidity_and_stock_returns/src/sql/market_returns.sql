-- market_returns.sql
-- Purpose: Monthly equally-weighted market returns, 1963-01 .. 1997-12
--          (Amihud 2002 §3.1/§3.3; Assumption 4).
--   rm_ew_nyse: computed from dsf daily — EW cross-section each day
--          (mean of daily ret across all NYSE common stocks with a
--          valid return that day), then daily portfolio returns
--          compounded within each month: prod(1 + RM_t) - 1.
--   rm_ew_crsp: CRSP's published monthly EW index return
--          (crsp_202601.msi.ewretd, NYSE+AMEX blend), decimal.
-- Universe for rm_ew_nyse: shrcd IN (10,11), exchcd = 1, PIT via dsfhdr;
--          valid return: ret non-null AND ret > -1.
-- Tables: crsp_202601.dsf, crsp_202601.dsfhdr, crsp_202601.msi
-- Output columns: month (Date32 first-of-month), rm_ew_nyse, rm_ew_crsp
-- Depends on: (none)
-- Note: toDate32 everywhere (Date saturates pre-1970).
WITH univ AS (
    SELECT
        toDate32(d.date) AS date32,
        d.ret            AS ret
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsfhdr AS h
        ON d.permno = h.permno
    WHERE h.hshrcd IN (10, 11)
      AND h.hexcd = 1
      AND d.date >= '1963-01-01' AND d.date <= '1997-12-31'
      AND toDate32(d.date) >= toDate32(h.begdat)
      AND toDate32(d.date) <= toDate32(h.enddat)
      AND d.ret IS NOT NULL AND d.ret > -1
),
day_ew AS (
    SELECT date32, avg(ret) AS rm
    FROM univ
    GROUP BY date32
),
mon AS (
    SELECT
        -- month built from string parts: toStartOfMonth() returns Date,
        -- which saturates pre-1970 dates to 1970-01-01
        toDate32(concat(toString(toYear(date32)), '-',
                 leftPad(toString(toMonth(date32)), 2, '0'),
                 '-01'))              AS month,
        exp(sum(log(1 + rm))) - 1     AS rm_ew_nyse
    FROM day_ew
    GROUP BY month
),
msi AS (
    -- align to first-of-month keys (msi.date is end-of-month)
    SELECT toDate32(concat(toString(toYear(toDate32(date))), '-',
                    leftPad(toString(toMonth(toDate32(date))), 2, '0'),
                    '-01')) AS month,
           ewretd           AS rm_ew_crsp
    FROM crsp_202601.msi
    WHERE date >= '1963-01-01' AND date <= '1997-12-31'
)
SELECT
    m.month        AS month,
    m.rm_ew_nyse   AS rm_ew_nyse,
    i.rm_ew_crsp   AS rm_ew_crsp
FROM mon AS m
LEFT JOIN msi AS i ON m.month = i.month
ORDER BY m.month
SETTINGS max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
