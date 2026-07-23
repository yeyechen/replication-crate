"""
Foster, Olsen & Shevlin (1984) — INNER ITERATION 3: Tables 1, 3, 4, 6, 7.

Reads the cached Iteration-1 artifacts (panel / decile_returns / event_returns
parquets) plus src/sql/market_index.sql, and writes:

  results/table_1.md, table_3.md, table_4.md, table_6.md, table_7.md
  results/cells_iter2.csv     — every registry cell (798 rows), names matching
                                preparations/tables_to_replicate.json
                                (T7 names use the variant-aware fep|fsq|both
                                convention from the task spec, assigned
                                positionally because the registry's literal T7
                                names are duplicated across the three eq-16
                                regressions — see note below)
  results/drift_bars_m2.png, event_car_m2.png, quarterly_car_m2.png

Iteration-3 changes vs iteration-2:
  A) Table 3 SW beta -> Dimson (1979) summed-beta estimator (the implementable
     form of the Scholes-Williams non-synchronous-trading correction).
  B) Table 4 significance -> the paper's two-stage draw (8,000 firm/quarter
     pairs from the full frame, then keep the available ones).
  C) Table 6 (size-quintile CARs), D) Table 7 (eq. 16 regressions).
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402
from clickhouse_driver import Client  # noqa: E402

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402

LAYOUT = paper_layout("earnings_releases_anomalies")
SQL_DIR = LAYOUT.src_path("sql")
_CFG = get_clickhouse_config()
WINDOWS = [("m1_0", "car_m1_0"), ("m60_0", "car_m60_0"), ("p1_60", "car_p1_60")]
WIN_LABEL = {"m1_0": "[-1, 0]", "m60_0": "[-60, 0]", "p1_60": "[+1, +60]"}
QLABELS = [y * 10 + q for y in range(1974, 1982) for q in range(1, 5)]  # 32


def q(sql: str) -> pd.DataFrame:
    c = Client(host=os.getenv("CLICKHOUSE_HOST", _CFG["host"]),
               port=int(os.getenv("CLICKHOUSE_PORT", _CFG["port"])),
               user=os.getenv("CLICKHOUSE_USER", _CFG["user"]),
               password=os.getenv("CLICKHOUSE_PASSWORD", _CFG["password"]),
               settings={"max_execution_time": 300})
    data, cols = c.execute(sql.strip().rstrip(";"), with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    return q(Path(SQL_DIR / name).read_text())


def ols_slope(x, y) -> float:
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    return float(np.linalg.lstsq(np.column_stack([np.ones(len(x)), x]), y, rcond=None)[0][1])


# --- registry -> ordered intended-name target list ----------------------------
# The registry's T7 metric names are DUPLICATED (the FEP-only / FSQ-only / both
# regressions share the literal suffix _fep_alpha, _fep_t_alpha, _fep_b2 etc.);
# only _adj_r2 carries the variant token. The task spec's variant-aware naming
# (fep|fsq|both) is what yields unique names, so we assign T7 targets
# positionally (17 per (model, window): fep[5] + fsq[5] + both[7]).
_T7_SUFFIX = ["fep_alpha", "fep_t_alpha", "fep_b1", "fep_t_b1", "fep_adj_r2",
              "fsq_alpha", "fsq_t_alpha", "fsq_b2", "fsq_t_b2", "fsq_adj_r2",
              "both_alpha", "both_t_alpha", "both_b1", "both_t_b1",
              "both_b2", "both_t_b2", "both_adj_r2"]
REG = json.loads(Path(LAYOUT.preparations_path("tables_to_replicate.json")).read_text())
_TABLES = REG["tables"] if isinstance(REG, dict) else REG
ALL_TARGETS: list[tuple[str, str, float, float]] = []  # (tid, name, paper, tol)
_HANDLED = {"T1", "T3", "T4", "T5", "T6", "T7", "T8", "T9"}
CUTOFF_Q0, CUTOFF_Q1 = 7896, 7927  # 1973Q4..1981Q3 cutoffs (assign 1974Q1..1981Q4)
for tbl in _TABLES:
    tid = tbl["id"]
    if tid == "T7":
        cnt: dict[tuple[str, str], int] = {}
        for met in tbl["metrics"]:
            nm = met["name"]
            parts = nm.split("_")
            mw = (parts[0], parts[1] + "_" + parts[2])  # (m{k}, window)
            k = cnt.get(mw, 0)
            intended = f"{mw[0]}_{mw[1]}_{_T7_SUFFIX[k]}"
            cnt[mw] = k + 1
            ALL_TARGETS.append((tid, intended, float(met["value"]), float(met["tolerance_pct"])))
        assert all(v == 17 for v in cnt.values()) and len(cnt) == 12, cnt
    elif tid in _HANDLED:
        for met in tbl["metrics"]:
            ALL_TARGETS.append((tid, met["name"], float(met["value"]), float(met["tolerance_pct"])))
    else:
        raise ValueError(f"unhandled table id {tid}")
assert {t["id"] for t in _TABLES} <= _HANDLED, {t["id"] for t in _TABLES}
# TARGETS name->(tid,paper,tol): names collide across T4/T8 and T6/T9, so this dict
# is ONLY safe for keys read from it (T3 in table_3 md + report). Tally/CSV dispatch by tid.
TARGETS = {nm: (tid, pv, tol) for (tid, nm, pv, tol) in ALL_TARGETS}
assert len(ALL_TARGETS) == 1188, len(ALL_TARGETS)


def tier(ours: float, paper: float, tol_pct: float) -> str:
    if not np.isfinite(ours):
        return "FAIL"
    if paper == 0.0:
        return "T1" if ours == 0.0 else ("T2" if abs(ours) <= 0.25 else "FAIL")
    if abs(ours - paper) <= (tol_pct / 100.0) * abs(paper):
        return "T1"
    if ((ours >= 0) == (paper >= 0)) and 0.5 <= abs(ours) / abs(paper) <= 2.0:
        return "T2"
    return "FAIL"


def fsq_code(fep: int, quintile: int) -> int:  # L2102
    return (11 - quintile) if fep <= 5 else quintile


def main():
    t0 = time.time()
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["qidx"] = panel["fyearq"].astype(int) * 4 + panel["fqtr"].astype(int)
    decile_returns = pd.read_parquet(LAYOUT.data_path("cache/decile_returns.parquet"))
    decile_returns["date"] = pd.to_datetime(decile_returns["date"])
    print(f"[{time.time() - t0:5.1f}s] loaded panel {panel.shape}, decile_returns {decile_returns.shape}")
    comp: dict[str, float] = {}  # intended_name -> computed value (T1/T3/T4/T6/T7)
    comp2: dict[str, float] = {}  # T5/T8/T9 (their names collide with T4/T6 names)

    # =========================================================================
    # Table 3 — mean daily return, OLS beta, Dimson (1979) summed beta (A17)
    # =========================================================================
    dsi = q_file("market_index.sql")
    dsi["date"] = pd.to_datetime(dsi["date"])
    dsi = dsi.sort_values("date").reset_index(drop=True)
    dsi["m_lag"] = dsi["ewretd"].shift(1)
    dsi["m_lead"] = dsi["ewretd"].shift(-1)
    dr = decile_returns.copy(); dr["year"] = dr["date"].dt.year
    dr7381 = dr[(dr["date"] >= "1973-01-01") & (dr["date"] <= "1981-12-31")]
    avg_ret_pct = dr7381.groupby("decile")["ret_ew"].mean() * 100.0
    mr = dr.merge(dsi[["date", "ewretd", "m_lag", "m_lead"]], on="date", how="inner")
    mr = mr.dropna(subset=["ewretd", "m_lag", "m_lead", "ret_ew"])
    mr["year"] = mr["date"].dt.year

    beta_ols, beta_dim = {}, {}
    for dec in range(1, 11):
        ols_y, dim_y = [], []
        for Y in range(1973, 1983):
            s = mr[(mr["year"] == Y) & (mr["decile"] == dec)]
            ols_y.append(ols_slope(s["ewretd"].to_numpy(), s["ret_ew"].to_numpy()))
            if 1974 <= Y <= 1981:
                A = np.column_stack([np.ones(len(s)), s["m_lag"].to_numpy(),
                                     s["ewretd"].to_numpy(), s["m_lead"].to_numpy()])
                b = np.linalg.lstsq(A, s["ret_ew"].to_numpy(), rcond=None)[0]
                dim_y.append(float(b[1] + b[2] + b[3]))  # b_lag + b_contemp + b_lead
        beta_ols[dec] = float(np.mean(ols_y[:9]))          # 1973..1981
        beta_dim[dec] = float(np.mean(dim_y))              # 1974..1981
    for dec in range(1, 11):
        comp[f"d{dec}_ret"] = avg_ret_pct[dec]
        comp[f"d{dec}_beta_ols"] = beta_ols[dec]
        comp[f"d{dec}_beta_sw"] = beta_dim[dec]

    lines = [
        "# Table 3 — NYSE Firm Size Deciles, 1973-1981",
        "",
        "Mean daily EW decile return (percent/day) over 1973-1981; average annual OLS",
        "market-model beta over 9 years (1973-1981, market = CRSP EW NYSE+AMEX dsi.ewretd,",
        "A13); and the Dimson (1979) summed-beta estimator used here as the implementable",
        "form of the Scholes-Williams (1977) non-synchronous-trading correction: for each",
        "year y in 1974-1981 one OLS of the decile EW return on (r_m,t-1, r_m,t, r_m,t+1),",
        "beta_SW,y = b_lag + b_contemp + b_lead, averaged over the 8 years (the paper's",
        "exact SW formula variant is not stated; the previous iteration's",
        "(beta_{y-1}+2beta_y+beta_{y+1})/(1+2rho_y) form was structurally incapable of",
        "matching — see iteration-2 diagnosis).",
        "",
        "| Size decile | Mean daily return (%) | Paper | Mean OLS beta | Paper | Mean SW/Dimson beta | Paper |",
        "|---|---|---|---|---|---|---|",
    ]
    for dec in range(1, 11):
        tag = " (smallest)" if dec == 1 else " (largest)" if dec == 10 else ""
        lines.append(f"| {dec}{tag} | {comp[f'd{dec}_ret']:.3f} | {TARGETS[f'd{dec}_ret'][1]:.3f} "
                     f"| {comp[f'd{dec}_beta_ols']:.2f} | {TARGETS[f'd{dec}_beta_ols'][1]:.2f} "
                     f"| {comp[f'd{dec}_beta_sw']:.2f} | {TARGETS[f'd{dec}_beta_sw'][1]:.2f} |")
    Path(LAYOUT.result_path("table_3.md")).write_text("\n".join(lines) + "\n")
    print(f"[{time.time() - t0:5.1f}s] Table 3 written (Dimson SW)")

    # =========================================================================
    # Table 1 — unconditional & conditional FEP relative frequencies
    # =========================================================================
    for m in range(1, 5):
        sub = panel[["gvkey", "qidx", f"fep{m}"]].dropna()
        sub = sub.astype({"gvkey": str, "qidx": int, f"fep{m}": int})
        uncond = sub[f"fep{m}"].value_counts(normalize=True)
        cur = sub.rename(columns={"qidx": "t", f"fep{m}": "f_cur"})
        prev = sub.rename(columns={"qidx": "t_prev", f"fep{m}": "f_prev"})
        cond = {}
        for n in range(1, 5):
            j = cur.assign(key=cur["t"] - n).merge(prev, left_on=["gvkey", "key"],
                                                    right_on=["gvkey", "t_prev"])
            cond[n] = {jv: float((g["f_prev"] == jv).mean()) if len(g) else float("nan")
                       for jv, g in j.groupby("f_cur")}
        for jv in range(1, 11):
            comp[f"m{m}_fep{jv}_uncond"] = float(uncond.get(jv, 0.0))
            for n in range(1, 5):
                comp[f"m{m}_fep{jv}_cond_l{n}"] = float(cond[n].get(jv, float("nan")))

    lines = ["# Table 1 — Unconditional and Conditional Relative Frequencies of FEP Membership",
             "", "Unconditional = share of non-null assignments in FEP j (32q, 1974Q1-1981Q4).",
             "Conditional L_n = share in FEP j at t-n among obs in FEP j at t whose firm also",
             "has a non-null FEP at t-n (qidx quarter arithmetic, year-crossing safe).", ""]
    for m in range(1, 5):
        lines += [f"## Model {m}", "", "| FEP | Uncond | Cond L1 | Cond L2 | Cond L3 | Cond L4 |",
                  "|---|---|---|---|---|---|"]
        for jv in range(1, 11):
            lines.append(f"| {jv} | {comp[f'm{m}_fep{jv}_uncond']:.3f} "
                         f"| {comp[f'm{m}_fep{jv}_cond_l1']:.3f} | {comp[f'm{m}_fep{jv}_cond_l2']:.3f} "
                         f"| {comp[f'm{m}_fep{jv}_cond_l3']:.3f} | {comp[f'm{m}_fep{jv}_cond_l4']:.3f} |")
        lines.append("")
    Path(LAYOUT.result_path("table_1.md")).write_text("\n".join(lines) + "\n")
    print(f"[{time.time() - t0:5.1f}s] Table 1 written")

    # =========================================================================
    # Table 6 — size-quintile CARs (M2 & M4), full 10x5x3 display + registry cells
    # =========================================================================
    t6_car: dict[tuple[int, int, int, str], float] = {}  # (m, fep, quintile, w)
    for m in (1, 2, 3, 4):  # all 4 needed for Table 7 regressions; T6 md/csv = m2,m4 only
        g = panel[[f"fep{m}", "quintile"] + [c for _, c in WINDOWS]]
        for wkey, wcol in WINDOWS:
            means = g.dropna(subset=[f"fep{m}", wcol]).groupby([f"fep{m}", "quintile"])[wcol].mean() * 100.0
            for (fep, qv), val in means.items():
                t6_car[(m, int(fep), int(qv), wkey)] = float(val)
    # registry T6 names -> comp (only names the registry has; OCR-missing m2 cells excluded)
    n_t6 = 0
    for nm in list(TARGETS):
        if nm.startswith(("m2_fep", "m4_fep")) and "_q" in nm:
            body = nm.split("_")
            m = int(body[0][1:]); fep = int(body[1][3:]); qv = int(body[2][1:])
            w = "_".join(body[3:])  # window token contains an underscore (m1_0, p1_60)
            comp[nm] = t6_car.get((m, fep, qv, w), float("nan"))
            n_t6 += 1
    lines = ["# Table 6 — Cumulative Average Residuals by FEP x NYSE Size Quintile (Model 2 & 4)",
             "", "CAR (percent) = mean per-observation CAR grouped by (fep_m, quintile);",
             "quintile = ceil(decile/2) from the announcement-year NYSE decile (A15).",
             "Model 2 is shown for all ten FEPs (our computation; the paper's OCR is damaged",
             "for M2 FEP7-10 in the registry).", ""]
    for m in (2, 4):
        lines.append(f"## Model {m}")
        for wkey, _ in WINDOWS:
            lines += ["", f"### Window {WIN_LABEL[wkey]}", "",
                      "| FEP | Q I | Q II | Q III | Q IV | Q V |", "|---|---|---|---|---|---|"]
            for fep in range(1, 11):
                vals = [t6_car.get((m, fep, qv, wkey), float("nan")) for qv in range(1, 6)]
                lines.append("| " + str(fep) + " | " + " | ".join(f"{v:.2f}" for v in vals) + " |")
        lines.append("")
    Path(LAYOUT.result_path("table_6.md")).write_text("\n".join(lines) + "\n")
    print(f"[{time.time() - t0:5.1f}s] Table 6 written ({n_t6} registry cells; full M2 10x5x3 displayed)")

    # =========================================================================
    # Table 7 — eq. 16 regressions (CAR ~ FEP, ~ FSQ, ~ FEP+FSQ) over the 10x5 cells
    # =========================================================================
    t7: dict[tuple[int, str], dict] = {}
    lines = ["# Table 7 — Regression Statistics for CAR_j on FEP_j and FSQ_j (eq. 16)",
             "", "50 portfolio observations (FEP 1-10 x quintile I-V); FSQ coding per L2102",
             "(FEP1-5: I-V = 10,9,8,7,6; FEP6-10: I-V = 1,2,3,4,5). OLS with intercept via",
             "statsmodels; rows with a missing Table-6 cell dropped. Reported: alpha, t(alpha),",
             "b1/b2, t(b1/b2), adjusted R-squared.", ""]
    n_t7 = 0
    for m in range(1, 5):
        for wkey, _ in WINDOWS:
            rows = []
            for fep in range(1, 11):
                for qv in range(1, 6):
                    car = t6_car.get((m, fep, qv, wkey), float("nan"))
                    rows.append({"CAR": car, "FEP": float(fep), "FSQ": float(fsq_code(fep, qv))})
            dfr = pd.DataFrame(rows).dropna()
            res = {}
            for spec, key in ((["FEP"], "fep"), (["FSQ"], "fsq"), (["FEP", "FSQ"], "both")):
                if len(dfr) < len(spec) + 2:
                    res[key] = {"alpha": float("nan"), "t_alpha": float("nan"),
                                "b1": float("nan"), "t_b1": float("nan"),
                                "b2": float("nan"), "t_b2": float("nan"),
                                "adj_r2": float("nan"), "n": int(len(dfr))}
                    continue
                X = sm.add_constant(dfr[spec]); y = dfr["CAR"]
                r = sm.OLS(y, X).fit()
                p = r.params; t = r.tvalues
                res[key] = {
                    "alpha": float(p["const"]), "t_alpha": float(t["const"]),
                    "b1": float(p["FEP"]) if "FEP" in p else float("nan"),
                    "t_b1": float(t["FEP"]) if "FEP" in t else float("nan"),
                    "b2": float(p["FSQ"]) if "FSQ" in p else float("nan"),
                    "t_b2": float(t["FSQ"]) if "FSQ" in t else float("nan"),
                    "adj_r2": float(r.rsquared_adj), "n": int(r.nobs),
                }
            t7[(m, wkey)] = res
            s = res
            lines.append(f"### Model {m}, window {WIN_LABEL[wkey]}  (n: fep={s['fep']['n']} fsq={s['fsq']['n']} both={s['both']['n']})")
            lines.append("")
            lines.append("| spec | alpha | t(alpha) | b1(FEP) | t(b1) | b2(FSQ) | t(b2) | adj R2 |")
            lines.append("|---|---|---|---|---|---|---|---|")
            for key, label in (("fep", "FEP-only"), ("fsq", "FSQ-only"), ("both", "FEP+FSQ")):
                r = s[key]
                lines.append(f"| {label} | {r['alpha']:.2f} | {r['t_alpha']:.2f} | "
                             f"{r['b1']:.2f} | {r['t_b1']:.2f} | {r['b2']:.2f} | {r['t_b2']:.2f} | {r['adj_r2']:.3f} |")
            lines.append("")
            for suf, val in (("fep_alpha", s["fep"]["alpha"]), ("fep_t_alpha", s["fep"]["t_alpha"]),
                             ("fep_b1", s["fep"]["b1"]), ("fep_t_b1", s["fep"]["t_b1"]),
                             ("fep_adj_r2", s["fep"]["adj_r2"]),
                             ("fsq_alpha", s["fsq"]["alpha"]), ("fsq_t_alpha", s["fsq"]["t_alpha"]),
                             ("fsq_b2", s["fsq"]["b2"]), ("fsq_t_b2", s["fsq"]["t_b2"]),
                             ("fsq_adj_r2", s["fsq"]["adj_r2"]),
                             ("both_alpha", s["both"]["alpha"]), ("both_t_alpha", s["both"]["t_alpha"]),
                             ("both_b1", s["both"]["b1"]), ("both_t_b1", s["both"]["t_b1"]),
                             ("both_b2", s["both"]["b2"]), ("both_t_b2", s["both"]["t_b2"]),
                             ("both_adj_r2", s["both"]["adj_r2"])):
                comp[f"m{m}_{wkey}_{suf}"] = val
                n_t7 += 1
    Path(LAYOUT.result_path("table_7.md")).write_text("\n".join(lines) + "\n")
    print(f"[{time.time() - t0:5.1f}s] Table 7 written ({n_t7} cells)")

    # =========================================================================
    # Table 4 — CARs + two-stage significance (B)
    # =========================================================================
    car_cells = {}
    for m in range(1, 5):
        g = panel[[f"fep{m}"] + [c for _, c in WINDOWS]]
        for wkey, wcol in WINDOWS:
            means = g.dropna(subset=[f"fep{m}"]).groupby(f"fep{m}")[wcol].mean() * 100.0
            for jv in range(1, 11):
                car_cells[(m, jv, wkey)] = float(means.get(jv, float("nan")))
    for (m, jv, wkey), val in car_cells.items():
        comp[f"m{m}_fep{jv}_{wkey}"] = val

    # Two-stage empirical distribution (paper L1357-1363). Frame = firms appearing
    # in the panel at least once x 32 qlabels; draw 8,000 firm/quarter pairs without
    # replacement; keep those present in the per-window availability pool; mean CAR
    # of the kept set (x100); 1,000 trials; seed=42.
    rng = np.random.default_rng(42)
    firms = sorted(panel["gvkey"].astype(str).unique())
    firm_i = {f: i for i, f in enumerate(firms)}
    ql_i = {ql: j for j, ql in enumerate(QLABELS)}
    n_frame = len(firms) * len(QLABELS)
    car_frame = {wkey: np.full(n_frame, np.nan) for wkey, _ in WINDOWS}
    gv = panel["gvkey"].astype(str).to_numpy()
    ql = panel["qlabel"].astype(int).to_numpy()
    for wkey, wcol in WINDOWS:
        vals = (panel[wcol].to_numpy(dtype=float)) * 100.0
        cf = car_frame[wkey]
        for gi in range(len(panel)):
            f = gv[gi]; q = ql[gi]
            if f in firm_i and q in ql_i and not np.isnan(vals[gi]):
                cf[firm_i[f] * len(QLABELS) + ql_i[q]] = vals[gi]
    pct = {}
    kept_sizes = {}
    for wkey, _ in WINDOWS:
        cf = car_frame[wkey]
        means = np.empty(1000); ks = np.empty(1000, dtype=int)
        for tt in range(1000):
            idx = rng.choice(n_frame, size=8000, replace=False)
            v = cf[idx]; v = v[~np.isnan(v)]
            ks[tt] = len(v); means[tt] = v.mean() if v.size else np.nan
        pct[wkey] = (float(np.percentile(means, 1)), float(np.percentile(means, 99)))
        kept_sizes[wkey] = (int(ks.min()), int(ks.max()), int(ks.mean()))

    def star(fep, wkey, val):
        lo, hi = pct[wkey]
        return "*" if (fep <= 5 and val < lo) or (fep >= 6 and val > hi) else ""

    _RS = {1: ["1111", "1111", "1100"], 2: ["1111", "1111", "1100"], 3: ["1111", "1111", "1100"],
           4: ["1111", "1111", "1100"], 5: ["0010", "1011", "1000"], 6: ["0110", "1111", "1100"],
           7: ["1111", "1111", "1100"], 8: ["1111", "1111", "1100"], 9: ["1111", "1111", "1100"],
           10: ["1111", "1111", "1100"]}
    PS = {(f, w, m): ch == "1" for f, bl in _RS.items()
          for w, bl2 in zip(("m1_0", "m60_0", "p1_60"), bl) for m, ch in enumerate(bl2, 1)}
    star_match = 0
    mism = []
    for (fep, wkey, m), ps in PS.items():
        ours = star(fep, wkey, car_cells[(m, fep, wkey)]) == "*"
        if ours == ps:
            star_match += 1
        else:
            mism.append((fep, wkey, m, car_cells[(m, fep, wkey)], ours, ps))

    lines = ["# Table 4 — Cumulative Average Residuals for Forecast Error Portfolios: All Observations Pooled",
             "", "CAR (percent) = mean per-observation CAR by (fep, model). Stars from the",
             "paper's TWO-STAGE empirical-distribution test (L1357-1363): 1,000 draws of 8,000",
             "(firm, quarter) pairs without replacement from the full frame (firms in panel x 32",
             "qlabels), keeping those present in the per-window availability pool; '*' iff observed",
             "CAR < p1 (FEP1-5) or > p99 (FEP6-10) of the kept-set mean distribution. seed=42.",
             "",
             f"Frame = {len(firms)} firms x 32 qlabels = {n_frame} pairs. Per-window kept-set size "
             + "; ".join(f"{w}: {kept_sizes[w][0]}-{kept_sizes[w][1]} (mean {kept_sizes[w][2]})" for w, _ in WINDOWS)
             + f". Percentiles (p1/p99): "
             + "; ".join(f"{w}: {pct[w][0]:.3f}/{pct[w][1]:.3f}" for w, _ in WINDOWS),
             "",
             "| FEP | " + " | ".join(f"{WIN_LABEL[w]} M{m}" for w, _ in WINDOWS for m in range(1, 5)) + " |",
             "|---|" + "---|" * 12]
    for jv in range(1, 11):
        row = [str(jv)]
        for wkey, _ in WINDOWS:
            for m in range(1, 5):
                v = car_cells[(m, jv, wkey)]
                row.append(f"{v:.2f}{star(jv, wkey, v)}")
        lines.append("| " + " | ".join(row) + " |")
    lines += ["", f"Star pattern agreement with the paper: {star_match}/{len(PS)}.", ""]
    if mism:
        lines.append("Mismatches (FEP, window, model, our CAR, our star, paper star):")
        for mm in mism:
            lines.append(f"- FEP{mm[0]} {mm[1]} M{mm[2]}: {mm[3]:.2f} ours={'*' if mm[4] else '-'} paper={'*' if mm[5] else '-'}")
    Path(LAYOUT.result_path("table_4.md")).write_text("\n".join(lines) + "\n")
    print(f"[{time.time() - t0:5.1f}s] Table 4 written (two-stage; stars {star_match}/{len(PS)})")

    # (cells_iter2.csv + Tier tally emitted below, after Tasks A-C, over all 1,188 cells)

    # =========================================================================
    # Plots (unchanged from iteration 2)
    # =========================================================================
    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(1, 11); width = 0.26
    cols = {"m1_0": "#8c8c8c", "m60_0": "#4878a8", "p1_60": "#d05050"}
    for i, (wkey, _) in enumerate(WINDOWS):
        ax.bar(x + (i - 1) * width, [car_cells[(2, j, wkey)] for j in range(1, 11)],
               width, label=WIN_LABEL[wkey], color=cols[wkey])
    ax.axhline(0.0, color="black", linewidth=0.7); ax.set_xticks(x)
    ax.set_xlabel("Forecast Error Portfolio (Model 2)"); ax.set_ylabel("Cumulative average residual (%)")
    ax.legend(title="Event window"); fig.tight_layout()
    fig.savefig(LAYOUT.result_path("drift_bars_m2.png"), dpi=150); plt.close(fig)

    pmap = panel.loc[panel["fep2"].isin([1.0, 10.0]), ["obs_id", "fep2"]]
    er = pd.read_parquet(LAYOUT.data_path("cache/event_returns.parquet"),
                         columns=["obs_id", "event_day", "u"],
                         filters=[("event_day", ">=", -60), ("event_day", "<=", 60)])
    er = er.merge(pmap, on="obs_id", how="inner")
    daily = (er.groupby(["fep2", "event_day"])["u"].mean() * 100.0).reset_index()
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for fep, color, lbl in ((1.0, "#4878a8", "FEP1 (most negative FE)"),
                            (10.0, "#d05050", "FEP10 (most positive FE)")):
        d = daily[daily["fep2"] == fep].sort_values("event_day")
        ax.plot(d["event_day"], d["u"].cumsum(), color=color, label=lbl, linewidth=1.6)
    ax.axvline(0, color="black", linewidth=0.7, linestyle="--"); ax.axhline(0, color="black", linewidth=0.5)
    ax.set_xlabel("Event time (trading days)"); ax.set_ylabel("Cumulative average residual, sum from -60 (%)")
    ax.legend(); fig.tight_layout(); fig.savefig(LAYOUT.result_path("event_car_m2.png"), dpi=150); plt.close(fig)

    qtr = (panel[panel["fep2"].isin([1.0, 10.0])].groupby(["fep2", "qlabel"])["car_p1_60"].mean() * 100.0).reset_index()
    qlabels = sorted(panel["qlabel"].unique())
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for fep, color, lbl in ((1.0, "#4878a8", "FEP1"), (10.0, "#d05050", "FEP10")):
        d = qtr[qtr["fep2"] == fep].sort_values("qlabel")
        ax.plot(range(len(d)), d["car_p1_60"], marker="o", markersize=3.5, color=color, label=lbl, linewidth=1.4)
    ax.set_xticks(range(0, len(qlabels), 4)); ax.set_xticklabels([str(q) for q in qlabels[::4]], rotation=45)
    ax.axhline(0, color="black", linewidth=0.5); ax.set_xlabel("Announcement quarter (qlabel)")
    ax.set_ylabel("CAR [+1, +60] (%)"); ax.legend(); fig.tight_layout()
    fig.savefig(LAYOUT.result_path("quarterly_car_m2.png"), dpi=150); plt.close(fig)
    print(f"[{time.time() - t0:5.1f}s] plots written")

    # =========================================================================
    # Tasks A-C: Tables 5, 8, 9 (extend comp/comp2; FE/sigma/alignment UNTOUCHED)
    # =========================================================================
    NEW_T = {"T5", "T8", "T9"}

    def cval(tid, nm):
        return comp2.get(nm, float("nan")) if tid in NEW_T else comp.get(nm, float("nan"))

    def hasv(tid, nm):
        return (nm in comp2) if tid in NEW_T else (nm in comp)

    # ---- Table 5: subperiod stability of quarterly CAR[+1,60] (panel only) ----
    def ql(y, q):
        return y * 10 + q
    SUB = {
        "s1": [ql(1974, q) for q in range(1, 5)] + [ql(1975, q) for q in range(1, 5)] + [ql(1976, 1), ql(1976, 2)],
        "s2": [ql(1976, 3), ql(1976, 4)] + [ql(1977, q) for q in range(1, 5)] + [ql(1978, q) for q in range(1, 5)],
        "s3": [ql(y, q) for y in (1979, 1980, 1981) for q in range(1, 5)],
    }
    qcar: dict[int, dict[tuple[int, int], float]] = {}
    for m in range(1, 5):
        g5 = panel[[f"fep{m}", "qlabel", "car_p1_60"]].dropna().astype({f"fep{m}": int, "qlabel": int})
        qcar[m] = {(int(f), int(qq)): float(v)
                   for (f, qq), v in (g5.groupby([f"fep{m}", "qlabel"])["car_p1_60"].mean() * 100.0).items()}
        for fep in range(1, 11):
            for sk, qls in SUB.items():
                comp2[f"m{m}_fep{fep}_{sk}"] = float(sum(1 for qq in qls if qcar[m].get((fep, qq), 0.0) < 0))
    lines = ["# Table 5 — Subperiod Stability: Quarters with Negative Quarterly CAR[+1,+60]",
             "", "Per (model, FEP, subperiod): number of quarters whose quarterly mean CAR[+1,+60]",
             "is negative. s1 = 1974Q1-1976Q2 (10q), s2 = 1976Q3-1978Q4 (10q), s3 = 1979Q1-1981Q4 (12q).",
             "Tolerance 100% (counts are vintage-sensitive; the PATTERN is the claim).", ""]
    for m in range(1, 5):
        lines += [f"## Model {m}", "",
                  "| FEP | s1 ours | s1 paper | s2 ours | s2 paper | s3 ours | s3 paper |",
                  "|---|---|---|---|---|---|---|"]
        for fep in range(1, 11):
            cells = []
            for sk in ("s1", "s2", "s3"):
                nm = f"m{m}_fep{fep}_{sk}"
                cells += [str(int(comp2[nm])), str(int(TARGETS[nm][1]))]
            lines.append("| " + str(fep) + " | " + " | ".join(cells) + " |")
        lines.append("")
    Path(LAYOUT.result_path("table_5.md")).write_text("\n".join(lines) + "\n")
    t5_sum = {}
    for m in range(1, 5):
        per = {}
        for sk, qls in SUB.items():
            half = len(qls) / 2.0
            lo5 = sum(1 for f in range(1, 6) if comp2[f"m{m}_fep{f}_{sk}"] >= half)
            hi10 = sum(1 for f in range(8, 11) if comp2[f"m{m}_fep{f}_{sk}"] <= 2)
            mean_all = float(np.mean([comp2[f"m{m}_fep{f}_{sk}"] for f in range(1, 11)]))
            per[sk] = (lo5, hi10, round(mean_all, 2))
        t5_sum[m] = per
    print(f"[{time.time() - t0:5.1f}s] Table 5 written")

    # ---- Table 8: market-adjusted (u_M = ret - ewretd) pooled CARs ----
    dsi8 = q_file("market_index.sql"); dsi8["date"] = pd.to_datetime(dsi8["date"])
    ew = dict(zip(dsi8["date"], dsi8["ewretd"]))
    er8 = pd.read_parquet(LAYOUT.data_path("cache/event_returns.parquet"),
                          columns=["obs_id", "event_day", "date", "ret"])
    er8["date"] = pd.to_datetime(er8["date"])
    er8["u_M"] = er8["ret"] - er8["date"].map(ew)  # NaN on pre-1973 days (no ewretd)
    ed = er8["event_day"].to_numpy(); uM = er8["u_M"].to_numpy(); notna = ~np.isnan(uM)
    er8 = er8.assign(
        m10=np.where((ed >= -1) & (ed <= 0), uM, np.nan),
        m600=np.where((ed >= -60) & (ed <= 0), uM, np.nan),
        p160=np.where((ed >= 1) & (ed <= 60), uM, np.nan),
        s3=np.where((ed >= -251) & (ed <= -2), uM, np.nan),
        s4=np.where((ed >= -311) & (ed <= -61), uM, np.nan),
        c3=((ed >= -251) & (ed <= -2) & notna).astype("int8"),
        c4=((ed >= -311) & (ed <= -61) & notna).astype("int8"))
    g8 = er8.groupby("obs_id", sort=False)
    sM = {w: g8[w].sum(min_count=1) for w in ("m10", "m600", "p160")}
    std3 = g8["s3"].std(ddof=1); n3 = g8["c3"].sum()
    std4 = g8["s4"].std(ddof=1); n4 = g8["c4"].sum()
    fe3M = (sM["m10"] / std3).where(n3 >= 100)
    fe4M = ((sM["m600"] / 61.0) / std4).where(n4 >= 100)
    oids = np.asarray(fe3M.index)
    _parts = [str(o).rsplit("_", 2) for o in oids]
    gv_m = np.array([p[0] for p in _parts])
    fy_m = np.array([int(p[1]) for p in _parts]); fq_m = np.array([int(p[2]) for p in _parts])
    obs_meta = pd.DataFrame({"obs_id": oids, "qidx": fy_m * 4 + fq_m, "qlabel": fy_m * 10 + fq_m,
                             "fe3M": fe3M.to_numpy(), "fe4M": fe4M.to_numpy()})
    del er8

    def assign_fep(fe_arr, qidx_arr, oid_arr):
        fep = np.full(len(fe_arr), np.nan)
        for cq in range(CUTOFF_Q0, CUTOFF_Q1 + 1):
            msk = (qidx_arr == cq) & ~np.isnan(fe_arr)
            if not msk.any():
                continue
            so = np.lexsort((oid_arr[msk], fe_arr[msk]))
            vals = fe_arr[msk][so]; n = len(vals)
            edges = np.array([vals[int(np.ceil(k * n / 10)) - 1] for k in range(1, 10)])
            tm = (qidx_arr == cq + 1) & ~np.isnan(fe_arr)
            if not tm.any():
                continue
            fep[tm] = np.clip(1 + np.sum(edges[None, :] < fe_arr[tm][:, None], axis=1), 1, 10).astype(float)
        return pd.Series(fep, index=pd.Index(oid_arr, name="obs_id"))

    fep3M = assign_fep(obs_meta["fe3M"].to_numpy(), obs_meta["qidx"].to_numpy(), oids)
    fep4M = assign_fep(obs_meta["fe4M"].to_numpy(), obs_meta["qidx"].to_numpy(), oids)
    p3 = panel["obs_id"].map(fep3M); p4 = panel["obs_id"].map(fep4M)
    cM = {w: panel["obs_id"].map(sM[w]) for w in ("m10", "m600", "p160")}
    fep_for = {1: panel["fep1"], 2: panel["fep2"], 3: p3, 4: p4}
    WINKEY = ["m1_0", "m60_0", "p1_60"]; COLM = ["m10", "m600", "p160"]
    for m in range(1, 5):
        fcol = fep_for[m]
        for wk, cm in zip(WINKEY, COLM):
            df8 = pd.DataFrame({"f": fcol, "c": cM[cm]}).dropna().astype({"f": int})
            mm8 = df8.groupby("f")["c"].mean() * 100.0
            for fep in range(1, 11):
                comp2[f"m{m}_fep{fep}_{wk}"] = float(mm8.get(fep, float("nan")))

    # two-stage empirical stars under u_M (model-independent per window; seed=42)
    rng8 = np.random.default_rng(42)
    firms8 = sorted(panel["gvkey"].astype(str).unique()); fi8 = {f: i for i, f in enumerate(firms8)}
    qi8 = {qq: j for j, qq in enumerate(QLABELS)}; nf8 = len(firms8) * len(QLABELS)
    gv8 = panel["gvkey"].astype(str).to_numpy(); ql8 = panel["qlabel"].astype(int).to_numpy()
    cf8 = {}
    for wk, cm in zip(WINKEY, COLM):
        arr = cM[cm].to_numpy(dtype=float) * 100.0
        cf = np.full(nf8, np.nan)
        for gi in range(len(panel)):
            f = gv8[gi]; qq = ql8[gi]
            if f in fi8 and qq in qi8 and not np.isnan(arr[gi]):
                cf[fi8[f] * len(QLABELS) + qi8[qq]] = arr[gi]
        cf8[wk] = cf
    pct8 = {}
    for wk in WINKEY:
        cf = cf8[wk]; means = np.empty(1000)
        for tt in range(1000):
            idx = rng8.choice(nf8, size=8000, replace=False); v = cf[idx]; v = v[~np.isnan(v)]
            means[tt] = v.mean() if v.size else np.nan
        pct8[wk] = (float(np.percentile(means, 1)), float(np.percentile(means, 99)))

    def star8(fep, wk, val):
        lo, hi = pct8[wk]
        return "*" if (fep <= 5 and val < lo) or (fep >= 6 and val > hi) else ""

    lines = ["# Table 8 — Market-Adjusted Pooled CARs (u_M = ret - ewretd, eq. 17)",
             "", "Abnormal return uses the CRSP EW NYSE+AMEX market index instead of the size decile.",
             "Models 1-2 use unchanged earnings-based FEPs; Models 3-4 recompute the FE AND the CAR",
             "from u_M and re-assign FEPs via prior-quarter decile cutoffs on fe3_M/fe4_M (paper",
             "footnote L3029; same >=100-day floors as A11). Stars: two-stage empirical test on u_M",
             "CARs (seed=42), one distribution per window pooled across models.",
             "", f"Frame = {len(firms8)} firms x 32 qlabels = {nf8}. Percentiles (p1/p99): "
             + "; ".join(f"{w}: {pct8[w][0]:.3f}/{pct8[w][1]:.3f}" for w in WINKEY),
             "", "| FEP | " + " | ".join(f"{WIN_LABEL[w]} M{m}" for w in WINKEY for m in range(1, 5)) + " |",
             "|---|" + "---|" * 12]
    for jv in range(1, 11):
        row = [str(jv)]
        for wk in WINKEY:
            for m in range(1, 5):
                v = comp2[f"m{m}_fep{jv}_{wk}"]
                row.append(f"{v:.2f}{star8(jv, wk, v)}")
        lines.append("| " + " | ".join(row) + " |")
    Path(LAYOUT.result_path("table_8.md")).write_text("\n".join(lines) + "\n")
    cache8 = obs_meta.copy()
    cache8["carM_m10"] = sM["m10"].reindex(oids).to_numpy()
    cache8["carM_m600"] = sM["m600"].reindex(oids).to_numpy()
    cache8["carM_p160"] = sM["p160"].reindex(oids).to_numpy()
    cache8["fep3M"] = fep3M.to_numpy(); cache8["fep4M"] = fep4M.to_numpy()
    cache8.to_parquet(LAYOUT.data_path("cache/market_adjusted.parquet"), index=False)
    print(f"[{time.time() - t0:5.1f}s] Table 8 written + cache/market_adjusted.parquet")

    # ---- Table 9: market-adjusted Model-2 quintile CARs ----
    for wk, cm in zip(WINKEY, COLM):
        df9 = pd.DataFrame({"f": panel["fep2"], "q": panel["quintile"], "c": cM[cm]}).dropna()
        df9 = df9.astype({"f": int, "q": int})
        mm9 = df9.groupby(["f", "q"])["c"].mean() * 100.0
        for fep in range(1, 11):
            for qv in range(1, 6):
                comp2[f"m2_fep{fep}_q{qv}_{wk}"] = float(mm9.get((fep, qv), float("nan")))
    qV = {wk: [comp2.get(f"m2_fep{f}_q5_{wk}", float("nan")) for f in range(1, 11)] for wk in WINKEY}
    lines = ["# Table 9 — Market-Adjusted Model-2 CARs by FEP x NYSE Size Quintile",
             "", "CAR (percent) from u_M = ret - ewretd, grouped by (panel FEP2, quintile). Quintile V",
             "= largest firms. Paper point (L3027): quintile V shows NEGATIVE CARs across all ten FEPs",
             "in [-60,0] and [+1,+60] (the size effect swamps the earnings effect when the benchmark",
             "does not control for size).", ""]
    for wk in WINKEY:
        lines += [f"## Window {WIN_LABEL[wk]}", "", "| FEP | Q I | Q II | Q III | Q IV | Q V |",
                  "|---|---|---|---|---|---|"]
        for fep in range(1, 11):
            vals = [comp2.get(f"m2_fep{fep}_q{qv}_{wk}", float("nan")) for qv in range(1, 6)]
            lines.append("| " + str(fep) + " | " + " | ".join(f"{v:.2f}" for v in vals) + " |")
        lines.append("")
    Path(LAYOUT.result_path("table_9.md")).write_text("\n".join(lines) + "\n")
    print(f"[{time.time() - t0:5.1f}s] Table 9 written")

    # =========================================================================
    # cells_iter2.csv (1,188 rows, ALL_TARGETS order) + Tier tally over all tables
    # =========================================================================
    missing = [(tid, nm) for (tid, nm, _, _) in ALL_TARGETS if not hasv(tid, nm)]
    assert not missing, f"computed missing registry names: {missing[:10]}"
    rows = [(tid, nm, cval(tid, nm)) for (tid, nm, _, _) in ALL_TARGETS]
    pd.DataFrame(rows, columns=["table_id", "metric_name", "value"]).to_csv(
        LAYOUT.result_path("cells_iter2.csv"), index=False)
    tally = {t: {"T1": 0, "T2": 0, "FAIL": 0, "SKIP": 0} for t in _HANDLED}
    fails = []
    for (tid, nm, pv, tol) in ALL_TARGETS:
        v = cval(tid, nm)
        tr = "SKIP" if not np.isfinite(v) else tier(v, pv, tol)
        tally[tid][tr] += 1
        if tr == "FAIL":
            fails.append((tid, nm, pv, v))
    total = {k: sum(tally[t][k] for t in tally) for k in ("T1", "T2", "FAIL", "SKIP")}
    print(f"[{time.time() - t0:5.1f}s] cells_iter2.csv — {len(rows)} rows; total "
          f"T1={total['T1']} T2={total['T2']} FAIL={total['FAIL']} SKIP={total['SKIP']}")

    # =========================================================================
    # Report
    # =========================================================================
    print("\n" + "=" * 92)
    print("ITERATION 4 REPORT — Tables 1,3,4,5,6,7,8,9 (1,188 cells)")
    print("=" * 92)
    print("\nTable 3 anchor (SW/Dimson row) ours vs paper:")
    print(f"  {'dec':>4} {'SW ours':>8} {'paper':>7}")
    for dec in (1, 10):
        print(f"  {dec:>4} {comp[f'd{dec}_beta_sw']:>8.2f} {TARGETS[f'd{dec}_beta_sw'][1]:>7.2f}")
    print("\nTable 6 anchor — M2 quintile-I column & M4 P1 [-60,0]:")
    print("  M2 q1 [-1,0]   ours:", [round(t6_car.get((2, f, 1, 'm1_0'), float('nan')), 2) for f in range(1, 11)])
    print("                    paper: [-1.83,-1.07,-0.50,-0.09,0.38,0.81,1.36,1.41,1.91,2.58]")
    print("  M2 q1 [+1,+60] ours:", [round(t6_car.get((2, f, 1, 'p1_60'), float('nan')), 2) for f in range(1, 11)])
    print("                    paper: [-3.34,-4.10,-1.98,-0.97,1.45,1.82,2.34,3.60,3.51,5.00]")
    print(f"  M4 FEP1 q1 [-60,0] ours: {t6_car.get((4,1,1,'m60_0'), float('nan')):.2f}  paper: -28.68")
    print("\nTable 7 anchor — Model 2 all three windows (FEP-only / FSQ-only / Both):")
    for wkey in ("m1_0", "m60_0", "p1_60"):
        s = t7[(2, wkey)]
        print(f"  M2 {WIN_LABEL[wkey]}: FEP a={s['fep']['alpha']:.2f} t={s['fep']['t_alpha']:.2f} "
              f"b1={s['fep']['b1']:.2f} t={s['fep']['t_b1']:.2f} R2={s['fep']['adj_r2']:.3f} | "
              f"FSQ a={s['fsq']['alpha']:.2f} t={s['fsq']['t_alpha']:.2f} b2={s['fsq']['b2']:.2f} "
              f"t={s['fsq']['t_b2']:.2f} R2={s['fsq']['adj_r2']:.3f} | "
              f"BOTH a={s['both']['alpha']:.2f} b1={s['both']['b1']:.2f} b2={s['both']['b2']:.2f} "
              f"R2={s['both']['adj_r2']:.3f}")
    print("   paper M2 [+1,60]: FEP a=-3.62 t=-12.65 b1=0.67 t=14.48 R2=0.810 | FSQ a=3.38 t=8.85 "
          "b2=-0.60 t=-9.83 R2=0.661 | BOTH a=-1.37 b1=0.49 b2=-0.23 R2=0.850")
    print("  M3/M4 [+1,+60] adj R2 (FEP-only):",
          {m: round(t7[(m, 'p1_60')]['fep']['adj_r2'], 3) for m in (3, 4)}, "(paper ~0)")
    print("\nTable 5 anchor — M2 FEP1/FEP10 & M3 FEP1 counts [s1,s2,s3] ours vs paper:")
    for m, feps in ((2, (1, 10)), (3, (1,))):
        for fep in feps:
            o = [int(comp2[f"m{m}_fep{fep}_{s}"]) for s in ("s1", "s2", "s3")]
            p = [int(TARGETS[f"m{m}_fep{fep}_{s}"][1]) for s in ("s1", "s2", "s3")]
            print(f"  M{m} FEP{fep}: ours={o} paper={p}")
    print("  T5 pattern (per subperiod: FEP1-5 with >=half-negative / FEP8-10 with <=2 / mean count):")
    for m in range(1, 5):
        print(f"   M{m}:", {s: t5_sum[m][s] for s in ("s1", "s2", "s3")})
    print("\nTable 8 anchor — ours vs paper (windows [m1_0, m60_0, p1_60]):")
    for m, fep, pap in ((1, 10, [1.48, 6.72, 3.78]), (2, 1, [-1.36, -6.75, -3.46]),
                        (4, 10, [1.75, 28.72, -1.09])):
        o = [round(comp2[f"m{m}_fep{fep}_{w}"], 2) for w in WINKEY]
        print(f"  M{m} FEP{fep}: ours={o} paper={pap}")
    print("\nTable 9 anchor — ours vs paper:")
    print("  FEP1 q1 :", [round(comp2.get(f"m2_fep1_q1_{w}", float('nan')), 2) for w in WINKEY],
          " paper=[-1.78,-5.51,-2.10]")
    print("  FEP10 q5:", [round(comp2.get(f"m2_fep10_q5_{w}", float('nan')), 2) for w in WINKEY],
          " paper=[0.39,-1.98,-0.78]")
    print("  Quintile-V sign pattern (paper L3027: V negative across all FEPs in [-60,0]&[+1,+60]):")
    for wk in ("m60_0", "p1_60"):
        nneg = sum(1 for v in qV[wk] if v < 0)
        print(f"    {WIN_LABEL[wk]}: {nneg}/10 FEPs negative; values="
              + str([round(v, 2) for v in qV[wk]]))

    print("\nTier tally per table (registry 1,188 cells):")
    for tid in ("T1", "T3", "T4", "T5", "T6", "T7", "T8", "T9"):
        tt = tally[tid]
        print(f"  {tid}: T1={tt['T1']} T2={tt['T2']} FAIL={tt['FAIL']} SKIP={tt['SKIP']}")
    print(f"  TOTAL: T1={total['T1']} T2={total['T2']} FAIL={total['FAIL']} SKIP={total['SKIP']}")
    if fails:
        print(f"\nFAIL cells ({len(fails)}):")
        for tid, nm, p, o in fails[:150]:
            print(f"  {tid} {nm}: paper={p:.3f} ours={o:.3f}")
    print(f"\nT4 two-stage star pattern: {star_match}/{len(PS)} vs paper "
          f"(was 109/120 with one-stage).")
    print(f"Total runtime: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
