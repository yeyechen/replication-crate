-- monthly_returns.sql
-- Purpose: Point-in-time NYSE/AMEX common-stock MONTHLY return panel for
--          LSV (1994) Table VII (market-state conditioning, Assumption A10).
--          Universe is defined point-in-time AT EACH MONTH (dsenames shrcd IN
--          (10,11) / exchcd IN (1,2) active on the msf date), so a stock enters
--          when it first qualifies and leaves when it stops qualifying or delists.
--          Monthly return = coalesce(clean msf.ret, clean dlret in the delisting
--          month, 0); a member delisted in a month earns coalesce(ret, dlret) that
--          month and exits thereafter (Assumption A10). Return sentinels (< -1.0)
--          are treated as missing (references/CRSP.md). Span: May 1968 .. April
--          1995 (the months over which at least one annual cohort is outstanding).
-- NOTE: This is the Table VII deliverable. It is large; validate syntax on a
--       date-bounded sample. The panel's annual holding-year returns instead use
--       stock_returns_monthly.sql (formation-universe membership, not PIT-monthly).
-- Tables: crsp_202601.msf, crsp_202601.dsenames, crsp_202601.dsedelist
-- Output columns: permno, month_date (msf date), mnum (year*12+month), ret
-- Depends on: (none)
WITH msf_u AS (
    SELECT
        m.permno AS permno,
        m.date   AS month_date,
        toUInt32(substring(m.date, 1, 4)) * 12 + toUInt32(substring(m.date, 6, 2)) AS mnum,
        if(m.ret IS NOT NULL AND m.ret >= -1.0, m.ret, NULL) AS clean_ret
    FROM crsp_202601.msf AS m
    WHERE m.date >= '1963-05-01' AND m.date <= '1995-04-30'
),
-- point-in-time universe membership at each month
pit AS (
    SELECT mu.permno AS permno, mu.month_date AS month_date, mu.mnum AS mnum,
        mu.clean_ret AS clean_ret
    FROM msf_u AS mu
    INNER JOIN crsp_202601.dsenames AS n
        ON n.permno = mu.permno
       AND n.namedt <= mu.month_date
       AND ifNull(n.nameendt, '2100-01-01') >= mu.month_date
    WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2)
),
delist AS (
    SELECT
        e.permno AS permno,
        toUInt32(substring(e.dlstdt, 1, 4)) * 12 + toUInt32(substring(e.dlstdt, 6, 2)) AS dl_mnum,
        if(e.dlret IS NOT NULL AND e.dlret >= -1.0, e.dlret, NULL) AS clean_dlret
    FROM crsp_202601.dsedelist AS e
    WHERE e.dlstdt >= '1963-05-01' AND e.dlstdt <= '1995-04-30' AND e.dlstdt IS NOT NULL
),
present_msf AS (
    SELECT p.permno AS permno, p.month_date AS month_date, p.mnum AS mnum,
        coalesce(p.clean_ret, d.clean_dlret, 0) AS ret
    FROM pit AS p
    LEFT JOIN delist AS d ON d.permno = p.permno AND d.dl_mnum = p.mnum
),
msf_months AS (
    SELECT DISTINCT permno, mnum FROM pit
),
-- delisting month with no msf row but the stock is in the PIT universe up to then
delist_only AS (
    SELECT d.permno AS permno,
        concat(toString(intDiv(d.dl_mnum, 12)), '-',
               leftPad(toString(d.dl_mnum - intDiv(d.dl_mnum, 12) * 12), 2, '0'), '-01') AS month_date,
        d.dl_mnum AS mnum,
        coalesce(d.clean_dlret, 0) AS ret
    FROM delist AS d
    LEFT JOIN msf_months AS mm ON mm.permno = d.permno AND mm.mnum = d.dl_mnum
    WHERE mm.permno IS NULL
)
SELECT permno, month_date, mnum, ret FROM present_msf
UNION ALL
SELECT permno, month_date, mnum, ret FROM delist_only
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 900,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
