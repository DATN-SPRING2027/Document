# PLATFORM_OPERATOR V1 — Canonical contract

> **Cập nhật phạm vi quản lý người dùng — 2026-10-21:** Người dùng xác nhận dùng
> OpenAPI hiện tại của BE làm chuẩn cho task quản lý người dùng và đồng bộ tài liệu
> cũ. Với riêng tìm/xem tài khoản, sửa hồ sơ, đổi trạng thái, archive/restore,
> xem tổ chức và phiên đăng nhập, xem [hợp đồng và nghiệm thu hiện tại](platform-user-management-current.md).
> Các dòng DEFERRED và giới hạn “chỉ ba quyền” bên dưới là baseline lịch sử A-04,
> không mô tả trạng thái hiện tại của phạm vi này. Các phạm vi khác không được
> phê duyệt thêm bởi cập nhật này. Tên hiển thị Admin tương ứng PLATFORM_OPERATOR;
> quyền tổ chức ADMIN hiển thị Manager. Cấp quyền vẫn theo assignment chính xác.

| Field | Value |
|---|---|
| Status | Contract complete; only external approvals and deployed DB evidence remain |
| Jira | DATN-294; parent DATN-293; decision record DATN-301 |
| Reviewed | 2026-10-16 (Asia/Bangkok) |
| Authority baseline | DATN-79 / A-04 unchanged |
| Active permissions/operations | 3 existing A-04 codes/operations |
| Candidate inventory | 40 identifiers: 3 ACTIVE + 37 DEFERRED FROM V1 |

> Canonical source of truth for DATN-295–300. Active operations are PLAT-ORG-01, PLAT-HEALTH-01 and PLAT-AUDIT-01 with existing A-04 behavior unchanged. All other candidates are explicitly deferred. No runtime permission, API, UI, migration, or capability is added here.

## 1. Scope and precedence

This documentation task does not change DATN-79, runtime code, DB state, ACL, RAG, ingestion or configuration. This closure supersedes earlier draft wording that treated the 40-code inventory as an active/full-set runtime grant. The inventory remains traceable; the effective V1 grantable catalog is exactly the three current A-04 permissions. No wildcard, role hierarchy, Break-glass, tenant-content access, or implicit permission inheritance.

Labels: CONFIRMED = source evidence; DERIVED = follows from evidence and this explicit scope instruction; APPROVED = explicit V1 disposition; PROPOSED / EXTERNAL APPROVAL REQUIRED = complete package awaiting authority; DEFERRED FROM V1 = excluded from grant and implementation; UNVERIFIED = no target-environment evidence.

## 2. Current authorization baseline

| Item | Confirmed behavior |
|---|---|
| Runtime platform codes | organization.create, platform.health.read, platform.audit.read only |
| Assignment | One exact permission per subject, PLATFORM scope, ACTIVE/REVOKED, grant/revoke attribution, optional expiry |
| Authorization | Current ACTIVE user and exact current permission are checked; no wildcard/role expansion |
| Platform authentication | Separate PLATFORM context; login/refresh/protected requests revalidate authority |
| Organization provisioning | Existing route creates Organization + first ACTIVE ADMIN membership/role and audit in one Mongo transaction |
| Health | Existing route reports IAM process liveness only |
| Audit | Existing route returns fixed allowlisted projection capped at 100 |
| Access boundary | Platform authority grants no Organization role, Project ACL or tenant-content access |

Effective V1 catalog: organization.create, platform.health.read, platform.audit.read. Preserve existing standalone A-04 assignments/behavior; do not backfill, rewrite, revoke or silently adopt a row. A deferred code is not grantable. Reopening one requires new approval, full operation contract, implementation and QA oracle.

`PLATFORM_OPERATOR` is one conceptual actor with no V1 tiers. The existing A-04 guard resolves authority from the authenticated ACTIVE user's exact current PLATFORM assignment for each requested permission; it does not expand a role label, wildcard, or bundle. A fully provisioned V1 operator has all three active A-04 assignments, which are the complete effective Platform Administration V1 bundle. No other candidate permission is implied by the actor designation.

## 3. Permission matrix

The 40-row inventory is retained for traceability. Deferred actor/precondition/projection fields are candidate notes only and do not authorize implementation.

| Permission | Domain | Action | Resource | Scope | Actor | Preconditions | Data boundary | Audit | Error | Status | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `organization.create` | Organization | Create Organization + first ADMIN | new Organization | PLATFORM | Authenticated ACTIVE subject; exact current A-04 permission | Exact current A-04; active subject; provisioning invariants | Input and safe created metadata | Required, transactional | 201; 401/403; 422 validation; 409 ORGANIZATION_ADMIN_UNAVAILABLE / ORGANIZATION_SLUG_CONFLICT; preserve current A-04 behavior | ACTIVE — unchanged A-04 | DATN-79/A-04; current runtime |
| `platform.health.read` | Service | Read IAM liveness | service | PLATFORM | Authenticated ACTIVE subject; exact current A-04 permission | Exact current permission | Liveness only | No business read event; denial telemetry per §11 | 200; 401/403; preserve current A-04 behavior | ACTIVE — unchanged A-04 | DATN-79/A-04; current runtime |
| `platform.audit.read` | Audit | Read filtered projection | audit event | PLATFORM | Authenticated ACTIVE subject; exact current A-04 permission | Exact current permission; bounded filters | Existing allowlisted fields | No recursive business read event; denial telemetry per §11 | 200; 401/403; preserve current A-04 behavior | ACTIVE — unchanged A-04 | DATN-79/A-04; current runtime |
| `platform.dashboard.summary.read` | Dashboard | Read approved aggregate counters | aggregate | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Aggregates only | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.organizations.organization.read` | Organization | Read metadata | Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Allowlisted metadata | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.organizations.status.manage` | Organization | Suspend/reactivate | Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | State and safe result | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.organizations.usage.read` | Organization | Read usage/health counters | Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Aggregates only | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.users.account.read` | User | Read account metadata | User | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Safe identity/profile/state | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.users.profile.manage` | User | Update allowlisted profile fields | User | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Safe profile only | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.users.status.manage` | User | Suspend/reactivate | User | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | State/result | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.memberships.membership.read` | Membership | Read Organization membership | membership→Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Membership/role state | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.memberships.invitation.create` | Membership | Invite to Organization | Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Safe invite result; no token | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.memberships.lifecycle.manage` | Membership | Suspend/reactivate/remove | membership→Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Membership state | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.memberships.roles.manage` | Membership | Change Organization role | membership→Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Role metadata | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.projects.project.read` | Project | Read metadata | Project→Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Approved metadata only | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.projects.metadata.manage` | Project | Update allowlisted metadata | Project→Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Metadata only | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.projects.visibility.manage` | Project | Change visibility | Project→Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Visibility only | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.projects.members.manage` | Project | List/add/remove Project member | Project→Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | ACL metadata, no content | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.projects.leaders.manage` | Project | Assign/remove leader | Project→Organization | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Assignment metadata | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.sessions.session.read` | Security | Read session metadata | session→User | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Safe state/time/device; IP/UA unresolved | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.sessions.session.revoke` | Security | Revoke session | session→User | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Revocation result only | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.audit.event.export` | Audit | Export filtered audit events | event set | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | No secrets/raw events | Export log proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.services.health.read` | Service | Read approved service health | service | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Health only | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.services.metrics.read` | Service | Read approved metrics | aggregate | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Aggregates only | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.jobs.job.read` | Queue | Inspect job state/metadata | job→owner scope | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Operational metadata, no payload | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.jobs.job.retry` | Queue | Retry eligible job | job→owner scope | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | State/result ref | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.jobs.job.cancel` | Queue | Cancel cancellable job | job→owner scope | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | State/result | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.jobs.job.requeue` | Queue | Requeue eligible job | job→owner scope | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | State/result ref | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.rag.indexes.read` | RAG | Read index status | index→owner scope | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Index status only, no chunks | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.rag.indexes.rebuild` | RAG | Rebuild/reindex | index→owner scope | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Operation status | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.ai.runtime.read` | Laya | Read runtime/model status | runtime | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | No prompts/content | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.ai.runtime.manage` | Laya | Finite operational control | runtime | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Safe status/result | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.llm.providers.read` | LLM | Read provider/model status | provider | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Non-secret metadata | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.llm.providers.manage` | LLM | Finite provider operation | provider | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Redacted metadata | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.integrations.integration.read` | Integration | Read metadata/status | integration | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Non-secret metadata | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.integrations.integration.manage` | Integration | Enable/disable/reconnect | integration | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Redacted result | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.incidents.incident.read` | Incident | Read incident metadata | incident | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Operational metadata | Read logging proposed | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.incidents.incident.manage` | Incident | Create/update/resolve | incident | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Safe state/summary | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.diagnostics.record.read` | Diagnostics | Read bounded diagnostics | diagnostic ref | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Sanitized errors; no payload | Read logging requires Diagnostics/Security owner disposition | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |
| `platform.support.actions.manage` | Support | Finite support action | resolved target | PLATFORM | No active V1 actor; candidate only; not grantable | Not applicable while deferred | Safe result only | Required | D4 baseline in §11; per-operation stable code and concealment require owner approval | DEFERRED FROM V1 | PO-D02; no runtime permission/endpoint; see §4.3 |

Counts: 40 identifiers; 3 ACTIVE A-04 permissions; 37 DEFERRED; no added permission codes. Configuration has no V1 permission.

## 4. Operation registry

Only three A-04 operations are active. The detailed inventory retains exact candidate permission/domain/action/resource/scope/actor notes; deferred rows have no active runtime meaning.

### 4.1 Active operation contracts

| Operation ID | Permission | Domain | Action | Resource | Scope / target | Actor / authorization | Response projection | Preconditions / state / side effects / audit | Error | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `PLAT-ORG-01` | `organization.create` | Organization | create + first ADMIN | new Organization | PLATFORM / new Organization | Authenticated ACTIVE platform subject; exact A-04 permission; actor is not the first ADMIN; recipient is an existing ACTIVE User | Current response: `id`, `name`, `slug`, `plan`, `createdAt`, `updatedAt` | Input allowlist: name (trimmed, 1–200 chars), slug (trimmed/lowercased, 1–100 chars), plan (`FREE`/`ENTERPRISE`), 24-hex firstAdminUserId. One Mongo transaction creates Organization, first ACTIVE membership, ADMIN role assignment and audit event with actorUserId/action/targetResource/targetResourceId/metadata/occurredAt. Any failed write aborts all records. Same slug retry returns conflict. Current route defines no idempotency key or operationId. | 201 success; 401 auth; 403 permission; 422 invalid request; 409 `ORGANIZATION_ADMIN_UNAVAILABLE` or `ORGANIZATION_SLUG_CONFLICT`. No 404 target selector. Audit-store outage is not declared by current OpenAPI; D5 forbids success without durable audit. | ACTIVE — existing A-04 operation; unchanged |
| `PLAT-HEALTH-01` | `platform.health.read` | Service | IAM liveness | IAM process | PLATFORM / IAM process | Authenticated ACTIVE platform subject; exact current permission reloaded by the guard | Existing IAM response `{status: "ok"}` only | No request input; read-only; reports IAM handler liveness only, not MongoDB/Redis/BullMQ readiness; `Cache-Control: no-store`; no state change. Read/denial audit coverage is not approved. | 200 success; 401 auth; 403 permission. No target resource or concealment case. | ACTIVE — existing A-04 operation; unchanged |
| `PLAT-AUDIT-01` | `platform.audit.read` | Audit | operational metadata projection | fixed allowlisted event set | PLATFORM / fixed allowlisted event set | Authenticated ACTIVE platform subject; exact current permission reloaded by the guard | Up to 100 records, sorted `occurredAt DESC, _id DESC`; only `action`, `targetResource`, `targetResourceId`, `actorUserId`, `occurredAt`; allowlisted action set only | No request input/filter; read-only; `Cache-Control: no-store`; no export; no mutation. Read/denial audit coverage remains an owner decision. | 200 success; 401 auth; 403 permission. No target resource or concealment case. | ACTIVE — existing A-04 operation; unchanged |

### 4.2 Complete candidate operation list

| Operation ID | Permission | Domain | Action | Resource | Scope / target resolution | Actor / authorization | Data returned | Preconditions, state, side effect, audit, repeat/concurrency | Error | V1 status / owner gate |
|---|---|---|---|---|---|---|---|---|---|---|
| `PLAT-ORG-01` | `organization.create` | Organization | create + first ADMIN | new Organization | PLATFORM / new Organization | Authenticated ACTIVE platform subject; exact A-04 permission; actor is not the first ADMIN; recipient is an existing ACTIVE User | Current response: `id`, `name`, `slug`, `plan`, `createdAt`, `updatedAt` | Input allowlist: name (trimmed, 1–200 chars), slug (trimmed/lowercased, 1–100 chars), plan (`FREE`/`ENTERPRISE`), 24-hex firstAdminUserId. One Mongo transaction creates Organization, first ACTIVE membership, ADMIN role assignment and audit event with actorUserId/action/targetResource/targetResourceId/metadata/occurredAt. Any failed write aborts all records. Same slug retry returns conflict. Current route defines no idempotency key or operationId. | 201 success; 401 auth; 403 permission; 422 invalid request; 409 `ORGANIZATION_ADMIN_UNAVAILABLE` or `ORGANIZATION_SLUG_CONFLICT`. No 404 target selector. Audit-store outage is not declared by current OpenAPI; D5 forbids success without durable audit. | ACTIVE — existing A-04 operation; unchanged |
| `PLAT-HEALTH-01` | `platform.health.read` | Service | IAM liveness | IAM process | PLATFORM / IAM process | Authenticated ACTIVE platform subject; exact current permission reloaded by the guard | Existing IAM response `{status: "ok"}` only | No request input; read-only; reports IAM handler liveness only, not MongoDB/Redis/BullMQ readiness; `Cache-Control: no-store`; no state change. Read/denial audit coverage is not approved. | 200 success; 401 auth; 403 permission. No target resource or concealment case. | ACTIVE — existing A-04 operation; unchanged |
| `PLAT-AUDIT-01` | `platform.audit.read` | Audit | operational metadata projection | fixed allowlisted event set | PLATFORM / fixed allowlisted event set | Authenticated ACTIVE platform subject; exact current permission reloaded by the guard | Up to 100 records, sorted `occurredAt DESC, _id DESC`; only `action`, `targetResource`, `targetResourceId`, `actorUserId`, `occurredAt`; allowlisted action set only | No request input/filter; read-only; `Cache-Control: no-store`; no export; no mutation. Read/denial audit coverage remains an owner decision. | 200 success; 401 auth; 403 permission. No target resource or concealment case. | ACTIVE — existing A-04 operation; unchanged |
| `PLAT-DASH-01` | `platform.dashboard.summary.read` | Dashboard | approved summary | aggregate sources | PLATFORM / aggregate sources | No active V1 actor; candidate only; not authorized | Approved counters | Read; read log proposed | 401/403; unavailable-source code open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-ORG-02` | `platform.organizations.organization.read` | Organization | metadata read | server-resolved Org | PLATFORM / server-resolved Org | No active V1 actor; candidate only; not authorized | Allowlisted metadata | Read; read log proposed | 401/403; 404 policy open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-ORG-03` | `platform.organizations.status.manage` | Organization | suspend/reactivate | resolved Org | PLATFORM / resolved Org | No active V1 actor; candidate only; not authorized | State and safe result | Mutation; audit; idempotency + CAS; suspend can interrupt service | 401/403; conflict/stale codes open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-ORG-04` | `platform.organizations.usage.read` | Organization | usage read | resolved Org | PLATFORM / resolved Org | No active V1 actor; candidate only; not authorized | Aggregates | Read; read log proposed | 401/403; metric-source code open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-USER-01` | `platform.users.account.read` | User | metadata read | resolved User | PLATFORM / resolved User | No active V1 actor; candidate only; not authorized | Safe identity/profile/state | Read; read log proposed | 401/403; concealment per DEC-ACCESS-10 | DEFERRED FROM V1 — PO-D02 |
| `PLAT-USER-02` | `platform.users.profile.manage` | User | allowlisted profile update | resolved User | PLATFORM / resolved User | No active V1 actor; candidate only; not authorized | Safe updated profile | Mutation; audit + CAS; idempotency by field | 401/403; validation/stale codes open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-USER-03` | `platform.users.status.manage` | User | suspend/reactivate | resolved User | PLATFORM / resolved User | No active V1 actor; candidate only; not authorized | State/result | Mutation; audit + CAS/idempotency; may revoke access | 401/403; self/last-operator policy requires owner approval before any future activation | DEFERRED FROM V1 — PO-D02 |
| `PLAT-MEM-01` | `platform.memberships.membership.read` | Membership | read | membership→Org | PLATFORM / membership→Org | No active V1 actor; candidate only; not authorized | Membership/role/state metadata | Read; read log proposed | 401/403; concealment open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-MEM-02` | `platform.memberships.invitation.create` | Membership | invite | resolved Org | PLATFORM / resolved Org | No active V1 actor; candidate only; not authorized | Safe invite result, no token | Mutation; audit; idempotency required | 401/403; duplicate code open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-MEM-03` | `platform.memberships.lifecycle.manage` | Membership | suspend/reactivate/remove | membership→Org | PLATFORM / membership→Org | No active V1 actor; candidate only; not authorized | Membership state | Mutation; audit + CAS/idempotent; removal affects access | 401/403; C-02 conflicts and concealment open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-MEM-04` | `platform.memberships.roles.manage` | Membership | change role | membership→Org | PLATFORM / membership→Org | No active V1 actor; candidate only; not authorized | Role metadata | Mutation; audit + CAS/idempotent; may reduce access | 401/403; transition/conflict code open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-PROJ-01` | `platform.projects.project.read` | Project | metadata read | Project→Org | PLATFORM / Project→Org | No active V1 actor; candidate only; not authorized | Metadata only | Read; read log proposed | 401/403; no content implication | DEFERRED FROM V1 — PO-D02 |
| `PLAT-PROJ-02` | `platform.projects.metadata.manage` | Project | update allowlist | Project→Org | PLATFORM / Project→Org | No active V1 actor; candidate only; not authorized | Updated metadata | Mutation; audit + CAS; field idempotency | 401/403; validation/stale codes open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-PROJ-03` | `platform.projects.visibility.manage` | Project | visibility change | Project→Org | PLATFORM / Project→Org | No active V1 actor; candidate only; not authorized | Visibility only | Mutation; audit + CAS/idempotency; broadens metadata reach only | 401/403; invalid-state/conflict open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-PROJ-04` | `platform.projects.members.manage` | Project | list/add/remove member | Project + member resolved | PLATFORM / Project + member resolved | No active V1 actor; candidate only; not authorized | ACL metadata only | List read; add/remove audited + CAS/idempotent; removal affects access | 401/403; not applicable while deferred | DEFERRED FROM V1 — PO-D02 |
| `PLAT-PROJ-05` | `platform.projects.leaders.manage` | Project | assign/remove leader | Project + Org member | PLATFORM / Project + Org member | No active V1 actor; candidate only; not authorized | Assignment metadata | Mutation; audit + CAS/idempotent; changes authority | 401/403; invalid-state code open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-SEC-01` | `platform.sessions.session.read` | Session / Security | session metadata | session→User | PLATFORM / session→User | No active V1 actor; candidate only; not authorized | Safe state/time/device; IP/UA unresolved | Read; read log proposed | 401/403; hiding open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-SEC-02` | `platform.sessions.session.revoke` | Session / Security | revoke session | session→User | PLATFORM / session→User | No active V1 actor; candidate only; not authorized | Revocation result | Mutation; audit + CAS; idempotent repeat; invalidates session | 401/403; state/stale code open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-AUDIT-02` | `platform.audit.event.export` | Audit | export filtered events | same dataset as read | PLATFORM / same dataset as read | No active V1 actor; candidate only; not authorized | Same safe fields as read | Export; no mutation; export audit proposed | 401/403; size-limit error open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-SVC-01` | `platform.services.health.read` | Service | approved health | service registry | PLATFORM / service registry | No active V1 actor; candidate only; not authorized | Health state only | Read; read log proposed | 401/403; upstream code open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-SVC-02` | `platform.services.metrics.read` | Service | metrics | service + metric dimensions | PLATFORM / service + metric dimensions | No active V1 actor; candidate only; not authorized | Aggregates only | Read; read log proposed | 401/403; source error open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-JOB-01` | `platform.jobs.job.read` | Job / Queue | inspect job | job owner scope resolved | PLATFORM / job owner scope resolved | No active V1 actor; candidate only; not authorized | Operational metadata, no payload | Read; read log proposed | 401/403; concealment open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-JOB-02` | `platform.jobs.job.retry` | Job / Queue | retry job | job owner resolved | PLATFORM / job owner resolved | No active V1 actor; candidate only; not authorized | State/result ref | Mutation; audit + idempotency key + CAS; may repeat cost/side effects | 401/403; state/dependency code open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-JOB-03` | `platform.jobs.job.cancel` | Job / Queue | cancel job | job owner resolved | PLATFORM / job owner resolved | No active V1 actor; candidate only; not authorized | State/result | Mutation; audit + CAS; idempotent terminal state; stops work | 401/403; state/stale code open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-JOB-04` | `platform.jobs.job.requeue` | Job / Queue | requeue job | job owner resolved | PLATFORM / job owner resolved | No active V1 actor; candidate only; not authorized | State/result ref | Mutation; audit + key + CAS; schedules execution | 401/403; conflict/dependency code open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-RAG-01` | `platform.rag.indexes.read` | RAG | index status | index owner resolved | PLATFORM / index owner resolved | No active V1 actor; candidate only; not authorized | Status only, no chunks | Read; read log proposed | 401/403; hiding open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-RAG-02` | `platform.rag.indexes.rebuild` | RAG | rebuild index | index + source resolved | PLATFORM / index + source resolved | No active V1 actor; candidate only; not authorized | Operation status | Mutation; audit + job tracking + CAS; resource/cost impact | 401/403; state/dependency open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-AI-01` | `platform.ai.runtime.read` | Laya / AI | runtime status | registered runtime | PLATFORM / registered runtime | No active V1 actor; candidate only; not authorized | Status only; no prompts/content | Read; read log proposed | 401/403; authority integration absent | DEFERRED FROM V1 — PO-D02 |
| `PLAT-AI-02` | `platform.ai.runtime.manage` | Laya / AI | finite control | runtime resolved | PLATFORM / runtime resolved | No active V1 actor; candidate only; not authorized | Safe result/status | Mutation; audit; per-command idempotency; declare destructive effect | 401/403; command errors unapproved | DEFERRED FROM V1 — PO-D02 |
| `PLAT-LLM-01` | `platform.llm.providers.read` | LLM | provider status | provider catalogue | PLATFORM / provider catalogue | No active V1 actor; candidate only; not authorized | Non-secret metadata | Read; read log proposed | 401/403; provider error map open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-LLM-02` | `platform.llm.providers.manage` | LLM | finite provider operation | provider resolved | PLATFORM / provider resolved | No active V1 actor; candidate only; not authorized | Redacted metadata/result | Mutation; audit + CAS/idempotency; impact per action | 401/403; secret API absent | DEFERRED FROM V1 — PO-D02 |
| `PLAT-INT-01` | `platform.integrations.integration.read` | Integration | status | integration resolved | PLATFORM / integration resolved | No active V1 actor; candidate only; not authorized | Non-secret metadata | Read; read log proposed | 401/403; dependency map open | DEFERRED FROM V1 — PO-D02 |
| `PLAT-INT-02` | `platform.integrations.integration.manage` | Integration | enable/disable/reconnect | integration resolved | PLATFORM / integration resolved | No active V1 actor; candidate only; not authorized | Redacted result | Mutation; audit + CAS/idempotency; may interrupt delivery | 401/403; control/secret API absent | DEFERRED FROM V1 — PO-D02 |
| `PLAT-INC-01` | `platform.incidents.incident.read` | Incident | metadata read | incident resolved | PLATFORM / incident resolved | No active V1 actor; candidate only; not authorized | Operational metadata | Read; read log proposed | 401/403; source contract absent | DEFERRED FROM V1 — PO-D02 |
| `PLAT-INC-02` | `platform.incidents.incident.manage` | Incident | create/update/resolve | incident resolved | PLATFORM / incident resolved | No active V1 actor; candidate only; not authorized | Safe state/summary | Mutation; audit + CAS/idempotency; resolution workflow effect | 401/403; lifecycle codes unapproved | DEFERRED FROM V1 — PO-D02 |
| `PLAT-DIAG-01` | `platform.diagnostics.record.read` | Diagnostics | bounded diagnostics lookup | exact request/correlation/job/operation reference | PLATFORM / exact request/correlation/job/operation reference | No active V1 actor; candidate only; not authorized | Sanitized diagnostics only; no payload, prompt, content, token, secret, or host detail | Read only; read logging and exact field allowlist require Diagnostics/Security owner disposition | 401/403 baseline; 404 class and stable code require DEC-ACCESS-10/owner decision; dependency errors use D4 status mapping | DEFERRED FROM V1 — PO-D02 |
| `PLAT-SUP-01` | `platform.support.actions.manage` | Support | finite action | target and action resolved server-side | PLATFORM / target and action resolved server-side | No active V1 actor; candidate only; not authorized | Safe result only | Mutation; durable audit; per-action CAS/idempotency; destructive effect must be stated by the owner | 401/403 baseline; action catalogue, resource concealment and stable codes absent | DEFERRED FROM V1 — PO-D02 |


### 4.3 Final disposition for every operation

| Operation | Permission | Domain | Status | Reason | Owner | Evidence | Implementation impact |
|---|---|---|---|---|---|---|---|
| `PLAT-ORG-01` | `organization.create` | Organization | ACTIVE | Existing A-04 exact guard and implementation; preserve unchanged. | DATN-79/A-04 owner | DATN-79/A-04; current IAM policy/controller/repository/tests. | Keep route/permission/projection; no widening. |
| `PLAT-HEALTH-01` | `platform.health.read` | Service | ACTIVE | Existing A-04 exact guard and implementation; preserve unchanged. | DATN-79/A-04 owner | DATN-79/A-04; current IAM policy/controller/repository/tests. | Keep route/permission/projection; no widening. |
| `PLAT-AUDIT-01` | `platform.audit.read` | Audit | ACTIVE | Existing A-04 exact guard and implementation; preserve unchanged. | DATN-79/A-04 owner | DATN-79/A-04; current IAM policy/controller/repository/tests. | Keep route/permission/projection; no widening. |
| `PLAT-DASH-01` | `platform.dashboard.summary.read` | Dashboard | DEFERRED FROM V1 | No approved metric source or aggregate oracle; counters can expose tenant activity or misstate health. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-ORG-02` | `platform.organizations.organization.read` | Organization | DEFERRED FROM V1 | Organization metadata field allowlist is not approved. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-ORG-03` | `platform.organizations.status.manage` | Organization | DEFERRED FROM V1 | Current Organization schema has no lifecycle status. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-ORG-04` | `platform.organizations.usage.read` | Organization | DEFERRED FROM V1 | No authoritative usage-counter source. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-USER-01` | `platform.users.account.read` | User | DEFERRED FROM V1 | No safe field/lifecycle contract; identity/security data is sensitive and account changes affect access. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-USER-02` | `platform.users.profile.manage` | User | DEFERRED FROM V1 | No safe field/lifecycle contract; identity/security data is sensitive and account changes affect access. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-USER-03` | `platform.users.status.manage` | User | DEFERRED FROM V1 | No safe field/lifecycle contract; identity/security data is sensitive and account changes affect access. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-MEM-01` | `platform.memberships.membership.read` | Membership | DEFERRED FROM V1 | Could bypass or conflict with C-02; platform override of Organization authority is not approved. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-MEM-02` | `platform.memberships.invitation.create` | Membership | DEFERRED FROM V1 | Could bypass or conflict with C-02; platform override of Organization authority is not approved. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-MEM-03` | `platform.memberships.lifecycle.manage` | Membership | DEFERRED FROM V1 | Could bypass or conflict with C-02; platform override of Organization authority is not approved. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-MEM-04` | `platform.memberships.roles.manage` | Membership | DEFERRED FROM V1 | Could bypass or conflict with C-02; platform override of Organization authority is not approved. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-PROJ-01` | `platform.projects.project.read` | Project | DEFERRED FROM V1 | Could cross DATN-82/85 ACL or change visibility/authority; platform scope is not Project ACL. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-PROJ-02` | `platform.projects.metadata.manage` | Project | DEFERRED FROM V1 | Could cross DATN-82/85 ACL or change visibility/authority; platform scope is not Project ACL. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-PROJ-03` | `platform.projects.visibility.manage` | Project | DEFERRED FROM V1 | Visibility change may widen metadata audience. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-PROJ-04` | `platform.projects.members.manage` | Project | DEFERRED FROM V1 | Membership changes alter ACL and are owned by DATN-82. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-PROJ-05` | `platform.projects.leaders.manage` | Project | DEFERRED FROM V1 | Leader assignment changes authority. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-SEC-01` | `platform.sessions.session.read` | Session / Security | DEFERRED FROM V1 | IP/user-agent/device visibility lacks Security/Privacy approval. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-SEC-02` | `platform.sessions.session.revoke` | Session / Security | DEFERRED FROM V1 | Cross-user session revoke and session outcome are undefined. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-AUDIT-02` | `platform.audit.event.export` | Audit | DEFERRED FROM V1 | Export size/audience/retention policy is absent. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-SVC-01` | `platform.services.health.read` | Service | DEFERRED FROM V1 | No service/metric catalogue; detailed health can reveal topology. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-SVC-02` | `platform.services.metrics.read` | Service | DEFERRED FROM V1 | No service/metric catalogue; detailed health can reveal topology. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-JOB-01` | `platform.jobs.job.read` | Job / Queue | DEFERRED FROM V1 | No owner-scope/state/idempotency/cost oracle; retries can repeat effects. Payload is denied. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-JOB-02` | `platform.jobs.job.retry` | Job / Queue | DEFERRED FROM V1 | Retry can repeat side effects or cost. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-JOB-03` | `platform.jobs.job.cancel` | Job / Queue | DEFERRED FROM V1 | Cancellation guarantee/state transition is undefined. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-JOB-04` | `platform.jobs.job.requeue` | Job / Queue | DEFERRED FROM V1 | Requeue schedules new execution and can duplicate work. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-RAG-01` | `platform.rag.indexes.read` | RAG | DEFERRED FROM V1 | No ACL-safe source-version/rebuild/cost/recovery contract. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-RAG-02` | `platform.rag.indexes.rebuild` | RAG | DEFERRED FROM V1 | Rebuild consumes resources and changes index state. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-AI-01` | `platform.ai.runtime.read` | Laya / AI | DEFERRED FROM V1 | No shared authority adapter or finite command allowlist. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-AI-02` | `platform.ai.runtime.manage` | Laya / AI | DEFERRED FROM V1 | Command effects and rollback are undefined. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-LLM-01` | `platform.llm.providers.read` | LLM | DEFERRED FROM V1 | No provider workflow or secret-reference contract. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-LLM-02` | `platform.llm.providers.manage` | LLM | DEFERRED FROM V1 | No approved secret-reference/rotation path. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-INT-01` | `platform.integrations.integration.read` | Integration | DEFERRED FROM V1 | No delivery-safe transition contract; reconnect/disable can interrupt service. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-INT-02` | `platform.integrations.integration.manage` | Integration | DEFERRED FROM V1 | Reconnect/disable can interrupt delivery. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-INC-01` | `platform.incidents.incident.read` | Incident | DEFERRED FROM V1 | No authoritative source, lifecycle, notification or audit contract. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-INC-02` | `platform.incidents.incident.manage` | Incident | DEFERRED FROM V1 | Incident transition and notification effects are undefined. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-DIAG-01` | `platform.diagnostics.record.read` | Diagnostics | DEFERRED FROM V1 | No safe field allowlist; diagnostics may contain prompt, payload, token, secret or topology. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |
| `PLAT-SUP-01` | `platform.support.actions.manage` | Support | DEFERRED FROM V1 | No finite action catalogue; impersonation/content access is prohibited. No complete precondition/state/replay/concurrency/audit/error/test oracle. | KeyT/Thang under explicit closure request; domain owner required for later activation | DATN-79/A-04 and DATN_BE expose only three platform permissions/endpoints; candidate lacks complete owner-approved oracle. | Exclude from grantable codes, BE routes, FE actions and V1 QA capability; no migration/schema change. |

Final count: 3 ACTIVE, 37 DEFERRED FROM V1, zero unresolved dispositions. Deferrals are the conservative decision requested for this closure; they are not represented as individual domain-owner signatures. Reactivation requires a new authorized decision.

## 5. Sixteen-domain disposition

| Domain | Operations | V1 disposition |
|---|---|---|
| Dashboard | PLAT-DASH-01 | DEFERRED; no dashboard/aggregate counters. |
| Organization | PLAT-ORG-01..04 | PLAT-ORG-01 active only; no metadata read, lifecycle or usage. |
| User / Account | PLAT-USER-01..03 | DEFERRED; no user search/profile/status actions. |
| Membership | PLAT-MEM-01..04 | DEFERRED; no platform membership/invitation/lifecycle/role action; preserve C-02. |
| Project metadata/access | PLAT-PROJ-01..05 | DEFERRED; no platform Project/ACL action; preserve DATN-82/85. |
| Session / Security | PLAT-SEC-01..02 | DEFERRED; existing A-04 actor login/refresh only. |
| Audit | PLAT-AUDIT-01..02 | PLAT-AUDIT-01 active; export deferred. |
| Service | PLAT-HEALTH-01, PLAT-SVC-01..02 | PLAT-HEALTH-01 active; IAM liveness only. |
| Job / Queue | PLAT-JOB-01..04 | DEFERRED; no inspect/retry/cancel/requeue; payload denied. |
| RAG / Index | PLAT-RAG-01..02 | DEFERRED; no index read/rebuild; content denied. |
| Laya / AI | PLAT-AI-01..02 | DEFERRED; no runtime status/control. |
| LLM Provider | PLAT-LLM-01..02 | DEFERRED; no provider control/secret reference. |
| Integration | PLAT-INT-01..02 | DEFERRED; no integration read/reconnect/disable. |
| Incident | PLAT-INC-01..02 | DEFERRED; no incident actions. |
| Support | PLAT-SUP-01 | DEFERRED; no impersonation/content access. |
| Diagnostics | PLAT-DIAG-01 | DEFERRED; no diagnostics query/payload. |

Configuration is OUT OF V1 for BE/FE/QA. DATN-301 deferral stands; DEC-ACCESS-09 broader FUTURE / DECISION_REQUIRED state is unchanged.

## 6. Data visibility

| Data class | V1 visibility |
|---|---|
| Organization | PLAT-ORG-01 current allowlisted create input/response only. |
| User | No general user data; first ADMIN is checked only for existing ACTIVE state. |
| Membership | Only first ADMIN membership created atomically by PLAT-ORG-01. |
| Project metadata/ACL | None; no Project scope or ACL bypass. |
| Session/security | Existing actor login/refresh only; no token, MFA, session list, IP or UA projection. |
| Audit | At most 100 allowlisted action/target/actor/time fields; no export. |
| Service | IAM process liveness only, not dependency readiness/metrics. |
| Dashboard/job/RAG/Laya/LLM/integration/incident/support/diagnostics | No V1 access/mutation. |
| Project/task/document content, RAG chunks/embeddings, chat/prompts, job payload | Deny. |
| Passwords, keys, tokens, credentials, MFA/provider/integration secrets | Never return or log. |
| Configuration | No read/write/UI. |

Administration does not imply tenant-content access. An unsafe future projection stays deferred.

## 7. Authorization and error behavior

Validate authentication, current ACTIVE user, exact current A-04 permission, server-resolved target/scope, operation invariants, then safe projection. Fail closed on missing/invalid evidence. Do not trust role labels, client actor/scope, or stale token claims.

Keep IAM envelope code/message/details/requestId with safe allowlists.

| Condition | HTTP | V1 result |
|---|---:|---|
| Missing/invalid authentication/session | 401 | Existing authentication result |
| Authenticated but missing permission/inactive actor | 403 | No target detail |
| Invalid input | 422 | VALIDATION_FAILED; no body echo |
| Slug conflict/first ADMIN missing or inactive | 409 | ORGANIZATION_SLUG_CONFLICT / ORGANIZATION_ADMIN_UNAVAILABLE |
| Dependency unavailable | 503 | No success without required durable audit |
| Unexpected failure | 500 | Safe envelope only |
| Stale controlled assignment change | 409 | AUTHORITY_STATE_CONFLICT; no partial write |

### DEC-ACCESS-10 for active V1

| Resource | Missing | Unauthorized | Cross-scope | Conceal? | HTTP/code |
|---|---|---|---|---|---|
| New Organization create | No pre-existing target | Missing exact permission: 403 | N/A | No | 401/403; invalid 422; slug conflict 409 |
| First ADMIN selector | Missing/inactive share safe result | Missing actor permission: 403 | N/A | No existence disclosure | 409 ORGANIZATION_ADMIN_UNAVAILABLE |
| IAM health | No selector | 403 | N/A | No | 401/403 |
| Fixed audit projection | No selector | 403 | N/A | No | 401/403 |
| PO-AUTH-01 recipient | Missing/inactive share safe result | Unapproved executor denied | PLATFORM only | No existence disclosure | Internal 409 BOOTSTRAP_RECIPIENT_UNAVAILABLE |

No active A-04 endpoint has a target selector requiring concealment; no 404 concealment is introduced. 403 is default; 404 only applies to an explicitly classified concealed class. This resolves PLATFORM_OPERATOR V1 only; shared DEC-ACCESS-10 stays open for other resources.

## 8. Security/IAM and bootstrap package

AI cannot grant authority. No self-grant, operator-to-operator grant, public grant/revoke API, hidden account, seed, bypass or Break-glass.

Recipient is a distinct existing ACTIVE DATN User resolved through configured IdP immutable issuer+subject (iss+sub), not email alone; require fresh MFA. A named Security/IAM human issuer approves and a separate named IAM maintainer executes. Existing A-04 login/refresh remains unchanged.

PO-AUTH-01 is an internal controlled procedure, not runtime permission/API:

1. Record UUID operationId, change-ticket ID, target identity, BOOTSTRAP/REGRANT/REVOKE action, exact target and fixed reason code.
2. Issuer verifies need/identity and approves exact action/codes.
3. Separate executor authenticates with MFA, resolves identity to ACTIVE DATN User and uses short-lived least-privilege vault credential.
4. Preflight exact rows, provenance, version/state hash, unique indexes, other operator count and last-operator condition.
5. If any target A-04 row predates the procedure or lacks matching committed provenance, refuse with LEGACY_ASSIGNMENT_CONFLICT; never adopt/rewrite/revoke it.
6. In one Mongo transaction using snapshot read and majority commit, write exactly the three A-04 assignments, unique operation-id record and audit event.
7. Revoke only rows whose stable IDs/current state match the grant event. Preserve pre-existing standalone assignments. Deny if no other ACTIVE User retains all three current, unexpired assignments (LAST_OPERATOR_REQUIRED).
8. Majority-read and verify exact rows/event, save redacted report/hash, then return success.

### Grant/revoke and failure rules

- Grant exactly the three A-04 codes at PLATFORM scope, all-or-nothing.
- No operator grants another; issuer and executor are distinct from recipient.
- Same operationId + same payload returns prior committed result; same ID + different payload is 409 IDEMPOTENCY_KEY_REUSED.
- Concurrent same requests serialize; distinct requests use pre-state hash/CAS; stale conflict is 409 AUTHORITY_STATE_CONFLICT. No last-write-wins.
- New operation ID against conflicting changed state is 409; no silent adoption.
- Revoke must leave one other ACTIVE User with all three current, unexpired codes. Commit/verify replacement before removing last operator.
- If all operators are lost/expired/suspended, same two-person recovery path may create a new first operator; no bypass.
- Assignment, operation-id reservation and audit share one transaction. Any failure aborts all; no success.
- Unknown timeout: majority-read by operationId; matching event/state means committed; no event plus unchanged state permits retry with same ID; conflict/read failure returns 503 for reconciliation.
- Current protected requests recheck authority, so committed revoke denies the next request. No new bulk session revocation.

Security/IAM must name issuer/executor and approve identity/MFA proof, legacy guard, last-operator/recovery before first production use. No signer names are fabricated.

## 9. Audit contract

| Event | Coverage and required fields |
|---|---|
| organization.create | Each successful PLAT-ORG-01; preserve existing actorUserId/action/targetResource/targetResourceId/metadata/occurredAt fields and current safe summary. No new operation ID is required for this unchanged A-04 route. |
| platform.authority.granted | Successful PO-AUTH-01 bootstrap/regrant; executor actor, issuer, target, exact codes/scope, operation/change/request IDs, outcome/reason, assignment IDs and safe summary. |
| platform.authority.revoked | Successful PO-AUTH-01 revoke; same fields plus revoked assignment IDs/status. |
| Authorization denial | Sanitized telemetry: actor if known, action/permission, target class, status/reason, time/request ID; no body/secret. |

Current audit schema supports actor/action/target/time and Mixed metadata. A-04 Organization create inserts audit in the same transaction with a limited summary. New PO-AUTH-01 fields are DATN-295 requirements; PLAT-ORG-01 keeps its existing fields and failure semantics. These contracts are not proof of deployed options. Health/audit reads create no business read event; no export is active.

- Business mutation and required audit share one Mongo transaction. Audit/operation-id failure rolls back and returns no success; stale state is 409.
- APIs cannot update/delete history. Source proves append insert, not storage immutability. Writer cannot update/delete; retention principal deletes only expired rows.
- Proposed retention: 365 days from event time online, encrypted WORM/archive/backups; backup expiry no later than source record. Delete after expiry only by restricted dual-control worker with evidence. Operator cannot delete/shorten retention.
- Raw read is restricted to designated Security/Audit read-only access; Platform API exposes current fixed projection only; export disabled.
- Denial telemetry failure never changes denial to allow or alters 401/403; alert operations.
- Exclude passwords, keys, tokens, credentials, MFA/IdP assertions, prompts, payloads, tenant content and unrestricted exception text.
- Restore audit/business state from consistent recovery point; suspend privileged mutations until correlation is checked.

Security/IAM + Security/Audit + Privacy/Legal must approve retention, archive, backup/deletion, raw-read audience and denial telemetry. Proposal is complete but not signed.

## 10. DB contract and actual-state verification

Source declares platform_authority_assignments in continuum_iam with unique (subjectUserId, permission, scope), lookup (subjectUserId, status, permission), and only three A-04 permission enum values. The 20261005 migration creates collection/indexes only, does not mutate assignment documents, and defines no JSON-schema validator. Audit is in continuum_audit.audit_logs_iam with Mixed metadata. Source does not prove deployed state.

DATN-295 must preserve existing assignment/audit history; no backfill/rewrite/delete/adoption. Controlled regrant touches only provenance-matched rows. Atomic write includes exact three assignments, unique operation-id record and audit. Proposed ledger is platform_authority_change_operations in continuum_iam with unique UUID operationId, payload hash, issuer/executor references, audit event ID and committed result. Verify live DB before any additive migration; dry-run, target fingerprint, duplicate preflight, rollback. Never edit the existing migration or drop populated records.

The inspected repository does not record this migration in a persistent migration-history collection; deployment proof must come from the environment release/change record and approved dry-run checksum. DB REALITY = UNVERIFIED. Only connectionStatus was run using BE .env credential; host kimthang.mh3rrz2.mongodb.net, role atlasAdmin, readOnly:false. NODE_ENV=development does not prove staging/prod. No collection/assignment/index/validator/migration-history/audit data was read. No mutation was attempted. Do not reuse that credential. Follow the [read-only DB verification runbook](platform-operator-v1-db-verification-runbook.md).

## 11. Four-gate matrix and child readiness

| Gate | Current state/evidence | Decision | Owner | Status | Tasks |
|---|---|---|---|---|---|
| Security/IAM | Contract complete; no named issuer/executor in source | Two-person PO-AUTH-01; exact 3 codes; no self/operator grant; legacy guard/CAS/last operator | Security/IAM | EXTERNAL APPROVAL REQUIRED | 295/300 |
| Audit | A-04 create audit is transactional; global retention/immutability unproven | Approve PO-AUTH-01 event fields, 365-day archive proposal, denial telemetry and enforcement; preserve existing A-04 behavior | Security/IAM + Audit + Privacy/Legal | EXTERNAL APPROVAL REQUIRED | 295/300 |
| Operations | 3 ACTIVE / 37 DEFERRED / 0 open; DATN-79 and runtime confirm 3 | Preserve A-04 three; defer candidates | KeyT/Thang per explicit closure request | READY | 293–300 |
| DB reality | Non-read-only atlasAdmin; connectionStatus only | Obtain read-only staging/prod report, no writes | IAM DB owner/Data Platform | EXTERNAL APPROVAL REQUIRED | 295/300 |

| Task | Readiness | Handoff |
|---|---|---|
| DATN-295 | EXTERNAL APPROVAL REQUIRED | Attach read-only DB report and Security/IAM/Audit approval before implementation/migration. |
| DATN-296 | READY | Preserve PLAT-ORG-01; no new admin API; bootstrap tool belongs to DATN-295. |
| DATN-297 | READY | Preserve PLAT-HEALTH-01; no new operations endpoint. |
| DATN-298 | READY | No administration UI in V1; no deferred actions. |
| DATN-299 | READY | No operations UI or Configuration control. |
| DATN-300 | READY | Test three A-04 behaviors, denial, visibility/secrets, audit rollback and PO-AUTH-01 replay/CAS/last-operator when tool exists. |

READY means deterministic scope, not Done/shipped; no Jira workflow status changes.

## 12. Decision register and exact remaining approvals

The complete rationale, evidence, implementation impact, owner, affected tasks and exit/rollback condition for every decision are in the [DATN-301 decision record](DATN-301/design.md#3-decision-register).

| ID | Decision | Status | Owner/evidence |
|---|---|---|---|
| PO-D01 | Keep three A-04 codes/semantics unchanged | APPROVED | KeyT / DATN-79/A-04 |
| PO-D02 | Defer all 37 candidates; active catalog is three codes | APPROVED | KeyT/Thang explicit closure request; no complete candidate source/test oracle |
| PO-D03 | No hierarchy/wildcard/Break-glass/self/operator grant/public grant API | APPROVED | User scope and A-04 boundary |
| PO-D04 | Two-person PO-AUTH-01; IdP identity/MFA; legacy guard; last operator/recovery | PROPOSED | Security/IAM names unavailable |
| PO-D05 | Assignment, operation ID and audit atomic; CAS stale=409; audit failure rolls back | DERIVED | A-04 transaction/rollback precedent |
| PO-D06 | Audit fields/redaction/read/export/denial/failure | DERIVED | Audit schema and A-04 precedent |
| PO-D07 | 365-day retention, WORM/archive/backups, dual-control expiry deletion | PROPOSED | No existing policy found |
| PO-D08 | Active catalog has no concealment target; 403 default/no new 404 | DERIVED | Active endpoint target shape |
| PO-D09 | Configuration OUT OF V1 | APPROVED | DATN-301; DEC-ACCESS-09 broader status unchanged |
| PO-D10 | Deployed DB unverified | EXTERNAL APPROVAL REQUIRED | atlasAdmin/readOnly false; no collection query |
| PO-D11 | Preserve legacy rows; change only procedure-provenance rows | PROPOSED | Unique index; no provenance source |
| PO-D12 | One conceptual PLATFORM_OPERATOR actor; full active V1 bundle is exactly three A-04 assignments; no tiers | APPROVED | Explicit task constraint and current A-04 exact-permission guard |

Remaining human approvals:

1. Security/IAM: name issuer and separate executor; approve immutable IdP iss+sub/MFA proof, two-person approval, exact three codes, no self/operator grant, legacy guard, last-operator/all-lost recovery, rollback/post-check. Proposed answer: approve §8 and attach names/change procedure. Evidence: signed runbook. Tasks 295/300.
2. Security/IAM + DB: approve legacy conflict/regrant and operation-id ledger. Proposed answer: reject rows without controlled provenance; reactivate only matching rows. Evidence: signed lifecycle decision and additive migration/rollback after DB inspection. Tasks 295/300.
3. Security/IAM + Audit + Privacy/Legal: approve 365 days, archive/WORM/backup/deletion, raw-read audience and denial telemetry or exact replacement. Evidence: signed retention/control decision. Tasks 295/300.
4. IAM DB owner/Data Platform: provide read-only staging/prod access/report for continuum_iam and continuum_audit. Proposed access: read only. Evidence: redacted role/index/validator/count/migration report and SHA-256. Tasks 295/300.

No per-operation owner approval or DEC-ACCESS-10 resource classification remains for deferred capabilities. Reactivation requires new approval.

## 13. Acceptance and source references

- [x] 3 active permissions/operations; 37 deferred; zero unresolved operation dispositions.
- [x] Every operation is mapped and carries status, reason, owner, evidence and implementation impact.
- [x] All 16 domains dispositioned; Configuration out of V1.
- [x] DATN-79 unchanged; no tenant-content or secret access.
- [x] Bootstrap/recovery/grant/revoke/race/retry/timeout/rollback/last operator/post-check specified.
- [x] Audit coverage/fields/redaction/retention proposal/read/export/denial/integrity/failure specified.
- [x] DEC-ACCESS-10 resolved for active V1.
- [x] DB state marked UNVERIFIED with read-only runbook.
- [x] Child handoffs deterministic; no Jira status inferred.
- [x] No runtime code, migration, seed, ACL/RAG/ingestion or DB mutation.

Jira DATN-293–301, DATN-79/80 and A-04 subtasks DATN-190–194 were reviewed. Source review covered DATN_BE authorization policy, assignment schema/index declarations, platform controller/audit repository, Organization provisioning transaction/tests and existing migration/README/plan. DEC-ACCESS-09, Project Access/Visibility, shared access readiness and audit/outbox research were reviewed. No source was treated as deployed DB evidence.

FINAL STATUS: READY EXCEPT EXTERNAL APPROVAL. Documentation only; do not push/merge. DATN-295 must attach DB report and signed decisions before any migration. DB changes must be additive and include rollout/rollback while preserving existing history.
