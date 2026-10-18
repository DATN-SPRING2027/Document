# DATN-373 — D-13 Task V1 API, Lifecycle and Contract Decisions

- **Status:** PROPOSED & DISPOSITION CLOSURE (Awaiting Human Reviewer Approval).
- **Date:** 18/10/2026 (Asia/Bangkok).
- **Author:** Nguyen Hong Phuc (phuc2348hong@gmail.com).
- **Target Epic:** [DATN-75 Epic D — Task Management](https://trankimthang0207.atlassian.net/browse/DATN-75).
- **Parent Task:** [DATN-373](https://trankimthang0207.atlassian.net/browse/DATN-373) — `D-13 Close remaining Task V1 API and lifecycle decisions`.
- **Subtasks Covered:**
  - [DATN-374](https://trankimthang0207.atlassian.net/browse/DATN-374) — D-13.1 Inventory unresolved Task contract and lifecycle decisions
  - [DATN-375](https://trankimthang0207.atlassian.net/browse/DATN-375) — D-13.2 Obtain authority disposition for API and transition matrix
  - [DATN-376](https://trankimthang0207.atlassian.net/browse/DATN-376) — D-13.3 Publish downstream acceptance and dependency trace
- **Baseline Revisions:**
  - Task V1 contract approval record: [PR #30](20-task-v1-contract-approval-record.md)
  - Task V1 D-03 delta approval record: [PR #31](22-task-v1-d03-delta-approval-record.md)
  - Task V1 state machine contract: [DATN-94 / D-02](16-task-v1-state-machine-contract.md)
  - ADR-009 / ADR-010: [Task service architecture](../../research-tech/ADR-010-task-service-in-existing-repositories.md)
- **Scope Boundary:** Research, Contract Specification & Dependency Trace only. No backend/frontend code implementation, schema migration execution, or runtime changes are made in this document task. D-03 and D-04 remain completed within their accepted runtime-seam boundaries.

---

## 1. Executive Summary & Objective

The objective of **DATN-373 (D-13)** is to resolve the remaining `UNKNOWN` and conditionally approved decisions regarding the Task V1 API surface, extended field dictionary, state machine lifecycle transitions (the 25 cells of D-02), authorization boundary, and error semantics before downstream backend implementation under **DATN-97** and **D-07/D-08** proceeds.

The earlier approval records ([DATN-95 / PR #30](20-task-v1-contract-approval-record.md) and [PR #31](22-task-v1-d03-delta-approval-record.md)) established:
1. Recommendation-level decisions (single owning Project, contextual Organization, 0..1 Team/Assignee, non-unique Title, append-only history, atomic mutation + history persistence).
2. The foundational 7 persisted fields of D-03 (`_id`, `projectId`, `title`, `createdBy`, `createdAt`, `updatedAt`, `version`) strictly for the private data-foundation slice.

However, all 25 transition cells, extended editable fields, API endpoint definitions, actor permission matrices, and executable test oracles remained marked as **UNKNOWN**. This document systematically inventories all unresolved items (DATN-374), delivers recommended authority dispositions (DATN-375), and establishes downstream acceptance criteria and dependency blocking traces (DATN-376).

---

## 2. DATN-374 (D-13.1): Inventory of Unresolved Decisions

This section categorizes every unresolved item identified from previous records by its **Authority Domain** (Product, Architecture, Security), **Subsystem Boundary**, and **Downstream Blocking Impact**.

### 2.1. Decision Inventory Matrix

| ID | Unresolved Decision Area | Source Reference | Authority Domain | Subsystem Boundary | Downstream Blocking Impact |
|---|---|---|---|---|---|
| **INV-01** | **Task State Machine 5-State Catalogue & Initial State** | `20-task-v1-contract-approval-record.md` §34, `16-task-v1-state-machine-contract.md` §2 | Product | Task Lifecycle | Blocks D-07, DATN-97 |
| **INV-02** | **25-Cell State Transition Matrix (T01–T25)** | `16-task-v1-state-machine-contract.md` §3 | Product & Arch | Task Lifecycle | Blocks D-07, DATN-97, D-08 |
| **INV-03** | **Extended Field Dictionary (Beyond D-03's 7 fields)** | `20-task-v1-contract-approval-record.md` §17, `21-task-v1-d03-contract-delta.md` §5 | Product | Task Core Schema | Blocks D-05, D-08, DATN-97 |
| **INV-04** | **Task V1 REST API Endpoint Surface** | `20-task-v1-contract-approval-record.md` §16, `ADR-010` | Architecture | Task API Router | Blocks DATN-97, FE Integration |
| **INV-05** | **Actor, Role & Permission Matrix (RBAC / Context)** | `20-task-v1-contract-approval-record.md` §16, §32 | Security & Arch | Authorization Guard | Blocks DATN-97, D-07, D-08 |
| **INV-06** | **Standardized API Error Codes & Idempotency** | `20-task-v1-contract-approval-record.md` §20, §39 | Architecture | API Error Layer | Blocks DATN-97, Test Suite |
| **INV-07** | **Audit Log & History Event Boundary (`task_events`)** | `20-task-v1-contract-approval-record.md` §23, §24 | Architecture & Sec | History Event Store | Blocks DATN-97, D-07, D-08 |
| **INV-08** | **Work Note / Handover & Deletion Policy Boundary** | `20-task-v1-contract-approval-record.md` §19, §26 | Product | Integration Seam | Confirmed Excluded from V1 |

---

## 3. DATN-375 (D-13.2): Recommended Authority Disposition

### 3.1. Task Lifecycle State Machine Disposition (INV-01, INV-02)

#### A. Approved 5-State Catalogue
The canonical lifecycle consists of exactly 5 states:
1. `TODO`: Initial state upon creation. Task is unstarted.
2. `IN_PROGRESS`: Actively being worked on by an assignee or team member.
3. `BLOCKED`: Work halted due to an external impediment or dependency. Requires a mandatory explanatory reason.
4. `DONE`: Work delivered and completed. Can be reopened to `IN_PROGRESS` if review fails.
5. `CANCELLED`: Terminal state for abandoned/discarded tasks. Cannot be transitioned out in V1.

#### B. The 25-Cell State Transition Matrix Evaluation
Cartesian product $5 \times 5 = 25$ cells:
- **PERMITTED (8 edges):** Valid business state transitions.
- **FORBIDDEN (17 edges):** Invalid skips, backward resets, self-loops, or transitions from terminal `CANCELLED`. Return `409 Conflict` (or `400 Bad Request` if payload invalid).

| Edge | Source State | Target State | Disposition | Command Label | Required Actor Role | Guard Conditions & Audit Reason |
|---|---|---|---|---|---|---|
| **T01** | `TODO` | `TODO` | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. |
| **T02** | `TODO` | `IN_PROGRESS` | **PERMITTED** | `START` | Assignee or Project Member | Assignee assigned; optional start comment. |
| **T03** | `TODO` | `BLOCKED` | **FORBIDDEN** | Direct-Block | None | Cannot block unstarted work. Must `START` first. |
| **T04** | `TODO` | `DONE` | **FORBIDDEN** | Direct-Complete | None | Cannot complete unstarted work. Must `START` first. |
| **T05** | `TODO` | `CANCELLED` | **PERMITTED** | `CANCEL` | Project Admin or Task Creator | Mandatory `cancellationReason` (min 5 chars). |
| **T06** | `IN_PROGRESS` | `TODO` | **FORBIDDEN** | Reset | None | Cannot unstart work already in progress. |
| **T07** | `IN_PROGRESS` | `IN_PROGRESS` | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. |
| **T08** | `IN_PROGRESS` | `BLOCKED` | **PERMITTED** | `BLOCK` | Assignee or Project Member | Mandatory `blockReason` (min 5 chars). |
| **T09** | `IN_PROGRESS` | `DONE` | **PERMITTED** | `COMPLETE` | Assignee or Project Admin | Optional completion note; records `completedAt`. |
| **T10** | `IN_PROGRESS` | `CANCELLED` | **PERMITTED** | `CANCEL` | Project Admin or Task Creator | Mandatory `cancellationReason` (min 5 chars). |
| **T11** | `BLOCKED` | `TODO` | **FORBIDDEN** | Reset | None | Cannot reset blocked work to unstarted. |
| **T12** | `BLOCKED` | `IN_PROGRESS` | **PERMITTED** | `RESUME` | Assignee or Project Member | Mandatory `resumeReason` (min 5 chars). |
| **T13** | `BLOCKED` | `BLOCKED` | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. |
| **T14** | `BLOCKED` | `DONE` | **FORBIDDEN** | Direct-Complete | None | Cannot complete while blocked. Must `RESUME` first. |
| **T15** | `BLOCKED` | `CANCELLED` | **PERMITTED** | `CANCEL` | Project Admin or Task Creator | Mandatory `cancellationReason` (min 5 chars). |
| **T16** | `DONE` | `TODO` | **FORBIDDEN** | Reset | None | Cannot uncomplete to unstarted. |
| **T17** | `DONE` | `IN_PROGRESS` | **PERMITTED** | `REOPEN` | Project Admin or Task Creator | Mandatory `reopenReason` (min 5 chars). |
| **T18** | `DONE` | `BLOCKED` | **FORBIDDEN** | Direct-Block | None | Cannot block completed work. Reopen first. |
| **T19** | `DONE` | `DONE` | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. |
| **T20** | `DONE` | `CANCELLED` | **FORBIDDEN** | Cancel Done | None | Completed work cannot be cancelled in V1. |
| **T21** | `CANCELLED` | `TODO` | **FORBIDDEN** | Restore | None | Terminal state. No transitions allowed. |
| **T22** | `CANCELLED` | `IN_PROGRESS` | **FORBIDDEN** | Reopen Cancel | None | Terminal state. No transitions allowed. |
| **T23** | `CANCELLED` | `BLOCKED` | **FORBIDDEN** | Restore Block | None | Terminal state. No transitions allowed. |
| **T24** | `CANCELLED` | `DONE` | **FORBIDDEN** | Complete Cancel | None | Terminal state. No transitions allowed. |
| **T25** | `CANCELLED` | `CANCELLED` | **FORBIDDEN** | N/A | None | Self-transition rejected. Returns 409 Conflict. |

---

### 3.2. Extended Field Dictionary for Task V1 (INV-03)

In addition to D-03's 7 foundation fields (`_id`, `projectId`, `title`, `createdBy`, `createdAt`, `updatedAt`, `version`), the following extension fields are approved for Task V1:

| Field Name | Type | Storage Type | Nullable | Default Value | Mutability | Validation Rules |
|---|---|---|---|---|---|---|
| `status` | String | `enum` | No | `"TODO"` | Mutable via status API | Must be one of `["TODO", "IN_PROGRESS", "BLOCKED", "DONE", "CANCELLED"]`. |
| `description` | String | `string` | Yes | `null` | Mutable | Optional; max length 5,000 characters; UTF-8 encoded. |
| `priority` | String | `enum` | No | `"MEDIUM"` | Mutable | Must be one of `["LOW", "MEDIUM", "HIGH", "URGENT"]`. |
| `assigneeId` | ObjectId | `ObjectId` | Yes | `null` | Mutable | Must reference an active `User` who is an active member of `projectId`. Cardinality 0..1. |
| `dueDate` | Date | `ISODate` | Yes | `null` | Mutable | Optional; must be a valid ISO-8601 Date string. If set, cannot be earlier than `createdAt`. |
| `tags` | Array | `[String]` | No | `[]` | Mutable | Array of strings; max 10 tags; each tag max 30 characters; trimmed, no empty strings. |
| `organizationId` | ObjectId | `ObjectId` | No | Derived | Immutable | Derived contextually from owning `Project.organizationId` at creation. |

---

### 3.3. Task V1 REST API Surface Specification (INV-04)

All Task endpoints are scoped strictly under `/api/v1/projects/:projectId/tasks` to guarantee multi-tenancy isolation.

| Method | Endpoint | Operation | Request Body | Response Status | Authorization Required |
|---|---|---|---|---|---|
| `POST` | `/api/v1/projects/:projectId/tasks` | Create Task | `{ title, description?, priority?, assigneeId?, dueDate?, tags? }` | `201 Created` | Project Member or Admin |
| `GET` | `/api/v1/projects/:projectId/tasks` | List Tasks (paginated) | Query: `?status=&priority=&assigneeId=&search=&page=&limit=` | `200 OK` | Project Member or Admin |
| `GET` | `/api/v1/projects/:projectId/tasks/:taskId` | Get Task Detail | None | `200 OK` | Project Member or Admin |
| `PATCH` | `/api/v1/projects/:projectId/tasks/:taskId` | Update Task Core Info | `{ title?, description?, priority?, dueDate?, tags?, expectedVersion }` | `200 OK` | Task Creator, Assignee, or Admin |
| `PATCH` | `/api/v1/projects/:projectId/tasks/:taskId/status` | Execute State Transition | `{ targetStatus, reason?, expectedVersion }` | `200 OK` | Enforced by 25-cell Matrix |
| `PATCH` | `/api/v1/projects/:projectId/tasks/:taskId/assignee` | Assign / Reassign Task | `{ assigneeId, expectedVersion }` | `200 OK` | Project Member or Admin |
| `GET` | `/api/v1/projects/:projectId/tasks/:taskId/events` | Get Task History Log | Query: `?page=&limit=` | `200 OK` | Project Member or Admin |

---

### 3.4. Actor, Role & Permission Boundary (INV-05)

Multi-tenancy isolation is enforced at the project level:
1. **Context Verification:** Actor must possess an active `ProjectMembership` with `status: "ACTIVE"` in the target `projectId`.
2. **Role Capabilities:**
   - **Project Admin:** Full access to create, edit, assign, cancel, reopen, and complete any task.
   - **Task Assignee:** Can edit metadata, execute allowed status transitions (`START`, `BLOCK`, `RESUME`, `COMPLETE`), and update progress.
   - **Task Creator:** Can edit metadata and request cancellation or reopening.
   - **Project Member:** Can read all tasks, create tasks, and comment; cannot cancel tasks owned by others unless assigned.
   - **Cross-Project Invariant:** Actors cannot view, query, or mutate tasks belonging to projects where they hold no active membership (returns `404 Not Found` or `403 Forbidden`).

---

### 3.5. Standardized API Error Response Contract (INV-06)

Error payloads conform to the existing backend standard:

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

#### Canonical Error Code Mapping:
- `400 Bad Request`: `TASK_VALIDATION_ERROR`, `INVALID_TITLE_FORMAT`, `INVALID_DUE_DATE`
- `401 Unauthorized`: `UNAUTHORIZED` (Missing or invalid JWT)
- `403 Forbidden`: `FORBIDDEN_PROJECT_ACCESS`, `INSUFFICIENT_TASK_PERMISSIONS`
- `404 Not Found`: `TASK_NOT_FOUND`, `PROJECT_NOT_FOUND`
- `409 Conflict`: `TASK_STATE_TRANSITION_CONFLICT`, `CONCURRENT_VERSION_CONFLICT`
- `422 Unprocessable Entity`: `ASSIGNEE_NOT_PROJECT_MEMBER`

---

### 3.6. Audit History & Event Boundary (INV-07)

Every mutation to a Task must atomically commit a corresponding record into `task_events` within the same MongoDB transaction:
- **Event Types:** `TASK_CREATED`, `TASK_UPDATED`, `TASK_STATUS_CHANGED`, `TASK_ASSIGNED`.
- **Payload Schema:**
  ```typescript
  {
    _id: ObjectId;
    taskId: ObjectId;
    projectId: ObjectId;
    eventType: string;
    actorId: ObjectId;
    previousState: Record<string, unknown>;
    newState: Record<string, unknown>;
    reason?: string;
    timestamp: Date;
    version: number;
  }
  ```

---

## 4. DATN-376 (D-13.3): Downstream Acceptance & Dependency Trace

### 4.1. Traceability & Blocking Register

This table explicitly traces how decisions in this document govern and unblock downstream tasks under Epic DATN-75:

| Downstream Task ID | Task Summary | Governing Section in this Document | Blocking Status |
|---|---|---|---|
| **DATN-97** | Implement Task V1 Core BE API & Services | §3.2 (Fields), §3.3 (Endpoints), §3.4 (Auth), §3.5 (Errors) | **BLOCKED** until this document is approved & merged. |
| **D-05** | Task Query & Index Workload Optimization | §3.2 (Fields: `projectId`, `status`, `assigneeId`, `dueDate`) | **BLOCKED** until fields & query patterns are approved. |
| **D-07** | Task Status & Lifecycle Execution Engine | §3.1 (25-Cell State Matrix, Transition Guards & Reasons) | **BLOCKED** until 25-cell matrix is approved. |
| **D-08** | Task Mutation & Assignment Service | §3.2 (Fields), §3.4 (Permissions), §3.6 (Event Logging) | **BLOCKED** until mutation boundaries are approved. |

### 4.2. Downstream Executable Acceptance Oracles (O1–O15)

Downstream backend implementations (DATN-97, D-05, D-07, D-08) must satisfy these automated test oracles:

1. **O1 (Default Initial State):** `POST /api/v1/projects/:projectId/tasks` returns `status: "TODO"`, `version: 1`.
2. **O2 (Allowed Transition START):** `PATCH .../status` with `targetStatus: "IN_PROGRESS"` from `"TODO"` succeeds, increments `version` to `2`, commits `TASK_STATUS_CHANGED` event.
3. **O3 (Forbidden Direct Complete):** `PATCH .../status` with `targetStatus: "DONE"` from `"TODO"` fails with `409 Conflict` (`TASK_STATE_TRANSITION_CONFLICT`).
4. **O4 (Forbidden Self-Transition):** `PATCH .../status` with same status returns `409 Conflict`.
5. **O5 (Mandatory Reason for Block):** `PATCH .../status` to `"BLOCKED"` without `reason` fails with `400 Bad Request`.
6. **O6 (Mandatory Reason for Cancel):** `PATCH .../status` to `"CANCELLED"` requires `cancellationReason` (min 5 chars).
7. **O7 (Terminal State Invariant):** Any status transition attempt from `"CANCELLED"` fails with `409 Conflict`.
8. **O8 (Reopen Transition):** `PATCH .../status` from `"DONE"` to `"IN_PROGRESS"` succeeds with mandatory `reopenReason`.
9. **O9 (Assignee Membership Validation):** Assigning an `assigneeId` that is not an active member of `projectId` fails with `422 Unprocessable Entity`.
10. **O10 (Atomic Event Commit):** If writing to `task_events` fails, the task mutation is rolled back; state remains unchanged.
11. **O11 (Optimistic Concurrency Control):** Mismatched `expectedVersion` returns `409 Conflict` (`CONCURRENT_VERSION_CONFLICT`).
12. **O12 (Project Isolation):** Non-member querying `/api/v1/projects/:projectId/tasks` receives `403 Forbidden` or `404 Not Found`.
13. **O13 (Due Date Boundary):** `dueDate` prior to creation returns `400 Bad Request`.
14. **O14 (Description Boundary):** `description` exceeding 5,000 characters returns `400 Bad Request`.
15. **O15 (Tag Constraint):** More than 10 tags returns `400 Bad Request`.

---

## 5. Reviewer Checklist & Verification

To verify that DATN-373 and its subtasks are complete and ready for sign-off:

- [x] **DATN-374:** Full inventory of all unresolved UNKNOWN items categorized with authority, subsystem, and blocking impact.
- [x] **DATN-375:** Deterministic disposition for all 25 state machine cells, extended fields, REST endpoints, RBAC, and error codes.
- [x] **DATN-376:** Explicit traceability matrix mapping downstream tasks (DATN-97, D-05, D-07, D-08) and 15 executable test oracles.
- [x] **Scope Integrity:** D-03 7 foundation fields and D-04 runtime seam remain respected and untouched. No code or migration added.
