# DATN-94 — D-02 Task V1 state machine: contract để review

**Revision:** D02-R1, 12/10/2026 (Asia/Saigon). **Owner tổng hợp:** Nguyen Hong Phuc.
**Trạng thái:** PREPARATION / PROPOSED; chưa có approved state/edge catalogue.
**Enabled transitions:** 0. Không dùng bảng candidate làm enum, fixture hay runtime policy.

[DATN-94](https://trankimthang0207.atlassian.net/browse/DATN-94) yêu cầu lifecycle
deterministic theo D-01-approved contract. Artifact này bổ sung D-02 riêng trên
baseline [DATN-93 R5](13-task-v1-contract-readiness.md); không sửa B1–B10,
Q1–Q9 hoặc owning ADR/schema. Phạm vi hiện tại là Document và scenario/oracle
preparation. [Reliability decisions](17-task-v1-command-reliability-review.md)
và [scenario/oracle + acceptance](18-task-v1-state-machine-oracles.md) là hai
phần còn lại của cùng revision; chưa triển khai DATN-100, API, DB, runtime hay FE.

## 1. Evidence, authority và revision

Doc base: `8ab9268523c3fb661008cd0b6715e0e1ca3cd79c` (origin/main).
Các link local dưới đây thuộc base này, trừ ba artifact D02-R1 mới.
APPROVED là constraint có authority; FACT là quan sát; PROPOSED là lựa chọn
để reviewer quyết định; UNKNOWN là thiếu accepted answer. Không tìm thấy
approval trong nguồn đã đọc không chứng minh nguồn khác không tồn tại.

| ID | Nguồn / revision được đọc | Authority và giới hạn |
|---|---|---|
| E01 | [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md), 01/10/2026, Decision 1–5 | Team decision: canonical Task, Jira exclusion, Work Note/SAG/Handover boundary; không chọn states |
| E02 | [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md), 01/10/2026, Decision 1–9 | Thang/team, accepted service/repo/storage/API/atomic history/Agent boundary; không approve port, DTO hoặc matrix |
| E03 | [Use Cases §3/5/7](12-continuum-task-management-use-cases.md), 01/10/2026 | State/actor/field/reason/Handover eligibility candidates vẫn PROPOSED |
| E04 | [Task schema boundary §2–4](../../database-design/12_TASK_MANAGEMENT_SCHEMA.md), 01/10/2026 | Accepted ownership, field/cardinality/index/history details vẫn proposal |
| E05 | [Actors §1–7](../02_ACTORS_ROLES_AND_PERMISSIONS.md) và [Workspace §2–4](../Workspace/00-organization-and-access-contract-readiness.md) | Accepted vocabulary, membership/scope/ACL, explicit deny precedence; Task action codes/matrix còn proposal |
| E06 | [Organization Context](../Governance/01-organization-context.md), [Authorization](../Governance/02-role-permission-authorization.md), [Audit/Outbox](../Governance/03-audit-outbox-contract.md) | Research snapshots; policy amendments được phân biệt khỏi inventory cũ, không thay Task authority |
| E07 | [D-01 readiness](13-task-v1-contract-readiness.md), [worksheet](14-task-v1-review-worksheet.md), [validation](15-task-v1-review-validation.md), merged R5 | B1–B10 reused; Q4/Q5/Q7 và relevant Q6/Q8 vẫn UNKNOWN. Tiêu đề “Accepted transition matrix” trong worksheet cũ không approve 25 UNKNOWN cells; D-02 dùng nhãn review trung tính |
| E08 | [Jira DATN-93](https://trankimthang0207.atlassian.net/browse/DATN-93), [PR #22](https://github.com/DATN-SPRING2027/Document/pull/22), đọc 12/10/2026 | Parent và 105–110 Done; KeyT9999 merged 5 commits thành doc base. Completion của precise blocker list; không phải lifecycle sign-off |
| E09 | [R5 review](https://github.com/DATN-SPRING2027/Document/pull/22#issuecomment-6117498589), head `11ff188ddc5b702daffd1ba22b1fd01dd121fa94` | Technical comment chấp nhận blocker-list direction, còn P2 nhãn matrix; không product approval, không tự sửa finding cũ |
| E10 | [DATN-94](https://trankimthang0207.atlassian.net/browse/DATN-94) và từng 111–115, đọc 12/10/2026 | Parent To Do/Phúc; children To Do/Unassigned, description/comments trống; không approval mới. Dependency 93 Done → 94 → 100 To Do; không link 87 hiển thị |
| E11 | [BE main](https://github.com/DATN-SPRING2027/DATN-BE/tree/e80617cde67fed146bab3ee874e68040ecf2caf3), live remote SHA khớp local origin/main | Không Task service/controller/OpenAPI/tests. Lifecycle/Handover application services chỉ health; IAM/Project tests không chứng minh Task lifecycle |
| E12 | [Creator MEMBER decision](https://github.com/DATN-SPRING2027/DATN-BE/blob/e80617cde67fed146bab3ee874e68040ecf2caf3/docs/decisions/project-creator-member-bootstrap-v1.md), reaffirmed 04/10; [Project Access](https://github.com/DATN-SPRING2027/DATN-BE/blob/e80617cde67fed146bab3ee874e68040ecf2caf3/docs/decisions/project-access-visibility-v1.md), 02/10 | Requester-approved creator member rights và ACTIVE ProjectMembership; PUBLIC/ADMIN metadata không cấp Task content ACL |
| E13 | [FE main BFF](https://github.com/DATN-SPRING2027/DATN-FE/blob/f6380a4bdd01f5547a6c6d07d975d3da7e6d5aff/src/lib/bff-proxy.ts), remote main đọc 12/10 | Existing BFF boundary; inventory chỉ có Task icons, không Task feature contract. Checkout FE cũ được giữ nguyên |

**Reconciliation:** E08/E09 không đóng Q4/Q5/Q7; E11 không cung cấp accepted
Task implementation hoặc API contract. D1–D6 Organization và K1–K6 DATN-87
không quyết định Task policy, TTL, errors hoặc replay. B8–B10 vẫn áp dụng;
không yêu cầu duyệt lại baseline chỉ vì Task runtime chưa có. Guide BE/AGENTDB
còn mô tả monolith trong khi E02 chọn Task service riêng; reconciliation thuộc
application/runtime lane, không sửa guide trong task này.

## 2. DATN-111 — approved states và candidates

[DATN-111](https://trankimthang0207.atlassian.net/browse/DATN-111).
**Approved concrete states: chưa có bằng chứng. Approved initial state: UNKNOWN.
Approved terminal semantics: UNKNOWN.** Approved constraints B4/B5/B7 vẫn có
hiệu lực: history nguyên tử, knowledge verification tách biệt, Agent không tự ghi.

| Candidate | Nguồn | Ý nghĩa / initial / terminal đề nghị | Accepted answer / authority |
|---|---|---|---|
| TODO | E03 §3/7; E04 §3 | Chưa bắt đầu; initial duy nhất khi create; chưa kết thúc | UNKNOWN, D02-01; named Product approver chưa xác nhận |
| IN_PROGRESS | E03 §3/7; E04 §3 | Đang thực hiện; không initial/terminal | UNKNOWN, D02-01 |
| BLOCKED | E03 §3/7; E04 §3 | Đang vướng; không terminal; cần reason khi vào/ra theo đề nghị D02-03 | UNKNOWN, D02-01/03 |
| DONE | E03 §3/7; E04 §3 | Hoàn thành, có ngoại lệ reopen → IN_PROGRESS; không terminal bất khả đảo theo đề nghị | UNKNOWN, D02-01/02 |
| CANCELLED | E03 §3/7; E04 §3 | Kết thúc do hủy, không reopen trong V1 theo đề nghị | UNKNOWN, D02-01/02 |

**D02-01 — đề nghị:** giữ 5 candidates, initial TODO; completion khác verified
knowledge. BLOCKED biểu đạt trở ngại, không phải permission state. DONE không
đòi Work Note/evidence; Handover assignment đề nghị chỉ chọn TODO/IN_PROGRESS/
BLOCKED. Tất cả chi tiết này cần sign-off, kể cả hai rule từ E03 §7.
Alternative: chỉ TODO/IN_PROGRESS/DONE, lý do vướng ở metadata. Cách này giảm
matrix nhưng làm filter việc bị chặn khó hơn; ảnh hưởng Q3 enum, Q4 edges,
Handover eligibility và UI sau này. Không thêm REOPENED hoặc workflow editor.

**Câu hỏi gửi Product reviewer:** “Duyệt từng state và ý nghĩa trong bảng,
initial TODO, DONE có reopen, CANCELLED không reopen; DONE không có Work Note
guard và Handover chỉ nhận ba state mở hay chọn subset nào? Ghi rõ ngoại lệ,
authority và owning revision; chưa chọn thì item vẫn UNKNOWN.”

## 3. DATN-112 — transition register gồm cả cancel, reopen và same-state

[DATN-112](https://trankimthang0207.atlassian.net/browse/DATN-112).
25 rows dưới bao phủ Cartesian product của 5 candidates, **không có enabled edge**.
Command labels là business labels để review, không route/DTO/permission code.
G là tất cả applicable guards G1–G6 ở §4; A là eligible current assignee hoặc
explicit scoped Leader theo proposal; L là explicit scoped Leader theo proposal.
X nghĩa đề nghị reject với mọi actor, kể cả A/L; lý do không thể override X.
P-M/P-X là đầy đủ version, success/denial/retry/history profile dưới bảng.
Mọi accepted cell vẫn UNKNOWN Q4/Q5/Q7; error/event representation thêm Q6/Q8.

| Edge | From | To | Đề nghị / command | Actor + guards | Reason proposal | Version + outcomes | History | Accepted | Enabled |
|---|---|---|---|---|---|---|---|---|---|
| T01 | TODO | TODO | Reject / same-state | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T02 | TODO | IN_PROGRESS | Allow / START | A + G | Optional | P-M | H+ | UNKNOWN | NO |
| T03 | TODO | BLOCKED | Reject / direct-block | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T04 | TODO | DONE | Reject / direct-complete | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T05 | TODO | CANCELLED | Allow / CANCEL | L + G | Required | P-M | H+ | UNKNOWN | NO |
| T06 | IN_PROGRESS | TODO | Reject / reset | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T07 | IN_PROGRESS | IN_PROGRESS | Reject / same-state | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T08 | IN_PROGRESS | BLOCKED | Allow / BLOCK | A + G | Required | P-M | H+ | UNKNOWN | NO |
| T09 | IN_PROGRESS | DONE | Allow / COMPLETE | A + G | Optional | P-M | H+ | UNKNOWN | NO |
| T10 | IN_PROGRESS | CANCELLED | Allow / CANCEL | L + G | Required | P-M | H+ | UNKNOWN | NO |
| T11 | BLOCKED | TODO | Reject / reset | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T12 | BLOCKED | IN_PROGRESS | Allow / RESUME | A + G | Required | P-M | H+ | UNKNOWN | NO |
| T13 | BLOCKED | BLOCKED | Reject / same-state | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T14 | BLOCKED | DONE | Reject / direct-complete | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T15 | BLOCKED | CANCELLED | Allow / CANCEL | L + G | Required | P-M | H+ | UNKNOWN | NO |
| T16 | DONE | TODO | Reject / reset-completion | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T17 | DONE | IN_PROGRESS | Allow / REOPEN | A + G | Required | P-M | H+ | UNKNOWN | NO |
| T18 | DONE | BLOCKED | Reject / direct-reopen-block | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T19 | DONE | DONE | Reject / same-state | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T20 | DONE | CANCELLED | Reject / cancel-completed | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T21 | CANCELLED | TODO | Reject / restore | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T22 | CANCELLED | IN_PROGRESS | Reject / reopen-cancelled | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T23 | CANCELLED | BLOCKED | Reject / restore-blocked | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T24 | CANCELLED | DONE | Reject / complete-cancelled | X + G | N/A | P-X | H0 | UNKNOWN | NO |
| T25 | CANCELLED | CANCELLED | Reject / same-state | X + G | N/A | P-X | H0 | UNKNOWN | NO |

**Profiles (PROPOSED D02-02/04/05–10):**

- P-M: mới + authorized + approved edge + reason valid + expected version
  match → canonical target, version tăng một lần, H+. Stale → conflict,
  denial/validation/history failure → không commit mutation. Retry uncertain
  result với cùng operation-ID/payload; exact committed replay trả result cũ
  sau current authorization, không tăng version/history. Payload mismatch,
  in-flight duplicate, expiry → [reliability tables](17-task-v1-command-reliability-review.md).
- P-X: command mới → transition denial, không đổi state/version, H0. Retry
  không biến denial thành allow; read/refetch rồi chỉ gửi command mới khi có
  edge được duyệt. Committed replay của một command đã thành công trước đó
  đi qua replay resolution, không bị phân loại thành same-state command mới.
- H+: một domain history record cho mỗi mutation commit; B4 đã APPROVED
  atomicity. Exact event names/fields/projection Q8 còn UNKNOWN D02-10.
  H0: đề nghị không thêm mutation history cho rejection/no-op/replay; security
  denial audit riêng cần Q8, không được suy ra rằng mọi audit đều bị bỏ.

**D02-02 — lý do lựa chọn:** 8 candidate allow edges, 17 candidate rejection
edges. Buộc START trước BLOCK/COMPLETE và RESUME trước COMPLETE giúp đọc
history rõ; đổi lại thêm thao tác cho việc hoàn tất ngay hoặc bị chặn từ đầu.
Alternative: cho T03/T04/T14 trực tiếp nếu team cần; phải ghi riêng actor,
reason và history. Reject same-state mới giúp tránh version/event giả; alternative
no-op success không event/version cũng hợp lý nhưng cần contract riêng.
Cancel chỉ state mở, reopen chỉ DONE → IN_PROGRESS để tránh ghi lại completion
thành cancellation; giữ CANCELLED kết thúc làm rollback nghiệp vụ khó hơn.

**D02-03 — reason:** đề nghị reason required cho BLOCK/RESUME/CANCEL/REOPEN,
optional START/COMPLETE; trim rồi từ chối rỗng cho required. Exact length,
encoding/redaction và history visibility cần Q3/Q6/Q8; không tự đặt limit.

**Câu hỏi gửi Product/API reviewer:** “Duyệt hoặc thay lựa chọn từng T01–T25,
A/L và reason rules; new same-state reject hay no-op? Cho direct block/complete,
cancel DONE hoặc restore CANCELLED không? Cùng-ID replay là retry operation,
không phải new same-state. Ghi success/denial/history cho từng ngoại lệ.”

## 4. DATN-113 — guards và actor/action matrix

[DATN-113](https://trankimthang0207.atlassian.net/browse/DATN-113).
Không dùng role name, stored creator/assignee hay Project visibility làm grant.
Identity và ACTIVE membership là prerequisites; chúng không thay Task action
authority. “UNKNOWN không enable” áp dụng cả guard/authority bị thiếu evidence.

| Guard | Layer riêng | Accepted constraint | Chi tiết còn cần D02-04 / Q2/Q5/Q6/Q7 |
|---|---|---|---|
| G1 | Identity | Authenticated identity từ trusted service/API, B3/B7/B8 | Exact delegated human/service transport, active-subject predicate, không tin client actor ID |
| G2 | OrganizationMembership | Caller có ACTIVE membership đúng Organization; RoleAssignment không thay evidence, B8 | Current authorization tại replay/write, cache/freshness/failure contract |
| G3 | Project scope | Actual parent Organization/Project match; ACTIVE ProjectMembership ở Project scope, B10 | Parent archive/read/write policy; selector không tạo quyền |
| G4 | Team scope | Chỉ assigned Project/Team authority; không sibling-Team/all-Project implication, E05 | TeamMembership eligibility, teamless Task và Project Leader child delegation; Team contract vẫn mở |
| G5 | Task resource ACL | ACL độc lập với role và PUBLIC metadata, B8/B10 | Exact read/update/transition/history permission, creator/assignee ceiling, target successor eligibility |
| G6 | Explicit deny/lifecycle | Applicable deny overrides allow; Agent không tự mutate, E05/B7 | Deny evidence source và revoke/write fence; unknown evidence không authorize |

**PROPOSED D02-04 matrix:** mỗi positive cell còn UNKNOWN ở mức Task command.
G áp dụng mọi caller; unauthorized được reject theo DATN-94 AC. B9 creator
MEMBER create/edit rights đã chốt và được giữ; bảng chỉ hỏi resource/field/scope
limits, không đặt thêm blanket role gate hoặc hạ creator rights thành không tồn tại.

| Actor evidence | Create / edit fields | Ordinary transition / reopen | Cancel / assign | Read/history | Scope/deny ceiling |
|---|---|---|---|---|---|
| Creator ordinary MEMBER | B9 member rights; đề nghị editable allowlist trên own/currently assigned Task | Creator riêng không cấp A; đề nghị chỉ current assignee hoặc scoped Leader | Đề nghị không cancel/gán người khác; self-assign/create cần sign-off | Đề nghị Task-readable ACL; history projection riêng | G, field/resource/Team limits UNKNOWN |
| Current assignee MEMBER | Đề nghị allowlist; không sửa mọi field | Đề nghị A cho T02/08/09/12/17 | Không tự reassign/cancel theo proposal | Current ACL cần thiết; assignee ID không thay membership | G; lost membership/assignment không grant |
| Project-scoped TEAM_LEADER | Đề nghị trong explicit assigned scope | Đề nghị A; Team ceiling cần explicit delegation | Đề nghị L cancel/assign eligible target | ACL vẫn bắt buộc | G; không tự suy toàn child Team content |
| Team-scoped TEAM_LEADER | Đề nghị đúng Team đã giao | Đề nghị A đúng Team | Đề nghị L đúng Team/eligible target | ACL đúng Task | G; sibling Team/cross Project không cấp quyền |
| SUCCESSOR assignment | Không create/edit chỉ từ assignment; dùng eligible assignee rule nếu được duyệt | Không cấp A chỉ từ Handover package | Không tự cancel/reassign | Chỉ handed-over resources và ACL, không kế thừa quyền predecessor | G, assignment validity và lifetime cần chốt |
| Organization ADMIN | Không grant Task từ ADMIN alone | Không grant A từ ADMIN alone | Không grant L từ ADMIN alone | Metadata access không cấp content | Nếu có independent valid Member/Leader evidence thì đánh giá evidence đó |
| PLATFORM_OPERATOR | Platform operations không cấp Task mutation | Không grant A từ platform alone | Không grant L từ platform alone | Không default Task content | Cần independent authorized Organization/Project evidence |
| Agent / Handover service | Authenticated contract, không direct DB | Agent proposal cần permitted human confirmation; Handover không tự đổi status | B6 assignment qua Task API; delegated actor/target policy UNKNOWN | Context chỉ current authorized projection | Service identity không thay human scope/ACL; B3/B6/B7 |

**Đề nghị D02-04:** creator/assignee chỉ editable allowlist; state/cancel/assignment
dùng command authority riêng. Team Leader không rộng hơn assignment; teamless
Task chỉ explicit Project authority. Recheck authorization trước write/replay;
fence được owner chọn phải chứng minh revoke racing write không lọt stale grant.
Alternative: creator cũng transition; tăng tiện lợi nhưng thay A policy, cần
ghi rõ. Không tự chọn cơ chế epoch/session của DATN-87 cho Task.

**Câu hỏi gửi Product/Security reviewer:** “Duyệt exact actor × command ×
resource/field × Project/Team matrix, permission mapping và Team delegation;
creator B9 giữ quyền tạo/sửa ở resource/field nào? Creator không là assignee
có transition không? Chốt teamless, successor eligibility/lifetime, current
authorization/revocation fence và deny evidence; ADMIN/PUBLIC/platform không
implicit Task content grant. Cung cấp named authority và owning revision.”

## 5. Gate trước sử dụng contract

State, edge, actor hoặc outcome chỉ được enable sau decision record có accepted
answer cụ thể, approver/authority, thời điểm, source revision và scenario mapping.
“Approve draft” chỉ có hiệu lực với items được nêu rõ; partial approval giữ
phần còn lại UNKNOWN. Owning D-01/Use Cases/Actors/schema/OpenAPI phải được
reconcile và merge đúng workflow trước implementation phụ thuộc; không dùng
merge D02-R1 để mở DATN-100. [Closure register](18-task-v1-state-machine-oracles.md)
theo dõi riêng product decisions và tiến độ tài liệu.
