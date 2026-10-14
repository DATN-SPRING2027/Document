# DATN-95 — P1–P3 approval and scoped D-03 readiness

- **Decision status:** APPROVED — P1, P2 and P3 for the private D-03 slice only.
- **Confirmation recorded:** 14/10/2026, Asia/Bangkok. The date of the original Leader message was not supplied; this is the requester's confirmation date, not a fabricated original decision timestamp.
- **Approver:** Trần Kim Thắng, Leader, as established by [Member.md](../../Member.md) and the [PR #30 approval record](20-task-v1-contract-approval-record.md).
- **Evidence channel:** requester-relayed Leader approval in this conversation. The requester supplied the Leader's recommendation/review and then explicitly clarified: “leader tôi nhắn như trên là duyệt tất cả nội dung với toàn bộ p trên”. This clarification establishes approval of all P rows, rather than treating “nên duyệt” alone as approval.
- **Approved source:** [contract delta at immutable revision 6628c60ed5b259ae8c368883c8619543919aaf20](https://github.com/DATN-SPRING2027/Document/blob/6628c60ed5b259ae8c368883c8619543919aaf20/research-docs/Internal-Work-Management/21-task-v1-d03-contract-delta.md), delivered in [PR #31](https://github.com/DATN-SPRING2027/Document/pull/31).
- **Recorder:** Codex. This records the human decision relayed by the requester; it is not an AI product approval, an independent review, or a GitHub APPROVED review. PR #31 was OPEN with no submitted reviews at this recheck.

## 1. Scope and authority

Preserve all recommendation-level decisions in PR #30: exactly one owning Project, contextual Organization, 0..1 Team/assignee, non-unique title, default unique _id, append-only history, atomic Task/history persistence and conditional outbox deferral. This record closes only the additional P1–P3 semantics at the exact revision above. The earlier proposal and approval records remain historical evidence.

For the selected slice, read the approved delta's §4–11 as the scoped field/history/use-case specification and engineering/test design. Its pending P labels are superseded by this record, not by an assumed approval of older research schemas, the complete Task V1 API, or all future mutations. Ordinary technical designs remain subject to implementation review and evidence.

| Item | Decision and exact scope | Acceptance / oracle mapping |
|---|---|---|
| P1 | **APPROVED.** Private, human-origin create/read persistence primitives, Task/history definitions, repeatable disposable initialization and tests. Creation is the only mutation. No status/default, edit, assignment, search API, HTTP/Redis handler, production caller or integration is introduced. This limits D-03 implementation, not eventual Task V1. | AC1/AC2; O1/O2/O6/O13 and applicable AC3 tests. |
| P2 | **APPROVED as written.** Exactly seven required/non-null persisted fields: _id, projectId, title, createdBy, createdAt, updatedAt, version. Server constructs trusted metadata; it is not required user input. Title preserves its original string, has a code point outside §5's W set, is non-unique and has no business length cap in this slice. Existing BSON size limits apply. Creation has updatedAt = createdAt and version = 1; no public CAS/ETag semantics. | AC1 and relevant AC2; O2–O6, O13. |
| P3 | **APPROVED with the clarification in §2.** Exactly one creation event per successfully committed Task version 1, using §8's identifiers, actor/source, timestamp, operation/correlation and changed-field-name projection. No content snapshots/title values/prompts/credentials/profile copies. Task/event writes are atomic; history remains append-only. | AC2; O2/O5/O7–O11 and applicable AC3 tests. |

The B designs in §5–11 define the implementation/test basis: ObjectId/BSON Date representation, derived Organization context, trusted scoped adapter, original-input/DB validation, query-driven indexes, transaction/uncertainty handling, restricted history privileges and executable oracles. No additional product decision is needed merely to encode the approved semantics. Do not claim actual query performance or executed test results from these designs.

## 2. P3 clarification: confirmed rejection/abort versus uncertainty

The sentence “Failed creation writes no successful mutation-history record” must be read with §9/O10, not as a guarantee from every error response:

- Creation rejected before writes, or a transaction confirmed aborted, commits no new Task/creation event from that attempt.
- A confirmed successful commit contains the matching Task and event together.
- If commit remains ambiguous, the internal result is **UNCERTAIN**. The pair may already have committed together. An exception alone proves neither failure nor rollback, and is not permission to issue a second create with fresh identifiers.
- Follow §9's stable IDs, reconciliation and persisted-state oracles. A single absent read does not establish that an in-flight commit can never finish.

This is the Leader's requested clarification of the existing design, not a new publication, HTTP failure, idempotency or rollback policy. It governs P3 and its summaries and test fixtures wherever they use the word “failure”.

## 3. P2 clarification: exact title predicate is accepted

The requester confirmed approval of all P content after supplying the Leader's explicit U+200B observation. Record P2 unchanged: W is exactly the set in the approved §5; U+200B is outside W, so a title containing only U+200B is valid under this predicate. No “visibly rendered text” requirement is introduced. Tests must include this accepted case, plus the existing empty/all-W/Vietnamese/mixed cases, at application and DB boundaries.

Do not silently add U+200B or other invisible code points to W, normalize/trim stored content, or add a business cap. A later visible-content or public-input policy requires an explicit change to the owning contract and compatible validation/tests.

## 4. Readiness and completion remain separate

**A — READY FOR D-03 IMPLEMENTATION**, limited to P1's private data-foundation slice using P2/P3 and the defined B designs. The selected slice now has accepted data semantics and testable oracles; all 25 D-02 transition cells are not a prerequisite for this status-free slice.

Before source edits, refresh the owning source/contracts, reconcile the relevant BE guide with accepted ADR-010 and follow the separate DB/BE delivery gates. No production caller, Task-service activation, shared/live database provisioning or data cutover is enabled by this record. Later lifecycle introduction requires its own approved initial-state/transition contract and migration for existing base records.

O1–O13 remain **test specifications, NOT RUN**. Implementation, review and actual passing checks are the completion gate. O11's DB-privilege proof requires an authentication-enabled disposable MongoDB replica set; if unavailable, report that check **BLOCKED**, never PASS. An ordinary unauthenticated transaction test cannot prove update/delete privilege denial.

Outbox and retention remain deferred; Task history is not a delivery queue. Full API/permission/idempotency, lifecycle, assignment/eligibility, D-04 runtime and measured-workload claims remain with their owning follow-ups. This does not reopen the approved Organization Membership contract now on main or imply its remaining readiness gates are complete.

## 5. Delivery, Jira and work record

This is a documentation-only continuation of open PR #31, not a new implementation task. The existing task branch was originally created from main at 69c1644. Main was refreshed and inspected at ddce1b231f44c25b42b75626046af533bb05153d; its intervening PR #27 adds Organization Membership documentation, not a Task delta approval. No merge/rebase or application/source-baseline change is needed to record this confirmation.

Write scope: this new record, a successor/readiness note in the delta, and its README link. Keep PR #30's record and the immutable approved revision intact. No code, schema, migration, DB, FE or SAGE selector changes. Review the final documentation diff using the local review-agent workflow; disclose self-review and run document/link/table/diff checks. No application test result is claimed.

Jira DATN-95 should record the approval source/revision, closed P1–P3 product blockers, `READY FOR D-03 IMPLEMENTATION`, and the unexecuted test/completion gates. Do not mark the parent or all of Task V1 Done. DATN-116's ownership completion is preserved; DATN-117–120 can remain In Review while the documentation delivery is reviewed, and DATN-121 stays To Do until implementation begins. Record actual verified tracking separately from these instructions. No new team message, GitHub review approval or merge is authorized by the product decision.
