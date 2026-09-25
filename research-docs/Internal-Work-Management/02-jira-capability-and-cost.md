# Jira Capability, Plan Boundaries and Cost Model

**Trạng thái:** Draft research; không đánh giá Jira theo cảm nhận và không khuyến nghị mua/bỏ plan.  
**Web evidence checked:** 2026-09-25. Giá/plan thay đổi; cần xác nhận lại bằng Atlassian Cloud Pricing Calculator và billing site trước quyết định.

## Phân biệt loại bằng chứng

- `[JIRA CAPABILITY]`: chức năng sản phẩm được mô tả chính thức.
- `[JIRA CONFIGURATION]`: chức năng có thể phụ thuộc project scheme, hierarchy, permission, dashboard, automation hoặc tích hợp.
- `[JIRA PLAN LIMIT]`: khác biệt do Free/Standard/Premium/Enterprise.
- `[JIRA ECOSYSTEM]`: cần sản phẩm Atlassian khác hoặc app Marketplace.
- `[UNKNOWN]`: không thể biết trạng thái tenant DATN chỉ từ public docs.

## Plan snapshot

| Plan | Publicly described limits/capabilities có liên quan | Ý nghĩa cho hypothesis | DATN hiện dùng? |
|---|---|---|---|
| Free | Tối đa 10 users; 2 GB storage; 100 automation rule runs/month; basic planning/dependencies. Một số controls/advanced features giới hạn hơn plan trả phí. | Có thể là $0 cho nhóm nhỏ nếu capability đủ; giới hạn quyền/audit/automation có thể làm plan này không đáp ứng yêu cầu. | `[UNKNOWN]` |
| Standard | Role/permission controls mở rộng, audit logs/issue security, 250 GB storage; mức automation cao hơn Free; Rovo credits theo pricing page. | Có thể đáp ứng nhu cầu permissions và audit mà Free không đáp ứng; không được mặc định phải trả Premium. | `[UNKNOWN]` |
| Premium | Advanced Roadmaps/Plans cho nhiều team/project, planning/capacity/dependencies nâng cao; unlimited storage; automation pool theo user; SLA theo terms công bố. | Cross-team planning không đồng nghĩa phải thay Jira; một số use case có plan gate. | `[UNKNOWN]` |
| Enterprise | Nhiều site, Atlassian Analytics/Data Lake/cross-product reporting và governance mức enterprise theo plan page. | Có thể quá mức cho cohort đồ án; cần định nghĩa nhu cầu thực và giá quote. | `[UNKNOWN]` |

Các giới hạn cụ thể có thể thay đổi theo sản phẩm, rollout, site và thời điểm; bảng này là orientation, không thay thế quote hoặc tenant inspection. Nguồn chính: [Jira Pricing](https://www.atlassian.com/software/jira/pricing), [Jira editions guide](https://www.atlassian.com/software/jira/guides/more/jira-editions).

## Năng lực Jira và hệ sinh thái

| Nhu cầu | Evidence public | Phân loại | Caveat |
|---|---|---|---|
| Team/project planning liên quan nhiều project | Jira Premium Plans/Advanced Roadmaps cung cấp planning view đa team/project. [Official guide](https://support.atlassian.com/jira-software-cloud/docs/what-is-advanced-roadmaps/) | `[JIRA CAPABILITY]` + `[JIRA PLAN LIMIT]` | Cần kiểm tra plan, product configuration, hierarchy và data quality của tenant. |
| Permission scopes | Jira có global, project và issue permission categories. [Types of permissions](https://support.atlassian.com/jira-cloud-administration/docs/types-of-permissions-in-jira/) | `[JIRA CAPABILITY]` + `[JIRA CONFIGURATION]` | Không chứng minh policy DATN đã được cấu hình đúng; app/plan có thể ảnh hưởng. |
| Dashboard/reporting | Jira có dashboard/reporting features, nâng cao portfolio reporting có thể thuộc Premium/Enterprise hoặc product khác. [Pricing](https://www.atlassian.com/software/jira/pricing) | `[JIRA CAPABILITY]` / `[JIRA PLAN LIMIT]` | Cần xác định câu hỏi quyết định và khả năng phân quyền dữ liệu khi drill-down. |
| Knowledge liên kết work | Confluence tích hợp Jira bằng link/embed/Smart Links. [Jira + Confluence](https://www.atlassian.com/software/confluence/jira-integration), [Smart Links](https://support.atlassian.com/platform-experiences/docs/use-smart-links-to-collaborate-across-products/) | `[JIRA ECOSYSTEM]` | Có thể cải thiện liên kết, nhưng là subscription/product/data source khác; không tự động hợp nhất SoT. |
| Enterprise strategy/portfolio | Jira Align được mô tả cho enterprise strategy/portfolio. [Jira Align](https://www.atlassian.com/software/jira-align) | `[JIRA ECOSYSTEM]` | Không phải mặc định dành cho DATN; giá/fit cần xác minh riêng. |
| Automation/API/integrations | Jira Cloud có API và integration ecosystem; feature/quotas tùy plan/app. [Jira developer docs](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) | `[JIRA CAPABILITY]` | Cần thử với use case, auth, rate limits, webhook delivery và quyền thật. |
| Department entity | Không thấy evidence public được kiểm tra đủ để khẳng định Jira có/không có native DATN Department business entity. | `[UNKNOWN]` | Có thể biểu diễn một số grouping bằng project/team/field/configuration; đây không đồng nhất với domain Department. |

## Seat pricing: ví dụ minh họa, không phải báo giá DATN

Atlassian cloud pricing per product/user, với monthly billing có thể dùng Maximum Quantity Billing: billable count có thể căn cứ mức seat cao nhất trong kỳ và gỡ seat giữa kỳ không làm giảm hóa đơn kỳ đó. Xem [Cloud Pricing & Licensing](https://www.atlassian.com/licensing/cloud). Mỗi sản phẩm (ví dụ Jira và Confluence) được tính riêng; Marketplace apps/Guard có thể phát sinh thêm.

Để minh họa độ nhạy, dùng **$8.60/user/month** làm đơn giá Standard ở tier đầu tiên được nêu trong ví dụ bảng giá cloud công khai; đây là phép nhân giả định, USD, trước thuế/discount, không phải quote hay giá được xác nhận cho tenant:

| Paid Standard users | Ước tính/tháng | Ước tính/năm (12×) |
|---:|---:|---:|
| 10 | $86.00 | $1,032.00 |
| 11 | $94.60 | $1,135.20 |
| 20 | $172.00 | $2,064.00 |
| 30 | $258.00 | $3,096.00 |
| 50 | $430.00 | $5,160.00 |
| 100 | $860.00 | $10,320.00 |

Free có thể là $0 cho tối đa 10 users nếu các giới hạn chấp nhận được. Nhóm 10 người vẫn có thể cần Standard nếu cần controls/audit ở plan trả phí. Premium/Enterprise, annual discounts, FX, tax, eligible academic/community discounts và quote thực tế chưa tính; cần calculator/tenant invoice. Không dùng bảng này để kết luận build tiết kiệm hơn.

## TCO so sánh

- **SaaS:** `Σ subscription (Jira + Confluence + apps/Guard) + admin hours × loaded rate + onboarding/migration + operating overhead`.
- **Internal build:** `discovery/build person-months × loaded cost + hosting/storage/LLM + backups/monitoring/security/support + maintenance labor + onboarding/migration`.
- **Hybrid:** `SaaS + connector development/monitoring/reconciliation/ACL sync + internal knowledge-layer operating cost`.

Không có break-even nếu thiếu: user/seat counts, billable products, invoice, staffing/cost rates, time horizon, workload, reliability/security requirements và migration scope.

## Kết luận có giới hạn

- `[WEB RESEARCH]` Có thể sai khi nói “Jira không làm được cross-team”; Premium có Plans/Advanced Roadmaps.
- `[INFERENCE]` Một số pain có thể là plan/configuration/operating-model, không hẳn product limitation.
- `[UNKNOWN]` Chưa biết Jira có đủ cho DATN vì chưa xem tenant, workflows, permissions, data, invoices và phỏng vấn.
- `[DECISION REQUIRED]` Chọn plan, thêm Confluence/Guard/Jira Align, hoặc rời Jira phải do chủ sở hữu quyết định sau TCO/use-case validation.
