# [REVIEW] Workspace Research Review

Review date: 2026-09-24

Review scope: independent verification of the four Workspace research documents against the current product documentation, SAGE inventory, governed documentation, leader task breakdown, DATN-BE, and DATN-FE.

This is a review report only. No source code, architecture, ADR, SPEC, decision register, product requirement, Jira issue, or the four reviewed research documents were modified.

## Review Method

The review checks major claims using the following chain:

`claim -> source evidence -> interpretation -> implementation status -> scope`

The review distinguishes a persistence declaration from an executable business capability. A Mongoose schema, index declaration, generic query wrapper, module scaffold, or dashboard template is not treated as a completed product feature.

## Review Result Vocabulary

- `[PASS]`: the claim is supported by the cited source.
- `[PARTIAL]`: the claim is supported only for part of the asserted scope.
- `[UNSUPPORTED]`: sufficient evidence was not found.
- `[CONTRADICTED]`: another source directly conflicts with the claim.
- `[OVERSTATED]`: the claim goes beyond the evidence or its implementation status is too strong.
- `[MISSING]`: an important requirement or finding is absent.
- `[SCOPE_ERROR]`: the claim belongs to another domain or crosses the stated issue boundary.
- `[GOOD_UNKNOWN]`: the research correctly keeps the matter unresolved.
- `[GOOD_DECISION_REQUIRED]`: the research correctly preserves a human decision boundary.

The reviewed research files use the required evidence labels `[FACT]`, `[IMPLEMENTED]`, `[DESIGN]`, `[PARTIAL]`, `[GAP]`, `[INFERENCE]`, `[UNKNOWN]`, and `[DECISION REQUIRED]`. This review also calls out where a label should be narrowed.

# 1. Project Lifecycle Review

## Verdict

`PASS_WITH_CORRECTIONS`

The document covers the requested Project lifecycle scope and does not claim that the current schema is a complete CRUD feature. A small status correction is required for index declarations, and the generic frontend mutation test should be called out explicitly as a scaffold rather than Project functionality.

## Strengths

- `[PASS]` The document identifies the source Project fields: `organizationId`, `name`, `code`, `description`, `status`, and `createdBy`, with `ACTIVE` and `ARCHIVED` as schema values. Evidence: `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:66-75`; research file 01, sections 4 and 11.
- `[PASS]` It correctly identifies the declared composite uniqueness rule for `(organizationId, code)` and does not turn that declaration into a working Project API. Evidence: `DATN-BE/src/services/iam/infrastructure/persistence.ts:21-22`; research file 01, sections 4 and 11.
- `[PASS]` It covers Create, List, Detail, Update, Search, Filter, Pagination, Sort, Archive, and the unresolved Restore question from the leader breakdown.
- `[PASS]` It correctly records that `IamController` exposes health only and `IamApplicationService` contains health behavior only. Evidence: `DATN-BE/src/services/iam/controllers/iam.controller.ts:10-14`; `DATN-BE/src/services/iam/application/iam.service.ts:5-8`.
- `[PASS]` It correctly reports no verified Project DTO, repository/application flow, authorization guard, Project-specific frontend page, Project-specific query hook, or Project lifecycle E2E test.
- `[GOOD_UNKNOWN]` Project ownership, archive cascade effects, archive metadata, optimistic concurrency, hard-delete exceptions, and Restore behavior remain unknown rather than being invented.
- `[PASS]` Authorization and audit are treated as dependencies and design requirements, not as implemented Project behavior.

## Findings

1. `[PASS]` The statement that a Project is organization-scoped is supported both by the schema and by the product/domain documentation. The schema proves the field exists; it does not by itself prove organization access enforcement. The research makes that distinction.
2. `[PASS]` The statement that Project code is unique within an Organization is accurate as a persistence declaration. It should remain qualified as a declared index until runtime index creation and duplicate-write behavior are tested.
3. `[PARTIAL]` The research labels the Project index row `[IMPLEMENTED]` while also stating that runtime creation depends on configuration and `MONGODB_AUTO_INDEX` defaults. The safer classification is `[PARTIAL]` or `[FACT: DECLARATION ONLY]`; a code declaration is not proof that the running database has the index.
4. `[PASS]` The frontend finding is materially accurate: `activeProjectId` exists in `DATN-FE/src/stores/client-state.ts`, but this is client selection state, not Project management, server context, or authorization.
5. `[PARTIAL]` `DATN-FE/src/lib/queries/backend.ts` contains a generic `useBackendMutation`, and `backend.spec.tsx` exercises it with the string `/projects`. This is a generic wrapper test with a mocked response, not a Project endpoint, Project hook, page, DTO, or integration. The research conclusion remains correct, but this scaffold should be named explicitly to prevent a reader from mistaking the test fixture for Project support.
6. `[PASS]` The BFF route and API client are correctly described as routing infrastructure. They do not prove that the backend exposes Project operations.

## Missing Evidence

- No source evidence was found for Project create/list/detail/update/archive transitions, query behavior, validation, authorization, audit event wiring, or E2E behavior.
- No source evidence was found for Project-specific loading, error, empty, search, filter, pagination, or sort UI behavior.
- No source evidence proves whether an archived Project remains readable, blocks child mutations, blocks login/context selection, or cascades to Teams and Memberships.
- No source evidence proves Project ownership or an owner/leader field. The research correctly marks this unknown; it should not be added to the current model as a fact.

## Unsupported Claims

- No material unsupported Project claim was found.
- The only status concern is the `[IMPLEMENTED]` label on an index declaration; the underlying factual statement that the declaration exists is supported.

## Conflicts

- The leader breakdown describes Project CRUD and Archive as required work, while current backend source exposes only health behavior. This is an implementation gap, not a contradiction in the research.
- The leader breakdown leaves the database/ID/API standards to be finalized, while current schemas use MongoDB `ObjectId` and current persistence uses service-specific database names. The research records this as a conflict/decision boundary rather than resolving it.

## Unknown / Decision Required

The research correctly preserves these items:

- Restore as MVP behavior.
- Archive effects on Teams, Memberships, Knowledge, Capture, and related resources.
- Project ownership/leader semantics.
- Exact fields allowed by Update.
- Search/filter/pagination/sort response contract.
- Whether hard delete is ever allowed.
- Exact Project read/update/archive capability mapping.
- Whether the accepted database topology supersedes the historical repository notes.

## Scope Issues

`[PASS]` No Project document was found to absorb Authentication implementation, Session implementation, Knowledge, Jira, or SAG. Auth, audit, and organization context are described as dependencies only.

## Recommended Corrections

1. Change the Project index implementation label from `[IMPLEMENTED]` to `[PARTIAL]` or explicitly state `declaration only; runtime index not verified` in the same table cell.
2. Add `DATN-FE/src/lib/queries/backend.ts` and `backend.spec.tsx` to the FE evidence list as generic infrastructure/scaffold, explicitly stating that `/projects` is a mocked test input and not a working Project API.
3. Keep the current separation between schema facts, design requirements, and executable behavior.

# 2. Project Membership Review

## Verdict

`PASS_WITH_CORRECTIONS`

The document accurately separates the current `project_memberships` persistence scaffold from the requested membership lifecycle. It correctly exposes the most important state-model conflict, but the unique-index status should receive the same declaration-only qualification as Project and Team indexes.

## Strengths

- `[PASS]` The source fields are accurately reported: `organizationId`, `projectId`, `userId`, `status`, and `joinedAt`; the current enum is `ACTIVE`/`INACTIVE`. Evidence: `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:91-100`.
- `[PASS]` The declared unique `(projectId, userId)` index is accurately reported. Evidence: `DATN-BE/src/services/iam/infrastructure/persistence.ts:31-32`.
- `[PASS]` The document covers Add, Remove, Update Role, status, eligibility, project scope, cross-project access, team dependency, authorization, audit, frontend behavior, API, data, and tests.
- `[PASS]` It correctly says that no add/remove/update-role endpoint, service logic, authorization enforcement, invitation acceptance flow, frontend member-management flow, or membership E2E was found.
- `[GOOD_DECISION_REQUIRED]` The document does not silently replace the source `ACTIVE`/`INACTIVE` enum with the leader breakdown states `ACTIVE`, `INVITED`, `SUSPENDED`, and `REMOVED`.
- `[GOOD_UNKNOWN]` Invitation acceptance, effective dates, role assignment semantics, removal semantics, and user eligibility are not over-resolved.

## Findings

1. `[PASS]` The statement that Project Membership connects a User and Project is supported by both the schema and product hierarchy. The relationship is a source fact; the business meaning of active access remains a policy concern.
2. `[PASS]` The document correctly identifies the Project Membership prerequisite for Team Membership as a documented/design rule that is not enforced in source.
3. `[PASS]` The “cannot remove Project Membership while an active Team Membership exists” rule is correctly attributed to the leader breakdown and marked as non-implemented. This is not claimed as a database constraint.
4. `[GOOD_DECISION_REQUIRED]` The state mismatch is correctly surfaced: source supports only `ACTIVE` and `INACTIVE`, while the leader requirement lists `ACTIVE`, `INVITED`, `SUSPENDED`, and `REMOVED`. This requires a product/domain decision and contract synchronization; it cannot be inferred from the schema.
5. `[PARTIAL]` The unique index row should be downgraded from `[IMPLEMENTED]` if it currently uses that label. The repository contains an index declaration, but no test or runtime verification proves the database index exists or rejects duplicates in the running environment.
6. `[PASS]` Role assignment is not incorrectly treated as proof that membership role mutation exists. The research distinguishes role-assignment persistence from a membership API/business operation.

## Missing Evidence

- No endpoint or service proves Add, Remove, status transition, invitation acceptance, role update, or eligibility validation.
- No evidence proves whether an invited user can access any Project data before acceptance.
- No evidence proves whether `INACTIVE` corresponds to Removed, Suspended, Disabled, or another business state.
- No evidence proves whether a User may belong to multiple Organizations, whether a project member must be an organization member at the time of mutation, or how cross-organization IDs are rejected.
- No evidence proves the exact audit payload, idempotency behavior, or notification behavior for membership changes.

## Unsupported Claims

- No material unsupported membership claim was found.
- The document labels user eligibility as an inference rather than a source fact, which is correct.

## Conflicts

| Topic | Source A | Source B | Conflict | Correct Handling |
|---|---|---|---|---|
| Membership states | `mongodb.schemas.ts` supports `ACTIVE` and `INACTIVE` | Leader breakdown requires `ACTIVE`, `INVITED`, `SUSPENDED`, `REMOVED` | State vocabulary and lifecycle are not aligned | `DECISION REQUIRED` plus documentation/contract synchronization |
| Membership role | `role_assignments` schema exists | Leader requires “update role” on membership | Persistence for assignments is not a mutation contract | `IMPLEMENTATION GAP`; do not infer endpoint semantics |
| Removal constraint | Leader requires active Team Membership to block Project Membership removal | Source has no service or transaction enforcing it | Rule is design-only | `IMPLEMENTATION GAP` |

## Unknown / Decision Required

The research correctly keeps the following unresolved:

- Invitation creation and acceptance flow.
- Whether invitation is a membership state or a separate invitation entity.
- Effective/joined date semantics.
- Meaning of `INACTIVE`, and whether the state model expands.
- Whether Project Membership role is stored on membership, role assignment, or both.
- What happens to Team Membership when Project Membership is suspended/removed.
- Whether the last Admin constraint applies at Organization, Project, or both scopes.

## Scope Issues

`[PASS]` Authorization and audit are used as membership dependencies. The document does not attempt to define a global authorization matrix, Authentication protocol, Knowledge ACL model, Jira integration, or SAG behavior.

## Recommended Corrections

1. Qualify the membership unique index as a declaration, not a verified runtime constraint.
2. Add an explicit note that `backend.spec.tsx` uses a generic mocked mutation and does not prove membership or Project API behavior.
3. Preserve the current state-model conflict as an explicit blocker for implementation input rather than selecting a canonical state list.

# 3. Team Lifecycle Review

## Verdict

`PASS_WITH_CORRECTIONS`

The document correctly identifies Team persistence and its Project/Organization scope, and correctly reports the absence of Team lifecycle behavior. The main correction is to distinguish the declared composite index from a verified runtime uniqueness guarantee.

## Strengths

- `[PASS]` The source Team fields are accurately reported: `organizationId`, `projectId`, `name`, `code`, and `description`. Evidence: `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:77-88`.
- `[PASS]` The document accurately identifies the declared unique composite index `(organizationId, projectId, code)`. Evidence: `DATN-BE/src/services/iam/infrastructure/persistence.ts:25-28`.
- `[PASS]` It covers Create, List, Detail, Update, Archive, Restore if evidenced, code uniqueness, Project/Organization relationship, access, authorization, audit, FE, API, data, tests, and Team Leader relationship.
- `[PASS]` It correctly notes that the Team schema has no `status`, `archivedAt`, `archivedBy`, `leaderId`, or equivalent Team lifecycle field.
- `[GOOD_UNKNOWN]` The Team Leader relationship is not inferred from the existence of `TEAM_LEADER` in the role schema. The research keeps whether a Team Leader must be a Project Member, whether there is one or many leaders, and whether leadership is role assignment or a Team field unresolved.
- `[PASS]` The absence of Team controller/service/DTO/repository/guard and Team-specific frontend behavior is accurately recorded.

## Findings

1. `[PASS]` The statement that a Team belongs to a Project is supported by `projectId` in the Team schema and by product/domain hierarchy. The schema does not provide a foreign-key or service-level referential check, and the research does not claim one.
2. `[PASS]` The unique code rule is correctly tied to the composite index and leader requirements. It should be stated as a declaration because runtime index creation and duplicate handling are untested.
3. `[PASS]` Team Archive is correctly treated as a design/leader requirement with a current implementation gap; the source enum on Project must not be reused as evidence that Team Archive exists.
4. `[PARTIAL]` If the index row is labeled `[IMPLEMENTED]`, it should be narrowed to `[PARTIAL]` or `declaration only` for the same reason as Project and Membership.
5. `[PASS]` The research does not claim that the `TEAM_LEADER` role itself establishes a Team Leader relationship. This is an important non-inference.

## Missing Evidence

- No Team lifecycle controller, service, repository, DTO, validation, guard, audit wiring, or E2E test was found.
- No source evidence proves Team Archive, Restore, archive effects, or hard-delete behavior.
- No source evidence proves whether a Team can exist without a Project Membership for its users.
- No source evidence proves a Team Leader field, assignment endpoint, cardinality, or leader succession behavior.
- No Team-specific FE pages, Team hooks, Team API integration, member tab, or Team loading/error/empty states were found.

## Unsupported Claims

- No material unsupported Team claim was found.
- Any relationship statement is appropriately tied to source fields or labeled as design/inference, not presented as a working referential constraint.

## Conflicts

| Topic | Source A | Source B | Conflict | Correct Handling |
|---|---|---|---|---|
| Team lifecycle state | Leader requires Archive and possibly Restore | Team schema has no status or archive metadata | Required behavior has no current persistence representation | `IMPLEMENTATION GAP` and `DECISION REQUIRED` for exact semantics |
| Team Leader | Role schema contains `TEAM_LEADER` | No Team `leaderId` or Team assignment behavior exists | A role code does not define Team leadership | `UNKNOWN` / `DECISION REQUIRED` |
| Referential integrity | Team schema stores `projectId` and `organizationId` | No FK or service validation exists | Scope fields exist, enforcement does not | `IMPLEMENTATION GAP` |

## Unknown / Decision Required

- Whether Team Restore is required.
- Whether archive blocks member changes or only hides the Team.
- Whether Team archival cascades to Team Membership.
- Whether a Team must always have one leader, may have multiple leaders, or has no dedicated leader relationship.
- Whether a Team Leader must be an active Project Member.
- Whether Team code uniqueness is case-sensitive beyond the schema `uppercase` transform.

## Scope Issues

`[PASS]` The Team document does not define Authentication or invent a new auth model. Authorization, Project Membership, and audit are treated as dependencies. It does not absorb Knowledge, Jira, or SAG.

## Recommended Corrections

1. Qualify the Team index status as declaration-only unless runtime index behavior is verified.
2. Keep Team Leader as an explicit decision boundary; do not use the `TEAM_LEADER` role enum as proof of a Team leader assignment feature.
3. Keep archive/restore semantics separate from the Project status enum until a Team lifecycle model is approved.

# 4. Team Membership & Workspace FE Contract Review

## Verdict

`PASS_WITH_CORRECTIONS`

The document accurately covers Team Membership and the current Workspace FE/BE contract surface. It correctly identifies BFF/API infrastructure and `activeProjectId` as partial foundations rather than a Workspace feature. The only material correction is to make the generic `/projects` mutation test and generic UI primitives even more explicit as non-feature evidence.

## Strengths

- `[PASS]` The source Team Membership fields are accurately reported: `organizationId`, `projectId`, `teamId`, `userId`, and `joinedAt`, with no `status` field. Evidence: `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:101-110`.
- `[PASS]` The declared unique `(teamId, userId)` index is accurately reported. Evidence: `DATN-BE/src/services/iam/infrastructure/persistence.ts:35-36`.
- `[PASS]` The document covers Add, Remove, state, Project Membership prerequisite, scope, authorization, Team access, audit, API, data, tests, and frontend behavior.
- `[PASS]` The BFF route mapping is accurately tied to `SPEC-004`: browser `/api/backend/*` to backend `/api/v1/*`. Evidence: `DATN-FE/src/app/api/backend/[...path]/route.ts`, `DATN-FE/src/lib/bff-proxy.ts`, and `docs/specs/SPEC-004-BFF-ROUTING-ARCHITECTURE.md:16,40-43,76-97`.
- `[PASS]` The frontend API client behavior is accurately described: browser calls use `/api/backend`, while SSR uses `CONTINUUM_API_BASE_URL` with a `http://localhost:3001` default. Evidence: `DATN-FE/src/lib/api-client.ts:6-18`.
- `[PASS]` `activeProjectId` is correctly identified as client-only state. Evidence: `DATN-FE/src/stores/client-state.ts:5-12`.
- `[PASS]` The document correctly reports no verified Workspace pages, Workspace-specific hooks, Team Membership endpoints, backend DTOs, authorization guards, or Workspace E2E flow.
- `[GOOD_UNKNOWN]` Team Membership state, API DTO details, pagination/filter/sort/error contracts, permission-aware UI behavior, invitation behavior, and archive effects remain unresolved.

## Findings

1. `[PASS]` The Team Membership prerequisite and Project Membership removal constraint are correctly treated as design requirements from the leader breakdown, not as current source behavior.
2. `[PASS]` The BFF target is correct for the current architecture. A functioning catch-all route is not equivalent to functioning Project/Team/Membership endpoints, and the research preserves that distinction.
3. `[PARTIAL]` `DATN-FE/src/lib/queries/backend.ts` provides a generic health query and generic mutation wrapper. `backend.spec.tsx` calls the generic wrapper with `/projects` and a mocked `{id: "project-1"}` response. This is useful contract scaffolding but is not a Workspace API integration or E2E proof.
4. `[PASS]` The research treats generic dashboard tables, labels, and form primitives as templates rather than Workspace UI. This prevents false frontend implementation claims.
5. `[PARTIAL]` The BFF implementation forwards the documented request headers and exposes a catch-all route, but current backend source does not expose the Workspace business endpoints. The research correctly calls this infrastructure partial.
6. `[PASS]` The FE contract section does not turn frontend permission checks into the security boundary; backend authorization remains the required boundary.

## Missing Evidence

- No Team Membership Add/Remove endpoint, service, repository, validation, transaction, guard, or audit wiring was found.
- No source evidence proves that Team Membership is rejected when Project Membership is absent or inactive.
- No source evidence proves the Team Membership state machine or whether removal is soft, inactive, removed, or hard-deleted.
- No Project member page, Team page, Project member-management page, Team member-management page, Workspace hook, DTO mapping, permission-aware action state, or Workspace-specific loading/error/empty state was found.
- No Workspace response envelope, error contract, pagination, filter, sort, or concurrency contract is implemented.
- No FE/BE integration or Workspace E2E test was found.

## Unsupported Claims

- No material unsupported claim was found.
- The generic `/projects` mutation test could be misread as a Project feature if read without its test context, but the research's current conclusion is not unsupported. The report should explicitly call out the fixture to eliminate ambiguity.

## Conflicts

| Topic | Source A | Source B | Conflict | Correct Handling |
|---|---|---|---|---|
| Team Membership state | Leader requires four named membership states | Source has no Team Membership status field | State model is undefined in implementation | `DECISION REQUIRED` and `IMPLEMENTATION GAP` |
| BFF route | SPEC-004 and FE implement catch-all routing | Backend currently exposes health/metrics rather than Workspace routes | Transport exists; business endpoint target does not | `IMPLEMENTATION GAP`, not a routing contradiction |
| Browser auth propagation | BFF forwards cookie/authorization headers | `useAuth.ts` exposes an `AuthSession` with raw access-token data while governance requires HttpOnly cookies | Cross-domain auth conflict exists outside Workspace | Record as an external dependency; do not resolve in this document |

## Unknown / Decision Required

- Whether Team Membership has its own status or uses Project/Team lifecycle states.
- Whether Team Membership Add requires active Project Membership only, or any historical membership.
- Whether an invited user can be placed into a Team before accepting the Project invitation.
- Whether Team Membership removal affects Team-specific access immediately.
- Whether Workspace lists use offset or cursor pagination.
- Exact response envelope, error codes, filters, sort fields, and DTO mapping.
- Which UI actions are hidden, disabled, or shown with a 403 explanation.

## Scope Issues

`[PASS]` The document stays within Team Membership and Workspace FE/BE contract scope. It references Authentication, authorization, audit, and Project Membership as dependencies. It does not define the global authorization matrix, implement Authentication, or absorb Knowledge, Jira, or SAG.

## Recommended Corrections

1. Qualify the Team Membership index as a declaration-only artifact unless runtime behavior is tested.
2. Add the generic backend query wrapper/test to the explicit FE scaffold evidence list and state that the `/projects` call is mocked.
3. Retain the distinction between BFF transport readiness and missing backend Workspace endpoints.

# Business Rule Audit

| Rule | Evidence | Classification | Review Result |
|---|---|---|---|
| Project belongs to Organization | Project schema `organizationId`; product/domain docs | `[FACT]` for field, `[DESIGN]` for enforced scope | `[PASS]` The research distinguishes field presence from access enforcement. |
| Project code is unique in Organization | `persistence.ts` unique `(organizationId, code)` | `[FACT]` declaration, `[DESIGN]` rule | `[PASS]` Add runtime-index qualification. |
| Team belongs to Project | Team schema `projectId`; product hierarchy | `[FACT]` for field, `[DESIGN]` for business relationship | `[PASS]` No FK is incorrectly claimed. |
| Team code is unique in Project | `persistence.ts` unique `(organizationId, projectId, code)` | `[FACT]` declaration, `[DESIGN]` rule | `[PASS]` Add runtime-index qualification. |
| Team Membership requires Project Membership | Leader breakdown and Workspace relationship | `[DESIGN]` | `[GOOD_DECISION_REQUIRED]` Correctly not claimed as implemented. |
| Project Membership cannot be removed while active Team Membership remains | Leader breakdown | `[DESIGN]` | `[GOOD_DECISION_REQUIRED]` Correctly marked as missing backend enforcement. |
| Users outside scope cannot access resources | Product authorization docs and target state | `[DESIGN]` | `[PASS]` Correctly identified as an authorization gap. |
| Backend enforces authorization | Architecture/product requirements | `[DESIGN]` | `[PASS]` Frontend is not treated as security. |
| FE authorization is UX support only | Product docs and SPEC-002/target state | `[DESIGN]` | `[PASS]` Correct boundary. |
| Roles/permissions must not be inferred beyond evidence | Role schema, grants, product permission docs | `[FACT]` / `[DESIGN]` with open details | `[PASS]` The research keeps exact mapping and evaluator behavior unresolved. |

# UNKNOWN / DECISION REQUIRED Audit

| Item | Evidence state | Review result |
|---|---|---|
| Team Leader must be a Project Member | No Team leader field or service rule; source has role code only | `[GOOD_UNKNOWN]` |
| Invitation acceptance | Leader requires invitation-related work; no current flow | `[GOOD_UNKNOWN]` |
| Effective date and joined date semantics | `joinedAt` exists, but transition semantics are absent | `[GOOD_UNKNOWN]` |
| Archive effects | Project status exists; Team status and cascade behavior do not | `[GOOD_UNKNOWN]` / `[GOOD_DECISION_REQUIRED]` |
| Membership state naming | Leader and source enums differ | `[GOOD_DECISION_REQUIRED]` |
| API contract details | BFF transport exists; Workspace endpoint DTOs do not | `[GOOD_UNKNOWN]` |
| Role assignment versus membership role | Both persistence concepts exist, relationship is not operationalized | `[GOOD_DECISION_REQUIRED]` |
| Database topology and ID standard | Leader breakdown asks for decisions; repository evidence is not fully aligned | `[GOOD_DECISION_REQUIRED]` / documentation sync needed |

No reviewed document was found to silently resolve these matters. Recommendations in the reviewed files are generally labeled as proposals/design or decision-required rather than as approved product rules.

# Conflict Audit

| Topic | Source A | Source B | Conflict | Correct Handling |
|---|---|---|---|---|
| Project Membership states | Leader breakdown: `ACTIVE`, `INVITED`, `SUSPENDED`, `REMOVED` | Backend schema: `ACTIVE`, `INACTIVE` | Lifecycle vocabulary and persistence model differ | `DECISION REQUIRED`; synchronize product, contract, and schema before implementation |
| Team Membership state | Leader checklist expects state review | Backend `team_memberships` schema has no `status` | No current state representation | `DECISION REQUIRED` plus implementation gap |
| Team Archive | Leader requires Archive and optional Restore | Team schema has no status/archive metadata | Required lifecycle is not represented | `DECISION REQUIRED` for semantics; implementation gap |
| Database topology | Current SAGE/backend inventory reports service-specific names such as `continuum_iam` | Accepted architecture context and current governance direction require one shared `continuum_db` for MVP | Repository historical evidence and accepted direction are not synchronized | Do not reconcile in research; mark `DOCUMENTATION SYNC NEEDED` and follow the accepted decision when implementation is authorized |
| BFF transport versus business API | SPEC-004 and FE BFF implement transport | Backend gateway/IAM controllers expose health-oriented endpoints only | Transport exists without Workspace business endpoints | `IMPLEMENTATION GAP` |
| Browser token handling | Governance/SPEC-002 requires HttpOnly BFF cookies | FE auth hook inventory exposes raw access-token data to client state | Cross-domain implementation conflict | Record as external IAM dependency; do not resolve in Workspace research |
| Role and membership semantics | Role/assignment schemas exist | Leader requires member role changes and scoped management behavior | Persistence does not prove evaluator/mutation contract | `DECISION REQUIRED` plus implementation gap |

# Scope Audit

| Scope check | Result | Evidence |
|---|---|---|
| Project issue avoids Authentication implementation | `[PASS]` | Auth is listed only as authorization/session dependency. |
| Project issue avoids Knowledge, Jira, and SAG | `[PASS]` | No Workspace document claims those features. |
| Membership issue avoids defining the global authorization matrix | `[PASS]` | It references permission requirements but keeps evaluator details unresolved. |
| Team issue avoids deciding the auth model | `[PASS]` | Auth is a dependency only. |
| FE contract issue avoids treating FE checks as security | `[PASS]` | Backend authorization is identified as the boundary. |
| Proposed implementation breakdowns avoid creating new product scope | `[PASS_WITH_CORRECTIONS]` | They are marked proposals; each should continue to be treated as non-approved planning input. |

No material `[SCOPE_ERROR]` was found.

# Dependency Audit

The reviewed documents describe the dependency chain consistently:

`Authentication / Organization Context -> Authorization -> Project -> Project Membership -> Team -> Team Membership -> Workspace FE contract`

Review result:

- `[PASS]` Organization and authorization are treated as prerequisites for scoped Project/Team behavior.
- `[PASS]` Project Membership is treated as the prerequisite for Team Membership.
- `[PASS]` FE contract is downstream of backend API, authorization, and scope semantics.
- `[PASS]` The research does not claim that this dependency graph is an approved implementation order.
- `[GOOD_DECISION_REQUIRED]` Cross-domain details such as invitation acceptance, role assignment, and archive cascade remain explicit dependencies rather than assumptions.

# Implementation Status Audit

| Artifact type | What exists | What does not exist | Review result |
|---|---|---|---|
| MongoDB schemas | Project, Team, Project Membership, Team Membership, roles, assignments, grants | Complete lifecycle behavior | `[PASS]` Research distinguishes persistence from feature completion. |
| Index declarations | Composite uniqueness declarations for Project, Team, and Membership | Verified running indexes and duplicate-write tests | `[PARTIAL]` Labels should say declaration-only/runtime unverified. |
| Backend controllers | IAM health endpoint and other health-oriented module scaffolds | Workspace CRUD/membership endpoints | `[PASS]` |
| Backend application services | Health response behavior | Workspace application/use-case behavior | `[PASS]` |
| DTO/repository/guards | No verified Workspace DTO/repository/guard flow | Full contract and enforcement | `[PASS]` |
| Frontend BFF | Catch-all route and header/cookie forwarding | Workspace endpoint integration | `[PASS]` |
| Frontend API/query layer | Generic API client, health query, generic mutation wrapper | Workspace-specific hooks and DTO mapping | `[PASS_WITH_CORRECTIONS]` Generic `/projects` test must remain clearly labeled scaffold. |
| Frontend state | `activeProjectId` and setter | Server-validated project context and permission state | `[PASS]` |
| Tests | Health/config/API client/BFF/generic query/store tests | Workspace persistence, authorization, integration, and E2E tests | `[PASS]` |

# Traceability Matrix

| Research File | Claim | Source | Classification | Review Result | Comment |
|---|---|---|---|---|---|
| 01-project-lifecycle.md | Project stores organization, name, code, description, status, creator | `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:66-75` | `[FACT]` | `[PASS]` | Schema fact only. |
| 01-project-lifecycle.md | Project code has organization-scoped unique declaration | `DATN-BE/src/services/iam/infrastructure/persistence.ts:21-22` | `[FACT]` / `[DESIGN]` | `[PASS_WITH_CORRECTIONS]` | Runtime index not verified. |
| 01-project-lifecycle.md | Project lifecycle API is not implemented | IAM controller/service | `[GAP]` | `[PASS]` | Only health behavior found. |
| 01-project-lifecycle.md | `activeProjectId` is client selection state | `DATN-FE/src/stores/client-state.ts:5-12` | `[IMPLEMENTED]` | `[PASS]` | Not Project management. |
| 02-project-membership.md | Membership stores scope, user, status, and joined time | `mongodb.schemas.ts:91-100` | `[FACT]` | `[PASS]` | Current state enum is only ACTIVE/INACTIVE. |
| 02-project-membership.md | Project/user uniqueness is declared | `persistence.ts:31-32` | `[FACT]` | `[PASS_WITH_CORRECTIONS]` | Declaration is not runtime proof. |
| 02-project-membership.md | Team Membership requires Project Membership | Leader breakdown section 5 | `[DESIGN]` | `[GOOD_DECISION_REQUIRED]` | No backend enforcement found. |
| 02-project-membership.md | Membership feature is persistence-only | Schema plus absence of controller/service/FE flow/tests | `[PARTIAL]` / `[GAP]` | `[PASS]` | Evidence supports the implementation gap. |
| 03-team-lifecycle.md | Team has organization/project scope and code | `mongodb.schemas.ts:77-88` | `[FACT]` | `[PASS]` | No referential enforcement claimed. |
| 03-team-lifecycle.md | Team code uniqueness is composite | `persistence.ts:25-28` | `[FACT]` | `[PASS_WITH_CORRECTIONS]` | Runtime index not verified. |
| 03-team-lifecycle.md | Team has no implemented archive lifecycle | Team schema plus health-only IAM behavior | `[GAP]` | `[PASS]` | Correctly not inferred from Project status. |
| 03-team-lifecycle.md | Team Leader relationship is unresolved | No leader field/flow; role enum only | `[UNKNOWN]` | `[GOOD_UNKNOWN]` | Correct boundary. |
| 04-team-membership-workspace-fe-contract.md | Team Membership stores team/user/project/org scope | `mongodb.schemas.ts:101-110` | `[FACT]` | `[PASS]` | No status field. |
| 04-team-membership-workspace-fe-contract.md | Team/user uniqueness is declared | `persistence.ts:35-36` | `[FACT]` | `[PASS_WITH_CORRECTIONS]` | Runtime index not verified. |
| 04-team-membership-workspace-fe-contract.md | BFF maps browser `/api/backend/*` to backend `/api/v1/*` | SPEC-004; FE BFF route/proxy | `[DESIGN]` / `[IMPLEMENTED]` | `[PASS]` | Transport exists; business routes do not. |
| 04-team-membership-workspace-fe-contract.md | Generic API/query infrastructure exists | `DATN-FE/src/lib/api-client.ts`, `queries/backend.ts` | `[PARTIAL]` | `[PASS]` | `/projects` test is mocked generic scaffolding. |
| 04-team-membership-workspace-fe-contract.md | Workspace pages/hooks/flows are absent | FE source inventory and tests | `[GAP]` | `[PASS]` | No dedicated Workspace feature found. |

# Overall Review

## Overall Verdict

`PASS_WITH_CORRECTIONS`

The four Workspace research documents are substantially evidence-aligned. They correctly distinguish schema/index/module scaffolding from implemented business behavior, identify the absence of Workspace endpoints and FE flows, preserve important unknowns, and avoid absorbing unrelated product domains.

The corrections are important for implementation planning but do not invalidate the research set:

1. Index declarations should be labeled as declarations or partial implementation unless runtime index creation and duplicate-write behavior are verified.
2. The generic frontend mutation wrapper and its mocked `/projects` test should be called out explicitly as infrastructure scaffolding, not Project support.
3. The state-model, Team lifecycle, database topology, and browser-auth conflicts must remain visible and must not be silently resolved by an implementer.

## Critical Findings

- No material unsupported claim was found in the four research files.
- No reviewed research file claims that Project, Team, or Membership CRUD is already complete.
- The most significant product/implementation blocker is the mismatch between the leader membership state model and the current backend schema.
- Team has no current lifecycle status or Team Leader relation in source.
- BFF transport and generic FE query infrastructure exist, but no Workspace business API or Workspace UI flow exists.
- Authorization, audit, invitation, and cross-scope enforcement remain design requirements or scaffolds, not executable Workspace behavior.

## Corrections Required Before Approval

- Revise index status wording in all four research files to distinguish declaration from verified runtime behavior.
- Add an explicit note in the FE evidence sections that `backend.spec.tsx` uses a mocked generic `/projects` mutation and does not prove a Project API.
- Preserve the current conflict table and decision boundaries when the research is used as input for later planning.

## Decisions Required

- Canonical Project Membership state model and transition semantics.
- Team Membership state model.
- Invitation acceptance and eligibility rules.
- Team Leader relationship and cardinality.
- Archive/restore effects for Projects, Teams, and Memberships.
- Exact Workspace API envelope, errors, pagination, filtering, sorting, and DTO mapping.
- Final database topology and ID standard as governed by the accepted architecture decision.
- Role assignment versus membership-role representation.

## Unknowns

- Runtime index creation and production index migration behavior.
- Workspace authorization evaluator and guard behavior.
- Audit event schema/wiring/idempotency for Workspace mutations.
- Frontend permission-aware action behavior.
- Cross-domain effects on Knowledge, Capture, Jira, and SAG when Workspace scope changes.

## Cross-file Issues

- The same persistence-versus-feature distinction is used consistently, but index status wording should be normalized across all four files.
- The same source/design state distinction is used consistently for membership rules and Team lifecycle.
- The BFF contract is consistently described as transport infrastructure, not business implementation.
- The repository contains historical topology/auth notes that conflict with current accepted direction; the review records this for documentation synchronization and does not reconcile it.

## Ready for Implementation Planning?

NO

The research can serve as a strong evidence base, but it should not be treated as final implementation input until the listed corrections are applied and the state-model, archive, Team Leader, API contract, and topology decisions are explicitly resolved by the appropriate human owner. This review does not create or propose a Jira task and does not select any of those decisions.

# Evidence References

- `product_docs/research-docs/Workspace/01-project-lifecycle.md`
- `product_docs/research-docs/Workspace/02-project-membership.md`
- `product_docs/research-docs/Workspace/03-team-lifecycle.md`
- `product_docs/research-docs/Workspace/04-team-membership-workspace-fe-contract.md`
- `product_docs/research-docs/Danh Chia Task.docx`
- `product_docs/research-docs/01_MVP_SCOPE.md`
- `product_docs/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md`
- `docs/product/domain-map.md`
- `docs/flows/flow-map.md`
- `docs/architecture/current-state.md`
- `docs/architecture/target-state.md`
- `docs/architecture/gaps.md`
- `docs/specs/SPEC-004-BFF-ROUTING-ARCHITECTURE.md`
- `docs/specs/SPEC-002-AUTHENTICATION-TOKEN-MODEL.md`
- `docs/adr/ADR-001-authentication-and-token-model.md`
- `docs/adr/ADR-002-persistence-and-source-of-truth-ownership.md`
- `docs/decisions/decision-register.md`
- `.sage/inventory/apis.md`
- `.sage/inventory/backend.md`
- `.sage/inventory/frontend.md`
- `.sage/inventory/database.md`
- `.sage/inventory/tests.md`
- `.sage/inventory/unknowns.md`
- `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts`
- `DATN-BE/src/services/iam/infrastructure/persistence.ts`
- `DATN-BE/src/services/iam/controllers/iam.controller.ts`
- `DATN-BE/src/services/iam/application/iam.service.ts`
- `DATN-FE/src/app/api/backend/[...path]/route.ts`
- `DATN-FE/src/lib/bff-proxy.ts`
- `DATN-FE/src/lib/api-client.ts`
- `DATN-FE/src/lib/queries/backend.ts`
- `DATN-FE/src/lib/queries/backend.spec.tsx`
- `DATN-FE/src/stores/client-state.ts`
