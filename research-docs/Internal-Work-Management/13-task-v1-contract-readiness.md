# DATN-93 — Task Management V1: working contract và quyết định còn thiếu

**Trạng thái:** Working contract tổng hợp phần baseline đã duyệt và phần
UNKNOWN; chưa phải Task V1 contract được phê duyệt đầy đủ.
**Revision:** R2 — tiếp tục bản báo cáo tại commit `0ec12fc`.
**Ngày kiểm tra lại:** 04/10/2026 (Asia/Saigon).
**Task owner:** Nguyen Hong Phuc.

Mục tiêu của [DATN-93](https://trankimthang0207.atlassian.net/browse/DATN-93)
là có contract được duyệt **hoặc danh sách blocker cụ thể**. Báo cáo này thực
hiện phương án thứ hai: phân biệt quyết định hiện hành với proposal, đặt câu
hỏi có thể review và ánh xạ chúng tới công việc phụ thuộc. Việc ưu tiên ticket,
tạo tài liệu hoặc merge tài liệu báo cáo không tự phê duyệt product policy.
R2 đối chiếu từng Q1–Q9 với quyết định hiện hành, bổ sung contract checklist
và acceptance traceability; không đóng một Q chỉ vì đã biết một phần boundary.

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
| S10 | BE [Project creator Member bootstrap](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/docs/decisions/project-creator-member-bootstrap-v1.md), Decision; [Project Foundation read policy](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/docs/decisions/project-foundation-read-mvp.md), Contract used; [Project Access & Visibility V1](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/docs/decisions/project-access-visibility-v1.md), role mapping, Visibility, Membership operations và Tests and boundaries | Quyết định có nhãn requester-approved/accepted trên main; quyền creator Member, giới hạn metadata và thu hồi Project access; không phải Task action matrix |
| S11 | [MVP scope](../01_MVP_SCOPE.md), mục 6.2; [Daily workflow](../03_DAILY_WORKFLOW_AND_JIRA_SYNC.md), Status và mục 2–3; [Graduation specification](../Continuum_AI_Graduation_Project_Specification_v1.0.docx.md), scope amendment và FR-24 | Xác minh Task feature scope chi tiết vẫn là proposal; statement field/state ở workflow không tự đóng Q2–Q4 |
| S12 | [DATN-94](https://trankimthang0207.atlassian.net/browse/DATN-94), [DATN-95](https://trankimthang0207.atlassian.net/browse/DATN-95), [DATN-96](https://trankimthang0207.atlassian.net/browse/DATN-96), descriptions và linked work items đọc lại ngày 04/10/2026 | Downstream acceptance criteria và dependency gate; nghiệm thu trong ticket không chứng minh implementation đã đạt |

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
| B9 | Project creator được bootstrap thành ordinary MEMBER, không thành Leader/owner/Team; documented member rights gồm tạo/sửa Task khi API sẵn sàng. Leader Tổng ánh xạ ADMIN ở Organization, Leader Project ánh xạ TEAM_LEADER ở Project; không thêm role code | S10; creator policy dated 30/09, reaffirmed 04/10/2026; Project Access dated 02/10/2026 |
| B10 | PUBLIC Project và Organization ADMIN metadata access không cấp quyền Task/content. Project Membership removal thành INACTIVE thu hồi effective Project access, giữ records; mọi authorization ở Project scope vẫn cần ACTIVE ProjectMembership | S10 Project Foundation/Project Access; không quyết định tự clear/transfer assignee hoặc xóa Task |

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

B9 xác nhận creator có quyền thành viên tạo/sửa Task khi API có mặt; không
chốt họ được sửa mọi Task, sửa field nào, hay bỏ qua Team scope/ACL. B10 chốt
access revocation ở Project boundary; cách xử lý Task đang giao cho người bị
removal vẫn thuộc Q2/Q5/Q7. Không áp dụng Project 404, pagination hoặc IAM
audit collection cho Task chỉ vì các contract đó đã được duyệt cho Project.

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
| Q5 | **UNKNOWN ở mức action contract:** B9 xác nhận quyền thành viên tạo/sửa Task cho Project creator, B8/B10 giới hạn scope/ACL. Chốt actor nào list/read/create/update/assign/transition/cancel/history, quyền creator/assignee/successor, field được sửa, Project/Team Membership và thu hồi giữa authorize/write như thế nào? | S5 Task policy, S6, S10; B8–B10 | DATN-109 | Task authorization và cross-scope/concurrency tests |
| Q6 | **UNKNOWN:** Chốt method/path/version, trusted identity/context propagation, request/response DTO, nullable semantics, list/search/filter/sort/pagination, errors và 403/404 disclosure policy trong Task OpenAPI nào? | S2 đoạn sau Service setup proposal; S3 UC-TM-01–07 | DATN-110 | DATN-96 và các Task API/BFF/FE phụ thuộc |
| Q7 | **UNKNOWN:** Version token/CAS, stale response, operation-ID scope/uniqueness, payload mismatch, retry/replay response, expiry và Handover compensation cụ thể là gì? | S2 Decision 6–7; S4 mục 4 | DATN-108, DATN-110 | DATN-94, assignment/lifecycle, transaction/migration tests |
| Q8 | **UNKNOWN:** Chốt event vocabulary, field types, safe before/after/projection, history visibility/order/pagination và retention. Có gửi compliance audit vào `continuum_audit` không; nếu có thì contract/atomicity nào áp dụng? | S2 Decision 7; S4 mục 3–4; S7 | DATN-110 | DATN-95, history API và audit integration |
| Q9 | **UNKNOWN:** Có consumer async cần outbox trong V1 không? Nếu có, event schema, consumer, delivery/retry/dedup/retention là gì? Port, queue names, health/config/timeouts và việc giữ hoặc loại Jira runtime được owner deployment chốt ở đâu? | S2 Service setup proposal, Consequences; S4 mục 4 | DATN-106, DATN-110 | DATN-96 và outbox/deployment khi được chấp thuận |

Không thay thế Q3–Q4 bằng các giá trị proposal `ObjectId`, `TODO`,
`IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`, `LOW/MEDIUM/HIGH` hoặc default
`TODO/MEDIUM`. Chúng cần quyết định tương ứng trước khi tạo schema, test fixture
hoặc UI enum như requirement. Tương tự, không dùng lỗi/pagination của IAM để
tự quyết contract Task, hoặc coi port đề xuất `3009` là port đã được chốt.

### 5.1. Kết quả đối chiếu Q1–Q9 ở revision R2

**Chưa có Q nào được đóng đầy đủ** bằng bằng chứng đã đọc. Bảng dưới ghi
phần đã biết và artifact còn thiếu, không thay đổi trạng thái Jira. Owner
tổng hợp là Phúc; người duyệt product/architecture từng Q vẫn **UNKNOWN**.
Danh là owner implementation DATN-95/96, không tự suy ra là người phê duyệt.

| Q | Phần có authority | Phần còn thiếu để đóng quyết định |
| --- | --- | --- |
| Q1 | B1, B5–B7; S11 xác nhận mục tiêu task/capture/handover | Release scope: từng UC-TM-01–11 được included/deferred/excluded, slice và acceptance cụ thể; quyết định riêng cho Kanban, subtask, rewrite, comment/file/notification/report |
| Q2 | B3, B5–B6, B8/B10; Project thuộc Organization, Team thuộc Project (S6 mục 4.1) | Task Project/Team/assignee cardinality; Work Note link cardinality; reference eligibility; assignment cleanup/transfer khi membership hoặc parent lifecycle đổi; successor eligibility/access duration |
| Q3 | B1 xác định MongoDB; B7 chốt provenance intent | Approved data dictionary cho identifier và từng Task field: presence, type, required/null/default/limit, enum, server-owned/editable; due-date/timezone semantics; không lấy ObjectId ở S11 thay phê duyệt field-level |
| Q4 | B4 yêu cầu mutation/history atomic; B5 tách Task khỏi verified knowledge | Initial/terminal state, mọi enabled edge, actor/guard/reason; cancel/reopen; Task state nào đủ điều kiện Handover; Work Note/evidence có phải completion guard không |
| Q5 | B8–B10, actor vocabulary và scoped assignment; S5 explicit deny precedence | Action × actor × scope × resource matrix, exact permission codes; creator/assignee/teamless Task; read/search/history/successor projection; reauthorization/fence khi revoke trong mutation |
| Q6 | B3 yêu cầu existing BFF/Gateway và authenticated service contract | Approved Task OpenAPI cho từng operation được Q1 duyệt: method/path/version, transport/trust, DTO và nullable semantics, list controls, response/errors, 403/404 disclosure và unavailable upstream |
| Q7 | B6 yêu cầu operation ID/idempotent Handover command và retry/compensation; B7 task version provenance | Version/CAS token, stale/conflict contract; key scope/uniqueness/expiry, duplicate vs payload mismatch, concurrent/replay response; failure/compensation và reconciliation ownership |
| Q8 | B4/B7: append-only atomic history; actor identity/type, event/source, changed-field metadata, version/time, operation/correlation, Agent provenance; no full prompt/raw context | Exact event names/field shape/nullability; safe before/after policy, history projection/order/pagination/retention; Task compliance audit sink và atomicity. Project audit decision trong S10 chỉ áp dụng Project |
| Q9 | B2–B4, S2 Decision 4–5/7: process riêng, hybrid HTTP/Redis, reuse infra, conditional outbox/dedup | Explicit V1 consumer/no-consumer decision; nếu có: delivery schema/retry/dedup/retention. Port, queues, health/config/timeouts và Jira runtime reconciliation có owner quyết định |

### 5.2. Những statement phải đọc cùng nhãn authority

- S5 có status “Accepted MVP authorization baseline”, nhưng mục 6 nói rõ
  Task action codes/matrix và các rule Member/Team Leader/status là pending
  approval. Không dùng nhãn chung của file để duyệt những dòng này.
- S4 mở đầu đánh dấu field/cardinality/history proposal. S11 Daily workflow
  có statement ObjectId và tập state Handover, nhưng Status/mục 2 chuyển
  detailed field/state review về S3. Giữ chúng ở Q2–Q4; ghi nhận chênh lệch
  cách diễn đạt, không lấy statement đứng riêng làm quyết định mới.
- S2 Decision 7 đã chốt metadata intent của history, trong khi S4 đề xuất
  `operationId?`/`correlationId?`. Q8 phải chốt exact representation và trường
  hợp presence/nullability phù hợp S2; không âm thầm chọn nullable hoặc optional.
- Accepted Project public-read/404/audit trong S10 có scope giới hạn Project.
  Task quyền đọc, concealment và compliance sink vẫn cần Q5/Q6/Q8.

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
- **FACT (R2):** Đã fetch cả bốn repo; main SHA không đổi so với bảng trên.
  Nhánh DATN-93 local/remote cùng commit `0ec12fc` khi bắt đầu, working tree
  sạch; tiếp tục nhánh theo yêu cầu người dùng, không tạo nhánh task mới.
  DATN-93/94/95/96 và DATN-105–110 vẫn To Do khi đọc lại; Comments hiển thị
  chưa có phê duyệt bổ sung. DATN-95/96 cùng chặn DATN-97; DATN-94 chặn DATN-100.
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
| DATN-109 | Governance B8–B10; quyền creator Member có căn cứ nhưng action matrix vẫn thiếu Q2, Q5 | Actor/scope/ACL/deny/concurrency matrix được duyệt |
| DATN-110 | API/audit/history/outbox gaps Q6–Q9 | Task OpenAPI, event/history và unresolved-item decisions có authority |

Contract closure cần lưu: decision ID, người duyệt, thời điểm, owning document/
contract revision, nội dung quyết định, các câu Q được đóng và tests/acceptance
criteria truy vết. Nếu chỉ ghi proposal hoặc chưa trả lời đủ field/matrix/DTO,
giữ phần phụ thuộc ở UNKNOWN. Phê duyệt một nhóm không mở chặn nhóm khác.

Sau phê duyệt, kiểm tra các artifact phụ thuộc nhất quán và đã vào `main` theo
workflow, rồi mỗi DB/BE/FE task tạo branch riêng từ `origin/main` mới nhất.
Thay đổi tài liệu trong architecture/database-design/deploy phải tuân thủ
quy trình frozen baseline; không sửa baseline để hợp thức hóa implementation.

## 8. Contract checklist còn thiếu cho implementation

Đây là cấu trúc cần người duyệt điền theo Q1–Q9, không phải DTO/schema hay
bộ endpoint mới. Mỗi phần chỉ được dùng cho operation đã được Q1 duyệt.

| Contract surface | Baseline áp dụng | Giá trị chi tiết hiện tại / nội dung cần cung cấp |
| --- | --- | --- |
| Task data dictionary | B1/B4, scoped authority B8 | **UNKNOWN (Q2/Q3).** Checklist field candidates từ S3/S4: identifier, organization/project/team, title/description, status/priority/type, creator/assignee, due date, timestamps/version. Presence của từng candidate cũng cần duyệt; không chỉ type/default |
| Reference rules | B3/B5/B6/B8/B10 | **UNKNOWN (Q2/Q5).** Mỗi reference cần owner, cardinality, eligible target, scope validation và hành vi khi target mất quyền/inactive/archived; không tạo cascade hoặc copy Task |
| Lifecycle table | B4/B5 | **UNKNOWN (Q4/Q5/Q7).** Mỗi cạnh cần from/to, command, actor, membership/ACL guard, reason semantics, precondition/version, event và denial/conflict result. Chưa có state/edge nào được báo cáo này authorize |
| Authorization table | B8–B10 | **UNKNOWN (Q5).** Mỗi action cần actor/assignment, exact permission, parent membership, Team/resource ACL, explicit deny, visible fields và stale-authorization handling. Quyền tạo/sửa của creator Member phải reconcile cùng matrix |
| HTTP operation table / OpenAPI | B3/B6/B7 | **UNKNOWN (Q6).** Exact BFF/Gateway/internal method/path, authenticated caller context, request/response/error schemas, projection, pagination/filter/sort/search limits; transport session/header/token và error code chưa chốt |
| Mutation/replay table | B4/B6/B7 | **UNKNOWN (Q7).** Version compare/update, operation key scope, replay/mismatch/concurrent outcomes, expiry và retry/compensation. Atomic history không tự xác định status code hoặc replay payload |
| History/audit table | B4/B7 | Metadata intent **APPROVED**; field-level/event/visibility/retention/sink **UNKNOWN (Q8)**. Phân biệt domain `task_events` với compliance audit và event delivery; không copy IAM audit shape thành Task shape |
| Runtime/event contract | B2–B4 | Boundary **APPROVED TARGET**; exact runtime values/consumer decision **UNKNOWN (Q9)**. Không mặc định bật outbox, không xem bootstrap pattern là bằng chứng health/config/route đã chạy |

Decision closure ghi cho **từng item**: Q/sub-item, quyết định chính xác,
nguồn + revision/commit, người/authority duyệt, ngày, owning artifact, các
acceptance cases bị ảnh hưởng và những item vẫn UNKNOWN. Phê duyệt “ADR-010”
hoặc “dùng proposal hiện tại” không đủ để suy ra field/matrix/DTO chưa được
ghi rõ. Khi chỉ duyệt một phần, ghi PARTIAL cùng phần còn thiếu.

## 9. Acceptance traceability và downstream gate

### 9.1. DATN-93

| Acceptance criterion đọc từ Jira | Artifact trong revision R2 | Kết luận |
| --- | --- | --- |
| AC1: authority tách khỏi research/inference | Mục 2–4, B1–B10; mục 5.1–5.2 đối chiếu từng Q | Có source/authority map; không tạo phê duyệt mới |
| AC2: fields/transitions/API/authorization/audit explicit hoặc UNKNOWN có câu hỏi | Q1–Q9 và contract surfaces ở mục 8 | Đã mô tả blocker cụ thể; detailed implementation contract vẫn UNKNOWN |
| AC3: downstream chỉ dùng approved behavior, acceptance truy vết | Mục 9.2–9.3 | Có constraint/check mapping; chưa có implementation/test evidence hoặc nghiệm thu bởi team |

Expected result được chuẩn bị là **precise blocker list + approved baseline
constraints**, chưa phải approved full contract. Kết quả này cần owner/team
review; không tự đổi Jira/subtask Done hoặc gỡ dependency link.

### 9.2. Các ticket bị chặn trực tiếp

| Ticket / owner hiện tại | AC theo ticket, tóm tắt | Authority và phần cần đóng trước implementation |
| --- | --- | --- |
| DATN-94 / Phúc | Mọi transition/actor có trong D-01 approved contract; invalid/unauthorized/unapproved bị từ chối/disabled; test allowed/denied/stale/idempotent | B4/B7/B8–B10 giới hạn boundary; Q4/Q5/Q7 quyết định matrix và conflict/replay, Q6/Q8 cho error/event contract tương ứng. Tài liệu này chưa mở chặn state machine |
| DATN-95 / Danh | Data shape/owner approved; constraints/atomicity theo use case, không speculative field hoặc legacy fallback; disposable index/persistence/failure tests | B4 chốt ownership/atomic history; Q1–Q3/Q4/Q5/Q7/Q8/Q9 phần ảnh hưởng persistence, query/index/uniqueness rationale và ADR-003/SPEC-001 hiện hành. Chưa provision/init/migrate `continuum_task` |
| DATN-96 / Danh | Runtime chọn `continuum_task`, config sai fail-fast; dùng existing BFF/Gateway; integration/bootstrap tests cho routing/trust/health/failure | B2/B3/B4 và AC Jira chốt runtime boundary; Q6/Q9 chốt exact routing/config/health/timeouts/errors, Q5/Q7 cho command contract được expose; reconcile BE/FE guides và authority persistence. Chưa coi route/port proposal là build-ready |

Việc nào cần artifact dependency đã merge thì vẫn theo `AI_WORKFLOW.md`:
đọc lại Git/Jira, đợi dependency vào main, tạo branch mới từ `origin/main`.
Blocker list của DATN-93 được review/merge cũng không thay approval các Q.

### 9.3. Scenarios dùng để review contract, chưa phải tests đã chạy

| Case | Điều cần kiểm chứng khi contract/implementation có mặt | Căn cứ và chi tiết còn chờ |
| --- | --- | --- |
| AT-01 | Client chọn/đoán Organization/Project/Team ID không tạo quyền; thiếu ACTIVE Organization Membership hoặc Project access đã thu hồi không được đọc/ghi Task thuộc scope đó | B8/B10; Q5/Q6 chốt transport/error và mutation fence |
| AT-02 | ADMIN/PLATFORM_OPERATOR và người chỉ thấy PUBLIC Project metadata không tự đọc Task; creator Member không được bootstrap thành Leader | B8–B10; Q5 chốt readable/mutable resource matrix |
| AT-03 | Task mutation và history cùng commit hoặc cùng rollback; không có direct Task collection access từ consumers | B3/B4; Q3/Q7/Q8 chốt persisted shape và conflict/failure outputs; DATN-95 cần disposable replica-set evidence |
| AT-04 | Handover command lặp không tạo tác dụng lặp; payload khác/concurrent/stale có kết quả xác định; failure giữa Task và Handover có recovery owner | B6; Q7 chốt key/response/expiry/compensation, không tự chọn behavior |
| AT-05 | Agent chỉ nhận context được phép; proposal chưa được người có quyền xác nhận không mutate; event giữ user + Agent/proposal provenance và tránh full prompt/raw context | B7; Q1/Q5/Q6/Q8 chốt feature scope/permission/representation |
| AT-06 | Optional Work Note link được Task API kiểm tra scope; Task text/status không thành verified knowledge hoặc standalone SAG source; Jira không cần cho Task lifecycle | B1/B3/B5; Q2/Q6 chốt cardinality và lỗi link |
| AT-07 | Mọi enabled transition có decision record; invalid/unauthorized/stale/idempotent cases có expected result; không thêm state/edge từ proposal | DATN-94 AC; Q4/Q5/Q6/Q7/Q8 |
| AT-08 | Runtime qua existing BFF/Gateway, database đúng owner/config fail-fast; health, trusted correlation và upstream timeout/failure quan sát được | B2/B3/B4, DATN-96 AC; Q6/Q9 chốt exact values và mappings |
| AT-09 | Nếu Q9 duyệt async consumer, outbox cùng mutation/history transaction, relay sau commit và consumer dedup event ID | B4/S2 Decision 7; Q8/Q9 chốt event/delivery semantics; không bật nhánh scenario này khi consumer chưa được duyệt |

## 10. Phạm vi bàn giao R2

Chỉ tài liệu working contract/readiness và link trong README. Không có
schema/API/UI/runtime/migration/data change; không provision database, seed,
cutover hoặc gửi thông báo team. Báo cáo không tự chuyển Jira/subtask thành
Done hoặc xác nhận DATN-93 đã có approved contract.
