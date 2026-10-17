# [SPEC] DATN-353 — Basic User Profile Editing (Chỉnh Sửa Hồ Sơ Cơ Bản)

> **Mã Jira**: `DATN-353`  
> **Tên task**: `Figma USER-03: Research and design basic user profile editing`  
> **Assignee**: Nguyễn Hồng Phúc  
> **Độ phân giải chuẩn**: Desktop 1440px (Modal Dialog 640px hoặc Drawer Mode)  
> **Ngôn ngữ**: Song ngữ Việt - Anh (VI / EN)

---

## 1. Mục Tiêu & Bối Cảnh Nghiệp Vụ

Task **`DATN-353`** thiết kế luồng và form cập nhật thông tin người dùng. Trọng tâm cốt lõi của task này là **phân định quyền hạn rõ rệt** giữa hai chế độ thao tác:

1. **Chế độ Tự Cập Nhật (Self-Service Profile Edit)**: Người dùng tự cập nhật thông tin cá nhân của chính mình.
2. **Chế độ Quản Trị Viên (Admin Management Edit)**: Quản trị viên cập nhật vai trò, trạng thái hoặc cấp quyền của thành viên trong tổ chức.

---

## 2. Ma Trận Quyền Hạn Chỉnh Sửa (Field-Level Permissions Matrix)

| Trường thông tin | Người Dùng Tự Sửa (Self) | Quản Trị Viên (Admin) | Ràng buộc bảo mật (Security Rules) |
| :--- | :---: | :---: | :--- |
| **Ảnh đại diện (`avatarUrl`)** | Có | Có | Tải ảnh JPEG/PNG tối đa 2MB; tự động crop tròn. |
| **Họ và tên (`fullName`)** | Có | Có | Bắt buộc; độ dài từ 2 đến 100 ký tự. |
| **Email (`email`)** | **Không** | **Không** | Là Primary Identifier trong MongoDB `users`. Tuyệt đối không cho sửa tự do trong form cơ bản. Phải qua quy trình đổi email có xác minh mã OTP. |
| **Vai trò (`roleCode`)** | **Không (Disabled)** | **Có** | Chỉ Admin mới được chọn giữa 3 role: `ADMIN`, `TEAM_LEADER`, `MEMBER`. |
| **Trạng thái (`status`)** | **Không (Disabled)** | **Có** | Chỉ Admin mới được chuyển đổi giữa `ACTIVE` và `SUSPENDED`. |
| **Quyền tạo dự án (`grant`)** | **Không (Disabled)** | **Có** | Chỉ Admin mới được cấp/thu hồi capability `project.create` cho `TEAM_LEADER`. |

---

## 3. Bố Cục Form Chỉnh Sửa (Modal Dialog 640px)

```text
┌──────────────────────────────────────────────────────────────────┐
│ [Tiêu đề: Chỉnh sửa thông tin thành viên]                [✕ Đóng]│
│ Mô tả: Cập nhật thông tin định danh và phân quyền trong tổ chức  │
├──────────────────────────────────────────────────────────────────┤
│ ┌─ KHU VỰC 1: ẢNH ĐẠI DIỆN (Avatar Section) ───────────────────┐ │
│ │ (Avatar Preview 80px)  [Tải ảnh mới ⬆]  [Xóa ảnh 🗑]          │ │
│ │                        Hỗ trợ PNG, JPG, WebP tối đa 2MB       │ │
│ └──────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌─ KHU VỰC 2: THÔNG TIN ĐỊNH DANH (Identity Details) ──────────┐ │
│ │ Họ và tên *                                                  │ │
│ │ [Nguyễn Hồng Phúc                                          ] │ │
│ │                                                              │ │
│ │ Email tổ chức (Không thể sửa) 🛈                              │ │
│ │ [phuc2348hong@gmail.com                        ] [🔒 Đã khóa]│ │
│ │ (Email là định danh tài khoản, liên hệ bộ phận IT để thay đổi)│ │
│ └──────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌─ KHU VỰC 3: QUẢN TRỊ & PHÂN QUYỀN (Admin Only Section) ──────┐ │
│ │ Vai trò tổ chức *                                            │ │
│ │ [ADMIN - Quản trị viên toàn tổ chức                        ▾] │ │
│ │                                                              │ │
│ │ Trạng thái hoạt động *                                       │ │
│ │ (●) Đang hoạt động (ACTIVE)     ( ) Tạm khóa (SUSPENDED)     │ │
│ └──────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────┤
│ Footer: [Hủy bỏ]                          [Lưu thay đổi (Loading)]│
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Quy Tắc Kiểm Hợp Lệ & Thông Báo Lỗi (Validation Rules)

Sử dụng chuẩn kiểm tra dữ liệu Frontend (tương thích thư viện `Zod` / `React Hook Form`):

```typescript
import { z } from 'zod';

export const userProfileEditSchema = z.object({
  fullName: z
    .string()
    .min(2, 'Họ và tên phải có ít nhất 2 ký tự')
    .max(100, 'Họ và tên không được vượt quá 100 ký tự')
    .trim(),
  avatarUrl: z
    .string()
    .url('Đường dẫn ảnh đại diện không hợp lệ')
    .optional()
    .or(z.literal('')),
  roleCode: z.enum(['ADMIN', 'TEAM_LEADER', 'MEMBER'], {
    errorMap: () => ({ message: 'Vui lòng chọn vai trò hợp lệ' }),
  }),
  status: z.enum(['ACTIVE', 'SUSPENDED']),
});
```

### Các trạng thái phản hồi của Form:
1. **Trạng thái Mặc định (Default)**: Hiển thị đúng dữ liệu hiện tại của user. Nút `Lưu thay đổi` bị mờ (`disabled`) cho đến khi người dùng có ít nhất một thay đổi so với ban đầu (`isDirty === true`).
2. **Trạng thái Đang lưu (`Saving / Submitting`)**: Nút `Lưu thay đổi` hiển thị Spinner xoay tròn + chữ *"Đang lưu..."*, tất cả các ô input bị khóa để chống bấm lặp (double submit).
3. **Trạng thái Thành công (`Success Toast`)**: Modal đóng lại, hiển thị Toast thông báo màu xanh lá: *"Cập nhật thông tin thành viên thành công"*, bảng danh bạ tự động cập nhật dữ liệu mới.
4. **Trạng thái Lỗi từng trường (`Field-level Error`)**: Viền ô input đổi sang màu đỏ + Dòng chữ đỏ bên dưới mô tả lỗi chính xác.
5. **Trạng thái Lỗi máy chủ (`Server Error Alert`)**: Xuất hiện Banner đỏ ở đầu form: *"Không thể lưu thay đổi. Vui lòng kiểm tra lại kết nối hoặc thử lại sau."*

---

## 5. Các Ràng Buộc An Toàn Quản Trị (Admin Guard Rails)

Đây là điểm ăn điểm rất lớn trong đồ án tốt nghiệp khi thể hiện tư duy phần mềm doanh nghiệp:

1. **Quy tắc Chống Tổ Chức Vô Chủ (Sole Admin Protection Rule)**:
   - Nếu user được chỉnh sửa đang là **ADMIN duy nhất còn hoạt động** của tổ chức:
   - Hệ thống **khóa chức năng hạ quyền** (Dropdown chọn vai trò bị disabled) kèm thông báo cảnh báo:  
     `⚠️ Không thể thay đổi vai trò hoặc khóa tài khoản của Quản trị viên duy nhất trong tổ chức. Hãy chỉ định một Admin khác trước.`
2. **Hộp Thoại Xác Nhận Thao Tác Nguy Hiểm (Confirmation Dialog)**:
   - Khi Admin đổi trạng thái sang `SUSPENDED` (Tạm khóa):
   - Bắt buộc bật Modal xác nhận:  
     *"Bạn có chắc chắn muốn tạm khóa tài khoản của Nguyễn Hồng Phúc? Người dùng này sẽ bị ngắt phiên đăng nhập ngay lập tức và không thể truy cập bất kỳ dự án nào."*  
     Nút bấm: `[Hủy]` vs `[Xác nhận tạm khóa (Màu Đỏ)]`.

---

## 6. Ghi Chú Handoff Kỹ Thuật (API Gaps)

* **Endpoints Frontend gọi**:
  - `PATCH /api/v1/users/:userId`: Cập nhật `fullName`, `avatarUrl`.
  - `PUT /api/v1/organizations/:orgId/members/:userId/role`: Cập nhật vai trò tổ chức (Yêu cầu quyền Admin).
  - `PUT /api/v1/organizations/:orgId/members/:userId/status`: Cập nhật trạng thái `ACTIVE` / `SUSPENDED`.
* **API Gap Annotation**:
  - Hiện tại Gateway chưa có endpoint gộp chung (Atomic Multi-resource update); do đó Frontend có thể cần gọi tuần tự hoặc Backend sẽ bổ sung endpoint hợp nhất trong Sprint tới.
