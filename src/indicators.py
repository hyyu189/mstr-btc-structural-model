from __future__ import annotations

from typing import Dict, Tuple

import numpy as np
import pandas as pd

from .calibration import ModelParams, OUParams


def compute_ile_from_panel(panel: pd.DataFrame) -> pd.Series:
    """
    Implied Leverage Elasticity (ILE) from historical panel.

    beta_LS(t) = (H_t S_t) / (H_t S_t - D_t) when H_t S_t > D_t.
    """
    h = panel["btc_holdings"].astype(float)
    s = panel["btc_price"].astype(float)
    d = panel["debt_total_usd"].astype(float)
    asset = h * s
    denom = asset - d
    ile = asset / denom
    ile[denom <= 0.0] = np.nan
    return ile


def compute_tee_from_panel(panel: pd.DataFrame, gamma_pi_s: float) -> pd.Series:
    """
    Total Equity Elasticity (TEE) using historical balance sheet and
    regression-based premium sensitivity gamma_pi_s.
    """
    ile = compute_ile_from_panel(panel)
    return gamma_pi_s + ile


def compute_pmri(ou_params: OUParams, pi0: float) -> float:
    """
    Premium Mean-Reversion Index (PMRI) for current premium pi0.
    """
    var_ss = ou_params.sigma ** 2 / (2.0 * ou_params.kappa)
    std_ss = np.sqrt(var_ss)
    return float((pi0 - ou_params.theta) / std_ss)


def compute_ibgr_total(params: ModelParams, h0: float, pi0: float) -> float:
    """
    Approximate total Implied BTC Growth Rate (IBGR) at current state.

    mu_H ≈ (alpha * pi0^+ + lambda_M * E[ΔH]) / H0.
    """
    if h0 <= 0.0:
        return float("nan")
    pi_pos = max(pi0, 0.0)
    alpha = params.holdings.alpha
    lambda_m = params.holdings.lambda_m
    mean_jump = params.holdings.mean_jump_size
    mu_H = (alpha * pi_pos + lambda_m * mean_jump) / h0
    return float(mu_H)


def compute_ibgr_per_share(
    B_paths: np.ndarray,
    dt: float,
    horizon_idx: int,
) -> float:
    """
    Estimate per-share IBGR from simulated BTC-per-share paths.

    mu_{H/N} ≈ (1 / B0) E[(B_T - B0) / (T - 0)].

    Parameters
    ----------
    B_paths:
        Array of shape (n_steps+1, n_paths).
    dt:
        Time step in years.
    horizon_idx:
        Index in the time dimension corresponding to horizon T.
    """
    B0 = B_paths[0, :]
    B_T = B_paths[horizon_idx, :]
    T = horizon_idx * dt
    if T <= 0.0:
        return float("nan")
    growth = (B_T - B0) / (T * B0)
    return float(np.nanmean(growth))


def compute_ifrd(
    S_paths: np.ndarray,
    H_paths: np.ndarray,
    horizon_idx: int,
) -> np.ndarray:
    """
    Compute pathwise funding requirement G_T ≈ sum S_t * (H_{t+1} - H_t).

    Parameters
    ----------
    S_paths, H_paths:
        Arrays of shape (n_steps+1, n_paths).
    horizon_idx:
        Index for horizon T (use all steps up to this index).

    Returns
    -------
    np.ndarray
        Array of length n_paths with G_T values.
    """
    S = S_paths[: horizon_idx, :]
    dH = H_paths[1 : horizon_idx + 1, :] - H_paths[:horizon_idx, :]
    G = (S * dH).sum(axis=0)
    return G


def compute_survival_probability(
    S_paths: np.ndarray,
    H_paths: np.ndarray,
    D_paths: np.ndarray,
    eps: float,
    horizon_idx: int,
) -> float:
    """
    Estimate survival probability up to horizon T.

    Survival event: for all t <= T,
        H_t S_t > (1 + eps) D_t.
    """
    S = S_paths[: horizon_idx + 1, :]
    H = H_paths[: horizon_idx + 1, :]
    D = D_paths[: horizon_idx + 1, :]
    A = H * S
    threshold = (1.0 + float(eps)) * D
    distress = A <= threshold
    # Any distress at any time up to horizon => path fails.
    distress_any = distress.any(axis=0)
    survival = (~distress_any).mean()
    return float(survival)


