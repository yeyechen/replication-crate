"""
SAAR diagnostic for LSV (1994) — REPORT ONLY (writes no results/*.md or *.json,
changes no defaults).

Tests the alternative A5 reading: size-decile benchmark REASSIGNED each December
inside the holding window (holding year k of formation t uses the decile from the
December (t+k-2) ME ranking of the then-universe), vs the FIXED formation-time
assignment used by sortlib/tables. Reports a before/after table (paper | fixed |
reassigned) for the 11 failing near-zero SAAR cells + 6 headline corner cells.

R_k (the sort portfolio's own return) is identical under both variants; only the
size benchmark B_k changes. Both variants here use the SAME monthly-return series
so the comparison isolates the decile-assignment effect.

Run: cd repo-root && uv run python replications/contrarian_investment/src/saar_diagnostic.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from clickhouse_driver import Client  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

load_dotenv(REPO_ROOT / ".env")
from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402
import sortlib as S  # noqa: E402

LAYOUT = paper_layout("contrarian_investment",
                      replications_root=REPO_ROOT / "replications")
RES = LAYOUT.results_dir
SIG = {"bm": "bm", "cp": "cp", "ep": "ep", "gs": "gs_rank_frac"}


def vmask(df, var):
    return {"bm": (df["be_valid"] == 1) & df["bm"].notna(),
            "cp": df["cp_pos"] == 1, "ep": df["ep_pos"] == 1,
            "gs": df["gs_rank_frac"].notna()}[var]


def decile_on(univ: pd.DataFrame, var: str) -> pd.Series:
    """decile (Int64, NaN outside univ) aligned to univ.index, full-panel idx."""
    dec = pd.Series(pd.NA, index=univ.index, dtype="Int64")
    for _, idx in univ.groupby("fy").groups.items():
        ii = idx[vmask(univ, var).loc[idx]]
        if len(ii) >= 10:
            dec.loc[ii] = S.assign_deciles(univ.loc[ii, SIG[var]], 10)
    return dec


def groups_on(univ: pd.DataFrame, var: str) -> pd.Series:
    g = pd.Series(pd.NA, index=univ.index, dtype="Int64")
    for _, idx in univ.groupby("fy").groups.items():
        ii = idx[vmask(univ, var).loc[idx]]
        if len(ii):
            g.loc[ii] = S.assign_304030(univ.loc[ii, SIG[var]])
    return g


# --- cell catalogue --------------------------------------------------------
# each: (report_label, json_file, metric_name, mask_builder(panel, subsample))
def dec_mask(var, d):
    def f(panel, sub):
        dec = decile_on(panel, var)
        return (dec == d).fillna(False).astype(bool)
    return f


def cell_mask(v1, a, v2, b, use_sub):
    def f(panel, sub):
        u = sub if use_sub else panel
        g1 = groups_on(u, v1)
        g2 = groups_on(u, v2)
        cond = ((g1 == a) & (g2 == b)).fillna(False).astype(bool)
        m = pd.Series(False, index=panel.index)
        m.loc[u.index] = cond.loc[u.index]
        return m
    return f


CELLS = [
    # --- 11 failing near-zero cells ---
    ("T1  GS  D1",        "I",   "Panel D (GS) decile 1 SAAR",            dec_mask("gs", 1)),
    ("T1  GS  D7",        "I",   "Panel D (GS) decile 7 SAAR",            dec_mask("gs", 7)),
    ("T1  GS  D8",        "I",   "Panel D (GS) decile 8 SAAR",            dec_mask("gs", 8)),
    ("T2A (C/P1,GS1)",    "II",  "Panel A (C/PxGS) cell (C/P1,GS1) SAAR", cell_mask("cp", 1, "gs", 1, False)),
    ("T2B (E/P1,GS1)",    "II",  "Panel B (E/PxGS) cell (E/P1,GS1) SAAR", cell_mask("ep", 1, "gs", 1, False)),
    ("T2C (B/M1,GS1)",    "II",  "Panel C (B/MxGS) cell (B/M1,GS1) SAAR", cell_mask("bm", 1, "gs", 1, False)),
    ("T2C (B/M2,GS3)",    "II",  "Panel C (B/MxGS) cell (B/M2,GS3) SAAR", cell_mask("bm", 2, "gs", 3, False)),
    ("T2E (B/M1,C/P3)",   "II",  "Panel E (B/MxC/P) cell (B/M1,C/P3) SAAR", cell_mask("bm", 1, "cp", 3, False)),
    ("T3A (C/P3,GS3)",    "III", "Panel A (C/PxGS) cell (C/P3,GS3) SAAR", cell_mask("cp", 3, "gs", 3, True)),
    ("T3B (E/P3,GS2)",    "III", "Panel B (E/PxGS) cell (E/P3,GS2) SAAR", cell_mask("ep", 3, "gs", 2, True)),
    ("T3E (B/M2,C/P3)",   "III", "Panel E (B/MxC/P) cell (B/M2,C/P3) SAAR", cell_mask("bm", 2, "cp", 3, True)),
    # --- 6 headline corner cells ---
    ("T1  B/M D1",        "I",   "Panel A (B/M) decile 1 SAAR",           dec_mask("bm", 1)),
    ("T1  B/M D10",       "I",   "Panel A (B/M) decile 10 SAAR",          dec_mask("bm", 10)),
    ("T2A glam (1,3)",    "II",  "Panel A (C/PxGS) cell (C/P1,GS3) SAAR", cell_mask("cp", 1, "gs", 3, False)),
    ("T2A value(3,1)",    "II",  "Panel A (C/PxGS) cell (C/P3,GS1) SAAR", cell_mask("cp", 3, "gs", 1, False)),
    ("T3A glam (1,3)",    "III", "Panel A (C/PxGS) cell (C/P1,GS3) SAAR", cell_mask("cp", 1, "gs", 3, True)),
    ("T3A value(3,1)",    "III", "Panel A (C/PxGS) cell (C/P3,GS1) SAAR", cell_mask("cp", 3, "gs", 1, True)),
]

JSONF = {"I": "table_I_cells.json", "II": "table_II_cells.json",
         "III": "table_III_cells.json"}


# --- SQL: extended December rankings + decile EW monthly returns -----------
EXT_DEC_SQL = """
WITH dec_dates AS (
    SELECT toUInt32(substring(date, 1, 4)) AS D, max(date) AS dec_date
    FROM crsp_202601.msf
    WHERE substring(date, 6, 2) = '12' AND date >= '1967-12-01' AND date <= '1992-12-31'
    GROUP BY substring(date, 1, 4)
),
dec_univ AS (
    SELECT DISTINCT d.D AS D, d.dec_date AS dec_date, n.permno AS permno
    FROM crsp_202601.dsenames AS n CROSS JOIN dec_dates AS d
    WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2) AND n.permno IS NOT NULL
      AND n.namedt <= '1992-12-31' AND ifNull(n.nameendt, '2100-01-01') >= '1967-01-01'
      AND n.namedt <= d.dec_date AND ifNull(n.nameendt, '2100-01-01') >= d.dec_date
),
dec_me AS (
    SELECT u.D AS D, u.permno AS permno, abs(m.prc) * m.shrout * 1000 AS me
    FROM dec_univ AS u
    INNER JOIN crsp_202601.msf AS m ON m.permno = u.permno AND m.date = u.dec_date
    WHERE m.date >= '1967-12-01' AND m.date <= '1992-12-31'
      AND abs(m.prc) * m.shrout * 1000 > 0
)
SELECT D, permno,
       ntile(10) OVER (PARTITION BY D ORDER BY me ASC) AS decile
FROM dec_me
SETTINGS max_execution_time = 300, max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
"""

EW_SQL = """
WITH dec_dates AS (
    SELECT toUInt32(substring(date, 1, 4)) AS D, max(date) AS dec_date
    FROM crsp_202601.msf
    WHERE substring(date, 6, 2) = '12' AND date >= '1967-12-01' AND date <= '1992-12-31'
    GROUP BY substring(date, 1, 4)
),
dec_univ AS (
    SELECT DISTINCT d.D AS D, d.dec_date AS dec_date, n.permno AS permno
    FROM crsp_202601.dsenames AS n CROSS JOIN dec_dates AS d
    WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2) AND n.permno IS NOT NULL
      AND n.namedt <= '1992-12-31' AND ifNull(n.nameendt, '2100-01-01') >= '1967-01-01'
      AND n.namedt <= d.dec_date AND ifNull(n.nameendt, '2100-01-01') >= d.dec_date
),
dec_me AS (
    SELECT u.D AS D, u.permno AS permno, abs(m.prc) * m.shrout * 1000 AS me
    FROM dec_univ AS u
    INNER JOIN crsp_202601.msf AS m ON m.permno = u.permno AND m.date = u.dec_date
    WHERE m.date >= '1967-12-01' AND m.date <= '1992-12-31'
      AND abs(m.prc) * m.shrout * 1000 > 0
),
ext_dec AS (
    SELECT D, permno, ntile(10) OVER (PARTITION BY D ORDER BY me ASC) AS decile
    FROM dec_me
),
univ_permno AS (SELECT DISTINCT permno FROM ext_dec),
msf_u AS (
    SELECT m.permno AS permno,
        toUInt32(substring(m.date, 1, 4)) * 12 + toUInt32(substring(m.date, 6, 2)) AS mnum,
        if(m.ret IS NOT NULL AND m.ret >= -1.0, m.ret, NULL) AS clean_ret
    FROM crsp_202601.msf AS m
    INNER JOIN univ_permno AS u ON u.permno = m.permno
    WHERE m.date >= '1968-05-01' AND m.date <= '1994-04-30'
),
delist AS (
    SELECT e.permno AS permno,
        toUInt32(substring(e.dlstdt, 1, 4)) * 12 + toUInt32(substring(e.dlstdt, 6, 2)) AS dl_mnum,
        if(e.dlret IS NOT NULL AND e.dlret >= -1.0, e.dlret, NULL) AS clean_dlret
    FROM crsp_202601.dsedelist AS e
    INNER JOIN univ_permno AS u ON u.permno = e.permno
    WHERE e.dlstdt >= '1968-05-01' AND e.dlstdt <= '1994-04-30' AND e.dlstdt IS NOT NULL
),
present_msf AS (
    SELECT m.permno AS permno, m.mnum AS mnum,
        coalesce(m.clean_ret, d.clean_dlret, 0) AS ret
    FROM msf_u AS m LEFT JOIN delist AS d ON d.permno = m.permno AND d.dl_mnum = m.mnum
),
msf_months AS (SELECT DISTINCT permno, mnum FROM msf_u),
delist_only AS (
    SELECT d.permno AS permno, d.dl_mnum AS mnum, coalesce(d.clean_dlret, 0) AS ret
    FROM delist AS d LEFT JOIN msf_months AS mm ON mm.permno = d.permno AND mm.mnum = d.dl_mnum
    WHERE mm.permno IS NULL
),
mret AS (
    SELECT permno, mnum, ret FROM present_msf
    UNION ALL
    SELECT permno, mnum, ret FROM delist_only
)
SELECT e.D AS D, e.decile AS decile, mr.mnum AS mnum, avg(mr.ret) AS ew
FROM ext_dec AS e
INNER JOIN mret AS mr ON mr.permno = e.permno
GROUP BY e.D, e.decile, mr.mnum
SETTINGS max_execution_time = 600, max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
"""


def q(sql):
    cfg = get_clickhouse_config()
    c = Client(host=cfg["host"], port=int(cfg["port"]), user=cfg["user"],
               password=cfg["password"])
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


# --- benchmark annual return per (assignment-Dec, decile, target months) ---
def build_bk_long(panel: pd.DataFrame, ext_dec: pd.DataFrame,
                  ew: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (bk_fix, bk_rea) long tables indexed by (fy, permno, k)."""
    base = panel[["fy", "permno", "size_dec"]].copy()
    ks = pd.DataFrame({"k": np.arange(1, 6)})
    grid = (base.assign(_k=1).merge(ks.assign(_k=1), on="_k").drop(columns="_k")
            .assign(_j=1).merge(
                pd.DataFrame({"j": np.arange(12), "_j": 1}), on="_j")
            .drop(columns="_j"))
    grid["start"] = (grid["fy"] + grid["k"] - 1) * 12 + 5
    grid["mnum"] = grid["start"] + grid["j"]
    grid["D_fix"] = (grid["fy"] - 1).astype("int32")
    grid["D_rea"] = (grid["fy"] + grid["k"] - 2).astype("int32")
    # reassigned decile = ext_dec[D_rea, permno]
    grid = grid.merge(ext_dec.rename(columns={"D": "D_rea", "decile": "dec_rea"}),
                      on=["D_rea", "permno"], how="left")

    # fixed EW: merge on (D_fix, size_dec, mnum)
    grid = grid.merge(ew.rename(columns={"D": "D_fix", "decile": "size_dec",
                                         "ew": "ew_fix"}),
                      on=["D_fix", "size_dec", "mnum"], how="left")
    # reassigned EW: merge on (D_rea, dec_rea, mnum)
    grid = grid.merge(ew.rename(columns={"D": "D_rea", "decile": "dec_rea",
                                         "ew": "ew_rea"}),
                      on=["D_rea", "dec_rea", "mnum"], how="left")
    grid["ef"] = 1 + grid["ew_fix"].fillna(0)
    grid["er"] = 1 + grid["ew_rea"].fillna(0)
    g = grid.groupby(["fy", "permno", "k"], sort=False)
    bk_fix = (g["ef"].prod() - 1).rename("bk")
    bk_rea = (g["er"].prod() - 1).rename("bk")
    return bk_fix.reset_index(), bk_rea.reset_index()


def cell_saar(mask: pd.Series, panel: pd.DataFrame, bk_fix: pd.DataFrame,
              bk_rea: pd.DataFrame) -> tuple[float, float, int]:
    """Returns (saar_fix, saar_rea, n_fy). Strict per-fy 5-yr mean (matches sortlib)."""
    members = panel.loc[mask, ["fy", "permno"]].copy()
    bf = bk_fix.rename(columns={"bk": "bf"})
    br = bk_rea.rename(columns={"bk": "br"})
    R, Bf, Br = {}, {}, {}
    for k in range(1, 6):
        mk = members.merge(
            panel[["fy", "permno", f"alive_{k}", f"stock_ret_{k}"]],
            on=["fy", "permno"])
        mk = mk[(mk[f"alive_{k}"] == 1) & mk[f"stock_ret_{k}"].notna()]
        mk = mk.merge(bf[bf["k"] == k][["fy", "permno", "bf"]],
                      on=["fy", "permno"], how="left")
        mk = mk.merge(br[br["k"] == k][["fy", "permno", "br"]],
                      on=["fy", "permno"], how="left")
        R[k] = mk.groupby("fy")[f"stock_ret_{k}"].mean()
        Bf[k] = mk.groupby("fy")["bf"].mean()
        Br[k] = mk.groupby("fy")["br"].mean()
    fys = sorted(panel["fy"].unique())

    def per_fy(B):
        s = {}
        for fy in fys:
            vals = [R[k].get(fy, np.nan) - B[k].get(fy, np.nan)
                    for k in range(1, 6)]
            s[fy] = np.mean(vals)   # strict: NaN if any year missing
        return pd.Series(s).dropna()

    sf = per_fy(Bf)
    sr = per_fy(Br)
    return float(sf.mean()), float(sr.mean()), len(sf)


def main():
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    our = {k: json.loads((RES / JSONF[k]).read_text()) for k in JSONF}
    tgt = {m["name"]: m["value"] for t in
           json.loads(LAYOUT.preparations_path("tables_to_replicate.json")
                      .read_text())["tables"]
           for m in t["metrics"] if t["id"] in
           ("table_I", "table_II", "table_III")}

    # top-50% subsample (for Table III cells)
    big = pd.Series(False, index=panel.index)
    for _, idx in panel.groupby("fy").groups.items():
        me = panel.loc[idx, "me_apr"]
        big.loc[idx] = (me >= me.median()) & me.notna()
    sub = panel[big].reset_index(drop=True)

    print("Pulling extended December rankings + EW monthly returns ...")
    ext_dec = q(EXT_DEC_SQL)
    ew = q(EW_SQL)
    print(f"  ext_dec rows={len(ext_dec):,} (D {ext_dec.D.min()}-{ext_dec.D.max()}); "
          f"ew rows={len(ew):,}")

    print("Building fixed/reassigned benchmark annual returns ...")
    bk_fix, bk_rea = build_bk_long(panel, ext_dec, ew)
    print(f"  bk rows={len(bk_fix):,}")

    print("\n" + "=" * 104)
    print("SAAR DIAGNOSTIC — fixed (formation-time) vs reassigned (each December)")
    print("  fixed_tbl = accepted tables JSON; fixed_diag = this run's recomputation of the")
    print("  SAME fixed assignment (parity check); reassign = reassigned-each-December.")
    print("  Δ = reassign − fixed_diag (clean within-diagnostic effect of reassignment).")
    print("=" * 104)
    print(f"{'cell':<17}{'paper':>7}{'fx_tbl':>8}{'fx_diag':>9}"
          f"{'reassign':>9}{'Δ':>8}{'n_fy':>5}")
    rows = []
    for label, jf, mname, mkf in CELLS:
        mask = mkf(panel, sub)
        sf, sr, nf = cell_saar(mask, panel, bk_fix, bk_rea)
        paper = tgt.get(mname)
        fixed_tbl = our[jf].get(mname)
        rows.append((label, paper, fixed_tbl, sf, sr, nf))
        print(f"{label:<17}"
              f"{paper if paper is not None else float('nan'):>7.3f}"
              f"{fixed_tbl if fixed_tbl is not None else float('nan'):>8.3f}"
              f"{sf:>9.3f}{sr:>9.3f}{(sr - sf):>+8.3f}{nf:>5d}")
    print("-" * 104)

    def closer(paper, a, b):
        return paper is not None and abs(b - paper) < abs(a - paper) - 1e-9

    # count improvements using the diagnostic's own fixed as baseline (clean)
    imp_diag = sum(1 for _, paper, _, sf, sr, _ in rows if closer(paper, sf, sr))
    # and vs the accepted table value (only meaningful where parity holds)
    imp_tbl = sum(1 for _, paper, ft, sf, sr, _ in rows
                  if ft is not None and closer(paper, ft, sr))
    print(f"\nReassigned CLOSER to paper than fixed_diag in {imp_diag}/{len(rows)} cells.")
    print(f"Reassigned CLOSER to paper than fixed_tbl  in {imp_tbl}/{len(rows)} cells "
          f"(T3 rows less reliable: see parity).")
    print("\nParity (fx_diag vs fx_tbl): T1/T2 match within ~0.003; T3 (top-50% corner "
          "cells) diverge because this diagnostic uses a strict 5-yr mean (dropping "
          "formations with a missing benchmark year -> n_fy=11) AND a benchmark EW built "
          "from the full Dec-1967..1992 universe, whereas the accepted tables use nanmean "
          "and the panel's sizedec_ret (Dec-1967..1988 ∩ April universe). So T3 Δ still "
          "isolates the assignment effect but its absolute 'reassign' level is not "
          "directly additive to the accepted table value.")
    print("=" * 104)
    print("\nREAD-OUT (report only; no defaults/results changed):")
    print("  Failing cells where paper > fixed_tbl (reassign should raise SAAR):")
    for label, paper, ft, sf, sr, nf in rows[:8]:
        if paper is not None and ft is not None and paper > ft + 1e-6:
            print(f"    {label:<17} paper{paper:+.3f} fx_tbl{ft:+.3f} -> "
                  f"reassign{sr:+.3f}  ({'toward paper' if sr > sf else 'away'})")
    print("  Headline corners (reassign should NOT wreck these):")
    for label, paper, ft, sf, sr, nf in rows[11:]:
        print(f"    {label:<17} paper{paper:+.3f} fx_tbl{ft:+.3f} reassign{sr:+.3f} "
              f"(Δ{sr - sf:+.3f})")


if __name__ == "__main__":
    main()
