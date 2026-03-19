# TASK: Mathematical Review of New Theory Sections

You are reviewing the NEW theoretical sections of an academic finance paper. These sections are the paper's core contribution and will be evaluated by AI reviewers at the UCLA Anderson Fink Center competition.

Read ALL of:
- paper/sections/theory_endogenous_premium.tex
- paper/sections/theory_optimal_capital.tex  
- paper/sections/theory_greeks.tex (if exists)
- paper/sections/theory_etf_comparison.tex (if exists)
- paper/sections/theory_market_impact.tex (if exists)
- paper/sections/model_extended.tex
- paper/sections/methodology.tex (for base model reference)
- results/summary.md (calibrated values to check against)

## Review Checklist

### 1. INTERNAL CONSISTENCY
- Are all variables defined before use?
- Do the new sections use the SAME notation as methodology.tex? (S_t, H_t, pi_t, kappa, theta, sigma_pi, etc.)
- Any symbol conflicts between the theory sections and the base model?
- Do the new theorems/propositions reference the correct equations from the base model?

### 2. MATHEMATICAL RIGOR
- Are proofs complete? Any gaps in logic?
- Are assumptions clearly stated and reasonable?
- Do comparative statics have correct signs? (e.g., higher sigma_S -> higher fair premium)
- Is the reflexivity gain formula correct? Does G < 1 ensure stability?
- Multiple equilibria: is the existence proof rigorous? Saddle-node bifurcation correct?
- Fair premium formula: does pi* = log(1 + V_acc/NAV) follow from the derivation?
- Is the mispricing metric Delta_t well-defined and mean-reverting?

### 3. ECONOMIC REASONABLENESS
- Does the fair premium formula give sensible values for the calibrated parameters?
  (Use: mu_S=0.14, sigma_S=0.49, kappa=4.08, theta=0.71, rho=-0.49, gamma_piS=-1.48, lambda_M=17.3, E[DH]=6887, ILE=1.17, current pi=0.24)
- Plug in: what is pi* approximately? Is it positive? Is Delta_t = pi - pi* reasonable?
- Does the tipping point formula give a credible critical premium level?
- Do the option Greeks analogies hold up? (ILE as Delta makes sense, but does PMRI as Theta?)
- Is the ETF comparison fair? (ETFs have no accumulation option, but also no leverage risk)

### 4. CROSS-SECTION CONSISTENCY
- Do the theory sections reference each other correctly?
- Is the notation for preferred stock (P_c, P_nc, delta_STRK, etc.) consistent with model_extended.tex?
- Are the new indicators (CSLR, PCR, WACBA, ELE) consistently defined across sections?

### 5. LaTeX ISSUES
- Duplicate labels?
- Missing references?
- Undefined commands or environments?
- Will the paper compile cleanly with all sections included?

Write your review to paper/THEORY_REVIEW.md. Fix all errors directly in the .tex files. Be rigorous — this is what separates a B paper from an A paper.

Commit and push when done.

When completely finished, run: openclaw system event --text "Done: Theory review completed" --mode now
