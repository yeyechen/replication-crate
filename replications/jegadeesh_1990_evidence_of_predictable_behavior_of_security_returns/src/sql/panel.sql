-- panel.sql
-- Purpose: Monthly (permno, month) panel for Table I cross-sectional regression
--          with lagged returns and forward-looking 60-month mean (R_bar_it).
-- Tables: crsp_202601.msf, crsp_202601.dsenames
-- Output columns: permno, month, ret, lag1..lag12, lag24, lag36, r_bar_it
-- Depends on: (none — direct assembly to avoid CTE name-shadowing issues)
-- Settings: join_algorithm=partial_merge, max_execution_time=900
--
-- The forward-looking R_bar_it is intentionally look-ahead: it is the
-- AVERAGE of ret over months t+1..t+60 for the same stock. The paper
-- uses this to remove cross-sectional differences in unconditional
-- expected returns from the dependent variable (paper L152-156,
-- equation 2). It is OK as a dependent-side correction because the
-- regressors are lagged returns only — the forward window does NOT
-- contaminate the regressor side.
--
-- Sample month range: 1929-01 through 1987-12. R_bar_it is non-NULL
-- only for 1929-01..1982-12 (the last 60 months of the panel have
-- no forward window).
--
-- Strategy:
--   Step 1: build the stock-month ret history with PIT shrcd/exchcd
--           filter over the extended sample window 1926-1988.
--   Step 2: with_lags CTE — lag1..lag12, lag24, lag36 via lagInFrame.
--   Step 3: with_leads CTE — lead1..lead60 via lagInFrame(..., -k).
--   Step 4: outer SELECT — average the 60 leads into r_bar_it.
--
-- Note on column naming: the inner date column is aliased date32 (not
-- date) to avoid shadowing the raw string `date` column from msf in the
-- same query block. ClickHouse's `toDate32OrNull(Date32)` would error
-- out — see the Illegal-type-Date32 case in ClickHouse.md.

WITH
  -- Step 1: PIT-filtered stock-month ret history with extended sample
  -- window (1926-01 to 1988-12) so lags and forward window fit.
  stock_month AS (
    SELECT
      msf.permno                                              AS permno,
      toDate32(toDate32OrNull(msf.date) - toIntervalDay(dayOfMonth(toDate32OrNull(msf.date)) - 1)) AS month,
      msf.ret                                                 AS ret,
      msf.retx                                                AS retx,
      msf.prc                                                 AS prc,
      msf.shrout                                              AS shrout
    FROM crsp_202601.msf AS msf
    INNER JOIN crsp_202601.dsenames AS n
      ON msf.permno = n.permno
     AND toDate32OrNull(msf.date) >= toDate32OrNull(n.namedt)
     AND toDate32OrNull(msf.date) <= toDate32OrNull(n.nameendt)
    WHERE n.shrcd IN (10, 11)
      AND n.exchcd IN (1, 2, 3)
      AND toDate32OrNull(msf.date) BETWEEN toDate32('1926-01-01') AND toDate32('1988-12-31')
  ),
  -- Step 2: 12/24/36-month lags of ret.
  with_lags AS (
    SELECT
      permno, month, ret, retx, prc, shrout,
      lagInFrame(ret,  1) OVER w AS lag1,
      lagInFrame(ret,  2) OVER w AS lag2,
      lagInFrame(ret,  3) OVER w AS lag3,
      lagInFrame(ret,  4) OVER w AS lag4,
      lagInFrame(ret,  5) OVER w AS lag5,
      lagInFrame(ret,  6) OVER w AS lag6,
      lagInFrame(ret,  7) OVER w AS lag7,
      lagInFrame(ret,  8) OVER w AS lag8,
      lagInFrame(ret,  9) OVER w AS lag9,
      lagInFrame(ret, 10) OVER w AS lag10,
      lagInFrame(ret, 11) OVER w AS lag11,
      lagInFrame(ret, 12) OVER w AS lag12,
      lagInFrame(ret, 24) OVER w AS lag24,
      lagInFrame(ret, 36) OVER w AS lag36
    FROM stock_month
    WINDOW w AS (PARTITION BY permno ORDER BY month
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  ),
  -- Step 3: forward-looking 60-month window. Each lead_k holds the ret
  -- value k months after `month`. Then arraySum/length() below averages
  -- them, ignoring NULLs. leadInFrame takes a positive offset (lagInFrame
  -- only accepts positive offsets — negative lags error out).
  with_leads AS (
    SELECT
      permno, month, ret, retx, prc, shrout,
      lag1, lag2, lag3, lag4, lag5, lag6, lag7, lag8,
      lag9, lag10, lag11, lag12, lag24, lag36,
      leadInFrame(ret,  1) OVER w AS ld1,  leadInFrame(ret,  2) OVER w AS ld2,
      leadInFrame(ret,  3) OVER w AS ld3,  leadInFrame(ret,  4) OVER w AS ld4,
      leadInFrame(ret,  5) OVER w AS ld5,  leadInFrame(ret,  6) OVER w AS ld6,
      leadInFrame(ret,  7) OVER w AS ld7,  leadInFrame(ret,  8) OVER w AS ld8,
      leadInFrame(ret,  9) OVER w AS ld9,  leadInFrame(ret, 10) OVER w AS ld10,
      leadInFrame(ret, 11) OVER w AS ld11, leadInFrame(ret, 12) OVER w AS ld12,
      leadInFrame(ret, 13) OVER w AS ld13, leadInFrame(ret, 14) OVER w AS ld14,
      leadInFrame(ret, 15) OVER w AS ld15, leadInFrame(ret, 16) OVER w AS ld16,
      leadInFrame(ret, 17) OVER w AS ld17, leadInFrame(ret, 18) OVER w AS ld18,
      leadInFrame(ret, 19) OVER w AS ld19, leadInFrame(ret, 20) OVER w AS ld20,
      leadInFrame(ret, 21) OVER w AS ld21, leadInFrame(ret, 22) OVER w AS ld22,
      leadInFrame(ret, 23) OVER w AS ld23, leadInFrame(ret, 24) OVER w AS ld24,
      leadInFrame(ret, 25) OVER w AS ld25, leadInFrame(ret, 26) OVER w AS ld26,
      leadInFrame(ret, 27) OVER w AS ld27, leadInFrame(ret, 28) OVER w AS ld28,
      leadInFrame(ret, 29) OVER w AS ld29, leadInFrame(ret, 30) OVER w AS ld30,
      leadInFrame(ret, 31) OVER w AS ld31, leadInFrame(ret, 32) OVER w AS ld32,
      leadInFrame(ret, 33) OVER w AS ld33, leadInFrame(ret, 34) OVER w AS ld34,
      leadInFrame(ret, 35) OVER w AS ld35, leadInFrame(ret, 36) OVER w AS ld36,
      leadInFrame(ret, 37) OVER w AS ld37, leadInFrame(ret, 38) OVER w AS ld38,
      leadInFrame(ret, 39) OVER w AS ld39, leadInFrame(ret, 40) OVER w AS ld40,
      leadInFrame(ret, 41) OVER w AS ld41, leadInFrame(ret, 42) OVER w AS ld42,
      leadInFrame(ret, 43) OVER w AS ld43, leadInFrame(ret, 44) OVER w AS ld44,
      leadInFrame(ret, 45) OVER w AS ld45, leadInFrame(ret, 46) OVER w AS ld46,
      leadInFrame(ret, 47) OVER w AS ld47, leadInFrame(ret, 48) OVER w AS ld48,
      leadInFrame(ret, 49) OVER w AS ld49, leadInFrame(ret, 50) OVER w AS ld50,
      leadInFrame(ret, 51) OVER w AS ld51, leadInFrame(ret, 52) OVER w AS ld52,
      leadInFrame(ret, 53) OVER w AS ld53, leadInFrame(ret, 54) OVER w AS ld54,
      leadInFrame(ret, 55) OVER w AS ld55, leadInFrame(ret, 56) OVER w AS ld56,
      leadInFrame(ret, 57) OVER w AS ld57, leadInFrame(ret, 58) OVER w AS ld58,
      leadInFrame(ret, 59) OVER w AS ld59, leadInFrame(ret, 60) OVER w AS ld60
    FROM with_lags
    WINDOW w AS (PARTITION BY permno ORDER BY month
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  )
SELECT
  permno                                                     AS permno,
  month                                                      AS month,
  ret                                                        AS ret,
  retx                                                       AS retx,
  prc                                                        AS prc,
  shrout                                                     AS shrout,
  lag1, lag2, lag3, lag4, lag5, lag6, lag7, lag8,
  lag9, lag10, lag11, lag12, lag24, lag36,
  -- R_bar_it = mean of ret over months t+1..t+60 (avg ignores NULLs).
  -- Returns NULL if all 60 leads are NULL (e.g. last 60 months of panel).
  -- arrayAvg() rejects Array(Nullable(Float64)) input, so we explicitly
  -- filter NULLs out of the array first (arrayFilter on isNull),
  -- then assumeNotNull inside arrayMap yields Array(Float64).
  arraySum(
    arrayMap(x -> assumeNotNull(x),
      arrayFilter(x -> NOT isNull(x),
        [ld1,ld2,ld3,ld4,ld5,ld6,ld7,ld8,ld9,ld10,
         ld11,ld12,ld13,ld14,ld15,ld16,ld17,ld18,ld19,ld20,
         ld21,ld22,ld23,ld24,ld25,ld26,ld27,ld28,ld29,ld30,
         ld31,ld32,ld33,ld34,ld35,ld36,ld37,ld38,ld39,ld40,
         ld41,ld42,ld43,ld44,ld45,ld46,ld47,ld48,ld49,ld50,
         ld51,ld52,ld53,ld54,ld55,ld56,ld57,ld58,ld59,ld60])
    )
  ) / greatest(1,
      length(
        arrayFilter(x -> NOT isNull(x),
          [ld1,ld2,ld3,ld4,ld5,ld6,ld7,ld8,ld9,ld10,
           ld11,ld12,ld13,ld14,ld15,ld16,ld17,ld18,ld19,ld20,
           ld21,ld22,ld23,ld24,ld25,ld26,ld27,ld28,ld29,ld30,
           ld31,ld32,ld33,ld34,ld35,ld36,ld37,ld38,ld39,ld40,
           ld41,ld42,ld43,ld44,ld45,ld46,ld47,ld48,ld49,ld50,
           ld51,ld52,ld53,ld54,ld55,ld56,ld57,ld58,ld59,ld60])
      )
    ) AS r_bar_it
FROM with_leads
SETTINGS max_execution_time = 900,
         join_algorithm = 'partial_merge'