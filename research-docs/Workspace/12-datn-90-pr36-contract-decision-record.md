# DATN-90 / PR #36 — Contract Decision Record

- **Revision:** 1, 2026-10-15 ICT
- **Purpose:** single approval ledger for TQ-05, TQ-07/08, TQ-09 and TQ-10.
- **Decision boundary:** proposed choices below are not operative contract until the named owner records approval. This record does not amend an accepted contract, grant permissions, enable Team writes, or change Jira/PR status.

## Authority and status rules

- The current C-04 decision record is [DATN-89 report §10.1](09-team-management-foundation-decision-gap-report.md#101-jira-decision-update--2026-10-14). Its 2026-10-14 Jira readback records TQ-05–08 as **AMEND**, TQ-09 contract semantics as **APPROVE / mutations DEFER**, and TQ-10 as **DEFER**.
- DATN-90 R4 is a proposal, not approval: [R4 §§1–3](11-team-foundation-runtime-options-r4.md#1-reviewer-cần-duyệt-gì), [§§4–7](11-team-foundation-runtime-options-r4.md#4-p1p2--exact-quyền-và-phạm-vi). Its candidate OpenAPI is marked `PROPOSED_NOT_APPROVED`.
- `[APPROVED]` below means an existing, traceable owner decision in the cited authority. `[PROPOSED]` means the requested direction is recorded for owner selection. Runtime tests, CI, document merges, and reviewer comments do not approve policy.
- The only new status authority is an explicit decision by the owner role listed per finding, linked to this record with the selected option or exact amendment and date. Until then the proposed behavior is not an authorization to expose or mutate Team data.

## Decision ledger

| Finding | Required reviewer resolution | Decision/status in this record | Approval owner |
|---|---|---|---|
| TQ-05 | [PR #36 thread](https://github.com/DATN-SPRING2027/DATN-BE/pull/36#discussion_r4284523266): Team-leader delegation scope and its representation must be explicit; no implicit child-Team authority. | **PROPOSED — P1=A**, details in §1; existing C-04 disposition remains AMEND. | C-04 Team contract owner with IAM/authorization and Security owner |
| TQ-07 | [PR #36 thread](https://github.com/DATN-SPRING2027/DATN-BE/pull/36#discussion_r4284523277): freeze route/DTO/query/transport and boundary before treating routes as exposed. | **PROPOSED — P3=A**, details in §2; existing C-04 disposition remains AMEND. | IAM/API contract owner with Gateway/BFF and Team product owner |
| TQ-08 | [PR #36 thread](https://github.com/DATN-SPRING2027/DATN-BE/pull/36#discussion_r4284523277): reconcile error mapping, precedence, authorization context and concealment with the owning contract. | **PROPOSED — P4=A**, details in §3; existing C-04 disposition remains AMEND. | IAM/Auth API and Security contract owners |
| TQ-09 | [PR #36 thread](https://github.com/DATN-SPRING2027/DATN-BE/pull/36#discussion_r4284523244): keep mutation disabled until provider, writer-coverage and ambiguous-commit recovery evidence exist. | **APPROVED — contract semantics only** by DATN-89 §10.1; runtime readiness remains **NOT READY**. | No new policy choice requested; IAM/DB/Security owners must accept runtime evidence before any enablement |
| TQ-10 | [PR #36 thread](https://github.com/DATN-SPRING2027/DATN-BE/pull/36#discussion_r4284523263): do not retain a Team audit writer/index without an approved canonical event mapping. | **DEFERRED** by DATN-89 §10.1. **PROPOSED — Option A** is a target for owner decision only; no writer or index is authorized. | Audit/Architecture and IAM/DB contract owners, with Security and Team product owner |

## 1. TQ-05 — delegation and action permissions

**Existing contract references:** DATN-89 report §2, rule B4; §6 and TQ-05 in §10; R4 §4/P1; existing [role-scope baseline](../02_ACTORS_ROLES_AND_PERMISSIONS.md). B4 says a TEAM_LEADER acts only in explicitly assigned/delegated scope and does not gain Team authority from ADMIN/platform status. R4 P1 remains unselected; its option A requires an action grant plus `team:children.manage` and `team.read` for reads.

**Reviewer request:** determine the authority and representation for project-scoped TEAM_LEADER actions on child Teams. The review notes no Team-specific grant representation and rejects treating a role label or Project relationship as an unbounded grant.

**Proposal — P1=A:** one explicit, current TEAM_LEADER assignment scoped to the exact `(organizationId, projectId)`, with `team:children.manage` and the action-specific permission (`team.create`, `team.update`, `team.archive`, or `team.restore`) for that operation. `team.read` is required for list/detail only. The grant applies only to child Teams in that exact Project; a sibling Project, another Organization, ADMIN/platform authority, Project creator status, public visibility, or Team membership does not grant access. Missing/unknown permission, deny, inactive membership, mismatched parent or stale assignment denies. No grant is provisioned by this proposal.

**Existing source evidence:** at BE PR #36 head [`b4a7e21`](https://github.com/DATN-SPRING2027/DATN-BE/tree/b4a7e21bef5d49be977b32a7c021f03866215080), [`team-authorization.policy.ts`](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/services/iam/application/teams/team-authorization.policy.ts#L96-L115) filters RoleAssignment by Organization and Project and checks `TEAM_LEADER` plus `team:children.manage`; there is no Team ID grant check. It requires `team.read` for `team.read`, but does not enforce an operation-specific permission for mutations. Existing-Team mutations also pass [repository visibility/read authorization](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/services/iam/infrastructure/mongodb/team-foundation.repository.ts#L500-L559). Thus current code's Project-wide child scope is broader than the proposed permission matrix; it is not evidence that the matrix is approved or safe to enable.

**Security/compatibility:** the proposal preserves the approved explicit-scope/default-deny boundary and avoids a new Team-grant schema, but assigns each explicitly delegated Project leader authority across all child Teams within that Project. Action-specific checks narrow write rights compared with the current code. Changing the policy may deny requests that previously passed the policy; do not weaken reads or grant rights to make those requests succeed.

**Remaining unknowns:** which role/permission provisioner may create and revoke the explicit Project delegation; whether the existing-Team `team.read` visibility check is also required before each mutation; effective-deny source and freshness; whether any Team-only grant is in scope later. No cross-Project authority is proposed.

**Owner question:** “Approve P1=A exactly as specified, including all-child-Team scope within one explicitly assigned Project and action-specific write grants, or require a Team-specific grant representation and keep access denied until it exists? If approving A, confirm the authorized grant/provisioning owner and whether `team.read` is a prerequisite for existing-Team mutations.”

**Options / recommendation:** A = approve the bounded Project delegation above; B = require Team-specific grant/scope and retain deny-by-default; `AMEND` = record exact permission/scope matrix. Recommend A because it uses the existing Organization+Project scoped RoleAssignment and limits authority to a single Project, while adding action-level checks. Recommendation is not approval.

**If unresolved:** no Team grant is provisioned; this assignment is not treated as Team authority, and the proposed authorization behavior is not ready for release.

## 2. TQ-07 — six-operation API baseline

**Exact references:** DATN-89 report §7 and TQ-07 in §10; R4 §5/P3; candidate [`c-05-team-foundation-r4.openapi.json`](contracts/c-05-team-foundation-r4.openapi.json), currently `PROPOSED_NOT_APPROVED`; existing IAM OpenAPI at BE `docs/openapi/iam-v1.openapi.json` defines the shared IAM wire conventions but does not itself approve Team routes.

**Reviewer request:** settle each Team route, DTO, query, success/error shape and browser/Gateway/IAM transport boundary before treating the six handlers as an exposed API.

**Proposal — P3=A:** retain six R4 operations under `/api/v1/iam`: `POST /projects/{projectId}/teams`, `PATCH /teams/{teamId}`, `GET /projects/{projectId}/teams`, `GET /teams/{teamId}`, `POST /teams/{teamId}/archive`, and `POST /teams/{teamId}/restore`. Accept the R4 §5 strict DTO/query/header rules, page 1 / size 20 / max 100, manager status filter, stable order, strong `If-Match` on existing-Team mutations, `Idempotency-Key` on mutations, and the documented ETag/Location/replay/retry response headers. Browser requests continue through the trusted BFF→Gateway→IAM boundary; the decision does not create a bearer bypass.

**Existing source evidence:** PR #36 implements these six [controller routes](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/services/iam/controllers/team-foundation.controller.ts#L81-L227) and DTO/query candidates; [Gateway forwarding](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/gateway/gateway-iam.controller.ts) and response handling are covered by current source/tests. This implementation is compatibility evidence only. R4 §5 itself records the Gateway/BFF/IAM transport checks still required; the candidate OpenAPI and routes are not accepted by virtue of being implemented.

**Security/compatibility:** accepting P3=A makes current candidate paths and request semantics a public compatibility surface. Header loss, body/query divergence, or a later route amendment would affect FE/BFF clients. Existing auth/context and CSRF checks remain required; no alternate caller identity source is introduced.

**Remaining unknowns:** explicit confirmation from API/Gateway/BFF/IAM owners that all six operations, DTO bounds/null behavior, status filtering, concurrency headers, CSRF and forwarded response headers match production routing. Any omission must be a precise `AMEND`, not silent drift.

**Owner question:** “Approve P3=A and all six operations with the request/response/query/header semantics in R4 §5, including BFF→Gateway→IAM forwarding, or choose the reduced ACTIVE-only list option / provide an exact AMEND for route, field, status, query or header?”

**Options / recommendation:** A = accept R4 §5 as written; B = ACTIVE-only paging for list and defer archived filtering; `AMEND` = exact final API matrix. Recommend A because it matches the current six-operation implementation and includes explicit preconditions and idempotency; it remains pending owner approval.

**If unresolved:** the six routes remain implementation candidates, not an accepted public API; DATN-255–259 acceptance remains pending.

## 3. TQ-08 — shared error response and precedence

**Exact references:** DATN-89 report §7 and TQ-08 in §10; R4 §6/P4; IAM `ErrorResponse` in `docs/openapi/iam-v1.openapi.json#/components/schemas/ErrorResponse`; authentication/context conventions in `docs/decisions/auth-session-contract-a-01.md` and current `StructuredExceptionFilter`.

**Reviewer request:** finalize per-operation error status/code, authorization context, 403/404 concealment and error precedence against the owning IAM/auth contract; do not expose Team-specific behavior from an unapproved candidate.

**Proposal — P4=A:** reuse `{code,message,details,requestId}` and current IAM authentication/context error behavior. Adopt R4 §6 mappings, including 401 for invalid auth/context, 403 for CSRF or visible resource without action, scoped 404 for missing/invisible resources, 422 for malformed input/required command header, 409 for duplicate/key-reuse/state conflicts, 428/412 for missing/stale precondition, and sanitized 500/503 for command/readiness failure. Precedence: authentication/context → CSRF on mutation → path/body/query shape → scoped visibility → current action/delegation → command-header syntax/key replay → new-command version → state → transaction/fence/write. Conceal hidden parent/Team before exposing key/version state.

**Existing source evidence:** IAM OpenAPI [`ErrorResponse`](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/docs/openapi/iam-v1.openapi.json#L1961-L1976) and [`StructuredExceptionFilter`](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/common/http/structured-exception.filter.ts) provide the shared envelope; current Team controller/repository implement the candidate mapping and checks. They do not amend the owning IAM/auth contract or establish that the exact precedence is accepted for Team.

**Security/compatibility:** preserves the established 401 auth/context behavior and minimizes information disclosure for hidden resources. Changing to generic not-found or remapping auth context to 403 would alter IAM-wide client behavior and requires an owning auth-contract amendment.

**Remaining unknowns:** owner acceptance of each Team code/status and the ordering for simultaneous malformed/unauthorized/hidden/stale cases; Gateway rate-limit precedence remains under Gateway policy.

**Owner question:** “Approve P4=A with the shared IAM envelope and the R4 §6 status/code/precedence matrix, including 401 auth/context and scoped 404 concealment, or provide a per-case AMEND? Any generic not-found or 403 context change must also amend its owning IAM/auth contract.”

**Options / recommendation:** A = reuse shared IAM mapping and R4 precedence; B = generic `RESOURCE_NOT_FOUND` and `ORGANIZATION_CONTEXT_REQUIRED` only after the owning auth contract is amended; `AMEND` = exact case matrix. Recommend A because it preserves existing IAM authentication semantics and avoids an unapproved cross-contract remap.

**If unresolved:** do not treat Team status/code/precedence as contract-backed or accept API behavior that depends on the candidate mapping.

## 4. TQ-09 — approved command semantics, runtime readiness pending

**Exact references:** DATN-89 report §10.1 records TQ-09 contract `APPROVE` and mutation readiness `DEFER`; R4 §5 states scoped key/fingerprint, 24-hour application expiry, compare-and-set replacement, version preconditions and replay rules; R4 §8/P6 lists evidence required before runtime enablement. PR #36 review thread is linked in the ledger.

**Approved contract:** retain the accepted Team version/ETag and idempotency semantics: key scoped by Organization+actor+key, canonical command fingerprint, application-enforced 24-hour expiry and terminal-slot CAS, current authorization revalidation on replay, bounded recovery, no blind second mutation. No new contract decision is requested here.

**Runtime facts at BE head `b4a7e21`:** all four `TEAM_MUTATION_ENABLEMENT_EVIDENCE` booleans—`idempotencyProviderVerified`, `idempotencyWriterCoverageVerified`, `ambiguousCommitRecoveryVerified`, and `canonicalAuditContractAndWriterVerified`—remain `false`; the [gate](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/services/iam/infrastructure/mongodb/team-foundation.repository.ts#L58-L65) is closed before [`team_operations` access/session start](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/services/iam/infrastructure/mongodb/team-foundation.repository.ts#L298-L342), after authorization preflight reads. Source uses the IAM `Connection` to create one session for `withTransaction`; Team, idempotency and authorization-fence writes receive that session. [`TeamAuthorizationEvidence`](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/services/iam/infrastructure/mongodb/team-foundation.authorization-evidence.ts#L22-L75) reads current auth facts and [fences them in-session](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/services/iam/infrastructure/mongodb/team-foundation.authorization-evidence.ts#L170-L238). The current source inventory finds the repository runtime writer and a separate [one-time Team normalization writer](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/scripts/migrations/20261015-team-foundation-runtime.mjs#L129); external/import/manual/repair writers and deployment wiring remain unknown. The disposable local MongoDB 7 replica-set suite verifies **8/8** cases: fail-closed behavior despite collection/index presence; committed replay and changed-payload rejection; same-key concurrency; expired-slot CAS replacement; rollback on command-result write failure; duplicate-code rollback; ambiguous commit acknowledgement followed by same-key replay; and scoped list/detail reads. The focused unit/controller/gateway set reports **34 passed, 8 integration cases skipped** (the separate replica-set runner executes those integration cases). These results do not verify the deployed provider/topology or every writer.

**Security/compatibility:** current production behavior remains fail-closed with no Team mutation. Enabling writes before full provider/writer/recovery/audit proof could duplicate or partially expose mutation outcomes. Application expiry is the correctness rule; a TTL index is cleanup only.

**Remaining readiness evidence:** (1) deployed session-bound provider, topology and transaction options; (2) exhaustive runtime/import/repair/manual writer inventory and fences; (3) production-equivalent replay/recovery under retry, concurrency and expiry; (4) ambiguous commit resolution under actual supported failover/network behavior. TQ-10 canonical audit decision/writer is an additional false prerequisite. The mutation function performs authorization preflight reads before the readiness check, so the correct claim is that command-result access/session/write and Team mutation are gated—not that no DB read occurs.

**Owner action:** IAM/DB/Security owners review and accept the runtime evidence package after provider/deployment and writer inventory are verified. This is an evidence acceptance for the already approved contract, not a request to re-decide its semantics.

**If unresolved:** the four readiness predicates stay false and Team mutation remains disabled.

## 5. TQ-10 — Option A audit decision proposal (still DEFER)

**Exact references:** DATN-89 report §2/B6 and TQ-10 in §10; R4 §7/P5 and §8 audit readiness; accepted BE `docs/decisions/project-audit-collection-mvp.md`; Project implementation in `src/services/iam/infrastructure/mongodb/project-access.repository.ts` and collection constants in `src/common/mongodb/database-names.ts` at PR #36 base/head source. Jira DATN-89 §10.1 keeps TQ-10 **DEFER**.

**Verified Project pattern:** Project Access writes through the existing IAM Mongo connection's [`useDb(AUDIT_DATABASE_NAME).collection(IAM_AUDIT_COLLECTION_NAME).insertOne(event, {session})`](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/services/iam/infrastructure/mongodb/project-access.repository.ts#L1276-L1302). The [constants](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/common/mongodb/database-names.ts#L15-L17) are `continuum_audit.audit_logs_iam`. The [accepted Project decision](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/docs/decisions/project-audit-collection-mvp.md) confirms its envelope and same-session Project transaction. The new isolated [`project-audit-atomicity.mongodb.spec.ts`](https://github.com/DATN-SPRING2027/DATN-BE/blob/b4a7e21bef5d49be977b32a7c021f03866215080/src/services/iam/infrastructure/mongodb/project-audit-atomicity.mongodb.spec.ts) injects an audit validation failure and verifies code 121, unchanged Project visibility and zero audit rows; after clearing the test validator it verifies a successful same-session Project+audit commit (**1/1 passed** on MongoDB 7 replica set). This establishes the existing Project pattern's local atomicity under the test conditions, not production topology or Team approval. Generic `audit_logs` is a separate collection. The Project decision does **not** select retention duration, a Team dedupe index, or Team event mapping; source behavior is not approval for those details.

**Proposed decision — Option A:** direct same-client/session write to `continuum_audit.audit_logs_iam` in the transaction with Team state and durable command result; do not introduce an outbox for the MVP. Proposed actions: `TEAM_CREATED`, `TEAM_METADATA_UPDATED`, `TEAM_ARCHIVED`, `TEAM_RESTORED`, with `targetResource=TEAM` and stable `targetResourceId=teamId`. Reuse `organizationId`, `projectId`, `actorUserId`, `action`, `occurredAt`; allowlist metadata to command ID, old/new version, lifecycle reason, old/new name/status and a `descriptionChanged` flag. Do not store full description, request body, credentials, profile copies or protected content. A replay/no-op creates no additional business event.

**Retention proposal:** the MVP writer inserts events and performs no TTL/delete operation. The audit/data-retention owner must define the retention duration, archival/deletion authority and applicable legal/PITR handling before writer enablement; Project implementation supplies no answer. This proposal does not imply indefinite retention.

**Dedupe proposal:** separate DB PR for a unique partial index on `{ organizationId: 1, 'metadata.commandId': 1, action: 1, targetResourceId: 1 }`, filtered to `{ targetResource: 'TEAM', 'metadata.commandId': { $exists: true } }`. This constrains Team command events and avoids imposing uniqueness on existing Project records. Verify legacy shape/collation/index compatibility before migration; no index is created by this record.

**Transaction participants:** business write set: `continuum_iam.teams`, `continuum_iam.team_operations`, and proposed `continuum_audit.audit_logs_iam`. Current same-session authorization reads/fences cover `users`, `organization_memberships`, `projects`, `project_memberships`, `role_assignments`, and `roles`; `TeamAuthorizationEvidence.fenceAuthorization` issues conditional `__v` writes to those six IAM collections. The DB/architecture owner must validate actual fence participants and topology. Option A requires a cross-database Mongo transaction and aborts Team state and command result if audit insert fails. Existing Project code demonstrates the session-passing pattern, not deployed Team atomicity.

**Security/compatibility:** Option A preserves synchronous atomic audit and avoids eventual-delivery gaps; a new audit index/collection policy is a database change requiring a separate DB PR and compatibility/recovery plan. The allowlist limits sensitive data. No writer/index/migration may ship while this contract stays deferred.

**Remaining unknowns:** authoritative ADR-003/SPEC-001 revisions and their applicability; approved Team event field set/reason semantics; explicit retention duration and disposal/archival; index key compatibility with legacy audit records; deployed cross-database transaction support; dedup behavior for duplicate command recovery; denied-attempt audit and history consumer requirements. The project evidence does not settle these.

**Owner question:** “Approve Option A with the event mapping, allowlist, same-session participants and Team-scoped partial dedupe index above, and select the retention duration/archival policy; or amend the exact fields/index/participants/retention; or keep TQ-10 DEFER? Option B outbox is an alternative only if the owning audit invariant is explicitly amended to define relay, idempotency, lag and recovery.”

**Options / recommendation:** A = approve direct same-session canonical audit after specifying retention; B = amend B6 and approve atomic outbox+relay contract; C = retain DEFER and keep mutation gate closed. Recommend A because it follows the accepted Project collection/session pattern and preserves synchronous atomicity, contingent on an explicit retention decision. TQ-10 remains DEFER until owner approval is recorded.

**If unresolved:** TQ-10 remains DEFER, no Team audit writer/index/migration is introduced, and mutation enablement stays closed.

## Acceptance and reviewer response boundary

DATN-89 [review-validation §4](10-team-foundation-review-validation.md#4-datn-90-and-downstream-implementation-gate) maps DATN-255–259 to contract-backed runtime evidence. At this record revision, **none is accepted as runtime complete**:

| Ticket | Status | Required closure evidence |
|---|---|---|
| DATN-255 Create Team | Pending contract and mutation prerequisites | Approved TQ-05/07/08/10; live isolated acceptance for auth, create, replay, audit atomicity and rollback |
| DATN-256 Update Team | Pending contract and mutation prerequisites | Approved DTO/grants/errors; ETag concurrency, replay, audit and rollback proof |
| DATN-257 List/detail | Source/unit evidence only; acceptance pending | Approved visibility/projection/query/errors and runtime cross-scope/denial evidence |
| DATN-258 Delete/deactivate (approved archive/restore lifecycle) | Lifecycle choice is recorded in DATN-89 TQ-02, but runtime acceptance pending; no hard delete is authorized | Approved auth/API/audit contract; restore/history, concurrency and rollback proof |
| DATN-259 API tests | Partial local evidence only | Full accepted TV-18–21 and acceptance matrix on the supported isolated runtime, with contract owner sign-off |

The response drafts below are not posted. Request re-review only after the relevant owner decision or new evidence is attached, and keep the ask scoped to that change/evidence. Do not resolve any review thread without reviewer confirmation.

### Prepared reviewer replies (not posted)

- **TQ-05:** “At BE head `b4a7e21`, `team-authorization.policy.ts` confirms Project-scoped assignment filtering but no Team-specific grant or operation-specific mutation permission. We have not widened scope or provisioned access. P1=A is only proposed; please re-review authorization behavior after the IAM/Security owner records the grant matrix and the implementation enforces it.” **Do not request re-review yet.**
- **TQ-07/08:** “R4 P3=A/P4=A and the six routes/error matrix are now captured as proposals in the DATN-90 decision ledger; DATN-89 still records AMEND. The source and tests match candidates but do not approve their public contract. Please re-review after API/Auth owners accept or amend the route/DTO/transport/error matrix.” **Do not request re-review yet.**
- **TQ-09:** “Commit [`b4a7e21`](https://github.com/DATN-SPRING2027/DATN-BE/commit/b4a7e21bef5d49be977b32a7c021f03866215080) adds isolated replica-set cases for expired-slot CAS replacement, rollback on command-result write failure, and one committed Team/result after a simulated lost commit acknowledgement before same-key replay. The readiness predicate remains fail-closed. Provider deployment and complete writer inventory remain unverified, so no runtime readiness or mutation enablement is claimed.” **A scoped re-review of the new test evidence is appropriate; do not resolve the runtime-readiness finding.**
- **TQ-10:** “BE commit [`9bfd7d8`](https://github.com/DATN-SPRING2027/DATN-BE/commit/9bfd7d823b57f930db1bd0cd1b06958a9db8adb3) removed the Team audit writer and audit-index prerequisite. Existing Project source and the new local failure-injection test support the same-session atomicity pattern, but Team mapping, retention and dedupe remain unapproved. TQ-10 stays DEFER and Option A is only proposed.” **A scoped review of the writer/index removal is appropriate; do not ask the reviewer to approve the audit proposal.**

## Approval log

| Finding | Status | Owner / authority evidence | Date / revision |
|---|---|---|---|
| TQ-05 | PROPOSED | Existing DATN-89 §10.1 says AMEND; no P1=A owner approval recorded | — |
| TQ-07 | PROPOSED | Existing DATN-89 §10.1 says AMEND; no P3=A owner approval recorded | — |
| TQ-08 | PROPOSED | Existing DATN-89 §10.1 says AMEND; no P4=A owner approval recorded | — |
| TQ-09 | APPROVED contract / runtime NOT READY | DATN-89 §10.1 Jira decision update, 2026-10-14; runtime approval not recorded | 2026-10-14 / current readiness evidence pending |
| TQ-10 | DEFERRED; Option A PROPOSED | DATN-89 §10.1; no audit/contract owner approval recorded | — |
