# Master Strategic Research: Internal Work + Knowledge Management

**Status:** Draft research. Records the user's task-source decision but makes no decision on broad enterprise work-management scope or detailed implementation requirements.
**Evidence date:** Repository snapshot read during this research; official web sources checked 2026-09-25.  
**Scope:** Assess the delivery boundary and operating implications of the selected internal task source, and keep the broader organization-wide work-management hypothesis separate.

**Decision update (2026-10-01):** Continuum Task API with canonical task records in MongoDB is the source for DATN task lifecycle; Jira is not the task source. This boundary is recorded in ADR-009 and the affected product/architecture/database documents. The detailed Use Case/schema remains under review. Market/cost research below remains reference material, but Jira-as-source and hybrid recommendations are no longer current product direction.

## Executive Summary

- `[DOCUMENTED]` Current Continuum AI MVP addresses knowledge continuity for **one software project with multiple teams**, not enterprise-wide work management. Continuum Task API/MongoDB supplies task lifecycle context; user-confirmed capture, evidence-backed knowledge, authorized human verification, permission-aware retrieval and handover form its core.
- `[UNKNOWN]` The repository contains no quantified user friction, build/run cost, delivery capacity or maintenance-owner evidence. The user's decision selects an internal task source; it does not by itself prove economic advantage or a need for Department/executive entities.
- `[WEB RESEARCH]` Jira has Free and paid tiers with differing user/feature limits; Premium includes cross-team/project planning features. Thus “Jira cannot support cross-team planning” is too broad; some capabilities are plan-gated or configuration-dependent. Jira + Confluence provides product-level work/document linking. Public capability is not proof that DATN tenant is configured or that workflow fits.
- `[DECIDED]` Internal Continuum Task is canonical for DATN; Jira is not used as the task source. This does not approve a full Jira feature clone, organization-wide hierarchy, or unbounded scope.
- `[DECISION REQUIRED]` Review detailed task Use Cases, fields/statuses, delivery boundary and technical impact. Cost research does not override the chosen source-of-truth direction.

## Business Problem

The research hypothesis is that an external SaaS work system may impose cost, plan limits, organizational friction, fragmented task/knowledge context, or governance mismatch for a constrained graduation-project group. Each is a separate claim and needs evidence.

| Claim | Current evidence | Status |
|---|---|---|
| Jira subscription is material cost | No tenant invoice/plan/user count in reviewed repository | `[UNKNOWN]` |
| Plan limits prevent required workflows | Official plan differences exist, but no named DATN workflow mapped to a blocker | `[UNKNOWN]` |
| Organization model does not fit | Department/executive hierarchy appears in new hypothesis, not accepted Continuum scope | `[UNKNOWN]` |
| Knowledge is lost during team/member changes | This is the documented Continuum problem/purpose | `[DOCUMENTED]` |
| Jira itself causes the knowledge loss | Task context and verified experiential knowledge differ; causality not established | `[INFERENCE]` / `[UNKNOWN]` |

## Jira Market Research (Reference Only)

`[UNKNOWN]` Actual DATN site, plan, billable seats, apps, workflows, permissions, automation, dashboards, integrations and Confluence use were not available in repo evidence. Public capabilities below are historical market context only; Jira is not the selected task source for Continuum.

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

Operational source of truth for accepted Continuum target: MongoDB 7.0, shared `continuum_db` (DEC-011/SPEC-001). LanceDB is auxiliary SAG retrieval per DEC-015/SPEC-005; PostgreSQL+pgvector is future scaling option only. These decisions do not require copying every external system’s canonical data into MongoDB.

## Integration Model

Current product documentation calls for internal Continuum Task API/MongoDB and does not require Jira task-context sync. The reviewed code snapshots do not provide internal task CRUD. ADR-009 and the affected Tech, Architecture, workflow and database-design documents record the internal source boundary; the remaining implementation/spec gap is the detailed task Use Case, field-level schema, API contract and authorization matrix. LanceDB is the accepted MVP SAG target (DEC-015/SPEC-005), while its current source/deployment integration still requires verification; PostgreSQL + pgvector/Qdrant remains a future alternative.

Any future external connector would require identity mapping, source authority, least-scope auth, webhook verification where relevant, idempotency, retries, ordering/versioning, reconciliation, deletion/ACL revocation, observability, retention and audit. This is future connector research, not a requirement for the current internal Task API.

## Build vs Buy vs Hybrid

| Option | Main upside | Main cost/risk | DATN evidence fit |
|---|---|---|---|
| A Continue Jira | Reuse mature work system; adjust plan/config/process | Plan costs/limitations; tenant fit unknown | Requires tenant/use-case audit |
| B Jira + Confluence | Work + documentation product integration | Separate product seats/admin, permissions across products | Knowledge needs must be measured |
| C Internal task source | Tailored task context; direct linking to notes and handover | Build/run cost, security and ongoing operations burden | Selected by the user as task source; detailed scope and technical design remain open |
| D Internal above Jira | Preserve Jira task SoT while joining verified context | Connector, ACL, duplication and freshness burden | Not the selected DATN task direction |
| E Internal + multi-system | Broad interoperability potential | Highest connector/governance/maintenance scope | Hypothesis only; other connectors stretch/future in current MVP docs |

No ranking: weights and real costs are absent. Market examples in `08-build-buy-hybrid.md` link official product docs and are feature-area scan, not vendor validation or recommendation.

## Internal Platform Concept

Organization → (Department?) → Team → Project → Work → Knowledge → Decision/Evidence is a conceptual hypothesis only. A logical unified view can preserve separate authoritative systems; a single UI/database does not guarantee consistent meaning or permissions. Avoid starting from hierarchy; start from validated user decisions and traceable outcomes.

## MVP Hypothesis

The candidate in `09-internal-platform-mvp.md` keeps the broader Department/portfolio layer hypothetical while recording the selected internal project-scoped Task source. Detailed P0/P1 task Use Cases remain in `12-continuum-task-management-use-cases.md` for user review; they do not silently expand the MVP before approval.

## Success Metrics

Define baseline before target: actual recurring TCO; time to answer repeatable context/handover question; tool switches; traceability/evidence coverage; sync lag/duplicate/missing/revoked data; successor outcome; adoption effort; and authorization leakage (zero as a security guardrail). Avoid individual productivity scoring. See `09-internal-platform-mvp.md`.

## Risks

1. Rewriting Continuum’s accepted MVP into an enterprise system without approval.
2. Reintroducing Jira as a second writable task source or expanding the internal module to full Jira parity.
3. Assuming Department, director access or cardinality.
4. Underestimating build/maintenance/security/backup/support costs.
5. ACL mismatch causing disclosure in search, model prompts, aggregate views, cache or logs.
6. Stale dashboards giving false confidence.
7. Confusing schemas/modules/API scaffolding with complete feature or E2E flow.
8. Stale `.sage` inventory/current-state statements conflicting with accepted decisions; do not treat historical drift as new decision.
9. Treating vendor marketing/public capability as DATN tenant evidence.

## What We Should NOT Build

`[PROPOSAL]` Do not build full Jira parity; generic workflow builder; broad enterprise Department hierarchy before cardinality decisions; every connector at once; a second task source; unrestricted director visibility; employee scoring; autonomous knowledge verification/permission changes; full HR/LMS; or Jira migration/synchronization without a separate decision. The narrow internal task source is selected; this guardrail limits feature breadth.

## UNKNOWN

- User-reported and observed friction; root cause distribution.
- Operating model, team/org sizes, Department presence and all cardinalities.
- Executive persona, recurring decisions, visibility and data classes.
- Internal staff/run cost, delivery capacity, operations owner and security constraints.
- Exact internal task fields, state transitions, ownership scope and permissions.
- Connector credentials, data scopes, ACL behavior, retention and privacy.
- Approved scope relationship between new hypothesis and Continuum MVP.

## DECISION REQUIRED

Product/technical lead to decide after review: detailed internal task Use Cases and fields; whether Department/executive layer is in scope; user cohort; data/authorization policy; metrics/thresholds; cost horizon and operations owner. The task-source choice is already recorded as internal Continuum Task for DATN.

## Next Research Questions

1. What exact recurring incident causes measurable loss/time/cost, for which actor, how often?
2. Which exact internal task fields, statuses, assignments and permissions are needed for the selected project's capture and handover flow?
3. Which parts of the accepted six-week MVP must be reduced to deliver the task flow without compromising knowledge verification, permission-aware retrieval and handover evaluation?
4. Which facts/knowledge are lost, where are sources stored, and what handover task demonstrates the loss?
5. Is Department a real unit with independent lifecycle/access/ownership, or merely reporting grouping?
6. What decision would an executive view change, and what fields may that audience see?
7. What is the build/run cost and who owns maintenance of the internal task source after the graduation project?
8. What is the smallest project-scoped task slice that supports capture and handover without expanding into full Jira parity?
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
- [11 — ManageWork codebase assessment](11-managework-codebase-assessment.md)
- [12 — Continuum task-management use cases for review](12-continuum-task-management-use-cases.md)
