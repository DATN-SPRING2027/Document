# DATN-301 — Current V1 implementation gates

## Product decision

- [x] Preserve three existing A-04 capabilities unchanged.
- [x] Activate PLAT-ORG-02 Organization read.
- [x] Activate PLAT-USER-01 exact ACTIVE User lookup.
- [x] Activate PLAT-MEM-01 bounded Organization membership read.
- [x] Activate PLAT-MEM-03 SUSPEND only; keep invite, resume, remove deferred by DATN-291 A7/A8.
- [x] Keep the remaining 33 candidates deferred and Configuration OUT OF V1.
- [x] Record PO-D13 and supersede the earlier PO-D02/PO-D12 three-permission handoff.

## Implementation and verification

- [x] DATN-295 implementation: exact seven-code catalog, legacy/new bundle compatibility, provenance-matched V1 expansion, mandatory snapshot-hash CAS, transaction/idempotency/audit, and separate additive report-first index migration. The migration is not applied; the authority authorization provider remains fail-closed with 503 until external Security/IAM configures approved issuer/MFA evidence.
- [x] DATN-296 implementation: Organization list/detail, exact ACTIVE User lookup by POST body, scoped Membership list and SUSPEND-only Platform routes; preserve A-04 and tenant membership behavior.
- [x] DATN-297 implementation: preserve health and bounded audit response; add only membership-suspension action to the fixed allowlist.
- [x] DATN-298 implementation: dedicated Platform sign-in/session shell; Organization create/list/detail, exact User lookup and Membership list/suspend.
- [x] DATN-299 implementation: Health and bounded Audit views in the Platform shell; no deferred Operations/Configuration controls.
- [x] DATN-300 focused coverage: BE Platform E2E (27 tests), Mongo administration/authority integration, exact authorization, projection/resource scope, CAS/replay/last-admin/audit rollback; FE Console/API/BFF regression.
- [x] FE full check: lint, typecheck, 345 tests and production build passed. BE lint, typecheck, development DB smoke safety, unit suite (69 suites / 678 tests), focused Platform E2E (27 tests) and production build passed. Migration plan tests passed (3 tests).
- [ ] Full BE repository E2E remains blocked by local infrastructure: rerun had 11 suites pass, 2 skipped, 2 fail (76 tests pass, 4 skipped, 3 fail) because shared AppModule tests require Redis, unavailable on 127.0.0.1:6379. The isolated missing-JWT startup test now passes. Re-run with the repository's Redis service before merge.
- [x] Record as-built API, UI, audit and DB impact in the canonical contract, DATN-301 record, task folder and Jira DATN-295/298 descriptions; do not change Jira workflow status.
- [x] Final diff/security review: exact permission and resource checks, privileged transaction/audit atomicity, FE action gates, migration additive-only behavior, secret/content exposure, and changed-file scope reviewed; no additional findings.
- [ ] Local commits pending. Push/PR are not created automatically.

## External rollout gates

- [ ] Security/IAM approves and configures PO-AUTH-01 issuer/executor, trusted identity/MFA evidence, explicit V1 expansion, provenance and last-operator behavior. Until then the runtime deliberately refuses grants with 503 and the new four permissions are not provisioned.
- [ ] Audit/Privacy/Legal reviews minimal User projection, audit visibility and retention controls.
- [ ] DB owner supplies a redacted read-only report for each deployment environment.
- [ ] Do not activate invite/resume/remove until DATN-291 A7/A8 evidence and cutover are accepted.
- [x] Jira workflow statuses were not changed; do not infer rollout readiness from the existing Done statuses.
