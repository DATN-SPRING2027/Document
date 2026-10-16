# PLATFORM_OPERATOR V1 Contract

| Field | Value |
|---|---|
| Status | Review draft; not implementation-approved |
| Jira | DATN-294; parent DATN-293 |
| Reviewed | 2026-10-16 (Asia/Bangkok) |
| Documentation repository | `Document-B05-reference` |
| Base branch / commit | `main` / `c8190aa3b3c9670ef96a9d651feba5e0de63e742` |
| Task branch | `feat/KeyT-platform-operator-v1-contract-bootstrap` |

> Canonical contract draft. Evidence is separated from new policy proposals. This document grants no runtime permission. DATN-294's “no implementation-affecting open decision” acceptance is **not met** while blockers/conflicts below remain.

## 1. Purpose

Define a reviewable V1 source of truth for DATN-295–300: permission names, operations, scopes, visibility, authorization, audit and bootstrap rules. Avoid widening DATN-79/A-04 authority accidentally.

## 2. Scope and evidence labels

V1 intends one platform role with the full set of **approved Platform Administration V1 permissions**, with no tiers or role hierarchy. “Full” means the finite approved operation set, not wildcard access, tenant-content access, authentication bypass or unrestricted CRUD.

- **[CONFIRMED]** Directly supported by accepted Jira decisions, approved docs or current code.
- **[DERIVED]** Follows from confirmed evidence without adding policy.
- **[PROPOSED]** New policy requiring owner/security approval before implementation.
- **[CONFLICT]** Sources disagree; implementation must wait for resolution.

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

**[PROPOSED, consistent with DATN-293]** One platform-level role whose effective permissions equal the finite approved Platform Administration V1 set. No `Observe`, `Operate`, `Security` or `Break-glass` tiers; no `PLATFORM_ADMIN`/`PLATFORM_SUPPORT`; no role hierarchy. It never bypasses authentication or middleware.

This role bundle is absent from runtime. Until expansion and bootstrap decisions are approved, only the three exact DATN-79 permissions remain usable under existing rules. This draft grants nothing new.

## 5. Permission Model

### 5.1 Naming and scope

**[PROPOSED]** Use `platform.<domain>.<resource>.<action>` for new permissions; preserve the three existing codes byte-for-byte. Never implement `PLATFORM_OPERATOR = *`.

`PLATFORM` is the grant scope, not a trusted target selector. The server resolves each target and derives its scope/relationships from authoritative storage. Client scope/parent IDs are selectors only and must be checked. Cross-Organization/Project relationships are validated server-side. Missing-resource concealment follows DEC-ACCESS-10.

### 5.2 Permission matrix

`ALLOW` is intended bundle membership after approval, not proof of runtime support. `DENY` is outside contract. Each target must be resolved server-side. Audit/error shorthand is detailed below.

| Permission | Domain | Action / resource | Grant / target scope | Role | Authorization | Visibility | Audit | Status / source |
|---|---|---|---|---|---|---|---|---|
| `organization.create` | Organization | Create Organization + first ADMIN | PLATFORM / new Organization | ALLOW | Exact current A-04; active subject; provisioning invariants | Input and safe created metadata | Required, transactional | [CONFIRMED] DATN-79 |
| `platform.health.read` | Service | Read IAM liveness | PLATFORM / service | ALLOW | Exact current permission | Liveness only | Read logging unresolved | [CONFIRMED] DATN-79 |
| `platform.audit.read` | Audit | Read filtered projection | PLATFORM / audit event | ALLOW | Exact current permission; bounded filters | Existing allowlisted fields | Read logging unresolved | [CONFIRMED] DATN-79 |
| `platform.dashboard.read` | Dashboard | Read approved aggregate counters | PLATFORM / aggregate | ALLOW | Active subject; approved metric sources | Aggregates only | Read logging proposed | [PROPOSED] DATN-293 |
| `platform.organizations.read` | Organization | Read metadata | PLATFORM / Organization | ALLOW | Resolve target server-side | Allowlisted metadata | Read logging proposed | [PROPOSED] |
| `platform.organizations.status.manage` | Organization | Suspend/reactivate | PLATFORM / Organization | ALLOW | Approved transition, reason, version | State and safe result | Required | [PROPOSED]; status absent in schema |
| `platform.organizations.usage.read` | Organization | Read usage/health counters | PLATFORM / Organization | ALLOW | Approved metric source/definition | Aggregates only | Read logging proposed | [PROPOSED]; counters absent |
| `platform.users.read` | User | Read account metadata | PLATFORM / User | ALLOW | Resolve target server-side | Safe identity/profile/state | Read logging proposed | [PROPOSED] |
| `platform.users.profile.manage` | User | Update allowlisted profile fields | PLATFORM / User | ALLOW | Field allowlist and version check | Safe profile only | Required | [PROPOSED] |
| `platform.users.status.manage` | User | Suspend/reactivate | PLATFORM / User | ALLOW | Lifecycle policy/reason/version; final-operator rule unresolved | State/result | Required | [PROPOSED]; lifecycle incomplete |
| `platform.memberships.read` | Membership | Read Organization membership | PLATFORM / membership→Organization | ALLOW | Resolve both; C-02 projection | Membership/role state | Read logging proposed | [PROPOSED]; preserve DATN-80/86–88 |
| `platform.memberships.invite` | Membership | Invite to Organization | PLATFORM / Organization | ALLOW | Reuse C-02 invite invariants | Safe invite result; no token | Required | [PROPOSED]; precedence needs approval |
| `platform.memberships.lifecycle.manage` | Membership | Suspend/reactivate/remove | PLATFORM / membership→Organization | ALLOW | C-02 last ADMIN, self-action, CAS/idempotency | Membership state | Required | [PROPOSED]; precedence needs approval |
| `platform.memberships.roles.manage` | Membership | Change Organization role | PLATFORM / membership→Organization | ALLOW | C-02 allowed transitions/actor rules | Role metadata | Required | [PROPOSED]; no invented grant power |
| `platform.projects.read` | Project | Read metadata | PLATFORM / Project→Organization | ALLOW | Resolve relation | Approved metadata only | Read logging proposed | [PROPOSED]; DATN-85 |
| `platform.projects.metadata.manage` | Project | Update allowlisted metadata | PLATFORM / Project→Organization | ALLOW | Field allowlist and version | Metadata only | Required | [PROPOSED] |
| `platform.projects.visibility.manage` | Project | Change visibility | PLATFORM / Project→Organization | ALLOW | Reuse DATN-82 | Visibility only | Required | [PROPOSED]; DATN-82 |
| `platform.projects.members.manage` | Project | List/add/remove Project member | PLATFORM / Project→Organization | ALLOW | Resolve Project/member; preserve DATN-82 ACL | ACL metadata, no content | Required | [PROPOSED]; composition unresolved |
| `platform.projects.leaders.manage` | Project | Assign/remove leader | PLATFORM / Project→Organization | ALLOW | DATN-82 leader constraints | Assignment metadata | Required | [PROPOSED]; reuse semantics |
| `platform.sessions.read` | Security | Read session metadata | PLATFORM / session→User | ALLOW | Resolve owner; privacy allowlist | Safe state/time/device; IP/UA unresolved | Read logging proposed | [PROPOSED] |
| `platform.sessions.revoke` | Security | Revoke session | PLATFORM / session→User | ALLOW | Exact permission; current state; idempotent repeat | Revocation result only | Required | [PROPOSED] |
| `platform.audit.export` | Audit | Export filtered audit events | PLATFORM / event set | ALLOW | Same projection as read; bounded output | No secrets/raw events | Export log proposed | [PROPOSED]; read/export logging open |
| `platform.services.health.read` | Service | Read approved service health | PLATFORM / service | ALLOW | Service allowlist | Health only | Read logging proposed | [PROPOSED]; only IAM liveness confirmed |
| `platform.services.metrics.read` | Service | Read approved metrics | PLATFORM / aggregate | ALLOW | Approved catalogue/dimensions | Aggregates only | Read logging proposed | [PROPOSED]; owner/source absent |
| `platform.jobs.read` | Queue | Inspect job state/metadata | PLATFORM / job→owner scope | ALLOW | Resolve owner scope; honor content ACL | Operational metadata, no payload | Read logging proposed | [PROPOSED] |
| `platform.jobs.retry` | Queue | Retry eligible job | PLATFORM / job→owner scope | ALLOW | State, budget, deduplication | State/result ref | Required | [PROPOSED]; state machine absent |
| `platform.jobs.cancel` | Queue | Cancel cancellable job | PLATFORM / job→owner scope | ALLOW | State and concurrency | State/result | Required | [PROPOSED]; state machine absent |
| `platform.jobs.requeue` | Queue | Requeue eligible job | PLATFORM / job→owner scope | ALLOW | Eligibility, dedupe/idempotency | State/result ref | Required | [PROPOSED]; semantics absent |
| `platform.rag.indexes.read` | RAG | Read index status | PLATFORM / index→owner scope | ALLOW | Resolve owner; preserve content ACL | Index status only, no chunks | Read logging proposed | [PROPOSED]; shared API absent |
| `platform.rag.indexes.rebuild` | RAG | Rebuild/reindex | PLATFORM / index→owner scope | ALLOW | Source/state, idempotency, job tracking | Operation status | Required | [PROPOSED]; owner/semantics absent |
| `platform.ai.runtime.read` | Laya | Read runtime/model status | PLATFORM / runtime | ALLOW | Approved runtime registry | No prompts/content | Read logging proposed | [PROPOSED]; shared authority absent |
| `platform.ai.runtime.manage` | Laya | Finite operational control | PLATFORM / runtime | ALLOW | Command allowlist and state checks | Safe status/result | Required | [PROPOSED]; control list absent |
| `platform.llm.providers.read` | LLM | Read provider/model status | PLATFORM / provider | ALLOW | Approved catalogue | Non-secret metadata | Read logging proposed | [PROPOSED] |
| `platform.llm.providers.manage` | LLM | Finite provider operation | PLATFORM / provider | ALLOW | Approved workflow; secret reference only | Redacted metadata | Required | [PROPOSED]; control/secret API absent |
| `platform.integrations.read` | Integration | Read metadata/status | PLATFORM / integration | ALLOW | Approved catalogue | Non-secret metadata | Read logging proposed | [PROPOSED] |
| `platform.integrations.manage` | Integration | Enable/disable/reconnect | PLATFORM / integration | ALLOW | Finite transitions; secret refs | Redacted result | Required | [PROPOSED]; control/secret API absent |
| `platform.configuration.read` | Configuration | Read approved config | PLATFORM / config key | DENY pending resolution | A-04 deferred config read/write | None until approved; never secret | Unresolved | [CONFLICT] DATN-293 vs DEC-ACCESS-09 |
| `platform.configuration.manage` | Configuration | Manage approved config | PLATFORM / config key | DENY pending resolution | A-04 deferred config read/write | Redacted only if approved | Unresolved | [CONFLICT] DATN-293 vs DEC-ACCESS-09 |
| `platform.incidents.read` | Incident | Read incident metadata | PLATFORM / incident | ALLOW | Resolve target; sanitized fields | Operational metadata | Read logging proposed | [PROPOSED]; contract absent |
| `platform.incidents.manage` | Incident | Create/update/resolve | PLATFORM / incident | ALLOW | Transition, reason, version rules | Safe state/summary | Required | [PROPOSED]; lifecycle absent |
| `platform.diagnostics.read` | Support | Read bounded diagnostics | PLATFORM / diagnostic ref | ALLOW | Exact IDs, bounded window, allowlist | Sanitized errors; no payload | Read logging proposed | [PROPOSED] |
| `platform.support.actions.manage` | Support | Finite support action | PLATFORM / resolved target | ALLOW | Per-action allowlist/state/reason | Safe result only | Required | [PROPOSED]; catalogue absent |

**Permission count: 42 rows = 3 confirmed existing codes + 37 proposed new codes + 2 conflicted Configuration codes.** Thirty-nine names are absent from runtime. Configuration rows must not be implemented before conflict resolution. ALLOW/DENY is intent only.
## 6. Operation Catalog

### 6.1 Shared rules

The actor for each row is an authenticated current `ACTIVE` user with the exact current platform permission. Server resolves targets and scope; client cannot assert trusted scope. Repeated mutations require defined idempotency; state changes need CAS/version checks where a stale write can overwrite newer state. Mutations return safe results and an operation/correlation ID when available. Errors beyond A-04 are unapproved; concealment depends on DEC-ACCESS-10. Proposed rows do not authorize implementation.

| Operation ID | Permission | Domain / action / resource | Scope / target resolution | Actor / authorization | Data returned | Mutation, audit, repeat/concurrency, destructive effect | Error |
|---|---|---|---|---|---|---|---|
| `PLAT-ORG-01` | `organization.create` | Org / create + first ADMIN | PLATFORM / new Org | Active subject; exact A-04; provisioning invariants | Safe created metadata, ADMIN reference | Mutation; transactional audit; request idempotency to confirm; not destructive | Existing validation/conflict; A-04 401/403 |
| `PLAT-HEALTH-01` | `platform.health.read` | Service / IAM liveness | PLATFORM / IAM process | Exact current permission | Liveness only | Read; no mutation; read log unresolved | A-04 401/403; dependency mapping open |
| `PLAT-AUDIT-01` | `platform.audit.read` | Audit / filtered projection | PLATFORM / allowlisted events | Exact current permission | Bounded projection, current max 100 | Read; no mutation; read log unresolved | A-04 401/403; invalid-filter convention |
| `PLAT-DASH-01` | `platform.dashboard.read` | Dashboard / approved summary | PLATFORM / aggregate sources | Exact permission; approve source allowlist | Approved counters | Read; read log proposed | 401/403; unavailable-source code open |
| `PLAT-ORG-02` | `platform.organizations.read` | Org / metadata read | PLATFORM / server-resolved Org | Exact permission; resolve target | Allowlisted metadata | Read; read log proposed | 401/403; 404 policy open |
| `PLAT-ORG-03` | `platform.organizations.status.manage` | Org / suspend/reactivate | PLATFORM / resolved Org | Exact permission; approved transition/reason/version | State and safe result | Mutation; audit; idempotency + CAS; suspend can interrupt service | 401/403; conflict/stale codes open |
| `PLAT-ORG-04` | `platform.organizations.usage.read` | Org / usage read | PLATFORM / resolved Org | Exact permission; approve metric source | Aggregates | Read; read log proposed | 401/403; metric-source code open |
| `PLAT-USER-01` | `platform.users.read` | User / metadata read | PLATFORM / resolved User | Exact permission; active actor | Safe identity/profile/state | Read; read log proposed | 401/403; concealment per DEC-ACCESS-10 |
| `PLAT-USER-02` | `platform.users.profile.manage` | User / allowlisted profile update | PLATFORM / resolved User | Exact permission; field allowlist/version | Safe updated profile | Mutation; audit + CAS; idempotency by field | 401/403; validation/stale codes open |
| `PLAT-USER-03` | `platform.users.status.manage` | User / suspend/reactivate | PLATFORM / resolved User | Exact permission; lifecycle/version policy | State/result | Mutation; audit + CAS/idempotency; may revoke access | 401/403; last-operator/self rules BLOCKED |
| `PLAT-MEM-01` | `platform.memberships.read` | Membership / read | PLATFORM / membership→Org | Exact permission; C-02 projection | Membership/role/state metadata | Read; read log proposed | 401/403; concealment open |
| `PLAT-MEM-02` | `platform.memberships.invite` | Membership / invite | PLATFORM / resolved Org | Exact permission; C-02 invite rules | Safe invite result, no token | Mutation; audit; idempotency required | 401/403; duplicate code open |
| `PLAT-MEM-03` | `platform.memberships.lifecycle.manage` | Membership / suspend/reactivate/remove | PLATFORM / membership→Org | Exact permission; C-02 last ADMIN/self/CAS invariants | Membership state | Mutation; audit + CAS/idempotent; removal affects access | 401/403; C-02 conflicts and concealment open |
| `PLAT-MEM-04` | `platform.memberships.roles.manage` | Membership / change role | PLATFORM / membership→Org | Exact permission; C-02 transitions | Role metadata | Mutation; audit + CAS/idempotent; may reduce access | 401/403; transition/conflict code open |
| `PLAT-PROJ-01` | `platform.projects.read` | Project / metadata read | PLATFORM / Project→Org | Exact permission; DATN-85 boundary | Metadata only | Read; read log proposed | 401/403; no content implication |
| `PLAT-PROJ-02` | `platform.projects.metadata.manage` | Project / update allowlist | PLATFORM / Project→Org | Exact permission; field allowlist/version | Updated metadata | Mutation; audit + CAS; field idempotency | 401/403; validation/stale codes open |
| `PLAT-PROJ-03` | `platform.projects.visibility.manage` | Project / visibility change | PLATFORM / Project→Org | Exact permission; DATN-82 | Visibility only | Mutation; audit + CAS/idempotency; broadens metadata reach only | 401/403; invalid-state/conflict open |
| `PLAT-PROJ-04` | `platform.projects.members.manage` | Project / list/add/remove member | PLATFORM / Project + member resolved | Exact permission; DATN-82 ACL composition | ACL metadata only | List read; add/remove audited + CAS/idempotent; removal affects access | 401/403; composition BLOCKED |
| `PLAT-PROJ-05` | `platform.projects.leaders.manage` | Project / assign/remove leader | PLATFORM / Project + Org member | Exact permission; DATN-82 constraints | Assignment metadata | Mutation; audit + CAS/idempotent; changes authority | 401/403; invalid-state code open |
| `PLAT-SEC-01` | `platform.sessions.read` | Security / session metadata | PLATFORM / session→User | Exact permission; privacy allowlist | Safe state/time/device; IP/UA unresolved | Read; read log proposed | 401/403; hiding open |
| `PLAT-SEC-02` | `platform.sessions.revoke` | Security / revoke session | PLATFORM / session→User | Exact permission; current state; no client owner assertion | Revocation result | Mutation; audit + CAS; idempotent repeat; invalidates session | 401/403; state/stale code open |
| `PLAT-AUDIT-02` | `platform.audit.export` | Audit / export filtered events | PLATFORM / same dataset as read | Exact permission; bounded projection/export | Same safe fields as read | Export; no mutation; export audit proposed | 401/403; size-limit error open |
| `PLAT-SVC-01` | `platform.services.health.read` | Service / approved health | PLATFORM / service registry | Exact permission; allowlist | Health state only | Read; read log proposed | 401/403; upstream code open |
| `PLAT-SVC-02` | `platform.services.metrics.read` | Service / metrics | PLATFORM / service + metric dimensions | Exact permission; approved catalogue | Aggregates only | Read; read log proposed | 401/403; source error open |
| `PLAT-JOB-01` | `platform.jobs.read` | Queue / inspect job | PLATFORM / job owner scope resolved | Exact permission; no content bypass | Operational metadata, no payload | Read; read log proposed | 401/403; concealment open |
| `PLAT-JOB-02` | `platform.jobs.retry` | Queue / retry job | PLATFORM / job owner resolved | Exact permission; retryable state/budget/dedupe | State/result ref | Mutation; audit + idempotency key + CAS; may repeat cost/side effects | 401/403; state/dependency code open |
| `PLAT-JOB-03` | `platform.jobs.cancel` | Queue / cancel job | PLATFORM / job owner resolved | Exact permission; cancellable state | State/result | Mutation; audit + CAS; idempotent terminal state; stops work | 401/403; state/stale code open |
| `PLAT-JOB-04` | `platform.jobs.requeue` | Queue / requeue job | PLATFORM / job owner resolved | Exact permission; eligibility/dedupe | State/result ref | Mutation; audit + key + CAS; schedules execution | 401/403; conflict/dependency code open |
| `PLAT-RAG-01` | `platform.rag.indexes.read` | RAG / index status | PLATFORM / index owner resolved | Exact permission; preserve content ACL | Status only, no chunks | Read; read log proposed | 401/403; hiding open |
| `PLAT-RAG-02` | `platform.rag.indexes.rebuild` | RAG / rebuild index | PLATFORM / index + source resolved | Exact permission; source/state/idempotency | Operation status | Mutation; audit + job tracking + CAS; resource/cost impact | 401/403; state/dependency open |
| `PLAT-AI-01` | `platform.ai.runtime.read` | Laya / runtime status | PLATFORM / registered runtime | Exact permission; approved registry | Status only; no prompts/content | Read; read log proposed | 401/403; authority integration absent |
| `PLAT-AI-02` | `platform.ai.runtime.manage` | Laya / finite control | PLATFORM / runtime resolved | Exact permission; command allowlist/state | Safe result/status | Mutation; audit; per-command idempotency; declare destructive effect | 401/403; command errors unapproved |
| `PLAT-LLM-01` | `platform.llm.providers.read` | LLM / provider status | PLATFORM / provider catalogue | Exact permission; redact secrets | Non-secret metadata | Read; read log proposed | 401/403; provider error map open |
| `PLAT-LLM-02` | `platform.llm.providers.manage` | LLM / finite provider operation | PLATFORM / provider resolved | Exact permission; approved workflow; secret ref only | Redacted metadata/result | Mutation; audit + CAS/idempotency; impact per action | 401/403; secret API absent |
| `PLAT-INT-01` | `platform.integrations.read` | Integration / status | PLATFORM / integration resolved | Exact permission; redact credentials | Non-secret metadata | Read; read log proposed | 401/403; dependency map open |
| `PLAT-INT-02` | `platform.integrations.manage` | Integration / enable/disable/reconnect | PLATFORM / integration resolved | Exact permission; finite transitions, secret refs | Redacted result | Mutation; audit + CAS/idempotency; may interrupt delivery | 401/403; control/secret API absent |
| `PLAT-CFG-01` | `platform.configuration.read` | Config / read allowlisted key | PLATFORM / config key resolved | Deny until A-04 conflict resolved | None approved | Not callable; audit unresolved | Do not implement |
| `PLAT-CFG-02` | `platform.configuration.manage` | Config / manage allowlisted key | PLATFORM / config key resolved | Deny until A-04 conflict resolved | Redacted only if later approved | Mutation/audit/idempotency unapproved | Do not implement |
| `PLAT-INC-01` | `platform.incidents.read` | Incident / metadata read | PLATFORM / incident resolved | Exact permission; sanitized fields | Operational metadata | Read; read log proposed | 401/403; source contract absent |
| `PLAT-INC-02` | `platform.incidents.manage` | Incident / create/update/resolve | PLATFORM / incident resolved | Exact permission; transition/reason/version | Safe state/summary | Mutation; audit + CAS/idempotency; resolution workflow effect | 401/403; lifecycle codes unapproved |
| `PLAT-SUP-01` | `platform.diagnostics.read` | Support / diagnostics lookup | PLATFORM / exact request/correlation/job/op ref | Exact permission; bounded window/allowlist | Sanitized diagnostics, no payload | Read; read log proposed | 401/403; disclosure policy open |
| `PLAT-SUP-02` | `platform.support.actions.manage` | Support / finite action | PLATFORM / target/action resolved server-side | Exact permission; action allowlist/state/reason | Safe result only | Mutation; audit + per-action CAS/idempotency; declare destructive effect | 401/403; action catalogue absent |

**Operation count: 42.** Each permission has exactly one operation row. Proposed/blocked rows do not authorize implementation.
## 7. Actor → Action → Resource → Scope

1. **Authenticate:** validate access token, current user state and revocation as the existing auth service does.
2. **Identify actor:** use the verified token subject; never trust a client-supplied actor ID.
3. **Resolve authority:** require the exact current permission. A role name alone, stale token claim or wildcard cannot authorize.
4. **Resolve target:** load target and parent relationships from the authoritative service/store. Client IDs are lookup inputs only.
5. **Evaluate state:** validate Organization/Project relationship, resource lifecycle, current version, and operation-specific invariants.
6. **Allow or deny:** fail closed on invalid/missing authorization evidence. Concealment of resource existence follows DEC-ACCESS-10, not a new rule here.
7. **Audit mutation:** persist the required audit record with the operation outcome.

Grant scope is PLATFORM for these platform permissions. Target scope remains distinct: PLATFORM, Organization, Project, or resource as shown per operation. A platform grant does not convert target scope, create Organization membership, or bypass Project ACL/content checks.

## 8. Data Visibility Boundary

Platform administration authority and tenant-content visibility are separate. This table is the proposed minimum-necessary boundary; proposed additions need approval before implementation.

| Resource/data | View | Mutate | Scope / condition | Audit |
|---|---|---|---|---|
| Organization metadata | Allow, allowlisted | Only explicit status/metadata operations after approval | Resolve Organization server-side | Mutation required; reads unresolved |
| Organization usage/health | Proposed aggregate only | Deny | Metric source/meaning must be approved | Read logging unresolved |
| User metadata | Allow, safe identity/profile/state | Only allowlisted profile/lifecycle actions after approval | Resolve User server-side | Mutation required |
| Membership metadata | Allow subject to C-02 | Only separately approved invite/lifecycle/role actions | Membership and owning Organization resolved | Mutation required |
| Project metadata | Allow approved fields | Only explicit metadata/visibility ops | Resolve Project→Organization; respect DATN-85 | Mutation required |
| Project ACL/leader metadata | Proposed | Only explicit DATN-82-compatible actions | Project and member relationship resolved | Mutation required |
| Project/task/work content | **Deny** | **Deny** | Platform role does not imply Project/content permission | N/A |
| Document metadata | **Deny by default** | **Deny** | No approved platform content grant | N/A |
| Document content | **Deny** | **Deny** | No tenant-content permission | N/A |
| RAG index metadata/status | Proposed allow | Rebuild only after contract approval | No chunk/content access; owner scope checked | Mutation required |
| RAG retrieved chunks/context | **Deny** | **Deny** | No prompt/context/content access | N/A |
| Chat history/prompts | **Deny** | **Deny** | No conversation access | N/A |
| Job metadata | Proposed safe operational fields | Retry/cancel/requeue only after approval | Resolve owning scope; omit payload/source content | Mutation required |
| Job payload/input/output | **Deny** | **Deny** | Not operational metadata | N/A |
| Service health/metrics | Proposed allowlisted state/aggregate | Only finite controls after approval | No host secrets; approved source/catalogue | Mutation required for controls |
| Error/diagnostic data | Proposed sanitized subset | No direct edits | Bounded identifiers/time; redact payloads | Reads proposed to log |
| Audit data | Existing filtered read; export proposed | Never edit/delete historical records | Allowlisted, bounded records | Export/read logging unresolved |
| Security events | Proposed safe metadata | Only named security actions, e.g. revoke session after approval | Resolve subject/resource, no credential material | Mutations required |
| Integration metadata | Proposed safe status | Finite operation only after approval | No secret values | Mutations required |
| API keys, passwords, tokens, refresh tokens | **Never return** | Never accept replacement values through response | Secret store remains outside this contract | Never log value |
| Signing/private keys, MFA secrets, DB credentials | **Never return** | No secret storage change in DATN-294 | Secret store remains authoritative | Never log value |
| Configuration secrets | **Never return** | Config permission is conflicted and blocked | No V1 config operation until decision | Unresolved |

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
| Configuration | None until read/write decision | A-04 defers configuration permission while DATN-293 lists full config | CONFLICT / BLOCKED |
| Incident | Read and defined lifecycle transitions | Incident state model/owner/error contract absent | PROPOSED / BLOCKED |
| Support / Diagnostic | Bounded sanitized diagnostics and finite support actions | No payload/tenant-content/secret exposure; action catalogue absent | PROPOSED / BLOCKED |
## 10. Authorization Behavior

| Condition | Contract behavior | Status / evidence |
|---|---|---|
| Unauthenticated, invalid, revoked/stale token | Reject before operation; `401 AUTHENTICATION_FAILED` | [CONFIRMED] A-04/current auth and token revocation checks |
| Authenticated but missing exact permission | Deny; `403 FORBIDDEN` | [CONFIRMED] A-04 and current platform guard |
| Organization ADMIN but not platform-authorized | Deny platform operation; Organization role is not a platform grant | [DERIVED] A-04 + role model |
| User not ACTIVE, including suspended/pending invite | Reject platform subject; do not evaluate target action | [CONFIRMED] Current subject resolution; HTTP mapping follows authentication convention |
| Suspended/inactive Organization target | No platform operation until Organization lifecycle semantics and target eligibility are approved | [PROPOSED/BLOCKED]; current schema lacks status |
| Cross-Organization or cross-Project target | Resolve relation server-side and deny if action is outside approved target scope | [DERIVED]; exact 403 vs concealed 404 depends on DEC-ACCESS-10 |
| Missing target | Apply existing resource-hiding policy; do not invent a universal 404 | [BLOCKED] DEC-ACCESS-10 remains open |
| Stale session/revoked token | Reject under existing token revocation behavior; session-target revoke remains a separate operation | [CONFIRMED] current auth; session API contract proposed |
| Authorization evidence unavailable/invalid | Fail closed; no target operation | [CONFIRMED] platform guard |
| Resource state/version changed during mutation | Reject or re-evaluate using approved conflict/stale contract; never silently overwrite | [DERIVED/PROPOSED]; new exact codes open |

Authorization order: authentication → verified actor → exact effective permission → server-resolved resource and relationships → current state/version and operation invariants → allow/deny → required mutation audit. Client-provided scope/resource IDs are never authorization evidence.

## 11. Error Contract

Only A-04's 401/403 behavior and current generic codes are confirmed. New operation-specific codes, conflict semantics, dependency mapping, and missing-versus-forbidden concealment require DEC-ACCESS-10 or domain-owner decisions. The table below is therefore a mapping contract proposal, not an approved API schema.

| Condition | HTTP | Error code | Message policy | Audit |
|---|---:|---|---|---|
| Unauthenticated/invalid/revoked token | 401 | `AUTHENTICATION_FAILED` | Generic; no token/auth internals | Denied-attempt audit policy unresolved |
| Authenticated but forbidden | 403 | `FORBIDDEN` | Generic; no permission-evidence internals | Denied-attempt audit policy unresolved |
| Missing resource | 404 only where approved hiding applies | DECISION_REQUIRED | Avoid revealing existence when policy requires hiding | No resource mutation |
| Invalid operation/input | 400 | Existing validation convention / code to confirm | Field-level safe detail only | Mutation attempt policy unresolved |
| Invalid current state | Proposed 409 | New code DECISION_REQUIRED | State-safe explanation | Record failed mutation only if audit policy approves |
| Conflict/duplicate/idempotency mismatch | Proposed 409 | New code DECISION_REQUIRED | No internal identifiers/secrets | Record outcome per audit policy |
| Stale version/CAS | Proposed 409 | New code DECISION_REQUIRED | Indicate reload/retry safely | Record outcome per audit policy |
| Service/dependency unavailable | Proposed 503 | New code DECISION_REQUIRED | Generic dependency failure; no topology/secrets | Preserve operation/correlation ID if available |
| Configuration/secret-provider failure | No config operation until conflict resolved; otherwise generic dependency failure | DECISION_REQUIRED | Never reveal value, path, key or provider credential | Do not log secret; audit attempted privileged change per approved policy |
| Unexpected failure | 500 | Existing generic server-error convention to confirm | Never stack trace, database detail or credential | Record sanitized correlation metadata only |

## 12. Audit Contract

**[CONFIRMED]** Existing Organization provisioning writes its audit event transactionally. Existing platform audit endpoint reads a bounded projection; it is not a general-purpose operator mutation log. Code inspection does not prove immutable storage or a complete grant/revoke producer.

**[PROPOSED]** Every successful privileged mutation in the approved catalog records:

- actor subject ID;
- action and stable operation ID;
- target resource type/ID and resolved target scope;
- timestamp;
- result (success/failure where failure logging is approved);
- request/correlation/operation ID where available;
- required reason for operations that need one;
- minimal before/after summary only if the event policy approves it.

Never include a password, API key, token, secret, private key, MFA value, raw job payload, document content, chat history or retrieved RAG text. Audit history is never editable/deletable via this role. Audit append-only enforcement, retention, redaction, export, read logging, denied-attempt logging, and grant/revoke event production are open decisions; DB-level immutability cannot be claimed from current service code alone.

## 13. Secret Handling

**[CONFIRMED]** DATN-293 requires secrets not be returned to FE/API. **[DERIVED]** Management of an integration/provider reference does not authorize retrieval of its value. Never return API keys, passwords, access/refresh tokens, signing/private keys, MFA secrets or database credentials. Do not add a secret store in DATN-294. A future approved operation may accept a controlled secret-store reference or trigger rotation, but the interface and exact actions are not defined here; responses and audit contain only safe metadata/status.

## 14. Bootstrap Strategy

The first operator is security-critical and is not resolved by A-04 or current implementation. The following is a **proposal for reviewer decision**, not an operational procedure authorized by this draft:

1. **Identity:** bind authority to an existing, verified user ID that is ACTIVE; do not create a hidden user or seed a production identity. [DERIVED/PROPOSED]
2. **Assignment point:** a controlled out-of-band operator assignment path with explicit change control is suggested; no such approved issuer/path is evidenced. [PROPOSED, BLOCKED]
3. **Execution:** one-time, explicitly authorized, idempotent and concurrency-safe; do not expose a self-service endpoint to any authenticated user. [PROPOSED]
4. **Authority bundle:** grant only the exact approved permission set, individually and visibly; whether grant is atomic across assignments is not supported by current schema and needs a DB decision. [PROPOSED, BLOCKED]
5. **Secret/config:** do not put credentials in FE, repository, audit or production seed. No bootstrap secret mechanism is designed here. [DERIVED]
6. **Self-grant:** operator cannot grant authority to itself or bootstrap itself through ordinary application requests. Current policy rejects self-grant; retain this invariant. [CONFIRMED]
7. **Initial issuer:** identity/role allowed to approve and execute the first assignment is unknown. No sufficient evidence to select an issuer. [BLOCKED]
8. **Audit:** initial assignment must produce an auditable actor, target, exact permissions, time, result and approved reason; existing event completeness/immutability is not proven. [PROPOSED, BLOCKED]
9. **Transaction/CAS:** required behavior for partial bundle assignment and concurrent bootstrap is not settled by current one-permission assignment model. [BLOCKED]
10. **Manual gate:** some controlled operational gate is necessary to prevent arbitrary self-bootstrap, but authorized people/process and recovery controls require security-owner decision. [DERIVED/BLOCKED]
11. **No production seed:** no seed or unattended default account is allowed by this task. [CONFIRMED from task scope]

**Bootstrap decision:** implementation cannot begin until the authorized issuer, assignment path, atomicity/lifecycle and bootstrap audit behavior are approved. “Use a manual process” alone is not a complete runbook.
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
- Wildcard/effective permission expansion for the proposed 37 permissions.
- General Organization/User/Membership/Project/Session or operational-domain control plane.
- An approved first-operator issuer/bootstrap/recovery process.
- Proof of immutable audit storage or universal mutation-audit production.

### Handoff implications

- **DATN-295 DB:** after approval, propose storage/index/lifecycle support for exact finite assignments and any approved target state/audit metadata. The current one-permission-per-assignment shape does not settle atomic role-bundle semantics. Any DB change needs migration, rollout and rollback plan; no schema is approved here.
- **DATN-296/297 BE:** consume only the approved operation/permission matrix; reuse A-04 guard/auth patterns; resolve target scope server-side; do not add wildcard or trust client scope. Keep the three existing codes compatible.
- **DATN-298/299 FE:** render only APIs and capabilities delivered by the approved BE contract; hide or disable actions based on server-authoritative capability response, not client role claims; never display secrets or tenant content from these APIs.
- **DATN-300 QA:** verify auth/permission/scope matrix, inactive/revoked actor/session, audit coverage/integrity, secret redaction, cross-tenant denial and DATN-79 / Organization / Project ACL regressions.

This DATN-294 draft does not change DATN-79. Any new permission remains design-only until the relevant owner decisions and implementation tasks are approved.

## 18. Implementation Handoff

Every operation is assigned to at least one child task for delivery planning. A task assignment does not mean the operation is unblocked or approved.

| Contract item / operation IDs | DB | BE Administration (296) | BE Operations (297) | FE Administration (298) | FE Operations (299) | QA (300) |
|---|---|---|---|---|---|---|
| Permission registry, operator assignment, approved bootstrap/audit lifecycle | 295 | 296 | — | — | — | 300 |
| `PLAT-DASH-01`, `PLAT-ORG-01..04`, `PLAT-USER-01..03`, `PLAT-MEM-01..04`, `PLAT-PROJ-01..05`, `PLAT-SEC-01..02`, `PLAT-AUDIT-01..02` | 295 | 296 | — | 298 | — | 300 |
| `PLAT-HEALTH-01`, `PLAT-SVC-01..02`, `PLAT-JOB-01..04`, `PLAT-RAG-01..02`, `PLAT-AI-01..02`, `PLAT-LLM-01..02`, `PLAT-INT-01..02`, `PLAT-CFG-01..02`, `PLAT-INC-01..02`, `PLAT-SUP-01..02` | 295 | — | 297 | — | 299 | 300 |
| Shared auth/errors/audit/secret redaction and cross-scope behavior | 295 | 296 | 297 | 298 | 299 | 300 |

DATN-295/296/297/298/299/300 are the expected owners from Jira. Configuration operations are listed for traceability only and have no implementation authorization while blocked. Dashboard metric ownership is unassigned at source level; the dashboard implementation row is blocked until data/source owners are named.

## 19. Decision Register

| ID | Decision | Status | Evidence | Impact |
|---|---|---|---|---|
| PO-D01 | V1 has one full Platform Operator role, no permission tiers or hierarchy | APPROVED | User's V1 scope and DATN-293 | Role model boundary |
| PO-D02 | Authentication remains mandatory; mutations audited; secret values never returned; no Break-glass | APPROVED | User-approved scope and DATN-293 | Applies to all child tasks |
| PO-D03 | Preserve only the three existing A-04 permissions unchanged until expansion approval | APPROVED | DATN-79/A-04 code and decision | Prevents accidental runtime widening |
| PO-D04 | Exact current permission match and fail-closed current evidence remain authorization baseline | DERIVED | DATN_BE authorization policy/guard | No wildcard or stale-token authority |
| PO-D05 | Namespace new permissions as `platform.<domain>.<resource>.<action>` | PROPOSED | Existing names plus explicit platform namespace | DB/BE permission identifiers |
| PO-D06 | Platform grant scope is separate from server-resolved Organization/Project/resource target scope | DERIVED | A-04 scope and DATN-82/85 boundaries | All target operations |
| PO-D07 | Adopt the finite 37-code expansion in this matrix (plus existing three), excluding conflicted config | PROPOSED | DATN-293 domain scope; operation draft | DB/BE/FE cannot implement until owner approves |
| PO-D08 | Platform admin authority does not grant tenant-content visibility | APPROVED | DATN-85, A-04 boundary, explicit V1 requirements | Protects Project/document/chat/RAG content |
| PO-D09 | Platform Configuration read/manage inclusion | BLOCKED | DATN-293 includes configuration; DEC-ACCESS-09/A-04 defers it | Must resolve before DATN-295–299 config work |
| PO-D10 | Initial operator issuer and bootstrap route/process | BLOCKED | No accepted issuer/runbook found in A-04/code | Critical bootstrap dependency |
| PO-D11 | Full permission-bundle atomicity and assignment lifecycle | BLOCKED | Current model stores exact individual assignments; no bundle atomicity decision | DATN-295/296 |
| PO-D12 | Audit immutability, complete producers, retention/redaction, read/export and denied-attempt logging | BLOCKED | Current append service/projection does not prove these controls | DB/BE/QA |
| PO-D13 | Missing-vs-forbidden behavior and new error-code matrix | BLOCKED | DEC-ACCESS-10 open; A-04 only settles 401/403 basics | BE/FE/QA contract |
| PO-D14 | Organization suspend/reactivate and usage fields/semantics | BLOCKED | Organization schema lacks status/counters; no accepted lifecycle definition found | DB/BE/FE |
| PO-D15 | Job, RAG, Laya, LLM, Integration, Incident and Support action/state semantics | BLOCKED | No unified operator contracts/control APIs found in DATN_BE/SAG | BE Ops/FE Ops/QA |
| PO-D16 | Dashboard metrics, aggregation window, source and owner | BLOCKED | No agreed source/catalogue found | BE/FE/QA |
| PO-D17 | Session IP/user-agent visibility | PROPOSED | Current session schema contains these fields; no display policy found | Privacy and FE scope |
| PO-D18 | Audit privileged reads and exports | PROPOSED | Existing endpoint is read-only projection; access logging policy unresolved | DB/BE/QA |
| PO-D19 | Safe projections and never returning credentials/content | DERIVED | DATN-293 secret boundary and DATN-85 content boundary | All operations |
| PO-D20 | Exact platform role-to-permission bundle and assigning authority | BLOCKED | No runtime role bundle or issuer found | Role resolution/bootstrap implementation |

**Status count: 4 APPROVED, 3 DERIVED, 4 PROPOSED, 9 BLOCKED (20 decisions).** The PROPOSED/BLOCKED items are implementation-affecting; this draft therefore cannot certify DATN-294's “no open implementation decision” acceptance.
## 20. Acceptance Checklist

This checklist records the present review state rather than marking blocked policy as complete.

- [x] Permission matrix has 42 rows with ID, domain, action/resource, scope, role intent, authorization, visibility, audit and evidence/status.
- [x] Operation catalog contains 42 concrete rows; each has one permission, actor, action/resource, scope, authorization, response data, mutation/audit, repeat/concurrency/destructive notes and error behavior.
- [x] Every catalog permission maps one-to-one to a permission-matrix row.
- [x] Sixteen required domains are covered.
- [x] Organization, User, Membership, Project, Session/Security, Audit, Job/RAG/Service/Integration/Configuration/Incident/Support boundaries are stated.
- [x] Actor → action → resource → scope flow is explicit; client scope is not trusted.
- [x] Tenant-content visibility is separated from platform administration.
- [x] Authentication, exact permission match and fail-closed baseline follow evidence.
- [x] Existing A-04 401/403 behavior is preserved; undecided concealment/errors are called out.
- [x] Audit fields, secret redaction, non-editable history and current audit evidence limits are documented.
- [x] Bootstrap and recovery questions are answered with proposals and explicit blockers; no production seed or hidden path.
- [x] Non-goals, DATN-79 relationship and child-task handoff are included.
- [x] Evidence labels prevent proposals/conflicts from being presented as approved policy.
- [ ] Permission expansion / exact role bundle is approved; 37 new codes remain proposals.
- [ ] Platform Configuration conflict is resolved.
- [ ] Initial operator issuer, bootstrap assignment, atomicity and recovery process are approved.
- [ ] DEC-ACCESS-10 settles resource concealment and new error behavior.
- [ ] Audit integrity/producers/read-export logging policy is approved.
- [ ] Organization lifecycle/usage and operational domain semantics have owners/contracts.
- [ ] Dashboard metrics and session IP/UA visibility are settled.
- [ ] Every proposed operation is implementation-ready without interpretation.

**Acceptance result: NOT READY for implementation.** The contract is detailed enough to review and make decisions, but source evidence is insufficient to approve critical policy choices without an owner/security reviewer decision. Do not mark DATN-294 complete or unblock child tasks based solely on this draft.

## 21. Open Risks / Blockers

| Priority | Blocker / evidence gap | Decision needed | Affected tasks |
|---|---|---|---|
| Critical | First operator issuer/bootstrap/recovery absent; current code has no approved assignment path | Name authorized issuer, verify identity, specify controlled assignment, idempotency/atomicity, audit and recovery | 294, 295, 296, 300 |
| Critical | 37 new permission IDs and role bundle are not in A-04/runtime | Approve exact finite bundle, names, role-resolution and assignment lifecycle | 294–300 |
| Critical | Configuration is in DATN-293 but deferred by DEC-ACCESS-09 | Resolve scope and amend decision before config permission/operations | 294–299 |
| High | Audit append code does not prove immutable history or full mutation producers | Define append-only enforcement, event coverage, redaction/retention, read/export and denied-attempt policy | 295–300 |
| High | DEC-ACCESS-10 is open | Set missing-vs-forbidden rule and new operation error codes | 294, 296, 297, 300 |
| High | Organization status/usage fields and lifecycle semantics are absent | Define suspension effects, reactivation, usage metrics and migration/rollback behavior | 295, 296, 298, 300 |
| High | Membership and Project authority composition for an operator is unapproved | Specify whether/how platform authority composes with C-02 and DATN-82 without altering ACL semantics | 294–300 |
| High | Queue/RAG/Laya/LLM/Integration/Incident/Support lack a shared operator API/state contract | Name service owners and define finite commands, eligibility, idempotency, cost and failure semantics | 294, 297, 299, 300 |
| High | Dashboard metrics have no source/catalogue/owner | Define aggregate fields, time window, source, privacy and freshness | 294, 296, 298, 300 |
| Medium | Session records contain IP/UA but display policy is not established | Approve safe session projection and retention/privacy limits | 294, 296, 298, 300 |
| Medium | Existing SAG/Laya service authentication is not proven to share DATN platform authority | Define trusted service-to-service identity and enforcement boundary before operator control | 294, 297, 299, 300 |

## 22. Implementation Readiness TODO

1. **Security/Platform owner:** decide PO-D07 expansion and PO-D20 role/bundle/issuer; keep the three A-04 permissions unchanged meanwhile.
2. **IAM owner:** resolve bootstrap and recovery (PO-D10/11); specify authorized issuer, approval evidence, no-self-grant, exact bundle application, concurrency and audit.
3. **Authorization owner:** resolve DEC-ACCESS-10 and PO-D13; define 404 concealment, operation errors and denied-attempt policy.
4. **Security/Audit owner:** approve PO-D12/18; prove immutable history and event producer coverage before mutation UI ships.
5. **Domain owners:** resolve PO-D09/14/15/16/17; publish config, Organization lifecycle, operational command, metric and session visibility contracts.
6. **DATN-295 DB:** only after the above approval, prepare a separate schema/index migration plan with rollout and rollback; no DB change is part of DATN-294.
7. **DATN-296/297 BE:** implement only approved rows; preserve A-04 exact matching, active subject, server-side target resolution and no-content boundary.
8. **DATN-298/299 FE:** consume approved server capabilities; do not infer authorization from a role selector or expose secrets/content.
9. **DATN-300 QA:** build positive/negative scope and permission cases, audit/secret checks, and regressions for DATN-79, C-02, DATN-82/85.
10. **Contract maintainer:** update this canonical file after each decision; do not copy competing permission lists into multiple documents.

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

Accepted decisions are policy evidence; repository implementation establishes current behavior, not permission to widen that behavior. Jira proposals are scope inputs, not evidence that a capability already exists or is approved. Where these sources disagree, this contract preserves the current accepted boundary and records a conflict for decision.
