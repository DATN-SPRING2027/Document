# Continuum AI — Project, Team and Membership Use Cases

## Document status

- Status: **Proposal for product review**; the use-case package and detailed lifecycle rules are not approved requirements yet.
- Product boundary: one software project with multiple teams for the MVP.
- Authorization baseline: the persistent human roles remain `ADMIN`, `TEAM_LEADER` and `MEMBER`. `SME`, `KNOWLEDGE_OWNER` and `SUCCESSOR` remain scoped assignments; `ONBOARDING` and `OFFBOARDING` remain lifecycle states.
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
| `ADMIN` | Manage organization users, Projects, Teams, membership and role/capability assignments according to organization policy; grant or revoke `project.create`; inspect permitted operational metadata. | The `ADMIN` role alone does not grant access to confidential task, note, evidence or knowledge content. |
| `TEAM_LEADER` | Manage assigned Project/Team workspace and its members when the relevant policy or delegation permits it; create a new Project only with an explicit organization-level `project.create` grant. | Cannot self-grant capabilities, assign broader access than delegated, cross the assigned scope or override a resource ACL. |
| `MEMBER` | View and contribute within active Project/Team membership and resource ACL. | Cannot manage membership or grant another person access unless an approved policy explicitly delegates a narrow action. |
| Scoped assignee | `SME`, `KNOWLEDGE_OWNER` or `SUCCESSOR` may act on the matching resource and period. | An assignment grants only its stated scope; it is not a persistent role or blanket Project Membership. |

The role definitions and canonical permission baseline remain in [Actors, roles and permissions](../02_ACTORS_ROLES_AND_PERMISSIONS.md).

## 4. Authorization rules

Every read, search and mutation must be authorized by the backend using the authenticated subject and trusted Organization context. The decision must consider, as applicable:

1. Organization and Project identity, and whether their relationship is valid;
2. Project lifecycle state;
3. active Organization, Project and Team membership;
4. persistent role and any explicit scoped capability/delegation;
5. the resource/source ACL for confidential content;
6. explicit deny, which takes precedence over an allow.

| Operation | `ADMIN` | `TEAM_LEADER` | `MEMBER` | Scoped assignment |
|---|---|---|---|---|
| Create Project | Allowed under Organization policy | Only with explicit `project.create` grant | Not allowed | Not applicable |
| View Project metadata | Within authorized Organization scope | Within assigned/delegated scope | Within active Project Membership | No extra right |
| Read Project content | Only when resource ACL allows | Only within assigned scope and resource ACL | Only within active scope and resource ACL | Only matching assigned resources and ACL |
| Update/archive Project | Under Organization policy | Only with explicit Project-management delegation | Not allowed | Not applicable |
| Manage Project/Team membership | Under Organization policy | Only within explicit assigned/delegated scope | Not allowed by default | Not applicable |
| Create/manage Team | Under Organization policy | Only within explicit assigned/delegated Project scope | Not allowed by default | Not applicable |
| Grant persistent role or `project.create` | Authorized `ADMIN` only | Cannot grant or self-grant | Cannot grant | Cannot grant |

The exact capability names for Project update/archive, membership management and Team management are **not approved** by this document. They must be aligned with the canonical permission matrix before implementation. `project.create` is already an explicit organization-level capability in the accepted authorization baseline.

## 5. Proposed use-case catalogue

All rows below are proposals. “MVP candidate” means a capability needed to operate the accepted Project-with-multiple-Teams scope, not proof of implementation or product approval of every edge case.

### Project lifecycle

| ID | Use case | Primary actor | Proposed rules and outcomes | Priority |
|---|---|---|---|---|
| UC-WS-01 | Create Project | `ADMIN`; `TEAM_LEADER` with `project.create` | Create one Project in the current Organization with required name/code and optional description. Enforce Organization scope and code uniqueness. Record the actor and audit event. Initial membership and leadership bootstrap must follow an approved policy; do not infer them solely from `createdBy`. | MVP candidate |
| UC-WS-02 | List and select accessible Projects | All human actors with applicable scope | Return only Project metadata the actor may discover. Selecting a Project changes UI context only; every subsequent API request rechecks access. | MVP candidate |
| UC-WS-03 | View Project details | All human actors with applicable scope | Return permitted Project metadata. Confidential content is retrieved separately under its resource ACL. | MVP candidate |
| UC-WS-04 | Update Project details | `ADMIN`; delegated `TEAM_LEADER` | Update only approved mutable metadata. Whether `code` is mutable and which fields can change after creation require a product decision. Record actor, time and changed fields. | MVP candidate |
| UC-WS-05 | Archive Project | `ADMIN`; delegated `TEAM_LEADER` | Preserve task, note, evidence, knowledge and handover references; do not hard-delete. The write lock, residual read access and effect on child Teams and memberships must be defined before implementation. | P1 / policy-dependent |
| UC-WS-06 | Restore archived Project | Authorized administrator, if supported | Restore only if an explicit restoration policy is approved. No restore behavior is assumed for the MVP. | Later / decision required |

### Project membership and access

| ID | Use case | Primary actor | Proposed rules and outcomes | Priority |
|---|---|---|---|---|
| UC-WS-07 | View and search Project members | `ADMIN`; scoped `TEAM_LEADER`; permitted Project members | List only members in the authorized Organization/Project scope. Search/filter must not expose users or membership details from another scope. | MVP candidate |
| UC-WS-08 | Add an eligible user to a Project | `ADMIN`; delegated `TEAM_LEADER` | Validate that the target user is eligible in the same Organization, the Project is usable, the actor is authorized and the membership does not already exist. The invitation/acceptance mechanism and canonical initial state remain open decisions. | MVP candidate |
| UC-WS-09 | Grant or revoke scoped access | `ADMIN`; delegated `TEAM_LEADER` only within the delegation ceiling | Change only an approved role, capability or scoped assignment. Persistent role grants and `project.create` remain Admin-controlled. Never convert a Project membership record into an undocumented role store. Audit the grant/revocation and its scope. | MVP candidate; exact contract pending |
| UC-WS-10 | Remove or deactivate Project membership | `ADMIN`; delegated `TEAM_LEADER` | Revoke effective Project access while retaining historical references. Before completion, resolve active Team Memberships and owned tasks/knowledge/handover responsibilities according to approved transfer rules. The exact membership status transition is not decided here. | MVP candidate; transition pending |

### Team lifecycle and membership

| ID | Use case | Primary actor | Proposed rules and outcomes | Priority |
|---|---|---|---|---|
| UC-WS-11 | Create Team | `ADMIN`; delegated `TEAM_LEADER` | Create a Team within one valid Project. Validate that Organization scope matches its parent Project and that its code is unique within the Project scope. Record the actor and audit event. | MVP candidate |
| UC-WS-12 | List and view Teams | All actors with applicable Project/Team scope | Return only Teams under an accessible Project; Team discovery must not grant access to Team content. | MVP candidate |
| UC-WS-13 | Update Team details | `ADMIN`; delegated `TEAM_LEADER` | Update approved metadata such as name, description and, if policy permits, code. Cross-Project moves are not part of the MVP candidate. Record changed fields and actor. | MVP candidate |
| UC-WS-14 | View and search Team members | `ADMIN`; scoped `TEAM_LEADER`; permitted Project members | Return members only for a Team inside the authorized Project. | MVP candidate |
| UC-WS-15 | Add a Project member to a Team | `ADMIN`; delegated `TEAM_LEADER` | Require eligible Project Membership first; validate matching Organization, Project and Team IDs. A user who is not a member of the parent Project cannot be added to its Team. Audit the change. | MVP candidate |
| UC-WS-16 | Remove a Team member | `ADMIN`; delegated `TEAM_LEADER` | Revoke Team-scoped access and preserve history. Resolve Team-owned responsibilities according to task, knowledge and handover rules; do not silently remove Project Membership. | MVP candidate |
| UC-WS-17 | Assign or change Team Leader scope | `ADMIN` | Assign an eligible person to lead a specific Team/Project scope. A `TEAM_LEADER` role code alone does not prove leadership of a particular Team. The authoritative representation and effect on other assignments require a decision. | MVP candidate; representation pending |
| UC-WS-18 | Archive Team | `ADMIN`; delegated `TEAM_LEADER` | Preserve references and membership history. Read/write behavior, restoration and effects on Project Membership must be approved first. The current Team schema does not establish an archive state. | Later / decision required |

## 6. Core workflows

### 6.1 Create and initialize a Project

1. Authenticate the actor and resolve trusted Organization context.
2. Check `ADMIN` authority or a valid, unexpired, non-revoked `project.create` grant for the `TEAM_LEADER`.
3. Validate required Project fields and Organization-scoped code uniqueness.
4. Create the Project and audit the actor and scope.
5. Apply the approved bootstrap policy to establish initial Project membership and Team leadership. This step is blocked on a product decision; creation must not silently imply owner/member/leader rights.
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
| Project bootstrap | Create the initial authorized Project membership and Team Leader scope as an explicit, audited bootstrap operation. | Whether the creator receives either assignment automatically and who is eligible. |
| Member selection | For the MVP, manage users already known to the Organization; use the existing identity/onboarding process when a person is not yet eligible. | Whether Project-specific invite, accept, resend and cancel flows are required. |
| Membership status | Keep role and lifecycle separate; define one canonical state transition model before changing the current persistence enum. | Mapping of `ACTIVE`/`INACTIVE` to onboarding, offboarding, suspension and removal. |
| Role representation | Use one authoritative assignment mechanism for persistent roles and scoped Team leadership; do not store a second competing role on membership. | Whether Team leadership is represented by scoped `role_assignments` or another approved assignment contract. |
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

1. Does Project creation automatically create the creator's Project Membership and Team Leader assignment? Which exact bootstrap actor/assignment is recorded?
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
| MVP required capability | [MVP Scope, Project and Team management](../01_MVP_SCOPE.md#61-project-and-team-management) | Defines the product-level multi-team Project boundary. |
| Task operations and handover linkage | [Task Management Use Cases](../Internal-Work-Management/12-continuum-task-management-use-cases.md) | Owns task lifecycle; task access consumes Project/Team authorization defined here. |
| Persistence contracts | [Workspace database design](../../database-design/README.md) and the relevant schema documents | Owns approved data model; this proposal does not alter collections, fields, indexes or references. |

The Workspace research files remain evidence/gap reports. This document is the proposed use-case entry point; unresolved decisions remain open until approved and must be synchronized into the role, API, schema, task, knowledge and handover documents before implementation.
