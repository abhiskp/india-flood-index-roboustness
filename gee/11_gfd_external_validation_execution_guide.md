# GFD External Validation Export Guide

Use `gee/11_gfd_external_validation_export_chunked.js` in the Google Earth
Engine Code Editor if the all-in-one export exceeds memory. The chunked script
is now the recommended route for this pilot.

## Steps

1. Open the Google Earth Engine Code Editor.
2. Create a new script and paste the full contents of `gee/11_gfd_external_validation_export_chunked.js`.
3. Run the script.
4. Review the printed diagnostics:
   - Indian ADM2 geometry count;
   - sample boundary properties;
   - raw boundary and image property names;
   - GFD total and India-filtered event counts;
   - event date range and event IDs;
   - GFD band names;
   - nominal projection scale of `flooded`, `duration`, `clear_perc` and `jrc_perm_water`;
   - selected analysis scale.
   If the country-code or country-name metadata filters return zero events but
   the spatial-intersection filter returns India-related events, continue with
   the spatial-intersection union and retain the exported event inventory as
   documentation. In the first Code Editor check, this produced 192
   India-related events from 2000-09-18 to 2018-09-01.
5. In the **Tasks** tab, start these Drive exports:
   - `gfd_india_adm2_boundaries`
   - `gfd_india_event_inventory`
   - `gfd_india_district_event_metrics_part_00`
   - `gfd_india_district_event_metrics_part_01`
   - `gfd_india_district_event_metrics_part_02`
   - `gfd_india_district_event_metrics_part_03`
   - `gfd_india_district_event_metrics_part_04`
   - `gfd_india_district_event_metrics_part_05`
   - `gfd_india_district_event_metrics_part_06`
   - `gfd_india_district_event_metrics_part_07`
   - `gfd_india_district_event_metrics_part_08`
   - `gfd_india_district_event_metrics_part_09`
   - `gfd_india_district_event_metrics_part_10`
   - `gfd_india_district_event_metrics_part_11`
   - `gfd_india_district_event_metrics_part_12`
   - `gfd_india_district_event_metrics_part_13`
   - `gfd_india_district_event_metrics_part_14`
   - `gfd_india_district_event_metrics_part_15`
   - `gfd_india_district_event_metrics_part_16`
   - `gfd_india_district_event_metrics_part_17`
   - `gfd_india_district_event_metrics_part_18`
   - `gfd_india_district_event_metrics_part_19`
6. Download the exported CSV files from the Google Drive folder:
   - `gfd_external_validation`
7. Place the CSV files here:
   - `data/processed/gfd_external_validation/gfd_india_adm2_boundaries.csv`
   - `data/processed/gfd_external_validation/gfd_india_event_inventory.csv`
   - `data/processed/gfd_external_validation/gfd_india_district_event_metrics_part_00.csv`
   - `data/processed/gfd_external_validation/gfd_india_district_event_metrics_part_01.csv`
   - and so on through `part_19.csv`
8. Run:
   - `notebooks/11a_gfd_boundary_matching.ipynb`
   - `notebooks/11b_gfd_external_validation_pilot.ipynb`

## Notes

- The GFD period is 2000-2018, whereas the published DFSI reflects a longer historical period.
- GFD is an independent satellite-observed sample of mapped flood events, not a complete flood inventory.
- The pilot tests convergent validity between DFSI and physical inundation metrics; it is not a weight-optimisation exercise.
