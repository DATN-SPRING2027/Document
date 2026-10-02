# Problem and Pain-Point Research

> **Decision amendment — 2026-10-02:** Earlier framing described Jira task-context synchronization as the proposed/current MVP and treated internal task ownership as undecided. That is superseded: Continuum Task API is canonical for task lifecycle in the MVP; Jira task import/sync is out of scope. This document remains research on knowledge-continuity pain and whether broader enterprise workflow capability is needed. It does not reopen the accepted task-source decision.

**Trạng thái:** Draft research để human review — không phải requirement, recommendation được duyệt hay quyết định sản phẩm.  
**Mốc đối chiếu:** repository evidence hiện có và thông tin vendor công khai được kiểm tra ngày 2026-09-25.

## Câu hỏi nghiên cứu

Sau khi Continuum đã chốt Task API nội bộ làm nguồn task cho MVP, DATN còn cần mở rộng thành work-management platform cấp doanh nghiệp hay không; những pain point rộng hơn có được giải quyết tốt hơn bằng cấu hình/quy trình hoặc một connector SaaS được duyệt riêng không?

Các nhãn trong tài liệu: `[FACT]` là sự kiện quan sát/đo được; `[DOCUMENTED]` là nội dung đã ghi trong tài liệu DATN; `[WEB RESEARCH]` là thông tin từ nguồn ngoài có link; `[INFERENCE]` là kết luận suy ra; `[ASSUMPTION]` là giả định tạm; `[PROPOSAL]` là phương án để xem xét; `[UNKNOWN]` là thiếu evidence; `[DECISION REQUIRED]` là lựa chọn cần người có thẩm quyền.

## Kết luận tạm thời

- `[DOCUMENTED]` Continuum MVP kết hợp quản lý task nội bộ với knowledge continuity cho **một software project có nhiều team**; Continuum Task API là task source canonical. Nguồn chuẩn: `research-docs/01_MVP_SCOPE.md`, `03_DAILY_WORKFLOW_AND_JIRA_SYNC.md`, Task Management Use Cases và ADR-009/010.
- `[SUPERSEDED]` Jira task context sync từng được ghi là hỗ trợ capture/knowledge. Quyết định hiện tại loại Jira import/sync khỏi task MVP; Work Note vẫn do con người xác nhận và có thể giữ `taskId` tùy chọn để liên kết đến Continuum Task API.
- `[UNKNOWN]` Chưa có evidence trong repository về Jira plan/license hiện DATN đang dùng, số billable seats, invoice, Marketplace apps, workflow/configuration, mức độ sử dụng Confluence, Jira friction đo được, hay phỏng vấn người dùng. Vì vậy không thể xác nhận “Jira quá đắt”, “Jira thiếu Department”, hoặc pain point thực tế là Jira.
- `[WEB RESEARCH]` Jira Cloud có Free plan tối đa 10 người và các plan trả phí có những khác biệt về permissions, automation, storage, planning; Premium có cross-team/project planning. Do đó khẳng định chung rằng Jira không thể hỗ trợ cross-team là không chính xác; giới hạn có thể là plan hoặc cấu hình. Xem [Jira pricing](https://www.atlassian.com/software/jira/pricing) và [Plans in Jira Premium](https://support.atlassian.com/jira-software-cloud/docs/what-is-advanced-roadmaps/).
- `[INFERENCE]` Hiện hypothesis “xây internal ecosystem để tiết kiệm tiền và hợp governance hơn” chưa được chứng minh. Nó cần được kiểm thử độc lập với mục tiêu Continuum đã được ghi nhận.

## Pain point và giả thuyết nguyên nhân

| Pain point được nêu | Evidence hiện có | Root-cause khả dĩ cần phân biệt | Jira có phải nguyên nhân? | Liên quan đến internal platform |
|---|---|---|---|---|
| Chi phí SaaS | Chỉ có hypothesis; không có invoice, plan, user count | SaaS cost; plan limitation; seat provisioning/billing; Marketplace apps; admin overhead | `[UNKNOWN]` | Chỉ đánh giá sau khi biết TCO thực tế và nhu cầu tính năng |
| Giới hạn plan/user | Tài liệu public cho biết tier/seat limits | Product/plan limitation; có thể giải quyết bằng cấu hình hoặc đổi plan | Có thể một phần; phải xác định feature cụ thể | Không tự build cho tới khi so sánh nâng plan, tối ưu seat, giải pháp thay thế |
| Friction trong cách tổ chức công việc | Chưa có user research/workflow observation | Operating model; configuration; information architecture; product limitation | `[UNKNOWN]` | Một lớp điều phối có thể hữu ích nhưng cũng làm phát sinh thao tác mới |
| Task và knowledge phân mảnh | Continuum research xác định task context khác với tri thức xác nhận | Knowledge fragmentation; thiếu liên kết/provenance; integration problem | Không chỉ do Jira; nhiều nguồn có chủ đích khác nhau | Có liên quan trực tiếp tới mục tiêu Continuum; không chứng minh cần thay task manager |
| Governance theo Department | Tài liệu accepted hiện tập trung Organization/Project/Team scope, không có Department role/domain đã chốt | Governance model; hierarchy/configuration; plan permission boundary | Chưa thể kết luận Jira thiếu Department | Cần xác minh cardinality và policy; không tạo Department entity theo giả định |
| Executive visibility | Chưa có decision questions, báo cáo hay đối tượng lãnh đạo được xác nhận | Reporting/configuration; portfolio planning; data quality; governance | Jira cung cấp dashboard/planning ở mức khác nhau theo plan/product | Xây view chỉ khi biết quyết định quản lý cụ thể và quyền drill-down |

## Root-cause taxonomy cần dùng khi phỏng vấn

1. SaaS cost (subscription, apps, admin)  2. Product limitation  3. Plan limitation  4. Configuration problem  5. Operating-model problem  6. Information-architecture problem  7. Governance problem  8. Knowledge fragmentation  9. Integration problem.

Một pain point có thể có nhiều nguyên nhân cùng lúc. Không gán tất cả cho Jira. Với từng ví dụ thực tế, ghi người gặp, tác vụ, tần suất, thời gian/chi phí, workaround, hậu quả và bằng chứng.

## Bằng chứng còn thiếu

- `[UNKNOWN]` Roster billable users theo từng sản phẩm, plan/cadence/currency, invoice và Marketplace/Guard add-ons.
- `[UNKNOWN]` Danh sách top workflow và cấu hình Jira hiện tại; project/issue hierarchy, permission schemes, automation rules, integrations, dashboards và mức sử dụng.
- `[UNKNOWN]` Phỏng vấn đại diện member, team leader, người quản trị và người ra quyết định; ví dụ gần đây về blocker, handover, tìm knowledge, report.
- `[UNKNOWN]` Định nghĩa “organization”, Department, team và project thực tế của nhóm DATN; số lượng hiện tại/dự kiến và quan hệ nhiều-nhiều.
- `[UNKNOWN]` So sánh Jira-only/Jira+Confluence/Continuum-hybrid dựa trên cùng một bộ use case.

## Cách xác minh hypothesis (đề xuất nghiên cứu)

`[PROPOSAL]` Thu thập invoice và cấu hình trước; lập inventory quy trình; chọn 3–5 tình huống cụ thể; đo baseline (thời gian, số lần chuyển tool, sai lệch sync, thời gian tìm thông tin); sau đó prototype/pilot nhỏ theo kiến trúc hiện đã accepted. Không đặt ngưỡng thành công trước khi có baseline và người chịu trách nhiệm chọn ngưỡng.

## Nguồn DATN

- `product_docs/research-docs/01_MVP_SCOPE.md`
- `product_docs/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md`
- `product_docs/research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md`
- `product_docs/research-docs/Workspace/00-workspace-research-review-v2.md`
- `docs/decisions/decision-register.md` (DEC-011, DEC-013, DEC-014, DEC-015)
