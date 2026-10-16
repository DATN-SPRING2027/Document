# DATN-301 — Todo và cổng gỡ blocker

Jira: [DATN-301](https://trankimthang0207.atlassian.net/browse/DATN-301) · Contract: [DATN-294](../platform-operator-v1-contract.md)

## Đã chuẩn bị trong PR tài liệu này

- [x] Ghi rõ evidence hiện có và các ranh giới đã được xác nhận.
- [x] Tạo decision worksheet cho sáu nhóm policy trong DATN-301.
- [x] Liệt kê riêng 37 permission proposal để owner disposition từng mã.
- [x] Gắn decision với chủ thể phê duyệt và tác động lên DATN-295–300.
- [x] Giữ nguyên trạng thái chưa duyệt; không thay đổi runtime.

## Chờ người có thẩm quyền quyết định

- [ ] **D1 — Bundle:** DEC-ACCESS-09 A-04 hiện duyệt ba mã; disposition đủ 37 mã mới, chốt role resolution, grant/revoke, bundle atomicity và partial failure. Giữ nguyên ba mã A-04 trừ khi có duyệt riêng.
- [ ] **D2 — Bootstrap/recovery:** ghi rõ issuer, xác minh issuer/recipient, assignment path, no-self-grant, race/duplicate, revoke, mất operator duy nhất, audit, rollback và hậu kiểm.
- [ ] **D3 — Configuration:** DEC-ACCESS-09 hiện giữ config read/write là `FUTURE / DECISION_REQUIRED`; chọn defer và reconcile DATN-293, hoặc amend DEC-ACCESS-09 trước khi thêm quyền/operation.
- [ ] **D4 — Error/concealment:** duyệt missing-vs-forbidden theo DEC-ACCESS-10 và status/body cho validation, stale/conflict, dependency, unexpected failure.
- [ ] **D5 — Audit:** duyệt invariant, event coverage, field allowlist, redaction, retention, read/export/denial logging, audit-write failure behavior và cách bảo đảm append-only.
- [ ] **D6 — Operation semantics:** duyệt preconditions/state transitions, scope/target resolution, input/output, idempotency/concurrency, side effect/destructive impact, audit và error cho mỗi operation còn active.
- [ ] Ghi tên/nhóm owner, ngày, rationale, evidence và phạm vi cho từng quyết định.

## Sau khi được duyệt

- [ ] Cập nhật decision register, permission matrix và operation catalog trong DATN-294.
- [ ] Đồng bộ `research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md` và `architecture/05_SECURITY_AND_GOVERNANCE.md` nếu quyết định làm thay đổi các mô tả tổng quát hiện tại.
- [ ] Cập nhật DATN-293, DEC-ACCESS-09/10 và các child task liên quan; không sửa decision gốc nếu chưa theo quy trình owner của tài liệu đó.
- [ ] Chỉ gỡ từng dependency DATN-295–300 khi điều kiện cụ thể của task đó đã có evidence.
- [ ] Bàn giao các test oracle cho DATN-300; sau đó domain task chạy validation riêng theo yêu cầu repository.

## Trạng thái blocker tại thời điểm lập worksheet

| Nhóm | Trạng thái | Không được làm trước khi đóng |
|---|---|---|
| D1 — 37 mã và bundle | `BLOCKED` | Tạo role bundle hoặc grant quyền mới |
| D2 — Bootstrap/recovery | `BLOCKED` | Gán operator đầu tiên hoặc tạo đường phục hồi ngầm |
| D3 — Configuration | `BLOCKED / SCOPE CONFLICT` | Thêm config permission/API |
| D4 — Error/concealment | `BLOCKED` | Công bố status/mã lỗi mới hoặc chọn 404/403 để che resource |
| D5 — Audit | `BLOCKED` | Tuyên bố audit append-only/đầy đủ hoặc cho phép mutation không audit |
| D6 — Operation semantics | `BLOCKED` theo từng domain | Bật operation mà state, side-effect hoặc retry chưa có contract |

## Gate riêng để bắt đầu DATN-295

Đối chiếu schema/DEC-ACCESS-09 trong [design.md §11](design.md): hiện **chưa đủ điều kiện implementation**. Trước khi bỏ liên kết DATN-301 → DATN-295, cần owner duyệt:

- [ ] Exact finite permission bundle (3 mã A-04 + disposition của 37 mã mới; Configuration có scope riêng).
- [ ] Một authority representation và semantics khi thiếu/partial assignment; atomic grant/revoke và bundle version.
- [ ] Issuer/bootstrap/recovery path, identity evidence và transaction/rollback.
- [ ] Tối thiểu audit contract cho grant/bootstrap/revoke mà DATN-295 phải persist hoặc bảo đảm.

D4 (chi tiết error codes/bodies) và D6 (semantics từng operation) có thể là dependency riêng cho API/operation downstream, nhưng chỉ sau khi owner xác nhận phạm vi DATN-295 không đòi các field/state đó. Không tự chuyển DATN-295 sang Ready hoặc gỡ blocker bằng worksheet này.
