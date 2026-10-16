# DATN-301 — Kế hoạch chốt policy PLATFORM_OPERATOR V1

| Trường | Giá trị |
|---|---|
| Jira | [DATN-301](https://trankimthang0207.atlassian.net/browse/DATN-301) |
| Parent | [DATN-293](https://trankimthang0207.atlassian.net/browse/DATN-293) |
| Canonical contract | [PLATFORM_OPERATOR V1 Contract](../platform-operator-v1-contract.md) |
| Decision record | [design.md](design.md) |
| Trạng thái | Đã chốt một phần; vẫn In Progress vì còn chữ ký Security/IAM và operation decisions |
| Phạm vi | Policy/documentation và Jira scope; không thay đổi runtime |

## Mục tiêu

Đóng các policy decisions DATN-301 đang chặn DATN-295–300, ghi nguồn phê duyệt, phần còn chờ owner, và giữ implementation không suy diễn từ permission membership.

## Disposition đã nhận ngày 2026-10-16

KeyT phê duyệt:

- PLATFORM_OPERATOR có đúng 40 exact codes: 3 permission hiện hữu của DATN-79/A-04 và toàn bộ 37 code cụ thể trong DATN-294 matrix. Không wildcard, không tự mở rộng runtime.
- Tiếp tục dùng exact permission assignments; grant/revoke toàn bộ tập là atomic, all-or-nothing. Assignment một phần không tạo role operator; không viết lại/backfill các grant legacy.
- Hoãn Platform Configuration khỏi active V1 theo disposition được KeyT duyệt trong DATN-301. DEC-ACCESS-09 tự nó vẫn ghi read/write là `FUTURE / DECISION_REQUIRED`; cần reconcile scope DATN-293, DATN-297 và DATN-299.
- Giữ 401/403; dùng 404 chỉ theo resource-concealment policy; dùng 422/409/503/500 cho validation, conflict/stale, dependency và unexpected failure; response theo safe allowlist IAM envelope.
- Operator API không sửa/xóa audit history; privileged mutations fail closed nếu audit chưa ghi bền vững.

Security/IAM cần ký issuer/executor và bootstrap/recovery procedure; Security/IAM cũng cần chốt audit retention. Audit producer coverage, read/export/denial behavior, durability controls và operation-specific contracts vẫn cần audit/domain owners. Chi tiết và exact codes ở [design.md](design.md).

## Ranh giới bắt buộc

- Authentication luôn bắt buộc; không bypass Organization/Project ACL hoặc tenant-content boundary.
- Secret/credential không trả ra API/FE; không có Break-glass, hidden account, production seed hoặc wildcard.
- Ba mã A-04 không đổi tên hoặc semantics; không backfill tự động các assignment cũ.
- Permission membership tự nó không bật API/UI: 37 operation mới đang `BLOCKED / NOT ACTIVE`, chờ domain owner quyết định từng operation là active (kèm semantics đầy đủ) hay deferred khỏi V1. Không suy ra defer chỉ từ việc chưa có approval.
- Configuration không thuộc active V1.

## Kế hoạch hoàn tất

1. [x] Ghi exact permission set và assignment atomicity theo disposition của KeyT.
2. [x] Ghi nhận Configuration deferral và D4 error baseline; resource classes cho concealment/404 còn chờ owner.
3. [x] Ghi nhận audit API append-only và privileged-mutation fail-closed baseline; giữ retention/coverage là blocker.
4. [ ] Ghi disposition có thẩm quyền cho từng operation trong 37 operation mới: `ACTIVE` với full operation contract và test oracle, hoặc `DEFERRED FROM V1` có lý do/evidence. Tạm thời giữ tất cả `BLOCKED / NOT ACTIVE`.
5. [ ] Security/IAM ghi tên issuer/executor, identity verification, approval path và bootstrap/recovery/revoke/rollback runbook.
6. [ ] Security/IAM ghi retention period và enforcement boundary.
7. [ ] Security/Audit/domain owners chốt audit producers, fields/reason, redaction, read/export/denial coverage và failure/durability behavior.
8. [x] Đồng bộ Configuration deferral và current blockers trong DATN-293/294/295–300.
9. [ ] DEC-ACCESS-10 owner chốt resource classes cần concealment/404 trong shared readiness và các contract liên quan.
10. [ ] Chỉ gỡ dependency khi evidence cho đúng task đã được duyệt và acceptance contract được cập nhật.

## Readiness

DATN-301 chưa đạt acceptance hoàn chỉnh; DATN-295–300 vẫn bị chặn. Exact permission set, Configuration deferral, D4 baseline và hai audit invariants đã có disposition. Issuer/recovery, retention, audit completeness, resource classes cần concealment/404 và disposition của từng 37 operation mới còn mở. Operation chưa được phê duyệt không được bật, nhưng trạng thái an toàn này không phải quyết định defer khỏi V1. Xem [design.md §5–7](design.md) để biết gate theo child.
