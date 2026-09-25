# Internal Platform MVP Hypothesis

**Status:** Entire scope in this document is `[PROPOSAL]` for validation, not approved Continuum MVP scope.

## Guardrail: two different product questions

- `[DOCUMENTED] CURRENT CONTINUUM MVP`: knowledge continuity within one software project that has multiple teams; Jira task context, user-confirmed capture, evidence-backed knowledge, permission-aware retrieval, handover and evaluation.
- `[HYPOTHESIS] POSSIBLE INTERNAL WORK-MANAGEMENT PLATFORM`: organization-wide Department/team/project/task/executive model, potentially replacing or sitting above Jira. Not approved and not a rewrite of Continuum architecture/spec.

The MVP candidate below tests whether a narrow additional layer creates measurable value; it is not a Jira clone blueprint.

## Candidate validation slice

`[PROPOSAL]` Choose one representative project/team cohort; link to canonical work items (do not duplicate task ownership by default); capture context/decision with source evidence; show scoped knowledge/handover; test a narrowly defined management question only if interviews establish a real decision need. Department entity, portfolio planning and generic workflow engine are excluded until validated.

| Candidate level | Hypothesis contents | Why / what must be validated |
|---|---|---|
| MUST HAVE — proposed only | One selected cohort; authentication/access inherited from accepted Continuum model; task link/reference; human-confirmed capture; provenance/evidence; verified-vs-proposed state; permission-filtered retrieval; handover scenario; audit of sensitive actions | Matches Continuum continuity objective; do not interpret as approval of task manager replacement |
| SHOULD HAVE — proposed only | Basic project/team context, source freshness/status, minimal operational view for a named persona | Only after required fields/decision question and access boundary are known |
| LATER — proposed only | Additional connectors, multi-project portfolio, Department hierarchy, leadership roll-ups, rich work item/task lifecycle, advanced dashboards | Broad scope; needs evidence and owner; many items exceed current Continuum scope |
| OUT OF SCOPE for this validation hypothesis | Full Jira clone, generic workflow builder, employee performance score, autonomous approval/policy changes, enterprise HR/LMS, unrestricted director access, mass migration | Prevent hypothesis from silently expanding current MVP; revisit only with explicit product decision |

## Validation protocol

1. Record a baseline using a repeatable task/knowledge/handover scenario in existing tools.
2. Prototype/pilot with one cohort and explicit data permissions; avoid migrating or mutating source records unless separately approved.
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
| Sync reliability | Event lag, duplicate/missing/revoked records, reconciliation result | Source API/webhook limits and retries must be included |
| Handover effectiveness | Successor time to locate context / correctly answer scenario questions | Not merely checklist completion |
| Authorization | Unauthorized records returned, displayed, exported or included in model context | Security guardrail; desired leakage count is zero |
| Adoption/effort | Active use and time required to capture/update | Avoid optimizing activity count or employee scoring |

## Risks and stop signals

- Duplicating Jira and creating conflicting task sources.
- More data surfaces without reliable ACL propagation.
- Reports create false certainty from stale/missing data.
- Capture overhead exceeds value of retained context.
- Integrations/LLM/security/maintenance consume team capacity beyond available runway.
- A user can get same outcome by changing Jira configuration or operating process at lower cost.
- Existing Continuum scope is silently rewritten to organization-wide work management.

`[PROPOSAL]` Stop or narrow the hypothesis if pain is not reproducible, user count/plan makes SaaS cost immaterial, configuration addresses the issue, no owner for internal operations exists, or security semantics cannot be preserved.

## Open decisions

`[DECISION REQUIRED]` Whether to conduct pilot; cohort; task SoT; management persona; Department scope; integrations; data classes; success thresholds; staffing and run-cost; relationship to accepted Continuum MVP. No decision is made by this research document.
