-- 10_panel_pull.sql
-- Purpose: final panel pull into pandas (Steps 7/9/10 merge). Attaches to
--          each aligned stock-month:
--          * 60-month CAPM beta and BAB = -beta (qmj_beta)
--          * monthly return with delisting adjustment (paper L330 /
--            Shumway 1997): if dlretx is missing (NULL or CRSP sentinel
--            <= -1.0) and dlstcd >= 500 (performance-related), use
--            -0.30; ret = (1 + ret_msf)*(1 + dlret_eff) - 1
--          * market cap (dollars) and end-of-month exchange code
--          * excess return: ret - rf (ff.four_factor_monthly.rf is a
--            monthly decimal in this instance)
--          * ret_next: next month's excess return via leadInFrame,
--            guarded so the lead row is exactly month + 1
--          Sample months: Jun 1957 - Dec 2016 (paper long sample, L1878).
-- Tables: write_yeye.qmj_panel_raw, write_yeye.qmj_beta,
--         write_yeye.qmj_univ_m, crsp_202601.dsedelist,
--         ff.four_factor_monthly
-- Output columns: permno, month, datadate, fyear, gpoa, roe, roa, cfoa,
--         gmar, acc, d_gpoa, d_roe, d_roa, d_cfoa, d_gmar, lev, oscore,
--         zscore, evol, beta, bab, at, be, me_m, mcap, hexcd_eom, ret,
--         rf, ret_excess, ret_next
-- Depends on: 06_beta_monthly.sql, 09_panel_align.sql

WITH
delist AS (
    SELECT
        assumeNotNull(permno)          AS permno,
        subtractDays(toDate32(dlstdt), toDayOfMonth(toDate32(dlstdt)) - 1) AS month,
        if(dlretx IS NOT NULL AND dlretx > -1.0,
           dlretx,
           if(ifNull(dlstcd >= 500, 0), -0.30, NULL)) AS dlret_eff
    FROM crsp_202601.dsedelist
    WHERE dlstdt >= '1957-06-01' AND dlstdt <= '2017-01-31'
      AND permno IS NOT NULL
),
rf AS (
    SELECT subtractDays(toDate32(dt), toDayOfMonth(toDate32(dt)) - 1) AS month, rf
    FROM ff.four_factor_monthly
    WHERE dt IS NOT NULL
),
pr AS (
    SELECT
        p.permno   AS permno,
        p.month    AS month,
        p.datadate AS datadate,
        p.fyear    AS fyear,
        p.gpoa     AS gpoa,
        p.roe      AS roe,
        p.roa      AS roa,
        p.cfoa     AS cfoa,
        p.gmar     AS gmar,
        p.acc      AS acc,
        p.d_gpoa   AS d_gpoa,
        p.d_roe    AS d_roe,
        p.d_roa    AS d_roa,
        p.d_cfoa   AS d_cfoa,
        p.d_gmar   AS d_gmar,
        p.lev      AS lev,
        p.oscore   AS oscore,
        p.zscore   AS zscore,
        p.evol     AS evol,
        b.beta     AS beta,
        -b.beta    AS bab,
        p.at       AS at,
        p.be       AS be,
        p.me_m     AS me_m,
        u.mcap     AS mcap,
        u.hexcd_eom AS hexcd_eom,
        if(d.dlret_eff IS NOT NULL,
           (1 + coalesce(u.ret, 0)) * (1 + d.dlret_eff) - 1,
           u.ret) AS ret,
        r.rf       AS rf
    FROM write_yeye.qmj_panel_raw AS p
    LEFT JOIN write_yeye.qmj_beta AS b
        ON p.permno = b.permno AND p.month = b.month
    LEFT JOIN write_yeye.qmj_univ_m AS u
        ON p.permno = u.permno AND p.month = u.month
    LEFT JOIN delist AS d
        ON p.permno = d.permno AND p.month = d.month
    INNER JOIN rf AS r
        ON p.month = r.month
),
withlead AS (
    SELECT
        pr.*,
        ret - rf AS ret_excess,
        leadInFrame(ret - rf, 1) OVER w AS ret_next_raw,
        leadInFrame(month, 1)    OVER w AS month_lead
    FROM pr
    WINDOW w AS (PARTITION BY permno ORDER BY month
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
)
SELECT
    permno, month, datadate, fyear,
    gpoa, roe, roa, cfoa, gmar, acc,
    d_gpoa, d_roe, d_roa, d_cfoa, d_gmar,
    lev, oscore, zscore, evol,
    beta, bab, at, be, me_m,
    mcap, hexcd_eom, ret, rf, ret_excess,
    if(month_lead = addMonths(month, 1), ret_next_raw, NULL) AS ret_next
FROM withlead
WHERE month <= toDate32('2016-12-01')
SETTINGS allow_experimental_analyzer = 0,
         join_algorithm = 'partial_merge',
         max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
