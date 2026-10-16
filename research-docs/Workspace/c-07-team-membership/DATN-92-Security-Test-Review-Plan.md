# DATN-92 — Security, Test, and Review Plan

**Revision:** 0.1-draft
**Status:** Test design only; no DATN-92 backend behavior or tests have been implemented on this branch. Test cases whose semantics are approved are marked approved; other expected results require Gate A.

## 1. Threat model and security invariants

Assets: Organization/Project/Team boundaries; membership admission identity/history; actor authority; target eligibility; idempotent command results; audit evidence. Trust boundaries include client → Gateway/BFF → IAM, separate logical audit database, concurrent parent/role writers, and legacy records.

Required invariants:

- Only a current Project-scoped TEAM_LEADER with an explicit action grant may mutate within that exact Project; no implicit grant or cross-project access.
- Actor and target eligibility, scoped RoleAssignment/Role, Team ancestry, and generation snapshots are revalidated/fenced at commit.
- Parent suspension/removal invalidates prior Team proof; parent restoration cannot revive it.
- Explicit removal then rejoin creates a different Membership ID and new `joinedAt` (approved F-01 correction).
- At most one effective admission per Team/User pair; no blind retry after uncertain commit.
- Required audit failure aborts the mutation; logs/events contain no credential or unnecessary personal payload.
- Untrusted parent IDs in the request cannot override Team ancestry. Cross-scope responses do not reveal resource existence/target state.

## 2. Approved lifecycle regression cases

| ID | Scenario | Expected assertion | Status |
|---|---|---|---|
| L-01 | First eligible add | Creates one admission with ID1 and injected `joinedAt` time. | ID/time semantics approved; POST success code pending. |
| L-02 | Add same active Team/User pair with a new command | `409`, no second active row, no second business audit event. | `409` approved; audit no-op recommendation pending Audit owner. |
| L-03 | Remove ID1 | Returns `204`, ID1 no longer effective. | `204` approved; retained state form pending DB owner. |
| L-04 | Repeat removal of ID1 in authorized scope | Returns `204`; remains ineffective. | `204` approved; second audit-event behavior pending Audit owner. |
| L-05 | Explicit rejoin after removing ID1 | Creates ID2 where ID2 != ID1 and new `joinedAt` >/distinct from ID1's injected admission time; old row is not reactivated. | Approved F-01 correction. |
| L-06 | Parent suspend/remove then restore | Old generation snapshot remains stale; membership is ineffective; reactivation does not restore access. | Generation/fencing direction approved; exact fresh admission identity and storage require TQ-06/DB approval. |
| L-07 | Legacy admission missing generation proof | Fails closed; no automatic backfill or access grant. | Recommended safety rule pending DB approval; no implementation until Gate A. |

Do not assert a rejoin HTTP code until API-owner approval; recommended `201` with new `Location` is documented separately.

## 3. Authorization and boundary test matrix

The cases below make target eligibility explicit. The actor context is otherwise valid and authorized under the recommended TQ-05 model (active actor, exact Project-scoped `TEAM_LEADER`, explicit POST grant, trusted Team ancestry); the exact permission identifier and provisioning path remain IAM/Security decisions. API status codes remain pending TQ-07/08 approval. For each denied or raced-out case, assert no slot change, no admission/history write, no durable success result, and no successful business audit event. Rejected-attempt security logging is only asserted if its separate policy is approved. No case may create Project Membership, RoleAssignment, or another authority side effect.

| ID | Target setup / operation | Expected eligibility and result | Persistence / audit assertion |
|---|---|---|---|
| A | Target User is inactive; attempt POST. | Ineligible; deny after actor and Team authorization, without exposing target details to unauthorized actors. | No slot/admission/command-success mutation; no success business audit event. |
| B | Target has no Organization Membership in the Team's Organization; attempt POST. | Ineligible; deny. | No writes or success business audit event. |
| C | Target Organization Membership is suspended or removed; attempt POST. | Ineligible; deny. | No writes or success business audit event. |
| D | Target has no ACTIVE Project Membership in the Team's Project; attempt POST. | Ineligible; deny. | No writes or success business audit event. |
| E | Target is admitted to a different Organization; attempt POST to this Team. | Cross-Organization target; deny with approved concealed/sanitized response. | No writes or success business audit event; no foreign membership details disclosed. |
| F | Target has ACTIVE Project Membership, but only in a different Project; attempt POST. | Wrong Project; deny with approved concealed/sanitized response. | No writes or success business audit event; no foreign Project details disclosed. |
| G | Target is eligible at initial read, then a parent/User eligibility generation changes before commit. | Fence/CAS fails; abort and re-read. If target is now ineligible, deny; if still eligible, only a separately validated retry with current facts may proceed. Never commit from stale reads. | No admission/slot success pointer or durable success result from the aborted stale attempt; no success business audit event from that attempt. |
| H | Existing admission snapshot is stale after parent restore; target is eligible again and a fresh authorized POST is made. | Old admission remains ineffective. Fresh POST creates a different Membership ID and new `joinedAt`, then CAS-replaces the stale slot pointer; approved lifecycle semantics apply. | Exactly one current slot pointer and one new admission; old identity is retained but ineffective. One success audit event only if the eventual approved mapping requires it, in the same transaction; no invented stale-close event. |

- Actor User inactive, Organization Membership suspended/removed, Project Membership inactive, Project archived/inactive, Team hidden/archived, wrong Organization/Project, stale RoleAssignment/Role, or permission revoked during request → no mutation; hidden parent returns scoped `404` under the approved concealment contract.
- Organization ADMIN without explicit Team permission, Project creator without grant, public/visible Project user, ordinary Project member, existing Team member, stale former TEAM_LEADER, and a role name without current scoped assignment → denied.
- `team.members.add` cannot authorize DELETE and `team.members.remove` cannot authorize POST; colon-delimited `team:children.manage` is not an alias after canonicalization.
- Target ineligible/foreign Team User is not disclosed before actor authorization; path Team and Membership IDs are always checked against the exact parent scope.
- Body attempts to supply/override organizationId/projectId/teamId, extra properties, malformed ID, or another user's Membership ID → rejected without side effects.
- CSRF missing/invalid; auth/context missing; Gateway drops actor/context/correlation/idempotency header; response cache headers missing → fail closed and assert no-store.

## 4. Concurrency, idempotency, and audit fault tests

After owner decisions and DB dependencies are implemented, use MongoDB 7 replica-set integration tests and deterministic barriers:

1. Two concurrent add commands for one active pair: exactly one admission; losing command has approved conflict behavior.
2. Add racing with Organization/Project/User suspension or Project/Role revocation: no commit using stale authority; every retry reads current facts.
3. Parent removal/reactivation racing with add/rejoin: stale snapshots never become effective; no silent restoration; fresh POST conditionally replaces only the stale slot pointer.
4. Remove racing with rejoin: old Membership ID remains ineffective; new ID/time is unique; a stale DELETE cannot clear the slot after it has been replaced.
5. Concurrent first slot creation and competing stale-slot replacements: unique slot creation has one winner; CAS losers re-read all actor/target/parent facts and cannot overwrite a newer pointer.
6. Transient transaction conflict and retry: permission, target eligibility, generation, slot pointer, and key state are re-read.
7. Audit write failure after attempted Membership write: entire transaction aborts; no success response or durable command success record.
8. Idempotency same key/same fingerprint: approved original result after current authorization is checked; one domain effect and one business event maximum.
9. Same key/different fingerprint: stable `409`, no side effect.
10. Crash/connection loss at commit: committed, aborted, and unknown outcomes reconcile from durable operation result; never blind-repeat or produce a duplicate audit event.
11. Privacy allowlist: no profile/credential/token/full payload; verify cross-Organization/Project errors and logs disclose no target state.

**F-07 test limitation:** these are acceptance cases only. MongoDB 7 replica-set behavior for slot CAS, history insert, audit transaction, and competing writes has not been run in this environment; do not treat the design as Gate B proof.

Exact event mapping, replay behavior, and retention are not test acceptance criteria until Audit/Security signs the corresponding decision. The transaction rollback invariant is approved.

## 5. API precedence and Gateway tests

After TQ-07/08 detail approval, test pairwise precedence across auth/context, CSRF, malformed request, hidden Team, missing action grant, required command headers/key, key mismatch, ineligible target, active duplicate, stale admission/precondition, rate limit, unavailable dependency, and write/audit failure. Assert stable shared error codes/envelope and sanitized details/requestId.

Test Gateway/BFF-to-IAM POST/DELETE path ownership, auth/context and CSRF propagation, conditional/idempotency header behavior, correlation ID, error pass-through, and `Cache-Control: no-store`. Assert the C-07 OpenAPI has only POST/DELETE and no membership GET.

## 6. Mandatory review loop and finding ledger

For each of DATN-266–271 and again for final integration:

**IMPLEMENT → TEST → REVIEW → FIND → FIX → REGRESSION TEST → RE-REVIEW.**

Review sources, tests, database migration, OpenAPI, authorization, parent writers, transaction boundaries, audit, and Gate C controls. For every real finding record ID, severity P0/P1/P2/P3, file/line or contract section, reproducer/evidence, root cause, fix, regression test, reviewer type (independent or self-review), and re-review result. Do not invent findings. All confirmed blocking P0/P1/P2 findings must be fixed before final Backend PR. An independent code-review capability should be used if available; report it separately from self-review.

## 7. Current verification boundary

This Document PR validates prose/link structure and the draft OpenAPI JSON shape only. No BE tests, migration test, MongoDB transaction proof, Security approval, DB review, Gate A/B/C, or production readiness is claimed. See [Readiness checklist](DATN-92-Implementation-Readiness.md).
