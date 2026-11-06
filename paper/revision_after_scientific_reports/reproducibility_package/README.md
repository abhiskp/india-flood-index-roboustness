# Reproducibility Package

This directory indexes the exact data provenance, linkage evidence, source code and derived tables used in the revised reliability-focused manuscript. Raw files are not duplicated here; their repository paths and SHA-256 hashes are recorded in `raw_data_provenance_and_hashes.csv`.

## Contents

- `raw_data_provenance_and_hashes.csv`: file sizes, hashes, source identifiers and raw/derived status.
- `environment_versions.csv`: verified software and execution settings.
- `analysis_reproduction_order.csv`: ordered workflow, inputs and outputs.
- `district_crosswalk.csv`: accepted DFSI–GFD boundary links.
- `district_exclusion_reasons.csv`: all complete DFSI districts excluded from satellite validation.
- `final_analytical_district_tables/`: district-level datasets used by the three validation branches.
- `audit_outputs/`: machine-readable editor-response reliability results.
- `scripts/`: source scripts and Earth Engine export code.
- `notebooks/`: notebooks defining linkage, satellite validation, temporal panels, retrospective validation and the reliability audit.

## Exact reproduction order

1. Verify raw-file hashes against `raw_data_provenance_and_hashes.csv`.
2. Run notebooks 01–03 to audit source files and construct `dfsi_verified_baseline.csv`.
3. Run the Earth Engine export in `scripts/11_gfd_external_validation_export.js`; place exported parts under `data/processed/gfd_external_validation/`.
4. Run notebook 11a to create the reviewed boundary linkage; do not automatically accept fuzzy candidates. Run notebook 11b to consolidate the downloaded GFD export parts and create the satellite validation sample.
5. Run notebooks 12a and 12b for satellite benchmarks and grouped physical-hazard validation.
6. Run notebooks 13a–13c for temporal feasibility, event-to-district linkage, the district-period panel and the frozen fatality benchmark.
7. Run notebook 14 for the retrospective physical backtest.
8. Run notebook 15 or `scripts/editor_response_audit.py` for the reliability audit.
9. Compare generated files with the supplied machine-readable tables. Randomised procedures use seed 42.

## Important non-reproducible metadata

The original GFD export date was not recorded, the population reference year is not recoverable from released project files and the original DFSI event-to-district fatality allocation procedure cannot be verified. These uncertainties are reported rather than inferred.
