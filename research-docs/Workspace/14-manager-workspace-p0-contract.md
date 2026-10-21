# CONTINUUM AI — Manager Workspace P0 Specification & Forensic Resolution Contract

- **Status:** Accepted & Implemented across `DATN_BE`, `DATN_FE`, and `Document`
- **Date:** 2026-10-22 (Asia/Saigon)
- **Scope:** Organization Manager (`ADMIN`) P0 Governance Workspace, Permission Matrix, 6 P0 Screens, Membership & Leader State Transitions, API Contracts, and Resolved Forensic Findings (`F-01`..`F-08`, `F-11`)

---

## 1. Architectural Boundary: Where Manager (`ADMIN`) Sits in Continuum AI

```text
CONTINUUM AI PLATFORM
│
├── Admin (PLATFORM_OPERATOR)
│   ├── Platform Operations & Governance
│   ├── Provisions Organization & Bootstraps First Manager
│   └── Emergency User Suspension (`EMERGENCY_OVERRIDE` policy)
│
└── ORGANIZATION
    │
    ├── Manager (Technical Role Code: ADMIN)
    │   ├── Organization Overview & Governance KPIs
    │   ├── Organization Profile Settings (Allowlisted `name` & `description`)
    │   ├── Organization Membership Lifecycle (Active / Suspend / Reactivate / Remove)
    │   ├── Organization Invitations (Invite / Resend / Cancel / Atomic Accept)
    │   ├── Organization Role Assignment (`ADMIN` / `MEMBER` with Last-Manager Protection)
    │   ├── Projects Directory Governance (`activeMemberCount`, `effectiveLeaderCount`, Leaderless Alerts)
    │   └── Project Leader Appointment, Replacement, Revocation & Leaderless Project Recovery
    │
    └── PROJECT
        ├── Leader (Technical Role Code: TEAM_LEADER / DTO Alias: LEADER)
        │   ├── Daily Project Execution & Settings
        │   ├── Project Members & Teams Management
        │   └── Task & Handover Governance
        │
        └── Member (Technical Role Code: MEMBER)
            └── Contributes Tasks, Work Notes, Evidence & Knowledge within ACL
```

### 1.1. Role Vocabulary Rule (Persisted Code vs. UI Display Label)

| Persisted / API Technical Code | Scope | Frontend (`DATN_FE`) Display Label |
| --- | --- | --- |
| `PLATFORM_OPERATOR` | Platform (`platform_authority_assignments`) | **Admin** |
| `ADMIN` | Organization (`roles` & `role_assignments`, `projectId: null`) | **Manager** |
| `TEAM_LEADER` (DTO alias `LEADER`) | Project (`roles` & `role_assignments`, `projectId != null`) | **Leader** / **Leaders** |
| `MEMBER` | Organization & Project | **Member** |

> **Scope Separation Rule:** Organization Managers (`ADMIN`) govern the Organization (membership, roles, invitations, project metadata visibility, and Project Leader appointment/recovery). They do **not** manage daily task execution inside projects unless separately appointed as a Project `TEAM_LEADER`, and they do **not** automatically bypass confidential content ACLs.

---

## 2. Manager Workspace Requirements (`MGR-01` .. `MGR-12`)

| ID | Requirement | Priority | Runtime Status & Implementation Summary |
| --- | --- | --- | --- |
| `MGR-01` | View Organization Overview with real metrics | **P0** | Implemented via `GET /api/v1/iam/organizations/{organizationId}/overview` and `/dashboard` (`OrganizationOverviewDashboard`). Replaces legacy Ecommerce fixtures for Managers. |
| `MGR-02` | View and update allowlisted Organization Settings | **P0** | Implemented via `GET` & `PATCH /api/v1/iam/organizations/{organizationId}/settings` and `/organization/settings` (`OrganizationSettingsManager`). Allowlists `name` and `description` with `expectedUpdatedAt` CAS; `slug`, `plan`, and `status` remain Platform-governed read-only fields. |
| `MGR-03` | View, search, and filter Organization Members | **P0** | Implemented via `GET /api/v1/iam/organizations/{organizationId}/memberships` and `/organization/members` (`OrganizationMembershipManager`). |
| `MGR-04` | Invite and manage Organization Invitations | **P0** | Implemented via `POST/GET /invitations`, `/resend`, `/cancel`, and recipient `/accept` (`F-07` atomic `ACTIVE` membership + `MEMBER` role assignment). |
| `MGR-05` | Manage Organization Membership states (`ACTIVE`, `SUSPENDED`, `REMOVED`) | **P0** | Implemented via `/suspend`, `/resume` (Reactivate), and `/remove` with Last-Manager protection and Active Project Leader dependency check (`MEMBER_HAS_ACTIVE_PROJECT_LEADERSHIP`). |
| `MGR-06` | Assign and revoke Organization Roles (`ADMIN` / `MEMBER`) | **P0** | Implemented via `POST /api/v1/iam/organizations/{organizationId}/memberships/{membershipId}/role` with `expectedMembershipVersion`, `expectedRoleVersion`, required `reason`, and shared write fence. |
| `MGR-07` | Govern Organization Projects Directory & visibility | **P0** | Implemented via `GET /api/v1/iam/projects` returning `activeMemberCount`, `effectiveLeaderCount`, and `leaders` summary, with `0 Effective Leaders` badge and filter in `/projects`. |
| `MGR-08` | Appoint, replace, and revoke Project Leaders (`TEAM_LEADER`) | **P0** | Implemented via `/api/v1/iam/projects/{projectId}/leaders` (`POST`, `PUT`, `DELETE`) and `/projects/[projectId]/members` governance recovery workflow. |
| `MGR-09` | Last-Manager (`ADMIN`) & Last-Leader (`TEAM_LEADER`) Invariant Protection | **P0** | Enforced via MongoDB transactional shared write fences (`organization_role_fences` and Project document write lock) across all demotion, suspension, removal, and revocation paths (`F-01`, `F-02`, `F-03`). |
| `MGR-10` | Audit logging for all Organization & Project governance mutations | **P0** | All Manager mutations write transactional `continuum_audit.audit_logs_iam` records (`schemaVersion: 2`), including `PROJECT_DELETED` (`F-11`), `ORGANIZATION_SETTINGS_UPDATED`, `ORGANIZATION_MEMBERSHIP_RESUMED`, and `ORGANIZATION_MEMBERSHIP_REMOVED`. |
| `MGR-11` | Cross-Project Team & Workload Governance | **P1/P2** | Deferred to Project Leader scope (`TEAM_LEADER`); Manager only governs Project Leader appointment and recovery. |
| `MGR-12` | Organization Audit Explorer UI | **P1/P2** | Audit events are persisted in `continuum_audit.audit_logs_iam`; dedicated Organization Manager Audit Explorer UI is scheduled for P1 after filter/export contract sign-off. |

---

## 3. Permission Matrix (Manager Workspace P0)

| Capability / Operation | `PLATFORM_OPERATOR` (Admin) | `ADMIN` (Manager) | `TEAM_LEADER` (Leader) | `MEMBER` (Member) |
| --- | --- | --- | --- | --- |
| View Organization Overview (`GET /iam/organizations/:id/overview`) | No (Platform scope only) | **Yes** (`organization.memberships.read` / `org:read`) | No | No (sees Member Workspace Summary) |
| Read Organization Settings (`GET /iam/organizations/:id/settings`) | No | **Yes** (`organization.memberships.read` / `org:read`) | No | No |
| Update Organization Settings (`PATCH /iam/organizations/:id/settings`) | Platform Console only | **Yes** (`organization.memberships.manage` & `org:update`; allowlisted `name`, `description`) | No | No |
| List Organization Members & Invitations | Platform Console only | **Yes** (`organization.memberships.read`) | No | No |
| Invite / Resend / Cancel Invitation | No | **Yes** (`organization.memberships.manage`) | No | No |
| Suspend / Reactivate (`resume`) / Remove Member | Emergency user suspend only (`EMERGENCY_OVERRIDE`) | **Yes** (`organization.memberships.manage`; blocked on self & last Manager) | No | No |
| Change Organization Role (`ADMIN` $\leftrightarrow$ `MEMBER`) | No | **Yes** (`organization.memberships.manage`; blocked on self & last Manager) | No | No |
| View Projects Directory (`GET /iam/projects`) | Platform Console only | **Yes** (sees all active/archived org projects + `effectiveLeaderCount`) | **Yes** (visible projects) | **Yes** (visible projects) |
| Recover Leaderless Project (`0 Effective Leaders`) | No | **Yes** (may add member & appoint `TEAM_LEADER` without prior project membership) | N/A (0 Leaders) | No |
| Read Confidential Project Content (Tasks, Notes, Chat, Evidence) | No | **No** (requires explicit Project Membership & ACL) | **Yes** (in assigned Project/Team scope) | **Yes** (in assigned Project/Team scope) |

---

## 4. The 6 P0 Manager Workspace Screens (`DATN_FE`)

1. **Screen 01 — Organization Overview (`/dashboard`)**
   - Component: `src/components/organization-overview/OrganizationOverviewDashboard.tsx`
   - Displays Organization profile header (`@slug`, `plan`, `status`), 6 real KPI cards (`Active members`, `Pending invitations`, `Suspended members`, `Active projects`, `Archived projects`, `Projects missing Leader`), **Leaderless Projects Recovery Banner** (when `leaderlessProjectsCount > 0` with direct `Recover Leader` CTAs), **Active Organization Managers Roster** (with `Protected` badge and Last-Manager Protection notice when `managers.length === 1`), and **Quick Governance Navigation**.
2. **Screen 02 — Organization Settings (`/organization/settings`)**
   - Component: `src/components/organization-settings/OrganizationSettingsManager.tsx`
   - Allows Managers to edit allowlisted `name` (2–100 chars) and `description` (up to 500 chars) with `expectedUpdatedAt` optimistic concurrency control (`409 ORGANIZATION_VERSION_CONFLICT` recovery). Displays read-only Platform-governed fields (`slug`, `plan`, `status`, `createdAt`, `updatedAt`), Active Managers list, and Effective Manager Permissions.
3. **Screen 03 — Organization Members Management (`/organization/members`)**
   - Component: `src/components/organization-members/OrganizationMembershipManager.tsx`
   - Supports server-paginated directory, status filtering (`ALL`, `ACTIVE`, `SUSPENDED`, `PENDING_INVITE`, `REMOVED`), role change (`Manager` / `Member`), **Suspend**, **Reactivate (`resume`)**, and **Remove (`remove`)** with explicit handling for `409 LAST_ELIGIBLE_ADMIN` and `409 MEMBER_HAS_ACTIVE_PROJECT_LEADERSHIP`.
4. **Screen 04 — Organization Invitations (`/organization/members` — Invitations Tab)**
   - Component: `src/components/organization-members/OrganizationInvitationList.tsx` & `OrganizationInvitationCreateDialog.tsx`
   - Supports creating email-bound invitations (`MEMBER` or `ADMIN`), resending invitations (`SUPERSEDED` rotation), and cancelling pending invitations with versioned CAS (`expectedMembershipVersion: 0`, `expectedInvitationVersion`).
5. **Screen 05 — Projects Directory (`/projects`)**
   - Component: `src/components/projects/ProjectWorkspace.tsx` & `ProjectCard.tsx`
   - Displays `activeMemberCount`, `effectiveLeaderCount`, leader names, amber/red `0 Effective Leaders` warning badge on leaderless active projects, a **Leaderless Projects Alert Banner** with one-click filter (`Show Leaderless only`), and direct `Recover Leader` action linking to `/projects/[projectId]/members`.
6. **Screen 06 — Project Governance & Leader Management (`/projects/[projectId]/members`)**
   - Component: `src/components/projects/members/ProjectMembers.tsx` & `MemberDirectory.tsx`
   - Displays **Leaderless Project Governance Recovery Banner** when `effectiveLeaderCount === 0`, supports **Add & Appoint Leader** in one recovery flow for Organization Managers, highlights **Inactive Project Leaders** (`isEffective === false`, e.g., suspended Organization members) with a `Leader (Inactive)` badge, and allows revoking or replacing inactive leader assignments safely.

---

## 5. State Transitions & Dependency Rules

### 5.1. Organization Membership State Machine

```text
                  ┌──────────────────────────────────────┐
                  │         (Invitation Accept)          │
                  │   Creates ACTIVE Membership + Role   │
                  └──────────────────┬───────────────────┘
                                     ▼
                              ┌──────────────┐
               ┌─────────────►│    ACTIVE    ├─────────────┐
               │              └──────┬───────┘             │
       resume  │                     │ suspend             │ remove
  (Reactivate) │                     ▼                     │ (Checks Last Manager &
               │              ┌──────────────┐             │  Active Project Leader)
               └──────────────┤  SUSPENDED   ├─────────────┤
                              └──────────────┘             │
                                                           ▼
                                                    ┌──────────────┐
                                                    │   REMOVED    │
                                                    │  (Terminal)  │
                                                    └──────────────┘
```

- **Suspend (`ACTIVE -> SUSPENDED`):**
  - Blocks if target is actor (`403 MEMBERSHIP_SELF_ACTION_FORBIDDEN`) or last eligible Manager (`409 LAST_ELIGIBLE_ADMIN`).
  - Immediately revokes effective Organization and Project leadership authority without deleting historical records.
- **Reactivate / Resume (`SUSPENDED -> ACTIVE`):**
  - Requires `expectedMembershipVersion` CAS and `reasonCode` (`ACCESS_REQUEST` | `ACCESS_REVIEW` | `SECURITY_INCIDENT`).
  - Ensures the member has an active Organization `RoleAssignment` (restores default `MEMBER` assignment if none is active) and writes `ORGANIZATION_MEMBERSHIP_RESUMED` audit.
- **Remove (`ACTIVE | SUSPENDED -> REMOVED`):**
  - Blocks if target is actor (`403`) or last eligible Manager (`409 LAST_ELIGIBLE_ADMIN`).
  - Checks active Project leadership dependencies: if the target user is an active `TEAM_LEADER` in any `ACTIVE` Project of the Organization, rejects with `409 MEMBER_HAS_ACTIVE_PROJECT_LEADERSHIP` (details include `blockingProjectIds`) until a replacement Leader is appointed or the leader role is revoked.
  - Within the same MongoDB transaction: transitions Organization Membership to `REMOVED`, revokes active Organization `RoleAssignment`s, deactivates non-leader `ProjectMembership`s and `ProjectRoleAssignment`s in the Organization, and writes `ORGANIZATION_MEMBERSHIP_REMOVED` audit.

---

## 6. API Contracts Summary (New & Updated Endpoints)

| Method & Path | Auth & Permission | Request Body / Query | Response (`200 OK`) |
| --- | --- | --- | --- |
| `GET /api/v1/iam/organizations/:organizationId/overview` | Active Org Context + `organization.memberships.read` (or `org:read`) | — | `{ organization, metrics: { activeMembers, suspendedMembers, pendingInvitations, totalProjects, activeProjects, archivedProjects, leaderlessProjectsCount }, leaderlessProjects, managers }` |
| `GET /api/v1/iam/organizations/:organizationId/settings` | Active Org Context + `organization.memberships.read` (or `org:read`) | — | `{ organization, editableFields: ["name", "description"], managers, availablePermissions }` |
| `PATCH /api/v1/iam/organizations/:organizationId/settings` | Active Org Context + `organization.memberships.manage` & `org:update` + CSRF | `{ expectedUpdatedAt, name?, description? }` | Updated `OrganizationSettingsSummary` + `ORGANIZATION_SETTINGS_UPDATED` audit |
| `POST /api/v1/iam/organizations/:organizationId/memberships/:membershipId/resume` | Active Org Context + `organization.memberships.manage` + CSRF + `Idempotency-Key` | `{ expectedMembershipVersion, reasonCode }` | `{ operationId, membership: { id, organizationId, userId, status: "ACTIVE", version } }` |
| `POST /api/v1/iam/organizations/:organizationId/memberships/:membershipId/remove` | Active Org Context + `organization.memberships.manage` + CSRF + `Idempotency-Key` | `{ expectedMembershipVersion, reasonCode }` | `{ operationId, membership: { id, organizationId, userId, status: "REMOVED", version } }` |
| `GET /api/v1/iam/projects` | Active Org Context | `page`, `pageSize`, `status`, `visibility`, `search` | Paginated `ProjectSummaryDto` items enriched with `activeMemberCount`, `effectiveLeaderCount`, and `leaders` |

---

## 7. Resolved Forensic Audit Findings (`F-01` .. `F-08`, `F-11`)

| Finding ID | Severity | Description | Resolution in `DATN_BE` & `DATN_FE` |
| --- | --- | --- | --- |
| `F-01` | **P0 Critical** | Removing a Project Member (`DELETE /projects/:id/memberships/:membershipId`) did not check if the member was the last effective `TEAM_LEADER` and left orphan `role_assignments`. | Fixed in PR #83 & verified in `project.repository.ts`: `removeMember` acquires the Project write lock, verifies effective leaders (`ACTIVE` user + `ACTIVE` org membership + `ACTIVE` project membership + active `TEAM_LEADER` role), blocks removing the last effective leader (`409 PROJECT_LAST_LEADER_REQUIRED`), and atomically revokes project `role_assignments`. |
| `F-02` | **P0 Critical** | `revokeLeader` counted raw `role_assignments` instead of effective leaders and lacked a shared write fence against concurrent leader removals. | Fixed in PR #83 & verified in `project.repository.ts`: all leader mutations lock the Project document in the transaction and count only **effective** leaders (`isEffective: true`). |
| `F-03` | **P0 High** | Conflict between Last Manager (`ADMIN`) Protection and Platform Operator user suspension (`POST /platform/admin/users/:userId/suspend`). | Resolved in `platform-administration.service.ts`, `user-status-write.repository.ts`, and `suspend-platform-user.dto.ts`: normal Platform user suspension enforces Last-Manager protection (`409 USER_IS_LAST_ORGANIZATION_ADMIN`). Emergency suspension of a sole Manager requires explicit `reasonCode: "EMERGENCY_OVERRIDE"` and records `emergencyOverride: true` and `affectedSoleAdminOrganizationIds` in `continuum_audit.audit_logs_iam`. |
| `F-04` | **P1 High** | Suspending an Organization Member left their Project `TEAM_LEADER` assignments appearing active in UI without indicating loss of effective authority. | Resolved: `GET /iam/projects/:id/leaders` computes `isEffective` by verifying `ACTIVE` User + `ACTIVE` Organization Membership + `ACTIVE` Project Membership. `DATN_FE` displays `Leader (Inactive)` badges and `0 Effective Leaders` recovery banners. |
| `F-05` | **P1 High** | Organization Manager could not recover an `ACTIVE` Project that reached `0 Effective Leaders` without already being a Project Member. | Resolved: `ProjectPolicy` and `ProjectService` authorize Organization `ADMIN` (`Manager`) to add members and appoint/replace `TEAM_LEADER` on projects in their Organization without auto-granting confidential content read access. |
| `F-06` | **P1 Medium** | Concurrent Organization `ADMIN` role demotion and membership suspension could race under snapshot isolation if not sharing the same write fence. | Fixed in PR #82 & verified in `organization-membership-command.repository.ts`: all Organization `ADMIN` mutations (`suspend`, `remove`, `setRole`, `user-status-write`) touch the shared `organization_role_fences` document (`scopeKey: "ORG:<orgId>:ADMIN"`) inside the MongoDB transaction before counting eligible Managers. |
| `F-07` | **P0 Critical** | Accepting an Organization Invitation (`POST /auth/invitations/:id/accept`) created an `ACTIVE` `OrganizationMembership` but did **not** create an Organization `RoleAssignment`, leaving the accepted member with `roleCode: null` and 0 permissions. | Resolved in `organization-invitation.repository.ts`: `acceptInvitation` atomically resolves the invitation's allowlisted Organization role (`MEMBER` or `ADMIN`, defaulting to `MEMBER`), creates/ensures the active `RoleAssignment` document (`projectId: null`), updates `roleVersion`, and writes the `roleCode` in the transactional audit log. Idempotent retries preserve the exact result. |
| `F-08` | **P1 Medium** | Re-inviting or resuming a previously suspended/removed member could leave stale or missing Organization role assignments. | Resolved in `organization-membership-command.repository.ts`: `resumeMembership` ensures an active Organization `RoleAssignment` (`MEMBER` if none exists) and `removeMembership` cleanly revokes active Organization `RoleAssignment`s and cascades non-leader project memberships. |
| `F-11` | **P1 Medium** | Project soft-deletion (`deleteProject` in `project.repository.ts`) mutated `deletedAt` without writing an IAM audit log entry in the transaction. | Resolved in `project.repository.ts`: `deleteProject` now writes a transactional `PROJECT_DELETED` audit event to `continuum_audit.audit_logs_iam` with before/after state inside the same `ClientSession`. |
