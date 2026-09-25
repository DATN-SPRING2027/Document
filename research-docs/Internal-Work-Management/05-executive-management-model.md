# Executive and Management Model Research

**Trạng thái:** Hypothesis research; không đưa Director/Department Manager vào role model hay approved MVP.

## Câu hỏi quản trị trước câu hỏi dashboard

“Executive view” chỉ có ích nếu nêu được quyết định mà người xem phải đưa ra. `[UNKNOWN]` Repo hiện không ghi rõ DATN có director/department manager persona, quyết định định kỳ, reporting cadence, hay toàn quyền xem dữ liệu. Continuum role docs nêu ADMIN, TEAM_LEADER, MEMBER; không có executive role. ADMIN không đồng nghĩa với quyền đọc toàn bộ nội dung.

## Candidate decision questions

| Câu hỏi có thể cần trả lời | Dữ liệu tối thiểu có thể cần | Ai được thấy? | Evidence / trạng thái |
|---|---|---|---|
| Dự án/team nào đang bị block và cần escalation? | Status, blocker, owner, age, last updated, project/team | `[UNKNOWN]` | Chưa có persona/use case cụ thể |
| Có deadline/dependency risk nào? | Due date, dependency, confidence, source freshness | `[UNKNOWN]` | Không tự coi overdue report là requirement |
| Có quyết định chờ owner/approval? | Decision record, approver, due, evidence, state | `[UNKNOWN]` | Candidate concept trong brief |
| Có knowledge gap/handover risk? | Critical topic, verified source, ownership, successor state | Continuum scoped ACL | Handover/gap monitoring đã documented cho Continuum; enterprise roll-up chưa |
| Capacity/portfolio allocation ra sao? | Plan, estimates, capacity, cross-project dependencies | `[UNKNOWN]` | Jira Premium/portfolio products may offer related capability |

## Drill-down model to study

`[PROPOSAL]` Nếu xác nhận management use case: bắt đầu từ câu hỏi/roll-up aggregate → filter org scope → Department/Team/Project only if domain approved → work/task/decision/knowledge evidence with per-item access checks. Không để quyền xem aggregate tự động cấp quyền mở nội dung nguồn.

Mỗi metric cần định nghĩa owner, formula, source, refresh/latency, missing-data handling, access, audit, drill-down behavior và action sau khi phát hiện. “Status màu xanh/vàng/đỏ” không có nghĩa nếu không có rule và freshness.

## Security/governance implications

- `[DOCUMENTED]` Backend là enforcement authority; frontend gating chỉ là UX. Permission-aware knowledge retrieval phải lọc trước khi đưa context vào LLM (xem accepted role research và Continuum docs).
- `[INFERENCE]` Aggregates có thể tiết lộ dữ liệu nhạy cảm ngay cả khi chi tiết bị ẩn; cần kiểm thử inference/aggregation leakage.
- `[DECISION REQUIRED]` Có executive role/group không; có org-wide metrics không; thông tin nào confidential; ai phê duyệt; audit nào bắt buộc.

## Jira comparison evidence

`[WEB RESEARCH]` Jira có dashboard/reporting và Jira Premium Plans/Advanced Roadmaps hỗ trợ multi-team/project planning; Atlassian cũng định vị Jira Align cho enterprise strategy/portfolio. Điều này không chứng minh có đúng một “director view” cần thiết cho DATN. Nguồn: [Jira pricing](https://www.atlassian.com/software/jira/pricing), [Advanced Roadmaps](https://support.atlassian.com/jira-software-cloud/docs/what-is-advanced-roadmaps/), [Jira Align](https://www.atlassian.com/software/jira-align).

## Candidate measures (không có target tự đặt)

- Thời gian trả lời bộ câu hỏi quản lý chuẩn.
- Tỷ lệ con số có nguồn/owner/timestamp rõ.
- Số trường hợp dữ liệu stale hoặc không drill-down được do thiếu permission.
- Thời gian từ blocker được báo tới người có thể hành động.
- Unauthorized disclosure trong test = zero như security guardrail, không phải metric productivity.

Baseline, cohort, window và threshold cần do product/leader xác nhận. Không dùng dashboard để chấm điểm năng suất cá nhân nếu không có quyết định/đạo đức/chính sách rõ.
