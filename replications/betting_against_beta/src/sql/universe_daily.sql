-- universe_daily.sql
-- Purpose: PIT-filtered daily LOG returns for US common stocks, with the
--          CRSP value-weighted market log return joined per date. This is the
--          input to the Frazzini-Pedersen (2014) ex-ante beta estimation
--          (1-year rolling volatility + 5-year rolling correlation of
--          overlapping 3-day log returns).
-- Tables: crsp_202601.dsf, crsp_202601.dsenames, crsp_202601.dsi
-- Output columns: permno (Int32), date (String ISO), logret (Float64),
--                 mkt_logret (Float64)
-- Parameters: %(dstart)s, %(dend)s — ISO-8601 date bounds (inclusive). The
--             pipeline calls this once per multi-year chunk to bound the
--             PIT range-join and keep client memory low.
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge, max_execution_time=600
--
-- CRSP gotchas handled here:
--   * ret sentinels (-55/-66/-77/-88/-99) are non-NULL negative floats;
--     filtered with `ret IS NOT NULL AND ret > -1.0`.
--   * Universe is point-in-time: a stock-day is kept only if a dsenames
--     record with shrcd IN (10,11) AND exchcd IN (1,2,3) covers that date
--     (namedt <= date <= nameendt).
--   * logret = ln(1 + ret); the market log return = ln(1 + vwretd).
WITH uni AS (
    SELECT
        d.permno            AS permno,
        d.date              AS date,
        log(1 + d.ret)      AS logret
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsenames AS n
        ON d.permno = n.permno
       AND d.date >= n.namedt
       AND d.date <= n.nameendt
    WHERE n.shrcd IN (10, 11)
      AND n.exchcd IN (1, 2, 3)
      AND d.date >= %(dstart)s
      AND d.date <= %(dend)s
      AND d.ret IS NOT NULL
      AND d.ret > -1.0
)
SELECT
    u.permno            AS permno,
    u.date              AS date,
    u.logret            AS logret,
    log(1 + m.vwretd)   AS mkt_logret
FROM uni AS u
LEFT JOIN crsp_202601.dsi AS m
    ON m.date = u.date
SETTINGS join_algorithm = 'partial_merge', max_execution_time = 600;
