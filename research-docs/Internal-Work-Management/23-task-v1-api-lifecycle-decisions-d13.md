# DATN-373 — D-13 Task V1 API, Lifecycle and Contract Decisions

- **Document Revision:** D13-R2 (18/10/2026, Asia/Bangkok).
- **Document Status:** PROPOSED DISPOSITION & CONTRACT SPECIFICATION FOR REVIEW.
- **Review Authority Required:**
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
  - This is a specification, inventory, and disposition document. It does NOT constitute human approval by itself.
  - No backend/frontend source code, schema migration, or database cutover is introduced in this document.
  - All downstream implementation under **DATN-97**, **D-05**, **D-07**, and **D-08** remains strictly **BLOCKED** until this document receives a formal Human Approval Record from the Leader.

---

## 1. Executive Summary & Review Context

The primary purpose of **DATN-373 (D-13)** is to eliminate all remaining `UNKNOWN` items identified in earlier contract readiness reviews (D-01, D-02, D-03) by establishing a comprehensive, deterministic specification for:
1. **Task V1 Lifecycle State Machine:** Resolving the 5-state catalogue and the complete 25-cell transition matrix.
2. **Extended Field Dictionary:** Defining exact field types, constraints, mutability, and nullability beyond D-03's 7 foundation fields.
3. **REST API Endpoint Surface:** Formulating deterministic request, response, query, and pagination schemas separating Gateway from internal Task Service.
4. **Role-Based Access Control (RBAC):** Aligning permissions strictly with the active project roles (`ADMIN`, `TEAM_LEADER`, `MEMBER`).
5. **Mutation Reliability, Event Logging & Idempotency:** Providing a three-way commit resolution model (`CONFIRMED_SUCCESS`, `CONFIRMED_REJECTED`, `UNCERTAIN`) and restricting `task_events` to a privacy-safe, non-snapshot allowlist.

### 1.1. Accepted Baseline vs. Proposed Dispositions

To prevent unauthorized assumptions, this document strictly differentiates between what has already been approved and what is proposed for decision:

| Layer | Accepted Baseline (Immutable without new Approval) | Proposed Disposition in D-13 (Awaiting Human Review) |
|---|---|---|
| **Data Foundation** | 7 required persisted fields approved for D-03 private slice: `_id`, `projectId`, `title`, `createdBy`, `createdAt`, `updatedAt`, `version`. | Proposed candidate extension fields: `status`, `description`, `priority`, `assigneeId`, `teamId`, `dueDate`, `completedAt`, `tags`. |
| **State Transitions** | 0 transitions enabled. All 25 cells in D-02 are marked `UNKNOWN / Enabled: NO`. | Proposed candidate disposition: 8 Permitted transitions vs. 17 Forbidden transitions with explicit guards and reason checks. |
| **Organization Context** | Derived contextual isolation from owning Project. No standalone storage in V1. | Reaffirmed: `organizationId` is derived contextually from `Project.organizationId`; not persisted independently in Task V1. |
| **Audit Logging** | Atomic Task + Event write approved in B4 / P3. Content snapshots and PII prohibited. | Strict allowlist event schema (`changedFields` and structured delta only; whole-task snapshot strictly forbidden). |
| **Reliability** | Exception during commit does not prove rollback; must distinguish uncertain commit. | Standardized `operationId` (Idempotency Key) and three-way commit outcome handling. |

---

## 2. DATN-374 (D-13.1): Inventory of Unresolved Decisions

This section catalogs every unresolved item from D-01, D-02, and D-03, mapping each to its governing question, authority domain, subsystem, and downstream blocking impact.

### 2.1. Decision Inventory & Categorization Matrix

| Item ID | Governing Question / Source | Unresolved Scope & Description | Authority Domain | Subsystem Boundary | Downstream Blocking Impact |
|---|---|---|---|---|---|
| **INV-01** | Q4 / D02-01 ([Doc 16](16-task-v1-state-machine-contract.md) §2) | 5-State lifecycle catalogue (`TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`), initial state semantics, and terminal state immutability. | Product | Task Lifecycle Engine | Blocks D-07, DATN-97 |
| **INV-02** | Q4, Q5, Q7 / D02-02 ([Doc 16](16-task-v1-state-machine-contract.md) §3) | Complete 25-cell state transition matrix ($5 \times 5$), determining allowed edges, forbidden skips, self-loops, and required reason payloads. | Product & Arch | Task Lifecycle Engine | Blocks D-07, D-08, DATN-97 |
| **INV-03** | Q1, Q2 ([Doc 13](13-task-v1-contract-readiness.md) §4) | Field dictionary expansion: `status`, `description`, `priority`, `assigneeId`, `teamId`, `dueDate`, `completedAt`, `tags`. | Product | Task Schema & DTO | Blocks D-05, D-08, DATN-97 |
| **INV-04** | Q6, Q9 ([Doc 13](13-task-v1-contract-readiness.md) §4) | REST API surface, pagination limits, sorting rules, clear-assignment semantics, and Gateway vs. Internal Service route separation. | Architecture | Task API Router | Blocks DATN-97, FE BFF |
| **INV-05** | Q5 ([Doc 13](13-task-v1-contract-readiness.md) §4) | Actor, role, and permission matrix based on active project roles (`ADMIN`, `TEAM_LEADER`, `MEMBER`), cross-project isolation, and team eligibility. | Security & Arch | Authorization Guard | Blocks DATN-97, D-07, D-08 |
| **INV-06** | Q8, B4, P3 ([Doc 21](21-task-v1-d03-contract-delta.md) §8) | Mutation audit projection in `task_events`: prohibition of whole-task snapshots and restriction to allowlist delta. | Architecture & Sec | History Event Store | Blocks DATN-97, D-07, D-08 |
| **INV-07** | ADR-010 §5, P3 ([Doc 22](22-task-v1-d03-delta-approval-record.md) §2) | Command reliability: `operationId` replay, idempotency deduplication window, and three-way outcome handling (`UNCERTAIN` commits). | Architecture | Reliability & Mongo Tx | Blocks DATN-97, Test Suite |
| **INV-08** | Q1, Q7 ([Doc 20](20-task-v1-contract-approval-record.md) §25, §26) | Work Note / Handover integration, agent autonomous mutation, and soft deletion: confirmed excluded from Task V1. | Product | Integration Boundary | Excluded from V1 Scope |

---

## 3. DATN-375 (D-13.2): Recommended Authority Disposition

### 3.1. Task Lifecycle State Machine Disposition (INV-01, INV-02)

#### A. State Catalogue
The Task V1 lifecycle consists of exactly 5 canonical states:
- `TODO` (Initial State): Newly created task. Work has not commenced.
- `IN_PROGRESS` (Active State): Actively being executed.
- `BLOCKED` (Halted State): Impediment encountered. Requires mandatory reason.
- `DONE` (Completed State): Deliverables satisfied. Can be reopened if review rejects. Sets `completedAt`.
- `CANCELLED` (Terminal State): Discarded or abandoned work. In V1, no transitions out of `CANCELLED` are permitted.

#### B. The 25-Cell State Transition Matrix
**Accepted Baseline Status:** All 25 cells currently remain **`DISABLED (Enabled: NO)`**.
**Proposed Candidate Disposition:** Evaluates 8 Candidate Permitted edges and 17 Candidate Forbidden edges.

| Cell | From | To | Accepted Baseline | Proposed Disposition | Trigger Command | Permitted Actor Roles | Guard Conditions & Reason Requirements | Side Effects & Event |
|---|---|---|---|---|---|---|---|---|
| **T01** | `TODO` | `TODO` | DISABLED | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. | None (`H0`). |
| **T02** | `TODO` | `IN_PROGRESS` | DISABLED | **Candidate Permitted** | `START` | Assignee, `TEAM_LEADER`, `ADMIN` | Task must have an active `assigneeId`. Optional reason. | Increments `version`. Emits `TASK_STATUS_TRANSITIONED`. |
| **T03** | `TODO` | `BLOCKED` | DISABLED | **FORBIDDEN** | Direct-Block | None | Work not started cannot be blocked. Must `START` first. Returns 409 Conflict. | None (`H0`). |
| **T04** | `TODO` | `DONE` | DISABLED | **FORBIDDEN** | Direct-Complete | None | Work not started cannot be completed. Must `START` first. Returns 409 Conflict. | None (`H0`). |
| **T05** | `TODO` | `CANCELLED` | DISABLED | **Candidate Permitted** | `CANCEL` | `ADMIN`, `TEAM_LEADER`, Creator | Mandatory `reason` (min 5 characters). | Increments `version`. Emits `TASK_STATUS_TRANSITIONED`. |
| **T06** | `IN_PROGRESS` | `TODO` | DISABLED | **FORBIDDEN** | Reset | None | Cannot unstart work already in progress. Returns 409 Conflict. | None (`H0`). |
| **T07** | `IN_PROGRESS` | `IN_PROGRESS` | DISABLED | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. | None (`H0`). |
| **T08** | `IN_PROGRESS` | `BLOCKED` | DISABLED | **Candidate Permitted** | `BLOCK` | Assignee, `TEAM_LEADER`, `ADMIN` | Mandatory `reason` (min 5 characters) explaining impediment. | Increments `version`. Emits `TASK_STATUS_TRANSITIONED`. |
| **T09** | `IN_PROGRESS` | `DONE` | DISABLED | **Candidate Permitted** | `COMPLETE` | Assignee, `TEAM_LEADER`, `ADMIN` | Optional completion note. | Sets `completedAt = now()`, increments `version`. Emits `TASK_STATUS_TRANSITIONED`. |
| **T10** | `IN_PROGRESS` | `CANCELLED` | DISABLED | **Candidate Permitted** | `CANCEL` | `ADMIN`, `TEAM_LEADER`, Creator | Mandatory `reason` (min 5 characters). | Increments `version`. Emits `TASK_STATUS_TRANSITIONED`. |
| **T11** | `BLOCKED` | `TODO` | DISABLED | **FORBIDDEN** | Reset | None | Cannot reset blocked task to unstarted. Returns 409 Conflict. | None (`H0`). |
| **T12** | `BLOCKED` | `IN_PROGRESS` | DISABLED | **Candidate Permitted** | `RESUME` | Assignee, `TEAM_LEADER`, `ADMIN` | Mandatory `reason` (min 5 characters) detailing unblocking resolution. | Increments `version`. Emits `TASK_STATUS_TRANSITIONED`. |
| **T13** | `BLOCKED` | `BLOCKED` | DISABLED | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. | None (`H0`). |
| **T14** | `BLOCKED` | `DONE` | DISABLED | **FORBIDDEN** | Direct-Complete | None | Cannot complete directly while blocked. Must `RESUME` first. Returns 409 Conflict. | None (`H0`). |
| **T15** | `BLOCKED` | `CANCELLED` | DISABLED | **Candidate Permitted** | `CANCEL` | `ADMIN`, `TEAM_LEADER`, Creator | Mandatory `reason` (min 5 characters). | Increments `version`. Emits `TASK_STATUS_TRANSITIONED`. |
| **T16** | `DONE` | `TODO` | DISABLED | **FORBIDDEN** | Reset | None | Cannot uncomplete to unstarted. Returns 409 Conflict. | None (`H0`). |
| **T17** | `DONE` | `IN_PROGRESS` | DISABLED | **Candidate Permitted** | `REOPEN` | `ADMIN`, `TEAM_LEADER`, Creator | Mandatory `reason` (min 5 characters) explaining review rejection. | Clears `completedAt = null`, increments `version`. Emits `TASK_STATUS_TRANSITIONED`. |
| **T18** | `DONE` | `BLOCKED` | DISABLED | **FORBIDDEN** | Direct-Block | None | Completed task cannot be blocked directly. Reopen first. Returns 409 Conflict. | None (`H0`). |
| **T19** | `DONE` | `DONE` | DISABLED | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. | None (`H0`). |
| **T20** | `DONE` | `CANCELLED` | DISABLED | **FORBIDDEN** | Cancel-Done | None | Completed task cannot be cancelled in V1. Returns 409 Conflict. | None (`H0`). |
| **T21** | `CANCELLED` | `TODO` | DISABLED | **FORBIDDEN** | Restore | None | Terminal state. No transitions allowed. Returns 409 Conflict. | None (`H0`). |
| **T22** | `CANCELLED` | `IN_PROGRESS` | DISABLED | **FORBIDDEN** | Reopen-Cancel | None | Terminal state. No transitions allowed. Returns 409 Conflict. | None (`H0`). |
| **T23** | `CANCELLED` | `BLOCKED` | DISABLED | **FORBIDDEN** | Restore-Block | None | Terminal state. No transitions allowed. Returns 409 Conflict. | None (`H0`). |
| **T24** | `CANCELLED` | `DONE` | DISABLED | **FORBIDDEN** | Complete-Cancel | None | Terminal state. No transitions allowed. Returns 409 Conflict. | None (`H0`). |
| **T25** | `CANCELLED` | `CANCELLED` | DISABLED | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. | None (`H0`). |

---

### 3.2. Extended Field Dictionary (INV-03)

#### A. Approved Foundation Fields (D-03 Baseline — PR #31)
These 7 fields are permanently accepted and cannot be modified without reopening D-03:
- `_id`: ObjectId, immutable, system-generated primary key.
- `projectId`: ObjectId, immutable, required owning Project reference.
- `title`: String, mutable, required, original input preserved, contains at least one non-whitespace character outside set $W$, non-unique.
- `createdBy`: ObjectId, immutable, server-derived authenticated actor ID.
- `createdAt`: ISODate, immutable, server-derived timestamp.
- `updatedAt`: ISODate, mutable, server-derived timestamp (initially equal to `createdAt`).
- `version`: Number, mutable, optimistic concurrency counter (initial value `1`).

#### B. Proposed Extension Fields for Task V1 (Awaiting Human Approval)

| Field Name | Type | Storage | Nullable | Default | Mutability | Constraints & Validation Rules |
|---|---|---|---|---|---|---|
| `status` | String | `enum` | No | `"TODO"` | Mutable (Status API only) | Enum: `["TODO", "IN_PROGRESS", "BLOCKED", "DONE", "CANCELLED"]`. Governed by 25-cell matrix. |
| `description` | String | `string` | Yes | `null` | Mutable | Optional; max length 5,000 UTF-8 characters. Plain text or Markdown. |
| `priority` | String | `enum` | No | `"MEDIUM"` | Mutable | Enum: `["LOW", "MEDIUM", "HIGH", "URGENT"]`. |
| `assigneeId` | ObjectId | `ObjectId` | Yes | `null` | Mutable | Cardinality 0..1. Must reference active `User` who is an active member of `projectId`. Clearable via `null`. |
| `teamId` | ObjectId | `ObjectId` | Yes | `null` | Mutable | Cardinality 0..1. Must reference active `Team` belonging to `projectId`. Clearable via `null`. |
| `dueDate` | Date | `ISODate` | Yes | `null` | Mutable | Optional ISO-8601 string. If provided, must satisfy: `dueDate >= createdAt`. |
| `completedAt` | Date | `ISODate` | Yes | `null` | Server-derived | Automatically set to `now()` on transition T09 (`COMPLETE`). Cleared to `null` on T17 (`REOPEN`). |
| `tags` | Array | `[String]` | No | `[]` | Mutable | Array of strings; max 10 tags; each tag max 30 characters; trimmed, no empty strings. |

#### C. Contextual Derivation (Not Independent Storage in V1)
- `organizationId`: Contextually derived from owning `Project.organizationId` via trusted Project Service lookup. In compliance with D-03 delta approval, `organizationId` is **NOT** persisted as an independent column in the Task collection for V1.

---

### 3.3. Task V1 REST API Surface Specification (INV-04)

#### A. Route Architecture & Boundary (ADR-010)
- **External Public Boundary (Gateway / BFF):** `/api/v1/projects/:projectId/tasks...`
  - Gateway validates user session JWT, injects trusted headers, and proxies to internal Task Service.
- **Internal Service Boundary (Task Service):** `/tasks...`
  - Consumes trusted internal headers: `x-organization-id`, `x-project-id`, `x-actor-id`, `x-actor-role`.
  - Service rejects any direct request lacking trusted headers.

#### B. Endpoint Catalogue & Payload Contracts

##### 1. Create Task
- **Route:** `POST /api/v1/projects/:projectId/tasks`
- **Headers:** `Idempotency-Key` (Optional UUID v4 for `operationId`).
- **Request Body:**
  ```json
  {
    "title": "string (required, non-empty)",
    "description": "string (optional, max 5000)",
    "priority": "LOW | MEDIUM | HIGH | URGENT (optional, default MEDIUM)",
    "assigneeId": "ObjectId string (optional)",
    "teamId": "ObjectId string (optional)",
    "dueDate": "ISO-8601 string (optional)",
    "tags": ["string"] (optional, max 10)
  }
  ```
- **Response `201 Created`:** Full Task representation (`version: 1`, `status: "TODO"`).

##### 2. List Project Tasks (Paginated & Filtered)
- **Route:** `GET /api/v1/projects/:projectId/tasks`
- **Query Parameters:**
  - `status`: Filter by enum (single or comma-separated).
  - `priority`: Filter by priority enum.
  - `assigneeId`: Filter by assignee (`"null"` for unassigned).
  - `teamId`: Filter by team.
  - `search`: Case-insensitive substring search on `title`.
  - `page`: Integer $\ge 1$ (default: `1`).
  - `limit`: Integer between `1` and `100` (default: `20`).
  - `sort`: Default `-createdAt`. Allowed: `createdAt`, `-createdAt`, `updatedAt`, `-updatedAt`, `dueDate`, `-dueDate`, `priority`.
- **Response `200 OK`:**
  ```json
  {
    "success": true,
    "data": [ /* Array of Task projections */ ],
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
- **Response `200 OK`:** Single Task object. Returns `404 Not Found` if task does not exist or does not belong to `projectId`.

##### 4. Update Task Metadata
- **Route:** `PATCH /api/v1/projects/:projectId/tasks/:taskId`
- **Request Body:**
  ```json
  {
    "title": "string (optional)",
    "description": "string (optional)",
    "priority": "LOW | MEDIUM | HIGH | URGENT (optional)",
    "dueDate": "ISO-8601 string | null (optional)",
    "tags": ["string"] (optional),
    "expectedVersion": 2
  }
  ```
- **Response `200 OK`:** Updated Task object (`version: 3`).

##### 5. Execute State Transition
- **Route:** `PATCH /api/v1/projects/:projectId/tasks/:taskId/status`
- **Headers:** `Idempotency-Key` (Optional UUID v4 for `operationId`).
- **Request Body:**
  ```json
  {
    "targetStatus": "IN_PROGRESS | BLOCKED | DONE | CANCELLED (required)",
    "reason": "string (required min 5 chars for BLOCKED/CANCELLED/RESUME/REOPEN; optional for START/COMPLETE)",
    "expectedVersion": 2
  }
  ```
- **Response `200 OK`:** Updated Task object with new status and updated `version`. Returns `409 Conflict` if transition is forbidden or `expectedVersion` mismatches.

##### 6. Assign or Unassign Task
- **Route:** `PATCH /api/v1/projects/:projectId/tasks/:taskId/assignee`
- **Headers:** `Idempotency-Key` (Optional UUID v4).
- **Request Body:**
  ```json
  {
    "assigneeId": "ObjectId string | null (required; pass null to unassign)",
    "teamId": "ObjectId string | null (optional)",
    "expectedVersion": 2
  }
  ```
- **Response `200 OK`:** Updated Task object. Returns `422 Unprocessable Entity` if `assigneeId` is not an active member of `projectId`.

##### 7. Get Task Audit History Log
- **Route:** `GET /api/v1/projects/:projectId/tasks/:taskId/events`
- **Query Parameters:** `page` (default 1), `limit` (default 20, max 100).
- **Response `200 OK`:** Paginated list of `task_events` projections.

---

### 3.4. Role-Based Access Control (RBAC) Matrix (INV-05)

Role definitions conform strictly to `02_ACTORS_ROLES_AND_PERMISSIONS.md`:
- `ADMIN` (Project Admin): Full administrative control over the Project and all its tasks.
- `TEAM_LEADER` (Team Lead): Team-level management; can assign tasks and manage lifecycle for team members.
- `MEMBER` (Project Contributor): Standard contributor. Can create tasks, edit own/assigned tasks, and perform allowed lifecycle transitions on assigned work.

#### 4-Dimensional Authorization Matrix: Role $\times$ Action $\times$ Resource $\times$ Scope

| Action Code | Target Operation | Required Minimum Role | Additional Ownership / Scope Guard | Non-Member / Cross-Scope Outcome |
|---|---|---|---|---|
| `TASK_CREATE` | `POST .../tasks` | `MEMBER` | Must have active `ProjectMembership` in target `projectId`. | `404 Not Found` (Mask project existence) |
| `TASK_READ` | `GET .../tasks` (List/Detail/Events) | `MEMBER` | Active member of `projectId`. | `404 Not Found` |
| `TASK_EDIT_META` | `PATCH .../tasks/:taskId` | `MEMBER` | Must be either: (a) `ADMIN`, (b) `TEAM_LEADER`, (c) `assigneeId == actorId`, or (d) `createdBy == actorId`. | `404 Not Found` (or `403 Forbidden` if project member lacking ownership) |
| `TASK_ASSIGN` | `PATCH .../assignee` | `TEAM_LEADER` | Only `ADMIN` or `TEAM_LEADER` can assign/reassign. Plain `MEMBER` cannot reassign tasks. | `403 Forbidden` |
| `TASK_TRANSITION_WORK` | `START`, `BLOCK`, `RESUME`, `COMPLETE` | `MEMBER` | Must be assigned to task (`assigneeId == actorId`), or hold `TEAM_LEADER` / `ADMIN`. | `403 Forbidden` |
| `TASK_CANCEL` | `CANCEL` (T05, T10, T15) | `MEMBER` | Must be: `ADMIN`, `TEAM_LEADER`, or the original `createdBy` of the task. | `403 Forbidden` |
| `TASK_REOPEN` | `REOPEN` (T17) | `MEMBER` | Must be: `ADMIN`, `TEAM_LEADER`, or the original `createdBy` of the task. | `403 Forbidden` |

*Note on Team Scope:* When a task has `teamId` populated, members of that team inherit collaborative read and update rights under the supervision of their `TEAM_LEADER`. No comment action is scoped in Task V1.

---

### 3.5. Standardized Error Response Contract (INV-06)

All error responses strictly adhere to the following unified JSON schema:

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

#### Canonical HTTP Status & Error Code Mapping:
- **`400 Bad Request`**:
  - `TASK_VALIDATION_ERROR`: Field constraint violation (e.g., `description` > 5000 chars, `tags` > 10).
  - `MANDATORY_TRANSITION_REASON_MISSING`: State transition requires `reason` (min 5 chars).
  - `INVALID_DUE_DATE`: `dueDate` is prior to `createdAt`.
- **`401 Unauthorized`**:
  - `UNAUTHORIZED`: Missing, expired, or malformed JWT token.
- **`403 Forbidden`**:
  - `INSUFFICIENT_PROJECT_PERMISSIONS`: Authenticated project member lacks the required role for the action (e.g., Member attempting to reassign).
- **`404 Not Found`**:
  - `PROJECT_NOT_FOUND`: Target `projectId` does not exist or actor is not an active member.
  - `TASK_NOT_FOUND`: Target `taskId` does not exist in the specified `projectId`.
- **`409 Conflict`**:
  - `TASK_STATE_TRANSITION_CONFLICT`: Requested transition is forbidden by the 25-cell matrix.
  - `CONCURRENT_VERSION_CONFLICT`: Client `expectedVersion` does not match current database `version`.
- **`422 Unprocessable Entity`**:
  - `ASSIGNEE_NOT_PROJECT_MEMBER`: Assigned user does not hold an active membership in the project.
  - `TEAM_NOT_IN_PROJECT`: Assigned team does not belong to the project.
  - `IDEMPOTENCY_KEY_PAYLOAD_MISMATCH`: Replayed `operationId` with differing payload.

---

### 3.6. Audit History Event Schema & Privacy Projection (INV-06)

In strict accordance with D-03 PR #31 P3 approval, **whole-task snapshots (`previousState / newState`) are explicitly forbidden**. The history collection `task_events` captures only safe, discriminated allowlist metadata:

#### `task_events` Schema:
```typescript
interface TaskEventRecord {
  _id: ObjectId;                     // Unique event identifier
  taskId: ObjectId;                  // Target task
  projectId: ObjectId;               // Owning project
  eventType: TaskEventType;          // Event enum
  actorId: ObjectId;                 // Authenticated user initiating mutation
  timestamp: Date;                   // UTC server timestamp
  version: number;                   // Task version resulting from this mutation
  operationId?: string;              // Client-supplied idempotency key
  changedFields: string[];           // Allowlist of field names modified
  delta: TaskEventDelta;             // Discriminated payload (No whole-task snapshots)
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

### 3.7. Mutation Reliability, Idempotency & Uncertain Commit Model (INV-07)

Every mutation endpoint supports an optional `operationId` (via `Idempotency-Key` HTTP header) with a 24-hour deduplication window.

#### A. Three-Way Commit Outcome Handling
In distributed MongoDB transactions, a network drop or driver timeout during commit must not be blindly assumed to be a rollback:

1. **`CONFIRMED_SUCCESS`:** Both the Task document and the `task_events` record commit together within the MongoDB replica set transaction. Response: `200 OK` or `201 Created`.
2. **`CONFIRMED_REJECTED / ABORTED`:** Transaction confirms abort before write, or guard validation fails. State and version remain unchanged; no event is written (`H0`). Response: `400 / 403 / 404 / 409 / 422`.
3. **`UNCERTAIN`:** The client or driver experiences a network disconnect or timeout while awaiting transaction commit acknowledgment.
   - **Invariant:** The transaction may have committed successfully on the replica set primary. An exception alone does **NOT** prove rollback.
   - **Client Rule:** The client **MUST NOT** generate a new `operationId` and reissue the request. The client must either:
     (a) Re-send the request with the identical `operationId`, allowing the server's idempotent replay cache to return the committed result; or
     (b) Query the resource state via `GET /tasks/:taskId` to observe the persisted `version`.

#### B. Replay Resolution
- When an `operationId` is re-received with an identical payload within 24 hours: Task Service returns the previously committed response without incrementing `version` or writing duplicate history records (`H0`).
- If an `operationId` is re-received with a conflicting payload: Task Service returns `422 Unprocessable Entity` (`IDEMPOTENCY_KEY_PAYLOAD_MISMATCH`).

---

## 4. DATN-376 (D-13.3): Downstream Acceptance & Dependency Trace

### 4.1. Detailed 1-to-1 Traceability Matrix

This table maps every unresolved question from D-01, D-02, and D-03 directly to its proposed disposition, required authority, affected Jira issue, and automated test oracle:

| Question ID | Topic | Proposed Disposition | Required Authority | Affected Jira Issue | Test Oracle |
|---|---|---|---|---|---|
| **Q1 / D01-01** | Extended Field Boundary | Approved D-03 7 fields + 8 candidate extension fields in §3.2. | Product | DATN-97, D-05, D-08 | O1, O13, O14, O15 |
| **Q2 / D01-02** | Validation Rules | Server-derived timestamps; strict length bounds; original string preservation. | Architecture | DATN-97, D-08 | O1, O13, O14 |
| **Q3 / D01-03** | Lifecycle Enum | 5 states: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`. | Product | DATN-97, D-07 | O1, O2, O7 |
| **Q4 / D02-01** | Initial & Terminal States | Initial is `TODO`; Terminal is `CANCELLED` (no transitions out). | Product | DATN-97, D-07 | O1, O7 |
| **Q5 / D02-02** | 25 Transition Cells | 8 Candidate Permitted vs. 17 Candidate Forbidden cells in §3.1. | Product & Arch | DATN-97, D-07 | O2, O3, O4, O7, O8 |
| **Q6 / D01-04** | API Endpoint Surface | 7 REST endpoints in §3.3; Gateway vs. Internal separation. | Architecture | DATN-97, D-08 | O1, O2, O11, O12 |
| **Q7 / D01-05** | Role & Permissions | 4D RBAC matrix using `ADMIN`, `TEAM_LEADER`, `MEMBER` in §3.4. | Security & Arch | DATN-97, D-07, D-08 | O9, O12 |
| **Q8 / D02-10** | History Projection | Non-snapshot allowlist delta in §3.6; whole-task snapshot forbidden. | Security & Arch | DATN-97, D-07, D-08 | O2, O10 |
| **Q9 / D01-06** | Reliability & Idempotency | `operationId` replay and three-way commit handling in §3.7. | Architecture | DATN-97, D-07 | O10, O11 |

---

### 4.2. Downstream Executable Acceptance Oracles (O1–O15)

Downstream automated tests (unit, integration, and replica-set tests) must satisfy these 15 executable oracles:

1. **O1 (Creation Defaults & Version 1):** `POST /api/v1/projects/:projectId/tasks` returns `status: "TODO"`, `priority: "MEDIUM"`, `version: 1`, and `createdAt == updatedAt`.
2. **O2 (Allowed Transition START):** `PATCH .../status` with `targetStatus: "IN_PROGRESS"` from `"TODO"` succeeds, increments `version` to `2`, and appends a `TASK_STATUS_TRANSITIONED` event with `delta: { fromStatus: "TODO", toStatus: "IN_PROGRESS" }`.
3. **O3 (Forbidden Direct Complete):** `PATCH .../status` with `targetStatus: "DONE"` from `"TODO"` fails with `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`). Version and status remain unchanged.
4. **O4 (Forbidden Self-Transition):** `PATCH .../status` with identical status returns `409 Conflict`.
5. **O5 (Mandatory Reason on Blocking):** `PATCH .../status` to `"BLOCKED"` without `reason` or with `reason.length < 5` fails with `400 Bad Request` (`MANDATORY_TRANSITION_REASON_MISSING`).
6. **O6 (Mandatory Reason on Cancellation):** `PATCH .../status` to `"CANCELLED"` without `reason` fails with `400 Bad Request`.
7. **O7 (Terminal State Invariant):** Any status transition attempt from `"CANCELLED"` fails with `409 Conflict`.
8. **O8 (Reopen Transition & Timestamp Reset):** `PATCH .../status` from `"DONE"` to `"IN_PROGRESS"` succeeds with mandatory `reason`, resets `completedAt = null`, and increments `version`.
9. **O9 (Assignee Membership Validation):** Setting `assigneeId` to a user who is not an active member of `projectId` fails with `422 Unprocessable Entity` (`ASSIGNEE_NOT_PROJECT_MEMBER`).
10. **O10 (Atomic Transaction & Uncertainty Guarantee):**
    - A confirmed aborted transaction rolls back both Task and event log (`H0`).
    - An unacknowledged commit exception leaves status as `UNCERTAIN`; client re-query or replay with same `operationId` retrieves canonical state without duplicate version increment.
11. **O11 (Optimistic Concurrency Control):** Submitting `expectedVersion` differing from the current database version returns `409 Conflict` (`CONCURRENT_VERSION_CONFLICT`).
12. **O12 (Project Multi-Tenancy Masking):** Non-member querying `/api/v1/projects/:projectId/tasks` receives `404 Not Found`, masking the existence of the foreign project.
13. **O13 (Due Date Boundary):** Submitting `dueDate` prior to `createdAt` returns `400 Bad Request` (`INVALID_DUE_DATE`).
14. **O14 (Description Boundary):** Submitting `description` exceeding 5,000 characters returns `400 Bad Request` (`TASK_VALIDATION_ERROR`).
15. **O15 (Tag Constraint):** Submitting more than 10 tags returns `400 Bad Request`.

---

## 5. Review & Sign-Off Checklist for Lead

- [x] **Finding 1 Addressed:** Document framed strictly as `PROPOSED DISPOSITION`. Clear boundary between approved baseline and proposed items. Implementation gate marked BLOCKED.
- [x] **Finding 2 Addressed:** All 25 transition cells reaffirmed as `DISABLED (Enabled: NO)` in accepted baseline. Permitted transitions framed as proposed candidates. `completedAt` integrated into T09/T17.
- [x] **Finding 3 Addressed:** Extended fields partitioned from D-03 7 foundation fields. Added `teamId` and `completedAt`. `organizationId` reaffirmed as contextual derivation.
- [x] **Finding 4 Addressed:** Standardized status body, clear-assignment semantics, pagination defaults, unified `404 Not Found` for foreign projects, and ADR-010 Gateway/Service route separation.
- [x] **Finding 5 Addressed:** Standardized 4D RBAC matrix using active roles (`ADMIN`, `TEAM_LEADER`, `MEMBER`). Reassignment restricted to Lead/Admin. Comments excluded from V1.
- [x] **Finding 6 Addressed:** Whole-task snapshot strictly banned. Event schema restricted to allowlist `changedFields` and structured deltas.
- [x] **Finding 7 Addressed:** Formulated `operationId` replay model, 24-hour deduplication, and three-way commit outcome handling (`UNCERTAIN`).
- [x] **Finding 8 Addressed:** Detailed 1-to-1 traceability table mapping every Q/UNKNOWN item to proposed disposition, authority, Jira issue, and test oracle.
