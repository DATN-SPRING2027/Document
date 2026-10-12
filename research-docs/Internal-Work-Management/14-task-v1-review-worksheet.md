# DATN-93 — Worksheet review Task V1 theo DATN-105–110

**Trạng thái:** PROPOSED review package; chưa phải approved Task implementation contract.
**Revision:** R1, 12/10/2026 (Asia/Saigon). **Owner tổng hợp:** Nguyen Hong Phuc.

Worksheet cụ thể hóa các gaps trong [working contract R5](13-task-v1-contract-readiness.md)
để reviewer trả lời từng item. [Review PR #22](https://github.com/DATN-SPRING2027/Document/pull/22#pullrequestreview-5410654477)
ghi **No findings**, dạng Comment; đó không phải Approval hay quyết định product.
Các bảng dưới có đề nghị rõ ràng nhưng **accepted answer vẫn UNKNOWN** ở mức
chi tiết, trừ các baseline được chỉ nguồn riêng. Không provision, tạo fixture,
enable endpoint hoặc transition từ các candidate này.

Nguồn owning: [Task Use Cases](12-continuum-task-management-use-cases.md) (S3),
[Task storage proposal](../../database-design/12_TASK_MANAGEMENT_SCHEMA.md) (S4),
[Task permission proposal](../02_ACTORS_ROLES_AND_PERMISSIONS.md) (S5),
[ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md) (S1),
[ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md) (S2).
B1–B10 và Q1–Q9 giữ ID của working contract; không tạo một bộ authority khác.

## 1. DATN-105 — V1 làm gì, không làm gì, ai dùng

**PROPOSED SCOPE**, tổng hợp S3 mục 3–7. Reviewer ghi `included`, `deferred`
hoặc `excluded` cho từng dòng, không chỉ duyệt chung câu “Task V1”. Đề nghị
review nhóm core cùng nhau vì update/assignment/lifecycle/history ảnh hưởng
data và API ngay từ đầu; lịch triển khai từng slice không tự thay release scope.

| ID | Use case | Đề nghị để review | Accepted scope |
|---|---|---|---|
| UC-TM-01 | List Task | Included, scoped list | UNKNOWN Q1 |
| UC-TM-02 | Create Task | Included, một đơn vị công việc đơn giản | UNKNOWN Q1 |
| UC-TM-03 | View Task detail | Included, chỉ projection được quyền xem | UNKNOWN Q1 |
| UC-TM-04 | Update Task | Included, allowlist field; không generic status/assignee PATCH | UNKNOWN Q1/Q3/Q5 |
| UC-TM-05 | Assign/reassign Task | Included, command riêng trong scope | UNKNOWN Q1/Q2/Q5 |
| UC-TM-06 | Change status | Included, fixed lifecycle được duyệt | UNKNOWN Q1/Q4/Q5 |
| UC-TM-07 | Basic search/filter | Included trong list; bounds cần chốt | UNKNOWN Q1/Q6 |
| UC-TM-08 | Optional Work Note link | Included; B5 đã chốt optional logical link, cardinality/DTO còn mở | UNKNOWN detailed Q1/Q2/Q6 |
| UC-TM-09 | Handover open tasks | Included; B6 đã chốt Team Leader/Task API boundary, eligible states còn mở | UNKNOWN detailed Q1/Q4/Q7 |
| UC-TM-10 | View history | Included, scoped read-only history | UNKNOWN Q1/Q5/Q8 |
| UC-TM-11 | Agent rewrite proposal | Deferred đến khi core/ACL có contract; B7 vẫn áp dụng nếu bật | UNKNOWN release Q1 |
| P1-KANBAN | Fixed-column board | Deferred; thay đổi demo scope cần quyết định riêng | UNKNOWN Q1 |
| P1-SUBTASK | Subtask một cấp | Deferred; không nhầm với subtasks Jira của team | UNKNOWN Q1 |

**APPROVED EXCLUSIONS:** Jira canonical/import/sync/two-way writes (B1),
Task record thành standalone SAG source (B5), Agent tự ghi Task hoặc bypass
human confirmation (B7), repo ManageWork/cluster Mongo mới (B2).

**PROPOSED EXCLUSIONS/DEFERRALS, chưa accepted:** Scrum/sprint/estimate;
Epic/Story/Bug/version; workflow editor; Task comment/file/mention/watcher;
time tracking; JQL/shared filters; dependency graph; automation/notification
builder; dashboard/report; bulk operations; hard delete/archive/retention
feature. Nguồn S3 mục 4; từng nhóm vẫn cần Q1, không suy ra release exclusion
từ một chức năng tương tự của Jira. Work Note/evidence không tự cấp Task ACL.

## 2. DATN-106 — ownership và service boundary

| Concern | Accepted constraint | Còn phải chốt |
|---|---|---|
| Canonical Task | Continuum Task API + MongoDB, B1 | Exact fields/DTO, Q2/Q3/Q6 |
| Source/runtime | Existing DATN-BE, independent NestJS process; UI DATN-FE, B2 | Entry/config/health values và guide reconciliation, Q9/DATN-96 |
| Browser | Existing BFF → Gateway → Task, B3 | Paths/trusted identity/errors/timeouts, Q6/Q9 |
| Storage | Target continuum_task; tasks + append-only task_events; atomic mutation/history, B4 | Approved persistence shape/indexes, Q3/Q7/Q8 và canonical ADR/SPEC |
| Capture/Handover | API/contract + logical task reference, B5/B6 | Cardinality/eligibility/recovery, Q2/Q7 |
| Agent/events | Authenticated API; human-confirmed mutation; conditional transactional outbox, B4/B7 | Feature scope, consumer/event/delivery details, Q1/Q8/Q9 |

Không hỏi duyệt lại boundary đã accepted chỉ vì Task chưa có runtime. Không
copy field/status từ IAM, dùng shared continuum_db fallback, hoặc truy cập
chéo collections để né API. Port `3009`/queue names vẫn proposal của ADR-010.

## 3. DATN-107 — data dictionary và reference review

**PROPOSED DATA**, từ S3 Field tối thiểu/mục 7 và S4 mục 3. Đây là candidate
contract dictionary, không phải schema/OpenAPI đã duyệt. Required/default ở
cột giữa cũng là proposal. Type/limit/null/normalization chưa có owning answer
phải được ghi rõ; không tự đặt title length hay enum mới để lấp ô trống.

| Candidate field | Proposal để review | Exact accepted detail còn thiếu |
|---|---|---|
| id/_id | Mongo ObjectId canonical; API string representation là candidate | Q3: API name/format, validation; chưa có key/sequence contract |
| organizationId | Required scope; server kiểm tra trusted context | Q2/Q3/Q6: representation và client/server ownership |
| projectId | Required, đúng một Project thuộc Organization | Q2/Q3: cardinality, reference/state eligibility |
| teamId | Optional, tối đa một Team trong Project | Q2/Q3/Q5: null/absent, teamless access, reassignment |
| title | Required string, editable | Q3: trim/empty/length/encoding limits |
| description | Optional string, editable | Q3/Q5: null/clear, format/size, visible content |
| createdBy | Required authenticated user; server-owned | Q3/Q6: representation và attribution/trusted caller |
| assigneeId | Optional; Member tự gán/để trống, Leader gán người khác | Q2/Q5: eligible target/unassign/cross-scope rules |
| status | Server initial TODO, approved command sau đó | Q3/Q4: accepted enum/default và writable operations |
| priority | LOW/MEDIUM/HIGH; server default MEDIUM | Q3: accepted enum/default/editability |
| type | Chỉ TASK | Q1/Q3: có persist/expose field hay implied single type |
| dueDate | Optional, editable | Q3: date-only/timestamp, timezone, past date, null/clear |
| createdAt/updatedAt | Server timestamps | Q3/Q6: exact representation, clock semantics |
| version | Server mutation version | Q3/Q7: type/initial value/CAS/token/ETag semantics |

Reference review phải đóng riêng: Organization/Project/Team parent IDs; assignee
User và membership eligibility; Work Note 0..1 Task / Task 0..N notes proposal;
successor eligibility/access lifetime; xử lý suspended/removed/archived targets.
Không suy ra cascade delete/transfer hoặc restore quyền từ stored RoleAssignment.
Các quyết định Organization Membership đã nhận có scope Organization; chúng
không tự chọn Task assignee transfer, Team rules hay permission matrix.

## 4. DATN-108 — lifecycle và concurrency review

**PROPOSED STATES:** TODO, IN_PROGRESS, BLOCKED, DONE, CANCELLED; initial TODO,
DONE reopen → IN_PROGRESS có reason, CANCELLED terminal theo S3/S4. Knowledge
verification tiếp tục là lifecycle khác. S3 mục 7 đề nghị DONE không cần Work
Note/evidence và chỉ TODO/IN_PROGRESS/BLOCKED vào Handover assignment; cả hai
rule chi tiết vẫn cần Q4, không suy ra từ optional link hoặc từ B5.

**Accepted transition matrix: tất cả 25 cells vẫn UNKNOWN (Q4/Q5/Q7).**
Same-state cells cũng cần no-op/conflict/replay decision; không tự xem là allowed.

| From → To | TODO | IN_PROGRESS | BLOCKED | DONE | CANCELLED |
|---|---|---|---|---|---|
| TODO | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| IN_PROGRESS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| BLOCKED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| DONE | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| CANCELLED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

| Review item | Proposal/evidence | Exact decision cần ghi |
|---|---|---|
| Initial state/creation | TODO proposal, S3/S4 | Confirm initial state và create/history behavior |
| Ordinary transitions | Current assignee hoặc scoped Leader proposal, S3 | Mỗi from/to edge, actor/guard/reason, invalid result |
| Cancel | Scoped TEAM_LEADER proposal, S5 | Eligible source states, reason, terminal/replay outcomes |
| Reopen | DONE → IN_PROGRESS + reason proposal, S3/S5 | Actor, validation, concurrency và event |
| Retention | Không hard delete Task proposal, S3 | Approved cancellation/read visibility/retention |
| Stale/replay | B6 operation ID + B7 version provenance accepted intent | Q7: key scope/expiry, payload mismatch, CAS/replay response |

Cho **mỗi enabled edge** cần: from/to + command, authenticated actor, scope/ACL,
target eligibility, reason, version precondition, safe event và success/denial/
conflict/retry outputs. B4 đã chốt task + history atomic; phần cần quyết định
là representation/failure outputs, không hỏi có giữ atomic history hay không.

## 5. DATN-109 — ai được thao tác Task

**APPROVED GUARDS:** authenticated identity, ACTIVE OrganizationMembership,
scoped authority và resource ACL (B8); Project-scoped access cần ACTIVE
ProjectMembership (B10). Project PUBLIC metadata không cấp Task content access.
ADMIN/platform authority không tự cấp quyền đọc confidential Task. Creator
bootstrap ordinary MEMBER có documented create/edit rights khi API tồn tại
(B9); resource/field/Team limits còn Q2/Q3/Q5.

**PROPOSED ACTION MATRIX**, S3/S5; không phải grants, Role seed hay capability
response. Tất cả cells chi tiết dưới cần Q5 sign-off; role name không đủ.

| Action | MEMBER proposal | Scoped TEAM_LEADER proposal | SUCCESSOR assignment proposal |
|---|---|---|---|
| List/view/search | Trong scope/ACL | Trong assigned scope/ACL | Task được bàn giao và ACL cho phép |
| Create | Trong scope; unassigned hoặc self-assigned | Trong assigned scope; target eligible | Assignment không tự cấp create; rule UNKNOWN |
| Update fields | Creator hoặc current assignee; allowlist | Trong assigned scope; allowlist | Rule theo assignee + membership nếu accepted; assignment riêng không đủ |
| Assign/reassign | Không gán người khác; self-assign lúc create | Gán eligible target trong scope | Assignment không tự cấp reassign |
| Change status | Current assignee + enabled edge | Assigned scope + enabled edge | Nếu là assignee eligible, rule cần Q5; không mặc định cho phép |
| Cancel | Không cấp từ ordinary Member proposal | Assigned scope, source states/reason cần chốt | Assignment không tự cấp cancel |
| View history | Task hiện được phép đọc | Task hiện được phép đọc | Task được giao, projection/ACL cần chốt |

ADMIN hoặc PLATFORM_OPERATOR chỉ có management authority chưa đủ để điền
ALLOW cho bảng này. Nếu actor đồng thời có một assignment/member permission
hợp lệ, đánh giá evidence đó theo Q5; không blanket deny mọi operation của họ
chỉ vì mang role quản trị. Agent không có mutation grant độc lập: B7 yêu cầu
permitted human confirmation, không tạo AI bypass cho assign/status/ACL.

Permission-code candidates từ S5: task.create, task.read, task.update_own,
task.status.change, task.assign, task.cancel, task.history.read. Các code chưa
accepted, không seed hoặc tái dùng Project permission như Task permission.
Chốt thêm Team-level Leader vs Project-level Leader, teamless Task, creator vs
assignee rights và reauthorization khi membership/permission đổi trong mutation.

## 6. DATN-110 — API, errors, history và runtime review

**PROPOSED OPERATION DESIGN**, author đề nghị command riêng để giảm mass
assignment; không có accepted Task method/path/DTO trong OpenAPI hiện tại.
Đường dẫn phải được API owner chốt cho Gateway/BFF và internal service; bảng
này cố ý không gán candidate path thành route đang tồn tại.

| Operation | Request candidate | Response candidate | Cần chốt ngoài Q1/Q5 |
|---|---|---|---|
| Create | title, optional description/teamId/assigneeId/dueDate/priority; project/context selectors cần chốt | Task projection + server id/version | Q2/Q3/Q6: required/nullable/limits, actor attribution, success status |
| List/search | Project/scope, status/assignee/priority/due-date/title filters proposal | Bounded list projection + paging metadata | Q6: method/path, accepted filters, sort, cursor/page, limits/totals |
| Detail | Task identifier + trusted context | Authorized Task projection | Q6: path/ID shape, visibility, missing vs inaccessible |
| Update | Allowlisted editable fields + version precondition | Current authorized projection/version | Q3/Q6/Q7: partial/null semantics, mass-assignment denial, stale result |
| Assign/reassign | Task ID + target/unassign selector + operation ID | Canonical assignment/version | Q2/Q6/Q7: target eligibility, null/replay/mismatch/recovery |
| Transition/cancel/reopen | Task ID + target command/state + reason + version | Resulting authorized state/version | Q4/Q6/Q7: edges/reason/status/conflict/retry outputs |
| History | Task ID + history page/order selector | Safe authorized event projection | Q6/Q8: field shape, pagination/order/retention/redaction |

Server-owned scope/creator/time/version/status fields không được nhận bằng
generic update chỉ vì có trong Task response candidate. Status/assignment đi
qua operation được duyệt; actor/context provenance phải đến từ authenticated
contract, không tin identity do client tự gửi.

| Failure class | Contract answer còn UNKNOWN | Review case |
|---|---|---|
| Unauthenticated/expired session | Task-facing status/body/refresh contract Q6 | Không đọc/ghi protected Task; không lộ token |
| Inactive membership/cross-scope/ACL deny | Q5/Q6: precedence + concealment | Role/client ID không thay membership; không leak existence/content |
| Malformed/unknown/forbidden field or target | Q2/Q3/Q6: validation/status/code/details | Allowlist, ID/enum/limit/reference failures |
| Missing vs inaccessible Task | Q6: exact 403/404 disclosure policy | Không copy IAM/Project error policy thành Task policy |
| Illegal/stale/duplicate/payload-mismatch command | Q4/Q6/Q7: status/code/replay response | Không double mutation/history hoặc overwrite stale version |
| Persistence/history/audit failure | Q7/Q8: rollback/response/retry mapping | B4 yêu cầu task/history cùng commit hoặc rollback |
| Internal upstream unavailable/timeout | Q6/Q9: safe status/body/correlation | Không direct-DB fallback, không trả protected upstream data |

**APPROVED HISTORY INTENT B4/B7:** append-only task_events cùng transaction
với mutation; actor type/identity, event/source, changed metadata, task version,
time, operation/correlation, initiating user + Agent/proposal provenance khi
áp dụng; không full prompt/raw context. Exact field types/names, nullability,
event vocabulary, before/after safety, readable projection và retention còn Q8.
Compliance audit sink của Task chưa được IAM/Project decision chốt thay.

**APPROVED DELIVERY B4:** nếu phải publish bền vững, outbox cùng transaction,
relay sau commit và dedup event ID. V1 có consumer nào/no-consumer, event DTO,
retry/expiry/retention vẫn Q9. Leader D1–D6 về Organization không tự chọn Task
email consumer/outbox. Runtime/config/health/trust/timeouts chưa triển khai;
DATN-96 cần exact values và evidence riêng, không dùng port proposal làm default.

## 7. Ghi quyết định, nghiệm thu phần tài liệu và tracking

Reviewer trả lời theo mẫu cho từng UC/field/edge/action/API item:

```text
Item + Q/subtask:
Accepted answer (hoặc rejected/deferred + phạm vi):
Decision authority/approver:
Evidence + owning revision/commit + ngày duyệt:
Owning contract/OpenAPI/schema cần đồng bộ:
Acceptance cases và downstream được mở chặn:
Chi tiết vẫn UNKNOWN:
```

Phúc tổng hợp; named Product/Security/API/DB/runtime approvers chưa được xác
nhận. Không suy ra authority từ Reporter hoặc review dạng Comment. Reviewer
có thể chọn proposal/alternative hoặc chỉ duyệt một phần; ghi đúng PARTIAL.

Theo quy ước tracking user ngày 06/10 và 11/10: status Jira phản ánh **phần việc
đã làm**, quyết định product/readiness ghi riêng. Sáu worksheet/checkpoint đã
chuẩn bị để review → đề nghị To Do → In Review cho DATN-105–110; user tự đổi.
Nếu phần tài liệu được nghiệm thu theo precise blocker list thì tiến độ có thể
Done mà Q chi tiết vẫn open; đó không phải authority triển khai DATN-94/95/96.
Parent hiện In Review; không tự chuyển status/gỡ dependency hoặc gọi report
merge là full contract Approval. Thứ tự 105+106 → 107/108/109 → 110 là luồng
review đề nghị, không phải dependency cứng được suy ra từ số thứ tự subtasks.

Đối chiếu từng review item và [scenarios validation](15-task-v1-review-validation.md)
trước khi nhận quyết định. Scenarios chưa phải runtime tests đã chạy.
