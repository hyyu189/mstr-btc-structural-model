# Strategy (MSTR) BTC Structural Model -- Summary

**As of date:** 2026-03-17

## Capital Structure

- **BTC Holdings:** 761,068 BTC
- **BTC Price:** $73,909.36
- **BTC Asset Value:** $56.25B
- **Debt:** $8.22B
- **Preferred Liquidation Value:** $10.23B
- **Preferred Annual Dividend:** $976.6M
- **Common Shares:** 320.4M

### Preferred Stock Detail

| Ticker | Div Rate | Shares | Liq Value | Annual Div | Convertible |
|--------|----------|--------|-----------|------------|-------------|
| STRK | 8.0% | 12.8M | $1.28B | $102M | Yes |
| STRF | 10.0% | 10.5M | $1.05B | $105M | No |
| STRC | 9.6% | 50.0M | $5.00B | $479M | No |
| STRD | 10.0% | 25.0M | $2.50B | $250M | No |
| STRE | 10.0% | 5.0M | $0.40B | $40M | No |

## Calibrated Parameters

- **mu_s**: 0.11119021353118116
- **sigma_s**: 0.48649820207568567
- **rho**: -0.3680159137155432
- **gamma_pi_s**: -3.5970287536571397
- **debt_0**: 8222070000.0
- **shares_0**: 320440000.0
- **preferred_liq_0**: 10229353900.0
- **preferred_annual_div_0**: 976573822.0
- **nav_floor**: 1.0
- **ou_kappa**: 5.2136544604770165
- **ou_theta**: 1.0805109745558952
- **ou_sigma**: 3.7943578361266157
- **holdings_alpha**: 0.0
- **holdings_lambda_m**: 19.04976051091006
- **holdings_mean_jump_size**: 7043.551020408163

## Key Indicators

- **current_date**: 2026-03-17
- **S0**: 73909.36
- **H0**: 761068.0
- **D0**: 8222070000.0
- **N0**: 320440000.0
- **preferred_liq_total**: 10229353900.0
- **preferred_annual_div_total**: 976573822.0
- **pi0**: 0.24216726950671505
- **ILE_current**: 1.488150665547579
- **TEE_current**: -2.108878088109561
- **PMRI_current**: -0.7134605135110367
- **IBGR_total_current**: 0.17630219649906664
- **IBGR_per_share_3y**: 0.1761834832175858
- **IFRD_mean**: 35327916376.529175
- **IFRD_p95**: 71779486368.09663
- **survival_prob_3y_eps0**: 0.919
- **survival_prob_3y_eps10pct**: 0.8908
- **dividend_coverage_ratio_current**: 49.18008010712374
- **dividend_coverage_ratio_3y_mean**: 113.69384101704367
- **dividend_coverage_prob_undercovered_3y**: 0.01
- **CSLR_current**: 0.38316159895196006
- **PCR_current**: 7.602036603099638
- **pi_star_current**: 0.03374393122249513
- **mispricing_delta**: 0.2084233382842199
- **mispricing_label**: overvalued
- **mispricing_zscore**: 0.02083237769040124
- **reflexivity_gain_G**: 0.0010064504007562534
- **kappa_effective**: 5.208407175855865
- **tipping_point_premium**: 0.36371871108123177
- **WACBA**: 108617.33462109548
- **WACBA_ratio_to_spot**: 1.4696018829157156
- **WACBA_k_atm**: 86332.52353515911
- **WACBA_k_conv**: 83148.03
- **WACBA_k_pfd**: 240205.42

## Theory Indicators (Endogenous Premium)

- **Fair Premium (pi_star):** 0.0337
- **Actual Premium (pi):** 0.2422
- **Mispricing (Delta):** 0.2084 (overvalued)
- **Mispricing Z-Score:** 0.02
- **Reflexivity Gain (G):** 0.0010
- **Effective Kappa:** 5.2084 (vs raw kappa=5.2137)
- **Tipping Point Premium:** 0.3637
- **CSLR:** 0.3832
- **PCR (3y):** 7.60

### WACBA (Weighted Average Cost of BTC Acquisition)

- **WACBA:** $108,617.33 (1.4696x spot)
- **ATM cost:** $86,332.52 (1.1681x spot)
- **Convertible cost:** $83,148.03 (1.1250x spot)
- **Preferred cost:** $240,205.42 (3.2500x spot)
