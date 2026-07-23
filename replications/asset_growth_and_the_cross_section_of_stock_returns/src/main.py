"""
Replication of Cooper, Gulen, Schill (2008) "Asset Growth and the Cross-Section
of Stock Returns" (Journal of Finance).

FOUNDATION DATA-PIPELINE TASK.
Builds the analysis-ready data only (no Table I/II/III/IV results yet):
    data/formation.parquet  -- one row per (permno, june_year), all formation
                               variables + decile + size_group.
    data/panel.parquet      -- one row per (permno, month), Jul-1968..Jun-2003,
                               delisting-adjusted monthly return + ME + decile.

Timing conventions (paper rules, L87):
  * Accounting variables formed at END OF JUNE of year t using Compustat fiscal
    year t-1 (Fama-French 1992 lag). Portfolios sorted end of June t on ASSETG,
    held July t .. June t+1, rebalanced annually.
  * ASSETG(t) = (at[FY t-1] - at[FY t-2]) / at[FY t-2]; require at>0 in both
    FY t-1 and FY t-2 (rule sample_assetg_nonzero_assets).
  * MV = CRSP market equity at end of June t.
  * BM denominator = CRSP market equity at end of December t-1 (Assumption 2);
    numerator = Davis-Fama-French (2000) book equity at FY t-1.

ClickHouse Date clamps pre-1970 dates to the epoch, so all dates are pulled as
ISO strings from SQL and parsed here (pandas datetime64 handles the 1960s).
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

# --- repo / layout -----------------------------------------------------------
# parents[3] is the rep-it-up project root (the directory carrying utils/):
#   src/main.py -> [0] src -> [1] <slug> -> [2] replications -> [3] rep-it-up.
# (The previous parents[2] resolved to rep-it-up/replications — audit issue m2.)
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
# Pin the replications root so paper_layout() is cwd-independent; otherwise
# utils.env.get_replications_path() falls back to <cwd>/replications and, when
# main.py is run from inside the slug, LAYOUT.ensure() creates a nested orphan
# tree <slug>/replications/<slug>/{data,src,...} (audit issue m2).
os.environ.setdefault("REPLICATIONS_PATH", str(REPO / "replications"))
from utils.env import get_clickhouse_config          # noqa: E402
from utils.paths import paper_layout                 # noqa: E402
from utils.quantile import assign_quantiles          # noqa: E402

SLUG = "asset_growth_and_the_cross_section_of_stock_returns"
LAYOUT = paper_layout(SLUG)
LAYOUT.ensure()
SQL_DIR = LAYOUT.src_path("sql")

# --- configuration (paper sample; NOT the paper's reported RESULTS) ----------
N_DECILES = 10
FIRST_FORMATION = 1968          # rule sample_start_1968 (portfolio tests start Jun-1968)
LAST_FORMATION = 2002           # last June sort whose portfolio ends Jun-2003
FORMATION_YEARS = list(range(FIRST_FORMATION, LAST_FORMATION + 1))  # 1968..2002 (35)
PANEL_START = "1968-07-01"
PANEL_END = "2003-06-30"
BACKFILL_YEARS = 2              # rule sample_backfill_2yr

_CFG = get_clickhouse_config()


def _client() -> Client:
    return Client(host=_CFG["host"], port=int(_CFG["port"]),
                  user=_CFG["user"], password=_CFG["password"],
                  database=_CFG["database"], settings={"max_execution_time": 900})


def q(sql: str) -> pd.DataFrame:
    c = _client()
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def q_file(name: str) -> pd.DataFrame:
    return q((SQL_DIR / name).read_text())


# =============================================================================
# 1. LOAD (SQL does universe filtering, funda dedup, ME aggregation)
# =============================================================================
def load() -> dict[str, pd.DataFrame]:
    t0 = time.time()
    fund = q_file("comp_fundamentals.sql")
    link = q_file("crsp_comp_link.sql")
    msf = q_file("universe_monthly.sql")
    delist = q_file("delisting.sql")
    ff = q_file("ff_factors.sql")
    print(f"[load] {time.time()-t0:.1f}s | fund {fund.shape} msf {msf.shape} "
          f"link {link.shape} delist {delist.shape} ff {ff.shape}")

    # parse ISO-string dates in pandas (handles pre-1970, unlike ClickHouse Date)
    fund["datadate"] = pd.to_datetime(fund["datadate"])
    fund["first_datadate"] = pd.to_datetime(fund["first_datadate"])
    link["linkdt"] = pd.to_datetime(link["linkdt"])
    link["linkenddt"] = pd.to_datetime(link["linkenddt"])
    msf["date"] = pd.to_datetime(msf["date"])
    delist["dlstdt"] = pd.to_datetime(delist["dlstdt"])
    ff["month"] = pd.to_datetime(ff["month"])
    return {"fund": fund, "link": link, "msf": msf, "delist": delist, "ff": ff}


# =============================================================================
# 2. DELISTING-ADJUSTED MONTHLY RETURNS (Assumption 1)
# =============================================================================
def adjust_delistings(msf: pd.DataFrame, delist: pd.DataFrame) -> pd.DataFrame:
    """Combine each delisting return with the holding return in the delisting
    month: (1+ret)*(1+dlret)-1. Missing dlret -> -0.30 if dlstcd 500..599 else 0.
    Also synthesize a return for delisting months that have no msf record (so the
    delisting return is not lost)."""
    msf = msf.copy()
    # CRSP monthly return sentinels are < -1; legitimate range is [-1, inf).
    msf["ret"] = msf["ret"].where(msf["ret"] >= -1.0)
    msf["ym"] = msf["date"].dt.to_period("M")

    dl = delist.copy()
    dl["ym"] = dl["dlstdt"].dt.to_period("M")
    dl["dlret_clean"] = dl["dlret"].where(dl["dlret"] >= -1.0)
    dl["eff_dlret"] = dl["dlret_clean"]
    miss = dl["eff_dlret"].isna()
    perf = dl["dlstcd"].between(500, 599)
    dl.loc[miss & perf, "eff_dlret"] = -0.30
    dl.loc[miss & ~perf, "eff_dlret"] = 0.0
    dl = dl[["permno", "ym", "eff_dlret", "dlstdt"]].drop_duplicates(
        subset=["permno", "ym"], keep="first")

    # (a) adjust msf rows that coincide with a delisting month
    m = msf.merge(dl[["permno", "ym", "eff_dlret"]], on=["permno", "ym"], how="left")
    has_dl = m["eff_dlret"].notna()
    m["ret_adj"] = np.where(has_dl,
                            (1.0 + m["ret"].fillna(0.0)) * (1.0 + m["eff_dlret"]) - 1.0,
                            m["ret"])

    # (b) delisting events with NO msf record that month -> synthetic row
    msf_keys = msf[["permno", "ym"]].drop_duplicates()
    dl_un = dl.merge(msf_keys, on=["permno", "ym"], how="left", indicator=True)
    dl_un = dl_un[dl_un["_merge"] == "left_only"]
    if len(dl_un):
        last = (msf.sort_values(["permno", "date"])
                    .groupby("permno")
                    .agg(me=("me", "last"), hexcd=("hexcd", "last"))
                    .reset_index())
        dl_un = dl_un.merge(last, on="permno", how="left")
        synth = pd.DataFrame({
            "permno": dl_un["permno"].values,
            "date": dl_un["dlstdt"].values,
            "ret": np.nan,
            "prc": np.nan,
            "me": dl_un["me"].values,
            "hexcd": dl_un["hexcd"].values,
            "ym": dl_un["ym"].values,
            "ret_adj": dl_un["eff_dlret"].values,
            "eff_dlret": dl_un["eff_dlret"].values,
        })
        m = pd.concat([m, synth[m.columns.intersection(synth.columns)]], ignore_index=True)
        print(f"[delist] adjusted {int(has_dl.sum())} matched months; "
              f"synthesized {len(synth)} delisting months without an msf record")
    else:
        print(f"[delist] adjusted {int(has_dl.sum())} matched months; 0 synthesized")
    return m


# =============================================================================
# 3. COMPUSTAT VARIABLES (per gvkey, june_year) -- ASSETG + controls + extras
# =============================================================================
def _lag_merge(base: pd.DataFrame, fund: pd.DataFrame, items, offset, suffix):
    """Attach funda `items` from fyear = base.fyear - offset (renamed +suffix)."""
    r = fund[["gvkey", "fyear"] + items].copy()
    r["fyear"] = r["fyear"] + offset
    r = r.rename(columns={c: c + suffix for c in items})
    return base.merge(r, on=["gvkey", "fyear"], how="left")


def build_fundamentals(fund: pd.DataFrame) -> pd.DataFrame:
    f = fund
    items_all = ["at", "sale", "ceq", "seq", "txdb", "pstkrv", "pstkl", "pstk",
                 "act", "ch", "lct", "dlc", "dltt", "dp", "txp", "capx", "oibdp",
                 "csho", "prcc_f", "ppegt", "re", "mib", "epspx", "epsfi", "lt", "che"]
    base = f[["gvkey", "fyear", "first_datadate"] + items_all].copy()
    base["june_year"] = base["fyear"] + 1   # FY f used at the June of f+1

    base = _lag_merge(base, f, ["at", "sale", "act", "ch", "lct", "dlc", "txp",
                                "ppegt", "re", "pstk", "ceq", "mib", "dltt", "capx"],
                      1, "_t2")   # FY t-2
    base = _lag_merge(base, f, ["at", "capx", "sale"], 2, "_t3")   # FY t-3
    base = _lag_merge(base, f, ["capx", "sale"], 3, "_t4")          # FY t-4
    base = _lag_merge(base, f, ["csho"], 4, "_t5")                  # FY t-5

    at1, at2, at3 = base["at"], base["at_t2"], base["at_t3"]

    # --- core signal ---------------------------------------------------------
    base["ASSETG"] = np.where((at1 > 0) & (at2 > 0), (at1 - at2) / at2, np.nan)
    base["L2ASSETG"] = np.where((at2 > 0) & (at3 > 0), (at2 - at3) / at3, np.nan)
    base["ASSETS"] = at1                                   # total assets FY t-1, $M

    # --- accounting controls (all FY t-1 unless noted) -----------------------
    eps = base["epspx"].fillna(base["epsfi"])
    base["EP"] = np.where(base["prcc_f"] > 0, eps / base["prcc_f"], np.nan)
    base["Leverage"] = np.where(at1 > 0,
                                (base["dltt"].fillna(0) + base["dlc"].fillna(0)) / at1,
                                np.nan)
    base["ROA"] = np.where(at1 > 0, base["oibdp"] / at1, np.nan)
    base["SALESG"] = np.where((base["sale"] > 0) & (base["sale_t2"] > 0),
                              (base["sale"] - base["sale_t2"]) / base["sale_t2"], np.nan)

    # book equity (Davis-Fama-French 2000), FY t-1
    pstk_pref = base["pstkrv"].fillna(base["pstkl"]).fillna(base["pstk"]).fillna(0)
    txdb = base["txdb"].fillna(0)
    be_seq = base["seq"] + txdb - pstk_pref
    be_ceq = base["ceq"] + txdb - pstk_pref
    be_at = at1 - base["dlc"].fillna(0) - base["dltt"].fillna(0) - pstk_pref
    base["be"] = be_seq.where(be_seq.notna(), be_ceq.where(be_ceq.notna(), be_at))

    # ACCRUALS (rule var_accruals): deltas FY t-2 -> FY t-1, scaled by avg assets
    d_act = base["act"] - base["act_t2"]
    d_ch = base["ch"] - base["ch_t2"]
    d_lct = base["lct"] - base["lct_t2"]
    d_dlc = base["dlc"] - base["dlc_t2"]
    d_txp = base["txp"] - base["txp_t2"]
    avg_at = (at1 + at2) / 2.0
    accr_num = (d_act - d_ch) - (d_lct - d_dlc - d_txp) - base["dp"]
    base["ACCRUALS"] = np.where(avg_at > 0, accr_num / avg_at, np.nan)

    # ISSUANCE (Table I): 5-year % change in shares outstanding
    base["ISSUANCE"] = np.where(base["csho_t5"] > 0,
                                (base["csho"] - base["csho_t5"]) / base["csho_t5"], np.nan)

    # --- Table III extra: abnormal capital investment (Titman-Wei-Xie 2004) --
    ce1 = base["capx"] / base["sale"]
    ce2 = base["capx_t2"] / base["sale_t2"]
    ce3 = base["capx_t3"] / base["sale_t3"]
    ce4 = base["capx_t4"] / base["sale_t4"]
    avg_ce = (ce2 + ce3 + ce4) / 3.0
    base["CI"] = ce1 / avg_ce - 1.0

    # --- Table IV extras: balance-sheet decomposition (scaled by AT FY t-2) --
    inv = at2 > 0
    d_at = (at1 - at2) / at2
    d_cash = (base["ch"] - base["ch_t2"]) / at2
    d_curasst = ((base["act"] - base["ch"]) - (base["act_t2"] - base["ch_t2"])) / at2
    d_ppe = (base["ppegt"] - base["ppegt_t2"]) / at2
    base["d_cash"] = np.where(inv, d_cash, np.nan)
    base["d_curasst"] = np.where(inv, d_curasst, np.nan)
    base["d_ppe"] = np.where(inv, d_ppe, np.nan)
    base["d_othassets"] = np.where(inv, d_at - d_cash - d_curasst - d_ppe, np.nan)

    stk1 = (base["pstk"].fillna(0) + base["ceq"].fillna(0)
            + base["mib"].fillna(0) - base["re"].fillna(0))
    stk2 = (base["pstk_t2"].fillna(0) + base["ceq_t2"].fillna(0)
            + base["mib_t2"].fillna(0) - base["re_t2"].fillna(0))
    d_re = (base["re"] - base["re_t2"]) / at2
    d_stock = (stk1 - stk2) / at2
    d_debt = ((base["dltt"].fillna(0) + base["dlc"].fillna(0))
              - (base["dltt_t2"].fillna(0) + base["dlc_t2"].fillna(0))) / at2
    base["d_re"] = np.where(inv, d_re, np.nan)
    base["d_stock"] = np.where(inv, d_stock, np.nan)
    base["d_debt"] = np.where(inv, d_debt, np.nan)
    base["d_opliab"] = np.where(inv, d_at - d_re - d_stock - d_debt, np.nan)

    return base


# =============================================================================
# 4. CRSP FORMATION CROSS-SECTIONS (June MV, December ME, buy-and-hold returns)
# =============================================================================
def june_and_dec_cross_sections(msf: pd.DataFrame):
    msf = msf.copy()
    msf["year"] = msf["date"].dt.year
    msf["month"] = msf["date"].dt.month

    june = msf[msf["month"] == 6][["permno", "year", "me", "hexcd", "prc"]].copy()
    june = june.rename(columns={"year": "june_year"})
    june["MV"] = june["me"] / 1e6                      # $MILLIONS (rule var_mv)
    june = june.drop_duplicates(subset=["permno", "june_year"], keep="last")

    dec = msf[msf["month"] == 12][["permno", "year", "me"]].copy()
    dec = dec.rename(columns={"year": "dec_year"})
    dec["me_dec"] = dec["me"] / 1e6                    # $MILLIONS (Assumption 2)
    dec["june_year"] = dec["dec_year"] + 1             # Dec t-1 -> June t
    dec = dec[["permno", "june_year", "me_dec"]].drop_duplicates(
        subset=["permno", "june_year"], keep="last")
    return june, dec


def buy_and_hold_returns(msf: pd.DataFrame):
    """BHRET6 = prod(1+r)-1 over Jan..Jun of year t (all 6 months required).
    BHRET36 = prod(1+r)-1 over Jul(t-3)..Jun(t) (all 36 months required)."""
    msf = msf.copy()
    msf["year"] = msf["date"].dt.year
    msf["month"] = msf["date"].dt.month
    r = msf["ret_adj"].where(msf["ret_adj"] >= -1.0)

    # BHRET6 (within-year Jan..Jun)
    h1 = msf[r.notna() & msf["month"].between(1, 6)].copy()
    with np.errstate(divide="ignore", invalid="ignore"):   # log1p(-1) = -inf -> BHRET -1
        h1["log1p"] = np.log1p(h1["ret_adj"])
    cnt6 = h1.groupby(["permno", "year"])["log1p"].count()
    sum6 = h1.groupby(["permno", "year"])["log1p"].sum()
    bh6 = (np.exp(sum6) - 1.0).rename("BHRET6")
    bh6 = bh6[cnt6 >= 6].reset_index().rename(columns={"year": "june_year"})

    # BHRET36 (rolling 36 calendar months ending Jun t)
    ym_index = pd.period_range("1965-01", "2003-12", freq="M")
    wide = (msf.drop_duplicates(["permno", "ym"])
               .pivot_table(index="ym", columns="permno", values="ret_adj", aggfunc="first")
               .reindex(ym_index))
    with np.errstate(divide="ignore", invalid="ignore"):
        roll = np.log1p(wide).rolling(36, min_periods=36).sum()
    bh36_wide = np.exp(roll) - 1.0
    june_periods = {pd.Period(f"{t}-06", freq="M"): t for t in FORMATION_YEARS}
    rows = bh36_wide.loc[list(june_periods.keys())].copy()
    rows.index = pd.Index([june_periods[p] for p in rows.index], name="june_year")
    bh36 = (rows.reset_index()
                .melt(id_vars="june_year", var_name="permno", value_name="BHRET36")
                .dropna(subset=["BHRET36"]))
    return bh6, bh36


# =============================================================================
# 5. ASSEMBLE FORMATION TABLE
# =============================================================================
def assemble_formation(fund, link, june, dec, bh6, bh36):
    # June cross-section restricted to formation years
    june_f = june[june["june_year"].isin(FORMATION_YEARS)].copy()
    june_f["june_date"] = june_f["june_year"].map(
        lambda t: pd.Timestamp(f"{t}-06-30"))

    # point-in-time CRSP->Compustat link at June t
    m = june_f.merge(link, on="permno", how="left")
    m = m[(m["june_date"] >= m["linkdt"]) & (m["june_date"] <= m["linkenddt"])]
    m = (m.sort_values("linkdt")
            .drop_duplicates(subset=["permno", "june_year"], keep="last"))

    # attach Compustat variables
    base = build_fundamentals(fund)
    keep = ["gvkey", "june_year", "first_datadate",
            "ASSETG", "L2ASSETG", "ASSETS", "EP", "Leverage", "ROA", "SALESG",
            "be", "ACCRUALS", "ISSUANCE", "CI",
            "d_cash", "d_curasst", "d_ppe", "d_othassets",
            "d_re", "d_stock", "d_debt", "d_opliab"]
    form = m.merge(base[keep], on=["gvkey", "june_year"], how="left")

    # attach CRSP price-based pieces
    form = form.merge(dec, on=["permno", "june_year"], how="left")
    form = form.merge(bh6, on=["permno", "june_year"], how="left")
    form = form.merge(bh36, on=["permno", "june_year"], how="left")
    form["BM"] = np.where(form["me_dec"] > 0, form["be"] / form["me_dec"], np.nan)

    # --- sample filters ------------------------------------------------------
    # 2-year Compustat backfill: earliest funda datadate <= (June t minus 2y)
    form["backfill_cutoff"] = form["june_year"].map(
        lambda t: pd.Timestamp(f"{t - BACKFILL_YEARS}-06-30"))
    pass_backfill = form["first_datadate"] <= form["backfill_cutoff"]
    valid_assetg = form["ASSETG"].notna()
    n_before = len(form)
    form = form[pass_backfill & valid_assetg].copy()
    print(f"[formation] {n_before} linked firm-years -> {len(form)} after "
          f"2yr-backfill + nonzero-assets ASSETG filter")

    # --- decile (full cross-section, Assumption 6) ---------------------------
    form["decile"] = assign_quantiles(form, "june_year", "ASSETG",
                                      n_bins=N_DECILES, warn_fallback=False)

    # --- size group (NYSE 30th/70th MV percentiles, Assumption 4) ------------
    nyse = june_f[june_f["hexcd"] == 1]
    bp = nyse.groupby("june_year")["MV"].quantile([0.30, 0.70]).unstack()
    form["size_group"] = np.select(
        [form["MV"] < form["june_year"].map(bp[0.30]),
         form["MV"] > form["june_year"].map(bp[0.70])],
        ["small", "large"], default="medium")
    return form


# =============================================================================
# 6. ASSEMBLE MONTHLY PANEL
# =============================================================================
def assemble_panel(msf_adj: pd.DataFrame, form: pd.DataFrame) -> pd.DataFrame:
    p = msf_adj[(msf_adj["date"] >= PANEL_START) & (msf_adj["date"] <= PANEL_END)].copy()
    p["formation_year"] = np.where(p["date"].dt.month >= 7,
                                   p["date"].dt.year, p["date"].dt.year - 1)
    p = p[["permno", "date", "ret_adj", "me", "formation_year"]].copy()
    assign = (form[["permno", "june_year", "decile", "size_group"]]
              .rename(columns={"june_year": "formation_year"})
              .drop_duplicates(subset=["permno", "formation_year"]))
    panel = p.merge(assign, on=["permno", "formation_year"], how="inner")
    panel = panel.rename(columns={"date": "month", "ret_adj": "ret"})
    panel = panel[["permno", "month", "ret", "me", "formation_year", "decile", "size_group"]]
    panel["decile"] = panel["decile"].astype(int)
    return panel.sort_values(["permno", "month"]).reset_index(drop=True)


# =============================================================================
# 7. DIAGNOSTICS (reported back to the Replicator)
# =============================================================================
def ts_avg_cs_median(df, col):
    cs = df.groupby(["june_year", "decile"])[col].median()
    return cs.groupby("decile").mean()


def diagnose(form: pd.DataFrame, panel: pd.DataFrame):
    print("\n" + "=" * 70)
    print("DIAGNOSTICS")
    print("=" * 70)
    print(f"formation.parquet: {form.shape[0]} rows x {form.shape[1]} cols")
    print(f"  columns: {list(form.columns)}")
    print(f"panel.parquet:     {panel.shape[0]} rows x {panel.shape[1]} cols")
    print(f"  columns: {list(panel.columns)}")

    fy = sorted(form["june_year"].unique())
    print(f"\nformation years: {fy[0]}..{fy[-1]}  (n={len(fy)})")
    print(f"panel months: {panel['month'].min().date()} .. {panel['month'].max().date()} "
          f"({panel['month'].nunique()} months, {panel['permno'].nunique()} permnos)")

    per_year = form.groupby("june_year").size()
    print(f"\navg stocks / formation year: {per_year.mean():.1f}")
    print(f"  1990: {per_year.get(1990, 'NA')}   2000: {per_year.get(2000, 'NA')}")
    print(f"  min/max year count: {per_year.min()} ({per_year.idxmin()}) / "
          f"{per_year.max()} ({per_year.idxmax()})")

    print("\nASSETG time-series-avg cross-sectional MEDIAN by decile "
          "(paper D1=-0.2115 D5=0.0961 D10=0.8357):")
    ag = ts_avg_cs_median(form, "ASSETG")
    for d in (1, 5, 10):
        print(f"  D{d}: {ag.get(d, np.nan):.4f}")

    print("\nMV (June, $M) TS-avg cross-sectional MEDIAN by decile "
          "(paper D1=15.7 D10=85.6):")
    mv = ts_avg_cs_median(form, "MV")
    for d in (1, 10):
        print(f"  D{d}: {mv.get(d, np.nan):.2f}")

    print("\nBM TS-avg cross-sectional MEDIAN by decile (paper D1=0.8156 D10=0.4256):")
    bm = ts_avg_cs_median(form, "BM")
    for d in (1, 10):
        print(f"  D{d}: {bm.get(d, np.nan):.4f}")

    a = form["ASSETG"]
    print(f"\nASSETG overall: mean={a.mean():.4f} median={a.median():.4f} "
          f"std={a.std():.4f} null%={round(a.isna().mean()*100, 2)}")

    print("\ncontrol null% (formation):")
    for c in ["ASSETG", "L2ASSETG", "ASSETS", "MV", "BM", "EP", "Leverage",
              "ROA", "BHRET6", "BHRET36", "ACCRUALS", "ISSUANCE", "be", "me_dec",
              "SALESG", "CI"]:
        print(f"  {c:10s}: {round(form[c].isna().mean()*100, 1)}%")

    print("\nsize_group distribution:")
    print(form["size_group"].value_counts().to_string())


# =============================================================================
def main():
    data = load()
    msf_adj = adjust_delistings(data["msf"], data["delist"])
    june, dec = june_and_dec_cross_sections(msf_adj)
    bh6, bh36 = buy_and_hold_returns(msf_adj)
    form = assemble_formation(data["fund"], data["link"], june, dec, bh6, bh36)

    # --- write formation.parquet ---
    formation_cols = ["permno", "june_year", "ASSETG", "L2ASSETG", "ASSETS", "MV",
                      "BM", "EP", "Leverage", "ROA", "BHRET6", "BHRET36",
                      "ACCRUALS", "ISSUANCE", "decile", "size_group", "be", "me_dec"]
    extra_cols = ["SALESG", "CI", "d_cash", "d_curasst", "d_ppe", "d_othassets",
                  "d_re", "d_stock", "d_debt", "d_opliab"]
    form_out = form[formation_cols + extra_cols].copy()
    form_out["decile"] = form_out["decile"].astype(int)
    form_out = form_out.sort_values(["june_year", "permno"]).reset_index(drop=True)
    form_out.to_parquet(LAYOUT.data_path("formation.parquet"), index=False)
    print(f"\n[write] {LAYOUT.data_path('formation.parquet')}  {form_out.shape}")

    # --- write panel.parquet ---
    panel = assemble_panel(msf_adj, form)
    panel.to_parquet(LAYOUT.data_path("panel.parquet"), index=False)
    print(f"[write] {LAYOUT.data_path('panel.parquet')}  {panel.shape}")

    diagnose(form_out, panel)


if __name__ == "__main__":
    main()
