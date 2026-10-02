# [RESEARCH] Roles, Capabilities, Evaluator & Access Control Baseline

**Ticket**: `DATN-16`  
**Assignee**: Nguyen Hong Phuc  
**Due Date**: Sep 26, 2026  
**Status**: Research Only (No coding, no configuration/dependency changes, no PR, no implementation)  
**Target System**: DATN / Continuum AI Baseline  

> **Decision update — 2026-10-02:** This is a dated implementation/evidence report. The current accepted hierarchy separates `PLATFORM_OPERATOR` from Organization roles; `ADMIN` manages Organization Users/membership/roles/scopes without default confidential-content access; `TEAM_LEADER` manages only explicitly assigned Project/Team scope; `MEMBER` access requires membership and ACL. BE DEC-016 establishes `OrganizationMembership` as the authoritative User–Organization relationship, with only `ACTIVE` establishing context. Project Foundation allows any authenticated User with active Organization Membership in matching trusted context to create a `PRIVATE` Project and atomically bootstrap creator Project Membership + project-scoped `MEMBER` assignment + audit. `project.create` is not required. Older grant-gate or undecided-bootstrap text below is superseded policy; implementation still needs verification.

---

## 1. Evidence Classification Standard (Truth Grading)

This research report strictly adheres to the project's evidence classification and truth grading standard:
- `[FACT / VERIFIED]`: Directly verified from existing source code in the repository (`DATN-BE`, `DATN-FE`).
- `[IMPLEMENTED]`: Executable behavior exists, is operational, and verifiable (not merely a schema, type definition, or interface).
- `[DESIGN / PROPOSED]`: Described in architecture documents, specifications, SRS, ADRs, or approved decisions, but not yet implemented in source code.
- `[PARTIAL]`: Supporting infrastructure/scaffolding exists (e.g., Mongoose schema, index declaration), but business logic or API layer is incomplete.
- `[GAP]`: Documented requirement exists in specifications but is completely absent from the current codebase.
- `[INFERENCE]`: Logical conclusion synthesized from multiple substantiated sources.
- `[UNKNOWN]`: Evidence is insufficient; no record found in documentation or source code.
- `[DECISION REQUIRED]`: Architectural discrepancies, unapproved matrices, or open policy points requiring team/lead consensus (do not invent unapproved matrices).

---

## 2. Executive Summary

1. `[FACT]` / `[PARTIAL]` **Data Model Scaffolding (Not Runtime Enforcement)**: The backend persistence layer (`DATN-BE`) contains Mongoose schema and index declarations for the 3 Persistent Human Roles (`ADMIN`, `TEAM_LEADER`, `MEMBER`), `role_assignments`, `organization_capability_grants` (limited to enum `'project.create'`), and specialized assignment collections (`sme_assignments`, `knowledge_owner_assignments`). However, this represents persistence-level scaffolding only; runtime evaluation and permission validation logic are entirely unbuilt.
2. `[GAP]` **Zero Evaluator & Guard in Backend**: Across the entire `DATN-BE/src` codebase, there are currently **no** NestJS Guards (`CanActivate`), Interceptors, Evaluator Services, or Custom Decorators (`@Roles()`, `@RequireCapability()`). The sole controller in IAM (`iam.controller.ts`) exposes only a basic `/health` check.
3. `[GAP]` **Missing 401 vs. 403 Transport Handling**: While `401 Unauthorized` and `403 Forbidden` response schemas are drafted in the OpenAPI specification (`DATN-BE/docs/openapi/iam-v1.openapi.json`), no NestJS exception filters, guards, or middleware currently enforce this distinction.
4. `[GAP]` **Frontend UI Is Static Template Only**: In `DATN-FE`, the codebase is an unmodified bootstrap from the TailAdmin Next.js template. The Zustand store (`src/stores/client-state.ts`) only manages `activeProjectId`, with zero user identity, role, or capability state. No UX gating helpers (`can(...)`, `<Authorize />`) exist.
5. `[APPROVED POLICY]` **Current Access Rules**: `PLATFORM_OPERATOR` is platform-scoped and has no default Organization-content access; `ADMIN` administers Organization membership/roles/scopes but has no default confidential-content access; `TEAM_LEADER` is limited to explicit Project/Team assignments; `MEMBER` is limited by membership and ACL. `OrganizationMembership` is authoritative and only `ACTIVE` establishes context. Any authenticated User with active Organization Membership in matching trusted context can create a `PRIVATE` Project without a role or `project.create` grant. Explicit deny wins; backend authorization is authoritative and FE checks are UX only.

---

## 3. Scope & Focus

### 3.1. In Scope:
- **3 Persistent Roles**: `ADMIN`, `TEAM_LEADER`, `MEMBER`, and the strict separation between roles and capabilities (Role vs. Capability boundaries).
- **Scope Hierarchy**: Organization Scope ➔ Project Scope ➔ Team Scope ➔ Domain / Resource ACL.
- **Project Creation**: Active Organization Membership and trusted context are required; `project.create` is not a gate. Remaining capability grant policy is separate and unresolved.
- **Evaluator & Guard Status**: Current implementation state of NestJS Guards, Decorators, and Deny Precedence resolution.
- **401 Unauthorized vs. 403 Forbidden Boundaries**: Authentication failure vs. authorization/scope failure; authoritative backend enforcement vs. frontend UX gating.
- **Cross-Scope & Privilege Escalation Scenarios**: Cross-tenant isolation, cross-project protection, and separation of duties.

### 3.2. Out of Scope:
- Writing implementation code, modifying runtime configurations, adding dependencies, or creating pull requests.
- Deciding or inventing an unapproved detailed permission matrix without formal Lead approval.

---

## 4. Verified Requirements Checklist

| Requirement / Architectural Item | Source Evidence | Truth Grade | Current Codebase Finding & Status |
| :--- | :--- | :--- | :--- |
| **3 Persistent Roles: `ADMIN`, `TEAM_LEADER`, `MEMBER`** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Sec. 1); `05_SECURITY...md` (Sec. 1.1) | `[FACT]` / `[PARTIAL]` | Schema `roles` in `DATN-BE/.../mongodb.schemas.ts:107-119` declares enum `['ADMIN', 'TEAM_LEADER', 'MEMBER']`. Seed migration and role management endpoints are missing. |
| **Superseded role names forbidden (`PROJECT_MANAGER`, `PROJECT_ADMIN`, `TEAM_MEMBER`)** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Sec. 1) | `[FACT]` | Zero occurrences of superseded role names found in backend schemas or types. |
| **SME, KNOWLEDGE_OWNER, SUCCESSOR are Scoped Assignments, not Roles** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Sec. 4) | `[FACT]` / `[PARTIAL]` | `sme_assignments` and `knowledge_owner_assignments` exist as distinct collections in `DATN-BE/.../mongodb.schemas.ts`, decoupled from persistent roles. |
| **ONBOARDING / OFFBOARDING are lifecycle states, not Roles** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Sec. 4) | `[FACT]` / `[PARTIAL]` | `users.status` in Mongoose schema defines `['ACTIVE', 'SUSPENDED', 'PENDING_INVITE']`. Membership lifecycle states (`ONBOARDING`/`OFFBOARDING`) are documented in design but absent from schema. |
| **Legacy Project-create grant schema** | `mongodb.schemas.ts:139`; BE Project Foundation decision | `[FACT]` / `[SUPERSEDED POLICY]` | Schema defines `capability: 'project.create'`, but the grant is not required for current Project creation. Other grant policies are unaffected. |
| **Hierarchical Containment: Org ➔ Project ➔ Team ➔ Resource** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Sec. 2) | `[FACT]` / `[PARTIAL]` | `projects`, `teams`, `project_memberships`, and `team_memberships` schemas enforce foreign key references reflecting this strict hierarchy. |
| **Deny Precedence (Explicit Deny takes precedence)** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Sec. 2); `05_SECURITY...md` (Sec. 2) | `[DESIGN]` / `[GAP]` | Defined mathematically ($P_{\text{eff}} = \dots \setminus \text{ExplicitDeny}$); zero executable logic or checks exist in backend code. |
| **NestJS Evaluator / Guard Enforcement in Backend** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Sec. 6) | `[GAP]` | No class implements `CanActivate`, no `@UseGuards()`, and no permission evaluation service exists in `DATN-BE/src`. |
| **Distinct Error Boundaries: 401 Unauthorized vs. 403 Forbidden** | `iam-v1.openapi.json:670-685` | `[PARTIAL]` / `[GAP]` | OpenAPI spec defines both responses. Backend controllers do not emit them yet. Frontend `api-client.ts` lumps all HTTP errors into generic strings. |
| **Frontend UX-only Checks (route gating, conditional actions)** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Sec. 2) | `[GAP]` | Zero role/capability checks, context stores, or `<Can />` components exist in `DATN-FE/src`. |

---

## 5. Core Business Rules & Boundaries

### 5.1. Roles and Capability Boundaries (Role vs. Capability)
1. **BR-AUTH-01 (Role Boundary)**: `[APPROVED POLICY]` `ADMIN`, `TEAM_LEADER`, and `MEMBER` are persistent Organization/Project roles; `PLATFORM_OPERATOR` is a separate platform-scoped actor. SME, Knowledge Owner, and Successor are scoped assignments.
2. **BR-AUTH-02 (Admin and Platform Boundary)**: `[APPROVED POLICY]` Platform operations do not grant default Organization-content access. An `ADMIN` manages Organization Users/membership/roles/scopes but has no default confidential Project-content access.
3. **BR-AUTH-03 (Organization Membership Context)**: `[APPROVED BE DECISION: DEC-016]` `OrganizationMembership` is authoritative; only `ACTIVE` establishes Organization Context. RoleAssignment alone is insufficient.
4. **BR-AUTH-04 (Explicit Team Leader Scope)**: `[APPROVED POLICY]` A `TEAM_LEADER` manages only explicitly assigned Project/Team scope and cannot self-grant broader authority.
5. **BR-AUTH-05 (Project Creation Rule)**: `[APPROVED BE DECISION: Project Foundation]` Any authenticated User with active Organization Membership in matching trusted context may create a `PRIVATE` Project. The creator receives active Project Membership and project-scoped `MEMBER` RoleAssignment with the audit event atomically; no role or `project.create` grant is required.
6. **BR-AUTH-06 (Deny and Enforcement)**: `[DESIGN]` Explicit deny wins; backend authorization is authoritative and FE checks are UX only.

### 5.2. Scope Hierarchy & Access Control Checks (Scope & ACL)
1. **BR-SCOPE-01 (Hierarchical Containment)**: `[FACT]` / `[DESIGN]` Access evaluation requires strict containment validation:
   $$\text{Organization Context} \supseteq \text{Project Context} \supseteq \text{Team Context} \supseteq \text{Resource ACL}$$
   Requests attempting to access resources across organizational or unassigned project boundaries must be rejected immediately.
2. **BR-SCOPE-02 (Pre-Retrieval Scoped ACL)**: `[DESIGN]` Effective permissions must be calculated before database queries or before injecting context into the LLM pipeline:
   $$P_{\text{eff}} = \left( P_{\text{user}} \cup P_{\text{teams}} \cup P_{\text{roles}} \right) \cap \text{SourceACL} \cap \text{Lifecycle}(\text{ACTIVE}) \setminus \text{ExplicitDeny}$$
3. **BR-SCOPE-03 (Deny Precedence)**: `[DESIGN]` If any condition yields an explicit Deny (e.g., capability revoked, account `SUSPENDED`, status `OFFBOARDING`, or explicit resource ACL Deny), access is denied unconditionally, overriding any positive role or grant.

### 5.3. Error Response Boundaries: 401 Unauthorized vs. 403 Forbidden
1. **BR-ERR-01 (401 Unauthorized / Unauthenticated)**:
   - **Definition**: The caller's identity is **unauthenticated, missing, invalid, or expired**.
   - **Trigger Conditions**:
     + Missing `Authorization: Bearer <token>` header.
     + Malformed token, signature verification failure, or expired access token.
     + JWT ID (`jti`) present in the Redis immediate revocation blacklist.
     + Invalid refresh token or detected refresh token family reuse attack.
   - **Client/Frontend Action**: Clear stale session tokens and redirect the user to `/signin` (or trigger silent token rotation).
2. **BR-ERR-02 (403 Forbidden / Unauthorized Scope)**:
   - **Definition**: The caller is **authenticated**, but **lacks required permissions** for the requested scope or resource.
   - **Trigger Conditions**:
     + User with role `MEMBER` attempting administrative operations (e.g., creating teams).
     + Active Organization member with no `project.create` grant creating a Project is allowed; missing/non-active membership, mismatched context, or inactive subject is denied.
     + Expired (`expiresAt < now()`) or revoked (`revokedAt !== null`) capability grant.
     + Non-member attempting access to project resources (`project_memberships.status !== 'ACTIVE'`).
     + Operation blocked by explicit Deny Precedence or resource ACL.
   - **Client/Frontend Action**: Display an "Access Denied / Insufficient Permissions" view. **Must never redirect to `/signin`** (which creates infinite redirect loops).
3. **BR-ERR-03 (Authoritative Backend Boundary vs. FE UX-only)**:
   - **Backend Guard**: Authoritative and mandatory security barrier. Every incoming API call must pass server-side authentication and capability evaluation.
   - **Frontend Check**: Purely visual UX gating (e.g., disabling buttons, hiding the "Create Project" link). Client-side checks must never be relied upon for security enforcement.

---

## 6. Requirement ➔ Evidence ➔ Implementation ➔ Gap Matrix

| Architectural Layer | Requirement | Specification Evidence | Source Implementation | Technical Gap |
| :--- | :--- | :--- | :--- | :--- |
| **Database Schema** | Store 3 Persistent Roles | `02_ACTORS_ROLES...md:11`; `05_SECURITY...md:23` | `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:107-119` (`roles`) | `[PARTIAL]` Schema has enum `ADMIN`, `TEAM_LEADER`, `MEMBER`. Missing seed migration for default role documents. |
| **Database Schema** | Scoped Role Assignments | `02_ACTORS_ROLES...md:27` | `DATN-BE/.../mongodb.schemas.ts:120-134` (`role_assignments`) | `[PARTIAL]` Compound unique index `{ organizationId: 1, projectId: 1, userId: 1 }`. Null handling for org-level roles (`projectId: null`) requires verification. |
| **Database Schema** | Time-bounded `project.create` Grants | `02_ACTORS_ROLES...md:13,84` | `DATN-BE/.../mongodb.schemas.ts:135-150` (`organization_capability_grants`) | `[FACT]` Complete schema with `capability`, `grantedBy`, `reason`, `expiresAt`, `revokedAt`. Index `{ organizationId: 1, userId: 1, capability: 1, revokedAt: 1 }`. |
| **API Contract** | Project creation and capability grants | BE Project Foundation decision; `iam-v1.openapi.json` | `[GAP / CONTRACT ALIGNMENT]` The earlier OpenAPI `project.create` requirement is superseded for Project creation. Align route authorization with active Organization Membership and trusted context; other grant routes need a separate contract. |
| **Backend Logic** | Capability Evaluator & Deny Precedence | `02_ACTORS_ROLES...md:84-85` | Zero files in `DATN-BE/src` | `[GAP]` Missing `CapabilityEvaluatorService` and effective permission calculator. |
| **Backend Guards** | NestJS Guards for 401 & 403 Enforcement | `02_ACTORS_ROLES...md:25`; `05_SECURITY...md:49` | Zero files in `DATN-BE/src` | `[GAP]` Missing `JwtAuthGuard` (401), `RolesGuard` (403), `CapabilityGuard` (403), and `ProjectScopeGuard` (403). |
| **Frontend State** | Store user identity, roles, and grants | Architecture baseline | `DATN-FE/src/stores/client-state.ts` | `[GAP]` Zustand store only holds `activeProjectId`. Lacks user profile, roles, and granted capabilities. |
| **Frontend UX** | UX gating for Project Creation | `02_ACTORS_ROLES...md:25` | `DATN-FE/src` | `[GAP]` No `<Can capability="..." />` component or `useCapability()` hook. UI is static TailAdmin template. |
| **Integration / E2E** | Automated tests for 401/403 and Deny | CI/CD Quality Gate | `DATN-BE/test` | `[GAP]` Test suite only validates `/health`. Zero test coverage for authorization, evaluator, or error boundaries. |

---

## 7. API / Data / Security Findings

### 7.1. Data Model & Storage Insights
1. **Organization-Level Role Assignment (`projectId: null`)**:
   - `role_assignments` uses a compound unique index: `{ organizationId: 1, projectId: 1, userId: 1 }`.
   - For an Organization Admin, `projectId` is `null` (or omitted).
   - In MongoDB, `null` is indexed as an explicit value. This correctly restricts a user to at most one organization-level role assignment per organization. The implementation must adopt a consistent convention (storing literal `null` vs. sparse indexing).
2. **Capability Enum Hardcoding**:
   - In `organization_capability_grants`, `capability` is strictly constrained to `enum: ['project.create']`.
   - This is a source-schema fact only. It does not establish that `project.create` is an active authorization gate (it is not required by the accepted Project Foundation decision) or that no other capabilities/policies exist. The remaining grant model is not fully specified.

### 7.2. API Contract Findings (OpenAPI vs. Implementation)
1. **Missing Capability Grant Management Endpoints**:
   - In `DATN-BE/docs/openapi/iam-v1.openapi.json`, `POST /api/v1/projects` explicitly specifies:
     `"description": "Requires organization Admin or an active project.create capability grant."`
     and defines `403 Forbidden` response. This is an earlier OpenAPI snapshot superseded for Project creation by the Project Foundation decision; align the OpenAPI before implementation.
   - Any capability-grant management contract is separate; do not make it a prerequisite for Project creation.

### 7.3. Security & Privilege Escalation Vulnerabilities
1. **Client-Side State Tampering Risk**:
   - If the application relied solely on client-side state to authorize project creation, malicious actors could forge API requests via Postman/curl.
    - **Non-Negotiable Rule**: The backend must evaluate database/cache state on every Project-create invocation:
      + Caller is an authenticated active subject, has trusted matching Organization Context, and has `OrganizationMembership.status = ACTIVE` for that Organization.
      + Validate Project input and code uniqueness, then atomically write the `PRIVATE` Project, creator Project Membership, project-scoped `MEMBER` RoleAssignment, and audit event. No role or `project.create` grant is required.
2. **Token Revocation Lag (Stateful vs. Stateless)**:
   - If capability grants were encoded directly inside short-lived JWT access tokens, a revoked grant would remain usable until token expiration (up to 15 minutes).
   - **Design Mitigation**: Membership and scope changes affecting sensitive access must be checked against authoritative state or a safely invalidated cache. Capability expiry is a separate policy and does not control Project creation.

---

## 8. Frontend / Backend Mismatches

| Domain | Backend (`DATN-BE`) | Frontend (`DATN-FE`) | Mismatch Description |
| :--- | :--- | :--- | :--- |
| **HTTP Status Handling** | OpenAPI defines `401 Unauthorized` and `403 Forbidden` | `src/lib/api-client.ts` lumps all `!response.ok` into a generic error string | **Critical**: Frontend cannot differentiate between expired sessions (requiring signin redirect) and permission denial (requiring an Access Denied banner). |
| **Identity & Role State** | Schema stores `userId`, `organizationId`, `roleCode`, `capability` | Zustand store (`client-state.ts`) only holds `activeProjectId` | **Gap**: Frontend has no access to user roles or capabilities for conditional rendering. |
| **BFF Header Forwarding** | Backend requires request identity and context headers | `src/lib/bff-proxy.ts` whitelist only includes standard headers (`accept`, `authorization`, `cookie`, `x-request-id`) | **Partial**: Auth token passes through `authorization`, but custom tenant headers are stripped. |
| **Project Creation UI** | Any authenticated active Organization member may create | UI template has no project creation form or modal | **Unimplemented**: Project creation flow is absent; UX should reflect membership/context, with backend enforcement authoritative. |

---

## 9. Dependencies & Blockers

1. **Authentication Service & JWT Claims**:
   - The Evaluator requires an authenticated principal on `request.user`. Authorization is strictly blocked until the Auth module verifies JWT signatures and attaches the decoded payload.
2. **Organization Context (DATN-15)**:
   - Organization and project scope validation requires resolving the request's `organizationId` from session context or request headers.
3. **Redis Infrastructure**:
   - Immediate access token revocation checks (<1ms) and high-performance evaluator caching depend on a functional Redis connection.

---

## 10. UNKNOWN & DECISION REQUIRED Register

In compliance with the directive **"Do not decide an unapproved matrix"**, the following architectural questions remain recorded as open decisions:

- `[DECISION REQUIRED]` **DR-01: Cross-Scope Resource Response: HTTP 403 Forbidden vs. HTTP 404 Not Found?**
  - *Option A*: Return `403 Forbidden` (Transparent, easier to debug, but enables Resource ID enumeration attacks).
  - *Option B (Security Best Practice)*: Return `404 Not Found` for resources outside the user's organization or project scope (hiding resource existence), reserving `403 Forbidden` strictly for unauthorized actions on visible resources.
- `[DECISION REQUIRED]` **DR-02: Detailed Permission Matrix Approval**
  - Section 5 of `02_ACTORS_ROLES_AND_PERMISSIONS.md` outlines high-level permissions for 10 core actions. Team Lead consensus is required to approve the complete mapping for all 20 listed permission codes before backend enforcement logic is coded.
- `[UNKNOWN]` **UN-01: Explicit Deny Storage Mechanism**
  - The permission formula requires subtracting `ExplicitDeny`. Schema currently lacks an explicit deny rule collection. Must determine whether Deny is dynamically configurable in database or statically enforced in business logic (e.g., account `SUSPENDED`).
- `[UNKNOWN]` **UN-02: Retained Grant Expiration Strategy**
  - If the legacy `project.create` grant value or other capability grants remain in use outside Project creation, should expiry use scheduled cleanup or passive validity filtering? This does not block the approved Project-create rule.

---

## 11. Implementation Breakdown Recommendation

In accordance with [AI_WORKFLOW.md](../../AI_WORKFLOW.md), implementation must be separated into three distinct branches and PRs:

```text
[ 1. DATABASE PR ] ────────► [ 2. BACKEND PR ] ────────► [ 3. FRONTEND PR ]
 (Schema & Seeds)            (Guards & Evaluator)        (UX Gating & Errors)
```

### Step 1: Database Branch & PR (`feat/Phuc-roles-capabilities-db`)
- **Scope**:
  + Refine `role_assignments` and `organization_capability_grants` schemas in `DATN-BE`.
  + Verify compound unique index behavior on `role_assignments` when `projectId` is null.
  + Add a database seed migration to populate the 3 default system roles: `ADMIN`, `TEAM_LEADER`, `MEMBER`.
- **Acceptance Criteria**: Seed executes idempotently; indexes are created successfully in MongoDB.

### Step 2: Backend Branch & PR (`feat/Phuc-roles-capabilities-evaluator-be-api`)
- **Scope**:
  + Implement `JwtAuthGuard`: Validate Bearer token, verify against Redis blacklist; emit `401 Unauthorized`.
  + Implement `CapabilityEvaluatorService`: Enforce effective permission calculation and Deny Precedence.
  + Implement Decorators and Guards:
    * Organization-context and active-membership guard for Project creation; do not attach `@RequireCapability('project.create')` to this operation.
    * `@Roles('ADMIN')` paired with `RolesGuard`.
    * Protect `POST /api/v1/projects`: Emit `403 Forbidden` if caller lacks required authority.
  + Add Admin API endpoints to grant/revoke capabilities.
  + Write unit and integration tests covering 401, 403, and grant expiration scenarios.
- **Acceptance Criteria**: 100% test pass rate; API accurately reflects OpenAPI contract error codes.

### Step 3: Frontend Branch & PR (`feat/Phuc-roles-capabilities-fe-ui`)
- **Scope**:
  + Enhance `api-client.ts`: Intercept HTTP status codes (redirect to `/signin` on `401`; throw structured forbidden error on `403`).
  + Add User Identity and Capability state to Zustand client store.
  + Create UX gating components (`<Can capability="..." />` and `useCanCapability()` hook).
  + Conditionally render the "Create Project" action based on capability check.
  + Implement a user-friendly `403 Access Denied` error page.
- **Acceptance Criteria**: Unauthorized users cannot see project creation triggers; direct URL navigation presents a clean 403 message without infinite redirect loops.
