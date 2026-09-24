# [RESEARCH] Governance - Organization Context

**Ticket**: `DATN-15`  
**Assignee**: Nguyen Hong Phuc  
**Due Date**: Sep 26, 2026  
**Status**: Research Only (No implementation, no code changes, no dependency changes)  
**Target System**: DATN / Continuum AI Baseline  

---

## 1. Evidence Classification Standard (Truth Grading)

Báo cáo tuân thủ nghiêm ngặt chuẩn phân loại bằng chứng theo quy định của dự án:
- `[FACT / VERIFIED]`: Đã được kiểm chứng trực tiếp từ mã nguồn thực tế đang tồn tại trong repository.
- `[IMPLEMENTED]`: Đã có logic/code thực thi hoạt động (không chỉ là schema hay interface).
- `[DESIGN / PROPOSED]`: Được mô tả trong tài liệu kiến trúc, specification, SRS hoặc ADR nhưng chưa có code.
- `[PARTIAL]`: Đã có một phần cấu trúc hỗ trợ (như schema), nhưng logic nghiệp vụ/API chưa hoàn thiện.
- `[GAP]`: Yêu cầu đã được đặc tả trong tài liệu nhưng hoàn toàn chưa có trong mã nguồn.
- `[INFERENCE]`: Kết luận được tổng hợp và suy luận logic từ nhiều nguồn có cơ sở.
- `[UNKNOWN]`: Thiếu bằng chứng, không tìm thấy thông tin trong cả tài liệu lẫn mã nguồn.
- `[DECISION REQUIRED]`: Tồn tại mâu thuẫn hoặc điểm hở kiến trúc cần người/nhóm họp ra quyết định chính thức.

---

## 2. Executive Summary

1. `[FACT]` / `[PARTIAL]` **Data Isolation Baseline**: Toàn bộ hệ thống cơ sở dữ liệu backend (`DATN-BE`) đã được chuẩn bị cấu trúc Multi-Tenant phân cấp nghiêm ngặt thông qua trường `organizationId` (ObjectId) trên hầu hết các collection: `projects`, `teams`, `lifecycle_*`, `jira_*`, `ingestion_*`, `handover_*`, `audit_logs`.
2. `[FACT]` / `[PARTIAL]` **Session Binding**: Bảng `refresh_sessions` trong module IAM đã lưu cặp `(userId, organizationId)`. Điều này khẳng định phiên đăng nhập của người dùng được neo chặt vào một ngữ cảnh Organization cụ thể.
3. `[GAP]` **Zero Context Resolution in Code**: Tại tầng HTTP của backend (`DATN-BE/src/common/http`), hiện tại chỉ có duy nhất `request-id.middleware.ts` (`x-request-id`). Hoàn toàn **chưa có** Middleware, Interceptor, hoặc Custom Param Decorator nào để trích xuất và thiết lập Organization Context cho request.
4. `[GAP]` **Zero Authorization Guards in Code**: `DATN-BE/src` hiện tại chưa triển khai bất kỳ NestJS Guard (`CanActivate`) nào để kiểm tra quyền truy cập hay chặn truy cập chéo tổ chức (Cross-Organization Denial).
5. `[GAP]` **Frontend Inactive**: `DATN-FE` hiện tại là template TailAdmin thuần giao diện. Thư mục `src/context` chỉ có `SidebarContext` và `ThemeContext`. Chưa có Auth Context, chưa có Organization Switcher, và chưa lưu trạng thái `activeOrganizationId`.

---

## 3. Scope & Focus

### Trong phạm vi nghiên cứu (In Scope):
- Phạm vi tổ chức (Organization scope) và quan hệ thực thể: `User ➔ Organization` và `Resource ➔ Organization`.
- Cơ chế nhận diện ngữ cảnh request (Request Context Resolution: Header vs JWT vs Route Param).
- Cơ chế từ chối và cách ly truy cập chéo tổ chức (Cross-Organization Denial).
- Sự phụ thuộc của phân quyền Project và Team vào Organization Context.
- Đối chiếu giữa tài liệu đặc tả kiến trúc (`Document/architecture/05_SECURITY_AND_GOVERNANCE.md`, `02_ACTORS_ROLES_AND_PERMISSIONS.md`) và mã nguồn thực tế (`DATN-BE`, `DATN-FE`).

### Ngoài phạm vi nghiên cứu (Out of Scope):
- Tuyệt đối **không code**, không chỉnh sửa cấu hình hệ thống, không thay đổi dependencies, không mở PR.
- Không tự ý giải quyết các điểm mâu thuẫn hoặc tự chế tác ra hành vi multi-org khi chưa có quyết định của team.

---

## 4. Verified Requirements Checklist

| Yêu cầu (Requirement) | Nguồn bằng chứng (Evidence Source) | Phân loại (Classification) | Ghi chú & Hiện trạng kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Organization là ranh giới dữ liệu cấp cao nhất** | `05_SECURITY_AND_GOVERNANCE.md`; `02_ACTORS_ROLES_AND_PERMISSIONS.md` | `[DESIGN]` | Mọi tài nguyên dự án, nhóm, tri thức đều trực thuộc một Organization. |
| **Bảng Organizations tồn tại trong CSDL** | `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts` | `[FACT]` | Có collection `organizations` với `name`, `slug` (unique index), `plan` (`FREE` \| `ENTERPRISE`), `settings`. |
| **User không chứa cứng `organizationId`** | `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts` | `[FACT]` | Schema `users` chỉ chứa `email`, `passwordHash`, `status`, `twoFactorEnabled`. Quan hệ User - Org là quan hệ nhiều - nhiều qua bảng trung gian. |
| **Liên kết User ➔ Organization qua Role & Membership** | `DATN-BE/.../mongodb.schemas.ts` | `[FACT]` | Được liên kết qua `role_assignments` (index `{ organizationId: 1, projectId: 1, userId: 1 }`) và `organization_capability_grants`. |
| **Mọi Resource đều gắn cứng `organizationId`** | Toàn bộ các file `persistence.ts` trong `DATN-BE/src/services/*` | `[FACT]` | `projects`, `teams`, `jira_connections`, `raw_documents`, `knowledge_objects`, `audit_logs` đều có `organizationId` và compound index. |
| **Phiên làm việc (Session) neo theo Organization** | `refresh_sessions` schema trong IAM service | `[FACT]` | Schema khai báo rõ `userId` và `organizationId`. |
| **Request Context Resolution qua JWT Claims** | `05_SECURITY_AND_GOVERNANCE.md` (Mục 2) | `[DESIGN]` | Tài liệu thiết kế chỉ định Pre-Retrieval ACL giải mã JWT lấy `userId`, `roles`, `teamIds`. |
| **Middleware / Guard nhận diện Organization Context** | `DATN-BE/src/common/http` | `[GAP]` | Chưa có file middleware hoặc guard nào để validate và inject `organizationId` vào Request pipeline. |
| **Cross-Organization Access Denial** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 2) | `[DESIGN]` | "Deny takes precedence. Cross-tenant or cross-project access must be explicitly authorized, not inferred." |
| **Enforcement chặn truy cập chéo ở Backend** | `DATN-BE/src` | `[GAP]` | Chưa có Guard hoặc Mongoose Tenant Filter Plugin để tự động từ chối truy cập chéo Org. |
| **Frontend Organization State / Switcher** | `DATN-FE/src/context`, `src/layout` | `[GAP]` | Chưa có context quản lý Org hiện tại, chưa có UI dropdown chọn Organization. |

---

## 5. Core Business Rules (Quy tắc nghiệp vụ cốt lõi)

### 5.1. Quy tắc đã được xác minh (`[FACT]` & `[DESIGN]`)
1. **BR-ORG-01 (Isolation Boundary)**: `[DESIGN]` Một request chỉ được phép truy xuất hoặc thao tác trên tài nguyên (Resource) có `organizationId` khớp chính xác với Organization Context của phiên làm việc hiện tại.
2. **BR-ORG-02 (Hierarchical Containment)**: `[FACT]` / `[DESIGN]` Cấu trúc phân cấp bắt buộc:
   $$\text{Organization} \longrightarrow \text{Project} \longrightarrow \text{Team} \longrightarrow \text{Domain / Resource ACL}$$
   Không thể tồn tại một Project hay Team độc lập nằm ngoài Organization.
3. **BR-ORG-03 (Explicit Capability Grant)**: `[FACT]` / `[DESIGN]` Để tạo mới một Project trong Organization, User có vai trò `TEAM_LEADER` bắt buộc phải có bản ghi cấp quyền hợp lệ và còn hiệu lực trong collection `organization_capability_grants` với `capability = 'project.create'`.
4. **BR-ORG-04 (Admin Limitation)**: `[DESIGN]` Người dùng có vai trò `ADMIN` của Organization có toàn quyền quản trị tài khoản, phân quyền, cấu hình kết nối Jira, nhưng **không có quyền mặc định** đọc nội dung tri thức mật của Project/Team nếu không có membership trong project đó.
5. **BR-ORG-05 (Audit Provenance)**: `[FACT]` Mọi hành động nhạy cảm cấp Organization (gán role, cấp capability, tạo project) bắt buộc phải ghi log vào collection `audit_logs` có kèm `organizationId`, `actorUserId`, `action`, `targetResourceId`.

### 5.2. Quy tắc chưa xác lập / Cần làm rõ (`[UNKNOWN]` / `[DECISION REQUIRED]`)
- **BR-ORG-UN01**: Khi người dùng cố tình truy cập tài nguyên của Organization khác (bằng cách sửa ID trên URL/body), hệ thống trả về HTTP `403 Forbidden` hay `404 Not Found`?
- **BR-ORG-UN02**: Tài khoản người dùng có được phép active ở nhiều Organization cùng một thời điểm qua nhiều tab trình duyệt không, hay mỗi access token chỉ đại diện cho đúng 1 Organization tại một thời điểm?

---

## 6. Requirement ➔ Evidence ➔ Implementation ➔ Gap Matrix

| Phân tầng (Layer) | Yêu cầu nghiệp vụ (Requirement) | Bằng chứng tài liệu (Evidence) | Hiện trạng mã nguồn (Implementation) | Khoảng trống kỹ thuật (Gap) |
| :--- | :--- | :--- | :--- | :--- |
| **Schema (Database)** | Lưu trữ định danh và cài đặt Organization | `05_SECURITY...md`, `SPEC.md` | Đã có collection `organizations` trong `DATN-BE` (`continuum_iam`) | `[PARTIAL]` Thiếu migration tạo dữ liệu default organization khởi tạo. |
| **Schema (Database)** | Quan hệ User - Organization | `02_ACTORS...md` | `role_assignments` và `organization_capability_grants` | `[PARTIAL]` Index của `role_assignments` là `{ organizationId: 1, projectId: 1, userId: 1 }`. Nếu gán role cấp Org (không có Project), `projectId` là `null`, cần kiểm tra index sparse. |
| **API Contract** | Giao thức truyền Organization Context | `05_SECURITY...md` | Chưa có endpoint API nào ngoài `/health` | `[GAP]` Chưa chốt chuẩn truyền: Header `X-Organization-Id` hay Claim trong JWT payload hay URL param. |
| **Business Logic** | Trích xuất và xác thực Org Context | `05_SECURITY...md` (Mục 2) | File `DATN-BE/src/common/http` chỉ có `request-id` | `[GAP]` Chưa có `OrgContextMiddleware` hoặc NestJS Guard trích xuất Org Context và gán vào request object. |
| **Security / Guard** | Ngăn chặn truy cập chéo tổ chức (Cross-Org Denial) | `02_ACTORS...md` (Mục 2) | Không có Guard nào trong `DATN-BE/src` | `[GAP]` Cần xây dựng `OrgScopeGuard` chặn đứng request nếu `request.orgId !== resource.orgId`. |
| **Frontend UI** | Quản lý trạng thái Organization hiện tại | TailAdmin specs | `DATN-FE/src/context` chỉ có Sidebar & Theme | `[GAP]` Hoàn toàn chưa có `OrgContext` / State lưu trữ `activeOrgId` và UI Switcher. |
| **Integration / E2E** | Test case xác nhận từ chối chéo tổ chức | `DATN-BE/docs/SPEC.md` | `DATN-BE/test` mới chỉ test health check | `[GAP]` Chưa có E2E test cho kịch bản Cross-Org 403/404. |

---

## 7. API, Data & Security Findings

### 7.1. Data & Schema Findings
- **Tính nhất quán ở tầng dữ liệu**: Điểm mạnh là 100% các domain service (`iam`, `lifecycle`, `jira`, `ingestion`, `handover`, `notification`) đều đã gắn trường `organizationId: { type: Schema.Types.ObjectId, required: true }` vào tất cả các schema thực thể.
- **Index Composite**: Các collection đều có composite index bắt đầu bằng `organizationId`, ví dụ:
  - `projects`: `{ organizationId: 1, code: 1 }`
  - `teams`: `{ organizationId: 1, projectId: 1, code: 1 }`
  - `lifecycle_proposals`: `{ organizationId: 1, projectId: 1, status: 1 }`
  Điều này tối ưu hóa việc cô lập dữ liệu theo từng tenant ở tầng MongoDB query.

### 7.2. API & Context Findings
- Hiện tại chưa có quy ước chính thức về việc truyền Organization Context:
  - **Phương án 1 (Header-based)**: Client gửi `X-Organization-Id: <org_id>` trong mọi request.
  - **Phương án 2 (JWT-based)**: Client gửi Bearer Token, token chứa sẵn claim `{ org_id: "..." }`. Khi đổi Org phải xin cấp lại Access Token mới.
  - **Phương án 3 (URL-based)**: Mọi endpoint có prefix `/api/v1/orgs/:orgId/...`.

### 7.3. Security & Vulnerability Findings
- **Nguy cơ Insecure Direct Object References (IDOR)**: Nếu các API sau này truy vấn trực tiếp bằng `_id` mà không kèm điều kiện `{ organizationId: currentOrgId }`, kẻ tấn công thuộc Org A có thể xem/sửa dữ liệu của Org B bằng cách đoán ID.
- **Giải pháp kiến trúc bắt buộc**: Cần có một Mongoose Plugin hoặc Base Repository tự động chèn `{ organizationId }` vào tất cả các thao tác `find`, `findOne`, `updateOne`, `deleteOne`.

---

## 8. Frontend & Backend Mismatches & BFF Findings

Dựa trên mã nguồn mới nhất vừa cập nhật từ `DATN-FE` (`origin/main`):

1. **State Store (`src/stores/client-state.ts`)**:
   - `[FACT]` Store Zustand hiện tại chỉ có `activeProjectId: string | null` và `setActiveProjectId`.
   - `[GAP]` **Hoàn toàn thiếu `activeOrganizationId`** để lưu giữ ngữ cảnh Organization đang chọn.
2. **User Identity Contract (`src/lib/queries/auth/useAuth.ts`)**:
   - `[FACT]` Kiểu dữ liệu `CurrentUserResponse` từ endpoint `/users/me` đã định nghĩa sẵn trường `organizationId: string`:
     ```typescript
     export type CurrentUserResponse = Readonly<{
       id: string;
       email: string;
       name: string;
       organizationId: string;
       roles: readonly string[];
     }>;
     ```
   - `[INFERENCE]` Bản thiết kế FE ngầm định mỗi User thuộc về một `organizationId` chính khi login.
3. **BFF Proxy Header Whitelist (`src/lib/bff-proxy.ts`)**:
   - `[FACT]` Next.js BFF Proxy (`/api/backend/[...path]`) lọc header chuyển tiếp qua danh sách cố định:
     ```typescript
     const forwardedHeaders = [
       'accept',
       'authorization',
       'content-type',
       'cookie',
       'x-request-id',
     ];
     ```
   - `[GAP / WARNING]` **Nguy cơ lỗi tích hợp**: Header `x-organization-id` hiện **KHÔNG** nằm trong `forwardedHeaders`. Nếu Frontend gửi header này lên BFF, proxy sẽ lọc bỏ hoàn toàn trước khi chuyển tiếp sang Backend!
4. **Về Routing**:
   - Frontend đang dùng route dạng `/[locale]/(admin)/...` mà không có segment cho `[organizationId]`. Điều này ngụ ý Organization Context trên Frontend phải được duy trì qua State/Cookie/Header thay vì URL Path.

---

## 9. Dependencies for Project & Team Authorization

Phân quyền Project và Team phụ thuộc chặt chẽ vào Organization Context theo chuỗi phụ thuộc (Dependency Chain) sau:

$$\text{Authentication (User Verified)} \longrightarrow \mathbf{\text{Organization Context}} \longrightarrow \text{Project Authorization} \longrightarrow \text{Team Authorization}$$

1. **Điều kiện tiên quyết để vào Project**: Người dùng phải có liên kết hợp lệ với Organization chứa Project đó. Nếu Organization Context không hợp lệ hoặc bị đình chỉ (`SUSPENDED`), toàn bộ quyền truy cập Project và Team lập tức bị chặn.
2. **Quyền hạn tạo Project**: Phụ thuộc vào `organization_capability_grants` tại tầng Organization. Chỉ khi có bản ghi hợp lệ ở tầng này, Team Leader mới có thể gọi API tạo Project.
3. **Phân cấp dữ liệu Team**: Mọi team đều mang cặp `(organizationId, projectId)`. Việc kiểm tra quyền hạn của Team bắt buộc phải kế thừa và nằm trong phạm vi của Organization tương ứng.

---

## 10. UNKNOWN / DECISION REQUIRED

Trước khi bước vào giai đoạn hiện thực hóa (Implementation), nhóm phát triển và Leader cần thống nhất các quyết định kiến trúc sau:

| Mã quyết định | Vấn đề cần quyết định | Các phương án lựa chọn | Khuyến nghị (Recommendation) |
| :--- | :--- | :--- | :--- |
| **DEC-01** | **Cách thức truyền Organization Context trong HTTP Request** | A. Qua Header `X-Organization-Id`<br>B. Nằm trong Payload của JWT Token<br>C. Nằm trên URL Route (`/api/v1/organizations/:orgId/...`) | **Chọn Phương án B kết hợp A**: JWT mang `org_id` mặc định của phiên; có thể hỗ trợ Header `X-Organization-Id` đối với request cần chuyển đổi ngữ cảnh nếu User thuộc nhiều Org. |
| **DEC-02** | **Mã lỗi HTTP khi vi phạm Cross-Organization Access** | A. Trả về `403 Forbidden`<br>B. Trả về `404 Not Found` | **Chọn Phương án B (404 Not Found)** đối với truy vấn tài nguyên cụ thể để ngăn chặn enumeration attack (dò đoán ID của tổ chức khác). Trả về **403 Forbidden** khi User không có quyền trên toàn bộ Organization Context. |
| **DEC-03** | **Cơ chế một tài khoản thuộc nhiều Organization (Multi-Org User)** | A. Cho phép 1 User thuộc nhiều Org, khi đăng nhập chọn 1 Active Org.<br>B. MVP chỉ hỗ trợ 1 User thuộc 1 Org duy nhất. | **Chọn Phương án A về mặt Schema** (Schema hiện tại đã hỗ trợ quan hệ N-N), nhưng **giới hạn UI ở MVP** chỉ hiển thị 1 Org mặc định để giảm độ phức tạp giao diện. |

---

## 11. Implementation-Breakdown Recommendation (Đề xuất kế hoạch triển khai)

Tuân thủ nghiêm ngặt quy trình của dự án tại `Document/AI_WORKFLOW.md`, công việc hiện thực hóa sau khi research cần được chia tách thành các nhánh (branch) và PR độc lập theo thứ tự:

```text
[1. DB PR] ────────► [2. BE PR] ────────► [3. FE PR]
```

### Bước 1: Database Branch & PR (`feat/Phuc-org-context-db`)
- Kiểm tra và bổ sung index cho `role_assignments` đối với các quyền cấp Organization (`projectId: null`).
- Viết migration script khởi tạo Organization mặc định (`Continuum AI Default Org`) và seed dữ liệu ban đầu.

### Bước 2: Backend Branch & PR (`feat/Phuc-org-context-be-api`)
- Xây dựng `OrgContextMiddleware` hoặc NestJS Interceptor để đọc `X-Organization-Id` / JWT payload và gắn vào `request.orgContext`.
- Tạo custom decorator `@CurrentOrg()` và `@CurrentOrgId()`.
- Xây dựng `OrgScopeGuard` (`CanActivate`) để kiểm tra người dùng có quyền trong Organization hiện tại hay không.
- Thêm Base Mongoose Tenant Plugin/Helper để tự động inject `{ organizationId }` vào các query.
- Viết Unit Test và E2E test cho kịch bản hợp lệ và kịch bản từ chối truy cập chéo tổ chức.

### Bước 3: Frontend Branch & PR (`feat/Phuc-org-context-fe-ui`)
- Tạo `OrganizationContext` trong `DATN-FE/src/context/OrganizationContext.tsx` để lưu trữ thông tin và trạng thái của Organization đang hoạt động.
- Cấu hình Axios/Fetch client tự động đính kèm Header `X-Organization-Id` vào tất cả các request gửi sang Backend.
- Bổ sung `x-organization-id` vào danh sách `forwardedHeaders` trong `DATN-FE/src/lib/bff-proxy.ts`.
- Xây dựng UI component Organization Switcher / Display trên Navbar hoặc Sidebar của TailAdmin layout.
