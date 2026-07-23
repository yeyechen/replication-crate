-- issuance_split_adjusted.sql
-- Purpose: Split-adjusted Compustat common shares outstanding (csho) at each
--          fiscal year-end, for the Table I ISSUANCE refinement (Assumption 8).
--          Attaches CRSP's CUMULATIVE SHARE-ADJUSTMENT FACTOR cfacshr at each
--          firm's fiscal-year-end datadate (by permno, via the SAME PIT
--          CRSP-Compustat link the foundation uses) so that mechanical stock
--          splits are removed:  split_adj_shares = csho * cfacshr.
--          The 5-year ISSUANCE is then split_adj_shares(FY t-1)/split_adj_shares(FY t-5) - 1,
--          computed downstream in src/table_1.py (the cfacshr base level cancels
--          in the ratio; only its change over the 5-year window matters).
-- Tables: comp_202601.funda, crsp_202601.ccmxpf_linktable, crsp_202601.msf
-- Output columns: gvkey, fyear, datadate, csho, permno, cfacshr
-- Depends on: (none)
--
-- VERIFIED CONVENTION (permno 10032 = gvkey 012945, 2:1 splits 1997-08-29 & 2000-09-29):
--   on a 2:1 split shrout DOUBLES while cfacshr HALVES, keeping shrout*cfacshr
--   CONTINUOUS (7246*4.0 = 28984 -> 14492*2.0 = 28984; the 2000 split's raw 2.01x
--   shrout jump becomes a ~0.7% genuine change after adjustment). So multiplying
--   shares by cfacshr REMOVES splits (cfacshr is not a divisor here).
--
-- Notes:
--   * funda de-duplication is IDENTICAL to comp_fundamentals.sql (Assumption 3):
--     indfmt='INDL', consol='C', datafmt='STD', popsrc='D'; one row per (gvkey,fyear)
--     keeping non-null-at then latest datadate. Only csho>0 rows are kept (ISSUANCE
--     needs positive shares in both years).
--   * Link filter is IDENTICAL to crsp_comp_link.sql (foundation PIT link):
--     linkprim='P', linktype IN ('LU','LC'), usedflag=1. The gvkey->permno link is
--     taken point-in-time at the fiscal-year-end datadate (linkdt<=datadate<=linkenddt),
--     dedup to the latest linkdt if several permnos are valid that day.
--   * cfacshr is attached by matching the msf record of the datadate's CALENDAR MONTH
--     (substring(date,1,7) = substring(datadate,1,7)). cfacshr changes only at split
--     events, and the ISSUANCE statistic is a 5-year RATIO, so the exact intra-month
--     timing is immaterial. cfacshr<=0 / NULL rows are excluded (0 is a liquidation/
--     missing sentinel); a missing factor leaves split_adj_shares NULL.
--   * DATES ARE ISO STRINGS (pre-1970 -> cannot use toDate()).
SELECT
    fl.gvkey     AS gvkey,
    fl.fyear     AS fyear,
    fl.datadate  AS datadate,
    fl.csho      AS csho,
    fl.permno    AS permno,
    m.cfacshr    AS cfacshr
FROM (
    SELECT gvkey, fyear, datadate, csho, permno
    FROM (
        SELECT
            f.gvkey AS gvkey,
            f.fyear AS fyear,
            f.datadate AS datadate,
            f.csho AS csho,
            toInt32(l.lpermno) AS permno,
            row_number() OVER (
                PARTITION BY f.gvkey, f.fyear
                ORDER BY l.linkdt DESC
            ) AS rn_link
        FROM (
            SELECT gvkey, fyear, datadate, csho
            FROM (
                SELECT
                    ff.gvkey AS gvkey, ff.fyear AS fyear,
                    ff.datadate AS datadate, ff.csho AS csho,
                    row_number() OVER (
                        PARTITION BY ff.gvkey, ff.fyear
                        ORDER BY isNull(ff.at) ASC, ff.datadate DESC
                    ) AS rn
                FROM comp_202601.funda AS ff
                WHERE ff.indfmt = 'INDL'
                  AND ff.consol = 'C'
                  AND ff.datafmt = 'STD'
                  AND ff.popsrc = 'D'
                  AND ff.fyear >= 1960 AND ff.fyear <= 2003
                  AND ff.gvkey IS NOT NULL
                  AND ff.datadate IS NOT NULL
                  AND ff.csho > 0
            )
            WHERE rn = 1
        ) AS f
        INNER JOIN (
            SELECT gvkey, lpermno, linkdt,
                   if(linkenddt IS NULL, '2099-12-31', linkenddt) AS linkenddt
            FROM crsp_202601.ccmxpf_linktable
            WHERE linkprim = 'P'
              AND linktype IN ('LU', 'LC')
              AND usedflag = 1
              AND lpermno IS NOT NULL
              AND gvkey IS NOT NULL
              AND linkdt IS NOT NULL
        ) AS l
            ON f.gvkey = l.gvkey
           AND f.datadate >= l.linkdt
           AND f.datadate <= l.linkenddt
    )
    WHERE rn_link = 1
) AS fl
LEFT JOIN (
    SELECT permno, substring(date, 1, 7) AS ym, cfacshr
    FROM crsp_202601.msf
    WHERE permno IS NOT NULL
      AND cfacshr IS NOT NULL
      AND cfacshr > 0
) AS m
    ON m.permno = fl.permno
   AND m.ym = substring(fl.datadate, 1, 7)
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 900,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
