"""
Belo, Lin, Bazdresch (2014) — Labor Hiring, Investment, and Stock Return
Predictability — pipeline build.

This module builds the monthly analysis panel from CRSP (stock returns,
market equity) and Compustat (HN, IK, ROA, KM). All heavy lifting
(universe filtering, PIT joins, signal aggregation) is done in ClickHouse
SQL; Python orchestrates the calls and writes the final parquet.

Reads the following SQL files from src/sql/:
    - universe_monthly.sql : CRSP msf + dsenames PIT-filtered monthly universe
    - compustat_funda.sql  : Compustat funda with FY-level HN, IK, ROA
    - panel.sql            : Final monthly panel with all variables (single CTE pipeline)

Output:
    - data/panel.parquet   : Final analysis panel
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from clickhouse_driver import Client

from utils.env import get_clickhouse_config, load_project_env
from utils.paths import paper_layout


# --- configuration ----------------------------------------------------------

load_project_env()
LAYOUT = paper_layout("belo_lin_bazdresch_2014_labor_hiring_investment_and_stock_return_predictability")
LAYOUT.ensure()

CFG = get_clickhouse_config()
SQL_DIR = LAYOUT.src_path("sql")
DATA_DIR = LAYOUT.data_path("")

# Parameters from preprocessing_rules.json (paper §2.1).
SAMPLE_START = "1965-07-01"
SAMPLE_END   = "2010-06-30"
COMP_START   = "1962-01-01"   # compustat datadate window start (need fyear 1963 for HN)
COMP_END     = "2011-12-31"   # compustat datadate window end   (need fyear 2009 for sample)


# --- ClickHouse connection --------------------------------------------------

def _client() -> Client:
    return Client(
        host=CFG["host"],
        port=int(CFG["port"]),
        user=CFG["user"],
        password=CFG["password"],
        settings={"max_execution_time": 900},
    )


def q(sql: str) -> pd.DataFrame:
    """Execute a SQL query (string) and return a DataFrame."""
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    """Read a .sql file from src/sql/ and execute it."""
    sql = (SQL_DIR / name).read_text()
    return q(sql)


# --- pipeline ---------------------------------------------------------------

def build_universe_monthly() -> pd.DataFrame:
    """Step 1: PIT-filtered monthly stock universe (CRSP msf + dsenames)."""
    print(f"[1/3] Running src/sql/universe_monthly.sql ...")
    df = q_file("universe_monthly.sql")
    print(f"      universe_monthly: {len(df):,} rows, "
          f"{df['permno'].nunique():,} permnos, {df['month'].nunique():,} months")
    out = LAYOUT.data_path("universe_monthly.parquet")
    df.to_parquet(out, index=False)
    print(f"      wrote {out}")
    return df


def build_compustat_funda() -> pd.DataFrame:
    """Step 2: Compustat annual fundamentals with HN/IK/ROA signals."""
    print(f"[2/3] Running src/sql/compustat_funda.sql ...")
    df = q_file("compustat_funda.sql")
    print(f"      compustat_funda: {len(df):,} rows, "
          f"{df['gvkey'].nunique():,} gvkeys, fyear range "
          f"{int(df['fyear'].min())}-{int(df['fyear'].max())}")
    out = LAYOUT.data_path("compustat_funda.parquet")
    df.to_parquet(out, index=False)
    print(f"      wrote {out}")
    return df


def build_panel() -> pd.DataFrame:
    """Step 3: Final monthly panel (single CTE pipeline in ClickHouse)."""
    print(f"[3/3] Running src/sql/panel.sql ...")
    df = q_file("panel.sql")
    print(f"      panel: {len(df):,} rows")
    out = LAYOUT.data_path("panel.parquet")
    df.to_parquet(out, index=False)
    print(f"      wrote {out}")
    return df


# --- diagnostics ------------------------------------------------------------

def diagnostics(panel: pd.DataFrame) -> None:
    """Print summary stats for the panel: dimensions, signal distributions."""
    print("\n=== Panel diagnostics ===")
    print(f"Total rows: {len(panel):,}")
    print(f"Unique months: {panel['month'].nunique()}")
    print(f"Month range: {panel['month'].min()} to {panel['month'].max()}")
    print(f"Unique permnos: {panel['permno'].nunique():,}")
    print(f"Unique gvkeys: {panel['gvkey'].nunique():,}")

    firm_year_any = panel.dropna(subset=["fyear"]).groupby(["gvkey", "fyear"]).size().shape[0]
    firm_year_hn = (
        panel.dropna(subset=["hn"]).groupby(["gvkey", "fyear"]).size().shape[0]
    )
    firm_year_hn_ik = (
        panel.dropna(subset=["hn", "ik"]).groupby(["gvkey", "fyear"]).size().shape[0]
    )
    print(f"Unique (gvkey, fyear) — any signal: {firm_year_any:,}")
    print(f"Unique (gvkey, fyear) — valid hn only: {firm_year_hn:,}  (paper: 75,381)")
    print(f"Unique (gvkey, fyear) — valid hn AND ik: {firm_year_hn_ik:,}")

    print("\n=== Signal distributions ===")
    for col in ["hn", "ik", "roa", "km", "size", "me_dollars", "ret"]:
        if col in panel.columns:
            s = panel[col]
            n_valid = s.notna().sum()
            pct_null = 100.0 * (1.0 - n_valid / max(len(s), 1))
            print(f"{col:>12s}: n_valid={n_valid:>12,}  null%={pct_null:>5.1f}  "
                  f"mean={s.mean():>14.6f}  std={s.std():>14.6f}  "
                  f"min={s.min():>14.6f}  max={s.max():>14.6f}")

    # HN bounded check (paper says bounded ±200%)
    hn = panel["hn"].dropna()
    print(f"\n  HN bound check: rows with |HN| > 2: {(hn.abs() > 2).sum()}")
    print(f"  HN bound check: rows with |HN| > 3: {(hn.abs() > 3).sum()}")


def sanity_check_ibm() -> None:
    """30-second single-stock sanity check: pull IBM observations and verify
    signs, units, and magnitudes for HN, IK, ROA, KM."""
    print("\n=== Sanity check (IBM permno=12490, gvkey='006066') ===")
    p = LAYOUT.data_path("panel.parquet")
    if not p.exists():
        print(f"  (panel.parquet missing — skipping)")
        return
    panel = pd.read_parquet(p)
    ibm = panel[(panel["permno"] == 12490) | (panel["gvkey"] == "006066")].sort_values("month")
    print(f"  IBM rows: {len(ibm):,}")
    if len(ibm) == 0:
        return

    me = ibm["me_dollars"]
    print(f"  me_dollars: mean={me.mean():>15,.0f}  min={me.min():>15,.0f}  "
          f"max={me.max():>15,.0f}")
    print(f"  size (log ME): mean={ibm['size'].mean():.2f}  "
          f"min={ibm['size'].min():.2f}  max={ibm['size'].max():.2f}")
    hn_valid = ibm["hn"].dropna()
    ik_valid = ibm["ik"].dropna()
    roa_valid = ibm["roa"].dropna()
    if len(hn_valid) > 0:
        print(f"  hn: n={len(hn_valid):,}  mean={hn_valid.mean():.4f}  "
              f"min={hn_valid.min():.4f}  max={hn_valid.max():.4f}")
    if len(ik_valid) > 0:
        print(f"  ik: n={len(ik_valid):,}  mean={ik_valid.mean():.4f}  "
              f"min={ik_valid.min():.4f}  max={ik_valid.max():.4f}")
    if len(roa_valid) > 0:
        print(f"  roa: n={len(roa_valid):,}  mean={roa_valid.mean():.4f}  "
              f"min={roa_valid.min():.4f}  max={roa_valid.max():.4f}")

    # Spot check: HN should be bounded by ±200% and values like 0.5 indicate
    # IBM hired ~50% more workers year-over-year (extreme but valid).
    print(f"  HN bound check (paper says ±200%): "
          f"{(hn_valid.abs() > 2).sum()} rows violate")


# --- main -------------------------------------------------------------------

def main() -> None:
    """Build the analysis panel: universe → compustat signals → final panel."""
    # Step 1+2 produce intermediates useful for debugging but not strictly
    # required by panel.sql (which inlines them as CTEs). Run them anyway
    # so the parquets exist as audit points.
    build_universe_monthly()
    build_compustat_funda()

    # Step 3 is the actual final panel.
    panel = build_panel()
    diagnostics(panel)
    sanity_check_ibm()


if __name__ == "__main__":
    main()
