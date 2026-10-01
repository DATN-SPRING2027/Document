# Operating Model Research

**Trạng thái:** Draft; mô hình dưới đây là cách nghiên cứu vận hành, không phải quy trình đã được phê duyệt.

## Bối cảnh hiện hành

- `[DOCUMENTED]` Continuum được mô tả nhằm duy trì tri thức dự án phần mềm qua capture, ingestion/retrieval, đề xuất knowledge có evidence, human review, gap monitoring và handover. Xem `product_docs/research-docs/01_MVP_SCOPE.md` và `03_DAILY_WORKFLOW_AND_JIRA_SYNC.md`.
- `[DOCUMENTED]` Jira là nguồn task context cho MVP; capture/Work Note được người dùng xác nhận và không bị thay bằng dữ liệu issue một cách ngầm định.
- `[UNKNOWN]` Operating model thực tế của tổ chức (cách lập kế hoạch, phân bổ việc, review, quản lý thay đổi, weekly reporting và quyết định) chưa được chứng minh bằng telemetry hay phỏng vấn trong repo.

## Các luồng vận hành cần quan sát

| Luồng | Mô tả nghiên cứu | Evidence cần thu thập | Rủi ro khi thiết kế hệ thống trước khi hiểu luồng |
|---|---|---|---|
| Plan work | Mục tiêu/issue được tạo, phân rã, gán owner, định hạn | Ai được tạo, hierarchy thật, nơi duyệt, quy tắc ưu tiên | Tạo duplicate task SoT hoặc ép team vào workflow sai |
| Execute and report | Member cập nhật tiến độ/blocker; leader điều phối | Trạng thái có nghĩa gì, tần suất, cách escalation | Dashboard phản ánh dữ liệu stale hoặc thúc đẩy báo cáo kép |
| Capture learning | Người làm ghi lại quyết định/lesson/context theo task | Thời điểm, định dạng, ai xác nhận, evidence | Capture quá nặng làm giảm adoption |
| Verify/publish knowledge | SME/owner xem xét đề xuất và kiểm tra nguồn | Vai trò, trạng thái, version, quyền truy cập | AI proposal bị hiểu nhầm là fact đã xác minh |
| Handover | Người rời/đổi nhiệm vụ bàn giao context cho successor | Trigger, package, owner, readiness, xác nhận | Checklist không phù hợp quy trình hoặc rò rỉ dữ liệu |
| Management review | Leader tìm blocker/risk/gap để quyết định | Câu hỏi quyết định, độ sâu drill-down, freshness, audience | “Dashboard” chung chung, visibility vượt quá need-to-know |

## Candidate operating loop (không phải requirement)

`[PROPOSAL]` Work/task được giữ ở hệ thống SoT được xác nhận → con người liên kết/capture kinh nghiệm và bằng chứng → hệ thống tạo knowledge proposal có nguồn → người có thẩm quyền xác minh → tri thức được dùng trong tìm kiếm/handover → gap hoặc blocker được đưa đến người có trách nhiệm → kết quả/điều chỉnh được phản ánh lại đúng source.

Loop này tương thích về ý tưởng với Continuum MVP đã ghi nhận; phần bổ sung toàn tổ chức/Department/management layer vẫn là hypothesis mới, không được gộp vào current scope.

## Operating-model questions

1. Ai là người chịu trách nhiệm tạo, cập nhật và đóng task? Nơi nào là canonical?
2. “Done” là hoàn tất deliverable, được review, hay đã có knowledge evidence?
3. Những gì cần ghi lại ngoài task? Ai xác nhận sự thật và nguồn?
4. Khi owner rời team, ai nhận trách nhiệm và ai chấp thuận handover?
5. Ai được phép xem work/knowledge theo project/team? Có confidential class nào không?
6. Reporting nào đang làm thủ công? Bao lâu, ai dùng, quyết định gì dựa trên report?
7. Bất đồng giữa Jira, tài liệu, code/PR và knowledge được xử lý ở đâu?

## Friction diagnosis protocol

`[PROPOSAL]` Ghi từng incident thành: actor → mục tiêu → thao tác hiện tại → system(s) → wait/rework/context switches → workaround → tác động → root cause category. Phân biệt lỗi do capability, plan, configuration, process, thiếu ownership/data quality hay connector.

Đo baseline tối thiểu: thời gian hoàn thành tác vụ mẫu; số lần mở/chuyển hệ thống; số trường hợp thiếu owner/evidence; sync lag/error/reconciliation; thời gian người mới trả lời câu hỏi handover. Đặt target sau khi baseline và decision owner được thống nhất.

## Nguồn DATN

- `product_docs/research-docs/01_MVP_SCOPE.md`
- `product_docs/research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md`
- `product_docs/research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md`
- `product_docs/research-docs/Workspace/00-workspace-research-review-v2.md`
