-- market_index_monthly.sql
-- Purpose: monthly CRSP value-weighted index return (msi.vwretd), the market
--          proxy for the Dimson sum-beta estimations (pre-ranking and
--          post-ranking). Paper: "the CRSP value-weighted portfolio of NYSE,
--          AMEX, and (after 1972) NASDAQ stocks used as the proxy for the
--          market" (L171, preprocessing_rules factor_market_proxy).
-- Tables: crsp_202601.msi
-- Output columns:
--   ym     UInt32  month key YYYYMM
--   mdate  String  month-end date (ISO string, as stored in msi)
--   vwretd Float64 value-weighted return with dividends (decimal)
-- Window: 1958-01 .. 1991-12. Needed months:
--   * pre-ranking betas: current months July 1958 .. June 1990 (formation
--     years t = 1963..1990, window July t-5 .. June t) plus one lag month
--     before each window (June 1958);
--   * post-ranking betas: July 1963 .. December 1990 (330 months) plus the
--     June 1963 lag, and the final holding window July 1990 .. June 1991.
-- Depends on: (none)
-- Note: msi.date is an ISO string. ClickHouse `Date` clamps pre-1970 dates to
--       1970-01-01, so the month key uses toDate32 (valid back to 1900).
SELECT
    toYYYYMM(toDate32(date)) AS ym,
    max(date)                AS mdate,
    argMax(vwretd, date)     AS vwretd
FROM crsp_202601.msi
WHERE date >= '1958-01-01' AND date <= '1991-12-31'
  AND date IS NOT NULL AND date != ''
GROUP BY ym
ORDER BY ym
SETTINGS max_execution_time = 300;
