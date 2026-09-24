# [RESEARCH] Workspace - Project Membership

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

`[DESIGN]` Project Membership represents the relationship between a User and a Project. It is the primary prerequisite for Project-scoped access and for adding a User to a Team.

`[FACT]` The backend contains a `project_memberships` Mongoose schema with `organizationId`, `projectId`, `userId`, `status` (`ACTIVE` or `INACTIVE`) and `joinedAt`. A unique `(projectId, userId)` index is declared.

`[PARTIAL]` The membership entity exists only as persistence scaffolding. No add/remove/update-role endpoint, service logic, authorization enforcement, invitation acceptance flow, frontend member-management flow or membership E2E was found.

`[CONFLICT]` Leader/product documents describe a richer state model (`ACTIVE`, `INVITED`, `SUSPENDED`, `REMOVED`) and onboarding/offboarding states, while the current source schema exposes only `ACTIVE`/`INACTIVE`. This document records the mismatch without choosing a canonical model.

## 2. Business Goal

Project Membership should:

- make Project access explicit and auditable;
- prevent users outside a Project from reading or mutating Project resources;
- support adding, changing and removing Project participants without deleting historical identity references;
- provide the prerequisite for Team Membership;
- connect Project-scoped role assignments and downstream ACL evaluation.

`[DESIGN]` A Project member is not automatically entitled to every confidential source or every knowledge object; source ACL and scoped assignments may further restrict access.

## 3. Scope

Included:

- add, remove and role-update behavior;
- membership state model and transitions;
- user eligibility;
- Project scope and cross-Project isolation;
- relationship with Role Assignment and Team Membership;
- audit, FE, API, data and tests;
- gaps and decisions required.

Excluded:

- implementing Membership APIs or UI;
- deciding the final role/capability matrix;
- implementing Team Membership;
- changing source schemas or indexes;
- deciding organization membership policy not evidenced by the repository.

## 4. Verified Requirements

| Requirement | Evidence | Classification | Notes |
|---|---|---|---|
| A Project Membership connects User and Project | Product docs; `project_memberships` schema | `[DESIGN]` / `[FACT]` | Source stores `projectId` and `userId`. |
| Membership carries Organization scope | `project_memberships` schema | `[FACT]` | `organizationId` is required in the schema. |
| Membership has status | `project_memberships` schema | `[FACT]` | Current source enum is `ACTIVE`/`INACTIVE`. |
| Membership records join time | `project_memberships` schema | `[FACT]` | `joinedAt` is required. |
| Project/user pair is unique | IAM persistence definition | `[FACT]` | Unique `(projectId, userId)` index declared. |
| User must be eligible before membership | Product/leader flow and User domain | `[INFERENCE]` | Source has no database foreign key or service validation proving this. |
| Add member is permission controlled | Leader breakdown; actors/permissions docs | `[DESIGN]` | Exact actor depends on Project policy and delegation. |
| Remove member is permission controlled | Leader breakdown; actors/permissions docs | `[DESIGN]` | No source behavior. |
| Update Project role is permission controlled | Leader breakdown; role assignment schema | `[DESIGN]` / `[PARTIAL]` | Role assignment data exists; mutation/evaluator does not. |
| Team Membership requires Project Membership | Leader task; workspace relationship | `[DESIGN]` | Must be enforced by backend, not only FE. |
| Active Team Membership blocks Project Membership removal | Leader task | `[DESIGN]` | No implementation found. |
| Cross-Project access must be denied | Actors/permissions docs | `[DESIGN]` | No executable guard found. |
| Membership changes require audit | Leader breakdown; audit docs | `[DESIGN]` | Audit infrastructure exists, mutation producer is absent. |
| Invitation/acceptance is part of the desired lifecycle | Leader and User requirements | `[DESIGN]` | Current Membership schema does not model invitation explicitly. |

## 5. Membership Lifecycle

The exact lifecycle is unresolved because the leader breakdown and source schema differ.

### Documented target direction

```text
INVITED → ACTIVE → SUSPENDED → REMOVED
             ↓
        OFFBOARDING
```

`ONBOARDING` and `OFFBOARDING` are described as membership lifecycle states in product documentation, not persistent roles.

### Current source direction

```text
ACTIVE ↔ INACTIVE
```

This is only the current schema enum and does not prove transition behavior.

| Lifecycle question | Evidence | Status |
|---|---|---|
| Add to Project | Leader/product requirements | `[DESIGN]` / `[GAP]` |
| Invitation pending | Leader/User requirements | `[DESIGN]` / `[GAP]` |
| Activate/accept invitation | Product direction; no source handler | `[DESIGN]` / `[GAP]` |
| Suspend | Product/leader state list; source does not include it | `[CONFLICT]` |
| Remove | Leader requirement; source has `INACTIVE`, not `REMOVED` | `[CONFLICT]` |
| Restore/reactivate | Not established | `[UNKNOWN]` |
| Effective date | `joinedAt` exists; future effective period not defined | `[PARTIAL]` / `[UNKNOWN]` |

## 6. Membership State Model

| State | Document meaning | Source evidence | Classification |
|---|---|---|---|
| `ACTIVE` | User can participate within authorized Project scope | Source enum; product docs | `[FACT]` / `[DESIGN]` |
| `INVITED` | Invitation exists but membership is not active | Leader breakdown | `[DESIGN]` / `[GAP]` |
| `SUSPENDED` | Membership/user access temporarily narrowed | Leader breakdown/product lifecycle | `[DESIGN]` / `[GAP]` |
| `REMOVED` | Membership no longer grants Project access while history remains | Leader breakdown | `[DESIGN]` / `[GAP]` |
| `INACTIVE` | Current source status value | Schema enum | `[FACT]`, but semantic mapping is unknown |
| `ONBOARDING` | Incoming member lifecycle state | Product docs | `[DESIGN]`, relation to membership record unresolved |
| `OFFBOARDING` | Departing/transferring member lifecycle state | Product docs | `[DESIGN]`, relation to membership record unresolved |

`[DECISION REQUIRED]` Product/leader must choose the canonical state vocabulary and transition matrix. `INACTIVE` must not be silently treated as `REMOVED` or `SUSPENDED`.

## 7. Business Rules

### Evidence-supported/design rules

1. `[DESIGN]` A Project Membership must be scoped to an Organization and Project.
2. `[DESIGN]` Only authorized actors may add, remove or change a member's Project role.
3. `[DESIGN]` User access to Project resources requires active membership plus applicable role/capability/ACL checks.
4. `[DESIGN]` A User must be a Project Member before being added to a Team.
5. `[DESIGN]` A Project Membership must not be removed while an active Team Membership remains.
6. `[DESIGN]` Cross-Project access must be denied unless explicitly authorized.
7. `[DESIGN]` Membership/role changes must be audited.
8. `[DESIGN]` Removing membership should preserve historical records rather than hard-delete them.

### Not established

- Whether adding a member immediately creates `ACTIVE` or first creates `INVITED`.
- Whether a user must be `ACTIVE` at organization level to receive an invitation.
- Whether Project Membership itself stores a role or only references `role_assignments`.
- Whether changing a role terminates or preserves Team Membership.
- Whether removing a Project Member automatically removes scoped SME/Knowledge Owner assignments.
- Whether membership status changes revoke sessions immediately.

## 8. Entity Relationships

```text
Organization
    ├── User / organization identity
    └── Project
          └── Project Membership
                ├── userId → User
                ├── projectId → Project
                └── role assignment / capability evaluation
                      ↓
                 Team Membership prerequisite
```

`[FACT]` Source fields:

- Project Membership: `organizationId`, `projectId`, `userId`, `status`, `joinedAt`.
- Role Assignment: `organizationId`, optional `projectId`, `userId`, `roleId`, `roleCode`, `assignedBy`.
- Team Membership separately stores `organizationId`, `projectId`, `teamId`, `userId`, `joinedAt`.

`[UNKNOWN]` The source does not define a foreign-key enforcement mechanism. Relationship validity must therefore come from application authorization and validation logic, which is currently absent.

## 9. Backend Current State

| Area | Source | Status | Evidence |
|---|---|---|---|
| Membership schema | IAM Mongo schemas | `[PARTIAL]` | Entity fields exist. |
| Unique index | IAM persistence | `[PARTIAL]` | `(projectId, userId)` unique index declaration exists in source; runtime index creation and duplicate-write behavior are not verified. |
| Add/remove service | IAM application layer | `[GAP]` | Only health service method found. |
| Role update | Role assignment schema | `[PARTIAL]` | Storage structure exists; no command/evaluator. |
| State transitions | IAM source | `[GAP]` | No transition service or DTO. |
| Scope validation | Guards/policies | `[GAP]` | No executable membership guard found. |
| Audit | IAM audit service/schema | `[PARTIAL]` | Generic infrastructure exists, no membership mutation wiring. |
| API | IAM controller | `[GAP]` | Only health endpoint/message pattern. |
| Tests | backend tests | `[GAP]` | No Membership unit/integration/E2E tests. |

## 10. Frontend Current State

| Area | Source | Status | Evidence |
|---|---|---|---|
| Project member list | `DATN-FE/src/app`, `src/lib/queries` | `[GAP]` | No dedicated Member page or query found. |
| Add/remove member UI | FE source | `[GAP]` | No verified form/action found. |
| Role update UI | FE source | `[GAP]` | No Project Membership role flow found. |
| Permission-aware action visibility | FE source | `[GAP]` | No verified workspace permission hook. |
| Loading/error/empty states | Generic components/API client | `[PARTIAL]` | Generic primitives exist, no membership flow uses them. |
| Tests | FE tests | `[GAP]` | Generic query/store tests only. |

## 11. API / Contract Findings

`[DESIGN]` The repository inventory describes a future IAM API surface under `/api/v1/projects/*`, `/api/v1/teams/*` and `/api/v1/memberships/*`. The exact membership paths are not proven by a live backend implementation.

| Action | Expected contract status |
|---|---|
| List Project Members | Design only; no backend route or FE hook |
| Add Project Member | Design only; no DTO/service/controller |
| Remove Project Member | Design only; no transition/error behavior |
| Update Member Role | Design only; relationship with `role_assignments` unresolved |
| Invitation accept | Unknown endpoint and flow |
| Pagination/filter/sort | Leader requires standardized contract; no membership contract exists |
| 401/403/404/409/422 | General architecture direction only; membership-specific mapping unknown |

## 12. Authorization Dependencies

Membership authorization depends on:

1. authenticated subject and current session;
2. Organization context;
3. Project existence and state;
4. actor's role/capability in the relevant scope;
5. target user's organization/user state;
6. Project policy and explicit deny;
7. Team Membership constraints before removal.

`[DESIGN]` Admin can manage organization membership policy. Team Leader may manage members only within assigned/delegated Project/Team scope and must not escalate permissions.

`[GAP]` No backend guard, current-user decorator, capability evaluator or cross-Project denial path was found.

## 13. Audit Dependencies

Required audit candidates from the leader/product documents:

- add Project Member;
- invitation/resend/acceptance;
- activate/suspend/remove membership;
- Project role change;
- failed or denied sensitive membership operation if security policy requires it;
- attempted removal blocked by active Team Membership.

`[PARTIAL]` Audit schema/services exist. `[GAP]` No Membership command exists to emit these records, and no final event vocabulary is approved.

## 14. Requirement → Evidence → Implementation → Gap

| Requirement | Evidence | Current implementation | Gap |
|---|---|---|---|
| Add member | Leader breakdown; actor docs | Membership schema only | No API, policy or FE action |
| Remove member | Leader breakdown | Schema only | No removal transition or active-team check |
| Update role | Role assignment schema/docs | Role storage only | No assignment policy/evaluator |
| Official state model | Leader/product docs vs source enum | Source only `ACTIVE`/`INACTIVE` | State conflict requires decision |
| User eligibility | User/member domain docs | IDs are stored; no validation | No application check |
| Cross-Project isolation | Authorization docs | No guard | Security gap |
| Team prerequisite | Leader rule | No Team Membership command | Backend constraint missing |
| Historical preservation | Leader soft-delete guidance | Status field exists | No lifecycle behavior |
| Audit | Audit schema/service | Generic scaffold | No event wiring |
| FE member management | Leader breakdown | No dedicated UI/hooks | Complete FE gap |
| Membership tests | Leader testing section | No workspace tests | Complete test gap |

## 15. FE / BE Mismatch

1. `[GAP]` No FE membership API usage exists, while backend has no membership endpoint.
2. `[CONFLICT]` The source status enum does not match the leader/product status vocabulary.
3. `[UNKNOWN]` FE role/member types are not defined as a workspace contract.
4. `[UNKNOWN]` Invitation acceptance has no FE route or backend contract.
5. `[DESIGN]` FE permission checks cannot replace backend authorization, but no backend evaluator currently exists.

## 16. UNKNOWN

- Official Project Membership status list and transitions.
- Whether invitation is a User state, Membership state or both.
- Whether add-member creates an invitation or active membership.
- User eligibility requirements and organization membership prerequisite.
- Exact actor allowed to add/remove/change role.
- Whether a Team Leader can change a Project role.
- Effective-from/effective-to semantics.
- Behavior of membership on Project archive.
- Behavior of role/membership removal on Team Membership, assignments, documents and knowledge.
- Exact API paths, DTOs, pagination and errors.

## 17. DECISION REQUIRED

1. Approve canonical Membership states and transitions.
2. Approve invite/acceptance ownership between User and Membership domains.
3. Approve add/remove/change-role actor matrix.
4. Approve relationship between Project Membership and `role_assignments`.
5. Approve whether active Team Membership blocks removal as a hard business invariant.
6. Approve session/cache behavior after membership or role changes.
7. Approve API contract and error mapping.

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
Team Membership
```

This is a dependency map for research and domain reasoning, not an absolute implementation order.

## 19. Proposed Implementation Breakdown

Proposal only:

1. Resolve Membership state and invitation decisions.
2. Freeze add/remove/change-role API and authorization contract.
3. Implement repository/service validation for Organization, User and Project scope.
4. Implement state transitions and active-Team-Membership removal protection.
5. Integrate role assignment and audit/outbox events.
6. Add FE member list/actions with permission-aware UX and explicit error states.
7. Add unique-index, authorization, state-transition and Membership E2E tests.

## 20. Evidence References

- `product_docs/research-docs/01_MVP_SCOPE.md`
- `product_docs/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md`
- `product_docs/research-docs/Danh Chia Task.docx`
- `docs/product/domain-map.md`
- `docs/flows/flow-map.md`
- `docs/architecture/gaps.md`
- `docs/decisions/decision-register.md`
- `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts`
- `DATN-BE/src/services/iam/infrastructure/persistence.ts`
- `DATN-BE/src/services/iam/controllers/iam.controller.ts`
- `DATN-BE/src/services/iam/application/iam.service.ts`
- `DATN-FE/src/lib/api-client.ts`
- `DATN-FE/src/lib/bff-proxy.ts`
- `.sage/inventory/apis.md`
- `.sage/inventory/database.md`
- `.sage/inventory/tests.md`
