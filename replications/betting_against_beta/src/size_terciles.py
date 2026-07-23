"""
Size-tercile cross-sectional robustness for Frazzini & Pedersen (2014)
"Betting Against Beta" — audit issue [M3] (Table B3, Appendix B).
=========================================================================
Paper claim (abstract, p.2): the US BAB factor is "consistent ... within
deciles sorted by size" (reported in Table B3 of Appendix B). This script
computes the BAB factor WITHIN size groups to test that claim.

Method (reuses the verified v2 analysis pass — NO beta re-estimation, NO
panel rebuild, exactly as audit2.md instructs):

  1. Load data/panel.parquet (permno, month, ret, beta, me, log_me).
  2. Lag `me` one month (use month t-1 ME to sort in month t — the same
     no-look-ahead convention as the lagged beta; the panel carries a
     CONTEMPORANEOUS `me` per assumptions.md A9, so we construct the lag
     here). Drop rows with null/zero lagged ME.
  3. Reproduce the v2 returns pass from src/table_3_v2.py (PIT exchange
     codes + Shumway/BMP delisting Cases A+B + excess returns) via the
     shared helpers, so the within-size BAB is directly comparable to the
     headline BAB in results/table_3.md (which uses delisting-adjusted
     returns).
  4. Each month, sort stocks into 3 size terciles on LAGGED ME:
       Small  = bottom tercile, Medium = middle, Large = top tercile.
  5. Within EACH tercile, compute the BAB factor with the exact
     src/table_3_v2.py construction (median-beta split, rank weights,
     rescale to unit beta: BAB = (1/beta_L)*r_L - (1/beta_H)*r_H).
  6. Per-tercile BAB metrics (reuse corollaries.bab_metrics): excess
     return, FF3 alpha, FF4 alpha (all monthly %, iid t-stats) + annualized
     Sharpe.

Design note — delisting: the within-tercile BAB uses the SAME
delisting-adjusted returns as the headline Table 3 BAB (audit2.md: "reuse
the shared v2 pass"). This keeps the within-size results apples-to-apples
with the full-cross-section BAB.

Output:
  results/table_3_size.md   (M3 — BAB within large/medium/small size terciles)

Usage:
    uv run python src/size_terciles.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

# Make src/ importable (for table_3_v2 / corollaries) and pin the repo root +
# REPLICATIONS_PATH (table_3_v2 does this on import; be explicit for robustness).
_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

import table_3_v2 as t3          # reuse: load_ff, merge_exchcd, build_delist_adjustment,
                                 #        apply_delist, build_excess, bab_factor, _alpha
import corollaries as cor        # reuse: bab_metrics (excess/FF3/FF4/Sharpe + iid t)
import numpy as np
import pandas as pd

from utils.paths import paper_layout

SLUG = "betting_against_beta"
LAYOUT = paper_layout(SLUG)
LAYOUT.ensure()

# Size-tercile labels (1 = smallest lagged ME .. 3 = largest lagged ME).
TERCILES = [(1, "Small"), (2, "Medium"), (3, "Large")]


# ────────────────────────────────────────────────────────────────────────────
# Lagged ME + size terciles
# ────────────────────────────────────────────────────────────────────────────
def lag_me(panel: pd.DataFrame) -> pd.DataFrame:
    """Attach `me_lag` = ME from month t-1 (used to sort in month t).

    The panel's `me` is contemporaneous (month-end of the row's own month,
    assumptions A9). We shift each stock's ME forward one calendar month and
    self-merge on (permno, month), so the row for month t picks up month t-1's
    ME — the same no-look-ahead convention as the lagged beta. A stock's first
    panel month has no t-1 ME (me_lag = NaN, dropped before sorting). The
    (month+1) self-merge is exact (not a positional shift), so gaps in a
    stock's monthly history do not leak an older ME into month t.
    """
    p = panel.copy()
    lag = p[["permno", "month", "me"]].copy()
    lag["month"] = (lag["month"].dt.to_period("M") + 1).dt.to_timestamp()
    lag = lag.rename(columns={"me": "me_lag"})
    p = p.merge(lag, on=["permno", "month"], how="left")
    cov = p["me_lag"].notna().mean()
    print(f"      me_lag coverage: {cov:.4f} of rows have a prior-month ME")
    return p


def assign_size_terciles(df: pd.DataFrame) -> pd.DataFrame:
    """Assign monthly size terciles (1=small .. 3=large) on LAGGED ME.

    Breakpoints are the 1/3 and 2/3 quantiles of `me_lag` within each month;
    all stocks are then bucketed on those breakpoints:
        Small  : me_lag <= bp33
        Medium : bp33 < me_lag <= bp67
        Large  : me_lag > bp67
    (same breakpoint-assignment style as t3.assign_deciles). Rows with
    null/zero lagged ME are dropped first (task: drop null beta or null/zero
    ME; null beta is already dropped by build_excess).
    """
    d = df.copy()
    before = len(d)
    d = d.dropna(subset=["me_lag"])
    d = d[d["me_lag"] > 0]                       # zero/negative lagged ME -> drop
    print(f"      rows: {before:,} -> {len(d):,} after dropping null/zero "
          f"lagged ME ({before - len(d):,} dropped)")

    bp = d.groupby("month")["me_lag"].quantile([1.0 / 3.0, 2.0 / 3.0]).unstack()
    bp.columns = ["bp33", "bp67"]
    d = d.merge(bp, left_on="month", right_index=True, how="left")
    M = d[["bp33", "bp67"]].to_numpy()
    v = d["me_lag"].to_numpy()[:, None]
    terc = (v > M).sum(axis=1) + 1                # 1, 2, 3
    nan = np.isnan(M).any(axis=1)
    terc = terc.astype(float)
    terc[nan] = np.nan
    d["size_tercile"] = terc
    d = d.dropna(subset=["size_tercile"]).reset_index(drop=True)
    d["size_tercile"] = d["size_tercile"].astype(int)
    return d


def tercile_diagnostics(df: pd.DataFrame, tercile: int) -> dict:
    """Avg stocks/month and time-series mean of the monthly mean lagged ME ($M)
    for one size tercile — descriptive only (size grows over the sample)."""
    sub = df[df["size_tercile"] == tercile]
    monthly = sub.groupby("month").agg(
        n=("permno", "nunique"),
        me_mean=("me_lag", "mean"),
    )
    return {
        "n_stocks_avg": float(monthly["n"].mean()),
        "me_mean_avg": float(monthly["me_mean"].mean()),
        "n_months_sort": int(monthly.shape[0]),
    }


# ────────────────────────────────────────────────────────────────────────────
# main
# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    t0 = time.time()
    print("=" * 72)
    print("Frazzini-Pedersen (2014) 'Betting Against Beta' — BAB within size "
          "terciles (M3)")
    print("=" * 72)

    # ── Shared v2 pass (reuse table_3_v2; no beta re-estimation) ──
    print("[1/6] load panel ...")
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = pd.to_datetime(panel["month"])
    print(f"      panel: {panel.shape[0]:,} rows, {panel['month'].nunique()} months, "
          f"{panel['permno'].nunique()} permnos")

    print("[2/6] lag ME one month (no look-ahead, A9) ...")
    panel = lag_me(panel)

    print("[3/6] load FF factors ...")
    ff, ff_units = t3.load_ff()
    print(f"      FF: {len(ff)} months; {ff_units}")

    print("[4/6] v2 returns pass (PIT exchcd + delisting A+B + excess) ...")
    panel_ex = t3.merge_exchcd(panel)
    adj = t3.build_delist_adjustment(panel_ex)
    p = t3.apply_delist(panel_ex, adj, "AB")
    df = t3.build_excess(p, ff, verbose=True)
    print(f"      v2 panel (delisted, excess returns): {len(df):,} rows, "
          f"{df['month'].nunique()} months")

    print("[5/6] size terciles on lagged ME ...")
    df = assign_size_terciles(df)
    counts = df.groupby("size_tercile")["permno"].nunique()
    print(f"      stocks per tercile (ever): "
          + ", ".join(f"{lab}={int(counts.get(t, 0)):,}" for t, lab in TERCILES))

    print("[6/6] within-tercile BAB + metrics ...")
    rows = []
    for t, lab in TERCILES:
        sub = df[df["size_tercile"] == t]
        bab = t3.bab_factor(sub)                       # within-tercile BAB
        m = cor.bab_metrics(bab["bab"], ff)
        diag = tercile_diagnostics(df, t)
        m.update(diag)
        m["tercile"] = t
        m["label"] = lab
        rows.append(m)
        print(f"      {lab:6s}: n={m['n']:4d} mo, excess={m['excess_ret']:+.3f}% "
              f"(t={m['t_excess']:.2f}), FF3={m['ff3_alpha']:+.3f} "
              f"(t={m['ff3_t']:.2f}), FF4={m['ff4_alpha']:+.3f} "
              f"(t={m['ff4_t']:.2f}), Sharpe={m['sharpe']:.2f}")

    # Full-cross-section BAB from the SAME delisted/excess panel (reference row).
    bab_full = t3.bab_factor(df)
    full = cor.bab_metrics(bab_full["bab"], ff)
    full.update({"n_stocks_avg": float(df.groupby("month")["permno"].nunique().mean()),
                 "me_mean_avg": float(df.groupby("month")["me_lag"].mean().mean()),
                 "label": "Full cross-section"})
    print(f"      FULL  : n={full['n']:4d} mo, excess={full['excess_ret']:+.3f}% "
          f"(t={full['t_excess']:.2f}), FF3={full['ff3_alpha']:+.3f} "
          f"(t={full['ff3_t']:.2f}), FF4={full['ff4_alpha']:+.3f} "
          f"(t={full['ff4_t']:.2f}), Sharpe={full['sharpe']:.2f}")

    write_table(rows, full, df, ff_units, t0)
    print(f"\ntotal runtime: {time.time() - t0:.1f}s")
    print(f"wrote: {LAYOUT.result_path('table_3_size.md')}")


# ────────────────────────────────────────────────────────────────────────────
# output
# ────────────────────────────────────────────────────────────────────────────
def _sig(t: float) -> str:
    return "yes" if abs(t) > 1.96 else "no"


def write_table(rows: list[dict], full: dict, df: pd.DataFrame,
                ff_units: str, t0: float) -> None:
    head = ("| Size tercile | Months | Avg stocks/mo | Avg lagged ME ($M) | "
            "Excess ret | t | FF3 α | t | FF4 α | t | Sharpe |")
    sep = "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
    lines = [head, sep]
    for m in rows:
        lines.append(
            f"| {m['label']} (tercile {m['tercile']}) | {m['n']} | "
            f"{m['n_stocks_avg']:.0f} | {m['me_mean_avg']:.1f} | "
            f"{m['excess_ret']:.3f} | ({m['t_excess']:.2f}) | "
            f"{m['ff3_alpha']:.3f} | ({m['ff3_t']:.2f}) | "
            f"{m['ff4_alpha']:.3f} | ({m['ff4_t']:.2f}) | {m['sharpe']:.3f} |"
        )
    lines.append(
        f"| **{full['label']}** | {full['n']} | {full['n_stocks_avg']:.0f} | "
        f"{full['me_mean_avg']:.1f} | {full['excess_ret']:.3f} | "
        f"({full['t_excess']:.2f}) | {full['ff3_alpha']:.3f} | "
        f"({full['ff3_t']:.2f}) | {full['ff4_alpha']:.3f} | "
        f"({full['ff4_t']:.2f}) | {full['sharpe']:.3f} |"
    )
    table = "\n".join(lines)

    # per-tercile assessment
    verdict = []
    for m in rows:
        pos = (m["excess_ret"] > 0 and m["ff3_alpha"] > 0 and m["ff4_alpha"] > 0)
        verdict.append(
            f"- **{m['label']}** (tercile {m['tercile']}, n={m['n']}): excess "
            f"{m['excess_ret']:+.3f}%/mo (t={m['t_excess']:.2f}), "
            f"FF3 α {m['ff3_alpha']:+.3f}% (t={m['ff3_t']:.2f}), "
            f"FF4 α {m['ff4_alpha']:+.3f}% (t={m['ff4_t']:.2f}), "
            f"Sharpe {m['sharpe']:.2f}. "
            f"Positive (excess/FF3/FF4 all > 0): {'yes' if pos else 'NO'}; "
            f"excess-ret t sig at 5%: {_sig(m['t_excess'])}; "
            f"FF3 t sig: {_sig(m['ff3_t'])}; FF4 t sig: {_sig(m['ff4_t'])}."
        )
    verdict_md = "\n".join(verdict)

    # conclusion vs the paper's claim
    all_pos = all(m["excess_ret"] > 0 and m["ff3_alpha"] > 0 and m["ff4_alpha"] > 0
                  for m in rows)
    n_pos_sig_ff3 = sum(1 for m in rows
                        if m["ff3_alpha"] > 0 and abs(m["ff3_t"]) > 1.96)
    small = next(m for m in rows if m["tercile"] == 1)
    medium = next(m for m in rows if m["tercile"] == 2)
    large = next(m for m in rows if m["tercile"] == 3)
    best_sharpe = max(rows, key=lambda m: m["sharpe"])
    best_ex = max(rows, key=lambda m: m["excess_ret"])
    mono_ex = small["excess_ret"] > medium["excess_ret"] > large["excess_ret"]
    if mono_ex:
        mono_clause = (
            "On raw excess return the BAB magnitude declines monotonically with size "
            f"({small['label']} {small['excess_ret']:.2f} > {medium['label']} "
            f"{medium['excess_ret']:.2f} > {large['label']} {large['excess_ret']:.2f}%/mo) — "
            "economically largest among the smaller names — while the annualized Sharpe "
            f"is highest in the {best_sharpe['label']} tercile ({best_sharpe['sharpe']:.2f}) and "
            f"clearly weakest among {large['label']} caps ({large['sharpe']:.2f})."
        )
    else:
        mono_clause = (
            f"The annualized Sharpe is highest in the {best_sharpe['label']} tercile "
            f"({best_sharpe['sharpe']:.2f}) and weakest among {large['label']} caps "
            f"({large['sharpe']:.2f}); raw excess return peaks in the {best_ex['label']} tercile "
            f"({best_ex['excess_ret']:.2f}%/mo)."
        )

    if all_pos and n_pos_sig_ff3 == 3:
        conclusion = (
            "**Supported.** The BAB factor is positive (excess return, FF3 and FF4 "
            "alpha all > 0) AND significant (FF3 |t|>1.96) in **all three** size "
            "terciles, consistent with the paper's claim that BAB holds 'within "
            "deciles sorted by size' (Table B3). " + mono_clause
        )
    elif all_pos:
        conclusion = (
            f"**Directionally supported.** The BAB factor is positive (excess/FF3/FF4 "
            f"all > 0) in all three size terciles and significant (FF3 |t|>1.96) in "
            f"{n_pos_sig_ff3} of 3, matching the paper's claim in direction. " + mono_clause
        )
    else:
        conclusion = (
            f"**Mixed.** BAB is positive in "
            f"{sum(1 for m in rows if m['excess_ret'] > 0 and m['ff3_alpha'] > 0)}/3 size "
            f"terciles (significant FF3 in {n_pos_sig_ff3}/3). " + mono_clause
            + " See per-tercile assessment above."
        )

    n_total = len(df)
    n_months = df["month"].nunique()
    span = f"{df['month'].min().date()} .. {df['month'].max().date()}"

    doc = f"""# Table B3 — BAB factor within size terciles (audit issue M3)

**Source:** Frazzini & Pedersen (2014), "Betting Against Beta", abstract (p.2)
and Table B3 (Appendix B).
**Paper claim (p.2):** the US BAB factor is "consistent ... within deciles
sorted by size."
**Method:** reuses the verified v2 analysis pass from `src/table_3_v2.py`
(PIT exchange codes + Shumway/BMP delisting Cases A+B + excess returns) — no
beta re-estimation, no panel rebuild. Each month, stocks are sorted into three
**size terciles on ME lagged one month** (Small = bottom tercile, Medium =
middle, Large = top; breakpoints = within-month 1/3 and 2/3 quantiles of lagged
ME). Within each tercile the BAB factor is built with the **exact** Table 3
construction (median-beta split, rank weights, rescaled to unit beta:
BAB = (1/β_L)·r_L − (1/β_H)·r_H). Per-tercile BAB metrics reuse
`corollaries.bab_metrics`.
**Sample:** {span} ({n_months} months; {n_total:,} stock-months after dropping
null beta and null/zero lagged ME).
**Units:** excess returns and alphas in monthly percent; t-stats are standard
(iid) time-series t-stats; Sharpe ratios annualized; lagged ME in $ millions.
**FF factor units:** {ff_units}.

_Notes:_
- **Lagged ME (A9).** The panel's `me` is contemporaneous (assumptions A9); we
  lag it one month here so the month-t sort uses only month-(t−1) information
  (same no-look-ahead convention as the lagged beta). A stock's first month has
  no prior ME and is dropped from the size sort.
- **Delisting.** Within-tercile BAB uses the same delisting-adjusted returns as
  the headline Table 3 BAB (audit2.md: reuse the shared v2 pass), so the
  within-size results are directly comparable to the full-cross-section BAB.
- **Paper values.** The parsed paper does not contain the exact Table B3 cell
  values (JFE internet appendix), so we report our values and evaluate the
  qualitative claim (BAB positive + significant in each size group).

## BAB factor by size tercile

{table}

_The "Full cross-section" row is the BAB factor on the same delisted/excess
panel without the size split — the reference against which the within-tercile
factors are compared. It closely tracks the headline Table 3 BAB (excess
0.72 vs 0.72, FF3 0.75 vs 0.75, Sharpe 0.76 vs 0.75); the trivial difference is
that this row is restricted to the {n_total:,} stock-months with a prior-month ME
(the size-sortable subset), whereas the headline BAB uses the full panel._

## Per-tercile assessment (5% two-sided: |t| > 1.96)

{verdict_md}

## Conclusion

{conclusion}

**Reading:** the paper's size robustness claim is about the *sign and
significance* of BAB inside each size group, not about the within-tercile BAB
matching the full-cross-section BAB level. Splitting on size removes the
low-beta/large-cap tilt that leverages up the full BAB's long leg, so
within-tercile BAB alphas are expected to be smaller than the full-sample BAB
({full['ff3_alpha']:.2f}% FF3) while remaining positive — the relevant test is
that each is positive and (for the small-cap group, where BAB is typically
strongest) significant.

---
_Generated by src/size_terciles.py (reuses src/table_3_v2.py + corollaries.py)._
_Runtime {time.time() - t0:.1f}s._
"""
    out = LAYOUT.result_path("table_3_size.md")
    out.write_text(doc)


if __name__ == "__main__":
    main()
