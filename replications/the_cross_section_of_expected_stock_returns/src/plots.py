"""
Replication of Fama & French (1992) "The Cross-Section of Expected Stock Returns"
=================================================================================
Stage: Plots — five figures that illustrate the paper's central claims, built
from the cached data artifacts (NO ClickHouse re-query; analysis only).

Plots (all in results/, dpi 150, Agg backend):
  1. size_effect.png        bar chart, average monthly return of the 10 size
                            deciles (Table I "All" column / Table II Panel A
                            analog). The paper's size effect: returns decline
                            Small -> Large.
  2. beme_effect.png        bar chart, average monthly return of the 12 BE/ME
                            portfolios 1A..10B (Table IV Panel A analog). The
                            strong positive BE/ME -> return relation.
  3. size_beme_heatmap.png  10x10 heatmap of the Table V average-return matrix
                            (rows Small-ME -> Large-ME, cols Low -> High BE/ME),
                            min/max annotated. The two-dimensional structure:
                            within-decile BE/ME gradient + size gradient.
  4. cumulative_portfolios.png  cumulative compounded returns, July 1963 -
                            December 1990, for four EW series: Small-ME (size_1),
                            Large-ME (size_10), High BE/ME (group 10) and Low
                            BE/ME (group 1). Economic magnitude over time.
                            Uses the utils.plot.plot_cumulative_returns primitive.
  5. fm_slopes_rolling.png  rolling 60-month average Fama-MacBeth slopes for
                            beta (R1), ln(ME) (R2) and ln(BE/ME) (R4), with a
                            zero line and the December-1976 subperiod boundary
                            shaded (Table III / Table VI stability analog).

Inputs (built by earlier iterations):
  data/panel.parquet                  firm-month panel
  data/agg_portfolio_returns.parquet  size_1..size_10 / beta_1..10 / grand EW
                                      monthly series (330 obs each)

Usage:
    uv run python replications/the_cross_section_of_expected_stock_returns/src/plots.py
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# --- path bootstrap: runnable from any CWD -------------------------------
SRC_DIR = Path(__file__).resolve().parent
REPO_ROOT = SRC_DIR.parents[2]
os.environ.setdefault("REPLICATIONS_PATH", str(REPO_ROOT / "replications"))
for _p in (str(SRC_DIR), str(REPO_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import matplotlib
matplotlib.use("Agg")                      # headless: first matplotlib import
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from main import LAYOUT  # noqa: E402  (resolved paper layout)
# reuse the table computation functions (single source of truth) rather than
# re-implementing the aggregations
import table_4 as t4   # noqa: E402  (BE/ME one-dimensional portfolio returns)
import table_5 as t5   # noqa: E402  (size x BE/ME 10x10 matrix)
import table_3_6 as t36  # noqa: E402  (Fama-MacBeth monthly OLS helpers)
from utils.plot import plot_cumulative_returns  # noqa: E402

DPI = 150
SUBPERIOD_BOUNDARY_YM = 197612            # Dec 1976 | Jan 1977 split (Table VI)


def _out(name: str) -> Path:
    return LAYOUT.result_path(name)


# ────────────────────────────────────────────────────────────────────────────
# 1. Size effect — average monthly return of the 10 size deciles
# ────────────────────────────────────────────────────────────────────────────
def plot_size_effect(agg: pd.DataFrame) -> None:
    means = [agg.loc[agg["series"] == f"size_{d}", "ret"].mean() * 100.0
             for d in range(1, 11)]
    x = np.arange(10)
    labels = ["Small"] + [str(d) for d in range(2, 10)] + ["Large"]
    fig, ax = plt.subplots(figsize=(11, 5.5))
    bars = ax.bar(x, means, color="#1e88e5", edgecolor="black", linewidth=0.5)
    for xi, v in zip(x, means):
        ax.text(xi, v + 0.015, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Size decile  (Small = decile 1  →  Large = decile 10)")
    ax.set_ylabel("Average monthly return (% per month)")
    ax.set_title("Fama & French (1992), Table I 'All' column / Table II Panel A analog\n"
                 "Average equal-weighted monthly return by size decile, "
                 "July 1963 – December 1990")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    out = _out("size_effect.png")
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}  (Small {means[0]:.2f} → Large {means[-1]:.2f} %/mo)")


# ────────────────────────────────────────────────────────────────────────────
# 2. BE/ME effect — average monthly return of the 12 BE/ME portfolios
# ────────────────────────────────────────────────────────────────────────────
def plot_beme_effect(panel: pd.DataFrame) -> None:
    # reuse the exact Table IV Panel A aggregation (time-series mean of the
    # monthly stock-level EW return x 100)
    vals = t4.compute_panel(panel, t4.PANEL_COL["A"], t4.COLS_A)["Return"]
    cols = t4.COLS_A
    means = [vals[c] for c in cols]
    x = np.arange(len(cols))
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.bar(x, means, color="#43a047", edgecolor="black", linewidth=0.5)
    for xi, v in zip(x, means):
        ax.text(xi, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(cols)
    ax.set_xlabel("BE/ME portfolio  (1A = lowest BE/ME  →  10B = highest BE/ME)")
    ax.set_ylabel("Average monthly return (% per month)")
    ax.set_title("Fama & French (1992), Table IV Panel A analog\n"
                 "Average equal-weighted monthly return by BE/ME portfolio, "
                 "July 1963 – December 1990")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    out = _out("beme_effect.png")
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}  (1A {means[0]:.2f} → 10B {means[-1]:.2f} %/mo)")


# ────────────────────────────────────────────────────────────────────────────
# 3. Size x BE/ME heatmap — the Table V 10x10 average-return matrix
# ────────────────────────────────────────────────────────────────────────────
def plot_size_beme_heatmap(panel: pd.DataFrame, agg: pd.DataFrame) -> None:
    matrix = t5.compute_matrix(panel, agg)
    row_labels = t5.ROW_LABELS[1:]          # Small-ME, ME-2, ..., Large-ME
    col_labels = t5.COL_LABELS[1:]          # Low, 2, ..., High
    M = np.array([[matrix[(r, c)] for c in col_labels] for r in row_labels])

    imin, jmin = np.unravel_index(np.argmin(M), M.shape)
    imax, jmax = np.unravel_index(np.argmax(M), M.shape)

    fig, ax = plt.subplots(figsize=(9.5, 7.5))
    im = ax.imshow(M, cmap="YlGn", aspect="auto")
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)
    ax.set_xlabel("BE/ME group  (Low = group 1  →  High = group 10)")
    ax.set_ylabel("Size decile  (Small-ME = decile 1  →  Large-ME = decile 10)")
    ax.set_title("Fama & French (1992), Table V analog\n"
                 "Average equal-weighted monthly return (%), "
                 "size × BE/ME portfolios, July 1963 – December 1990")
    # annotate every cell; min (red) / max (blue) highlighted
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            is_min = (i == imin and j == jmin)
            is_max = (i == imax and j == jmax)
            color = "red" if is_min else ("blue" if is_max else "black")
            weight = "bold" if (is_min or is_max) else "normal"
            ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                    fontsize=8, color=color, fontweight=weight)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Average monthly return (% per month)")
    ax.set_xlabel(ax.get_xlabel() +
                  f"\nMIN {M[imin, jmin]:.2f} at "
                  f"{row_labels[imin]}×{col_labels[jmin]} (red);  "
                  f"MAX {M[imax, jmax]:.2f} at "
                  f"{row_labels[imax]}×{col_labels[jmax]} (blue)")
    fig.tight_layout()
    out = _out("size_beme_heatmap.png")
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}  (min {M[imin, jmin]:.2f} @ {row_labels[imin]}×"
          f"{col_labels[jmin]}; max {M[imax, jmax]:.2f} @ "
          f"{row_labels[imax]}×{col_labels[jmax]})")


# ────────────────────────────────────────────────────────────────────────────
# 4. Cumulative compounded returns of four EW portfolios
# ────────────────────────────────────────────────────────────────────────────
def plot_cumulative_portfolios(panel: pd.DataFrame, agg: pd.DataFrame) -> None:
    months = (agg.loc[agg["series"] == "size_1", ["month", "ym"]]
              .sort_values("ym").reset_index(drop=True))
    size1 = agg.loc[agg["series"] == "size_1"].sort_values("ym")["ret"].to_numpy()
    size10 = agg.loc[agg["series"] == "size_10"].sort_values("ym")["ret"].to_numpy()

    # pooled BE/ME group-10 (High) and group-1 (Low) EW monthly returns:
    # stock-level mean ret across all size deciles within the BE/ME group
    sb = panel["size_beme"].str.split("_", expand=True)
    work = pd.DataFrame({"month": panel["month"], "ret": panel["ret"],
                         "bg": sb[1].astype(int)})
    hi = (work[work["bg"] == 10].groupby("month")["ret"].mean()
          .rename("hi").reset_index())
    lo = (work[work["bg"] == 1].groupby("month")["ret"].mean()
          .rename("lo").reset_index())
    df = months.merge(hi, on="month", how="left").merge(lo, on="month", how="left")
    df = df.rename(columns={"hi": "High BE/ME (group 10)",
                            "lo": "Low BE/ME (group 1)"})
    df["Small-ME (size_1)"] = size1
    df["Large-ME (size_10)"] = size10
    cols = ["Small-ME (size_1)", "Large-ME (size_10)",
            "High BE/ME (group 10)", "Low BE/ME (group 1)"]
    df = df[["month"] + cols].sort_values("month").reset_index(drop=True)

    plot_cumulative_returns(
        df, index_col_name="month", ret_col_lst=cols,
        title=("Fama & French (1992), Tables I/IV/V analog — cumulative "
               "compounded EW returns\nSmall vs Large size and High vs Low "
               "BE/ME, July 1963 – December 1990"),
        save_to=_out("cumulative_portfolios.png"),
    )
    # console facts: total compounded growth of each series
    for c in cols:
        growth = float((1 + df[c]).prod())
        print(f"  {c}: cumulative x{growth:.1f} over 330 months")
    print(f"wrote {_out('cumulative_portfolios.png')}")


# ────────────────────────────────────────────────────────────────────────────
# 5. Rolling 60-month average Fama-MacBeth slopes (beta, ln(ME), ln(BE/ME))
# ────────────────────────────────────────────────────────────────────────────
def plot_fm_slopes_rolling(pw: pd.DataFrame) -> None:
    # monthly cross-sectional OLS (reuse the Table III/VI helper exactly)
    coefs_beta = t36.fm_monthly(pw, ["post_beta"])      # R1: beta alone
    coefs_me = t36.fm_monthly(pw, ["lnME"])             # R2: ln(ME) alone
    coefs_bm = t36.fm_monthly(pw, ["ln_bm"])            # R4: ln(BE/ME) alone

    def monthly_ym_series(coefs: pd.DataFrame, col: str) -> pd.Series:
        s = coefs[col] * 100.0                          # %/month per unit
        idx = pd.to_datetime(s.index.astype(str), format="%Y%m")
        return pd.Series(s.to_numpy(), index=idx).sort_index()

    beta = monthly_ym_series(coefs_beta, "post_beta")
    lnme = monthly_ym_series(coefs_me, "lnME")
    lnbm = monthly_ym_series(coefs_bm, "ln_bm")

    W = 60
    beta_r = beta.rolling(W).mean()
    lnme_r = lnme.rolling(W).mean()
    lnbm_r = lnbm.rolling(W).mean()

    boundary = pd.Timestamp("1976-12-31")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(lnbm_r.index, lnbm_r, color="#43a047", linewidth=2,
            label="ln(BE/ME) slope  (R4)")
    ax.plot(lnme_r.index, lnme_r, color="#1e88e5", linewidth=2,
            label="ln(ME) slope  (R2)")
    ax.plot(beta_r.index, beta_r, color="#f31d36", linewidth=2,
            label="β slope  (R1)")
    ax.axhline(0.0, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
    # shade the two subperiods split at December 1976 (Table VI)
    ax.axvspan(beta_r.index.min(), boundary, color="grey", alpha=0.10)
    ax.axvspan(boundary, beta_r.index.max(), color="khaki", alpha=0.12)
    ax.axvline(boundary, color="grey", linewidth=1.0, linestyle=":")
    ax.annotate("subperiod split\n(Dec 1976)", xy=(boundary, 0),
                xytext=(boundary, ax.get_ylim()[1] * 0.85),
                fontsize=8, ha="center", color="grey")
    ax.set_xlabel("Month")
    ax.set_ylabel(f"Rolling {W}-month average FM slope (% per month per unit)")
    ax.set_title("Fama & French (1992), Table III / Table VI analog\n"
                 f"Rolling {W}-month average Fama-MacBeth slopes: β (R1), "
                 "ln(ME) (R2), ln(BE/ME) (R4)")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = _out("fm_slopes_rolling.png")
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}")
    print(f"  full-sample mean slopes: β {beta.mean():.3f}, "
          f"ln(ME) {lnme.mean():.3f}, ln(BE/ME) {lnbm.mean():.3f}")


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    t0 = time.time()
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    agg = pd.read_parquet(LAYOUT.data_path("agg_portfolio_returns.parquet"))

    plot_size_effect(agg)
    plot_beme_effect(panel)
    plot_size_beme_heatmap(panel, agg)
    plot_cumulative_portfolios(panel, agg)

    # rolling FM slopes need the pre-winsorized panel (Table III/IV convention)
    panel["ym"] = panel["month"].dt.year * 100 + panel["month"].dt.month
    pw = t36.prewinsorize(panel)
    plot_fm_slopes_rolling(pw)

    print(f"\ntotal time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
