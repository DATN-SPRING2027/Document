# C-07 Team Membership contract

**Revision:** 0.1-draft
**Status:** Draft; only the bounded decisions listed as approved below are approved. All implementation details marked proposed require the approvals in the [Decision Register](DATN-92-Decision-Register.md).
**Parent:** [DATN-92](https://trankimthang0207.atlassian.net/browse/DATN-92) — C-07 Team Membership BE.

## 1. Scope and boundaries

DATN-92 covers Team Membership add, remove, validation, authorization, audit, and tests through DATN-266–271. It does not create Organization or Project Membership, assign roles, invite users, enable self-join, change Team ownership, or expose a Team Membership list.

Only the POST add and DELETE remove operations are in the approved DATN-92 surface. Membership-list GET is excluded. Any existing GET draft remains governed by its owning shared contract and is not silently deleted or changed by this package.

Effective Team admission is subordinate to the exact Organization and Project containing the Team. Membership never grants access to the Organization or Project by itself.

## 2. Evidence-based approved rules

These are the exact bounded C-07 approvals made by KeyT at 11:17 ICT on 2026-10-16, based on the proposal shown immediately before the response. Evidence and attribution limits are recorded in [Approval Evidence](DATN-92-Approval-Evidence-and-Findings.md).

| Rule | Approved scope | Still requires technical resolution |
|---|---|---|
| TQ-05 authorization | Project-scoped `TEAM_LEADER`; explicit Team add/remove authority; no implicit grant. | Canonical permission codes, assignment provisioning/revocation path, actor evidence/fence, and exact scope checks. |
| TQ-06 parent lifecycle | Admission-generation and transaction-fencing direction to prevent silent access restoration after a parent membership is activated again. | Generation source/fields, User suspension scope, all writers, transaction protocol, migration, and proof. |
| Membership lifecycle | Active duplicate add returns `409`; repeated removal returns `204`; after explicit removal, rejoin creates a **new Membership ID and new `joinedAt`**. | Storage/history model, stable pair-slot strategy, rejoin status/Location, and stale-generation re-admission identity. |
| TQ-07/08 scope | Implement POST/DELETE membership operations only; GET/list is excluded from DATN-92; follow the proposed API/error contract subject to consistency verification. | Exact API status/error/precedence, headers, DTO, Gateway forwarding, shared error mapping, and any amendment required for compatibility. |
| TQ-10 consistency | Mutation and audit are in the same transaction; if audit fails, roll back the mutation. | Canonical event/action mapping, allowlist, dedupe/no-op behavior, transaction topology proof, history access, and retention/archival policy. |

TQ-09 is conditional: reuse the C-04 idempotency semantics only if R0 verifies that the referenced C-04 decision was authorized and remains effective. The 11:17 approval explicitly made TQ-09 conditional; it is not a new standalone approval of an unverified C-04 record.

## 3. Proposed eligibility and authorization model

**Recommended, awaiting IAM/Security and domain-owner approval:**

- The actor and target User are `ACTIVE`.
- The actor and target have `ACTIVE` Organization Membership and `ACTIVE` Project Membership in the same Organization/Project that owns the Team.
- The actor has a current Project-scoped `TEAM_LEADER` assignment for that exact Project and the explicit action permission for the requested mutation.
- Team, Project, and Organization identifiers are resolved from authoritative records; request bodies cannot choose or override parent IDs.
- `ADMIN`, Project creator, Project visibility, ordinary Project membership, Team membership, or role name alone does not grant Team Membership mutation authority.
- Mutation revalidates and fences actor authority, target eligibility, Team/Project scope, parent admission generations, and the active-pair invariant inside the write transaction. A retry obtains fresh authorization evidence.
- No Project Membership, Organization Role, or other authority is implicitly created or restored.

The recommended action permission identifiers are `team.members.add` and `team.members.remove`, using the repository's dot-delimited IAM permission style. The existing Team Foundation code currently checks `team:children.manage`; do not accept both spellings as aliases. IAM/Security must approve the canonical IDs and their grant path before the mutation policy is implemented. The historical `team.children.manage` candidate should be reconciled as a distinct Team-management grant, not silently substituted for the add/remove action permissions.

## 4. Proposed Team Membership lifecycle

| Command/state | Contract rule | Approval status |
|---|---|---|
| First eligible add | Create one admission with a new Membership ID and current `joinedAt`; recommended `201 Created`. | New ID/time invariant approved; response code proposed. |
| Add while the pair is actively admitted | Return `409` and create no second active admission. | `409` outcome approved. |
| Remove the current admission | Remove effective admission; recommended retained history state `REMOVED` plus `removedAt`; return `204`. | `204` outcome approved; storage representation proposed. |
| Repeat removal of the same removed admission | Return `204` when the Team/resource is in the caller's authorized scope. | `204` outcome approved; whether this produces a business audit event is open. |
| Explicit rejoin after removal | Create a **different Membership ID** and a **new `joinedAt`**; never reuse the removed ID. | Approved by reference to the proposal; corrected by F-01. |
| Parent suspension/removal then restoration | Old generation proof remains stale; parent restoration must not silently reactivate old access. A fresh authorized add is required. | Generation/fencing direction approved; exact stale-row identity/history behavior proposed. |
| Exact idempotency replay | No duplicate membership, audit, or other domain effect; replay only under the effective C-04 contract and after current authorization is checked. | Conditional on R0 and exact replay contract. |

Recommended response for explicit rejoin is `201 Created` with the new resource `Location` because it creates a distinct admission identity. This is not represented as approved; the API owner must select or amend it.

### Recommended storage constraint — F-07 correction (awaiting DB/domain approval)

The earlier draft proposed a partial unique index on admission rows with `status=ACTIVE`. That conflicts with generation invalidation: a stale admission can remain marked ACTIVE and occupy the unique pair even though it is ineffective, blocking a fresh authorized POST. The recommended logical design uses one stable unique Team/User slot pointing to the current admission ID and separate per-admission history records. Removal clears the slot pointer using a compare-and-set (CAS) while preserving the old admission identity; explicit rejoin or stale-generation re-admission creates a new history ID and `joinedAt`, then replaces the slot pointer transactionally. Exact status/removal-history fields and indexes remain subject to DB/Audit owner approval and MongoDB 7 replica-set proof. See the [DB/parent-writer proposal](DATN-92-DB-Parent-Writer-Design.md#2-recommended-logical-model--awaiting-dbdomain-approval) and finding [F-07](DATN-92-Approval-Evidence-and-Findings.md#f-07--stale-active-row-blocks-fresh-re-admission).

## 5. Invariants

1. At most one **effective** Team admission exists for a Team/User pair; the recommended unique slot key is stable across admission lifecycle changes.
2. Historical removed admissions remain distinguishable from later admissions; explicit rejoin always creates a new ID/time.
3. A missing or stale generation snapshot fails closed; no backfill or parent restoration grants access.
4. Actor authorization and parent eligibility are current at commit, not just at request entry.
5. Membership mutation, its durable command result (if TQ-09 applies), and required audit event commit atomically; any required audit failure aborts the mutation.
6. Rejected requests and exact replays do not create a second membership or business audit event unless the approved Audit/Security policy explicitly says otherwise.
7. Responses and logs expose no cross-Organization/Project membership or target eligibility details.

## 6. Subtask traceability

| Jira subtask | Responsibility | Contract sections |
|---|---|---|
| [DATN-266](https://trankimthang0207.atlassian.net/browse/DATN-266) | Add Team member | 3–5; API POST |
| [DATN-267](https://trankimthang0207.atlassian.net/browse/DATN-267) | Remove Team member | 3–5; API DELETE |
| [DATN-268](https://trankimthang0207.atlassian.net/browse/DATN-268) | Validate Team Membership | 3–5; current generations and active pair |
| [DATN-269](https://trankimthang0207.atlassian.net/browse/DATN-269) | Enforce Team authorization | 3; explicit permissions and fences |
| [DATN-270](https://trankimthang0207.atlassian.net/browse/DATN-270) | Audit Team Membership changes | 2, 5; Audit/Security decisions |
| [DATN-271](https://trankimthang0207.atlassian.net/browse/DATN-271) | Membership tests | all approved and finalized rules |

## 7. Approval and implementation gates

This document is not a production implementation authorization for unresolved policy. Gate A requires approved C-07 decisions and a synchronized versioned contract. Gate B requires the reviewed/merged DB and parent-writer dependencies plus complete readiness evidence. Gate C alone controls runtime write enablement. See [Implementation Readiness](DATN-92-Implementation-Readiness.md).
