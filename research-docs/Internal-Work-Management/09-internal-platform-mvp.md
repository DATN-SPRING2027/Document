# Internal Platform MVP Hypothesis

**Status:** `[PROPOSAL]` for enterprise-wide expansion only; the existing single-project Continuum MVP and its Task API are approved scope.

> **Decision amendment — 2026-10-02:** The proposal labels below do not describe all of the approved MVP anymore. Continuum Task API/Task Service is approved as the canonical internal task source; its API/use-case and persistence documents are the authority for that capability. This file remains proposal-only for expansion beyond the existing single-project/multi-team Continuum scope (for example, Department hierarchy, executive portfolio views, generic workflows, or additional connectors). Jira task import/sync is not part of the current MVP.

## Guardrail: two different product questions

- `[DOCUMENTED] CURRENT CONTINUUM MVP`: knowledge continuity and internal task management within one software project that has multiple teams; Continuum Task API, user-confirmed capture, evidence-backed knowledge, permission-aware retrieval, handover and evaluation.
- `[HYPOTHESIS] POSSIBLE ENTERPRISE-WIDE EXPANSION`: Department/portfolio/executive model and broader organization-wide workflow. Not approved and not a rewrite of the accepted Continuum architecture/spec.

The MVP candidate below tests whether a narrow additional layer creates measurable value; it is not a Jira clone blueprint.

## Candidate validation slice

`[PROPOSAL]` To validate expansion beyond the approved product, choose one representative project/team cohort; exercise the approved Continuum Task API with capture, source evidence, scoped knowledge/handover; test a narrowly defined management question only if interviews establish a real decision need. Department entity, portfolio planning and generic workflow engine are excluded until validated. Do not create a second task authority.

| Candidate level | Hypothesis contents | Why / what must be validated |
|---|---|---|
| MUST HAVE — proposal for an expansion pilot only | One selected cohort; use of the approved Task API; human-confirmed capture; provenance/evidence; verified-vs-proposed state; permission-filtered retrieval; handover scenario; audit of sensitive actions | The Task API itself is already part of approved MVP; this row concerns an expansion validation slice, not a new source-of-truth decision |
| SHOULD HAVE — proposed only | Basic project/team context, source freshness/status, minimal operational view for a named persona | Only after required fields/decision question and access boundary are known |
| LATER — proposed only | Additional external connectors, multi-project portfolio, Department hierarchy, leadership roll-ups, advanced dashboards | Broad scope; needs evidence and owner; these do not change the approved internal Task API |
| OUT OF SCOPE for this validation hypothesis | Full Jira clone, generic workflow builder, employee performance score, autonomous approval/policy changes, enterprise HR/LMS, unrestricted director access, mass migration | Prevent hypothesis from silently expanding current MVP; revisit only with explicit product decision |

## Validation protocol

1. Record a baseline using a repeatable task/knowledge/handover scenario in existing tools.
2. Pilot with one cohort and explicit data permissions; exercise task changes through the canonical Continuum Task API. Do not migrate or mutate any external system's records unless separately approved.
3. Compare completion time, context switches, missing evidence, handover outcome, synchronization correctness and access-control behavior.
4. Ask users and leaders whether the result changed an actual decision or removed a repeated operational pain.
5. Decide continue/stop/adjust against pre-agreed criteria; no threshold is set here.

## Success measures (define baseline and target first)

| Measure | Operational definition candidate | Data collection / caveat |
|---|---|---|
| SaaS total cost | Actual invoice + apps/Guard + admin effort per period | Do not compare list prices to internal build without labor/operations |
| Time-to-context | Time to answer a fixed work/knowledge/handover question | Same question, same cohort, source citations retained |
| Context switching | Tool switches to complete defined scenario | Observe/sample; not equal to user satisfaction |
| Traceability | Share of sampled knowledge claims with valid source, owner and verification state | Define denominator and quality rubric |
| Task/data reliability | Task mutation integrity, duplicate/retried requests, missing audit/event records, revoked access behavior | Keep task integrity checks separate from any future connector sync measurements |
| Handover effectiveness | Successor time to locate context / correctly answer scenario questions | Not merely checklist completion |
| Authorization | Unauthorized records returned, displayed, exported or included in model context | Security guardrail; desired leakage count is zero |
| Adoption/effort | Active use and time required to capture/update | Avoid optimizing activity count or employee scoring |

## Risks and stop signals

- Reintroducing Jira or another external system as a competing writable task source.
- More data surfaces without reliable ACL propagation.
- Reports create false certainty from stale/missing data.
- Capture overhead exceeds value of retained context.
- Integrations/LLM/security/maintenance consume team capacity beyond available runway.
- A user can get same outcome by changing Jira configuration or operating process at lower cost.
- Existing Continuum scope is silently rewritten to organization-wide work management.

`[PROPOSAL]` Stop or narrow the hypothesis if pain is not reproducible, user count/plan makes SaaS cost immaterial, configuration addresses the issue, no owner for internal operations exists, or security semantics cannot be preserved.

## Open decisions

`[DECISION REQUIRED]` Whether to conduct an expansion pilot; cohort; management persona; Department scope; future integrations; data classes; success thresholds; staffing and run-cost; relationship to accepted Continuum MVP. The task source of truth is already approved and is not an open question here.
