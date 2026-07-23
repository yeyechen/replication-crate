-- earnings_announcements.sql
-- Purpose: Table IX (Jegadeesh-Titman 1993 §VIII) earnings-announcement
--          3-day returns (days -2..0) for every Compustat quarterly
--          announcement that links (point-in-time) to a CRSP permno, over the
--          rdq window 1980-02 .. 1992-12 (formations 1980-01..1989-12 + 36
--          post-formation months). The cohort filter (winner/loser decile
--          membership per formation) and the post-formation-month aggregation
--          are applied in src/main.py; this query returns one row per distinct
--          (permno, rdq) with its 3-day announcement return ret3 (NULL if the
--          3-day window is incomplete).
-- Tables: comp_202601.fundq, crsp_202601.ccmxpf_linktable, crsp_202601.dsf
-- Output columns: permno (Int32), rdq ('YYYY-MM-DD' String), ret3 (Float64,
--                 NULL if any of days -2/-1/0 has a missing/sentinel return)
-- Depends on: (none)
--
-- Construction (documented in preparations/assumptions.md P27):
--   fq   : dedupe fundq to ONE rdq per (gvkey, fyearq, fqtr) = min(rdq);
--          indfmt = 'INDL' (the paper's "quarterly industrial database";
--          verified a no-op on this vintage — 100% of rdq rows are INDL).
--   link : primary CRSP<->Compustat links: usedflag = 1,
--          linktype IN ('LU','LC','LS','LX'), lpermno non-NULL; linkenddt
--          empty-string -> '2100-01-01' so open links stay valid.
--   ann  : PIT join linkdt <= rdq <= linkenddt; dedupe to ONE gvkey per
--          (permno, rdq): prefer linkprim = 'P', then earliest linkdt
--          (row_number ORDER BY linkprim='P' DESC, linkdt ASC, rk = 1).
--   dsf3 : per (permno, trading day) the 3-day cumulative return ending that
--          day = (1+r0)(1+r-1)(1+r-2)-1 from lagInFrame over the per-permno
--          date-ordered daily series; NULL unless all 3 days have a valid
--          return (ret IS NOT NULL AND ret > -1.0) and >= 3 trading days
--          exist (cnt3 = 3). Daily returns are used as-is (ret_raw; no
--          delisting adjustment is meaningful over 3 days).
--   day0 : day 0 = the FIRST dsf trading day ON OR AFTER rdq, capped within
--          5 calendar days (else the announcement has no day0 and drops).
--          ret3 is then read off dsf3 at (permno, day0) — so days -1/-2 are
--          the two trading days immediately preceding day0 (no calendar-day
--          cap on the backward side; a trading halt just pushes them back).
-- NOTE: all dates here are 1979-12 .. 1993-01 (post-1970), so toDate() is
--       safe (no pre-1970 saturation — cf. P8). Date-range arithmetic uses
--       toDate(col) + n. Strings 'YYYY-MM-DD' compare lexicographically =
--       chronologically, so the PIT link uses raw string comparison.
WITH
fq AS
(
    -- min(rdq) aliased to min_rdq (NOT rdq) — a same-name alias would shadow
    -- the column and ClickHouse resolves later fq.rdq refs to the aggregate.
    SELECT gvkey, min(rdq) AS min_rdq
    FROM comp_202601.fundq
    WHERE rdq IS NOT NULL AND rdq <> ''
      AND indfmt = 'INDL'
      AND rdq >= '1980-02-01' AND rdq <= '1992-12-31'
    GROUP BY gvkey, fyearq, fqtr
),
link AS
(
    SELECT
        gvkey,
        toInt32(lpermno) AS permno,
        linkdt,
        coalesce(nullIf(linkenddt, ''), '2100-01-01') AS linkenddt,
        linkprim
    FROM crsp_202601.ccmxpf_linktable
    WHERE usedflag = 1
      AND linktype IN ('LU', 'LC', 'LS', 'LX')
      AND lpermno IS NOT NULL
),
ann AS
(
    SELECT permno, rdq
    FROM
    (
        SELECT
            fq.min_rdq AS rdq,
            l.permno AS permno,
            row_number() OVER (
                PARTITION BY l.permno, fq.min_rdq
                ORDER BY (CASE WHEN l.linkprim = 'P' THEN 0 ELSE 1 END) ASC,
                         l.linkdt ASC
            ) AS rk
        FROM fq
        INNER JOIN link AS l ON fq.gvkey = l.gvkey
        WHERE l.linkdt <= fq.min_rdq AND fq.min_rdq <= l.linkenddt
    )
    WHERE rk = 1
),
dsf AS
(
    SELECT permno, date, ret
    FROM crsp_202601.dsf
    WHERE date >= '1979-12-01' AND date <= '1993-01-31'
      AND permno IS NOT NULL
),
dsf3 AS
(
    SELECT
        permno,
        date,
        if(cnt3 = 3
           AND ret IS NOT NULL AND ret > -1.0
           AND r1 IS NOT NULL AND r1 > -1.0
           AND r2 IS NOT NULL AND r2 > -1.0,
           (1 + ret) * (1 + r1) * (1 + r2) - 1,
           NULL) AS ret3
    FROM
    (
        SELECT
            permno,
            date,
            ret,
            lagInFrame(ret, 1) OVER w AS r1,
            lagInFrame(ret, 2) OVER w AS r2,
            count() OVER (PARTITION BY permno ORDER BY date
                          ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS cnt3
        FROM dsf
        WINDOW w AS (PARTITION BY permno ORDER BY date
                     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
    )
),
day0 AS
(
    SELECT a.permno AS permno, a.rdq AS rdq, min(d.date) AS d0
    FROM dsf AS d
    INNER JOIN ann AS a
        ON d.permno = a.permno
       AND toDate(d.date) >= toDate(a.rdq)
       AND toDate(d.date) <= toDate(a.rdq) + 5
    GROUP BY a.permno, a.rdq
)
SELECT day0.permno AS permno, day0.rdq AS rdq, d3.ret3 AS ret3
FROM day0
INNER JOIN dsf3 AS d3
    ON d3.permno = day0.permno AND d3.date = day0.d0
SETTINGS
    join_algorithm = 'hash',
    max_execution_time = 1800,
    max_rows_to_read = 20000000000,
    timeout_before_checking_execution_speed = 0;
