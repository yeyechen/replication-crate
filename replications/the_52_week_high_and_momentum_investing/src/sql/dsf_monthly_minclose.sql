-- dsf_monthly_minclose.sql
-- Purpose: Monthly MINIMUM of DAILY |prc| per permno, for the 52-week-LOW
--          signal (wh_lo_sig; audit1.md [M4] prep, George & Hwang 2004
--          Table IX): the paper's 52-low measure = P_{t-j} / min price over
--          the trailing 12 months (inputs/content.md L2460-2464).
--          min_daily_close(m) = min of dsf daily |prc| in calendar month m;
--          the rolling 12-month MIN over f-11..f is taken in main.py, so
--          wh_lo_sig(f) = |prc(f)| / min(min_daily_close over f-11..f) >= 1
--          (the month-end close is one of month f's own daily closes, so the
--          window min <= |prc(f)|). Mirror image of dsf_monthly_maxclose.sql
--          (min instead of max), same coverage and conventions.
--          Coverage 1957-01 .. 2002-12 (the analysis grid starts 1958-01; the
--          extra 1957 months are dropped when the result is reindexed to the
--          grid in main.py, matching dsf_monthly_maxclose.sql exactly).
--          Only filter: prc IS NOT NULL (keep every valid daily close so the
--          monthly min is a true min; abs() removes the CRSP negative-quote
--          sign convention).
-- Tables: crsp_202601.dsf (57.7M rows with prc IS NOT NULL in window; GROUP BY
--         is cheap in ClickHouse)
-- Output columns: permno, ym ('YYYY-MM' string), min_daily_close
-- Notes: dsf.date is Nullable(String) in 'YYYY-MM-DD' format, so the month key
--        is substring(date,1,7). The ClickHouse Date type cannot hold
--        pre-1970 dates — keep string month keys; the calendar month-end key
--        is derived in main.py (ym + '-01' then MonthEnd(0)), exactly like
--        the maxclose query.
-- Depends on: (none)
SELECT
    permno,
    substring(date, 1, 7) AS ym,
    min(abs(prc)) AS min_daily_close
FROM crsp_202601.dsf
WHERE date >= '1957-01-01' AND date <= '2002-12-31'
  AND prc IS NOT NULL
GROUP BY permno, substring(date, 1, 7)
SETTINGS
    max_execution_time = 600,
    max_rows_to_read = 10000000000,
    timeout_before_checking_execution_speed = 0
