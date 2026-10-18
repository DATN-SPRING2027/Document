# DATN-97 — D-05 Task Core BE: ghi nhận quyết định cho D05-DR1

- **Trạng thái quyết định:** APPROVED MỘT PHẦN. DR-1, DR-2, DR-4, DR-5, DR-6 và DR-7(a)(b) được duyệt. DR-3, DR-7(c)(d) và DR-8 là `DEFER` và **vẫn bị chặn**.
- **Tài liệu được quyết định:** [doc 24](24-task-v1-d05-core-decision-request.md), revision D05-DR1 (đã merge qua Document PR #44).
- **Người phê duyệt:** Trần Kim Thắng, Leader (theo [Member.md](../../Member.md)), ngày 18/10/2026 (Asia/Bangkok). Comment được đăng bằng tài khoản GitHub `KeyT9999`; việc tài khoản này là người trên do chính comment và chủ task DATN-97 nêu, `Member.md` không ghi GitHub handle. Người phê duyệt tự ghi: "thực hiện phê duyệt theo phạm vi ủy quyền Product/Architecture/Security (cần xác nhận phạm vi ủy quyền)".
- **Kênh bằng chứng:** [comment trên Document PR #44](https://github.com/DATN-SPRING2027/Document/pull/44#issuecomment-6248155568) (comment id 6248155568, tạo 09:18:46Z, sửa lần cuối 09:29:32Z ngày 18/10/2026). Nội dung dưới đây được đọc sau lần sửa 09:29:32Z; các lần sửa sau đó không được bao phủ. Vì comment có thể bị sửa, nguyên văn các quyết định được lưu ở §2 làm bản bất biến của record này.
- **Người ghi nhận:** Claude (AI) theo yêu cầu của Nguyen Hong Phuc, chủ task DATN-97. Record này ghi lại quyết định của con người; không phải phê duyệt của AI, không phải đánh giá độc lập và không phải một GitHub review APPROVED.
- **Jira:** [DATN-97](https://trankimthang0207.atlassian.net/browse/DATN-97), subtask DATN-128 đến DATN-133. Record này không đổi trạng thái Jira của task hay subtask nào.

---

## 1. Phạm vi và ghi chú mở

- Chỉ các dòng được đánh dấu `APPROVE` ở §2 có hiệu lực, và chỉ ở đúng nội dung doc 24 revision D05-DR1 cùng các điều chỉnh người duyệt ghi trong cột "Nội dung". Theo doc 23 và chính comment, việc merge PR #44 không đồng nghĩa phê duyệt các mục còn lại.
- Quyền chỉ hiệu lực cho lát cắt 7 trường D-03. Không mở route công khai, mutation, lifecycle, assignment hay history API.
- **Ghi chú mở (không chặn công việc kỹ thuật):** người duyệt tự ghi cần xác nhận phạm vi ủy quyền của Leader đối với Product, Architecture và Security. Record này chỉ ghi lại chữ trong comment, không tự thiết lập ủy quyền đó. Tiền lệ cùng loại: [doc 22](22-task-v1-d03-delta-approval-record.md) ghi phê duyệt của Leader, và ngoại lệ guide D04-1 trong `AGENTS.md` của BE (dòng 8) được ghi dưới ủy quyền của Leader. Tiền lệ này không tự thay thế xác nhận cho phần Security.
- **Cách đóng ghi chú:** khi Leader review PR chứa record này, ghi thêm một dòng xác nhận trên PR đó, gồm (1) phạm vi ủy quyền, (2) người quyết định các mục `DEFER` (§5), (3) authority duyệt OpenAPI. Công việc kỹ thuật (PR guide BE, soạn OpenAPI) được làm và trình review như bình thường trong lúc chờ; không có gì được kích hoạt, và các mục `DEFER` vẫn bị chặn.
- Metadata GitHub của tài khoản (`author_association` = `COLLABORATOR`) là quyền truy cập repository, không dùng để suy ra vai trò.

## 2. Quyết định đã ghi nhận (nguyên văn nội dung của người duyệt)

Cột "Authority theo doc 24" là authority doc 24 §3 đề nghị cho từng DR. Mọi dòng `APPROVE` trong bảng do Leader duyệt theo ủy quyền nêu ở §1.

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

Ba trường "Người quyết định" của các mục `DEFER` vẫn là chỗ trống (`[Tên …]`); record này không điền thay.

## 3. Cách hiểu và hệ quả của từng quyết định đã duyệt

- **DR-1:** phạm vi là create `{title}`, list theo Project, detail. Response gồm `id, projectId, title, createdBy, createdAt, updatedAt, version`. `version` chỉ là thông tin; không có `expectedVersion`, CAS hay ETag. Trường mở rộng, filter, sort và status vẫn `DISABLED`.
- **DR-2:**
  - *Điều được duyệt:* route nội bộ `/internal/tasks`, mặc định tắt; ngoại lệ guide BE cho controller trong `src/services/task/**`. Phê duyệt này là quyết định về hướng đi, **chưa sửa** `AGENTS.md` của BE; việc cập nhật guide vẫn phải làm trong một PR BE riêng (doc 24 §4 bước 1).
  - *Suy ra từ `AGENTS.md` BE (dòng 9), không phải điều người duyệt ghi:* guide hiện cấm "add or activate" route/controller cho đến khi các gate replay và ownership được ghi nhận. Vì DR-3 và DR-8 đang `DEFER`, nên PR guide nên chỉ cho phép controller ở trạng thái ngủ (mặc định tắt, mặc định từ chối theo authorization boundary hiện có) và nói rõ việc kích hoạt vẫn bị chặn. Nội dung cụ thể này cần reviewer của PR guide xem xét.
- **DR-4:** điều kiện đọc/tạo là Organization Membership ACTIVE (kiểm tra phía server theo `AGENTS.md` BE) và ProjectMembership ACTIVE. Người duyệt xác nhận đọc toàn Project là có chủ đích, và Events nằm ngoài phạm vi.
- **DR-5:** dùng định dạng lỗi hiện có của BE; không dùng `{success, data/error}` của D-13. Mã trạng thái và mã lỗi cụ thể của 3 thao tác phải được viết trong OpenAPI để duyệt.
- **DR-6:** cursor `afterId` + `limit` 1–100, sắp xếp `_id` tăng dần, không có `page/total`.
- **DR-7(a)(b):** create dùng đúng sự kiện P3 đã duyệt (doc 22) và không đặt giới hạn độ dài `title`.
- **Database:** không có thay đổi database từ các quyết định đã duyệt. Nếu DR-3 hoặc DR-7(c) sau này kéo theo kho replay/dedupe mới thì đó là database change riêng (xem doc 24 §1 mục 5).

## 4. Tác động lên subtask DATN-97

| Subtask | Đã đủ quyết định | Còn chờ |
|---|---|---|
| DATN-128 Repository | DR-1, DR-6 | Không còn quyết định chờ; repository hiện có đã đáp ứng 7 trường (cần chạy lại bộ kiểm tra khi bàn giao) |
| DATN-129 Create | DR-1, DR-2, DR-4, DR-5, DR-7(a)(b) | DR-3, DR-7(c)(d), DR-8 |
| DATN-130 List | DR-1, DR-2, DR-4, DR-5, DR-6 | DR-3, DR-8 |
| DATN-131 Detail | DR-1, DR-2, DR-4, DR-5 | DR-3, DR-8 |
| DATN-132 Scope và authorization | DR-1, DR-4 | DR-3, DR-8 |
| DATN-133 Test | Phần list/detail sau khi OpenAPI được duyệt | Phần create và phần nối verifier/scope sau khi các DR chờ được chốt |

## 5. Việc còn lại

1. **Một dòng xác nhận của Leader trên PR chứa record này** (xem "Cách đóng ghi chú" ở §1): phạm vi ủy quyền, người quyết định DR-3, DR-7(c)(d), DR-8, và authority duyệt OpenAPI.
2. **Ghi nhận quyết định của các DR còn `DEFER`** bằng một record tiếp theo theo cùng mẫu khi người quyết định trả lời.
3. **PR BE cập nhật guide** theo DR-2 (ngoại lệ có phạm vi, mặc định tắt, chưa kích hoạt), trình reviewer.
4. **Soạn OpenAPI** cho lát cắt 7 trường theo DR-1, DR-4, DR-5, DR-6, DR-7(a)(b); phần create ghi rõ các điểm đang chờ DR-7(c)(d). Chủ soạn là chủ task DATN-97; trình authority duyệt.
5. Chỉ sau khi OpenAPI được duyệt mới viết oracle và handler; chạy `npm run check` và báo cáo theo checklist bàn giao của `AI_WORKFLOW.md`.

Record này không kích hoạt route nào, không sửa mã hay guide BE, không đổi trạng thái Jira và không phải phê duyệt OpenAPI.
