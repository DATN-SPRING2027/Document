# C-07 Team Membership API contract

**Revision:** 0.1-draft
**Status:** POST/DELETE-only scope is approved for DATN-92. Routes below reflect the current proposal; response details, transport/error semantics, and shared-contract compatibility remain subject to API/IAM/Security review.
**Machine-readable companion:** [draft OpenAPI](c-07-team-membership.openapi.json).

**Resource IDs:** the C-07 OpenAPI reuses one opaque `ResourceId` schema (`type: string`, `minLength: 1`) for Team, Membership, User, Organization, and Project identifiers, matching the BE OpenAPI convention. It intentionally does not constrain IDs to UUID/ObjectId syntax. Correlation `requestId` is not a resource identifier.

**Current source comparison:** [BE `iam-v1.openapi.json` at inspected main](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/docs/openapi/iam-v1.openapi.json) already contains POST, DELETE and a shared-draft GET for Team Membership. POST uses a strict `userId` request and `201`; DELETE by `membershipId` uses `204`; the current response includes `organizationId` and `projectId`. This C-07 companion preserves the POST/DELETE shapes and response fields, adds no GET, and proposes `Location`, no-store, CSRF, and conditional idempotency details for owner review.

## 1. Operations in scope

| Method and route | Purpose | Approved / proposed behavior |
|---|---|---|
| `POST /api/v1/iam/teams/{teamId}/memberships` | Create an admission for an eligible User in the Team's Project. | POST scope approved. Proposed strict JSON body `{ "userId": "..." }`; do not accept organizationId/projectId/teamId in body. New admission returns `201`; explicit rejoin also recommended `201` and `Location` because it creates a new ID. |
| `DELETE /api/v1/iam/teams/{teamId}/memberships/{membershipId}` | Remove one scoped admission. | DELETE scope approved. Recommended `204` for successful or repeated removal, subject to exact scoped-resource and authorization checks. |

There is **no GET/list operation in DATN-92**. The Backend repo has an older shared OpenAPI draft containing `listTeamMemberships`; its presence does not expand this scope. The responsible API contract owner must either exclude it here and preserve its independent disposition, or propose a separately reviewed amendment. Do not delete unrelated functionality or silently publish GET through this work.

## 2. Proposed request and response details

### POST add

- Authentication and Organization context come from the trusted session/context contract, not client-supplied parent identifiers.
- CSRF protection is required for cookie-authenticated mutation requests, consistent with the shared IAM/Gateway boundary.
- Require `Idempotency-Key` only if R0 confirms the C-04 TQ-09 contract or an authorized replacement approves it. Recommended syntax: 1–128 ASCII characters matching `[A-Za-z0-9._:-]+`.
- Validate the body as an allowlisted object containing only a valid `userId`; reject unknown fields.
- Recommended success: `201 Created`, JSON admission representation with only safe identifiers and `joinedAt`, and `Location` for the newly created Membership. Explicit rejoin returns the new ID and timestamp.
- Active duplicate: `409` with stable shared error code; no new row/event.
- Ineligible target: recommended `422` only after the actor has passed authorization and Team scope checks; do not leak eligibility to unauthorized callers.

### DELETE remove

- The path `teamId` and `membershipId` are resolved and scoped under the exact Team/Project/Organization.
- Require CSRF and, conditionally on TQ-09, `Idempotency-Key`.
- Recommended success and repeat removal: `204 No Content`; a repeat is a no-op with no duplicate business audit event unless Audit/Security approves otherwise.
- Do not accept a User identifier as a substitute for `membershipId`; this keeps deletion bound to the exact admission identity, including historical rejoin records.

## 3. Proposed transport, privacy, and error contract

All values in this table except POST/DELETE-only scope and the approved lifecycle outcomes are recommendations pending API/IAM/Security and Gateway review.

| Condition | Recommended result | Privacy/ordering rule |
|---|---|---|
| Missing/invalid authentication | `401 Unauthorized` | Authenticate before data-dependent work. |
| Authenticated request without the required trusted Organization context | `403 Forbidden`, existing code `ORGANIZATION_CONTEXT_REQUIRED` | Do not silently remap this established IAM 403 to 401. |
| CSRF failure for cookie-authenticated mutation | `403 Forbidden`, existing code `AUTH_CSRF_INVALID` | Require `X-CSRF-Token` to match `__Host-csrf`; reject before mutation/target lookup. A trusted bearer request follows the existing bearer/CSRF policy. |
| Malformed or unrecognized path resource ID | `404 NotFound` | Treat malformed path resource IDs like unavailable resources; do not disclose storage format/existence. |
| Malformed body, unknown field, missing `userId`, or invalid user ID | `422 ValidationFailed` | Reject unknown body fields. Do not perform writes. |
| Team missing or outside trusted Organization/Project scope | `404` indistinguishable response | Hide cross-scope Team existence. |
| Team visible, actor lacks explicit action grant | `403` | Check before disclosing target eligibility or duplicate membership state. |
| Missing/invalid required idempotency key, if TQ-09 applies | `422` | After actor and scoped Team authorization, before target state inspection. |
| Active duplicate admission / idempotency-key fingerprint mismatch | `409` | Stable codes; no second domain write or audit event. |
| Target User or parent eligibility is invalid | recommended `422` after actor authorization | Do not reveal to unauthorized actor; fail closed. |
| Stale precondition, if one is added by shared IAM contract | `412` | Do not add a new precondition absent the owning contract. |
| Contention/exhausted retry or dependency unavailable | `503` and `Retry-After` only if the shared contract defines it | A retry revalidates all current authorization and generation evidence. |
| Required persistence/audit dependency unavailable or transaction cannot complete | `503 ServiceUnavailable` | No success acknowledgment; abort the transaction. |
| Unexpected internal error | `500` shared `ErrorResponse` | Do not return raw Mongo/service details. |

Recommended precedence: authentication → trusted Organization context → cookie CSRF → malformed path/body validation → scoped Team visibility (`404`) → actor action permission (`403`) → required command headers/key syntax → replay/key conflict → target eligibility/active-pair state → transactional fence/write/audit. This order avoids target-state disclosure and matches existing IAM response categories (`Unauthorized`, `Forbidden`, `NotFound`, `Conflict`, `ValidationFailed`, `TooManyRequests`, `ServiceUnavailable`). API owner must confirm shared `ErrorResponse` codes and Gateway middleware before Gate A.

Cookie-authenticated POST/DELETE should require the existing `X-CSRF-Token` header matching the readable `__Host-csrf` cookie; the Gateway already forwards CSRF values on covered IAM calls, but Membership route coverage must be verified. Responses for both operations should use the shared error envelope and set `Cache-Control: no-store`. Gateway/BFF must forward trusted auth/context, CSRF, correlation/request ID, and (if TQ-09 applies) idempotency headers without trusting client-provided Organization/Project scope. No new shared error-code family is approved by this draft.

## 4. C-04 idempotency dependency

TQ-09 is **conditional**, not unconditionally approved. R0 must verify the authority and current effect of C-04 §10.1. If valid, reuse its exact contract rather than re-approving or changing it. If not valid, the API/IAM owner must approve the following replacement as one bounded choice before implementation:

- Key scope: `(actorUserId, organizationId, keyHash)`.
- Fingerprint: HTTP method + normalized route + canonical validated request body; reject same key/different fingerprint with `409`.
- Expiry/CAS: application-level 24-hour expiry with compare-and-set terminal claim; do not rely on a TTL index as the correctness mechanism.
- Replay: return the durable original result only after current actor/team authorization is revalidated; revoked authority does not replay a protected result.
- Atomicity: command result, Membership mutation, and required audit event commit in the same transaction; exact replay causes no second effect/event.
- Concurrency/uncertain commit: use one canonical durable operation record, retry with fresh reads, and prove committed/aborted/unknown outcomes do not duplicate effects.

These are candidate semantics from the C-04 proposal record, not a new approval. See R0/TQ-09 in the [Decision Register](DATN-92-Decision-Register.md).

## 5. Error contract acceptance tests

The API contract is not accepted until the owner approves exact statuses/codes and the following precedence tests pass: unauthenticated+malformed; CSRF+hidden Team; hidden Team+stale key; visible Team+missing action grant+missing key; authorized actor+active duplicate; invalid target+unauthorized actor; repeat DELETE; cross-Project Membership ID; rejoin response ID/Location; shared Gateway forwarding and `no-store`. See [Security/Test Plan](DATN-92-Security-Test-Review-Plan.md).
