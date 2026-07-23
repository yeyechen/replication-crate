-- divyld_annual.sql
-- Purpose: Annual cash-dividend sum per (permno, year) for DIVYLD in
--          Amihud (2002). DIVYLD_iY = 100 * div_sum / |prc| at end of
--          year Y is completed in main.py using price_end from
--          characteristics_annual.sql (non-payers -> div_sum NULL ->
--          DIVYLD = 0).
-- Rules (Assumption 6, preprocessing_rules var_divyld):
--   - ordinary cash dividends only: distcd BETWEEN 1000 AND 1999
--   - attribution date = paydt, falling back to exdt when paydt is
--     NULL or empty (CRSP stores some dates as '' rather than NULL)
--   - per-share amounts from divamt (NULLs dropped)
-- Tables: crsp_202601.dsedist
-- Output columns: permno, y, div_sum  (div_sum in $/share)
-- Depends on: (none)
WITH attributed AS (
    SELECT
        permno,
        multiIf(
            paydt IS NOT NULL AND paydt != '', paydt,
            exdt  IS NOT NULL AND exdt  != '', exdt,
            ''
        ) AS attr_dt,
        divamt
    FROM crsp_202601.dsedist
    WHERE distcd BETWEEN 1000 AND 1999
      AND divamt IS NOT NULL
)
SELECT
    permno,
    toYear(toDate32(attr_dt)) AS y,
    sum(divamt)               AS div_sum
FROM attributed
WHERE attr_dt >= '1963-01-01' AND attr_dt <= '1996-12-31'
GROUP BY permno, y
ORDER BY permno, y
SETTINGS max_execution_time = 300
