-- returns_windows.sql
-- Purpose: Windowed buy-and-hold returns (firm + value-weighted market) for the
--          high-BM panel rows staged in write_yeye.{win_table}:
--            * raw_ret1 / n_months_traded1 : 12 month-ends [win_start .. +11m]
--            * raw_ret2 / n_months_traded2 : 24 month-ends [win_start .. +23m]
--            * firm_mom_bhr / n_mom_months : 6 month-ends [win_start-6m .. -1m]
--            * mkt_ret1 / mkt_ret2 / mkt_mom_bhr : same windows, CRSP VW index
--            * moment = firm_mom_bhr - mkt_mom_bhr (Table 7 MOMENT)
--          win_start = beginning of the 5th month after fiscal year-end
--          (addMonths(toStartOfMonth(datadate), 5)).
--          Delisting rule (paper §3.2): months missing because the firm delisted
--          (or simply have no msf row) contribute factor 1 (return 0) — BHR is the
--          product over AVAILABLE monthly returns only; n_months_traded* records
--          coverage so delisted windows are identifiable. The market never delists:
--          its BHR compounds the FULL window. ret guarded with greatest(ret,-0.9999)
--          against exactly -1; sentinel rows (ret <= -1, none verified in-window)
--          are excluded.
-- Tables: write_yeye.{win_table} (scratch: gvkey, fyear, permno, win_start),
--         crsp_202601.msf, crsp_202601.msi
-- Output columns: gvkey, fyear, raw_ret1, n_months_traded1, raw_ret2,
--                 n_months_traded2, firm_mom_bhr, n_mom_months,
--                 mkt_ret1, mkt_ret2, mkt_mom_bhr, moment
-- Depends on: main.py stages the scratch table from the high-BM panel
--             (high_bm_signals.sql output + crsp_link.sql permnos).
-- Settings: join_algorithm=partial_merge (range join msf on permno + month window),
--           max_execution_time=600, max_rows_to_read=10e9

WITH fm AS (
    -- Firm months within [win_start - 6m, win_start + 24m).
    SELECT w.gvkey AS gvkey, w.fyear AS fyear, w.win_start AS win_start,
           dateDiff('month', w.win_start,
                    toDate(parseDateTimeBestEffort(m.date))) AS mi,
           toFloat64(m.ret) AS ret
    FROM write_yeye.{win_table} AS w
    INNER JOIN crsp_202601.msf AS m
            ON m.permno = w.permno
    WHERE m.date >= '{msf_start}' AND m.date <= '{msf_end}'
      AND m.ret IS NOT NULL AND m.ret > -1
      AND toDate(parseDateTimeBestEffort(m.date)) >= addMonths(w.win_start, -6)
      AND toDate(parseDateTimeBestEffort(m.date)) < addMonths(w.win_start, 24)
),
firm AS (
    SELECT gvkey, fyear, win_start,
           exp(sum(if(mi BETWEEN 0 AND 11, log(1 + greatest(ret, -0.9999)), 0))) - 1
               AS raw_ret1,
           countIf(mi BETWEEN 0 AND 11) AS n_months_traded1,
           exp(sum(if(mi BETWEEN 0 AND 23, log(1 + greatest(ret, -0.9999)), 0))) - 1
               AS raw_ret2,
           countIf(mi BETWEEN 0 AND 23) AS n_months_traded2,
           exp(sum(if(mi BETWEEN -6 AND -1, log(1 + greatest(ret, -0.9999)), 0))) - 1
               AS firm_mom_bhr,
           countIf(mi BETWEEN -6 AND -1) AS n_mom_months
    FROM fm
    GROUP BY gvkey, fyear, win_start
),
mk AS (
    -- Market (CRSP VW with dividends) months per distinct window start.
    SELECT w.win_start AS win_start,
           dateDiff('month', w.win_start,
                    toDate(parseDateTimeBestEffort(i.date))) AS mi,
           toFloat64(i.vwretd) AS r
    FROM (SELECT DISTINCT win_start FROM write_yeye.{win_table}) AS w
    CROSS JOIN crsp_202601.msi AS i
    WHERE i.date >= '{msf_start}' AND i.date <= '{msf_end}'
      AND i.vwretd IS NOT NULL
      AND toDate(parseDateTimeBestEffort(i.date)) >= addMonths(w.win_start, -6)
      AND toDate(parseDateTimeBestEffort(i.date)) < addMonths(w.win_start, 24)
),
mkt AS (
    SELECT win_start,
           exp(sum(if(mi BETWEEN 0 AND 11, log(1 + r), 0))) - 1 AS mkt_ret1,
           exp(sum(if(mi BETWEEN 0 AND 23, log(1 + r), 0))) - 1 AS mkt_ret2,
           exp(sum(if(mi BETWEEN -6 AND -1, log(1 + r), 0))) - 1 AS mkt_mom_bhr
    FROM mk
    GROUP BY win_start
)
-- One row per staged window (LEFT JOIN): permnos with zero msf rows in the
-- whole [-6m, +24m) span still get a row — firm-side columns NULL (main.py
-- applies the delisting=zero rule: empty product -> 0), market-side columns
-- always present so the market adjustment is defined for every firm-year.
SELECT w.gvkey AS gvkey, w.fyear AS fyear,
       f.raw_ret1 AS raw_ret1, f.n_months_traded1 AS n_months_traded1,
       f.raw_ret2 AS raw_ret2, f.n_months_traded2 AS n_months_traded2,
       f.firm_mom_bhr AS firm_mom_bhr, f.n_mom_months AS n_mom_months,
       m.mkt_ret1 AS mkt_ret1, m.mkt_ret2 AS mkt_ret2,
       m.mkt_mom_bhr AS mkt_mom_bhr,
       f.firm_mom_bhr - m.mkt_mom_bhr AS moment
FROM write_yeye.{win_table} AS w
LEFT JOIN firm AS f ON f.gvkey = w.gvkey AND f.fyear = w.fyear
LEFT JOIN mkt AS m ON m.win_start = w.win_start
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
