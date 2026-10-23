# Admin — quản lý người dùng

## Nguồn chuẩn và phạm vi

Ngày 2026-10-21 (Asia/Ho_Chi_Minh), người dùng xác nhận dùng OpenAPI hiện tại
của BE làm chuẩn và cập nhật tài liệu cũ cho khớp. Đây là quyết định cho phạm vi
quản lý người dùng, không mở rộng quyền quản trị các domain khác.

Base đã kiểm tra: FE `3fda57a`, BE `5eea11b`, Document `68b8894`.
Hợp đồng: `DATN-BE/docs/openapi/iam-v1.openapi.json`.
Triển khai: `PlatformUsersDirectory.tsx`, `usePlatformOperations.ts`,
`platform.controller.ts`, `platform-administration.repository.ts`.

Admin là nhãn hiển thị của `PLATFORM_OPERATOR`, thuộc context `PLATFORM`.
Organization role `ADMIN` hiển thị Manager và không cấp quyền quản trị hệ thống.
Không suy quyền từ nhãn: backend kiểm tra user ACTIVE và từng assignment PLATFORM
hiện hành. Không wildcard, không cấp quyền tenant content từ quyền Platform.

## Chức năng và nghiệm thu

Mọi đường dẫn bên dưới có prefix `/api/v1/iam/platform`.

| Chức năng | Endpoint | Quyền chính xác | Hành vi nghiệm thu |
|---|---|---|---|
| Tìm và xem tài khoản | `GET /users`, `GET /users/{userId}` | `platform.users.account.read` | Search, lọc ACTIVE/SUSPENDED/PENDING_INVITE/ARCHIVED, phân trang; chỉ projection an toàn |
| Sửa hồ sơ | `PATCH /users/{userId}` | `platform.users.account.manage` | Chỉ fullName/avatarUrl; không đổi email, mật khẩu, role hay permission; gửi expectedUpdatedAt |
| Đổi trạng thái | `PATCH /users/{userId}/status` | `platform.users.account.manage` | ACTIVE ↔ SUSPENDED; không tự đổi trạng thái bản thân; không suspend Manager cuối cùng đủ điều kiện của tổ chức |
| Archive | `POST /users/{userId}/archive` | `platform.users.account.manage` | ACTIVE/SUSPENDED → archived + SUSPENDED; xác nhận và acknowledgment; không tự archive; giữ user/membership/audit; thu hồi refresh sessions |
| Restore | `POST /users/{userId}/restore` | `platform.users.account.manage` | Chỉ archived + SUSPENDED; xóa archive marker, vẫn SUSPENDED; không phục hồi sessions; muốn đăng nhập phải Reactivate riêng |
| Xem tổ chức của user | `GET /users/{userId}/organizations` | `platform.users.account.read` | Phân trang metadata và membership/role; không truy cập nội dung tổ chức |
| Xem phiên đăng nhập | `GET /users/{userId}/sessions`, `GET /users/{userId}/sessions/{sessionId}` | `platform.sessions.session.read` | Metadata an toàn, phân trang, detail; thiếu quyền hiển thị thông báo, không coi là danh sách rỗng |

Session revoke đã có endpoint riêng với `platform.sessions.session.manage`.
FE không cho thu hồi phiên của chính operator vì API chưa xác định phiên browser
hiện tại. Đây không phải quyền ngầm từ account.manage.

## Trạng thái, lỗi và bảo toàn dữ liệu

- Các lệnh ghi dùng cookie/CSRF qua API client hiện có; không đưa token vào localStorage.
- CAS `expectedUpdatedAt` chặn ghi đè dữ liệu cũ. `409` yêu cầu đọc lại/review;
  mutation không tự retry và không tự thay CAS để ghi đè quyết định mới hơn.
- Backend kiểm tra lại actor/authority trong transaction. User mutation và audit
  cùng commit; audit lỗi thì rollback. Suspend/archive thu hồi refresh sessions.
- Restore giữ nguyên membership và sessions đã revoked; không đồng nghĩa với
  reactivation, cấp role, cấp authority hay mở quyền tenant content.
- FE xử lý loading, empty, lỗi mạng/refetch, denied, pending mutation và thông báo
  thành công. Không hiển thị raw error, credential, token hash hoặc audit payload.
- Dùng TailAdmin/theme hiện có, logical CSS cho RTL, focus khi mở/đóng dialog và
  thông báo thiếu quyền được dịch theo locale có trong source (`en.json`).

## Thay đổi của task này

Source main đã triển khai các chức năng trên. Task này bổ sung thông báo thiếu
quyền xem sessions, kiểm thử FE restore (CSRF/CAS, safe projection, response sai,
conflict không retry), và kiểm thử Mongo restore (giữ SUSPENDED/membership/session,
audit một lần, chống replay CAS và rollback khi audit thất bại).

Không sửa schema, index hay migration; không chạy migration hoặc sửa dữ liệu
môi trường triển khai. Kiểm thử Mongo dùng replica set tạm do test tạo và dọn.
Kết quả xác minh ngày 2026-10-21:

| Kiểm tra | Kết quả |
|---|---|
| FE lint / TypeScript | Pass |
| FE toàn bộ Vitest | 85 file, 689 test pass |
| FE production build | Pass; compile trong sandbox bị đứng, chạy lại `npm run build` ngoài sandbox pass |
| BE Platform/API/authorization/Mongo tập trung | 5 suite, 94 test pass |
| BE `npm run check` | Pass ở lần chạy lại; lint, typecheck, safety tests, unit, E2E và build |
| BE toàn bộ unit | 120 suite pass, 14 skipped; 1.266 test pass, 135 skipped |
| BE E2E | 14 suite pass, 2 skipped; 82 test pass, 4 skipped |
| Thử đảo điều kiện denied sessions | Test thất bại như mong đợi; đã khôi phục source, chạy lại 47 test liên quan pass |
| `git diff --check` | Pass ở cả ba repo |

Lần chạy BE đầy đủ đầu tiên có một failure trong
`organization-membership-read.repository.spec.ts`: expected 503, nhận 400.
Chạy riêng cả 52 test trong file pass và chạy lại toàn bộ check pass. File này
không thay đổi trong task; ghi nhận test không ổn định, không che giấu failure đầu.
Test tự động không thay thế bằng chứng browser/live authenticated end-to-end;
task này chưa xác minh luồng qua browser với tài khoản thật.

Review cuối theo `code-review-and-quality`: không có finding chặn trong diff
của task. Không thay API contract, schema hay authorization backend; test Mongo
chứng minh các invariant của restore trên replica set tạm.

Các branch riêng: FE `feat/Tien-platform-user-management-verification-fe-ui`,
BE `feat/Tien-platform-user-management-verification-be-api`,
Docs `docs/Tien-platform-user-management-contract`; base `origin/main`.
Không tạo commit/push/merge trong bước hoàn thiện local này.
