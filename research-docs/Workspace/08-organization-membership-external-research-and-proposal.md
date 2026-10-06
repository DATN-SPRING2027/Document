# DATN-86 — External membership research and leader proposal

## Trạng thái và cách sử dụng

- Revision **R5, 2026-10-06 (Asia/Saigon)**; người chuẩn bị: Nguyen Hong Phuc.
  Research R4 đọc nguồn ngoài ngày 2026-10-05; R5 sửa bốn finding đã được người
  dùng duyệt sửa, không phải approval cho các đề nghị nghiệp vụ.
- Jira: [DATN-86](https://trankimthang0207.atlassian.net/browse/DATN-86);
  artifact review: [Document PR #23](https://github.com/DATN-SPRING2027/Document/pull/23).
- **[PROPOSED — CHƯA PHÊ DUYỆT]**: tài liệu đưa ra khuyến nghị để leader và
  các authority review. Không cập nhật approved baseline, permission, transition
  hay schema. Accepted policy của các lựa chọn mới vẫn **UNKNOWN**; expected
  reviewed contract của DATN-86 vẫn **NOT MET**.
- Reuse [working contract 06](06-organization-membership-contract.md) cho B1–B7,
  E1–E14, Q1–Q8 và AT-01–09; [worksheet 07](07-organization-membership-review-worksheet.md)
  cho alternatives, API examples, RV-01–08 và decision record. Tài liệu này
  bổ sung căn cứ bên ngoài và ưu tiên đề nghị, không thay thế hai tài liệu đó.
- Phạm vi research: tài liệu công khai chính thức của GitHub, GitLab, Auth0,
  Clerk, OWASP và RFC; đọc ngày 2026-10-05. Chưa chạy demo, benchmark hay thử mutation
  trên hệ thống nhà cung cấp. Đây là mẫu so sánh có chủ đích, không chứng minh
  một chuẩn chung của mọi hệ thống hoặc topology/persistence nội bộ của họ.

## 1. Vấn đề được lưu lại

Đọc lại Jira và PR #23 ngày 2026-10-05: parent In Review trước lượt research;
DATN-229/230 In Review, DATN-231–234 In Progress, cả sáu children Unassigned.
Descriptions đã có R2/R3; không có approval mới trong Comments được hiển thị,
PR chưa có review/comment. Parent chuyển In Progress trong lúc chuẩn bị R4.
86 blocks 87, 87 blocks 88; downstream To Do; 274 Done chỉ cung cấp context evidence.

Fetch BE thấy `7f5737399a4e997f3229e858219eb08daddf994a` chỉ thêm A-04 decision
docs; membership resolver/schema/refresh/OpenAPI không đổi so với R3. E12 trong
06 là [bounded A-04 approval record](https://github.com/DATN-SPRING2027/DATN-BE/blob/7f5737399a4e997f3229e858219eb08daddf994a/docs/decisions/dec-access-09-platform-operator-authorization.md):
PLATFORM_OPERATOR được first-ADMIN bootstrap trong organization.create, không có
ongoing membership/role management hoặc Organization-content access từ platform
authority. Record ghi Leader approval, không cung cấp tên; overall matrix PARTIAL.
Không biến sub-scope này thành approval cho C-01, revoke policy của membership
hay audit collection/event/transaction specifics.

R5 re-read Jira ngày 2026-10-06: status/descriptions/dependencies như R4;
parent chuyển In Progress để sửa. PR có một comment với ba P2 và một P3, chưa
có formal review hay decision sign-off. E13/E14 xác minh account-source gap và
Project-create baseline tại cùng BE SHA. Các corrections dưới đây vẫn đề nghị
xin quyết định; không nghiệm thu bốn subtasks hoặc reviewed-contract result.

| Subtask | Phần thiếu để chốt contract | Nơi theo dõi |
|---|---|---|
| [DATN-231](https://trankimthang0207.atlassian.net/browse/DATN-231) | Identity được mời; actor/proof nhận lời; expiry/replay/resend/cancel/delivery và kết quả bốn trạng thái | 06 Q1/Q2/Q3/Q5–Q7; 07 §1; RP-01/02 dưới đây |
| [DATN-232](https://trankimthang0207.atlassian.net/browse/DATN-232) | Commands/transitions, safeguards, suspend/remove/resume/rejoin và effects/recovery ở domain con | 06 Q1/Q3/Q6/Q8; 07 §2; RP-03/04 |
| [DATN-233](https://trankimthang0207.atlassian.net/browse/DATN-233) | Exact API/DTO/visibility/validation/errors/retries/concurrency và canonical audit scope/details | 06 Q1–Q7; 07 §3/4; RP-05/06 |
| [DATN-234](https://trankimthang0207.atlassian.net/browse/DATN-234) | Accepted rule table và exact review oracles; mapping tới verification của implementation | 06 §8/AT-01–09; 07 §5/RV-01–08; §5 dưới đây |

**Thiếu quyết định không phải Jira/rules cấm In Review.** Team có thể dùng
In Review để review/chốt chính proposal, nếu ghi rõ pending decisions. Status
không tự tạo product approval. Không đưa subtask Done chỉ vì đã viết tài liệu
hoặc technical review không có findings. Người quyết định policy chưa được
xác nhận; leader cần chỉ định authority, không mặc định assignee là approver.

## 2. So sánh các hệ thống bên ngoài — chỉ là external facts

| Hệ thống / nguồn chính thức | Hành vi được tài liệu mô tả | Điều đáng tham khảo cho DATN / giới hạn |
|---|---|---|
| GitHub: [inviting users](https://docs.github.com/en/organizations/managing-membership-in-your-organization/inviting-users-to-join-your-organization) | Owner mời bằng username/email; người nhận phải chấp nhận trước khi trở thành member. Email cần khớp verified email của tài khoản. Invite hết hạn sau 7 ngày; có retry/cancel. Không áp dụng cho Enterprise Managed Users. | Tách lời mời khỏi quyền truy cập; 7 ngày là một ví dụ cụ thể, không phải thời hạn DATN đã duyệt. |
| GitHub: [reinstating a former member](https://docs.github.com/en/organizations/managing-membership-in-your-organization/reinstating-a-former-member-of-your-organization) | Owner có thể mời lại, chọn khôi phục quyền cũ hoặc bắt đầu với quyền mới; dữ liệu quyền/settings được giữ 3 tháng. | Rejoin và restoration là quyết định riêng. Không copy retention 3 tháng hoặc mặc định restore. |
| GitLab: [groups — remove a member](https://docs.gitlab.com/user/group/#remove-a-member-from-the-group) | Owner remove direct member; inherited member phải remove ở parent. Dialog có lựa chọn remove direct memberships ở subgroups/projects và unassign issues/merge requests. | Access, stored relationships và assigned responsibilities cần effects rõ ràng; hierarchy/inheritance GitLab khác DATN. Không tự copy cascade. |
| GitLab: [moderate users](https://docs.gitlab.com/user/group/moderate_users/#ban-and-unban-users) và [change group Owner](https://docs.gitlab.com/user/group/manage/#change-the-owner-of-a-group) | Group ban/unban của GitLab.com Ultimate chặn access group/repositories; ban Owner cần demote trước. Group phải giữ ít nhất một human Owner. | Tham khảo scoped suspension và safeguards. Ban không đồng nhất với DATN SUSPENDED; vendor roles/tier không phải permission DATN. |
| Auth0: [invite Organization members](https://auth0.com/docs/manage-users/organizations/configure-organizations/invite-members) | Email invite hỗ trợ user có/chưa có account. Người nhận login/signup bằng email được mời; ứng dụng cần acceptance route chuyển invitation + organization vào authorization flow. Organization roles tách khỏi global RBAC. | Cần giải quyết identity/onboarding trước khi cấp Organization Context. Availability phụ thuộc plan/login implementation; không nhập email-verification policy của Auth0. |
| Clerk: [Organization invitations](https://clerk.com/docs/guides/organizations/add-members/invitations) | Invite link đi qua sign-in flow; admin được phép mời theo mặc định. Có thể revoke link. Clerk cũng cho thêm trực tiếp user có account bằng createOrganizationMembership khi bỏ invitation flow. | Recipient acceptance và admin direct-add đều là pattern tồn tại; direct-add không chứng minh consent policy DATN. Không copy role names/default grants. |
| GitHub: [REST Organization members](https://docs.github.com/en/rest/orgs/members#create-an-organization-invitation) | Create invite nhận user ID hoặc email, yêu cầu Owner và token permission phù hợp; creation/cancellation có endpoint riêng. | Tham khảo command boundary và server authorization, không copy DTO, HTTP errors, roles hay vendor state enum. |

**[INFERENCE]** Những ví dụ này gợi ý ba điểm để review: xác nhận identity trước
khi gia nhập; tách lifecycle khỏi việc cấp/khôi phục quyền; quy định offboarding
theo từng effect. Chúng không quyết định mô hình DATN. Public docs cũng không
chứng minh atomicity giữa IAM mutation và audit trong kiến trúc DATN.

## 3. Gói khuyến nghị DATN — tất cả RP là PROPOSED

Baseline giữ nguyên đúng **PENDING_INVITE, ACTIVE, SUSPENDED, REMOVED**. Chỉ ACTIVE
thiết lập Organization Context; RoleAssignment riêng lẻ không chứng minh membership.
MVP hiện tập trung một Project/nhiều Teams; full self-service Organization admin
và multi-Organization switching chưa được mặc định trong scope. Đề nghị dưới đây
chỉ nhắm membership của Organization đã được provision theo authority hiện hành.

### RP-01 — Mời user đã tồn tại, người nhận tự chấp nhận

**Đề nghị có điều kiện INV-A + ACT-A**: chỉ dùng existing-user-only cho MVP khi
Product + IAM/auth + Security xác nhận nguồn tài khoản/provisioning workflow đã
duyệt, owner, eligibility và cách ADMIN tìm/chọn đúng User. E13 có GET User list,
GET/PATCH detail nhưng không có create-User API; directory chỉ gồm ACTIVE member
của caller Organization, chưa giải quyết người được mời ngoài/chưa thuộc org.
IAM cần xác minh provisioning ngoài OpenAPI và contract chọn recipient với scope/
PII an toàn, không mở global directory. Nếu chưa có, ghi dependent work package
cần được giao/chốt trước invite implementation; không coi dev seed hoặc tạo DB
thủ công là product flow hoàn chỉnh. Workflow/owner/selection specifics và mã
task phụ thuộc chưa được xác nhận, vẫn UNKNOWN.

Sau khi các prerequisite đó được duyệt, đề nghị ADMIN có ACTIVE membership và
authority phù hợp trong chính Organization mời bằng userId đã tồn tại.
Tạo PENDING_INVITE; chưa cấp context
hoặc tự gán role/grant. Recipient xác thực đúng identity, account đủ eligibility,
invitation đúng User/Organization, còn hạn/chưa dùng rồi explicit accept mới ACTIVE.

**Hệ quả baseline E14 cần leader hiểu khi chốt D1:** sau future accepted activation,
authenticated active User với ACTIVE membership và trusted matching context có
thể pass Project-create authorization dù roles=[] và không có project.create
grant. Input hợp lệ, unique code và applicable deny vẫn áp dụng; tạo thành công
còn cần current MEMBER Role có project.read để bootstrap creator, thiếu/sai cấu
hình thì transaction rollback. Đề nghị giữ baseline Project; nếu muốn hạn chế
Project create phải chốt decision Project riêng. Accept không tự gán Organization
role, nhưng không có nghĩa User chưa thể tạo Project. RV-02 ghi case tương ứng;
đây chưa là bằng chứng C-01 accept được implement hoặc test runtime.

Căn cứ: E6 hiện yêu cầu userId/organizationId, còn các ví dụ GitHub/Auth0/Clerk
cho thấy recipient flow có thể tách khỏi ordinary Organization access. Đây là
khuyến nghị cho DATN, không suy ra từ schema rằng invite-only hay accept đã được duyệt.

**Dependency bắt buộc:** E5 không cho user có zero ACTIVE membership vào ordinary
Organization login. Cần IAM/auth + Security duyệt contract xác thực identity/
redemption giới hạn cho recipient, dùng được khi chưa có ACTIVE context, kể cả
user đang ở Organization khác. Chỉ cho xử lý lời mời của đúng identity, không
cho đọc resource của Organization trước activation. Sau atomic commit mới resolve
context bằng rule hiện hành; không tự chọn foreign context hay phát context trước commit.
Credential/session/route mechanism cụ thể vẫn UNKNOWN; không viết code bypass.

Đề nghị defer INV-B/email cho người chưa có account, auto-join theo domain, SCIM
và bulk invite. Platform bypass cho ongoing administration không được E12 cho
phép; first-ADMIN provisioning là workflow riêng. Đánh đổi: giảm scope onboarding, nhưng vẫn phải
làm recipient authentication contract. Nếu leader cần ADMIN activation (ACT-B)
thay vì ACT-A, phải duyệt proof/consent/actor riêng; không tự chọn fallback để
né dependency. Không bổ sung ACT-B vào cùng MVP như một cửa kích hoạt thứ hai.

### RP-02 — Credential có hạn và delivery tách khỏi activation

Đề nghị credential gắn đúng invitation/User/Organization, single-use, TTL **7 ngày**;
resend làm credential trước mất hiệu lực, cancel chấm dứt quyền accept. 7 ngày
là lựa chọn DATN đề nghị từ ví dụ GitHub ở §2, cần Product/Security chốt. Đề nghị
expiry chỉ làm credential không sử dụng được: membership giữ PENDING_INVITE cho
đến resend/cancel; không thêm stored state EXPIRED/CANCELLED và không tự auto-activate.

Đề nghị DEL-A: commit pending membership cùng required audit trước; lỗi gửi mail
không đổi ACTIVE hoặc rollback business state đã commit. Cho retry delivery có
giới hạn và hiển thị delivery outcome riêng. Đây không phải eventual-audit option;
delivery mechanism, retry limits và transaction boundary vẫn UNKNOWN.

Áp dụng candidate kiểm soát token ngẫu nhiên đủ mạnh, lưu an toàn, single-use/
expiry và rate limiting. Đây là **analogy**, vì [OWASP Forgot Password guidance](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)
mô tả reset token, không phải DATN invitation spec. Resend invalidation là khuyến
nghị riêng ở đây. Hash/storage/collection/token format, audit identifiers và
retention chưa được chọn. Không đưa raw credential vào summary, logs hay audit.

### RP-03 — Lifecycle commands có preconditions, không generic status update

**Bảng dưới là proposed grid; accepted grid trong 06 vẫn 16 UNKNOWN.** E = đề
nghị enabled bằng command đã nêu; X = đề nghị excluded. Giữ PENDING khi delivery
fail/expiry không phải một mutation mới. Không suy ra allow/deny runtime từ bảng này.

| From / to [PROPOSED] | PENDING_INVITE | ACTIVE | SUSPENDED | REMOVED |
|---|---|---|---|---|
| PENDING_INVITE | E: resend credential; vẫn pending | E: recipient accept | X | E: ADMIN cancel |
| ACTIVE | X | X: new lifecycle write | E: ADMIN suspend | E: ADMIN remove |
| SUSPENDED | X | E: ADMIN resume sau revalidation | X: new lifecycle write | E: ADMIN remove |
| REMOVED | E: ADMIN reinvite, quyền phải review lại | X | X | X: new lifecycle write |

Ordinary first creation chưa có row → PENDING_INVITE chỉ qua invite theo proposal;
first-ADMIN bootstrap của E12 ngoài bảng C-01 này. ADMIN commands cần
own ACTIVE/trusted context, approved per-action permission và target cùng scope;
accept là recipient exception theo RP-01. Đề nghị target account đủ eligibility
khi accept/resume; resume/rejoin không tự khôi phục role/grant/child access.
ACTIVE với roles=[] vẫn là context hợp lệ theo baseline, không cấp mọi operation.

Đề nghị reason bắt buộc cho suspend/remove; không cho self suspend/remove.
Ở luồng bình thường, đề nghị bảo vệ peer ADMIN bằng workflow handover/demotion
và không để mất eligible ADMIN cuối cùng. Product/Security cần chốt cách áp dụng
các safeguards cho luồng khẩn cấp RP-04 riêng; không lấy handover trước làm gate
chặn emergency suspension, cũng không tự duyệt ngoại lệ peer/last ADMIN.
Cách đếm eligibility, bootstrap/recovery,
permission codes, race protection và error cụ thể phải IAM/Security chốt; không
copy global User LAST_ACTIVE_ADMIN. Role change/handover không nằm trong commands này.

New command ở same-state hoặc invite một pair đang ACTIVE/SUSPENDED đề nghị
conflict; resend chỉ ở PENDING, reinvite chỉ ở REMOVED. Exact replay cùng request
identity/payload có thể trả kết quả đã commit một lần, không mutation/audit lần
hai; phải chốt quyền đọc/replay, expiry và stale-result behavior trong RP-05/06.
Client không được tùy ý gửi status đích. Thêm resume/reinvite/cancel/resend vào
scope cần leader duyệt, không mặc định là required MVP vì chúng có trong proposal.

### RP-04 — Thu hồi access trong Organization, giữ dữ liệu và chốt handover

Đề nghị suspend/remove không đổi global User status hoặc membership Organization
khác. Chặn effective access ở Organization mục tiêu; retain membership/history
và child records cho đối soát, không hard-delete/cascade/unassign tự động. Khi
resume/rejoin, quyền cũ chỉ có hiệu lực nếu được revalidate rõ ràng; giữ row không
đồng nghĩa cấp lại quyền. Cơ chế ngăn stale grants tái hiệu lực cần DB/IAM contract;
nếu chưa bảo đảm được thì resume/rejoin chưa được triển khai.

**Hai trường hợp PROPOSED để Product/Security review:**

- Bình thường: responsibility bắt buộc bàn giao phải hoàn tất approved handover
  trước **remove**; owning domain xác định prerequisite và failure/recovery.
- Khẩn cấp: suspend/chặn access trong Organization mục tiêu trước, người được
  ủy quyền xử lý handover sau; chỉ remove tiếp nếu điều kiện đã được duyệt cho phép.
  Không dùng handover-before-remove để trì hoãn emergency suspension.

Exact actor/delegation, điều kiện khẩn cấp, self/peer/last-ADMIN safeguards,
audit/recovery, thứ tự handover/remove và revocation SLA vẫn UNKNOWN, cần record
Product + Security/IAM và domain owners trước enablement. Đây không tự cấp quyền
ADMIN đọc nội dung hoặc exception cho PLATFORM_OPERATOR: E12 không cho ongoing
membership management qua platform authority. Nếu còn thiếu authority/recovery
cho last ADMIN, phần emergency tương ứng vẫn blocked, không tự bỏ safeguard.
DATN-93 draft chưa thể làm authority cho Task effects.

Mục tiêu đề nghị: request Organization được authorize sau committed mutation
không dùng membership cũ để tiếp tục; refresh không cấp lại context đã mất.
E10 đã recheck selected ACTIVE context trước refresh rotation, nhưng chưa chứng
minh lifecycle mutation, mọi resource route, cache, in-flight work hoặc race fence.
SLA propagation, cancellation và cross-domain enforcement vẫn cần Security/IAM
và domain owners chốt; không hứa global immediate revocation từ source hiện có.

### RP-05 — Command API, least data và retry/concurrency rõ ràng

Đề nghị dùng [07 §3 API candidates](07-organization-membership-review-worksheet.md#3-datn-233--concrete-api-candidates)
cho list/invite/suspend/remove và mở rộng command surfaces cho grid RP-03 sau
review. ACT-A cần recipient accept surface riêng, không dùng ACT-B ADMIN activate
route. Admin list chỉ own Organization và fields tối thiểu; recipient chỉ thấy
lời mời của mình. Không role/grant/cascade/actor field client-writable.

Đề nghị 401 cho ordinary auth failure, 403 cho thiếu action authority, uniform
404 cho target không tồn tại/không nhìn thấy sau applicable authorization, 422
cho invalid DTO, 409 cho duplicate/illegal/stale command; invitation credential
failure dùng safe generic response, status/code cần chốt. Reuse envelope/page
conventions E4; exact DTO limits, sorting/projection/PII và mixed-error precedence
vẫn Q4–Q6. Không copy nguyên vendor errors hoặc mở Organization paths trong OpenAPI.

Đề nghị require một concurrency precondition chống cả stale state cycle, cùng
business idempotency cho mutation để giải quyết uncertain commit/retry. Q5/Q6
phải chốt request key scope/expiry, payload mismatch, permission recheck, replay
response và conflict precedence; expectedStatus một mình chưa đủ. Version/ETag/
fence field/mechanism vẫn UNKNOWN. [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)
phân biệt idempotent method; POST không tự làm command retry-safe. Đây là contract
requirement đề nghị, không phải persistence implementation được chọn.

### RP-06 — Bảo toàn audit invariant, xác minh canonical authority

AGENTDB §6 / B6 / 06 §6/Q7/AT-07 **đã yêu cầu IAM mutation và audit giữ atomicity**
trong continuum_audit theo ADR-003. Không đề nghị mở lại invariant hay eventual
audit tùy ý. Architecture/DB cần cung cấp canonical ADR-003/SPEC-001 revision và
phạm vi Organization; thiếu authority/scope là reconciliation blocker.

Collection, event/action identifier, payload, transaction mechanism/boundary,
rollback/error/retry/deduplication, rejected-attempt audit và retention/outbox
policies **vẫn UNKNOWN**. Đề nghị leader giao người chốt các specifics đó cùng
IAM/Security; public vendor docs không thay thế authority. Giữ replica-set
commit/rollback proof trước cutover theo invariant hiện hành; docs checks không
phải bằng chứng transaction hay runtime acceptance.

## 4. Leader cần chốt gì và ai chịu trách nhiệm

Tên approver chưa xác nhận. Leader điều phối/chỉ định authority; không mặc định
leader, Phuc, Danh hoặc Tien có mọi quyền phê duyệt. Phuc chuẩn bị contract;
Danh hỗ trợ context evidence; Tien review FE consumption theo 07 §6.

| Decision package | Câu hỏi leader cần giao/chốt | Authority cần xác nhận / downstream |
|---|---|---|
| D1 / Q1/Q2 / RP-01 | Chọn INV-A + ACT-A có điều kiện hay amendment nào? Xác nhận nguồn/provisioning User, owner, eligibility và ADMIN selection an toàn; thiếu thì giao dependent work nào? Defer new-account invite? Ai duyệt narrow recipient auth? Xác nhận hiểu ACTIVE có thể cho phép Project create với roles=[] theo E14; hạn chế phải là Project decision riêng. | Product + IAM/auth + Security; 231/233 và invite/accept 87/88; account-source/selection dependency chưa được đặt mã |
| D2 / Q2/Q5/Q6 / RP-02 | TTL 7 ngày, single-use, resend invalidation, expiry giữ pending và DEL-A có phù hợp? Exact rate/delivery/error policy? | Product + Security + IAM + Notification/DB liên quan; 231/233/234 |
| D3 / Q1/Q3 / RP-03 | Duyệt/amend đủ 16 cells và first creation; commands nào enabled/excluded/deferred? Self/peer/last-ADMIN, reason và recovery? | Product + IAM + Security; 232/234 và operation set 87/88 |
| D4 / Q1/Q3/Q6–Q8 / RP-04 | Giữ records, không auto-restore/cascade? Chốt normal handover-before-remove riêng với emergency suspend/access-block-before-handover; exact actor/delegation, audit/recovery, peer/last-ADMIN safeguards và later remove? Revocation SLA/in-flight/cache/domain effects là gì? | Product + Security/IAM + Project/Team/Task/knowledge/handover owners + DB; 232/234 và downstream domains; không suy platform bypass |
| D5 / Q4–Q6 / RP-05 | Exact HTTP/DTO/visibility/errors, recipient route, mixed failures, retries và concurrency guarantees? | IAM/API + Product/Security + FE, DB liên quan; 233/234 rồi 87/88 |
| D6 / Q7 / RP-06 | Ai cung cấp canonical ADR/SPEC, reconcile scope và phê duyệt audit specifics trong invariant hiện hành? | Architecture/DB + IAM + Security; audit mutation implementation blocked |

Mỗi câu trả lời dùng decision record 07 §6: exact rule/amendment; scope; named
authority/approver; date; canonical revision; error/effect oracle; affected
API/DB/tests và remaining UNKNOWN. “Đồng ý nghiên cứu” hoặc technical LGTM không
đủ để chọn tất cả RP. Approved deferral phải chỉ rõ required scope nào được điều
chỉnh và downstream nào vẫn blocked; không silently tính phần thiếu là completed.

## 5. Review và bước tiếp theo sau quyết định

DATN-234 review accepted grid/commands/actor/effects/DTO/errors theo RV-01–08 và
AT-01–09, gồm wrong recipient/expiry/replay, foreign Organization, self/peer/last
ADMIN, concurrency/uncertain commit, domain+audit failure, stale descendant grants
và resume/rejoin. RV-02 kiểm tra account-source/recipient-selection prerequisite
và Project-create consequence sau future accepted activation (roles=[], configured/
missing MEMBER Role); RV-07 tách normal/emergency ordering và safety/recovery.
UNKNOWN oracle không được đánh PASS. Có thể validate contract
được duyệt trước BE implementation; runtime tests sẽ thuộc DB/BE/FE lanes.

Sau sign-off exact revision, Phuc reconcile 06/07 và owning API contract, review
từng child acceptance rồi cập nhật status theo kết quả thật; đánh giá lại expected
result DATN-86. DB/schema/migration nếu cần có task/branch/PR riêng trước BE; BE87
chỉ implement accepted operations, FE88 phụ thuộc accepted API + BE. Research R5
không sửa app/schema/index/migration/data hoặc tự unblock dependencies.

## 6. Đoạn tin nhắn để người dùng gửi leader

> Em đã research tài liệu chính thức GitHub, GitLab, Auth0 và Clerk cho DATN-86.
> Bốn subtasks 231–234 đang thiếu quyết định invitation, lifecycle/offboarding,
> API/audit và rule table để validation; tài liệu hiện có chưa là product contract
> được duyệt. Đề nghị MVP mời user có tài khoản chỉ khi IAM xác nhận nguồn tạo
> tài khoản, owner, eligibility và cách ADMIN tìm/chọn recipient an toàn; thiếu
> thì cần giao việc phụ thuộc trước triển khai, dev seed/manual DB chưa đủ.
> Người nhận tự accept qua luồng xác thực giới hạn; ACTIVE có thể cho phép tạo
> Project dù roles=[] theo baseline, tạo thành công còn cần MEMBER Role có
> project.read để bootstrap. Đề nghị giữ baseline; hạn chế Project create cần
> decision riêng. Invite đề nghị 7 ngày/single-use, resend vô hiệu link cũ;
> suspend/remove chỉ trong Organization, giữ dữ liệu, review quyền khi resume/rejoin. Gói
> research có bảng 16 transitions đề nghị, safeguards, API choices và sáu decision
> packages để review, tất cả còn PROPOSED.
>
> Nhờ anh/chị chỉ định Product/IAM/Security/DB và domain owners có thẩm quyền,
> review D1–D6, chốt account-source/selection và recipient khi chưa có ACTIVE context.
> Offboarding đề nghị tách bình thường bàn giao trước remove; khẩn cấp suspend/
> chặn access trước, người được ủy quyền bàn giao sau rồi remove nếu phù hợp.
> Exact actor, audit/recovery, peer/last-ADMIN safeguards và revocation SLA cần
> Product/Security chốt; không suy quyền quản trị thường xuyên từ platform role.
> Cần xác minh canonical audit scope. Atomicity IAM mutation + audit là yêu cầu hiện
> hành, không phải lựa chọn tùy ý; chi tiết implementation còn UNKNOWN. Có thể dùng
> In Review để review proposal, nhưng Done cần acceptance của exact contract.
>
> Jira: https://trankimthang0207.atlassian.net/browse/DATN-86
> Request: https://github.com/DATN-SPRING2027/Document/pull/23
> Research: xem file 08 trong PR; worksheet chi tiết: file 07. Đây là đề nghị xin
> quyết định, không phải thông báo policy đã được chốt.
