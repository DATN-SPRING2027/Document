# CONTINUUM AI — Actors, roles and permissions

## Document status

- Status: Accepted MVP authorization baseline
- Date: 2026-09-18
- Scope: One software project with multiple teams; platform operations are separate from Organization membership and Project content access

## 1. Decision

The three persistent Organization/Project human roles are `ADMIN`, `TEAM_LEADER` and `MEMBER`. `PLATFORM_OPERATOR` is a separate platform-scoped operations actor; it is not an Organization role and does not grant Organization membership or content access. `SME` (Subject Matter Expert), `KNOWLEDGE_OWNER` and `SUCCESSOR` are scoped assignments, not persistent roles. `ONBOARDING` and `OFFBOARDING` describe workflows, not Organization-context eligibility. `PROJECT_MANAGER`, `PROJECT_ADMIN` and `TEAM_MEMBER` are superseded names and must not be used as new role codes.

An authenticated User with an `ACTIVE` Organization Membership may create a Project in that Organization when the trusted Organization Context matches. The role does not gate Project creation, and an `organization_capability_grants.project.create` grant is not required for that operation. This supersedes the earlier grant-based Project-create rule; it does not automatically remove or redesign the grant collection for other policy uses. On creation, the User receives an `ACTIVE` Project Membership and a project-scoped `MEMBER` assignment; the Project is `PRIVATE`. Creation does not make the creator a `TEAM_LEADER`, owner, or Team, and grants no access to other Projects. See the [Organization and Workspace Access Contract Readiness register](Workspace/00-organization-and-access-contract-readiness.md).

## 2. Scope and authorization

```text
CONTINUUM AI PLATFORM
├── PLATFORM_OPERATOR
│   └── provisions Organization / first ADMIN, operates health/config; no default Organization-content access
└── ORGANIZATION
    ├── ADMIN (manages Organization Users/membership, roles/scopes and Organization settings)
    │   └── no default confidential-content access
    └── PROJECT
        ├── TEAM_LEADER (manages only explicitly assigned Project/Team scope)
        └── MEMBER (acts within active membership, scope and ACL)
```

Effective access depends on active organization/project/team membership, persistent role, explicit capability grant, scoped assignment, resource/source ACL, lifecycle state, and explicit deny. **Deny takes precedence.** Authorization is enforced by NestJS before retrieval and again before passing a citation or snippet to the LLM. Client-side guards are only UX. No role or assignment automatically bypasses a confidential source ACL.

Role and assignment records need `organizationId`, subject, scope, `validFrom`, optional `validUntil`, `assignedBy` and audit reference. An expired/revoked grant has no effect. Cross-tenant or cross-project access must be explicitly authorized, not inferred from a matching email or title.

## 3. Human actors

### PLATFORM_OPERATOR

- Operates the Continuum platform, provisions Organizations, bootstraps the first Organization `ADMIN`, and monitors system health/configuration.
- Is not an Organization member by virtue of platform operations and receives no default access to private Organization, Project, task, Work Note, evidence, knowledge, or handover content.
- Must use a separately authorized Organization membership and role if also acting as an Organization user; platform authority alone is not an Organization content grant.

### ADMIN

- Manages users and Organization Memberships, assigns roles/scopes, and manages Organization settings and policies within that Organization.
- Does not automatically receive Project Membership, Team Leader scope, or read/verification access to confidential task, note, evidence, knowledge, or handover content.
- Does not need a special `project.create` grant for Project creation; any authenticated User with active Organization Membership may create a Project under the accepted Project Foundation decision.
- May inspect technical status and metadata; **does not automatically read confidential content or verify knowledge**. Exceptional access, if implemented, requires a separately approved, reasoned and audited process.

### TEAM_LEADER

- Manages assigned project/team workspaces, members and knowledge requirements within granted scope; tracks who owns each domain/module; follows up on missing updates and reviews handover.
- May create teams and invite/add members **within an existing project only if project policy permits**. May grant ordinary member access within their scope, never a role/capability broader than their delegation, and never override source ACL.
- Manages only the Project or Team scopes explicitly assigned. A Project-level assignment may manage child Teams only when that delegation is explicit; a Team-level assignment does not grant access to sibling Teams or all Project content.
- Project creation does not make the creator a Team Leader; creator bootstrap grants only Project Membership and the `MEMBER` assignment.
- Can review/approve knowledge only within a policy-authorized team/domain scope and after evidence checks. Specialist verification should use an SME or Knowledge Owner assignment.

### MEMBER

- Contributes manual notes and documents, records what was done/how/why, maintains assigned knowledge, asks the assistant, flags gaps, and participates in transfer.
- Reads only resources permitted by active membership and ACL. Creating a note or uploading a source does not authorize self-verification or wider disclosure.

Every leader is also expected to contribute knowledge; contribution is not delegated solely to members.

## 4. Scoped assignments and lifecycle

| Assignment/state | Meaning | Permission effect |
| --- | --- | --- |
| `SME` | Expert for a specified domain/module/process/requirement and period | Can review/interview/verify claims **only in that scope**, subject to source ACL and approval policy. |
| `KNOWLEDGE_OWNER` | Accountable maintainer of a knowledge object or required knowledge area | Can maintain, request review, approve/reject or supersede in scope according to policy; does not gain all project data. |
| `SUCCESSOR` | Takes over a defined responsibility/handover package | Sees the approved package **and** only evidence allowed by its ACL; never inherits predecessor permissions. |
| `ONBOARDING` / `OFFBOARDING` | Membership lifecycle state | May narrow permitted actions or trigger checklists/reminders; neither is an RBAC role. |

Human review is required before AI-proposed knowledge becomes verified/active. The reviewer must be authorized for both the domain and evidence. A person should not approve their own sensitive proposal where separation of duties is required.

## 5. Permission matrix (baseline)

`Yes` always means “within active scope and ACL”; `Grant` means an explicit, audited capability/policy grant; `Assigned` means a matching scoped assignment.

| Action | PLATFORM_OPERATOR | ADMIN | TEAM_LEADER | MEMBER | Scoped assignment |
| --- | --- | --- | --- | --- |
| Provision Organization / bootstrap first Admin | Yes | No | No | No | No |
| Manage Organization users, membership, roles and settings | No by platform role alone | Yes, within Organization | No | No | No |
| Create Project | No by platform role alone | Yes with `ACTIVE` Organization Membership | Yes with `ACTIVE` Organization Membership | Yes with `ACTIVE` Organization Membership | No extra right; Organization Membership is required |
| Manage Project/Team configuration and membership | No by platform role alone | No by Organization Admin role alone; Organization role/scope administration does not itself grant Project/Team mutation or content rights | Explicit assigned Project/Team scope and approved action policy | No by role alone | No privilege beyond assignment/ACL |
| Assign persistent roles or Organization membership | No | Yes, within Organization policy | No | No | No |
| Create/view/update task | No by platform role alone | No by Organization role alone | Assigned Project/Team scope | May create in scope; may edit own/currently assigned task fields in scope | `SUCCESSOR` reads only handed-over tasks allowed by ACL |
| Assign/reassign task | No by platform role alone | No by Organization role alone | Assigned Project/Team scope; may assign only eligible members in that scope | May self-assign on create or leave unassigned; cannot assign another user | No; authorized Team Leader acts through Task API |
| Change task status / reopen DONE | No by platform role alone | No by Organization role alone | Assigned Project/Team scope | Current assignee under approved task policy | Only after explicit assignment and within current task ACL |
| Cancel task / read task history | No by platform role alone | No by Organization role alone | Assigned Project/Team scope | No cancel by role alone; history within readable task scope | History only for handed-over tasks allowed by ACL |
| Read confidential content / ask chat | No | No by Organization role alone | ACL and membership required | ACL and membership required | Only matching assignment and ACL |
| See audit | Platform operational metadata only | Organization security scope | Assigned Project/Team scope | Own activity where policy allows | No extra right |

All Organization/Project operations also require a valid Organization Context and the corresponding active membership. `PLATFORM_OPERATOR` is not a bypass for Organization ACL. Project/Team administration actions beyond this high-level boundary still require the approved detailed permission matrix.

## 6. Permission codes and enforcement

Task action codes proposed for the Use Case review: `task.create`, `task.read`, `task.update_own`, `task.status.change`, `task.assign`, `task.cancel`, `task.history.read`. Here `task.update_own` means a MEMBER may edit a task they created or are currently assigned; a TEAM_LEADER acts within their granted Project/Team scope. Final codes and matrix remain subject to approval; every read/write/search/history request must pass Continuum Task API Organization Membership, Project/Team scope and resource ACL. A task belongs to one Project and at most one Team in the proposed MVP model. There is no Jira sync permission in the MVP.

The proposed task rule is deliberately narrower than project membership: a `MEMBER` may create a task, self-assign or leave it unassigned, and update fields only when they created or currently own the task; a `TEAM_LEADER` may manage and assign tasks in their granted scope. Only `TEAM_LEADER` may assign/reassign another user or cancel a task. The task’s current assignee or scoped Team Leader may update its status; a `DONE` task reopens to `IN_PROGRESS` with a reason. `CANCELLED` is terminal in the MVP. These are recommendations pending approval in [Task-management Use Cases](Internal-Work-Management/12-continuum-task-management-use-cases.md), not new persistent roles or blanket ADMIN access.

Organization context is established by an `ACTIVE` Organization Membership, not by a RoleAssignment alone. The Organization Membership decision defines context selection: none means no context, one active membership is selected automatically, and multiple active memberships require explicit selection validated by the backend. The transport for that selection remains an API/session contract detail. Do not gate Project creation on the legacy `project.create` grant; enforce authenticated active subject, matching trusted context, and active Organization Membership. Project/Team management and content access still require scoped role/assignment plus resource ACL. Permission changes invalidate affected sessions/caches as policy requires.

## 7. System actors and audit

`PLATFORM_OPERATOR` is a platform operations actor, not a fourth Organization role. The AI orchestrator, Task Agent integration, ingestion worker and scheduler use separate least-privilege service identities. A Task Agent can request only task context authorized for the initiating user, then return a draft/proposal through the Task API; it cannot read the Task database directly or commit a task mutation without a permitted human's confirmation. Agents may parse, index, draft, suggest or remind, but may not grant access, verify organizational truth, or impersonate a human reviewer. Any future external-source content is untrusted input and requires separately approved scope and ACL handling.

Audit at least: Organization provisioning and first-Admin bootstrap; membership/role/assignment changes; any retained capability grants and revocations; Project creation and atomic creator bootstrap; Team changes; approved source-connection failures; upload/source ACL changes; task ownership/status changes under the approved task scope; note edits; knowledge review/version changes; sensitive retrieval/chat access; handover approvals and waivers. Logs must avoid tokens, full prompts and document bodies. Missing daily notes trigger a follow-up, **not employee performance scoring**.

## 8. Scope exclusions

No enterprise-wide HR hierarchy, automatic disciplinary action, AI-controlled permission grants, automatic successor assignment, or blanket `ADMIN`/`PLATFORM_OPERATOR` access to confidential content in the 10-week MVP.

Project, Team and membership operations are detailed in the proposed [Project, Team and Membership Use Cases](Workspace/05-project-team-access-use-cases.md). This document remains the source of truth for persistent role vocabulary and the authorization baseline; the linked use-case proposal adds no roles and does not approve unresolved capability mappings.
