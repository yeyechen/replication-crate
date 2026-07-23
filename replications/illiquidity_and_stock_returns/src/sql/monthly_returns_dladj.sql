-- monthly_returns_dladj.sql
-- Purpose: Delisting-adjusted monthly returns (decimal) for the Table 2
--          Fama-MacBeth panel, returns years y = 1964..1997
--          (Amihud 2002 §2.2; Shumway 1997; Assumption 10).
-- Mechanics:
--   - monthly return from crsp_202601.msf (ret, with dividends);
--     ret < -1 (CRSP missing sentinels -55/-66/-77/-88/-99) -> NULL.
--   - the adjustment applies to a stock's FINAL msf month on CRSP
--     (max msf date over the FULL table, so stocks surviving past 1997
--     are never adjusted inside the panel window).
--   - dlret_star = dsedelist.dlret when non-null (kept as-is even when
--     = -1, paper footnote 9); else -0.30 when dlstcd is in the paper's
--     list {500, 520, 551-574, 580, 584}; else NULL (no adjustment).
--     (No dlret < -1 sentinels exist in this vintage — verified.)
--   - final-month return:
--       ret_last valid & dlret_star non-null -> (1+ret_last)(1+dlret*)-1
--       ret_last null  & dlret_star non-null -> dlret_star
--       dlret_star null                      -> ret_last unchanged
--   - rows restricted to the panel keys (permno, returns-year y) built
--     by main.py from characteristics_annual output (characteristics
--     year y-1 exists) via session temp table _amihud_panel_keys.
-- Tables: crsp_202601.msf, crsp_202601.dsedelist, temp _amihud_panel_keys
-- Output columns: permno, y, mo (1..12), ret_adj
-- Depends on: temp table _amihud_panel_keys (permno Int32, y Int32)
-- Note: toDate32 everywhere (Date saturates pre-1970); max(date) is a
--       lexicographic max on ISO strings (= chronological).
WITH last_msf AS (
    SELECT permno, max(date) AS last_date
    FROM crsp_202601.msf
    GROUP BY permno
),
dl AS (
    SELECT
        permno,
        if(dlret IS NOT NULL AND dlret >= -1,
           dlret,
           if(dlstcd IN (500, 520, 551, 552, 553, 554, 555, 556, 557, 558,
                         559, 560, 561, 562, 563, 564, 565, 566, 567, 568,
                         569, 570, 571, 572, 573, 574, 580, 584),
              -0.30,
              NULL)) AS dlret_star
    FROM crsp_202601.dsedelist
),
mret AS (
    SELECT
        m.permno                   AS permno,
        toYear(toDate32(m.date))   AS y,
        toMonth(toDate32(m.date))  AS mo,
        m.date                     AS date,
        if(m.ret IS NOT NULL AND m.ret >= -1, m.ret, NULL) AS ret_clean
    FROM crsp_202601.msf AS m
    INNER JOIN _amihud_panel_keys AS k
        ON m.permno = k.permno AND toYear(toDate32(m.date)) = k.y
    WHERE m.date >= '1964-01-01' AND m.date <= '1997-12-31'
)
SELECT
    r.permno AS permno,
    r.y      AS y,
    r.mo     AS mo,
    multiIf(
        r.date = l.last_date AND d.dlret_star IS NOT NULL AND r.ret_clean IS NOT NULL,
            (1 + r.ret_clean) * (1 + d.dlret_star) - 1,
        r.date = l.last_date AND d.dlret_star IS NOT NULL,
            d.dlret_star,
        r.ret_clean
    ) AS ret_adj
FROM mret AS r
LEFT JOIN last_msf AS l ON r.permno = l.permno
LEFT JOIN dl       AS d ON r.permno = d.permno
ORDER BY r.permno, r.y, r.mo
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
