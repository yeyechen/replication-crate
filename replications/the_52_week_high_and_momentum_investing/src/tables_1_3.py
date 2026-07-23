"""
George & Hwang (2004), "The 52-Week High and Momentum Investing", JF —
Tables I, II, III.

Reads data/panel.parquet (built by src/main.py). The panel builder and the
table code are deliberately separable: editing this file does NOT rebuild
the panel.

Machinery (paper §II; footnote 3 — no skip month for Tables I-IV; footnote 6
— nonempty-cell rule for Table III W-L rows):
  - EW 30/30 winner/loser portfolios; (6,6) strategies; overlapping 6-month
    holding.
  - Formation month f: cross-section = universe rows at f with the signal
    non-null. Sort by (signal ascending, permno ascending) — deterministic
    tie-break. Losers = first int(0.3*n) rows, winners = last int(0.3*n).
  - A portfolio formed in f is HELD in months f+1 .. f+6. Cohort return at
    holding month t = EW mean of ret(t) over cohort members with non-null
    ret(t) (members without a panel row at t drop out).
  - Month-t strategy series value = mean of the 6 cohort returns for
    f ∈ {t-6 .. t-1} (paper L120), averaging only cohorts that exist
    (nanmean). Holding months: 1963-07-31 .. 2001-12-31 (462) => formation
    months 1963-01-31 .. 2001-11-30 (467). [Note: the task's "formation
    months needed: .. 2001-06-30" line is inconsistent with the stated
    t-6..t-1 convention, which requires formations through 2001-11-30 for
    the last holding month; the convention itself is implemented exactly.]
  - All returns reported in PERCENT (x100). t-stat of W-L =
    mean(WL series) / (std(WL series, ddof=1) / sqrt(T)).
  - Table II: Panel A = holding months with month-of-year != 1; Panel B =
    month-of-year == 1 (split on the calendar month of t).
  - Table III: independent 30/40/30 sorts on jt_sig (outer Panel A) and
    wh_sig_cl (inner Panel A); 3x3 intersection cells; W-L row = average
    over months where BOTH cells are non-missing; W-L row is NOT the
    difference of the two reported cell rows (paper, explicitly).

52WH adjudication: Table I's 52WH row is computed under the PRIMARY signal
(wh_sig_cl) and under the VARIANT wh_sig_hi_abs (|prc|/max(|askhi|), added
to the panel by main.py). Both are reported; the closer fit to the paper is
flagged for the Replicator to lock.

Outputs:
  - results/intermediate/strategy_returns.parquet  (462 rows, percent; wh_* = PRIMARY;
                                                    relocated out of data/ by audit1.md [M6])
  - results/table_1.md, results/table_2.md, results/table_3.md
"""
from __future__ import annotations

import json
import warnings

import numpy as np
import pandas as pd

from utils.paths import paper_layout

LAYOUT = paper_layout("the_52_week_high_and_momentum_investing")


def intermediate_path(name: str):
    """Relocated derived caches (audit1.md [M6]): the 8 non-allowlisted
    fm_coefficients*/strategy_returns parquets live under results/intermediate/
    (results/ is validator-clean) instead of data/ (closed parquet allowlist).
    One-line auditable relocation — every cache read/write routes through here.
    (Local copy, not imported from tables_5: tables_5 imports this module, so
    importing it back would be circular. Resolves to the same results/ dir.)"""
    d = LAYOUT.result_path("intermediate")
    d.mkdir(parents=True, exist_ok=True)
    return d / name


HOLD_START = pd.Timestamp("1963-07-31")
HOLD_END = pd.Timestamp("2001-12-31")
FORM_START = pd.Timestamp("1963-01-31")   # HOLD_START minus 6 months
FORM_END = pd.Timestamp("2001-11-30")     # HOLD_END minus 1 month (t-1 cohort)
FRAC = 0.30
J = 6  # formation lag / holding length of the (6,6) strategy

# PRIMARY 52WH signal. Locked to wh_sig_dc (max of DSF daily closes) after the
# granularity diagnostic (src/tables_dc_vs_cl.py -> results/table_3_dc_vs_cl.md):
# over the 48 Table III cells + 4 Table I 52WH metrics, dc lowers total
# |deviation| from paper by 6.02 vs wh_sig_cl (26.41 -> 20.39, -22.8%) and lifts
# Table III Tier-1 count 27 -> 30. The literal "highest price achieved during
# the 12-month period" reading of L122. wh_sig_cl is retained in the panel for
# reference; wh_sig_hi_abs remains the VARIANT for the Table I adjudication.
PRIMARY_WH = "wh_sig_dc"
VARIANT_WH = "wh_sig_hi_abs"

TOL = 1e-12


# --- targets -----------------------------------------------------------------

def load_targets() -> dict:
    tabs = json.loads(
        LAYOUT.preparations_path("tables_to_replicate.json").read_text()
    )["tables"]
    out = {}
    for t in tabs:
        out[t["id"]] = {
            m["name"]: (float(m["value"]), float(m["tolerance_pct"]))
            for m in t["metrics"]
        }
    return out


# --- data matrices -------------------------------------------------------------

def load_matrices(ret_col: str = "ret"):
    """Panel -> (grid month array, permno array, ret matrix [months x permnos]).
    ret_col selects the HOLDING-PERIOD return used for portfolio DEPENDENT
    variables: "ret" (original msf) or "ret_dl" (delisting-adjusted; NaN rows
    drop out of the EW means like any missing month, added delisting rows
    contribute dlret). NaN where the panel has no row or a null value."""
    assert ret_col in ("ret", "ret_dl"), f"unknown return column {ret_col}"
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    grid = pd.date_range(panel["month"].min(), panel["month"].max(), freq="ME")
    uniq = np.sort(panel["month"].unique())
    assert (grid.to_numpy() == uniq).all(), "panel months are not a clean grid"
    permnos = np.sort(panel["permno"].unique())
    mi = np.searchsorted(grid.to_numpy(), panel["month"].to_numpy())
    pi = np.searchsorted(permnos, panel["permno"].to_numpy())
    r = panel[ret_col].to_numpy(dtype="float64")
    ret_mat = np.full((len(grid), len(permnos)), np.nan)
    ok = np.isfinite(r)
    ret_mat[mi[ok], pi[ok]] = r[ok]
    return panel, grid.to_numpy(), permnos, ret_mat


def formation_rows(panel: pd.DataFrame, sig_col: str):
    """Rows in the formation window with a finite signal: (month_grid_idx
    input arrays) -> (months, permnos, sigs) numpy arrays."""
    sub = panel[["month", "permno", sig_col]]
    sub = sub[(sub["month"] >= FORM_START) & (sub["month"] <= FORM_END)]
    s = sub[sig_col].to_numpy(dtype="float64")
    keep = np.isfinite(s)
    return (
        sub["month"].to_numpy()[keep],
        sub["permno"].to_numpy()[keep],
        s[keep],
    )


# --- ranking -------------------------------------------------------------------

def split_30_30(sig: np.ndarray, permno: np.ndarray) -> dict:
    """One formation cross-section -> {"W","M","L"} permno arrays.
    Sort by (signal asc, permno asc); losers = first int(0.3n), winners =
    last int(0.3n), middle = remainder."""
    n = sig.size
    k = int(FRAC * n)
    order = np.lexsort((permno, sig))  # primary key = sig (last), ascending
    g = np.full(n, "M", dtype="U1")
    g[order[:k]] = "L"
    if k > 0:
        g[order[n - k:]] = "W"
    return {
        "W": permno[g == "W"],
        "M": permno[g == "M"],
        "L": permno[g == "L"],
    }


def build_cohorts(months, permnos, sigs, grid) -> tuple[dict, dict]:
    """{grid_idx: {"W","M","L"} permno arrays}, {grid_idx: n} over formation
    months present in the data."""
    mi = np.searchsorted(grid, months)
    order = np.argsort(mi, kind="stable")
    mi, p, s = mi[order], permnos[order], sigs[order]
    bounds = np.concatenate([[0], np.flatnonzero(np.diff(mi)) + 1, [len(mi)]])
    cohorts: dict[int, dict] = {}
    ns: dict[int, int] = {}
    for a, b in zip(bounds[:-1], bounds[1:]):
        g = split_30_30(s[a:b], p[a:b])
        cohorts[int(mi[a])] = g
        ns[int(mi[a])] = b - a
    return cohorts, ns


# --- industry-level MG cutoff variant (audit1.md [M5]) -------------------------

def industry_cum_returns(panel: pd.DataFrame, grid) -> tuple[np.ndarray, np.ndarray]:
    """Recompute the monthly VW industry returns from the panel and roll them
    into 6-month cumulative returns — the ranking input of the industry-level
    MG variant (audit1.md [M5]).

    Formula identical to src/main.py's pipeline (A7): ind_ret(k, m) =
    sum(ret_i,m * mcap_{i,m-1}) / sum(mcap_{i,m-1}) over rows with
    industry == k, non-missing ret and positive lagged mcap; cumulative =
    prod(1 + ind_ret) over f-5..f requiring all 6 months (same log-sum roll
    as the jt/mg signals, A5). The variant is an independent recompute on
    panel rows; note it is per-industry membership per month, so it differs
    from the official per-stock mg_sig ONLY for the small set of stocks that
    switch MG industry inside the 6-month window (plus last-bit edge
    effects) — immaterial to the ranking of the 20 industries.

    Returns (ind_cum, ind_w): ind_cum shape (21, n_months) with rows 1..20
    defined; ind_w shape (n_permnos, n_months) = the wide industry matrix on
    the panel's sorted permno order."""
    permnos = np.sort(panel["permno"].unique())
    grid = np.asarray(grid)
    M, P = len(grid), len(permnos)
    mi = np.searchsorted(grid, panel["month"].to_numpy())
    pi = np.searchsorted(permnos, panel["permno"].to_numpy())

    def _wide(col: str) -> np.ndarray:
        w = np.full((P, M), np.nan)
        w[pi, mi] = panel[col].to_numpy(dtype="float64")
        return w

    ret_w = _wide("ret")
    mcap_w = _wide("mcap")
    ind_w = _wide("industry")
    mcap_lag = np.full_like(mcap_w, np.nan)
    mcap_lag[:, 1:] = mcap_w[:, :-1]
    valid = (np.isfinite(ret_w) & np.isfinite(mcap_lag) & (mcap_lag > 0)
             & np.isfinite(ind_w))
    ind_ret = np.full((21, M), np.nan)
    for k in range(1, 21):
        mask = valid & (ind_w == k)
        den = np.where(mask, mcap_lag, 0.0).sum(axis=0)
        num = np.where(mask, ret_w * mcap_lag, 0.0).sum(axis=0)
        np.divide(num, den, out=ind_ret[k], where=den > 0)
    with np.errstate(divide="ignore", invalid="ignore"):
        lt = np.log1p(ind_ret)
    cum = pd.DataFrame(lt).T.rolling(6, min_periods=6).sum().T.values
    return np.exp(cum) - 1.0, ind_w


def industry_rank_groups(ind_values: np.ndarray, n_top: int = 6, n_bot: int = 6):
    """Rank the 20 MG industries by their 6-month cumulative VW return
    (audit1.md [M5] variant): winner industries = top `n_top`, loser
    industries = bottom `n_bot` (the MG-intended reading, as opposed to the
    official A8 ordinal split of individual stocks, which arbitrarily divides
    the boundary industry's stocks).

    `ind_values`: length-21 array, rows 1..20 = industry cumrets (NaN =
    undefined that month). Deterministic tie-break (value desc, industry id
    asc); boundary ties keep ALL members of the tied industries (inclusive
    cutoffs): n_tie_w / n_tie_l count the extra tied industries beyond
    n_top / n_bot (0 = no boundary tie).

    Returns (win_ids, lose_ids, n_industries, n_tie_w, n_tie_l);
    (None, None, n, 0, 0) when fewer than n_top + n_bot industries are
    defined (no winner/loser that month)."""
    v = np.asarray(ind_values, dtype="float64").copy()
    v[0] = np.nan
    ids = np.arange(21)
    fin = np.isfinite(v)
    n_ind = int(fin.sum())
    if n_ind < n_top + n_bot:
        return None, None, n_ind, 0, 0
    f_ids, f_vals = ids[fin], v[fin]
    order = np.lexsort((f_ids, -f_vals))       # value desc, then id asc
    ranked = f_vals[order]
    t_w, t_l = ranked[n_top - 1], ranked[n_ind - n_bot]
    if not (t_l < t_w):                        # degenerate mass tie: fall
        win = f_ids[order[:n_top]]             # back to the deterministic
        lose = f_ids[order[n_ind - n_bot:]]    # industry-ordinal split
        return win, lose, n_ind, 0, 0
    win_ids = f_ids[f_vals >= t_w]
    lose_ids = f_ids[f_vals <= t_l]
    return (win_ids, lose_ids, n_ind,
            int(len(win_ids) - n_top), int(len(lose_ids) - n_bot))


def build_cohorts_industry(panel: pd.DataFrame, grid, ind_cum: np.ndarray,
                           ind_w: np.ndarray, permnos_all: np.ndarray,
                           n_top: int = 6, n_bot: int = 6) -> tuple[dict, list]:
    """Industry-level MG cohorts over FORM_START..FORM_END (Table I window):
    {grid_idx: {"W","M","L"} permno arrays} + per-formation tie diagnostics
    [(grid_idx, n_industries, n_tie_w, n_tie_l)]. At each formation f the 20
    industries are ranked by ind_cum(:, f); winner stocks = members of the
    top-`n_top` industries AT f, loser = members of the bottom-`n_bot`.
    Rankable = industry(f) defined AND that industry's cumret finite."""
    grid = np.asarray(grid)
    f_lo = int(np.searchsorted(grid, FORM_START.to_datetime64()))
    f_hi = int(np.searchsorted(grid, FORM_END.to_datetime64()))
    cohorts: dict[int, dict] = {}
    diag: list[tuple] = []
    for f in range(f_lo, f_hi + 1):
        win, lose, n_ind, tw, tl = industry_rank_groups(ind_cum[:, f],
                                                        n_top, n_bot)
        diag.append((f, n_ind, tw, tl))
        if win is None:
            continue
        inds = ind_w[:, f]
        rankable = np.isfinite(inds)
        is_w = rankable & np.isin(inds, win)
        is_l = rankable & np.isin(inds, lose)
        cohorts[f] = {"W": permnos_all[is_w],
                      "M": permnos_all[rankable & ~is_w & ~is_l],
                      "L": permnos_all[is_l]}
    return cohorts, diag


# --- cohort returns --------------------------------------------------------------

def cohort_matrix(groups_by_idx: dict, group: str, f0: int, n_f: int,
                  permnos_all: np.ndarray, ret_mat: np.ndarray) -> np.ndarray:
    """C[k, j] = EW return of cohort formed at grid index f0+k, held in its
    (j+1)-th holding month. NaN when the group is empty or no member has a
    return that month."""
    C = np.full((n_f, J), np.nan)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        for k in range(n_f):
            members = groups_by_idx.get(f0 + k, {}).get(group)
            if members is None or members.size == 0:
                continue
            pos = np.searchsorted(permnos_all, members)
            sub = ret_mat[f0 + k + 1: f0 + k + 1 + J][:, pos]
            C[k] = np.nanmean(sub, axis=1)
    return C


def assemble_series(C: np.ndarray, hold0: int, f0: int, n_hold: int):
    """Month-t series value = mean over cohorts f ∈ {t-6..t-1} of C.
    Returns (series in DECIMAL, n_available_cohorts per t)."""
    cols = []
    for j in range(J):
        k0 = hold0 - f0 - 1 - j          # cohort row for the (t-j-1)-lagged f
        assert 0 <= k0 and k0 + n_hold <= C.shape[0], (
            f"cohort coverage gap: j={j} k0={k0} n_f={C.shape[0]} n_hold={n_hold}")
        cols.append(C[k0: k0 + n_hold, j])
    M = np.column_stack(cols)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        s = np.nanmean(M, axis=1)
    s[np.isfinite(M).sum(axis=1) == 0] = np.nan
    return s, np.isfinite(M).sum(axis=1)


def strategy_pair(cohorts: dict, f0: int, n_f: int, hold0: int, n_hold: int,
                  permnos_all: np.ndarray, ret_mat: np.ndarray):
    Cw = cohort_matrix(cohorts, "W", f0, n_f, permnos_all, ret_mat)
    Cl = cohort_matrix(cohorts, "L", f0, n_f, permnos_all, ret_mat)
    w, nw = assemble_series(Cw, hold0, f0, n_hold)
    l, nl = assemble_series(Cl, hold0, f0, n_hold)
    return {"w": w, "l": l, "wl": w - l, "n_w": nw, "n_l": nl}


# --- Table III cells ----------------------------------------------------------------

def intersection_cells(jt_coh: dict, wh_coh: dict, f_indices) -> dict:
    """{(jt_group, wh_group): {grid_idx: permno array}} over the 3x3 grid."""
    cells: dict[tuple, dict] = {(a, b): {} for a in "WML" for b in "WML"}
    for idx in f_indices:
        jg = jt_coh.get(idx)
        wg = wh_coh.get(idx)
        if jg is None or wg is None:
            continue
        wh_sets = {g: set(arr.tolist()) for g, arr in wg.items()}
        for a, arr in jg.items():
            for b, ws in wh_sets.items():
                inter = np.fromiter((p for p in arr if p in ws), dtype=np.int64)
                if inter.size:
                    cells[(a, b)][idx] = inter
    return cells


def cell_series(cell_members: dict, f0: int, n_f: int, hold0: int,
                n_hold: int, permnos_all: np.ndarray, ret_mat: np.ndarray):
    """Per-month cell value = mean over cohorts f ∈ {t-6..t-1} that are
    non-empty (and have a member with a return at t)."""
    C = np.full((n_f, J), np.nan)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        for idx, members in cell_members.items():
            k = idx - f0
            pos = np.searchsorted(permnos_all, members)
            sub = ret_mat[idx + 1: idx + 1 + J][:, pos]
            C[k] = np.nanmean(sub, axis=1)
    s, n = assemble_series(C, hold0, f0, n_hold)
    return s, n


# --- statistics / tiers ---------------------------------------------------------------

def tstat(x: np.ndarray) -> float:
    x = x[np.isfinite(x)]
    if x.size < 2:
        return np.nan
    sd = x.std(ddof=1)
    if sd == 0:
        return np.nan
    return float(x.mean() / (sd / np.sqrt(x.size)))


def mean_pct(x: np.ndarray, mask: np.ndarray) -> float:
    v = x[mask]
    v = v[np.isfinite(v)]
    return float(v.mean() * 100) if v.size else np.nan


def tier(paper: float, ours: float, tol_pct: float) -> str:
    if not np.isfinite(ours):
        return "FAIL"
    if abs(ours - paper) <= abs(paper) * tol_pct / 100.0 + TOL:
        return "Tier 1"
    if paper == 0 or (paper > 0) == (ours > 0):
        return "Tier 2"
    return "FAIL"


TIER2_WARN = "Tier 2 ⚠"


def tier_display(paper: float, ours: float, tol_pct: float) -> str:
    """Tier-COLUMN render string (audit1.md m2). Tier-2 cells whose magnitude
    is far off (|ours/paper| > 2; paper == 0 with a non-zero ours counts as an
    infinite ratio) are flagged 'Tier 2 ⚠'. The underlying tier assignment and
    the hit-rate tally are UNCHANGED — only the displayed tier-column string
    differs (a sign match can still hide a >2x magnitude gap)."""
    tr = tier(paper, ours, tol_pct)
    if tr == "Tier 2" and (paper == 0 or abs(ours / paper) > 2):
        return TIER2_WARN
    return tr


# One-line legend printed under each table's hit-rate summary (audit1.md m2).
TIER2_LEGEND = (
    "Tier 2 ⚠ = sign matches but |ours/paper| > 2 (magnitude far off; see "
    "audit1.md spot-check 10). FAIL cells with |paper| < 0.05 are "
    "rounding-boundary artifacts unless noted."
)


def fmt(x, nd=4) -> str:
    return f"{x:.{nd}f}" if np.isfinite(x) else "NaN"


def dev_pct(paper: float, ours: float) -> str:
    if paper == 0 or not np.isfinite(ours):
        return "n/a"
    return f"{(ours - paper) / abs(paper) * 100:+.1f}%"


def md_metric_table(rows: list[dict]) -> tuple[list[str], dict]:
    """rows: [{name, paper, ours, tol}]. Returns (markdown lines, counts)."""
    L = ["| cell name | paper value | our value | deviation pp | deviation % | tier |",
         "|---|---:|---:|---:|---:|---|"]
    counts = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0}
    for r in rows:
        t = tier(r["paper"], r["ours"], r["tol"])
        counts[t] += 1
        L.append(
            f"| {r['name']} | {fmt(r['paper'])} | {fmt(r['ours'])} | "
            f"{r['ours'] - r['paper']:+.4f} | {dev_pct(r['paper'], r['ours'])} "
            f"| {tier_display(r['paper'], r['ours'], r['tol'])} |"
        )
    total = len(rows)
    L.append("")
    L.append(f"**Hit rate: {counts['Tier 1']} Tier 1 / {counts['Tier 2']} Tier 2 / "
             f"{counts['FAIL']} FAIL out of {total}**")
    L.append("")
    L.append(f"_{TIER2_LEGEND}_")
    return L, counts


# --- main -------------------------------------------------------------------------------

def run(ret_col: str = "ret_dl", write_outputs: bool = True,
        verbose: bool = True) -> dict:
    """Full Tables I/II/III pipeline on holding-period return column `ret_col`
    ("ret" = original msf, "ret_dl" = delisting-adjusted). DEFAULT `ret_dl` =
    the OFFICIAL holding-period return adopted by the delisting experiment
    (results/delisting_experiment.md: +6 Tier-1 cells), so `python tables_1_3.py`
    reproduces the official artifacts bit-exactly. Ranking signals are ALWAYS
    the original panel signals (delisting adjustment touches dependent variables
    only). Writes results/intermediate/strategy_returns.parquet +
    results/table_1/2/3.md when write_outputs, prints the console report when
    verbose, and returns the bundle (rows/counts/series) for the delisting
    experiment driver."""
    targets = load_targets()
    t1, t2, t3 = targets["T1"], targets["T2"], targets["T3"]

    panel, grid, permnos, ret_mat = load_matrices(ret_col)
    f0 = int(np.searchsorted(grid, FORM_START.to_datetime64()))
    hold0 = int(np.searchsorted(grid, HOLD_START.to_datetime64()))
    hold_end_i = int(np.searchsorted(grid, HOLD_END.to_datetime64()))
    n_hold = hold_end_i - hold0 + 1
    n_f = n_hold + J - 1  # formation months t-6..t-1 span: 462 + 5 = 467
    assert grid[f0] == np.datetime64(FORM_START) and \
        grid[hold0] == np.datetime64(HOLD_START) and \
        grid[hold_end_i] == np.datetime64(HOLD_END)
    assert n_hold == 462, f"expected 462 holding months, got {n_hold}"
    assert n_f == 467, f"expected 467 formation months, got {n_f}"

    hold_months = pd.DatetimeIndex(grid[hold0: hold_end_i + 1])
    mo = hold_months.month.to_numpy()
    mask_all = np.ones(n_hold, dtype=bool)
    mask_exjan = mo != 1
    mask_jan = mo == 1
    n_jan = int(mask_jan.sum())

    # ---- cohorts for the four signals -------------------------------------
    cohort_sets: dict[str, tuple] = {}
    uni_stats: dict[str, dict] = {}
    for sig in ("jt_sig", "mg_sig", PRIMARY_WH, VARIANT_WH):
        months, pnos, sigs = formation_rows(panel, sig)
        cohorts, ns = build_cohorts(months, pnos, sigs, grid)
        cohort_sets[sig] = (cohorts, ns)
        counts = np.array([ns.get(f0 + k, 0) for k in range(n_f)])
        uni_stats[sig] = {
            "mean": float(counts.mean()), "min": int(counts.min()),
            "max": int(counts.max()),
            "n_below_4": int((counts < 4).sum()),
            "n_zero": int((counts == 0).sum()),
        }

    # ---- strategy series (decimal) -----------------------------------------
    series = {}
    for key, sig in (("jt", "jt_sig"), ("mg", "mg_sig"),
                     ("wh", PRIMARY_WH), ("wh_hi_abs", VARIANT_WH)):
        cohorts, _ = cohort_sets[sig]
        series[key] = strategy_pair(cohorts, f0, n_f, hold0, n_hold,
                                    permnos, ret_mat)

    min_avail = min(
        int(series[k][f"n_{g}"].min())
        for k in series for g in ("w", "l")
    )
    # strategy_returns.parquet (percent, wh = PRIMARY)
    sr = pd.DataFrame({
        "month": hold_months,
        "jt_w": series["jt"]["w"] * 100, "jt_l": series["jt"]["l"] * 100,
        "jt_wl": series["jt"]["wl"] * 100,
        "mg_w": series["mg"]["w"] * 100, "mg_l": series["mg"]["l"] * 100,
        "mg_wl": series["mg"]["wl"] * 100,
        "wh_w": series["wh"]["w"] * 100, "wh_l": series["wh"]["l"] * 100,
        "wh_wl": series["wh"]["wl"] * 100,
    })
    if write_outputs:
        sr.to_parquet(intermediate_path("strategy_returns.parquet"), index=False)

    # ---- Table I -------------------------------------------------------------
    def t1_rows(prefix: str, key: str):
        s = series[key]
        return [
            {"name": f"{prefix}_winner", "paper": t1[f"{prefix}_winner"][0],
             "ours": mean_pct(s["w"], mask_all), "tol": t1[f"{prefix}_winner"][1]},
            {"name": f"{prefix}_loser", "paper": t1[f"{prefix}_loser"][0],
             "ours": mean_pct(s["l"], mask_all), "tol": t1[f"{prefix}_loser"][1]},
            {"name": f"{prefix}_w_minus_l", "paper": t1[f"{prefix}_w_minus_l"][0],
             "ours": mean_pct(s["wl"], mask_all), "tol": t1[f"{prefix}_w_minus_l"][1]},
            {"name": f"{prefix}_w_minus_l_tstat", "paper": t1[f"{prefix}_w_minus_l_tstat"][0],
             "ours": tstat(s["wl"][mask_all] * 100), "tol": t1[f"{prefix}_w_minus_l_tstat"][1]},
        ]

    rows1 = (t1_rows("jt", "jt") + t1_rows("mg", "mg") + t1_rows("wh", "wh"))
    tab1_lines, counts1 = md_metric_table(rows1)

    wh_cl_rows = t1_rows("wh", "wh")
    wh_var_rows = t1_rows("wh", "wh_hi_abs")
    var_lines = [
        f"| metric | paper | {PRIMARY_WH} (PRIMARY) | err pp | "
        f"{VARIANT_WH} (VARIANT) | err pp |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for rc, rv in zip(wh_cl_rows, wh_var_rows):
        var_lines.append(
            f"| {rc['name']} | {fmt(rc['paper'])} | {fmt(rc['ours'])} | "
            f"{rc['ours'] - rc['paper']:+.4f} | {fmt(rv['ours'])} | "
            f"{rv['ours'] - rv['paper']:+.4f} |"
        )
    err_cl = sum(abs(r["ours"] - r["paper"]) for r in wh_cl_rows)
    err_var = sum(abs(r["ours"] - r["paper"]) for r in wh_var_rows)
    wl_err_cl = abs(wh_cl_rows[2]["ours"] - wh_cl_rows[2]["paper"])
    wl_err_var = abs(wh_var_rows[2]["ours"] - wh_var_rows[2]["paper"])
    pick = (f"{PRIMARY_WH} (PRIMARY)" if err_cl <= err_var
            else f"{VARIANT_WH} (VARIANT)")

    L1 = [
        "# Table I — George & Hwang (2004): average monthly returns, (6,6) "
        "strategies, EW, all months 1963-07 .. 2001-12 (462 months)",
        "",
        "Machinery: signal at formation f -> 30/30 sort (signal asc, permno "
        "asc tie-break) -> cohort held f+1..f+6 -> month-t value = mean of "
        "the 6 cohorts formed at t-6..t-1. No skip month. Returns in percent.",
        "",
        f"Holding-period returns: panel column `{ret_col}`"
        + (" (delisting-adjusted)" if ret_col == "ret_dl" else "")
        + "; ranking signals always on original ret.",
        "",
        f"## Official metrics (wh_* = PRIMARY signal {PRIMARY_WH})",
        "",
        *tab1_lines,
        "",
        f"## 52WH signal adjudication (PRIMARY {PRIMARY_WH} vs VARIANT "
        f"{VARIANT_WH} = |prc|/max(|askhi|))",
        "",
        *var_lines,
        "",
        f"- |W-L error|: {PRIMARY_WH} {wl_err_cl:.4f}pp vs {VARIANT_WH} {wl_err_var:.4f}pp",
        f"- Sum of |error| over the 4 metrics: {PRIMARY_WH} {err_cl:.4f} vs {VARIANT_WH} {err_var:.4f}",
        f"- **Pick: {pick}** (for the Replicator to lock)",
        "",
        "## Universe size at formation (per signal, over the 467 formation months "
        f"{FORM_START.date()} .. {FORM_END.date()})",
        "",
        "| signal | mean n | min n | max n | months with n<4 |",
        "|---|---:|---:|---:|---:|",
    ]
    for sig, st in uni_stats.items():
        L1.append(f"| {sig} | {st['mean']:.1f} | {st['min']} | {st['max']} | {st['n_below_4']} |")
    L1 += [
        "",
        f"- Min cohorts available per holding month across all W/L series: {min_avail} "
        "(6 = no cohort ever dropped by missing returns).",
    ]
    if write_outputs:
        LAYOUT.result_path("table_1.md").write_text("\n".join(L1))

    # ---- Table II ---------------------------------------------------------------
    def t2_rows(pfx: str, key: str, mask: np.ndarray):
        s = series[key]
        return [
            {"name": f"{pfx}_winner", "paper": t2[f"{pfx}_winner"][0],
             "ours": mean_pct(s["w"], mask), "tol": t2[f"{pfx}_winner"][1]},
            {"name": f"{pfx}_loser", "paper": t2[f"{pfx}_loser"][0],
             "ours": mean_pct(s["l"], mask), "tol": t2[f"{pfx}_loser"][1]},
            {"name": f"{pfx}_w_minus_l", "paper": t2[f"{pfx}_w_minus_l"][0],
             "ours": mean_pct(s["wl"], mask), "tol": t2[f"{pfx}_w_minus_l"][1]},
            {"name": f"{pfx}_tstat", "paper": t2[f"{pfx}_tstat"][0],
             "ours": tstat(s["wl"][mask] * 100), "tol": t2[f"{pfx}_tstat"][1]},
        ]

    rowsA = t2_rows("pA_jt", "jt", mask_exjan) + t2_rows("pA_mg", "mg", mask_exjan) \
        + t2_rows("pA_wh", "wh", mask_exjan)
    rowsB = t2_rows("pB_jt", "jt", mask_jan) + t2_rows("pB_mg", "mg", mask_jan) \
        + t2_rows("pB_wh", "wh", mask_jan)
    tabA, countsA = md_metric_table(rowsA)
    tabB, countsB = md_metric_table(rowsB)

    # January-collapse sanity
    san = ["| strategy | loser Table I (all) | loser Panel A (ex-Jan) | loser Panel B (Jan) |",
           "|---|---:|---:|---:|"]
    for pfx_t1, pfx_t2, key in (("jt", "jt", "jt"), ("mg", "mg", "mg"), ("wh", "wh", "wh")):
        s = series[key]
        san.append(
            f"| {pfx_t1.upper()} | {mean_pct(s['l'], mask_all):.4f} | "
            f"{mean_pct(s['l'], mask_exjan):.4f} | {mean_pct(s['l'], mask_jan):.4f} |"
        )

    L2 = [
        "# Table II — George & Hwang (2004): (6,6) strategies split by calendar "
        "month of the HOLDING month t",
        "",
        f"Panel A: months t with month-of-year != 1 ({int(mask_exjan.sum())} months). "
        f"Panel B: January only ({n_jan} months). Same machinery as Table I.",
        "",
        f"Holding-period returns: panel column `{ret_col}`"
        + (" (delisting-adjusted)" if ret_col == "ret_dl" else "")
        + "; ranking signals always on original ret.",
        "",
        "## Panel A (excluding January)",
        "",
        *tabA,
        "",
        "## Panel B (January only)",
        "",
        *tabB,
        "",
        "## January-collapse sanity check (loser returns, percent/month)",
        "",
        *san,
        "",
        "- Expected: losers collapse from Table I to Panel A (January rebound "
        "removed), especially JT/52WH; Panel B losers ~11-12%.",
    ]
    if write_outputs:
        LAYOUT.result_path("table_2.md").write_text("\n".join(L2))

    # ---- Table III ------------------------------------------------------------------
    jt_coh, _ = cohort_sets["jt_sig"]
    wh_coh, _ = cohort_sets[PRIMARY_WH]
    f_indices = [f0 + k for k in range(n_f)]
    cells = intersection_cells(jt_coh, wh_coh, f_indices)
    cell_ser = {
        key: cell_series(members, f0, n_f, hold0, n_hold, permnos, ret_mat)
        for key, members in cells.items()
    }

    def cell_mean(jg: str, wg: str, mask: np.ndarray) -> float:
        return mean_pct(cell_ser[(jg, wg)][0], mask)

    rows3: list[dict] = []
    drop_report: list[tuple] = []
    for outer in ("W", "M", "L"):
        o_name = {"W": "winner", "M": "middle", "L": "loser"}[outer]
        for col, inner, tgt in (("winner", "W", "winner"), ("loser", "L", "loser")):
            for suffix, mask in (("all", mask_all), ("exjan", mask_exjan)):
                nm = f"pa_{o_name}_{col}_{suffix}"
                rows3.append({"name": nm, "paper": t3[nm][0],
                              "ours": cell_mean(outer, inner, mask), "tol": t3[nm][1]})
        for suffix, mask in (("all", mask_all), ("exjan", mask_exjan)):
            nm = f"pa_{o_name}_w_minus_l_{suffix}"
            # Panel A: 52WH winner vs 52WH loser WITHIN jt group `outer`
            m, t, nboth, dropped = wl_row_pair(cell_ser, (outer, "W"), (outer, "L"), mask)
            rows3.append({"name": nm, "paper": t3[nm][0], "ours": m, "tol": t3[nm][1]})
            rows3.append({"name": nm + "_tstat", "paper": t3[nm + "_tstat"][0],
                          "ours": t, "tol": t3[nm + "_tstat"][1]})
            drop_report.append(("Panel A", o_name, suffix, nboth, dropped, int(mask.sum())))

    for outer in ("W", "M", "L"):
        o_name = {"W": "winner", "M": "middle", "L": "loser"}[outer]
        for col, inner in (("winner", "W"), ("loser", "L")):
            for suffix, mask in (("all", mask_all), ("exjan", mask_exjan)):
                nm = f"pb_{o_name}_{col}_{suffix}"
                rows3.append({"name": nm, "paper": t3[nm][0],
                              "ours": cell_mean(inner, outer, mask), "tol": t3[nm][1]})
        for suffix, mask in (("all", mask_all), ("exjan", mask_exjan)):
            nm = f"pb_{o_name}_w_minus_l_{suffix}"
            m, t, nboth, dropped = wl_row_pair(cell_ser, ("W", outer), ("L", outer), mask)
            rows3.append({"name": nm, "paper": t3[nm][0], "ours": m, "tol": t3[nm][1]})
            rows3.append({"name": nm + "_tstat", "paper": t3[nm + "_tstat"][0],
                          "ours": t, "tol": t3[nm + "_tstat"][1]})
            drop_report.append(("Panel B", o_name, suffix, nboth, dropped, int(mask.sum())))

    tab3, counts3 = md_metric_table(rows3)
    drop_lines = ["| panel | outer group | column | months both cells exist | months dropped | months total |",
                  "|---|---|---|---:|---:|---:|"]
    for p, o, sfx, nb, dr, tot in drop_report:
        drop_lines.append(f"| {p} | {o} | {sfx} | {nb} | {dr} | {tot} |")

    L3 = [
        "# Table III — George & Hwang (2004): pairwise nested sorts (JT x 52-week high), EW",
        "",
        "At each formation f, INDEPENDENT 30/40/30 sorts on jt_sig and on "
        f"{PRIMARY_WH}; a 3x3 cell holds stocks present in BOTH groupings. "
        "Cell month-t value = mean over cohorts f ∈ {t-6..t-1} that are "
        "non-empty. W-L rows average only months where BOTH cells are "
        "non-missing (footnote 6) and are deliberately NOT the difference of "
        "the two cell rows above them (paper, explicitly).",
        "",
        f"Holding-period returns: panel column `{ret_col}`"
        + (" (delisting-adjusted)" if ret_col == "ret_dl" else "")
        + "; ranking signals always on original ret.",
        "",
        *tab3,
        "",
        "## Months dropped by the nonempty-cell rule (W-L rows)",
        "",
        *drop_lines,
    ]
    if write_outputs:
        LAYOUT.result_path("table_3.md").write_text("\n".join(L3))

    c2 = {k: countsA[k] + countsB[k] for k in countsA}

    # ---- console report ----------------------------------------------------------
    if verbose:
        print("=" * 78)
        print(f"TABLES I/II/III — holding-period return column `{ret_col}`")
        print("=" * 78)
        print("TABLE I (all 462 months, percent/month)")
        for r in rows1:
            print(f"  {r['name']:28s} paper {r['paper']:8.4f}  ours {r['ours']:10.4f}  "
                  f"dev {r['ours'] - r['paper']:+.4f}pp  {tier(r['paper'], r['ours'], r['tol'])}")
        print()
        print("52WH ADJUDICATION (Table I row)")
        for rc, rv in zip(wh_cl_rows, wh_var_rows):
            print(f"  {rc['name']:28s} paper {rc['paper']:8.4f}  {PRIMARY_WH} {rc['ours']:10.4f} "
                  f"(err {rc['ours'] - rc['paper']:+.4f})  {VARIANT_WH} {rv['ours']:10.4f} "
                  f"(err {rv['ours'] - rv['paper']:+.4f})")
        print(f"  |W-L error|: {PRIMARY_WH} {wl_err_cl:.4f}pp vs {VARIANT_WH} {wl_err_var:.4f}pp; "
              f"sum|err| {PRIMARY_WH} {err_cl:.4f} vs {VARIANT_WH} {err_var:.4f} -> PICK {pick}")
        print()
        print("TABLE II")
        print(f"  Panel A months (ex-Jan): {int(mask_exjan.sum())}; Panel B (Jan): {n_jan}")
        for r in rowsA + rowsB:
            print(f"  {r['name']:28s} paper {r['paper']:8.4f}  ours {r['ours']:10.4f}  "
                  f"dev {r['ours'] - r['paper']:+.4f}pp  {tier(r['paper'], r['ours'], r['tol'])}")
        print()
        print("  January-collapse sanity (losers):")
        for key in ("jt", "mg", "wh"):
            s = series[key]
            print(f"    {key.upper()}: all {mean_pct(s['l'], mask_all):.4f}  "
                  f"ex-Jan {mean_pct(s['l'], mask_exjan):.4f}  "
                  f"Jan {mean_pct(s['l'], mask_jan):.4f}")
        print()
        print("TABLE III")
        for r in rows3:
            print(f"  {r['name']:34s} paper {r['paper']:8.4f}  ours {r['ours']:10.4f}  "
                  f"dev {r['ours'] - r['paper']:+.4f}pp  {tier(r['paper'], r['ours'], r['tol'])}")
        print()
        print("  Months dropped by nonempty-cell rule (W-L rows):")
        for p, o, sfx, nb, dr, tot in drop_report:
            print(f"    {p} {o:6s} {sfx:6s}: {nb} months used, {dr} dropped of {tot}")
        print()
        print("UNIVERSE AT FORMATION (467 formation months "
              f"{FORM_START.date()} .. {FORM_END.date()})")
        for sig, st in uni_stats.items():
            print(f"  {sig:14s} mean {st['mean']:.1f}  min {st['min']}  max {st['max']}  "
                  f"n<4 months {st['n_below_4']}")
        print(f"  min cohorts available per holding month across W/L series: {min_avail}")
        print()
        print("HIT RATES")
        for label, c in (("T1", counts1), ("T2A", countsA), ("T2B", countsB),
                         ("T3", counts3)):
            tot = sum(c.values())
            print(f"  {label}: {c['Tier 1']} Tier 1 / {c['Tier 2']} Tier 2 / "
                  f"{c['FAIL']} FAIL out of {tot}")
        print(f"  T2 combined: {c2['Tier 1']} / {c2['Tier 2']} / {c2['FAIL']} out of {sum(c2.values())}")

    return {
        "ret_col": ret_col,
        "rows1": rows1, "rowsA": rowsA, "rowsB": rowsB, "rows3": rows3,
        "counts1": counts1, "countsA": countsA, "countsB": countsB,
        "counts2_combined": c2, "counts3": counts3,
        "series": series, "uni_stats": uni_stats, "min_avail": min_avail,
        "wh_cl_rows": wh_cl_rows, "wh_var_rows": wh_var_rows,
        "wl_err_cl": wl_err_cl, "wl_err_var": wl_err_var, "pick": pick,
        "drop_report": drop_report,
    }


def main() -> None:
    run()


def wl_row_pair(cell_ser, keyW, keyL, mask):
    sW, _ = cell_ser[keyW]
    sL, _ = cell_ser[keyL]
    both = np.isfinite(sW) & np.isfinite(sL) & mask
    wl = sW - sL
    n_both = int(both.sum())
    dropped = int(mask.sum()) - n_both
    mean = float(wl[both].mean() * 100) if n_both else np.nan
    t = tstat(wl[both] * 100) if n_both else np.nan
    return mean, t, n_both, dropped


if __name__ == "__main__":
    main()
