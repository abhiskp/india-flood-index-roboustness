# Do Complex Flood-Priority Rankings Add Value? Satellite and Temporal Validation of District Flood Prioritisation in India

## Abstract

District flood-priority rankings are useful for summarising complex evidence for planning, but a single composite score may combine physical flooding, population exposure and recorded human consequences that are not the same decision target. This study evaluates whether complex flood-priority rankings and fitted models add value beyond simple objective-specific indicators in India. We use the published District Flood Severity Index (DFSI) as a national district-scale case study. The analysis has two validation components. First, published and reconstructed DFSI scores are compared with satellite-derived inundation from the Global Flood Database for 2000–2018. Second, a strict non-overlapping temporal test uses district flood history from 1986–2004 to rank districts by primary assignable recorded district fatalities in 2005–2023. Full-period DFSI, full-period flooded area, full-period GFD summaries and outcome-period information are excluded from the temporal predictors. In the satellite comparison, an equal-weight physical-hazard index using flood-event frequency, mean duration and corrected flooded-area percentage had Spearman correlation 0.4529 with cumulative inundation area-days per square kilometre, compared with 0.3575 for published DFSI and 0.3721 for reconstructed DFSI. In the temporal test, a regularised Poisson model showed predictive signal but did not robustly outperform simple past flood-event count: final-test Spearman correlations were 0.4614 and 0.4930, respectively, and state-block uncertainty crossed zero for the model-versus-event-count comparison. The main temporal limitation is fatality attribution: many reported deaths occurred in multi-district event records that could not be assigned uniquely to districts without arbitrary allocation or duplication. The study does not invalidate DFSI or propose a universal replacement. It demonstrates an objective-specific validation workflow combining satellite comparison, non-overlapping temporal testing, geographic uncertainty analysis and simple-baseline comparison.

## 1. Introduction

District flood-priority rankings are widely attractive because they turn many sources of hazard and impact information into an administratively usable ordering of places. For agencies responsible for flood mitigation, emergency preparedness and resource allocation, a district ranking can help identify where further investigation, investment or monitoring should begin. India is a natural setting for this kind of evidence because flood impacts are widespread, administrative decisions are often made at district scale and national flood information is assembled from heterogeneous records. The District Flood Severity Index (DFSI) is therefore an important contribution: it provides a national district-level index intended to support flood management in India (Saharia et al., 2025).

The usefulness of any priority ranking depends on the decision it is meant to support. Physical inundation, population exposure and recorded human consequences are related, but they are not interchangeable. A district with repeated satellite-derived flood extent and duration may not be the district with the largest population exposed. A district with high recorded fatalities may reflect severe floods, high exposure, vulnerability, reporting intensity or a small number of extreme events. A composite index can communicate broad concern, but the validation target must be explicit. If a ranking is used for physical flood-management infrastructure, it should correspond with physical inundation. If it is used for fatality-prevention planning, it should be tested against later human impacts using information available before the outcome period.

Flood vulnerability, severity and resilience indices have a long methodological tradition. Flood Vulnerability Index approaches have been proposed at multiple spatial scales, and later work has sought to reduce index complexity and adapt composite flood indicators to cities, regions and local planning contexts (Balica et al., 2009; Balica and Wright, 2010; Balica et al., 2012; Kotzee and Reyers, 2016). India-specific work has also constructed district-level flood vulnerability indices for states such as Bihar and Uttarakhand (Jha and Gundimeda, 2019; Kumar and Bhattacharjya, 2020). These studies show why composite rankings are useful: they can combine biophysical, social, economic and institutional information in a form that is easy to map and communicate.

At the same time, composite-index methodology warns that weighting, aggregation and robustness are consequential choices. The OECD/JRC handbook treats transparency, sensitivity analysis and uncertainty analysis as core parts of composite-indicator construction (OECD/European Union/EC-JRC, 2008). Saisana et al. (2005) show how uncertainty and sensitivity analysis can be used to assess the quality of composite indicators, while Paruolo et al. (2013) show that nominal weights may differ from realised importance in rankings. Greco et al. (2019) review the methodological issues around weighting, aggregation and robustness. These concerns matter for flood-priority rankings because a high national rank correlation can still hide changes in which districts enter a priority group.

The flood-index literature also points to validation as an unsettled problem. Moreira et al. (2021) reviewed flood vulnerability indices and found that validation, sensitivity analysis, uncertainty analysis and temporal dynamics were not consistently addressed. More broadly, disaster-index validation studies show that observed outcomes can be used to test whether resilience or vulnerability indicators behave as expected (Bakkensen et al., 2017). Tellman et al. (2020) used flood deaths and property damage to validate components of social vulnerability to floods in the United States, showing that the value of indicators depends on the outcome being predicted or explained. Flood-index validation through uncertainty and sensitivity analysis is also established in the vulnerability-index literature (Aroca-Jiménez et al., 2022). Flood-risk model validation work similarly argues for clearer validation practice and benchmark comparisons (Molinari et al., 2019).

Satellite-derived flood observations provide another validation opportunity. The Global Flood Database maps large flood events from daily MODIS imagery at 250 m resolution for 2000–2018 and provides an independent record of observed inundation extent and duration (Tellman et al., 2021). These observations are not a complete record of every flood and are not a direct measure of human impact. They are, however, useful for asking whether a district-level priority score corresponds with physical flood burden.

This study uses DFSI respectfully as a case study for objective-specific validation. It does not challenge the validity of DFSI as a broad historical flood-severity index, does not try to optimise new DFSI weights and does not propose a universal replacement ranking. Instead, it asks whether different district-ranking tools correspond with different validation targets. The narrower contribution is to combine four checks that are often treated separately: independent satellite comparison for physical inundation, strict non-overlapping temporal validation for later recorded fatalities, comparison with transparent simple baselines and state-block uncertainty analysis.

The study asks two empirical questions. First, do districts with higher DFSI values show greater satellite-derived physical inundation? Second, can historical district flood records identify districts with elevated later recorded flood-fatality burden under non-overlapping temporal validation? Together, these address the broader methodological question: do complex composite rankings and fitted models add useful information beyond simple objective-specific indicators?

## 2. Data

### 2.1 Published DFSI and component data

The study uses the published India District Flood Severity Index and associated component datasets as the starting point for district-level comparison. The original DFSI paper is identified with DOI `10.1007/s11069-025-07493-9` (Saharia et al., 2025). The analysis used Version 4 of the India Flood Inventory–Impacts dataset, archived on Zenodo under DOI `10.5281/zenodo.16994648` and accessed on 29 July 2026 (Saharia, 2025). The raw project folder contains the released DFSI table, district flooded-area data, flood-impact data and the India Flood Inventory.

The verified analytical baseline contained 720 one-to-one district comparison records. Of these, 709 records had complete DFSI component values and 11 were retained as incomplete without imputation. The six DFSI components available in the baseline were flood-event count, mean flood duration, fatalities, injured people, corrected percent flooded area and population.

The published DFSI was treated as a mixed flood-priority ranking because it combines physical flood history, population as a proxy for exposure and recorded human consequences. In log-space, the reconstructed expression used in the project was:

DFSI = log10(1 + flood event count) + log10(1 + mean flood duration) + 2log10(1 + fatalities) + log10(1 + injured) + log10(1 + corrected percent flooded area) + log10(population).

The reconstructed DFSI was used only for reproducibility and comparison. It was not used as a leakage-free temporal predictor, because it is derived from full-period component information.

### 2.2 Satellite-derived inundation data

Physical flood burden was evaluated using the Global Flood Database image collection `GLOBAL_FLOOD_DB/MODIS_EVENTS/V1`, which maps large flood events from 2000–2018 (Tellman et al., 2021). Administrative boundaries were taken from `WM/geoLab/geoBoundaries/600/ADM2`, filtered to India. The GFD period only partially overlaps the longer historical period represented by DFSI.

The Earth Engine export identified 192 India-related GFD events. Of these, 148 events had detected non-permanent floodwater in Indian district-event rows. Permanent water was removed before calculating district flood metrics. Event floodwater was defined as pixels where `flooded == 1`, excluding pixels where `jrc_perm_water == 1`.

The primary satellite-derived inundation outcome was cumulative inundation area-days per square kilometre:

Cumulative inundation area-days per km2 = Σ over events and flooded non-permanent-water pixels (flooded pixel area in km2 × inundation duration in days) / district area in km2.

This outcome measures repeated mapped inundation over 2000–2018. It is area-normalised, combines mapped extent and duration and avoids treating larger districts as more severely flooded simply because they have more area. It is an independent satellite-derived comparison for physical inundation, not a complete flood inventory and not a completely independent time period relative to the historical DFSI components.

The downloaded boundary file contained 735 Indian administrative geometries. The validation sample included 657 unique accepted DFSI-boundary matches, corresponding to 92.7% of the 709 complete DFSI districts. Of these matched districts, 639 had non-zero satellite-observed floodwater.

### 2.3 Event-level flood inventory for temporal validation

The temporal validation used the event-level India Flood Inventory (Saharia et al., 2021). The event schema included event identifier, start and end dates, state, district, duration, fatalities, injuries, event source and administrative identifiers where available. Three non-overlapping 19-year periods were used: 1967–1985, 1986–2004 and 2005–2023.

The primary temporal test used district flood-history predictors from 1986–2004 to rank districts by recorded flood fatalities in 2005–2023. The earlier transition, 1967–1985 predictors to 1986–2004 outcomes, was used for development. Full-period DFSI, reconstructed full-period DFSI, full-period flooded area and full-period GFD summaries were excluded as temporal predictors.

Historical reporting volume changed substantially across the three windows. The inventory contained 762 recorded events in 1967–1985, 1,968 in 1986–2004 and 4,126 in 2005–2023. Fatality reporting completeness was 49.9%, 61.8% and 52.6% across the same periods. Injury reporting completeness was 14.2%, 17.8% and 14.5%. These changes mean the temporal exercise predicts recorded future fatalities, not unobserved mortality burden. This caution is consistent with broader concerns about natural-hazard loss data and reporting comparability (Gall et al., 2009; Jonkman and Kelman, 2005).

Fatality handling is especially important. Missing fatality values were not interpreted as verified absence of deaths. For the primary district target, a reported fatality was assigned only when the event was district-specific or single-district and the district could be matched to the verified baseline. Positive fatalities in multi-district records were not divided among districts because the inventory does not provide a verified within-event allocation rule. Therefore, a zero-fatality district means zero primary assignable recorded district deaths, not verified absence of flood deaths.

A large share of event-level reported fatalities could not be assigned uniquely to individual districts under this conservative rule, principally because they occurred in positive-fatality records listing multiple districts. In 1986–2004, the inventory reported 29,011 raw event-level fatalities, while 3,202 were primary assignable district fatalities. The largest unassigned category was multi-district positive-fatality records, accounting for 22,876 fatalities, or 78.9% of raw reported fatalities; unmatched district records accounted for 1,902 fatalities, or 6.6%; and state-only or non-district locations accounted for 1,031 fatalities, or 3.6%. In 2005–2023, the inventory reported 24,745 raw event-level fatalities, while 3,654 were primary assignable district fatalities. Multi-district positive-fatality records accounted for 19,168 unassigned fatalities, or 77.5% of raw reported fatalities; unmatched district records accounted for 1,290 fatalities, or 5.2%; and state-only or non-district locations accounted for 633 fatalities, or 2.6%. These deaths were not assumed absent; they were excluded from the district target to avoid arbitrary allocation or duplication.

## 3. Methods

### 3.1 Overall validation design

The study separated two decision targets. The first target was physical flood burden, measured using satellite-derived inundation. The second target was later recorded human consequence, measured as primary assignable recorded district flood fatalities in a future non-overlapping period. A district ranking that corresponds with satellite-derived inundation is not automatically a ranking of future recorded fatalities. A ranking that predicts recorded future fatalities is not automatically a physical-hazard ranking.

### 3.2 DFSI reproduction

The DFSI was reconstructed from the released component datasets to establish a verified comparison baseline. Incomplete records were preserved without imputation. Ranks were assigned in descending order, where rank 1 represents the highest score. The reproduction step was used only to confirm that the released components strongly reproduce the published ranking; it is not the main contribution of the paper.

### 3.3 Satellite comparison

The six DFSI variables were separated into physical hazard, population as a proxy for exposure and recorded human consequences. The main physical-hazard index was an equal-weight index: H_equal = [log10(1 + flood event count) + log10(1 + mean flood duration) + log10(1 + corrected percent flooded area)] / 3.

This equal-weight physical-hazard index is the main satellite result because it is transparent and was not fitted to the satellite outcome. A learned physical-hazard index was evaluated only as a secondary check.

The satellite benchmark comparison evaluated published DFSI, reconstructed DFSI, an equal-weight six-component log index, individual DFSI component terms and the equal-weight physical-hazard index against cumulative inundation area-days per square kilometre. Spearman rank correlation was the main metric. Kendall correlation, 2,000-sample bootstrap confidence intervals, top-10% overlap and Jaccard similarity were also calculated. The top 10% satellite group contained 66 districts.

At least one secondary valid satellite outcome was retained for supplementary reporting: cumulative flooded-area-event fraction. This outcome measures cumulative event-level flooded area normalised by district area. It does not use the invalid unique-pixel `ever_flooded_area` field.

### 3.4 State-blocked physical-hazard validation

A secondary learned physical-hazard index used nonnegative weights on the transformed event, duration and flooded-area terms: H_w = w_E x_E + w_D x_D + w_A x_A, where all weights were nonnegative and summed to 1. Weights were selected inside five grouped cross-validation folds using state and union-territory units as groups. No state or union-territory unit appeared in both training and test data within a fold. Candidate weights were selected on training units and evaluated only on held-out units. Where candidate weights were nearly tied, the tie rule selected the most even weight vector within 0.001 Spearman correlation of the best training candidate. This learned index is reported as secondary because its improvement over the equal-weight physical-hazard index was modest and geographically variable.

### 3.5 Temporal prediction of recorded future fatalities

The final temporal test used 1986–2004 predictors to rank 720 districts by primary assignable recorded district flood fatalities in 2005–2023. The development transition used 1967–1985 predictors and 1986–2004 outcomes. No final-period outcome information was used to select transformations or model settings.

The final predictors used by the primary model were `log1p(event_count)`, `log1p(mean_flood_duration)`, `log1p(total_flood_duration)`, `log1p(fatality_count)`, `log1p(injury_count)`, `log1p(fatal_event_count)`, `log1p(distinct_flood_years)` and `1 / (1 + years_since_recent_flood)`.

The primary model was a regularised Poisson count model with an L2 penalty on coefficients and regularisation setting `alpha = 1.0`. This setting was fixed before final evaluation and no large hyperparameter search was conducted. Predictors were standardised using the development transition only and then applied to the final test.

The secondary log-linear score was 0.35log1p(past fatalities) + 0.20log1p(event count) + 0.20log1p(total flood duration) + 0.15log1p(past injuries) + 0.10log1p(distinct flood years).

Because this score was secondary and not the primary prespecified model, it is reported as a benchmark and should be placed in the supplement if space is limited.

### 3.6 Temporal benchmark rankings and metrics

The primary model was compared with simple predictor-period rankings: past fatalities, past fatal-event count, past injury count, past flood-event count, past mean duration, past total duration, an equal-weight historical hazard score, a historical persistence score, population alone as a secondary sensitivity analysis and hazard plus population as a secondary sensitivity analysis.

Top-10% groups used fixed counts. In the final temporal test, the top decile contained 72 districts. Ties were broken deterministically by state and district name so that group sizes were reproducible. NDCG at the top 10% used linear fatality-count gains with logarithmic rank discount: DCG@k = Σ_i fatality count_i / log2(rank_i + 1), and NDCG@k = DCG@k / ideal DCG@k.

Paired bootstrap comparisons used 2,000 ordinary district resamples. State-block bootstrap comparisons used 2,000 resamples of entire state and union-territory units. These comparisons tested whether the primary model improved over simple baselines under district-level and geographic uncertainty.

## 4. Results

### 4.1 DFSI reproduction established the comparison baseline

The released component datasets strongly reproduced the published DFSI ranking but did not reproduce it exactly. Among 709 complete records, reconstructed DFSI had Spearman correlation 0.9588 and Pearson correlation 0.9587 with published DFSI. Detailed rank differences and top-group overlaps are treated as supplementary reproduction material.

### 4.2 Equal-weight physical-hazard index better matched satellite-derived inundation

The primary satellite outcome was cumulative inundation area-days per square kilometre. The comparison used 657 uniquely matched districts.

Published DFSI had Spearman correlation 0.3575 with the primary satellite outcome, with bootstrap confidence interval 0.2774 to 0.4300. Reconstructed DFSI had Spearman correlation 0.3721, with interval 0.2964 to 0.4441. The equal-weight physical-hazard index had a higher Spearman correlation of 0.4529, with interval 0.3840 to 0.5200.

Individual component comparisons showed that flooded area alone had Spearman correlation 0.3745, population alone 0.3944, duration alone 0.3841 and flood-event frequency alone 0.2987. The equal-weight six-component log index had Spearman correlation 0.3878.

Top-10% overlap with the satellite-derived top group also differed across measures. Published DFSI and reconstructed DFSI each overlapped with 25 of the satellite top 66 districts, with Jaccard similarity 0.2336. The equal-weight physical-hazard index overlapped with 43 of 66 districts, with Jaccard similarity 0.4831. Flooded area alone overlapped with 39 of 66 districts, with Jaccard similarity 0.4194.

Paired bootstrap comparisons supported the difference between the equal-weight physical-hazard index and mixed DFSI. The observed Spearman difference between the equal-weight physical-hazard index and published DFSI was 0.0954, with interval 0.0436 to 0.1505. The difference relative to reconstructed DFSI was 0.0808, with interval 0.0330 to 0.1304. The difference relative to flooded area alone was 0.0784, with interval 0.0116 to 0.1474.

The same direction appeared for the secondary valid satellite outcome, cumulative flooded-area-event fraction. For that outcome, the equal-weight physical-hazard index had Spearman correlation 0.4899, compared with 0.3611 for published DFSI, 0.3793 for reconstructed DFSI and 0.4440 for flooded area alone. These secondary results should be reported in a supplementary table.

These results indicate that a transparent physical-hazard-only index corresponded more strongly with satellite-derived physical inundation than the mixed DFSI. This does not show that DFSI is invalid. It shows that DFSI and satellite-derived inundation measure different constructs.

### 4.3 State-blocked validation showed positive but geographically variable associations

The learned physical-hazard index was evaluated using five grouped folds over 35 state and union-territory units. The selected weights were broadly stable: the median event weight was 0.150, the median duration weight was 0.450 and the median flooded-area weight was 0.375. Across folds, event weights ranged from 0.075 to 0.175, duration weights from 0.425 to 0.500 and flooded-area weights from 0.350 to 0.500.

The learned physical-hazard index had overall out-of-fold Spearman correlation 0.4874 and Kendall correlation 0.3433 with the primary satellite outcome. The equal-weight physical-hazard index had out-of-fold Spearman correlation 0.4529 and Kendall correlation 0.3239. Flooded area alone had out-of-fold Spearman correlation 0.3745, published DFSI 0.3575 and reconstructed DFSI 0.3721.

Fold-level results varied substantially. The learned physical-hazard index had a median held-out Spearman correlation of 0.4329 across folds, with a range from 0.0992 to 0.6462. The equal-weight physical-hazard index had a median held-out Spearman correlation of 0.4084, with a range from 0.2423 to 0.6069. Published DFSI had a median held-out Spearman correlation of 0.3947, with a range from 0.0620 to 0.5137.

State-block bootstrap results showed positive but geographically uncertain associations. The learned physical-hazard out-of-fold score had observed national Spearman correlation 0.4874 and state-block interval 0.1960 to 0.6608. The equal-weight physical-hazard index had observed national Spearman correlation 0.4529 and interval 0.1783 to 0.6384. Published DFSI had observed national Spearman correlation 0.3575 and interval 0.1148 to 0.5446.

After demeaning within state or union-territory unit, correlations were much smaller. The learned physical-hazard score had state-demeaned Spearman correlation 0.0876, the equal-weight physical-hazard index 0.1193 and published DFSI 0.0575. This suggests that the national satellite association is partly shaped by broad between-unit differences, and district-level within-unit ranking should be interpreted cautiously.

### 4.4 Fatality assignment limits the temporal target

The final temporal test used 720 districts. The outcome period, 2005–2023, contained 3,654 primary assignable recorded district fatalities. A total of 332 districts had positive primary assignable recorded future fatalities, while 388 districts, or 53.9%, had zero primary assignable recorded future fatalities. Among the 388 zero-fatality districts, 236 had matched flood-event rows and 152 had no matched event rows in 2005–2023.

These zeros should not be interpreted as confirmed absence of deaths. They mean no primary assignable recorded deaths under the conservative district attribution rule. A large share of raw reported fatalities was not assignable to a single district without risking arbitrary allocation or double counting. In 2005–2023, the dominant reason was multi-district positive-fatality records, which accounted for 19,168 unassigned fatalities, or 77.5% of all raw reported fatalities. Unmatched district records accounted for 1,290 fatalities, or 5.2%, and state-only or non-district locations accounted for 633 fatalities, or 2.6%.

This assignment problem is the main limitation of the temporal analysis. The fatality analysis is secondary to the satellite-derived inundation comparison, and it should be interpreted as prediction of primary assignable recorded district fatalities rather than precise district-level mortality burden. The model may partly predict reporting intensity or event assignability, not only flood mortality.

### 4.5 The fitted fatality model showed signal but was not robustly better than simple baselines

The primary regularised Poisson model had Spearman correlation 0.4614 and Kendall correlation 0.3607 with recorded future fatalities in the final 2005–2023 test. It identified 31 of the 72 actual future-fatality top-decile districts, giving top-10% recall 0.4306 and Jaccard similarity 0.2743. Its NDCG at the top 10% was 0.6884, average precision was 0.4032 and mean absolute error was 6.2942 fatalities.

The simple past flood-event count benchmark had Spearman correlation 0.4930 and Kendall correlation 0.3921. It identified 28 of the 72 future top-decile districts, giving top-10% recall 0.3889 and Jaccard similarity 0.2414. Past fatalities had Spearman correlation 0.3595 and top-10% recall 0.3750. The historical persistence score had Spearman correlation 0.3683 and top-10% recall 0.4167. The equal-weight historical hazard score had Spearman correlation 0.4626 but lower top-10% recall, 0.2639.

The secondary log-linear score had the highest national Spearman correlation among evaluated scores, 0.4968, with top-10% recall 0.4028. Because it was a secondary benchmark rather than the prespecified primary model, it should not be used to claim a fitted-model advantage in the main text.

Ordinary paired bootstrap comparisons showed that the primary Poisson model outperformed past fatalities on Spearman correlation by 0.1019, with interval 0.0410 to 0.1629. However, it did not outperform past flood-event count. The observed Spearman difference relative to past flood-event count was -0.0315, with interval -0.0637 to 0.0008. The difference relative to the equal-weight historical hazard score was -0.0012, with interval -0.0374 to 0.0343.

State-block bootstrap weakened claims of a model advantage further. The primary model's Spearman difference relative to past fatalities was 0.1019, but the state-block interval ranged from -0.0216 to 0.2317. Relative to past flood-event count, the Spearman difference was -0.0315, with interval -0.0951 to 0.0301. Relative to the equal-weight historical hazard score, the difference was -0.0012, with interval -0.0809 to 0.0865. For top-decile recall, all three state-block intervals crossed zero for comparisons with past fatalities, past flood-event count and the equal-weight historical hazard score.

A focused better-reporting subset check did not overturn this conclusion. Among 452 districts with at least one final-period matched event and at least 50% fatality-field reporting in final-period event rows, the primary model had Spearman correlation 0.2461 and top-10% recall 0.3913. Past flood-event count had Spearman correlation 0.3197 and top-10% recall 0.4130. This subset check is diagnostic rather than a new modelling branch, but it supports the same cautious conclusion.

The temporal result is therefore narrow: historical flood records contain predictive signal for recorded future fatalities, but the fitted model did not robustly outperform simple historical flood-event frequency.

### 4.6 Influence checks did not remove the main caution

Several diagnostics tested whether the temporal result was dominated by narrow subsets. Among 558 districts with zero historical fatalities in the predictor period, the primary model still had Spearman correlation 0.3730, but top-10% recall fell to 0.2500. After excluding states and union-territory units with the weakest reporting completeness, the primary model had Spearman correlation 0.4458 and top-10% recall 0.4737.

The final-period fatality outcome was not entirely driven by one or two individual events. The largest single district-event fatality count was 273. The top two events accounted for 11.4% of final-period fatalities, and the top ten events accounted for 22.5%.

These checks indicate that the temporal ranking signal is not purely an artefact of one disaster or one reporting subset. However, they do not remove the main caution that missing fatality reporting and non-assignable multi-district deaths limit interpretation.

## 5. Discussion

### 5.1 Main finding

The central result is that model or index complexity did not automatically produce stronger outcome-specific district rankings. This finding is deliberately narrow. It does not mean that composite indices are unnecessary, that DFSI is invalid or that simple indicators should replace all flood-priority tools. It means that added complexity should be evaluated against a stated decision target and compared with simple alternatives before being treated as useful.

This is important because composite flood-priority rankings can appear more comprehensive simply because they combine more information. Comprehensiveness, however, is not the same as validation. A mixed index can be a useful historical summary while still being less closely aligned with one specific outcome. The results here show that the answer depends on the target: physical inundation was better matched by a physical-hazard-only score, while later recorded fatalities were predicted about as well by past flood-event frequency as by a fitted model.

### 5.2 Physical inundation

The satellite comparison provides the clearest empirical support for construct separation. The equal-weight physical-hazard index combined event frequency, mean duration and corrected flooded-area percentage, and it corresponded more strongly with cumulative satellite-derived inundation area-days than the mixed DFSI. This result should not be read as evidence against DFSI's broader purpose. DFSI was not designed only as a satellite-inundation index. It also includes population as a proxy for exposure, fatalities and injuries. These are important dimensions of flood concern, but they do not necessarily improve correspondence with physical water extent and duration.

The distinction matters in practical terms. If the decision objective is flood-control infrastructure, drainage planning or identifying districts with repeated physical inundation, a physical-hazard score is easier to interpret. If the decision objective is social protection, emergency response or mortality prevention, population and recorded impacts become more relevant. Treating all of these objectives as one ranking risks making the score difficult to validate because success against one target can imply weaker correspondence with another.

The learned physical-hazard index had slightly higher national correlation with the satellite outcome than the equal-weight hazard index, but the improvement was modest and geographically variable. For this reason, the equal-weight hazard index remains the main satellite result. It is transparent, uses only physical-hazard components and was not fitted to the satellite outcome. The learned weights are useful as a check, not as a proposed new national index.

### 5.3 Later recorded fatalities

The temporal fatality analysis asked a different question: whether information available from a district's earlier flood history could identify districts with elevated later primary assignable recorded district fatalities. The answer is cautiously positive, but not in a way that justifies claiming model superiority. The regularised Poisson model showed predictive signal on the final 2005–2023 period, but simple past flood-event count had a higher Spearman correlation, and state-block bootstrap uncertainty crossed zero for the model-versus-event-count comparison.

This does not mean modelling has no value. The Poisson model had slightly higher top-decile recall than event count, and it may capture complementary aspects of fatal-event history, duration and recency. But a fitted model should not be treated as better merely because it is more complex. In a prioritisation setting, the practical question is whether the extra modelling choices produce more reliable district rankings for the decision being made. Here, that case was not robust.

The finding also supports the need for simple baselines. Past event count is transparent, easy to explain and difficult to beat in this dataset. A fitted model that does not clearly improve on such a baseline may still be useful for sensitivity or diagnosis, but it should not be presented as a superior national fatality-prioritisation ranking.

### 5.4 Geographic variation

The geographic checks further limit strong ranking claims. The national satellite associations were positive, but held-out fold correlations varied widely across state and union-territory groups. Within-state demeaned correlations were much smaller than national correlations. This suggests that part of the national relationship reflects broad differences between state and union-territory units rather than precise within-unit district ordering.

For users of district rankings, this distinction matters. A ranking can look useful nationally while being less reliable for choosing between districts inside the same state. Many operational decisions are made within state-level planning systems, so weak within-state association should temper claims about local precision. State-block validation does not make the satellite result disappear, but it changes its interpretation: the relationship is positive and meaningful, yet geographically variable.

### 5.5 Fatality attribution

The most important limitation of the temporal analysis is fatality attribution. The issue is not simply that fatality fields were absent. Most excluded reported deaths occurred in event records listing multiple districts, where the inventory did not provide a verified rule for dividing fatalities among districts. Under the conservative district attribution rule, these deaths were not assumed absent. They were excluded from the district target to avoid arbitrary splitting or duplicating the same event total across all listed districts.

This choice protects the temporal validation from a different error: creating artificial district fatalities by copying a multi-district total to every district. But it also means the target is conservative and incomplete. The correct interpretation is prediction of primary assignable recorded district fatalities, not precise district-level mortality burden. Districts with zero assignable recorded deaths may still have experienced deaths that were reported only in multi-district or unmatched event records.

The original DFSI district-allocation procedure could not be verified from the released documentation. The released district flood-impact table is already aggregated to district totals and does not include event identifiers, allocation flags, dates or provenance fields showing how multi-district event fatalities were transformed into district-level values. This does not imply that the original procedure was incorrect. It only means that the temporal-validation rule used here should be described as an independent conservative attribution rule rather than a reproduction of the original DFSI allocation method.

### 5.6 Practical meaning

The practical lesson is that flood-priority rankings should state their decision objective. Physical flood-management infrastructure, population exposure reduction, fatality prevention, social vulnerability analysis and emergency response may each need different rankings. A single composite score can still be useful as a broad screening tool, especially when decision makers need an interpretable national overview. But it should not automatically be assumed equally suitable for every decision.

For India district flood prioritisation, the results suggest a multi-axis framing may be more honest than a single universal score. Physical hazard, population as a proxy for exposure and recorded human consequences can be reported together but validated separately. This approach does not remove judgement from prioritisation. It makes the judgement visible: users can see which districts are high on physical inundation, which are high on exposure and which have recorded human consequences.

### 5.7 Contribution

The paper demonstrates an objective-specific validation workflow combining satellite comparison, non-overlapping temporal testing, geographic uncertainty analysis and simple-baseline comparison. Each part exists in related literature, but the combination is useful for district-level Indian flood prioritisation. The workflow asks not only whether a composite ranking is correlated with something, but whether it corresponds with the right outcome, whether it adds value over simple indicators and whether the result remains credible under geographic uncertainty.

This contribution is best framed as a short methodological article. It is not a new universal index, not a claim of exact DFSI reproduction and not a final model for national flood-fatality prediction. Its value is in showing how to audit ranking usefulness before relying on complexity.

## 6. Limitations

The Global Flood Database is not a complete inventory of every Indian flood. It maps large satellite-observed events from 2000–2018, so the satellite comparison partially overlaps with the historical DFSI period and should be interpreted as convergent evidence for physical inundation, not as full independent validation of all flood history.

Administrative-boundary mismatch remains a limitation. The GFD comparison used 657 unique accepted DFSI-boundary matches, but unmatched and ambiguous records were retained outside the accepted match set. Boundary vintage differences can affect district-level comparisons, especially where districts split or names changed.

The satellite association is geographically variable. State-blocked validation showed positive associations, but fold-level performance varied, and state-demeaned correlations were weak. National rank correlations should therefore not be interpreted as precise within-state district ordering.

Historical event reporting changed substantially over time. Event counts, district coverage, fatality completeness and injury completeness varied across the 1967–1985, 1986–2004 and 2005–2023 windows. Recorded changes cannot be interpreted directly as changes in physical flood frequency.

Injury records were sparse, and fatality attribution was conservative. Multi-district positive-fatality records were not allocated to individual districts because the inventory did not provide a verified within-event allocation rule. The original DFSI fatality-allocation procedure could not be verified from the released documentation. This limits the temporal analysis to primary assignable recorded district fatalities.

Many districts had zero primary assignable recorded future fatalities, creating tied outcomes and limiting fine-grained ranking interpretation. The study does not claim universal risk prediction, a superior national flood ranking or a replacement for DFSI.

## 7. Conclusion

This study shows that complex flood-priority rankings should be validated against the specific outcome they are meant to support. In the satellite comparison, a transparent physical-hazard-only index corresponded more strongly with satellite-derived inundation than the mixed DFSI. This does not invalidate DFSI; it shows that a mixed index and physical inundation measure different constructs.

In the temporal test, historical flood records contained predictive signal for primary assignable recorded district fatalities in a later period. However, the fitted Poisson model did not robustly outperform simple past flood-event count, especially under state-block uncertainty. Complexity therefore did not clearly add value for the future-fatality ranking task.

No universal replacement ranking is proposed. The main recommendation is methodological: district flood-priority tools should separate physical inundation, population as a proxy for exposure and recorded human consequences; validate each ranking against an objective-specific outcome; and compare complex scores with simple baselines. The temporal fatality result remains limited by reporting change and by multi-district fatality records that could not be assigned uniquely to districts without arbitrary allocation or duplication. These constraints make the paper strongest as a short methodological article rather than as a claim to a new operational national ranking. The defensible contribution is the validation workflow and the caution that complexity should earn its place through demonstrated added value.

## 8. Data and Code Availability

The IFI-Impacts Version 4 dataset is available from Zenodo under DOI `10.5281/zenodo.16994648`. The Global Flood Database is available through Google Earth Engine as `GLOBAL_FLOOD_DB/MODIS_EVENTS/V1`. The administrative boundaries used for the satellite comparison are available in Google Earth Engine as `WM/geoLab/geoBoundaries/600/ADM2`.

Analysis code and derived outputs will be archived in a public repository before submission. Repository URL or DOI: `[TO BE INSERTED BEFORE SUBMISSION]`.

## 9. References

Aroca-Jiménez, E., Bodoque, J.M., García, J.A. and Figueroa-García, J.E. (2022) ‘Holistic characterization of flash flood vulnerability: Construction and validation of an integrated multidimensional vulnerability index’, *Journal of Hydrology*, 612, Part A, article 128083. doi:10.1016/j.jhydrol.2022.128083.

Bakkensen, L.A., Fox-Lent, C., Read, L.K. and Linkov, I. (2017) ‘Validating resilience and vulnerability indices in the context of natural disasters’, *Risk Analysis*, 37(5), pp. 982–1004. doi:10.1111/risa.12677.

Balica, S.F., Douben, N. and Wright, N.G. (2009) ‘Flood vulnerability indices at varying spatial scales’, *Water Science and Technology*, 60(10), pp. 2571–2580. doi:10.2166/wst.2009.183.

Balica, S.F. and Wright, N.G. (2010) ‘Reducing the complexity of the flood vulnerability index’, *Environmental Hazards*, 9(4), pp. 321–339. doi:10.3763/ehaz.2010.0043.

Balica, S.F., Wright, N.G. and van der Meulen, F. (2012) ‘A flood vulnerability index for coastal cities and its use in assessing climate change impacts’, *Natural Hazards*, 64(1), pp. 73–105. doi:10.1007/s11069-012-0234-1.

Gall, M., Borden, K.A. and Cutter, S.L. (2009) ‘When do losses count? Six fallacies of natural hazards loss data’, *Bulletin of the American Meteorological Society*, 90(6), pp. 799–810. doi:10.1175/2008BAMS2721.1.

Greco, S., Ishizaka, A., Tasiou, M. and Torrisi, G. (2019) ‘On the methodological framework of composite indices: A review of the issues of weighting, aggregation, and robustness’, *Social Indicators Research*, 141(1), pp. 61–94. doi:10.1007/s11205-017-1832-9.

Jha, R.K. and Gundimeda, H. (2019) ‘An integrated assessment of vulnerability to floods using composite index – A district level analysis for Bihar, India’, *International Journal of Disaster Risk Reduction*, 35, article 101074. doi:10.1016/j.ijdrr.2019.101074.

Jonkman, S.N. and Kelman, I. (2005) ‘An analysis of the causes and circumstances of flood disaster deaths’, *Disasters*, 29(1), pp. 75–97. doi:10.1111/j.0361-3666.2005.00275.x.

Kotzee, I. and Reyers, B. (2016) ‘Piloting a social-ecological index for measuring flood resilience: A composite index approach’, *Ecological Indicators*, 60, pp. 45–53. doi:10.1016/j.ecolind.2015.06.018.

Kumar, D. and Bhattacharjya, R.K. (2020) ‘Estimation of integrated flood vulnerability index for the hilly region of Uttarakhand, India’, *Journal of Hazardous, Toxic, and Radioactive Waste*, 24(4), article 04020051. doi:10.1061/(ASCE)HZ.2153-5515.0000540.

Molinari, D., De Bruijn, K.M., Castillo-Rodríguez, J.T., Aronica, G.T. and Bouwer, L.M. (2019) ‘Validation of flood risk models: Current practice and possible improvements’, *International Journal of Disaster Risk Reduction*, 33, pp. 441–448. doi:10.1016/j.ijdrr.2018.10.022.

Moreira, L.L., de Brito, M.M. and Kobiyama, M. (2021) ‘Review article: A systematic review and future prospects of flood vulnerability indices’, *Natural Hazards and Earth System Sciences*, 21(5), pp. 1513–1530. doi:10.5194/nhess-21-1513-2021.

OECD/European Union/EC-JRC (2008) *Handbook on constructing composite indicators: Methodology and user guide*. Paris: OECD Publishing. doi:10.1787/9789264043466-en.

Paruolo, P., Saisana, M. and Saltelli, A. (2013) ‘Ratings and rankings: Voodoo or science?’, *Journal of the Royal Statistical Society Series A: Statistics in Society*, 176(3), pp. 609–634. doi:10.1111/j.1467-985X.2012.01059.x.

Saharia, M. (2025) *India Flood Inventory-Impacts (IFI-Impacts) [1967–2023]: A multi-source national geospatial database to facilitate comprehensive flood research*. Version v4. Zenodo. doi:10.5281/zenodo.16994648. Accessed 29 July 2026.

Saharia, M., Jain, A., Baishya, R.R., Haobam, S., Sreejith, O.P., Pai, D.S. and Rafieeinasab, A. (2021) ‘India flood inventory: creation of a multi-source national geospatial database to facilitate comprehensive flood research’, *Natural Hazards*, 108(1), pp. 619–633. doi:10.1007/s11069-021-04698-6.

Saharia, M., Jain, S.K., Prakash, V., Malik, H., Sreejith, O.P. and Joshi, D. (2025) ‘A district-level flood severity index for flood management in India’, *Natural Hazards*, 121(15), pp. 17815–17831. doi:10.1007/s11069-025-07493-9.

Saisana, M., Saltelli, A. and Tarantola, S. (2005) ‘Uncertainty and sensitivity analysis techniques as tools for the quality assessment of composite indicators’, *Journal of the Royal Statistical Society Series A: Statistics in Society*, 168(2), pp. 307–323. doi:10.1111/j.1467-985X.2005.00350.x.

Tellman, B., Schank, C., Schwarz, B., Howe, P.D. and de Sherbinin, A. (2020) ‘Using disaster outcomes to validate components of social vulnerability to floods: Flood deaths and property damage across the USA’, *Sustainability*, 12(15), article 6006. doi:10.3390/su12156006.

Tellman, B., Sullivan, J.A., Kuhn, C., Kettner, A.J., Doyle, C.S., Brakenridge, G.R., Erickson, T.A. and Slayback, D.A. (2021) ‘Satellite imaging reveals increased proportion of population exposed to floods’, *Nature*, 596(7870), pp. 80–86. doi:10.1038/s41586-021-03695-w.
