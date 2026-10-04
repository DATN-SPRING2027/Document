# Continuum AI — tài liệu đồ án

Repository này lưu đặc tả, phạm vi MVP, mô hình actor/role, nghiên cứu và quyết định công nghệ cho Continuum AI: nền tảng hỗ trợ duy trì và chuyển giao tri thức trong một software project có nhiều team.

## Tài liệu bắt đầu

- [Phạm vi MVP](research-docs/01_MVP_SCOPE.md)
- [Actor, role và permission](research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md)
- [Organization, workspace và readiness hợp đồng truy cập](research-docs/Workspace/00-organization-and-access-contract-readiness.md)
- [Use Case quản lý Project, Team và Membership](research-docs/Workspace/05-project-team-access-use-cases.md)
- [Quy trình quản lý task nội bộ và ghi chú công việc](research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md)
- [Đặc tả dự án](research-docs/Continuum_AI_Graduation_Project_Specification_v1.0.docx.md)
- [Kiến trúc hệ thống hoàn chỉnh (System Architecture)](architecture/README.md)
- [Sơ đồ kiến trúc trực quan tương tác](diagram/architecture_diagram.html)
- [Thiết kế Cơ sở dữ liệu & Danh mục Schemas Microservices](database-design/README.md)
- [Quyết định Task API + MongoDB (ADR-009)](research-tech/ADR-009-internal-task-source-and-mongodb.md)
- [Quyết định triển khai Task Service trong hai repo hiện tại (ADR-010)](research-tech/ADR-010-task-service-in-existing-repositories.md)
- [Ranh giới lưu trữ Task](database-design/12_TASK_MANAGEMENT_SCHEMA.md)
- [DATN-93 — Task V1 contract readiness và quyết định còn thiếu](research-docs/Internal-Work-Management/13-task-v1-contract-readiness.md)

Stack hiện tại: Next.js (App Router) + TypeScript với TailAdmin/Tailwind CSS; Node.js + NestJS + TypeScript; MongoDB + Mongoose; Redis + BullMQ; Python + FastAPI tích hợp SAG; Cloudflare R2 ưu tiên cho file qua S3-compatible adapter. Continuum là nguồn chuẩn của task: Task Service chạy độc lập nhưng source nằm trong DATN_BE hiện tại, giao diện/API client nằm trong DATN_FE hiện tại; service sở hữu `tasks`/`task_events` trong logical database `continuum_task` trên MongoDB replica set hiện có. FE đi qua BFF/Gateway; Work Note/Handover/Agent dùng API hoặc event contract, không truy cập database Task trực tiếp. Jira không phải nguồn task MVP. Chỉ Work Note/evidence đủ điều kiện mới đi vào SAG retrieval/index; quyết định Task không thay đổi lựa chọn SAG. Xem [ADR-009](research-tech/ADR-009-internal-task-source-and-mongodb.md), [ADR-010](research-tech/ADR-010-task-service-in-existing-repositories.md) và [Technology baseline](research-tech/Tech.md). Chat có citation là trải nghiệm tiếp quản chính. `PLATFORM_OPERATOR` vận hành nền tảng và bootstrap Organization Admin nhưng không có mặc định đọc nội dung Organization; ba role Organization/Project là `ADMIN`, `TEAM_LEADER`, `MEMBER`. Organization Membership `ACTIVE` xác lập context; mọi authenticated member đang ACTIVE đều có thể tạo Project PRIVATE và trở thành Project `MEMBER` ban đầu. Bản thân SAG có stack riêng.

Đọc [AGENTS.md](AGENTS.md) và [AI_WORKFLOW.md](AI_WORKFLOW.md) trước khi thay đổi tài liệu hoặc triển khai. Sau commit khởi tạo của repository trống, các task tiếp theo phải dùng branch mới từ origin/main và PR theo quy trình này.
