# TASK: Option Greeks Reinterpretation + ETF Comparison

You are writing two important sections for an academic finance paper about Strategy (MSTR) as a BTC treasury vehicle.

CONTEXT: Read paper/main.tex, paper/sections/methodology.tex, and paper/sections/results.tex. The paper defines several indicators: ILE (Implied Leverage Elasticity), TEE (Total Equity Elasticity), PMRI (Premium Mean-Reversion Index), IBGR (Implied BTC Growth Rate), IFRD (Implied Funding Requirement Distribution).

YOUR TASK: Create two files:

## FILE 1: paper/sections/theory_greeks.tex — Indicators as Option Greeks

The key insight: if the NAV premium represents an accumulation option, then the existing indicators can be reinterpreted as option Greeks. This reframing connects our model to the well-understood options pricing framework.

Develop the following mapping rigorously:

| Indicator | Greek Analogue | Interpretation |
|-----------|---------------|----------------|
| ILE (leverage elasticity) | Delta | Sensitivity of equity to BTC price changes. Like delta of a call option on BTC, amplified by leverage. Derive: ILE = partial(log E) / partial(log S) = A/(A-D) when premium fixed. |
| TEE (total equity elasticity) | Gamma-adjusted Delta | Includes the second-order premium response. TEE = gamma_piS + ILE. When gamma_piS < 0 (as calibrated), TEE < ILE, meaning the premium cushion absorbs some BTC shocks. |
| PMRI (premium mean-reversion) | Theta (time decay) | Measures how far premium is from equilibrium. High PMRI = premium will decay. Like theta: the "carry cost" of holding overpriced premium. |
| IBGR (BTC growth rate) | Moneyness / Intrinsic value | Positive IBGR = accumulation option is in-the-money. The higher the IBGR, the more valuable the option to issue and accumulate. |
| IFRD (funding requirement) | Exercise cost | The dollar cost of "exercising" the accumulation option. Like the strike price of a call. |

For each mapping:
1. State it as a formal Proposition
2. Derive the mathematical connection
3. Explain the economic intuition
4. Show what the calibrated values tell us (reference results: ILE=1.17, TEE=-0.31, PMRI=-1.51, IBGR=18.3%)

Also derive NEW Greeks that the option framework suggests:
- Vega_pi: sensitivity of fair premium to BTC volatility (higher vol -> higher option value -> higher justified premium)
- Rho_premium: sensitivity to interest rates (higher rates -> higher cost of convertible debt -> lower IBGR -> lower fair premium)

## FILE 2: paper/sections/theory_etf_comparison.tex — MSTR vs BTC ETF

This section answers: Why does MSTR trade at a premium when BTC ETFs (IBIT, FBTC, etc.) exist at NAV?

Develop:

1. **ETF as pure delta-one exposure**: ETF NAV = H * S, no premium, no leverage, no accumulation option. Model: E_ETF = A_ETF (trivially).

2. **MSTR premium decomposition**: 
   pi = pi_leverage + pi_accumulation + pi_noise
   Where:
   - pi_leverage = log(ILE) — justified by leverage amplification
   - pi_accumulation = log(1 + V_acc/NAV) — justified by accumulation option value
   - pi_noise = residual — behavioral/momentum/narrative premium

3. **Conditions under which MSTR dominates ETF**: Show that rational investors prefer MSTR over ETF when pi_accumulation > 0 and actual pi < pi_leverage + pi_accumulation (i.e., MSTR is underpriced relative to its option value).

4. **Conditions under which ETF dominates**: When pi > pi_leverage + pi_accumulation (overpriced), or when leverage makes downside too severe, or when dividend obligations erode NAV faster than accumulation grows it.

5. **Use current calibration to assess**: Is MSTR's current premium justified?

Use proper LaTeX formatting with theorems, propositions, equations. 

Commit and push when done.

When completely finished, run: openclaw system event --text "Done: Greeks reinterpretation + ETF comparison completed" --mode now
