-- size_quintile.sql
-- Purpose: monthly size-quintile assignment using NYSE-only market-cap
--          breakpoints (Fama-French / Jegadeesh 1990 convention).
-- Tables: crsp_202601.msf, crsp_202601.dsenames
-- Output columns: permno, month, me_month, me, exchcd, size_quintile,
--                 size_quintile_allstock, n_nyse, n_all
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge, max_execution_time=600
--
-- Method
-- ------
--  1. Market equity per (permno, month):  me = abs(prc) * shrout * 1000
--     (CRSP prc in $/share, shrout in thousands of shares -> me in dollars).
--     Universe: PIT shrcd IN (10,11), exchcd IN (1,2,3) via dsenames.
--  2. At each month-end, the NYSE-only (exchcd = 1) 20/40/60/80 percentile
--     breakpoints of me are computed with quantileExact.
--  3. EVERY stock (NYSE/AMEX/NASDAQ) is assigned to a quintile by where its
--     own me falls relative to those NYSE breakpoints:
--       Q1: me <= p20, Q2: p20 < me <= p40, Q3: p40 < me <= p60,
--       Q4: p60 < me <= p80, Q5: me > p80.
--     (Applying NYSE breakpoints to the full cross-section deliberately does
--      NOT give an equal 20/20/20/20/20 split once AMEX (1962+) and NASDAQ
--      (1972+) enter — small non-NYSE stocks pile into Q1. Pre-1962 the CRSP
--      universe is NYSE-only, so the split is exactly 20% each there.)
--  4. Timing.  `me_month` is the calendar month in which market equity is
--     measured (msf.date is the last trading day of that month, i.e. the
--     month END). The paper forms the size groups from "firm size at the end
--     of the PREVIOUS month" (preprocessing rule fm_size_quintile_subsamples,
--     paper L585), so the quintile is stamped onto the FOLLOWING month:
--         month = me_month + 1 month
--     `month` is therefore directly joinable to the panel's month-start key
--     and carries no look-ahead (the month-t return is not used to sort).
--
-- Date handling: all date math is Date32 (CRSP starts 1926; `Date` clamps
-- anything before 1970-01-01). Month-start is computed as
-- `d - (dayOfMonth(d) - 1) days` because toStartOfMonth(Date32) returns Date.

WITH
  -- Step 1: PIT-filtered monthly market equity (dollars).
  me_panel AS (
    SELECT
      m.permno                                                              AS permno,
      toDate32(toDate32OrNull(m.date) - toIntervalDay(dayOfMonth(toDate32OrNull(m.date)) - 1)) AS me_month,
      n.exchcd                                                              AS exchcd,
      abs(m.prc) * m.shrout * 1000.0                                        AS me
    FROM crsp_202601.msf AS m
    INNER JOIN crsp_202601.dsenames AS n
      ON m.permno = n.permno
     AND toDate32OrNull(m.date) >= toDate32OrNull(n.namedt)
     AND toDate32OrNull(m.date) <= toDate32OrNull(n.nameendt)
    WHERE n.shrcd IN (10, 11)
      AND n.exchcd IN (1, 2, 3)
      AND toDate32OrNull(m.date) BETWEEN toDate32('1926-01-01') AND toDate32('1988-12-31')
      AND m.prc IS NOT NULL
      AND m.shrout IS NOT NULL
      AND abs(m.prc) > 0
      AND m.shrout > 0
  ),
  -- Step 2: NYSE-only (exchcd = 1) 20/40/60/80 breakpoints, per month-end.
  nyse_bp AS (
    SELECT
      me_month                       AS bp_month,
      quantileExact(0.2)(me)         AS p20,
      quantileExact(0.4)(me)         AS p40,
      quantileExact(0.6)(me)         AS p60,
      quantileExact(0.8)(me)         AS p80,
      count()                        AS n_nyse
    FROM me_panel
    WHERE exchcd = 1
    GROUP BY bp_month
  ),
  -- Step 2b (DIAGNOSTIC ONLY): all-stock (NYSE+AMEX+NASDAQ) 20/40/60/80
  -- breakpoints, i.e. equal-count quintiles. Emitted as a second column so
  -- the two size-sort conventions can be compared without re-querying.
  all_bp AS (
    SELECT
      me_month                       AS bp_month,
      quantileExact(0.2)(me)         AS a20,
      quantileExact(0.4)(me)         AS a40,
      quantileExact(0.6)(me)         AS a60,
      quantileExact(0.8)(me)         AS a80,
      count()                        AS n_all
    FROM me_panel
    GROUP BY bp_month
  )
-- Step 3 + 4: assign every stock against the NYSE breakpoints, stamp the
-- quintile onto the following calendar month.
SELECT
  p.permno                                     AS permno,
  addMonths(p.me_month, 1)                     AS month,
  p.me_month                                   AS me_month,
  p.me                                         AS me,
  p.exchcd                                     AS exchcd,
  multiIf(
    p.me <= b.p20, 1,
    p.me <= b.p40, 2,
    p.me <= b.p60, 3,
    p.me <= b.p80, 4,
    5
  )                                            AS size_quintile,
  multiIf(
    p.me <= a.a20, 1,
    p.me <= a.a40, 2,
    p.me <= a.a60, 3,
    p.me <= a.a80, 4,
    5
  )                                            AS size_quintile_allstock,
  b.n_nyse                                     AS n_nyse,
  a.n_all                                      AS n_all
FROM me_panel AS p
INNER JOIN nyse_bp AS b
  ON p.me_month = b.bp_month
INNER JOIN all_bp AS a
  ON p.me_month = a.bp_month
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         join_algorithm = 'partial_merge'
