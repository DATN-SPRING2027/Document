# [SPEC] DATN-352 — User Profile Detail (Chi Tiết Hồ Sơ Người Dùng)

> **Mã Jira**: `DATN-352`  
> **Tên task**: `Figma USER-02: Research and design user profile detail`  
> **Assignee**: Nguyễn Hồng Phúc  
> **Độ phân giải chuẩn**: Desktop 1440px (Slide-over Drawer width: 560px)  
> **Ngôn ngữ**: Song ngữ Việt - Anh (VI / EN)

---

## 1. Mục Tiêu & Bối Cảnh Nghiệp Vụ

Giao diện **Chi Tiết Hồ Sơ Người Dùng (User Profile Detail)** trong hệ thống Continuum AI không đơn thuần chỉ là một trang lý lịch cá nhân, mà là một **bảng tổng hợp 360 độ về quyền hạn, dự án và đóng góp tri thức** của nhân sự trong doanh nghiệp.

### Phân Định Trách Nhiệm Quan Trọng:
* **Hồ sơ thành viên trong Directory (User Profile - Task này)**: Là góc nhìn quản trị/đồng nghiệp khi xem thông tin của một người trong tổ chức. Chứa các trường nghiệp vụ: Vai trò, Dự án tham gia, Quyền tạo dự án, Gán chuyên gia SME.
* **Cài đặt cá nhân (Personal Account Settings - Scope riêng)**: Là nơi người dùng tự đổi mật khẩu, cấu hình app, đổi theme. **Không nhầm lẫn hai phạm vi này.**

---

## 2. Bố Cục Slide-over Drawer (Width: 560px)

```text
┌────────────────────────────────────────────────────────┐
│ [✕ Đóng (Esc)]               [Mở toàn trang ↗] [••• Sửa]│
├────────────────────────────────────────────────────────┤
│ ┌─ HEADER DANH TÍNH (Profile Identity) ──────────────┐ │
│ │  (Avatar 72px)  Nguyễn Hồng Phúc                   │ │
│ │  [Chấm Xanh]    phuc2348hong@gmail.com             │ │
│ │                 [ADMIN]  [2FA Đã kích hoạt ✓]      │ │
│ └────────────────────────────────────────────────────┘ │
│                                                        │
│ [Trạng thái: Đang hoạt động] • Tham gia: 01/09/2026    │
├────────────────────────────────────────────────────────┤
│ ┌─ 4 TABS ĐIỀU HƯỚNG ────────────────────────────────┐ │
│ │ [Tổng quan]  [Vai trò & Quyền]  [Dự án]  [Hoạt động] │ │
│ └────────────────────────────────────────────────────┘ │
│                                                        │
│ [NỘI DUNG THEO TAB ĐANG CHỌN]                          │
│                                                        │
│ (Chi tiết từng tab được đặc tả ở Mục 3)                │
│                                                        │
├────────────────────────────────────────────────────────┤
│ Footer Drawer: [Chỉnh sửa hồ sơ (Admin)]   [Đóng]     │
└────────────────────────────────────────────────────────┘
```

---

## 3. Đặc Tả Chi Tiết 4 Phân Khu Tab Nghiệp Vụ

### Tab 1: Tổng Quan (Overview)
* **Thông tin liên hệ & hệ thống**:
  - Email tổ chức: `phuc2348hong@gmail.com`
  - Mã người dùng (`User ID`): `usr_001` (hỗ trợ nút sao chép nhanh)
  - Ngày khởi tạo tài khoản (`createdAt`): `01/09/2026`
  - Đăng nhập gần nhất (`lastLoginAt`): `17/10/2026, 13:30 (2 giờ trước)`
  - Trạng thái bảo mật 2FA (`twoFactorEnabled`): Badge xanh lá *"Đã bật xác thực 2 lớp"*
* **Thống kê nhanh (Quick Stats Grid)**:
  - Dự án tham gia: **4**
  - Ghi chú công việc (Notes): **142**
  - Tri thức đóng góp: **28**

### Tab 2: Vai Trò & Quyền Hạn (Roles & Governance)
Tuân thủ chính xác tài liệu [02_ACTORS_ROLES_AND_PERMISSIONS.md](file:///f:/%C4%90%E1%BB%93-%C3%81n-T%E1%BB%91t-Nghi%E1%BB%87p/Document/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md):
* **Persistent Human Role**:
  - Hiển thị badge: `ADMIN` | `TEAM_LEADER` | `MEMBER`.
  - Giải thích phạm vi quyền hạn theo role tương ứng.
* **Cấp quyền năng lực đặc biệt (`organization_capability_grants`)**:
  - Nếu là `TEAM_LEADER` và có quyền tạo dự án:
    - Huy hiệu: `project.create` (Màu hổ phách Amber)
    - Người cấp: `Admin (admin@continuum.vn)`
    - Lý do cấp: *"Phụ trách khởi tạo dự án thanh toán Payment Gateway V2"*
    - Thời hạn: *Hết hạn vào 31/12/2026*
* **Vai trò chuyên môn lâm thời (Scoped Assignments)**:
  - Nếu được gán vai trò chuyên môn:
    - `SME` (Subject Matter Expert): Phạm vi `IAM & Security Domain` (Đến hết Q4/2026)
    - `KNOWLEDGE_OWNER`: Phụ trách tài liệu `01_SVC_IAM_SCHEMA.md`

### Tab 3: Dự Án & Nhóm Trực Thuộc (Projects & Teams)
* Danh sách card các dự án mà user là thành viên (đọc từ `project_memberships`):
  - **Continuum AI Baseline** (`CONT`) — Vai trò: Project Creator & Lead
  - **Payment Gateway V2** (`PAYMENT`) — Vai trò: Contributor
  - **Internal Work Core** (`WORK`) — Vai trò: Reviewer
* Kèm nhãn Team trực thuộc: `#backend-core`, `#secops`.

### Tab 4: Dấu Ấn Hoạt Động (Activity Footprint)
* Dòng thời gian (Timeline) thể hiện các tương tác công việc gần nhất:
  - *16/10/2026*: Đã tạo ghi chú What/How/Why cho task `DATN-90 Team Foundation BE`.
  - *15/10/2026*: Đã bàn giao gói tài liệu `DATN-87` cho đội Frontend.
  - *11/10/2026*: Đã duyệt đề xuất tri thức trong module Governance.

---

## 4. Xử Lý Các Trạng Thái Biên (Edge Cases)

1. **Tài khoản đang bị Khóa (`SUSPENDED`)**:
   - Xuất hiện Banner cảnh báo màu đỏ ở đầu Drawer:  
     `⚠️ Tài khoản này hiện đang bị tạm khóa quyền truy cập tổ chức. Người dùng không thể đăng nhập hoặc thao tác tài nguyên.`
   - Nút hành động đổi thành: `[Mở khóa tài khoản]` *(Chỉ Admin)*.
2. **Tài khoản đang Chờ Kích Hoạt (`PENDING_INVITE`)**:
   - Banner màu vàng cảnh báo:  
     `✉️ Lời mời tham gia đã được gửi tới email nhưng người dùng chưa kích hoạt mật khẩu.`
   - Nút hành động: `[Gửi lại email kích hoạt]` và `[Hủy lời mời]`.
3. **Thành viên không có Dự án nào (`projectCount === 0`)**:
   - Tab Dự án hiển thị Empty State: *"Thành viên này chưa được gán vào dự án nào"* + Nút `[Thêm vào dự án]`.

---

## 5. TypeScript Interfaces Khớp Contract Chi Tiết

```typescript
export interface IUserProfileDetail {
  _id: string;
  fullName: string;
  email: string;
  avatarUrl?: string;
  status: 'ACTIVE' | 'SUSPENDED' | 'PENDING_INVITE';
  twoFactorEnabled: boolean;
  createdAt: string;
  lastLoginAt?: string;
  
  // Governance & Permissions
  role: {
    code: 'ADMIN' | 'TEAM_LEADER' | 'MEMBER';
    name: string;
    assignedAt: string;
    assignedBy: string;
  };
  
  capabilityGrants: Array<{
    capability: 'project.create';
    grantedBy: string;
    reason: string;
    expiresAt?: string;
  }>;

  scopedAssignments: Array<{
    type: 'SME' | 'KNOWLEDGE_OWNER' | 'SUCCESSOR';
    scopeName: string;
    validUntil?: string;
  }>;

  // Projects & Teams
  projects: Array<{
    projectId: string;
    projectCode: string;
    projectName: string;
    roleInProject: string;
    joinedAt: string;
    teams: string[];
  }>;
}
```

---

## 6. Ghi Chú Handoff Kỹ Thuật (Handoff Notes)

* **Tương tác bàn giao**:
  - Hỗ trợ phím tắt: Bấm phím `Escape` tự động đóng Drawer.
  - Click vào overlay bên ngoài (Backdrop) có hiệu ứng mờ nhẹ `bg-black/30 backdrop-blur-sm`, click ra ngoài đóng drawer.
  - Hỗ trợ nút `Mở toàn trang`: Mở URL `/app/organization/members/:id` nếu người dùng muốn làm việc ở màn hình lớn độc lập.
