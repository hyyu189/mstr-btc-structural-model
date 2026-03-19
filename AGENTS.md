# Agent config for MSTR BTC structural model

## Project purpose
- This repo implements a stochastic structural model of MicroStrategy (MSTR) as a BTC-backed vehicle, estimating IBGR, ILE, PMRI, IFRD, and survival probabilities.

## What you must read first
- Skim the model note (AFP.pdf compiled from plan.tex) for financial background and definitions of S_t, H_t, D_t, NAV, premium, and all indicators.
- Open the latest NAV-corrected notebook and original data files to understand current data schema and any prior fixes.
- Before coding, build a short internal summary of the model equations, required parameters, and available data series.

## Tech stack and environment
- Use Python 3.11+ with a virtual environment (python -m venv .venv) and a single dependency file (pyproject.toml or requirements.txt).
- Prefer numpy, pandas, scipy, statsmodels, and matplotlib/plotly; avoid heavyweight frameworks unless truly needed.
- Add or update dependencies explicitly in the project manifest and document any nonstandard tools in a short README section.
- Ensure all scripts and notebooks run from a clean checkout with no hidden local paths or credentials.

## Core tasks
- Implement a clean data pipeline: load BTC prices, MSTR prices, BTC holdings, debt schedule, and shares; align them on a daily grid; compute NAV, equity, premium, and BTC per share with numerically safe formulas.
- Calibrate the premium OU process, BTC volatility, and holdings dynamics (including jump statistics) following the model note, using robust regressions and clear diagnostics.
- Build a vectorized Monte Carlo engine under the historical measure to simulate joint paths of S_t, π_t, H_t, N_t, D_t, and E_t.
- Compute all indicators (IBGR total and per share, ILE, total equity elasticity, PMRI, IFRD, survival probabilities) and save them as tables and plots under a results/ directory.

## Coding style and numerical best practices
- Favor small, well-named functions and modules over monolithic notebooks; add docstrings, type hints, and comments only where they add clarity.
- Use vectorized numpy/pandas operations instead of Python loops for simulations and statistics; seed random generators for reproducibility.
- Be careful with NAV near zero: never take log of nonpositive values, clip NAV with a small positive floor for plotting, and exclude those points from statistical calibration.
- Validate intermediate results with sanity checks and simple plots (e.g., time series, histograms, scatter plots) before moving on.

## Working with existing files
- Treat the existing NAV-fixed notebook and raw data as reference and ground truth for data cleaning, not as code to copy; reimplement the pipeline in src/ modules where possible.
- If you change any data definitions or formulas, update or create a concise markdown note explaining what changed and why.
- Keep configuration and computation outputs in English; avoid adding Chinese comments or labels in code or plots.

## Quality, tests, and reporting
- For any nontrivial module, add minimal smoke tests or checks (even simple assert-based tests) to avoid silent regressions.
- Prefer deterministic tools (linters, formatters) over LLMs for style; run black/ruff or equivalent before finalizing code.
- At the end of a major change, regenerate key indicators and a short summary notebook or report that demonstrates the full pipeline running end to end.