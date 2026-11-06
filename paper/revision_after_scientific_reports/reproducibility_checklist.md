# Reproducibility Checklist

## A. Former method-reporting gaps

| Item | Previous status | Revision location | Current status |
|---|---|---|---|
| District-name normalisation | Partial | Main Methods 3.2; ESM S1.1 | Closed |
| LGD-code precedence and exact-name fallback | Partial | Main Methods 3.2; ESM S1.2 | Closed |
| Duplicate and repeated-name handling | Partial | Main Methods 3.2; ESM S1.1–S1.2 | Closed |
| GFD metadata versus spatial event inclusion | Partial | Data 2.2; ESM S2 | Closed |
| District-area calculation and projection settings | Partial | Data 2.2; ESM S2 | Closed |
| Zero-history district handling and event deduplication | Partial | Methods 3.4; ESM S4 | Closed |
| Missing duration, fatality and injury handling | Partial | Methods 3.2, 3.5; ESM S3 | Closed |
| Multi-district event explosion and mismatched lists | Partial | Methods 3.2, 3.5; ESM S1.2 | Closed |
| Predictor standardisation and zero variance | Partial | Methods 3.5 | Closed |
| Poisson objective, clipping and optimizer | Partial | Methods 3.5 | Closed |
| L2 penalty and intercept treatment | Partial | Methods 3.5 | Closed |
| Grouped-fold balancing and membership logic | Partial | Methods 3.3 | Closed |
| Learned-weight 0.025 grid and near-tie rule | Partial | Methods 3.3; ESM S4 | Closed |
| State-demeaning, bootstrap blocks and resample tie handling | Absent/partial | Methods 3.3, 3.6; ESM S4 | Closed |

All 14 gaps identified by the reliability audit are now described from recoverable code. No implementation detail was guessed.

## B. Data integrity and provenance

- [x] Raw files were not modified during the audit.
- [x] SHA-256 hashes are recorded for four raw files and principal derived inputs.
- [x] IFI-Impacts DOI and access date are recorded.
- [x] GFD collection identifier is recorded.
- [x] geoBoundaries collection identifier is recorded.
- [x] District crosswalk and exclusion reasons are included.
- [x] Final satellite, retrospective and fatality sensitivity tables are included.
- [x] Random seed 42 and 2,000-bootstrap design are documented.
- [x] Software versions recoverable from notebook execution metadata are documented.
- [ ] GFD export date was not recorded in the original workflow; do not invent it.
- [ ] Separate source/access dates for the three released DFSI component CSVs are not documented beyond their dataset context.
- [ ] Population reference year/source remains undocumented in released project files; population is not used in the primary temporal model.
- [ ] Original DFSI event-to-district fatality allocation procedure remains unverifiable from released documentation.

## C. Before resubmission elsewhere

- [ ] Insert a stable public repository URL.
- [ ] Create an archival release and DOI if required by the target journal.
- [ ] Confirm author list, affiliations and corresponding author.
- [ ] Confirm CRediT contributions, funding and competing-interests declaration.
- [ ] Apply target-journal word, reference and figure requirements.
- [ ] Have the revised methods and ESM checked independently against code.
- [ ] Confirm that all machine-readable supplemental files will be deposited.

## D. Scientific readiness

The revised analytical framing is suitable for professor/co-author review. It is not yet submission-ready because external archive metadata and author/journal details remain unresolved.
