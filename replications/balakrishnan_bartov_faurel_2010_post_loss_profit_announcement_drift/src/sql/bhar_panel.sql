-- bhar_panel.sql
-- For each (gvkey, rdq) firm-quarter, compute BHAR over [-2,0], [1,60],
-- and [1,120] windows. SAR variant uses CRSP size-decile equal-weighted
-- daily return (erdport1.decret) as the daily expected-return benchmark.

WITH
panel AS (
    SELECT c.gvkey, c.datadate, c.rdq, l.lpermno AS permno, c.ibq, c.atq
    FROM comp_202601.fundq c
    INNER JOIN (
        SELECT gvkey AS gvkey_l, lpermno, linkdt, linkenddt
        FROM crsp_202601.ccmxpf_linktable
        WHERE linktype IN ('LC', 'LU')
          AND linkprim IN ('P', 'C')
          AND usedflag = 1
    ) l ON l.gvkey_l = c.gvkey
    WHERE c.rdq BETWEEN '1976-01-01' AND '2005-12-31'
      AND c.ibq IS NOT NULL AND c.atq IS NOT NULL AND c.rdq IS NOT NULL
      AND toDate32(c.rdq) >= toDate32(l.linkdt)
      AND coalesce(nullIf(l.linkenddt, ''), '2099-12-31') >= c.rdq
),
daily_m20 AS (
    SELECT p.gvkey, p.rdq,
        exp(sum(log(coalesce(nullIf(1 + d.ret, 0), 1)))) - 1 AS raw_m20,
        exp(sum(log(coalesce(nullIf(1 + e.decret, 0), 1)))) - 1 AS bench_m20,
        countIf(d.ret IS NOT NULL) AS n_m20
    FROM panel p
    INNER JOIN crsp_202601.dsf d
        ON d.permno = p.permno
       AND toDate32OrNull(d.date) >= addDays(toDate32(p.rdq), -3)
       AND toDate32OrNull(d.date) <= toDate32(p.rdq)
       AND d.ret IS NOT NULL AND d.ret > -1.0
    INNER JOIN crsp_202601.erdport1 e
        ON e.permno = d.permno AND e.date = d.date
    GROUP BY p.gvkey, p.rdq
),
daily_60 AS (
    SELECT p.gvkey, p.rdq,
        exp(sum(log(coalesce(nullIf(1 + d.ret, 0), 1)))) - 1 AS raw_60,
        exp(sum(log(coalesce(nullIf(1 + e.decret, 0), 1)))) - 1 AS bench_60,
        countIf(d.ret IS NOT NULL) AS n_60
    FROM panel p
    INNER JOIN crsp_202601.dsf d
        ON d.permno = p.permno
       AND toDate32OrNull(d.date) > toDate32(p.rdq)
       AND toDate32OrNull(d.date) <= addDays(toDate32(p.rdq), 252)
       AND d.ret IS NOT NULL AND d.ret > -1.0
    INNER JOIN crsp_202601.erdport1 e
        ON e.permno = d.permno AND e.date = d.date
    GROUP BY p.gvkey, p.rdq
),
daily_120 AS (
    SELECT p.gvkey, p.rdq,
        exp(sum(log(coalesce(nullIf(1 + d.ret, 0), 1)))) - 1 AS raw_120,
        exp(sum(log(coalesce(nullIf(1 + e.decret, 0), 1)))) - 1 AS bench_120,
        countIf(d.ret IS NOT NULL) AS n_120
    FROM panel p
    INNER JOIN crsp_202601.dsf d
        ON d.permno = p.permno
       AND toDate32OrNull(d.date) > toDate32(p.rdq)
       AND toDate32OrNull(d.date) <= addDays(toDate32(p.rdq), 504)
       AND d.ret IS NOT NULL AND d.ret > -1.0
    INNER JOIN crsp_202601.erdport1 e
        ON e.permno = d.permno AND e.date = d.date
    GROUP BY p.gvkey, p.rdq
)
SELECT
    p.gvkey, p.datadate, p.rdq, p.permno, p.ibq, p.atq,
    p.ibq / nullIf(p.atq, 0)                       AS earnings_at,
    COALESCE(m.raw_m20,  0) - COALESCE(m.bench_m20,  0) AS bhar_m20,
    COALESCE(s.raw_60,   0) - COALESCE(s.bench_60,   0) AS bhar_60,
    COALESCE(x.raw_120,  0) - COALESCE(x.bench_120,  0) AS bhar_120,
    COALESCE(m.n_m20,    0)                       AS n_days_m20,
    COALESCE(s.n_60,     0)                       AS n_days_60,
    COALESCE(x.n_120,    0)                       AS n_days_120
FROM panel p
LEFT JOIN daily_m20 m ON m.gvkey = p.gvkey AND m.rdq = p.rdq
LEFT JOIN daily_60  s ON s.gvkey = p.gvkey AND s.rdq = p.rdq
LEFT JOIN daily_120 x ON x.gvkey = p.gvkey AND x.rdq = p.rdq