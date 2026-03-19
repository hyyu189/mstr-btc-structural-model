# TASK: Optimal Capital Structure + Market Impact

You are writing two sections for an academic finance paper about Strategy (MSTR) as a BTC treasury vehicle.

CONTEXT: Read paper/main.tex, paper/sections/methodology.tex, and paper/sections/model_extended.tex. Strategy uses multiple financing channels: ATM equity, convertible bonds, and 5 tiers of preferred stock (STRK 8% convertible, STRF 10% non-convertible, STRC 9.6%, STRD 10%, STRE 10% EUR-denominated). Each has different cost of capital and dilution impact.

YOUR TASK: Create two files:

## FILE 1: paper/sections/theory_optimal_capital.tex — Optimal Capital Structure

Extend the Leland (1994) / Leland-Toft (1996) framework to BTC treasury vehicles:

### 1. Cost of Capital for Each Channel
Define the effective cost of BTC acquisition for each financing channel:

For ATM equity issuance:
- Cost = dilution to existing shareholders
- When pi > log(ILE), issuance is accretive (cost is negative — you're getting BTC "for free" by issuing overpriced equity)
- When pi < log(ILE), issuance is dilutive

For convertible bonds:
- Cost = coupon + expected dilution at conversion
- Conversion probability depends on premium path
- Before conversion: fixed coupon cost. After conversion: dilution cost.

For preferred stock (non-convertible):
- Cost = perpetual dividend / proceeds
- STRF at 10% = 10% perpetual cost of capital
- Increases fixed obligations, raises distress probability

For convertible preferred (STRK):
- Hybrid: 8% dividend + conversion optionality
- If converted: removes dividend obligation but adds dilution
- Effective cost depends on premium regime

### 2. Optimal Financing Rule
Derive the optimal channel selection as a function of the state (pi_t, S_t, ILE_t):

Proposition: The optimal financing channel is:
- ATM equity when pi_t > pi_equity_threshold (premium high enough for accretive issuance)
- Convertible bonds when pi_t is moderate (locks in low coupon, conversion upside shared)
- Preferred stock when pi_t is low or negative (cannot issue common equity attractively)

Derive the threshold values. Show that Strategy's observed behavior approximately follows this rule.

### 3. Weighted Average Cost of BTC Acquisition (WACBA)
Define WACBA as the blended cost across all channels, analogous to WACC:

WACBA_t = sum_c (w_c * k_c(pi_t, S_t))

where w_c is the fraction of BTC acquired through channel c and k_c is the channel-specific cost.

Show that management minimizes WACBA subject to:
- Market capacity constraints (ATM has limited daily volume)
- Leverage constraints (debt/preferred cannot exceed threshold)
- Regulatory constraints

### 4. Endogenous Leverage Dynamics
Show how the capital structure evolves endogenously:
- In bull markets: equity issuance -> leverage falls -> safety increases
- In bear markets: cannot issue equity -> leverage rises (BTC drops but debt stays) -> distress risk rises
- This creates procyclical leverage — connect to Brunnermeier & Pedersen (2009)

## FILE 2: paper/sections/theory_market_impact.tex — BTC Market Impact

### 1. Price Impact of MSTR Accumulation
MSTR is one of the largest BTC buyers. Model the market impact:

dS_t/S_t = mu_S dt + sigma_S dW + eta * (dH_t / V_t)

where V_t is daily BTC trading volume and eta is the Kyle (1985) lambda (price impact coefficient).

### 2. Estimate eta
Use available data:
- Average MSTR purchase size: ~6,887 BTC per event (from calibration)
- Daily BTC spot volume: ~$20-30B
- Estimate eta from event study around MSTR purchase announcements

### 3. Reflexivity Amplification Factor
When MSTR buys BTC, BTC price goes up, which increases NAV, which increases premium, which enables more issuance, which enables more buying.

Define the reflexivity amplification factor:
R = 1 / (1 - eta * partial(H)/partial(S) * partial(pi)/partial(NAV) * partial(issuance)/partial(pi))

When R > 1 (which it should be given the parameter estimates), the system amplifies BTC shocks. Show conditions under which R -> infinity (positive feedback loop becomes unstable).

### 4. Systemic Risk Implications
If MSTR holds 3%+ of all BTC and more companies adopt the treasury model:
- What happens to BTC volatility?
- What happens during forced liquidation?
- Connect to Shleifer & Vishny (1997) fire sale literature

Use proper LaTeX with theorems, proofs, propositions.

Commit and push when done.

When completely finished, run: openclaw system event --text "Done: Optimal capital structure + market impact completed" --mode now
