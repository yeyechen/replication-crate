-- comp_fundamentals.sql
-- Purpose: Build Compustat-derived NOA, PM, ATO, RNOA panel at (gvkey, fyear)
-- Tables: comp_202601.funda, comp_202601.company
-- Output columns: gvkey, fyear, datadate, sic, AT, ACT, LCT, CHE, IVST, DLTT, DLC, CEQ, MIB, PSTK, OIADP, SALE, NOA, PM, ATO, RNOA, avg_NOA
-- Depends on: (none)
-- Settings: max_execution_time=600, max_rows_to_read=5e8
--
-- NOA construction (per Soliman 2007 L504-505, L1664):
--   Operating Assets = AT - CHE - IVST
--   Operating Liabilities = AT - (DLTT + DLC) - CEQ - MIB - PSTK
--   NOA = (CHE + IVST) - (DLTT + DLC + CEQ + MIB + PSTK)
--
-- PM = OIADP / SALE
-- ATO = SALE / ((NOA_t + NOA_{t-1}) / 2)
-- RNOA = PM * ATO  (paper says "RNOA = Operating Income / Average NOA" — both
--   are equivalent only when OIADP = PM*ATO*avg_NOA = OIADP*ATO/(avg_NOA*PM*ATO)
--   * avg_NOA, which is identity. So multiplicative form and direct form agree.)
--
-- Filters (paper L488, L498):
--   indfmt='FS' (Compustat industrial format - 2003 vintage convention; modern is INDL
--     but in this catalog indfmt is checked to be 'FS' since the paper era was 2007)
--   consol='C'
--   popsrc='D'
--   SIC NOT IN ('6000'..'6999')
--   OIADP > 0  AND NOA > 0
--   fyear BETWEEN 1984 AND 2002

WITH
  raw AS (
    SELECT
      f.gvkey,
      toUInt32OrZero(f.fyear) AS fyear,
      toDate32OrNull(f.datadate) AS datadate,
      c.sic,
      toFloat64OrNull(f.at)  AS AT,
      toFloat64OrNull(f.act) AS ACT,
      toFloat64OrNull(f.lct) AS LCT,
      toFloat64OrNull(f.che) AS CHE,
      toFloat64OrNull(f.ivst) AS IVST,
      toFloat64OrNull(f.dltt) AS DLTT,
      toFloat64OrNull(f.dlc)  AS DLC,
      toFloat64OrNull(f.ceq)  AS CEQ,
      toFloat64OrNull(f.mib)  AS MIB,
      toFloat64OrNull(f.pstk) AS PSTK,
      toFloat64OrNull(f.oiadp) AS OIADP,
      toFloat64OrNull(f.sale) AS SALE
    FROM comp_202601.funda AS f
    INNER JOIN comp_202601.company AS c ON f.gvkey = c.gvkey
    WHERE f.indfmt = 'FS'
      AND f.consol = 'C'
      AND f.popsrc  = 'D'
      AND f.fyear BETWEEN 1984 AND 2002
      AND f.at  IS NOT NULL
      AND f.oiadp IS NOT NULL
      AND f.sale IS NOT NULL
  ),
  derived AS (
    SELECT
      *,
      -- Operating Assets = AT - CHE - IVST
      (AT - CHE - IVST) AS op_assets,
      -- Operating Liabilities = AT - (DLTT+DLC) - CEQ - MIB - PSTK
      (AT - DLTT - DLC - CEQ - MIB - PSTK) AS op_liab,
      -- NOA = op_assets - op_liab = (CHE + IVST) - (DLTT + DLC + CEQ + MIB + PSTK)
      (CHE + IVST) - (DLTT + DLC + CEQ + MIB + PSTK) AS NOA
    FROM raw
  ),
  filtered AS (
    SELECT *
    FROM derived
    WHERE NOA > 0
      AND OIADP > 0
      AND sic IS NOT NULL
      -- SIC NOT IN 6000-6999 (financials): filter as a string range
      AND NOT (
        toUInt32OrZero(sic) BETWEEN 6000 AND 6999
      )
      AND AT IS NOT NULL AND ACT IS NOT NULL AND LCT IS NOT NULL
      AND CHE IS NOT NULL AND IVST IS NOT NULL
      AND DLTT IS NOT NULL AND DLC IS NOT NULL
      AND CEQ IS NOT NULL AND MIB IS NOT NULL AND PSTK IS NOT NULL
  ),
  -- Pick the most-recently-filed row per (gvkey, fyear) to handle duplicate
  -- filings (the same (gvkey, datadate) can have multiple rows in comp_202601
  -- if datafmt, indfmt, consol, popsrc differ — we already filtered these).
  -- Take row_number=1 by datadate desc to get the latest filed datadate.
  deduped AS (
    SELECT *
    FROM (
      SELECT
        gvkey, fyear, datadate, sic, AT, ACT, LCT, CHE, IVST, DLTT, DLC, CEQ, MIB, PSTK,
        OIADP, SALE, op_assets, op_liab, NOA,
        row_number() OVER (PARTITION BY gvkey, fyear ORDER BY datadate DESC) AS rn
      FROM filtered
    )
    WHERE rn = 1
  ),
  -- Compute per-firm lagged NOA via window function (PARTITION BY gvkey).
  -- When the prior fyear is missing the lag is NULL (and ATO is NULL downstream).
  with_lags AS (
    SELECT
      gvkey, fyear, datadate, sic,
      AT, ACT, LCT, CHE, IVST, DLTT, DLC, CEQ, MIB, PSTK,
      OIADP, SALE, op_assets, op_liab, NOA,
      lagInFrame(NOA, 1) OVER w AS NOA_lag1
    FROM deduped
    WINDOW w AS (PARTITION BY gvkey ORDER BY fyear
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  ),
  -- Construct PM, ATO, RNOA, avg_NOA.
  ratios AS (
    SELECT
      gvkey, fyear, datadate, sic,
      AT, ACT, LCT, CHE, IVST, DLTT, DLC, CEQ, MIB, PSTK,
      OIADP, SALE, NOA, NOA_lag1,
      -- PM = OIADP / SALE
      OIADP / SALE AS PM,
      -- avg_NOA = (NOA_t + NOA_{t-1}) / 2
      (NOA + NOA_lag1) / 2.0 AS avg_NOA,
      -- ATO = SALE / avg_NOA
      SALE / ((NOA + NOA_lag1) / 2.0) AS ATO,
      -- RNOA via direct form: OIADP / avg_NOA
      OIADP / ((NOA + NOA_lag1) / 2.0) AS RNOA
    FROM with_lags
    WHERE NOA_lag1 IS NOT NULL
  )
SELECT
  gvkey, fyear, datadate, sic,
  AT, ACT, LCT, CHE, IVST, DLTT, DLC, CEQ, MIB, PSTK,
  OIADP, SALE, NOA,
  NOA_lag1,
  avg_NOA,
  PM, ATO, RNOA
FROM ratios
SETTINGS max_execution_time = 600,
         max_rows_to_read = 500000000,
         timeout_before_checking_execution_speed = 0