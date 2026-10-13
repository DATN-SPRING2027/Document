# DATN-89 — C-04 Team Foundation evidence and decision-gap report

## Status and reading boundary

- Revision: **R1, 2026-10-12 (Asia/Saigon)**; document owner: Nguyen Hong Phuc.
- Deliverable: **precise decision-gap report, ready for human review**. This is
  not an approved Team implementation contract. Technical review, Jira completion
  and a documentation merge cannot authorize its proposed Team behavior.
- Jira: [DATN-89](https://trankimthang0207.atlassian.net/browse/DATN-89), with
  [checkpoint/acceptance mapping and validation](10-team-foundation-review-validation.md).
  All six checkpoints form one C-04 deliverable.
- Scope: Document only. No BE/FE, OpenAPI, schema, index, migration, seed or data
  changes; no DATN-90 implementation. Existing records and references are preserved.
- `[APPROVED]`: explicit decision within the cited scope. `[FACT]`: inspected
  source at a pinned revision, not approval or deployment evidence. `[PROPOSED]`:
  research/OpenAPI candidate. `[UNKNOWN]`: an unanswered Team question. A missing
  permission must fail closed; UNKNOWN is not a newly approved business prohibition.

## 1. Authority and evidence map

Document base: `4488b225db41197875a5454f1e02701746aae707` (origin/main).
BE snapshot: `38ef95c0f114daf6c5dca35eb0ce9f41102f1c29` (origin/main).
Both checkouts were clean on main; `pull --ff-only` and fetch succeeded before
the new Document branch was created directly from origin/main. No unmerged
DATN-80/86/93 branch is a base or source of accepted Team policy.

| ID | Source and revision | Authority / inspected scope | Limit |
|---|---|---|---|
| E1 | [DATN-89](https://trankimthang0207.atlassian.net/browse/DATN-89), children DATN-248–253; UI read 2026-10-12 | Task requires explicit Team entity/lifecycle/relationships/actors/API/errors and separation of decisions from research; expected result permits reviewed contract **or** precise decision-gap report | Parent To Do/Nguyen Hong Phuc; children To Do/Unassigned, no description/comments displayed; titles do not approve policies |
| E2 | [DATN-90](https://trankimthang0207.atlassian.net/browse/DATN-90), UI read 2026-10-12 | Implementation requires approved C-04, service ownership, default denial and isolated contract-backed tests | To Do; blocked by DATN-89; blocks DATN-91/92, both To Do; no approval comments displayed |
| E3 | [Actors baseline](../02_ACTORS_ROLES_AND_PERMISSIONS.md) and [Workspace index](00-organization-and-access-contract-readiness.md), Document base above | `[APPROVED]` role vocabulary, tenant hierarchy, explicit scope, parent relationship checks, backend authority and ACL boundary | Detailed Team action codes, delegated child management and leader representation are not selected |
| E4 | [DEC-016 copy](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/docs/decisions/organization-membership-context.md), accepted work package 2026-09-28 | `[APPROVED]` OrganizationMembership proves membership; four states; only ACTIVE establishes context; zero/one/multiple selection | Does not approve Team states or Team APIs; historical shared continuum_db sentence is superseded |
| E5 | [C-01 R5](06-organization-membership-contract.md), merged [PR #23](https://github.com/DATN-SPRING2027/Document/pull/23), squash `e5d05e4a183740f4b33a9605cdb35686906048a5`; [DATN-86](https://trankimthang0207.atlassian.net/browse/DATN-86) read 2026-10-12 | Merged evidence/work record; parent and six children Done; no new approval comments displayed | R2/R3/R5 UNKNOWN snapshots predate E6 and cannot reopen E6's selected Organization policies |
| E6 | Workspace-local WORKING_CONTEXT.md §35; Leader D1–D6 screenshot received 2026-10-06, re-inspected 2026-10-12; requester confirmed “Leader gửi” and reaffirmed in DATN-89 instruction | `[APPROVED]` exact Organization Membership selections in §2 | Screenshot shows 08:08, no sender identity/link or send date. Leader is confirmed by requester; no invented account. Local evidence is outside Git; not Team sign-off |
| E7 | [Schemas](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts), [persistence](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/services/iam/infrastructure/persistence.ts), [database names](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/common/mongodb/database-names.ts) | `[FACT]` Team/TeamMembership fields, declared indexes, IAM ownership in continuum_iam | No live database/index proof, parent integrity, Team lifecycle or authorization from schema declarations |
| E8 | [IAM OpenAPI draft](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/docs/openapi/iam-v1.openapi.json) and [review rules](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/docs/openapi/README.md), `1.0.0-draft` | `[FACT]` seven Team/TeamMembership operation candidates and their DTO/error conventions; §7 transcribes them | `[PROPOSED]` for Team; Project slice acceptance does not accept the Team slice |
| E9 | [Project Foundation decision](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/docs/decisions/project-foundation-read-mvp.md), accepted 2026-09-29/30; [Project Access V1](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/docs/decisions/project-access-visibility-v1.md), accepted 2026-10-02 | `[APPROVED]` Project creation/bootstrap, metadata visibility, Project leadership and member operations | Explicitly excludes Team behavior and nested content ACL; public Project metadata does not grant Team access |
| E10 | [IAM module](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/services/iam/iam.module.ts), [policy](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/services/iam/application/authorization/authorization.policy.ts), [context resolver](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/services/iam/application/authentication/membership-organization-context.resolver.ts), [authentication](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/services/iam/application/authentication/authentication.application.service.ts) | `[FACT]` implemented auth/context and Project/Platform policies; getCurrentIdentity rechecks active User and Organization Membership; no Team controller/service/guard found in src inventory | Existing guards are not Team enforcement; stale token role labels cannot establish a Team grant |
| E11 | [Project Access repository](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/services/iam/infrastructure/mongodb/project-access.repository.ts), removeMember and audit methods | `[FACT]` removal retains membership/assignment, sets INACTIVE; leader revocation prerequisite; Project writes and audit_logs_iam use one session | No TeamMembership query/cascade in removal; Project events/collection selection do not approve Team events/collection |
| E12 | [Team research](03-team-lifecycle.md), [membership research](04-team-membership-workspace-fe-contract.md), [Project membership](02-project-membership.md), [use cases](05-project-team-access-use-cases.md), [IAM design](../../database-design/01_SVC_IAM_SCHEMA.md), Document base above | `[FACT]` dated document content; `[PROPOSED]` Team add/remove, archive/restore, handover and deletion alternatives | “Leader breakdown” provenance inside research is not a separately verified approval of each Team proposal; no current FE audit performed here |
| E13 | Local AGENTDB.md §2/6 and [topology successor](02-database-topology-successor-2026-10-02.md); [generic audit](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/services/iam/infrastructure/audit/audit.service.ts), [outbox](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/services/iam/infrastructure/outbox/outbox.service.ts), [idempotency helper](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/services/iam/infrastructure/redis/idempotency.service.ts) | Existing workflow requires atomic IAM mutation/audit, replica-set proof; current adapters inspected | Canonical ADR-003/SPEC-001 owning revisions unavailable in this checkout; preserve invariant, confirm Team mapping; no Team replay/outbox/history implementation evidenced |

Local E6 evidence: `C:/Users/ASUS/Documents/DATN-handoff-evidence/DATN-86-leader-D1-D6-2026-10-06.png`.
It is not committed or exposed as a repository-relative link. Source inspection
does not claim a running deployment or passing BE/FE/integration suite.

## 2. Approved decisions consumed by C-04

| ID | Approved rule | C-04 consequence and limit |
|---|---|---|
| B1 | E3/E4: Organization is tenant boundary; Team belongs to one Project, Project to one Organization; server checks actual parent IDs | Reject cross-scope access; no Project reassignment/standalone Team policy inferred |
| B2 | E4: OrganizationMembership states exactly PENDING_INVITE, ACTIVE, SUSPENDED, REMOVED; only ACTIVE establishes context | Applies to actor's Organization context, not Team status or TeamMembership state vocabulary |
| B3 | E3/E4: context is not authorization; RoleAssignment does not prove membership; backend evaluates scope/permission/ACL and applicable deny | No FE-selected ID, role title, Project visibility or assignment may bypass membership/ACL |
| B4 | E3: TEAM_LEADER acts only in explicitly assigned/delegated scope; ADMIN/platform authority alone does not grant Team administration or confidential content | Specific Team action grants remain UNKNOWN; Project scope does not automatically delegate every child Team |
| B5 | E9: Project creation is available to authenticated active Organization members in trusted context; PRIVATE Project + ACTIVE creator ProjectMembership + scoped MEMBER bootstrap, atomic with audit | Creator is not implicitly Team Leader/owner/Team member; no Team is created; no project.create grant gate reinstated |
| B6 | E3/E13: governance mutations require audit; IAM mutation/audit atomicity must be preserved; secrets and protected content excluded | Exact Team event/collection/reason/retention/history DTO remains UNKNOWN; eventual audit is not an optional replacement |

### Leader D1–D6: Organization scope, already selected

These are E6 decisions, newer than C-01 R2/R3/R5 records. Do not ask the Leader
to choose them again and do not promote entire historical alternatives as approved.

| Decision | Selected Organization Membership policy | Remaining detail / Team limit |
|---|---|---|
| D1 | Invite existing account by exact email; recipient authenticates and accepts; limited auth flow for recipient without Organization context | Account source, safe lookup, exact identity binding/DTO remain unspecified; no Team invitation rule selected |
| D2 | Seven-day, single-use invitation; resend invalidates old link; cancel PENDING_INVITE → REMOVED; expiry alone does not change state; delivery failure never activates | Replay/error/storage details still need C-01 refinement; do not set Team invite TTL/state from this |
| D3 | Keep four Organization states; ADMIN manages invite/suspend/remove/resume with reason; no self suspend/remove or loss of last ADMIN; reinvite reviews/invalidates old rights | Exact command/action-code and concurrency mechanics not stated; not Team role/cardinality/last-leader rules |
| D4 | Normal removal follows handover; emergency may suspend before handover; retain data; deny Organization access at next check after suspend/remove; resume reviews rights; rejoin does not restore Project/Team rights automatically; no PLATFORM_OPERATOR last-ADMIN bypass | Stored child-record reconciliation, in-flight work and cross-domain handover mechanisms remain dependent decisions; no Team cascade chosen |
| D5 | Separate command APIs; server authorization; Idempotency-Key and version/ETag; selected HTTP error family | Exact Organization endpoints/DTO/replay/preconditions remain unlisted; no Team Idempotency-Key/ETag policy automatically inherited |
| D6 | Audit all membership changes; IAM mutation/audit atomic, audit failure rolls back; email after commit via outbox; exclude token/password/private content | Exact event/collection/outbox ownership/retry remains unspecified; Team email/outbox consumer not selected |

Organization API details remain with C-01; this report does not declare DATN-87
ready. Project Access V1 separately accepts ACTIVE/INACTIVE Project membership
add/removal and Project leader appointments. Those decisions are not open again,
and do not approve Team membership semantics or Team leader representation.

## 3. DATN-248 — Team entity and validation

All storage cells below are `[FACT]` E7. API cells are `[PROPOSED]` E8, not an
approved data model change or implemented input validation.

| Field / identifier | Current storage evidence | Draft wire contract / unresolved validation |
|---|---|---|
| _id / id | Mongoose default _id; ObjectId storage model | Team response id is nonempty string; public IDs opaque. Mapping and malformed-ID errors need TQ-07/08 |
| organizationId | Required ObjectId | Response ResourceId; omitted from create/update body; trusted resolution and parent-match validation required by B1–B3 |
| projectId | Required ObjectId | Create/list path parameter; response ResourceId; Team move/update-parent policy UNKNOWN (TQ-04) |
| name | Required String, trim | Draft length 1–200; whether trim precedes length, Unicode/blank handling and name uniqueness UNKNOWN (TQ-01) |
| code | Required String, uppercase + trim; unique index declaration (organizationId, projectId, code) | Draft pattern `^[A-Z][A-Z0-9_-]{1,31}$` (2–32 chars). Pattern/length absent from storage schema; reject vs normalize and mutability require TQ-01/04 |
| description | Optional String | Draft create String ≤2000; response/update String or null ≤2000. Missing/null/clear semantics require TQ-01/07 |
| createdAt, updatedAt | Team schema timestamps:true | Draft UTC ISO-8601 with trailing Z; client cannot supply them in draft requests; serialization/clock rules need API review |
| status, archive metadata, createdBy/owner/leaderId | No explicit fields in Team schema | No Team enum, creator bootstrap, leader reference or archive metadata approved (TQ-02/05/06) |
| version / ETag | No explicit Team concurrency field or API precondition | ODM metadata is not an approved version contract (TQ-09) |

Strict schema and ObjectId types do not establish API allowlists, foreign keys,
existence checks or authorization. Declared uniqueness is not evidence that an
environment created the index. Duplicate code error/retry behavior is TQ-08/09.

## 4. DATN-249 — Team Membership

`[FACT]` E7: team_memberships stores required ObjectId organizationId, projectId,
teamId, userId and required Date joinedAt, with default _id and strict:true.
It has no explicit status, role, leader, leave/rejoin metadata or timestamps:true.
Unique (teamId, userId) is declared; no live index or membership CRUD is verified.

| Rule or operation | Established boundary | Missing Team decision |
|---|---|---|
| Parent eligibility | E3 hierarchy/access boundary requires eligible Project membership before effective Team access; E8 proposes ACTIVE ProjectMembership on add | Exact add-time actor/target checks, invitation/direct-add and initial Team state: TQ-03/05 |
| Actor Organization context | B2/B3: authenticated active User + ACTIVE OrganizationMembership; RoleAssignment alone is insufficient | Team membership action grant and target/member projection: TQ-05/07 |
| Add target | Project Access V1 already adds active Organization Users as ordinary Project MEMBER; this is Project-only | Whether Team add requires ACTIVE target User and Organization/Project memberships, and whether actor must be Team member: TQ-03/05 |
| Duplicate membership | Unique pair declaration; one stored pair per Team/User when index enforced | Conflict vs replay, rejoin identity/history and concurrency: TQ-03/08/09 |
| Remove | E8 proposes idempotent DELETE; research proposes historical preservation/handover | Delete vs deactivate, reasons, last-leader/self rules and responsibility transfer: TQ-03/06/10 |
| Parent suspend/remove/rejoin | D4 denies Organization access at next check and forbids automatic restoration of child rights | Do not erase or reactivate Team records automatically; approved storage/access reconciliation required by TQ-03/06 |
| Project removal with Team links | Current Project operation is approved INACTIVE removal; E11 has no Team check | Research removal blocker is not accepted behavior. Choose blocking/coordinated resolution/effective denial mapping before enabling Team flows: TQ-06 |

RoleAssignment stores organizationId, optional projectId, userId, roleId,
roleCode and assignedBy, without teamId (E7). Its unique key is
(organizationId, projectId, userId). No Team-scoped assignment store, membership
role or direct leader field can be invented to fill that gap. Project leader
cardinality accepted in E9 does not decide Team leader cardinality.

## 5. DATN-250 — Team lifecycle and transitions

No Team state machine is approved or implemented in the inspected evidence.
Project ACTIVE/ARCHIVED and Organization four-state enums are separate models.
The following is a decision coverage table, not allowed transitions:

| Operation / transition to review | Evidence | Preconditions, outcome and effects still required |
|---|---|---|
| First create → usable Team | Schema + draft POST; UC-WS-11 proposal | Initial state if any; parent Project eligibility; actor/delegation; no implicit creator leader/member (TQ-02/05/06) |
| Update existing Team → updated Team | Draft PATCH name/description | Mutable fields, code policy, parent lifecycle, no-op/reason and stale writes (TQ-01/02/04/09) |
| Archive/deactivate → unavailable scope | Research/use-case proposal only; no Team field/route | Is operation in MVP; exact states, actor, reason, metadata, reads/writes/child effects (TQ-02/06) |
| Restore → usable scope | UNKNOWN; no candidate OpenAPI operation | Is restore allowed; eligibility, previous rights review, uniqueness conflicts (TQ-02/03/06) |
| Hard delete → absent record | UNKNOWN; DATN-258 title says delete or deactivate, not a choice | Retention, referenced tasks/knowledge/history and recovery; no cascade selected (TQ-02/06/10) |
| Same-state/repeated/illegal/concurrent commands | No Team command semantics | Accept/no-op/conflict, idempotent response/audit and concurrency conditions (TQ-08/09/10) |

No supported archive API, lifecycle enum or transition is claimed. Once an
authority selects the model, enumerate every state × command cell with actor,
preconditions, resulting state, error, child effects and audit before DATN-90.

## 6. DATN-251/252 — Relationship and authorization

`[APPROVED]` B1 fixes Organization → Project → Team containment: one Project per
Team, one Organization per Project, tenant consistency checked server-side.
Multi-team Project MVP is established; exact limits, Team moves, leader count,
User participation across Teams, and delete/archive cascades remain TQ-02–06.
Unique membership pair only constrains duplicate rows, not product cardinality.

| Actor / evidence | Approved boundary | Team endpoint grant readiness |
|---|---|---|
| PLATFORM_OPERATOR only | Platform scope, no Team membership/content/admin grant | Deny by authority alone; holding another authority requires independent evaluation |
| Organization ADMIN only | Organization administration; no default Team configuration/member/content rights | Team grant UNKNOWN; Project metadata exception is not nested Team access |
| TEAM_LEADER with Project assignment | Explicit assigned scope; no self-escalation or automatic child delegation | Exact Team action permissions and child scope delegation TQ-05; project.members.* is Project-only |
| TEAM_LEADER with supposed Team assignment | Team scope cannot imply siblings/whole Project | Representation absent in E7; TQ-05 must define valid evidence before any allow |
| MEMBER / Project creator | Membership + scope + ACL; Project bootstrap grants MEMBER only | No Team management grant by role/creation; Team metadata read/list policy TQ-05/07 |
| SME / KNOWLEDGE_OWNER / SUCCESSOR | Scoped assignments, no inherited predecessor or broad admin rights | Resource ACL remains independent; assignment does not prove Organization/Team membership |

For any future Team operation: authenticate/revalidate User; establish ACTIVE
Organization membership and trusted context; resolve actual Project/Team path;
check required parent/member lifecycle eligibility; resolve the approved action
permission and explicit assignment/delegation; apply resource ACL and applicable
deny before read/search/pagination or mutation. Missing/UNKNOWN evidence must
refuse access. This is a security boundary, not a newly selected Team allow matrix.

`[FACT]` E10 implements Project/Platform policies and active Organization checks;
it has no Team action code/guard. No Team permission code, Role.permissions seed
or schema change is approved here. Public Project metadata read rights and
ADMIN Project metadata visibility do not expose Team membership or content.
Team metadata ACL/projection and detailed 403/404 concealment remain TQ-05/07/08.
Existing [OpenAPI structural tests](https://github.com/DATN-SPRING2027/DATN-BE/blob/38ef95c0f114daf6c5dca35eb0ce9f41102f1c29/src/contracts/iam-openapi.spec.ts)
reference Team schemas/list operations; Project bootstrap tests assert no Team
creation. Neither is Team command, lifecycle or authorization runtime coverage.

## 7. DATN-253 — API evidence, not a frozen Team API

All seven rows are `[PROPOSED]` E8, transcribed from the pinned BE draft.
Organization context is resolved through authenticated server context; these
paths carry parent/target IDs, not a new Organization selector transport.

| Method / path | Request | Success DTO/status | Draft error statuses |
|---|---|---|---|
| GET /api/v1/iam/projects/{projectId}/teams | projectId, page, pageSize | 200 TeamList | 401/403/404/422/429 |
| POST /api/v1/iam/projects/{projectId}/teams | CreateTeamRequest | 201 Team | 401/403/404/409/422/429 |
| GET /api/v1/iam/teams/{teamId} | teamId | 200 Team | 401/403/404/429 |
| PATCH /api/v1/iam/teams/{teamId} | UpdateTeamRequest | 200 Team | 401/403/404/409/422/429 |
| GET /api/v1/iam/teams/{teamId}/memberships | teamId, page, pageSize | 200 TeamMembershipList | 401/403/404/422/429 |
| POST /api/v1/iam/teams/{teamId}/memberships | CreateTeamMembershipRequest | 201 TeamMembership | 401/403/404/409/422/429 |
| DELETE /api/v1/iam/teams/{teamId}/memberships/{membershipId} | teamId, membershipId; no body | 204, absent membership; containing Team must exist | 401/403/404/429 |

### DTO and query inventory

- CreateTeamRequest: required name/code, optional string description; limits in
  §3. UpdateTeamRequest: name and nullable description only; at least one property.
  Both additionalProperties:false; no org/project/role/status/leader supplied in body.
- Team: required id, organizationId, projectId, name, code, createdAt, updatedAt;
  optional nullable description; additionalProperties:false. No Team status/leader.
- CreateTeamMembershipRequest: required userId ResourceId; no other properties.
  TeamMembership: required id, organizationId, projectId, teamId, userId, joinedAt;
  additionalProperties:false. No membership status/role.
- Both lists: `{data: [...], pagination: {page, pageSize, totalItems, totalPages}}`.
  Draft page defaults 1, pageSize 20, integers ≥1, pageSize ≤100; totals integers ≥0.
  No Team search/filter/sort/archived selection is defined. Stable order, total
  visibility, empty/out-of-range pages and query allowlist remain TQ-07.
- ResourceId is opaque nonempty string, not a public ObjectId format guarantee.
  UtcTimestamp requires date-time with trailing Z. HTTP malformed-ID validation
  and body whitespace/null behavior remain TQ-01/07/08.
- E8 general security lists bearerAuth or continuum_access cookieAuth. This
  does not approve Team grants, a new token flow, or a Team-specific BFF mapping.
  Browser → BFF → Gateway → owning service boundary is retained; FE integration
  and header transport must follow its own reviewed contract/workflow.

### Errors, concurrency and retries

E8's shared ErrorResponse requires code, message, details object and requestId,
with no additional top-level fields. Shared responses describe 401 invalid/missing
authentication, 403 insufficient scope permission, 404 absent/invisible resource,
409 uniqueness/current-state conflict, 422 validation, and 429 rate limit.
429 proposes Retry-After and X-RateLimit-Limit/Remaining/Reset headers; no Team
rate/window or Team problem code is selected. No Team-specific 500/audit-failure
mapping is defined. Exact concealment, malformed-ID, inactive context, duplicate,
illegal transition, stale write and error precedence require TQ-08.

There is no Team Idempotency-Key, ETag, If-Match, replay storage, fingerprint,
retention, retry/no-op rule or precondition status in E8. DELETE's draft
idempotent absence claim does not define record retention or safe authorization
on replay. D5 selected these mechanisms for Organization Membership, not Team.
The Redis claim helper is scaffolding and does not prove response replay or
transactional duplicate protection. TQ-09 must resolve Team requirements, including
parent membership/role changes between authorization and write; do not invent
409/412/428 behavior or silently use last-write-wins.

## 8. Audit, history and downstream limits

B6 preserves mandatory audit and existing IAM/audit atomicity; Team mutation
failure must not be accepted with a missing required audit. E11 proves a Project
session-bound audit pattern, not Team wiring. Generic AuditService writes
audit_logs without a session argument; OutboxService also lacks a session input.
Neither adapter alone demonstrates the required atomic Team boundary.

Team action/target vocabulary, collection selection, teamId representation,
before/after fields, reason, correlation, rejected-attempt events, duplicate
command audit behavior, retention and history read permission/DTO are UNKNOWN
(TQ-10). No Team history endpoint or event consumer is evidenced. D6's after-commit
email outbox is Organization invitation policy; do not create Team email/events
or delivery/consumer guarantees without an approved need and contract.

DATN-90 remains dependent on approved Team policy + exact API/persistence review;
this gap report cannot clear it. DATN-91 FE and DATN-92 Team Membership BE remain
downstream of DATN-90 per E2. Task/Work Note/knowledge/SAG/handover use owning
API/event and ACL contracts; no direct IAM/Task DB access, cascade, reassignment
or automatic permission inheritance is authorized. Unmerged DATN-93 Task
proposals do not settle transfer, task Team cardinality or lifecycle.

Any future field/index/validation/relationship change needs the separate DB
branch/PR, compatibility/backfill/rollback review and environment authorization
from AI_WORKFLOW/AGENTDB. BE and FE work follow their separate workflows after
approved dependencies merge; no database rollout or team notification here.

## 9. Differences to review before behavior changes

| Difference | Current evidence versus older document/proposal | Consequence |
|---|---|---|
| Organization decisions | C-01 R2/R3/R5 UNKNOWNs predate selected D1–D6 | §2 records exact selected policy; unresolved exact API mechanics remain separate; no repeated policy-choice request |
| IAM implementation | Old Workspace/Governance research says health-only/no guards/Project APIs; E9–E11 now contain Project Foundation/Access and active context enforcement | Dated findings retained as history; they are not current BE facts or Team grant evidence |
| Team paths | Research target /api/v1/teams/* differs from E8's /api/v1/iam/... | Use exact draft inventory; authority must freeze paths, not infer from SRS/BFF examples |
| Validation | Draft name/code/description restrictions are stronger than Team storage schema; PATCH omits code; schema uppercases/trims | TQ-01/04/07 decide validation/mutability/normalization; no silent schema/API change |
| Membership removal | Draft DELETE suggests absence; research suggests retention/handover; no Team status exists | TQ-03/06/10 resolve representation and history before DATN-92 or DATN-258 behavior |
| Parent removal | Research suggests active Team links block Project removal; E11 sets INACTIVE without Team queries | TQ-06 must reconcile future Team access and coordination; no change to accepted Project operation in this task |
| Leadership/scope | Approved explicit Team scope direction, but RoleAssignment lacks teamId; Project Access V1 defines Project leaders only | TQ-05 needs Team evidence/delegation/representation; do not infer new role or modify assignment schema |
| Lifecycle | Team archive/restore proposed; no state/route; Project ARCHIVED fail-closed rule is Project Access V1 scope | TQ-02/06 decide Team operations/child effects; no copied Team enum/cascade |
| Audit/topology | Historical shared continuum_db and “zero producers” findings; current continuum_iam + continuum_audit and transactional Project producer | Preserve current ownership/atomicity; TQ-10 establishes Team mapping; no generic sessionless adapter substitution |

## 10. Precise Team decision gaps

All TQ items are `[UNKNOWN]`. Required authority domains below describe the
review needed, not assigned people. **The authorized Team product approver and
final sign-off roster are UNKNOWN; requester must identify them.** Leader is
confirmed for D1–D6, not automatically assigned every Team decision. IAM/API,
Security, Architecture/DB and affected domain owners must validate their parts;
no new Jira assignments or decision tickets have been created.

| ID | Exact question to close | Required authority domains | Dependent scope |
|---|---|---|---|
| TQ-01 | Which Team fields are required/mutable; name/code/description bounds, blank/Unicode handling, reject vs trim/uppercase, null clear semantics, name uniqueness and code uniqueness scope? Confirm schema/draft differences explicitly. | Team product authority + IAM/API; DB validates constraints | DATN-248/253; DATN-254/255/256 |
| TQ-02 | Are archive/deactivate/hard delete/restore in MVP? Select exact state vocabulary, initial state and complete state × command outcomes, actors/reasons, same-state behavior, retention and recovery. | Team product authority + IAM/API + Security; DB/domain impact review | DATN-250; DATN-255/256/258 |
| TQ-03 | Does Team add directly admit eligible Project members or use a separate invite? Exact target/actor membership eligibility, initial state, leave/remove/rejoin representation, duplicate/rejoin identity, historical rights review and participation limits? Do not reselect Organization D1–D4. | Team product authority + IAM/auth + Security; DB | DATN-249; DATN-92; DATN-255 if bootstrap selected |
| TQ-04 | Can a Team move Projects/Organizations or change code? If allowed, which invariant, audit, reference/history and permission checks apply; how many Teams per Project and memberships per User are allowed? One Project per Team is already B1. | Team product authority + IAM + DB; affected references' owners | DATN-251/248; DATN-254/256 |
| TQ-05 | For create/list/detail/update/archive/restore/delete/member list/add/remove/leader appointment, what exact permission, actor membership, assignment representation and scope apply? Does Project leadership delegate child Team actions; how is Team-only authority represented, who appoints it and what cardinality/self/last-leader limits apply? | Team product authority + Security/authorization + IAM/API; DB if representation changes | DATN-252/249; every DATN-90 API, DATN-91/92 |
| TQ-06 | On Team archive/remove, Project archive/member removal and Organization suspend/remove/resume/rejoin, what stored records remain/change, what effective access is denied, who transfers responsibilities, and what failure/order/recovery apply? Does future Team linkage block Project removal or use coordinated resolution? Preserve D4 and accepted Project V1; changes require owning workflow approval. | Team/Project/Organization product authorities + IAM/Security + Task/knowledge/handover owners; architecture/DB | DATN-250/251/249; DATN-258/92 and downstream consumers |
| TQ-07 | Freeze method/path, DTO, success body/status, query allowlist/page bounds/stable sort/filter/search/totals/empty semantics and field/PII visibility for each enabled Team operation. Accept/amend/defer each E8 candidate; confirm context/CSRF/header/BFF transport in owning contract. | IAM/API + Team product authority + Security; FE review | DATN-253; DATN-255–257, DATN-91/92 |
| TQ-08 | Per operation, what exact status/problem code/details and precedence apply to auth failure, inactive context, malformed IDs, wrong parent, missing/invisible Team/member, duplicate/state/stale conflict and audit/internal failure? Decide 403/404 concealment specifically for Team. | Security + IAM/API + Team product authority; FE | DATN-253; DATN-259 and FE errors |
| TQ-09 | Does Team require Idempotency-Key and version/ETag; for which commands and scopes? Define fingerprint/replay/TTL/in-flight/key reuse, preconditions/error status, atomic duplicate safety and authorization revalidation/fence against concurrent membership/role/parent changes. D5 is Organization scope only. | IAM/API + Security + architecture/DB; Team product authority for observable outcomes | DATN-253; mutations/tests in DATN-90/92; separate DB work if needed |
| TQ-10 | Confirm canonical ADR-003/SPEC-001 revisions and exact atomic Team audit mapping without weakening B6. Which collection/action/target/reason/diff/correlation/retention and history read policy; rollback/retry/dedup/denied-attempt behavior? Is an async Team consumer needed; if so who owns outbox/delivery? | Architecture/DB + IAM + Security; Team product authority; relevant async/history domain owner if chosen | DATN-253/250/249; DATN-90/92 audit/history/replica-set checks |

For every resolution record: exact selected rule, approval authority and evidence,
date/revision, affected TQ/B/API/state/validation rows, owning repository contract,
DB impact and acceptance scenarios. Partial approval enables only its explicitly
accepted scope; unknown Team operations remain unimplemented and fail closed.
