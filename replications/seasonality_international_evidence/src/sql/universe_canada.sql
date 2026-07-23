-- universe_canada.sql
-- Purpose: CANADA equity universe — exactly ONE issue per Canadian firm (gvkey),
--          matching the global file's one-primary-issue-per-firm convention and
--          the paper's firm-level universe (see assumptions.md finding F6).
--          Canadian equities live in Compustat North America (Compustat Global
--          has essentially no Canadian coverage).
--
--          Deterministic selection (replaces the old "all excntry='CAN' issues"
--          of Assumption A2): for each Canadian gvkey, pick the iid with the
--          LARGEST total market cap over the sample (sum of month-end
--          prccd x cshoc across months, NULLs skipped); tie-break on the
--          lexicographically smallest iid. This removes the duplicate
--          (gvkey, month) rows that multi-issue firms (dual share classes /
--          listings) previously produced.
--
-- Tables: comp_202601.secd (NA daily, 159M rows), comp_202601.security (master)
-- Output columns: gvkey (String), iid (String), country (String = 'CAN')
--                 — exactly one row per gvkey.
-- Depends on: (none)
-- Settings: join_algorithm=hash (small issue list -> large daily fact),
--           max_execution_time, max_rows_to_read guards; ALWAYS filtered on datadate.
--
-- Data window: datadate 1979-12-01 .. 2006-06-30 (same as the panel build).
WITH
can_issues AS (
    -- every Canadian issue (candidate set), EXCLUDING firms domiciled in the 13
    -- global countries: those already enter via the global (g_company.loc) leg,
    -- so excluding them here keeps the two sources disjoint at the gvkey level
    -- (one firm, one country = domicile). Without this, ~11 foreign-domiciled
    -- firms cross-listed in Canada appear twice (once per source) — see finding F6.
    SELECT DISTINCT gvkey, iid
    FROM comp_202601.security
    WHERE excntry = 'CAN' AND gvkey IS NOT NULL AND iid IS NOT NULL
      AND gvkey NOT IN (
          SELECT gvkey FROM comp_202601.g_company
          WHERE loc IN ('AUT','BEL','FIN','FRA','DEU','ITA','JPN','NLD','NOR','ESP','SWE','CHE','GBR')
            AND gvkey IS NOT NULL
      )
),
-- month-end market cap per Canadian issue over the full data window
can_me AS (
    SELECT
        s.gvkey AS gvkey, s.iid AS iid,
        toDate(toStartOfMonth(toDate(s.datadate)) + INTERVAL 1 MONTH - INTERVAL 1 DAY) AS month,
        argMax(s.prccd, s.datadate) AS prccd,
        argMax(s.cshoc, s.datadate) AS cshoc
    FROM comp_202601.secd AS s
    INNER JOIN can_issues AS ci ON s.gvkey = ci.gvkey AND s.iid = ci.iid
    WHERE s.datadate >= '1979-12-01' AND s.datadate <= '2006-06-30'
      AND s.prccd IS NOT NULL AND s.prccd > 0
    GROUP BY s.gvkey, s.iid, month
),
-- total market cap per issue over the sample (NULL me skipped; sum -> 0 if none)
can_tot AS (
    SELECT gvkey, iid,
           sum(if(cshoc IS NOT NULL AND cshoc > 0, prccd * cshoc, 0)) AS tot_me
    FROM can_me
    GROUP BY gvkey, iid
),
-- rank: largest total market cap first; tie-break on lexicographically smallest iid
can_rank AS (
    SELECT gvkey, iid,
           row_number() OVER (PARTITION BY gvkey ORDER BY tot_me DESC, iid ASC) AS rn
    FROM can_tot
)
SELECT gvkey AS gvkey, iid AS iid, 'CAN' AS country
FROM can_rank
WHERE rn = 1
SETTINGS join_algorithm = 'hash',
         max_execution_time = 600,
         max_rows_to_read = 500000000000,
         timeout_before_checking_execution_speed = 0
