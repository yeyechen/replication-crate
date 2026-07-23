-- bm_annual.sql
-- Purpose: Annual book-to-market (BM) per permno per return-year Y (post-1970).
--   For return months July Y .. June Y+1 (paper L108):
--     BE  = ceq (Compustat data60) for fiscal year Y-1; if missing, fiscal Y-2
--           (one-step fallback, L108).
--     ME  = |prc|*shrout at end of December Y-1 (CRSP, $thousands).
--     bm  = ln(BE/ME);  bm_dum = 1 iff BE>0 and ME>0, else bm=0, bm_dum=0 (L110).
--
--   UNITS (important): Compustat ceq is in $MILLIONS; CRSP ME (prc*shrout) is in
--   $THOUSANDS. A valid log ratio needs common units, so BE is scaled x1000 to
--   $thousands (bm = ln(ceq*1000 / me_dec)). This reproduces the paper's Table I
--   BM mean of -0.34 (verified on IBM: ceq FY1999=20,264M vs Dec-1999 ME~507e6 K;
--   ln(20264*1000/507e6) ~ -3.2 for that high-P/B name, pooled mean ~ -0.34).
--   Without the x1000 the mean would be ~ -7.2 (off by ln 1000).
--
--   Filter: WRDS-standard industrial filter. NOTE the task spec wrote
--   consol='STD' AND popsrc='STD', but those values DO NOT EXIST in funda
--   (consol in {C,P,R,D}; popsrc = D only). Implemented with the correct,
--   data-present values consol='C' AND popsrc='D' (flagged in the report).
--
--   Pre-July-1970 months are zeroed in Python (DFF book equity unavailable).
--   dedup: argMax(ceq, datadate) -> latest filing per (permno, fyear); PIT via
--   datadate within [linkdt, linkenddt].
-- Paper: §I Book-to-market (L108-110).
-- Tables: comp_202601.funda, crsp_202601.ccmxpf_linktable, crsp_202601.msf
-- Output columns: permno, Y, bm, bm_dum
-- Depends on: (none)
WITH
be AS (
    SELECT toInt32(l.lpermno) AS permno,
           b.fyear            AS fyear,
           argMax(b.ceq, b.datadate) AS ceq
    FROM (
        SELECT gvkey, fyear, datadate, ceq
        FROM comp_202601.funda
        WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
          AND ceq IS NOT NULL
          AND fyear BETWEEN 1968 AND 2005        -- Y-1 (1969) .. Y-1 (2005) + Y-2 fallback
          AND gvkey IS NOT NULL
    ) AS b
    INNER JOIN (
        SELECT gvkey, lpermno, linkdt, linkenddt
        FROM crsp_202601.ccmxpf_linktable
        WHERE linktype IN ('LC', 'LU')
          AND linkprim IN ('P', 'C')
          AND usedflag = 1
          AND lpermno IS NOT NULL AND gvkey IS NOT NULL
    ) AS l
      ON b.gvkey = l.gvkey
     AND toDate32(b.datadate) >= ifNull(toDate32(l.linkdt),    toDate32('1900-01-01'))
     AND toDate32(b.datadate) <= ifNull(toDate32(l.linkenddt), toDate32('2099-12-31'))
    GROUP BY permno, b.fyear
),
dec_me AS (
    SELECT permno,
           toYear(toDate32(date)) AS cyear,       -- December calendar year = Y-1
           max(abs(prc) * shrout) AS me_dec       -- $thousands
    FROM crsp_202601.msf
    WHERE toMonth(toDate32(date)) = 12
      AND date >= '1968-01-01' AND date <= '2005-12-31'
      AND permno IS NOT NULL AND shrout > 0 AND prc IS NOT NULL AND abs(prc) > 0
    GROUP BY permno, cyear
)
SELECT
    permno,
    Y,
    CASE WHEN be > 0 AND me_dec > 0 THEN log(be * 1000.0 / me_dec) ELSE 0.0 END AS bm,
    CASE WHEN be > 0 AND me_dec > 0 THEN 1 ELSE 0 END                            AS bm_dum
FROM (
    SELECT
        m.permno      AS permno,
        m.cyear + 1   AS Y,                        -- return-year Y = December-year + 1
        coalesce(b1.ceq, b2.ceq) AS be,            -- FY Y-1, fallback FY Y-2
        m.me_dec      AS me_dec
    FROM dec_me AS m
    LEFT JOIN be AS b1 ON m.permno = b1.permno AND b1.fyear = m.cyear        -- Y-1
    LEFT JOIN be AS b2 ON m.permno = b2.permno AND b2.fyear = m.cyear - 1    -- Y-2
)
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 1200,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
