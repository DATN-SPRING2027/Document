# DATN-94 — D-02 scenario/oracle matrix và decision closure

**Revision:** D02-R1, 12/10/2026 (Asia/Saigon). **Status:** review preparation.
[DATN-115](https://trankimthang0207.atlassian.net/browse/DATN-115).
Nguồn/authority ở [D-02 contract §1](16-task-v1-state-machine-contract.md);
outcomes candidates ở [reliability review](17-task-v1-command-reliability-review.md).
Tái sử dụng AT-01–09/TV-01–22 của [D-01 validation](15-task-v1-review-validation.md),
thêm concrete operation/CAS/replay/compensation obligations riêng cho D-02.

## 1. Test gate và oracle vocabulary

**APPROVED_BOUNDARY:** invariant có authority, ví dụ unauthorized không mutate
hoặc Task/history cùng commit/rollback. Exact executable assertion có thể còn
blocked bởi DTO/state/error/event decision. **BLOCKED_SELECTION:** expected
detail chưa được accepted; cột proposal là hypothetical oracle để reviewer
chọn. Không đặt test PASS cho hypothetical behavior.

Executable behavior tests **NOT RUN / BLOCKED**: E11 chưa có Task implementation
và approved state/edge/actor/outcome contract chưa có. Không chạy Project/IAM
suite để lấy bằng chứng Task, không tạo state fixtures/mock engine từ proposal.
Checks links/table/coverage/authority/whitespace chỉ là kiểm tra tài liệu.

Sau sign-off: mỗi executable case ghi accepted decision/revision, fixture và
scope evidence, command, expected output, Task/version/history before/after,
observed assertions và suite/CI run. Test atomicity/concurrency dùng disposable
MongoDB replica set + real Task command/persistence implementation; mock/unit
checker không chứng minh transaction, HTTP authorization hoặc integration.

## 2. Scenarios — mỗi case có oracle hoặc decision blocker

I = authenticated identity; O/P = eligible Organization/Project memberships;
T = applicable Team authority; R = Task ACL/action authority; D = explicit deny.
“Eligible” không tự tạo fixtures: exact contract D02-04 cần duyệt trước.
Version/state labels chỉ symbolic candidates, không implementation values.
Tất cả rows hiện **UNEXECUTED**; oracle-grade khác test execution status.

| Case | Setup / trigger | Oracle-grade và approved boundary hoặc proposal expectation | Decision blocker cho executable detail | D-01 mapping |
|---|---|---|---|---|
| O01 | Missing/invalid/expired identity gửi transition | APPROVED_BOUNDARY E05/B8: không protected content/mutation | D02-04/10, Q6 transport/error precedence | TV-01, AT-01 |
| O02 | Role hiện hành nhưng O missing/PENDING_INVITE/SUSPENDED/REMOVED | APPROVED_BOUNDARY B8: không context/access; không Task mutation | D02-04/10 exact rejection | TV-02/09, AT-01 |
| O03 | Client thay organizationId/actorId, RoleAssignment hợp lệ Organization khác | APPROVED_BOUNDARY B3/B8: selector/role không cấp membership hoặc impersonation | D02-04/06/10 trusted DTO | TV-03, AT-01 |
| O04 | Task ở Organization/Project khác hoặc Team sibling; IDs không cùng parent | APPROVED_BOUNDARY E05/B8/B10: không suy quyền cross-scope | D02-04/10, Q2 exact Team/parent/disclosure | TV-03/08, AT-01 |
| O05 | I/O ACTIVE nhưng P INACTIVE/missing, stored assignment còn | APPROVED_BOUNDARY B10: không effective Project-scoped Task access | D02-04/10 exact response; không tự clear assignee | TV-09, AT-01 |
| O06 | Role allow nhưng Task ACL deny hoặc explicit D=DENY | APPROVED_BOUNDARY E05/B8: deny precedence, không mutate | D02-04/10 ACL/deny evidence and failure output | TV-03/19, AT-01 |
| O07 | Guard/deny assessment UNKNOWN hoặc không đọc được evidence | APPROVED_BOUNDARY DATN-94/E10: unapproved actor/edge không enable; đề nghị fail closed evidence | D02-04/10 unknown-evidence semantics | TV-15, AT-07 |
| O08 | ADMIN/platform alone hoặc PUBLIC Project metadata caller yêu cầu Task | APPROVED_BOUNDARY B8/B10: không implicit content/mutation grant | D02-04/10 independent evidence và concealment | TV-04, AT-02 |
| O09 | ADMIN đồng thời có independently valid assignee/Leader evidence | BLOCKED_SELECTION: đánh giá independent evidence, không blanket allow/deny từ ADMIN label | D02-04 và enabled edge D02-02 | TV-04/08, AT-02 |
| O10 | Project creator ordinary MEMBER create/edit; thử sửa arbitrary Task/field/state | APPROVED_BOUNDARY B9: giữ member create/edit rights; BLOCKED_SELECTION cho resource/field/transition ceiling | D02-01/02/04, Q1/Q2/Q3/Q6 | TV-05/07/21, AT-02 |
| O11 | Parameterized fresh command cho từng T01–T25; eligible I/O/P/T/R, D clear, token current | BLOCKED_SELECTION: P-M success cho 8 candidate allow; P-X denial cho 17 candidate reject; hiện tất cả UNKNOWN disabled | D02-01/02/03/04/05/10; từng edge phải có accepted decision riêng | TV-12/13, AT-07 |
| O12 | New ID cho same-state T01/07/13/19/25; so với exact ID replay | BLOCKED_SELECTION: new same-state reject/H0; committed replay theo O20, không tạo giả event/version | D02-02/07/10 | TV-12/14, AT-07 |
| O13 | State/command ngoài accepted vocabulary hoặc UNKNOWN edge | APPROVED_BOUNDARY E10 AC: reject/disabled, không mutate; proposal string không được silently coerce | D02-01/02/10 exact validation/error | TV-12, AT-07 |
| O14 | BLOCK/RESUME/CANCEL/REOPEN thiếu/blank reason; START/COMPLETE có reason | BLOCKED_SELECTION: required reason sau trim theo T profiles; optional bình thường | D02-03/10, Q3 bounds/redaction | TV-13, AT-07 |
| O15 | Current assignee vs creator-only vs scoped Leader vs sibling Leader trên cùng edge | BLOCKED_SELECTION: A/L và G áp dụng; creator ID không tự cấp transition | D02-02/04 và Task permission mapping | TV-07/08/13, AT-07 |
| O16 | New command expectedVersion thiếu/malformed/cũ | BLOCKED_SELECTION: validation hoặc stale conflict; không state/version/history delta | D02-05/10 exact distinction | TV-14, AT-07 |
| O17 | Hai different IDs cùng expectedVersion, barrier trước write | BLOCKED_SELECTION: tối đa một mutation commit, một version increment/H+; loser conflict | D02-05/07/10 và DB CAS contract | TV-14/16, AT-03/07 |
| O18 | Field edit/assignment commit cạnh tranh transition cùng version | BLOCKED_SELECTION: aggregate CAS không cho transition dựa trên assignee/state cũ | D02-04/05 và editable/assignment contract Q3/Q5 | TV-07/14/15, AT-07 |
| O19 | Membership/ACL revoke giữa authorization và Task commit | APPROVED_BOUNDARY B8/B10: không dùng mất-quyền làm grant; BLOCKED_SELECTION về serialization/fence | D02-04/05, owning IAM/ACL propagation/fence contract | TV-15, AT-01 |
| O20 | First commit response mất, retry cùng ID/fingerprint | APPROVED_BOUNDARY B6 cho Handover không double-assign; BLOCKED_SELECTION: original safe ack replay, không new H+/version | D02-06/07/10, ordinary transitions idempotency chưa accepted | TV-14/17, AT-04/07 |
| O21 | First commit, Task version/state/assignee sau đó đổi; exact retry còn được authorize | BLOCKED_SELECTION: replay original operation result, không stale-conflict từ current version; current read riêng | D02-07/10 replay representation | TV-14/17, AT-04 |
| O22 | Same ID khác target state/reason/expectedVersion/command trong cùng namespace | BLOCKED_SELECTION: fingerprint mismatch, không overwrite/mutate hoặc lộ cached result | D02-06/07/10 normalization/error | TV-14, AT-04/07 |
| O23 | Retry thay correlation/session; hoặc ID giống nhưng Task/principal namespace khác | BLOCKED_SELECTION: correlation/session không đổi operation; distinct authorized namespace độc lập, cross-scope không leak | D02-04/06/07/10 exact principal and scope | TV-03/14, AT-04 |
| O24 | Same ID/fingerprint đồng thời; một attempt crash/abort/in-flight | BLOCKED_SELECTION: single commit proof, contender bounded resolve/retry-later, không fake success | D02-05/07/10 durability/in-flight contract | TV-14/16, AT-03/04 |
| O25 | Committed retry sau O/P/ACL/action grant bị revoke | APPROVED_BOUNDARY B8/B10: không leak content qua replay; BLOCKED_SELECTION detailed ack denial | D02-04/07/10 current authority/projection | TV-09/14/19, AT-01/04 |
| O26 | Logical window hết nhưng record chưa cleanup; result cleanup rồi còn proof/tombstone | BLOCKED_SELECTION: expired ID không execute như absent; authorized recovery | D02-08/10 exact W, proof retention/error | TV-14/17, AT-04 |
| O27 | Task write xong, history write lỗi; history staged xong, Task/commit lỗi | APPROVED_BOUNDARY B4: cùng rollback, không orphan state/history; success phải cùng commit | D02-05/10 persisted shape/error và accepted implementation | TV-16, AT-03 |
| O28 | Operation result write lỗi hoặc process crash tại commit boundary | BLOCKED_SELECTION: đề nghị atomic Task/history/operation proof, uncertain resolve cùng ID | D02-05/07/10 durable operation design | TV-14/16/17, AT-03/04 |
| O29 | Handover pre-request failure/Task abort/Task commit response lost/local ack lỗi | APPROVED_BOUNDARY B3/B6: API-only/idempotent assignment/retry; BLOCKED_SELECTION reconcile-first từng boundary | D02-01/04/06–10, Q1/Q2/Q6 Handover contract | TV-11/17, AT-04 |
| O30 | Compensation sau Task commit, có intervening assignment hoặc actor mất quyền | BLOCKED_SELECTION: new authorized command + current CAS; conflict → manual recovery, không overwrite/erase event | D02-04/05/09/10 recovery owner/compensation policy | TV-17, AT-04 |
| O31 | Agent gửi proposal chưa permitted human confirmation; đọc context ngoài ACL | APPROVED_BOUNDARY B3/B7: không autonomous mutation/direct DB; no unauthorized context | D02-04/10, Q1 Agent release scope | TV-18, AT-05 |
| O32 | History/replay/outbox projection lộ raw reason/body/prompt; optional async event | APPROVED_BOUNDARY B4/B7: safe provenance, no full prompt/raw context, conditional outbox atomic/relay/dedup; exact fields/retention chưa accepted | D02-10, Q8/Q9 history/compliance/consumer | TV-19/20, AT-05/09 |

O11 expansion: instantiate **một case cho từng T01–T25**; from/to, command,
A/L/X, G, reason, P-M/P-X và H+/H0 lấy nguyên row trong contract. Mapping này
bao gồm cancel T05/10/15, reopen T17 và toàn bộ CANCELLED exits T21–25; không
chỉ test happy path. Mỗi instance vẫn blocked bởi accepted edge/actor/outcome
record tương ứng. Fresh unknown rejection O13 độc lập với hypothetical allow
O11; không dùng empty allow-set để tuyên bố allowed-case coverage đạt AC3.

## 3. Decision register — không đóng Q từ tracking/merge

Tất cả accepted answers dưới hiện **UNKNOWN**; named personal approvers chưa
xác nhận. Required authority roles là routing đề nghị, không gán quyền duyệt
cho Reporter/assignee. Không có Q4/Q5/Q7 hoặc related Q6/Q8 được đóng bởi D02-R1.

| Decision | Owning review surface | D-01 questions | Required authority roles / affected cases |
|---|---|---|---|
| D02-01 | States/initial/completion/terminal, DONE evidence, Handover eligibility; doc16 §2 | Q1/Q3/Q4 | Product + Handover; O10–13/29 |
| D02-02 | T01–25 commands/allow/reject/same-state/cancel/reopen; doc16 §3 | Q4/Q5 | Product + API + Security; O11–15 |
| D02-03 | Required/optional reason và validation; doc16 §3 | Q3/Q4/Q6/Q8 | Product + API + Security; O14/32 |
| D02-04 | G1–6, actor/action/resource/field/Team/target/freshness/fence; doc16 §4 | Q2/Q3/Q5/Q6/Q7 | Product + Security + IAM/Project/Team + API; O01–10/15/18/19/23/25/29–31 |
| D02-05 | Version/CAS/stale/concurrent/uncertain commit; doc17 §2 | Q3/Q7 | API + DB + Security; O16–19/24/27/28/30 |
| D02-06 | Namespace/principal/fingerprint; doc17 §3 | Q6/Q7 | API + Security + Handover; O20–24/29 |
| D02-07 | Replay/mismatch/in-flight/durable result/denial caching; doc17 §4 | Q7, related Q5/Q6/Q8 | API + DB + Security; O12/20–25/28/29 |
| D02-08 | Window/proof retention/expiry/recovery; doc17 §5 | Q7/Q8 | Ops + DB + API + Handover; O26/29 |
| D02-09 | Coordinator/retry/compensation/manual owner; doc17 §6 | Q2/Q4/Q5/Q6/Q7 | Handover + Task Product/API; O29/30 |
| D02-10 | Exact success/denial/retry/error/history/projection/retention; doc17 §7 | Q6/Q8, conditional Q9 | API + Security + History/DB + consumer owner nếu có; O01–08/13/14/16/20–32 |

Reviewer trả lời từng item/edge bằng mẫu:

```text
Decision + edge/guard/outcome IDs; accepted/partial/rejected/deferred:
Exact answer và rationale/tradeoff (nếu khác proposal):
Approver + authority + decision time:
Evidence permalink + owning document/OpenAPI/schema revision/commit:
Scenarios/oracles được chốt; items còn UNKNOWN:
Owning artifacts cần reconcile; dependency merged và implementation gate:
```

## 4. Năm checkpoints, acceptance và Jira tracking

Snapshot E10: DATN-94 và 111–115 đều To Do; không tự đổi Jira.
Đề nghị status dựa trên artifact/checks/review thực tế ở handoff; phần việc
tài liệu sẵn review không đồng nghĩa full ticket hoặc business policy accepted.

| Checkpoint | Artifact cụ thể | Gap còn lại / đề nghị sau checks và review đạt |
|---|---|---|
| [DATN-111](https://trankimthang0207.atlassian.net/browse/DATN-111) | Doc16 §1–2: approved-vs-candidate register, nguồn/authority/initial/terminal | To Do → In Review cho preparation; approved concrete state catalogue còn D02-01 |
| [DATN-112](https://trankimthang0207.atlassian.net/browse/DATN-112) | Doc16 §3: 25 edges đủ command/actor/guard/reason/version/outcomes/history profiles | To Do → In Review cho preparation; accepted matrix còn D02-01–07/10 |
| [DATN-113](https://trankimthang0207.atlassian.net/browse/DATN-113) | Doc16 §4: six guard layers + eight actor rows, B9 rights và deny ceiling | To Do → In Review cho preparation; detailed authority/ACL/fence còn D02-04 |
| [DATN-114](https://trankimthang0207.atlassian.net/browse/DATN-114) | Doc17 §1–7: CAS/key/replay/expiry/concurrency/Handover choices, tradeoffs/questions | To Do → In Review cho preparation; exact decisions còn D02-05–10 |
| [DATN-115](https://trankimthang0207.atlassian.net/browse/DATN-115) | Doc18 §1–2: 32 scenario families, O11 có 25 per-edge obligations, oracle/blocker mapping | To Do → In Review cho scenario/oracle preparation; executable contract tests còn blocked, chưa hoàn thành full test requirement |

| DATN-94 AC / expected result | Evidence preparation | Current acceptance conclusion |
|---|---|---|
| AC1: mọi enabled transition/actor nằm trong D-01-approved contract | Source map + states/25 edges/actors, enable NO | NOT MET cho full approved catalogue; không dùng 0 enabled để claim vacuous completion |
| AC2: invalid/unauthorized reject, unapproved disabled | Unknown enable gate và approved-boundary O01–08/13 | Document constraint recorded; runtime enforcement chưa được chứng minh |
| AC3: tests cover allowed/denied/stale/idempotent | O11–30, exact blocker theo từng scenario | NOT MET: chưa accepted oracle/implementation/executable tests |
| Deterministic contract-backed lifecycle | D02-01–10 concrete choices và closure template | Draft preparation sẵn review; full DATN-94 acceptance chưa đạt |

Parent [DATN-94](https://trankimthang0207.atlassian.net/browse/DATN-94): đề nghị
To Do → In Progress cho phần contract đang chờ sign-off/test gate; không đề nghị
Done/full acceptance. [DATN-100](https://trankimthang0207.atlassian.net/browse/DATN-100)
không được mở chặn hoặc triển khai từ proposal này. DATN-93 Done/PR22 merged
giữ nguyên; business decisions ở register riêng, không reopen D-01 vì Q còn mở.

## 5. Verification boundary và bàn giao

Required document checks: local links/anchors, pinned source revisions, table
widths, full 25-pair coverage, 5 same-state/cancel/reopen coverage, NO enabled
UNKNOWNs, guards/actors, all D02/scenario/checkpoint mappings, baseline B1–B10
unchanged và diff whitespace. Review diff cuối bằng code-review-and-quality;
findings phải severity/file/line/impact/fix, chờ user duyệt trước sửa. Check/review
results và commit/push SHA ghi trong handoff riêng để không tự chứng thực draft.

DB/schema/index/migration/seed/data impact: **không có**. Không provision
continuum_task, chạy database/application tests, đổi API/runtime/FE hoặc source
DATN-87. Sau checks/review đạt: commit/push branch Document; user review artifact
trước PR. Chuẩn bị compare/commit và complete PR title/body; không tự gửi Jira
comment/team message, mở PR, approve hoặc merge. Sau decisions được accepted,
reconcile owning contracts và theo dependency/main/DB–BE–FE gates riêng.
