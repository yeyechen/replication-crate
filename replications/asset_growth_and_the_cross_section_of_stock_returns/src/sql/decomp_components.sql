-- decomp_components.sql
-- Purpose: Deduplicated Compustat annual fundamentals carrying ONLY the data items
--          needed for the Table IV balance-sheet decomposition of asset growth, so
--          the investment/financing components can be (re)computed and VALIDATED
--          against data/formation.parquet's d_* columns.
-- Tables: comp_202601.funda
-- Output columns: gvkey, fyear, datadate, at, ch, act, ppegt, re, pstk, ceq, mib,
--                 dltt, dlc   (all $MILLIONS; one row per (gvkey, fyear))
-- Depends on: (none)
-- Notes:
--   * Component definitions (Table IV caption, content.md L2678; rules
--     var_decomp_investment / var_decomp_financing / var_decomp_scaling):
--       INVESTMENT side (sums to ASSETG = (at[t-1]-at[t-2])/at[t-2]):
--         d_cash      = (ch[t-1]   - ch[t-2])                       / at[t-2]   (#30 cash; paper "#1")
--         d_curasst   = ((act-ch)[t-1] - (act-ch)[t-2])             / at[t-2]   (#4 - #1 noncash current)
--         d_ppe       = (ppegt[t-1]- ppegt[t-2])                    / at[t-2]   (#8 gross PPE)
--         d_othassets = ASSETG - d_cash - d_curasst - d_ppe                     (residual)
--       FINANCING side (sums to ASSETG):
--         d_re        = (re[t-1]   - re[t-2])                       / at[t-2]   (#36)
--         d_stock     = ((pstk+ceq+mib-re)[t-1] - (...)[t-2])       / at[t-2]   (#130+#60+#38-#36)
--         d_debt      = ((dltt+dlc)[t-1] - (dltt+dlc)[t-2])         / at[t-2]   (#9+#34)
--         d_opliab    = ASSETG - d_re - d_stock - d_debt                        (residual)
--     Changes are FY t-2 -> FY t-1, scaled by at in FY t-2. This query pulls the raw
--     items; the change/scale arithmetic is applied in table_4.py (lag-merge on fyear),
--     exactly mirroring src/main.py build_fundamentals so the recomputation is
--     bit-comparable to the foundation.
--   * DATES ARE RETURNED AS ISO STRINGS (ClickHouse Date clamps pre-1970 to epoch).
--   * Same WRDS industrial dedup as comp_fundamentals.sql (Assumption 3):
--     indfmt='INDL', consol='C', datafmt='STD', popsrc='D'; ROW_NUMBER keeping the
--     non-null-at row, then latest datadate -> one row per (gvkey, fyear).
WITH filtered AS (
    SELECT
        gvkey, fyear, datadate,
        at, ch, act, ppegt, re, pstk, ceq, mib, dltt, dlc
    FROM comp_202601.funda
    WHERE indfmt = 'INDL'
      AND consol = 'C'
      AND datafmt = 'STD'
      AND popsrc = 'D'
      AND fyear >= 1960 AND fyear <= 2003
      AND gvkey IS NOT NULL
      AND datadate IS NOT NULL
),
ranked AS (
    SELECT
        f.*,
        row_number() OVER (
            PARTITION BY f.gvkey, f.fyear
            ORDER BY isNull(f.at) ASC, f.datadate DESC
        ) AS rn
    FROM filtered AS f
)
SELECT
    gvkey, fyear, datadate,
    at, ch, act, ppegt, re, pstk, ceq, mib, dltt, dlc
FROM ranked
WHERE rn = 1
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
