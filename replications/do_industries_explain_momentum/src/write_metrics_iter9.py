"""Iteration 9 finalization — write results/metrics.json + results/diagnostics_block.md.

READS   data/panel.parquet (48 cols, frozen), data/bin_rets.parquet,
        results/cells_tables_1_2_3.json, results/cells_table_6.json,
        and two small in-memory SQL pulls of ff.four_factor_monthly /
        ff.five_factor_monthly (1963-01..1995-12).
WRITES  results/metrics.json (flat dict of floats/ints, all finite) and
        results/diagnostics_block.md (verbatim format_diagnostics_block
        output for REPORT.md).

Series (all from the frozen panel via the tables_1_2_3 cohort engine):
  * primary  — (6,6) raw individual W-L monthly, 1963-07..1995-07 (T=385;
    reproduces 0.004135 / t 2.311, Table II Panel A "Raw").
  * industry — (6,6) raw industry-momentum W-L (IM(6,6) Panel-A convention,
    industry VW returns; reproduces ~0.0040 / t ~2.36, Table II Panel B
    "Raw Industry").
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from clickhouse_driver import Client

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_REPLICATIONS_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = Path(__file__).resolve().parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from utils.paths import paper_layout  # noqa: E402
from utils.env import get_clickhouse_config  # noqa: E402
from utils import (  # noqa: E402
    performance_metrics,
    factor_alpha,
    portfolio_diagnostics,
    format_diagnostics_block,
)
import tables_1_2_3 as t123  # noqa: E402

SLUG = "do_industries_explain_momentum"
LAYOUT = paper_layout(SLUG, replications_root=_REPLICATIONS_ROOT)
_CFG = get_clickhouse_config()


def q(sql: str) -> pd.DataFrame:
    c = Client(host=_CFG["host"], port=int(_CFG["port"]),
               user=_CFG["user"], password=_CFG["password"],
               settings={"max_execution_time": 60})
    try:
        data, cols = c.execute(sql, with_column_types=True)
    finally:
        c.disconnect()
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def load_ff(table: str, extra_cols: list[str]) -> pd.DataFrame:
    """Pull an ff monthly factor table, 1963-01..1995-12, indexed by month
    (DatetimeIndex, month-start — aligned with the primary series'
    to_timestamp() index; portfolio_diagnostics' pd.to_datetime call
    coerces a PeriodIndex to NaT). Values in the ff tables are stored as
    decimals (consistent with the replication's rf usage: exret = ret - rf;
    ff4 rf mean == panel rf mean over 1963-07..1995-07)."""
    cols = ", ".join(
        f"CAST({c} AS Nullable(Float64)) AS {c}" for c in extra_cols
    )
    sql = f"""
    SELECT toDate32(dt) AS dt, {cols}
    FROM {table}
    WHERE toDate32(dt) >= toDate32('1963-01-01')
      AND toDate32(dt) <= toDate32('1995-12-31')
    SETTINGS max_execution_time = 60,
             max_rows_to_read = 1000000000,
             timeout_before_checking_execution_speed = 0
    """
    df = q(sql)
    df["dt"] = pd.to_datetime(df["dt"])
    idx = pd.PeriodIndex(df["dt"].dt.to_period("M")).to_timestamp()
    df = df.set_index(idx).drop(columns="dt")
    df = df[~df.index.duplicated(keep="first")].sort_index()
    return df


def main() -> int:
    t0 = time.time()
    metrics: dict[str, object] = {}

    # ---- primary (6,6) raw individual W-L series --------------------------
    print("[1] loading frozen panel + bin_rets ...")
    panel, ind = t123.load_data()
    print(f"    panel {panel.shape}, bin_rets {ind.shape}")

    print("[2] global individual cohorts + (6,6) raw W-L series ...")
    cohorts = t123.build_global_cohorts(panel)
    ret_wide = panel.pivot(index="month", columns="permno", values="ret")
    spread = t123.individual_spread_series(ret_wide, cohorts, hold=6)
    primary = t123.restrict(spread, t123.RAW_START, t123.RAW_END).dropna()
    m_raw, t_raw, n_raw = t123.mean_t(primary)
    print(f"    primary: mean={m_raw:.6f}, t={t_raw:.4f}, n={n_raw} "
          f"({primary.index.min()}..{primary.index.max()})")
    metrics["wilo_66_raw_mean"] = float(m_raw)
    metrics["wilo_66_raw_t"] = float(t_raw)
    metrics["wilo_66_raw_n_obs"] = int(n_raw)

    # Same series with a month-start DatetimeIndex for the utils calls
    # (portfolio_diagnostics' pd.to_datetime coerces a PeriodIndex to NaT).
    primary_ts = primary.copy()
    primary_ts.index = primary.index.to_timestamp()

    pm = performance_metrics(primary_ts, freq="M")
    metrics["wilo_66_raw_sharpe_annualized"] = float(pm["sharpe_ratio"])
    metrics["wilo_66_raw_max_drawdown"] = float(pm["max_drawdown"])

    # ---- industry (6,6) raw W-L series (Table II Panel B convention) ------
    print("[3] industry (6,6) raw W-L series (IM(6,6), Panel A) ...")
    ind_vw_mat = ind.pivot(index="month", columns="ind",
                           values="ind_ret_vw").reindex(columns=np.arange(1, 21))
    sig6 = ind.pivot(index="month", columns="ind",
                     values="ind_mom6").reindex(columns=np.arange(1, 21))
    sels6 = t123.industry_selections(sig6)
    months_idx = ind_vw_mat.index
    Wi, _Mid, Lo, f_list, f_pos = t123.industry_cohort_returns(
        sels6, ind_vw_mat, months_idx, max_hold=6)
    wi_s = t123.industry_strat_series(Wi, f_list, f_pos, months_idx, 6, "A")
    lo_s = t123.industry_strat_series(Lo, f_list, f_pos, months_idx, 6, "A")
    wilo_ind = t123.restrict(wi_s - lo_s, t123.RAW_START, t123.RAW_END).dropna()
    m_ind, t_ind, n_ind = t123.mean_t(wilo_ind)
    print(f"    industry: mean={m_ind:.6f}, t={t_ind:.4f}, n={n_ind}")
    metrics["wilo_66_industry_raw_mean"] = float(m_ind)
    metrics["wilo_66_industry_raw_t"] = float(t_ind)
    metrics["wilo_66_industry_raw_n_obs"] = int(n_ind)

    # ---- Carhart-4-factor alpha on the primary series ----------------------
    print("[4] Carhart-4-factor alpha (ff.four_factor_monthly) ...")
    ff4 = load_ff("ff.four_factor_monthly",
                  ["mkt_rf", "smb", "hml", "mom", "rf"])
    print(f"    ff4: {ff4.shape}, {ff4.index.min()}..{ff4.index.max()}")
    fa = factor_alpha(
        portfolio_returns=primary_ts,
        factor_returns=ff4,
        factors=["mkt_rf", "smb", "hml", "mom"],
    )
    print(f"    alpha_annualized_pct={fa['alpha_annualized_pct']:.4f}, "
          f"t={fa['t_alpha_newey_west']:.4f}, n_obs={fa['n_obs']}")
    metrics["wilo_66_raw_alpha_annualized_pct"] = float(fa["alpha_annualized_pct"])
    metrics["wilo_66_raw_alpha_t"] = float(fa["t_alpha_newey_west"])

    # ---- FF5 standard report diagnostics block -----------------------------
    print("[5] FF5 portfolio_diagnostics + diagnostics_block.md ...")
    ff5 = load_ff("ff.five_factor_monthly",
                  ["mkt_rf", "smb", "hml", "rmw", "cma", "rf"])
    print(f"    ff5: {ff5.shape}, {ff5.index.min()}..{ff5.index.max()}")
    diag = portfolio_diagnostics(
        primary_ts,
        factor_returns=ff5,
        zero_investment=True,
        freq="M",
    )
    block = format_diagnostics_block(
        diag, portfolio_label="(6,6) raw W-L individual momentum")
    block_path = LAYOUT.result_path("diagnostics_block.md")
    block_path.write_text(block)
    print(f"    wrote {block_path}")

    # ---- replication tallies from the cells JSONs --------------------------
    print("[6] per-cell tallies ...")
    cells_123 = json.loads(
        LAYOUT.result_path("cells_tables_1_2_3.json").read_text())
    cells_6 = json.loads(LAYOUT.result_path("cells_table_6.json").read_text())
    all_cells = cells_123 + cells_6

    def _tally(cells):
        out = {"tier1": 0, "tier2": 0, "fail": 0, "skip": 0}
        for c in cells:
            st = c["status"].strip().lower()
            key = {"tier1": "tier1", "tier2": "tier2",
                   "fail": "fail", "skip": "skip"}.get(st)
            if key:
                out[key] += 1
        return out

    tot = _tally(all_cells)
    metrics["total_tier1"] = int(tot["tier1"])
    metrics["total_tier2"] = int(tot["tier2"])
    metrics["total_fail"] = int(tot["fail"])
    metrics["total_skip"] = int(tot["skip"])
    metrics["total_cells"] = int(len(all_cells))

    by_table: dict[str, list] = {}
    for c in all_cells:
        by_table.setdefault(str(c["table"]).lower(), []).append(c)
    for tid in ("t1", "t2", "t3", "t6"):
        tt = _tally(by_table.get(tid, []))
        metrics[f"{tid}_tier1"] = int(tt["tier1"])
        metrics[f"{tid}_tier2"] = int(tt["tier2"])
        metrics[f"{tid}_fail"] = int(tt["fail"])

    # ---- Table VI Fama-MacBeth headline coefficients -----------------------
    print("[7] Table VI FM coefficients ...")
    cell_by_metric = {c["metric"]: c for c in cells_6}

    def _cell(metric: str) -> float:
        c = cell_by_metric[metric]
        return float(c["ours"])

    metrics["fm_ind_6_1_coef"] = _cell("pB_6_1_s1_ind")
    metrics["fm_ind_6_1_t"] = _cell("pB_6_1_s1_ind_t")
    metrics["fm_ret_6_1_C_coef"] = _cell("pC_6_1_s1_ret")
    metrics["fm_ret_6_1_C_t"] = _cell("pC_6_1_s1_ret_t")
    metrics["fm_ret_12_1_C_coef"] = _cell("pC_12_1_s1_ret")
    metrics["fm_ret_12_1_C_t"] = _cell("pC_12_1_s1_ret_t")

    # ---- finiteness guard + write ------------------------------------------
    for k, v in metrics.items():
        if isinstance(v, float) and not math.isfinite(v):
            raise ValueError(f"non-finite metric {k} = {v}")
        if not isinstance(v, (int, float)):
            raise ValueError(f"metric {k} has non-numeric type {type(v)}")

    out_path = LAYOUT.result_path("metrics.json")
    out_path.write_text(json.dumps(metrics, indent=1) + "\n")
    print(f"\n[8] wrote {out_path} ({len(metrics)} keys) in "
          f"{time.time() - t0:.1f}s")
    print(json.dumps(metrics, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
