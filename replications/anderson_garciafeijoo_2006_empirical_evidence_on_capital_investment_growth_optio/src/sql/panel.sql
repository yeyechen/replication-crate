-- panel.sql
-- Purpose: Build the analysis-ready monthly panel for the Anderson &
--          Garcia-Feijoo (2006) "Empirical Evidence on Capital
--          Investment, Growth Options, and Security Returns" replication.
-- Tables:  crsp_202601.msf (monthly returns),
--          crsp_202601.dsenames (PIT shrcd/exchcd/siccd),
--          crsp_202601.ccmxpf_linktable (CRSP-Compustat link),
--          comp_202601.funda (annual fundamentals, capx)
-- Output columns: permno, month, gvkey, ret, me_dollars, me_lag,
--                 n_prior_ret, year0, inv_growth, prc, shrout,
--                 exchcd, siccd, shrcd
-- Depends on: (none)
-- Notes: Universe is NYSE/AMEX/NASDAQ common stocks (shrcd IN 10,11),
--        SIC NOT IN 6000-6999 (financials excluded), PIT filtered via
--        dsenames. Investment growth signal is
--          inv_growth = (capx_{t-1} - capx_{t-3}) / capx_{t-3}
--        where year0 = t (year 0 = year of portfolio formation).
--        Signal is assigned to all months July year0 through June year0+1.
--        We do NOT apply the paper's `inv_growth > 10 or < -0.99` clip
--        here; the clip is applied at the decile-sort step in Python.
--        36-month CRSP return-history filter is NOT enforced here at the
--        SQL stage (it's enforced at the analysis-stage in main.py via
--        `n_prior_ret`); the panel preserves the full data so the auditor
--        can verify the impact.

WITH
  -- CRSP universe: monthly stocks with PIT shrcd/exchcd/siccd via dsenames
  crsp_universe AS (
    SELECT
      m.permno,
      toDate32(m.date)                    AS msf_date,
      toStartOfMonth(toDate32(m.date))    AS month,
      m.ret                               AS ret,
      m.prc                               AS prc,
      m.shrout                            AS shrout,
      d.shrcd                             AS shrcd,
      d.exchcd                            AS exchcd,
      d.siccd                             AS siccd
    FROM crsp_202601.msf AS m
    INNER JOIN crsp_202601.dsenames AS d
      ON m.permno = d.permno
     AND toDate32(m.date) >= toDate32(d.namedt)
     AND toDate32(m.date) <= ifNull(toDate32(d.nameendt), toDate32('2099-12-31'))
    WHERE toDate32(m.date) BETWEEN toDate32('1976-01-01') AND toDate32('2000-12-31')
      AND d.shrcd IN (10, 11)
      AND d.exchcd IN (1, 2, 3)
      AND (d.siccd < 6000 OR d.siccd >= 7000)
      AND m.ret IS NOT NULL
      AND m.ret > -1.0
  ),

  -- CRSP-Compustat link (PIT, usedflag=1, primary/confirmed)
  link AS (
    SELECT
      toInt32(lpermno)                    AS permno,
      gvkey,
      ifNull(toDate32(linkdt),  toDate32('1900-01-01'))   AS linkdt,
      ifNull(toDate32(linkenddt), toDate32('2099-12-31')) AS linkenddt
    FROM crsp_202601.ccmxpf_linktable
    WHERE lpermno IS NOT NULL
      AND linktype IN ('LC', 'LU')
      AND linkprim IN ('P', 'C')
      AND usedflag = 1
  ),

  -- Attach gvkey (PIT) to CRSP universe
  universe_with_gvkey AS (
    SELECT
      u.permno,
      u.month,
      u.msf_date,
      u.ret,
      u.prc,
      u.shrout,
      u.shrcd,
      u.exchcd,
      u.siccd,
      l.gvkey
    FROM crsp_universe AS u
    INNER JOIN link AS l
      ON u.permno = l.permno
     AND u.msf_date >= l.linkdt
     AND u.msf_date <= l.linkenddt
  ),

  -- Compustat capx by (gvkey, fyear), filtered to industrial format
  comp_capx AS (
    SELECT
      gvkey,
      fyear,
      capx
    FROM comp_202601.funda
    WHERE fyear IS NOT NULL
      AND fyear BETWEEN 1973 AND 1999
      AND indfmt = 'INDL'
      AND consol = 'C'
      AND popsrc = 'D'
      AND datafmt = 'STD'
      AND capx IS NOT NULL
  ),

  -- Investment growth per (gvkey, year0), year0 = fyear + 1
  -- Need capx at fyear = year0-1 and fyear = year0-3, both > 0
  inv_signal AS (
    SELECT
      c1.gvkey,
      c1.fyear + 1          AS year0,
      (c1.capx - c3.capx) / c3.capx AS inv_growth
    FROM comp_capx AS c1
    INNER JOIN comp_capx AS c3
      ON c1.gvkey = c3.gvkey
     AND c3.fyear = c1.fyear - 2
    WHERE c1.capx > 0
      AND c3.capx > 0
  ),

  -- year0 of formation year for each month:
  --   month >= July:   year0 = calendar year of month (new formation)
  --   month <  July:   year0 = calendar year of month - 1 (holding window)
  panel AS (
    SELECT
      u.permno,
      u.month,
      u.gvkey,
      u.ret,
      u.prc,
      u.shrout,
      u.shrcd,
      u.exchcd,
      u.siccd,
      CASE
        WHEN toMonth(u.month) >= 7 THEN toYear(u.month)
        ELSE toYear(u.month) - 1
      END                                                       AS year0,
      abs(u.prc) * u.shrout * 1000                              AS me_dollars,
      i.inv_growth                                              AS inv_growth
    FROM universe_with_gvkey AS u
    LEFT JOIN inv_signal AS i
      ON u.gvkey = i.gvkey
     AND i.year0 = (CASE
                      WHEN toMonth(u.month) >= 7 THEN toYear(u.month)
                      ELSE toYear(u.month) - 1
                    END)
  ),

  -- Per-permno one-month-lagged ME (for [M1] Table V value-weight look-ahead
  -- fix). NaN where the lag is not available (first month of each permno's
  -- life). Also count the number of prior CRSP return observations per
  -- permno (for [M7] 36-month return-history filter).
  panel_with_lag AS (
    SELECT
      p.permno,
      p.month,
      p.gvkey,
      p.ret,
      p.prc,
      p.shrout,
      p.shrcd,
      p.exchcd,
      p.siccd,
      p.year0,
      p.me_dollars,
      p.inv_growth,
      lagInFrame(p.me_dollars, 1) OVER w                        AS me_lag,
      row_number() OVER w - 1                                   AS n_prior_ret
    FROM panel AS p
    WINDOW w AS (PARTITION BY p.permno ORDER BY p.month
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
  )

SELECT
  permno,
  month,
  gvkey,
  ret,
  me_dollars,
  me_lag,
  n_prior_ret,
  year0,
  inv_growth,
  prc,
  shrout,
  exchcd,
  siccd,
  shrcd
FROM panel_with_lag
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 5000000000,
         timeout_before_checking_execution_speed = 0
