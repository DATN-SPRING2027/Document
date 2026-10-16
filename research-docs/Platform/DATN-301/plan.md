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
- Contract audit boundary: state change + required event share one durable commit boundary; external side effects need a durable intent/audit before dispatch or remain outside active V1. A-04 Organization provisioning supplies a same-transaction precedent, not proof of universal coverage/outbox.
- Với 37 operation mới, authorization yêu cầu full exact 40-code set hiện hành cộng exact operation permission; ba operation A-04 giữ single-code behavior.
- Preserve current A-04 platform login/refresh: password + ACTIVE-user + rate-limit/MFA + fresh authority on login; platform-context refresh revalidates current authority; protected requests recheck current authority.

Security/IAM cần ký issuer/executor và bootstrap/recovery procedure; Security/IAM cũng cần chốt audit retention. Audit producer coverage, read/export/denial behavior, durability controls và operation-specific contracts vẫn cần audit/domain owners. Chi tiết và exact codes ở [design.md](design.md).

## Ranh giới bắt buộc

- Authentication luôn bắt buộc; không bypass Organization/Project ACL hoặc tenant-content boundary.
- Secret/credential không trả ra API/FE; không có Break-glass, hidden account, production seed hoặc wildcard.
- Ba mã A-04 không đổi tên hoặc semantics; không backfill tự động các assignment cũ.
- Permission membership tự nó không bật API/UI: 37 mapping mới nằm ngoài active V1 catalog và bị chặn triển khai, chờ domain owner quyết định từng operation là `ACTIVE` (kèm semantics/test oracle đầy đủ) hay `DEFERRED FROM V1` (kèm rationale/evidence). Chưa có disposition nào; không suy ra defer hay status cuối cùng chỉ từ việc chưa có approval.
- Configuration không thuộc active V1.

## Kế hoạch hoàn tất

1. [x] Ghi exact permission set và assignment atomicity theo disposition của KeyT.
2. [x] Ghi nhận Configuration deferral và D4 error baseline; resource classes cho concealment/404 còn chờ owner.
3. [x] Ghi nhận audit API append-only và privileged-mutation fail-closed baseline; giữ retention/coverage là blocker.
4. [x] Ghi rõ 3 operation A-04 đang ở active catalog; 37 permission-to-operation mappings là decision queue ngoài catalog, không coi thiếu approval là defer hay final operation status.
5. [ ] Ghi disposition có thẩm quyền cho từng mapping trong 37 mapping mới: `ACTIVE` với full operation contract và test oracle, hoặc `DEFERRED FROM V1` có lý do/evidence.
6. [ ] Security/IAM ghi tên issuer/executor, identity verification, approval path và bootstrap/recovery/revoke/rollback runbook.
7. [ ] Security/IAM + DB owner quyết định legacy A-04 assignment overlap, full-set revoke ownership và regrant-after-revoke dưới unique index hiện tại.
8. [ ] Security/IAM ghi retention period và enforcement boundary.
9. [ ] Security/Audit/domain owners chốt event coverage/fields/reason/redaction/read-export-denial policy và chứng minh failure/durability behavior đáp ứng shared commit-boundary contract.
10. [x] Đồng bộ Configuration deferral và current blockers trong DATN-293/294/295–300.
11. [ ] DEC-ACCESS-10 owner chốt resource classes cần concealment/404 trong shared readiness và các contract liên quan.
12. [ ] Chỉ gỡ dependency khi evidence cho đúng task đã được duyệt và acceptance contract được cập nhật.

## Readiness

DATN-301 chưa đạt acceptance hoàn chỉnh; DATN-295–300 vẫn bị chặn theo dependency tương ứng. Exact permission set, Configuration deferral, D4 baseline, audit invariants, A-04 session behavior và the shared durable commit boundary have been recorded. Issuer/recovery, retention/enforcement, audit completeness, resource classes requiring concealment/404 and owner disposition of each of the 37 new mappings remain open. The three existing A-04 operations stay unchanged; no unapproved operation may be enabled. Xem [design.md §5–7](design.md) để biết gate theo child.
