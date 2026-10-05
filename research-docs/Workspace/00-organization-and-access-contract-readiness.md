# Continuum AI — Organization and Workspace Access Contract Readiness

## Document status

- Status: **Cross-document alignment and decision register**; this document records the governance model confirmed on 2026-10-02 and does not approve remaining open product or architecture decisions.
- Product boundary: Continuum is the source of truth for workspace and task records. The accepted MVP centers on one software Project with multiple Teams; full self-service Organization administration and multi-Organization switching are not assumed MVP features.
- Audience: product owner, backend, frontend, database, AI/SAG, and handover implementers.
- This document is the index for cross-cutting Organization/Project/Team access decisions. Detailed source evidence remains in the linked research reports; accepted role vocabulary remains in [Actors, roles and permissions](../02_ACTORS_ROLES_AND_PERMISSIONS.md).
- [DATN-86 Organization Membership working contract](06-organization-membership-contract.md) reconciles the accepted four-state/context baseline with current IAM source and maps unresolved lifecycle/API decisions to DATN-229–234. It is pending human contract review and does not clear DATN-87/DATN-88 dependencies.
- [DATN-86 review worksheet](07-organization-membership-review-worksheet.md) supplies concrete invitation, transition, API and validation alternatives for DATN-231–234; all candidates remain proposals pending named authority decisions.

## 1. Purpose and conclusion

The governance hierarchy is now confirmed: `PLATFORM_OPERATOR` operates the platform and provisions Organizations; `ADMIN` administers one Organization; `TEAM_LEADER` manages only explicitly assigned Project/Team scope; `MEMBER` participates within membership and ACL. The documents are **not yet a complete implementation contract** for Organization lifecycle, membership transitions, scoped delegation, or the detailed permission matrix. The evidence reports correctly show implementation gaps, but proposals must remain distinct from accepted policy.

Use this document to:

- distinguish accepted product constraints, implementation evidence, proposals, and decisions still required;
- track decisions that affect more than one document or service;
- define the cross-document contract checks required before implementation starts;
- keep Project/Team use cases connected to task, Work Note, knowledge retrieval, and handover without copying their lifecycles.

The decision register below is an index, **not authority to decide**. A decision becomes accepted only after the product/architecture owner approves it and the owning specification, API contract, and schema are updated consistently.

## 2. Evidence and decision labels

| Label | Meaning |
|---|---|
| `[APPROVED BASELINE]` | Explicitly accepted product/architecture constraint already recorded in the canonical baseline. |
| `[FACT]` / `[IMPLEMENTED]` | What the cited source code, schema, contract, or document currently contains. This does not by itself make it the target behavior. |
| `[PROPOSED]` | A candidate use case or rule for review. Do not implement it as settled policy without approval. |
| `[DECISION REQUIRED]` | Product or architecture owner must choose and record one behavior. |
| `[IMPLEMENTATION GAP]` | Required or proposed behavior has no complete runtime/API/UI implementation yet. |

## 3. Source-of-truth map

| Topic | Owning document | What it owns | What it does not decide |
|---|---|---|---|
| Persistent role vocabulary and accepted high-level authorization baseline | [Actors, roles and permissions](../02_ACTORS_ROLES_AND_PERMISSIONS.md) | `ADMIN`, `TEAM_LEADER`, `MEMBER`; separate `PLATFORM_OPERATOR`; role vs. scoped assignment; approved high-level boundaries | Detailed endpoint-by-endpoint grants; unresolved membership transitions and delegation mechanics |
| Organization tenant/context evidence | [Organization Context research](../Governance/01-organization-context.md) and accepted backend DEC-016 | Current schema, transport, UI and runtime findings; Organization Membership and active-context rules | HTTP transport, invite lifecycle, or 403/404 policy |
| Authorization implementation evidence | [Role/Permission Authorization research](../Governance/02-role-permission-authorization.md) and [Evaluator baseline](../Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md) | Current implementation/API/FE gaps and technical findings | Permission matrix approval or product policy not present in source |
| Organization and workspace decision index | This document | Cross-document decisions, dependency order and implementation exit criteria | It cannot approve product policy by itself |
| Project/Team/Membership use cases | [Project, Team and Membership Use Cases](05-project-team-access-use-cases.md) | Proposed actors, scope, use cases, business flows and acceptance criteria | Persistence fields, endpoint paths, or decisions explicitly left open |
| Project, Project Membership, Team and Team Membership evidence | [Project Lifecycle](01-project-lifecycle.md), [Project Membership](02-project-membership.md), [Team Lifecycle](03-team-lifecycle.md), [Team Membership and Workspace contract](04-team-membership-workspace-fe-contract.md) | Existing model/API/UI evidence and gaps | Product approval merely because a field or recommendation appears in the report |
| Task lifecycle and task permissions | [Task Management Use Cases](../Internal-Work-Management/12-continuum-task-management-use-cases.md) and accepted task ADRs | Continuum Task API ownership, task lifecycle and task-to-workflow contracts | Project/Organization membership lifecycle |
| Storage model | [Database design index](../../database-design/README.md) and its schema documents | Persistence schema proposals/decisions | Authorization behavior not encoded by the schema |
| Product scope | [MVP Scope](../01_MVP_SCOPE.md) and [Graduation Project Specification](../Continuum_AI_Graduation_Project_Specification_v1.0.docx.md) | Product outcomes and MVP boundary | Missing endpoint or transition behavior not specified there |

When documents conflict, do not infer policy from a research report or a schema enum. Record the conflict here, ask the authorized owner, then update the owning baseline and its dependent contracts together.

## 4. Domain boundary and data ownership

### 4.1 Organization and workspace hierarchy

```text
Organization
└── Project
    ├── Project Membership ── User
    ├── Team
    │   └── Team Membership ── Project Member
    ├── Continuum Tasks ── owned by Continuum Task API
    ├── Work Notes and evidence ── Continuum-owned; taskId is optional
    ├── Knowledge/evidence eligible for SAG retrieval ── subject to approval and ACL
    └── Handover ── reads authorized Continuum tasks and approved knowledge
```

`[APPROVED BASELINE]` Organization is the tenant boundary; each Project belongs to one Organization and each Team belongs to one Project. Parent/child IDs must be checked by the backend. A selected ID in the browser is never authorization.

```text
CONTINUUM AI PLATFORM
├── PLATFORM_OPERATOR
│   ├── platform operations, Organization provisioning, first-ADMIN bootstrap, health/configuration
│   └── no default Organization-content access
└── ORGANIZATION
    ├── ADMIN: manages Users/membership, assigns roles/scopes, manages Organization
    │   └── no default confidential-content access
    └── PROJECT
        ├── TEAM_LEADER: manages only explicitly assigned Project/Team scope
        └── MEMBER: participates within active membership, scope and resource ACL
```

`[APPROVED BASELINE: confirmed 2026-10-02]` `PLATFORM_OPERATOR` is a platform-scoped operations actor, not an Organization role. It may provision Organizations, bootstrap the first Organization `ADMIN`, and monitor platform health/configuration. Platform authority alone grants no Organization Membership and no access to private Organization content. `ADMIN` administers its Organization but receives no default confidential-content access. `TEAM_LEADER` authority is limited to explicitly assigned Project/Team scope and cannot grant itself broader access. `MEMBER` access remains subject to membership, scope, and resource ACL.

`[APPROVED BASELINE: DEC-016]` `OrganizationMembership` is the authoritative relationship proving a User belongs to an Organization; an Organization-level `RoleAssignment` alone does not establish membership. Membership status vocabulary is `PENDING_INVITE`, `ACTIVE`, `SUSPENDED`, `REMOVED`; only `ACTIVE` establishes Organization Context. Zero active memberships means no context, one is selected automatically, and multiple require explicit selection. The backend validates any client-supplied Organization ID against the authenticated User's active membership. `ONBOARDING` and `OFFBOARDING` describe workflows, not Organization-context eligibility.

`[APPROVED BASELINE: Project Foundation]` Any authenticated User with active Organization Membership can create a Project in the trusted Organization; `ADMIN`, `TEAM_LEADER`, or `project.create` is not required for this operation. The new Project is `PRIVATE`, and creation atomically gives its creator an `ACTIVE` Project Membership and project-scoped `MEMBER` RoleAssignment. It does not make the creator a Team Leader, owner, or Team. The earlier grant-based Project-create rule is superseded only for Project creation; the grant schema is not removed by this decision.

`[APPROVED BASELINE]` Continuum is the task source of truth. Task data is accessed through the Continuum Task API and its service boundary; Work Note, Agent, and Handover consumers use the agreed API/event contract and do not access task collections directly. A Work Note may link to a task using an optional `taskId`. Only eligible, permitted Work Note/evidence enters SAG retrieval/index. Handover reads task state from Continuum and only exposes content permitted to the successor.

`[FACT / IMPLEMENTATION GAP]` The earlier source inventory describes a global User without direct `organizationId` and reports role/capability records as the available Organization links. That snapshot predates or does not yet implement the accepted DEC-016 `OrganizationMembership` contract. Update IAM schema/API and perform the approved historical backfill; do not continue treating RoleAssignment as the membership source.

### 4.2 Authorization layers

Every backend read, search, mutation, task request, and retrieval request must validate authenticated identity and active Organization Membership before evaluating the applicable role/scope and ACL. Keep the layers separate:

1. **Identity and Organization context** identify the authenticated User and resolve the Organization from active membership. The chosen Organization ID is context input, never authority by itself.
2. **Membership** determines whether the User has active access to the Organization/Project/Team scope, according to the approved state model.
3. **Role/capability/delegation** determines which management operations the actor may perform within that scope.
4. **Resource/source ACL** independently gates confidential task, note, evidence, knowledge, and handover content.
5. **Lifecycle and explicit deny** can reduce access and must be evaluated before the data is returned or sent to an AI component.

The frontend may hide or disable actions for usability, but the backend remains authoritative. An `ADMIN` role does not grant automatic read access to confidential Project content. A `TEAM_LEADER` role without a matching scope assignment does not grant access to every Project or Team.

## 5. Organization use-case candidates

The Organization lifecycle is not yet covered by a complete end-user use-case package. The catalogue separates accepted platform bootstrap/context rules from lifecycle details that remain proposals. Because the accepted MVP centers on one Project with multiple Teams, full self-service Organization administration is not assumed MVP scope.

| Candidate | Use case | Expected boundary | Status / decision needed |
|---|---|---|---|
| ORG-01 | Provision an Organization | `PLATFORM_OPERATOR` provisions the Organization and bootstraps its first `ADMIN`; audit provenance | `[APPROVED BASELINE]` Platform bootstrap is accepted; self-service Organization creation is not in the MVP model |
| ORG-02 | Resolve and select an accessible Organization | No active memberships means no context; one active membership resolves automatically; multiple active memberships require explicit selection validated by the backend | `[APPROVED BASELINE: DEC-016]` Selection rule is accepted; transport/session/UI details remain to be contracted |
| ORG-03 | View/update Organization settings | Read and change only approved metadata/settings within Organization scope | `[PROPOSED]` Define mutable settings and authorized actors; avoid exposing confidential Project content |
| ORG-04 | View Organization members | Search/list Users and membership metadata within Organization admin scope | `[PROPOSED]` Membership source is decided; visible fields/search contract and audit are not |
| ORG-05 | Add/invite a User to an Organization | Associate an eligible identity with an Organization and activate access only through a verified onboarding flow | `[PROPOSED / REVIEW]` Invite-only is proposed; decide invite/accept/resend/cancel, token expiry, and exact transition commands before building member management |
| ORG-06 | Change/suspend/remove Organization access | Revoke or reduce access, preserve audit/history, and resolve Project/Team/task/knowledge ownership | `[DECISION REQUIRED]` Define status transitions, session revocation, descendant membership handling, and responsibility transfer |
| ORG-07 | Grant/revoke an Organization capability | An authorized `ADMIN` manages only capabilities approved for Organization scope and records who, why, scope, and validity | `[DECISION REQUIRED]` Do not use `project.create` to gate Project creation. Existing grant schema/use outside that route requires a separate policy/API decision |
| ORG-08 | Assign/revoke persistent role | An authorized `ADMIN` assigns/removes one of the accepted persistent roles at the approved scope | `[DECISION REQUIRED]` Confirm role/scope assignment representation and lifecycle. Do not derive Organization Membership from RoleAssignment. |

Candidate operations must be split into precise actor, precondition, scope, success, denial/conflict, audit, and downstream effects before becoming build-ready use cases.

## 6. Cross-document decision register

“P0” means this decision blocks a safe, consistent implementation contract; “P1” means it blocks the corresponding lifecycle feature but not necessarily all Organization/Project read flows. Priority does not imply that a decision is already approved.

| ID | Decision / contract item | Status and evidence | Affected documents and contracts | Priority |
|---|---|---|---|---|
| DEC-ACCESS-01 | Which transport carries an Organization ID (session/JWT, header, route, or combination), and how is it integrity-protected? | `[DECISION REQUIRED]` Selection/validation behavior is settled by DEC-016; HTTP transport is not. | IAM OpenAPI, JWT/session, BFF forwarding, FE context state, all scoped APIs | P0 |
| DEC-ACCESS-02 | Contract the zero/one/multiple active-membership context selection in login, `/me`, session and UI flows. | `[APPROVED BEHAVIOR / CONTRACT GAP]` DEC-016 accepts no context / auto-select one / explicit selection for multiple. | User/Organization response, session, FE switcher, API context | P0 |
| DEC-ORG-03 | Persist `OrganizationMembership` as the authoritative User–Organization relationship with unique `(organizationId, userId)` and accepted status vocabulary. | `[APPROVED BEHAVIOR / IMPLEMENTATION GAP]` Accepted in DEC-016; role assignment alone is insufficient. Historical backfill contract exists in BE decision. | IAM schema/API, DB design, backfill, user admin, auth context | P0 |
| DEC-ORG-04 | Platform provisioning and first-Admin bootstrap. | `[APPROVED BASELINE]` `PLATFORM_OPERATOR` provisions Organization and bootstraps first `ADMIN`; self-service Organization creation is outside the MVP model. | Platform operations, IAM setup/runbook, audit and least-privilege identity | P0 for initial deployment |
| DEC-ORG-05 | Invite-only member onboarding: invite/accept/resend/cancel, email verification and token expiry. | `[PROPOSED / REVIEW]` The supplied requirement proposes invite-only; exact API/expiry/transitions still require approval. | Auth/IAM API, Organization Membership, FE onboarding, notifications, audit | P0 before member-management implementation |
| DEC-ACCESS-06 | Align User account status, Organization Membership states and Project/Team Membership states/transitions. | `[PARTIAL]` Organization states `PENDING_INVITE`, `ACTIVE`, `SUSPENDED`, `REMOVED` are accepted; Project/Team state and transition behavior remains open. `ONBOARDING/OFFBOARDING` are workflows, not Organization-context eligibility. | IAM schema/APIs, Project/Team membership, session revocation, FE states, audit | P0 before membership mutations |
| DEC-WS-07 | Project creation authorization and creator bootstrap. | `[APPROVED BE DECISIONS]` Any authenticated User with active Organization Membership may create; the Project is private; creator receives active Project Membership + project-scoped `MEMBER`, not Team Leader/owner/Team. Writes and audit are atomic. | Actors/roles, Project use cases/API, schema, audit, SRS | `[RESOLVED POLICY]`; OpenAPI/schema alignment remains P0 |
| DEC-WS-08 | Represent Team Leader assignment scope and enforce Project-level vs Team-level delegation; decide whether one Project can have multiple Team Leaders. | `[PARTIAL]` Explicit Project/Team scope is approved; Project-level descendant delegation must be encoded, and Team-level scope does not imply sibling/whole-Project access. Leader cardinality remains open. | Role assignment schema, Team membership, authorization matrix, API/FE | P0 before Team authorization |
| DEC-ACCESS-09 | Approve exact action × actor × Organization/Project/Team/resource permission matrix, including admin and platform boundaries. | `[PARTIAL]` High-level hierarchy and confidentiality boundaries were confirmed 2026-10-02; detailed grants/delegations remain open. Project creation is allowed by active Organization Membership, not `project.create`. | Canonical matrix, guards/evaluator, OpenAPI, FE actions, acceptance tests | P0 before enforcement |
| DEC-ACCESS-10 | For authenticated inaccessible-resource requests, define 403 vs. 404 cases. | `[DECISION REQUIRED]` DEC-016 does not decide error concealment. | API errors, security tests, FE error handling | P0 before final API error contract |
| DEC-WS-11 | Resolve tasks, Work Notes, knowledge ownership, SME assignments and handover responsibilities on membership removal/offboarding. | `[PROPOSED / REVIEW]` Supplied requirement proposes transfer or unassignment with authorized reason; exact workflow remains open. | Project/Team membership, Task API, knowledge, handover, audit/outbox | P0 before removal/offboarding |
| DEC-WS-12 | Decide Project/Team archive/restore and descendant read/write effects. | `[DECISION REQUIRED]` Current schema/use cases do not settle the lifecycle. | Project/Team schema/API, Task/Work Note/SAG/Handover, FE | P1 before archive implementation |
| DEC-WS-13 | Decide whether Project/Team codes may change after creation. | `[DECISION REQUIRED]` Declared unique indexes exist; mutability is not specified. | API validation, references, audit, FE | P1 before update contract |
| DEC-ACCESS-14 | Publish canonical Organization/Project/Team/member/capability API paths, DTOs, pagination, filters, errors and audit events. Reconcile SRS example routes with backend OpenAPI. | `[IMPLEMENTATION CONTRACT GAP]` Existing IAM routes cover only part of the required flow; Task API and membership/assignment flows need reviewed OpenAPI. | BE OpenAPI, BFF, FE client/hooks, SRS, API review | P0 before cross-repository implementation |
| DEC-ACCESS-15 | Decide whether to retain, repurpose or deprecate the legacy `organization_capability_grants.project.create` value. It must not gate current Project creation. | `[DECISION REQUIRED / NOT A PROJECT-CREATE BLOCKER]` BE Project Foundation supersedes its use on Project create only; schema and other grant policies are not removed. | Capability schema/API, migration only if later approved, audit and docs | P1 |

Use the referenced local question numbers as pointers to detailed evidence. Once a decision is approved, record its decision date/owner and update all affected documents; remove it from the open list only after those updates are complete.

## 7. Mapping from use cases to runtime contracts

| Use-case family | Required backend contract | Required frontend/BFF behavior | Downstream consumers that must stay aligned |
|---|---|---|---|
| Organization context and membership | Resolve trusted Organization; validate actor association and lifecycle; return scoped Organization/member data | Load accessible Organizations; retain selected context; forward only approved context; handle 401/403/404 distinctly after policy approval | Project/Team APIs, Task API, Work Note, SAG retrieval, Handover |
| Project lifecycle and membership | Validate Organization parent, role/capability and Project state; enforce Project membership transitions; audit changes | Accessible Project list/detail, member list/actions, conflict and denied states | Task ownership, Work Note linkage, evidence ACL, knowledge ownership, Handover |
| Team lifecycle and membership | Validate `(organizationId, projectId, teamId)` relationship; require eligible Project membership; enforce scoped Team Leader assignment | Team list/detail/member actions within active Project context | Task team scope, knowledge/domain scope, successor routing |
| Role/capability management | One evaluator and authoritative assignment/grant model; explicit deny and expiration/revocation checks | Show actions according to returned capabilities for usability; backend still enforces each request | Project creation, membership management, AI retrieval and sensitive actions |
| Task management | Continuum Task API owns task lifecycle; enforce current user scope/ACL; expose approved API/event contract | FE accesses Task API through approved BFF/gateway path | Work Note optional `taskId`, Agent context, audit, Handover |
| Work Note and knowledge | Persist Work Notes in Continuum; enforce ACL before any indexing/retrieval; only permitted/approved evidence is indexed | Display provenance and permission-aware links | SAG retrieval/index, cited answers, knowledge review |
| Handover | Read current authorized task state and approved knowledge; record successor scope and decisions | Show a scoped handover package and completion state | Task API, knowledge, audit; no direct task database access |

No downstream service should query IAM, Project, Team, or Task collections directly to reconstruct authorization. Use an explicit service/API/event contract owned by the source domain.

## 8. Cross-cutting acceptance checks

The Organization/Workspace access package is ready to drive implementation only when the approved specs and API contracts allow reviewers to verify at least these scenarios:

1. A request without valid authentication is rejected as unauthenticated; an authenticated User without `ACTIVE` Organization Membership cannot establish Organization Context.
2. A caller cannot read or mutate an Organization, Project, Team, membership, task, note, or knowledge record by guessing its ID across a tenant or scope boundary.
3. Organization, Project, and Team identifiers in one request are checked against their actual parent-child relationship server-side.
4. Team Membership cannot grant effective access without the required eligible Project Membership.
5. Removing/suspending a parent membership cannot leave effective child access active; linked tasks and knowledge responsibilities follow the approved transfer workflow.
6. Any authenticated User with active Organization Membership can create a Project only in the trusted matching Organization; the Project is private and its creator atomically receives active Project Membership and project-scoped `MEMBER`, never implicit Team Leader/owner/Team rights.
7. A Team Leader cannot self-grant, act outside the assigned scope, or use the FE's selected context as authorization.
8. An `ADMIN` cannot read confidential content solely because of the persistent role; retrieval checks ACL before content reaches SAG/LLM.
9. Revoked/expired capability and membership changes affect subsequent API and retrieval requests according to the approved cache/session policy.
10. Membership, role, capability, Project and Team mutations record actor, Organization/scope, target, time, operation, and approved reason/changed fields without logging secrets or protected content bodies.
11. Task consumers use Continuum Task API/events; Work Notes may link with optional `taskId`; handover reads authorized tasks; none bypasses the source service boundary.
12. FE and BE use the same DTO/error/pagination contract; FE controls improve usability but cannot create an authorization bypass.

## 9. Recommended resolution and implementation order

1. Align IAM schema/API and FE/BFF context flow to accepted DEC-016; complete an auditable backfill from eligible Organization-level RoleAssignments.
2. Publish the Project create contract, including authenticated active Organization Membership, `PRIVATE` default, atomic Project Membership + project-scoped `MEMBER` bootstrap, and audit event.
3. Approve invite lifecycle, Project/Team membership transitions, Team Leader assignment representation, and detailed action/scope permission matrix.
4. Decide the inaccessible-resource error policy and legacy grant treatment; do not put `project.create` back in the Project-create gate.
5. Resolve removal/offboarding effects and archive policy (`DEC-WS-11/12`).
6. Publish one versioned OpenAPI/DTO/error/audit contract (`DEC-ACCESS-14`) and align database design with the approved domain decisions.
7. Implement and validate Organization context/authorization before Project/Team mutation flows; then implement Project, Project Membership, Team, and Team Membership flows.
8. Connect Task, Work Note, SAG retrieval, Agent, and Handover only through their approved APIs/events and run cross-service authorization scenarios.

This order is a dependency recommendation. It does not add a new database collection, endpoint, role, status, or permission code.

## 10. Related decisions and documents

- [MVP Scope](../01_MVP_SCOPE.md)
- [Actors, roles and permissions](../02_ACTORS_ROLES_AND_PERMISSIONS.md)
- [Organization Context research](../Governance/01-organization-context.md)
- [Role/Permission Authorization research](../Governance/02-role-permission-authorization.md)
- [Roles, Capabilities and Evaluator research](../Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md)
- [Project, Team and Membership Use Cases](05-project-team-access-use-cases.md)
- [Project Lifecycle research](01-project-lifecycle.md)
- [Project Membership research](02-project-membership.md)
- [Team Lifecycle research](03-team-lifecycle.md)
- [Team Membership and Workspace FE/BE contract research](04-team-membership-workspace-fe-contract.md)
- [Task Management Use Cases](../Internal-Work-Management/12-continuum-task-management-use-cases.md)
- [Database design index](../../database-design/README.md)
