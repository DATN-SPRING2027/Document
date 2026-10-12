# DATN-94 — D-02 version, conflict, replay và Handover review

**Revision:** D02-R1, 12/10/2026 (Asia/Saigon). **Status:** PROPOSED / UNKNOWN.
[DATN-114](https://trankimthang0207.atlassian.net/browse/DATN-114).
Nguồn E01–E13/B1–B10 và [state/guard contract](16-task-v1-state-machine-contract.md)
giữ nguyên. Đây là lựa chọn Task-specific để review, không HTTP/OpenAPI/schema
đã accepted và không áp dụng contract/TTL/errors của Organization DATN-87.
[Scenario oracles](18-task-v1-state-machine-oracles.md) truy vết từng quyết định.

## 1. Accepted invariant và phần cần chọn

| Concern | Đã APPROVED | Chi tiết còn UNKNOWN |
|---|---|---|
| Task/history | B4/E02 Decision 7: mutation và append-only task_events atomic trong Task DB | Exact version/CAS, event shape, failure/retry/output D02-05/10 |
| Handover | B6/E02 Decision 6: Task API assignment có operation ID, idempotency, retry/compensation; không chung DB transaction | Key scope, payload, horizon, coordinator và recovery rules D02-06–09 |
| Provenance | B7/E02 Decision 7–8: actor/source/changed metadata/version/time/operation/correlation; Agent + initiating user nếu áp dụng, không raw prompt | Names/types/visibility/retention và compliance sink D02-10 |
| Authorization | B8–B10/E05/E12; current authorized scope/ACL | Revoke/write fence và delegated identity protocol D02-04; không dùng RoleAssignment làm membership |

## 2. D02-05 — version/CAS và stale conflict

**Đề nghị:** một monotonic aggregate version cho Task; mọi committed state,
assignment hoặc editable-field mutation dùng cùng CAS. Command mới phải có
expectedVersion do server cấp; server không tin version client làm giá trị mới.
Compare actual scoped Task + version tại conditional write; chỉ một concurrent
mutation cùng version có thể commit. Version/history cũng trong transaction B4.
Không auto-refetch rồi tự reapply một ý định stale.

Alternative: opaque ETag với equivalent CAS (che implementation nhưng debug
khó hơn); version theo từng field giảm false conflicts nhưng tăng phối hợp
status/assignee/history. Đề nghị aggregate version cho V1 để tránh transition
commit dưới assignee cũ. Initial value, numeric bounds/overflow, wire ETag vs
body token, create behavior và exact stale response vẫn cần Q3/Q6/Q7.

| Situation | Outcome PROPOSED | Version/history/retry | Accepted |
|---|---|---|---|
| Fresh new command, all guards + approved edge + expectedVersion match | Commit một lần | Version tăng một lần và H+; trả safe committed result | UNKNOWN D02-05/10 |
| Fresh new command thiếu/malformed version | Precondition validation denial | Không write; không suy default; client lấy token đúng | UNKNOWN D02-05/10 |
| Fresh new command token cũ, Task đã đổi | Stale conflict | Không state/assignment/version/history delta; refetch authorized Task và human reconfirm, command ID mới | UNKNOWN D02-05/07/10 |
| Hai IDs khác nhau cùng expectedVersion | Một commit tối đa, loser stale/conflict | Không retry loser bằng current version tự động; verify transaction serialization | UNKNOWN D02-05 |
| Role/membership/ACL revoke racing mutation | Không write từ stale authority | Owner chọn freshness/fence proof; CAS Task một mình không fence IAM/ACL changes | UNKNOWN D02-04/05 |
| Abort trước commit hoặc commit outcome chưa biết | Failure/uncertain outcome được phân biệt | Resolve operation cùng ID trước khi thử mutation mới; retry transaction theo approved driver policy | UNKNOWN D02-05/07/10 |

**Câu hỏi gửi API/DB reviewer:** “Chọn aggregate monotonic version hay opaque
token với CAS equivalent? Chốt create initial token, wire representation,
version increment, malformed/missing/stale response, transaction retry và
revocation fence. Duyệt cross-command CAS: assignment/update/state cùng version;
không retry stale intent tự động. Ghi exact API/DB revision và approver.”

## 3. D02-06 — operation-ID scope và fingerprint

**Đề nghị:** operation identity là `(Organization, Task, stable caller principal,
operation-ID)`; command type và accepted semantic payload nằm trong fingerprint.
Một ID dùng cho command khác cùng namespace phải mismatch, không tạo hai
mutation. Principal là authenticated user với human command; Handover là
authenticated logical calling service ổn định qua retry, với initiating human,
handover/item identity được bind vào semantic payload. Client không tự chọn
principal. Correlation ID đổi giữa attempts, không phải idempotency identity.

Fingerprint đề nghị gồm command type, target Task/scope, expectedVersion,
target state/assignee, normalized reason và các business input của command;
Handover thêm stable intent/item ID + initiating human. Không gồm transport
token, retry timestamp/correlation ID. Normalization/absent-vs-null, length,
ID grammar, fingerprint algorithm và versioning phải chốt ở Q3/Q6/Q7; không
hash raw body rồi coi hai payload tương đương khi chúng có semantics khác.

Alternative: `(Organization, principal, operation-ID)` toàn service giúp phát
hiện reuse trên Task khác nhưng tăng contention và cần privacy-safe lookup.
Không include command type trong key vì sẽ che nhầm-ID đổi command; giữ nó
trong fingerprint. Principal per HTTP session gây mất replay khi session đổi;
principal ổn định tránh lỗi đó nhưng yêu cầu current authorization mỗi attempt.

**Câu hỏi gửi API/Security reviewer:** “Duyệt namespace trên hay namespace
toàn Task Service? Chốt stable Handover service principal/delegated initiator,
ID grammar và fingerprint fields/normalization. Same ID khác command/target
trong cùng namespace phải mismatch; new correlation/session không tạo operation
mới. Recovery thay initiating actor phải là command mới được authorize riêng?”

## 4. D02-07 — replay resolution, mismatch và concurrency

**Đề nghị processing order:** validate trusted identity/context và request
shape; evaluate current applicable guards/command authority + safe replay
projection; resolve operation record; chỉ command chưa commit mới evaluate
current state/expectedVersion/reason và CAS. Exact committed replay không được
đòi current Task version vẫn bằng expectedVersion hoặc version result cũ.
Điều này giữ retry an toàn sau lost response dù Task đã tiếp tục thay đổi.
Replay trả acknowledgement của operation cũ, không tuyên bố đó là Task hiện tại;
đọc current Task qua authorized read riêng nếu cần. Không trả cached Task body
khi ACL đã đổi. Rule mới này là đề nghị D-02 với lý do riêng, không approval K4.

| Operation observation | Outcome PROPOSED | Side effects / retry | Accepted |
|---|---|---|---|
| Absent, current guards pass | Evaluate new command và CAS | Mutation + H+ + durable committed operation result cùng transaction đề nghị | UNKNOWN D02-05/06/07 |
| Committed, cùng namespace + fingerprint | Replay minimal safe original operation result | Không CAS lại, không version/event tăng; current auth vẫn bắt buộc, kể cả sau resource đổi | UNKNOWN D02-07/10 |
| Same ID, semantic payload/command/expectedVersion khác | Payload mismatch | Không mutate hoặc overwrite stored result; sửa intent → new ID + current token | UNKNOWN D02-06/07/10 |
| Same ID/same fingerprint đến đồng thời | Single winner, contender resolve/wait bounded hoặc retry-later | Không trả fake success khi chưa commit; không execute independent second mutation | UNKNOWN D02-07/10 |
| Current membership/ACL/action authority đã mất sau first commit | Authorization denial | Không cached content/replay disclosure; khôi phục quyền không tự undo first commit | UNKNOWN detailed D02-04/07/10; B8/B10 vẫn bắt buộc |
| Operation có transient abort chưa commit | Retry same ID sau fresh auth + state/CAS validation | Không claim permanent business success; retry ceiling/backoff cần owner chọn | UNKNOWN D02-07/10 |
| Validation/authorization/transition/stale denial | Không persist success result theo đề nghị | Không Task mutation/history; exact negative-result caching/denial audit policy cần chọn | UNKNOWN D02-07/10 |

**Durability proposal:** committed result và dedup identity trong cùng Task
transaction với mutation/history; nếu result write thất bại thì abort tất cả.
Đây là mở rộng Q7 cần DB approval, không phải invariant operation-store đã có
trong B4. Redis claim/lock có thể tối ưu contention nhưng không thay durable
commit proof: crash giữa Task commit và Redis write không được tạo duplicate.
Alternative: recover operation proof từ unique operation identity trong history;
ít record hơn nhưng replay projection/retention khó tách. Không chọn collection,
index, TTL hoặc migration tại D02-R1.

**Câu hỏi gửi API/DB reviewer:** “Duyệt current-auth → committed replay trước
fresh-state/CAS? Duyệt original minimal acknowledgement, negative-result caching,
in-flight wait/retry behavior và atomic operation-result durability? Chốt exact
success/mismatch/stale/in-flight/abort error DTOs, không copy IAM HTTP mapping.”

## 5. D02-08 — expiry và late replay

**Đề nghị:** operation-ID không tái sử dụng. Logical replay window W được
chọn từ maximum Handover retry/recovery horizon cộng safety margin; cần owner
xác nhận duration cụ thể. Sau W, giữ compact dedup tombstone/proof gắn với
Task/history retention, trả expired-operation denial hoặc recovery-required,
không coi expired ID là operation absent rồi execute lại. Đọc Task/operation
proof qua authorized recovery flow trước new intent. Exact tombstone retention,
Task deletion/retention và khả năng replay sau W vẫn UNKNOWN Q7/Q8.

Alternative: không expire operation proof trong V1 (an toàn retry, storage tăng);
hoặc giữ result ngắn rồi tombstone dài (ít content retention, thêm recovery path).
Chỉ physical TTL deletion sẽ mất dedup proof và có thể double-apply khi timeout
retry đến muộn; TTL cleanup không định nghĩa business expiry. Không dùng invite
7 ngày, key TTL của DATN-87 hoặc TTL Jira research làm W của Task.

**Câu hỏi gửi Ops/DB/API reviewer:** “Chọn no-expiry V1 hay window W + tombstone?
Nếu W, cung cấp retry/recovery horizon, safety margin, duration và proof retention
sau W. Chọn late-replay response/recovery owner; xác nhận expired key không
được tự execute như new operation, kể cả cleanup chạy chậm hoặc đã xóa result.”

## 6. D02-09 — Handover retry/compensation

Baseline B6 không đòi hai services commit atomically. Đề nghị Handover làm
coordinator intent: record stable item/operation ID trước request, Task là owner
assignment canonical; Handover acknowledgement chỉ được ghi sau commit proof.
Eligible states/target/scope cần D02-01/04, release/API/data contract cần Q1–Q3/Q6.

| Failure boundary | Recovery PROPOSED | Actor/version/history / ownership | Accepted |
|---|---|---|---|
| Request chưa đến Task | Retry same operation ID/payload | Fresh delegated auth; Task mới evaluate CAS, Handover giữ pending intent | UNKNOWN D02-09 |
| Task abort trước commit | Retry same ID chỉ cho transient failure | Reason/target/CAS còn hợp lệ; deterministic denial trả coordinator để user sửa intent | UNKNOWN D02-07/09 |
| Task commit, response mất | Resolve/replay same ID | Không gán lần hai; original resultVersion không current TaskVersion | UNKNOWN D02-07/09 |
| Task commit, Handover local ack write lỗi | Retry reconcile Handover ack từ Task operation proof | Không rollback Task trực tiếp; Task history giữ commit lần đầu | UNKNOWN D02-09 |
| User muốn hủy Handover sau Task đã assign | Compensation là authorized Task command mới | New operation ID + current CAS + eligible target; append compensating history, không xóa event cũ | UNKNOWN D02-04/05/09/10 |
| Assignee/state/quyền đã đổi sau first commit | Không tự restore assignee cũ | Reconcile proof riêng; compensation conflict → manual authorized resolution owner | UNKNOWN D02-04/09 |
| Retry horizon hết / proof không còn / service down lâu | Recovery-required, không đoán success | Handover owner giữ unresolved item; hỏi authorized Task state/proof, không direct DB fallback | UNKNOWN D02-08/09/10 |

Alternative: always compensate khi Handover ack lỗi có thể ghi đè việc sau đó;
reconcile-first giữ canonical Task và append-only history, đổi lại cần pending
recovery queue/owner. Không tự tạo coordinator states/queue/API trong repo.

**Câu hỏi gửi Handover/Product/API reviewer:** “Chốt coordinator và stable
intent/item identity, Task commit proof/query, bounded retry/horizon và manual
recovery owner. Duyệt reconcile-first; compensation phải là command mới có
current CAS/authorization, không automatic restore. Successor eligibility,
Handover states và replay projection được owning contracts nào duyệt?”

## 7. D02-10 — response, history và failure contract

Đề nghị command-specific acknowledgement tối thiểu có operation identity,
Task identity, committed result version và outcome/replay indication; safe
history có actor/source/from-to/changed metadata, version, time, operation và
correlation theo B7. Exact names/types/nullability, event vocabulary/reason
visibility, redaction và history ordering/retention phải Q6/Q8 approval.
Auth/denial/validation/stale/mismatch/in-flight/expired/storage failure/uncertain
commit cần từng response và precedence; không tự quyết 401/403/404/409/422
hoặc response body từ DATN-87/Project. Domain history khác compliance audit;
Task compliance sink còn Q8. Conditional outbox B4 chỉ kích hoạt nếu Q9 đã chọn
consumer; email/Notification của DATN-87 không chọn consumer cho Task.

**Câu hỏi gửi API/Security/History reviewer:** “Duyệt exact acknowledgement,
error/precedence/disclosure và event/projection/retention table cho từng profile
P-M/P-X/replay. Reason ai đọc được? Denial audit ở đâu? Có compliance sink hoặc
async consumer nào được Task owner chọn? Ghi partial items, revision và authority.”
