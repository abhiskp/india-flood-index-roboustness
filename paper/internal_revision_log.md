# Internal Revision Log

Created by `notebooks/10_internal_review_revisions.ipynb`.

## Scope Controls

- Preserved the frozen 709-record analytical baseline.
- Did not run new exploratory analyses.
- Did not resample Monte Carlo weights or load sampled-weight vectors.
- Did not alter analytical definitions, priority thresholds or missing-data handling.
- Verified that `data/raw` file hashes were unchanged.

## Reproduction Diagnostics Added

- Added mean signed error: -1.115266 DFSI score units.
- Added median signed error: -1.185715 DFSI score units.
- Added RMSE: 1.376872 DFSI score units.
- Added OLS slope for reconstructed DFSI as a function of published DFSI: 0.885496.
- Added OLS intercept: 0.441866 DFSI score units.
- Added these values to `paper/results_claims_audit_v2.csv` with claim IDs A01-A05.

## Manuscript Revisions

- Replaced the phrase "corrected additive log-space expression" with "algebraically equivalent additive log-space expression".
- Added the complete DFSI equation and definitions for flood-event count, mean duration, fatalities, injured people, corrected percent flooded area and population.
- Added [SOURCE DETAIL REQUIRED] placeholders for dataset DOI/version/access date, population year/source, flooded-area temporal definition and administrative-boundary vintage.
- Expanded district harmonisation and joining methods using existing join-audit outputs.
- Clarified one-to-one construction, unmatched records, multiply matched records, the 720 baseline rows, 709 complete records and 11 incomplete records.
- Replaced unqualified probability language with Monte Carlo inclusion frequency and simulation-based inclusion probability conditional on the specified Dirichlet weight distribution.
- Stated that concentration parameters 100, 30 and 10 are analyst-defined sensitivity scenarios and not empirically calibrated uncertainty distributions.
- Replaced policy-priority cutoff language with analytical priority cutoff language.
- Preferred historical flood severity wording and removed unsupported flood-risk phrasing.
- Moved reporting-completeness audit material into a concise Data Limitations subsection and supplementary framing.
- Removed internal claim IDs from `paper/manuscript_v2.md`.
- Corrected Results 3.2 to report the minimum leave-one-out Spearman correlation as 0.945272 rather than claiming all leave-one-out correlations exceed 0.95.

## Figure Revisions

- Created `outputs/figures/paper_figure_1_dfsi_reproduction_v2.png` with score and rank scatterplots, ranks 1-709, identity and fitted lines, signed bias and RMSE, and overlap/Jaccard summaries.
- Created `outputs/figures/paper_figure_2_component_sensitivity_v2.png` with median and 95th-percentile rank changes, top-10% retention/turnover and fatality-exponent sensitivity.
- Created `outputs/figures/paper_figure_3_monte_carlo_uncertainty_v2.png` with Monte Carlo top-10% inclusion frequency, point-category legend, 5th-95th percentile rank intervals and a reproducible district display rule.
- Created `outputs/figures/paper_figure_4_cutoff_sensitivity_v2.png` with robust share, mean overlap share and median turnover share across analytical priority cutoffs.
- Created `outputs/figures/supplementary_figure_4_component_arithmetic_share_v2.png` for arithmetic component contribution under released units.

## Table Revisions

- Created `paper/table_1_reproduction_summary_v2.csv`.
- Created `paper/table_2_leave_one_out_summary_v2.csv`.
- Created `paper/table_3_monte_carlo_scenario_summary_v2.csv`.
- Created `paper/supplementary_table_fatality_exponent_v2.csv`.
- Created `paper/supplementary_table_cutoff_sensitivity_v2.csv`.
- Created `paper/supplementary_table_component_arithmetic_v2.csv`.
- Avoided structurally empty mixed tables by separating reproduction, leave-one-out, Monte Carlo, fatality-exponent, cutoff and arithmetic-contribution outputs.

## Validation Results

- V2 manuscript numerical claims are traceable through `paper/results_claims_audit_v2.csv` and the existing source CSVs.
- No V2 manuscript statement says all leave-one-out Spearman values exceed 0.95.
- Monte Carlo inclusion results are explicitly conditional on the assumed Dirichlet weight distribution.
- No new simulation or exploratory analysis was run.
- `data/raw` hashes were unchanged.
