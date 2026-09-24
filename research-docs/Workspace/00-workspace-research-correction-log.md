# Workspace Research Correction Log

Correction pass date: 2026-09-24

Scope: apply only the three corrections identified by `00-workspace-research-review.md`. No requirements, business rules, unknowns, decision boundaries, domain scope, source code, architecture, ADR, SPEC, `.sage` baseline, or Jira data were changed.

## Correction 1 — Index Status

### Files Changed

- `01-project-lifecycle.md`
- `02-project-membership.md`
- `03-team-lifecycle.md`
- `04-team-membership-workspace-fe-contract.md`

### Before

- Project, Project Membership, Team, and Team Membership index rows used `[IMPLEMENTED]` wording such as `IMPLEMENTED as declaration`.
- The underlying source evidence was an index declaration in `DATN-BE/src/services/iam/infrastructure/persistence.ts`; runtime index creation and duplicate-write behavior were not verified.

### After

- All four index rows now use `[PARTIAL]`.
- Each row explicitly states that the unique index declaration exists in source, while runtime index creation and duplicate-write behavior are not verified.
- Index evidence was retained; no index was removed or described as absent.

### Reason

Review finding: a source declaration is not proof that the running database has created the index or that duplicate writes are rejected in the target environment.

## Correction 2 — Generic `/projects` FE Test

### Files Changed

- `01-project-lifecycle.md`
- `04-team-membership-workspace-fe-contract.md`

### Before

- The FE evidence identified generic query/API scaffolding, but the specific `/projects` fixture in `DATN-FE/src/lib/queries/backend.spec.tsx` was not called out next to the Project/Workspace findings.

### After

- The research now states: `Generic API/query mutation scaffolding only.`
- It identifies that `backend.spec.tsx` uses a mocked `/projects` mutation fixture.
- It explicitly states that this does not prove a working Project endpoint, Project hook, Project page, Workspace feature, or business flow.

### Reason

The test is a generic mocked mutation scaffold, not a Project feature or an integration with a live backend endpoint.

## Correction 3 — Database Topology

### Files Changed

- `01-project-lifecycle.md`
- `03-team-lifecycle.md`

### Before

- Historical service-specific persistence names such as `continuum_iam` were described as a conflict and were included in a `DECISION REQUIRED` implementation-planning item.

### After

- The research now records the accepted MVP decision: MongoDB 7.0 is operational persistence and the MVP uses shared `continuum_db`.
- Historical service-specific names remain recorded as `[DOCUMENTATION SYNC NEEDED]`.
- The research no longer presents the MVP database topology as an unresolved architecture decision.
- The existing Project/Membership/Team product unknowns and state-model decision boundaries were not changed.

### Evidence

- `docs/decisions/decision-register.md:382-420` — DEC-011 is `ACCEPTED`; DEC-1A accepts MongoDB 7.0 as the operational source of truth and DEC-1B accepts shared `continuum_db` for the MVP Modular Monolith.
- `docs/adr/ADR-002-persistence-and-source-of-truth-ownership.md` — ADR-002 status is `ACCEPTED`.
- `docs/decisions/decision-register.md:549-556` — decision summary lists DEC-011 as accepted.
- `docs/architecture/gaps.md` and `.sage/inventory/*` — historical source/inventory references still contain service-specific topology names and therefore require synchronization.

### Reason

Historical repository references must not be presented as an unresolved architecture decision when the MVP database topology has been formally accepted. The correction records the accepted decision without modifying the ADR, decision register, source configuration, or `.sage` baseline.

## Safety Validation

- Source code changed: `NO`
- Architecture changed: `NO`
- ADR changed: `NO`
- SPEC changed: `NO`
- Decision register changed: `NO`
- `.sage` baseline/inventory changed: `NO`
- Jira changed: `NO`
- Product requirements changed: `NO`
- Business unknowns or decision boundaries resolved: `NO`
