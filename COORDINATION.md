# Paper Coordination

## Deadline: March 18, 2026, 11:59 PM PT (TONIGHT)
## Target: Human × AI Finance Competition at UCLA Anderson

## Repo Structure
- `plan.tex` — original model spec (implementation plan format)
- `paper/` — final paper output (LaTeX + PDF)
- `src/` — Python pipeline code
- `data/` — raw and processed data
- `results/` — figures, indicators, params

## Branch Assignment
- `research` — Research agent: data collection, lit review materials, Strategy capital structure
- `model` — Model agent: extended math, priority waterfall, preferred stock dynamics
- `paper` — Paper agent: restructure into academic paper format
- `data-code` — Data/Code agent: update pipeline, new data, run results

## Key Model Extensions Needed
1. **Preferred Stock Layer**: STRK (8% convertible), STRF (10% non-convertible), STRC, STRD, STRE
2. **Priority Waterfall**: Liquidation/distribution ordering preferred > common
3. **Dividend Obligations**: Fixed perpetual dividends change survival/distress definitions
4. **Multi-channel Financing Flywheel**: ATM equity + convertible bonds + preferred stock issuance
5. **Conversion Optionality**: STRK conversion into MSTR common (0.1 shares per STRK)

## Strategy's Current Capital Stack (as of early 2026)
- MSTR (common equity) — levered BTC exposure
- STRK ("Strike") — 8% convertible perpetual preferred, converts to 0.1 MSTR/share
- STRF ("Strife") — 10% non-convertible perpetual preferred
- STRC ("Stretch") — additional preferred layer
- STRD — high yield preferred
- STRE ("Stream") — EUR-denominated preferred (~€80/share)
- Multiple convertible bonds outstanding
- ATM equity program (21/21 plan → expanded)

## File Conventions
- Each agent works on its own branch
- Paper LaTeX goes in `paper/main.tex`
- New model math goes in `paper/sections/model.tex`
- Figures go in `results/figures/`
