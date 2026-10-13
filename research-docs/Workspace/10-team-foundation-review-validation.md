# DATN-89 — checkpoint, acceptance and validation mapping

Revision **R1, 2026-10-12 (Asia/Saigon)**. Read with the
[C-04 evidence and decision-gap report](09-team-management-foundation-decision-gap-report.md).
E/B/TQ identifiers below refer to that report. This records documentation
coverage and scenarios for review, not executed Team runtime tests or product approval.

## 1. Jira source and progress

UI read 2026-10-12: DATN-89 To Do/Nguyen Hong Phuc, Medium, no due date;
DATN-248–253 To Do/Unassigned, empty descriptions, no comments displayed. Parent
Comments panel likewise has no approval comments. Its displayed dependency is
DATN-89 blocks DATN-90; no incoming blocker is displayed. DATN-90 To Do, blocked
by DATN-89, blocks DATN-91 FE and DATN-92 Team Membership BE, both To Do.
DATN-86 and children DATN-229–234 are Done; status/merge is not Team policy approval.

No Jira status, description, comment, assignment or dependency was changed here.
Requester changes statuses. The recorded status is a read snapshot, not proof
that a recommendation has been applied. Work progress and decision readiness
are tracked separately; Team TQ items do not prevent completing gap-report work.

| Checkpoint | Deliverable evidence | Remaining decision gate | Snapshot → recommendation |
|---|---|---|---|
| [DATN-248 — Define Team entity](https://trankimthang0207.atlassian.net/browse/DATN-248) | Report §3; storage vs API validation, identifiers, missing fields; E7/E8 | TQ-01/02/04/07/09 | To Do → In Review; documentation ready |
| [DATN-249 — Define Team Membership rules](https://trankimthang0207.atlassian.net/browse/DATN-249) | §2/4/6/8; Organization context, Project prerequisite, pair uniqueness, RoleAssignment separation, D4 boundary | TQ-03/05/06/08–10 | To Do → In Review; documentation ready |
| [DATN-250 — Define Team lifecycle](https://trankimthang0207.atlassian.net/browse/DATN-250) | §5/8/9; every operation needing state/actor/effect decision, no copied enum | TQ-02/06/08–10 | To Do → In Review; lifecycle gap table ready |
| [DATN-251 — Define Team and Project relationship](https://trankimthang0207.atlassian.net/browse/DATN-251) | §2/4/6/9; approved containment, scope consistency, Project removal mismatch | TQ-03–06 | To Do → In Review; relationship evidence ready |
| [DATN-252 — Define Team authorization rules](https://trankimthang0207.atlassian.net/browse/DATN-252) | §2/6; actor/evidence matrix, deny/ACL, no ADMIN/public-Project bypass; no Team action code selected | TQ-05/07/08/09 | To Do → In Review; boundary/gap matrix ready |
| [DATN-253 — Define Team API contract](https://trankimthang0207.atlassian.net/browse/DATN-253) | §7/8/10; seven exact draft operations, DTO/query/errors, concurrency/idempotency/audit gaps | TQ-01/02/05/07–10 | To Do → In Review; API inventory/gaps ready |

Recommend [DATN-89](https://trankimthang0207.atlassian.net/browse/DATN-89) To Do →
In Review when handing over this report. After human inspection of the document
work, Done can reflect its completion while TQ decisions stay separately open.
Neither recommendation clears DATN-90's approved-contract requirement.

## 2. Parent acceptance criteria and expected result

| Jira acceptance / result | Coverage and assessment |
|---|---|
| Team fields, lifecycle, Organization/Project relationships, actor rules, API and errors are explicit | Report §2–8 states approved boundaries, current fields and exact draft APIs; state/actor/error gaps have specific TQ decisions. **Gap-report coverage complete; full approved contract incomplete.** |
| No unsupported Team behavior presented as product decision | E1–E13 authority map, B1–B6 scoped approval, D1–D6 Organization-only limits, all Team API candidates PROPOSED and TQ items UNKNOWN; no invented Team roles/states/cascades |
| Unknown/conflicting requirements listed for human decision before dependent implementation | §9 differences, §10 ten concrete questions with authority domains and dependent scope; below maps downstream gates |
| Reviewed Team Foundation contract **or** precise decision-gap report | **Precise decision-gap report prepared for human review.** No claim of human-reviewed/approved Team implementation contract; human review remains pending |

## 3. Validation scenarios and evidence limits

The following are document review scenarios and future implementation checks.
“Baseline” means an approved constraint to preserve; “Decision” requires an
authority-selected observable result before runtime tests can assert it.
No BE/FE suite, live index check, API call, migration or Team integration test
was run by this documentation task.

| ID | Scenario | Constraint / expected decision coverage | Mapping |
|---|---|---|---|
| TV-01 | Four Organization states; role-only evidence; ACTIVE with no role | Baseline B2/B3: only ACTIVE establishes context; no RoleAssignment fallback; context alone never permits Team actions | 249/252; E4/E10 |
| TV-02 | Zero/one/multiple ACTIVE Organization memberships; forged selection | Baseline E4: none/no context, one auto-select, multiple explicit validated choice; Team API transport/errors remain TQ-07/08 | 249/252/253 |
| TV-03 | Inactive User, suspended/removed Organization member, stale token claims | Baseline active subject/context required; D4 deny at next check; not proof of implemented suspend or global cache/in-flight revocation | 249/252; TQ-06/09 |
| TV-04 | Team ID guessed across Organizations, wrong Project/Team pair | Baseline B1/B3: server validates actual parent chain, no response/mutation across scope; exact 403/404 TQ-08 | 251/252/253 |
| TV-05 | ADMIN/platform-only actor requests Team list/create/content | Baseline B4: no implicit Team rights; Project metadata/publicity exception grants no nested access; projection/grants TQ-05/07 | 252 |
| TV-06 | Project-scoped leader acts on child or sibling Team; fabricated Team assignment | Baseline explicit scope only; delegation/evidence representation TQ-05; role title/project.members.* is insufficient | 251/252 |
| TV-07 | Team member with forbidden confidential evidence; SME/SUCCESSOR attempts scope expansion | Baseline B3/B4: independent ACL/deny and scoped assignment; no inherited predecessor rights | 249/252; TQ-05 |
| TV-08 | Create Team with blank/whitespace/long name, invalid/lowercase code, null/long description or extra role/status field | Decision TQ-01/07/08: reject/normalize order and API allowlist vs schema must be approved; E8 bounds remain proposed | 248/253 |
| TV-09 | Same code in same Project vs different Project; name duplicates | E7 index declaration only; TQ-01/08/09 approved uniqueness/error/concurrent outcome; live index verification in DB scope | 248/251/253 |
| TV-10 | Team create in missing/mismatched/archived Project; creator rights | Baseline B1/B5 no implicit Team bootstrap; TQ-02/05/06 selects parent-state eligibility and creator membership/leadership | 248/250/251 |
| TV-11 | Add target with missing/INACTIVE/wrong Project membership or inactive Organization/User | Eligible parent required for effective Team access; exact add-time eligibility/state/invite TQ-03/05; no copied Organization invite policy | 249/252 |
| TV-12 | Duplicate add, rejoin after remove, concurrent add, one User in multiple Teams | Decision TQ-03/04/08/09 defines pair identity, cardinality, replay/conflict and reviewed rights; no unique-user global constraint inferred | 249/251/253 |
| TV-13 | Project member removal while Team link/responsibility remains | E11 currently INACTIVE removal without Team query; TQ-06 resolves future blocker/coordination/access effect before Team flows; no unapproved Project side effect | 249/251 |
| TV-14 | Organization suspend/remove/resume/rejoin with stored Team roles/links | D4 selected handover/retention/next-check denial/rights review; no automatic child rights restoration; storage reconciliation TQ-03/06 | 249/250/251 |
| TV-15 | Update code or Project parent; missing/null description; empty/same-value PATCH | Decision TQ-01/04/07/09; draft PATCH omits code/parent, but omission is not product approval of immutability | 248/250/251/253 |
| TV-16 | Archive, restore, delete/deactivate, repeated/illegal transitions | Decision TQ-02/06 must enumerate full state × command matrix and references/children/read/write effects; no Team ACTIVE/ARCHIVED copied | 250/251 |
| TV-17 | Team list/member paging boundaries, malformed page, search/filter/sort, out-of-range, hidden totals | E8 page 1/20/max100 is candidate; TQ-07/08 resolves exact queries/projection/order; authorized filtering before pagination | 252/253 |
| TV-18 | Missing/invalid auth, wrong scope, invisible/malformed/missing target, duplicate/state/internal error precedence | Decision TQ-08; exact per-operation status/code/details, concealment, safe requestId; no invented Team problem codes | 253 |
| TV-19 | Simultaneous updates; actor/target membership/role/parent revoked between authorize and write | Decision TQ-09 defines concurrency/preconditions/fence; no last-write-wins or Organization D5 transfer assumed | 252/253 |
| TV-20 | Same Idempotency-Key/body, different body, pending request, expired key, DELETE replay | Decision TQ-09 + TQ-03/08/10 defines fingerprint/replay/storage/auth/audit; Redis claim is not proof; E8 DELETE proposal not approved deletion policy | 249/253 |
| TV-21 | Team mutation success, audit write failure, rollback/retry, repeated audit and rejected attempt | Preserve B6 atomic IAM/audit invariant; TQ-10 exact event/collection/session/dedup; future replica-set commit/rollback proof required | 249/250/253 |
| TV-22 | History read, retained references, sensitive audit payload, async Team event delivery | Baseline no secrets/private body in audit; TQ-06/10 selects history/retention and any consumer; D6 Org email does not create Team outbox | 249/250/253 |

## 4. DATN-90 and downstream implementation gate

| Work | Required before implementation | Current result |
|---|---|---|
| [DATN-254](https://trankimthang0207.atlassian.net/browse/DATN-254) Team schema | Accepted TQ-01–06/09/10 persistence requirements; DB ownership/compatibility/migration/rollback workflow | Source inventory supplied; no approved schema delta or DB execution |
| [DATN-255](https://trankimthang0207.atlassian.net/browse/DATN-255) Create Team | Accepted fields, initial lifecycle, actor/target scope, bootstrap and API/audit/concurrency | Report alone cannot authorize create |
| [DATN-256](https://trankimthang0207.atlassian.net/browse/DATN-256) Update Team | Mutable fields/code/parent/lifecycle, exact grant/DTO/stale-write/audit | UNKNOWN choices remain separate |
| [DATN-257](https://trankimthang0207.atlassian.net/browse/DATN-257) List/detail | Accepted Team visibility/member projection, paging/filter/sort, ACL and errors | Project metadata read contract is not reusable approval |
| [DATN-258](https://trankimthang0207.atlassian.net/browse/DATN-258) Delete or deactivate | Explicit TQ-02/06/10 choice, reference/retention/recovery/access effects | Ticket title does not choose either option |
| [DATN-259](https://trankimthang0207.atlassian.net/browse/DATN-259) API tests | Accepted observable outcomes for TV rows; real index/transaction proof where required | Documentation scenarios only; no passing Team runtime claim |
| [DATN-91](https://trankimthang0207.atlassian.net/browse/DATN-91) FE / [DATN-92](https://trankimthang0207.atlassian.net/browse/DATN-92) Team Membership BE | Own ticket/contract/API decisions and merged DATN-90 dependency, separate BE/FE/DB workflows | Linked statuses To Do; no implementation or readiness approval here |
| Task/knowledge/handover consumers | Approved owning API/event/ACL and responsibility-transfer contract; named authorized domain owners | No unmerged Task contract, direct DB query or implicit cascade used |

## 5. Document verification and handoff boundary

Required checks: final diff/whitespace/scope, relative links and anchors, pinned
BE links/paths, all seven draft operations/DTOs/errors against E8, authority
labels and D1–D6 scope, B/TQ/TV references and complete six-checkpoint/three-AC
mapping. Final `code-review-and-quality` review follows these checks; any finding
requires requester-approved fixes before commit/push, per Document AGENTS.md.
Actual results, final commit/remote SHA and review outcome are recorded in the
handoff and workspace-local WORKING_CONTEXT.md outside Git.

DB/schema/index/migration/data impact: **none**. No deployment, PR, approval,
merge or team message. Once checks/review pass, workflow permits committing and
pushing only the verified Document task branch. Requester inspects before asking
for a PR into main. Human policy/contract approval remains a separate step.
