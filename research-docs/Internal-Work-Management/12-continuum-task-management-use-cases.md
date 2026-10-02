# Đề xuất Use Case quản lý Task cho Continuum AI

**Trạng thái:** Nguồn task nội bộ đã được người dùng chốt; danh sách Use Case chi tiết vẫn là đề xuất chờ duyệt.

**Ngày:** 2026-10-01.

**Mục tiêu sản phẩm:** ghi nhận công việc → đề xuất tri thức → con người kiểm chứng → hỏi đáp có dẫn chứng → bàn giao cho người kế nhiệm.

**Nguồn đầu vào:** danh sách 299 use case Jira do người dùng cung cấp để tham khảo; `research-docs/01_MVP_SCOPE.md`; `research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md`; `research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md`; ADR-009 và ADR-010.

## 1. Quyết định nguồn task đã chốt

Danh sách 299 use case trong tài liệu tham khảo mô tả một hệ thống quản lý dự án rộng như Jira. Continuum AI cần quản lý công việc để giữ lại ngữ cảnh, bằng chứng, trách nhiệm và trạng thái cho tri thức/bàn giao; không cần tái tạo toàn bộ Jira.

`[DECIDED — 2026-10-01]` Người dùng xác nhận nhóm **không dùng Jira làm nguồn task** và sẽ tự xây chức năng quản lý task. Vì vậy, **Continuum Task API là nguồn chính và duy nhất cho vòng đời task DATN trong phạm vi MVP; bản ghi chuẩn được lưu trong MongoDB**. Jira không phải actor, nguồn đồng bộ, hay nguồn dự phòng của các Use Case dưới đây. Nếu sau này cần import/link Jira như nguồn tham khảo, phải duyệt thành phạm vi riêng; không tạo đồng bộ ghi hai chiều. Nguồn task/MongoDB xem [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md); ranh giới repository/service/deployment xem [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md).

`[PROPOSAL]` Xây một **task tracker nội bộ tối giản**, giới hạn trong một software project có nhiều team và gắn trực tiếp với Work Note/Handover. Không đặt mục tiêu parity với Jira. Hướng nguồn task này đã chốt; danh sách P0/P1, trạng thái, field và luồng cụ thể bên dưới vẫn cần bạn duyệt trước khi trở thành requirement chi tiết.

## 2. Giả định và ranh giới

- Task phục vụ theo dõi việc đang làm/chưa xong và giữ ngữ cảnh công việc cho thành viên, Team Leader và người kế nhiệm.
- Continuum vẫn phân biệt task với knowledge: nội dung task không tự động trở thành tri thức đã xác minh. Work Note do thành viên xác nhận; Proposed Knowledge cần người có quyền kiểm chứng.
- Phạm vi tổ chức vẫn là một project phần mềm có nhiều team. Không thêm Department, portfolio, quản lý nhân sự hay chấm điểm năng suất.
- Dùng actor/role đã có trong baseline: `ADMIN`, `TEAM_LEADER`, `MEMBER`; `SUCCESSOR` là assignment có scope/thời hạn, không phải role mới. Quyền phải tuân theo project/team scope và ACL hiện hành.
- Trạng thái, field và ma trận quyền chi tiết trong tài liệu này vẫn là đề xuất chờ duyệt; các khuyến nghị để xử lý câu hỏi sản phẩm được tổng hợp ở mục 7.
- Khuyến nghị mỗi task bắt buộc thuộc đúng một project và có thể gắn tối đa một team trong project đó; không hỗ trợ task đa project/đa team trong MVP.
- Work Note có thể không liên kết task; nếu có, liên kết tối đa một task qua `taskId`. Một task có thể được tham chiếu từ nhiều Work Note. API phải kiểm tra task tồn tại và caller được phép truy cập task.
- Chỉ Work Note/evidence đã qua kiểm tra quyền và đủ điều kiện nguồn mới được đưa vào SAG retrieval/index. Task, status và assignee không phải nguồn SAG độc lập.
- Handover đọc task từ Task API; Team Leader có quyền chọn task và giao cho successor. Handover giữ workflow/tham chiếu bàn giao, không trở thành nguồn ghi task thứ hai.
- Task Service là microservice NestJS triển khai độc lập nhưng mã nguồn thuộc DATN_BE hiện có; task UI/client thuộc DATN_FE hiện có. Service sở hữu database logic `continuum_task` trên MongoDB replica set hiện có; không tạo repository ManageWork hay MongoDB cluster vật lý mới. FE gọi qua BFF/Gateway; các service/Agent truy cập bằng API hoặc event contract, không đọc/ghi database trực tiếp. Task Service không quyết định công nghệ lưu SAG.

## 3. Use case đề xuất — P0 của task nội bộ

Các mã Jira trong cột cuối là nguồn gợi ý từ danh sách bạn gửi; phần lý do xác định vì sao use case phù hợp với Continuum. Những UC mới có ký hiệu “mới” vì phục vụ riêng luồng tri thức/bàn giao.

| ID | Use case | Actor chính | Phạm vi đề xuất và lý do | Tham chiếu danh sách |
|---|---|---|---|---|
| UC-TM-01 | Xem danh sách task trong project | MEMBER, TEAM_LEADER; SUCCESSOR chỉ xem task được bàn giao | Thấy việc đang làm/chưa xong, người phụ trách và hạn; phạm vi chỉ trong project/team được cấp quyền. | #31 |
| UC-TM-02 | Tạo task | MEMBER, TEAM_LEADER | Tạo một đơn vị công việc cơ bản để ghi nhận trách nhiệm và trạng thái. Chỉ cần một loại `Task`; follow-up handover dùng cùng task; không cần Epic/Story/Bug/Version. | #30, #60 |
| UC-TM-03 | Xem chi tiết task | MEMBER, TEAM_LEADER; SUCCESSOR theo assignment | Hiển thị mô tả, trạng thái, người tạo/phụ trách, hạn, ưu tiên và Work Note/nguồn liên quan để giữ ngữ cảnh. | #31 |
| UC-TM-04 | Chỉnh sửa thông tin task | MEMBER là người tạo hoặc assignee hiện tại; TEAM_LEADER trong scope được giao | Cập nhật tiêu đề, mô tả, ưu tiên, hạn. Giữ lại thay đổi quan trọng để ngữ cảnh bàn giao không bị mất. | #32, #40, #43, #44 |
| UC-TM-05 | Gán hoặc chuyển người phụ trách | TEAM_LEADER | Xác định owner hiện tại và chuyển trách nhiệm khi đổi người hoặc bàn giao. Chỉ gán người thuộc cùng project/team scope; ghi nhận actor và thời điểm. | #36–38, #41 |
| UC-TM-06 | Cập nhật trạng thái task | Người phụ trách hiện tại, TEAM_LEADER | Theo dõi task từ chưa làm đến hoàn tất hoặc bị chặn; chỉ cho phép các chuyển trạng thái cố định và ghi lịch sử. | #39 |
| UC-TM-07 | Tìm kiếm/lọc task cơ bản | MEMBER, TEAM_LEADER; SUCCESSOR theo assignment | Lọc theo project, trạng thái, người phụ trách, ưu tiên, hạn; tìm theo tiêu đề. Đủ để tìm đúng ngữ cảnh mà không cần JQL hay bộ lọc chia sẻ. | #146, #150–151, #153–154, #158 |
| UC-TM-08 | Liên kết Work Note với task | MEMBER | Khi ghi Work Note, người dùng có thể chọn task nội bộ liên quan. Work Note vẫn là phần giải thích “đã làm gì, làm thế nào/vì sao, vướng mắc gì”; task chỉ cung cấp context. | Mới; phù hợp mục 4 và 6.2 của `01_MVP_SCOPE.md` |
| UC-TM-09 | Rà soát và bàn giao task còn mở | TEAM_LEADER; SUCCESSOR xem phần được giao | Trong quy trình handover, Continuum lấy task còn mở qua Task API; Team Leader chọn task và giao successor. Task API cập nhật assignee canonical; Handover lưu `taskId` và trạng thái tiếp nhận, không tạo bản task thứ hai. Successor chỉ xem task được giao và evidence được phép. | Mới; nối với 6.5 `01_MVP_SCOPE.md` |
| UC-TM-10 | Xem lịch sử thay đổi quan trọng của task | MEMBER/TEAM_LEADER theo scope; SUCCESSOR với task được giao | Xem tối thiểu lịch sử đổi trạng thái, owner, hạn và ưu tiên (người thực hiện + thời điểm), hữu ích khi cần biết trách nhiệm/tiến độ đã đổi ra sao. Không phải trang audit toàn hệ thống. | #54–55, #293, #298–299 ở mức giới hạn |

### Agent contract — bắt buộc về ranh giới, giới hạn triển khai đề xuất

Task API phải cho phép các tính năng AI/Agent được tích hợp qua authenticated API/event contract, không qua truy cập database. Với task thuộc scope người dùng, Agent chỉ tạo bản đề xuất (ví dụ rewrite title/description hoặc gợi ý cập nhật); người có quyền xem diff và xác nhận trước khi Task Service ghi thay đổi canonical. API lưu được danh tính người khởi tạo, Agent/proposal ID và quyết định xác nhận vào lịch sử.

| ID | Use case | Actor chính | Giới hạn |
|---|---|---|---|
| UC-TM-11 | Agent đề xuất chỉnh sửa nội dung task | Task Agent; người có quyền xác nhận | Lấy task context theo quyền của người khởi tạo, trả draft/diff và lý do; không tự ghi task, đổi assignee/status hay cấp quyền. Đề xuất thực hiện sau P0 CRUD/ACL/API; nếu tích hợp Agent trong MVP, chỉ triển khai luồng draft → human approve. |

### Trạng thái và thao tác đề xuất

Để không xây workflow editor, dùng trạng thái cố định ban đầu: `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`. Đây là `[PROPOSAL]` cần duyệt; `BLOCKED` giúp bộc lộ việc đang mắc, còn trạng thái kiểm chứng tri thức phải tiếp tục tách riêng khỏi task status. Chuyển trạng thái thường do người phụ trách hoặc Team Leader thực hiện. Task `DONE` có thể được mở lại thành `IN_PROGRESS` bởi người phụ trách hoặc Team Leader kèm lý do; `CANCELLED` là trạng thái kết thúc trong MVP. Không xóa cứng task để bảo toàn liên kết Work Note và lịch sử.

Priority đề xuất: `LOW`, `MEDIUM`, `HIGH`, mặc định `MEDIUM`; due date là tùy chọn. Task type chỉ có `TASK`. Bộ giá trị cuối cùng chưa được chốt.

### Field tối thiểu đề xuất

`organizationId`, `projectId`, `title` và `createdBy` là bắt buộc; hệ thống sinh `status`, `priority`, `createdAt` và `updatedAt`. `teamId`, `description`, `assigneeId` và `dueDate` là tùy chọn; khi tạo, Member chỉ có thể để trống assignee hoặc tự gán cho mình. Team Leader mới được giao task cho người khác. Mongo `ObjectId` là định danh canonical; human-readable task key để ngoài P0.

### P1 — chỉ đưa vào nếu còn thời gian sau luồng P0

| Use case | Lý do / giới hạn |
|---|---|
| Xem Kanban board đơn giản và chuyển task giữa các cột | Hữu ích để nhìn nhanh việc đang mở/đang bị chặn, nhưng list + filter đã đáp ứng mục tiêu tìm ngữ cảnh. Nếu làm, chỉ một board với cột cố định theo status; không cho cấu hình cột, swimlane, WIP limit hay card layout. Nguồn gợi ý: #116, #120–122. |
| Tạo sub-task một cấp | Chỉ cần nếu một follow-up handover phải chia thành bước con độc lập. Trước hết ưu tiên checklist handover đã có để tránh hai mô hình trùng lặp. Nguồn gợi ý: #62, #64. |

Nếu demo bắt buộc phải có giao diện kiểu Jira board, có thể nâng Kanban đơn giản thành P0; khi đó cần giảm một phần P1/tiện ích khác, không mở rộng sang Scrum.

## 4. Không đưa vào MVP này

| Nhóm use case trong tài liệu tham khảo | Quyết định đề xuất | Lý do với Continuum AI |
|---|---|---|
| Sprint, Scrum backlog, estimate/story point, velocity/burndown (#50–51, #89–115, #214–219) | Loại | Mục tiêu hiện tại là duy trì context và bàn giao, không phải đo năng suất Scrum hoặc lập kế hoạch release. |
| Epic/Story/Bug, version/release, component (#47–50, #58–66, #97–99, #164–186, #223–225) | Loại | Tăng taxonomy/cấu hình nhưng không cần cho vòng đời Work Note → knowledge → handover. Một loại task đơn giản đủ cho bản đầu. |
| Configurable workflow/status/transition (#26–28, #125–129, #134–145) | Loại | Một workflow cố định giảm rủi ro scope và quyền quản trị; chưa có yêu cầu cho mỗi team tự thiết kế lifecycle. |
| Dependency graph, link type phức tạp (#67–75, #232–234) | Hoãn | Ghi blocker trong Work Note/trạng thái `BLOCKED` trước; dependency graph cần thêm validation, xử lý vòng lặp và UI. |
| Comment thread, mention, reaction, watcher, chia sẻ và file đính kèm task (#76–88) | Loại khỏi P0 | Work Note có cấu trúc và xác nhận người dùng phù hợp hơn làm nguồn ngữ cảnh/tri thức. File/evidence nên đi qua luồng quản lý nguồn có ACL/provenance, không tạo đường đính kèm task riêng. |
| Time tracking và estimate (#52–53, #187–194, #222) | Loại | Không phục vụ trực tiếp mục tiêu handover; tránh biến sản phẩm thành công cụ chấm/đo cá nhân. |
| JQL, advanced/shared/saved filters (#148–149, #159–163), board tùy biến (#123–129) | Loại | Basic search/filter là đủ cho một project; query language và cấu hình nâng cao tăng chi phí đáng kể. |
| Automation builder và email/notification rules (#195–204, #259–267) | Hoãn | MVP hiện yêu cầu reminders cho Work Note/knowledge thiếu hoặc quá hạn; không cần bộ rule engine hoặc notification policy tổng quát. |
| Dashboard, reports, roadmap/timeline (#205–234) | Loại | Chỉ xây khi có persona và quyết định cụ thể cần hỗ trợ; không suy ra dashboard chỉ vì Jira có. |
| User/group/permission scheme management (#235–258) | Không lặp lại trong task module | IAM/role/permission đã có baseline riêng. Mọi task API vẫn bắt buộc kiểm tra quyền theo project/team; không tạo permission scheme builder riêng. |
| Git/development integration, import/export, bulk operations (#268–292) | Hoãn | Không thuộc vòng lặp cốt lõi và có thể làm trễ luồng capture/handover. |
| Delete task (#33), restore/archive tổng quát (#15–16, #34–35) | Không làm trong P0 | Giữ lịch sử và liên kết; dùng trạng thái `CANCELLED`. Archive/retention chỉ cần khi có policy đã xác nhận. |

Authentication, profile, project/member lifecycle và cấp quyền ở cấp tổ chức/project không được sao chép vào tài liệu task này; tiếp tục dùng các use case/baseline tương ứng của Continuum, được nối tại [Project, Team and Membership Use Cases](../Workspace/05-project-team-access-use-cases.md).

## 5. Actor và quan hệ với use case hiện có

- **MEMBER:** tạo task trong phạm vi được cấp; chỉ sửa task mình tạo hoặc đang được giao; đổi trạng thái theo policy, ghi Work Note và tùy chọn liên kết note với task.
- **TEAM_LEADER:** xem tiến độ trong scope, gán/chuyển owner, theo dõi việc bị chặn, rà soát danh sách việc còn mở và chọn nội dung bàn giao.
- **SUCCESSOR assignment:** chỉ xem task/context đã được bàn giao hoặc tài nguyên mà ACL cho phép; đây là assignment scope, không phải role mới.
- **ADMIN:** duy trì user/project/integration/policy theo baseline; `ADMIN` không tự động được đọc nội dung task/tri thức mật.
- Không có actor hệ thống task bên ngoài trong Use Case MVP: Continuum tự quản lý task và toàn bộ vòng đời task DATN.
- **Task Agent / AI Engine:** chỉ đọc task context được Task API cấp theo người dùng và đề xuất thay đổi qua contract. Không gọi DB trực tiếp, không tự commit, đổi assignee/status hay thay đổi ACL; mọi mutation cần người có quyền xác nhận và được ghi audit. Agent integration phải dùng ranh giới API/event của Task Service, nhưng mức tính năng rewrite còn tùy scope MVP.

Quan hệ UML đề xuất:

- `Ghi Work Note` có thể được mở rộng bởi `Liên kết Work Note với Task` khi người dùng chọn task (`<<extend>>`, lựa chọn tùy chọn).
- `Chuẩn bị Handover Package` gồm bước lấy/rà soát task còn mở từ task store nội bộ (`<<include>>`).
- Không dùng `<<include>>` cho “Task trở thành Knowledge”: đây là hai thực thể/lifecycle khác nhau; knowledge cần evidence và human verification.

## 6. Điều kiện chấp nhận mức use case

Nếu duyệt hướng internal task tracker, P0 chỉ được xem là đủ khi:

1. Member/Team Leader chỉ thao tác trên task trong project/team scope được phép; successor chỉ thấy context đã được cấp.
2. Tạo, gán, cập nhật trạng thái/ưu tiên/hạn, tìm kiếm/lọc và xem chi tiết đều được mô tả cho actor và luồng lỗi/quyền phù hợp.
3. Work Note có thể giữ liên kết ổn định tới task; liên kết không làm Work Note thành task và không tự nâng nội dung task thành verified knowledge.
4. Handover hiển thị owner, status, due date, Work Note/context liên quan của việc còn mở; việc chuyển owner được ghi lại và tuân theo scope.
5. Hành động quan trọng có actor/time history theo authorization baseline; không rò nội dung qua task search, note link, handover hoặc AI context.
6. Vòng đời, trạng thái và người phụ trách task được đọc/ghi trong Continuum; Jira không tham gia các luồng này.

Đây là tiêu chí proposal cho tài liệu/use case, chưa phải kiểm thử hay xác nhận triển khai.

## 7. Khuyến nghị xử lý các câu hỏi trước khi chốt SRS

Các mục dưới đây là **đề xuất để người dùng duyệt**, không phải quyết định đã được chấp thuận. Tác động chi tiết được liên kết tới tài liệu sở hữu nội dung để tránh mỗi tài liệu tự đặt một bộ quy tắc khác nhau.

| # | Câu hỏi | Hướng giải quyết đề xuất | Mapping chính |
|---:|---|---|---|
| 1 | Task thuộc project, team hay cả hai? | Bắt buộc đúng một `projectId`; `teamId` tùy chọn và phải thuộc project đó. | Task schema, permission baseline, workflow |
| 2 | Một task thuộc nhiều team? | Không trong MVP; tối đa một team. Việc liên team xử lý qua Handover/Work Note, không nhân bản task. | Task schema, Use Case |
| 3 | MEMBER tạo task/giao task cho người khác? | MEMBER được tạo task trong scope, để trống assignee hoặc tự gán; chỉ Team Leader giao/chuyển sang người khác. | Permission matrix, API proposal |
| 4 | Ai chuyển owner, đóng, hủy, mở lại? | Team Leader gán/chuyển owner và hủy; người phụ trách hoặc Team Leader đổi status. DONE mở lại thành `IN_PROGRESS` có lý do; CANCELLED không mở lại trong MVP. | Permission matrix, status flow, audit |
| 5 | Bộ status chính thức? | Cố định `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED`; không có workflow editor hoặc status `REOPENED`. | Use Case, Task schema |
| 6 | Field bắt buộc? | Bắt buộc `organizationId`, `projectId`, `title`, `createdBy`; hệ thống đặt `status=TODO`, `priority=MEDIUM`, timestamps. Team, description, assignee, due date tùy chọn. | Task schema, API contract |
| 7 | Task type? | Chỉ một loại `TASK`; không có Epic/Story/Bug trong MVP. | Use Case, MVP scope |
| 8 | Kanban P0 hay P1? | P1; list, detail, create/edit, transition và filter là P0. Chỉ nâng board lên P0 nếu demo yêu cầu và đổi scope được xác nhận. | MVP scope, FE architecture |
| 9 | Quan hệ Work Note–Task? | Một Work Note gắn 0–1 task; một task có 0..N Work Note. Liên kết là `taskId` tùy chọn, được Task API xác thực. | Capture schema, Task schema |
| 10 | DONE có cần Work Note/evidence? | Không. Hoàn thành task không đồng nghĩa đã ghi đủ tri thức hoặc knowledge được verify. | Daily workflow, lifecycle |
| 11 | Task nào vào Handover? | Mặc định chỉ task chưa kết thúc (`TODO`, `IN_PROGRESS`, `BLOCKED`) là mục giao việc. Task đã DONE có thể được trích dẫn qua Work Note/evidence read-only, không chuyển owner. | Handover schema/workflow |
| 12 | Ai xác nhận giao task? | Team Leader khởi tạo assignment; successor xác nhận đã nhận/nắm gói Handover. Trong luồng giao task, Task API đổi assignee canonical sang successor; hai actor không tạo hai assignee độc lập. | Handover workflow, Task API, audit |
| 13 | Successor giữ quyền bao lâu? | Chỉ task được chọn trong Handover; không kế thừa quyền toàn project. Quyền task theo assignee/scope hiện hành và bị thu hồi khi reassignment hoặc mất membership; gói Handover đã hoàn tất còn read-only theo ACL. | Handover ACL, security |
| 14 | ADMIN có mặc định đọc task? | Không. Quyền quản trị không tự cấp quyền đọc nội dung task hoặc evidence. | Role matrix, security |
| 15 | Có index task text vào SAG? | Không index task record, title, description, status hay assignee. Chỉ Work Note/evidence đã được tác giả xác nhận, đủ điều kiện nguồn và ACL mới được index. | Ingestion schema, SAG storage |
| 16 | Comment/file/mention/watcher/notification? | Không đưa comment, attachment, mention, watcher hay task notification riêng vào P0. Dùng Work Note/evidence và Handover hiện có; đánh giá thông báo assignment ở P1. | MVP scope, notification boundary |
| 17 | Task history lưu gì? | `task_events` append-only ghi actor/time và field thay đổi cho status, assignee, due date, priority, team, title/description, cancel/reopen; không lưu snapshot toàn bộ task trong event. Hiển thị theo cùng quyền task; successor chỉ xem event của task được giao. | DB schema, audit, security |
| 18 | Task key? | Dùng Mongo `ObjectId` canonical trong P0; chưa tạo sequence/key theo kiểu Jira. UI có thể rút gọn ID khi cần. | API/data contract |
| 19 | Import task từ ManageWork/Jira? | Không bulk import trong MVP. ManageWork là tham khảo hành vi/UI; dữ liệu task không được tự nhập sang Continuum Mongo. Nếu cần dữ liệu thật, làm mapping/import riêng và duyệt migration trước. | ADR-010, migration plan |
| 20 | Task quyết định SAG retrieval engine nào? | Không. Task Service giữ task trong MongoDB; chỉ Work Note/evidence đủ điều kiện đi vào SAG. Công nghệ SAG thuộc ADR riêng. Nếu chọn PostgreSQL và Qdrant cùng lúc, ADR đó cần nói rõ PostgreSQL giữ relational metadata còn Qdrant giữ vector, hay PostgreSQL + pgvector là lựa chọn thay Qdrant. Quyết định Task không thay đổi engine. | SAG storage ADR and architecture |
| 21 | Task nào được chép/index nếu có hai DB? | Không chép/index task. Continuum kiểm tra ACL nguồn hiện hành; thu hồi thì chặn retrieval ngay và xếp việc de-index, không phụ thuộc index cũ. | Security, ingestion, SAG storage |
| 22 | Tách Task thành repo mới hay tích hợp vào repo hiện tại? | Giữ mã nguồn service trong DATN_BE, UI/API client trong DATN_FE; triển khai Task thành NestJS service/process riêng, route qua Gateway và sở hữu database logic `continuum_task`. Không tạo ManageWork repo mới. Trade-off và cách setup xem ADR-010. | ADR-010, BE topology, FE architecture |
| 23 | Transaction task/history/handover? | Transaction trên Mongo replica set bảo đảm task mutation + `task_events` (và outbox khi cần) nguyên tử trong `continuum_task`. Handover gọi Task API bằng `operationId` idempotent và retry/compensation rõ ràng; không truy cập database Task trực tiếp. | Task schema, Handover schema, architecture |
| 24 | Dashboard/report hay capture/handover? | Không làm dashboard/report trong MVP; ưu tiên task lifecycle, capture và handover. Chỉ mở lại khi có persona, quyết định cần hỗ trợ và nguồn metric cụ thể. | MVP scope |

### Ranh giới cập nhật tài liệu

- **ADR-009** sở hữu quyết định đã chốt: Continuum là nguồn task và MongoDB lưu bản canonical; không dùng Jira làm nguồn trong MVP.
- **ADR-010** sở hữu ranh giới repo/service/deployment, giao tiếp Gateway/API/event và vị trí database logic của Task; ưu nhược điểm được ghi trong ADR để review.
- **Tài liệu này** sở hữu Use Case/P0/P1 và các đề xuất sản phẩm còn chờ duyệt.
- **`12_TASK_MANAGEMENT_SCHEMA.md`** sở hữu field/cardinality/index/history đề xuất; **`02_ACTORS_ROLES_AND_PERMISSIONS.md`** sở hữu ma trận quyền; **`03_DAILY_WORKFLOW_AND_JIRA_SYNC.md`** sở hữu luồng Capture/Handover.
- Kiến trúc, Capture/Handover/ingestion schema và diagram chỉ mô tả các boundary trên; chúng không được tự đưa task thành nguồn SAG hay mở rộng P0.
- Quyết định vector engine, SAG schema và runtime không nằm trong ADR-010; phải được chốt/ghi riêng để không làm sai lệch phạm vi Task.
