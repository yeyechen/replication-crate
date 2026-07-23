"""
Replication of Fama & French (1992) "The Cross-Section of Expected Stock Returns"
=================================================================================
Stage: January-seasonality corollary for the ln(BE/ME) slope (paper
`inputs/content.md` L2186). Splits the 330 monthly reg(a) ln(BE/ME)
Fama-MacBeth slopes into January (27 months) vs February-December (303
months) and tests the paper's three claim elements:

  (a) "The average January slopes for ln(BE/ME) are about twice those for
      February to December."                              -> Jan ~= 2 x Feb-Dec
  (b) "the average monthly February-to-December slopes for ln(BE/ME) are
      about 4 standard errors from 0"                     -> Feb-Dec t ~= 4
  (c) "they are close to (within 0.05 of) the average slopes for the whole
      year."                                              -> |full - Feb-Dec| < 0.05

Methodology is IDENTICAL to src/table_3_6.py and is imported from it (no
re-implementation): `prewinsorize` (clip ln_bm/ln_ame/ln_abe/ep_pos at the
monthly 0.005/0.995 cross-sectional fractiles, computed on the valid-return
sample; beta/lnME/ep_dummy untouched — paper L1189, Assumption 9) and
`fm_monthly` (plain monthly cross-sectional OLS with intercept, rows with a
valid return and all regressors present; plain time-series t-statistic, NO
Newey-West — paper L1187). reg(a) = ret ~ ln(ME) + ln(BE/ME), the SAME
specification whose monthly slopes Table VI reports (and which is verified
identical to R7 in table_3_6.py). Slopes are in percent/month (x100).

Input:  data/panel.parquet ONLY (no ClickHouse).
Output: results/table_6_january.md

Auditor-verified expected values (logs/audit1.md, spot-check 11): January
mean 0.606 %/mo, Feb-Dec 0.318 (t = 3.85), full-year 0.341 (gap 0.024).

Usage:
    uv run python replications/the_cross_section_of_expected_stock_returns/src/table_6_january.py
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

import numpy as np   # noqa: E402
import pandas as pd  # noqa: E402

from main import LAYOUT  # noqa: E402
from table_3_6 import prewinsorize, fm_monthly, ts_stats  # noqa: E402

# reg(a) = ret ~ ln(ME) + ln(BE/ME)  (Table VI reg(a); == R7, verified in
# table_3_6.py). The corollary is about the ln(BE/ME) slope of this spec.
REGA_X = ["lnME", "ln_bm"]
COEF = "ln_bm"

# Claim-element thresholds (documented; L2186).
RATIO_LO, RATIO_HI = 1.5, 2.5   # (a) "about twice": ratio within [1.5, 2.5]
T_LO, T_HI = 3.0, 5.0           # (b) "about 4 standard errors": t within [3, 5]
GAP_MAX = 0.05                  # (c) "within 0.05 of" the full-year mean


def decompose(panel: pd.DataFrame) -> dict:
    """Run reg(a) monthly FM, split the ln(BE/ME) slopes by calendar month,
    return the three groups' ts-stats + the gap and ratio."""
    panel = panel.copy()
    panel["ym"] = panel["month"].dt.year * 100 + panel["month"].dt.month
    pw = prewinsorize(panel)
    fm_a = fm_monthly(pw, REGA_X)
    s = fm_a[COEF]
    is_jan = (fm_a.index % 100) == 1
    jan = s[is_jan]
    febdec = s[~is_jan]

    fm_m, fm_sd, fm_t, fm_n = ts_stats(s)
    jn_m, jn_sd, jn_t, jn_n = ts_stats(jan)
    fd_m, fd_sd, fd_t, fd_n = ts_stats(febdec)
    return {
        "full": dict(mean=fm_m, sd=fm_sd, t=fm_t, n=fm_n),
        "jan": dict(mean=jn_m, sd=jn_sd, t=jn_t, n=jn_n),
        "febdec": dict(mean=fd_m, sd=fd_sd, t=fd_t, n=fd_n),
        "gap": abs(fm_m - fd_m),          # |full-year - Feb-Dec|
        "ratio": jn_m / fd_m,             # Jan / Feb-Dec
    }


def verdicts(d: dict) -> list[tuple[str, str, str, str]]:
    """Return (claim element, our value, threshold, verdict) rows."""
    ratio = d["ratio"]
    a = ("(a) January slopes ~ 2x Feb-Dec",
         f"Jan/Feb-Dec = {ratio:.2f} (Jan {d['jan']['mean']:.2f}, "
         f"Feb-Dec {d['febdec']['mean']:.2f})",
         f"ratio in [{RATIO_LO:.1f}, {RATIO_HI:.1f}]",
         "PASS" if RATIO_LO <= ratio <= RATIO_HI else "FAIL")
    t = d["febdec"]["t"]
    b = ("(b) Feb-Dec slope ~ 4 SE from 0",
         f"Feb-Dec t = {t:.2f}",
         f"t in [{T_LO:.1f}, {T_HI:.1f}]",
         "PASS" if T_LO <= t <= T_HI else "FAIL")
    gap = d["gap"]
    c = (r"(c) \|full-year - Feb-Dec\| < 0.05",
         f"gap = {gap:.3f} (full {d['full']['mean']:.2f}, "
         f"Feb-Dec {d['febdec']['mean']:.2f})",
         f"gap < {GAP_MAX:.2f}",
         "PASS" if gap < GAP_MAX else "FAIL")
    return [a, b, c]


def build_md(d: dict, n_permno: int) -> str:
    v = verdicts(d)
    g, j, f = d["full"], d["jan"], d["febdec"]
    md = []
    md.append("# Table VI Corollary — January seasonality of the ln(BE/ME) slope")
    md.append("")
    md.append("Fama & French (1992), *The Cross-Section of Expected Stock "
              "Returns*. Decomposition of the 330 monthly Fama-MacBeth "
              "**reg(a)** ln(BE/ME) slopes (ret ~ ln(ME) + ln(BE/ME)) into "
              "January vs February-December, testing the paper's "
              "January-seasonality corollary.")
    md.append("")
    md.append("> **Paper claim (`inputs/content.md` L2186):** \"The average "
              "January slopes for ln(BE/ME) are about twice those for February "
              "to December. ... the average monthly February-to-December slopes "
              "for ln(BE/ME) are about 4 standard errors from 0, and they are "
              "close to (within 0.05 of) the average slopes for the whole "
              "year.\"")
    md.append("")
    md.append("**Methodology.** Identical to `src/table_3_6.py` (imported, not "
              "re-implemented): `prewinsorize` clips ln(BE/ME), ln(A/ME), "
              "ln(A/BE), E(+)/P at each month's 0.005/0.995 cross-sectional "
              "fractiles (fractiles on the valid-return sample; beta, ln(ME), "
              "E/P dummy untouched — paper L1189, Assumption 9); `fm_monthly` "
              "fits a plain monthly cross-sectional OLS with intercept on the "
              "rows with a valid return; slopes are the time-series mean of the "
              "330 monthly estimates x100 (%/month); the t-statistic is the "
              "mean divided by its time-series standard error (plain "
              "time-series t, NO Newey-West — paper L1187). reg(a) is the SAME "
              "specification Table VI reports (verified identical to R7). Reads "
              "only `data/panel.parquet`.")
    md.append("")
    md.append("## Decomposition of the monthly ln(BE/ME) slopes")
    md.append("")
    md.append("| Group | N months | Mean (%/mo) | Std (%/mo) | t-stat |")
    md.append("|---|---:|---:|---:|---:|")
    md.append(f"| January | {j['n']} | {j['mean']:.3f} | {j['sd']:.3f} | "
              f"{j['t']:.2f} |")
    md.append(f"| February-December | {f['n']} | {f['mean']:.3f} | "
              f"{f['sd']:.3f} | {f['t']:.2f} |")
    md.append(f"| **Full year (Jul 1963 - Dec 1990)** | {g['n']} | "
              f"{g['mean']:.3f} | {g['sd']:.3f} | {g['t']:.2f} |")
    md.append("")
    md.append("## Three-way comparison")
    md.append("")
    md.append(f"- **Jan vs Feb-Dec:** Jan mean {j['mean']:.3f} %/mo is "
              f"**{d['ratio']:.2f}x** the Feb-Dec mean {f['mean']:.3f} %/mo "
              "(\"about twice\").")
    md.append(f"- **Feb-Dec significance:** the Feb-Dec slope is "
              f"**{f['t']:.2f}** standard errors from 0 (\"about 4\").")
    md.append(f"- **Feb-Dec vs full year:** the gap |full-year - Feb-Dec| = "
              f"**{d['gap']:.3f}** (full {g['mean']:.3f}, Feb-Dec "
              f"{f['mean']:.3f}), within the paper's 0.05 bound.")
    md.append("")
    md.append("## Claim-element verdicts (L2186)")
    md.append("")
    md.append("| Claim element (L2186) | Our value | Threshold | Verdict |")
    md.append("|---|---|---|:---:|")
    for elem, ours, thr, verdict in v:
        mark = "PASS" if verdict == "PASS" else "FAIL"
        md.append(f"| {elem} | {ours} | {thr} | **{mark}** |")
    n_pass = sum(1 for *_x, verdict in v if verdict == "PASS")
    md.append("")
    md.append(f"**Overall: {n_pass}/3 claim elements PASS.** "
              + ("The January-seasonality corollary replicates: there is a "
                 "January seasonal in the BE/ME effect (January slopes about "
                 "twice Feb-Dec), but the positive BE/ME relation is strong "
                 "throughout the year (Feb-Dec ~4 SE from 0 and within 0.05 of "
                 "the full-year mean)."
                 if n_pass == 3 else
                 "One or more claim elements did not replicate — see above."))
    md.append("")
    md.append("## Notes")
    md.append("")
    md.append("- The January t-statistic ({:.2f}, N = {} months) is NOT "
              "reported as a claim element; the paper's claim concerns the "
              "*magnitude* of the January slopes relative to Feb-Dec, and the "
              "*significance* of the Feb-Dec slopes. The wide January "
              "standard deviation ({:.3f}) over only {} Januaries is why the "
              "January mean, though larger, is itself less precisely "
              "estimated than the Feb-Dec mean.".format(
                  j["t"], j["n"], j["sd"], j["n"]))
    md.append(f"- reg(a) ln(ME) (size) slopes are not decomposed here; the "
              f"corollary (L2186) is specifically about the BE/ME effect, "
              f"contrasting it with the well-known January seasonality of the "
              f"size effect (Roll 1983; Keim 1983).")
    md.append(f"- Panel: {d['full']['n']} months (Jul 1963 - Dec 1990), "
              f"{n_permno:,} permnos; reg(a) fit on the valid-return rows each "
              f"month, same as Tables III/VI.")
    md.append("")
    md.append("---")
    md.append("*Computed by src/table_6_january.py from data/panel.parquet, "
              "importing prewinsorize + fm_monthly + ts_stats from "
              "src/table_3_6.py (same winsorization, same reg(a) = [ln(ME), "
              "ln(BE/ME)] specification, plain monthly OLS).*")
    return "\n".join(md)


def main() -> None:
    t0 = time.time()
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    n_permno = int(panel["permno"].nunique())
    d = decompose(panel)
    v = verdicts(d)

    out = LAYOUT.result_path("table_6_january.md")
    out.write_text(build_md(d, n_permno))
    print(f"wrote {out}")

    # ---- console report ----
    print("\n===== JANUARY-SEASONALITY COROLLARY (reg(a) ln(BE/ME) slopes) =====")
    print(f"  Full year      : mean {d['full']['mean']:.3f} %/mo, "
          f"t {d['full']['t']:.2f}, N {d['full']['n']}")
    print(f"  January        : mean {d['jan']['mean']:.3f} %/mo, "
          f"t {d['jan']['t']:.2f}, N {d['jan']['n']}")
    print(f"  Feb-December   : mean {d['febdec']['mean']:.3f} %/mo, "
          f"t {d['febdec']['t']:.2f}, N {d['febdec']['n']}")
    print(f"  Jan/Feb-Dec ratio : {d['ratio']:.3f}")
    print(f"  |full - Feb-Dec|  : {d['gap']:.4f}")
    print("  ---- claim-element verdicts (L2186) ----")
    for elem, ours, thr, verdict in v:
        print(f"  [{verdict}] {elem.replace(chr(92) + chr(124), chr(124))}: "
              f"{ours}  ({thr})")
    print(f"\ntotal time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
