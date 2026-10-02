# [RESEARCH] Governance - Organization Context

> This is an evidence and gap report. Its `[DESIGN]` statements and non-binding recommendations are not product approval. Cross-document Organization/Workspace decisions are indexed in [Organization and Workspace Access Contract Readiness](../Workspace/00-organization-and-access-contract-readiness.md).

**Ticket**: `DATN-15`  
**Assignee**: Nguyen Hong Phuc  
**Due Date**: Sep 26, 2026  
**Status**: Research Only (No implementation, no code changes, no configuration/dependency changes)  
**Target System**: DATN / Continuum AI Baseline  

> **Policy update — 2026-10-02:** This report's source inventory is a dated implementation snapshot. The accepted governance model now places `PLATFORM_OPERATOR` at platform scope (provisioning/bootstrap/health/configuration; no default Organization-content access), `ADMIN` at Organization scope (Users/membership/role/scope/Organization administration; no default confidential-content access), and `TEAM_LEADER`/`MEMBER` at explicitly assigned Project/Team scope. BE DEC-016 makes `OrganizationMembership` the authoritative User–Organization relationship and defines `ACTIVE` as the only state that establishes Organization Context. The Project Foundation decision allows any authenticated User with active Organization Membership in the trusted Organization to create a `PRIVATE` Project and bootstraps the creator as Project `MEMBER`; `project.create` is not required. Older role-assignment linkage and grant-gate descriptions below are historical snapshots, not current policy. Runtime implementation still requires verification against these decisions.

---

## 1. Evidence Classification Standard (Truth Grading)

This report strictly adheres to the project's evidence classification and truth grading standard:
- `[FACT / VERIFIED]`: Directly verified from existing source code in the repository.
- `[IMPLEMENTED]`: Executable behavior exists and is operational (not merely a schema or interface).
- `[DESIGN / PROPOSED]`: Described in architecture documents, specifications, SRS, or ADRs, but not yet implemented in code.
- `[PARTIAL]`: Supporting infrastructure/scaffolding exists (e.g., database schema), but business logic/API is incomplete.
- `[GAP]`: Documented requirement exists in specifications but is completely absent from the current codebase.
- `[INFERENCE]`: Logical conclusion synthesized from multiple substantiated sources.
- `[UNKNOWN]`: Evidence is insufficient; no record found in documentation or source code.
- `[DECISION REQUIRED]`: Architectural discrepancies or open policy points requiring team/lead consensus.

---

## 2. Executive Summary

1. `[FACT]` / `[PARTIAL]` **Data Model Scaffolding (Not Runtime Enforcement)**: The backend persistence layer (`DATN-BE`) contains schema and index scaffolding declaring `organizationId` (`ObjectId`) across most domain-scoped collections (`projects`, `teams`, `lifecycle_*`, `jira_*`, `documents`, `handover_*`). However, this is persistence-level scaffolding only, NOT runtime enforcement: global entities (`users`, `organizations`, `roles`) are not organization-scoped, `auditSchema.organizationId` is optional (`organizationId?: string`), and executable guards or query tenant filters are completely absent.
2. `[FACT]` / `[PARTIAL]` **Session Binding**: The `refresh_sessions` collection in the IAM module binds user sessions to a specific organization via `(userId, organizationId)`. This confirms that user sessions are intended to operate within an explicit organization context.
3. `[GAP]` **Zero Context Resolution in Code**: At the backend HTTP transport layer (`DATN-BE/src/common/http`), only `request-id.middleware.ts` (`x-request-id`) currently exists. There is **no** Middleware, Interceptor, or Custom Param Decorator implemented to extract, resolve, or attach `organizationId` to the execution context.
4. `[GAP]` **Zero Authorization Guards in Code**: No NestJS Guards (`CanActivate`) currently exist anywhere in `DATN-BE/src` to enforce organization scope or execute Cross-Organization Denial.
5. `[GAP]` **Frontend Organization State**: In `DATN-FE`, the Zustand store (`src/stores/client-state.ts`) only contains `activeProjectId`, completely lacking an `activeOrganizationId`. Furthermore, Next.js BFF Proxy (`src/lib/bff-proxy.ts`) maintains a fixed header whitelist that **omits** `x-organization-id`, meaning incoming organization headers would be stripped before reaching the backend.

---

## 3. Scope & Focus

### In Scope:
- Organization scope and domain boundaries: `User ➔ Organization` and `Resource ➔ Organization` relationships.
- Request context resolution mechanisms (Header vs. JWT Payload vs. Route Param).
- Cross-organization access denial and tenant boundary isolation.
- Dependencies of Project and Team authorization upon Organization Context.
- Comparative analysis between architectural specifications (`Document/architecture/05_SECURITY_AND_GOVERNANCE.md`, `02_ACTORS_ROLES_AND_PERMISSIONS.md`) and actual source code (`DATN-BE`, `DATN-FE`).

### Out of Scope:
- Modifying production code, changing runtime configurations, adding dependencies, or creating implementation PRs.
- Speculating or inventing arbitrary multi-organization switching behaviors not established in project specifications.

---

## 4. Verified Requirements Checklist

| Requirement | Evidence Source | Classification | Technical Finding & Notes |
| :--- | :--- | :--- | :--- |
| **Organization is the top-level isolation boundary** | `05_SECURITY_AND_GOVERNANCE.md`; `02_ACTORS_ROLES_AND_PERMISSIONS.md` | `[DESIGN]` | All projects, teams, documents, and knowledge assets belong to an Organization. |
| **Organizations collection exists in persistence** | `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts` | `[FACT]` | Collection `organizations` defines `name`, `slug` (unique index), `plan` (`FREE` \| `ENTERPRISE`), and `settings`. |
| **Users schema does not hardcode `organizationId`** | `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts` | `[FACT]` | `users` schema defines `email`, `passwordHash`, `fullName`, `avatarUrl`, `status`, `twoFactorEnabled`, `twoFactorSecretEncrypted`, and `lastLoginAt` (without `organizationId`). User-to-Organization relationship is Many-to-Many via intermediate collections. |
| **User ➔ Organization linkage** | BE DEC-016; prior `DATN-BE/.../mongodb.schemas.ts` inventory | `[APPROVED POLICY]` / `[IMPLEMENTATION GAP]` | `OrganizationMembership` is authoritative; an Organization-scoped RoleAssignment alone is insufficient. The cited schema inventory predates or does not implement the accepted contract; verify current schema/API/backfill. |
| **Resources carry mandatory `organizationId` in scoped collections** | All `persistence.ts` across `DATN-BE/src/services/*` | `[FACT]` | `projects`, `teams`, `jira_connections`, `documents` (and `document_versions`), and `knowledge_objects` require `organizationId` with compound indexes. (Note: `audit_logs` declares optional `organizationId?: string`). |
| **Session model binds to Organization** | `refresh_sessions` schema in IAM service | `[FACT]` | Schema explicitly declares `userId: ObjectId` and `organizationId: ObjectId`. |
| **Request Context Resolution via JWT Claims** | `05_SECURITY_AND_GOVERNANCE.md` (Section 2) | `[DESIGN]` | Pre-Retrieval ACL specifies decoding JWT to extract `userId`, `roles`, and `teamIds`. |
| **Middleware / Guard for Organization Context** | `DATN-BE/src/common/http` | `[GAP]` | No middleware, interceptor, or guard exists to validate or inject `organizationId` into the request pipeline. |
| **Cross-Organization Access Denial** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Section 2) | `[DESIGN]` | Explicit rule: "Deny takes precedence. Cross-tenant or cross-project access must be explicitly authorized, not inferred." |
| **Backend Cross-Tenant Enforcement** | `DATN-BE/src` | `[GAP]` | No Guard or Mongoose Tenant Filter plugin exists to reject cross-tenant resource access automatically. |
| **Frontend Organization State / Switcher** | `DATN-FE/src/stores/client-state.ts`, `src/context` | `[GAP]` | Zustand store only holds `activeProjectId`. No `activeOrganizationId` or Organization Switcher UI exists. |
| **BFF Proxy Header Forwarding** | `DATN-FE/src/lib/bff-proxy.ts` | `[GAP]` | Whitelist `forwardedHeaders` does NOT include `x-organization-id`. |

---

## 5. Core Business Rules

### 5.1. Verified & Design Rules
1. **BR-ORG-01 (Tenant Isolation Boundary)**: `[DESIGN]` A request is only permitted to access or mutate resources whose `organizationId` matches the authenticated session's resolved Organization Context.
2. **BR-ORG-02 (Hierarchical Containment)**: `[FACT]` / `[DESIGN]` Strict hierarchy is enforced:
   $$\text{Organization} \longrightarrow \text{Project} \longrightarrow \text{Team} \longrightarrow \text{Domain / Resource ACL}$$
   No standalone Project or Team can exist without an owning Organization.
3. **BR-ORG-03 (Active Membership and Project Creation)**: `[APPROVED POLICY]` Only an authenticated User with `ACTIVE` Organization Membership in the trusted matching Organization Context may create a Project. The Project is `PRIVATE`; creator bootstrap adds active Project Membership and project-scoped `MEMBER` RoleAssignment with the Project-create audit event. No Organization role or `project.create` grant is required. The legacy grant schema is not removed by this rule.
4. **BR-ORG-04 (Platform and Organization Admin Boundaries)**: `[APPROVED POLICY]` `PLATFORM_OPERATOR` provisions Organizations, bootstraps the first `ADMIN`, and monitors platform health/configuration, but has no default Organization-content access. `ADMIN` manages Organization membership, role/scope and Organization settings, but does **not** have default access to view or verify confidential Project/Team content.
5. **BR-ORG-05 (Scoped Project/Team Leadership)**: `[APPROVED POLICY]` `TEAM_LEADER` manages only explicitly assigned Project/Team scope and cannot self-grant broader scope. `MEMBER` access remains bounded by membership and resource ACL.
6. **BR-ORG-06 (Audit Provenance)**: `[APPROVED POLICY]` Project creation and other high-privilege mutations must emit auditable records with actor, Organization/scope, action and target. Exact event/schema alignment remains an implementation contract gap.

### 5.2. Open Rules & Discrepancies (`[UNKNOWN]` / `[DECISION REQUIRED]`)
- **BR-ORG-UN01**: Does an invalid cross-organization resource request return HTTP `403 Forbidden` or HTTP `404 Not Found`?
- **BR-ORG-UN02**: Can a user session operate across multiple active organizations concurrently, or is each issued Access Token restricted to exactly one active organization?

---

## 6. Requirement ➔ Evidence ➔ Implementation ➔ Gap Matrix

| Architectural Layer | Requirement | Specification Evidence | Source Implementation | Technical Gap |
| :--- | :--- | :--- | :--- | :--- |
| **Database Schema** | Store Organization entities & metadata | `05_SECURITY...md`, `SPEC.md` | Schema `organizations` exists in `DATN-BE` (`continuum_iam`) | `[PARTIAL]` Initial database seed migration for default organization is missing. |
| **Database Schema** | User-Organization Membership & Roles | BE DEC-016; `02_ACTORS...md` | Historical inventory cited `role_assignments` and `organization_capability_grants` | `[IMPLEMENTATION GAP]` The accepted model requires authoritative `OrganizationMembership`; verify its collection/API, unique `(organizationId, userId)` pair, status vocabulary and idempotent historical backfill. RoleAssignment remains role data, not membership proof. |
| **API Contract** | Transport protocol for Organization Context | `05_SECURITY...md` | No business endpoints implemented beyond `/health` | `[GAP]` No contract established: Header `X-Organization-Id` vs. JWT claim vs. URL path parameter. |
| **Business Logic** | Extract and validate Organization Context | `05_SECURITY...md` (Section 2) | `DATN-BE/src/common/http` only contains `request-id` | `[GAP]` Missing `OrgContextMiddleware` or Interceptor to populate `request.orgContext`. |
| **Security / Guard** | Prevent Cross-Organization Access | `02_ACTORS...md` (Section 2) | No Guards found in `DATN-BE/src` | `[GAP]` Missing `OrgScopeGuard` to reject requests where `request.orgId !== resource.orgId`. |
| **Frontend UI** | Manage active Organization State | TailAdmin specifications | `DATN-FE/src/stores/client-state.ts` | `[GAP]` Missing `activeOrganizationId` in Zustand store and missing Organization Switcher component. |
| **BFF Layer** | Forward Organization Header to Backend | BFF specification | `DATN-FE/src/lib/bff-proxy.ts` | `[GAP]` `x-organization-id` is missing from `forwardedHeaders` array. |
| **Integration / E2E** | Automated tests for cross-tenant rejection | `DATN-BE/docs/SPEC.md` | `DATN-BE/test` only covers `/health` (Checks 0 on GitHub PR) | `[GAP]` `[UNIMPLEMENTED]` Zero automated tests exist for tenant isolation or cross-tenant rejection; this remains an explicit gap rather than a validated security result. |

---

## 7. API, Data & Security Findings

### 7.1. Data & Schema Findings
- **Domain Entity Schema Scaffolding**: Domain services (`iam`, `lifecycle`, `jira`, `ingestion`, `handover`, `notification`) declare `organizationId` on their scoped business entities, but this is static schema scaffolding, not runtime enforcement. Crucially: global entities (`users`, `organizations`, `roles`) do not have an `organizationId` scope; `audit_logs` defines `organizationId` as optional (`{ type: String, index: true }`); and no automated tenant query filters or guards exist at runtime.
- **Optimized Compound Indexing**: Primary queries leverage compound indexes prefixed by `organizationId`:
  - `projects`: `{ organizationId: 1, code: 1 }`
  - `teams`: `{ organizationId: 1, projectId: 1, code: 1 }`
  - `lifecycle_proposals`: `{ organizationId: 1, projectId: 1, status: 1 }`
  - `documents`: `{ organizationId: 1, projectId: 1, status: 1, createdAt: 1 }`
  This enables deterministic query filtering and partition isolation in MongoDB once runtime tenant parameters are supplied.

### 7.2. API & Context Resolution Findings
- No unified convention currently exists across BE and FE for passing Organization Context:
  - **Option 1 (Header-based)**: Client supplies `X-Organization-Id: <id>` with each request.
  - **Option 2 (Token-based)**: Client supplies Bearer JWT containing an `org_id` claim. Switching organization requires token re-issuance.
  - **Option 3 (URL-based)**: Endpoints follow `/api/v1/organizations/:orgId/...`.

### 7.3. Security & Vulnerability Analysis
- **Insecure Direct Object Reference (IDOR) Risk**: If future services query MongoDB by document `_id` alone without enforcing `{ organizationId: currentOrgId }`, users could access cross-tenant data.
- **Architectural Safeguard**: Implement a global Mongoose Tenant Plugin or Base Repository pattern to inject tenant isolation filters automatically into all `find`, `update`, and `delete` operations.

---

## 8. Frontend & Backend Mismatches & BFF Findings

Based on the latest source code synchronized from `DATN-FE` (`origin/main`):

1. **Client State Store (`src/stores/client-state.ts`)**:
   - `[FACT]` Zustand store currently defines only `activeProjectId: string | null` and `setActiveProjectId`.
   - `[GAP]` **`activeOrganizationId` is completely missing**.
2. **User Identity Contract (`src/lib/queries/auth/useAuth.ts`)**:
   - `[FACT]` The `CurrentUserResponse` interface from `/users/me` already defines `organizationId: string`:
     ```typescript
     export type CurrentUserResponse = Readonly<{
       id: string;
       email: string;
       name: string;
       organizationId: string;
       roles: readonly string[];
     }>;
     ```
   - `[INFERENCE]` The frontend assumes each user belongs to a default active organization upon authentication.
3. **BFF Proxy Header Dropping (`src/lib/bff-proxy.ts`)**:
   - `[FACT]` The Next.js BFF proxy restricts forwarded headers to an explicit whitelist:
     ```typescript
     const forwardedHeaders = [
       'accept',
       'authorization',
       'content-type',
       'cookie',
       'x-request-id',
     ];
     ```
   - `[GAP / WARNING]` **Integration Defect**: `x-organization-id` is **NOT** present in `forwardedHeaders`. If the client attaches this header, the BFF proxy will silently strip it before the request reaches the backend.
4. **URL Routing Architecture**:
   - Routes follow `/[locale]/(admin)/...` with no organizational route slug. Organization context must therefore be resolved through state/headers rather than URL segments.

---

## 9. Dependencies for Project & Team Authorization

Project and Team authorization strictly depend on Organization Context via the following authorization chain:

$$\text{Authentication (Identity Verified)} \longrightarrow \mathbf{\text{Organization Context}} \longrightarrow \text{Project Scope} \longrightarrow \text{Team Scope}$$

1. **Project Entry Gate**: A user must possess a valid, active association within the target Organization before any project-level access can be evaluated. If the organization status is suspended or invalid, all downstream access is denied immediately.
2. **Project Creation Rule**: Require authenticated active subject, trusted matching Organization Context, and `ACTIVE` Organization Membership. Do not gate on `ADMIN`, `TEAM_LEADER`, or `organization_capability_grants.project.create`. Bootstrap the new Project as `PRIVATE` with creator Project Membership, project-scoped `MEMBER`, and audit atomically.
3. **Team Boundary**: Teams inherit the composite key `(organizationId, projectId)`. Team access control checks cannot execute without validating the parent organization context.

---

## 10. UNKNOWN / DECISION REQUIRED

> [!IMPORTANT]
> The architectural items below (`DEC-01`, `DEC-02`, and `DEC-03`) remain unaccepted and pending official decision. All recommendations provided are **strictly non-binding exploratory options** for team discussion and must not be treated as approved requirements until the team lead / architecture authority explicitly decides.

| Decision ID | Architectural Question | Viable Options | Non-Binding Recommendation (Pending Lead Decision) |
| :--- | :--- | :--- | :--- |
| **DEC-01** | **Organization Context transport protocol in HTTP requests** | A. HTTP Header `X-Organization-Id`<br>B. Claims in JWT payload<br>C. URL Route Parameter (`/organizations/:orgId/...`) | **Option B + A (Non-binding suggestion)**: JWT carries the default `org_id` for the session; support `X-Organization-Id` for explicit tenant context switching when a user belongs to multiple organizations. |
| **DEC-02** | **HTTP status code for Cross-Organization Access Denial** | A. `403 Forbidden`<br>B. `404 Not Found` | **Option B (404 Not Found) (Non-binding suggestion)** for specific resource requests to prevent tenant enumeration and information leakage. Use `403 Forbidden` only when the user lacks rights to the overall Organization Context. |
| **DEC-03** | **Multi-Organization user scope for MVP** | A. Full multi-org switching in UI<br>B. Database supports multi-org, but MVP UI fixes to default organization | **Option B (Non-binding suggestion)**: Maintain multi-tenant schema readiness in DB while constraining MVP UI to a single active organization to maintain velocity. |

---

## 11. Implementation-Breakdown Recommendation

Following the mandatory multi-phase PR workflow defined in `Document/AI_WORKFLOW.md`, future implementation should be divided into three discrete branches:

```text
[1. DB PR] ────────► [2. BE PR] ────────► [3. FE PR]
```

### Phase 1: Database Branch & PR (`feat/Phuc-org-context-db`)
- Verify compound index behavior on `role_assignments` for organization-wide roles (`projectId = null`).
- Provide an idempotent database migration/seed script creating the initial default organization (`Continuum AI Default Org`).

### Phase 2: Backend Branch & PR (`feat/Phuc-org-context-be-api`)
- Implement `OrgContextMiddleware` to resolve and attach `organizationId` to the request pipeline.
- Implement `@CurrentOrg()` and `@CurrentOrgId()` parameter decorators.
- Implement `OrgScopeGuard` (`CanActivate`) enforcing Cross-Organization Denial.
- Provide a Mongoose tenant query filter helper to prevent cross-tenant IDOR vulnerabilities.
- Add unit and E2E test suites for authorized tenant access and cross-tenant rejection.

### Phase 3: Frontend Branch & PR (`feat/Phuc-org-context-fe-ui`)
- Extend Zustand store (`src/stores/client-state.ts`) with `activeOrganizationId` and `setActiveOrganizationId`.
- Add `x-organization-id` to `forwardedHeaders` in `DATN-FE/src/lib/bff-proxy.ts`.
- Integrate organization context into `apiClient` request headers.
- Implement UI components for displaying and switching the active organization in the TailAdmin layout.
