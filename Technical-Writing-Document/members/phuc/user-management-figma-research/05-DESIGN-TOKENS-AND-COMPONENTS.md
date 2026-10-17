# [DESIGN SYSTEM] Tokens, Components & Từ Điển Song Ngữ (i18n)

> **Tài liệu phục vụ**: `DATN-351`, `DATN-352`, `DATN-353`  
> **Tác giả / Assignee**: Nguyễn Hồng Phúc  
> **Chuẩn Design Foundations**: Module 00 Figma Continuum AI

---

## 1. Hệ Thống Màu Sắc & Tokens (Color Tokens)

### 1.1. Bảng Màu Vai Trò Hệ Thống (Persistent Roles)

| Role Code | Tên Hiển Thị | Màu Nền (Background) | Màu Chữ (Text) | Viền (Border) |
| :--- | :--- | :--- | :--- | :--- |
| **`ADMIN`** | Quản trị viên | `bg-indigo-50` / dark: `bg-indigo-950/40` | `text-indigo-700` / dark: `text-indigo-300` | `border-indigo-200` / dark: `border-indigo-800` |
| **`TEAM_LEADER`** | Trưởng nhóm | `bg-blue-50` / dark: `bg-blue-950/40` | `text-blue-700` / dark: `text-blue-300` | `border-blue-200` / dark: `border-blue-800` |
| **`MEMBER`** | Thành viên | `bg-slate-100` / dark: `bg-slate-800` | `text-slate-700` / dark: `text-slate-300` | `border-slate-200` / dark: `border-slate-700` |

### 1.2. Bảng Màu Trạng Thái Tài Khoản (User Status)

| Status Code | Ý nghĩa | Chấm Đèn (Dot Indicator) | Huy Hiệu (Badge) |
| :--- | :--- | :--- | :--- |
| **`ACTIVE`** | Đang hoạt động | `bg-emerald-500` (Xanh lá) | `bg-emerald-50 text-emerald-700 border-emerald-200` |
| **`PENDING_INVITE`** | Chờ kích hoạt | `bg-amber-500` (Hổ phách) | `bg-amber-50 text-amber-700 border-amber-200` |
| **`SUSPENDED`** | Đã tạm khóa | `bg-rose-500` (Đỏ hồng) | `bg-rose-50 text-rose-700 border-rose-200` |

---

## 2. Thư Viện Biểu Tượng (Lucide Iconography)

Sử dụng bộ icon chuẩn **Lucide React** đồng bộ trong toàn bộ ứng dụng:

```typescript
import {
  Users,           // Biểu tượng Menu Danh bạ
  UserCheck,       // Trạng thái Active / Duyệt thành viên
  UserX,           // Khóa tài khoản Suspended
  Mail,            // Email liên hệ
  Shield,          // Vai trò bảo mật Admin
  KeyRound,        // Quyền project.create
  FolderGit2,      // Dự án trực thuộc
  Clock,           // Lần đăng nhập cuối
  Search,          // Ô tìm kiếm
  Filter,          // Bộ lọc
  MoreVertical,    // Nút menu thao tác
  ExternalLink,    // Mở chi tiết toàn trang
  CheckCircle2,    // Thông báo thành công
  AlertTriangle,   // Cảnh báo thao tác
  X,               // Đóng Drawer / Modal
} from 'lucide-react';
```

---

## 3. Từ Điển Song Ngữ Hoàn Chỉnh (`src/i18n.tsx`)

Bạn có thể sao chép trực tiếp khối từ điển này vào file `src/i18n.tsx` của prototype Figma Make để hỗ trợ nút gạt chuyển đổi ngôn ngữ **VI / EN**:

```typescript
export const userTranslations = {
  vi: {
    // Header & Navigation
    'user.directory.title': 'Danh bạ thành viên',
    'user.directory.subtitle': 'Quản lý nhân sự, vai trò hệ thống và trạng thái hoạt động trong tổ chức.',
    'user.directory.invite_btn': 'Mời thành viên mới',
    'user.directory.total_members': '{{count}} thành viên',

    // Filters & Search
    'user.filter.search_placeholder': 'Tìm theo họ tên, email...',
    'user.filter.all_roles': 'Tất cả vai trò',
    'user.filter.all_statuses': 'Tất cả trạng thái',
    'user.filter.all_projects': 'Tất cả dự án',
    'user.filter.reset': 'Làm mới',

    // Table Columns
    'user.col.member': 'Thành viên',
    'user.col.role': 'Vai trò',
    'user.col.status': 'Trạng thái',
    'user.col.projects': 'Dự án',
    'user.col.last_login': 'Đăng nhập cuối',
    'user.col.actions': 'Thao tác',

    // Roles & Badges
    'role.admin': 'Quản trị viên',
    'role.team_leader': 'Trưởng nhóm',
    'role.member': 'Thành viên',
    'role.project_create_badge': 'Được tạo dự án',

    // Statuses
    'status.active': 'Đang hoạt động',
    'status.pending_invite': 'Chờ kích hoạt',
    'status.suspended': 'Bị tạm khóa',

    // Profile Drawer
    'profile.drawer.overview': 'Tổng quan',
    'profile.drawer.roles_and_perms': 'Vai trò & Quyền hạn',
    'profile.drawer.projects': 'Dự án & Nhóm',
    'profile.drawer.activity': 'Hoạt động',
    'profile.drawer.edit_btn': 'Chỉnh sửa hồ sơ',
    'profile.drawer.open_full': 'Mở toàn trang',
    'profile.drawer.2fa_enabled': 'Xác thực 2 lớp (2FA) đã bật',
    'profile.drawer.2fa_disabled': 'Chưa bật xác thực 2 lớp',

    // Profile Edit Form
    'profile.edit.title': 'Chỉnh sửa thông tin thành viên',
    'profile.edit.fullname_label': 'Họ và tên',
    'profile.edit.email_label': 'Email tổ chức',
    'profile.edit.email_hint': 'Email là định danh tài khoản, không thể tự ý sửa đổi.',
    'profile.edit.role_label': 'Vai trò trong tổ chức',
    'profile.edit.status_label': 'Trạng thái tài khoản',
    'profile.edit.save_btn': 'Lưu thay đổi',
    'profile.edit.cancel_btn': 'Hủy bỏ',
    'profile.edit.saving': 'Đang lưu...',
    'profile.edit.success': 'Cập nhật thông tin thành viên thành công!',
  },
  en: {
    // Header & Navigation
    'user.directory.title': 'User Directory',
    'user.directory.subtitle': 'Manage members, system roles, and account statuses across the organization.',
    'user.directory.invite_btn': 'Invite Member',
    'user.directory.total_members': '{{count}} members',

    // Filters & Search
    'user.filter.search_placeholder': 'Search by name, email...',
    'user.filter.all_roles': 'All Roles',
    'user.filter.all_statuses': 'All Statuses',
    'user.filter.all_projects': 'All Projects',
    'user.filter.reset': 'Reset',

    // Table Columns
    'user.col.member': 'Member',
    'user.col.role': 'Role',
    'user.col.status': 'Status',
    'user.col.projects': 'Projects',
    'user.col.last_login': 'Last Active',
    'user.col.actions': 'Actions',

    // Roles & Badges
    'role.admin': 'Administrator',
    'role.team_leader': 'Team Leader',
    'role.member': 'Member',
    'role.project_create_badge': 'Project Creator',

    // Statuses
    'status.active': 'Active',
    'status.pending_invite': 'Pending Invite',
    'status.suspended': 'Suspended',

    // Profile Drawer
    'profile.drawer.overview': 'Overview',
    'profile.drawer.roles_and_perms': 'Roles & Permissions',
    'profile.drawer.projects': 'Projects & Teams',
    'profile.drawer.activity': 'Activity',
    'profile.drawer.edit_btn': 'Edit Profile',
    'profile.drawer.open_full': 'Open Full Page',
    'profile.drawer.2fa_enabled': '2FA Enabled',
    'profile.drawer.2fa_disabled': '2FA Disabled',

    // Profile Edit Form
    'profile.edit.title': 'Edit Member Profile',
    'profile.edit.fullname_label': 'Full Name',
    'profile.edit.email_label': 'Work Email',
    'profile.edit.email_hint': 'Work email is a permanent identity and cannot be altered directly.',
    'profile.edit.role_label': 'Organization Role',
    'profile.edit.status_label': 'Account Status',
    'profile.edit.save_btn': 'Save Changes',
    'profile.edit.cancel_btn': 'Cancel',
    'profile.edit.saving': 'Saving...',
    'profile.edit.success': 'Member profile updated successfully!',
  },
};
```
