# Continuum AI — tài liệu đồ án

Repository này lưu đặc tả, phạm vi MVP, mô hình actor/role, nghiên cứu và quyết định công nghệ cho Continuum AI: nền tảng hỗ trợ duy trì và chuyển giao tri thức trong một software project có nhiều team.

## Tài liệu bắt đầu

- [Phạm vi MVP](research-docs/01_MVP_SCOPE.md)
- [Actor, role và permission](research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md)
- [Đặc tả dự án](research-docs/Continuum_AI_Graduation_Project_Specification_v1.0.docx.md)
- [Tech stack và quyết định kiến trúc](research-tech/Tech.md)
- [Ghi chú nghiên cứu](research-docs/RESEARCH%20%C4%90%E1%BB%92%20%C3%81N.md)

Stack MVP đã chốt: React + TypeScript + Vite với TailAdmin/Tailwind CSS; Node.js + NestJS + TypeScript; MongoDB + Mongoose; Redis + BullMQ; Python + FastAPI tích hợp SAG với LanceDB ban đầu; MinIO/S3 cho file. Bản thân SAG có stack riêng, không quyết định stack ứng dụng Continuum.

Đọc [AGENTS.md](AGENTS.md) và [AI_WORKFLOW.md](AI_WORKFLOW.md) trước khi thay đổi tài liệu hoặc triển khai. Sau commit khởi tạo của repository trống, các task tiếp theo phải dùng branch mới từ origin/main và PR theo quy trình này.
