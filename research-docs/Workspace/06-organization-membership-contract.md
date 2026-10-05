# DATN-86 — Organization Membership lifecycle and API working contract

## Status and authority

- Revision: **R3, 2026-10-05 (Asia/Saigon)**; owner: Nguyen Hong Phuc.
- R2 applies the user-approved P2 correction preserving the existing IAM/audit
  atomicity requirement; this approval is not a product/lifecycle contract sign-off.
- Status: **Working contract for human review; lifecycle/API decisions incomplete**.
- R3 adds a [decision worksheet with concrete alternatives, API examples and
  validation cases](07-organization-membership-review-worksheet.md). None is an
  accepted lifecycle/API policy; the approved baseline and UNKNOWN grid stay intact.
- Jira: [DATN-86](https://trankimthang0207.atlassian.net/browse/DATN-86).
  Expected result is a **reviewed Organization Membership contract for implementation**.
  This draft, its question register, technical checks, or an agent diff review do
  not satisfy that result or authorize DATN-87/DATN-88 implementation.
- Scope: preserve accepted membership/context rules, reconcile current IAM
  evidence, and identify exact decisions needed for the administration contract.
  No application, schema, index, migration, seed, or data change is included.
- Labels: `[APPROVED BASELINE]` is an explicitly accepted rule within its stated
  scope; `[FACT]` is current source evidence, not product approval; `[PROPOSED]`
  is a candidate for review; `[UNKNOWN]` requires the named authority and record.
  An unknown transition is neither an approved allow nor an approved business deny.

This extends the [Organization/Workspace decision index](00-organization-and-access-contract-readiness.md),
particularly DEC-ORG-03/05, DEC-ACCESS-01/02/06/09/10/14 and DEC-WS-11. The
[Organization Context](../Governance/01-organization-context.md),
[Authorization Foundation research](../Governance/02-role-permission-authorization.md),
and [Audit/Outbox research](../Governance/03-audit-outbox-contract.md) contain
dated inventories and non-binding recommendations. Their older “no resolver/
guards/tests” findings do not describe the current BE snapshot below.

## 1. Initial R1 snapshot and subsequent revalidation

Jira was read directly on 2026-10-05: parent DATN-86 is **To Do**, assigned to
Nguyen Hong Phuc, Medium, without a due date. All six children DATN-229–234 are
**To Do / Unassigned**, with empty descriptions and no comments displayed in
their Comments panels. Parent and linked tickets likewise show no additional
approval comments. Child titles are work items; no separate child AC was present.

| Relationship | Verified scope and status | Contract consequence |
|---|---|---|
| DATN-86 blocks [DATN-87](https://trankimthang0207.atlassian.net/browse/DATN-87) | C-02 Organization Membership Administration BE; To Do, Phuc | Implement only accepted operations; authorized, validated, auditable mutations; duplicate/partial-write safety; lifecycle/cross-Organization/audit tests |
| DATN-87 blocks [DATN-88](https://trankimthang0207.atlassian.net/browse/DATN-88) | C-03 Organization Membership FE; To Do, Tien | Accepted API, four states, server denial, list/invite/permitted actions and loading/empty/error coverage |
| DATN-86 relates to [DATN-274](https://trankimthang0207.atlassian.net/browse/DATN-274) | Organization Context Resolution; Done, Danh; references BE PR #7/#8 | Context resolution evidence only; no invitation or mutation approval |

No incoming blocker or DATN-93 link is displayed on DATN-86. DATN-93 / Document
PR #22 is not the base or authority for this contract; its Task product details
remain unapproved. Offboarding cannot depend on those details as settled policy.

All four working trees were clean before work; fetch and main fast-forward pull
succeeded. Document branch `docs/Phuc-datn-86-organization-membership-contract`
was created directly from the fetched Document `origin/main` below.

| Repository | Verified origin/main SHA |
|---|---|
| Document | `654c8b16ecc7c3becdfd29ee2a7fa6ef7f437755` |
| DATN-BE | `56036d13ed86f5db47ba7cbcb02256f02eab80ae` |
| DATN-FE | `c57c01455e7a47f4865485d00ded2c05f7b3b203` |
| sag-laya-integration | `82a8f80bf728ad1c56b08628d4eb392bf55bcb29` |

R2 continued on that branch with both R1 changes intact. Jira was re-read on the
same date: parent moved from To Do to **In Progress** for the approved correction;
children and linked dependency/approval evidence remained as above. Document
origin/main and base were unchanged. After fetch, BE origin/main was
`fc488a7ced952fc51fc4615dff9917d78c118010`, FE unchanged, and SAG origin/main
`0102e1ec003be3f41923c6923f9333ea5875fa23`; source checkouts were not altered.

R3 re-read all six children, parent, DATN-274 and DATN-87/88 on the same date.
Parent was In Review and moved to **In Progress** while preparing R3; DATN-229/230
were In Review and DATN-231–234 In Progress. Each child now has an R2 work record;
no new approval comments or separate accepted child policy was displayed. PR
[#23](https://github.com/DATN-SPRING2027/Document/pull/23) was Open with no reviews
or comments. Dependency links and downstream To Do statuses were unchanged.
Fetched BE origin/main advanced to `1f28bb3143bd216b2a7a107b4ef527ee127baf58`
(A-02 refresh), FE to `e38fe695f1007a9ae2aa15b4e2dc4a5e06f927aa` (auth/BFF changes).
Document base and SAG SHA stayed unchanged; source checkouts were not altered.

R3 also read governance research tickets [DATN-15](https://trankimthang0207.atlassian.net/browse/DATN-15),
[DATN-16](https://trankimthang0207.atlassian.net/browse/DATN-16) and
[DATN-17](https://trankimthang0207.atlassian.net/browse/DATN-17). Their Done statuses
do not approve membership writes: the displayed September research reviews retain
decision/evidence corrections, including audit connection concerns. These dated
comments are neither current runtime evidence nor a replacement for E9's invariant
or canonical authority. No other research report or ticket was changed.

## 2. Source and approval boundaries

E1–E8 remain pinned to the verified R1 BE SHA, not a moving branch. R2 inspected
the newer [A-01 auth/session compilation](https://github.com/DATN-SPRING2027/DATN-BE/blob/fc488a7ced952fc51fc4615dff9917d78c118010/docs/decisions/auth-session-contract-a-01.md)
and its OpenAPI delta: no membership lifecycle/API or runtime change was added;
it does not close the Organization mutation questions below. Local source and
test inspection establish facts; they do not prove a deployment or passing suite.

| ID | Source | Authority / evidence limit |
|---|---|---|
| E1 | [BE DEC-016 copy](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/docs/decisions/organization-membership-context.md) | Accepted by requester for the 2026-09-28 work package; explicitly does not claim separate Product/Security approval; lifecycle writes and future API access rules excluded |
| E2 | [Actors/roles baseline](../02_ACTORS_ROLES_AND_PERMISSIONS.md) and [Workspace readiness](00-organization-and-access-contract-readiness.md) | Accepted high-level actor boundaries; detailed action matrix, invite/transition/error/offboarding policy still open |
| E3 | [BE Authorization Foundation scope](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/docs/authorization-foundation-scope.md) and [policy](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/src/services/iam/application/authorization/authorization.policy.ts) | Default deny/deny precedence; accepted Project creation exception to role/grant gating; no Organization Membership action codes |
| E4 | [IAM OpenAPI](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/docs/openapi/iam-v1.openapi.json) and [review rules](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/docs/openapi/README.md) | Auth/User/Project/Team slice; no Organization Membership administration paths or resource DTO; shared conventions do not approve new operations |
| E5 | [Membership resolver](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/src/services/iam/application/authentication/membership-organization-context.resolver.ts) and [authentication service](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/src/services/iam/application/authentication/authentication.application.service.ts) | Current selection, login result/error and per-request User/membership revalidation; not lifecycle commands |
| E6 | [Authentication repository](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/src/services/iam/infrastructure/mongodb/authentication.repository.ts), [schemas](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/src/services/iam/infrastructure/mongodb/mongodb.schemas.ts), [persistence](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/src/services/iam/infrastructure/persistence.ts) | ACTIVE-only query, required fields, four-state enum and declared pair/query indexes; no live database inspection |
| E7 | [Database names](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/src/common/mongodb/database-names.ts), [Project audit decision](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/docs/decisions/project-audit-collection-mvp.md), [generic audit adapter](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/src/services/iam/infrastructure/audit/audit.service.ts) | IAM runtime `continuum_iam`; cross-cutting `continuum_audit`; Project transaction/collection approval has Project scope; generic adapter writes `audit_logs` without a session argument |
| E8 | [User directory repository](https://github.com/DATN-SPRING2027/DATN-BE/blob/56036d13ed86f5db47ba7cbcb02256f02eab80ae/src/services/iam/infrastructure/mongodb/user-directory.repository.ts) | ACTIVE member directory and global User status update; not Organization Membership list/lifecycle API |
| E9 | Workspace-local `AGENTDB.md` §6 (outside this repository), re-read for R2 | Existing instruction: Project/IAM mutations with audit in `continuum_audit` must preserve atomicity per ADR-003, with MongoDB replica-set commit/rollback proof before cutover. Canonical ADR-003/SPEC-001 authority and exact Organization scope still need verification; no exception or implementation detail is approved here. |
| E10 | R3 [authentication service](https://github.com/DATN-SPRING2027/DATN-BE/blob/1f28bb3143bd216b2a7a107b4ef527ee127baf58/src/services/iam/application/authentication/authentication.application.service.ts), [controller](https://github.com/DATN-SPRING2027/DATN-BE/blob/1f28bb3143bd216b2a7a107b4ef527ee127baf58/src/services/iam/controllers/authentication.controller.ts), [service tests](https://github.com/DATN-SPRING2027/DATN-BE/blob/1f28bb3143bd216b2a7a107b4ef527ee127baf58/src/services/iam/application/authentication/authentication.application.service.spec.ts) | Refresh now re-resolves the persisted owner's selected Organization before signing/rotation; no-context failure returns generic 401 AUTH_REFRESH_INVALID and does not rotate. This does not prove a suspend/remove mutation, concurrency fence, global revocation or deployment. Tests inspected, not executed here. |
| E11 | R3 [IAM OpenAPI](https://github.com/DATN-SPRING2027/DATN-BE/blob/1f28bb3143bd216b2a7a107b4ef527ee127baf58/docs/openapi/iam-v1.openapi.json) | Adds auth refresh; still no Organization Membership administration path/DTO. E5 resolver and E6 OrganizationMembership schema/persistence files are unchanged at this revision. |

E1 references canonical `projects/DATN/docs/decisions/ORGANIZATION-MEMBERSHIP-CONTEXT-DECISION-V1.md`
and `decision-register.md`; AGENTDB references ADR-003 and SPEC-001. Those owning
files were not found in the local GitHub workspace search. The available E1 copy
is used within its stated acceptance scope; obtain canonical revisions when
closing decisions. E1's shared `continuum_db` topology sentence is historical:
current BE AGENTS, AGENTDB and E7 describe database-per-service. It is not a
reason to restore a shared runtime. Frozen `architecture/`, `database-design/`
and `deploy/` remain untouched; reconciliation needs the owning workflow.

## 3. Accepted baseline and actor/scope contract

| ID | Rule | Source / scope |
|---|---|---|
| B1 | `[APPROVED BASELINE]` OrganizationMembership proves User–Organization membership; RoleAssignment alone never proves it. | E1; DATN-86 AC; role evaluation follows context |
| B2 | `[APPROVED BASELINE]` Exactly `PENDING_INVITE`, `ACTIVE`, `SUSPENDED`, `REMOVED`; only `ACTIVE` establishes Organization Context. ONBOARDING/OFFBOARDING are workflows. | E1; no added state or transition approval |
| B3 | `[APPROVED BASELINE]` Zero active memberships: no context; one: auto-select; multiple: explicit selection; server validates a supplied Organization ID against the authenticated User's active membership. | E1; DATN-274 |
| B4 | `[APPROVED BASELINE]` Organization-scoped access checks identity, active membership and trusted matching context, then the operation's approved scope/permission/ACL; client selection/title is not authorization. | E2/E3; invitation redemption exception, if any, requires Q1/Q2 |
| B5 | `[APPROVED BASELINE]` ADMIN administers membership within its Organization; platform authority alone creates no membership/content right; TEAM_LEADER/MEMBER/scoped assignments do not gain Organization administration. | E2; precise permissions/guards and constraints remain Q1 |
| B6 | `[APPROVED BASELINE]` Governance membership/role changes require audit provenance; secrets and protected content bodies must not enter logs. Existing workflow instruction E9 requires IAM mutation + audit in `continuum_audit` to preserve atomicity per ADR-003. | E2/E9; preserve the requirement while canonical authority/scope is reconciled. Collection, event fields, transaction mechanism and failure/retry details remain UNKNOWN in Q7; no exception selected. |
| B7 | `[APPROVED BASELINE]` E1's historical backfill creates missing ACTIVE pairs from eligible Organization-level legacy assignments only, preserves existing records, and requires deterministic/idempotent dry-run and a unique pair index. | Migration-specific exception; never a runtime RoleAssignment fallback, general add/activation policy, or permission to rerun migration here |

| Actor / subject | Established boundary | Still needed before an API grant |
|---|---|---|
| Authenticated Organization ADMIN | Own ACTIVE membership and matching trusted Organization; Organization administration within accepted policy; no default confidential-content access | Q1 action codes/current evidence, target visibility, self/peer/last-admin limits |
| PLATFORM_OPERATOR | Provision Organization / first-ADMIN bootstrap at platform scope | No ordinary membership-management bypass; provisioning/bootstrap contract is separate |
| TEAM_LEADER / MEMBER / scoped assignee | Own membership, explicitly assigned Project/Team/resource scope and ACL | No Organization invitation/suspend/remove authority inferred from Project/Team scope |
| Invite recipient / target User | Membership status is separate from global User account status and actor status | Q2 redemption identity, verification and credentials; a pending recipient has no ACTIVE context |
| Service / AI actor | Least-privilege system identity under E2 | No autonomous grant/activation/offboarding; service participation needs Q1/Q7 authority |

`[FACT]` Current authentication additionally checks User account eligibility.
An ACTIVE membership does not make a suspended account login-eligible. An ACTIVE
member without RoleAssignment can resolve context with `roles: []` (E5); that is
not permission for every operation. The accepted `project.create` membership-only
rule in E3 cannot be generalized to Organization Membership administration.

## 4. Lifecycle: context eligibility is settled; commands are not

| Organization Membership state | Establishes Organization Context | Lifecycle meaning available for implementation |
|---|---|---|
| `PENDING_INVITE` | No | State accepted; invitation creation, verification, expiry, cancel/resend/accept rules UNKNOWN (Q2) |
| `ACTIVE` | Yes, subject to validated identity/selection and separate authorization | Context eligibility accepted; activation authority and source-state rules UNKNOWN (Q1–Q3) |
| `SUSPENDED` | No | Context ineligible; suspend/resume triggers, reason and effects UNKNOWN (Q3/Q8) |
| `REMOVED` | No | Context ineligible; removal/rejoin, retention and effects UNKNOWN (Q3/Q8); no hard-delete/cascade inference |

The complete transition grid intentionally approves no lifecycle write. Every
cell, including same-state retry/no-op, needs an explicit accepted command and
outcome. UNKNOWN is a contract gap, not a fifth stored status.

| From / to | PENDING_INVITE | ACTIVE | SUSPENDED | REMOVED |
|---|---|---|---|---|
| PENDING_INVITE | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| ACTIVE | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SUSPENDED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| REMOVED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

Creation of the first membership record is a separate undecided command, not
a state or transition from a new enum value. The pair index does not settle
whether re-invitation updates a REMOVED row, rejects, or uses another approved
design. Expiry/cancellation/rejection must be decided within the four-state
model; no EXPIRED/CANCELLED/REJECTED membership states may be introduced here.

`[FACT]` E6 queries `{ userId, status: 'ACTIVE' }`, projects Organization IDs,
deduplicates them, and loads existing Organization documents. E5 returns no
context if none exist, validates supplied selection, otherwise auto-selects one
or requests selection for multiple; only then does it load roles. Missing
Organization documents are filtered out. This is current resolver behavior,
not a decision about deleting Organizations or cascading memberships.

## 5. API, payload and validation surface

`[FACT]` E4 has no Organization Membership administration path or DTO. Existing
Project/Team `MembershipStatus` is `ACTIVE/INACTIVE`; it must not be reused as
the Organization enum. E8 lists Users through ACTIVE membership and changes
global User status, with `LAST_ACTIVE_ADMIN` / `SHARED_ACCOUNT_STATUS_CHANGE`
account protections. It neither lists all four membership states nor defines
Organization suspend/remove, and those protections cannot be copied as policy.

The candidate commands below are `[PROPOSED]` review surfaces from DATN-87 and
the readiness register, not enabled APIs. Method/path, success status and DTO
are **UNKNOWN for every row in the accepted contract**; worksheet section 3
provides concrete candidates, not approved replacements. Do not generate
controller/UI contracts from either document until the decision gate is closed.

| Candidate operation | Established constraint | Payload / validation / outcome decisions |
|---|---|---|
| List Organization members | Trusted Organization scope and approved actor; no confidential-content grant | Q1/Q4: four-state visibility, fields/PII, filters/search/sort/pagination and response |
| Invite member | Pending state cannot grant context; actor/target are separate | Q1/Q2/Q5: userId vs email, existing vs new identity, verification, duplicate behavior, delivery and pending record creation |
| Accept invitation / activate membership | Context only after accepted activation; recipient currently lacks ACTIVE context | Q1–Q3/Q5: whether separate commands, credentials/token, actor scope exception, allowed source states, atomic writes and response |
| Resend / cancel invitation | No additional membership state inferred | Q2/Q3/Q5: enabled scope, rate limit, token invalidation, resulting state and retry outcome |
| Suspend / remove member | Resulting non-ACTIVE state cannot establish context | Q1/Q3/Q5/Q8: authorized command, source states, reason, self/last-admin safety, concurrency, linked responsibilities |
| Resume / rejoin | Neither reverse transition nor new invitation is approved | Q2/Q3: enablement, previous-state preconditions and preserved/reissued roles/scopes |

| Data boundary | Verified representation / validation | Organization Membership contract gap |
|---|---|---|
| Stored relationship | `[FACT]` E6: required ObjectId `organizationId`, `userId`; required four-state `status`; strict schema, timestamps; no status default | Q5 final read/write DTO, API identifier validation and reference checks; schema is not an API allowlist |
| Pair / query indexes | `[FACT]` E6 declares unique `(organizationId,userId)` and query `(userId,status,organizationId)` | No live index or constraint proof; Q2/Q3 duplicate/rejoin semantics; DB work remains separate |
| Identity / Organization input | B1/B3/B4 require server-validated actor membership/context; E4 exposes opaque IDs | Q1/Q5 selector placement, target ID vs membership ID, trust/source precedence and malformed/mismatched input outcomes |
| Status / server fields | B2 limits the vocabulary; no approval for generic status PATCH, client actorUserId, role changes or cascade flags | Q3/Q5 command allowlist, unknown-field rejection, writable fields, reasons, lengths, idempotency and version/fence |
| List / response | `[FACT]` E4 conventions: camelCase, opaque string IDs, UTC ISO-8601 timestamps; lists default page=1/pageSize=20, max=100 | Q4/Q5 adopt explicit list DTO, limits, ordering, filters, totals, empty results and permitted PII; no membership response exists |
| Existing login | `[FACT]` E4: required email/password, optional organizationId, additionalProperties=false; email max 320, password 1–1024; runtime DTO uses IsMongoId for selector | Preserve existing auth behavior; Q5 resolves opaque-ID contract vs storage validation for new APIs without changing login |

Any approved write contract must enumerate actor, target, scope, exact accepted
source state, validated fields, success/retry/conflict outcome and audit effect.
No arbitrary request body may become a persistence update or permission source
under the workflow. Concrete fields/limits remain pending Q5 approval.

## 6. Errors and audit boundaries

| Surface | Current evidence / rule | Remaining decision |
|---|---|---|
| Login / current identity | `[FACT]` E5: zero eligible context or invalid login selection gives generic 401 `AUTHENTICATION_FAILED`; multiple choices gives 409 `ORGANIZATION_SELECTION_REQUIRED` with eligible IDs/names; current identity rechecks active User and membership and rejects a stale token with 401 | This implements auth context, not new member-management denial policy or a zero-context session/UI |
| Refresh / selected Organization | `[FACT]` E10/E11: CSRF check precedes token-state access; eligible session owner/account and selected ACTIVE context are resolved before signing/rotation; no-context failure gives generic 401 `AUTH_REFRESH_INVALID`, without rotation | Not an invitation-recipient authentication route or proof of mutation-time fencing, in-flight cancellation, cache propagation or full revocation; Q1/Q2/Q6/Q8 remain open |
| Body validation | `[FACT]` Login validates a whitelist and rejects extra fields with 422 `VALIDATION_FAILED`; E4 documents 422 field/business validation | Q5/Q6 exact validation/error details for each membership command |
| Scope / resource denial | B4 denies access without matching active scope; E4 has 403 permission and 404 absent/not-visible responses | Q6 explicit mapping for inactive actor, cross-Organization target, nonexistent membership and invite failure; no blanket 403/404 choice |
| Duplicate / lifecycle / concurrency | E4 contains 409 conflict convention, not Organization Membership outcomes | Q2/Q3/Q6 duplicate invites, stale state/version, illegal transition, same-state retry and partial failures |
| Envelope / limits | `[FACT]` E4 error shape requires `code`, `message`, `details`, `requestId`; documented 429 rate-limit response | Q6 exact codes, safe details, retry headers and precedence; no new code names or rates approved |

B6 and DATN-87 require auditable, partial-write-safe mutations. The Organization
contract must also preserve E9's existing IAM mutation/audit atomicity requirement.
Missing canonical ADR-003/SPEC-001 authority and exact Organization applicability
are a **reconciliation blocker**, not permission to reopen atomicity as an optional
choice. Any exception remains blocked pending an explicit owning-authority decision.
Q7 still needs the canonical scope and approved collection, event names, target
identifiers, changed fields, reason rules, correlation, append-only handling,
transaction mechanism/boundary and failure/retry semantics; these details remain
UNKNOWN. Audit payloads must exclude passwords, invitation/
session tokens, two-factor secrets and protected content bodies.

`[FACT]` E7's accepted Project-create contract writes domain/bootstrap data to
`continuum_iam` and audit to `continuum_audit.audit_logs_iam` in one session/
transaction. Its approval explicitly does not settle every module's audit choice.
The generic AuditService writes `audit_logs` without a session parameter. Neither
adapter existence nor Project approval settles Organization-specific implementation
details or overrides E9. Do not substitute eventual audit or assume the adapter is
sufficient. No async invitation/offboarding consumer, outbox envelope or delivery
guarantee is approved by this artifact; Q2/Q7/Q8 must identify any such consumer.

## 7. Decision register — all questions remain UNKNOWN

The [R3 review worksheet](07-organization-membership-review-worksheet.md) turns
these questions into alternatives and per-command/API/test review records. It
does not close a Q item; choose, amend or explicitly defer each candidate with
the owning authority before promoting it into this accepted contract.

Authority below names required roles, not invented reviewer accounts. Phuc is
the verified contract/BE owner, Danh the context implementer/reporter, and Tien
the FE owner; Product/Security/architecture authority and final sign-off roster
must be confirmed. Each answer needs an exact accepted rule, approver, date,
owning decision revision and affected OpenAPI/schema/test mapping. Technical
review or merging this document cannot fill that record.

| ID | Specific decision to record | Source / authority needed | Blocked scope |
|---|---|---|---|
| Q1 | For each list/invite/activate/suspend/remove command, what current role/permission evidence, actor ACTIVE context and target scope are required? Can an invite recipient redeem without ACTIVE context, under which narrowly scoped identity proof? What self/peer/last-admin rules apply? | E2; DEC-ACCESS-09; Product + Security/authorization owner, with IAM owner | DATN-233; DATN-87 authorization; DATN-88 controls |
| Q2 | Is onboarding invite-only? Invite existing userId, email/new account, or both? Who may accept vs activate? What verification/token binding, expiry, resend/cancel/replay/duplicate/rate/delivery rules and resulting four-state outcomes apply? Does failed delivery retain a pending row? | E1 excludes writes; DEC-ORG-05; Product + IAM/auth + Security; Notification owner if involved | DATN-231/233; invite/activation BE and FE |
| Q3 | For all 16 transition cells and first creation, which commands are enabled, by whom, from which state, with which reason and same-state/retry/conflict outcome? Are resume/rejoin enabled; how are REMOVED pair uniqueness and roles handled? | E1; DEC-ACCESS-06; Product + IAM owner + Security; DB owner validates chosen representation | DATN-232/234; activation/suspend/remove BE; FE actions |
| Q4 | Who may see each membership state and which member/User fields? What exact list filters, search, sort, paging, totals, empty-result and PII visibility rules apply? | E4/E8; DEC-ACCESS-14; Product + IAM/API + Security; FE review | DATN-233; member list BE/FE |
| Q5 | What method/path and request/response/success status apply to every enabled command? Which IDs/selectors are accepted and how validated? What allowlist, required/optional fields, limits, reason format, reference checks, idempotency key and stale-write/version/fence rules apply? | E4/E6; DEC-ACCESS-01/14; IAM/API + Product; DB and FE consistency review | DATN-233/234; DB contract if needed, DATN-87/88 integration |
| Q6 | Which status/code/details and precedence apply to unauthenticated, inactive actor, cross-Organization/not-visible/missing target, malformed payload, invite token failure, duplicate/illegal/stale transition, retry and audit failure? How does context selection/refresh/cache invalidation behave after membership changes? | E4/E5; DEC-ACCESS-02/10; IAM/auth + Security + API/FE owners | DATN-233/234; error tests and FE UX; revocation/caching |
| Q7 | Obtain the canonical ADR-003/SPEC-001 authority/revision and confirm the exact Organization scope of E9's existing IAM mutation/audit atomicity requirement; preserve it while unresolved, with any exception blocked. Which collection/action/target/before-after/reason/correlation fields, transaction mechanism/boundary, audit-failure rollback and deduplication/retry behavior implement it per command and rejected attempt? Are async consumers/outbox required; who owns delivery and retention? All specific details remain UNKNOWN. | E2/E7/E9; canonical authority/scope reconciliation blocker; architecture/DB + IAM + Security owning approval | DATN-233/234; auditable/partial-write-safe BE and integration tests; no optional eventual-audit alternative inferred |
| Q8 | On suspend/remove, which child memberships/roles/grants/sessions/caches remain stored, lose effective access, or change? What happens to Project/Team leadership, Task assignment, Work Note/knowledge ownership, SME/SUCCESSOR and handover responsibilities? Who transfers/unassigns, with what order/failure recovery, and what changes on resume/rejoin? | DEC-WS-11; Product + IAM + Project/Team/Task/knowledge/handover owners, Security; accepted contracts for each domain | DATN-232/234; offboarding/cascade BE and FE; dependent domains |

B2/B4 settle the parent access gate: a non-ACTIVE parent cannot establish
Organization Context. They do not settle how stored descendants, responsibilities,
already-running requests/jobs, issued tokens, or caches are reconciled. Q8 must
preserve that access boundary without inventing cascade/delete/transfer behavior.
Task effects require the eventual accepted Task contract, not DATN-93's draft.

## 8. Acceptance mapping and validation evidence

| DATN-86 child | Coverage in this revision | Evidence / unresolved acceptance |
|---|---|---|
| [DATN-229](https://trankimthang0207.atlassian.net/browse/DATN-229) — Define Organization Membership states | B2; section 4 exact enum/context table | E1/E6; enum preserved; no new state |
| [DATN-230](https://trankimthang0207.atlassian.net/browse/DATN-230) — Define ACTIVE membership semantics | B1/B3/B4; sections 3/4/6 context vs roles/account/HTTP | E1/E5/E6; baseline settled; new operation grants/transport/error policy still Q1/Q5/Q6 |
| [DATN-231](https://trankimthang0207.atlassian.net/browse/DATN-231) — Define Organization invitation behavior | Candidate surfaces, Q2; worksheet section 1 identity/activation/delivery alternatives | Invitation contract not approved; Q1–Q3/Q5–Q7 required |
| [DATN-232](https://trankimthang0207.atlassian.net/browse/DATN-232) — Define suspend and remove semantics | Context denial; UNKNOWN grid; worksheet section 2 command/transition/effect alternatives | Commands, reasons, safeguards, revocation/descendant effects unresolved |
| [DATN-233](https://trankimthang0207.atlassian.net/browse/DATN-233) — Define Membership API contract | Sections 3/5/6; worksheet section 3 candidate paths/DTO/errors and section 4 audit gate | Concrete proposal available for review; exact API not frozen/build-ready |
| [DATN-234](https://trankimthang0207.atlassian.net/browse/DATN-234) — Validate lifecycle rules | UNKNOWN grid; scenarios below; worksheet section 5 detailed review cases and section 6 decision record | Documentation consistency can be checked now; accepted lifecycle outcomes and runtime verification remain pending Q1–Q8 |

| Parent acceptance criterion / result | Assessment |
|---|---|
| Preserve four states and context eligibility exactly | Documented by B2/section 4 against E1; no lifecycle write inferred |
| RoleAssignment is not membership evidence | B1/B7 and resolver separation; historical migration exception is explicit |
| Document payloads, validation and unresolved policy without new states | Sections 5–7 distinguish current facts and unknown new API semantics |
| Reviewed Organization Membership contract for implementation | **NOT MET**: no human contract sign-off or accepted answers to Q1–Q8 in the inspected evidence; draft/blocker coverage is not the expected result |

Existing tests inspected (not executed for this documentation change):

- `membership-organization-context.resolver.spec.ts`: role-only refusal, one/
  multiple ACTIVE selection, selection validation, roles-empty resolution and
  missing Organization handling.
- `authentication.repository.spec.ts`: exact ACTIVE membership query/projection.
- `organization-membership.schema.spec.ts`: declared pair/query indexes and four
  accepted enum values; rejects ONBOARDING. No live-index proof.
- `authentication.application.service.spec.ts`: stale token rejected when active
  membership query returns none; this mocks repository evidence, not a persisted
  suspend/remove command or full revocation propagation.
- `scripts/migrations/organization-membership-backfill.plan.test.mjs`: historical
  dedup/exclusion/idempotency/conflict tests; not invitation/activation tests or
  evidence of migration execution on the current database topology.

Required review/implementation scenarios, **not executed acceptance tests**:

| Scenario | Expected constraint / decision gate |
|---|---|
| AT-01 — all four states, role-only data, active membership without role | B1/B2/B3; context only from ACTIVE; permissions evaluated separately |
| AT-02 — zero/one/multiple ACTIVE and valid/invalid selection | B3; existing auth outcome in section 6; future API/UI must resolve Q5/Q6 |
| AT-03 — inactive account or inactive actor membership; cross-Organization IDs | B4; deny access; precise HTTP/error/assertions require Q1/Q6 |
| AT-04 — invite/accept/activate/resend/cancel and token/identity/delivery failure | Only Q1–Q3/Q5–Q7-approved commands and outcomes; no added state |
| AT-05 — every transition cell, same-state repeat, duplicate pair and concurrent/stale write | Q3/Q5/Q6: test accepted outcomes, atomic duplicate/partial-write safety |
| AT-06 — allowed/denied actor, self/peer/last-admin target | Q1/Q3; no copied account or Project grants |
| AT-07 — audit persistence, state/audit failure and retry | Preserve B6/E9 atomicity; Q7 authority/scope and specific transaction/dedup/error rules must be closed before implementation. E9 requires MongoDB replica-set commit/rollback evidence before cutover; no concrete mechanism/outcome is selected here. |
| AT-08 — suspend/remove/resume across tokens, caches, descendants and responsibilities | Parent context denial B2/B4; E10 refresh revalidation is a source fact, not executed mutation evidence; stored/cascade/offboarding behavior only after Q6/Q8 |
| AT-09 — member list projection/pagination and FE list/actions/errors | Q4–Q6; four states and backend authority; DATN-88 after accepted BE API |

## 9. Review exit and downstream handoff

Before marking DATN-86's expected result achieved, confirm the approval authority
and record accepted answers for each enabled operation and each excluded/deferred
operation, then review the exact contract revision with those authorities. Reconcile
the owning decision, versioned IAM OpenAPI/DTO/errors/audit specification and DB
contract where applicable; map each of DATN-229–234 to accepted rules and evidence.
Keep any remaining UNKNOWN and the affected downstream scope explicitly blocked.

DATN-87/DATN-88 must not start from this draft or assume a blocker register clears
the Jira dependency. Once the contract gate and required reviewed changes are
merged to main, use fresh task branches: DB changes in a separate DB lane first
when needed, then BE, then FE after its dependency is ready. Do not alter frozen
baselines, run migrations, add permission seeds, or change application behavior
to make this documentation task appear complete. PR #23 is already Open; human
contract review/approval, Jira completion and team communication remain separate
actions. A technical review of R3 is not product contract approval.
