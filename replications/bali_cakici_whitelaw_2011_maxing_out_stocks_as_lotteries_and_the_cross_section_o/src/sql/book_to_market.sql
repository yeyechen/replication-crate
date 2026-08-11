-- book_to_market.sql
-- Purpose: Book-to-market ratio using Compustat funda (book equity) and
--          CRSP msf (December market equity) via the ccmxpf_linktable.
--
--          Book equity (primary formula, per Fama-French convention):
--              be = ceq + txdb - pstkrv
--          Fallback when be <= 0:
--              be = at - dlc - dltt - pstkrv
--
--          Fiscal-year alignment: book equity from fiscal year Y is paired
--          with ME from December of year Y-1 (i.e., returns from July Y
--          through June Y+1 use book equity from fyear=Y-1 and ME from
--          December Y-1). This is the standard FF1992 lag.
--
--          Output: a (gvkey, fyear) -> bm mapping. For use with monthly
--          portfolios at month t: look up fyear where
--              t.month >= 7 -> fyear_use = t.year - 1
--              t.month <  7 -> fyear_use = t.year - 2
--          and use the bm from that fyear.
-- Tables: comp_202601.funda, crsp_202601.ccmxpf_linktable, crsp_202601.msf
-- Output columns: permno, fyear, bm
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge, max_execution_time=600
WITH
  be AS (
      -- Compute book equity per (gvkey, fyear) using the FF convention.
      SELECT gvkey,
             fyear,
             -- Primary formula: ceq + txdb - pstkrv
             coalesce(ceq, 0) + coalesce(txdb, 0) - coalesce(pstkrv, 0) AS be_primary
      FROM comp_202601.funda
      WHERE indfmt = 'INDL'
        AND consol = 'C'
        AND popsrc = 'D'
        AND datafmt = 'STD'
        AND fyear IS NOT NULL
        AND fyear BETWEEN 1961 AND 2005
  ),
  be_fallback AS (
      -- Fallback: total assets - current liabilities - long-term debt - preferred stock
      SELECT gvkey,
             fyear,
             coalesce(at, 0) - coalesce(dlc, 0) - coalesce(dltt, 0) - coalesce(pstkrv, 0) AS be_alt
      FROM comp_202601.funda
      WHERE indfmt = 'INDL'
        AND consol = 'C'
        AND popsrc = 'D'
        AND datafmt = 'STD'
        AND fyear IS NOT NULL
        AND fyear BETWEEN 1961 AND 2005
  ),
  book_equity AS (
      -- Use primary when > 0; otherwise fallback; otherwise NULL.
      SELECT b.gvkey,
             b.fyear,
             if(b.be_primary > 0, b.be_primary,
                if(fb.be_alt > 0, fb.be_alt, NULL)) AS be
      FROM be AS b
      LEFT JOIN be_fallback AS fb
          ON b.gvkey = fb.gvkey AND b.fyear = fb.fyear
  ),
  link AS (
      -- CRSP-Compustat link: keep LC/LU, primary links.
      SELECT gvkey, lpermno AS permno, linkdt, linkenddt
      FROM crsp_202601.ccmxpf_linktable
      WHERE linktype IN ('LC', 'LU')
        AND linkprim IN ('P', 'C')
        AND usedflag = 1
  ),
  dec_me AS (
      -- December ME per (permno, calendar year). CRSP msf is in thousands
      -- of dollars (shrout in thousands, prc in $). me_dec_thousands = abs(prc) * shrout.
      SELECT permno,
             toYear(toDate32OrNull(date)) AS cyear,
             abs(prc) * shrout AS me_dec_thousands
      FROM crsp_202601.msf
      WHERE toMonth(toDate32OrNull(date)) = 12
        AND prc IS NOT NULL
        AND shrout IS NOT NULL
        AND shrout > 0
  )
SELECT l.permno                          AS permno,
       b.fyear                           AS fyear,
       -- BM = (be in millions * 1e6) / (me_dec_thousands * 1000)
       --    = (be / me_dec_thousands) * 1000
       -- Compustat be is in millions; CRSP mcap is in thousands of dollars.
       -- To get BM in consistent units, multiply numerator by 1e6 and
       -- denominator by 1000 (yielding BM = be / me_dec_thousands * 1000).
       (b.be * 1000000.0) / nullIf(d.me_dec_thousands * 1000.0, 0) AS bm
FROM book_equity AS b
INNER JOIN link AS l
    ON b.gvkey = l.gvkey
LEFT JOIN dec_me AS d
    ON l.permno = d.permno
   AND b.fyear = d.cyear - 1       -- fyear Y pairs with Dec of Y-1 ME
WHERE b.be IS NOT NULL
  AND b.be > 0
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
