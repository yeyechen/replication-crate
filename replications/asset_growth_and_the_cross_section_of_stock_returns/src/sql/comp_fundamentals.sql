-- comp_fundamentals.sql
-- Purpose: Deduplicated Compustat annual fundamentals, ONE row per (gvkey, fyear),
--          plus the firm's earliest Compustat appearance (first_datadate) for the
--          2-year backfill filter.
-- Tables: comp_202601.funda
-- Output columns: gvkey, fyear, datadate, first_datadate, sich, and all data items
--                 needed for ASSETG and the control / decomposition variables.
-- Depends on: (none)
-- Notes:
--   * DATES ARE RETURNED AS ISO STRINGS (YYYY-MM-DD). ClickHouse `Date` clamps
--     anything before 1970-01-01 to the Unix epoch, and this sample starts in the
--     early 1960s — so we keep datadate as a string (ISO strings sort
--     chronologically) and parse dates in Python.
--   * Standard WRDS industrial filter applied (Assumption 3): indfmt='INDL',
--     consol='C', datafmt='STD', popsrc='D'. Verified empirically that NO gvkey
--     has only SUMM_STD rows (0 gvkeys), so datafmt='STD' drops no firms.
--   * funda has up to 4 rows per (gvkey,fyear) even after the filter; dedup with
--     ROW_NUMBER keeping the non-null-at row, then the latest datadate (Assumption 3).
--   * first_datadate = min datadate over ALL funda rows for the gvkey (first
--     Compustat appearance, any format) — used for the 2-year backfill filter.
--   * at/sale/etc. are in $MILLIONS; csho in MILLIONS of shares; prcc_f in $.
WITH filtered AS (
    SELECT
        gvkey,
        fyear,
        datadate,
        sich,
        at, sale, ceq, seq, txdb, pstkrv, pstkl, pstk,
        act, ch, lct, dlc, dltt, dp, txp, capx, oibdp,
        csho, prcc_f, ppegt, ppent, re, mib, recta, ivao, che, lt,
        epspx, epsfi
    FROM comp_202601.funda
    WHERE indfmt = 'INDL'
      AND consol = 'C'
      AND datafmt = 'STD'
      AND popsrc = 'D'
      AND fyear >= 1960 AND fyear <= 2003
      AND gvkey IS NOT NULL
      AND datadate IS NOT NULL
),
first_dd AS (
    SELECT gvkey, min(datadate) AS first_datadate
    FROM comp_202601.funda
    WHERE gvkey IS NOT NULL AND datadate IS NOT NULL
    GROUP BY gvkey
),
ranked AS (
    SELECT
        f.*,
        row_number() OVER (
            PARTITION BY f.gvkey, f.fyear
            ORDER BY isNull(f.at) ASC, f.datadate DESC
        ) AS rn
    FROM filtered AS f
)
SELECT
    r.gvkey,
    r.fyear,
    r.datadate,
    fd.first_datadate,
    r.sich,
    r.at, r.sale, r.ceq, r.seq, r.txdb, r.pstkrv, r.pstkl, r.pstk,
    r.act, r.ch, r.lct, r.dlc, r.dltt, r.dp, r.txp, r.capx, r.oibdp,
    r.csho, r.prcc_f, r.ppegt, r.ppent, r.re, r.mib, r.recta, r.ivao, r.che, r.lt,
    r.epspx, r.epsfi
FROM ranked AS r
LEFT JOIN first_dd AS fd ON r.gvkey = fd.gvkey
WHERE r.rn = 1
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
