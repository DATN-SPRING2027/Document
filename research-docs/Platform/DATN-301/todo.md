# DATN-301 — Todo và cổng gỡ blocker

Jira: [DATN-301](https://trankimthang0207.atlassian.net/browse/DATN-301) · Contract: [DATN-294](../platform-operator-v1-contract.md) · Decision record: [design.md](design.md)

## Đã được KeyT phê duyệt ngày 2026-10-16

- [x] Exact set gồm 3 permission DATN-79/A-04 hiện có + đúng 37 code trong DATN-294; không wildcard.
- [x] Giữ exact-permission assignment; cấp/thu hồi toàn tập atomic, all-or-nothing; không đổi hoặc tự backfill assignment legacy.
- [x] Configuration deferred khỏi active V1 theo disposition DATN-301; DEC-ACCESS-09 vẫn ghi `FUTURE / DECISION_REQUIRED`.
- [x] 401/403 baseline; 404 chỉ khi concealment áp dụng; 422/409/503/500 theo error class; IAM envelope và body an toàn.
- [x] Operator không sửa/xóa audit history; privileged mutation fail closed nếu audit chưa ghi bền vững.
- [x] Operation mới chưa có owner-approved semantics không được bật; permission không tự bật API/UI.

## Chờ Security/IAM và domain owners

- [ ] Security/IAM chỉ định issuer và executor, identity verification, approval/change evidence và quy trình cấp operator đầu tiên.
- [ ] Security/IAM hoàn tất recovery khi mất operator duy nhất, revoke, no-self-grant, chống race/duplicate, rollback và hậu kiểm.
- [ ] Security/IAM chốt audit retention period và enforcement boundary.
- [ ] Security/Audit/domain owners chốt event producer coverage, required fields/reason, redaction, read/export/denial treatment và audit failure/durability.
- [ ] Authorized domain owners ghi disposition từng operation trong 37 operation mới: `ACTIVE` với operation record/test oracle đầy đủ hoặc `DEFERRED FROM V1` với rationale. Cho tới lúc đó, giữ `BLOCKED / NOT ACTIVE`; không suy luận defer.
- [x] Ghi baseline error/concealment đã được KeyT duyệt vào shared access-readiness record.
- [ ] DEC-ACCESS-10 owner chỉ định resource classes cần concealment/404; cập nhật security tests và API/FE contracts tương ứng.
- [x] Đồng bộ scope Configuration và current blockers trong Jira DATN-293–300; giữ nguyên DATN-301 → DATN-295–300 links.

## Gate DATN-295

**BLOCKED.** D1 đã chốt exact codes và atomic grant/revoke, nhưng DATN-295 acceptance vẫn cần issuer/bootstrap/recovery và audit persistence contract. Không thêm code runtime, migration, seed, bootstrap API hoặc gỡ dependency khi Security/IAM chưa ký.

## Trạng thái Jira

DATN-301 đang In Progress; giữ trạng thái này. Jira hiện ghi DATN-301 block DATN-295–300. Không gỡ links hoặc chuyển task con sang Ready chỉ vì decision record đã được cập nhật một phần. Epic DATN-293 và các child descriptions hiện thể hiện Configuration deferred theo DATN-301, DEC-ACCESS-09 source-accurate, và 37 operation đang chờ disposition (không ghi như approved deferred); xem [design.md §5](design.md).
