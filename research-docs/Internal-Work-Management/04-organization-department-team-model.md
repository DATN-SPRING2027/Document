# Organization, Department and Team Model

**Trạng thái:** Domain-model research hypothesis; không xác nhận cardinality hay tạo requirement.

## Evidence hiện hành

- `[DOCUMENTED]` Continuum MVP hiện tại giới hạn ở một software project có nhiều team; roles được nêu là ADMIN, TEAM_LEADER, MEMBER. SME, KNOWLEDGE_OWNER, SUCCESSOR là assignment theo scope, không phải persistent global role. Nguồn: `product_docs/research-docs/01_MVP_SCOPE.md`, `02_ACTORS_ROLES_AND_PERMISSIONS.md`.
- `[DOCUMENTED]` Architecture/Workspace research thảo luận Organization, Project, Team và membership. Các decision/spec xác định runtime/persistence, không tự định nghĩa enterprise org chart.
- `[FACT]` Workspace research review hiện ghi nhận các schema một phần nhưng không có Project/Team CRUD end-to-end, guard/authz hoàn chỉnh hoặc FE product flows. Schema/scaffold không chứng minh nghiệp vụ đã chạy.
- `[UNKNOWN]` Repository chưa chứng minh Department là entity sản phẩm; cũng chưa chốt quan hệ Department↔Team↔Project hay số lượng thực tế.

## Candidate model để kiểm chứng

```text
Organization
├── User identities / memberships (scope chưa chốt)
├── Departments? (hypothesis)
│   └── Teams? (cardinality chưa chốt)
├── Projects (có thể cross-department? unknown)
│   ├── Project memberships
│   └── Team participation? (unknown)
└── Organization policies / grants (đã có architecture/documentation concept)
```

Sơ đồ là câu hỏi nghiên cứu, không phải schema target. Không được mặc định team chỉ thuộc một Department, Project chỉ thuộc một Department, hay User có đúng một team.

## Cardinality và policy questions

| Quan hệ | Các khả năng cần phân biệt | Điều gì thay đổi nếu chọn | Trạng thái |
|---|---|---|---|
| Organization ↔ Department | Một org có 0/1/n department; có org không phân phòng ban? | URL/context, authorization, reporting, migration | `[UNKNOWN]` |
| Department ↔ Team | Team thuộc đúng một department, nhiều department, hoặc không thuộc department | Ownership, cross-department view, team move, grants | `[DECISION REQUIRED]` |
| Department ↔ Project | Project thuộc một/many department hoặc portfolio-only grouping | Project access, roll-up, charge/ownership | `[DECISION REQUIRED]` |
| Project ↔ Team | Một project dùng nhiều teams; một team tham gia nhiều projects? | Membership, delivery ownership, permission intersection | `[UNKNOWN]` |
| User ↔ Organization | Một identity thuộc một/nhiều org? | Login, org context, data isolation | `[DECISION REQUIRED]` |
| User ↔ Team/Project | Membership trực tiếp, qua group/team, hay cả hai | Authorization and lifecycle consistency | `[DECISION REQUIRED]` |

## Actor/scope implications

- `[DOCUMENTED]` ADMIN không tự động có quyền đọc nội dung confidential; access được giới hạn theo membership/ACL và policy.
- `[DOCUMENTED]` TEAM_LEADER không mặc định có `project.create`; quyền đó cần explicit organization capability grant theo research hiện hành.
- `[INFERENCE]` Department manager/director role không thể thêm vào role matrix chỉ vì concept org chart xuất hiện trong hypothesis.
- `[DECISION REQUIRED]` Nếu cần org-wide view, xác định audience, fields/data classes, delegated access, drill-down enforcement, export/audit trước khi chọn role hoặc entity.

## Domain language checklist

Trước khi model: định nghĩa “organization” (legal entity, class/team workspace, tenant?); “department” (formal unit vs reporting label); “team” (stable membership vs project squad); “project” (bounded deliverable vs portfolio); “member” (identity vs active assignment). Tách persistent identity/role khỏi time-bound membership/assignment.

## Nguồn ngoài tham khảo cho model (không dùng làm requirement)

- Jira supports project/teams concepts and configurable planning; Jira Premium Plans is multi-team/project-oriented: [Atlassian Advanced Roadmaps](https://support.atlassian.com/jira-software-cloud/docs/what-is-advanced-roadmaps/).
- Các công cụ khác tổ chức hierarchy khác nhau; ví dụ [ClickUp hierarchy](https://help.clickup.com/hc/en-us/articles/13856392825367-Intro-to-the-Hierarchy) và [Azure DevOps teams/area paths](https://learn.microsoft.com/en-us/azure/devops/organizations/settings/about-teams-and-settings?view=azure-devops). Đây là mẫu sản phẩm so sánh, không chứng minh DATN cần cùng structure.

## Decision gate

`[PROPOSAL]` Chỉ xem xét Department entity/role khi interview và use cases chỉ ra cần lifecycle, membership, governance, access, reporting hoặc ownership mà không thể diễn đạt an toàn/hiểu được bằng scope hiện có. Người quyết định phải xác nhận cardinality, inheritance, cross-scope access và migration behavior.
