# DATN-301 — Decision worksheet và thiết kế chốt policy

| Trường | Giá trị |
|---|---|
| Jira | [DATN-301](https://trankimthang0207.atlassian.net/browse/DATN-301) |
| Nguồn contract | [DATN-294 — PLATFORM_OPERATOR V1 Contract](../platform-operator-v1-contract.md) |
| Trạng thái | Draft để review; nội dung ở cột “hướng đề xuất” không phải phê duyệt |
| Nguyên tắc | Chỉ evidence hiện có được coi là baseline; policy mới cần đúng owner duyệt |

## 1. Cách đọc worksheet

- **Evidence** ghi điều đã được nguồn hiện có xác nhận.
- **Hướng đề xuất** nêu phương án nên đem ra review, không cấp quyền và không thay owner quyết định.
- **Disposition** phải được owner ghi là `APPROVE`, `MODIFY`, `REJECT` hoặc `DEFER`, kèm tên/nhóm, ngày, rationale và evidence.
- Nếu chưa có quyết định có thẩm quyền, giữ `BLOCKED`/`DEFERRED`; không chuyển proposal thành allow, deny hay API contract.

## 2. Những ràng buộc đã xác nhận

1. Chỉ một role V1 là `PLATFORM_OPERATOR`; không chia Observe/Operate/Security/Break-glass, không role hierarchy.
2. Authentication và authorization middleware hiện hành vẫn bắt buộc. Không tự suy ra tenant membership, Project ACL hoặc quyền đọc nội dung.
3. Secret/credential không trả ra API/FE; privileged mutation phải được audit.
4. Không wildcard, hidden account, credential bypass, production seed hoặc Break-glass trong V1.
5. Giữ nguyên ba permission hiện có: `organization.create`, `platform.health.read`, `platform.audit.read` cho tới khi có phê duyệt riêng.
6. Runtime hiện chỉ có các permission chính xác theo A-04; assignment lưu một permission/scope mỗi record. Chưa có role bundle và chưa có bootstrap issuer được xác nhận.

Nguồn: DATN-79/A-04 evidence được DATN-294 ghi ở §3; quyết định V1 đã được người yêu cầu xác nhận; contract DATN-294 vẫn là review draft.

## 3. D1 — Disposition cho 37 permission proposal

DATN-294 §5.2 là matrix chuẩn để xem mô tả chi tiết, scope, authorization, visibility, audit và evidence từng mã. Bảng sau giúp owner ghi quyết định mà không phải suy rộng theo domain. Cả 37 mã đều hiện là `PROPOSED`, không có mã nào được cấp trong runtime.

| # | Permission từ DATN-294 | Disposition | Owner / ngày / rationale |
|---:|---|---|---|
| 1 | `platform.dashboard.summary.read` | `TBD` | — |
| 2 | `platform.organizations.organization.read` | `TBD` | — |
| 3 | `platform.organizations.status.manage` | `TBD` | — |
| 4 | `platform.organizations.usage.read` | `TBD` | — |
| 5 | `platform.users.account.read` | `TBD` | — |
| 6 | `platform.users.profile.manage` | `TBD` | — |
| 7 | `platform.users.status.manage` | `TBD` | — |
| 8 | `platform.memberships.membership.read` | `TBD` | — |
| 9 | `platform.memberships.invitation.create` | `TBD` | — |
| 10 | `platform.memberships.lifecycle.manage` | `TBD` | — |
| 11 | `platform.memberships.roles.manage` | `TBD` | — |
| 12 | `platform.projects.project.read` | `TBD` | — |
| 13 | `platform.projects.metadata.manage` | `TBD` | — |
| 14 | `platform.projects.visibility.manage` | `TBD` | — |
| 15 | `platform.projects.members.manage` | `TBD` | — |
| 16 | `platform.projects.leaders.manage` | `TBD` | — |
| 17 | `platform.sessions.session.read` | `TBD` | — |
| 18 | `platform.sessions.session.revoke` | `TBD` | — |
| 19 | `platform.audit.event.export` | `TBD` | — |
| 20 | `platform.services.health.read` | `TBD` | — |
| 21 | `platform.services.metrics.read` | `TBD` | — |
| 22 | `platform.jobs.job.read` | `TBD` | — |
| 23 | `platform.jobs.job.retry` | `TBD` | — |
| 24 | `platform.jobs.job.cancel` | `TBD` | — |
| 25 | `platform.jobs.job.requeue` | `TBD` | — |
| 26 | `platform.rag.indexes.read` | `TBD` | — |
| 27 | `platform.rag.indexes.rebuild` | `TBD` | — |
| 28 | `platform.ai.runtime.read` | `TBD` | — |
| 29 | `platform.ai.runtime.manage` | `TBD` | — |
| 30 | `platform.llm.providers.read` | `TBD` | — |
| 31 | `platform.llm.providers.manage` | `TBD` | — |
| 32 | `platform.integrations.integration.read` | `TBD` | — |
| 33 | `platform.integrations.integration.manage` | `TBD` | — |
| 34 | `platform.incidents.incident.read` | `TBD` | — |
| 35 | `platform.incidents.incident.manage` | `TBD` | — |
| 36 | `platform.diagnostics.record.read` | `TBD` | — |
| 37 | `platform.support.actions.manage` | `TBD` | — |

### Quyết định role/bundle đi kèm

Sau khi disposition từng mã, owner cần chốt:

- `PLATFORM_OPERATOR` được resolve thành **chính xác** tập mã nào; mọi mã `DEFER`/`REJECT` không được cấp.
- Ba mã DATN-79 hiện có liên hệ thế nào với role này; không đổi assignment cũ hoặc buộc người đang giữ chúng vào bundle nếu chưa có quyết định riêng.
- Source of truth là role/bundle assignment được resolve sang exact codes hay nhiều exact permission assignments; cách version hóa bundle và hành vi khi registry đổi.
- Grant/revoke có atomic không; nếu lưu nhiều record thì partial failure, retry, duplicate, concurrent grant/revoke và rollback được xử lý thế nào.
- Capability response cho FE được tính ở server thế nào; không tin role claim hoặc scope/parent ID do client gửi.

**Hướng đề xuất để review:** giữ role là một bundle hữu hạn, có version, gồm đúng những permission đã được phê duyệt; không wildcard. Chưa chọn mô hình lưu DB hay ngữ nghĩa atomicity thay cho owner và DATN-295.

**Owner cần ghi:** Platform product owner + IAM/Authorization owner; DB owner tham gia nếu lựa chọn làm thay đổi assignment storage/lifecycle.

## 4. D2 — Người và quy trình bootstrap/recovery

| Câu hỏi bắt buộc | Evidence hiện có | Hướng đưa ra quyết định | Disposition |
|---|---|---|---|
| Ai có thẩm quyền cấp operator đầu tiên? | A-04 hiện cho biết assignment exact-permission; issuer bootstrap chưa xác định | Ghi rõ role/người hoặc quy trình vận hành được ủy quyền; xác định bằng chứng phê duyệt | `TBD` |
| Xác minh issuer và recipient ra sao? | Actor runtime phải authenticated và ACTIVE; chưa có identity-verification runbook | Định nghĩa nguồn danh tính, approver, recipient eligibility và bằng chứng lưu | `TBD` |
| Cấp bundle bằng đường nào? | Không có bundle/issuer runtime được xác nhận | Chọn API được phân quyền hoặc quy trình kiểm soát ngoài ứng dụng; ghi owner, transaction boundary, rollback | `TBD` |
| Chống self-grant, duplicate và race thế nào? | No-self-grant là baseline; concurrency/bundle atomicity chưa chốt | Chốt invariant, uniqueness/idempotency, version/CAS và kết quả partial failure | `TBD` |
| Mất operator duy nhất thì xử lý sao? | Không có recovery authority; Break-glass không thuộc V1 | Ghi đường recovery có định danh, thẩm quyền, audit, revoke/rollback và hậu kiểm; không tạo đường vòng ngầm | `TBD` |
| Thu hồi/đổi người vận hành thế nào? | Assignment có revoked state; hiệu lực lifecycle/session cần contract | Chốt revoke authority, hiệu lực request/session đang hoạt động, verification và operator coverage | `TBD` |

**Hướng đề xuất để review:** không có tự cấp quyền, seed hoặc bypass. Bootstrap và recovery phải là một quy trình tường minh có issuer chịu trách nhiệm, recipient ACTIVE, audit evidence và xác minh sau thao tác. Ai là issuer, phê duyệt đơn/người đôi, công cụ thực hiện và điều kiện phục hồi vẫn là lựa chọn cần owner duyệt.

**Owner cần ghi:** IAM/Authorization + Security/Platform operations. Nếu yêu cầu vận hành thủ công, cần runbook do owner chịu trách nhiệm, không dừng ở câu “manual process”.

## 5. D3 — Configuration và DEC-ACCESS-09

**Evidence:** DEC-ACCESS-09 hiện hoãn config read/write; DATN-293 liệt kê Configuration trong đề xuất phạm vi; DATN-294 chưa có permission/operation Configuration active và đánh dấu conflict.

| Lựa chọn | Hệ quả phải ghi | Hiện trạng |
|---|---|---|
| A. Tiếp tục defer trong V1 | Sửa/reconcile phạm vi DATN-293 và DATN-295–299; ghi rõ không có config permission/operation; giữ secret management ở boundary riêng | **Hướng đề xuất theo evidence hiện có**, cần owner xác nhận scope |
| B. Đưa Configuration vào V1 | Sửa DEC-ACCESS-09 theo quy trình; xác định từng operation, safe metadata, secret reference/value boundary, approval, audit, API/schema, rollout và tests trước khi giao child task | Chưa được duyệt; không triển khai |

**Owner cần ghi:** DATN-293/Platform product owner + Security + chủ sở hữu Configuration/secret-management. Không diễn giải việc quản lý integration/LLM provider là tự động cho phép quản lý cấu hình nền tảng.

## 6. D4 — Error và concealment

| Trường hợp | Baseline có evidence | Cần owner chốt |
|---|---|---|
| Chưa authenticated / credential không hợp lệ | Giữ authentication và A-04 behavior | Chỉ thay khi có decision auth chính thức |
| Đã authenticated nhưng thiếu permission | A-04 xác nhận thiếu quyền bị từ chối; current baseline có 403 | Có áp dụng concealment theo loại resource/operation không |
| Resource không tồn tại so với ngoài scope/ACL | DEC-ACCESS-10 còn mở trong hồ sơ DATN-294 | Chọn 404 concealment, 403 phân biệt, hay policy theo resource; response phải nhất quán và không tạo side channel |
| Input không hợp lệ / chuyển trạng thái sai | Error matrix mới chưa duyệt | Chốt status + stable code + safe message + field details cho validation |
| Stale version / conflict / duplicate | Idempotency, CAS và conflict behavior còn proposal theo operation | Chốt 409/other mapping, retryability, operation ID và client recovery |
| Dependency unavailable / unexpected failure | Mapping chưa duyệt | Chốt retryable status, `Retry-After` nếu dùng, correlation ID, safe response và logging |

**Hướng đề xuất để review:** giữ nguyên authentication/authorization behavior A-04 đã có; dùng DEC-ACCESS-10 làm nơi chốt concealment. Mọi response/log/error chỉ trả thông tin an toàn, không lộ secret, topology, raw payload hoặc sự tồn tại của resource ngoài policy. Status/code cụ thể vẫn `TBD` cho đến khi owner phê duyệt.

**Owner cần ghi:** IAM/Authorization + Security; API/FE/QA xác nhận tính nhất quán và test oracle.

## 7. D5 — Audit

### Evidence và invariant đã nêu

- A-04 có audit cho provisioning và projection bounded cho audit read; code hiện tại chưa chứng minh immutable storage hoặc đủ event producers.
- V1 đã xác nhận privileged mutations phải được audit và secrets/credentials không được trả ra API/FE.
- Audit history không được chỉnh/xóa qua quyền PLATFORM_OPERATOR trong contract draft.

### Những lựa chọn chưa được phê duyệt

| Trục quyết định | Cần xác định cụ thể | Owner |
|---|---|---|
| Bất biến toàn vẹn | Append-only ở application, DB enforcement, tamper evidence; actor nào được phép thay đổi retention/archive | Security + DB/Audit |
| Event coverage | Mọi mutation; có/không log privileged reads, exports, denied attempts; sự kiện bundle/bootstrap/revoke và failure | Security + IAM + domain owners |
| Event schema | Actor, target, action, timestamp, result, operation/correlation ID; trường nào bắt buộc reason; before/after tối thiểu | Security + Audit |
| Redaction | Allowlist và denylist cho identity, diagnostics, request metadata; loại trừ secret, token, password, payload/content | Security + data owners |
| Retention/export | Thời hạn, legal/operational basis, export limits, quyền đọc/export, log việc đọc/export | Data/Security + Platform |
| Audit failure | Mutation có fail closed, durable buffer/outbox hay trạng thái pending; đảm bảo không báo success khi audit chưa bền vững | Security + DB/BE + SRE |

**Hướng đề xuất để review:** không tuyên bố immutable/complete trước khi có bằng chứng triển khai; event cần đủ để truy vết actor → action → target → result mà không lưu secret/content. Security owner phải quyết định audit failure và retention; kỹ thuật phải chứng minh invariant bằng test/DB control sau khi chọn.

## 8. D6 — Worksheet semantics cho operation

DATN-294 §6 là inventory operation. Với từng operation còn active, owner/domain owner cần hoàn tất các trường dưới đây; operation thiếu quyết định thì `DEFERRED`, không có API bật.

| Nhóm / operation IDs theo DATN-294 | Quyết định semantics cần ghi | Evidence gap đang nêu trong contract |
|---|---|---|
| Dashboard `PLAT-DASH-01` | Metric definitions, aggregation window, source, freshness, dimensions, owner, empty/partial source behavior | Dashboard source/owner chưa xác định |
| Organization `PLAT-ORG-01..04` | Lifecycle transition, eligibility, reason, version/CAS, repeated request, usage source/units | Organization status/counter chưa có trong schema |
| User `PLAT-USER-01..03` | Field allowlist, suspend/reactivate, self/last-operator protections, session/token effect, reactivation | User lifecycle and last-operator rules chưa chốt |
| Membership `PLAT-MEM-01..04` | Tương tác C-02: invite, suspend/remove, role transitions, last ADMIN, self-action, cross-org | Quy tắc precedence/actor cho platform role chưa chốt |
| Project `PLAT-PROJ-01..05` | Metadata allowlist, visibility, membership/leader actions, ACL preservation, no content access | Composition của platform operation với DATN-82 cần owner duyệt |
| Session `PLAT-SEC-01..02` | Read projection (IP/UA hay không), session revoke, repeated revoke, active token effect | IP/UA privacy và session lifecycle còn mở |
| Audit `PLAT-AUDIT-01..02` | Filter allowlist, page/limit/export cap, redaction, read/export audit | Read logging/export behavior còn mở |
| Health/service `PLAT-HEALTH-01`, `PLAT-SVC-01..02` | Health vs metrics, service allowlist, dimensions, freshness, dependency failures | Chỉ IAM process liveness được xác nhận; metrics source chưa có |
| Job `PLAT-JOB-01..04` | Eligible states, retry budget, cancelability, requeue dedupe, idempotency, payload redaction | State machine/owner API chưa có |
| RAG `PLAT-RAG-01..02` | Index owner resolution, rebuild scope, duplicate/in-flight behavior, content/chunk boundary | Shared API/owner, rebuild semantics chưa có |
| Laya/LLM `PLAT-AI-01..02`, `PLAT-LLM-01..02` | Finite command list, provider/model transition, health result, secret reference, rollback | Control API and exact command set chưa có |
| Integration `PLAT-INT-01..02` | Enable/disable/reconnect transitions, dependency side effects, retries, secret reference | Shared control/secret API chưa có |
| Incident `PLAT-INC-01..02` | Create/update/resolve states, immutable history, reason/version, safe summaries | Incident lifecycle contract chưa có |
| Diagnostics/support `PLAT-SUP-01..02` | Source, exact identifiers, time window, payload allowlist, sanitization, each permitted support action | Catalogue/source/window/sanitization/action list chưa có |

### Operation decision record template

Copy một record cho từng operation được giữ lại:

```text
Operation ID / permission:
Disposition: APPROVE | MODIFY | REJECT | DEFER
Owner(s) and approval date:
Actor eligibility and exact authorization evidence:
Target resolution and scope/relationship checks:
Preconditions and state transition:
Input/output allowlist and concealed fields:
Idempotency, duplicate/replay, CAS and concurrent-request behavior:
Side effects, cost, reversibility and rollback:
Audit event, required reason, failure behavior:
HTTP/status + stable error code/body and concealment:
Evidence/source and test oracle:
Downstream tasks unblocked:
```

## 9. Nguồn có thể bất đồng và cách đồng bộ

- [DATN-294 contract](../platform-operator-v1-contract.md) chứa proposal/matrix hiện tại, không phải implementation approval.
- [Actors, Roles and Permissions](../../02_ACTORS_ROLES_AND_PERMISSIONS.md) và [Security and Governance](../../../architecture/05_SECURITY_AND_GOVERNANCE.md) có mô tả tổng quát cũ rằng platform operator theo dõi configuration; mô tả đó không đủ thay thế DEC-ACCESS-09 hoặc tạo config permission.
- DEC-ACCESS-09 là evidence hoãn config read/write; DATN-293 cần được reconcile bằng owner thay vì diễn giải scope cho phù hợp một phía.
- DEC-ACCESS-10 được DATN-294 ghi là còn mở; chỉ decision owner mới chọn missing-vs-forbidden behavior.
- Sau phê duyệt, cập nhật canonical contract và các nguồn liên quan trong cùng handoff. Không sửa quyết định gốc hoặc đánh dấu child unblock nếu chưa theo thẩm quyền của từng nguồn.

## 10. Phiếu phê duyệt tổng hợp

| Nhóm | Disposition | Người/nhóm duyệt | Ngày | Evidence / decision URL | Task con được mở |
|---|---|---|---|---|---|
| D1 — 37 mã / bundle | `TBD` | — | — | — | — |
| D2 — Bootstrap / recovery | `TBD` | — | — | — | — |
| D3 — Configuration | `TBD` | — | — | — | — |
| D4 — Error / concealment | `TBD` | — | — | — | — |
| D5 — Audit | `TBD` | — | — | — | — |
| D6 — Operation semantics | `TBD` | — | — | — | — |

**Readiness:** `NOT READY`. Worksheet này ghi nhận vấn đề, evidence và lựa chọn để review; không tự phê duyệt một policy nào, không thay DATN-294 và không gỡ dependency DATN-295–300.

## 11. Cổng bắt đầu riêng cho DATN-295

### Evidence BE hiện hành

Đối chiếu DATN-BE `main` tại [`3b839198cfcbc40d6b11e1167ae8c68c54afea99`](https://github.com/DATN-SPRING2027/DATN-BE/commit/3b839198cfcbc40d6b11e1167ae8c68c54afea99):

- [DEC-ACCESS-09](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/docs/decisions/dec-access-09-platform-operator-authorization.md) hiện `PARTIAL overall`; A-04 chỉ duyệt đúng `organization.create`, `platform.health.read`, `platform.audit.read`. Không có permission A-04 mới nào được duyệt trong quyết định này. `platform.configuration.read/write` vẫn `FUTURE / DECISION_REQUIRED`.
- [A-04 implementation record](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/docs/decisions/a-04-platform-operator-authorization-implementation.md) xác nhận model hiện hành là assignment theo từng subject + exact permission + `PLATFORM`; không phải một role-bundle record. Schema chỉ enum ba mã đã duyệt; index unique theo `(subjectUserId, permission, scope)`. Record có trạng thái, grant/revoke attribution/time và optional expiry.
- Cùng implementation record ghi rõ chưa có issuer/bootstrap/recovery mechanism được duyệt; không thêm public grant/revoke API hoặc seed. Grant/revoke audit producer và event contract vẫn là follow-up.
- DEC-ACCESS-09 cho phép ranh giới business là authority riêng, platform-scoped; collection/entity/index/migration cụ thể thuộc implementation design. Điều đó không tự duyệt một role bundle 37 mã hay thao tác cấp bundle.

### Kết luận readiness

| Điều kiện của DATN-295 | Evidence hiện tại | Kết luận |
|---|---|---|
| Exact permission set cho `PLATFORM_OPERATOR` | A-04 duyệt 3 mã; 37 mã DATN-294 là proposal; scope Configuration mâu thuẫn với DEC-ACCESS-09 | **BLOCKED** — cần owner phê duyệt/amend scope và disposition exact 37 mã |
| Representation của role/bundle và grant/revoke | BE có per-permission assignments; chưa có role bundle, bundle version, atomic grant/revoke hoặc partial-failure contract | **BLOCKED** — DATN-295 không được tự chọn role row hay multi-assignment bundle |
| Bootstrap/recovery đáp ứng acceptance của DATN-295 | Issuer, recipient verification, assignment route/runbook và recovery authority chưa được quyết định | **BLOCKED** — task không thể tuyên bố bootstrap hoạt động theo contract |
| Audit của grant/bootstrap/revoke | Có attribution fields trên assignment; event producer/schema/failure/retention chưa được duyệt | **BLOCKED** nếu DATN-295 cần tạo audit persistence hoặc ghi event trong cùng transaction |
| Error/concealment DEC-ACCESS-10 | A-04 giữ 401/403 và 404 theo policy resource-hiding; body/problem codes còn mở | Không chặn schema-only design nếu không mở API; vẫn chặn API contract/BE task |
| Semantics các operation domain | Nhiều operation còn cần state machine/source/side-effect owner | Không chặn authority storage thuần túy nếu permission disposition đã được duyệt; vẫn chặn operation implementation tương ứng |

Jira [DATN-295](https://trankimthang0207.atlassian.net/browse/DATN-295) còn yêu cầu migration/schema được review và bootstrap operator hoạt động theo contract. Vì vậy chỉ thu hẹp task xuống migration/schema cũng chưa đủ để đạt acceptance hiện tại; cần owner quyết định rõ phần bootstrap/audit hoặc sửa phạm vi và dependency trước.

**Kết luận:** với evidence hiện tại, DATN-295 chưa đủ điều kiện bắt đầu implementation theo Jira acceptance. Có thể làm design spike cho mô hình hiện có, nhưng không được thêm 37 code vào schema/migration, tạo role bundle, seed/grant operator hoặc bỏ dependency trước khi owner chốt ba điều kiện chính: exact permission/scope, storage/atomicity model, và issuer/bootstrap/audit path. D4/D6 có thể tiếp tục chặn các API/operation downstream nếu được tách rõ khỏi phần authority DB.

### Đề xuất để owner duyệt — không phải quyết định

1. Giữ `platform_authority_assignments` tách biệt khỏi Organization roles; đây là boundary đã có evidence. Chọn rõ giữa (A) tiếp tục lưu một exact permission mỗi assignment và cấp/thu hồi cả bundle trong transaction, hoặc (B) thêm một platform role-assignment record trỏ tới một bundle version hữu hạn. Không chọn dựa vào convenience; phải xác định deny/partial-assignment semantics và cách giữ ba code A-04 tương thích.
2. Disposition từng 37 mã trong §3; nếu giữ đúng intent full Platform Administration, phê duyệt tập mã hữu hạn chính xác. Configuration cần lựa chọn riêng vì DEC-ACCESS-09 hiện hoãn nó.
3. Ghi issuer, xác minh danh tính, no-self-grant, approval evidence, cấp/thu hồi nguyên tử, audit event và recovery/rollback runbook. Không mặc định API, seed, một hay hai người duyệt.
4. Chỉ sau các approval trên mới mở DATN-295. DEC-ACCESS-10 và semantics operation có thể tiếp tục là dependency riêng cho DATN-296–300 nếu task DB được giới hạn đúng và decision owner đồng ý.
