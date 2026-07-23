-- fx_gbp_cross.sql
-- Purpose: Month-end USD conversion factors built from Compustat Global daily
--          FX (comp_202601.g_exrt_dly), which stores GBP-base CROSS rates:
--          fromcurd='GBP', tocurd=X, exratd = units of X per 1 GBP.
--
--          Define  usd_per_x(month, X) = USD price of 1 unit of currency X
--                                      = rate(GBP->USD) / rate(GBP->X)
--          (GBP cancels: (USD/GBP) / (X/GBP) = USD/X). This is the convention
--          consistent with the verified sanity anchors:
--            - GBP->JPY/GBP->USD ~ 107 JPY/USD  => USD/JPY = 1/107 ~ 0.0094
--            - NTT me_usd 2000-06-30 = prccd*cshoc * USD/JPY ~ 2.1e11 USD  (check)
--          Special cases handled by the same formula:
--            X='USD' : usd_per_usd = rate(GBP->USD)/rate(GBP->USD) = 1
--            X='GBP' : inject rate(GBP->GBP) = 1 => usd_per_gbp = rate(GBP->USD)
--
--          Month-end FX = last datadate ON-OR-BEFORE month-end (argMax within the
--          calendar month). Missing months are carried FORWARD (running-count
--          group fill) — a safety no-op here since every universe currency has
--          continuous monthly coverage 1982-02 .. 2006-06 (FX data begins
--          1982-02-01, so 1979-12 .. 1982-01 have no FX and map to NULL USD fields).
--
--          ret_usd is built in panel.sql as
--            (1+ret_local) * usd_per_x(curcdd_t, t) / usd_per_x(curcdd_{t-1}, t-1) - 1
--          joining this table twice (current and prior-month currency), so this
--          file only needs to supply usd_per_x per (cur, month).
--
-- Tables: comp_202601.g_exrt_dly (2.2M rows)
-- Output columns: cur (String), month (Date, last-day), usd_per_x (Float64)
-- Depends on: (none)
-- Settings: max_execution_time, max_rows_to_read guards; datadate filtered.
WITH
fx_me AS (
    -- month-end GBP-base cross rate per currency: units of `cur` per 1 GBP
    SELECT
        tocurd AS cur,
        toDate(toStartOfMonth(toDate(datadate)) + INTERVAL 1 MONTH - INTERVAL 1 DAY) AS month,
        argMax(exratd, datadate) AS rate
    FROM comp_202601.g_exrt_dly
    WHERE fromcurd = 'GBP'
      AND datadate >= '1979-12-01' AND datadate <= '2006-06-30'
      AND exratd IS NOT NULL AND exratd > 0
    GROUP BY tocurd, month
),
-- forward-fill any missing month within a currency's coverage (running-count grp)
fx_grp AS (
    SELECT cur, month, rate,
           count(rate) OVER (PARTITION BY cur ORDER BY month
                             ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
    FROM fx_me
),
fx_ff AS (
    SELECT cur, month, max(rate) OVER (PARTITION BY cur, grp) AS rate_gbp_cur
    FROM fx_grp
),
-- USD leg: units of USD per 1 GBP, per month
usd AS (
    SELECT month, rate_gbp_cur AS rate_usd FROM fx_ff WHERE cur = 'USD'
),
-- all currencies with a rate, plus an injected GBP leg (rate(GBP->GBP)=1).
-- (exclude any raw GBP rows first so the injection never duplicates.)
fx_all AS (
    SELECT cur, month, rate_gbp_cur FROM fx_ff WHERE cur != 'GBP'
    UNION ALL
    SELECT 'GBP' AS cur, month, 1.0 AS rate_gbp_cur FROM usd
)
SELECT
    a.cur AS cur, a.month AS month,
    u.rate_usd / a.rate_gbp_cur AS usd_per_x   -- USD per 1 unit of `cur`
FROM fx_all AS a
INNER JOIN usd AS u ON a.month = u.month
SETTINGS max_execution_time = 300,
         max_rows_to_read = 20000000,
         timeout_before_checking_execution_speed = 0
