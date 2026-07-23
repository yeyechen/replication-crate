"""
DIAGNOSTIC ONLY — Amihud (2002) replication. Does NOT touch canonical
artifacts (src/main.py, data/panel.parquet, ...).

Task B: DIVYLD split-adjustment hypothesis on the admitted sample
(characteristic years 1963-1996):
  B1 (current): divyld = 100 * sum(divamt) / |prc_end|
  B2          : divyld = 100 * sum(divamt * cfacpr_end / cfacpr_at) /
                |prc_end|, cfacpr_at from dsf at paydt (fallback exdt),
                nearest-prior-within-year carry-forward when no dsf row
                exists at the dist date.
Reports the six Table-1-style stats for both, fallback/coverage counts,
fraction of admitted stock-years with a within-year cfacpr change
(split events), and the mean adjustment factor.
Paper targets: meanMeans 4.14, meanSDs 5.48, median 4.16, meanSkew
5.385, min 2.43, max 6.68.

Task C: dividend coverage for admitted stocks 1990-1996 (payer
fraction, mean payments among payers; paper-era expectation ~65-75%
payers, ~4/yr among payers).

New cached variants: data/_cache/diag_divyld_splitadj.parquet,
data/_cache/diag_cfacpr_yearend.parquet,
data/_cache/diag_div_coverage.parquet.

Run: python replications/illiquidity_and_stock_returns/src/diag_divyld.py
"""
import numpy as np
import pandas as pd
from scipy import stats as sstats

import main  # noqa: E402  (reuses q_file/cached/LAYOUT; safe import)

PAPER = dict(meanMeans=4.14, meanSDs=5.48, median=4.16,
             meanSkew=5.385, minMean=2.43, maxMean=6.68)


def divyld_table1(df: pd.DataFrame, col: str) -> dict:
    """Paper Table 1 stats: over years, per-year mean/sd/skewness of the
    variable across admitted stocks; then aggregates over 34 years."""
    means, sds, skews = [], [], []
    for _, g in df.groupby("y"):
        x = g[col].dropna().to_numpy(dtype=float)
        if len(x) < 3:
            continue
        means.append(x.mean())
        sds.append(x.std(ddof=1))
        skews.append(float(sstats.skew(x, bias=False)))
    am = np.array(means)
    return dict(meanMeans=float(am.mean()), meanSDs=float(np.mean(sds)),
                median=float(np.median(am)), meanSkew=float(np.mean(skews)),
                minMean=float(am.min()), maxMean=float(am.max()),
                n_years=len(am))


def print_divyld_block(tag: str, st: dict) -> None:
    print(f"  {tag}: meanMeans={st['meanMeans']:.3f}  "
          f"meanSDs={st['meanSDs']:.3f}  median={st['median']:.3f}  "
          f"meanSkew={st['meanSkew']:.3f}  min={st['minMean']:.3f}  "
          f"max={st['maxMean']:.3f}  (n_years={st['n_years']})")


def main_diag() -> None:
    print("=" * 72)
    print("Setup: annual characteristics + admission (canonical machinery)")
    print("=" * 72)
    chars = main.cached("chars_annual.parquet", main.load_characteristics)
    chars, ailliq = main.apply_admission(chars)
    chars = main.derive_units(chars, ailliq)          # B1 divyld column
    n_adm = int(chars["admitted"].sum())
    print(f"chars rows: {len(chars)}; admitted stock-years: {n_adm} "
          f"(y {chars['y'].min()}..{chars['y'].max()})")

    # ---------------- B2 split-adjusted dividends ----------------
    print("\n" + "=" * 72)
    print("TASK B: DIVYLD split-adjustment (B1 current vs B2 cfacpr-aligned)")
    print("=" * 72)
    det = main.cached("diag_divyld_splitadj.parquet",
                      lambda: main.q_file("diag_divyld_splitadj.sql"))
    for c in ["divamt", "cfacpr_at", "cfacpr_end", "cf_ratio"]:
        det[c] = pd.to_numeric(det[c], errors="coerce")
    det["cf_exact"] = pd.to_numeric(det["cf_exact"], errors="coerce")
    print(f"distribution rows 1963-1996: {len(det)}")

    # -- cross-check B1: SQL div_sum vs cached canonical div_sum --
    b1_sql = det.groupby(["permno", "y"])["divamt"].sum()
    chk = chars.set_index(["permno", "y"])["div_sum"].sub(b1_sql).abs()
    print(f"[B1 cross-check] max |div_sum(canonical) - sum(divamt, B2 SQL)| "
          f"over shared (permno,y) = {chk.max():.3e} "
          f"({chk.notna().sum()} pairs; non-payer rows excluded)")

    # -- fallback / coverage counts --
    n_no_cf = int(det["cfacpr_at"].isna().sum())
    n_matched = int(det["cfacpr_at"].notna().sum())
    n_fallback = int(((det["cfacpr_at"].notna())
                      & (det["cf_exact"] == 0)).sum())
    print(f"cfacpr match: {n_matched}/{len(det)} rows matched "
          f"({100 * n_matched / len(det):.2f}%); "
          f"carry-forward fallback triggered on {n_fallback} rows "
          f"({100 * n_fallback / len(det):.3f}% of all; "
          f"{100 * n_fallback / n_matched:.3f}% of matched); "
          f"no cfacpr found (dividend dropped in B2): {n_no_cf} rows "
          f"({100 * n_no_cf / len(det):.4f}%)")
    if n_no_cf:
        sample = det.loc[det["cfacpr_at"].isna(),
                         ["permno", "y", "attr_dt"]].head(10)
        print("  [flag] rows with no cfacpr found at all (sample):")
        print(sample.to_string(index=False))
    rat = det["cf_ratio"].dropna()
    adj_rows = rat[(rat - 1).abs() > 1e-9]
    print(f"adjustment factor cf_ratio: n_valid={len(rat)}; "
          f"mean (all valid) = {rat.mean():.6f}; "
          f"rows with |ratio-1|>1e-9: {len(adj_rows)} "
          f"({100 * len(adj_rows) / len(rat):.2f}%); "
          f"mean among adjusted = {adj_rows.mean():.6f} "
          f"(min {adj_rows.min():.4f}, max {adj_rows.max():.4f})")

    # -- per (permno, y) aggregates --
    det["adj_div"] = det["divamt"] * det["cf_ratio"]
    agg = det.groupby(["permno", "y"]).agg(
        div_sum_b1=("divamt", "sum"),
        div_sum_b2=("adj_div", "sum"),
        n_dist=("divamt", "count"),
        n_no_cf=("cfacpr_at", lambda s: int(s.isna().sum())),
        n_adj=("cf_ratio", lambda s: int(((s - 1).abs() > 1e-9).sum())),
    ).reset_index()

    chars = chars.merge(agg[["permno", "y", "div_sum_b2"]],
                        on=["permno", "y"], how="left")
    chars["div_sum_b2"] = chars["div_sum_b2"].fillna(0.0)
    chars["divyld_b2"] = np.where(
        chars["price_end"] > 0,
        100.0 * chars["div_sum_b2"] / chars["price_end"], np.nan)

    adm = chars[chars["admitted"] == 1].copy()
    st1 = divyld_table1(adm, "divyld")
    st2 = divyld_table1(adm, "divyld_b2")
    print("\nTable 1 DIVYLD stats, admitted sample 1963-1996:")
    print_divyld_block("B1 (current)", st1)
    print_divyld_block("B2 (cfacpr) ", st2)
    print(f"  paper       : meanMeans={PAPER['meanMeans']:.3f}  "
          f"meanSDs={PAPER['meanSDs']:.3f}  median={PAPER['median']:.3f}  "
          f"meanSkew={PAPER['meanSkew']:.3f}  min={PAPER['minMean']:.3f}  "
          f"max={PAPER['maxMean']:.3f}")
    print(f"  B2 - B1 shift: meanMeans {st2['meanMeans'] - st1['meanMeans']:+.4f} "
          f"({100 * (st2['meanMeans'] / st1['meanMeans'] - 1):+.2f}%); "
          f"gap to paper 4.14: B1 {100 * (st1['meanMeans'] / 4.14 - 1):+.1f}%, "
          f"B2 {100 * (st2['meanMeans'] / 4.14 - 1):+.1f}%")

    # -- split-event fraction among admitted stock-years --
    yr_cf = main.cached("diag_cfacpr_yearend.parquet",
                        lambda: main.q_file("diag_cfacpr_yearend.sql"))
    for c in ["cf_start", "cf_end"]:
        yr_cf[c] = pd.to_numeric(yr_cf[c], errors="coerce")
    m = adm[["permno", "y"]].merge(yr_cf, on=["permno", "y"], how="left")
    no_cf_days = int(m["cf_start"].isna().sum())
    split = (m["cf_start"].notna()
             & ((m["cf_start"] - m["cf_end"]).abs() / m["cf_start"] > 1e-9))
    m["split"] = split
    fac = (m.loc[split, "cf_end"] / m.loc[split, "cf_start"])
    print(f"\nadmitted stock-years with a within-year cfacpr change "
          f"(split/stock-dividend event): {int(split.sum())}/{len(m)} "
          f"= {100 * split.mean():.2f}% "
          f"(no cfacpr days in universe table: {no_cf_days})")
    print(f"mean split-year adjustment cf_end/cf_start = {fac.mean():.4f} "
          f"(median {fac.median():.4f}, min {fac.min():.4f})")
    # by decade for color
    dec = m.assign(decade=(m["y"] // 10 * 10)).groupby("decade")["split"].mean()
    print("split fraction by decade: " +
          ", ".join(f"{int(d)}s {100 * v:.1f}%" for d, v in dec.items()))
    # dividend-row adjustment within admitted sample
    adm_det = det.merge(adm[["permno", "y"]], on=["permno", "y"], how="inner")
    r2v = adm_det["cf_ratio"].dropna()
    print(f"admitted dividend rows: {len(adm_det)}; "
          f"rows with |cf_ratio-1|>1e-9: {int(((r2v-1).abs() > 1e-9).sum())} "
          f"({100 * ((r2v - 1).abs() > 1e-9).mean():.2f}%); "
          f"mean cf_ratio (all valid) = {r2v.mean():.6f}, "
          f"divamt-weighted = "
          f"{(adm_det['adj_div'].sum() / adm_det['divamt'].sum()):.6f}")

    # ---------------- Task C: dividend coverage 1990-1996 ----------------
    print("\n" + "=" * 72)
    print("TASK C: dividend coverage, admitted stocks 1990-1996")
    print("=" * 72)
    cov = main.cached("diag_div_coverage.parquet",
                      lambda: main.q_file("diag_div_coverage.sql"))
    cov["n_div"] = pd.to_numeric(cov["n_div"], errors="coerce")
    adm_c = adm[adm["y"].between(1990, 1996)][["permno", "y"]]
    mc = adm_c.merge(cov, on=["permno", "y"], how="left")
    mc["n_div"] = mc["n_div"].fillna(0).astype(int)
    rows = []
    for y, g in mc.groupby("y"):
        payers = g["n_div"] > 0
        rows.append({"y": int(y), "n_stocks": len(g),
                     "payers": int(payers.sum()),
                     "frac_payers": payers.mean(),
                     "mean_count_payers":
                         g.loc[payers, "n_div"].mean() if payers.any() else np.nan})
    out = pd.DataFrame(rows)
    with pd.option_context("display.float_format", lambda v: f"{v:.3f}",
                           "display.width", 200):
        print(out.to_string(index=False))
    all_pay = mc["n_div"] > 0
    print(f"1990-1996 pooled: payer fraction = {all_pay.mean():.3f} "
          f"({int(all_pay.sum())}/{len(mc)}); "
          f"mean dividend count among payers = "
          f"{mc.loc[all_pay, 'n_div'].mean():.3f}")
    print(f"paper-era expectation: ~65-75% payers, ~4 payments/yr among "
          f"payers.")


if __name__ == "__main__":
    main_diag()
