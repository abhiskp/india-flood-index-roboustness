# Do Complex Flood-Priority Rankings Add Value? Satellite and Temporal Validation of District Flood Prioritisation in India

**Draft scope:** Data, Methods and Results only. This version adds the final fatality-assignment audit and keeps the same professor-facing direction: satellite-derived inundation as the main validation comparison, temporal fatality prediction as a secondary test, and cautious evaluation of whether complex rankings add value over simple objective-specific indicators. It does not include an Introduction, Discussion, Abstract or Conclusion.

## 1. Data

### 1.1 Published DFSI and component data

The study uses the published India District Flood Severity Index (DFSI) and associated component datasets as the starting point for district-level comparison. The original DFSI paper is identified in the project literature matrix with DOI `10.1007/s11069-025-07493-9`. The analysis used Version 4 of the India Flood Inventory–Impacts dataset, archived on Zenodo under DOI 10.5281/zenodo.16994648 and accessed on 29 July 2026. The raw project folder contains the released DFSI table, district flooded-area data, flood-impact data and the India Flood Inventory.

The verified analytical baseline contained 720 one-to-one district comparison records. Of these, 709 records had complete DFSI component values and 11 were retained as incomplete without imputation. The six DFSI components available in the baseline were flood-event count, mean flood duration, fatalities, injured people, corrected percent flooded area and population.

The published DFSI was treated as a mixed flood-priority ranking because it combines physical flood history, population as a proxy for exposure and recorded human consequences. In log-space, the reconstructed expression used in the project was:

```text
DFSI =
  log10(1 + flood_event_count)
+ log10(1 + mean_flood_duration)
+ 2 * log10(1 + fatalities)
+ log10(1 + injured)
+ log10(1 + corrected_percent_flooded_area)
+ log10(population)
```

The reconstructed DFSI was used only for reproducibility and comparison. It was not used as a leakage-free temporal predictor, because it is derived from full-period component information.

### 1.2 Satellite-derived inundation data

Physical flood burden was evaluated using the Global Flood Database image collection `GLOBAL_FLOOD_DB/MODIS_EVENTS/V1`, which maps large flood events from 2000-2018. Administrative boundaries were taken from `WM/geoLab/geoBoundaries/600/ADM2`, filtered to India. These are versioned Earth Engine sources; the GFD paper DOI recorded in the literature matrix is `10.1038/s41586-021-03695-w`.

The Earth Engine export identified 192 India-related GFD events. Of these, 148 events had detected non-permanent floodwater in Indian district-event rows. Permanent water was removed before calculating district flood metrics. Event floodwater was defined as pixels where `flooded == 1`, excluding pixels where `jrc_perm_water == 1`.

The primary satellite-derived inundation outcome was cumulative inundation area-days per square kilometre:

```text
cumulative_inundation_area_days_per_km2 =
  sum over events and flooded non-permanent-water pixels
    (flooded pixel area in km2 * inundation duration in days)
  / district area in km2
```

This outcome measures repeated mapped inundation over 2000-2018. It is area-normalised, combines mapped extent and duration and avoids treating larger districts as more severely flooded simply because they have more area. It is an independent satellite-derived comparison for physical inundation, not a complete flood inventory and not a completely independent time period relative to the historical DFSI components.

The downloaded boundary file contained 735 Indian administrative geometries. The validation sample included 657 unique accepted DFSI-boundary matches, corresponding to 92.7% of the 709 complete DFSI districts. Of these matched districts, 639 had non-zero satellite-observed floodwater.

### 1.3 Event-level flood inventory for temporal validation

The temporal validation used the event-level India Flood Inventory. The event schema included event identifier, start and end dates, state, district, duration, fatalities, injuries, event source and administrative identifiers where available. The India Flood Inventory paper DOI recorded in the literature matrix is `10.1007/s11069-021-04698-6`.

Three non-overlapping 19-year periods were used:

- 1967-1985;
- 1986-2004;
- 2005-2023.

The primary temporal test used district flood-history predictors from 1986-2004 to rank districts by recorded flood fatalities in 2005-2023. The earlier transition, 1967-1985 predictors to 1986-2004 outcomes, was used for development. Full-period DFSI, reconstructed full-period DFSI, full-period flooded area and full-period GFD summaries were excluded as temporal predictors.

Historical reporting volume changed substantially across the three windows. The inventory contained 762 recorded events in 1967-1985, 1,968 in 1986-2004 and 4,126 in 2005-2023. Fatality reporting completeness was 49.9%, 61.8% and 52.6% across the same periods. Injury reporting completeness was 14.2%, 17.8% and 14.5%. These changes mean the temporal exercise predicts recorded future fatalities, not unobserved mortality burden.

Fatality handling is especially important. Missing fatality values were not interpreted as confirmed zero deaths. For the primary district target, a reported fatality was assigned only when the event was district-specific or single-district and the district could be matched to the verified baseline. Positive fatalities in multi-district records were not divided among districts because the inventory does not provide a verified within-event allocation rule. Therefore, a zero-fatality district means zero primary assignable recorded district deaths, not confirmed absence of flood deaths.

A large share of event-level reported fatalities could not be assigned uniquely to individual districts under this conservative rule, principally because they occurred in positive-fatality records listing multiple districts. In 1986-2004, the inventory reported 29,011 raw event-level fatalities, while 3,202 were primary assignable district fatalities. The largest unassigned category was multi-district positive-fatality records, accounting for 22,876 fatalities, or 78.9% of raw reported fatalities; unmatched district records accounted for 1,902 fatalities, or 6.6%; and state-only or non-district locations accounted for 1,031 fatalities, or 3.6%. In 2005-2023, the inventory reported 24,745 raw event-level fatalities, while 3,654 were primary assignable district fatalities. Multi-district positive-fatality records accounted for 19,168 unassigned fatalities, or 77.5% of raw reported fatalities; unmatched district records accounted for 1,290 fatalities, or 5.2%; and state-only or non-district locations accounted for 633 fatalities, or 2.6%. These deaths were not assumed absent; they were excluded from the district target to avoid arbitrary allocation or duplication. This is a major limitation and means the secondary fatality analysis may partly reflect reporting intensity and event assignability.

## 2. Methods

### 2.1 Overall validation design

The study separated two decision targets. The first target was physical flood burden, measured using satellite-derived inundation. The second target was later recorded human consequence, measured as primary assignable district flood fatalities in a future non-overlapping period.

This separation is central. A district ranking that corresponds with satellite-derived inundation is not automatically a ranking of future recorded fatalities. A ranking that predicts recorded future fatalities is not automatically a physical-hazard ranking.

### 2.2 DFSI reproduction

The DFSI was reconstructed from the released component datasets to establish a verified comparison baseline. Incomplete records were preserved without imputation. Ranks were assigned in descending order, where rank 1 represents the highest score. The reproduction step was used only to confirm that the released components strongly reproduce the published ranking; it is not the main contribution of the paper.

### 2.3 Satellite comparison

The six DFSI variables were separated into physical hazard, population as a proxy for exposure and recorded human consequences. The main physical-hazard index was an equal-weight index:

```text
H_equal = mean[
  log10(1 + flood_event_count),
  log10(1 + mean_flood_duration),
  log10(1 + corrected_percent_flooded_area)
]
```

This equal-weight physical-hazard index is the main satellite result because it is transparent and was not fitted to the satellite outcome. A learned physical-hazard index was evaluated only as a secondary check.

The satellite benchmark comparison evaluated published DFSI, reconstructed DFSI, an equal-weight six-component log index, individual DFSI component terms and the equal-weight physical-hazard index against cumulative inundation area-days per square kilometre. Spearman rank correlation was the main metric. Kendall correlation, 2,000-sample bootstrap confidence intervals, top-10% overlap and Jaccard similarity were also calculated. The top 10% satellite group contained 66 districts.

At least one secondary valid satellite outcome was retained for supplementary reporting: cumulative flooded-area-event fraction. This outcome measures cumulative event-level flooded area normalised by district area. It does not use the invalid unique-pixel `ever_flooded_area` field.

### 2.4 State-blocked physical-hazard validation

A secondary learned physical-hazard index used nonnegative weights on the transformed event, duration and flooded-area terms:

```text
H_w = w_E x_E + w_D x_D + w_A x_A
```

where all weights were nonnegative and summed to 1. Weights were selected inside five grouped cross-validation folds using state and union-territory units as groups. No state or union-territory unit appeared in both training and test data within a fold. Candidate weights were selected on training units and evaluated only on held-out units. Where candidate weights were nearly tied, the tie rule selected the most even vector within 0.001 Spearman correlation of the best training candidate.

This learned index is reported as secondary because its improvement over the equal-weight physical-hazard index was modest and geographically variable.

### 2.5 Temporal prediction of recorded future fatalities

The final temporal test used 1986-2004 predictors to rank 720 districts by primary assignable recorded flood fatalities in 2005-2023. The development transition used 1967-1985 predictors and 1986-2004 outcomes. No final-period outcome information was used to select transformations or model settings.

The final predictors used by the primary model were:

- `log1p(event_count)`;
- `log1p(mean_flood_duration)`;
- `log1p(total_flood_duration)`;
- `log1p(fatality_count)`;
- `log1p(injury_count)`;
- `log1p(fatal_event_count)`;
- `log1p(distinct_flood_years)`;
- `1 / (1 + years_since_recent_flood)`.

The primary model was a regularised Poisson count model with an L2 penalty on coefficients and regularisation setting `alpha = 1.0`. This setting was fixed before final evaluation and no large hyperparameter search was conducted. Predictors were standardised using the development transition only and then applied to the final test.

The secondary log-linear score was:

```text
0.35 * log1p(past_fatalities)
+ 0.20 * log1p(event_count)
+ 0.20 * log1p(total_flood_duration)
+ 0.15 * log1p(past_injuries)
+ 0.10 * log1p(distinct_flood_years)
```

Because this score was secondary and not the primary prespecified model, it is reported as a benchmark and should be placed in the supplement if space is limited.

### 2.6 Temporal benchmark rankings and metrics

The primary model was compared with simple predictor-period rankings: past fatalities, past fatal-event count, past injury count, past flood-event count, past mean duration, past total duration, an equal-weight historical hazard score, a historical persistence score, population alone as a secondary sensitivity analysis and hazard plus population as a secondary sensitivity analysis.

Top-10% groups used fixed counts. In the final temporal test, the top decile contained 72 districts. Ties were broken deterministically by state and district name so that group sizes were reproducible. NDCG at the top 10% used linear fatality-count gains with logarithmic rank discount:

```text
DCG@k = sum_i fatality_count_i / log2(rank_i + 1)
NDCG@k = DCG@k / ideal_DCG@k
```

Paired bootstrap comparisons used 2,000 ordinary district resamples. State-block bootstrap comparisons used 2,000 resamples of entire state and union-territory units. These comparisons tested whether the primary model improved over simple baselines under district-level and geographic uncertainty.

## 3. Results

### 3.1 DFSI reproduction established the comparison baseline

The released component datasets strongly reproduced the published DFSI ranking but did not reproduce it exactly. Among 709 complete records, reconstructed DFSI had Spearman correlation 0.9588 and Pearson correlation 0.9587 with published DFSI. Detailed rank differences and top-group overlaps are treated as supplementary reproduction material.

### 3.2 Equal-weight physical-hazard index better matched satellite-derived inundation

The primary satellite outcome was cumulative inundation area-days per square kilometre. The comparison used 657 uniquely matched districts.

Published DFSI had Spearman correlation 0.3575 with the primary satellite outcome, with bootstrap confidence interval 0.2774 to 0.4300. Reconstructed DFSI had Spearman correlation 0.3721, with interval 0.2964 to 0.4441. The equal-weight physical-hazard index had a higher Spearman correlation of 0.4529, with interval 0.3840 to 0.5200.

Individual component comparisons showed that flooded area alone had Spearman correlation 0.3745, population alone 0.3944, duration alone 0.3841 and flood-event frequency alone 0.2987. The equal-weight six-component log index had Spearman correlation 0.3878.

Top-10% overlap with the satellite-derived top group also differed across measures. Published DFSI and reconstructed DFSI each overlapped with 25 of the satellite top 66 districts, with Jaccard similarity 0.2336. The equal-weight physical-hazard index overlapped with 43 of 66 districts, with Jaccard similarity 0.4831. Flooded area alone overlapped with 39 of 66 districts, with Jaccard similarity 0.4194.

Paired bootstrap comparisons supported the difference between the equal-weight physical-hazard index and mixed DFSI. The observed Spearman difference between the equal-weight physical-hazard index and published DFSI was 0.0954, with interval 0.0436 to 0.1505. The difference relative to reconstructed DFSI was 0.0808, with interval 0.0330 to 0.1304. The difference relative to flooded area alone was 0.0784, with interval 0.0116 to 0.1474.

The same direction appeared for the secondary valid satellite outcome, cumulative flooded-area-event fraction. For that outcome, the equal-weight physical-hazard index had Spearman correlation 0.4899, compared with 0.3611 for published DFSI, 0.3793 for reconstructed DFSI and 0.4440 for flooded area alone. These secondary results should be reported in a supplementary table.

These results indicate that a transparent physical-hazard-only index corresponded more strongly with satellite-derived physical inundation than the mixed DFSI. This does not show that DFSI is invalid. It shows that DFSI and satellite-derived inundation measure different constructs.

### 3.3 State-blocked validation showed positive but geographically variable associations

The learned physical-hazard index was evaluated using five grouped folds over 35 state and union-territory units. The selected weights were broadly stable: the median event weight was 0.150, the median duration weight was 0.450 and the median flooded-area weight was 0.375. Across folds, event weights ranged from 0.075 to 0.175, duration weights from 0.425 to 0.500 and flooded-area weights from 0.350 to 0.500.

The learned physical-hazard index had overall out-of-fold Spearman correlation 0.4874 and Kendall correlation 0.3433 with the primary satellite outcome. The equal-weight physical-hazard index had out-of-fold Spearman correlation 0.4529 and Kendall correlation 0.3239. Flooded area alone had out-of-fold Spearman correlation 0.3745, published DFSI 0.3575 and reconstructed DFSI 0.3721.

Fold-level results varied substantially. The learned physical-hazard index had a median held-out Spearman correlation of 0.4329 across folds, with a range from 0.0992 to 0.6462. The equal-weight physical-hazard index had a median held-out Spearman correlation of 0.4084, with a range from 0.2423 to 0.6069. Published DFSI had a median held-out Spearman correlation of 0.3947, with a range from 0.0620 to 0.5137.

State-block bootstrap results showed positive but geographically uncertain associations. The learned physical-hazard out-of-fold score had observed national Spearman correlation 0.4874 and state-block interval 0.1960 to 0.6608. The equal-weight physical-hazard index had observed national Spearman correlation 0.4529 and interval 0.1783 to 0.6384. Published DFSI had observed national Spearman correlation 0.3575 and interval 0.1148 to 0.5446.

After demeaning within state or union-territory unit, correlations were much smaller. The learned physical-hazard score had state-demeaned Spearman correlation 0.0876, the equal-weight physical-hazard index 0.1193 and published DFSI 0.0575. This suggests that the national satellite association is partly shaped by broad between-unit differences, and district-level within-unit ranking should be interpreted cautiously.

### 3.4 Fatality assignment limits the temporal target

The final temporal test used 720 districts. The outcome period, 2005-2023, contained 3,654 primary assignable recorded district fatalities. A total of 332 districts had positive primary assignable recorded future fatalities, while 388 districts, or 53.9%, had zero primary assignable recorded future fatalities. Among the 388 zero-fatality districts, 236 had matched flood-event rows and 152 had no matched event rows in 2005-2023.

These zeros should not be interpreted as confirmed absence of deaths. They mean no primary assignable recorded deaths under the conservative district-specific assignment rule. A large share of raw reported fatalities was not assignable to a single district without risking arbitrary allocation or double counting. In 2005-2023, the dominant reason was multi-district positive-fatality records, which accounted for 19,168 unassigned fatalities, or 77.5% of all raw reported fatalities. Unmatched district records accounted for 1,290 fatalities, or 5.2%, and state-only or non-district locations accounted for 633 fatalities, or 2.6%.

This assignment problem is the main limitation of the temporal analysis. The fatality analysis is secondary to the satellite-derived inundation comparison, and it should be interpreted as prediction of primary assignable recorded district fatalities rather than precise district-level mortality burden. The model may partly predict reporting intensity or event assignability, not only flood mortality.

### 3.5 The fitted fatality model showed signal but was not robustly better than simple baselines

The primary regularised Poisson model had Spearman correlation 0.4614 and Kendall correlation 0.3607 with recorded future fatalities in the final 2005-2023 test. It identified 31 of the 72 actual future-fatality top-decile districts, giving top-10% recall 0.4306 and Jaccard similarity 0.2743. Its NDCG at the top 10% was 0.6884, average precision was 0.4032 and mean absolute error was 6.2942 fatalities.

The simple past flood-event count benchmark had Spearman correlation 0.4930 and Kendall correlation 0.3921. It identified 28 of the 72 future top-decile districts, giving top-10% recall 0.3889 and Jaccard similarity 0.2414. Past fatalities had Spearman correlation 0.3595 and top-10% recall 0.3750. The historical persistence score had Spearman correlation 0.3683 and top-10% recall 0.4167. The equal-weight historical hazard score had Spearman correlation 0.4626 but lower top-10% recall, 0.2639.

The secondary log-linear score had the highest national Spearman correlation among evaluated scores, 0.4968, with top-10% recall 0.4028. Because it was a secondary benchmark rather than the prespecified primary model, it should not be used to claim a fitted-model advantage in the main text.

Ordinary paired bootstrap comparisons showed that the primary Poisson model outperformed past fatalities on Spearman correlation by 0.1019, with interval 0.0410 to 0.1629. However, it did not outperform past flood-event count. The observed Spearman difference relative to past flood-event count was -0.0315, with interval -0.0637 to 0.0008. The difference relative to the equal-weight historical hazard score was -0.0012, with interval -0.0374 to 0.0343.

State-block bootstrap weakened claims of a model advantage further. The primary model's Spearman difference relative to past fatalities was 0.1019, but the state-block interval ranged from -0.0216 to 0.2317. Relative to past flood-event count, the Spearman difference was -0.0315, with interval -0.0951 to 0.0301. Relative to the equal-weight historical hazard score, the difference was -0.0012, with interval -0.0809 to 0.0865. For top-decile recall, all three state-block intervals crossed zero for comparisons with past fatalities, past flood-event count and the equal-weight historical hazard score.

A focused better-reporting subset check did not overturn this conclusion. Among 452 districts with at least one final-period matched event and at least 50% fatality-field reporting in final-period event rows, the primary model had Spearman correlation 0.2461 and top-10% recall 0.3913. Past flood-event count had Spearman correlation 0.3197 and top-10% recall 0.4130. This subset check is diagnostic rather than a new modelling branch, but it supports the same cautious conclusion.

The temporal result is therefore narrow: historical flood records contain predictive signal for recorded future fatalities, but the fitted model did not robustly outperform simple historical flood-event frequency.

### 3.6 Influence checks did not remove the main caution

Several diagnostics tested whether the temporal result was dominated by narrow subsets. Among 558 districts with zero historical fatalities in the predictor period, the primary model still had Spearman correlation 0.3730, but top-10% recall fell to 0.2500. After excluding states and union-territory units with the weakest reporting completeness, the primary model had Spearman correlation 0.4458 and top-10% recall 0.4737.

The final-period fatality outcome was not entirely driven by one or two individual events. The largest single district-event fatality count was 273. The top two events accounted for 11.4% of final-period fatalities, and the top ten events accounted for 22.5%.

These checks indicate that the temporal ranking signal is not purely an artefact of one disaster or one reporting subset. However, they do not remove the main caution that missing fatality reporting and non-assignable multi-district deaths limit interpretation.

## Recommended Main-Paper Figures and Tables

### Main Figures

1. Study design showing the satellite-derived inundation comparison and the non-overlapping temporal validation periods.
2. Satellite benchmark comparison showing DFSI, component benchmarks and the equal-weight physical-hazard index against cumulative inundation area-days per square kilometre.
3. Future-fatality model and simple-baseline comparison showing final-test Spearman correlation, top-10% recall and uncertainty.

### Main Tables

1. Data sources, periods and samples.
2. Main satellite and temporal validation results.

### Supplementary Material

- Detailed DFSI reproduction and rank-overlap table.
- Physical-hazard cross-validation weights and fold-level results.
- Valid secondary satellite outcome table, including cumulative flooded-area-event fraction.
- Reporting completeness and fatality-assignment audit.
- Full ordinary and state-block bootstrap tables.
- Influence diagnostics and district-level prediction table.
