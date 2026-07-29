## Day 1 — Verified DFSI reproduction

### Baseline construction

- Total one-to-one baseline records: 720
- Complete comparison records used for reproduction: 709
- Incomplete records preserved without imputation: 11
- Reconstructed DFSI range: 5.6728–17.9487
- Spearman correlation with published DFSI: 0.95885
- Pearson correlation with published DFSI: 0.95872
- Median absolute numerical difference: 1.20677
- Median absolute rank difference: 18
- Maximum absolute rank difference: 345

### Ranking reproduction

- Top 10% overlap: 59 of 71 districts
- Top 25 overlap: 19 of 25 districts
- Top 50 overlap: 41 of 50 districts
- Top 100 overlap: 89 of 100 districts
- Districts moving more than 10 positions: 475
- Districts moving more than 25 positions: 271
- Districts moving more than 50 positions: 158

### Interpretation

The released component datasets strongly reproduce the overall published DFSI
ranking, with a Spearman correlation of 0.95885. However, the reproduction is
not numerically exact, and substantial district-level rank differences remain.
This supports proceeding with a robustness analysis focused on whether flood-
priority decisions remain stable under defensible methodological alternatives.

The 11 incomplete records were retained and were not imputed.

Earlier negative DFSI values resulted from an implementation error involving
subtraction between logarithmic terms. The corrected calculation adds all six
logarithmic component contributions and agrees with an independently calculated
multiplicative product expression. The erroneous results are excluded from all
scientific analyses and reported findings.

## Day 1 — Fatality-weight sensitivity pilot

The published DFSI gives fatalities an exponent of 2. Alternative exponents
were compared against the reconstructed exponent-2 baseline using 709 complete
district records.

- Exponent 1.0:
  - Spearman correlation: 0.9925
  - Median absolute rank change: 12
  - Maximum rank change: 163
  - Top 10% overlap: 63 of 71

- Exponent 1.5:
  - Spearman correlation: 0.9985
  - Median absolute rank change: 5
  - Maximum rank change: 72
  - Top 10% overlap: 67 of 71

- Exponent 2.5:
  - Spearman correlation: 0.9990
  - Median absolute rank change: 5
  - Maximum rank change: 46
  - Top 10% overlap: 70 of 71

- Exponent 3.0:
  - Spearman correlation: 0.9970
  - Median absolute rank change: 8
  - Maximum rank change: 78
  - Top 10% overlap: 66 of 71

### Preliminary interpretation

Overall rank correlations remain high under alternative fatality exponents.
However, high correlations conceal meaningful changes for individual districts.
Reducing the fatality exponent from 2 to 1 moves some districts by as many as
163 positions and changes 8 members of the top-10% priority group.

This indicates that the fatalities weighting has limited influence on the
overall national ordering but can materially affect individual district
prioritisation.

## Day 1 — Component influence analysis

The six DFSI components were evaluated using 709 complete district records.

### Numerical contribution

The largest median contributions to reconstructed DFSI were:

- Population: 47.8%
- Fatalities: 26.1%
- Flood-event frequency: 10.7%

Population therefore dominates the numerical magnitude of the index, although
numerical contribution should not be interpreted as causal importance.

### Leave-one-component-out sensitivity

Removing fatalities caused the greatest overall ranking instability:

- Median absolute rank change: 37 positions
- Maximum absolute rank change: 383 positions

Removing injured people caused the largest change in the top-10% priority
group:

- 19 districts entered the top 10%
- 19 districts left the top 10%

All six leave-one-component-out variants retained Spearman correlations above
0.94 with the complete baseline. However, several variants still moved
individual districts by more than 50 positions.

### Preliminary interpretation

High national rank correlations conceal substantial district-level
instability. A component can have a relatively modest numerical contribution
while materially determining which districts enter or leave the priority
group.

The Monte Carlo uncertainty analysis should therefore allow the greatest
weight variation for fatalities, injured people and population, while retaining
all six components.

## Day 1 — Monte Carlo weight uncertainty

Thirty thousand alternative weight vectors were simulated across narrow,
moderate and wide uncertainty scenarios using 709 complete district records.

The moderate uncertainty scenario was selected as the primary analysis because
it remains centred on the published DFSI weighting structure while permitting
meaningful methodological variation.

### Main results

- Median Spearman correlation with baseline ranking: 0.9878
- Robust high-priority districts: 43
- Weight-sensitive priority districts: 56
- Baseline top-10% districts with less than 80% probability of remaining in
  the top 10%: 28

The districts with the widest rank uncertainty included:

- Upper Siang
- Rudraprayag
- West Siang
- East Siang
- Uttarkashi
- Bangalore
- Darjiling
- Bid
- Kinnaur
- Medinipur West

### Interpretation

Although simulated national rankings remain highly correlated with the
baseline, district-level priority decisions are materially sensitive to
reasonable alternative component weights.

Only 43 districts are robustly classified as high priority under the moderate
scenario. Fifty-six districts have top-10% membership probabilities between
0.20 and 0.80 and are therefore described as weight-sensitive priorities.

The 0.20 and 0.80 thresholds are analytical reporting thresholds and are not
presented as universal policy standards.

This analysis demonstrates that rank correlation alone is insufficient for
evaluating the robustness of a flood-prioritisation index. Decision-relevant
stability must also be evaluated through priority-group membership and
district-level rank uncertainty.

## Day 1 — Historical reporting-completeness audit

The India Flood Inventory was audited for the period 1967–2023.

### Main findings

- Recorded flood-event volume changes substantially through time.
- Reporting completeness also changes substantially through time.
- The equal-length historical windows 1967–1985, 1986–2004 and 2005–2023
  are not fully comparable for direct flood-risk trend claims.
- Missingness and coverage vary across event duration, fatalities, injuries,
  district identification and spatial coordinates.
- Missing impact values were not treated as reported zeros.

### Temporal feasibility

A complete period-specific DFSI cannot be reconstructed from the event
inventory alone because:

- corrected flooded-area percentage is not available by historical period;
- population is not available as a period-specific component;
- historical administrative and reporting coverage are uneven;
- impact-variable completeness changes through time.

An event-derived temporal sensitivity analysis may be technically possible,
but it would require strong reporting-completeness caveats and would not be
equivalent to the published DFSI.

### Research decision

The paper will not interpret changes in recorded flood events as direct changes
in physical flood frequency or district flood risk.

The main contribution will remain the robustness of district prioritisation
under alternative component weights, supported by a historical
reporting-completeness audit that demonstrates the limitations of temporal
index interpretation.

## Day 1 — Priority-cutoff sensitivity

The moderate Monte Carlo scenario was evaluated under five alternative
priority thresholds using 709 complete district records:

- Top 5%: 36 districts
- Top 10%: 71 districts
- Top 15%: 106 districts
- Top 20%: 142 districts
- Top 25%: 177 districts

### Robustness of baseline priority membership

- Top 5%: 58.3% of baseline priority districts were robust
- Top 10%: 60.6%
- Top 15%: 74.5%
- Top 20%: 81.7%
- Top 25%: 83.6%

Priority instability persisted across all five thresholds.

The largest number of weight-sensitive districts was 56, observed under the
top-10%, top-15%, top-20% and top-25% thresholds.

Uncertainty was not confined to districts immediately beside the priority
cutoff. Sensitive district-cutoff cases were identified more than 25 baseline
rank positions from the threshold.

### Interpretation

The paper's central conclusion does not depend on selecting the top 10% as the
policy-priority group.

Broader priority groups are more stable than highly selective groups, but
reasonable component-weight uncertainty continues to alter district
prioritisation under every threshold examined.

The results distinguish ordinary cutoff-boundary uncertainty from broader
structural sensitivity caused by the index weighting design.

## End of exploratory analysis

The primary empirical analysis is now frozen.

The final paper will use:

1. Verified DFSI reproduction
2. Fatality-exponent sensitivity
3. Leave-one-component-out analysis
4. Monte Carlo weight uncertainty
5. Priority-cutoff sensitivity
6. Historical reporting-completeness audit

No additional exploratory notebooks should be created unless required to
resolve a documented methodological issue.
