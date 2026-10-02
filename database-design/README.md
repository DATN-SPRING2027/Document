# Continuum AI — Danh Mục Thiết Kế Cơ Sở Dữ Liệu Theo Service + SAG Storage
## (Service-Owned Database & Schema Catalog — Product Target)

> **Dự án:** Continuum AI — Nền tảng kế thừa và chuyển giao tri thức dự án phần mềm  
> **Phiên bản thiết kế DB:** 3.0 (Module hóa hoàn chỉnh: 9 Services + Audit + SAG Post-Extraction Storage)
> **Ngăn xếp lưu trữ:** MongoDB 7.0 (Source of Truth) + PostgreSQL 16 & pgvector (SAG Post-Extraction Storage) + Cloudflare R2 (Object Storage)

> **Phạm vi:** Đây là catalog schema/target của Product, không phải ảnh chụp runtime. Theo quyết định được phê duyệt ngày 2026-10-02 (workspace ADR-003/DEC-011), mỗi bounded service đang hoạt động sở hữu một logical MongoDB database trên cluster dùng chung; audit dùng `continuum_audit`. Runtime DATN-BE hiện có tám domain DB gồm cả `continuum_jira`, cộng audit. `continuum_task` và `continuum_ai_adapter` là target docs nhưng chưa có active owner/deployment trong BE runtime; không đưa chúng vào migration inventory cho tới khi hợp đồng service được triển khai và đối soát. Product docs hiện mô tả Jira là lịch sử trong khi BE runtime còn `continuum_jira`; đây là đối soát cần hoàn tất riêng. Dữ liệu `continuum_db` cũ chỉ được copy qua migration có dry-run/backup/cutover gate; source không bị xóa trong gói này. Xem [database topology alignment note](../research-docs/Workspace/02-database-topology-successor-2026-10-02.md).

---

## 1. Triết Lý Kiến Trúc: Database-per-Service & Bộ Lưu Trữ Tri Thức Sau Extract

Trong kiến trúc Microservices của Continuum AI:
1. **Mỗi Bounded Service sở hữu Database riêng (Database-per-Service):** Tuyệt đối không chia sẻ kết nối DB hay JOIN bảng xuyên service.
2. **MongoDB 7.0 đóng vai trò Source of Truth** cho toàn bộ dữ liệu nghiệp vụ, vòng đời tri thức, phân quyền và kiểm toán.
3. **`continuum_sag_storage` (Dựa trên Zleap-AI/SAG) đóng vai trò Bộ lưu trữ dữ liệu sau trích xuất (Post-Extraction Knowledge Store):** Chuẩn hóa hợp nhất trên **PostgreSQL 16 + pgvector**, lưu trữ phân đoạn (Chunk), Sự kiện (Event), Thực thể (Entity), Siêu cạnh quan hệ (Dynamic Hyperedges) và Vector Embeddings phục vụ truy vấn ngữ nghĩa sâu.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│              HỆ THỐNG 9 DATABASE DỊCH VỤ + AUDIT + SAG POST-EXTRACTION STORAGE         │
│                                                                                        │
│  [01. continuum_iam]          ➔ svc_iam (Auth, Users, Platform Ops + 3 Org Roles)      │
│  [02. continuum_capture]      ➔ svc_capture (Work Notes What/How/Why, Requirements)     │
│  [03. continuum_task]         ➔ svc_task (Canonical task lifecycle, history, outbox)     │
│  [04. continuum_lifecycle]    ➔ svc_lifecycle (Verified Knowledge, Snapshots, Evidence) │
│  [05. continuum_chat]         ➔ svc_chat (Cited Assistant, Sessions, Messages, Logs)   │
│  [06. continuum_handover]     ➔ svc_handover (Responsibilities, Handover, Audio STT)    │
│  [07. continuum_ingestion]    ➔ svc_ingestion (Documents, R2 Metadata, SAG Mappings)    │
│  [08. continuum_notification] ➔ svc_notification (In-App Alerts, Resend/SMTP Logs)     │
│  [09. continuum_ai_adapter]   ➔ svc_ai_engine (Model Routing, Prompts, Token Executions)│
│  ───────────────────────────────────────────────────────────────────────────────────  │
│  [10. continuum_audit]        ➔ Cross-Cutting Immutable Audit Trail & Compliance        │
│  ───────────────────────────────────────────────────────────────────────────────────  │
│  [11. continuum_sag_storage]  ➔ SAG Knowledge Store (Chunk, Event, Entity, Hyperedge,   │
│                                 Hợp nhất trên PostgreSQL 16 + pgvector)                │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Mục Lục Bộ Tài Liệu Schema Module Hóa Độc Lập

Tất cả các thành phần cơ sở dữ liệu đều có **1 tài liệu đặc tả markdown riêng biệt**:

| STT | File Tài Liệu Schema | Bounded Context / Tầng | Tên Database / Công Nghệ | Mục Đích Lưu Trữ & Nghiệp Vụ Chính |
| :---: | :--- | :--- | :--- | :--- |
| **01** | [01_SVC_IAM_SCHEMA.md](01_SVC_IAM_SCHEMA.md) | **`svc_iam`** | `continuum_iam` (MongoDB) | Xác thực, OrganizationMembership, actor PLATFORM_OPERATOR riêng, 3 role Organization/Project (`ADMIN`, `TEAM_LEADER`, `MEMBER`), scoped assignments và refresh-token rotation. Project creation dựa trên active Organization Membership; grant `project.create` không bắt buộc. |
| **02** | [02_SVC_CAPTURE_SCHEMA.md](02_SVC_CAPTURE_SCHEMA.md) | **`svc_capture`** | `continuum_capture` (MongoDB) | Ghi nhận What/How/Why, autosave drafts, bắt buộc tác giả tự xác nhận (`authorConfirmedAt`). |
| **03** | [12_TASK_MANAGEMENT_SCHEMA.md](12_TASK_MANAGEMENT_SCHEMA.md) | **`svc_task` (target)** | `continuum_task` (MongoDB; target, not active runtime) | Task canonical, history append-only và outbox tùy chọn; API là đường đọc/ghi duy nhất. |
| **04** | [04_SVC_LIFECYCLE_SCHEMA.md](04_SVC_LIFECYCLE_SCHEMA.md) | **`svc_lifecycle`** | `continuum_lifecycle` (MongoDB) | Vòng đời tri thức bất biến (`v1 → v2`), Verification Inbox, ACID Transaction, truy vết Evidence. |
| **05** | [05_SVC_CHAT_SCHEMA.md](05_SVC_CHAT_SCHEMA.md) | **`svc_chat`** | `continuum_chat` (MongoDB) | Hội thoại hỏi đáp RAG, bắt buộc trích dẫn citations, log trạng thái `INSUFFICIENT_EVIDENCE`. |
| **06** | [06_SVC_HANDOVER_SCHEMA.md](06_SVC_HANDOVER_SCHEMA.md) | **`svc_handover`** | `continuum_handover` (MongoDB) | Quản lý chuyển giao kế thừa, thực thể Trách nhiệm độc lập, phỏng vấn âm thanh bóc băng STT. |
| **07** | [07_SVC_INGESTION_SCHEMA.md](07_SVC_INGESTION_SCHEMA.md) | **`svc_ingestion`** | `continuum_ingestion` (MongoDB) | Siêu dữ liệu file Cloudflare R2, băm SHA-256 chống trùng lặp, cầu nối `sag_mappings`. |
| **08** | [08_SVC_NOTIFICATION_SCHEMA.md](08_SVC_NOTIFICATION_SCHEMA.md) | **`svc_notification`** | `continuum_notification` (MongoDB) | Thông báo In-App WebSocket, cấu hình nhận tin, nhật ký gửi Mail giao dịch Resend/SMTP. |
| **09** | [09_SVC_AI_ENGINE_SCHEMA.md](09_SVC_AI_ENGINE_SCHEMA.md) | **`svc_ai_engine` (target)** | `continuum_ai_adapter` (MongoDB; target, not active runtime) | Quản lý định tuyến LLM Provider, System Prompt có phiên bản, nhật ký tiêu thụ Token. |
| **10** | [10_AUDIT_AND_COMPLIANCE_SCHEMA.md](10_AUDIT_AND_COMPLIANCE_SCHEMA.md) | **Cross-Cutting** | `continuum_audit` (MongoDB) | Nhật ký kiểm toán bất biến (Append-only) phục vụ tiêu chuẩn bảo mật doanh nghiệp (SOC2/ISO). |
| **11** | [11_SAG_STORAGE_SCHEMA.md](11_SAG_STORAGE_SCHEMA.md) | **SAG Subsystem** | `continuum_sag_storage` (PostgreSQL 16 + pgvector / Qdrant) | Tầng lưu trữ tri thức sau extract: Chunks, Events, Entities, Hyperedges quan hệ và Vector Store (pgvector / Qdrant). |

> Catalog Product giữ `03_SVC_JIRA_SCHEMA.md` làm tài liệu lịch sử và chọn Task làm nguồn task canonical. Tuy nhiên, `continuum_jira` vẫn có trong BE runtime inventory hiện tại; không xóa hoặc gộp database Jira trước khi chủ sở hữu sản phẩm chốt việc retire deployment và migration của Jira.

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
