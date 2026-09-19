# Antigravity/Gemini workspace instructions

Trước mọi task, bắt buộc đọc và tuân thủ toàn bộ [`AI_WORKFLOW.md`](AI_WORKFLOW.md)
cùng [`AGENTS.md`](AGENTS.md).

Các ràng buộc ưu tiên cao:

- Tạo branch mới từ `origin/main` cho từng task; không code trực tiếp trên `main`.
- Tách DB, backend và frontend thành branch/PR riêng.
- STRICT SPEC FREEZE: Thư mục `Document/architecture`, `Document/database-design` và `Document/deploy` là NGUYÊN BẢN CỐT LÕI (FROZEN BASELINE). Cực kỳ hạn chế thay đổi; gần như KHÔNG ĐƯỢC PHÉP SỬA trừ khi có yêu cầu và xác nhận tường minh từ người dùng.
- Mọi schema/model/migration/index/data change dùng DB PR riêng; không sửa
  migration cũ và phải chuẩn bị thông báo team.
- Được push feature branch sau khi kiểm tra/commit; không push trực tiếp hoặc
  force-push lên `main`, không tự approve hoặc merge PR.
- Feature PR chỉ target `main`; link PR phải được bàn giao để cập nhật Jira.
- Theo source architecture/UI kit thực tế của DATN, reuse trước khi tạo mới, validate
  input và xử lý Loading/Success/Empty/Error.
- Không hardcode hoặc commit secret/`.env`.
- Chạy kiểm tra phù hợp và báo đầy đủ checklist bàn giao.

Nếu `origin/main` hoặc thông tin owner/Jira bắt buộc bị thiếu, dừng trước khi
chỉnh sửa và báo người dùng; không tự bịa hoặc dùng base khác.
