# ADR-009: Continuum-Owned Tasks Stored in MongoDB

- **Status:** Accepted
- **Date:** 2026-10-01
- **Decision owner:** Continuum AI project team
- **Scope:** DATN MVP task lifecycle, Work Note references, SAG indexing boundary, and handover task selection

## Context

The earlier technology baseline treated Jira as the source for DATN tasks and proposed Jira sync into Continuum. The product now needs its own task-management capability so work ownership and state remain available to Continuum's knowledge-capture and successor-handover workflows. Continuum already uses MongoDB/Mongoose as its primary operational store and enforces authorization in the Continuum API.

## Decision

1. Continuum is the canonical and only task source for DATN in the MVP. Users manage tasks through the Continuum Task API; canonical task records are persisted in MongoDB.
2. Jira task import, webhooks, reconciliation, and two-way synchronization are outside the current MVP.
3. A Work Note may optionally reference an internal task using a logical `taskId`. A task provides context only; it does not replace the author's confirmed Work Note or become verified knowledge automatically.
4. Only Work Notes and evidence that pass Continuum authorization and source-eligibility checks may be sent to SAG retrieval/indexing. Task records and task lifecycle state remain in MongoDB and are not standalone SAG sources.
5. During handover, an authorized Team Leader reads task candidates from the Continuum Task API, chooses the tasks to include, and assigns selected tasks to the scoped successor. The Task API remains authoritative for task state; handover stores its own workflow and task references, not a second mutable task record.

## Consequences

- Continuum APIs must enforce organization/project/team scope and applicable resource ACL for task reads and writes. Task-linked Work Note creation must validate the optional `taskId` against the caller's scope.
- MongoDB schema documentation must define the Task collections, tenant/project references, indexes, lifecycle/audit needs, and the Work Note `taskId` reference before implementation. They belong in the existing approved operational MongoDB store (`continuum_db` per DEC-011/SPEC-001); this decision does not create a separate `continuum_task` database. Exact Task API routes, fields, status values, and authorization matrix remain governed by the Task Use Case/SRS review.
- SAG ingestion must receive eligible source content through a Continuum-controlled boundary and preserve source references/ACL. Permission changes must be reflected before subsequent retrieval and context construction.
- Handover must not copy task status/owner as a second writable source. It records the selected task reference, successor assignment, and handover-specific acknowledgement state.
- MongoDB deployment requirements for any multi-document task/history/audit transaction must be specified with the schema. The accepted technology baseline already requires a replica set for MongoDB multi-document transactions.
- This decision selects MongoDB only for operational task records. The accepted MVP SAG retrieval target remains LanceDB (DEC-015/SPEC-005); PostgreSQL + pgvector/Qdrant in database-design is a future/alternative design, not an engine selection. The runtime implementation and deployment still need source verification.

## Alternatives considered

| Alternative | Decision | Reason |
|---|---|---|
| Jira remains canonical and Continuum mirrors issues | Rejected for MVP | Adds external availability, sync, credential, and permission coupling to task capture and handover. |
| Split task lifecycle between Continuum/MongoDB and SAG/PostgreSQL | Rejected | Creates competing writable records and requires cross-store authorization/state reconciliation. |
| Continuum Task API with MongoDB canonical records | Accepted | Aligns task operations with Continuum's existing operational data and authorization boundary. |

## Related documents

- [Technology baseline](Tech.md)
- [MVP Scope](../research-docs/01_MVP_SCOPE.md)
- [Daily workflow and internal task management](../research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md)
- [Task-management Use Cases](../research-docs/Internal-Work-Management/12-continuum-task-management-use-cases.md)
- [Task schema boundary](../database-design/12_TASK_MANAGEMENT_SCHEMA.md)
