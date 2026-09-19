# Continuum AI — Thiết Kế Tầng Lưu Trữ Tri Thức Sau Trích Xuất (SAG Storage)
## (Bản Đối Chiếu Schema Gốc Zleap-AI/SAG & Bản Tinh Chỉnh Áp Dụng Cho Continuum AI)

> **Tài liệu:** Đặc tả kỹ thuật Cơ sở dữ liệu Tri thức sau Trích xuất (Post-Extraction Knowledge Store)  
> **Hệ quản trị CSDL quan hệ:** **PostgreSQL 16** (Database: `continuum_sag_storage`)  
> **Kho Vector Lưu Trữ:** **PostgreSQL 16 pgvector** (Mặc định hợp nhất) hoặc **Qdrant** (Lựa chọn chuyên dụng phân tán)  
> **Service sở hữu & điều phối:** `svc_ai_engine` (Orchestrator) & `svc_ingestion` (Feeder)  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ & Vai Trò Trong Dự Án

Trong Continuum AI, **MongoDB 7.0 là Source of Truth** cho toàn bộ dữ liệu nghiệp vụ: tài khoản, phân quyền (IAM), ghi chú công việc (Capture), liên kết Jira, vòng đời tri thức bất biến (Lifecycle), gói bàn giao (Handover) và kiểm toán (Audit).

Tuy nhiên, đối với bài toán **Truy vấn Tri thức Chuyên sâu (Semantic Search, Multi-hop Reasoning & Graph Retrieval)**:
- Dữ liệu văn bản kỹ thuật (SRS, Architecture, API Specs, Meeting STT, Jira Issues) sau khi bóc tách cần một **Bộ lưu trữ dữ liệu sau extract chuyên dụng (Post-Extraction Store)**.
- Dự án chuẩn hóa trên **PostgreSQL 16 kết hợp extension pgvector** dựa trên nguyên lý kiến trúc của **Zleap-AI/SAG (SQL-Retrieval Augmented Generation)**: Thay vì tách biệt 2 hệ thống lưu trữ rời rạc (Relational DB và Vector DB riêng) dễ gây lệch pha dữ liệu khi xóa/sửa, hệ thống hợp nhất toàn bộ thực thể quan hệ (Chunk, Event, Entity, Hyperedge) và các Vector Embeddings vào **duy nhất một Database PostgreSQL 16 + pgvector**.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│              CONTINUUM AI ➔ KIẾN TRÚC LƯU TRỮ DỮ LIỆU SAU EXTRACT (SAG STORAGE)                   │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                  │
│   [MongoDB 7.0 (Source of Truth)]          [Cloudflare R2 (Object Storage)]                      │
│     - document_versions (Raw & Parsed)       - Original PDF, DOCX, Audio Recordings              │
│     - sag_mappings (Bridge Continuum ⟷ SAG)                                                      │
│                        │                                                                         │
│                        ▼ (Async Extraction Worker / LLM Pipeline)                                │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────┐  │
│   │               CONTINUUM_SAG_STORAGE (Hợp Nhất Trên PostgreSQL 16 + pgvector)              │  │
│   │                                                                                           │  │
│   │   1. TẦNG QUAN HỆ HYPERGRAPH (Relational SQL Schema)                                      │  │
│   │      ├── data_source       : Cấu hình phân vùng tri thức theo Organization / Project       │  │
│   │      ├── kb_document       : Siêu dữ liệu tài liệu sau bóc tách text                       │  │
│   │      ├── source_chunk      : Các đoạn văn bản phân rã ngữ nghĩa kèm Heading hierarchy     │  │
│   │      ├── entity_type       : Danh mục kiểu thực thể chuẩn kỹ nghệ phần mềm                │  │
│   │      ├── entity            : Thực thể trích xuất (name, description, heat frequency)      │  │
│   │      ├── source_event      : Sự kiện / Fact nghiệp vụ được bóc tách từ đoạn văn bản       │  │
│   │      └── event_entity      : XƯƠNG SỐNG HYPERGRAPH (N-N join Event ⟷ Entity với trọng số) │  │
│   │                                                                                           │  │
│   │   2. TẦNG VECTOR EMBEDDINGS (pgvector Extension hoặc Qdrant)                              │  │
│   │      ├── chunk_vectors             : Cột kiểu vector(1024/1536) có chỉ mục HNSW Cosine    │  │
│   │      └── chunk_heading_vectors     : Vector Embeddings của Heading phân cấp ngữ cảnh      │  │
│   │                                                                                           │  │
│   │   3. TẦNG VŨ TRỤ TRI THỨC 3D (3D Knowledge Galaxy & Exploration)                          │  │
│   │      ├── universe_overviews        : Bản chụp không gian 3D Bounding Box theo Project     │  │
│   │      ├── universe_partitions       : Tinh thể module x, y, z, radius & mật độ tri thức    │  │
│   │      ├── universe_dirty_sources    : Cờ hiệu tính toán phép chiếu 3D bất đồng bộ          │  │
│   │      └── exploration_sessions/steps: Lịch sử bay thám hiểm & Tọa độ Camera 3D            │  │
│   └───────────────────────────────────────────────────────────────────────────────────────────┘  │
│                   │                                                           │                  │
│                   ▼ (Dynamic SQL JOIN + Cosine Distance <=> + ACL)            ▼ (Three.js WebGL) │
│   [svc_chat] ➔ Trả về câu trả lời kèm Exact Citations    [Next.js 3D Galaxy Canvas] ➔ Trực quan  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. PHẦN I: Khảo Sát Schema Gốc Có Sẵn Của Repo `Zleap-AI/SAG`

Khảo sát trực tiếp từ mã nguồn repository [Zleap-AI/SAG](https://github.com/Zleap-AI/SAG) (dựa trên FastAPI backend và thư viện lõi `zleap-sag==0.12.0`), cơ sở dữ liệu của SAG gốc được chia làm 2 tầng rõ rệt:

### 2.1. Tầng 1: SAG Platform API DB (`apps/api/sag_api/db/models/`)
Quản lý người dùng, nguồn dữ liệu và giao diện của bản thân ứng dụng SAG độc lập:
1. `users`: Tài khoản người dùng nội bộ của SAG (`id`, `email`, `hashed_password`, `role`).
2. `sources`: Nguồn tài liệu nạp vào (`id`, `name`, `type`, `status`).
3. `documents`: Danh sách tệp đính kèm nạp vào từng source (`id`, `source_id`, `filename`, `content_type`, `size_bytes`, `storage_path`, `status`, `token_usage`).
4. `agents`: Cấu hình Agent trò chuyện riêng của SAG (`id`, `name`, `system_prompt`, `is_default`).
5. `jobs`: Quản lý tiến trình xử lý bất đồng bộ (`id`, `type`, `payload`, `status`).
6. `settings`: Cấu hình khóa API của LLM / Embedding model.
7. `universe_*` (`universe_overviews`, `universe_partitions`, `universe_dirty_sources`): Phục vụ hiển thị mô hình không gian 3D đồ thị tri thức trên nền web Three.js.
8. `octx_*` (`octx_assets`, `octx_releases`, `octx_installations`, `octx_transfers`, `octx_operation_leases`): Hệ thống quản lý và chia sẻ các gói tri thức (OCTX protocol).

### 2.2. Tầng 2: Core Engine Storage (`zleap.sag.DataEngine`)
Tầng này chịu trách nhiệm trích xuất và lưu trữ cấu trúc tri thức thực sự:
- **Cơ sở dữ liệu quan hệ (Relational - SQLite / PostgreSQL):**
  - `data_source` (trước đây là `source_config`): Cấu hình phân vùng tri thức.
  - `kb_document`: Tài liệu tri thức gốc.
  - `source_chunk`: Các đoạn văn bản sau khi chia nhỏ (`id`, `heading`, `content`, `rank`).
  - `entity_type`: Bảng loại thực thể (`code`, `name`, `description`).
  - `entity`: Bảng thực thể trích xuất (`id`, `name`, `type`, `description`, `heat`).
  - `source_event`: Bảng sự kiện / luận cứ trích xuất (`id`, `title`, `summary`, `content`, `category`, `rank`, `parent_id`, `chunk_id`, `start_time`).
  - `event_entity`: Bảng liên kết N-N giữa Event và Entity (`event_id`, `entity_id`, `weight`, `description`).
- **Kho Vector (LanceDB / pgvector):**
  - `chunk_vectors`: Vector embeddings của văn bản chunk.
  - `chunk_heading_vectors`: Vector embeddings của các tiêu đề mục.

---

## 3. PHẦN II: Ma Trận Phân Tích Thay Đổi (Gap Analysis & Customization Matrix)

Để áp dụng vào Continuum AI — một nền tảng kế thừa tri thức phần mềm cấp doanh nghiệp đa tổ chức (Multi-Tenant) — chúng ta **không sử dụng nguyên si 100% ứng dụng SAG độc lập**, mà thực hiện các thay đổi kỹ thuật then chốt sau:

| Bảng / Thành phần | Hiện trạng SAG Gốc | Thay đổi áp dụng vào Continuum AI | Lý do & Rationale Kỹ Thuật |
| :--- | :--- | :--- | :--- |
| **`users`, `agents`** | Có sẵn trong SAG Platform DB | **LOẠI BỎ HOÀN TOÀN** khỏi SAG Storage | Continuum AI đã có vi dịch vụ [01_SVC_IAM_SCHEMA.md](01_SVC_IAM_SCHEMA.md) độc lập với 3 roles tĩnh (`ADMIN`, `TEAM_LEADER`, `MEMBER`) và `continuum_iam`. Không lưu người dùng trùng lặp. |
| **`chat_conversation`, `chat_message`** | Có sẵn trong SAG Platform DB | **LOẠI BỎ KHỎI SAG** | Lịch sử chat, phiên hỏi đáp và trích dẫn citations do [05_SVC_CHAT_SCHEMA.md](05_SVC_CHAT_SCHEMA.md) quản lý tập trung trong `continuum_chat`. |
| **`universe_*` & `exploration_*` (3D Knowledge Galaxy)** | Lưu tọa độ `x, y, z`, `radius`, cụm module và camera | **CHÍNH THỨC SỬ DỤNG & NÂNG CẤP THÀNH ĐIỂM NHẤN CỐT LÕI (WOW-FACTOR)** | Trực quan hóa toàn cảnh tri thức dự án thành một **"Vũ Trụ / Thiên Hà Tri Thức 3D"** (Interactive 3D Knowledge Galaxy trên Three.js). Người kế nhiệm có thể bay qua các tinh cầu module, xem mật độ tri thức, và camera tự động zoom vào đúng bằng chứng khi hỏi đáp. |
| **`octx_*` (Gói chuyển giao)** | Gói xuất/nhập tri thức tĩnh | **GIỮ CHUẨN ĐỂ MỞ RỘNG GIAI ĐOẠN 2** | Sẽ dùng làm định dạng export gói tri thức khi kỹ sư bàn giao rời dự án (Offline Handover Archive). |
| **Multi-Tenancy (`organization_id`, `project_id`)** | SAG gốc **KHÔNG CÓ**, chỉ có `user_id` đơn lẻ | **BẮT BUỘC BỔ SUNG vào tất cả các bảng** | Đảm bảo tính cô lập dữ liệu tuyệt đối giữa các công ty và các dự án trong Continuum AI. Không để lộ tri thức chéo tenant. |
| **Phân loại Nguồn Tri thức (`source_type`)** | SAG gốc chỉ coi mọi nguồn là Document tệp phẳng | **BỔ SUNG trường `source_type`**: `DOCUMENT`, `JIRA_ISSUE`, `WORK_NOTE`, `AUDIO_HANDOVER` | Tri thức dự án phần mềm đa dạng từ ghi chú hàng ngày (Work Note), task Jira, đến bóc băng phỏng vấn bàn giao (Audio STT). |
| **Bảo mật Trước Truy Vấn (Pre-retrieval ACL)** | SAG gốc **KHÔNG CÓ**, bất kỳ ai search cũng thấy toàn bộ | **BỔ SUNG `confidentiality_level` & `allowed_roles`** vào `kb_document`, `source_chunk`, `source_event` | Kỹ sư cấp `MEMBER` không được phép tìm thấy thông tin tài chính/hợp đồng dự án cấp `ADMIN` hoặc `TEAM_LEADER`. Phải lọc quyền ngay từ tầng SQL JOIN. |
| **Liên kết Ngược MongoDB (`continuum_ref_id`)** | SAG gốc sinh UUID ngẫu nhiên không trace được | **BỔ SUNG `continuum_document_version_id`, `continuum_source_id`** | Cho phép frontend khi nhấp vào Citation link có thể đối chiếu tức thì về document gốc trong MongoDB mà không bị mất dấu. |
| **Danh mục `entity_type`** | SAG gốc để rỗng hoặc generic | **CHUẨN HÓA DANH MỤC THỰC THỂ PHẦN MỀM** | Định nghĩa tập thực thể chuyên biệt: `TECH_STACK`, `MODULE_SERVICE`, `ARCHITECTURE_DECISION`, `API_CONTRACT`, `BUSINESS_RULE`, `ROLE_RESPONSIBILITY`. |

---

## 4. PHẦN III: Đặc Tả Schema Đã Tinh Chỉnh Áp Dụng Cho Continuum AI

Dưới đây là đặc tả SQL DDL của **Bộ lưu trữ dữ liệu sau extract (`continuum_sag_storage`)** đã tích hợp các thuộc tính đặc thù của Continuum AI:

### 4.1. `data_source` (Không Gian Tri Thức Phân Vùng Dự Án)
Mỗi dự án trong Continuum AI tương ứng với 1 hoặc nhiều `data_source` độc lập.

```sql
CREATE TABLE data_source (
    id VARCHAR(64) PRIMARY KEY,                 -- Khóa chính logic (Thường là projectId)
    organization_id VARCHAR(64) NOT NULL,       -- [CONTINUUM THÊM] Cô lập Tổ chức
    project_id VARCHAR(64) NOT NULL,            -- [CONTINUUM THÊM] Cô lập Dự án
    
    name VARCHAR(255) NOT NULL,                 -- Tên nguồn (VD: "Continuum Core Backend")
    description TEXT,
    language VARCHAR(16) DEFAULT 'vi',          -- 'vi' (Tiếng Việt), 'en' (Tiếng Anh)
    status VARCHAR(32) DEFAULT 'ACTIVE',        -- ACTIVE, INDEXING, ARCHIVED
    
    -- Thống kê trích xuất
    chunk_count INTEGER DEFAULT 0,
    event_count INTEGER DEFAULT 0,
    entity_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_data_source_tenant UNIQUE (organization_id, project_id, id)
);

CREATE INDEX ix_data_source_tenant ON data_source(organization_id, project_id);
```

---

### 4.2. `kb_document` (Tài Liệu / Thực Thể Nguồn Sau Parser)
Lưu vết các tài liệu, Jira issue, Work note, hoặc Audio bóc băng được đưa vào SAG.

```sql
CREATE TABLE kb_document (
    id VARCHAR(64) PRIMARY KEY,                 -- Khóa chính trong SAG
    data_source_id VARCHAR(64) NOT NULL,        -- FK sang data_source(id)
    organization_id VARCHAR(64) NOT NULL,       -- [CONTINUUM THÊM]
    project_id VARCHAR(64) NOT NULL,            -- [CONTINUUM THÊM]
    
    -- [CONTINUUM THÊM] Ánh xạ ngược về MongoDB và phân loại nguồn
    source_type VARCHAR(32) NOT NULL,           -- 'DOCUMENT_VERSION' | 'WORK_NOTE' | 'JIRA_ISSUE' | 'AUDIO_HANDOVER'
    continuum_ref_id VARCHAR(64) NOT NULL,      -- ID bản ghi trong MongoDB (VD: document_versions._id)
    
    filename VARCHAR(512) NOT NULL,             -- Tên hiển thị (Tên file, Issue Key, hoặc Tiêu đề Note)
    content_type VARCHAR(128),                  -- MIME type
    size_bytes BIGINT DEFAULT 0,
    storage_path VARCHAR(1024),                 -- Đường dẫn tệp Cloudflare R2
    
    -- [CONTINUUM THÊM] Bảo mật phân quyền Pre-retrieval ACL
    confidentiality_level VARCHAR(32) DEFAULT 'INTERNAL', -- 'INTERNAL' | 'CONFIDENTIAL' | 'RESTRICTED'
    allowed_roles JSON DEFAULT '["ADMIN", "TEAM_LEADER", "MEMBER"]', -- Danh sách roles được phép đọc
    
    status VARCHAR(32) DEFAULT 'PENDING',       -- PENDING, EXTRACTING, EXTRACTED, FAILED
    token_usage BIGINT DEFAULT 0,               -- Số token tiêu thụ để LLM extract tài liệu này
    error TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_kb_doc_source FOREIGN KEY (data_source_id) 
        REFERENCES data_source(id) ON DELETE CASCADE
);

CREATE INDEX ix_kb_document_tenant ON kb_document(organization_id, project_id);
CREATE INDEX ix_kb_document_continuum_ref ON kb_document(source_type, continuum_ref_id);
```

---

### 4.3. `source_chunk` (Phân Đoạn Văn Bản Kèm Heading & ACL)
Các đoạn văn bản phân rã ngữ nghĩa, chứa thông tin trích dẫn phục vụ hiển thị Citation.

```sql
CREATE TABLE source_chunk (
    id VARCHAR(64) PRIMARY KEY,                 -- Chunk ID (Lưu trong sag_mappings của MongoDB)
    data_source_id VARCHAR(64) NOT NULL,
    source_id VARCHAR(64) NOT NULL,             -- FK sang kb_document(id)
    organization_id VARCHAR(64) NOT NULL,       -- [CONTINUUM THÊM]
    project_id VARCHAR(64) NOT NULL,            -- [CONTINUUM THÊM]
    
    heading VARCHAR(512) DEFAULT '',            -- Tiêu đề mục cha (VD: "3.2 Cơ chế xác thực Token Rotation")
    content TEXT NOT NULL,                      -- Nội dung văn bản của đoạn trích
    token_count INTEGER DEFAULT 0,
    rank INTEGER DEFAULT 0,                     -- Thứ tự đoạn trong văn bản gốc
    
    -- [CONTINUUM THÊM] ACL kế thừa từ tài liệu cha để lọc vector siêu tốc
    allowed_roles JSON DEFAULT '["ADMIN", "TEAM_LEADER", "MEMBER"]',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_chunk_document FOREIGN KEY (source_id) 
        REFERENCES kb_document(id) ON DELETE CASCADE
);

CREATE INDEX ix_source_chunk_tenant ON source_chunk(organization_id, project_id);
CREATE INDEX ix_source_chunk_source_rank ON source_chunk(source_id, rank);
```

---

### 4.4. `entity_type` (Danh Mục Thực Thể Chuẩn Kỹ Nghệ Phần Mềm)
Danh mục các nhóm khái niệm chuyên biệt cho tri thức dự án phần mềm:

```sql
CREATE TABLE entity_type (
    code VARCHAR(64) PRIMARY KEY,               -- Mã loại thực thể
    name VARCHAR(128) NOT NULL,                 -- Tên hiển thị
    description TEXT,                           -- Chỉ dẫn cho Prompt LLM nhận diện
    color_hex VARCHAR(16) DEFAULT '#3B82F6'
);

-- Seed bộ từ điển thực thể chuẩn cho Continuum AI:
INSERT INTO entity_type (code, name, description, color_hex) VALUES
('TECH_STACK', 'Công nghệ & Thư viện', 'Framework, Ngôn ngữ lập trình, Thư viện, Database (VD: Next.js, Mongoose, Redis)', '#10B981'),
('MODULE_SERVICE', 'Vi dịch vụ & Module', 'Tên Service, Component, Subsystem (VD: svc_iam, svc_lifecycle, AuthGuard)', '#3B82F6'),
('ARCHITECTURE_DECISION', 'Quyết định kiến trúc', 'Quyết định thiết kế, Mẫu thiết kế, ADR (VD: Database-per-service, JWT in Cookie)', '#8B5CF6'),
('BUSINESS_RULE', 'Quy tắc nghiệp vụ', 'Chính sách, Ràng buộc nghiệp vụ (VD: Phải có authorConfirmedAt, Bắt buộc 3 roles)', '#F59E0B'),
('DATABASE_SCHEMA', 'Bảng dữ liệu & Thực thể', 'Collection, Table, Field dữ liệu (VD: documents, knowledge_versions)', '#EC4899'),
('ROLE_RESPONSIBILITY', 'Trách nhiệm & Vai trò', 'Vai trò dự án, Module phụ trách (VD: Lead Architect, Module Payment Owner)', '#6366F1');
```

---

### 4.5. `entity` (Kho Thực Thể Đã Trích Xuất Của Dự Án)
Lưu trữ các thực thể cụ thể xuất hiện trong tài liệu hoặc ghi chú.

```sql
CREATE TABLE entity (
    id VARCHAR(64) PRIMARY KEY,                 -- UUID thực thể
    data_source_id VARCHAR(64) NOT NULL,
    organization_id VARCHAR(64) NOT NULL,       -- [CONTINUUM THÊM]
    project_id VARCHAR(64) NOT NULL,            -- [CONTINUUM THÊM]
    
    name VARCHAR(255) NOT NULL,                 -- Tên thực thể chuẩn hóa (VD: "Cloudflare R2", "BullMQ")
    type_code VARCHAR(64) NOT NULL,             -- FK sang entity_type(code)
    description TEXT DEFAULT '',                -- Tóm tắt tổng hợp về thực thể trong dự án
    heat INTEGER DEFAULT 1,                     -- Tần suất xuất hiện (Độ quan trọng)
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_entity_type FOREIGN KEY (type_code) REFERENCES entity_type(code),
    CONSTRAINT uq_entity_tenant_name UNIQUE (organization_id, project_id, name)
);

CREATE INDEX ix_entity_tenant_type ON entity(organization_id, project_id, type_code);
CREATE INDEX ix_entity_heat ON entity(organization_id, project_id, heat DESC);
```

---

### 4.6. `source_event` (Luận Điểm & Sự Kiện Kỹ Thuật Bóc Tách)
Mỗi sự kiện đại diện cho một kiến thức, hành động, giải pháp hoặc lỗi đã giải quyết.

```sql
CREATE TABLE source_event (
    id VARCHAR(64) PRIMARY KEY,                 -- UUID sự kiện
    data_source_id VARCHAR(64) NOT NULL,
    source_id VARCHAR(64) NOT NULL,             -- FK sang kb_document(id)
    chunk_id VARCHAR(64),                       -- FK sang source_chunk(id)
    organization_id VARCHAR(64) NOT NULL,       -- [CONTINUUM THÊM]
    project_id VARCHAR(64) NOT NULL,            -- [CONTINUUM THÊM]
    
    title VARCHAR(512) NOT NULL,                -- Tiêu đề sự kiện (VD: "Chuyển lưu trữ file sang Cloudflare R2")
    summary TEXT DEFAULT '',                    -- Tóm lược luận điểm
    content TEXT NOT NULL,                      -- Chi tiết nội dung luận cứ
    category VARCHAR(64) DEFAULT 'TECHNICAL',   -- 'TECHNICAL' | 'DECISION' | 'BUG_FIX' | 'PROCESS'
    parent_id VARCHAR(64),                      -- Sự kiện cha (nếu có quan hệ cấp bậc)
    rank INTEGER DEFAULT 0,
    
    start_time TIMESTAMP WITH TIME ZONE,        -- Thời điểm phát sinh (nếu có)
    score FLOAT DEFAULT 1.0,                    -- Độ tin cậy trích xuất LLM
    
    -- [CONTINUUM THÊM] Kế thừa ACL
    allowed_roles JSON DEFAULT '["ADMIN", "TEAM_LEADER", "MEMBER"]',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_event_document FOREIGN KEY (source_id) REFERENCES kb_document(id) ON DELETE CASCADE,
    CONSTRAINT fk_event_chunk FOREIGN KEY (chunk_id) REFERENCES source_chunk(id) ON DELETE SET NULL
);

CREATE INDEX ix_source_event_tenant ON source_event(organization_id, project_id);
CREATE INDEX ix_source_event_chunk ON source_event(chunk_id);
```

---

### 4.7. `event_entity` (Xương Sống Dynamic Hypergraph: N-N Event ⟷ Entity)
Bảng liên kết động giữa Sự kiện và Thực thể. **Đây chính là chìa khóa để SAG thực hiện các câu truy vấn Dynamic SQL Hyperedges.**

```sql
CREATE TABLE event_entity (
    event_id VARCHAR(64) NOT NULL,              -- FK sang source_event(id)
    entity_id VARCHAR(64) NOT NULL,             -- FK sang entity(id)
    organization_id VARCHAR(64) NOT NULL,       -- [CONTINUUM THÊM]
    project_id VARCHAR(64) NOT NULL,            -- [CONTINUUM THÊM]
    
    weight FLOAT DEFAULT 1.0,                   -- Mức độ gắn kết (0.1 -> 1.0)
    description VARCHAR(512) DEFAULT '',        -- Mô tả quan hệ (VD: "sử dụng để", "khắc phục lỗi của")
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (event_id, entity_id),
    CONSTRAINT fk_ee_event FOREIGN KEY (event_id) REFERENCES source_event(id) ON DELETE CASCADE,
    CONSTRAINT fk_ee_entity FOREIGN KEY (entity_id) REFERENCES entity(id) ON DELETE CASCADE
);

CREATE INDEX ix_event_entity_query ON event_entity(organization_id, project_id, entity_id, weight DESC);
```

---

### 4.8. Cấu Trúc Bảng Vector Trên PostgreSQL 16 (`pgvector` Extension)
Dự án chuẩn hóa lưu trữ trực tiếp các Vector Embeddings vào cùng cơ sở dữ liệu PostgreSQL 16 thông qua extension **`pgvector`** (thay vì tách riêng LanceDB file). Điều này đảm bảo tính nhất quán giao dịch ACID 100% khi thêm/sửa/xóa tài liệu:

```sql
-- Kích hoạt extension pgvector (đã có sẵn trong image pgvector/pgvector:pg16)
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Bảng Vector Phân Đoạn Văn Bản (Dense Retrieval)
CREATE TABLE chunk_vectors (
    id VARCHAR(64) PRIMARY KEY,                 -- Khóa chính trùng với source_chunk.id
    chunk_id VARCHAR(64) NOT NULL,              -- FK sang source_chunk(id)
    source_id VARCHAR(64) NOT NULL,             -- FK sang kb_document(id)
    organization_id VARCHAR(64) NOT NULL,       -- [CONTINUUM] Tenant Filter
    project_id VARCHAR(64) NOT NULL,            -- [CONTINUUM] Project Filter
    
    -- Cột Vector Embedding: 1024 chiều (Text-Embedding-004) hoặc 1536 (OpenAI text-embedding-3-small)
    embedding vector(1024) NOT NULL,
    
    -- Pre-retrieval ACL kế thừa từ Document
    allowed_roles JSONB DEFAULT '["ADMIN", "TEAM_LEADER", "MEMBER"]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_chunk_vector_chunk FOREIGN KEY (chunk_id) 
        REFERENCES source_chunk(id) ON DELETE CASCADE,
    CONSTRAINT fk_chunk_vector_doc FOREIGN KEY (source_id) 
        REFERENCES kb_document(id) ON DELETE CASCADE
);

-- Chỉ mục HNSW cho vector cosine search siêu tốc (< 10ms trên hàng triệu vector)
CREATE INDEX ix_chunk_vectors_hnsw 
ON chunk_vectors USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX ix_chunk_vectors_tenant_roles 
ON chunk_vectors(organization_id, project_id);


-- 2. Bảng Vector Tiêu Đề Cây Phân Cấp (Hierarchical Heading Vectors)
CREATE TABLE chunk_heading_vectors (
    id VARCHAR(64) PRIMARY KEY,
    chunk_id VARCHAR(64) NOT NULL,
    organization_id VARCHAR(64) NOT NULL,
    project_id VARCHAR(64) NOT NULL,
    heading_text VARCHAR(512) NOT NULL,
    
    embedding vector(1024) NOT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_heading_vector_chunk FOREIGN KEY (chunk_id) 
        REFERENCES source_chunk(id) ON DELETE CASCADE
);

CREATE INDEX ix_heading_vectors_hnsw 
ON chunk_heading_vectors USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

---

### 4.9. Phương Án Thay Thế Chuyên Dụng: Qdrant Vector Database
Nếu dự án quyết định tách riêng kho vector khỏi PostgreSQL để xử lý quy mô hàng chục triệu vector với tải tìm kiếm cao, **Qdrant** (viết bằng Rust, chuyên biệt cho vector search và payload filtering) được sử dụng làm Vector Backend chuyên trách:

#### A. Cấu Hình Tạo Collection Trong Qdrant (`PUT /collections/continuum_chunks`)
```json
{
  "vectors": {
    "size": 1024,
    "distance": "Cosine",
    "on_disk": true
  },
  "hnsw_config": {
    "m": 16,
    "ef_construct": 100,
    "on_disk": false
  },
  "optimizers_config": {
    "indexing_threshold": 10000
  }
}
```

#### B. Cấu Trúc Payload Lưu Kèm Vector & Chỉ Mục Payload (Payload Indexes)
Để hỗ trợ Pre-retrieval ACL và cô lập dữ liệu Multi-Tenant cực nhanh, Qdrant yêu cầu tạo **Payload Keyword Index**:

```json
// Cấu trúc một Point trong Qdrant
{
  "id": "chunk_uuid_string",
  "vector": [0.0123, -0.0456, ...],
  "payload": {
    "chunk_id": "chunk_uuid_string",           // Ánh xạ sang source_chunk.id trong PostgreSQL
    "source_id": "doc_uuid_string",            // Ánh xạ sang kb_document.id
    "organization_id": "org_uuid_string",      // Tenant Filter
    "project_id": "proj_uuid_string",          // Project Filter
    "allowed_roles": ["ADMIN", "TEAM_LEADER", "MEMBER"], // Pre-retrieval ACL Filter
    "heading": "3.2 Cơ chế xác thực Token Rotation",
    "text_content": "Chi tiết đoạn trích..."
  }
}
```

* **Lệnh tạo Payload Index trong Qdrant:**
```bash
# 1. Index cho Organization
curl -X PUT "http://localhost:6333/collections/continuum_chunks/index" \
  -H "Content-Type: application/json" \
  -d '{"field_name": "organization_id", "field_schema": "keyword"}'

# 2. Index cho Project
curl -X PUT "http://localhost:6333/collections/continuum_chunks/index" \
  -H "Content-Type: application/json" \
  -d '{"field_name": "project_id", "field_schema": "keyword"}'

# 3. Index cho Allowed Roles (Pre-retrieval ACL)
curl -X PUT "http://localhost:6333/collections/continuum_chunks/index" \
  -H "Content-Type: application/json" \
  -d '{"field_name": "allowed_roles", "field_schema": "keyword"}'
```

#### C. Cú Pháp Tìm Kiếm Vector Kèm Lọc Quyền (Qdrant Search API)
```json
// POST /collections/continuum_chunks/points/search
{
  "vector": [0.0123, -0.0456, ...],
  "filter": {
    "must": [
      { "key": "organization_id", "match": { "value": "org_continuum_corp" } },
      { "key": "project_id", "match": { "value": "proj_continuum_core" } },
      { "key": "allowed_roles", "match": { "any": ["MEMBER"] } }
    ]
  },
  "limit": 10,
  "with_payload": true
}
```

---

### 4.10. BỘ SCHEMAS VŨ TRỤ TRI THỨC 3D (3D KNOWLEDGE UNIVERSE & EXPLORATION)
> ⭐ **ĐIỂM NHẤN TRỰC QUAN ĐẶC BIỆT CỦA DỰ ÁN (WOW FACTOR)**:  
> Thay vì chatbot hỏi đáp thông thường hoặc danh sách phẳng khô khan, Continuum AI tái sử dụng và nâng cấp **Tầng Trực Quan Hóa Không Gian 3D (3D Knowledge Galaxy)** của SAG.  
> Toàn bộ tri thức dự án phần mềm được chiếu lên không gian 3D tương tác trên giao diện Next.js (Three.js / WebGL Canvas). Kỹ sư kế nhiệm khi Onboarding có thể "bay" qua các tinh cầu Module, xem độ dày tri thức (Cluster Density), và Camera 3D sẽ tự động xoay chuyển (Fly-to Animation) tới đúng vị trí bằng chứng khi hỏi đáp.

#### A. `universe_overviews` (Bản Chụp Không Gian Vũ Trụ Tri Thức Của Dự Án)
```sql
CREATE TABLE universe_overviews (
    id VARCHAR(64) PRIMARY KEY,                 -- UUID bản chụp không gian 3D
    organization_id VARCHAR(64) NOT NULL,       -- [CONTINUUM] Cô lập Tổ chức
    project_id VARCHAR(64) NOT NULL,            -- [CONTINUUM] Cô lập Dự án
    
    status VARCHAR(32) DEFAULT 'BUILDING',      -- 'BUILDING' | 'READY' | 'FAILED'
    is_active BOOLEAN DEFAULT TRUE,             -- Đang là không gian 3D hoạt động chính
    
    -- Thống kê tổng thể không gian
    source_count INTEGER DEFAULT 0,
    partition_count INTEGER DEFAULT 0,          -- Số lượng cụm tinh vân / module
    event_count INTEGER DEFAULT 0,
    entity_count INTEGER DEFAULT 0,
    node_count INTEGER DEFAULT 0,
    relation_count INTEGER DEFAULT 0,
    
    -- Giới hạn tọa độ bao bọc không gian 3D (Bounding Box)
    bounds_json JSONB DEFAULT '{"min_x": -1000, "max_x": 1000, "min_y": -1000, "max_y": 1000, "min_z": -500, "max_z": 500}'::jsonb,
    schema_version INTEGER DEFAULT 2,
    as_of TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    error TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_universe_overview_active UNIQUE (organization_id, project_id, is_active)
);

CREATE INDEX ix_universe_overview_tenant ON universe_overviews(organization_id, project_id, is_active);
```

#### B. `universe_partitions` (Các Cụm Thiên Hà & Tinh Cầu Tri Thức Module)
Đại diện cho các vùng tri thức cụ thể trong không gian 3D (VD: Cụm Auth, Cụm Payment Gateway, Cụm Data Pipeline, Cụm Handover).

```sql
CREATE TABLE universe_partitions (
    id VARCHAR(64) PRIMARY KEY,                 -- UUID cụm tinh cầu
    overview_id VARCHAR(64) NOT NULL,           -- FK sang universe_overviews(id)
    organization_id VARCHAR(64) NOT NULL,
    project_id VARCHAR(64) NOT NULL,
    source_id VARCHAR(64),                      -- FK logic sang data_source(id)
    parent_id VARCHAR(64),                      -- FK sang universe_partitions(id) (Cụm cha phân cấp)
    
    kind VARCHAR(32) NOT NULL,                  -- 'MODULE' | 'SERVICE' | 'TECH_DOMAIN' | 'TOPIC_CLUSTER'
    key VARCHAR(160) NOT NULL,                  -- Business key (VD: "module.authentication")
    label VARCHAR(255) NOT NULL,                -- Tên hiển thị trên 3D Canvas (VD: "Module Xác Thực & Token Rotation")
    
    -- TỌA ĐỘ VÀ KÍCH THƯỚC TRONG KHÔNG GIAN 3D
    x FLOAT NOT NULL,                           -- Tọa độ trục X
    y FLOAT NOT NULL,                           -- Tọa độ trục Y
    z FLOAT NOT NULL DEFAULT 0.0,               -- Tọa độ trục Z
    radius FLOAT DEFAULT 120.0,                 -- Bán kính tinh cầu (Tỷ lệ thuận với số lượng tri thức)
    
    -- Mật độ và cấu trúc liên kết
    node_count INTEGER DEFAULT 0,
    event_count INTEGER DEFAULT 0,
    entity_count INTEGER DEFAULT 0,
    relation_count INTEGER DEFAULT 0,
    density FLOAT DEFAULT 0.0,                  -- Mật độ liên kết nội bộ
    importance FLOAT DEFAULT 1.0,               -- Trọng số nổi bật (Độ sáng tinh cầu)
    color_hex VARCHAR(16) DEFAULT '#6366F1',    -- Màu sắc tinh cầu tương ứng loại module
    
    time_range_json JSONB DEFAULT '{}'::jsonb,  -- Khoảng thời gian phát triển của module
    time_buckets_json JSONB DEFAULT '[]'::jsonb,-- Lịch sử phân bố sự kiện theo thời gian
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_univ_part_overview FOREIGN KEY (overview_id) 
        REFERENCES universe_overviews(id) ON DELETE CASCADE,
    CONSTRAINT fk_univ_part_parent FOREIGN KEY (parent_id) 
        REFERENCES universe_partitions(id) ON DELETE CASCADE,
    CONSTRAINT uq_univ_partition_key UNIQUE (overview_id, key)
);

CREATE INDEX ix_univ_partition_coords ON universe_partitions(overview_id, x, y, z);
CREATE INDEX ix_univ_partition_tenant ON universe_partitions(organization_id, project_id);
```

#### C. `universe_dirty_sources` (Hàng Đợi Cờ Hiệu Tái Chiếu Tọa Độ 3D Bất Đồng Bộ)
Khi có tài liệu mới hoặc cập nhật, hệ thống ghi cờ dirty để Worker tính toán lại phép chiếu 3D (UMAP/t-SNE/Force-directed) trong nền mà không làm chậm ứng dụng chính.

```sql
CREATE TABLE universe_dirty_sources (
    id VARCHAR(64) PRIMARY KEY,
    organization_id VARCHAR(64) NOT NULL,
    project_id VARCHAR(64) NOT NULL,
    source_id VARCHAR(64) NOT NULL,             -- FK sang data_source(id)
    
    reason VARCHAR(64) DEFAULT 'DOC_MODIFIED',  -- 'DOC_MODIFIED' | 'NEW_DOC' | 'DOC_DELETED'
    revision INTEGER DEFAULT 1,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_univ_dirty_source UNIQUE (organization_id, project_id, source_id)
);
```

#### D. `exploration_sessions` & `exploration_steps` (Lịch Sử Thám Hiểm Không Gian 3D)
Lưu lại hành trình khám phá dự án của kỹ sư kế nhiệm, cho phép tua lại góc nhìn Camera 3D và các bằng chứng đã đi qua.

```sql
-- 1. Phiên Thám Hiểm Vũ Trụ Tri Thức
CREATE TABLE exploration_sessions (
    id VARCHAR(64) PRIMARY KEY,                 -- UUID phiên thám hiểm
    organization_id VARCHAR(64) NOT NULL,
    project_id VARCHAR(64) NOT NULL,
    user_id VARCHAR(64) NOT NULL,               -- Kỹ sư thực hiện thám hiểm
    
    title VARCHAR(300) NOT NULL DEFAULT 'Hành trình tiếp quản dự án',
    source_ids_json JSONB DEFAULT '[]'::jsonb,  -- Các nguồn tài liệu đã chọn lọc
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_explor_session_user ON exploration_sessions(organization_id, project_id, user_id, updated_at DESC);


-- 2. Từng Bước Di Chuyển & Tọa Độ Camera 3D
CREATE TABLE exploration_steps (
    id VARCHAR(64) PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,            -- FK sang exploration_sessions(id)
    
    query TEXT NOT NULL,                        -- Câu hỏi thám hiểm (VD: "Kiến trúc xác thực hoạt động thế nào?")
    summary TEXT DEFAULT '',                    -- Tóm tắt kết quả tìm thấy
    
    -- Danh sách tham chiếu thực thể và bằng chứng đã duyệt qua
    source_ids_json JSONB DEFAULT '[]'::jsonb,
    event_refs_json JSONB DEFAULT '[]'::jsonb,
    entity_refs_json JSONB DEFAULT '[]'::jsonb,
    evidence_refs_json JSONB DEFAULT '[]'::jsonb,
    
    -- TỌA ĐỘ VỊ TRÍ VÀ GÓC QUAY CAMERA 3D (Tua lại hành trình)
    camera_json JSONB NOT NULL DEFAULT '{"position": {"x": 0, "y": 200, "z": 800}, "target": {"x": 0, "y": 0, "z": 0}, "zoom": 1.0, "fov": 45}'::jsonb,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_explor_step_session FOREIGN KEY (session_id) 
        REFERENCES exploration_sessions(id) ON DELETE CASCADE
);

CREATE INDEX ix_explor_step_created ON exploration_steps(session_id, created_at ASC);
```

---

## 5. PHẦN IV: Quy Trình Truy Vấn Dynamic SQL Hyperedges Kèm Pre-retrieval ACL

Tùy thuộc vào việc lựa chọn **PostgreSQL + pgvector (Hợp nhất)** hay **PostgreSQL + Qdrant (Tách rời)**, quy trình truy vấn siêu cạnh động được thực hiện như sau:

### 5.1. Phương Án 1: Hợp Nhất Trên PostgreSQL 16 + pgvector (Single-Query Dynamic Retrieval)
Hệ thống thực hiện tìm kiếm vector (`<=>`), kết nối Dynamic Hyperedges (`JOIN`), và lọc phân quyền Pre-retrieval ACL (`allowed_roles`) gói gọn trong **1 câu SQL duy nhất**:

```sql
WITH top_similar_chunks AS (
    -- Giai đoạn 1: Vector Search tìm top đoạn liên quan nhất có lọc quyền người dùng
    SELECT 
        cv.chunk_id,
        cv.source_id,
        (cv.embedding <=> :queryEmbedding) AS cosine_distance
    FROM chunk_vectors cv
    WHERE cv.organization_id = :currentOrgId
      AND cv.project_id = :currentProjectId
      AND cv.allowed_roles ? :currentUserRole
    ORDER BY cv.embedding <=> :queryEmbedding ASC
    LIMIT 10
)
-- Giai đoạn 2: Nối động các sự kiện và thực thể liên quan qua Hyperedges
SELECT 
    tsc.chunk_id,
    tsc.cosine_distance,
    sc.heading AS chunk_heading,
    sc.content AS chunk_content,
    se.id AS event_id,
    se.title AS event_title,
    se.summary AS event_summary,
    e.name AS entity_name,
    et.name AS entity_type_name,
    ee.weight AS link_weight,
    kd.filename AS source_filename,
    kd.continuum_ref_id AS mongo_ref_id
FROM top_similar_chunks tsc
JOIN source_chunk sc ON tsc.chunk_id = sc.id
JOIN kb_document kd ON sc.source_id = kd.id
LEFT JOIN source_event se ON sc.id = se.chunk_id
LEFT JOIN event_entity ee ON se.id = ee.event_id
LEFT JOIN entity e ON ee.entity_id = e.id
LEFT JOIN entity_type et ON e.type_code = et.code
ORDER BY tsc.cosine_distance ASC, ee.weight DESC NULLS LAST
LIMIT 20;
```

---

### 5.2. Phương Án 2: Hai Chặng Khi Dùng PostgreSQL + Qdrant (Two-Stage Retrieval Flow)

1. **Chặng 1 (Qdrant Vector Search):** Gọi REST/gRPC API sang Qdrant với Payload Filter (`organization_id`, `project_id`, `allowed_roles`) để lấy danh sách top 10 `chunk_id` có điểm tương đồng cao nhất.
2. **Chặng 2 (PostgreSQL Hyperedges Expansion):** Dùng danh sách `chunk_ids` từ Chặng 1 để truy vấn vào PostgreSQL, mở rộng đồ thị siêu cạnh các thực thể liên quan:

```sql
SELECT 
    sc.id AS chunk_id,
    sc.heading AS chunk_heading,
    sc.content AS chunk_content,
    se.id AS event_id,
    se.title AS event_title,
    se.summary AS event_summary,
    e.name AS entity_name,
    et.name AS entity_type_name,
    ee.weight AS link_weight,
    kd.filename AS source_filename,
    kd.continuum_ref_id AS mongo_ref_id
FROM source_chunk sc
JOIN kb_document kd ON sc.source_id = kd.id
LEFT JOIN source_event se ON sc.id = se.chunk_id
LEFT JOIN event_entity ee ON se.id = ee.event_id
LEFT JOIN entity e ON ee.entity_id = e.id
LEFT JOIN entity_type et ON e.type_code = et.code
WHERE sc.id IN (:topChunkIdsFromQdrant)
  AND sc.organization_id = :currentOrgId
  AND sc.project_id = :currentProjectId
ORDER BY ee.weight DESC NULLS LAST;
```

---

## 6. PHẦN V: Bảng So Sánh Quyết Định Giữa Hai Phương Án Lưu Trữ Vector

| Tiêu chí kỹ thuật | Phương án A: PostgreSQL 16 + pgvector | Phương án B: PostgreSQL 16 + Qdrant |
| :--- | :--- | :--- |
| **Mô hình kiến trúc** | **Hợp nhất (Unified Single DB):** Cả bảng quan hệ lẫn vector đều nằm trong PostgreSQL. | **Tách rời (Decoupled Vector DB):** PostgreSQL giữ quan hệ, Qdrant giữ Vector & Payload. |
| **Tính toàn vẹn giao dịch (ACID)** | **Tuyệt đối 100%:** Xóa document thì vector tự động bị xóa theo `CASCADE` trong cùng 1 transaction. | **Nhất quán sau (Eventual Consistency):** Phải gọi 2 lệnh xóa (PostgreSQL + Qdrant API), cần worker bù trừ lỗi. |
| **Quy mô Vector tối ưu** | Tối ưu cho quy mô từ **100.000 đến 5.000.000 vectors** (Phù hợp hoàn hảo cho phần lớn doanh nghiệp vừa và lớn). | Tối ưu vượt trội khi quy mô đạt **từ 10 triệu đến hàng trăm triệu vectors**. |
| **Độ trễ truy vấn** | Siêu thấp nhờ cơ chế **Single-Query CTE** (không tốn network hop trung gian). | Cần **2 network hops** (App ➔ Qdrant ➔ App ➔ PostgreSQL). |
| **Khả năng Scale độc lập** | Phụ thuộc vào tài nguyên của cụm PostgreSQL. | Scale Pod Qdrant độc lập (CPU/RAM riêng cho vector search mà không ảnh hưởng DB giao dịch). |
| **Vận hành & Triển khai** | **Cực kỳ đơn giản:** Chỉ duy nhất 1 container `pgvector/pgvector:pg16`, backup bằng `pg_dump`. | Cần vận hành thêm 1 cụm Qdrant riêng biệt kèm cơ chế snapshot riêng. |
| **Khuyến nghị áp dụng** | **LỰA CHỌN MẶC ĐỊNH CHO continuum_sag_storage**. | **LỰA CHỌN MỞ RỘNG** khi hệ thống đạt ngưỡng scale tải hàng chục triệu chunks. |
