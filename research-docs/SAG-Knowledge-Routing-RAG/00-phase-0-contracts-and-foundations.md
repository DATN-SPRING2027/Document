# [RESEARCH & PLAN] SAG Knowledge Routing RAG - Phase 0: Contracts & Foundations Baseline

**Ticket**: `DATN-23`  
**Assignee**: Phan Thành Tài (DE190491)  
**Status**: Research & Architecture Plan  
**Target System**: `sag-laya-integration` (SAG Engine) & Continuum AI (`DATN-BE` / `DATN-FE`)  
**Canonical Spec**: [SAG_Knowledge_Routing_RAG_Workflow_v1.1.md](../../sag-laya-integration/SAG/docs/SAG_Knowledge_Routing_RAG_Workflow_v1.1.md)  
**Execution Plan Ref**: [plan.md](../../sag-laya-integration/SAG/tasks/plan.md) | [todo.md](../../sag-laya-integration/SAG/tasks/todo.md)  
**Pull Request**: [#14](https://github.com/DATN-SPRING2027/Document/pull/14)  

---

## 1. Evidence Classification Standard (Truth Grading)

Báo cáo nghiên cứu và kế hoạch này tuân thủ nghiêm ngặt chuẩn phân loại bằng chứng dự án DATN:
- `[FACT / VERIFIED]`: Đã đối chiếu và kiểm chứng trực tiếp từ mã nguồn thực tế trong repository (`sag-laya-integration/SAG/apps/api`, `DATN-BE`, `DATN-FE`).
- `[IMPLEMENTED]`: Tính năng đã được hiện thực bằng code có thể thực thi, test suite đã pass.
- `[DESIGN / PROPOSED]`: Được quy định trong `SAG_Knowledge_Routing_RAG_Workflow_v1.1.md`, `11_SAG_STORAGE_SCHEMA.md` hoặc tài liệu kiến trúc, nhưng chưa hoàn thiện trong code.
- `[PARTIAL]`: Đã có một phần hạ tầng hoặc model/schema nhưng chưa hoàn chỉnh luồng nghiệp vụ end-to-end.
- `[GAP]`: Yêu cầu bắt buộc trong đặc tả nhưng hoàn toàn chưa có trong mã nguồn hiện tại.
- `[INFERENCE]`: Suy luận logic có căn cứ từ các bằng chứng đã xác thực.
- `[DECISION REQUIRED]`: Điểm xung đột kiến trúc hoặc chính sách mở cần thống nhất giữa các thành viên.

---

## 2. Executive Summary

1. `[FACT]` **Chuyển giao Kiến trúc từ Classic RAG sang Knowledge Routing RAG**: Hệ thống chuyển đổi triệt để từ mô hình naive RAG ("chia chunk phẳng -> embedding -> similarity search") sang **Knowledge Routing RAG**. Mục tiêu cốt lõi: *"Build expensive once, query cheap many times"* — trả chi phí trích xuất, phân nhóm và cấu trúc cây ở giai đoạn Ingestion; khi người dùng truy vấn hằng ngày, hệ thống định tuyến qua cây tri thức và tìm kiếm cục bộ (branch-local hybrid search) nhằm tối ưu latency (p95), giảm chi phí LLM và ngăn ngừa hiện tượng ảo giác (hallucination).
2. `[FACT]` **Hiện trạng Hạ tầng Lưu trữ**: Repository `sag-laya-integration` đã hoàn tất chuyển đổi kho lưu trữ từ SQLite/LanceDB sang **PostgreSQL 16 + Qdrant** (PR #3, PR #5). PostgreSQL đóng vai trò **Source of Truth** cho toàn bộ metadata, version, provenance, graph edges và tree lineage. Qdrant đóng vai trò **Search Accelerator** (lưu vector và payload filter) và phải luôn dựng lại được từ PostgreSQL.
3. `[FACT]` **Hiện trạng Tích hợp Laya Router**: Service `laya_router.py` và luồng định tuyến truy vấn tại `/api/v1/search` đã được tích hợp thành công (PR #2, PR #7), cung cấp coarse intent (`CHAT`, `KNOWLEDGE`, `COMMAND`, `AMBIGUOUS`). Các truy vấn `CHAT` có độ tin cậy $\ge 0.65$ bỏ qua retrieval; các truy vấn tri thức, mã định danh chính xác hoặc khi Laya gặp sự cố đều fallback an toàn về retrieval.
4. `[GAP]` **Mô hình Dữ liệu Hiện tại Chưa Hỗ trợ Versioning & Lineage**: Model `Document` trong `apps/api/sag_api/db/models/document.py` hiện là bảng phẳng, không có `document_versions`, không có hash file, không lưu provenance (thời điểm xuất bản, thời điểm quan sát, thời điểm nạp), và không có liên kết kế thừa (`supersedes_id`).
5. `[GAP]` **Thiếu Khái niệm Tách Rời Giữa Search Readiness và Knowledge Readiness**: Trạng thái tài liệu hiện tại chỉ có `DocumentStatus.READY`. Điều này vi phạm nguyên tắc kiến trúc: khi quá trình trích xuất đồ thị/cây tri thức bất đồng bộ bị chậm hoặc lỗi, luồng tìm kiếm hybrid thông thường (`SEARCH_READY`) bị chặn oan.
6. `[GAP]` **Thiếu Hạ tầng Canonical Blocks, Search Units và Knowledge Units**: Hiện tại SAG chunk thô tài liệu (`chunk_count`), không phân tách giữa đơn vị phục vụ tìm kiếm lexical/dense (`SearchUnit`) và đơn vị ngữ nghĩa phục vụ phân cụm/cây tri thức (`KnowledgeUnit`).
7. `[FACT]` **Ranh giới Sở hữu Dữ liệu (Data Ownership)**: Theo `data-ownership-and-storage.md`, `DATN-BE` (MongoDB) sở hữu toàn bộ định danh và phân quyền người dùng (`user`, `project`, `team`, `membership`). `sag-laya-integration` (PostgreSQL + Qdrant) chỉ nhận assertion scope đã xác thực và enforce access control qua metadata/payload filter.

---

## 3. Khảo Sát Hiện Trạng & Phân Tích Gap (Pillar 1)

### 3.1. Bảng Đối Chiếu Hiện Trạng vs Đặc Tả Mục Tiêu

| Thành phần | Hiện trạng trong Code (`sag-laya-integration`) | Đặc tả mục tiêu (`Workflow v1.1` & `plan.md`) | Phân loại | Gap cụ thể & Hướng xử lý |
| :--- | :--- | :--- | :--- | :--- |
| **Upload Flow** | `POST /sources/{id}/documents` nhận file, ghi vào volume cục bộ, tạo 1 record `Document` với status `pending`. | Validate MIME signature/size/ext, tính SHA-256 stream, tạo `SourceSnapshot` và `DocumentVersion` liên kết trong transaction. | `[PARTIAL]` | Chưa có bảng `SourceSnapshot`; chưa tính hash trước khi ghi đĩa; chưa có chính sách xử lý 4 trường hợp trùng lặp (cùng/khác hash vs cùng/khác identity). |
| **Worker / Job** | `JobManager` quản lý bảng `jobs` với status (`queued`, `running`, `succeeded`, `failed`), progress float, attempts count. | `IngestionRun` idempotent, theo dõi tiến trình qua từng stage chi tiết (`stage_runs`), hỗ trợ retry độc lập từng giai đoạn. | `[PARTIAL]` | Bảng `jobs` hiện chỉ có `payload_json` và 1 trường `error` Text; không lưu lịch sử chạy từng stage; không có `idempotency_key` ở tầng schema. |
| **Document State** | Enum `DocumentStatus`: `pending`, `processing`, `ready`, `failed`. | Tách biệt: `RECEIVED` $\rightarrow$ `PARSED` $\rightarrow$ `DEDUPED` $\rightarrow$ `SEARCH_READY` (xong hybrid index); nhánh async: $\rightarrow$ `KNOWLEDGE_READY`. | `[GAP]` | Chỉ có 1 trạng thái `ready` duy nhất. Không thể báo cho UI biết tài liệu đã tìm kiếm được nhưng đang tiếp tục làm giàu tri thức. |
| **Search & Indexing** | Qdrant vector store (`qdrant_store.py`) lưu embeddings của chunk, fallback lexical search về vector search. | Hybrid search kết hợp Dense (Cosine) + Sparse representation (BM25/SPLADE) với Rank Fusion (RRF) và Index Manifest. | `[PARTIAL]` | Qdrant store đã có adapter HTTP chuẩn, nhưng payload chưa gắn `security_partition_id`, chưa có sparse vector, chưa có `IndexManifest` kiểm tra tính toàn vẹn. |
| **Query Routing** | `LayaRouter` phân loại coarse intent (`CHAT`, `KNOWLEDGE`, `COMMAND`, `AMBIGUOUS`) tích hợp trong `/search`. | Laya coarse intent + Deterministic Feature Extractor + Query Strategy Planner (`EXACT`, `LOCAL_FACTUAL`, `MULTI_HOP`...). | `[PARTIAL]` | Đã có Laya coarse intent và trích xuất regex cơ bản (`query_analysis.py`); chưa có bộ Planner hoàn chỉnh để sinh ra chiến lược kèm reason codes. |
| **Multi-tenancy / ACL** | Model `Source` gắn với `User` cục bộ qua `user_id`. Không có cấu trúc Tenant / Project / Team. | `tenant_id`, `project_id`, `security_partition_id` được enforce nghiêm ngặt trên mọi câu truy vấn SQL và Qdrant payload filter. | `[GAP]` | Schema hiện tại không có cột `project_id` hay `security_partition_id`. Phải tái cấu trúc để tích hợp với identity assertion từ `DATN-BE`. |
| **Knowledge Graph & Tree** | Chỉ có bảng liên kết `event_entity` cổ điển của SAG, không có phân cấp cây tri thức. | Constrained Hierarchical Leiden clustering, Knowledge Routing Tree, `node_routing_profiles`, dual-slot pointer (A/B). | `[GAP]` | Hoàn toàn chưa có bảng biểu cho cây tri thức (`knowledge_nodes`, `tree_manifests`, `node_routing_profiles`). |

---

## 4. Chốt Thực Thể & Định Danh Dữ Liệu (Pillar 2)

### 4.1. Cấu trúc Thực thể Tách Lớp (Multi-Tier Relational Model)

Hệ thống Phase 0 chốt 4 thực thể cốt lõi cho vòng đời nạp tài liệu:

```
┌────────────────────────────────────────────────────────────────────────┐
│                              Document                                  │
│  id: UUIDv5(tenant_id, project_id, logical_source_id)                  │
│  tenant_id, project_id, owner_id, logical_source_id, created_at        │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ 1
                                   │
                                   │ N
┌──────────────────────────────────▼─────────────────────────────────────┐
│                           DocumentVersion                              │
│  id: UUIDv5(document_id, version_no)                                   │
│  version_no, file_hash (SHA-256), supersedes_id                       │
│  source_published_at, observed_at, ingested_at                         │
│  valid_from, valid_to, search_ready_at, knowledge_ready_at             │
└──────────────────┬──────────────────────────────────┬──────────────────┘
                   │ 1                                │ 1
                   │                                  │
                   │ 1                                │ N
┌──────────────────▼───────────────┐  ┌───────────────▼──────────────────┐
│          SourceSnapshot          │  │           IngestionRun           │
│  id: UUIDv4                      │  │  id: UUIDv4                      │
│  document_version_id             │  │  document_version_id             │
│  storage_uri, original_filename  │  │  idempotency_key (SHA-256)       │
│  mime_type, byte_size, checksum  │  │  stage, status, attempt_count    │
│  created_at                      │  │  error_details, started/ended_at │
└──────────────────────────────────┘  └──────────────────────────────────┘
```

### 4.2. Quy tắc Sinh Stable ID và Checksum (Deterministic Identification)

Để đảm bảo tính bất biến, idempotent và khả năng dựng lại dữ liệu từ đầu:
1. **Document ID**: Sinh theo UUIDv5 dựa trên namespace cố định của dự án:
   $$\text{Document ID} = \text{UUIDv5}(\text{NAMESPACE\_URL}, \text{"sag:doc:"} + \text{project\_id} + \text{":"} + \text{logical\_source\_id})$$
2. **Document Version ID**:
   $$\text{Version ID} = \text{UUIDv5}(\text{NAMESPACE\_URL}, \text{"sag:ver:"} + \text{document\_id} + \text{":"} + \text{version\_no})$$
3. **Canonical Block ID**:
   $$\text{Block ID} = \text{UUIDv5}(\text{NAMESPACE\_URL}, \text{"sag:block:"} + \text{version\_id} + \text{":"} + \text{ordinal} + \text{":"} + \text{content\_hash})$$
4. **Search Unit Point ID (Qdrant)**:
   $$\text{Point ID} = \text{UUIDv5}(\text{NAMESPACE\_URL}, \text{"sag:qdrant:search\_units:"} + \text{search\_unit\_id})$$
5. **Idempotency Key**:
   $$\text{Idempotency Key} = \text{SHA-256}(\text{project\_id} + \text{":"} + \text{file\_hash} + \text{":"} + \text{client\_request\_token})$$

### 4.3. Các Trường Thời Gian & Truy Vết (Provenance & Temporal Fields)

Mỗi `DocumentVersion` và `Claim/Event` bắt buộc phải có các trường temporal:
- `source_published_at`: Thời điểm tài liệu gốc được tạo hoặc phát hành bên ngoài (ví dụ: ngày ban hành spec, timestamp của commit/Jira issue).
- `observed_at`: Thời điểm hệ thống lần đầu tiên phát hiện hoặc thu thập tài liệu.
- `ingested_at`: Thời điểm worker hoàn thành bóc tách và ghi nhận vào PostgreSQL.
- `valid_from` & `valid_to`: Khoảng thời gian tri thức có hiệu lực nghiệp vụ. Khi có tài liệu mới thay thế, `valid_to` của phiên bản cũ được cập nhật và `supersedes_id` trỏ từ phiên bản mới về phiên bản cũ.

---

## 5. Chốt Ngữ Nghĩa Trạng Thái & Lỗi (Pillar 3)

### 5.1. Hai Nhánh Tiến Trình Độc Lập: Search Lane vs Knowledge Lane

Trạng thái xử lý của tài liệu được chuẩn hóa thành 2 làn ranh giới rõ rệt:

```
[UPLOAD] ──> RECEIVED ──> VALIDATING ──> PARSING ──> DEDUPING ──> INDEXING
                                                                     │
                                                                     ▼
                                                             ┌──────────────┐
                                                             │ SEARCH_READY │  <── Người dùng bắt đầu tìm kiếm được!
                                                             └──────┬───────┘
                                                                    │ (Chuyển sang nhánh async nền)
                                                                    ▼
                                                             KNOWLEDGE_EXTRACTING (E0 / E1 / selective E2)
                                                                    │
                                                                    ▼
                                                             GRAPH_BUILDING (Multi-signal edge linking)
                                                                    │
                                                                    ▼
                                                             TREE_ASSIGNING (Constrained Leiden clustering)
                                                                    │
                                                                    ▼
                                                             ┌─────────────────┐
                                                             │ KNOWLEDGE_READY │  <── Tree Routing sẵn sàng!
                                                             └─────────────────┘
```

### 5.2. Bảng Định Nghĩa Trạng Thái (Readiness Matrix)

| Trạng thái | Điều kiện đạt được | Khả năng phục vụ hệ thống | Hành động khi gặp lỗi |
| :--- | :--- | :--- | :--- |
| **`RECEIVED`** | File upload hợp lệ về dung lượng, MIME type; đã ghi vào storage tạm và lưu `SourceSnapshot`. | Chưa sẵn sàng tìm kiếm. | Đánh dấu `FAILED` tại stage `RECEIVE`. File tạm bị xóa. |
| **`PARSED`** | Các canonical block đã được bóc tách thành công, xác định rõ cấu trúc heading/table/code/page. | Chưa sẵn sàng tìm kiếm. | Đánh dấu `FAILED` tại stage `PARSE`. Lưu nguyên nhân (corrupted file, unreadable PDF). |
| **`DEDUPED`** | Đã hoàn tất đối chiếu hash chính xác và near-duplicate; xác lập quan hệ phiên bản (`supersedes`). | Chưa sẵn sàng tìm kiếm. | Đánh dấu `FAILED` tại stage `DEDUP`. |
| **`SEARCH_READY`** | Search Units đã được tạo; vector dense + sparse đã index vào Qdrant; `IndexManifest` đã được xác thực toàn vẹn. | **SẴN SÀNG CHO TRUY VẤN HYBRID**. Người dùng có thể hỏi đáp với trích dẫn chính xác (Checkpoint A). | Đánh dấu `FAILED` tại stage `INDEX`. Dữ liệu vector rác trong Qdrant được rollback theo batch. |
| **`KNOWLEDGE_READY`** | Knowledge Units, thực thể, sự kiện, quan hệ đa tín hiệu và Knowledge Routing Tree đã cập nhật thành công (Checkpoint B). | **SẴN SÀNG CHO TREE-GUIDED RETRIEVAL**. Hỗ trợ định tuyến phân tầng và đa bước nhảy (multi-hop). | Ghi log cảnh báo `ENRICHMENT_FAILED`. **TUYỆT ĐỐI KHÔNG HẠ TRẠNG THÁI `SEARCH_READY`**. Hệ thống tự động fallback về global hybrid retrieval. |
| **`FAILED`** | Lỗi không thể phục hồi tại bất kỳ stage nào thuộc làn Ingestion trước `SEARCH_READY`. | Không thể tìm kiếm tài liệu này. | Cho phép người dùng hoặc worker kích hoạt retry bằng `idempotency_key`. |

### 5.3. Chuẩn Hóa Cấu Trúc Lỗi (Structured Error Envelope)

Mọi lỗi xử lý đều được chuẩn hóa theo schema:

```json
{
  "error_layer": "api | engine | llm | store | laya",
  "error_stage": "validation | parse | dedup | index | extraction | graph | tree",
  "code": "CORRUPTED_FILE | PARSER_TIMEOUT | EMBEDDING_FAILED | QDRANT_UNAVAILABLE | RATE_LIMITED",
  "message": "Thông báo lỗi chi tiết bằng tiếng Việt hoặc tiếng Anh kỹ thuật",
  "retryable": true,
  "attempt_count": 2,
  "details": {
    "file_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "step_failure_timestamp": "2026-09-28T11:15:00Z"
  }
}
```

---

## 6. Chốt Contracts Cho Query, Planner & Manifests (Pillar 4)

### 6.1. Hợp đồng Định Tuyến Laya (Laya Coarse Intent Contract)

`[FACT]` Đã kiểm chứng trong `apps/api/sag_api/services/laya_router.py`. Hợp đồng trả về từ router:

```python
class LayaRouteResult(BaseModel):
    coarse_intent: Literal["CHAT", "KNOWLEDGE", "COMMAND", "AMBIGUOUS"]
    confidence: float
    is_fallback: bool = False
    fallback_reason: str | None = None
    model_name: str = "multilingual"
```

**Quy tắc bất biến:**
- Chỉ khi `coarse_intent == "CHAT"` VÀ `confidence >= 0.65`: Đặt `need_retrieval = False`.
- Mọi trường hợp còn lại (`KNOWLEDGE`, `COMMAND`, `AMBIGUOUS`, lỗi model, model timeout): Đặt `need_retrieval = True` và giữ nguyên câu query gốc cùng user source scope.

### 6.2. Hợp đồng Trích Xuất Đặc Trưng Truy Vấn (Deterministic Query Features)

```python
class QueryFeatures(BaseModel):
    raw_query: str
    normalized_query: str
    exact_phrases: list[str]          # Cụm từ trong ngoặc kép
    identifier_terms: list[str]       # Mã lỗi, ID kỹ thuật: CTM-1234, ERR_TIMEOUT, UUID
    file_and_path_cues: list[str]     # Đường dẫn: src/auth/login.ts, /api/v1/users
    temporal_cues: list[dict]         # Mốc thời gian: "hôm qua", "tháng 8", "phiên bản 1.0"
    relational_cues: list[str]        # Từ khóa quan hệ: "nguyên nhân", "phụ thuộc", "kế thừa"
    multi_hop_triggers: list[str]     # Dấu hiệu đa bước: "tại sao X dẫn đến Y", "luồng từ A đến C"
```

### 6.3. Hợp đồng Kế Hoạch Chiến Lược Truy Vấn (Query Strategy Planner Contract)

Query Strategy Planner kết hợp `coarse_intent` từ Laya và `QueryFeatures` để quyết định chiến lược tìm kiếm:

```python
class RetrievalStrategy(str, Enum):
    DIRECT_ANSWER = "DIRECT_ANSWER"           # Dành cho CHAT thuần túy, không cần retrieval
    EXACT_LOOKUP = "EXACT_LOOKUP"             # Có identifier/path: ưu tiên exact lexical + filter
    LOCAL_FACTUAL = "LOCAL_FACTUAL"           # Hỏi sự kiện đơn lẻ: branch-local hybrid search
    TEMPORAL = "TEMPORAL"                     # Hỏi theo mốc thời gian: lọc time window + dense
    ENTITY_RELATIONAL = "ENTITY_RELATIONAL"   # Hỏi quan hệ thực thể: graph expansion 1-hop
    GLOBAL_TOPIC = "GLOBAL_TOPIC"             # Hỏi tổng quan: quét top-level nodes trên tree
    MULTI_HOP = "MULTI_HOP"                   # Leo thang suy luận: multi-branch beam routing

class QueryPlan(BaseModel):
    planner_version: str = "1.0.0"
    requested_strategy: RetrievalStrategy
    effective_strategy: RetrievalStrategy
    reason_codes: list[str]
    selected_node_ids: list[str] = Field(default_factory=list)
    escape_budget_ratio: float = 0.2          # Dành 20% ngân sách cho global escape search
    max_candidates: int = 50
    rerank_enabled: bool = True
```

### 6.4. Hợp đồng Truy Vết Tìm Kiếm (Retrieval Trace Schema)

Mỗi phản hồi tìm kiếm tại `/api/v1/search` phải đính kèm trace đầy đủ để đo đạc SLA/SLO:

```python
class RetrievalTrace(BaseModel):
    trace_id: str
    query_analysis_ms: float
    laya_ms: float
    routing_ms: float
    branch_dense_ms: float
    branch_sparse_ms: float
    escape_search_ms: float
    fusion_ms: float
    dedup_mmr_ms: float
    graph_expand_ms: float = 0.0
    rerank_ms: float = 0.0
    context_build_ms: float
    total_pipeline_ms: float
    tree_version: str | None
    selected_nodes: list[str]
    strategy_used: RetrievalStrategy
    fallback_used: bool
    fallback_reason: str | None
```

### 6.5. Hợp đồng Index Manifest & Tree Manifest

- **Index Manifest (`index_manifests`)**: Xác thực tính toàn vẹn giữa PostgreSQL và Qdrant collection:
  ```json
  {
    "manifest_version": "1.0.0",
    "project_id": "proj_12345",
    "collection_name": "search_units_proj_12345",
    "indexed_units_count": 1420,
    "dense_vector_dim": 1024,
    "sparse_model": "qdrant_bm25",
    "checksum": "sha256_of_sorted_unit_ids_and_hashes",
    "verified_at": "2026-09-28T11:15:00Z",
    "status": "VALID"
  }
  ```
- **Tree Manifest (`tree_manifests`)**: Quản lý phiên bản cây tri thức Blue-Green:
  ```json
  {
    "tree_version": "tree_v20260928_01",
    "project_id": "proj_12345",
    "config_version": "leiden_v1.1",
    "node_count": 48,
    "leaf_count": 36,
    "max_leaf_size": 25,
    "giant_ratio": 0.18,
    "routing_recall_at_k": 0.942,
    "escape_win_rate": 0.051,
    "active_slot": "SLOT_A",
    "status": "ACTIVE"
  }
  ```

---

## 7. Chốt Phạm Vi Bảo Mật, Multi-Tenancy & Rollback (Pillar 5)

### 7.1. Mô hình Phân Vùng Bảo Mật (Multi-Tenant Security Model)

Theo thỏa thuận ranh giới lưu trữ giữa Continuum BE và SAG:
1. `DATN-BE` xác thực danh tính người dùng và gửi assertion headers sang SAG API:
   - `X-Continuum-User-Id`: ID người dùng
   - `X-Continuum-Project-Id`: ID dự án hiện tại
   - `X-Continuum-Security-Partitions`: Danh sách partition quyền người dùng được phép đọc (ví dụ: `["public", "team_backend", "private_member_123"]`).
2. **PostgreSQL Enforce**: Mọi câu query metadata, version và tree profiles đều phải có mệnh đề:
   `WHERE project_id = :project_id AND security_partition_id IN (:partitions)`.
3. **Qdrant Enforce (Pre-filtering)**:
   - Trước khi thực hiện tìm kiếm Cosine Similarity, Qdrant **bắt buộc** áp bộ lọc Filter Condition:
     ```json
     {
       "must": [
         { "key": "project_id", "match": { "value": "proj_12345" } },
         { "key": "security_partition_id", "match": { "any": ["public", "team_backend"] } }
       ]
     }
     ```
   - **Tuyệt đối không post-filter sau khi LLM đã nhận chunk**: Tránh rò rỉ thông tin mật qua prompt context.

### 7.2. Chiến Lược Rollback Toàn Diện (Rollback & Failure Recovery)

1. **Rollback Schema CSDL**:
   - Sử dụng Alembic migrations có cả hàm `upgrade()` và `downgrade()`.
   - Mỗi bảng mới đều hỗ trợ soft-delete (`is_active = false`) hoặc versioning, không ghi đè dữ liệu cũ.
2. **Rollback Qdrant Index**:
   - Khi tiến trình indexing bị lỗi giữa chừng, toàn bộ điểm vector thuộc `ingestion_run_id` bị thu hồi bằng lệnh `delete_points(filter={"ingestion_run_id": run_id})`.
3. **Rollback Cây Tri Thức (Blue-Green Dual Slot)**:
   - Hệ thống duy trì 2 slot định tuyến: `SLOT_A` và `SLOT_B`.
   - Khi dựng cây mới cho dữ liệu delta, toàn bộ quá trình diễn ra trên slot không hoạt động (`inactive_slot`).
   - Chỉ khi `tree_manifest` vượt qua tất cả các cổng kiểm định chất lượng (Quality Gates: `giant_ratio < 0.3`, `routing_recall >= 0.90`), con trỏ `active_routing_slot` trong bảng `project_search_state` mới được chuyển đổi (switch pointer).
   - Nếu slot mới phát sinh lỗi trong quá trình vận hành, con trỏ có thể rollback về phiên bản trước đó trong thời gian $< 100\text{ms}$ mà không cần re-index lại vector.

---

## 8. Kế Hoạch Triển Khai Hành Động Cụ Thể (Action Plan cho Phase 0)

Để hoàn tất trọn vẹn Phase 0 và mở đường cho Phase 1, các bước hành động cụ thể bao gồm:

```
┌────────────────────────────────────────────────────────────────────────┐
│ BƯỚC 1: ĐẶC TẢ SCHEMA VÀ DATA CONTRACTS TRÊN CODE                      │
│ - Tạo Pydantic schemas cho DocumentVersion, SourceSnapshot, IngestionRun│
│ - Chuẩn hóa Enum trạng thái (SEARCH_READY, KNOWLEDGE_READY)            │
│ - Định nghĩa error envelope và payload filter contract                 │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ BƯỚC 2: THIẾT KẾ MIGRATION SCRIPT CHO POSTGRESQL                       │
│ - Viết migration Alembic tạo bảng: document_versions, source_snapshots,│
│   canonical_blocks, search_units, tree_manifests, project_search_state │
│ - Đảm bảo tính tương thích ngược với bảng documents hiện tại           │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ BƯỚC 3: XÂY DỰNG CONTRACTS CHO QUERY STRATEGY PLANNER & TRACE          │
│ - Khai báo RetrievalStrategy enum và QueryPlan schema                  │
│ - Định nghĩa cấu trúc RetrievalTrace chuẩn hóa                         │
│ - Tạo fixture regression cho các loại câu hỏi (Exact, Temporal, Chat)  │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ BƯỚC 4: RÀ SOÁT CỔNG NGHIỆM THU PHASE 0 (DEFINITION OF DONE GATE)       │
│ - Đối chiếu toàn bộ contract với mã nguồn hiện hữu                     │
│ - Xác nhận không còn trạng thái READY mơ hồ                            │
│ - Bàn giao bằng chứng trên Pull Request và Jira ticket DATN-23         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Definition of Done & Checkpoints Của Phase 0

- [x] Đã khảo sát và lập ma trận phân tích gap giữa code hiện hữu và đặc tả `Workflow v1.1`.
- [x] Đã chốt cấu trúc thực thể `Document`, `DocumentVersion`, `SourceSnapshot`, `IngestionRun` với stable ID và temporal fields.
- [x] Đã chốt ngữ nghĩa độc lập của `SEARCH_READY` và `KNOWLEDGE_READY`. Lỗi ở nhánh knowledge không hạ search capability.
- [x] Đã chốt contract cho Laya coarse intent, Query Features, Query Strategy Planner và Retrieval Trace.
- [x] Đã chốt quy chuẩn phân vùng bảo mật (`project_id`, `security_partition_id`) trên PostgreSQL và Qdrant pre-filtering.
- [x] Đã xác định chiến lược rollback cho Schema, Vector Index và Cây Tri Thức (Dual-Slot A/B).
- [x] Đã mở Pull Request [#14](https://github.com/DATN-SPRING2027/Document/pull/14) trên repository `Document` và ghi nhật ký đóng góp tài liệu.
