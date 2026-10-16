# PLATFORM_OPERATOR V1 Contract

| Field | Value |
|---|---|
| Status | Partial owner-approved policy; no runtime enablement |
| Jira | DATN-294; parent DATN-293 |
| Reviewed | 2026-10-16 (Asia/Bangkok) |
| Documentation repository | `DATN-SPRING2027/Document` (local checkout: `Document-B05-reference`) |
| Base branch / commit | `main` / `c8190aa3b3c9670ef96a9d651feba5e0de63e742` |
| Original contract branch (DATN-294) | `feat/KeyT-platform-operator-v1-contract-bootstrap` |

> Canonical contract and evidence ledger. Section 24 records the latest DATN-301 owner disposition and supersedes earlier draft statuses where they conflict. Policy approval does not enable runtime permissions or operations. DATN-301 remains incomplete while issuer/recovery, retention, audit coverage, concealment resource classes and disposition of each new operation are unresolved. The 37 new operations are `BLOCKED / NOT ACTIVE`; no evidence approves them either active or deferred from V1.

## 1. Purpose

Define a reviewable V1 source of truth for DATN-295–300: permission names, operations, scopes, visibility, authorization, audit and bootstrap rules. Avoid widening DATN-79/A-04 authority accidentally.

## 2. Scope and evidence labels

V1 intends one platform role with the full set of **approved Platform Administration V1 permissions**, with no tiers or role hierarchy. “Full” means the finite approved operation set, not wildcard access, tenant-content access, authentication bypass or unrestricted CRUD.

- **[CONFIRMED]** Directly supported by accepted Jira decisions, approved docs or current code.
- **[DERIVED]** Follows from confirmed evidence without adding policy.
- **[PROPOSED]** New policy requiring owner/security approval before implementation.
- **[CONFLICT]** Sources disagree; implementation must wait for resolution.
- **[APPROVED POLICY; NOT RUNTIME]** A KeyT-approved authorization or response policy recorded in §24; it does not enable runtime permissions, endpoints or UI.
- **[DEFERRED]** Explicitly excluded from active V1; do not implement or render it.
- **[BLOCKED]** Required owner decision or evidence is missing; implementation must wait.
- **[BLOCKED / NOT ACTIVE]** No operation may be implemented or rendered yet; this is a safe gate, not a decision to exclude it from V1. The authorized domain owner must explicitly approve it active with complete semantics or explicitly defer it from V1.

This task is documentation only. No permission here is added to runtime authorization.

## 3. Current Authorization Baseline

### 3.1 DATN-79 / A-04 facts

| Item | Current fact | Evidence |
|---|---|---|
| Platform permissions | Exactly `organization.create`, `platform.health.read`, `platform.audit.read` | DATN-79; DATN_BE IAM schemas, authorization policy, OpenAPI |
| Organization roles | `ADMIN`, `TEAM_LEADER`, `MEMBER`; not platform roles | DATN_BE schemas and A-04 docs |
| Assignment | `platform_authority_assignments`: subject user, one exact permission, `scope: PLATFORM`, `ACTIVE`/`REVOKED`, grant actor/time, optional expiry/revocation | DATN_BE IAM schemas |
| Resolution | Exact permission match; no wildcard or role-to-permission expansion | DATN_BE `authorization.policy.ts` and platform guard |
| Actor | Verified access-token subject; must resolve to current `ACTIVE` user and pass token revocation checks | DATN_BE authentication service |
| Enforcement | Missing permission annotation is forbidden; current assignment is checked per request; invalid/unavailable evidence denies | DATN_BE platform guard |
| Platform token | Carries no Organization or Organization-role claims | DATN_BE authentication service |
| Organization creation | `POST /iam/platform/organizations`; Organization, first active ADMIN membership/role assignment and `organization.create` audit share a Mongo transaction. Operator cannot become first Organization ADMIN in this flow | DATN-79; provisioning controller/service/repository |
| Health | `GET /iam/platform/health` is IAM process liveness only | DATN-79; platform controller |
| Audit read | `GET /iam/platform/audit` returns bounded filtered projection for org creation and authority grant/revoke; cap 100 | DATN-79; platform audit repository |
| Project access | Platform authority, Organization administration and Project access are separate | DATN-82, DATN-85; DATN_BE policy |
| Account states | `ACTIVE`, `SUSPENDED`, `PENDING_INVITE`; current platform subject must be ACTIVE | DATN_BE schemas/auth service |

### 3.2 Current implementation limits

Code does **not** establish `PLATFORM_OPERATOR` as a runtime role; it establishes three exact platform codes. No evidence supports wildcard grants, implicit bundles, general platform User/Membership/Project controls, or shared operator APIs for service, job, RAG, Laya, providers, integrations, configuration, incidents or support. Health is liveness, not dashboard/metrics. Do not infer capabilities from Jira proposal or role name.

Organization schema has no lifecycle status or usage counters. Current audit code supports append operations but does not prove immutable storage or complete grant/revoke producers. Platform-authority bootstrap issuer and recovery are not established.

### 3.3 Organization and Project boundaries

- Organization membership authority is separate (DATN-80/86/87/88, C-02). A platform assignment does not imply Organization `ADMIN` or those powers.
- Project access uses separate scope and permissions (DATN-82). `project.visibility.manage`, `project.leader.manage`, and Project TEAM_LEADER's `project.members.list/add/remove` are not platform wildcard permissions.
- DATN-85 permits Project metadata visibility under its rules; it does not grant task, document, knowledge, chat or other nested content.

## 4. PLATFORM_OPERATOR Definition

**[APPROVED POLICY; NOT RUNTIME]** V1 has one PLATFORM_OPERATOR whose exact effective permission set is the 3 unchanged DATN-79/A-04 codes plus the 37 codes listed in §5.2. There are no tiers, hierarchy, wildcard, tenant-content access or authentication bypass.

The persistence model remains exact per-permission assignments; this decision does not require a role/bundle database row. Granting or revoking the full 40-code operator set is all-or-nothing and atomic. A partial or inconsistent set is not an effective PLATFORM_OPERATOR. Existing standalone A-04 assignments retain their current behavior and are not automatically rewritten or backfilled. The 37 codes are not added to runtime by this document.

## 5. Permission Model

### 5.1 Naming and scope

**[APPROVED POLICY; NOT RUNTIME]** The exact 37 permission identifiers in §5.2 are accepted for the V1 operator set, using the four-segment platform.domain.resource.action pattern. Preserve the three existing DATN-79 identifiers byte-for-byte. No wildcard or additional permission is approved.

PLATFORM is the grant scope, not a trusted target selector. The server resolves each target and derives scope/relationships from authoritative storage. Client scope/parent IDs are selectors only and must be checked. Cross-Organization/Project relationships are validated server-side. Missing-resource concealment follows the approved rule in §24 and applicable resource policy.

### 5.2 Permission matrix

`ALLOW` is approved policy membership, not proof of runtime support or operation approval. An explicit `DENY` would be an approved policy prohibition; none is defined in this matrix. Deferred/out-of-scope capabilities are recorded separately and are not represented as DENY. Each target must be resolved server-side. Audit/error shorthand is detailed below.

| Permission | Domain | Action / resource | Grant / target scope | Role | Authorization | Visibility | Audit | Status / source |
|---|---|---|---|---|---|---|---|---|
| `organization.create` | Organization | Create Organization + first ADMIN | PLATFORM / new Organization | ALLOW | Exact current A-04; active subject; provisioning invariants | Input and safe created metadata | Required, transactional | [CONFIRMED] DATN-79 |
| `platform.health.read` | Service | Read IAM liveness | PLATFORM / service | ALLOW | Exact current permission | Liveness only | Read logging unresolved | [CONFIRMED] DATN-79 |
| `platform.audit.read` | Audit | Read filtered projection | PLATFORM / audit event | ALLOW | Exact current permission; bounded filters | Existing allowlisted fields | Read logging unresolved | [CONFIRMED] DATN-79 |
| `platform.dashboard.summary.read` | Dashboard | Read approved aggregate counters | PLATFORM / aggregate | ALLOW | Active subject; approved metric sources | Aggregates only | Read logging proposed | [APPROVED POLICY; NOT RUNTIME] DATN-293 |
| `platform.organizations.organization.read` | Organization | Read metadata | PLATFORM / Organization | ALLOW | Resolve target server-side | Allowlisted metadata | Read logging proposed | [APPROVED POLICY; NOT RUNTIME] |
| `platform.organizations.status.manage` | Organization | Suspend/reactivate | PLATFORM / Organization | ALLOW | Approved transition, reason, version | State and safe result | Required | [APPROVED POLICY; NOT RUNTIME]; status absent in schema |
| `platform.organizations.usage.read` | Organization | Read usage/health counters | PLATFORM / Organization | ALLOW | Approved metric source/definition | Aggregates only | Read logging proposed | [APPROVED POLICY; NOT RUNTIME]; counters absent |
| `platform.users.account.read` | User | Read account metadata | PLATFORM / User | ALLOW | Resolve target server-side | Safe identity/profile/state | Read logging proposed | [APPROVED POLICY; NOT RUNTIME] |
| `platform.users.profile.manage` | User | Update allowlisted profile fields | PLATFORM / User | ALLOW | Field allowlist and version check | Safe profile only | Required | [APPROVED POLICY; NOT RUNTIME] |
| `platform.users.status.manage` | User | Suspend/reactivate | PLATFORM / User | ALLOW | Lifecycle policy/reason/version; final-operator rule unresolved | State/result | Required | [APPROVED POLICY; NOT RUNTIME]; lifecycle incomplete |
| `platform.memberships.membership.read` | Membership | Read Organization membership | PLATFORM / membership→Organization | ALLOW | Resolve both; C-02 projection | Membership/role state | Read logging proposed | [APPROVED POLICY; NOT RUNTIME]; preserve DATN-80/86–88 |
| `platform.memberships.invitation.create` | Membership | Invite to Organization | PLATFORM / Organization | ALLOW | Reuse C-02 invite invariants | Safe invite result; no token | Required | [APPROVED POLICY; NOT RUNTIME]; precedence needs approval |
| `platform.memberships.lifecycle.manage` | Membership | Suspend/reactivate/remove | PLATFORM / membership→Organization | ALLOW | C-02 last ADMIN, self-action, CAS/idempotency | Membership state | Required | [APPROVED POLICY; NOT RUNTIME]; precedence needs approval |
| `platform.memberships.roles.manage` | Membership | Change Organization role | PLATFORM / membership→Organization | ALLOW | C-02 allowed transitions/actor rules | Role metadata | Required | [APPROVED POLICY; NOT RUNTIME]; no invented grant power |
| `platform.projects.project.read` | Project | Read metadata | PLATFORM / Project→Organization | ALLOW | Resolve relation | Approved metadata only | Read logging proposed | [APPROVED POLICY; NOT RUNTIME]; DATN-85 |
| `platform.projects.metadata.manage` | Project | Update allowlisted metadata | PLATFORM / Project→Organization | ALLOW | Field allowlist and version | Metadata only | Required | [APPROVED POLICY; NOT RUNTIME] |
| `platform.projects.visibility.manage` | Project | Change visibility | PLATFORM / Project→Organization | ALLOW | Reuse DATN-82 | Visibility only | Required | [APPROVED POLICY; NOT RUNTIME]; DATN-82 |
| `platform.projects.members.manage` | Project | List/add/remove Project member | PLATFORM / Project→Organization | ALLOW | Resolve Project/member; preserve DATN-82 ACL | ACL metadata, no content | Required | [APPROVED POLICY; NOT RUNTIME]; composition unresolved |
| `platform.projects.leaders.manage` | Project | Assign/remove leader | PLATFORM / Project→Organization | ALLOW | DATN-82 leader constraints | Assignment metadata | Required | [APPROVED POLICY; NOT RUNTIME]; reuse semantics |
| `platform.sessions.session.read` | Security | Read session metadata | PLATFORM / session→User | ALLOW | Resolve owner; privacy allowlist | Safe state/time/device; IP/UA unresolved | Read logging proposed | [APPROVED POLICY; NOT RUNTIME] |
| `platform.sessions.session.revoke` | Security | Revoke session | PLATFORM / session→User | ALLOW | Exact permission; current state; idempotent repeat | Revocation result only | Required | [APPROVED POLICY; NOT RUNTIME] |
| `platform.audit.event.export` | Audit | Export filtered audit events | PLATFORM / event set | ALLOW | Same projection as read; bounded output | No secrets/raw events | Export log proposed | [APPROVED POLICY; NOT RUNTIME]; read/export logging open |
| `platform.services.health.read` | Service | Read approved service health | PLATFORM / service | ALLOW | Service allowlist | Health only | Read logging proposed | [APPROVED POLICY; NOT RUNTIME]; only IAM liveness confirmed |
| `platform.services.metrics.read` | Service | Read approved metrics | PLATFORM / aggregate | ALLOW | Approved catalogue/dimensions | Aggregates only | Read logging proposed | [APPROVED POLICY; NOT RUNTIME]; owner/source absent |
| `platform.jobs.job.read` | Queue | Inspect job state/metadata | PLATFORM / job→owner scope | ALLOW | Resolve owner scope; honor content ACL | Operational metadata, no payload | Read logging proposed | [APPROVED POLICY; NOT RUNTIME] |
| `platform.jobs.job.retry` | Queue | Retry eligible job | PLATFORM / job→owner scope | ALLOW | State, budget, deduplication | State/result ref | Required | [APPROVED POLICY; NOT RUNTIME]; state machine absent |
| `platform.jobs.job.cancel` | Queue | Cancel cancellable job | PLATFORM / job→owner scope | ALLOW | State and concurrency | State/result | Required | [APPROVED POLICY; NOT RUNTIME]; state machine absent |
| `platform.jobs.job.requeue` | Queue | Requeue eligible job | PLATFORM / job→owner scope | ALLOW | Eligibility, dedupe/idempotency | State/result ref | Required | [APPROVED POLICY; NOT RUNTIME]; semantics absent |
| `platform.rag.indexes.read` | RAG | Read index status | PLATFORM / index→owner scope | ALLOW | Resolve owner; preserve content ACL | Index status only, no chunks | Read logging proposed | [APPROVED POLICY; NOT RUNTIME]; shared API absent |
| `platform.rag.indexes.rebuild` | RAG | Rebuild/reindex | PLATFORM / index→owner scope | ALLOW | Source/state, idempotency, job tracking | Operation status | Required | [APPROVED POLICY; NOT RUNTIME]; owner/semantics absent |
| `platform.ai.runtime.read` | Laya | Read runtime/model status | PLATFORM / runtime | ALLOW | Approved runtime registry | No prompts/content | Read logging proposed | [APPROVED POLICY; NOT RUNTIME]; shared authority absent |
| `platform.ai.runtime.manage` | Laya | Finite operational control | PLATFORM / runtime | ALLOW | Command allowlist and state checks | Safe status/result | Required | [APPROVED POLICY; NOT RUNTIME]; control list absent |
| `platform.llm.providers.read` | LLM | Read provider/model status | PLATFORM / provider | ALLOW | Approved catalogue | Non-secret metadata | Read logging proposed | [APPROVED POLICY; NOT RUNTIME] |
| `platform.llm.providers.manage` | LLM | Finite provider operation | PLATFORM / provider | ALLOW | Approved workflow; secret reference only | Redacted metadata | Required | [APPROVED POLICY; NOT RUNTIME]; control/secret API absent |
| `platform.integrations.integration.read` | Integration | Read metadata/status | PLATFORM / integration | ALLOW | Approved catalogue | Non-secret metadata | Read logging proposed | [APPROVED POLICY; NOT RUNTIME] |
| `platform.integrations.integration.manage` | Integration | Enable/disable/reconnect | PLATFORM / integration | ALLOW | Finite transitions; secret refs | Redacted result | Required | [APPROVED POLICY; NOT RUNTIME]; control/secret API absent |
| `platform.incidents.incident.read` | Incident | Read incident metadata | PLATFORM / incident | ALLOW | Resolve target; sanitized fields | Operational metadata | Read logging proposed | [APPROVED POLICY; NOT RUNTIME]; contract absent |
| `platform.incidents.incident.manage` | Incident | Create/update/resolve | PLATFORM / incident | ALLOW | Transition, reason, version rules | Safe state/summary | Required | [APPROVED POLICY; NOT RUNTIME]; lifecycle absent |
| `platform.diagnostics.record.read` | Support | Read bounded diagnostics | PLATFORM / diagnostic ref | ALLOW | Exact IDs, bounded window, allowlist | Sanitized errors; no payload | Read logging proposed | [APPROVED POLICY; NOT RUNTIME] |
| `platform.support.actions.manage` | Support | Finite support action | PLATFORM / resolved target | ALLOW | Per-action allowlist/state/reason | Safe result only | Required | [APPROVED POLICY; NOT RUNTIME]; catalogue absent |

**Permission count: 40 exact codes = 3 existing A-04 permissions + 37 KeyT-approved permission-set additions.** These codes define the PLATFORM_OPERATOR policy set; this is not runtime enablement or operation approval. Existing A-04 codes and standalone assignments are unchanged. Every new code remains absent from runtime until its operation and implementation are separately approved. Configuration is deferred from active V1 by the DATN-301 disposition in §24; DEC-ACCESS-09 itself still marks configuration read/write `FUTURE / DECISION_REQUIRED`. Configuration has no permission row here; this is not an implicit deny.
## 6. Operation Catalog

### 6.1 Shared rules
**Operation disposition:** the three existing DATN-79/A-04 operation contracts remain approved with their existing semantics: PLAT-ORG-01, PLAT-HEALTH-01 and PLAT-AUDIT-01. This records the approved baseline; it does not claim runtime deployment beyond the existing release state. Each of the other 37 operation rows is `BLOCKED / NOT ACTIVE` pending an authorized per-operation decision: approve it active with complete semantics, or explicitly defer it from active V1. A permission in the role set does not activate an API or UI. The pending IDs are PLAT-DASH-01; PLAT-ORG-02..04; PLAT-USER-01..03; PLAT-MEM-01..04; PLAT-PROJ-01..05; PLAT-SEC-01..02; PLAT-AUDIT-02; PLAT-SVC-01..02; PLAT-JOB-01..04; PLAT-RAG-01..02; PLAT-AI-01..02; PLAT-LLM-01..02; PLAT-INT-01..02; PLAT-INC-01..02; PLAT-SUP-01..02.

The actor for each row is an authenticated current `ACTIVE` user with the exact current platform permission. Server resolves targets and scope; client cannot assert trusted scope. Repeated mutations require defined idempotency; state changes need CAS/version checks where a stale write can overwrite newer state. Mutations return safe results and an operation/correlation ID when available. The broad HTTP/error mapping and safe IAM envelope are approved in §24; stable codes, field-level response allowlists and concealment resource classes remain open per operation/DEC-ACCESS-10. Proposed rows do not authorize implementation.

| Operation ID | Permission | Domain / action / resource | Scope / target resolution | Actor / authorization | Data returned | Mutation, audit, repeat/concurrency, destructive effect | Error | Disposition |
|---|---|---|---|---|---|---|---|
| `PLAT-ORG-01` | `organization.create` | Org / create + first ADMIN | PLATFORM / new Org | Authenticated active subject; exact A-04; actor cannot be first ADMIN; recipient must be existing ACTIVE User | Safe created Organization metadata: id, name, slug, plan, createdAt, updatedAt | Input allowlist: name (trimmed, 1–200 chars), slug (trimmed/lowercased, 1–100 chars), plan (`FREE`/`ENTERPRISE`), 24-hex firstAdminUserId; one Mongo transaction creates Organization, first ADMIN membership/role assignment and audit event; event fields are actorUserId/action/targetResource/targetResourceId/metadata/occurredAt; no idempotency key or operationId; same slug retry conflicts; no partial commit | 401/403 auth; 422 validation; 409 self-first-admin/unavailable recipient/slug conflict; D4 maps dependency/unexpected failures to 503/500, but exact endpoint status/body mapping is not verified; stable per-operation codes remain open | APPROVED BASELINE — A-04; behavior and runtime state unchanged |
| `PLAT-HEALTH-01` | `platform.health.read` | Service / IAM liveness | PLATFORM / IAM process | Authenticated active subject; exact current permission; guard reloads exact current assignment | Existing IAM response `{status: "ok"}` only | No request input; read-only; reports IAM process liveness only, not MongoDB/Redis/BullMQ readiness; `Cache-Control: no-store`; no operation side effect; read/denial audit coverage remains blocked under D5 | 401/403 from current auth/guard; D4 maps dependency/unexpected failure classes to 503/500, but this liveness endpoint does not define dependency checks or stable per-operation codes | APPROVED BASELINE — A-04; behavior and runtime state unchanged |
| `PLAT-AUDIT-01` | `platform.audit.read` | Audit / operational metadata projection | PLATFORM / fixed allowlisted event set | Authenticated active subject; exact current permission; guard reloads exact current assignment | Up to 100 events, sorted `occurredAt DESC, _id DESC`; fields action, targetResource, targetResourceId, actorUserId, occurredAt; only `organization.create`, `platform.authority.granted`, `platform.authority.revoked` | No request input/filter; read-only; `Cache-Control: no-store`; no export; no mutation; read/denial audit coverage remains blocked under D5; no idempotency/concurrency effect | 401/403 from current auth/guard; D4 maps dependency/unexpected failure classes to 503/500, but exact storage-failure status and stable per-operation codes/body remain unresolved | APPROVED BASELINE — A-04; behavior and runtime state unchanged |
| `PLAT-DASH-01` | `platform.dashboard.summary.read` | Dashboard / approved summary | PLATFORM / aggregate sources | Exact permission; approve source allowlist | Approved counters | Read; read log proposed | 401/403; unavailable-source code open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-ORG-02` | `platform.organizations.organization.read` | Org / metadata read | PLATFORM / server-resolved Org | Exact permission; resolve target | Allowlisted metadata | Read; read log proposed | 401/403; 404 policy open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-ORG-03` | `platform.organizations.status.manage` | Org / suspend/reactivate | PLATFORM / resolved Org | Exact permission; approved transition/reason/version | State and safe result | Mutation; audit; idempotency + CAS; suspend can interrupt service | 401/403; conflict/stale codes open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-ORG-04` | `platform.organizations.usage.read` | Org / usage read | PLATFORM / resolved Org | Exact permission; approve metric source | Aggregates | Read; read log proposed | 401/403; metric-source code open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-USER-01` | `platform.users.account.read` | User / metadata read | PLATFORM / resolved User | Exact permission; active actor | Safe identity/profile/state | Read; read log proposed | 401/403; concealment per DEC-ACCESS-10 | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-USER-02` | `platform.users.profile.manage` | User / allowlisted profile update | PLATFORM / resolved User | Exact permission; field allowlist/version | Safe updated profile | Mutation; audit + CAS; idempotency by field | 401/403; validation/stale codes open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-USER-03` | `platform.users.status.manage` | User / suspend/reactivate | PLATFORM / resolved User | Exact permission; lifecycle/version policy | State/result | Mutation; audit + CAS/idempotency; may revoke access | 401/403; last-operator/self rules BLOCKED | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-MEM-01` | `platform.memberships.membership.read` | Membership / read | PLATFORM / membership→Org | Exact permission; C-02 projection | Membership/role/state metadata | Read; read log proposed | 401/403; concealment open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-MEM-02` | `platform.memberships.invitation.create` | Membership / invite | PLATFORM / resolved Org | Exact permission; C-02 invite rules | Safe invite result, no token | Mutation; audit; idempotency required | 401/403; duplicate code open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-MEM-03` | `platform.memberships.lifecycle.manage` | Membership / suspend/reactivate/remove | PLATFORM / membership→Org | Exact permission; C-02 last ADMIN/self/CAS invariants | Membership state | Mutation; audit + CAS/idempotent; removal affects access | 401/403; C-02 conflicts and concealment open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-MEM-04` | `platform.memberships.roles.manage` | Membership / change role | PLATFORM / membership→Org | Exact permission; C-02 transitions | Role metadata | Mutation; audit + CAS/idempotent; may reduce access | 401/403; transition/conflict code open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-PROJ-01` | `platform.projects.project.read` | Project / metadata read | PLATFORM / Project→Org | Exact permission; DATN-85 boundary | Metadata only | Read; read log proposed | 401/403; no content implication | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-PROJ-02` | `platform.projects.metadata.manage` | Project / update allowlist | PLATFORM / Project→Org | Exact permission; field allowlist/version | Updated metadata | Mutation; audit + CAS; field idempotency | 401/403; validation/stale codes open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-PROJ-03` | `platform.projects.visibility.manage` | Project / visibility change | PLATFORM / Project→Org | Exact permission; DATN-82 | Visibility only | Mutation; audit + CAS/idempotency; broadens metadata reach only | 401/403; invalid-state/conflict open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-PROJ-04` | `platform.projects.members.manage` | Project / list/add/remove member | PLATFORM / Project + member resolved | Exact permission; DATN-82 ACL composition | ACL metadata only | List read; add/remove audited + CAS/idempotent; removal affects access | 401/403; composition BLOCKED | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-PROJ-05` | `platform.projects.leaders.manage` | Project / assign/remove leader | PLATFORM / Project + Org member | Exact permission; DATN-82 constraints | Assignment metadata | Mutation; audit + CAS/idempotent; changes authority | 401/403; invalid-state code open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-SEC-01` | `platform.sessions.session.read` | Security / session metadata | PLATFORM / session→User | Exact permission; privacy allowlist | Safe state/time/device; IP/UA unresolved | Read; read log proposed | 401/403; hiding open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-SEC-02` | `platform.sessions.session.revoke` | Security / revoke session | PLATFORM / session→User | Exact permission; current state; no client owner assertion | Revocation result | Mutation; audit + CAS; idempotent repeat; invalidates session | 401/403; state/stale code open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-AUDIT-02` | `platform.audit.event.export` | Audit / export filtered events | PLATFORM / same dataset as read | Exact permission; bounded projection/export | Same safe fields as read | Export; no mutation; export audit proposed | 401/403; size-limit error open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-SVC-01` | `platform.services.health.read` | Service / approved health | PLATFORM / service registry | Exact permission; allowlist | Health state only | Read; read log proposed | 401/403; upstream code open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-SVC-02` | `platform.services.metrics.read` | Service / metrics | PLATFORM / service + metric dimensions | Exact permission; approved catalogue | Aggregates only | Read; read log proposed | 401/403; source error open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-JOB-01` | `platform.jobs.job.read` | Queue / inspect job | PLATFORM / job owner scope resolved | Exact permission; no content bypass | Operational metadata, no payload | Read; read log proposed | 401/403; concealment open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-JOB-02` | `platform.jobs.job.retry` | Queue / retry job | PLATFORM / job owner resolved | Exact permission; retryable state/budget/dedupe | State/result ref | Mutation; audit + idempotency key + CAS; may repeat cost/side effects | 401/403; state/dependency code open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-JOB-03` | `platform.jobs.job.cancel` | Queue / cancel job | PLATFORM / job owner resolved | Exact permission; cancellable state | State/result | Mutation; audit + CAS; idempotent terminal state; stops work | 401/403; state/stale code open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-JOB-04` | `platform.jobs.job.requeue` | Queue / requeue job | PLATFORM / job owner resolved | Exact permission; eligibility/dedupe | State/result ref | Mutation; audit + key + CAS; schedules execution | 401/403; conflict/dependency code open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-RAG-01` | `platform.rag.indexes.read` | RAG / index status | PLATFORM / index owner resolved | Exact permission; preserve content ACL | Status only, no chunks | Read; read log proposed | 401/403; hiding open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-RAG-02` | `platform.rag.indexes.rebuild` | RAG / rebuild index | PLATFORM / index + source resolved | Exact permission; source/state/idempotency | Operation status | Mutation; audit + job tracking + CAS; resource/cost impact | 401/403; state/dependency open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-AI-01` | `platform.ai.runtime.read` | Laya / runtime status | PLATFORM / registered runtime | Exact permission; approved registry | Status only; no prompts/content | Read; read log proposed | 401/403; authority integration absent | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-AI-02` | `platform.ai.runtime.manage` | Laya / finite control | PLATFORM / runtime resolved | Exact permission; command allowlist/state | Safe result/status | Mutation; audit; per-command idempotency; declare destructive effect | 401/403; command errors unapproved | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-LLM-01` | `platform.llm.providers.read` | LLM / provider status | PLATFORM / provider catalogue | Exact permission; redact secrets | Non-secret metadata | Read; read log proposed | 401/403; provider error map open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-LLM-02` | `platform.llm.providers.manage` | LLM / finite provider operation | PLATFORM / provider resolved | Exact permission; approved workflow; secret ref only | Redacted metadata/result | Mutation; audit + CAS/idempotency; impact per action | 401/403; secret API absent | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-INT-01` | `platform.integrations.integration.read` | Integration / status | PLATFORM / integration resolved | Exact permission; redact credentials | Non-secret metadata | Read; read log proposed | 401/403; dependency map open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-INT-02` | `platform.integrations.integration.manage` | Integration / enable/disable/reconnect | PLATFORM / integration resolved | Exact permission; finite transitions, secret refs | Redacted result | Mutation; audit + CAS/idempotency; may interrupt delivery | 401/403; control/secret API absent | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-INC-01` | `platform.incidents.incident.read` | Incident / metadata read | PLATFORM / incident resolved | Exact permission; sanitized fields | Operational metadata | Read; read log proposed | 401/403; source contract absent | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-INC-02` | `platform.incidents.incident.manage` | Incident / create/update/resolve | PLATFORM / incident resolved | Exact permission; transition/reason/version | Safe state/summary | Mutation; audit + CAS/idempotency; resolution workflow effect | 401/403; lifecycle codes unapproved | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-SUP-01` | `platform.diagnostics.record.read` | Support / diagnostics lookup | PLATFORM / exact request/correlation/job/op ref | Exact permission; bounded window/allowlist | Sanitized diagnostics, no payload | Read; read log proposed | 401/403; disclosure policy open | BLOCKED / NOT ACTIVE — domain-owner disposition pending |
| `PLAT-SUP-02` | `platform.support.actions.manage` | Support / finite action | PLATFORM / target/action resolved server-side | Exact permission; action allowlist/state/reason | Safe result only | Mutation; audit + per-action CAS/idempotency; declare destructive effect | 401/403; action catalogue absent | BLOCKED / NOT ACTIVE — domain-owner disposition pending |

**Operation count: 40.** Each permission has exactly one operation row. Three rows preserve the A-04 baseline; the other 37 are blocked pending explicit per-operation disposition. Proposed/blocked rows do not authorize implementation.
## 7. Actor → Action → Resource → Scope

1. **Authenticate:** validate access token, current user state and revocation as the existing auth service does.
2. **Identify actor:** use the verified token subject; never trust a client-supplied actor ID.
3. **Resolve authority:** require the exact current permission. A role name alone, stale token claim or wildcard cannot authorize.
4. **Resolve target:** load target and parent relationships from the authoritative service/store. Client IDs are lookup inputs only.
5. **Evaluate state:** validate Organization/Project relationship, resource lifecycle, current version, and operation-specific invariants.
6. **Allow or deny:** fail closed on invalid/missing authorization evidence. Return 404 for concealment only when the resource class is listed by DEC-ACCESS-10; otherwise follow the applicable authorization policy.
7. **Audit mutation:** persist the required audit record with the operation outcome.

Grant scope is PLATFORM for these platform permissions. Target scope remains distinct: PLATFORM, Organization, Project, or resource as shown per operation. A platform grant does not convert target scope, create Organization membership, or bypass Project ACL/content checks.

## 8. Data Visibility Boundary

This table records the approved visibility boundary and proposed operation shapes, not runtime enablement. The three DATN-79 operation contracts remain approved with their current behavior; no claim is made that a newer implementation is deployed. Every newly mapped operation remains `BLOCKED / NOT ACTIVE` until an authorized owner approves its operation contract or explicitly defers it from V1. Platform permission membership does not itself approve returned fields or tenant-content access.

| Resource/data | View | Mutate | Scope / condition | Audit |
|---|---|---|---|---|
| Organization metadata | Safe allowlisted metadata only after operation approval | Explicit status/metadata operation only after approval | Resolve Organization server-side | Mutation required; read coverage pending |
| Organization usage/health | Aggregate only after metric source approval | Deny unless separately approved | Source and meaning need owner | Read logging unresolved |
| User metadata | Safe identity/profile/state after operation approval | Allowlisted profile/lifecycle action only after approval | Resolve User server-side | Mutation required |
| Membership metadata | C-02 projection only after operation approval | Invite/lifecycle/role action only after approval | Resolve membership and owning Organization | Mutation required |
| Project metadata | DATN-85-approved fields after operation approval | Explicit metadata/visibility operations only after approval | Resolve Project → Organization | Mutation required |
| Project ACL/leader metadata | Only fields supported by DATN-82 after operation approval | Explicit DATN-82-compatible action only after approval | Resolve Project/member relationship | Mutation required |
| Project/task/work content | **Deny** | **Deny** | Platform role does not imply Project/content permission | N/A |
| Document metadata | **Deny by default** | **Deny** | No approved platform content grant | N/A |
| Document content | **Deny** | **Deny** | No tenant-content permission | N/A |
| RAG index metadata/status | Safe status only after operation approval | Rebuild only after contract approval | No chunk/content access; owner scope checked | Mutation required |
| RAG retrieved chunks/context | **Deny** | **Deny** | No prompt/context/content access | N/A |
| Chat history/prompts | **Deny** | **Deny** | No conversation access | N/A |
| Job metadata | Safe operational fields only after approval | Retry/cancel/requeue only after approval | Resolve owning scope; omit payload/source content | Mutation required |
| Job payload/input/output | **Deny** | **Deny** | Not operational metadata | N/A |
| Service health/metrics | Allowlisted state/aggregate only after source approval | Finite controls only after approval | No host secrets; approved source/catalogue | Mutation required for controls |
| Error/diagnostic data | Sanitized bounded subset only after approval | No direct edits | Bounded identifiers/time; redact payloads | Read coverage pending |
| Audit data | Existing bounded read; export is not active and awaits per-operation disposition | Never edit/delete historical records | Allowlisted, bounded records | Export/read logging pending |
| Security events | Safe metadata only after approval | Named security action only after approval | Resolve target; no credential material | Mutations required |
| Integration metadata | Safe status only after approval | Finite operation only after approval | No secret values | Mutation coverage required |
| API keys, passwords, tokens, refresh tokens | **Never return** | Never accept replacement values through response | Secret store remains outside this contract | Never log value |
| Signing/private keys, MFA secrets, DB credentials | **Never return** | No secret storage change in DATN-294 | Secret store remains authoritative | Never log value |
| Configuration secrets | **Never return** | Configuration is deferred from active V1 by DATN-301; DEC-ACCESS-09 retains `FUTURE / DECISION_REQUIRED` | No V1 config operation | Out of scope |

No privileged tenant-content access is defined. If support needs it, that is a separate explicit policy decision; do not add it by implication or create Break-glass in V1.

## 9. Domain Boundaries

| Domain | V1 contract intent | Explicit boundary / current evidence | Status |
|---|---|---|---|
| Platform Dashboard | Approved aggregate summary | Not equivalent to health; sources/metrics need owner and privacy bounds | PROPOSED / BLOCKED on metrics |
| Organization | Read metadata; lifecycle/usage only if approved | Schema lacks status and usage; provisioning exists | PROPOSED |
| User / Account | Safe account metadata; allowlisted profile/status action | Active actor required; last-operator/self-state rules unresolved | PROPOSED / BLOCKED |
| Membership | Read/invite/lifecycle/role actions only if consistent with C-02 | Platform authority is not Organization ADMIN; preserve last-ADMIN/self/CAS | PROPOSED / BLOCKED |
| Project metadata/access | Metadata and explicit ACL/leader operations | Preserve DATN-82/85; no content/task access | PROPOSED / BLOCKED on authority composition |
| Session / Security | Safe session metadata and revoke | No credential/MFA data; IP/UA display unresolved | PROPOSED |
| Audit | Bounded read/export; never edit/delete history | Current projection narrow; DB immutability and complete event producers unproven | Existing read CONFIRMED; export PROPOSED / BLOCKED |
| Service / Health | Liveness plus separately approved health/metrics | Existing health is IAM liveness only | Existing liveness CONFIRMED; expansion PROPOSED |
| Job / Queue | Inspect state; finite retry/cancel/requeue | No shared control API/state machine established | PROPOSED / BLOCKED |
| RAG / Index | Index status and approved rebuild | No chunks, retrieved content or ACL bypass | PROPOSED / BLOCKED |
| Laya / AI | Runtime status and finite controls | SAG/Laya has separate product auth; shared platform authority/control interface unproven | PROPOSED / BLOCKED |
| LLM Provider | Non-secret status and finite approved management | No shared secret/provider control contract | PROPOSED / BLOCKED |
| Integration | Safe status and finite enable/disable/reconnect | Credential values never visible; common control interface absent | PROPOSED / BLOCKED |
| Configuration | Deferred; no permission or operation in active V1 | DEC-ACCESS-09 `FUTURE / DECISION_REQUIRED`; DATN-301 owner disposition in §24 | APPROVED DEFERRED from V1; Jira scope reconciliation complete |
| Incident | Read and defined lifecycle transitions | Incident state model/owner/error contract absent | PROPOSED / BLOCKED |
| Support / Diagnostic | Bounded sanitized diagnostics and finite support actions | No payload/tenant-content/secret exposure; action catalogue absent | PROPOSED / BLOCKED |
## 10. Authorization Behavior

| Condition | Contract behavior | Status / evidence |
|---|---|---|
| Unauthenticated, invalid, revoked/stale token | Reject before operation; 401 AUTHENTICATION_FAILED | [CONFIRMED] A-04/current auth and token revocation checks |
| Authenticated but missing exact permission | Deny; 403 FORBIDDEN | [CONFIRMED] A-04 and current platform guard |
| Organization ADMIN but not platform-authorized | Deny platform operation; Organization role is not a platform grant | [DERIVED] A-04 + role model |
| User not ACTIVE, including suspended/pending invite | Reject platform subject; do not evaluate target action | [CONFIRMED] Current subject resolution |
| Suspended/inactive Organization target | No operation until target lifecycle and eligibility are approved | [BLOCKED / NOT ACTIVE] New Organization lifecycle operations need per-operation disposition |
| Cross-Organization or cross-Project target | Resolve relation server-side; deny if outside approved target scope; conceal with 404 only where resource-hiding policy applies | [APPROVED POLICY] KeyT disposition 2026-10-16; exact target rules belong to each operation |
| Missing vs. forbidden target | Approved baseline: 403 for authenticated actor missing permission; 404 only for a resource class whose approved concealment policy requires hiding. Exact response for missing vs. existing-but-inaccessible target must be classified per resource class; do not reveal existence before that decision. | [PARTIAL / BLOCKED] DEC-ACCESS-10 owner must classify resource classes and update dependent contracts |
| Stale session/revoked token | Reject under existing token revocation behavior; session-target revoke awaits per-operation disposition | [CONFIRMED] Current auth; new session operation is [BLOCKED / NOT ACTIVE] |
| Authorization evidence unavailable/invalid | Fail closed; no target operation | [CONFIRMED] Platform guard |
| Resource state/version changed during mutation | Return 409 for an approved conflict/stale condition; never silently overwrite | [APPROVED POLICY] HTTP class; operation-specific code/state remains owner-defined |

Authorization order: authentication → verified actor → exact effective permission → server-resolved resource and relationships → current state/version and operation invariants → allow/deny → required mutation audit. Client-provided scope/resource IDs are never authorization evidence.

## 11. Error Contract

KeyT approved the following HTTP mapping and safe-response policy on 2026-10-16. Keep the current IAM envelope fields code, message, details and requestId; allowlist safe values per operation. This does not authorize new endpoints or invent stable error-code strings.

| Condition | HTTP | Contract behavior |
|---|---:|---|
| Unauthenticated/invalid/revoked token | 401 | Generic authentication failure; no token or auth internals |
| Authenticated but missing permission | 403 | Generic forbidden result; no permission-evidence internals |
| Missing/out-of-scope resource | 404 only where concealment applies | Do not reveal existence outside the approved resource policy |
| Invalid input or disallowed state | 422 | Safe validation/state details only |
| Conflict, stale version or duplicate mismatch | 409 | Safe conflict response; operation-specific retry behavior must be documented |
| Dependency unavailable | 503 | Generic dependency failure; no topology or secret; preserve requestId |
| Unexpected failure | 500 | Generic server failure; no stack trace, database detail or credential |

Per-operation details, stable codes, retryability and concealment target classes remain operation-level decisions and must be recorded before implementation. Do not return stack traces, secrets, raw payloads or concealed-resource identifiers.

## 12. Audit Contract

**[APPROVED POLICY]** The operator interface/API is append-only: this role cannot update or delete audit history. Every privileged mutation must fail closed. The system must not report mutation success unless the required audit event is durably recorded. Secret, credential, raw payload and tenant content are excluded from responses and audit metadata.

**[CURRENT EVIDENCE]** Existing Organization provisioning writes its audit event transactionally. The existing platform audit endpoint reads a bounded projection; it is not a general-purpose operator mutation log. Code inspection does not prove immutable storage or a complete grant/revoke producer.

**[BLOCKED FOR OWNER DISPOSITION]** Security/IAM must approve retention period and enforcement boundary. Security/Audit/domain owners must define per-operation event producers, required actor/target/action/result/time/request identifiers, reason requirements, redaction, read/export/denial treatment, durability mechanism and failure handling. The approved fail-closed policy is binding, but this document does not claim database-level tamper-proofing or select a transaction/outbox implementation.

Never include passwords, API keys, tokens, private keys, MFA values, raw job payloads, document content, chat history or retrieved RAG text. Detailed per-operation fields and test oracles belong in the approved operation records.

## 13. Secret Handling

**[CONFIRMED]** DATN-293 requires secrets not be returned to FE/API. **[DERIVED]** Management of an integration/provider reference does not authorize retrieval of its value. Never return API keys, passwords, access/refresh tokens, signing/private keys, MFA secrets or database credentials. Do not add a secret store in DATN-294. A future approved operation may accept a controlled secret-store reference or trigger rotation, but the interface and exact actions are not defined here; responses and audit contain only safe metadata/status.

## 14. Bootstrap Strategy

The policy controls below are approved, but Security/IAM has not named the issuer/executor or approved the operational runbook. This section is a boundary, not authority to bootstrap an operator.

1. **Identity:** recipient must be an existing verified ACTIVE user. No hidden user or production seed.
2. **Issuer:** Security/IAM must name an authorized issuer and executor, the identity source for both, and the evidence/change record. Until then first grant is BLOCKED.
3. **Assignment:** use the exact 40-code set from §5.2; the full grant is atomic and all-or-nothing. No partial set may resolve as PLATFORM_OPERATOR. Do not rewrite or auto-backfill standalone A-04 assignments.
4. **Self-grant:** no issuer may grant authority to itself. Do not expose public self-service bootstrap.
5. **Concurrency and replay:** grant/revoke operation must prevent duplicate or racing partial state. Idempotency details and persistence behavior are DATN-295/296 implementation decisions under the owner-approved contract.
6. **Audit:** every privileged mutation, including grant/revoke, must fail closed unless the required audit event is durable. Event fields, producer coverage and retention remain owner decisions.
7. **Recovery:** recovery for loss of the only operator, revoke, rollback and post-action verification must be in the signed Security/IAM runbook.
8. **No bypass:** no Break-glass, hidden admin, credential bypass, unattended default account or production seed.

**Readiness:** no bootstrap API, seed or production assignment may be implemented until Security/IAM signs the issuer, identity evidence and complete recovery runbook. “Use a manual process” alone is not a runbook.

## 15. Re-bootstrap / Recovery

No approved V1 recovery authority or runbook is evidenced. Recovery must not become an undocumented bypass.

| Phase | Proposed minimum control | Decision status |
|---|---|---|
| Normal bootstrap | Controlled, explicitly approved assignment to an existing ACTIVE user; exact permissions; auditable result; no self-grant | BLOCKED: issuer/process unknown |
| Re-bootstrap | Same approved authority path; verify current assignment state and prevent duplicates/races | BLOCKED: assigner and lifecycle policy unknown |
| Loss of only operator | Owner-approved operational recovery with identity verification, change record, two-person/other gate if chosen by security owner, audit and post-recovery verification | BLOCKED: no evidence to pick actors or gate |
| Rollback | Revoke only through approved assignment authority; verify effective permissions and session behavior | BLOCKED: revocation producer/completeness and issuer unknown |

V1 has no Break-glass flow, hidden admin account, credential bypass, production seed or arbitrary authenticated-user bootstrap. A manual operation can be a future runbook only after the responsible authority, preconditions, evidence, audit, rollback and verification steps are approved.

## 16. Non-goals

- No Break-glass, permission tiers, role hierarchy, `PLATFORM_ADMIN` or `PLATFORM_SUPPORT`.
- No IAM, Project ACL, Organization membership, RAG or ingestion redesign.
- No tenant-content permission implied by the platform role.
- No change to DATN-79 implementation or its three current permission codes.
- No runtime permission, API, database/schema/migration, seed, test implementation, FE/BE implementation or production-config change in DATN-294.
- No secret storage design or secret-value exposure.

## 17. Relationship with DATN-79 / A-04 Authorization Foundation

### Reuse

- Authentication, verified actor identity, active-user resolution and token revocation checks.
- Exact permission checks, `scope: PLATFORM`, current per-request assignment evidence and fail-closed guard behavior.
- Existing codes `organization.create`, `platform.health.read`, `platform.audit.read` without renaming or widening.
- Existing Organization provisioning transaction and bounded audit projection, within their current semantics.

### Not provided by DATN-79

- A `PLATFORM_OPERATOR` role or role→permission bundle.
- Runtime support or wildcard expansion for the 37 policy-approved but not-yet-enabled permissions.
- General Organization/User/Membership/Project/Session or operational-domain control plane.
- An approved first-operator issuer/bootstrap/recovery process.
- Proof of immutable audit storage or universal mutation-audit production.

### Handoff implications

- **DATN-295 DB:** implement exact-permission assignments for the approved 40-code set with atomic all-or-nothing grant/revoke. Issuer/runbook, retention and durable audit coverage remain blockers. Any DB change needs a separate migration, rollout and rollback plan; no schema is approved here.
- **DATN-296/297 BE:** consume only the approved operation/permission matrix; reuse A-04 guard/auth patterns; resolve target scope server-side; do not add wildcard or trust client scope. Keep the three existing codes compatible.
- **DATN-298/299 FE:** render only APIs and capabilities delivered by the approved BE contract; hide or disable actions based on server-authoritative capability response, not client role claims; never display secrets or tenant content from these APIs.
- **DATN-300 QA:** verify auth/permission/scope matrix, inactive/revoked actor/session, audit coverage/integrity, secret redaction, cross-tenant denial and DATN-79 / Organization / Project ACL regressions.

This DATN-294 contract does not change DATN-79. The 37 new permission identifiers have policy approval but remain absent from runtime until operation and implementation decisions are approved. The 37 new operations are `BLOCKED / NOT ACTIVE`, pending an authorized per-operation decision to approve active semantics or explicitly defer from V1.

## 18. Implementation Handoff

Every operation is assigned to at least one child task for delivery planning. A task assignment does not mean the operation is unblocked or approved.

| Contract item / operation IDs | DB | BE Administration (296) | BE Operations (297) | FE Administration (298) | FE Operations (299) | QA (300) |
|---|---|---|---|---|---|---|
| Permission registry, operator assignment, approved bootstrap/audit lifecycle | 295 | 296 | — | — | — | 300 |
| `PLAT-DASH-01`, `PLAT-ORG-01..04`, `PLAT-USER-01..03`, `PLAT-MEM-01..04`, `PLAT-PROJ-01..05`, `PLAT-SEC-01..02`, `PLAT-AUDIT-01..02` | 295 | 296 | — | 298 | — | 300 |
| `PLAT-HEALTH-01`, `PLAT-SVC-01..02`, `PLAT-JOB-01..04`, `PLAT-RAG-01..02`, `PLAT-AI-01..02`, `PLAT-LLM-01..02`, `PLAT-INT-01..02`, `PLAT-INC-01..02`, `PLAT-SUP-01..02` | 295 | — | 297 | — | 299 | 300 |
| Shared auth/errors/audit/secret redaction and cross-scope behavior | 295 | 296 | 297 | 298 | 299 | 300 |

DATN-295/296/297/298/299/300 are the expected owners from Jira. Configuration is deferred from active V1 by the DATN-301 disposition; DEC-ACCESS-09 itself leaves configuration read/write `FUTURE / DECISION_REQUIRED`. Dashboard metric ownership is unassigned at source level; PLAT-DASH-01 remains blocked until its data/source owner records an explicit operation disposition and contract.

## 19. Decision Register

| ID | Decision | Status | Evidence | Impact |
|---|---|---|---|---|
| PO-D01 | One full Platform Operator role, no permission tiers or hierarchy | APPROVED | User-approved V1 scope | Role model boundary |
| PO-D02 | Authentication mandatory; privileged mutations audited; no secret return; no Break-glass | APPROVED | User-approved scope and DATN-293 | All child tasks |
| PO-D03 | Preserve the three existing A-04 identifiers and semantics | APPROVED | DATN-79/A-04 and owner disposition | Compatibility |
| PO-D04 | Exact permission match and fail-closed current evidence | DERIVED | DATN_BE authorization policy/guard | No wildcard or stale-token authority |
| PO-D05 | Accept the exact 37 identifiers in §5.2 for the operator set | APPROVED POLICY; NOT RUNTIME | KeyT disposition 2026-10-16 | Implementation remains gated |
| PO-D06 | Platform grant scope remains separate from server-resolved target scope | DERIVED | A-04, DATN-82/85 | All target operations |
| PO-D07 | Exactly 3 existing + 37 new codes; Configuration deferred | APPROVED POLICY; NOT RUNTIME | KeyT disposition 2026-10-16; DEC-ACCESS-09 | Reconcile Epic/child scope; no runtime widening |
| PO-D08 | Platform authority grants no tenant-content visibility | APPROVED | DATN-85, A-04 boundary | Project/document/chat/RAG content |
| PO-D09 | Configuration read/write and management outside active V1 | APPROVED: DEFERRED | KeyT disposition; DEC-ACCESS-09 records `FUTURE / DECISION_REQUIRED` | No configuration permission/operation/API/UI |
| PO-D10 | Initial operator issuer and recovery path | BLOCKED | Security/IAM have not named issuer/executor or runbook | DATN-295/296 |
| PO-D11 | Exact assignments and atomic full-set grant/revoke | APPROVED POLICY; IMPLEMENTATION BLOCKED | KeyT disposition 2026-10-16; current exact-assignment model | DB/IAM transaction, idempotency and race implementation |
| PO-D12 | Audit API append-only; privileged mutation fail-closed | APPROVED POLICY; COVERAGE BLOCKED | KeyT disposition; code does not prove completeness | Retention, producers, redaction and durability remain gated |
| PO-D13 | Preserve 401/403; 404 only under concealment; 422/409/503/500 mapping | APPROVED BASELINE; RESOURCE CLASSES OPEN | KeyT disposition 2026-10-16; current IAM envelope | DEC-ACCESS-10 owner classifies resource concealment; per-operation stable codes/body details remain gated |
| PO-D14 | Per-operation disposition for Organization, User, Membership, Project, Session, Audit and Dashboard operations | BLOCKED / NOT ACTIVE | No authorized per-operation include/defer decision; required owner and semantics absent | DB/BE/FE/QA for affected operations |
| PO-D15 | Per-operation disposition for Service, Job, RAG, Laya, LLM, Integration, Incident, Support and Diagnostics operations | BLOCKED / NOT ACTIVE | Domain owner, source/control contract and semantics remain open | BE Ops/FE Ops/QA |
| PO-D16 | Dashboard metric source, ownership and PLAT-DASH-01 disposition | BLOCKED / NOT ACTIVE | No agreed source/catalogue or owner decision | BE/FE/QA |
| PO-D17 | Session IP/user-agent visibility | BLOCKED / NOT ACTIVE | Privacy display policy absent; PLAT-SEC-01 requires owner disposition | Privacy and FE scope |
| PO-D18 | Audit privileged reads/exports/denials and complete event coverage | BLOCKED | Security/Audit owner disposition remains open | DB/BE/QA |
| PO-D19 | Safe projections; no credentials or tenant content | APPROVED | User-approved secret and ACL boundary | All operations |
| PO-D20 | Effective operator set resolves only from exact 40 permission assignments | APPROVED POLICY; ISSUER BLOCKED | KeyT disposition; no role/bundle row selected | Bootstrap and exact-set persistence |

Authoritative approval details and remaining owner actions are recorded in §24. Policy approval does not imply implementation readiness.

## 20. Acceptance Checklist

- [x] Permission matrix identifies exactly 3 existing A-04 codes plus 37 approved new codes; approval is policy-only and does not enable runtime.
- [x] Exact-assignment storage and atomic all-or-nothing grant/revoke are decided; partial assignment is not a full operator.
- [x] Configuration is explicitly deferred from active V1 by DATN-301; Jira scope is reconciled. DEC-ACCESS-09 remains `FUTURE / DECISION_REQUIRED` for read/write.
- [x] 401/403, concealment-only 404, 422/409/503/500 and safe IAM response envelope are decided at policy level.
- [x] Operator API append-only and privileged-mutation fail-closed invariants are decided.
- [x] All 37 new operation IDs map one-to-one to the approved new permission set, and are marked `BLOCKED / NOT ACTIVE` until individual owner dispositions.
- [ ] Authorized domain owners explicitly disposition all 37 operations as active with complete operation records/test oracles or deferred from V1 with rationale/evidence.
- [x] Tenant-content and secret boundaries remain explicit.
- [ ] Security/IAM names issuer/executor and approves complete bootstrap/recovery/revoke/rollback runbook.
- [ ] Security/IAM approves audit retention and enforcement boundary.
- [ ] Security/Audit/domain owners complete audit producers, fields/reasons, redaction, read/export/denial policy and durable failure behavior.
- [x] KeyT-approved baseline mapping is recorded in the shared access-readiness source.
- [ ] DEC-ACCESS-10 owner classifies resource types that require concealment/404; corresponding API/security/FE contracts are updated.

**Acceptance result: PARTIAL; not ready to close DATN-301 or start DATN-295–300 implementation.** See §24 for remaining blockers and approved dispositions.

## 21. Open Risks / Blockers

| Priority | Remaining blocker / evidence gap | Decision/evidence needed | Affected tasks |
|---|---|---|---|
| Critical | First-operator issuer and recovery are not named | Security/IAM-approved identity verification, issuer/executor, controlled bootstrap, recovery, revoke and rollback runbook | 295, 296, 300 |
| Critical | Audit retention and durability enforcement are not defined | Security/IAM retention period; Audit/DB/BE evidence for durable fail-closed behavior | 295–300 |
| High | Audit producer/read/export/denial coverage and field policy are incomplete | Security/Audit/domain owner disposition; exclude sensitive data | 295–300 |
| Medium | DEC-ACCESS-10 has only a baseline; resource classes and missing-vs-forbidden outcomes are unspecified | Decision owner classifies resource types, decides missing vs existing-but-inaccessible responses, and updates dependent API/security/FE contracts | 294, 296, 297, 300 |
| Critical | No per-operation disposition exists for the 37 new operations | Named authorized domain owners approve each operation as active with complete semantics or explicitly defer it from V1; update Jira and contract per row | 296–300; 295 where persistence model depends on final active set |

## 22. Implementation Readiness TODO

1. **Security/IAM:** name the issuer/executor and approve bootstrap/recovery, identity evidence, no-self-grant, concurrency, revoke and rollback.
2. **Security/IAM:** approve audit retention and enforcement boundary.
3. **Security/Audit/domain owners:** define event coverage, required fields/reason, redaction, read/export/denial treatment and durability/failure handling.
4. **Per-operation disposition:** authorized domain owners must decide each new operation as active with a complete record/test oracle or explicitly deferred from V1 with rationale. Until then it is `BLOCKED / NOT ACTIVE`; do not infer deferral from missing approval.
5. **DEC-ACCESS-10 owner:** classify resource types requiring concealment/404. Keep the KeyT-approved baseline and update dependent API/security/FE acceptance.
6. **DATN-295–300:** remain blocked by applicable unresolved dependencies; do not add runtime codes or imply readiness from this policy approval.

## 23. Evidence References

### Jira decisions / dependencies

- DATN-293 — PLATFORM_OPERATOR V1 intent and domain scope (Epic).
- DATN-294 — this contract/spec task and its acceptance criteria.
- DATN-79 and A-04 subtasks DATN-190–194 — authorization foundation and accepted boundary.
- DATN-80, DATN-82, DATN-85, DATN-86–88 — Organization provisioning, Project access/public metadata, and membership administration.
- DATN-295–300 — DB, BE Administration, BE Operations, FE Administration, FE Operations and QA handoff.

### Repository evidence inspected (read-only)

- `DATN_BE` main snapshot `3b839198cfcbc40d6b11e1167ae8c68c54afea99`: `src/services/iam/infrastructure/mongodb/mongodb.schemas.ts`; `src/services/iam/application/authorization/authorization.policy.ts`; platform authorization guard; authentication application service; platform controller; organization provisioning service/repository; platform audit repository; `src/contracts/iam-openapi.spec.ts`.
- `DATN_BE` accepted contract: `docs/decisions/dec-access-09-platform-operator-authorization.md`; relevant IAM, membership, Project-access docs and tests were inspected for current policy boundaries.
- `DATN_FE` main snapshot `e6dbeedd94d3774cc91a3f6d9983d441a0294bf8`: searched platform routes/navigation; no Platform Operator console/route was found in the inspected paths.
- `sag-laya-integration` snapshot `780ff8499d041dcacfc7a37ce1e7f9b806c2b2c4`: `api/v1/jobs.py`, `api/v1/laya.py`, `api/v1/system.py`, `core/principal_assertion.py`, `core/config.py`; this shows SAG-specific auth/config paths, not shared DATN platform authority.
- `research-docs/Governance/02-role-permission-authorization.md` and `03-audit-outbox-contract.md`; `research-docs/Workspace/09-organization-membership-administration-v1.md`.
- No source inspected establishes a platform secret-management interface, unified control-plane API, approved first-operator issuer, or database-level audit immutability.

### Source interpretation

Accepted decisions are policy evidence; repository implementation establishes current behavior, not permission to widen it. Jira proposals alone do not establish runtime capability; DATN-301 approval establishes the finite permission membership only. Operation activation still requires its domain contract and implementation approval. Where evidence disagrees, preserve the accepted boundary and record the conflict.

## 24. DATN-301 Owner Disposition — 2026-10-16

This section is the current policy source of truth and supersedes conflicting PROPOSED/BLOCKED labels in earlier draft language and earlier versions of this contract. The disposition was explicitly approved by KeyT in the DATN-301 discussion on 2026-10-16. This record does not claim a Security/IAM sign-off that has not yet been supplied.

### Approved policy decisions

1. **Exact permission membership.** PLATFORM_OPERATOR V1 membership is exactly the three existing A-04 codes plus the 37 codes already enumerated in §5.2. No wildcard or additional code is approved. Keep all three existing codes and semantics unchanged. The approved 37-code set is policy only; it is not yet present in runtime.
2. **Assignment and role resolution.** Continue using exact per-permission assignment records; do not require a role/bundle row. The full 40-code operator grant and revoke must be atomic and all-or-nothing. A partial/corrupt set does not resolve to an effective PLATFORM_OPERATOR. Do not rewrite or automatically backfill existing standalone A-04 assignments. Transaction, idempotency, concurrency and persistence details belong to DATN-295/296.
3. **Configuration.** Platform Configuration is deferred from active V1 by the KeyT disposition recorded in DATN-301. DEC-ACCESS-09 itself leaves configuration read/write `FUTURE / DECISION_REQUIRED`. DATN-293, DATN-297 and DATN-299 must say it is out of scope. No Configuration permission, operation, API or UI is active. Reopening this area requires a new approved decision and an amendment to DEC-ACCESS-09.
4. **Authentication, authorization and errors.** Preserve 401 for unauthenticated/invalid authentication and 403 for authenticated actors missing permission. Use 404 only where the applicable resource-concealment policy requires hiding. Map invalid input/disallowed state to 422, conflict/stale/duplicate mismatch to 409, unavailable dependency to 503 and unexpected failure to 500. Keep the existing IAM response envelope fields code, message, details and requestId; allowlist safe details per operation. This approves the broad baseline only; the DEC-ACCESS-10 owner still must decide the missing-versus-forbidden behavior and concealment class for each resource. Do not invent stable code names or resource classes here.
5. **Audit invariants.** The operator interface/API cannot update or delete audit history. Every privileged mutation fails closed: do not return success unless the required event is durable. Never include secrets, credentials, raw payloads or tenant content in responses/audit metadata.

### Deferred and blocked decisions

- **Bootstrap/recovery — BLOCKED:** Security/IAM must name the authorized issuer and executor, identity-verification source, approval evidence and runbook for first grant, no-self-grant, race/idempotency, loss of the only operator, revoke, rollback and post-action verification. No seed, hidden account, public self-grant or Break-glass path.
- **Audit retention — BLOCKED:** Security/IAM must approve the retention period and enforcement boundary.
- **Audit completeness — BLOCKED:** Security/Audit/domain owners must define producers, required fields/reason, redaction, read/export/denial logging and durability/failure mechanism. Append-only API policy does not prove database-level immutability or complete producers.
- **Operation semantics — PARTIAL / BLOCKED:** Preserve only the three existing DATN-79 operations unchanged: PLAT-ORG-01, PLAT-HEALTH-01 and PLAT-AUDIT-01; their existing implementation semantics are summarized in §6 from A-04 evidence. For each of the 37 new operations, an authorized domain owner must either approve active semantics (preconditions/transitions, target/scope, input/output allowlist, repeat/concurrency, side effects/cost/rollback, audit and error behavior) and a test oracle, or explicitly defer it from V1 with rationale. Until then each row is `BLOCKED / NOT ACTIVE`. Exact IDs and permission mapping are listed in DATN-301/design.md §4 and the §6 disposition column.
- **DEC-ACCESS-10 — partial:** the shared access-readiness record now carries the KeyT-approved 2026-10-16 baseline. The decision owner must still classify which resource types require concealment/404; do not apply 404 outside those approved classes.

### Current task readiness

DATN-295–300 remain blocked by the unresolved items applicable to each task. In particular, DATN-295 is not ready to implement while no authorized issuer/runbook and durable audit contract exist. No Jira blocker link is removed by this record. The permission codes are approved for policy membership but remain absent from runtime; no schema/API/UI change is authorized here.

### Approval record

| Decision owner | Date | Approval evidence | Scope / limits |
|---|---|---|---|
| KeyT | 2026-10-16 | Explicit disposition in the DATN-301 conversation; Jira DATN-301 | Approves D1 exact 40-code permission-set policy and atomic exact-assignment model; D3 Configuration deferral; D4 baseline mapping/safe body; D5 append-only API and mutation fail-closed invariants. No final D6 disposition for the 37 operations is evidenced. Security/IAM issuer, recovery and retention sign-offs remain outstanding. |
