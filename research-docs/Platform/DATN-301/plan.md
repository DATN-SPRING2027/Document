# DATN-301 — Kế hoạch đóng gate PLATFORM_OPERATOR V1

| Field | Value |
|---|---|
| Jira | DATN-301, parent DATN-293 |
| Contract | [PLATFORM_OPERATOR V1](../platform-operator-v1-contract.md) |
| Decision record | [design.md](design.md) |
| DB runbook | [Read-only verification](../platform-operator-v1-db-verification-runbook.md) |
| Scope | Documentation and Jira synchronization only |
| Outcome | Contract ready except external Security/IAM, Audit and DB evidence |

## Final implementation boundary

- Active: PLAT-ORG-01, PLAT-HEALTH-01, PLAT-AUDIT-01 using unchanged DATN-79/A-04 permissions and behavior.
- Deferred from V1: all remaining 37 candidate operations in canonical contract §4.3. No permission, endpoint, UI or QA feature is implied.
- Configuration: OUT OF V1.
- Effective active permission count: 3. DATN-79 is unchanged.

## Completed decision work

1. Inspected Jira DATN-293–301, DATN-79, DATN-80 and A-04 subtasks; checked current repo authorization, assignment schema/index declarations, transaction/audit implementation and migration behavior.
2. Dispositioned every operation ACTIVE or DEFERRED FROM V1 with reason, owner, evidence and implementation impact.
3. Specified the exact PO-AUTH-01 bootstrap/recovery/revoke procedure, identity proof, issuer/executor separation, no self/operator grants, legacy-row policy, concurrency, idempotency, rollback, last-operator and post-check.
4. Specified audit events/fields, redaction, read/export/denial handling, atomic failure semantics, proposed retention/archive/deletion and exact external signers.
5. Resolved DEC-ACCESS-10 for the active A-04 catalog; left broader resource classifications for unrelated capabilities open.
6. Marked DB deployment reality UNVERIFIED and created a read-only runbook. No collection data was queried or changed.
7. Synchronized canonical contract, decision record, readiness references and Jira descriptions without status transitions; identified stale `DATN-301 blocks` links to DATN-296–300 for removal while retaining the historical DATN-294 prerequisite and external gate for DATN-295.
8. Cross-checked for count/permission/operation/readiness consistency; docs only.

## Remaining gates

- Security/IAM must name and approve the issuer/executor and PO-AUTH-01 controls.
- Security/IAM + DB must approve legacy assignment/regrant handling and operation-ID storage.
- Security/IAM + Security/Audit + Privacy/Legal must approve retention/enforcement.
- IAM DB owner must provide read-only staging/prod evidence using the runbook.

These are external approvals/access facts; no unresolved policy wording remains for the active V1 catalog. Child readiness is recorded in the contract and design record. Keep Jira statuses as-is until an authorized human updates the workflow.
