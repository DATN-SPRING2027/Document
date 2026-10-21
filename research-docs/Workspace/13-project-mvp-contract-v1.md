# Project MVP contract V1

**Status:** Owner-approved Project management contract for the current Project MVP.
**Decision date:** 2026-10-20.
**Decision authority:** Thang, Project owner, as stated in the workspace instructions and this task.
**Scope:** Project creation/bootstrap, metadata settings, visibility, Project Members, Project Leaders and tenant authorization.

This contract is the source of truth for Project management in this MVP. It supersedes conflicting Project creator/bootstrap and Project access statements in the older Workspace research snapshots and the 2026-10-02 Project Access decision, only for the behaviors defined here. It does not approve Team, task, note, knowledge, chat, AI or Platform Admin behavior.

## 1. Lifecycle and MVP boundary

Project records use `ACTIVE` and `ARCHIVED` states. A new Project is `ACTIVE` and `PRIVATE`. The MVP supports create, read, settings update, visibility change, member management and Project Leader management for active Projects.

Archive, restore and delete APIs and policy are **OUT OF MVP / FUTURE**. The existing `ARCHIVED` data state is not an archive workflow. Project list search and sort are **OUT OF MVP / FUTURE**; the current paginated list and status filter remain. Team runtime integration is **OUT OF SCOPE** for this Project MVP. A development preview does not represent a production Team capability.

## 2. Create and creator bootstrap

Any authenticated User with an `ACTIVE` Organization Membership may create a Project in the trusted matching Organization. No Organization role or `project.create` grant is required. Creation starts a `PRIVATE`, `ACTIVE` Project and, in the same transaction, creates:

1. an `ACTIVE` Project Membership for the creator;
2. a Project-scoped `TEAM_LEADER` RoleAssignment for the creator; and
3. the existing `project.create` audit event with bootstrap references.

All writes roll back together on failure. The creator is a Project Leader, not an Organization Admin, Project owner or Team Leader of any Team by implication. The Project Leader assignment remains bounded to that Project.

The current `TEAM_LEADER` Role must contain `project.read`, `project.members.list`, `project.members.add`, `project.members.remove`, `project.update` and `project.visibility.manage`. Missing, stale or ambiguous evidence fails closed. The additive permission provisioning migration already present on BE `main` is the provisioning mechanism; this contract does not request another migration or a live database apply.

## 3. Authorization matrix

Every tenant operation requires an active authenticated User and `ACTIVE` Organization Membership in the trusted Organization Context. A browser-provided organization or project ID is a selector, never authorization. The backend is authoritative; FE checks are presentation only.

| Operation | Required actor evidence | Exact permission / scope | Boundary |
|---|---|---|---|
| Read Project metadata | `ADMIN` at Organization scope, or active Project Membership with current Project `TEAM_LEADER`/`MEMBER` assignment and `project.read`; an active same-Organization member may also read `PUBLIC` metadata | Existing Project read policy | Cross-Organization reads are concealed as not found. `PUBLIC` means Project metadata only. `ADMIN` metadata access does not grant nested content access. |
| Edit name/description | Active Project Membership and current Project-scoped `TEAM_LEADER` assignment | `project.update` on that resolved Role | `ADMIN` does not gain this action from the role name or Organization scope. |
| Change visibility | Active Project Membership and current Project-scoped `TEAM_LEADER`, or Organization-scoped `ADMIN` with active Organization Membership | `project.visibility.manage` on the resolved Role at the corresponding scope | Active Projects only. Both `PRIVATE`↔`PUBLIC` directions are supported. Same-state requests conflict. |
| List/add/remove Project Members | Active Project Membership and current Project-scoped `TEAM_LEADER` | Exact `project.members.list`, `.add` or `.remove` | Organization `ADMIN` alone does not grant these actions. A Leader must be revoked before that user's Project Membership can be removed. |
| List/assign/change/revoke Project Leaders | Organization-scoped `ADMIN` with active Organization Membership (`project.leader.manage`); active Project `TEAM_LEADER` with `project.members.list` may read `GET /iam/projects/{projectId}/leaders` | `project.leader.manage` for Leader mutations and candidate search; `project.leader.manage` or Project-scoped `project.members.list` for Leader list projection | Project Leader role does not grant self-escalation, appointment or revocation authority. |

The FE may show an action only after its documented access projection succeeds, but every mutation is independently authorized by BE. Missing Role, RoleAssignment, permission, active Membership or tenant evidence denies the request.

## 4. Visibility and private access

- `PRIVATE` metadata is readable by active Project members with current `project.read` evidence and by Organization `ADMIN` within the same Organization under the existing operational metadata read policy.
- `PUBLIC` adds metadata reads for authenticated Users with an `ACTIVE` Organization Membership in that same Organization.
- Cross-Organization access is denied even for `PUBLIC` Projects.
- Visibility never grants access to member directories, Teams, tasks, Work Notes, evidence, knowledge or handover content. Each nested resource retains its own Project scope and ACL.
- Both visibility directions use the permission-backed, audited tenant visibility operation. Changing to `PRIVATE` removes metadata access that existed solely because the Project was public; cached Project reads are revalidated.

## 5. Project Members

Member addition follows `email search → select an eligible candidate → add the selected user`. Candidate search is a literal, case-insensitive email search restricted to active Users with active Organization Membership in the Project's Organization. Eligibility filters run before the 50-result cap. An omitted or blank search returns an empty list without enumerating the Organization directory. The result identifies whether the candidate already has Project Membership. The FE sends the selected candidate's opaque `userId`; it never asks the person to type an ObjectId.

Add creates or reactivates an ordinary Project `MEMBER` and requires `project.members.add`. A duplicate active membership conflicts. Remove requires `project.members.remove`, changes the existing Project Membership to `INACTIVE`, preserves history and emits the existing audit event. A current Project Leader must first be revoked by an Organization Admin; remove does not silently demote a Leader. Generic member role-change is **NOT MVP** and `project.members.role.change` remains disabled/unprovisioned.

## 6. Project Leaders

- An active Project supports **one or multiple** effective Project Leaders (`TEAM_LEADER`), where an effective Leader requires an `ACTIVE` User, `ACTIVE` Organization Membership, `ACTIVE` Project Membership, and a current Project-scoped `TEAM_LEADER` RoleAssignment. Revoking the last effective Project Leader is rejected with `409 LAST_PROJECT_LEADER_REQUIRED` unless a replacement Leader is appointed first or replaced atomically via `PUT /iam/projects/{projectId}/leaders`. Concurrent Leader revocations serialize through a transactional write fence on both the Project document and a surviving effective Leader's membership/assignment chain. If an active Project reaches `0` effective Project Leaders due to emergency User or Organization Membership suspension/removal, an Organization `ADMIN` (`project.leader.manage`) may recover the Project via `POST /iam/projects/{projectId}/leaders` by assigning any eligible active Organization Member, which atomically activates their Project Membership in the same transaction.
- Assign promotes an eligible existing active Project `MEMBER` to `TEAM_LEADER`; candidates must have an active User, Organization Membership and Project Membership in this exact Project. The same user cannot be assigned twice.
- Change replaces one Leader with an eligible existing active Project Member in one MongoDB transaction: the prior assignment becomes `MEMBER`, the replacement becomes `TEAM_LEADER`, both Project Memberships stay active, and no intermediate committed state is visible.
- Revoke changes that user's Project-scoped assignment to `MEMBER`, keeps the active Project Membership, and writes the audit event. Revoking a Project Leader is required before removing their Project Membership.
- Assign, change and revoke are Organization Admin operations with `project.leader.manage`. Project Leaders can view their own Project settings and manage members, but cannot appoint or revoke Leaders.
- Leader projections contain only `userId`, `fullName`, `email`, nullable `avatarUrl`, `role` and `status`. They never include authentication, password, token or private account fields. Leader candidate search uses email and returns only eligible active Project Members who are not already Leaders.

## 7. Tenant API contract

The canonical machine-readable API contract is BE's `docs/openapi/iam-v1.openapi.json`. FE browser calls go through the existing BFF `/api/backend/iam/...`; BE remains the authorization boundary.

| Method and path (BE API prefix omitted) | Purpose | Authorization |
|---|---|---|
| `POST /iam/projects` | Create a Project and atomically bootstrap creator Leader | Active Organization Membership and trusted context |
| `GET /iam/projects/{projectId}` | Read Project metadata | Existing scoped Project read policy |
| `PATCH /iam/projects/{projectId}` | Patch only supplied `name` and/or `description`; unknown fields are rejected; blank description may be cleared with `null` | Project-scoped `TEAM_LEADER` with `project.update` |
| `GET /iam/projects/{projectId}/settings-access` | Read-only `{ canUpdateProject: true }` signal; does not grant a later mutation | Same `project.update` policy as PATCH |
| `GET/PATCH /iam/projects/{projectId}/visibility` | Read-only permission signal and visibility transition | Project-scoped `TEAM_LEADER` or Organization-scoped `ADMIN`, each with `project.visibility.manage` |
| `GET /iam/projects/{projectId}/memberships` | Paginated member directory | Project `TEAM_LEADER` with `project.members.list` |
| `GET /iam/projects/{projectId}/member-candidates?email=...` | Search eligible Organization members by email | Project `TEAM_LEADER` with `project.members.add` |
| `POST /iam/projects/{projectId}/memberships` | Add selected candidate by `userId` | Project `TEAM_LEADER` with `project.members.add` |
| `DELETE /iam/projects/{projectId}/memberships/{membershipId}` | Deactivate one membership | Project `TEAM_LEADER` with `project.members.remove` |
| `GET /iam/projects/{projectId}/leaders` | Safe Leader projection | Organization `ADMIN` with `project.leader.manage` or Project `TEAM_LEADER` with `project.members.list` |
| `GET /iam/projects/{projectId}/leader-candidates?email=...` | Search eligible active Project Members for Leader appointment | Organization `ADMIN` with `project.leader.manage` |
| `POST /iam/projects/{projectId}/leaders` | Assign one eligible member | Organization `ADMIN` with `project.leader.manage` |
| `PUT /iam/projects/{projectId}/leaders` | Atomically replace one Leader | Organization `ADMIN` with `project.leader.manage` |
| `DELETE /iam/projects/{projectId}/leaders/{userId}` | Revoke one Leader | Organization `ADMIN` with `project.leader.manage` |

Requests reject malformed IDs, invalid values, unknown patch fields and unsupported transitions. Project codes are unique within an Organization; duplicate code returns `409 PROJECT_CODE_CONFLICT`. Project creation is not idempotent and accepts no idempotency key, so retrying after a lost success response can return that conflict instead of replaying the original result. Callers must reconcile the Project state before deciding whether to submit another create. Responses containing Project or member/Leader data use `Cache-Control: no-store`. Cross-Organization and hidden Project probes retain the existing concealed `404` behavior; authenticated authorization denial is `403`; validation is `422`; state/duplicate conflicts are `409`.

## 8. Cross-repository acceptance matrix

This table is the release gate. Source presence alone is not completion; runtime is unverified until the safe browser acceptance flow passes.

| Capability | Document | BE | OpenAPI | FE | Test |
|---|---|---|---|---|---|
| Create + Creator→Leader | This contract §2 | Atomic bootstrap | `POST /iam/projects` | Project create flow | BE transaction test; FE create behavior |
| Name/description | §3, §7 | `PATCH /iam/projects/{id}` | PATCH request/response | Settings form | BE validation/auth/audit; FE save/error/validation |
| Public/private | §4, §7 | Guarded visibility API | GET/PATCH visibility | Visibility panel | BE scope/visibility tests; FE response/error states |
| Members and email add/remove | §5, §7 | Membership and candidate APIs | Existing membership schemas | Member directory/add/remove flow | BE scope/duplicate/audit; FE candidate selection and mutation |
| Leader list/assign/change/revoke | §6, §7 | Leader and candidate APIs | Safe projection and mutation operations | Leader section and confirmation flows | BE authorization/transaction/audit; FE behavior |
| Cross-Organization/private boundary | §3–4 | Tenant filters and fail-closed authorization | Error semantics | BFF-only API calls | BE tests; browser runtime required for PASS |
