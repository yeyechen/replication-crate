-- comp_panel.sql
-- Purpose: Build the Lev & Nissim (2004) comp-only firm-year panel with
--          TAX / DEF / CFO fundamentals, R_TAX / R_DEF / R_CFO industry-year
--          quintile ranks, and G1 / G2 / G3 future-earnings growth measures.
-- Tables: comp_202601.funda
-- Output columns:
--   gvkey, datadate, fyear, sich, sich_2digit, fic
--   at, ib, csho, prcc_f, ceq, sale, xrd, capx, dvp, dv
--   ca, che, lct, dlc, dp
--   txfed, txfo, txt, txdb
--   lag_at, lag_ib, lag_ca, lag_che, lag_lct, lag_dlc, lag_txdb
--   cur_tax_exp, taxable_income, TAX, DEF, accruals, CFO
--   mcap_compustat
--   R_TAX, R_DEF, R_CFO   (industry-year quintile ranks, 1..5)
--   G1, G2, G3            (future-earnings growth, percentage points)
--   n_industry_year       (group size for sanity check)
-- Depends on: (none)
-- Settings: max_execution_time=600, max_rows_to_read=2e9
--
-- Notes
-- - Per assumption #1 we use `lct` (total current liabilities, modern name for
--   the paper's `cl`) and `act` (modern name for the paper's current assets,
--   item #4). The instance column `ca` is mostly null in this extract (see
--   prep notes).
-- - Paper #5 = current liabilities → use lct; Paper #34 = change in debt in
--   current liabilities → compute as dlc_t − dlc_{t-1} (the instance
--   `dlcch` is empty in this extract).
-- - ΔCash, ΔCA, ΔCL, ΔDTL are computed via lead/lagInFrame windows partitioned
--   by gvkey, ordered by fyear. All firm-year rows are preserved (lags are
--   NULL outside the firm's history).
-- - TAX / DEF / CFO can be NULL when inputs are missing; R_TAX / R_DEF /
--   R_CFO quintile assignment uses ntile(5) over the within-(sich_2digit,
--   fyear) distribution of the non-null values (ClickHouse ntile is
--   deterministic with the same ORDER BY).
-- - G1 / G2 / G3 are computed from lead(ib, 1..5) within gvkey and the
--   fyear window. G3 needs fyear ≤ 1995 (5-year forward window into the
--   2000 endpoint). G2 needs fyear ≤ 1998; G1 needs fyear ≤ 1999.

WITH
  ---------------------------------------------------------------
  -- 1) Standard comp quality filter + paper's universe (US,
  --    Dec FYE, non-regulated, non-flow-through, sample window).
  ---------------------------------------------------------------
  base AS (
    SELECT
      gvkey,
      toDate32OrNull(datadate)                         AS datadate,
      fyear,
      fyr,
      sich,
      intDiv(sich, 100)                                AS sich_2digit,
      fic,
      curcd,
      at, ib, csho, prcc_f, ceq,
      sale, xrd, capx, dvp, dv,
      act                                              AS ca,
      che, lct, dlc, dp,
      txfed, txfo, txt, txdb
    FROM comp_202601.funda
    WHERE indfmt = 'INDL'
      AND consol = 'C'
      AND popsrc  = 'D'
      AND datafmt = 'STD'
      AND fic     = 'USA'
      AND fyr     = 12
      AND fyear  BETWEEN 1973 AND 2000
      AND intDiv(sich, 100) NOT IN (49, 60, 61, 62, 63, 64, 65, 66, 67)
      -- Required-data screen (paper's #6, #18, #199, #25, #60, #16, #50).
      AND at      IS NOT NULL
      AND ib      IS NOT NULL
      AND prcc_f  IS NOT NULL
      AND csho    IS NOT NULL
      AND ceq     IS NOT NULL
      AND txt     IS NOT NULL
      AND txdb    IS NOT NULL
  ),
  ---------------------------------------------------------------
  -- 2) Window per gvkey: lag/lead values needed for Δ-terms and
  --    future-earnings growth (G1, G2, G3).
  ---------------------------------------------------------------
  with_window AS (
    SELECT
      b.*,
      lagInFrame(b.at,    1) OVER w AS lag_at,
      lagInFrame(b.ib,    1) OVER w AS lag_ib,
      lagInFrame(b.ca,    1) OVER w AS lag_ca,
      lagInFrame(b.che,   1) OVER w AS lag_che,
      lagInFrame(b.lct,   1) OVER w AS lag_lct,
      lagInFrame(b.dlc,   1) OVER w AS lag_dlc,
      lagInFrame(b.txdb,  1) OVER w AS lag_txdb,
      leadInFrame(b.ib,   1) OVER w AS lead_ib_1,
      leadInFrame(b.ib,   2) OVER w AS lead_ib_2,
      leadInFrame(b.ib,   3) OVER w AS lead_ib_3,
      leadInFrame(b.ib,   4) OVER w AS lead_ib_4,
      leadInFrame(b.ib,   5) OVER w AS lead_ib_5
    FROM base AS b
    WINDOW w AS (
      PARTITION BY b.gvkey
      ORDER BY b.fyear
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    )
  ),
  ---------------------------------------------------------------
  -- 3) Derived variables: current tax expense, taxable income,
  --    TAX, DEF, accruals, CFO, mcap, future growth.
  ---------------------------------------------------------------
  derived AS (
    SELECT
      gvkey, datadate, fyear, sich, sich_2digit, fic, curcd,
      at, ib, csho, prcc_f, ceq,
      sale, xrd, capx, dvp, dv,
      ca, che, lct, dlc, dp,
      txfed, txfo, txt, txdb,
      lag_at, lag_ib, lag_ca, lag_che, lag_lct, lag_dlc, lag_txdb,
      lead_ib_1, lead_ib_2, lead_ib_3, lead_ib_4, lead_ib_5,
      -- Year-specific top federal corporate tax rate (paper footnote 10).
      multiIf(
        fyear BETWEEN 1973 AND 1978, 0.48,
        fyear BETWEEN 1979 AND 1986, 0.46,
        fyear = 1987,                0.40,
        fyear BETWEEN 1988 AND 1992, 0.34,
        fyear BETWEEN 1993 AND 2000, 0.35,
        NULL
      ) AS t_stat,
      -- Current tax expense (paper footnote 10): txfed + txfo, fallback
      -- to txt - txdb when either component is missing.
      if(
        txfed IS NOT NULL AND txfo IS NOT NULL, txfed + txfo,
        if(txt IS NOT NULL AND txdb IS NOT NULL, txt - txdb, NULL)
      ) AS cur_tax_exp
    FROM with_window
  ),
  computed AS (
    SELECT
      *,
      -- taxable_income = cur_tax_exp / t_stat (paper Eq. 2)
      if(cur_tax_exp IS NOT NULL AND t_stat IS NOT NULL AND t_stat > 0,
         cur_tax_exp / t_stat, NULL) AS taxable_income,
      -- ΔCA = ca_t − ca_{t-1}; lag_ca is NULL for the firm's first year.
      if(ca     IS NOT NULL AND lag_ca    IS NOT NULL, ca    - lag_ca,    NULL) AS d_ca,
      if(che    IS NOT NULL AND lag_che   IS NOT NULL, che   - lag_che,   NULL) AS d_cash,
      if(lct    IS NOT NULL AND lag_lct   IS NOT NULL, lct   - lag_lct,   NULL) AS d_cl,
      if(dlc    IS NOT NULL AND lag_dlc   IS NOT NULL, dlc   - lag_dlc,   NULL) AS d_std,
      if(txdb   IS NOT NULL AND lag_txdb  IS NOT NULL, txdb  - lag_txdb,  NULL) AS d_dtl
    FROM derived
  ),
  fundamentals AS (
    SELECT
      *,
      -- DEF = -txdb / ((at + lag_at) / 2). Require lag_at present.
      if(
        at IS NOT NULL AND lag_at IS NOT NULL AND txdb IS NOT NULL,
        -txdb / ((at + lag_at) / 2.0),
        NULL
      ) AS def_raw,
      -- TAX = taxable_income * (1 - t_stat) / ib. Require ib > 0.
      if(
        taxable_income IS NOT NULL AND t_stat IS NOT NULL AND ib > 0,
        taxable_income * (1 - t_stat) / ib,
        NULL
      ) AS tax_raw,
      -- Accruals = (ΔCA − ΔCash) − (ΔCL − ΔSTD) − ΔDTL − dp
      if(
        d_ca IS NOT NULL AND d_cash IS NOT NULL
        AND d_cl IS NOT NULL AND d_std IS NOT NULL
        AND d_dtl IS NOT NULL AND dp IS NOT NULL,
        (d_ca - d_cash) - (d_cl - d_std) - d_dtl - dp,
        NULL
      ) AS accruals,
      -- Compustat market cap (millions of USD). csho is in millions;
      -- prcc_f is in USD per share → product is in millions.
      if(csho IS NOT NULL AND prcc_f IS NOT NULL, prcc_f * csho, NULL) AS mcap_compustat,
      -- Future earnings growth (paper Eq. 4), deflated by at and reported
      -- in percentage points.
      if(
        lead_ib_1 IS NOT NULL AND at IS NOT NULL AND at > 0,
        (lead_ib_1 - ib) / at * 100,
        NULL
      ) AS g1,
      if(
        lead_ib_1 IS NOT NULL AND lead_ib_2 IS NOT NULL AND lead_ib_3 IS NOT NULL
        AND at IS NOT NULL AND at > 0,
        ((lead_ib_1 + lead_ib_2 + lead_ib_3) / 3.0 - ib) / at * 100,
        NULL
      ) AS g2,
      if(
        lead_ib_1 IS NOT NULL AND lead_ib_2 IS NOT NULL AND lead_ib_3 IS NOT NULL
        AND lead_ib_4 IS NOT NULL AND lead_ib_5 IS NOT NULL
        AND at IS NOT NULL AND at > 0,
        ((lead_ib_1 + lead_ib_2 + lead_ib_3 + lead_ib_4 + lead_ib_5) / 5.0 - ib) / at * 100,
        NULL
      ) AS g3
    FROM computed
  ),
  ---------------------------------------------------------------
  -- 4) CFO and the DEF/TAX final variables.
  ---------------------------------------------------------------
  cfo_step AS (
    SELECT
      *,
      -- CFO = (ib − accruals) / ib, paper footnote 16.
      if(
        accruals IS NOT NULL AND ib > 0,
        (ib - accruals) / ib,
        NULL
      ) AS cfo_raw
    FROM fundamentals
  ),
  ---------------------------------------------------------------
  -- 5) Within (sich_2digit, fyear) industry-year group, compute
  --    R_TAX, R_DEF, R_CFO quintile ranks using ntile(5).
  --    ntile is non-deterministic when ties exist at a bucket
  --    boundary, but over a 5-bucket partition the result is
  --    stable across the same SQL text. We use ROWS BETWEEN
  --    UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING so the
  --    ranking sees every firm in the group.
  ---------------------------------------------------------------
  ranked AS (
    SELECT
      c.*,
      -- Group size for downstream sanity checks / diagnostics.
      count() OVER (PARTITION BY c.sich_2digit, c.fyear) AS n_industry_year,
      -- R_TAX: quintile of TAX within industry-year, 1 = lowest,
      -- 5 = highest. NULL inputs get NULL rank.
      if(
        c.tax_raw IS NOT NULL,
        ntile(5) OVER (
          PARTITION BY c.sich_2digit, c.fyear
          ORDER BY c.tax_raw ASC
          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ),
        NULL
      ) AS r_tax,
      if(
        c.def_raw IS NOT NULL,
        ntile(5) OVER (
          PARTITION BY c.sich_2digit, c.fyear
          ORDER BY c.def_raw ASC
          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ),
        NULL
      ) AS r_def,
      if(
        c.cfo_raw IS NOT NULL,
        ntile(5) OVER (
          PARTITION BY c.sich_2digit, c.fyear
          ORDER BY c.cfo_raw ASC
          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ),
        NULL
      ) AS r_cfo
    FROM cfo_step AS c
  )
SELECT
  gvkey, datadate, fyear, sich, sich_2digit, fic, curcd,
  at, ib, csho, prcc_f, ceq,
  sale, xrd, capx, dvp, dv,
  ca, che, lct, dlc, dp,
  txfed, txfo, txt, txdb,
  lag_at, lag_ib, lag_ca, lag_che, lag_lct, lag_dlc, lag_txdb,
  t_stat, cur_tax_exp, taxable_income,
  tax_raw  AS tax,
  def_raw  AS def,
  accruals,
  cfo_raw  AS cfo,
  mcap_compustat,
  g1, g2, g3,
  r_tax, r_def, r_cfo,
  n_industry_year
FROM ranked
SETTINGS max_execution_time = 600,
         max_rows_to_read = 2000000000,
         timeout_before_checking_execution_speed = 0
