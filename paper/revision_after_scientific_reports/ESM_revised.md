# Electronic Supplementary Material

## Supplementary Methods S1. District-name normalisation and linkage

### S1.1 DFSI-to-geoBoundaries linkage

District text was converted to lower case, surrounding whitespace was stripped, `&` was replaced by `and`, non-alphanumeric runs were replaced by one space and repeated whitespace was collapsed. The following prespecified aliases were then applied:

| Source form | Normalised form |
|---|---|
| bangalore | bengaluru |
| bangalore rural | bengaluru rural |
| bangalore urban | bengaluru urban |
| belgaum | belagavi |
| bellary | ballari |
| bid | beed |
| bijapur | vijayapura |
| gulbarga | kalaburagi |
| mysore | mysuru |
| tumkur | tumakuru |
| cuddapah | ysr |
| puducherry | pondicherry |
| gurgaon | gurugram |
| mewat | nuh |
| ahmadabad | ahmedabad |
| medinipur west | paschim medinipur |
| medinipur east | purba medinipur |
| north twenty four pargan | north 24 parganas |
| south twenty four pargan | south 24 parganas |

The downloaded geoBoundaries export did not contain a usable state field. Matching was therefore district-name based, with non-unique names rejected. The hierarchy was: (1) unique exact original-name match; (2) unique exact normalised/standardised-name match among remaining boundaries; and (3) an explicitly accepted manual crosswalk. Fuzzy matches were recorded only as suggestions. After combining stages, any repeated boundary identifier or repeated DFSI identifier was reclassified as ambiguous. District splits were never automatically merged.

### S1.2 Event-inventory-to-baseline linkage

Semicolon/list fields for districts and LGD codes were split by their stored delimiters and retained by list position. Unique LGD codes took precedence. If no unique LGD match was available, an exact normalised state–district match was attempted, followed by district name alone only when unique nationally. A non-unique LGD code or district name was marked ambiguous. If district and code lists differed in length, missing positions remained blank; values were not shifted. The exploded table preserved unmatched and ambiguous rows. The inventory had zero duplicates under `UEI + Start Date + End Date + Districts + State`, so no source event was silently removed.

### S1.3 Stable-match definition

The primary satellite sample accepted all one-to-one original, standardised or reviewed manual matches. The strict subset required `match_method == exact_original`, unique normalised district names in both the DFSI and boundary universes, and no ambiguity flag. This yielded 648 of 657 accepted satellite records.

## Supplementary Methods S2. Satellite processing

The Earth Engine workflow used `GLOBAL_FLOOD_DB/MODIS_EVENTS/V1` and `WM/geoLab/geoBoundaries/600/ADM2`. Metadata filters tested `cc` for `IND` and `countries` for `India`; both returned zero events in the available collection. The analysis therefore used the union of metadata matches and images whose footprints spatially intersected the combined Indian ADM2 geometry, deduplicated by event `id`. Spatial intersection identified 192 images.

For event \(e\), floodwater was

\[
M_e=\mathbf{1}(\texttt{flooded}=1)\,\mathbf{1}(\texttt{jrc\_perm\_water}\ne1).
\]

`selfMask()` removed non-flood pixels. Flooded area was \(M_e\) multiplied by Earth Engine pixel area. Area-days were duration multiplied by the masked pixel area. District area was geodesic `geometry().area(1)/1e6`. Reductions used 250 m scale, `maxPixels=1e13` and `tileScale=4`. A district-event record was emitted only when detected non-permanent flooded area exceeded zero.

The primary outcome summed event pixel-area × duration and divided by district area. The secondary outcome summed event flooded area and divided by district area. The unique-pixel `ever_flooded_area` field was not used for validation.

## Supplementary Methods S3. Reporting-quality and fatality allocation

For each district and 19-year period, the audit separated observed event frequency, field completeness and administrative assignability. Completeness was the proportion of matched event rows with non-missing values; missing fatalities and injuries were not converted to reported zeros. Multi-district share was the proportion of matched rows originating from records listing more than one district.

Event frequency counted matched exploded event–district rows. Duration summaries used only non-missing durations; if a credible zero-history district had no matched duration observation, its event, total-duration, mean-duration and maximum-duration summaries were zero. Source diversity was the number of distinct non-missing `Event Source` values. Reporting-quality labels were not based on event count alone.

The conservative fatality target included reported fatalities only when an event row matched one baseline district and contained no more than one district and one LGD code. Under equal fractional allocation, event fatalities were divided by the number of identifiable listed district positions. Only matched shares were assigned; unresolved shares remained unassigned. State-level allocation similarly divided multi-state totals across identifiable listed states. No allocation duplicated an event total.

The primary higher-reporting-quality subset required at least one matched event in 1986–2004, fatality-field completeness ≥50% in both 1986–2004 and 2005–2023, accepted administrative matching and no unresolved ambiguity. Thresholds of 25% and 75% were sensitivity checks selected before examining their model comparisons.

## Supplementary Methods S4. Benchmarks, resampling and ties

- Equal-weight six-component score: mean of \(\log_{10}\)-transformed events, duration, fatalities, injuries, flooded area and population terms.
- Equal-weight physical-hazard score: mean of \(\log_{10}(1+E)\), \(\log_{10}(1+D)\) and \(\log_{10}(1+A)\).
- Learned physical-hazard score: non-negative simplex weights on these three terms, grid step 0.025; the most even vector within 0.001 Spearman of the training maximum was selected.
- Historical event-duration score: mean of \(\log_{10}(1+\text{past events})\) and \(\log_{10}(1+\text{past mean duration})\).
- Historical equal-weight hazard: mean of development-standardised \(\log(1+\text{events})\), \(\log(1+\text{mean duration})\) and \(\log(1+\text{distinct flood years})\).
- Historical persistence: mean of development-standardised \(\log(1+\text{past fatalities})\) and \(\log(1+\text{fatal-event count})\).
- Hazard-plus-population sensitivity: mean of development-standardised log event count, mean duration, distinct flood years and population.
- Secondary prespecified log-linear score: \(0.35\log(1+F)+0.20\log(1+E)+0.20\log(1+\text{total duration})+0.15\log(1+I)+0.10\log(1+\text{distinct years})\).

Zero-history districts remained in the 720-record panel with zero event/duration summaries and full-window recency. Predictor standardisation used development-period population means and standard deviations (`ddof=0`); zero standard deviations were replaced by one. The Poisson loss, clipping, initialisation, optimizer and penalty are specified in Main Methods 3.5.

Ranks were descending. Top-decile size was fixed at \(\lceil0.10n\rceil\); ties were ordered by state and district in analytical tables and by resampled row position in bootstraps. Ties were not expanded. Ordinary and state-block bootstraps used identical paired samples, 2,000 replicates, seed 42 and percentile intervals. Repeated sampled states were retained as repeated blocks. State-demeaned correlations used \(x_{is}-\bar x_s\) and \(y_{is}-\bar y_s\).

## Supplementary Table S1. Included versus excluded complete DFSI districts

| Variable | Included n | Excluded n | Included median (IQR) | Excluded median (IQR) | Standardised mean difference |
|---|---:|---:|---:|---:|---:|
| Published DFSI | 657 | 52 | 14.17 (4.21) | 13.44 (4.58) | 0.333 |
| Reconstructed DFSI | 657 | 52 | 13.01 (3.91) | 12.10 (4.40) | 0.411 |
| Published rank | 657 | 52 | 345 (356) | 406.5 (322) | −0.364 |
| Flood-event count | 657 | 52 | 24 (28) | 10.5 (26) | 0.629 |
| Mean flood duration | 657 | 52 | 7 (12) | 9 (10) | −0.233 |
| Fatalities | 657 | 52 | 52 (110) | 38.5 (72) | 0.229 |
| Injuries | 657 | 52 | 3 (10) | 1 (3.25) | 0.324 |
| Corrected flooded-area percentage | 657 | 52 | 1.254 (2.901) | 0.874 (2.298) | −0.047 |
| Population | 657 | 52 | 1,550,443 (1,851,093) | 1,241,602 (2,492,463) | −0.109 |

Mann–Whitney results are available in `included_vs_excluded_summary.csv` as descriptive evidence only. Three of the published top 71 DFSI districts were excluded.

## Supplementary Table S2. State/union-territory matching gaps

| Unit | Complete DFSI districts | Matched | Excluded | Match percentage |
|---|---:|---:|---:|---:|
| Ladakh | 2 | 1 | 1 | 50.0 |
| Telangana | 33 | 22 | 11 | 66.7 |
| West Bengal | 22 | 15 | 7 | 68.2 |
| Karnataka | 30 | 25 | 5 | 83.3 |
| Andhra Pradesh | 13 | 11 | 2 | 84.6 |
| Uttar Pradesh | 72 | 66 | 6 | 91.7 |

The complete 35-unit table and all 52 district-level exclusion records are provided as machine-readable audit files.

## Supplementary Table S3. Stable-match satellite validation (n = 648)

| Measure | Spearman ρ | 95% ordinary bootstrap CI | Top-decile overlap (of 65) | Jaccard |
|---|---:|---:|---:|---:|
| Published DFSI | 0.3606 | 0.2853–0.4336 | 25 | 0.2381 |
| Reconstructed DFSI | 0.3773 | 0.3043–0.4492 | 25 | 0.2381 |
| Equal-weight physical hazard | 0.4595 | 0.3875–0.5253 | 41 | 0.4607 |
| Flooded-area component | 0.3758 | 0.2999–0.4512 | 38 | 0.4130 |
| Population component | 0.3978 | 0.3217–0.4663 | 13 | 0.1111 |
| Hazard minus published DFSI | +0.0989 | 0.0435–0.1513 | +16 | — |

## Supplementary Table S4. Leave-one-major-GFD-event-out results

| Removed event ID | Event share of total | Published DFSI ρ | Equal hazard ρ | Difference |
|---|---:|---:|---:|---:|
| 2248 | 0.0992 | 0.3571 | 0.4520 | 0.0949 |
| 3136 | 0.0754 | 0.3593 | 0.4544 | 0.0951 |
| 3857 | 0.0714 | 0.3552 | 0.4514 | 0.0962 |
| 3128 | 0.0693 | 0.3577 | 0.4525 | 0.0948 |
| 3122 | 0.0523 | 0.3573 | 0.4527 | 0.0954 |

## Supplementary Table S5. Historical reporting completeness by period

| Period | Event records | Matched district-event rows | Matched districts | Raw reported fatalities | Conservative assignable fatalities | Fatality field complete | Injury field complete | Multi-district fatality rows excluded |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1967–1985 | 762 | 4,432 | 550 | 16,933 | 3,201 | 49.9% | 14.2% | 2,300 |
| 1986–2004 | 1,968 | 6,710 | 549 | 29,011 | 3,202 | 61.8% | 17.8% | 5,714 |
| 2005–2023 | 4,126 | 9,373 | 568 | 24,745 | 3,654 | 52.6% | 14.5% | 5,440 |

## Supplementary Table S6. Fatality allocation comparison, 2005–2023

| Quantity | Conservative | Equal fractional |
|---|---:|---:|
| Raw event-level reported fatalities | 24,745 | 24,745 |
| Assignable fatalities | 3,654 | 17,705.9 |
| Unassigned fatalities | 21,091 | 7,039.1 |
| District ranking agreement | Spearman ρ = 0.6541 | Spearman ρ = 0.6541 |
| Median absolute rank change | 116 positions | 116 positions |
| Top-decile overlap | 37/72 | 37/72 |
| Districts moving >50 ranks | 74.4% | 74.4% |

## Supplementary Table S7. Temporal benchmarks under two allocation rules

| Allocation | Method | Spearman ρ | Kendall τ | Top-decile recall | Jaccard | NDCG@10% |
|---|---|---:|---:|---:|---:|---:|
| Conservative | Poisson | 0.4614 | 0.3607 | 0.4306 | 0.2743 | 0.6884 |
| Conservative | Event count | 0.4930 | 0.3921 | 0.3889 | 0.2414 | 0.6805 |
| Conservative | Past fatalities | 0.3595 | 0.3114 | 0.3750 | 0.2308 | 0.4459 |
| Conservative | Equal historical hazard | 0.4626 | 0.3613 | 0.2639 | 0.1520 | 0.3110 |
| Fractional | Poisson | 0.7532 | 0.5767 | 0.5000 | 0.3333 | 0.5330 |
| Fractional | Event count | 0.7081 | 0.5426 | 0.5139 | 0.3458 | 0.3925 |
| Fractional | Past fatalities | 0.7785 | 0.6027 | 0.3750 | 0.2308 | 0.5155 |
| Fractional | Equal historical hazard | 0.7519 | 0.5690 | 0.3333 | 0.2000 | 0.2558 |

| Paired Poisson minus event count | Observed Δρ | Ordinary 95% CI | State-block 95% CI |
|---|---:|---:|---:|
| Conservative | −0.0315 | −0.0637–0.0008 | −0.0951–0.0301 |
| Equal fractional | +0.0451 | 0.0228–0.0673 | −0.0038–0.1014 |

## Supplementary Table S8. Higher-reporting-quality subset

| Allocation | n | Poisson ρ | Event-count ρ | Δρ | Ordinary 95% CI | State-block 95% CI | Poisson recall | Event-count recall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Conservative | 388 | 0.2155 | 0.3170 | −0.1015 | −0.1719–−0.0296 | −0.2563–0.0594 | 0.3846 | 0.4359 |
| Equal fractional | 388 | 0.4982 | 0.4742 | +0.0240 | −0.0266–0.0692 | −0.0603–0.1132 | 0.4359 | 0.4872 |

The 25% subset contained 489 districts and the 75% subset 197 districts. Complete threshold results are provided in `high_quality_subset_validation.csv`.

## Supplementary Table S9. State/union-territory fatality validation (n = 37)

| Method | Spearman ρ | Kendall τ | Top-decile recall | NDCG@10% |
|---|---:|---:|---:|---:|
| Poisson | 0.8301 | 0.6753 | 0.25 | 0.5260 |
| Event count | 0.8115 | 0.6367 | 0.25 | 0.5209 |
| Past fatalities | 0.8784 | 0.7150 | 0.50 | 0.4868 |
| Equal historical hazard | 0.8115 | 0.6479 | 0.25 | 0.3654 |
| Poisson minus event count | +0.0186 | — | 0.00 | 95% ordinary CI for Δρ: −0.0307–0.0696 |

## Supplementary Table S10. Retrospective physical validation on the stable subset

| Cutoff | Method | Spearman ρ | Top-decile recall | Jaccard | NDCG@10% |
|---|---|---:|---:|---:|---:|
| 2010 | Event count | 0.3031 | 0.4000 | 0.2500 | 0.3634 |
| 2010 | Event-duration score | 0.3759 | 0.5385 | 0.3684 | 0.5030 |
| 2010 | Past GFD persistence | 0.8882 | 0.8308 | 0.7105 | 0.8729 |
| 2005 | Event count | 0.3029 | 0.4615 | 0.3000 | 0.3919 |
| 2005 | Event-duration score | 0.3711 | 0.5538 | 0.3830 | 0.5449 |
| 2005 | Past GFD persistence | 0.8728 | 0.8308 | 0.7105 | 0.9645 |

| Cutoff | Event-duration minus event count Δρ | Ordinary 95% CI | State-block 95% CI |
|---|---:|---:|---:|
| 2010 | 0.0728 | 0.0414–0.1033 | −0.0047–0.1479 |
| 2005 | 0.0682 | 0.0368–0.0977 | −0.0080–0.1321 |

## Supplementary data files

Machine-readable district-level matching, reporting-quality, allocation, bootstrap and influence results are supplied in `outputs/editor_response_audit/`. The accompanying reproducibility package provides hashes, provenance, source-code locations and execution order.
