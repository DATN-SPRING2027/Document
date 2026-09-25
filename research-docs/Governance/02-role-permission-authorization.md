# [RESEARCH] Governance - Role, Permission & Authorization Baseline

**Ticket**: `DATN-16`  
**Assignee**: Nguyen Hong Phuc  
**Reporter**: danh2492004  
**Due Date**: Sep 26, 2026  
**Status**: Research Only (No coding, no configuration/dependency changes, no PR for implementation)  
**Target System**: DATN / Continuum AI Baseline  

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
- `[DECISION REQUIRED]`: Architectural discrepancies, unapproved matrices, or open policy points requiring team/lead consensus (unapproved matrices must not be invented).

---

## 2. Executive Summary

1. `[FACT]` / `[PARTIAL]` **Data Model Scaffolding (Not Runtime Enforcement)**: The backend persistence layer (`DATN-BE`) contains Mongoose schema and index declarations for the 3 Persistent Human Roles (`ADMIN`, `TEAM_LEADER`, `MEMBER`), `role_assignments`, `organization_capability_grants` (currently limited to enum `'project.create'`), and specialized assignment collections (`sme_assignments`, `knowledge_owner_assignments`). However, this represents persistence-level scaffolding only: Mongoose `ObjectId` fields model references rather than database-enforced foreign keys, and runtime evaluation logic is entirely absent.
2. `[GAP]` **Zero Evaluator & Guard in Backend**: Across the entire `DATN-BE/src` codebase, there are currently **no** NestJS Guards (`CanActivate`), Interceptors, Evaluator Services, or Custom Decorators (`@Roles()`, `@RequireCapability()`). The sole controller in IAM (`iam.controller.ts`) exposes only a basic `/health` check.
3. `[GAP]` **Missing 401 vs. 403 Transport Handling**: While `401 Unauthorized` and `403 Forbidden` response schemas are drafted in the OpenAPI specification (`DATN-BE/docs/openapi/iam-v1.openapi.json`), no NestJS exception filters, guards, or middleware currently enforce this distinction.
4. `[GAP]` **Frontend UI Is Static Template Only**: In `DATN-FE`, the codebase is an unmodified bootstrap from the TailAdmin Next.js template. The Zustand store (`src/stores/client-state.ts`) only manages `activeProjectId`, with zero user identity, role, or capability state. No UX gating helpers (`can(...)`, `<Authorize />`) exist.
5. `[DESIGN]` **Core Access Control Rules Defined in Specifications**:
   - `ADMIN` does **not** automatically possess read or verification access to confidential project knowledge.
   - `TEAM_LEADER` leadership alone **never** implies the ability to create projects; `project.create` requires an explicit, audited grant in `organization_capability_grants` issued by an `ADMIN`.
   - **Deny Precedence**: Explicit Deny overrides all positive roles, assignments, or grants.
   - **Enforcement Boundary**: Backend guards serve as the authoritative security boundary; frontend checks are strictly UX-only.

---

## 3. Scope & Focus

### 3.1. In Scope:
- **3 Persistent Roles**: `ADMIN`, `TEAM_LEADER`, `MEMBER`, and the strict separation between roles and capabilities (Role vs. Capability boundaries).
- **Scope Hierarchy**: Organization Scope ➔ Project Scope ➔ Team Scope ➔ Domain / Resource ACL.
- **Project Creation Capability (`project.create`)**: ADMIN issuing authority, grant validity, revocation, and privilege escalation prevention.
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
| **Role vs. Capability Separation** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Sec. 2.1) | `[FACT]` / `[PARTIAL]` | Persistence separates `role_assignments` from `organization_capability_grants`. Only capability defined in backend enum is `'project.create'`. |
| **Scoped Roles (`organizationId`, `projectId`)** | `mongodb.schemas.ts:121-137` | `[FACT]` / `[PARTIAL]` | `role_assignments` declares `{ organizationId, projectId, userId, roleId }`. Note: Compound unique index behavior for organization-wide roles (`projectId = null`) requires database-level verification. |
| **Reference Modeling vs. Foreign Keys** | `DATN-BE/src/services/iam/...` | `[FACT]` | Collections use Mongoose `ObjectId` references (`ref: 'organizations'`). MongoDB does not enforce relational foreign keys; referential integrity is entirely an application-level responsibility. |
| **Specialized Scoped Assignments** | `mongodb.schemas.ts:153-195` | `[FACT]` / `[PARTIAL]` | Schemas exist for `sme_assignments`, `knowledge_owner_assignments`, and `successors`. These represent scoped, time-bounded functional assignments (`[DESIGN]`), not persistent roles. |
| **Explicit Capability Grant for Project Creation** | `02_ACTORS...md` (Sec. 2); `mongodb.schemas.ts:139-151` | `[FACT]` / `[DESIGN]` | `organization_capability_grants` schema defines `capability: 'project.create'`. Leadership alone does not confer creation capability. |
| **Backend Authorization Evaluator / Guard** | `DATN-BE/src` | `[GAP]` | Zero NestJS Guards (`CanActivate`), Interceptors, or Evaluators exist in the codebase. Sole IAM controller (`iam.controller.ts`) contains only `/health`. |
| **Deny Precedence Resolution** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Sec. 2.3) | `[DESIGN]` / `[GAP]` | Formally specified: $\text{Result} = \text{Deny} \succ \text{Explicit Grant} \succ \text{Role Default} \succ \text{Implicit Deny}$. Completely unimplemented in code. |
| **Transport Boundary: 401 vs. 403** | `iam-v1.openapi.json:115-135`; `05_SECURITY...md` | `[DESIGN]` / `[GAP]` | OpenAPI documents `401 Unauthorized` (auth failure) and `403 Forbidden` (permission failure). Zero NestJS exception filters or handlers implement this logic. |
| **Frontend UI Authorization State** | `DATN-FE/src/stores/client-state.ts` | `[GAP]` | Zustand store only contains `activeProjectId`. User identity, roles, and capability checks are absent. No UX gating component exists. |

---

## 5. Core Business Rules

### 5.1. Verified & Design Rules
1. **BR-GOV-01 (Role Boundary)**: `[DESIGN]` There are exactly three persistent human roles: `ADMIN`, `TEAM_LEADER`, and `MEMBER`.
2. **BR-GOV-02 (Separation of Duty - Admin Isolation)**: `[DESIGN]` An `ADMIN` manages organizational entities (users, teams, connectors) but possesses **no default read or verification access** to confidential project knowledge unless explicitly assigned a project role.
3. **BR-GOV-03 (Capability Explicitness)**: `[FACT]` / `[DESIGN]` A `TEAM_LEADER` role does **not** include project creation authority. Creating a project requires an active record in `organization_capability_grants` with `capability = 'project.create'`, granted by an `ADMIN`.
4. **BR-GOV-04 (Deny Precedence)**: `[DESIGN]` If any policy or active exclusion evaluates to `DENY`, access is immediately refused, overriding all positive roles, assignments, or capability grants.
5. **BR-GOV-05 (Authoritative Boundary)**: `[DESIGN]` Backend guards provide authoritative security enforcement. Frontend checks (`can(...)`, `<Authorize />`) are strictly UX optimizations and must never be relied upon for security boundaries.
6. **BR-GOV-06 (Audited Escalations)**: `[FACT]` / `[DESIGN]` Any grant or revocation in `organization_capability_grants` or `role_assignments` must emit an immutable audit event to `audit_logs`.

### 5.2. Open Rules & Discrepancies (`[UNKNOWN]` / `[DECISION REQUIRED]`)
- **BR-GOV-UN01**: Does an unauthenticated request to a protected endpoint yield `401 Unauthorized` with `WWW-Authenticate` header, or does it trigger an immediate redirect?
- **BR-GOV-UN02**: Does access denial across different tenant projects return `403 Forbidden` or `404 Not Found` to prevent project existence enumeration?
- **BR-GOV-UN03**: What is the formal grant lifecycle for capabilities (time-bound with automatic expiration vs. indefinite until manual revocation)?

---

## 6. Requirement ➔ Evidence ➔ Implementation ➔ Gap Matrix

| Architectural Layer | Requirement | Specification Evidence | Current Implementation | Technical Gap |
| :--- | :--- | :--- | :--- | :--- |
| **Database Schema** | 3 Persistent Roles | `02_ACTORS...md` (Sec. 1) | `roles` enum in `mongodb.schemas.ts` | `[PARTIAL]` Schema scaffolding exists; seed migration is missing. |
| **Database Schema** | Capability Grants | `02_ACTORS...md` (Sec. 2.1) | `organization_capability_grants` | `[PARTIAL]` Only `'project.create'` defined; grant lifecycle unbuilt. |
| **Database Index** | Scoped Role Assignments | `mongodb.schemas.ts:133-137` | Compound index `{ organizationId, projectId, userId }` | `[PARTIAL]` Index behavior for organization-level roles (`projectId = null`) requires database validation. |
| **API Contract** | 401 & 403 Response Definitions | `iam-v1.openapi.json` | Schemas declared in JSON | `[GAP]` No DTOs, NestJS response models, or exception filters exist in backend code. |
| **Backend Security** | Authorization Evaluator | `05_SECURITY...md` (Sec. 2) | None | `[GAP]` No `CapabilityEvaluatorService` or NestJS `CanActivate` guards exist. |
| **Backend Security** | Method Decorators | `02_ACTORS...md` | None | `[GAP]` Missing `@Roles(...)` and `@RequireCapability(...)` decorators. |
| **Frontend State** | Auth & Role State | `SPEC.md` | `DATN-FE/src/stores/client-state.ts` | `[GAP]` Zustand store only tracks `activeProjectId`; zero role or capability state. |
| **Frontend UX** | Conditional UI Gating | `SPEC.md` | TailAdmin unmodified template | `[GAP]` Missing `<Authorize />` component and `useAuthorization` hook. |

---

## 7. API, Data & Security Findings

### 7.1. Data & Schema Findings
- **Persistence Scaffolding vs. Enforcement**: Collections in `DATN-BE` declare `organizationId` and `projectId` as Mongoose `ObjectId` fields. However, MongoDB does not enforce foreign key referential integrity; missing records or dangling references must be guarded at the application layer.
- **Compound Unique Index on `role_assignments`**:
  ```typescript
  // Index definition in mongodb.schemas.ts
  { organizationId: 1, projectId: 1, userId: 1 }, { unique: true }
  ```
  In MongoDB, multiple documents with `projectId: null` for the same `(organizationId, userId)` will conflict unless sparse or partial filter expressions are configured. This index behavior must be verified in a dedicated database migration test.

### 7.2. API & Transport Findings
- **OpenAPI 401 vs. 403 Contracts**: The existing specification in `DATN-BE/docs/openapi/iam-v1.openapi.json` outlines:
  - `401 Unauthorized`: Returned when Bearer token is missing, expired, malformed, or revoked.
  - `403 Forbidden`: Returned when the authenticated caller lacks the required role, capability, or scope.
- **Current Runtime Status**: Because `iam.controller.ts` contains only an unprotected `/health` endpoint, neither 401 nor 403 status codes can currently be produced by the running application.

### 7.3. Security & Boundary Findings
- **Privilege Escalation Risk**: If `TEAM_LEADER` could create projects without an explicit `project.create` capability grant, arbitrary workspace creation could lead to resource exhaustion.
- **Frontend vs. Backend Boundary**: Any client-side authorization check (`canCreateProject`, `hasRole('ADMIN')`) must be treated as purely cosmetic UX gating. The backend must enforce capabilities at the controller/service entry point.

---

## 8. Frontend & Backend Mismatches & BFF Findings

1. **Client State Store (`DATN-FE/src/stores/client-state.ts`)**:
   - `[FACT]` Zustand store only manages `activeProjectId`.
   - `[GAP]` Store lacks `roles: string[]`, `capabilities: string[]`, and `user: CurrentUser | null`.
2. **Current User Contract (`DATN-FE/src/lib/queries/auth/useAuth.ts`)**:
   - `[FACT]` `CurrentUserResponse` returns `roles: readonly string[]`.
   - `[GAP]` Does not include `capabilities: string[]`. As a result, frontend cannot check `project.create` without an additional API call or enriched `/users/me` contract.
3. **BFF Proxy Boundary (`DATN-FE/src/lib/bff-proxy.ts`)**:
   - `[FACT]` BFF passes through `authorization` header.
   - `[GAP]` BFF does not inspect or validate token roles; it functions as a pass-through proxy. All enforcement remains with the backend.

---

## 9. Dependencies for Project & Team Authorization

The access control hierarchy operates strictly top-down:

$$\text{Organization Boundary} \longrightarrow \text{Project Boundary} \longrightarrow \text{Team Boundary} \longrightarrow \text{Resource ACL}$$

1. **Organization Prerequisite**: A caller must have an active association within the target organization before any project-level access can be evaluated.
2. **Project Creation Dependency**: Project creation requires:
   $$\text{Caller Role} \in \{\text{ADMIN}\} \quad \lor \quad (\text{Caller Role} = \text{TEAM_LEADER} \land \text{Valid Grant in } \texttt{organization\_capability\_grants})$$
3. **Team Membership Invariant**: A user cannot be added to a team within a project unless they already hold project membership.

---

## 10. UNKNOWN / DECISION REQUIRED

> [!IMPORTANT]
> The architectural items below remain open for team lead decision. The recommendations provided are **exploratory and non-binding**.

| Decision ID | Open Question | Viable Options | Non-Binding Recommendation |
| :--- | :--- | :--- | :--- |
| **DEC-AUTH-01** | **Permission Matrix Approval** | A. Coarse-grained role-based checks (`ADMIN`, `TEAM_LEADER`, `MEMBER`)<br>B. Fine-grained permission strings (`project:write`, `knowledge:verify`) | **Option A for MVP (Non-binding)**: Rely on 3 roles + explicit capabilities (`project.create`) for MVP velocity, transitioning to fine-grained ACLs later. |
| **DEC-AUTH-02** | **Capability Grant Expiration** | A. Indefinite until manual revocation<br>B. Time-bounded with mandatory `expiresAt` | **Option B (Non-binding)**: Include optional `expiresAt` with default 90-day renewal requirement for high-privilege grants. |
| **DEC-AUTH-03** | **Access Denied Response for Cross-Project Probes** | A. Always return `403 Forbidden`<br>B. Return `404 Not Found` for nonexistent or unauthorized projects | **Option B (Non-binding)**: Return `404 Not Found` to prevent attackers from discovering private project identifiers through status code probing. |

---

## 11. Implementation-Breakdown Recommendation

Following the project's standard 3-phase workflow:

```text
[1. DB PR] ────────► [2. BE PR] ────────► [3. FE PR]
```

### Phase 1: Database PR (`feat/Phuc-auth-baseline-db`)
- Create idempotent seed migration for system roles (`ADMIN`, `TEAM_LEADER`, `MEMBER`).
- Add database migration test verifying unique compound index behavior on `role_assignments` when `projectId: null`.

### Phase 2: Backend PR (`feat/Phuc-auth-baseline-be-guard`)
- Implement `JwtAuthGuard` enforcing `401 Unauthorized` for invalid or missing tokens.
- Implement `CapabilityGuard` and `@RequireCapability('project.create')` enforcing `403 Forbidden`.
- Implement `CapabilityEvaluatorService` applying Deny Precedence logic.
- Add comprehensive unit and integration test coverage for 401/403 boundaries.

### Phase 3: Frontend PR (`feat/Phuc-auth-baseline-fe-ui`)
- Enrich `CurrentUserResponse` in `DATN-FE` with capabilities array.
- Extend Zustand client store to cache user roles and capabilities.
- Implement `<Authorize />` component and `useAuthorization` hook for UX gating.
- Handle 401 (redirect to `/signin`) and 403 (render Access Denied banner without session logout) in `api-client.ts`.
