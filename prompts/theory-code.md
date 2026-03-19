# TASK: Implement New Theory Indicators in Python

You are implementing the NEW theoretical indicators from the paper into the Python pipeline.

Read:
- paper/sections/theory_endogenous_premium.tex — for fair premium, mispricing, reflexivity formulas
- paper/sections/theory_optimal_capital.tex — for WACBA
- paper/sections/model_extended.tex — for CSLR, PCR, ELE
- src/ — existing pipeline code
- results/summary.md — current calibrated parameters and indicators

## What to Implement

### 1. Fair Premium (pi_star)
In src/indicators.py, add compute_fair_premium():

The fair premium is: pi_star = log(1 + V_acc / NAV)

Where V_acc (accumulation option value) depends on:
- IBGR (accretion rate when issuing)
- sigma_S (BTC volatility — higher vol = more option value)  
- kappa (premium mean-reversion — faster = fewer opportunities)
- ILE (leverage amplification)
- A discount rate r

Use the closed-form steady-state approximation from the theory section. If no closed form exists, use a simple approximation:

V_acc / NAV approx= IBGR / (r + kappa) * (1 + sigma_S^2 / (2 * kappa))

where r = risk-free rate (use 0.04 or calibrate from T-bill data).

### 2. Mispricing Metric (Delta_t)
delta_t = pi_t - pi_star_t

Compute this as a time series. Also compute:
- delta_z = delta_t / std(delta_t) — z-score
- Is current delta positive (overvalued) or negative (undervalued)?

### 3. Reflexivity Gain (G)
G = eta * (partial H / partial S) * (partial pi / partial NAV) * (partial issuance / partial pi)

Approximate using calibrated parameters:
- eta: estimate from MSTR purchase size vs daily BTC volume (assume ~0.01-0.05)
- The other partials come from the model

### 4. Effective Mean-Reversion
kappa_eff = kappa * (1 - G)

When G close to 1: slow reversion (reflexive regime)
When G close to 0: fast reversion (efficient regime)

### 5. Tipping Point Premium
The critical premium below which the system enters death spiral.
Use the formula from the theory section, or approximate as:
pi_crit = log(ILE) - IBGR / kappa

### 6. WACBA (Weighted Average Cost of BTC Acquisition)
For each financing channel, compute cost:
- ATM equity: cost depends on premium (accretive when pi > log(ILE))
- Convertible bonds: coupon rate
- Preferred stock: dividend rate
Weight by historical usage proportions.

### 7. Update Pipeline
- Add all new indicators to run_pipeline.py
- Save to results/indicators.json (add new fields)
- Update results/summary.md
- Generate new figure: results/figures/fair_premium_vs_actual.png (time series of pi_t and pi_star_t)
- Generate new figure: results/figures/mispricing_timeseries.png

### 8. Run and Verify
python -m src.run_pipeline must complete without errors.

Commit and push when done.

When completely finished, run: openclaw system event --text "Done: Theory code implementation completed" --mode now
