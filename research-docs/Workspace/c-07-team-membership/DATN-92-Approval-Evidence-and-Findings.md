# DATN-92 — Approval Evidence and Finding History

**Revision:** 0.1-draft
**Status:** Evidence register. Historical records remain preserved; this file does not create an approval.

## 1. Approval attribution and scope

### Project-level implementation authorization

- **Approver:** KeyT, identified by the requester as the Jira-recorded DATN Project Owner.
- **Evidence:** direct conversation screenshot supplied by the requester and attached to [DATN-92](https://trankimthang0207.atlassian.net/browse/DATN-92); visible date 2026-10-16, 10:51 ICT. No original-message permalink is available in the artifacts inspected.
- **Verbatim:** “Anh duyệt nhé. Em cập nhật phê duyệt vào Jira và contract rồi triển khai DATN-266–271 theo kế hoạch. Cuối cùng review findings, fix, kiểm thử và gom vào một PR backend nhé.”
- **Scope:** permission to record the approval, update Jira and contract, proceed with DATN-266–271 according to the plan after dependencies/gates, review/fix/test findings, and consolidate work in one Backend PR. Current execution instructions further require re-review, one final Backend PR, no auto-merge, and no runtime writes before Gate C.
- **Limit:** this 10:51 statement authorizes the project workflow; it does not by itself decide detailed C-07 policy or replace IAM/Security, DB, API/Gateway, or Audit/Security review.

### C-07 decision approval

- **Approver:** KeyT; requester confirms Jira records KeyT as DATN Project Owner. The 11:17 approval is within the presented DATN-92 proposal scope; it does not prove delegation for every specialist domain.
- **Evidence:** proposal screenshot shown immediately before the reply; screenshot attached to Jira as `codex-clipboard-ef0729a5-65ec-40b9-984e-39245f868252.png`; direct reply visible at 11:17 ICT on 2026-10-16. Jira links to the original comments are on DATN-92; no separate chat permalink was available.
- **Verbatim:** “Anh duyệt TQ-05, TQ-06, membership lifecycle và TQ-07/08 theo đề xuất. TQ-09 chỉ áp dụng nếu C-04 đã được phê duyệt và còn hiệu lực; ghi link quyết định vào Jira. Anh đồng ý audit cùng transaction và rollback nếu ghi audit thất bại. Retention chưa chốt: đừng tự đặt thời hạn; xác nhận với owner Audit/Security. Schema/migration theo DB workflow riêng, cần DB owner review. Cập nhật các quyết định đã duyệt vào Jira và versioned contract. Chỉ bắt đầu phần implementation sau khi các dependencies còn mở được chốt và Gate A/B đạt yêu cầu.”
- **Accurate scope:** TQ-05 direction; TQ-06 generation/fencing direction; duplicate add `409`; repeated remove `204`; rejoin after explicit removal new ID/new `joinedAt`; POST/DELETE-only and GET out of DATN-92; TQ-09 conditional; TQ-10 atomic audit/rollback. Exact permission/provisioning, generation fields/writers/fences, API response/error details, audit map/retention, DB migrations, and runtime gates remain separate decisions/evidence.

## 2. F-01 — approval/contract lifecycle mismatch

**Finding:** F-01, P2 — contract/approval-record correctness.
**Source:** earlier approval summary and older C-07 drafts stated that explicit rejoin after removal reused the same Membership ID.
**Evidence:** the proposal screenshot presented to KeyT at 11:15 says “rejoin tạo membership ID mới”; KeyT's 11:17 reply approves the membership lifecycle “theo đề xuất”. No authorized amendment changing that rule was found in the available Jira/conversation evidence. The same-ID statement was an engineering transcription based on Project Membership same-row reactivation, not an approver amendment.

**Correction:** explicit removal followed by rejoin creates a **new Membership ID and a new `joinedAt`**. Old approval comments and uploaded historical files remain unchanged; the correction comment and v0.2/v0.5/v0.6-correction artifacts attached to Jira supersede only the incorrect lifecycle sentence. The correction did not approve rejoin HTTP status, storage/index design, stale-generation row identity, or audit events.

**Fix verification:** compare original proposal → KeyT 11:17 reply → later engineering summary; check that this canonical package asserts ID2 != ID1, new timestamp, no old-row reactivation; inspect OpenAPI/contract/test plan and DB design for no identity-preserving rejoin. The old same-ID language is retained only in historical sources and explicitly marked superseded. No production source/schema was changed to fix this document finding.

**Affected lifecycle cases:** first add; active duplicate `409`; remove ID1; repeat remove `204`; explicit rejoin creates ID2 != ID1 and new `joinedAt`; active-only uniqueness permits retained history; parent-generation stale admission cannot revive; audit correlates old removal/new admission while event details remain pending Audit/Security approval. See [Security/Test Plan](DATN-92-Security-Test-Review-Plan.md#2-approved-lifecycle-regression-cases).

## 3. Additional documentation consistency findings

| ID / severity | Evidence and root cause | Correction in this package | Verification/status |
|---|---|---|---|
| F-02 / P2 — Permission identifier drift | Current BE Team Foundation authorization checks `team:children.manage`; established permission names elsewhere use dot style (`project.*`, `team.read`) and prior C-04 proposal uses `team.children.manage`. No Team-member action permission is provisioned. Code convention and proposal drift were conflated. | Recommend separate `team.members.add`/`team.members.remove`, dot style, no colon alias, while preserving/reconciling Foundation permission separately. Mark exact IDs/provisioning awaiting IAM/Security. | Verified by source scan at BE `3b83919`; contract/OpenAPI/readiness use one stated proposal and no implementation is claimed. Open until IAM decision. |
| F-03 / P1 — Approved new ID incompatible with declared uniqueness | [Team schema](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts) lacks status/history/generations; [persistence](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/infrastructure/persistence.ts) declares unique `(teamId,userId)`. That cannot retain ID1 and insert ID2 for the same pair. | Corrected DB proposal uses distinct admission rows and recommends partial uniqueness for active pair, with deployment/index/migration proof required. | Verified schema/index facts at BE `3b83919`; no production migration changed. Blocks DB/BE implementation. |
| F-04 / P2 — GET scope leakage | Older BE shared OpenAPI includes Team membership GET while KeyT approved only POST/DELETE in DATN-92. Deleting the shared operation would alter another contract unilaterally. | C-07 OpenAPI contains only POST/DELETE; README/API contract explicitly exclude GET from DATN-92 and require independent disposition of the shared draft. | JSON path set checked during PR validation; no shared BE OpenAPI file changed. |
| F-05 / P1 — TQ-09 authority conditionality lost in some proposal summaries | C-04 §10.1 records TQ-09 semantics approved but later Jira review questions whether the table is owner-authorized; KeyT explicitly conditions applicability. | Matrix separates R0 authority, conditional contract semantics, and Gate C runtime evidence. One short C-04 owner decision is requested. | Local documents and Jira disposition summarized; exact authorized owner/evidence still unresolved. |
| F-06 / P1 — Audit duration example could be mistaken for policy | Workspace audit schema contains an example retention value; no authoritative Team duration/archival policy was found. | No duration chosen; request Audit/Security source/revision or explicit selection; retention remains deferred. | Canonical audit docs and DEC-AUD-01/DEC-OUT-02 are non-binding for Team retention; owner confirmation outstanding. |

F-02/F-05/F-06 are documentation/contract findings, not confirmed production vulnerabilities. Do not claim a security defect in production code without a code-path finding and independent proof.

## 4. Evidence provenance and retained history

- Jira parent: [DATN-92](https://trankimthang0207.atlassian.net/browse/DATN-92); subtasks DATN-266–271.
- KeyT approval screenshots and correction comment are attached or recorded on the Jira issue. Original same-ID comment is not erased; it is superseded only by the traceable correction.
- Historical package files `C-07-Team-Membership-v0.5-draft`, `C-07-Team-Membership-v0.6-draft-correction`, Approval Addendum, Matrix v0.4/v0.5, test/readiness corrections, and F-01 correction records remain historical evidence. This canonical directory does not copy those into another folder.
- C-04 source: [DATN-89](https://trankimthang0207.atlassian.net/browse/DATN-89) and [decision-gap report](../09-team-management-foundation-decision-gap-report.md). Its R0 conflict is preserved rather than silently resolved.
- BE evidence is pinned to `3b839198cfcbc40d6b11e1167ae8c68c54afea99`; it is a read-only technical snapshot, not current deployed-index or external-writer proof. Review relevant [Team authorization](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/application/teams/team-authorization.policy.ts), [User status writer](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/infrastructure/mongodb/user-directory.repository.ts), [Organization Membership writer](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/infrastructure/mongodb/organization-membership-command.repository.ts), and [Project Access writer](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/infrastructure/mongodb/project-access.repository.ts).

## 5. Reviewer checklist

- [ ] KeyT approval scope matches the 11:17 source; no unapproved details labeled approved.
- [ ] F-01 correction and the new-ID/new-`joinedAt` lifecycle appear consistently across contract, API, tests, DB design, and findings.
- [ ] Historical Jira comments are preserved and the correcting record is linked.
- [ ] R0 and TQ-09 conditionality remain explicit.
- [ ] IAM, API/Gateway, DB/domain, and Audit/Security owners are assigned by role; no names or authority are fabricated.
- [ ] GET is absent from C-07 OpenAPI but its shared-contract disposition is not silently changed.
- [ ] No retention duration is selected from an example.
- [ ] No production schema, implementation, Jira status, or runtime gate is claimed changed.
- [ ] Draft PR is not represented as approval or Gate A/B/C evidence.
