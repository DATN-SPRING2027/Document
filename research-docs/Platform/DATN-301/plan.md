# DATN-301 — Kế hoạch chốt policy PLATFORM_OPERATOR V1

| Trường | Giá trị |
|---|---|
| Jira | [DATN-301](https://trankimthang0207.atlassian.net/browse/DATN-301) |
| Parent | [DATN-293](https://trankimthang0207.atlassian.net/browse/DATN-293) |
| Contract đầu vào | [PLATFORM_OPERATOR V1 Contract](../platform-operator-v1-contract.md) — DATN-294 |
| Trạng thái tài liệu | Chuẩn bị quyết định; chưa phải phê duyệt policy |
| Phạm vi | Tài liệu / quyết định; không thay đổi runtime |

## Mục tiêu

Tạo một quy trình quyết định có thể review và truy vết cho sáu nhóm policy đang chặn các task DATN-295–300: bundle 37 quyền, bootstrap/recovery, Configuration, error/concealment, audit và semantics của operation. Đầu ra cuối cùng phải ghi rõ quyết định nào được duyệt, bởi ai, dựa trên evidence nào, phạm vi áp dụng và các task con nào được mở khóa.

## Ranh giới đã biết

- V1 chỉ có một `PLATFORM_OPERATOR` với quyền hiệu lực đầy đủ trong tập Platform Administration V1 được duyệt; không chia tier, không wildcard và không Break-glass.
- Authentication vẫn bắt buộc. Role này không tự cấp quyền Organization/Project membership hoặc đọc nội dung tenant.
- Secret/credential không được trả về API/FE; privileged mutation phải được audit.
- Ba permission hiện có của DATN-79 được giữ nguyên cho đến khi có phê duyệt thay đổi riêng.
- `DEC-ACCESS-09` hiện hoãn config read/write; DATN-293 lại liệt kê Configuration. Chưa có quyết định hòa giải hai nguồn này.
- Các lựa chọn còn mở trong DATN-294 là proposal/blocker, không phải quyền runtime.

## Kế hoạch thực hiện

1. **Đóng gói evidence:** đối chiếu DATN-294, DATN-293, DATN-79/A-04, DEC-ACCESS-09 và DEC-ACCESS-10; đánh dấu rõ fact, derived constraint, proposal và conflict.
2. **Xin disposition theo từng nhóm:** người phụ trách Platform/Security duyệt phạm vi và audit; IAM/Authorization duyệt role resolution, grant, bootstrap và lỗi; domain owner duyệt state/side-effect của operation thuộc domain mình.
3. **Ghi decision record:** lưu lựa chọn, người duyệt, ngày, lý do, evidence, ngoại lệ, ảnh hưởng API/schema và task con. Mục chưa có owner approval giữ `BLOCKED` hoặc `DEFERRED`.
4. **Đồng bộ contract:** sau khi có quyết định, cập nhật DATN-294 và các nguồn kiến trúc liên quan; sửa DATN-293/child tasks nếu scope thay đổi; không để proposal trông như approved.
5. **Đánh giá readiness:** chỉ gỡ dependency tương ứng khi quyết định đã được owner duyệt và contract có thể implement mà không cần suy diễn. DATN-300 cần giữ gate cho test evidence sau khi các contract được chốt.

## Điều kiện hoàn tất DATN-301

- Có disposition được người/nhóm có thẩm quyền xác nhận cho đủ sáu nhóm trong [design.md](design.md).
- Từng permission trong danh sách 37 mã có trạng thái `APPROVE`, `MODIFY`, `REJECT` hoặc `DEFER`, có rationale và liên kết đến role bundle cuối cùng.
- Bootstrap/recovery có issuer, identity verification, no-self-grant, atomicity/lifecycle, audit, revoke, rollback và hậu kiểm.
- Configuration có quyết định nhất quán với DEC-ACCESS-09 hoặc decision được sửa chính thức.
- Error/concealment, audit invariant và semantics của từng operation còn active được ghi thành contract có thể triển khai.
- Contract DATN-294, phạm vi DATN-293 và dependencies DATN-295–300 đồng bộ; không còn TBD implementation-affecting bị ngầm coi là đã duyệt.

## Không thuộc phạm vi của PR này

- Không cấp 37 permission mới, tạo role/bundle runtime hoặc đổi authorization.
- Không chọn policy thay cho Platform/Security, IAM/Authorization hay domain owner.
- Không thay đổi schema, migration, API, UI, seeds, production configuration hoặc audit store.
- Không chuyển DATN-295–300 sang trạng thái sẵn sàng chỉ vì decision worksheet đã được tạo.
