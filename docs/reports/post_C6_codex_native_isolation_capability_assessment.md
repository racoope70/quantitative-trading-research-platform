# Post-C6 Codex Native Isolation Capability Assessment

```text
document_status =
TECHNICAL_ASSESSMENT_REFERENCE

document_role =
NON_AUTHORIZING_CODEX_INFRASTRUCTURE_RESEARCH_REFERENCE

authorization_effect =
NONE

current_state_control =
NO

REAL_execution_authority =
NONE

scientific_data_access_authority =
NONE

production_mutation_authority =
NONE

checkpoint_mutation_authority =
NONE

ATTEMPT11_authorization_effect =
NONE

controlling_current_state_document =
PROJECT_CONTEXT.md
```

This report preserves the original research, subsequent accepted bounded capability findings, and the Owner's closure of the current Batch0004 native-profile pursuit: **CLOSED__UNRESOLVED_NOT_REJECTED**. Native permission-profile technology has not been rejected, but mandatory security enforcement remains unqualified and Attempt 11 remains HOLD / NOT AUTHORIZED. Sections 1–10 retain the original assessment chronology; section 11 records the later findings and closure. This reference grants no execution, research, scientific access or mutation authority and does not change QTRP's controlling state. The nonauthorizing Milestone Review Reference Map remains the navigation/history reference; this report does not amend it.

## 1. Purpose and scope

The investigation followed Batch0004 Attempt 10's operational failure at `item_3`, where the reported executable basename was `python`, the internal status was **127**, and executable lookup failed. The task handoff characterizes the event as a bare-`python` lookup failure; the *historical full command and originating command-selection layer* remain unresolved. This reference does not retrieve or reconstruct either.

A subsequent proposed custom macOS Seatbelt synthetic isolation surface was **not qualified**: launch outcomes were recorded as exit 71 (sandbox application refused in a managed wrapper) and exit 134 (cause unresolved outside that wrapper). Protected-read enforcement and model-command credential confinement were not established. The finite prospective repeat-risk matrix did not execute; prospective recurrence remained **UNRESOLVED**.

The narrow research question was whether a **smaller supported native Codex permission mechanism** could provide a representative, disposable, nonproduction execution surface while protecting frozen science, authentication material, secret environments, and command networking. This assessment is not a renewed Attempt 10 investigation or authorization for Attempt 11.

## 2. Research inputs and evidence levels

| Input | Role | What it establishes / does not establish |
|---|---|---|
| **Source A — ChatGPT Deep Research, _QTRP Codex Isolation / Configuration Assessment_** | External/current Codex-capability assessment | Documents candidate features and configuration semantics from cited Codex references; **did not inspect the Owner's installed QTRP Codex runtime**. |
| **Source B — Codex local QTRP infrastructure review** | Host/repository-specific read-only review, summarized in the supplied reconciliation | Reports installed package/version and static source, executable and configuration observations; **did not execute native qualification**. |
| **Source C — Codex reconciliation of external research with local inspection** | Compares A with B and narrows the candidate design | Establishes an assessment-stage preferred approach and qualified caveats; **does not certify effective policy enforcement**. |

Evidence levels distinguish the original research from subsequent observations:

- **DOCUMENTED_SUPPORT:** described in the external capability research; may depend on installed version and precedence.
- **LOCALLY_OBSERVED_STATIC_CAPABILITY:** the original host/source-inspection classification, without an enforcement test.
- **STATIC_LOCAL_CAPABILITY_MARKER:** installed binary markers or version-matched source support a capability; they do not demonstrate accepted configuration or runtime behavior.
- **HOST_EXECUTED_OBSERVATION:** a retained host result, including version/help output or a failed helper launch; it is not inherently a security pass.
- **DYNAMIC_CONFIGURATION_ACCEPTANCE:** a native configuration-parse receipt; not established for `qtrp-synthetic`.
- **EFFECTIVE_PROFILE_SELECTION:** verified resolved profile selection; not established.
- **NATIVE_ENFORCEMENT_INITIALIZATION:** observed initialization of the selected native enforcement path; not established for normal execution.
- **SECURITY_QUALIFICATION:** required positive and negative controls establish effective confinement; not performed.
- **UNRESOLVED:** the permitted evidence does not establish the property.
- **EXECUTED_QUALIFICATION_PASS:** would require accepted runtime positive and negative controls; **none is supplied by these research inputs**.

The original Sources A–C synthesis involved no independent host reinspection or new web research. Section 11 incorporates later accepted evidence; this documentation amendment performs no new capability research or runtime qualification. The repository's established `docs/reports/` nonauthorizing-reference pattern is retained.

## 3. External Codex capability findings — Source A

Source A identified a supported **beta native permission-profile** mechanism as a more precise candidate than legacy `sandbox_mode` for QTRP's negative *read* requirements:

- A named permission profile can express filesystem `read`, `write`, and `deny`, with a **deny-by-default root** (`:root = "deny"`), curated minimal runtime reads (`:minimal = "read"`), and narrowly specified synthetic read/write roots. Rule precedence and actual path aliases still require qualification.
- Command networking can be disabled separately (`permissions.<name>.network.enabled = false`); this concerns command execution, **not** necessary trusted driver/model-control-plane connectivity.
- Spawned-command environment inheritance can be constrained to nonsecret variables. Approval policy `never` can remove interactive approval escalation but **does not itself provide isolation**.
- Legacy `read-only`/`workspace-write` modes alone do not establish the required negative read boundary. Legacy sandbox selection may conflict with or override native permission-profile selection.
- `.rules` control command-execution policy and are **not a substitute** for denying filesystem reads. New hooks, MCP servers, connectors and subagents were not justified; they could expand available execution or data-access surfaces.
- A remote/hosted synthetic sandbox was considered but judged less representative of the existing local Codex command-selection environment than a native local session.
- File-based authentication material can be treated as a denied path class for model-executable commands; **OS Keychain/keyring access was not proven confined** by the reviewed documentation.

Source A's conclusion was **SUPPORTED_SIMPLE_PATH = YES__QUALIFICATION_REQUIRED**, **PREFERRED_DIRECTION = NATIVE_CODEX_PERMISSION_PROFILE**, and **NEW_ARCHITECTURE_REQUIRED = NO** as a *candidate design judgment*, not an operational pass.

## 4. Local QTRP / Codex inspection — Sources B and C

| Property | Supplied local finding | Evidence classification |
|---|---|---|
| Installed native Codex package | **0.157.0**; related native CLI/configuration markers and `--strict-config` marker inspected | **LOCALLY_OBSERVED_STATIC_CAPABILITY**; runtime effectiveness not tested |
| Global Codex configuration | Exists; does **not explicitly establish** the required native profile isolation | Local configuration observation |
| Project `.codex/config.toml` | Absent in the inspected repository state | Local configuration observation |
| Accepted REAL launch route | Explicit `--ignore-user-config`, `--ignore-rules`, and legacy `--sandbox read-only` arguments; exact launch argument tuple identity-bound | Accepted source/static observation; **do not alter** |
| Native profile filesystem/network settings | External docs support the design; local executable/config markers were identified | **DOCUMENTED_SUPPORT**, **not executed qualification** |
| Current authentication backend | File-backed credential resource class exists; active backend not established | **UNRESOLVED** |
| macOS Keychain confinement | Not demonstrated | **UNRESOLVED** |
| Effective runtime policy, rule precedence and hooks/tools inventory | Not qualified in a native synthetic session | **QUALIFICATION_REQUIRED** |
| Four primary model-mediated repeat-risk cases | Not executed by these research inputs | **0/4; NOT_RUN** |

The accepted REAL route is **not** a transparent insertion point for this profile: its external working directory, explicit legacy read-only sandbox argument, ignored user rules/configuration, and exact bound argument identity prevent assuming native-profile qualification can simply be placed underneath it. The proposed test must instead be a **separate nonproduction synthetic native Codex session**. No change to the REAL launch tuple was recommended or authorized.

## 5. Reconciliation and material refinements

```text
DEEP_RESEARCH_AND_LOCAL_REVIEW_AGREEMENT =
PARTIAL__NO_FUNDAMENTAL_ARCHITECTURAL_CONFLICT
```

The local evidence refined the external design in these respects:

1. **Configuration mechanism:** Prefer **explicit CLI `-c` overrides** for a fresh synthetic session, with supported strict validation, rather than creating/modifying global, project, or permanent named-profile configuration files. Managed requirements remain binding; an unexpected configuration layer is a stop condition.
2. **Legacy precedence:** Do not reuse the identity-bound REAL route's `--sandbox read-only`, or add `--full-auto`, `danger-full-access`, or other conflicting legacy selection. Verify **effective** profile selection; accepted syntax alone is insufficient.
3. **Authentication:** The existence of file-backed credentials does **not** prove current active storage. The proposed explicit file-storage choice must be supported and effective. File denial does not by itself prove Keychain-service isolation or that alternate credentials cannot be obtained.
4. **Alternate execution surfaces:** Explicitly disable unneeded hooks, MCP, plugins/connectors, hosted search, shell snapshots, login-shell behavior and multiagent pathways when supported, then verify no effective bypass remains. Do not infer `--ignore-user-config` or an empty MCP table alone eliminates every other layer.
5. **Test accounting:** There is **one** predeclared four-case primary synthetic matrix; **Case 1 counts as the first positive representative model execution**, not as a free rehearsal preceding four more cases. Every launched primary invocation counts.
6. **Platform and beta risk:** Locally observed CLI markers do not prove installed-version runtime parsing, selected-policy enforcement, credential confinement, or a functioning model-mediated path. Each requires qualification.

These are proposed design refinements, **not executed corrections or validation passes**.

## 6. Original preferred candidate architecture

```text
PREFERRED_CONFIGURATION_MECHANISM = EXPLICIT_CLI_CONFIG_OVERRIDES
PERMISSION_PROFILE_ID = qtrp-synthetic
EXECUTION_SURFACE = SEPARATE_DISPOSABLE_SYNTHETIC_NATIVE_CODEX_SESSION
FILESYSTEM_DEFAULT = DENY
MINIMAL_RUNTIME = READ_AS_REQUIRED
SYNTHETIC_SOURCE = READ_ONLY
SYNTHETIC_WORK = BOUNDED_WRITE
PROTECTED_SCIENTIFIC_LOCATIONS = DENY
REAL_AND_HISTORICAL_EVIDENCE_LOCATIONS = DENY
MODEL_COMMAND_CREDENTIAL_LOCATIONS = DENY
COMMAND_NETWORK = DISABLED
SUBPROCESS_ENVIRONMENT = MINIMAL_NONSECRET
APPROVAL_POLICY = NEVER_FOR_QUALIFICATION
LOGIN_SHELL = DISABLED
SHELL_SNAPSHOT = DISABLED
UNNECESSARY_HOOKS = DISABLED
MCP = NONE_EFFECTIVE_FOR_QUALIFICATION
UNNECESSARY_PLUGINS_CONNECTORS = DISABLED
HOSTED_SEARCH = DISABLED
LEGACY_SANDBOX_MODE = ABSENT
STRICT_CONFIG_VALIDATION = REQUIRED_WHERE_SUPPORTED
CUSTOM_SEATBELT_WRAPPER = NOT_REQUIRED_IF_NATIVE_PROFILE_QUALIFIES
NEW_CONTROLLER = NO
NEW_SUPERVISOR = NO
NEW_SECURITY_ARCHITECTURE = NO
```

The conceptual filesystem topology is to deny `:root`, grant only curated `:minimal` runtime read requirements, and reopen **exact, disposable synthetic source and scratch locations**. Denied classes include QTRP frozen science, REAL/historical evidence, the QTRP production repository/deployment outside the synthetic surface, and credentials/related key material. Example path placeholders (not actual locations) are `<QTRP_SYNTHETIC_SOURCE>` (read), `<QTRP_SYNTHETIC_WORK>` (bounded write), `<QTRP_REAL_DEPLOYMENT>` (deny), and `$HOME/.codex` (model-command deny). Actual protected payloads must not be opened to demonstrate denial.

Model-command networking is disabled separately from the trusted Codex driver's necessary authentication/model-service connectivity. A trusted driver's access to an authentication backend **does not authorize** model-generated commands to access credential material; no credential proxy or new broker is part of this candidate.

The native Codex implementation may itself use **macOS Seatbelt** underneath its permission profile. The design proposes retiring the *additional hand-built QTRP Seatbelt wrapper* for this synthetic purpose **only if the native profile qualifies**; it does not remove the platform sandbox, explain historical exit 134, or repair that earlier failure.

This candidate is preferred because it targets the required scientific-read and credential/environment boundaries using supported Codex capabilities, while leaving Policy B, scientific acceptance, proof/recovery, checkpoint state, Owner single-use authorizations and the accepted REAL launch route unchanged. Simplicity is a **design expectation**, not proof of security.

## 7. Original proposed staged qualification — not executed

The following is the **historical proposed test design**, retained for lineage rather than as scheduled or authorized work. The current pursuit is closed under section 11. The design required establishing installed-version syntax and effective configuration precedence before using fabricated fixtures, synthetic credentials/environment sentinels and disposable paths; its model matrix did not execute.

| Phase | Required qualification | Mandatory boundary |
|---|---|---|
| **0 — Freeze** | Pin native binary, effective configuration inputs, fixture identities, safe observations, budgets and finite case definitions | No unauthorized source/payload access |
| **1 — Parse and precedence** | Strictly parse supported CLI overrides; establish `qtrp-synthetic` effective; rule out legacy conflicts and alternate tool surfaces | Configuration acceptance **plus effective selection**, not syntax only |
| **2 — Filesystem positive** | Read approved synthetic fixture; write only within approved scratch | Ordinary synthetic operation works; source remains read-only |
| **3 — Scientific-class negative** | Deny disposable out-of-scope scientific-shaped canaries, child/alias attempts; structural coverage for real protected classes | **Never open actual frozen/validation/holdout bodies** |
| **4 — Credential-class negative** | Deny synthetic credential-shaped canaries and applicable synthetic-only alternate routes | No actual credentials queried; Keychain/service uncertainty must be resolved or **stop** |
| **5 — Secret environment negative** | Show synthetic secret-shaped and unrelated variables absent from model commands; no shell-login/snapshot reintroduction | No secret environment inheritance |
| **6 — Command network negative** | Bounded safe connection attempt under command policy | Command egress denied; driver control-plane distinguished |
| **7 — Unrelated-path negative** | Deny synthetic unrelated-user-path canaries and relevant aliases | Default deny actually enforced |
| **8 — Representative command** | First native model-selected command as **CASE_1**, under all qualified boundaries | Counts as first of **four maximum** model invocations |
| **9 — Remaining matrix** | Execute only CASE_2–CASE_4 if Case 1 stays safe | No adaptive fifth case, retries, rehearsal matrix, or forced interpreter selection |

Each security phase must demonstrate **actual enforcement** before model-mediated execution. Any unsupported, failed, or unresolved mandatory control is **STOP**, not authority to weaken sandboxing or create a new controller. Do not imply model-selected `python`, executable lookup risk, or four-case nonreproduction has been observed unless an accepted future evidence package actually establishes it.

## 8. Unresolved risks and evidence needed

| Requirement | Research-stage status |
|---|---|
| Native beta permission-profile parsing and enforcement on installed **0.157.0** | **QUALIFICATION_REQUIRED** |
| Configuration precedence and effective default permission selection | **QUALIFICATION_REQUIRED** |
| macOS filesystem denials, aliases and child-command inheritance | **QUALIFICATION_REQUIRED** |
| File-backed authentication selection and model-command credential denial | **QUALIFICATION_REQUIRED** |
| OS Keychain/alternate credential-service confinement | **UNRESOLVED** |
| Secret environment inheritance, login shell and shell snapshots | **QUALIFICATION_REQUIRED** |
| Command network confinement and alternate tool routes | **QUALIFICATION_REQUIRED** |
| Native representative model-mediated execution | **QUALIFICATION_REQUIRED** |
| Four-case natural `python` selection/repeat-risk result | **NOT_YET_EXECUTED_IN_RESEARCH_INPUTS** |
| Complete historical Attempt 10 command-selector origin and custom isolation exit 134 cause | **UNRESOLVED; CLOSED INVESTIGATIONS** |

Neither documented support nor static local markers amount to an **EXECUTED_QUALIFICATION_PASS**. A future qualifying result must carry its own exact effective-configuration evidence, positive and negative control receipts, and independent review. This document cannot substitute for them.

## 9. Implications for accepted QTRP state

```text
SCIENTIFIC_CONTRACT_IMPACT = NONE_EXPECTED__NOT_EXECUTED
OWNER_AUTHORIZATION_MODEL_IMPACT = NONE_EXPECTED__NOT_EXECUTED
POLICY_B_IMPACT = NONE
POLICY_B = UNCHANGED
PRODUCTION_RUNTIME = UNCHANGED
REAL_EXECUTION = NONE
CHECKPOINT_SEQUENCE = 54__PRESERVE
FROZEN_ACCEPTED_RECORDS = 275__PRESERVE
U0012 = PENDING__TEN_HISTORICAL_ATTEMPTS
ATTEMPT10_AUTHORIZATION = CONSUMED__NOT_REUSABLE
U0013 = PROHIBITED
ATTEMPT11 = NOT_AUTHORIZED__REMAINS_HOLD
PRODUCTION_SOURCE_OR_CONFIG_MUTATION = NOT_AUTHORIZED_BY_THIS_REPORT
REAL_DISPATCH = NOT_AUTHORIZED_BY_THIS_REPORT
```

The candidate may provide a path to a future synthetic operational assessment **only after** native-profile security qualification and separately applicable Owner direction. It cannot itself clear Attempt 11, alter the bound REAL execution tuple, or establish scientific readiness. `PROJECT_CONTEXT.md` remains the controlling source for broad current lifecycle and authorization state; this report is a reference, not a checkpoint tracker or second current-state authority.

## 10. Original nonauthorizing research conclusion

The following preserves the original assessment-stage conclusion. Section 11 supersedes its qualification-readiness language with the accepted findings and final Owner closure; it creates no pending follow-up work.

```text
SIMPLER_SUPPORTED_CAPABILITY_AVAILABLE =
YES__QUALIFICATION_REQUIRED

PREFERRED_CANDIDATE =
NATIVE_CODEX_PERMISSION_PROFILE_ON_SEPARATE_SYNTHETIC_SURFACE

CUSTOM_ISOLATION_CODE_REQUIRED =
NO_FOR_PREFERRED_APPROACH_IF_QUALIFICATION_PASSES

NEW_SECURITY_ARCHITECTURE_REQUIRED =
NO__CANDIDATE_ASSESSMENT

READY_FOR_OWNER_QUALIFICATION_DECISION =
YES__AT_RESEARCH_ASSESSMENT_STAGE

NATIVE_PROFILE_RUNTIME_QUALIFICATION =
NOT_ESTABLISHED_BY_THIS_REPORT

ATTEMPT11_IMPLICATION =
REMAINS_HOLD__POTENTIALLY_UNBLOCKABLE_ONLY_AFTER_SUCCESSFUL_QUALIFICATION_AND_SEPARATE_OWNER_DECISION

FINAL_DISPOSITION =
NATIVE_CODEX_PERMISSION_PROFILE_SELECTED_AS_PREFERRED_QUALIFICATION_CANDIDATE__NOT_YET_QUALIFIED

AUTHORIZATION_EFFECT =
NONE
```

### Source and repository reference notes

- **Source A:** Owner-supplied ChatGPT Deep Research, _QTRP Codex Isolation / Configuration Assessment_; includes references to Codex [permissions](https://learn.chatgpt.com/docs/permissions), [configuration](https://learn.chatgpt.com/docs/config-file/config-reference), and [authentication](https://learn.chatgpt.com/docs/auth). These links are **source-reported references**, not freshly checked for this report.
- **Sources B/C:** Owner-supplied Codex local infrastructure observations and reconciliation, including installed 0.157.0 identity, existing REAL argument restrictions, static configuration/capability classifications, and the proposed staged qualification matrix. No new host inspection was conducted for the original synthesis; subsequent accepted observations are distinguished in section 11.
- **Repository convention:** `docs/reports/` holds nonauthorizing technical/evidence references; `docs/decisions/` holds Owner decisions; `docs/workflows/milestone_review_reference_map.md` is nonauthorizing navigation; `PROJECT_CONTEXT.md` alone controls broad current lifecycle and authorization boundaries.

## 11. Accepted bounded findings and final Owner closure

The native-helper qualification and subsequent nonmodel normal-execution assessment refined the original candidate without establishing mandatory confinement. The prior custom Seatbelt qualification remains unsuccessful or unresolved, with its accepted exit-71 / unresolved-exit-134 classification preserved; neither historical investigation was reopened.

The installed native Codex 0.157.0 executable identity is SHA-256 `17ae582b1048415503cf9455e677fd75c5b25ced17f20b883e55946fc5eeb679` (256,856,672 bytes). The helper returned exit 65 because its generated sandbox policy contained an unbound `TIOCSTI` variable. An incorrect help form had unintentionally entered helper setup; the corrected help query succeeded. Version-matched source confirms the [helper-specific append](https://github.com/openai/codex/blob/rust-v0.157.0/codex-rs/cli/src/debug_sandbox.rs#L395-L440). The inspected [normal local manager](https://github.com/openai/codex/blob/rust-v0.157.0/codex-rs/sandboxing/src/manager.rs#L425-L462) uses the shared Seatbelt builder without that append. This distinction establishes neither normal-execution failure nor successful normal enforcement.

The accepted nonmodel assessment used installed identities, retained safe help receipts, configuration metadata and version-matched source. Named user configuration profiles (`--profile`, selecting `<name>.config.toml`) are distinct from permission-profile selection (`default_permissions` and `[permissions.<name>]`). Layered configuration, explicit CLI overrides, managed requirements and legacy selection have source-defined precedence; complete dynamic resolution was not obtained. No `qtrp-synthetic` profile was successfully created, parsed or activated.

No safe installed parser-only or initialization-only diagnostic was established within that task's limits. Normal `exec` proceeds through authentication and session/turn setup; `features list` uses authentication-backed configuration; `doctor` runs wider authentication, network and sandbox checks. None was invoked as a substitute validator. The normal-execution assessment launched no new native process, model session, sandbox target or security trial. The existing REAL launch tuple and production runtime remain unchanged.

```text
TESTED_HELPER_RESULT = EXIT65__UNBOUND_TIOCSTI
HELPER_SPECIFIC_TIOCSTI_APPEND = CONFIRMED_IN_VERSION_MATCHED_SOURCE
NORMAL_LOCAL_MANAGER_TIOCSTI_APPEND = ABSENT_IN_INSPECTED_SOURCE
HELPER_FAILURE_GENERALIZES_TO_NORMAL_EXEC = NOT_DEMONSTRATED
DOCUMENTED_PERMISSION_PROFILE_SUPPORT = ESTABLISHED
STATIC_LOCAL_CAPABILITY_SUPPORT = ESTABLISHED
NORMAL_NATIVE_PERMISSION_PROFILE_CAPABILITY = PARTIAL
NORMAL_EXEC_CONFIGURATION_ACCEPTANCE = UNRESOLVED
STRICT_CONFIG_PARSE = NOT_EXECUTED
NORMAL_EXEC_PROFILE_SELECTION = NOT_EXECUTED
NORMAL_EXEC_ENFORCEMENT_INITIALIZATION = NOT_EXECUTED
CONFIGURATION_PRECEDENCE = SOURCE_BACKED__NOT_FULLY_DYNAMICALLY_RESOLVED
SECURITY_QUALIFICATION = NOT_PERFORMED
SCIENTIFIC_DATA_CONFINEMENT = UNRESOLVED
FILE_CREDENTIAL_CONFINEMENT = UNRESOLVED
ALTERNATE_CREDENTIAL_ROUTE = UNRESOLVED
SECRET_ENVIRONMENT_CONFINEMENT = UNRESOLVED
COMMAND_NETWORK_CONFINEMENT = UNRESOLVED
MODEL_MEDIATED_EXECUTION = NOT_RUN
PRIMARY_SYNTHETIC_MODEL_INVOCATIONS = 0_OF_4
PROSPECTIVE_PYTHON_REPEAT_RISK = UNRESOLVED
```

The Owner accepted the partial capability assessment and **closed the current Batch0004 native-profile pursuit because mandatory runtime security enforcement remains unqualified**. The technology remains a potentially supported candidate. This is a closure, with no automatic follow-up or periodic retesting.

```text
CURRENT_BATCH0004_NATIVE_PROFILE_PURSUIT = CLOSED__UNRESOLVED_NOT_REJECTED
NATIVE_PROFILE_TECHNOLOGY_REJECTED = NO
PARTIAL_CAPABILITY_ASSESSMENT = ACCEPTED
MATERIAL_SECURITY_HOLD = ACTIVE
FURTHER_BATCH0004_ENGINEERING = NOT_AUTHORIZED
ADDITIONAL_STATIC_RESEARCH = NOT_AUTHORIZED
ADDITIONAL_HELPER_DIAGNOSIS = NOT_AUTHORIZED
ADDITIONAL_NORMAL_EXEC_ASSESSMENT = NOT_AUTHORIZED
MODEL_MEDIATED_QUALIFICATION = NOT_AUTHORIZED
CUSTOM_ISOLATION_REDESIGN = NOT_AUTHORIZED
ATTEMPT11 = HOLD__NOT_AUTHORIZED
REOPENING_CONDITION = MATERIALLY_NEW_EVIDENCE_OR_SEPARATE_OWNER_AUTHORIZATION
```

A materially changed supported Codex release, an official model-free enforcement validator, supported credential/Keychain confinement evidence, independently demonstrated native isolation, or a separately authorized materially different execution surface could support future Owner reconsideration. These are illustrative conditions, not scheduled work or automatic authority to reopen research, diagnosis, qualification or execution.

Accepted nonpayload control receipts and scoped metadata preserve checkpoint 54, U0012 pending with ten historical attempts, 275 accepted records, consumed/nonreusable Attempt 10 authorization and U0013 pending with zero attempts. Frozen scientific bodies were not opened or rehashed. Policy B, scientific proof/recovery and production runtime remain unchanged; REAL execution is NONE. This report records the Owner disposition as a nonauthorizing reference and does not become a lifecycle controller; `PROJECT_CONTEXT.md` retains that role.

Evidence and disposition references:

- `BATCH0004_NATIVE_CODEX_PERMISSION_PROFILE_SYNTHETIC_QUALIFICATION_V1`: retained helper observation and source distinction, not a confinement pass.
- `BATCH0004_NATIVE_CODEX_NORMAL_EXEC_PERMISSION_PROFILE_CAPABILITY_ASSESSMENT_V1`: accepted partial assessment; archive `BATCH0004_NATIVE_NORMAL_EXEC_CAPABILITY_ASSESSMENT_EVIDENCE.zip`, SHA-256 `0fb2d04865c4ea8490ce64dbc406f07cd28aacc0e817741198ce53093f258b36`. Its `SOURCE_REFERENCE_MAP.json`, `NORMAL_EXEC_VS_HELPER.json`, capability/precedence records and scoped preservation receipts retain the precise evidence limits. Version-tagged source identities are not a reproducible-build attestation.
- `BATCH0004_NATIVE_CODEX_ISOLATION_CAPABILITY_DURABLE_REPORT_AMENDMENT_V1`: controlling Owner closure and authorization for this report amendment only; no further technical work or execution is authorized.
