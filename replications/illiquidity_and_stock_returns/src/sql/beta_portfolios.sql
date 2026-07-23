-- beta_portfolios.sql
-- Purpose: Scholes-Williams (1977) market-model betas of the 10 size
--          portfolios formed at the end of each characteristic year Y
--          (1963..1996) from the admitted sample (criteria i-iv; the
--          portfolio assignment is provided by main.py via the session
--          temp table _amihud_ports(permno, y, port), port 1 = smallest).
--          Each stock receives its portfolio's BETA_pY (done in main.py).
-- Method (paper L217, L287-291; Assumption 7):
--   R_ptY = equal-weighted mean of daily ret across member stocks
--           trading on day t of year Y;
--   RM_tY = equal-weighted mean of daily ret across ALL NYSE common
--           stocks (PIT universe, shrcd 10/11 exchcd 1) trading that day;
--   market model R_ptY = a + beta*RM_tY + e estimated per (p, Y) with
--   one lead and one lag of RM:
--     b0    = OLS slope of rp on rm      (all days of Y),
--     b_lead= OLS slope of rp on rm_{t+1} (days with a next day in Y),
--     b_lag = OLS slope of rp on rm_{t-1} (days with a prior day in Y),
--     rho   = first-order autocorrelation of RM within Y,
--     BETA_SW = (b0 + b_lead + b_lag) / (1 + 2*rho).
--   OLS slopes via the covariance formula
--     b = (n*sum(x*y) - sum(x)*sum(y)) / (n*sum(x*x) - sum(x)^2).
-- Tables: crsp_202601.dsf, crsp_202601.dsfhdr, session temp _amihud_ports
-- Output columns: y, port, n_obs, b0, b_lead, b_lag, rho, beta
-- Depends on: temp table _amihud_ports (permno Int32, y Int32, port Int32)
-- Note: toDate32 everywhere (Date saturates pre-1970).
WITH univ AS (
    SELECT
        d.permno         AS permno,
        toDate32(d.date) AS date32,
        toYear(toDate32(d.date)) AS y,
        d.ret            AS ret
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsfhdr AS h
        ON d.permno = h.permno
    WHERE h.hshrcd IN (10, 11)
      AND h.hexcd = 1
      AND d.date >= '1963-01-01' AND d.date <= '1996-12-31'
      AND toDate32(d.date) >= toDate32(h.begdat)
      AND toDate32(d.date) <= toDate32(h.enddat)
      AND d.ret IS NOT NULL AND d.ret > -1
),
-- daily EW market return (all NYSE common stocks trading that day)
mkt AS (
    SELECT y, date32, avg(ret) AS rm
    FROM univ
    GROUP BY y, date32
),
mkt_ll AS (
    SELECT
        y, date32, rm,
        leadInFrame(rm, 1) OVER w AS rm_lead,
        lagInFrame(rm, 1)  OVER w AS rm_lag
    FROM mkt
    WINDOW w AS (PARTITION BY y ORDER BY date32
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
),
-- daily EW portfolio returns (admitted members trading that day)
port_day AS (
    SELECT u.y AS y, p.port AS port, u.date32 AS date32, avg(u.ret) AS rp
    FROM univ AS u
    INNER JOIN _amihud_ports AS p
        ON u.permno = p.permno AND u.y = p.y
    GROUP BY u.y, p.port, u.date32
),
joined AS (
    SELECT j.y AS y, j.port AS port, j.rp AS rp,
           m.rm AS rm, m.rm_lead AS rm_lead, m.rm_lag AS rm_lag
    FROM port_day AS j
    INNER JOIN mkt_ll AS m ON j.y = m.y AND j.date32 = m.date32
),
rho_yr AS (
    -- first-order autocorrelation of RM within year: corr(rm_t, rm_{t-1})
    SELECT
        y,
        (count() * sum(rm * rm_lag) - sum(rm) * sum(rm_lag))
        / sqrt((count() * sum(rm * rm) - sum(rm) * sum(rm))
             * (count() * sum(rm_lag * rm_lag) - sum(rm_lag) * sum(rm_lag))) AS rho
    FROM mkt_ll
    WHERE rm_lag IS NOT NULL
    GROUP BY y
),
slopes AS (
    SELECT
        y, port,
        count() AS n_obs,
        (count() * sum(rm * rp) - sum(rm) * sum(rp))
          / (count() * sum(rm * rm) - sum(rm) * sum(rm)) AS b0,
        (countIf(rm_lead IS NOT NULL) * sumIf(rm_lead * rp, rm_lead IS NOT NULL)
           - sumIf(rm_lead, rm_lead IS NOT NULL) * sumIf(rp, rm_lead IS NOT NULL))
          / (countIf(rm_lead IS NOT NULL) * sumIf(rm_lead * rm_lead, rm_lead IS NOT NULL)
           - sumIf(rm_lead, rm_lead IS NOT NULL) * sumIf(rm_lead, rm_lead IS NOT NULL)) AS b_lead,
        (countIf(rm_lag IS NOT NULL) * sumIf(rm_lag * rp, rm_lag IS NOT NULL)
           - sumIf(rm_lag, rm_lag IS NOT NULL) * sumIf(rp, rm_lag IS NOT NULL))
          / (countIf(rm_lag IS NOT NULL) * sumIf(rm_lag * rm_lag, rm_lag IS NOT NULL)
           - sumIf(rm_lag, rm_lag IS NOT NULL) * sumIf(rm_lag, rm_lag IS NOT NULL)) AS b_lag
    FROM joined
    GROUP BY y, port
)
SELECT
    s.y        AS y,
    s.port     AS port,
    s.n_obs    AS n_obs,
    s.b0       AS b0,
    s.b_lead   AS b_lead,
    s.b_lag    AS b_lag,
    r.rho      AS rho,
    (s.b0 + s.b_lead + s.b_lag) / (1 + 2 * r.rho) AS beta
FROM slopes AS s
INNER JOIN rho_yr AS r ON s.y = r.y
ORDER BY s.y, s.port
SETTINGS max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
