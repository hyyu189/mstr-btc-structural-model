from __future__ import annotations

from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.optimize import brentq

from .calibration import ModelParams, OUParams


def compute_ile_from_panel(panel: pd.DataFrame) -> pd.Series:
    """
    Implied Leverage Elasticity (ILE) from historical panel.

    Now accounts for preferred stock:
    beta_LS(t) = (H_t S_t) / (H_t S_t - D_t - P_liq) when denominator > 0.
    """
    h = panel["btc_holdings"].astype(float)
    s = panel["btc_price"].astype(float)
    d = panel["debt_total_usd"].astype(float)
    p = panel["preferred_liq"].astype(float) if "preferred_liq" in panel.columns else 0.0
    asset = h * s
    denom = asset - d - p
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
    Compute pathwise funding requirement G_T = sum S_t * (H_{t+1} - H_t).
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
    pref_liq: float = 0.0,
) -> float:
    """
    Estimate survival probability up to horizon T.

    Survival event: for all t <= T,
        H_t S_t > (1 + eps) * (D_t + P_liq).
    """
    S = S_paths[: horizon_idx + 1, :]
    H = H_paths[: horizon_idx + 1, :]
    D = D_paths[: horizon_idx + 1, :]
    A = H * S
    threshold = (1.0 + float(eps)) * (D + pref_liq)
    distress = A <= threshold
    distress_any = distress.any(axis=0)
    survival = (~distress_any).mean()
    return float(survival)


def compute_dividend_coverage_ratio(
    asset_value: float,
    debt: float,
    annual_preferred_dividend: float,
) -> float:
    """
    Dividend Coverage Ratio (DCR): measures how many times the company can
    cover its preferred dividend obligations from net asset value.

    DCR = (Assets - Debt) / Annual_Preferred_Dividend

    A ratio > 1 means the company can cover dividends; higher is better.
    Returns NaN if there are no preferred dividends.
    """
    if annual_preferred_dividend <= 0.0:
        return float("nan")
    net_assets = asset_value - debt
    return float(net_assets / annual_preferred_dividend)


def compute_dividend_coverage_from_sim(
    S_paths: np.ndarray,
    H_paths: np.ndarray,
    D_paths: np.ndarray,
    annual_preferred_dividend: float,
    horizon_idx: int,
) -> Dict[str, float]:
    """
    Compute dividend coverage statistics from simulation paths.

    Returns dict with mean, min (across time), and probability of coverage < 1.
    """
    if annual_preferred_dividend <= 0.0:
        return {"mean": float("nan"), "min": float("nan"), "prob_undercovered": 0.0}

    A = H_paths[: horizon_idx + 1, :] * S_paths[: horizon_idx + 1, :]
    D = D_paths[: horizon_idx + 1, :]
    net = A - D
    dcr = net / annual_preferred_dividend

    mean_dcr = float(np.mean(dcr[-1, :]))
    min_dcr_per_path = dcr.min(axis=0)
    prob_under = float((min_dcr_per_path < 1.0).mean())

    return {
        "mean": mean_dcr,
        "min_mean": float(np.mean(min_dcr_per_path)),
        "prob_undercovered": prob_under,
    }


# ====================================================================
# New theory indicators
# ====================================================================


def compute_ele_from_panel(panel: pd.DataFrame) -> pd.Series:
    """
    Effective Leverage Elasticity (ELE): A_t / (A_t - L_t)
    where L_t = D_t + P_liq (debt + all preferred liquidation value).

    This is identical to ILE when preferred = 0 but diverges when preferred > 0.
    In this codebase ILE already includes preferred, so ELE = ILE.
    """
    return compute_ile_from_panel(panel)


def compute_cslr(
    debt: float, preferred_liq: float, equity_mkt_cap: float
) -> float:
    """
    Capital Stack Leverage Ratio: L_t / E_t.
    Total claims senior to common equity relative to equity market cap.
    """
    if equity_mkt_cap <= 0.0:
        return float("nan")
    return (debt + preferred_liq) / equity_mkt_cap


def compute_pcr(
    asset_value: float,
    mu_s: float,
    annual_preferred_dividend: float,
    horizon_years: float = 3.0,
) -> float:
    """
    Preferred Coverage Ratio: expected asset appreciation / preferred dividends.

    PCR = E[Delta A+] / (Phi * T)
    where E[Delta A+] approx A_0 * (exp(mu_s * T) - 1) for GBM.
    """
    if annual_preferred_dividend <= 0.0:
        return float("nan")
    expected_appreciation = asset_value * (np.exp(mu_s * horizon_years) - 1.0)
    total_div = annual_preferred_dividend * horizon_years
    return float(max(expected_appreciation, 0.0) / total_div)


def compute_fair_premium(
    ibgr: float,
    sigma_s: float,
    kappa: float,
    ile: float,
    r: float = 0.04,
) -> float:
    """
    Fair premium pi_star = log(1 + V_acc / NAV).

    Uses steady-state approximation:
        V_acc / NAV ≈ IBGR / (r + kappa) * (1 + sigma_S^2 / (2*kappa))

    Parameters
    ----------
    ibgr : BTC growth rate (proxy for accretion rate)
    sigma_s : BTC annualized volatility
    kappa : premium mean-reversion speed
    ile : implied leverage elasticity (ELE)
    r : risk-free / discount rate
    """
    denom = r + kappa
    if denom <= 0:
        return float("nan")
    vol_adj = 1.0 + sigma_s ** 2 / (2.0 * kappa) if kappa > 0 else 1.0
    v_acc_over_nav = ibgr / denom * vol_adj
    v_acc_over_nav = max(v_acc_over_nav, 0.0)
    return float(np.log(1.0 + v_acc_over_nav))


def compute_fair_premium_timeseries(
    panel: pd.DataFrame,
    params: ModelParams,
    r: float = 0.04,
) -> pd.Series:
    """
    Compute fair premium pi_star_t for each date in the panel.
    """
    h = panel["btc_holdings"].astype(float)
    s = panel["btc_price"].astype(float)
    d = panel["debt_total_usd"].astype(float)
    p = panel["preferred_liq"].astype(float) if "preferred_liq" in panel.columns else pd.Series(0.0, index=panel.index)

    asset = h * s
    liab = d + p
    nav = (asset - liab).clip(lower=1.0)

    kappa = params.ou_premium.kappa
    sigma_s = params.sigma_s

    # Per-row IBGR approximation
    pi = panel["premium"].astype(float)
    pi_pos = pi.clip(lower=0.0)
    alpha = params.holdings.alpha
    lambda_m = params.holdings.lambda_m
    mean_jump = params.holdings.mean_jump_size
    mu_H = (alpha * pi_pos + lambda_m * mean_jump) / h.clip(lower=1.0)

    # ILE series
    ile = asset / nav

    denom = r + kappa
    vol_adj = 1.0 + sigma_s ** 2 / (2.0 * kappa) if kappa > 0 else 1.0
    v_ratio = (mu_H / denom * vol_adj).clip(lower=0.0)
    pi_star = np.log(1.0 + v_ratio)

    return pi_star


def compute_mispricing(
    pi_t: float, pi_star_t: float
) -> Tuple[float, str]:
    """
    Structural mispricing: Delta_t = pi_t - pi_star_t.
    Returns (delta, label) where label is 'overvalued' or 'undervalued'.
    """
    delta = pi_t - pi_star_t
    label = "overvalued" if delta > 0 else "undervalued"
    return delta, label


def compute_mispricing_zscore(
    delta_series: pd.Series,
) -> pd.Series:
    """
    Mispricing z-score: delta_t / std(delta_t).
    """
    std = delta_series.std()
    if std <= 0 or np.isnan(std):
        return delta_series * 0.0
    return delta_series / std


def compute_reflexivity_gain(
    eta: float,
    ile: float,
    pi: float,
    kappa: float,
    lambda_bar: float,
) -> float:
    """
    Approximate reflexivity gain G.

    G = eta * (dH/dS) * (dpi*/dNAV) * (d_issuance/dpi)

    We approximate using:
    - dH/dS: proportional to current holdings leverage ~ ILE
    - dpi*/dNAV: ~ 1/NAV * dV_acc/dNAV, approximated as ~1/(1 + exp(pi))
    - d_issuance/dpi: ~ lambda_bar (linear issuance policy)

    Simplified: G ≈ eta * ILE * lambda_bar / kappa
    """
    if kappa <= 0:
        return float("nan")
    return float(eta * ile * lambda_bar / kappa)


def compute_effective_kappa(kappa: float, G: float) -> float:
    """
    Effective mean-reversion: kappa_eff = kappa * (1 - G).
    """
    return kappa * (1.0 - G)


def compute_tipping_point_premium(
    ile: float,
    ibgr: float,
    kappa: float,
) -> float:
    """
    Critical premium below which the system enters death spiral.
    Approximation: pi_crit ≈ log(ILE) - IBGR / kappa.
    """
    if kappa <= 0:
        return float("nan")
    return float(np.log(ile) - ibgr / kappa)


def compute_wacba(
    pi: float,
    ile: float,
    s: float,
    w_atm: float = 0.60,
    w_conv: float = 0.25,
    w_pfd: float = 0.15,
    coupon_conv: float = 0.005,
    div_pfd: float = 0.09,
    r: float = 0.04,
) -> Dict[str, float]:
    """
    Weighted Average Cost of BTC Acquisition.

    Channel costs (per BTC, relative to spot):
    - ATM: S * ELE / exp(pi)  (accretive when pi > log(ELE))
    - Convertible: S * (1 + coupon/r)
    - Preferred: S * (1 + div_rate/r)
    - Ops: S (at cost)

    Returns dict with channel costs and blended WACBA.
    """
    k_atm = s * ile / np.exp(pi)
    k_conv = s * (1.0 + coupon_conv / r)
    k_pfd = s * (1.0 + div_pfd / r)

    # Normalize weights
    w_total = w_atm + w_conv + w_pfd
    w_atm_n = w_atm / w_total
    w_conv_n = w_conv / w_total
    w_pfd_n = w_pfd / w_total

    wacba = w_atm_n * k_atm + w_conv_n * k_conv + w_pfd_n * k_pfd
    wacba_ratio = wacba / s  # ratio to spot

    return {
        "k_atm": float(k_atm),
        "k_conv": float(k_conv),
        "k_pfd": float(k_pfd),
        "wacba": float(wacba),
        "wacba_ratio": float(wacba_ratio),
        "k_atm_ratio": float(k_atm / s),
        "k_conv_ratio": float(k_conv / s),
        "k_pfd_ratio": float(k_pfd / s),
    }
