-- table_1_source.sql
-- Purpose: Analysis-ready Table I panel join from cached parquet artifacts.
-- Tables: data/panel.parquet, data/size_quintile.parquet
-- Output columns: permno, month, ret, r_bar_it, lag1..lag12, lag24, lag36, size_quintile
-- Depends on: preprocessing pipeline artifacts
-- Note: execution is optional; main.py reads the parquet artifacts directly.
SELECT * FROM file('data/panel.parquet', Parquet)
SETTINGS max_execution_time = 300, max_rows_to_read = 10000000000;
