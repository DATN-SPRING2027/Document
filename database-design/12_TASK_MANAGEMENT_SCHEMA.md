# Continuum AI — Thiết kế lưu trữ Task nội bộ

> **Trạng thái:** Nguồn task và MongoDB đã chốt; field/cardinality/history dưới đây là đề xuất chờ duyệt Use Case.
>
> **Ngày quyết định:** 2026-10-01
>
> **API sở hữu:** Continuum Task API (NestJS Core)
> **Database engine:** MongoDB 7.0 với Mongoose; dùng operational database đã được duyệt (`continuum_db` theo DEC-011/SPEC-001). Task API sở hữu các collection `tasks` và `task_events`; không tạo database task riêng.

## 1. Quyết định và phạm vi

Continuum là nguồn chính thức và duy nhất cho vòng đời task DATN trong MVP. Client tạo, đọc, cập nhật, gán người phụ trách và đổi trạng thái task qua Continuum Task API. Bản ghi canonical thuộc collection `tasks` trên MongoDB. Jira không tham gia tạo, đồng bộ hoặc làm bản sao task.

Ranh giới đã chốt: Continuum Task API là đường đọc/ghi duy nhất cho task canonical, lưu trên MongoDB; Jira không tham gia task lifecycle trong MVP. Các chi tiết field-level dưới đây là đề xuất đồng bộ với [Task Use Cases](../research-docs/Internal-Work-Management/12-continuum-task-management-use-cases.md), chưa phải schema đã được phê duyệt hoặc triển khai.

## 2. Ràng buộc dữ liệu

- Mọi task phải có `organizationId` và đúng một `projectId`; đề xuất `teamId` tùy chọn, tối đa một team trong project. Task API phải kiểm tra quyền/scope ở mỗi thao tác đọc/ghi.
- Task API là đường ghi duy nhất cho lifecycle task. Các module khác chỉ đọc qua API hoặc giữ logical reference; không tạo mirror writable ở Work Note, Handover hay SAG.
- Work Note giữ `taskId` tùy chọn: mỗi Work Note gắn tối đa một task, một task có thể được tham chiếu bởi nhiều Work Note. Khi tạo/cập nhật liên kết, Continuum xác thực task tồn tại và caller có quyền truy cập task. Work Note không liên kết task vẫn hợp lệ.
- Handover giữ `taskId` cho task còn mở do Team Leader chọn. Lệnh giao task gọi Task API để cập nhật assignee canonical sang successor; Handover lưu recipient/acknowledgement của gói và logical reference, không lưu bản task mutable thứ hai. Hai bước dùng `operationId` idempotent và retry/compensation vì Task và Handover sở hữu dữ liệu riêng.
- Task, title/description/status/assignee không được gửi như nguồn độc lập vào SAG. Đề xuất chỉ Work Note đã được tác giả xác nhận và evidence/source đủ điều kiện, còn được phép theo ACL, mới đủ điều kiện retrieval/index.
- Quyền hiện hành phải được kiểm tra trước khi trả content hoặc xây LLM context. Khi ACL thu hồi, chặn truy xuất ngay; de-index/refresh chạy nền có thể retry nhưng không được mở quyền lại.
- `tasks` và `task_events` là các collection do Task API sở hữu trong operational database `continuum_db` đã được duyệt. Dùng transaction trên replica set hiện có để ghi task mutation và event history cùng nhau; Handover không truy cập trực tiếp database/collection này.

## 3. Thành phần dự kiến

| Thành phần | Ranh giới đã chốt | Chi tiết còn mở |
|---|---|---|
| `tasks` | Collection canonical do Continuum Task API sở hữu trong `continuum_db` | Field proposal: `organizationId`, `projectId`, `teamId?`, `title`, `description?`, `status`, `priority`, `assigneeId?`, `createdBy`, `dueDate?`, `createdAt`, `updatedAt` |
| `task_events` | Append-only history trong cùng operational database; không nhúng mảng history không giới hạn vào task | Field proposal: `taskId`, `organizationId`, `projectId`, `actorId`, `eventType`, `changedFields`, safe before/after values, `occurredAt`, `operationId?` |
| Work Note link | Optional logical `taskId`; quan hệ 0..1 task per Work Note, 0..N Work Notes per task | ID là Mongo `ObjectId`; xử lý hiển thị khi task `CANCELLED` hoặc caller mất quyền |
| Handover link | `taskId` trên item do Team Leader chọn; Task API cập nhật assignee; Handover lưu recipient và acknowledgement | `operationId`, trạng thái retry/compensation và chính sách giữ read-only package |
| SAG mapping | Chỉ mapping/index nguồn Work Note/evidence được phép; không có source type Task | LanceDB là engine target được chấp nhận cho MVP; runtime/deployment và cơ chế de-index vẫn cần xác minh/đặc tả |

### Field, status và index đề xuất

- Task type duy nhất: `TASK`; không có Epic/Story/Bug trong MVP.
- `title`, `organizationId`, `projectId`, `createdBy` là required. `status` mặc định `TODO`; `priority` mặc định `MEDIUM`. `teamId`, `description`, `assigneeId`, `dueDate` là optional.
- Status cố định: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`. `DONE` có thể trở lại `IN_PROGRESS` nếu người phụ trách/Team Leader ghi lý do; `CANCELLED` không được xóa cứng hoặc mở lại trong MVP.
- Đề xuất compound indexes: `(organizationId, projectId, status, updatedAt)`, `(organizationId, projectId, assigneeId, status)`, `(organizationId, projectId, teamId, dueDate)`. Index cuối cần phù hợp filter/query sau khi API contract được duyệt.
- Đề xuất event history ghi actor/time và field đã đổi cho status, assignee, due date, priority, team, title/description, cancel/reopen. Không lưu task snapshot đầy đủ; không ghi raw body dài vào central security audit.
- Dùng Mongo `ObjectId` làm task identifier trong MVP; không tạo sequence/task key kiểu Jira. Không bulk import task từ ManageWork/Jira trong MVP.

## 4. Các quyết định cần hoàn tất trước khi triển khai

1. Duyệt các khuyến nghị trong Use Case doc trước khi biến field/status/permission proposal thành requirement.
2. Xác nhận tên database MongoDB hiện có (`continuum_db` theo DEC-011/SPEC-001) trong cấu hình triển khai; không tạo database riêng cho task.
3. Chốt response/DTO và cách trả lỗi khi task bị hủy hoặc caller không còn quyền xem.
4. Chốt retention cho `task_events` và cách đồng bộ domain event sang compliance audit nếu cần.
5. Xác minh SAG runtime/source/deployment có triển khai engine target LanceDB và cơ chế de-index; không copy task records vào SAG. PostgreSQL + pgvector/Qdrant chỉ là phương án thay thế/mở rộng, cần ADR riêng nếu muốn đổi target.

Tham chiếu: [ADR-009](../research-tech/ADR-009-internal-task-source-and-mongodb.md), [Task-management Use Cases](../research-docs/Internal-Work-Management/12-continuum-task-management-use-cases.md), [permission baseline](../research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md), [daily workflow](../research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md), [Work Note schema](02_SVC_CAPTURE_SCHEMA.md), [Handover schema](06_SVC_HANDOVER_SCHEMA.md), [SAG storage schema](11_SAG_STORAGE_SCHEMA.md).
