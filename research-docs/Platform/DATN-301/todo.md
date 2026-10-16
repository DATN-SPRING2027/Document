# DATN-301 — Todo và cổng gỡ blocker

Jira: [DATN-301](https://trankimthang0207.atlassian.net/browse/DATN-301) · Contract: [DATN-294](../platform-operator-v1-contract.md) · Decision record: [design.md](design.md)

## Đã được KeyT phê duyệt ngày 2026-10-16

- [x] Exact set gồm 3 permission DATN-79/A-04 hiện có + đúng 37 code trong DATN-294; không wildcard.
- [x] Giữ exact-permission assignment; cấp/thu hồi toàn tập atomic, all-or-nothing; không đổi hoặc tự backfill assignment legacy.
- [x] Configuration deferred khỏi active V1 theo disposition DATN-301; DEC-ACCESS-09 vẫn ghi `FUTURE / DECISION_REQUIRED`.
- [x] 401/403 baseline; 404 chỉ khi concealment áp dụng; 422/409/503/500 theo error class; IAM envelope và body an toàn.
- [x] Operator không sửa/xóa audit history; privileged mutation fail closed nếu audit chưa ghi bền vững.
- [x] Ghi contract durability: mutation + required audit event có chung durable commit boundary; external side effect cần durable intent/audit trước dispatch hoặc chưa vào active catalog.
- [x] Ghi lại A-04 platform login/refresh và exact permission check hiện hành; không thay đổi DATN-79.
- [x] Ghi resolver boundary: 3 A-04 operation giữ single-code check; operation mới yêu cầu đủ exact 40-code set và exact operation permission.
- [x] Operation mới chưa có owner-approved semantics không được bật; permission không tự bật API/UI.

## Chờ Security/IAM và domain owners

- [ ] Security/IAM chỉ định issuer và executor, identity verification, approval/change evidence và quy trình cấp operator đầu tiên.
- [ ] Security/IAM hoàn tất recovery khi mất operator duy nhất, revoke, no-self-grant, chống race/duplicate, rollback và hậu kiểm.
- [ ] Security/IAM + DB owner chốt full-set grant/revoke đối với legacy A-04 assignments và regrant-after-revoke theo unique index hiện tại.
- [ ] Security/IAM chốt audit retention period và enforcement boundary.
- [ ] Security/Audit/domain owners chốt event producer coverage, required fields/reason, redaction, read/export/denial policy, retention enforcement và evidence storage đáp ứng durable commit boundary.
- [ ] Authorized domain owners ghi disposition từng mapping trong 37 mapping mới: `ACTIVE` với operation record/test oracle đầy đủ hoặc `DEFERRED FROM V1` với rationale/evidence. Hiện chúng ở ngoài active V1 catalog và bị chặn triển khai; thiếu approval không phải defer hay final operation status.
- [x] Ghi baseline error/concealment đã được KeyT duyệt vào shared access-readiness record.
- [ ] DEC-ACCESS-10 owner chỉ định resource classes cần concealment/404; cập nhật security tests và API/FE contracts tương ứng.
- [x] Đồng bộ scope Configuration và current blockers trong Jira DATN-293–300; giữ nguyên DATN-301 → DATN-295–300 links.

## Gate DATN-295

**BLOCKED.** D1 đã chốt exact codes/atomic grant-revoke; DATN-294 đã chốt contract rằng assignment change và required audit event phải cùng durable commit boundary, audit failure phải rollback/no success. DATN-295 vẫn cần Security/IAM issuer/executor, identity evidence, first-grant/recovery/revoke runbook, retention/enforcement và producer/event schema decisions; DB-specific persistence design must implement the contract invariant. Không thêm runtime code/API, seed hoặc gỡ dependency khi các owner decision còn thiếu.

## Trạng thái Jira

DATN-301 đang In Progress; giữ trạng thái này. Jira hiện ghi DATN-301 block DATN-295–300. Không gỡ links hoặc chuyển task con sang Ready chỉ vì decision record đã được cập nhật một phần. Epic DATN-293 và các child descriptions hiện thể hiện Configuration deferred theo DATN-301, DEC-ACCESS-09 source-accurate, và 37 operation đang chờ disposition (không ghi như approved deferred); xem [design.md §5](design.md).
