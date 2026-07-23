-- size_benchmarks_monthly.sql
-- Purpose: Equally-weighted MONTHLY return of each formation-year size-decile
--          portfolio, for the SAAR benchmark and the optional Table VII size
--          checks. Assumption A5 (fixed-assignment reading): the decile membership
--          is fixed at formation year t (stocks in the NYSE/AMEX universe at end of
--          April t, assigned to deciles by December t-1 market equity); in each
--          month the EW return is taken over the members ALIVE (present) that month.
--          A member delisted in a month earns coalesce(ret, dlret) that month and
--          exits thereafter. Span: May 1968 .. April 1995.
-- NOTE: Deliverable; large. Validate syntax on a date-bounded sample. For the
--       panel, the same EW series is assembled in Python from stock_returns_monthly
--       (bounded to April 1994) + size_deciles to avoid re-scanning msf.
-- Tables: crsp_202601.msf, crsp_202601.dsenames, crsp_202601.dsedelist
-- Output columns: fy, size_dec, mnum, ew_ret, n_members
-- Depends on: universe_formation + size_deciles logic (inlined)
WITH
formation AS (
    SELECT toUInt32(substring(date, 1, 4)) AS fy, max(date) AS form_date
    FROM crsp_202601.msf
    WHERE date >= '1968-04-01' AND date <= '1989-04-30' AND substring(date, 6, 2) = '04'
    GROUP BY fy
),
universe AS (
    SELECT DISTINCT f.fy AS fy, n.permno AS permno
    FROM crsp_202601.dsenames AS n
    CROSS JOIN formation AS f
    WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2) AND n.permno IS NOT NULL
      AND n.namedt <= '1989-12-31' AND ifNull(n.nameendt, '2100-01-01') >= '1968-01-01'
      AND n.namedt <= f.form_date AND ifNull(n.nameendt, '2100-01-01') >= f.form_date
),
dec_dates AS (
    SELECT toUInt32(substring(date, 1, 4)) + 1 AS fy, max(date) AS dec_date
    FROM crsp_202601.msf
    WHERE substring(date, 6, 2) = '12' AND date >= '1967-12-01' AND date <= '1988-12-31'
    GROUP BY substring(date, 1, 4)
),
dec_univ AS (
    SELECT DISTINCT d.fy AS fy, d.dec_date AS dec_date, n.permno AS permno
    FROM crsp_202601.dsenames AS n
    CROSS JOIN dec_dates AS d
    WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2) AND n.permno IS NOT NULL
      AND n.namedt <= '1988-12-31' AND ifNull(n.nameendt, '2100-01-01') >= '1967-01-01'
      AND n.namedt <= d.dec_date AND ifNull(n.nameendt, '2100-01-01') >= d.dec_date
),
size_dec AS (
    SELECT fy, permno, ntile(10) OVER (PARTITION BY fy ORDER BY me_dec ASC) AS size_dec
    FROM (
        SELECT u.fy AS fy, u.permno AS permno, abs(m.prc) * m.shrout * 1000 AS me_dec
        FROM dec_univ AS u
        INNER JOIN crsp_202601.msf AS m ON m.permno = u.permno AND m.date = u.dec_date
        WHERE m.date >= '1967-12-01' AND m.date <= '1988-12-31'
          AND abs(m.prc) * m.shrout * 1000 > 0
    )
),
univ_permno AS (SELECT DISTINCT permno FROM universe),
msf_u AS (
    SELECT m.permno AS permno,
        toUInt32(substring(m.date, 1, 4)) * 12 + toUInt32(substring(m.date, 6, 2)) AS mnum,
        if(m.ret IS NOT NULL AND m.ret >= -1.0, m.ret, NULL) AS clean_ret
    FROM crsp_202601.msf AS m
    INNER JOIN univ_permno AS u ON u.permno = m.permno
    WHERE m.date >= '1968-05-01' AND m.date <= '1995-04-30'
),
delist AS (
    SELECT e.permno AS permno,
        toUInt32(substring(e.dlstdt, 1, 4)) * 12 + toUInt32(substring(e.dlstdt, 6, 2)) AS dl_mnum,
        if(e.dlret IS NOT NULL AND e.dlret >= -1.0, e.dlret, NULL) AS clean_dlret
    FROM crsp_202601.dsedelist AS e
    INNER JOIN univ_permno AS u ON u.permno = e.permno
    WHERE e.dlstdt >= '1968-05-01' AND e.dlstdt <= '1995-04-30' AND e.dlstdt IS NOT NULL
),
present_msf AS (
    SELECT m.permno AS permno, m.mnum AS mnum,
        coalesce(m.clean_ret, d.clean_dlret, 0) AS ret
    FROM msf_u AS m
    LEFT JOIN delist AS d ON d.permno = m.permno AND d.dl_mnum = m.mnum
),
msf_months AS (SELECT DISTINCT permno, mnum FROM msf_u),
delist_only AS (
    SELECT d.permno AS permno, d.dl_mnum AS mnum, coalesce(d.clean_dlret, 0) AS ret
    FROM delist AS d
    LEFT JOIN msf_months AS mm ON mm.permno = d.permno AND mm.mnum = d.dl_mnum
    WHERE mm.permno IS NULL
),
stock_ret AS (
    SELECT permno, mnum, ret FROM present_msf
    UNION ALL
    SELECT permno, mnum, ret FROM delist_only
),
members AS (
    SELECT u.fy AS fy, sd.size_dec AS size_dec, u.permno AS permno
    FROM universe AS u
    INNER JOIN size_dec AS sd ON sd.fy = u.fy AND sd.permno = u.permno
)
SELECT
    mb.fy AS fy,
    mb.size_dec AS size_dec,
    sr.mnum AS mnum,
    avg(sr.ret) AS ew_ret,
    count() AS n_members
FROM members AS mb
INNER JOIN stock_ret AS sr ON sr.permno = mb.permno
GROUP BY mb.fy, mb.size_dec, sr.mnum
ORDER BY mb.fy, mb.size_dec, sr.mnum
SETTINGS max_execution_time = 900,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
