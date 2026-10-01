# Internal Platform MVP Hypothesis

**Status:** Organization-wide work-management scope remains `[PROPOSAL]`. Internal Continuum Task as DATN's task source was explicitly selected by the user on 2026-10-01; detailed task Use Cases remain pending review.

## Guardrail: two different product questions

- `[DECIDED] CURRENT TASK DIRECTION`: Continuum's internal Task module is canonical for DATN task lifecycle; Jira is not a task source. Work Notes remain human-confirmed, knowledge remains evidence-backed and human-verified, retrieval remains permission-aware, and handover/evaluation remain core.
- `[HYPOTHESIS] POSSIBLE BROADER WORK-MANAGEMENT PLATFORM`: organization-wide Department/portfolio/executive model. This broader expansion is not approved and is separate from the selected project-scoped task module.

The MVP candidate below tests whether a narrow additional layer creates measurable value; it is not a Jira clone blueprint.

## Candidate validation slice

`[PROPOSAL]` Choose one representative project/team cohort; manage DATN tasks internally as the canonical work records; link confirmed Work Notes and evidence; show scoped knowledge/handover; test a narrowly defined management question only if interviews establish a real decision need. Jira sync, Department entity, portfolio planning and generic workflow engine are excluded from the current task slice unless separately approved.

| Candidate level | Hypothesis contents | Why / what must be validated |
|---|---|---|
| MUST HAVE — proposed only | One selected cohort; internal project-scoped Task source; task lifecycle detailed in `12-continuum-task-management-use-cases.md` after review; task-linked or manual Work Notes; provenance/evidence; verified-vs-proposed state; permission-filtered retrieval; handover scenario; audit of sensitive actions | Matches Continuum continuity objective; detailed task fields/statuses and exact boundaries still need review |
| SHOULD HAVE — proposed only | Basic project/team context, source freshness/status, minimal operational view for a named persona | Only after required fields/decision question and access boundary are known |
| LATER — proposed only | Additional external connectors, multi-project portfolio, Department hierarchy, leadership roll-ups, advanced task lifecycle, advanced dashboards | Broad scope; needs evidence and owner; many items exceed current Continuum scope |
| OUT OF SCOPE for this validation hypothesis | Full Jira parity, generic workflow builder, employee performance score, autonomous approval/policy changes, enterprise HR/LMS, unrestricted director access, Jira task migration/synchronization | Prevent the selected internal task source from expanding into a broad management suite; revisit integrations only with explicit product decision |

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

- Scope creep toward full Jira parity or adding Jira as a second writable task source later.
- More data surfaces without reliable ACL propagation.
- Reports create false certainty from stale/missing data.
- Capture overhead exceeds value of retained context.
- Integrations/LLM/security/maintenance consume team capacity beyond available runway.
- Existing Continuum scope is silently expanded to organization-wide work management.

`[PROPOSAL]` Keep the selected task slice narrow; revisit it if no operational owner exists, required authorization semantics cannot be preserved, or the six-week delivery window cannot support core knowledge/handover outcomes.

## Open decisions

`[DECISION REQUIRED]` Cohort; detailed task requirements; Department scope; management persona; future integrations; data classes; success thresholds; staffing and run-cost; relationship of any broader platform to accepted Continuum MVP. Task source is already decided as internal Continuum Task for DATN.
