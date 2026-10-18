# DATN-373 — D-13 Task V1 API, Lifecycle and Contract Decisions

- **Document Revision:** D13-R6 (18/10/2026, Asia/Bangkok).
- **Document Status:** PROPOSED DISPOSITION & CONTRACT SPECIFICATION FOR REVIEW.
- **Review Authority Framework:**
  - Product authority: Task V1 scope, fields, lifecycle meanings, and product behavior. No named approver is assigned or inferred by this record.
  - Architecture authority: Task Service & Gateway Boundary per [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md).
  - Security authority: IAM, Project Scope & RBAC Boundary per [`02_ACTORS_ROLES_AND_PERMISSIONS.md`](../02_ACTORS_ROLES_AND_PERMISSIONS.md).
  - Approval evidence must identify the authority, exact D13 revision and decision scope. Existing approval records apply only to their stated scope; PR merge state and Jira status are not approval evidence.
- **Author & Document Owner:** Nguyen Hong Phuc (phuc2348hong@gmail.com).
- **Target Epic:** [DATN-75 Epic D — Task Management](https://trankimthang0207.atlassian.net/browse/DATN-75).
- **Parent Task:** [DATN-373](https://trankimthang0207.atlassian.net/browse/DATN-373) — `D-13 Close remaining Task V1 API and lifecycle decisions`.
- **Subtasks Covered:**
  - [DATN-374](https://trankimthang0207.atlassian.net/browse/DATN-374) — D-13.1 Inventory unresolved Task contract and lifecycle decisions
  - [DATN-375](https://trankimthang0207.atlassian.net/browse/DATN-375) — D-13.2 Obtain authority disposition for API and transition matrix
  - [DATN-376](https://trankimthang0207.atlassian.net/browse/DATN-376) — D-13.3 Publish downstream acceptance and dependency trace
- **Baseline Sources & Approved Foundations:**
  - B1–B10 & Recommendation Decisions: [Task V1 Approval Record #20](20-task-v1-contract-approval-record.md).
  - D-03 Foundation 7 Fields & P1–P3 Decisions: [D-03 Approval Record #22](22-task-v1-d03-delta-approval-record.md).
  - State Machine Baseline: [DATN-94 / D-02 Contract Review](16-task-v1-state-machine-contract.md) (All 25 transitions currently `UNKNOWN / Enabled: NO`).
  - Architecture Seam: [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md) and [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md).
- **Scope & Implementation Gate:**
  - This document provides an exact source-ID inventory crosswalk, candidate contract specifications, explicit unresolved/disabled dispositions, an authority blocker register, and conditional test-oracle designs. It does **NOT** constitute human approval by itself and contains no backend application source code.
  - D-03 seven-field persistence (private slice) and D-04 runtime-seam boundaries remain completed within their accepted scopes and are neither reopened nor modified.
  - Only the exact D-03 private-slice behavior approved by [approval record #22](22-task-v1-d03-delta-approval-record.md) is enabled by this record. Every proposed public operation, extension field, authorization rule, and lifecycle transition below remains **NOT APPROVED / DISABLED** until the applicable Product, Architecture, and/or Security authority records a revision-specific disposition. DATN-97, DATN-99, DATN-100, and DATN-101 remain blocked by their Jira links until their own contract prerequisites are approved.

---

## 1. Executive Summary & Review Framework

The objective of **DATN-373 (D-13)** is to provide a source-linked disposition for every known Task V1 contract and lifecycle question. This revision (D13-R6) records the approved D-03 baseline, keeps every unapproved operation or transition disabled, and lists the authority evidence still required. It does not claim that every policy decision has received authority approval.

### 1.1. Accepted Baseline vs. Proposed Dispositions

To prevent unauthorized assumptions, all policy elements in this document are strictly classified into one of four deterministic states:

1. **`APPROVED`**: Behavior accepted in a formal human approval record, only within that record's stated scope (including the D-03 private slice in record #22).
2. **`PROPOSED_DISPOSITION`**: Concrete engineering specification formulated for review by the applicable authority role(s).
3. **`PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION`**: Candidate exclusion awaiting a Product decision; it is not a final V1 scope decision and the affected integration remains blocked.
4. **`UNKNOWN / DISABLED`**: No approved disposition exists. The operation/transition is excluded from implementation and must not be enabled by inference.

**Approval boundary:** A proposed route, DTO, error, role rule, test oracle, or candidate transition is review material only. It is not an accepted V1 contract. A downstream implementation may consume it only after revision-specific evidence from each applicable authority is recorded. The currently approved executable boundary remains the D-03 private slice; all public Task V1 operations in this document are disabled pending those decisions.

| Policy Domain | Accepted Baseline (approval records #20 / #22, within their stated scope) | Proposed Disposition in D-13-R6 (Awaiting applicable authority approval) | Status |
|---|---|---|---|
| **Data Foundation** | Exactly 7 fields approved for D-03 private slice: `_id`, `projectId`, `title`, `createdBy`, `createdAt`, `updatedAt`, `version`. | 8 candidate extension fields: `status`, `description`, `priority`, `assigneeId`, `teamId`, `dueDate`, `completedAt`, `tags`. | 7 Fields: `APPROVED`<br>Extension: `PROPOSED_DISPOSITION` |
| **Creation Event Contract** | D-03 §8 P3 is approved for private-slice creation only. | Preserves P3 exactly for that private slice. Whether public create reuses P3 or has another event schema remains unresolved; public create is disabled. Subsequent mutation events are candidate-only. | Private slice: `APPROVED`<br>Public create mapping: `UNKNOWN / DISABLED`<br>Mutation schema: `PROPOSED_DISPOSITION / DISABLED` |
| **Version Semantics** | Internal creation ordinal `1`. No public CAS/ETag semantics in private slice. | Introduces `expectedVersion` for optimistic concurrency control (OCC) on public mutations. | Baseline: `APPROVED`<br>OCC: `PROPOSED_DISPOSITION` |
| **Lifecycle Transitions** | All 25 cells in D-02 are disabled (`Enabled: NO`). | Records 8 candidate permitted and 17 candidate forbidden cells for authority review; none are enabled by this proposal. | All 25: `UNKNOWN / DISABLED`<br>Candidate: `PROPOSED_DISPOSITION` |
| **Organization Scope** | Project ownership and contextual Organization are approved at recommendation level; D-03 record #22 approves derived context for its private slice. Whether broader Task V1 needs a separately persisted `organizationId` remains unresolved. | For D-03 private-slice operations, derive Organization context from the owning Project through the trusted lookup; do not persist `organizationId` as a Task field. Broader V1 storage and lookup semantics remain unapproved. | Private slice: `APPROVED`<br>Broader V1: `UNKNOWN / DISABLED` |
| **History & Audit** | D-03 P3 atomic Task + creation-event persistence for private slice; no whole-task snapshots. | P3 remains approved only for that slice. Public mutation projection, retention, ordering, and ACL are candidate/unresolved and disabled. | Private P3: `APPROVED`<br>Public history: `UNKNOWN / DISABLED` / `PROPOSED_DISPOSITION` |
| **Mutation Reliability** | Commit exceptions do not prove rollback; must distinguish uncertain commit. | Client `operationId` (Idempotency Key), SHA-256 payload fingerprint, 24h dedupe, and three-way commit handling. | `PROPOSED_DISPOSITION` |
| **Work Note & Handover** | Integration optional; only enters V1 if contract approved by owner (Record #20 §16). | Candidate exclusion from Task V1 core pending Product decision. DATN-387 and DATN-452 remain blocked by Jira links. | `PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION` |

---

## 2. DATN-374 (D-13.1): Complete 1-to-1 Source Inventory & Crosswalk

In strict compliance with DATN-374 pass criteria, this master crosswalk maintains the exact original question identifiers from [D-01 Contract Readiness (Doc 13 §4)](13-task-v1-contract-readiness.md), [D-02 State Machine Review (Doc 16 §2–3, Doc 18 §2)](16-task-v1-state-machine-contract.md), and [D-03 Delta Approval (Doc 21 / 22)](22-task-v1-d03-delta-approval-record.md). All items from `SRC-13-Q1` through `SRC-13-Q9`, `SRC-D02-01` through `SRC-D02-10`, and D-03 follow-ups are represented 1-to-1.

### 2.1. Master Source Inventory Crosswalk

| Original Source ID | Source Reference | Exact Source Question / Item | Disposition Status | D-13-R6 Recorded Outcome / Candidate | Required Authority Role | Impacted Downstream Jira Issue | Test Oracle / Gate ID |
|---|---|---|---|---|---|---|---|
| **SRC-13-Q1** | Doc 13 §4.1 / Doc 20 §16 | **V1 Scope & Use Cases:** Exact UC-TM use cases included in V1; inclusion of Work Note / Handover. | `PROPOSED_DISPOSITION` / `PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION` | Create/list/detail/update, status, and assignment are candidates only; no public Task operation is approved by D-13. DELETE/archive/restore is absent and undecided (O32). Work Note and Handover exclusion awaits Product decision. | Product authority (name not assigned by D-13) | DATN-97, DATN-387, DATN-452 | O1, O2, O8, O12, O32 |
| **SRC-13-Q2** | Doc 13 §4.2 / Doc 20 §18, §19 | **Ownership & Relationships:** One Project per Task; 0..1 Team, 0..1 Assignee; Organization derivation. | `APPROVED` (project ownership/context only) / `PROPOSED_DISPOSITION` / `UNKNOWN / DISABLED` | One owning Project and contextual Organization follow the approved baseline; separate organization storage outside the D-03 private slice remains unresolved. Optional `teamId`/`assigneeId` fields and eligibility are proposals. Whether Team membership grants any Task scope, whether assignee must belong to the selected Team, and effects of Project Membership revocation on access, assignment references, history, and concurrent writes remain `UNKNOWN / DISABLED` (O31). | Product, Architecture, and Security authorities for their respective effects | DATN-97, DATN-99 (D-07), DATN-100 (D-08), DATN-101 (D-09) | O0, O1, O9, O12, O31 |
| **SRC-13-Q3** | Doc 13 §4.3 / Doc 21 §5 | **Field Dictionary & Constraints:** Exact field names, types, nullability, defaults, mutability, lengths. | `APPROVED` (7 fields for D-03 private slice only) / `PROPOSED_DISPOSITION` (8 fields) | D-03 private slice has exactly 7 approved fields. Eight extension fields are candidate-only and unavailable to public V1 until approved; title limits, description format/rendering, and tag duplicate semantics remain explicit approval gates. | Product authority; Security/Architecture for description rendering and handling | DATN-97, DATN-99, DATN-100 | O0, O1, O13, O14, O15, O32, O33 |
| **SRC-13-Q4** | Doc 13 §4.4 / Doc 16 §2 | **Lifecycle Catalogue & Terminals:** State enum catalogue, initial state, and terminal semantics. | `UNKNOWN / DISABLED` (all 25 cells) / `PROPOSED_DISPOSITION` | Five-state catalogue and cell dispositions are proposals only; all T01–T25 remain disabled and excluded from implementation pending explicit disposition. | Product authority; Architecture/Security where guards or effects apply | DATN-97, DATN-100 (D-08) | O1–O8, O18–O26 |
| **SRC-13-Q5** | Doc 13 §4.5 / Doc 20 §16, §32 | **Authorization & RBAC:** Actor, role, and scope permission matrix; cross-project isolation. | `POLICY CONFLICT UNDER REVIEW / UNKNOWN / DISABLED` | Candidate 4D RBAC uses `ADMIN`, `TEAM_LEADER`, `MEMBER`; permission, masking, and Project Admin behavior are not approved. Public operations remain disabled. | Product and Security authorities | DATN-97, DATN-99, DATN-100 | O9, O12, O31, O32 |
| **SRC-13-Q6** | Doc 13 §4.6 / ADR-010 §3 | **API Surface & Route Boundary:** Route schemas, pagination, filter grammar, Gateway vs. Internal Service. | `PROPOSED_DISPOSITION / UNKNOWN / DISABLED` | Seven Gateway operations and internal route details are candidates only. Exact proposal is in §3.4; malformed inputs, precedence, authentication failures, and omitted operations are explicitly unresolved in O32. No public route is enabled by this record. | Architecture authority; Product for operation scope; Security for trust and scope | DATN-97, DATN-99, DATN-100, DATN-101 | O1, O2, O4, O11, O12, O30, O32 |
| **SRC-13-Q7** | Doc 13 §4.7 / Doc 22 §1 | **Version, Mutation & Idempotency:** Version counter vs. public OCC; operation replay; uncertain commits. | `APPROVED` (D-03 creation ordinal only) / `PROPOSED_DISPOSITION` / `UNKNOWN / DISABLED` | D-03 starts `version` at 1. Public OCC, replay, key scope, expiry, and uncertain-commit behavior are candidates only; no public mutation is enabled. | Architecture authority; Product/Security where request behavior or trust scope applies | DATN-97, DATN-99, DATN-100 | O0, O10, O11, O16, O27, O28, O32 |
| **SRC-13-Q8** | Doc 13 §4.8 / Doc 21 §8 | **History Event Boundary:** Event coverage, projection, prohibition of whole-task snapshots, retention. | `APPROVED` (D-03 P3 creation event only) / `PROPOSED_DISPOSITION` / `UNKNOWN / DISABLED` | D-03 P3 remains exact for private create. Public-create mapping, mutation history schema, retention, ordering, ACL, and effects of membership revocation are unresolved proposals; no public history API is enabled. | Architecture and Security authorities | DATN-97, DATN-101 (D-09) | O0, O2, O8, O10, O17, O29, O31, O32 |
| **SRC-13-Q9** | Doc 13 §4.9 / Doc 20 §25; Doc 21 §10; Doc 22 §4 | **Durable Consumer & Outbox:** Transactional outbox requirement and event delivery queue. | `APPROVED DEFERRED` for D-03 private slice / `UNKNOWN / DISABLED` for broader V1 delivery | D-03 private slice creates local history only and publishes no event; no outbox/relay/queue is in that accepted slice. Any future durable consumer and broader V1 delivery are not approved or enabled. Name the consumer, purpose, owner, delivery/retry contract, and obtain Product/Architecture disposition before adding delivery infrastructure. | Product and Architecture authorities; Security if delivery crosses a trust boundary | DATN-97, DATN-101 (D-09), and any named consumer issue | O0; Q9 decision gate |
| **SRC-D02-01** | Doc 16 §2 | **Candidate State Meanings:** Semantic validation of `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`. | `PROPOSED_DISPOSITION / UNKNOWN / DISABLED` | Candidate definitions in §3.2; reason requirements are proposals only. | Product authority (name not assigned) | DATN-97, DATN-100 | O1, O2, O5, O7 |
| **SRC-D02-02** | Doc 16 §3 | **25-Cell Transition Matrix:** Cartesian evaluation of T01 through T25. | `UNKNOWN / DISABLED` (Baseline) / `PROPOSED_DISPOSITION` | All 25 cells `Enabled: NO` in baseline. Proposed candidate matrix: 8 Permitted vs. 17 Forbidden cells. | Product & Architecture | DATN-97, DATN-100 | O2–O8, O18–O26 |
| **SRC-D02-03** | Doc 16 §3 | **Transition Reasons:** Rules for mandatory reasons on state transitions. | `PROPOSED_DISPOSITION / UNKNOWN / DISABLED` | Candidate rule: mandatory `reason` (min 5 chars) on `BLOCKED`, `CANCELLED`, `RESUME`, `REOPEN`; optional on `START`, `COMPLETE`. Not enabled before Product disposition. | Product authority (name not assigned) | DATN-100 (D-08) | O4–O8, O18, O22, O25, O26 |
| **SRC-D02-04** | Doc 16 §4 | **Guard Layers G1–G6 & Actor Scope:** Validation, IAM active membership, Project/Team fence, freshness. | `PROPOSED_DISPOSITION` / `UNKNOWN / DISABLED` for revocation effects and races | G1–G6, active membership checks, masking, and freshness behavior are proposals. Post-revocation task access/status, assignment references, Team effects, history access, and race fencing remain unresolved and are not implemented by inference (O31). | Security and Architecture authorities; Product for assignment and lifecycle behavior | DATN-97, DATN-99, DATN-100, DATN-101 | O9, O12, O31 |
| **SRC-D02-05** | Doc 17 §2 | **Concurrency & CAS:** Aggregate versioning, stale conflict resolution, uncertain transaction boundaries. | `PROPOSED_DISPOSITION / UNKNOWN / DISABLED` | Candidate `expectedVersion` aggregate CAS; stale returns 409; three-way commit outcome handling. No public mutation is enabled. | Architecture authority; Product for client-visible conflicts | DATN-97, DATN-100 | O10, O11, O32 |
| **SRC-D02-06** | Doc 17 §3 | **Idempotency Namespace & Fingerprinting:** Uniqueness tuple, payload fingerprinting, and parameter normalization. | `PROPOSED_DISPOSITION / UNKNOWN / DISABLED` | Candidate tuple `(actorId, projectId, operationId)`, SHA-256 canonical payload hash, and mismatch 422. | Architecture authority; Security for actor/key trust | DATN-97, DATN-100 | O16, O32 |
| **SRC-D02-07** | Doc 17 §4 | **Operation Replay Resolution:** Replay cache, in-flight duplicate handling, denial caching prohibition. | `PROPOSED_DISPOSITION / UNKNOWN / DISABLED` | Candidate replay returns persisted result; in-flight duplicate 409; no denial caching. | Architecture authority; Security for denial caching policy | DATN-97, DATN-100 | O16, O27 |
| **SRC-D02-08** | Doc 17 §5 | **Deduplication Window & Proof Retention:** Key TTL, cleanup window, and post-expiry semantics. | `PROPOSED_DISPOSITION / UNKNOWN / DISABLED` | Candidate 24-hour TTL in Redis/Mongo; expired key treated as fresh request; no indefinite storage. | Architecture and Operations authorities | DATN-97 | O28 |
| **SRC-D02-09** | Doc 17 §6 | **Cross-Boundary Coordination & Handover:** Handover retry/compensation, operation ID propagation. | `PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION` | Handover assignment integration proposed excluded from V1; DATN-452 blocked pending owner contract. | Product & Architecture | DATN-452 | N/A (Blocked) |
| **SRC-D02-10** | Doc 16 §3 / Doc 18 §2 | **Event Schema & Audit Delta:** History representation, provenance fields, redaction of sensitive content. | `APPROVED` (D-03 P3 only) / `PROPOSED_DISPOSITION / UNKNOWN / DISABLED` | D-03 P3 creation event remains approved; mutation allowlist/delta, provenance, retention, and successor ACL are candidate-only. | Architecture and Security authorities | DATN-97, DATN-101 (D-09) | O0, O2, O8, O17, O29, O31 |
| **SRC-D03-P1** | Doc 22 §1 | **Private Slice Foundation:** Private create/read persistence primitives, task/history definitions. | `APPROVED` | Approved by record #22 for the D-03 private slice. It introduces no public API or status lifecycle. | Product authority evidence in approval record #22 | DATN-95, D-03 | O0 |
| **SRC-D03-P2** | Doc 22 §1 | **Exact 7 Foundation Fields:** `_id`, `projectId`, `title`, `createdBy`, `createdAt`, `updatedAt`, `version`. | `APPROVED` | Record #22 approves exactly seven non-null fields for the private slice; `version = 1`; `updatedAt = createdAt`. | Product authority evidence in approval record #22 | DATN-95, D-03 | O0 |
| **SRC-D03-P3** | Doc 22 §1 | **Atomic Creation History:** Exactly one creation event, atomic write, append-only history. | `APPROVED` | Record #22 approves one exact P3 creation event per committed Task version 1, with no content snapshots. | Product authority evidence in approval record #22 | DATN-95, D-03 | O0 |

---

## 3. DATN-375 (D-13.2): Authority Disposition & Contract Specification

### 3.1. Authority & Blocker Register

To ensure transparent governance, each unresolved policy is linked to its required authority role, exact evidence still required, and current implementation gate. No named approver is assigned here. Approval is accepted only when the record identifies the approving authority, this D13 revision, and the decision scope.

| Policy Area | Source Question IDs | Current Status | Governing Authority Role | Exact Action / Evidence Required to Close Gate | Impacted Issues Kept Blocked |
|---|---|---|---|---|---|
| **Lifecycle 25-Cell Matrix** | `SRC-13-Q4`, `SRC-D02-01–03` | `UNKNOWN / DISABLED` for all T01–T25; candidate matrix is not approved | Product authority; Architecture/Security for technical guard and effect choices | Record an explicit authority disposition for each cell and its actor guard/side effects, or explicitly exclude the transition from V1. Until then all 25 remain `Enabled: NO`; do not implement candidate outcomes. | DATN-97, DATN-100 (D-08) |
| **Extended Fields Dictionary** | `SRC-13-Q3` | `PROPOSED_DISPOSITION`; public fields not approved or enabled | Product authority; Security/Architecture for description rendering and handling | Approve or explicitly exclude each extension field and its constraints/defaults/mutability; resolve description format/rendering/sanitization and tag duplicate semantics. | DATN-97, DATN-99 (D-07), DATN-100 (D-08) |
| **Public OCC Version Semantics** | `SRC-13-Q7`, `SRC-D02-05` | `PROPOSED_DISPOSITION`; public mutations disabled | Architecture authority; Product for client-visible conflict behavior | Approve or explicitly exclude `expectedVersion`, stale-write status/code, and commit-uncertainty recovery behavior. | DATN-97, DATN-99, DATN-100, DATN-101 |
| **Internal Route & mTLS Trust** | `SRC-13-Q6` | `PROPOSED_DISPOSITION`; no new internal route enabled by D-13 | Architecture and Security authorities | Approve `/internal/tasks` route ownership, caller identity, credential validation, trusted actor/scope derivation, and failure semantics. | DATN-97 |
| **RBAC & Project Admin Scope** | `SRC-13-Q5`, `SRC-D02-04` | `POLICY CONFLICT UNDER REVIEW / UNKNOWN / DISABLED` | Security and Product authorities | Resolve Organization Admin access to private Projects versus Project Admin Task management; approve actors × actions × resources × scope, including exact deny/masking outcomes. | DATN-97, DATN-99, DATN-100 |
| **Team/Assignee Eligibility & Revocation Effects** | `SRC-13-Q2`, `SRC-D02-04` | `PROPOSED_DISPOSITION`; revocation effects and Team/Assignee relation `UNKNOWN / DISABLED` | Security and Product authorities; Architecture for freshness/fencing | Approve eligible Team/User scope, whether Team membership alone grants list/detail/history/transition access or any mutation permission, whether active Project membership is also required, whether assignee must belong to the selected Team, and post-revocation access/assignment/history effects. Decide automatic side effects (if any) and concurrent revoke-vs-mutation fencing. No Team-derived access, auto-clear/reassign, or special Task operation is enabled meanwhile (O31). | DATN-97, DATN-99, DATN-100, DATN-101 |
| **Public API Operation Schemas & Errors** | `SRC-13-Q6` | `PROPOSED_DISPOSITION`; all public operations disabled pending approval | Architecture authority; Product for field/validation decisions; Security for authorization outcomes | Approve or explicitly exclude each route, request/response schema, filters/pagination, validation precedence, stable error code/status, and cross-scope behavior. | DATN-97, DATN-99, DATN-100, DATN-101 |
| **API Edge Cases & Error Precedence** | `SRC-13-Q3`, `SRC-13-Q5–Q6` | `UNKNOWN / DISABLED`; listed endpoint errors are candidate-only | Product, Architecture, and Security authorities for the relevant rule | Record exact behavior and executable oracle for malformed path IDs; unsupported/invalid query values and ranges; search Unicode case-folding/normalization; priority sort order; null due-date ordering; offset pagination under concurrent inserts/deletes; missing or invalid `expectedVersion`; unknown body fields; tag trimming whitespace set and duplicate semantics; invalid or omitted idempotency keys and no-key uncertainty recovery; authentication versus validation ordering; and not-found versus cross-scope masking. Decide description format/rendering, and whether Task delete/archive/restore exists. Until decided, do not implement these unresolved outcomes. | DATN-97, DATN-99, DATN-100, DATN-101 |
| **Audit Event Schema & Provenance** | `SRC-13-Q8`, `SRC-D02-10` | `APPROVED` for D-03 P3 creation event only; public-create mapping and mutation events `UNKNOWN / DISABLED` or `PROPOSED_DISPOSITION` | Architecture and Security authorities; Product for event coverage | Keep D-03 P3 exact. Decide whether approved P3 applies to a future public create; approve or exclude mutation event types, allowlisted deltas, retention, ordering, deterministic pagination, read ACL, and membership-revocation behavior before public event/history routes are enabled. | DATN-97, DATN-101 (D-09) |
| **Idempotency & Replay Engine** | `SRC-D02-06–08` | `PROPOSED_DISPOSITION`; no public idempotency contract enabled | Architecture authority; Security for actor/key trust; Product for retry-visible results | Approve or explicitly exclude key namespace, normalization/fingerprint, retention, duplicate handling, denial caching, and uncertain commit recovery for each approved mutation. | DATN-97, DATN-99, DATN-100 |
| **Durable Consumer & Outbox** | `SRC-13-Q9`, Doc 21 §10, Doc 22 §4 | D-03 local-history-only deferral `APPROVED`; broader V1 delivery `UNKNOWN / DISABLED` | Product and Architecture authorities; Security if trust boundary changes | D-03 has no outbox/relay/queue and publishes no Task event. For any broader delivery, identify named consumer, purpose, owner, guarantees/retry/retention, and record Product/Architecture disposition before implementation. Do not add delivery infrastructure based only on the candidate schema. | DATN-97, DATN-101, any named consumer issue |
| **Work Note & Handover Exclusion** | `SRC-13-Q1`, `SRC-D02-09` | `PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION` | Product authority; Architecture for integration boundary | Record Product decision to include or exclude each integration from Task V1. Existing Jira dependencies continue to block the dependent work; this proposal is not a final scope decision. | DATN-387, DATN-452 |

---

### 3.2. Task Lifecycle State Machine (SRC-13-Q4, SRC-D02-01–03)

#### A. Candidate State Catalogue (Not Approved)
The following catalogue is proposal material only. No public Task state is enabled by this document; the D-02 baseline remains all 25 cells `UNKNOWN / DISABLED` until the authority disposition is recorded.
1. `TODO`: Initial state upon creation. Task persisted but execution has not begun.
2. `IN_PROGRESS`: Active execution by eligible assignee.
3. `BLOCKED`: Execution halted by an external impediment. Mandatory `reason` required.
4. `DONE`: Execution completed. Can be reopened via `REOPEN`. Automatically sets `completedAt = now()`.
5. `CANCELLED`: Terminal state. Work discarded or abandoned. In V1, no exits are permitted.

#### B. Complete 25-Cell State Transition Matrix Evaluation
**Baseline Authority Rule:** Currently, all 25 cells are **`UNKNOWN / DISABLED (Enabled: NO)`** under baseline DATN-94. The table below records candidate dispositions for review only. Neither `Candidate Permitted` nor `FORBIDDEN` changes a cell's baseline or enables it; each cell remains excluded from implementation until an authority either approves it with actor guard and side effects or explicitly excludes it from V1.

| Cell | From State | To State | Baseline Status | Proposed Candidate Disposition | Trigger Command | Permitted Actor Roles | Guard Conditions & Reason Rules | Side Effects & Event | Test Oracle |
|---|---|---|---|---|---|---|---|---|---|
| **T01** | `TODO` | `TODO` | DISABLED | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. | None (`H0`). | O4 |
| **T02** | `TODO` | `IN_PROGRESS` | DISABLED | **Candidate Permitted** | `START` | Assignee, `TEAM_LEADER`, `ADMIN` | Task must have `assigneeId != null`. Optional reason. | `version++`. Emits `TASK_STATUS_TRANSITIONED`. | O2 |
| **T03** | `TODO` | `BLOCKED` | DISABLED | **FORBIDDEN** | Direct-Block | None | Work not started cannot be blocked. Must `START` first. 409 Conflict. | None (`H0`). | O18 |
| **T04** | `TODO` | `DONE` | DISABLED | **FORBIDDEN** | Direct-Complete | None | Work not started cannot be completed directly. 409 Conflict. | None (`H0`). | O3 |
| **T05** | `TODO` | `CANCELLED` | DISABLED | **Candidate Permitted** | `CANCEL` | `ADMIN`, `TEAM_LEADER`, Creator | Mandatory `reason` (min 5 chars). | `version++`. Emits `TASK_STATUS_TRANSITIONED`. | O6 |
| **T06** | `IN_PROGRESS` | `TODO` | DISABLED | **FORBIDDEN** | Reset | None | Cannot unstart active work back to TODO. 409 Conflict. | None (`H0`). | O19 |
| **T07** | `IN_PROGRESS` | `IN_PROGRESS` | DISABLED | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. | None (`H0`). | O4 |
| **T08** | `IN_PROGRESS` | `BLOCKED` | DISABLED | **Candidate Permitted** | `BLOCK` | Assignee, `TEAM_LEADER`, `ADMIN` | Mandatory `reason` (min 5 chars) stating impediment. | `version++`. Emits `TASK_STATUS_TRANSITIONED`. | O5 |
| **T09** | `IN_PROGRESS` | `DONE` | DISABLED | **Candidate Permitted** | `COMPLETE` | Assignee, `TEAM_LEADER`, `ADMIN` | Optional completion note. | Sets `completedAt = now()`, `version++`. Emits event. | O20 |
| **T10** | `IN_PROGRESS` | `CANCELLED` | DISABLED | **Candidate Permitted** | `CANCEL` | `ADMIN`, `TEAM_LEADER`, Creator | Mandatory `reason` (min 5 chars). | `version++`. Emits `TASK_STATUS_TRANSITIONED`. | O6 |
| **T11** | `BLOCKED` | `TODO` | DISABLED | **FORBIDDEN** | Reset | None | Cannot reset blocked work to unstarted. 409 Conflict. | None (`H0`). | O21 |
| **T12** | `BLOCKED` | `IN_PROGRESS` | DISABLED | **Candidate Permitted** | `RESUME` | Assignee, `TEAM_LEADER`, `ADMIN` | Mandatory `reason` (min 5 chars) detailing resolution. | `version++`. Emits `TASK_STATUS_TRANSITIONED`. | O22 |
| **T13** | `BLOCKED` | `BLOCKED` | DISABLED | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. | None (`H0`). | O4 |
| **T14** | `BLOCKED` | `DONE` | DISABLED | **FORBIDDEN** | Direct-Complete | None | Cannot complete while blocked. Must `RESUME` first. 409 Conflict. | None (`H0`). | O23 |
| **T15** | `BLOCKED` | `CANCELLED` | DISABLED | **Candidate Permitted** | `CANCEL` | `ADMIN`, `TEAM_LEADER`, Creator | Mandatory `reason` (min 5 chars). | `version++`. Emits `TASK_STATUS_TRANSITIONED`. | O6 |
| **T16** | `DONE` | `TODO` | DISABLED | **FORBIDDEN** | Reset | None | Cannot uncomplete to unstarted. 409 Conflict. | None (`H0`). | O24 |
| **T17** | `DONE` | `IN_PROGRESS` | DISABLED | **Candidate Permitted** | `REOPEN` | `ADMIN`, `TEAM_LEADER`, Creator | Mandatory `reason` (min 5 chars) explaining defect/rejection. | Clears `completedAt = null`, `version++`. Emits event. | O8 |
| **T18** | `DONE` | `BLOCKED` | DISABLED | **FORBIDDEN** | Direct-Block | None | Completed work cannot be blocked directly. Reopen first. | None (`H0`). | O25 |
| **T19** | `DONE` | `DONE` | DISABLED | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. | None (`H0`). | O4 |
| **T20** | `DONE` | `CANCELLED` | DISABLED | **FORBIDDEN** | Cancel-Done | None | Completed work cannot be cancelled in V1. 409 Conflict. | None (`H0`). | O26 |
| **T21** | `CANCELLED` | `TODO` | DISABLED | **FORBIDDEN** | Restore | None | Terminal state. No exit transitions in V1. 409 Conflict. | None (`H0`). | O7 |
| **T22** | `CANCELLED` | `IN_PROGRESS` | DISABLED | **FORBIDDEN** | Reopen-Cancel | None | Terminal state. No exit transitions in V1. 409 Conflict. | None (`H0`). | O7 |
| **T23** | `CANCELLED` | `BLOCKED` | DISABLED | **FORBIDDEN** | Restore-Block | None | Terminal state. No exit transitions in V1. 409 Conflict. | None (`H0`). | O7 |
| **T24** | `CANCELLED` | `DONE` | DISABLED | **FORBIDDEN** | Complete-Cancel | None | Terminal state. No exit transitions in V1. 409 Conflict. | None (`H0`). | O7 |
| **T25** | `CANCELLED` | `CANCELLED` | DISABLED | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. | None (`H0`). | O4 |

---

### 3.3. Field Dictionary & Schema Specification (SRC-13-Q3)

#### A. Approved Foundation Fields (D-03 Private Slice — Approval Record #22)
These 7 fields are accepted only for the D-03 private creation slice. Their presence does not approve a public Task API or public mutation semantics:
- `_id`: ObjectId, immutable, system-generated primary key.
- `projectId`: ObjectId, immutable, required owning Project reference.
- `title`: String, required at private-slice creation; original string preserved, non-empty outside set $W$, non-unique. Public editability is not approved.
- `createdBy`: ObjectId, immutable, server-derived authenticated actor ID.
- `createdAt`: ISODate, immutable, server-derived UTC timestamp.
- `updatedAt`: ISODate, server-derived UTC timestamp, initially equal to `createdAt`; public update semantics are not approved.
- `version`: Number, creation ordinal `1` in D-03; public increment/CAS semantics are not approved by the baseline.

The candidate public-create DTO proposes a `title` maximum of 500 Unicode code points. This is not part of the approved D-03 private-slice rule, which has no business length cap; Product approval is required before using the public constraint.

#### B. Proposed Extension Fields for Task V1 (Awaiting Authority Disposition)

| Field Name | Type | Storage Type | Nullable | Default | Mutability | Constraints & Validation Semantics |
|---|---|---|---|---|---|---|
| `status` | String | `enum` | No | `"TODO"` | Mutable (Status API only) | Enum: `["TODO", "IN_PROGRESS", "BLOCKED", "DONE", "CANCELLED"]`. Governed by 25-cell matrix. |
| `description` | String | `string` | Yes | `null` | Mutable | Optional; proposed maximum 5,000 Unicode code points; clearable by passing `null`. Whether the value is plain text or Markdown, and any rendering/sanitization policy, remains `UNKNOWN / DISABLED`; no renderer is enabled by this proposal. |
| `priority` | String | `enum` | No | `"MEDIUM"` | Mutable | Enum: `["LOW", "MEDIUM", "HIGH", "URGENT"]`. |
| `assigneeId` | ObjectId | `ObjectId` | Yes | `null` | Mutable | Cardinality 0..1. Must reference active `User` with active `ProjectMembership` in `projectId`. Clearable by passing `null`. |
| `teamId` | ObjectId | `ObjectId` | Yes | `null` | Mutable | Cardinality 0..1. Must reference active `Team` in `projectId`. Clearable by passing `null`. |
| `dueDate` | Date | `ISODate` | Yes | `null` | Mutable | ISO-8601 UTC timestamp (`YYYY-MM-DDTHH:mm:ss.sssZ`). Validation rule: `dueDate >= createdAt`. Clearable by passing `null`. |
| `completedAt` | Date | `ISODate` | Yes | `null` | Server-derived | Automatically set to `now()` on transition T09 (`COMPLETE`). Automatically reset to `null` on T17 (`REOPEN`). |
| `tags` | Array | `[String]` | No | `[]` | Mutable | Max 10 tags; each tag max 30 Unicode code points; trim each value before storage and reject values empty after trimming. **Non-nullable.** To clear tags, client must pass `[]`; passing `null` is a candidate `400 Bad Request`. Whether duplicate tags are preserved or rejected remains `UNKNOWN / DISABLED`. |

#### C. Derived Context Boundary
- `organizationId`: Contextually derived from owning `Project.organizationId` via trusted Project Service lookup. In compliance with the D-03 private-slice boundary in approval record #22, `organizationId` is **NOT** persisted as an independent Task field.

---

### 3.4. REST API Surface & Network Boundary (SRC-13-Q6)

The routes, DTOs, filters, status codes, and error codes in this section are **candidate contract text only**. None of the seven proposed public operations is approved or enabled by D-13. The unresolved operations are excluded from implementation until their row in §3.1 has revision-specific authority evidence. D-03's private create/read persistence seam is not a public HTTP route. No Task DELETE/archive/restore route is proposed; whether one belongs in V1 remains undecided and excluded.

#### A. Network & Route Boundary Separation (ADR-010)
- **Public API Gateway / BFF Boundary:** `/api/v1/projects/:projectId/tasks...`
  - Gateway validates client session JWT, enforces tenant isolation, and proxies to internal Task Service.
- **Internal Service Boundary:** `/internal/tasks...`
  - Routes carry `/internal` prefix and require internal service authentication (mTLS / shared internal service secret `x-service-token`).
  - Task Service consumes and verifies trusted internal context headers: `x-organization-id`, `x-project-id`, `x-actor-id`, `x-actor-role`. Direct requests lacking verified internal credentials are rejected with `401 Unauthorized`.

#### B. Response & Error DTO Specifications

##### Response DTO: `TaskResponseDTO`
```typescript
interface TaskResponseDTO {
  id: string;                         // Hex string of _id
  projectId: string;                  // Hex string of projectId
  title: string;                      // Persisted title string
  description: string | null;         // Null if not set
  status: "TODO" | "IN_PROGRESS" | "BLOCKED" | "DONE" | "CANCELLED";
  priority: "LOW" | "MEDIUM" | "HIGH" | "URGENT";
  assigneeId: string | null;          // Hex string or null
  teamId: string | null;              // Hex string or null
  dueDate: string | null;             // ISO-8601 UTC string or null
  completedAt: string | null;         // ISO-8601 UTC string or null
  tags: string[];                     // Array of tag strings (non-null)
  createdBy: string;                  // Hex string of creator
  createdAt: string;                  // ISO-8601 UTC string
  updatedAt: string;                  // ISO-8601 UTC string
  version: number;                    // Integer >= 1
}
```

##### Audit History Response DTO: `TaskEventResponseDTO`
```typescript
interface TaskEventResponseDTO {
  id: string;                         // Hex string of event _id
  taskId: string;                     // Hex string of taskId
  projectId: string;                  // Hex string of projectId
  eventType: TaskEventType;
  actorId: string;                    // Hex string of actor
  actorType: "USER" | "SYSTEM";       // Actor category
  source: "WEB" | "API" | "INTERNAL_SERVICE";
  timestamp: string;                  // ISO-8601 UTC string
  version: number;                    // Resulting task version
  operationId?: string;               // Idempotency key if supplied
  changedFields: TaskMutableField[];  // Exact allowlist of updated field names
  delta: TaskEventDelta;              // Event-specific allowlist; no arbitrary keys or snapshots
}
```

##### Standard Error Response Schema
```json
{
  "success": false,
  "error": {
    "code": "TASK_STATE_TRANSITION_CONFLICT",
    "message": "Cannot transition task from 'TODO' to 'DONE'. Direct completion is forbidden; task must be started first.",
    "details": {
      "currentStatus": "TODO",
      "targetStatus": "DONE",
      "allowedTransitions": ["IN_PROGRESS", "CANCELLED"]
    }
  }
}
```

#### C. Endpoint Specifications

##### 1. Create Task
- **Route:** `POST /api/v1/projects/:projectId/tasks`
- **Headers:** `Idempotency-Key` (Optional UUID v4 for `operationId`).
- **Request Body:**
  ```json
  {
    "title": "string (required, min 1 non-W code point, max 500 Unicode code points; candidate public limit)",
    "description": "string | null (optional, max 5000 Unicode code points; format/rendering unresolved)",
    "priority": "LOW | MEDIUM | HIGH | URGENT (optional, default MEDIUM)",
    "assigneeId": "string | null (optional, valid ObjectId)",
    "teamId": "string | null (optional, valid ObjectId)",
    "dueDate": "string | null (optional, ISO-8601 UTC timestamp)",
    "tags": ["string"] (optional, max 10 tags, each max 30 Unicode code points; trim and reject blank; non-nullable; duplicate behavior unresolved)
  }
  ```
- **Responses:**
  - `201 Created`: `{ "success": true, "data": TaskResponseDTO }`.
  - `400 Bad Request`: `TASK_VALIDATION_ERROR`, `INVALID_TITLE_FORMAT`, `TAGS_MUST_BE_ARRAY`, `INVALID_DUE_DATE`.
  - `404 Not Found`: `PROJECT_NOT_FOUND` (if project does not exist or caller is not active member).
  - `422 Unprocessable Entity`: `ASSIGNEE_NOT_PROJECT_MEMBER`, `TEAM_NOT_IN_PROJECT`.

##### 2. List Project Tasks (Deterministic Pagination & Filtering)
- **Route:** `GET /api/v1/projects/:projectId/tasks`
- **Query Grammar:**
  - `status`: Exact enum or comma-separated list (e.g. `?status=TODO,IN_PROGRESS`).
  - `priority`: Exact enum match (e.g. `?priority=HIGH`).
  - `assigneeId`: Exact ObjectId hex string, or `"null"` for unassigned tasks.
  - `teamId`: Exact ObjectId hex string, or `"null"` for tasks without a team.
  - `search`: Literal substring search on `title`, case-insensitive; regex metacharacters are escaped, max 100 Unicode code points. (Candidate behavior; final input errors remain gated by O32.)
  - `page`: Integer $\ge 1$ (default: `1`).
  - `limit`: Integer $1 \le \text{limit} \le 100$ (default: `20`).
  - `sort`: Default `-createdAt`. Allowed keys: `createdAt`, `-createdAt`, `updatedAt`, `-updatedAt`, `dueDate`, `-dueDate`, `priority`, `-priority`.
  - **Candidate Tie-Breaker Rule:** Query engine appends `_id: 1` as secondary sort to produce a deterministic total order for a fixed dataset. This does not prevent offset-page drift when rows are inserted/deleted; snapshot or cursor consistency semantics remain unresolved under O32, so the list route stays disabled.
- **Responses:**
  - `200 OK`: `{ "success": true, "data": TaskResponseDTO[], "pagination": { "page": 1, "limit": 20, "total": 45, "totalPages": 3 } }`.
  - `404 Not Found`: `PROJECT_NOT_FOUND`.

##### 3. Get Task Detail
- **Route:** `GET /api/v1/projects/:projectId/tasks/:taskId`
- **Responses:**
  - `200 OK`: `{ "success": true, "data": TaskResponseDTO }`.
  - `404 Not Found`: `TASK_NOT_FOUND` (also returned if actor is not an active member of `projectId`, masking resource existence).

##### 4. Update Task Metadata (Omitted vs. Null Semantics)
- **Route:** `PATCH /api/v1/projects/:projectId/tasks/:taskId`
- **Headers:** `Idempotency-Key` (Optional UUID v4 for `operationId`; candidate behavior under §3.7).
- **Semantics:**
  - Omitted fields are left unchanged.
  - Passing `null` on nullable fields (`description`, `dueDate`) clears their value.
  - Passing `[]` on `tags` clears tags. Passing `null` on `tags` returns `400 Bad Request`.
- **Request Body:**
  ```json
  {
    "title": "string (optional; non-W predicate; max 500 Unicode code points; candidate public limit)",
    "description": "string | null (optional, max 5000 Unicode code points; format/rendering unresolved)",
    "priority": "LOW | MEDIUM | HIGH | URGENT (optional)",
    "dueDate": "string | null (optional, ISO-8601 UTC timestamp)",
    "tags": ["string"] (optional, max 10 tags, each max 30 Unicode code points; non-nullable; trimming/duplicate details gated),
    "expectedVersion": "integer >= 1"
  }
  ```
- **Responses:**
  - `200 OK`: `{ "success": true, "data": TaskResponseDTO }`.
  - `400 Bad Request`: `TASK_VALIDATION_ERROR`, `TAGS_MUST_BE_ARRAY`, `INVALID_DUE_DATE`.
  - `403 Forbidden`: `INSUFFICIENT_TASK_PERMISSIONS`.
  - `404 Not Found`: `TASK_NOT_FOUND`.
  - `409 Conflict`: `CONCURRENT_VERSION_CONFLICT`.

##### 5. Execute State Transition (Unified Target Status Grammar)
- **Route:** `PATCH /api/v1/projects/:projectId/tasks/:taskId/status`
- **Headers:** `Idempotency-Key` (Optional UUID v4 for `operationId`).
- **Request Body:**
  ```json
  {
    "targetStatus": "TODO | IN_PROGRESS | BLOCKED | DONE | CANCELLED (required)",
    "reason": "string (required min 5 chars for BLOCKED/CANCELLED/RESUME/REOPEN; optional for START/COMPLETE)",
    "expectedVersion": 2
  }
  ```
- **Semantics:** `targetStatus` accepts any valid lifecycle enum. Invalid transitions (e.g. resets to `TODO` via T06/T11/T16/T21) pass DTO enum validation but are evaluated and rejected at the business lifecycle layer returning `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`).
- **Responses:**
  - `200 OK`: `{ "success": true, "data": TaskResponseDTO }`.
  - `400 Bad Request`: `MANDATORY_TRANSITION_REASON_MISSING`.
  - `403 Forbidden`: `INSUFFICIENT_TRANSITION_PERMISSIONS`.
  - `404 Not Found`: `TASK_NOT_FOUND`.
  - `409 Conflict`: `TASK_STATE_TRANSITION_CONFLICT`, `CONCURRENT_VERSION_CONFLICT`.

##### 6. Assign or Clear Assignment
- **Route:** `PATCH /api/v1/projects/:projectId/tasks/:taskId/assignee`
- **Headers:** `Idempotency-Key` (Optional UUID v4 for `operationId`).
- **Request Body:**
  ```json
  {
    "assigneeId": "string | null (required; pass null to clear assignee)",
    "teamId": "string | null (optional; pass null to clear team)",
    "expectedVersion": 2
  }
  ```
- **Patch semantics:** `assigneeId` is required; `null` clears it. Omitted `teamId` leaves the current Team unchanged; `teamId: null` clears it. `expectedVersion` is the candidate concurrency precondition.
- **Responses:**
  - `200 OK`: `{ "success": true, "data": TaskResponseDTO }`.
  - `403 Forbidden`: `INSUFFICIENT_PROJECT_PERMISSIONS` (plain members cannot reassign).
  - `404 Not Found`: `TASK_NOT_FOUND`.
  - `409 Conflict`: `CONCURRENT_VERSION_CONFLICT`.
  - `422 Unprocessable Entity`: `ASSIGNEE_NOT_PROJECT_MEMBER`, `TEAM_NOT_IN_PROJECT`.

##### 7. Get Task Audit History Log
- **Route:** `GET /api/v1/projects/:projectId/tasks/:taskId/events`
- **Query Parameters:** `page` (default 1), `limit` (default 20, max 100).
- **Responses:**
  - `200 OK`: `{ "success": true, "data": TaskEventResponseDTO[], "pagination": { "page": 1, "limit": 20, "total": 12, "totalPages": 1 } }`.
  - `404 Not Found`: `TASK_NOT_FOUND`.
  - **Unresolved query behavior:** Event ordering, deterministic tie-breaker, pagination edge cases, retention, and read-scope behavior are not approved; see §3.1 and O31–O32. This route remains disabled.

#### D. Unresolved API Input and Error Cases (O32)
The route examples above list candidate success responses and selected candidate errors, but do not establish the following outcomes. Each remains `UNKNOWN / DISABLED` until the relevant authority records a disposition: malformed path IDs; unsupported or malformed query filters and pagination values; missing/non-integer/non-positive `expectedVersion`; unknown or conflicting body fields; malformed idempotency keys; authentication-versus-validation precedence; exact not-found versus cross-scope error masking; and history ordering, tie-breaker, and pagination boundaries. O32 enumerates the required tests without guessing their status or error code. The seven proposed operations and any unlisted delete/archive/restore behavior remain excluded from implementation until these decisions are closed.

---

### 3.5. Role-Based Access Control & Policy Conflict Disclosure (SRC-13-Q5)

#### A. Role Alignment & Conflict Disclosure
The permission baseline in [`02_ACTORS_ROLES_AND_PERMISSIONS.md`](../02_ACTORS_ROLES_AND_PERMISSIONS.md) and [`12-continuum-task-management-use-cases.md`](12-continuum-task-management-use-cases.md) §3 contains an unresolved policy tension:
- **Baseline Constraint:** Organization `ADMIN` does not possess default read access to private Project contents; assignment and cancellation are scoped to `TEAM_LEADER`.
- **D-13 Proposal:** Grants Project-level `ADMIN` management oversight over all tasks in the project.
- **Formal Status:** **`POLICY CONFLICT UNDER REVIEW (Awaiting Security & Product Disposition)`**. The table below is a candidate matrix for review only and does not govern runtime behavior before approval.

#### B. Candidate 4D Authorization Matrix: Role $\times$ Action $\times$ Resource $\times$ Scope

| Action Code | Target Operation | Required Role | Ownership / Guard Condition | Non-Member / Cross-Scope Outcome |
|---|---|---|---|---|
| `TASK_CREATE` | `POST /tasks` | `MEMBER` | Active `ProjectMembership` in target `projectId`. | `404 Not Found` (Mask project existence) |
| `TASK_READ` | `GET /tasks` (List/Detail/Events) | `MEMBER` | Active member of `projectId`. | `404 Not Found` |
| `TASK_EDIT_META` | `PATCH /tasks/:taskId` | `MEMBER` | Must be: (a) Project `ADMIN`, (b) `TEAM_LEADER`, (c) `assigneeId == actorId`, or (d) `createdBy == actorId`. | `404 Not Found` (or `403 Forbidden` if member lacking role) |
| `TASK_ASSIGN` | `PATCH /tasks/:taskId/assignee` | `TEAM_LEADER`; Project `ADMIN` is a contested candidate | Candidate rule allows Project `ADMIN` or `TEAM_LEADER`; plain `MEMBER` cannot reassign. Project Admin behavior remains under §3.1 policy conflict. | `403 Forbidden` (candidate; exact cross-scope result pending approval) |
| `TASK_TRANSITION_WORK` | `START`, `BLOCK`, `RESUME`, `COMPLETE` | `MEMBER` | Must be assigned to task (`assigneeId == actorId`), or hold `TEAM_LEADER` / `ADMIN`. | `403 Forbidden` |
| `TASK_CANCEL` | `CANCEL` (T05, T10, T15) | `MEMBER` | Must be: Project `ADMIN`, `TEAM_LEADER`, or original `createdBy`. | `403 Forbidden` |
| `TASK_REOPEN` | `REOPEN` (T17) | `MEMBER` | Must be: Project `ADMIN`, `TEAM_LEADER`, or original `createdBy`. | `403 Forbidden` |

*Candidate Scope Rules (Not Approved):*
- **Team Scope:** The proposal says members of a selected Team inherit task visibility. Whether Team membership alone grants list/detail/history/transition access, whether active Project membership is also required, and whether Team membership grants any mutation permission remain `UNKNOWN / DISABLED` under O31. No Team-derived Task access is enabled by this proposal.
- **Successor ACL:** Per Task Use Cases §7, successors only view event history of tasks transferred to them.
- **Out-of-scope operation:** Comment creation is excluded from the candidate Task V1 surface.

---

### 3.6. Audit History Event Schema & Provenance (SRC-13-Q8, ADR-010 §7)

#### A. Approved Baseline Event Contract (D-03 §8 P3 Baseline)
For the private creation primitive approved in record #22, the schema is fixed and immutable within that slice:
- `_id`: ObjectId allocated before transaction.
- `taskId`: ObjectId matching created Task `_id`.
- `projectId`: ObjectId matching Task `projectId`.
- `eventName`: String `"TASK_CREATED"`.
- `actorType`: `"USER"`.
- `actorId`: ObjectId equal to `createdBy`.
- `source`: `"HUMAN"`.
- `changedFields`: Exact array `["projectId", "title", "createdBy", "createdAt", "updatedAt", "version"]` (does **not** include `_id`).
- `taskVersion`: Integer `1`.
- `occurredAt`: BSON Date, identical to Task `createdAt`.
- `operationId`: Server-generated UUID v4 string.
- `correlationId`: Server requestId or UUID fallback.
- **Invariants:** No content snapshots, no PII, no generic payload object.

#### B. Proposed Task V1 Mutation Event Schema (Awaiting Authority Disposition)
This candidate schema is for post-creation public mutations only; it does not replace, extend, or rename the approved D-03 P3 creation event. The public-create event contract and whether the public API reuses P3 remain unresolved in §3.1. Any such public create stays disabled until Product/Architecture approval records the exact schema. For subsequent public mutations (`TASK_STATUS_TRANSITIONED`, `TASK_ASSIGNMENT_CHANGED`, `TASK_METADATA_UPDATED`), the proposed schema extends provenance per ADR-010 §7 while preserving the non-snapshot rule:

```typescript
interface TaskEventRecord {
  _id: ObjectId;                     // Unique event identifier
  taskId: ObjectId;                  // Target task reference
  projectId: ObjectId;               // Owning project
  organizationId: ObjectId;          // Contextual organization reference
  actorId: ObjectId;                 // Authenticated user initiating mutation
  actorType: "USER" | "SYSTEM";      // Actor classification
  source: "WEB" | "API" | "INTERNAL_SERVICE"; // Provenance channel
  eventType: TaskEventType;          // Event classification
  operationId?: string;              // Client-supplied idempotency key
  correlationId?: string;            // Distributed trace correlation identifier
  timestamp: Date;                   // UTC server timestamp
  version: number;                   // Resulting task version
  changedFields: TaskMutableField[]; // Exact allowlist of modified field names
  delta: TaskEventDelta;             // Discriminated payload (NO snapshots)
}

type TaskStatus = "TODO" | "IN_PROGRESS" | "BLOCKED" | "DONE" | "CANCELLED";

type TaskMutableField =
  | "title"
  | "description"
  | "priority"
  | "status"
  | "assigneeId"
  | "teamId"
  | "dueDate"
  | "completedAt"
  | "tags";

type TaskEventType =
  | "TASK_METADATA_UPDATED"
  | "TASK_STATUS_TRANSITIONED"
  | "TASK_ASSIGNMENT_CHANGED";

type TaskEventDelta =
  | { type: "STATUS_TRANSITION"; fromStatus: TaskStatus; toStatus: TaskStatus; reason?: string }
  | { type: "ASSIGNMENT_CHANGED"; previousAssigneeId: ObjectId | null; newAssigneeId: ObjectId | null; previousTeamId?: ObjectId | null; newTeamId?: ObjectId | null }
  | { type: "METADATA_UPDATED"; updatedScalarFields: TaskMutableField[] };
```

**Candidate cross-field invariants:** `TASK_STATUS_TRANSITIONED` pairs only with `STATUS_TRANSITION` and `changedFields == ["status"]`; `TASK_ASSIGNMENT_CHANGED` pairs only with `ASSIGNMENT_CHANGED` and `changedFields` contains only `assigneeId` and/or `teamId`; `TASK_METADATA_UPDATED` pairs only with `METADATA_UPDATED`, and `changedFields` exactly matches `updatedScalarFields`, limited to `title`, `description`, `priority`, `dueDate`, and `tags`. O17 must reject mismatched event/delta pairs and extra keys. These invariants remain proposed and disabled until the event contract is approved.

---

### 3.7. Mutation Reliability, Idempotency & Three-Way Commit Model (SRC-13-Q7, ADR-010 §6)

#### A. Idempotency Key Semantics
- **Key Header:** `Idempotency-Key` (Client-supplied UUID v4).
- **Uniqueness Scope:** Scoped to the tuple `(actorId, projectId, operationId)`.
- **Candidate Coverage:** Create, metadata update, assignment, and status mutation routes accept the optional header. Behavior when it is omitted, including uncertain-commit recovery without a client key, remains unresolved under O32.
- **Payload Fingerprinting:** Task Service computes a SHA-256 hash over the HTTP method, normalized route/resource identifiers, and canonical JSON request body (excluding the idempotency header), so the same key and body cannot replay a response across different operations or Task resources.
- **Deduplication Window:** Stored in Redis / MongoDB idempotency collection with a 24-hour TTL.
- **Replay Behavior:**
  - Matching `operationId` + matching SHA-256 within 24h: Returns the cached HTTP response and persisted state without incrementing `version` or writing history (`H0`).
  - Matching `operationId` + mismatched SHA-256: Returns `422 Unprocessable Entity` (`IDEMPOTENCY_KEY_PAYLOAD_MISMATCH`).
  - Concurrent in-flight duplicate: Returns `409 Conflict` (`CONCURRENT_OPERATION_IN_PROGRESS`).
  - After 24h expiry: Key is pruned; identical `operationId` is treated as a fresh request.

#### B. Three-Way Commit Outcome Handling
In distributed MongoDB replica set transactions, commit uncertainty is resolved through a deterministic three-way model:

1. **`CONFIRMED_SUCCESS`:** Both Task mutation and `task_events` record commit atomically. Returns `200 OK` or `201 Created`.
2. **`CONFIRMED_REJECTED / ABORTED`:** Transaction confirms abort or validation failure. State and version remain unchanged; no event is written (`H0`). Returns `400 / 403 / 404 / 409 / 422`.
3. **`UNCERTAIN`:** Client or driver experiences network disconnect or timeout while awaiting transaction commit acknowledgment.
   - **Invariant:** The commit may have succeeded on the primary. An exception alone does **NOT** prove rollback.
   - **Client Invariant:** The client **MUST NOT** generate a fresh `operationId`. The client must either:
     (a) Resubmit the request with the identical `operationId` to retrieve the cached result via replay resolution; or
     (b) Issue `GET /tasks/:taskId` to observe the persisted `version`.

---

## 4. DATN-376 (D-13.3): Downstream Acceptance & Dependency Trace

### 4.1. Downstream Jira Task Dependency Trace

This register records the current Jira dependency snapshot checked on 2026-10-18. DATN-373 has Jira `Blocks` links to each listed downstream issue; their displayed workflow status is still `To Do`, not a Jira status named `BLOCKED`. The links are the dependency evidence; the status snapshot may change independently.

| Jira Key | Official Issue Summary | Relationship to DATN-373 | Governing D-13-R6 Sections / Gates | Jira Status at Check |
|---|---|---|---|---|
| **DATN-97** | D-05 Task Core BE | **BLOCKED** by DATN-373 Jira link | §3.1 gates, §3.3 fields, §3.4 API, §3.5 authorization, §3.6 history, §3.7 reliability; O31–O32 | `To Do` |
| **DATN-99** | D-07 Task Assignment BE | **BLOCKED** by DATN-373 Jira link | §3.1 gates, §3.3 assignment fields, §3.4 API, §3.5 authorization, §3.6 history, §3.7 reliability; O31–O32 | `To Do` |
| **DATN-100** | D-08 Task Lifecycle Enforcement BE | **BLOCKED** by DATN-373 Jira link | §3.1 lifecycle/authority gates, §3.2 candidate matrix, §3.4 status API, §3.5 authorization, §3.6 history, §3.7 concurrency; O32 | `To Do` |
| **DATN-101** | D-09 Task History & Event Integrity | **BLOCKED** by DATN-373 Jira link | §3.1 event/access gates, §3.6 history, §3.7 commit behavior; O31–O32 | `To Do` |
| **DATN-387** | E-04 Add optional Task context to Work Notes through Task API | **BLOCKED** by DATN-373 Jira link | §2.1 SRC-13-Q1/Q9, §3.1 Product scope/outbox gates | `To Do` |
| **DATN-452** | K-02 Implement scoped Handover API and canonical Task coordination | **BLOCKED** by DATN-373 Jira link | §2.1 SRC-13-Q1/D02-09, §3.1 scope/integration gates | `To Do` |

---

### 4.2. Test-Oracle and Decision-Gate Specifications (O0–O33)

Test oracles are partitioned into:
- **Approved Baseline Oracle (O0):** Verifies the immutable D-03 baseline foundation in approval record #22.
- **Conditional Proposal Oracles (O1–O33):** Candidate tests only. They become implementation oracles only after the applicable Product, Architecture, and Security authorities approve the exact behavior; approval by one authority is insufficient for decisions owned by multiple authorities.
- **Unresolved Decision Gate (O31):** Lists evidence and test scenarios required to close the Project Membership revocation decision; it deliberately specifies no unapproved HTTP status, automatic assignment change, or lifecycle outcome.
- **Unresolved API Contract Gate (O32):** Lists omitted input/error outcomes and required tests; it deliberately does not guess response statuses or codes.

#### A. Approved Baseline Oracle (D-03 Private Slice)
- **O0 (Approved Baseline: D-03 Private Slice Persistence Primitive):**
  - *Setup:* Authenticated internal caller invoking the private Task persistence service with trusted `projectId` and `actorId` context.
  - *Input:* `{ projectId: ObjectId, title: "Private Foundation Task" }` plus verified actor context; `createdBy` is server-derived from `actorId`, not accepted as caller-controlled body data.
  - *Expectation:* Successfully persists document with **exactly 7 non-null fields**: `_id`, `projectId`, `title`, `createdBy`, `createdAt`, `updatedAt`, `version: 1`. Assert `task.createdBy == trusted actorId` and `createdAt == updatedAt`. Atomically persists exactly one `task_events` record matching D-03 §8 P3:
    - Event `_id` is present and is an ObjectId; `taskId == task._id`; `projectId == task.projectId`.
    - The event contains exactly the P3 allowlist keys: `_id`, `taskId`, `projectId`, `eventName`, `actorType`, `actorId`, `source`, `changedFields`, `taskVersion`, `occurredAt`, `operationId`, `correlationId`; no extra fields or generic payload.
    - `eventName == "TASK_CREATED"`
    - `actorType == "USER"`, `actorId == createdBy`
    - `source == "HUMAN"`
    - `taskVersion == 1`
    - `occurredAt == createdAt`
    - `operationId`: server-generated UUID v4
    - `correlationId`: server requestId or UUID fallback
    - `changedFields == ["projectId", "title", "createdBy", "createdAt", "updatedAt", "version"]` (excludes `_id`).
  - *Invariants:* No whole-task snapshot; no outbox, relay, queue, or public event delivery is created by the approved D-03 private slice. **No public HTTP route, no status field, and no public CAS.**

#### B. Conditional Public API & Transition Oracles (O1–O30)

**Shared negative-transition fixture `NT-1`:** Seed a Task in the named project with an active Project membership for a `TEAM_LEADER` actor. For each candidate action below, satisfy the candidate scope and authorization preconditions from §3.5 so the request reaches the lifecycle guard; use a fresh Task fixture per case and the listed current version as `expectedVersion`. These are test setup assumptions for conditional proposal oracles only; they do not approve §3.5 or select a production actor policy. Every request must pass DTO validation before the transition under test; include a valid reason of at least 5 characters whenever the target is `BLOCKED` or `CANCELLED`.

**Shared validation fixture `VF-1`:** For O9–O11, O13–O16, and O27–O28, use an authenticated `TEAM_LEADER` with active membership in the target Project and satisfy the candidate route permission checks. For routes targeting an existing Task, use a fresh Task per case; for create/idempotency cases, an active Project context is sufficient. Keep all request values valid except the input under test. This isolates the named validation/conflict condition from an earlier authorization or scope failure.
- **O1 (Proposed Task Creation via Public Gateway API):**
  - *Setup:* Authenticated `MEMBER` with active `ProjectMembership` in `projectId`.
  - *Request:* `POST /api/v1/projects/:projectId/tasks` with `{ "title": "Public Task" }`.
  - *Expectation:* Candidate result `201 Created`; proposed fields/defaults as described. Public creation remains disabled. Its history assertion is not executable until Product/Architecture records whether the public operation uses the exact P3 schema or another approved schema; do not infer that P3 applies to a public route.
- **O2 (T02: START - Permitted Candidate):**
  - *Setup:* `NT-1`; Task in `TODO`, `version: 1`, with active `assigneeId`.
  - *Request:* `PATCH .../status` `{ "targetStatus": "IN_PROGRESS", "expectedVersion": 1 }`.
  - *Expectation:* `200 OK`. `status = "IN_PROGRESS"`, `version = 2`. Emits `TASK_STATUS_TRANSITIONED` event with `delta: { fromStatus: "TODO", toStatus: "IN_PROGRESS" }`.
- **O3 (T04: Direct Complete - Forbidden):**
  - *Setup:* `NT-1`; Task in `TODO`, `version: 1`.
  - *Request:* `PATCH .../status` `{ "targetStatus": "DONE", "expectedVersion": 1 }`.
  - *Expectation:* `409 Conflict`, error code `"TASK_STATE_TRANSITION_CONFLICT"`. Database document unchanged (`status == "TODO"`, `version == 1`). No event appended (`H0`).
- **O4 (Self-Transitions: T01, T07, T13, T19, T25 - Forbidden):**
  - *Setup / independent fixtures:* `NT-1`, T01 `TODO` v1; T07 `IN_PROGRESS` v2; T13 `BLOCKED` v3; T19 `DONE` v3; T25 `CANCELLED` v4.
  - *Requests:* For each fixture, `PATCH .../status` with `targetStatus` equal to its current state and matching `expectedVersion`. Include `reason: "Still blocked"` for T13 and `reason: "Still cancelled"` for T25 so request validation passes.
  - *Expectation for each:* `409 Conflict`, error code `"TASK_STATE_TRANSITION_CONFLICT"`; document state/version unchanged; no event appended (`H0`).
- **O5 (T08: BLOCK - Permitted Candidate):**
  - *Setup:* `NT-1`; Task in `IN_PROGRESS`, `version: 2`.
  - *Request:* `PATCH .../status` `{ "targetStatus": "BLOCKED", "reason": "Missing API Dependency", "expectedVersion": 2 }`.
  - *Expectation:* `200 OK`. `status = "BLOCKED"`, `version = 3`. Emits event with reason recorded. Missing/blank reason $\rightarrow$ `400 Bad Request` (`MANDATORY_TRANSITION_REASON_MISSING`), state unchanged (`H0`).
- **O6 (Cancellation: T05, T10, T15 - Permitted Candidate Parameterized):**
  - *T05 Fixture:* `NT-1`; Task in `TODO`, `version: 1`. Request: `{ "targetStatus": "CANCELLED", "reason": "Cancelled in TODO", "expectedVersion": 1 }`. Result: `200 OK`, `status = "CANCELLED"`, `version = 2`.
  - *T10 Fixture:* `NT-1`; Task in `IN_PROGRESS`, `version: 2`. Request: `{ "targetStatus": "CANCELLED", "reason": "Cancelled in PROGRESS", "expectedVersion": 2 }`. Result: `200 OK`, `status = "CANCELLED"`, `version = 3`.
  - *T15 Fixture:* `NT-1`; Task in `BLOCKED`, `version: 3`. Request: `{ "targetStatus": "CANCELLED", "reason": "Cancelled in BLOCKED", "expectedVersion": 3 }`. Result: `200 OK`, `status = "CANCELLED"`, `version = 4`.
  - *Assertion for all:* Mandatory `reason` (min 5 chars) enforced; emits `TASK_STATUS_TRANSITIONED`.
- **O7 (Terminal Exits: T21, T22, T23, T24 from CANCELLED - Forbidden):**
  - *Setup:* `NT-1`; Task in `CANCELLED`, `version: 4`.
  - *Requests:* Independently submit `PATCH .../status` with `targetStatus` set to `TODO`, `IN_PROGRESS`, `BLOCKED`, or `DONE`, each with `expectedVersion: 4`. For target `BLOCKED`, include `reason: "Restored but blocked"` so DTO validation passes.
  - *Expectation:* `409 Conflict`, error code `"TASK_STATE_TRANSITION_CONFLICT"`. Database document unchanged (`status == "CANCELLED"`, `version == 4`). No event appended (`H0`).
- **O8 (T17: REOPEN - Permitted Candidate):**
  - *Setup:* `NT-1`; Task in `DONE`, `version: 3`, with `completedAt != null`.
  - *Request:* `PATCH .../status` `{ "targetStatus": "IN_PROGRESS", "reason": "QA Defect #12 Reopen", "expectedVersion": 3 }`.
  - *Expectation:* `200 OK`. `status = "IN_PROGRESS"`, `completedAt == null`, `version = 4`. Emits event with reopen reason.
- **O9 (Assignee Membership Validation and Clear Semantics):**
  - `VF-1`; submit `PATCH .../assignee` with `{ "assigneeId": "<valid User ObjectId without active ProjectMembership>", "expectedVersion": <current version> }`. Candidate response: `422 Unprocessable Entity` (`ASSIGNEE_NOT_PROJECT_MEMBER`). Document state/version unchanged and no history event (`H0`).
  - On a separate Task with an assignee and Team, submit `{ "assigneeId": null, "expectedVersion": <current version> }`; candidate result is `200 OK`, assignee cleared, Team preserved, version incremented once. In a separate fixture, pass `"teamId": null` and assert Team cleared. Event assertions depend on approval of the public mutation-event contract.
- **O10 (Atomic Transaction & Uncertainty Guarantee):** `VF-1`; on `POST /api/v1/projects/:projectId/tasks` with `{ "title": "Atomicity candidate" }` and a valid `Idempotency-Key`, inject a confirmed transaction abort and assert neither Task nor history record is persisted (`H0`). In a separate case, simulate loss of commit acknowledgment; classify the outcome as `UNCERTAIN`, then retry the identical request with the same key. Candidate expectation: return the canonical result with exactly one Task and the event specified by the separately approved creation-event contract; do not generate a new key.
- **O11 (Optimistic Concurrency Control):** `VF-1`; submit a valid metadata mutation with `expectedVersion` different from the current Task version. Candidate response: `409 Conflict` (`CONCURRENT_VERSION_CONFLICT`). Document state/version unchanged and no history event (`H0`).
- **O12 (Project Multi-Tenancy Masking):** Candidate only: an authenticated user without active membership in the target Project querying `/api/v1/projects/:projectId/tasks` receives `404 Not Found`, masking project existence. Security/Architecture must approve this exact cross-scope result under O32; the route remains disabled meanwhile.
- **O13 (Due Date Boundary):** `VF-1`; submit a syntactically valid ISO-8601 `dueDate < createdAt` in a metadata PATCH with current `expectedVersion`. Candidate response: `400 Bad Request` (`INVALID_DUE_DATE`). Document state/version unchanged and no history event (`H0`).
- **O14 (Description Boundary):** `VF-1`; submit `description` with more than 5,000 Unicode code points in a metadata PATCH with current `expectedVersion`. Candidate response: `400 Bad Request` (`TASK_VALIDATION_ERROR`). Document state/version unchanged and no history event (`H0`).
- **O15 (Tag Constraint & Nullability):**
  - `VF-1`; submit `tags` with more than 10 valid tag strings in a metadata PATCH with current `expectedVersion`; candidate response `400 Bad Request` (`TASK_VALIDATION_ERROR`), state/version unchanged (`H0`).
  - On fresh fixtures, test one tag exceeding 30 Unicode code points and a tag that becomes empty after trimming; each candidate response is `400 Bad Request` (`TASK_VALIDATION_ERROR`), state/version unchanged (`H0`).
  - On a fresh `VF-1` fixture, submit `"tags": null`; candidate response `400 Bad Request` (`TAGS_MUST_BE_ARRAY`), state/version unchanged (`H0`).
- **O16 (Idempotency Replay & Fingerprint Mismatch):**
  - `VF-1`; for each candidate write route (Task create, metadata update, assignment, and status transition), send a valid request with its own UUID v4 `Idempotency-Key`. Candidate first responses are `201 Created` for create and `200 OK` for PATCH operations.
  - Re-send identical method, normalized path/resource, body, and key; candidate response replays the original status/resource/version without a second Task mutation or event.
  - Re-send a changed body, method, or path/resource within the same actor/Project key scope; candidate response is `422 Unprocessable Entity` (`IDEMPOTENCY_KEY_PAYLOAD_MISMATCH`) and no additional mutation is written. Event assertions depend on approval of the relevant event contract; all replay behavior remains proposed pending authority disposition.
- **O17 (Audit Event Non-Snapshot Invariant):** For approved P3 records, assert the exact O0 schema. For any future candidate mutation records, assert exact event-type-specific keys, the cross-field event/delta/`changedFields` invariants in §3.6.B, and `changedFields` members drawn only from `TaskMutableField`; reject mismatched event/delta pairs, arbitrary keys, whole-task snapshots, description values, and user credentials. Mutation-record assertions remain conditional on approval of that event contract.
- **O18 (T03: Direct Block - Forbidden):**
  - *Setup:* `NT-1`; Task in `TODO`, `version: 1`. Request: `PATCH .../status` `{ "targetStatus": "BLOCKED", "reason": "Direct Block", "expectedVersion": 1 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 1`, `H0`.
- **O19 (T06: Reset to TODO - Forbidden):**
  - *Setup:* `NT-1`; Task in `IN_PROGRESS`, `version: 2`. Request: `PATCH .../status` `{ "targetStatus": "TODO", "expectedVersion": 2 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 2`, `H0`.
- **O20 (T09: COMPLETE - Permitted Candidate):**
  - *Setup:* `NT-1`; Task in `IN_PROGRESS`, `version: 2`. Request: `PATCH .../status` `{ "targetStatus": "DONE", "expectedVersion": 2 }`.
  - *Expectation:* `200 OK`. `status = "DONE"`, `completedAt != null`, `version = 3`. Emits event.
- **O21 (T11: Blocked Reset to TODO - Forbidden):**
  - *Setup:* `NT-1`; Task in `BLOCKED`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "TODO", "expectedVersion": 3 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 3`, `H0`.
- **O22 (T12: RESUME - Permitted Candidate):**
  - *Setup:* `NT-1`; Task in `BLOCKED`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "IN_PROGRESS", "reason": "Impediment Resolved", "expectedVersion": 3 }`.
  - *Expectation:* `200 OK`. `status = "IN_PROGRESS"`, `version = 4`. Emits event.
- **O23 (T14: Blocked Direct Complete - Forbidden):**
  - *Setup:* `NT-1`; Task in `BLOCKED`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "DONE", "expectedVersion": 3 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 3`, `H0`.
- **O24 (T16: Complete Reset to TODO - Forbidden):**
  - *Setup:* `NT-1`; Task in `DONE`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "TODO", "expectedVersion": 3 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 3`, `H0`.
- **O25 (T18: Complete Direct Block - Forbidden):**
  - *Setup:* `NT-1`; Task in `DONE`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "BLOCKED", "reason": "Direct block after done", "expectedVersion": 3 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 3`, `H0`.
- **O26 (T20: Cancel Completed - Forbidden):**
  - *Setup:* `NT-1`; Task in `DONE`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "CANCELLED", "reason": "No longer needed", "expectedVersion": 3 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 3`, `H0`.
- **O27 (Concurrent In-Flight Idempotency Duplicate):** `VF-1`; issue two simultaneous identical Task-create requests with the same valid UUID v4 `Idempotency-Key` and body. The candidate second request returns `409 Conflict` (`CONCURRENT_OPERATION_IN_PROGRESS`) while the first remains in flight; when the first completes, exactly one Task and the event defined by the separately approved create-event contract exist.
- **O28 (Idempotency Key Expiry):** `VF-1`; create a Task with a valid UUID v4 `Idempotency-Key`, advance the injected clock beyond the proposed 24-hour dedupe window, then re-submit the same create request. Candidate outcome: process as a fresh request and create a second Task/event according to the separately approved create-event contract rather than return the first response. This oracle depends on approval of the key-expiry policy.
- **O29 (Audit Log Pagination & Successor Scoping):** Querying `GET /tasks/:taskId/events` returns paginated events matching `TaskEventResponseDTO`. Successors only view events after task handover.
- **O30 (Internal Route Caller Authentication):** Direct HTTP request to `/internal/tasks` without valid mTLS certificate or valid `x-service-token` returns `401 Unauthorized`.

- **O31 (Project Membership Revocation / Team Scope and Assignee Relation — Unresolved Decision Gate):** This is not a runtime oracle and asserts no specific `403`/`404`, automatic task update, or history event. Before any membership- or Team-scope-dependent Task behavior is implemented, obtain Product/Security/Architecture disposition and executable tests for: (1) former Project member list/detail/transition/history access and exact masking/error result after revocation takes effect; (2) whether Team membership alone grants Task list/detail/transition/history scope, whether active Project membership is also required, and which Team actors may mutate; (3) whether an assignee must be a member of the selected Team when both are set; (4) whether existing `assigneeId`/`teamId` references are retained, cleared, or reassigned and who may perform that action; (5) event/history ACL and audit effects; and (6) a revoke-versus-mutation race proving stale authority cannot commit, with the required freshness/fence evidence. Until resolved, do not add a membership-triggered Task mutation or enable any affected public operation; keep DATN-97, DATN-99, DATN-100, and DATN-101 blocked on their respective unresolved dependencies.

- **O32 (API Input/Error Contract — Unresolved Decision Gate):** This is not a runtime oracle and asserts no specific HTTP status or error code. Before enabling any public route, authorities must decide and add executable tests for malformed path IDs; unsupported/malformed filter and pagination inputs; search Unicode case-folding/normalization; priority sort order; null due-date ordering; offset pagination under concurrent inserts/deletes; missing, non-integer, or non-positive `expectedVersion`; unknown/conflicting request fields; tag trimming whitespace set and duplicate behavior; malformed or omitted idempotency keys and no-key uncertainty recovery; authentication-versus-validation precedence; and not-found versus cross-scope masking. Product must resolve description format/rendering and explicitly include or exclude Task delete/archive/restore. Until these decisions are recorded, the corresponding requests and operations remain excluded from implementation; keep DATN-97, DATN-99, DATN-100, and DATN-101 blocked on affected decisions.

- **O33 (Metadata PATCH Omitted-vs-Null Semantics):** `VF-1`; seed a Task with non-null `description`, `dueDate`, non-empty `tags`, and a title/priority. Submit metadata PATCH `{ "description": null, "dueDate": null, "tags": [], "expectedVersion": <current version> }`. Candidate result: `200 OK`, description/dueDate cleared, tags empty, omitted title/priority unchanged, version incremented once, and one metadata mutation event if its schema is approved. This oracle is conditional; the route remains disabled until the relevant authority disposition is recorded.

---

## 5. Artifact Readiness & Authority Sign-Off Status

This checklist reports the contents of this revision. It does not record an authority's approval, mark a subtask Done, or change Jira status.

- [x] **DATN-374 artifact:** The source crosswalk retains `SRC-13-Q1` through `SRC-13-Q9`, `SRC-D02-01` through `SRC-D02-10`, and `SRC-D03-P1..P3`. The membership-revocation effects and outbox scope map to explicit unresolved gates. D-03's private-slice boundary and D-04's accepted scope are preserved.
- [ ] **DATN-375 authority disposition: OPEN.** §3.1 names authority roles, required evidence, disabled operations, and affected Jira issues. This revision contains no new Product, Architecture, or Security approval evidence. No candidate public field, API operation, error contract, or D-02 transition is approved or enabled by D-13.
- [x] **DATN-376 artifact:** The Jira dependency trace covers DATN-97, DATN-99, DATN-100, DATN-101, DATN-387, and DATN-452. O0 is the approved D-03 baseline; O1–O30 and O33 are conditional proposals; O31–O32 are unresolved decision gates, not behavioral oracles.
- [x] **Oracle precision:** O0 asserts P3 event identity fields and exact allowlist keys. Negative transition proposals define actor/scope preconditions and pass request validation before checking lifecycle `409`, unchanged state/version, and no history event. BLOCKED/CANCELLED targets include valid reasons so validation cannot mask the lifecycle result.
- [x] **D-04 boundary:** D-04 remains complete within its accepted runtime-seam scope; this document makes no D-04 change or implementation claim.
- **Current gate:** DATN-374, DATN-375, and DATN-376 remain `In Review` in Jira as of the dependency snapshot. DATN-373 remains `To Do`; its existing `Blocks` links remain the downstream gate. Authority sign-off and reviewer acceptance are still required before any public Task V1 operation is enabled.
