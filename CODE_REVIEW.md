# Code Review: MSTR BTC Structural Model Pipeline

**Reviewer:** Claude Code
**Date:** 2026-03-18
**Branch:** `paper`
**Pipeline test:** `python -m src.run_pipeline` — **PASSES** (no errors)

---

## 1. CORRECTNESS

### 1.1 NAV Calculation — CORRECT
`preprocessing.py:119-124`
- `nav_raw = asset_btc_usd - debt_total` matches plan.tex: `NAV_t = (A_t - D_t)^+`
- `nav = nav_raw.clip(lower=0.0)` correctly implements the `max(·, 0)` operator
- `nav_clip = np.maximum(nav_raw, nav_floor)` with floor=1.0 prevents log singularities
- Premium: `pi_t = log(E_t / NAV_clip)` matches plan.tex equation

### 1.2 OU Calibration — CORRECT (AR(1) equivalent to exact MLE)
`calibration.py:97-133`
- Uses AR(1) OLS: `π_{t+1} = a + b*π_t + eps`, then recovers `κ = -log(b)/Δt`, `θ = a/(1-b)`
- This is algebraically equivalent to conditional Gaussian MLE on the exact OU transition density:
  `π_{t+Δt} = θ + (π_t - θ)e^{-κΔt} + σ_π √((1-e^{-2κΔt})/(2κ)) · Z_t`
- Sigma recovery `σ = sqrt(resid_var * 2κ / (1 - e^{-2κΔt}))` correctly inverts the conditional variance formula
- Guard `b = clip(b, 1e-6, 1-1e-6)` at line 124 prevents `log(0)` and negative kappa

### 1.3 Holding Jump Statistics — CORRECT with one data caveat
`calibration.py:176-247`
- Event identification via `delta_h != 0` is correct
- Jump intensity `λ_M = N_events / T_years` matches plan.tex
- **DATA NOTE:** Purchase history row for 2022-12-22 shows `-704` BTC (a sale). This negative value is included in `mean_jump_size`, pulling the average slightly down. Consider filtering to positive purchases only for the flywheel model, since the model assumes `ΔH ≥ 0`.

### 1.4 Simulation — CORRECT
`simulation.py:62-141`
- Cholesky decomposition for correlated Brownians: correct
- GBM exact discretization: `S_{t+1} = S_t exp((μ-½σ²)Δt + σ√Δt · Z_S)` — correct
- OU exact discretization: `π_{t+1} = θ(1-e^{-κΔt}) + e^{-κΔt}π_t + σ_ou_std · Z_π` — correct, uses precomputed constants
- Holdings: continuous drift + Poisson jumps with constant jump size — matches plan.tex
- `H[t+1,:] = max(h_cont + h_jump, 0.0)` enforces non-negativity — correct

### 1.5 IBGR per-share — CORRECT
`indicators.py:61-86`
- `growth = (B_T - B0) / (T * B0)` with `mean(growth)` matches:
  `μ_{H/N} = (1/B0) E[(B_T - B0)/T]` since B0 is constant across paths at t=0

### 1.6 IFRD — CORRECT
`indicators.py:89-112`
- `G = (S * dH).sum(axis=0)` matches discrete approximation: `G ≈ Σ S_{t_k}(H_{t_{k+1}} - H_{t_k})`

### 1.7 Survival Probability — CORRECT
`indicators.py:115-137`
- Checks `A_t ≤ (1+ε)D_t` at all times, any breach fails the path — matches plan.tex

---

## 2. NUMERICAL ISSUES

### 2.1 Division by zero in ILE — MINOR
`indicators.py:21-23`
```python
ile = asset / denom         # produces inf when denom=0
ile[denom <= 0.0] = np.nan  # then overwritten
```
NumPy handles this (inf → NaN), but a `np.where` would be cleaner.

### 2.2 exp() overflow risk in simulation — LOW RISK
`simulation.py:139`: `E[t+1,:] = np.exp(PI[t+1,:]) * NAV[t+1,:]`
With calibrated OU (κ≈4, θ≈0.7, σ≈1.4), extreme premium values are rare but possible. No explicit clamp. At current parameters, `exp(PI)` could overflow for `PI > 709`. The OU mean-reversion makes this astronomically unlikely over 3 years, but a `np.clip(PI, -50, 50)` guard would be defensive.

### 2.3 Random seed handling — GOOD
`simulation.py:62`: Uses `np.random.default_rng(42)` — modern, isolated RNG. No global state contamination.

---

## 3. DATA QUALITY

### 3.1 CSV files — COMPLETE and CONSISTENT
| File | Rows | Date Range | Notes |
|------|------|-----------|-------|
| `3-month-tbill-yield-curve.csv` | 1,305 | 2020-12-04 to 2025-12-01 | Clean, no gaps |
| `mstr-balance-sheet-basic.csv` | 19 | 2021-Q1 to 2025-Q3 | Quarterly, all fields present |
| `mstr-btc-holdings-over-time.csv` | 100 | 2020-08-10 to 2025-12-01 | BOM on first column (handled) |
| `mstr-btc-purchase-history.csv` | 88 | 2020-08 to 2025-12 | Tab-delimited, date ranges handled |
| `mstr-daily-price&shares.csv` | 1,238 | 2021-01-04 to 2025-12-01 | Compustat format, split-adjusted via cshoc |

### 3.2 Forward-fill logic — CORRECT
- `preprocessing.py:91-110`: All series are reindexed to a common daily DatetimeIndex and forward-filled. This correctly handles weekends and holidays for MSTR price and T-bill data.
- Debt is quarterly → forward-filled daily: correct for piecewise-constant modeling.

### 3.3 Date alignment — CORRECT
- Panel range is `max(holdings_start, mstr_start)` to `min(btc_end, mstr_end, rf_end, end_date)`, ensuring no NaN from misalignment.

### 3.4 MEDIUM: Preferred stock not subtracted from NAV
`preprocessing.py:119-121` computes `nav_raw = asset_btc_usd - debt_total` but does NOT subtract preferred stock liquidation preferences (~$5.5B per `data/capital_structure_2026.json`). The base model in `plan.tex` only has debt, but the extended model (`model_extended.tex`) requires:
```
NAV = A_t - D_t - P_nc - P_c
```
For the base paper this is acceptable; for the extended model this is a gap worth noting.

### 3.5 MEDIUM: BTC price fetched from remote URL at runtime
`data_io.py:194`: `load_btc_daily()` downloads from `https://www.cryptodatadownload.com/cdd/Binance_BTCUSDT_d.csv` every time the pipeline runs. **If this URL changes or goes down, the pipeline breaks.** Should include a local CSV fallback or cache.

---

## 4. REPRODUCIBILITY

### 4.1 Pipeline execution — PASSES
```
$ python -m src.run_pipeline
```
Runs end-to-end, produces `results/params.json`, `results/indicators.json`, `results/summary.md`, `results/figures/*.png`.

### 4.2 Random seed — SET
`SimulationConfig.random_seed = 42` with `np.random.default_rng()`. Fully deterministic given the same input data.

### 4.3 MEDIUM: Dependencies not pinned
`requirements.txt` lists packages without versions:
```
numpy
pandas
scipy
statsmodels
matplotlib
seaborn
```
Different versions of numpy/scipy could produce different numerical results. Pin versions for reproducibility (e.g., `numpy==1.26.4`).

### 4.4 MINOR: yfinance listed but unused
`yfinance` is in `requirements.txt` but not imported anywhere in the codebase.

### 4.5 MEDIUM: No local BTC price CSV
BTC data comes from a URL (see 3.5). If running offline or if the URL changes format, the pipeline fails. The other data sources are all local CSVs.

---

## 5. ISSUES SUMMARY

### Critical (must fix)
None — pipeline runs correctly and produces reasonable calibrated values matching the published results.

### Medium (should fix before submission)
| # | File | Issue |
|---|------|-------|
| M1 | `data_io.py:194` | BTC price from remote URL — add local CSV fallback |
| M2 | `requirements.txt` | Dependencies not pinned — add version constraints |
| M3 | `calibration.py:241` | Negative BTC purchase (-704) included in mean jump size — filter to positive |
| M4 | `preprocessing.py:120` | No preferred stock in NAV — acceptable for base model but document the limitation |

### Minor (nice to fix)
| # | File | Issue |
|---|------|-------|
| m1 | `indicators.py:21` | Division before NaN guard in ILE — use `np.where` |
| m2 | `simulation.py:139` | No exp() overflow clamp on premium — add `np.clip` |
| m3 | `requirements.txt` | `yfinance` unused — remove |
| m4 | `data_io.py:9` | `DATA_ROOT = Path(".")` — fragile if CWD changes |

---

## 6. CALIBRATED OUTPUT VERIFICATION

The pipeline output matches the values in `paper/sections/results.tex`:

| Parameter | Pipeline | Paper | Match |
|-----------|----------|-------|-------|
| μ_S | 0.140 | 0.140 | YES |
| σ_S | 0.488 | 0.488 | YES |
| κ | 4.081 | 4.081 | YES |
| θ | 0.705 | 0.705 | YES |
| σ_π | 1.417 | 1.417 | YES |
| ρ | -0.491 | -0.491 | YES |
| γ_πS | -1.480 | -1.480 | YES |
| λ_M | 17.29 | 17.3 | YES |
| E[ΔH] | 6,887 | 6,887 | YES |
| IBGR | 18.3% | 18.3% | YES |
| ILE | 1.172 | 1.172 | YES |
| Survival (3y) | 99.42% | 99.42% | YES |

All values match to reported precision.

---

## 7. VERDICT

**The pipeline is correct and ready for use.** The math implementation faithfully follows `plan.tex`. There are no critical bugs. The medium-priority issues (remote BTC data, unpinned deps, negative jump) should be addressed before final submission but do not affect the validity of current results.
