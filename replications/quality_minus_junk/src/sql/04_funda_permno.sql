-- 04_funda_permno.sql
-- Purpose: merge Compustat annual fundamentals to CRSP permnos via the
--          point-in-time CCM link (Step 2/3 merge). PIT condition:
--          linkdt <= datadate AND (linkenddt >= datadate OR linkenddt
--          IS NULL — encoded as 2099-12-31 in qmj_link). Explicit column
--          list (no alias.* — ClickHouse would keep the qualifier as part
--          of the output column name).
-- Tables: write_yeye.qmj_funda, write_yeye.qmj_link
-- Output: write_yeye.qmj_funda_permno — permno + all qmj_funda columns,
--         one row per (permno, datadate) unless a gvkey has concurrent
--         links (rare; duplicates monitored by main.py)
-- Depends on: 02_funda_annual.sql, 03_ccm_link.sql

CREATE OR REPLACE TABLE write_yeye.qmj_funda_permno
ENGINE = MergeTree ORDER BY (permno, datadate) AS
SELECT
    l.permno   AS permno,
    f.gvkey    AS gvkey,
    f.datadate AS datadate,
    f.fyear    AS fyear,
    f.revt     AS revt,
    f.cogs     AS cogs,
    f.at       AS at,
    f.ib       AS ib,
    f.dp       AS dp,
    f.act      AS act,
    f.lct      AS lct,
    f.dlc      AS dlc,
    f.dltt     AS dltt,
    f.lt       AS lt,
    f.sale     AS sale,
    f.pi       AS pi,
    f.re       AS re,
    f.ebit     AS ebit,
    f.prcc_f   AS prcc_f,
    f.csho     AS csho,
    f.pstk     AS pstk,
    f.wc       AS wc,
    f.be       AS be,
    f.gp       AS gp,
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
    f.oeneg    AS oeneg,
    f.intwo    AS intwo,
    f.chin     AS chin,
    f.evol_a   AS evol_a
FROM write_yeye.qmj_funda AS f
INNER JOIN write_yeye.qmj_link AS l
    ON f.gvkey = l.gvkey
WHERE l.linkdt <= f.datadate
  AND f.datadate <= l.linkenddt
SETTINGS allow_experimental_analyzer = 0,
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
