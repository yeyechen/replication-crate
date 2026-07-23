-- universe_daily.sql
-- Purpose: point-in-time (PIT) filtered daily returns for the Jegadeesh-Titman
--          (1993) universe: NYSE + AMEX common stocks over the paper's CRSP
--          daily vintage 1926-07-01 .. 1989-12-31. The daily window was
--          extended back from 1962-07-01 in outer iteration 2 (audit-1 M1) so
--          6-month formations start at 1927-01 (Table VIII back-test, §VII);
--          the 1962-07..1989-12 region is unaffected by the extension (daily
--          rows, day_rank, and monthly aggregates there depend only on days
--          within each month). Pre-1962 PIT behavior verified sound (P21):
--          97-98% of dsf stocks match a shrcd/exchcd dsenames window every
--          year 1926-1961 (same rate as 1962-64); universe counts 528/mo
--          (1926) -> ~770 (1940) -> ~1,120 (mid-1962). A stock-day is in universe
--          iff the date falls inside a dsenames validity window
--          (namedt .. coalesce(nameendt, '2100-01-01')) with
--          shrcd IN (10, 11) and exchcd IN (1, 2) — applied at the DAILY level
--          before compounding, as the paper universe is point-in-time.
--          Missing-return sentinels (CRSP -55/-66/-77/-88/-99 appear as
--          non-NULL floats < -1) are dropped: ret IS NOT NULL AND ret > -1.0.
--          day_rank = 1-based trading-day index within (permno, month) over
--          valid-return days; used for the Panel B skip-week partial-month
--          return ret_skip5 (skip the first 5 trading days).
-- Tables: crsp_202601.dsf, crsp_202601.dsenames
-- Output columns: permno, date, month, ret, prc, shrout, day_rank
-- Depends on: (none)
-- NOTE: month is a 'YYYY-MM' string. Do NOT use toDate()/toStartOfMonth() on
--       pre-1970 dates — ClickHouse Date saturates to 1970-01-01 (verified:
--       toDate('1965-06-15') -> 1970-01-01, and toStartOfMonth(toDate32(...))
--       returns Date and saturates too).
-- NOTE: GROUP BY (permno, date) collapses any duplicate dsenames-window
--       matches (verified 1:1 for this period; max() is a safety net only).
-- NOTE: this query is embedded as the `universe_daily` CTE of
--       monthly_panel.sql by src/main.py (the trailing settings clause is
--       stripped at embed time).
SELECT
    permno,
    date,
    month,
    ret,
    prc,
    shrout,
    row_number() OVER (PARTITION BY permno, month ORDER BY date) AS day_rank
FROM
(
    SELECT
        d.permno AS permno,
        d.date AS date,
        substring(d.date, 1, 7) AS month,
        max(d.ret) AS ret,
        max(d.prc) AS prc,
        max(d.shrout) AS shrout
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsenames AS n
        ON d.permno = n.permno
       AND d.date >= n.namedt
       AND d.date <= coalesce(n.nameendt, '2100-01-01')
    WHERE d.date >= '1926-07-01' AND d.date <= '1989-12-31'
      AND d.permno IS NOT NULL
      AND n.shrcd IN (10, 11)
      AND n.exchcd IN (1, 2)
      AND d.ret IS NOT NULL AND d.ret > -1.0
    GROUP BY d.permno, d.date
)
SETTINGS
    join_algorithm = 'hash',
    max_execution_time = 1800,
    max_rows_to_read = 20000000000,
    timeout_before_checking_execution_speed = 0;
