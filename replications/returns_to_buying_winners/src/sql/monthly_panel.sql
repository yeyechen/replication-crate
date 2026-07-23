-- monthly_panel.sql
-- Purpose: analysis-ready monthly stock panel for Jegadeesh & Titman (1993),
--          "Returns to Buying Winners and Selling Losers", JF 48(1).
--          One row per permno x calendar month (1926-07 .. 1989-12; the daily
--          window was extended back from 1962-07 in outer iteration 2,
--          audit-1 M1, for the Table VIII back-test — 6-month formations from
--          1927-01 need cumret_6 over 1926-07..1926-12. The 1962-07..1989-12
--          region is bit-identical to the pre-extension panel at 1965/1975/
--          1985 stock-months — snapshot-verified in ensure_panel; the only
--          cells that can differ are warm-up cumrets at 1962-07..1963-06,
--          which no table uses). The panel
--          carries BOTH delisting treatments (Assumption A3-revision, inner
--          iteration 3: PRIMARY = unadjusted; adjusted = sensitivity):
--            ret          ADJUSTED monthly return = prod(1 + daily ret) - 1
--                         over the month's trading days, multiplied by
--                         (1 + delisting adj) when the stock delists within
--                         the month (sensitivity series).
--            ret_raw      UNADJUSTED monthly return = exp(sum(log(1+ret)))-1
--                         over the month's valid days; NO dlret applied, no
--                         fallback (PRIMARY series). NULLs iff the stock has
--                         no valid trading days in the month (identical null
--                         pattern to `ret`, verified).
--            ret_skip5    partial-month return from the 6th valid trading day
--                         on (Panel B first holding month; NULL if the stock
--                         has fewer than 6 trading days in the month).
--                         Delisting adjustment is NOT applied (P3).
--            ret_skip5_raw  raw-series twin of ret_skip5 for the Panel B
--                         PRIMARY machinery. IDENTICAL to ret_skip5 by
--                         construction — ret_skip5 never carried a delisting
--                         adjustment (P3) — carried as its own column so the
--                         raw column set is self-contained.
--            cumret_3/6/9/12    formation-period compounded return over the
--                         previous J calendar months: prod(1 + ret) - 1 over
--                         months [m-J, m-1] of the ADJUSTED series; NULL
--                         unless count(ret) = J over the window.
--            cumret_3/6/9/12_raw  same windows compounded from ret_raw; NULL
--                         unless count(ret_raw) = J over the window (same
--                         null pattern as cumret_J since ret_raw/ret nulls
--                         coincide).
--            me_millions  month-end market cap = abs(prc)*shrout*1000/1e6,
--                         last trading day of the month (prc signed $/share ->
--                         abs first; shrout in thousands).
--          Rows are kept where the stock traded in-universe that month
--          (ret non-NULL) OR is formation-eligible that month (cumret_3
--          non-NULL — e.g. the month right after a delisting, so the
--          formation cross-section stays complete).
-- Tables: crsp_202601.dsf, crsp_202601.dsenames, crsp_202601.dsedelist
-- Output columns: permno, month, ret, ret_raw, ret_skip5, ret_skip5_raw,
--                 cumret_3, cumret_3_raw, cumret_6, cumret_6_raw, cumret_9,
--                 cumret_9_raw, cumret_12, cumret_12_raw, me_millions
-- Depends on: universe_daily.sql and delisting_adjust.sql — src/main.py
--             embeds them (trailing settings clauses stripped) as the
--             `universe_daily` and `delist` CTEs at the two include markers
--             below, so the SQL logic has a single source of truth.
-- NOTE: months are 'YYYY-MM' strings throughout — ClickHouse Date saturates
--       pre-1970 dates to 1970-01-01 (verified; toDate32 does NOT saturate,
--       hence its use for the grid anchor below). Window frames are ROWS-based
--       over the complete per-permno 762-month grid, so "J PRECEDING .. 1
--       PRECEDING" spans exactly J calendar months; count(ret) = J over the
--       frame enforces "all J months available".
-- NOTE: compounding via exp(sum(log(...))) with log(greatest(1+ret, 1e-300))
--       so a -100% delisting month (1+ret = 0) yields cumret -> -1 instead of
--       NaN. join_use_nulls = 1 is REQUIRED so non-matching LEFT JOIN rows
--       (grid months with no trading) are NULL, not Float64 defaults.
WITH universe_daily AS
(
-- @@universe_daily@@
),
delist AS
(
-- @@delist@@
),
monthly_agg AS
(
    SELECT
        permno,
        month,
        exp(sum(log(greatest(1 + ret, 1e-300)))) - 1 AS ret_raw,
        if(count() >= 6,
           exp(sumIf(log(greatest(1 + ret, 1e-300)), day_rank >= 6)) - 1,
           NULL) AS ret_skip5,
        -- raw-series twin of the skip-5 partial month; same expression as
        -- ret_skip5 (skip5 never carried a delisting adjustment — P3).
        if(count() >= 6,
           exp(sumIf(log(greatest(1 + ret, 1e-300)), day_rank >= 6)) - 1,
           NULL) AS ret_skip5_raw,
        argMax(if(prc IS NOT NULL AND shrout IS NOT NULL AND abs(prc) * shrout > 0,
                  abs(prc) * shrout / 1000, NULL), date) AS me_millions
    FROM universe_daily
    GROUP BY permno, month
),
adjusted AS
(
    SELECT
        m.permno AS permno,
        m.month AS month,
        (1 + m.ret_raw) * (1 + if(e.permno IS NOT NULL,
                                  coalesce(e.dlret_clean,
                                           if(e.dlstcd >= 500, -0.30, 0.0)),
                                  0.0)) - 1 AS ret,
        m.ret_raw AS ret_raw,
        m.ret_skip5 AS ret_skip5,
        m.ret_skip5_raw AS ret_skip5_raw,
        m.me_millions AS me_millions
    FROM monthly_agg AS m
    LEFT JOIN delist AS e
        ON m.permno = e.permno
       AND e.dlst_month = m.month
),
permnos AS
(
    SELECT DISTINCT permno FROM adjusted
),
months AS
(
    -- 762 months: 1926-07 .. 1989-12 inclusive ((1989*12+12)-(1926*12+7)+1)
    SELECT formatDateTime(addMonths(toDate32('1926-07-01'), x), '%Y-%m') AS month
    FROM (SELECT arrayJoin(range(762)) AS x)
),
grid AS
(
    SELECT p.permno AS permno, mm.month AS month
    FROM permnos AS p
    CROSS JOIN months AS mm
),
panel_raw AS
(
    SELECT
        g.permno AS permno,
        g.month AS month,
        a.ret AS ret,
        a.ret_raw AS ret_raw,
        a.ret_skip5 AS ret_skip5,
        a.ret_skip5_raw AS ret_skip5_raw,
        a.me_millions AS me_millions
    FROM grid AS g
    LEFT JOIN adjusted AS a
        ON g.permno = a.permno
       AND g.month = a.month
),
windowed AS
(
    SELECT
        permno,
        month,
        ret,
        ret_raw,
        ret_skip5,
        ret_skip5_raw,
        if(count(ret) OVER w3 = 3,
           exp(sum(log(greatest(1 + ret, 1e-300))) OVER w3) - 1, NULL) AS cumret_3,
        if(count(ret_raw) OVER w3 = 3,
           exp(sum(log(greatest(1 + ret_raw, 1e-300))) OVER w3) - 1, NULL) AS cumret_3_raw,
        if(count(ret) OVER w6 = 6,
           exp(sum(log(greatest(1 + ret, 1e-300))) OVER w6) - 1, NULL) AS cumret_6,
        if(count(ret_raw) OVER w6 = 6,
           exp(sum(log(greatest(1 + ret_raw, 1e-300))) OVER w6) - 1, NULL) AS cumret_6_raw,
        if(count(ret) OVER w9 = 9,
           exp(sum(log(greatest(1 + ret, 1e-300))) OVER w9) - 1, NULL) AS cumret_9,
        if(count(ret_raw) OVER w9 = 9,
           exp(sum(log(greatest(1 + ret_raw, 1e-300))) OVER w9) - 1, NULL) AS cumret_9_raw,
        if(count(ret) OVER w12 = 12,
           exp(sum(log(greatest(1 + ret, 1e-300))) OVER w12) - 1, NULL) AS cumret_12,
        if(count(ret_raw) OVER w12 = 12,
           exp(sum(log(greatest(1 + ret_raw, 1e-300))) OVER w12) - 1, NULL) AS cumret_12_raw,
        me_millions
    FROM panel_raw
    WINDOW
        w3 AS (PARTITION BY permno ORDER BY month
               ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING),
        w6 AS (PARTITION BY permno ORDER BY month
               ROWS BETWEEN 6 PRECEDING AND 1 PRECEDING),
        w9 AS (PARTITION BY permno ORDER BY month
               ROWS BETWEEN 9 PRECEDING AND 1 PRECEDING),
        w12 AS (PARTITION BY permno ORDER BY month
                ROWS BETWEEN 12 PRECEDING AND 1 PRECEDING)
)
SELECT
    toInt32(permno) AS permno,
    month AS month,
    ret AS ret,
    ret_raw AS ret_raw,
    ret_skip5 AS ret_skip5,
    ret_skip5_raw AS ret_skip5_raw,
    cumret_3 AS cumret_3,
    cumret_3_raw AS cumret_3_raw,
    cumret_6 AS cumret_6,
    cumret_6_raw AS cumret_6_raw,
    cumret_9 AS cumret_9,
    cumret_9_raw AS cumret_9_raw,
    cumret_12 AS cumret_12,
    cumret_12_raw AS cumret_12_raw,
    me_millions AS me_millions
FROM windowed
WHERE ret IS NOT NULL OR cumret_3 IS NOT NULL
SETTINGS
    join_algorithm = 'hash',
    join_use_nulls = 1,
    max_execution_time = 3600,
    max_rows_to_read = 60000000000,
    timeout_before_checking_execution_speed = 0;
