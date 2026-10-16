# DATN-301 — Gate closure todo

Jira: DATN-301 · Parent: DATN-293 · Contract: [DATN-294](../platform-operator-v1-contract.md) · Decisions: [design.md](design.md)

## Completed in this documentation change

- [x] Preserve exactly three active A-04 permissions and operations; DATN-79 unchanged.
- [x] Assign all 37 remaining candidate operations DEFERRED FROM V1, each with rationale, owner, evidence and implementation effect.
- [x] Resolve the active V1 permission bundle; no full-40 runtime grant.
- [x] Define all 16 domains and exclude Configuration.
- [x] Define actor/action/resource/scope for active operations and the controlled PO-AUTH-01 procedure.
- [x] Define identity verification, issuer/executor, no self/operator grant, bootstrap/recovery, last operator, race/CAS, retry/idempotency, timeout, rollback and post-verification.
- [x] Define audit coverage, required fields, redaction, read/export/denial, retention proposal, integrity, access and failure semantics.
- [x] Resolve DEC-ACCESS-10 for active A-04 operations; preserve broader global decision scope.
- [x] Create read-only DB verification runbook and record actual DB as UNVERIFIED.
- [x] Set deterministic readiness for DATN-295–300 without changing Jira workflow statuses.
- [x] Preserve all existing Jira issue links per KeyT's explicit choice; DATN-301 is Done and the retained links remain traceability, while DATN-295 still has external approval/evidence gates.
- [x] No runtime code, migration, seed, DB write, ACL, RAG or ingestion change.

## External approvals/evidence only

- [ ] Security/IAM names issuer/executor and signs PO-AUTH-01 identity/MFA, legacy guard, last-operator, recovery and transaction controls.
- [ ] Security/IAM + DB approve legacy-row/regrant behavior and operation-ID ledger storage.
- [ ] Security/IAM + Audit + Privacy/Legal approve retention/archive/backup/deletion/read/denial policy or give exact replacement.
- [ ] IAM DB owner provides read-only staging/prod report per [runbook](../platform-operator-v1-db-verification-runbook.md).

## Readiness

| Task | Status | Exact gate |
|---|---|---|
| DATN-295 | EXTERNAL APPROVAL REQUIRED | Signed Security/IAM/Audit package and actual read-only environment report before implementation/migration |
| DATN-296 | READY | Preserve PLAT-ORG-01; no new administration API |
| DATN-297 | READY | Preserve PLAT-HEALTH-01; no new operations API |
| DATN-298 | READY | No administration UI in V1 |
| DATN-299 | READY | No operations UI or Configuration |
| DATN-300 | READY | Test oracle fixed; bootstrap transaction tests follow DATN-295 tool |

Do not infer Security/IAM or Audit approval from Jira status Done, and do not transition child statuses. Existing issue links are intentionally preserved; READY describes deterministic implementation scope, not a request to edit Jira dependencies.
