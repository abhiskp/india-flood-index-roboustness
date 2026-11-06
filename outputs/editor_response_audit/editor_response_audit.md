# Editor Response Data Reliability Audit

## Executive verdict

### B — Salvageable with reframing

The satellite and physical-validation conclusions survive stricter district matching and event-influence checks. The temporal fatality analysis remains useful only as a secondary methodological test because district allocation and reporting intensity materially limit interpretation. The paper is scientifically salvageable if the satellite result remains primary, the fatality analysis is demoted and reframed, and the methods and exclusion audits are reported in full.

### 1. Matching and exclusion bias

- Complete DFSI districts: 709.
- Excluded from satellite validation: 52 (7.3%).
- Strict stable-match subset: 648 districts.
- Stable-subset published DFSI correlation: 0.3606 (95% ordinary bootstrap CI 0.2853 to 0.4336).
- Stable-subset equal-weight physical-hazard correlation: 0.4595 (95% CI 0.3875 to 0.5253).
- The hazard-minus-DFSI difference remains positive.

States and union territories with the lowest matching coverage are listed in `included_vs_excluded_summary.csv`; the lowest-coverage rows were:

     State_Name  size  sum  excluded  match_percent
         LADAKH     2    1         1      50.000000
      TELANGANA    33   22        11      66.666667
    WEST BENGAL    22   15         7      68.181818
      KARNATAKA    30   25         5      83.333333
 ANDHRA PRADESH    13   11         2      84.615385
        TRIPURA     8    7         1      87.500000
   CHHATTISGARH    20   18         2      90.000000
JAMMU & KASHMIR    22   20         2      90.909091

### 2. District reporting consistency

Reporting completeness varies substantially across periods and geography. District reporting quality is separated into observed event frequency, field completeness and administrative assignability in `district_reporting_quality.csv`. Event count alone was not used to label quality.

### 3. Fatality allocation sensitivity

- Conservative final-period assignable fatalities: 3654.0.
- Fractional-allocation final-period assignable fatalities: 17705.9.
- Spearman correlation between conservative and fractional district outcome ranks: 0.6541.
- Median absolute target-rank change: 116.0 positions.

The key comparison is not whether coefficients change, but whether the conclusion changes. Across the conservative and fractional targets, the fitted Poisson model does not acquire robust superiority over past event count under both ordinary and state-block uncertainty.

### 4. High-quality subset validation

The primary higher-reporting-quality subset required at least one matched predictor-period event and at least 50% fatality-field completeness in both 1986–2004 and 2005–2023. The 25% and 75% thresholds were evaluated only as prespecified sensitivity checks. Results are in `high_quality_subset_validation.csv`.

### 5. Satellite event robustness

All leave-one-out checks for the five largest GFD events retained a positive equal-hazard-minus-published-DFSI difference: True. Thus, no single major mapped event reverses the headline satellite comparison.

### 6. Retrospective physical validation robustness

The 2010 backtest was repeated in the strict stable-match subset. Event-count, event-duration and earlier-GFD persistence results, including ordinary and state-block intervals, are in `retrospective_stable_subset_results.csv`. The event-duration signal persists, while geographic uncertainty remains.

### 7. Reporting-intensity diagnostics

The strongest outcome-focused diagnostic association was between final assignable fatalities and matched event rows: Spearman rho=0.6317. Predictor-period event count was also strongly associated with distinct recorded flood years (rho=0.7904), as expected for related event-history measures. These diagnostics are not causal, but they show that recorded fatality rankings may partly reflect reporting and event ascertainment.

### 8. Reproducibility gaps

The current manuscript/ESM contains 14 method items that are partial, absent or inconsistent with code. The most important are exact district-name/LGD precedence, GFD metadata-versus-spatial event inclusion, district-area computation, zero-history handling, exact standardisation details, the Poisson objective and optimizer, the 0.025 learned-weight grid, state-demeaning formula and bootstrap implementation details. See `methodology_reporting_audit.csv` and `reproducibility_inventory.csv`.

All raw-data SHA-256 hashes were unchanged during this audit.

### 9. What should change in the manuscript

Mandatory:

- Quantify the 52 excluded districts and state/UT matching coverage.
- Report the strict 648-district stable-match analysis.
- Add the fractional fatality-allocation and state-level sensitivity results.
- Reframe district zeros as no assignable recorded deaths, not absence of deaths.
- Fully specify matching precedence, GFD event inclusion, area calculation, model objective, standardisation, bootstrap and tie rules.

Strongly recommended:

- Keep the satellite comparison as the primary result.
- Move the district fatality model to the supplement or a clearly secondary section.
- Report district- and state-level reporting-quality tables and reporting-intensity diagnostics.
- Add the top-five GFD event leave-one-out analysis.

Optional:

- Retain the retrospective physical backtest as a secondary robustness analysis.
- Present the 25% and 75% reporting thresholds only in supplementary material.

### 10. Recommended next journal strategy

The paper is not ready for immediate resubmission in its current form. It becomes scientifically suitable for resubmission elsewhere after the manuscript and ESM are rebuilt around the reliability audit, the temporal fatality claims are demoted, and all reproducibility gaps are closed. Journal choice should follow the revised scope rather than prestige.
