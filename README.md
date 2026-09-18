# Continuum AI — tài liệu đồ án

Repository này lưu đặc tả, phạm vi MVP, mô hình actor/role, nghiên cứu và quyết định công nghệ cho Continuum AI: nền tảng hỗ trợ duy trì và chuyển giao tri thức trong một software project có nhiều team.

## Tài liệu bắt đầu

- [Phạm vi MVP](research-docs/01_MVP_SCOPE.md)
- [Actor, role và permission](research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md)
- [Quy trình ghi chú công việc và đồng bộ Jira](research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md)
- [Đặc tả dự án](research-docs/Continuum_AI_Graduation_Project_Specification_v1.0.docx.md)
- [Tech stack và quyết định kiến trúc](research-tech/Tech.md)
- [Database design (đề xuất)](database-design/03_DATABASE_DESIGN.md)

Stack MVP đã chốt: React + TypeScript + Vite với TailAdmin/Tailwind CSS; Node.js + NestJS + TypeScript; MongoDB + Mongoose; Redis + BullMQ; Python + FastAPI tích hợp SAG với LanceDB ban đầu; Cloudflare R2 ưu tiên cho file qua S3-compatible adapter. Jira Cloud đồng bộ task để hỗ trợ manual note; chat có citation là trải nghiệm tiếp quản chính. Ba role là `ADMIN`, `TEAM_LEADER`, `MEMBER`; Team Leader cần grant `project.create` cấp tổ chức từ Admin để tạo project mới. Bản thân SAG có stack riêng, không quyết định stack ứng dụng Continuum.

Đọc [AGENTS.md](AGENTS.md) và [AI_WORKFLOW.md](AI_WORKFLOW.md) trước khi thay đổi tài liệu hoặc triển khai. Sau commit khởi tạo của repository trống, các task tiếp theo phải dùng branch mới từ origin/main và PR theo quy trình này.
