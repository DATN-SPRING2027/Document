# [RESEARCH] B2B SaaS Benchmarking & Authentic Pattern Decisions

> **Tài liệu phục vụ**: `DATN-351` (Figma USER-01: Research and design user directory), `DATN-352`, `DATN-353`  
> **Tác giả / Assignee**: Nguyễn Hồng Phúc  
> **Nguyên tắc cốt lõi**: **KHÔNG tự động generate UI phi thực tế bằng AI**. Toàn bộ giao diện và luồng tương tác đều được đào sâu nghiên cứu, đối chiếu từ các Design System, UI Templates mã nguồn mở và sản phẩm SaaS doanh nghiệp hàng đầu thế giới trên Internet.

---

## 1. Bối Cảnh & Phương Pháp Nghiên Cứu Mẫu (Research Methodology)

Trong phát triển phần mềm doanh nghiệp B2B (Enterprise SaaS), giao diện quản lý nhân sự (**User Directory**, **Member Governance**, **Access Control**) là trung tâm điều hành nhạy cảm về bảo mật và vận hành. Thay vì để AI tự sinh (hallucinate) các giao diện ngẫu nhiên không có chuẩn mực, nhóm thực hiện phương pháp **Nghiên cứu khảo sát sâu trên Internet (Deep-dive Internet Benchmarking)**:

1. **Nhóm Design System & UI Kits thịnh hành**: Untitled UI, Tailwind UI, shadcn/ui (TanStack Table).
2. **Nhóm IAM & Identity Management chuyên nghiệp**: Clerk (`<OrganizationProfile />`), WorkOS Directory Sync.
3. **Nhóm Nền Tảng Độc Lập Có Nghiệp Vụ Quản Trị Tương Tự**: Vercel Team & Project Governance, GitLab Group Members, Supabase Team Access, Stripe Dashboard Team Settings, Notion Workspace Members.

---

## 2. Các Mẫu Tham Chiếu Cốt Lõi Từ Internet

### 2.1. Mẫu 1: Untitled UI — B2B SaaS User Table System
* **Nguồn**: Jordan Hughes (`untitledui.com` & Figma Community `@untitledui`)
* **Đặc trưng cấu trúc**:
  - Ô người dùng tích hợp (Composite User Cell): Avatar tròn 40x40px + Tên in đậm + Email chữ xám bên dưới.
  - Chấm LED trạng thái mềm mại (Soft Tinted Status Pill): Chấm tròn 6px kết hợp nền pastel trong suốt.
  - Thanh phân trang tiêu chuẩn: `Showing 1-10 of 48 results` kèm nút `< Previous` và `Next >`.

### 2.2. Mẫu 2: Tailwind UI — "Tables with Avatars and Multi-line Content"
* **Nguồn**: Tailwind Labs (`tailwindui.com/components/application-ui/tables`)
* **Đặc trưng cấu trúc**:
  - Bố cục danh sách phân dòng tinh gọn (`divide-y divide-gray-200`), loại bỏ viền ngoài nặng nề.
  - Sử dụng Font tabular nums cho ngày tháng và số liệu giúp các con số thẳng hàng hoàn hảo.
  - Phù hợp màn hình mật độ thông tin cao (High Density).

### 2.3. Mẫu 3: shadcn/ui & TanStack Table (`tablecn`)
* **Nguồn**: shadcn (`ui.shadcn.com/docs/components/data-table`) và Sadmann (`github.com/sadmann7/tablecn`)
* **Đặc trưng cấu trúc**:
  - Kiến trúc Headless UI kết hợp Radix UI Primitives: Tối ưu hoàn toàn khả năng tiếp cận (Accessibility WCAG 2.1 AA).
  - Bộ lọc đa chiều dạng popover (Faceted Filter pills: Role, Status).
  - Checkbox chọn nhiều dòng hỗ trợ thanh công cụ nổi (Floating Action Bar).

### 2.4. Mẫu 4: Clerk `<OrganizationProfile />` & WorkOS Directory Sync
* **Nguồn**: Clerk Docs (`clerk.com/docs/components/organization/organization-profile`) & WorkOS (`workos.com`)
* **Đặc trưng cấu trúc**:
  - Tách tab "Thành viên" (Members) và "Lời mời đang chờ" (Pending Invitations).
  - Đổi vai trò trực tiếp qua dropdown với phản hồi tức thì (Optimistic UI).
  - Thao tác nhanh cho lời mời: Gửi lại (Resend) và Hủy (Revoke).

### 2.5. Mẫu 5: Linear App — Workspace Members & Slide-over Drawer
* **Nguồn**: Linear (`linear.app`)
* **Đặc trưng cấu trúc**:
  - **Slide-over Side Sheet (560px)**: Khi click vào bất kỳ dòng nào, Drawer trượt từ mép phải ra, giữ nguyên ngữ cảnh danh bạ nền mà không cần reload trang.
  - Phím tắt thông minh: Nhấn phím `Esc` để đóng Drawer, phím mũi tên lên/xuống để duyệt nhân sự.

### 2.6. Mẫu 6: Atlassian Administration (`admin.atlassian.com`)
* **Nguồn**: Atlassian Cloud Admin & Atlassian Design System (`atlassian.design`)
* **Đặc trưng cấu trúc**:
  - Quản trị bảo mật quy mô lớn: Kiểm soát xác thực 2 bước (2FA Enforcement).
  - Cảnh báo an toàn (Safety Impact Warning): Chặn tự hạ quyền nếu là Admin hoạt động duy nhất (`Prevent Lockout Rule`).
  - Thao tác hàng loạt (Bulk Actions): Đình chỉ tài khoản hoặc gửi lại email xác nhận cho nhiều nhân sự cùng lúc.

---

## 3. Khảo Sát Các Mẫu Độc Lập Hoàn Toàn Nhưng Cùng Miền Nghiệp Vụ (Independent Alternative Benchmarks)

Nhằm đảm bảo tính khách quan và đối chiếu sâu rộng, nhóm tiến hành khảo sát thêm 5 hệ sinh thái công nghệ độc lập hoàn toàn trên thế giới có nghiệp vụ quản lý thành viên và phân quyền tương tự:

### 3.1. Vercel Team & Project Governance
* **Nguồn**: Vercel Docs (`vercel.com/docs/accounts/teams/members`)
* **Nghiệp vụ tương đồng**:
  - **Phân cấp 2 tầng quyền (Two-tier Role Scoping)**: Tách rạch ròi giữa **Team-level Roles** (`Owner`, `Member`, `Developer`, `Billing`) và **Project-level Roles** (`Project Administrator`, `Project Developer`, `Project Viewer`).
  - **Quyền mở rộng đặc biệt (Extended Permissions)**: Cho phép cấp riêng quyền `Create Project` cho các Member/Developer mà không cần nâng họ lên cấp Admin toàn quyền. *(Khớp 100% với thuộc tính `hasProjectCreateGrant` và nghiệp vụ `DATN-16` của Continuum AI)*.
  - **Ràng buộc bảo mật an toàn**: Quy định bắt buộc luôn phải có tối thiểu một `Owner` hoạt động trong Team.

### 3.2. GitLab Group & Project Member Directory
* **Nguồn**: GitLab Documentation (`docs.gitlab.com/ee/user/group`)
* **Nghiệp vụ tương đồng**:
  - **Cơ chế thiết lập ngày hết hạn quyền truy cập (`Access expiration date` / `expires_at`)**: Cho phép Admin đặt thời hạn (theo định dạng ISO 8601: `YYYY-MM-DD`). Đến ngày hẹn, quyền thành viên tự động bị thu hồi hoặc hạ cấp, bảo đảm an toàn dữ liệu nội bộ.
  - **Thang phân quyền cấp số (Integer Access Levels)**: 10 (Guest), 20 (Reporter), 30 (Developer), 40 (Maintainer), 50 (Owner).
  - **Nhãn nhận diện nguồn gốc thành viên**: Phân biệt giữa thành viên trực tiếp (`Direct member`) và thành viên được thừa hưởng từ nhóm cha (`Inherited from Parent Group`).

### 3.3. Supabase Dashboard Organization Team Access
* **Nguồn**: Supabase Docs (`supabase.com/docs/guides/platform/org-based-access-control`)
* **Nghiệp vụ tương đồng**:
  - **Mô hình phân quyền linh hoạt**: `Owner`, `Administrator`, `Developer`, `Read-only`, và đặc biệt là chế độ **`No-Access`** (mặc định không có quyền gì ở cấp Tổ chức, chỉ được phân bổ quyền truy cập vào từng Project cụ thể được chỉ định).
  - **Vòng đời lời mời nghiêm ngặt**: Lời mời qua email tự động hết hạn sau **24 giờ** để ngăn chặn rò rỉ liên kết mời.
  - **Tích hợp Webhook sự kiện**: Bắn các sự kiện Webhook (`member.invitation.created`, `member.role.assigned`) khi có biến động nhân sự.

### 3.4. Stripe Dashboard Team Settings
* **Nguồn**: Stripe Docs (`stripe.com/docs/dashboard/teams`)
* **Nghiệp vụ tương đồng**:
  - **Nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege)**: Chỉ cấp đúng phạm vi quyền cần thiết cho công việc.
  - **Vai trò kết hợp (Composite Roles)**: Một người dùng có thể cùng lúc giữ vai trò Developer kết hợp Support Specialist mà không bị bó hẹp trong một chức danh cứng.
  - **Cảnh báo tác động nghiệp vụ (Business Impact Warning)**: Khi thay đổi quyền hạn có thể ảnh hưởng đến giao dịch, hệ thống yêu cầu xác nhận 2 lớp.
  - **Thời hạn thư mời**: Tự động vô hiệu hóa sau 10 ngày nếu chưa được kích hoạt.

### 3.5. Notion Workspace Settings (Members & Groups)
* **Nguồn**: Notion Help Center (`notion.so/help/members-and-groups`)
* **Nghiệp vụ tương đồng**:
  - **Phân nhóm theo vị trí sử dụng ghế (Seat Allocation Counter)**: Phân định rõ ràng giữa `Workspace Owner`, `Full Member` (tính phí/chiếm ghế bản quyền) và `Guest` (khách bên ngoài chỉ xem).
  - **Gắn thẻ nhóm chức năng trực tiếp**: Cho phép gán các nhóm như `@Engineering`, `@Product`, `@Marketing` ngay trong bảng người dùng để giao quyền hàng loạt.
  - **Xuất dữ liệu thành viên (Member Export CSV)**: Hỗ trợ Admin xuất toàn bộ danh bạ ra file CSV phục vụ kiểm toán nhân sự định kỳ.

---

## 4. Bảng Ma Trận Đối Chiếu Nghiệp Vụ Giữa Các Mẫu Độc Lập

| Nghiệp Vụ Doanh Nghiệp | Vercel | GitLab | Supabase | Stripe | Notion | Ứng Dụng Vào Continuum AI (`DATN-351` - `DATN-353`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Phân cấp Role Cố Định** | ✅ 4 roles | ✅ 5 levels | ✅ 5 roles | ✅ Built-in | ✅ 3 tiers | **3 Roles IAM: `ADMIN`, `TEAM_LEADER`, `MEMBER`** |
| **Quyền tạo dự án riêng** | ✅ `Create Project` | Maintainer+ | Project-scoped | Custom | Member+ | **Quyền đặc biệt `hasProjectCreateGrant` (Icon Chìa Khóa)** |
| **Phân vùng dự án (Scoping)** | ✅ Project roles | Group/Subgroup | ✅ `No-Access` | Per-account | Teamspaces | **Hiển thị các tag dự án: `CONT`, `IAM`, `CORE`, `WORK`** |
| **Hết hạn quyền / Lời mời** | Invite link | ✅ `expires_at` | ✅ 24h Expiry | ✅ 10 days | Guest expiry | **Hiển thị trạng thái hết hạn trong Tab Lời mời đang chờ** |
| **Bảo vệ chống mất Admin** | ✅ Phải có 1 Owner | Min 1 Owner | Transfer rule | Account Owner | Min 1 Owner | **Khóa nút hạ quyền nếu là Admin hoạt động duy nhất** |
| **Thao tác hàng loạt (Bulk)** | Team invite | Batch remove | API batch | Batch invite | Bulk CSV | **Floating Bulk Bar (Đổi Role, Khóa, Xuất CSV hàng loạt)** |

---

## 5. Hiện Thực Hóa Trực Quan Tại `DEMO_FE_TASK`

Toàn bộ các mẫu khảo sát trên đã được lập trình trực tiếp thành các mô-đun giao diện có thể chuyển đổi và tương tác trực tiếp tại thư mục `DEMO_FE_TASK`:

1. **Bộ Chuyển Đổi Mẫu Thiết Kế (Design Model Switcher)** trên Header:
   - `Mẫu Gốc`: Prototype ban đầu của nhóm để đối chiếu.
   - `Untitled UI`: Phong cách chuẩn mực Modern B2B SaaS (Avatar gộp email, chấm LED trạng thái mềm).
   - `Tailwind + Linear`: Mật độ cao, tối giản phẳng, hiển thị badge dự án và phím tắt.
   - `Atlassian Enterprise`: Quản trị an ninh, theo dõi 2FA và thanh thao tác hàng loạt (Bulk Bar).
   - `shadcn/ui & TanStack Table`: Headless data table với bộ lọc đa chiều (Faceted Filters), tùy chỉnh ẩn hiện cột.
   - `Clerk & WorkOS`: Tách riêng tab Thành viên và Lời mời đang chờ kèm thao tác đổi quyền inline và gửi lại lời mời.
2. **Nút "So Sánh Các Mẫu Thiết Kế" (Compare Modal)**:
   - Đối chiếu ưu/nhược điểm từng mẫu kèm **đường link nguồn trực tiếp từ Internet** để reviewer và hội đồng kiểm chứng.
3. **Mô Phỏng 5 Trạng Thái Biên (Edge States Simulator)**:
   - `Normal View`, `Skeleton Shimmer 5 rows`, `Empty Search Result`, `Empty Organization`, `Server Error 500`, `Permission Denied 403`.
4. **Modal Thông Số Thiết Kế Figma (Figma Specs Modal)**:
   - Đầy đủ bảng mã màu Hex chuẩn, Spacing tokens hệ 8px, và Hợp đồng API giữa Frontend và Backend.
