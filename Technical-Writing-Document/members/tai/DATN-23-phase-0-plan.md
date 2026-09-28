# Kế hoạch và Nghiên cứu Cơ sở cho Task DATN-23 (Phase 0)

- **Người thực hiện**: Phan Thành Tài (Tài - DE190491)
- **Task Jira**: [DATN-23](https://trankimthang0207.atlassian.net/browse/DATN-23)
- **Hạng mục**: Phase 0 — Contracts & Foundations (SAG Knowledge Routing RAG)
- **File tài liệu chính thức**: [`research-docs/SAG-Knowledge-Routing-RAG/00-phase-0-contracts-and-foundations.md`](../../research-docs/SAG-Knowledge-Routing-RAG/00-phase-0-contracts-and-foundations.md)
- **Pull Request**: [#14](https://github.com/DATN-SPRING2027/Document/pull/14)

---

## Tóm tắt nội dung nghiên cứu & Kế hoạch Phase 0

1. **Khảo sát hiện trạng & Gap Analysis**:
   - Đối chiếu hạ tầng PostgreSQL + Qdrant và Laya query routing hiện có trong `sag-laya-integration`.
   - Xác định gap lớn nhất: Model `Document` hiện là bảng phẳng thiếu versioning, thiếu `SourceSnapshot`, thiếu `canonical_blocks` và gộp chung trạng thái `ready`.

2. **Chốt Entities & Stable IDs**:
   - Tách 4 thực thể: `Document`, `DocumentVersion`, `SourceSnapshot`, `IngestionRun`.
   - Chuẩn hóa quy tắc sinh Stable ID bằng UUIDv5 và idempotency key bằng SHA-256.
   - Bổ sung các trường temporal (`valid_from`, `valid_to`, `supersedes_id`) và provenance (`source_published_at`, `observed_at`, `ingested_at`).

3. **Chốt Ngữ nghĩa Readiness & Lỗi**:
   - Tách riêng 2 làn: `SEARCH_READY` (xong canonical blocks, dedup, dense+sparse vector index) và `KNOWLEDGE_READY` (nhánh async làm giàu đồ thị và cây tri thức).
   - Lỗi ở nhánh knowledge tuyệt đối không hạ hoặc chặn `SEARCH_READY`.
   - Chuẩn hóa cấu trúc lỗi theo layer và stage.

4. **Chốt Contracts cho Query, Planner & Manifests**:
   - Giữ vững hợp đồng Laya coarse-intent (`CHAT >= 0.65` bỏ retrieval, còn lại fallback an toàn).
   - Đặc tả `QueryFeatures`, `QueryPlan` (`RetrievalStrategy`), `RetrievalTrace`.
   - Đặc tả cấu trúc `IndexManifest` và `TreeManifest` (Blue-Green dual-slot A/B).

5. **Chốt Bảo mật & Rollback**:
   - Enforce multi-tenancy qua `project_id` và `security_partition_id` bằng Qdrant pre-filtering.
   - Cơ chế rollback schema Alembic, vector batch delete, và dual-slot pointer switch $< 100\text{ms}$.
