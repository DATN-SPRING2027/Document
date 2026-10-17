# Hồ Sơ Nghiên Cứu & Đặc Tả Frontend Cho Cụm Task USER (Phúc FE)

Tài liệu được biên soạn phục vụ cụm task thiết kế Hi-Fi Figma và phát triển Frontend cho nhân sự **Nguyễn Hồng Phúc** thuộc dự án **Continuum AI** (Đồ án tốt nghiệp B2B SaaS).

---

## 1. Danh Sách Task Phụ Trách

| Mã Task Jira | Tên Task (Tiêu đề) | Module Figma | Phạm vi Frontend | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **`DATN-351`** | **Figma USER-01: Research and design user directory** | `03 Organization` / `Users` | Màn hình Danh bạ người dùng, tìm kiếm, bộ lọc đa chiều, phân trang, Table/Grid view | Nghiên cứu & Thiết kế |
| **`DATN-352`** | **Figma USER-02: Research and design user profile detail** | `03 Organization` / `User Drawer` | Panel trượt (Slide-over Drawer) xem chi tiết hồ sơ 360°, phân định Role & Assignment | Nghiên cứu & Thiết kế |
| **`DATN-353`** | **Figma USER-03: Research and design basic user profile editing** | `03 Organization` / `Edit Form` | Luồng & Form chỉnh sửa hồ sơ (Phân tách Self-Service vs Admin Management, Validation) | Nghiên cứu & Thiết kế |

---

## 2. Cấu Trúc Bộ Tài Liệu Trong Thư Mục `PhucFE`

1. **[01-BENCHMARK-ENTERPRISE-SAAS.md](file:///f:/%C4%90%E1%BB%93-%C3%81n-T%E1%BB%91t-Nghi%E1%BB%87p/PhucFE/01-BENCHMARK-ENTERPRISE-SAAS.md)**:
   - Nghiên cứu đối chiếu 3 nền tảng SaaS hàng đầu: **Atlassian Admin**, **GitHub Enterprise**, **Linear App**.
   - Lý do chọn lựa UI patterns (Side-over Drawer, Faceted Filter, Badge Hierarchy).
   - Phân tích sự khác biệt và cải tiến vượt bậc so với template tĩnh TailAdmin.

2. **[02-DATN-351-USER-DIRECTORY-FE-SPEC.md](file:///f:/%C4%90%E1%BB%93-%C3%81n-T%E1%BB%91t-Nghi%E1%BB%87p/PhucFE/02-DATN-351-USER-DIRECTORY-FE-SPEC.md)**:
   - Đặc tả kiến trúc Component cho Danh bạ người dùng (`DATN-351`).
   - Xử lý các trạng thái biên: `Loading Skeleton`, `Empty Filter Result`, `Permission Denied (403)`, `Error (500)`.
   - TypeScript Interfaces, Mock Data mẫu khớp chuẩn MongoDB `continuum_iam`.

3. **[03-DATN-352-USER-PROFILE-DETAIL-FE-SPEC.md](file:///f:/%C4%90%E1%BB%93-%C3%81n-T%E1%BB%91t-Nghi%E1%BB%87p/PhucFE/03-DATN-352-USER-PROFILE-DETAIL-FE-SPEC.md)**:
   - Đặc tả kiến trúc Panel trượt (`Slide-over Drawer`) xem chi tiết hồ sơ (`DATN-352`).
   - 4 Tabs nghiệp vụ: **Tổng quan**, **Vai trò & Quyền hạn**, **Dự án & Nhóm**, **Nhật ký hoạt động**.
   - Thể hiện rõ sự phân định giữa **Role tĩnh** (`ADMIN`, `TEAM_LEADER`, `MEMBER`) và **Scoped Assignments** (`SME`, `KNOWLEDGE_OWNER`).

4. **[04-DATN-353-USER-PROFILE-EDITING-FE-SPEC.md](file:///f:/%C4%90%E1%BB%93-%C3%81n-T%E1%BB%91t-Nghi%E1%BB%87p/PhucFE/04-DATN-353-USER-PROFILE-EDITING-FE-SPEC.md)**:
   - Đặc tả Form cập nhật hồ sơ (`DATN-353`).
   - Ma trận phân quyền chỉnh sửa: Người dùng tự sửa (Self-Service) vs Admin quản trị (Admin Control).
   - Quy tắc kiểm tra hợp lệ (Form Validation rules), xử lý lỗi tại từng trường (Field-level errors), cảnh báo an toàn (Safe Guard Rules).

5. **[05-DESIGN-TOKENS-AND-COMPONENTS.md](file:///f:/%C4%90%E1%BB%93-%C3%81n-T%E1%BB%91t-Nghi%E1%BB%87p/PhucFE/05-DESIGN-TOKENS-AND-COMPONENTS.md)**:
   - Hệ thống Tokens: Bảng màu Trạng thái & Role Badges, Typography 1440px Desktop, Kho icon Lucide.
   - Từ điển Song ngữ hoàn chỉnh (`vi` / `en`) sẵn sàng áp dụng vào mã nguồn hoặc prototype Figma Make.
