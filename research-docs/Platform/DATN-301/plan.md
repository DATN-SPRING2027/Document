# DATN-301 — Implementation plan for usable PLATFORM_OPERATOR V1

## Current V1 boundary

Keep the existing A-04 organization.create, platform.health.read and platform.audit.read behavior. Add only PLAT-ORG-02 safe Organization list/detail, PLAT-USER-01 exact normalized-email lookup for an ACTIVE User, PLAT-MEM-01 bounded membership read, and PLAT-MEM-03 suspension only. Invite, membership resume/remove, role change, Organization/User status changes, Projects, Sessions, Operations, export and Configuration remain excluded.

## Dependency order

1. Contract and decision: PO-D13, exact API/projection/error/audit/QA mapping, operation matrix and approval record.
2. DB model branch: add the exact permission enum values and compatible legacy/new PO-AUTH bundle validation. Add a separate additive, report-first provenance snapshot index migration; no assignment data backfill/update; do not modify existing migrations or apply the new migration before external gates close.
3. BE branch: add server-side exact permissions; current Platform session recovery; bounded Organization/User/Membership reads; platform-only suspension through the existing transaction/audit path; extend fixed audit allowlist.
4. FE branch: dedicated Platform auth/sign-in/session recovery; separate shell; Organization create/list/detail; exact User picker; membership list/suspend; Health and Audit views.
5. QA: BE unit/integration/E2E for permissions, target resolution, legacy bundle, CAS/replay/audit rollback; FE unit/build/typecheck and browser flow; cross-system security review.
6. As-built: update canonical contract, DATN-301 record, task folder, Jira issue descriptions, diff and handoff. Keep Jira workflow status unchanged.

## Verification gates

- Exact current permission on every protected request; do not trust client permission or scope.
- Route resource IDs are resolved in BE and Organization/Membership relationships are checked.
- Membership suspend retains self-action and last eligible Organization ADMIN guards.
- Mutations use Idempotency-Key and expected version; stale state returns 409.
- Business change, operation record and required audit commit atomically; audit failure returns no success.
- FE uses existing BFF/cookie/CSRF conventions and never stores access/refresh tokens in local storage.
- No secret, tenant content, Project ACL, RAG or ingestion change.
- Actual production/staging DB state remains unverified until a read-only evidence report exists.
