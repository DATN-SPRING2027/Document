# [RESEARCH] B2B SaaS Benchmarking & Authentic Pattern Decisions

> **Tài liệu phục vụ**: `DATN-351` (Figma USER-01: Research and design user directory), `DATN-352`, `DATN-353`  
> **Tác giả / Assignee**: Nguyễn Hồng Phúc  
> **Nguyên tắc cốt lõi**: **KHÔNG tự động generate UI phi thực tế bằng AI**. Toàn bộ giao diện và luồng tương tác đều được đào sâu nghiên cứu, đối chiếu từ các Design System, UI Templates mã nguồn mở và sản phẩm SaaS doanh nghiệp hàng đầu thế giới trên Internet.

---

## 1. Bối Cảnh & Phương Pháp Nghiên Cứu Mẫu (Research Methodology)

Trong phát triển phần mềm doanh nghiệp B2B (Enterprise SaaS), giao diện quản lý nhân sự (**User Directory**, **Member Governance**, **Access Control**) là trung tâm điều hành nhạy cảm về bảo mật và vận hành. Thay vì để AI tự sinh (hallucinate) các giao diện ngẫu nhiên không có chuẩn mực, nhóm thực hiện phương pháp **Nghiên cứu khảo sát sâu trên Internet (Deep-dive Internet Benchmarking)**:

1. **Khảo sát Design System & Figma Kits thịnh hành nhất**: Untitled UI (Figma Community), Tailwind UI, shadcn/ui (TanStack Table).
2. **Khảo sát các nền tảng Identity & Access Management (IAM) chuyên nghiệp**: Clerk (`<OrganizationProfile />`), WorkOS Directory Sync.
3. **Khảo sát hệ thống quản trị của các sản phẩm B2B SaaS dẫn đầu**: Atlassian Administration (`admin.atlassian.com`), GitHub Enterprise People (`github.com/orgs/{org}/people`), Linear App (`linear.app`).

Từ đó, đúc kết thành **4 mô hình giao diện** được lập trình trực quan có thể chuyển đổi tức thì trên bộ công cụ `DEMO_FE_TASK`.

---

## 2. Danh Sách Các Mẫu Tham Chiếu Khảo Sát Từ Internet

### 2.1. Mẫu 1: Untitled UI — B2B SaaS User Table System
* **Nguồn / Tác giả**: Jordan Hughes (`untitledui.com` & Figma Community `@untitledui`)
* **Định dạng**: Figma UI Kit & React Aria / Tailwind CSS Component Library
* **Đặc trưng cấu trúc**:
  - Ô người dùng tích hợp (Composite User Cell): Avatar tròn 40x40px + Tên in đậm + Email chữ xám bên dưới.
  - Chấm LED trạng thái mềm mại (Soft Tinted Status Pill): Chấm tròn 6px kết hợp nền pastel trong suốt (Active = Xanh lá `#ecfdf5`, Pending = Vàng hổ phách `#fffbeb`, Suspended = Đỏ hồng `#fff1f2`).
  - Thanh phân trang tiêu chuẩn dưới chân bảng: `Showing 1-10 of 48 results` kèm nút `< Previous` và `Next >`.
* **Minh họa cấu trúc Anatomy**:
  ```text
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ [Avatar] Nguyễn Hồng Phúc        [ADMIN]      ● Hoạt động   phuc2348@... [•••]│
  │          phuc2348@gmail.com                                                 │
  └─────────────────────────────────────────────────────────────────────────────┘
  ```

---

### 2.2. Mẫu 2: Tailwind UI — "Tables with Avatars and Multi-line Content"
* **Nguồn**: Tailwind Labs (`tailwindui.com/components/application-ui/tables`)
* **Định dạng**: Tailwind CSS, React, Vue
* **Đặc trưng cấu trúc**:
  - Bố cục danh sách phân dòng tinh gọn (`divide-y divide-gray-200`), loại bỏ viền ngoài nặng nề.
  - Sử dụng Font tabular nums cho ngày tháng và số liệu giúp các con số thẳng hàng hoàn hảo.
  - Phù hợp màn hình mật độ thông tin cao (High Density), cho phép xem nhanh nhiều nhân sự mà không tốn diện tích cuộn trang.

---

### 2.3. Mẫu 3: shadcn/ui & TanStack Table (`tablecn`)
* **Nguồn**: shadcn (`ui.shadcn.com/docs/components/data-table`) và Sadmann (`github.com/sadmann7/tablecn`)
* **Đặc trưng cấu trúc**:
  - Kiến trúc Headless UI kết hợp Radix UI Primitives: Tối ưu hoàn toàn khả năng tiếp cận (Accessibility WCAG 2.1 AA).
  - Bộ lọc đa chiều (Faceted Filter Popover): Cho phép lọc kết hợp nhiều tiêu chí (Role + Status + Project) cùng lúc với debounce 300ms.
  - Chế độ chọn nhiều dòng (Row Selection) hỗ trợ thanh công cụ nổi (Floating Action Bar) khi có ít nhất 1 dòng được chọn.

---

### 2.4. Mẫu 4: Clerk `<OrganizationProfile />` & WorkOS Directory Sync
* **Nguồn**: Clerk Docs (`clerk.com/docs/components/organization/organization-profile`) & WorkOS (`workos.com/directory-sync`)
* **Đặc trưng cấu trúc**:
  - Mô hình dữ liệu thành viên chuẩn: `OrganizationMembership` (userId, organizationId, role, status, 2FA status, lastActiveAt).
  - Quản lý lời mời đang chờ (`Pending Invites`): Hiển thị hạn lời mời (Expires in 7 days), có nút bấm nhanh "Gửi lại lời mời" (Resend invite) hoặc hủy lời mời ngay trên dòng.
  - Cập nhật quyền hạn lạc quan (Optimistic UI): Khi Admin đổi role qua Dropdown, giao diện cập nhật ngay kèm thông báo Toast, tự động rollback nếu API trả mã lỗi.

---

### 2.5. Mẫu 5: Linear App — Workspace Members & Slide-over Drawer
* **Nguồn**: Linear (`linear.app`)
* **Đặc trưng cấu trúc**:
  - **Slide-over Side Sheet (560px)**: Khi click vào bất kỳ dòng nào, Drawer trượt từ mép phải ra, giữ nguyên ngữ cảnh danh bạ nền mà không cần reload trang.
  - Phím tắt thông minh: Nhấn phím `Esc` để đóng Drawer, phím mũi tên lên/xuống để duyệt nhân sự kế tiếp.
  - Typography tối giản, bo góc chuẩn mực, tương thích hoàn hảo chế độ Light/Dark Mode.

---

### 2.6. Mẫu 6: Atlassian Administration (`admin.atlassian.com`)
* **Nguồn**: Atlassian Cloud Admin & Atlassian Design System (`atlassian.design`)
* **Đặc trưng cấu trúc**:
  - Quản trị bảo mật quy mô lớn: Kiểm soát xác thực 2 bước (2FA Enforcement).
  - Cảnh báo an toàn (Safety Impact Warning): Chặn thao tác tự tước quyền Admin của chính mình nếu là Admin hoạt động duy nhất trong tổ chức (`Prevent Lockout Rule`).
  - Thao tác hàng loạt (Bulk Actions): Đình chỉ tài khoản hoặc gửi lại email xác nhận cho nhiều nhân sự cùng lúc.

---

## 3. Bảng Ma Trận So Sánh Các Mẫu Thực Tế

| Tiêu Chí Kỹ Thuật / UX | TailAdmin (Mẫu Cũ) | Untitled UI (Mẫu 1) | Tailwind + Linear (Mẫu 2) | Atlassian (Mẫu 3) | Lựa Chọn Cho Continuum AI |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Nguồn gốc** | Template HTML tĩnh | Untitledui.com | Tailwind Labs & Linear | Atlassian.design | **Tổng hợp tinh hoa từ các mẫu chuẩn** |
| **Phù hợp Schema 3 Role** | ❌ Chức danh tự do | ✅ 3 Role IAM | ✅ 3 Role IAM | ✅ 3 Role IAM | **ADMIN (Tím), TEAM_LEADER (Xanh), MEMBER (Xám)** |
| **Xem chi tiết hồ sơ** | ❌ Không có | Modal giữa màn hình | **Slide-over Drawer** | Full-page redirect | **Slide-over Drawer (560px) giữ ngữ cảnh** |
| **Bảo mật 2FA & Đăng nhập** | ❌ Không có | ✅ Có cột 2FA & Login | ❌ Lược giản | ✅ Báo cáo 2FA | **Cột Đăng nhập cuối + Badge 2FA** |
| **Thao tác hàng loạt (Bulk)** | ❌ Không có | Checkbox cơ bản | Menu context | ✅ Bulk Bar hoàn chỉnh | **Floating Bulk Bar (Hiện khi chọn dòng)** |
| **Xử lý trạng thái biên** | ❌ Trắng trang | Loading Spinner | Shimmer | Skeleton | **5 Edge States đầy đủ (Skeleton, Empty, 500, 403)** |
| **Đáp ứng kích thước (RWD)** | Bị tràn bảng | Co giãn cột | Card View rút gọn | Co giãn cột | **Tự động chuyển Card View trên Mobile 375px** |

---

## 4. Hiện Thực Hóa Trực Quan Tại `DEMO_FE_TASK`

Toàn bộ các mẫu khảo sát trên không nằm lại trên lý thuyết mà đã được tích hợp đầy đủ vào ứng dụng thực nghiệm tại thư mục `DEMO_FE_TASK`:

1. **Bộ Chuyển Đổi Mẫu Thiết Kế (Design Model Switcher)**:
   - Cho phép reviewer/giảng viên click chọn giữa 4 mẫu thực tế:
     - `Mẫu Gốc`: Baseline theo prototype hiện tại của nhóm.
     - `Untitled UI`: Đạt chuẩn Design System B2B hiện đại nhất.
     - `Tailwind + Linear`: Mật độ cao, tối giản phẳng.
     - `Atlassian Enterprise`: Quản trị an ninh và thao tác hàng loạt.
2. **Nút "So Sánh Các Mẫu Thiết Kế" (Compare Modal)**:
   - Bảng đối chiếu ưu/nhược điểm từng mẫu kèm **đường link nguồn trực tiếp từ Internet** để kiểm chứng.
3. **Mô Phỏng 5 Trạng Thái Biên (Edge States Simulator)**:
   - `Normal View`: Hiển thị bảng dữ liệu đầy đủ 48 thành viên.
   - `Skeleton Loading`: Hiệu ứng shimmer nhấp nháy 5 dòng khi mạng chậm.
   - `Empty Search Result`: Giao diện rỗng kèm nút "Đặt lại bộ lọc".
   - `Empty Organization`: Trạng thái tổ chức mới chưa có thành viên.
   - `Server Error (500)`: Nút thử lại (Retry) kèm mã lỗi hệ thống.
   - `Permission Denied (403)`: Báo lỗi khi user không có quyền quản trị.
4. **Modal Thông Số Thiết Kế Figma (Figma Specs & Handoff)**:
   - Bảng mã màu Hex, Spacing tokens (hệ 8px), và Typography chuẩn Inter.
