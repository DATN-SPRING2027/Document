# DATN-413 — Human Knowledge Gap and Follow-up Contract

## Document status

- Revision: **R0.5, 2026-10-18 (Asia/Saigon)**
- State: **Contract closure revision incorporating the conditional Project Lead disposition in Jira comment #10255. Product decisions include amendments; independent Security and API/Architecture confirmations and several exact policy values remain pending. R0.5 is not implementation-ready until those gates are resolved.**
- Jira: [DATN-413](https://trankimthang0207.atlassian.net/browse/DATN-413)
- Related subtasks: [DATN-414](https://trankimthang0207.atlassian.net/browse/DATN-414), [DATN-415](https://trankimthang0207.atlassian.net/browse/DATN-415)
- Evidence base: Document `origin/main` at merged PR #45 commit `95edc801a68da2d6a4c23efaaf83bbe7d3d42279`; task-linked Jira records; DATN-BE `origin/main` at `9e3227925d01532b6e26336a77b38895392112b5`; DATN-FE `origin/main` at `217a9da38ca8db5334aeab51f2dea854a02844b1`; and SAG `main` at `ab27c61e90fb24ea0e73ea935f68baee36ba9942`, checked 2026-10-18.
- Decision evidence: Jira comment #10255 records KeyT's conditional, role-labeled disposition. The closure instruction identifies KeyT as Project Lead. Product accepted P1/P2, D-04/D-05, D-10, and G-01–G-12 subject to a D-07 amendment. Security-labeled and API/Architecture-labeled decisions include additional requirements. The comment does not identify separate Security/API approvers or repeat the R0.4 SHA; this revision requests explicit confirmation against R0.5 where role separation applies.
- Approval evidence: **Conditional Product/Project Lead disposition exists; independent Security and API/Architecture approval against R0.5 is not yet established.** Do not infer approval from role labels, PR #45 merge, or the R0.4 recommendation.
- Scope gate: DATN-413 is the Phase 1 contract task. Persistence/API, UI, and trigger implementation are separately scoped by DATN-444, DATN-448, and DATN-451 and are blocked by this contract. This document does not create or change application schemas, grants, endpoints, or runtime behavior.

This is the versioned J-01 contract and evidence package. It separates accepted rules, bounded technical choices, existing code that is not yet a contract, and decisions that require Product/Security/API-owner authority. Jira `Done`, code presence, technical review, and this document do not constitute a role approval.

### Revision history

| Revision | Change |
|---|---|
| R0.1 | Clarify that DATN-63/64 and PR 28 are complete while broader SAG work may continue; keep SAG integration details open until its owner confirms the stable interface. |
| R0.2 | Add non-binding recommended defaults to make the Product/Security decision review concrete. No recommendation is selected policy. |
| R0.3 | Reconcile every J-01 criterion with Jira, current DATN-BE/FE source, and current SAG `main`; classify decisions, record the existing schema mismatch, and add an acceptance checklist with completion evidence and remaining approval blockers. |
| R0.4 | Refresh BE/FE source refs; verify that J-02/J-03/J-04 still own runtime work; record the exact PR/Jira review state and the corrected BE IAM E2E test on current `origin/main`. No Product/Security disposition is presumed. |
| R0.5 | Incorporate Jira #10255's conditional Product/Project Lead acceptance and amendments; define the exact remaining D-07, retention/deletion, reference create/read, and API/audit confirmation gates; correct PR #45's merged state. |

## Acceptance checklist (J-01)

| Jira criterion / completion evidence | Result | Evidence and limit |
|---|---|---|
| Gap fields, states, ownership, links, and actor/scope are explicit or recorded as decision blockers | **Met at contract level, subject to R0.5 role confirmation.** §9.3 records the Project Lead disposition and remaining decisions. | Exact resolution outcomes, retention rules, and reference create/read/error behavior remain explicit owner decisions. |
| Insufficient-evidence and required-knowledge follow-up can create a gap without inventing a score | **Partly met.** Jira #10255 conditionally accepts explicit user submission for both paths and the minimal-context rule; R0.5 records those decisions. | Confirm Product disposition against R0.5; Security must confirm retention and the reference behavior. No automatic overdue creation is in the accepted proposal. |
| Human resolution is explicit; advanced scoring/autonomous crawl is excluded | **Partly met.** Human-only `OPEN → IN_PROGRESS → RESOLVED` is accepted conditionally; advanced scoring/autonomous crawl remains excluded. | Product must specify the resolution outcome vocabulary and whether notes/evidence are required; Security must confirm resolver authority. |
| Task/evidence references use owning APIs and cannot widen access | **Met as an invariant; operation behavior is incomplete.** References never grant access and must be checked by their owning APIs. | Security/API must specify create/read results for missing, stale, inaccessible, and cross-scope references and confirm shared denial/audit conventions. |
| Required completion evidence: versioned contract/state matrix, source-to-gap mapping, authorization/test scenario matrix | **Met in this package.** See §§3–4, 6–8. | Scenarios are acceptance oracles, not evidence of runtime test execution. J-01 does not implement J-02/J-03/J-04. |
| Expected result: approved human-owned workflow contract | **Not met.** Jira #10255 provides a conditional Project Lead disposition against the R0.4 discussion, not complete approval of R0.5. | Security/API authority and the specific amendments in §9.3 must be confirmed before treating the workflow as approved or DATN-413 as Done. |

## 1. Goal and boundary

Define a human-owned DATN workflow to record, assign, track, and resolve knowledge gaps. The gap is a Continuum follow-up record; it does not replace SAG's quality signals, scored-gap model, bounded research task, or ingestion pipeline.

In scope:

- Follow-up initiated from an assistant insufficient-evidence response.
- Follow-up for missing or overdue required knowledge.
- Project/Team ownership and authorization boundaries.
- Required gap information, lifecycle, optional references, and human resolution.
- Create/list/detail/update/resolve behavior and security scenarios.

Out of scope for this MVP contract:

- A DATN duplicate of SAG coverage, freshness, contradiction, uncertainty, demand, or priority scoring.
- Autonomous question generation, research planning, crawl/fetch, or ingestion.
- Advanced freshness/conflict scoring, employee scoring, automatic knowledge verification, or automatic gap resolution.
- Treating Jira issues as Continuum task records. The accepted MVP identifies the Continuum Task API as the canonical task source and excludes Jira task sync.

## 2. Source and authority ledger

| Source | Evidence used | Authority / limit |
|---|---|---|
| DATN-413, read 2026-10-18 | Required gap fields, source actions, CRUD/resolution scenarios, authorization scope, and acceptance criteria | Task scope. It assigns Product and Security as decision-owner domains; it does not record their approval. |
| [MVP Scope v1.3](../01_MVP_SCOPE.md), accepted baseline, last updated 2026-10-01 | One Project with multiple Teams; required-knowledge reminders; insufficient-evidence response with a way to report a gap; handover follow-up; advanced scoring and AI interviewing boundaries | Accepted product baseline for the cited scope. |
| [Actors, Roles and Permissions](../02_ACTORS_ROLES_AND_PERMISSIONS.md), accepted baseline | Role vocabulary, active membership/scope/ACL, explicit Team Leader scope, Member gap reporting, deny precedence, and no default confidential-content access for Organization Admin or Platform Operator | Accepted high-level authorization boundary; it does not specify Knowledge Gap action grants. |
| [Daily Workflow](../03_DAILY_WORKFLOW_AND_JIRA_SYNC.md), § assistant experience | Insufficient evidence is stated explicitly and the assistant offers a Knowledge Gap rather than guessing | Supports a user-facing follow-up action; does not settle auto-create versus explicit submit. |
| [Team decision-gap report R2](09-team-management-foundation-decision-gap-report.md) | Team actions and exact Team Leader permission provisioning remain conditional or deferred | Decision-gap evidence, not authority to infer a Knowledge Gap permission matrix. |
| [DATN-63](https://trankimthang0207.atlassian.net/browse/DATN-63), Done | SAG quality signals, reproducible scoring, reason/evidence traceability, and scored-gap questions | Existing SAG capability boundary; Jira status is not runtime verification. |
| [DATN-64](https://trankimthang0207.atlassian.net/browse/DATN-64), Done | SAG detector-to-research pipeline, approved sources/policy, budgets, duplicate guards, stop conditions, and normal ingestion | Existing bounded research scope. Its Jira comment points to [PR 28](https://github.com/DATN-SPRING2027/sag-laya-integration/pull/28), which GitHub reports closed and merged. Relevant current-main gap/research models, router registration, and Project-scoped principal code were inspected; this is not a full runtime audit or proof that all SAG work is finished. |
| [DATN-BE current source](https://github.com/DATN-SPRING2027/DATN-BE/tree/9e32279) | Lifecycle MongoDB schema and persistence metadata contain a `knowledge_gaps` collection | Current code evidence, not a J-01 approval. Fetched `origin/main` search found only the schema and persistence/index registration, with no gap repository, application service, controller/API, or executable behavior/tests. The scaffold is reconciled in §2.1 and §5. |
| [SAG current source](https://github.com/DATN-SPRING2027/sag-laya-integration/tree/ab27c61e90fb24ea0e73ea935f68baee36ba9942) | Current SAG quality models, gap/question tables, bounded research service, all 16 registered v1 router modules, and Project-scoped principal assertion | Current code evidence, not a DATN cross-service contract. The public `main` router registry and each registered v1 router were inspected; none defines a quality/gap CRUD or source-reference route. Scored gaps are internal SAG persistence and the Phase 10 research planner consumes them internally. |

The workspace governance configuration currently has no selected source baseline (`baseline.active: null`). This package makes no claim of exhaustive runtime behavior; its implementation survey is limited to the explicit current repository heads cited above.

Jira currently marks DATN-63 and DATN-64 Done, and PR 28 is merged. SAG `main` is at `ab27c61` (a later Project-scoped Continuum SSO change); the public repository showed no open PRs at inspection time. This cannot rule out local or unpushed work reported by the requester. J-01 does not require SAG CRUD/API integration, so that uncertainty does not block its contract boundary. Any later SAG signal/API dependency remains gated on an owner-confirmed interface.

### 2.1. Current implementation and integration boundary

| Area | Verified current state | Consequence for DATN-413 |
|---|---|---|
| DATN backend | `DATN-BE` is a NestJS modular monolith. On fetched `origin/main` (`9e322792`), `knowledge_gaps` is declared in `src/services/lifecycle/infrastructure/mongodb/mongodb.schemas.ts` and registered in lifecycle persistence with an index. A source-wide `origin/main` search found no gap repository, application service, controller/API, or tests using the collection. | Treat the schema as a persistence scaffold with no implemented gap workflow, not as the approved J-01 contract. Do not change it in this contract task; DATN-444 owns storage/API. |
| Existing DATN gap shape | The scaffold has `organizationId`, `projectId`, optional `teamId`, `responsibilityCode`, `title`, `description`, `severity` (`LOW`/`MEDIUM`/`HIGH`/`CRITICAL`), `status` (`OPEN`/`IN_PROGRESS`/`RESOLVED`/`IGNORED`), `assignedToUserId`, `resolvedByKnowledgeObjectId`, and `resolvedAt`. | It has no explicit source/reason, reporter, or resolver-user field. `severity` and `IGNORED` are not adopted automatically; see §5 and D-04–D-07. |
| DATN frontend | On fetched `origin/main` (`217a9da3`), source search found no Knowledge Gap route/component or API client. The local checkout was 21 commits behind that ref and was not modified. | UI belongs to DATN-448; no frontend work is required by J-01's contract acceptance evidence. |
| SAG quality/gap data | Current SAG `main` migration `0004` stores versioned quality assessments and internal scored `knowledge_gaps` linked to assessments and evidence-backed `knowledge_gap_questions`. Migration `0005` adds `research_tasks` with a foreign key to SAG's `knowledge_gaps` table; the Phase 10 research planner consumes eligible scored gaps internally. | A SAG `gap_id`, score, reason codes, question, or research-task state cannot be used as the DATN human gap ID/state or assumed to be a public reference. |
| SAG HTTP API | Current `sag_api/api/v1/__init__.py` registers 16 v1 router modules; each module was inspected for gap, quality, or research-task HTTP routes. None exposes a knowledge-quality/gap CRUD or DATN source-reference route. Existing project-scoped principal assertions govern evidence access. | No stable SAG gap endpoint or DATN correlation contract was found. Do not add SAG references or call a guessed endpoint in J-01/J-02. Confirm any later source-link contract with the SAG/API owner. |
| SAG work in progress | Public `main` had no open PR at inspection time; its latest commit was `ab27c61` on 2026-10-17. | The requester's report may refer to local/unpushed work. It does not block J-01 because the issue needs only a non-duplicative boundary; it blocks a future integration assumption needing an unverified interface. |

## 3. Reuse and boundary matrix

| Capability / signal | Existing owner and evidence | DATN Knowledge Gap responsibility | Boundary |
|---|---|---|---|
| Coverage, freshness, contradiction, uncertainty, query demand, and priority metrics | SAG / DATN-63 | Store a human follow-up reference and an allowed reason/source reference when provided by the owning integration | Do not calculate or persist a second score, threshold, or priority model. |
| Evidence-grounded gap question | SAG / DATN-63 internal question generation | Let the user review and submit a human follow-up when the assistant reports insufficient authorized evidence | Do not expose or copy SAG's internal scored-gap question as a DATN record or let an LLM invent the reason/evidence. |
| Bounded research and ingestion | SAG / DATN-64 | Remain outside the CRUD/resolution lifecycle; consume no permission through a link | No autonomous research, crawl, fetch, retry, or ingestion behavior in this task. |
| Required knowledge missing or overdue | Continuum product workflow / accepted MVP scope | Provide a visible follow-up action tied to the configured requirement; a human-submitted action can create a DATN gap | Auto-creation, overdue threshold, and source authority still require Product; no score is required. |
| Assistant has insufficient authorized evidence | Assistant / accepted MVP scope and daily workflow | State insufficient evidence and offer a user-controlled report/follow-up action | Do not fabricate an answer. Do not convert inaccessible evidence into a disclosure or an automatic gap without the decision below. |
| Handover unresolved question | Handover / accepted MVP scope | Candidate source/reference for a gap, if Product confirms it is included in this workflow | The required source actions in DATN-413 name insufficient evidence and missing required knowledge; handover linkage is not yet an approved trigger for this contract. |

The Continuum record refers to a source only through its owning contract; the owning service remains responsible for source content and authorization. The contract must not expose SAG internals or treat link presence as an access grant. The accepted no-answer and missing/overdue paths do not require a SAG signal.

Keep the DATN human follow-up record distinct from SAG's internal scored-gap/question/research lifecycle. Do not reuse a SAG identifier as the DATN gap identifier or assume a direct foreign-key relationship. If integration needs correlation, define an opaque cross-system reference, its owning API, authorization checks, and lifecycle with the SAG owner.

## 4. Source-to-gap action mapping

| Trigger | Accepted product behavior | Candidate DATN action | Decision still required |
|---|---|---|---|
| Assistant cannot answer from authorized evidence | State insufficient evidence and offer a way to report a Knowledge Gap; never guess | An authorized actor can submit a report action that creates a human follow-up. This does not require the SAG quality model. | Product/Security must approve whether submission is explicit versus draft creation and what context is retained. Full prompt/evidence-body retention is not assumed. |
| Required knowledge is missing | Missing required knowledge creates a visible follow-up/reminder | Surface the existing requirement as a human action source; the actor can submit that action to create a human gap. | Product must identify the authoritative requirement/coverage API, assignee/routing policy, and whether any automated persistent record is allowed. |
| Required knowledge is overdue | Reminders for overdue required knowledge are in MVP | Surface the source requirement/review date and allow human submission; do not calculate a new freshness score. | Product must approve the overdue rule/source and any automated creation policy. J-01 does not invent a threshold. |
| Handover question remains unresolved | Handover records unresolved questions for human follow-up | Candidate link to the originating handover question/gap | Confirm whether handover creates/reuses a Knowledge Gap and which service owns the reference. |
| SAG emits a scored gap/reason | Current SAG code persists scored gaps and evidence-grounded questions internally; the registered HTTP routers do not expose a gap CRUD/source endpoint | **No DATN action in J-01.** Do not create or correlate a DATN gap from this internal SAG object. | A future integration needs a stable owner-approved SAG API/event, reference identity, and authorization contract. None was found in current `main`; this is a future integration blocker, not a J-01 blocker. |

## 5. Record contract inventory and legacy scaffold reconciliation

DATN-413 requires a versioned record/state contract. The backend source currently has a Mongo schema scaffold, but no gap application flow. Code presence is not approval. The J-01 contract therefore records the scaffold for the DATN-444 implementer and makes no schema change here.

| Existing field in `DATN-BE` `origin/main` | Current source meaning | J-01 disposition |
|---|---|---|
| `organizationId`, `projectId`, optional `teamId` | Scope identifiers | Keep Project as a required contract boundary. Team support is constrained by approved scope; optionality does not grant Project-wide visibility. Product/Security must define Teamless visibility and Team membership rules. |
| `responsibilityCode`, `title`, `description` | Existing unvalidated business fields | `title`/`description` can be reused as candidate human context; source/reason is still missing. Product decides required content, length, privacy/PII, and whether responsibility code belongs in MVP. |
| `severity` (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`) | Existing required enum | Not the SAG score, but no accepted Product rule defines who sets it or what behavior it drives. Do not use it for sorting, automation, or priority until Product decides; default recommendation is omit from J-01 MVP behavior. |
| `status` (`OPEN`, `IN_PROGRESS`, `RESOLVED`, `IGNORED`) | Existing required enum | `OPEN`/`IN_PROGRESS`/`RESOLVED` are candidate names, not accepted transitions. `IGNORED` has no J-01 acceptance basis. Product must approve states and transition rules before DATN-444 exposes them. |
| `assignedToUserId` | One assignee field | Supports an assignment candidate, but not a separate owner/reporter. Assignment rights, eligible targets, and whether unassigned is valid require Product/Security decision. |
| `resolvedByKnowledgeObjectId`, `resolvedAt` | Resolution link/time | Does not identify the human resolver. J-01 requires explicit human resolution; the contract needs resolver actor/audit evidence. Product decides outcome/note/knowledge-link requirements; Security decides who may resolve. |
| timestamps/index | Mongoose timestamps; index by organization/project/status/severity | Existing persistence metadata only. Retention, audit event, and index changes belong in the approved DB/API design for DATN-444. |

The items below come from DATN-413's required scope. Rows distinguish accepted requirements from decisions that need an owner; a missing runtime implementation is not itself a Product/Security policy blocker. Jira #10255 adds conditional dispositions after R0.4; §9.3 is the current status and supersedes earlier open rows only where it explicitly records an acceptance or amendment.

| Concept | Contract need | Status / unresolved detail |
|---|---|---|
| Project scope | Every gap has one Project boundary | **Explicit in task and product model.** Project identity is required; current authorization is rechecked on each operation. Cross-Project references are denied. |
| Team scope | Enforce Team scope when a gap is Team-scoped | **Conditionally accepted in Jira #10255.** Project gaps are visible to active Project members; Team gaps to active members of that Team unless an explicit scoped grant applies. No sibling-Team or role-title inference. Confirm Security authority against R0.5 if role separation applies. |
| Reason | Explain why follow-up exists | **Conditionally accepted in Jira #10255.** Reasons are `INSUFFICIENT_EVIDENCE`, `REQUIRED_KNOWLEDGE_MISSING`, and `REQUIRED_KNOWLEDGE_OVERDUE`; severity does not drive MVP prioritization or automation. |
| Source/provenance | Identify what initiated the follow-up | **Conditionally accepted in Jira #10255.** Require a source kind; retain only validated opaque references. Assistant no-answer and explicit missing/overdue reports are supported; handover and SAG scored-gap links are not approved J-01 sources. |
| Description/context | Give a human enough context to act | **P2 conditionally accepted.** Store an editable short summary, reason, source kind, reporter, and validated opaque references only. Do not copy protected prompts, answers, or evidence. Retention/deletion specifics remain open in §9.3. |
| Evidence link | Optional reference to evidence | **Optional.** Owning API validation, current ACL re-check, and no inherited access are required. Create/read handling for missing, stale, inaccessible, and cross-scope references remains open in §9.3. |
| Knowledge link | Optional reference to knowledge | **Optional per task.** Validate with the owning Knowledge API and confirm the same Project/Team policy. Presence does not mean the linked knowledge is verified or readable. |
| Task link | Optional reference to an internal task | **Optional per task.** Resolve through the Continuum Task API (not Jira sync); verify owning Project/Team scope and actor access. Decide stale/deleted-reference handling. |
| Owner / assignee | Human accountability and routing | **Conditionally accepted in Jira #10255.** Assignee remains optional. Creator may edit unresolved summary; assignee may update progress; appropriately scoped leaders may assign/reassign; assignee or scoped leader may resolve. Security confirmation and target eligibility remain to be recorded. |
| Status | Track lifecycle | **Conditionally accepted in Jira #10255.** Use user-driven `OPEN → IN_PROGRESS → RESOLVED`; no automatic resolution, `IGNORED`, or reopen behavior in MVP. |
| Resolution | Record explicit human outcome | **Human resolution is required.** On `RESOLVED`, record the human actor and an explicit outcome. Product has not yet supplied the outcome vocabulary or decided whether notes/evidence are mandatory; Security must confirm resolver authority. Automated resolution is excluded. |
| Audit / timestamps | Support accountability and change history | **Cross-cutting need; exact event mapping and retention are not selected.** The accepted actor baseline requires auditing relevant changes and excludes full prompts/document bodies from logs. DATN-422/audit owner must confirm the owning service's event/atomicity/retention contract before runtime implementation. |

Existing schema names/enums are noted above but are not approved by J-01. No new field names, API paths, error codes, or index changes are authorized by this document.

## 6. Lifecycle decision matrix

This matrix states the operations the contract must cover. Jira #10255 conditionally accepts the lifecycle and action baseline; the unresolved D-07 and reference details are called out explicitly and summarized in §9.3.

| Operation | Minimum behavior to define | Open contract decision |
|---|---|---|
| Create | Persist only after explicit user submission for both no-answer and missing/overdue reports; bind Project and required fields; validate each supplied reference | Security/API must decide whether an invalid optional reference rejects the whole create or is omitted; exact external error follows the confirmed owning API convention. |
| List | Return only gaps visible to the caller in current Project/Team scope | Project-member and same-Team visibility are conditionally accepted; Security must confirm role authority and any explicit scoped-grant handling. |
| Detail | Return only fields and references allowed by resource/source ACL | Reauthorize each reference on read; Security/API must confirm whether an inaccessible reference is omitted or causes the parent read to fail, without protected metadata. |
| Update | Permit only selected mutable fields and authorized actors | Creator summary edit while unresolved, assignee progress update, and scoped-leader assignment are conditionally accepted; exact immutable fields and role confirmation remain. |
| Assign | Route to an eligible in-scope human | The scoped-leader assignment baseline is conditionally accepted. Security/API must confirm eligible assignee types, assigner permission, self-assignment, clearing/reassignment, and audit requirements. |
| Resolve | Human-driven transition to `RESOLVED`; record actor and explicit outcome | Product must choose outcome vocabulary and whether notes/evidence are required; Security must confirm resolver authority against R0.5. |
| Reopen or withdraw | Not required by the acceptance criteria as written | Decide whether supported in MVP. Until decided, do not invent a transition or imply automatic reopen behavior. |

## 7. Authorization and reference safety matrix

The accepted authorization baseline is active membership, explicit scope, resource/source ACL, and deny precedence. Jira #10255 conditionally accepts Project-member visibility, same-Team visibility for Team-scoped gaps, and the proposed action grants. The comment's author is identified as Project Lead in the closure context; separate Security/API authority is not independently established. Do not treat this matrix as final Security approval until the named Security owner confirms it against R0.5. A `TEAM_LEADER` acts only in explicitly assigned Project/Team scope. Organization `ADMIN` and `PLATFORM_OPERATOR` receive no default confidential-content access. `SME`, `KNOWLEDGE_OWNER`, and `SUCCESSOR` are scoped assignments, not persistent roles.

| Action | Known guardrail | Decision required before implementation |
|---|---|---|
| Create/report | Persist only after explicit user submission for both no-answer and missing/overdue reports; bind to an authenticated actor and authorized Project/source context | Product must confirm this baseline against R0.5. Security/API must specify whether an invalid optional reference rejects create or is omitted, plus the safe error response. |
| List/detail | Apply current membership, scope, and ACL; references cannot widen visibility | Project-member and same-Team visibility are conditionally accepted. Security must confirm authority and field exposure; reauthorize each linked reference on read. |
| Update | Do not let an actor change Project/Team or source references to escape scope | Proposed grants are conditionally accepted: creator edits unresolved summary, assignee updates progress, scoped leader assigns/reassigns. Security must confirm role authority and exact mutable fields. |
| Assign | Target an eligible human in the gap's approved scope | Scoped-leader assignment is conditionally accepted; eligible assignee types, membership, reassignment, and audit behavior need Security/API confirmation. Task assignment rules do not automatically transfer to gaps. |
| Resolve | Resolution is an explicit human action; preserve the human actor and outcome | Product must specify outcome vocabulary and notes/evidence requirements. Security must confirm resolver grant and whether reporter self-resolution is allowed. |
| Link evidence/knowledge/task | Validate through the owning API, require same authorized Project and applicable Team scope, reauthorize on every read, and do not copy protected content | Define create/read behavior for missing, stale, inaccessible, and wrong-scope references. No protected metadata may be returned. |
| Cross-scope attempt | Deny; do not reveal protected object contents or use a link as a grant | Security/API must confirm when to conceal existence with 404 versus safely acknowledge denial with 403, consistent with the owning API. |

## 8. Authorization and behavior scenarios to specify

These are contract scenarios, not evidence that runtime tests have been run.

| ID | Scenario | Expected invariant |
|---|---|---|
| G-01 | Authorized member reports insufficient evidence from an in-scope assistant session | No answer is fabricated; the report action is available; any created record follows the approved confirmation rule and contains only permitted context. |
| G-02 | An authorized actor follows up on a missing required-knowledge item | The source requirement and Project scope are validated; no score is required; auto-create vs human-confirm behavior follows the approved rule. |
| G-03 | An overdue requirement is reported | The approved overdue rule is used; no new freshness/conflict score is calculated. |
| G-04 | Actor creates a gap with an authorized evidence, knowledge, or internal task link in the same scope | Each reference is confirmed by its owning API and remains subject to its own ACL. |
| G-05 | Actor supplies a reference from another Project or Team | Request is denied without cross-scope content disclosure; exact response code follows the approved Security/API rule. |
| G-06 | Actor links an inaccessible or stale reference | No content is copied or revealed; create/read outcome follows the approved stale/inaccessible-reference rule. |
| G-07 | Organization Admin or Platform Operator lacks a separate Project membership/authorization | No default gap content access is granted. |
| G-08 | Team Leader acts outside the assigned Team/Project scope | Mutation and read are denied; sibling Team scope is not inferred. |
| G-09 | Unauthorized actor attempts list, detail, update, assignment, or resolution | Each action is independently checked; no action permission is inferred from another action or a role title. |
| G-10 | Authorized human resolves a gap | A human actor and the approved resolution outcome are recorded; resolution does not silently verify knowledge or launch SAG research. |
| G-11 | Repeated assistant report or repeated missing-knowledge signal | Duplicate, merge, or multiple-record behavior follows an approved rule; no deduplication key is assumed here. |
| G-12 | Membership, Team assignment, ACL, or linked-object access changes after the gap was created | Subsequent reads and mutations re-check current authorization; stored references do not preserve revoked access. |

## 9. Decision register and blockers

| ID | Decision needed | Owner domain | Blocks |
|---|---|---|---|
| D-01 | Does insufficient evidence only offer a report, create a draft, or persist a gap after explicit user confirmation? Which assistant context can be retained? | Product + Security | Product conditionally accepts explicit submission and minimal context; confirm against R0.5 and settle retention. |
| D-02 | What is the authoritative source and overdue rule for missing/overdue follow-up? | Product + Knowledge Owner | Explicit user submission is conditionally accepted; the requirement/overdue source and rule remain open. |
| D-03 | How do Project-level and Team-level visibility interact? | Product + Security | The proposed Project-member and same-Team visibility is conditionally accepted; Security authority and role confirmation remain. |
| D-04 | Which reason and source values are canonical? | Product | Conditionally accepted values and source kind are recorded in #10255; Product must confirm the amended R0.5 package. |
| D-05 | Which fields are required or optional, and which are immutable? | Product | The proposed required/optional field set is conditionally accepted; confirm R0.5 and exact mutability before runtime implementation. |
| D-06 | Which scoped actors may create, view, update, assign, and resolve? | Product + Security | S1/S2 are labeled accepted in #10255, but independent Security authority and exact role/target eligibility need confirmation. |
| D-07 | What resolution outcome vocabulary applies, and are notes/evidence required? | Product | Amendment requested in #10255. Keep `OPEN → IN_PROGRESS → RESOLVED`; outcome vocabulary and notes/evidence requiredness remain open. |
| D-08 | Which owning APIs validate references, and what are the denial/audit conventions? | Architecture + owning service owners + Security | SAG independence is accepted as a boundary; owning-API validation and shared denial/audit conventions still need confirmation. |
| D-09 | What response and field visibility rules apply to missing, stale, inaccessible, or cross-scope references? | Security + API owners | Amendment requested in #10255; specify safe create/read outcomes and confirm 403/404 convention. |
| D-10 | What duplicate/replay behavior applies when the same source signal is submitted again? | Product + Architecture/API | No fuzzy merge and stable idempotency key for automatic retries are conditionally accepted; confirm R0.5. |

Jira #10255 is the latest disposition, but it is conditional and was made in discussion of R0.4. The comment author is identified as Project Lead in the closure context; separate Security, API/Architecture, and audit-owner authority is not independently established. R0.5 requests confirmation against its exact commit. Until then, only the explicitly recorded constraints are conditional dispositions, not implementation-ready policy.

### 9.1 R0.2 decision classification and disposition

Classification key: **A** = explicit in an accepted source or Jira acceptance criterion; **T** = bounded technical choice that J-01 may make without changing product/security policy; **P** = Product approval; **S** = Security approval; **API** = owning service/API owner confirmation. This table preserves the R0.2 analysis; current dispositions are recorded in §9.3.

| R0.2 topic / decision | Class | Settled now | Remaining decision and owner |
|---|---|---|---|
| D-01 Insufficient-evidence trigger | **A + T + P/S** | State insufficient evidence and offer a Knowledge Gap report action; do not fabricate an answer. A DATN record is separate from SAG's scored gap. | Whether the UI creates a draft or persists only after explicit submit, which context may be retained, and PII limits — Product + Security. |
| D-02 Missing/overdue follow-up | **A + T + P** | Missing/overdue required knowledge has a visible follow-up/reminder; no quality score is needed. A source requirement can be shown for human action. | Whether an automated signal creates a persistent record, authoritative requirement/overdue rule, and routing — Product with Knowledge Owner. DATN-451 implements only after approval. |
| D-03 Project/Team scope | **A + T + P/S** | One Project can contain multiple Teams. Bind each gap to one Project; never infer sibling-Team access. | Whether Team is optional/derived and what Teamless or Project-level visibility grants — Product + Security. |
| D-04 Reason/source taxonomy | **A + P** | J-01 names insufficient evidence and missing required knowledge as source families; advanced scoring/priority is not required. | Canonical reason/source values, multiple-reason policy, and whether the existing `severity` field is a human label or omitted — Product. |
| D-05 Required fields and mutability | **A + P** | Project, reason/source concept, ownership, status, allowed links, and resolution must be defined in the contract. Existing `title`/`description` are only implementation candidates. | Exact required fields, immutable fields, context limits, and unassigned-gap policy — Product; privacy-sensitive context — Security. |
| D-06 Action grants | **A + S/P** | Baseline permits a Member to flag a gap; authorization uses active membership, explicit scope, resource ACL, and deny precedence. Organization Admin/Platform Operator have no default confidential-content access. | Exact create/list/detail/update/assign/resolve grants, target eligibility, reporter self-resolution, and field visibility — Security + Product. |
| D-07 Lifecycle/resolution | **A + T + P/S** | Human resolution is explicit; no automatic resolution or SAG crawl. Existing `OPEN`/`IN_PROGRESS`/`RESOLVED` values can be reused as candidates only. | Initial state, transitions, `IGNORED`/reopen policy, outcome/note/evidence, resolver authority — Product + Security. |
| D-08 Optional cross-service links | **A + T + P/S/API** | Evidence/Task references go through owning APIs and cannot widen access; Task is Continuum-owned, not Jira-synced. Use no copied protected content or direct SAG foreign key. | Which concrete Knowledge/Evidence/Task endpoints and same-Team rules apply, failure/concealment behavior, and any SAG source contract — Architecture + owning API owners + Security. |
| D-09 Unauthorized/cross-scope responses | **A + S/API** | Deny cross-scope access, re-check current authorization, and return no protected metadata. | 403 vs 404 concealment and field-level response rules — Security + API owners. |
| D-10 Duplicate/replay | **T + P/API** | Do not fuzzy-merge by text/reason. Do not automate retrying a source trigger until an idempotency key and owner contract exist. | Whether human reports may be separate or merged and exact idempotency semantics — Product + Architecture/API. |
| SAG correlation | **A + T + API** | SAG's quality/research model remains separate; current SAG main exposes no gap CRUD route or stable DATN reference. Keep IDs independent and do not call an assumed endpoint. | Add a typed SAG source reference only after the SAG owner publishes and confirms an API/event and authorization contract — SAG/API owner + Security. This does not block J-01. |

R0.2 classification is historical. It must not override Jira #10255 or the current status in §9.3. Bounded technical invariants remain usable as contract constraints; proposal-only policy remains unselected until its owner confirms it.

### 9.2 Recommended defaults for review — proposal only

The following defaults are the historical R0.2/R0.4 proposal package. Jira #10255 conditionally accepts or amends selected rows; see §9.3 for the current disposition. Any row not explicitly accepted there remains a proposal and must not be treated as approved behavior.

| Topic | Recommended default | Why / limit |
|---|---|---|
| Insufficient-evidence trigger | The assistant offers **Report a Knowledge Gap**; the user reviews and confirms before a persistent record is created. Prefill only a short editable question summary and authorized source references. | Preserves human ownership, avoids retaining full prompts by default, and follows the accepted assistant behavior of offering a gap rather than guessing. |
| Missing/overdue knowledge | Show an in-scope follow-up action from the configured knowledge requirement; let an authorized human confirm creation. Use the existing requirement/review-date owner as the source of truth. | Delivers visible follow-up without inventing an overdue score or silently creating records from unreviewed signals. Exact overdue policy still needs Product decision. |
| Scope | Require one Project per gap; allow an optional Team only when the initiating requirement/source is Team-scoped and that parent relationship is validated. Never infer sibling-Team visibility. | Matches the one-Project/multiple-Team MVP boundary while preserving Team isolation. |
| Minimal record | Require Project, one primary reason, source kind, concise human-readable summary, reporter, status, and created/updated timestamps. Make Team, assignee, detail, and typed evidence/knowledge/task references optional. Keep creator and assignee distinct. | Gives the workflow enough context to route and resolve while keeping open questions about exact storage/API names for later contracts. |
| Reason/source | Start with three candidate reasons: `INSUFFICIENT_EVIDENCE`, `REQUIRED_KNOWLEDGE_MISSING`, and `REQUIRED_KNOWLEDGE_OVERDUE`. Require one source kind; allow an opaque source reference where a stable owning API exists. | Directly maps the two required trigger families and keeps SAG score/research details out of the DATN record. Human reports without a source reference need an explicit Product rule. |
| Lifecycle | Candidate states: `OPEN` on creation, `IN_PROGRESS` after an authorized human takes ownership, and `RESOLVED` after an explicit human resolution. Do not auto-resolve; defer reopen/cancel states from MVP unless Product requires them. | Small lifecycle covers create, track, and resolve without importing SAG research-task statuses. Names remain proposals. |
| Assignment | Allow an unassigned gap. Permit assignment/reassignment only by an explicitly authorized Project/Team leader in that same scope; target only an active eligible member or approved scoped knowledge owner. | Avoids inventing a new persistent role or granting authority to Organization Admin. Exact Team Leader grants remain subject to Security/IAM confirmation. |
| Read/update/resolve | Check current membership, explicit Project/Team scope, and source ACL on every operation. Let a reporter update their own unresolved summary; let the assignee update progress; let an authorized scoped leader manage assignment. Resolve through a human with an approved scope grant. | Defines a least-privilege review candidate; Product/Security must decide exact grants, self-resolution, and mutable fields. Resolving a gap must not itself verify knowledge. |
| Optional links | Store typed opaque references and validate them through each owning API; enforce same Project and applicable Team scope; reauthorize when read. Do not use direct cross-service foreign keys or copy linked content into the gap. | Keeps data ownership with Knowledge, Evidence, Task, or SAG owners and prevents references from expanding access. |
| Duplicates | Do not merge records by fuzzy reason/text matching. Require a stable source-event key before automating retries; human submissions may remain separate until a merge policy is approved. | Avoids hiding distinct questions and keeps automation idempotency explicit. |
| Unauthorized references | Return no protected metadata and use the shared API error contract; Security/API owners select whether the external response conceals existence. | Preserves a consistent contract and leaves 403/404 behavior to the owning Security/API decision. |
| SAG correlation | Keep a DATN gap ID independent. If needed, use a separate opaque SAG source reference confirmed by the SAG owner; do not persist a SAG score or make a direct FK into SAG storage. | Allows the human follow-up contract to proceed while broader SAG interface work continues. |

Product and Security should accept, amend, or reject each row explicitly. Architecture and API owners should confirm only the cross-service rows; their technical review does not replace Product/Security approval.

### 9.3 R0.5 disposition and closure gates

Jira comment **#10255**, posted 2026-10-18 by KeyT, is the latest role-labeled disposition. The closure context identifies KeyT as Project Lead. The comment discusses R0.4 and does not cite its commit SHA; R0.5 records the disposition without treating it as unconditional approval. Jira does not establish separate Security, API/Architecture, or audit-owner authority for the author. Obtain their explicit confirmations against the R0.5 commit before claiming those approvals.

| Area | Disposition recorded in #10255 | R0.5 state |
|---|---|---|
| Product P1/P2, D-04/D-05, D-10, G-01–G-12 | Labeled ACCEPT, subject to the D-07 amendment | Conditional Project Lead disposition. Confirm against R0.5; P1 requires explicit submission for both trigger families, P2 limits stored content to the editable summary and approved metadata/references. |
| Product P3/D-07 | Labeled AMEND; keep `OPEN → IN_PROGRESS → RESOLVED`, define required resolution outcome and whether notes/evidence are required | **Open.** Product must choose the outcome vocabulary and whether notes/evidence are optional, required, or disallowed. No reopen or automatic resolution is introduced. |
| Security S1/S2/S3 | Labeled ACCEPT as proposed; specify retention/deletion for summary and reporter metadata | **Conditional; Security authority and exact retention/deletion rules unconfirmed.** No TTL, deletion trigger, or cascade behavior is selected. |
| Security/API S3, G-05/G-06 | Labeled AMEND; define create/read behavior for missing, stale, inaccessible, and cross-scope references, with no protected metadata returned | **Open.** The no-protected-metadata invariant is recorded; operation outcomes and error/concealment behavior need Security/API confirmation. |
| API/Architecture D-08 | Labeled ACCEPT for SAG boundary; confirm owning-API validation and existing denial/audit conventions | **Boundary accepted conditionally; conventions open.** Do not assume a SAG endpoint, foreign key, or trigger. Confirm owner APIs and shared API/audit contracts. |

#### Decisions to close

1. **D-07 resolution (Product):** choose one of these requirement shapes and supply the outcome vocabulary: **A.** controlled outcome is required and notes/evidence are optional; **B.** controlled outcome and a short resolution note are required; **C.** controlled outcome plus an approved evidence reference is required. Product may amend the choices. A resolving human and timestamp are required by the accepted human-resolution invariant; outcome labels are not invented here.
2. **Retention/deletion (Product + Security):** choose **A.** a fixed retention period with deletion or anonymization after resolution; **B.** an existing approved Project/Team records schedule; or **C.** another explicit schedule and deletion trigger. State the period/trigger and treatment for reporter departure/erasure, Project/Team deletion, legal hold, resolved records, and audit events. The covered data includes summary, reporter identifier, reason/source metadata, opaque references, any approved resolution notes/evidence, and audit records. Define application-record and audit retention separately if they differ. No TTL, soft-delete, hard-delete, or cascade rule is authorized by R0.5. A research-only audit proposal's seven-day value is not adopted; DATN-422 remains To Do.
3. **Reference create behavior (Security + owning API):** for a supplied optional reference that is missing, stale, inaccessible, or cross-scope, choose **A.** reject the whole create with the owning API's safe error; or **B.** omit the invalid reference, create the otherwise valid gap, and return a safe field-level validation result. In either case do not persist or reveal protected target metadata. Confirm status/error conventions from the owning API.
4. **Reference read behavior (Security + owning API):** if the caller may read the gap but can no longer read a linked object, choose **A.** omit that reference from the response; or **B.** fail the whole gap read with a safe generic response. Reauthorize the gap and every reference on each read. If the caller cannot read the gap, apply the approved concealment rule and return no protected metadata.
5. **Authorization and denial convention (Security + API/Architecture):** confirm S1/S2 and the conditional S3 baseline against R0.5, including Teamless visibility, scoped-grant semantics, assignee eligibility, resolver authority, and when existing conventions use 403 versus existence-concealing 404. The C-07 examples are recommendations pending API/IAM/Security confirmation; they do not settle the convention for Knowledge Gaps.
6. **Audit/API boundary (API/Architecture + audit owner):** identify the owning APIs for each supported reference kind, confirm their validation and current-ACL behavior, and confirm event names, atomicity expectations, and audit retention through the approved audit owner/DATN-422. No research-only value is promoted to policy.
7. **Revision-specific disposition:** Product confirms its accepted/amended entries above against the exact R0.5 commit. A named Security owner and API/Architecture owner separately accept or amend their entries, and the audit owner confirms the audit convention. A Jira/PR merge or an author's role labels alone do not satisfy this gate.

Until these decisions are recorded, the contract evidence is reviewable but not fully approved or implementation-ready. Runtime work in DATN-444/448/451 remains downstream; none of the decisions above authorizes guessing an integration contract while those implementation issues are To Do.

## 10. Work completed and remaining gates

| Work item | Evidence completed | Remaining gate |
|---|---|---|
| DATN-413 scope/dependencies | Read full parent acceptance criteria, DATN-414/415, and linked DATN-444/448/451. DATN-63/64 are Done; DATN-444 (persistence/API), DATN-448 (UI), and DATN-451 (trigger integration) are downstream To Do items blocked by DATN-413. | No application code from those downstream tasks is included in J-01. |
| DATN-414 — separate SAG signals | Current SAG schema, quality/question services, research task model/planner, API router registry, principal assertion, current `main`, PR 28, and open PR list were inspected. The matrix now distinguishes internal SAG signals from the DATN human record and records that no SAG gap CRUD interface is published. | The owner must confirm any future event/API before a SAG reference is introduced. This does not block J-01. |
| DATN-415 — fields/ownership/resolution | Contract inventory, existing DATN backend scaffold, state candidates, actor/scope invariants, G-01–G-12, and the updated D-01–D-10 disposition register are recorded. Jira #10255 has a conditional Project Lead disposition and concrete Product/Security/API amendments. | DATN-415 remains In Progress. Product must close D-07 and confirm R0.5; independent Security, API/Architecture, and audit-owner decisions remain unconfirmed. |
| Runtime implementation survey | DATN-BE/FE current refs and relevant source were inspected. Backend has a gap schema/persistence index but no gap workflow; frontend has no gap UI. | Storage/API, UI, and assistant/coverage triggers belong to DATN-444/448/451, not J-01. No DB, BE, FE, SAG, or runtime behavior was changed. |
| Verification | The Document repository has no `package.json`, `Makefile`, or CI workflow defining lint/typecheck/unit/integration/E2E/build commands. Source searches were refreshed against current BE/FE `origin/main`. | G-scenarios are contract oracles, not executed J-01 application tests. Separate baseline checks and the latest-main BE E2E result are recorded in the Jira validation comment; they do not validate this documentation change. |

### Remaining approval blockers

1. **Product:** choose the D-07 resolution outcome and whether notes/evidence are required; confirm conditional P1/P2, D-04/D-05, D-10, and G-01–G-12 against exact R0.5; identify the authoritative missing/overdue requirement source.
2. **Security:** a named Security owner must confirm S1/S2 and the amended S3 behavior against R0.5; specify retention/deletion; choose reference create/read behavior and the safe concealment/error rule.
3. **API/Architecture and audit owner:** confirm owning-API validation, existing denial and audit conventions, and event/atomicity/retention expectations. DATN-422 is To Do, so no audit TTL or event contract is inferred.

Jira records a conditional role-labeled disposition, not full authority-backed approval. The contract evidence and SAG boundary work are complete; the expected **approved** contract result is not achieved.

## 11. Current outcome

- **Contract evidence complete:** versioned contract, accepted-source map, SAG reuse boundary, DATN scaffold reconciliation, lifecycle matrix, authorization/reference matrix, 12 contract scenarios, and decision disposition register.
- **J-01 acceptance:** the versioned contract, mapping, authorization/scenario matrices, SAG boundary evidence, and explicit blocker list are present. The creation rule is conditionally accepted as explicit user submission for both trigger paths. Human-only lifecycle states are conditionally accepted, but D-07's outcome and notes/evidence requirement remain open. Reference operation behavior, retention, and role-specific confirmations remain incomplete. The expected approved-contract result is not met.
- **SAG dependency:** DATN-63/64 and PR 28 are complete. Current SAG `main` has internal scored-gap/research persistence but no published gap CRUD API; broader unpushed team work cannot be ruled out. This does not block J-01, only future integration assumptions.
- **Implementation scope:** no DB, BE, FE, SAG, or runtime changes in J-01. Jira-linked J-02/J-03/J-04 own persistence/API, UI, and trigger integration. App baseline checks were run separately and are not DATN-413 implementation tests.
- **External state at R0.5 preparation:** DATN-413 and DATN-415 are In Progress; DATN-414 is Done. PR #45 is merged at `95edc801a68da2d6a4c23efaaf83bbe7d3d42279`, based on contract R0.4. GitHub has no review submissions, inline review threads, or PR comments for #45. Jira #10255 is the latest role-labeled disposition but is conditional, discusses R0.4 without citing its SHA, and requests amendments. This does not satisfy approval of R0.5. Record the exact R0.5 commit and review link in Jira when published. Keep DATN-413 not-Done until the approved-contract acceptance outcome is evidenced.
