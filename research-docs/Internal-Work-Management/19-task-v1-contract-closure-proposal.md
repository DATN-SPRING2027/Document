# DATN-95 — Task V1 data foundation: contract closure proposal

> **Status: PROPOSED — NOT APPROVED.** This is a review package for the authorized DATN product/domain and technical decision owners. It is not an implementation contract, does not approve Task fields or lifecycle policy, and does not unblock D-03.
>
> **D-03 implementation readiness: BLOCKED / CONTRACT AUTHORITY REQUIRED.** No Task schema, index, migration, runtime database, or application code is created by this document.
>
> **Prepared:** 13/10/2026 (Asia/Bangkok). **Basis:** current Product Docs `origin/main` at `b92d09f8b3725e0145b6d937664160064a23f992`, D-01 R5 and D-02 R1 artifacts, accepted ADRs, current DATN-BE main evidence, and Jira DATN-95/117–121 inspection.

This document turns the existing Task V1 proposals into a decision-ready, testable recommendation. Every recommendation below remains a proposal until an identified approver with applicable authority records an answer in the owning contract or decision record. A document merge, Jira status, technical review, or SAGE traceability entry alone is not product approval.

## 1. Authority and sources of truth

| Concern | Authoritative source | Current finding and limit |
|---|---|---|
| Product/domain Task contract | `product_docs` owning use-case, contract, and decision artifacts | D-01 is a working contract plus explicit UNKNOWNs. D-02 documents candidate states, edges, and reliability oracles. Neither authorizes field-level persistence choices. |
| Governance and traceability | DATN `.sage` context, constitution, governance model, inventory, and decision registers | The inspected SAGE context has `baseline.active: null`. SAGE records evidence and routes decisions; it does not approve product policy. The named person/role authorized to approve each Task decision is not established in the sources inspected. |
| Runtime implementation | DATN-BE source and its accepted architecture decisions | DATN-BE [`origin/main` at `fc7d0be`](https://github.com/DATN-SPRING2027/DATN-BE/tree/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a) has no Task service implementation, Task collections/models/indexes/migrations, active Task database in `SERVICE_DATABASES`, Task API, or Task integration tests. ADR-010 still establishes `continuum_task` as the accepted target owner. Existing Project and membership decisions constrain authorization but do not define the Task action matrix. |
| Work tracking | Jira DATN-95 and DATN-117–121 | Jira identifies scope/dependencies. The inspected child issues have empty descriptions and no child-specific acceptance criteria; the parent DATN-95 acceptance criteria govern. Jira is not evidence that the contract has been approved. |

The request authorizes preparation of this proposal. It does not identify an individual approver or authorize this document to turn proposals into accepted policy. Before approval, the Leader must be identified by name/role, the scope of that authority recorded, and the answer linked to an owning document revision. The current evidence does not support naming a person. **Unknown authority must remain unknown.**

### 1.1 Evidence labels

- **DECISION:** accepted DATN constraint with a traceable source.
- **FACT:** state observed in a repository or Jira at the revision/date recorded.
- **DESIGN:** technical consequence or option, not product policy.
- **INFERENCE:** recommendation derived from accepted boundaries; requires review.
- **UNKNOWN:** no accepted answer was found in the inspected evidence.
- **CONFLICT:** current sources appear to disagree; resolve before implementation.

## 2. Accepted baseline and exact blockers

### 2.1 D-01 review result and P2 finding

[DATN-93](https://trankimthang0207.atlassian.net/browse/DATN-93) is Done because its acceptance allowed either an approved contract or a precise blocker list. Merged documentation-only [PR #22](https://github.com/DATN-SPRING2027/Document/pull/22) records the working contract, accepted B1–B10 boundaries, and Q1–Q9 UNKNOWNs. It did not add application code and did not approve the full Task V1 contract. D-02 PR #26 continues that boundary: it records candidate lifecycle/reliability decisions, with zero enabled transitions and every one of the 25 candidate state-pair cells UNKNOWN.

The R5 [review comment](https://github.com/DATN-SPRING2027/Document/pull/22#pullrequestreview-5410654477) reported a P2 wording issue in [the D-01 worksheet](14-task-v1-review-worksheet.md): **“Accepted transition matrix: tất cả 25 cells vẫn UNKNOWN (Q4/Q5/Q7).”** The word “Accepted” implies approval even though the cells are UNKNOWN. The separate documentation correction will rename only the heading to neutral review wording; it will not change any state, transition cell, or decision semantics. The review finding is not product approval.

### 2.2 Accepted constraints reused here

| ID | Accepted boundary | Evidence and limit |
|---|---|---|
| B1 | Continuum Task API is the canonical Task source; Task operational records use MongoDB; Jira is not imported, synchronized, or a second writable source in the MVP. | [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md); does not approve Task fields or workflows. |
| B2 | Task service runs as an independent NestJS process in the existing DATN-BE repository; no new Task repository or MongoDB cluster. | [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md); accepted target boundary, not proof that runtime is provisioned. |
| B3 | Browser access goes through the BFF/Gateway. Other services use Task API or an approved event contract; they do not access Task collections directly. | [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md); no current Task route or event consumer is identified. |
| B4 | Target logical database is `continuum_task`; Task Service owns `tasks` and append-only `task_events`. A Task mutation and its corresponding history record commit atomically. A same-transaction outbox is conditional on a durable publication requirement. | [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md); does not define exact event fields, which mutations emit history, retention, or an outbox consumer. |
| B5 | A Work Note may hold an optional logical `taskId`; a Task is context, not verified knowledge or an independent SAG source. | [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md); detailed link behavior remains to be approved. |
| B6 | Handover uses Task API and keeps its own record. Assignment uses an operation ID/idempotency with retry or compensation because the services do not share a database transaction. | [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md) and [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md); does not define the Task operation-key contract or all Handover eligibility rules. |
| B7 | Agent work is a proposal; an authorized human confirms before a canonical Task mutation. Do not persist full prompts or unrestricted raw AI context in history. | [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md); Agent feature scope remains undecided. |
| B8 | Active Organization Membership establishes organization context; role assignment alone is insufficient. Scoped authorization and ACL apply. ADMIN/PLATFORM_OPERATOR do not gain implicit access to protected Task content. | [Actor and permission baseline](../02_ACTORS_ROLES_AND_PERMISSIONS.md) and [Organization/Project access readiness](../Workspace/00-organization-and-access-contract-readiness.md); exact Task action matrix is UNKNOWN. |
| B9 | A Project creator is an ordinary Project MEMBER and has documented member rights to create/edit Tasks when the API exists. | [Accepted Project creator decision](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/docs/decisions/project-creator-member-bootstrap-v1.md); does not grant edit rights to every Task or bypass field/Team scope. |
| B10 | Task access requires active Project membership in the applicable scope. PUBLIC Project metadata or Organization ADMIN metadata access does not grant Task content access. | [Accepted Project Access decision](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/docs/decisions/project-access-visibility-v1.md); does not decide assignment cleanup after access revocation. |

In inherited D-01 R5 references below, **S3** means the [Task V1 use-case proposal](12-continuum-task-management-use-cases.md), and **S4** means the [Task storage boundary proposal](../../database-design/12_TASK_MANAGEMENT_SCHEMA.md). Their field, state and relationship details remain proposals.

`continuum_task` is an **approved target**, not an active runtime database observed on DATN-BE main. It is absent from the active `SERVICE_DATABASES` inventory and there is no Task implementation to validate against. Current MongoDB deployment configuration uses a replica set, which supports multi-document transactions; that platform fact does not provision `continuum_task` or approve a schema.

### 2.3 D-03 parent acceptance and child mapping

DATN-95 requires: (1) approved data shape and Task DB ownership, (2) constraints/atomicity derived from approved use cases without speculative fields or a legacy `continuum_db` fallback, and (3) disposable tests that verify indexes, persistence, and failure behavior. Current work can prepare the decisions and test plan; it cannot satisfy approved-contract or implementation-test evidence.

| Jira item | Inspected scope/status | Proposal mapping | What still blocks its acceptance |
|---|---|---|---|
| [DATN-95 — D-03 Task Data Foundation](https://trankimthang0207.atlassian.net/browse/DATN-95) | Parent acceptance criteria require approved shape, constraints, Task DB ownership, and disposable persistence/index/failure tests. Status was In Progress for contract-resolution work when checked. | This proposal supplies a reviewable data/use-case/index/history/outbox recommendation. | Named approval and accepted contract revision; then Task DB/runtime implementation and disposable tests. In Progress does not mean persistence is unblocked. |
| [DATN-117 — D-03.2 Define approved schema and validation](https://trankimthang0207.atlassian.net/browse/DATN-117) | To Do; description and child-specific AC empty when inspected. | §5 data dictionary, §6 relationships, §7 validation, decision rows D2–D5. | Leader-approved field presence/type/null/default/limits, relationships, and validation; then schema implementation evidence. |
| [DATN-118 — D-03.3 Define indexes and uniqueness](https://trankimthang0207.atlassian.net/browse/DATN-118) | To Do; description and child-specific AC empty when inspected. | §8 query workload, candidate indexes, uniqueness boundaries, and verification plan. | Approved V1 queries and invariants; indexes derived from those queries; disposable index tests against the implementation. |
| [DATN-119 — D-03.4 Define atomic Task history writes](https://trankimthang0207.atlassian.net/browse/DATN-119) | To Do; description and child-specific AC empty when inspected. | §9 distinguishes accepted atomicity from proposed event schema and operation coverage. | Accepted history/event policy and transaction behavior; implementation and failure-injection evidence. B4 is accepted but is not proof that code exists. |
| [DATN-120 — D-03.5 Confirm whether an outbox is needed](https://trankimthang0207.atlassian.net/browse/DATN-120) | To Do; description and child-specific AC empty when inspected. | §10 recommends deferring an outbox unless an identified durable V1 consumer is approved. | Explicit decision on consumer/publication requirement; if required, its delivery, retry, ordering, idempotency, and retention contract. |
| [DATN-121 — D-03.6 Add isolated initialization and integration tests](https://trankimthang0207.atlassian.net/browse/DATN-121) | To Do; description and child-specific AC empty when inspected. | §11 gives a contract-backed test matrix and execution gate. | Approved contract plus actual Task initialization/persistence implementation. No Task integration tests have been run by this documentation task. |

DATN-116 is already Done for Task collection ownership. Its completion is consistent with B4/ADR-010 and does not close the remaining schema, index, history, outbox, or test decisions. No subtask is marked Done by this proposal.

## 3. Proposed V1 use-case inventory

The existing use-case document proposes UC-TM-01–11. The following recommendation includes the core operational list/create/detail/edit/assignment/status/search/history slice and the already accepted Work Note/Handover boundaries. This inventory is **PROPOSED — NOT APPROVED**. An actor listed below is a candidate, not a granted permission. Every use case still needs an accepted scope and actor/action/scope mapping before code or fixtures use it.

| Use case | Actor and goal | Context and preconditions | Data read/mutated | Ownership and authorization | Consistency/history | Candidate acceptance criteria | Source and state |
|---|---|---|---|---|---|---|---|
| UC-TM-01 List project Tasks | Project MEMBER or TEAM_LEADER locates current work; SUCCESSOR may see only explicitly assigned/handed-over context. | One Project selected; caller has current Organization and Project access; exact filters, pagination, disclosure, and Team behavior are unresolved. | Read Task summaries and candidate filters: status, assignee, priority, due date, title. No mutation. | Task API scopes every query to Project and current membership/ACL. Do not treat PUBLIC metadata, ADMIN, or a stored assignment as an access grant. | A list read creates no Task history. If this query is eventually an event consumer source, that publication is a separate decision. | Results cannot include another Project; current authorization is checked; filters/sorts are bounded; response fields match approved projection; empty page behavior is specified. | UC-TM-01/07; B3/B8/B10. Scope/permission/query contract UNKNOWN. |
| UC-TM-02 Create Task | Project MEMBER creates a work item; Project creator rights from B9 apply when the API exists. | Active Organization context and active Project membership; supplied project must be in that scope. Initial status, team, assignee, required fields, and member self-assignment remain UNKNOWN. | Create canonical Task; candidate server-owned creator and timestamps. | Task service derives actor/context from trusted identity; it does not trust client `organizationId`, `createdBy`, role, or membership claims without the accepted trust contract. | Task and corresponding creation history, if creation is included in the history policy, commit atomically under B4. Exact create-event requirement UNKNOWN. | Invalid or cross-scope input creates no Task; successful create returns the approved representation; Task and required history either both commit or neither does. | UC-TM-02; B4/B8/B9. Requiredness, defaults, actor/action contract UNKNOWN. |
| UC-TM-03 Read Task detail | Member/Leader reads a Task; successor reads only eligible assigned context. | Task belongs to one Project under the caller's active Organization context; current Project/Team/ACL scope must authorize the read. | Read Task detail and approved related references; no mutation. | Task service is canonical. Work Note/Handover references do not grant access by themselves. | No Task mutation/history. Access audit requirements, if any, belong to the security/audit decision. | Cross-Project or unauthorized IDs disclose no protected content; exact HTTP 403/404 behavior is an API decision, not inferred here. | UC-TM-03; B3/B5/B6/B8/B10. Projection and disclosure UNKNOWN. |
| UC-TM-04 Edit Task fields | Eligible Member/assignee or scoped Leader edits approved editable fields. | Existing Task belongs to a Project in the caller's active Organization context; exact editable fields, creator/assignee rights, and optimistic concurrency contract remain UNKNOWN. | Candidate title, description, priority, due date, and team; only fields approved for V1 may be changed. | Project/Team scope and current ACL are checked by Task API. B9 does not authorize editing arbitrary Tasks or every field. | Mutation and corresponding `task_events` record commit atomically. Field-level before/after and version rules remain UNKNOWN. | Reject unsupported/read-only fields and stale writes according to approved contract; failure leaves Task/history unchanged. | UC-TM-04; B4/B8–B10. Q3/Q5/Q7/Q8 UNKNOWN. |
| UC-TM-05 Assign/reassign | A scoped Leader assigns or transfers responsibility; Handover may request a transfer through Task API. | Source Task is in the Leader's active Organization/Project context; target user must satisfy approved Organization/Project/Team eligibility. Removal, inactivity, and teamless behavior remain UNKNOWN. | Candidate `assigneeId`; possibly Team context. | No client-written assignee without authorization. Handover cannot mutate Task DB directly. | Assignment mutation and corresponding history atomic. Handover's operation ID/idempotency and retry boundary follows B6; exact Task key contract UNKNOWN. | Ineligible/cross-scope target leaves Task unchanged; retry cannot cause duplicate assignment; authorization is current at the accepted commit boundary. | UC-TM-05/09; B4/B6/B8/B10. Q2/Q5/Q7/Q8 UNKNOWN. |
| UC-TM-06 Change lifecycle status | Current assignee or scoped Leader may issue a transition if that edge is explicitly approved. | Task is in a Project within the caller's active Organization context; source/target states, initial state, transition guards, reason, terminal behavior, and Handover eligibility are all unresolved. | Candidate status and reason metadata; only after D-02 selects each edge. | Exact actor × action × resource matrix must be approved. An UNKNOWN edge remains disabled. | Mutation and required history are atomic. Version/CAS/replay rules await D-02. | No UNKNOWN transition is enabled; every accepted edge has positive and negative oracle coverage; errors do not mutate Task/history. | UC-TM-06; B4/B8/B10; D-02. All 25 candidate cells remain UNKNOWN. |
| UC-TM-07 Basic search/filter | Authorized Member/Leader finds a Task by approved Project-local filters and title search. | One Project in the caller's active Organization context; exact text-search, sort, pagination and Team behavior unresolved. | Read Task summaries; likely filters include lifecycle, assignee, priority, due date, title. | Every search applies current Project access and does not leak through counts/snippets. | Read-only; no Task history. | Query parameters are bounded and documented; indexes support approved workload; unauthorized scope yields no protected records. | UC-TM-07; B3/B8/B10. Search/API contract UNKNOWN. |
| UC-TM-08 Link Work Note | Member optionally links one Work Note to a Task for context. | Work Note remains valid without a Task; Task belongs to a Project in the caller's active Organization context. Capture's exact note-scope relationship remains with its owner. | Work Note stores optional logical `taskId`; Task is read through Task API when needed. | Validate Task access at link/read time. A stale logical reference cannot bypass Task ACL. | No cross-service transaction is implied. Capture/Task consistency and link-removal semantics require an owning decision. | Zero or one Task per Work Note and multiple Work Notes per Task are existing proposals, not accepted cardinality; use only after approved. | UC-TM-08; B5. Link cardinality and stale-reference behavior UNKNOWN. |
| UC-TM-09 Handover of open Task | Team Leader selects an eligible Task; successor receives only permitted context. | Handover item references a Task in the Leader's active Organization/Project context; successor receives only the approved Task scope. Eligible states and membership-removal behavior remain UNKNOWN. | Handover stores logical `taskId` and handover state; Task Service owns canonical assignee. | Handover calls Task API with stable operation identity; no direct database access or second writable Task copy. | Cross-service operation cannot be one local transaction. B6 requires idempotency and retry/compensation boundary; reconcile details remain unresolved. | Lost response/retry does not silently assign twice; package does not widen successor access; recovery has an identified owner. | UC-TM-09; B3/B6/B8/B10. Eligibility and operation contract UNKNOWN. |
| UC-TM-10 View important history | Authorized actor sees approved changes for a Task. | Task belongs to a Project in the caller's active Organization context; the same Project/Task ACL and successor visibility boundaries apply. | Read append-only `task_events`; no mutation. | History is protected Task content. No implicit ADMIN/platform access. | Event chronology/order and retention must be approved; events are not a replacement for compliance audit. | Only approved safe fields are returned; no prompt/raw context; access is scoped; ordering/pagination and retention are explicit. | UC-TM-10; B4/B7/B8/B10. Event schema/policy UNKNOWN. |
| UC-TM-11 Agent suggestion | Agent prepares a candidate edit for human review. | Future capability unless Product explicitly includes it in V1; the requesting user's active Organization/Project access must authorize Task context first. | Draft/proposal separate from canonical Task; a confirmed authorized human command may mutate Task. | Agent has no direct database or self-approval permission. | Accepted B7 requires human confirmation and limits stored context. Whether this use case belongs to V1 is unresolved. | Agent cannot commit autonomously; proposal and confirmer provenance are safe and authorized. | UC-TM-11; B3/B7. V1 inclusion UNKNOWN; recommended FUTURE. |

### 3.1 Recommended V1 scope boundary

**Proposal:** prioritize project-local list, create, detail, limited edit, assignment, approved lifecycle commands, basic filters, and limited history, with optional Work Note and Handover integration only where their owners approve the exact contract. The proposal does not assume Kanban is core; the existing use-case document treats it separately from the core list. UC-TM-11 is future; human confirmation remains an accepted boundary if it is ever included. Do not infer subtasks, recurring tasks, workflow automation, external event consumers, configurable custom fields, or other capabilities absent from the selected and approved use cases.

Rationale: this matches the minimal internal tracker proposed in the current use-case document and avoids importing Jira's fields or workflow. It still requires explicit Leader selection. Do not create tests or schema fixtures that treat this recommended scope as accepted.

## 4. Ownership and relationship proposal

| Relationship | Recommended cardinality/reference | Scope and integrity | Lifecycle/deletion | Authorization impact | State |
|---|---|---|---|---|---|
| Organization → Project → Task | One Task belongs to exactly one Project. Project belongs to one Organization under the accepted domain model. Project is the Task resource owner; Organization is the parent/context. | Candidate stored `projectId` is canonical owner. `organizationId`, if stored, is a denormalized immutable context value derived from the trusted Project relationship, never accepted from the client. Validate that the two IDs agree through the owning Project contract/API. MongoDB cannot enforce a foreign key to another service's database. | Project deletion/transfer and Task retention/transfer behavior need owning lifecycle decisions. No cascade behavior is inferred. | All Task reads/writes require current scoped Project access under B8–B10. | Project ownership is DECISION at domain boundary; exact Task field shape and org denormalization are PROPOSED/UNKNOWN. |
| Project → Task | One Project has zero or more Tasks; each Task has one Project. | Store a stable logical Project ID; do not embed the full Project document or copy mutable Project data. Project existence and caller access are checked against the authoritative Project contract. | What happens to Tasks if Project is archived/deleted/transferred is UNKNOWN. | Project membership and Task ACL are re-evaluated; PUBLIC metadata alone does not grant Task access. | Recommended; cardinality still requires Task contract approval. |
| Project → Team → Task | Candidate zero or one `teamId` per Task; any selected Team must belong to the same Project. Teamless Tasks may be useful but are not approved. | Task may store a logical Team ID. Validate current parent relationship using Team/Project owner. Do not accept cross-Project or multi-Team references. | Team deletion, movement, membership loss, and reassignment are UNKNOWN. | Team must not expand Project access; exact Team action scope requires Q5 approval. | PROPOSED; cardinality and teamless behavior UNKNOWN. |
| User → Task creator | Candidate exactly one server-derived creator identity. | Store identity only; no copied role/membership as authorization truth. | User deletion/anonymization/retention is UNKNOWN. | Creator ID alone is not authorization; B9 is limited to documented ordinary Member rights. | PROPOSED; requiredness and identity representation UNKNOWN. |
| User → Task assignee | Candidate zero or one current assignee. | Validate target eligibility in the correct Organization/Project/Team scope through accepted identity/access contracts. Avoid embedding mutable user profile. | Inactive/removed user, project removal, and reassignment policy are UNKNOWN; do not silently clear/transfer. | Stored assignee alone must not preserve access after membership/ACL revocation. | PROPOSED; cardinality and lifecycle UNKNOWN. |
| Work Note ↔ Task | Candidate Work Note has zero or one logical Task reference; Task can be referenced by zero or many Work Notes. | Cross-service reference, not DB foreign key. Work Note remains canonical in Capture; Task remains canonical in Task Service. | Missing, canceled, or inaccessible Task link display/repair semantics are UNKNOWN. | Each read/link operation checks current Task access; link existence is not a grant. | B5 accepts optional reference concept; exact cardinality remains PROPOSED. |
| Handover ↔ Task | Handover item holds a logical Task ID; Handover package/acknowledgment is separate; Task assignee remains canonical in Task Service. | Command uses Task API, not direct database access. Cross-service records cannot share the Task transaction. | Retry, reconciliation, compensation, Handover package retention, and Task eligibility remain under the owning contracts. | SUCCESSOR receives only explicitly authorized Task context, not inherited project access. | B3/B6 are DECIDED boundaries; details UNKNOWN. |
| Task → TaskEvent | Candidate each accepted Task mutation has one corresponding safe history record; one Task has zero or many event records. Exact operation coverage is undecided. | Same Task database; separate append-only collection. No unbounded embedded history array. | Retention and privacy/deletion obligations require policy. Append-only does not by itself mean retained forever. | History uses the same protected Task scope with an approved projection. | B4 accepts atomic corresponding history and append-only collection; event schema/coverage UNKNOWN. |

### 4.1 Ownership recommendation

Treat Project as the resource ownership boundary and Organization as contextual parent scope. The `organizationId` candidate is a query/integrity denormalization, not a second owner. If the authoritative contract chooses to store it, the Task service must derive it from the trusted Project relationship and maintain the immutable equality invariant. If it chooses not to store it, the service must resolve Organization context through the Project owner/API. This proposal recommends storing the scoped context only if approved query workload and isolation checks justify the duplicate; a convenience filter alone is insufficient evidence.

## 5. Proposed Task data dictionary

No row below is a final schema. `Required?`, nullability, defaults, limits, and enum values remain decision inputs even where a technical recommendation is shown. Do not use these candidates in a model, migration, API fixture, or production validator before approval.

| Field candidate | Meaning / purpose | Type / representation candidate | Required / null / default | Validation candidate | Owner / mutability | Relationship / cardinality | Query justification | Evidence and unresolved decision |
|---|---|---|---|---|---|---|---|---|
| `_id` | Stable canonical Task identifier. | MongoDB `ObjectId` candidate. | Generated on create; no null; no business default. | BSON ObjectId. | Task Service; immutable. | Task identity. | Direct detail/update lookup and references. | S3/S4 propose ObjectId. Q3 must approve identifier representation. No human-readable key is established. |
| `projectId` | Project that owns the Task. | Project's stable logical ID; exact BSON/string representation follows Project contract. | Candidate required, non-null, no default. | Valid ID shape; Project scope/existence checked through owning contract. | Server verifies; immutable after create unless a transfer policy is separately approved. | Exactly one Project per Task is recommended. | Every Task query is Project-scoped. | Project is the accepted domain resource boundary; Task cardinality/type still needs approval. |
| `organizationId` | Parent organization context for scoped checks and optionally query isolation. | Organization's stable logical ID. | If persisted, candidate required/non-null; no client default. | Derived from authoritative Project; must equal that Project's Organization; immutable. | Server-derived; immutable unless explicit Project transfer semantics are approved. | Contextual parent; not a second owner. | May support tenant-scoped filters/indexes if approved workload needs it. | Current schema doc proposes it, but ownership and denormalization must be explicitly accepted. Q2/Q3. |
| `teamId` | Optional single Team context. | Team's stable logical ID. | Optional candidate; null vs absent and default unresolved. | Team must belong to the Task's Project; eligibility/current membership checked by owner. | Authorized command only; mutability/transfer rules unresolved. | Candidate 0..1 Team per Task. | Team filtering/assignment only if approved use cases require it. | S3/S4 proposal; Q2/Q5. No multi-Team relationship is approved. |
| `title` | Short human-readable work summary. | String. | Candidate required; null disallowed; no default. | Empty/whitespace policy, length, normalization, and control character rules UNKNOWN. | User-editable only under approved action/field matrix. | Scalar. | List, detail, title search. | S3/S4 proposal. No uniqueness rule is evidenced. Q3/Q6. |
| `description` | Optional longer task context. | String candidate. | Optional; null/omitted distinction UNKNOWN; no default selected. | Length/format/markup limits and safe rendering rules UNKNOWN. | User-editable only under approved action/field matrix. | Scalar. | Detail; possibly text search only if approved. | Proposed field, not accepted. Q3/Q5/Q6. |
| `status` | Current lifecycle state. | String enum only after D-02 approval. | Requiredness and initial default UNKNOWN. | Exact values and per-command transition validation from accepted D-02 contract; unknown value/edge fails closed. | Only approved lifecycle command may mutate. | One current state. | Project list, filters, counts, Handover eligibility. | D-02 R1 records zero enabled edges and all 25 cells UNKNOWN. `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED` remain candidates, not schema values. |
| `priority` | Relative urgency, if V1 needs it. | Enum/string candidate. | Optional/required/default all UNKNOWN. | Allowed values and ordering UNKNOWN. | Authorized field edit only. | Scalar. | Filter/order only if approved. | S3/S4 propose LOW/MEDIUM/HIGH and MEDIUM default; no accepted rule. Q1/Q3/Q6. Could omit if out of approved scope. |
| `createdBy` | Trusted identity that created the Task. | Stable User ID representation from identity contract. | Candidate required, non-null; server supplied. | Must come from verified request context, never client body. | Immutable. | One creator identity. | Audit/provenance and optional display projection. | S3/S4 proposal; accepted scoped identity rules. Q3/Q5/Q8. Identity deletion/retention unresolved. |
| `assigneeId` | Current single responsible user, if assignment is in approved V1. | Stable User ID representation. | Candidate optional; absent vs null unresolved; no default selected. | Target eligibility, same scope, active membership and reauthorization rules need approval. | Assignment command only; not arbitrary field update. | Candidate 0..1 assignee. | Assignment list/filter and Handover selection. | S3/S4 proposal; B6 canonical assignment boundary. Q2/Q5/Q7. Stored value cannot grant access. |
| `dueDate` | Optional planned due point. | BSON Date timestamp candidate; date-only is an alternative. | Optional; nullability/default unresolved. | Date-only versus instant, timezone, past date, precision and display rules UNKNOWN. | Authorized field edit only. | Scalar. | Due-date filter/sort only if approved. | S3/S4 proposal uses `dueDate`; Q3/Q6 must decide semantics. Do not choose UTC midnight/date-only silently. |
| `createdAt` | Server creation time. | BSON Date, UTC instant candidate. | Candidate required and server generated; no null/default from client. | Server clock and precision policy. | Immutable, server-owned. | Scalar. | Default project ordering and operational audit. | S3/S4 proposal; Q3/Q8 exact representation and clock expectations. |
| `updatedAt` | Last committed Task mutation time. | BSON Date, UTC instant candidate. | Candidate required and server generated. | Updated in same transaction as mutation/history; behavior for no-op/replay UNKNOWN. | Server-owned; every approved mutation updates. | Scalar. | Recent-activity sort and query indexes. | S3/S4 proposal; Q3/Q7/Q8. Timestamp alone is not a concurrency token. |
| `version` | Optional monotonic concurrency token. | Non-negative integer candidate. | Candidate starts at agreed initial value; exact requiredness/default UNKNOWN. | Increment only on accepted committed mutation; stale-write behavior from D-02. | Server-owned, monotonic. | One version per Task; event may record resulting version. | CAS and history/event ordering if approved. | [D-02 Q7/D02-05](17-task-v1-command-reliability-review.md) remains unapproved. Do not implement CAS values or fixtures from this candidate alone. |

### 5.1 Field categories

| Category | Proposal | Reason / gate |
|---|---|---|
| Candidate for core V1 | `_id`, `projectId`, `title`, `createdBy`, lifecycle, timestamps; optional `organizationId`, `teamId`, description, assignee, due date, priority, version as selected by approved use cases. | These candidates appear across existing Task use-case/schema docs. Their requiredness and exact shapes are not approved. |
| Optional only if scope requires | `teamId`, description, assignee, due date, priority, version, optional `organizationId` denormalization. | Do not persist a field solely because the schema proposal lists it; tie it to an approved operation/query/invariant. |
| Do not add for V1 without a new decision | `taskKey`, task type hierarchy, soft-delete/archive fields, AI draft fields, external sync IDs. | No accepted use case currently requires these; the capability boundary in §3.1 also prohibits inferring additional functionality from Jira parity. |
| Decision required | State/priority enums, status/priority defaults, exact identifier, null versus absent, field lengths, due-date/timezone meaning, user deletion behavior, retention/deletion policy, concurrency and idempotency metadata. | Each has product/API/security/operations implications and must have a named decision owner. |

`deletedAt`/`archivedAt` is not recommended for the first V1 dictionary because no accepted use case defines soft deletion or archive behavior. The current use-case proposal prefers preserving references/history, but that is not a retention or legal-deletion policy. A delete/cancel/archive decision must define visibility, link behavior, retention, and recovery before a field or endpoint is added.

## 6. Validation and integrity recommendation

### 6.1 Document-level validation

After the Leader approves field choices, use MongoDB schema validation (and matching NestJS/Mongoose request validation) to enforce selected BSON types, required fields, allowed enums, and approved length/range/format constraints. The database validator should protect persistence from invalid service writes; API validation should return the approved client contract. Neither layer should silently coerce an UNKNOWN value.

Recommended validation categories, with actual values awaiting approval:

1. **Shape:** required versus optional, null versus absent, BSON type, and allowed nested structure. Prefer a flat Task record for the currently proposed access patterns; no unbounded embedded history array.
2. **Strings:** title/description trim, max length, line breaks, Unicode and rendering rules. No numeric limits are established by current authority.
3. **Enums:** exact lifecycle and priority values only from approved registers. D-02 currently has no enabled transition, so candidate states are not usable fixtures.
4. **References:** ID format plus application checks for Project, Team and eligible User. A MongoDB validator cannot enforce a foreign key in another service's database.
5. **Scope invariants:** persisted `organizationId` (if selected) must equal the Organization of `projectId`; `teamId` (if selected) must belong to that Project. The owning service/API and transaction/fencing behavior must be specified because cross-service membership can change concurrently.
6. **Server-owned values:** derive creator, timestamps, organization context, and version from trusted server state after the corresponding fields are approved. Reject attempts to set them from an untrusted request.
7. **No silent fallback:** no fallback to `continuum_db`, shared collections, default enum, placeholder assignee, or guessed date semantics.

### 6.2 Integrity not provided by unique indexes

Unique indexes enforce only an explicitly chosen key invariant. They do not prove that a user is an active member, that a Team belongs to a Project, that an actor is authorized, or that Task and history committed together. Those guarantees belong to validated service operations and the accepted transaction contract.

## 7. Data integrity and deletion options

| Topic | Recommendation | Alternatives / consequence | State |
|---|---|---|---|
| Cross-service parent integrity | Keep logical IDs; Task Service validates Project/Team/User scope through owning contracts and trusted context. Do not copy mutable parent/user documents. | Local snapshots can reduce calls but create drift and stale authorization. | PROPOSED. Exact trust/freshness contract UNKNOWN. |
| Organization context | Prefer deriving it from Project; persist only if approved tenant/query isolation needs justify denormalization. If persisted, set from server and enforce equality with Project owner. | No stored `organizationId` avoids duplication but may add owner lookups. | PROPOSED. Q2/Q3. |
| Task hard delete | Exclude a delete operation from recommended V1 until product, link, retention, audit, and privacy behavior is decided. | Hard delete risks dangling Work Note/Handover references and history loss; soft delete also needs explicit semantics. | PROPOSED/FUTURE, not accepted retention policy. |
| Cancellation/archival | Do not equate `CANCELLED` with deletion or archive. State semantics and terminal behavior belong to D-02. | A terminal state preserves identity but requires read/search/retention rules. | UNKNOWN. |
| Parent deletion/transfer | No cascade, transfer, or automatic assignee clearing is inferred. Require an explicit owning lifecycle command and audit/recovery policy. | Cascade is simple but can lose linked context; transfer can cross authorization scopes. | UNKNOWN. |
| Membership/ACL revocation | Re-check effective access at each read/write; do not use a stored `assigneeId` or role snapshot as authorization. | Cleanup may be asynchronous only if it never restores access; whether to clear/transfer assignment is separate. | B8/B10 accepted boundary; cleanup behavior UNKNOWN. |

## 8. Query workload, indexes, and uniqueness

### 8.1 Candidate access patterns

The following are derived from UC-TM-01/03/05/07/09/10. Exact operations and filters must first be selected for V1. An index is not required merely because a field is present.

| Pattern | Candidate filter/sort | Candidate index shape | Correctness or performance | Cost and open decision |
|---|---|---|---|---|
| List/recent Tasks in one Project | `{ projectId }`, optional approved `status`, sort `updatedAt DESC` (stable tie-breaker to be selected). | Candidate non-unique `{ projectId: 1, updatedAt: -1, _id: -1 }`; if status is a common mandatory filter, compare `{ projectId: 1, status: 1, updatedAt: -1, _id: -1 }`. | Performance. Project scoping is also an authorization correctness requirement enforced by query construction, not by index. | Status-before-sort helps one filter shape but may not support unfiltered sort equally. Choose from real approved workload and `explain()` evidence. |
| List Tasks for one assignee in Project | `{ projectId, assigneeId }`, optional approved state, recent sort. | Candidate non-unique `{ projectId: 1, assigneeId: 1, updatedAt: -1, _id: -1 }`; status variant only if measured and approved. | Performance. A unique index would be wrong because a Project/assignee can have many Tasks. | More indexes add write, storage, and update cost. Validate actual UI/API query shape. |
| Filter by Team or due date | Project-scoped optional Team and/or due-date range/sort. | No index recommendation until V1 query is selected; candidate `{ projectId: 1, teamId: 1, dueDate: 1 }` only if that exact query exists. | Performance. | Optional fields and sort/range order determine usefulness. Avoid speculative indexes. |
| Read Task detail/update | `_id` and authorization-scoped Project. | Built-in unique `_id` index; optionally query `{ _id, projectId }` for scoped update predicates if implementation requires it. | `_id` uniqueness is database identity; Project condition in update is correctness defense-in-depth. | `_id` index is automatically created. Extra compound index should be justified with actual query plan and schema. |
| Read one Task's history page | `taskId`, order by `occurredAt` with stable tie-breaker; after/before cursor only after API selection. | Candidate non-unique `{ taskId: 1, occurredAt: -1, _id: -1 }`. | Performance and deterministic pagination; no unique business invariant. | Requires approved event timestamp/order/cursor contract; unbounded history scan is not acceptable. |
| Relay unpublished outbox entries | Only if outbox is approved; filter unpublished/retryable records and order according to approved delivery semantics. | Conditional partial index on approved pending state/time; unique event identity may use `_id` or a separately approved event key. | Correctness for event identity/dedup depends on approved contract; queue lookup is performance. | Don't create collection/index unless a consumer and relay are approved. |

Organization prefixes should be added to compound keys only if `organizationId` storage is approved and every relevant query uses it. Compound key order must follow actual equality filters, then range/sort requirements; the examples are alternatives to test, not final indexes. A title index or text index needs a concrete approved search behavior. No title uniqueness is proposed.

### 8.2 Uniqueness decisions

| Candidate key | Recommendation | Reason / state |
|---|---|---|
| Mongo `_id` | Keep built-in unique identity index. | MongoDB identity invariant; no additional business approval is implied. |
| `(projectId, title)` or `(organizationId, title)` | Do not add uniqueness. | No accepted product rule says titles are unique; duplicate titles are normal task behavior. |
| `operationId` / idempotency key | Do not define an index in D-03 from this proposal. | D-02 still has UNKNOWN scope, namespace, payload fingerprint, expiration, replay, and retention. Once approved, unique enforcement may be required for correctness and must be part of the operation contract. |
| Event ID | Use a stable event identity only if its event contract requires it; exact key is UNKNOWN. | Event delivery deduplication is conditional on an approved consumer/outbox. `_id` may suffice, but no choice is made here. |
| Any other key | No uniqueness without a specific business invariant and collision semantics. | A unique index changes user-visible create/update behavior and needs explicit approval. |

### 8.3 Index validation plan

After contract approval and implementation, initialize an isolated disposable MongoDB replica set using the supported project test mechanism. Assert that the approved index names, keys, options, uniqueness and partial filters are present; insert duplicate values only for approved unique invariants; verify non-unique patterns accept legitimate repeated values; run representative scoped queries with realistic fixture cardinality and inspect `explain()` for expected index use. Do not freeze planner-specific exact costs without a stable environment. The tests must fail if an implementation omits an approved index or creates a forbidden unique constraint.

## 9. Task history and transaction contract

### 9.1 Accepted boundary vs proposed event content

**Accepted (B4/B7):** Task Service owns an append-only `task_events` collection in `continuum_task`; a Task mutation and its corresponding history record commit atomically. History carries actor type/identity, event/source, changed-field metadata, Task version, timestamp, operation ID and correlation ID at the accepted intent level. Do not store full prompts or unrestricted raw Agent context.

**Not yet approved:** exact BSON field names/types, event vocabulary, whether create/no-op/failed/denied commands create a record, safe before/after projection, redaction, user-visible history, ordering, pagination, retention, compliance audit mirroring, version representation, operation identity presence/nullability, and failure response. ADR-010's metadata intent does not close those choices.

### 9.2 Event-shape recommendation

For each approved state-changing command, write one immutable event in the same Task database transaction. A reviewable candidate event shape is:

| Candidate event field | Proposed purpose | Decision still needed |
|---|---|---|
| Event `_id` | Stable event identity. | ObjectId vs explicit event ID; whether delivery uses this as dedupe key. |
| `taskId` | Identify the aggregate. | Exact representation and retention when Task is unavailable. |
| `organizationId`, `projectId` | Preserve the authorization context at commit time if approved. | Whether stored, immutable, and included in every event. |
| `actorId`, `actorType`, `source` | Attribute human/service/Agent-originated action. | Exact actor taxonomy and trusted source values. |
| `eventType` / action | Describe accepted command/mutation. | Vocabulary and create/no-op/command mapping. |
| `changedFields` | Record the changed field names and safe value deltas. | Exact structure and whether before/after is stored. |
| `taskVersion` | Associate event to committed aggregate version. | Depends on D-02 concurrency decision. |
| `occurredAt` | Server commit time. | Clock/precision and ordering contract. |
| `operationId`, `correlationId` | Trace retries and cross-service interaction. | Requiredness, namespaces, privacy, retention and idempotency link. |
| Agent proposal/confirmation reference | Record proposal provenance without raw prompt/context. | Only if Agent use case is approved; exact safe identifier and retention. |

This is a candidate data dictionary for review, not an event schema. Prefer changed-field deltas over an unrestricted full Task snapshot, but define a safe allowlist and redaction rules first. Do not assume a timestamp alone orders concurrent writes; use the accepted aggregate version/operation order if D-02 approves it.

### 9.3 Atomicity and failure expectations

| Failure point | Accepted/proposed expected invariant | Contract boundary still needed |
|---|---|---|
| Task validation or authorization fails before mutation | No Task mutation. | Exact failure result and whether security audit is separately required. |
| Task write fails | No corresponding success history record. | Storage error and retry/uncertain-commit behavior. |
| Task write succeeds provisionally but event write fails | Transaction aborts; neither Task mutation nor its required history is committed. | Failure response/status and retry semantics. |
| Event write succeeds provisionally but transaction aborts | Event is not visible as committed history without its Task mutation. | Failure response and observability/metrics. |
| Transaction commit outcome is uncertain to caller | Do not issue a false replacement result or execute an unsafe duplicate command. | D-02 must choose idempotency namespace, proof retention, replay, and reconciliation contract. |
| Outbox write is enabled and fails | If publication is approved, Task, history, and required outbox record must commit or roll back together. | Consumer, delivery guarantees, retry/dedup/order, and failure response. |

MongoDB replica-set transactions provide the technical mechanism for a multi-document transaction, but add operational cost/limits and do not remove the need to model documents well. In a disposable replica-set integration test, force failures on both writes and verify rollback from persisted state. A mocked unit test alone cannot prove this transaction boundary.

## 10. Event publication and outbox recommendation

**Proposal:** defer `outbox_events` for V1 unless a named, approved downstream consumer needs durable asynchronous delivery of committed Task mutations. Current accepted integrations establish API/event boundaries generally, but the inspected Task use cases identify no required durable Task event consumer. Work Note linking and Handover assignment can use Task API; they do not by themselves require an outbox. `task_events` is business history, not a delivery queue.

| Option | Benefits | Costs / risks | Recommendation and status |
|---|---|---|---|
| No durable Task event publication in first slice | Fewer collections, indexes, relay operations, retries and duplicate handling; aligns with API-only integration until a consumer is named. | A later consumer cannot reconstruct delivery guarantees from ad hoc polling; new approved design/implementation needed. | Recommended for V1 only if Product/API owners confirm no durable consumer. PROPOSED — LEADER APPROVAL REQUIRED. |
| Add transactional outbox with a named consumer | Avoids dual-write loss by committing Task, history and delivery record together; relay retries after commit. | Requires event schema, delivery semantics, ordering, dedupe, retry limits, dead-letter/recovery owner, retention, metrics and privacy review. | Select only after consumer/use case and operational owner are approved. UNKNOWN. |
| Publish directly after Task transaction without outbox | Simple for best-effort notifications. | Crash between database commit and publish can lose the event; publish retry can duplicate; cannot meet durable delivery requirement. | Do not claim durable delivery with this option. It may be considered only for an explicitly best-effort contract. |

If an outbox is approved, proposal requirements are: write its record in the same transaction as Task and history; relay only committed records; make consumers idempotent by stable event ID; specify at-least-once/other delivery explicitly; define aggregate ordering; bound retries and identify recovery ownership; protect payloads from raw prompts/private content; and test rollback, retry, duplicate delivery, and ordering. These are technical design recommendations, not current DATN delivery decisions.

## 11. Disposable integration-test proposal

These are future test obligations, not tests run or pass results. DATN-BE currently has no Task implementation. Exact API assertions must wait for approved HTTP/DTO/error contracts; repository/integration assertions can be finalized only after the schema and event choices are approved.

| Test group | Disposable setup and action | Expected invariant | Approval/implementation blocker |
|---|---|---|---|
| Initialization | Start an isolated Task database on a disposable replica set; run service initialization twice. | Initialization is repeatable; only approved collections/validators/indexes exist; no shared `continuum_db` fallback or writes to another service DB. | Task owner/runtime and approved migration/initialization contract. |
| Persistence round trip | Create each approved field combination, read it back, restart/reconnect, and verify stored BSON types and server-owned values. | Persistence matches approved dictionary; no unapproved fields or silent coercions. | DATN-117 approval and implementation. |
| Validation | Attempt missing, null, wrong BSON type, unsupported enum, out-of-range/oversize values, and mismatched scope/reference cases. | Rejected input persists no Task/history; only approved constraints enforced. | Approved validation values, API error contract, and reference authority. |
| Relationship integrity | Use same-project and cross-project Organization/Team/User references, including inactive/removal states where contract defines them. | Invalid or out-of-scope relationships cannot be persisted or exposed. | Approved cardinalities, membership freshness/fencing, and failure contract. |
| Indexes/uniqueness | Inspect indexes and run representative queries; exercise duplicate cases only for approved unique invariants. | Required indexes exist; title duplicates remain valid unless a rule is approved; no accidental uniqueness. | DATN-118 query/index and uniqueness decision. |
| Atomic Task/history success | Commit an approved mutation and inspect Task plus corresponding immutable history record. | Both are visible with same committed operation/version relationship. | Accepted event policy and implementation. |
| Atomic rollback | Inject event-write failure after provisional Task update; separately abort after provisional event insertion. | Neither side is visible after abort; prior Task/history remain intact. | DATN-119 implementation and failure contract. |
| Concurrency/idempotency | Race approved commands and retry the same operation after simulated lost response. | Matches the approved CAS/key/replay oracle; no duplicate state mutation or history event. | D-02 version/idempotency decisions; do not invent expected response. |
| Authorization/revocation | Revoke Project/Team membership around read/write and test cross-scope access. | Current effective access is checked; membership or stored assignee alone cannot grant access. | Accepted B8/B10 plus exact Task authorization/fence contract. |
| Conditional outbox | If selected, fail relay, retry, duplicate delivery, reorder and roll back producer transaction. | Approved delivery/dedup/order guarantees hold; rollback emits nothing. | DATN-120 consumer and delivery contract; outbox implementation. |

After approval, maintain a trace from each accepted decision ID to fixtures and tests. Record replica-set version/config, seed data, commands, assertions, observed result, and CI run. Do not use Project/IAM tests or mocks as evidence of Task persistence/transaction behavior.

## 12. Leader decision matrix

All recommendations are for explicit review. Status values follow the task's allowed vocabulary. `ACCEPTED` appears only for existing baseline decisions; no proposed field, query, status, or event schema is marked accepted.

| Decision | Recommended option | Alternatives | Evidence | Consequence | Status |
|---|---|---|---|---|---|
| V1 Task use cases | Core project-local list/create/detail/edit/assignment/approved status/search/limited history; defer advanced features. Decide each UC-TM explicitly. | Smaller CRUD slice; include Kanban/Agent/other capabilities with new requirements. | UC-TM-01–11 proposal; B1–B7. | Defines BE/FE/API and tests; prevents speculative fields. | PROPOSED — LEADER APPROVAL REQUIRED |
| Required fields and types | Project ownership plus stable ID, title, creator, server timestamps and only fields required by approved operations; exact types from owning contracts. | Store organization context; omit priority/team/version when not needed; choose alternate date/ID forms. | D-01 Q2/Q3; schema doc is proposal. | Controls storage, DTO, migration and validation. | PROPOSED — LEADER APPROVAL REQUIRED |
| Defaults and lifecycle values | Reuse only states/defaults explicitly approved by D-02; fail closed for unknown values/edges. | Candidate 5-state lifecycle; reduce states; another approved set. | D-02 R1; all 25 edges UNKNOWN. | Determines schema enum, command behavior, history, UI and fixtures. | UNKNOWN |
| Organization/Project ownership | Project owns Task; Organization is contextual parent; persist derived `organizationId` only if query/isolation case is approved. | Organization-owned Task; Project lookup without stored organization context. | B8–B10; Project hierarchy; Q2. | Affects access scoping, query shape, integrity and transfer behavior. | PROPOSED — LEADER APPROVAL REQUIRED |
| Relationships/cardinalities | One Project; candidate 0..1 Team and 0..1 assignee; optional Work Note reference; Handover uses logical ID/API. | Teamless prohibited; multi-Team; alternate Work Note cardinality. | B5/B6; S3/S4 proposal; Q2. | Determines IDs, cross-service checks and deletion lifecycle. | PROPOSED — LEADER APPROVAL REQUIRED |
| Validation rules | DB validator plus matching API validation for approved types/required/enums/ranges; server derives trusted fields; cross-service scope checked through owning contracts. | API-only validation (weaker protection); stricter DB constraints after data/migration review. | MongoDB validator docs; accepted scope boundaries. | Rejection behavior, data cleanliness and rollout compatibility. | PROPOSED — LEADER APPROVAL REQUIRED |
| Unique constraints | Only `_id` by default; no unique Task title. Add operation/event uniqueness only after D-02/outbox contracts define the invariant. | Project-local business key if a real product rule requires it. | Existing use cases contain no title uniqueness; D-02 idempotency UNKNOWN. | Unique indexes change create/retry outcomes and require migration duplicate analysis. | PROPOSED — LEADER APPROVAL REQUIRED |
| Query indexes | Start from approved scoped list/detail/history queries; select compound order using representative `explain()`; omit speculative Team/due-date index. | Add index only for measured/filter requirement. | UC patterns; MongoDB index/query guidance. | Indexes add write/storage cost. | PROPOSED — LEADER APPROVAL REQUIRED |
| Task history contract | Append-only `task_events`; safe actor/action/target/time/change provenance; define visible projection, order, retention and redaction. | More/less history; separate compliance audit only if policy demands. | B4/B7; ADR-010; Q8 UNKNOWN. | Affects privacy, audit, history API and storage growth. | PROPOSED — LEADER APPROVAL REQUIRED |
| Mutation + history atomicity | Keep one Task DB transaction for mutation and corresponding required history. | None within accepted B4 boundary; specify operation coverage and failure mapping. | B4 accepted; Mongo replica set transaction capability. | If either write fails, no partial success; requires replica-set integration tests. | ACCEPTED (B4 boundary); exact event coverage UNKNOWN |
| Durable event publication | No required durable consumer identified for V1; confirm explicitly. | Name a consumer and define event contract. | Current UC/API boundary; Q9 unknown. | Determines if delivery records and relay infrastructure are required. | UNKNOWN |
| Outbox requirement | Defer unless a named durable consumer is approved; history does not imply delivery. | Transactional outbox for named consumer; best-effort direct publish only if explicitly acceptable. | B4 conditional outbox; AWS transactional outbox guidance. | Outbox adds relay, retries, idempotency, ordering, retention and on-call ownership. | PROPOSED — LEADER APPROVAL REQUIRED |
| Integrity and deletion rules | No V1 delete field/route until link, retention, privacy and parent lifecycle rules are decided; no implicit cascade/transfer. | Explicit archive/soft delete/hard delete policy with migration and reference behavior. | S3/S4 proposal; B5/B6; no accepted delete UC. | Affects data loss, dangling links and recovery. | UNKNOWN |
| Test/failure contract | Disposable replica-set tests for indexes, validation, persistence, atomic rollback, authorization boundary, and conditional outbox; exact HTTP errors from API owner. | Standalone Mongo for tests cannot prove transaction; mock-only tests are insufficient. | DATN-95 AC3; MongoDB transaction docs. | Establishes meaningful D-03 evidence without asserting unspecified errors. | PROPOSED — LEADER APPROVAL REQUIRED |
| Named approval authority | Record person, role, decision scope, date, evidence link and owning revision before converting proposals. | Route separate decisions to Product, API/Security, DB, Handover and Operations authorities. | `.sage` active baseline null; no Task approver identified. | Prevents review or SAGE recording from being mistaken for approval. | UNKNOWN |

### 12.1 Decisions requested from the Leader

Please record an answer for each line, including partial approval and explicit deferrals. Unanswered items remain UNKNOWN.

1. **Product scope:** select each UC-TM-01–11 as V1, future, or excluded; specify whether status, assignment, history, Work Note link, and Handover are in the first usable slice.
2. **Ownership and relationships:** confirm Project resource ownership; whether `organizationId` is persisted as derived context; Team cardinality/teamless policy; assignee cardinality/eligibility; Work Note cardinality; Project/Team/User removal and transfer behavior.
3. **Task dictionary and validation:** approve each field's presence/type/required/null/default/limits, server-owned/editable status, due-date meaning/timezone, state and priority values/defaults, and cross-scope validation behavior. Resolve D-02 states/edges before accepting `status` enum.
4. **Queries and constraints:** choose supported list/search/history query shapes, sort/pagination, and any business uniqueness/idempotency invariant; approve index candidates only after workload and `explain()` review.
5. **History and compliance:** define event vocabulary/coverage, safe before/after fields, visibility, ordering, retention, redaction, and whether compliance audit is needed.
6. **Publication and tests:** name any durable consumer; if one exists, approve delivery/retry/order/dedup/retention and operational owner. Approve the disposable replica-set failure/index/persistence test expectations and exact error contract through the owning API decision.

These answers should be recorded with: decision ID; accepted/partial/rejected/deferred; exact value/rationale; approver name, authority and time; evidence permalink; owning document/API/schema revision; remaining UNKNOWNs; and test/oracle mapping.

## 13. Research and source ledger

Research was used to assess technical options; it does not establish DATN product policy. Sources below are official primary documentation and were reviewed 13/10/2026.

| Source | Relevant finding | Applicability to DATN | Limitation |
|---|---|---|---|
| [MongoDB Data Modeling, v7.0](https://www.mongodb.com/docs/v7.0/data-modeling/) | Model around access patterns; choose embedding versus references based on how data is used and updated together. | Supports keeping unbounded Task history separate and storing logical references to Project/User/Work Note/Handover where ownership is separate. | Does not pick DATN's cardinality, fields, or owner; those are product decisions. |
| [MongoDB Schema Design Process, v7.0](https://www.mongodb.com/docs/v7.0/data-modeling/schema-design-process/) | Identify workload, map relationships, select embed/reference strategy, then create indexes. | Supports deferring final compound indexes until V1 operations and filters are approved. | Technical design advice, not a DATN workload measurement. |
| [MongoDB Schema Validation, v7.0](https://www.mongodb.com/docs/v7.0/core/schema-validation/) | MongoDB can reject or warn on documents that violate configured rules; validation is applied at the database boundary. | A second persistence guard can complement NestJS/Mongoose request validation after field rules are approved. | Cannot enforce authorization or foreign keys across service-owned databases; validation settings and rollout behavior need implementation review. |
| [MongoDB Unique Indexes and Schema Validation, v7.0](https://www.mongodb.com/docs/v7.0/tutorial/unique-indexes-schema-validation/) | Unique indexes enforce selected key constraints; schema validation can constrain document shape. | Helps separate product uniqueness from performance indexes and supports explicit duplicate tests after a uniqueness rule exists. | It does not determine whether Task titles or operation IDs should be unique in DATN. Existing duplicate data must be checked before adding a unique index. |
| [MongoDB Indexes, v7.0](https://www.mongodb.com/docs/v7.0/indexes/) | Indexes support query patterns with read/write and storage trade-offs; compound field order affects which queries are supported. | Candidate Project-scoped and history query indexes should be compared against real approved filters/sorts. | Exact benefit depends on DATN data volume, query plans, optional filters and sort shape; run workload tests after approval. |
| [MongoDB Transactions, v7.0](https://www.mongodb.com/docs/v7.0/core/transactions/) | Single-document writes are atomic; multi-document/collection work may use transactions on supported deployments. | `tasks` plus `task_events` (and conditional outbox) need a multi-document transaction under accepted B4. | Transaction support does not make a poor schema good or define API errors/idempotency. |
| [MongoDB Transaction Production Considerations, v7.0](https://www.mongodb.com/docs/v7.0/core/transactions-production-consideration/) | Transaction support and limits depend on deployment topology; transactions add operational considerations and bounded runtime/resource constraints. | Use disposable replica-set integration tests and keep Task/history transaction bounded. Existing DATN MongoDB is configured as a replica set. | Must verify the actual target/test deployment and configuration at implementation time; no Task DB runtime is currently active. |
| [AWS Transactional Outbox Pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) | A transactional outbox addresses dual writes when a database commit must be paired with reliable message publication; relays/consumers need retry and duplicate handling. | Supports conditional outbox only when a durable Task event consumer is identified. | AWS pattern is architecture guidance, not a DATN requirement; it cannot decide whether V1 has a consumer or its delivery guarantee. |

No Jira field model, status set, permission scheme, or workflow was copied into this recommendation. No current Jira behavior was needed to decide DATN Task persistence; the existing Jira research document is market/capability context, not product authority.

## 14. Artifact ownership, Jira traceability, and approval gate

### 14.1 Repository ownership

- **This proposal and Task product contract:** `product_docs`, because it owns product/domain use cases and Task contract documentation.
- **SAGE:** keep governance/evidence/decision traceability synchronized only after an authorized decision exists. This proposal does not modify `.sage` or claim a SAGE decision.
- **DATN-BE:** implementation source after approval. No backend schema/model/index/migration, runtime config, API, or tests are changed here.
- **DATN-FE:** no change; A-03/frontend recovery or Task UI is outside this task.
- **Jira:** track actual preparation/implementation work and link review artifacts. Status is not product approval.

### 14.2 Readiness gate

Keep DATN-95 In Progress for contract-resolution work if that is the current Jira state; keep DATN-117–121 To Do until their own acceptance has evidence. Do not mark the parent or children Done based on this proposal. Do not remove D-03's persistence gate or start implementation until:

1. The Task approver identity/authority and each decision's scope are recorded.
2. Product use cases, data dictionary, relationships, lifecycle, authorization and API boundaries are accepted in owning revisions.
3. Validation, uniqueness, query/index, history/retention, transaction-failure and conditional outbox decisions are testable and traceable.
4. The updated contract passes review without unresolved contradictions and is synchronized into SAGE traceability.
5. DATN-BE main/runtime ownership and a disposable replica-set test path are rechecked before a separate implementation task/branch starts.

Until all applicable conditions are met, readiness remains **BLOCKED**. Proposal review can improve the decision record, but it cannot convert a technical recommendation to an accepted DATN requirement.

## 15. References to existing DATN evidence

- [D-01 Task V1 contract readiness, Q1–Q9](13-task-v1-contract-readiness.md)
- [D-01 review worksheet](14-task-v1-review-worksheet.md) — contains the P2 heading to be corrected in a separate documentation change
- [D-01 validation scenarios](15-task-v1-review-validation.md)
- [D-02 state machine contract](16-task-v1-state-machine-contract.md)
- [D-02 command reliability review](17-task-v1-command-reliability-review.md)
- [D-02 scenario and oracle matrix](18-task-v1-state-machine-oracles.md)
- [Task V1 use cases](12-continuum-task-management-use-cases.md)
- [Task storage boundary proposal](../../database-design/12_TASK_MANAGEMENT_SCHEMA.md)
- [ADR-009 — canonical Task source and MongoDB](../../research-tech/ADR-009-internal-task-source-and-mongodb.md)
- [ADR-010 — Task service and storage boundary](../../research-tech/ADR-010-task-service-in-existing-repositories.md)
- [DATN-95 — D-03 Task Data Foundation](https://trankimthang0207.atlassian.net/browse/DATN-95)
