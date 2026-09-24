# [RESEARCH] Workspace - Team Membership & Workspace FE Contract

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

This research covers two connected boundaries:

1. Team Membership: User ↔ Team Membership ↔ Team, constrained by Project Membership.
2. Workspace FE/BE contract: Browser → Next.js BFF → NestJS backend for Project, Membership, Team and Team Membership actions.

`[FACT]` The backend has a `team_memberships` schema with `organizationId`, `projectId`, `teamId`, `userId` and `joinedAt`, plus a unique `(teamId, userId)` index declaration.

`[DESIGN]` The leader rule is: a User must already be a Project Member before becoming a Team Member; an active Team Membership prevents removal of the related Project Membership.

`[PARTIAL]` The frontend has a generic BFF, API client and `activeProjectId` store. `[GAP]` There are no verified workspace pages, workspace hooks, Team Membership endpoints, backend DTOs, authorization guards or Workspace E2E flows.

## 2. Scope

Included:

- Team Membership add/remove/update if supported;
- state, Project prerequisite, scope validation and isolation;
- Team access and authorization dependency;
- audit dependency;
- Project/Team/Membership FE/BE/BFF contract;
- request/response/error/pagination/filter/sort findings;
- loading/empty/error/permission-aware UX evidence;
- current backend/frontend/BFF/tests;
- unknowns and decisions required.

Excluded:

- implementing any API, UI or authorization code;
- choosing final role/capability matrix;
- changing BFF/architecture/spec;
- implementing Project, Team or Project Membership domain behavior.

## 3. Team Membership Requirements

| Requirement | Evidence | Classification | Notes |
|---|---|---|---|
| Team Membership connects User and Team | `team_memberships` schema; product hierarchy | `[FACT]` / `[DESIGN]` | Source stores `teamId` and `userId`. |
| Team Membership carries Project and Organization scope | `team_memberships` schema | `[FACT]` | `organizationId` and `projectId` are required. |
| User must be a Project Member first | Leader breakdown; workspace research scope | `[DESIGN]` | Must be enforced by backend. |
| Active Team Membership blocks Project Membership removal | Leader breakdown | `[DESIGN]` | No implementation found. |
| Team Membership may be added/removed | Leader breakdown | `[DESIGN]` / `[GAP]` | Schema only. |
| Team Membership state exists | Leader checklist asks to verify | `[UNKNOWN]` | Source has no `status` field. |
| Team access is scope-limited | Product authorization docs | `[DESIGN]` | No executable guard. |
| Cross-project/team isolation is required | Product authorization docs | `[DESIGN]` | No E2E security test. |
| Team Membership changes are audited | Leader/product audit requirements | `[DESIGN]` | Audit scaffold exists; event wiring absent. |

## 4. Team Membership Lifecycle

The only relationship constraint that is directly stated in the leader task is:

```text
User
  ↓ must already be Project Member
Team Membership
  ↓
Team-scoped access
```

| Action/state | Evidence | Status |
|---|---|---|
| Add Team Member | Leader breakdown | `[DESIGN]` / `[GAP]` |
| Remove Team Member | Leader breakdown | `[DESIGN]` / `[GAP]` |
| Update Team Membership | “if any” in research scope | `[UNKNOWN]` |
| Active membership | Business wording and source relationship | `[DESIGN]` / `[PARTIAL]` |
| Invited/suspended/removed state | Leader Project Membership state list, not proven for Team Membership | `[UNKNOWN]` |
| Restore/rejoin | Not defined | `[UNKNOWN]` |

`[DECISION REQUIRED]` Team Membership state vocabulary and whether invitation is managed at Project or Team level must be approved before implementation.

## 5. Workspace FE/BE Architecture

### Target/design topology

```text
Browser
   ↓ /api/backend/*
Next.js BFF
   ↓ /api/v1/*
NestJS backend
   ↓
Workspace domain + MongoDB source of truth
```

`[DESIGN]` SPEC-004 defines Browser → Next.js BFF → NestJS Monolith and cookie/request-ID propagation.

### Current source topology

`[IMPLEMENTED]` The frontend contains a catch-all Route Handler at `DATN-FE/src/app/api/backend/[...path]/route.ts`, a BFF helper at `DATN-FE/src/lib/bff-proxy.ts`, and an API client at `DATN-FE/src/lib/api-client.ts`.

`[FACT]` The BFF forwards `accept`, `authorization`, `content-type`, `cookie` and `x-request-id`, generating a request ID when missing. Browser API calls use `/api/backend`; server calls default to `http://localhost:3001/api/v1`.

`[GAP]` A generic BFF route does not prove that Workspace endpoints exist. The backend Gateway/domain controllers currently expose health behavior only.

## 6. API Contract Map

| Business Action | FE | BFF | Backend | Status |
|---|---|---|---|---|
| List Projects | No dedicated page/hook found | Generic catch-all can forward | No Project route | `[GAP]` |
| Project detail | No dedicated page/hook found | Generic catch-all can forward | No Project route | `[GAP]` |
| Create Project | No verified form/hook | Generic catch-all can forward | No Project route | `[GAP]` |
| Update Project | No verified flow | Generic catch-all can forward | No Project route | `[GAP]` |
| Archive Project | No verified flow | Generic catch-all can forward | No Project route | `[GAP]` |
| List Project Members | No dedicated hook/page | Generic catch-all can forward | No Membership route | `[GAP]` |
| Add Project Member | No verified action | Generic catch-all can forward | No Membership route | `[GAP]` |
| Remove Project Member | No verified action | Generic catch-all can forward | No Membership route | `[GAP]` |
| Update Project Role | No verified action | Generic catch-all can forward | No role mutation route | `[GAP]` |
| List Teams | No dedicated page/hook | Generic catch-all can forward | No Team route | `[GAP]` |
| Team detail | No dedicated page/hook | Generic catch-all can forward | No Team route | `[GAP]` |
| Create Team | No verified form/hook | Generic catch-all can forward | No Team route | `[GAP]` |
| Update Team | No verified flow | Generic catch-all can forward | No Team route | `[GAP]` |
| Archive Team | No verified flow | Generic catch-all can forward | No Team route/status | `[GAP]` |
| List Team Members | No dedicated hook/page | Generic catch-all can forward | No Team Membership route | `[GAP]` |
| Add Team Member | No verified action | Generic catch-all can forward | No Team Membership route | `[GAP]` |
| Remove Team Member | No verified action | Generic catch-all can forward | No Team Membership route | `[GAP]` |

The documented target API surface is design evidence only. Exact endpoint names must be taken from the approved contract, not inferred from generic BFF forwarding.

## 7. Request / Response Findings

### Backend

`[GAP]` No Workspace DTOs, validators, controllers or response types were found in the current IAM source. Therefore the following are not established:

- create/update request fields;
- Project/Team/Membership response envelope;
- member representation and role representation;
- archive response;
- cursor/page pagination shape;
- filter and sort field names;
- optimistic concurrency/version behavior.

### Frontend

`[FACT]` The generic `apiClient` adds JSON content type, includes credentials and converts non-2xx responses into a generic JavaScript `Error` containing status/statusText/body text.

`[GAP]` No Workspace-specific TypeScript contract or hook was found that could prove alignment with the backend.

## 8. Error Contract Findings

`[DESIGN]` Leader/architecture materials mention standardized 401, 403, 409 and 422 handling.

`[FACT]` The current FE API client has generic non-2xx error handling; it does not establish Workspace-specific behavior.

`[GAP]` No backend Workspace endpoint exists to prove:

- unauthenticated vs unauthorized distinction;
- cross-scope denial;
- duplicate Project/Team code conflict;
- duplicate membership conflict;
- invalid parent relationship;
- archive-state conflict;
- validation payload shape.

## 9. Pagination / Filter / Sort

`[DESIGN]` Leader breakdown requires pagination, search/filter and sort for Project and User/Workspace surfaces.

`[UNKNOWN]` No Workspace implementation or API contract establishes:

- page-number versus cursor pagination;
- default page size;
- stable sort order;
- searchable fields;
- allowed filter values;
- behavior for archived resources;
- whether Team Members use pagination.

## 10. Backend Current State

| Area | Source | Status | Evidence |
|---|---|---|---|
| Team Membership schema | IAM Mongo schemas | `[PARTIAL]` | Fields and relationship IDs exist. |
| Team Membership index | IAM persistence | `[PARTIAL]` | Unique `(teamId, userId)` index declaration exists in source; runtime index creation and duplicate-write behavior are not verified. |
| Project prerequisite validation | IAM source | `[GAP]` | No service/guard validation. |
| Team scope validation | IAM source | `[GAP]` | No parent/scope enforcement. |
| Workspace controllers | IAM controller | `[GAP]` | Health-only controller. |
| Workspace services/repositories | IAM source | `[GAP]` | No business service/repository flow. |
| Authorization | Architecture gaps/source | `[GAP]` | No executable evaluator/guards. |
| Audit/outbox | Infrastructure files | `[PARTIAL]` | Generic services/schemas exist, no Workspace producers. |
| Backend tests | `DATN-BE/test`, source specs | `[GAP]` | No Workspace integration/E2E coverage. |

## 11. Frontend Current State

| Area | Source | Status | Evidence |
|---|---|---|---|
| Workspace routes/pages | `DATN-FE/src/app` | `[GAP]` | No Project/Team/Membership-specific page structure found. |
| Workspace hooks | `DATN-FE/src/lib/queries` | `[GAP]` | Existing hooks cover auth/capture/verification/backend health, not Workspace. |
| API client | `DATN-FE/src/lib/api-client.ts` | `[IMPLEMENTED]` | Generic browser/SSR boundary exists. |
| BFF | `DATN-FE/src/app/api/backend/[...path]/route.ts` | `[IMPLEMENTED]` | Catch-all forwarding exists. |
| activeProjectId | `DATN-FE/src/stores/client-state.ts` | `[IMPLEMENTED]` | Client selection state only. |
| Permission-aware UX | FE source | `[GAP]` | No verified Workspace permission hook/guard. |
| Loading/error/empty Workspace states | FE source | `[GAP]` | Generic components may exist, no Workspace flow uses them. |
| Workspace tests | FE test inventory | `[GAP]` | Store/API generic tests exist, not Workspace E2E. |

`[PARTIAL]` Generic API/query mutation scaffolding only: `DATN-FE/src/lib/queries/backend.ts` provides a generic mutation wrapper, and `DATN-FE/src/lib/queries/backend.spec.tsx` uses a mocked `/projects` mutation fixture. This does not prove a working Project endpoint or Workspace feature.

## 12. BFF Current State

`[IMPLEMENTED]`:

- catch-all methods include GET, HEAD, POST, PUT, PATCH and DELETE;
- query strings/path segments are forwarded by the helper;
- selected authentication/correlation headers are forwarded;
- Browser requests use `/api/backend`;
- SSR requests use `CONTINUUM_API_BASE_URL` and append `/api/v1` when needed.

`[PARTIAL/GAP]` compared with the documented BFF contract:

- current forwarding list is narrower than the design's broader user-agent/forwarded-for examples;
- current route does not prove the documented timeout/error mapping;
- no Workspace endpoint can currently succeed because backend business routes are absent;
- BFF forwarding does not replace backend authorization.

## 13. Permission / Security Findings

`[DESIGN]` Workspace authorization must resolve:

1. authenticated subject;
2. Organization context;
3. Project Membership;
4. Team Membership;
5. role/capability and delegated policy;
6. resource/source ACL where relevant;
7. explicit deny and cross-scope isolation.

`[DESIGN]` FE permission checks are UX-only. Security must be enforced in the backend before returning Workspace data or mutating Workspace state.

`[GAP]` Current source has no Workspace authorization guard, no Team Membership prerequisite check and no cross-project/team isolation E2E test.

## 14. Requirement → Evidence → Implementation → Gap

| Requirement | Evidence | Current implementation | Gap |
|---|---|---|---|
| Add Team Member | Leader breakdown; Team Membership schema | Schema only | No API, validation or FE action |
| Remove Team Member | Leader breakdown | Schema only | No removal rule/audit/UI |
| Project Member prerequisite | Leader rule | No backend check | Security/business invariant missing |
| Active Team Membership blocks Project removal | Leader rule | No command flow | Cross-domain validation missing |
| Team isolation | Product authorization docs | No guard | Cross-project/team leakage risk untested |
| Workspace pages | Leader breakdown | Generic dashboard/template only | Product UI missing |
| Workspace API contract | Architecture/API inventory | Generic BFF only | DTO/response/error missing |
| activeProjectId context | Zustand store | Client state exists | No server/URL/authz integration |
| Permission-aware UX | Authorization docs | No Workspace hook/guard | FE behavior missing |
| Audit | Audit schema/service | Generic scaffold | No Workspace event wiring |
| Testing | Leader breakdown | Health/generic tests | Workspace E2E and persistence tests missing |

## 15. FE / BE Mismatch

1. `[GAP]` FE has no actual Workspace pages/hooks while backend has no Workspace APIs.
2. `[PARTIAL]` BFF route and API client are technically present, but no Workspace business route exists behind them.
3. `[UNKNOWN]` No shared Project/Team/Membership request/response types exist.
4. `[UNKNOWN]` Error/pagination/filter/sort contract is not aligned because it is not defined by implemented endpoints.
5. `[GAP]` `activeProjectId` is client-only; no verified backend active context or access validation exists.
6. `[GAP]` Any future FE permission hiding would be UX only until backend guards are implemented.

## 16. UNKNOWN

- Exact Team Membership status and invitation model.
- Whether Team Membership has a role distinct from Project role.
- Whether changing Project role affects Team Membership.
- Whether Team Member removal affects knowledge ownership or handover assignments.
- Exact Workspace route naming and API versioning.
- Request/response DTOs and error envelope.
- Pagination/filter/sort behavior.
- Whether `activeProjectId` is URL state, session state, persisted client state or only a UI selection.
- Whether BFF or backend owns session refresh on Workspace calls.
- Whether Workspace updates use optimistic concurrency/version checks.

## 17. DECISION REQUIRED

1. Approve Team Membership state and invitation semantics.
2. Approve the invariant and transaction behavior for Project Membership removal while Team Membership is active.
3. Approve Project/Team/Membership API routes and DTOs.
4. Approve response, error, pagination, filter and sort contracts.
5. Approve active-project context behavior and its relation to authorization.
6. Approve BFF timeout/error/cookie propagation behavior for Workspace endpoints.
7. Approve backend authorization boundary and required cross-scope tests.

## 18. Dependencies

```text
Authentication
    ↓
Organization context
    ↓
Authorization
    ↓
Project
    ↓
Project Membership
    ↓
Team
    ↓
Team Membership
    ↓
Workspace FE/BE contract
```

This graph expresses business/data dependency, not an absolute implementation order.

## 19. Proposed Implementation Breakdown

Proposal only:

1. Freeze Team Membership state and Project prerequisite rules.
2. Freeze Workspace API/DTO/error/pagination/filter/sort contract.
3. Implement backend scope validation and authorization before exposing member data.
4. Implement Team Membership add/remove with Project Membership invariant and audit/outbox events.
5. Implement FE Workspace routes, pages, hooks, active-project behavior and explicit loading/empty/error states.
6. Connect the FE through the BFF only after backend endpoints exist.
7. Add cross-org/cross-project/cross-team denial tests and Workspace E2E flow.

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
- `docs/specs/SPEC-003-MODULAR-MONOLITH-RUNTIME.md`
- `docs/specs/SPEC-004-BFF-ROUTING-ARCHITECTURE.md`
- `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts`
- `DATN-BE/src/services/iam/infrastructure/persistence.ts`
- `DATN-BE/src/services/iam/controllers/iam.controller.ts`
- `DATN-BE/src/services/iam/application/iam.service.ts`
- `DATN-FE/src/app/api/backend/[...path]/route.ts`
- `DATN-FE/src/lib/bff-proxy.ts`
- `DATN-FE/src/lib/api-client.ts`
- `DATN-FE/src/stores/client-state.ts`
- `.sage/inventory/apis.md`
- `.sage/inventory/backend.md`
- `.sage/inventory/frontend.md`
- `.sage/inventory/tests.md`
