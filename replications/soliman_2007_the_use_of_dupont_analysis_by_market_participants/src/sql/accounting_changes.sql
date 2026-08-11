-- accounting_changes.sql
-- Purpose: Compute ΔNOA, ΔPM, ΔATO (from lagged values) and ΔRNOA_{t+1}
--          (from forward RNOA) on top of comp_fundamentals output.
-- Tables: in-memory CTE chain — does not query ClickHouse. Reads panel from
--         data/panel.parquet via Python (main.py) for this purpose OR is
--         appended as CTEs in panel.sql.
-- Output columns: gvkey, fyear, ..., NOA, NOA_lag1, PM, ATO, RNOA,
--                  ΔNOA, ΔPM, ΔATO, ΔRNOA (forward change RNOA_{t+1} - RNOA_t)
-- Depends on: comp_fundamentals.sql
--
-- Strategy: build a panel CTE chain with self-joins via ASOF on (gvkey, fyear)
-- to bring lagged (fyear-1) and forward (fyear+1) values into the current row.
-- We use ANY-INNER JOIN on (gvkey, fyear-1) for lagged values and
-- (gvkey, fyear+1) for forward RNOA — straightforward since fyear is integer.
--
-- This file is run as a stand-alone ClickHouse query that loads its input
-- from the comp_fundamentals SQL via `INSERT INTO ... SELECT` pattern.
-- In this implementation, the entire CTE chain is collapsed into a single
-- `INSERT INTO table_x SELECT ... FROM (comp_fundamentals_query)` so that
-- we don't materialize a huge intermediate. Here we present the logical
-- CTE chain; main.py executes the entire query (panel.sql).

WITH
  base AS (
    -- Pulls from comp_fundamentals.sql output via subquery.
    -- The actual SQL execution embeds comp_fundamentals.sql as a CTE subquery;
    -- see panel.sql for the consolidated form.
    SELECT *
    FROM comp_fundamentals
  ),
  -- Self-join on (gvkey, fyear+1) to fetch next-year NOA and RNOA
  forward AS (
    SELECT
      b.gvkey, b.fyear,
      nx.NOA   AS NOA_fwd,
      nx.RNOA  AS RNOA_fwd
    FROM base AS b
    LEFT JOIN base AS nx
      ON b.gvkey = nx.gvkey AND b.fyear = nx.fyear - 1
  ),
  changes AS (
    SELECT
      b.*,
      -- ΔNOA = (NOA_t - NOA_{t-1}) / NOA_{t-1}
      (b.NOA - b.NOA_lag1) / b.NOA_lag1 AS delta_NOA,
      -- ΔPM = PM_t - PM_{t-1}
      b.PM - lagInFrame(b.PM, 1) OVER w AS delta_PM,
      -- ΔATO = ATO_t - ATO_{t-1}
      b.ATO - lagInFrame(b.ATO, 1) OVER w AS delta_ATO,
      -- ΔRNOA = RNOA_{t+1} - RNOA_t  (forward)
      f.RNOA_fwd - b.RNOA AS delta_RNOA
    FROM base AS b
    INNER JOIN forward AS f ON b.gvkey = f.gvkey AND b.fyear = f.fyear
    WINDOW w AS (PARTITION BY b.gvkey ORDER BY b.fyear
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  )
SELECT
  gvkey, fyear, datadate, sic,
  AT, ACT, LCT, CHE, IVST, DLTT, DLC, CEQ, MIB, PSTK,
  OIADP, SALE, NOA, avg_NOA,
  PM, ATO, RNOA,
  delta_NOA, delta_PM, delta_ATO, delta_RNOA
FROM changes
SETTINGS max_execution_time = 600,
         max_rows_to_read = 500000000,
         timeout_before_checking_execution_speed = 0