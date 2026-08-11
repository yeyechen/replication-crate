-- fm_panel.sql
-- Purpose: Extend the analysis-ready monthly panel with the variables
--          needed for the Fama-MacBeth regressions in Table III.
--          Adds: ln_me (log market equity), ln_bm (log book-to-market),
--          ln_inv (log 1+investment-growth), plus intermediate columns
--          be (book equity at FY ending in calendar year (year0-1)),
--          me_dec (CRSP market equity at end of December of year0-1),
--          bm = be / me_dec, plus per-permno lagged ME and prior ret
--          count from panel.sql.
-- Tables:  crsp_202601.msf (monthly returns, prc, shrout),
--          crsp_202601.dsenames (PIT shrcd/exchcd/siccd),
--          crsp_202601.ccmxpf_linktable (CRSP-Compustat link),
--          comp_202601.funda (annual fundamentals: capx, ceq, txdb,
--                              pstkrv, at, dlc, dltt)
-- Output columns: permno, month, gvkey, ret, me_dollars, me_lag,
--                 n_prior_ret, year0, inv_growth, prc, shrout,
--                 exchcd, siccd, shrcd, be, me_dec, bm, me_jun_form,
--                 ln_me, ln_bm, ln_inv
-- Depends on: (none) — inherits the same logic as panel.sql
-- Notes: BE follows FF (1993) convention from Davis-Fama-French memo:
--        primary = ceq + txdb - pstkrv (if > 0), fallback
--        = at - dlc - dltt - pstkrv (if > 0), else NULL.
--        BE is joined by gvkey at fyear = year0 - 1 (i.e. fiscal year
--        ending in calendar year year0 - 1, consistent with Table I
--        caption "book equity at the end of fiscal year t-1").
--        me_dec is the row's me_dollars at the December snapshot of
--        panel year0 - 1 (i.e. December of calendar year year0 - 1).
--        ln_inv = ln(1 + inv_growth) = ln(capx_t / capx_{t-2}); symmetric
--        around 0, well-defined for inv_growth > -1 (after the paper's
--        1%/99% clip).

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
    WHERE toDate32(m.date) BETWEEN toDate32('1975-07-01') AND toDate32('2000-06-30')
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

  -- Panel base: same as panel.sql.
  -- year0 = paper's "year t" of portfolio formation;
  --         month >= July:   year0 = calendar year of month
  --         month <  July:   year0 = calendar year of month - 1
  -- The holding window for year0 = Y is July Y .. June (Y+1).
  -- Portfolio formation occurs at end of June Y (just before July Y).
  base_panel AS (
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
      END                                                  AS year0,
      abs(u.prc) * u.shrout * 1000                         AS me_dollars,
      i.inv_growth                                         AS inv_growth
    FROM universe_with_gvkey AS u
    LEFT JOIN inv_signal AS i
      ON u.gvkey = i.gvkey
     AND i.year0 = (CASE
                      WHEN toMonth(u.month) >= 7 THEN toYear(u.month)
                      ELSE toYear(u.month) - 1
                    END)
  ),

  -- Book equity at fiscal year ending in calendar year (year0 - 1).
  -- FF recipe: primary = ceq + txdb - pstkrv (if positive),
  --            fallback = at - dlc - dltt - pstkrv (if positive),
  --            else NULL.
  -- Units: comp_202601.funda stores ceq/txdb/pstkrv/at/dlc/dltt in
  --        **millions of USD** (Compustat convention). CRSP's
  --        me_dollars is in **dollars**. We convert BE to dollars by
  --        multiplying by 1,000,000 so the ratio is unitless.
  -- We key the BE signal to year0 = fyear + 1 so that joining on
  -- year0 (paper's portfolio formation year) automatically picks up
  -- fyear = year0 - 1.
  comp_be AS (
    SELECT
      gvkey,
      fyear + 1                                                    AS year0,
      CASE
        WHEN (ceq + txdb - pstkrv) > 0
          THEN (ceq + txdb - pstkrv) * 1000000.0
        WHEN (at - dlc - dltt - pstkrv) > 0
          THEN (at - dlc - dltt - pstkrv) * 1000000.0
        ELSE NULL
      END                                                          AS be
    FROM comp_202601.funda
    WHERE indfmt = 'INDL'
      AND consol = 'C'
      AND popsrc = 'D'
      AND datafmt = 'STD'
      AND fyear IS NOT NULL
      AND fyear BETWEEN 1974 AND 1999
  ),

  -- ME snapshot at end of December of calendar year (year0 - 1).
  -- December (month 12, calendar year Z) row has panel year0 = Z.
  -- For cohort year0 = Y we want Dec (Y-1), which has panel year0 = Y-1.
  -- The snapshot table stores one row per (permno, panel_year0_of_dec);
  -- join condition for cohort year0 = Y is snap_year0 = Y - 1.
  me_dec_snapshot AS (
    SELECT
      permno,
      year0                                          AS snap_year0,
      me_dollars                                     AS me_dec
    FROM base_panel
    WHERE toMonth(month) = 12
  ),

  -- ME snapshot at end of FORMATION June: the calendar June of year
  -- (year0 + 1) is the LAST month of the year0 cohort's holding window
  -- — but the FORMATION date is end of June of CALENDAR YEAR year0
  -- (since year0 = Y means holding starts July Y and the formation
  -- is at end of June Y). The calendar June Y row has panel year0 =
  -- Y - 1 (because month < 7 in the FF panel labeling). So we look up
  -- the snapshot by `snap_year0 = p.year0 - 1` — same lookup arithmetic
  -- as the December ME used for the B/M denominator.
  -- Used for `ln_size` (Ln(size)) — the FM convention takes size at
  -- portfolio-formation date and holds it constant for 12 months.
  -- This avoids the look-ahead bias of using same-month me_dollars,
  -- which mechanically correlates with the same-month return.
  me_jun_form_snapshot AS (
    SELECT
      permno,
      year0                                          AS snap_year0,
      me_dollars                                     AS me_jun_form
    FROM base_panel
    WHERE toMonth(month) = 6
  ),

  -- Final FM panel: join BE + me_dec snapshot + compute bm + log terms.
  panel_with_fm AS (
    SELECT
      p.permno        AS permno,
      p.month         AS month,
      p.gvkey         AS gvkey,
      p.ret           AS ret,
      p.me_dollars    AS me_dollars,
      p.year0         AS year0,
      p.inv_growth    AS inv_growth,
      p.prc           AS prc,
      p.shrout        AS shrout,
      p.exchcd        AS exchcd,
      p.siccd         AS siccd,
      p.shrcd         AS shrcd,
      b.be            AS be,
      m.me_dec        AS me_dec,
      j.me_jun_form   AS me_jun_form,
      CASE
        WHEN b.be IS NOT NULL AND m.me_dec IS NOT NULL AND m.me_dec > 0
          THEN b.be / m.me_dec
        ELSE NULL
      END             AS bm,
      -- ln_me = log(me_jun_form); formation-month ME held constant for
      -- 12 months (FF convention). NULL where formation ME missing.
      CASE
        WHEN j.me_jun_form IS NOT NULL AND j.me_jun_form > 0
          THEN log(j.me_jun_form)
        ELSE NULL
      END             AS ln_me,
      -- ln_bm = log(bm); NULL where bm <= 0
      CASE
        WHEN b.be IS NOT NULL AND m.me_dec IS NOT NULL
         AND m.me_dec > 0 AND (b.be / m.me_dec) > 0
          THEN log(b.be / m.me_dec)
        ELSE NULL
      END             AS ln_bm,
      -- ln_inv = ln(1 + inv_growth) = ln(capx_t / capx_{t-2}).
      -- Well-defined for inv_growth > -1 (which holds after the
      -- paper's 1%/99% winsorization); captures both positive and
      -- negative investment-growth as symmetric around 0.
      CASE
        WHEN p.inv_growth IS NOT NULL AND p.inv_growth > -1.0
          THEN log(1 + p.inv_growth)
        ELSE NULL
      END             AS ln_inv
    FROM base_panel AS p
    LEFT JOIN comp_be               AS b ON p.gvkey = b.gvkey  AND p.year0 = b.year0
    LEFT JOIN me_dec_snapshot       AS m ON p.permno = m.permno AND (p.year0 - 1) = m.snap_year0
    LEFT JOIN me_jun_form_snapshot  AS j ON p.permno = j.permno AND (p.year0 - 1) = j.snap_year0
  ),

  -- Per-permno one-month-lagged ME (for [M1] Table V value-weight look-ahead
  -- fix) and prior-CRSP-return count (for [M7] 36-month return-history filter).
  panel_with_lag AS (
    SELECT
      pp.*,
      lagInFrame(pp.me_dollars, 1) OVER w                        AS me_lag,
      row_number() OVER w - 1                                     AS n_prior_ret
    FROM panel_with_fm AS pp
    WINDOW w AS (PARTITION BY pp.permno ORDER BY pp.month
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
  shrcd,
  be,
  me_dec,
  bm,
  me_jun_form,
  ln_me,
  ln_bm,
  ln_inv
FROM panel_with_lag
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 5000000000,
         timeout_before_checking_execution_speed = 0
