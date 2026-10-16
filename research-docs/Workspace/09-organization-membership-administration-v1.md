# DATN-87 — Organization Membership Administration V1

Decision date: **2026-10-12, Asia/Saigon**. Status: **USER-APPROVED implementation
contract, dependency readiness PARTIAL**. Owner of this work package: Nguyen Hong
Phuc. The requester approved A1–A6/A8 and correction P2-01 with “ok duyệt” after
the approval scope was explained. This records that approval, not an unnamed
independent Product/Security review. The earlier Leader D1–D6 decision was conveyed
by the requester on2026-10-06. Backend reference: `fc7d0be91c7b3e9e1ff6a4a726d0cd4e5efabe6a`.

On 2026-10-13, the requester conveyed that the reviewer accepted the technical
implementation plan without substantial changes. This permits continuing the
reviewable Document/DB deliverables; it does not establish A7 provider readiness,
approve a shared database apply, or replace review of the final implementation diff.

This successor closes the selected policy/API questions of the historical
[C-01 R5](06-organization-membership-contract.md). Do not treat the selected rules
below as UNKNOWN because R5 or its exploratory worksheets predate the decisions.
A7 dependency/provider/proof contracts remain open; this decision is not evidence
that any new command has been implemented, deployed, tested or enabled.

- Jira: [DATN-87](https://trankimthang0207.atlassian.net/browse/DATN-87);
  contract predecessor[DATN-86](https://trankimthang0207.atlassian.net/browse/DATN-86);
  FE successor[DATN-88](https://trankimthang0207.atlassian.net/browse/DATN-88).
- Wire contract: [C-02 OpenAPI V1](contracts/c-02-membership-v1.openapi.json).
- Approval includes N1/V2/E1/H1/Q1/R3(epoch dependency), A1–A6/A8 and P2-01.
  It does not authorize shared-data migration/cutover, PR creation/merge, Jira
  status changes, reviewer requests or team messages.

## 1. Authority and context

Only an authenticated current ACTIVE User's **ACTIVE OrganizationMembership**
establishes Organization Context. PENDING_INVITE/SUSPENDED/REMOVED deny; no
RoleAssignment/client Organization or User ID can substitute. Preserve existing
Project creation: any ACTIVE authenticated member may create a PRIVATE Project
without an Organization role; creator bootstrap is Project MEMBER, not leader.

A1 exact permissions: `organization.memberships.read` and
`organization.memberships.manage`. Manage does not imply read. Every ADMIN route
requires current account ACTIVE, trusted Organization session, matching path scope,
actor ACTIVE membership, Organization-level assignment(projectId absent/null)
resolving actual Role ADMIN with matching roleCode and the exact permission in
Role.permissions. Unknown/deny evidence fails closed. JWT role/permission claims
are not current evidence. Platform authority alone, Project TEAM_LEADER and MEMBER
do not authorize C-02 even if assigned an inappropriate permission string.

DB provisioning unions both codes into the existing system ADMIN Role, preserving
old permissions including PR #25; no new User/Membership/RoleAssignment or grants
to other roles. Misconfigured roles fail closed; verify eligible ADMIN readiness
for each Organization. Bootstrap79/80 remains separate and must preserve atomicity.

Eligible ADMIN = distinct ACTIVE User + ACTIVE Membership + exact Organization
assignment resolving current ADMIN + manage permission. No self suspend/remove,
last-eligible-ADMIN removal/suspension or platform override. Peer ADMIN commands
are permitted only with all applicable safeguards/proofs. Emergency suspend may
precede handover, but never bypasses self/last-ADMIN constraints.

Recipient uses current authenticated ACTIVE account(ACCOUNT or Organization
session), bound targetUserId and current exact normalized invited email. No target
Organization ACTIVE context is required to accept. No ADMIN activate, auto role
grant, auto Organization session, direct-add, bulk invite or C-02 account creation.

## 2. Reads and DTOs (A2)

`O=/api/v1/iam/organizations/{organizationId}`, `M=O/memberships`,
`I=O/invitations`, `A=/api/v1/auth/invitations`. IDs24hex normalize lowercase;
times ISO8601UTC. Read responses are no-store. ADMIN reads require read permission.

| Route | Result / filters |
|---|---|
|GET M |All four membership states; optional single status filter |
|GET M/{membershipId} |Own scoped MembershipSummary |
|GET I |Current pending/unexpired invitations, not all Organization members |
|GET A |Own recipient pending/unexpired invitations |
|GET A/{invitationId} |Bound recipient's minimal invitation/membership and Organization label; expired detail may show EXPIRED |

Every list uses page1/pageSize20, maximum100; envelope
`{data,pagination:{page,pageSize,totalItems,totalPages}}`, empty[]/0/0.
Fixed createdAtDESC,_idDESC; no role/free-text/global-User search or arbitrary sort.
Strict allowlist query/body. MembershipSummary:
`id,organizationId,userId,status,version,createdAt,updatedAt,
user:{id,fullName,email,accountStatus}|null`. Null reference is an administrative
diagnostic, never evidence permitting a command. Membership.status differs from
User.accountStatus. No password/MFA/token/session/roles/last-login/private content.

Invitation fields: id,membershipId,organizationId,status,version,expiresAt,createdAt,
membershipVersion; ADMIN adds targetUserId/email, recipient adds organizationName
only. Recipient detail adds minimal Membership id/status/version. Stored PENDING
at expiresAt<=now is presented EXPIRED; version remains stored business version.
Delivery outcome is separate and only exposed when a provider supplies evidence;
outbox PUBLISHED does not prove email sent/delivered.

Page/count may share a scoped Membership aggregate/facet; User lookup only after
page limit with projection. No N+1 or pre-pagination User join. Index both scoped
sort and scoped status-sort where needed. Exact count/large offset still incur
work; use query timeout and verify plans. Stable sort is not a frozen snapshot
across requests; all mutations revalidate versions/authority. Cursor amendment
requires a separate wire review because current IAM lists use page/pageSize.

## 3. Commands and lifecycle (A3, N1/V2/E1)

Every command requires valid CSRF pair and Idempotency-Key. Strict JSON allowlist;
versions positive safe integers. ADMIN commands require manage. Version fields
are expectedMembershipVersion(MV) and expectedInvitationVersion(IV), not one
ambiguous version. Client IDs select resources, never confer authority.

| POST route | Body | Success | Allowed state / effect |
|---|---|---|---|
|I |email,reasonCode |201 MutationAck |No pair: create PENDING_INVITE + bound Invitation; no role |
|I/{invitationId}/resend |MV,IV,reasonCode |200 MutationAck |Current Invitation + PENDING_INVITE; new Invitation ID |
|I/{invitationId}/cancel |MV,IV,reasonCode |200 MutationAck |PENDING_INVITE→REMOVED; live Invitation→CANCELLED |
|A/{invitationId}/accept |MV,IV |200 MutationAck |Bound recipient; live/current pending Invitation + PENDING_INVITE→ACTIVE |
|M/{membershipId}/suspend |MV,reasonCode |200 MutationAck |ACTIVE→SUSPENDED |
|M/{membershipId}/remove |MV,reasonCode,handoverReceiptId |200 MutationAck |ACTIVE/SUSPENDED→REMOVED, domain handover proof |
|M/{membershipId}/resume |MV,reasonCode,rightsReviewReceiptId |200 MutationAck |SUSPENDED→ACTIVE, review+restoration gate |
|M/{membershipId}/reinvite |MV,reasonCode,rightsReviewReceiptId |200 MutationAck |REMOVED→PENDING_INVITE, new Invitation+review+restoration gate |
|M/{membershipId}/rights-review |MV,reasonCode |201 ReceiptAck |SUSPENDED/REMOVED, approved IAM review proof mechanism |

Reason enum: invite/resend/reinvite ACCESS_REQUEST|ACCESS_REVIEW; cancel
INVITATION_CANCELLED; suspend SECURITY_INCIDENT|ACCESS_REVIEW; remove OFFBOARDING;
resume/rights-review ACCESS_REVIEW. No free text. Accept records server reason
RECIPIENT_ACCEPTED. Email trim/lowercase/max254/valid format; no plus-address
equivalence, wildcard or account creation. Bind existing eligible User ID and
exact normalized email atomically. Unknown/inactive target is one generic error.

| From / To | PENDING_INVITE | ACTIVE | SUSPENDED | REMOVED |
|---|---|---|---|---|
|PENDING_INVITE |Resend, MV unchanged |Recipient accept |Deny |Cancel |
|ACTIVE |Deny |New-key conflict |Suspend |Remove+handover |
|SUSPENDED |Deny |Resume+review |New-key conflict |Remove+handover |
|REMOVED |Reinvite+review |Deny |Deny |New-key conflict |

One long-lived Membership per Organization/User; Invitation lifecycle is separate:
PENDING/ACCEPTED/CANCELLED/EXPIRED/SUPERSEDED. Old legacy REVOKED remains history,
not a V2 state.7days/single-use; resend creates new ID and invalidates old link:
old live→SUPERSEDED, old expired materializeEXPIRED; old IV increments, new IV1,
MV unchanged but Membership conditional write fence protects accept/cancel races.
Invitation ID is sufficient account-bound selector; no generation query or epoch
equivalence. Expiry is enforced on read/accept/delivery, not by a TTL delete/worker.
Expiry alone does not change Membership. Cancel expired current Invitation
materializes EXPIRED and removes pending Membership; it does not rewrite expiry.

First invite with ACTIVE/SUSPENDED pair denied; pending uses resend, removed uses
reinvite; never create a second pair. New key in already-destination state returns
conflict. Same committed key/fingerprint follows replay, not the transition grid.

Immutable MutationAck:
`operationId,membership:{id,organizationId,userId,status,version},
invitation?:{id,status,version,expiresAt}`. Resend returns new Invitation; audit
records old/new IDs/versions. ReceiptAck:
`operationId,receipt:{id,purpose,targetMembershipVersion,expiresAt}`.
No dynamic User/Organization/delivery data; replay is historical operation result,
not current state. Accept/replay never mints a session. GET before a new command.

## 4. Replay and quota (A4)

Key16..128 `[A-Za-z0-9._:-]`, unique scope(actorUserId,organizationId,keyHash).
Fingerprint = canonical command/path/target + normalized validated body, including
versions/reason/receipt IDs; excludes credentials/CSRF/requestId/current display
data. Compute before re-resolving mutable email to a different User. Recipient
Organization derives from persisted bound Invitation. Store only hashes and
minimal committed ack/status/operationId/binding/committedAt/expiresAt in IAM.

24hour replay cache window from commit, distinct from Invitation7days. Reauthenticate
and reauthorize current actor/recipient binding, then exact committed-key lookup
**before** new-attempt version/state/expiry conditions. Exact replay preserves HTTP
status/body with Idempotency-Replayed:true, even if versions/state subsequently
changed. No stale-result409, repeated audit/outbox/quota or session mint. Lost
authority denies replay. Same key different fingerprint409 IDEMPOTENCY_KEY_REUSED.

Only new attempts check CAS/lifecycle/proofs. Unique operation key serializes
same-key contenders; loser reads committed result after reauthorization. Failure
rolls back and does not cache success. Unknown commit recovers by original key.
Expired cache may be reused as new attempt with all business/version invariants;
expired-but-not-TTL-deleted record must be conditional replaced/deleted atomically,
not bypass unique index. TTL only deletes operation cache, never domain/audit history.

Create/resend/reinvite share quota30 committed invitation creations per Organization/
actor rolling1hour; replay/failure consume none. Reservation/counter participates
in transaction and actor-org/shared write fence; no count-then-insert race.
429 Retry-After follows oldest counted operation leaving window. Transport abuse
throttling is separate. Client retains key/body across retries, new action new key.

## 5. Errors and precedence (A5)

Reuse `{code,message,details,requestId}`; validation details field names only,
5xxdetails{}; do not leak DB/private/proof/credential data. Parser-level malformed
JSON/oversize preserves transport semantics rather than forcing422.

| Situation | HTTP / code |
|---|---|
|Invalid credential/current account/context |401 AUTHENTICATION_FAILED; refresh keeps AUTH_REFRESH_INVALID |
|CSRF |403 AUTH_CSRF_INVALID |
|Missing ADMIN/permission or different selected Organization |403 ORGANIZATION_MEMBERSHIP_FORBIDDEN |
|ADMIN missing/foreign target |404 ORGANIZATION_MEMBERSHIP_NOT_FOUND or INVITATION_NOT_FOUND |
|Recipient GET missing/foreign |404 INVITATION_NOT_FOUND |
|New recipient accept missing/foreign/expired/cancelled/superseded/used |409 INVITATION_NOT_ACCEPTABLE |
|Malformed IDs/body/query/key/version/reason/unknown fields |422 VALIDATION_FAILED |
|Unknown/inactive invite target |422 INVITATION_TARGET_NOT_ELIGIBLE |
|Self suspend/remove |403 MEMBERSHIP_SELF_ACTION_FORBIDDEN |
|Last eligible ADMIN |409 LAST_ELIGIBLE_ADMIN |
|Stale precondition |409 MEMBERSHIP_VERSION_CONFLICT or INVITATION_VERSION_CONFLICT |
|Wrong new-attempt state |409 MEMBERSHIP_INVALID_TRANSITION |
|First invite existing pair |409 TARGET_ALREADY_MEMBER / ALREADY_PENDING / USE_RESUME / USE_REINVITE |
|Different fingerprint |409 IDEMPOTENCY_KEY_REUSED |
|Missing/invalid/stale proof |409 HANDOVER_REQUIRED or RIGHTS_REVIEW_REQUIRED |
|Provider/readiness unavailable |503 IAM_MEMBERSHIP_DEPENDENCY_UNAVAILABLE |
|Quota |429 ORGANIZATION_INVITATION_RATE_LIMITED +Retry-After |
|Required write failure |500 IAM_MEMBERSHIP_MUTATION_FAILED |

Read-response clarification (2026-10-14): the requester authorized corrections
following [PR28 review](https://github.com/DATN-SPRING2027/DATN-BE/pull/28#issuecomment-6160371586).
For the Membership list/detail GETs, 500 describes an unexpected internal read
failure, without mutation/audit/outbox rollback semantics. Dependency connection,
server-selection, network or operation/query-deadline failures use the existing
503 `IAM_MEMBERSHIP_DEPENDENCY_UNAVAILABLE`; unexpected application/query defects
remain 500. Stored MemberUser.email must satisfy the wire email format before a
successful DTO is returned; invalid projected metadata fails closed with 503.
Technical review/merge of this clarification remains pending; A7/cutover gates
and mutation failure semantics are unchanged.

Bounded parsing→authentication/CSRF→current scope/permission or recipient binding→
strict validation→scoped selector→key replay/conflict→new-attempt preconditions.
New ADMIN attempt: MV then IV, state/expiry, self/lastADMIN, proof. Recipient
invitation inadmissibility is generic409; admissible invitations then version-check.

## 6. Atomicity, invariant writers and audit (A6)

One ClientSession transaction: actor/evidence conditional writes + Organization
shared ADMIN fence + domain CAS + required continuum_audit.audit_logs_iam audit +
operation result + IAM outbox intent for invitation creation. Required failure
rolls back all; email is after commit. Reuse existing IAM topology, not Redis
SETNX/generic AuditService without session. Snapshot alone does not prevent stale
authority/write skew; internal fence is a real write separate from business version.

All eligible-ADMIN writers must participate: C-02, User.status, ADMIN Assignment/
Role.permissions and related provisioning/cutover. Two different targets must
conflict via one Organization write before counting eligible ADMIN; retry reloads
actor/evidence. Preserve current User-status transaction/Organization write and
SHARED_ACCOUNT_STATUS_CHANGE denial; update current roleCode-only isAdmin/count to
actual Role/manage definition and harmonize protocols. P2-01 explicitly corrects
the earlier claim that this repository only counted then updated. No duplicate
lock system; DB fields alone do not prove all writers/readers are integrated.

One append-only success audit per operation, schemaVersion2. Exact actions:
ORGANIZATION_MEMBERSHIP_INVITED/ACTIVATED/SUSPENDED/REMOVED/RESUMED/REINVITED,
ORGANIZATION_INVITATION_RESENT/CANCELLED, ORGANIZATION_MEMBERSHIP_RIGHTS_REVIEWED.
Allowlist eventId/operationId/organizationId/actorUserId/action/occurredAt/reasonCode/
correlationId/membershipId/invitationIds, separate stored before/after(status/version/
expiresAt), applicable proof/reservation IDs. Exclude email/name/raw body/free text/
credentials/handover content. Preserve legacy CREATED/ACCEPTED/REVOKED audit history.

## 7. A7 dependencies and A8 compatibility

H1: owning Handover/responsibility domains issue/verify purpose/org/target/version/
approver/coverage/freshness proofs, including owner-attested NONE_REQUIRED. Client
receipt ID/reason/checkbox is not completion evidence. Reservation/finalize/release
requires approved recovery; unknown commit cannot release blindly. No direct
cross-domain DB transaction. Q1 invalidates old rights; new grant by proper owner.
Epoch scoped per Membership is a separate dependency, not Invitation generation;
all old child/session/token/grant readers/issuers and legacy cutover need coverage.
No normal remove/resume/reinvite/rejoin or unsafe first-accept enablement before
these prerequisites. Emergency suspend may work independently with safeguards.

IAM outbox/dispatcher→Notification exported delivery/dedup contract, correct owner
DBs, no cross-owner reads. A7 exact payload/provider/credentials/proof freshness/
consumer recovery/retention are **not approved or ready**. No health stub or outbox
writer alone proves delivery/handover, no SENT without provider evidence. Keep
old link denial even when an email was already in flight. Do not promise exactly
once provider delivery. Existing suggested15min/5s/retries are not selected policy.

A8 coordinated cutover: canonical invitation paths retained, email+reason replaces
email+roleCode, accept no implicit Role/session. Old DELETE adapts into the same
cancel auth/key/MV/IV/reason/audit command or is disabled during cutover; no guessed
default reason/version or old bypass. Legacy Invitation metadata/history retained,
never auto-link/create User/Membership from email. New persistence shape does not
enable V2 behavior. FE onboarding/88 remains a separate lane; release owner/window
must be confirmed before enabling changed contract.

## 8. Acceptance and rollout

| Checkpoint | Proof still required |
|---|---|
|[235](https://trankimthang0207.atlassian.net/browse/DATN-235) list |Own ADMIN/read,denied actors,inactive/cross-scope,4states/paging/empty/null/PII/query plan |
|[236](https://trankimthang0207.atlassian.net/browse/DATN-236) invite |Exact eligible User,pair/Invitation/audit/result/outbox atomicity,duplicate/resend/expiry/quota races,no grants/old links |
|[237](https://trankimthang0207.atlassian.net/browse/DATN-237) activate |Bound recipient/twoCAS,no role/session,replay after versions/state/expiry change,orphan-right safeguards |
|[238](https://trankimthang0207.atlassian.net/browse/DATN-238) lifecycle |Self/lastADMIN/two-target+User-status/Role races,proof/emergency/review/epoch legacy denial |
|[239](https://trankimthang0207.atlassian.net/browse/DATN-239) auth |Current User/Membership/Role.permissions/actual scope,deny unknown/staleJWT/revoke during write/replay |
|[240](https://trankimthang0207.atlassian.net/browse/DATN-240) audit |One allowlisted persisted audit,required-write failure rollback,uncertain commit/exact retry dedup |
|[241](https://trankimthang0207.atlassian.net/browse/DATN-241) tests |Disposable Mongo7replica set,index/transaction/CAS races,failure injection,expired cache present,explicit CI suite selection |

Contract approval ≠ completion: no executable command evidence in this document.
Initial ACTIVE-context test delta18ea169 is separate partial evidence. DB schema+
new migration branch must be reviewed/merged before dependent BE from updated main.
Do not rewrite old migrations or apply shared DB here. Publish accepted wire,
implement independent lanes, obtain A7 readiness, then enable dependent paths and
verify all checkpoints. Jira statuses remain requester-owned; parent/children last
observed InProgress, not Done merely because this contract is approved.
