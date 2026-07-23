"""Three figures illustrating the claims of George & Hwang (2004),
"The 52-Week High and Momentum Investing".

Figure 1 — results/cumulative_wl.png
    Cumulative value of $1 invested in each (6,6) EW W-L spread series
    (JT / MG / WH), 1963-07 .. 2001-12, log scale, 2001 momentum crash
    annotated. Source: data/strategy_returns.parquet.

Figure 2 — results/january_effect.png
    Winner / Loser / W-L mean monthly returns for the 3 strategies,
    Panel A = ex-January, Panel B = January only. Source:
    data/strategy_returns.parquet split on month-of-year.

Figure 3 — results/table5_spreads.png
    Table V (6,6) Fama-MacBeth dummy spreads: OURS vs PAPER across the
    four columns (raw/RA x Jan-incl/Jan-excl). Sources:
    data/fm_coefficients.parquet (raw series -> mean), results/table_5.md
    (RA intercepts), preparations/tables_to_replicate.json (paper values).

Run from the repo root:
    python replications/the_52_week_high_and_momentum_investing/src/plots.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: must precede pyplot import

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Repo-root bootstrap so the script runs from any cwd.
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from utils.paths import paper_layout  # noqa: E402
from utils.plot_config import plot_config  # noqa: E402

LAYOUT = paper_layout("the_52_week_high_and_momentum_investing")


def intermediate_path(name: str):
    """Relocated derived caches (audit1.md [M6]): the 8 non-allowlisted
    fm_coefficients*/strategy_returns parquets live under results/intermediate/
    (results/ is validator-clean) instead of data/ (closed parquet allowlist).
    (Local copy — plots.py does not import the tables_5 hub.)"""
    d = LAYOUT.result_path("intermediate")
    d.mkdir(parents=True, exist_ok=True)
    return d / name


# Visual conventions (consistent with utils/plot.py primitives).
BLUE = plot_config.blue_hex    # #1e88e5
RED = plot_config.red_hex      # #f31d36
GREEN = "#43a047"
GREY = "#9e9e9e"
DPI = 150

STRATS = [("jt", "JT (Jegadeesh-Titman 12-2)"),
          ("mg", "MG (Moskowitz-Grinblatt)"),
          ("wh", "WH (52-week high)")]


# --------------------------------------------------------------------------
# Figure 1: cumulative value of $1 in each W-L spread
# --------------------------------------------------------------------------
def figure1_cumulative_wl(sr: pd.DataFrame, out: Path) -> dict:
    """Compound (1 + wl/100) monthly for jt_wl, mg_wl, wh_wl; log y-scale.

    Plain matplotlib (not utils.plot.plot_cumulative_returns): the
    primitive plots (1+r).cumprod()-1 on a linear axis starting at 0,
    which rules out the requested log scale (cum-1 starts at 0) and
    the crash annotation (the primitive closes the figure internally).
    """
    fig, ax = plt.subplots(figsize=(11, 6))
    colors = {"jt": RED, "mg": GREEN, "wh": BLUE}
    end_vals = {}
    for key, long in STRATS:
        cum = (1 + sr[f"{key}_wl"] / 100.0).cumprod()
        end_vals[key] = float(cum.iloc[-1])
        ax.plot(sr["month"], cum, color=colors[key], linewidth=2,
                label=f"{long} — $1 → ${end_vals[key]:.2f}")

    # 2001 momentum crash: Oct-Dec 2001 (final 3 months of the sample).
    crash = sr[sr["month"] >= "2001-10-01"]
    wh_crash = (1 + crash["wh_wl"] / 100.0).prod() - 1
    ax.axvspan(pd.Timestamp("2001-10-01"), pd.Timestamp("2001-12-31"),
               color=GREY, alpha=0.15, zorder=0)
    ax.annotate(
        f"2001 momentum crash\nOct–Dec 2001: WH spread\ncumulates {wh_crash:+.0%}\n(sample ends Dec 2001)",
        xy=(pd.Timestamp("2001-11-15"), 3.9),
        xytext=(pd.Timestamp("1996-01-01"), 9.5),
        fontsize=9, ha="left", va="center",
        arrowprops=dict(arrowstyle="->", color="0.3", lw=1.2),
    )

    ax.set_yscale("log")
    ax.set_yticks([1, 2, 5, 10])
    ax.set_yticklabels(["$1", "$2", "$5", "$10"])
    ax.set_ylim(0.75, 16)
    ax.set_xlabel("Month")
    ax.set_ylabel("Value of $1 invested (log scale)")
    ax.set_title("George & Hwang (2004), Table I strategies — "
                 "W-L spreads, EW (6,6)\nCumulative value of $1, "
                 "July 1963 – December 2001 (462 months)")
    ax.legend(loc="upper left", frameon=True, fontsize=10)
    ax.grid(True, which="both", alpha=0.3, linewidth=0.5)
    fig.tight_layout()
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return end_vals


# --------------------------------------------------------------------------
# Figure 2: January effect — Winner / Loser / W-L ex-Jan vs January
# --------------------------------------------------------------------------
def figure2_january_effect(sr: pd.DataFrame, out: Path) -> pd.DataFrame:
    """Grouped bars: 3 strategies x {Winner, Loser, W-L} in two panels.

    Plain matplotlib: utils.plot.plot_decile_spread plots one bar set per
    EW/VW column against quantile bins — the wrong shape here (we need
    strategy groups x Winner/Loser/W-L bars in ex-January vs January
    panels with value labels).
    """
    is_jan = sr["month"].dt.month == 1
    n_jan, n_ex = int(is_jan.sum()), int((~is_jan).sum())

    rows = []
    for key, _long in STRATS:
        for label, sub in [("ex_jan", sr[~is_jan]), ("jan", sr[is_jan])]:
            rows.append({
                "strategy": key.upper(), "panel": label,
                "Winner": sub[f"{key}_w"].mean(),
                "Loser": sub[f"{key}_l"].mean(),
                "W-L": sub[f"{key}_wl"].mean(),
            })
    stats = pd.DataFrame(rows)

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 5.5), sharey=True)
    bar_cols = [("Winner", BLUE), ("Loser", RED), ("W-L", GREY)]
    x = np.arange(len(STRATS))
    width = 0.26

    for ax, panel, title in [
        (ax_a, "ex_jan", f"Panel A: Ex-January ({n_ex} months)"),
        (ax_b, "jan", f"Panel B: January only ({n_jan} months)"),
    ]:
        sub = stats[stats["panel"] == panel].set_index("strategy")
        for i, (col, color) in enumerate(bar_cols):
            vals = sub.loc[[s.upper() for s, _ in STRATS], col]
            bars = ax.bar(x + (i - 1) * width, vals, width,
                          label=col, color=color, alpha=0.85,
                          edgecolor="white", linewidth=0.4)
            ax.bar_label(bars, fmt="%.1f", fontsize=8,
                         padding=2, label_type="edge")
        ax.axhline(0, color="0.4", linewidth=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels([s for s, _ in STRATS])
        ax.set_title(title, fontsize=12)
        ax.grid(True, axis="y", alpha=0.3, linewidth=0.5)

    ax_a.set_ylabel("Mean monthly return (%)")
    ax_a.legend(loc="upper left", frameon=True, fontsize=9, ncol=3)
    fig.suptitle("Momentum profits live outside January; losers rebound in January\n"
                 "George & Hwang (2004), Table I strategies — EW (6,6), "
                 "winner / loser / W-L portfolio means",
                 fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return stats


# --------------------------------------------------------------------------
# Figure 3: Table V (6,6) spreads — ours vs the paper
# --------------------------------------------------------------------------
COLUMNS = ["raw_janincl", "raw_janexcl", "ra_janincl", "ra_janexcl"]
COLUMN_LABELS = {"raw_janincl": "Raw\nJan incl", "raw_janexcl": "Raw\nJan excl",
                 "ra_janincl": "Risk-adj\nJan incl", "ra_janexcl": "Risk-adj\nJan excl"}


def _parse_table5_md(path: Path) -> dict:
    """Parse '### Column: <col>' sections of results/table_5.md into
    {col: {row: (paper, ours)}}."""
    out: dict = {}
    cur = None
    for line in path.read_text().splitlines():
        m = re.match(r"### Column: (\S+)", line)
        if m:
            cur = m.group(1)
            out[cur] = {}
            continue
        if cur and line.startswith("|") and "row" not in line.split("|")[1]:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4:
                try:
                    paper, ours = float(cells[1]), float(cells[2])
                except ValueError:
                    continue
                out[cur][cells[0]] = (paper, ours)
    return out


def _paper_spreads(path: Path) -> dict:
    """Paper values from tables_to_replicate.json: {(column, strat): value}
    for the T5 s66_*_*_spread metrics (percent per month)."""
    tables = json.loads(path.read_text())["tables"]
    t5 = next(t for t in tables if t.get("id") == "T5")
    out = {}
    for m in t5["metrics"]:
        name = m["name"]
        if not name.startswith("s66_") or not name.endswith("_spread"):
            continue  # skip s612_* and *_tstat entries
        body = name[len("s66_"):-len("_spread")]
        for col in COLUMNS:
            if body.startswith(col + "_"):
                strat = body[len(col) + 1:]
                out[(col, strat)] = float(m["value"])
    return out


def figure3_table5_spreads(fm: pd.DataFrame, out: Path) -> pd.DataFrame:
    """Grouped bars: 4 Table V columns x 3 strategies, OURS vs PAPER.

    Plain matplotlib: no primitive covers an ours-vs-paper grouped bar
    chart (plot_decile_spread is EW/VW per quantile bin; the others are
    line plots).
    """
    paper = _paper_spreads(LAYOUT.preparations_path("tables_to_replicate.json"))
    md = _parse_table5_md(LAYOUT.result_path("table_5.md"))

    # OURS: raw columns straight from the c_{k,t} spread series means;
    # RA columns from table_5.md (FF3 regression intercepts, computed in
    # tables_5.py against ClickHouse FF factors — not re-run here).
    is_jan = fm["month"].dt.month == 1
    ours = {}
    for strat in ["wh", "jt", "mg"]:
        series = fm[f"s66_{strat}_spread"]
        ours[("raw_janincl", strat)] = series.mean()
        ours[("raw_janexcl", strat)] = series[~is_jan].mean()
        for col in ["ra_janincl", "ra_janexcl"]:
            ours[(col, strat)] = md[f"s66_{col}"][f"{strat}_spread"][1]

    # Cross-check the raw means against table_5.md's reported ours values.
    for col in ["raw_janincl", "raw_janexcl"]:
        for strat in ["wh", "jt", "mg"]:
            md_ours = md[f"s66_{col}"][f"{strat}_spread"][1]
            assert abs(ours[(col, strat)] - md_ours) < 5e-4, (
                f"parquet/md mismatch {col}/{strat}: "
                f"{ours[(col, strat)]:.4f} vs {md_ours:.4f}")

    comp = pd.DataFrame([
        {"column": col, "strategy": strat,
         "ours": ours[(col, strat)], "paper": paper[(col, strat)]}
        for col in COLUMNS for strat in ["wh", "jt", "mg"]
    ])

    # Four side-by-side subplots (one per Table V column) — each holds the
    # 3 strategy pairs {WH, JT, MG} x 2 bars (Ours / Paper). This avoids the
    # two-level x-label collision a single crowded axis produced (the column
    # tick falls on the middle strategy and hides it) while mapping exactly
    # onto the spec's "the four (6,6) columns".
    strats = ["wh", "jt", "mg"]
    strat_lbl = ["WH", "JT", "MG"]
    x = np.arange(len(strats))
    width = 0.36
    fig, axes = plt.subplots(1, 4, figsize=(14, 6.2), sharey=True,
                             gridspec_kw={"wspace": 0.08})

    for ax, col in zip(axes, COLUMNS):
        for pi, strat in enumerate(strats):
            o = comp[(comp["column"] == col) &
                     (comp["strategy"] == strat)].iloc[0]
            b1 = ax.bar(x[pi] - width / 2, o["ours"], width, color=BLUE,
                        alpha=0.9, edgecolor="white", linewidth=0.4,
                        label="Ours" if (ax is axes[0] and pi == 0) else None)
            b2 = ax.bar(x[pi] + width / 2, o["paper"], width, color=GREY,
                        alpha=0.55, hatch="//", edgecolor="0.35", linewidth=0.4,
                        label="Paper" if (ax is axes[0] and pi == 0) else None)
            ax.bar_label(b1, fmt="%.2f", fontsize=8, rotation=90, padding=2)
            ax.bar_label(b2, fmt="%.2f", fontsize=8, rotation=90, padding=2)
        ax.set_xticks(x)
        ax.set_xticklabels(strat_lbl, fontsize=10)
        ax.set_ylim(0, 1.45)
        ax.set_title(COLUMN_LABELS[col].replace("\n", " "), fontsize=11)
        ax.grid(True, axis="y", alpha=0.3, linewidth=0.5)

    axes[0].set_ylabel("Winner − Loser spread (%/month)")
    axes[0].legend(loc="upper left", frameon=True, fontsize=9)

    # Dynamic note on whether OURS reproduces the paper's WH>JT>MG ordering.
    reproduced = []
    flip = ""
    for col in COLUMNS:
        cc = comp[comp["column"] == col].set_index("strategy")["ours"]
        w, j, m = float(cc["wh"]), float(cc["jt"]), float(cc["mg"])
        ok = (w > j) and (j > m)
        reproduced.append(ok)
        if not ok and col == "raw_janincl":
            flip = f"raw Jan-incl: JT {j:.2f} > WH {w:.2f}"
    n_ok = sum(reproduced)
    note = (f"Both bars labeled (%/month). Paper ordering WH > JT > MG holds in "
            f"all 4 columns; ours reproduces it in {n_ok} of 4"
            + (f" ({flip})" if n_ok < 4 else "") + ".")
    fig.suptitle("George & Hwang (2004), Table V — Fama-MacBeth dummy-variable "
                 "W−L spreads, (6,6): replication vs paper",
                 fontsize=12.5, y=0.97)
    fig.text(0.5, 0.015, note,
             ha="center", va="bottom", fontsize=9, style="italic", color="0.3")
    fig.tight_layout(rect=[0, 0.06, 1, 0.91])
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    return comp


# --------------------------------------------------------------------------
def main() -> None:
    plt.rcParams.update({
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": DPI,
    })

    sr = pd.read_parquet(intermediate_path("strategy_returns.parquet"))
    fm = pd.read_parquet(intermediate_path("fm_coefficients.parquet"))

    p1 = LAYOUT.result_path("cumulative_wl.png")
    p2 = LAYOUT.result_path("january_effect.png")
    p3 = LAYOUT.result_path("table5_spreads.png")

    end_vals = figure1_cumulative_wl(sr, p1)
    jan = figure2_january_effect(sr, p2)
    comp = figure3_table5_spreads(fm, p3)

    # Console summary (for the rep-worker report).
    print("Cumulative $1 end-values: "
          + ", ".join(f"{k.upper()}={v:.3f}" for k, v in end_vals.items()))
    print("\nJanuary-effect means (%/month):")
    print(jan.to_string(index=False, float_format=lambda v: f"{v:.2f}"))
    print("\nTable V (6,6) spreads — ours vs paper (%/month):")
    print(comp.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"\nSaved: {p1}\nSaved: {p2}\nSaved: {p3}")


if __name__ == "__main__":
    main()
