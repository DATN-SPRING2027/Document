# Continuum AI — Hạ Tầng Dữ Liệu, Hàng Đợi & AI (Storage, Messaging & AI)

> Nằm trong tài liệu kiến trúc tổng thể Continuum AI. Xem [Mục lục](README.md).
> **Cập nhật đồng bộ runtime (`2026-11-27` — `SAG-DB-003`, `SAG-RET-004`, `E2E-INT-001`, `DOC-003`):** Tài liệu phản ánh chính xác kiến trúc triển khai hiện hành của `DATN_BE` và `sag-laya-integration` (**MongoDB 7.0 + PostgreSQL 16 (`sag`) + Qdrant + Backend Object Storage `STORAGE_MODE=r2|s3|local`**). Các thiết kế thử nghiệm cũ (LanceDB, `pgvector`, R2 trực tiếp từ SAG, UMAP/Neural Cross-Encoder/Laya) đã bị thay thế bởi các ADR chính thức.

---

## 1. Hạ tầng lưu trữ dữ liệu (Data Storage Tier)

Hệ thống phân định ranh giới lưu trữ dữ liệu rõ ràng giữa các tầng công nghệ:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       HẠ TẦNG LƯU TRỮ DỮ LIỆU (ACTIVE RUNTIME)                                │
│                                                                                                               │
│   ┌─────────────────────────┐  ┌──────────────────────────────────┐  ┌─────────────────────────────────────┐ │
│   │ MongoDB 7.0 Replica Set │  │ PostgreSQL 16 (`sag` schema)     │  │ Qdrant Vector Engine (Bắt buộc Prod)│ │
│   │ (rs0 — Source of Truth) │  │ + SAG Local Upload Volume        │  │ (Per-Project Hybrid Collections)    │ │
│   ├─────────────────────────┤  ├──────────────────────────────────┤  ├─────────────────────────────────────┤ │
│   │ • Source of Truth       │  │ • Documents, Versions, ACL Maps  │  │ • `search_units_{project_id}`       │ │
│   │ • IAM, Capture, Task,   │  │ • SearchUnits, DenseGraph E0/E1  │  │ • `routing_tree_{project_id}`       │ │
│   │   Chat, Handover, Audit │  │ • Leiden Routing Tree & Universe │  │ • `session_units_{project_id}`      │ │
│   │ • ACID Transactions     │  │ • InProcJobQueue job records     │  │ • 1024-d Dense + BM25 Sparse (IDF)  │ │
│   └─────────────────────────┘  └──────────────────────────────────┘  └─────────────────────────────────────┘ │
│                                                                                                               │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Backend Object Storage (`STORAGE_MODE=r2|s3|local`; Cloudflare R2 cho Production)                     │   │
│   │ • Owned strictly by `DATN_BE` (Capture Project Documents, Chat Attachments, Handover Audio)           │   │
│   │ • BE streams approved bytes via HTTP multipart to SAG `/api/v1/projects/{project_id}/documents/upload`│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.1. MongoDB 7.0 (3-Node Replica Set `rs0`) — Nguồn Chân Lý (Source of Truth)
**Topology hiện hành theo workspace ADR-003/DEC-011 & cập nhật `2026-11-27`:** MongoDB remains the operational source of truth on the existing cluster/replica set, with logical databases per bounded domain: `continuum_iam`, `continuum_capture`, `continuum_task` (activated `2026-10-22`, pragmatically mounted inside `IamModule` via `useDb('continuum_task')` and accessed exclusively through `TaskWorkspaceRepository`), `continuum_lifecycle`, `continuum_chat`, `continuum_handover`, `continuum_ingestion`, `continuum_notification`, `continuum_jira` (legacy module pending retirement), and cross-cutting `continuum_audit`. `continuum_ai_adapter` remains a target schema without an active standalone runtime owner. Do not use the former shared `continuum_db` for runtime domain writes. See the local [topology catalog](../database-design/README.md).

* **Tại sao dùng MongoDB?** Mô hình tri thức phần mềm (Knowledge Objects), Capture records (`work_notes`, `project_documents`, `work_reports`), và Task/Handover có cấu trúc linh hoạt và hỗ trợ **Multi-Document ACID Transactions** trên Replica Set `rs0`.
* **Đặc tả Schema chi tiết từng Service:** Xem toàn bộ thiết kế cơ sở dữ liệu tại [Document/database-design/](../database-design/README.md).

#### Task Workspace storage boundary (`2026-10-22` / `2026-11-27`)

`continuum_task` đã được kích hoạt trên replica set hiện có và chứa `tasks`, `task_events`, sprints/boards và các index vận hành (bao gồm `deadline_scan_due_cursor`). Trong topology capstone hiện hành, Task Workspace chạy trong `IamModule` nhưng mọi truy cập từ Capture, Handover và Notification Center đều đi qua `TaskWorkspaceRepository` / Task API contract (không đọc/ghi raw collection chéo domain). Tách process độc lập (`dist/services/task/main.js`) vẫn là đích kiến trúc khi bật microservices Gateway. Xem [Task storage design](../database-design/12_TASK_MANAGEMENT_SCHEMA.md) và [ADR-010](../research-tech/ADR-010-task-service-in-existing-repositories.md).

### 1.2. PostgreSQL 16 (`sag` schema) + Qdrant (Bộ Lưu Trữ SAG & Vũ Trụ Tri Thức 3D)
* **PostgreSQL 16 (`sag` schema — Metadata, ACL, Graph & Routing Tree):**
  - Lưu trữ `documents`, `document_versions`, `source_project_mappings` (`state='CONFIRMED'`), `search_units`, `dense_graph` (E0/E1 deterministic entities & relations), cây điều hướng Leiden (`routing_tree`), và bản chụp 3D Knowledge Universe (`universe_*`). SQLite chỉ dùng cho dev/test đơn tiến trình, tuyệt đối không dùng cho production.
  - Áp dụng SQLAlchemy async connection pooling tường minh (`pool_size`, `max_overflow`, `pool_pre_ping=True`, `pool_recycle`).
* **Qdrant (Kho Vector Bắt Buộc Cho Production — thay thế LanceDB & `pgvector`):**
  - Tổ chức theo từng project để cô lập tenant vật lý và tăng tốc lọc ACL: `search_units_{project_id}`, `routing_tree_{project_id}`, `session_units_{project_id}`.
  - Mỗi collection hỗ trợ **Hybrid Dense (1024-d Cosine) + Native Sparse BM25 (`Modifier.IDF`)**, với payload index trên `document_id`, `version_id`, `partition_id`, `is_active`, `status`.
  - Khi tài liệu bị thay thế hoặc thu hồi (`KNOWLEDGE_SOURCE_REVOKED` / `KNOWLEDGE_SOURCE_REPLACED`), SAG cập nhật trạng thái trong PostgreSQL, kích hoạt `UnitSupersessionOverlay` để lọc ngay ở truy vấn và xóa các vector points tương ứng khỏi Qdrant theo batch.
  - Chi tiết schema và đối chiếu lịch sử xem tại [11_SAG_STORAGE_SCHEMA.md](../database-design/11_SAG_STORAGE_SCHEMA.md).

### 1.3. Backend Object Storage (`STORAGE_MODE=r2|s3|local`) & Cơ chế Upload sang SAG
* **Phân tách quyền sở hữu Storage (`adr-remove-laya-and-r2.md`):**
  - **`DATN_BE`** sở hữu Cloudflare R2 (Production) / S3-compatible / Local adapter (`STORAGE_MODE=r2|s3|local`) cho file gốc Project Documents, Chat Attachments và Handover Audio.
  - Capture hỗ trợ `upload-intent` (presigned PUT URL gắn chặt `(organizationId, projectId)` — `SEC-AUTH-002`) và `confirm-upload` (kiểm tra magic bytes + full-file SHA-256).
  - **`sag-laya-integration` không truy cập trực tiếp R2** và không hỗ trợ endpoint `/ingest-object`. Khi tài liệu/báo cáo được phê duyệt (`APPROVED`), `KnowledgeOutboxConsumer` ở `DATN_BE` đọc bytes từ Object Storage và stream qua HTTP multipart tới `POST /api/v1/projects/{project_id}/documents/upload` của SAG (lưu trên local upload volume của SAG rồi đưa vào `InProcJobQueue`).

---

## 2. Hạ tầng Hàng đợi & Xử lý bất đồng bộ (NestJS BullMQ + Redis & SAG `InProcJobQueue`)

Phân định ranh giới hàng đợi giữa hai runtime Node.js và Python:

```
[ DATN_BE Domain Services ] ──► [ Redis 7.2 (noeviction) + BullMQ / Outbox Consumers ]
                                    ├── KnowledgeOutboxConsumer ──(HTTP multipart /upload)──► [ SAG FastAPI ]
                                    ├── notification.realtime.v1 (Redis Pub/Sub) ──► [ Chat WS Gateway ]
                                    ├── mail-queue / handover-queue / report schedulers
                                    └── Failed jobs / DLQ ──► Audit Log & Alert

[ SAG FastAPI (`sag-laya-integration`) ] ──► [ InProcJobQueue (asyncio in-process worker) ]
                                                 ├── Parse (MarkItDown / PDF / DOCX / OCR)
                                                 ├── C99 DP Segmentation + SearchUnit Chunking
                                                 ├── Embedding + Qdrant Batched Upsert
                                                 └── Deterministic E0/E1 DenseGraph + Leiden Routing Tree
```

### 2.1. Quy tắc vận hành Redis & Hàng đợi
* **Redis `maxmemory-policy noeviction`:** Bắt buộc cấu hình `noeviction` cho Redis lưu BullMQ queues, distributed leases và JWT blacklist (tuyệt đối không dùng `allkeys-lru` để tránh mất job/lock ngầm).
* **SAG không tiêu thụ BullMQ trực tiếp:** `sag-laya-integration` vận hành `InProcJobQueue` nội bộ (single-worker asyncio queue) kết hợp khóa/trạng thái bền vững trong PostgreSQL; vì vậy trong MVP hiện tại, SAG triển khai với `replicas: 1` cho đến khi chuyển sang worker queue phân tán riêng.
* **Dead Letter & Retry (`DATN_BE`):** Các job BullMQ và outbox consumer dùng exponential backoff có giới hạn số lần thử và ghi nhật ký lỗi rõ ràng; job thất bại **không bao giờ** xóa tệp nguồn gốc trên Object Storage.

---

## 3. Kiến trúc SAG AI Engine & Đường Ống Truy Xuất Thực Tế (Synced with `05_SAG_AI_RAG_AUDIT.md`)

Đường ống RAG đang vận hành thực tế trong `sag-laya-integration` (`main`):

```
[ Approved File Bytes (BE HTTP /upload) ]
                 │
                 ▼
[ Document Parser (MarkItDown / PDF / DOCX / Office / OCR) ]
                 │
                 ▼
[ Canonical C99 Dynamic Programming Topic Segmentation ]
                 │
                 ▼
[ Dense DP SearchUnit Chunking (heading-aware, locator/span preserved) ]
                 │
         ┌───────┴────────────────────────────────────────┐
         ▼                                                ▼
[ Qdrant Per-Project Collections ]             [ PostgreSQL 16 (`sag` schema) ]
  • 1024-d Dense Vector (Cosine)                 • Document / Version / Active ACL Maps
  • Native Sparse BM25 (`Modifier.IDF`)          • Deterministic E0/E1 `DenseGraph`
                                                 • Leiden Community Routing Tree
                                                 • 3D Universe Projections (Deterministic Layout)
```

### 3.1. Truy xuất lai (Hybrid Retrieval), Xếp hạng & Kiểm chứng trích dẫn
1. **Pre-Retrieval Tenant & ACL Scoping:** Backend NestJS xác thực `ACTIVE` Organization + `ACTIVE` Project Membership (`scope.isProjectMember === true`, Trap 5 fail-closed) và truyền `project_id` / `partition_id` hợp lệ. SAG lọc cứng theo `SourceProjectMapping(state='CONFIRMED')`, `Document.is_active=True` và `DocumentVersion.status != 'REVOKED'`.
2. **Hybrid Search + RRF (`k=60`):** Truy vấn đồng thời Dense Vector + Native BM25 Sparse trên Qdrant, hợp nhất thứ hạng bằng Reciprocal Rank Fusion (`k=60`), tùy chọn bổ sung truy hồi theo nhánh Leiden Routing Tree.
3. **Deterministic Reranking & Diversity:** Áp dụng bộ chấm điểm **heuristic deterministic** (lexical overlap, proximity, IDF, structural signals) kết hợp **MMR (Maximal Marginal Relevance)** và **`UnitSupersessionOverlay`** để loại bỏ đoạn trích từ phiên bản tài liệu đã bị thay thế/thu hồi.
4. **LLM Generation, Streaming SSE & Citation Verification:**
   - Prompt cách ly hoàn toàn ngữ cảnh tài liệu như untrusted data; `decision_provider` mặc định là `"disabled"` (không gọi thêm router LLM thừa trước mỗi truy vấn trừ khi bật tường minh).
   - Hỗ trợ streaming SSE (`MESSAGE_DELTA`) kết hợp kiểm chứng trích dẫn/grounding và trả `INSUFFICIENT_EVIDENCE` khi thiếu bằng chứng hợp lệ.
5. **Các thành phần đã loại bỏ / không có trong runtime (tránh nhầm lẫn tài liệu cũ):**
   - **Không** dùng LanceDB hay `pgvector` trong production.
   - **Không** dùng E2 LLM graph enrichment hoặc Laya (đã loại bỏ chính thức theo ADR để giảm chi phí/latency và đảm bảo tính tất định).
   - **Không** dùng neural cross-encoder reranker, METIS/Spectral clustering, UMAP, hoặc semantic response cache.
   - **ECCE (Query Expansion):** mặc định **TẮT** (opt-in qua cờ cấu hình).
