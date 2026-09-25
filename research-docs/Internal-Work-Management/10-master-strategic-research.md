# Master Strategic Research: Internal Work + Knowledge Management

**Status:** Draft research for product/technical lead review. No decision, approved requirement, implementation task or architecture change is made here.  
**Evidence date:** Repository snapshot read during this research; official web sources checked 2026-09-25.  
**Scope:** Assess whether DATN needs an internal work-management ecosystem or whether Jira/Atlassian plus configuration/operating-model changes suffice.

## Executive Summary

- `[DOCUMENTED]` Current Continuum AI MVP addresses knowledge continuity for **one software project with multiple teams**, not enterprise-wide work management. Jira supplies task context; user-confirmed capture, evidence-backed knowledge, authorized human verification, permission-aware retrieval and handover form its documented core.
- `[UNKNOWN]` The central problem in this hypothesis is not proven: repository evidence contains no current Jira plan/invoice, seat count, configuration audit, measured friction, or user interviews. Therefore cost pressure, Jira deficiency, and need for Department/executive entities remain unknown.
- `[WEB RESEARCH]` Jira has Free and paid tiers with differing user/feature limits; Premium includes cross-team/project planning features. Thus “Jira cannot support cross-team planning” is too broad; some capabilities are plan-gated or configuration-dependent. Jira + Confluence provides product-level work/document linking. Public capability is not proof that DATN tenant is configured or that workflow fits.
- `[INFERENCE]` A hybrid concept—keep task authority in Jira while Continuum addresses verified knowledge continuity—is consistent with current Continuum documents. That is not a recommendation to build a broad management platform or a decision to retain Jira forever.
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

## Current Jira Situation

`[UNKNOWN]` Actual DATN site, plan, billable seats, apps, workflows, permissions, automation, dashboards, integrations and Confluence use were not available in repo evidence. Public capabilities below must not be conflated with tenant state.

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

Current product documentation calls for Jira task-context sync for Continuum MVP and treats other connectors as future/stretch. Source has Jira-related scaffolding but does not prove full live API/OAuth/webhook/reconciliation UX; source search found no active LanceDB runtime dependency. This is an implementation gap against current target/spec evidence, not a reason to change accepted architecture.

Integration quality requires identity mapping, source authority, least-scope auth, webhook verification, idempotency, retries, ordering/versioning, reconciliation, deletion/ACL revocation, observability, retention and audit. Start with links/read-only sync as candidate, not a decided architecture.

## Build vs Buy vs Hybrid

| Option | Main upside | Main cost/risk | DATN evidence fit |
|---|---|---|---|
| A Continue Jira | Reuse mature work system; adjust plan/config/process | Plan costs/limitations; tenant fit unknown | Requires tenant/use-case audit |
| B Jira + Confluence | Work + documentation product integration | Separate product seats/admin, permissions across products | Knowledge needs must be measured |
| C Internal replacing Jira | Tailored domain and control | Large build, migration, security and ongoing operations burden | Not current Continuum MVP; no complete task product evidenced |
| D Internal above Jira | Preserve task SoT while joining verified context | Connector, ACL, duplication and freshness burden | Conceptually aligned with Continuum current documents; not a broad product approval |
| E Internal + multi-system | Broad interoperability potential | Highest connector/governance/maintenance scope | Hypothesis only; other connectors stretch/future in current MVP docs |

No ranking: weights and real costs are absent. Market examples in `08-build-buy-hybrid.md` link official product docs and are feature-area scan, not vendor validation or recommendation.

## Internal Platform Concept

Organization → (Department?) → Team → Project → Work → Knowledge → Decision/Evidence is a conceptual hypothesis only. A logical unified view can preserve separate authoritative systems; a single UI/database does not guarantee consistent meaning or permissions. Avoid starting from hierarchy; start from validated user decisions and traceable outcomes.

## MVP Hypothesis

The candidate in `09-internal-platform-mvp.md` is an experimental, one-cohort slice around task links, capture, verified knowledge, scoped retrieval and handover; Department, portfolio layer and task-system replacement remain unapproved. Proposed MUST/SHOULD/LATER/OUT OF SCOPE labels do not modify `01_MVP_SCOPE.md`.

## Success Metrics

Define baseline before target: actual recurring TCO; time to answer repeatable context/handover question; tool switches; traceability/evidence coverage; sync lag/duplicate/missing/revoked data; successor outcome; adoption effort; and authorization leakage (zero as a security guardrail). Avoid individual productivity scoring. See `09-internal-platform-mvp.md`.

## Risks

1. Rewriting Continuum’s accepted MVP into an enterprise system without approval.
2. Duplicating Jira task authority and creating conflicting updates.
3. Assuming Department, director access or cardinality.
4. Underestimating build/maintenance/security/backup/support costs.
5. ACL mismatch causing disclosure in search, model prompts, aggregate views, cache or logs.
6. Stale dashboards giving false confidence.
7. Confusing schemas/modules/API scaffolding with complete feature or E2E flow.
8. Stale `.sage` inventory/current-state statements conflicting with accepted decisions; do not treat historical drift as new decision.
9. Treating vendor marketing/public capability as DATN tenant evidence.

## What We Should NOT Build

`[PROPOSAL]` Do not build a Jira clone before proving an unmet need; generic workflow builder; broad enterprise Department hierarchy before cardinality decisions; every connector at once; duplicate canonical task CRUD without source-of-truth decision; unrestricted director visibility; employee scoring; autonomous knowledge verification/permission changes; full HR/LMS; migration platform without a migration decision. These guardrails are research proposals, not binding product decisions.

## UNKNOWN

- Actual Jira plan, users, invoices, Confluence/apps/Guard and configuration.
- User-reported and observed friction; root cause distribution.
- Operating model, team/org sizes, Department presence and all cardinalities.
- Executive persona, recurring decisions, visibility and data classes.
- Internal staff/run cost, delivery capacity, operations owner and security constraints.
- Whether Jira configuration or Jira+Confluence resolves any measured problem.
- Canonical task source, link/sync/write mode and acceptable freshness.
- Connector credentials, data scopes, ACL behavior, retention and privacy.
- Approved scope relationship between new hypothesis and Continuum MVP.

## DECISION REQUIRED

Product/technical lead to decide only after review: whether to investigate/pilot the hypothesis; whether Department/executive layer is in scope; system-of-record boundaries; build/buy/hybrid option; user cohort; data/authorization policy; metrics/thresholds; cost horizon and owner. This report makes none of those choices.

## Next Research Questions

1. What exact recurring incident causes measurable loss/time/cost, for which actor, how often?
2. What Jira plan, paid products, seats, apps and permissions does DATN currently operate, from invoice/admin evidence?
3. Which required task workflows are blocked after configuration and plan alternatives are tested?
4. Which facts/knowledge are lost, where are sources stored, and what handover task demonstrates the loss?
5. Is Department a real unit with independent lifecycle/access/ownership, or merely reporting grouping?
6. What decision would an executive view change, and what fields may that audience see?
7. Does Jira+Confluence or a lightweight operating-model change resolve the problem at lower TCO?
8. What is the smallest pilot that tests value without duplicating task authority or changing accepted Continuum scope?
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
