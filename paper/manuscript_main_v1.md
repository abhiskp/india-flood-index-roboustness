# Do Complex Flood-Priority Rankings Add Value? Satellite and Temporal Validation of District Flood Prioritisation in India

**Draft scope:** Data, Methods and Results only. This draft uses frozen quantitative outputs and reports. It does not revise the old manuscript.

## 1. Data

### 1.1 District Flood Severity Index inputs

The analysis began from the released district-level District Flood Severity Index (DFSI) data and associated component datasets. The verified comparison baseline contained 720 one-to-one district records. Of these, 709 records had complete values for numerical DFSI reconstruction, while 11 records were retained as incomplete and were not imputed.

The DFSI components available in the verified baseline were flood-event count, mean flood duration, fatalities, injured people, corrected percent flooded area and population. These components mix three different constructs: physical flood hazard, exposure and recorded human consequences. For this reason, the present study treats DFSI as a published mixed flood-priority ranking and evaluates it against two separate validation targets: independently observed physical inundation and later recorded fatalities.

The reconstructed DFSI was used only as a reproducibility and comparison measure. It was not treated as a leakage-free temporal predictor, because it is derived from full-period component information.

### 1.2 Satellite-observed physical inundation

Physical flood burden was evaluated using Global Flood Database (GFD) satellite-observed flood metrics for 2000-2018. The GFD was treated as an independent sample of mapped inundation, not as a complete ground-truth inventory of all floods in India.

The GFD validation used unique accepted matches between DFSI districts and administrative boundary records. The downloaded boundary file contained 735 Indian administrative geometries. The final validation sample included 657 uniquely matched DFSI-boundary records, corresponding to 92.7% of the 709 complete DFSI districts. Of these matched districts, 639 had non-zero satellite-observed floodwater. The primary satellite outcome was cumulative inundation area-days per square kilometre. This area-normalised outcome was selected because it captures both mapped flood extent and inundation duration while reducing the tendency for larger districts to dominate raw-area measures.

The satellite comparison is a convergent-validity test for physical inundation. It is not a direct validation of future human impacts, and it does not imply that weak or moderate correspondence invalidates DFSI.

### 1.3 Event-level flood inventory for temporal validation

The temporal validation used the India Flood Inventory event-level file. The event schema included event identifier, start and end dates, state, district, duration, fatalities, injuries, event source and administrative identifiers where available.

Three non-overlapping 19-year periods were used:

- 1967-1985;
- 1986-2004;
- 2005-2023.

The primary temporal test used district flood-history predictors from 1986-2004 to rank districts by recorded flood fatalities in 2005-2023. The earlier transition, 1967-1985 to 1986-2004, was used as the development transition. No outcome-period information was used to construct predictors for the final test.

Historical reporting volume changed substantially across the three windows. The event inventory contained 762 recorded events in 1967-1985, 1,968 in 1986-2004 and 4,126 in 2005-2023. Fatality reporting completeness was 49.9%, 61.8% and 52.6% across the same periods. Injury reporting completeness remained low, ranging from 14.2% to 17.8%. These reporting differences are treated as a major limitation. Temporal results are therefore interpreted as prediction of recorded flood-fatality burden, not as direct measurement of true physical flood trends.

For district-level fatality outcomes, the analysis used only district-specific or single-district event records. Multi-district event death totals were not duplicated across all listed districts. This avoids artificial double counting but makes the district-level fatality burden conservative.

## 2. Methods

### 2.1 Overall validation design

The analysis separated two decision targets. The first target was physical flood burden, measured by satellite-observed inundation. The second target was future recorded human consequence, measured as district flood fatalities in a later period.

This separation is central to the study. A district ranking that corresponds with physical inundation is not necessarily a ranking of future fatality burden. Similarly, a ranking that predicts later recorded fatalities is not necessarily a physical-hazard ranking.

### 2.2 DFSI reproduction and baseline construction

The DFSI was reconstructed from the released component datasets to create a verified comparison baseline. The reconstruction used the published six components and preserved incomplete records without imputation. Ranks were assigned in descending order, where rank 1 represents the highest DFSI score.

The reproduction step was used to establish that the released component data approximately reproduced the published DFSI ranking. It was not used to force an exact numerical match.

### 2.3 Physical-hazard indices for satellite comparison

For the satellite comparison, the six DFSI variables were separated into:

- physical hazard: flood-event count, mean flood duration and corrected percent flooded area;
- exposure: population;
- recorded human consequences: fatalities and injuries.

The equal-weight physical-hazard index was defined as the mean of three transformed physical-hazard terms:

```text
H_equal = mean[
  log10(1 + flood_event_count),
  log10(1 + mean_flood_duration),
  log10(1 + corrected_percent_flooded_area)
]
```

The satellite benchmark comparison evaluated published DFSI, reconstructed DFSI, an equal-weight six-component log index, individual DFSI component terms and the equal-weight physical-hazard index against the primary satellite outcome.

Spearman rank correlation was the main association metric. Kendall correlation, bootstrap confidence intervals, top-10% overlap and Jaccard similarity were also calculated. The top-10% satellite comparison used 66 districts among the 657 matched records.

### 2.4 State-blocked physical-hazard cross-validation

A transparent learned physical-hazard index was also evaluated:

```text
H_w = w_E x_E + w_D x_D + w_A x_A
```

where `x_E`, `x_D` and `x_A` are the transformed flood-event, duration and flooded-area terms. The weights were constrained to be nonnegative and to sum to 1.

Weights were selected inside five grouped cross-validation folds using state as the grouping variable. No state appeared in both training and test data within a fold. Candidate weights were selected on the training states and then evaluated only on held-out states. The fold-specific selected weights were chosen with a tie rule that preferred the most even vector within 0.001 Spearman correlation of the best training candidate.

The learned hazard index was compared with the equal-weight physical-hazard index, flooded area alone, published DFSI and reconstructed DFSI.

### 2.5 Temporal prediction of future recorded fatalities

The final temporal test ranked 720 districts by predicted recorded flood fatalities in 2005-2023 using only 1986-2004 district flood-history predictors. The following full-period or overlapping predictors were excluded to avoid leakage: published full-period DFSI, reconstructed full-period DFSI, full-period flooded area and full-period GFD metrics.

For each district-period, the panel included event count, total flood duration, mean flood duration, maximum event duration, fatality count, injury count, fatal-event count, injury-event count, proportions of events with fatalities and injuries, number of distinct flood years, average annual event count, average annual fatalities, average annual injuries and recency.

The primary model was a regularised Poisson count model predicting future fatalities. Model settings and transformations were selected using only the development transition, 1967-1985 predictors to 1986-2004 outcomes, before evaluation on the final transition. A restrained log-linear risk score was evaluated as a secondary benchmark, not as the primary model.

### 2.6 Temporal benchmark rankings and metrics

The primary model was compared with simple rankings constructed only from the predictor period:

- past fatalities;
- past fatal-event count;
- past injury count;
- past flood-event count;
- past mean duration;
- past total duration;
- equal-weight historical hazard score;
- historical persistence score;
- population alone as a secondary sensitivity analysis;
- hazard plus population as a secondary sensitivity analysis.

The final 2005-2023 ranking was evaluated using Spearman correlation, Kendall correlation, top-10% overlap, top-10% recall, Jaccard similarity, NDCG at the top 10%, average precision for identifying the future top 10% and mean absolute error for fatality counts. The final top decile contained 72 districts.

Paired bootstrap comparisons used 2,000 ordinary district resamples. State-block bootstrap comparisons used 2,000 resamples of entire states. These paired comparisons tested whether the primary model improved over simple baselines under district-level and state-level uncertainty.

## 3. Results

### 3.1 DFSI was strongly, but not exactly, reproduced

The verified DFSI baseline contained 720 one-to-one comparison records, including 709 complete records and 11 incomplete records preserved without imputation. Among complete records, reconstructed DFSI had Spearman correlation 0.9588 and Pearson correlation 0.9587 with published DFSI. The median absolute numerical difference was 1.2068, the median absolute rank difference was 18 and the maximum absolute rank difference was 345.

Top-group agreement was high but not exact. The published and reconstructed top 10% groups overlapped in 59 of 71 districts. The top-25, top-50 and top-100 overlaps were 19 of 25, 41 of 50 and 89 of 100 districts, respectively.

These results support strong ranking reproduction, but not exact numerical reproduction.

### 3.2 Physical-hazard measures corresponded more strongly with satellite-observed inundation than mixed DFSI

The primary satellite outcome was cumulative inundation area-days per square kilometre. The comparison used 657 uniquely matched districts.

Published DFSI had Spearman correlation 0.3575 with the primary satellite outcome, with bootstrap confidence interval 0.2774 to 0.4300. Reconstructed DFSI had Spearman correlation 0.3721, with interval 0.2964 to 0.4441. The equal-weight physical-hazard index had a higher Spearman correlation of 0.4529, with interval 0.3840 to 0.5200.

Individual component comparisons showed that flooded area alone had Spearman correlation 0.3745, population alone 0.3944, duration alone 0.3841 and flood-event frequency alone 0.2987. The equal-weight six-component log index had Spearman correlation 0.3878.

Top-10% overlap with the satellite top group also differed across measures. Published DFSI and reconstructed DFSI each overlapped with 25 of the satellite top 66 districts, with Jaccard similarity 0.2336. The equal-weight physical-hazard index overlapped with 43 of 66 districts, with Jaccard similarity 0.4831. Flooded area alone overlapped with 39 of 66 districts, with Jaccard similarity 0.4194.

Paired bootstrap comparisons supported the difference between the equal-weight physical-hazard index and mixed DFSI. The observed Spearman difference between the equal-weight physical-hazard index and published DFSI was 0.0954, with bootstrap interval 0.0436 to 0.1505. The difference relative to reconstructed DFSI was 0.0808, with interval 0.0330 to 0.1304. The difference relative to flooded area alone was 0.0784, with interval 0.0116 to 0.1474.

These results indicate that a physical-hazard-only index corresponded more strongly with independently satellite-observed physical inundation than the mixed DFSI. This does not imply that DFSI is wrong; rather, it shows that DFSI and satellite inundation measure different constructs.

### 3.3 State-blocked validation supported the physical-hazard result, with geographic caveats

The learned physical-hazard index was evaluated using five state-grouped folds. The selected weights were stable in broad terms: the median event weight was 0.150, the median duration weight was 0.450 and the median flooded-area weight was 0.375. Across folds, event weights ranged from 0.075 to 0.175, duration weights from 0.425 to 0.500 and flooded-area weights from 0.350 to 0.500.

The learned physical-hazard index had overall out-of-fold Spearman correlation 0.4874 and Kendall correlation 0.3433 with the primary satellite outcome. The equal-weight physical-hazard index had out-of-fold Spearman correlation 0.4529 and Kendall correlation 0.3239. Flooded area alone had out-of-fold Spearman correlation 0.3745, published DFSI 0.3575 and reconstructed DFSI 0.3721.

Fold-level results varied. The learned physical-hazard index had a median held-out Spearman correlation of 0.4329 across folds, with a range from 0.0992 to 0.6462. The equal-weight physical-hazard index had a median held-out Spearman correlation of 0.4084, with a range from 0.2423 to 0.6069. Published DFSI had a median held-out Spearman correlation of 0.3947, with a range from 0.0620 to 0.5137.

State-block bootstrap results also showed positive but geographically uncertain associations. The learned physical-hazard out-of-fold score had observed national Spearman correlation 0.4874 and state-block bootstrap interval 0.1960 to 0.6608. The equal-weight physical-hazard index had observed national Spearman correlation 0.4529 and interval 0.1783 to 0.6384. Published DFSI had observed national Spearman correlation 0.3575 and interval 0.1148 to 0.5446.

After demeaning within state, correlations were much smaller. The learned physical-hazard score had state-demeaned Spearman correlation 0.0876, the equal-weight physical-hazard index 0.1193 and published DFSI 0.0575. This suggests that the national satellite association is partly shaped by broad between-state differences, and district-level within-state ranking should be interpreted cautiously.

### 3.4 Temporal prediction was feasible, but reporting drift was substantial

The temporal inventory supported a leakage-free prediction exercise, but only with important reporting caveats. Recorded event volume increased from 762 events in 1967-1985 to 1,968 in 1986-2004 and 4,126 in 2005-2023. Matched event-district rows increased from 4,432 to 6,710 and then 9,373. Fatality reporting completeness was 49.9%, 61.8% and 52.6% across the three periods, while injury reporting completeness was 14.2%, 17.8% and 14.5%.

The final temporal test used 720 districts. The outcome period, 2005-2023, contained 3,654 primary assignable district fatalities. A total of 332 districts had positive recorded future fatalities, while 388 districts, or 53.9%, had zero recorded future fatalities. The largest district-level future fatality count was 338. The final top decile contained 72 districts.

Because reporting volume and completeness changed over time, the temporal analysis is interpreted as prediction of recorded fatalities, not as a direct estimate of changes in true fatality risk.

### 3.5 The fitted fatality model showed predictive signal but was not robustly superior to simple baselines

The primary regularised Poisson model had Spearman correlation 0.4614 and Kendall correlation 0.3607 with recorded future fatalities in the final 2005-2023 test. It identified 31 of the 72 actual future-fatality top-decile districts, giving top-10% recall 0.4306 and Jaccard similarity 0.2743. Its NDCG at the top 10% was 0.6884, average precision was 0.4032 and mean absolute error was 6.2942 fatalities.

The simple past flood-event count benchmark had Spearman correlation 0.4930 and Kendall correlation 0.3921. It identified 28 of the 72 future top-decile districts, giving top-10% recall 0.3889 and Jaccard similarity 0.2414. Past fatalities had Spearman correlation 0.3595 and top-10% recall 0.3750. The historical persistence score had Spearman correlation 0.3683 and top-10% recall 0.4167. The equal-weight historical hazard score had Spearman correlation 0.4626 but lower top-10% recall, 0.2639.

A secondary restrained log-linear score had the highest national Spearman correlation among the evaluated scores, 0.4968, with top-10% recall 0.4028. Because it was a secondary benchmark and not the prespecified primary model, it is not used to claim model superiority.

Ordinary paired bootstrap comparisons showed that the primary Poisson model outperformed past fatalities on Spearman correlation by 0.1019, with interval 0.0410 to 0.1629. However, it did not outperform past flood-event count. The observed Spearman difference relative to past flood-event count was -0.0315, with interval -0.0637 to 0.0008. The difference relative to the equal-weight historical hazard score was -0.0012, with interval -0.0374 to 0.0343.

For top-decile recall, the primary model exceeded past flood-event count by 0.0417, but the ordinary bootstrap interval ranged from -0.1250 to 0.1250. The primary model exceeded the equal-weight historical hazard score by 0.1667, with interval 0.0274 to 0.2639. It exceeded past fatalities by 0.0556, but the interval ranged from -0.0278 to 0.1389.

State-block bootstrap results weakened the model-superiority claim further. The primary model's Spearman difference relative to past fatalities was 0.1019, but the state-block interval ranged from -0.0216 to 0.2317. Relative to past flood-event count, the Spearman difference was -0.0315, with interval -0.0951 to 0.0301. Relative to the equal-weight historical hazard score, the difference was -0.0012, with interval -0.0809 to 0.0865. For top-decile recall, all three state-block intervals crossed zero for the comparisons with past fatalities, past flood-event count and the equal-weight historical hazard score.

These results support a cautious conclusion: historical flood records contain predictive signal for later recorded fatalities, but the fitted model did not robustly outperform simple historical baselines, especially past flood-event frequency.

### 3.6 Influence and robustness checks did not remove the main caution

Several diagnostics tested whether the temporal result was dominated by narrow subsets. Among districts with zero historical fatalities in the predictor period, the primary model still had Spearman correlation 0.3730, but top-10% recall fell to 0.2500. After excluding states with the weakest reporting completeness, the primary model had Spearman correlation 0.4458 and top-10% recall 0.4737.

The final-period fatality outcome was not entirely driven by one or two individual events. The largest single district-event fatality count was 273. The top two events accounted for 11.4% of final-period fatalities, and the top ten events accounted for 22.5%.

These checks indicate that the temporal ranking signal is not purely an artefact of one disaster or one reporting subset. However, they do not overturn the main finding that simple past flood-event frequency was difficult to beat.

## Recommended Main-Paper Figures and Tables

### Recommended Figures

1. **Satellite validation scatter and benchmark panel:** published DFSI, reconstructed DFSI and physical-hazard index versus cumulative inundation area-days per square kilometre.
2. **Physical-hazard cross-validation figure:** held-out Spearman correlations by fold and selected physical-hazard weights.
3. **Temporal prediction model comparison:** final-test Spearman, top-10% recall and NDCG for the primary model and simple baselines.
4. **Temporal calibration or actual-versus-predicted figure:** observed 2005-2023 fatalities by predicted-risk quintile or predicted versus observed fatalities.
5. **Reporting completeness figure:** recorded event volume and fatality/injury completeness across 1967-2023.

### Recommended Tables

1. **Data and validation samples:** DFSI records, GFD matched records and temporal prediction periods.
2. **Satellite validation benchmark table:** correlations, confidence intervals and top-10% overlaps for DFSI, physical-hazard indices and component benchmarks.
3. **State-blocked physical-hazard validation table:** fold-level and state-block bootstrap performance.
4. **Final temporal prediction table:** primary model and benchmark performance in the 2005-2023 test.
5. **Paired uncertainty comparison table:** ordinary and state-block bootstrap differences between the primary model and simple baselines.
