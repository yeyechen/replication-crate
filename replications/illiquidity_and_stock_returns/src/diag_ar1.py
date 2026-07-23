"""
DIAGNOSTIC ONLY — Amihud (2002) replication. Does NOT touch canonical
artifacts (src/main.py, data/panel.parquet, data/ailliq.parquet, ...).

Task A: annual AILLIQ_TS universe variants (1963-1996), each = mean of
per-stock annual ILLIQ (x1e6, pipeline formula) excluding the UPPER 1%
tail per year:
  A1 current  : stocks passing admission (i)-(iii) [data/ailliq.parquet]
  A2 NYSE all : ALL NYSE common stocks (shrcd 10/11, hexcd 1 PIT) with
                >= 1 valid trading day — no >200-day / $5 / Dec-listing
                filters [from data/_cache/chars_annual.parquet]
  A3 any shrcd: ALL NYSE securities with daily data [new query,
                data/_cache/diag_chars_allshrcd.parquet]
Per variant: 34-value series + AR(1) of ln(ailliq_y) on ln(ailliq_{y-1})
over 1964-1996 (T=33): intercept, slope, t-stats, R2, DW, Kendall-
corrected slope, residual lag-1 autocorrelation; paper shape check.

Task D: mean(ln MILLIQ) of the 408-month series and implied intercepts
(1-slope)*mean for paper slope 0.945 and our slope.

Paper annual targets: -0.200 + 0.768 (t 1.70, 5.89), R2 0.53, DW 1.57,
Kendall-corrected 0.869; shape "peaked mid-1970s, rose again in 1990,
low in 1968, mid-1980s and 1996".

Run: python replications/illiquidity_and_stock_returns/src/diag_ar1.py
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson

import main  # noqa: E402  (reuses client/q_file/cached/LAYOUT; safe import)

TAIL = 0.01
YEARS = list(range(1963, 1997))
PAPER = dict(intercept=-0.200, slope=0.768, t_i=1.70, t_s=5.89,
             r2=0.53, dw=1.57, kc=0.869)


# ---------------------------------------------------------------- A-series
def ailliq_open_universe(chars: pd.DataFrame) -> pd.DataFrame:
    """Mean annual ILLIQ (x1e6) over stocks with >= 1 valid trading day
    (illiq non-null), excluding the upper 1% tail per year (strict <) —
    the paper's literal AILLIQ_TS definition, no admission filters."""
    rows = []
    for y, g in chars.groupby("y"):
        ill = g["illiq"].dropna().to_numpy(dtype=float)
        if len(ill) == 0:
            continue
        hi = np.percentile(ill, 100 * (1 - TAIL))
        keep = ill[ill < hi]
        rows.append({"year": int(y), "ailliq": float(keep.mean()),
                     "n_stocks": int(len(keep))})
    df = pd.DataFrame(rows).sort_values("year").reset_index(drop=True)
    df["ln"] = np.log(df["ailliq"])
    return df


def a1_series() -> pd.DataFrame:
    a = pd.read_parquet(main.LAYOUT.data_path("ailliq.parquet"))
    df = pd.DataFrame({"year": a["year"].astype(int),
                       "ailliq": a["ailliq_ts"].astype(float),
                       "n_stocks": a["n_stocks_ts"].astype(int)})
    df["ln"] = np.log(df["ailliq"])
    return df.sort_values("year").reset_index(drop=True)


def a1_recomputed() -> pd.DataFrame:
    """A1 via the canonical admission path, as a cross-check of A1."""
    chars = main.cached("chars_annual.parquet", main.load_characteristics)
    _, ailliq = main.apply_admission(chars)
    df = pd.DataFrame({"year": ailliq["year"].astype(int),
                       "ailliq": ailliq["ailliq_ts"].astype(float),
                       "n_stocks": ailliq["n_stocks_ts"].astype(int)})
    df["ln"] = np.log(df["ailliq"])
    return df.sort_values("year").reset_index(drop=True)


def a2_series() -> pd.DataFrame:
    chars = main.cached("chars_annual.parquet", main.load_characteristics)
    chars["illiq"] = pd.to_numeric(chars["illiq"], errors="coerce")
    return ailliq_open_universe(chars)


def a3_series() -> pd.DataFrame:
    df = main.cached(
        "diag_chars_allshrcd.parquet",
        lambda: main.q_file("diag_chars_allshrcd.sql"))
    df["illiq"] = pd.to_numeric(df["illiq"], errors="coerce")
    return ailliq_open_universe(df)


# ---------------------------------------------------------------- AR(1)
def ar1(df: pd.DataFrame) -> dict:
    l = df.set_index("year")["ln"]
    xr = l.reindex(range(1964, 1997)).to_numpy(dtype=float)   # y: 1964..1996
    xl = l.reindex(range(1963, 1996)).to_numpy(dtype=float)   # lag
    res = sm.OLS(xr, sm.add_constant(xl)).fit()
    T = int(res.nobs)
    slope = float(res.params[1])
    resid = np.asarray(res.resid)
    rho = float(np.corrcoef(resid[:-1], resid[1:])[0, 1])
    return dict(intercept=float(res.params[0]), slope=slope,
                t_i=float(res.tvalues[0]), t_s=float(res.tvalues[1]),
                r2=float(res.rsquared), dw=float(durbin_watson(resid)),
                n=T, kc=slope + (1 + 3 * slope) / T, rho_resid=rho)


def shape_check(df: pd.DataFrame) -> dict:
    a = df.set_index("year")["ailliq"]
    peak = int(a.idxmax())
    smin = int(a.idxmin())
    mid80s_min = int(a.loc[1984:1987].idxmin())
    return dict(
        peak_year=peak,
        peak_mid1970s=(1973 <= peak <= 1976),
        v1968_local_min=(a.loc[1968] < a.loc[1967] and a.loc[1968] < a.loc[1969]),
        v1990_rises=(a.loc[1990] > a.loc[1989]),
        mid1980s_low_year=mid80s_min,
        v1996_is_series_min=(smin == 1996),
        series_min_year=smin,
    )


def print_variant(tag: str, title: str, df: pd.DataFrame) -> dict:
    print(f"\n--- {tag}: {title} ---")
    with pd.option_context("display.float_format", lambda v: f"{v:10.6f}",
                           "display.width", 200):
        print(df.to_string(index=False))
    st = ar1(df)
    sh = shape_check(df)
    print(f"AR(1) ln(ailliq_y) ~ ln(ailliq_y-1), 1964-1996 (T={st['n']}):")
    print(f"  intercept = {st['intercept']:+.4f} (t = {st['t_i']:.2f})")
    print(f"  slope     = {st['slope']:.4f}  (t = {st['t_s']:.2f})")
    print(f"  R2 = {st['r2']:.4f}   DW = {st['dw']:.3f}   "
          f"resid lag-1 autocorr = {st['rho_resid']:+.4f}")
    print(f"  Kendall-corrected slope = {st['kc']:.4f}")
    print(f"  paper: -0.200 (1.70) + 0.768 (5.89), R2=0.53, DW=1.57 "
          f"(resid rho ~ +0.215), KC=0.869")
    d = dict(slope=abs(st["slope"] - PAPER["slope"]),
             r2=abs(st["r2"] - PAPER["r2"]),
             dw=abs(st["dw"] - PAPER["dw"]))
    print(f"  |diff| vs paper: slope {d['slope']:.3f}, R2 {d['r2']:.3f}, "
          f"DW {d['dw']:.3f}")
    print(f"shape: peak={sh['peak_year']} "
          f"(mid-1970s: {'YES' if sh['peak_mid1970s'] else 'no'}); "
          f"1968 local min: {'YES' if sh['v1968_local_min'] else 'no'}; "
          f"1990 rises vs 1989: {'YES' if sh['v1990_rises'] else 'no'}; "
          f"mid-1980s low year: {sh['mid1980s_low_year']}; "
          f"1996 = series min: {'YES' if sh['v1996_is_series_min'] else 'no'} "
          f"(series min year: {sh['series_min_year']})")
    return dict(stats=st, shape=sh)


# ---------------------------------------------------------------- task D
def task_d() -> None:
    print("\n" + "=" * 72)
    print("TASK D: monthly AR(1) intercept reconciliation")
    print("=" * 72)
    m = pd.read_parquet(main.LAYOUT.data_path("milliq.parquet"))
    m = m.sort_values("month")
    lm = np.log(m["milliq"].to_numpy(dtype=float))
    res = sm.OLS(lm[1:], sm.add_constant(lm[:-1])).fit()
    slope = float(res.params[1])
    mean_ln = float(lm.mean())
    print(f"n months = {len(lm)} "
          f"({pd.to_datetime(m['month'].min()).date()} .. "
          f"{pd.to_datetime(m['month'].max()).date()})")
    print(f"ln MILLIQ: mean = {mean_ln:.4f}, sd = {lm.std(ddof=1):.4f}, "
          f"min = {lm.min():.4f}, max = {lm.max():.4f}")
    print(f"our AR(1): intercept = {res.params[0]:+.4f}, slope = {slope:.4f}, "
          f"R2 = {res.rsquared:.4f}, DW = {durbin_watson(res.resid):.3f}")
    print(f"implied intercept (1 - 0.945)*mean = "
          f"{(1 - 0.945) * mean_ln:+.4f}   [paper slope]")
    print(f"implied intercept (1 - {slope:.4f})*mean = "
          f"{(1 - slope) * mean_ln:+.4f}   [our slope]")
    print(f"paper reports monthly intercept -0.313 (slope 0.945): "
          f"inconsistent with its own slope+level "
          f"(|-0.313 - {(1 - 0.945) * mean_ln:.3f}| = "
          f"{abs(-0.313 - (1 - 0.945) * mean_ln):.3f}); we keep ours.")
    imp_annual = (1 - PAPER["slope"]) * mean_ln
    print(f"note: (1 - 0.768 annual slope)*mean = {imp_annual:+.4f} "
          f"-- within {abs(-0.313 - imp_annual):.3f} of the paper's monthly "
          f"intercept -0.313 (the monthly intercept looks computed with "
          f"the ANNUAL slope).")


def main_diag() -> None:
    print("=" * 72)
    print("TASK A: AILLIQ_TS universe variants (annual, 1963-1996)")
    print("=" * 72)
    res = {}
    a1 = a1_series()
    res["A1"] = print_variant(
        "A1", "current pipeline: admitted (i)-(iii), upper-1% tail excluded "
        "(data/ailliq.parquet)", a1)
    # cross-check A1 via recomputed admission path
    a1c = a1_recomputed()
    d = (a1.set_index("year")["ailliq"] - a1c.set_index("year")["ailliq"]).abs().max()
    print(f"[A1 cross-check] max |ailliq.parquet - recomputed| = {d:.2e}")
    res["A2"] = print_variant(
        "A2", "ALL NYSE common (shrcd 10/11, hexcd 1 PIT) with >= 1 valid "
        "day; no admission filters", a2_series())
    res["A3"] = print_variant(
        "A3", "ALL NYSE securities (any shrcd, hexcd 1 PIT) with >= 1 valid "
        "day [reference only]", a3_series())

    print("\n--- TASK A summary vs paper AR(1) (-0.200+0.768, R2 .53, "
          "DW 1.57) and shape ---")
    for tag, r in res.items():
        st, sh = r["stats"], r["shape"]
        nshape = sum([sh["peak_mid1970s"], sh["v1968_local_min"],
                      sh["v1990_rises"], sh["v1996_is_series_min"]])
        print(f"  {tag}: slope={st['slope']:.3f} R2={st['r2']:.3f} "
              f"DW={st['dw']:.3f} rho={st['rho_resid']:+.3f} "
              f"KC={st['kc']:.3f}; shape score {nshape}/4 "
              f"(peak {sh['peak_year']}, 68min "
              f"{int(sh['v1968_local_min'])}, 90rise "
              f"{int(sh['v1990_rises'])}, 96min "
              f"{int(sh['v1996_is_series_min'])})")

    task_d()


if __name__ == "__main__":
    main_diag()
