# Mathematical Review: Multi-Layer Structural Framework for BTC Treasury Vehicles

**Reviewer**: Math Reviewer (AI Agent)
**Date**: 2026-03-18
**Status**: Review complete, critical fixes applied

---

## CRITICAL ISSUES (Fixed)

### 1. Accretion Condition Error (model_extended.tex, Proposition 5)

**Location**: `paper/sections/model_extended.tex`, lines 380-408 (eq:accretive and proof)

**Issue**: The proposition claims ATM issuance is accretive iff $\pi_t > 0$. This is **WRONG** when $D_t > 0$.

The derivation correctly shows the accretion condition is $E_t > A_t = H_t S_t$. But $\pi_t > 0$ means $E_t > \text{NAV}_t = (A_t - D_t)^+$, which is a **weaker** condition.

**Correct condition**: $\pi_t > \log(\text{ILE}_t) = \log\!\bigl(A_t/(A_t - D_t)\bigr)$.

When $D_t > 0$, this threshold is strictly positive. For the current calibration with ILE = 1.172, the threshold is $\log(1.172) \approx 0.159$, not zero.

**Economic significance**: The paper currently overstates the ease of accretive issuance. A firm with $\pi_t = 0.1$ (10% premium to NAV) and ILE = 1.17 would be told issuance is accretive when it is actually dilutive.

**Fix applied**: Corrected the proposition, proof, and displayed equation chain.

### 2. Literature Review Sign Error (literature_review.tex, line 31)

**Location**: `paper/sections/literature_review.tex`, line 31

**Issue**: States "$\pi_t$ positively correlated with BTC returns ($\rho > 0$)" but the calibrated value is $\rho = -0.491$ and the entire paper discusses negative correlation.

**Fix applied**: Changed to $\rho < 0$.

### 3. Conversion-Adjusted NAV Missing OTM Preferred Claim (model_extended.tex, Def 8)

**Location**: `paper/sections/model_extended.tex`, eq:ca_nav (line 249-252)

**Issue**: The formula for $\text{NAV}_t^{CA}$ subtracts $D_s, D_c, P_{nc}$ from the numerator but never subtracts $P_c$ (convertible preferred par). When STRK is out-of-the-money, its par claim still exists but is not deducted, overstating NAV.

**Fix applied**: Added $P_c^{OTM}(t)$ deduction to the numerator.

---

## MODERATE ISSUES (Fixed)

### 4. Dual Use of $\varepsilon$ Symbol

**Location**: methodology.tex lines 32-40 (NAV floor) and lines 181-183 (distress buffer)

**Issue**: $\varepsilon$ is used for two distinct quantities:
- NAV clipping floor (small positive constant to avoid log singularities)
- Distress buffer parameter in $A_t \le (1+\varepsilon)D_t$

**Fix applied**: Renamed the distress buffer to $\varepsilon_d$ throughout methodology.tex to disambiguate.

### 5. Half-Life Units Error

**Location**: results.tex line 46, discussion.tex line 12

**Issue**: States "half-life of approximately $\ln 2 / \kappa \approx 62$ trading days". With $\kappa = 4.081$: $\ln 2 / 4.081 = 0.170$ years $= 62$ **calendar** days $= 43$ trading days. The text says "trading days" which is wrong.

**Fix applied**: Changed to "calendar days" in both locations.

### 6. Equity Identity Inconsistency

**Location**: methodology.tex, eq:equity_identity (line 118)

**Issue**: The identity writes $E_t = e^{\pi_t}(H_tS_t - D_t)^+$, but $\pi_t$ is defined using $\text{NAV}_t^{clip}$ (with floor $\varepsilon$). These are inconsistent when $0 < A_t - D_t < \varepsilon$.

**Fix applied**: Added clarifying note that the identity holds exactly outside the distress regime (where $\text{NAV}_t > \varepsilon$) and approximately otherwise.

### 7. Table Label Conflict

**Location**: results.tex `\label{tab:indicators}` and model_extended.tex `\label{tab:indicators}`

**Issue**: Duplicate LaTeX label. If both files are included, cross-references will be ambiguous.

**Fix applied**: Renamed the model_extended table label to `tab:indicators_extended`.

### 8. Literature Review Not Included in main.tex

**Location**: main.tex (between introduction and methodology inputs)

**Issue**: `literature_review.tex` exists but is not `\input{}`-ed. The introduction references numbered sections that assume it's present.

**Fix applied**: Added `\input{sections/literature_review}` to main.tex.

### 9. model_extended.tex Not Included in main.tex

**Location**: main.tex

**Issue**: The extended model section is written but not included in the compiled paper.

**Fix applied**: Added `\input{sections/model_extended}` to main.tex after methodology.

---

## MINOR ISSUES (Noted, not all fixed)

### 10. $\eta_\pi$ Not Formally Defined

**Location**: methodology.tex line 60

The jump term $\eta_\pi dJ_t^\pi$ introduces $\eta_\pi$ without formal definition. Since jumps are set to zero at baseline, this is acceptable, but adding "where $\eta_\pi$ is the jump size scaling parameter" would improve clarity.

**Status**: No fix needed for submission; jump process disabled at baseline.

### 11. Flywheel Decomposition Proof Assumption

**Location**: model_extended.tex, Theorem 1 proof (lines 553-558)

The proof assumes preferred dividends reduce $A_t = H_tS_t$ (i.e., BTC is sold to pay dividends). This assumption should be stated explicitly since in practice dividends may be paid from operating cash flow or new issuance.

**Status**: Noted. The $O(dt)$ term absorbs second-order corrections, but the dividend-from-assets assumption is substantive and should be acknowledged.

---

## MATHEMATICAL CONSISTENCY SUMMARY

| Component | Status | Notes |
|-----------|--------|-------|
| OU premium dynamics | OK | Correct transition density, mean-reversion specification |
| ILE derivation | OK | Correct partial derivative of log equity w.r.t. log BTC |
| TEE decomposition | OK | Correctly adds $\gamma_{\pi S}$ (regression coefficient) to ILE |
| PMRI formula | OK | Correct z-score using OU stationary std dev $\sigma_\pi/\sqrt{2\kappa}$ |
| IBGR formula | OK | Correct conditional expectation from holding dynamics |
| IFRD integral | OK | Correct Stieltjes integral decomposition |
| Survival/distress | OK | Standard first-passage formulation (after $\varepsilon_d$ rename) |
| Accretion condition | FIXED | Was incorrect; now uses $\pi_t > \log(\text{ILE}_t)$ |
| Waterfall algebra | OK | Correct recursive residual computation |
| ELE ordering proof | OK | Correct monotonicity argument |
| Conversion-Adjusted NAV | FIXED | Added OTM preferred deduction |
| Flywheel decomposition | OK | Correct Ito's lemma application with $O(dt)$ absorbing corrections |

## ECONOMIC LOGIC ASSESSMENT

- **OU mean-reversion for premium**: Economically sound. Closed-end fund literature supports mean-reverting premia. The fast reversion ($\kappa = 4.08$) is plausible given the high-attention, liquid nature of MSTR.
- **Flywheel mechanism**: Correctly modeled. Premium-driven accumulation with discrete financing events matches observed behavior.
- **Negative $\rho$**: Economically sensible. BTC rallies mechanically increase NAV faster than equity adjusts, compressing the premium ratio.
- **Survival conditions**: Reasonable. The 99.4% three-year survival probability is consistent with the 6.8x asset/debt ratio, though it doesn't account for preferred dividend stress (which the extended model addresses).
- **Preferred stock extensions**: Financially sound. The priority waterfall, conversion optionality, and dividend coverage framework are standard corporate finance constructs correctly adapted to the BTC treasury setting.

## CALIBRATION NOTES

- $\gamma_{\pi S} = -1.48$ is large in magnitude. A 1% BTC increase associated with a 1.48pp premium decrease means BTC rallies are more than offset in premium terms. This produces the counterintuitive negative TEE ($-0.31$). The paper acknowledges this and interprets it correctly, but the stability of this estimate should be tested with rolling windows.
- The per-share IBGR (18.4%) being nearly identical to total IBGR (18.3%) is an empirical finding, not a model prediction. The model correctly allows these to diverge; the near-equality reflects Strategy's historical execution.

---

*Review completed 2026-03-18. Critical fixes have been applied directly to the .tex files.*
