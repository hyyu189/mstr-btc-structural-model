# TASK: Core Pricing Theory — Endogenous Premium

You are building the CORE PRICING THEORY for an academic finance paper.

CONTEXT: Read paper/main.tex and paper/sections/methodology.tex to understand the existing model. The current model treats the NAV premium pi_t as an EXOGENOUS Ornstein-Uhlenbeck process. This is descriptive, not explanatory.

YOUR TASK: Create paper/sections/theory_endogenous_premium.tex — the key theoretical contribution.

## The Central Insight

The NAV premium of a BTC treasury vehicle (like Strategy/MSTR) reflects the market value of a **perpetual accumulation option** — the option to issue equity at a premium and convert proceeds into BTC, thereby increasing BTC-per-share for existing holders.

## What to Derive (be mathematically rigorous, use theorems/propositions/proofs)

### 1. ENDOGENOUS PREMIUM MODEL — The Reflexive System

Replace the exogenous OU with a coupled system of SDEs:

- dS_t/S_t = mu_S dt + sigma_S dW^S + eta * (dH_t/H_t)    — BTC price includes market impact from MSTR buying
- dpi_t = kappa(pi_star(Phi_t) - pi_t) dt + sigma_pi dW^pi  — mean-reversion to ENDOGENOUS equilibrium premium
- dH_t = f(pi_t, S_t) dt + jumps                            — premium-driven accumulation (from existing model)

Where pi_star(Phi_t) is the **equilibrium (fair) premium** that depends on the state Phi_t = (S_t, H_t, D_t, N_t, sigma_S, kappa, ...).

### 2. FAIR PREMIUM DERIVATION

Derive pi_star (the justified premium) as the present value of future accretive issuance:

pi_star = log(1 + V_accretion / NAV)

where V_accretion is the value of the accumulation option. This should depend on:
- BTC volatility sigma_S (higher vol -> more valuable option -> higher fair premium)
- Mean accretion rate IBGR (higher -> higher fair premium)
- Leverage ILE (higher -> amplifies both upside and downside)
- Premium mean-reversion speed kappa (faster reversion -> fewer opportunities -> lower fair premium)

Show conditions under which:
- pi_star > 0 (premium justified — accumulation option has positive value)
- pi_star < 0 (discount — accumulation destroys value, e.g., high dilution or negative IBGR)

### 3. REFLEXIVITY AND MULTIPLE EQUILIBRIA

Prove (or show conditions for) the existence of multiple equilibria:

**High-premium equilibrium**: pi high -> easy issuance -> rapid BTC accumulation -> BTC price support (market impact) -> NAV grows -> premium justified -> stable

**Death spiral equilibrium**: pi low or negative -> cannot issue -> no BTC accumulation -> no growth -> premium compresses -> dilution from convertible bonds -> further compression -> unstable

Characterize the **tipping point** — the critical premium level below which the system transitions from stable to spiral.

### 4. MISPRICING METRIC

Define:
Delta_t = pi_t - pi_star(Phi_t)

This is the **mispricing**: actual premium minus fair premium. Positive = overvalued. Negative = undervalued.
Show how Delta_t evolves and whether it mean-reverts (it should, faster than pi_t itself).

## Writing Style
- Full academic rigor: Definition -> Proposition -> Proof or Proof Sketch
- Use Assumption environments for key assumptions
- Provide economic intuition after each mathematical result
- Reference the existing model notation (S_t, H_t, pi_t, kappa, theta, etc.)
- This section should be 8-12 pages and feel like it could stand as a theory paper on its own

## LaTeX formatting
- Use \newtheorem for Theorem, Proposition, Lemma, Definition, Assumption, Remark, Corollary
- Number equations
- Add \label{} to all numbered equations and results for cross-referencing

Commit and push when done.

When completely finished, run: openclaw system event --text "Done: Theory core - endogenous premium theory completed" --mode now
