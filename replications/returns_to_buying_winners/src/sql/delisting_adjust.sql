-- delisting_adjust.sql
-- Purpose: delisting events within the paper's data vintage (1926-07-01 ..
--          1989-12-31; extended back from 1962-07-01 in outer iteration 2,
--          audit-1 M1 — the Table VIII back-test panel) used for the
--          delisting-return adjustment of monthly
--          returns. dlret carries CRSP missing sentinels (-44/-55/-66/-77/
--          -88/-99) as non-NULL negative floats; any dlret < -1.0 is a
--          sentinel and is mapped to NULL (dlret_clean). Valid dlret lives
--          in [-1, +inf): dlret = -1.0 means a worthless security.
--          dlst_month ('YYYY-MM' of dlstdt) joins the event to the monthly
--          panel row of the delisting month.
--          Adjustment applied in monthly_panel.sql:
--            adj = coalesce(dlret_clean, -0.30 if dlstcd >= 500 else 0)
--            ret = (1 + daily-compounded month return) * (1 + adj) - 1
--          -0.30 is the Shumway (1997) NYSE/AMEX imputation for missing
--          performance-related delisting returns (no NASDAQ in this universe).
--          Empirically verified on this vintage: dsf.ret on the final trading
--          day does NOT embed dlret — for month-end delistings msf.ret equals
--          the raw daily compound (|M - D| < 2e-6) and differs from
--          (1+D)(1+dlret)-1 by the full dlret, so multiplying by (1+dlret)
--          after compounding does not double count.
-- Tables: crsp_202601.dsedelist
-- Output columns: permno, dlstdt, dlstcd, dlret_raw, dlret_clean, dlst_month
-- Depends on: (none)
-- NOTE: no duplicates — verified 7,945 events = 7,945 distinct permnos in
--       this date range.
SELECT
    permno,
    dlstdt,
    dlstcd,
    dlret AS dlret_raw,
    if(dlret IS NOT NULL AND dlret >= -1.0, dlret, NULL) AS dlret_clean,
    substring(dlstdt, 1, 7) AS dlst_month
FROM crsp_202601.dsedelist
WHERE dlstdt >= '1926-07-01' AND dlstdt <= '1989-12-31'
  AND permno IS NOT NULL
  AND dlstdt IS NOT NULL
  AND dlstcd IS NOT NULL
SETTINGS
    max_execution_time = 300,
    max_rows_to_read = 1000000,
    timeout_before_checking_execution_speed = 0;
