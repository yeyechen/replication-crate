-- crsp_monthly_returns.sql
-- Purpose: Pull monthly CRSP returns (with delisting-return fallback)
--          for the panel's permnos for the BHAR window of each
--          portfolio-formation year (year_t in 1976-1993).
--          The window is July year_t to June year_t+3 (= 36 months
--          max), so we need msf returns from 1976-07-01 to 1996-12-31.
--
-- Returns one row per (permno, year_t, month_offset) where
-- month_offset = 1..36 corresponds to the 36 months of the BHAR
-- window. The agent joins this back to the panel and computes
-- Ret12, Ret24, Ret36 in Python via cumulative product of (1+ret).
--
-- Output columns: permno, year_t, month_offset (1..36), ret
-- Tables: crsp_202601.msf, crsp_202601.msedelist
-- Depends on: data/panel.parquet
-- Settings: join_algorithm=partial_merge, max_execution_time=600

WITH
  -------------------------------------------------------------------
  -- 1. Panel keys (permno, year_t) — read directly from the panel
  --    parquet via the ClickHouse file() table function.
  -------------------------------------------------------------------
  panel_keys AS (
      SELECT permno, year_t
      FROM file('${PANEL_PATH}', 'Parquet', 'permno UInt32, year_t UInt16')
  ),

  -------------------------------------------------------------------
  -- 2. Monthly returns from CRSP msf for the BHAR window of each
  --    panel year. 1976-1993 portfolio formation -> window spans
  --    July 1976 to June 1996 (covers Ret36 for the latest cohort).
  -------------------------------------------------------------------
  monthly AS (
      SELECT m.permno                       AS permno,
             toYear(toDate32OrNull(m.date))  AS yr,
             toMonth(toDate32OrNull(m.date)) AS mo,
             m.ret                           AS ret
      FROM crsp_202601.msf AS m
      INNER JOIN (
          SELECT DISTINCT permno FROM panel_keys
      ) AS p
          ON m.permno = p.permno
      WHERE m.date BETWEEN '1976-07-01' AND '1996-12-31'
        AND m.ret IS NOT NULL
  ),

  -------------------------------------------------------------------
  -- 3. Delisting returns from msedelist — one record per delisted
  --    permno. Convert dlstdt to (yr, mo) for window matching.
  -------------------------------------------------------------------
  delist AS (
      SELECT permno,
             toYear(toDate32OrNull(dlstdt))  AS dl_yr,
             toMonth(toDate32OrNull(dlstdt)) AS dl_mo,
             dlret
      FROM crsp_202601.msedelist
      WHERE dlret IS NOT NULL
  ),

  -------------------------------------------------------------------
  -- 4. Window months: for each panel (permno, year_t), generate
  --    month_offset=1..36 where offset k maps to (yr_k, mo_k):
  --      offset 1 -> July year_t
  --      offset 13 -> July year_t+1
  --      offset 25 -> July year_t+2
  --      offset 36 -> June year_t+3
  -------------------------------------------------------------------
  offsets AS (
      SELECT arrayJoin(arrayMap(i -> i + 1, range(36))) AS month_offset
  ),
  window_months AS (
      SELECT pk.permno AS permno,
             pk.year_t AS year_t,
             o.month_offset AS month_offset,
             -- Compute (yr, mo) for each offset. offsets 1-6 -> July-Dec of year_t;
             -- offsets 7-12 -> Jan-June of year_t+1; etc.
             pk.year_t + intDiv(o.month_offset - 1, 12) +
                 if((o.month_offset - 1) % 12 >= 6, 1, 0) AS yr,
             ((o.month_offset - 1) % 12 + 7 - 1) % 12 + 1 AS mo
      FROM panel_keys AS pk
      CROSS JOIN offsets AS o
  ),

  -------------------------------------------------------------------
  -- 5. Build the final (permno, year_t, month_offset, ret) table.
  --    The ret comes from msf; missing ret falls back to dlret from
  --    the delisting record (one per permno).
  -------------------------------------------------------------------
  window_returns AS (
      SELECT w.permno                         AS permno,
             w.year_t                         AS year_t,
             w.month_offset                   AS month_offset,
             if(m.ret IS NOT NULL, m.ret,
                if(d.dlret IS NOT NULL, d.dlret, NULL)
             )                                AS ret
      FROM window_months AS w
      LEFT JOIN monthly AS m
          ON w.permno = m.permno
         AND w.yr     = m.yr
         AND w.mo     = m.mo
      LEFT JOIN delist AS d
          ON w.permno = d.permno
         AND w.yr     = d.dl_yr
         AND w.mo     = d.dl_mo
  )

SELECT permno, year_t, month_offset, ret
FROM window_returns
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
