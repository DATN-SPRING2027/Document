# DATN-97 — D-05 Task Core BE: gói yêu cầu quyết định

- **Revision:** D05-DR1 (18/10/2026, Asia/Bangkok).
- **Trạng thái tài liệu:** YÊU CẦU QUYẾT ĐỊNH — PROPOSED, NOT APPROVED. Tài liệu này không phải bản phê duyệt, không phải đánh giá độc lập và không chứa mã ứng dụng.
- **Soạn bởi:** Claude (AI) theo yêu cầu của Nguyen Hong Phuc, chủ task DATN-97. Không có người duyệt nào được chỉ định hay suy ra trong tài liệu này.
- **Quy ước đánh số:** "doc N" là số thứ tự file trong thư mục này; "PR #N" là Pull Request GitHub (nêu rõ repository khi cần); "D-03 O*n*" là oracle của contract delta D-03 ([doc 21](21-task-v1-d03-contract-delta.md)); "D-13 O*n*" là oracle của [doc 23](23-task-v1-api-lifecycle-decisions-d13.md) §4.2. Hai hệ số O này khác nhau.
- **Jira:** [DATN-97](https://trankimthang0207.atlassian.net/browse/DATN-97) D-05 Task Core BE. Subtask [DATN-128](https://trankimthang0207.atlassian.net/browse/DATN-128) đến [DATN-133](https://trankimthang0207.atlassian.net/browse/DATN-133). Theo ghi nhận của chủ task ngày 18/10/2026: DATN-97 và các subtask đang In Progress; Jira `is blocked by` DATN-95, DATN-96, DATN-373 đều hiển thị Done. Người soạn chưa tự kiểm lại Jira khi viết revision này. [Doc 23](23-task-v1-api-lifecycle-decisions-d13.md) §4.1 và §5 (cùng ngày) ghi DATN-97 và DATN-373 là `To Do` và DATN-375 (authority disposition) là OPEN; trạng thái Jira thay đổi độc lập và không đóng gate quyết định (xem "Ranh giới phê duyệt"). Doc 23 không liệt kê DATN-96 trong dependency trace.
- **Nguồn nền:**
  - [D-13 R6 (doc 23, merged qua Document PR #43)](23-task-v1-api-lifecycle-decisions-d13.md): contract Task V1, mọi thao tác công khai đang `NOT APPROVED / DISABLED`.
  - [Approval record doc 20](20-task-v1-contract-approval-record.md) và [doc 22](22-task-v1-d03-delta-approval-record.md): phần đã duyệt (lát cắt riêng tư D-03).
  - [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md), [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md).
  - DATN-BE `origin/main` tại `7d3e65a`: `AGENTS.md`, DATN-BE PR #31 (D-03), PR #45 (D-04), PR #52 (test D-13 O0).
- **Ranh giới phê duyệt:** theo phần "Review Authority Framework" ở đầu doc 23 (dòng 9) và §3.1 của doc 23, trạng thái merge của PR và trạng thái Jira Done không phải bằng chứng phê duyệt. Một quyết định chỉ được chấp nhận khi ghi rõ authority, revision này và phạm vi quyết định.

---

## 1. Kết luận ngắn

1. DATN-97 yêu cầu API create/list/detail "khớp chính xác contract đã duyệt". Contract công khai hiện **chưa được duyệt**: D-13 R6 chỉ ghi nhận lát cắt riêng tư D-03 là `APPROVED` (7 trường; create là mutation duy nhất, kèm các primitive đọc; không có route công khai).
2. `AGENTS.md` của BE đang cấm thêm controller, route hoặc public business API trước khi các gate Product/Security được ghi nhận, và giữ ma trận D-05 ở trạng thái DENY.
3. Phần nền đã có trên `origin/main`: repository D-03, runtime Task ở trạng thái dormant, authorization boundary mặc định từ chối, Gateway client dormant, và bộ test tương ứng (§2).
4. Vì vậy phần còn thiếu của DATN-97 là **quyết định**, không phải thêm mã. Tài liệu này đề nghị thu hẹp DATN-97 vào lát cắt 7 trường và xin 8 quyết định (§3) để mở khóa DATN-129 đến DATN-133 (và chốt phạm vi DATN-128).
5. Thay đổi database: **không có cho riêng lát cắt 7 trường**, vì nó dùng lại schema, index và collection của D-03. Điều này chỉ đúng nếu (i) DR-7(c) loại `Idempotency-Key` khỏi lát cắt và (ii) DR-3 không đòi một kho replay/dedupe mới. Nếu một trong hai không đúng, collection hoặc index mới là database change theo `AI_WORKFLOW.md` §4.1 và cần DB PR riêng, báo team và đối chiếu ADR-003.
6. Lưu ý dữ liệu: lát cắt 7 trường không có `status`. Theo [doc 22](22-task-v1-d03-delta-approval-record.md) §4, khi sau này đưa lifecycle vào thì cần contract trạng thái khởi tạo và migration cho các bản ghi gốc đã tạo.

## 2. Đối chiếu subtask với hiện trạng

Nguồn: DATN-BE `origin/main` `7d3e65a`. Chưa có route hay controller Task nào trong `AppModule`/`GatewayModule`; `TaskRuntimeModule` chỉ đăng ký `TaskHealthController`.

| Subtask | Đã có trên `origin/main` | Khoảng trống còn lại | Bị chặn bởi |
|---|---|---|---|
| DATN-128 Repository | `TaskDataRepository` (`src/services/task/infrastructure/mongodb/task-data.repository.ts`): `create`, `getById(projectId, taskId)`, `listByProject(projectId, {limit, afterId})`, `listHistory`. Database `continuum_task`, collection `tasks` và `task_events`, schema đóng, index theo query. Test D-03 O1–O13 trong `task-data.repository.mongodb.spec.ts`. | Hoàn thành cho 7 trường nếu DR-1 = A và DR-6 = A. Nếu DR-6 = B thì cần thêm truy vấn đếm và ngữ nghĩa snapshot. Trường mở rộng (status, priority, assignee, team, dueDate, tags, description), filter và sort chưa được duyệt nên không thêm. | DR-1, DR-6 |
| DATN-129 Create endpoint | `create` chỉ nhận `{ title }`, từ chối trường lạ, trả `REJECTED / ABORTED / COMMITTED / UNCERTAIN`. `operationId` do repository sinh (UUID v4), không nhận từ caller. | Chưa có handler, DTO công khai, ánh xạ kết quả repository sang HTTP (đặc biệt `ABORTED` và `UNCERTAIN`), idempotency. | DR-1, DR-2, DR-3, DR-4, DR-5, DR-7, DR-8 |
| DATN-130 List | `listByProject` giới hạn `limit` 1–100, cursor `afterId`, sắp xếp `_id` tăng dần. Không có filter. | Chưa có handler. Contract đề xuất dùng `page/limit/total`, filter và sort khác với repository. List cũng cần verifier, quyền và scope evidence. | DR-1, DR-2, DR-3, DR-4, DR-5, DR-6, DR-8 |
| DATN-131 Detail | `getById` luôn lọc theo cả `projectId` và `taskId`. | Chưa có handler, chưa có quy tắc che giấu sự tồn tại; cũng cần verifier, quyền và scope evidence. | DR-1, DR-2, DR-3, DR-4, DR-5, DR-8 |
| DATN-132 Scope và authorization | `TaskAuthorizationBoundary` và `TaskAuthorizationHttpGuard` (các thao tác `create`, `list`, `detail`) có test deny-by-default: verifier, scope evidence, permission policy, project mismatch, resource scope. Mặc định: verifier không khả dụng, scope evidence không khả dụng, policy `DenyAll`. | Mọi thao tác đang bị từ chối. Cần verifier thật, nguồn scope evidence thật và policy `ALLOW` được duyệt. | DR-1, DR-3, DR-4, DR-8 |
| DATN-133 Test | Các test ở trên cho phần đã duyệt và phần dormant. | Test cho create/list/detail cần oracle từ contract được duyệt; viết trước khi có contract sẽ phải làm lại. | Tất cả DR trên |

Cột "Bị chặn bởi" ở đây và cột "Mở khóa" ở §3 là cùng một ma trận (DR-1: 128–133; DR-2: 129–131; DR-3, DR-4, DR-8: 129–132; DR-5: 129–131; DR-6: 128, 130; DR-7: 129). Khi sửa một bảng phải sửa bảng kia.

### 2.1. Bằng chứng kiểm thử đã chạy (18/10/2026, `origin/main` `7d3e65a`, không sửa mã)

- `jest src/services/task src/gateway/task`: 147 pass, 26 skipped, 1 fail. Lỗi duy nhất là timeout 5 giây của `task-runtime-registration.spec.ts` ở lần chạy đầu (khởi động `AppModule` lúc chưa có cache); chạy lại riêng spec này với `--testTimeout=60000` thì 3/3 pass. Chạy lại toàn bộ lệnh trên với `--testTimeout=60000` trong lần review: 148 pass, 26 skipped, 0 fail (3 suite bị skip).
- Ba spec MongoDB của Task (`task-data.repository.mongodb.spec.ts`, `task-delegation-replay-store.mongodb.spec.ts`, `task-runtime.bootstrap.mongodb.spec.ts`) **bị bỏ qua mặc định**. Chúng cần `MONGODB_INTEGRATION=true` và một replica set MongoDB 7 đã đánh dấu, bật xác thực, bật `enableTestCommands` (D-03 O10 dùng `configureFailPoint`, D-03 O11 cần xác thực để kiểm tra quyền).
- Vì sao CI chưa chạy chúng (`.github/workflows/ci.yml`): job `unit-tests` không đặt `MONGODB_INTEGRATION` nên các spec này bị skip; job `mongodb-integration-tests` có đặt biến nhưng chỉ chạy các spec IAM theo đường dẫn tường minh, và mongod của job đó khởi động với `--replSet rs0` mà không bật xác thực hay `enableTestCommands`.
- Chạy cục bộ trên replica set tạm thời, loopback, bật xác thực (mongod 7.0.24): spec repository và replay-store 22 pass, 1 skipped, 0 fail, gồm D-03 O1–O13; spec bootstrap 3/3 pass khi chạy riêng. Khi chạy ngay sau spec replay-store trong cùng một fixture, spec bootstrap từng thoát bằng `process.exit(1)` lúc khởi tạo Nest; nguyên nhân chưa được tách riêng. Kết quả cục bộ này do người soạn chạy ở phiên trước, chưa đính kèm lệnh/log và chưa được tái hiện khi review; cần ghi lại lệnh và log trước khi dùng làm bằng chứng bàn giao.
- Đề xuất kỹ thuật riêng, không cần quyết định sản phẩm: đưa các spec MongoDB của Task vào CI trên replica set bật xác thực và `enableTestCommands`. Chưa thực hiện.

## 3. Quyết định đề nghị

Mỗi dòng cần được ghi nhận là `APPROVE`, `AMEND`, `REJECT` hoặc `DEFER`, kèm authority, ngày và revision của tài liệu này. "Đề xuất" là ý kiến của người soạn, không phải quyết định.

| ID | Quyết định cần ghi nhận | Phương án | Đề xuất | Authority | Mở khóa |
|---|---|---|---|---|---|
| DR-1 | Phạm vi lát cắt của DATN-97 | **A.** Lát cắt 7 trường: create `{title}`, list theo Project, detail. Response chỉ gồm `id, projectId, title, createdBy, createdAt, updatedAt, version`. Trường mở rộng, filter, sort, status vẫn `DISABLED`.<br>**B.** Toàn bộ contract đề xuất D-13 §3.3–3.4, cần duyệt từng trường mở rộng.<br>**Điểm con:** có đưa `version` vào response hay không. | A. DTO của D-13 (`TaskResponseDTO`) đòi `status`, `priority`, `assigneeId`... nên không dùng được cho lát cắt 7 trường; cần DTO riêng đã duyệt.<br>Về `version`: [doc 22](22-task-v1-d03-delta-approval-record.md) P2 không duyệt ngữ nghĩa CAS/ETag công khai, nên nếu giữ `version` trong response thì ghi rõ nó chỉ là thông tin, không dùng làm `expectedVersion`; Product có thể chọn bỏ khỏi response. | Product | 128–133 |
| DR-2 | Vị trí route và việc kích hoạt | **A.** Route nội bộ `/internal/tasks...` trong Task service theo ADR-010, mặc định tắt, bật bằng cấu hình tường minh; route công khai qua Gateway để quyết định riêng.<br>**B.** Route công khai `/api/v1/projects/:projectId/tasks...` ngay. | A. Cần thêm một ngoại lệ cho guide BE (tương tự D04-1) cho phép controller trong `src/services/task/**`, vì guide hiện cấm controller. | Architecture; chủ guide BE | 129–131 |
| DR-3 | Trust và delegation của lời gọi vào Task service | Chọn profile verifier: issuer, audience, định dạng token, bằng chứng dịch vụ (mTLS hoặc tương đương), replay store. Hoặc chấp nhận một prototype cụ thể. Hiện `UnconfiguredTaskInboundContextVerifier` từ chối tất cả.<br>Nếu replay store cần collection hoặc index mới trong MongoDB thì đó là database change (xem §1 mục 5). | Cần quyết định của Security; người soạn không đề xuất profile. | Security; Architecture | 129–132 |
| DR-4 | Ma trận quyền cho create/list/detail | Duyệt hai dòng của D-13 §3.5: `TASK_CREATE`, và `TASK_READ` chỉ cho list và detail (Events không thuộc phạm vi này) cho `MEMBER` có `ProjectMembership` ACTIVE. Xác nhận: Organization `ADMIN` không có quyền đọc Project riêng tư mặc định; quyền xuất phát từ Team chưa bật; guide yêu cầu kiểm tra Organization Membership ACTIVE phía server.<br>**Cần xác nhận về nguồn:** [02_ACTORS_ROLES_AND_PERMISSIONS.md](../02_ACTORS_ROLES_AND_PERMISSIONS.md) §5–6 mô tả quyền của `MEMBER` hẹp hơn tư cách thành viên Project (tạo task, sửa task của mình hoặc được giao) và không nêu rõ `MEMBER` đọc mọi task trong Project; D-13 §3.5 là ma trận ứng viên. Cần Security/Product xác nhận việc đọc toàn Project là có chủ đích. | Duyệt đúng hai dòng này nếu xác nhận trên được ghi nhận. Nhận định rằng xung đột Project `ADMIN` chỉ ảnh hưởng thao tác sửa/gán là **suy luận của người soạn**, chưa có trong doc 23 (§3.1 chặn DATN-97 bằng cả hàng RBAC và đòi duyệt toàn ma trận); cần Security xác nhận trước khi dựa vào nó. | Security; Product | 129–132 |
| DR-5 | Hợp đồng lỗi và che giấu | Mã trạng thái và mã lỗi cho 3 thao tác; non-member hoặc cross-scope trả 404; id sai định dạng; trường body lạ. **Cần chọn định dạng response:** D-13 đề xuất `{success, data/error}`, còn BE hiện dùng `StructuredExceptionFilter` trả `{code, message, details, requestId}` và không có response bao `success` nào trong mã production. | Dùng định dạng hiện có của BE, trừ khi Architecture quyết định khác. | Architecture; Security; Product | 129–131 |
| DR-6 | Ngữ nghĩa phân trang của list | **A.** Cursor `afterId` + `limit` 1–100, sắp xếp `_id` tăng dần (đã có, D-03 O12 trong doc 21 đã kiểm thử).<br>**B.** `page/limit/total` + tie-breaker `_id` (đề xuất D-13, cần ngữ nghĩa snapshot theo D-13 O32 và một truy vấn đếm). | A cho lát cắt 7 trường. | Product; Architecture | 128, 130 |
| DR-7 | Ngữ nghĩa create công khai | (a) Create công khai có dùng đúng sự kiện P3 đã duyệt không.<br>(b) Giới hạn độ dài `title`: đã duyệt là không giới hạn, D-13 đề xuất 500 code point.<br>(c) `Idempotency-Key`: đưa vào hay loại khỏi lát cắt.<br>(d) **Ánh xạ HTTP cho `ABORTED` và `UNCERTAIN`**; nếu không có idempotency, client thử lại có thể tạo trùng.<br>**Liên hệ (a)–(c):** P3 quy định `operationId` do server sinh (UUID v4) và repository hiện không nhận key từ caller; dùng key của client làm `operationId` nghĩa là đổi P3 hoặc đổi chữ ký `create`, và cần kho dedupe (D-13 §3.7) là database change. | (a) dùng P3 nguyên vẹn.<br>(b) giữ không giới hạn như doc 22.<br>(c), (d): không đề xuất; cần quyết định của Architecture, người soạn không đề xuất mã trạng thái. Nếu (c) = loại khỏi lát cắt thì §1 mục 5 giữ nguyên "không đổi database". | Product; Architecture | 129 |
| DR-8 | Nguồn bằng chứng scope | Task service lấy Project tồn tại, Organization sở hữu, Organization Membership ACTIVE và ProjectMembership từ đâu: claim trong delegation đã ký, gọi đồng bộ sang IAM, hoặc read model. Gồm yêu cầu độ mới và xử lý thu hồi quyền. | Cần quyết định của Architecture và Security; người soạn không đề xuất. | Architecture; Security | 129–132 |

**Điều kiện kèm theo (contract-first).** `AGENTS.md` của BE (mục "Mandatory Gates") yêu cầu duyệt OpenAPI về request, response, error, scope và pagination trước khi implement API nghiệp vụ. D-13 §3.4 chỉ là văn bản ứng viên, và `28-task-v1-d05-proposed.openapi.yaml` không tồn tại (xem §5). Vì vậy một OpenAPI mới cho lát cắt 7 trường là sản phẩm phải được soạn và duyệt cùng DR-1, DR-5, DR-6 (và DR-7 nếu có), trước khi viết oracle hay handler. Chủ soạn và authority duyệt OpenAPI chưa được chỉ định trong tài liệu này.

**Ngoài phạm vi, giữ nguyên chặn:** kích hoạt production, provisioning `continuum_task` và quy trình migration/seed theo ADR-003; route công khai qua Gateway/BFF; mutation, assignment, lifecycle, history API công khai; Work Note và Handover.

## 4. Việc sẽ làm khi quyết định được ghi nhận

Chỉ làm sau khi các DR tương ứng có bằng chứng, theo thứ tự ưu tiên của DATN-128 đến DATN-133:

1. Cập nhật guide BE theo DR-2 trong một PR riêng, nếu phương án A được duyệt.
2. Soạn và duyệt OpenAPI cho lát cắt 7 trường (xem "Điều kiện kèm theo" ở §3), rồi viết oracle cho create/list/detail từ OpenAPI đó và test thất bại trước khi viết handler.
3. Thêm controller, DTO và ánh xạ lỗi trong `src/services/task/**`, dùng `TaskDataRepository` hiện có, không đổi schema hay index (trừ khi DR-3 hoặc DR-7(c) kéo theo database change, khi đó tách DB PR riêng).
4. Nối verifier, nguồn scope evidence và policy theo DR-3, DR-4, DR-8; giữ mặc định từ chối khi cấu hình thiếu.
5. Chạy `npm run check` và báo cáo kết quả theo checklist bàn giao của `AI_WORKFLOW.md`.

## 5. Trạng thái của gói này

- Chưa có thay đổi nào ở DATN-BE, DATN-FE hay database. Chưa đổi trạng thái Jira của DATN-97 hay subtask.
- `AGENTS.md` của BE nhắc tới decision record 27 §§14–17 và `28-task-v1-d05-proposed.openapi.yaml` như các đề xuất review. Hai tài liệu này không có trên `origin/main` hay các nhánh remote của Document đã fetch (đã kiểm tra lại ngày 18/10/2026), nên không được dùng làm nguồn ở đây.
- Cách ghi nhận phê duyệt: theo mẫu của [doc 22](22-task-v1-d03-delta-approval-record.md), gồm authority, ngày, kênh bằng chứng, revision và phạm vi từng DR.
