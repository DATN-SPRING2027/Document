# [RESEARCH] B2B SaaS Benchmarking & Pattern Decisions

> **Tài liệu phục vụ**: `DATN-351`, `DATN-352`, `DATN-353`  
> **Tác giả / Assignee**: Nguyễn Hồng Phúc  
> **Tiêu chuẩn nghiệm thu**: So sánh 2–3 mẫu Enterprise SaaS liên quan; ghi lại nguồn và lý do chọn pattern; không sao chép mẫu TailAdmin.

---

## 1. Tổng Quan Nghiên Cứu Benchmarking

Để xây dựng cụm màn hình quản lý nhân sự (**User Directory**, **Profile Detail**, **Profile Editing**) đạt đẳng cấp doanh nghiệp cho nền tảng B2B SaaS **Continuum AI**, chúng ta tiến hành khảo sát và phân tích ưu/nhược điểm từ 3 hệ thống phần mềm SaaS dẫn đầu thị trường:

1. **Atlassian Administration (Jira / Confluence Cloud Admin)**
2. **GitHub Enterprise (Organization People & Member Governance)**
3. **Linear (Workspace Members & Fast Team Directory)**

---

## 2. Phân Tích Chi Tiết Từng Hệ Thống Tham Chiếu

### 2.1. Atlassian Administration (`admin.atlassian.com`)

* **Điểm mạnh (Strengths)**:
  - **Khả năng quản trị quy mô lớn (High Scalability)**: Bảng dữ liệu hỗ trợ hàng nghìn người dùng với bộ lọc phân cấp (Status: Active / Suspended / Invited; Product Access; Roles).
  - **Nhận diện trạng thái rõ ràng**: Mỗi user có badge trạng thái kèm màu sắc tương phản cao (Active = Green, Suspended = Gray/Red, Invited = Yellow).
  - **Hành động phân quyền an toàn**: Các thao tác nhạy cảm (Đổi vai trò, đình chỉ tài khoản) luôn yêu cầu xác nhận kèm mô tả hậu quả (Impact warning).
* **Điểm yếu (Weaknesses)**:
  - Trải nghiệm mở trang chi tiết người dùng thường chuyển hẳn sang URL mới (`full-page reload`), gây mất mạch làm việc (context loss) khi Admin cần duyệt qua nhiều nhân sự liên tiếp.
  - Giao diện dạng form kiểu truyền thống, mất nhiều bước bấm chuột.

### 2.2. GitHub Enterprise (`github.com/orgs/{org}/people`)

* **Điểm mạnh (Strengths)**:
  - **Faceted Filters & Quick Search**: Tìm kiếm theo Username, Tên thật, Role (`Owner` vs `Member`), 2FA Status (`Enabled` vs `Disabled`).
  - **Phân tách rạch ròi giữa Thành viên chính thức và Khách bên ngoài**: Tách thành 2 tab "Members" và "Outside Collaborators".
  - **Bảo mật rõ ràng**: Cho phép Admin kiểm tra xem thành viên nào chưa bật xác thực hai bước (2FA) để gửi lời nhắc.
* **Điểm yếu (Weaknesses)**:
  - Màn hình thông tin thành viên tập trung nhiều vào Code & Repositories, chưa tối ưu cho mô hình quản trị tri thức và dự án đa phòng ban như Continuum AI.

### 2.3. Linear App (`linear.app`)

* **Điểm mạnh (Strengths)**:
  - **Slide-over Drawer (Side Sheet)**: Khi click vào bất kỳ thành viên nào, một Drawer trượt mượt mà từ cạnh phải ra với phím tắt `Esc` để đóng. Người dùng có thể vừa xem danh bạ vừa tra cứu hồ sơ cá nhân chỉ trong tích tắc.
  - **Micro-interactions & Modern Aesthetics**: Layout tối giản, typography hiện đại, bo góc chuẩn mực, hỗ trợ Dark/Light mode không gian phẳng.
  - **Phân nhóm thông tin thông minh**: Hiển thị ngay người này đang thuộc những Team nào, đang phụ trách những Issue nào và trạng thái trực tuyến.
* **Điểm yếu (Weaknesses)**:
  - Không đi quá sâu vào các lớp phân quyền phức tạp nhiều tầng như cấp Organization - Project - Team của Continuum AI.

---

## 3. Bảng Ma Trận So Sánh Tính Năng (Feature Matrix)

| Tiêu Chí / Pattern | Atlassian Admin | GitHub Enterprise | Linear App | Lựa Chọn Cho Continuum AI |
| :--- | :---: | :---: | :---: | :--- |
| **Bố cục danh bạ** | Table truyền thống | Table danh sách | Table & Grid gọn | **Hybrid Table + Quick Toggle Grid** |
| **Xem chi tiết hồ sơ** | Full-page redirect | Full-page redirect | **Slide-over Drawer** | **Slide-over Drawer (Ưu tiên) + Nút Mở Full Page** |
| **Phân loại vai trò** | Product Roles | Owner / Member | Admin / Member / Guest | **3 Persistent Roles (`ADMIN`, `TEAM_LEADER`, `MEMBER`)** |
| **Trạng thái 2FA** | Báo cáo riêng | Badge trong list | Cài đặt bảo mật | **Hiển thị Badge 2FA trực tiếp trên hồ sơ chi tiết** |
| **Chỉnh sửa hồ sơ** | Form riêng từng tab | Settings Page | Inline / Modal | **Slide Modal có phân tách Self-Service vs Admin** |
| **Ngăn chặn lỗi Admin** | Cảnh báo hệ thống | Chặn xóa Owner cuối | Cảnh báo | **Khóa nút hạ quyền nếu là Admin hoạt động duy nhất** |

---

## 4. Lý Do Lựa Chọn Pattern Cho Continuum AI

### 4.1. Tại sao chọn Slide-over Drawer cho `DATN-352` (Profile Detail)?
1. **Bảo toàn ngữ cảnh (Context Preservation)**: Admin hoặc Team Leader khi tra cứu nhân sự cần rà soát liên tục. Drawer trượt từ phải ra (chiều rộng 560px) cho phép đọc ngay thông tin chi tiết, sau đó nhấn phím `Esc` hoặc click ra ngoài để trở lại danh bạ mà không phải tải lại trang.
2. **Cấu trúc Tabbed Drawer**: Bên trong Drawer chia thành 4 tab: **Tổng quan**, **Vai trò & Quyền hạn**, **Dự án & Nhóm**, **Nhật ký hoạt động**. Cấu trúc này giúp thông tin gọn gàng, không bị cuộn trang quá dài.

### 4.2. Tại sao chọn Faceted Filter + Debounced Search cho `DATN-351`?
- Hệ thống SaaS B2B có thể có từ hàng chục đến hàng trăm nhân sự. Việc lọc tức thời theo:
  - **Role** (`ADMIN` / `TEAM_LEADER` / `MEMBER`)
  - **Trạng thái** (`ACTIVE` / `PENDING_INVITE` / `SUSPENDED`)
  - **Dự án trực thuộc**
  kết hợp ô tìm kiếm gõ tới đâu lọc tới đó (debounce 300ms) giúp giảm 70% thời gian thao tác so với việc phải bấm nút "Tìm kiếm" thủ công.

### 4.3. Sự Khác Biệt Và Cải Tiến So Với Template TailAdmin
Template mã nguồn khởi tạo ban đầu là **TailAdmin** (Next.js). Dưới đây là các điểm cải tiến cốt lõi để nâng tầm giao diện thành sản phẩm thương mại thật:

1. **Không sao chép giao diện cứng (Static Mockup)**:
   - TailAdmin chỉ có các bảng HTML tĩnh với dữ liệu cố định, không có logic trạng thái.
   - Continuum AI xây dựng **State Machine đầy đủ**: Xử lý trạng thái tải (`Loading Skeleton`), trạng thái rỗng (`Empty Filter Result`), lỗi mất mạng/máy chủ (`Error State`), và trạng thái bị từ chối quyền (`Permission Denied 403`).
2. **Tuân thủ đúng kiến trúc bảo mật IAM**:
   - TailAdmin không có khái niệm phân quyền. Giao diện mới áp dụng nghiêm ngặt quy tắc: Người dùng thường không thấy các nút phân quyền/khóa tài khoản; chỉ Admin mới có quyền thao tác quản trị.
3. **Màu sắc và Typography đạt chuẩn Accessibility (WCAG 2.1 AA)**:
   - Sử dụng gam màu Slate/Zinc hiện đại kết hợp màu nhấn Brand Indigo/Violet, loại bỏ các màu sắc nguyên bản lòe loẹt.
   - Tương phản màu chữ trên nền badge đạt tỉ lệ tối thiểu 4.5:1.
