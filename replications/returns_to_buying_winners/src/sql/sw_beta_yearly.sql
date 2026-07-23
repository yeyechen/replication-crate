-- sw_beta_yearly.sql
-- Purpose: Scholes-Williams (1977) lead-lag-corrected DAILY betas per
--          (permno, calendar year Y), Y = 1964..1989, for the Jegadeesh-Titman
--          (1993) universe (Assumption A8). For stock trading days in year Y:
--            beta_0   = OLS slope of the stock's daily return on the
--                       CONTEMPORANEOUS CRSP VW daily index return (dsi.vwretd);
--            beta_lag = slope on the index return of the PREVIOUS index
--                       trading day (lagInFrame over the index's own ordered
--                       date sequence);
--            beta_lead= slope on the NEXT index trading day (leadInFrame);
--            beta_SW  = (beta_lead + 2*beta_0 + beta_lag) / 2.
--          Lead/lag days at year boundaries use the adjacent index trading
--          day even when it falls in the neighboring calendar year, so the
--          index is fetched 1963-12-01 .. 1990-02-28 while stock days are
--          restricted to year Y. Slopes come from group aggregates:
--            beta = (n*sum(x*r) - sum(x)*sum(r)) / (n*sum(x^2) - sum(x)^2),
--          requiring n >= 50 valid stock-index day pairs in the year for each
--          of the three slopes, else beta_sw = NULL (paper silent on the
--          minimum; 50 days keeps most NYSE/AMEX stocks while excluding thin
--          traders — documented in assumptions.md P17). A stock-year has
--          n_contemp = n_lag = n_lead in practice (the index has every trading
--          day; the only NULL lag/lead is the first/last fetched index day,
--          outside 1964..1989 stock days).
--          Stock-day universe filter is IDENTICAL to universe_daily.sql
--          (dsenames PIT windows, shrcd IN (10,11), exchcd IN (1,2),
--          ret IS NOT NULL AND ret > -1.0), so betas are estimated on the
--          same in-universe daily returns the panel compounds.
-- Tables: crsp_202601.dsf, crsp_202601.dsenames, crsp_202601.dsi
-- Output columns: permno, beta_year (Int16), beta_sw (Nullable(Float64))
-- Depends on: (none)
-- NOTE: dates are strings (P8: never toDate() pre-1970 — ClickHouse Date
--       saturates to 1970-01-01); beta_year = substring(date, 1, 4).
WITH idx AS
(
    SELECT
        date,
        vwretd AS m,
        lagInFrame(vwretd, 1) OVER (ORDER BY date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS m_lag,
        leadInFrame(vwretd, 1) OVER (ORDER BY date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS m_lead
    FROM crsp_202601.dsi
    WHERE date >= '1963-12-01' AND date <= '1990-02-28'
      AND vwretd IS NOT NULL
      AND vwretd > -1.0
),
stk AS
(
    SELECT
        d.permno AS permno,
        d.date AS date,
        max(d.ret) AS ret
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsenames AS n
        ON d.permno = n.permno
       AND d.date >= n.namedt
       AND d.date <= coalesce(n.nameendt, '2100-01-01')
    WHERE d.date >= '1964-01-01' AND d.date <= '1989-12-31'
      AND d.permno IS NOT NULL
      AND n.shrcd IN (10, 11)
      AND n.exchcd IN (1, 2)
      AND d.ret IS NOT NULL AND d.ret > -1.0
    GROUP BY d.permno, d.date
),
paired AS
(
    SELECT
        s.permno AS permno,
        toInt16(substring(s.date, 1, 4)) AS beta_year,
        s.ret AS r,
        i.m AS m0,
        i.m_lag AS ml,
        i.m_lead AS md
    FROM stk AS s
    INNER JOIN idx AS i ON s.date = i.date
),
moments AS
(
    SELECT
        permno,
        beta_year,
        countIf(m0 IS NOT NULL) AS n0,
        sum(m0) AS x0,
        sumIf(r, m0 IS NOT NULL) AS r0,
        sum(m0 * r) AS xr0,
        sum(m0 * m0) AS q0,
        countIf(ml IS NOT NULL) AS nl,
        sum(ml) AS xl,
        sumIf(r, ml IS NOT NULL) AS rl,
        sum(ml * r) AS xrl,
        sum(ml * ml) AS ql,
        countIf(md IS NOT NULL) AS nd,
        sum(md) AS xd,
        sumIf(r, md IS NOT NULL) AS rd,
        sum(md * r) AS xrd,
        sum(md * md) AS qd
    FROM paired
    GROUP BY permno, beta_year
)
SELECT
    permno,
    beta_year,
    if(
        n0 >= 50 AND nl >= 50 AND nd >= 50
        AND (n0 * q0 - x0 * x0) != 0
        AND (nl * ql - xl * xl) != 0
        AND (nd * qd - xd * xd) != 0,
        (
            ((nd * xrd - xd * rd) / (nd * qd - xd * xd))
            + 2 * ((n0 * xr0 - x0 * r0) / (n0 * q0 - x0 * x0))
            + ((nl * xrl - xl * rl) / (nl * ql - xl * xl))
        ) / 2,
        NULL
    ) AS beta_sw
FROM moments
ORDER BY beta_year, permno
SETTINGS
    join_algorithm = 'hash',
    max_execution_time = 1800,
    max_rows_to_read = 20000000000,
    timeout_before_checking_execution_speed = 0;
