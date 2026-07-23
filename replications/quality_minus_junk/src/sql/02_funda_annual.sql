-- 02_funda_annual.sql
-- Purpose: compute all QMJ annual measures from qmj_funda_base via
--          explicit fiscal-year self-joins (t-1, t-5, t-6) — no alias.*
--          expansion (ClickHouse keeps qualifiers in CTE column names,
--          which breaks downstream resolution):
--          Profitability: GPOA, ROE, ROA, CFOA, GMAR, ACC
--          (dWC = WC_t - WC_{t-1}; CFOA = (IB + DP - dWC - CAPX)/AT;
--           ACC = -(dWC - DP)/AT)
--          Growth (5-yr change in residual profitability; residual charge
--          rf = calendar-year sum of monthly T-bill rf from
--          ff.four_factor_monthly — rf is stored as a MONTHLY DECIMAL in
--          this instance, e.g. 0.0020, summed over 12 months = annual
--          decimal; the task spec's "/1200" note does not apply because
--          the column is already decimal; flagged for the Replicator):
--            d_gpoa = [(gp_t - rf*at_{t-1}) - (gp_{t-5} - rf*at_{t-6})]/at_{t-5}
--            d_roe  = [(ib_t - rf*be_{t-1}) - (ib_{t-5} - rf*be_{t-6})]/be_{t-5}
--            d_roa  = [(ib_t - rf*at_{t-1}) - (ib_{t-5} - rf*at_{t-6})]/at_{t-5}
--            d_cfoa = [(cf_t - rf*at_{t-1}) - (cf_{t-5} - rf*at_{t-6})]/at_{t-5}
--            d_gmar = (gp_t - gp_{t-5})/sale_{t-5}
--          Safety inputs: LEV = -(DLTT+DLC+MIBT+PSTK)/AT (dlc/mibt/pstk
--          coalesced to 0); O-Score inputs OENEG, INTWO, CHIN; EVOL
--          annual fallback = std dev of annual ROE (IB/BE) over 5 fiscal
--          years, requiring 5 nonmissing years.
-- Tables: write_yeye.qmj_funda_base, ff.four_factor_monthly
-- Output: write_yeye.qmj_funda — one row per (gvkey, fyear)
-- Depends on: 01_funda_base.sql

CREATE OR REPLACE TABLE write_yeye.qmj_funda
ENGINE = MergeTree ORDER BY (gvkey, fyear) AS
WITH
rf_ann AS (
    SELECT toYear(toDate32(dt)) AS yr, sum(rf) AS rf_y   -- monthly decimals
    FROM ff.four_factor_monthly
    WHERE dt IS NOT NULL
    GROUP BY yr
)
SELECT
    t.gvkey    AS gvkey,
    t.datadate AS datadate,
    t.fyear    AS fyear,
    t.revt     AS revt,
    t.cogs     AS cogs,
    t.at       AS at,
    t.ib       AS ib,
    t.dp       AS dp,
    t.act      AS act,
    t.lct      AS lct,
    t.dlc      AS dlc,
    t.dltt     AS dltt,
    t.lt       AS lt,
    t.sale     AS sale,
    t.pi       AS pi,
    t.re       AS re,
    t.ebit     AS ebit,
    t.prcc_f   AS prcc_f,
    t.csho     AS csho,
    t.pstk     AS pstk,
    t.wc       AS wc,
    t.be       AS be,
    t.gp       AS gp,
    -- profitability
    t.gp / nullIf(t.at, 0)  AS gpoa,
    t.ib / nullIf(t.be, 0)  AS roe,
    t.ib / nullIf(t.at, 0)  AS roa,
    (t.ib + t.dp - (t.wc - l1.wc) - t.capx) / nullIf(t.at, 0) AS cfoa,
    t.gp / nullIf(t.sale, 0) AS gmar,
    -((t.wc - l1.wc) - t.dp) / nullIf(t.at, 0) AS acc,
    -- growth in residual profitability
    ((t.gp - coalesce(r5.rf_y, 0.0) * l1.at)
        - (l5.gp - coalesce(r6.rf_y, 0.0) * l6.at))
        / nullIf(l5.at, 0) AS d_gpoa,
    ((t.ib - coalesce(r5.rf_y, 0.0) * l1.be)
        - (l5.ib - coalesce(r6.rf_y, 0.0) * l6.be))
        / nullIf(l5.be, 0) AS d_roe,
    ((t.ib - coalesce(r5.rf_y, 0.0) * l1.at)
        - (l5.ib - coalesce(r6.rf_y, 0.0) * l6.at))
        / nullIf(l5.at, 0) AS d_roa,
    (((t.ib + t.dp - (t.wc - l1.wc) - t.capx)
        - coalesce(r5.rf_y, 0.0) * l1.at)
     - ((l5.ib + l5.dp - (l5.wc - l6.wc) - l5.capx)
        - coalesce(r6.rf_y, 0.0) * l6.at))
        / nullIf(l5.at, 0) AS d_cfoa,
    (t.gp - l5.gp) / nullIf(l5.sale, 0) AS d_gmar,
    -- leverage
    -(t.dltt + coalesce(t.dlc, 0) + coalesce(t.mibt, 0)
      + coalesce(t.pstk, 0)) / nullIf(t.at, 0) AS lev,
    -- O-Score inputs
    multiIf(
        t.lt > t.at, 1,
        t.lt IS NULL OR t.at IS NULL, NULL,
        0
    ) AS oeneg,
    if(t.ib IS NULL OR l1.ib IS NULL,
       NULL,
       if(greatest(t.ib, l1.ib) < 0, 1, 0)) AS intwo,
    (t.ib - l1.ib) / nullIf(abs(t.ib) + abs(l1.ib), 0) AS chin,
    -- EVOL annual fallback: std of annual ROE over 5 fiscal years,
    -- requiring 5 nonmissing years
    if(count(t.ib / nullIf(t.be, 0)) OVER w >= 5,
       stddevSamp(t.ib / nullIf(t.be, 0)) OVER w,
       NULL) AS evol_a
FROM write_yeye.qmj_funda_base AS t
LEFT JOIN write_yeye.qmj_funda_base AS l1
    ON l1.gvkey = t.gvkey AND l1.fyear = t.fyear - 1
LEFT JOIN write_yeye.qmj_funda_base AS l5
    ON l5.gvkey = t.gvkey AND l5.fyear = t.fyear - 5
LEFT JOIN write_yeye.qmj_funda_base AS l6
    ON l6.gvkey = t.gvkey AND l6.fyear = t.fyear - 6
LEFT JOIN rf_ann AS r5 ON r5.yr = t.fyear
LEFT JOIN rf_ann AS r6 ON r6.yr = t.fyear - 5
WINDOW w AS (PARTITION BY t.gvkey ORDER BY t.fyear
             ROWS BETWEEN 4 PRECEDING AND CURRENT ROW)
SETTINGS allow_experimental_analyzer = 0,
         max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
