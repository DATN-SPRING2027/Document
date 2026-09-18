# DATN — Quy trình bắt buộc cho AI coding agent

Tài liệu này là nguồn chuẩn cho Codex, Antigravity/Gemini, Claude, Copilot và
các AI coding agent khác khi làm việc với dự án DATN. Đây không phải dự án
TAMI ERP. Không được suy luận domain, module, đường dẫn hoặc architecture của
TAMI cho DATN. Nếu hướng dẫn chung của
công cụ xung đột với tài liệu này, tài liệu này được ưu tiên trong phạm vi dự
án. Các quy tắc an toàn cấp hệ thống của công cụ vẫn luôn được áp dụng.

## 1. Nguyên tắc không được vi phạm

1. Mỗi task mới phải dùng một branch mới, được tạo từ phiên bản mới nhất của
   `origin/main`. Không dùng lại branch của task cũ.
2. Không code trực tiếp, push trực tiếp hoặc force-push lên `main`.
3. Backend, frontend và database phải dùng branch/PR riêng. Một branch chỉ phục
   vụ một mục đích review.
4. Feature branch chỉ tạo Pull Request vào `main`.
5. AI được chạy `git push` cho branch của task hiện tại sau khi đã kiểm
   tra và commit đúng phạm vi. Không push trực tiếp hoặc force-push lên `main`;
   không tự approve, merge, auto-merge hoặc bypass branch protection.
6. Mọi thay đổi schema/model/collection/field/type/default/enum/index/reference/
   relationship/validation/unique constraint đều là database change và phải có
   DB branch + DB PR riêng.
7. Không sửa, xóa, đổi tên hoặc ghi đè migration đã commit hoặc đã chạy ở môi
   trường dùng chung. Mỗi thay đổi mới phải có migration/script mới.
8. Không hardcode secret, token, password, database URL, API URL theo môi trường
   hoặc config nhạy cảm. Không commit file `.env`.
9. Luôn theo architecture và pattern đang tồn tại trong source production;
   không tự tạo một kiến trúc song song khi chưa được phê duyệt.
10. Chỉ báo task hoàn tất khi các kiểm tra liên quan đã chạy thành công và kết
    quả bàn giao nêu rõ branch, test, database impact và bước thủ công còn lại.

## 2. Bắt đầu task và đặt tên branch

### 2.1. Kiểm tra trước khi chỉnh sửa

Trước khi thay đổi file, AI phải:

1. Đọc `AGENTS.md`, tài liệu architecture và tài liệu task/Jira liên quan.
2. Chạy `git status --short --branch` để phát hiện thay đổi có sẵn của người dùng.
3. Chạy `git fetch origin`, kiểm tra `origin/main` tồn tại và không có lỗi fetch.
4. Không tự ý stash, reset, checkout bỏ, ghi đè hoặc commit thay đổi của người khác.
5. Tạo branch mới trực tiếp từ `origin/main`, không dựa vào một local `main` cũ.

Lệnh chuẩn:

```bash
git fetch origin
git switch --create <branch-name> origin/main
```

Nếu Git/repository chưa được khởi tạo, remote `origin` chưa cấu hình,
`origin/main` không tồn tại, branch đích đã tồn tại, hoặc working tree có thay
đổi gây xung đột, AI phải dừng trước khi chỉnh sửa và báo chính xác trở ngại.
Không tự tạo lịch sử Git hoặc tự chọn một base branch khác.

### 2.2. Quy ước tên branch

- Backend: `feat/<Tên>-<tên-task>-be-api`
- Frontend: `feat/<Tên>-<tên-task>-fe-ui`
- Database: `feat/<Tên>-<tên-task>-db`

Ví dụ:

```text
feat/Thang-management-dashboard-be-api
feat/Thang-management-dashboard-fe-ui
feat/Thang-user-role-db
```

`<Tên>` là tên người thực hiện/owner đã biết từ task hoặc do người dùng cung
cấp; AI không được tự bịa. `<tên-task>` dùng kebab-case ngắn gọn. Với bug/chore,
giữ hậu tố phạm vi tương ứng nhưng dùng prefix `fix/` hoặc `chore/` khi team/Jira
yêu cầu.

## 3. Tách phạm vi branch và Pull Request

Một task có nhiều lớp được tách theo thứ tự sau:

1. **DB PR**: entity/schema/model, migration mới, index và data migration.
2. **BE PR**: controller, service, API, DTO/validation và business logic.
3. **FE PR**: UI, API integration, state, form và table.

Entity/schema và migration tương ứng phải nằm cùng DB branch/PR để database
contract được review đầy đủ. Không gộp logic ứng dụng hoặc UI không liên quan
vào DB PR. Nếu BE/FE phụ thuộc database contract mới, chờ DB PR được teammate
review và merge vào `main`, sau đó tạo hoặc cập nhật branch phụ thuộc từ
`origin/main` theo quy trình của team.

## 4. Database, schema và migration

### 4.1. Phân loại database change

Các thay đổi sau luôn được xem là database change: Mongoose schema, ORM entity,
model, collection/table, field/column, data type, default, enum, index,
reference/relationship, validation, unique constraint, migration và database
script.

AI không được xem việc “chỉ thêm một field” là thay đổi backend thông thường.
Trước khi triển khai, phải xác định backward compatibility, data loss risk,
rollback/recovery và ảnh hưởng tới dữ liệu hiện có.

### 4.2. Dữ liệu cũ

Nếu DATN sử dụng MongoDB, cần nhớ MongoDB không bắt buộc migration ở tầng
engine, nhưng thay đổi schema ảnh hưởng document hiện có vẫn phải có
migration/script idempotent để backfill hoặc chuyển đổi dữ liệu. Ví dụ thêm
`status: "active"` phải xử lý các document chưa có `status`; không được giả
định sửa schema sẽ tự cập nhật dữ liệu cũ.

Migration/script phải:

- có thể kiểm tra trên môi trường phù hợp trước khi áp dụng;
- không phá hoặc âm thầm làm mất dữ liệu cũ;
- có điều kiện để không sửa lại dữ liệu đã đúng;
- là file mới, không chỉnh migration lịch sử;
- ghi rõ cách chạy, cách xác minh và phương án phục hồi khi cần.

### 4.3. Thông báo team bắt buộc

Khi có database change, AI phải chuẩn bị hoặc gửi (chỉ khi có quyền và người
dùng đã yêu cầu) thông báo theo mẫu:

```text
[DATABASE CHANGE]

Collection/Entity: <tên>

Thay đổi:
- <field/index/reference/type/default/validation đã đổi>

Ảnh hưởng dữ liệu:
- <ảnh hưởng tới dữ liệu cũ hoặc "Không">

Migration:
- <tên script, cách xử lý hoặc "Không cần" kèm lý do>

PR type: Database
PR: <link PR>
```

Nếu không có quyền gửi group chat, ghi rõ `Pending team notification` và đưa
nguyên văn thông báo để người dùng gửi. Không được tuyên bố đã gửi khi chưa có
bằng chứng.

## 5. Quy tắc triển khai backend

Chỉ áp dụng các ví dụ Node.js/Mongoose dưới đây khi source DATN thực sự sử dụng
stack đó. Với stack khác, giữ nguyên nguyên tắc phân lớp, validation, query có
kiểm soát và error handling nhưng follow framework/pattern hiện tại của DATN.

1. Đọc source production và feature gần nhất trước khi tạo file mới.
2. Giữ luồng trách nhiệm theo architecture hiện tại, thông thường:
   `Route/Controller -> Service -> Model/Repository -> Database`.
3. Controller xử lý HTTP; service xử lý business logic. Không dồn toàn bộ logic
   vào controller.
4. Tất cả input từ client phải được validate: body, params, query, ObjectId/ID,
   enum, required field và data type. Không truyền thẳng `req.body` vào model.
5. Query phải có phạm vi: pagination cho danh sách lớn, chỉ select field cần
   thiết, dùng index khi cần, hạn chế deep populate, tránh N+1 và tránh quét toàn
   collection không cần thiết.
6. Có error handling nhất quán; không log dữ liệu nhạy cảm.
7. Không tạo `handlers/`, `managers/`, `processors/` hoặc abstraction mới nếu
   source hiện tại không dùng và chưa có quyết định architecture được duyệt.

## 6. Quy tắc triển khai frontend

Chỉ áp dụng các ví dụ React/TailAdmin dưới đây khi source hoặc tài liệu được
duyệt của DATN xác nhận đang dùng các công nghệ đó.

1. Nếu dùng React, theo đúng structure hiện tại cho pages, components, hooks,
   services, API, state, types, routing và error handling.
2. Nếu DATN dùng TailAdmin, Admin UI phải bám sát TailAdmin về sidebar, header,
   card, table, form, modal, button, badge, typography, spacing và responsive,
   trừ khi task có thiết kế được duyệt khác.
3. Trước khi tạo component mới, áp dụng thứ tự: **Reuse -> Extend -> Create**.
   Kiểm tra UI kit hiện tại, shared components và page/component tương tự trước.
4. Dùng API client/service/hook hiện có. Không gọi `fetch` trực tiếp trong
   component nếu project đã có service/API layer mà không có lý do được ghi rõ.
5. Màn hình lấy dữ liệu từ API phải xử lý tối thiểu: Loading, Success, Empty và Error.
6. Kiểm tra responsive, console error, API integration, form validation và
   accessibility phù hợp với phạm vi task.

## 7. Kiểm tra, commit và push

### 7.1. Trước khi commit

Luôn xem `git status`, `git diff` và chỉ stage file thuộc task. Không mặc định
dùng `git add .` khi working tree chứa thay đổi ngoài phạm vi.

Backend tối thiểu kiểm tra: syntax/typecheck, validation, error handling, test
liên quan, build/lint, không có secret hoặc log nhạy cảm.

Frontend tối thiểu kiểm tra: typecheck, lint, test/build, UI theo design,
responsive, console, API integration và bốn UI states.

Database tối thiểu kiểm tra: schema/entity và migration đồng bộ, migration mới
chạy được, dữ liệu cũ không bị phá, idempotency/backward compatibility và mẫu
thông báo team đã chuẩn bị.

### 7.2. Commit

Commit phải atomic và dùng Conventional Commits, ví dụ:

```text
feat: add management dashboard api
feat: add management dashboard ui
feat: add user status schema migration
```

AI chỉ tạo commit khi người dùng yêu cầu hoặc workflow của task đã trao quyền
rõ ràng. Không stage/commit thay đổi không liên quan.

### 7.3. Push feature branch

Sau khi kiểm tra và commit đúng phạm vi, AI được push branch của task hiện
tại lên `origin` và có thể mở Pull Request vào `main` khi task yêu cầu:

```bash
git push -u origin <branch-name>
```

## 8. Pull Request, Jira và code review

Sau khi branch được push, PR phải có base là `main` và gồm:

- tên task và Jira ticket;
- nội dung đã làm;
- API/screen bị ảnh hưởng;
- database change hoặc xác nhận không có;
- cách test và kết quả test;
- screenshot với thay đổi frontend;
- migration/data impact khi có.

Sau khi mở PR:

1. Cung cấp link PR để dán vào Jira ticket tương ứng.
2. Tag reviewer chỉ khi danh tính đã biết; không tự bịa tài khoản.
3. Không tự approve hoặc merge. Chờ code review, đủ approve, không còn Request
   Changes/conflict, CI/build/test thành công và không có regression đã biết.
4. Xử lý comment sau khi người dùng phê duyệt phạm vi sửa; thông báo reviewer
   kiểm tra lại khi cần.

Review phải bao phủ theo phạm vi:

- Backend: architecture, logic, security, validation, error handling,
  performance và database query.
- Frontend: UI/UX, component structure, state, API handling, reuse, responsive
  và accessibility.
- Database: schema design, index, migration, backward compatibility và data
  loss risk.

## 9. Luồng chuẩn

```text
Nhận Jira task
-> đọc rules, architecture và source hiện tại
-> fetch origin
-> tạo branch mới từ origin/main
-> triển khai đúng phạm vi
-> test local + kiểm tra diff
-> commit atomic khi được phép
-> AI hoặc người thực hiện push feature branch
-> mở PR feature -> main
-> dán link PR vào Jira + thông báo team khi có DB change
-> tag reviewer
-> sửa comment được duyệt và kiểm tra lại
-> teammate approve
-> teammate được ủy quyền merge vào main
```

## 10. Checklist bàn giao của AI

Mỗi lần bàn giao, AI phải nêu:

- branch hiện tại và base branch;
- file/phạm vi đã thay đổi;
- test/lint/typecheck/build đã chạy và kết quả;
- database change: Có/Không; migration: Có/Không; data impact;
- commit đã tạo hay chưa;
- trạng thái push và xác nhận chưa merge;
- lệnh push thủ công nếu branch sẵn sàng nhưng chưa được push;
- PR/Jira/team notification còn chờ người dùng thực hiện.
