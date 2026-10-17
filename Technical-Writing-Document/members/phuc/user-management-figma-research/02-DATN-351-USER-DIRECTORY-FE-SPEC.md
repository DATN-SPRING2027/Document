# [SPEC] DATN-351 — User Directory (Danh Bạ Người Dùng)

> **Mã Jira**: `DATN-351`  
> **Tên task**: `Figma USER-01: Research and design user directory`  
> **Assignee**: Nguyễn Hồng Phúc  
> **Độ phân giải chuẩn**: Desktop 1440px (Responsive Tablet 1024px / Mobile 375px)  
> **Ngôn ngữ**: Song ngữ Việt - Anh (VI / EN)

---

## 1. Mục Tiêu & Bối Cảnh Nghiệp Vụ

Màn hình **User Directory (Danh bạ người dùng)** là trung tâm quản trị nhân sự cấp Tổ chức (`Organization Context`) trong nền tảng SaaS Continuum AI. Màn hình phục vụ 3 nhóm đối tượng:
1. **Admin**: Xem toàn bộ danh sách, lọc theo trạng thái/vai trò, mời thành viên mới, phân quyền và khóa/mở khóa tài khoản.
2. **Team Leader / PM**: Tra cứu thông tin chuyên môn, kiểm tra nhân sự thuộc dự án nào để giao việc hoặc đề xuất quyền `project.create`.
3. **Member**: Tra cứu danh bạ nội bộ, tìm kiếm email, avatar và chức danh của đồng nghiệp trong cùng tổ chức.

---

## 2. Bố Cục Giao Diện Desktop 1440px (Layout Hierarchy)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Header: [Logo Continuum AI] [Org Selector: Acme Corp ▾]       [User Avatar] │
├─────────────────────────────────────────────────────────────────────────────┤
│ Breadcrumb: Trang chủ / Tổ chức / Danh bạ người dùng                        │
│                                                                             │
│ [TIÊU ĐỀ: Thành viên & Người dùng] (Tổng số: 48 thành viên)                 │
│ Mô tả: Quản lý danh bạ thành viên, vai trò hệ thống và phân quyền tổ chức   │
│                                           [+ Mời thành viên mới (Admin)]    │
├─────────────────────────────────────────────────────────────────────────────┤
│ ┌─ Thanh Công Cụ & Bộ Lọc (Toolbar) ──────────────────────────────────────┐ │
│ │ [🔍 Tìm theo họ tên, email...     ] [Vai trò: Tất cả ▾] [Trạng thái: ▾] │ │
│ │ [Dự án: Tất cả ▾]                    [Làm mới ↻] [Chế độ: ▦ Lưới | ☰ Bảng]│ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
│ ┌─ Bảng Dữ Liệu Thành Viên (Data Table View) ─────────────────────────────┐ │
│ │ [ ] THÀNH VIÊN        VAI TRÒ       TRẠNG THÁI     DỰ ÁN      ĐĂNG NHẬP │ │
│ │ ─────────────────────────────────────────────────────────────────────── │ │
│ │ [ ] Nguyễn Hồng Phúc  [ADMIN]       ● Hoạt động    4 dự án    2 giờ trước│ │
│ │     phuc2348@...                                              [••• Xem] │ │
│ │ [ ] Trần Kim Thắng    [TEAM_LEADER] ● Hoạt động    2 dự án    1 ngày tr.│ │
│ │     thangtk@...       + Grant                                 [••• Xem] │ │
│ │ [ ] Đỗ Tuấn Anh       [MEMBER]      ● Chờ kích hoạt 1 dự án    Chưa      │ │
│ │     anhdt@...                       (Pending)                 [••• Xem] │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│ Hiển thị 1 - 10 trên 48 thành viên                   [< Trước] [1] 2 3 [Sau >]│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Cấu Trúc Các Cột Dữ Liệu (Table Schema)

| Cột | Dữ liệu hiển thị | Logic nghiệp vụ & Tương tác |
| :--- | :--- | :--- |
| **Thành viên (User Info)** | • Avatar (40x40px, bo tròn)<br>• Họ và tên (Font Medium, màu đậm)<br>• Email (Font Regular, màu nhạt) | Click vào dòng hoặc tên sẽ kích hoạt **Slide-over Drawer (`DATN-352`)** để xem chi tiết ngay lập tức. |
| **Vai trò (Role)** | • `ADMIN`: Badge Tím (Indigo/Violet)<br>• `TEAM_LEADER`: Badge Xanh dương (Blue)<br>• `MEMBER`: Badge Xám (Slate) | • Nếu là Team Leader có cấp quyền `project.create`, hiển thị thêm icon chìa khóa nhỏ kèm tooltip: *"Được cấp quyền tạo dự án"*.<br>• Phân định rõ ràng: Không hiển thị chức danh nội bộ ngoài 3 role chuẩn. |
| **Trạng thái (Status)** | • `ACTIVE`: Chấm xanh lá + "Đang hoạt động"<br>• `PENDING_INVITE`: Chấm vàng hổ phách + "Chờ xác nhận"<br>• `SUSPENDED`: Chấm đỏ/xám + "Bị tạm dừng" | Trạng thái lấy trực tiếp từ thuộc tính `status` trong `IUser`. |
| **Dự án (Projects)** | Hiển thị số lượng dự án (VD: *3 dự án*). Hover vào hiển thị Popover danh sách tên mã dự án (VD: *CONT, PAY, CORE*). | Dữ liệu tổng hợp từ `project_memberships`. |
| **Đăng nhập cuối (Last Active)** | Thời gian tương đối (VD: *10 phút trước*, *Hôm qua*). Nếu chưa đăng nhập lần nào hiển thị: *Chưa đăng nhập*. | Dữ liệu từ `lastLoginAt`. |
| **Thao tác (Actions)** | Nút ba chấm `•••` mở Menu ngữ cảnh: <br>• Xem hồ sơ (`DATN-352`)<br>• Chỉnh sửa quyền (`DATN-353`) *(Chỉ Admin)*<br>• Gửi lại lời mời *(Chỉ với `PENDING_INVITE`)*<br>• Khóa tài khoản *(Chỉ Admin)* | Ẩn các thao tác quản trị nếu người đăng nhập hiện tại chỉ là `MEMBER`. |

---

## 4. Xử Lý Các Trạng Thái Biên (Edge States)

Một thiết kế Hi-Fi chuẩn đồ án bắt buộc phải thể hiện đầy đủ 4 trạng thái giao diện:

1. **Trạng thái Tải dữ liệu (`Loading State - Skeleton Loader`)**:
   - Hiển thị 5 hàng Skeleton xám nhấp nháy (shimmer animation) giả lập avatar, 2 dòng chữ, badge và ngày tháng.
   - Tránh dùng spinner quay đơn điệu ở giữa trang gây giật layout.
2. **Trạng thái Không tìm thấy kết quả (`Empty Filter State`)**:
   - Xuất hiện khi người dùng gõ từ khóa tìm kiếm hoặc lọc không có kết quả phù hợp.
   - Hình minh họa vector nhẹ nhàng + Tiêu đề: *"Không tìm thấy thành viên nào"* + Gợi ý: *"Thử kiểm tra lại từ khóa hoặc xóa bớt bộ lọc"* + Nút bấm: *"Xóa tất cả bộ lọc"*.
3. **Trạng thái Chưa có dữ liệu (`Empty Initial State`)**:
   - Khi tổ chức mới tạo chưa mời ai.
   - Tiêu đề: *"Chưa có thành viên nào trong tổ chức"* + Nút bấm nổi bật: *"Mời thành viên đầu tiên"*.
4. **Trạng thái Bị từ chối quyền truy cập (`Permission Denied 403`)**:
   - Hiển thị khi một user bên ngoài cố truy cập URL danh bạ của tổ chức khác mà không có `OrganizationMembership`.
   - Banner cảnh báo: *"Bạn không có quyền truy cập danh bạ tổ chức này. Vui lòng liên hệ Quản trị viên để được cấp quyền."*

---

## 5. TypeScript Interfaces Khớp Database Backend

```typescript
// Định nghĩa khớp schema continuum_iam (01_SVC_IAM_SCHEMA.md)
export type UserStatus = 'ACTIVE' | 'SUSPENDED' | 'PENDING_INVITE';
export type PersistentRole = 'ADMIN' | 'TEAM_LEADER' | 'MEMBER';

export interface IUserDirectoryItem {
  _id: string;
  fullName: string;
  email: string;
  avatarUrl?: string;
  status: UserStatus;
  twoFactorEnabled: boolean;
  roleCode: PersistentRole;
  roleName: string;
  hasProjectCreateCapability?: boolean;
  projectCount: number;
  projectCodes: string[];
  lastLoginAt?: string;
  createdAt: string;
}

export interface IUserDirectoryFilters {
  searchTerm: string;
  role?: PersistentRole | 'ALL';
  status?: UserStatus | 'ALL';
  projectId?: string | 'ALL';
  page: number;
  pageSize: number;
}
```

---

## 6. Dữ Liệu Giả Lập Mẫu (Mock Dataset Hoàn Chỉnh)

```json
[
  {
    "_id": "usr_001",
    "fullName": "Nguyễn Hồng Phúc",
    "email": "phuc2348hong@gmail.com",
    "avatarUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
    "status": "ACTIVE",
    "twoFactorEnabled": true,
    "roleCode": "ADMIN",
    "roleName": "Quản trị viên tổ chức",
    "hasProjectCreateCapability": true,
    "projectCount": 4,
    "projectCodes": ["CONT", "IAM", "CORE", "WORK"],
    "lastLoginAt": "2026-10-17T06:30:00Z",
    "createdAt": "2026-09-01T08:00:00Z"
  },
  {
    "_id": "usr_002",
    "fullName": "Trần Kim Thắng",
    "email": "thangtk@continuum.vn",
    "avatarUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150",
    "status": "ACTIVE",
    "twoFactorEnabled": true,
    "roleCode": "TEAM_LEADER",
    "roleName": "Trưởng nhóm kỹ thuật",
    "hasProjectCreateCapability": true,
    "projectCount": 2,
    "projectCodes": ["CONT", "PAYMENT"],
    "lastLoginAt": "2026-10-16T15:45:00Z",
    "createdAt": "2026-09-05T09:15:00Z"
  },
  {
    "_id": "usr_003",
    "fullName": "Đỗ Tuấn Anh",
    "email": "anhdt@continuum.vn",
    "avatarUrl": "",
    "status": "PENDING_INVITE",
    "twoFactorEnabled": false,
    "roleCode": "MEMBER",
    "roleName": "Kỹ sư phần mềm",
    "hasProjectCreateCapability": false,
    "projectCount": 1,
    "projectCodes": ["CONT"],
    "lastLoginAt": null,
    "createdAt": "2026-10-15T11:20:00Z"
  },
  {
    "_id": "usr_004",
    "fullName": "Lê Thị Mai",
    "email": "mailt@continuum.vn",
    "avatarUrl": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150",
    "status": "SUSPENDED",
    "twoFactorEnabled": false,
    "roleCode": "MEMBER",
    "roleName": "Kỹ sư phần mềm",
    "hasProjectCreateCapability": false,
    "projectCount": 0,
    "projectCodes": [],
    "lastLoginAt": "2026-09-20T04:12:00Z",
    "createdAt": "2026-09-10T10:00:00Z"
  }
]
```

---

## 7. Ghi Chú Handoff Kỹ Thuật (Frontend & API Gaps)

* **Endpoint dự kiến**:
  - `GET /api/v1/organizations/:orgId/members`: Đọc danh sách có phân trang và bộ lọc `query: { page, limit, search, role, status }`.
  - `POST /api/v1/organizations/:orgId/members/invite`: Gửi email mời thành viên mới.
  - `POST /api/v1/organizations/:orgId/members/:userId/resend-invite`: Gửi lại thư kích hoạt cho thành viên `PENDING_INVITE`.
* **API Gap Annotation**:
  - Hiện tại Gateway chưa mở rộng toàn bộ bộ lọc đa dự án; frontend prototype dùng client-side filtering trên mock dataset để trải nghiệm người dùng mượt mà nhất.
