"""
Replication of Foster, Olsen & Shevlin (1984), "Earnings Releases, Anomalies, and
the Behavior of Security Prices" (JAE 1984) — DATA PIPELINE.

Post-earnings-announcement-drift event study over 1974Q1-1981Q4. Four forecast-error
(FE) models:
  Model 1: FE1 = (Q_t - E_t) / |Q_t|                       (eq. 9)
  Model 2: FE2 = (Q_t - E_t) / sigma(prior forecast errors) (eq. 10)
  Model 3: FE3 = sum u[-1,0] / sigma(u[-251,-2])            (eq. 12)
  Model 4: FE4 = (sum u[-60,0] / 61) / sigma(u[-311,-61])   (eq. 13)
with E(Q_t) = Q_{t-4} + phi*(Q_{t-1} - Q_{t-5}) + delta      (eq. 8)
and   u = R_i - R_p (NYSE size-decile EW benchmark)          (eq. 15)

Artifacts:
  data/cache/decile_returns.parquet  (date, decile, ret_ew)   — NYSE size-decile EW daily returns
  data/cache/event_returns.parquet   (obs_id, event_day, date, ret, decile_ret, u)
  data/panel.parquet           one row per (firm, quarter) observation, 1974Q1-1981Q4

Methodology decisions are FIXED in preparations/assumptions.md (A1-A15) and
preparations/preprocessing_rules.json — this script implements them exactly.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

# --- project utils (path + env resolution) ---------------------------------
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402

LAYOUT = paper_layout("earnings_releases_anomalies")
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")

# --- configuration (assumptions A1-A15 / preprocessing_rules.json) ----------
RULES = json.loads(Path(LAYOUT.preparations_path("preprocessing_rules.json")).read_text())
RULE_IDS = {r["rule_id"] for r in RULES}  # single source of truth; constants below
# reference the rule/assumption they implement — fail loudly if the registry changed.
_REQUIRED_RULES = {
    "sample_ten_consecutive_earnings", "sample_earnings_file_range", "sample_car_period",
    "var_earnings_forecast_model", "var_forecast_params_20q", "var_fe_model1",
    "var_fe_model2", "var_fe_model2_sigma_max20", "var_fe_model3", "var_fe_model3_sigma",
    "var_fe_model4", "var_fe_model4_window", "var_fe_model4_sigma",
    "sort_fep_decile_cutoffs", "sort_prior_quarter_cutoffs_equal_weight",
    "var_abnormal_return_size_decale", "factor_size_decile_benchmark",
    "factor_size_decile_construction", "var_car_m1_0", "var_car_m60_0", "var_car_p1_p60",
}
assert _REQUIRED_RULES <= RULE_IDS, f"missing rules: {_REQUIRED_RULES - RULE_IDS}"

MIN_CONSEC_QUARTERS = 10        # A5 / sample_ten_consecutive_earnings
EARN_WINDOW = ("1970-04-01", "1981-12-31")   # A2 / sample_earnings_file_range (1970Q2-1981Q4)
DSF_WINDOW = ("1968-01-01", "1982-12-31")    # Step 3 (250+61+60 days before 1974Q1, +60 after 1981Q4)
RANK_YEARS = range(1973, 1983 + 0)           # A8: year-start rankings 1973..1982 (inclusive)
PANEL_Q0, PANEL_Q1 = 7897, 7928              # 1974Q1 .. 1981Q4 (qidx = fyearq*4 + fqtr)
EXT_Q0 = 7896                                # 1973Q4 included for FEP cutoffs (A14)
CUTOFF_Q0, CUTOFF_Q1 = 7896, 7927            # cutoff quarters 1973Q4..1981Q3
FE_START_QLABEL = 19734                      # Step 2: forecasts start at 1973Q4
REG_MAX, REG_MIN = 20, 10                    # A10 / var_forecast_params_20q
SIG2_MAX, SIG2_MIN = 20, 5                   # A9 / var_fe_model2_sigma_max20
SIG34_WINDOW, SIG34_MIN = 250, 100           # A11 / var_fe_model3_sigma, var_fe_model4_sigma
DAY0_SLACK_DAYS = 5                          # A7 (trading day within rdq..rdq+5)
N_FEP = 10                                   # A14 / sort_fep_decile_cutoffs
LINK_PRIM, LINK_TYPE = ("P", "C"), ("LU", "LC")  # A6


def qidx_of(fyearq: int, fqtr: int) -> int:
    return int(fyearq) * 4 + int(fqtr)


def qidx_to_label(q: int) -> int:
    fqtr = (q - 1) % 4 + 1
    return (q - fqtr) // 4 * 10 + fqtr


# --- ClickHouse connection ---------------------------------------------------
_CFG = get_clickhouse_config()


def _client() -> Client:
    return Client(
        host=os.getenv("CLICKHOUSE_HOST", _CFG["host"]),
        port=int(os.getenv("CLICKHOUSE_PORT", _CFG["port"])),
        user=os.getenv("CLICKHOUSE_USER", _CFG["user"]),
        password=os.getenv("CLICKHOUSE_PASSWORD", _CFG["password"]),
        settings={"max_execution_time": 600},
    )


def q(sql: str) -> pd.DataFrame:
    c = _client()
    data, cols = c.execute(sql.strip().rstrip(";"), with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str, **subs) -> pd.DataFrame:
    sql = Path(SQL_DIR / name).read_text()
    for k, v in subs.items():
        sql = sql.replace("{" + k + "}", v)
    return q(sql)


def gvkey_list_sql(gvkeys) -> str:
    return ",".join("'" + str(g).replace("'", "") + "'" for g in gvkeys)


def t(msg: str, t0: float) -> float:
    t1 = time.time()
    print(f"[{t1 - t0:6.1f}s] {msg}", flush=True)
    return t1


# =============================================================================
# Step 1 — Compustat quarterly earnings + Screen 1 (A5)
# =============================================================================
def step1_earnings(t0: float):
    earn = q_file("earnings.sql")
    earn["datadate"] = pd.to_datetime(earn["datadate"])
    earn["rdq"] = pd.to_datetime(earn["rdq"])
    earn = earn.dropna(subset=["gvkey", "fyearq", "fqtr"])
    earn["qidx"] = earn["fyearq"].astype(int) * 4 + earn["fqtr"].astype(int)
    earn["qlabel"] = earn["fyearq"].astype(int) * 10 + earn["fqtr"].astype(int)
    t(f"Step 1: fundq pull — {len(earn):,} rows, {earn['gvkey'].nunique():,} gvkeys", t0)

    # Screen 1 (A5): >=10 consecutive non-missing epspxq quarters within the window.
    # Consecutive = adjacent (fyearq, fqtr) sequence (qidx steps of 1), no gap.
    valid = earn.loc[earn["epspxq"].notna(), ["gvkey", "qidx"]]
    qsets = valid.groupby("gvkey")["qidx"].agg(set)

    def max_run(qs) -> int:
        best = run = 0
        prev = None
        for x in sorted(qs):
            run = run + 1 if (prev is not None and x == prev + 1) else 1
            best = max(best, run)
            prev = x
        return best

    runs = qsets.map(max_run)
    keep = runs[runs >= MIN_CONSEC_QUARTERS].index
    screen1 = earn[earn["gvkey"].isin(keep)].copy()
    n_firms_s1 = screen1["gvkey"].nunique()
    # A1: drop rows with NULL epspxq (no imputation). Earnings Q = epspxq.
    earnings = screen1[screen1["epspxq"].notna()].rename(columns={"epspxq": "Q"}).copy()
    t(f"Step 1: Screen 1 — {n_firms_s1:,} firms with >={MIN_CONSEC_QUARTERS} consecutive "
      f"non-missing EPS quarters (paper: 2,213); {len(earnings):,} firm-quarter rows kept", t0)
    return earnings, n_firms_s1


# =============================================================================
# Step 2 — FE Models 1 & 2 (Foster 1977 seasonal model, eq. 8-10, A9/A10)
# =============================================================================
def step2_fe12(earnings: pd.DataFrame, t0: float) -> pd.DataFrame:
    rows = []
    n_zero_sigma2 = 0
    for gvkey, g in earnings.groupby("gvkey", sort=False):
        g = g.sort_values("qidx")
        Q = dict(zip(g["qidx"].to_numpy(), g["Q"].to_numpy()))
        min_key = min(Q)
        raws: list[float] = []  # forecast errors in ascending quarter order
        for t_q in sorted(Q):
            if qidx_to_label(t_q) < FE_START_QLABEL:
                continue
            # --- phi, delta: OLS of (Q_s - Q_{s-4}) on const + (Q_{s-1} - Q_{s-5})
            # over the most recent min(20, available) quarters s <= t-1 with all
            # four inputs; require >=10 (A10).
            xs: list[float] = []
            ys: list[float] = []
            s = t_q - 1
            while len(xs) < REG_MAX and s >= min_key:
                if s in Q and (s - 4) in Q and (s - 1) in Q and (s - 5) in Q:
                    xs.append(Q[s - 1] - Q[s - 5])
                    ys.append(Q[s] - Q[s - 4])
                s -= 1
            if len(xs) < REG_MIN:
                continue
            # Drop the forecast if Q_{t-4} or (Q_{t-1} - Q_{t-5}) unavailable (A10).
            if (t_q - 4) not in Q or (t_q - 1) not in Q or (t_q - 5) not in Q:
                continue
            xa = np.asarray(xs)
            ya = np.asarray(ys)
            coef = np.linalg.lstsq(np.column_stack([np.ones(len(xa)), xa]), ya, rcond=None)[0]
            delta, phi = float(coef[0]), float(coef[1])
            e_t = Q[t_q - 4] + phi * (Q[t_q - 1] - Q[t_q - 5]) + delta
            raw = Q[t_q] - e_t
            # FE1 (eq. 9): drop if Q_t == 0.
            fe1 = raw / abs(Q[t_q]) if Q[t_q] != 0 else np.nan
            # FE2 (eq. 10, A9): sigma over most recent <=20 prior forecast errors,
            # require >=5 priors.
            prior = raws[-SIG2_MAX:]
            fe2 = np.nan
            if len(prior) >= SIG2_MIN:
                sig = float(np.std(prior, ddof=1))
                if sig > 0:
                    fe2 = raw / sig
                else:
                    n_zero_sigma2 += 1
            rows.append((gvkey, t_q, qidx_to_label(t_q), fe1, fe2, raw))
            raws.append(raw)
    fe12 = pd.DataFrame(rows, columns=["gvkey", "qidx", "qlabel", "fe1", "fe2", "raw_fe"])
    t(f"Step 2: FE1/FE2 — {len(fe12):,} firm-quarter forecasts "
      f"(fe1 N={fe12['fe1'].notna().sum():,}, fe2 N={fe12['fe2'].notna().sum():,}; "
      f"zero-sigma2 drops={n_zero_sigma2})", t0)
    return fe12


# =============================================================================
# Step 3 — CRSP-Compustat link (A6) + sample daily returns
# =============================================================================
def step3_link_and_daily(earnings: pd.DataFrame, t0: float):
    # Observation universe: quarters 1973Q4..1981Q4 with non-null rdq (A3). 1973Q4
    # is needed so its FEs form the cutoffs assigning 1974Q1 portfolios (A14).
    obs = earnings[(earnings["qidx"] >= EXT_Q0) & (earnings["qidx"] <= PANEL_Q1)]
    obs = obs.loc[obs["rdq"].notna(),
                  ["gvkey", "fyearq", "fqtr", "qlabel", "qidx", "Q", "rdq"]].copy()
    n_obs_no_rdq_dropped = int(
        ((earnings["qidx"] >= EXT_Q0) & (earnings["qidx"] <= PANEL_Q1)).sum() - len(obs)
    )

    gvkeys = sorted(earnings["gvkey"].unique())
    links = q_file("sample_links.sql", GVKEY_LIST=gvkey_list_sql(gvkeys))
    links["linkdt"] = pd.to_datetime(links["linkdt"])
    links["linkenddt"] = pd.to_datetime(links["linkenddt"])
    links = links.dropna(subset=["permno"])
    links["permno"] = links["permno"].astype(int)

    # PIT validity per announcement (A6): rdq in [linkdt, COALESCE(linkenddt,'2100-01-01')];
    # prefer linkprim='P', then earliest linkdt.
    m = obs.merge(links, on="gvkey", how="inner")
    m = m[(m["rdq"] >= m["linkdt"]) & (m["rdq"] <= m["linkenddt"])]
    m["_prio"] = (m["linkprim"] != "P").astype(int)
    m = m.sort_values(["gvkey", "fyearq", "fqtr", "_prio", "linkdt", "permno"])
    obs_linked = m.drop_duplicates(["gvkey", "fyearq", "fqtr"], keep="first").drop(
        columns=["linkprim", "linkdt", "linkenddt", "_prio"])
    obs_linked["obs_id"] = (obs_linked["gvkey"].astype(str) + "_"
                            + obs_linked["fyearq"].astype(str) + "_"
                            + obs_linked["fqtr"].astype(str))
    firms_s2_panel = obs_linked.loc[obs_linked["qidx"] >= PANEL_Q0, "gvkey"].nunique()
    t(f"Step 3: CRSP link (A6) — {len(obs_linked):,} observations linked "
      f"({firms_s2_panel:,} firms with a valid link + non-null rdq in 1974Q1-1981Q4; "
      f"paper: 2,053); {n_obs_no_rdq_dropped:,} obs dropped for missing rdq (A3)", t0)

    # Daily returns for all permnos ever linked to Screen-1 firms, 1968-1982.
    sample = q_file("sample_daily.sql", GVKEY_LIST=gvkey_list_sql(gvkeys))
    sample["date"] = pd.to_datetime(sample["date"])
    sample["permno"] = sample["permno"].astype(int)
    sample = sample.drop_duplicates(["permno", "date"]).sort_values(["permno", "date"])
    t(f"Step 3: sample_daily — {len(sample):,} rows, {sample['permno'].nunique():,} permnos "
      f"over {DSF_WINDOW[0]}..{DSF_WINDOW[1]}", t0)
    return obs_linked, sample


# =============================================================================
# Step 4 — NYSE size-decile benchmark (A8)
# =============================================================================
def yearstart_me(df: pd.DataFrame, Y: int) -> pd.DataFrame:
    """Per-permno market cap at the start of year Y (A8): |prc|*shrout*1000 ($)
    as of the last trading day on/before Dec 31 of Y-1; fallback: first trading
    day of January Y."""
    dec31 = pd.Timestamp(Y - 1, 12, 31)
    jan1, jan31 = pd.Timestamp(Y, 1, 1), pd.Timestamp(Y, 1, 31)
    pre = df[df["date"] <= dec31]
    idx_pre = pre.groupby("permno")["date"].idxmax()
    have = set(pre["permno"].unique())
    jan = df[(df["date"] >= jan1) & (df["date"] <= jan31) & (~df["permno"].isin(have))]
    idx_jan = jan.groupby("permno")["date"].idxmin()
    rows = df.loc[np.concatenate([idx_pre.to_numpy(), idx_jan.to_numpy()])].copy()
    rows["me_yearstart"] = rows["prc"].abs() * rows["shrout"] * 1000.0
    rows["year"] = Y
    return rows[["year", "permno", "me_yearstart"]]


def step4_deciles(t0: float):
    nyse = q_file("nyse_daily.sql")
    nyse["date"] = pd.to_datetime(nyse["date"])
    nyse["permno"] = nyse["permno"].astype(int)
    # Prefer the row with a non-missing ret if windows overlapped.
    nyse = (nyse.sort_values(["permno", "date", "ret"], na_position="last")
            .drop_duplicates(["permno", "date"], keep="first"))
    t(f"Step 4: nyse_daily — {len(nyse):,} rows, {nyse['permno'].nunique():,} PIT-NYSE permnos", t0)

    memberships, dr_chunks, edges_rows = [], [], []
    for Y in RANK_YEARS:
        jan1, dec31Y = pd.Timestamp(Y, 1, 1), pd.Timestamp(Y, 12, 31)
        mem = yearstart_me(nyse, Y)
        # Equal-count deciles (1=smallest .. 10=largest); ties split by permno
        # order (deterministic rank). The 9 interior bin edges (max ME within
        # bins 1..9) are the breakpoints; member deciles are then defined by
        # those edges (decile = 1 + #{edges < ME}) so membership and assignment
        # are identical for NYSE firms.
        mem = mem.sort_values(["me_yearstart", "permno"])
        n = len(mem)
        bins = np.ceil(np.arange(1, n + 1) * N_FEP / n).astype(int)
        edge_vals = np.array(
            [mem["me_yearstart"].to_numpy()[bins == k].max() for k in range(1, N_FEP)])
        mev = mem["me_yearstart"].to_numpy()
        mem["decile"] = (1 + np.sum(edge_vals[None, :] < mev[:, None], axis=1)).astype(int)
        edges_rows.append((Y, *edge_vals))
        memberships.append(mem)
        # Decile EW daily return over year Y (members fixed; non-missing ret only).
        yr = nyse[(nyse["date"] >= jan1) & (nyse["date"] <= dec31Y) & nyse["ret"].notna()]
        yr = yr.merge(mem[["permno", "decile"]], on="permno", how="inner")
        dr = (yr.groupby(["date", "decile"])["ret"].mean().reset_index()
              .rename(columns={"ret": "ret_ew"}))
        dr_chunks.append(dr)

    membership = pd.concat(memberships, ignore_index=True)
    edges = pd.DataFrame(edges_rows, columns=["year"] + [f"e{k}" for k in range(1, N_FEP)])
    decile_returns = pd.concat(dr_chunks, ignore_index=True)
    out = LAYOUT.data_path("cache/decile_returns.parquet")
    out.parent.mkdir(parents=True, exist_ok=True)
    decile_returns.to_parquet(out, index=False)
    t(f"Step 4: decile_returns — {len(decile_returns):,} (date x decile) rows -> {out.name}; "
      f"membership: {len(membership):,} (year, permno) entries", t0)

    # Table 3 preview: decile mean daily return 1973-1981, in percent.
    d7381 = decile_returns[(decile_returns["date"] >= "1973-01-01")
                           & (decile_returns["date"] <= "1981-12-31")]
    means_pct = d7381.groupby("decile")["ret_ew"].mean() * 100.0
    print("\n  Table 3 preview — NYSE size-decile mean daily return 1973-1981 (%/day):")
    paper_t3 = [0.111, 0.084, 0.070, 0.063, 0.061, 0.053, 0.048, 0.046, 0.038, 0.021]
    for dec in range(1, 11):
        v = means_pct.get(dec, np.nan)
        print(f"    D{dec:2d}: {v:7.3f}   (paper: {paper_t3[dec - 1]:.3f})")
    print("", flush=True)
    return membership, decile_returns, edges


# =============================================================================
# Step 5 — Event-time returns and u = R_i - R_p (eq. 15, A7/A8)
# =============================================================================
def step5_event_returns(obs_linked, sample, decile_returns, edges, t0):
    obs = obs_linked.copy()
    obs["ann_year"] = obs["rdq"].dt.year
    # Firm's size decile "in the quarter examined" (A8): the decile its own
    # year-start ME falls into under the NYSE breakpoints of the announcement's
    # calendar year. Decile RETURNS are the EW means of NYSE members only
    # (Step 4); assignment uses those breakpoints for every sample firm, so
    # non-NYSE firms are placed into the decile defined by the NYSE size edges
    # (standard breakpoint methodology; the paper's 2,053-firm sample exceeds
    # the NYSE listing count of the era, so all sample firms must be assigned).
    me_chunks = [yearstart_me(sample, Y) for Y in RANK_YEARS]
    sample_me = pd.concat(me_chunks, ignore_index=True)
    obs = obs.merge(sample_me, left_on=["ann_year", "permno"],
                    right_on=["year", "permno"], how="left").drop(columns=["year"])
    n_no_me = int(obs["me_yearstart"].isna().sum())
    obs = obs[obs["me_yearstart"].notna()].copy()
    obs = obs.merge(edges, left_on="ann_year", right_on="year", how="left")
    n_no_edges = int(obs["e1"].isna().sum())  # rdq in a year outside the 1973-1982 rankings
    obs = obs[obs["e1"].notna()].copy()
    edge_mat = obs[[f"e{k}" for k in range(1, N_FEP)]].to_numpy()
    mev = obs["me_yearstart"].to_numpy()
    obs["decile"] = np.clip(1 + np.sum(edge_mat < mev[:, None], axis=1), 1, N_FEP).astype(int)
    obs = obs.drop(columns=[f"e{k}" for k in range(1, N_FEP)] + ["year"])

    # Lookup: (date, decile) -> EW decile return.
    drp = decile_returns.pivot(index="date", columns="decile", values="ret_ew").sort_index()
    dr_vals = drp.to_numpy()  # columns 1..10 -> index decile-1
    dr_index = drp.index

    # Per-permno trading-day arrays.
    perm_dates: dict[int, np.ndarray] = {}
    perm_rets: dict[int, np.ndarray] = {}
    for permno, sub in sample.groupby("permno", sort=False):
        perm_dates[int(permno)] = sub["date"].to_numpy()
        perm_rets[int(permno)] = sub["ret"].to_numpy(dtype=float)

    oid_c, oid_v, ev_l, dt_l, r_l, dr_l, u_l = [], [], [], [], [], [], []
    day0_rows = []
    n_no_perm, n_no_day0 = 0, 0
    slack = np.timedelta64(DAY0_SLACK_DAYS, "D")
    for row in obs.itertuples(index=False):
        dates = perm_dates.get(int(row.permno))
        if dates is None or len(dates) == 0:
            n_no_perm += 1
            continue
        rdq64 = np.datetime64(row.rdq)
        pos = int(np.searchsorted(dates, rdq64, side="left"))
        # Day 0 = first trading day ON OR AFTER rdq (A7); require one within rdq..rdq+5.
        if pos >= len(dates) or dates[pos] > rdq64 + slack:
            n_no_day0 += 1
            continue
        day0 = dates[pos]
        lo, hi = max(0, pos - 311), min(len(dates) - 1, pos + 60)
        ev = np.arange(lo - pos, hi - pos + 1, dtype=np.int16)
        dts = dates[lo:hi + 1]
        r = perm_rets[int(row.permno)][lo:hi + 1]
        rpos = dr_index.get_indexer(dts)
        dr = np.full(len(dts), np.nan)
        ok = rpos >= 0
        dr[ok] = dr_vals[rpos[ok], int(row.decile) - 1]
        u = r - dr
        oid_c.append(row.obs_id)
        oid_v.append(np.full(len(ev), len(oid_c) - 1, dtype=np.int32))
        ev_l.append(ev)
        dt_l.append(dts)
        r_l.append(r)
        dr_l.append(dr)
        u_l.append(u)
        day0_rows.append((row.obs_id, pd.Timestamp(day0)))

    cats = pd.Categorical(oid_c)
    event_returns = pd.DataFrame({
        "obs_id": pd.Categorical.from_codes(np.concatenate(oid_v), categories=cats.categories),
        "event_day": np.concatenate(ev_l).astype(np.int16),
        "date": np.concatenate(dt_l).astype("datetime64[ns]"),
        "ret": np.concatenate(r_l),
        "decile_ret": np.concatenate(dr_l),
        "u": np.concatenate(u_l),
    })
    out = LAYOUT.data_path("cache/event_returns.parquet")
    out.parent.mkdir(parents=True, exist_ok=True)
    event_returns.to_parquet(out, index=False)
    day0_df = pd.DataFrame(day0_rows, columns=["obs_id", "day0"])
    obs_surv = obs.merge(day0_df, on="obs_id", how="inner")
    t(f"Step 5: event_returns — {len(event_returns):,} rows for {len(obs_surv):,} observations "
      f"-> {out.name}; dropped: {n_no_me:,} (no year-start ME for announcement year), "
      f"{n_no_edges:,} (rdq outside ranking years 1973-1982), {n_no_perm:,} (no dsf rows), "
      f"{n_no_day0:,} (no trade within rdq..rdq+{DAY0_SLACK_DAYS}d, A7)", t0)
    return obs_surv


# =============================================================================
# Step 6 — Models 3 & 4 FE + per-observation CARs (eq. 12-13, A11)
# =============================================================================
def step6_fe34(t0: float) -> pd.DataFrame:
    er = pd.read_parquet(LAYOUT.data_path("cache/event_returns.parquet"),
                         columns=["obs_id", "event_day", "u"])
    if not hasattr(er["obs_id"].dtype, "categories"):
        er["obs_id"] = er["obs_id"].astype("category")
    er = er.sort_values(["obs_id", "event_day"])
    codes = er["obs_id"].cat.codes.to_numpy()
    cats = er["obs_id"].cat.categories
    ev = er["event_day"].to_numpy()
    uv = er["u"].to_numpy(dtype=float)
    ends = np.flatnonzero(np.r_[codes[1:] != codes[:-1], True]) + 1
    starts = np.r_[0, ends[:-1]]

    out = []
    for c, (a, b) in enumerate(zip(starts, ends)):
        e, uu = ev[a:b], uv[a:b]
        m10 = (e >= -1) & (e <= 0)
        m600 = (e >= -60) & (e <= 0)
        p160 = (e >= 1) & (e <= 60)
        s3w = (e >= -SIG34_WINDOW - 1) & (e <= -2)      # [-251, -2]
        s4w = (e >= -311) & (e <= -61)                  # [-311, -61]

        def win_sum(mask):
            v = uu[mask]
            v = v[~np.isnan(v)]
            return (float(v.sum()), len(v)) if v.size > 0 else (np.nan, 0)

        sum10, n10 = win_sum(m10)
        sum600, n600 = win_sum(m600)
        sump160, _ = win_sum(p160)
        v3 = uu[s3w]; v3 = v3[~np.isnan(v3)]; n3 = int(v3.size)
        v4 = uu[s4w]; v4 = v4[~np.isnan(v4)]; n4 = int(v4.size)
        sig3 = float(np.std(v3, ddof=1)) if n3 >= 2 else np.nan
        sig4 = float(np.std(v4, ddof=1)) if n4 >= 2 else np.nan
        fe3 = sum10 / sig3 if (n3 >= SIG34_MIN and sig3 > 0 and not np.isnan(sum10)) else np.nan
        fe4 = ((sum600 / 61.0) / sig4
               if (n4 >= SIG34_MIN and sig4 > 0 and not np.isnan(sum600)) else np.nan)
        out.append((cats[c], fe3, fe4, n3, n4, sum10, sum600, sump160))

    fe34 = pd.DataFrame(out, columns=["obs_id", "fe3", "fe4", "n_days_sigma3",
                                      "n_days_sigma4", "car_m1_0", "car_m60_0", "car_p1_60"])
    t(f"Step 6: FE3/FE4 — {len(fe34):,} observations "
      f"(fe3 N={fe34['fe3'].notna().sum():,}, fe4 N={fe34['fe4'].notna().sum():,})", t0)
    return fe34


# =============================================================================
# Step 7 — FEP assignment with prior-quarter cutoffs (A14)
# Step 8 — size quintiles (A15)
# Step 9 — final panel
# =============================================================================
def steps7to9(obs_surv, fe12, fe34, t0) -> pd.DataFrame:
    master = obs_surv.merge(fe12[["gvkey", "qidx", "fe1", "fe2"]],
                            on=["gvkey", "qidx"], how="left")
    master = master.merge(fe34, on="obs_id", how="left")

    panel = master[master["qidx"] >= PANEL_Q0].copy()
    for m in range(1, 5):
        panel[f"fep{m}"] = np.nan
        fecol = f"fe{m}"
        for cq in range(CUTOFF_Q0, CUTOFF_Q1 + 1):
            src = master[(master["qidx"] == cq) & master[fecol].notna()]
            if src.empty:
                continue
            order = np.lexsort((src["obs_id"].to_numpy(), src[fecol].to_numpy()))
            vals = src[fecol].to_numpy()[order]
            n = len(vals)
            # 9 interior equal-frequency edges: max value within each of bins 1..9
            # (deterministic tie-split by (fe, obs_id) rank).
            edges = np.array([vals[int(np.ceil(k * n / N_FEP)) - 1] for k in range(1, N_FEP)])
            tgt = panel[(panel["qidx"] == cq + 1) & panel[fecol].notna()]
            if tgt.empty:
                continue
            fep = 1 + np.sum(edges[None, :] < tgt[fecol].to_numpy()[:, None], axis=1)
            panel.loc[tgt.index, f"fep{m}"] = np.clip(fep, 1, N_FEP)

    # A15: quintile = ceil(decile/2): I = deciles 1-2 ... V = deciles 9-10.
    panel["quintile"] = ((panel["decile"].astype(int) - 1) // 2 + 1).astype(int)
    panel = panel.sort_values(["gvkey", "qidx"]).reset_index(drop=True)
    cols = ["obs_id", "gvkey", "fyearq", "fqtr", "qlabel", "permno", "rdq", "day0", "Q",
            "fe1", "fe2", "fe3", "fe4", "fep1", "fep2", "fep3", "fep4",
            "decile", "quintile", "me_yearstart", "n_days_sigma3", "n_days_sigma4",
            "car_m1_0", "car_m60_0", "car_p1_60"]
    panel = panel[cols]
    out = LAYOUT.data_path("panel.parquet")
    panel.to_parquet(out, index=False)
    t(f"Step 9: panel — {len(panel):,} rows x {len(panel.columns)} cols -> {out.name}", t0)
    return panel


# =============================================================================
# Report
# =============================================================================
def report(panel, n_firms_s1, firms_s2_panel, earnings, t0):
    print("\n" + "=" * 78)
    print("PIPELINE REPORT — Foster, Olsen & Shevlin (1984)")
    print("=" * 78)

    print("\n1. Panel dimensions + columns")
    print(f"   rows x cols: {panel.shape[0]:,} x {panel.shape[1]}")
    print(f"   columns: {list(panel.columns)}")
    print(f"   quarters: {panel['qlabel'].nunique()} "
          f"({qidx_to_label(PANEL_Q0)}..{qidx_to_label(PANEL_Q1)}); "
          f"firms: {panel['gvkey'].nunique():,}; permnos: {panel['permno'].nunique():,}")

    print("\n2. Firm counts at each stage")
    print(f"   after Screen 1 (>=10 consecutive EPS quarters, A5): {n_firms_s1:,} (paper: 2,213)")
    print(f"   after CRSP-link Screen 2 (A6), with non-null rdq in 1974Q1-1981Q4: "
          f"{firms_s2_panel:,} (paper: 2,053)")
    print(f"   in final panel (decile assigned + day0 found, A7/A8): {panel['gvkey'].nunique():,}")

    print("\n3. Observations per quarter (32 quarters, 1974Q1-1981Q4)")
    pq = panel.groupby("qlabel").size()
    print(f"   min={pq.min():,}  max={pq.max():,}  mean={pq.mean():,.1f}  (paper: 1,495 / 1,978)")

    print("\n4. FE summary stats (panel observations)")
    print(f"   {'model':<7} {'N':>7} {'mean':>10} {'median':>10} {'std':>10}")
    for m in range(1, 5):
        s = panel[f"fe{m}"].dropna()
        print(f"   fe{m:<4} {len(s):>7,} {s.mean():>10.4f} {s.median():>10.4f} {s.std():>10.4f}")

    print("\n5. Unconditional FEP relative frequencies per model (Table 1 col-1 preview)")
    for m in range(1, 5):
        vc = panel[f"fep{m}"].value_counts(normalize=True).sort_index()
        fr = [f"{vc.get(float(k), 0.0):.3f}" for k in range(1, 11)]
        print(f"   Model {m}: N={panel[f'fep{m}'].notna().sum():,}  "
              f"min={vc.min():.3f} max={vc.max():.3f}  [{' '.join(fr)}]")

    print("\n7. Median fe1..fe4 within FEP for Model 2's own portfolios (Table 2 preview)")
    g2 = panel.dropna(subset=["fep2"]).groupby("fep2")[["fe1", "fe2", "fe3", "fe4"]].median()
    with pd.option_context("display.float_format", lambda v: f"{v:8.3f}"):
        print(g2.to_string())
    print("   (paper: FEP1 median FE2 = -2.244, FEP10 median FE2 = 3.151)")

    print("\n8. Files produced")
    for f in ["cache/decile_returns.parquet", "cache/event_returns.parquet", "panel.parquet"]:
        p = Path(LAYOUT.data_path(f))
        print(f"   {p}  ({p.stat().st_size / 1e6:,.1f} MB)")
    print("=" * 78, flush=True)


def main():
    t0 = time.time()
    print(f"Earnings-releases-anomalies pipeline — {time.strftime('%Y-%m-%d %H:%M:%S')}")
    earnings, n_firms_s1 = step1_earnings(t0)
    fe12 = step2_fe12(earnings, t0)
    obs_linked, sample = step3_link_and_daily(earnings, t0)
    membership, decile_returns, edges = step4_deciles(t0)
    obs_surv = step5_event_returns(obs_linked, sample, decile_returns, edges, t0)
    del sample, membership, decile_returns, edges
    fe34 = step6_fe34(t0)
    panel = steps7to9(obs_surv, fe12, fe34, t0)
    firms_s2_panel = int(obs_linked.loc[obs_linked["qidx"] >= PANEL_Q0, "gvkey"].nunique())
    report(panel, n_firms_s1, firms_s2_panel, earnings, t0)
    print(f"\nTotal runtime: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
