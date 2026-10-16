# PLATFORM_OPERATOR V1 — Read-only DB verification runbook

| Field | Value |
|---|---|
| Purpose | Verify deployed assignment/audit DB reality for DATN-295 |
| Status | Ready to execute when read-only credentials and environment owner are available |
| Owner | IAM DB owner / Data Platform |
| Affected tasks | DATN-295, DATN-300 |
| Safety | Read-only commands only; no collection/index/validator/data changes |

## 1. Current evidence

BE .env reports NODE_ENV=development. The only MongoDB probe was connectionStatus; its Atlas credential reported atlasAdmin and readOnly:false. No collection name, validator, index, assignment, audit row, or migration state was queried. This does not establish staging or production. Do not reuse that credential.

Request environment names/fingerprints and a short-lived credential with only read on continuum_iam and continuum_audit. Run separately against staging and production. If production access is unauthorized, record production UNVERIFIED; do not infer it from staging.

## 2. Evidence artifact

Save a redacted report with environment, cluster fingerprint (not URI/user/password), DB names, UTC timestamp, inspector identity, role proof, collection options/validator, exact index definitions, aggregate assignment counts, duplicate/malformed counts, audit indexes, release/migration evidence, tool version and SHA-256. Exclude subject IDs, emails, secrets, tokens, full assignment rows and raw audit metadata. Report PASS/FAIL per environment; missing collection and permission denial are evidence.

## 3. Read-only commands

Connect with approved read-only URI without printing it. Prove roles first:

~~~javascript
db.adminCommand({ connectionStatus: 1, showPrivileges: true })
~~~

Use `authenticatedUserRoles` and `authenticatedUserPrivileges` to prove effective access, not only the role name. PASS only when effective privileges are read on continuum_iam/continuum_audit (or narrower), with no atlasAdmin/readWrite/dbAdmin/root/write/DDL. Stop otherwise.

Inspect namespaces/options:

~~~javascript
const iam = db.getSiblingDB("continuum_iam");
const audit = db.getSiblingDB("continuum_audit");
iam.getCollectionInfos({ name: "platform_authority_assignments" });
audit.getCollectionInfos({ name: "audit_logs_iam" });
~~~

Record validator and validationLevel/action. Missing collection does not prove migration.

Read indexes only:

~~~javascript
iam.platform_authority_assignments.getIndexes();
audit.audit_logs_iam.getIndexes();
~~~

Compare actual assignment indexes with:
- subjectUserId_1_permission_1_scope_1, key {subjectUserId: 1, permission: 1, scope: 1}, unique true;
- subjectUserId_1_status_1_permission_1, key {subjectUserId: 1, status: 1, permission: 1}, unique false.

Record all actual options. Source migration declares no JSON-schema validator; live collection metadata proves deployed validator state.

Aggregate assignment counts without subject IDs:

~~~javascript
iam.platform_authority_assignments.aggregate([
  { $group: {
    _id: { permission: "$permission", scope: "$scope", status: "$status" },
    count: { $sum: 1 },
    expiredCount: { $sum: { $cond: [
      { $and: [
        { $ne: ["$expiresAt", null] },
        { $lte: ["$expiresAt", new Date()] }
      ]}, 1, 0
    ]}}
  }},
  { $sort: { "_id.permission": 1, "_id.scope": 1, "_id.status": 1 } }
]).toArray();
~~~

Count duplicate subject/permission/scope tuples without returning IDs:

~~~javascript
iam.platform_authority_assignments.aggregate([
  { $group: {
    _id: { subjectUserId: "$subjectUserId", permission: "$permission", scope: "$scope" },
    count: { $sum: 1 }
  }},
  { $match: { count: { $gt: 1 } } },
  { $count: "duplicateTupleCount" }
]).toArray();
~~~

Count malformed rows only:

~~~javascript
iam.platform_authority_assignments.aggregate([
  { $match: { $or: [
    { subjectUserId: { $not: { $type: "objectId" } } },
    { grantedBy: { $not: { $type: "objectId" } } },
    { permission: { $nin: [
      "organization.create", "platform.health.read", "platform.audit.read"
    ]}},
    { scope: { $ne: "PLATFORM" } },
    { status: { $nin: ["ACTIVE", "REVOKED"] } },
    { grantedAt: { $not: { $type: "date" } } },
    { expiresAt: { $exists: true, $not: { $type: "date" } } },
    { revokedAt: { $exists: true, $not: { $type: "date" } } }
  ]}},
  { $count: "malformedAssignmentCount" }
]).toArray();
~~~

Aggregate allowlisted audit actions/results/times only:

~~~javascript
audit.audit_logs_iam.aggregate([
  { $match: { action: { $in: [
    "organization.create", "platform.authority.granted", "platform.authority.revoked"
  ]}}},
  { $group: {
    _id: { action: "$action", result: "$metadata.result" },
    count: { $sum: 1 },
    oldest: { $min: "$occurredAt" },
    newest: { $max: "$occurredAt" }
  }},
  { $sort: { "_id.action": 1, "_id.result": 1 } }
]).toArray();
~~~

If an operation-id guard already exists, inspect its live collection/index. Do not create it during verification.

## 4. Migration and assignment conclusions

Source migration presence is not deployment evidence. The inspected repository does not record it in a persistent migration-history collection. Confirm execution from the environment release/change record and approved dry-run/checksum, then compare live options/indexes. The script creates collection/indexes only and does not seed assignments. Do not execute it for this report: its output may contain row identifiers in duplicate/invalid reports.

Report active/expired counts per exact A-04 permission without user IDs. A zero count is evidence only for that environment.

## 5. Pass/fail

PASS per environment only when read-only role proof passes; DB/collection identity is confirmed; actual indexes/options match or differences are recorded; validator state is captured; duplicate/malformed count is zero or reviewed remediation exists; assignment counts are redacted; exact migration/release evidence is linked; report is timestamped, hashed and DB-owner reviewed.

Mismatch, missing collection/evidence, duplicate/malformed row or conflicting index is FAIL / OWNER REVIEW. Do not repair it in this task. Keep DATN-295 gated pending an approved remediation/rollout/rollback plan.

## 6. Exact owner request

IAM DB owner/Data Platform: provide short-lived read-only access to staging and production continuum_iam and continuum_audit, identify cluster fingerprints, and return the signed/redacted report. Proposed role is read only, without atlasAdmin/write/DDL. This closes DB evidence for DATN-295/300; it does not authorize migration or production change.
