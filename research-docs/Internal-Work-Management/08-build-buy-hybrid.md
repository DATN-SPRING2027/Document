# Build vs Buy vs Hybrid Research

**Trạng thái:** Comparative analysis; current DATN task-source direction is recorded below. Cost, feature breadth and organization-wide product strategy remain open research questions.

## Options in scope

- **A — Continue Jira:** retain task system; resolve friction through workflow/configuration, plan, training or governance changes.
- **B — Jira + Confluence:** use Jira for work and Confluence for documented knowledge with product integration.
- **C — Internal replaces Jira:** internal product owns task lifecycle and potentially more work/knowledge domains.
- **D — Internal above Jira:** Jira remains task source; internal layer aggregates context, decisions/verified knowledge or management views.
- **E — Internal + multiple external systems:** integration layer connects Jira/GitHub/docs/chat/calendar and internal knowledge capabilities.

`[HISTORICAL FRAMING]` Earlier Continuum product documents described Option D (Jira task context + knowledge continuity). That framing is superseded for DATN task lifecycle by the decision below; it remains only as a market comparison, not the current product direction.

`[DECIDED — 2026-10-01]` For the DATN MVP, Continuum owns the internal task lifecycle; Jira is not the task source or an MVP sync dependency. This is a narrow product decision, not approval for full Jira parity or organization-wide migration. Options A, B and D remain comparative market scenarios only, not the selected task direction.

## Qualitative trade-off matrix

| Dimension | A Continue Jira | B Jira + Confluence | C Replace Jira | D Internal above Jira | E Multi-system internal layer |
|---|---|---|---|---|---|
| Subscription cost | Existing plan/app cost; can be $0 on eligible Free scope; actual DATN spend unknown | Adds separate Confluence seats/plan | May reduce SaaS seats only if fully migrated; not guaranteed | Retains Jira plus internal running cost | Retains some SaaS plus several connector/operating costs |
| Fit/flexibility | Configuration constrained by product/plan | Better doc/work linking; still Atlassian model | Maximum domain-specific control | Tailored context while reusing task lifecycle | Broadest integration control; broadest complexity |
| Time to usable workflow | Potentially shortest if setup exists | Low-to-medium setup, two products | Long; build full lifecycle and migrate | Medium; scope depends on precise use case | Longest/continuous operations likely |
| Maintenance/security | Vendor operation, tenant configuration/admin still required | Same plus knowledge product administration | DATN owns uptime, patching, backup, incident response | Own added layer plus SaaS dependency | Own connectors, identity/ACL mapping, data lifecycle |
| Governance | Jira project/issue/role controls, plan dependent | Cross-product permission design | Fully custom responsibility and risk | Must preserve source ACL and internal ACL | Complex multi-provider ACL equivalence problem |
| Knowledge | Issue context; Confluence adds content system | Stronger document link ecosystem | Can own knowledge but requires lifecycle/search quality | Continuum knowledge continuity aligns conceptually | Can connect diverse sources but content rights/ACL hard |
| Migration/lock-in | Low change | Moderate content/project coupling | High migration and user retraining | Lower if mostly links/read-only | Medium-high mapping/reconciliation |
| DATN MVP fit | Not the selected task direction | Not the selected task direction | Internal task lifecycle is selected; full Jira parity/migration is not implied | Not the selected task direction because Jira is not task source | Future hypothesis; broad scope unproven |

No column is universally superior. Scores are intentionally not assigned because there is no agreed use-case weighting or observed baseline.

## Cost model

Let:
- `U_j`, `U_c`, `U_other` = billable users by Jira, Confluence and other product;
- `P` = plan, billing cadence, currency, tax/discount and add-on selection;
- `A` = administration, support, onboarding, migration and governance effort;
- `B0` = one-time internal discovery/build labor;
- `Run` = hosting, storage, AI/LLM, backups, observability, security reviews and ongoing engineering/support;
- `Conn` = connector build, monitoring, reconciliation and ACL/identity operations.

`SaaS TCO = subscription(U,P) + A`  
`Internal TCO = B0 + Run + migration/onboarding`  
`Hybrid TCO = relevant SaaS TCO + internal layer + Conn`

Need common horizon (e.g., 12/24/36 months) and fully-loaded cost rate. Public list price alone is not TCO. A small team on Free may make SaaS spend $0; a feature requirement may push to Standard/Premium; neither proves build is cheaper.

## Product market examples (not recommendations)

| Product | Documented model to compare | Official reference |
|---|---|---|
| Jira | Issue/project work, plan-dependent planning/permissions/automation | [Jira pricing](https://www.atlassian.com/software/jira/pricing) |
| Confluence | Knowledge/docs linked to Jira | [Jira + Confluence](https://www.atlassian.com/software/confluence/jira-integration) |
| Linear | Teams, projects, initiatives, webhooks | [Teams](https://linear.app/docs/teams), [Projects](https://linear.app/docs/projects) |
| ClickUp | Workspace hierarchy, tasks/docs/dashboards/automation | [Hierarchy](https://help.clickup.com/hc/en-us/articles/13856392825367-Intro-to-the-Hierarchy) |
| Asana | Portfolios, dashboards, work coordination | [Portfolios](https://help.asana.com/s/article/monitor-initiatives-and-manage-resources-with-portfolios) |
| monday work management | Workspaces/boards/items/dashboards; tier-dependent portfolio | [Official overview](https://support.monday.com/hc/en-us/articles/115005305649-Get-started-with-monday-AI-work-platform) |
| Notion | Projects/tasks plus docs/database/API | [Projects and tasks](https://www.notion.com/en-gb/help/guides/getting-started-with-projects-and-tasks) |
| OpenProject | Projects/work packages/wiki | [Projects](https://www.openproject.org/docs/user-guide/projects/) |
| Plane | Workspace/projects/work items/pages/API/self-host options | [Docs](https://docs.plane.so/), [API](https://developers.plane.so/api-reference/introduction) |
| YouTrack | Projects/issues/agile/knowledge base | [Project overview](https://www.jetbrains.com/help/youtrack/cloud/project-overview.html) |
| Azure DevOps | Organization/projects/teams/area paths/work items/service hooks | [Teams and settings](https://learn.microsoft.com/en-us/azure/devops/organizations/settings/about-teams-and-settings?view=azure-devops) |

This is a feature-area scan, not an apples-to-apples pricing, security, usability or fit benchmark. Department concepts vary: a configurable grouping is not necessarily a native Department domain.

## DATN engineering feasibility

- `[DOCUMENTED]` Accepted target: NestJS Modular Monolith, Next.js BFF, MongoDB 7.0 shared `continuum_db`, LanceDB auxiliary SAG store, PostgreSQL/pgvector only future SAG scaling option.
- `[FACT]` Current source has domain schemas/scaffolding and health controllers, but workspace research states no end-to-end Project/Team CRUD or FE workflows; source search did not find completed Jira integration or LanceDB runtime implementation.
- `[INFERENCE]` A narrow project-scoped internal tracker is materially smaller than full Jira parity. Engineering capacity, quality/security bar and operations ownership still constrain scope; the current task-source decision does not establish long-term TCO or approve a broad product replacement.
- `[DOCUMENTED]` Historical `.sage` inventory/current-state contains drift on accepted decisions; current decision register and SPEC are controlling evidence for accepted target. This report does not reconcile/edit those files.

## Decision conditions (not decisions)

To assess long-term economics and broader product strategy, collect SaaS invoice/plan, real user journeys, quantified friction, capability gap, data/ACL needs, internal staffing/cost and migration/exit constraints. The DATN MVP task source is already selected; these items do not reopen Jira as its source. `[DECISION REQUIRED]` Product owner decides whether to expand beyond the narrow internal task MVP and over what time horizon.
