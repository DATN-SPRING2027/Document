# Master Strategic Research: Internal Work + Knowledge Management

**Status:** Draft research for product/technical lead review. No decision, approved requirement, implementation task or architecture change is made here.
**Evidence date:** Repository snapshot read during this research; official web sources checked 2026-09-25.  
**Scope:** Compare external SaaS and process alternatives for possible future integration, and assess whether DATN needs work-management expansion beyond the already approved single-project Continuum task-and-knowledge MVP.

> **Approved Task product target — 2026-10-02 (not current runtime):** The earlier Jira-source hypothesis is superseded for the DATN task-management MVP. Continuum's Task API/Service is the canonical task lifecycle; when implemented, it will run separately from other NestJS services, use source in the existing `DATN_BE` repository, and store canonical records in MongoDB `continuum_task`. Jira is not a task source in this MVP; import, sync, reconciliation and Jira-specific actors are out of scope. This research remains useful for future connector evaluation, external SaaS comparisons and the boundary between the approved single-project Continuum product and any broader enterprise work-management proposal. See [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md), [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md) and [Task Management Use Cases](12-continuum-task-management-use-cases.md).

## Executive Summary

- `[DOCUMENTED]` Current Continuum AI MVP addresses knowledge continuity and internal task management for **one software project with multiple teams**, not enterprise-wide portfolio/HR work management. Continuum Task API owns canonical task context; user-confirmed capture, evidence-backed knowledge, authorized human verification, permission-aware retrieval and handover form its documented core.
- `[UNKNOWN]` The central problem in this hypothesis is not proven: repository evidence contains no current Jira plan/invoice, seat count, configuration audit, measured friction, or user interviews. Therefore cost pressure, Jira deficiency, and need for Department/executive entities remain unknown.
- `[WEB RESEARCH]` Jira has Free and paid tiers with differing user/feature limits; Premium includes cross-team/project planning features. Thus “Jira cannot support cross-team planning” is too broad; some capabilities are plan-gated or configuration-dependent. Jira + Confluence provides product-level work/document linking. Public capability is not proof that DATN tenant is configured or that workflow fits.
- `[SUPERSEDED]` The earlier hybrid concept—keep task authority in Jira while Continuum handles knowledge continuity—does not describe the approved task MVP. External SaaS products may still be evaluated as future connectors or comparison points; none is the canonical DATN task source.
- `[DECISION REQUIRED]` Choose after obtaining actual license/configuration/use-case evidence and comparing SaaS, internal and hybrid total cost over a common time horizon.

## Business Problem

The research hypothesis is that an external SaaS work system may impose cost, plan limits, organizational friction, fragmented task/knowledge context, or governance mismatch for a constrained graduation-project group. Each is a separate claim and needs evidence.

| Claim | Current evidence | Status |
|---|---|---|
| Jira subscription is material cost | No tenant invoice/plan/user count in reviewed repository | `[UNKNOWN]` |
| Plan limits prevent required workflows | Official plan differences exist, but no named DATN workflow mapped to a blocker | `[UNKNOWN]` |
| Organization model does not fit | Department/executive hierarchy appears in new hypothesis, not accepted Continuum scope | `[UNKNOWN]` |
| Knowledge is lost during team/member changes | This is the documented Continuum problem/purpose | `[DOCUMENTED]` |
| Jira itself causes the knowledge loss | Task context and verified experiential knowledge differ; causality not established | `[INFERENCE]` / `[UNKNOWN]` |

## Jira as a Market Comparator / Possible Future Connector

`[UNKNOWN]` Actual DATN site, plan, billable seats, apps, workflows, permissions, automation, dashboards, integrations and Confluence use were not available in repo evidence. Public capabilities below must not be conflated with tenant state. This audit is useful only for evaluating a future external connector or SaaS alternative; it does not determine the approved internal task source.

`[WEB RESEARCH]` Atlassian lists Free up to 10 users and plan-dependent limits; Standard/Premium/Enterprise add different controls, storage, automation, planning/reporting and governance. Jira Premium Plans/Advanced Roadmaps supports planning across multiple teams/projects. Jira has global/project/issue permission concepts. Jira/Confluence integration and Smart Links support linking work and docs. Links: [Jira pricing](https://www.atlassian.com/software/jira/pricing), [Jira editions](https://www.atlassian.com/software/jira/guides/more/jira-editions), [Advanced Roadmaps](https://support.atlassian.com/jira-software-cloud/docs/what-is-advanced-roadmaps/), [permission types](https://support.atlassian.com/jira-cloud-administration/docs/types-of-permissions-in-jira/), [Jira + Confluence](https://www.atlassian.com/software/confluence/jira-integration).

Jira capability labels: cross-project planning can be a product capability with plan gate; permissions/reporting depend on features and configuration; Confluence is ecosystem/additional product; Department as DATN business entity is `[UNKNOWN]`. No source here establishes that Jira is “bad” or adequate for this tenant.

## Cost Analysis

Use actual cloud billing/quote. Atlassian describes per-product/user billing and monthly Maximum Quantity Billing behavior; seats removed mid-cycle may not reduce that cycle’s bill. See [Cloud Pricing & Licensing](https://www.atlassian.com/licensing/cloud) and [Cloud Pricing Calculator](https://www.atlassian.com/software/pricing-calculator).

An illustrative Standard scenario using an example public monthly rate of $8.60 for the first price tier (USD, before tax/discount, not a DATN quote): 10 paid seats = $86/month; 20 = $172; 50 = $430; 100 = $860. Annualized 12× figures are sensitivity arithmetic only. Free may be $0 for up to 10 users when its capability limits are acceptable. Standard may still be required for permission/audit needs. Premium/Enterprise/Confluence/apps costs require current calculator/quote and counts.

Compare over a shared period:

```text
SaaS = Jira/Confluence/apps/Guard subscriptions + administration + onboarding/migration
Internal = discovery/build labor + hosting/AI + backups/monitoring/security/support + maintenance + migration
Hybrid = relevant SaaS + internal layer + connector/ACL/reconciliation operations
```

`[UNKNOWN]` No valid break-even can be calculated without invoice, users, products, staffing rates, required reliability/security, migration, operating owner and chosen time horizon.

## Root Cause Analysis

| Pain point | Likely root-cause categories | Jira limitation? | Internal platform relevance |
|---|---|---|---|
| High bill | SaaS cost, seat management, plan selection, add-ons | Unknown until invoice/feature mapping | Compare whole TCO; build cost may exceed subscription |
| Missing cross-team view | Plan limitation, configuration, reporting model, source data | Not blanket: Premium has multi-team/project Plans | Could add tailored view; preserve permissions/data freshness |
| Repeated status reporting | Operating model, automation/configuration, duplicated updates | Unknown | A unified view could help only if source/status contracts are reliable |
| Knowledge lost at handover | Knowledge fragmentation, capture/ownership/process | Not inherently a Jira work-tracking defect | Directly related to existing Continuum goal |
| Department visibility gap | Governance, information architecture, perhaps product/plan | Unknown | Requires validated Department semantics and access policy |
| Multiple systems | Integration, source-of-truth, identity/ACL mapping | Ecosystem is one option | Broad connector layer has material operating/security cost |

## Operating Model

Candidate loop `[PROPOSAL]`: canonical work source → person links relevant task/context → human confirms capture → system proposes evidence-backed knowledge → authorized reviewer verifies → scoped retrieval/handover → gap/blocker returned to owner/source. This follows the Continuum knowledge-continuity concept but does not define company-wide management workflow.

Research current work creation, ownership, state semantics, approvals, reporting, handover and exception paths. Identify whether pain is configuration, process or actual missing capability before product design.

## Organization / Department / Team Model

`[DOCUMENTED]` Current role model includes ADMIN, TEAM_LEADER, MEMBER; scope-based SME/KNOWLEDGE_OWNER/SUCCESSOR; no documented Department manager/Director role. ADMIN is not automatically allowed to read confidential content. Project/team/organization membership and capability grants are part of current governance concepts.

`[UNKNOWN]` Whether Department is first-class, cardinalities (Team↔Department, Project↔Department, Team↔Project, User↔Organization), cross-department projects and org-wide visibility. An organization chart must not be inferred from schema scaffolding. See `04-organization-department-team-model.md`.

## Executive Management Model

No confirmed executive persona, cadence, decision question or access scope is evidenced. A dashboard is not a requirement by itself. If needed, define question → metric/source/freshness → permitted aggregate → drill-down ACL → action owner. Jira Premium planning and enterprise portfolio offerings exist, but do not imply a DATN need. See `05-executive-management-model.md`.

## Work + Knowledge Model

Work and knowledge are related but distinct: task lifecycle vs verified understanding/evidence. Current Continuum docs require user-confirmed capture and human-verified knowledge proposals; AI retrieval is subject to permission/provenance. Do not treat a Jira issue, schema, vector record or generated answer as verified product knowledge. See `06-work-knowledge-unification.md`.

Operational source of truth for the accepted Continuum target is MongoDB 7.0 on the existing cluster/replica set, with one logical database per active bounded service; cross-cutting audit uses `continuum_audit` (ADR-003/DEC-011). In the approved product target, the Task API/Service owns `continuum_task`; `continuum_task` and `continuum_ai_adapter` are not in the current active BE runtime database inventory yet. The current BE inventory includes `continuum_jira` even though Jira is not the canonical MVP task source and Jira task import/sync is excluded; reconcile runtime and product inventory separately. LanceDB is auxiliary SAG retrieval per DEC-015/SPEC-005; PostgreSQL+pgvector is a future SAG scaling option only. These decisions do not require copying every external system’s canonical data into MongoDB.

## Integration Model

`[APPROVED TARGET]` Continuum Task API/Task Service is the MVP task source. Jira integration is not required and Jira-related source scaffolding is legacy evidence, not proof of an active connector. Any future external connector needs separate approval and must not create a competing writable task source. Source search found no active LanceDB runtime dependency; that remains a separate implementation gap against the accepted SAG target, not a reason to change the task-source decision.

Future integration quality requires identity mapping, source authority, least-scope auth, webhook verification, idempotency, retries, ordering/versioning, reconciliation, deletion/ACL revocation, observability, retention and audit. Link-only or read-only integration may be evaluated later; neither is part of the approved Task MVP.

## Build vs Buy vs Hybrid

| Option | Main upside | Main cost/risk | DATN evidence fit |
|---|---|---|---|
| A Continue Jira | Reuse mature external work system; adjust plan/config/process | Plan costs/limitations; tenant fit unknown | SaaS comparison only; Jira is not the MVP task source |
| B Jira + Confluence | External work + documentation product integration | Separate product seats/admin, permissions across products | Future connector/alternative question; not an MVP dependency |
| C Internal task management | Continuum owns the task lifecycle tailored to its knowledge/handover flow | Build, security and ongoing operations burden | Approved for the current DATN task MVP; not a full enterprise Jira replacement |
| D Internal above Jira | Link an external task source to verified context | Connector, ACL, duplication and freshness burden | Future-only hypothesis; must not replace Continuum's canonical task API in the MVP |
| E Internal + multi-system | Broad interoperability potential | Highest connector/governance/maintenance scope | Hypothesis only; no general integration hub is approved |

No ranking: weights and real costs are absent. Market examples in `08-build-buy-hybrid.md` link official product docs and are feature-area scan, not vendor validation or recommendation.

## Internal Platform Concept

Organization → (Department?) → Team → Project → Work → Knowledge → Decision/Evidence is a conceptual hypothesis only. A logical unified view can preserve separate authoritative systems; a single UI/database does not guarantee consistent meaning or permissions. Avoid starting from hierarchy; start from validated user decisions and traceable outcomes.

## MVP Hypothesis

The candidate in `09-internal-platform-mvp.md` is an older validation proposal and is superseded where it treats task ownership as undecided. Current MVP includes Continuum Task API plus capture, verified knowledge, scoped retrieval and handover. Department, enterprise portfolio, broad workflow-engine and HR scope remain unapproved; the current scope authority is `01_MVP_SCOPE.md`.

## Success Metrics

Define baseline before target: actual recurring TCO; time to answer repeatable context/handover question; tool switches; traceability/evidence coverage; task mutation/event integrity; future-connector sync lag/duplicate/missing/revoked data only if a connector is later approved; successor outcome; adoption effort; and authorization leakage (zero as a security guardrail). Avoid individual productivity scoring. See `09-internal-platform-mvp.md`.

## Risks

1. Rewriting Continuum’s accepted MVP into an enterprise system without approval.
2. Reintroducing Jira as a second writable task authority or retaining stale connector assumptions as current requirements.
3. Assuming Department, director access or cardinality.
4. Underestimating build/maintenance/security/backup/support costs.
5. ACL mismatch causing disclosure in search, model prompts, aggregate views, cache or logs.
6. Stale dashboards giving false confidence.
7. Confusing schemas/modules/API scaffolding with complete feature or E2E flow.
8. Stale `.sage` inventory/current-state statements conflicting with accepted decisions; do not treat historical drift as new decision.
9. Treating vendor marketing/public capability as DATN tenant evidence.

## What We Should NOT Build

`[PROPOSAL]` Do not expand the approved single-project Task Service into a full Jira clone, generic workflow builder, broad enterprise Department hierarchy before cardinality decisions, every external connector at once, a second canonical task store, unrestricted director visibility, employee scoring, autonomous knowledge verification/permission changes, full HR/LMS or a migration platform without a product decision. The internal task source is already approved; these guardrails concern scope beyond that decision.

## UNKNOWN

- Actual Jira plan, users, invoices, Confluence/apps/Guard and configuration.
- User-reported and observed friction; root cause distribution.
- Operating model, team/org sizes, Department presence and all cardinalities.
- Executive persona, recurring decisions, visibility and data classes.
- Internal staff/run cost, delivery capacity, operations owner and security constraints.
- Whether Jira configuration or Jira+Confluence resolves any measured problem.
- Detailed Task API fields, lifecycle transitions, action-by-action permissions, and task-to-Project/Team constraints where they remain open in the Task Use Case contract.
- Connector credentials, data scopes, ACL behavior, retention and privacy.
- Approved scope relationship between new hypothesis and Continuum MVP.

## DECISION REQUIRED

Product/technical lead to decide only after review: whether to investigate/pilot any broader hypothesis; whether Department/executive layer or external connectors are in scope; future external data boundaries; user cohort; data/authorization policy; metrics/thresholds; cost horizon and owner. This report does not reopen the approved Continuum Task API source-of-truth decision.

## Next Research Questions

1. What exact recurring incident causes measurable loss/time/cost, for which actor, how often?
2. What Jira plan, paid products, seats, apps and permissions does DATN currently operate, from invoice/admin evidence?
3. Which required task workflows are blocked after configuration and plan alternatives are tested?
4. Which facts/knowledge are lost, where are sources stored, and what handover task demonstrates the loss?
5. Is Department a real unit with independent lifecycle/access/ownership, or merely reporting grouping?
6. What decision would an executive view change, and what fields may that audience see?
7. Does Jira+Confluence or a lightweight operating-model change resolve the problem at lower TCO?
8. What is the smallest validation of broader management/reporting value without duplicating task authority or changing accepted Continuum scope?
9. What are internal build/run/security/support costs under a realistic staffing and time horizon?
10. What measurable evidence would make the leader stop, narrow, continue or approve a separate product scope?

## Research File Index

- [01 — Problem and pain points](01-problem-and-pain-point.md)
- [02 — Jira capability and cost](02-jira-capability-and-cost.md)
- [03 — Operating model](03-operating-model.md)
- [04 — Organization, Department and Team](04-organization-department-team-model.md)
- [05 — Executive management](05-executive-management-model.md)
- [06 — Work and knowledge](06-work-knowledge-unification.md)
- [07 — Integration hub](07-integration-hub.md)
- [08 — Build, buy and hybrid](08-build-buy-hybrid.md)
- [09 — Internal platform MVP hypothesis](09-internal-platform-mvp.md)
