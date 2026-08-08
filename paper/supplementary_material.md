# Supplementary Material

## Supplementary Text S1. DFSI Reproduction And District Matching

The published District Flood Severity Index (DFSI) and released components were reconstructed to establish the district-level comparison baseline. Incomplete component records were retained without imputation. The accepted one-to-one baseline contained 720 district records, of which 709 had complete component values. Detailed reproduction metrics and top-group overlaps are provided in Supplementary Tables S1 and S1b.

District matching for the satellite comparison used accepted unique matches between the verified DFSI baseline and geoBoundaries ADM2 geometries. Unmatched and ambiguous records were retained in audit outputs rather than automatically assigned. The matching audit is provided in Supplementary Tables S9 and S9b.

## Supplementary Text S2. Satellite Validation Details

The primary satellite-derived inundation outcome was cumulative inundation area-days per square kilometre. The main text reports the primary benchmark comparison. Supplementary Table S2 reports all satellite benchmark correlations for the primary outcome and valid secondary outcomes, including cumulative flooded-area-event fraction. Supplementary Table S3 reports top-decile agreement and Jaccard similarity. Supplementary Figure S2 provides the extended satellite benchmark comparison.

## Supplementary Text S3. Learned Physical-Hazard Index

The learned physical-hazard index was a secondary validation check rather than the main satellite result. Candidate nonnegative event, duration and flooded-area weights were selected inside state-blocked folds and evaluated on held-out state and union-territory units. Fold-level performance, selected weights, state-block bootstrap results and state-demeaned results are reported in Supplementary Tables S4-S4d and Supplementary Figure S3.

## Supplementary Text S4. Temporal Fatality Target And Reporting Completeness

The temporal analysis used primary assignable recorded district fatalities. Multi-district positive-fatality event records were not allocated across districts because the released event inventory did not provide a verified within-event allocation rule. These reported deaths were excluded from the district target to avoid arbitrary splitting or duplication, not treated as absent. Fatality-assignment reasons and period summaries are reported in Supplementary Tables S5 and S5b. Reporting-completeness summaries are reported in Supplementary Table S8 and Supplementary Figure S4.

## Supplementary Text S5. Temporal Benchmarks And Uncertainty

The main text reports the primary regularised Poisson model, past flood-event count and selected simple baselines. Supplementary Tables S6-S6c report full final-test benchmark metrics, top-decile results and calibration by predicted-risk quintile. Supplementary Table S6d reports the secondary prespecified log-linear benchmark:

\[
0.35\log(1+\mathrm{past\ fatalities}) +
0.20\log(1+\mathrm{event\ count}) +
0.20\log(1+\mathrm{total\ duration}) +
0.15\log(1+\mathrm{past\ injuries}) +
0.10\log(1+\mathrm{distinct\ flood\ years}).
\]

This manually weighted score is reported as a secondary benchmark only and is not used to claim model superiority. Ordinary paired bootstrap and state-block bootstrap comparisons are reported in Supplementary Tables S7 and S7b. Better-reporting subset and influence diagnostics are reported in Supplementary Tables S7c and S7d.

## Supplementary Tables

- Supplementary Table S1: `paper/supplementary_tables/supplementary_table_s1_dfsi_reproduction_metrics.csv`
- Supplementary Table S1b: `paper/supplementary_tables/supplementary_table_s1b_dfsi_top_group_overlap.csv`
- Supplementary Table S2: `paper/supplementary_tables/supplementary_table_s2_satellite_all_benchmarks.csv`
- Supplementary Table S3: `paper/supplementary_tables/supplementary_table_s3_satellite_top10_agreement.csv`
- Supplementary Table S4: `paper/supplementary_tables/supplementary_table_s4_hazard_cv_folds.csv`
- Supplementary Table S4b: `paper/supplementary_tables/supplementary_table_s4b_hazard_selected_weights.csv`
- Supplementary Table S4c: `paper/supplementary_tables/supplementary_table_s4c_hazard_state_block_bootstrap.csv`
- Supplementary Table S4d: `paper/supplementary_tables/supplementary_table_s4d_hazard_state_demeaned_results.csv`
- Supplementary Table S5: `paper/supplementary_tables/supplementary_table_s5_fatality_assignment_reasons.csv`
- Supplementary Table S5b: `paper/supplementary_tables/supplementary_table_s5b_fatality_assignment_period_summary.csv`
- Supplementary Table S6: `paper/supplementary_tables/supplementary_table_s6_temporal_full_benchmarks.csv`
- Supplementary Table S6b: `paper/supplementary_tables/supplementary_table_s6b_temporal_top10_results.csv`
- Supplementary Table S6c: `paper/supplementary_tables/supplementary_table_s6c_temporal_calibration.csv`
- Supplementary Table S6d: `paper/supplementary_tables/supplementary_table_s6d_secondary_log_linear_score.csv`
- Supplementary Table S7: `paper/supplementary_tables/supplementary_table_s7_ordinary_bootstrap.csv`
- Supplementary Table S7b: `paper/supplementary_tables/supplementary_table_s7b_state_block_bootstrap.csv`
- Supplementary Table S7c: `paper/supplementary_tables/supplementary_table_s7c_better_reporting_subset.csv`
- Supplementary Table S7d: `paper/supplementary_tables/supplementary_table_s7d_influence_diagnostics.csv`
- Supplementary Table S8: `paper/supplementary_tables/supplementary_table_s8_reporting_period_completeness.csv`
- Supplementary Table S9: `paper/supplementary_tables/supplementary_table_s9_district_matching_audit.csv`
- Supplementary Table S9b: `paper/supplementary_tables/supplementary_table_s9b_gfd_boundary_match_audit.csv`

## Supplementary Figures

- Supplementary Figure S1: detailed DFSI reproduction figure, `outputs/figures/paper_figure_1_dfsi_reproduction_v2.png`
- Supplementary Figure S2: extended satellite benchmark comparison, `outputs/figures/hazard_index_benchmark_correlations.png`
- Supplementary Figure S3: learned hazard-weight validation, `outputs/figures/hazard_index_cv_performance.png` and `outputs/figures/hazard_index_selected_weights.png`
- Supplementary Figure S4: temporal reporting and model diagnostics, `outputs/figures/predictive_ranking_reporting_completeness.png` and `outputs/figures/predictive_ranking_model_comparison.png`

## Reproducibility Notes

The main reproducibility details are stated in the manuscript. Items requiring final pre-submission confirmation are listed in `paper/final_submission_checklist.md`.
