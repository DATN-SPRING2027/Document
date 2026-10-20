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

**Email-bound invitation amendment (2026-10-20, requester-approved product decision).**
This amendment supersedes earlier statements in this document that require an
existing ACTIVE User, `targetUserId`, or a PENDING_INVITE Membership at invitation
creation. A Manager may invite a normalized email whether or not it currently maps
to a User. An invitation is a distinct record until acceptance; it does not create
a User, Membership, RoleAssignment, or Organization session. Acceptance requires a
current authenticated ACTIVE account and the server-derived account email, normalized
by the existing IAM trim/lowercase convention, to equal the invitation's immutable
`invitedEmail`. Request-body email is never an authority. No target Organization
ACTIVE context is required to accept. A successful accept atomically creates one
ACTIVE Membership, changes the invitation to ACCEPTED, and writes the required audit.
No ADMIN activation, automatic role grant, automatic Organization session, direct-add,
bulk invite, or account creation from the invitation endpoint is allowed.

Supported recipients: existing accounts and unregistered email addresses. For an
unregistered recipient, the invitation token is retained through login/registration
as an opaque continuation value and revalidated by the server after authentication;
the client continuation is not authority. Do not persist Organization/email context
as a trusted value in localStorage. Registration must use the invited email.
Registering with another email never transfers or changes the invitation; show
“This invitation was sent to another email address.” without echoing the invited
address in an error response.

Explicitly out of scope: generic Organization join URLs, public join pages, manager
copy/share links, multi-use bearer links, or a token that can accept multiple
invitations. An emailed URL represents exactly one invitation and one email identity.

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
|GET A/{invitationId} |Authenticated recipient whose current normalized email matches; minimal invitation and Organization label |
|POST /api/v1/auth/invitations/resolve |Resolve one opaque emailed token before or after login; no-store, minimal detail, never accepts |

Every list uses page1/pageSize20, maximum100; envelope
`{data,pagination:{page,pageSize,totalItems,totalPages}}`, empty[]/0/0.
Fixed createdAtDESC,_idDESC; no role/free-text/global-User search or arbitrary sort.
Strict allowlist query/body. MembershipSummary:
`id,organizationId,userId,status,version,createdAt,updatedAt,
user:{id,fullName,email,accountStatus}|null`. Null reference is an administrative
diagnostic, never evidence permitting a command. Membership.status differs from
User.accountStatus. No password/MFA/token/session/roles/last-login/private content.

Invitation fields: `id,organizationId,invitedEmail,createdBy,status,version,expiresAt,
createdAt,updatedAt,acceptedAt?,acceptedByUserId?`. Persistence reuses current `email`,
`invitedBy`, and `acceptedBy` fields and maps them to the public names above; timestamps
use the existing schema timestamps. `membershipId` and `targetUserId`
are optional optimization/history references and never required to create, list, or
accept an invitation. ADMIN list includes invited email and inviter label when policy
permits; recipient detail includes Organization label, invited email, status, and
expiry. Neither DTO exposes token or tokenHash. A random per-invitation token is
stored only as a one-way SHA-256 hash; token-bearing delivery material must be
protected at rest and never logged. `PENDING` at `expiresAt<=now` is effectively
`EXPIRED` and fails closed. Delivery outcome is separate and only exposed when a
provider supplies evidence; outbox PUBLISHED does not prove email sent/delivered.
Generate at least 32 random bytes with a cryptographic RNG and encode as base64url.
The email CTA uses an invitation-specific URL fragment (`/organization/invitations#<token>`);
the FE removes the fragment from browser history immediately, sends the token only
in the no-store resolve body, and carries the opaque continuation through
login/registration for server revalidation.

Page/count may share a scoped Membership aggregate/facet; User lookup only after
page limit with projection. No N+1 or pre-pagination User join. Index both scoped
sort and scoped status-sort where needed. Exact count/large offset still incur
work; use query timeout and verify plans. Stable sort is not a frozen snapshot
across requests; all mutations revalidate versions/authority. Cursor amendment
requires a separate wire review because current IAM lists use page/pageSize.

## 3. Commands and lifecycle (A3, N1/V2/E1)

Every mutation requires a valid CSRF pair and Idempotency-Key. Strict JSON
allowlist; supplied versions are positive safe integers. ADMIN commands require
manage. Membership lifecycle commands use `expectedMembershipVersion` (MV); email
invitation commands use `expectedInvitationVersion` (IV) only because there is no
pending Membership. Client IDs select resources, never confer authority.

| POST route | Body | Success | Allowed state / effect |
|---|---|---|---|
|I |email,reasonCode |201 InvitationMutationAck |No active/suspended pair: create email-bound PENDING Invitation only; no Membership or role |
|I/{invitationId}/resend |IV,reasonCode |200 InvitationMutationAck |Current pending Invitation; new Invitation ID/token; old token superseded |
|I/{invitationId}/cancel |IV,reasonCode |200 InvitationMutationAck |Current pending Invitation→CANCELLED |
|A/{invitationId}/accept |IV |200 AcceptMutationAck |Authenticated email matches; pending/unexpired Invitation→ACCEPTED and create one ACTIVE Membership |
|M/{membershipId}/suspend |MV,reasonCode |200 MutationAck |ACTIVE→SUSPENDED |
|M/{membershipId}/remove |MV,reasonCode,handoverReceiptId |200 MutationAck |ACTIVE/SUSPENDED→REMOVED, domain handover proof |
|M/{membershipId}/resume |MV,reasonCode,rightsReviewReceiptId |200 MutationAck |SUSPENDED→ACTIVE, review+restoration gate |
|M/{membershipId}/reinvite |MV,reasonCode,rightsReviewReceiptId |200 MutationAck |REMOVED→PENDING_INVITE, new Invitation+review+restoration gate |
|M/{membershipId}/rights-review |MV,reasonCode |201 ReceiptAck |SUSPENDED/REMOVED, approved IAM review proof mechanism |

Reason enum: invite/resend/reinvite ACCESS_REQUEST|ACCESS_REVIEW; cancel
INVITATION_CANCELLED; suspend SECURITY_INCIDENT|ACCESS_REVIEW; remove OFFBOARDING;
resume/rights-review ACCESS_REVIEW. No free text. Accept records server reason
RECIPIENT_ACCEPTED. Email trim/lowercase/max254/valid format; no plus-address
equivalence, wildcard or account creation. Store the normalized email as the
invitation identity. If an ACTIVE Membership already exists, reject as already a
member; never create a duplicate. Existing suspended/removed Membership continues
through the separately approved resume/reinvite and rights-review workflow.

Membership lifecycle remains unchanged once a Membership exists:
| From / To | ACTIVE | SUSPENDED | REMOVED |
|---|---|---|---|
|ACTIVE |New-key conflict |Suspend |Remove+handover |
|SUSPENDED |Resume+review |New-key conflict |Remove+handover |
|REMOVED |Deny |Deny |New-key conflict |

Invitation lifecycle (independent from Membership):
| From / To | PENDING | ACCEPTED | CANCELLED | EXPIRED | SUPERSEDED |
|---|---|---|---|---|---|
|PENDING |Resend creates a new invitation and supersedes this one |Recipient accept, once |Manager cancel |Expiry is fail-closed |Resend |
|ACCEPTED |Deny |Terminal; replay only by original idempotency key |Deny |Deny |Deny |
|CANCELLED |Deny |Deny |Terminal |Deny |Deny |
|EXPIRED |Deny |Deny |Deny |Terminal |Deny |
|SUPERSEDED |Deny |Deny |Deny |Deny |Terminal |

One ACTIVE/SUSPENDED/REMOVED Membership per Organization/User. A pending invitation
has no Membership row. Invitation lifetime is seven days and single-use; resend
creates a new invitation ID/token and invalidates the old one (`SUPERSEDED`). The
token is an opaque selector for that invitation only; server record remains
authoritative. Expiry is enforced on resolve/read/accept/delivery, not by TTL deletion.
Expiry never creates or mutates a Membership. The expiry processor, or the first
mutation that observes expiry, materializes `EXPIRED` with a compare-and-set and
writes exactly one `ORGANIZATION_INVITATION_EXPIRED` audit event in the same
transaction. Expired invitations fail closed before materialization. Cancel affects
only the invitation.

Invite for an already ACTIVE member returns `409 TARGET_ALREADY_MEMBER`; for an
existing pending invitation, the same normalized email is consolidated through the
resend/idempotency convention, never multiplied. A suspended or removed member is
not silently restored; use its separately approved lifecycle path. New key in an
already-destination state returns conflict. Same committed key/fingerprint follows
replay, not the transition grid.

Invitation create acknowledgement is
`operationId,invitation:{id,status,version,expiresAt}` and contains no Membership or
recipient token. Accept acknowledgement is
`operationId,membership:{id,organizationId,userId,status,version},
invitation:{id,status,version,expiresAt}`. Other membership mutations preserve
their current acknowledgement shapes. Resend returns a new Invitation; audit
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
|New recipient accept missing/foreign/cancelled/superseded/already accepted |409 INVITATION_NOT_ACCEPTABLE |
|Expired invitation |410 INVITATION_EXPIRED |
|Authenticated email differs from invitation email |403 INVITATION_EMAIL_MISMATCH, generic message without echoing either email |
|Malformed IDs/body/query/key/version/reason/unknown fields |422 VALIDATION_FAILED |
|Invalid email |422 VALIDATION_FAILED |
|Self suspend/remove |403 MEMBERSHIP_SELF_ACTION_FORBIDDEN |
|Last eligible ADMIN |409 LAST_ELIGIBLE_ADMIN |
|Stale precondition |409 MEMBERSHIP_VERSION_CONFLICT or INVITATION_VERSION_CONFLICT |
|Wrong new-attempt state |409 MEMBERSHIP_INVALID_TRANSITION |
|Email already has a pending invitation |409 ALREADY_PENDING; use resend |
|Email belongs to current ACTIVE member |409 TARGET_ALREADY_MEMBER |
|Different fingerprint |409 IDEMPOTENCY_KEY_REUSED |
|Missing/invalid/stale proof |409 HANDOVER_REQUIRED or RIGHTS_REVIEW_REQUIRED |
|Provider/readiness unavailable |503 IAM_MEMBERSHIP_DEPENDENCY_UNAVAILABLE |
|Quota |429 ORGANIZATION_INVITATION_RATE_LIMITED +Retry-After |
|Required write failure |500 IAM_MEMBERSHIP_MUTATION_FAILED |

Bounded parsing→authentication/CSRF→current scope/permission or recipient binding→
strict validation→scoped selector→key replay/conflict→new-attempt preconditions.
New ADMIN attempt: MV for Membership commands; IV for invitation commands, then
state/expiry and applicable self/lastADMIN/proof checks. Recipient mismatch is a
403 without echoing either email, expired is 410, and other invitation inadmissibility
is generic409; admissible invitations then version-check.

## 6. Atomicity, invariant writers and audit (A6)

One ClientSession transaction: actor/evidence conditional writes + Organization
shared ADMIN fence + invitation/membership conditional writes + required
continuum_audit.audit_logs_iam audit + operation result + IAM outbox intent for
invitation creation. Accept atomically creates ACTIVE Membership and marks the
invitation ACCEPTED; any required failure rolls back both. Email is after commit.
Reuse existing IAM topology, not Redis
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
ORGANIZATION_INVITATION_RESENT/CANCELLED/ACCEPTED/EXPIRED,
ORGANIZATION_MEMBERSHIP_RIGHTS_REVIEWED.
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
consumer recovery/retention are **not approved or ready**. The current create,
resend, cancel, and accept readiness gates remain enforced until approved; this amendment
does not enable email or invitation commands in production. No hardcoded READY,
fake provider, health stub, or outbox writer alone proves delivery; no SENT without
provider evidence. The invitation URL may be sent only through the approved provider
path and must contain a token bound to one invitation and email. Do not promise
exactly-once provider delivery. Existing suggested 15min/5s/retries are not selected
policy.

A8 coordinated cutover: canonical invitation paths retained, email+reason replaces
email+roleCode, accept no implicit Role/session. Old DELETE adapts into the same
cancel auth/key/IV/reason/audit command or is disabled during cutover; no guessed
default reason/version or old bypass. Legacy Invitation metadata/history retained.
Email invitations never auto-create a User or Membership; acceptance creates the
Membership only after server identity/email validation. The new persistence shape
and this product decision do not enable production behavior. FE onboarding/88 remains
a separate lane; release owner/window must be confirmed before enabling changed
contract.

## 8. Acceptance and rollout

| Checkpoint | Proof still required |
|---|---|
|[235](https://trankimthang0207.atlassian.net/browse/DATN-235) list |Own ADMIN/read,denied actors,inactive/cross-scope,4states/paging/empty/null/PII/query plan |
|[236](https://trankimthang0207.atlassian.net/browse/DATN-236) invite |Existing/unregistered normalized email, no membership at invite, invitation/audit/result/outbox atomicity, duplicate/resend/expiry/quota races, no grants/shareable links |
|[237](https://trankimthang0207.atlassian.net/browse/DATN-237) activate |Authenticated email binding, existing and post-registration recipient, atomic Membership+Invitation+audit, one-time acceptance, mismatch/expired/cancelled/replay denial, no role/session |
|[238](https://trankimthang0207.atlassian.net/browse/DATN-238) lifecycle |Self/lastADMIN/two-target+User-status/Role races,proof/emergency/review/epoch legacy denial |
|[239](https://trankimthang0207.atlassian.net/browse/DATN-239) auth |Current User/Membership/Role.permissions/actual scope,deny unknown/staleJWT/revoke during write/replay |
|[240](https://trankimthang0207.atlassian.net/browse/DATN-240) audit |One allowlisted persisted audit,required-write failure rollback,uncertain commit/exact retry dedup |
|[241](https://trankimthang0207.atlassian.net/browse/DATN-241) tests |Disposable Mongo7replica set,index/transaction/CAS races,failure injection,expired cache present,explicit CI suite selection |

Contract approval ≠ completion: no executable command evidence in this document.
The email-bound amendment records the requester's product decision; it does not
record A7/A8 operational approval. DB schema and new migration branch must be
reviewed/merged before dependent BE from updated main. Do not rewrite old migrations
or apply shared DB here. Implement separate lanes, obtain A7 readiness, complete
coordinated A8 cutover, and verify all checkpoints before enabling the changed paths.
Jira statuses remain requester-owned; parent/children last observed InProgress, not
Done merely because this contract is approved.

## 9. Email-bound V1 source-to-flow map and acceptance scenarios

| User step | Authority/source | Required outcome |
|---|---|---|
|Manager enters email |Current authenticated ADMIN, Organization scope, `organization.memberships.manage` |Normalize by existing trim/lowercase rule; reject invalid email; no User lookup requirement |
|Create invite |Invitation command + IAM persistence + audit/outbox transaction |One PENDING record with normalized `invitedEmail`, creator, expiry, one-way token hash; no Membership row |
|Deliver email |Approved notification provider only (A7) |Organization name, permitted inviter label, expiry, invitation-specific URL; no password, raw DB IDs, authorization data, or token in logs |
|Open email URL |Invitation-specific opaque token |Resolve one invitation only; no state change on GET/resolve; no token displayed in response |
|Login/register |Existing authentication flow |Continuation token is validated server-side afterward; user account email must match invitation; client redirect/storage is not authority |
|Accept |Authenticated principal + invitation record |Server compares normalized principal email; one transaction creates one ACTIVE Membership, marks ACCEPTED, records audit; no role/session grant |

Acceptance scenarios: an existing account with matching email accepts once; an
unregistered email registers with that same address and then accepts; a different
authenticated email receives `INVITATION_EMAIL_MISMATCH`; invalid/expired/cancelled/
superseded tokens fail closed; repeated accept with the same idempotency key replays
the original result, while a different key cannot create a second Membership; an
active member cannot receive a duplicate invite; cross-Organization token/ID swaps
do not change the Organization bound in the invitation record.
