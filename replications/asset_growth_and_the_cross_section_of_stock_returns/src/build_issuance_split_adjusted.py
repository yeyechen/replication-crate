"""
Cooper, Gulen, Schill (2008) — split-adjusted ISSUANCE for Table I (Assumption 8
refinement, audit issue M1).

Builds a SPLIT-ADJUSTED 5-year share-change series so that mechanical stock-split
share increases are NOT counted as equity issuance:

    split_adj_shares(FY) = csho(FY) * cfacshr(at the fiscal-year-end datadate)
    ISSUANCE_sa(permno, june_year t) = split_adj_shares(FY t-1)/split_adj_shares(FY t-5) - 1

CRSP cfacshr convention (VERIFIED on permno 10032 = gvkey 012945, which has 2:1
splits in 1997-08 and 2000-09): on a 2:1 split shrout doubles while cfacshr halves,
so shrout*cfacshr is CONTINUOUS across the split -> multiplying shares by cfacshr
REMOVES splits. cfacshr is well-populated back to 1965 (~99.5%), covering the full
sample (no pre-1983 gap).

The split-adjusted shares come from src/sql/issuance_split_adjusted.sql (funda csho
+ CRSP cfacshr attached at each fiscal-year-end via the SAME PIT CRSP-Compustat link
the foundation uses). The (permno, june_year) -> gvkey mapping replicates the
foundation's June-t link EXACTLY, and the deciles are read from data/formation.parquet
(NOT recomputed), so the split-adjusted column lands on the identical (permno,
june_year, decile) keys as the raw column it refines.

Output: data/issuance_split_adjusted.parquet
        columns: permno, june_year, decile, ISSUANCE_split_adj, ISSUANCE_raw

Does NOT modify data/formation.parquet or data/panel.parquet.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

SLUG_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SLUG_DIR.parents[1]                       # rep-it-up root (carries utils/)
sys.path.insert(0, str(REPO_ROOT))
os.environ.setdefault("REPLICATIONS_PATH", str(REPO_ROOT / "replications"))

from utils.env import get_clickhouse_config            # noqa: E402

DATA = SLUG_DIR / "data"
SQL_DIR = SLUG_DIR / "src" / "sql"
N_DECILES = 10
FIRST_FORMATION, LAST_FORMATION = 1968, 2002          # 35 june_years
FORMATION_YEARS = list(range(FIRST_FORMATION, LAST_FORMATION + 1))

_CFG = get_clickhouse_config()


def _client() -> Client:
    return Client(host=_CFG["host"], port=int(_CFG["port"]), user=_CFG["user"],
                  password=_CFG["password"], database=_CFG["database"],
                  settings={"max_execution_time": 900})


def q(sql: str) -> pd.DataFrame:
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def build_split_adjusted_issuance() -> pd.DataFrame:
    # --- 1. split-adjusted shares at each (gvkey, fyear) ---------------------
    sa = q((SQL_DIR / "issuance_split_adjusted.sql").read_text())
    sa["cfacshr"] = pd.to_numeric(sa["cfacshr"], errors="coerce")
    sa["csho"] = pd.to_numeric(sa["csho"], errors="coerce")
    sa = sa[(sa["cfacshr"] > 0) & (sa["csho"] > 0)].copy()
    sa["split_adj"] = sa["csho"] * sa["cfacshr"]
    sa["june_year"] = sa["fyear"] + 1
    # one split-adjusted share value per (gvkey, june_year) [== per (gvkey, fyear)]
    sa = (sa[["gvkey", "june_year", "fyear", "split_adj"]]
          .drop_duplicates(["gvkey", "fyear"], keep="last"))
    n_cf = int((sa["split_adj"].notna()).sum())
    print(f"[sa] split-adjusted shares: {len(sa)} (gvkey,fyear) rows, "
          f"{n_cf} with a valid cfacshr; fyear {sa['fyear'].min()}..{sa['fyear'].max()}")

    # --- 2. 5-year change at the gvkey level: FY t-1 vs FY t-5 ---------------
    t1 = sa[["gvkey", "june_year", "split_adj"]].rename(columns={"split_adj": "sa_t1"})
    t5 = sa[["gvkey", "june_year", "split_adj"]].copy()
    t5["june_year"] = t5["june_year"] + 4               # FY t-5 -> june_year (t-5)+1 = t-4
    t5 = t5.rename(columns={"split_adj": "sa_t5"})
    iss = t1.merge(t5, on=["gvkey", "june_year"], how="left")
    iss["ISSUANCE_split_adj"] = np.where(iss["sa_t5"] > 0,
                                         iss["sa_t1"] / iss["sa_t5"] - 1.0, np.nan)
    iss = iss[["gvkey", "june_year", "ISSUANCE_split_adj"]]
    print(f"[sa] gvkey-level split-adj ISSUANCE: {len(iss)} rows, "
          f"{int(iss['ISSUANCE_split_adj'].notna().sum())} non-null")

    # --- 3. map (permno, june_year) -> gvkey via the foundation's June-t link -
    link = q((SQL_DIR / "crsp_comp_link.sql").read_text())
    link["linkdt"] = pd.to_datetime(link["linkdt"])
    link["linkenddt"] = pd.to_datetime(link["linkenddt"])

    form = pd.read_parquet(DATA / "formation.parquet")
    form = form[["permno", "june_year", "decile", "ISSUANCE"]].copy()
    form = form.rename(columns={"ISSUANCE": "ISSUANCE_raw"})
    form = form.drop_duplicates(["permno", "june_year"], keep="last")
    form["june_date"] = form["june_year"].map(lambda t: pd.Timestamp(f"{t}-06-30"))

    m = form.merge(link, on="permno", how="left")
    m = m[(m["june_date"] >= m["linkdt"]) & (m["june_date"] <= m["linkenddt"])]
    m = (m.sort_values("linkdt")
            .drop_duplicates(subset=["permno", "june_year"], keep="last"))
    m = m.merge(iss, on=["gvkey", "june_year"], how="left")

    out = m[["permno", "june_year", "decile", "ISSUANCE_split_adj",
             "ISSUANCE_raw"]].copy()
    out["decile"] = out["decile"].astype(int)
    out = out.sort_values(["june_year", "permno"]).reset_index(drop=True)
    print(f"[sa] mapped to formation keys: {len(out)} (permno,june_year) rows; "
          f"split-adj non-null {int(out['ISSUANCE_split_adj'].notna().sum())} "
          f"({out['ISSUANCE_split_adj'].notna().mean():.1%}); "
          f"raw non-null {int(out['ISSUANCE_raw'].notna().sum())}")
    return out


def ts_avg_cs_median(df: pd.DataFrame, col: str) -> pd.Series:
    cs = df.groupby(["june_year", "decile"])[col].median()
    return cs.groupby("decile").mean()


def issuance_cells(df: pd.DataFrame, col: str) -> dict:
    """Replicate table_1.py EXACTLY: TS-avg of yearly cross-sectional MEDIAN per
    decile; spread D10-D1; t = mean(yearly spread)/(std(ddof=1)/sqrt(N_years))."""
    yearly = df.pivot_table(index="june_year", columns="decile", values=col,
                            aggfunc="median")
    dec_med = yearly.mean(axis=0)                       # TS-avg per decile
    yearly_spread = yearly[N_DECILES] - yearly[1]
    n_years = len(yearly)
    spread = dec_med[N_DECILES] - dec_med[1]
    t = yearly_spread.mean() / (yearly_spread.std(ddof=1) / np.sqrt(n_years))
    return {"D1": float(dec_med[1]), "D10": float(dec_med[N_DECILES]),
            "spread": float(spread), "t": float(t), "n_years": int(n_years),
            "dec_medians": {int(d): float(dec_med[d]) for d in dec_med.index}}


def main() -> None:
    out = build_split_adjusted_issuance()
    out.to_parquet(DATA / "issuance_split_adjusted.parquet", index=False)
    print(f"\n[write] {DATA / 'issuance_split_adjusted.parquet'}  {out.shape}")

    raw = issuance_cells(out, "ISSUANCE_raw")
    adj = issuance_cells(out, "ISSUANCE_split_adj")
    paper = {"D1": 0.0803, "D10": 0.3012, "spread": 0.2209, "t": 8.36}

    print("\n" + "=" * 78)
    print("Table I ISSUANCE — split-adjusted vs raw vs paper")
    print("=" * 78)
    print(f"{'':<10}{'D1':>12}{'D10':>12}{'spread':>12}{'t(spread)':>12}")
    for name, d in [("paper", paper), ("raw", raw), ("split-adj", adj)]:
        print(f"{name:<10}{d['D1']:>12.4f}{d['D10']:>12.4f}"
              f"{d['spread']:>12.4f}{d['t']:>12.2f}")
    for label, d in [("raw", raw), ("split-adj", adj)]:
        ratios = {k: (d[k] / paper[k] if paper[k] else float("nan"))
                  for k in ["D1", "D10", "spread"]}
        print(f"  {label} / paper ratios: D1 {ratios['D1']:.2f}x  "
              f"D10 {ratios['D10']:.2f}x  spread {ratios['spread']:.2f}x")

    # full decile profile for the markdown note
    print("\nDecile medians (TS-avg yearly cross-sectional median):")
    print(f"{'decile':<8}" + "".join(f"{d:>9}" for d in range(1, 11)))
    print(f"{'raw':<8}" + "".join(
        f"{raw['dec_medians'].get(d, float('nan')):>9.4f}" for d in range(1, 11)))
    print(f"{'split':<8}" + "".join(
        f"{adj['dec_medians'].get(d, float('nan')):>9.4f}" for d in range(1, 11)))


if __name__ == "__main__":
    main()
