-- panel.sql
-- Purpose: Final monthly analysis panel. Single SQL query that:
--          1. Builds the PIT-filtered monthly stock universe (CRSP msf + dsenames)
--             with shrcd/exchcd/SIC exclusions.
--          2. Builds the Compustat fiscal-year signals (HN_fy, IK_fy, ROA_fy) with
--             lag of emp/ppent by fyear.
--          3. PIT-links permno to gvkey via ccmxpf_linktable.
--          4. Maps monthly observations to the relevant fiscal-year signals using
--             the FF 1992 convention: HN_fy ending calendar year Y is paired with
--             monthly observations July Y+1 through June Y+2.
--          5. Computes mcap_lag1, size = log(me_dollars_lag1), km = ppent / me_dollars
--             (with ppent * 1e6 unit conversion per COMPUSTAT.md gotcha).
-- Output columns: month, permno, gvkey, ret, me_dollars, mcap_lag1,
--                 hn, ik, roa, km, size, sic
-- Tables:  crsp_202601.msf, crsp_202601.dsenames, crsp_202601.ccmxpf_linktable,
--          comp_202601.funda
-- Depends on: (none — this is the final assembly)
-- Settings: join_algorithm=partial_merge, max_execution_time=900

WITH
  -- ===== Step 1: Monthly stock universe =====
  --    We alias the parsed dates to `mdate`/`ndt`/`nendt` to avoid ClickHouse
  --    resolving the inner WHERE's `toDate32OrNull(...)` against the
  --    already-typed alias.
  msf_filtered AS (
      SELECT permno,
             toDate32OrNull(date) AS mdate,
             ret,
             prc,
             shrout,
             hexcd,
             hsiccd
      FROM crsp_202601.msf
      WHERE toDate32OrNull(date) >= toDate32('1965-07-01')
        AND toDate32OrNull(date) <= toDate32('2010-06-30')
        AND permno IS NOT NULL
        AND ret IS NOT NULL
        AND ret > -1.0
  ),
  names_filtered AS (
      SELECT permno,
             toDate32OrNull(namedt)   AS ndt,
             ifNull(toDate32OrNull(nameendt), toDate32('2099-12-31')) AS nendt,
             shrcd,
             exchcd,
             siccd
      FROM crsp_202601.dsenames
      WHERE shrcd  IN (10, 11)
        AND exchcd IN (1, 2, 3)
        AND toDate32OrNull(namedt) <= toDate32('2010-06-30')
        AND (toDate32OrNull(nameendt) >= toDate32('1965-07-01') OR nameendt IS NULL)
  ),
  universe_pit AS (
      SELECT
          m.permno                       AS permno,
          m.mdate                        AS mdate,
          -- Manual start-of-month: `toStartOfMonth(date32)` clamps pre-1970
          -- dates to 1970-01-01 (ClickHouse bug).
          addDays(m.mdate, -toDayOfMonth(m.mdate) + 1)  AS month,
          m.ret                          AS ret,
          m.prc                          AS prc,
          m.shrout                       AS shrout,
          m.hexcd                        AS hexcd,
          m.hsiccd                       AS hsiccd,
          n.shrcd                        AS shrcd,
          n.exchcd                       AS exchcd,
          if(n.siccd IS NOT NULL, n.siccd, m.hsiccd) AS sic
      FROM msf_filtered AS m
      INNER JOIN names_filtered AS n
          ON m.permno = n.permno
         AND m.mdate >= n.ndt
         AND m.mdate <= n.nendt
      WHERE
          NOT (if(n.siccd IS NOT NULL, n.siccd, m.hsiccd) BETWEEN 4900 AND 4999)
          AND NOT (if(n.siccd IS NOT NULL, n.siccd, m.hsiccd) BETWEEN 6000 AND 6999)
          AND abs(m.prc) > 0
          AND m.shrout > 0
  ),
  universe AS (
      SELECT
          permno,
          month,
          max(mdate)                     AS month_end,
          argMax(ret,    mdate)          AS ret,
          argMax(prc,    mdate)          AS prc,
          argMax(shrout, mdate)          AS shrout,
          argMax(hexcd,  mdate)          AS hexcd,
          argMax(hsiccd, mdate)          AS hsiccd,
          anyHeavy(shrcd)                AS shrcd,
          anyHeavy(exchcd)               AS exchcd,
          anyHeavy(sic)                  AS sic
      FROM universe_pit
      GROUP BY permno, month
  ),
  universe_with_me AS (
      SELECT
          *,
          abs(prc) * shrout * 1000.0     AS me_dollars,
          if(exchcd = 1, 1, 0)           AS nyse
      FROM universe
  ),
  -- ===== Step 2: Compustat annual fundamentals with signals =====
  comp_raw AS (
      SELECT gvkey,
             fyear,
             toDate32OrNull(datadate)   AS ddate,
             sich,
             emp,
             capx,
             ifNull(sppe, 0.0)          AS sppe,
             ppent,
             ni,
             at
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
  comp_lagged AS (
      SELECT
          gvkey, fyear, ddate AS datadate, sich, emp, capx, sppe, ppent, ni, at,
          lagInFrame(emp,   1) OVER w AS emp_lag1,
          lagInFrame(ppent, 1) OVER w AS ppent_lag1
      FROM comp_raw
      WINDOW w AS (PARTITION BY gvkey ORDER BY fyear
                   ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  ),
  comp_signals AS (
      SELECT
          gvkey, fyear, datadate, sich, emp, capx, sppe, ppent, ni, at,
          if(emp IS NOT NULL AND emp_lag1 IS NOT NULL AND (emp + emp_lag1) != 0,
             (emp - emp_lag1) / (0.5 * (emp + emp_lag1)), NULL) AS hn_fy,
          if(ppent IS NOT NULL AND ppent_lag1 IS NOT NULL AND capx IS NOT NULL
             AND (ppent + ppent_lag1) != 0,
             (capx - sppe) / (0.5 * (ppent + ppent_lag1)), NULL) AS ik_fy,
          if(ni IS NOT NULL AND at IS NOT NULL AND at != 0,
             ni / at, NULL) AS roa_fy
      FROM comp_lagged
  ),
  -- ===== Step 3: PIT permno -> gvkey link =====
  --    lpermno is already Float64 in the table; use toInt32() (not toInt32OrNull,
  --    which requires String input).
  link AS (
      SELECT
          toInt32(lpermno)       AS permno_i32,
          gvkey,
          toDate32OrNull(linkdt)    AS linkdt,
          ifNull(toDate32OrNull(linkenddt), toDate32('2099-12-31')) AS linkenddt
      FROM crsp_202601.ccmxpf_linktable
      WHERE linktype IN ('LC', 'LU')
        AND usedflag = 1
        AND linkprim IN ('P', 'C')
        AND lpermno IS NOT NULL
        AND gvkey   IS NOT NULL
  ),
  -- ===== Step 4: Universe + link + Compustat signals =====
  joined AS (
      SELECT
          u.month         AS month,
          u.permno        AS permno,
          u.month_end     AS month_end,
          u.ret           AS ret,
          u.me_dollars    AS me_dollars,
          u.nyse          AS nyse,
          u.sic           AS sic,
          l.gvkey         AS gvkey,
          c.sich          AS sich_fy,
          c.ppent         AS ppent,
          c.emp           AS emp,
          c.capx          AS capx,
          c.sppe          AS sppe,
          c.ni            AS ni,
          c.at            AS at,
          c.hn_fy         AS hn_fy,
          c.ik_fy         AS ik_fy,
          c.roa_fy        AS roa_fy,
          c.fyear         AS fyear,
          if(toMonth(u.month) >= 7, toYear(u.month) - 1, toYear(u.month) - 2) AS formation_fyear
      FROM universe_with_me AS u
      INNER JOIN link AS l
          ON u.permno    = l.permno_i32
         AND u.month_end >= l.linkdt
         AND u.month_end <= l.linkenddt
      LEFT JOIN comp_signals AS c
          ON l.gvkey = c.gvkey
         AND c.fyear = if(toMonth(u.month) >= 7, toYear(u.month) - 1, toYear(u.month) - 2)
  ),
  -- ===== Step 5: Lag-one-month market equity and size =====
  with_lags AS (
      SELECT
          month,
          permno,
          gvkey,
          month_end,
          ret,
          me_dollars,
          lagInFrame(me_dollars, 1) OVER w    AS mcap_lag1,
          hn_fy                               AS hn,
          ik_fy                               AS ik,
          roa_fy                              AS roa,
          -- KM = ppent / me_dollars.
          -- ppent is in MILLIONS of USD; me_dollars is in USD. Multiply by 1e6
          -- to get a dimensionless ratio (per COMPUSTAT.md gotcha).
          if(ppent IS NOT NULL AND me_dollars > 0,
             ppent * 1e6 / me_dollars, NULL)  AS km,
          -- size = log(me_dollars) at sort date (lag 1 month).
          ln(nullIf(lagInFrame(me_dollars, 1) OVER w, 0)) AS size,
          sic,
          sich_fy,
          fyear,
          formation_fyear,
          nyse
      FROM joined
      WINDOW w AS (PARTITION BY permno ORDER BY month
                   ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  )
SELECT
    month,
    permno,
    gvkey,
    ret,
    me_dollars,
    mcap_lag1,
    hn,
    ik,
    roa,
    km,
    size,
    sic,
    fyear,
    formation_fyear
FROM with_lags
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 900,
         max_rows_to_read = 20000000000,
         timeout_before_checking_execution_speed = 0
