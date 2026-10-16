# DATN-92 — Database and parent-writer design proposal

**Revision:** 0.1-draft
**Status:** Proposed for DB/domain owner review; no schema, index, migration, or parent-writer change is approved by this document.
**Source baseline:** DATN-BE `3b839198cfcbc40d6b11e1167ae8c68c54afea99` (read-only inventory).

## 1. Approved goal and current implementation gap

KeyT approved the TQ-06 direction: admission generation plus transaction fencing so restoration of a parent membership cannot silently restore prior Team access. Explicit removal followed by rejoin must create a new Membership ID and `joinedAt` (F-01 correction).

The inspected BE `origin/main` Team Membership schema contains only `organizationId`, `projectId`, `teamId`, `userId`, and `joinedAt`. The declared persistence index is unconditional unique `(teamId,userId)`. No Team Membership production writer, status, removal timestamp, or generation snapshot was found in the inspected source. Therefore the current schema/index cannot support the approved retained-history/new-ID lifecycle as proposed. The deployment's actual collection/index inventory is unknown; repository declarations are not proof of deployed state.

## 2. Recommended logical model — awaiting DB/domain approval

**F-07 correction:** the earlier partial unique index proposal is unsafe for the approved generation behavior. A stale-generation admission can remain `status=ACTIVE` while being ineffective. Its pair still occupies the partial unique index, so a fresh authorized POST after parent reactivation cannot create the required new Membership ID. This is a contract-design conflict, not a verified production defect; no MongoDB 7 reproduction was possible in this environment.

Recommend separating the stable pair-uniqueness key from per-admission history. This is a logical design only; collection names and fields below are not approved:

| Logical record | Candidate contents | Behavior / status |
|---|---|---|
| Current-membership slot, unique by `{teamId,userId}` | Exact Organization/Project scope, current admission ID (nullable), and a CAS/version value. | One stable slot per pair; never delete/reinsert it to release and reuse a unique pair key. Proposed; DB owner approval required. |
| Admission history record | New immutable admission ID, exact parent/subject IDs, `joinedAt`, and User/Organization/Project generation snapshots. | Every explicit rejoin or fresh re-admission after a stale snapshot receives a new ID/time. Records are retained; exact removal representation is pending DB/Audit approval. |
| Removal/lifecycle evidence | The approved durable representation for removal and audit correlation. | Must not mutate/reuse an old admission identity. Exact event/field mapping and retention are pending Audit/DB approval. |

Effective membership requires the slot to point to that admission, exact parent IDs, current `ACTIVE` User/Organization Membership/Project Membership, and equality between each stored admission snapshot and current generation. Missing, stale, or mismatched proof denies; never backfill it in a way that restores access. Parent restoration only advances parent generation and does not rewrite the slot or admission snapshot. A fresh authorized POST may CAS the slot from its stale admission pointer to a newly inserted admission ID; the stale admission remains ineffective and retained as history.

### Slot uniqueness and conditional replacement

1. Enforce a unique stable slot key `{teamId: 1, userId: 1}`. The slot's key never changes and is not released/reused during removal or rejoin.
2. Store each admission under its distinct Membership ID; index that identity uniquely. Add only owner-approved non-unique history lookup indexes.
3. For a fresh add, create a slot if absent (duplicate-key loser rereads); otherwise CAS the expected slot version/current admission pointer. Create the new admission and update the slot in the same transaction. A current effective admission remains a duplicate (`409`); a stale pointer may be replaced only by a freshly authorized POST under the approved stale-generation policy.
4. On removal, CAS the slot only if it still points to the path Membership ID, and record the approved removal/history evidence in the same transaction. A racing rejoin cannot be cleared by a stale DELETE.
5. Operation-key uniqueness/expiry indexes only follow the effective TQ-09 contract; TTL must not be the correctness mechanism.

This design avoids relying on releasing and reusing a partial unique-index key in one transaction. Its MongoDB 7 replica-set behavior, transaction participants, write-conflict handling, audit topology, concurrency and recovery still require DB owner review and runtime evidence. The current unconditional unique pair index must not be dropped until DB owner verifies deployed index definitions, duplicate slots/pairs, application compatibility, and migration cutover. Do not edit an immutable committed migration.

## 3. Generation and transaction-fence proposal

### Generation sources

Use explicit, monotonic `eligibilityGeneration` values on User, Organization Membership, and Project Membership. Keep that business epoch separate from the concurrency fence: the recommended fence is the repository's explicit same-document Mongoose `__v` increment used by `ProjectAccessRepository.fenceAuthorizationDocument`. The existing helper is evidence of an established pattern, not evidence that every parent writer currently participates. Do not treat `__v`, Organization Membership `version`, or `mutationFence` as an eligibility generation by name alone.

Increment generation on every transition or authority change that can invalidate or restore effective membership. At minimum include User suspend/reactivate, Organization Membership suspend/remove/re-admit, and Project Membership ACTIVE/INACTIVE transitions. Never reset/decrement. Store the resulting values on each new Team admission. Parent restoration only updates the parent generation; it never rewrites Team snapshots.

Role, RoleAssignment, Project status, and Team status/parent facts that affect actor authority or Team scope must be read/fenced with the mutation too. Reuse the explicit `__v` CAS fence for these authorization facts only after the owning domain proves every writer advances it; do not add a second generation field where no admission-snapshot semantics require one.

### Fence and retry protocol

Within one Mongo session/transaction, the command should:

1. Read trusted actor context and resolve exact Team → Project → Organization.
2. Read actor and target Users, Organization Memberships, Project Memberships, Project RoleAssignment/Role, and current generation/version facts.
3. Require current ACTIVE parents, exact scoped TEAM_LEADER and action permission, and expected admission snapshots.
4. Conditionally update/CAS each relevant source document using its observed `__v` and current status, with explicit `$inc: { __v: 1 }` in the same session. Check the admission's expected `eligibilityGeneration` separately. Parent writers must update the same fenced source record in the same transaction when changing eligibility/authority and increment the relevant generation on eligibility transitions. If a source cannot use `__v`, its owner must approve a dedicated same-document fence with the same conflict semantics; no read-only/status-only fallback is allowed.
5. CAS the stable Team/User slot, create a distinct admission history record, record a durable command result if TQ-09 applies, and write the required audit event in the same transaction.
6. Commit all records together. On conflict, abort and retry from step 1 with fresh authorization evidence. On audit/result failure, abort. On unresolved commit, use the approved idempotency operation record to determine outcome; never blind-repeat a domain write.

This causes a conditional write to each actor/target/parent/role/team source document for each mutation, so it may increase write contention; the established Project Access helper makes this the smallest supported protocol now visible in code. Mongo multi-document transaction semantics, write conflicts, transaction participants, and audit database membership in the same cluster/session must be validated against the supported MongoDB 7 replica-set deployment. A session existing in code is not proof that every parent writer participates. If any parent authority source cannot be fenced, the path remains fail-closed pending redesign; do not downgrade to status-only checks.

## 4. In-repository writer inventory — not external/deployment attestation

| Source/operation observed on BE main | Current behavior/evidence | Required owner proof/change |
|---|---|---|
| [User directory repository](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/infrastructure/mongodb/user-directory.repository.ts) `updateStatusAtomically` | Updates User status in transaction and advances Organization `membershipAdminRevision`; inspected implementation does not establish a monotonic User eligibility generation or increment the User's `__v` fence. | IAM/User owner lists all suspension/reactivation/admin/import/repair/external writers and adds generation + explicit same-document fence increment to each eligible transition. |
| [Organization Membership command repository](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/infrastructure/mongodb/organization-membership-command.repository.ts) | Organization Membership has `version` and `mutationFence`; command paths use conditional/versioned changes. | Organization owner attests every invite/accept/suspend/resume/remove/bootstrap/migration/import/repair writer and chooses whether an existing version is a valid eligibility generation. |
| [Organization provisioning repository](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/infrastructure/mongodb/organization-provisioning.repository.ts) | Creates initial ACTIVE Organization Membership during provisioning. | Provisioning owner must set initial generation/fence correctly; no default can reactivate old Team admission. |
| [Project Access repository](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/infrastructure/mongodb/project-access.repository.ts) | Adds/reactivates/removes Project Membership; current reactivation is same-row Project Membership behavior. Project Access fences selected authorization/eligibility documents. | Project owner enumerates every status writer and proves each changes generation/fence atomically. Do not copy same-row Project behavior into Team Membership. |
| [Project repository](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/infrastructure/mongodb/project.repository.ts) creator setup | Creates the creator's Project Membership. | Project owner includes create/repair/seed paths and generation initialization. |
| Project RoleAssignment and Role writers | Project Access assigns/revokes scoped TEAM_LEADER and fences selected authorization documents; role provisioning is code-driven. | IAM owner inventories assignment and role permission updates, grant seed/migration/admin paths, proving revocation serializes against Team mutation. |
| Team Membership | Schema/index exist, but no Membership command writer/provider/registered runtime write path was found in inspected source. | IAM/Team owner inventories any external/admin/import/repair writers before implementation. |
| [IAM persistence setup](https://github.com/DATN-SPRING2027/DATN-BE/blob/3b839198cfcbc40d6b11e1167ae8c68c54afea99/src/services/iam/infrastructure/persistence.ts), migration/init scripts, and deployed state | Repository has IAM schema/index initialization and Organization/Project membership migrations. Actual deployed Team index state was not inspected. | DB/Operations owner provides collection/index inventory, scripts, out-of-repository writer attestation, duplicate scan, backup and rollback/recovery evidence. |

This is complete only for the in-repository production paths located in the inspected BE commit. It is **not** a complete operational or external-writer inventory and cannot pass Gate B without named owner attestations.

## 5. Migration, rollout, rollback, and recovery

1. DB owner captures deployed schema/index and document counts, scans duplicate active pairs and legacy rows, and prepares a non-mutating dry run.
2. Approve field/index and legacy-row treatment with IAM, User/Organization/Project, Audit/Security owners. Legacy records without proof remain ineffective; do not silently generate proof or restore access.
3. Implement fields/indexes and migration in a separate DB branch/PR per repository workflow. Use idempotent forward migrations and preserve all historical migrations.
4. Deploy a compatibility stage only if the owner-approved rollout supports both old and new readers/writers safely. Do not turn on Team writes during schema rollout.
5. Validate MongoDB 7 replica-set transactions, concurrent add/remove/rejoin, parent status transitions, actor revocation, transient conflict retry, duplicate cleanup, and unknown commit outcome.
6. Define rollback as fail-closed disablement plus a reviewed forward-recovery or backup restore procedure. Once multiple admission IDs exist, a downgrade that reinstates the unconditional unique pair index may be impossible; do not promise a lossy automatic down migration.
7. Merge the required DB PR and any parent-writer PRs; only then base the dependent BE branch on the updated main.

## 6. DB/domain decision required

**DB owner + IAM/User + Organization Membership + Project Membership/Access + Security + Team product owner:** approve or amend the stable pair-slot plus retained admission-history model, exact generation fields/sources, full production writer inventory, fence/retry protocol, stale-pointer replacement rule, deployed-index reconciliation, legacy handling, and migration/rollback plan. Name each owner and provide MongoDB 7 replica-set race/transaction evidence. This review does not itself approve or implement schema changes. See [Decision Register](DATN-92-Decision-Register.md#3-consolidated-decision-table).
