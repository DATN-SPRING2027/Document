# Continuum AI — Kiến Trúc Hệ Thống (System Architecture)

> **Dự án:** Continuum AI — Nền tảng kế thừa và chuyển giao tri thức dự án phần mềm  
> **Phiên bản kiến trúc:** 2.0 (Approved Architecture Baseline)  
> **Sơ đồ tương tác trực quan:** [architecture_diagram.html](../diagram/architecture_diagram.html)  

---

## 1. Giới thiệu & Triết lý thiết kế

Continuum AI không phải là một kho lưu trữ tài liệu tĩnh hay một chatbot hỏi đáp chung chung. Hệ thống được thiết kế xoay quanh mục tiêu cốt lõi: **Ghi nhận tri thức liên tục khi đang làm việc ➔ Kiểm chứng bởi chuyên gia (SME) ➔ Phát hiện khoảng trống tri thức ➔ Tự động hóa bàn giao cho người kế nhiệm khi có sự thay đổi nhân sự**.

### Các nguyên tắc bất biến (Architecture Invariants):
1. **Human-in-the-loop (Con người là chốt chặn cuối cùng):** AI chỉ đóng vai trò đề xuất (`PROPOSED`). Bắt buộc SME hoặc Team Leader có thẩm quyền xác nhận thì tri thức mới chuyển sang trạng thái hoạt động (`ACTIVE`).
2. **Pre-Retrieval Scoped ACL:** Tính toán tập quyền hiệu lực ($P_{\text{eff}}$) của người dùng **trước khi** truy vấn Vector Database/SAG để triệt tiêu hoàn toàn nguy cơ rò rỉ tài liệu mật.
3. **Evidence-Grounded Citations (Trích dẫn minh bạch):** Mọi câu trả lời của trợ lý AI bắt buộc phải đính kèm trích dẫn (Document ID, Locator, Hash, Version). Nếu không đủ bằng chứng, hệ thống trả về `INSUFFICIENT_EVIDENCE` và ghi nhận một Knowledge Gap thay vì bịa đặt (hallucination).
4. **Source of Truth phân định rõ ràng:** MongoDB 7.0 là nơi lưu trữ sự thật duy nhất về nghiệp vụ, vòng đời, quyền và lịch sử kiểm toán. LanceDB chỉ là bản sao chỉ mục phục vụ truy hồi (retrieval index).

---

## 2. Bản đồ cấu trúc tài liệu kiến trúc (Architecture Map)

Nhằm tránh việc phình to kích thước tệp và giúp các kỹ sư, giảng viên phản biện dễ dàng tra cứu, toàn bộ tài liệu kiến trúc được module hóa thành các phần chuyên biệt:

```
Document/architecture/
├── README.md                          # [Tài liệu hiện tại] Tổng quan, mục lục và ma trận công nghệ
├── 01_SYSTEM_TOPOLOGY.md              # Topo hệ thống, phân tầng mạng Ingress, API Gateway & VPC
├── 02_FRONTEND_NEXTJS.md              # Kiến trúc Next.js App Router, SSR/CSR, State & Streaming
├── 03_SERVICES_DEEP_DIVE.md           # Chi tiết 9 Domain Services (Clean Architecture 4 tầng)
├── 04_STORAGE_MESSAGING_AI.md         # Lưu trữ (MongoDB, LanceDB, R2), BullMQ & SAG AI Engine
├── 05_SECURITY_AND_GOVERNANCE.md      # Bảo mật, Rate Limiting, Race Conditions, RBAC & Caching
├── 06_CONTAINER_ORCHESTRATION_K8S.md  # Điều phối Microservices Kubernetes, HPA, Probes & Helm
└── 07_RELIABILITY_CAPACITY_OBSERVABILITY.md # Vận hành trên ít server, Capacity, Sizing & Saga

### Hướng dẫn tra cứu nhanh:
* **Muốn hiểu luồng mạng, ingress, cân bằng tải:** Xem [01_SYSTEM_TOPOLOGY.md](01_SYSTEM_TOPOLOGY.md).
* **Muốn nắm cách tổ chức giao diện Next.js, Server vs Client components:** Xem [02_FRONTEND_NEXTJS.md](02_FRONTEND_NEXTJS.md).
* **Muốn xem cấu trúc mã nguồn, DTO, Repository của từng backend service:** Xem [03_SERVICES_DEEP_DIVE.md](03_SERVICES_DEEP_DIVE.md).
* **Muốn hiểu cách vận hành MongoDB, Vector LanceDB, OCR MinerU/MarkItDown, BullMQ:** Xem [04_STORAGE_MESSAGING_AI.md](04_STORAGE_MESSAGING_AI.md).
* **Muốn xem quy tắc bảo mật 3 roles, Rate Limiting, Redlock chống race conditions:** Xem [05_SECURITY_AND_GOVERNANCE.md](05_SECURITY_AND_GOVERNANCE.md).
* **Muốn xem kiến trúc điều phối cụm Kubernetes, StatefulSet, HPA, Probes & Helm Charts:** Xem [06_CONTAINER_ORCHESTRATION_K8S.md](06_CONTAINER_ORCHESTRATION_K8S.md).
* **Muốn xem cách tính toán RAM/CPU, chống sập OOM khi ít server, Saga và Backup 0đ:** Xem [07_RELIABILITY_CAPACITY_OBSERVABILITY.md](07_RELIABILITY_CAPACITY_OBSERVABILITY.md).

---

## 3. Ma trận ngăn xếp công nghệ (Technology Stack Matrix)

| Tầng kiến trúc | Công nghệ đã phê duyệt | Trách nhiệm chính |
| :--- | :--- | :--- |
| **Frontend Framework** | **Next.js 16 (App Router)**, React 19, TypeScript | Hybrid Rendering (SSR/SSG/Client Components), Route Handlers, Streaming UI |
| **UI Design System** | **TailAdmin** for Next.js / Tailwind CSS | Dashboard layout, Bảng biểu, Form kiểm chứng, Visual tokens |
| **Client State** | **TanStack Query v5** + **Zustand** | Quản lý Server Cache, Optimistic UI và Local UI state nhẹ |
| **Container Orchestration** | **Kubernetes (K8s)** & **Helm v3** | Điều phối Microservices, StatefulSets, HPA Auto-scaling, Self-healing, Probes |
| **Ingress & Edge** | **Nginx L7 Reverse Proxy / K8s Ingress** | TLS Termination, Gzip/Brotli, WebSocket Upgrade, WAF/Rate limit |
| **Core API Gateway** | **NestJS API Gateway** (hoặc Nginx Reverse) | JWT Claims extraction, Token Blacklist check (<1ms), Global Routing |
| **Core Backend (VPC)** | **Node.js, NestJS, TypeScript** | 8 Domain Services: Nghiệp vụ, RBAC, Vòng đời, Handover, Jira sync |
| **AI Retrieval Service** | **Python, FastAPI (SAG Engine)** | Độc lập: OCR bóc tách (MarkItDown/MinerU), Embedding, Hybrid Search |
| **Primary Database** | **MongoDB 7.0 (3-Node Replica Set)** | **Source of Truth**: Lưu entities, revisions, audit logs, Jira mappings |
| **Vector Store** | **LanceDB** (Disk-backed IVF-PQ / HNSW) | Chỉ mục vector cục bộ phục vụ ngữ nghĩa, nhúng trực tiếp trong SAG |
| **Object Storage** | **Cloudflare R2** (S3 SDK Adapter fallback) | Private file originals (PDF, DOCX, Ảnh), OCR artifacts, Audio recordings |
| **In-Memory & Cache** | **Redis 7.2 In-Memory Cluster** | Distributed Cache L2, SingleFlight Mutex, Token Blacklist, Pub/Sub realtime |
| **Asynchronous Jobs** | **BullMQ (Redis-backed)** | Phân phối tác vụ nền: `ingestion-queue`, `jira-sync`, `mail-queue`, `DLQ` |
| **External Integrations** | **Jira Cloud REST v3** + **SMTP / Resend** | Jira ticket sync, Transactional email alerts |
| **LLM Gateway** | **Provider-Agnostic Adapter** | Tích hợp Google Gemini 2.5 Flash / Pro, Whisper API, OpenAI fallback |
