# Do Complex Flood-Priority Rankings Add Value?

## Satellite and Temporal Validation of District Flood Prioritisation in India

**Draft status:** first professor-facing draft. This is not submission-ready text. Citation placeholders mark references that still need full-text verification.

## Abstract

Composite flood-priority indices are often designed to summarise multiple dimensions of flood concern in a single ranking. Such rankings can be useful for communication, but they may also combine distinct decision targets, including physical flooding, exposure and recorded human consequences. This study evaluates whether complex composite flood-priority rankings and fitted predictive models provide more useful district rankings than simpler, objective-specific historical indicators.

We use India as a national district-scale case study, centred on the published District Flood Severity Index (DFSI). The analysis has two validation components. First, we compare published and reconstructed DFSI scores with independently satellite-observed flood inundation from the Global Flood Database for 2000-2018. Second, we conduct a strict non-overlapping temporal validation, using district flood history from 1986-2004 to rank districts by recorded flood-fatality burden in 2005-2023. Full-period DFSI, full-period flooded area, full-period GFD metrics and outcome-period information are not used as temporal predictors.

The satellite comparison suggests that a physical-hazard index using flood-event frequency, mean flood duration and flooded-area percentage corresponds more strongly with satellite-observed inundation than the mixed six-component DFSI. For the primary satellite outcome, the equal-weight physical-hazard index had a Spearman correlation of 0.4529, compared with 0.3575 for published DFSI and 0.3721 for reconstructed DFSI. In the temporal fatality-ranking test, a regularised Poisson model showed predictive signal, with Spearman correlation 0.4614 and top-10% recall 0.4306. However, it did not robustly outperform simple past flood-event frequency, which had Spearman correlation 0.4930 and top-10% recall 0.3889. State-block uncertainty further weakened claims of model superiority.

These results do not invalidate DFSI. Instead, they show that different flood-prioritisation objectives require different validation targets. Physical inundation, population exposure and future recorded fatalities should not be assumed to be captured equally well by one universal ranking. The study supports a short methodological contribution: flood-priority indices should be validated against the specific decision objective they are meant to support and compared with simple baselines before added complexity is treated as useful.

## 1. Introduction

Flood-priority rankings are attractive because they reduce a complex national problem into an ordered list of places requiring attention. For governments and disaster-management agencies, such lists can support screening, resource allocation and communication. However, a single ranking can hide an important question: what exactly is being prioritised?

Flood impacts include physical inundation, population exposure, mortality, injury, economic damage, disruption and long-term vulnerability. These are related but not identical constructs. A district that floods frequently may not be the district with the highest population exposure. A district with high recorded fatalities may not be the district with the greatest satellite-observed inundation. A composite index that combines these dimensions may therefore be useful as a historical summary but less clear as a decision tool unless it is validated against the outcome it is intended to support.

The District Flood Severity Index (DFSI) was recently developed as a national district-level flood severity index for India [CITE: Saharia et al. 2025]. DFSI combines flood-event frequency, mean flood duration, fatalities, injuries, corrected flooded area and population into a single district score. This is an important contribution because district-level flood prioritisation in India requires national, administratively meaningful evidence. At the same time, the mixed nature of DFSI raises a methodological question: does the combined index correspond equally well with physical flood burden and later human impacts?

This paper does not propose a replacement index and does not claim that DFSI is invalid. Instead, it treats DFSI as a case study for a broader validation question. Composite flood and vulnerability indices are common, but reviews have found that validation, uncertainty analysis and temporal dynamics are often underdeveloped [CITE: Moreira et al. 2021; CITE: Hamidi et al. 2025]. Related work has validated vulnerability and resilience indicators against observed disaster outcomes [CITE: Bakkensen et al. 2017; CITE: Tellman et al. 2020]. Our contribution is narrower: we ask whether complex district flood-priority rankings in India add value relative to simple, objective-specific historical indicators under two independent validation targets.

The study is guided by two questions:

1. Do districts with higher DFSI values also show greater independently satellite-observed physical inundation?
2. Can historical district flood records identify districts at elevated future recorded flood-fatality burden under strict non-overlapping temporal validation?

The larger methodological question is whether complex composite flood-priority indices and fitted models provide more useful rankings than simple historical baselines. This is a construct-validation and added-value study, not a new index proposal.

## 2. Data

### 2.1 District Flood Severity Index data

The study uses the published DFSI component datasets available in the project raw data folder. These include the released DFSI table, district flooded-area data, flood-impact data and the India Flood Inventory. The verified baseline contains 720 one-to-one district comparison records. Of these, 709 records were complete for DFSI reconstruction and 11 were retained as incomplete without imputation.

The published DFSI combines six components:

- flood-event count;
- mean flood duration;
- fatalities;
- injured people;
- corrected percent flooded area;
- population.

The project approximately reproduced the published DFSI ranking but did not claim exact numerical reproduction. The verified reproduction produced strong ranking agreement with published DFSI, with Spearman correlation 0.95885 and Pearson correlation 0.95872. The median absolute numerical difference was 1.20677, and the median absolute rank difference was 18.

### 2.2 Global Flood Database satellite data

Satellite-observed flood inundation was obtained from the Global Flood Database (GFD), which maps large flood events using MODIS imagery over 2000-2018 [CITE: Tellman et al. 2021]. The GFD is not a complete inventory of every flood in India. It is used here as an independent satellite-observed sample of physical inundation.

The GFD comparison used unique accepted matches between DFSI districts and administrative boundaries. The validation sample included 657 matched districts across 35 states. Among these, 639 had non-zero satellite-observed floodwater. The primary satellite outcome was cumulative inundation area-days per square kilometre. This outcome was chosen because it is area-normalised and captures both extent and duration of mapped inundation.

The GFD period, 2000-2018, only partially overlaps the longer historical period represented by DFSI. For this reason, the satellite analysis is interpreted as convergent validity evidence for physical flood burden, not as definitive ground-truth validation of DFSI.

### 2.3 India Flood Inventory event data

The temporal prediction analysis uses the event-level India Flood Inventory. The actual event-level fields used include event identifier, start date, state, district, duration, fatalities, injuries, event source and available administrative identifiers.

Three equal-length 19-year windows were used:

- 1967-1985;
- 1986-2004;
- 2005-2023.

The primary temporal test predicts recorded district flood fatalities in 2005-2023 using only district flood-history predictors from 1986-2004. A historical replication transition uses 1967-1985 predictors and 1986-2004 outcomes.

The inventory shows substantial reporting change over time. Recorded events increased from 762 in 1967-1985 to 1,968 in 1986-2004 and 4,126 in 2005-2023. Fatality reporting completeness also changed between periods. These changes mean that temporal results must be interpreted as prediction of recorded flood-fatality burden, not necessarily physical changes in flood frequency or true mortality risk.

## 3. Methods

### 3.1 Study design

The study separates two validation targets:

1. **Physical flood burden**, measured using satellite-observed inundation from GFD.
2. **Future recorded human consequences**, measured using recorded district flood fatalities in a later, non-overlapping period.

This separation is central. A score that matches satellite-observed inundation is not automatically a good fatality-prioritisation score, and a score that predicts later fatalities is not automatically a physical-hazard score.

### 3.2 DFSI reproduction and construct separation

The DFSI was reconstructed from released component datasets to create a verified analytical baseline. The reconstruction was not forced to match the published values. Incomplete records were preserved without imputation.

For construct separation, the six DFSI components were grouped conceptually:

- physical hazard: flood-event count, mean flood duration and corrected flooded-area percentage;
- exposure: population;
- recorded human consequences: fatalities and injuries.

The physical-hazard-only index was constructed using the same log transformation style as DFSI:

`H_equal = mean(log10(1 + events), log10(1 + duration), log10(1 + corrected flooded area))`

A learned physical-hazard index was also evaluated using state-blocked cross-validation, with nonnegative weights on the three physical-hazard terms.

### 3.3 Satellite validation

The satellite validation compared multiple index measures with the primary satellite outcome, cumulative inundation area-days per square kilometre. The measures included published DFSI, reconstructed DFSI, individual DFSI components, an equal-weight six-component log index and physical-hazard-only indices.

The main metric was Spearman rank correlation, supported by Kendall correlation, bootstrap confidence intervals, top-10% overlap and Jaccard similarity. The analysis was conducted nationally and with geographic robustness checks.

### 3.4 Temporal prediction of future fatalities

The temporal prediction analysis used only information available before the outcome period. The final test used 1986-2004 district history to predict 2005-2023 recorded flood fatalities. The full-period DFSI, reconstructed full-period DFSI, full-period flooded area and full-period GFD metrics were excluded as predictors to avoid temporal leakage.

For each district and predictor period, the analysis calculated event count, total duration, mean duration, maximum duration, fatality count, injury count, fatal-event count, injury-event count, proportion of events with fatalities, proportion of events with injuries, distinct flood years and recency.

The primary fitted model was a regularised Poisson count model predicting future fatalities. A restrained log-linear risk score was also evaluated as a secondary model.

### 3.5 Simple benchmark rankings

The fitted model was compared with transparent benchmark rankings based only on the predictor period:

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

This comparison is important because a complex model is only useful if it improves on simple alternatives relevant to the same decision objective.

### 3.6 Evaluation metrics

For the temporal final test, rankings were evaluated using:

- Spearman correlation with future fatalities;
- Kendall correlation;
- top-10% overlap and recall;
- Jaccard similarity;
- NDCG at the top 10%;
- average precision for identifying the future top 10%;
- mean absolute error for fatality counts;
- calibration by predicted-risk quintile.

Paired ordinary bootstrap and state-block bootstrap were used to compare the primary model with key baselines. State-block bootstrap resampled entire states to reflect geographic dependence.

## 4. Results

### 4.1 DFSI was strongly but not exactly reproduced

The released component datasets strongly reproduced the overall DFSI ranking. The verified reconstruction used 709 complete district records and achieved Spearman correlation 0.95885 with published DFSI. Pearson correlation was 0.95872. However, the reproduction was not numerically exact: the median absolute numerical difference was 1.20677, the median absolute rank difference was 18 and the maximum absolute rank difference was 345.

This supports using the reconstructed data for validation, but it does not support a claim of exact reproduction.

### 4.2 Physical-hazard indices aligned better with satellite-observed inundation than mixed DFSI

The GFD validation sample included 657 uniquely matched districts. The primary satellite outcome was cumulative inundation area-days per square kilometre.

For this physical flood-burden outcome, the equal-weight physical-hazard index had a stronger rank correlation than the mixed DFSI:

- equal-weight physical-hazard index: Spearman 0.4529, bootstrap interval 0.3840 to 0.5200;
- published DFSI: Spearman 0.3575, bootstrap interval 0.2774 to 0.4300;
- reconstructed DFSI: Spearman 0.3721, bootstrap interval 0.2964 to 0.4441;
- flooded-area component alone: Spearman 0.3745;
- population component alone: Spearman 0.3944.

State-blocked cross-validation for a learned physical-hazard index produced out-of-fold Spearman correlation 0.4874. The equal-weight physical-hazard index had out-of-fold Spearman 0.4529, flooded area alone 0.3745 and published DFSI 0.3575.

These results suggest that physical inundation is better represented by physical-hazard components than by a mixed index that also includes population and recorded human impacts.

### 4.3 Future recorded fatalities had predictive signal but remained sparse

The final temporal test ranked 720 districts by predicted recorded flood fatalities in 2005-2023. The outcome period contained 3,654 primary assignable recorded fatalities. However, 388 districts, or 53.9%, had zero recorded future fatalities. This sparsity creates many ties and limits strong ranking claims.

The primary Poisson model showed predictive signal:

- Spearman correlation: 0.4614;
- Kendall correlation: 0.3607;
- top-10% recall: 0.4306;
- NDCG at top 10%: 0.6884;
- average precision: 0.4032;
- mean absolute error: 6.2942.

The model therefore captured some future fatality burden, but the key question is whether it improved over simpler rankings.

### 4.4 Simple past flood-event frequency was hard to beat

The simple past flood-event count benchmark performed at least as well as the fitted Poisson model on national rank correlation:

- past flood-event count: Spearman 0.4930, top-10% recall 0.3889;
- primary Poisson model: Spearman 0.4614, top-10% recall 0.4306;
- past fatalities: Spearman 0.3595, top-10% recall 0.3750;
- historical persistence score: Spearman 0.3683, top-10% recall 0.4167.

The fitted model improved top-10% recall relative to event count, but event count had the stronger Spearman correlation. This means the model cannot be described as clearly superior.

Paired bootstrap comparisons support this cautious interpretation. Against past fatalities, the primary model had a positive ordinary-bootstrap Spearman difference of 0.1019, with interval 0.0410 to 0.1629. Against past flood-event count, the observed Spearman difference was negative, -0.0315, with ordinary-bootstrap interval -0.0637 to 0.0008. Against the equal-weight historical hazard score, the observed Spearman difference was -0.0012, with interval -0.0374 to 0.0343.

State-block bootstrap further weakened model-superiority claims. For the primary model versus past fatalities, the state-block Spearman interval crossed zero, from -0.0216 to 0.2317. For the primary model versus past flood-event count, the interval was -0.0951 to 0.0301. For the primary model versus equal-weight historical hazard, the interval was -0.0809 to 0.0865.

The conclusion is not that modelling is useless. Rather, under this dataset and validation design, the fitted model did not robustly outperform simple historical flood-event frequency.

### 4.5 Reporting completeness limits temporal interpretation

The historical inventory changed substantially over time. Recorded event volume increased across the three 19-year periods, and fatality/injury reporting completeness varied. Therefore, observed changes cannot be interpreted directly as physical flood trends.

The temporal ranking should be read as predicting recorded flood-fatality burden, not true unobserved mortality risk. The analysis also avoided duplicating multi-district fatality totals across all mentioned districts. This makes district fatality counts conservative but avoids creating artificial deaths through double counting.

## 5. Discussion

The central result is simple: more complex flood-priority rankings did not automatically provide better district rankings.

For physical inundation, the mixed DFSI was less aligned with satellite-observed flood burden than a physical-hazard-only index. This is not surprising once the construct is made explicit. DFSI includes population, fatalities and injuries, which are not measurements of physical inundation. A district may be socially important or historically deadly without having the greatest satellite-observed flooded area-days.

For future recorded fatalities, the fitted model showed real predictive signal, but it did not clearly beat simple past flood-event frequency. This matters because complex models and composite indices are often assumed to add value. In a prioritisation setting, that assumption should be tested. If a simple, transparent indicator performs similarly, the burden of justification for a complex score becomes higher.

The findings align with prior work arguing that vulnerability and disaster indices should be validated against observed outcomes and should be matched to the decision they are intended to support [CITE: Bakkensen et al. 2017; CITE: Tellman et al. 2020]. They also support review findings that flood vulnerability indices often lack validation, uncertainty analysis and temporal dynamics [CITE: Moreira et al. 2021].

The practical implication is not to discard composite indices. Composite indices can still be useful as descriptive summaries. The problem arises when a single composite ranking is treated as equally valid for multiple decisions. A flood-management agency may need one ranking for physical inundation exposure, another for future fatality prevention and another for social vulnerability. These rankings can overlap, but they should not be assumed to be interchangeable.

This study therefore supports construct separation. Physical hazard, exposure and recorded human consequences should be reported as related but distinct dimensions. A mixed index may remain useful, but its purpose should be stated clearly and validated against that purpose.

## 6. Limitations

First, the satellite validation uses GFD events from 2000-2018. This only partially overlaps the longer historical period represented by DFSI. GFD is also not a complete inventory of all Indian floods. The satellite analysis should therefore be interpreted as convergent validity evidence for physical flood burden, not as definitive validation or invalidation of DFSI.

Second, district boundary matching is imperfect. The GFD validation used 657 unique accepted district matches, but unmatched and ambiguous records remain.

Third, the temporal fatality analysis depends on historical reporting quality. Reporting volume and fatality completeness changed across periods. The outcome is recorded district flood fatalities, not necessarily all true flood fatalities.

Fourth, multi-district event fatalities were not allocated across districts. This avoids double counting, but it may understate district fatality burden for large regional events.

Fifth, many districts had zero recorded future fatalities. This makes ranking difficult and limits claims about precise district ordering.

Sixth, population was used only as a secondary sensitivity variable in the temporal prediction analysis because its exact reference year/source was not fully documented in the current project files.

Finally, the literature review is still in progress. The closest papers have been screened, but several require full-text verification before final submission claims can be made.

## 7. Conclusion

This first draft supports a narrow methodological claim. In India district flood prioritisation, complex composite indices and fitted predictive models did not automatically outperform simple, objective-specific historical indicators.

The physical-hazard-only index corresponded more strongly with satellite-observed inundation than the mixed DFSI. For later recorded fatalities, the fitted Poisson model showed predictive signal but did not robustly outperform past flood-event frequency, especially under state-block uncertainty.

The study does not show that DFSI is wrong. It shows that flood-priority rankings must be validated against the decision objective they are meant to support. Physical inundation and future human consequences are different targets. A single universal ranking should not be assumed to serve both.

The recommended paper format is a short methodological article. The strongest contribution is a leakage-aware validation workflow: separate constructs, compare against independent outcomes, use non-overlapping time periods where prediction is claimed and test complex rankings against simple baselines.

## 8. References to Verify

These references are placeholders and should be verified against full text before submission.

- [CITE: Saharia et al. 2025] Original District Flood Severity Index paper.
- [CITE: Saharia et al. 2021] India Flood Inventory paper.
- [CITE: Tellman et al. 2021] Global Flood Database / satellite flood exposure paper.
- [CITE: Tellman et al. 2020] Disaster outcomes validating social vulnerability to floods.
- [CITE: Bakkensen et al. 2017] Validation of resilience and vulnerability indices using observed disaster impacts.
- [CITE: Moreira et al. 2021] Systematic review of flood vulnerability indices.
- [CITE: Hamidi et al. 2025] Systematic review of social vulnerability to floods.
- [CITE: Aroca-Jimenez et al. 2022] Integrated multidimensional flash flood vulnerability index.
- [CITE: Jha and Gundimeda 2019] District-level flood vulnerability index for Bihar, India.
- [CITE: Kumar and Bhattacharjya 2020] Integrated flood vulnerability index for Uttarakhand, India.
- [CITE: Molinari et al. 2019] Flood risk model validation practice.
- [CITE: Saisana et al. 2005] Composite-indicator uncertainty and sensitivity analysis.
- [CITE: Paruolo et al. 2013] Ratings, rankings and composite-indicator importance.
- [CITE: Greco et al. 2019] Composite-index weighting, aggregation and robustness review.
- [CITE: OECD/JRC 2008] Handbook on constructing composite indicators.
- [CITE: Gall et al. 2009] Natural hazards loss-data limitations.
