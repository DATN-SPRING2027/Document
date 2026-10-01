# Continuum AI — Thiết Kế Lưu Trữ Theo Bounded Context + SAG Retrieval
## (MongoDB operational store, domain collection ownership, and derived retrieval index)

> **Dự án:** Continuum AI — Nền tảng kế thừa và chuyển giao tri thức dự án phần mềm  
> **Phiên bản thiết kế DB:** 3.1 (Domain collection ownership + SAG retrieval boundary)
> **Ngăn xếp lưu trữ MVP:** MongoDB 7.0 (`continuum_db`, Source of Truth, gồm task nội bộ) + LanceDB (SAG retrieval target theo DEC-015/SPEC-005) + Cloudflare R2 (Object Storage)

---

## 1. Triết Lý Kiến Trúc: Domain Ownership & SAG Retrieval

Trong kiến trúc MVP đã được duyệt của Continuum AI:
1. **Tách quyền sở hữu theo bounded context:** Mỗi module/service sở hữu collection, repository và API của mình; không đọc/ghi collection xuyên context trực tiếp. MVP vẫn dùng operational MongoDB `continuum_db` đã được duyệt (DEC-011/SPEC-001); Task module có collection riêng trong database đó, không phải database/deployment riêng. Database-per-service là hướng tách triển khai, không được suy ra chỉ từ bảng mapping tài liệu này.
2. **MongoDB 7.0 đóng vai trò Source of Truth** cho toàn bộ dữ liệu nghiệp vụ, gồm task nội bộ do Continuum Task API quản lý, Work Note, vòng đời tri thức, quyền và kiểm toán.
3. **SAG là kho retrieval/index dẫn xuất:** LanceDB là target MVP được chấp nhận theo DEC-015/SPEC-005. Chỉ Work Note/evidence được Continuum cho phép mới đủ điều kiện lập chỉ mục; Task không phải nguồn SAG độc lập.
4. **Phạm vi của tài liệu SAG SQL bên dưới:** [11_SAG_STORAGE_SCHEMA.md](11_SAG_STORAGE_SCHEMA.md) giữ nghiên cứu PostgreSQL + pgvector/Qdrant như phương án thay thế/mở rộng, không phải schema MVP được duyệt. Việc tích hợp LanceDB thực tế vẫn cần xác minh source/deployment.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             MONGODB OPERATIONAL STORE + DOMAIN MODULES + SAG RETRIEVAL                 │
│                                                                                        │
│  [01. MongoDB continuum_db]   ➔ Source of truth cho domain state và task                │
│  [02. Continuum Task API]    ➔ Sở hữu `tasks`/`task_events`; boundary đọc/ghi task     │
│  [03. Capture / Handover]    ➔ Work Note `taskId` tùy chọn; Handover giữ task refs     │
│  [04. Lifecycle / Audit]     ➔ Knowledge verification và audit theo quyền             │
│  [05. SAG / LanceDB]         ➔ Retrieval index chỉ cho Work Note/evidence đủ điều kiện  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Mục Lục Bộ Tài Liệu Schema Module Hóa Độc Lập

Mỗi bounded context có tài liệu schema riêng để ghi rõ quyền sở hữu collection và contract. Các tên như `continuum_iam`, `continuum_capture`, v.v. trong legacy schema documents là nhãn theo miền; theo baseline MongoDB dùng operational database chung `continuum_db`. Chúng không khẳng định đang có database/deployment riêng. Task collections được mô tả tại [12_TASK_MANAGEMENT_SCHEMA.md](12_TASK_MANAGEMENT_SCHEMA.md).

| STT | File Tài Liệu Schema | Bounded Context / Tầng | Logical label / công nghệ | Mục Đích Lưu Trữ & Nghiệp Vụ Chính |
| :---: | :--- | :--- | :--- | :--- |
| **01** | [01_SVC_IAM_SCHEMA.md](01_SVC_IAM_SCHEMA.md) | **`svc_iam`** | `continuum_iam` (MongoDB) | Xác thực, 3 roles tĩnh (`ADMIN`, `TEAM_LEADER`, `MEMBER`), cấp quyền `project.create`, xoay vòng Refresh Token. |
| **02** | [02_SVC_CAPTURE_SCHEMA.md](02_SVC_CAPTURE_SCHEMA.md) | **`svc_capture`** | `continuum_capture` (MongoDB) | Ghi nhận What/How/Why, autosave drafts, bắt buộc tác giả tự xác nhận (`authorConfirmedAt`). |
| **03** | [12_TASK_MANAGEMENT_SCHEMA.md](12_TASK_MANAGEMENT_SCHEMA.md) | **Task domain** | MongoDB `continuum_db` (`tasks`, `task_events`) | Task API owns canonical tasks; Work Note/Handover giữ tham chiếu logic, không tạo bản sao task trong SAG. |
| **04** | [04_SVC_LIFECYCLE_SCHEMA.md](04_SVC_LIFECYCLE_SCHEMA.md) | **`svc_lifecycle`** | `continuum_lifecycle` (MongoDB) | Vòng đời tri thức bất biến (`v1 → v2`), Verification Inbox, ACID Transaction, truy vết Evidence. |
| **05** | [05_SVC_CHAT_SCHEMA.md](05_SVC_CHAT_SCHEMA.md) | **`svc_chat`** | `continuum_chat` (MongoDB) | Hội thoại hỏi đáp RAG, bắt buộc trích dẫn citations, log trạng thái `INSUFFICIENT_EVIDENCE`. |
| **06** | [06_SVC_HANDOVER_SCHEMA.md](06_SVC_HANDOVER_SCHEMA.md) | **`svc_handover`** | `continuum_handover` (MongoDB) | Quản lý chuyển giao kế thừa, thực thể Trách nhiệm độc lập, phỏng vấn âm thanh bóc băng STT. |
| **07** | [07_SVC_INGESTION_SCHEMA.md](07_SVC_INGESTION_SCHEMA.md) | **`svc_ingestion`** | `continuum_ingestion` (MongoDB) | Siêu dữ liệu file Cloudflare R2, băm SHA-256 chống trùng lặp, cầu nối `sag_mappings`. |
| **08** | [08_SVC_NOTIFICATION_SCHEMA.md](08_SVC_NOTIFICATION_SCHEMA.md) | **`svc_notification`** | `continuum_notification` (MongoDB) | Thông báo In-App WebSocket, cấu hình nhận tin, nhật ký gửi Mail giao dịch Resend/SMTP. |
| **09** | [09_SVC_AI_ENGINE_SCHEMA.md](09_SVC_AI_ENGINE_SCHEMA.md) | **`svc_ai_engine`** | `continuum_ai_adapter` (MongoDB) | Quản lý định tuyến LLM Provider, System Prompt có phiên bản, nhật ký tiêu thụ Token. |
| **10** | [10_AUDIT_AND_COMPLIANCE_SCHEMA.md](10_AUDIT_AND_COMPLIANCE_SCHEMA.md) | **Cross-Cutting** | `continuum_audit` (MongoDB) | Nhật ký kiểm toán bất biến (Append-only) phục vụ tiêu chuẩn bảo mật doanh nghiệp (SOC2/ISO). |
| **11** | [11_SAG_STORAGE_SCHEMA.md](11_SAG_STORAGE_SCHEMA.md) | **SAG Subsystem** | LanceDB target (MVP); PostgreSQL + pgvector/Qdrant là phương án nghiên cứu thay thế | Tầng retrieval dẫn xuất; nội dung SQL trong file chưa phải storage contract được duyệt. |

`03_SVC_JIRA_SCHEMA.md` là tài liệu baseline lịch sử, không phải schema MVP đang áp dụng. Jira integration, task mirroring, webhook ingestion, and reconciliation are out of scope for current task management.

---

## 3. Quy Ước Thiết Kế Schema Chung (Design Conventions)

1. **Khóa chính & Khóa logic:**
   - Mọi collection đều dùng `_id: Types.ObjectId` thống nhất.
   - Tham chiếu chéo service dùng Logical Reference (`userId`, `projectId`, `knowledgeObjectId`) dạng `Types.ObjectId` hoặc `string`. **Không bao giờ dùng Mongoose `.populate()` xuyên Database.**
2. **Multi-Tenancy bắt buộc:**
   - Mọi document thuộc nghiệp vụ dự án bắt buộc có `organizationId` và `projectId`.
   - Tất cả Compound Index tìm kiếm đều có tiền tố `(organizationId, projectId, ...)`.
3. **Đồng bộ dữ liệu:**
   - Khi cần dữ liệu của nhau, các service giao tiếp qua **Domain Events** (Redis PubSub / BullMQ) hoặc truy vấn API Gateway nội bộ.
