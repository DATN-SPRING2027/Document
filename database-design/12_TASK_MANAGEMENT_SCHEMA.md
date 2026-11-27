# Continuum AI — Thiết kế lưu trữ Task nội bộ

> **Trạng thái:** **ACTIVE trong runtime `DATN_BE`** (kích hoạt ngày `2026-10-22` kèm Gate G4 Manager Task governance; đồng bộ Full-System Audit ngày `2026-11-27`).
>
> **Ngày quyết định:** `2026-10-01` (ADR-009/ADR-010) · Kích hoạt `2026-10-22` (Gate G4) · Đồng bộ `2026-11-27`
>
> **Service sở hữu:** Task Workspace trong `DATN_BE` — hiện triển khai thực dụng trong `IamModule` qua `useDb('continuum_task')` và cô lập truy cập qua `TaskWorkspaceRepository`; tách thành process độc lập (`dist/services/task/main.js`) vẫn là kiến trúc đích của ADR-010.
> **Database engine:** MongoDB 7.0 với Mongoose; database logical riêng `continuum_task` trên replica set hiện có (đã áp migration index `20261024-task-deadline-scan-index`). Không tạo repo ManageWork hay MongoDB cluster vật lý mới.

## 1. Quyết định và phạm vi

Continuum là nguồn chính thức và duy nhất cho vòng đời task DATN trong MVP. Client tạo, đọc, cập nhật, gán người phụ trách và đổi trạng thái task qua API Gateway rồi tới Task Service. Bản ghi canonical thuộc database `continuum_task`. Jira không tham gia tạo, đồng bộ hoặc làm bản sao task. Task Service có process và cấu hình triển khai riêng nhưng dùng chung repo BE, MongoDB replica set và Redis/BullMQ hiện có.

Ranh giới đã chốt: Task Service là đường đọc/ghi duy nhất cho task canonical; Gateway là lối vào từ FE, còn service-to-service truy cập qua contract nội bộ. Các service khác không đọc/ghi database của Task. Các chi tiết field-level dưới đây là đề xuất đồng bộ với [Task Use Cases](../research-docs/Internal-Work-Management/12-continuum-task-management-use-cases.md), chưa phải schema đã được phê duyệt hoặc triển khai.

## 2. Ràng buộc dữ liệu

- Mọi task phải có `organizationId` và đúng một `projectId`; đề xuất `teamId` tùy chọn, tối đa một team trong project. Task API phải kiểm tra quyền/scope ở mỗi thao tác đọc/ghi.
- Task Service API là đường ghi duy nhất cho lifecycle task. Các service khác chỉ đọc/gửi command qua API hoặc giữ logical reference; không tạo mirror writable ở Work Note, Handover hay SAG.
- **Task Note / Capture linking (cập nhật `2026-10-24` / `2026-11-27`):** `Task Note` (`work_notes`) gắn với một Task hợp lệ trong cùng Project (xác thực qua Task API/bridge theo phạm vi Organization/Project/Team và Gate G4), trong khi `Project Document` (`project_documents`) và `Periodic Work Report` (`work_reports`) là bản ghi cấp Project không gắn `taskId`.
- **Gate G4 Manager Task access (`2026-10-22`) & Monolith-Placement ADR Note (`2026-11-27`):** `TaskWorkspaceIamBridge` cấp quyền quản trị Task Workspace cho `ADMIN` (`Manager`) đang `ACTIVE` trong cùng Organization trên các Project hoạt động. Để tuân thủ ranh giới dữ liệu ngay cả khi Task Workspace đang chạy trong `IamModule`, `NotificationCenterRepository`, Capture và Handover **bắt buộc** gọi qua `TaskWorkspaceRepository` / Task API (tuyệt đối không mở raw collection `continuum_task.tasks` trực tiếp).
- **Handover link:** Handover giữ `taskId` cho task còn mở do Team Leader/Manager chọn. Trong luồng Handover V2 (`/quick-transfer`), việc chuyển giao task sang Successor B chỉ được phép sau khi gói bàn giao đã ở trạng thái được Successor B chấp nhận (`PACKAGE_NOT_ACCEPTED` được enforce đồng nhất — H-15/P-04). Task API cập nhật assignee canonical; Handover không tạo bản ghi task mutable thứ hai.
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
2. `continuum_task` **đã thuộc active `DATN_BE` runtime inventory từ `2026-10-22`** (đã có migration `20261024-task-deadline-scan-index` cho `deadline_scan_due_cursor`). Khi chuyển từ monolith hosting trong `IamModule` sang standalone process `dist/services/task/main.js` (ADR-010), giữ nguyên `SERVICE_DATABASE=continuum_task` trên cùng MongoDB replica set và định tuyến qua `TASK_SERVICE_URL` của Gateway mà không cần di trú dữ liệu sang cluster mới.
3. Chốt response/DTO và cách trả lỗi khi task bị hủy hoặc caller không còn quyền xem.
4. Chốt retention cho `task_events` và cách đồng bộ domain event sang compliance audit nếu cần.
5. Chốt retry, idempotency và retention cho outbox/event consumers. Không copy task records vào SAG; SAG storage được quyết định riêng và không bị thay đổi bởi Task Service.

Tham chiếu: [ADR-009](../research-tech/ADR-009-internal-task-source-and-mongodb.md), [ADR-010](../research-tech/ADR-010-task-service-in-existing-repositories.md), [Task-management Use Cases](../research-docs/Internal-Work-Management/12-continuum-task-management-use-cases.md), [permission baseline](../research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md), [daily workflow](../research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md), [Work Note schema](02_SVC_CAPTURE_SCHEMA.md), [Handover schema](06_SVC_HANDOVER_SCHEMA.md).
