# DATN-301 — Decision record: PLATFORM_OPERATOR V1 policy

| Trường | Giá trị |
|---|---|
| Jira | [DATN-301](https://trankimthang0207.atlassian.net/browse/DATN-301) |
| Canonical contract | [PLATFORM_OPERATOR V1 Contract](../platform-operator-v1-contract.md) |
| Ngày ghi nhận | 2026-10-16 (Asia/Bangkok) |
| Trạng thái | Phê duyệt một phần; implementation vẫn bị chặn |
| Người đưa ra disposition | KeyT, explicit approval in this conversation |
| Phê duyệt còn bắt buộc | Security/IAM: issuer/bootstrap/recovery và retention; Security/Audit/domain owners: audit coverage/durability; DEC-ACCESS-10 owner: concealment resource classes |

## 1. Phạm vi và cách đọc

Đây là bản ghi policy cho sáu nhóm quyết định trong DATN-301. Disposition được KeyT xác nhận ngày 2026-10-16. Giữ BLOCKED mọi mục cần issuer/runbook, retention, audit coverage/durability và phân loại resource concealment cho tới khi đúng owner cung cấp evidence.

- APPROVED POLICY là quyết định phạm vi/authorization, không tự thêm quyền vào runtime hoặc làm operation/API sẵn sàng.
- DEFERRED là không thuộc active V1; không tạo permission, endpoint hay UI tương ứng.
- BLOCKED là chưa có quyết định/evidence bắt buộc; implementation không được tự suy diễn.
- Giữ nguyên authentication, Organization/Project ACL, tenant-content boundary và nguyên tắc không trả secret.
- Không có permission wildcard, Break-glass, hidden account, credential bypass hoặc production seed.

## 2. Decision record

| Nhóm | Disposition ngày 2026-10-16 | Phạm vi đã chốt | Còn mở / owner ký |
|---|---|---|---|
| D1 — Permission bundle và assignment | **APPROVED POLICY** | PLATFORM_OPERATOR có đúng 40 exact permission codes: 3 mã DATN-79/A-04 hiện có và 37 mã mới ở §3. Không wildcard. Lưu vẫn là exact permission assignments; không yêu cầu role/bundle row. Grant/revoke cả tập là atomic, all-or-nothing. Partial/corrupt assignment không tạo effective PLATFORM_OPERATOR; giữ nguyên các grant legacy hiện có, không tự backfill/đổi mã. | DB/IAM chốt transaction, idempotency, race handling và persisted audit trong DATN-295/296; không được đổi policy 40 mã. |
| D2 — Bootstrap và recovery | **PARTIAL / BLOCKED** | Authentication bắt buộc; issuer không được tự cấp cho chính mình; recipient phải là user hiện hữu và ACTIVE; cấp/thu hồi chính xác cả 40 assignment; không seed, hidden account hay Break-glass. Grant/revoke all-or-nothing và có audit. | Security/IAM phải chỉ định issuer và executor, identity evidence cho issuer/recipient, approval/change record, quy trình cấp operator đầu, mất operator duy nhất, revoke, concurrency/idempotency, rollback và hậu kiểm. Chưa có issuer/runbook nên chưa thể mở DATN-295/296. |
| D3 — Platform Configuration | **APPROVED: DEFERRED FROM V1** | DEC-ACCESS-09 hiện ghi configuration read/write là `FUTURE / DECISION_REQUIRED`; KeyT disposition trong DATN-301 loại Platform Configuration khỏi active V1. Scope DATN-293 và DATN-297/299 đã được reconcile. Không có platform configuration permission, operation, API hay UI trong V1. Không suy ra quyền quản lý platform configuration từ LLM/Integration operation riêng. | Chỉ mở lại bằng decision mới và amendment được duyệt cho DEC-ACCESS-09 cùng permission/API/secret boundary. |
| D4 — Error và concealment | **PARTIAL — baseline approved; missing-vs-forbidden/resource classes open** | Giữ 401 khi unauthenticated/invalid session; 403 khi authenticated nhưng thiếu permission; dùng 404 chỉ cho resource class mà concealment policy đã chỉ định. 422 cho validation/state input không hợp lệ; 409 cho conflict/stale/duplicate; 503 cho dependency unavailable; 500 cho unexpected failure. Response dùng envelope IAM hiện tại (code, message, details, requestId) theo allowlist an toàn; không lộ resource bị che, topology, stack, secret hoặc raw payload. Hành vi chính xác với target không tồn tại so với target tồn tại nhưng không được phép chưa được chốt theo từng resource class. | KeyT đã duyệt baseline; owner DEC-ACCESS-10 cần ghi resource classes và missing-vs-forbidden outcome/concealment. Stable code và field-level body allowlist vẫn do operation owner chốt. |
| D5 — Audit | **PARTIAL / BLOCKED** | Giao diện operator không được sửa/xóa audit history (append-only API policy). Mọi privileged mutation phải fail closed: không trả success nếu audit event chưa được ghi bền vững; secret/credential/raw tenant content bị loại khỏi response và audit metadata. | Security/IAM phải ký retention period. Security/Audit/domain owners phải chốt producer coverage theo operation, audit attempt/denial/read/export, required fields/reason, redaction details, retention enforcement/export permissions và failure/durability mechanism. Không tuyên bố database-level tamper-proof khi chưa có evidence. |
| D6 — Semantics operation | **PARTIAL / BLOCKED — chưa có disposition cho 37 operation** | Ba operation DATN-79 hiện có giữ nguyên hành vi theo A-04. Từng operation mới phải có disposition riêng: `APPROVED ACTIVE` kèm contract đầy đủ, hoặc `DEFERRED FROM V1` do đúng domain owner phê duyệt. Hiện không có evidence owner duyệt lựa chọn nào trong 37 operation; cả 37 ở trạng thái `BLOCKED / NOT ACTIVE`. Quy tắc an toàn “không bật operation khi chưa được duyệt” không đồng nghĩa với quyết định defer khỏi V1. | Domain owner được chỉ định cho từng operation phải ghi lựa chọn, approver, ngày, lý do/evidence, semantics và test oracle. Giữ DATN-295–300 blocked cho đến khi các operation liên quan có disposition và contract được phản ánh trong Jira/docs. |

### Evidence and rationale

- D1: DATN-79/A-04 có chính xác 3 mã hiện hữu; DATN-294 matrix có chính xác 37 mã mới. User chốt bundle hữu hạn 3 + 37, exact assignment và atomic grant/revoke. Không đổi ba mã A-04.
- D2: A-04 chứng minh exact-permission assignment và active-subject checks nhưng không chỉ định issuer/bootstrap/recovery. Security/IAM được giao ký phần này; không được lấp khoảng trống bằng seed hay hidden path.
- D3: DEC-ACCESS-09 ghi config read/write là `FUTURE / DECISION_REQUIRED`; KeyT đã duyệt disposition riêng của DATN-301 là loại Platform Configuration khỏi active V1. Không gán quyết định này ngược lại cho DEC-ACCESS-09.
- D4: A-04 hiện có 401/403; DATN_BE đang có IAM error envelope code/message/details/requestId và các status convention. Decision chốt mapping/allowlist, nhưng không phát minh stable code mới.
- D5: hệ thống hiện có audit append path nhưng chưa chứng minh immutable storage hay đủ producer. Quyết định append-only và fail-closed là policy; retention/durability/coverage vẫn cần owners.
- D6: permission membership không thay thế state machine, domain source hoặc side-effect contract. Không có evidence để kết luận từng operation mới là active hay chính thức deferred; quyết định per-operation còn BLOCKED. Tạm thời không triển khai/hiển thị operation chưa có approval.

## 3. Exact permission set được duyệt cho role

Ba mã hiện có giữ nguyên tên và semantics hiện hữu:

- organization.create
- platform.health.read
- platform.audit.read

37 mã mới được chấp thuận là **membership trong effective permission set của PLATFORM_OPERATOR V1**, nhưng chưa được bật trong runtime:

1. platform.dashboard.summary.read
2. platform.organizations.organization.read
3. platform.organizations.status.manage
4. platform.organizations.usage.read
5. platform.users.account.read
6. platform.users.profile.manage
7. platform.users.status.manage
8. platform.memberships.membership.read
9. platform.memberships.invitation.create
10. platform.memberships.lifecycle.manage
11. platform.memberships.roles.manage
12. platform.projects.project.read
13. platform.projects.metadata.manage
14. platform.projects.visibility.manage
15. platform.projects.members.manage
16. platform.projects.leaders.manage
17. platform.sessions.session.read
18. platform.sessions.session.revoke
19. platform.audit.event.export
20. platform.services.health.read
21. platform.services.metrics.read
22. platform.jobs.job.read
23. platform.jobs.job.retry
24. platform.jobs.job.cancel
25. platform.jobs.job.requeue
26. platform.rag.indexes.read
27. platform.rag.indexes.rebuild
28. platform.ai.runtime.read
29. platform.ai.runtime.manage
30. platform.llm.providers.read
31. platform.llm.providers.manage
32. platform.integrations.integration.read
33. platform.integrations.integration.manage
34. platform.incidents.incident.read
35. platform.incidents.incident.manage
36. platform.diagnostics.record.read
37. platform.support.actions.manage

No Configuration, Feature Flag, Migration, Recovery, wildcard or other permission is added. Existing standalone A-04 assignments are not rewritten or automatically backfilled. A successful operator assignment must represent the full exact set under the approved atomic grant operation; a partial set is not an operator role.

## 4. Operation disposition

**Existing baseline operations (preserve unchanged):** PLAT-ORG-01 → organization.create; PLAT-HEALTH-01 → platform.health.read; PLAT-AUDIT-01 → platform.audit.read.

**BLOCKED / NOT ACTIVE — pending owner disposition:** all 37 newly mapped operations. Each must be explicitly approved active with a complete operation record, or explicitly deferred from V1 by its authorized domain owner. The list maps one-to-one to the new permission codes above:

- PLAT-DASH-01
- PLAT-ORG-02..04
- PLAT-USER-01..03
- PLAT-MEM-01..04
- PLAT-PROJ-01..05
- PLAT-SEC-01..02
- PLAT-AUDIT-02
- PLAT-SVC-01..02
- PLAT-JOB-01..04
- PLAT-RAG-01..02
- PLAT-AI-01..02
- PLAT-LLM-01..02
- PLAT-INT-01..02
- PLAT-INC-01..02
- PLAT-SUP-01..02

Configuration has no operation in active V1. The exact catalog and current evidence gaps are in §6 and §9 of the [canonical contract](../platform-operator-v1-contract.md).

Mỗi operation record phải ghi: exact permission và disposition; tên/nhóm domain owner và ngày duyệt; lựa chọn active hay deferred cùng lý do/evidence; actor eligibility; server-side target/scope checks; preconditions/state transition/concurrency; input/output allowlist; replay/idempotency; side effects/cost/rollback; audit event/fields/reason/failure; HTTP status/stable error/body/concealment; evidence/test oracle; và task con được mở. Chỉ ghi “chưa triển khai” không phải disposition cuối cùng.

## 5. Jira reconciliation and implementation readiness

Jira descriptions were updated and re-read on 2026-10-16:

- DATN-293 marks Platform Configuration deferred from active V1 by the DATN-301 owner disposition; DEC-ACCESS-09 itself leaves configuration read/write `FUTURE / DECISION_REQUIRED`.
- DATN-294 records the partial policy disposition and remaining owner sign-offs.
- DATN-295/296 explicitly gate bootstrap and implementation on the missing Security/IAM runbook and audit evidence.
- DATN-297/299 exclude Configuration and gate every operation whose per-operation disposition is not approved; their current descriptions distinguish blocked from explicitly deferred.
- DATN-298/300 gate UI and acceptance on operation-level approval and verify unapproved operations stay inactive.
- DATN-301 remains In Progress and continues to block DATN-295–300. Those links remain valid because issuer/recovery, audit retention/coverage, resource concealment classification and per-operation dispositions remain open. The 37 new operations are not approved active or approved deferred.

Configuration scope reconciliation is complete. Do not remove implementation blockers yet.

| Child | Readiness |
|---|---|
| DATN-295 DB | **BLOCKED** — exact-permission and atomic grant/revoke policy is decided; issuer/runbook, audit retention/coverage and persistence details remain open. |
| DATN-296 BE Administration | **BLOCKED** — bootstrap issuer/recovery and per-operation admin disposition/semantics/audit/error details remain open. |
| DATN-297 BE Operations | **BLOCKED per operation** — domain owners must approve active semantics or explicitly defer; Configuration is out of scope. |
| DATN-298 FE Administration | **BLOCKED** — consume only approved BE operations/capabilities; bootstrap, error and audit contracts are incomplete. |
| DATN-299 FE Operations | **BLOCKED per operation** — no UI for an operation without an approved active disposition; Configuration is out of scope. |
| DATN-300 QA | **BLOCKED for acceptance** — derive test oracles from approved operation records and audit/security contract after owners complete them. |

No task dependency is removed and no child is marked Ready based on this decision record alone.

## 6. Remaining owner actions

1. **Security/IAM:** name the authorized issuer and executor, identity-verification source, approval evidence and complete bootstrap/recovery/revoke/rollback runbook. Record approver name/group, date and evidence.
2. **Security/IAM:** approve the audit retention period and its enforcement boundary.
3. **Security/Audit/domain owners:** complete D5 producer coverage, required fields/reason, redaction, read/export/denial treatment and audit failure/durability behavior.
4. **Authorized domain owners:** for each of the 37 operations, explicitly approve `ACTIVE` with a complete operation decision record and test oracle, or explicitly approve `DEFERRED FROM V1` with rationale. Record owner identity, date and evidence. Until then, mark it `BLOCKED / NOT ACTIVE`; do not infer deferral.
5. **DEC-ACCESS-10 owner:** classify which resource types require concealment/404 and update dependent API/security/FE acceptance. The shared access-readiness record already carries the KeyT-approved baseline.
6. Reassess DATN-301 acceptance only after these items are reflected in canonical docs and Jira. Until then, keep DATN-301 In Progress and DATN-295–300 blocked.

## 7. DATN-295 gate

DATN-295 is **not ready to implement**. The policy now fixes the 40-code set and exact-assignment atomicity, but Jira's existing acceptance also depends on an operable first-operator bootstrap and durable audit path. Security/IAM have not yet named the issuer/executor; retention and audit persistence/coverage are also unresolved. DATN-295 may prepare non-binding design notes, but must not add runtime codes, implement bootstrap, seed an operator, or claim readiness until those blockers are approved.

## 8. Change boundary

This decision record changes documentation and Jira scope only. It does not change runtime authorization, permissions in DATN_BE, schema/index/migration, API, FE, audit storage, production configuration, status of child tasks or issue links. Any database implementation requires its own migration/rollout/rollback review.
