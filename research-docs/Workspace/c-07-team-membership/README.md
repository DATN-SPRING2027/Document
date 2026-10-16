# DATN-92 / C-07 Team Membership — consolidated review package

**Package revision:** 0.1-draft
**Status:** Draft for contract and owner review; not an approved C-07 contract.
**Evidence baseline:** DATN-BE `origin/main` at `3b839198cfcbc40d6b11e1167ae8c68c54afea99`; Document `origin/main` at `6143f0dd2a6f4e396b8d21a0511fb7f9da2f8eef`.
**Jira:** [DATN-92](https://trankimthang0207.atlassian.net/browse/DATN-92), subtasks [DATN-266](https://trankimthang0207.atlassian.net/browse/DATN-266)–[DATN-271](https://trankimthang0207.atlassian.net/browse/DATN-271).

This directory is the single review surface for the C-07 decisions required by DATN-92. It consolidates the corrected approval evidence, the current source-code findings, and one recommended decision set. A Draft PR requests review; it does not approve any proposal or pass Gate A/B/C.

## Canonical documents

1. [C-07 Team Membership contract](C-07-Team-Membership-Contract.md) — scope, rules, invariants, and approved/proposed boundaries.
2. [C-07 API contract](C-07-API-Contract.md) and [draft OpenAPI](c-07-team-membership.openapi.json) — POST/DELETE only; GET is excluded from DATN-92.
3. [Decision Register and approval matrix](DATN-92-Decision-Register.md) — evidence, options, recommendation, owners, approval text, and gates for every unresolved decision.
4. [Database and parent-writer design](DATN-92-DB-Parent-Writer-Design.md) — proposed schema, writer inventory, fencing, migration, and separate DB workflow.
5. [Security, test, and review plan](DATN-92-Security-Test-Review-Plan.md) — threat cases, lifecycle regressions, findings workflow, and acceptance evidence.
6. [Implementation readiness and gates](DATN-92-Implementation-Readiness.md) — dependency sequence and explicit Gate A/B/C evidence.
7. [Approval evidence and F-01 history](DATN-92-Approval-Evidence-and-Findings.md) — attribution limits, preserved source evidence, correction trail, and finding verification.

## Decision status at package creation

- **Approved — verified within stated scope:** KeyT's 2026-10-16 11:17 ICT approval of TQ-05 direction, TQ-06 generation/fencing direction, the proposal's membership lifecycle, POST/DELETE-only TQ-07/08 scope, and TQ-10 same-transaction audit with rollback on audit failure.
- **Approved — conditional:** TQ-09 contract semantics only if R0 validates the referenced C-04 decision as authoritative and still effective. Runtime writes remain subject to Gate C.
- **Recommended — awaiting owner approval:** exact IAM permission identifiers/provisioning, DB fields and complete writer/fence protocol, API response/error details, audit event mapping/retention, and R0 authority evidence.
- **Review findings in this Document PR:** F-07 corrects the stale-`ACTIVE`/partial-unique-index conflict with a stable pair-slot plus retained-admission recommendation; F-08 adds explicit target eligibility cases A–H; F-09 aligns C-07 resource IDs with reusable non-empty opaque `ResourceId`. F-07 remains pending DB/domain approval and MongoDB 7 replica-set proof.
- **Not approved:** schema/index or migration; parent-writer changes; final API details beyond the bounded approved scope; audit retention; runtime write enablement.

## Historical source documents

The following source material is retained in the repository or in the approval evidence already attached to Jira. They are evidence, not parallel canonical decision registers:

- [C-04 decision-gap report](../09-team-management-foundation-decision-gap-report.md)
- [C-05 Team Foundation OpenAPI draft](../contracts/c-05-team-foundation-r4.openapi.json)
- [C-05 runtime-options proposal R4](../11-team-foundation-runtime-options-r4.md) — proposal only; not a substitute for DATN-92 owner decisions.
- Backend PR [#35 — Team Foundation schema/index](https://github.com/DATN-SPRING2027/DATN-BE/pull/35) and [#36 — Team runtime gate](https://github.com/DATN-SPRING2027/DATN-BE/pull/36) are implementation history, not C-07 membership approval.
- [Workspace audit schema](../../../database-design/10_AUDIT_AND_COMPLIANCE_SCHEMA.md) — contains examples; it does not set Team Membership retention.
- [Jira DATN-92 approval evidence](https://trankimthang0207.atlassian.net/browse/DATN-92), including KeyT's 11:17 statement, the proposal screenshot, and the F-01 correction comment.

## Approval request

Use the single consolidated request in [Decision Register §10](DATN-92-Decision-Register.md#10-one-consolidated-approval-request). Domain-owner replies should identify the decision IDs, approver role, timestamp, selected option/amendment, and exact package revision. Do not infer approval from Jira status or PR review state.
