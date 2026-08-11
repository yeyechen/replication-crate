-- panel.sql
-- Purpose: Build the final analysis-ready firm-quarter panel for BBF (2009).
--          Steps:
--            1) Compustat firm-quarters in 1976-2005 with ibq/atq/rdq non-null
--            2) Self-join to attach epspxq at q-12 (12 quarters prior) and
--               atq at q-1 (1 quarter prior) — needed for SUE history check
--               and accruals sample, respectively.
--            3) PIT linktable join to attach the CRSP permno valid on rdq.
--            4) Window-join to CRSP daily (dsf) to attach price 5 trading
--               days prior to rdq (rn=5 over a 14-calendar-day look-back).
--            5) Output the firm-quarter panel with all needed columns and
--               supplementary flags set.
--
-- Tables: comp_202601.fundq, crsp_202601.ccmxpf_linktable, crsp_202601.dsf
-- Output columns: gvkey, datadate, rdq, fyearq, fqtr, ibq, atq,
--                 epspxq, ceqq, cshoq, prccq, oancfy, xidocy,
--                 epspxq_q12, atq_q1, permno, prc_5d_prior
-- Depends on: comp_fundamentals.sql, ccm_link.sql (conceptually)
-- Settings: join_algorithm=partial_merge, max_execution_time=600
--
-- Notes:
--   * The 14-calendar-day look-back window for the price-5-trading-days-prior
--     filter covers ~10 trading days, comfortably exceeding 5 even across
--     long holiday gaps. ROW_NUMBER ranks trading days descending by date
--     and keeps the 5th-from-last trading day strictly before rdq.
--   * epspxq_q12 / atq_q1 are LEFT JOINed — NULL means "the matching prior
--     row was not found" (firm's fiscal history too short, or atq/epspxq
--     missing for that quarter). Downstream Python applies the supplementary
--     filters against these flags.
--   * SUE simplification: the paper requires 13 CONSECUTIVE quarters of
--     epspxq (q-12 through q). Per the task spec, we approximate this as
--     "epspxq non-missing at q AND at q-12" (a strictly weaker condition).
--   * dsf.prc can be negative (bid/ask averages) — take abs() before using
--     as a price level.
--   * Implemented as nested subqueries (rather than a CTE chain) because
--     ClickHouse's analyzer has trouble propagating column names through a
--     chain of CTEs when the leaf CTE carries a ROW_NUMBER() OVER (see DEV
--     notes in the file). Functionally identical to the CTE form.

SELECT
    gvkey, datadate, rdq, fyearq, fqtr,
    ibq, atq, epspxq, ceqq, cshoq, prccq, oancfy, xidocy,
    epspxq_q12, atq_q1, permno, prc_5d_prior
FROM (
    SELECT
        c.gvkey AS gvkey,
        c.datadate AS datadate,
        c.rdq AS rdq,
        c.fyearq AS fyearq,
        c.fqtr AS fqtr,
        c.ibq AS ibq,
        c.atq AS atq,
        c.epspxq AS epspxq,
        c.ceqq AS ceqq,
        c.cshoq AS cshoq,
        c.prccq AS prccq,
        c.oancfy AS oancfy,
        c.xidocy AS xidocy,
        c.epspxq_q12 AS epspxq_q12,
        c.atq_q1 AS atq_q1,
        c.permno AS permno,
        d.prc AS prc_5d_prior,
        ROW_NUMBER() OVER (
            PARTITION BY c.gvkey, c.datadate, c.rdq
            ORDER BY d.date DESC
        ) AS rn
    FROM (
        SELECT
            c.gvkey, c.datadate, c.rdq, c.fyearq, c.fqtr,
            c.ibq, c.atq, c.epspxq, c.ceqq, c.cshoq, c.prccq,
            c.oancfy, c.xidocy,
            c.epspxq_q12, c.atq_q1,
            any(toInt32(l.lpermno)) AS permno
        FROM (
            SELECT
                c.gvkey, c.datadate, c.rdq, c.fyearq, c.fqtr,
                c.ibq, c.atq, c.epspxq, c.ceqq, c.cshoq, c.prccq,
                c.oancfy, c.xidocy,
                q12.epspxq AS epspxq_q12,
                q1.atq AS atq_q1
            FROM comp_202601.fundq AS c
            LEFT JOIN comp_202601.fundq AS q12
                ON c.gvkey = q12.gvkey
               AND c.fyearq - 3 = q12.fyearq
               AND c.fqtr = q12.fqtr
            LEFT JOIN comp_202601.fundq AS q1
                ON c.gvkey = q1.gvkey
               AND ((c.fqtr = 1 AND c.fyearq - 1 = q1.fyearq AND q1.fqtr = 4)
                 OR (c.fqtr > 1 AND c.fyearq = q1.fyearq AND c.fqtr - 1 = q1.fqtr))
            WHERE c.rdq BETWEEN '1976-01-01' AND '2005-12-31'
              AND c.ibq IS NOT NULL
              AND c.atq IS NOT NULL
              AND c.rdq IS NOT NULL
        ) AS c
        INNER JOIN crsp_202601.ccmxpf_linktable AS l
            ON c.gvkey = l.gvkey
           AND toDate32OrNull(c.rdq) >= toDate32OrNull(l.linkdt)
           AND coalesce(nullIf(l.linkenddt, ''), '2099-12-31') >= c.rdq
           AND l.linktype IN ('LC', 'LU')
           AND l.usedflag = 1
           AND l.linkprim IN ('P', 'C')
           AND l.lpermno IS NOT NULL
        GROUP BY
            c.gvkey, c.datadate, c.rdq, c.fyearq, c.fqtr,
            c.ibq, c.atq, c.epspxq, c.ceqq, c.cshoq, c.prccq,
            c.oancfy, c.xidocy, c.epspxq_q12, c.atq_q1
    ) AS c
    INNER JOIN (
        SELECT
            toInt32(permno) AS permno,
            toDate32(date) AS date,
            abs(prc) AS prc
        FROM crsp_202601.dsf
        WHERE date BETWEEN '1975-12-01' AND '2006-01-15'
    ) AS d
        ON c.permno = d.permno
       AND d.date BETWEEN (toDate32(c.rdq) - INTERVAL 14 DAY)
                      AND (toDate32(c.rdq) - INTERVAL 1 DAY)
)
WHERE rn = 5
SETTINGS max_execution_time = 600
