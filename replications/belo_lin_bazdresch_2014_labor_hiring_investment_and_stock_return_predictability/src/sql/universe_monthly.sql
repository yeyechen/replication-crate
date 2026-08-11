-- universe_monthly.sql
-- Purpose: PIT-filtered monthly stock observations (CRSP msf + dsenames).
--          Universe: shrcd IN (10,11), exchcd IN (1,2,3),
--          SIC code NOT in [4900-4999] and NOT in [6000-6999] (Belo et al. 2014 §2.1).
--          Sample window: July 1965 - June 2010.
-- Tables:  crsp_202601.msf, crsp_202601.dsenames
-- Output columns: permno, month (Date32, first-of-month), month_end (Date32, last trading day),
--                 ret, prc, shrout, hexcd, hsiccd, shrcd, exchcd, sic,
--                 me_dollars (= abs(prc) * shrout * 1000), nyse (1 if NYSE, else 0)
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge, max_execution_time=600

WITH
  -- 1. CRSP msf observations in the sample window (row-level, no aggregation).
  --    We alias the parsed date to `mdate` to avoid ClickHouse resolving the
  --    inner WHERE's `toDate32OrNull(date)` against the already-typed alias.
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
        AND ret > -1.0                 -- drop CRSP return sentinels
  ),
  -- 2. CRSP dsenames records overlapping the sample window (filter at SQL level).
  --    Rename aliases to `ndt`/`nendt` to avoid shadowing the raw columns
  --    (ClickHouse resolves the inner WHERE's toDate32OrNull(...) against
  --    the already-typed alias otherwise).
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
  -- Note: `date` is already Date32 in msf_filtered and namedt/nameendt are
  -- already Date32 in names_filtered; downstream CTEs use these directly.
  -- 3. PIT-join msf to dsenames (one row per (permno, date, name_record)).
  --    Apply SIC exclusion at the row level so we never aggregate a dropped row.
  --    NB: `toStartOfMonth(date32)` silently clamps pre-1970 dates to 1970-01-01
  --    (known ClickHouse bug). Use the manual formula instead.
  pit_joined AS (
      SELECT
          m.permno                                                  AS permno,
          m.mdate                                                   AS mdate,
          addDays(m.mdate, -toDayOfMonth(m.mdate) + 1)              AS month,
          m.ret                                                     AS ret,
          m.prc                                                     AS prc,
          m.shrout                                                  AS shrout,
          m.hexcd                                                   AS hexcd,
          m.hsiccd                                                  AS hsiccd,
          n.shrcd                                                   AS shrcd,
          n.exchcd                                                  AS exchcd,
          if(n.siccd IS NOT NULL, n.siccd, m.hsiccd)                AS sic
      FROM msf_filtered AS m
      INNER JOIN names_filtered AS n
          ON m.permno = n.permno
         AND m.mdate >= n.ndt
         AND m.mdate <= n.nendt
      WHERE
          -- SIC exclusions per paper §2.1 (L144): drop 4900-4999 (regulated) and
          -- 6000-6999 (financial). PIT siccd (dsenames) takes precedence over hsiccd.
          NOT (if(n.siccd IS NOT NULL, n.siccd, m.hsiccd) BETWEEN 4900 AND 4999)
          AND NOT (if(n.siccd IS NOT NULL, n.siccd, m.hsiccd) BETWEEN 6000 AND 6999)
          AND abs(m.prc) > 0
          AND m.shrout > 0
  ),
  -- 4. Collapse to one row per (permno, month) using month-end snapshot
  --    (last trading day of the month; msf.date is the month-end trading day).
  monthly AS (
      SELECT
          permno,
          month,
          max(mdate)                                               AS month_end,
          argMax(ret,    mdate)                                    AS ret,
          argMax(prc,    mdate)                                    AS prc,
          argMax(shrout, mdate)                                    AS shrout,
          argMax(hexcd,  mdate)                                    AS hexcd,
          argMax(hsiccd, mdate)                                    AS hsiccd,
          anyHeavy(shrcd)                                          AS shrcd,
          anyHeavy(exchcd)                                         AS exchcd,
          anyHeavy(sic)                                            AS sic
      FROM pit_joined
      GROUP BY permno, month
  )
SELECT
    permno,
    month,
    month_end,
    ret,
    prc,
    shrout,
    hexcd,
    hsiccd,
    shrcd,
    exchcd,
    sic,
    -- Market equity in USD (price * shares-out * 1000 because shrout is in thousands).
    abs(prc) * shrout * 1000.0                                    AS me_dollars,
    -- NYSE-only flag for size-breakpoint computation (micro-cap uses NYSE 20th pct).
    if(exchcd = 1, 1, 0)                                          AS nyse
FROM monthly
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
