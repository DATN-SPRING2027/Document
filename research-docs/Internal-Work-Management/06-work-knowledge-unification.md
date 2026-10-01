# Work and Knowledge Unification Research

**Trạng thái:** Conceptual research; không phải schema hay requirement được chấp thuận.

## Bài toán khái niệm

Work/task trả lời “đang làm gì, ai chịu trách nhiệm, trạng thái/điều kiện hoàn tất là gì”; knowledge trả lời “đã học/xác minh được gì, bằng chứng ở đâu, ai tin cậy/duyệt, người sau dùng thế nào”. Hai loại thông tin liên quan nhưng không đồng nhất.

- `[DECIDED — 2026-10-01]` Continuum tự sở hữu vòng đời task DATN và liên kết Task nội bộ với Work Note/Capture do người dùng xác nhận. Knowledge proposal vẫn cần evidence và human review trước verified state; continuity và handover vẫn là mục tiêu MVP.
- `[UNKNOWN]` “Work Item”, “Decision”, “Document”, “Discussion” và “Evidence” như unified platform objects chưa được phê duyệt trong Continuum scope.

## Conceptual graph để nghiên cứu

```text
Continuum Task (canonical for DATN)
  ├── assigned to → person/team (scope TBD)
  ├── references → requirement / decision / document / discussion
  ├── may reference → commit / pull request / external issue link (future, if approved)
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
| Operational records/users/projects/work notes | MongoDB `continuum_db` per accepted DEC-011/SPEC-001 | `[DOCUMENTED]` architectural decision; implementation maturity must be checked separately |
| Task lifecycle DATN | Continuum internal Task module | `[DECIDED — 2026-10-01]` canonical task source; detailed fields, status set and project/team cardinality remain subject to Use Case approval |
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
- `[UNKNOWN]` Exact task fields, fixed status set, and project/team ownership cardinality; these are documented as proposals in `12-continuum-task-management-use-cases.md`.
- `[DECISION REQUIRED]` Which content classes may be indexed by SAG, with ACL and retention behavior.

## References

`product_docs/research-docs/01_MVP_SCOPE.md`; `03_DAILY_WORKFLOW_AND_JIRA_SYNC.md`; `docs/decisions/decision-register.md` DEC-011/015; `docs/specs/SPEC-001-MONGODB-PERSISTENCE.md`; `SPEC-005-SAG-LANCEDB.md`.
