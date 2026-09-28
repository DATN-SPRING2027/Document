# [RESEARCH & PLAN] SAG Knowledge Routing RAG - Phase 0: Contracts & Foundations Baseline

**Ticket**: `DATN-23`  
**Assignee**: Phan Thành Tài (DE190491)  
**Status**: Research & Architecture Plan  
**Target System**: `sag-laya-integration` (SAG Engine) & Continuum AI (`DATN-BE` / `DATN-FE`)  
**Canonical Spec**: `SAG_Knowledge_Routing_RAG_Workflow_v1.1.md`  

---

## 1. Evidence Classification Standard (Truth Grading)

Báo cáo nghiên cứu và kế hoạch này tuân thủ nghiêm ngặt chuẩn phân loại bằng chứng:
- `[FACT / VERIFIED]`: Đã đối chiếu và kiểm chứng trực tiếp từ mã nguồn thực tế trong repository (`sag-laya-integration/SAG/apps/api`, `DATN-BE`, `DATN-FE`).
- `[IMPLEMENTED]`: Tính năng đã được hiện thực bằng code có thể thực thi, test đã pass.
- `[DESIGN / PROPOSED]`: Được quy định trong `SAG_Knowledge_Routing_RAG_Workflow_v1.1.md`, `11_SAG_STORAGE_SCHEMA.md` hoặc tài liệu kiến trúc, nhưng chưa có trong code.
- `[PARTIAL]`: Đã có một phần hạ tầng hoặc model/schema nhưng chưa hoàn chỉnh luồng nghiệp vụ.
- `[GAP]`: Yêu cầu bắt buộc trong đặc tả nhưng hoàn toàn chưa có trong mã nguồn hiện tại.
- `[INFERENCE]`: Suy luận logic có căn cứ từ các bằng chứng đã xác thực.
- `[DECISION REQUIRED]`: Điểm xung đột kiến trúc hoặc chính sách mở cần thống nhất giữa các thành viên.

---

## 2. Mục tiêu Task DATN-23 (Phase 0 — Contracts & Foundations)

Theo quy định tại `tasks/todo.md` và `tasks/plan.md` của hệ thống SAG, Phase 0 là giai đoạn thiết lập nền tảng hợp đồng dữ liệu, trạng thái và ranh giới hệ thống trước khi triển khai Ingestion pipeline mới (Phase 1).

5 mục tiêu cốt lõi của Phase 0:
1. **Khảo sát & mapping hiện trạng**: Rà soát luồng upload, job worker, search, query, schema, config và ACL hiện có; làm rõ phần tái sử dụng và gap.
2. **Chốt thực thể & định danh**: Thiết lập contract cho Document, DocumentVersion, SourceSnapshot, IngestionRun; stable ID, idempotency key, provenance và temporal fields.
3. **Chốt ngữ nghĩa trạng thái & lỗi**: Định nghĩa rõ ràng trạng thái tách rời của `SEARCH_READY`, `KNOWLEDGE_READY`, `FAILED`; chuẩn hóa error contract theo layer và stage.
4. **Chốt contract Query, Planner & Manifest**: Định nghĩa hợp đồng Laya coarse-intent, deterministic query features, Query Strategy Planner, retrieval trace, index manifest và tree manifest.
5. **Chốt phạm vi bảo mật & Rollback**: Thiết lập cơ chế bảo mật đa người thuê (tenant/project/security partition), cách áp ACL lên PostgreSQL/Qdrant, và chiến lược rollback.

---

*(Tài liệu đang được tiếp tục hoàn thiện chi tiết theo workflow dự án)*
