"""
Build the CRSP-linked comp-CRSP panel for Lev & Nissim (2004)
Tables 4 and 5.

Pipeline:
  1. ClickHouse `crsp_panel.sql` runs the entire join + cum-ret computation.
  2. Save `data/panel_crsp.parquet`.
  3. Print summary stats.

The SQL produces one row per (gvkey, fyear) that has a PIT-link to a
CRSP permno, with E/P*, B/P, SIZE, LEV, PAY, and one-year-ahead
return pre-computed.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pandas as pd

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from clickhouse_driver import Client  # noqa: E402
from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402

SLUG = "lev_nissim_2004_taxable_income_future_earnings_and_equity_values"
LAYOUT = paper_layout(SLUG)
SQL_DIR = LAYOUT.src_path("sql")
_CFG = get_clickhouse_config()


def _client() -> Client:
    return Client(
        host=_CFG["host"],
        port=int(_CFG["port"]),
        user=_CFG["user"],
        password=_CFG["password"],
        settings={"max_execution_time": 600},
    )


def q(sql: str) -> pd.DataFrame:
    c = _client()
    try:
        data, cols = c.execute(sql, with_column_types=True)
    finally:
        c.disconnect()
    df = pd.DataFrame(data, columns=[x[0] for x in cols])
    # strip "l." prefix from column aliases
    df.columns = [c.replace("l.", "") for c in df.columns]
    for c in df.columns:
        if df[c].dtype == object:
            try:
                df[c] = pd.to_numeric(df[c])
            except (ValueError, TypeError):
                pass
    return df


def q_file(name: str) -> pd.DataFrame:
    return q((SQL_DIR / name).read_text())


def run_crsp_panel() -> pd.DataFrame:
    LAYOUT.ensure()

    print("[1/3] running crsp_panel.sql ...")
    t0 = time.time()
    df = q_file("crsp_panel.sql")
    elapsed = time.time() - t0
    print(f"      pulled {len(df):,} rows × {len(df.columns)} cols in {elapsed:.1f}s")

    # Save parquet
    print("\n[2/3] write data/panel_crsp.parquet ...")
    parquet_path = LAYOUT.data_path("panel_crsp.parquet")
    df.to_parquet(parquet_path, index=False)
    print(f"      wrote {parquet_path} ({parquet_path.stat().st_size / 1e6:.2f} MB)")

    # Summary stats
    print("\n[3/3] summary stats")
    print(f"      rows: {len(df):,}, unique gvkeys: {df['gvkey'].nunique():,}, "
          f"unique permnos: {df['permno'].nunique():,}, "
          f"fyear: {int(df['fyear'].min())}-{int(df['fyear'].max())}")

    print(f"      n with cum_ret_jan_april: {int(df['cum_ret_jan_april'].notna().sum()):,}")
    print(f"      n with cum_ret_may_april: {int(df['cum_ret_may_april'].notna().sum()):,}")
    print(f"      n with me_april: {int(df['me_april'].notna().sum()):,}")
    print(f"      n with pstar: {int(df['pstar'].notna().sum()):,}")
    print(f"      n with epstar_pct: {int(df['epstar_pct'].notna().sum()):,}")
    print(f"      n with lev: {int(df['lev'].notna().sum()):,}")
    print(f"      n with pay: {int(df['pay'].notna().sum()):,}")
    print(f"      n with b_to_p: {int(df['b_to_p'].notna().sum()):,}")
    print(f"      n with r_tax: {int(df['r_tax'].notna().sum()):,}")

    # Key distributions
    if df["cum_ret_jan_april"].notna().sum():
        s = df["cum_ret_jan_april"].dropna()
        print(f"\n      cum_ret_jan_april: mean={s.mean():.4f}, "
              f"median={s.median():.4f}, "
              f"5%={s.quantile(.05):.4f}, 95%={s.quantile(.95):.4f}, "
              f"min={s.min():.4f}, max={s.max():.4f}")
    if df["cum_ret_may_april"].notna().sum():
        s = df["cum_ret_may_april"].dropna()
        print(f"      cum_ret_may_april: mean={s.mean():.4f}, "
              f"median={s.median():.4f}, "
              f"5%={s.quantile(.05):.4f}, 95%={s.quantile(.95):.4f}, "
              f"min={s.min():.4f}, max={s.max():.4f}")
    if df["epstar_pct"].notna().sum():
        s = df["epstar_pct"].dropna()
        print(f"      epstar_pct: mean={s.mean():.4f}, "
              f"median={s.median():.4f}, "
              f"5%={s.quantile(.05):.4f}, 95%={s.quantile(.95):.4f}, "
              f"min={s.min():.4f}, max={s.max():.4f}")

    # Headline test for T4: R_TAX should correlate negatively with E/P*
    # in the post-SFAS panel (paper claim C4)
    print("\n      Mean E/P* by R_TAX quintile (post-SFAS 1993-2000):")
    sub = df[(df.fyear >= 1993) & df.r_tax.notna() & df.epstar_pct.notna()]
    grp = sub.groupby("r_tax")["epstar_pct"].agg(["count", "mean", "median"])
    for q, row in grp.iterrows():
        print(f"        R_TAX={int(q)}: n={int(row['count']):>5,}  "
              f"mean={row['mean']:+.4f}  median={row['median']:+.4f}")

    # Headline test for T5: one-year-ahead return by R_TAX (pre-SFAS 1987-1992)
    print("\n      Mean one-year-ahead return by R_TAX quintile (pre-SFAS 1987-1992):")
    sub2 = df[(df.fyear >= 1987) & (df.fyear <= 1992)
              & df.r_tax.notna() & df.cum_ret_may_april.notna()]
    grp2 = sub2.groupby("r_tax")["cum_ret_may_april"].agg(["count", "mean", "median"])
    for q, row in grp2.iterrows():
        print(f"        R_TAX={int(q)}: n={int(row['count']):>5,}  "
              f"mean={row['mean']:+.4f}  median={row['median']:+.4f}")

    print("\n      Mean one-year-ahead return by R_TAX quintile (post-SFAS 1993-2000):")
    sub3 = df[(df.fyear >= 1993) & df.r_tax.notna() & df.cum_ret_may_april.notna()]
    grp3 = sub3.groupby("r_tax")["cum_ret_may_april"].agg(["count", "mean", "median"])
    for q, row in grp3.iterrows():
        print(f"        R_TAX={int(q)}: n={int(row['count']):>5,}  "
              f"mean={row['mean']:+.4f}  median={row['median']:+.4f}")

    return df


def main() -> int:
    LAYOUT.ensure()
    parquet_path = LAYOUT.data_path("panel_crsp.parquet")
    run_crsp_panel()
    print(f"\n[done] {parquet_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())