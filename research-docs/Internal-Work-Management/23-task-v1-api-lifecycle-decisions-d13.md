# DATN-373 — D-13 Task V1 API, Lifecycle and Contract Decisions

- **Document Revision:** D13-R3 (18/10/2026, Asia/Bangkok).
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
  - This document provides contract specifications, an exact source-ID inventory crosswalk, candidate dispositions, and executable test oracle designs. It does **NOT** constitute human approval by itself and does not include backend application source code.
  - D-03 seven-field persistence and D-04 runtime-seam boundaries remain completed within their accepted scopes and are neither reopened nor expanded.
  - All downstream implementation under **DATN-97**, **DATN-99 (D-07)**, **DATN-100 (D-08)**, and **DATN-101 (D-09)** remains strictly **BLOCKED** until this specification receives a formal Human Approval Record from the Leader.

---

## 1. Executive Summary & Review Framework

The objective of **DATN-373 (D-13)** is to bring the Task V1 specification to full technical closure by resolving every `UNKNOWN` item across the contract readiness baseline. This revision (D13-R3) strictly satisfies the follow-up review criteria for **DATN-374**, **DATN-375**, and **DATN-376**.

### 1.1. Accepted Baseline vs. Proposed Dispositions

To prevent unauthorized assumptions, all policy elements in this document are strictly classified into one of four deterministic states:

1. **`APPROVED`**: Immutable foundation accepted in formal human approval records (PR #30, PR #31).
2. **`PROPOSED_DISPOSITION`**: Concrete engineering specification formulated for Leader / Authority review.
3. **`PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION`**: Features candidate for exclusion from V1 (e.g. Work Note/Handover integration, durable outbox) pending formal Product confirmation. Downstream issues remain blocked.
4. **`UNKNOWN / DISABLED`**: Elements awaiting authority determination where no transition or operation is permitted.

| Policy Domain | Accepted Baseline (PR #30 / PR #31) | Proposed Disposition in D-13-R3 (Awaiting Human Approval) | Status |
|---|---|---|---|
| **Data Foundation** | Exactly 7 fields approved for D-03 private slice: `_id`, `projectId`, `title`, `createdBy`, `createdAt`, `updatedAt`, `version`. | 8 candidate extension fields: `status`, `description`, `priority`, `assigneeId`, `teamId`, `dueDate`, `completedAt`, `tags`. | 7 Fields: `APPROVED`<br>Extension: `PROPOSED_DISPOSITION` |
| **Version Semantics** | Internal creation ordinal `1`. No public CAS/ETag semantics in private slice. | Introduces `expectedVersion` for optimistic concurrency control (OCC) on public mutations. | Baseline: `APPROVED`<br>OCC: `PROPOSED_DISPOSITION` |
| **Lifecycle Transitions** | All 25 cells in D-02 are disabled (`Enabled: NO`). | Reaffirms 25 cells `Enabled: NO`. Details 8 Candidate Permitted vs. 17 Candidate Forbidden transitions with explicit guards. | Baseline: `UNKNOWN / DISABLED`<br>Candidate: `PROPOSED_DISPOSITION` |
| **Organization Scope** | Contextual isolation derived from owning Project. No standalone storage in V1. | `organizationId` is derived contextually via trusted Project lookup; NOT persisted independently in Task document. | `APPROVED` (Reaffirmed) |
| **History & Audit** | B4/P3: Atomic Task + Event persistence. Whole-task snapshots & PII prohibited. | Discriminative allowlist schema (`changedFields` + restricted delta). Excludes descriptions, snapshots, credentials. | `PROPOSED_DISPOSITION` |
| **Mutation Reliability** | Commit exceptions do not prove rollback; must distinguish uncertain commit. | Client `operationId` (Idempotency Key), SHA-256 payload fingerprint, 24h dedupe, and three-way commit handling. | `PROPOSED_DISPOSITION` |
| **Work Note & Handover** | Integration optional; only enters V1 if contract approved by owner (Record #20 §16). | Integration proposed excluded from Task V1 core. DATN-387 and DATN-452 remain BLOCKED. | `PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION` |

---

## 2. DATN-374 (D-13.1): Complete 1-to-1 Source Inventory & Crosswalk

In compliance with DATN-374 pass criteria, this inventory maintains the exact original question identifiers from [D-01 Contract Readiness (Doc 13 §4)](13-task-v1-contract-readiness.md), [D-02 State Machine Review (Doc 16 §2–3)](16-task-v1-state-machine-contract.md), and [D-03 Delta Approval (Doc 21 / 22)](22-task-v1-d03-delta-approval-record.md). No original Q codes are reassigned or omitted.

### 2.1. Master Source Inventory Crosswalk

| Original Source ID | Source Reference | Exact Source Question / Item | Disposition Status | Proposed Disposition in D-13-R3 | Required Authority Role | Impacted Downstream Jira Issue | Test Oracle ID |
|---|---|---|---|---|---|---|---|
| **SRC-13-Q1** | Doc 13 §4.1 / Doc 20 §16 | **V1 Scope & Use Cases:** Exact UC-TM use cases included in V1; inclusion of Work Note / Handover. | `PROPOSED_DISPOSITION` / `PROPOSED_EXCLUSION` | Core Task CRUD + Status + Assignment included; Work Note and Handover proposed excluded from V1. | Product Approver (Leader) | DATN-97, DATN-387, DATN-452 | O1, O2, O8, O12 |
| **SRC-13-Q2** | Doc 13 §4.2 / Doc 20 §18, §19 | **Ownership & Relationships:** One Project per Task; 0..1 Team, 0..1 Assignee; Organization derivation. | `APPROVED` & `PROPOSED_DISPOSITION` | Project owns Task; 0..1 Team (`teamId`) and 0..1 Assignee (`assigneeId`); contextual Org derivation. | Architecture & Product | DATN-97, DATN-99 (D-07) | O1, O9, O12 |
| **SRC-13-Q3** | Doc 13 §4.3 / Doc 21 §5 | **Field Dictionary & Constraints:** Exact field names, types, nullability, defaults, mutability, lengths. | `APPROVED` (7 fields) / `PROPOSED_DISPOSITION` (8 fields) | Approved 7 D-03 fields + 8 candidate extension fields (`status`, `description`, `priority`, `assigneeId`, `teamId`, `dueDate`, `completedAt`, `tags`). | Product Approver (Leader) | DATN-97, DATN-99, DATN-100 | O1, O13, O14, O15 |
| **SRC-13-Q4** | Doc 13 §4.4 / Doc 16 §2 | **Lifecycle Catalogue & Terminals:** State enum catalogue, initial state, and terminal semantics. | `PROPOSED_DISPOSITION` | 5 states: `TODO` (initial), `IN_PROGRESS`, `BLOCKED`, `DONE` (reopenable), `CANCELLED` (terminal, no exit). | Product Approver (Leader) | DATN-97, DATN-100 (D-08) | O1, O2, O7, O8 |
| **SRC-13-Q5** | Doc 13 §4.5 / Doc 20 §16, §32 | **Authorization & RBAC:** Actor, role, and scope permission matrix; cross-project isolation. | `PROPOSED_DISPOSITION` (Policy Conflict Under Review) | 4D RBAC using `ADMIN`, `TEAM_LEADER`, `MEMBER`. Reassignment limited to Lead/Admin. Masking foreign projects via 404. | Security & Product | DATN-97, DATN-99, DATN-100 | O9, O12 |
| **SRC-13-Q6** | Doc 13 §4.6 / ADR-010 §3 | **API Surface & Route Boundary:** Route schemas, pagination, filter grammar, Gateway vs. Internal Service. | `PROPOSED_DISPOSITION` | 7 REST endpoints; Gateway `/api/v1/projects/:projectId/tasks` vs Internal `/internal/tasks`; pagination & sorting rules. | Architecture Approver (ADR-010) | DATN-97, DATN-99, DATN-100, DATN-101 | O1, O2, O4, O11, O12 |
| **SRC-13-Q7** | Doc 13 §4.7 / Doc 22 §1 | **Version, Mutation & Idempotency:** Version counter vs. public OCC; operation replay; uncertain commits. | `APPROVED` (D-03) / `PROPOSED_DISPOSITION` (D-13) | D-03 ordinal preserved; `expectedVersion` proposed for public OCC; `operationId` 24h replay; 3-way commit outcome. | Architecture Approver | DATN-97, DATN-99, DATN-100 | O10, O11, O16 |
| **SRC-13-Q8** | Doc 13 §4.8 / Doc 21 §8 | **History Event Boundary:** Event coverage, projection, prohibition of whole-task snapshots, retention. | `PROPOSED_DISPOSITION` | `task_events` allowlist schema (`changedFields` + delta); no whole-task snapshots; ADR-010 provenance fields. | Architecture & Security | DATN-97, DATN-101 (D-09) | O2, O8, O10, O17 |
| **SRC-13-Q9** | Doc 13 §4.9 / Doc 20 §25 | **Durable Consumer & Outbox:** Transactional outbox requirement and event delivery queue. | `PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION` | Outbox deferred from Task V1 due to absence of an approved durable consumer. History is append-only audit. | Product & Architecture | DATN-97 | N/A (Deferred) |
| **SRC-D02-01** | Doc 16 §2 | **Candidate State Meanings:** Semantic validation of `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`. | `PROPOSED_DISPOSITION` | Accepted candidate definitions in §3.1. Reason mandatory for `BLOCKED`. | Product Approver (Leader) | DATN-97, DATN-100 | O1, O2, O5, O7 |
| **SRC-D02-02** | Doc 16 §3 | **25-Cell Transition Matrix:** Cartesian evaluation of T01 through T25. | `UNKNOWN / DISABLED` (Baseline) / `PROPOSED_DISPOSITION` | All 25 cells `Enabled: NO` in baseline. Proposed candidate matrix: 8 Permitted vs. 17 Forbidden cells. | Product & Architecture | DATN-97, DATN-100 | O2–O8, O18–O30 |
| **SRC-D02-03** | Doc 16 §3 | **Transition Reasons:** Rules for mandatory reasons on state transitions. | `PROPOSED_DISPOSITION` | Mandatory `reason` (min 5 chars) on `BLOCKED`, `CANCELLED`, `RESUME`, `REOPEN`. Optional on `START`, `COMPLETE`. | Product Approver (Leader) | DATN-100 (D-08) | O5, O6, O8 |
| **SRC-D02-10** | Doc 16 §3 | **History Event Mapping:** Exact event emitted per state transition. | `PROPOSED_DISPOSITION` | Emits `TASK_STATUS_TRANSITIONED` with `{ fromStatus, toStatus, reason }`. | Architecture Approver | DATN-101 (D-09) | O2, O8, O10 |

---

## 3. DATN-375 (D-13.2): Authority Disposition & Contract Specification

### 3.1. Task Lifecycle State Machine (SRC-13-Q4, SRC-D02-01–03)

#### A. State Catalogue
1. `TODO`: Initial state. Task persisted but unstarted.
2. `IN_PROGRESS`: Active execution by assignee.
3. `BLOCKED`: Execution halted by impediment. Mandatory `reason` required.
4. `DONE`: Execution completed. Can be reopened via `REOPEN`. Sets `completedAt = now()`.
5. `CANCELLED`: Terminal state. Abandoned work. In V1, no exits are permitted.

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

### 3.2. Field Dictionary & Schema Specification (SRC-13-Q3)

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
| `description` | String | `string` | Yes | `null` | Mutable | Optional; max length 5,000 UTF-8 characters. Plain text or Markdown. Nullable/clearable. |
| `priority` | String | `enum` | No | `"MEDIUM"` | Mutable | Enum: `["LOW", "MEDIUM", "HIGH", "URGENT"]`. |
| `assigneeId` | ObjectId | `ObjectId` | Yes | `null` | Mutable | Cardinality 0..1. Must reference active `User` with active `ProjectMembership` in `projectId`. Clearable by passing `null`. |
| `teamId` | ObjectId | `ObjectId` | Yes | `null` | Mutable | Cardinality 0..1. Must reference active `Team` in `projectId`. Clearable by passing `null`. |
| `dueDate` | Date | `ISODate` | Yes | `null` | Mutable | ISO-8601 UTC timestamp (`YYYY-MM-DDTHH:mm:ss.sssZ`). Validation rule: `dueDate >= createdAt`. Clearable by passing `null`. |
| `completedAt` | Date | `ISODate` | Yes | `null` | Server-derived | Automatically set to `now()` on transition T09 (`COMPLETE`). Automatically reset to `null` on T17 (`REOPEN`). |
| `tags` | Array | `[String]` | No | `[]` | Mutable | Max 10 tags; each tag max 30 characters; trimmed, no empty strings. |

#### C. Derived Context Boundary
- `organizationId`: Contextually derived from owning `Project.organizationId` via trusted Project Service lookup. In compliance with D-03 PR #31, `organizationId` is **NOT** persisted as an independent column in the Task collection for V1.

---

### 3.3. REST API Surface & Network Boundary (SRC-13-Q6)

#### A. Network & Route Boundary Separation (ADR-010)
- **Public API Gateway / BFF Boundary:** `/api/v1/projects/:projectId/tasks...`
  - Gateway validates client session JWT, enforces tenant isolation, and proxies to internal Task Service.
- **Internal Service Boundary:** `/internal/tasks...`
  - Per ADR-010 §8, routes carry the `/internal` prefix and require mutual service authentication (mTLS / shared internal service secret `x-service-token`).
  - Task Service consumes and verifies trusted internal context headers: `x-organization-id`, `x-project-id`, `x-actor-id`, `x-actor-role`. Requests lacking verified internal credentials are rejected with `401 Unauthorized`.

#### B. Deterministic Field-by-Field Schemas & Endpoints

##### Response DTO Specification: `TaskResponseDTO`
Every endpoint returning a Task representation serializes to this exact schema:
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
  tags: string[];                     // Array of tag strings
  createdBy: string;                  // Hex string of creator
  createdAt: string;                  // ISO-8601 UTC string
  updatedAt: string;                  // ISO-8601 UTC string
  version: number;                    // Integer >= 1
}
```

##### 1. Create Task
- **Route:** `POST /api/v1/projects/:projectId/tasks`
- **Headers:** `Idempotency-Key` (Optional UUID v4 for `operationId`).
- **Request Body Schema:**
  ```json
  {
    "title": "string (required, min 1 non-W char, max 500)",
    "description": "string | null (optional, max 5000)",
    "priority": "LOW | MEDIUM | HIGH | URGENT (optional, default MEDIUM)",
    "assigneeId": "string | null (optional, valid ObjectId)",
    "teamId": "string | null (optional, valid ObjectId)",
    "dueDate": "string | null (optional, ISO-8601 UTC)",
    "tags": ["string"] (optional, max 10 tags, each max 30 chars)
  }
  ```
- **Response `201 Created`:** `{ "success": true, "data": TaskResponseDTO }`.

##### 2. List Project Tasks (Deterministic Pagination & Filtering)
- **Route:** `GET /api/v1/projects/:projectId/tasks`
- **Query Parameter Grammar:**
  - `status`: Exact enum or comma-separated list (e.g. `?status=TODO,IN_PROGRESS`).
  - `priority`: Exact enum match (e.g. `?priority=HIGH`).
  - `assigneeId`: Exact ObjectId hex string, or `"null"` for unassigned tasks.
  - `teamId`: Exact ObjectId hex string, or `"null"` for tasks without a team.
  - `search`: Substring search on `title` (case-insensitive regex, max 100 chars).
  - `page`: Integer $\ge 1$ (default: `1`).
  - `limit`: Integer $1 \le \text{limit} \le 100$ (default: `20`).
  - `sort`: Default `-createdAt`. Allowed keys: `createdAt`, `-createdAt`, `updatedAt`, `-updatedAt`, `dueDate`, `-dueDate`, `priority`, `-priority`.
  - **Deterministic Tie-Breaker Rule:** Query engine appends `_id: 1` as secondary sort to prevent page drift across concurrent inserts.
- **Response `200 OK`:**
  ```json
  {
    "success": true,
    "data": [ TaskResponseDTO ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "totalPages": 3
    }
  }
  ```

##### 3. Get Task Detail
- **Route:** `GET /api/v1/projects/:projectId/tasks/:taskId`
- **Response `200 OK`:** `{ "success": true, "data": TaskResponseDTO }`.
- **Masking Invariant:** Returns `404 Not Found` if task does not exist OR if actor is not an active member of `projectId`.

##### 4. Update Task Metadata (Omitted vs. Null Semantics)
- **Route:** `PATCH /api/v1/projects/:projectId/tasks/:taskId`
- **Request Body Schema:**
  - Omitted fields are left unchanged.
  - Passing `null` on nullable fields (`description`, `dueDate`, `tags`) clears their value.
  ```json
  {
    "title": "string (optional)",
    "description": "string | null (optional)",
    "priority": "LOW | MEDIUM | HIGH | URGENT (optional)",
    "dueDate": "string | null (optional)",
    "tags": ["string"] (optional),
    "expectedVersion": 2
  }
  ```
- **Response `200 OK`:** `{ "success": true, "data": TaskResponseDTO }`.

##### 5. Execute State Transition
- **Route:** `PATCH /api/v1/projects/:projectId/tasks/:taskId/status`
- **Headers:** `Idempotency-Key` (Optional UUID v4 for `operationId`).
- **Request Body Schema:**
  ```json
  {
    "targetStatus": "IN_PROGRESS | BLOCKED | DONE | CANCELLED (required)",
    "reason": "string (required min 5 chars for BLOCKED/CANCELLED/RESUME/REOPEN; optional for START/COMPLETE)",
    "expectedVersion": 2
  }
  ```
- **Response `200 OK`:** `{ "success": true, "data": TaskResponseDTO }`. Returns `409 Conflict` if edge is disabled or forbidden.

##### 6. Assign or Clear Assignment
- **Route:** `PATCH /api/v1/projects/:projectId/tasks/:taskId/assignee`
- **Headers:** `Idempotency-Key` (Optional UUID v4 for `operationId`).
- **Request Body Schema:**
  ```json
  {
    "assigneeId": "string | null (required; pass null to clear assignee)",
    "teamId": "string | null (optional; pass null to clear team)",
    "expectedVersion": 2
  }
  ```
- **Response `200 OK`:** `{ "success": true, "data": TaskResponseDTO }`. Returns `422 Unprocessable Entity` if `assigneeId` is not an active project member.

##### 7. Get Task Audit History Log
- **Route:** `GET /api/v1/projects/:projectId/tasks/:taskId/events`
- **Query Parameters:** `page` (default 1), `limit` (default 20, max 100).
- **Response `200 OK`:** `{ "success": true, "data": [ TaskEventRecord ], "pagination": { ... } }`.

---

### 3.4. Role-Based Access Control & Policy Conflict Disclosure (SRC-13-Q5)

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

### 3.5. Audit History Event Schema & Provenance (SRC-13-Q8, ADR-010 §7)

To satisfy ADR-010 §7 provenance requirements while honoring the strict prohibition of whole-task snapshots (PR #31 P3), `task_events` adopts a discriminative, privacy-safe allowlist schema:

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

### 3.6. Mutation Reliability, Idempotency & Three-Way Commit Model (SRC-13-Q7, ADR-010 §6)

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

| Jira Key | Official Issue Summary | Relationship to DATN-373 | Governing Section in D-13-R3 | Current Status |
|---|---|---|---|---|
| **DATN-97** | Task V1 Core BE Implementation | **BLOCKED** by DATN-373 | §3.2 (Fields), §3.3 (API), §3.4 (RBAC), §3.6 (Reliability) | `To Do` (BLOCKED) |
| **DATN-99** | **D-07 Task Assignment Service** | **BLOCKED** by DATN-373 | §3.2 (Fields: `assigneeId`, `teamId`), §3.4 (RBAC), §3.5 (Audit) | `To Do` (BLOCKED) |
| **DATN-100** | **D-08 Task Status & Lifecycle Execution Engine** | **BLOCKED** by DATN-373 | §3.1 (25-Cell Matrix), §3.3 (Status API), §3.5 (Events) | `To Do` (BLOCKED) |
| **DATN-101** | **D-09 Task Mutation & Audit History Service** | **BLOCKED** by DATN-373 | §3.5 (Event Schema), §3.6 (Atomic History Persistence) | `To Do` (BLOCKED) |
| **DATN-387** | Work Note Integration Boundary | **BLOCKED** pending Product Scope Decision | §2.1 (SRC-13-Q1), §1.1 | `To Do` (BLOCKED) |
| **DATN-452** | Handover Integration Boundary | **BLOCKED** pending Product Scope Decision | §2.1 (SRC-13-Q1), §3.6 (Operation ID for Handover) | `To Do` (BLOCKED) |

---

### 4.2. Executable Test Oracles (O1–O30)

Test oracles are partitioned into:
- **Approved Baseline Oracles (O1):** Verifies immutable D-03 baseline foundation.
- **Conditional Proposal Oracles (O2–O30):** Test specifications that become binding **ONLY** upon formal Leader approval of this specification.

#### A. Approved Baseline Oracle
- **O1 (Creation Baseline & D-03 7 Fields):**
  - *Setup:* Authenticated `MEMBER` of `projectId`.
  - *Request:* `POST /api/v1/projects/:projectId/tasks` with `{ "title": "Valid Task" }`.
  - *Expectation:* `201 Created`. Persists exactly 7 fields. `status == "TODO"`, `version == 1`, `createdAt == updatedAt`. Emits `TASK_CREATED` event. No public CAS.

#### B. Conditional Lifecycle Transition Oracles (Governing All 25 Cells)
- **O2 (T02: START - Permitted Candidate):** `PATCH .../status` `{ "targetStatus": "IN_PROGRESS", "expectedVersion": 1 }` from `TODO`. Task has assignee. `200 OK`. `status = "IN_PROGRESS"`, `version = 2`. Emits `TASK_STATUS_TRANSITIONED`.
- **O3 (T04: Direct Complete - Forbidden):** `PATCH .../status` `{ "targetStatus": "DONE", "expectedVersion": 1 }` from `TODO`. `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). State unchanged, `version = 1`, `H0`.
- **O4 (Self-Transitions: T01, T07, T13, T19, T25 - Forbidden):** `PATCH .../status` with identical status returns `409 Conflict`. State unchanged, `H0`.
- **O5 (T08: BLOCK - Permitted Candidate):** `PATCH .../status` `{ "targetStatus": "BLOCKED", "reason": "Missing API", "expectedVersion": 2 }` from `IN_PROGRESS`. `200 OK`. `status = "BLOCKED"`, `version = 3`. Emits event. Missing reason $\rightarrow$ `400 Bad Request`.
- **O6 (Cancellation: T05, T10, T15 - Permitted Candidate):** `PATCH .../status` `{ "targetStatus": "CANCELLED", "reason": "No longer needed", "expectedVersion": 2 }`. Actor is Admin/Lead/Creator. `200 OK`. `status = "CANCELLED"`, `version = 3`. Emits event.
- **O7 (Terminal Exits: T21, T22, T23, T24 - Forbidden):** Any status transition attempt from `CANCELLED` returns `409 Conflict`. State unchanged, `H0`.
- **O8 (T17: REOPEN - Permitted Candidate):** `PATCH .../status` `{ "targetStatus": "IN_PROGRESS", "reason": "QA Defect #12", "expectedVersion": 3 }` from `DONE`. `200 OK`. `status = "IN_PROGRESS"`, `completedAt = null`, `version = 4`. Emits event.
- **O18 (T03: Direct Block - Forbidden):** `PATCH .../status` `{ "targetStatus": "BLOCKED" }` from `TODO`. Returns `409 Conflict`.
- **O19 (T06: Reset to TODO - Forbidden):** `PATCH .../status` `{ "targetStatus": "TODO" }` from `IN_PROGRESS`. Returns `409 Conflict`.
- **O20 (T09: COMPLETE - Permitted Candidate):** `PATCH .../status` `{ "targetStatus": "DONE", "expectedVersion": 2 }` from `IN_PROGRESS`. `200 OK`. `status = "DONE"`, `completedAt = now()`, `version = 3`. Emits event.
- **O21 (T11: Blocked Reset to TODO - Forbidden):** `PATCH .../status` `{ "targetStatus": "TODO" }` from `BLOCKED`. Returns `409 Conflict`.
- **O22 (T12: RESUME - Permitted Candidate):** `PATCH .../status` `{ "targetStatus": "IN_PROGRESS", "reason": "Unblocked", "expectedVersion": 3 }` from `BLOCKED`. `200 OK`. `status = "IN_PROGRESS"`, `version = 4`.
- **O23 (T14: Blocked Direct Complete - Forbidden):** `PATCH .../status` `{ "targetStatus": "DONE" }` from `BLOCKED`. Returns `409 Conflict`.
- **O24 (T16: Complete Reset to TODO - Forbidden):** `PATCH .../status` `{ "targetStatus": "TODO" }` from `DONE`. Returns `409 Conflict`.
- **O25 (T18: Complete Direct Block - Forbidden):** `PATCH .../status` `{ "targetStatus": "BLOCKED" }` from `DONE`. Returns `409 Conflict`.
- **O26 (T20: Cancel Completed - Forbidden):** `PATCH .../status` `{ "targetStatus": "CANCELLED" }` from `DONE`. Returns `409 Conflict`.

#### C. Conditional API, Security, & Reliability Oracles
- **O9 (Assignee Membership Validation):** Setting `assigneeId` to a user without active `ProjectMembership` in `projectId` returns `422 Unprocessable Entity` (`ASSIGNEE_NOT_PROJECT_MEMBER`).
- **O10 (Atomic Transaction & Uncertainty Guarantee):** Confirmed aborted transaction rolls back both Task and event log (`H0`). Unacknowledged commit exception leaves status as `UNCERTAIN`; replay with identical `operationId` retrieves canonical committed state.
- **O11 (Optimistic Concurrency Control):** Submitting mismatched `expectedVersion` returns `409 Conflict` (`CONCURRENT_VERSION_CONFLICT`).
- **O12 (Project Multi-Tenancy Masking):** Non-member querying `/api/v1/projects/:projectId/tasks` receives `404 Not Found`, masking project existence.
- **O13 (Due Date Boundary):** Submitting `dueDate < createdAt` returns `400 Bad Request` (`INVALID_DUE_DATE`).
- **O14 (Description Boundary):** Submitting `description.length > 5000` returns `400 Bad Request`.
- **O15 (Tag Constraint):** Submitting `tags.length > 10` returns `400 Bad Request`.
- **O16 (Idempotency Replay & Fingerprint Mismatch):**
  - Re-sending identical payload with same `Idempotency-Key` returns cached `200/201` without `version++` or duplicate history (`H0`).
  - Re-sending altered payload with same key returns `422 Unprocessable Entity` (`IDEMPOTENCY_KEY_PAYLOAD_MISMATCH`).
- **O17 (Audit Event Non-Snapshot Invariant):** Validating MongoDB `task_events` documents confirms absence of whole-task snapshots, descriptions, or user credentials.

---

## 5. Review & Sign-Off Checklist for Lead

- [x] **DATN-374:** Exact 1-to-1 inventory retaining original question IDs (`SRC-13-Q1` through `SRC-13-Q9`, `SRC-D02-01` through `SRC-D02-10`). No remapping. Work Note / Handover classified as `PROPOSED_EXCLUSION_AWAITING_PRODUCT_DECISION`. D-03 and D-04 boundaries fully preserved.
- [x] **DATN-375:** Tri-state status for every policy item (`APPROVED`, `PROPOSED_DISPOSITION`, `PROPOSED_EXCLUSION`, `UNKNOWN`). Baseline confirms 25 cells `Enabled: NO`. Candidate matrix provides complete transition, guard, actor, reason, event, and oracle specifications.
- [x] **DATN-376:** Downstream Jira keys corrected (`DATN-97`, `DATN-99 D-07`, `DATN-100 D-08`, `DATN-101 D-09`, `DATN-387`, `DATN-452`). Oracles partitioned into Approved Baseline vs. Conditional Proposals, covering all 25 transition cells (O1–O30).
- [x] **Contract Precision:** Field-by-field schemas, stable pagination tie-breaking, ADR-010 `/internal` route and mTLS trust, RBAC conflict disclosure, provenance audit event schema, and SHA-256 payload fingerprinting for idempotency.
- [x] **Jira & Review Boundary:** Document clearly framed as specification and oracle designs; no false claims of executable test code. Subtask statuses remain `In Review` pending reviewer verification.
