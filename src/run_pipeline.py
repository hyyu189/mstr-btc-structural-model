from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

from .calibration import build_model_params
from .indicators import (
    compute_ibgr_per_share,
    compute_ibgr_total,
    compute_ifrd,
    compute_ile_from_panel,
    compute_pmri,
    compute_survival_probability,
    compute_tee_from_panel,
)
from .plots import plot_core_timeseries, plot_ifrd_histogram
from .preprocessing import build_daily_panel
from .simulation import SimulationConfig, simulate_paths


ROOT = Path(".")
RESULTS_DIR = ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"


def main() -> None:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # 1. Data preprocessing
    panel_data = build_daily_panel()
    panel = panel_data.panel
    panel_calib = panel_data.panel_calib

    panel.to_csv(RESULTS_DIR / "panel_processed.csv")

    # 2. Calibration
    params = build_model_params(
        panel=panel,
        panel_calib=panel_calib,
        nav_floor=1.0,
        start_date="2021-01-01",
    )

    with open(RESULTS_DIR / "params.json", "w", encoding="utf-8") as f:
        json.dump(params.to_dict(), f, indent=2)

    # 3. Current-state indicators from panel
    last = panel.iloc[-1]
    s0 = float(last["btc_price"])
    h0 = float(last["btc_holdings"])
    d0 = float(last["debt_total_usd"])
    n0 = float(last["shares"])
    pi0 = float(last["premium"])

    ile_series = compute_ile_from_panel(panel)
    tee_series = compute_tee_from_panel(panel, params.gamma_pi_s)
    pmri_value = compute_pmri(params.ou_premium, pi0)
    ibgr_total = compute_ibgr_total(params, h0=h0, pi0=pi0)

    # 4. Monte Carlo simulation under P
    sim_cfg = SimulationConfig(n_paths=5000, years=3.0, dt=1.0 / 252.0, random_seed=42)
    sim = simulate_paths(
        params=params,
        s0=s0,
        pi0=pi0,
        h0=h0,
        d0=d0,
        n0=n0,
        config=sim_cfg,
    )

    n_steps = sim_cfg.n_steps
    horizon_idx = n_steps

    # 5. Simulation-based indicators
    ibgr_per_share = compute_ibgr_per_share(
        sim["B"], dt=sim_cfg.dt, horizon_idx=horizon_idx
    )

    G = compute_ifrd(sim["S"], sim["H"], horizon_idx=horizon_idx)
    ifrd_summary = {
        "mean": float(np.mean(G)),
        "std": float(np.std(G)),
        "p5": float(np.percentile(G, 5)),
        "p50": float(np.percentile(G, 50)),
        "p95": float(np.percentile(G, 95)),
    }

    survival_eps0 = compute_survival_probability(
        sim["S"],
        sim["H"],
        sim["D"],
        eps=0.0,
        horizon_idx=horizon_idx,
    )

    survival_eps10 = compute_survival_probability(
        sim["S"],
        sim["H"],
        sim["D"],
        eps=0.1,
        horizon_idx=horizon_idx,
    )

    # 6. Save indicator summary
    indicators = {
        "current_date": str(panel.index[-1].date()),
        "S0": s0,
        "H0": h0,
        "D0": d0,
        "N0": n0,
        "pi0": pi0,
        "ILE_current": float(ile_series.iloc[-1]),
        "TEE_current": float(tee_series.iloc[-1]),
        "PMRI_current": pmri_value,
        "IBGR_total_current": ibgr_total,
        "IBGR_per_share_3y": ibgr_per_share,
        "IFRD_mean": ifrd_summary["mean"],
        "IFRD_p95": ifrd_summary["p95"],
        "survival_prob_3y_eps0": survival_eps0,
        "survival_prob_3y_eps10pct": survival_eps10,
    }

    with open(RESULTS_DIR / "indicators.json", "w", encoding="utf-8") as f:
        json.dump(indicators, f, indent=2)

    # 7. Plots
    plot_core_timeseries(panel, ile_series, tee_series, FIGURES_DIR)
    plot_ifrd_histogram(G, FIGURES_DIR)

    # 8. Markdown summary report
    summary_path = RESULTS_DIR / "summary.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# MSTR BTC Structural Model – Summary\n\n")
        f.write(f"**As of date:** {indicators['current_date']}\n\n")
        f.write("## Calibrated Parameters\n\n")
        for k, v in params.to_dict().items():
            f.write(f"- **{k}**: {v}\n")

        f.write("\n## Key Indicators\n\n")
        for k, v in indicators.items():
            f.write(f"- **{k}**: {v}\n")

    # 9. Basic textual summary to stdout
    print("=== Calibrated parameters ===")
    for k, v in params.to_dict().items():
        print(f"{k}: {v}")

    print("\n=== Key indicators ===")
    for k, v in indicators.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()


