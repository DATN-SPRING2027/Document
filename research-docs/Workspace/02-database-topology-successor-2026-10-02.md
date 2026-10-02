# Database topology alignment after ADR-003

**Decision status:** ACCEPTED by the Authorized Human Architecture Decision Authority on 2026-10-02.
**Authority:** Workspace `docs/adr/ADR-003-database-per-service-persistence.md` and successor text in DEC-011.
**Scope:** Logical MongoDB database ownership and runtime topology. This does not select a new physical cluster, change MongoDB as the operational source of truth, alter SAG storage, or resolve the Task/Jira product scope.

## Accepted rule

- MongoDB 7.0 remains the operational source of truth on the existing cluster/replica set.
- Every active bounded service owns its own logical MongoDB database.
- Cross-cutting audit records use `continuum_audit`.
- A service reads and writes only its owned database. Cross-service reads/writes use approved service APIs or domain events.
- The old `continuum_db` is a migration source only. No source records are deleted by the split.
- Migration requires a clean deterministic dry-run, a verified backup, paused source and target writers, an exact reviewed report hash, and separate environment cutover authorization.

## Current DATN-BE runtime inventory

| Runtime owner | Logical database |
| --- | --- |
| IAM | `continuum_iam` |
| Capture | `continuum_capture` |
| Jira | `continuum_jira` |
| Lifecycle | `continuum_lifecycle` |
| Chat | `continuum_chat` |
| Handover | `continuum_handover` |
| Ingestion | `continuum_ingestion` |
| Notification | `continuum_notification` |
| Cross-cutting audit | `continuum_audit` |

The current DATN-BE deployment and service persistence definitions provide the runtime inventory. Product schema catalog targets `continuum_task` and `continuum_ai_adapter`, but neither has a matching active runtime owner in the current BE chart. Product docs mark Jira historical, while the current BE runtime still deploys Jira. Retiring Jira or adding Task/AI Adapter to the migration inventory requires an explicit implementation and ownership reconciliation; the database topology approval alone does not settle that product decision.

**ARCHITECTURE / INVENTORY RECONCILIATION — FOLLOW-UP:** Keep the current `continuum_jira` runtime mapping for this split. Do not remove, rename, or reassign its data, and do not add `continuum_task` or `continuum_ai_adapter` to the migration inventory until their service ownership is resolved separately.

## Implementation and migration status

The DATN-BE work package is aligning named Mongoose connections, service-specific `SERVICE_DATABASE` configuration, audit writes, migration scripts, and tests with this decision. The migration planner maps only the nine databases listed above, preserves `_id` and every source record, detects unowned collections such as legacy `outbox_events`, same-ID content conflicts, unique-index conflicts, and incompatible indexes/options. It does not infer ownership for data without an authoritative mapping.

No live database has been mutated by this work package. The migration must stop if the dry-run is not clean. In particular, an unowned collection or unresolved target mapping must be reported for authority before any copy is applied.
