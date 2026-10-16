# DATN-92 — Implementation Readiness and Gate Checklist

**Revision:** 0.1-draft
**Status:** Gate A and Gate B are not passed. This is a review checklist, not a release approval.
**Current implementation status:** no DATN-92 membership mutation code, schema, migration, or runtime write enablement was changed in this Document PR.

## 1. Current evidence snapshot

- DATN-BE main inspected read-only at `3b839198cfcbc40d6b11e1167ae8c68c54afea99`.
- Document branch starts at `origin/main` `6143f0dd2a6f4e396b8d21a0511fb7f9da2f8eef`.
- Team Foundation source is present in BE, but Team Membership mutation provider/write path is absent in inspected main. Team Foundation runtime flags remain fail-closed per the existing DATN-90 gate work; this is code evidence, not runtime acceptance.
- Current `team_memberships` schema has no status or generation snapshots; declared `(teamId,userId)` unique index conflicts with the approved new-ID rejoin if old rows are retained.
- API has an older Team Membership GET draft; DATN-92 scope excludes GET. No shared contract change is made by this package.
- A canonical Team audit event mapping and authoritative retention duration were not found. The `365` value in the audit schema is an example, not an approved Team retention policy.
- Required DB/domain, IAM/Security, API/Gateway, Audit/Security owner decisions remain open in the [Decision Register](DATN-92-Decision-Register.md).

## 2. Gate A — Contract Approved

Gate A passes only when every applicable item is evidenced and linked from DATN-92:

- [ ] R0 identifies authorized C-04 decision owner and validates the exact C-04 record/revision, or TQ-09 is replaced/deferred with an authorized C-07 decision.
- [ ] IAM/Security approves exact action permission IDs, Project-wide TEAM_LEADER scope, provision/revoke/assignment ownership, no-implicit-grant rule, and commit-time actor evidence.
- [ ] Team/DB/API owners approve retained admission identity/storage, active pair uniqueness, stale-generation re-admission, explicit new-ID/new-`joinedAt`, repeat removal, rejoin response semantics, and audit no-op behavior.
- [ ] User/Organization/Project/DB owners approve generation fields/source, User suspend/reactivate scope, all parent/role writers, transaction fences/retry behavior, legacy-row fail-closed treatment, migration and recovery boundary.
- [ ] API/IAM/Security/Gateway approves exact POST/DELETE DTOs, statuses, headers, error codes/precedence, shared ErrorResponse mapping, CSRF, concealment, cache behavior, and GET exclusion/disposition.
- [ ] Audit/Security approves canonical collection/schema, event/action mapping, allowlisted fields, dedupe/no-op/rejected-attempt policy, history-read scope, and exact retention/archival source or explicitly keeps the affected write deferred.
- [ ] Each decision has approver name/account, authority/delegation, timestamp/timezone, selected option/amendment, exact package/contract revision and Jira evidence.
- [ ] Contract, Decision Register, API/OpenAPI, approval record, and Jira cross-reference agree; no unresolved internal finding remains.

**Gate A evidence location:** Decision Register approvals and evidence links on [DATN-92](https://trankimthang0207.atlassian.net/browse/DATN-92), plus the versioned C-07 contract in this Document PR after decision updates. Do not mark the draft approved until owner evidence is present.

**Unlocks:** approved contract-level backend work, contingent on Gate B. It does not authorize schema work outside the DB process or runtime writes.

## 3. Gate B — Implementation Ready

- [ ] Separate DB branch/PR approves schema/index, migration, legacy-row handling, dry-run, deployed-index reconciliation, backup, rollback/forward-recovery.
- [ ] DB PR is reviewed/merged to main before the dependent Backend integration branch is based.
- [ ] Every User, Organization Membership, Project Membership, Project/RoleAssignment/Role and Team Membership writer is inventoried; owning domain owners attest in-repo and external/admin/seed/import/repair paths.
- [ ] Parent writer changes use the approved generation and transaction fence; retry re-reads current authority; race tests prove no stale admission or privilege restoration.
- [ ] MongoDB 7 replica-set support is verified for every transaction participant including canonical audit and idempotency records; late failure rolls back all required writes.
- [ ] Partial active-pair unique index and historical admission queries are implemented and tested; legacy rows without proof fail closed.
- [ ] Idempotency provider and durable operation result semantics are established if TQ-09 applies; expiry/CAS, replay authorization, contention and unknown commit are tested.
- [ ] Gateway/BFF/IAM routing and required context/CSRF/idempotency/correlation headers are contract-verified and integration-tested.
- [ ] Audit schema/event mapping and retention dependency are implemented as approved; no guessed duration.
- [ ] Membership writer remains inaccessible and fail-closed in every runtime config; direct routes, workers, flags, fallback paths and bootstrap paths are tested inaccessible.
- [ ] Independent review plan and regression suite are ready; finding log is linked.

**Gate B evidence location:** merged DB/parent-writer PRs and CI/integration reports linked to DATN-92 and the Backend PR.
**Unlocks:** implementation of DATN-266–271 behind an inaccessible fail-closed gate. It does not enable writes.

## 4. Gate C — Runtime Write Acceptance

Do not enable a runtime membership write flag before all are checked:

- [ ] Product/API contract is approved and linked; exact on-call, disable and rollback owners identified.
- [ ] Production-equivalent authorization, parent-generation and all-writer race tests pass.
- [ ] Replica-set transaction tests prove atomic Team + operation result + audit and rollback on injected audit failure.
- [ ] Idempotency expiry/CAS, replay after revocation, concurrency and committed/aborted/unknown commit recovery pass (if applicable).
- [ ] Actual collection/index state matches reviewed design; migration and recovery verified.
- [ ] Audit retention/archival, access controls, monitoring and alert ownership are approved and deployed.
- [ ] Runtime flag is default-off; direct route, worker, admin, seed and alternate entry points remain blocked until explicit enablement.
- [ ] Security, Operations, DB, IAM and product acceptance evidence is attached to Jira; test results and reviewer approvals are linked.
- [ ] Controlled enablement, post-deploy observation, disable procedure and rollback/recovery are accepted by named owners.

Gate C is independent of merging the backend PR and is not implied by Gate A/B.

## 5. Required execution order after approvals

1. Record owner decisions; update this one Decision Register and versioned C-07 contract; re-run documentation/OpenAPI/link validation.
2. Create the DB change through its separate workflow; review/fix/test/re-review; merge the DB PR.
3. Implement and merge approved parent-writer generation/fence dependencies through the owning domain workflow; verify all-writer inventory.
4. Rebase/create final Backend integration branch `feat/DATN-92-team-membership-be` from updated main after dependencies; implement DATN-266–271 behind fail-closed Gate C.
5. Per subtask and integration: **IMPLEMENT → TEST → REVIEW → FIND → FIX → REGRESSION TEST → RE-REVIEW**. Do not carry unresolved blocking P0/P1/P2 findings into final Backend PR.
6. Integrate all six subtasks in one Backend branch and one Backend PR; do not auto-merge.
7. Keep runtime writes disabled until Gate C evidence is accepted by responsible owners.

## 6. Current resumption blockers

**Gate A:** R0; exact IAM permission/provisioning; DB/domain generation and lifecycle detail; API/Gateway error contract; Audit/Security event and retention decision.
**Gate B:** separate DB design approval/PR/merge; parent-writer implementation and complete inventory/evidence.
**Gate C:** production-equivalent runtime/security/operations evidence and explicit enablement acceptance.

Documentation review and draft PR are safe now and do not wait on these gates.
