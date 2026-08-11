-- comp_lag_t1_sales_history.sql
-- Purpose: For each (gvkey, fyear) in our panel, pull comp_202601.funda
--          rows for fyear = year_t+1 (to compute actual ROE_{t+2})
--          and fyear in [year_t-6, year_t-1] (sale for SG).
--
-- The panel key is (permno, year_t). Each row of the panel corresponds
-- to a (gvkey, fyear=year_t-1) comp pair. To compute actual ROE at
-- horizon t+2, we need IB and ceq at fyear=year_t+1 (the realized
-- earnings reported for fiscal year ending in calendar year year_t+1).
--
-- For SG = 5-year sales growth from year_t-6 to year_t-1, we need
-- sale at fyear=year_t-6 (start) and fyear=year_t-1 (end).
--
-- Output columns:
--   gvkey (String), year_t (UInt16), ib_t2 ($M), ceq_t1 ($M),
--   ceq_t2 ($M), sale_tminus6 ($M), sale_tminus1 ($M)
--
-- Tables: comp_202601.funda
-- Depends on: (none; uses panel's (permno, year_t) -> (gvkey, fyear)
--              mapping passed via the panel itself)
-- Settings: max_execution_time=600

WITH
  -- Pull comp_202601.funda rows for the year range needed to cover
  -- all panel rows. Panel year_t is 1976..1993, so we need:
  --   fyear in [year_t-6, year_t+1] = [1970, 1994].
  comp_subset AS (
      SELECT
          CAST(gvkey, 'String')       AS gvkey,
          CAST(fyear, 'UInt16')       AS fyear,
          sale                         AS sale,
          ib                           AS ib,
          ceq                          AS ceq
      FROM comp_202601.funda
      WHERE fyear BETWEEN 1970 AND 1994
        AND indfmt = 'INDL'
        AND consol = 'C'
        AND popsrc = 'D'
        AND datafmt = 'STD'
        AND gvkey IS NOT NULL
  )

-- Output: for each (gvkey, year_t), gather the comp fields needed.
-- Since the panel only stores (gvkey, fyear=year_t-1), we join the
-- comp rows at year_t-6, year_t-1, year_t, year_t+1 relative to
-- year_t.
SELECT
    gvkey,
    toUInt16(fyear + 1)              AS year_t,
    argMaxIf(ib,  fyear, fyear = fyear + 0)    AS ib_at_fyear,   -- not used
    argMaxIf(ceq, fyear, fyear = fyear + 0)    AS ceq_at_fyear,  -- not used
    argMaxIf(sale, fyear, fyear = fyear + 0)   AS sale_at_fyear, -- not used
    -- Realized earnings for fiscal year ending in calendar year (year_t + 1):
    argMaxIf(ib,  fyear, fyear = toUInt16(year_t + 0)) AS ib_t1,   -- IB at fyear=year_t (not used)
    argMaxIf(ib,  fyear, fyear = toUInt16(year_t + 1)) AS ib_t2,   -- IB at fyear=year_t+1
    argMaxIf(ceq, fyear, fyear = toUInt16(year_t + 0)) AS ceq_t1,  -- ceq at fyear=year_t (B_{t+1})
    argMaxIf(ceq, fyear, fyear = toUInt16(year_t + 1)) AS ceq_t2,  -- ceq at fyear=year_t+1 (B_{t+2})
    argMaxIf(sale, fyear, fyear = toUInt16(year_t - 6)) AS sale_tminus6,
    argMaxIf(sale, fyear, fyear = toUInt16(year_t - 1)) AS sale_tminus1
FROM comp_subset
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0