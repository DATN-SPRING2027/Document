# Continuum AI — Thiết Kế Cơ Sở Dữ Liệu Chuẩn 9 Vi Dịch Vụ + SAG Storage
## (Microservices Dedicated Database & Schema Specification - 9 Services + Dedicated Storage)

> **Dự án:** Continuum AI — Nền tảng kế thừa và chuyển giao tri thức dự án phần mềm  
> **Phiên bản thiết kế DB:** 3.0 (Module hóa hoàn chỉnh: 9 Services + Audit + SAG Post-Extraction Storage)  
> **Ngăn xếp lưu trữ:** MongoDB 7.0 (Source of Truth) + PostgreSQL 16 & pgvector (SAG Post-Extraction Storage) + Cloudflare R2 (Object Storage)  

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
│  [01. continuum_iam]          ➔ svc_iam (Auth, Users, 3 Roles, Orgs, Grants)           │
│  [02. continuum_capture]      ➔ svc_capture (Work Notes What/How/Why, Requirements)     │
│  [03. continuum_jira]         ➔ svc_jira (Jira Cloud Connector, Issues, Idempotency)    │
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
| **01** | [01_SVC_IAM_SCHEMA.md](01_SVC_IAM_SCHEMA.md) | **`svc_iam`** | `continuum_iam` (MongoDB) | Xác thực, 3 roles tĩnh (`ADMIN`, `TEAM_LEADER`, `MEMBER`), cấp quyền `project.create`, xoay vòng Refresh Token. |
| **02** | [02_SVC_CAPTURE_SCHEMA.md](02_SVC_CAPTURE_SCHEMA.md) | **`svc_capture`** | `continuum_capture` (MongoDB) | Ghi nhận What/How/Why, autosave drafts, bắt buộc tác giả tự xác nhận (`authorConfirmedAt`). |
| **03** | [03_SVC_JIRA_SCHEMA.md](03_SVC_JIRA_SCHEMA.md) | **`svc_jira`** | `continuum_jira` (MongoDB) | Kết nối Jira Cloud, ánh xạ tài khoản, lưu trữ mirror issues, xử lý Idempotent Webhook. |
| **04** | [04_SVC_LIFECYCLE_SCHEMA.md](04_SVC_LIFECYCLE_SCHEMA.md) | **`svc_lifecycle`** | `continuum_lifecycle` (MongoDB) | Vòng đời tri thức bất biến (`v1 → v2`), Verification Inbox, ACID Transaction, truy vết Evidence. |
| **05** | [05_SVC_CHAT_SCHEMA.md](05_SVC_CHAT_SCHEMA.md) | **`svc_chat`** | `continuum_chat` (MongoDB) | Hội thoại hỏi đáp RAG, bắt buộc trích dẫn citations, log trạng thái `INSUFFICIENT_EVIDENCE`. |
| **06** | [06_SVC_HANDOVER_SCHEMA.md](06_SVC_HANDOVER_SCHEMA.md) | **`svc_handover`** | `continuum_handover` (MongoDB) | Quản lý chuyển giao kế thừa, thực thể Trách nhiệm độc lập, phỏng vấn âm thanh bóc băng STT. |
| **07** | [07_SVC_INGESTION_SCHEMA.md](07_SVC_INGESTION_SCHEMA.md) | **`svc_ingestion`** | `continuum_ingestion` (MongoDB) | Siêu dữ liệu file Cloudflare R2, băm SHA-256 chống trùng lặp, cầu nối `sag_mappings`. |
| **08** | [08_SVC_NOTIFICATION_SCHEMA.md](08_SVC_NOTIFICATION_SCHEMA.md) | **`svc_notification`** | `continuum_notification` (MongoDB) | Thông báo In-App WebSocket, cấu hình nhận tin, nhật ký gửi Mail giao dịch Resend/SMTP. |
| **09** | [09_SVC_AI_ENGINE_SCHEMA.md](09_SVC_AI_ENGINE_SCHEMA.md) | **`svc_ai_engine`** | `continuum_ai_adapter` (MongoDB) | Quản lý định tuyến LLM Provider, System Prompt có phiên bản, nhật ký tiêu thụ Token. |
| **10** | [10_AUDIT_AND_COMPLIANCE_SCHEMA.md](10_AUDIT_AND_COMPLIANCE_SCHEMA.md) | **Cross-Cutting** | `continuum_audit` (MongoDB) | Nhật ký kiểm toán bất biến (Append-only) phục vụ tiêu chuẩn bảo mật doanh nghiệp (SOC2/ISO). |
| **11** | [11_SAG_STORAGE_SCHEMA.md](11_SAG_STORAGE_SCHEMA.md) | **SAG Subsystem** | `continuum_sag_storage` (PostgreSQL 16 + pgvector / Qdrant) | Tầng lưu trữ tri thức sau extract: Chunks, Events, Entities, Hyperedges quan hệ và Vector Store (pgvector / Qdrant). |

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
