-- sample_daily.sql
-- Purpose: CRSP daily returns/prices for the sample firms' linked permnos,
--          1968-01-01 to 1982-12-31 (250+61+60 trading days before the earliest
--          1974Q1 announcements and +60 after the latest 1981Q4 ones). ret > -1
--          sentinel guard and NOT NULL ret applied here (A12); prc/shrout are
--          pulled for the sample firms' own year-start market caps (size-decile
--          assignment, A8). Event alignment and the rdq..rdq+5 day-0 requirement
--          are applied in Python (A7).
-- Tables: crsp_202601.dsf, crsp_202601.ccmxpf_lnkhist
-- Output columns: permno (Int32), date (Date), ret (Float64), prc (Float64),
--                 shrout (Float64)
-- Depends on: earnings.sql ({GVKEY_LIST} = comma-separated quoted gvkeys of the
--             Screen-1 firms, substituted at runtime by main.py)
SELECT
    d.permno AS permno,
    toDate(d.date) AS date,
    d.ret AS ret,
    d.prc AS prc,
    d.shrout AS shrout
FROM crsp_202601.dsf AS d
WHERE d.date BETWEEN '1968-01-01' AND '1982-12-31'
  AND d.ret IS NOT NULL
  AND d.ret > -1.0
  AND d.prc IS NOT NULL AND abs(d.prc) > 0
  AND d.shrout IS NOT NULL AND d.shrout > 0
  AND d.permno IN (
      SELECT DISTINCT toInt32(lpermno)
      FROM crsp_202601.ccmxpf_lnkhist
      WHERE linkprim IN ('P', 'C')
        AND linktype IN ('LU', 'LC')
        AND lpermno IS NOT NULL
        AND gvkey IN ({GVKEY_LIST})
  )
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0;
