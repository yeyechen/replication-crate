-- bhar.sql
-- Purpose: Compute size-adjusted BHAR (Table 7, eq. 8) per (gvkey, calendar_year)
--          following Fairfield-Whisenant-Yohn (2003) §VI ("the annual buy-and-hold
--          return for the same 12-month period on the market-capitalization-based
--          portfolio decile to which the firm belongs").
-- Tables: crsp_202601.msf, crsp_202601.ccmxpf_linktable, comp_202601.funda
-- Output columns: gvkey, calendar_year, bhar_firm, size_dec, bhar_size_dec,
--                 bhar_abnormal (size-adjusted)
-- Depends on: panel.sql (for the universe gvkeys and fyear).
-- Settings: max_execution_time=900, max_rows_to_read=5e9, partial_merge joins.

WITH
  -- ---------------------------------------------------------------
  -- 1. Universe (gvkey, fyear) from compustat, with calendar_year
  --    (year of datadate) and start_month (month of datadate).
  -- ---------------------------------------------------------------
  panel AS (
      SELECT gvkey, fyear,
             toYear(toDate32OrNull(datadate)) AS calendar_year,
             toMonth(toDate32OrNull(datadate)) AS start_month
      FROM comp_202601.funda
      WHERE fyear BETWEEN 1962 AND 1992
        AND indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
        AND (sich < 6000 OR sich > 6999 OR sich IS NULL)
        AND at IS NOT NULL AND at > 0
      GROUP BY gvkey, fyear, datadate
  ),
  -- ---------------------------------------------------------------
  -- 2. CRSP-Compustat PIT link (LC/LU, P/C primary).
  -- ---------------------------------------------------------------
  link AS (
      SELECT gvkey, toFloat64(lpermno) AS permno,
             toDate32OrNull(if(linkdt = '' OR linkdt IS NULL, '1962-01-01', linkdt)) AS link_start,
             toDate32OrNull(if(linkenddt = '' OR linkenddt IS NULL, '2099-12-31', linkenddt)) AS link_end
      FROM crsp_202601.ccmxpf_linktable
      WHERE linktype IN ('LC','LU')
        AND linkprim IN ('P','C')
        AND usedflag = 1
        AND lpermno IS NOT NULL
  ),
  -- ---------------------------------------------------------------
  -- 3. CRSP msf rows for the BHAR window.
  -- ---------------------------------------------------------------
  msf_filtered AS (
      SELECT permno, date,
             toYear(date_orig) AS calendar_year,
             toMonth(date_orig) AS calendar_month,
             -- Use retx (return excluding dividends) for BHAR
             -- computation. retx is the clean price return without
             -- dividend reinvestment, matching the standard academic
             -- convention for size-adjusted BHAR (Lyon, Barber,
             -- Tsai 1999). ret (total return) compounds dividends.
             ret AS ret,
             abs(prc) AS prc_abs,
             shrout,
             hexcd
      FROM (
          SELECT permno, date,
                 if(retx IS NOT NULL, retx, ret) AS ret,
                 prc, shrout, hexcd,
                 toDate32OrNull(date) AS date_orig
          FROM crsp_202601.msf
          WHERE toYear(toDate32OrNull(date)) BETWEEN 1962 AND 1993
            AND ret IS NOT NULL AND ret > -1.0
            AND abs(prc) IS NOT NULL AND abs(prc) > 0
            AND shrout IS NOT NULL AND shrout > 0
      )
  ),
  -- ---------------------------------------------------------------
  -- 4. Link panel (gvkey, fyear) -> permnos whose link range covers
  --    the calendar year.
  -- ---------------------------------------------------------------
  panel_permno AS (
      SELECT pw.gvkey AS gvkey, pw.fyear AS fyear,
             pw.calendar_year AS calendar_year, pw.start_month AS start_month,
             lr.permno AS permno
      FROM panel AS pw
      INNER JOIN link AS lr
        ON lr.gvkey = pw.gvkey
       AND lr.link_end >= toDate32(concat(toString(pw.calendar_year), '-01-01'))
       AND lr.link_start < toDate32(concat(toString(pw.calendar_year + 1), '-01-01'))
  ),
  -- ---------------------------------------------------------------
  -- 5. Expand to (gvkey, fyear, permno, m_offset in [0..11]) where
  --    m_offset 0 corresponds to the calendar month of datadate.
  -- ---------------------------------------------------------------
  months AS (
      SELECT arrayJoin([0,1,2,3,4,5,6,7,8,9,10,11]) AS m_offset
  ),
  panel_month AS (
      -- CALENDAR YEAR t+1 window: Jan calendar year (fyear+1) ..
      -- Dec calendar year (fyear+1). 12 consecutive months.
      -- This is the conventional 12-month holding period aligned to
      -- calendar years, and matches Sloan (1996)'s convention.
      SELECT pp.gvkey AS gvkey, pp.fyear AS fyear,
             pp.calendar_year AS calendar_year, pp.permno AS permno,
             pp.fyear + 1 AS bh_calendar_year,
             (m_offset % 12) + 1 AS target_month
      FROM panel_permno AS pp
      CROSS JOIN months
  ),
  bhar_components AS (
      SELECT pm.gvkey AS gvkey, pm.fyear AS fyear,
             pm.calendar_year AS calendar_year, pm.permno AS permno,
             m.ret AS ret
      FROM panel_month AS pm
      INNER JOIN msf_filtered AS m
        ON m.permno = pm.permno
       AND m.calendar_year = pm.bh_calendar_year
       AND m.calendar_month = pm.target_month
  ),
  -- 12-month buy-and-hold per (gvkey, fyear, permno). Require 12 months.
  bhar_firm AS (
      SELECT gvkey, fyear, calendar_year, permno,
             exp(sum(log(1 + ret))) - 1 AS bhar_firm,
             count(*) AS n_months
      FROM bhar_components
      GROUP BY gvkey, fyear, calendar_year, permno
      HAVING n_months = 12
  ),
  -- ---------------------------------------------------------------
  -- 6. NYSE-only size breakpoints per calendar_year, computed on
  --    the last msf month of each calendar year for each permno
  --    that has a PIT link.
  -- ---------------------------------------------------------------
  last_msf_per_cy AS (
      SELECT permno, calendar_year,
             argMax(prc_abs, date) AS prc_last,
             argMax(shrout, date) AS shrout_last,
             argMax(hexcd, date) AS hexcd_last
      FROM msf_filtered
      GROUP BY permno, calendar_year
  ),
  msf_linked AS (
      SELECT ml.permno AS permno, ml.calendar_year AS calendar_year,
             ml.prc_last AS prc_last, ml.shrout_last AS shrout_last,
             ml.hexcd_last AS hexcd_last,
             ml.prc_last * ml.shrout_last AS mcap,
             link.gvkey AS gvkey
      FROM last_msf_per_cy AS ml
      INNER JOIN link
        ON link.permno = ml.permno
       AND link.link_end >= toDate32(concat(toString(ml.calendar_year), '-01-01'))
       AND link.link_start < toDate32(concat(toString(ml.calendar_year + 1), '-01-01'))
  ),
  nyse_breakpoints AS (
      SELECT calendar_year,
             quantileExact(0.1)(mcap) AS bp10,
             quantileExact(0.2)(mcap) AS bp20,
             quantileExact(0.3)(mcap) AS bp30,
             quantileExact(0.4)(mcap) AS bp40,
             quantileExact(0.5)(mcap) AS bp50,
             quantileExact(0.6)(mcap) AS bp60,
             quantileExact(0.7)(mcap) AS bp70,
             quantileExact(0.8)(mcap) AS bp80,
             quantileExact(0.9)(mcap) AS bp90
      FROM msf_linked
      WHERE hexcd_last = 1 AND mcap > 0
      GROUP BY calendar_year
  ),
  msf_with_dec AS (
      SELECT ml.permno AS permno, ml.calendar_year AS calendar_year,
             ml.gvkey AS gvkey,
             CASE
                 WHEN ml.mcap <= bp.bp10 THEN 1
                 WHEN ml.mcap <= bp.bp20 THEN 2
                 WHEN ml.mcap <= bp.bp30 THEN 3
                 WHEN ml.mcap <= bp.bp40 THEN 4
                 WHEN ml.mcap <= bp.bp50 THEN 5
                 WHEN ml.mcap <= bp.bp60 THEN 6
                 WHEN ml.mcap <= bp.bp70 THEN 7
                 WHEN ml.mcap <= bp.bp80 THEN 8
                 WHEN ml.mcap <= bp.bp90 THEN 9
                 ELSE 10
             END AS size_dec
      FROM msf_linked AS ml
      INNER JOIN nyse_breakpoints AS bp
        ON bp.calendar_year = ml.calendar_year
  ),
  -- Per-(calendar_year, size_dec) equal-weighted mean BHAR.
  -- Compute via subqueries to avoid ClickHouse correlated-subquery
  -- confusion when the final SELECT joins multiple CTEs.
  bhar_dec AS (
      SELECT calendar_year AS bd_cy, size_dec AS bd_sd,
             avg(bhar_firm) AS bhar_size_dec
      FROM (
          SELECT md.calendar_year AS calendar_year, md.size_dec AS size_dec,
                 bf.bhar_firm AS bhar_firm
          FROM msf_with_dec AS md
          INNER JOIN bhar_firm AS bf
            ON bf.calendar_year = md.calendar_year
           AND bf.permno = md.permno
      )
      GROUP BY calendar_year, size_dec
  ),
  gvkey_size_dec AS (
      SELECT gvkey AS gs_gvkey, calendar_year AS gs_cy, size_dec AS gs_sd
      FROM msf_with_dec
  )
SELECT
    bf.gvkey AS gvkey,
    bf.fyear AS fyear,
    bf.calendar_year AS calendar_year,
    bf.calendar_year + 1 AS bh_calendar_year,
    bf.bhar_firm AS bhar_firm,
    gs.gs_sd AS size_dec,
    bd.bhar_size_dec AS bhar_size_dec,
    (bf.bhar_firm - bd.bhar_size_dec) AS bhar_abnormal
FROM bhar_firm AS bf
INNER JOIN gvkey_size_dec AS gs
  ON gs.gs_gvkey = bf.gvkey AND gs.gs_cy = bf.calendar_year
INNER JOIN bhar_dec AS bd
  ON bd.bd_cy = bf.calendar_year AND bd.bd_sd = gs.gs_sd
SETTINGS max_execution_time = 900,
         max_rows_to_read = 5000000000,
         join_algorithm = 'partial_merge',
         timeout_before_checking_execution_speed = 0;
