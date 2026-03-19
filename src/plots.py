from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Use a consistent seaborn theme for readability.
sns.set_theme(context="talk", style="whitegrid", font_scale=0.9)


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def plot_core_timeseries(
    panel: pd.DataFrame,
    ile: Optional[pd.Series],
    tee: Optional[pd.Series],
    outdir: Path,
) -> None:
    """
    Generate core time-series plots from the historical panel.

    - Assets vs debt vs NAV.
    - Premium (pi_t).
    - BTC per share.
    - ILE and TEE (if provided).
    """
    _ensure_dir(outdir)

    # 1. Assets, debt, NAV (in billions for readability).
    fig, ax = plt.subplots(figsize=(9, 4))
    scale = 1e9
    assets = panel["asset_btc_usd"] / scale
    debt = panel["debt_total_usd"] / scale
    nav = panel["nav"] / scale

    ax.plot(panel.index, assets, label="BTC assets $A_t$", linewidth=2.0)
    ax.plot(panel.index, debt, label="Debt $D_t$", linewidth=2.0)
    ax.plot(panel.index, nav, label="NAV $(A_t-D_t)^+$", linewidth=2.0)
    ax.set_title("BTC Assets, Debt, and NAV (USD billions)")
    ax.set_ylabel("USD billions")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(outdir / "assets_debt_nav.png", dpi=200)
    plt.close(fig)

    # 2. Premium.
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.plot(panel.index, panel["premium"], color=sns.color_palette()[3], linewidth=2.0)
    ax.axhline(0.0, color="black", linestyle="--", linewidth=1.0, alpha=0.7)
    ax.set_title(r"Premium over time: $\pi_t = \log(E_t / \mathrm{NAV}_t^{\mathrm{clip}})$")
    ax.set_ylabel("log premium")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(outdir / "premium_timeseries.png", dpi=200)
    plt.close(fig)

    # 3. BTC per share, with annotation of 2024 stock split if present.
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.plot(panel.index, panel["btc_per_share"], color=sns.color_palette()[2], linewidth=2.0)
    ax.set_title(r"BTC per share $B_t = H_t/N_t^{\mathrm{sh}}$")
    ax.set_ylabel("BTC per share")
    ax.grid(True, alpha=0.3)

    split_date = pd.Timestamp("2024-08-08")
    if split_date in panel.index:
        ax.axvline(split_date, color="grey", linestyle="--", linewidth=1.2, alpha=0.8)
        ax.text(
            split_date,
            ax.get_ylim()[1] * 0.9,
            "10-for-1 split",
            rotation=90,
            va="top",
            ha="right",
            fontsize=8,
            color="grey",
        )

    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(outdir / "btc_per_share_timeseries.png", dpi=200)
    plt.close(fig)

    # 4. ILE and TEE if available.
    if ile is not None and tee is not None:
        aligned = pd.concat([ile.rename("ILE"), tee.rename("TEE")], axis=1)
        fig, ax = plt.subplots(figsize=(9, 3.5))
        ax.plot(aligned.index, aligned["ILE"], label="ILE (structural leverage)", linewidth=2.0)
        ax.plot(aligned.index, aligned["TEE"], label="TEE (total equity elasticity)", linewidth=2.0)
        ax.axhline(0.0, color="black", linestyle="--", linewidth=1.0, alpha=0.7)
        ax.set_title("Leverage and Total Equity Elasticity over Time")
        ax.set_ylabel("beta to BTC")
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.3)
        fig.autofmt_xdate()
        fig.tight_layout()
        fig.savefig(outdir / "ile_tee_timeseries.png", dpi=200)
        plt.close(fig)


def plot_ifrd_histogram(
    G: np.ndarray,
    outdir: Path,
) -> None:
    """
    Plot histogram of the funding requirement distribution G_T.
    """
    _ensure_dir(outdir)

    # Scale to billions for clearer axis.
    scale = 1e9
    G_bil = G / scale

    fig, ax = plt.subplots(figsize=(9, 3.5))
    sns.histplot(G_bil, bins=40, kde=False, color=sns.color_palette()[0], ax=ax)

    mean_val = float(G_bil.mean())
    ax.axvline(mean_val, color="red", linestyle="--", linewidth=1.2, label="Mean")

    ax.set_title("Implied Funding Requirement Distribution $G_T$")
    ax.set_xlabel("Total funding $G_T$ (USD billions)")
    ax.set_ylabel("Number of paths")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(outdir / "ifrd_histogram.png", dpi=200)
    plt.close(fig)

