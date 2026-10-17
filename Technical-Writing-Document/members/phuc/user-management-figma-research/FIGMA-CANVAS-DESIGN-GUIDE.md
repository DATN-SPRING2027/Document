# Hướng Dẫn Vẽ & Tổ Chức Frame Trên Figma Canvas (Desktop 1440px)

Tài liệu hướng dẫn chi tiết cách dựng các Frame tĩnh trên Figma Canvas và cấu hình Auto Layout, Component Variants, Prototype Links cho cụm màn hình `USER-01`, `USER-02`, `USER-03`.

---

## 1. Cấu Trúc Trang (Page & Canvas Organization)

Tạo một Figma Page mới mang tên: `Module 03 — Organization & Users`.

Trong Canvas, sắp xếp các Frame theo thứ tự từ trái sang phải:

```text
[Frame 1: USER-01]            [Frame 2: USER-01 Edge States]     [Frame 3: USER-02]       [Frame 4: USER-03]
User Directory - Default      Empty & Skeleton Loading           Profile Detail Drawer    Profile Edit Modal
(1440 × 1024 px)              (1440 × 1024 px)                   (560 × 1024 px)          (640 × 680 px)
```

---

## 2. Thông Số Kỹ Thuật Chi Tiết Từng Frame

### 2.1. Frame 1: `[USER-01] User Directory - Default` (1440 × 1024 px)
* **Bố cục tổng thể (App Shell)**:
  - Sidebar bên trái: Width `260px`, Height `Fill`, Background `#0F172A` (Slate 900) hoặc `#FFFFFF` (Light mode). Mục "Thành viên" được highlight active (`bg-indigo-50 text-indigo-600`).
  - Header trên cùng: Height `64px`, Width `Fill`, Border bottom `#E2E8F0`. Chứa Org Switcher (`Công ty Sao Bắc ▾`), Search global, Notifications, User Avatar.
  - Main Content Canvas: Width `1180px`, Auto Layout Vertical (`padding: 32px`, `gap: 24px`).
* **Header Màn hình**:
  - Breadcrumb: `Trang chủ / Tổ chức / Thành viên` (Text 13px, Slate 500).
  - Tiêu đề H1: `Danh bạ người dùng` (Text 24px SemiBold, Slate 900).
  - Phụ đề: `Tìm kiếm người dùng và xem thông tin cơ bản trong Organization.` (Text 14px Regular, Slate 500).
  - Nút chính (CTA): `+ Thêm thành viên` (Button Primary Indigo, Height 40px, Padding X 16px, Border Radius 8px).
* **Toolbar & Faceted Filters**:
  - Auto Layout Horizontal, `gap: 12px`, `align: center`.
  - Search Input: Width `320px`, Height `40px`, Icon kính lúp trái, Placeholder: `Tìm theo tên hoặc email...`.
  - Dropdown Filter 1: `Tất cả vai trò ▾` (Width `160px`).
  - Dropdown Filter 2: `Tất cả trạng thái ▾` (Width `160px`).
  - Nút Refresh: Icon `↻` (Height 40px, Width 40px).
* **Data Table (Auto Layout Vertical, Border Radius 12px, Border 1px #E2E8F0)**:
  - Header Row (Height 44px, Background `#F8FAFC`):
    - Cột 1: `NGƯỜI DÙNG` (Width `360px`, Text 12px SemiBold uppercase, Slate 500).
    - Cột 2: `VAI TRÒ` (Width `220px`).
    - Cột 3: `DỰ ÁN` (Width `140px`).
    - Cột 4: `TRẠNG THÁI` (Width `180px`).
    - Cột 5: `THAO TÁC` (Width `80px`, Align right).
  - Data Rows (Height 68px, Border bottom 1px `#F1F5F9`, Hover state: `#F8FAFC`):
    - Cột 1: Avatar (40×40px tròn) + Vertical stack [Họ tên (14px Medium), Email (13px Regular Slate 500)].
    - Cột 2: Role Badge (`ADMIN` = Tím Indigo, `TEAM_LEADER` = Xanh dương Blue, `MEMBER` = Xám Slate).
    - Cột 3: Số lượng dự án (VD: `3 dự án`).
    - Cột 4: Status Pill (Chấm đèn xanh lá + `Đang hoạt động`, hoặc chấm vàng + `Chờ kích hoạt`).
    - Cột 5: Icon chevron `>` hoặc `•••` action button.
* **Pagination Footer (Height 56px, Border top 1px #E2E8F0)**:
  - Trái: `Hiển thị 1 - 5 trên 48 thành viên` (Text 13px, Slate 500).
  - Phải: Nút `< Trước`, `1`, `2`, `3`, `Sau >`.

---

### 2.2. Frame 2: `[USER-02] User Profile Detail - Drawer` (560 × 1024 px)
* **Loại Frame**: Slide-over Drawer (Panel trượt).
* **Hiệu ứng khi hiển thị**: Nền mờ Backdrop (30% Black `#0000004D`), Drawer nằm sát mép phải màn hình (`Top: 0, Right: 0`), bo góc trái `16px 0 0 16px`, Shadow `Elevation 4` (`box-shadow: -4px 0 24px rgba(0,0,0,0.08)`).
* **Drawer Header (Padding: 24px, Border bottom 1px #E2E8F0)**:
  - Trái: Tiêu đề `Chi tiết Organization Membership` (Text 18px SemiBold) + Subtitle `membership-u1 · Công ty Sao Bắc` (Text 12px Slate 500).
  - Phải: Nút đóng `✕` (Icon X, 32×32px tròn).
* **Profile Identity Card (Padding: 24px, Background #F8FAFC, Radius 12px)**:
  - Avatar lớn 64×64px kèm chấm đèn trạng thái góc dưới.
  - Họ tên: `Minh Anh` (Text 20px Bold, Slate 900).
  - Email: `minh.anh@example.test` (Text 14px Regular, Slate 500).
  - Role Badge: `Quản trị viên (ADMIN)` hoặc `Trưởng nhóm (TEAM_LEADER)`.
* **4 Tabs Điều Hướng (Auto Layout Horizontal, Border bottom 1px #E2E8F0)**:
  - `Tổng quan` (Active, viền xanh Indigo dưới chân).
  - `Vai trò & Quyền hạn`.
  - `Dự án & Nhóm`.
  - `Hoạt động`.
* **Tab Content - Dữ Liệu Chi Tiết**:
  - Grid 2 cột các Card thông tin:
    - Card 1: `MEMBERSHIP ID` $\rightarrow$ `membership-u1`
    - Card 2: `USER ID` $\rightarrow$ `u1`
    - Card 3: `ORGANIZATION` $\rightarrow$ `Công ty Sao Bắc`
    - Card 4: `TRẠNG THÁI` $\rightarrow$ `● ĐANG HOẠT ĐỘNG`
    - Card 5: `VAI TRÒ` $\rightarrow$ `Project Manager`
    - Card 6: `NGÀY THAM GIA` $\rightarrow$ `12/05/2025`
* **Drawer Footer (Fixed Bottom, Height 72px, Border top 1px #E2E8F0, Padding 16px 24px)**:
  - Trái: Nút `Đóng` (Secondary Button).
  - Phải: Nút `Chỉnh sửa hồ sơ` (Primary Button Indigo).

---

### 2.3. Frame 3: `[USER-03] Basic Profile Editing - Modal` (640 × 680 px)
* **Loại Frame**: Centered Modal Dialog (Hộp thoại giữa màn hình).
* **Bố cục Modal**:
  - Bo góc `16px`, Background `#FFFFFF`, Shadow `Elevation 5` (`box-shadow: 0 20px 40px rgba(0,0,0,0.15)`).
  - Header: `Chỉnh sửa thông tin thành viên` + Nút `✕`.
  - Section 1: Avatar Upload (Avatar 72px + nút `Tải ảnh mới` + nút `Xóa ảnh`).
  - Section 2: Form Controls (Vertical Auto Layout `gap: 16px`):
    - Input `Họ và tên *`: Value `Minh Anh`.
    - Input `Email tổ chức (Định danh)`: Value `minh.anh@example.test`, trạng thái **Disabled** kèm icon ổ khóa `🔒` và ghi chú: *"Email là định danh tài khoản, không thể tự ý thay đổi."*
    - Select `Vai trò tổ chức *`: Dropdown 3 lựa chọn [`ADMIN`, `TEAM_LEADER`, `MEMBER`].
    - Radio Group `Trạng thái hoạt động *`: `(●) Đang hoạt động` / `( ) Tạm ngưng`.
  - Footer: Nút `Hủy bỏ` (Secondary) + Nút `Lưu thay đổi` (Primary Indigo).

---

## 3. Thiết Lập Prototype Nối Dây Tương Tác (Figma Prototype Flows)

1. **Từ Bảng Directory sang Drawer (`USER-01 ➔ USER-02`)**:
   - Chọn hàng thứ nhất (`Minh Anh`) trong bảng `USER-01`.
   - Kéo dây tương tác sang Frame `USER-02 Profile Detail Drawer`.
   - **Trigger**: `On click`.
   - **Action**: `Open overlay`.
   - **Overlay position**: `Top right`.
   - **Animation**: `Move in` từ phải sang trái (`Right ➔ Left`), Duration `300ms`, Easing `Ease out`.
   - **Checkbox**: Tick chọn `Close when clicking outside` và `Add background overlay (30% Black)`.

2. **Từ Drawer sang Modal Chỉnh Sửa (`USER-02 ➔ USER-03`)**:
   - Chọn nút `Chỉnh sửa hồ sơ` trong Footer của Drawer `USER-02`.
   - Kéo dây tương tác sang Frame `USER-03 Profile Edit Modal`.
   - **Trigger**: `On click`.
   - **Action**: `Open overlay`.
   - **Overlay position**: `Centered`.
   - **Animation**: `Dissolve` hoặc `Smart Animate`, Duration `200ms`.
   - **Checkbox**: Tick chọn `Close when clicking outside`.

3. **Từ Modal Hoàn Tất Trở Lại (`USER-03 ➔ USER-01`)**:
   - Nút `Lưu thay đổi` $\rightarrow$ `Close overlay` + Hiển thị Toast thông báo thành công.

---

## 4. Checklist Kiểm Định Trước Khi Handoff

- [x] Frame chuẩn desktop **1440px**, tuân thủ 12-column grid.
- [x] Tất cả các component dùng Auto Layout (Horizontal / Vertical), không dùng absolute position tùy tiện.
- [x] Phân định chuẩn xác 3 Persistent Roles: `ADMIN`, `TEAM_LEADER`, `MEMBER`.
- [x] Email ở chế độ read-only trong form cơ bản để bảo mật định danh.
- [x] Dữ liệu mẫu (Dummy data) là dữ liệu doanh nghiệp thực tế, không dùng lorem ipsum.
- [x] Dây nối prototype mượt mà, hỗ trợ đóng bằng phím `Esc` và click backdrop.
