"""
One-shot regeneration after the §3.3 MILLIQ_open adoption (Task A) and
the Newey-West lag sweep (Task B):

  1. Rebuild data/milliq.parquet with columns [month, milliq (= open),
     milliq_admitted (old series), n_days, n_stocks (open)] — from the
     two cached series (no ClickHouse needed).
  2. Re-run main.build_table_3() (now with T3_NW_MAXLAGS) and
     main.build_table_4() (now on the open MILLIQ) → results/table_3.md
     and results/table_4.md.
  3. Re-render results/g1_g2_by_size.png from the new estimates.

Tables 1-2 artifacts are NOT touched.
"""
import sys
from pathlib import Path

import pandas as pd

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC))
import main as M  # noqa: E402


def main() -> None:
    print("=== regen: milliq.parquet + table_3.md + table_4.md + plot ===")

    # --- 1. milliq.parquet (open primary + admitted provenance) ---
    opq = pd.read_parquet(M.CACHE_DIR / "milliq_open_monthly.parquet")
    adm_path = M.LAYOUT.data_path("milliq.parquet")
    old = pd.read_parquet(adm_path)
    if "milliq_admitted" in old.columns:          # idempotent re-run
        adm_series = old["milliq_admitted"]
    else:
        adm_series = old["milliq"]
    m = opq.merge(
        pd.DataFrame({"month": old["month"], "milliq_admitted": adm_series}),
        on="month", how="inner")
    m = m[["month", "milliq", "milliq_admitted", "n_days", "n_stocks"]]
    m = m.sort_values("month").reset_index(drop=True)
    m.to_parquet(adm_path, index=False)
    print(f"[1] wrote {adm_path}: {len(m)} rows x {list(m.columns)}")

    # --- 2. tables 3-4 (read the refreshed milliq.parquet) ---
    print("[2] build_table_3 (NW maxlags "
          f"{M.T3_NW_MAXLAGS}) ...")
    t3 = M.build_table_3()
    print("[3] build_table_4 (open MILLIQ) ...")
    t4 = M.build_table_4()

    # --- 3. g1/g2 by size plot with the new estimates ---
    if t3.get("gate_passed") and t4.get("gate_passed"):
        print("[4] g1_g2_by_size.png ...")
        M.plot_g1_g2_by_size(t3["est"], t4["est"])

    print("\nDONE.")
    print(f"  Table 4 Tier counts: {t4['counts']}")
    print(f"  SZ1: {'HOLDS' if t4.get('sz1') else 'PARTIAL'}; "
          f"SZ2: {'HOLDS' if t4.get('sz2') else 'PARTIAL'}")


if __name__ == "__main__":
    main()
