-- moment_accrual_deciles.sql
-- Purpose: Prior-year decile breakpoints (10 bins) of MOMENT and of the raw
--          ACCRUAL value, computed within fyear s over the FULL linked-Compustat
--          population staged in write_yeye.{uni_table} (every funda firm-year with
--          a valid CRSP link and ME>0 — NOT just high-BM — with the variable
--          available). main.py applies the fyear t-1 breakpoints to high-BM fyear-t
--          firms (moment_decile, accrual_decile 1-10 for Table 7).
--          MOMENT = firm BHR over the 6 months [win_start-6m .. win_start-1m]
--          minus the VW market BHR over the same window.
-- Tables: write_yeye.{uni_table} (scratch: gvkey, fyear, permno, win_start, accrual),
--         crsp_202601.msf, crsp_202601.msi
-- Output columns: fyear, mom_d1..mom_d9, acc_d1..acc_d9, n_mom, n_acc
-- Depends on: main.py stages the scratch table (funda_base.sql + crsp_link.sql:
--             all linked funda FY{cutoff_start}..{cutoff_end} with ME>0;
--             accrual = (ib - oancf)/at_{t-1} where available).
-- Notes: quantileExact ignores NULLs — MOMENT breakpoints use firm-years with at
--        least one traded month in the 6-month window; ACCRUAL breakpoints use
--        firm-years with non-null accrual (oancf exists only FY1987+, so the
--        FY1986 accrual breakpoints come from the few firms with FY1986 cash-flow
--        data — typically none; see main.py report).
-- Settings: join_algorithm=partial_merge, max_execution_time=600, max_rows_to_read=10e9

WITH fm AS (
    SELECT u.gvkey AS gvkey, u.fyear AS fyear, u.win_start AS win_start,
           u.accrual AS accrual,
           toFloat64(m.ret) AS ret
    FROM write_yeye.{uni_table} AS u
    INNER JOIN crsp_202601.msf AS m
            ON m.permno = u.permno
    WHERE m.date >= '{msf_start}' AND m.date <= '{msf_end}'
      AND m.ret IS NOT NULL AND m.ret > -1
      AND toDate(parseDateTimeBestEffort(m.date)) >= addMonths(u.win_start, -6)
      AND toDate(parseDateTimeBestEffort(m.date)) < u.win_start
),
firm AS (
    SELECT gvkey, fyear, win_start, accrual,
           exp(sum(log(1 + greatest(ret, -0.9999)))) - 1 AS firm_bhr6
    FROM fm
    GROUP BY gvkey, fyear, win_start, accrual
),
mkt AS (
    SELECT w.win_start AS win_start,
           exp(sum(log(1 + toFloat64(i.vwretd)))) - 1 AS mkt_bhr6
    FROM (SELECT DISTINCT win_start FROM write_yeye.{uni_table}) AS w
    CROSS JOIN crsp_202601.msi AS i
    WHERE i.date >= '{msf_start}' AND i.date <= '{msf_end}'
      AND i.vwretd IS NOT NULL
      AND toDate(parseDateTimeBestEffort(i.date)) >= addMonths(w.win_start, -6)
      AND toDate(parseDateTimeBestEffort(i.date)) < w.win_start
    GROUP BY w.win_start
),
mom AS (
    SELECT f.fyear AS fyear,
           f.accrual AS accrual,
           f.firm_bhr6 - m.mkt_bhr6 AS moment
    FROM firm AS f
    LEFT JOIN mkt AS m ON m.win_start = f.win_start
)
SELECT fyear,
       quantileExact(0.1)(moment) AS mom_d1,
       quantileExact(0.2)(moment) AS mom_d2,
       quantileExact(0.3)(moment) AS mom_d3,
       quantileExact(0.4)(moment) AS mom_d4,
       quantileExact(0.5)(moment) AS mom_d5,
       quantileExact(0.6)(moment) AS mom_d6,
       quantileExact(0.7)(moment) AS mom_d7,
       quantileExact(0.8)(moment) AS mom_d8,
       quantileExact(0.9)(moment) AS mom_d9,
       quantileExact(0.1)(accrual) AS acc_d1,
       quantileExact(0.2)(accrual) AS acc_d2,
       quantileExact(0.3)(accrual) AS acc_d3,
       quantileExact(0.4)(accrual) AS acc_d4,
       quantileExact(0.5)(accrual) AS acc_d5,
       quantileExact(0.6)(accrual) AS acc_d6,
       quantileExact(0.7)(accrual) AS acc_d7,
       quantileExact(0.8)(accrual) AS acc_d8,
       quantileExact(0.9)(accrual) AS acc_d9,
       count(moment) AS n_mom,
       count(accrual) AS n_acc
FROM mom
GROUP BY fyear
ORDER BY fyear
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
