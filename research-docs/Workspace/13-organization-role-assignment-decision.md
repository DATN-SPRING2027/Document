# Organization role assignment decision (ORG-08)

**Status:** User-approved contract; recorded 2026-10-20

**Decision owner:** Danh

**Scope:** Organization role assignment and the role projection on Organization
Membership reads. This decision does not approve Project role administration,
custom roles, role inheritance, or changes to Project access.

## Decision

1. **Role catalog.** The Organization assignment accepts only the existing catalog
   role codes `ADMIN` and `MEMBER`. Do not create custom roles, arbitrary role
   codes, or a new role code for this feature.
2. **Scope.** An Organization role applies only within the assigned Organization.
   Project role assignments are independent and are neither inherited from an
   Organization role nor managed through Organization APIs. The service checks the
   actor, target Membership, and requested resource against the same Organization.
3. **Actor and target.** An active Organization `ADMIN` with
   `organization.memberships.manage` may change the role of another active
   Membership in that Organization. A regular Member cannot assign roles. The
   role-change endpoint does not permit an actor to change their own role, even
   when another active Admin exists. Platform provisioning remains a separate
   operation under the Platform permissions already granted.
4. **Revocation and self-protection.** The role-change operation sets an active
   Membership to `ADMIN` or `MEMBER`; it does not clear the assignment. Removing
   Admin authority is performed by assigning `MEMBER`. Self-role changes are
   rejected by the backend; FE visibility is only a usability control.
5. **Last active Admin.** A role change, suspension, or removal must not leave an
   Organization with zero active Admins. The invariant is checked in the same
   transaction and through the shared Organization write/concurrency fence so
   concurrent changes cannot remove the last Admin. Promote a replacement before
   lowering or removing the current last Admin. Recovery of an Organization with
   no active Admin is a separately controlled process.
6. **Role read projection.** Membership list/detail responses include
   `roleCode: "ADMIN" | "MEMBER" | null` and `roleVersion: integer >= 0`. When no
   Organization role assignment exists, return `roleCode: null` and
   `roleVersion: 0`. These values describe only the Organization assignment, not
   Project roles or User-global roles.
7. **Mutation contract.** The operation is
   `POST /api/v1/iam/organizations/{organizationId}/memberships/{membershipId}/role`.
   It requires `expectedMembershipVersion`, `expectedRoleVersion`, `roleCode`, and
   a required `reason` string. `roleCode` is `ADMIN` or `MEMBER`; `reason` is
   trimmed and limited to 500 characters. `expectedMembershipVersion` is a
   positive safe integer; `expectedRoleVersion` is a non-negative safe integer,
   with `0` meaning no existing Organization assignment. Success returns
   `{operationId,membership,role:{roleCode,version}}`. The command requires
   authenticated authorization, matching Organization scope, a valid active
   target Membership, CSRF validation for cookie authentication, and an
   `Idempotency-Key`. Stale versions, forbidden scope, invalid input, and
   last-Admin conflicts follow the existing IAM structured error convention.
8. **Audit and atomicity.** A successful role change records the actor, target
   Membership, Organization scope, action, role before/after, bounded `reason`,
   timestamp, request/correlation ID, operation ID, and result. This is the only
   free-text reason exception in the Membership V1 audit allowlist. Do not include
   the raw request body, tokens, secrets, or unnecessary sensitive data. Persist
   the role change, idempotency result, and audit consistently in one transaction;
   audit or persistence failure must not return success, and a failed transaction
   must not leave a partial role change.

## Acceptance boundaries

- Reject self role changes, cross-Organization access, inactive targets, and role
  values outside the existing catalog.
- Keep Project assignments unchanged and do not allow Organization Admin status
  to imply access to private Project content.
- Protect the last active Admin under concurrent role and membership lifecycle
  mutations.
- Return Organization role code/version with Membership reads, including the
  `null`/`0` unassigned pair.
- Test authorization, version conflicts, idempotency/replay, concurrency,
  last-Admin protection, audit consistency, and persistence rollback.

## Evidence and implementation mapping

Danh approved the ORG-08 authorization and lifecycle semantics and the proposed
IAM endpoint/request/response contract in the project conversation on 2026-10-20.
The backend implementation and OpenAPI are tracked in
[DATN-BE PR #65](https://github.com/DATN-SPRING2027/DATN-BE/pull/65), with the
client in [DATN-FE PR #43](https://github.com/DATN-SPRING2027/DATN-FE/pull/43).
This record makes the previously approved decision discoverable from the
documentation source of truth; PR links are implementation references, not
substitutes for this decision.
