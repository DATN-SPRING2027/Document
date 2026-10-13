# DATN-95 — Task V1 contract approval record

- **Status:** Partially approved — recommendation-level decisions only.
- **Approval date:** 13/10/2026 (Asia/Bangkok).
- **Approver:** Trần Kim Thắng (Leader, per [`Member.md`](../../Member.md)); the user directly confirmed in this conversation: “giờ tôi là leader tôi xác nhận.”
- **Evidence:** User reply “approve + research unknown,” followed by “chưa cần research bên .sage, bây giờ chỉ cần appove.”
- **Approved source revision:** Product Docs `145af128e70fcfbcd6a64d5ac7859dfb9468d14c` (PR #29 merge; includes PR #28).
- **Decision scope:** The concrete recommendations in §12 of [the Task V1 contract closure proposal](19-task-v1-contract-closure-proposal.md), with the limits and UNKNOWNs below.

This record captures the Leader's approval of the proposal recommendations at the stated revision. It does not turn conditional or incomplete proposals into exact schema/API requirements. In particular, it does not approve an exact field dictionary, permissions matrix, lifecycle enum, or any of the 25 state-transition cells. Those decisions remain UNKNOWN. This partial approval does not satisfy all DATN-95 acceptance criteria and does not unblock D-03 implementation.

## Approved recommendations

| Decision | Approved recommendation | Remaining UNKNOWNs / conditions |
|---|---|---|
| V1 scope | Target the core Project-local list, create, detail, edit, assignment, status command, search, and limited history slice. Work Note/Handover integration is optional and only enters V1 when its owner approves the exact contract. Defer advanced capabilities, including Agent behavior, unless separately scoped. | Exact UC-TM inclusion, actor/action/scope permissions, filters, response projections, and field-level edit rights remain open. A status command does not enable any transition; all 25 transition cells remain UNKNOWN and disabled. |
| Field principles | Persist a stable Task ID, Project ownership, title, creator, server-derived timestamps, and only fields required by approved operations. | Exact field names, storage/API types, required/null/default/editable rules, length/range limits, date semantics, and any optional fields remain UNKNOWN. |
| Project and Organization ownership | The Project owns each Task. Organization is contextual. Persisting a derived `organizationId` is conditional on an approved query or isolation need. | Whether `organizationId` is stored, and its derivation/integrity rules, remains open. |
| Relationships | Use one Project per Task; adopt the recommended 0..1 Team and 0..1 assignee cardinalities, optional logical Work Note reference, and Handover through Task API/logical ID. | Eligibility, cross-scope checks, Work Note cardinality and stale-link behavior, and Project/Team/User removal or transfer rules remain UNKNOWN. |
| Validation | Use API and database validation for approved shape constraints; derive trusted actor/context fields server-side and validate cross-service scope through the owning contract. | Exact validators, enums, requiredness, bounds, failure precedence, and API error responses remain UNKNOWN. |
| Uniqueness | Do not require unique Task titles. Use `_id` as the default unique key; add operation/event uniqueness only after an approved invariant defines it. | Operation and event key scope/retention/idempotency contracts remain open. |
| Query/index approach | Derive indexes from approved Project-scoped list/detail/history workloads and representative query plans; omit speculative Team or due-date indexes. | Exact query parameters, sort/pagination behavior, and index definitions remain UNKNOWN until workload approval and `explain()` review. |
| History boundary | Keep `task_events` append-only and limit provenance to safe actor/action/target/time/change metadata. | Exact event schema, which mutations emit events, before/after projection, visibility, ordering, retention, and redaction remain UNKNOWN. |
| Mutation/history atomicity | Retain the already accepted B4 boundary: a Task mutation and its corresponding required history record commit or roll back together. | Exact history coverage, transaction failure mapping, and implementation evidence remain outstanding. |
| Event publication and outbox | Do not add a transactional outbox to V1 unless a named durable consumer is approved. History is not event delivery. | No durable consumer was identified in the proposal evidence; whether a consumer exists remains UNKNOWN and must be checked before any publication requirement is finalized. If one is approved, define its delivery contract and revisit the outbox decision. |
| Deletion | Do not add a Task delete/archive field or route to V1 before deletion, privacy, retention, and relationship rules are decided; do not infer cascades or transfers. | Parent deletion, member removal, retention, recovery, and dangling-reference behavior remain UNKNOWN. |
| Test/failure strategy | Use disposable MongoDB replica-set integration tests for approved indexes, validation, persistence, rollback/atomicity, authorization boundaries, and outbox behavior if applicable. | Exact executable oracles, API error contract, target test configuration, and all runtime test results remain outstanding. |
| Approval authority | Record Trần Kim Thắng as the Leader approving the scoped recommendations in this record, based on the direct confirmation in this conversation and the project roster. | This approval does not confer or imply separate authority for other product, security, API, or operational decisions. |

## Decisions that remain open

- The exact Task V1 use-case list and actor/action/resource/scope permission matrix.
- The complete data dictionary, including field types, requiredness, nullability, defaults, lifecycle, and validation limits.
- The D-02 state/default contract and all 25 transition cells. No edge is enabled by this approval.
- Team/assignee eligibility, Work Note relationship behavior, and deletion, membership-removal, and transfer semantics.
- Approved search/list/history workloads and resulting concrete indexes.
- Event vocabulary and coverage, history projection, retention, redaction, and API access rules.
- Whether any durable event consumer is required in V1; the outbox remains deferred unless one is named and approved.
- Exact API success/error semantics and executable test oracles.
- Reconciliation of the accepted Task-service deployment target in ADR-010 with the backend repository's current architecture instructions before implementation.
- SAGE traceability and full DATN-95 acceptance evidence.

## Readiness and change boundary

DATN-95 remains **In Progress** and D-03 remains **BLOCKED**. This approval establishes recommendation-level scope and authority evidence, but exact contract items are still open, and no Task implementation or disposable integration tests exist. Reassess DATN-95 only after the owning contract is updated, unresolved dependencies and architecture conflicts are reconciled, and the required test evidence is produced.

No SAGE files, Jira fields/comments/statuses, backend/frontend code, schema, index, migration, runtime configuration, or database contents were changed for this approval record.
