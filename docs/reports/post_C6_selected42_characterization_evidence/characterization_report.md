# Fixed accepted 42: descriptive characterization against the verified 619

ARTIFACT_CLASS = NEW_CHARACTERIZATION_OUTPUT

TASK_STATUS = COMPLETE__DESCRIPTIVE_CHARACTERIZATION_COMPLETE

Execution date: 2026-09-20. The bounded characterization is complete and independently checked by a separate arithmetic implementation. This is technical validation by the same executor; Managing/Admin scientific review remains separate. Membership remains SELECTED__UNFROZEN. No freeze suitability or governance breadth classification is assigned.

## Verified scope and identity

- Canonical `main` read-only verification: `9f61e40aeea71a722f9328ff09495cd20002b811`; matches the Admin pin.
- Controlling protocol: [EVID_POSTC6_SELECTED42_CHARACTERIZATION_PROTOCOL_001](https://github.com/racoope70/quantitative-trading-research-platform/blob/9f61e40aeea71a722f9328ff09495cd20002b811/docs/workflows/milestone_review_reference_map.md#L1232).
- Fixed membership SHA-256: `43a42ddf4e4ac40730be7457904be588f4cf26bc333650a301090c925097041f`.
- Verified 619 reference SHA-256: `aed6f9e137b52948ebd4c2385c84b5a2b39e2ddd8c7be90fe1f30fa8415cb7c7`.
- Accepted 619 input SHA-256: `46d8b36e43e5a70193e7fd6d273ff6672b21c37b4dc1932a7b643bd27aec8821`.
- Accepted V3 SIC bridge SHA-256: `5de90b0ac567a1e488dce54b319e242939f6c139517be04423c32a4f3486c091`.
- Exactly 42 unique securities and 42 issuers; all 42 are in the verified 619. No reselection was performed.
- All 619 required sector, exchange-family and liquidity values are complete; no required subject or reference values are missing.
- Formation: 2024-09-03 regular-session open. Information cutoff: completed 2024-08-30 regular session.

## Protocol reconciliation and authority

PROTOCOL_CONFLICT = NONE. The current 42-member registry explicitly supersedes prior three-security subject-specific rules. Its accepted reference is the available 619 pool, with incompleteness disclosed. The old three-security membership, completeness/freeze prerequisites and subject-specific restrictions are historical context and were not substituted for the current protocol. The current Owner handoff grants characterization execution authority; the older repository statements withholding that authority are not an unresolved contradiction. All freeze, C7, data-generation, model, provider-research and holdout restrictions remain in force.

## Categorical composition

Counts and shares give each exact security equal weight. Sector labels retain the accepted 1987 SIC-division taxonomy, rather than substituting a modern sector taxonomy.

| Dimension / category | Fixed 42 count | Fixed 42 share | Reference 619 count | Reference share |
|---|---:|---:|---:|---:|
| sector / B__MINING | 3 | 7.1429% | 14 | 2.2617% |
| sector / C__CONSTRUCTION | 3 | 7.1429% | 14 | 2.2617% |
| sector / D__MANUFACTURING | 8 | 19.0476% | 265 | 42.8110% |
| sector / E__TRANSPORTATION_COMMUNICATIONS_ELECTRIC_GAS_SANITARY_SERVICES | 5 | 11.9048% | 37 | 5.9774% |
| sector / F__WHOLESALE_TRADE | 4 | 9.5238% | 15 | 2.4233% |
| sector / G__RETAIL_TRADE | 5 | 11.9048% | 41 | 6.6236% |
| sector / H__FINANCE_INSURANCE_REAL_ESTATE | 7 | 16.6667% | 101 | 16.3166% |
| sector / I__SERVICES | 7 | 16.6667% | 132 | 21.3247% |
| exchange / NASDAQ | 18 | 42.8571% | 260 | 42.0032% |
| exchange / NYSE | 24 | 57.1429% | 359 | 57.9968% |
| exchange / NYSE_AMERICAN | 0 | 0.0000% | 0 | 0.0000% |

## Concentration and categorical alignment

| Dimension | 42 HHI | 619 HHI | 42 effective categories | 619 effective categories | 42 maximum share | 619 maximum share | TVD |
|---|---:|---:|---:|---:|---:|---:|---:|
| exchange | 0.510204 | 0.512790 | 1.960000 | 1.950117 | 57.1429% | 57.9968% | 0.008539 |
| sector | 0.139456 | 0.264946 | 7.170732 | 3.774353 | 19.0476% | 42.8110% | 0.284214 |

The largest sector is Manufacturing in both sets: 8/42 (19.0476%) versus 265/619 (42.8110%). The fixed 42 have lower sector concentration under the predeclared HHI measure. Sector TVD is 2463/8666 = 0.2842141703. The sector quotas deliberately alter composition, so this distance is not a defect criterion.

The 42 include 24 NYSE and 18 Nasdaq securities; the reference contains 359 NYSE and 260 Nasdaq securities. Neither contains NYSE American members. Exchange TVD is 37/4333 = 0.0085391184. No post-hoc threshold interprets either distance as a scientific pass/fail.

## Accepted C5 liquidity

Values are each security's already accepted trailing-60-completed-session median daily dollar volume, in USD. These are cross-security descriptive summaries, not newly calculated daily-bar eligibility tests.

| Statistic | Fixed 42 | Reference 619 |
|---|---:|---:|
| Minimum USD | 21278741.01 | 20076087.285 |
| Median USD | 86396912.0975 | 74613039.77 |
| Maximum USD | 3775788867.43 | 38908006606.3 |
| ln(maximum/minimum) | 5.178656 | 7.569426 |

The fixed 42 median liquidity is $86,396,912.0975, compared with $74,613,039.77 in the reference. The fixed 42 span a narrower observed liquidity range. Both descriptions are conditional on the accepted eligibility screen and deterministic selection design.

## All 42 empirical liquidity reference percentiles

For each member, percentile = count(reference liquidity <= member liquidity)/619. The reference includes the selected members. Ties use the inclusive <= rule. Fractions and 60-digit decimal renderings are also recorded in `results/member_liquidity_percentiles.csv`.

The median of the 42 member percentiles is **340/619 = 0.5492730210 = 54.92730210%**. This is the median of the 42 empirical positions, not a separately calculated empirical percentile of the subject's median dollar value.

| Canonical order | Recorded symbol | Liquidity USD | Reference count <= value | Reference percentile |
|---:|---|---:|---:|---:|
| 1 | ASPN | 33385629.155 | 140 / 619 | 22.6171% |
| 2 | ALB | 259032246.135 | 504 / 619 | 81.4216% |
| 3 | CHRD | 123180306.86 | 400 / 619 | 64.6204% |
| 4 | SYM | 46103735.08 | 208 / 619 | 33.6026% |
| 5 | BAH | 88562596.585 | 344 / 619 | 55.5735% |
| 6 | WBA | 185796891.77 | 462 / 619 | 74.6365% |
| 7 | NVR | 151730479.34 | 431 / 619 | 69.6284% |
| 8 | NWL | 31061502.255 | 120 / 619 | 19.3861% |
| 9 | SMTC | 47210616.29 | 214 / 619 | 34.5719% |
| 10 | CDE | 35777135.44 | 159 / 619 | 25.6866% |
| 11 | MOD | 72613092.395 | 306 / 619 | 49.4346% |
| 12 | BXP | 69127899.015 | 294 / 619 | 47.4960% |
| 13 | UHS | 126399632.68 | 407 / 619 | 65.7512% |
| 14 | TGNA | 27372421.21 | 87 / 619 | 14.0549% |
| 15 | BX | 401827118.37 | 553 / 619 | 89.3376% |
| 16 | CHRW | 115342756 | 389 / 619 | 62.8433% |
| 17 | ADP | 365382847.09 | 547 / 619 | 88.3683% |
| 18 | YUM | 231277858.75 | 489 / 619 | 78.9984% |
| 19 | CFLT | 84231227.61 | 336 / 619 | 54.2811% |
| 20 | GOOGL | 3775788867.43 | 614 / 619 | 99.1922% |
| 21 | MDGL | 73941909.74 | 308 / 619 | 49.7577% |
| 22 | CME | 369391326.11 | 548 / 619 | 88.5299% |
| 23 | RJF | 115378386.225 | 390 / 619 | 63.0048% |
| 24 | JACK | 26561655.1 | 77 / 619 | 12.4394% |
| 25 | MATX | 30858466.815 | 118 / 619 | 19.0630% |
| 26 | GPC | 118070438.54 | 393 / 619 | 63.4895% |
| 27 | RYAN | 43420297.355 | 195 / 619 | 31.5024% |
| 28 | LOPE | 21278741.01 | 18 / 619 | 2.9079% |
| 29 | GO | 32164914.125 | 130 / 619 | 21.0016% |
| 30 | HCC | 46976138.44 | 213 / 619 | 34.4103% |
| 31 | MMS | 26029130.475 | 69 / 619 | 11.1470% |
| 32 | MPWR | 435687974.5 | 556 / 619 | 89.8223% |
| 33 | GWW | 201517147.64 | 467 / 619 | 75.4443% |
| 34 | LRCX | 989949485.73 | 598 / 619 | 96.6074% |
| 35 | NFG | 26095855.33 | 72 / 619 | 11.6317% |
| 36 | PARA | 113957252.55 | 384 / 619 | 62.0355% |
| 37 | LNC | 36981529.965 | 167 / 619 | 26.9790% |
| 38 | DG | 263115912.73 | 508 / 619 | 82.0679% |
| 39 | GEO | 29487832.37 | 102 / 619 | 16.4782% |
| 40 | EME | 141262978.935 | 417 / 619 | 67.3667% |
| 41 | GMS | 30503511.27 | 116 / 619 | 18.7399% |
| 42 | COIN | 1602055495.85 | 607 / 619 | 98.0614% |

## Calculation and validation

`characterize.py` uses exact fractions for shares, HHI, effective counts, TVD and empirical percentiles. Original decimal liquidity strings are parsed without pre-computation rounding. Medians use the arithmetic mean of the middle pair for even N. Natural-log range is evaluated with Decimal precision 80; exact range ratios are retained. Display rounding in this report occurs only after calculation.

`validate_independently.py` imports no producer functions and reopens accepted input bytes. It verifies HHI through ordered-pair category equality, TVD through distribution overlap, liquidity through exact rational order statistics and an independent libm log calculation, and every percentile by exhaustive <= counting. Exact rational results require exact agreement. Log checks use a numerical tolerance of 1e-14; that tolerance is not a scientific adequacy threshold.

- Preflight / identity / integrity checks: **6873 passed**.
- Separate validator checks: **255 passed**, **0 failed**.
- Reversed reference-input row order yields identical serialized metrics and tables.
- Accepted input containers retain their original hashes after calculation.
- Membership and all projected accepted attributes retain their exact identities.
- The producer-stage execution summary says PENDING_INDEPENDENT_VALIDATION; the subsequent `validation_results.json` and `final_return.json` record the completed PASS state.

## Provenance and scientific limitations

The 619 are the available positively certified reference pool, not a complete formation-date eligible population or the general U.S. equity market. The latest canonically recorded 619 / 7,110 / 7,162 split has NOT been independently reconstructed at row level. The verified construction baseline is 619 / 7,109 / 7,163; this declared gap remains Owner-accepted and does not alter the accepted 619 or fixed 42 identities.

Selection was deterministic and used sector quotas and exchange/liquidity marginal targets. Alignment on these variables is partly induced by selection and is not independent evidence of natural representativeness or probability sampling. These results establish neither broad-market representativeness nor adequate statistical power, model validity, trading edge, or freeze suitability. No composite score, adequacy threshold, p-value, or representativeness pass/fail test was introduced. Validation PASS concerns calculation and artifact integrity only.

Accepted derived input evidence was reused. This execution did not independently recertify the 619 against raw SEC filings or daily bars. BRK.B, HEI.A and LANC have blank numeric liquidity fields in the construction pool; their complete values are taken from the exact accepted, hashed selection input. All three are reference-only, and their values affect reference percentiles. The prior independent review disclosed that optional original source bytes for these precise reused values were not supplied to that review. This execution preserves that source-verification limitation.

The input retains 608 V2 sector-container references. All 619 row-level accession and source-hash pointers match the accepted V3 bridge; 11 corrected evidence rows are preserved. This archival navigation limitation is recorded without rewriting accepted evidence. All required accepted-table attributes are present, with no imputation, dropped rows, or denominator renormalization. Bridge timestamps were checked as recorded at or before 2024-08-30 16:00 ET; raw filing timestamps were not reverified.

The same-named loose Downloads selection-input CSV has SHA-256 64a0f76420590721be5c42d8181a0148f589ec93e1a1d17fd20a48b85868c088 and was excluded. The ZIP member used matches accepted SHA-256 46d8b36e43e5a70193e7fd6d273ff6672b21c37b4dc1932a7b643bd27aec8821.

## Boundary and routing

MEMBERSHIP_CHANGED = NO

DEVIATIONS_FROM_PROTOCOL = NONE

REPOSITORY_FILES_MODIFIED = NONE

GITHUB_MUTATION_PERFORMED = NO

NEW_PROVIDER_RESEARCH = NO

RAW_SEC_CORPUS_SEARCH = NO

UNIVERSE_FREEZE_PERFORMED = NO

C7_EXECUTION_PERFORMED = NO

FINAL_HOLDOUT_ACCESSED = NO

RECOMMENDED_NEXT_ACTOR = ADMIN

This package supplies characterization evidence for review. No Owner breadth classification, freeze recommendation or next-lifecycle-stage decision has been executed. Return through Managing/Admin review to Owner.
