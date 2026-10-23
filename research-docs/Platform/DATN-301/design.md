# DATN-301 — PLATFORM_OPERATOR V1 decision record

| Field | Value |
|---|---|
| Jira | DATN-301 |
| Canonical contract | research-docs/Platform/platform-operator-v1-contract.md |
| Date | 2026-10-16 (Asia/Bangkok) |
| Current decision | PO-D13 supersedes the earlier empty-console / 3-active scope |
| Product owner | Thang, from the explicit task instruction |
| Jira workflow | Existing statuses remain unchanged by this decision |

## 1. Current scope revision — PO-D13

The prior DATN-301 closure recorded three A-04 operations active and all 37 candidates deferred. Thang has now explicitly changed the product goal to a usable Organization, User and Membership administration flow. That prior scope is retained as history but is superseded for current V1 implementation.

V1 has seven exact permissions across seven operation IDs:

- Existing A-04, unchanged: organization.create, platform.health.read, platform.audit.read.
- PLAT-ORG-02: platform.organizations.organization.read — bounded Organization list and detail metadata.
- PLAT-USER-01: platform.users.account.read — exact normalized-email lookup for one eligible ACTIVE User.
- PLAT-MEM-01: platform.memberships.membership.read — bounded membership list within one server-resolved Organization.
- PLAT-MEM-03: platform.memberships.lifecycle.manage — SUSPEND only. Resume and remove stay deferred.

The other 33 candidates remain DEFERRED FROM V1. PLAT-MEM-02 invitation.create stays deferred because DATN-291 currently returns fail-closed 503 until the A7 notification evidence and A8 coordinated cutover are accepted. Resume/remove also remain gated. No gate is bypassed to meet the new goal.

Configuration remains OUT OF V1. No wildcard, hierarchy, break-glass, self-grant, operator-to-operator grant, account-global status change, secret access, project ACL bypass or tenant-content access is introduced.

## 2. Decision rationale

This is the smallest currently usable set supported by existing source and safe failure behavior:

1. The existing Organization create operation provisions the first ACTIVE ADMIN atomically.
2. Organization read and exact ACTIVE User lookup let an operator find a target and select that first ADMIN safely.
3. Membership read provides bounded state and last-ADMIN context.
4. Membership SUSPEND is the lifecycle command already implemented with self-action denial, last-eligible-ADMIN protection, idempotency, version CAS and transactional audit.
5. Invitation, resume and remove are not activated because their existing source readiness gates are still closed. Implementing them by removing those gates would be unsafe.

Platform authority authorizes only the exact operation permission on each request. Organization and Membership IDs are selectors; BE must load and verify the resource and its relationship. The operator does not become a tenant ADMIN and receives no Project or content ACL.

## 3. Active end-to-end contract

The full Actor → Action → Resource → Scope → Permission → API → FE action → Audit → Error → QA mapping is maintained in canonical contract section 4.1A. This table summarizes the selected additions.

| Operation | API | FE action | Audit | Key QA oracle |
|---|---|---|---|---|
| PLAT-ORG-02 | GET /api/v1/iam/platform/organizations; GET /api/v1/iam/platform/organizations/:organizationId | Organization directory/detail | Read-only; no new read audit policy | Exact permission, pagination ≤100, allowlisted fields, unknown ID 404 |
| PLAT-USER-01 | POST /api/v1/iam/platform/users/lookup with `{email}` body and CSRF | Exact User lookup / first ADMIN picker | Do not persist or audit queried email | Exact-match only, ACTIVE User only, minimal response; 404 when no eligible User; invalid email 422 |
| PLAT-MEM-01 | GET /api/v1/iam/platform/organizations/:organizationId/memberships | Membership list | Read-only; no new read audit policy | Exact permission, Organization relationship, bounded projection |
| PLAT-MEM-03 | POST /api/v1/iam/platform/organizations/:organizationId/memberships/:membershipId/suspend | Confirm and suspend | Existing ORGANIZATION_MEMBERSHIP_SUSPENDED event, in same transaction | Cross-Organization ID denied, CAS stale 409, self/last ADMIN guard, replay idempotency, injected audit rollback |
| Existing PLAT-ORG-01 | POST /api/v1/iam/platform/organizations | Create Organization with selected first ADMIN | Existing organization.create event/transaction | Existing response compatibility and audit rollback |
| Existing PLAT-HEALTH-01 | GET /api/v1/iam/platform/health | IAM process liveness | None | Existing {status: ok} response and exact denial |
| Existing PLAT-AUDIT-01 | GET /api/v1/iam/platform/audit | Bounded audit view | None; no recursive audit | Existing response shape, 100-row bound, allowlisted fields/actions |

Platform login remains POST /api/v1/auth/platform/login. Session recovery uses GET /api/v1/auth/platform/me and returns the current identity plus current exact permission codes; it cannot grant permissions. FE display checks are advisory; every BE route independently enforces authorization.

## 4. Decision register

| ID | Decision | Status | Evidence / effect |
|---|---|---|---|
| PO-D01 | Preserve the three A-04 codes and their existing semantics | APPROVED | DATN-79/A-04 and existing runtime |
| PO-D02 | Defer all 37 candidates; only three active | SUPERSEDED by PO-D13 | Original explicit closure request, superseded by Thang's later explicit scope revision |
| PO-D03 | No wildcard, hierarchy, break-glass, public grant endpoint, self-grant or operator-to-operator grant | APPROVED | Current task constraints |
| PO-D04 | PO-AUTH-01 remains two-person, internal, identity/MFA checked, provenance/CAS/last-operator guarded | EXTERNAL APPROVAL REQUIRED; runtime provider intentionally fails closed with 503 | No signed Security/IAM procedure or named issuer/executor is present |
| PO-D05 | Permission assignment, operation ledger and required audit are atomic; stale CAS is 409 | IMPLEMENTED LOCALLY; production provisioning gated | Mongo integration tests cover transaction, snapshot CAS and audit rollback |
| PO-D06 | Preserve audit event shape; add only the membership suspension action to the fixed Platform allowlist | APPROVED product scope; Audit review pending | Existing audit projection and membership audit writer |
| PO-D07 | Retention/archive/deletion policy remains external | EXTERNAL APPROVAL REQUIRED | No signed retention/enforcement policy found |
| PO-D08 | Exact resource lookup; 403 for missing permission; 404 for unknown Organization or mismatched Membership selector | DERIVED for this Platform API | No caller-supplied scope or resource relationship is trusted |
| PO-D09 | Configuration remains OUT OF V1 | APPROVED | Explicit task requirement |
| PO-D10 | Deployed DB state remains UNVERIFIED | EXTERNAL APPROVAL REQUIRED | No approved read-only staging/production report |
| PO-D11 | Never silently adopt or mutate standalone legacy assignments | APPROVED | PO-AUTH-01 provenance guard |
| PO-D12 | One conceptual actor; prior full bundle had only A-04 permissions | PARTIALLY SUPERSEDED | One actor/no hierarchy remains; active bundle is now seven exact permissions |
| PO-D13 | Activate PLAT-ORG-02, PLAT-USER-01, PLAT-MEM-01 and PLAT-MEM-03 SUSPEND only; retain 33 deferred candidates | APPROVED — product scope | Thang's explicit 2026-10-16 instruction; no external sign-off is implied |

## 5. Authority and database model

New PO-AUTH-01 provisioning uses the seven exact V1 permissions. Existing three-code A-04 assignments are not silently upgraded. An explicit V1 expansion must identify a complete, provenance-matched legacy bundle, use a distinct issuer and executor, compare the full pre-state hash, preserve assignment IDs/history, add only the four selected permissions and atomically write an operation record and audit. Standalone/unprovenanced rows are refused unchanged.

The source model change expands local Mongoose permission validation and the operation ledger's accepted exact bundle shapes. Assignment document fields and existing unique indexes do not change. A separate additive, report-first migration adds the non-unique `platform_authority_snapshot_provenance` index for provenance-aware snapshot inspection; it does not backfill or modify assignment records and has not been applied to any environment. Actual database validators/indexes are UNVERIFIED; read-only environment evidence is required before rollout. Do not edit a historical migration or run a DB write to discover state.

## 6. Audit and security boundary

- PLAT-ORG-01 audit and the first ADMIN transaction remain unchanged.
- PLAT-MEM-03 uses the existing membership suspend audit action and its existing transactional write boundary.
- DATN-297 preserves audit response fields, sort and 100-row bound while adding only the new suspension action to its fixed allowlist.
- Reads do not introduce a new read-logging policy in this scope; queried email is never persisted in logs/audit.
- No secret, tenant content, prompt, Project content, job payload, credential, token, MFA value or raw exception reaches the response.
- Existing self-action and last eligible Organization ADMIN safeguards are retained.
- Membership IDs must match the Organization ID loaded from the route; no cross-Organization mutation.

## 7. Remaining external gates

| Gate | Status | Required evidence | Blocks |
|---|---|---|---|
| Security/IAM PO-AUTH-01 | Pending | Named separate issuer/executor, identity/MFA proof, explicit V1 expansion and legacy handling approval | Production permission provisioning |
| Audit / Privacy / Legal | Pending | Review of User identity allowlist, audit projection extension, retention/access controls | Production rollout |
| DB environment state | UNVERIFIED | Read-only redacted report for each target environment; verify indexes/validators/migration history | Production rollout |
| DATN-291 A7/A8 invitation cutover | Pending in existing task | Accepted notification readiness and coordinated migration/cutover | Invite, resume and remove remain deferred |

These gates do not block implementation or local regression tests. No approval signature or production state is inferred from a Jira Done status.

## 8. Jira scope synchronization

Update descriptions and acceptance criteria for DATN-295 through DATN-300 to match PO-D13 and the implementation. Preserve current Jira workflow statuses and issue links; they were Done under the old handoff scope and are not changed by this record. The new description must make the superseding scope visible so Done does not imply that the expanded flow shipped.

## 9. Historical record

The former PO-D02 decision (3 A-04 active, 37 deferred, empty Administration/Operations UI) remains useful as a historical record of the prior closure. It is superseded for current implementation by PO-D13; the old decision must not be applied as a reason to omit the new V1 scope.

## References

- Canonical contract: research-docs/Platform/platform-operator-v1-contract.md
- Existing membership readiness and lifecycle: DATN_BE/tasks/datn-291-organization-membership-mutations-plan.md
- DB verification: research-docs/Platform/platform-operator-v1-db-verification-runbook.md
- Current auth baseline: DATN-79 / A-04 and the inspected DATN_BE source.
