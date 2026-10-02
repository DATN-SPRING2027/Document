# Continuum AI — Project, Team and Membership Use Cases

## Document status

- Status: **Proposal for product review**; the use-case package and detailed lifecycle rules are not approved requirements yet.
- Product boundary: one software project with multiple teams for the MVP.
- Authorization baseline: the persistent Organization/Project roles are `ADMIN`, `TEAM_LEADER` and `MEMBER`. `PLATFORM_OPERATOR` is a separate platform-scoped actor. `SME`, `KNOWLEDGE_OWNER` and `SUCCESSOR` remain scoped assignments; `ONBOARDING` and `OFFBOARDING` describe workflows, not Organization-context eligibility.
- This document defines proposed Continuum use cases and their boundaries. It does not claim that the APIs, screens or workflows have been implemented, and it does not change database schemas or accepted architecture decisions.

## 1. Purpose and scope

Continuum needs a clear workspace boundary for organizing project work, members, teams, task ownership, Work Notes, knowledge and handover. Project and Team management must also provide the scope inputs used by backend authorization. A user interface selection is never proof of access.

This proposal covers:

- Project creation, discovery, details and lifecycle;
- Project member discovery and access lifecycle;
- Team creation, discovery and lifecycle;
- Team membership and scoped leadership;
- authorization, audit, validation and cross-document ownership.

Task lifecycle remains owned by the Continuum Task Management Use Cases. Knowledge review and handover remain owned by their respective workflows. This document defines the Project/Team scope those workflows consume; it does not duplicate their task, knowledge or handover actions.

## 2. Domain relationships and boundaries

```text
Organization
└── Project
    ├── Project Membership ── User
    ├── Team
    │   └── Team Membership ── Project Member
    ├── Tasks
    ├── Work Notes and evidence
    ├── Knowledge
    └── Handover packages
```

Rules for the boundary:

1. Each Project belongs to one Organization.
2. Each Team belongs to one Project and carries matching Organization scope.
3. A user must have eligible, active Project Membership before receiving Team Membership.
4. Project Membership grants entry into the Project scope; it does not by itself grant access to every confidential resource. Resource/source ACL still applies.
5. Team Membership narrows work and knowledge scope inside the Project; it does not create a separate tenant or bypass Project access.
6. Project, Team and membership records must retain provenance needed by existing tasks, Work Notes, knowledge and handover references. Hard deletion is not the default lifecycle operation.
7. Continuum services own and validate these records. No client or downstream service may treat a selected project/team identifier as authorization or access the underlying database directly.

## 3. Actors

| Actor | Relevant responsibilities | Limits |
|---|---|---|
| `PLATFORM_OPERATOR` | Provision Organizations, bootstrap the first Organization `ADMIN`, and operate system health/configuration. | Platform authority does not establish Organization Membership or grant access to Organization content. |
| `ADMIN` | Manage Organization Users/Memberships, assign permitted Organization roles/scopes, and manage Organization settings/policy. Any Project creation requires active Organization Membership, not an `ADMIN` role or `project.create` grant. | The role alone does not grant Project/Team membership, Project/Team management authority, or confidential content access. Project actions require a separate Project membership/scope path. |
| `TEAM_LEADER` | Manage only the Project/Team scopes explicitly assigned. Project-level delegation may include child Teams only when the assignment contract allows it. | Cannot self-grant or exceed assigned scope, cross into sibling Teams, or override a resource ACL. The role alone does not grant every Project. |
| `MEMBER` | View and contribute within active Organization and Project/Team membership and resource ACL; create a Project if their Organization Membership is active. | Cannot manage membership or grant another person access unless an approved policy explicitly delegates a narrow action. |
| Scoped assignee | `SME`, `KNOWLEDGE_OWNER` or `SUCCESSOR` may act on the matching resource and period. | An assignment grants only its stated scope; it is not a persistent role or blanket Project Membership. |

The role definitions and canonical permission baseline remain in [Actors, roles and permissions](../02_ACTORS_ROLES_AND_PERMISSIONS.md).

## 4. Authorization rules

Every read, search and mutation must first validate the authenticated subject's active Organization Membership and trusted Organization context, then evaluate scope and resource ACL. The decision must consider, as applicable:

1. active Organization Membership and Organization/Project identity, including whether parent-child relationships are valid;
2. Project lifecycle state;
3. active Organization, Project and Team membership;
4. persistent role and any explicit scoped capability/delegation;
5. the resource/source ACL for confidential content;
6. explicit deny, which takes precedence over an allow.

| Operation | `ADMIN` | `TEAM_LEADER` | `MEMBER` | Scoped assignment |
|---|---|---|---|---|
| Create Project | Yes if authenticated and Organization Membership is `ACTIVE` | Yes if authenticated and Organization Membership is `ACTIVE` | Yes if authenticated and Organization Membership is `ACTIVE` | Not applicable; scoped assignment is not needed |
| View Project metadata | No access by Organization role alone; separate Project Membership/scope required | Within assigned/delegated scope | Within active Project Membership | No extra right |
| Read Project content | No access by Organization role alone; separate Project Membership and resource ACL required | Only within assigned scope and resource ACL | Only within active scope and resource ACL | Only matching assigned resources and ACL |
| Update/archive Project | No access by Organization role alone | Only within explicit assigned Project scope and approved action policy | Not allowed by role alone | Not applicable |
| Manage Project/Team membership | Organization membership is separate; no Project/Team authority by `ADMIN` alone | Only within explicit assigned/delegated scope and approved action policy | Not allowed by role alone | Not applicable |
| Create/manage Team | No Project/Team authority by `ADMIN` alone | Only within explicit assigned/delegated Project scope and approved action policy | Not allowed by role alone | Not applicable |
| Assign Organization roles/scopes | Authorized `ADMIN` within Organization policy | Cannot grant or self-grant broader access | Cannot grant | Project/Team scope assignment follows its separately approved delegation contract |

The exact capability names for Project update/archive, membership management and Team management are **not approved** by this document. They must be aligned with the canonical permission matrix before implementation. The accepted Project Foundation decision allows Project creation to any authenticated User with active Organization Membership; `project.create` is not a gate for this operation.

## 5. Proposed use-case catalogue

All rows below are proposals. “MVP candidate” means a capability needed to operate the accepted Project-with-multiple-Teams scope, not proof of implementation or product approval of every edge case.

### Project lifecycle

| ID | Use case | Primary actor | Proposed rules and outcomes | Priority |
|---|---|---|---|---|
| UC-WS-01 | Create Project | Any authenticated User with `ACTIVE` Organization Membership | Create one `PRIVATE` Project in the trusted Organization with required name/code and optional description. No role or `project.create` grant is required. In the same transaction, create an `ACTIVE` Project Membership and project-scoped `MEMBER` RoleAssignment for the creator and record the existing `project.create` audit event with bootstrap IDs. Creator does not become Team Leader, owner, or Team. | MVP candidate; authorization/bootstrap decided, endpoint/schema alignment required |
| UC-WS-02 | List and select accessible Projects | All human actors with applicable scope | Return only Project metadata the actor may discover. Selecting a Project changes UI context only; every subsequent API request rechecks access. | MVP candidate |
| UC-WS-03 | View Project details | All human actors with applicable scope | Return permitted Project metadata. Confidential content is retrieved separately under its resource ACL. | MVP candidate |
| UC-WS-04 | Update Project details | `TEAM_LEADER` explicitly assigned to the Project, within approved scope | Update only approved mutable metadata. Whether `code` is mutable and which fields can change after creation require a product decision. Record actor, time and changed fields. `ADMIN` role alone is not sufficient. | MVP candidate; exact actions pending |
| UC-WS-05 | Archive Project | `TEAM_LEADER` explicitly assigned to the Project, if policy allows | Preserve task, note, evidence, knowledge and handover references; do not hard-delete. The write lock, residual read access and effect on child Teams and memberships must be defined before implementation. `ADMIN` role alone is not sufficient. | P1 / policy-dependent |
| UC-WS-06 | Restore archived Project | Explicitly scoped `TEAM_LEADER`, if supported | Restore only if an explicit restoration policy is approved. No restore behavior is assumed for the MVP. `ADMIN` role alone is not sufficient. | Later / decision required |

### Project membership and access

| ID | Use case | Primary actor | Proposed rules and outcomes | Priority |
|---|---|---|---|---|
| UC-WS-07 | View and search Project members | Scoped `TEAM_LEADER`; permitted Project members | List only members in the authorized Project scope. Organization Admin can manage the Organization directory but receives no Project membership details by role alone. | MVP candidate |
| UC-WS-08 | Add an eligible user to a Project | `TEAM_LEADER` explicitly assigned to the Project, if policy allows | Validate that the target user is eligible in the same Organization, the Project is usable, the actor is authorized and the membership does not already exist. The invitation/acceptance mechanism and canonical initial state remain open decisions. `ADMIN` role alone is not Project membership authority. | MVP candidate; transition pending |
| UC-WS-09 | Grant or revoke scoped access | `ADMIN` for approved Organization roles/scopes; authorized `TEAM_LEADER` only within explicit delegation | Change only an approved role, capability or scoped assignment. Do not model Project creation as a `project.create` grant. Policy for any retained legacy grant is separate. Never convert a Project membership record into an undocumented role store. Audit the grant/revocation and its scope. | MVP candidate; exact contract pending |
| UC-WS-10 | Remove or deactivate Project membership | `TEAM_LEADER` explicitly assigned to the Project, if policy allows | Revoke effective Project access while retaining historical references. Before completion, resolve active Team Memberships and owned tasks/knowledge/handover responsibilities according to approved transfer rules. The exact membership status transition is not decided here. Organization Admin manages Organization Membership separately. | MVP candidate; transition pending |

### Team lifecycle and membership

| ID | Use case | Primary actor | Proposed rules and outcomes | Priority |
|---|---|---|---|---|
| UC-WS-11 | Create Team | `TEAM_LEADER` explicitly assigned to the parent Project | Create a Team within one valid Project. Validate that Organization scope matches its parent Project and that its code is unique within the Project scope. Record the actor and audit event. Organization Admin role alone does not authorize Project/Team management. | MVP candidate |
| UC-WS-12 | List and view Teams | All actors with applicable Project/Team scope | Return only Teams under an accessible Project; Team discovery must not grant access to Team content. | MVP candidate |
| UC-WS-13 | Update Team details | `TEAM_LEADER` explicitly assigned to the parent Project/Team | Update approved metadata such as name, description and, if policy permits, code. Cross-Project moves are not part of the MVP candidate. Record changed fields and actor. Organization Admin role alone does not authorize the operation. | MVP candidate |
| UC-WS-14 | View and search Team members | Scoped `TEAM_LEADER`; permitted Project/Team members | Return members only for a Team inside the authorized Project. Organization Admin receives only Organization membership data by role alone. | MVP candidate |
| UC-WS-15 | Add a Project member to a Team | `TEAM_LEADER` explicitly assigned to the parent Project/Team, if policy allows | Require eligible Project Membership first; validate matching Organization, Project and Team IDs. A user who is not a member of the parent Project cannot be added to its Team. Audit the change. | MVP candidate |
| UC-WS-16 | Remove a Team member | `TEAM_LEADER` explicitly assigned to the parent Project/Team, if policy allows | Revoke Team-scoped access and preserve history. Resolve Team-owned responsibilities according to task, knowledge and handover rules; do not silently remove Project Membership. | MVP candidate |
| UC-WS-17 | Assign or change Team Leader scope | `ADMIN` within Organization role/scope policy; exact target scope contract pending | Assign an eligible person to a specific Team/Project scope. A `TEAM_LEADER` role code alone does not prove leadership of a particular Team. Define the authoritative representation, scope and audit record before implementation. | MVP candidate; representation pending |
| UC-WS-18 | Archive Team | `TEAM_LEADER` explicitly assigned to the parent Project/Team, if policy allows | Preserve references and membership history. Read/write behavior, restoration and effects on Project Membership must be approved first. The current Team schema does not establish an archive state. `ADMIN` role alone is not sufficient. | Later / decision required |

## 6. Core workflows

### 6.1 Create and initialize a Project

1. Authenticate the actor and resolve trusted Organization context from active Organization Membership.
2. Verify the actor has `ACTIVE` Organization Membership in the selected Organization. Do not require `ADMIN`, `TEAM_LEADER`, or `project.create` for the create operation.
3. Validate Project input and Organization-scoped code uniqueness.
4. In one transaction, create the `PRIVATE` Project, creator's `ACTIVE` Project Membership, project-scoped `MEMBER` RoleAssignment, and audit record with bootstrap references.
5. Do not create a Team or assign Team Leader/owner status as part of creator bootstrap. Project/Team leadership is assigned separately.
6. Create Teams within the Project, then add eligible Project members to each Team.

### 6.2 Add a person to a Team

1. Authorize the actor for Team membership management in that Project.
2. Verify that the Project and Team exist, are in an allowed lifecycle state and share the same Organization scope.
3. Verify the target user has eligible active Project Membership.
4. Apply the approved Team Membership state and uniqueness rule.
5. Emit an auditable membership change; subsequent resource requests still evaluate ACL.

### 6.3 Remove a person from a Project

1. Authorize the actor and identify the target Project Membership.
2. Find active Team Memberships and owned/open responsibilities that depend on that Project access.
3. Require explicit resolution of those dependencies before revoking Project access; do not leave active child access or silently orphan work.
4. Apply the approved inactive/removed transition, revoke effective access according to policy, retain history and audit the operation.

## 7. Cross-cutting business and security rules

- Project, Team and membership mutations must validate that all supplied IDs belong to the same Organization/Project path. Reject mismatched IDs; never trust FE-supplied scope alone.
- An active Team Membership requires an eligible Project Membership. Removing or deactivating the parent membership must not leave a child membership that still grants access.
- Permission changes must take effect for later requests and retrievals. Session/cache invalidation behavior must follow the approved authorization policy.
- `ADMIN` visibility of operational metadata does not imply read access to task descriptions, Work Notes, evidence, verified knowledge or confidential handover content.
- `TEAM_LEADER` can operate only in assigned/delegated scope. A role name without a scoped assignment is not sufficient evidence of access.
- `MEMBER` cannot add other people, change roles or grant access by default.
- `SUCCESSOR`, `SME` and `KNOWLEDGE_OWNER` gain only their explicit resource/assignment scope; they do not inherit all Project or predecessor rights.
- Project/Team/member changes and access grants/revocations require actor, timestamp, target, scope and changed-field audit data. Sensitive content bodies and credentials do not belong in audit logs.
- Frontend permission-aware controls improve usability but never replace backend authorization.
- Search, detail, task linkage, Work Note retrieval, SAG retrieval and handover must all enforce the same current scope and ACL; hiding a Project or Team in the UI is not sufficient.

## 8. Lifecycle recommendations requiring approval

These are proposed defaults to resolve the open questions in the Workspace research; they are not accepted schema or policy decisions:

| Topic | Recommended direction | Approval still needed |
|---|---|---|
| Project bootstrap | `[APPROVED BE DECISION]` Any authenticated User with active Organization Membership may create a private Project; atomically create active creator Project Membership and project-scoped `MEMBER` assignment. | Do not infer Team Leader, owner, or Team creation. Keep schema/OpenAPI aligned with the BE decision. |
| Member selection | Project/Team additions use Users with active Organization Membership; no separate Project/Team invite is assumed in the supplied MVP proposal. | Organization invite/accept/resend/cancel flow and invitation expiry remain for review. |
| Membership status | Organization Membership vocabulary is `PENDING_INVITE`, `ACTIVE`, `SUSPENDED`, `REMOVED` under DEC-016. Project Membership currently uses `ACTIVE`/`INACTIVE`; Team Membership state remains unspecified. | Approve Project/Team transitions and alignment with User account status and ONBOARDING/OFFBOARDING workflows. |
| Role representation | Keep membership lifecycle and role assignment separate. The creator's Project role is a project-scoped `MEMBER` assignment. | Confirm Team Leader assignment representation, scope and delegated actions. |
| Project removal | Resolve Team memberships and owned/open responsibilities before revocation; preserve records rather than hard-delete. | Whether removal is blocked, staged or performed as an explicit coordinated workflow. |
| Archive | Preserve child records and references. Recommend disabling new writes on archived scope while retaining read access only where policy/ACL permits. | Whether archive is MVP, how reads work, and whether child Team/membership states change. |
| Mutable identifiers | Recommend treating Project/Team codes as stable identifiers after creation when referenced by other records. | Whether code changes are ever allowed and how references remain stable. |

## 9. API and frontend contract boundaries

- This use-case document does not invent endpoint paths, DTO field names, error envelopes or pagination conventions. Those contracts must be defined once and shared by backend, BFF and frontend.
- Every command/read contract must carry or resolve Organization and Project scope from trusted server context, validate target relationships, and return only authorized fields.
- The frontend must support loading, success, empty and error states for Project, Team and membership lists/actions, and explain denied/unavailable operations without revealing protected data.
- The BFF/gateway forwards authenticated requests; backend policy remains the authorization boundary.
- No service may read/write Project, Team or membership collections directly outside their owning IAM/workspace API contract.

## 10. Acceptance criteria for this use-case package

Before these proposals become implementation requirements, reviewers should be able to confirm:

1. Each use case has an authorized actor, Organization/Project/Team scope, preconditions, successful outcome and denial/conflict outcome.
2. Project Membership is required before Team Membership; parent/child Organization and Project IDs are checked server-side.
3. Removing access does not silently preserve child access, orphan open responsibilities or erase referenced history.
4. Project list/search/detail never reveals out-of-scope metadata; content access independently enforces resource ACL.
5. An `ADMIN` cannot read confidential content solely because of the role; a `TEAM_LEADER` cannot self-grant or exceed delegation.
6. Membership, Team leadership and permission grants have one authoritative representation and auditable mutations.
7. Project/Team archive behavior and restoration policy are explicit before those operations are implemented.
8. Task-specific behavior continues to follow the Task Management Use Cases, while knowledge and handover retain their own lifecycle and authorization checks.

## 11. Open product decisions

The Organization-level dependencies and cross-document decision IDs are indexed in [Organization and Workspace Access Contract Readiness](00-organization-and-access-contract-readiness.md). The questions below retain the detailed Project/Team context; they are not approvals.

1. `[RESOLVED]` Project creation atomically creates a private Project, active Project Membership and project-scoped `MEMBER` assignment for the creator; it does not create a Team Leader, owner, or Team. Any authenticated User with active Organization Membership may create without `project.create`.
2. Which Project metadata can be changed, and is Project code immutable after creation?
3. Can an Admin view only Project operational metadata, or is any exceptional content access needed? If needed, what separately approved reasoned/audited process governs it?
4. Are MVP member operations limited to eligible Organization users, or must Project invitations and acceptance be implemented?
5. What are the canonical Project Membership states and transitions? How do `ONBOARDING`/`OFFBOARDING` relate to `ACTIVE`/`INACTIVE`?
6. Does Project Membership store only lifecycle status, while role/capability is authoritative in role assignments? Which operations may a delegated Team Leader perform?
7. How is Team Leader scope represented, and can a Team have one or multiple Team Leaders?
8. When a person leaves a Team or Project, how are open tasks, knowledge ownership, SME assignments and handover responsibilities reassigned or closed?
9. Does a Project Membership removal require prior Team Membership removal, or can one explicit workflow coordinate both changes?
10. Is Project archive part of the MVP? What happens to child Team membership, task writes, note/evidence access, knowledge retrieval and handover?
11. Does Team have an archive state? If so, is restoration supported and how does it affect Team Membership?
12. What shared API/DTO/error/pagination contract and active-Project context will FE, BFF and backend use?
13. Which membership, role, Team and Project audit event fields and retention policy are required?

## 12. Document ownership and mapping

| Concern | Owning document | Relationship to this proposal |
|---|---|---|
| Project use cases and lifecycle evidence | [Project Lifecycle research](01-project-lifecycle.md) | Provides source facts, implementation gaps and unresolved Project behavior. |
| Project member lifecycle evidence | [Project Membership research](02-project-membership.md) | Provides membership schema/state evidence and API/security gaps. |
| Team use cases and lifecycle evidence | [Team Lifecycle research](03-team-lifecycle.md) | Provides Team schema, parent-scope and lifecycle evidence. |
| Team membership and FE/BE contract evidence | [Team Membership and Workspace contract research](04-team-membership-workspace-fe-contract.md) | Provides membership/API/UI gap analysis. |
| Canonical human roles and permission rules | [Actors, roles and permissions](../02_ACTORS_ROLES_AND_PERMISSIONS.md) | Owns role vocabulary and accepted authorization baseline; this document adds no roles. |
| Organization lifecycle, context and cross-cutting decisions | [Organization and Workspace Access Contract Readiness](00-organization-and-access-contract-readiness.md) | Indexes Organization use-case candidates, implementation dependencies, and unresolved decisions spanning this package and IAM. |
| MVP required capability | [MVP Scope, Project and Team management](../01_MVP_SCOPE.md#61-project-and-team-management) | Defines the product-level multi-team Project boundary. |
| Task operations and handover linkage | [Task Management Use Cases](../Internal-Work-Management/12-continuum-task-management-use-cases.md) | Owns task lifecycle; task access consumes Project/Team authorization defined here. |
| Persistence contracts | [Workspace database design](../../database-design/README.md) and the relevant schema documents | Owns approved data model; this proposal does not alter collections, fields, indexes or references. |

The Workspace research files remain evidence/gap reports. This document is the proposed use-case entry point; unresolved decisions remain open until approved and must be synchronized into the role, API, schema, task, knowledge and handover documents before implementation.
