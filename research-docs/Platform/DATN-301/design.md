# DATN-301 — Decision record: PLATFORM_OPERATOR V1 policy

| Trường | Giá trị |
|---|---|
| Jira | [DATN-301](https://trankimthang0207.atlassian.net/browse/DATN-301) |
| Canonical contract | [PLATFORM_OPERATOR V1 Contract](../platform-operator-v1-contract.md) |
| Ngày ghi nhận | 2026-10-16 (Asia/Bangkok) |
| Trạng thái | Phê duyệt một phần; implementation vẫn bị chặn |
| Người đưa ra disposition | KeyT, explicit approval in this conversation |
| Phê duyệt còn bắt buộc | Security/IAM: issuer/bootstrap/recovery, retention/enforcement; Security/Audit/domain owners: event coverage/fields/read-denial policy; authorized domain owners: operation dispositions; DEC-ACCESS-10 owner: concealment resource classes |

## 1. Phạm vi và cách đọc

Đây là bản ghi policy cho sáu nhóm quyết định trong DATN-301. Disposition được KeyT xác nhận ngày 2026-10-16. Giữ implementation gated khi thiếu issuer/runbook, retention/enforcement, audit coverage/storage evidence, operation disposition hoặc phân loại resource concealment.

- APPROVED POLICY là quyết định phạm vi/authorization, không tự thêm quyền vào runtime hoặc làm operation/API sẵn sàng.
- DEFERRED là không thuộc active V1; không tạo permission, endpoint hay UI tương ứng.
- OUTSIDE ACTIVE CATALOG là mapping chưa được duyệt thành operation V1; bị chặn triển khai cho đến khi có disposition. Thiếu approval không tự trở thành quyết định `DEFERRED FROM V1`.
- BLOCKED dùng cho gate implementation/decision đang chờ evidence; không phải operation disposition.
- Giữ nguyên authentication, Organization/Project ACL, tenant-content boundary và nguyên tắc không trả secret.
- Không có permission wildcard, Break-glass, hidden account, credential bypass hoặc production seed.

## 2. Decision record

| Nhóm | Disposition ngày 2026-10-16 | Phạm vi đã chốt | Còn mở / owner ký |
|---|---|---|---|
| D1 — Permission set và assignment | **APPROVED POLICY** | PLATFORM_OPERATOR policy set có đúng 40 exact permission codes: 3 mã DATN-79/A-04 hiện có và 37 mã mới ở §3. Không wildcard. Tiếp tục lưu exact permission assignments, không yêu cầu role/bundle row. Full-set grant/revoke atomic, all-or-nothing; partial/corrupt set không resolve thành full operator set. Mọi operation mới phải có đủ full set hiện hành và exact code operation; ba endpoint A-04 giữ nguyên single-code behavior. Giữ nguyên standalone A-04 behavior; không tự backfill/đổi mã. | DATN-295/296 chọn DB transaction, idempotency, race handling và xác minh persistence theo atomic audit boundary. Security/IAM + DB owner còn phải quyết định regrant sau revoke và cách full-set grant/revoke tương tác với standalone A-04 rows dưới unique index hiện tại; không được đổi 40 mã. |
| D2 — Bootstrap và recovery | **PARTIAL / BLOCKED** | Authentication bắt buộc; issuer không được tự cấp cho chính mình; recipient là user hiện hữu và ACTIVE; cấp/thu hồi chính xác cả 40 assignment; không seed, hidden account hay Break-glass. Grant/revoke all-or-nothing, audit chung durable commit boundary. Không có operator-initiated grant/revoke API trong baseline. | Security/IAM phải chỉ định issuer/executor, identity evidence, approval/change record, first grant, mất operator duy nhất, can-operator-grant-others, last-operator removal, revoke/session outcome, assignment provenance/regrant, concurrency/idempotency, rollback và hậu kiểm. Chưa có issuer/runbook nên chưa thể mở DATN-295/296. |
| D3 — Platform Configuration | **APPROVED: DEFERRED FROM V1** | DEC-ACCESS-09 hiện ghi configuration read/write là `FUTURE / DECISION_REQUIRED`; KeyT disposition trong DATN-301 loại Platform Configuration khỏi active V1. Scope DATN-293 và DATN-297/299 đã được reconcile. Không có platform configuration permission, operation, API hay UI trong V1. Không suy ra quyền quản lý platform configuration từ LLM/Integration operation riêng. | Chỉ mở lại bằng decision mới và amendment được duyệt cho DEC-ACCESS-09 cùng permission/API/secret boundary. |
| D4 — Error và concealment | **PARTIAL — baseline approved; missing-vs-forbidden/resource classes open** | Giữ 401 khi unauthenticated/invalid session; 403 khi authenticated nhưng thiếu permission; dùng 404 chỉ cho resource class mà concealment policy đã chỉ định. 422 cho validation/state input không hợp lệ; 409 cho conflict/stale/duplicate; 503 cho dependency unavailable; 500 cho unexpected failure. Response dùng envelope IAM hiện tại (code, message, details, requestId) theo allowlist an toàn; không lộ resource bị che, topology, stack, secret hoặc raw payload. Hành vi chính xác với target không tồn tại so với target tồn tại nhưng không được phép chưa được chốt theo từng resource class. | KeyT đã duyệt baseline; owner DEC-ACCESS-10 cần ghi resource classes và missing-vs-forbidden outcome/concealment. Stable code và field-level body allowlist vẫn do operation owner chốt. |
| D5 — Audit | **PARTIAL / BLOCKED** | Operator API không sửa/xóa audit history. Privileged mutation fail closed: không success nếu audit chưa durable. Contract yêu cầu state change và audit chung durable commit boundary; external side effect cần durable intent+audit trước dispatch hoặc operation stays outside active catalog. Secret/credential/raw tenant content không vào response/audit. | Security/IAM ký retention/enforcement. Security/Audit/domain owners chốt producers, fields/reason, redaction, read/export/denial coverage and durability evidence. Không tuyên bố database-level tamper-proof hay universal outbox. |
| D6 — Semantics operation | **PARTIAL / EXTERNAL APPROVAL REQUIRED — 37 mappings outside active catalog** | Ba operation DATN-79 hiện có giữ nguyên hành vi theo A-04. 37 mapping mới chưa phải operation trong active V1 catalog; không có disposition `ACTIVE` hoặc `DEFERRED FROM V1` nào được owner duyệt. Mỗi operation cần owner decision record/test oracle hoặc rationale/evidence cho deferral. | Domain owner phải ghi approver, ngày, evidence, semantics/test oracle hoặc deferral rationale. Giữ child tasks gated theo nội dung liên quan. Missing approval không phải quyết định defer. |

### Evidence and rationale

- D1: DATN-79/A-04 có chính xác 3 mã hiện hữu; DATN-294 matrix có chính xác 37 mã mới. User chốt bundle hữu hạn 3 + 37, exact assignment và atomic grant/revoke. Không đổi ba mã A-04.
- D2: A-04 chứng minh exact-permission assignment, active-subject checks và platform login/refresh; login dùng password, active user, rate-limit/MFA và fresh A-04 authority; refresh revalidates current authority. Nó không chỉ định issuer/bootstrap/recovery. Security/IAM ký phần này; không lấp khoảng trống bằng seed hay hidden path.
- D3: DEC-ACCESS-09 ghi config read/write là `FUTURE / DECISION_REQUIRED`; KeyT đã duyệt disposition riêng của DATN-301 là loại Platform Configuration khỏi active V1. Không gán quyết định này ngược lại cho DEC-ACCESS-09.
- D4: A-04 hiện có 401/403; DATN_BE đang có IAM error envelope code/message/details/requestId và các status convention. Decision chốt mapping/allowlist, nhưng không phát minh stable code mới.
- D5: A-04 Organization provisioning writes its audit event in the same Mongo transaction and tests show audit failure rolls back the business records. This supports the contract's shared durable commit boundary; it does not prove audit immutability or universal producer coverage. Retention/enforcement and coverage remain owner decisions.
- D6: permission membership không thay thế state machine, domain source hoặc side-effect contract. 37 mappings nằm ngoài active catalog và bị chặn triển khai; chưa có evidence để kết luận operation nào active hay chính thức deferred. Không triển khai/hiển thị operation chưa có approval.

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

**Outside the active V1 catalog — external owner disposition required:** all 37 newly mapped operations. Each must be explicitly approved `ACTIVE` with a complete operation record, or explicitly `DEFERRED FROM V1` by its authorized domain owner. No row has either disposition yet; the lack of approval is not a deferral. The list maps one-to-one to the new permission codes above:

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
- PLAT-DIAG-01
- PLAT-SUP-01

Configuration has no operation in active V1. The exact catalog and current evidence gaps are in §6 and §9 of the [canonical contract](../platform-operator-v1-contract.md).

Mỗi operation record phải ghi: exact permission và disposition; tên/nhóm domain owner và ngày duyệt; lựa chọn active hay deferred cùng lý do/evidence; actor eligibility; server-side target/scope checks; preconditions/state transition/concurrency; input/output allowlist; replay/idempotency; side effects/cost/rollback; audit event/fields/reason/failure; HTTP status/stable error/body/concealment; evidence/test oracle; và task con được mở. Chỉ ghi “chưa triển khai” không phải disposition cuối cùng.

## 5. Jira reconciliation and implementation readiness

Jira descriptions were updated and re-read on 2026-10-16:

- DATN-293 marks Platform Configuration deferred from active V1 by the DATN-301 owner disposition; DEC-ACCESS-09 itself leaves configuration read/write `FUTURE / DECISION_REQUIRED`.
- DATN-294 records the partial policy disposition and remaining owner sign-offs.
- DATN-295/296 explicitly gate bootstrap and implementation on the missing Security/IAM runbook and audit owner decisions; the contract now states the shared durable commit boundary for assignment + audit.
- DATN-297/299 exclude Configuration and gate every operation whose per-operation disposition is not approved; their current descriptions distinguish blocked from explicitly deferred.
- DATN-298/300 gate UI and acceptance on operation-level approval and verify unapproved operations stay inactive.
- DATN-301 remains In Progress and continues to block DATN-295–300. Those links remain valid because issuer/recovery, audit retention/coverage, resource concealment classification and per-operation dispositions remain open. The 37 new operations are not approved active or approved deferred.

Configuration scope reconciliation is complete. Do not remove implementation blockers yet.

| Child | Readiness |
|---|---|
| DATN-295 DB | **BLOCKED** — exact-permission and atomic grant/revoke policy plus the state+audit durable commit invariant are decided; issuer/runbook, retention/enforcement, event schema and DB-specific persistence design remain open. |
| DATN-296 BE Administration | **BLOCKED** — bootstrap issuer/recovery and per-operation admin disposition/semantics/audit/error details remain open. |
| DATN-297 BE Operations | **BLOCKED per operation** — domain owners must approve active semantics or explicitly defer; Configuration is out of scope. |
| DATN-298 FE Administration | **BLOCKED** — consume only approved BE operations/capabilities; bootstrap, error and audit contracts are incomplete. |
| DATN-299 FE Operations | **BLOCKED per operation** — no UI for an operation without an approved active disposition; Configuration is out of scope. |
| DATN-300 QA | **BLOCKED for acceptance** — derive test oracles from approved operation records and audit/security contract after owners complete them. |

No task dependency is removed and no child is marked Ready based on this decision record alone.

## 6. Remaining owner actions

1. **Security/IAM:** name the authorized issuer and executor, identity-verification source, approval evidence and complete bootstrap/recovery/revoke/rollback runbook. Record approver name/group, date and evidence.
2. **Security/IAM + DB:** decide how a full-set grant/revoke treats any pre-existing standalone A-04 assignments and how regrant-after-revoke is represented under the current one-row-per-subject/permission/scope unique index; approve any needed provenance/migration change.
3. **Security/IAM:** approve the audit retention period and its enforcement boundary.
4. **Security/Audit/domain owners:** complete producer coverage, required fields/reason, redaction, read/export/denial treatment, retention enforcement and evidence that every operation meets the shared durable commit boundary.
5. **Authorized domain owners:** for each of the 37 mappings, explicitly approve `ACTIVE` with a complete operation decision record and test oracle, or explicitly approve `DEFERRED FROM V1` with rationale. Record owner identity, date and evidence. Until then keep it outside the active catalog and blocked from implementation; do not infer a final operation status or deferral.
6. **DEC-ACCESS-10 owner:** classify which resource types require concealment/404 and update dependent API/security/FE acceptance. The shared access-readiness record already carries the KeyT-approved baseline.
7. Reassess DATN-301 acceptance only after these items are reflected in canonical docs and Jira. Until then, keep DATN-301 In Progress and DATN-295–300 blocked.

## 7. DATN-295 gate

DATN-295 is **not ready to implement**. The policy fixes the 40-code set and exact-assignment atomicity; the contract also requires the assignment change and grant/revoke event to share a durable commit boundary with rollback/no success on audit failure. Security/IAM have not named the issuer/executor or signed the runbook; Security/IAM + DB have not decided full-set grant/revoke interaction with legacy A-04 rows or regrant-after-revoke; retention/enforcement and event coverage remain open. DB-specific persistence design must meet the invariant and existing unique-index behavior. DATN-295 may prepare non-binding design notes, but must not add runtime codes, implement bootstrap, seed an operator, or claim readiness until those owner decisions are approved.

## 8. Change boundary

This decision record changes documentation and Jira scope only. It does not change runtime authorization, permissions in DATN_BE, schema/index/migration, API, FE, audit storage, production configuration, status of child tasks or issue links. Any database implementation requires its own migration/rollout/rollback review.
