-- 08_funda_enriched.sql
-- Purpose: enrich permno-level annual fundamentals with (a) market equity
--          at the fiscal year-end (ASOF to raw CRSP msf month of datadate),
--          (b) EVOL = quarterly ROE volatility ASOF to the fiscal date with
--          the annual 5-yr fallback (paper rule), and (c) compute the two
--          ME-dependent safety measures:
--          * O-Score (Ohlson 1980, paper Appendix 1):
--            ADJASSET = AT + 0.1*(ME - BE); TLTA = (DLC+DLTT)/ADJASSET;
--            WCTA = (ACT-LCT)/ADJASSET; CLCA = LCT/ACT; OENEG = 1(LT>AT);
--            NITA = IB/AT; FUTL = PI/LT; INTWO, CHIN from 02.
--            oscore = -(logit), so higher = safer (paper sign convention).
--            CPI is normalized to 1.0 per the task spec: log(ADJASSET/CPI)
--            with a time-constant CPI only shifts the cross-section by a
--            month-constant, which is exactly invariant to the monthly
--            rank z-scoring applied downstream (so CPI level is
--            immaterial for this replication). ADJASSET <= 0 -> NULL.
--          * Z-Score (Altman): Z = (1.2*WC + 1.4*RE + 3.3*EBIT + 0.6*ME
--            + SALE)/AT. Units: Compustat items are $millions, CRSP ME is
--            $ -> ME divided by 1e6 to $millions. Higher = safer.
--          Explicit column lists throughout (no alias.*).
-- Tables: write_yeye.qmj_funda_permno, write_yeye.qmj_evol,
--         crsp_202601.msf (raw, for fiscal-date ME regardless of universe
--         membership)
-- Output: write_yeye.qmj_fp_enrich — qmj_funda_permno columns + me_m
--         ($millions at fiscal date), evol, adjasset, oscore, zscore
-- Depends on: 04_funda_permno.sql, 07_evol_quarterly.sql

CREATE OR REPLACE TABLE write_yeye.qmj_fp_enrich
ENGINE = MergeTree ORDER BY (permno, datadate) AS
WITH
me_src AS (
    SELECT
        assumeNotNull(permno)        AS permno,
        subtractDays(toDate32(date), toDayOfMonth(toDate32(date)) - 1) AS month,
        if(prc IS NULL OR prc = 0 OR shrout IS NULL,
           NULL,
           abs(prc) * shrout * 1000) AS mcap
    FROM crsp_202601.msf
    WHERE date >= '1951-01-01' AND date <= '2017-01-31'
      AND permno IS NOT NULL AND date IS NOT NULL
),
fme AS (
    SELECT
        f.permno   AS permno,
        f.gvkey    AS gvkey,
        f.datadate AS datadate,
        f.fyear    AS fyear,
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
        f.wc       AS wc,
        f.be       AS be,
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
        f.evol_a   AS evol_a,
        m.mcap / 1000000 AS me_m   -- $millions, matching Compustat units
    FROM write_yeye.qmj_funda_permno AS f
    ASOF LEFT JOIN me_src AS m
        ON f.permno = m.permno
       AND m.month <= subtractDays(f.datadate, toDayOfMonth(f.datadate) - 1)
)
SELECT
    f.permno   AS permno,
    f.gvkey    AS gvkey,
    f.datadate AS datadate,
    f.fyear    AS fyear,
    f.at       AS at,
    f.ib       AS ib,
    f.act      AS act,
    f.lct      AS lct,
    f.sale     AS sale,
    f.re       AS re,
    f.ebit     AS ebit,
    f.wc       AS wc,
    f.be       AS be,
    f.me_m     AS me_m,
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
    coalesce(e.evol, f.evol_a) AS evol,
    -- adjusted assets (O-Score)
    f.at + 0.1 * (f.me_m - f.be) AS adjasset,
    -- O-Score: minus the Ohlson logit (higher = safer)
    if(f.at + 0.1 * (f.me_m - f.be) > 0,
       -(
           -1.32
           - 0.407 * log(f.at + 0.1 * (f.me_m - f.be))
           + 6.03  * ((coalesce(f.dlc, 0) + f.dltt)
                      / nullIf(f.at + 0.1 * (f.me_m - f.be), 0))
           - 1.43  * ((f.act - f.lct)
                      / nullIf(f.at + 0.1 * (f.me_m - f.be), 0))
           + 0.076 * (f.lct / nullIf(f.act, 0))
           - 1.72  * f.oeneg
           - 2.37  * (f.ib / nullIf(f.at, 0))
           - 1.83  * (f.pi / nullIf(f.lt, 0))
           + 0.285 * f.intwo
           - 0.521 * f.chin
       ),
       NULL) AS oscore,
    -- Altman Z-Score (ME in $millions); higher = safer
    (1.2 * f.wc + 1.4 * f.re + 3.3 * f.ebit + 0.6 * f.me_m + f.sale)
        / nullIf(f.at, 0) AS zscore
FROM fme AS f
ASOF LEFT JOIN write_yeye.qmj_evol AS e
    ON f.gvkey = e.gvkey
   AND e.datadate <= f.datadate
SETTINGS allow_experimental_analyzer = 0,
         join_algorithm = 'hash',   -- required for ASOF joins on this server
         max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
