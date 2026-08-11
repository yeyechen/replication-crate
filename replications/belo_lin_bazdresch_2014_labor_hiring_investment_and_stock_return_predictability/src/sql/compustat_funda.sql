-- compustat_funda.sql
-- Purpose: Pull Compustat annual fundamentals filtered to industrial-format,
--          consolidated, domestic, STD-format firms with December fiscal year-end,
--          and compute fiscal-year-level hiring/investment/ROA signals.
-- Tables:  comp_202601.funda
-- Filters: indfmt='INDL' AND consol='C' AND popsrc='D' AND datafmt='STD' AND fyr=12
--          AND datadate in [1962-01-01, 2011-12-31] (covers fyear 1963-2009 needed by sample)
-- Output columns: gvkey, fyear, datadate, sich, emp, capx, sppe, ppent, ni, at,
--                 hn_fy, ik_fy, roa_fy
-- Depends on: (none)
-- Settings: max_execution_time=600

WITH
  -- 1. Raw Compustat rows meeting standard WRDS industrial filter and Dec FYE.
  --    Rename the alias to `ddate` to avoid shadowing the raw `datadate` column
  --    (ClickHouse resolves the inner WHERE's toDate32OrNull(...) against the
  --    already-typed alias otherwise).
  raw AS (
      SELECT gvkey,
             toDate32OrNull(datadate)        AS ddate,
             fyear,
             emp,
             capx,
             sppe,
             ppent,
             ni,
             at,
             sich
      FROM comp_202601.funda
      WHERE indfmt = 'INDL'
        AND consol = 'C'
        AND popsrc = 'D'
        AND datafmt = 'STD'
        AND fyr    = 12
        AND toDate32OrNull(datadate) >= toDate32('1962-01-01')
        AND toDate32OrNull(datadate) <= toDate32('2011-12-31')
        AND gvkey IS NOT NULL
  ),
  -- 2. Add lagged fundamentals by (gvkey, fyear - 1).
  --    PARTITION BY gvkey, ORDER BY fyear.
  with_lags AS (
      SELECT
          gvkey,
          fyear,
          ddate AS datadate,
          sich,
          emp,
          capx,
          ifNull(sppe, 0.0)                              AS sppe,
          ppent,
          ni,
          at,
          -- Lagged fundamentals (null when previous fiscal year missing).
          lagInFrame(emp,   1) OVER w                    AS emp_lag1,
          lagInFrame(ppent, 1) OVER w                    AS ppent_lag1
      FROM raw
      WINDOW w AS (PARTITION BY gvkey
                   ORDER BY fyear
                   ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  )
SELECT
    gvkey,
    fyear,
    datadate,
    sich                                                 AS sich,
    emp,
    capx,
    sppe,
    ppent,
    ni,
    at,
    -- Hiring rate (Belo et al. 2014 §2.1 L156):
    --   HN_fy = (emp - emp_lag1) / (0.5 * (emp + emp_lag1))
    -- Symmetric around 0, bounded ±200%. NULL if any input missing.
    if(emp IS NOT NULL AND emp_lag1 IS NOT NULL AND (emp + emp_lag1) != 0,
       (emp - emp_lag1) / (0.5 * (emp + emp_lag1)),
       NULL)                                            AS hn_fy,
    -- Investment rate (Belo et al. 2014 §2.1 L156):
    --   IK_fy = (capx - sppe) / (0.5 * (ppent + ppent_lag1))
    -- sppe NULL is treated as 0 (paper §2.1: "Missing values of SPPE are set to zero").
    if(ppent IS NOT NULL AND ppent_lag1 IS NOT NULL AND capx IS NOT NULL
       AND (ppent + ppent_lag1) != 0,
       (capx - sppe) / (0.5 * (ppent + ppent_lag1)),
       NULL)                                            AS ik_fy,
    -- Return-on-assets (Belo et al. 2014 §2.1 L160):
    --   ROA = ni / at
    if(ni IS NOT NULL AND at IS NOT NULL AND at != 0,
       ni / at,
       NULL)                                            AS roa_fy
FROM with_lags
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
