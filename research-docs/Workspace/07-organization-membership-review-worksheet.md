# DATN-86 — Organization Membership decision worksheet

## Review status and use

- Revision: **R5, 2026-10-06 (Asia/Saigon)**; prepared by Nguyen Hong Phuc.
  R3 alternatives are retained; R5 applies the approved documentation corrections.
- Companion to the [working contract](06-organization-membership-contract.md)
  (B1–B7, E1–E14, Q1–Q8, AT-01–09) and [PR #23](https://github.com/DATN-SPRING2027/Document/pull/23).
- **All alternatives, command mappings, HTTP/DTO examples and proposed outcomes
  below are [PROPOSED]. No option has been selected or approved.** An explicit
  exclusion/deferment also requires a decision; blank approval is UNKNOWN.
- The accepted transition grid remains 16 UNKNOWN cells. Exactly PENDING_INVITE,
  ACTIVE, SUSPENDED, REMOVED are stored states; only ACTIVE establishes context.
  RoleAssignment never substitutes for membership. This worksheet grants no access.
- IAM mutation/audit atomicity remains the existing AGENTDB §6 requirement.
  Collection, event, transaction mechanism/boundary and unapproved policies remain
  UNKNOWN. This is documentation only, not executable OpenAPI or a DB design.

Review each option against the named Q gate, record the exact adopted/amended
rule and authority in section 6, then update the working contract. Until human
contract review closes the required decisions, DATN-86's expected result is
**NOT MET** and DATN-87/88 remain blocked. Technical review is a separate check.

The [external research and leader proposal](08-organization-membership-external-research-and-proposal.md)
adds vendor evidence and a recommended package for these choices. Recommendations
are PROPOSED; no option in this worksheet is selected or approved by that research.
E12 confirms the separately approved first-ADMIN provisioning boundary and denies
ordinary membership management through platform authority alone. It does not
select any Organization administration alternative below.

## 1. DATN-231 — invitation and activation alternatives

| Choice | Concrete alternative for review | Tradeoff / remaining authority gate |
|---|---|---|
| INV-A | Conditionally invite an existing User by userId; first membership creation would produce PENDING_INVITE. Unknown userId would create neither User nor membership. | Product + IAM/auth + Security must first confirm an approved account source/provisioning workflow, owner, eligibility and safe ADMIN discovery/selection for outside/nonmember recipients. E13 has no create-User API and its ACTIVE own-Organization directory is insufficient. If missing, define dependent work before enablement; dev seed/manual DB is not a complete product flow. Q1/Q2/Q4/Q6. |
| INV-B | Invite an email recipient who may not yet have a User; create/link identity only through an accepted onboarding contract. | Needs an approved identity binding and representation before a membership requiring userId can exist; no placeholder User, collection or schema is chosen. Product + IAM/auth + Security + DB; DATN-231/233 blocked until resolved. |
| ACT-A | Recipient proves the invited identity and accepts; successful accepted redemption would change PENDING_INVITE to ACTIVE. | A recipient with zero ACTIVE memberships cannot obtain current Organization login context (B3/E5). Define a narrowly scoped authentication/redemption contract first; do not bypass the ordinary ADMIN route or treat a token as general Organization access. Q1/Q2/Q3/Q5/Q6. |
| ACT-B | An authorized Organization ADMIN activates a pending membership after the approved verification/consent prerequisite. | Avoids requiring a recipient session for this command, but does not decide verification or consent, or grant ADMIN an arbitrary ACTIVE write. Product + Security + IAM must specify proof and self/peer/last-admin safety. Q1/Q2/Q3. |
| DEL-A | Commit the pending mutation with its atomic audit, then attempt delivery; retain pending membership on delivery failure and expose a safe retry outcome. | Delivery occurs outside the membership/audit atomicity guarantee unless the owning contract says otherwise. Requires Notification ownership, durable delivery/retry semantics and an accepted response; event/outbox mechanism remains UNKNOWN. Q2/Q5/Q6/Q7. |
| DEL-B | Define successful delivery as a prerequisite to the business result. | Team must explain how external delivery and a failed membership/audit commit are reconciled; no cross-service transaction or compensation is assumed. Cannot be implemented from this row. Q2/Q7. |

INV-A/B decide identity; ACT-A/B decide activation authority; DEL-A/B decide delivery
semantics. These are separate choices, not bundled approval. For every enabled
choice, decide onboarding eligibility, identity proof, invite binding, expiry,
resend/cancel, replay, duplicate and rate limits. All durations/counts and proof
formats remain UNKNOWN; an expired credential is not a fifth membership state.

**Existing Project baseline (E14), not an activation proposal:** after any future
approved acceptance establishes ACTIVE, an authenticated active User in trusted
matching context can pass Project-create authorization even with roles=[] and no
project.create grant. Other request/deny rules apply; creation also needs the
configured current MEMBER Role containing project.read for creator bootstrap,
otherwise the transaction rolls back. Preserve this baseline. A restriction on
Project creation needs a separate Project decision; ACT-A does not add a role gate.

For a token-based ACT-A design, a security candidate is an unpredictable,
identity-bound, securely stored, expiring, single-use credential, excluded from
logs and ordinary member DTOs. This is an **analogy** from OWASP's password-reset
guidance, not an accepted invitation policy or permission to reuse the reset API.
See [OWASP Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).
IAM/auth + Security must still approve issuance, redemption, transport, proof,
storage representation, and replay behavior under Q2/Q5–Q7.

## 2. DATN-232 — candidate lifecycle and effects

| Candidate command | Proposed source → result for review | Required decision before enablement |
|---|---|---|
| Invite first pair | First record → PENDING_INVITE, only if INV-A/B prerequisites are met | Q1/Q2/Q3/Q5/Q7; first creation is not a new enum state. |
| Accept or activate | PENDING_INVITE → ACTIVE, according to ACT-A/B | Q1–Q3; no implicit role assignment, new account or session is approved. |
| Suspend | ACTIVE → SUSPENDED | Q1/Q3/Q5/Q6/Q7/Q8; authorized actor, reason, target safety, concurrency and offboarding prerequisite. |
| Remove | ACTIVE or SUSPENDED → REMOVED | Q1/Q3/Q5/Q6/Q7/Q8; retain/delete representation and responsibilities must be decided; REMOVED does not mean hard delete. |
| Resend | PENDING_INVITE → PENDING_INVITE with separately decided invitation credential effect | Q2/Q3; same stored state does not imply no side effects or safe unlimited retries. |
| Cancel invitation | Consider PENDING_INVITE → REMOVED, or explicitly defer cancellation | Q2/Q3; cancellation interpretation and retention must be approved, no CANCELLED state. |
| Resume | Consider SUSPENDED → ACTIVE, or explicitly defer | Q1/Q3/Q8; define renewed eligibility and whether old roles/scopes regain effect. |
| Rejoin | Consider REMOVED → PENDING_INVITE, or explicitly defer | Q2/Q3/Q8; reconcile current unique pair; no second row or role restoration is assumed. |

For each of the 16 cells in contract section 4, reviewers must mark **enabled
with a command**, **excluded**, or **deferred**, and specify retry/error behavior.
The rows above cover candidates, not the other cells by inference. Direct
activation without a pending invite, suspending a pending invite, ACTIVE →
PENDING_INVITE and all other unspecified transitions remain UNKNOWN. Same-state
requests need an explicit no-op/replay/conflict rule for each command.

| Effect boundary | Concrete alternatives to decide | Constraint that is already settled |
|---|---|---|
| Stored child memberships/roles/grants | Preserve records with access gated by parent eligibility; or explicitly reconcile selected records through approved domain contracts | Non-ACTIVE parent cannot establish context. Neither alternative permits effective child access to bypass B4; no cascade or delete is selected. Q8. |
| Leadership / assigned responsibilities | Review normal removal with mandatory handover before remove separately from emergency scoped suspension/access blocking before handover; an authorized person handles handover afterward, then remove if appropriate | Both paths PROPOSED: exact actor/delegation, responsibility prerequisites, audit/recovery, self/peer/last-ADMIN treatment and later-remove conditions remain UNKNOWN. No ADMIN content right, platform bypass or direct cross-service DB write; owning domain contracts required. Q1/Q3/Q7/Q8. |
| Sessions / caches / running work | Retain stored sessions subject to current eligibility checks; or explicitly revoke selected sessions/invalidate caches under an approved propagation contract | E10 refresh checks ACTIVE context before rotation; /me rechecks membership. Neither proves cancellation of in-flight work or a mutation-time race guarantee. Q6/Q8. |
| Resume / rejoin effects | Require explicit reassignment/revalidation; or restore an explicitly approved subset of retained scopes | Prior storage/RoleAssignment does not prove current membership or permission. Which subset and order remain UNKNOWN. Q3/Q8. |

Per-command ADMIN constraints need a separate choice for self-action, other
ADMIN targets and last eligible ADMIN. A conservative candidate is to reject a
command that would leave no eligible administrator; another is a separately
authorized transfer workflow. Neither is approved. Do not copy global User
`LAST_ACTIVE_ADMIN` or `SHARED_ACCOUNT_STATUS_CHANGE` as membership policy.
Product/Security must reconcile these safeguards separately for the proposed
normal and emergency cases; do not apply normal handover-before-remove as a
blanket prerequisite to emergency suspension. No emergency safeguard exception
or actor is approved, including for a peer or last ADMIN. Platform authority
alone remains insufficient under E12.

## 3. DATN-233 — concrete API candidates

Every method, path, field, status and visibility choice in this section is
[PROPOSED]; the accepted administration API is still UNKNOWN. The prefix follows
E11's existing `/api/v1/iam` convention; no route is added to source or OpenAPI.
Let `M` mean `/api/v1/iam/organizations/{organizationId}/memberships` below.

| Candidate HTTP surface | Candidate input → success result | Actor/scope and open gate |
|---|---|---|
| GET M | page, pageSize, optional single four-state status filter → 200 paginated MembershipSummary list | Own ACTIVE ADMIN/trusted Organization candidate; Q1/Q4 decide other readers, fields, totals/order/PII. |
| POST M/invitations | INV-A userId, optional reason → 201 pending MembershipSummary after accepted commit | Own ACTIVE ADMIN candidate, target reference/scope checked; INV-B needs a separate agreed DTO. Q1/Q2/Q5/Q7. |
| POST M/{membershipId}/activate | expectedStatus=PENDING_INVITE, verification prerequisite, optional/required reason to be decided → 200 ACTIVE MembershipSummary | ACT-B only; per-action authorization and proof UNKNOWN. Q1–Q3/Q5/Q7. |
| POST M/{membershipId}/suspend | expectedStatus=ACTIVE, reason → 200 SUSPENDED MembershipSummary | Own ACTIVE ADMIN candidate with accepted target safeguards/effects. Q1/Q3/Q5–Q8. |
| POST M/{membershipId}/remove | expectedStatus=ACTIVE or SUSPENDED, reason → 200 REMOVED MembershipSummary | Same boundary plus accepted offboarding prerequisites. Q1/Q3/Q5–Q8. |
| Recipient accept; resend/cancel; resume/rejoin | No concrete route or DTO selected; enabled vs deferred requires section 1/2 decisions | Recipient scope differs from ordinary ACTIVE-context routes; do not silently route ACT-A through ACT-B. Q1–Q3/Q5–Q8. |

The proposed ADMIN boundary is B5 plus the current own ACTIVE/trusted-context
gate. Actual action codes, grant evaluation, deny precedence, target safeguards
and scope evidence must be approved per operation. No Project-create exception,
platform bypass, Team Leader delegation or seeded permission is inferred.

Candidate write allowlist: path IDs, INV-A userId, accepted reason, and an
explicit precondition such as expectedStatus. Reject unknown body fields such
as status, actorUserId, roles, permissions or cascade. Verify actor from server
credentials, organizationId against trusted context and membershipId against
its actual Organization; validate target references server-side. ID format,
reason necessity/length/format, and exact precondition contract remain Q5.
expectedStatus alone cannot detect an ACTIVE → SUSPENDED → ACTIVE stale cycle;
version/fence/ETag mechanism and actor/target authorization races remain UNKNOWN.

Illustrative INV-A request and pending summary (synthetic opaque ID placeholders;
these examples do not decide identifier validation or server field availability):

```json
{"userId":"<user-id>","reason":"Invite for approved project work"}
```

```json
{"membership":{"id":"<membership-id>","organizationId":"<organization-id>","userId":"<user-id>","status":"PENDING_INVITE","createdAt":"2026-10-05T00:00:00.000Z","updatedAt":"2026-10-05T00:00:00.000Z"}}
```

MembershipSummary above proposes relationship fields only. User name/email,
roles, invite credentials, delivery metadata and confidential content are not
assumed response fields; Q4/Q5 must decide projection. A list candidate reuses
page=1/pageSize=20/max=100 from E4, with a deterministic ID tie-breaker; exact
ordering, response envelope, totals and filter visibility still need approval.

GET must have read semantics. POST candidates are not automatically retry-safe;
decide business idempotency before clients retry after timeouts. This HTTP
distinction follows [RFC 9110 safe methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.1)
and [idempotent methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2);
it does not decide DATN duplicate/no-op policy. Q2/Q3/Q5 must choose same-request
replay vs conflict, key scope/expiry, different-payload reuse, concurrent keys,
response recovery and whether a retry emits another audit record. Details UNKNOWN.

| Failure candidate | Proposed HTTP review choice | Exact unresolved rule / safe outcome |
|---|---|---|
| Missing/invalid ordinary authentication | 401 using accepted auth behavior where applicable | Recipient authentication is separate; no reuse of ordinary auth errors without Q1/Q2/Q6. |
| Valid identity lacking operation permission | 403 | Q1/Q6 decide whether target existence can be disclosed and error precedence. |
| Missing or cross-Organization/not-visible target | Uniform 404 candidate to limit enumeration, or approved explicit denial distinction | Q4/Q6 must choose; no membership lookup/data disclosure before applicable authorization. |
| Invalid input/unknown field | 422 following E4 | Q5/Q6 exact field details, limits and ordering vs authentication/scope checks. |
| Duplicate pair, stale state or illegal transition | 409 candidate | Q2/Q3/Q5/Q6 must distinguish retry success, business conflict and excluded operation. |
| Invitation credential failure | Generic safe failure; status/code UNKNOWN | Decide expiry/replay/recipient mismatch and disclosure, not an authentication bypass. Q2/Q6. |
| Rate or persistence/audit failure | 429 or 5xx candidates according to accepted cause | Q6/Q7 exact code/status/headers/recovery; do not return mutation success before required atomic commit. |

Envelope candidate reuses E4's `code`, `message`, `details`, `requestId`; no new
error code is assigned here. Decide precedence with mixed failures (invalid
credential + malformed body; unauthorized + unknown target; stale state + lost
permission), redacted details and FE behavior before freezing OpenAPI.

## 4. Audit gate — preserve the existing invariant

B6/E9 and contract section 6/Q7/AT-07 already require preserving IAM mutation
and audit atomicity in continuum_audit. This requirement is not an option in
the worksheet. Missing canonical ADR-003/SPEC-001 authority/revision and exact
Organization applicability block reconciliation, not enforcement of the existing
instruction. No eventual-audit alternative or implicit exception is proposed.

Architecture/DB + IAM + Security must supply the owning authority and resolve
collection, event/action identifiers, payload fields, transaction mechanism/
boundary, rollback/error/retry/deduplication, rejected-attempt audit, retention
and any outbox/consumer contract. **All these specifics remain UNKNOWN**; the
Project adapter/transaction is evidence only, not a selected Organization design.
Exclude credentials/protected content from audit. For the accepted implementation,
E9 requires real replica-set commit/rollback proof before cutover; document
consistency or mocked refresh tests do not supply that evidence.

## 5. DATN-234 — detailed review and future verification cases

These are review cases and a future test specification, **not executed runtime
tests**. Contract review can validate a complete accepted rule table and test
oracles without waiting for DATN-87 implementation; runtime evidence belongs to
the appropriate DB/BE/FE tasks. An UNKNOWN oracle cannot be reported as PASS.

| Case / subtask mapping | Setup and action to review | Settled constraint / required oracle |
|---|---|---|
| RV-01 / AT-01–03 / 229–230 | Four synthetic memberships plus role-only User; resolve zero/one/multiple contexts and a foreign selector | B1–B4; only ACTIVE supplies context; no role fallback; permission separate. Existing source tests inspected, not executed. |
| RV-02 / AT-04 / 231 | Verify approved account source and safe ADMIN recipient selection, including outside/nonmember User; invite known/unknown identity; accept/activate with correct/wrong identity, expired/replayed credential and failed delivery. After future accepted activation, attempt Project create with roles=[] and with configured/missing/misconfigured MEMBER Role | INV-A conditional prerequisites and chosen INV/ACT/DEL proof/state/safe response require Q1–Q3/Q4–Q7. No context before ACTIVE. E14 allows roles-empty Project-create authorization with active subject/trusted matching context and no project.create grant; other input/deny rules apply. Correct MEMBER Role with project.read permits bootstrap; missing/misconfigured Role rolls back creation. C-01 runtime case unexecuted. |
| RV-03 / AT-05 / 232/234 | Enumerate all 16 ordered state pairs, first creation and repeat commands; apply each enabled/excluded/deferred rule | Accepted command/actor/precondition/result/error for every cell, including same-state and REMOVED pair handling; Q3/Q5/Q6. |
| RV-04 / AT-03/06 / 232/233 | ADMIN in another Organization, inactive actor, MEMBER/Team Leader, self/peer/last-ADMIN target | B4/B5 boundaries plus accepted per-command safety/error rules Q1/Q3/Q6; no cross-Organization effect or copied User policy. |
| RV-05 / AT-05/07 / 233/234 | Two invites to one pair, two concurrent mutations, same/different retry payloads; actor loses authority or target cycles states after precheck | Approved idempotency/fence/error oracles Q3/Q5/Q6/Q7; unique/partial-write safety; mechanism remains UNKNOWN. |
| RV-06 / AT-07 / 233/234 | Fault required domain write and audit write independently; retry and simulate uncertain commit response | Existing atomicity preserved; exact persistence/retry/error oracles Q7 must be approved; real replica-set commit/rollback before cutover. |
| RV-07 / AT-08 / 232/234 | Review normal mandatory handover before remove and emergency scoped suspend/access block before authorized handover, then later remove if appropriate. Cover handover failure, peer/last-ADMIN, issued tokens, caches, child records, running work and resume/rejoin | B2/B4 deny new context; E10 is refresh source evidence only. Both proposed paths need exact actor/delegation/safeguard/audit/recovery and later-remove oracles Q1/Q3/Q6–Q8. No blanket handover gate may silently defeat the proposed emergency path; no exception, propagation SLA or restoration approved. |
| RV-08 / AT-09 / 233/234 | All-state list filters, boundaries/empty pages, foreign IDs, PII projection and server-denied FE actions | Approved Q4–Q6 DTO/visibility/pagination/error assertions; no secret/foreign data. FE loading/empty/error and permitted actions belong to DATN-88. |

## 6. Decision record and completion responsibility

| Review package | Required owning authority (names not yet confirmed) | Record needed / downstream blocked |
|---|---|---|
| Q1/Q2: identity, INV/ACT/DEL choices and command authority | Product + IAM/auth + Security; Notification/DB when relevant | Exact choice/amendment/exclusion, proof and permissions; DATN-231/233 and invite/activation in 87/88. |
| Q3/Q8: 16-cell rules and effects | Product + IAM + Security + affected Project/Team/Task/knowledge/handover owners; DB consistency | Full transition outcomes, safeguards and effects/recovery; DATN-232/234 and dependent domains. |
| Q4–Q6: concrete HTTP/DTO/visibility/errors/retries | IAM/API + Product + Security, FE consistency review and DB where needed | Accepted per-command and list contract, mixed-failure precedence and concurrency guarantees; DATN-233/234, then 87/88. |
| Q7: canonical reconciliation and audit specifics | Architecture/DB + IAM + Security | Owning ADR-003/SPEC-001 revisions and exact Organization scope; preserved invariant plus approved implementation details; auditable mutation work remains blocked. |
| Final contract acceptance | Named authorities above, coordinated by Phuc as contract owner | Review exact revised artifact and resolve required Q gates; technical review alone does not complete parent. |

Use one record per decision (no fields are pre-approved): decision ID/Q mapping;
selected option or exact amendment; enabled/excluded/deferred scope; accepted
rule and error/side-effect oracle; owning authority and named approver; date;
canonical source/revision; affected API/DB/test cases; remaining UNKNOWN and
downstream exclusions. A GitHub review must identify the decisions it accepts;
an unqualified technical LGTM does not establish all Product/Security authority.

Phuc prepares/reconciles the contract; Danh can confirm context implementation
evidence; Tien reviews FE consumption. Those responsibilities do not establish
Product, Security or DB decision authority. Confirm the actual roster first.
After accepted decisions are recorded, review DATN-229–234 separately and update
each status when its acceptance is met; then assess DATN-86's reviewed-contract
result. Any permitted deferred scope must be explicitly approved and retained as
a downstream blocker, not silently counted as a completed required operation.
