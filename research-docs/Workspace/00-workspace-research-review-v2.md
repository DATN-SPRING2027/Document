# [REVIEW V2] Workspace Research Review

Review date: 2026-09-24

This is the post-correction verification of:

- `01-project-lifecycle.md`
- `02-project-membership.md`
- `03-team-lifecycle.md`
- `04-team-membership-workspace-fe-contract.md`

The review re-checks the corrections identified in `00-workspace-research-review.md` and validates that the original evidence boundaries remain intact. It does not research the whole system again and does not resolve product or implementation decisions.

## Correction Verification

| Correction | Verification | Result |
|---|---|---|
| Index status wording | Project, Project Membership, Team, and Team Membership index rows now use `[PARTIAL]` and explicitly state that runtime index creation and duplicate-write behavior are not verified. | `[PASS]` |
| Generic `/projects` FE test | Project/Workspace FE evidence states that the generic mutation wrapper is scaffolding and that `backend.spec.tsx` uses a mocked `/projects` fixture. It explicitly says this does not prove a Project endpoint, hook, page, or Workspace flow. | `[PASS]` |
| Database topology | Workspace research now records MongoDB 7.0 with shared `continuum_db` as the accepted MVP decision and labels historical service-specific names as `[DOCUMENTATION SYNC NEEDED]`. | `[PASS]` |

## Accepted Architecture Evidence

- `docs/decisions/decision-register.md:382-420` records DEC-011 as `ACCEPTED`, with MongoDB 7.0 as the operational source of truth and shared `continuum_db` for the MVP Modular Monolith.
- `docs/adr/ADR-002-persistence-and-source-of-truth-ownership.md` has status `ACCEPTED`.
- `docs/decisions/decision-register.md:549-556` lists DEC-011 among accepted decisions.
- `docs/architecture/gaps.md` and `.sage/inventory/*` still contain historical service-specific topology references. The corrected research records this as synchronization work and does not alter those files.

# 1. Project Lifecycle Review

## Verdict

`PASS`

## Strengths

- Project fields and `ACTIVE`/`ARCHIVED` schema values remain accurately cited from `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:66-75`.
- The `(organizationId, code)` uniqueness evidence remains present and is now classified as a partial/declaration-only implementation state.
- Project CRUD, search, filter, pagination, sort, archive, restore, authorization, audit, FE behavior, API contract, and tests are covered without claiming that they are implemented.
- The IAM controller/service health-only limitation remains accurately stated.
- The generic FE `/projects` test is now explicitly classified as a mocked mutation scaffold and not a Project feature.
- Accepted database topology is referenced as accepted decision plus documentation sync, not as an open architecture decision.

## Findings

- `[PASS]` Schema fields and Project status are source facts, not lifecycle behavior.
- `[PASS]` Unique index evidence is retained without runtime verification overclaim.
- `[PASS]` No Project controller, service flow, DTO, guard, Project page, Project hook, or Project E2E flow is claimed as present.
- `[PASS]` `activeProjectId` remains correctly described as client-side selection state only.
- `[PASS]` The research continues to preserve Project ownership, archive effects, Restore, API details, and capability mapping as unknown or decision-required.

## Missing Evidence

No missing correction was identified. Source still provides no evidence for Project business endpoints, lifecycle transitions, authorization enforcement, audit wiring, or Project-specific FE flows; the research correctly records these as gaps.

## Unsupported Claims

None material found.

## Conflicts

The historical `continuum_iam` persistence naming versus accepted `continuum_db` topology is now correctly classified as `[DOCUMENTATION SYNC NEEDED]`. It is no longer presented as an unresolved architecture decision.

## Unknown / Decision Required

Project ownership, archive cascade/effects, Restore MVP status, exact authorization matrix, API envelope/errors, and hard-delete exceptions remain unresolved. The correction did not resolve them.

## Scope Issues

None. Authentication, Knowledge, Jira, and SAG remain dependencies/out-of-scope rather than being absorbed into Project Lifecycle.

## Recommended Corrections

None required for the three correction items. Any future change to Project requirements or decisions requires a separate approved research/product change.

# 2. Project Membership Review

## Verdict

`PASS`

## Strengths

- The source membership schema, including `ACTIVE`/`INACTIVE`, `joinedAt`, and scoped IDs, remains accurately cited from `mongodb.schemas.ts:91-100`.
- The `(projectId, userId)` unique index remains evidenced and is now `[PARTIAL]` with runtime behavior explicitly unverified.
- Add, Remove, Update Role, eligibility, cross-project access, Team prerequisite, authorization, audit, FE, API, data, and tests remain covered.
- The source state vocabulary is not silently replaced by the leader vocabulary.
- Invitation acceptance, effective date, role representation, removal semantics, and user eligibility remain unknown/decision-required.

## Findings

- `[PASS]` Membership is correctly described as persistence scaffolding only.
- `[PASS]` Project Membership as a prerequisite for Team Membership is kept as a design rule without claiming backend enforcement.
- `[PASS]` The active Team Membership removal constraint remains a documented rule/gap, not a database constraint.
- `[PASS]` The distinction between `role_assignments` persistence and an implemented membership role mutation remains correct.

## Missing Evidence

No correction introduced or exposed a missing source claim. No membership endpoint, service transition, invitation flow, guard, audit producer, FE member-management flow, or E2E test exists in the reviewed source inventory.

## Unsupported Claims

None material found.

## Conflicts

The mismatch between leader states `ACTIVE`, `INVITED`, `SUSPENDED`, `REMOVED` and source states `ACTIVE`, `INACTIVE` remains explicitly recorded as a decision boundary. It was not resolved.

## Unknown / Decision Required

Canonical membership states, invitation acceptance, effective date, eligibility, role representation, Team Membership consequences, and last-Admin behavior remain unresolved.

## Scope Issues

None. The document does not define a global authorization matrix or absorb Authentication, Knowledge, Jira, or SAG.

## Recommended Corrections

None required for this correction pass.

# 3. Team Lifecycle Review

## Verdict

`PASS`

## Strengths

- Team fields and scope IDs remain accurately cited from `mongodb.schemas.ts:77-88`.
- The `(organizationId, projectId, code)` uniqueness evidence remains present and now uses `[PARTIAL]` declaration wording.
- The absence of Team status, archive metadata, Team CRUD API, service flow, DTO, guard, FE flow, and E2E tests remains correctly reported.
- Team Leader relationship remains unknown; the `TEAM_LEADER` role enum is not treated as proof of a Team leader assignment feature.
- The accepted database topology and historical service-specific names are now handled as accepted decision plus documentation sync.

## Findings

- `[PASS]` Team-to-Project relationship is supported by `projectId`; no foreign-key or runtime referential enforcement is incorrectly claimed.
- `[PASS]` Team Archive/Restore remains a product/implementation gap because the current Team schema has no lifecycle state.
- `[PASS]` Unique index status is no longer overstated as runtime-verified.
- `[PASS]` Team Leader cardinality, representation, and Project Membership prerequisite remain unresolved.

## Missing Evidence

No source evidence exists for Team CRUD/archive transitions, Team authorization, audit wiring, Team FE pages/hooks, Team Membership UI, or Team lifecycle tests. The research correctly records these gaps.

## Unsupported Claims

None material found.

## Conflicts

The historical persistence naming mismatch is now documentation sync, not an open topology decision. Team lifecycle and Team Leader conflicts remain product/implementation unknowns and were not altered.

## Unknown / Decision Required

Team states, Archive/Restore, archive effects, Team Leader relationship/cardinality, Project Membership prerequisite, and case/uniqueness semantics remain unresolved.

## Scope Issues

None. The Team document does not decide Authentication and does not absorb Knowledge, Jira, or SAG.

## Recommended Corrections

None required for this correction pass.

# 4. Team Membership & Workspace FE Contract Review

## Verdict

`PASS`

## Strengths

- Team Membership fields and the lack of a `status` field remain accurately cited from `mongodb.schemas.ts:101-110`.
- The `(teamId, userId)` unique index remains evidenced and is now `[PARTIAL]` with runtime behavior explicitly unverified.
- Project Membership prerequisite, scope, authorization, Team access, audit, API, data, tests, FE pages/hooks, loading/error/empty states, and permission-aware UI are covered without overclaiming implementation.
- BFF routing remains correctly tied to `SPEC-004` and the current FE catch-all route/proxy.
- `activeProjectId` remains a client-only state primitive, not a validated Workspace context.
- The generic `/projects` mocked test is now explicitly labeled as query/mutation scaffolding and not a Workspace feature.

## Findings

- `[PASS]` BFF transport exists, but no Workspace business endpoint exists in the backend.
- `[PASS]` `api-client.ts`, `bff-proxy.ts`, the catch-all route, generic query wrapper, and `activeProjectId` are partial infrastructure foundations only.
- `[PASS]` No Team Membership Add/Remove service, guard, DTO, audit producer, FE flow, or E2E flow is claimed as implemented.
- `[PASS]` FE authorization is correctly treated as UX support; backend enforcement remains the security boundary.

## Missing Evidence

No correction changes the underlying source gap: there is no Workspace response envelope, Workspace error mapping, pagination/filter/sort contract, DTO mapping, permission-aware action state, or FE/BE integration test.

## Unsupported Claims

None material found. The `/projects` fixture is now clearly identified as mocked generic scaffolding.

## Conflicts

- Team Membership state remains unresolved because the leader breakdown names states while the current schema has no Team Membership `status`.
- BFF transport exists while backend Workspace routes do not; this is an implementation gap, not a routing contradiction.
- Browser auth/token handling has a separate FE/IAM conflict; the Workspace research does not attempt to resolve it.

## Unknown / Decision Required

Team Membership states, invitation timing, Project Membership prerequisite details, API envelope/errors, pagination/filter/sort, optimistic concurrency, and permission-aware UI behavior remain unresolved.

## Scope Issues

None. The document remains limited to Team Membership and the Workspace FE/BE contract.

## Recommended Corrections

None required for this correction pass.

# Traceability Matrix

| Research File | Claim | Source | Classification after correction | Result |
|---|---|---|---|---|
| 01-project-lifecycle.md | Project schema and status values exist | `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts:66-75` | `[FACT]` / `[PARTIAL]` capability | `[PASS]` |
| 01-project-lifecycle.md | Organization-scoped Project code uniqueness is declared | `DATN-BE/src/services/iam/infrastructure/persistence.ts:21-22` | `[PARTIAL]` declaration/runtime unverified | `[PASS]` |
| 01-project-lifecycle.md | FE `/projects` test is generic mocked scaffolding | `DATN-FE/src/lib/queries/backend.ts`, `backend.spec.tsx` | `[PARTIAL]` | `[PASS]` |
| 01-project-lifecycle.md | MVP topology is shared `continuum_db` | `docs/decisions/decision-register.md:382-420`; ADR-002 | `[ACCEPTED DECISION]` | `[PASS]` |
| 02-project-membership.md | Membership schema and source states exist | `mongodb.schemas.ts:91-100` | `[FACT]` / `[PARTIAL]` capability | `[PASS]` |
| 02-project-membership.md | Project/user unique declaration exists | `persistence.ts:31-32` | `[PARTIAL]` declaration/runtime unverified | `[PASS]` |
| 02-project-membership.md | Team Membership prerequisite is a design rule | Leader breakdown section 5 | `[DESIGN]` / `[GAP]` | `[PASS]` |
| 03-team-lifecycle.md | Team schema and scoped code declaration exist | `mongodb.schemas.ts:77-88`; `persistence.ts:25-28` | `[FACT]` / `[PARTIAL]` | `[PASS]` |
| 03-team-lifecycle.md | Team lifecycle and Team Leader relation are not implemented/proven | Team source inventory and IAM health-only controller | `[GAP]` / `[UNKNOWN]` | `[PASS]` |
| 03-team-lifecycle.md | Historical topology names need synchronization | `docs/architecture/gaps.md`; `.sage/inventory/*` | `[DOCUMENTATION SYNC NEEDED]` | `[PASS]` |
| 04-team-membership-workspace-fe-contract.md | Team Membership schema and unique declaration exist | `mongodb.schemas.ts:101-110`; `persistence.ts:35-36` | `[FACT]` / `[PARTIAL]` | `[PASS]` |
| 04-team-membership-workspace-fe-contract.md | BFF transport exists | `SPEC-004`; FE BFF route/proxy/API client | `[IMPLEMENTED]` transport / `[GAP]` business routes | `[PASS]` |
| 04-team-membership-workspace-fe-contract.md | Generic `/projects` fixture is not a Workspace feature | `DATN-FE/src/lib/queries/backend.spec.tsx` | `[PARTIAL]` scaffold | `[PASS]` |

# Decision Boundary Audit

The correction pass did not resolve any product or domain decision. These remain unchanged:

- Project Membership canonical states and transitions.
- Team Membership state vocabulary.
- Invitation acceptance and eligibility.
- Effective date semantics.
- Team Leader relationship/cardinality.
- Project/Team Archive and Restore effects.
- Role assignment versus membership-role representation.
- Workspace API envelope, errors, pagination, filter, sort, and concurrency.
- Backend authorization evaluator and audit/outbox behavior.

The only architecture wording corrected was the already accepted MVP persistence topology. Historical repository/inventory references remain evidence of documentation/configuration drift, not an invitation to reopen DEC-011/ADR-002.

# Scope and Safety Validation

- Index declarations are not represented as runtime-verified feature behavior.
- Generic `/projects` mock is explicitly identified as a scaffold.
- Accepted database topology is reflected without modifying architecture governance.
- No UNKNOWN was resolved.
- No DECISION REQUIRED product rule was resolved.
- No Workspace scope was expanded.
- No source code, dependency, database schema, configuration, architecture, ADR, SPEC, decision register, `.sage` baseline, or Jira issue was changed.
- The original four research files retain their evidence references and source paths.

# Overall Review

## Overall Verdict

`PASS`

The correction pass addressed all three findings from the first review. The four Workspace research files now use accurate index-status wording, clearly identify the generic mocked `/projects` test as scaffolding, and correctly reference the accepted MVP database topology while preserving historical documentation-sync findings.

The PASS verdict means the research set is evidence-aligned and safe to use as a reviewed research baseline. It does not mean that Project, Team, Membership, authorization, or Workspace FE/BE features are implemented, and it does not approve unresolved product decisions.

## Critical Findings

- Current source still contains persistence and transport scaffolding rather than complete Workspace business flows.
- Membership state mismatch remains the most important domain decision boundary.
- Team lifecycle state and Team Leader relationship remain unresolved.
- Authorization, audit, invitation, and Workspace API/FE contracts remain gaps or unknowns.

## Decisions Required

The decision-required list is unchanged from the original research. The correction pass did not select any membership state, archive policy, Team Leader model, invitation flow, or API contract.

## Unknowns

All original Project, Membership, Team, Team Membership, API, FE contract, authorization, audit, and archive unknowns remain explicitly preserved in the four research files.

## Ready for Implementation Planning?

YES — as an evidence-reviewed research baseline.

This YES does not authorize implementation or Jira creation. Implementation planning must still respect the preserved decision boundaries and obtain the required human decisions before turning any unresolved item into an implementation commitment.

# Evidence References

- `00-workspace-research-review.md`
- `00-workspace-research-correction-log.md`
- `01-project-lifecycle.md`
- `02-project-membership.md`
- `03-team-lifecycle.md`
- `04-team-membership-workspace-fe-contract.md`
- `product_docs/research-docs/Danh Chia Task.docx`
- `docs/decisions/decision-register.md`
- `docs/adr/ADR-002-persistence-and-source-of-truth-ownership.md`
- `docs/architecture/gaps.md`
- `.sage/inventory/database.md`
- `.sage/inventory/unknowns.md`
- `DATN-BE/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts`
- `DATN-BE/src/services/iam/infrastructure/persistence.ts`
- `DATN-BE/src/services/iam/controllers/iam.controller.ts`
- `DATN-BE/src/services/iam/application/iam.service.ts`
- `DATN-FE/src/lib/api-client.ts`
- `DATN-FE/src/lib/bff-proxy.ts`
- `DATN-FE/src/lib/queries/backend.ts`
- `DATN-FE/src/lib/queries/backend.spec.tsx`
- `DATN-FE/src/stores/client-state.ts`
- `docs/specs/SPEC-004-BFF-ROUTING-ARCHITECTURE.md`
