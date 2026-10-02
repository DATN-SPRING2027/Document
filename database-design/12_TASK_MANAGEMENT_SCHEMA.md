# Continuum AI — Thiết kế lưu trữ Task nội bộ

> **Trạng thái:** Task Service/repository boundary đã chốt; field/cardinality/history dưới đây là đề xuất chờ duyệt Use Case/API.
>
> **Ngày quyết định:** 2026-10-01
>
> **Service sở hữu:** Task Service (NestJS, triển khai độc lập; source trong repo DATN_BE hiện có)
> **Database engine:** MongoDB 7.0 với Mongoose; database logical riêng `continuum_task` trên replica set hiện có. Không tạo repo ManageWork hay MongoDB cluster vật lý mới.

## 1. Quyết định và phạm vi

Continuum là nguồn chính thức và duy nhất cho vòng đời task DATN trong MVP. Client tạo, đọc, cập nhật, gán người phụ trách và đổi trạng thái task qua API Gateway rồi tới Task Service. Bản ghi canonical thuộc database `continuum_task`. Jira không tham gia tạo, đồng bộ hoặc làm bản sao task. Task Service có process và cấu hình triển khai riêng nhưng dùng chung repo BE, MongoDB replica set và Redis/BullMQ hiện có.

Ranh giới đã chốt: Task Service là đường đọc/ghi duy nhất cho task canonical; Gateway là lối vào từ FE, còn service-to-service truy cập qua contract nội bộ. Các service khác không đọc/ghi database của Task. Các chi tiết field-level dưới đây là đề xuất đồng bộ với [Task Use Cases](../research-docs/Internal-Work-Management/12-continuum-task-management-use-cases.md), chưa phải schema đã được phê duyệt hoặc triển khai.

## 2. Ràng buộc dữ liệu

- Mọi task phải có `organizationId` và đúng một `projectId`; đề xuất `teamId` tùy chọn, tối đa một team trong project. Task API phải kiểm tra quyền/scope ở mỗi thao tác đọc/ghi.
- Task Service API là đường ghi duy nhất cho lifecycle task. Các service khác chỉ đọc/gửi command qua API hoặc giữ logical reference; không tạo mirror writable ở Work Note, Handover hay SAG.
- Work Note giữ `taskId` tùy chọn: mỗi Work Note gắn tối đa một task, một task có thể được tham chiếu bởi nhiều Work Note. Khi tạo/cập nhật liên kết, Continuum xác thực task tồn tại và caller có quyền truy cập task. Work Note không liên kết task vẫn hợp lệ.
- Handover giữ `taskId` cho task còn mở do Team Leader chọn. Lệnh giao task gọi Task Service API để cập nhật assignee canonical sang successor; Handover lưu recipient/acknowledgement của gói và logical reference, không lưu bản task mutable thứ hai. Hai bước dùng `operationId` idempotent và retry/compensation vì Task và Handover sở hữu database riêng.
- Task, title/description/status/assignee không được gửi như nguồn độc lập vào SAG. Đề xuất chỉ Work Note đã được tác giả xác nhận và evidence/source đủ điều kiện, còn được phép theo ACL, mới đủ điều kiện retrieval/index.
- Quyền hiện hành phải được kiểm tra trước khi trả content hoặc xây LLM context. Khi ACL thu hồi, chặn truy xuất ngay; de-index/refresh chạy nền có thể retry nhưng không được mở quyền lại.
- `tasks`, `task_events` và `outbox_events` (nếu bật phát sự kiện bền vững) là collection do Task Service sở hữu trong database logical `continuum_task`. Dùng transaction trên replica set hiện có để ghi task mutation cùng audit event/outbox; Handover không truy cập trực tiếp database/collection này.

## 3. Thành phần dự kiến

| Thành phần | Ranh giới đã chốt | Chi tiết còn mở |
|---|---|---|
| `tasks` | Collection canonical do Task Service sở hữu trong `continuum_task` | Field proposal: `organizationId`, `projectId`, `teamId?`, `title`, `description?`, `status`, `priority`, `assigneeId?`, `createdBy`, `dueDate?`, `createdAt`, `updatedAt`, `version` |
| `task_events` | Append-only business history trong cùng Task database; không nhúng mảng history không giới hạn vào task | Field proposal: `taskId`, scope IDs, `actorId`, `actorType`, `source`, `eventType`, `changedFields`, safe before/after values, `taskVersion`, `occurredAt`, `operationId?`, `correlationId?` |
| `outbox_events` | Durable delivery record written in the same transaction as a task mutation when downstream event delivery is required | Event ID/type, aggregate ID/version, safe payload or references, created/published timestamps, retry state |
| Work Note link | Optional logical `taskId`; quan hệ 0..1 task per Work Note, 0..N Work Notes per task | ID là Mongo `ObjectId`; xử lý hiển thị khi task `CANCELLED` hoặc caller mất quyền |
| Handover link | `taskId` trên item do Team Leader chọn; Task API cập nhật assignee; Handover lưu recipient và acknowledgement | `operationId`, trạng thái retry/compensation và chính sách giữ read-only package |
| SAG mapping | Chỉ mapping/index nguồn Work Note/evidence được phép; không có source type Task | Vector engine follows the separate SAG storage decision; Task Service does not select or change it |

### Field, status và index đề xuất

- Task type duy nhất: `TASK`; không có Epic/Story/Bug trong MVP.
- `title`, `organizationId`, `projectId`, `createdBy` là required. `status` mặc định `TODO`; `priority` mặc định `MEDIUM`. `teamId`, `description`, `assigneeId`, `dueDate` là optional.
- Status cố định: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`. `DONE` có thể trở lại `IN_PROGRESS` nếu người phụ trách/Team Leader ghi lý do; `CANCELLED` không được xóa cứng hoặc mở lại trong MVP.
- Đề xuất compound indexes: `(organizationId, projectId, status, updatedAt)`, `(organizationId, projectId, assigneeId, status)`, `(organizationId, projectId, teamId, dueDate)`. Index cuối cần phù hợp filter/query sau khi API contract được duyệt.
- Đề xuất event history ghi actor/time/source và field đã đổi cho status, assignee, due date, priority, team, title/description, cancel/reopen. Ghi riêng user actor và Agent/proposal identity khi có AI hỗ trợ. Không lưu task snapshot đầy đủ hoặc full prompt/raw AI context trong event. Nếu cần lưu bản nháp AI rewrite, giữ nó như proposal/version riêng có ACL, retention và human approval; chỉ bản được duyệt mới cập nhật task canonical.
- Dùng Mongo `ObjectId` làm task identifier trong MVP; không tạo sequence/task key kiểu Jira. Không bulk import task từ ManageWork/Jira trong MVP.

## 4. Các quyết định cần hoàn tất trước khi triển khai

1. Duyệt các khuyến nghị trong Use Case doc trước khi biến field/status/permission proposal thành requirement.
2. Khi Task service được triển khai, cấu hình `SERVICE_DATABASE=continuum_task` trên MongoDB replica set hiện có; không tạo MongoDB cluster vật lý mới. `continuum_task` chưa thuộc active DATN-BE runtime inventory. Reconcile việc sở hữu service/database với workspace ADR-003 và lập dry-run migration riêng trước khi chuyển dữ liệu.
3. Chốt response/DTO và cách trả lỗi khi task bị hủy hoặc caller không còn quyền xem.
4. Chốt retention cho `task_events` và cách đồng bộ domain event sang compliance audit nếu cần.
5. Chốt retry, idempotency và retention cho outbox/event consumers. Không copy task records vào SAG; SAG storage được quyết định riêng và không bị thay đổi bởi Task Service.

Tham chiếu: [ADR-009](../research-tech/ADR-009-internal-task-source-and-mongodb.md), [ADR-010](../research-tech/ADR-010-task-service-in-existing-repositories.md), [Task-management Use Cases](../research-docs/Internal-Work-Management/12-continuum-task-management-use-cases.md), [permission baseline](../research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md), [daily workflow](../research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md), [Work Note schema](02_SVC_CAPTURE_SCHEMA.md), [Handover schema](06_SVC_HANDOVER_SCHEMA.md).
