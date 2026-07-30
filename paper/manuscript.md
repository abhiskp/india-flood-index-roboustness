# Robust National Rankings, Uncertain Local Priorities:
A Sensitivity Audit of India’s District Flood Severity Index

# Abstract

Structured abstract placeholder.

- **Background:** Placeholder.
- **Objective:** Placeholder.
- **Methods:** Placeholder.
- **Results:** Placeholder.
- **Conclusions:** Placeholder.

# 1. Introduction

- Motivate district-level flood-risk prioritisation in India.
- Introduce index-based prioritisation and the need for reproducible audits.
- Distinguish national ranking reproduction from local decision stability.
- State the study objective: evaluate robustness of district prioritisation under defensible methodological alternatives.

# 2. Data and Methods

## 2.1 Data sources

The analysis used the released DFSI and component datasets preserved in the project repository, including the published DFSI table, district-level flood-impact data, district-level flooded-area data and the India Flood Inventory. Raw files were treated as immutable inputs. Processed comparison records and audit outputs from the verified reproduction workflow were used for consolidation. The final verified baseline contained 720 one-to-one comparison records, of which 709 were complete and 11 were retained as incomplete without imputation (Claims R01-R03).

## 2.2 DFSI reproduction

The published DFSI was approximately reproduced using the released component data and the corrected additive log-space expression. The reconstructed index was compared with the published DFSI score rather than with the published rank. Ranks were ordered in descending DFSI, so rank 1 indicates the highest score. Reproduction was evaluated using Pearson correlation, Spearman rank correlation, absolute numerical differences, absolute rank differences and overlap of published and reconstructed high-priority groups. Exact numerical reproduction was not claimed.

## 2.3 Fatality-exponent sensitivity

The published index gives fatalities an exponent of 2. To evaluate sensitivity to this design choice, alternative indices were calculated using fatality exponents of 1.0, 1.5, 2.0, 2.5 and 3.0 while leaving all other component transformations unchanged. Each variant was compared with the correctly reconstructed exponent-2 baseline, not with the published DFSI, so that the experiment isolated the fatality-weighting choice.

## 2.4 Leave-one-component-out analysis

Six leave-one-component-out variants were constructed by removing one DFSI component at a time from the reconstructed baseline. The analysis recalculated district ranks after each removal and summarized rank correlation, median and maximum absolute rank change, top-group overlap and changes in top-10% membership. Component correlations and term contributions were interpreted as descriptive diagnostics rather than causal effects.

## 2.5 Monte Carlo weight uncertainty

Monte Carlo weight uncertainty was evaluated using unweighted log terms for flood-event frequency, mean duration, fatalities, injured people, flooded area and population. Weight vectors were sampled in prior verified analysis from Dirichlet distributions centred on the published weight proportions. The present manuscript treats the moderate uncertainty scenario as the primary analysis because it remains centred on the published weighting structure while permitting meaningful methodological variation (Claims MC01-MC02). Districts were categorized using top-10% membership probabilities: robust high-priority districts had probability >= 0.80, weight-sensitive districts had probability > 0.20 and < 0.80, and usually-outside districts had probability <= 0.20. The 0.20 and 0.80 values are descriptive reporting thresholds, not universal policy standards.

## 2.6 Priority-cutoff sensitivity

Priority-cutoff sensitivity tested whether conclusions depended on selecting the top 10% as the policy-priority group. The saved moderate-scenario Monte Carlo outputs were evaluated under fixed cutoffs of top 5%, top 10%, top 15%, top 20% and top 25%, corresponding to 36, 71, 106, 142 and 177 districts (Claims P_top_5pct_count-P_top_25pct_count). The analysis reported robust membership, weight-sensitive membership and baseline priority districts with membership probability below 0.80.

## 2.7 Historical reporting-completeness audit

The India Flood Inventory was audited for historical reporting volume and completeness over the period 1967-2023 (Claims T01-T02). The audit evaluated whether temporal DFSI sensitivity analysis could be conducted without confusing changing reporting completeness with changing flood risk. Recorded event counts were treated as reporting volume and were not interpreted as physical flood-frequency trends.

## 2.8 Evaluation metrics and reporting thresholds

The study reports Pearson correlation for numerical agreement and Spearman correlation for ranking agreement. Rank differences are absolute differences in descending ranks. Priority-group overlap is reported as the number of districts common to two high-priority sets. Monte Carlo priority categories use the descriptive thresholds 0.20 and 0.80. These thresholds support transparent reporting but are not proposed as universal policy standards.

# 3. Results

## 3.1 Reproduction of the published DFSI

The verified reproduction used 709 complete district records from 720 one-to-one baseline records, while preserving 11 incomplete records without imputation (Claims R01-R03). The reconstructed DFSI ranged from 5.6728 to 17.9487, while the published DFSI among complete records ranged from 4.2445 to 19.3006 (Claims R09-R12). The reconstructed index strongly reproduced the published ranking, with Spearman correlation 0.95885 and Pearson correlation 0.95872 (Claims R04-R05). However, exact numerical reproduction was not achieved: the median absolute numerical difference was 1.20677, the median absolute rank difference was 18 positions and the maximum absolute rank difference was 345 positions (Claims R06-R08). Published-versus-reconstructed overlap was 19 of 25 districts, 41 of 50, 59 of 71 and 89 of 100 (Claims R13-R16).

## 3.2 Component influence and leave-one-out sensitivity

The largest median numerical contribution came from population (47.8%), followed by fatalities (26.1%) and flood-event frequency (10.7%) (Claims C01-C06). These values describe the arithmetic composition of the reconstructed score and should not be interpreted as causal importance. Leave-one-component-out analysis showed that removing fatalities produced a median absolute rank change of 37 positions and a maximum absolute rank change of 383 positions (Claims L01-L02). Removing injured people produced the largest top-10% membership turnover, with 19 districts entering and 19 leaving the group (Claims L03-L04). All leave-one-component-out variants retained Spearman correlations above 0.95, indicating that high national rank correlation can coexist with substantial district-level movement (Claim L05).

Fatality-exponent sensitivity produced high rank correlations with the reconstructed exponent-2 baseline, but individual district movements remained nontrivial. Reducing the exponent to 1.0 gave Spearman correlation 0.9925, median absolute rank change 12, maximum rank change 163 and top-10% overlap 63 of 71 districts (Claims F1_0_rho-F1_0_top10).

## 3.3 Monte Carlo uncertainty in district prioritisation

In the primary moderate uncertainty scenario, 10000 saved Monte Carlo weight vectors were evaluated for 709 complete districts (Claims MC01-MC02). The median Spearman correlation with the baseline ranking was 0.9878, but top-priority membership remained sensitive (Claim MC_moderate_rho). The scenario identified 43 robust high-priority districts, 56 weight-sensitive districts and 610 usually-outside districts (Claims MC_moderate_robust, MC_moderate_sensitive and MC04). Among baseline top-10% districts, 28 had less than 0.80 probability of remaining in the top 10% (Claim MC03). Thus, national ranking stability did not guarantee district-level decision stability.

## 3.4 Sensitivity to the policy-priority cutoff

Priority instability persisted across all five priority thresholds examined (Claim P02). The proportion of baseline priority districts classified as robust was 58.3% for the top 5%, 60.6% for the top 10%, 74.5% for the top 15%, 81.7% for the top 20% and 83.6% for the top 25% (Claims P_top_5pct_robust_share-P_top_25pct_robust_share). The largest number of weight-sensitive districts was 56, observed under the top-10%, top-15%, top-20% and top-25% thresholds (Claim P01). These results indicate that the central conclusion does not depend on using the top-10% threshold.

## 3.5 Limitations of temporal comparison

The reporting-completeness audit found that recorded flood-event volume changed substantially over time and that reporting completeness also changed substantially (Claims T03-T04). A complete period-specific DFSI could not be reconstructed from the event inventory alone (Claim T05), because flooded-area percentage and population were not available as period-specific components and because historical reporting coverage was uneven. Event-derived temporal sensitivity analysis may be technically possible with caveats (Claim T06), but it would not be equivalent to the published DFSI and should not be interpreted as a direct trend in physical flood risk.

# 4. Discussion

- Interpret strong national rank reproduction alongside non-exact numerical reproduction.
- Discuss why policy decisions based on top-priority membership require more than rank correlation.
- Discuss component-weight uncertainty as a transparent robustness problem.
- Discuss implications for district prioritisation and communication of uncertainty.
- Discuss limitations of static population/flooded-area components and historical reporting completeness.

# 5. Conclusion

- The released datasets approximately reproduce the published DFSI ranking.
- District-level priority membership is sensitive to reasonable methodological alternatives.
- Robust prioritisation should report priority probabilities and cutoff sensitivity, not only national rank correlations.
- Temporal claims require explicit reporting-completeness caveats.

# Data and Code Availability

Placeholder. Data and analysis code availability statement to be completed after repository and dataset citation details are finalized.

# References

- Original DFSI paper placeholder.
- Zenodo dataset placeholder.
