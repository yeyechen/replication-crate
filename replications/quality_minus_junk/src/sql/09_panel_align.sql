-- 09_panel_align.sql
-- Purpose: Step 4 fiscal-year alignment. For each stock-month in the
--          universe grid, attach the most recent fiscal year ending at
--          least 6 months before the month: cutoff = last day of
--          (month - 6 months), ASOF join on datadate <= cutoff. This
--          implements the FF (1992) convention the paper follows
--          ("fiscal year ending anywhere in calendar year t-1 aligned to
--          June of calendar year t"): e.g. month = Jun 1958 -> cutoff
--          1957-12-31, so Dec-1957 fiscal year-ends qualify; month =
--          May 1958 -> cutoff 1957-11-30, so the latest qualifying
--          year-end is Dec 1956. (For non-December fiscal year-ends in
--          Jan-May this is marginally fresher than a strict calendar-year
--          mapping; flagged for the Replicator.)
--          Grid: universe months Jun 1957 - Jan 2017 (Jan 2017 included
--          only so the Dec 2016 row gets a next-month return; dropped in
--          10_panel_pull.sql).
-- Tables: write_yeye.qmj_univ_m, write_yeye.qmj_fp_enrich
-- Output: write_yeye.qmj_panel_raw — permno, month + aligned annual
--         measures (gpoa, roe, roa, cfoa, gmar, acc, d_gpoa, d_roe,
--         d_roa, d_cfoa, d_gmar, lev, oscore, zscore, evol, be, at,
--         me_m, datadate, fyear)
-- Depends on: 05_universe_monthly.sql, 08_funda_enriched.sql

CREATE OR REPLACE TABLE write_yeye.qmj_panel_raw
ENGINE = MergeTree ORDER BY (permno, month) AS
WITH
grid AS (
    SELECT
        permno,
        month,
        subtractDays(addMonths(month, -5), 1) AS cutoff
    FROM (
        SELECT DISTINCT permno, month
        FROM write_yeye.qmj_univ_m
        WHERE month >= toDate32('1957-06-01')
          AND month <= toDate32('2017-01-01')
    )
)
SELECT
    g.permno   AS permno,
    g.month    AS month,
    f.datadate AS datadate,
    f.fyear    AS fyear,
    f.gpoa     AS gpoa,
    f.roe      AS roe,
    f.roa      AS roa,
    f.cfoa     AS cfoa,
    f.gmar     AS gmar,
    f.acc      AS acc,
    f.d_gpoa   AS d_gpoa,
    f.d_roe    AS d_roe,
    f.d_roa    AS d_roa,
    f.d_cfoa   AS d_cfoa,
    f.d_gmar   AS d_gmar,
    f.lev      AS lev,
    f.oscore   AS oscore,
    f.zscore   AS zscore,
    f.evol     AS evol,
    f.be       AS be,
    f.at       AS at,
    f.me_m     AS me_m
FROM grid AS g
ASOF LEFT JOIN write_yeye.qmj_fp_enrich AS f
    ON g.permno = f.permno
   AND f.datadate <= g.cutoff
SETTINGS allow_experimental_analyzer = 0,
         join_algorithm = 'hash',   -- required for ASOF joins on this server
         max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
