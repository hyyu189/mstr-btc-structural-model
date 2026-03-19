# TASK: Full Paper Restructure — Theory-First Architecture

You are the FINAL ARCHITECT for an academic finance paper. Your job is to RESTRUCTURE the entire paper from a measurement-first paper into a theory-first paper.

DEADLINE: TONIGHT. This is the most important task.

## Context

Read ALL files in paper/sections/ — there are many .tex files written by different agents. The paper currently reads like: "we built a measurement framework, and oh here's some theory too." It needs to read like: "we propose a pricing theory, and here's empirical validation."

Also read:
- paper/main.tex (current structure)
- results/summary.md (calibrated values)
- results/indicators.json

## New Structure

Rewrite paper/main.tex and ALL section files to implement this architecture:

```
1. ABSTRACT (rewrite — lead with theory, not measurement)
   "We develop a theory of endogenous premium formation in Bitcoin treasury vehicles..."

2. INTRODUCTION (rewrite — the story is the theory)
   - Hook: Strategy holds $56B in BTC, trades at persistent premium. Why?
   - Research question: What determines the fair premium? When is it justified?
   - Central insight: Premium = PV of perpetual accumulation option
   - Contribution: (1) endogenous premium theory, (2) reflexivity + multiple equilibria, (3) indicator framework as option Greeks, (4) empirical calibration, (5) optimal capital structure implications
   - Paper outline matching new structure

3. LITERATURE REVIEW (lightly reframe)
   - Add: gap in theoretical understanding of BTC treasury premiums
   - Connect to: real options, reflexivity (Soros), structural credit models

4. THE MODEL (theory_endogenous_premium.tex is the CORE — put it here)
   4.1 Setup and State Variables (from old methodology, keep brief)
   4.2 The Perpetual Accumulation Option (from theory_endogenous_premium.tex)
   4.3 Fair Premium Derivation
   4.4 Reflexivity and Multiple Equilibria
   4.5 Indicators as Option Greeks (from theory_greeks.tex if exists)
   4.6 BTC ETF vs Treasury Vehicle (from theory_etf_comparison.tex if exists)
   4.7 Optimal Capital Structure (from theory_optimal_capital.tex if exists)

5. EMPIRICAL FRAMEWORK
   5.1 Data and Variable Construction (from old methodology — the SDE specs, OU, holding dynamics)
   5.2 Estimation Strategy (calibration approach)
   5.3 Capital Structure (preferred stock details from model_extended.tex)

6. RESULTS AND VALIDATION
   6.1 Calibrated Parameters (from old results — but now framed as "do they validate the theory?")
   6.2 Fair Premium Estimation (new — apply the theory formula to get pi_star)
   6.3 Mispricing Analysis (new — Delta_t = pi_t - pi_star)
   6.4 Indicator Analysis as Greeks (ILE as Delta, PMRI as Theta, etc.)
   6.5 Survival and Distress (from old results)

7. DISCUSSION
   - Does the theory hold? (compare pi_star to observed pi)
   - Multiple equilibria: where is MSTR currently? (stable flywheel or near tipping point?)
   - Implications for BTC ETF vs treasury vehicle investors
   - What should management do? (optimal capital structure prescriptions)
   - Systemic risk if more companies adopt the model
   - Limitations and future work

8. CONCLUSION (rewrite — theory-forward)
```

## New Title

"A Theory of Endogenous Premium in Bitcoin Treasury Vehicles: Accumulation Options, Reflexive Equilibria, and Capital Stack Dynamics"

Author: Haiyang Yu, UCLA Anderson School of Management

## Critical Rules

1. DO NOT DELETE any mathematical content. Every equation, theorem, proposition from every section file must appear in the final paper. Reorganize, don't discard.

2. The narrative arc must be: THEORY -> EMPIRICS -> VALIDATION, not EMPIRICS -> THEORY

3. The abstract should make a reader think "this is a theory paper with empirical validation" not "this is an empirical paper with some theory"

4. If theory_greeks.tex, theory_etf_comparison.tex, or theory_optimal_capital.tex don't exist yet, create placeholder subsections with the key ideas (2-3 paragraphs each) based on methodology.tex and model_extended.tex content.

5. Recompile the PDF when done: PATH=/Library/TeX/texbin:$PATH && cd paper && pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex

6. Commit everything and push.

When completely finished, run: openclaw system event --text "Done: Paper restructured — theory-first architecture complete" --mode now
