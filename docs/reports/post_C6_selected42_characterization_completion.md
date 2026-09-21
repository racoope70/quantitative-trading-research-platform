# Post-C6 Selected-42 Characterization Completion Record

```text
document_status =
OWNER_ACCEPTED_SCIENTIFIC_COMPLETION_RECORD

document_role =
POST_C6_SELECTED42_CHARACTERIZATION_COMPLETION_RECORD

current_state_controller =
NO

authorization_source =
NO

lifecycle_controller =
NO

controlling_current_state_document =
PROJECT_CONTEXT.md

controlling_characterization_protocol =
EVID_POSTC6_SELECTED42_CHARACTERIZATION_PROTOCOL_001
```

This record preserves the accepted descriptive characterization of the fixed
42-security selected experimental universe and its governed comparison against
the accepted 619-security available certified reference frame.

It does not independently freeze the universe, authorize C7, authorize provider
access, authorize dataset generation, authorize model work, or replace
`PROJECT_CONTEXT.md` as the controller of broad current lifecycle state.

## 1. Completion and controlling identities

```text
CHARACTERIZATION_TASK =
POSTC6_SELECTED42_CHARACTERIZATION_EXECUTION

CHARACTERIZATION_STATUS =
COMPLETE__DESCRIPTIVE_CHARACTERIZATION_COMPLETE

CHARACTERIZATION_VALIDATION_RESULT =
PASS

CANONICAL_EXECUTION_BASE_SHA =
9f61e40aeea71a722f9328ff09495cd20002b811

CHARACTERIZATION_PACKAGE_SHA256 =
2e6b7f5e577da7ca590c8e5176a91e98221ac8543a5b0872650cb1bc312f70bf

CHARACTERIZATION_PROTOCOL_ID =
EVID_POSTC6_SELECTED42_CHARACTERIZATION_PROTOCOL_001

DEVIATIONS_FROM_PROTOCOL =
NONE

PROTOCOL_CONFLICT =
NONE
```

The accepted execution was read against canonical state at
`9f61e40aeea71a722f9328ff09495cd20002b811`.

## 2. Fixed subject and reference identities

```text
SUBJECT =
SELECTED_EXPERIMENTAL_UNIVERSE_42

SUBJECT_COUNT =
42

FIXED_42_SHA256 =
43a42ddf4e4ac40730be7457904be588f4cf26bc333650a301090c925097041f

FIXED_42_IDENTITY_VERIFIED =
YES

REFERENCE_FRAME =
AVAILABLE_POSITIVELY_CERTIFIED_ELIGIBLE_CANDIDATE_POOL_619

REFERENCE_COUNT =
619

REFERENCE_619_SHA256 =
aed6f9e137b52948ebd4c2385c84b5a2b39e2ddd8c7be90fe1f30fa8415cb7c7

REFERENCE_619_IDENTITY_VERIFIED =
YES

FIXED_42_SUBSET_OF_REFERENCE_619 =
YES

MEMBERSHIP_FIXED_DURING_CHARACTERIZATION =
YES

MEMBERSHIP_CHANGED =
NO
```

The 619-security frame remains the available positively certified reference
frame. It is not asserted to be the complete formation-date eligible
population.

## 3. Required characterization dimensions

The accepted protocol required:

```text
PIT_SECTOR_1987_SIC_DIVISION
+
C5_TRAILING_60_COMPLETED_SESSION_MEDIAN_DAILY_DOLLAR_VOLUME
+
PIT_PRIMARY_EXCHANGE_FAMILY
```

```text
REQUIRED_SUBJECT_ATTRIBUTE_COMPLETENESS =
PASS

REQUIRED_REFERENCE_ATTRIBUTE_COMPLETENESS_FOR_COMPARISON =
PASS

MISSING_REQUIRED_VALUE_IMPUTATION =
NONE

MARKET_CAP_CHARACTERIZATION =
NOT_REQUIRED
```

## 4. Sector characterization

```text
OBSERVED_SUBJECT_SIC_DIVISION_COUNT =
8

SUBJECT_SECTOR_HHI =
41/294

SUBJECT_SECTOR_HHI_DECIMAL =
0.139455782312925170068027210884353741496598639455782312925170

SUBJECT_SECTOR_EFFECTIVE_CATEGORY_COUNT =
294/41

SUBJECT_SECTOR_EFFECTIVE_CATEGORY_COUNT_DECIMAL =
7.17073170731707317073170731707317073170731707317073170731707

SUBJECT_SECTOR_MAXIMUM_CATEGORY_SHARE =
4/21

SUBJECT_SECTOR_MAXIMUM_CATEGORY_SHARE_DECIMAL =
0.190476190476190476190476190476190476190476190476190476190476

SECTOR_TOTAL_VARIATION_DISTANCE_VS_REFERENCE =
2463/8666

SECTOR_TOTAL_VARIATION_DISTANCE_VS_REFERENCE_DECIMAL =
0.284214170320793907223632587122086314331871682437110546965151
```

Material descriptive finding:

```text
FIXED_42_SECTOR_CONCENTRATION =
LOWER_THAN_REFERENCE_ON_REPORTED_HHI_COMPARISON

LARGEST_NOTED_SECTOR_COMPARISON =
MANUFACTURING__8_OF_42_SUBJECT__265_OF_619_REFERENCE
```

This is descriptive comparison only. It is not a general-U.S.-equity-market
representativeness claim.

## 5. Primary-exchange characterization

```text
SUBJECT_NYSE_COUNT =
24

SUBJECT_NASDAQ_COUNT =
18

SUBJECT_NYSE_AMERICAN_COUNT =
0

SUBJECT_EXCHANGE_HHI =
25/49

SUBJECT_EXCHANGE_HHI_DECIMAL =
0.510204081632653061224489795918367346938775510204081632653061

SUBJECT_EXCHANGE_EFFECTIVE_CATEGORY_COUNT =
49/25

SUBJECT_EXCHANGE_EFFECTIVE_CATEGORY_COUNT_DECIMAL =
1.96

SUBJECT_EXCHANGE_MAXIMUM_CATEGORY_SHARE =
4/7

SUBJECT_EXCHANGE_MAXIMUM_CATEGORY_SHARE_DECIMAL =
0.571428571428571428571428571428571428571428571428571428571429

EXCHANGE_TOTAL_VARIATION_DISTANCE_VS_REFERENCE =
37/4333

EXCHANGE_TOTAL_VARIATION_DISTANCE_VS_REFERENCE_DECIMAL =
0.00853911839372259404569582275559658435264251096238172167089776
```

## 6. Liquidity characterization

```text
SUBJECT_LIQUIDITY_COUNT =
42

SUBJECT_MINIMUM_MEDIAN_DAILY_DOLLAR_VOLUME_USD =
21278741.01

SUBJECT_MEDIAN_MEDIAN_DAILY_DOLLAR_VOLUME_USD =
86396912.0975

SUBJECT_MAXIMUM_MEDIAN_DAILY_DOLLAR_VOLUME_USD =
3775788867.43

SUBJECT_LIQUIDITY_MAXIMUM_OVER_MINIMUM =
377578886743/2127874101

SUBJECT_LIQUIDITY_NATURAL_LOG_RANGE =
5.1786561116969265903930796645100362601052847071498952493446301087031510135462349

REFERENCE_LIQUIDITY_COUNT =
619

REFERENCE_MINIMUM_MEDIAN_DAILY_DOLLAR_VOLUME_USD =
20076087.285

REFERENCE_MEDIAN_MEDIAN_DAILY_DOLLAR_VOLUME_USD =
74613039.77

REFERENCE_MAXIMUM_MEDIAN_DAILY_DOLLAR_VOLUME_USD =
38908006606.3

REFERENCE_LIQUIDITY_MAXIMUM_OVER_MINIMUM =
7781601321260/4015217457

REFERENCE_LIQUIDITY_NATURAL_LOG_RANGE =
7.5694259142702941129236501326204086960821879334097755445599735797499542227761386
```

The empirical reference percentile definition was:

```text
COUNT(reference_value <= subject_value) / 619
```

with ties handled by `<=` and the 42 subject securities included in the
reference frame because the subject is a subset of that frame.

```text
MEDIAN_MEMBER_LIQUIDITY_REFERENCE_PERCENTILE =
340/619

MEDIAN_MEMBER_LIQUIDITY_REFERENCE_PERCENTILE_DECIMAL =
0.549273021001615508885298869143780290791599353796445880452342
```

## 7. Interpretation and selection-conditioning boundary

The characterization is descriptive.

```text
SCALAR_COMPOSITE_SCORE =
NONE

CROSS_DIMENSION_WEIGHTING =
NONE

POST_HOC_NUMERIC_ROUTING_THRESHOLD =
NONE

AUTOMATIC_PASS_FAIL_CHARACTERIZATION_THRESHOLD =
NONE

GENERAL_US_EQUITY_MARKET_REPRESENTATIVENESS_CLAIM =
PROHIBITED

REFERENCE_RELATIVE_ALIGNMENT =
DESCRIPTIVE_ONLY
```

Sector was used in the predeclared hard selection quotas. Primary exchange and
liquidity were used in the predeclared global marginal-balancing design.
Therefore alignment on these dimensions is partly design-induced and must not
be represented as independent evidence of random or natural
representativeness.

## 8. Formation-frame and provenance limitations

The accepted characterization preserves the already known formation-frame
limitation:

```text
FORMATION_FRAME_STATUS =
INCOMPLETE__OWNER_ACCEPTED_MATERIAL_LIMITATION

REFERENCE_FRAME_COMPLETE_FORMATION_POPULATION_CLAIM =
PROHIBITED

FAIL_CLOSED_UNRESOLVED_FORMATION_FRAME_COUNT =
7162

LATEST_7110_7162_ROW_LEVEL_TRANSITION =
NOT_INDEPENDENTLY_RECONSTRUCTED

LATEST_7110_7162_PROVENANCE_LIMITATION_PRESERVED =
YES
```

The unresolved row-level provenance for the single net transition represented
by the later 7110 ineligible / 7162 unresolved aggregate state remains a
declared evidence limitation. It does not alter the accepted fixed-42 identity,
the accepted 619 reference identity, or the reported descriptive
characterization results.

## 9. Reproducibility and independent validation

The complete characterization package is durably preserved outside the
repository with SHA-256:

```text
2e6b7f5e577da7ca590c8e5176a91e98221ac8543a5b0872650cb1bc312f70bf
```

The bounded canonical evidence subset is preserved at:

```text
docs/reports/post_C6_selected42_characterization_evidence/
```

Retained package evidence:

```text
SHA256SUMS.txt
artifact_manifest.json
canonical_verification.json
characterization_report.md
provenance_and_limitations.md
results/calculation_definitions.json
results/input_identity_manifest.json
results/metrics.json
results/missingness_and_reuse.json
validation_results.json
```

Exact retained evidence SHA-256 identities:

```text
SHA256SUMS.txt =
7cd4ba1c3f76e40754b512535dbd35bda8ec0d18f6582951bc30ecff7f77da8c

artifact_manifest.json =
7d246f1ac76a92fb7f3bd9c6ff1041babdcec2bd61f18e7c07c9d1b3240f699a

canonical_verification.json =
c6e2dadd052899e4713ffec38547511240788f69f8499dab6171f44463caff24

characterization_report.md =
c1e34ea05315abca665ffd69243d12a36fdcda4526f47f9b8d6bf6aa5702f01b

provenance_and_limitations.md =
e8454f8c76f29d9761a8459a4d78b061946c6eeaf8f1a04173cca7e0754cfba8

results/calculation_definitions.json =
dd33741367ed33f175551fa5d70f3a1a3bbc6d9493e6dbf88bbb7b1db6fa7115

results/input_identity_manifest.json =
4c6e52c0e20f1a09c72535b3c4d0d6eaacfce7b979170c57c8d3e04ddc95702c

results/metrics.json =
a67c088851975a95d7210334d28d405d325fd802f7b3f135477c4d1367037962

results/missingness_and_reuse.json =
b3f27bfb49bf725dcb78ce5945c6ce936db537e77f5130d00dabd028609021aa

validation_results.json =
45542ec9616464bf6afa1e21a7ad09dd7771b8e972ac57c21c4616e6eb6e4b59
```

The package's internal SHA-256 manifest was independently rechecked before
canonical recording:

```text
INTERNAL_MEMBER_HASH_FAILURE_COUNT =
0

INTERNAL_SHA256_MANIFEST =
PASS
```

Independent validation confirmed:

```text
ALL_REQUIRED_CHARACTERIZATION_CHECKS =
PASS

ALL_42_EMPIRICAL_LIQUIDITY_PERCENTILES =
PASS

OUTPUT_NO_MEMBERSHIP_MUTATION =
PASS

ALL_PRODUCER_PREFLIGHT_CHECKS =
PASS

NO_MISSING_REQUIRED_INPUTS =
PASS

DECLARED_PROVENANCE_GAP_PRESERVED =
PASS

REPORTED_ROW_ORDER_INVARIANCE =
PASS

SOURCE_IMMUTABILITY_CHECKS =
PASS
```

## 10. Scientific and repository non-actions

The characterization transaction itself performed none of the following:

```text
MEMBERSHIP_CHANGE_PERFORMED =
NO

UNIVERSE_FREEZE_PERFORMED =
NO

PROVIDER_ACCESS_EXECUTION_PERFORMED =
NO

DATASET_GENERATION_PERFORMED =
NO

FEATURE_GENERATION_PERFORMED =
NO

MODEL_WORK_PERFORMED =
NO

FINAL_HOLDOUT_ACCESSED =
NO

PAPER_TRADING_PERFORMED =
NO

LIVE_TRADING_PERFORMED =
NO

DEPLOYMENT_PERFORMED =
NO

C7_EXECUTED =
NO
```

## 11. Current-state consequence

The required descriptive characterization of the accepted fixed 42-security
selection is complete and reproducibly validated.

This completion record does not itself perform the separately governed
fixed-42 universe freeze. Any freeze effect must come from the separate
Owner-approved fixed-42 freeze decision and its aligned freeze manifest and
current-state recording.

C7 remains separately governed and unauthorized by this record.
