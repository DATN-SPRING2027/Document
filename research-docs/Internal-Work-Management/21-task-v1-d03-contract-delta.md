# DATN-95 — D-03 contract delta and minimum data-foundation specification

> **Approval successor — confirmation recorded 14/10/2026:** the requester confirmed that the Leader approved all P1–P3 at revision `6628c60ed5b259ae8c368883c8619543919aaf20`. The [scoped approval record](22-task-v1-d03-delta-approval-record.md) is the current authority for those rows and records the P3 `UNCERTAIN` clarification and acceptance of P2's exact W predicate (including U+200B-only titles). Current contract gate: **A — READY FOR D-03 IMPLEMENTATION**, for the private slice only. No implementation/test completion or GitHub approval is claimed.
>
> The proposal wording, C classifications, pending-approval conditions and Jira snapshot below describe the reviewed revision. Read them with the successor record; they do not reopen P1–P3. The immutable reviewed revision remains available in Git history.

> **New product decisions: PROPOSED — NOT APPROVED.** PR #30's scoped approval remains valid. This document resolves engineering choices and proposes only the remaining D-03 product decisions; it does not supersede that approval or authorize backend work.
>
> **Current readiness: C — BLOCKED — EXPLICIT PRODUCT DECISIONS REQUIRED.** Only P1–P3 below block the proposed minimal D-03 slice. D-02's full transition matrix, public API contracts, and D-04 runtime activation are separate dependencies of their own features.

Prepared 13/10/2026 (Asia/Bangkok), DRI Danh. Product Docs remote main was fetched and verified at **69c16445417f3fbcaecd6b04943603c092003b77**. DATN-BE remote main was fetched and inspected read-only at **fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a**. No application, schema, migration, runtime, database, or SAGE selector is changed here.

## 1. Three decisions for the Leader

Approve, amend, or reject each row independently. Approval must name this document's reviewed Git revision and the selected rows. Engineering details marked B below require engineering review, not another product-policy vote.

| Item | Existing approval | Concrete recommendation | Evidence and rationale | Required Leader action |
|---|---|---|---|---|
| **P1 — D-03 scope** | Core Project-local Task direction and the data-foundation objective are approved; exact operation selection is open. | D-03 delivers private, human-origin **create and read persistence primitives**, Task/history storage definitions, repeatable disposable initialization and tests. Creation is the only mutation. No HTTP/Redis handler or production caller is connected. Defer post-create edits, assignment, status, search APIs and integrations to their owning work packages. A base record has no lifecycle field yet; add it through an approved later schema change before a lifecycle API is released. | Parent AC asks for a minimal data foundation and persistence/failure evidence, not all CRUD or all transitions. Creation exercises the accepted atomicity boundary without choosing a state, update policy, or actor permission matrix. This reduces D-03 scope only, not the approved eventual V1 direction. | Approve this D-03 slice and its exclusions, or identify the additional mutation/field genuinely required for D-03. |
| **P2 — Minimum record and title rule** | Stable ID, Project ownership, title, creator and server timestamps are approved field principles; exact requiredness/rules remain open. | Persist only the seven fields in §5: _id, projectId, title, createdBy, createdAt, updatedAt, version. All required and non-null. Title is a preserved Unicode string containing at least one non-whitespace character; no trimming, case folding, business length cap, or unique title rule. MongoDB's document-size ceiling still applies. Version is the internal creation ordinal 1, not a public concurrency token. | No evidence supports a particular business title-length cap, priority enum, due-date policy, or optional field. Explicitly selecting this record closes field presence/requiredness rather than treating the earlier dictionary as accepted. Version supplies ADR-010's history provenance for this single mutation. | Approve the minimal record and title semantics, or supply exact alternative rules. ObjectId/BSON Date encodings and validator implementation are B engineering choices. |
| **P3 — Creation history content and coverage** | Append-only history, safe provenance and atomic Task/history persistence are accepted. Exact coverage/content is open. | Every successful creation writes exactly one creation event with the identifier/provenance/changed-field-name projection in §8. No title/description values, before/after snapshots, prompts, tokens or personal profile copies. Failed creation writes no successful mutation-history record. No other mutation is exposed. | Establishes the minimum observable history oracle and one-event-per-created-version invariant. Avoids silently adopting a complete audit, retention, event-sourcing or delivery policy. | Approve creation coverage, the safe projection and the one-event-per-version invariant; amend any required provenance field. Event spelling/BSON types/index keys are B engineering details after this semantic choice. |

**No reapproval requested:** one Project owner; contextual Organization; 0..1 Team/assignee; non-unique title; default unique _id; append-only history; atomic mutation/history; conditional outbox deferral; the approved validation/index/test direction. Technical choices do not close P1–P3 by themselves.

## 2. Authority, evidence and classification

Use A = ACCEPTED / DECISION; B = TECHNICAL DESIGN; C = PRODUCT/DOMAIN DECISION; D = FOLLOW-UP. FACT records an observation, INFERENCE a reasoned recommendation, UNKNOWN an unanswered requirement, and CONFLICT a source mismatch. A recommendation in a C row is always **PROPOSED — NOT APPROVED**.

| Evidence | Finding and limit |
|---|---|
| [PR #30](https://github.com/DATN-SPRING2027/Document/pull/30), [approval record](20-task-v1-contract-approval-record.md), [proposal §12](19-task-v1-contract-closure-proposal.md#12-leader-decision-matrix) | DECISION: Trần Kim Thắng, Leader, approved the recorded recommendation scope on 13/10/2026, bound to proposal source 145af128e70fcfbcd6a64d5ac7859dfb9468d14c. Approval excludes exact fields, lifecycle, action permissions, event details and executable oracles. This document is a delta, not a replacement approval record. |
| Local SAGE project context, constitution, Governance Model v1, ADR-003, SPEC-001 and decision register | Governance preserves accepted decisions and routes new ones to humans. FACT: baseline.active remains null; this does not revoke PR #30 or prevent a scoped document review. Historical inventory/current-state snapshots are not fresh runtime evidence. Root-file provenance is recorded in §13; SAGE files are outside this documentation change. |
| [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md), [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md) | DECISION: Task is canonical; Task service source stays in DATN-BE, target deployment is independent, target owner is continuum_task, history is local/atomic, and consumers use contracts. No field-level schema follows just from these boundaries. ADR-010 §7 requires version, actor/source, change metadata, time, operation and correlation provenance; §8's Agent branch stays outside this slice. |
| [D-01 worksheet](14-task-v1-review-worksheet.md), [D-02 catalogue](16-task-v1-state-machine-contract.md) | FACT: corrected heading says “Transition matrix for review”; 25 cells remain UNKNOWN and enabled transitions are 0. Earlier research schemas/use cases retain their proposal status; read them through the later scoped approval. |
| DATN-BE main at fc7d0be: [ownership inventory](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/src/common/mongodb/database-names.ts), [Compose](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/docker-compose.microservices.yml) | FACT: MongoDB 7.0 / rs0 is configured; Task is absent from SERVICE_DATABASES and no Task source/model/consumer exists. Configuration is not a live deployment verification. continuum_task is a target, not an active runtime owner. |
| [Organization context](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/docs/decisions/organization-membership-context.md), [Project Access V1](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/docs/decisions/project-access-visibility-v1.md) | DECISION: ACTIVE Organization membership establishes trusted context; Project access also needs effective scoped evidence. PUBLIC metadata and Organization ADMIN do not grant nested Task access. Project removal revokes effective access while preserving records. The Organization document's historical shared-DB reference is superseded by ADR-003; it does not authorize a continuum_db fallback. Task action codes are not inferred from Project permissions. |
| [IAM schema conventions](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts), [Project repository](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/src/services/iam/infrastructure/mongodb/project.repository.ts), [transaction integration fixture](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/src/services/iam/infrastructure/mongodb/project.repository.mongodb.spec.ts) | FACT: ObjectId references, server timestamps, service-owned models, startSession/withTransaction/finally endSession and disposable DB tests exist. Reuse these patterns; do not copy IAM audit fields, exception statuses or permissions as Task policy. |
| [BE guide](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/AGENTS.md) versus ADR-010 | CONFLICT: the guide calls BE a modular monolith while the accepted Task target is an independent service. B: reconcile the relevant guide against the accepted target in the owning implementation PR before source edits; do not ask the Leader to select the deployment again. D-04 owns activation/routing/ports, not this document. |

### 2.1 Jira snapshot and exact acceptance criteria

Inspected directly in Jira on 13/10/2026. [DATN-95](https://trankimthang0207.atlassian.net/browse/DATN-95), “D-03 Task Data Foundation”, is In Progress; assignee danh2492004 (Danh). Its description requires design against the approved Task contract, treats continuum_task as target ownership, excludes speculative fields and requires an isolated test database. Parent AC:

1. **AC1:** “Data shape and database ownership are explicitly approved and use the Task service database.”
2. **AC2:** “Constraints and atomicity reflect approved use cases; no speculative fields or legacy continuum_db fallback.”
3. **AC3:** “Disposable tests validate indexes, persistence, and failure handling.”

| Jira item | Exact summary | Observed status | Description / acceptance / mapping |
|---|---|---|---|
| DATN-116 | D-03.1 Confirm Task collection ownership | Done | Description empty; no child-specific AC. A: target ownership already accepted. |
| DATN-117 | D-03.2 Define approved schema and validation | In Review | Description empty; no child-specific AC. P1/P2 and §5–6. |
| DATN-118 | D-03.3 Define indexes and uniqueness | In Review | Description empty; no child-specific AC. §7 engineering design; conditional P3 history invariant. |
| DATN-119 | D-03.4 Define atomic Task history writes | In Review | Description empty; no child-specific AC. P3 and §8–9. |
| DATN-120 | D-03.5 Confirm whether an outbox is needed | In Review | Description empty; no child-specific AC. A deferral plus bounded source inspection in §10. No new consumer decision requested. |
| DATN-121 | D-03.6 Add isolated initialization and integration tests | To Do | Description empty; no child-specific AC. §11 oracles after P1–P3; execution belongs to implementation. |

No child dependency links were shown. Parent links: blocked by DATN-93 (Done), blocks DATN-97 (To Do), relates to DATN-288 (Done). Tracking completion does not supply missing semantic values. Latest inspected parent comment records PR #30 partial approval; no later detailed approval was visible. This document creates no new Jira issue or accepted policy.

## 3. Dependency matrix: only real D-03 blockers

| Open item | Required by DATN-95? | Current status | Can be technical design? | Required action |
|---|---|---|---|---|
| Project owner, cardinalities, title non-uniqueness, atomic append-only history | Yes, AC1/2 | A, PR #30 / ADR-010 | Already accepted | Preserve, test in implementation; no approval repeat. |
| Which mutations D-03 must persist | Yes, AC2/3 | C, P1 | Choosing a phase's business operation coverage needs explicit selection | Approve create/read foundation slice; otherwise specify the additional operation and its oracle. |
| Exact minimal field presence/requiredness and title validity | Yes, AC1/2 | C, P2 | BSON encoding/validator mechanism is B; business validity is C | Select P2. No unapproved optional field is silently introduced. |
| ObjectId references, BSON timestamps, creation ordinal encoding, unknown-field rejection | Yes, AC1/2 | B, conditional on P1/P2 | Yes, follows accepted ownership/provenance and BE types | Adopt §5–6 through engineering review. |
| Persist Organization or derive it | Yes, correct scope | B: derive through trusted Project; no stored organizationId | Yes for the private slice: avoids a second/stale ownership source without changing access rights | Use §6; any later requirement for historical tenant snapshots/transfer needs an owning decision. |
| Creation event coverage and safe stored content | Yes, AC2/3 | C, P3 | Event encoding is B; retained meaning/coverage is C | Select P3 and its one-event-per-version invariant. |
| History uniqueness and indexes | Yes, AC3 | B conditional on P3 | Yes once the invariant is approved | Derive §7 keys; no operationId uniqueness invented. |
| Internal scoped reads and bounded cursor traversal | Needed for inspection/testing; no public list contract | B, §7 | Yes: internal access pattern, not UI sorting/pagination policy | Verify index definition and representative query; measure production workload later. |
| All 25 transitions, status enum/default and terminal/reopen policy | No for P1's status-free record; yes before a lifecycle field/command is introduced | D: D-02 UNKNOWN | Cannot select business states technically | Keep all edges disabled. D-03 can proceed after P1–P3 without waiting for all 25 cells; any broader scope must explicitly approve its needed state/default subset first. |
| Team/assignee eligibility, reassignment, removal and transfer | No when these fields/operations are omitted | D, unchanged UNKNOWN | Reference encoding would be B; eligibility is domain policy | Defer to assignment/Team use cases; preserve 0..1 if later added. |
| Full Task action matrix, HTTP responses and request idempotency | No for private primitives with no production caller | D | Cannot infer permissions or public retry semantics from Project/IAM | Approve before exposing a caller/endpoint. D-03 tests do not certify real actor authorization. |
| Transaction failure/driver retry for one create | Yes, AC2/3 | B, §9 | Yes: no false success or partial committed pair; no HTTP mapping | Reuse session pattern, test persisted outcomes and ambiguous commit separately. |
| Outbox/durable consumer | No approved D-03 consumer found | A deferral; D if publication later required | No new product vote needed to keep accepted deferral | No outbox/relay/queue in D-03. |
| Delete/archive, retention duration, before/after text snapshots | No for private insert/read slice; no deletion or TTL is added | D | Not an authorization to invent privacy/retention policy | Keep content-minimal events; decide lifecycle/retention before such behavior is introduced or deployed. |
| D-04 runtime, port, Gateway/BFF, health and cross-service access adapter | No for isolated data-foundation artifacts/tests | D; accepted target, inactive runtime | Engineering implementation against ADR-010, not new business architecture | No active registry/provisioning/cutover as a side effect of D-03. Follow owning runtime and DB delivery gates. |
| Measured explain/performance, production data inventory/cutover | No measurement needed to approve a design; required before performance/cutover claims | D verification | Engineering work, no Leader business question | Record real plans later; no measured-speed or live-data assertion here. |

## 4. Minimum use cases and authorization boundary

P1 proposes a private persistence contract, not an API capability grant. For its eventual production caller, Organization/User identity and Project access must come from an authenticated owning contract; arbitrary client IDs, PUBLIC Project metadata, a stored creator/assignee, or role names are insufficient. There is no mock/default-allow runtime path. D-03's disposable tests supply explicit fixtures and test owner predicates; they do not prove live membership revocation or a distributed authorization/write fence. A production caller remains disconnected until that seam is approved and implemented in its owning task.

Every internal read carries the trusted projectId; one Task ID never permits an unscoped read. The private adapter is kept inside the future Task boundary and cannot read IAM models or resolve membership through cross-database joins. Missing scope or unavailable authorization evidence at an eventual caller fails closed before the adapter. Source of truth for Project/User relations remains IAM.

| Use case / D-03 need | Actor, purpose and context | Data, preconditions and persistence constraints | Failure / oracle | Approval status |
|---|---|---|---|---|
| UC-TM-01 List Tasks: internal traversal only | Trusted human context; inspect stored records in one Project. Public actor matrix is deferred. | Read minimal fields; required Project scope; deterministic bounded query Q2 in §7; no mutation/history. | Wrong Project never yields its Tasks; no count/snippet leakage. No HTTP/page envelope chosen. | B design conditional P1; public list API D. |
| UC-TM-02 Create: required mutation | Human-origin creation; Project and creator identity are supplied by trusted server context, not user-writable owner fields. | Insert minimal Task and creation event with same session; all server IDs/metadata preallocated; P2 validity and P3 history. | Valid pair commits; invalid scope/record, either failed write or abort produces no successful partial pair. | C P1/P2/P3; no Task permission code approved here. |
| UC-TM-03 Detail: required internal read | Trusted caller inspects one Task in its Project. | Filter by _id and projectId; owner immutable in this slice; no mutation. | Same ID with different Project returns no record; transport 403/404 unresolved outside D-03. | B design conditional P1; public detail API D. |
| UC-TM-04 Edit: not needed for creation atomicity | Future permitted Member/Leader, exact rights open. | No update/title-edit primitive in the selected slice; current data is not declared permanently immutable. | Future edit requires its own field allowlist, version and history oracles. | D; new operation must obtain its owning contract. |
| UC-TM-05 Assign/reassign: not needed | Future scoped Leader, target eligibility open. | No teamId/assigneeId write. Cardinality approval remains intact for later schema change. | No inference that any member is eligible; no phantom assignment tests. | D. |
| UC-TM-06 Status: not needed | Future approved actor/guard for each enabled edge. | No status field/default or transition command. | All 25 UNKNOWN edges remain disabled; no candidate enum in fixtures. | D: D-02. |
| UC-TM-07 Search/filter: not needed | Future scoped reader. | No text index, search parameters, priority/due filters, counts or search projection. | Internal Q2 is not evidence of a search API or measured workload. | D. |
| UC-TM-08 Work Note: not needed | Future authorized note author; Capture owns note. | No Work Note field/cross-service mutation; logical link boundary retained. | Stale links/access policy remains with owning integration. | D, conditional integration under PR #30. |
| UC-TM-09 Handover: not needed | Future scoped Leader/successor. | No assignment/eligible-state operation or Handover DB access. | External command idempotency/recovery is not inferred from driver retries. | D. |
| UC-TM-10 History: internal evidence read | Trusted scoped inspection; no public history entitlement. | Read creation event by verified Task/Project; no update/delete; §8 projection only. | IDs/version/time agree with Task; text/prompts/secrets absent; no history from wrong Project. | P3 content C, retrieval B; public projection/access D. |
| UC-TM-11 Agent suggestion: not needed | Future authorized human/Agent workflow. | No Agent actor/source or proposal mutation path in this slice. | No Agent authorization or raw-context fixtures are invented. | D, deferred by approved core direction. |

## 5. Field-level dictionary for the proposed D-03 slice

These are a proposed minimal schema contract, not a schema implementation. **P2 selects presence/requiredness and title semantics.** B specifies internal representation without changing business meaning. All fields have exactly one scalar value; arrays/objects/null are rejected unless explicitly specified below. Server fields are not accepted from a public body. No implicit ORM field or fallback business default is allowed.

| Field | Meaning / source of truth | Type and representation (B) | Required / nullable / default | Validation and mutability | Relationship / query | Classification |
|---|---|---|---|---|---|---|
| _id | Canonical Task identity, Task service | BSON ObjectId; server allocates once per logical creation, reused on driver callback retries | Required / non-null / generated, no user default | Valid ObjectId, immutable | Unique Task; Q1/Q2, event taskId | A uniqueness; B representation; P2 complete record selection |
| projectId | The one owning Project, authoritative Project relationship | BSON ObjectId matching existing Project IDs | Required / non-null / no default | Scalar; trusted context; immutable for this slice; Project transfer is not implemented | One Project has 0..many Tasks; Q1/Q2 | A ownership; B representation; P2 record |
| title | Human work summary, Task owns supplied content | Unicode BSON string, preserved exactly | Required / non-null / no default | P2: contains a non-whitespace character; no normalization or narrower business maximum. Document-size failure rejects creation. No edit in this slice. | Non-unique; visible only in scoped reads, no title index | C P2; B encoding |
| createdBy | Human creator provenance, authenticated User identity | BSON ObjectId matching IAM User IDs | Required / non-null / server-derived | Equals trusted actorId; immutable; no copied user profile/role/membership | One creator identity, no access granted by this value | A principle; B encoding; P2 record |
| createdAt | Time the server starts this logical creation | BSON Date, UTC instant, millisecond resolution | Required / non-null / server clock once per operation | Valid finite Date; immutable; clock time is not commit-order proof | No extra time index | A timestamp principle; B semantics for this internal creation; P2 record |
| updatedAt | Last committed mutation time | BSON Date, same instant as createdAt for creation | Required / non-null / same creation value | Must equal createdAt while creation is the only mutation; future update contract changes this rule explicitly | No recent-activity sort promised | A timestamp principle; B creation rule; P2 record |
| version | Internal committed mutation ordinal used in history provenance | BSON numeric integer value 1; validator accepts int32 or double encoding of 1, not string/decimal/long/coercion | Required / non-null / server value 1 | Exactly 1 in this creation-only schema; no CAS, increment, ETag or client version API is specified | Corresponding event taskVersion equals 1 | B: supplies ADR-010 version metadata; P2 record selection |

Title nonblank predicate is a B implementation definition conditional on P2: at least one Unicode code point lies outside W = U+0009–000D, U+0020, U+0085, U+00A0, U+1680, U+2000–200A, U+2028–2029, U+202F, U+205F, U+3000. Application and DB regex use this same explicit set; tests include an empty string, ASCII-only spaces, NBSP-only, tabs/newlines, Vietnamese text and mixed whitespace/text. This does not silently trim or change stored content. The title rule itself is still a Leader decision.

| Omitted candidate | Reason and next owning decision | Category |
|---|---|---|
| organizationId | Derive current Organization from the authoritative owning Project (§6); no duplicate tenant snapshot/query requirement exists for this private slice. | B technical selection; new historical snapshot/transfer requirement would be C. |
| teamId / assigneeId | Creation can have neither under approved 0..1 cardinality; P1 explicitly omits assignment behavior/storage for D-03. Add only with eligibility/reference rules. | P1 omission C; subsequent assignment D. |
| description | No narrative editing operation is needed for this slice. Its format/nullability/limits remain with later edit scope. | P1 omission C; later feature D. |
| status | Avoid choosing the candidate enum/default. A base record is not a runnable lifecycle Task API. Later status introduction needs an approved initial-state rule and migration for existing base records. | P1 omission C; D-02/D-05 follow-up D. |
| priority | No approved ordering/filter requires it here; no enum/default inferred. | D. |
| dueDate | No due-date operation/query; date-only/instant/timezone rules do not affect this slice. | D. |
| operationId on tasks | Creation's internal operation metadata belongs to its event; no persistent API idempotency ledger is selected. | B; external request idempotency D. |
| deletedAt / archivedAt / taskKey / parentTaskId / custom fields | No accepted D-03 deletion, archive, business-key, subtask or extensibility operation. | D; no new fields. |

## 6. Ownership, references and validation layers

**B recommendation: derive Organization rather than persist organizationId.** Project is already the sole owner. All foundation queries have projectId, so a second tenant key adds no required query capability. A stored copy could reduce future tenant-wide query cost or preserve historical context, but introduces stale data on transfers and synchronization ownership. Neither workload nor historical-snapshot policy is selected. The runtime caller must resolve Project-to-Organization and current membership through the owning contract; it cannot trust a client or use cross-database populate. Project unavailable/mismatched means no authorized call. D-03's private fixture-based adapter does not pretend to provide that remote check.

No cascade, transfer, reassignment, automatic clear, deletion or archival is performed. Missing/removed users or Projects do not grant access through stored IDs; records remain until an owning lifecycle/privacy policy defines an action. This is absence of a new mutation, not a promise of perpetual retention. Team/assignee are omitted, so target eligibility/removal does not change a D-03 document. Public execution requires current authorization even after membership removal; its distributed fence is a later seam, not a guarantee from a local Task transaction.

| Invariant | Application / repository | MongoDB / infrastructure | Oracle / limit |
|---|---|---|---|
| P2 shape, scalar types, non-null fields, no unknown fields | Check original input types before Mongoose casting; explicit allowlist, reject unknown keys rather than silently strip; trusted metadata constructed server-side | Strict JSON Schema validation with error action and strict level; additionalProperties false includes _id and every specified field; no implicit __v | Malformed raw collection writes fail too; API statuses remain outside this spec. |
| Title validity and size | Apply P2 predicate without changing content; reject an oversized serialized record before write where measurable | Same W predicate/minimum length and BSON string type; MongoDB document-size ceiling | Same accepted/rejected text cases at both layers; no invented product length cap. |
| Project/User relationship | Server context supplies owner/actor; private query always includes projectId; eventual runtime caller verifies owning contracts | Scalar ObjectIds only; no cross-service foreign key or access policy claimed | Wrong-Project ID reads no record; this test is isolation evidence, not a live Task actor permission matrix. |
| Trusted fields and immutability | Only creation/read methods; no generic update/import of body; server actor/time/version cannot be spoofed | JSON Schema checks values/types but cannot establish their trusted origin or old/new immutability by itself | Verify adapter stores trusted values and never exports a mutation method for ownership/provenance. |
| Same creation timestamp/version and matching event | One preallocated creation context; Task and event written sequentially in one session | Local document consistency validators where expressible; transaction and §7 event uniqueness | Pair equality is checked from committed DB state; schema validation alone is not cross-collection integrity. |
| Append-only history | Private insert/read history adapter, no update/delete API or mutable model export | Task runtime principal should have insert/find only for task_events; provisioning principal is separate | Test update/delete denial with a restricted principal on an auth-enabled disposable replica set. An admin can bypass privileges; this is not tamper-proof history. |

Reuse the maintained service model factory/repository boundaries; do not route Task models through IAM or add a second persistence framework. The future DB PR declares validators/indexes together, disables implicit ORM version fields, and verifies no cast/strip behavior bypasses these invariants. Existing model conventions are implementation examples, not Task business policy.

## 7. Minimal queries, indexes and uniqueness

These internal access patterns are B design, conditional on the chosen slice. They do not freeze public API query parameters, sort order, page envelopes or HTTP errors. Internal traversal requests a limit from 1 to 100 (technical resource bound), with no total-count query. A cursor is a typed ObjectId passed by the private caller; it supplies no access grant.

| Pattern | Exact filter / sort / pagination | Minimal index | Purpose and trade-off |
|---|---|---|---|
| Q1 — inspect one scoped Task | _id = taskId AND projectId = trustedProjectId; no sort | tasks built-in unique _id | A identity correctness; _id lookup plus owner predicate needs no speculative extra compound identity index. |
| Q2 — inspect bounded Project records | projectId equality; after first page, _id greater than last returned ID; sort _id ascending; limit 1..100 | tasks non-unique {projectId: 1, _id: 1} | B performance for a Project-owned cursor scan; ObjectId key order is deterministic, not exact creation/commit chronology. Adds write/storage cost; title duplication remains allowed. |
| Q3 — inspect a scoped Task's history | Verify Q1 first; task_events filter taskId AND projectId; sort taskVersion ascending; bounded limit | task_events unique {taskId: 1, taskVersion: 1}, **only after P3 approves one event per committed version** | B correctness derived from P3; prefix also supports per-Task history. No distinct operationId/eventName/actor/time index needed for the selected query. D-03 only stores version 1; a future mutation/event contract must revise validators before adding other versions. |
| Event identity | Lookup _id as necessary inside reconciliation; always verify expected Task/Project/provenance | task_events built-in unique _id | A default identity key; no new global/business operation-key constraint. |

Do not add unique title, text search, Team, assignee, due-date, Organization prefix, TTL or outbox indexes. A schema field alone is insufficient rationale. P3's extra event-version constraint is proposed consistency protection, not an already accepted operation-id invariant. If P3 is rejected, redesign this row rather than creating it anyway.

Disposable tests inspect index keys/options and exercise duplicate/non-duplicate behavior. A representative Q2/Q3 explain is engineering evidence after implementation; optimizer plan selection depends on fixture cardinality. Do not require a tiny fixture to naturally choose IXSCAN or claim measured production performance from an index definition. Record candidate/hinted plan compatibility separately from unhinted plans, latency and production workload validation (follow-up).

## 8. Minimum creation event contract

P3 selects coverage and retained meaning. B names and encodes the selected fields. This is state plus history, not full event sourcing or a publication message. All fields below are required/non-null, server-derived, immutable and allowlisted; no generic metadata/payload object is added.

| Event field | Representation and value for the proposed slice | Purpose / invariant |
|---|---|---|
| _id | ObjectId allocated once before transaction retries | Stable event identity; no regenerate/publish side effects in callback. |
| taskId | ObjectId matching created Task _id | Task identity; one corresponding history per version under P3. |
| projectId | ObjectId matching Task projectId | Protected owner scope for queries; not another owner. |
| eventName | String TASK_CREATED (internal spelling, B) | P3 creation classification only. No future event vocabulary enabled. |
| actorType / actorId | USER / ObjectId equal to createdBy | Human identity provenance; no copied roles/profile or implicit permissions. |
| source | HUMAN (internal spelling, B) | Human-origin operation in P1; no Agent/service actor policy inferred. |
| changedFields | Exact array [projectId, title, createdBy, createdAt, updatedAt, version] of field-name strings | P3 names-only creation metadata; excludes title values and unrestricted snapshots. |
| taskVersion | Numeric integer 1, same accepted int32/double encoding as Task version | ADR-010 provenance; one local aggregate version, no global ordering/CAS contract. |
| occurredAt | BSON Date, identical to Task createdAt | Operation timestamp; not an exact commit timestamp or cross-Task order. |
| operationId | Server-generated UUID v4 string, allocated once per logical create | Trace callback retry/reconciliation; no public replay-key namespace, retention or unique index. |
| correlationId | Trusted server requestId if present and matching existing [A-Za-z0-9._-]{1,128}; otherwise server UUID | Reuse [request-id middleware convention](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/src/common/http/request-id.middleware.ts), no new public header. Correlation is not identity/authorization. |

No full title/description, before/after text, raw prompts, unrestricted Agent context, tokens, cookies, email/IP/user-agent or profile copies are stored/logged by this proposed event. It records only the safe identifiers/provenance and field names selected above. No TTL or retention duration is chosen. A security/compliance audit for denied/failed attempts is a separate policy; failures do not create a successful Task mutation event. Future mutations/Agent provenance/retention need an explicit extension rather than a generic writable event sink.

## 9. Transaction, ordering and failure contract (B engineering design)

Use the existing startSession → withTransaction → finally endSession pattern. Preallocate Task/event IDs, time, operationId and correlation context once; keep the callback free of HTTP, Redis, email or logging of content. Run Task insert then event insert sequentially with the same session/client in the same owned DB. Return success only after the transaction helper confirms commit. No nested/parallel transaction work and no outer blind replay loop.

For these preinitialized collections, select primary read preference, snapshot read concern and majority transaction commit write concern. Do not set write concern on individual writes. Initialization/validator/index DDL runs separately before the transaction; no runtime implicit collection creation. Use the supported MongoDB 7 replica-set test environment. Exact test-only timeouts may be bounded without creating a public HTTP SLA.

The pinned BE lockfile resolves mongodb 6.20.0 with Mongoose 8.x. Its convenient transaction API handles labelled transient-transaction and uncertain-commit retries. Preserve those semantics; a callback error must propagate, not be swallowed as success. Verify actual dependency versions in the implementation PR. No claim is made that a network failure always proves rollback.

| Failure | Internal result / persisted-state oracle | Retry and boundary |
|---|---|---|
| Invalid record or missing trusted scope | No transaction/mutation; no successful creation event | Deterministic invalid-input/scope outcome; HTTP status/body is a later API decision. |
| Task insert fails before a successful commit | Transaction fails; no new committed event; pre-existing data remains | Distinguish duplicate identity from title duplicates. Never interpret an arbitrary duplicate key as a successful prior operation. |
| Required event insert fails after provisional Task insert | Transaction aborts; neither newly inserted document is committed | Rethrow so the helper cannot commit a Task without history; no fallback to history-less success. |
| Abort after both provisional inserts | Neither new document is visible as committed; existing data unchanged | No history from an aborted attempt; inspect persisted state after abort. |
| Transient failure / callback replay | Same logical IDs/time/provenance are reused; eventual confirmed commit gives exactly one Task/event pair | Driver handles labelled retries; test forced callback replay against persisted counts, not mock call counts alone. No business-level request replay behavior is implied. |
| Commit result still ambiguous when helper exits | Report an internal uncertain outcome with safe operation identifiers; never report success or definitive rollback from the exception alone | Do not issue a fresh create with new IDs. Reconcile expected IDs/content using primary majority reads (one snapshot for pair inspection). Matching pair proves committed state; mismatch/partial pair is an integrity incident; absence at one instant does not prove an in-flight commit can never finish. Keep uncertainty unresolved until definitive evidence. Durable cross-request recovery is outside P1 and required before exposing automatic retries. |

Only creation ordinal 1 exists, so no D-03 concurrent update/CAS or cross-Task event-order promise is necessary. Concurrent creates with different server IDs and the same title are allowed. Concurrent inserts of the same Task identity cannot create two Tasks; this is identity uniqueness, not approved client idempotency. Timestamp/ObjectId order is not substituted for D-02 concurrency decisions.

## 10. Outbox and runtime assessment

At inspected BE revision fc7d0be, a source search for continuum_task, task_events and Task event names across src/scripts/test found no Task producer/consumer; matches were only planned-owner exclusion/validation tests and migration documentation. Existing generic outbox collections in other services and optional notification/AI patterns in ADR-010 do not establish a named D-03 durable consumer.

**A: preserve outbox deferral.** D-03 stores local history, publishes nothing and creates no outbox/relay/queue. No new Leader decision is necessary to keep that direction. Consequence: no external delivery, replay, ordering or eventual notification guarantee is claimed. A later named consumer must define its approved delivery purpose/owner and semantics before a transactional outbox is introduced; history cannot be used as a delivery queue by assumption.

For D-03 implementation, keep Task persistence definitions private and test with a unique disposable database override. Reject live/default/other-service DB targets in test initialization; use no continuum_db fallback. Declare continuum_task as the intended owner without registering an active service or writing to it on the developer cluster. A DB companion PR includes schema/validator/index/init artifacts and tests; actual runtime inventory, service entrypoint/routing and live provisioning/cutover are owned by D-04 and the environment workflow. No Task business seed is needed. Inspect actual legacy data before any later move; no live-data absence is inferred from source absence.

## 11. Acceptance and executable-oracle matrix

All rows are **test specifications, NOT RUN**. Pending P decisions are stated explicitly; no fixture may silently select an UNKNOWN business value. After approval, real persisted-state replica-set tests establish AC3; passing document checks is not a substitute.

| Oracle | Parent / subtask | Concrete verification | Approval dependency |
|---|---|---|---|
| O1 Ownership/init | AC1/3; 116/121 | Repeat disposable initialization twice; only selected Task-owned collections, validators and indexes exist; no IAM/other DB write or shared fallback | A/B; P1/P2/P3 for selected definitions. |
| O2 Valid base creation | AC1/2/3; 117/119/121 | Insert selected seven fields through private primitive; read committed Task and matching safe creation event | P1/P2/P3. |
| O3 Shape and trusted metadata | AC1/3; 117/121 | Raw DB inserts missing each persisted required field, or containing null/wrong types/extra keys, reject. Private command tests reject missing/invalid title and spoofed server-field inputs; the trusted constructor supplies IDs/actor/time/version rather than requiring them in user input. Verify original input types before ORM casts. | P2; accepted trust boundary. |
| O4 Title | AC1/3; 117/121 | Empty/all-W strings rejected; mixed W/text and Vietnamese accepted without normalization; large but engine-valid title has no invented business cap; oversized BSON fails without history | P2. |
| O5 Unique identity / non-unique title | AC2/3; 118/121 | Distinct Task IDs with identical title commit; duplicate _id rejects and does not add history; existing pair unchanged | A plus P1/P3. |
| O6 One owner / scope isolation | AC1/2/3; 117/121 | Project array/null rejected; a valid Task ID queried under another Project returns no Task/history; query always carries owner predicate | A/B, P1/P2; does not certify runtime permissions. |
| O7 Event invariant/index | AC2/3; 118/119/121 | Duplicate taskId/taskVersion event rejects after P3; persisted IDs/actor/time/version/change-name allowlist match; sensitive values absent | P3. |
| O8 Atomic success | AC2/3; 119/121 | Both documents committed together; observer cannot see an acknowledged half-creation | A atomicity, P1/P3 shape. |
| O9 Failure rollback | AC2/3; 119/121 | Inject Task failure, event failure after Task insert, and abort after event insert; inspect zero new committed documents and unchanged existing rows | A/B with P1/P3. |
| O10 Retry / uncertain commit | AC2/3; 119/121 | Labelled transient failure eventually yields one matching pair; lost commit response never yields a false success/rollback claim or second pair; reconcile confirmed/uncertain states separately | B §9; no HTTP/idempotency assertion. |
| O11 Append-only | AC2/3; 119/121 | No history mutation methods; with runtime-equivalent restricted principal, update/delete fail and existing event is unchanged | A/B; auth-enabled disposable test required for DB-privilege proof. If unavailable, classify that check BLOCKED, not PASS. |
| O12 Index/query compatibility | AC3; 118/121 | Inspect exact keys/options; traverse Q2 with small limits and interleaved other-Project fixtures, stable cursor with no cross-scope records; record explain with representative cardinality | B conditional slice/invariant. Optimizer choice and production performance are separate follow-ups. |
| O13 Exclusions | AC2/3; 120/121 | No status/default/priority/assignment/delete/TTL/outbox field or public caller in selected schemas/modules; creation enum only in history, not a Task lifecycle state | P1/P2/P3; A outbox deferral. |

These tests can run with private Task adapters/models and disposable DB connections. IAM/Project regression tests protect existing behavior when implementation arrives; they cannot prove Task history atomicity. Full Task API/state-transition E2E, membership/write-race behavior and D-04 routing tests belong to their owning tasks. Runtime dependency absence does not force a speculative business oracle.

## 12. Readiness at the proposal revision, approval binding and follow-ups

**Result at reviewed revision 6628c60: C — BLOCKED — EXPLICIT PRODUCT DECISIONS REQUIRED.** The product blockers at that time were exactly P1 (D-03 mutation/field exclusions), P2 (minimal record and title validity), and P3 (creation history coverage/projection/invariant). No accepted independent write subset could yet satisfy its own AC: even creation still required P2/P3. The successor approval closes those product blockers for the selected slice; initialization of an empty DB alone still would not close DATN-95.

Once P1–P3 are explicitly approved, the defined slice is **READY FOR D-03 IMPLEMENTATION** using the B designs and tests above, subject to normal source safety, scoped guide reconciliation and supported test infrastructure. This is not approval of the complete Task V1 API. If the Leader selects a narrower subset instead, record its exact AC and exclusions and use **PARTIALLY READY — IMPLEMENTABLE SUBSET IDENTIFIED** only when that subset has a complete oracle.

Do not require already-passing Task implementation tests before authorizing implementation: accepted/testable oracles are the start gate; actual passing implementation tests, review and evidence are the completion gate. Measured production performance, live deployment, all 25 transitions and all optional V1 capabilities are not hidden start gates for this selected data foundation.

Approval record for each P row must identify: accepted/amended/rejected/deferred; exact document commit; any changed value; approver/authority/date/evidence; AC and O-row mapping. Update owning field/history definitions or explicitly identify this accepted delta as their scoped implementation authority; reconcile conflicting proposal rows without overwriting historical review evidence. Then synchronize the relevant SAGE pointers without changing its source baseline unless separately authorized.

Jira: preserve DATN-116 Done, DATN-117–120 In Review, DATN-121 To Do, and DATN-95 In Progress while decisions are reviewed. In Review means reviewable material, not approved policy or implemented behavior. Add the delivery PR and the P1–P3 mapping to the parent; do not remove dependency links or mark schema/tests Done from documentation delivery. D-04/Task API, assignment/Team, lifecycle/D-02, Handover, Work Note, Agent, retention and consumer work remain existing follow-ups; no new issue is required merely to duplicate them.

## 13. Technical research and scoped work record

Official sources checked 13/10/2026, selected for the configured MongoDB 7.0 and the pinned Node driver 6.20.0. They guide B designs and cannot approve P decisions.

| Source | Finding applied / limitation |
|---|---|
| [MongoDB 7 data modeling](https://www.mongodb.com/docs/v7.0/data-modeling/) | Access patterns drive representation; separate growing history and use logical cross-service references. Does not establish DATN field/cardinality policy. |
| [MongoDB 7 schema validation](https://www.mongodb.com/docs/v7.0/core/schema-validation/), [JSON Schema](https://www.mongodb.com/docs/v7.0/reference/operator/query/jsonschema/) | DB validation can reject bad writes and closed shapes. It cannot establish trusted actor origin, enforce cross-service foreign keys or append-only policy by itself. |
| [MongoDB 7 compound indexes](https://www.mongodb.com/docs/v7.0/core/indexes/index-types/index-compound/), [unique indexes](https://www.mongodb.com/docs/v7.0/core/index-unique/) | Prefix/order matters; uniqueness protects a chosen key invariant. This supports Q2 and conditional Q3, not title uniqueness or measured performance. |
| [MongoDB 7 transactions](https://www.mongodb.com/docs/v7.0/core/transactions/), [production constraints](https://www.mongodb.com/docs/v7.0/core/transactions-production-consideration/) | Use the configured replica-set transaction with deliberate session/read/write concerns; initialize DDL before it. Configuration alone does not prove a live replica set or rollback test. |
| [Node driver 6.x transaction API](https://www.mongodb.com/docs/drivers/node/v6.x/crud/transactions/) | Same session on each awaited operation; convenient API handles labelled transaction/commit retries; no parallel operations in a transaction. §9 combines this mechanism with a DATN-scoped safe-outcome design, not a public retry contract. |
| [MongoDB 7 limits](https://www.mongodb.com/docs/v7.0/reference/limits/) | BSON document limit is 16 MiB including fields/overhead; it is an engine limit, not an approved title-specific product maximum. |
| [AWS transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) | Addresses database/message dual-write delivery. No such required D-03 consumer was found; preserve conditional deferral rather than treating history as a queue. |

Scope / authorization: user request “D-03 — TASK V1 CONTRACT DELTA CLOSURE”; documentation and research only. Read Product Docs, relevant local SAGE policy/authority, pinned BE architecture/persistence and Jira DATN-95/116–121. Write only this new Product Docs follow-up and its README link. No backend/FE/SAGE/live-data write; no PR approval/merge or team message. Author/technical reviewer: Codex; final-diff self-review is disclosed, not independent human approval.

Local SAGE evidence provenance (SHA-256 of inspected files; not a selected baseline or a Git-hosted approval):

| Workspace-relative file | SHA-256 |
|---|---|
| .sage/project-context.md | 0f25e947e03e03e0d249174b98afb3ae175043feb81d0afd13d03a0bdcfde780 |
| .sage/config.yaml | 62e38d93d9c7a6fa4bbc8cb7734c237a85524f2f09a115477a75508ef53ab6ce |
| docs/adr/ADR-003-database-per-service-persistence.md | 7160b9498c904f9caf9d0cf309eb3589f1a690b498e45fe144f61aa5933f8ad0 |
| docs/specs/SPEC-001-MONGODB-PERSISTENCE.md | ea58820aca62899487eaf44d083f141fc740cd2848b7922f6cf00cc75923305d |

These root artifacts are referenced at their local snapshot, not copied into product authority. SPEC-001's illustrative HTTP failures, audit shapes and migration tooling are not automatically Task requirements. Existing accepted topology/provenance is preserved; runtime/source/approval evidence must be refreshed at implementation time. Research, this design, document validation, Jira tracking and a merged PR each have separate meanings.
