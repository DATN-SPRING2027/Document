# [RESEARCH] Governance - Role, Permission & Authorization Baseline

> This is an evidence and gap report, not approval of the detailed permission matrix. Use [Actors, roles and permissions](../02_ACTORS_ROLES_AND_PERMISSIONS.md) for accepted role vocabulary and [Organization and Workspace Access Contract Readiness](../Workspace/00-organization-and-access-contract-readiness.md) for cross-document open decisions.

**Ticket**: `DATN-16`  
**Assignee**: Nguyen Hong Phuc  
**Reporter**: danh2492004  
**Due Date**: Sep 26, 2026  
**Status**: Research Only (No coding, no configuration/dependency changes, no PR for implementation)  
**Target System**: DATN / Continuum AI Baseline  

> **Decision update — 2026-10-02:** This report's code inventory is a dated snapshot. Current policy separates `PLATFORM_OPERATOR` (platform operations; no default Organization-content access) from Organization roles. `ADMIN` manages Organization Users/membership/roles/scopes but has no default confidential-content access. `TEAM_LEADER` manages only explicitly assigned Project/Team scope; `MEMBER` remains bounded by active membership and ACL. BE DEC-016 makes `OrganizationMembership` the authoritative User–Organization relationship and requires `ACTIVE` for Organization Context. Project Foundation allows any authenticated User with active Organization Membership in the trusted Organization to create a `PRIVATE` Project, atomically bootstrap creator Project Membership + scoped `MEMBER` assignment and audit; `project.create` is not required. The grant schema may remain, but this use is superseded. Historical grant-gate text below is not current policy; verify implementation separately.

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
5. `[APPROVED POLICY]` **Current Governance Rules**:
   - `PLATFORM_OPERATOR` operates the platform and provisions Organizations/first Admin; platform role gives no default Organization-content access.
   - `ADMIN` manages Organization membership and roles/scopes but has no default confidential-content access.
   - `TEAM_LEADER` manages only explicitly assigned Project/Team scope; `MEMBER` access requires active membership and ACL.
   - `OrganizationMembership` is the authoritative Organization association; only `ACTIVE` establishes context.
   - Any authenticated User with active Organization Membership may create a `PRIVATE` Project in matching trusted context; no `project.create` grant is required.
   - **Deny Precedence**: Explicit Deny overrides all positive roles, assignments, or grants. Backend authorization remains authoritative; frontend checks are UX-only.

---

## 3. Scope & Focus

### 3.1. In Scope:
- **3 Persistent Roles**: `ADMIN`, `TEAM_LEADER`, `MEMBER`, and the strict separation between roles and capabilities (Role vs. Capability boundaries).
- **Scope Hierarchy**: Organization Scope ➔ Project Scope ➔ Team Scope ➔ Domain / Resource ACL.
- **Project Creation Authorization**: Active Organization Membership and trusted context are required; `project.create` is not a gate. Any remaining capability-grant lifecycle is separate and unresolved.
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
| **Legacy Project-create grant schema** | `mongodb.schemas.ts:139-151`; BE Project Foundation decision | `[FACT]` / `[SUPERSEDED POLICY]` | Schema defines `capability: 'project.create'`, but this grant is not required for Project creation. Other grant policies are not changed. |
| **Backend Authorization Evaluator / Guard** | `DATN-BE/src` | `[GAP]` | Zero NestJS Guards (`CanActivate`), Interceptors, or Evaluators exist in the codebase. Sole IAM controller (`iam.controller.ts`) contains only `/health`. |
| **Deny Precedence Resolution** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Sec. 2.3) | `[DESIGN]` / `[GAP]` | Formally specified: $\text{Result} = \text{Deny} \succ \text{Explicit Grant} \succ \text{Role Default} \succ \text{Implicit Deny}$. Completely unimplemented in code. |
| **Transport Boundary: 401 vs. 403** | `iam-v1.openapi.json:115-135`; `05_SECURITY...md` | `[DESIGN]` / `[GAP]` | OpenAPI documents `401 Unauthorized` (auth failure) and `403 Forbidden` (permission failure). Zero NestJS exception filters or handlers implement this logic. |
| **Frontend UI Authorization State** | `DATN-FE/src/stores/client-state.ts` | `[GAP]` | Zustand store only contains `activeProjectId`. User identity, roles, and capability checks are absent. No UX gating component exists. |

---

## 5. Core Business Rules

### 5.1. Verified & Design Rules
1. **BR-GOV-01 (Role Boundary)**: `[APPROVED POLICY]` Persistent Organization/Project roles are `ADMIN`, `TEAM_LEADER`, and `MEMBER`; `PLATFORM_OPERATOR` is a separate platform-scoped actor, not a fourth Organization role.
2. **BR-GOV-02 (Admin and Operator Isolation)**: `[APPROVED POLICY]` Platform operations do not grant default Organization-content access. An `ADMIN` manages Organization Users/membership/roles/scopes but has no default read or verification access to confidential Project content.
3. **BR-GOV-03 (Organization Membership Context)**: `[APPROVED BE DECISION: DEC-016]` `OrganizationMembership` is the authoritative User–Organization relationship; only `ACTIVE` establishes Organization Context. A RoleAssignment alone is insufficient.
4. **BR-GOV-04 (Project Creation)**: `[APPROVED BE DECISION: Project Foundation]` Any authenticated User with `ACTIVE` Organization Membership in the trusted matching Organization may create a `PRIVATE` Project. Creator bootstrap adds active Project Membership and project-scoped `MEMBER` assignment with audit; no role or `project.create` grant is required.
5. **BR-GOV-05 (Explicit Scope)**: `[APPROVED POLICY]` `TEAM_LEADER` manages only explicitly assigned Project/Team scope and cannot self-grant broader scope. `MEMBER` access remains bounded by membership, scope, and resource ACL.
6. **BR-GOV-06 (Deny Precedence)**: `[DESIGN]` If any applicable policy evaluates to `DENY`, access is refused, overriding positive roles, assignments, or grants.
7. **BR-GOV-07 (Authoritative Boundary and Audit)**: `[DESIGN]` Backend authorization is authoritative; frontend checks are UX only. Membership, role/scope and Project mutations require audit; exact event payloads remain a contract gap.

### 5.2. Open Rules & Discrepancies (`[UNKNOWN]` / `[DECISION REQUIRED]`)
- **BR-GOV-UN01**: Does an unauthenticated request to a protected endpoint yield `401 Unauthorized` with `WWW-Authenticate` header, or does it trigger an immediate redirect?
- **BR-GOV-UN02**: Does access denial across different tenant projects return `403 Forbidden` or `404 Not Found` to prevent project existence enumeration?
- **BR-GOV-UN03**: What is the formal grant lifecycle for capabilities (time-bound with automatic expiration vs. indefinite until manual revocation)?

---

## 6. Requirement ➔ Evidence ➔ Implementation ➔ Gap Matrix

| Architectural Layer | Requirement | Specification Evidence | Current Implementation | Technical Gap |
| :--- | :--- | :--- | :--- | :--- |
| **Database Schema** | 3 Persistent Roles | `02_ACTORS...md` (Sec. 1) | `roles` enum in `mongodb.schemas.ts` | `[PARTIAL]` Schema scaffolding exists; seed migration is missing. |
| **Database Schema** | Organization Membership | BE DEC-016 | Existing inventory/source snapshot | `[IMPLEMENTATION GAP]` Verify authoritative membership schema/API, unique pair, status vocabulary and backfill. |
| **Database Schema** | Legacy Capability Grants | `organization_capability_grants` | `[PARTIAL]` `'project.create'` exists as schema value but is not the current Project-create gate; remaining grant policy is open. |
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
- **Project Boundary Risk**: The approved rule permits every authenticated active Organization member to create Projects. Backend must enforce active subject, trusted matching context, Organization Membership, valid input, per-Organization code uniqueness, atomic creator bootstrap and audit. Do not substitute a role or `project.create` gate.
- **Frontend vs. Backend Boundary**: Any client-side membership or role check is cosmetic UX gating. The backend must enforce identity, membership, scope and ACL at the service boundary.

---

## 8. Frontend & Backend Mismatches & BFF Findings

1. **Client State Store (`DATN-FE/src/stores/client-state.ts`)**:
   - `[FACT]` Zustand store only manages `activeProjectId`.
   - `[GAP]` Store lacks `roles: string[]`, `capabilities: string[]`, and `user: CurrentUser | null`.
2. **Current User Contract (`DATN-FE/src/lib/queries/auth/useAuth.ts`)**:
   - `[FACT]` `CurrentUserResponse` returns `roles: readonly string[]`.
   - `[GAP]` The `/users/me` and Organization-context contracts do not yet expose the accepted membership/context state needed for UX. A `project.create` capability is not needed to display Project creation to an active Organization member; backend enforcement remains authoritative.
3. **BFF Proxy Boundary (`DATN-FE/src/lib/bff-proxy.ts`)**:
   - `[FACT]` BFF passes through `authorization` header.
   - `[GAP]` BFF does not inspect or validate token roles; it functions as a pass-through proxy. All enforcement remains with the backend.

---

## 9. Dependencies for Project & Team Authorization

The access control hierarchy operates strictly top-down:

$$\text{Organization Boundary} \longrightarrow \text{Project Boundary} \longrightarrow \text{Team Boundary} \longrightarrow \text{Resource ACL}$$

1. **Organization Prerequisite**: A caller must have `ACTIVE` `OrganizationMembership` in the trusted target Organization before scoped authorization is evaluated.
2. **Project Creation Dependency**: Require authenticated active subject + matching trusted Organization Context + active Organization Membership. Any such member may create; no role or `project.create` grant is required.
3. **Creator Bootstrap**: Create the `PRIVATE` Project, active creator Project Membership, project-scoped `MEMBER` RoleAssignment, and audit record atomically.
4. **Team Membership Invariant**: A user cannot be added to a Team unless they already hold eligible Project Membership and the actor has the explicit scope needed for that action.

---

## 10. UNKNOWN / DECISION REQUIRED

> [!IMPORTANT]
> The architectural items below remain open for team lead decision. The recommendations provided are **exploratory and non-binding**.

| Decision ID | Open Question | Viable Options | Non-Binding Recommendation |
| :--- | :--- | :--- | :--- |
| **DEC-AUTH-01** | **Detailed Permission Matrix** | A. Coarse-grained role defaults with scoped assignments<br>B. Fine-grained permission strings with explicit delegation | **Open** for actions other than accepted Organization Membership-based Project creation and the high-level role boundaries. Do not restore `project.create` as a creation gate. |
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
- Implement Organization-context/membership and scoped authorization guards. Project creation must require active Organization Membership and trusted matching context; do not add `@RequireCapability('project.create')` to that route.
- Implement the authorization evaluator applying Deny Precedence and explicit Team Leader scope.
- Add comprehensive unit and integration test coverage for 401/403 boundaries.

### Phase 3: Frontend PR (`feat/Phuc-auth-baseline-fe-ui`)
- Enrich the User/Organization context contract with active Organization Membership and approved scope data for UX.
- Extend Zustand client state to represent authenticated identity and selected Organization/Project context without treating client state as authority.
- Implement `<Authorize />` component and `useAuthorization` hook for UX gating.
- Handle 401 (redirect to `/signin`) and 403 (render Access Denied banner without session logout) in `api-client.ts`.
