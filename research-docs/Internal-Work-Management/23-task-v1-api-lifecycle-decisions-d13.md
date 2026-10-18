# DATN-373 — D-13 Task V1 API, Lifecycle and Contract Decisions

- **Document Revision:** D13-R5 (18/10/2026, Asia/Bangkok).
- **Document Status:** PROPOSED DISPOSITION & CONTRACT SPECIFICATION FOR REVIEW.
- **Review Authority Framework:**
  - Product Approver: Trần Kim Thắng (Leader, per [`Member.md`](../../Member.md)).
  - Architecture Approver: Task Service & Gateway Boundary per [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md).
  - Security Approver: IAM, Project Scope & RBAC Boundary per [`02_ACTORS_ROLES_AND_PERMISSIONS.md`](../02_ACTORS_ROLES_AND_PERMISSIONS.md).
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
  - This document provides contract specifications, an exact source-ID inventory crosswalk, candidate dispositions, an authority blocker register, and deterministic executable test oracle designs. It does **NOT** constitute human approval by itself and contains no backend application source code.
  - D-03 seven-field persistence (private slice) and D-04 runtime-seam boundaries remain completed within their accepted scopes and are neither reopened nor modified.
  - All downstream implementation under **DATN-97**, **DATN-99 (D-07)**, **DATN-100 (D-08)**, and **DATN-101 (D-09)** remains strictly **BLOCKED** until this specification receives a formal Human Approval Record from the Leader.

---

## 1. Executive Summary & Review Framework

The objective of **DATN-373 (D-13)** is to bring the Task V1 specification to full technical closure by resolving every `UNKNOWN` item across the contract readiness baseline. This revision (D13-R5) addresses all remaining review findings for **DATN-374**, **DATN-375**, and **DATN-376**.

### 1.1. Accepted Baseline vs. Proposed Dispositions

To prevent unauthorized assumptions, all policy elements in this document are strictly classified into one of four deterministic states:

1. **`APPROVED`**: Immutable foundation accepted in formal human approval records (PR #30, PR #31).
2. **`PROPOSED_DISPOSITION`**: Concrete engineering specification formulated for Leader / Authority review.
3. **`PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION`**: Features candidate for exclusion from V1 (e.g. Work Note/Handover integration, durable outbox) pending formal Product confirmation. Downstream issues remain blocked.
4. **`UNKNOWN / DISABLED`**: Elements awaiting authority determination where no transition or operation is permitted.

| Policy Domain | Accepted Baseline (PR #30 / PR #31) | Proposed Disposition in D-13-R5 (Awaiting Human Approval) | Status |
|---|---|---|---|
| **Data Foundation** | Exactly 7 fields approved for D-03 private slice: `_id`, `projectId`, `title`, `createdBy`, `createdAt`, `updatedAt`, `version`. | 8 candidate extension fields: `status`, `description`, `priority`, `assigneeId`, `teamId`, `dueDate`, `completedAt`, `tags`. | 7 Fields: `APPROVED`<br>Extension: `PROPOSED_DISPOSITION` |
| **Creation Event Contract** | D-03 §8 P3: Exactly 1 creation event with required provenance (`eventName: "TASK_CREATED"`, `taskVersion: 1`, `occurredAt`, `source: "HUMAN"`, `changedFields` without `_id`). | Preserves D-03 §8 P3 creation event schema verbatim for private slice; defines separate proposed schema for subsequent public mutations. | Baseline: `APPROVED`<br>Mutation Events: `PROPOSED_DISPOSITION` |
| **Version Semantics** | Internal creation ordinal `1`. No public CAS/ETag semantics in private slice. | Introduces `expectedVersion` for optimistic concurrency control (OCC) on public mutations. | Baseline: `APPROVED`<br>OCC: `PROPOSED_DISPOSITION` |
| **Lifecycle Transitions** | All 25 cells in D-02 are disabled (`Enabled: NO`). | Reaffirms 25 cells `Enabled: NO`. Details 8 Candidate Permitted vs. 17 Candidate Forbidden transitions with explicit guards. | Baseline: `UNKNOWN / DISABLED`<br>Candidate: `PROPOSED_DISPOSITION` |
| **Organization Scope** | Contextual isolation derived from owning Project. No standalone storage in V1. | `organizationId` is derived contextually via trusted Project lookup; NOT persisted independently in Task document. | `APPROVED` (Reaffirmed) |
| **History & Audit** | B4/P3: Atomic Task + Event persistence. Whole-task snapshots & PII prohibited. | Discriminative allowlist schema (`changedFields` + restricted delta + ADR-010 provenance fields). Excludes snapshots, credentials. | `PROPOSED_DISPOSITION` |
| **Mutation Reliability** | Commit exceptions do not prove rollback; must distinguish uncertain commit. | Client `operationId` (Idempotency Key), SHA-256 payload fingerprint, 24h dedupe, and three-way commit handling. | `PROPOSED_DISPOSITION` |
| **Work Note & Handover** | Integration optional; only enters V1 if contract approved by owner (Record #20 §16). | Integration proposed excluded from Task V1 core. DATN-387 and DATN-452 remain BLOCKED. | `PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION` |

---

## 2. DATN-374 (D-13.1): Complete 1-to-1 Source Inventory & Crosswalk

In strict compliance with DATN-374 pass criteria, this master crosswalk maintains the exact original question identifiers from [D-01 Contract Readiness (Doc 13 §4)](13-task-v1-contract-readiness.md), [D-02 State Machine Review (Doc 16 §2–3, Doc 18 §2)](16-task-v1-state-machine-contract.md), and [D-03 Delta Approval (Doc 21 / 22)](22-task-v1-d03-delta-approval-record.md). All items from `SRC-13-Q1` through `SRC-13-Q9`, `SRC-D02-01` through `SRC-D02-10`, and D-03 follow-ups are represented 1-to-1.

### 2.1. Master Source Inventory Crosswalk

| Original Source ID | Source Reference | Exact Source Question / Item | Disposition Status | Proposed Disposition in D-13-R5 | Required Authority Role | Impacted Downstream Jira Issue | Test Oracle ID |
|---|---|---|---|---|---|---|---|
| **SRC-13-Q1** | Doc 13 §4.1 / Doc 20 §16 | **V1 Scope & Use Cases:** Exact UC-TM use cases included in V1; inclusion of Work Note / Handover. | `PROPOSED_DISPOSITION` / `PROPOSED_EXCLUSION` | Core Task CRUD + Status + Assignment included; Work Note and Handover proposed excluded from V1 pending Product contract. | Product Approver (Leader) | DATN-97, DATN-387, DATN-452 | O1, O2, O8, O12 |
| **SRC-13-Q2** | Doc 13 §4.2 / Doc 20 §18, §19 | **Ownership & Relationships:** One Project per Task; 0..1 Team, 0..1 Assignee; Organization derivation. | `APPROVED` & `PROPOSED_DISPOSITION` | Project owns Task; 0..1 Team (`teamId`) and 0..1 Assignee (`assigneeId`); contextual Org derivation. | Architecture & Product | DATN-97, DATN-99 (D-07) | O0, O1, O9, O12 |
| **SRC-13-Q3** | Doc 13 §4.3 / Doc 21 §5 | **Field Dictionary & Constraints:** Exact field names, types, nullability, defaults, mutability, lengths. | `APPROVED` (7 fields) / `PROPOSED_DISPOSITION` (8 fields) | Approved 7 D-03 fields + 8 candidate extension fields (`status`, `description`, `priority`, `assigneeId`, `teamId`, `dueDate`, `completedAt`, `tags`). | Product Approver (Leader) | DATN-97, DATN-99, DATN-100 | O0, O1, O13, O14, O15 |
| **SRC-13-Q4** | Doc 13 §4.4 / Doc 16 §2 | **Lifecycle Catalogue & Terminals:** State enum catalogue, initial state, and terminal semantics. | `PROPOSED_DISPOSITION` | 5 states: `TODO` (initial), `IN_PROGRESS`, `BLOCKED`, `DONE` (reopenable), `CANCELLED` (terminal, no exit). | Product Approver (Leader) | DATN-97, DATN-100 (D-08) | O1, O2, O7, O8 |
| **SRC-13-Q5** | Doc 13 §4.5 / Doc 20 §16, §32 | **Authorization & RBAC:** Actor, role, and scope permission matrix; cross-project isolation. | `PROPOSED_DISPOSITION` (Policy Conflict Under Review) | 4D RBAC using `ADMIN`, `TEAM_LEADER`, `MEMBER`. Reassignment limited to Lead/Admin. Masking foreign projects via 404. | Security & Product | DATN-97, DATN-99, DATN-100 | O9, O12 |
| **SRC-13-Q6** | Doc 13 §4.6 / ADR-010 §3 | **API Surface & Route Boundary:** Route schemas, pagination, filter grammar, Gateway vs. Internal Service. | `PROPOSED_DISPOSITION` | 7 REST endpoints; Gateway `/api/v1/projects/:projectId/tasks` vs Internal `/internal/tasks`; pagination & sorting rules. | Architecture Approver (ADR-010) | DATN-97, DATN-99, DATN-100, DATN-101 | O1, O2, O4, O11, O12, O30 |
| **SRC-13-Q7** | Doc 13 §4.7 / Doc 22 §1 | **Version, Mutation & Idempotency:** Version counter vs. public OCC; operation replay; uncertain commits. | `APPROVED` (D-03) / `PROPOSED_DISPOSITION` (D-13) | D-03 ordinal preserved; `expectedVersion` proposed for public OCC; `operationId` 24h replay; 3-way commit outcome. | Architecture Approver | DATN-97, DATN-99, DATN-100 | O0, O10, O11, O16, O27, O28 |
| **SRC-13-Q8** | Doc 13 §4.8 / Doc 21 §8 | **History Event Boundary:** Event coverage, projection, prohibition of whole-task snapshots, retention. | `PROPOSED_DISPOSITION` | D-03 §8 P3 baseline preserved; `task_events` allowlist schema for mutations; ADR-010 provenance fields. | Architecture & Security | DATN-97, DATN-101 (D-09) | O0, O2, O8, O10, O17, O29 |
| **SRC-13-Q9** | Doc 13 §4.9 / Doc 20 §25 | **Durable Consumer & Outbox:** Transactional outbox requirement and event delivery queue. | `PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION` | Outbox deferred from Task V1 due to absence of an approved durable consumer. History is append-only audit. | Product & Architecture | DATN-97 | N/A (Deferred) |
| **SRC-D02-01** | Doc 16 §2 | **Candidate State Meanings:** Semantic validation of `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`. | `PROPOSED_DISPOSITION` | Accepted candidate definitions in §3.2. Reason mandatory for `BLOCKED`. | Product Approver (Leader) | DATN-97, DATN-100 | O1, O2, O5, O7 |
| **SRC-D02-02** | Doc 16 §3 | **25-Cell Transition Matrix:** Cartesian evaluation of T01 through T25. | `UNKNOWN / DISABLED` (Baseline) / `PROPOSED_DISPOSITION` | All 25 cells `Enabled: NO` in baseline. Proposed candidate matrix: 8 Permitted vs. 17 Forbidden cells. | Product & Architecture | DATN-97, DATN-100 | O2–O8, O18–O26 |
| **SRC-D02-03** | Doc 16 §3 | **Transition Reasons:** Rules for mandatory reasons on state transitions. | `PROPOSED_DISPOSITION` | Mandatory `reason` (min 5 chars) on `BLOCKED`, `CANCELLED`, `RESUME`, `REOPEN`. Optional on `START`, `COMPLETE`. | Product Approver (Leader) | DATN-100 (D-08) | O5, O6, O8 |
| **SRC-D02-04** | Doc 16 §4 | **Guard Layers G1–G6 & Actor Scope:** Validation, IAM active membership, Project/Team fence, freshness. | `PROPOSED_DISPOSITION` | Explicit G1–G6 guard pipeline; active membership check; project isolation masking. | Security & Architecture | DATN-97, DATN-99, DATN-100 | O9, O12, O13, O14, O15 |
| **SRC-D02-05** | Doc 17 §2 | **Concurrency & CAS:** Aggregate versioning, stale conflict resolution, uncertain transaction boundaries. | `PROPOSED_DISPOSITION` | `expectedVersion` aggregate CAS; stale returns 409; three-way commit outcome handling. | Architecture Approver | DATN-97, DATN-100 | O10, O11 |
| **SRC-D02-06** | Doc 17 §3 | **Idempotency Namespace & Fingerprinting:** Uniqueness tuple, payload fingerprinting, and parameter normalization. | `PROPOSED_DISPOSITION` | Tuple `(actorId, projectId, operationId)`; SHA-256 canonical payload hash; mismatch returns 422. | Architecture Approver | DATN-97, DATN-100 | O16 |
| **SRC-D02-07** | Doc 17 §4 | **Operation Replay Resolution:** Replay cache, in-flight duplicate handling, denial caching prohibition. | `PROPOSED_DISPOSITION` | Cached replay returns exact persisted result; concurrent in-flight returns 409; no denial caching. | Architecture Approver | DATN-97, DATN-100 | O16, O27 |
| **SRC-D02-08** | Doc 17 §5 | **Deduplication Window & Proof Retention:** Key TTL, cleanup window, and post-expiry semantics. | `PROPOSED_DISPOSITION` | 24-hour TTL in Redis / Mongo; expired key treated as fresh request; no indefinite storage. | Architecture & Ops | DATN-97 | O28 |
| **SRC-D02-09** | Doc 17 §6 | **Cross-Boundary Coordination & Handover:** Handover retry/compensation, operation ID propagation. | `PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION` | Handover assignment integration proposed excluded from V1; DATN-452 blocked pending owner contract. | Product & Architecture | DATN-452 | N/A (Blocked) |
| **SRC-D02-10** | Doc 16 §3 / Doc 18 §2 | **Event Schema & Audit Delta:** History representation, provenance fields, redaction of sensitive content. | `PROPOSED_DISPOSITION` | Allowlist delta (`changedFields`, discriminated delta); ADR-010 provenance fields; successor ACL. | Architecture & Security | DATN-97, DATN-101 (D-09) | O0, O2, O8, O17, O29 |
| **SRC-D03-P1** | Doc 22 §1 | **Private Slice Foundation:** Private create/read persistence primitives, task/history definitions. | `APPROVED` | Approved in PR #31 for private slice. No public API or status lifecycle introduced. | Product Approver (Leader) | DATN-95, D-03 | O0 |
| **SRC-D03-P2** | Doc 22 §1 | **Exact 7 Foundation Fields:** `_id`, `projectId`, `title`, `createdBy`, `createdAt`, `updatedAt`, `version`. | `APPROVED` | Approved in PR #31. Exactly 7 non-null fields; version = 1; updatedAt = createdAt. | Product Approver (Leader) | DATN-95, D-03 | O0 |
| **SRC-D03-P3** | Doc 22 §1 | **Atomic Creation History:** Exactly one creation event, atomic write, append-only history. | `APPROVED` | Approved in PR #31. Single creation event per committed Task version 1; no content snapshots. | Product Approver (Leader) | DATN-95, D-03 | O0 |

---

## 3. DATN-375 (D-13.2): Authority Disposition & Contract Specification

### 3.1. Authority & Blocker Register

To ensure transparent governance, each unresolved policy is linked to its required authority, required input, and current blocking status:

| Policy Area | Source Question IDs | Current Status | Governing Authority Role | Exact Action / Evidence Required to Close Gate | Impacted Issues Kept Blocked |
|---|---|---|---|---|---|
| **Lifecycle 25-Cell Matrix** | `SRC-13-Q4`, `SRC-D02-01–03` | `UNKNOWN / DISABLED` (Baseline) / `PROPOSED_DISPOSITION` | Product Approver (Leader per `Member.md`) | Formal Leader Approval Record adopting 8 candidate permitted transitions and confirming 17 forbidden transitions. | DATN-97, DATN-100 (D-08) |
| **Extended Fields Dictionary** | `SRC-13-Q3` | `PROPOSED_DISPOSITION` | Product Approver (Leader per `Member.md`) | Formal Leader Approval Record approving field dictionary (`status`, `description`, `priority`, `assigneeId`, `teamId`, `dueDate`, `completedAt`, `tags`). | DATN-97, DATN-99 (D-07) |
| **Public OCC Version Semantics** | `SRC-13-Q7`, `SRC-D02-05` | `PROPOSED_DISPOSITION` | Architecture Approver (ADR-010) | Architecture sign-off on public `expectedVersion` optimistic concurrency control. | DATN-97, DATN-100, DATN-101 |
| **Internal Route & mTLS Trust** | `SRC-13-Q6` | `PROPOSED_DISPOSITION` | Architecture Approver (ADR-010) | Architecture sign-off on `/internal/tasks` route prefix and mTLS / `x-service-token` service authentication. | DATN-97 |
| **RBAC & Project Admin Scope** | `SRC-13-Q5`, `SRC-D02-04` | `POLICY CONFLICT UNDER REVIEW` | Security Approver & Product Approver | Formal Security sign-off resolving Organization Admin private-project masking vs Project Admin task management rights. | DATN-97, DATN-99, DATN-100 |
| **Team/Assignee Eligibility & Fence** | `SRC-13-Q2`, `SRC-D02-04` | `PROPOSED_DISPOSITION` | Security Approver & Product Approver | Security sign-off on Project-scoped membership validation and Team boundary inheritance. | DATN-97, DATN-99 (D-07) |
| **Public API Operation Schemas & Errors** | `SRC-13-Q6` | `PROPOSED_DISPOSITION` | Architecture Approver (ADR-010) | Architecture sign-off on Request/Response DTOs, deterministic error codes, and tie-breaker sorting. | DATN-97, DATN-99, DATN-100, DATN-101 |
| **Audit Event Schema & Provenance** | `SRC-13-Q8`, `SRC-D02-10` | `PROPOSED_DISPOSITION` | Architecture & Security Approvers | Formal sign-off on mutation event types, allowlist delta projection, and successor history ACL. | DATN-97, DATN-101 (D-09) |
| **Idempotency & Replay Engine** | `SRC-D02-06–08` | `PROPOSED_DISPOSITION` | Architecture Approver | Architecture sign-off on tuple namespace, SHA-256 fingerprinting, 24h deduplication, and uncertain commit model. | DATN-97, DATN-100 |
| **Work Note & Handover Exclusion** | `SRC-13-Q1`, `SRC-D02-09` | `PROPOSED_EXCLUSION` | Product Approver (Leader per `Member.md`) | Formal Product decision confirming exclusion of Work Note and Handover integration from Task V1 core scope. | DATN-387, DATN-452 |

---

### 3.2. Task Lifecycle State Machine (SRC-13-Q4, SRC-D02-01–03)

#### A. State Catalogue
1. `TODO`: Initial state upon creation. Task persisted but execution has not begun.
2. `IN_PROGRESS`: Active execution by eligible assignee.
3. `BLOCKED`: Execution halted by an external impediment. Mandatory `reason` required.
4. `DONE`: Execution completed. Can be reopened via `REOPEN`. Automatically sets `completedAt = now()`.
5. `CANCELLED`: Terminal state. Work discarded or abandoned. In V1, no exits are permitted.

#### B. Complete 25-Cell State Transition Matrix Evaluation
**Baseline Authority Rule:** Currently, all 25 cells are **`DISABLED (Enabled: NO)`** under baseline DATN-94. The table below formulates the exact candidate proposal for authority review:

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

#### A. Approved Foundation Fields (D-03 Baseline — PR #31)
These 7 fields are permanently accepted:
- `_id`: ObjectId, immutable, system-generated primary key.
- `projectId`: ObjectId, immutable, required owning Project reference.
- `title`: String, mutable, required, original string preserved, non-empty outside set $W$, non-unique.
- `createdBy`: ObjectId, immutable, server-derived authenticated actor ID.
- `createdAt`: ISODate, immutable, server-derived UTC timestamp.
- `updatedAt`: ISODate, mutable, server-derived UTC timestamp (initially equal to `createdAt`).
- `version`: Number, mutable, creation ordinal `1` at baseline; proposed for optimistic concurrency counter in D-13.

#### B. Proposed Extension Fields for Task V1 (Awaiting Human Approval)

| Field Name | Type | Storage Type | Nullable | Default | Mutability | Constraints & Validation Semantics |
|---|---|---|---|---|---|---|
| `status` | String | `enum` | No | `"TODO"` | Mutable (Status API only) | Enum: `["TODO", "IN_PROGRESS", "BLOCKED", "DONE", "CANCELLED"]`. Governed by 25-cell matrix. |
| `description` | String | `string` | Yes | `null` | Mutable | Optional; max length 5,000 UTF-8 characters. Plain text or Markdown. Clearable by passing `null`. |
| `priority` | String | `enum` | No | `"MEDIUM"` | Mutable | Enum: `["LOW", "MEDIUM", "HIGH", "URGENT"]`. |
| `assigneeId` | ObjectId | `ObjectId` | Yes | `null` | Mutable | Cardinality 0..1. Must reference active `User` with active `ProjectMembership` in `projectId`. Clearable by passing `null`. |
| `teamId` | ObjectId | `ObjectId` | Yes | `null` | Mutable | Cardinality 0..1. Must reference active `Team` in `projectId`. Clearable by passing `null`. |
| `dueDate` | Date | `ISODate` | Yes | `null` | Mutable | ISO-8601 UTC timestamp (`YYYY-MM-DDTHH:mm:ss.sssZ`). Validation rule: `dueDate >= createdAt`. Clearable by passing `null`. |
| `completedAt` | Date | `ISODate` | Yes | `null` | Server-derived | Automatically set to `now()` on transition T09 (`COMPLETE`). Automatically reset to `null` on T17 (`REOPEN`). |
| `tags` | Array | `[String]` | No | `[]` | Mutable | Max 10 tags; each tag max 30 characters; trimmed, non-empty. **Non-nullable.** To clear tags, client must pass `[]`. Passing `null` returns `400 Bad Request`. |

#### C. Derived Context Boundary
- `organizationId`: Contextually derived from owning `Project.organizationId` via trusted Project Service lookup. In compliance with D-03 PR #31, `organizationId` is **NOT** persisted as an independent column in the Task collection for V1.

---

### 3.4. REST API Surface & Network Boundary (SRC-13-Q6)

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
  eventType: string;                  // e.g. "TASK_STATUS_TRANSITIONED"
  actorId: string;                    // Hex string of actor
  actorType: "USER" | "SYSTEM";       // Actor category
  source: "WEB" | "API" | "INTERNAL_SERVICE";
  timestamp: string;                  // ISO-8601 UTC string
  version: number;                    // Resulting task version
  operationId?: string;               // Idempotency key if supplied
  changedFields: string[];            // Allowlist of updated field names
  delta: Record<string, unknown>;     // Discriminated payload (NO snapshots)
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
    "title": "string (required, min 1 non-W char, max 500)",
    "description": "string | null (optional, max 5000)",
    "priority": "LOW | MEDIUM | HIGH | URGENT (optional, default MEDIUM)",
    "assigneeId": "string | null (optional, valid ObjectId)",
    "teamId": "string | null (optional, valid ObjectId)",
    "dueDate": "string | null (optional, ISO-8601 UTC timestamp)",
    "tags": ["string"] (optional, max 10 tags, each max 30 chars; non-nullable)
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
  - `search`: Substring search on `title` (case-insensitive regex, max 100 chars).
  - `page`: Integer $\ge 1$ (default: `1`).
  - `limit`: Integer $1 \le \text{limit} \le 100$ (default: `20`).
  - `sort`: Default `-createdAt`. Allowed keys: `createdAt`, `-createdAt`, `updatedAt`, `-updatedAt`, `dueDate`, `-dueDate`, `priority`, `-priority`.
  - **Deterministic Tie-Breaker Rule:** Query engine appends `_id: 1` as secondary sort to prevent page drift across concurrent inserts.
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
- **Semantics:**
  - Omitted fields are left unchanged.
  - Passing `null` on nullable fields (`description`, `dueDate`) clears their value.
  - Passing `[]` on `tags` clears tags. Passing `null` on `tags` returns `400 Bad Request`.
- **Request Body:**
  ```json
  {
    "title": "string (optional)",
    "description": "string | null (optional)",
    "priority": "LOW | MEDIUM | HIGH | URGENT (optional)",
    "dueDate": "string | null (optional, ISO-8601 UTC timestamp)",
    "tags": ["string"] (optional, non-nullable array),
    "expectedVersion": 2
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

---

### 3.5. Role-Based Access Control & Policy Conflict Disclosure (SRC-13-Q5)

#### A. Role Alignment & Conflict Disclosure
The permission baseline in [`02_ACTORS_ROLES_AND_PERMISSIONS.md`](../02_ACTORS_ROLES_AND_PERMISSIONS.md) and [`12-continuum-task-management-use-cases.md`](12-continuum-task-management-use-cases.md) §3 contains an unresolved policy tension:
- **Baseline Constraint:** Organization `ADMIN` does not possess default read access to private Project contents; assignment and cancellation are scoped to `TEAM_LEADER`.
- **D-13 Proposal:** Grants Project-level `ADMIN` management oversight over all tasks in the project.
- **Formal Status:** **`POLICY CONFLICT UNDER REVIEW (Awaiting Security & Product Disposition)`**. Until formally decided by the Security Authority, the candidate matrix below governs proposed behavior:

#### B. Candidate 4D Authorization Matrix: Role $\times$ Action $\times$ Resource $\times$ Scope

| Action Code | Target Operation | Required Role | Ownership / Guard Condition | Non-Member / Cross-Scope Outcome |
|---|---|---|---|---|
| `TASK_CREATE` | `POST /tasks` | `MEMBER` | Active `ProjectMembership` in target `projectId`. | `404 Not Found` (Mask project existence) |
| `TASK_READ` | `GET /tasks` (List/Detail/Events) | `MEMBER` | Active member of `projectId`. | `404 Not Found` |
| `TASK_EDIT_META` | `PATCH /tasks/:taskId` | `MEMBER` | Must be: (a) Project `ADMIN`, (b) `TEAM_LEADER`, (c) `assigneeId == actorId`, or (d) `createdBy == actorId`. | `404 Not Found` (or `403 Forbidden` if member lacking role) |
| `TASK_ASSIGN` | `PATCH /tasks/:taskId/assignee` | `TEAM_LEADER` | Only `ADMIN` or `TEAM_LEADER` can assign/reassign. Plain `MEMBER` cannot reassign. | `403 Forbidden` |
| `TASK_TRANSITION_WORK` | `START`, `BLOCK`, `RESUME`, `COMPLETE` | `MEMBER` | Must be assigned to task (`assigneeId == actorId`), or hold `TEAM_LEADER` / `ADMIN`. | `403 Forbidden` |
| `TASK_CANCEL` | `CANCEL` (T05, T10, T15) | `MEMBER` | Must be: Project `ADMIN`, `TEAM_LEADER`, or original `createdBy`. | `403 Forbidden` |
| `TASK_REOPEN` | `REOPEN` (T17) | `MEMBER` | Must be: Project `ADMIN`, `TEAM_LEADER`, or original `createdBy`. | `403 Forbidden` |

*Scope Rules:*
- **Team Scope:** When `teamId` is set, members of that Team inherit task visibility.
- **Successor ACL:** Per Task Use Cases §7, successors only view event history of tasks transferred to them.
- **Excluded Operations:** Comment creation is excluded from Task V1.

---

### 3.6. Audit History Event Schema & Provenance (SRC-13-Q8, ADR-010 §7)

#### A. Approved Baseline Event Contract (D-03 §8 P3 Baseline)
For the private creation primitive approved in PR #31, the schema is fixed and immutable:
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

#### B. Proposed Task V1 Mutation Event Schema (Awaiting Human Approval)
For subsequent public mutations (`TASK_STATUS_TRANSITIONED`, `TASK_ASSIGNMENT_CHANGED`, `TASK_METADATA_UPDATED`), the proposed schema extends provenance per ADR-010 §7 while strictly preserving the non-snapshot rule:

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
  changedFields: string[];           // Allowlist array of modified field names
  delta: TaskEventDelta;             // Discriminated payload (NO snapshots)
}

type TaskEventType = 
  | "TASK_CREATED"
  | "TASK_METADATA_UPDATED"
  | "TASK_STATUS_TRANSITIONED"
  | "TASK_ASSIGNMENT_CHANGED";

type TaskEventDelta = 
  | { type: "CREATED"; initialStatus: "TODO" }
  | { type: "STATUS_TRANSITION"; fromStatus: string; toStatus: string; reason?: string }
  | { type: "ASSIGNMENT_CHANGED"; previousAssigneeId: ObjectId | null; newAssigneeId: ObjectId | null; previousTeamId?: ObjectId | null; newTeamId?: ObjectId | null }
  | { type: "METADATA_UPDATED"; updatedScalarFields: string[] };
```

---

### 3.7. Mutation Reliability, Idempotency & Three-Way Commit Model (SRC-13-Q7, ADR-010 §6)

#### A. Idempotency Key Semantics
- **Key Header:** `Idempotency-Key` (Client-supplied UUID v4).
- **Uniqueness Scope:** Scoped to the tuple `(actorId, projectId, operationId)`.
- **Payload Fingerprinting:** Task Service computes a SHA-256 hash of the canonical JSON request payload.
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

This register formally establishes the blocking relationships between DATN-373 and downstream implementation tasks under Epic DATN-75:

| Jira Key | Official Issue Summary | Relationship to DATN-373 | Governing Section in D-13-R5 | Current Status |
|---|---|---|---|---|
| **DATN-97** | Task V1 Core BE Implementation | **BLOCKED** by DATN-373 | §3.2 (Fields), §3.3 (API), §3.4 (RBAC), §3.6 (Reliability) | `To Do` (BLOCKED) |
| **DATN-99** | **D-07 Task Assignment Service** | **BLOCKED** by DATN-373 | §3.2 (Fields: `assigneeId`, `teamId`), §3.4 (RBAC), §3.5 (Audit) | `To Do` (BLOCKED) |
| **DATN-100** | **D-08 Task Status & Lifecycle Execution Engine** | **BLOCKED** by DATN-373 | §3.1 (25-Cell Matrix), §3.3 (Status API), §3.5 (Events) | `To Do` (BLOCKED) |
| **DATN-101** | **D-09 Task Mutation & Audit History Service** | **BLOCKED** by DATN-373 | §3.5 (Event Schema), §3.6 (Atomic History Persistence) | `To Do` (BLOCKED) |
| **DATN-387** | Work Note Integration Boundary | **BLOCKED** pending Product Scope Decision | §2.1 (SRC-13-Q1), §1.1 | `To Do` (BLOCKED) |
| **DATN-452** | Handover Integration Boundary | **BLOCKED** pending Product Scope Decision | §2.1 (SRC-13-Q1), §3.6 (Operation ID for Handover) | `To Do` (BLOCKED) |

---

### 4.2. Comprehensive Executable Test Oracles (O0–O30)

Test oracles are partitioned into:
- **Approved Baseline Oracle (O0):** Verifies immutable D-03 baseline foundation (PR #31).
- **Conditional Proposal Oracles (O1–O30):** Test specifications that become binding **ONLY** upon formal Leader approval of this specification.

#### A. Approved Baseline Oracle (D-03 Private Slice)
- **O0 (Approved Baseline: D-03 Private Slice Persistence Primitive):**
  - *Setup:* Authenticated internal caller invoking private Task persistence service.
  - *Input:* `{ projectId: ObjectId, title: "Private Foundation Task", createdBy: ObjectId }`.
  - *Expectation:* Successfully persists document with **exactly 7 non-null fields**: `_id`, `projectId`, `title`, `createdBy`, `createdAt`, `updatedAt`, `version: 1`. `createdAt == updatedAt`. Atomically persists exactly one `task_events` record matching D-03 §8 P3:
    - `eventName == "TASK_CREATED"`
    - `actorType == "USER"`, `actorId == createdBy`
    - `source == "HUMAN"`
    - `taskVersion == 1`
    - `occurredAt == createdAt`
    - `operationId`: server-generated UUID v4
    - `correlationId`: server requestId or UUID fallback
    - `changedFields == ["projectId", "title", "createdBy", "createdAt", "updatedAt", "version"]` (excludes `_id`).
  - *Invariants:* No whole-task snapshot. **No public HTTP route, no status field, and no public CAS.**

#### B. Conditional Public API & Transition Oracles (O1–O30)
- **O1 (Proposed Task Creation via Public Gateway API):**
  - *Setup:* Authenticated `MEMBER` of `projectId`.
  - *Request:* `POST /api/v1/projects/:projectId/tasks` with `{ "title": "Public Task" }`.
  - *Expectation:* `201 Created`. Persists 7 foundation fields plus proposed defaults `status: "TODO"`, `priority: "MEDIUM"`, `version: 1`. Emits `TASK_CREATED` event.
- **O2 (T02: START - Permitted Candidate):**
  - *Setup:* Task in `TODO`, `version: 1`, with active `assigneeId`. Caller is Assignee.
  - *Request:* `PATCH .../status` `{ "targetStatus": "IN_PROGRESS", "expectedVersion": 1 }`.
  - *Expectation:* `200 OK`. `status = "IN_PROGRESS"`, `version = 2`. Emits `TASK_STATUS_TRANSITIONED` event with `delta: { fromStatus: "TODO", toStatus: "IN_PROGRESS" }`.
- **O3 (T04: Direct Complete - Forbidden):**
  - *Setup:* Task in `TODO`, `version: 1`.
  - *Request:* `PATCH .../status` `{ "targetStatus": "DONE", "expectedVersion": 1 }`.
  - *Expectation:* `409 Conflict`, error code `"TASK_STATE_TRANSITION_CONFLICT"`. Database document unchanged (`status == "TODO"`, `version == 1`). No event appended (`H0`).
- **O4 (Self-Transitions: T01, T07, T13, T19, T25 - Forbidden):**
  - *Setup:* Task in state $S_i$ (`TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`).
  - *Request:* `PATCH .../status` with `targetStatus == currentStatus`.
  - *Expectation:* `409 Conflict`, error code `"TASK_STATE_TRANSITION_CONFLICT"`. Document state and version unchanged. No event appended (`H0`).
- **O5 (T08: BLOCK - Permitted Candidate):**
  - *Setup:* Task in `IN_PROGRESS`, `version: 2`. Caller is Assignee.
  - *Request:* `PATCH .../status` `{ "targetStatus": "BLOCKED", "reason": "Missing API Dependency", "expectedVersion": 2 }`.
  - *Expectation:* `200 OK`. `status = "BLOCKED"`, `version = 3`. Emits event with reason recorded. Missing/blank reason $\rightarrow$ `400 Bad Request` (`MANDATORY_TRANSITION_REASON_MISSING`), state unchanged (`H0`).
- **O6 (Cancellation: T05, T10, T15 - Permitted Candidate Parameterized):**
  - *T05 Fixture:* Task in `TODO`, `version: 1`. Request: `{ "targetStatus": "CANCELLED", "reason": "Cancelled in TODO", "expectedVersion": 1 }`. Caller is Creator. Result: `200 OK`, `status = "CANCELLED"`, `version = 2`.
  - *T10 Fixture:* Task in `IN_PROGRESS`, `version: 2`. Request: `{ "targetStatus": "CANCELLED", "reason": "Cancelled in PROGRESS", "expectedVersion": 2 }`. Caller is `TEAM_LEADER`. Result: `200 OK`, `status = "CANCELLED"`, `version = 3`.
  - *T15 Fixture:* Task in `BLOCKED`, `version: 3`. Request: `{ "targetStatus": "CANCELLED", "reason": "Cancelled in BLOCKED", "expectedVersion": 3 }`. Caller is `ADMIN`. Result: `200 OK`, `status = "CANCELLED"`, `version = 4`.
  - *Assertion for all:* Mandatory `reason` (min 5 chars) enforced; emits `TASK_STATUS_TRANSITIONED`.
- **O7 (Terminal Exits: T21, T22, T23, T24 from CANCELLED - Forbidden):**
  - *Setup:* Task in `CANCELLED`, `version: 4`.
  - *Requests:* `PATCH .../status` with `targetStatus` set to `TODO`, `IN_PROGRESS`, `BLOCKED`, or `DONE`.
  - *Expectation:* `409 Conflict`, error code `"TASK_STATE_TRANSITION_CONFLICT"`. Database document unchanged (`status == "CANCELLED"`, `version == 4`). No event appended (`H0`).
- **O8 (T17: REOPEN - Permitted Candidate):**
  - *Setup:* Task in `DONE`, `version: 3`, with `completedAt != null`. Caller is Project `ADMIN`.
  - *Request:* `PATCH .../status` `{ "targetStatus": "IN_PROGRESS", "reason": "QA Defect #12 Reopen", "expectedVersion": 3 }`.
  - *Expectation:* `200 OK`. `status = "IN_PROGRESS"`, `completedAt == null`, `version = 4`. Emits event with reopen reason.
- **O9 (Assignee Membership Validation):** Setting `assigneeId` to a user without active `ProjectMembership` in `projectId` returns `422 Unprocessable Entity` (`ASSIGNEE_NOT_PROJECT_MEMBER`). Document state unchanged (`H0`).
- **O10 (Atomic Transaction & Uncertainty Guarantee):** Confirmed aborted transaction rolls back both Task and event log (`H0`). Unacknowledged commit exception leaves status as `UNCERTAIN`; replay with identical `operationId` retrieves canonical committed state.
- **O11 (Optimistic Concurrency Control):** Submitting mismatched `expectedVersion` returns `409 Conflict` (`CONCURRENT_VERSION_CONFLICT`). Document state unchanged (`H0`).
- **O12 (Project Multi-Tenancy Masking):** Non-member querying `/api/v1/projects/:projectId/tasks` receives `404 Not Found`, masking project existence.
- **O13 (Due Date Boundary):** Submitting `dueDate < createdAt` returns `400 Bad Request` (`INVALID_DUE_DATE`). Document state unchanged (`H0`).
- **O14 (Description Boundary):** Submitting `description.length > 5000` returns `400 Bad Request` (`TASK_VALIDATION_ERROR`). Document state unchanged (`H0`).
- **O15 (Tag Constraint & Nullability):**
  - Submitting `tags.length > 10` returns `400 Bad Request` (`TASK_VALIDATION_ERROR`).
  - Submitting `"tags": null` returns `400 Bad Request` (`TAGS_MUST_BE_ARRAY`).
- **O16 (Idempotency Replay & Fingerprint Mismatch):**
  - Re-sending identical payload with same `Idempotency-Key` returns cached `200/201` without `version++` or duplicate history (`H0`).
  - Re-sending altered payload with same key returns `422 Unprocessable Entity` (`IDEMPOTENCY_KEY_PAYLOAD_MISMATCH`).
- **O17 (Audit Event Non-Snapshot Invariant):** Validating MongoDB `task_events` documents confirms absence of whole-task snapshots, descriptions, or user credentials.
- **O18 (T03: Direct Block - Forbidden):**
  - *Setup:* Task in `TODO`, `version: 1`. Request: `PATCH .../status` `{ "targetStatus": "BLOCKED", "reason": "Direct Block", "expectedVersion": 1 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 1`, `H0`.
- **O19 (T06: Reset to TODO - Forbidden):**
  - *Setup:* Task in `IN_PROGRESS`, `version: 2`. Request: `PATCH .../status` `{ "targetStatus": "TODO", "expectedVersion": 2 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 2`, `H0`.
- **O20 (T09: COMPLETE - Permitted Candidate):**
  - *Setup:* Task in `IN_PROGRESS`, `version: 2`. Request: `PATCH .../status` `{ "targetStatus": "DONE", "expectedVersion": 2 }`. Caller is Assignee.
  - *Expectation:* `200 OK`. `status = "DONE"`, `completedAt != null`, `version = 3`. Emits event.
- **O21 (T11: Blocked Reset to TODO - Forbidden):**
  - *Setup:* Task in `BLOCKED`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "TODO", "expectedVersion": 3 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 3`, `H0`.
- **O22 (T12: RESUME - Permitted Candidate):**
  - *Setup:* Task in `BLOCKED`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "IN_PROGRESS", "reason": "Impediment Resolved", "expectedVersion": 3 }`. Caller is Assignee.
  - *Expectation:* `200 OK`. `status = "IN_PROGRESS"`, `version = 4`. Emits event.
- **O23 (T14: Blocked Direct Complete - Forbidden):**
  - *Setup:* Task in `BLOCKED`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "DONE", "expectedVersion": 3 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 3`, `H0`.
- **O24 (T16: Complete Reset to TODO - Forbidden):**
  - *Setup:* Task in `DONE`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "TODO", "expectedVersion": 3 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 3`, `H0`.
- **O25 (T18: Complete Direct Block - Forbidden):**
  - *Setup:* Task in `DONE`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "BLOCKED", "expectedVersion": 3 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 3`, `H0`.
- **O26 (T20: Cancel Completed - Forbidden):**
  - *Setup:* Task in `DONE`, `version: 3`. Request: `PATCH .../status` `{ "targetStatus": "CANCELLED", "expectedVersion": 3 }`.
  - *Expectation:* `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version == 3`, `H0`.
- **O27 (Concurrent In-Flight Idempotency Duplicate):** Two concurrent requests with the identical `Idempotency-Key` arriving simultaneously: the second request returns `409 Conflict` (`CONCURRENT_OPERATION_IN_PROGRESS`) until the first completes.
- **O28 (Idempotency Key Expiry):** Re-submitting the same `Idempotency-Key` after 24 hours results in key eviction; request is processed as a fresh mutation rather than returning a cached response.
- **O29 (Audit Log Pagination & Successor Scoping):** Querying `GET /tasks/:taskId/events` returns paginated events matching `TaskEventResponseDTO`. Successors only view events after task handover.
- **O30 (Internal Route Caller Authentication):** Direct HTTP request to `/internal/tasks` without valid mTLS certificate or valid `x-service-token` returns `401 Unauthorized`.

---

## 5. Review & Sign-Off Checklist for Lead

- [x] **DATN-374:** Exact 1-to-1 inventory retaining original question IDs (`SRC-13-Q1` through `SRC-13-Q9`, `SRC-D02-01` through `SRC-D02-10`, `SRC-D03-P1..P3`). No gaps, no remapped IDs. Work Note / Handover classified as `PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION`. D-03 7-field baseline and D-04 runtime-seam boundaries preserved.
- [x] **DATN-375:** Formal Authority & Blocker Register (§3.1) covering all proposed policy areas, exact governing authority role, current status, action required to close gate, and blocked downstream issues. Baseline confirms 25 cells `Enabled: NO`. Candidate matrix details all 25 transition cells.
- [x] **DATN-376:** Correct downstream Jira keys and official summaries (`DATN-97`, `DATN-99 D-07`, `DATN-100 D-08`, `DATN-101 D-09`, `DATN-387`, `DATN-452`). Comprehensive test oracles covering O0 through O30 with explicit baseline vs conditional classification.
- [x] **Contract Precision:**
  - O0 matches D-03 §8 P3 exactly (`eventName`, `taskVersion`, `occurredAt`, `source: "HUMAN"`, `changedFields` without `_id`).
  - Reconciled transition target enum (`TODO` included in DTO; rejected at lifecycle layer with 409).
  - Explicit parameterized assertions for all transition oracles (O3, O4, O6, O7, O18–O26) asserting `409 Conflict`, error code, document state unchanged, and `H0`.
  - Resolved tags non-nullability (`tags` non-nullable; clear via `[]`).
  - Complete response & error DTO schemas, deterministic tie-breaker sorting (`_id: 1`), ADR-010 `/internal` mTLS trust contract, RBAC conflict disclosure, and SHA-256 idempotency fingerprinting.
- [x] **Jira & Review Boundary:** Document explicitly framed as contract specification and oracle designs; no false claims of executed test suites. Subtask statuses remain `In Review` pending human reviewer verification.
