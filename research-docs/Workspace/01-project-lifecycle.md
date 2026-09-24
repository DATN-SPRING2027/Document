# [RESEARCH] Workspace - Project Lifecycle

Status: Research only. No implementation was performed.

## Evidence classification

- `[FACT]`: directly verified in source.
- `[IMPLEMENTED]`: executable behavior exists, not only a schema or design.
- `[DESIGN]`: described by product/architecture/specification documents.
- `[PARTIAL]`: some supporting structure exists, but the business capability is incomplete.
- `[GAP]`: documented requirement is not implemented in the current source.
- `[INFERENCE]`: conclusion synthesized from multiple sources.
- `[UNKNOWN]`: evidence is insufficient.
- `[DECISION REQUIRED]`: a human/product/architecture decision is needed.

## 1. Executive Summary

`[DESIGN]` A Project is the primary software-workspace boundary inside an Organization. It groups teams, project members, work notes, Jira context, documents, knowledge and later handover activity.

`[FACT]` The backend contains a Mongoose `projects` schema with `organizationId`, `name`, `code`, `description`, `status`, and `createdBy`. The persistence definition declares a unique `(organizationId, code)` index.

`[PARTIAL]` The current repository has the Project data model and persistence scaffold, but no Project HTTP API, application business logic, authorization guard, DTO layer, frontend Project management flow, or Project E2E flow. The current IAM controller exposes only health behavior.

`[DECISION REQUIRED]` The repository does not establish the complete Project lifecycle policy, including who may create/read/update/archive/restore a Project, what archive does to Teams and Memberships, and whether restore is part of MVP.

## 2. Business Goal

The Project boundary should provide a safe workspace in which:

1. an Organization can contain one or more software Projects;
2. Project Membership controls which users can enter the Project scope;
3. Teams and Team Membership remain inside the Project;
4. Work Notes, Jira data, documents, knowledge and handover data can be scoped to the Project;
5. Project mutations remain auditable and do not destroy historical references.

`[DESIGN]` The MVP product scope focuses on one software project with multiple teams. This is a product scope constraint, not evidence that only one Project entity may exist in the data model.

## 3. Scope

Included in this research:

- Project purpose and ownership boundary;
- Organization relationship;
- create, list, detail, update, search, filter, pagination and sort requirements;
- archive/restore and soft-delete semantics;
- Project code uniqueness and indexes;
- Project access and authorization dependencies;
- audit dependency;
- current backend, frontend, BFF and test evidence;
- FE/BE/API gaps and decisions required before implementation.

Excluded:

- implementing Project APIs or UI;
- changing MongoDB topology, ADRs, specs or decisions;
- deciding unresolved product policy;
- implementing Team, Membership, Jira, Knowledge or SAG behavior.

## 4. Verified Requirements

| Requirement | Evidence | Classification | Notes |
|---|---|---|---|
| Project is a software-workspace boundary | `product_docs/research-docs/01_MVP_SCOPE.md`; `docs/product/domain-map.md` | `[DESIGN]` | Project is part of the Project/Team Management domain. |
| Project belongs to an Organization | `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts`; product authorization docs | `[FACT]` / `[DESIGN]` | Source requires `organizationId` on Project. |
| Project has name, code and optional description | IAM `projects` schema | `[FACT]` | These are source-supported fields; no additional fields are inferred. |
| Project has lifecycle status `ACTIVE` or `ARCHIVED` in current schema | IAM `projects` schema | `[FACT]` | This is a schema enum, not proof of working transitions. |
| Project records creator | IAM `projects` schema | `[FACT]` | `createdBy` exists. Its business ownership meaning is not fully defined. |
| Project code is unique inside an Organization | IAM `persistence.ts` | `[FACT]` / `[DESIGN]` | Current index is unique on `(organizationId, code)`. |
| Create Project is permission controlled | `02_ACTORS_ROLES_AND_PERMISSIONS.md`; `organization_capability_grants` schema | `[DESIGN]` / `[PARTIAL]` | `project.create` is an explicit organization-level capability grant for a Team Leader. No evaluator exists. |
| Admin can create/manage Projects within organization policy | `02_ACTORS_ROLES_AND_PERMISSIONS.md` | `[DESIGN]` | The exact policy boundary is not implemented. |
| Team Leader may create a new Project only with `project.create` | Actors/roles document; SPEC-002 | `[DESIGN]` | Leadership alone must not imply the capability. |
| Project list/detail/update/search/filter/pagination/sort are required by leader breakdown | `Danh Chia Task.docx`, Project section | `[DESIGN]` | No implemented API was found. |
| Project access is limited by active membership and ACL/policy | `02_ACTORS_ROLES_AND_PERMISSIONS.md`; `docs/architecture/target-state.md` | `[DESIGN]` | Backend enforcement is required. |
| Archive/soft delete is preferred over hard delete | `Danh Chia Task.docx`; product research docs | `[DESIGN]` | Exact cascade/reference semantics are not defined. |
| Audit is required for Project creation, update and archive | `02_ACTORS_ROLES_AND_PERMISSIONS.md`; leader breakdown | `[DESIGN]` | Current audit service is infrastructure scaffolding only. |
| Current FE has a Project selection state | `DATN-FE/src/stores/client-state.ts` | `[IMPLEMENTED]` | `activeProjectId` and setter exist. This is not a Project management flow. |
| Current FE has Project management pages/hooks | `DATN-FE/src/app`, `DATN-FE/src/lib/queries` | `[GAP]` | No dedicated Project CRUD/list/detail hook or page was found. |

## 5. Business Rules

### Verified/design rules

1. `[DESIGN]` A Project must be associated with an Organization.
2. `[DESIGN]` Project code must be unique within that Organization.
3. `[DESIGN]` A user outside the authorized Project scope must not access Project resources.
4. `[DESIGN]` Backend authorization is the security boundary; frontend checks are UX only.
5. `[DESIGN]` Team Leaders need an explicit organization-level `project.create` grant to create a new Project.
6. `[DESIGN]` Project and Membership data should be archived/disabled rather than hard-deleted when historical references must remain.
7. `[DESIGN]` Important Project mutations must create audit records.

### Not established by current evidence

- Whether a Project must have exactly one owner, one leader or multiple owners.
- Whether `createdBy` is merely provenance or establishes ownership.
- Whether Project creation automatically creates a Project Membership for the creator.
- Whether Project creation automatically creates an initial Team.
- Whether Admin access to a Project's confidential content is automatic; product docs indicate it is not automatic.
- Whether archived Projects remain readable, searchable or retrievable.
- Whether archive cascades to Teams, Memberships, Jira connections, documents, knowledge or handovers.

## 6. Project Lifecycle

The following is the lifecycle evidenced by the current schema plus documented direction. It is not a final implementation contract.

| State/action | Evidence | Status | Consequence/unknown |
|---|---|---|---|
| Create | `projects` schema and leader breakdown | `[DESIGN]` / `[GAP]` | Must validate Organization, code uniqueness and `project.create`/Admin policy. |
| `ACTIVE` | Schema enum | `[FACT]` | Current code does not implement transition logic. |
| Update | Leader Project requirements | `[DESIGN]` / `[GAP]` | Fields and allowed changes are not specified. |
| Archive | Schema enum and leader breakdown | `[DESIGN]` / `[GAP]` | Must preserve references; impact on child resources is unknown. |
| Restore | Leader says “if needed”; no confirmed product rule | `[UNKNOWN]` / `[DECISION REQUIRED]` | Do not assume restore is MVP. |
| Hard delete | Leader/product guidance prefers archive | `[DESIGN]` | Whether any exceptional hard delete exists is unknown. |

Conceptual lifecycle:

```text
Create → ACTIVE → Update* → ARCHIVED → Restore? → ACTIVE
```

The `Restore?` transition is intentionally unresolved.

## 7. Entity & Relationship

```text
Organization
    └── Project
          ├── Project Membership → User
          ├── Team
          │     └── Team Membership → User
          ├── Work Notes / Jira / Documents
          └── Knowledge / Handover scope
```

`[FACT]` Source-supported Project fields:

- `organizationId`;
- `name`;
- `code`;
- `description`;
- `status`;
- `createdBy`;
- timestamps supplied by Mongoose.

`[INFERENCE]` Project is the parent scope for Team and Membership because the source stores `projectId` on Teams, Project Memberships and Team Memberships, and product documents describe Organization → Project → Team.

`[UNKNOWN]` The source does not define a direct `ownerId`, `leaderId` or Project policy entity. Role assignments contain optional `projectId`, but that does not by itself prove a Project ownership rule.

## 8. Backend Current State

| Area | Source | Status | Evidence |
|---|---|---|---|
| Project schema | `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts` | `[PARTIAL]` | Mongoose schema exists. |
| Project indexes | `DATN-BE/src/services/iam/infrastructure/persistence.ts` | `[PARTIAL]` | Unique `(organizationId, code)` declaration exists in source; runtime index creation and duplicate-write behavior are not verified. |
| Project repository | `DATN-BE/src/services/iam` | `[GAP]` | No Project repository/application data access flow found. |
| Project DTO/validation | `DATN-BE/src/services/iam` | `[GAP]` | No Project DTO/controller contract found. |
| Project HTTP API | IAM controller | `[GAP]` | Controller exposes only `GET health` and `iam.health`. |
| Project business logic | IAM application service | `[GAP]` | Service returns health response only. |
| Authorization | IAM source and architecture gaps | `[GAP]` | No executable Project guard/evaluator was found. |
| Audit | IAM audit service/schema | `[PARTIAL]` | Infrastructure can write audit records, but Project mutation wiring is absent. |
| Tests | backend test inventory | `[GAP]` | Existing tests cover health/config/contracts, not Project lifecycle. |

## 9. Frontend Current State

| Area | Source | Status | Evidence |
|---|---|---|---|
| Project selection | `DATN-FE/src/stores/client-state.ts` | `[IMPLEMENTED]` | Client-only `activeProjectId` state exists. |
| Project pages/routes | `DATN-FE/src/app` | `[GAP]` | No dedicated Project list/create/detail/edit/archive route was found. |
| Project hooks | `DATN-FE/src/lib/queries` | `[GAP]` | No Project CRUD/query hook was found. |
| Project forms/table | generic dashboard/table components | `[PARTIAL]` | Generic/template UI exists; it is not evidence of Project management. |
| Loading/error/empty states | generic components/API client | `[PARTIAL]` | Generic primitives exist; no Project-specific behavior exists. |
| Permission-aware Project UI | FE source | `[GAP]` | No verified Project permission guard was found. |
| Project tests | FE tests | `[GAP]` | Store/API helper tests exist, not Project flow tests. |

`activeProjectId` currently indicates a client-side selection concept. Its source usage does not establish persistence, server validation, URL synchronization or an active Project authorization context.

`[PARTIAL]` Generic API/query mutation scaffolding only: `DATN-FE/src/lib/queries/backend.ts` provides a generic mutation wrapper, and `DATN-FE/src/lib/queries/backend.spec.tsx` uses a mocked `/projects` mutation fixture. This does not prove a working Project endpoint, Project hook, Project page or Workspace business flow.

## 10. API / Contract Findings

| Business action | Documented target | Current source | Status |
|---|---|---|---|
| List Projects | Product/API inventory describes `/api/v1/projects/*` surface | No backend Project route | `[DESIGN]` / `[GAP]` |
| Create Project | Leader breakdown and IAM contract direction | No backend route | `[DESIGN]` / `[GAP]` |
| Detail/update/archive | Leader breakdown | No backend route | `[DESIGN]` / `[GAP]` |
| Browser access | `/api/backend/*` → backend `/api/v1/*` through BFF | BFF catch-all exists | `[PARTIAL]` |
| Pagination/filter/sort | Leader says contract must be standardized | No Project DTO/response contract | `[DESIGN]` / `[UNKNOWN]` |
| Error behavior | Architecture/spec references 401/403/409/422 | No Project endpoint behavior | `[DESIGN]` / `[UNKNOWN]` |

The exact Project endpoint paths, request DTOs, response envelope, pagination fields, filtering syntax and error payload are not proven by an implemented Project API.

## 11. Data / Index Findings

### Verified source model

- `projects.organizationId` is required.
- `projects.code` is required and normalized uppercase/trimmed by the schema.
- Project status is required and limited to `ACTIVE`/`ARCHIVED`.
- `createdBy` is required.
- A unique index is declared on `(organizationId, code)`.

### Findings requiring care

- `[PARTIAL]` Declaring an index in `persistence.ts` is not proof that the running environment has created it; `MONGODB_AUTO_INDEX` is configurable and defaults to false in current validation.
- `[ACCEPTED DECISION]` MVP operational persistence uses MongoDB 7.0 with shared `continuum_db` under DEC-011/ADR-002. `[DOCUMENTATION SYNC NEEDED]` Current source persistence definitions and historical inventories still contain service-specific names such as `continuum_iam`; this is a documentation/configuration alignment issue, not an open architecture decision.
- `[UNKNOWN]` No Project-specific soft-delete metadata beyond `status` is defined.
- `[UNKNOWN]` No archive reason, archivedBy, archivedAt, version or optimistic-concurrency behavior is defined in the Project schema.

## 12. Authorization Dependencies

`[DESIGN]` Project access depends on:

1. authenticated user/session;
2. Organization context;
3. active organization/project membership;
4. persistent role and scoped capability;
5. Project policy and resource/source ACL where applicable;
6. explicit deny precedence.

`[DESIGN]` The minimum relevant capabilities include `project.create`, `project.read` and `project.manage`. The exact mapping for read/update/archive is not fully approved in source.

`[GAP]` No backend Project authorization evaluator or guard is currently implemented.

## 13. Audit Dependencies

`[DESIGN]` The following Project events require audit coverage:

- Project creation;
- Project update;
- Project archive/restore if restore exists;
- use, grant or revoke of `project.create`;
- sensitive Project access where policy requires it.

`[PARTIAL]` IAM audit schema/service scaffolding exists. `[GAP]` No Project mutation exists to prove event wiring, actor/scope capture, idempotency or audit visibility.

## 14. Requirement → Evidence → Implementation → Gap

| Requirement | Evidence | Current implementation | Gap |
|---|---|---|---|
| Project belongs to Organization | Product docs; Project schema | `organizationId` field exists | No runtime scope validation |
| Project code unique per Organization | Persistence index | Unique index declaration exists | No API conflict behavior or test |
| Authorized Project creation | Actors/permissions docs; capability schema | Grant schema exists | No evaluator, guard or create service |
| Project list/detail | Leader/API docs | No endpoint | Entire business capability missing |
| Project update | Leader docs | No endpoint | Allowed fields and audit missing |
| Project archive | Leader docs; status enum | `ARCHIVED` enum exists | Transition logic and cascade policy missing |
| Restore if needed | Leader wording “if needed” | No evidence | Product decision required |
| Project access denial | Authorization docs | No executable guard | Cross-scope security behavior missing |
| FE Project management | Leader docs | No dedicated UI/hooks | Full FE flow missing |
| Audit Project mutation | Leader/docs audit service | Audit infrastructure scaffold | No Project event producer/wiring |
| Project E2E | Leader acceptance flow | No Project E2E | Test scenario and fixtures missing |

## 15. FE / BE Mismatch

1. `[GAP]` FE has no Project endpoint usage while backend has no Project endpoint.
2. `[PARTIAL]` FE `activeProjectId` represents client selection only; backend has no verified active-project context contract.
3. `[DESIGN]` BFF maps browser requests to `/api/v1/*`, but no Project route is exposed through the backend.
4. `[UNKNOWN]` Request/response models for Project are not shared between FE and BE.
5. `[UNKNOWN]` Error, pagination, filter and sort conventions are not proven for Project.

## 16. UNKNOWN

- Is Project creation organization-wide, Admin-only, or delegated to Team Leaders with `project.create`?
- Is a Project creator automatically a member, leader or owner?
- Is there one owner or multiple responsibility owners?
- Which Project fields are mutable after creation?
- Is Project code immutable after creation?
- Is restore in MVP?
- What remains readable after archive?
- Do Teams archive automatically with the Project?
- Do Project Memberships become suspended/removed on archive?
- Are Jira connections, documents, knowledge and handover packages disabled, hidden or retained after archive?
- What are the exact list/detail/error/pagination contracts?

## 17. DECISION REQUIRED

1. Approve the Project authorization matrix for create/read/update/archive.
2. Approve Project bootstrap behavior and initial membership/leader assignment.
3. Approve archive/restore cascade semantics for Teams, Memberships and downstream data.
4. Approve whether restore is MVP or later scope.
5. Approve the canonical Project API and response/error contract.
6. Follow the accepted shared MongoDB topology (`continuum_db`) in implementation planning and treat current service-specific persistence names as documentation/configuration sync work.

## 18. Dependencies

```text
Authentication
    ↓
Organization context
    ↓
Authorization evaluator
    ↓
Project lifecycle
    ↓
Project Membership
    ↓
Team / Team Membership
    ↓
Capture, Jira, Knowledge, Handover scope
```

This is a business dependency map, not an instruction to implement in this exact order.

## 19. Proposed Implementation Breakdown

Proposal only for a later planning phase:

1. Freeze Project business rules and API contract.
2. Implement repository/data access against the accepted persistence topology.
3. Implement create/list/detail/update/archive with organization-scope validation.
4. Integrate the approved authorization evaluator and `project.create` rule.
5. Add audit/outbox events for Project mutations.
6. Add Project FE pages, query/mutation hooks and permission-aware UX.
7. Add unit, persistence/index, authorization and Project E2E tests.
8. Confirm downstream archive behavior before connecting Team, Jira, Knowledge or Handover.

No implementation decision is made by this proposal.

## 20. Evidence References

- `product_docs/research-docs/01_MVP_SCOPE.md`
- `product_docs/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md`
- `product_docs/research-docs/Danh Chia Task.docx`
- `docs/product/domain-map.md`
- `docs/flows/flow-map.md`
- `docs/architecture/current-state.md`
- `docs/architecture/target-state.md`
- `docs/architecture/gaps.md`
- `docs/decisions/decision-register.md`
- `docs/specs/SPEC-001-MONGODB-PERSISTENCE.md`
- `docs/specs/SPEC-002-AUTHENTICATION-TOKEN-MODEL.md`
- `docs/specs/SPEC-004-BFF-ROUTING-ARCHITECTURE.md`
- `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts`
- `DATN-BE/src/services/iam/infrastructure/persistence.ts`
- `DATN-BE/src/services/iam/controllers/iam.controller.ts`
- `DATN-BE/src/services/iam/application/iam.service.ts`
- `DATN-FE/src/stores/client-state.ts`
- `DATN-FE/src/lib/api-client.ts`
- `DATN-FE/src/lib/bff-proxy.ts`
- `.sage/inventory/apis.md`
- `.sage/inventory/database.md`
- `.sage/inventory/frontend.md`
- `.sage/inventory/tests.md`
