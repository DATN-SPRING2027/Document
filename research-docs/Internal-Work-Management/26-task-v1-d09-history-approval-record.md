# DATN-101 — D-09 Task History Contract Approval Record

- **Decision date:** 2026-10-19 (Asia/Bangkok).
- **Decision maker:** The requester, who identified themself as Project Leader and decision maker for project decisions.
- **Authority scope:** The requester's explicit approval applies only to the limited D-09 contract and implementation scope recorded below. This record does not claim independent approval by any other person or authority.
- **Source revision:** D-13-R6, Document `main` blob `2de31568004b619db9037144d39fe0edb8a24ff3` (2026-10-18).
- **Approval evidence:** The user's explicit DATN-101 task-conversation decision: “I choose Option A — approve a limited D09 contract for DATN-101,” followed by the eight constraints recorded here.
- **Evidence limitation:** Authority and identity are requester-asserted in the task conversation. This record is scoped to DATN-101 and does not approve production activation, Gateway/FE integration, or a permanent retention policy.

## Approved D-09 scope

1. **Event allowlist:** Expose only `TASK_CREATED` and `TASK_STATUS_TRANSITIONED`. Do not add assignment or metadata events, whole-Task snapshots, arbitrary payloads, or sensitive Task-field values.
2. **Authorization:** Require active Project membership and permission to read the specific Task within the caller's current scope. Re-resolve authorization on every request. Organization Admin and Platform Operator roles do not grant implicit content access. A successor may read only a Task validly transferred through Handover while every applicable access condition remains satisfied. Return `404` for out-of-scope resources.
3. **Ordering and pagination:** Order by ascending resulting Task version, then event `_id` ascending. Default `limit` is 20; maximum is 100. A page beyond the current result range returns an empty list. Page-number pagination does not guarantee a stable snapshot when events are appended between requests; no snapshot consistency is promised.
4. **Temporary retention behavior:** Do not add an event TTL or retention migration in D-09. For this MVP slice, history follows the Task lifecycle. This is temporary and is not a permanent retention approval. Indefinite retention requires a separate policy decision before broader production enablement.
5. **Versioned response DTO:** Normalize the existing persisted event variants into a `schemaVersion: 1` response DTO for the two allowed event types. Preserve the existing persisted event documents. The DTO may expose event identity, actor, source, timestamp, resulting version, and allowlisted changed-field names; a status delta may include `fromStatus` and `toStatus`. It must omit free-text reason, Task field values, snapshots, operation/correlation identifiers, and unrecognized persisted properties. No database migration is authorized unless implementation inspection proves it necessary and the separate DB workflow is followed.
6. **Verification:** Tests must cover active Project membership, revoked membership, Project/Task scope, valid and invalid Handover successor access, event allowlisting, deterministic ordering, pagination boundaries, concurrent event insertion without claiming cross-request snapshot consistency, and Task/event write failure atomicity. MongoDB replica-set integration tests may be reported as passed only when the required fixture is verified available and the tests actually complete.
7. **Dormant runtime boundary:** Keep implementation dormant. Do not activate the business route, Gateway, FE integration, or production callers. DATN-103 and DATN-104 remain downstream consumers.
8. **Decision boundary:** This approval applies only to the stated DATN-101 scope. It does not approve production activation, a permanent/indefinite retention policy, additional event types, or unrelated Task V1 operations.

## Implementation and verification gates

- Backend work must remain on a fresh BE branch based on the current `origin/main` and use a separate BE PR.
- No schema, collection, index, TTL, data migration, shared database, or production database change is included in the approved D-09 scope.
- The history query must return the same safe DTO for old persisted creation and status-transition event records without rewriting those records.
- The history authorization evidence provider must fail closed when unavailable and resolve current Project membership, Task scope, and Handover access for each request. The current runtime remains unconfigured and deny-all.
- Broader production enablement requires a separate decision covering runtime ownership/migration prerequisites and a permanent retention policy.
