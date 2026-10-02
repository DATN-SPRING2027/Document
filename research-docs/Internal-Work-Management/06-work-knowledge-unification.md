# Work and Knowledge Unification Research

**Trạng thái:** Conceptual research; không phải schema hay requirement được chấp thuận.

> **Decision amendment — 2026-10-02:** Continuum Task API/Task Service is the approved canonical source for DATN task lifecycle in the MVP. Work Notes and handover records may link to a task using an optional logical `taskId`; they resolve task details through the Task API/event contract. Task records themselves are not SAG knowledge sources. Only authorized Work Notes/evidence that satisfy the ingestion policy may enter retrieval/indexing. Jira is not the task source for this MVP.

## Bài toán khái niệm

Work/task trả lời “đang làm gì, ai chịu trách nhiệm, trạng thái/điều kiện hoàn tất là gì”; knowledge trả lời “đã học/xác minh được gì, bằng chứng ở đâu, ai tin cậy/duyệt, người sau dùng thế nào”. Hai loại thông tin liên quan nhưng không đồng nhất.

- `[DOCUMENTED]` Continuum MVP links Continuum task context with user-confirmed Work Note/Capture; a knowledge proposal requires evidence and human review before reaching verified state. Knowledge continuity and handover are the current MVP goals.
- `[UNKNOWN]` “Work Item”, “Decision”, “Document”, “Discussion” và “Evidence” như unified platform objects chưa được phê duyệt trong Continuum scope.

## Conceptual graph để nghiên cứu

```text
Continuum task (canonical in MVP)
  ├── assigned to → person/team (scope TBD)
  ├── references → requirement / decision / document / discussion
  ├── linked from → commit / pull request / optional future external source reference
  └── has context → capture / work note
                         └── may propose → knowledge object
                                              ├── supported by → evidence/source
                                              ├── verified by → authorized human
                                              └── used for → retrieval / handover
```

Arrows are conceptual links, not foreign keys or approved product relationships.

## Source-of-truth separation

| Information | Possible canonical source | DATN evidence/status |
|---|---|---|
| Operational records/users/projects/work notes | MongoDB 7.0 on the existing cluster; one logical database per active bounded service; cross-cutting audit in `continuum_audit` | `[ACCEPTED DECISION / CURRENT RUNTIME]` Active BE inventory is eight domain databases plus audit, including `continuum_jira`; `continuum_task` and `continuum_ai_adapter` are not yet active runtime databases. Migration/cutover is separate. `continuum_db` is a migration source, not an active runtime target. |
| Task lifecycle | Continuum Task API/Task Service; target database `continuum_task` | `[APPROVED TARGET, NOT CURRENT RUNTIME]` Canonical task source for the MVP, separately deployed from source in the existing `DATN_BE` repository. ADR-003 excludes `continuum_task` from the current active runtime database inventory until its runtime owner and migration contract are implemented. |
| Jira runtime/integration | Current BE runtime inventory includes `continuum_jira`; product docs mark Jira historical | `[CURRENT RUNTIME / PRODUCT SCOPE RECONCILIATION]` Jira is not the canonical task source in the approved MVP. Runtime presence does not establish a Jira task-sync requirement or a complete connector. |
| Code and review events | GitHub repository/PR | `[INFERENCE]` source type, not integrated work product evidence |
| Files/docs | Drive/Confluence or other user-selected repository | `[UNKNOWN]` current DATN connector/use agreement |
| Verified knowledge facts/proposals | Continuum persistence + provenance model | `[DOCUMENTED]` conceptual lifecycle; end-to-end completeness not proven by schemas |
| Semantic retrieval index | LanceDB per accepted DEC-015/SPEC-005; auxiliary retrieval, not operational SoT | `[DOCUMENTED]` target decision; source/runtime integration appears incomplete in current repo evidence |

MongoDB is the operational source of truth for accepted Continuum target; LanceDB is an auxiliary SAG retrieval store. PostgreSQL+pgvector is a future SAG scaling option only. These architecture decisions do not imply that every external task/file/discussion must be copied into MongoDB.

## Traceability properties to test

`[PROPOSAL]` A knowledge result should answer: source URI/id; source system; captured/updated timestamps; project/team scope; author/owner; content version or revision; verification state and verifier; authorization basis; ingest/sync state; deletion/revocation propagation. Define which are needed per object before implementation.

For retrieval: verify permissions before model context construction, carry citations/evidence into answer, exclude inaccessible/deleted/stale material, and distinguish generated inference from verified source. For capture: explicit user confirmation, idempotency, duplicate handling, and clear task-link behavior.

## Boundaries and unknowns

- `[UNKNOWN]` Whether users need one product UI or only reliable links across tools.
- `[UNKNOWN]` Whether a knowledge object may have multiple project/team scopes or versions.
- `[UNKNOWN]` Decision/document/discussion lifecycle, ownership, approval, retention and deletion policy.
- `[DECISION REQUIRED]` Exact Task API/event fields, lifecycle and authorization contract; the canonical task source is already decided.
- `[DECISION REQUIRED]` Which content classes may be indexed by SAG, with ACL and retention behavior.

## References

`product_docs/research-docs/01_MVP_SCOPE.md`; `03_DAILY_WORKFLOW_AND_JIRA_SYNC.md`; `docs/decisions/decision-register.md` DEC-011/015; `docs/specs/SPEC-001-MONGODB-PERSISTENCE.md`; `SPEC-005-SAG-LANCEDB.md`.
