# Continuum AI — Hạ Tầng Dữ Liệu, Hàng Đợi & AI (Storage, Messaging & AI)

> Nằm trong tài liệu kiến trúc tổng thể Continuum AI. Xem [Mục lục](README.md).

---

## 1. Hạ tầng lưu trữ dữ liệu (Data Storage Tier)

Hệ thống phân định ranh giới lưu trữ dữ liệu rõ ràng giữa các tầng công nghệ:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       HẠ TẦNG LƯU TRỮ DỮ LIỆU                                          │
│                                                                                                        │
│   ┌────────────────────────┐  ┌───────────────────────────────────┐  ┌─────────────────────────────┐   │
│   │ MongoDB 7.0 Replica Set│  │ PostgreSQL 16 + pgvector (SAG)    │  │ Cloudflare R2               │   │
│   │ (rs0 - 3 Nodes)        │  │ (hoặc Qdrant Vector Engine)       │  │ (Object Store)              │   │
│   ├────────────────────────┤  ├───────────────────────────────────┤  ├─────────────────────────────┤   │
│   │ • Source of Truth      │  │ • Tri thức sau bóc tách           │  │ • File gốc PDF, DOCX, MD    │   │
│   │ • Nghiệp vụ, users     │  │ • Hypergraph (Chunk, Event, Entity)│ • File ghi âm phỏng vấn Handover│
│   │ • Lịch sử phiên bản    │  │ • Chỉ mục Vector HNSW (pgvector)  │  │ • Zero Egress Fees          │   │
│   │ • Audit Logs           │  │ • [3D UNIVERSE] Partitions & Nodes│  │ • S3 API Compatible         │   │
│   │ • ACID Transactions    │  │ • Dynamic Hyperedge SQL Retrieval │  │                             │   │
│   └────────────────────────┘  └───────────────────────────────────┘  └─────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.1. MongoDB 7.0 (3-Node Replica Set `rs0`) — Nguồn Chân Lý (Source of Truth)
**Topology hiện hành theo workspace ADR-003/DEC-011 (2026-10-02):** MongoDB remains the operational source of truth on the existing cluster/replica set, with one logical database per active bounded service. Current DATN-BE deployment owns `continuum_iam`, `continuum_capture`, `continuum_jira`, `continuum_lifecycle`, `continuum_chat`, `continuum_handover`, `continuum_ingestion`, and `continuum_notification`; cross-cutting audit is in `continuum_audit`. Do not use the former shared `continuum_db` for runtime domain writes. Product targets `continuum_task` and `continuum_ai_adapter` are not in the current BE runtime inventory; reconcile their service deployment before provisioning or migrating into them. See the workspace authority record `docs/adr/ADR-003-database-per-service-persistence.md` and the local [topology catalog](../database-design/README.md).

* **Tại sao dùng MongoDB?** Mô hình tri thức phần mềm (Knowledge Objects) có cấu trúc linh hoạt theo từng loại hình: Kiến trúc hệ thống, SOP quy trình triển khai, Báo cáo sự cố (Postmortem), Quyết định kỹ thuật (ADR). Cấu trúc Document-oriented của MongoDB cho phép lưu trữ snapshot nội dung bất biến (`knowledge_versions`) kèm siêu dữ liệu phong phú mà không cần migration bảng phức tạp.
* **Giao dịch ACID Đa tài liệu (Multi-Document ACID Transactions):** Khi một tri thức được phê duyệt trong Verification Inbox, hệ thống bắt buộc mở một Mongoose Session để:
  1. Tạo bản ghi `knowledge_versions` mới.
  2. Cập nhật `currentVersionId` và trạng thái `ACTIVE` trên `knowledge_objects`.
  3. Cập nhật trạng thái `SUPERSEDED` cho version cũ.
  4. Ghi nhận `knowledge_evidence` liên kết và nhật ký `audit_logs`.
  *Nếu bất kỳ bước nào lỗi, toàn bộ giao dịch bị `abortTransaction()`, đảm bảo tính toàn vẹn 100%.*
* **Đặc tả Schema chi tiết từng Service:** Xem toàn bộ thiết kế cơ sở dữ liệu vi dịch vụ tại [Document/database-design/](../database-design/README.md).

#### Task Service storage boundary

Task Service target dùng database logic riêng `continuum_task` trên replica set hiện có, cấu hình bằng `MONGODB_URI` + `SERVICE_DATABASE` theo mẫu các service hiện tại trong DATN-BE. Service sở hữu `tasks`, append-only `task_events` và `outbox_events` khi cần phát sự kiện bền vững. Ghi task mutation cùng history/outbox bằng transaction trong cùng database. Capture, Handover, Gateway và Agent không truy cập trực tiếp database này; chúng dùng Task API hoặc event contract. Đây là target service/database, chưa thuộc active BE runtime inventory. Không cần tạo MongoDB cluster vật lý hoặc repo mới.

Task Agent chỉ nhận task context mà API cho phép theo user/scope hiện hành. Bản rewrite/gợi ý được giữ ở dạng proposal; người có quyền xác nhận trước khi mutation cập nhật task canonical. Lịch sử ghi actor, nguồn Agent/proposal, field thay đổi, task version và correlation/operation ID; không lưu full prompt hoặc toàn bộ raw context mặc định. Xem [Task storage design](../database-design/12_TASK_MANAGEMENT_SCHEMA.md) và [ADR-010](../research-tech/ADR-010-task-service-in-existing-repositories.md).

### 1.2. PostgreSQL 16 + pgvector (Bộ Lưu Trữ SAG & Vũ Trụ Tri Thức 3D)
* **Tại sao dùng PostgreSQL 16 + pgvector (hoặc Qdrant)?**
  - **Hợp nhất ACID & Không lệch pha:** Thực thể quan hệ (Chunk, Event, Entity, Hyperedge) và Vector Embeddings nằm trong cùng một cơ sở dữ liệu. Khi xóa một tài liệu, toàn bộ vector và liên kết bị xóa theo `ON DELETE CASCADE`, loại bỏ triệt để rủi ro dữ liệu rác/lệch pha giữa relational DB và vector DB rời rạc.
  - **Single-Query Dynamic Retrieval:** Tìm kiếm vector kết hợp Dynamic SQL Hyperedges và lọc quyền bảo mật Pre-retrieval ACL (`allowed_roles`) gói gọn trong 1 câu truy vấn CTE duy nhất, độ trễ cực thấp (< 10ms).
  - **Hỗ trợ Vũ trụ Tri thức 3D (3D Knowledge Galaxy):** Lưu trữ trực tiếp tọa độ $x, y, z$, bán kính cụm module, và lịch sử góc quay camera thám hiểm (`universe_overviews`, `universe_partitions`, `exploration_steps`). Chi tiết xem tại [11_SAG_STORAGE_SCHEMA.md](../database-design/11_SAG_STORAGE_SCHEMA.md).
  - **Lựa chọn phân tán mở rộng:** Hỗ trợ kết nối **Qdrant** khi quy mô vector vượt ngưỡng chục triệu bản ghi.

### 1.3. Cloudflare R2 — Lưu trữ đối tượng đám mây (Object Storage)
* **Ưu điểm cốt lõi:** Tương thích 100% với S3 API nhưng **hoàn toàn miễn phí chi phí truyền tải ra ngoài (Zero Egress Fees)**.
* **Cơ chế Direct Presigned PUT:** Client tải file PDF/DOCX trực tiếp lên bucket private của R2 qua URL có chữ ký tạm thời. Backend không phải nhận file nhị phân qua RAM, giúp server không bao giờ bị nghẽn CPU/RAM khi người dùng upload file nặng hàng chục MB.

---

## 2. Hạ tầng Hàng đợi & Xử lý bất đồng bộ (BullMQ + Redis)

Để không chặn request người dùng khi thực hiện OCR, bóc tách AI, tính toán tọa độ 3D, phát event downstream hoặc gửi mail, các tác vụ nền phù hợp được đẩy qua **BullMQ** trên nền **Redis 7.2**.

```
[ Domain Services ] ──(Produce Job)──► [ Redis 7.2 BullMQ ]
                                              │
         ┌──────────────────┬─────────────────┼──────────────────┬──────────────────────┐
         ▼                  ▼                 ▼                  ▼                      ▼
  [ingestion-queue]  [task-event-relay]* [mail-queue]    [handover-queue]    [universe-projection]
         │                  │                 │                  │                      │
   (MarkItDown/OCR) (Optional Outbox)  (SMTP/Resend)     (Whisper Audio)     (UMAP/3D Force Layout)
         │                  │                 │                  │                      │
         └──────────────────┴────────┬────────┴──────────────────┴──────────────────────┘
                                     │ (Failed 3 Retries)
                                     ▼
                          [ dlq-failed-jobs ] ──► Ghi Audit Log & Alert Admin
```

### 2.1. Danh mục các hàng đợi chuyên biệt
* `task-event-relay` chỉ bật khi có consumer bất đồng bộ thực sự; outbox lưu trong database `continuum_task`, còn relay gửi event tới consumer. Nó không thay thế API đồng bộ cho task command.
1. **`ingestion-queue`:** Tiếp nhận file mới, tải byte từ R2, chuyển tiếp cho Worker bóc tách text và sinh vector vào PostgreSQL/Qdrant.
2. **`universe-projection`:** Khi có tài liệu mới hoặc cờ `universe_dirty_sources`, Worker tính toán lại phép chiếu không gian 3D (UMAP/Force-directed graph layout), cập nhật tọa độ $(x, y, z)$ và bán kính cụm module trên nền bất đồng bộ.
3. **`task-event-relay` (optional):** Chuyển tiếp event đã ghi vào outbox của Task Service tới notification/Agent consumers khi cần. Task CRUD và giao owner vẫn là lệnh HTTP đồng bộ; không thêm queue nếu không có consumer MVP.
4. **`mail-queue`:** Tiếp nhận các tác vụ gửi email giao dịch, email nhắc nhở cuối ngày và thông báo Verification Inbox.
5. **`handover-queue`:** Xử lý file ghi âm phỏng vấn, gọi model Whisper để chuyển speech-to-text và trích xuất câu hỏi mở.

### 2.2. Đường ống xử lý lỗi với Dead Letter Queue (DLQ Pipeline)
* **Cơ chế Exponential Backoff:** Khi một job gặp sự cố (ví dụ SAG downstream hoặc SMTP bị nghẽn), BullMQ tự động thử lại tối đa **3 lần** với độ trễ tăng theo lũy thừa thời gian:
  $$\Delta t = 2^n \times 1000\text{ms} \quad (2\text{s} \longrightarrow 4\text{s} \longrightarrow 8\text{s})$$
* **Dead Letter Queue (`dlq-failed-jobs`):** Nếu sau 3 lần vẫn thất bại, job sẽ bị đẩy vào DLQ. Hệ thống tự động ghi nhật ký vào `audit_logs` với cờ `SEVERITY: HIGH` và gửi thông báo cho Admin để can thiệp thủ công, tuyệt đối không làm thất thoát dữ liệu.

---

## 3. Kiến trúc SAG AI Engine & Phân luồng OCR

```
                     [ File Bytes từ Cloudflare R2 ]
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
        [ File văn bản chuẩn ]          [ File Scan / Ảnh chụp ]
        (PDF có text, DOCX, MD)         (PDF dạng ảnh, PNG, JPG)
                    │                             │
                    ▼                             ▼
          ┌───────────────────┐         ┌───────────────────┐
          │    MarkItDown     │         │    MinerU OCR     │
          │ (Bóc tách văn bản │         │ (Bóc tách công    │
          │  giữ cấu trúc MD) │         │  thức & bảng ảnh) │
          └─────────┬─────────┘         └─────────┬─────────┘
                    │                             │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    [ Markdown Cấu Trúc Thống Nhất ]
                                   │
                                   ▼
                    [ Header-Aware Chunking (512 tokens) ]
                                   │
                                   ▼
                    [ Vector Embedding (bge-m3 / text-emb-004) ]
                                   │
                                   ▼
                    [ Lưu trữ LanceDB + Hybrid Index BM25 ]
```

### 3.1. Phân luồng OCR thông minh (Dual OCR Routing)
* **Luồng 1 (MarkItDown):** Tối ưu hóa cho các tài liệu phần mềm văn bản (tài liệu thiết kế DOCX, README Markdown, PDF xuất từ Notion/Confluence). MarkItDown bóc tách cực nhanh, giữ nguyên các bảng biểu và khối code mà không tốn tài nguyên GPU.
* **Luồng 2 (MinerU OCR):** Kích hoạt khi phát hiện file scan, ảnh chụp màn hình kiến trúc hoặc PDF scan không có text layer. MinerU sử dụng mô hình thị giác máy tính để nhận diện cấu trúc bố cục đa cột, công thức toán học và bảng phức tạp.

### 3.2. Tìm kiếm lai (Hybrid Retrieval) & Provider-Agnostic LLM Gateway
* Khi có câu hỏi từ `svc_chat`, SAG AI Engine thực hiện **Hybrid Retrieval**:
  $$\text{Score} = \alpha \times \text{Score}_{\text{BM25}} + (1 - \alpha) \times \text{Score}_{\text{Vector}}$$
* Sau đó, các đoạn trích điểm cao nhất được đưa qua bộ **Reranker** để chọn ra Top-K bằng chứng chính xác nhất.
* **LLM Gateway:** Đóng gói giao tiếp qua adapter trừu tượng (`generate()`, `embed()`), hỗ trợ chuyển đổi linh hoạt giữa Google Gemini 2.5, OpenAI và các mô hình cục bộ mà không phải sửa code nghiệp vụ.
