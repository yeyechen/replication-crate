-- signals.sql
-- Purpose: One analysis-ready row per (formation year, permno) with the full
--          cross-sectional signal set for LSV (1994). Computes, entirely in SQL:
--            * PIT NYSE/AMEX universe (A1) and formation-date market equity
--            * PIT CRSP-Compustat link (linkprim='P', linktype LC/LU, active at formation)
--            * Accounting signal row (A3 window: datadate in [t-1-01-01, t-03-31])
--              -> book equity (A2 hierarchy), earnings, cash flow, sale, dividends
--            * Wide accounting for fiscal years t-5..t+4 (Table V per-$1 machinery)
--              and the extra t-6 sale needed for the GS year-5 growth rate
--            * Ratios: B/M (A2, only when BE>0), E/P, C/P, S/P, D/P and the
--              positive-ratio flags (A8: negatives kept in universe)
--            * GS = weighted (5,4,3,2,1) average of valid sales-growth years
--              g_k = sale(t-k)/sale(t-k-1)-1, valid when both sales > 0 (A4)
--            * gs_rank_frac = cross-sectional fractional percentile rank of GS
--              within the formation (window function), ascending: lowest growth -> 0
-- UNITS: me_apr is in DOLLARS (abs(prc)*shrout*1000); Compustat items are in
--        $ MILLIONS. Every ratio therefore divides the $M item by
--        me_millions = me_apr/1e6 (verified vs. the IBM check: E/P=5491/67502=0.081,
--        C/P=(5491+3871)/67502=0.139).
-- Tables: crsp_202601.msf, crsp_202601.dsenames, crsp_202601.ccmxpf_lnkhist,
--         comp_202601.funda
-- Output columns: fy, form_date, permno, gvkey, me_apr, be, be_valid, bm, earn,
--        cf, ep, cp, sp, dp_ratio, ep_pos, cp_pos, gs_wavg, gs_rank_frac,
--        n_gs_years, sig_datadate, sig_fyear, + 40 wide cols
--        (sale_/earn_/cf_/div_ x {m5,m4,m3,m2,m1,p0,p1,p2,p3,p4})
-- Depends on: formation_dates / universe_formation / ccm_link logic (inlined)
WITH
formation AS (
    SELECT toUInt32(substring(date, 1, 4)) AS fy, max(date) AS form_date
    FROM crsp_202601.msf
    WHERE date >= '1968-04-01' AND date <= '1989-04-30' AND substring(date, 6, 2) = '04'
    GROUP BY fy
),
universe AS (
    SELECT DISTINCT f.fy AS fy, f.form_date AS form_date, n.permno AS permno
    FROM crsp_202601.dsenames AS n
    CROSS JOIN formation AS f
    WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2) AND n.permno IS NOT NULL
      AND n.namedt <= '1989-12-31' AND ifNull(n.nameendt, '2100-01-01') >= '1968-01-01'
      AND n.namedt <= f.form_date AND ifNull(n.nameendt, '2100-01-01') >= f.form_date
),
link AS (
    SELECT fy, permno, gvkey FROM (
        SELECT f.fy AS fy, toInt32(l.lpermno) AS permno, l.gvkey AS gvkey,
            row_number() OVER (PARTITION BY f.fy, toInt32(l.lpermno)
                               ORDER BY l.linkdt DESC, l.gvkey ASC) AS rn
        FROM crsp_202601.ccmxpf_lnkhist AS l
        CROSS JOIN formation AS f
        WHERE l.linkprim = 'P' AND l.linktype IN ('LC', 'LU')
          AND l.lpermno IS NOT NULL AND l.gvkey IS NOT NULL
          AND l.linkdt <= f.form_date
          AND ifNull(l.linkenddt, '2100-01-01') >= f.form_date
    ) WHERE rn = 1
),
me_apr AS (
    SELECT u.fy AS fy, u.permno AS permno, abs(m.prc) * m.shrout * 1000 AS me_apr
    FROM universe AS u
    INNER JOIN crsp_202601.msf AS m
        ON m.permno = u.permno AND m.date = u.form_date
    WHERE m.date >= '1968-04-01' AND m.date <= '1989-04-30'
),
-- Compustat funda, standard filter (A7); one row per (gvkey, fyear) (latest datadate)
funda_dd AS (
    SELECT gvkey, fyear, datadate, ib, dp, sale, dvc, ceq, seq, at, lt, txdb, pstkrv, fyr
    FROM (
        SELECT *,
            row_number() OVER (PARTITION BY gvkey, fyear ORDER BY datadate DESC) AS rn
        FROM comp_202601.funda
        WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
          AND datadate >= '1961-12-31' AND datadate <= '1995-01-01'
          AND gvkey IS NOT NULL AND fyear IS NOT NULL
    ) WHERE rn = 1
),
-- Signal accounting row per (fy, gvkey): most recent datadate in the A3 window
acct_sig AS (
    SELECT fy, gvkey, sig_datadate, sig_fyear, sig_fyr, sig_ib, sig_dp, sig_sale, sig_dvc,
        coalesce(ceq + coalesce(txdb, 0),
                 seq  - coalesce(pstkrv, 0),
                 at   - lt - coalesce(pstkrv, 0)) AS be
    FROM (
        SELECT f.fy AS fy, ff.gvkey AS gvkey, ff.datadate AS sig_datadate,
            ff.fyear AS sig_fyear, ff.fyr AS sig_fyr, ff.ib AS sig_ib, ff.dp AS sig_dp,
            ff.sale AS sig_sale, ff.dvc AS sig_dvc, ff.ceq AS ceq, ff.seq AS seq,
            ff.at AS at, ff.lt AS lt, ff.txdb AS txdb, ff.pstkrv AS pstkrv,
            row_number() OVER (PARTITION BY f.fy, ff.gvkey ORDER BY ff.datadate DESC) AS rn
        FROM funda_dd AS ff
        CROSS JOIN formation AS f
        WHERE ff.datadate >= concat(toString(f.fy - 1), '-01-01')
          AND ff.datadate <= concat(toString(f.fy), '-03-31')
    ) WHERE rn = 1
),
-- Wide accounting per (fy, gvkey, offset). offset = fyear - fy.
-- offset -6 is pulled only to feed the GS year-5 growth rate (g_5 = sale(t-5)/sale(t-6)-1);
-- offsets -5..+4 become the 40 stored wide columns.
acct_wide AS (
    SELECT f.fy AS fy, ff.gvkey AS gvkey, toInt32(ff.fyear - f.fy) AS offset,
        ff.sale AS sale, ff.ib AS ib, ff.dp AS dp, ff.dvc AS dvc,
        ff.ib + ff.dp AS cf
    FROM funda_dd AS ff
    CROSS JOIN formation AS f
    WHERE ff.fyear >= f.fy - 6 AND ff.fyear <= f.fy + 4
),
-- Pivot wide items to one row per (fy, gvkey). maxIf preserves NULL for missing years.
acct_pivot AS (
    SELECT fy, gvkey,
        -- sale by year (GS uses s_m6..s_m1 internally; panel stores sale_m6..sale_p4)
        maxIf(sale, offset = -6) AS sale_m6,
        maxIf(sale, offset = -5) AS sale_m5, maxIf(sale, offset = -4) AS sale_m4,
        maxIf(sale, offset = -3) AS sale_m3, maxIf(sale, offset = -2) AS sale_m2,
        maxIf(sale, offset = -1) AS sale_m1, maxIf(sale, offset =  0) AS sale_p0,
        maxIf(sale, offset =  1) AS sale_p1, maxIf(sale, offset =  2) AS sale_p2,
        maxIf(sale, offset =  3) AS sale_p3, maxIf(sale, offset =  4) AS sale_p4,
        -- earnings (ib); _m6 = FY t-6 (year -5 level, needed for Table V growth)
        maxIf(ib, offset = -6) AS earn_m6,
        maxIf(ib, offset = -5) AS earn_m5, maxIf(ib, offset = -4) AS earn_m4,
        maxIf(ib, offset = -3) AS earn_m3, maxIf(ib, offset = -2) AS earn_m2,
        maxIf(ib, offset = -1) AS earn_m1, maxIf(ib, offset =  0) AS earn_p0,
        maxIf(ib, offset =  1) AS earn_p1, maxIf(ib, offset =  2) AS earn_p2,
        maxIf(ib, offset =  3) AS earn_p3, maxIf(ib, offset =  4) AS earn_p4,
        -- cash flow (ib + dp)
        maxIf(cf, offset = -6) AS cf_m6,
        maxIf(cf, offset = -5) AS cf_m5, maxIf(cf, offset = -4) AS cf_m4,
        maxIf(cf, offset = -3) AS cf_m3, maxIf(cf, offset = -2) AS cf_m2,
        maxIf(cf, offset = -1) AS cf_m1, maxIf(cf, offset =  0) AS cf_p0,
        maxIf(cf, offset =  1) AS cf_p1, maxIf(cf, offset =  2) AS cf_p2,
        maxIf(cf, offset =  3) AS cf_p3, maxIf(cf, offset =  4) AS cf_p4,
        -- dividends (dvc)
        maxIf(dvc, offset = -6) AS div_m6,
        maxIf(dvc, offset = -5) AS div_m5, maxIf(dvc, offset = -4) AS div_m4,
        maxIf(dvc, offset = -3) AS div_m3, maxIf(dvc, offset = -2) AS div_m2,
        maxIf(dvc, offset = -1) AS div_m1, maxIf(dvc, offset =  0) AS div_p0,
        maxIf(dvc, offset =  1) AS div_p1, maxIf(dvc, offset =  2) AS div_p2,
        maxIf(dvc, offset =  3) AS div_p3, maxIf(dvc, offset =  4) AS div_p4
    FROM acct_wide
    GROUP BY fy, gvkey
),
-- Merge everything onto the universe (one row per fy, permno)
base AS (
    SELECT
        u.fy AS fy, u.form_date AS form_date, u.permno AS permno, l.gvkey AS gvkey,
        m.me_apr AS me_apr,
        s.be AS be, s.sig_datadate AS sig_datadate, s.sig_fyear AS sig_fyear,
        s.sig_ib AS sig_ib, s.sig_dp AS sig_dp, s.sig_sale AS sig_sale, s.sig_dvc AS sig_dvc,
        p.sale_m6 AS sale_m6,
        p.sale_m5 AS sale_m5, p.sale_m4 AS sale_m4, p.sale_m3 AS sale_m3, p.sale_m2 AS sale_m2,
        p.sale_m1 AS sale_m1, p.sale_p0 AS sale_p0, p.sale_p1 AS sale_p1, p.sale_p2 AS sale_p2,
        p.sale_p3 AS sale_p3, p.sale_p4 AS sale_p4,
        p.earn_m6 AS earn_m6,
        p.earn_m5 AS earn_m5, p.earn_m4 AS earn_m4, p.earn_m3 AS earn_m3, p.earn_m2 AS earn_m2,
        p.earn_m1 AS earn_m1, p.earn_p0 AS earn_p0, p.earn_p1 AS earn_p1, p.earn_p2 AS earn_p2,
        p.earn_p3 AS earn_p3, p.earn_p4 AS earn_p4,
        p.cf_m6 AS cf_m6,
        p.cf_m5 AS cf_m5, p.cf_m4 AS cf_m4, p.cf_m3 AS cf_m3, p.cf_m2 AS cf_m2,
        p.cf_m1 AS cf_m1, p.cf_p0 AS cf_p0, p.cf_p1 AS cf_p1, p.cf_p2 AS cf_p2,
        p.cf_p3 AS cf_p3, p.cf_p4 AS cf_p4,
        p.div_m6 AS div_m6,
        p.div_m5 AS div_m5, p.div_m4 AS div_m4, p.div_m3 AS div_m3, p.div_m2 AS div_m2,
        p.div_m1 AS div_m1, p.div_p0 AS div_p0, p.div_p1 AS div_p1, p.div_p2 AS div_p2,
        p.div_p3 AS div_p3, p.div_p4 AS div_p4
    FROM universe AS u
    LEFT JOIN link       AS l ON l.fy = u.fy AND l.permno = u.permno
    LEFT JOIN me_apr     AS m ON m.fy = u.fy AND m.permno = u.permno
    LEFT JOIN acct_sig   AS s ON s.fy = u.fy AND s.gvkey = l.gvkey
    LEFT JOIN acct_pivot AS p ON p.fy = u.fy AND p.gvkey = l.gvkey
),
-- Ratios + GS growth rates
calc AS (
    SELECT *,
        (be IS NOT NULL AND be > 0) AS be_valid,
        me_apr / 1000000.0 AS me_mil,
        sig_ib AS earn,
        sig_ib + sig_dp AS cf
    FROM base
),
calc2 AS (
    SELECT *,
        if(be_valid, be / nullIf(me_mil, 0), NULL)        AS bm,
        earn / nullIf(me_mil, 0)                          AS ep,
        cf   / nullIf(me_mil, 0)                          AS cp,
        sig_sale / nullIf(me_mil, 0)                      AS sp,
        sig_dvc  / nullIf(me_mil, 0)                      AS dp_ratio,
        if(coalesce(earn, 0) / nullIf(me_mil, 0) > 0, 1, 0) AS ep_pos,
        if(coalesce(cf, 0)   / nullIf(me_mil, 0) > 0, 1, 0) AS cp_pos,
        -- GS year-by-year growth (valid when both years' sales are positive)
        if(sale_m1 > 0 AND sale_m2 > 0, sale_m1 / sale_m2 - 1, NULL) AS g1,
        if(sale_m2 > 0 AND sale_m3 > 0, sale_m2 / sale_m3 - 1, NULL) AS g2,
        if(sale_m3 > 0 AND sale_m4 > 0, sale_m3 / sale_m4 - 1, NULL) AS g3,
        if(sale_m4 > 0 AND sale_m5 > 0, sale_m4 / sale_m5 - 1, NULL) AS g4,
        if(sale_m5 > 0 AND sale_m6 > 0, sale_m5 / sale_m6 - 1, NULL) AS g5
    FROM calc
),
calc3 AS (
    SELECT *,
        (if(g1 IS NOT NULL, 1, 0) + if(g2 IS NOT NULL, 1, 0) + if(g3 IS NOT NULL, 1, 0)
         + if(g4 IS NOT NULL, 1, 0) + if(g5 IS NOT NULL, 1, 0)) AS n_gs_years,
        (5*if(g1 IS NOT NULL, 1, 0) + 4*if(g2 IS NOT NULL, 1, 0) + 3*if(g3 IS NOT NULL, 1, 0)
         + 2*if(g4 IS NOT NULL, 1, 0) + 1*if(g5 IS NOT NULL, 1, 0)) AS gs_den
    FROM calc2
),
calc4 AS (
    SELECT *,
        if(gs_den > 0,
           (5*coalesce(g1, 0)*if(g1 IS NOT NULL, 1, 0)
            + 4*coalesce(g2, 0)*if(g2 IS NOT NULL, 1, 0)
            + 3*coalesce(g3, 0)*if(g3 IS NOT NULL, 1, 0)
            + 2*coalesce(g4, 0)*if(g4 IS NOT NULL, 1, 0)
            + 1*coalesce(g5, 0)*if(g5 IS NOT NULL, 1, 0)) / gs_den,
           NULL) AS gs_wavg
    FROM calc3
),
-- Fractional percentile rank of GS within the formation cross-section (ascending),
-- computed over non-missing GS only; missing GS -> NULL rank (A4).
gs_ranked AS (
    SELECT fy, permno,
        (rank() OVER (PARTITION BY fy ORDER BY gs_wavg) - 1)
            / nullIf(count() OVER (PARTITION BY fy) - 1, 0) AS gs_rank_frac
    FROM calc4
    WHERE gs_wavg IS NOT NULL
)
SELECT
    c.fy AS fy, c.form_date AS form_date, c.permno AS permno, c.gvkey AS gvkey,
    c.me_apr AS me_apr, c.be AS be, c.be_valid AS be_valid, c.bm AS bm,
    c.earn AS earn, c.cf AS cf, c.ep AS ep, c.cp AS cp, c.sp AS sp,
    c.dp_ratio AS dp_ratio, c.ep_pos AS ep_pos, c.cp_pos AS cp_pos,
    c.gs_wavg AS gs_wavg, g.gs_rank_frac AS gs_rank_frac, c.n_gs_years AS n_gs_years,
    c.sig_datadate AS sig_datadate, c.sig_fyear AS sig_fyear,
    c.sale_m6, c.sale_m5, c.sale_m4, c.sale_m3, c.sale_m2, c.sale_m1,
    c.sale_p0, c.sale_p1, c.sale_p2, c.sale_p3, c.sale_p4,
    c.earn_m6, c.earn_m5, c.earn_m4, c.earn_m3, c.earn_m2, c.earn_m1,
    c.earn_p0, c.earn_p1, c.earn_p2, c.earn_p3, c.earn_p4,
    c.cf_m6, c.cf_m5, c.cf_m4, c.cf_m3, c.cf_m2, c.cf_m1,
    c.cf_p0, c.cf_p1, c.cf_p2, c.cf_p3, c.cf_p4,
    c.div_m6, c.div_m5, c.div_m4, c.div_m3, c.div_m2, c.div_m1,
    c.div_p0, c.div_p1, c.div_p2, c.div_p3, c.div_p4
FROM calc4 AS c
LEFT JOIN gs_ranked AS g ON g.fy = c.fy AND g.permno = c.permno
ORDER BY c.fy, c.permno
SETTINGS max_execution_time = 900,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
