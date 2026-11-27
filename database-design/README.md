# Continuum AI — Danh Mục Thiết Kế Cơ Sở Dữ Liệu Theo Service + SAG Storage
## (Service-Owned Database & Schema Catalog — Product Target)

> **Dự án:** Continuum AI — Nền tảng kế thừa và chuyển giao tri thức dự án phần mềm  
> **Phiên bản thiết kế DB:** 3.1 (Cập nhật đồng bộ Full-System Audit `2026-11-27`: Service-Owned MongoDB + Audit + SAG PostgreSQL 16 & Qdrant)
> **Ngăn xếp lưu trữ:** MongoDB 7.0 (Source of Truth) + PostgreSQL 16 (`sag` schema) & **Qdrant** (SAG Post-Extraction & Hybrid Vector Store) + Backend Object Storage (`STORAGE_MODE=r2|s3|local`, Cloudflare R2 cho Prod)

> **Phạm vi (`2026-11-27`):** Đây là catalog schema của Continuum AI đã đối soát với runtime `DATN_BE` và `sag-laya-integration`. Theo workspace ADR-003/DEC-011, mỗi bounded domain sở hữu một logical MongoDB database trên replica set dùng chung; audit dùng `continuum_audit`.
> - **Đã kích hoạt trong runtime `DATN_BE`:** `continuum_iam`, `continuum_capture`, **`continuum_task` (kích hoạt `2026-10-22`, hiện host thực dụng trong `IamModule` qua `useDb('continuum_task')` và cô lập bằng `TaskWorkspaceRepository`)**, `continuum_lifecycle`, `continuum_chat`, `continuum_handover`, `continuum_ingestion`, `continuum_notification`, `continuum_jira` (legacy module chờ kế hoạch retire), và `continuum_audit`.
> - **Chưa có standalone owner:** `continuum_ai_adapter` vẫn là target schema.
> - **SAG Storage (`sag-laya-integration`):** Triển khai thực tế sử dụng **PostgreSQL 16 (`sag` schema)** cho metadata/ACL/graph/Leiden tree kết hợp **Qdrant** cho vector search (1024-d Dense + native BM25 Sparse); `pgvector` và LanceDB không được dùng trong production runtime. Xem [database topology alignment note](../research-docs/Workspace/02-database-topology-successor-2026-10-02.md).

---

## 1. Triết Lý Kiến Trúc: Database-per-Service & Bộ Lưu Trữ Tri Thức Sau Extract

Trong kiến trúc Microservices của Continuum AI:
1. **Mỗi Bounded Service sở hữu Database riêng (Database-per-Service):** Tuyệt đối không chia sẻ kết nối DB hay JOIN bảng xuyên service.
2. **MongoDB 7.0 đóng vai trò Source of Truth** cho toàn bộ dữ liệu nghiệp vụ, vòng đời tri thức, phân quyền và kiểm toán.
3. **`continuum_sag_storage` (`sag-laya-integration`) đóng vai trò Bộ lưu trữ dữ liệu sau trích xuất (Post-Extraction Knowledge Store):** Triển khai thực tế trên **PostgreSQL 16 (`sag` schema)** lưu trữ tài liệu, phiên bản, `SourceProjectMapping`, `SearchUnit`, `DenseGraph` (E0/E1) và cây điều hướng Leiden, kết hợp **Qdrant** (bắt buộc trong production) lưu trữ Hybrid Vector 1024-d Dense + native BM25 Sparse theo từng project.

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
| **03** | [12_TASK_MANAGEMENT_SCHEMA.md](12_TASK_MANAGEMENT_SCHEMA.md) | **`svc_task` (active in `IamModule`)** | `continuum_task` (MongoDB; active since `2026-10-22`) | Task canonical, sprints, history append-only và `deadline_scan_due_cursor`; truy cập độc quyền qua `TaskWorkspaceRepository` / Task API. |
| **04** | [04_SVC_LIFECYCLE_SCHEMA.md](04_SVC_LIFECYCLE_SCHEMA.md) | **`svc_lifecycle`** | `continuum_lifecycle` (MongoDB) | Vòng đời tri thức bất biến (`v1 → v2`), Verification Inbox, ACID Transaction, truy vết Evidence. |
| **05** | [05_SVC_CHAT_SCHEMA.md](05_SVC_CHAT_SCHEMA.md) | **`svc_chat`** | `continuum_chat` (MongoDB) | Hội thoại hỏi đáp RAG, bắt buộc trích dẫn citations, log trạng thái `INSUFFICIENT_EVIDENCE`. |
| **06** | [06_SVC_HANDOVER_SCHEMA.md](06_SVC_HANDOVER_SCHEMA.md) | **`svc_handover`** | `continuum_handover` (MongoDB) | Quản lý chuyển giao kế thừa, thực thể Trách nhiệm độc lập, phỏng vấn âm thanh bóc băng STT. |
| **07** | [07_SVC_INGESTION_SCHEMA.md](07_SVC_INGESTION_SCHEMA.md) | **`svc_ingestion`** | `continuum_ingestion` (MongoDB) | Siêu dữ liệu file Cloudflare R2, băm SHA-256 chống trùng lặp, cầu nối `sag_mappings`. |
| **08** | [08_SVC_NOTIFICATION_SCHEMA.md](08_SVC_NOTIFICATION_SCHEMA.md) | **`svc_notification`** | `continuum_notification` (MongoDB) | Thông báo In-App WebSocket, cấu hình nhận tin, nhật ký gửi Mail giao dịch Resend/SMTP. |
| **09** | [09_SVC_AI_ENGINE_SCHEMA.md](09_SVC_AI_ENGINE_SCHEMA.md) | **`svc_ai_engine` (target)** | `continuum_ai_adapter` (MongoDB; target, not active runtime) | Quản lý định tuyến LLM Provider, System Prompt có phiên bản, nhật ký tiêu thụ Token. |
| **10** | [10_AUDIT_AND_COMPLIANCE_SCHEMA.md](10_AUDIT_AND_COMPLIANCE_SCHEMA.md) | **Cross-Cutting** | `continuum_audit` (MongoDB) | Nhật ký kiểm toán bất biến (Append-only) phục vụ tiêu chuẩn bảo mật doanh nghiệp (SOC2/ISO). |
| **11** | [11_SAG_STORAGE_SCHEMA.md](11_SAG_STORAGE_SCHEMA.md) | **SAG Subsystem** | `sag` schema (PostgreSQL 16) + **Qdrant** (per-project collections) | Tầng lưu trữ tri thức sau extract: Documents/Versions/ACL maps, SearchUnits, DenseGraph E0/E1, Leiden Routing Tree, 3D Universe và Qdrant Hybrid Dense+BM25 vectors. |

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
