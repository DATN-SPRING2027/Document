# DATN-97 — D-05 Task Core BE: ghi nhận quyết định cho D05-DR1

- **Trạng thái quyết định:** APPROVED MỘT PHẦN. DR-1, DR-2, DR-4, DR-5, DR-6 và DR-7(a)(b) được duyệt, kèm xác nhận thẩm quyền của Leader ngày 19/10/2026 (§1). DR-3, DR-7(c)(d) và DR-8 là `DEFER` và **vẫn bị chặn**. Ngoại lệ guide (DATN-BE PR #54) đã được Leader duyệt **bằng chữ** ngày 19/10/2026 (chưa bấm Approve trên GitHub). OpenAPI (DATN-BE PR #55) đã được Leader **approve cho list và detail** ngày 19/10/2026 (§2.3), gồm 5 lựa chọn thiết kế chủ task đã chốt (§2.2); không gồm create. Hai PR #54 và #55 **chưa được merge**.
- **Tài liệu được quyết định:** [doc 24](24-task-v1-d05-core-decision-request.md), revision D05-DR1 (đã merge qua Document PR #44).
- **Người phê duyệt:** Trần Kim Thắng, Leader (theo [Member.md](../../Member.md)). Quyết định ghi ngày 18/10/2026 và xác nhận thẩm quyền ghi ngày 19/10/2026 (Asia/Bangkok). Cả hai comment được đăng bằng tài khoản GitHub `KeyT9999`; comment ngày 19/10 tự ghi "Trần Kim Thắng (@KeyT9999) — Team Leader". `Member.md` không ghi GitHub handle.
- **Kênh bằng chứng:**
  - Quyết định: [comment trên Document PR #44](https://github.com/DATN-SPRING2027/Document/pull/44#issuecomment-6248155568) (id 6248155568, tạo 09:18:46Z, sửa lần cuối 09:29:32Z ngày 18/10/2026).
  - Xác nhận thẩm quyền: [comment trên Document PR #46](https://github.com/DATN-SPRING2027/Document/pull/46#issuecomment-6258355860) (id 6258355860, tạo và sửa lần cuối 02:27:43Z ngày 19/10/2026).
  - Phê duyệt OpenAPI: [comment trên DATN-BE PR #55](https://github.com/DATN-SPRING2027/DATN-BE/pull/55#issuecomment-6263376181) (id 6263376181, tạo và sửa lần cuối 08:49:46Z ngày 19/10/2026). Revision được review là commit `dc743a8`; sau đó Leader merge `main` vào nhánh (commit `97fc568`, không đổi ba file của OpenAPI).
  - Comment 6258346573 trên PR #46 (02:26:53Z ngày 19/10/2026) là mẫu còn nguyên placeholder, **không** được dùng làm căn cứ.
  - Nội dung được đọc sau các thời điểm sửa nêu trên; các lần sửa sau đó không được bao phủ. Vì comment có thể bị sửa, nguyên văn các quyết định được lưu ở §2 và §2.1 làm bản bất biến của record này.
- **Người ghi nhận:** Claude (AI) theo yêu cầu của Nguyen Hong Phuc, chủ task DATN-97. Record này ghi lại quyết định của con người; không phải phê duyệt của AI, không phải đánh giá độc lập và không phải một GitHub review APPROVED.
- **Jira:** [DATN-97](https://trankimthang0207.atlassian.net/browse/DATN-97), subtask DATN-128 đến DATN-133. Record này không đổi trạng thái Jira của task hay subtask nào.

---

## 1. Phạm vi, thẩm quyền và các điểm còn mở

- Chỉ các dòng được đánh dấu `APPROVE` ở §2 có hiệu lực, và chỉ ở đúng nội dung doc 24 revision D05-DR1 cùng các điều chỉnh người duyệt ghi. Theo doc 23 và chính các comment, việc merge PR không đồng nghĩa phê duyệt các mục còn lại.
- **Phạm vi:** theo xác nhận ngày 19/10/2026, chỉ áp dụng cho lát cắt Task 7 trường (list theo Project và detail); không mở rộng sang toàn bộ Task V1, các API chưa được duyệt hay việc kích hoạt production.
- **Thẩm quyền (đã xác nhận):** ngày 19/10/2026 Leader xác nhận mình "được phân công thực hiện thẩm quyền quyết định Product, Architecture và Security cho DATN-97 trong phạm vi các nội dung phê duyệt" (§2.1). Điều này đóng ghi chú mở về phạm vi ủy quyền trong comment ngày 18/10 và điều kiện của DR-4 mà bản trước của record này đã nêu theo review trên PR #46. [Doc 20](20-task-v1-contract-approval-record.md) (dòng "Approval authority") ghi rằng phê duyệt của Leader không ngụ ý authority riêng cho các quyết định product, security, API hay vận hành khác; xác nhận ngày 19/10 là tuyên bố rõ ràng cho đúng DATN-97 và phạm vi trên. Đây là tuyên bố của chính Leader; record này không có xác nhận độc lập của một người giữ riêng vai Security hay Architecture, và reviewer có thể yêu cầu thêm.
- **Điểm còn mở:**
  1. Tên người quyết định DR-3, DR-7(c)(d), DR-8 vẫn là chỗ trống (`[Tên …]`) trong comment; record này không điền thay.
  2. **Authority duyệt OpenAPI: đã giải quyết.** Ô tên authority trong comment ngày 19/10 vẫn là placeholder, nhưng chính Leader đã duyệt OpenAPI list/detail ngày 19/10/2026 theo thẩm quyền đã xác nhận (§2.3). Review PR #54 ghi trạng thái `COMMENTED`, nên nút Approve của GitHub chưa được bấm; PR #54 và #55 chưa được merge.
  3. **Create: đã giải quyết một phần.** Leader ghi rõ create chưa thuộc phạm vi OpenAPI được duyệt (§2.3 điều kiện 6). DATN-129 còn chờ DR-3, DR-7(c)(d), DR-8 và một OpenAPI riêng cho create. DR-4 ngày 18/10 ghi "create/list/detail", còn xác nhận ngày 19/10 chỉ nêu list và detail; việc create có thuộc DR-4 hay không cần được ghi lại khi làm create.
  4. **Thay đổi sau record:** DATN-BE PR #58 (lifecycle DB contract, đã merge vào `main` ngày 19/10/2026) khiến tài liệu Task trong DB có thêm `status`, `assigneeId`, `completedAt` và `version` có thể lớn hơn 1. OpenAPI đã duyệt vẫn đúng vì response chỉ có 7 trường, nhưng handler phải chọn đúng 7 trường khi trả về (không trả nguyên tài liệu), và câu "repository hiện có đã đáp ứng 7 trường" của bản trước record này không còn đúng. Cần Leader xác nhận việc này không đổi phạm vi DR-1.
- Metadata GitHub của tài khoản (`author_association` = `COLLABORATOR`) là quyền truy cập repository, không dùng để suy ra vai trò.

## 2. Quyết định đã ghi nhận (nguyên văn nội dung của người duyệt, comment ngày 18/10/2026)

Cột "Authority theo doc 24" là authority doc 24 §3 đề nghị cho từng DR. Mọi dòng `APPROVE` do Leader duyệt theo thẩm quyền nêu ở §1.

| DR | Authority theo doc 24 | Quyết định | Nội dung do người duyệt ghi |
|---|---|---|---|
| DR-1 | Product | APPROVE — A | Chọn lát cắt 7 trường. Giữ `version` trong response chỉ để cung cấp thông tin, không dùng CAS/ETag. |
| DR-2 | Architecture; chủ guide BE | APPROVE — A | Route nội bộ `/internal/tasks`, mặc định tắt. Chấp thuận ngoại lệ guide BE cho controller trong `src/services/task/**`. |
| DR-3 | Security; Architecture | DEFER | Chờ quyết định profile trust/delegation, issuer, audience, mTLS và replay store. Người quyết định: `[Tên người phụ trách Security/Architecture]`. |
| DR-4 | Security; Product | APPROVE | MEMBER có ProjectMembership ACTIVE và Organization Membership ACTIVE được create/list/detail Task trong Project. Cho phép đọc toàn Project là có chủ đích. Không bao gồm Events. |
| DR-5 | Architecture; Security; Product | APPROVE | Sử dụng error format BE hiện tại `{code, message, details, requestId}`. Non-member/cross-scope trả 404. Mã lỗi chi tiết cần thể hiện trong OpenAPI. |
| DR-6 | Product; Architecture | APPROVE — A | Cursor `afterId` và `limit` 1–100, sắp xếp `_id` tăng dần. |
| DR-7(a)(b) | Product; Architecture | APPROVE | Giữ nguyên P3 đã duyệt và không bổ sung business length cap cho `title`. |
| DR-7(c)(d) | Product; Architecture | DEFER | Chưa chốt `Idempotency-Key` và HTTP mapping cho ABORTED/UNCERTAIN. Người quyết định: `[Tên người phụ trách Architecture]`. |
| DR-8 | Architecture; Security | DEFER | Chưa chốt nguồn scope evidence và xử lý thu hồi quyền. Người quyết định: `[Tên người phụ trách Architecture/Security]`. |

Yêu cầu kèm theo của người duyệt: chủ task DATN-97 soạn contract OpenAPI cho lát cắt 7 trường và trình các authority liên quan duyệt trước khi triển khai handler. Kết luận của người duyệt: những mục `DEFER` vẫn bị chặn cho đến khi có quyết định chính thức.

### 2.1. Xác nhận thẩm quyền và phê duyệt ngày 19/10/2026 (tóm lược nguyên văn)

- **Thẩm quyền:** "Tôi, Trần Kim Thắng (@KeyT9999), với vai trò Leader của dự án, xác nhận tôi được phân công thực hiện thẩm quyền quyết định Product, Architecture và Security cho DATN-97 trong phạm vi các nội dung phê duyệt dưới đây. Phạm vi xác nhận chỉ áp dụng cho lát cắt Task 7 trường, gồm list theo Project và detail. Không mở rộng sang toàn bộ Task V1, các API chưa được duyệt hoặc việc kích hoạt production."
- **DR-1 (A), DR-2 (A), DR-4, DR-5, DR-6 (A), DR-7(a)(b): APPROVE.** Bổ sung so với comment ngày 18/10:
  - DR-2: route nội bộ `/internal/tasks`, mặc định tắt, cô lập trong Task module, tuân thủ DENY mặc định; "Chưa cho phép kích hoạt runtime hoặc production khi chưa hoàn tất các điều kiện bảo mật."
  - DR-4: xem danh sách và chi tiết toàn bộ Task trong Project mình tham gia, với Organization Membership `ACTIVE` và ProjectMembership `ACTIVE`; "Đây là chủ đích phân quyền cho lát cắt này, không bao gồm Events/history và không mặc định mở quyền truy cập sang Project khác."
- **DEFER giữ nguyên:** DR-3, DR-7(c)(d), DR-8; ba ô người quyết định và ô người duyệt OpenAPI vẫn là placeholder.
- **Kết luận của người duyệt:** "Cho phép tiếp tục các công việc chuẩn bị và triển khai list/detail sau khi OpenAPI cùng các điều kiện tương ứng được phê duyệt. Không coi các mục DEFER là đã thông qua. Không kích hoạt route, authorization ALLOW hoặc production khi chưa hoàn tất các quyết định bắt buộc."

### 2.2. Review của Leader ngày 19/10/2026 trên DATN-BE PR #54 và #55, và quyết định của chủ task

- **PR #54 (guide, DR-2):** trong thread review của PR, Leader viết "Reviewed and APPROVED — DATN-97 / D05-DR2": chấp thuận ngoại lệ guide Backend cho controller Task trong `src/services/task/**`, chỉ trong phạm vi các route nội bộ được duyệt; yêu cầu tiếp tục duy trì route mặc định tắt, Task module cô lập, authorization deny-by-default, không kích hoạt production, Gateway hoặc public API, và tuân thủ các điều kiện OpenAPI và Security còn chờ; "Phê duyệt này không đồng nghĩa chấp thuận DR-3, DR-7(c)(d) hoặc DR-8." Đây là comment (trạng thái review `COMMENTED`), không phải một GitHub review `APPROVED`.
- **PR #55 (OpenAPI):** review ghi `COMMENTED` lúc 02:28:25Z. Leader thống nhất phạm vi list/detail, cấu trúc Task 7 trường và nguyên tắc phân trang; đề nghị chủ PR xác nhận và ghi nhận quyết định cho PATH-1, LIMIT-1, CURSOR-1, ERR-1 và CACHE-1; AUTH-1 phải giữ phụ thuộc DR-3 và DR-8 và không được coi là đã phê duyệt xác thực hay scope evidence thực tế; sau khi hoàn tất và cập nhật contract, Leader sẽ review để phê duyệt OpenAPI chính thức.
- **Quyết định của chủ task** (Nguyen Hong Phuc, 19/10/2026, theo đề nghị trên). Bằng chứng ban đầu là xác nhận của chủ task gửi người ghi nhận trong cuộc trò chuyện; sau đó nội dung được đăng lại trên [DATN-BE PR #55](https://github.com/DATN-SPRING2027/DATN-BE/pull/55#issuecomment-6259996340) (id 6259996340, 04:57:16Z ngày 19/10/2026) và được Leader duyệt (§2.3).
  - PATH-1: giữ `/internal/tasks/projects/{projectId}/tasks[/{taskId}]`.
  - LIMIT-1: `limit` mặc định 20.
  - CURSOR-1: giữ cách "trang đầy" (`nextAfterId` là id phần tử cuối khi trang đầy, ngược lại `null`).
  - ERR-1: giữ ánh xạ lỗi; "bị từ chối quyền" và path id sai định dạng trả 404. DR-5 do Leader duyệt chỉ bao phủ non-member và cross-scope.
  - CACHE-1: `Cache-Control: no-store`.
  - Các quyết định này được ghi vào `x-owner-decisions` của OpenAPI trong PR #55.

### 2.3. Phê duyệt OpenAPI list/detail của Leader ngày 19/10/2026 (DATN-BE PR #55, tóm lược nguyên văn)

- **Phê duyệt:** "Tôi phê duyệt contract OpenAPI cho lát cắt Task 7 trường, chỉ gồm list và detail", với PATH-1, LIMIT-1 (mặc định 20, khoảng 1–100), CURSOR-1 (chấp nhận khả năng có một trang cuối rỗng), ERR-1 (ánh xạ 401/404/422/503 theo OpenAPI hiện tại, authorization được kiểm tra trước input validation, "Handler phải ánh xạ theo lý do từ chối thay vì chỉ trả 403 chung") và CACHE-1 (`Cache-Control: no-store` cho 200) đều ghi `APPROVE`.
- **Phạm vi và điều kiện (6 điều Leader nêu):**
  1. Chỉ áp dụng cho hai API list/detail và cấu trúc Task 7 trường trong revision được review.
  2. Giữ nguyên DR-4: Organization Membership và ProjectMembership đều phải ACTIVE; thành viên đọc Task trong Project tương ứng, không gồm Events.
  3. DR-3, DR-7(c)(d) và DR-8 tiếp tục `DEFER`.
  4. AUTH-1 chưa được phê duyệt về trust profile, service identity và scope evidence thực tế.
  5. Không kích hoạt route thực tế, production hoặc authorization policy `ALLOW` cho đến khi hoàn thành các điều kiện bảo mật liên quan.
  6. Create API chưa thuộc phạm vi OpenAPI được phê duyệt lần này.
- **Đề nghị của Leader:** cập nhật `x-approval-status`, `APPROVAL-1` và decision record để phản ánh phê duyệt, đồng thời giữ nguyên các mục chưa được quyết định. Việc này được thực hiện ở DATN-BE PR #55 (OpenAPI: `x-approval-status`, `x-approval-conditions`, bỏ `APPROVAL-1`) và ở record này.

## 3. Cách hiểu và hệ quả của từng quyết định đã duyệt

- **DR-1:** phạm vi của quyết định là create `{title}`, list theo Project, detail; OpenAPI được duyệt chỉ gồm list và detail (create bị chặn thêm bởi các DR `DEFER`, xem §1 điểm 3 và §2.3). Response gồm `id, projectId, title, createdBy, createdAt, updatedAt, version`. `version` chỉ là thông tin; không có `expectedVersion`, CAS hay ETag. Trường mở rộng, filter, sort và status vẫn `DISABLED`.
- **DR-2:**
  - *Điều được duyệt:* route nội bộ `/internal/tasks`, mặc định tắt; ngoại lệ guide BE cho controller trong `src/services/task/**`; không kích hoạt runtime hay production khi chưa hoàn tất điều kiện bảo mật. Phê duyệt này là quyết định về hướng đi; việc cập nhật `AGENTS.md` nằm ở DATN-BE PR #54, được Leader duyệt bằng chữ nhưng chưa merge. Cho tới khi PR #54 được merge, `AGENTS.md` trên `main` vẫn cấm thêm controller/route Task.
  - *Suy ra từ `AGENTS.md` BE (dòng 9), không phải điều người duyệt ghi:* guide hiện cấm "add or activate" route/controller cho đến khi các gate replay và ownership được ghi nhận. Vì DR-3 và DR-8 đang `DEFER`, nên PR guide chỉ cho phép controller ở trạng thái ngủ (mặc định tắt, mặc định từ chối theo authorization boundary hiện có) và nói rõ việc kích hoạt vẫn bị chặn.
- **DR-4:** điều kiện đọc là Organization Membership ACTIVE (kiểm tra phía server theo `AGENTS.md` BE) và ProjectMembership ACTIVE; đọc toàn Project của chính Project mình tham gia là chủ đích phân quyền của lát cắt này, Events nằm ngoài phạm vi. Điều kiện nêu ở bản trước của record đã được đóng bằng xác nhận ngày 19/10 (§1). Policy `ALLOW` vẫn chưa được bật vì DR-3 và DR-8 còn `DEFER`.
- **DR-5:** dùng định dạng lỗi hiện có của BE; không dùng `{success, data/error}` của D-13. Mã trạng thái và mã lỗi cụ thể của các thao tác phải được viết trong OpenAPI để duyệt.
- **DR-6:** cursor `afterId` + `limit` 1–100, sắp xếp `_id` tăng dần, không có `page/total`.
- **DR-7(a)(b):** create dùng đúng sự kiện P3 đã duyệt (doc 22) và không đặt giới hạn độ dài `title`.
- **Database:** không có thay đổi database từ các quyết định đã duyệt. Nếu DR-3 hoặc DR-7(c) sau này kéo theo kho replay/dedupe mới thì đó là database change riêng (xem doc 24 §1 mục 5). Việc tài liệu Task trong DB có thêm trường sau DATN-BE PR #58 là thay đổi độc lập với các quyết định này (§1 điểm 4).

## 4. Tác động lên subtask DATN-97

| Subtask | Đã đủ quyết định | Còn chờ |
|---|---|---|
| DATN-128 Repository | DR-1, DR-6 | Không còn quyết định chờ. Từ DATN-BE PR #58 repository trả tài liệu có thêm `status`, `assigneeId`, `completedAt`; list và detail phải chọn đúng 7 trường khi trả về (cần chạy lại bộ kiểm tra khi bàn giao) |
| DATN-129 Create | DR-1, DR-2, DR-4, DR-5, DR-7(a)(b) | DR-3, DR-7(c)(d), DR-8; create chưa thuộc OpenAPI được duyệt (§2.3) nên cần một OpenAPI riêng |
| DATN-130 List | DR-1, DR-2, DR-4, DR-5, DR-6; OpenAPI đã được duyệt (§2.3) | PR #54 (guide) chưa merge; DR-3, DR-8 để nối thật |
| DATN-131 Detail | DR-1, DR-2, DR-4, DR-5; OpenAPI đã được duyệt (§2.3) | PR #54 (guide) chưa merge; DR-3, DR-8 để nối thật |
| DATN-132 Scope và authorization | DR-1, DR-4; ánh xạ lý do từ chối đã được duyệt trong ERR-1 | DR-3, DR-8 để nối thật |
| DATN-133 Test | Phần list/detail: OpenAPI đã được duyệt | Phần create và phần nối verifier/scope sau khi các DR chờ được chốt |

## 5. Việc còn lại

1. **Điền tên** người quyết định DR-3, DR-7(c)(d), DR-8 (vẫn là chỗ trống trong comment của Leader).
2. **Merge DATN-BE PR #54 (guide) và PR #55 (OpenAPI)** do người có thẩm quyền thực hiện; bấm Approve trên GitHub cho PR #54 nếu cần bằng chứng chính thức (hiện chỉ có approve bằng chữ). Handler đầu tiên phụ thuộc PR #54 vì `AGENTS.md` trên `main` vẫn cấm controller Task.
3. **Xác nhận với Leader** rằng việc tài liệu Task trong DB có thêm trường sau PR #58 không đổi phạm vi DR-1: response vẫn đúng 7 trường (§1 điểm 4).
4. **Create:** cần OpenAPI riêng sau khi DR-7(c)(d), DR-3, DR-8 được chốt, và ghi lại create có thuộc DR-4 hay không.
5. **Ghi nhận quyết định của các DR còn `DEFER`** bằng một record tiếp theo theo cùng mẫu khi người quyết định trả lời.
6. **Viết handler list/detail chạy ngầm** sau khi PR #54 được merge: test trước, route mặc định tắt, ánh xạ lý do từ chối theo ERR-1, chỉ trả 7 trường; chạy `npm run check` và báo cáo theo checklist bàn giao của `AI_WORKFLOW.md`.

Record này không kích hoạt route nào, không sửa mã hay guide BE, không đổi trạng thái Jira. Nó ghi lại phê duyệt của Leader và không tự phê duyệt thêm điều gì.
