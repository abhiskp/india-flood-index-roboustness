# Supplementary Material Outline

This outline is for the first complete manuscript draft. It does not create new analyses or change existing outputs.

## Supplementary Text S1. DFSI Reproduction Workflow

Purpose: document the technical reproduction of the published DFSI without making it the main contribution.

Include:

- Source datasets and immutable raw-data handling.
- District harmonisation and one-to-one baseline construction.
- Complete DFSI equation and component mapping.
- Reproduction metrics.
- Explanation that exact numerical reproduction was not claimed.

Suggested source files:

- `data/processed/dfsi_verified_baseline.csv`
- `outputs/tables/dfsi_verified_discrepancy_summary.csv`
- `outputs/tables/dfsi_verified_top_group_overlap.csv`
- `paper/table_1_reproduction_summary_v2.csv`

## Supplementary Text S2. Satellite Boundary Matching And Export

Purpose: document the GFD/geoBoundaries workflow and limitations.

Include:

- Earth Engine dataset IDs.
- India-related GFD event filtering.
- Permanent-water removal.
- Boundary matching stages.
- Unmatched and ambiguous district records.
- Why the invalid unique-pixel `ever_flooded_area` field was not used.

Suggested source files:

- `gee/11_gfd_external_validation_export.js`
- `gee/11_gfd_external_validation_execution_guide.md`
- `outputs/tables/gfd_boundary_match_audit.csv`
- `outputs/tables/gfd_unique_matches.csv`
- `outputs/tables/gfd_unmatched_dfsi_records.csv`
- `outputs/tables/gfd_unmatched_boundary_records.csv`
- `outputs/tables/gfd_ambiguous_matches.csv`

## Supplementary Table S1. DFSI Reproduction Summary

Include detailed numerical reproduction diagnostics:

- Complete and incomplete record counts.
- Reconstructed and published DFSI ranges.
- Pearson and Spearman correlations.
- Numerical differences.
- Rank differences.
- Top-group overlaps.

## Supplementary Table S2. Satellite Benchmark Results

Include all benchmark/outcome combinations:

- Published DFSI.
- Reconstructed DFSI.
- Equal-weight six-component index.
- Individual DFSI components.
- Equal-weight physical-hazard index.
- Learned physical-hazard index where applicable.
- Primary and secondary satellite outcomes.

Suggested source file:

- `outputs/tables/hazard_index_benchmark_results.csv`

## Supplementary Table S3. Satellite Top-10% Agreement

Include:

- Top-10% overlap counts.
- Jaccard similarities.
- Districts high under both DFSI and satellite burden.
- Districts high under DFSI only.
- Districts high under satellite burden only.

Suggested source files:

- `outputs/tables/hazard_index_top10_comparison.csv`
- `outputs/tables/hazard_index_multi_axis_classification.csv`

## Supplementary Table S4. Physical-Hazard Cross-Validation

Include:

- State and union-territory units in each fold.
- Selected weights by fold.
- Training and held-out correlations.
- Benchmark comparison by fold.
- State-block bootstrap results.
- State-demeaned results.

Suggested source files:

- `outputs/tables/hazard_index_cv_folds.csv`
- `outputs/tables/hazard_index_selected_weights.csv`
- `outputs/tables/hazard_index_cv_benchmark_summary.csv`
- `outputs/tables/hazard_index_state_block_bootstrap.csv`
- `outputs/tables/hazard_index_state_demeaned_results.csv`

## Supplementary Table S5. Fatality-Assignment Audit

Include:

- Fatality-assignment category counts by period.
- Raw reported fatalities.
- Assignable fatalities.
- Unassigned fatalities.
- Percent of raw reported fatalities.
- Percent of event records.

Suggested source files:

- `outputs/tables/predictive_ranking_fatality_assignment_reasons.csv`
- `outputs/tables/predictive_ranking_fatality_assignment_period_summary.csv`
- `outputs/reports/predictive_ranking_fatality_assignment_explanation.md`
- `outputs/reports/original_dfsi_fatality_handling_comparison.md`

## Supplementary Table S6. Temporal Model And Benchmark Results

Include full temporal evaluation:

- Spearman and Kendall correlations.
- Top-10% recall.
- Jaccard similarity.
- NDCG at top 10%.
- Average precision.
- Mean absolute error.
- Calibration by predicted-risk quintile.

Suggested source files:

- `outputs/tables/predictive_ranking_final_test_results.csv`
- `outputs/tables/predictive_ranking_top10_results.csv`
- `outputs/tables/predictive_ranking_calibration.csv`
- `outputs/tables/predictive_ranking_district_predictions.csv`

## Supplementary Table S7. Paired Bootstrap And Geographic Robustness

Include:

- Ordinary paired bootstrap.
- State-block bootstrap.
- State-specific results where sufficient variation exists.
- Leave-one-state-out sensitivity.
- Better-reporting subset check.
- Influence diagnostics.

Suggested source files:

- `outputs/tables/predictive_ranking_paired_bootstrap.csv`
- `outputs/tables/predictive_ranking_state_block_bootstrap.csv`
- `outputs/tables/predictive_ranking_state_results.csv`
- `outputs/tables/predictive_ranking_leave_one_state_out.csv`
- `outputs/tables/predictive_ranking_fatality_reporting_subset_metrics.csv`
- `outputs/tables/predictive_ranking_influence_diagnostics.csv`

## Supplementary Figures

Recommended:

1. Detailed DFSI reproduction scatter and rank-overlap figure.
2. GFD boundary matching and observation-quality summary.
3. Secondary satellite outcome benchmark comparison.
4. Physical-hazard selected weights by fold.
5. Reporting completeness over time.
6. Fatality-assignment category stacked bars by period.
7. Temporal calibration by predicted-risk quintile.
8. Leave-one-state-out temporal robustness.

## Analyses To Exclude From Main Manuscript

- Early arithmetic debugging notebooks.
- In-sample exploratory Monte Carlo weight optimisation against satellite outcomes.
- Detailed DFSI weight-sensitivity and cutoff-sensitivity tables unless required by reviewers.

These analyses can remain archived for transparency but should not carry the central claim of the paper.
