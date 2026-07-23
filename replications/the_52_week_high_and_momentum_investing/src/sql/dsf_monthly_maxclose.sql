-- dsf_monthly_maxclose.sql
-- Purpose: Monthly maximum of DAILY |prc| per permno, for the daily-close
--          52-week-high signal variant (wh_sig_dc). This is the more literal
--          reading of George & Hwang (2004) L122: "the highest price achieved
--          during the 12-month period" — i.e. the max over daily closing
--          prices, not just month-end closes. The existing wh_sig_cl uses the
--          max of msf month-end closes; this variant uses the max of dsf daily
--          closes (max_daily_close >= month-end close in every month).
--          Coverage 1957-01 .. 2002-12 (the analysis grid starts 1958-01; the
--          extra 1957 months are dropped when the result is reindexed to the
--          grid in main.py, matching wh_sig_cl's exact window convention).
--          Only filter: prc IS NOT NULL (keep every valid daily close so the
--          monthly max is a true max; no ret filter — the denominator is a
--          price series, not a return series). abs() removes the CRSP
--          negative-quote sign convention.
-- Tables: crsp_202601.dsf (107M rows; GROUP BY is cheap in ClickHouse)
-- Output columns: permno, ym ('YYYY-MM' string), max_daily_close
-- Notes: dsf.date is Nullable(String) in 'YYYY-MM-DD' format, so the month key
--        is substring(date,1,7). The calendar month-end key is derived in
--        main.py (ym + '-01' then MonthEnd(0)), consistent with msf handling.
-- Depends on: (none)
SELECT
    permno,
    substring(date, 1, 7) AS ym,
    max(abs(prc)) AS max_daily_close
FROM crsp_202601.dsf
WHERE date >= '1957-01-01' AND date <= '2002-12-31'
  AND prc IS NOT NULL
GROUP BY permno, substring(date, 1, 7)
SETTINGS
    max_execution_time = 600,
    max_rows_to_read = 10000000000,
    timeout_before_checking_execution_speed = 0
