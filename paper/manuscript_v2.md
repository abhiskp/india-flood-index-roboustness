# Robust National Rankings, Uncertain Local Priorities:
A Sensitivity Audit of India's District Flood Severity Index

# Abstract

Structured abstract placeholder.

- **Background:** Placeholder.
- **Objective:** Placeholder.
- **Methods:** Placeholder.
- **Results:** Placeholder.
- **Conclusions:** Placeholder.

# 1. Introduction

- Motivate district-level historical flood-severity prioritisation in India.
- Introduce index-based prioritisation and the need for reproducible audits.
- Distinguish national ranking reproduction from local decision stability.
- State the study objective: evaluate robustness of district prioritisation under defensible methodological alternatives.

# 2. Data and Methods

## 2.1 Data sources

The analysis used the released DFSI and component datasets preserved in the project repository, including the published DFSI table, district-level flood-impact data, district-level flooded-area data and the India Flood Inventory. Raw files were treated as immutable inputs. The final verified baseline contained 720 one-to-one comparison records, of which 709 were complete and 11 were retained as incomplete without imputation.

The following source details are required before submission and are not recoverable from the current project files: dataset DOI/version/access date [SOURCE DETAIL REQUIRED]; population year/source [SOURCE DETAIL REQUIRED]; flooded-area temporal definition [SOURCE DETAIL REQUIRED]; administrative-boundary vintage [SOURCE DETAIL REQUIRED].

## 2.2 DFSI reproduction, harmonisation and joining

The published DFSI was approximately reproduced using the released component data and an algebraically equivalent additive log-space expression. The complete expression used for reconstruction was:

```text
DFSI = log10(1 + E) + log10(1 + D) + 2*log10(1 + F) + log10(1 + I) + log10(1 + A) + log10(P)
```

where `E` is flood-event count, `D` is mean flood duration, `F` is fatalities, `I` is injured people, `A` is corrected percent flooded area under the released units and `P` is population. This additive expression is algebraically equivalent to `log10((1 + E)(1 + D)(1 + F)^2(1 + I)(1 + A)P)`.

District harmonisation used audit-preserving review keys rather than silent correction of source names. The join audit documents the following steps: Step 1 joined District_FloodImpact.csv to District_FloodedArea.csv using district_review_key derived from Dist_Name; join type: inner for calculable one-to-one records; ambiguous and unmatched records audited separately; ambiguity policy: Keys appearing more than once on either side are excluded from the primary calculation and saved to dfsi_multiply_matched_records.csv. Step 2 joined Impact + FloodedArea one-to-one table to India_Flood_Inventory_v3.csv exploded event counts using district_review_key derived from district names; join type: left join; unmatched event counts audited separately; ambiguity policy: District names mapping to multiple LGD codes are reported as possible identifier ambiguity. Step 3 joined Calculated DFSI candidate table to DFSI.csv using district_review_key derived from District_FloodImpact.Dist_Name and DFSI.csv unnamed district column; join type: inner for comparison; unmatched and multiply matched records audited separately; ambiguity policy: Repeated published district names are excluded from the primary comparison unless the join is one-to-one. Official LGD identifiers were preferred where available in event parsing, but the final district-level joins could not be performed solely on LGD identifiers because the summary DFSI, impact and flooded-area source tables did not all contain compatible LGD state and district codes. One-to-one comparison records were defined as records with unique review-key matches across the component sources and the published DFSI table. Unmatched and multiply matched records were retained in audit outputs rather than forced into the baseline; 323 unmatched audit rows and 6 multiply matched audit rows were recorded separately. The resulting baseline contained 720 one-to-one records, with 709 complete records used for numerical comparisons and 11 incomplete records preserved without imputation.

The reconstructed index was compared with the published DFSI score rather than with the published rank. Ranks were ordered in descending DFSI, so rank 1 indicates the highest score. Exact numerical reproduction was not claimed.

## 2.3 Fatality-exponent sensitivity

The published index gives fatalities an exponent of 2. To evaluate sensitivity to this design choice, alternative indices used fatality exponents of 1.0, 1.5, 2.0, 2.5 and 3.0 while leaving all other component transformations unchanged. Each variant was compared with the correctly reconstructed exponent-2 baseline, not with the published DFSI, so that the experiment isolated the fatality-weighting choice.

## 2.4 Leave-one-component-out analysis

Six leave-one-component-out variants were constructed by removing one DFSI component at a time from the reconstructed baseline. The analysis recalculated district ranks after each removal and summarized rank correlation, median, 95th-percentile and maximum absolute rank change, top-group overlap and changes in top-10% membership. Component correlations and term contributions were interpreted as descriptive diagnostics rather than causal effects.

## 2.5 Monte Carlo weight uncertainty

Monte Carlo weight uncertainty was evaluated using unweighted log terms for flood-event frequency, mean duration, fatalities, injured people, flooded area and population. Weight vectors had previously been sampled from Dirichlet distributions centred on the published weight proportions. The concentration parameters 100, 30 and 10 are analyst-defined sensitivity scenarios and are not empirically calibrated uncertainty distributions. The moderate uncertainty scenario is treated as the primary analysis because it remains centred on the published weighting structure while permitting meaningful methodological variation.

Districts were categorized using Monte Carlo top-10% inclusion frequency, equivalently a simulation-based inclusion probability conditional on the specified Dirichlet weight distribution. Robust high-priority districts had inclusion frequency >= 0.80, weight-sensitive districts had inclusion frequency > 0.20 and < 0.80, and usually-outside districts had inclusion frequency <= 0.20. The 0.20 and 0.80 values are descriptive reporting thresholds, not universal policy standards.

## 2.6 Analytical priority-cutoff sensitivity

Analytical priority-cutoff sensitivity tested whether conclusions depended on selecting the top 10% as the priority group. The saved moderate-scenario Monte Carlo outputs were evaluated under fixed cutoffs of top 5%, top 10%, top 15%, top 20% and top 25%, corresponding to 36, 71, 106, 142 and 177 districts. The analysis reported robust membership, weight-sensitive membership and baseline priority districts with inclusion frequency below 0.80.

## 2.7 Evaluation metrics and reporting thresholds

The study reports Pearson correlation for numerical agreement and Spearman correlation for ranking agreement. Rank differences are absolute differences in descending ranks. Priority-group overlap is reported as both overlap share and Jaccard similarity. Monte Carlo inclusion categories use the descriptive thresholds 0.20 and 0.80.

## 2.8 Data limitations and historical reporting completeness

The India Flood Inventory was audited for historical reporting volume and completeness over the period 1967-2023. This audit is treated as a data-limitation and supplementary analysis rather than as a main historical trend result. Recorded event counts were treated as reporting volume and were not interpreted as physical flood-frequency trends. A complete period-specific DFSI could not be reconstructed from the event inventory alone because flooded-area percentage and population were not available as period-specific components and because historical reporting coverage was uneven.

# 3. Results

## 3.1 Reproduction of the published DFSI

The verified reproduction used 709 complete district records from 720 one-to-one baseline records, while preserving 11 incomplete records without imputation. The reconstructed DFSI ranged from 5.6728 to 17.9487, while the published DFSI among complete records ranged from 4.2445 to 19.3006. The reconstructed index strongly reproduced the published ranking, with Spearman correlation 0.95885 and Pearson correlation 0.95872. However, exact numerical reproduction was not achieved: the median absolute numerical difference was 1.20677, the median absolute rank difference was 18 positions and the maximum absolute rank difference was 345 positions.

Additional agreement diagnostics showed a mean signed error of -1.11527, a median signed error of -1.18572 and RMSE of 1.37687. An ordinary least-squares fit of reconstructed DFSI as a function of published DFSI had slope 0.88550 and intercept 0.44187. Published-versus-reconstructed overlap shares were 76.0% for the top 25, 82.0% for the top 50, 83.1% for the top 10% and 89.0% for the top 100.

## 3.2 Component and leave-one-out sensitivity

Leave-one-component-out analysis showed that removing fatalities produced the largest median absolute rank change, 37 positions, and a maximum absolute rank change of 383 positions. Removing injured people produced the largest top-10% membership turnover, with 19 districts entering and 19 leaving the group. The minimum leave-one-out Spearman correlation was 0.945272, observed when fatalities were removed. Thus, high national rank correlation can coexist with substantial district-level movement.

Fatality-exponent sensitivity produced high rank correlations with the reconstructed exponent-2 baseline, but individual district movements remained nontrivial. Reducing the exponent to 1.0 gave Spearman correlation 0.9925, median absolute rank change 12, maximum rank change 163 and top-10% overlap 63 of 71 districts.

## 3.3 Monte Carlo uncertainty in district prioritisation

In the primary moderate uncertainty scenario, 10000 saved Monte Carlo weight vectors were evaluated for 709 complete districts. The median Spearman correlation with the baseline ranking was 0.9878, but top-priority membership remained sensitive. Conditional on the specified moderate Dirichlet weight distribution, the scenario identified 43 robust high-priority districts, 56 weight-sensitive districts and 610 usually-outside districts. Among baseline top-10% districts, 28 had less than 0.80 Monte Carlo top-10% inclusion frequency. Thus, national ranking stability did not guarantee district-level decision stability.

## 3.4 Sensitivity to the analytical priority cutoff

Priority instability persisted across all five analytical priority thresholds examined. The proportion of baseline priority districts classified as robust was 58.3% for the top 5%, 60.6% for the top 10%, 74.5% for the top 15%, 81.7% for the top 20% and 83.6% for the top 25%. The largest number of weight-sensitive districts was 56, observed under the top-10%, top-15%, top-20% and top-25% thresholds. These results indicate that the central conclusion does not depend on using the top-10% threshold.

# 4. Discussion

- Interpret strong national rank reproduction alongside non-exact numerical reproduction.
- Discuss why decisions based on priority-group membership require more than rank correlation.
- Discuss component-weight uncertainty as a transparent robustness problem.
- Discuss implications for district prioritisation and communication of uncertainty.
- Discuss limitations of static population/flooded-area components and historical reporting completeness.

# 5. Conclusion

- The released datasets approximately reproduce the published DFSI ranking.
- District-level priority membership is sensitive to reasonable methodological alternatives.
- Robust prioritisation should report inclusion frequencies and analytical cutoff sensitivity, not only national rank correlations.
- Temporal claims require explicit reporting-completeness caveats.

# Data and Code Availability

Placeholder. Data and analysis code availability statement to be completed after repository and dataset citation details are finalized.

# References

- Original DFSI paper placeholder.
- Zenodo dataset placeholder.
