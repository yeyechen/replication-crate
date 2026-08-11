-- winsorize.sql
-- Purpose: Winsorize accounting variables (NOA, PM, ATO, RNOA, ΔNOA, ΔPM,
--          ΔATO, ΔRNOA) at 1st and 99th percentiles within each fiscal year
--          (per assumption 2 in preparations/assumptions.md).
-- Tables: in-memory panel (input from accounting_changes.sql)
-- Output columns: same as input + _w suffix on winsorized columns
-- Depends on: accounting_changes.sql (chain — see panel.sql)
-- Settings: max_execution_time=600, max_rows_to_read=5e8
--
-- Strategy: For each variable V and each fiscal year, compute the 1st and
-- 99th percentile of V across all (gvkey, fyear) rows in that year, then
-- clip V into [p1, p99]. We use `quantileExact(0.01)(V)` and
-- `quantileExact(0.99)(V)` partitioned by fyear.
--
-- ClickHouse note: `quantileExact` requires aggregate context. We compute
-- the percentiles in a GROUP BY fyear subquery, then JOIN back.

WITH
  -- Compute per-year winsorization bounds for each numeric variable.
  bounds AS (
    SELECT
      fyear,
      quantileExact(0.01)(NOA)      AS NOA_p01,
      quantileExact(0.99)(NOA)      AS NOA_p99,
      quantileExact(0.01)(PM)       AS PM_p01,
      quantileExact(0.99)(PM)       AS PM_p99,
      quantileExact(0.01)(ATO)      AS ATO_p01,
      quantileExact(0.99)(ATO)      AS ATO_p99,
      quantileExact(0.01)(RNOA)     AS RNOA_p01,
      quantileExact(0.99)(RNOA)     AS RNOA_p99,
      quantileExact(0.01)(delta_NOA)  AS delta_NOA_p01,
      quantileExact(0.99)(delta_NOA)  AS delta_NOA_p99,
      quantileExact(0.01)(delta_PM)   AS delta_PM_p01,
      quantileExact(0.99)(delta_PM)   AS delta_PM_p99,
      quantileExact(0.01)(delta_ATO)  AS delta_ATO_p01,
      quantileExact(0.99)(delta_ATO)  AS delta_ATO_p99,
      quantileExact(0.01)(delta_RNOA) AS delta_RNOA_p01,
      quantileExact(0.99)(delta_RNOA) AS delta_RNOA_p99
    FROM accounting_changes_input
    GROUP BY fyear
  ),
  -- Apply winsorization via JOIN back to the panel.
  clipped AS (
    SELECT
      p.gvkey,
      p.fyear,
      p.datadate,
      p.sic,
      p.AT, p.ACT, p.LCT, p.CHE, p.IVST, p.DLTT, p.DLC, p.CEQ, p.MIB, p.PSTK,
      p.OIADP, p.SALE, p.avg_NOA,
      -- Clip NOA into [NOA_p01, NOA_p99]
      least(greatest(p.NOA, b.NOA_p01), b.NOA_p99)        AS NOA_w,
      least(greatest(p.PM,  b.PM_p01),  b.PM_p99)         AS PM_w,
      least(greatest(p.ATO, b.ATO_p01), b.ATO_p99)        AS ATO_w,
      least(greatest(p.RNOA, b.RNOA_p01), b.RNOA_p99)     AS RNOA_w,
      least(greatest(p.delta_NOA,  b.delta_NOA_p01),  b.delta_NOA_p99)  AS delta_NOA_w,
      least(greatest(p.delta_PM,   b.delta_PM_p01),   b.delta_PM_p99)   AS delta_PM_w,
      least(greatest(p.delta_ATO,  b.delta_ATO_p01),  b.delta_ATO_p99)  AS delta_ATO_w,
      least(greatest(p.delta_RNOA, b.delta_RNOA_p01), b.delta_RNOA_p99) AS delta_RNOA_w,
      -- Keep raw values for downstream table-1 ID-check
      p.NOA, p.PM, p.ATO, p.RNOA,
      p.delta_NOA, p.delta_PM, p.delta_ATO, p.delta_RNOA
    FROM accounting_changes_input AS p
    INNER JOIN bounds AS b ON p.fyear = b.fyear
  )
SELECT * FROM clipped
SETTINGS max_execution_time = 600,
         max_rows_to_read = 500000000,
         timeout_before_checking_execution_speed = 0