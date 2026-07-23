"""
Shared portfolio-sort machinery for LSV (1994) Tables I, II, III.

All return statistics are computed from data/panel.parquet (built by main.py).
Definitions (from the task spec + assumptions.md):
  * R_k(fy, g)  = equal-weighted mean of stock_ret_k over group members with
                  alive_k == 1 and stock_ret_k not null  (annual buy-and-hold).
  * AR(fy, g)   = mean of R_1..R_5.
  * CR_5(fy, g) = prod_{k=1..5}(1 + R_k) - 1.
  * SAAR(fy, g) = (1/5) * sum_k [ R_k(fy,g) - B_k(fy,g) ], where
                  B_k = mean of sizedec_ret_k over the SAME members (A5/A6).
  * Table cell  = mean of the per-formation quantity across the 22 formations.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

N_HOLD = 5


def returns_long(panel: pd.DataFrame) -> pd.DataFrame:
    """Reshape the 5 holding-year return blocks into long form."""
    frames = []
    for k in range(1, N_HOLD + 1):
        sub = panel[["fy", "permno", f"stock_ret_{k}",
                     f"sizedec_ret_{k}", f"alive_{k}"]].copy()
        sub.columns = ["fy", "permno", "stock_ret", "sizedec_ret", "alive"]
        sub["k"] = k
        frames.append(sub)
    return pd.concat(frames, ignore_index=True)


def assign_deciles(values: pd.Series, n: int = 10) -> pd.Series:
    """Equal-count deciles 1..n, ascending; ties broken deterministically.

    `values` is the signal over the valid subset (already filtered to non-null).
    Returns decile labels aligned to `values.index`. Guarantees n non-empty bins
    when len(values) >= n.
    """
    m = len(values)
    r = values.rank(method="first", ascending=True)          # 1..m
    pct = (r - 1) / m
    d = np.minimum(n, np.floor(pct * n).astype(int) + 1)
    return pd.Series(d, index=values.index, dtype="Int64")


def assign_304030(values: pd.Series) -> pd.Series:
    """30/40/30 groups (1=bottom 30%, 2=middle 40%, 3=top 30%), ascending."""
    q30 = values.quantile(0.30)
    q70 = values.quantile(0.70)
    g = np.where(values <= q30, 1, np.where(values <= q70, 2, 3))
    return pd.Series(g, index=values.index, dtype="Int64")


def group_stats(L: pd.DataFrame, grp: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Per (fy, grp) stats and per (fy, grp) member counts.

    L   : long returns (fy, permno, stock_ret, sizedec_ret, alive, k)
    grp : (fy, permno, grp) group assignment
    Returns (table_fy, counts_fy):
      table_fy  indexed (fy, grp) with R_1..R_5, AR, CR_5, SAAR
      counts_fy indexed (fy, grp) with n_members (assigned at formation)
    """
    m = L.merge(grp, on=["fy", "permno"], how="inner")
    valid = m[(m["alive"] == 1) & (m["stock_ret"].notna())]
    g = valid.groupby(["fy", "grp", "k"])
    R = g["stock_ret"].mean()
    B = g["sizedec_ret"].mean()          # pandas mean skips NaN
    df = pd.concat({"R": R, "B": B}, axis=1).reset_index()
    Rp = df.pivot(index=["fy", "grp"], columns="k", values="R")
    Bp = df.pivot(index=["fy", "grp"], columns="k", values="B")
    Rp = Rp.reindex(columns=list(range(1, N_HOLD + 1)))
    Bp = Bp.reindex(columns=list(range(1, N_HOLD + 1)))

    out = pd.DataFrame(index=Rp.index)
    for k in range(1, N_HOLD + 1):
        out[f"R_{k}"] = Rp[k]
    out["AR"] = Rp.mean(axis=1)                                   # skipna
    out["CR_5"] = (1 + Rp).prod(axis=1, skipna=False) - 1         # strict
    out["SAAR"] = (Rp.values - Bp.values).mean(axis=1)            # (1/5)Σ(R-B)

    counts_fy = grp.groupby(["fy", "grp"]).size().rename("n_members")
    return out, counts_fy


def table_values(table_fy: pd.DataFrame) -> pd.DataFrame:
    """Average the per-formation stats across formations -> one row per group."""
    return table_fy.groupby("grp").mean()
