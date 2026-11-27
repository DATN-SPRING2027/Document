# WorkNote Rewrite — Product & Coder Brief

**Trạng thái:** Brief theo yêu cầu sản phẩm; chưa phải OpenAPI, quyết định database hay phê duyệt tích hợp SAG.  
**Mục tiêu:** Cho phép người viết ghi Work Note tự do, sau đó dùng AI để biên tập thành nội dung rõ ràng, đúng ngữ pháp và dễ tìm lại; người viết kiểm soát bản cuối.

## Tóm tắt cho người đọc

Người dùng mở WorkNote trong một popup lớn, nhập tiêu đề và ghi nội dung theo cách tự nhiên của họ. Không có các ô bắt buộc What/How/Why. Agent đọc Task được liên kết để hiểu mục tiêu, phạm vi và tiêu chí hoàn thành rồi đối chiếu với ghi chú.

Icon Agent nằm trên thanh đầu popup. Bấm icon sẽ mở khung chat ở dưới nội dung, nơi người dùng có thể chọn gợi ý nhanh hoặc chat nhiều lượt để hướng dẫn Agent. Nếu Agent cần làm rõ thông tin quan trọng, chat tự mở và hỏi ngay tại đó; nếu đã đủ dữ kiện thì Agent không ngắt quãng để hỏi cho có. Muốn chỉnh một đoạn, người dùng bôi đen đoạn đó, bấm icon Agent hiện cạnh vùng chọn và gửi yêu cầu cho đúng phần ấy.

Agent đưa ra đề xuất kèm phần thay đổi để người dùng xem trước. Người dùng quyết định áp dụng, sửa tiếp hoặc bỏ. Có thể lưu nguyên bản mà không dùng AI. Bản nháp, tin nhắn chat và đề xuất chưa được áp dụng không trở thành nội dung WorkNote hay được đưa vào SAG.

Phần dưới là brief chi tiết cho coder: bố cục, hành vi, dữ liệu, quyền, tích hợp và tiêu chí nghiệm thu.

## 1. Bối cảnh và ranh giới

- Form Project Work Notes hiện trong DATN-FE là preview dùng state cục bộ, chưa có API Work Note tương ứng. Preview hiện có các loại `WORK_UPDATE`, `WEEKLY_SUMMARY`, `KNOWLEDGE`, `DECISION`; không được coi enum này là contract backend.
- Capture backend hiện có schema `title`, `whatDone`, `howSolved`, `whyThisWay` và `work_note_versions`; các trường What/How/Why chưa cho phép ghi tự do đúng yêu cầu mới.
- Quy trình Work Note của sản phẩm tách **Task Note**, **Project Document** và **Periodic Work Report**. Brief này thay đổi cách nhập/biên tập nội dung; không gộp ba workflow, thay quyền, trạng thái duyệt hay lịch báo cáo.
- Tài liệu workflow 03 trên `origin/main` dẫn tới `04_WORK_NOTE_WORKFLOWS.md`, nhưng file 04 hiện chỉ thấy trên branch tài liệu riêng tại thời điểm soạn. Trước khi triển khai, agent phải đối chiếu revision được duyệt với code hiện tại.

Tham chiếu: `research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md`, `database-design/02_SVC_CAPTURE_SCHEMA.md`, `database-design/11_SAG_STORAGE_SCHEMA.md`, `DATN-FE/tasks/work-notes-ui/design.md`, `DATN-BE/src/services/capture/infrastructure/mongodb/mongodb.schemas.ts`, `sag-laya-integration/SAG/apps/api/sag_api/api/v1/documents.py`.

## 2. Kết quả sản phẩm

Người dùng có một vùng nhập tự do để ghi theo cách của họ: văn xuôi, gạch đầu dòng, ghi chú ngắn, code, log, đường dẫn hoặc trộn nhiều kiểu. Agent kết hợp nội dung này với context Task được cấp quyền để hiểu đang cần hoàn thành việc gì và note đã ghi nhận được gì. Trong cùng popup, họ có thể chat liên tục với Agent để chỉnh toàn note hoặc một đoạn; AI tự chọn cách sắp xếp phù hợp với nội dung, không bắt mọi ghi chú phải có cùng bộ heading. Lưu note không phụ thuộc vào việc có dùng AI hay không.

Workflow metadata vẫn tách khỏi phần nội dung:

- Task Note: tạo từ Task; `taskId` là bắt buộc và được kiểm tra cùng Project.
- Project Document: nội dung cấp Project, không ép phải gắn Task; giữ luồng version/review hiện hành.
- Periodic Work Report: kỳ báo cáo do hệ thống xác định; giữ cadence và luồng review hiện hành.

Agent Rewrite dùng chung được cho các vùng nhập nội dung nếu workflow cho phép. Tệp PDF/DOCX đính kèm không bị tự sửa hoặc ghi đè bởi Agent.

## 3. Composer: cửa sổ viết WorkNote

### Bố cục

- Mở WorkNote bằng dialog lớn. Desktop dùng gần toàn bộ chiều cao khả dụng; mobile dùng full-screen dialog. Header và thanh lưu cố định, phần soạn thảo cuộn độc lập.
- Header có nút đóng, context WorkNote (Task/Project hoặc kỳ báo cáo), trạng thái lưu và icon Agent. Icon Agent luôn ở cùng vị trí, đổi trạng thái khi panel chat mở.
- Phần nội dung có đúng hai trường chính: **Title** và **nội dung tự do**. Title do người dùng nhập hoặc nhận gợi ý; nội dung không bắt buộc theo What/How/Why.
- Dùng editor/component đã có nếu hỗ trợ giữ selection ổn định. Nếu không, ưu tiên textarea đa dòng có selection offset; không thêm rich-text dependency nếu chưa được duyệt.
- Body cho phép văn xuôi, bullet, Markdown, URL, code/log và nhiều ngôn ngữ. Không tự chuẩn hóa khoảng trắng trong code, log hoặc identifier.
- Metadata như Task ID, Project, period, author, tags và workflow status hiển thị riêng; không chiếm chỗ trong body. Link/evidence chỉ dùng nguồn upload hoặc liên kết được phép hiện có.
- Footer có hành động lưu theo đúng workflow hiện tại. Task Note lưu/xác nhận theo thao tác của tác giả; Project Document/Periodic Report giữ nút submit/draft/review riêng. Đóng dialog giữ draft đã autosave; **Discard draft** là hành động riêng có xác nhận.

### Agent chat ở đáy dialog

- Mặc định chat đóng để dành diện tích cho editor. Click icon Agent mở panel chat gắn ở đáy dialog, dưới editor; editor và chat có vùng cuộn riêng.
- Khi Agent phát hiện câu hỏi làm rõ có ảnh hưởng đáng kể tới nội dung, tự mở panel và đưa câu hỏi vào chat. Giữ nguyên editor, draft và selection để người dùng trả lời ngay. Nếu không cần hỏi, không tự mở chat; người dùng vẫn có thể mở bằng icon.
- Desktop panel mở có chiều cao ban đầu khoảng 280–360 px, co lại/mở rộng và collapse được. Mobile mở thành bottom sheet hoặc panel toàn chiều cao; editor vẫn có thể quay lại mà không mất nội dung.
- Chat có transcript theo draft, ô nhập tự do và nút gửi. Câu hỏi Agent có thể có lựa chọn nhanh và luôn cho phép trả lời tự do, “Chưa biết” hoặc “Tiếp tục mà không bổ sung”. Có quick-prompt chips không bắt buộc: “Sửa ngữ pháp”, “Làm rõ”, “Rút gọn”, “Sắp xếp lại”, “Giữ nguyên ý, đổi giọng văn”, “Viết cho bàn giao”. Người dùng luôn có thể nhập yêu cầu riêng.
- Chat không phải phần nội dung WorkNote và không được hiển thị trong bản lưu hoặc SAG. Có nút xóa/reset hội thoại. Transcript draft chỉ được giữ để khôi phục phiên đang soạn theo retention của draft; không lưu cùng bản WorkNote đã xác nhận trừ khi chính sách riêng được duyệt.
- Chat header/prompt thể hiện context Agent đang dùng: đoạn đang chọn, toàn bộ note và/hoặc Task context. Chỉ gửi context tối thiểu cần cho yêu cầu; không gửi Task metadata ẩn hoặc note khác ngoài scope.

### Luồng soạn thảo

1. Mở dialog, nhập/sửa title và nội dung tự do. Autosave title/body/context theo backend draft contract; có chỉ báo đang lưu/đã lưu/lỗi.
2. Click Agent để hỏi hoặc yêu cầu chỉnh sửa. Agent hiểu Task + note rồi chọn một trong ba kết quả: trả lời trực tiếp, hỏi làm rõ trong chat, hoặc hiển thị suggestion card có phạm vi rõ (**đoạn chọn** hoặc **toàn note**), tóm tắt thay đổi và bản xem trước.
3. Nếu Agent hỏi, người dùng trả lời trong chat. Agent cập nhật cách hiểu và tiếp tục; hỏi tiếp chỉ khi câu trả lời vẫn để ngỏ điểm quan trọng. Người dùng có thể bỏ qua câu hỏi; Agent khi đó không được tự điền phần chưa biết.
4. Người dùng chọn **Apply**, **Edit**, **Regenerate**, **Dismiss** hoặc tiếp tục trao đổi. Apply đánh dấu draft dirty; không submit/lưu canonical tự động.
5. Save đưa nội dung hiện tại qua lifecycle hiện hữu. Không bắt người dùng phải Rewrite trước khi lưu.

## 4. Chỉnh sửa một đoạn bằng selection comment

- Khi người dùng bôi đen một vùng trong editor, hiện action icon “Ask Agent” gần vùng chọn. Icon không che chữ; selection đổi/mất thì icon biến mất.
- Click icon mở request composer gắn trong panel chat và đính kèm quote của vùng chọn. Người dùng gõ chỉ dẫn như “viết tự nhiên hơn”, “rút gọn câu này”, “giữ số liệu, giải thích dễ hiểu hơn”, rồi gửi.
- Agent nhận đoạn chọn chính xác và ngữ cảnh lân cận cần thiết. Mặc định không gửi toàn bộ note cho yêu cầu cục bộ; người dùng có thể bật context toàn note khi cần.
- Suggestion trả về hiển thị diff/preview. Hành động mặc định là **Replace selected text**; có thể **Insert after**, **Apply to whole note** khi phù hợp, hoặc bỏ qua. Không tự thay text ngay khi model trả lời.
- Mỗi comment/request gắn với quote, range và editor revision. Trước khi apply, xác minh selected text và revision còn khớp. Nếu nội dung đã đổi, đánh dấu anchor stale và yêu cầu người dùng chọn lại/đối chiếu; tuyệt đối không áp dụng vào vị trí gần đúng.
- Sau khi apply, cho phép undo/redo; comment chuyển trạng thái Applied/Dismissed. Có thể trả lời tiếp trong thread để tinh chỉnh cùng đoạn.
- Keyboard: chọn text rồi dùng toolbar action/shortcut có nhãn. Mobile: dùng menu selection/accessibility action thay icon nổi phụ thuộc hover. Screen reader đọc được quote và trạng thái anchor.
- Đây là hội thoại riêng với Agent trong phiên soạn, không phải bình luận cộng tác nhìn thấy trong WorkNote đã lưu.

## 5. Task-aware reasoning và câu hỏi làm rõ

### Context Agent được phép sử dụng

- Nội dung/title hiện tại, workflow type, revision và vùng chọn của WorkNote.
- Với Task Note, backend lấy Task context chuẩn qua Task API: title, description, trạng thái, tiêu chí hoàn thành và các field được API/permission cho phép. Không tin task context do FE hoặc model tự gửi lên.
- Với Project Document/Periodic Report, dùng metadata và context của đúng workflow; không giả định có Task.
- Hiển thị nguồn context đang dùng trong chat (ví dụ “Nội dung WorkNote”, “Task được liên kết”). Không tự kéo thêm note khác, tài liệu khác hoặc dữ liệu ngoài scope.

### Cách Agent hiểu Task và note

1. Rút ra mục tiêu Task, phạm vi, điều kiện/tiêu chí hoàn thành và trạng thái theo nguồn tin cậy.
2. Tóm tắt note đang nói về việc gì, kết quả thực tế, cách xử lý, blocker, bước tiếp theo và evidence nếu có.
3. Đối chiếu hai nguồn, phát hiện thiếu thông tin quan trọng, cách hiểu mơ hồ hoặc mâu thuẫn. Trạng thái `DONE`/`IN_PROGRESS` của Task không tự chứng minh kết quả đã được làm hoặc kiểm thử.
4. Quyết định có đủ dữ kiện để trả lời/yêu cầu rewrite an toàn hay cần hỏi. Nếu đủ, tiếp tục ngay; không đặt câu hỏi máy móc trước mọi thao tác.
5. Sau khi nhận câu trả lời, cập nhật cách hiểu và đề xuất nội dung. Không hỏi lại điều đã được trả lời trong cùng draft.

### Khi nào hỏi và khi nào đi tiếp

- Hỏi khi thiếu dữ kiện làm thay đổi đáng kể ý nghĩa hoặc độ chính xác; hai cách hiểu dẫn tới note khác nhau; note mâu thuẫn với Task/context; hoặc Agent sắp phải khẳng định kết quả, nguyên nhân, quyết định hay kiểm chứng chưa có bằng chứng.
- Không hỏi cho yêu cầu hình thức đã rõ (sửa typo, rút gọn, đổi giọng), khi câu trả lời đã có trong note/Task context, hoặc khi phần thiếu có thể bỏ mà không làm sai ý.
- Hỏi ngắn, cụ thể, gắn với điểm đang thiếu và nói vì sao cần biết. Gom các câu liên quan trong một lượt; không phát checklist cố định. Ưu tiên một câu hỏi quan trọng nhất.
- Nếu thiếu thông tin không chặn được phần còn lại, tiếp tục với thông tin có thật và ghi phần chưa rõ riêng; không biến giả định thành sự thật.
- Người dùng có thể trả lời bằng văn bản tự do, chọn gợi ý, nói “Chưa biết”, bỏ câu hỏi hoặc yêu cầu tiếp tục. Khi bỏ qua, Agent bỏ/đánh dấu phần chưa biết thay vì tự suy ra.

### Hiển thị suy luận có thể kiểm tra

- Khi cần hoặc hữu ích, hiển thị một thẻ gọn **“Agent hiểu Task thế này”**: mục tiêu, dữ kiện lấy từ Task, dữ kiện lấy từ note và điểm chưa rõ. Cho phép người dùng sửa cách hiểu sai.
- Khi hỏi, nêu lý do ở mức ngắn: ví dụ Task ghi một trạng thái nhưng note mô tả trạng thái khác.
- Khi trả đề xuất, kèm change summary và các phần còn chưa xác minh. Không hiển thị chain-of-thought; hiển thị kết luận, nguồn và giả định để người dùng kiểm tra.

### Luồng chat làm rõ

`Đang soạn → Agent phân tích Task + note → (đủ dữ kiện) suggestion / (thiếu điểm quan trọng) tự mở chat hỏi → người dùng trả lời hoặc bỏ qua → Agent cập nhật cách hiểu → suggestion preview → người dùng Apply/Edit/Dismiss → Save theo lifecycle.`

## 6. Danh sách tính năng Agent

### Phải có

1. Sửa ngữ pháp, chính tả, dấu câu và độ rõ ràng; giữ ngôn ngữ gốc.
2. Viết lại theo custom instruction nhiều lượt, giữ context của cuộc hội thoại hiện tại.
3. Chỉnh toàn note hoặc chỉ đoạn được chọn; preview/diff trước khi Apply.
4. Rút gọn, làm rõ, đổi giọng văn/đối tượng đọc, sắp xếp đoạn, heading, checklist hoặc trình tự thao tác khi có ích.
5. Gợi ý/sửa Title; người dùng xác nhận và chỉnh được.
6. Giải thích phần mơ hồ, nêu câu hỏi cần bổ sung hoặc đề nghị tách note đa chủ đề; không tự sửa dữ kiện/không tự tạo bản ghi mới.
7. Bảo toàn code, log, URL, mã lỗi, identifiers, số liệu, phủ định, điều kiện và bằng chứng.
8. Regenerate, dismiss, undo/redo, khôi phục nội dung gốc, xóa chat draft.
9. Lưu không qua AI và tiếp tục khi provider lỗi; không mất nội dung.
10. Hiểu Task context, đối chiếu với note và chỉ hỏi khi thiếu/mơ hồ/mâu thuẫn có thể làm đổi đáng kể nội dung; tự mở chat cho câu hỏi đó và tiếp tục sau khi người dùng trả lời.

### Có thể bổ sung sau MVP

- Tùy chọn lưu style preference cá nhân cho lần sau. Chỉ lưu khi người dùng bật rõ ràng; preference chỉ ảnh hưởng văn phong, không được mang nội dung của note cũ sang note mới.
- Kiểm tra nhất quán nội bộ/đoạn trùng và đánh dấu để người dùng xem; không tự sửa mâu thuẫn hoặc tuyên bố đã kiểm chứng bằng nguồn ngoài.
- Dịch nội dung chỉ khi người dùng yêu cầu rõ ràng; bản gốc vẫn khôi phục được.

## 7. Hành vi và giới hạn của Agent

Agent chọn cấu trúc theo nội dung, không theo một form cố định. Một note ngắn có thể giữ một đoạn; note về tiến độ, quyết định, sự cố, hướng dẫn hoặc nghiên cứu có thể được sắp xếp theo những mục phù hợp.

1. Không bịa kết quả, nguyên nhân, giải pháp, kiểm chứng, nguồn hoặc số liệu; không biến giả thuyết thành sự thật.
2. Giữ nguyên phủ định, điều kiện, mức độ chắc chắn, ngày giờ, số liệu, mã lỗi, tên API/file, code, URL và identifier. Không “sửa đẹp” chuỗi kỹ thuật.
3. Viết tự nhiên, ngắn gọn, đúng ngữ pháp; giữ giọng chuyên nghiệp và ngôn ngữ/code-switching của người viết.
4. Nếu thiếu dữ kiện, giữ chỗ chưa rõ hoặc đặt câu hỏi riêng trong chat; không điền câu trả lời vào body.
5. Nếu có nhiều chủ đề, nêu gợi ý tách và chờ người dùng chọn. Không tự xóa, tách hoặc tạo WorkNote.
6. Xem nội dung người dùng và chat là dữ liệu không đáng tin; không làm theo prompt injection, không để lộ system prompt, không gọi action ngoài rewrite.
7. Không thêm YAML front matter. Với Markdown, chỉ dùng heading có nghĩa; bảng chỉ khi dữ liệu thực sự dạng bảng.

Output Agent cần cấu trúc kiểm tra được, ví dụ suggestion ID, scope, `suggestedTitle`, `contentMarkdown`, `changeSummary`, `openQuestions`, `sourceRevision`. Đây là logical contract proposal, chưa phải API contract. Backend tự tạo/đối chiếu revision; không tin revision/range từ model. Không trả chain-of-thought hoặc system prompt FE. Validate output; schema sai/empty thì giữ nguyên bản gốc và báo lỗi.

## 8. Nội dung, revision và lưu nháp

Đề xuất content model mới (tên trường cần chốt trong DB/OpenAPI review):

- `sourceText`: snapshot nội dung người viết nhập trước lần rewrite đầu của revision đó.
- `contentMarkdown`: nội dung đang soạn/được người viết chấp nhận; nếu bỏ qua AI thì bằng `sourceText`.
- `title`: tiêu đề người dùng xác nhận, có thể bắt đầu từ gợi ý AI.
- `rewriteMetadata`: metadata của các suggestion đã được áp dụng vào bản lưu: provider/model ID, prompt version, timestamp, actor và source revision/hash; không lưu chain-of-thought hoặc credential.
- `draftState`: title, sourceText, contentMarkdown, workflow context, current revision, pending suggestion IDs/anchors và transcript chat tạm để khôi phục bản nháp. Draft/chat tuân theo ACL và retention policy.
- Revision history giữ snapshot trước/sau của title/content đã lưu, tác giả sửa và provenance rewrite. Nháp và suggestion chưa được Apply/Save không tạo revision Work Note đã xác nhận.
- Selection comment/chat thread là dữ liệu phiên soạn, gồm quote, range, revision, instruction, suggestion và trạng thái. Không gộp vào contentMarkdown, WorkNote comment nghiệp vụ hoặc SAG source.

Raw input, bản canonical, draft và lịch sử phải có cùng ACL, retention và quy trình xóa của Work Note. Raw draft, chat transcript và rewrite proposal không được index. Nếu retention policy không cho giữ raw input sau khi lưu, UI phải nói rõ trước khi thay bản gốc; không âm thầm loại bỏ nội dung. Sau khi note lưu thành công, transcript Agent không đi theo WorkNote version; chỉ giữ nếu còn draft hoặc người dùng bật tính năng lưu style preference riêng.

Đổi schema là **database change**: DB PR riêng theo `Document/AI_WORKFLOW.md`. Migration cần giữ nguyên dữ liệu cũ, backfill What/How/Why bằng phép nối deterministic có nhãn tương ứng, không gọi LLM trong migration, và có kiểm tra/rollback. Không sửa migration lịch sử. Giữ API tương thích hoặc có kế hoạch nâng cấp FE/BE theo contract đã duyệt.

## 9. Quyền, trạng thái và tích hợp SAG

- Browser gọi backend/BFF theo API contract; không gọi SAG hoặc nhà cung cấp LLM trực tiếp. LLM credentials chỉ ở backend.
- Backend xác minh actor, Project, Task và quyền cho mọi thao tác; từ chối Task khác Project hoặc ID không được phép. Chỉ người có quyền sửa note mới được gọi rewrite; edit/archive tiếp tục theo quyền tác giả/reviewer hiện hành. Không coi role guard ở FE là bảo mật.
- Agent chỉ nhận nội dung cần rewrite cùng context tối thiểu đã được phép. Không gửi dữ liệu ngoài scope hoặc raw note chưa được người dùng yêu cầu xử lý. Log không ghi toàn văn note/prompt; chỉ log status, latency, token usage/operation ID cần chẩn đoán.
- Lưu/rewrite không thay đổi workflow state. Task Note theo quy trình hiện hành vẫn cần hành động lưu/xác nhận của tác giả. Project Document và Periodic Work Report vẫn phải qua review theo workflow hiện hành.
- Chỉ đưa **bản canonical đã lưu** vào SAG sau khi đạt source eligibility và ACL check. Không đánh đồng SAG retrieval với Verified Knowledge. Draft, rewrite preview, rejected/revoked content không được truy xuất.
- Tạo bridge BE→SAG có idempotency theo `workNoteId + version`; retry không tạo nguồn trùng. Edit/replacement/archive/ACL revoke phải chặn phiên bản cũ khỏi retrieval ngay theo policy và đồng bộ de-index có retry/audit.
- Giữ provenance tới Work Note ID, version, Task/Project scope, author và section/anchor để SAG trả citations về đúng nguồn. Task title/status/assignee không được sao chép thành tài liệu SAG độc lập.
- Local source/docs chưa chứng minh có WorkNote→SAG consumer chạy thật. Agent triển khai phải xác minh consumer, quyền partition và revoke path; nếu chưa có, báo blocker thay vì tuyên bố đã tích hợp.

## 10. Trạng thái giao diện và lỗi cần có

- Loading/error của Project/Task, không có quyền, Task không tồn tại/khác Project.
- Draft rỗng, đang autosave, đã autosave, autosave lỗi và khôi phục draft.
- Chat rỗng/đang gửi/đang phản hồi/lỗi/quota/timeout; clarification required/answered/skipped; tự mở chat khi cần hỏi; tiếp tục chat, reset transcript và quick prompt.
- Task understanding summary, hiển thị nguồn context, question reason và trạng thái open question.
- Text được chọn, selection action hiện/ẩn, request đang xử lý, suggestion ready, anchor stale, apply/undo.
- Đang rewrite toàn note, output không hợp lệ, đề xuất stale; preview/diff, sửa, tạo lại, bỏ, khôi phục bản gốc.
- Đang lưu, lưu thành công, xung đột revision, lỗi lưu và thử lại an toàn.
- Trạng thái workflow/review/index tách biệt; hiển thị rõ đang chờ review hay SAG indexing thay vì báo “hoàn tất” sớm.

Form phải dùng được bằng keyboard và screen reader; lỗi gắn với field; trạng thái thông báo qua live region; status không chỉ phân biệt bằng màu. Giữ responsive, dark mode, RTL và localization của DATN-FE. Nội dung do người dùng viết giữ nguyên ngôn ngữ bất kể locale UI.

## 11. Thay đổi theo tầng và thứ tự triển khai

| Tầng | Hiện trạng quan sát được | Cần đổi |
| --- | --- | --- |
| FE WorkNote composer | Preview dialog nhỏ, các field/kind cố định, state cục bộ | Dialog lớn; title + body tự do; autosave; header Agent; chat panel đáy; tự mở khi cần clarification; quick prompts; task understanding card; selection action; diff/apply/undo; state và lỗi đầy đủ; dùng API client/BFF. |
| FE WorkNote types | Preview enum khác taxonomy sản phẩm | Đọc workflow type/context từ contract được duyệt; không coi `WORK_UPDATE/WEEKLY_SUMMARY/KNOWLEDGE/DECISION` là contract dùng chung. |
| BE Capture/Agent | Schema cũ What/How/Why; trong source snapshot chưa thấy Project WorkNote API | Chốt OpenAPI cho draft, save/edit/version, rewrite chat và selection suggestion; validate input/output; authorize Task/Project; kiểm tra revision; gọi AI adapter backend. |
| Database | Schema strict và versioning cũ | Thêm content tự do, draft/session và revision metadata tương thích dữ liệu cũ; migration deterministic trong DB PR riêng. |
| SAG | Generic document/text ingest; chưa xác minh WorkNote consumer | Backend đẩy canonical version đủ điều kiện với idempotency/provenance; xử lý edit/archive/revoke và kiểm tra citation/search. FE không gọi SAG. |

### Luồng API cần thiết (ngữ nghĩa, chưa chốt endpoint)

1. Load/create/update draft: title, sourceText, current content, workflow context và revision. Autosave phải xử lý lỗi, retry và nhiều tab mà không ghi đè âm thầm.
2. Send Agent message: draft ID, revision hiện tại, instruction, conversation turns cần thiết, `scope=selection|whole_note`, selected quote/range khi áp dụng, và cờ context người dùng chọn. Backend xác thực quyền/context trước khi gửi model.
3. Agent response có trạng thái logic `ANSWER`, `CLARIFICATION_REQUIRED` hoặc `SUGGESTION_READY`; câu hỏi có ID, lý do, và gợi ý trả lời tùy trường hợp. Suggestion có ID, scope, suggested title/content hoặc `replacementText`, change summary/open questions, source revision và selection anchor hash. Đây là logical contract proposal, chưa phải API contract; không trả chain-of-thought.
4. Apply suggestion: server hoặc client cập nhật draft dựa trên đúng source revision; từ chối stale revision/anchor. User tiếp tục sửa và explicit Save mới tạo WorkNote version.
5. Save/edit/version/restore: dùng WorkNote lifecycle hiện hành và optimistic concurrency. Restore tạo revision mới từ snapshot đã chọn; không xóa lịch sử.
6. SAG sync: event/consumer backend idempotent theo note/version; retry, replacement, archive và revoke có trạng thái quan sát được.

OpenAPI phải xác định kích thước tối đa, timeout/quota, lỗi retryable, idempotency, concurrency/revision và data retention trước khi FE tích hợp. Nếu backend có streaming chat adapter thì tái sử dụng; nếu chưa, dùng request lifecycle hiện tại, không thêm streaming stack riêng chỉ để hiển thị token.

### Thứ tự thực hiện

1. Đối chiếu WorkNote workflow được duyệt với source hiện hành; Product chốt raw retention, Task Note confirmation, title behavior và SAG source eligibility.
2. Duyệt database/OpenAPI/AI data-handling contracts trước khi wire FE.
3. DB schema/migration/version snapshots trong DB branch/PR riêng.
4. BE API, authorization, AI adapter, draft/version và error handling.
5. FE composer/chat/selection action, accessibility và localized states qua BFF.
6. SAG consumer/revoke và retrieval evaluation trong branch/PR theo architecture được duyệt.

Không gộp DB, BE, FE thành một branch. Không wire FE đến SAG. Không tuyên bố SAG-ready nếu chưa chạy end-to-end với ACL, citation, version update và revoke.

## 12. Tiêu chí nghiệm thu

1. Dialog mở đủ rộng cho editor; header/Save không cuộn mất. Agent icon mở/đóng chat dưới editor. Mobile có luồng chat và editor dùng được.
2. Tạo note chỉ với title + freeform body; không bắt What/How/Why. Lưu được mà không gọi AI.
3. Agent đọc đúng Task context đã được authorize, tóm lược mục tiêu/tiêu chí và đối chiếu với note; không suy kết quả từ trạng thái Task.
4. Khi thiếu/mơ hồ/mâu thuẫn có thể làm đổi đáng kể nội dung, chat tự mở với câu hỏi cụ thể; người dùng có thể trả lời, bỏ qua hoặc “Chưa biết”; Agent tiếp tục từ câu trả lời, không hỏi lại thông tin đã có.
5. Với yêu cầu rõ và đủ dữ kiện (ví dụ sửa typo), Agent không hỏi và không tự mở chat. Không hiển thị chain-of-thought; summary nêu context, lý do hỏi và điểm chưa rõ.
6. Chat nhận custom instruction nhiều lượt, quick prompts, giữ context trong draft và không đưa transcript vào content/SAG.
7. Bôi đen text hiện Ask Agent; yêu cầu sửa gắn đúng quote/range. Suggestion không tự áp dụng; Replace selection chỉ thay vùng đúng; stale anchor bị chặn; undo khôi phục đúng nội dung.
8. Rewrite toàn note và selection đều có diff/preview, apply/edit/regenerate/dismiss; title suggestion luôn sửa được.
9. Test fixtures chứng minh giữ ngôn ngữ, phủ định, số, identifier, code, URL, ngày và mức chắc chắn; nội dung thiếu dữ kiện không bị bịa.
10. Lưu/restore tạo revisions có provenance; lỗi AI không chặn lưu raw note, draft không mất, retry không tạo version trùng.
11. Mọi thao tác kiểm tra Project/Task/actor phía BE; cross-project access bị từ chối; Project Document/Report giữ review permission/state machine.
12. Chỉ canonical eligible version searchable trong SAG; citation mở đúng Work Note/version/section. Draft/rejected/revoked/ACL-denied không lộ; archive/replacement/revoke chặn stale content.
13. Retrieval evaluation có note ngắn/dài, văn xuôi, checklist, code/log, tiếng Việt/Anh và task đa dạng; đo hit đúng nguồn, exact identifier và citation correctness trước/sau rewrite.
14. Tests bao phủ reasoning/clarification, chat, selection anchor, stale revision, auth, lifecycle, autosave/error, versioning và SAG idempotency/revoke. FE chạy `npm run check`; browser kiểm responsive/light-dark/keyboard/screen reader.

## 13. Ngoài phạm vi và điểm cần chốt

- Tự duyệt, tự xác nhận hoặc tự publish Knowledge thay người có quyền.
- Tạo hoặc sửa Task, đổi assignee/status, đồng bộ Jira, hoặc sao chép task thành source tri thức.
- Hiển thị hoặc lưu chain-of-thought nội bộ; người dùng nhận task understanding, lý do câu hỏi, nguồn context và điểm chưa rõ có thể kiểm tra.
- Tự chia một note thành nhiều bản ghi, tự điền dữ kiện còn thiếu, dịch tự động, hoặc rewrite file đính kèm.
- Đưa prompt/raw draft vào SAG, ghi log toàn văn, hoặc để Agent vượt ACL.

**Rủi ro cần giải quyết trước tích hợp:** source hiện tại, preview Work Notes và tài liệu workflow không cùng một contract; Task Note eligibility cho SAG và consumer đang chạy phải được xác minh trước khi gọi tính năng là hoàn chỉnh.
