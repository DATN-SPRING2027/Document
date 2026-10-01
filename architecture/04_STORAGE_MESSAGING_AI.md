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
│   │ MongoDB 7.0 Replica Set│  │ LanceDB (SAG MVP retrieval target)│  │ Cloudflare R2               │   │
│   │ (rs0 - 3 Nodes)        │  │ (derived index; runtime verify)    │  │ (Object Store)              │   │
│   ├────────────────────────┤  ├───────────────────────────────────┤  ├─────────────────────────────┤   │
│   │ • Source of Truth      │  │ • Retrieval index dẫn xuất        │  │ • File gốc PDF, DOCX, MD    │   │
│   │ • Nghiệp vụ, users, tasks│ │ • Chunk/embedding đủ điều kiện   │  │ • File ghi âm Handover       │   │
│   │ • Lịch sử phiên bản    │  │ • LanceDB theo target MVP         │  │ • Zero Egress Fees          │   │
│   │ • Audit Logs           │  │ • Không lưu task lifecycle        │  │ • S3 API Compatible         │   │
│   │ • ACID Transactions    │  │ • Runtime cần xác minh            │  │                             │   │
│   └────────────────────────┘  └───────────────────────────────────┘  └─────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.1. MongoDB 7.0 (3-Node Replica Set `rs0`) — Nguồn Chân Lý (Source of Truth)
MongoDB lưu bản ghi task canonical do Continuum Task API quản lý, cùng với dữ liệu vận hành khác. Các collection đề xuất `tasks` và `task_events` thuộc operational database hiện có (`continuum_db` theo DEC-011/SPEC-001), không tạo database riêng cho task. Transaction trên replica set bảo đảm một task mutation và event history được ghi cùng nhau. Work Note có thể giữ tham chiếu `taskId` tùy chọn; task không được sao chép thành nguồn dữ liệu riêng trong SAG.
* **Tại sao dùng MongoDB?** Mô hình tri thức phần mềm (Knowledge Objects) có cấu trúc linh hoạt theo từng loại hình: Kiến trúc hệ thống, SOP quy trình triển khai, Báo cáo sự cố (Postmortem), Quyết định kỹ thuật (ADR). Cấu trúc Document-oriented của MongoDB cho phép lưu trữ snapshot nội dung bất biến (`knowledge_versions`) kèm siêu dữ liệu phong phú mà không cần migration bảng phức tạp.
* **Giao dịch ACID Đa tài liệu (Multi-Document ACID Transactions):** Khi một tri thức được phê duyệt trong Verification Inbox, hệ thống bắt buộc mở một Mongoose Session để:
  1. Tạo bản ghi `knowledge_versions` mới.
  2. Cập nhật `currentVersionId` và trạng thái `ACTIVE` trên `knowledge_objects`.
  3. Cập nhật trạng thái `SUPERSEDED` cho version cũ.
  4. Ghi nhận `knowledge_evidence` liên kết và nhật ký `audit_logs`.
  *Nếu bất kỳ bước nào lỗi, toàn bộ giao dịch bị `abortTransaction()`, đảm bảo tính toàn vẹn 100%.*
* **Đặc tả Schema chi tiết từng Service:** Xem toàn bộ thiết kế cơ sở dữ liệu vi dịch vụ tại [Document/database-design/](../database-design/README.md).

### 1.2. LanceDB (SAG retrieval target cho MVP)
Theo Technology baseline và DEC-015/SPEC-005, LanceDB là target lưu retrieval/index của SAG trong MVP. Đây là dữ liệu dẫn xuất phục vụ truy hồi; MongoDB vẫn là source of truth cho task, quyền, Work Note và trạng thái tri thức.

- Chỉ Work Note/evidence vượt qua kiểm tra source eligibility và ACL của Continuum mới được lập chỉ mục. Task, title/description, status và assignee không phải nguồn index độc lập.
- SAG phải nhận phạm vi source được phép từ Continuum, áp dụng ACL hiện hành trước khi dựng LLM context và chặn kết quả ngay khi quyền bị thu hồi. De-index có thể chạy bất đồng bộ nhưng không được mở cửa sổ truy cập.
- LanceDB là target kiến trúc đã chấp nhận, không phải bằng chứng runtime hiện tại đã triển khai. Xác minh source/deployment riêng trước khi tuyên bố hoàn thành tích hợp.
- [11_SAG_STORAGE_SCHEMA.md](../database-design/11_SAG_STORAGE_SCHEMA.md) chứa nghiên cứu schema PostgreSQL + pgvector/Qdrant cho phương án thay thế/mở rộng; phần SQL đó không phải MVP storage contract. Thay đổi engine phải có ADR riêng.

### 1.3. Cloudflare R2 — Lưu trữ đối tượng đám mây (Object Storage)
* **Ưu điểm cốt lõi:** Tương thích 100% với S3 API nhưng **hoàn toàn miễn phí chi phí truyền tải ra ngoài (Zero Egress Fees)**.
* **Cơ chế Direct Presigned PUT:** Client tải file PDF/DOCX trực tiếp lên bucket private của R2 qua URL có chữ ký tạm thời. Backend không phải nhận file nhị phân qua RAM, giúp server không bao giờ bị nghẽn CPU/RAM khi người dùng upload file nặng hàng chục MB.

---

## 2. Hạ tầng Hàng đợi & Xử lý bất đồng bộ (BullMQ + Redis)

Để đảm bảo hệ thống không bị treo request khi người dùng thực hiện các thao tác tốn thời gian (OCR, bóc tách AI, tính toán tọa độ 3D, lập chỉ mục nguồn được phép, gửi mail), các tác vụ nền phù hợp được đẩy qua **BullMQ** trên nền **Redis 7.2**.

```
[ Domain Services ] ──(Produce Job)──► [ Redis 7.2 BullMQ ]
                                              │
         ┌──────────────────┬─────────────────┼──────────────────┬──────────────────────┐
         ▼                  ▼                 ▼                  ▼                      ▼
  [ingestion-queue]  [mail-queue]   [handover-queue]    [universe-projection]
         │                  │                 │                  │                      │
   (Parse/OCR/index)  (SMTP/Resend)    (Whisper Audio)   (UMAP/3D Force Layout)
         │                  │                 │                  │                      │
         └──────────────────┴────────┬────────┴──────────────────┴──────────────────────┘
                                     │ (Failed 3 Retries)
                                     ▼
                          [ dlq-failed-jobs ] ──► Ghi Audit Log & Alert Admin
```

### 2.1. Danh mục các hàng đợi chuyên biệt
1. **`ingestion-queue`:** Tiếp nhận nguồn đủ điều kiện, tải byte từ R2 khi cần, chuyển tiếp cho Worker bóc tách text và lập chỉ mục qua SAG/LanceDB adapter.
2. **`universe-projection`:** Khi có tài liệu mới hoặc cờ `universe_dirty_sources`, Worker tính toán lại phép chiếu không gian 3D (UMAP/Force-directed graph layout), cập nhật tọa độ $(x, y, z)$ và bán kính cụm module trên nền bất đồng bộ.
3. **`mail-queue`:** Tiếp nhận các tác vụ gửi email giao dịch, email nhắc nhở cuối ngày và thông báo Verification Inbox.
4. **`handover-queue`:** Xử lý file ghi âm phỏng vấn, gọi model Whisper để chuyển speech-to-text và trích xuất câu hỏi mở.

Task create/update/assignment/status requests remain synchronous Task API operations in the MVP; only eligible Work Note/evidence indexing uses background jobs. The source decision requires an author-confirmed Work Note and current source eligibility/ACL before indexing. Retrieval must reapply current ACL before returning chunks or constructing model context; revoked sources are blocked immediately and de-indexed asynchronously. LanceDB is the accepted MVP target; PostgreSQL + pgvector/Qdrant is an alternative/future-scale option only.

### 2.2. Đường ống xử lý lỗi với Dead Letter Queue (DLQ Pipeline)
* **Cơ chế Exponential Backoff:** Khi một job gặp sự cố (ví dụ SAG/index service hoặc SMTP bị nghẽn), BullMQ tự động thử lại tối đa **3 lần** với độ trễ tăng theo lũy thừa thời gian:
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
                    [ LanceDB target + Hybrid Retrieval Index ]
```

### 3.1. Phân luồng OCR thông minh (Dual OCR Routing)
* **Luồng 1 (MarkItDown):** Tối ưu hóa cho các tài liệu phần mềm văn bản (tài liệu thiết kế DOCX, README Markdown, PDF xuất từ Notion/Confluence). MarkItDown bóc tách cực nhanh, giữ nguyên các bảng biểu và khối code mà không tốn tài nguyên GPU.
* **Luồng 2 (MinerU OCR):** Kích hoạt khi phát hiện file scan, ảnh chụp màn hình kiến trúc hoặc PDF scan không có text layer. MinerU sử dụng mô hình thị giác máy tính để nhận diện cấu trúc bố cục đa cột, công thức toán học và bảng phức tạp.

### 3.2. Tìm kiếm lai (Hybrid Retrieval) & Provider-Agnostic LLM Gateway
* Khi có câu hỏi từ `svc_chat`, SAG AI Engine thực hiện **Hybrid Retrieval**:
  $$\text{Score} = \alpha \times \text{Score}_{\text{BM25}} + (1 - \alpha) \times \text{Score}_{\text{Vector}}$$
* Sau đó, các đoạn trích điểm cao nhất được đưa qua bộ **Reranker** để chọn ra Top-K bằng chứng chính xác nhất.
* **LLM Gateway:** Đóng gói giao tiếp qua adapter trừu tượng (`generate()`, `embed()`), hỗ trợ chuyển đổi linh hoạt giữa Google Gemini 2.5, OpenAI và các mô hình cục bộ mà không phải sửa code nghiệp vụ.
