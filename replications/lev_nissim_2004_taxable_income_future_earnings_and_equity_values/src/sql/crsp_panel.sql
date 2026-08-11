-- crsp_panel.sql
-- Purpose: Build the CRSP-linked comp-CRSP panel for Lev & Nissim
--          Tables 4 and 5. Combines:
--             (a) the comp panel from comp_panel.sql (TAX/DEF/CFO, R_*,
--                 G-vars), restricted to fyear 1987-2000 (post-1987 only);
--             (b) PIT link to CRSP permno via ccmxpf_linktable;
--             (c) cumulative CRSP return Jan-Apr (for P*);
--             (d) cumulative CRSP return May-Apr (for the one-year-ahead
--                 stock-return regression in Table 5);
--             (e) April ME at end of April (t+1) for SIZE in Table 5;
--             (f) book equity at FYE for B/P;
--             (g) the E/P* value itself for Table 4.
-- Tables: comp_202601.funda, crsp_202601.ccmxpf_linktable,
--         crsp_202601.msf
-- Output columns (one row per (gvkey, fyear) with a CRSP link):
--   gvkey, datadate, fyear, sich_2digit, permno,
--   ib, ceq, at, lt, dv, dvp, csho, prcc_f, mcap_compustat,
--   r_tax, r_def, r_cfo, tax, def, cfo,
--   cum_ret_jan_april, cum_ret_may_april, n_months_jan_april, n_months_may_april,
--   me_april,
--   pstar, epstar_pct, ln_me, lev, pay, b_to_p
-- Depends on: (none) — runs end-to-end against ClickHouse.
-- Settings: max_execution_time=600, max_rows_to_read=1e10

WITH
  ---------------------------------------------------------------
  -- 1) Comp-side panel: same universe + fundamentals as comp_panel.sql
  --    but restricted to fyear 1987-2000 (post-1987, where ib > 0).
  --    See comp_panel.sql for full derivations of TAX / DEF / CFO,
  --    R_TAX / R_DEF / R_CFO quintile ranks, and the G-vars.
  ---------------------------------------------------------------
  base AS (
    SELECT
      gvkey,
      toDate32OrNull(datadate) AS datadate,
      fyear,
      intDiv(sich, 100)       AS sich_2digit,
      fic,
      at, ib, csho, prcc_f, ceq,
      lt, dv, dvp,
      sale, xrd, capx,
      act AS ca, che, lct, dlc, dp,
      txfed, txfo, txt, txdb
    FROM comp_202601.funda
    WHERE indfmt = 'INDL'
      AND consol = 'C'
      AND popsrc  = 'D'
      AND datafmt = 'STD'
      AND fic     = 'USA'
      AND fyr     = 12
      AND fyear  BETWEEN 1987 AND 2000
      AND intDiv(sich, 100) NOT IN (49, 60, 61, 62, 63, 64, 65, 66, 67)
      AND at      IS NOT NULL
      AND ib      IS NOT NULL
      AND prcc_f  IS NOT NULL
      AND csho    IS NOT NULL
      AND ceq     IS NOT NULL
      AND txt     IS NOT NULL
      AND txdb    IS NOT NULL
      AND ib      > 0
  ),
  with_window AS (
    SELECT
      b.*,
      lagInFrame(b.at,   1) OVER w AS lag_at,
      lagInFrame(b.ca,   1) OVER w AS lag_ca,
      lagInFrame(b.che,  1) OVER w AS lag_che,
      lagInFrame(b.lct,  1) OVER w AS lag_lct,
      lagInFrame(b.dlc,  1) OVER w AS lag_dlc,
      lagInFrame(b.txdb, 1) OVER w AS lag_txdb,
      leadInFrame(b.ib,  1) OVER w AS lead_ib_1
    FROM base AS b
    WINDOW w AS (
      PARTITION BY b.gvkey
      ORDER BY b.fyear
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    )
  ),
  derived AS (
    SELECT
      gvkey, datadate, fyear, sich_2digit, fic,
      at, ib, csho, prcc_f, ceq, lt, dv, dvp,
      ca, che, lct, dlc, dp,
      sale, xrd, capx,
      txfed, txfo, txt, txdb,
      lag_at, lag_ca, lag_che, lag_lct, lag_dlc, lag_txdb, lead_ib_1,
      multiIf(
        fyear BETWEEN 1973 AND 1978, 0.48,
        fyear BETWEEN 1979 AND 1986, 0.46,
        fyear = 1987,                0.40,
        fyear BETWEEN 1988 AND 1992, 0.34,
        fyear BETWEEN 1993 AND 2000, 0.35,
        NULL
      ) AS t_stat,
      if(txfed IS NOT NULL AND txfo IS NOT NULL, txfed + txfo,
         if(txt IS NOT NULL AND txdb IS NOT NULL, txt - txdb, NULL)) AS cur_tax_exp
    FROM with_window
  ),
  computed AS (
    SELECT
      *,
      if(cur_tax_exp IS NOT NULL AND t_stat IS NOT NULL AND t_stat > 0,
         cur_tax_exp / t_stat, NULL) AS taxable_income,
      if(ca IS NOT NULL AND lag_ca IS NOT NULL, ca - lag_ca, NULL) AS d_ca,
      if(che IS NOT NULL AND lag_che IS NOT NULL, che - lag_che, NULL) AS d_cash,
      if(lct IS NOT NULL AND lag_lct IS NOT NULL, lct - lag_lct, NULL) AS d_cl,
      if(dlc IS NOT NULL AND lag_dlc IS NOT NULL, dlc - lag_dlc, NULL) AS d_std,
      if(txdb IS NOT NULL AND lag_txdb IS NOT NULL, txdb - lag_txdb, NULL) AS d_dtl
    FROM derived
  ),
  fundamentals AS (
    SELECT
      *,
      if(at IS NOT NULL AND lag_at IS NOT NULL AND txdb IS NOT NULL,
         -txdb / ((at + lag_at) / 2.0), NULL) AS def_raw,
      if(taxable_income IS NOT NULL AND t_stat IS NOT NULL AND ib > 0,
         taxable_income * (1 - t_stat) / ib, NULL) AS tax_raw,
      if(d_ca IS NOT NULL AND d_cash IS NOT NULL AND d_cl IS NOT NULL
         AND d_std IS NOT NULL AND d_dtl IS NOT NULL AND dp IS NOT NULL,
         (d_ca - d_cash) - (d_cl - d_std) - d_dtl - dp, NULL) AS accruals,
      if(csho IS NOT NULL AND prcc_f IS NOT NULL, prcc_f * csho, NULL)
        AS mcap_compustat
    FROM computed
  ),
  cfo_step AS (
    SELECT
      *,
      if(accruals IS NOT NULL AND ib > 0, (ib - accruals) / ib, NULL) AS cfo_raw
    FROM fundamentals
  ),
  ranked AS (
    SELECT
      c.*,
      count() OVER (PARTITION BY c.sich_2digit, c.fyear) AS n_industry_year,
      if(c.tax_raw IS NOT NULL,
         ntile(5) OVER (PARTITION BY c.sich_2digit, c.fyear ORDER BY c.tax_raw ASC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING),
         NULL) AS r_tax,
      if(c.def_raw IS NOT NULL,
         ntile(5) OVER (PARTITION BY c.sich_2digit, c.fyear ORDER BY c.def_raw ASC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING),
         NULL) AS r_def,
      if(c.cfo_raw IS NOT NULL,
         ntile(5) OVER (PARTITION BY c.sich_2digit, c.fyear ORDER BY c.cfo_raw ASC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING),
         NULL) AS r_cfo
    FROM cfo_step AS c
  ),
  comp_panel AS (
    SELECT
      gvkey, datadate, fyear, sich_2digit, fic,
      at, ib, csho, prcc_f, ceq, lt, dv, dvp, mcap_compustat,
      tax_raw AS tax, def_raw AS def, cfo_raw AS cfo,
      r_tax, r_def, r_cfo, n_industry_year
    FROM ranked
  ),
  ---------------------------------------------------------------
  -- 2) PIT link gvkey → permno at the comp datadate.
  ---------------------------------------------------------------
  link AS (
    SELECT
      gvkey,
      toInt32OrNull(toString(lpermno)) AS permno,
      toDate32OrNull(linkdt)          AS linkdt,
      if(linkenddt = '' OR linkenddt IS NULL,
         toDate32('2099-12-31'),
         toDate32OrNull(linkenddt))   AS linkenddt,
      linkprim
    FROM crsp_202601.ccmxpf_linktable
    WHERE linktype IN ('LC','LU')
      AND linkprim  IN ('P','C')
      AND usedflag   = 1
      AND lpermno IS NOT NULL
      AND gvkey   IS NOT NULL
  ),
  linked AS (
    SELECT
      cp.*, l.permno
    FROM comp_panel AS cp
    INNER JOIN link AS l
      ON cp.gvkey = cp.gvkey
     AND cp.datadate >= l.linkdt
     AND cp.datadate <= l.linkenddt
     AND cp.gvkey    = l.gvkey
  ),
  ---------------------------------------------------------------
  -- 3) CRSP monthly returns — for each linked (permno, fyear):
  --    cum_ret_jan_april and cum_ret_may_april. Use the linked
  --    panel as the window driver so we only compute returns for
  --    rows we actually need.
  ---------------------------------------------------------------
  windows AS (
    SELECT
      permno,
      fyear,
      toDate32(concat(toString(fyear + 1), '-01-01')) AS start_jan,
      toDate32(concat(toString(fyear + 1), '-05-01')) AS end_jan,
      toDate32(concat(toString(fyear + 1), '-05-01')) AS start_may,
      toDate32(concat(toString(fyear + 2), '-05-01')) AS end_may,
      toDate32(concat(toString(fyear + 1), '-04-30')) AS apr_obs
    FROM (SELECT DISTINCT permno, fyear FROM linked)
  ),
  ret_jan_april AS (
    SELECT
      w.permno, w.fyear,
      count() AS n_months_jan_april,
      exp(sum(log(if(ret IS NOT NULL AND ret > -0.99, 1 + ret, 1.0)))) - 1
        AS cum_ret_jan_april
    FROM windows AS w
    INNER JOIN crsp_202601.msf AS m
      ON m.permno = w.permno
     AND toDate32OrNull(m.date) >= w.start_jan
     AND toDate32OrNull(m.date) <  w.end_jan
    WHERE m.ret IS NOT NULL
    GROUP BY w.permno, w.fyear
  ),
  ret_may_april AS (
    SELECT
      w.permno, w.fyear,
      count() AS n_months_may_april,
      exp(sum(log(if(ret IS NOT NULL AND ret > -0.99, 1 + ret, 1.0)))) - 1
        AS cum_ret_may_april
    FROM windows AS w
    INNER JOIN crsp_202601.msf AS m
      ON m.permno = w.permno
     AND toDate32OrNull(m.date) >= w.start_may
     AND toDate32OrNull(m.date) <  w.end_may
    WHERE m.ret IS NOT NULL
    GROUP BY w.permno, w.fyear
  ),
  me_april AS (
    SELECT
      w.permno, w.fyear,
      abs(toFloat64(any(m.prc))) * toFloat64(any(m.shrout)) / 1000.0 AS me_april
    FROM windows AS w
    INNER JOIN crsp_202601.msf AS m
      ON m.permno = w.permno
     AND toYear(toDate32OrNull(m.date))  = w.fyear + 1
     AND toMonth(toDate32OrNull(m.date)) = 4
    WHERE m.prc IS NOT NULL AND m.shrout IS NOT NULL AND m.shrout > 0
    GROUP BY w.permno, w.fyear
  )
SELECT
  l.gvkey, l.datadate, l.fyear, l.sich_2digit, l.fic, l.permno,
  l.at, l.ib, l.csho, l.prcc_f, l.ceq, l.lt, l.dv, l.dvp,
  l.mcap_compustat,
  l.tax, l.def, l.cfo, l.r_tax, l.r_def, l.r_cfo, l.n_industry_year,
  rj.cum_ret_jan_april, rm.cum_ret_may_april,
  rj.n_months_jan_april, rm.n_months_may_april,
  me.me_april,
  -- P* = mcap_fye × (1 + cum_ret_jan_april); null if cum_ret is null.
  if(l.mcap_compustat IS NOT NULL AND rj.cum_ret_jan_april IS NOT NULL,
     l.mcap_compustat * (1 + rj.cum_ret_jan_april), NULL) AS pstar,
  -- E/P* in percentage points: ib / pstar * 100.
  if(l.ib IS NOT NULL
     AND rj.cum_ret_jan_april IS NOT NULL
     AND l.mcap_compustat IS NOT NULL
     AND l.mcap_compustat * (1 + rj.cum_ret_jan_april) > 0,
     l.ib / (l.mcap_compustat * (1 + rj.cum_ret_jan_april)) * 100,
     NULL) AS epstar_pct,
  -- ln_me = log(abs(prc)*shrout/1000) at FYE
  if(l.prcc_f IS NOT NULL AND l.csho IS NOT NULL,
     ln(abs(l.prcc_f) * l.csho), NULL) AS ln_me_fye,
  -- log of April ME (Table 5 SIZE)
  if(me.me_april IS NOT NULL AND me.me_april > 0,
     ln(me.me_april), NULL) AS ln_me_april,
  -- LEV = lt / at
  if(l.lt IS NOT NULL AND l.at IS NOT NULL AND l.at > 0,
     l.lt / l.at, NULL) AS lev,
  -- PAY = dv / ib
  if(l.dv IS NOT NULL AND l.ib IS NOT NULL AND l.ib > 0,
     l.dv / l.ib, NULL) AS pay,
  -- B/P = ceq / me_april (book-to-market at FYE divided by April ME)
  if(l.ceq IS NOT NULL AND me.me_april IS NOT NULL AND me.me_april > 0,
     l.ceq / me.me_april, NULL) AS b_to_p,
  -- E/P (current E/P ratio) = ib / me_april, in percentage points
  if(l.ib IS NOT NULL AND me.me_april IS NOT NULL AND me.me_april > 0,
     l.ib / me.me_april * 100, NULL) AS ep_pct
FROM linked AS l
LEFT JOIN ret_jan_april AS rj
  ON l.permno = rj.permno AND l.fyear = rj.fyear
LEFT JOIN ret_may_april AS rm
  ON l.permno = rm.permno AND l.fyear = rm.fyear
LEFT JOIN me_april      AS me
  ON l.permno = me.permno  AND l.fyear = me.fyear
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0