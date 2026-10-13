# DATN-93 — Worksheet review Task V1 theo DATN-105–110

**Trạng thái:** Review package: APPROVED BASELINE / PARTIAL recommendations /
PROPOSED exact policies / UNKNOWN answers; chưa phải approved implementation contract.
**Revision:** R3, 13/10/2026 (Asia/Saigon). **Owner tổng hợp:** Nguyen Hong Phuc.

Worksheet cụ thể hóa các gaps trong [working contract R5](13-task-v1-contract-readiness.md)
để reviewer trả lời từng item. [Review PR #22](https://github.com/DATN-SPRING2027/Document/pull/22#pullrequestreview-5410654477)
ghi **No findings**, dạng Comment; đó không phải Approval hay quyết định product.
Reviewer đã duyệt **hướng trình bày T1–T9**, chưa duyệt policy T1–T9 trong phản
hồi user chuyển ngày 13/10. Riêng approval record mới trên main ghi nhận
recommendations được duyệt một phần (§0.1); không bỏ qua evidence mới hoặc coi
nó là exact policy approval. Chi tiết chưa có answer vẫn UNKNOWN. Không provision,
tạo fixture, enable endpoint hoặc transition từ các candidate này.

Nguồn owning: [Task Use Cases](12-continuum-task-management-use-cases.md) (S3),
[Task storage proposal](../../database-design/12_TASK_MANAGEMENT_SCHEMA.md) (S4),
[Governance baseline / Task permission proposal](../02_ACTORS_ROLES_AND_PERMISSIONS.md) (S5),
[ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md) (S1),
[ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md) (S2).
B1–B10 và Q1–Q9 giữ ID của working contract; không tạo một bộ authority khác.

## 0. Baseline có nguồn — giữ nguyên, không xin duyệt lại

Các link dưới pin **Document `69c16445417f3fbcaecd6b04943603c092003b77`** và
**DATN-BE `fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a`**, đã fetch ngày
13/10/2026. Line range trỏ trực tiếp tới statement/section owning. ADR-009 chỉ
bị ADR-010 supersede ở deployment/database placement; B5 vẫn theo ADR-009.

| ID | APPROVED BASELINE | Owning evidence tại revision đã pin | Giới hạn authority / phần cần quyết định |
|---|---|---|---|
| B1 | Continuum Task API canonical; MongoDB operational records; không Jira import/sync/two-way write trong MVP | [ADR-009, Decision 1–2](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-tech/ADR-009-internal-task-source-and-mongodb.md#L12-L15) | Không chọn fields, routes hoặc lifecycle |
| B2 | Existing DATN-BE/DATN-FE; Task là NestJS process riêng; không repo ManageWork/cluster Mongo mới | [ADR-010, Decision 1–5](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-tech/ADR-010-task-service-in-existing-repositories.md#L18-L22) | Accepted target; không phải runtime/config đã triển khai |
| B3 | Browser qua existing BFF/Gateway; consumers qua authenticated API/event contract, không direct Task collections | [ADR-010, Decision 3–6](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-tech/ADR-010-task-service-in-existing-repositories.md#L20-L23) | Exact routes/trust/errors còn T6/T9 |
| B4 | Task sở hữu target `continuum_task`, `tasks`, append-only `task_events`; mutation + history atomic trong Task DB; outbox cùng transaction khi cần durable publish | [ADR-010, Decision 5/7](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-tech/ADR-010-task-service-in-existing-repositories.md#L22-L24) | Không xin chọn lại atomic history hoặc audit owner/status tối thiểu B8; exact coverage/schema/retention, Task-specific shared-audit mapping và consumer decision còn riêng |
| B5 | Work Note **có thể tùy chọn** tham chiếu internal Task qua logical `taskId`; Task không tự thành verified knowledge/standalone SAG source | [ADR-009, Decision 3–4 và scope validation](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-tech/ADR-009-internal-task-source-and-mongodb.md#L16-L23) | Optional reference đã accepted; feature/UI inclusion, cardinality và stale-link/DTO chưa được ADR chọn |
| B6 | Authorized Team Leader chọn/giao Task qua Task API; Handover giữ workflow/reference riêng; operation ID/idempotency/retry/compensation, không shared Task/Handover transaction | [ADR-009, Decision 5](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-tech/ADR-009-internal-task-source-and-mongodb.md#L18), [ADR-010, Decision 6](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-tech/ADR-010-task-service-in-existing-repositories.md#L23) | Eligible states/targets, successor access lifetime và exact recovery còn T2/T4/T7 |
| B7 | Agent dùng authorized context/proposal; permitted human xác nhận trước mutation; safe history provenance gồm user + Agent/proposal identity, không full prompt/raw context | [ADR-010, Decision 7–8](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-tech/ADR-010-task-service-in-existing-repositories.md#L24-L25) | Metadata intent accepted; feature inclusion và event names/types/projection/retention chưa được chọn |
| B8 | ACTIVE OrganizationMembership chứng minh context; RoleAssignment không thay membership; scoped authority/ACL/explicit deny; ADMIN/platform không implicit confidential access. Audit **ít nhất thay đổi owner/status Task trong approved Task scope**; logs tránh token, full prompts, document bodies | [Actors, §2–3](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md#L15-L54), [Actors, §7 audit minimum/privacy](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md#L102-L106), [Workspace, §4.1–4.2 / DEC-016](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-docs/Workspace/00-organization-and-access-contract-readiness.md#L66-L117) | Minimum audit/privacy accepted; Task action codes/matrix, exact events/schema/retention và shared-audit mapping vẫn cần Task-specific decision; không dùng ADR-009/010 thay governance |
| B9 | Creator bootstrap ordinary Project MEMBER, không Leader/owner/Team; documented create/edit Task rights khi API có mặt. Leader Tổng = Org ADMIN; Leader Project = Project TEAM_LEADER | [Project creator, Decision, 30/09 reaffirmed 04/10](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/docs/decisions/project-creator-member-bootstrap-v1.md#L3-L16), [Project Access, Accepted role mapping, 02/10](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/docs/decisions/project-access-visibility-v1.md#L11-L17) | Không cấp sửa mọi Task/field hoặc tự seed Task permissions |
| B10 | PUBLIC/Org ADMIN Project metadata access không cấp Task content; removal → INACTIVE giữ membership/assignment records nhưng thu hồi effective Project access; Project-scoped auth cần ACTIVE ProjectMembership | [Project Foundation, Contract used](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/docs/decisions/project-foundation-read-mvp.md#L7-L17), [Project Access, Visibility/Membership operations](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a/docs/decisions/project-access-visibility-v1.md#L34-L47) | Không chọn Task assignment clear/transfer/delete hoặc copy Project 404/audit policy sang Task |

### 0.1 Evidence mới — PARTIAL, không mở chặn implementation

[Approval record §Approved recommendations](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-docs/Internal-Work-Management/20-task-v1-contract-approval-record.md#L3-L28)
ghi Trần Kim Thắng (Leader), ngày 13/10, approve recommendations §12 tại
source `145af128e70fcfbcd6a64d5ac7859dfb9468d14c`; PR #30 ghi record này trên main.
Authority là approval evidence trong record, không phải việc PR được merge.

- **PARTIAL T1:** core Project-local list/create/detail/edit/assignment/status/
  search/limited history được chọn ở recommendation level. Exact UC scope,
  projection và permissions còn UNKNOWN; Work Note/Handover inclusion cần owner
  approve exact contract; advanced capabilities deferred trừ khi scope riêng.
- **PARTIAL T2/T3:** Project owns Task, đúng một Project; Team/assignee 0..1
  cardinalities được ghi nhận. Stable ID/title/creator/server timestamps là field
  principles; exact dictionary/eligibility còn UNKNOWN. Organization contextual;
  **persist `organizationId` chưa được chọn**, phải có query/isolation need.
- **PARTIAL T8/T9:** safe append-only history boundary/atomicity giữ nguyên;
  exact coverage/schema/retention chưa chọn, nhưng audit owner/status tối thiểu B8
  đã accepted. Outbox deferred tới khi named durable consumer được approve; điều
  này không chọn đáp án no-consumer hoặc Task-specific shared-audit mapping.
- Record cũng chọn non-unique Task titles, query-derived index/validation/test
  methods và chưa thêm delete/archive field/route trước khi có policy. Đây không
  phải phê duyệt concrete schema/index, API hoặc deletion/retention behavior.

[Open decisions và readiness](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-docs/Internal-Work-Management/20-task-v1-contract-approval-record.md#L30-L47)
vẫn giữ exact fields/permissions/lifecycle/errors UNKNOWN; **25 transition cells
UNKNOWN và disabled; D-03 BLOCKED**. [D02-R1](16-task-v1-state-machine-contract.md)
và [reliability proposal](17-task-v1-command-reliability-review.md) của DATN-94
vẫn PROPOSED/UNKNOWN; Jira Done hay PR #26 merge không thành policy approval.

### 0.2 Audit Task — baseline, topology và target/proposal

| Concern | Authority/evidence | Trạng thái và giới hạn |
|---|---|---|
| Audit owner/status tối thiểu, tránh token/full prompts/document bodies | [Actors Accepted baseline, §7](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md#L102-L106) | **APPROVED BASELINE B8** trong approved Task scope; không hỏi lại có cần audit hay cho phép bỏ audit |
| Shared audit destination `continuum_audit` | [Database catalog, Phạm vi](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/database-design/README.md#L8), [Audit catalog entry](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/database-design/README.md#L57) | Shared topology đã được ghi nhận; chưa là quyết định mỗi Task event phải ghi thêm vào shared sink hoặc Task-specific integration đã triển khai |
| `audit_logs`, Task action vocabulary và retention examples | [Audit schema, §2.1](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/database-design/10_AUDIT_AND_COMPLIANCE_SCHEMA.md#L22-L67), [Retention example](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/database-design/10_AUDIT_AND_COMPLIANCE_SCHEMA.md#L100-L109) | **TARGET/PROPOSED** cho Task-specific names/coverage/schema. `TASK_CREATED`, `TASK_UPDATED`, `TASK_ASSIGNED`, `TASK_STATUS_CHANGED`, `TASK_CANCELLED` và ví dụ 365 ngày chưa được Task-specific approval |
| Exact history contract còn mở | [Approval record, History boundary và atomicity](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-docs/Internal-Work-Management/20-task-v1-contract-approval-record.md#L23-L24) | Exact event coverage/schema/readers/retention UNKNOWN; không hủy minimum owner/status audit B8 hoặc atomic domain history B4 |

Schema phân biệt domain `task_events` phục vụ Task history với shared `audit_logs`
phục vụ security/accountability; không ghi toàn bộ Task description/document vào
diff. T8-A chỉ chốt cách đáp ứng audit bắt buộc: `task_events` có đủ hay cần ghi
thêm vào `continuum_audit`; không xin quyền bỏ minimum audit.

## 1. DATN-105 — V1 làm gì, không làm gì, ai dùng

**PARTIAL core recommendations (§0.1); PROPOSED exact scope**, tổng hợp S3 mục 3–7. Reviewer ghi `included`, `deferred`
hoặc `excluded` cho từng dòng, không chỉ duyệt chung câu “Task V1”. Đề nghị
review nhóm core cùng nhau vì update/assignment/lifecycle/history ảnh hưởng
data và API ngay từ đầu; lịch triển khai từng slice không tự thay release scope.

| ID | Use case | Đề nghị để review | Accepted scope |
|---|---|---|---|
| UC-TM-01 | List Task | Included, scoped list | PARTIAL core recommendation; exact Q1 UNKNOWN |
| UC-TM-02 | Create Task | Included, một đơn vị công việc đơn giản | PARTIAL core recommendation; exact Q1 UNKNOWN |
| UC-TM-03 | View Task detail | Included, chỉ projection được quyền xem | PARTIAL core recommendation; exact Q1 UNKNOWN |
| UC-TM-04 | Update Task | Included, allowlist field; không generic status/assignee PATCH | PARTIAL core recommendation; exact Q1/Q3/Q5 UNKNOWN |
| UC-TM-05 | Assign/reassign Task | Included, command riêng trong scope | PARTIAL core recommendation; exact Q1/Q2/Q5 UNKNOWN |
| UC-TM-06 | Change status | Included, fixed lifecycle được duyệt | PARTIAL core recommendation; exact Q1/Q4/Q5 UNKNOWN |
| UC-TM-07 | Basic search/filter | Included trong list; bounds cần chốt | PARTIAL core recommendation; exact Q1/Q6 UNKNOWN |
| UC-TM-08 | Optional Work Note link | B5 optional logical link accepted; đề nghị feature included khi owner duyệt exact contract | PARTIAL integration recommendation; exact Q1/Q2/Q6 UNKNOWN |
| UC-TM-09 | Handover open tasks | B6 Team Leader/Task API boundary accepted; included khi owner duyệt exact contract | PARTIAL integration recommendation; exact Q1/Q4/Q7 UNKNOWN |
| UC-TM-10 | View history | Included, scoped read-only history | PARTIAL limited history recommendation; exact Q1/Q5/Q8 UNKNOWN |
| UC-TM-11 | Agent rewrite proposal | Deferred đến khi core/ACL có contract; B7 vẫn áp dụng nếu bật | PARTIAL advanced deferral; exact release Q1 UNKNOWN |
| P1-KANBAN | Fixed-column board | Deferred; thay đổi demo scope cần quyết định riêng | PARTIAL advanced deferral; exact Q1 UNKNOWN |
| P1-SUBTASK | Subtask một cấp | Deferred; không nhầm với subtasks Jira của team | PARTIAL advanced deferral; exact Q1 UNKNOWN |

**APPROVED EXCLUSIONS:** Jira canonical/import/sync/two-way writes (B1),
Task record thành standalone SAG source (B5), Agent tự ghi Task hoặc bypass
human confirmation (B7), repo ManageWork/cluster Mongo mới (B2).

**PARTIAL advanced deferral (§0.1); PROPOSED exact exclusions/deferrals:** Scrum/sprint/estimate;
Epic/Story/Bug/version; workflow editor; Task comment/file/mention/watcher;
time tracking; JQL/shared filters; dependency graph; automation/notification
builder; dashboard/report; bulk operations; hard delete/archive/retention
feature. Nguồn S3 mục 4; từng nhóm vẫn cần Q1, không suy ra release exclusion
từ một chức năng tương tự của Jira. Work Note/evidence không tự cấp Task ACL.
§0.1 đã chọn advanced deferral ở recommendation level và chưa thêm delete/archive
field/route; chi tiết từng feature/deletion/retention rule vẫn cần exact answer.

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

**PARTIAL field/ownership principles (§0.1), PROPOSED exact DATA**, từ S3 Field
tối thiểu/mục 7 và S4 mục 3. Đây là candidate contract dictionary, không phải
schema/OpenAPI đã duyệt. Required/default chưa có owning answer vẫn là proposal;
chỉ các phần có evidence §0.1 được ghi nhận trong scope đó. Type/limit/null/normalization chưa có owning answer
phải được ghi rõ; không tự đặt title length hay enum mới để lấp ô trống.

| Candidate field | Proposal để review | Exact accepted detail còn thiếu |
|---|---|---|
| id/_id | Stable ID principle đã chọn (§0.1); Mongo ObjectId/API string representation là candidates | Q3: API/storage name/type/format, validation; chưa có key/sequence contract |
| organizationId | Trusted Organization context required; persisting derived organizationId conditional, chưa chọn (§0.1) | Q2/Q3/Q6: query/isolation rationale, derivation/integrity, representation |
| projectId | Đúng một Project ownership đã chọn (§0.1); exact field requiredness/type còn mở | Q2/Q3: reference/state eligibility, representation |
| teamId | 0..1 Team cardinality đã chọn (§0.1); exact shape còn mở | Q2/Q3/Q5: null/absent, eligibility, teamless access, reassignment |
| title | Required string, editable | Q3: trim/empty/length/encoding limits |
| description | Optional string, editable | Q3/Q5: null/clear, format/size, visible content |
| createdBy | Required authenticated user; server-owned | Q3/Q6: representation và attribution/trusted caller |
| assigneeId | 0..1 assignee cardinality đã chọn (§0.1); self/Leader assignment vẫn proposal | Q2/Q5: eligible target/unassign/cross-scope rules |
| status | Server initial TODO, approved command sau đó | Q3/Q4: accepted enum/default và writable operations |
| priority | LOW/MEDIUM/HIGH; server default MEDIUM | Q3: accepted enum/default/editability |
| type | Chỉ TASK | Q1/Q3: có persist/expose field hay implied single type |
| dueDate | Optional, editable | Q3: date-only/timestamp, timezone, past date, null/clear |
| createdAt/updatedAt | Server timestamps | Q3/Q6: exact representation, clock semantics |
| version | Server mutation version | Q3/Q7: type/initial value/CAS/token/ETag semantics |

Project/Team/assignee cardinality đã có limited answer (§0.1); reference review
phải đóng riêng: Organization/Project/Team parent IDs; assignee
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

**Transition matrix for review: tất cả 25 cells vẫn UNKNOWN (Q4/Q5/Q7).**
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
| Persistence/history failure | Q7/Q8: response/retry mapping | B4 yêu cầu task/history cùng commit hoặc rollback; không hỏi duyệt lại atomicity |
| Additional shared audit failure | T8-A: mandatory events chỉ task_events hay cần ghi thêm continuum_audit; consistency/failure policy UNKNOWN | Minimum owner/status audit B8 vẫn bắt buộc; không suy atomic cross-DB hoặc eventual delivery từ B4 |
| Internal upstream unavailable/timeout | Q6/Q9: safe status/body/correlation | Không direct-DB fallback, không trả protected upstream data |

**APPROVED HISTORY INTENT B4/B7:** append-only task_events cùng transaction
với mutation; actor type/identity, event/source, changed metadata, task version,
time, operation/correlation, initiating user + Agent/proposal provenance khi
áp dụng; không full prompt/raw context. Exact field types/names, nullability,
event vocabulary, before/after safety, readable projection và retention còn Q8.
**APPROVED AUDIT MINIMUM B8:** audit ít nhất thay đổi owner/status trong approved
Task scope; logs tránh token, full prompts và document bodies. Shared audit
topology `continuum_audit` đã có trong catalog (§0.2); Task-specific routing và
mapping chưa được IAM/Project decision chốt thay. Tên `TASK_*` và ví dụ retention
365 ngày trong audit schema là **TARGET/PROPOSED**, chưa là Task-specific approval.
**T8-A cần quyết định:** event audit bắt buộc được đáp ứng **CHỈ TASK_EVENTS**
hay **GHI THÊM CONTINUUM_AUDIT**? Schema/coverage chi tiết, readers/retention và
consistency/failure policy còn UNKNOWN. **DEFER** giữ gap mở, không chọn mặc định
hoặc bỏ audit tối thiểu. Chi tiết ở §8/T8.

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

Phúc tổng hợp; Leader cho scoped recommendations đã được record §0.1 ghi nhận.
Named Security/API/DB/Handover/runtime approvers và authority cho exact open
items vẫn cần xác nhận. Không suy ra authority từ Reporter hoặc review dạng Comment. Reviewer
có thể chọn proposal/alternative hoặc chỉ duyệt một phần; ghi đúng PARTIAL.

Theo quy ước tracking user ngày 06/10 và 11/10: status Jira phản ánh **phần việc
đã làm**, quyết định product/readiness ghi riêng. Snapshot live 13/10/2026:
[DATN-93](https://trankimthang0207.atlassian.net/browse/DATN-93) và DATN-105–110
**Done**, progress 100%; children Unassigned, descriptions trống, không thấy
linked dependency giữa children. PR #22 **merged**, commit
`8ab9268523c3fb661008cd0b6715e0e1ca3cd79c`; precise blocker list đã hoàn thành.
Status hiện tại → đề nghị **giữ Done** cho phần report, không reopen vì policies mở.
Parent links vẫn **blocks DATN-94/95/96**; downstream hiện 94 Done (docs), 95
In Progress, 96 To Do. 94 blocks 100; 95 và 96 blocks 97. Không sửa tracking/dependency,
không suy report merge hoặc Done là authority triển khai các policies chờ duyệt.
Thứ tự 105+106 → 107/108/109 → 110 chỉ là luồng review đề nghị.

Đối chiếu từng review item và [scenarios validation](15-task-v1-review-validation.md)
trước khi nhận quyết định. Scenarios chưa phải runtime tests đã chạy.

## 8. Phiếu xin quyết định chi tiết T1–T9

T1–T9 ánh xạ Q1–Q9, không tạo bộ authority mới. **APPROVED BASELINE** ở §0
giữ nguyên; **PARTIAL** chỉ trong scope §0.1; lựa chọn mới dưới đây **PROPOSED**,
accepted exact answer **UNKNOWN** tới khi có evidence. Reviewer presentation
approval không chọn các policies này. Bản chat gửi reviewer chỉ dẫn tới worksheet;
chi tiết quyết định và phần thiếu nằm ở đây.

### T1 — Scope V1 (Q1 / DATN-105)

**PARTIAL:** core Project-local list/create/detail/edit/assignment/status/search/
limited history đã được chọn ở recommendation level (§0.1). Work Note logical
`taskId` tùy chọn là **APPROVED BASELINE B5**, không xin chọn lại optionality.
Feature/UI inclusion của Work Note và Handover chưa có exact integration approval.

**PROPOSED exact scope:** included UC-TM-01–07 và 10; UC-TM-08–09 included khi
owning Capture/Handover reviewer duyệt exact contract. Deferred Agent rewrite,
Kanban và subtask sản phẩm. Đề nghị ngoài V1: Scrum/estimate, Epic/Story/Bug/
version, workflow editor, comment/file/mention/watcher riêng của Task, time
tracking, JQL, dependency graph, dashboard/report và bulk operations. Delete/
archive field/route tiếp tục deferred theo §0.1, policy retention vẫn UNKNOWN.
Jira import/sync, Task standalone SAG source, Agent tự ghi canonical và repo/
cluster mới đã excluded bởi B1/B2/B5/B7, không xin duyệt lại.

**Cần quyết định:** điền included/deferred/excluded cho từng UC/feature, slice và
acceptance; owner chốt optional integration có vào V1 hay không. Chọn scope không
tự chốt fields/quyền/lifecycle/API. Exact release answer còn UNKNOWN.

### T2 — Relationships và target eligibility (Q2 / DATN-107/109)

**PARTIAL:** Project owns Task; đúng một Project, Team/assignee 0..1 cardinalities
đã được record §0.1 chọn. Organization contextual; persist derived organizationId
chỉ khi được duyệt query/isolation need. **B5/B6 giữ optional logical taskId và
Task API/Handover boundary**; successor không tự kế thừa predecessor permissions.

**PROPOSED:** Work Note 0..1 Task mỗi note / Task 0..N notes; Team phải thuộc
Project đã chọn; assignee/successor là User và memberships eligible trong scope.
**UNKNOWN cần quyết định:** exact Work Note cardinality/DTO/stale-link behavior;
parent/Team membership requirements cho Task có Team hoặc teamless; target
eligibility và successor access/projection/lifetime. Khi membership suspend/remove
hoặc parent archived, giữ assignment, unassign hay chuyển người nào, ai thực hiện,
thứ tự/failure recovery? D1–D6 Organization không chọn các Task effects này.

### T3 — Fields, defaults và validation (Q3 / DATN-107)

**PARTIAL:** stable Task ID, Project ownership, title, creator, server timestamps
và field cần bởi approved operations; server-derived trusted actor/context;
non-unique Task title (§0.1). Không lấy principles này thành exact schema.

**PROPOSED candidates:** single type TASK; Mongo ObjectId/API string ID;
projectId/title/createdBy required; teamId/description/assigneeId/dueDate optional;
server id/creator/time/status/priority/version; initial TODO, priorities
LOW/MEDIUM/HIGH default MEDIUM. organizationId là trusted context; **persistence
presence UNKNOWN**, không ép field required từ packet cũ.

**Cần API/DB owner quyết định** từng field: name/type/representation, required/
optional, null vs absent/clear, default, trim/empty/length/payload bounds, enum,
server-owned/editable và reference validation. dueDate date-only hay timestamp,
timezone/past-date rule? version initial/type/bounds? Có persist type field không?
Approved principles/default riêng vẫn **PARTIAL** khi dictionary chưa đủ; không
tự đặt numeric limits hoặc nullable semantics. D-03 proposal không là schema approval.

### T4 — Lifecycle/transition/reason (Q4 / DATN-108; D02-01–03)

**PROPOSED:** TODO, IN_PROGRESS, BLOCKED, DONE, CANCELLED; initial TODO;
DONE reopen về IN_PROGRESS; CANCELLED terminal; DONE không bắt buộc Work Note/
evidence và không thành verified knowledge; Handover assignment chỉ open states
TODO/IN_PROGRESS/BLOCKED. B5 optional link không tự chọn completion guard này.

Tám **candidate allow edges**, từ [D02-R1 §3, transition register](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-docs/Internal-Work-Management/16-task-v1-state-machine-contract.md#L74-L111):
START TODO→IN_PROGRESS; CANCEL TODO→CANCELLED; BLOCK IN_PROGRESS→BLOCKED;
COMPLETE IN_PROGRESS→DONE; CANCEL IN_PROGRESS→CANCELLED; RESUME BLOCKED→IN_PROGRESS;
CANCEL BLOCKED→CANCELLED; REOPEN DONE→IN_PROGRESS. **Không edge nào đã enabled.**
START/BLOCK/COMPLETE/RESUME/REOPEN đề nghị current assignee hoặc scoped Leader;
CANCEL đề nghị scoped Leader. Reason sau trim required cho BLOCK/RESUME/CANCEL/
REOPEN, optional START/COMPLETE. Đề nghị 17 cells còn lại reject, gồm new same-state
command; exact committed retry xử lý qua T7, không thành same-state command mới.

**Cần quyết định:** approve/amend/defer từng state/edge cùng actor/guard/reason,
initial/terminal/completion/Handover semantics và error/event oracle. **Tất cả
25 accepted cells còn UNKNOWN/disabled**, kể cả candidate rejects chưa là exact
error policy. DATN-94 Done/PR #26 merge không chọn matrix; §0.1 cũng chưa chọn.

### T5 — Action × actor × scope × resource permissions (Q5 / DATN-109)

**B8–B10 giữ nguyên:** current authenticated Organization/Project membership,
scoped assignment + resource ACL/explicit deny; metadata access không grant Task
content; creator ordinary MEMBER có documented create/edit rights khi API có mặt.

**PROPOSED:** MEMBER create unassigned/self-assigned và sửa allowlist nếu creator
hoặc current assignee; scoped TEAM_LEADER quản lý/giao eligible Task; current
assignee/scoped Leader change status theo T4; cancel scoped Leader; read/search/
history theo current scope/ACL. SUCCESSOR assignment riêng không grant create/
reassign/cancel hoặc quyền toàn Project. Agent không có mutation grant độc lập.

**Cần quyết định:** exact action/permission-code matrix, Project vs Team Leader,
teamless Task, creator vs assignee editable fields, successor projection/lifetime
và reauthorization/fence khi quyền đổi giữa authorize/write. Candidate codes §5
chưa là Role seed. ADMIN/platform có evidence member/permission khác hợp lệ phải
evaluate evidence đó; không blanket deny actor chỉ vì tên role quản trị.

### T6 — Exact API/DTO/errors và query controls (Q6 / DATN-110)

**B3 accepted; exact contract UNKNOWN.** Chỉ định API/Security/Gateway/BFF
reviewer chốt method/path/version, request/response/success status/error details
cho create, list/search, detail, update, assign/reassign, transition/cancel/reopen
và history. **PROPOSED:** command riêng cho state/assignment; mutable allowlist,
không copy generic response fields vào update input.

**Cần quyết định:** trusted identity/context transport; DTO/types/nullable/bounds;
accepted filters/sort/pagination/limits/totals; unauthenticated, inactive/cross-
scope/ACL, malformed/missing/inaccessible, duplicate/illegal/stale/mismatch và
upstream timeout/failure responses. Chốt 403/404 concealment/error precedence;
không copy Project/IAM errors hoặc paging như Task contract đã duyệt.

### T7 — Version, replay và Handover recovery (Q7 / DATN-108/110)

**B4/B6/B7 accepted:** atomic domain history; Handover assignment API với operation
ID/idempotency/retry-compensation; history version/provenance intent. **Exact
reliability PROPOSED/UNKNOWN**, xem [D02 reliability](17-task-v1-command-reliability-review.md).

Đề nghị monotonic Task version/CAS chung update/assignment/state, expectedVersion
bắt buộc cho command mới; stale → refetch/human reconfirm, không auto-reapply.
Stable operation identity (Organization, Task, principal, operation-ID), normalized
command/payload/version/reason fingerprint; correlation/session token không thay
operation identity. Retry qua current authorization; exact committed replay trả
safe acknowledgement kết quả cũ, không mutation/history/version lần hai hoặc CAS
lại với version cũ. Mismatch không overwrite; durable result/dedup proof cùng
mutation/history là **proposal DB**. Handover stable service principal bind
initiating human/item/intent; không shared DB transaction/direct Task DB.

**Cần owners API/DB/Security/Handover quyết định:** namespace/normalization, wire
version/ETag; missing/stale/mismatch/in-flight/abort outputs; freshness/fence;
durable proof/retry/backoff/window theo recovery horizon; late replay/expiry
không execute lại; retention và recovery owner. Không chọn duration mặc định;
approve CAS riêng không duyệt toàn bộ reliability/schema/index.

### T8 — Audit tối thiểu, domain history và shared sink mapping (Q8 / DATN-110)

**APPROVED BASELINE B4/B7/B8 — không xin duyệt lại:** Task mutation và append-only
`task_events` atomic **trong Task DB**, cùng commit hoặc rollback. Metadata intent
gồm actor type/identity, event/source, changed fields, version/time, operation/
correlation; event giữ initiating user + Agent/proposal identity cho human-confirmed
Agent flow. **Audit ít nhất các thay đổi owner/status trong approved Task scope**
theo [Actors §7](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md#L102-L106).
Logs tránh token, full prompts và document bodies; history không full prompt/raw
context. §0.1 giữ safe append-only boundary. Baseline audit không enable owner/
status mutation hoặc transition chưa được duyệt.

**Shared topology đã có nguồn:** [database catalog](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/database-design/README.md#L8)
ghi `continuum_audit` là đích audit dùng chung. [Audit schema §2.1](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/database-design/10_AUDIT_AND_COMPLIANCE_SCHEMA.md#L22-L67)
phân biệt domain `task_events` và shared `audit_logs`; không full description/
Task document trong diff. Task action names `TASK_CREATED`, `TASK_UPDATED`,
`TASK_ASSIGNED`, `TASK_STATUS_CHANGED`, `TASK_CANCELLED` là **TARGET/PROPOSED**
cho Task-specific contract tới khi có approval. Ví dụ retention **365 ngày chưa
được duyệt** cho Task history hoặc Task compliance audit.

**Exact contract UNKNOWN:** event coverage ngoài minimum owner/status và mapping
minimum đó thành events cho create/update/assignment/transitions; event names/
types/nullability, safe changed fields/before-after/redaction; ordering/paging,
readers/projection và retention. [Approval record, History boundary](https://github.com/DATN-SPRING2027/Document/blob/69c16445417f3fbcaecd6b04943603c092003b77/research-docs/Internal-Work-Management/20-task-v1-contract-approval-record.md#L23-L24)
giữ các chi tiết này UNKNOWN, không hủy minimum audit B8. S4/D02 và schema target
không tự approve event vocabulary. B4 atomic domain history không tự chốt
Task-specific shared-audit mapping hoặc atomic cross-database transaction.

**T8-A — Câu hỏi phải chọn rõ:** Trong V1, **audit events bắt buộc** (ít nhất
owner/status trong approved Task scope) được đáp ứng **chỉ trong `task_events`**,
hay cần **ghi thêm vào `continuum_audit`**? Accepted Task-specific answer hiện
**UNKNOWN**; worksheet chưa chọn đáp án.

- **CHỈ TASK_EVENTS:** Security/Architecture xác nhận domain history đáp ứng đủ
  minimum audit baseline trong approved V1 scope; ghi rõ không thêm shared audit
  record cho Task trong scope đó. Chốt coverage/schema, owner, quyền đọc/projection,
  retention và failure mapping; giữ atomic Task/history B4. Đây không là lựa chọn
  bỏ audit hoặc bỏ safeguards chỉ vì chưa có shared integration.
- **GHI THÊM CONTINUUM_AUDIT:** giữ domain history B4 và bổ sung Task-specific
  mapping vào shared audit topology đã có. Chốt owner/producer, collection hoặc
  API/write boundary, event coverage/schema (gồm rejected-attempt policy), quyền
  đọc/administration/redaction, retention và **consistency/failure policy**.
  Audit bổ sung phải atomic với mutation hay theo delivery contract nào? Sink
  lỗi/unavailable trả gì, có cho mutation commit không, retry/dedup/recovery owner
  nào? Không mặc định `audit_logs`, tên `TASK_*`, 365 ngày, atomic cross-DB hoặc
  eventual delivery chỉ từ catalog/schema target.
- **DEFER:** ghi blocker/owner và slice bị ảnh hưởng; giữ mapping UNKNOWN,
  không suy Task-events-only hoặc bỏ audit tối thiểu từ im lặng.

**Nguồn thiếu:** original owning ADR-003/SPEC-001 không tìm thấy trong inspected
workspace; AGENTDB chỉ dẫn đường tới path khác. Cần Architecture/DB/Security owner
cung cấp revision/section hiện hành hoặc explicit Task-specific decision cho
phần còn thiếu. IAM/Project audit source không chọn exact Task event mapping/
schema/retention. B4 atomic history, B5 optional reference và B8 minimum audit
có nguồn độc lập; không đưa các invariant này trở lại trạng thái chờ duyệt.

### T9 — Runtime/config và consumer decision (Q9 / DATN-106/110)

**B2–B4 accepted target:** Task là process riêng trong existing BE, continuum_task
trên infra hiện có, existing BFF/Gateway. §0.1 outbox deferred tới khi named durable
consumer được approve; **consumer inventory/decision vẫn UNKNOWN**.

**Cần Runtime/API owner quyết định:** internal port registry/config/fail-fast,
health/readiness, trust/correlation/timeouts/failure mapping và BE/FE guide
reconciliation. Port 3009 vẫn proposal, không thành default từ ADR table.

Chọn explicit **V1 no async consumer** hoặc liệt kê **từng named consumer** với
approval/scope. Nhánh durable publication cần giữ B4 same-transaction outbox,
after-commit relay, consumer dedup event ID rồi chốt schema/retry/retention/owner.
Organization email outbox không chọn Task notifications. T8 mandatory-audit
destination/mapping và T9 async delivery là hai quyết định khác nhau.

### Cách ghi câu trả lời và phần còn thiếu

```text
Item T/Q + exact UC/field/edge/action/API:
APPROVE / AMEND / DEFER — answer và scope cụ thể:
Authority/approver + evidence permalink:
Owning contract/source revision + ngày duyệt:
T8-A: CHỈ TASK_EVENTS / GHI THÊM CONTINUUM_AUDIT / DEFER:
Owner/event mapping/schema/readers/retention/consistency/failure policy cho lựa chọn:
Owner API / DB / Security / Capture / Handover / Runtime cho phần chưa chốt:
Chi tiết vẫn UNKNOWN hoặc deferred khỏi V1:
```

Approve một phần phải ghi **PARTIAL**, không tự đóng cả Q. Phần thiếu trước
implementation: exact UC/dictionary/eligibility (T1–3), states/25 cells/action matrix
(T4–5), OpenAPI/errors (T6), concurrency/recovery (T7), history/compliance (T8),
runtime/consumer (T9), owning persistence authority và required test evidence.

| Downstream | Exact contract/gate phải đóng trước phần implementation tương ứng |
|---|---|
| DATN-94 / lifecycle enforcement DATN-100 | T4/T5/T7; error/event oracles T6/T8. D02-01–10 vẫn cần answer; scenario docs không phải executable tests |
| DATN-95 | T1–T3/T5–T8 và persistence authority; concrete indexes từ approved T6 query workload; §0.1 recommendation approval không mở D-03 |
| DATN-96 | T5–T9, trusted routing/config/health và guide reconciliation; accepted target không chứng minh runtime đã chạy |

Sau exact decision evidence: đồng bộ owning Document/OpenAPI/schema/acceptance
mapping trên follow-up branch mới từ updated main; checks/review và user xem
trước PR. Không tái sử dụng nhánh PR22 đã merge hoặc reopen report Done. Không
triển khai DATN-94/95/96 theo proposal đang chờ duyệt trong lần chỉnh này.
