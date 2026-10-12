# DATN-93 — Acceptance và phản hồi review R5

**Trạng thái:** Document review checklist + future scenarios, 12/10/2026.
Không phải passing application tests, product approval hay implemented Task.

Nguồn: [working contract R5](13-task-v1-contract-readiness.md),
[worksheet R1](14-task-v1-review-worksheet.md),
[Jira DATN-93](https://trankimthang0207.atlassian.net/browse/DATN-93) và
[review R4](https://github.com/DATN-SPRING2027/Document/pull/22#pullrequestreview-5410654477).

## 1. Review nói gì, R5 xử lý phần nào

Review R4 ghi **No findings**, Comment, không Request Changes/Approval.
Nội dung review là inventory các quyết định còn thiếu và tracking chưa cập
nhật, không phê duyệt actor/state/field/API. User yêu cầu xem review và sửa
ngày 12/10. R5 cụ thể hóa proposal và cách reviewer ghi quyết định; không
claim đã sửa một bug runtime hoặc đã đóng Q1–Q9 bằng review này.

| Review item | R5 artifact chuẩn bị | Decision/readiness còn mở |
|---|---|---|
| DATN-105: scope Q1 | Worksheet §1: 11 UC + Kanban/subtask; included/deferred/excluded candidate và exclusions có authority | Exact release scope + accepted actor/ACL |
| DATN-106: boundary/Q9 | Worksheet §2: canonical/repo/process/BFF/storage/consumer boundary | Exact runtime/config + deployment guide reconciliation |
| DATN-107: Q2/Q3 | Worksheet §3: candidate dictionary, required/default/ownership và reference checklist | Field types/nullability/limits/cardinality/index rationale |
| DATN-108: Q4/Q7 | Worksheet §4: five proposed states, 25 accepted cells UNKNOWN, per-edge review/replay | Enabled edges/actor/reason/version/conflict/retry |
| DATN-109: Q2/Q5 | Worksheet §5: baseline guards + action/member/Leader/successor proposal, admin/Agent limits | Exact permission/scope/resource/Team matrix |
| DATN-110: Q6–Q9 | Worksheet §6: seven operation surfaces, failure classes/history/delivery/runtime | Exact paths/DTO/errors/event/sink/consumer/trust/config |
| Subtask progress 0% | Worksheet §7: work progress, product decision và implementation gate riêng | User đổi Jira theo deliverable; chưa claim status đã đổi |

## 2. Contract scenarios — expected decision cần có

Các TV dưới là review obligations. `PASS` cho kiểm tra file/link/coverage
không làm TV thành tests passing. Proposal-dependent scenario chỉ được
enable sau accepted decision tương ứng; không test một enum/edge còn UNKNOWN
như thể policy đã tồn tại. AT-01–09 trong working contract vẫn giữ ID.

| ID | Review scenario | Expected boundary / answer cần ghi | Mapping |
|---|---|---|---|
| TV-01 | Anonymous hoặc expired session đọc/ghi Task | Protected content không được trả; exact API error/refresh còn cần chốt | 109/110, Q5/Q6, AT-01 |
| TV-02 | ACTIVE role assignment nhưng không ACTIVE OrganizationMembership | Không thiết lập scope access chỉ từ role; error precedence cần Q6 | 109/110, B8, AT-01 |
| TV-03 | Client đoán Organization/Project/Team/task ID | Validate actual parent scope/ACL; concealment policy chưa tự chọn | 107/109/110, Q2/Q5/Q6 |
| TV-04 | PUBLIC Project metadata hoặc ADMIN/platform actor đọc confidential Task | Không implicit content grant; riêng scoped evidence/ACL cần Q5 | 109, B8/B10, AT-02 |
| TV-05 | Project creator tạo/sửa Task khi API có mặt | Giữ ordinary MEMBER rights B9; exact resource/field/Team ceiling cần Q5 | 105/109, AT-02 |
| TV-06 | Member tạo Task với assignee người khác | Accepted allow/deny/self-assignment/default cần ghi, không suy ra từ proposal | 105/107/109, Q1/Q2/Q5 |
| TV-07 | Creator và assignee là hai User khác nhau | Field edit matrix và current-membership guards cần accepted answer | 107/109, Q3/Q5 |
| TV-08 | Team Leader có scope ở sibling Team hoặc Project | Chốt đúng assignment representation/ceiling; role name không cấp quyền toàn Project | 109, Q2/Q5 |
| TV-09 | Suspend/remove/ProjectMembership INACTIVE khi Task đang assign | Deny effective access theo baseline; transfer/unassign/retained data cần Task decision riêng | 107/109, Q2/Q5/Q7 |
| TV-10 | Work Note không taskId hoặc link Task ngoài scope | Giữ optional link B5; cardinality/reference/null/error details cần chốt | 107/110, Q2/Q6, AT-06 |
| TV-11 | DONE/CANCELLED Task được chọn vào Handover | Eligible state/source-projection policy cần Q4; không tự bật proposal | 105/108, Q1/Q4, AT-04 |
| TV-12 | Tất cả 25 from/to pairs, gồm same-state | Mỗi enabled/denied/no-op cell có decision; không edge ngầm định | 108, Q4/Q5/Q7, AT-07 |
| TV-13 | Cancel/reopen không reason hoặc actor không eligible | Required reason/actor/edge và error cần accepted answer | 108/109/110, Q4/Q5/Q6 |
| TV-14 | Duplicate op, mismatch payload hoặc stale version | Replay/conflict/retry deterministic; key/version specifics cần Q7 | 108/110, AT-04/07 |
| TV-15 | Membership/permission bị revoke giữa authorize và write | Revalidate/fence semantics phải accepted; không stale-authority write | 109/110, Q5/Q7 |
| TV-16 | Failure sau Task write trước history write | B4: cùng commit hoặc rollback; isolated replica-set proof ở DATN-95 | 106/110, Q7/Q8, AT-03 |
| TV-17 | Handover failure giữa hai services và retry | API operation ID/recovery; không direct DB hoặc shared transaction assumption | 106/110, Q7, AT-04 |
| TV-18 | Agent proposal chưa human confirm hoặc context ngoài scope | Không mutate; context ACL và safe provenance B7 | 105/109/110, Q1/Q5/Q8, AT-05 |
| TV-19 | Task history/body/filter trả content người đọc mất quyền | Current Task ACL + safe projection; exact order/paging/retention cần Q8 | 109/110, AT-01/02 |
| TV-20 | Optional async consumer/outbox delivery hoặc replay | Chỉ nếu Q9 chọn; same transaction + after-commit relay + event-ID dedup B4 | 106/110, Q8/Q9, AT-09 |
| TV-21 | Client update server-owned fields hoặc unbounded list/search | Input allowlist/bounds cần contract; không mass assignment hoặc unrestricted scan | 107/110, Q3/Q6 |
| TV-22 | Task upstream down, config sai, direct browser-container request | BFF/Gateway boundary/fail-fast; exact errors/health/timeouts cần Q6/Q9 | 106/110, AT-08 |

## 3. AC và downstream closure

| Jira acceptance | Artifact để reviewer kiểm tra | Giới hạn |
|---|---|---|
| AC1: authoritative decisions tách research/inference | R5 S/B map; worksheet từng section có APPROVED vs PROPOSED label | Comment/no findings và report merge không approve proposal |
| AC2: fields/transitions/API/authorization/audit explicit hoặc UNKNOWN có named questions | Q1–Q9 + worksheet dictionary/matrices/operation/failure tables | Named personal approvers chưa xác nhận; ghi required authority roles |
| AC3: downstream chỉ approved behavior, acceptance traceable | TV-01–22 → Q/subtask/AT; R5 DATN-94/95/96 gates | Các TV là future scenarios, không runtime/test evidence |

Expected result cung cấp là **precise blocker list với proposal review cụ thể**.
Team nghiệm thu phần tài liệu và user cập nhật tracking riêng; full Task V1
implementation contract vẫn cần accepted record theo từng item.

- DATN-94: cần accepted state/edge/actor/version/replay và error/event contract
  tương ứng; worksheet không enable 25 cells hoặc authorize tests cho proposal.
- DATN-95: cần accepted data dictionary/relationships/query-index rationale,
  history/mutation shape và canonical persistence authority; không init/migrate
  continuum_task từ report. Atomic mutation/history B4 giữ nguyên.
- DATN-96: cần approved operation paths/trusted context/error/health/config/
  timeout/runtime values và guide reconciliation; không port/queue fallback.

Reviewer phải chỉ rõ item accepted/partial/deferred, owning revision, approver,
ngày và scenarios tương ứng. Chỉ kiểm tra docs/file coverage không chứng minh
service startup, access enforcement, transaction, retries hoặc integration.
