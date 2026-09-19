# Continuum AI — Chi Tiết Các Domain Services (Services Deep-Dive)

> Nằm trong tài liệu kiến trúc tổng thể Continuum AI. Xem [Mục lục](README.md).

---

## 1. Tổng quan phân rã Domain Services

Kiến trúc backend của Continuum AI được phân tách thành **9 Bounded Services** (8 dịch vụ trên nền tảng **NestJS / TypeScript** và 1 dịch vụ AI Engine độc lập bằng **FastAPI / Python**).

Mỗi dịch vụ tuân thủ nguyên tắc **Đơn trách nhiệm (Single Responsibility Principle - SRP)** và được tổ chức theo cấu trúc Clean Architecture 4 tầng.

---

## 2. Chi tiết 9 Bounded Services

### 2.1. `svc_iam` (Authentication, Session & Identity Governance)
* **Thư mục:** `backend/src/modules/auth/` và `backend/src/modules/identity/`
* **Trách nhiệm:** 
  - Đăng nhập, đăng ký thành viên nội bộ, băm mật khẩu Bcrypt 12 rounds.
  - Cấp phát Access Token (JWT có Scoped Claims: `userId`, `orgId`, `roles`, `projectIds`) và Refresh Token.
  - Quản lý phiên an toàn (`refresh_sessions`) với cơ chế **Refresh Token Rotation & Reuse Detection**.
  - Quản lý 3 roles tĩnh: `ADMIN` (tổ chức), `TEAM_LEADER` (nhóm), `MEMBER` (thành viên).
  - Quản lý quyền tạo dự án riêng biệt (`organization_capability_grants` với mã `project.create`).
* **Collections sở hữu:** `users`, `organizations`, `projects`, `teams`, `project_memberships`, `team_memberships`, `roles`, `role_assignments`, `organization_capability_grants`, `refresh_sessions`.
* **API Endpoints chính:**
  - `POST /api/v1/auth/login`: Xác thực và cấp token.
  - `POST /api/v1/auth/refresh`: Đổi token mới, hủy token cũ trong `refresh_sessions`.
  - `POST /api/v1/auth/logout`: Đưa `jti` vào Redis Blacklist (<1ms).
  - `POST /api/v1/iam/projects/:id/members`: Thêm thành viên vào dự án.
  - `POST /api/v1/iam/grants/project-create`: Admin cấp quyền tạo project cho Team Leader.

---

### 2.2. `svc_capture` (Daily Knowledge Capture & Worklogs)
* **Thư mục:** `backend/src/modules/work-notes/`
* **Trách nhiệm:**
  - Thu thập ghi chú công việc hàng ngày của dev: What/How/Why, blockers, next steps, evidence.
  - Tự động lấy các issue Jira mà dev vừa làm trong ngày để điền sẵn vào form (Prefill).
  - **Quy tắc bất biến:** Ghi chú chỉ trở thành nguồn tri thức hợp lệ khi **chính tác giả tự tay bấm xác nhận (Author-confirmed)**.
  - Lưu trữ lịch sử chỉnh sửa bất biến vào `work_note_versions`.
* **Collections sở hữu:** `work_notes`, `work_note_versions`, `knowledge_requirements`.
* **API Endpoints chính:**
  - `GET /api/v1/capture/daily/prefill?date=YYYY-MM-DD`: Lấy task Jira điền sẵn.
  - `POST /api/v1/capture/daily`: Tạo bản nháp ghi chú ngày.
  - `PUT /api/v1/capture/daily/:id/confirm`: Tác giả xác nhận nội dung.

---

### 2.3. `svc_jira` (Jira Cloud Connector & Reconciliation)
* **Thư mục:** `backend/src/modules/jira/`
* **Trách nhiệm:**
  - Tiếp nhận Webhook từ Atlassian Jira Cloud (Issue Created, Updated, Comment Added).
  - **Khử trùng lặp (Idempotency):** Dùng Redis `SETNX` với key `jira:event:{eventId}` (TTL 86,400s). Nếu nhận trùng event thì drop ngay lập tức.
  - Đẩy payload hợp lệ vào hàng đợi BullMQ `jira-sync-queue`.
  - Chạy Reconciliation Cronjob quét đối soát lúc 02:00 AM để phát hiện và đồng bộ bù các event bị lỡ do mạng.
* **Collections sở hữu:** `jira_connections`, `jira_account_links`, `jira_issues`, `jira_events`, `jira_sync_jobs`.
* **API Endpoints chính:**
  - `POST /api/v1/integrations/jira/webhook`: Tiếp nhận webhook Jira.
  - `POST /api/v1/integrations/jira/connect`: Thiết lập kết nối OAuth2/Token với Jira Site.
  - `POST /api/v1/integrations/jira/sync-now`: Kích hoạt đồng bộ thủ công.

---

### 2.4. `svc_lifecycle` (Verification Inbox & Knowledge Lifecycle)
* **Thư mục:** `backend/src/modules/knowledge/`
* **Trách nhiệm:**
  - Cung cấp Hộp thư kiểm chứng (**Verification Inbox**) cho SME và Team Leader theo đúng domain được phân công.
  - Quản lý máy trạng thái vòng đời tri thức:
    $$\text{PROPOSED} \longrightarrow \text{UNDER\_REVIEW} \longrightarrow \text{VERIFIED / ACTIVE} \longrightarrow \text{SUPERSEDED / DEPRECATED}$$
  - **Giao dịch ACID Đa tài liệu:** Khi phê duyệt, tạo một `knowledge_versions` mới, cập nhật version cũ thành `SUPERSEDED`, ghi nhận `knowledge_evidence` và log `knowledge_verifications` trong cùng 1 Mongoose Transaction.
  - Định kỳ quét các module quá hạn review (`cadenceDays`) để sinh ra `knowledge_gaps`.
* **Collections sở hữu:** `knowledge_objects`, `knowledge_proposals`, `knowledge_versions`, `knowledge_evidence`, `knowledge_verifications`, `knowledge_gaps`, `knowledge_conflicts`.
* **API Endpoints chính:**
  - `GET /api/v1/lifecycle/inbox`: Lấy danh sách tri thức chờ duyệt theo scope của user.
  - `POST /api/v1/lifecycle/proposals/:id/verify`: Phê duyệt hoặc từ chối tri thức đề xuất.
  - `GET /api/v1/lifecycle/gaps`: Xem danh sách khoảng trống tri thức.

---

### 2.5. `svc_chat` (Cited Assistant & RAG Engine)
* **Thư mục:** `backend/src/modules/chat/`
* **Trách nhiệm:**
  - Xử lý câu hỏi của người dùng, phân tích ý định (Query Planning).
  - **Pre-Retrieval Scoped ACL:** Tính toán tập quyền hiệu lực $P_{\text{eff}}$ và gửi kèm truy vấn sang FastAPI SAG Engine để giới hạn không gian tìm kiếm.
  - **Trích dẫn minh bạch (Citation Grounding):** Ráp nối các đoạn trích từ vector store với `knowledge_evidence` trong MongoDB để hiển thị nguồn gốc câu trả lời.
  - **Chống ảo giác (No Hallucination):** Nếu điểm tương đồng thấp hoặc thiếu bằng chứng, trả về `INSUFFICIENT_EVIDENCE` và hỗ trợ 1-click tạo `knowledge_gaps`.
* **Collections sở hữu:** `chat_sessions`, `chat_messages`, `query_logs`, `retrieval_logs`.
* **API Endpoints chính:**
  - `POST /api/v1/chat/sessions`: Khởi tạo phiên trò chuyện.
  - `POST /api/v1/chat/sessions/:id/messages`: Gửi câu hỏi, stream câu trả lời qua SSE.
  - `POST /api/v1/chat/sessions/:id/report-gap`: Báo cáo khoảng trống tri thức từ câu hỏi chưa trả lời được.

---

### 2.6. `svc_handover` (Handover & Audio Continuity Service)
* **Thư mục:** `backend/src/modules/handover/`
* **Trách nhiệm:**
  - Khởi tạo quy trình bàn giao khi một thành viên hoặc Team Leader rời dự án / đổi nhóm.
  - Tự động phân tích trách nhiệm (`responsibilities`): module sở hữu, tài liệu đứng tên, task còn dang dở.
  - Gán người kế nhiệm (`SUCCESSOR`) và sinh gói bàn giao (**Handover Package**) có checklist ưu tiên.
  - **Host phiên phỏng vấn Audio:** Mở kết nối WebSocket tại `/ws/handover`, nhận luồng âm thanh từ microphone client, đẩy lên Cloudflare R2 và đưa vào `handover-queue` để gọi Whisper API trích xuất transcript.
  - Tự động tổng hợp lộ trình học việc (**Successor Learning Path**) cho nhân sự mới.
* **Collections sở hữu:** `handovers`, `handover_items`, `handover_assignments`, `responsibilities`, `responsibility_assignments`, `interviews`, `interview_sessions`, `learning_paths`.
* **API Endpoints chính:**
  - `POST /api/v1/handovers/initiate`: Khởi tạo bàn giao trách nhiệm.
  - `GET /api/v1/handovers/:id/package`: Lấy gói tài liệu và checklist bàn giao.
  - `PUT /api/v1/handovers/:id/items/:itemId/signoff`: Leader/SME xác nhận hoàn thành mục bàn giao.
  - `WS /ws/handover`: Kênh WebSocket nhận audio stream phỏng vấn.

---

### 2.7. `svc_ingestion` (Ingestion Coordinator Service)
* **Thư mục:** `backend/src/modules/storage/` và `backend/src/modules/ingestion/`
* **Trách nhiệm:**
  - Tiếp nhận yêu cầu upload tài liệu (PDF, DOCX, Markdown, TXT, Ảnh).
  - Cấp **Presigned PUT URL** để Client tải trực tiếp file lên Cloudflare R2 (không qua backend để bảo toàn CPU).
  - Xác thực mã băm SHA-256 của file để chống upload trùng lặp.
  - Tạo bản ghi trong `ingestion_jobs` và đẩy job vào BullMQ `ingestion-queue` để kích hoạt worker phân tách tài liệu.
  - Lưu trữ ánh xạ chunk vector vào `sag_mappings`.
* **Collections sở hữu:** `sources`, `source_acls`, `documents`, `document_versions`, `ingestion_jobs`, `sag_mappings`.
* **API Endpoints chính:**
  - `POST /api/v1/ingestion/presign`: Lấy URL tải trực tiếp lên Cloudflare R2.
  - `POST /api/v1/ingestion/complete`: Thông báo upload xong để xếp hàng bóc tách.
  - `GET /api/v1/ingestion/jobs/:id/status`: Kiểm tra tiến độ OCR và Indexing.

---

### 2.8. `svc_notification` (Notification & Mail Service)
* **Thư mục:** `backend/src/modules/notifications/`
* **Trách nhiệm:**
  - Là người tiêu thụ (Consumer/Worker) của hàng đợi BullMQ `mail-queue`.
  - Kết nối với nhà cung cấp email đám mây (`edge_mail` - SMTP / Resend / SendGrid) để gửi email giao dịch: Kích hoạt tài khoản, OTP Reset Password.
  - **Cronjob nhắc nhở lúc 17:30:** Gửi email cho các dev chưa xác nhận Daily Note trong ngày.
  - Gửi email cảnh báo tức thời cho SME khi có tri thức mới xuất hiện trong Verification Inbox.
  - Bắn thông báo In-App thời gian thực qua Redis Pub/Sub đến Client qua WebSocket.
* **Hàng đợi liên kết:** BullMQ `mail-queue`, Redis Pub/Sub channel `user:notify:{userId}`.
* **API Endpoints chính:**
  - `GET /api/v1/notifications`: Lấy danh sách thông báo chưa đọc.
  - `PUT /api/v1/notifications/:id/read`: Đánh dấu đã xem thông báo.

---

### 2.9. `svc_ai_engine` (SAG AI Engine - FastAPI / Python)
* **Thư mục:** `ai-service/app/`
* **Trách nhiệm:**
  - **Bộ định tuyến OCR kép:**
    * File văn bản chuẩn (PDF text, DOCX, MD): Xử lý bằng **MarkItDown** để giữ cấu trúc bảng biểu và header.
    * File scan hoặc ảnh chụp: Định tuyến qua **MinerU OCR** để bóc tách chữ và công thức.
  - **Chunking & Embedding:** Chia văn bản theo Markdown headers (kích thước 512 tokens, overlap 10%), sinh vector nhúng.
  - **Quản lý Vector Store:** Đọc/ghi bảng vector trên **LanceDB** cục bộ với chỉ mục disk-backed IVF-PQ / HNSW.
  - **Hybrid Search & Reranker:** Kết hợp tìm kiếm từ khóa (BM25) và tìm kiếm ngữ nghĩa vector theo bộ lọc Scoped ACL.
  - **LLM Gateway:** Tích hợp đa mô hình (Gemini 2.5 Flash/Pro, Whisper API, OpenAI fallback).
* **API Endpoints nội bộ (mTLS / Internal HTTP):**
  - `POST /api/v1/sag/parse-and-index`: Bóc tách file từ R2 và lập chỉ mục vào LanceDB.
  - `POST /api/v1/sag/hybrid-search`: Tìm kiếm đoạn trích kèm Scoped ACL filter.
  - `POST /api/v1/sag/llm/generate-proposal`: Trích xuất đề xuất tri thức từ evidence.
  - `POST /api/v1/sag/audio/transcribe`: Chuyển giọng nói phỏng vấn thành văn bản qua Whisper.
