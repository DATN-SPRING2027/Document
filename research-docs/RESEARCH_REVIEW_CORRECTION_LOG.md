# Research Review Correction Log

> Mục đích: ghi lại các finding, evidence và correction cần thực hiện sau khi review các research task/PR của DATN/Continuum AI.
>
> Quy tắc sử dụng:
> - Chỉ ghi nhận yêu cầu correction; không tự động sửa source, research file, architecture, ADR, SPEC hoặc Jira.
> - Mỗi correction phải có evidence cụ thể và trạng thái rõ ràng.
> - Các mục `UNKNOWN` hoặc `DECISION REQUIRED` không được tự ý chốt trong log.
> - Các review research mới sẽ được append ở cuối file này.

## Repository mapping

- Git repository `Document` tương ứng với thư mục local `product_docs` trong project DATN.
- PR path `Document/research-docs/<file>.md` tương ứng với local path `product_docs/research-docs/<file>.md`.
- Khi review PR của `Document`, cần đối chiếu với `product_docs` hiện tại và ghi rõ mapping này trong evidence nếu cần.

---

## Review 001 — DATN-15 / PR #5

- **Date:** 2026-09-24
- **Jira:** DATN-15 — `[RESEARCH] Governance - Organization Context`
- **PR:** https://github.com/DATN-SPRING2027/Document/pull/5
- **Review verdict:** `REQUEST_CHANGES`
- **Review scope:** Research-only review; no source/config/dependency/architecture changes.
- **Current status:** `PENDING MANUAL CORRECTION`

### Overall assessment

The PR covers the requested research scope: organization boundary, context resolution, cross-organization denial, Project/Team authorization dependencies, FE/BFF mismatch, security gaps, unknowns, decision points, and a future implementation breakdown.

The research is not ready to be accepted as the baseline because some source claims are inaccurate or overstate runtime implementation. The corrections below must be applied to the PR research file by the owner before acceptance.

### Required corrections

#### Correction 1 — Do not describe schema/index scaffolding as runtime tenant enforcement

- **Target file:** `Document/research-docs/Governance/01-organization-context.md`
- **Target lines:** `27`, `104-109`
- **Current issue:** The report states that the backend “enforces” a strict multi-tenant boundary and that 100% of domain services enforce `organizationId` across all business entities.
- **Required correction:** Reword this as schema/index scaffolding or organization-scoped data modeling. Explicitly separate:
  - `organizationId` fields and indexes in schemas;
  - application/business query filters;
  - NestJS authorization guards and runtime cross-tenant denial;
  - E2E verification.
- **Evidence:**
  - `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:25-64` — `users`, `organizations`, and `roles` are not organization-scoped; IAM `auditSchema.organizationId` is optional.
  - `docs/architecture/gaps.md:111-117` — authorization guards, pre-retrieval ACL filters, and deny-precedence logic are marked absent from executable code.
- **Reason:** A required schema field or index does not prove runtime tenant isolation.

#### Correction 2 — Correct the `users` schema inventory

- **Target file:** `Document/research-docs/Governance/01-organization-context.md`
- **Target line:** `56`
- **Current issue:** The report says the `users` schema only defines `email`, `passwordHash`, `status`, and `twoFactorEnabled`.
- **Required correction:** Include the fields evidenced by source: required `fullName`, optional `avatarUrl`, `twoFactorSecretEncrypted`, and `lastLoginAt`. Keep the conclusion that `users` does not contain a hardcoded `organizationId`.
- **Evidence:** `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:40-55`.
- **Reason:** The current statement is an incomplete source inventory.

#### Correction 3 — Use the actual ingestion collection name

- **Target file:** `Document/research-docs/Governance/01-organization-context.md`
- **Target line:** `58`
- **Current issue:** The resource inventory names `raw_documents` as an existing resource.
- **Required correction:** Replace `raw_documents` with the source-backed collection name `documents`; optionally mention `document_versions` separately. Do not claim a `raw_documents` collection unless new evidence is found.
- **Evidence:**
  - `DATN-BE/src/services/ingestion/infrastructure/mongodb/mongodb.schemas.ts:39-58` — collection schema key is `documents`.
  - `DATN-BE/src/services/ingestion/infrastructure/persistence.ts:9-18` — persistence definition names `documents`.
- **Reason:** The current resource name is not present in the inspected source.

#### Correction 4 — Preserve the test limitation precisely

- **Target file:** `Document/research-docs/Governance/01-organization-context.md`
- **Target area:** Requirement/evidence/gap matrix, especially line `97`
- **Current state:** The PR is documentation-only, changes one Markdown file (`+206/-0`), and GitHub reports `Checks 0`.
- **Required correction:** Keep cross-tenant E2E as an unimplemented test gap. Do not present the research findings as runtime security validation. No source test implementation is required for this research-only PR.
- **Reason:** Static source inspection and a documentation PR do not validate actual cross-tenant behavior.

#### Correction 5 — Keep recommendations non-binding

- **Target file:** `Document/research-docs/Governance/01-organization-context.md`
- **Target lines:** `177-179`
- **Current state:** DEC-01, DEC-02, and DEC-03 are listed as decision points with recommended options.
- **Required correction:** Keep the recommendations explicitly marked as non-binding. Do not represent them as accepted architecture or implementation requirements until the lead/architecture authority decides.
- **Reason:** Research may identify decision points but must not resolve them implicitly.

### Acceptance status after correction

- **Research scope coverage:** `PASS`
- **Requirement coverage:** `PASS`
- **Source evidence accuracy:** `PARTIAL` until Corrections 1-3 are applied.
- **Security/runtime conclusion:** `PARTIAL`; schema evidence must remain separate from executable enforcement.
- **Test evidence:** `PARTIAL`; no automated checks exist for this documentation-only PR.
- **Architecture alignment:** `PARTIAL` until accepted specifications and non-binding recommendations are clearly distinguished.
- **Ready to accept DATN-15:** `NO — pending manual correction and re-review.`

### Files that require manual correction

| File | Lines/area | Action | Status |
|---|---:|---|---|
| `Document/research-docs/Governance/01-organization-context.md` | `27`, `104-109` | Correct runtime tenant-enforcement overclaim | `PENDING` |
| `Document/research-docs/Governance/01-organization-context.md` | `56` | Correct incomplete `users` schema inventory | `PENDING` |
| `Document/research-docs/Governance/01-organization-context.md` | `58` | Replace `raw_documents` with `documents` | `PENDING` |
| `Document/research-docs/Governance/01-organization-context.md` | `97` and test/gap section | Preserve static-analysis/test limitation | `PENDING` |
| `Document/research-docs/Governance/01-organization-context.md` | `177-179` | Keep DEC-01/02/03 explicitly non-binding | `PENDING` |

### Review safety record

- Source code changed by this review: `NO`
- Configuration/dependencies changed: `NO`
- Architecture/ADR/SPEC changed: `NO`
- PR merged or approved: `NO`
- Jira comment posted: `YES` — review verdict `REQUEST_CHANGES`
- Corrections applied to the PR research file: `NO` — owner must apply manually

---

## Review 002 — DATN-16 / PR #6

- **Date:** 2026-09-25
- **Jira:** DATN-16 — `[RESEARCH] Governance - Role, Permission & Authorization`
- **PR:** https://github.com/DATN-SPRING2027/Document/pull/6
- **Review verdict:** `REQUEST_CHANGES`
- **Review scope:** Research-only review; no source/config/dependency/architecture changes.
- **Current status:** `PENDING MANUAL CORRECTION`

### Overall assessment

The PR covers the DATN-16 research scope and correctly identifies the main runtime gaps: no backend guards/evaluator, no executable deny precedence, missing 401/403 enforcement, missing FE capability gating, and open decision items. The PR also stays within the research-only boundary: one Markdown file, no implementation code, and no implementation tests.

The baseline is not ready for acceptance because several statements are stronger than the evidence supports or need to be aligned with the accepted BFF/HttpOnly boundary.

### Required corrections

#### Correction 1 — Do not describe MongoDB references as foreign-key enforcement

- **Target file:** `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md`
- **Target line:** `64`
- **Current issue:** The checklist says `projects`, `teams`, `project_memberships`, and `team_memberships` schemas “enforce foreign key references” and thereby reflect strict hierarchy.
- **Required correction:** Reword this as schema/reference-field scaffolding. The source shows required `ObjectId` fields and indexes, but no relational foreign-key constraints or executable organization/project/team containment validation. Keep runtime enforcement as `PARTIAL`/`GAP`.
- **Evidence:** `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:66-105`; `docs/architecture/gaps.md:111-117`.
- **Reason:** MongoDB/Mongoose reference fields do not by themselves enforce foreign keys or business authorization boundaries.

#### Correction 2 — Do not present the role-assignment uniqueness conclusion as verified

- **Target file:** `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md`
- **Target lines:** `126`, `143`
- **Current issue:** Line 126 correctly says null handling requires verification, but line 143 then states that MongoDB’s null indexing “correctly restricts” a user to one organization-level assignment. No database execution or test evidence is present, and `projectId` is optional in the schema.
- **Required correction:** State only the declared compound unique index as verified. Classify the null/omitted-value behavior and the one-assignment conclusion as `UNKNOWN`/pending DB verification until the storage convention and index behavior are tested.
- **Evidence:** `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:120-134`; `DATN-BE/src/services/iam/infrastructure/persistence.ts:40-44`.
- **Reason:** An index declaration is not evidence that the intended organization-level uniqueness behavior has been exercised with the actual stored values.

#### Correction 3 — Do not overstate the approved capability scope

- **Target file:** `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md`
- **Target line:** `146`
- **Current issue:** The report states as approved MVP scope that only `project.create` is separately grantable to non-admins and that all other standard permissions flow from persistent roles and team memberships.
- **Required correction:** Keep the source-backed fact that the current schema enum contains only `project.create`. Reclassify the broader “all other permissions” statement as an inference or decision-required item. The accepted baseline also describes project-policy grants, scoped assignments, ACLs, and a permission matrix whose detailed mapping remains open.
- **Evidence:** `product_docs/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md:62-84`; `docs/decisions/decision-register.md:47-68`; `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:135-150`.
- **Reason:** Current persistence shape does not prove that the complete organization/project/team permission model has been approved or that all other permissions are role/team-membership-only.

#### Correction 4 — Align 401 client behavior with the HttpOnly BFF boundary

- **Target file:** `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md`
- **Target line:** `105`
- **Current issue:** “Clear stale session tokens” is ambiguous and can be read as direct browser token management, while the accepted architecture prohibits raw browser token storage and assigns cookie lifecycle to the BFF/backend.
- **Required correction:** Clarify that FE reacts to a 401 by requesting silent rotation/logout as applicable and redirecting to `/signin`; the BFF/backend owns HttpOnly cookie/token lifecycle. Do not imply that client JavaScript reads or clears raw access/refresh tokens.
- **Evidence:** `docs/specs/SPEC-002-AUTHENTICATION-TOKEN-MODEL.md:28-43`; `DATN-FE/src/lib/api-client.ts:30-46`.
- **Reason:** The research contract must preserve the accepted browser authentication boundary.

#### Correction 5 — Distinguish current BFF behavior from a future tenant-header dependency

- **Target file:** `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md`
- **Target line:** `173`
- **Current issue:** The FE/BE mismatch table presents custom tenant headers as required by the current backend, although the current backend has no executable context/authorization guard and the accepted BFF contract currently documents cookie, authorization, and request-ID forwarding.
- **Required correction:** Label custom tenant-header forwarding as a target-state dependency or unresolved context-resolution decision, not as current runtime backend enforcement. Keep the observed whitelist behavior as a source fact.
- **Evidence:** `DATN-FE/src/lib/bff-proxy.ts:5-11`; `docs/specs/SPEC-004-BFF-ROUTING-ARCHITECTURE.md:29-43`; `docs/architecture/gaps.md:111-117`.
- **Reason:** Current header filtering is verified, but a current backend requirement for a custom tenant header is not evidenced.

#### Correction 6 — Correct the FE “unmodified bootstrap” wording

- **Target file:** `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md`
- **Target line:** `30`
- **Current issue:** The report calls the entire FE codebase an “unmodified bootstrap from the TailAdmin Next.js template.” Existing source includes BFF routing, API client, React Query auth/capture/verification hooks, and tests.
- **Required correction:** Narrow the statement to the current UI/domain-surface state: no role/capability store or UX authorization helpers are implemented. Do not imply that the whole FE codebase is unmodified or contains no implemented integration code.
- **Evidence:** `DATN-FE/src/lib/api-client.ts:1-47`; `DATN-FE/src/lib/bff-proxy.ts:1-38`; `docs/architecture/current-state.md:100-151`.
- **Reason:** The gap conclusion is valid, but the source inventory must remain accurate.

### Acceptance status after correction

- **Research scope coverage:** `PASS`
- **Requirement coverage:** `PASS`
- **Source evidence accuracy:** `PARTIAL` until Corrections 1-3 and 6 are applied.
- **Security/runtime conclusion:** `PARTIAL` until the HttpOnly and current-vs-target enforcement wording is corrected.
- **Test evidence:** `PARTIAL`; PR #6 contains no test changes, and the current backend E2E suite only covers `/api/v1/health`. The report should retain authorization/401/403/deny testing as an unimplemented gap.
- **Architecture alignment:** `PARTIAL` until Corrections 4-5 are applied and open decisions remain non-binding.
- **Ready to accept DATN-16:** `NO — pending manual correction and re-review.`

### Files that require manual correction

| File | Lines/area | Action | Status |
|---|---:|---|---|
| `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md` | `30` | Narrow the FE bootstrap claim to the actual UI/domain gap | `PENDING` |
| `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md` | `64` | Replace foreign-key enforcement wording with schema/reference scaffolding | `PENDING` |
| `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md` | `105` | Align 401 client behavior with HttpOnly/BFF ownership | `PENDING` |
| `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md` | `126`, `143` | Keep unique-index declaration separate from unverified null behavior | `PENDING` |
| `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md` | `146` | Reclassify broader capability-scope statement as inference/decision required | `PENDING` |
| `Document/research-docs/Roles-Capabilities-Evaluator/01-roles-capabilities-evaluator-baseline.md` | `173` | Mark custom tenant-header requirement as target-state/unknown | `PENDING` |

### Review safety record

- Source code changed by this review: `NO`
- Configuration/dependencies changed: `NO`
- Architecture/ADR/SPEC changed: `NO`
- PR merged or approved: `NO`
- Jira comment posted: `NO` — prepared, awaiting user confirmation immediately before posting.
- Corrections applied to the PR research file: `NO` — owner must apply manually.

---

## Review 003 — DATN-13 / PR #7

- **Date:** 2026-09-25
- **Jira:** DATN-13 — `[RESEARCH] Identity - Authentication & Token Contract`
- **PR:** https://github.com/DATN-SPRING2027/Document/pull/7
- **Review verdict:** `REQUEST_CHANGES`
- **Review scope:** Research-only review; no source/config/dependency/architecture changes.
- **Current status:** `PENDING MANUAL CORRECTION`

### Overall assessment

The PR correctly identifies the major authentication runtime gaps: missing login/refresh/me implementation, the FE/BE token-delivery conflict, and unimplemented brute-force/session-rotation behavior. It remains within the research-only scope. The baseline is not ready for acceptance because one schema claim is inaccurate, accepted SPEC-002 decisions are treated as unresolved, and several concrete FE/BE contract mismatches are omitted.

### Required corrections

#### Correction 1 — Do not report `familyId` as implemented in the refresh-session schema

- **Target file:** `Document/research-docs/Auth/01-auth-baseline-research.md`
- **Target line:** `46`
- **Current issue:** The report says the current `refresh_sessions` schema includes `familyId`, but the current Mongoose schema contains `userId`, `organizationId`, `tokenHash`, `ipAddress`, `userAgent`, `isRevoked`, and `expiresAt`; `familyId`, `revokedAt`, and `revokedReason` are not present there.
- **Required correction:** Separate target/documented session-family fields from the fields actually implemented in code. Keep rotation/reuse detection as an implementation gap.
- **Evidence:** `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:151-161`; `docs/specs/SPEC-001-MONGODB-PERSISTENCE.md:139-147`.
- **Reason:** A target schema or architecture diagram is not evidence that the runtime schema already supports family reuse detection.

#### Correction 2 — Treat `/api/v1/auth/me` as the accepted contract, not an open endpoint decision

- **Target file:** `Document/research-docs/Auth/01-auth-baseline-research.md`
- **Target lines:** `59-60`, `64`
- **Current issue:** The document presents `/api/v1/auth/me` versus `/api/v1/iam/users/me` as an unresolved endpoint-design decision. SPEC-002 already specifies `GET /api/v1/auth/me` for session verification.
- **Required correction:** Record the accepted SPEC-002 endpoint and identify the current FE `/users/me` call as the implementation/path mismatch. Keep any deviation from SPEC-002 as a human decision only if the authority explicitly reopens the accepted contract.
- **Evidence:** `docs/specs/SPEC-002-AUTHENTICATION-TOKEN-MODEL.md:119-121`; `DATN-FE/src/lib/queries/auth/useAuth.ts:32-39`.
- **Reason:** The research must not reopen an accepted contract as UNKNOWN without evidence of an approved change.

#### Correction 3 — Add refresh/logout request transport mismatches

- **Target file:** `Document/research-docs/Auth/01-auth-baseline-research.md`
- **Target lines:** `36-38`, `49`, `58-60`
- **Current issue:** The report identifies the login response token mismatch but omits that the OpenAPI contract requires `refreshToken` in JSON bodies for refresh and logout, while SPEC-002 defines refresh through the `continuum_refresh` cookie and logout through cookies or Bearer authentication.
- **Required correction:** Add these as explicit FE/BE/spec contract mismatches and do not reduce the issue to login response delivery only.
- **Evidence:** `DATN-BE/docs/openapi/iam-v1.openapi.json:51-99`; `docs/specs/SPEC-002-AUTHENTICATION-TOKEN-MODEL.md:102-117`.
- **Reason:** Refresh and logout transport determine whether the HttpOnly boundary is preserved end to end.

#### Correction 4 — Add the authentication response-shape mismatch

- **Target file:** `Document/research-docs/Auth/01-auth-baseline-research.md`
- **Target lines:** `36`, `45`, `49`
- **Current issue:** The document reports JSON-versus-cookie delivery but does not record that BE OpenAPI `AuthSession` is `{ tokens: { accessToken, refreshToken, tokenType, expiresIn }, user }`, while FE `AuthSession` is a flat `{ accessToken, tokenType, expiresInSeconds }` shape.
- **Required correction:** Add the response schema/type mismatch and distinguish it from the separate token transport mismatch.
- **Evidence:** `DATN-BE/docs/openapi/iam-v1.openapi.json:829-851`; `DATN-FE/src/lib/queries/auth/useAuth.ts:18-22`; `DATN-FE/src/lib/queries/auth/useAuth.spec.tsx:53-77`.
- **Reason:** Matching the transport alone would not make the current FE and BE response contracts interoperable.

#### Correction 5 — Reconcile the HttpOnly policy claim with current FE code

- **Target file:** `Document/research-docs/Auth/01-auth-baseline-research.md`
- **Target lines:** `27`, `49`
- **Current issue:** The report states that FE strictly prohibits tokens in browser memory, but current `useAuth.ts` exposes a raw `accessToken` in client-facing state and its test asserts that shape. The policy/documentation requirement and current implementation are in conflict.
- **Required correction:** Classify the HttpOnly rule as the accepted architecture/spec constraint, and separately report the raw-token FE model as an existing implementation conflict. Avoid wording that implies the current FE already enforces the rule.
- **Evidence:** `DATN-FE/README.md:40-43`; `DATN-FE/src/lib/queries/auth/useAuth.ts:18-22`; `DATN-FE/src/lib/queries/auth/useAuth.spec.tsx:53-58`; `docs/decisions/decision-register.md:367-375`.
- **Reason:** Security review must distinguish policy compliance from the behavior currently represented by the source and tests.

#### Correction 6 — Record the 204 logout handling gap

- **Target file:** `Document/research-docs/Auth/01-auth-baseline-research.md`
- **Target lines:** `35-38`, `66`
- **Current issue:** The OpenAPI logout operation returns `204`, while the shared FE API client always calls `response.json()` on successful responses. The current logout hook therefore has a concrete empty-body handling gap that is not recorded.
- **Required correction:** Add this as a current FE contract/runtime gap and retain it for implementation acceptance criteria.
- **Evidence:** `DATN-BE/docs/openapi/iam-v1.openapi.json:81-99`; `DATN-FE/src/lib/api-client.ts:30-46`; `DATN-FE/src/lib/queries/auth/useAuth.ts:61-77`.
- **Reason:** A successful logout response can still surface as a client error if the 204 body is parsed as JSON.

### Acceptance status after correction

- **Research scope coverage:** `PASS`
- **Requirement coverage:** `PASS`
- **Source evidence accuracy:** `PARTIAL` until Correction 1 and Correction 5 are applied.
- **Security/runtime conclusion:** `PARTIAL` until the accepted HttpOnly contract and all refresh/logout transport gaps are recorded.
- **Test evidence:** `PARTIAL`; the PR contains no test changes, and existing FE auth tests encode the stale path/raw-token response shape rather than validating the accepted cookie contract.
- **Architecture alignment:** `PARTIAL` until accepted SPEC-002 endpoint/token decisions are treated as fixed baseline constraints.
- **Ready to accept DATN-13:** `NO — pending manual correction and re-review.`

### Files that require manual correction

| File | Lines/area | Action | Status |
|---|---:|---|---|
| `Document/research-docs/Auth/01-auth-baseline-research.md` | `27`, `49` | Distinguish HttpOnly policy from current raw-token FE implementation | `PENDING` |
| `Document/research-docs/Auth/01-auth-baseline-research.md` | `36-38`, `49`, `58-60` | Add refresh/logout cookie-vs-body mismatches | `PENDING` |
| `Document/research-docs/Auth/01-auth-baseline-research.md` | `36`, `45`, `49` | Add AuthSession response-shape mismatch | `PENDING` |
| `Document/research-docs/Auth/01-auth-baseline-research.md` | `46` | Correct `refresh_sessions` schema inventory; separate target fields from implemented fields | `PENDING` |
| `Document/research-docs/Auth/01-auth-baseline-research.md` | `59-60`, `64` | Align endpoint decision with accepted SPEC-002 `/api/v1/auth/me` | `PENDING` |
| `Document/research-docs/Auth/01-auth-baseline-research.md` | `35-38`, `66` | Record the FE 204 response parsing gap | `PENDING` |

### Review safety record

- Source code changed by this review: `NO`
- Configuration/dependencies changed: `NO`
- Architecture/ADR/SPEC changed: `NO`
- PR merged or approved: `NO`
- Jira comment posted: `YES` — review verdict `REQUEST_CHANGES`.
- Corrections applied to the PR research file: `NO` — owner must apply manually.

---

## Future review entry template

Copy this section for each subsequent research review and append it below the previous entry.

```md
## Review NNN — <Jira key> / <PR number>

- **Date:** YYYY-MM-DD
- **Jira:** <issue key and title>
- **PR:** <PR URL>
- **Review verdict:** `APPROVE` / `REQUEST_CHANGES` / `BLOCKED` / `PASS_WITH_NOTES`
- **Review scope:** <research-only or other explicitly authorized scope>
- **Current status:** `PENDING MANUAL CORRECTION` / `READY FOR RE-REVIEW` / `ACCEPTED`

### Overall assessment

<Short evidence-based assessment.>

### Required corrections

#### Correction 1 — <short title>

- **Target file:** `<path>`
- **Target lines/area:** `<lines or section>`
- **Current issue:** <what is wrong or incomplete>
- **Required correction:** <what the owner must change>
- **Evidence:** `<file:line>`
- **Reason:** <why the correction is required>

### Acceptance status after correction

- **Research scope coverage:** `PASS` / `PARTIAL` / `FAIL`
- **Requirement coverage:** `PASS` / `PARTIAL` / `FAIL`
- **Source evidence accuracy:** `PASS` / `PARTIAL` / `FAIL`
- **Security/runtime conclusion:** `PASS` / `PARTIAL` / `FAIL`
- **Test evidence:** `PASS` / `PARTIAL` / `FAIL`
- **Architecture alignment:** `PASS` / `PARTIAL` / `CONFLICT`
- **Ready to accept:** `YES` / `NO`

### Files that require manual correction

| File | Lines/area | Action | Status |
|---|---:|---|---|
| `<path>` | `<lines>` | <manual correction> | `PENDING` |

### Review safety record

- Source code changed by this review: `NO`
- Configuration/dependencies changed: `NO`
- Architecture/ADR/SPEC changed: `NO`
- PR merged or approved: `NO`
- Jira comment posted: `YES` / `NO`
- Corrections applied: `NO` / `YES`
```
