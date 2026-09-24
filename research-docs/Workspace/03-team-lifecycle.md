# [RESEARCH] Workspace - Team Lifecycle

Status: Research only. No implementation was performed.

## Evidence classification

- `[FACT]`: directly verified in source.
- `[IMPLEMENTED]`: executable behavior exists.
- `[DESIGN]`: product/architecture/specification direction.
- `[PARTIAL]`: supporting structure exists but capability is incomplete.
- `[GAP]`: requirement is not implemented.
- `[INFERENCE]`: synthesized conclusion.
- `[UNKNOWN]`: insufficient evidence.
- `[DECISION REQUIRED]`: human decision needed.

## 1. Executive Summary

`[DESIGN]` A Team is a working group inside a Project. The intended hierarchy is Organization → Project → Team. Team scope is used for member access, knowledge ownership, work capture and later handover.

`[FACT]` The backend contains a `teams` schema with required `organizationId`, `projectId`, `name` and `code`, plus optional `description`. A unique `(organizationId, projectId, code)` index is declared.

`[PARTIAL]` Team persistence scaffolding exists, but the current source has no Team CRUD/archive API, application logic, Team lifecycle state, authorization guard, Team FE flow or Team E2E tests.

`[UNKNOWN]` The source does not define a `team.status`, `team.leaderId` or explicit Team-owner field. Product documents describe Team Leader responsibilities, but do not prove that a Team stores a direct leader reference.

## 2. Business Goal

The Team boundary should allow a Project to:

- organize users by working responsibility;
- scope knowledge, work notes and handover responsibilities;
- control Team Membership separately from Project Membership;
- apply project/team authorization without allowing cross-project leakage;
- preserve historical Team references when a Team is archived.

## 3. Scope

Included:

- Team purpose and Project/Organization relation;
- create, list, detail, update, archive and possible restore;
- code uniqueness and indexes;
- Team scope/access and authorization dependencies;
- Team Leader relationship;
- Membership and audit dependencies;
- current BE/FE/API/test evidence.

Excluded:

- implementing Team APIs/UI;
- deciding the final role/permission matrix;
- implementing Team Membership;
- deciding archive cascade policy without human approval.

## 4. Verified Requirements

| Requirement | Evidence | Classification | Notes |
|---|---|---|---|
| Team belongs to a Project | Team schema; product hierarchy | `[FACT]` / `[DESIGN]` | `projectId` is required in source. |
| Team also carries Organization scope | Team schema | `[FACT]` | `organizationId` is required. |
| Team has name/code/description | Team schema | `[FACT]` | These are the only business fields directly evidenced by source. |
| Team code unique in Project/Organization scope | IAM persistence | `[FACT]` | Unique `(organizationId, projectId, code)` declaration. |
| Teams are managed inside Project scope | Actors/permissions docs; leader breakdown | `[DESIGN]` | Exact actor policy is not implemented. |
| Team create is permission controlled | Leader breakdown; actors/permissions docs | `[DESIGN]` | Admin or delegated Team Leader direction exists, exact matrix is unresolved. |
| Team list/detail/update/archive are expected | `Danh Chia Task.docx` | `[DESIGN]` | No backend API found. |
| Team must belong to the correct Project | Leader breakdown | `[DESIGN]` | Must be backend validated. |
| Team archive is preferred to hard delete | Leader breakdown | `[DESIGN]` | No Team lifecycle status exists in source. |
| Team mutations require audit | Leader/product audit requirements | `[DESIGN]` | Audit scaffold exists, wiring does not. |
| Team FE flow exists | FE source inventory | `[GAP]` | No dedicated Team page/hook was found. |

## 5. Team Lifecycle

The current source does not define Team lifecycle states.

| Action/state | Evidence | Classification | Finding |
|---|---|---|---|
| Create | Leader breakdown; Team schema | `[DESIGN]` / `[PARTIAL]` | Schema supports creation data, but no command/API exists. |
| Active/usable | Product hierarchy and normal Team behavior | `[INFERENCE]` | No `status` field proves this in source. |
| Update | Leader breakdown | `[DESIGN]` / `[GAP]` | Mutable fields and constraints unknown. |
| Archive | Leader breakdown | `[DESIGN]` / `[GAP]` | No status/archive metadata or transition logic. |
| Restore | Leader asks to verify if evidence exists | `[UNKNOWN]` | No source or accepted product rule found. |
| Hard delete | Soft-delete/archive guidance | `[DESIGN]` | Exceptional deletion policy unknown. |

The only lifecycle that can be described without inventing a state field is:

```text
Create → usable Team → Update* → Archive?
```

`Archive?` remains a required policy decision because leader requirements mention it but source does not model it.

## 6. Business Rules

### Evidence-supported/design rules

1. `[DESIGN]` A Team must belong to exactly one Project scope for normal MVP operation.
2. `[DESIGN]` A Team must carry Organization context consistent with its Project.
3. `[FACT]` The current source requires both `organizationId` and `projectId` on Team.
4. `[FACT]` Team code is intended to be unique within `(organizationId, projectId)` by declared index.
5. `[DESIGN]` Team creation, update and archive require authorization within the Project scope.
6. `[DESIGN]` Team Membership must be validated against the Team's Project.
7. `[DESIGN]` Team changes require audit coverage.
8. `[DESIGN]` Team data should be archived rather than hard-deleted where historical knowledge references it.

### Not established

- Whether a Team has a lifecycle status separate from Project status.
- Whether a Team must have one or more Team Leaders.
- Whether a Team Leader is represented by a direct field, role assignment or Team Membership.
- Whether the Team creator becomes a Team Leader or only a Team member.
- Whether Team archive cascades to Team Membership.
- Whether Team archive prevents Project archive or vice versa.
- Whether restore is supported.

## 7. Entity Relationships

```text
Organization
    └── Project
          └── Team
                └── Team Membership → User
```

`[FACT]` The Team schema has `organizationId` and `projectId`. `[INFERENCE]` The duplicated Organization scope is intended to support tenant/scope validation, but the rule that these IDs must match the parent Project is not executable in current source.

`[DESIGN]` Product authorization describes persistent `TEAM_LEADER` as a role, but scoped Team leadership is described as a policy/assignment boundary. `[UNKNOWN]` There is no direct source evidence of a `leaderId` field or Team-specific leader assignment record.

## 8. Backend Current State

| Area | Source | Status | Evidence |
|---|---|---|---|
| Team schema | IAM Mongo schemas | `[PARTIAL]` | Required relation/data fields exist. |
| Unique index | IAM persistence | `[PARTIAL]` | `(organizationId, projectId, code)` unique index declaration exists in source; runtime index creation and duplicate-write behavior are not verified. |
| Team status/archive | IAM schema | `[GAP]` | No status field or archive transition. |
| Team repository | IAM source | `[GAP]` | No Team repository/data-access flow found. |
| Team DTO/API | IAM source | `[GAP]` | No Team DTO or controller route. |
| Team service logic | IAM application service | `[GAP]` | Service returns health only. |
| Project consistency validation | IAM source | `[GAP]` | No application validation found. |
| Authorization | IAM source/architecture gaps | `[GAP]` | No executable Team policy guard. |
| Audit | IAM audit service/schema | `[PARTIAL]` | Generic infrastructure exists only. |
| Tests | backend test inventory | `[GAP]` | No Team lifecycle/index behavior test. |

## 9. Frontend Current State

| Area | Source | Status | Evidence |
|---|---|---|---|
| Team list/detail | FE app/routes | `[GAP]` | No dedicated Team workspace route found. |
| Team create/edit/archive | FE source | `[GAP]` | No Team mutation hook/form found. |
| Team member view | FE source | `[GAP]` | No workspace Team Membership UI found. |
| Project context | `client-state.ts` | `[PARTIAL]` | `activeProjectId` exists but is not a Team flow. |
| Permission-aware Team UX | FE source | `[GAP]` | No verified workspace permission hook. |
| Tests | FE tests | `[GAP]` | No Team page/hook tests. |

Generic dashboard/table components contain sample project/team-like display data, but `[FACT]` this is not evidence of a connected Team management feature.

## 10. API / Contract Findings

`[DESIGN]` Product/API inventory describes a target `/api/v1/teams/*` surface. The BFF architecture provides the general browser path `/api/backend/*`, but no Team-specific endpoint is implemented.

| Action | FE | BFF | Backend | Status |
|---|---|---|---|---|
| List Teams in Project | No Team hook/page | Generic catch-all only | No route | `[GAP]` |
| Create Team | No form/hook | Generic catch-all only | No route | `[GAP]` |
| Team detail/update | No flow | Generic catch-all only | No route | `[GAP]` |
| Archive/restore | No flow | Generic catch-all only | No route/state | `[GAP]` |
| Team member list | No flow | Generic catch-all only | No route | `[GAP]` |
| Pagination/filter/sort | No Team contract | Generic forwarding | No DTO/response | `[UNKNOWN]` |

No final Team request DTO, response DTO, error mapping or optimistic-concurrency contract is evidenced.

## 11. Data / Index Findings

### Current source

- Team `organizationId`: required ObjectId.
- Team `projectId`: required ObjectId.
- Team `name`: required string.
- Team `code`: required uppercase/trimmed string.
- Team `description`: optional string.
- Unique declaration: `(organizationId, projectId, code)`.

### Gaps and conflicts

- `[GAP]` No Team `status`, `archivedAt`, `archivedBy`, archive reason or version field.
- `[UNKNOWN]` The persistence index is declared, but runtime index creation is separately controlled by infrastructure settings.
- `[ACCEPTED DECISION]` MVP operational persistence uses MongoDB 7.0 with shared `continuum_db` under DEC-011/ADR-002. `[DOCUMENTATION SYNC NEEDED]` Current persistence names remain service-specific in historical source/inventory references; this is a synchronization issue, not an open architecture decision.
- `[UNKNOWN]` No rule proves that a Team's Organization must equal the parent Project's Organization at runtime.

## 12. Authorization Dependencies

Team actions depend on:

1. authenticated user;
2. Organization context;
3. Project existence and state;
4. Project Membership and Project policy;
5. Team-specific role/capability/delegation;
6. explicit deny and cross-Project isolation;
7. Team Membership validation.

`[DESIGN]` Admin may manage Team configuration according to organization policy. Team Leaders may create/manage Teams only in assigned/delegated Project scope. The exact permission codes and delegation rules remain unresolved.

`[GAP]` Backend has no Team authorization guard or scope resolver.

## 13. Membership Dependencies

`[DESIGN]` A Team is not an independent tenant boundary. It is nested under Project, so:

- Team Membership must reference the same Project;
- a Team Member must first be a Project Member;
- Project archive/remove rules may affect Team access;
- Team archive behavior must preserve or explicitly transition Team Membership records.

`[UNKNOWN]` No final cascade policy is defined for Team archive versus Project Membership, Team Membership, ownership assignments, Jira or Knowledge.

## 14. Audit Dependencies

Audit candidates:

- Team creation;
- Team rename/update/code changes;
- Team archive/restore if supported;
- Team Membership additions/removals;
- Team policy or Team Leader assignment changes;
- denied cross-Project Team access where security policy requires it.

`[PARTIAL]` Generic audit schema/service exists. `[GAP]` No Team mutation or event producer is implemented.

## 15. Requirement → Evidence → Implementation → Gap

| Requirement | Evidence | Current implementation | Gap |
|---|---|---|---|
| Team belongs to Project | Schema/product hierarchy | `projectId` field | No runtime parent validation |
| Team has Organization scope | Schema | `organizationId` field | No consistency enforcement |
| Team code unique | Persistence definition | Unique declaration | No API conflict behavior/test |
| Team create/list/detail/update | Leader breakdown | Schema only | No API/service/UI |
| Team archive | Leader breakdown | No state field | Lifecycle decision and implementation missing |
| Team restore | No confirmed evidence | None | Unknown/MVP decision required |
| Team access scoped | Product authorization docs | No guard | Security gap |
| Team Leader relationship | Product role docs | No direct field/assignment flow | Representation unknown |
| Team audit | Product/leader docs | Generic audit scaffold | No event wiring |
| Team tests | Leader testing section | No Team tests | Test gap |

## 16. FE / BE Mismatch

1. `[GAP]` There is no Team FE flow and no Team backend endpoint.
2. `[UNKNOWN]` No shared Team TypeScript/DTO contract exists.
3. `[DESIGN]` BFF routing is generic, but absence of backend routes means forwarding cannot produce a feature.
4. `[GAP]` FE cannot enforce Team security; backend authorization is not implemented either.
5. `[UNKNOWN]` Archive/error/pagination/filter/sort semantics are not represented in FE.

## 17. UNKNOWN

- Does Team have a status lifecycle?
- Is Team archive reversible?
- Who can create/update/archive a Team?
- Must the actor be a Project Member?
- Must a Team Leader be a Project Member?
- Is Team Leader stored as a role assignment, membership role or direct field?
- What happens to Team Membership when Team is archived?
- What happens to Team data when Project is archived?
- Is Team code immutable?
- What are the exact API and UI contracts?

## 18. DECISION REQUIRED

1. Approve Team lifecycle states and archive/restore policy.
2. Approve Team Leader representation and assignment rules.
3. Approve Team create/update/archive permission matrix.
4. Approve Project/Team archive cascade semantics.
5. Approve Team API and FE/BE contract.
6. Confirm whether Team status fields must be added later or archive is represented elsewhere.

## 19. Dependencies

```text
Organization
    ↓
Project
    ↓
Project Membership / authorization
    ↓
Team lifecycle
    ↓
Team Membership
    ↓
Team-scoped Capture / Knowledge / Handover
```

## 20. Proposed Implementation Breakdown

Proposal only:

1. Resolve Team lifecycle and Team Leader decisions.
2. Freeze Team API, validation and error contract.
3. Implement Project-parent and Organization consistency validation.
4. Implement Team CRUD/archive behavior against the approved model.
5. Integrate authorization and audit/outbox events.
6. Implement Team list/detail/form/archive UI and query/mutation hooks.
7. Integrate Team Membership only after Project Membership rules are approved.
8. Add unique-index, authorization, archive and Team E2E tests.

## 21. Evidence References

- `product_docs/research-docs/01_MVP_SCOPE.md`
- `product_docs/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md`
- `product_docs/research-docs/Danh Chia Task.docx`
- `docs/product/domain-map.md`
- `docs/flows/flow-map.md`
- `docs/architecture/current-state.md`
- `docs/architecture/gaps.md`
- `docs/decisions/decision-register.md`
- `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts`
- `DATN-BE/src/services/iam/infrastructure/persistence.ts`
- `DATN-BE/src/services/iam/controllers/iam.controller.ts`
- `DATN-BE/src/services/iam/application/iam.service.ts`
- `DATN-FE/src/stores/client-state.ts`
- `.sage/inventory/apis.md`
- `.sage/inventory/database.md`
- `.sage/inventory/frontend.md`
- `.sage/inventory/tests.md`
