# DATN-301 — Decision record: PLATFORM_OPERATOR V1 gate closure

| Field | Value |
|---|---|
| Jira | DATN-301 |
| Canonical contract | [PLATFORM_OPERATOR V1 contract](../platform-operator-v1-contract.md) |
| DB verification | [Read-only runbook](../platform-operator-v1-db-verification-runbook.md) |
| Date | 2026-10-16 (Asia/Bangkok) |
| Jira status | Done; this status is administrative and is not evidence of owner/security sign-off |
| Decision status | Policy scope closed; Security/IAM, Audit and deployed DB evidence remain external |
| Decision owner | KeyT/Thang for the explicit gate-closure and conservative V1 scope decision |

## 1. Outcome

The V1 permission catalog is exactly the three existing DATN-79/A-04 codes:

- organization.create
- platform.health.read
- platform.audit.read

The 37 remaining DATN-294 candidate operations have each been explicitly dispositioned DEFERRED FROM V1 in the canonical contract §4.3. Their permission names remain only as a traceable candidate inventory. They are not grantable, implemented, shown in FE, or tested as V1 capabilities. The three A-04 operations keep their existing runtime semantics. DATN-79 is unchanged.

The earlier reading of D1 as a live 40-code grant bundle is superseded for implementation by this narrower active catalog. The 40 identifiers remain recorded for traceability, but effective permission count is three. There is no full-40 atomic bundle in V1.

## 2. Four-gate status

| Gate | Requirement | Current state and evidence | Decision | Owner | Status | Affected tasks |
|---|---|---|---|---|---|---|
| Security / IAM | Identity, issuer/executor, authorization, bootstrap, re-bootstrap, recovery, grant/revoke, concurrency, idempotency, rollback, last-operator and verification | A-04 confirms active user/current exact permission checks and separate platform auth context; no named issuer, executor or bootstrap approval exists in inspected Jira/source | PO-AUTH-01 is a two-person controlled procedure for exactly three A-04 codes; details in §4 | Security/IAM owner must name approvers/executor | EXTERNAL APPROVAL REQUIRED | 295, 300 |
| Audit | Event coverage/fields, redaction, retention, read/export/denial, integrity, failure semantics | Organization create audit shares a Mongo transaction; schema supports Mixed metadata; no global retention, storage immutability or universal coverage evidence | Required PO-AUTH-01 event fields and fail-closed policy are specified; propose 365 days, encrypted WORM/archive and dual-control deletion; preserve existing A-04 behavior | Security/IAM, Security/Audit, Privacy/Legal | EXTERNAL APPROVAL REQUIRED | 295, 300 |
| Operation disposition | Every candidate is ACTIVE or DEFERRED | DATN-79 and runtime contain only three operations; the 37 new rows lack complete runtime source and test oracles | Preserve the three A-04 operations; explicitly defer all 37 candidates | KeyT/Thang, under this closure request | READY | 293–300 |
| DB reality | Verify actual collection/index/validator/assignment/migration state read-only | Only connectionStatus was called; it returned atlasAdmin and readOnly=false. No collection was queried | Keep DB state UNVERIFIED; run the read-only runbook using approved staging/prod credentials | IAM DB owner / Data Platform | EXTERNAL APPROVAL REQUIRED | 295, 300 |

## 3. Decision register

| ID | Decision | Status | Rationale | Evidence | Impact | Owner | Affected tasks | Exit / rollback |
|---|---|---|---|---|---|---|---|---|
| PO-D01 | Preserve three A-04 permission codes and semantics | APPROVED | DATN-79 is the current authorization boundary; V1 must not widen it implicitly. | DATN-79/A-04 and current IAM guard/controller. | Keeps exactly the three existing permissions and routes unchanged. | KeyT / DATN-79 owner | 294–300 | Revisit only through a new approved contract before changing runtime authority. |
| PO-D02 | Defer all 37 new candidates; effective V1 permission count is three. | APPROVED | Candidate semantics lack complete owner-approved operation and QA oracles; the task requires a final disposition. | Explicit closure request; DATN-79/A-04 and inspected runtime expose only three platform permissions/operations. | Excludes 37 candidates from grants, BE/FE scope and V1 QA; allows 296–300 to start with narrow scope. | KeyT/Thang under this closure request | 293–300 | Any candidate reopens only with a new approved operation contract and QA oracle. |
| PO-D03 | No hierarchy, wildcard, Break-glass, self-grant, operator-to-operator grant or public grant/revoke API. | APPROVED | These are explicit V1 scope constraints and preserve the existing A-04 boundary. | User task scope; DATN-79/A-04. | Adds no role expansion, public authority endpoint or bypass path. | KeyT/Thang | 293–300 | Any exception requires a separate approved decision before implementation. |
| PO-D04 | PO-AUTH-01 two-person bootstrap/recovery/revoke; immutable IdP identity, fresh MFA, legacy-row guard and last-operator protection. | PROPOSED | No named issuer/executor or approved bootstrap workflow exists in inspected sources. | Complete procedure in canonical contract §8; no signers found. | No bootstrap tooling or production use until Security/IAM names and signs the controls. | Security/IAM | 295, 300 | Reject before write on any failed precondition; transaction aborts on failure; recover only through the same signed two-person process. |
| PO-D05 | Assignment rows, operation ID and required audit commit atomically; stale CAS is 409; audit failure rolls back. | DERIVED | Partial authority writes would leave ambiguous operator state; the existing A-04 transaction supplies a precedent. | A-04 transaction/rollback tests and source assignment unique index. | DATN-295 must use one transaction and stable operation ID; QA tests replay, race and rollback. | Security/IAM + DB | 295, 300 | Abort the transaction on any write/audit failure; no compensating partial grant. |
| PO-D06 | Audit coverage, fields, redaction, access, denial and failure behavior. | DERIVED | Existing schema and A-04 transaction establish a baseline, not global retention or storage integrity. | Current IAM audit schema, Organization-create transaction and fixed A-04 audit projection. | Required PO-AUTH-01 mutation audit is fail-closed; no recursive business-read event or active export; security telemetry stays sanitized. Existing PLAT-ORG-01 behavior remains unchanged. | Security/Audit; IAM for implementation | 295, 300 | Fail closed on required-event failure; preserve current history and reconcile from a consistent recovery point. |
| PO-D07 | Propose 365-day retention, encrypted WORM/archive/backups and dual-control expiry deletion. | PROPOSED | No approved retention or archive policy was found. | Reviewed repository/Jira/decision sources; no policy evidence. | No retention/storage implementation is authorized until Security/IAM, Audit and Privacy/Legal approve or replace it. | Security/IAM + Security/Audit + Privacy/Legal | 295, 300 | Replace the proposal only with an approved policy; delete only expired records under approved dual control. |
| PO-D08 | Active V1 has no concealed target class; 403 default and no new 404. | DERIVED | Active A-04 endpoints have no target selector; first-ADMIN unavailability uses a shared safe conflict. | Current route shapes and A-04 behavior; active-scope matrix in canonical contract §7. | BE/FE/QA share a deterministic 401/403/409 oracle; shared DEC-ACCESS-10 remains open for other resources. | KeyT; global resource owner for other classes | 294, 296–300 | A newly activated target resource requires an explicit concealment decision before use. |
| PO-D09 | Configuration is OUT OF V1. | APPROVED | The earlier domain mention conflicts with the existing configuration deferral. | DEC-ACCESS-09 and the explicit V1 scope decision. | No configuration permission, route, UI or QA capability is active. | KeyT | 293–300 | Reopen only with a new decision and a full secret/configuration boundary contract. |
| PO-D10 | Deployed DB state is UNVERIFIED; obtain a read-only report before migration. | EXTERNAL APPROVAL REQUIRED | The available probe used a non-read-only development credential and queried no collection state. | `connectionStatus` role evidence; exact verification runbook. | DATN-295 cannot migrate or claim deployment readiness until staging/prod evidence is attached. | IAM DB owner / Data Platform | 295, 300 | Stop on missing access or mismatch; no repair in this task; proceed only after reviewed evidence and approved rollout/rollback. |
| PO-D11 | Preserve legacy A-04 rows; alter only rows with controlled-procedure provenance. | PROPOSED | Source data has no approved provenance marker and unique index forbids duplicate subject/code/scope rows. | Assignment schema/index source; no live rows were read. | No silent adoption, rewrite, deletion or unrelated permission change; conflict aborts the controlled operation. | Security/IAM + DB | 295, 300 | Abort without mutation on unproven rows; retain legacy state and resolve via a separately approved migration plan. |
| PO-D12 | PLATFORM_OPERATOR is one conceptual actor with no tiers; its complete active V1 bundle is the exact three A-04 assignments. | APPROVED | The confirmed constraint requires one full Platform Administration V1 actor; the selected active catalog contains exactly three current A-04 permissions. | Explicit task constraint; current A-04 exact-permission guard and assignment model. | Resolve each request by exact current PLATFORM assignment; no role-label expansion or additional candidate permission. | KeyT / IAM | 294–300 | Any tiering or bundle change requires a new approved contract before implementation. |

## 4. Security/IAM bootstrap decision package

PO-AUTH-01 is an internal change-controlled procedure, not a new permission, public API, UI, seed, hidden account or Break-glass route.

1. Recipient is an existing ACTIVE DATN User resolved through configured IdP issuer+subject (iss+sub), never email alone.
2. Require fresh MFA. A named Security/IAM human issuer approves the exact action and codes; a separate named IAM maintainer executes. Recipient, issuer and executor are different identities.
3. The only grant set is the three A-04 permissions at PLATFORM scope, all-or-nothing. Existing A-04 login, refresh and per-request authorization remain unchanged.
4. Preflight checks identity, current user state, exact assignment rows, provenance, indexes, state hash, and last-operator condition.
5. Never adopt/rewrite a pre-existing A-04 row. Refuse rows without PO-AUTH-01 provenance. Revoke only exact row IDs recorded by its committed grant event.
6. Commit assignment change, unique operation ID and audit event in one Mongo transaction. Use pre-state CAS; stale operations return 409. Same operation ID/same payload is idempotent; reuse with another payload returns 409.
7. Never revoke the last ACTIVE user with all three current, unexpired codes. Commit and verify a replacement first.
8. After all operators are lost, only the same two-person issuer/executor process may re-bootstrap; no bypass.
9. On timeout, read by operation ID: matching event/state means committed; unchanged state with no event permits retry using the same ID; conflict or unavailable read returns 503 for manual reconciliation.
10. Verify exact three rows, scope/status/expiry, audit linkage and operator count after commit. Do not report success before verification.

No issuer/executor names or approval signatures were found; none is invented here.

## 5. Audit decision package

- Active mutation PLAT-ORG-01 must persist Organization, first ADMIN membership/role and required audit in one transaction. Any audit failure rolls back and returns no success.
- PO-AUTH-01 bootstrap/regrant/revoke events require actor, action, target, PLATFORM scope, timestamp, operation/request/change IDs, fixed reason, result, assignment IDs and safe before/after summary.
- Active PLAT-HEALTH-01 and PLAT-AUDIT-01 reads do not produce business-read events; no recursive audit event. Auth denials go to sanitized security telemetry; telemetry failure never allows access or changes 401/403.
- Never log credentials, tokens, MFA values, raw IdP assertions, prompts, job payloads, tenant content or unrestricted exceptions.
- Current schema proves append insertion but not storage immutability. Proposed retention is 365 days from event time, encrypted WORM/archive and backups, delete only after expiry via restricted dual-control worker. Platform operator cannot delete, export or shorten retention.
- Raw audit access is limited to designated Security/Audit read-only access. Platform API remains the existing fixed projection; export is deferred.

Security/IAM, Security/Audit and Privacy/Legal must approve retention period, archive/backup/deletion controls, read audience and denial telemetry before production use.

## 6. DB reality

DB REALITY = UNVERIFIED. Only connectionStatus was run with the BE .env credential. It reported Atlas host kimthang.mh3rrz2.mongodb.net and atlasAdmin/readOnly=false. The process config says development, which does not prove staging or production. No collection, validator, index, assignment, audit or migration history was read. No DB mutation was performed.

The [read-only DB verification runbook](../platform-operator-v1-db-verification-runbook.md) specifies role proof, actual collection options/indexes, redacted aggregate counts, duplicate/malformed checks, migration evidence and pass/fail criteria. Use a separate read-only credential; do not reuse the atlasAdmin credential.

The source migration creates the assignment collection/indexes only. It does not seed or mutate assignment documents and does not establish deployed state. Do not edit it. Any later DB change must be additive and include reviewed dry-run, rollout and rollback.

## 7. Child-task readiness

| Task | Readiness | Scope |
|---|---|---|
| DATN-295 | EXTERNAL APPROVAL REQUIRED | Runbook evidence and Security/IAM/Audit approvals before implementing the controlled bootstrap/idempotency persistence. |
| DATN-296 | READY | Preserve PLAT-ORG-01; no new admin route. Bootstrap tooling is owned by DATN-295. |
| DATN-297 | READY | Preserve PLAT-HEALTH-01; no new platform operations. |
| DATN-298 | READY | No administration UI in V1; deferred actions stay hidden. |
| DATN-299 | READY | No operations UI or Configuration controls. |
| DATN-300 | READY | Exact oracle: A-04 behavior, auth/errors, visibility/secret boundary, audit rollback, plus bootstrap replay/CAS/last-operator cases once tool exists. |

READY means implementation/test scope is deterministic, not that the issue is Done or code has shipped. Security/IAM, Audit and DB approvals gate DATN-295 bootstrap/ledger work and the conditional DATN-300 bootstrap tests; they do not widen the unchanged A-04 scope of DATN-296–299. Do not transition child Jira statuses in this decision record.

## 8. Remaining external approvals

| Exact approval | Proposed answer | Evidence | Owner | Affected tasks | Effect |
|---|---|---|---|---|---|
| Name issuer and separate executor; approve identity/MFA proof, two-person flow, exact three codes, no self/operator grant, legacy guard, last-operator and all-lost recovery | Approve PO-AUTH-01 in §4 and attach named roles/people and the controlled change workflow | Signed runbook and identity-verification process | Security/IAM | 295, 300 | Enables internal bootstrap tooling only; no public endpoint |
| Approve legacy assignment conflict/regrant behavior and operation-ID ledger | Reject rows without controlled provenance; reactivate only exact matching rows | Signed lifecycle decision; additive migration/rollback after DB report | Security/IAM + DB | 295, 300 | Enables safe persistence design |
| Approve 365-day retention, WORM/archive/backup/deletion, raw-read audience and denial telemetry or supply exact replacement | Approve §5 or return exact values/controls | Signed retention/enforcement policy and storage evidence | Security/IAM + Security/Audit + Privacy/Legal | 295, 300 | Enables bootstrap audit hardening/retention implementation; preserves existing A-04 behavior |
| Provide staging/prod read-only inspection for continuum_iam and continuum_audit | Grant read only, no atlasAdmin/write/DDL | Redacted report with environment, roles, indexes, validators, aggregate counts, migration evidence and hash | IAM DB owner / Data Platform | 295, 300 | Closes DB evidence gate; does not authorize migration |

There is no remaining operation-owner disposition or active-scope DEC-ACCESS-10 decision. The 37 candidates are deferred; future activation needs a new decision.

## 9. Jira synchronization rules

Synchronize DATN-293–301 descriptions/comments/acceptance/readiness without changing workflow statuses or issue links. Per KeyT's explicit choice, preserve the existing `DATN-301 blocks` links to DATN-295–300 and the DATN-294 → DATN-301 contract prerequisite as historical traceability. DATN-296–300 are READY because their scope is deterministic; DATN-301 is already Done, so retained links do not represent an unresolved policy decision. DATN-295 remains subject to external Security/IAM, Audit and deployed DB evidence. Jira DATN-301 being Done is not evidence of Security/IAM or Audit approval. The canonical contract and this decision record supersede old 40-code bundle and “37 awaiting disposition” wording.
