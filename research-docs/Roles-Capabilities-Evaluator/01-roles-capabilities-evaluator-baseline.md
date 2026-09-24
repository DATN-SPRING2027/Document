# [RESEARCH] Roles, Capabilities, Evaluator & Access Control Baseline

**Ticket**: `DATN-16`  
**Assignee**: Nguyen Hong Phuc  
**Due Date**: Sep 26, 2026  
**Status**: Research Only (No implementation, no code changes, no configuration/dependency changes, no PR)  
**Target System**: DATN / Continuum AI Baseline  

---

## 1. Evidence Classification Standard (Truth Grading)

Báo cáo nghiên cứu tuân thủ nghiêm ngặt chuẩn mực phân loại bằng chứng và kiểm chứng sự thật của dự án:
- `[FACT / VERIFIED]`: Đã kiểm chứng trực tiếp từ mã nguồn thực tế trong repository (`DATN-BE`, `DATN-FE`).
- `[IMPLEMENTED]`: Logic thực thi đã tồn tại, có thể vận hành và kiểm thử thực tế (không chỉ là schema/interface).
- `[DESIGN / PROPOSED]`: Được mô tả trong tài liệu kiến trúc, đặc tả SRS, ADR, hoặc quyết định đã được duyệt, nhưng chưa có mã nguồn thực thi.
- `[PARTIAL]`: Đã có phần khung hạ tầng (scaffolding/schema/type declaration), nhưng tầng nghiệp vụ hoặc API thực thi chưa hoàn chỉnh.
- `[GAP]`: Yêu cầu có trong đặc tả kiến trúc nhưng hoàn toàn vắng mặt trong mã nguồn hiện tại.
- `[INFERENCE]`: Kết luận logic được tổng hợp từ nhiều nguồn dữ liệu đã kiểm chứng.
- `[UNKNOWN]`: Thiếu bằng chứng trong cả tài liệu lẫn mã nguồn; chưa được định nghĩa.
- `[DECISION REQUIRED]`: Điểm sai lệch, xung đột kiến trúc hoặc chính sách mở cần Lead/Team thảo luận và ra quyết định chính thức (không tự tiện suy đoán hoặc tự duyệt ma trận).

---

## 2. Executive Summary

1. `[FACT]` / `[PARTIAL]` **Data Model & Scaffolding**: Tầng lưu trữ của Backend (`DATN-BE`) đã có khai báo Mongoose schemas cho 3 Persistent Roles cố định (`ADMIN`, `TEAM_LEADER`, `MEMBER`), `role_assignments`, `organization_capability_grants` (chỉ enum `'project.create'`), và các bảng phân công chuyên trách (`sme_assignments`, `knowledge_owner_assignments`). Tuy nhiên, đây mới chỉ là khai báo Schema và Index trong database; toàn bộ logic thực thi nghiệp vụ cấp quyền chưa hề được triển khai.
2. `[GAP]` **Zero Evaluator & Guard trong Backend**: Trong toàn bộ codebase `DATN-BE/src`, hiện tại **hoàn toàn chưa có** bất kỳ NestJS Guard (`CanActivate`), Interceptor, Evaluator Service, hay Custom Decorators (`@Roles()`, `@RequireCapability()`) nào. Controller duy nhất hiện tại (`iam.controller.ts`) chỉ có endpoint kiểm tra sức khỏe `/health`.
3. `[GAP]` **Thiếu ranh giới 401 vs 403 tại Transport Layer**: Mã lỗi `401 Unauthorized` và `403 Forbidden` mới chỉ được khai báo trong OpenAPI specification draft (`DATN-BE/docs/openapi/iam-v1.openapi.json`), chưa có bộ lọc exception hoặc middleware nào xử lý phân biệt hai loại lỗi này.
4. `[GAP]` **Frontend UI hoàn toàn là Template tĩnh**: Phía `DATN-FE` hiện chỉ là bản dựng Next.js từ TailAdmin template. Zustand store (`src/stores/client-state.ts`) chỉ có `activeProjectId`, hoàn toàn không có trạng thái lưu User Roles, Capabilities, hay các UX-only checks (`can(...)`, `hasRole(...)`).
5. `[DESIGN]` **Quy tắc phân quyền cốt lõi đã được định nghĩa**:
   - `ADMIN` không mặc định đọc nội dung tri thức mật.
   - `TEAM_LEADER` không mặc định có quyền tạo dự án; quyền `project.create` bắt buộc phải do `ADMIN` cấp riêng biệt qua `organization_capability_grants`.
   - **Deny Precedence**: Quyền từ chối (Explicit Deny) có độ ưu tiên cao nhất, vượt qua mọi role hay grant.
   - Frontend checks chỉ đóng vai trò hỗ trợ trải nghiệm người dùng (UX-only); Backend là chốt chặn an ninh bắt buộc (Authoritative Boundary).

---

## 3. Scope & Research Focus

### 3.1. Phạm vi nghiên cứu (In Scope):
- **3 Persistent Roles**: `ADMIN`, `TEAM_LEADER`, `MEMBER` và ranh giới vai trò vs. năng lực (Role vs. Capability boundaries).
- **Phân cấp phạm vi (Scope Hierarchy)**: Organization Scope ➔ Project Scope ➔ Team Scope ➔ Domain/Resource ACL.
- **Cơ chế cấp quyền tạo dự án (`project.create`)**: Thẩm quyền cấp của ADMIN, điều kiện hiệu lực, thu hồi, và ngăn chặn leo thang đặc quyền.
- **Trạng thái bộ đánh giá quyền (Evaluator / Guard status)**: Khảo sát hiện trạng NestJS Guards, Decorators, và đánh giá Deny Precedence.
- **Ranh giới lỗi 401 vs 403**: Bản chất phân biệt giữa lỗi xác thực (Unauthenticated) và lỗi phân quyền (Forbidden/Unauthorized Scope); ranh giới bảo mật Backend vs. UX gating Frontend.
- **Kịch bản kiểm tra chéo phạm vi và leo thang đặc quyền (Cross-scope & Escalation scenarios)**.

### 3.2. Ngoài phạm vi (Out of Scope):
- Không viết code thực thi, không thay đổi file cấu hình hay dependency, không tạo Pull Request.
- Không tự ý quyết định ma trận phân quyền chi tiết khi chưa có sự phê duyệt chính thức từ Team Lead (`Do not decide an unapproved matrix`).

---

## 4. Verified Requirements Checklist

| Yêu cầu nghiệp vụ / Kỹ thuật | Nguồn tài liệu / Bằng chứng | Đánh giá | Hiện trạng thực tế trong Codebase |
| :--- | :--- | :--- | :--- |
| **3 Persistent Roles cố định: `ADMIN`, `TEAM_LEADER`, `MEMBER`** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 1); `05_SECURITY...md` (Mục 1.1) | `[FACT]` / `[PARTIAL]` | Schema `roles` trong `DATN-BE/.../mongodb.schemas.ts:111` định nghĩa enum `['ADMIN', 'TEAM_LEADER', 'MEMBER']`. Chưa có seed migration hoặc API quản lý role. |
| **Không sử dụng tên vai trò cũ (`PROJECT_MANAGER`, `PROJECT_ADMIN`, `TEAM_MEMBER`)** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 1) | `[FACT]` | Không tìm thấy bất kỳ sự xuất hiện nào của các role cũ này trong schema của `DATN-BE`. |
| **SME, KNOWLEDGE_OWNER, SUCCESSOR là Scoped Assignments, không phải Role** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 4) | `[FACT]` / `[PARTIAL]` | Trong `DATN-BE`, `sme_assignments` và `knowledge_owner_assignments` được tách thành các collection riêng biệt, không gộp chung vào bảng `roles`. |
| **ONBOARDING / OFFBOARDING là trạng thái vòng đời, không phải Role** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 4) | `[FACT]` / `[PARTIAL]` | `users.status` trong schema Mongoose định nghĩa `['ACTIVE', 'SUSPENDED', 'PENDING_INVITE']`. Trạng thái `ONBOARDING`/`OFFBOARDING` chưa có trong schema User (chỉ xuất hiện ở tài liệu thiết kế). |
| **Quyền tạo dự án `project.create` độc lập, không mặc định cho TEAM_LEADER** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 1, 5) | `[FACT]` / `[PARTIAL]` | Bảng `organization_capability_grants` (`DATN-BE/.../mongodb.schemas.ts:139`) định nghĩa `capability: { type: String, enum: ['project.create'] }`. |
| **Phân cấp phạm vi: Organization ➔ Project ➔ Team ➔ Resource** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 2) | `[FACT]` / `[PARTIAL]` | Các bảng `projects`, `teams`, `project_memberships`, `team_memberships` đều có khóa ngoại tham chiếu theo đúng hình cây phân cấp. |
| **Quy tắc ưu tiên từ chối (Deny Precedence)** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 2); `05_SECURITY...md` (Mục 2) | `[DESIGN]` / `[GAP]` | Đã được đặc tả trong công thức toán học tính quyền hiệu lực ($P_{\text{eff}}$), nhưng chưa có bất kỳ dòng code logic nào cài đặt quy tắc này trong backend. |
| **NestJS Evaluator / Guard kiểm tra quyền tại Backend** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 6) | `[GAP]` | Không có class nào implement `CanActivate`, không có `@UseGuards()`, không có service kiểm tra quyền trong `DATN-BE`. |
| **Phân định rõ mã phản hồi 401 Unauthorized vs. 403 Forbidden** | `iam-v1.openapi.json:670-685` | `[PARTIAL]` / `[GAP]` | OpenAPI spec đã định nghĩa 401 và 403. Nhưng controller thực tế chưa implement, và phía FE `api-client.ts` chỉ ném lỗi chung `API request failed` mà không phân loại mã trạng thái HTTP. |
| **Frontend UX-only checks (ẩn/hiện nút bấm, bảo vệ route UI)** | `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 2) | `[GAP]` | Phía `DATN-FE` hoàn toàn chưa có component Authorize, hook kiểm tra quyền, hoặc store lưu quyền người dùng. |

---

## 5. Core Business Rules & Boundaries

### 5.1. Quy tắc về vai trò và ranh giới quyền lực (Role vs. Capability Boundaries)
1. **BR-AUTH-01 (Role Immutability & Exclusivity)**: `[DESIGN]` Hệ thống chỉ công nhận 3 Human Persistent Roles: `ADMIN`, `TEAM_LEADER`, và `MEMBER`. Các danh xưng khác như SME, Knowledge Owner chỉ là các phân công nghiệp vụ có thời hạn (Scoped Assignments).
2. **BR-AUTH-02 (Admin Isolation from Confidential Knowledge)**: `[DESIGN]` `ADMIN` có toàn quyền quản trị người dùng, cấu hình tổ chức, cấp phát quyền và kiểm tra metadata kỹ thuật; tuy nhiên `ADMIN` **không tự động có quyền đọc hoặc duyệt nội dung tri thức mật** của các dự án nếu không được cấp quyền tham gia dự án cụ thể đó.
3. **BR-AUTH-03 (Separation of Project Creation)**: `[FACT]` / `[DESIGN]` Role `TEAM_LEADER` chỉ quản lý các team và không gian làm việc đã được phân công trong phạm vi dự án hiện hữu. Một Team Leader **không bao giờ** tự động có quyền tạo Project mới.
4. **BR-AUTH-04 (Explicit `project.create` Grant)**: `[FACT]` / `[DESIGN]` Để một `TEAM_LEADER` có thể tạo Project mới, một `ADMIN` phải thực hiện thao tác cấp quyền tường minh vào bảng `organization_capability_grants` với:
   - `organizationId`: ID tổ chức cấp quyền.
   - `userId`: ID của Team Leader được cấp.
   - `capability`: `'project.create'`.
   - `grantedBy`: ID của Admin thực hiện cấp.
   - `reason`: Lý do nghiệp vụ cấp quyền (bắt buộc).
   - `expiresAt`: Thời hạn hết hiệu lực (tùy chọn nhưng khuyến nghị).
   - `revokedAt`: Thời điểm bị thu hồi (nếu bị hủy bỏ trước thời hạn).
5. **BR-AUTH-05 (No Self-Grant & No Delegation)**: `[DESIGN]` Người được cấp capability không thể tự gia hạn, tự cấp cho mình, hoặc ủy quyền capability đó cho người khác.
6. **BR-AUTH-06 (Bootstrap Policy post-Project Creation)**: `[DESIGN]` Khi một Team Leader sử dụng quyền `project.create` để tạo dự án mới thành công, hệ thống tự động gán người này làm Team Leader của dự án đó thông qua chính sách bootstrap. Thao tác này **không biến họ thành Admin của tổ chức** và **không cấp quyền truy cập sang các dự án khác**.

### 5.2. Phân cấp phạm vi và cơ chế kiểm soát truy cập (Scope & ACL Checks)
1. **BR-SCOPE-01 (Hierarchical Scope Constraint)**: `[FACT]` / `[DESIGN]` Mọi truy xuất tài nguyên phải thỏa mãn kiểm tra phạm vi lồng nhau:
   $$\text{Organization Context} \supseteq \text{Project Context} \supseteq \text{Team Context} \supseteq \text{Resource ACL}$$
   Không một thao tác nào được phép truy cập tài nguyên nếu phiên làm việc không thuộc đúng Organization của tài nguyên đó.
2. **BR-SCOPE-02 (Pre-Retrieval Scoped ACL)**: `[DESIGN]` Công thức tính quyền hiệu lực bắt buộc phải áp dụng trước khi truy vấn dữ liệu từ cơ sở dữ liệu hoặc chuyển ngữ cảnh cho LLM:
   $$P_{\text{eff}} = \left( P_{\text{user}} \cup P_{\text{teams}} \cup P_{\text{roles}} \right) \cap \text{SourceACL} \cap \text{Lifecycle}(\text{ACTIVE}) \setminus \text{ExplicitDeny}$$
3. **BR-SCOPE-03 (Deny Precedence - Từ chối tối thượng)**: `[DESIGN]` Nếu một hành động gặp bất kỳ điều kiện Deny nào (ví dụ: bị thu hồi grant, tài khoản bị khóa `SUSPENDED`, chuyển sang trạng thái `OFFBOARDING`, hoặc có bản ghi cấm tường minh), quyền truy cập phải bị từ chối ngay lập tức, bất kể người dùng có vai trò gì.

### 5.3. Ranh giới phản hồi lỗi: 401 Unauthorized vs. 403 Forbidden
1. **BR-ERR-01 (401 Unauthorized / Unauthenticated)**:
   - **Bản chất**: Hệ thống **không xác định được danh tính** của người gọi request.
   - **Các trường hợp kích hoạt**:
     + Thiếu Header `Authorization: Bearer <token>`.
     + Access Token bị sai định dạng, chữ ký không hợp lệ, hoặc đã hết hạn (`expired`).
     + JWT ID (`jti`) nằm trong danh sách thu hồi tức thời (Redis Blacklist).
     + Refresh Token không hợp lệ, đã bị thu hồi hoặc phát hiện tấn công tái sử dụng (Family Reuse Detection).
   - **Xử lý tại Client/FE**: Tự động chuyển hướng về trang Đăng nhập (`/signin`), xóa token lưu trữ tạm thời, hoặc kích hoạt tiến trình silent refresh.
2. **BR-ERR-02 (403 Forbidden / Unauthorized Scope)**:
   - **Bản chất**: Hệ thống **đã xác định được danh tính** người dùng, nhưng người dùng **không có quyền** thực hiện hành động trên phạm vi hoặc tài nguyên yêu cầu.
   - **Các trường hợp kích hoạt**:
     + Người dùng có role `MEMBER` cố tình gọi API tạo Team hoặc gán quyền.
     + Người dùng có role `TEAM_LEADER` nhưng chưa được cấp grant `project.create` cố tình gửi yêu cầu `POST /api/v1/projects`.
     + Grant `project.create` đã hết hạn (`expiresAt < now()`) hoặc đã bị thu hồi (`revokedAt !== null`).
     + Người dùng cố truy cập Project/Team mà mình không phải là thành viên hợp lệ (`project_memberships.status !== 'ACTIVE'`).
     + Bị chặn bởi quy tắc Deny Precedence hoặc Resource ACL.
   - **Xử lý tại Client/FE**: **Tuyệt đối không chuyển hướng về login** (tránh vòng lặp vô tận). Hiển thị trang hoặc thông báo thông cảm "403 - Bạn không có quyền truy cập tính năng này", hoặc hướng dẫn liên hệ Admin tổ chức để được cấp quyền.
3. **BR-ERR-03 (Authoritative Backend Boundary vs. FE UX-only)**:
   - **Backend Guard**: Là chốt chặn an ninh quyết định và bắt buộc (Authoritative Enforcement). Mọi request qua API Gateway / Controller đều phải đi qua Guard.
   - **Frontend Check**: Chỉ là giải pháp giao diện hỗ trợ trải nghiệm người dùng (UX gating). Việc ẩn nút "Tạo dự án" hoặc vô hiệu hóa form chỉ để tránh người dùng thao tác nhầm; không được xem là giải pháp an ninh thay thế Backend.

---

## 6. Requirement ➔ Evidence ➔ Implementation ➔ Gap Matrix

| Phân tầng kiến trúc | Yêu cầu nghiệp vụ / Kỹ thuật | Bằng chứng đặc tả (Specification Evidence) | Hiện trạng mã nguồn (Source Implementation) | Khoảng cách kỹ thuật (Technical Gap) |
| :--- | :--- | :--- | :--- | :--- |
| **Database: Roles** | Lưu trữ danh mục 3 Persistent Roles chuẩn | `02_ACTORS_ROLES...md:11`; `05_SECURITY...md:23` | `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:107-119` (Schema `roles`) | `[PARTIAL]` Schema đã có enum `ADMIN`, `TEAM_LEADER`, `MEMBER`. Chưa có script seed khởi tạo dữ liệu roles trong database. |
| **Database: Assignments** | Gán Role cho người dùng theo phạm vi | `02_ACTORS_ROLES...md:27` | `DATN-BE/.../mongodb.schemas.ts:120-134` (Schema `role_assignments`) | `[PARTIAL]` Index duy nhất là `{ organizationId: 1, projectId: 1, userId: 1 }`. Cần kiểm tra xử lý `projectId: null` đối với role cấp Organization (Admin). |
| **Database: Grants** | Quản lý việc cấp quyền `project.create` có thời hạn và lý do | `02_ACTORS_ROLES...md:13,84` | `DATN-BE/.../mongodb.schemas.ts:135-150` (Schema `organization_capability_grants`) | `[FACT]` Schema đầy đủ các trường `capability`, `grantedBy`, `reason`, `expiresAt`, `revokedAt`. Index `{ organizationId: 1, userId: 1, capability: 1, revokedAt: 1 }`. |
| **API Contract** | Endpoint cấp và thu hồi quyền `project.create` | `02_ACTORS_ROLES...md:80-84` | `DATN-BE/docs/openapi/iam-v1.openapi.json` | `[GAP]` Bản nháp OpenAPI chỉ mới có endpoint tạo dự án `POST /api/v1/projects`, hoàn toàn vắng bóng các endpoints quản lý capability grants (ví dụ `POST/DELETE /api/v1/iam/organizations/{orgId}/capability-grants`). |
| **Backend: Evaluator** | Service đánh giá quyền hiệu lực, kiểm tra thời hạn và Deny | `02_ACTORS_ROLES...md:84-85` | Không có trong `DATN-BE/src` | `[GAP]` Thiếu hoàn toàn `CapabilityEvaluatorService` và `AclService`. |
| **Backend: Guards** | NestJS Guard chặn 401 khi thiếu xác thực và 403 khi thiếu quyền | `02_ACTORS_ROLES...md:25`; `05_SECURITY...md:49` | Không có trong `DATN-BE/src` | `[GAP]` Thiếu `JwtAuthGuard` (ném 401), thiếu `RolesGuard`, `CapabilityGuard`, và `ProjectScopeGuard` (ném 403). |
| **Frontend: State** | Lưu trữ quyền hạn và danh sách capabilities của phiên làm việc | TailAdmin / Architecture baseline | `DATN-FE/src/stores/client-state.ts` | `[GAP]` Zustand store hiện tại chỉ chứa `activeProjectId`. Không có store quản lý User Profile, Roles, hoặc Capabilities. |
| **Frontend: UX Gating** | Ẩn/hiện nút "Tạo dự án" theo quyền `project.create` | `02_ACTORS_ROLES...md:25` | `DATN-FE/src` | `[GAP]` Chưa có component `<Can capability="project.create">` hoặc hook `useCapability()`. Form và giao diện hoàn toàn tĩnh theo TailAdmin. |
| **Integration / E2E** | Test tự động kiểm tra Deny, 401, 403, và phân quyền chéo | Quy trình CI/CD dự án DATN | `DATN-BE/test` | `[GAP]` Hiện tại chỉ có test cho endpoint `/health`. Chưa có test case nào cho RBAC/ABAC hoặc Evaluator. |

---

## 7. API / Data / Security Findings

### 7.1. Phát hiện về Data Model & Schema
1. **Index Xử lý Role cấp Tổ chức (`projectId: null`)**:
   - `role_assignments` có chỉ mục duy nhất compound: `{ organizationId: 1, projectId: 1, userId: 1 }`.
   - Với role `ADMIN` (phạm vi tổ chức, không thuộc project nào), trường `projectId` sẽ có giá trị `null` (hoặc `undefined`).
   - Trong MongoDB, giá trị `null` vẫn được tính vào unique index. Điều này đảm bảo một người dùng chỉ có tối đa một vai trò cấp tổ chức trong một organization cụ thể (đúng với thiết kế logic). Cần xác nhận quy ước lưu là `null` hay không truyền trường (sparse/partial index).
2. **Khai báo Capability Enum trong Mongoose**:
   - Trường `capability` trong `organization_capability_grants` được cấu hình hardcoded enum: `['project.create']`.
   - Trong khi đó, tài liệu chuẩn `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 6) đề cập đến 20 mã quyền tối thiểu. Điều này phản ánh rõ định hướng MVP: **Chỉ có `project.create` là capability độc lập cấp tổ chức được cấp phát riêng qua bảng này**; các mã quyền còn lại được suy ra từ vai trò (`Role`) và tư cách thành viên (`Membership`).

### 7.2. Phát hiện về API Contract (OpenAPI vs. Specification)
1. **Thiếu vắng Endpoint quản lý Grants trong OpenAPI**:
   - Tài liệu OpenAPI `DATN-BE/docs/openapi/iam-v1.openapi.json` đã mô tả nghiệp vụ tại endpoint tạo project:
     `"description": "Requires organization Admin or an active project.create capability grant."`
     và khai báo mã lỗi phản hồi `403 Forbidden`.
   - Tuy nhiên, trong toàn bộ danh sách `paths` của OpenAPI, **không hề có endpoint nào để Admin thực hiện cấp, thu hồi hoặc liệt kê các grants này** (ví dụ: `/api/v1/iam/capability-grants`). Đây là một lỗ hổng trong contract cần bổ sung trước khi triển khai.

### 7.3. Phát hiện về An ninh & Nguy cơ Leo thang đặc quyền (Security & Privilege Escalation)
1. **Nguy cơ Bypass qua Client State**:
   - Nếu Frontend chỉ dựa vào trạng thái local lưu trong browser để quyết định cho phép gọi API, kẻ tấn công có thể chỉnh sửa bộ nhớ hoặc gửi request trực tiếp bằng công cụ (Postman/Curl).
   - **Khẳng định bắt buộc**: Backend Guard bắt buộc phải thực hiện kiểm tra DB/Cache mỗi khi tiếp nhận request thực thi `POST /api/v1/projects`, kiểm tra đồng thời:
     + User có role `ADMIN` trong `role_assignments` (scope Organization), HOẶC:
     + User có bản ghi hợp lệ trong `organization_capability_grants` với `capability = 'project.create'`, `revokedAt == null`, và `(expiresAt == null || expiresAt > now())`.
2. **Kịch bản Thu hồi tức thời (Revocation Invalidation)**:
   - Khi Admin bấm thu hồi quyền `project.create` (`revokedAt = new Date()`), nếu quyền được cache trong Access Token JWT (stateless), Team Leader vẫn có thể tạo dự án cho đến khi Access Token hết hạn (thời gian sống token có thể là 15 phút).
   - **Giải pháp thiết kế**: Cần có cơ chế xác thực quyền tạo dự án trực tiếp từ cơ sở dữ liệu hoặc thông qua Redis Cache với cơ chế xóa khóa (cache invalidation) ngay khi có sự kiện thu hồi.

---

## 8. Frontend / Backend Mismatches

| Hạng mục so sánh | Backend (`DATN-BE`) | Frontend (`DATN-FE`) | Đánh giá sai lệch (Mismatch) |
| :--- | :--- | :--- | :--- |
| **Xử lý mã trạng thái lỗi HTTP** | OpenAPI định nghĩa `401 Unauthorized` và `403 Forbidden` | `src/lib/api-client.ts` chỉ bắt `!response.ok` và ném exception dạng chuỗi thông thường | **Nghiêm trọng**: FE không thể phân biệt được lỗi hết phiên đăng nhập (cần redirect signin) với lỗi không đủ quyền (cần báo Access Denied). |
| **Context & State danh tính** | Model lưu `userId`, `organizationId`, `roleCode`, `capability` | Zustand store (`client-state.ts`) chỉ quản lý mỗi `activeProjectId` | **Thiếu hụt**: FE không có thông tin về vai trò của user đăng nhập để phục vụ render giao diện có điều kiện. |
| **Header chuyển tiếp qua BFF** | Backend có thể yêu cầu thông tin định danh/ngữ cảnh qua Header | `src/lib/bff-proxy.ts` chỉ whitelist các headers: `accept`, `authorization`, `content-type`, `cookie`, `x-request-id` | **Khớp lệnh một phần**: Token được truyền qua `authorization` hoặc `cookie`, tuy nhiên các headers mở rộng ngữ cảnh (như tenant context) chưa được chuyển tiếp. |
| **Kiểm soát tạo dự án (Project Creation UI)** | Yêu cầu Admin hoặc Team Leader có grant `project.create` | Chưa có form hoặc trang tạo dự án; template tĩnh chỉ có trang tổng quan Admin | **Chưa triển khai**: Giao diện tạo dự án chưa tồn tại trên FE. |

---

## 9. Dependencies & Blockers

1. **Phụ thuộc vào JWT Claims Structure & Auth Service**:
   - Evaluator cần biết danh tính người gọi qua `request.user`. Do đó, module phân quyền phụ thuộc trực tiếp vào việc hoàn thiện module `Auth` (xác thực chữ ký JWT và trích xuất payload vào `request.user`).
2. **Phụ thuộc vào Organization Context (DATN-15)**:
   - Phân quyền cấp tổ chức và dự án yêu cầu phải xác định được `organizationId` của request hiện hành để đối chiếu trong bảng `role_assignments` và `organization_capability_grants`.
3. **Phụ thuộc vào Redis Infrastructure**:
   - Cơ chế kiểm tra Blacklist Token (phục vụ 401 khi user logout/bị khóa) và cơ chế cache kết quả kiểm tra quyền (phục vụ hiệu năng cao <1ms) phụ thuộc vào kết nối hạ tầng Redis.

---

## 10. UNKNOWN & DECISION REQUIRED Register

Tuân thủ nguyên tắc không tự quyết định các vấn đề kiến trúc chưa được phê chuẩn (`Do not decide an unapproved matrix`), các nội dung sau được ghi nhận thành sổ bộ quyết định:

- `[DECISION REQUIRED]` **DR-01: Hành vi phản hồi khi truy cập tài nguyên ngoài phạm vi (Cross-Scope): Trả về 403 Forbidden hay 404 Not Found?**
  - *Phương án A*: Trả về `403 Forbidden` (Minh bạch về lý do lỗi, dễ debug, nhưng có nguy cơ lộ sự tồn tại của tài nguyên qua kỹ thuật dò ID - Resource ID enumeration).
  - *Phương án B (Khuyến nghị an ninh)*: Trả về `404 Not Found` đối với tài nguyên nằm ngoài tổ chức hoặc ngoài dự án được cấp quyền (như thể tài nguyên không hề tồn tại), và chỉ trả về `403 Forbidden` cho các hành động bị chặn thao tác trên tài nguyên mà người dùng đã nhìn thấy hợp lệ.
- `[DECISION REQUIRED]` **DR-02: Phê duyệt Ma trận Quyền chi tiết (Detailed Permission Matrix Approval)**
  - Tài liệu `02_ACTORS_ROLES_AND_PERMISSIONS.md` (Mục 5) mới cung cấp ma trận cơ bản cho 10 hành động chính. Cần Team Lead phê duyệt ma trận ánh xạ chi tiết cho toàn bộ 20 permission codes trước khi code logic nghiệp vụ chi tiết.
- `[UNKNOWN]` **UN-01: Vị trí lưu trữ quy tắc cấm tường minh (Explicit Deny Storage)**
  - Công thức tính quyền yêu cầu loại trừ `ExplicitDeny`. Hiện tại schema Mongoose chưa có bảng lưu trữ các rule Deny cá nhân/nhóm. Cần làm rõ: Liệu MVP có hỗ trợ cấu hình Deny động trong database, hay Deny chỉ là hardcoded business logic trong code (ví dụ: tài khoản bị khóa thì cấm mọi quyền)?
- `[UNKNOWN]` **UN-02: Vòng đời và Gia hạn của Capability Grant**
  - Khi một grant `project.create` hết hạn (`expiresAt`), hệ thống tự động đánh dấu thu hồi qua job chạy ngầm, hay chỉ kiểm tra thụ động qua câu truy vấn (Query check: `expiresAt > new Date()`) tại thời điểm gọi API?

---

## 11. Implementation Breakdown Recommendation

Theo quy trình bắt buộc tại [AI_WORKFLOW.md](../../AI_WORKFLOW.md), khi bước vào giai đoạn hiện thực hóa (Implementation Phase), task này phải được chia nhỏ và tách biệt thành các PR độc lập theo thứ tự:

```text
[ 1. DATABASE PR ] ────────► [ 2. BACKEND PR ] ────────► [ 3. FRONTEND PR ]
 (Schema & Seeds)            (Guards & Evaluator)        (UX Gating & Errors)
```

### Bước 1: Database Branch & PR (`feat/Phuc-roles-capabilities-db`)
- **Phạm vi**:
  + Rà soát và hoàn thiện schema `role_assignments` và `organization_capability_grants` trong `DATN-BE`.
  + Đảm bảo compound unique index trên `role_assignments` tương thích với giá trị `projectId: null` cho Admin cấp tổ chức.
  + Tạo database seed script/migration để chèn 3 system roles mặc định: `ADMIN`, `TEAM_LEADER`, `MEMBER`.
- **Tiêu chí nghiệm thu**: Seed chạy thành công, index được build đầy đủ trong MongoDB.

### Bước 2: Backend Branch & PR (`feat/Phuc-roles-capabilities-evaluator-be-api`)
- **Phạm vi**:
  + Xây dựng `JwtAuthGuard`: Kiểm tra Bearer token, giải mã payload, kiểm tra Redis blacklist. Ném `401 Unauthorized` nếu vi phạm.
  + Xây dựng `CapabilityEvaluatorService`: Cài đặt logic kiểm tra quyền, thời hạn hiệu lực, và quy tắc ưu tiên từ chối (Deny Precedence).
  + Xây dựng Decorators và Guards:
    * `@RequireCapability('project.create')` kết hợp `CapabilityGuard`.
    * `@Roles('ADMIN')` kết hợp `RolesGuard`.
    * Áp dụng bảo vệ route `POST /api/v1/projects`: Ném `403 Forbidden` nếu người dùng không phải Admin và không có grant hợp lệ.
  + Bổ sung API endpoints phục vụ Admin cấp/thu hồi capability grant.
  + Viết unit test & integration test bao phủ các kịch bản: Thiếu token (401), Sai quyền (403), Quyền hết hạn (403), Quyền hợp lệ (201).
- **Tiêu chí nghiệm thu**: 100% tests pass, các mã lỗi 401 và 403 được trả về chính xác theo OpenAPI contract.

### Bước 3: Frontend Branch & PR (`feat/Phuc-roles-capabilities-fe-ui`)
- **Phạm vi**:
  + Cập nhật `api-client.ts`: Bắt mã trạng thái phản hồi HTTP. Khi gặp `401` ➔ chuyển hướng về `/signin`; khi gặp `403` ➔ trả về lỗi phân quyền tường minh.
  + Bổ sung User Identity & Capability State vào Zustand store hoặc React Context.
  + Tạo tiện ích UX-gating: Component `<Can capability="...">` và hook `useCanCapability(...)`.
  + Gắn điều kiện hiển thị nút "Tạo dự án mới" trên giao diện (chỉ hiển thị nếu user là Admin hoặc có capability `project.create`).
  + Xây dựng trang thông báo lỗi `403 Forbidden / Access Denied` thân thiện.
- **Tiêu chí nghiệm thu**: Người dùng không có quyền sẽ không thấy nút tạo dự án; nếu cố tình vào route sẽ nhận thông báo lỗi 403 rõ ràng, không bị crash hoặc loop redirect.
