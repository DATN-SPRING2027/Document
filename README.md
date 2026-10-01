# Continuum AI — tài liệu đồ án

Repository này lưu đặc tả, phạm vi MVP, mô hình actor/role, nghiên cứu và quyết định công nghệ cho Continuum AI: nền tảng hỗ trợ duy trì và chuyển giao tri thức trong một software project có nhiều team.

## Tài liệu bắt đầu

- [Phạm vi MVP](research-docs/01_MVP_SCOPE.md)
- [Actor, role và permission](research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md)
- [Quy trình quản lý task nội bộ và ghi chú công việc](research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md)
- [Đặc tả dự án](research-docs/Continuum_AI_Graduation_Project_Specification_v1.0.docx.md)
- [Kiến trúc hệ thống hoàn chỉnh (System Architecture)](architecture/README.md)
- [Sơ đồ kiến trúc trực quan tương tác](diagram/architecture_diagram.html)
- [Thiết kế Cơ sở dữ liệu & Danh mục Schemas Microservices](database-design/README.md)
- [Quyết định Task API + MongoDB (ADR-009)](research-tech/ADR-009-internal-task-source-and-mongodb.md)
- [Ranh giới lưu trữ Task](database-design/12_TASK_MANAGEMENT_SCHEMA.md)

Stack MVP đã chốt: Next.js (App Router) + TypeScript với TailAdmin/Tailwind CSS; Node.js + NestJS + TypeScript; MongoDB + Mongoose; Redis + BullMQ; Python + FastAPI tích hợp SAG; Cloudflare R2 ưu tiên cho file qua S3-compatible adapter. Continuum Task API lưu task canonical trong các collection `tasks`/`task_events` của MongoDB vận hành hiện có (`continuum_db`); Work Note có thể liên kết tùy chọn qua `taskId`; chỉ Work Note/evidence được phép mới vào SAG retrieval/index. Handover đọc task qua Continuum API và người có quyền chọn/giao successor. Jira không còn là nguồn task MVP. LanceDB là retrieval target đã chốt cho SAG MVP; PostgreSQL + pgvector/Qdrant là phương án thay thế/mở rộng, còn trạng thái triển khai runtime cần kiểm tra. Xem [ADR-009](research-tech/ADR-009-internal-task-source-and-mongodb.md) và [Technology baseline](research-tech/Tech.md). Chat có citation là trải nghiệm tiếp quản chính. Ba role là `ADMIN`, `TEAM_LEADER`, `MEMBER`; Team Leader cần grant `project.create` cấp tổ chức từ Admin để tạo project mới. Bản thân SAG có stack riêng, không quyết định stack ứng dụng Continuum.

Đọc [AGENTS.md](AGENTS.md) và [AI_WORKFLOW.md](AI_WORKFLOW.md) trước khi thay đổi tài liệu hoặc triển khai. Sau commit khởi tạo của repository trống, các task tiếp theo phải dùng branch mới từ origin/main và PR theo quy trình này.
