# DATN-93 — Task Management V1: contract readiness và quyết định còn thiếu

**Trạng thái:** Báo cáo đối chiếu và danh sách quyết định cần chốt; chưa phải
Task V1 contract được phê duyệt. **Ngày kiểm tra:** 04/10/2026 (Asia/Saigon).
**Task owner:** Nguyen Hong Phuc.

Mục tiêu của [DATN-93](https://trankimthang0207.atlassian.net/browse/DATN-93)
là có contract được duyệt **hoặc danh sách blocker cụ thể**. Báo cáo này thực
hiện phương án thứ hai: phân biệt quyết định hiện hành với proposal, đặt câu
hỏi có thể review và ánh xạ chúng tới công việc phụ thuộc. Việc ưu tiên ticket,
tạo tài liệu hoặc merge tài liệu báo cáo không tự phê duyệt product policy.

## 1. Vì sao làm DATN-93 trước

Tám parent task đang hiển thị cho Phúc đều ghi Priority **Medium** và không có
due date trong description khi đọc Jira. Đây là nội dung mô tả đã đọc, không
phải kết quả xác minh một Priority field riêng của parent. Thứ tự dưới đây là đánh giá theo
dependency, không phải thay đổi Priority trên Jira:

| Nhóm | Dependency đọc trực tiếp trên Jira | Điều kiện bắt đầu phần phụ thuộc |
| --- | --- | --- |
| Task V1 | DATN-93 chặn DATN-94, DATN-95, DATN-96; DATN-94 chặn DATN-100 | Contract, data và runtime tương ứng đã được duyệt; kiểm tra lại main trước code |
| Organization Membership | DATN-86 chặn DATN-87; DATN-87 chặn DATN-88 | Membership contract được chốt trước implementation |
| Team | DATN-89 chặn DATN-90; DATN-90 chặn DATN-91 và DATN-92 | Team contract và foundation tương ứng đã sẵn sàng |
| Organization provisioning | DATN-80 bị DATN-79 chặn; DATN-79 hiển thị To Do trên linked item | Xác minh Platform Operator authorization trước provisioning |

Ưu tiên DATN-93 giúp xử lý nút chặn trực tiếp ba task và nối tiếp lifecycle.
DATN-86 và DATN-89 là các lane contract có thể chuẩn bị độc lập. Nội dung Jira
đã đọc chưa cho thấy một lane được team xếp High hơn lane khác.

## 2. Nguồn và mức thẩm quyền

| ID | Nguồn đã đọc | Dùng để xác định |
| --- | --- | --- |
| S1 | [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md), mục Decision và Consequences | Nguồn Task canonical, MongoDB, Jira exclusion, Work Note/SAG/Handover boundary |
| S2 | [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md), mục Decision, Runtime status và Service setup proposal | Repo/service/database boundary và atomic history; port, queue, DTO vẫn cần chốt |
| S3 | [Task Use Cases](12-continuum-task-management-use-cases.md), trạng thái và mục 3–7 | Danh sách use case, field/status/permission và P0/P1 **đề xuất** |
| S4 | [Task storage design](../../database-design/12_TASK_MANAGEMENT_SCHEMA.md), trạng thái và mục 3–4 | Boundary lưu trữ; field/cardinality/index/history chưa phải approved field-level contract |
| S5 | [Actors, roles and permissions](../02_ACTORS_ROLES_AND_PERMISSIONS.md), mục Task policy | Role vocabulary và governance baseline; task action codes/matrix còn chờ duyệt |
| S6 | [Workspace readiness](../Workspace/00-organization-and-access-contract-readiness.md), mục 2–4 | Nhãn authority, ACTIVE Organization Membership, role/scope/ACL và giới hạn quản trị |
| S7 | [Storage topology](../../architecture/04_STORAGE_MESSAGING_AI.md), mục 1.1 và Task Service storage boundary | Active inventory khác Task target; database-per-service và audit boundary |
| S8 | [DATN-BE source](https://github.com/DATN-SPRING2027/DATN-BE/tree/56036d13ed86f5db47ba7cbcb02256f02eab80ae), src/services, src/gateway và docs/openapi | Implementation evidence tại SHA đã kiểm tra; không dùng code để tự duyệt product policy |
| S9 | [DATN-93](https://trankimthang0207.atlassian.net/browse/DATN-93) và DATN-105–110 | Scope, acceptance criteria và checklist phê duyệt; ticket không tự điền quyết định đang thiếu |

Các nhãn trong báo cáo: **APPROVED** chỉ cho quyết định có nguồn chấp thuận;
**FACT** chỉ là trạng thái source/Jira đã quan sát; **UNKNOWN** là chưa có
bằng chứng chấp thuận để implementation dùng. Có proposal không làm UNKNOWN
thành APPROVED. Quy định đóng băng một thư mục cũng không thay thế phê duyệt
chi tiết mà chính tài liệu trong thư mục đó còn đánh dấu proposal.

## 3. Baseline đã được chấp thuận

| ID | Quyết định | Nguồn |
| --- | --- | --- |
| B1 | Continuum Task API là nguồn canonical duy nhất trong MVP; task operational records lưu MongoDB; không Jira import/sync/two-way write | S1 Decision 1–2 |
| B2 | Task chạy NestJS service/process riêng, source trong DATN-BE; UI/client trong DATN-FE; không tạo repo ManageWork hoặc MongoDB cluster mới | S2 Decision 1–2, 5 |
| B3 | Browser đi qua BFF/Gateway; service khác dùng API/event contract, không truy cập Task collections trực tiếp | S2 Decision 3–4, 6 |
| B4 | Target `continuum_task` sở hữu `tasks` và append-only `task_events`; mutation và history nguyên tử. Outbox cùng transaction chỉ khi có yêu cầu publish bền vững | S2 Decision 5, 7 |
| B5 | Work Note có thể giữ logical `taskId` tùy chọn; task không tự thành verified knowledge hoặc nguồn SAG độc lập | S1 Decision 3–4 |
| B6 | Handover dùng Task API, giữ reference/workflow riêng; assignment dùng operation ID, idempotency và retry/compensation vì hai service không chung transaction | S1 Decision 5; S2 Decision 6 |
| B7 | Agent đọc context được cấp quyền và trả proposal; mutation cần người có quyền xác nhận. Event lưu initiating user và Agent/proposal identity, không full prompt/raw context | S2 Decision 7–8 |
| B8 | ACTIVE OrganizationMembership chứng minh context; RoleAssignment một mình không đủ. ADMIN/PLATFORM_OPERATOR không mặc định có quyền đọc nội dung mật; áp dụng scoped authority và ACL | S5–S6 |

`continuum_task` là **APPROVED TARGET**, chưa phải active runtime database
được quan sát trên main. B4 không cho phép provision/cutover hoặc áp dụng
migration trong task tài liệu này. Task không quyết định công nghệ SAG.

## 4. Actors, use cases và phạm vi chưa thể đóng băng

Role vocabulary `ADMIN`, `TEAM_LEADER`, `MEMBER` và platform actor
`PLATFORM_OPERATOR` đã có baseline. `SUCCESSOR` là scoped assignment, không
phải role mới. Tuy nhiên, quyền Task theo từng actor vẫn **UNKNOWN** ở mức
implementation contract:

- UC-TM-01–07 và UC-TM-10 trong S3 đề xuất list/create/detail/update/assign/
  transition/search/history. Chưa tự coi tất cả là V1 P0 đã được duyệt.
- Work Note linking và Handover có boundary được duyệt ở B5–B6; DTO, quyền,
  tập task đủ điều kiện và failure semantics chi tiết còn cần chốt.
- UC-TM-11 Agent rewrite, Kanban, subtask và các tiện ích khác có proposal
  scope riêng. Human approval boundary đã duyệt không đồng nghĩa tính năng
  rewrite hoặc Kanban thuộc V1 đã được cam kết.
- Không mở rộng Jira sync/import, task-to-SAG indexing, repo/cluster mới hoặc
  Agent tự ghi Task: các lựa chọn này trái B1–B7. Các loại bỏ/hoãn khác trong
  bảng MVP của S3 còn thuộc proposal scope cần review.

## 5. Danh sách quyết định cần chốt

Người có thẩm quyền product/architecture phê duyệt và ghi nguồn quyết định;
Phúc chuẩn bị và tổng hợp theo owner của DATN-93. Chưa xác minh người phê
duyệt cụ thể cho từng nhóm; Reporter trên Jira không tự chứng minh quyền duyệt.

| ID | Trạng thái và câu hỏi quyết định | Nguồn proposal/evidence | Subtask | Công việc phụ thuộc |
| --- | --- | --- | --- | --- |
| Q1 | **UNKNOWN:** V1 bắt buộc những UC nào trong UC-TM-01–11? List/create/detail là slice đầu hay cần assignment, transitions và history ngay? Kanban/subtask/Agent rewrite có thuộc V1 không? | S3 mục 3–7 | DATN-105 | Toàn bộ kế hoạch BE/FE và acceptance scope |
| Q2 | **UNKNOWN:** Task thuộc đúng một Project? `teamId` có tùy chọn và tối đa một Team? Điều kiện tham chiếu Organization/Project/Team và assignee là gì khi inactive hoặc bị removal? | S3 câu 1–3; S4 mục 2–3; B8 | DATN-107, DATN-109 | DATN-95 schema, constraints và scoped queries |
| Q3 | **UNKNOWN:** Chốt identifier, từng field type/required/nullability/default/limit, enum priority/type, field server-owned và editable; ngày hạn là date-only hay timestamp và theo timezone nào? | S3 mục field, câu 6–7, 18; S4 mục 3 | DATN-107 | DATN-95, DTO/validation, UI form |
| Q4 | **UNKNOWN:** Bộ state, transition matrix, actor/guard/reason cho mỗi cạnh, initial/terminal state và reopen/cancel semantics chính thức là gì? | S3 mục trạng thái, câu 4–5, 10–11; S4 mục 3 | DATN-108 | DATN-94, DATN-100 và data/history |
| Q5 | **UNKNOWN:** Actor nào list/read/create/update/assign/transition/cancel/history? Creator, assignee, Project Membership, Team Membership, successor và ACL kết hợp thế nào; quyền bị thu hồi giữa authorize và write xử lý ra sao? | S5 Task policy, S6; B8 | DATN-109 | Task authorization và cross-scope/concurrency tests |
| Q6 | **UNKNOWN:** Chốt method/path/version, trusted identity/context propagation, request/response DTO, nullable semantics, list/search/filter/sort/pagination, errors và 403/404 disclosure policy trong Task OpenAPI nào? | S2 đoạn sau Service setup proposal; S3 UC-TM-01–07 | DATN-110 | DATN-96 và các Task API/BFF/FE phụ thuộc |
| Q7 | **UNKNOWN:** Version token/CAS, stale response, operation-ID scope/uniqueness, payload mismatch, retry/replay response, expiry và Handover compensation cụ thể là gì? | S2 Decision 6–7; S4 mục 4 | DATN-108, DATN-110 | DATN-94, assignment/lifecycle, transaction/migration tests |
| Q8 | **UNKNOWN:** Chốt event vocabulary, field types, safe before/after/projection, history visibility/order/pagination và retention. Có gửi compliance audit vào `continuum_audit` không; nếu có thì contract/atomicity nào áp dụng? | S2 Decision 7; S4 mục 3–4; S7 | DATN-110 | DATN-95, history API và audit integration |
| Q9 | **UNKNOWN:** Có consumer async cần outbox trong V1 không? Nếu có, event schema, consumer, delivery/retry/dedup/retention là gì? Port, queue names, health/config/timeouts và việc giữ hoặc loại Jira runtime được owner deployment chốt ở đâu? | S2 Service setup proposal, Consequences; S4 mục 4 | DATN-106, DATN-110 | DATN-96 và outbox/deployment khi được chấp thuận |

Không thay thế Q3–Q4 bằng các giá trị proposal `ObjectId`, `TODO`,
`IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`, `LOW/MEDIUM/HIGH` hoặc default
`TODO/MEDIUM`. Chúng cần quyết định tương ứng trước khi tạo schema, test fixture
hoặc UI enum như requirement. Tương tự, không dùng lỗi/pagination của IAM để
tự quyết contract Task, hoặc coi port đề xuất `3009` là port đã được chốt.

## 6. Evidence runtime trên main và chênh lệch cần xử lý

| Repo | SHA được đối chiếu local và remote main ngày 04/10/2026 |
| --- | --- |
| Document | `654c8b16ecc7c3becdfd29ee2a7fa6ef7f437755` |
| DATN-BE | `56036d13ed86f5db47ba7cbcb02256f02eab80ae` |
| DATN-FE | `c57c01455e7a47f4865485d00ded2c05f7b3b203` |
| sag-laya-integration | `82a8f80bf728ad1c56b08628d4eb392bf55bcb29` |

- **FACT:** DATN-BE `src/services` có IAM, Capture, Jira, Lifecycle, Chat,
  Handover, Ingestion, Notification; chưa có thư mục Task service. Tìm trong
  source/Gateway và OpenAPI không thấy Task API; `follow_up_tasks` trong
  Handover không chứng minh Task canonical service/contract đã tồn tại.
- **FACT:** [database-names.ts tại SHA kiểm tra](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/src/common/mongodb/database-names.ts)
  không có `continuum_task` trong SERVICE_DATABASES. Inventory gồm
  `continuum_jira`; không xóa/đổi owner Jira chỉ vì Task MVP không dùng Jira sync.
- **FACT:** [OpenAPI README tại SHA kiểm tra](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/docs/openapi/README.md)
  và `iam-v1.openapi.json` mô tả IAM; có resource còn proposal. Đây không phải
  approved Task contract.
- **FACT:** BE/FE AGENTS vẫn mô tả backend modular monolith. S2 yêu cầu reconcile
  guide trong PR ứng dụng liên quan trước khi triển khai Task service. Báo cáo
  này ghi chênh lệch; không sửa guide hoặc deployment thay owner ứng dụng.
- **FACT:** DATN-105–110 đều To Do, Unassigned, chưa có description hoặc comment
  hiển thị bổ sung quyết định khi mở từng ticket. Chưa có bằng chứng phê duyệt
  field/state/API trong các ticket đã đọc; không suy ra rằng quyết định không
  thể tồn tại ở nguồn khác chưa được cung cấp.
- **Nguồn còn thiếu:** S7 dẫn workspace ADR-003/DEC-011; không tìm thấy file
  ADR-003/SPEC-001 riêng trong bốn checkout. Trước implementation persistence,
  owner cần cung cấp bản authority hiện hành hoặc repository copy đã duyệt.
  Link external workspace trong AGENTDB.md local không chứng minh đã đọc được
  nội dung nguồn đó. Baseline database-per-service đang được ghi rõ ở S7 và BE
  guide, nhưng không dùng chúng để đoán policy migration/cutover còn thiếu.

## 7. Mapping nghiệm thu và điều kiện mở chặn

| Subtask | Kết quả trong báo cáo | Bằng chứng cần bổ sung để đóng quyết định |
| --- | --- | --- |
| DATN-105 | Actor/use-case/scope được phân biệt baseline và proposal; Q1 | V1 UC/scope được product owner duyệt |
| DATN-106 | Boundary B1–B7 có nguồn; target/runtime khác nhau; Q9 | Xác nhận runtime contract/owner, không tự coi target đã chạy |
| DATN-107 | Field/relationship chưa được tự phê duyệt; Q2–Q3 | Data dictionary và references/constraints đã chốt |
| DATN-108 | Lifecycle/version/idempotency gaps Q4, Q7 | Transition matrix và operation/conflict contract được duyệt |
| DATN-109 | Governance B8; action matrix gaps Q2, Q5 | Actor/scope/ACL/deny/concurrency matrix được duyệt |
| DATN-110 | API/audit/history/outbox gaps Q6–Q9 | Task OpenAPI, event/history và unresolved-item decisions có authority |

Contract closure cần lưu: decision ID, người duyệt, thời điểm, owning document/
contract revision, nội dung quyết định, các câu Q được đóng và tests/acceptance
criteria truy vết. Nếu chỉ ghi proposal hoặc chưa trả lời đủ field/matrix/DTO,
giữ phần phụ thuộc ở UNKNOWN. Phê duyệt một nhóm không mở chặn nhóm khác.

Sau phê duyệt, kiểm tra các artifact phụ thuộc nhất quán và đã vào `main` theo
workflow, rồi mỗi DB/BE/FE task tạo branch riêng từ `origin/main` mới nhất.
Thay đổi tài liệu trong architecture/database-design/deploy phải tuân thủ
quy trình frozen baseline; không sửa baseline để hợp thức hóa implementation.

**Phạm vi bàn giao:** Chỉ tài liệu readiness và link trong README. Không có
schema/API/UI/runtime/migration/data change; không provision database, seed,
cutover hoặc gửi thông báo team. Báo cáo không tự chuyển Jira/subtask thành
Done hoặc xác nhận DATN-93 đã có approved contract.
