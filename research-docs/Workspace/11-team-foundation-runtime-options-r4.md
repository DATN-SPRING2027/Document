# DATN-90 — R4: phương án cần chọn trước Team runtime

Ngày: **2026-10-15 ICT**. Trạng thái: **PROPOSAL — CHƯA CHỌN, CHƯA ENABLE RUNTIME**.
Jira: [DATN-90](https://trankimthang0207.atlassian.net/browse/DATN-90).

## 1. Reviewer cần duyệt gì?

R4 đề nghị chọn **P1–P5** bên dưới để hoàn thiện phần contract còn mở.
**P6 là kế hoạch/bằng chứng triển khai cần có**, không phải kết quả test đã đạt.
Reviewer trả lời từng mục bằng `A`, `B`, `AMEND: <giá trị cuối>` hoặc
`DEFER: <operation chưa bật>`. Ví dụ: `P1=A; P2=A; P3=AMEND: ...; P4=A;
P5=A; P6=chấp nhận checklist, evidence còn NOT READY`.

Nhận xét chất lượng tài liệu hoặc merge PR công bố proposal không thay câu trả
lời lựa chọn policy và không chứng minh provisioning/transaction/transport đã sẵn sàng.
Khi có quyết định, cập nhật đúng giá trị đã chọn cùng nguồn/ngày/revision; không
xin duyệt lại danh tính người đã chốt bảng TQ trước đó.

PR này thêm **tài liệu mới** để reviewer có diff cụ thể:

- File này: phương án A/B, trade-off, quyết định cần trả và điều kiện nghiệm thu.
- [Candidate OpenAPI](contracts/c-05-team-foundation-r4.openapi.json): 6 operation,
  đánh dấu `PROPOSED_NOT_APPROVED`/`NOT_READY`, không thay owning BE OpenAPI.
- [Ma trận 41 kịch bản](contracts/c-05-team-foundation-r4.scenarios.json): mọi case
  `NOT_RUN_API_CONTRACT_GATE`; là kế hoạch coverage, không phải 41 API tests pass.

Không có code ứng dụng, schema, migration, seed, grant, handler hoặc dữ liệu trong
PR tài liệu này. Diff schema follow-up của DATN-254 giữ ở DB branch riêng; khi
bàn giao thay đổi đó cần DB PR riêng. Không ghép DB diff vào R4.

## 2. Phần đã duyệt giữ nguyên

Nguồn quyết định: [DATN-89](https://trankimthang0207.atlassian.net/browse/DATN-89),
[partial decision record §10.1](09-team-management-foundation-decision-gap-report.md#101-jira-decision-update--2026-10-14).

- TQ-01–04 đã chọn metadata/normalization/lifecycle ACTIVE–ARCHIVED/retained records;
  Team thuộc một Project, parent/code immutable, không move/merge/hard delete;
  không bootstrap member/leader/grant, membership commands thuộc DATN-92.
- Create thiếu description → server materialize `null`; null/empty hợp lệ.
  Schema required không đồng nghĩa client bắt buộc gửi description.
- TQ-05 chọn không cấp quyền ngầm; exact grants/provisioning còn mở.
- TQ-06 chọn missing/stale proof → deny, không cascade; generation implementation
  vẫn DEFER tới khi có owner/writer inventory/race evidence.
- TQ-07 chọn ranh giới route ownership; exact HTTP/DTO/query/transport còn conditional.
- TQ-08 chọn shared ErrorResponse; Team mapping/precedence cần reconcile.
- TQ-09 đã chọn version, scoped key/fingerprint, application expiry/CAS. Provider,
  all-writer coverage và ambiguous-commit recovery chưa có đủ evidence.
- TQ-10 vẫn DEFER về canonical audit mapping/atomicity.

[BE PR #33](https://github.com/DATN-SPRING2027/DATN-BE/pull/33) merge
`24853d13588de23fbe701530da705abb12e27979` lúc **2026-10-15 02:17:07 ICT** chỉ có
read-only preflight/rules/fixture/CI, không merge runtime schema hoặc Team API.
R4 không yêu cầu review lại PR đó hoặc các quyết định đã chọn ở trên.

## 3. Tóm tắt lựa chọn

| Mục / owner | A — khuyến nghị | B — lựa chọn thay thế / trade-off |
|---|---|---|
| P1 — IAM/Security, TQ-05 | Project-scoped TEAM_LEADER có đúng action + team.children.manage; đọc cần team.read; không quyền ngầm | Create còn cần team.read: tiện read-after-create nhưng ràng buộc thêm command với read; cần chốt rõ. Team-only leader tiếp tục ngoài MVP |
| P2 — Product/IAM/Security, TQ-05/06/07 | Slice đầu chỉ delegated manager metadata reads; member-facing reads hoãn tới khi admission provider đạt proof | Bật cả Team-member reads theo R2: đủ UX sớm hơn nhưng phải có current effective admission proof; không fallback Project membership/public Project |
| P3 — API/Gateway/BFF/IAM, TQ-07 | 6 operation và DTO/query/header tại §5; page1/size20/max100; strong If-Match; status filter cho manager | List chỉ paging ACTIVE, hoãn status filter và archived list; giảm query/UX phạm vi. Các route/body/header khác giữ §5; route khác phải ghi AMEND chính xác |
| P4 — API/Security, TQ-08 | Reuse auth hiện tại và shared envelope; mapping/precedence §6 | Dùng generic RESOURCE_NOT_FOUND và context403 ORGANIZATION_CONTEXT_REQUIRED như R2: ít resource codes hơn nhưng khác IAM auth/context401 hiện tại, cần owning auth contract amend trước |
| P5 — Architecture/Audit/IAM/DB, TQ-10 | Direct audit vào continuum_audit.audit_logs_iam, atomic cùng Team + command result; mapping §7 | Team + outbox atomic, relay eventual canonical audit: tăng availability nhưng thay consistency, thêm relay/dedup/lag/recovery/DB scope; cần AMEND invariant rõ trước triển khai |
| P6 — owning IAM/Org/Project/Security/DB/Gateway | Giữ mọi write chưa enabled đến khi checklist §8 có evidence; không thêm generation từ proposal | Hoãn toàn bộ Team runtime, giữ preflight-only lâu hơn; không dùng snapshot/Redis-only hoặc placeholder handler để thay proof |

## 4. P1/P2 — exact quyền và phạm vi

| Operation | Action code đề nghị | Delegation / actor |
|---|---|---|
| Create | team.create | team.children.manage; current Project-scoped TEAM_LEADER |
| Update | team.update | như Create, Team ACTIVE |
| Archive | team.archive | như Create, parent Project ACTIVE |
| Restore | team.restore | như Create, parent Project ACTIVE |
| List/detail ở P2=A | team.read | team.children.manage; current Project-scoped TEAM_LEADER |

Mỗi actor cần ACTIVE User, ACTIVE OrganizationMembership đúng trusted context,
ACTIVE Project/ProjectMembership, current RoleAssignment/Role resolution khớp
scope, applicable DENY/UNKNOWN thắng. ADMIN/platform/public Project/creator không
được grant ngầm. Delegated manager không cần TeamMembership để create hoặc quản lý.
Create chưa có Team nên không thể đòi actor có admission vào Team chưa tồn tại.

P2=A chỉ thu hẹp slice triển khai ban đầu, không phán quyết MEMBER vĩnh viễn bị
cấm đọc. P2=B theo R2 cần team.read trên Project-scoped MEMBER/TEAM_LEADER **và**
TeamMembership effective ACTIVE/current admission; delegated manager có
team.read + team.children.manage vẫn đọc metadata ACTIVE/ARCHIVED. Ordinary member
chỉ thấy Team ACTIVE của mình; stale/missing admission deny; không lộ profile,
offboarding metadata hoặc content của owning domain khác.

Nếu P1=B, Create phải có cả team.create + team.children.manage + team.read.
IAM/Security phải xác nhận chính xác codes/scope/provisioning trong owning work
package; PR tài liệu này không tự provision. Tests tối thiểu: thiếu từng grant,
role mismatch, sibling Project, deny/unknown, revoked permission, manager không
TeamMembership và không fallback role/public/creator.

## 5. P3 — 6 operation, DTO/query/transport đề nghị

Các path dưới đây có prefix `/api/v1/iam`.

| Method/path | Body/query | Success / headers |
|---|---|---|
| POST /projects/{projectId}/teams | name, code, description? | 201 Team; ETag; Location /api/v1/iam/teams/{id}; Idempotency-Key, không If-Match |
| PATCH /teams/{teamId} | name?, description?, ít nhất một field | 200 Team; ETag; If-Match + Idempotency-Key |
| GET /projects/{projectId}/teams | page, pageSize, status | 200 TeamList; không aggregate ETag |
| GET /teams/{teamId} | không query | 200 Team; ETag |
| POST /teams/{teamId}/archive | reason | 200 Team; ETag; If-Match + Idempotency-Key |
| POST /teams/{teamId}/restore | reason | 200 Team; ETag; If-Match + Idempotency-Key |

Strict body/query allowlist; scope/IDs/status/version/timestamps do server quản
lý; create parent Project phải khớp trusted Organization. Name NFC+trim1–200
code points; code trim+ASCII uppercase rồi regex `^[A-Z][A-Z0-9_-]{1,31}$`.
Description nullable tối đa2000 code points, giữ TAB/LF nhưng cấm C0 khác/DEL,
không trim; create thiếu→null, PATCH thiếu→giữ nguyên/null→clear. Reason trim1–500
code points, cấm C0/DEL. Không normalize/backfill legacy data.

Team DTO exact: id, organizationId, projectId, name, code, description, status,
version, createdAt, updatedAt, archivedAt, archivedBy; không archivedReason,
generation, member profile/count/content/capabilities. UTC timestamps trailing Z.
TeamList `{data,pagination:{page,pageSize,totalItems,totalPages}}`; page mặc định1,
pageSize20/max100; A: status ACTIVE(default)/ARCHIVED/ALL cho manager, không search/
custom sort; order createdAt DESC,id DESC; filter scope/visibility trước paging/
totals. Empty totalPages0; beyond-last data=[] giữ totals; không cross-request
snapshot guarantee. Với P2=B, ordinary member chỉ status ACTIVE; filter vượt
quyền trả403, không tự bỏ qua. P3=B chỉ paging và ACTIVE list, không nhận status.

Strong ETag `"team:<id>:<version>"`; If-Match đúng một tag, không weak/wildcard/
multiple; no-store. Business change tăng version1; no-op giữ version/updatedAt,
lưu result nhưng không business audit. Full next-state validation + scoped CAS,
không dựa riêng vào Mongoose query validators. Parent/code immutable mọi writer.

TQ-09 đã chọn: key ASCII1–128 `[A-Za-z0-9._:-]+`, scope organizationId+actorUserId+key;
fingerprint method+normalized path+canonical validated body+precondition; result/
mutation/audit cùng transaction; retention24h; application expiry/terminal-slot
replace-CAS theo R3; TTL chỉ cleanup. Replay revalidate current auth/action/
visibility rồi trả original status/body/ETag; Location chỉ áp dụng cho Create.
New key so current version.

Browser BFF→Gateway→IAM theo trusted auth/context hiện hành; candidate mutation
yêu cầu CSRF header khớp __Host-csrf cookie, theo membership commands hiện có;
không tự mở bearer exemption. Forward Idempotency-Key/If-Match và trả ETag/
Location/Idempotency-Replayed/Retry-After. Gateway allowlist ở24853d1 thiếu
If-Match request/ETag response; cần owner thay ở implementation PR riêng và
test xuyên luồng. Không quota mới;429 chỉ theo owning Gateway policy thực áp dụng.

Tests tối thiểu: omitted/null/extra/control/Unicode bounds; scope injection;
query arrays/operators/bounds/hidden totals/stable sort; ETag syntax; exact replay
vs new-key stale; no-op timestamp; BFF/Gateway header+CSRF/context spoof checks.

## 6. P4 — ErrorResponse và precedence đề nghị

Giữ shared `{code,message,details,requestId}`;5xx details={}; không secret/DB error.

| Trường hợp | A — status/code |
|---|---|
| Auth/current Organization context không hợp lệ | 401 AUTHENTICATION_FAILED theo IAM hiện hành |
| CSRF không hợp lệ | 403 AUTH_CSRF_INVALID |
| Malformed/missing/invisible parent hoặc Team | 404 PROJECT_NOT_FOUND cho create/list;404 TEAM_NOT_FOUND cho detail/mutations |
| Visible resource nhưng thiếu action/delegation | 403 TEAM_ACTION_FORBIDDEN |
| Sai body/query/header syntax | 422 VALIDATION_FAILED |
| Thiếu Idempotency-Key | 422 IDEMPOTENCY_KEY_REQUIRED |
| Duplicate scoped code / key khác fingerprint | 409 TEAM_CODE_EXISTS / IDEMPOTENCY_KEY_REUSED |
| Thiếu If-Match / valid stale If-Match | 428 PRECONDITION_REQUIRED / 412 PRECONDITION_FAILED |
| Visible update vào Team archived | 409 TEAM_ARCHIVED; archive same-state vẫn no-op sau kiểm quyền/precondition |
| Provider/provisioning chưa sẵn sàng | 503 TEAM_POLICY_NOT_READY, không fallback allow |
| Hết bounded contention/recovery chưa xác định | 503 RETRY_LATER, Retry-After:1; giữ cùng key, không blind second mutation |
| Write/audit failure / internal read failure | 500 TEAM_COMMAND_FAILED / TEAM_READ_FAILED, không success giả |

Precedence A: auth/context → CSRF mutation → shape (malformed path ID404) → scoped
visibility → current action/delegation → command header presence/syntax → scoped
key/fingerprint/replay → new-command version → state → transaction/fences/write/
audit. Body hợp lệ + hidden phải404 trước key/version/result; body sai có thể422
trước lookup. Gateway rate/middleware policy là boundary riêng cần kiểm chứng.

B chỉ đổi not-found sang RESOURCE_NOT_FOUND và context sang403
ORGANIZATION_CONTEXT_REQUIRED; phải amend owning auth contract, không tự remap
mọi401 thành403. Các mapping khác giữ A; thay đổi khác ghi AMEND chính xác.
Tests tối thiểu: unauth+invalid body, CSRF+hidden, hidden+stale/key, visible-noaction
+missing key, stale+archived, sanitized details/requestId và no cross-scope leaks.

## 7. P5 — audit đề nghị

A: `continuum_audit.audit_logs_iam`, cùng Mongo client/session với Team + durable
command result; commit/abort cùng nhau. Actions TEAM_CREATED, TEAM_METADATA_UPDATED,
TEAM_ARCHIVED, TEAM_RESTORED; targetResource=Team; stable targetResourceId=teamId.
Envelope organizationId/projectId/actorUserId/action/targetResource/
targetResourceId/occurredAt; metadata allowlist teamId/commandId/oldVersion/
newVersion, lifecycle reason, before/after name/status, descriptionChanged.
Không full description/request/profile/token. Append-only, không TTL/delete,
không Team history/outbox trong MVP. No-op/replay không business event mới.
Dedup `(organizationId,metadata.commandId,action,targetResourceId)` chỉ cho Team
events có commandId qua partial index; không tác động legacy audit records.
Nếu cần field/index/collection mới phải có DB branch/PR riêng.

B: atomic Team+outbox rồi relay idempotent tới canonical audit. Cần owner AMEND
consistency rõ ràng, chọn canonical mapping và thêm relay/dedup/lag/availability/
recovery contract, tests và owning DB/ops scope. Có outbox ở domain khác không tự
cho phép Team eventual audit. Không lựa chọn nào được xem là đạt atomicity chỉ
vì reviewer đồng ý thiết kế.

Authority chọn ADR-003/SPEC-001 đúng revision để đối chiếu hoặc explicitly chấp
nhận mapping A cho Team. Không bịa revision của hai tài liệu gốc chưa tìm thấy.
Tests tối thiểu: cross-DB commit, late audit failure rollback Team/result/event,
replay/no-op dedup, privacy allowlist và restore giữ lịch sử archive trước đó.

## 8. P6 — evidence cần cung cấp, không xin xác nhận PASS khi chưa chạy

| Evidence | Owner / điều kiện tối thiểu | Hiện tại |
|---|---|---|
| Exact grant provisioning | IAM/Security; approved codes/scope + provisioning/readiness evidence riêng | NOT READY |
| Parent provider + mọi writer | IAM/Org/Project/User/Role owners; writer inventory gồm suspend/remove/rejoin, lifecycle, RoleAssignment/Role edits, seed/import/repair/external deployments; chọn protocol trước code generation | NOT READY |
| Current-authority race | Session-bound proof/fences; replica-set barrier cho revoke trước/sau Team commit, fresh evidence khi retry, parent rejoin không revive stale admissions | NOT READY |
| Scoped idempotency/recovery | R3 expiry/CAS mọi writer; fault injection committed/aborted/unresolved commit, một effect/event, không replay revoked actor | NOT READY |
| Audit | P5 chọn xong + same-session commit/late-failure rollback (hoặc B consistency/relay evidence đã amend) | NOT READY |
| Transport | Gateway/BFF/IAM chọn forwarding/CSRF/context; tests xuyên luồng headers và concealment | NOT READY |
| DB dependency | Schema follow-up review/merge riêng; legacy mapping/migration/cutover chỉ trong work package được cấp quyền; không shared DB từ R4 | NOT READY |

P6=A chấp nhận checklist để triển khai evidence trong owning work packages, không
approve generation fields/protocol hoặc provider chưa thiết kế. P6=B giữ
preflight-only; không mở handler/write path phụ thuộc missing contract. Test
mechanics generic V4 không thay Team provider/all-writer/TTL-monitor/unknown-commit proof.

Khi đủ decisions và dependencies, thực hiện **255 Create →256 Update →257
List/detail →258 Archive/restore →259 API tests**. Reads không đòi write audit/
idempotency proof, nhưng vẫn cần read grants/parent proof/exact contract và DB
dependency của chính slice đó. Status phản ánh công việc thực tế; DATN-90/255–259
còn In Progress theo lần đọc2026-10-15; agent được user trao quyền cập nhật theo
mốc. Không đánh dấu implementation Done từ tài liệu hoặc test plan.

## 9. Provenance và verification của PR tài liệu

Document base `2b737e862e6eb4169d342750324bef15808128a2`; BE inspected source
`24853d13588de23fbe701530da705abb12e27979`. Đối chiếu ErrorResponse/auth/provider/
Gateway/sessionless audit/outbox theo các path trong candidate provenance.
41 scenarios trace về C255–C258; P1↔C255-03/C256-02/C258-02;
P2↔C257-01; P3↔C255-01/02/05,C256-01/03/04,C257-02/03,C258-01/03;
P4↔C255-06/C256-03/C257-04/C258-04; P5↔C255-08/C256-04/C258-04;
P6↔C255-04/07 và các readiness conditions chung.

Candidate mô tả normalization/control checks bằng normative text/vendor extension;
generic JSON/OpenAPI validator không tự thực hiện NFC/trim/authorization/CAS.
Kiểm PR: JSON/local refs, shared ErrorResponse exact, scope6 operations, scenario
IDs/traceability, Markdown links và diff-check. Không chạy Team API acceptance,
DB/provider/race/transport tests từ PR docs này. Baseline85 unit/120 migration-plan
đã chạy trong preparation có log local, không biến41 candidate scenarios thành PASS.
