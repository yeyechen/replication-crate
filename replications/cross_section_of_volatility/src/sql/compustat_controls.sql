-- compustat_controls.sql
-- Purpose: Book-to-market (BM) and leverage (total assets / book equity)
--   per (permno, month) via Compustat funda + CRSP-Compustat link +
--   December market equity. One row per (permno, month) that has a valid
--   link and book equity.
-- Tables: comp_202601.funda, crsp_202601.ccmxpf_linktable,
--         crsp_202601.msf, crsp_202601.dsenames
-- Output columns: permno, month, be, at, me_dec_million, bm, leverage
-- Depends on: (none)
-- Conventions:
--   * Compustat filter (A11): indfmt='INDL', consol='C', popsrc='D',
--     datafmt='STD'; dedup by (gvkey, fyear) keeping latest datadate.
--   * Book equity cascade (task + A5):
--       ceq + coalesce(txdb,0) - coalesce(pstkrv,0)   if ceq present
--       at - dlc - dltt - coalesce(pstkrv,0)           elif at,dlc,dltt
--       seq                                            elif seq
--   * FF June-rebalance mapping (no look-ahead): for month in year Y,
--       fyear_used = Y-1 if month>=July else Y-2
--     BM = BE(fyear_used) / ME_dec(year fyear_used); leverage = AT/BE.
--     Both require BE > 0 (A5), else NULL.
--   * Link (FF recommended): linktype IN (LC,LU), linkprim IN (P,C),
--     usedflag=1, point-in-time valid at the month.
--   * me in $ millions (abs(prc)*shrout/1000); Compustat be/at already in
--     $ millions, so BM and leverage are unit-free ratios.

WITH
    msf_spine AS (
        SELECT DISTINCT
            m.permno                                        AS permno,
            toDate32(date_trunc('month', toDate32(m.date))) AS month
        FROM crsp_202601.msf AS m
        INNER JOIN crsp_202601.dsenames AS n
            ON m.permno = n.permno
           AND m.date >= n.namedt
           AND m.date <= ifNull(n.nameendt, '2099-12-31')
        WHERE n.shrcd IN (10, 11)
          AND n.exchcd IN (1, 2, 3)
          AND m.ret IS NOT NULL
          AND m.ret > -1.0
          AND m.date BETWEEN '1963-06-01' AND '2000-12-31'
    ),
    be_raw AS (
        SELECT
            gvkey,
            toUInt32(fyear)                                 AS fyear,
            CASE
                WHEN ceq IS NOT NULL
                    THEN coalesce(ceq, 0) + coalesce(txdb, 0) - coalesce(pstkrv, 0)
                WHEN at IS NOT NULL AND dlc IS NOT NULL AND dltt IS NOT NULL
                    THEN at - dlc - dltt - coalesce(pstkrv, 0)
                WHEN seq IS NOT NULL
                    THEN seq
                ELSE NULL
            END                                             AS be,
            toFloat64(at)                                   AS at,
            row_number() OVER (PARTITION BY gvkey, fyear
                               ORDER BY datadate DESC)      AS rn
        FROM comp_202601.funda
        WHERE indfmt = 'INDL'
          AND consol = 'C'
          AND popsrc = 'D'
          AND datafmt = 'STD'
          AND fyear IS NOT NULL
          AND fyear BETWEEN 1960 AND 2000
    ),
    be AS (
        SELECT gvkey, fyear, be, at FROM be_raw WHERE rn = 1
    ),
    link AS (
        SELECT
            toInt32(lpermno)                                AS permno,
            gvkey,
            linkdt,
            linkenddt
        FROM crsp_202601.ccmxpf_linktable
        WHERE linktype IN ('LC', 'LU')
          AND linkprim IN ('P', 'C')
          AND usedflag = 1
    ),
    dec_me AS (
        SELECT
            ms.permno                                       AS permno,
            toUInt32(toYear(toDate32(ms.date)))             AS cyear,
            abs(toFloat64(ms.prc)) * toFloat64(ms.shrout) / 1000.0 AS me_dec_million
        FROM crsp_202601.msf AS ms
        INNER JOIN crsp_202601.dsenames AS nn
            ON ms.permno = nn.permno
           AND ms.date >= nn.namedt
           AND ms.date <= ifNull(nn.nameendt, '2099-12-31')
        WHERE nn.shrcd IN (10, 11)
          AND nn.exchcd IN (1, 2, 3)
          AND toMonth(toDate32(ms.date)) = 12
          AND ms.date BETWEEN '1962-01-01' AND '2000-12-31'
    )
SELECT
    s.permno                                                AS permno,
    s.month                                                 AS month,
    b.be                                                    AS be,
    b.at                                                    AS at,
    dm.me_dec_million                                       AS me_dec_million,
    if(b.be > 0, b.be / nullIf(dm.me_dec_million, 0), NULL) AS bm,
    if(b.be > 0, b.at / nullIf(b.be, 0), NULL)              AS leverage
FROM msf_spine AS s
INNER JOIN link AS l
    ON s.permno = l.permno
   AND toDate32(s.month) >= toDate32(l.linkdt)
   AND toDate32(s.month) <= toDate32(ifNull(l.linkenddt, '2099-12-31'))
INNER JOIN be AS b
    ON l.gvkey = b.gvkey
   AND (toYear(s.month) - 1 - if(toMonth(s.month) < 7, 1, 0)) = b.fyear
LEFT JOIN dec_me AS dm
    ON s.permno = dm.permno
   AND (toYear(s.month) - 1 - if(toMonth(s.month) < 7, 1, 0)) = dm.cyear
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 900,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
