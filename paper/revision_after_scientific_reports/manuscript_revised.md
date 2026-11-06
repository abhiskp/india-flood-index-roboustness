# Do Complex Flood-Priority Rankings Add Value? Satellite and Temporal Validation of District Flood Prioritisation in India

## Abstract

District flood-priority indices combine heterogeneous evidence into usable rankings, but their reliability depends on the outcome they are intended to represent and on the consistency of district records. We evaluated India's District Flood Severity Index (DFSI) primarily against satellite-derived physical inundation and secondarily through retrospective out-of-time physical validation. Published and reconstructed DFSI scores and transparent component benchmarks were compared with cumulative non-permanent inundation area-days per square kilometre from 192 India-related Global Flood Database events during 2000–2018. Of 709 complete DFSI districts, 657 had accepted district-boundary matches; 52 (7.3%) were excluded because a unique match could not be established. On a stricter stable-match subset (n = 648), published DFSI correlated with satellite-derived inundation at Spearman \(\rho=0.3606\) (95% bootstrap confidence interval 0.2853–0.4336), whereas an equal-weight physical-hazard index based on event frequency, duration and flooded area reached \(\rho=0.4595\) (0.3875–0.5253). The paired difference was 0.0989 (0.0435–0.1513), and removing each of the five largest contributing satellite events did not reverse it. In a retrospective physical test, information through 2010 was compared with inundation during 2011–2018; an event-duration score had \(\rho=0.3759\), but its improvement over event count was uncertain under state/union-territory block resampling. A secondary fatality analysis was allocation-sensitive (rank \(\rho=0.6541\); median shift 116 ranks), and the Poisson model did not show geographically robust superiority over event count under either allocation. The main conclusion is therefore objective-specific: a transparent physical-hazard ranking aligned more closely with mapped physical inundation, while human-impact rankings require stronger provenance and allocation evidence.

## 1. Introduction

District rankings are attractive tools for flood management because they compress many indicators into an administratively recognisable ordering of places. Such rankings can help organise screening, monitoring and resource-allocation discussions. Their interpretation, however, depends on the decision target. Physical inundation, population as a proxy for exposure, social vulnerability and recorded human consequences are related dimensions of flood concern, but they are not interchangeable.

Composite flood indices can be valuable precisely because they bring these dimensions together. Flood Vulnerability Index approaches have been developed at multiple spatial scales, including city, catchment and regional applications (Balica et al., 2009; Balica and Wright, 2010; Balica et al., 2012). Indian studies have similarly constructed district-level vulnerability and severity rankings to support flood planning (Jha and Gundimeda, 2019; Kumar and Bhattacharjya, 2020; Saharia et al., 2025). The published District Flood Severity Index (DFSI) is an important national-scale example because it combines historical flood frequency and duration, flooded area, population, fatalities and injuries for Indian districts (Saharia et al., 2025).

The comprehensiveness of a composite index does not by itself establish its suitability for every decision. Composite-indicator guidance emphasises transparency, sensitivity analysis and validation because weighting, aggregation and data quality can change rankings (OECD/European Union/EC-JRC, 2008; Saisana et al., 2005; Paruolo et al., 2013; Greco et al., 2019). Flood-index reviews likewise identify uneven use of external validation, uncertainty analysis and temporal testing (Moreira et al., 2021). Observed disaster outcomes can provide validation evidence (Bakkensen et al., 2017; Tellman et al., 2020), but the outcome must match the construct. An index containing exposure and human impacts should not necessarily be expected to maximise agreement with physical water extent and duration.

Satellite observations offer a useful convergent comparison for the physical component of flood prioritisation. The Global Flood Database (GFD) maps large flood events from daily Moderate Resolution Imaging Spectroradiometer imagery for 2000–2018 (Tellman et al., 2021). It is neither a complete inventory of Indian floods nor a measure of mortality, vulnerability or total risk. It can nevertheless test whether districts ranked highly on physical-hazard information also experienced greater mapped inundation. A second form of evidence is retrospective out-of-time validation: predictors are frozen at a historical cutoff and evaluated against later observations. This design is more demanding than comparing variables accumulated over the same period, although it remains retrospective and should not be described as operational forecasting.

These comparisons are credible only if district linkage and reporting quality are explicit. Administrative boundaries change, district names recur, event records list multiple districts and historical impact fields are incomplete. Excluding unmatched districts can introduce geographic selection, while assigning a multi-district fatality total to individual districts can either omit deaths or duplicate them. These are not peripheral data-management details; they affect the meaning and stability of district rankings.

This study therefore treats DFSI as a case study in objective-specific validation rather than as an index to be invalidated or replaced. The primary question is whether published DFSI and transparent alternatives correspond with satellite-derived physical inundation. The secondary physical question is whether flood history recorded through 2010 prioritises districts with greater satellite-derived inundation in 2011–2018. A supplementary fatality analysis examines how a fitted model and simple historical baselines behave under alternative defensible district-allocation rules. Across all three components, the broader question is whether added complexity provides stable, decision-relevant information beyond transparent objective-specific indicators.

## 2. Data

### 2.1 DFSI and India Flood Inventory–Impacts data

The released India Flood Inventory–Impacts data contain the published DFSI table, district flooded-area data, district flood-impact data and the event-level India Flood Inventory. Version 4 is archived on Zenodo under DOI `10.5281/zenodo.16994648` (Saharia, 2025); the event inventory and its construction are described by Saharia et al. (2021). The event-level file covers 1967–2023 and contains 6,876 records. We used the fields `UEI`, `Start Date`, `End Date`, `Duration(Days)`, `Districts`, `State`, `Human fatality`, `Human injured`, `Event Source`, `District_LGD_Codes` and `State_Codes` as stored.

The verified DFSI baseline contained 720 one-to-one comparison records. Of these, 709 had complete values for flood-event count, mean flood duration, fatalities, injuries, corrected percentage flooded area and population; 11 incomplete records were retained separately and were not imputed. The published index was approximately, but not exactly, reproduced from released components. Let \(E\) denote flood events, \(D\) mean flood duration, \(F\) fatalities, \(I\) injuries, \(A\) corrected percentage flooded area and \(P\) population. The reproduced expression was

\[
\mathrm{DFSI}=\log_{10}(1+E)+\log_{10}(1+D)+2\log_{10}(1+F)+\log_{10}(1+I)+\log_{10}(1+A)+\log_{10}(P).
\]

Reconstructed DFSI was used as a reproducibility benchmark, not as a leakage-free temporal predictor.

### 2.2 Satellite-derived inundation and boundaries

Satellite observations came from `GLOBAL_FLOOD_DB/MODIS_EVENTS/V1` in Google Earth Engine (Gorelick et al., 2017). District geometries came from the geoBoundaries ADM2 collection `WM/geoLab/geoBoundaries/600/ADM2`, filtered to `shapeGroup == 'IND'` (Runfola et al., 2020). The boundary collection contained 735 Indian ADM2 geometries. The GFD bands used in processing had a nominal scale of 250 m.

Country metadata fields yielded no India events in the Earth Engine collection, so event selection was verified by spatial intersection with the union of Indian ADM2 geometries. This produced 192 India-related GFD images dated from 18 September 2000 to 1 September 2018. Event floodwater was defined as `flooded == 1`, with pixels where `jrc_perm_water == 1` removed. Non-flood pixels were masked. The district-event export retained a row only when non-permanent floodwater was detected inside the district; 148 events produced 16,402 such rows.

The primary physical outcome was cumulative inundation area-days per square kilometre:

\[
Y_{\mathrm{GFD}}=
\frac{\sum_{e,p} a_p d_{ep}\,\mathbf{1}(f_{ep}=1,\;w_{ep}\ne1)}{A_{\mathrm{district}}},
\]

where \(a_p\) is pixel area in km², \(d_{ep}\) is mapped inundation duration in days, \(f_{ep}\) is the GFD flooded band, \(w_{ep}\) is the permanent-water band and \(A_{\mathrm{district}}\) is geodesic boundary area in km². Geometry area was calculated in Earth Engine as `geometry().area(1) / 1e6`, and reductions used the 250 m native-scale setting, `maxPixels = 1e13` and `tileScale = 4`. Cumulative flooded-area-event fraction was retained as a secondary satellite outcome.

### 2.3 Historical reporting data

The event inventory was divided into 1967–1985, 1986–2004 and 2005–2023. These equal 19-year periods contained 762, 1,968 and 4,126 event records. Fatality-field completeness was 49.9%, 61.8% and 52.6%, while injury-field completeness was 14.2%, 17.8% and 14.5%. Duration was present for essentially all valid records. Changes in counts therefore reflect reporting and ascertainment as well as physical occurrence.

For the retrospective physical validation, raw events dated on or before 31 December 2010 supplied historical predictors, and GFD inundation during 2011–2018 supplied the later outcome. Fifty-three India-related GFD events fell in the later period, of which 49 produced detected non-permanent floodwater in matched districts.

## 3. Methods

### 3.1 Analytical hierarchy

The primary analysis compared flood-priority measures with satellite-derived physical inundation across matched districts. Reliability was assessed through an included-versus-excluded comparison, a stricter stable-match subset and leave-one-major-event-out diagnostics. The secondary physical analysis froze historical information at 31 December 2010 and evaluated later GFD inundation. District fatality prediction was retained as a sensitivity analysis because allocation and reporting limitations prevented the outcome from representing complete district mortality burden.

### 3.2 District linkage and exclusion rules

Text normalisation converted names to lower case, trimmed whitespace, replaced `&` with `and`, removed non-alphanumeric punctuation and collapsed repeated spaces. A prespecified dictionary handled 19 recognised spelling or renaming variants; the complete dictionary is reported in Supplementary Methods S1. District splits were never merged automatically, and fuzzy matches were suggestions for review only.

For event-inventory linkage, unique Local Government Directory (LGD) district codes took precedence. A code was accepted only if it mapped to one verified baseline district. Otherwise, an exact normalised state–district key was used; a district-only key was accepted only if unique nationally. Ambiguous, unmatched and blank locations were retained in audit tables and excluded from matched analyses. When district and LGD lists had different lengths, each list position was retained in the exploded event table, blank positions remained unresolved and no value was shifted to create a match. The raw inventory had no duplicates under the audited key `UEI + start date + end date + district + state`; no undocumented event deduplication was applied.

The GFD export did not contain a usable state attribute for matching. Boundary linkage therefore proceeded through one-to-one district-name keys: exact original name, exact normalised/standardised name, then an explicitly accepted manual crosswalk. Keys occurring more than once on either side and any duplicated boundary or DFSI identifier after combining stages were rejected as ambiguous. Fuzzy candidates were never automatically accepted.

Of 709 complete DFSI districts, 657 had accepted GFD/ADM2 matches and 52 (7.3%) lacked a unique defensible link. A strict stable-match subset required an accepted exact-original match plus globally unique normalised names in both universes, leaving 648 districts. Exclusions were compared with inclusions using distribution summaries, standardised mean differences and Mann–Whitney U tests as descriptive diagnostics; magnitude and geographic pattern, not p-values, guided interpretation.

### 3.3 Satellite benchmarks and reliability checks

The main transparent physical-hazard score was

\[
H_{\mathrm{equal}}=\frac{\log_{10}(1+E)+\log_{10}(1+D)+\log_{10}(1+A)}{3}.
\]

Published DFSI, reconstructed DFSI, an equal-weight six-component log score, population, event frequency, duration, flooded area and \(H_{\mathrm{equal}}\) were compared with \(Y_{\mathrm{GFD}}\). Spearman correlation was primary; Kendall correlation, top-decile overlap, Jaccard similarity and normalised discounted cumulative gain (NDCG) were supporting measures. Top groups used \(k=\lceil0.10n\rceil\), descending scores and deterministic state-then-district ordering for ties; ties were not expanded.

A learned physical-hazard score \(H_w=w_Ex_E+w_Dx_D+w_Ax_A\) was secondary. Candidate non-negative weights summing to one were exhaustively evaluated on a simplex grid with step 0.025, with exact equal weights added. Five grouped folds were formed by sorting state and union-territory units by descending district count after a seed-42 random tie key and greedily assigning each unit to the currently smallest fold. No unit appeared in both train and test data. The training candidate with highest Spearman correlation was selected; within 0.001 of that maximum, the vector closest to equal weights was preferred.

The strict stable-match analysis repeated the principal comparisons. Event influence was assessed by removing each of the five GFD events contributing the most national inundation area-days and recomputing published-DFSI and equal-hazard correlations. State-demeaned diagnostics subtracted each state/union-territory mean from both the index and satellite outcome before calculating a national residual correlation.

### 3.4 Retrospective out-of-time physical prioritisation validation

For each district, events dated through the 2010 cutoff were used to calculate past event count, mean duration, total duration, distinct flood years and recency. Credible zero-history districts remained in the administrative universe with zero event and duration summaries; years since the latest flood was set to the full predictor-window length when no event was present. The historical event-duration score was

\[
H_{ED}=\frac{\log_{10}(1+\text{past event count})+\log_{10}(1+\text{past mean duration})}{2}.
\]

The later outcome was cumulative GFD inundation area-days per km² during 2011–2018. Past GFD inundation through 2010 was also assessed as a persistence benchmark. The principal backtest and a 2005 cutoff sensitivity were repeated on the 648-district stable-match subset. This design is termed retrospective out-of-time physical prioritisation validation, not operational flood prediction.

### 3.5 Fatality-allocation sensitivity

Event records were exploded to their listed district/LGD positions. Under the conservative rule, fatalities and injuries were assigned only when a matched record had no more than one listed district and no more than one LGD code. Missing values remained missing in reporting-completeness calculations and contributed no assigned deaths. Zero therefore meant no assignable recorded death, not confirmed absence of death.

Under equal fractional allocation, a positive event fatality total was divided by the number of identifiable listed district positions. The share corresponding to a matched district was assigned once; unmatched, ambiguous, blank and state-only portions remained unassigned. The full total was never duplicated across districts. A state/union-territory analysis allocated multi-state event totals equally across identifiable listed states to reduce district-level ambiguity.

The primary fitted benchmark used eight predictor-period variables: \(\log(1+\text{event count})\), \(\log(1+\text{mean duration})\), \(\log(1+\text{total duration})\), \(\log(1+\text{past fatalities})\), \(\log(1+\text{past injuries})\), \(\log(1+\text{fatal-event count})\), \(\log(1+\text{distinct flood years})\) and \(1/(1+\text{years since recent flood})\). Means and population standard deviations were estimated only from the 1967–1985-to-1986–2004 development transition; zero standard deviations were replaced by one. Missing standardised predictor values were set to zero, corresponding to the development mean. The frozen transformation was applied to the 1986–2004-to-2005–2023 test.

The Poisson model minimised

\[
\frac{1}{n}\sum_i\{\exp(\eta_i)-y_i\eta_i\}+\frac{1}{2}\alpha\sum_j\beta_j^2,
\qquad \eta_i=\beta_0+x_i^T\beta,
\]

with \(\alpha=1\), an unpenalised intercept and L-BFGS-B optimisation (maximum 1,000 iterations). Linear predictors were clipped to [−20, 20] before exponentiation. Coefficients were initialised at zero and the intercept at \(\log(\max(\bar y,10^{-6}))\). Model settings were fixed from the development transition.

The higher-reporting-quality subset was defined independently of final model performance: at least one matched predictor-period event, fatality-field completeness of at least 50% in both 1986–2004 and 2005–2023, an accepted district match and no unresolved administrative ambiguity. Thresholds of 25% and 75% were prespecified sensitivity checks.

### 3.6 Resampling and reproducibility

Ordinary paired bootstrap intervals used 2,000 seed-42 district samples with replacement; competing methods were evaluated on identical resamples. State-block intervals sampled the observed set of state and union-territory labels with replacement, concatenated all districts in each selected block and retained duplicate block occurrences. Fixed \(k=\lceil0.10n\rceil\) was recalculated for each resample; row position provided deterministic tie-breaking inside resamples. Confidence limits were the 2.5th and 97.5th percentiles.

NDCG used linear observed-outcome gains: \(\mathrm{DCG}@k=\sum_{r=1}^k y_r/\log_2(r+1)\), divided by the ideal DCG at the same fixed \(k\). All analyses used Python 3.9.6, pandas 2.3.3, NumPy 2.0.2, SciPy 1.13.1 and Matplotlib 3.9.4. Raw and principal derived files were SHA-256 hashed before and after the reliability audit; all raw hashes were unchanged. Supplementary Methods and the repository reproduction checklist report file provenance, formulas, exclusions and exact execution order.

## 4. Results

### 4.1 Matching coverage and exclusion bias

The satellite comparison included 657 of 709 complete DFSI districts; 52 (7.3%) had no unique defensible ADM2 match. Excluded districts had lower median published DFSI (13.44 versus 14.17), lower median reconstructed DFSI (12.10 versus 13.01) and fewer median flood events (10.5 versus 24). Standardised mean differences were 0.33 for published DFSI, 0.41 for reconstructed DFSI and 0.63 for flood-event count. Corrected flooded-area percentage and population differed little (absolute standardised mean differences 0.05 and 0.11). Exclusion was therefore not random, although only 3 of the published top 71 districts were excluded.

Matching failure was geographically uneven. The largest numerical gaps were Telangana (11/33 excluded), West Bengal (7/22), Uttar Pradesh (6/72) and Karnataka (5/30). Ladakh had 1/2 excluded, but this percentage has a very small denominator. Full state/union-territory coverage and district-level reasons are reported in Supplementary Tables S1–S2.

### 4.2 Satellite-derived convergent validation

In the original 657-district sample, published DFSI had Spearman \(\rho=0.3575\) with cumulative inundation area-days per km² (95% ordinary bootstrap interval 0.2774–0.4300). Reconstructed DFSI had \(\rho=0.3721\) (0.2964–0.4441), and the equal-weight physical-hazard index had \(\rho=0.4529\) (0.3840–0.5200). The physical-hazard-minus-published-DFSI difference was 0.0954 (0.0436–0.1505). Their satellite top-decile overlaps were 43/66 and 25/66, respectively.

The strict stable-match subset produced the same conclusion. Among 648 districts, published DFSI had \(\rho=0.3606\) (0.2853–0.4336), reconstructed DFSI \(\rho=0.3773\) (0.3043–0.4492), flooded area \(\rho=0.3758\) (0.2999–0.4512), population \(\rho=0.3978\) (0.3217–0.4663) and the equal-weight physical-hazard index \(\rho=0.4595\) (0.3875–0.5253). The paired hazard-minus-published difference was 0.0989 (0.0435–0.1513). The hazard index identified 41 of the 65 satellite top-decile districts, compared with 25 for published DFSI.

The satellite outcome was concentrated but not dependent on a single mapped event. The largest event contributed 9.9% of national inundation area-days; the largest five contributed 36.8% and the largest ten 51.8%. Removing the five largest events one at a time left the hazard-minus-published-DFSI difference between 0.0948 and 0.0962. No single removal reversed the headline result (Supplementary Table S4).

Geographic diagnostics remained cautious. In the original matched sample, the learned hazard score had overall out-of-fold \(\rho=0.4874\), compared with 0.4529 for equal weights. Its held-out fold correlations ranged from 0.0992 to 0.6462. After state/union-territory demeaning, correlations were 0.0876 for the learned score, 0.1193 for the equal-weight hazard score and 0.0575 for published DFSI. National alignment therefore did not imply equally precise within-unit district ordering.

### 4.3 Retrospective out-of-time physical validation

On the strict stable-match subset, past event count through 2010 correlated with 2011–2018 GFD inundation at \(\rho=0.3031\), and the historical event-duration score at \(\rho=0.3759\). The score identified 35 of the later satellite top 65 districts, compared with 26 for event count. Their paired difference was 0.0728; its ordinary bootstrap interval was 0.0414–0.1033, while its state-block interval was −0.0047–0.1479. The national improvement was therefore positive under district resampling but geographically uncertain.

Past GFD inundation through 2010 was a much stronger persistence benchmark, with \(\rho=0.8882\), top-decile recall 54/65 and Jaccard similarity 0.7105. A 2005 cutoff sensitivity yielded the same qualitative pattern: the event-duration-minus-event-count difference was 0.0682, with an ordinary interval of 0.0368–0.0977 and a state-block interval of −0.0080–0.1321. These results support persistence in mapped physical inundation, not an operational prediction claim.

### 4.4 Fatality-allocation sensitivity

The 2005–2023 inventory contained 24,745 reported event-level fatalities. The conservative unique-district rule assigned 3,654 deaths. Equal fractional allocation assigned 17,705.9, leaving 7,039.1 unassigned because some listed locations remained unmatched, ambiguous, blank or non-district. The conservative and fractional district fatality rankings had Spearman \(\rho=0.6541\). Their median absolute rank difference was 116 positions, top-decile overlap was 37/72 and 74.4% of districts moved by more than 50 positions. District fatality prioritisation was therefore materially allocation-sensitive.

Under conservative allocation, the Poisson model had \(\rho=0.4614\), compared with 0.4930 for past event count. The observed difference was −0.0315, with ordinary interval −0.0637–0.0008 and state-block interval −0.0951–0.0301. Under fractional allocation, the Poisson model had \(\rho=0.7532\), compared with 0.7081 for event count. The difference changed sign to +0.0451, with ordinary interval 0.0228–0.0673 but state-block interval −0.0038–0.1014. Thus, the national comparison changed with allocation, and neither rule supported geographically robust model superiority.

Aggregation to 37 state and union-territory units reduced district-allocation ambiguity but did not support a complexity claim. The Poisson model had \(\rho=0.8301\), event count 0.8115 and past fatalities 0.8784. The Poisson-minus-event-count difference was 0.0186 (ordinary interval −0.0307–0.0696).

### 4.5 Reporting quality and higher-quality subset

The prespecified 50% higher-reporting-quality subset contained 388 districts. With conservative allocation, Poisson \(\rho=0.2155\) and event-count \(\rho=0.3170\); their paired ordinary interval was −0.1719 to −0.0296 and state-block interval −0.2563 to 0.0594. With fractional allocation, Poisson \(\rho=0.4982\) and event-count \(\rho=0.4742\); both ordinary (−0.0266–0.0692) and state-block (−0.0603–0.1132) intervals for the difference crossed zero. Restricting the data to more complete district histories did not restore robust model superiority.

Reporting-intensity diagnostics showed that final conservative assignable fatalities correlated with matched event-row count at \(\rho=0.6317\), distinct recorded flood years at 0.6101 and multi-district share at −0.5440. Predictor-period event count correlated with distinct recorded flood years at 0.7904 and matched event rows at 0.7626. These are diagnostic rather than causal associations, but they indicate that recorded district fatality rankings partly reflect ascertainment and administrative reporting structure.

## 5. Discussion

### 5.1 Objective-specific validation

The main result is that a ranking restricted to physical flood-history components aligned more closely with satellite-derived physical inundation than the mixed DFSI. This conclusion survived a stricter district-matching definition, exclusion-bias diagnostics and removal of each of the five largest contributing GFD events. Its interpretation is deliberately narrow. It neither invalidates DFSI nor establishes that the equal-weight hazard score is universally better. It shows that construct alignment matters: a score composed of event frequency, duration and flooded area corresponded more strongly with an outcome measuring mapped water extent and duration.

The published DFSI combines physical history, population as a proxy for exposure and recorded fatalities and injuries. These components can all be relevant to flood management, but their inclusion should not necessarily increase correlation with physical inundation. Population and human consequences describe different pathways through which floods matter. The stronger hazard-only result is therefore better understood as alignment with one particular outcome rather than a general verdict on a broad severity index.

### 5.2 Reliability of the physical comparison

The district-matching audit identifies a real but bounded selection concern. Excluded districts had lower event counts and somewhat lower DFSI values, and exclusions clustered in several state and union-territory units. It would be inappropriate to describe the 657-district sample as geographically neutral. At the same time, high-ranked districts were not disproportionately lost: only three of the published top 71 were excluded. Most importantly, the 648-district strict subset produced almost the same published-DFSI, hazard-index and paired-difference estimates. The conclusion is therefore not an artefact of weaker standardised-name or crosswalk matches.

GFD is also an incomplete satellite-observed sample. Large events and high-inundation districts contribute disproportionately to national totals, and 250 m MODIS observations can miss small, short or cloud-obscured floods. The leave-one-major-event-out results address only one part of this limitation. They show that the comparative ranking result is not driven by one extraordinary mapped event; they do not make GFD a complete record of physical flooding.

Geographic diagnostics further qualify the result. Positive national associations coexisted with weak state-demeaned correlations and wide fold-level variation. Broad regional contrasts therefore explain part of the national relationship. The physical-hazard ranking is useful as a national convergent-validity result, but it should not be interpreted as precise within-state ordering for operational allocation.

### 5.3 Retrospective physical persistence

The out-of-time physical analysis provides a second, temporally separated line of evidence. Historical event count and duration through 2010 contained modest information about mapped inundation in 2011–2018. Combining event count and duration improved the national correlation and top-decile recall relative to event count alone, but the paired improvement crossed zero when whole state and union-territory units were resampled. This again separates national signal from geographic transferability.

Earlier GFD inundation was by far the strongest later-inundation benchmark. This persistence result is physically interpretable: districts repeatedly inundated in the earlier satellite period tended to remain highly inundated later. It also has an important limitation because both predictor and outcome are generated by the same satellite product and related processing chain. We therefore use it as evidence of physical persistence, not as proof that a fitted or historical index can forecast future floods operationally.

### 5.4 Human-impact uncertainty

The fatality analysis illustrates why provenance and allocation rules can dominate district rankings. Under the conservative rule, most reported deaths were excluded from the district target because positive-fatality events frequently listed multiple districts without a verified within-event allocation. Equal fractional allocation recovered substantially more deaths without duplicating totals, but it introduced the assumption that listed districts share deaths equally. Neither rule can be treated as a complete district mortality measure.

The model comparison changed sign across these two defensible rules. Under conservative allocation, event count had the higher national correlation; under fractional allocation, the Poisson model did. The fractional model difference was positive under ordinary district bootstrap but crossed zero under state-block resampling. State-level aggregation likewise showed high correlations for several historical measures, with past fatalities exceeding the fitted model. These findings make a stable model-superiority claim untenable.

Reporting intensity compounds the allocation problem. Assignable fatalities were associated with how many event rows and distinct flood years were recorded, while multi-district reporting reduced assignability. These relationships do not prove that the model predicts reporting rather than mortality, but they show that the target contains both flood-impact and ascertainment structure. The secondary analysis should therefore be interpreted as a demonstration of sensitivity, not as validation of a national mortality-prediction model.

### 5.5 Complexity and transparent baselines

Across both physical and human-impact analyses, additional complexity had to earn its value against simple benchmarks. Equal physical-hazard weights performed close to a learned weighted score and avoided presenting geographically variable fitted weights as a new national index. In the retrospective physical test, the event-duration score improved nationally over event count but not robustly across geographic blocks. In the fatality test, the fitted Poisson model did not provide a stable advantage over event count across allocation rules, reporting subsets and state-level aggregation.

This does not imply that simple indicators are always sufficient. More complex models can represent multiple mechanisms, support scenario analysis or improve calibration even when rank correlation changes little. The practical point is narrower: when the output is a priority ranking, a model should be compared with a transparent objective-specific baseline under the same held-out design and uncertainty structure.

### 5.6 Practical and methodological implications

Flood-priority rankings should state what decision they support. Physical flood-management infrastructure, population exposure reduction, social-vulnerability intervention, emergency response and fatality prevention may require different evidence. A broad composite score remains useful as a summary, but its interpretation should not silently shift between these objectives.

The methodological contribution is an auditable sequence: define the target construct; preserve unmatched and ambiguous districts; quantify exclusion patterns; compare with transparent baselines; test stricter linkage; examine influential events; use out-of-time comparisons where possible; and propagate geographic dependence through block resampling. This workflow is more important than any single alternative score. No universal replacement index is proposed.

## 6. Limitations

GFD covers selected large events from 2000–2018 rather than every Indian flood. Its 250 m MODIS resolution, cloud and clear-view constraints, event-selection process and permanent-water mask limit detection. The GFD period partially overlaps the longer history informing DFSI, so the primary analysis is satellite-derived convergent validation rather than temporally independent validation.

Administrative vintages differ between DFSI records, the event inventory and geoBoundaries. Fifty-two complete DFSI districts lacked unique accepted matches, and exclusion was geographically uneven. The strict subset reduces but cannot eliminate uncertainty from district splits and historical boundary change. The GFD export lacked a usable state field, so accepted boundary links relied on globally unique district keys or reviewed crosswalks.

National satellite correlations were stronger than within-state residual relationships. Results should not be interpreted as precise district ordering within every state or union territory. The retrospective physical backtest shares measurement processes between earlier and later GFD persistence measures and is not an operational forecast.

Historical event volume and impact-field completeness changed through time. Injury reporting was sparse. Fatality totals in multi-district records could not be uniquely allocated, and alternative conservative and fractional rules materially changed district ranks. The original DFSI district-allocation procedure could not be verified from the released documentation; this absence of verification does not imply that the original procedure was incorrect. Many districts tied at zero assignable deaths under the conservative rule. Reporting-intensity associations further limit mortality interpretation.

All analyses are observational and rank-based. They do not identify causal effects, establish deployment readiness, validate a universal risk construct or support replacing DFSI with a single alternative national ranking.

## 7. Conclusion

The most defensible result is physical and objective-specific. A transparent equal-weight index of flood frequency, duration and flooded area aligned more strongly with satellite-derived inundation than the mixed DFSI. That difference persisted under strict district matching and after removing each of the five largest contributing satellite events. The finding should be interpreted as better alignment with mapped physical inundation, not as evidence that DFSI is invalid.

Retrospective out-of-time physical validation supplied supporting evidence: historical event-duration information through 2010 had modest association with inundation during 2011–2018, while earlier satellite inundation showed strong persistence. Geographic resampling nevertheless made the incremental improvement over event count uncertain.

District fatality prediction is a secondary sensitivity analysis. Fatality rankings changed materially between conservative and fractional allocation, and the fitted model did not robustly outperform transparent baselines across allocation and state-block checks. The analysis is most useful as evidence that district provenance, reporting structure and allocation assumptions must be made visible.

No universal replacement ranking is proposed. The central recommendation is methodological: validate flood-priority rankings against a clearly defined outcome, quantify district-linkage and reporting uncertainty, and require complexity to demonstrate added value over simple objective-specific indicators.

## 8. Data and Code Availability

IFI-Impacts Version 4 is available from Zenodo under DOI `10.5281/zenodo.16994648`. GFD is available through Google Earth Engine as `GLOBAL_FLOOD_DB/MODIS_EVENTS/V1`, and the geoBoundaries collection as `WM/geoLab/geoBoundaries/600/ADM2`. A repository-ready reproducibility package accompanies this revision. Public repository URL/archival DOI remains a final-submission checklist item and must be inserted before resubmission.

## 9. Author Contributions

Provisional CRediT roles:

- Conceptualisation: Abhijith Shaji, [co-author names to confirm]
- Methodology: Abhijith Shaji, [to confirm]
- Software: Abhijith Shaji
- Formal analysis: Abhijith Shaji
- Data curation: Abhijith Shaji
- Writing – original draft: Abhijith Shaji
- Writing – review and editing: [to confirm]
- Supervision: [to confirm]

## 10. Funding

Funding information: [TO BE CONFIRMED]

## 11. Competing Interests

The authors declare no competing interests. [AUTHOR CONFIRMATION REQUIRED]

## 12. Acknowledgements

[TO BE COMPLETED AFTER AUTHOR AND SUPERVISOR CONFIRMATION]

## 13. References

Aroca-Jiménez, E., Bodoque, J.M., García, J.A. and Figueroa-García, J.E. (2022) ‘Holistic characterization of flash flood vulnerability: Construction and validation of an integrated multidimensional vulnerability index’, *Journal of Hydrology*, 612, Part A, article 128083. doi:10.1016/j.jhydrol.2022.128083.

Bakkensen, L.A., Fox-Lent, C., Read, L.K. and Linkov, I. (2017) ‘Validating resilience and vulnerability indices in the context of natural disasters’, *Risk Analysis*, 37(5), pp. 982–1004. doi:10.1111/risa.12677.

Balica, S.F., Douben, N. and Wright, N.G. (2009) ‘Flood vulnerability indices at varying spatial scales’, *Water Science and Technology*, 60(10), pp. 2571–2580. doi:10.2166/wst.2009.183.

Balica, S.F. and Wright, N.G. (2010) ‘Reducing the complexity of the flood vulnerability index’, *Environmental Hazards*, 9(4), pp. 321–339. doi:10.3763/ehaz.2010.0043.

Balica, S.F., Wright, N.G. and van der Meulen, F. (2012) ‘A flood vulnerability index for coastal cities and its use in assessing climate change impacts’, *Natural Hazards*, 64(1), pp. 73–105. doi:10.1007/s11069-012-0234-1.

Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D. and Moore, R. (2017) ‘Google Earth Engine: Planetary-scale geospatial analysis for everyone’, *Remote Sensing of Environment*, 202, pp. 18–27. doi:10.1016/j.rse.2017.06.031.

Greco, S., Ishizaka, A., Tasiou, M. and Torrisi, G. (2019) ‘On the methodological framework of composite indices: A review of the issues of weighting, aggregation, and robustness’, *Social Indicators Research*, 141(1), pp. 61–94. doi:10.1007/s11205-017-1832-9.

Jha, R.K. and Gundimeda, H. (2019) ‘An integrated assessment of vulnerability to floods using composite index – A district level analysis for Bihar, India’, *International Journal of Disaster Risk Reduction*, 35, article 101074. doi:10.1016/j.ijdrr.2019.101074.

Kumar, D. and Bhattacharjya, R.K. (2020) ‘Estimation of integrated flood vulnerability index for the hilly region of Uttarakhand, India’, *Journal of Hazardous, Toxic, and Radioactive Waste*, 24(4), article 04020051. doi:10.1061/(ASCE)HZ.2153-5515.0000540.

Moreira, L.L., de Brito, M.M. and Kobiyama, M. (2021) ‘Review article: A systematic review and future prospects of flood vulnerability indices’, *Natural Hazards and Earth System Sciences*, 21(5), pp. 1513–1530. doi:10.5194/nhess-21-1513-2021.

OECD/European Union/EC-JRC (2008) *Handbook on constructing composite indicators: Methodology and user guide*. Paris: OECD Publishing. doi:10.1787/9789264043466-en.

Paruolo, P., Saisana, M. and Saltelli, A. (2013) ‘Ratings and rankings: Voodoo or science?’, *Journal of the Royal Statistical Society Series A: Statistics in Society*, 176(3), pp. 609–634. doi:10.1111/j.1467-985X.2012.01059.x.

Runfola, D., Anderson, A., Baier, H., Crittenden, M., Dowker, E., Fuhrig, S., Goodman, S., Grimsley, G., Layko, R., Melville, G., Mulder, M., Oberman, R., Panganiban, J., Peck, A., Seitz, L., Shea, S., Slevin, H., Youngerman, R. and Hobbs, L. (2020) ‘geoBoundaries: A global database of political administrative boundaries’, *PLOS ONE*, 15(4), article e0231866. doi:10.1371/journal.pone.0231866.

Saharia, M. (2025) *India Flood Inventory-Impacts (IFI-Impacts) [1967–2023]: A multi-source national geospatial database to facilitate comprehensive flood research*. Version v4. Zenodo. doi:10.5281/zenodo.16994648. Accessed 29 July 2026.

Saharia, M., Jain, A., Baishya, R.R., Haobam, S., Sreejith, O.P., Pai, D.S. and Rafieeinasab, A. (2021) ‘India flood inventory: creation of a multi-source national geospatial database to facilitate comprehensive flood research’, *Natural Hazards*, 108(1), pp. 619–633. doi:10.1007/s11069-021-04698-6.

Saharia, M., Jain, S.K., Prakash, V., Malik, H., Sreejith, O.P. and Joshi, D. (2025) ‘A district-level flood severity index for flood management in India’, *Natural Hazards*, 121(15), pp. 17815–17831. doi:10.1007/s11069-025-07493-9.

Saisana, M., Saltelli, A. and Tarantola, S. (2005) ‘Uncertainty and sensitivity analysis techniques as tools for the quality assessment of composite indicators’, *Journal of the Royal Statistical Society Series A: Statistics in Society*, 168(2), pp. 307–323. doi:10.1111/j.1467-985X.2005.00350.x.

Tellman, B., Schank, C., Schwarz, B., Howe, P.D. and de Sherbinin, A. (2020) ‘Using disaster outcomes to validate components of social vulnerability to floods: Flood deaths and property damage across the USA’, *Sustainability*, 12(15), article 6006. doi:10.3390/su12156006.

Tellman, B., Sullivan, J.A., Kuhn, C., Kettner, A.J., Doyle, C.S., Brakenridge, G.R., Erickson, T.A. and Slayback, D.A. (2021) ‘Satellite imaging reveals increased proportion of population exposed to floods’, *Nature*, 596(7870), pp. 80–86. doi:10.1038/s41586-021-03695-w.

