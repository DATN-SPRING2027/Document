# DATN-413 — Human Knowledge Gap and Follow-up Contract

## Document status

- Revision: **R0.6, updated 2026-10-19 (Asia/Bangkok)**
- State: **R0.6 records the task owner's supplied KeyT D-07 disposition: successful resolution uses the `RESOLVED` outcome, always includes a resolution note, and includes evidence references when available; an empty reference list requires the note to explain why no reference exists. It does not add `WONT_FIX` or `DUPLICATE` without explicit acceptance. Retention policy, audit details, and API-specific create/read/error choices remain proposals or open decisions where the supplied text asks for approval or requires existing conventions.**
- Jira: [DATN-413](https://trankimthang0207.atlassian.net/browse/DATN-413)
- Related subtasks: [DATN-414](https://trankimthang0207.atlassian.net/browse/DATN-414), [DATN-415](https://trankimthang0207.atlassian.net/browse/DATN-415)
- Evidence base: Document `origin/main` at merged PR #45 commit `95edc801a68da2d6a4c23efaaf83bbe7d3d42279`; task-linked Jira records; DATN-BE `origin/main` at `9e3227925d01532b6e26336a77b38895392112b5`; DATN-FE `origin/main` at `217a9da38ca8db5334aeab51f2dea854a02844b1`; and SAG `main` at `ab27c61e90fb24ea0e73ea935f68baee36ba9942`, checked 2026-10-18.
- Decision evidence: Jira comment #10255 records KeyT's accepted/amended Product, Security, and API/Architecture dispositions. On 2026-10-19 the task owner confirmed KeyT's delegated authority over all those domains. The task owner then supplied the D-07 decision package in this task. This revision identifies the contract SHA in the follow-up Jira comment so the disposition is revision-specific. The package gives concrete D-07 requirements but labels the retention periods and several HTTP outcomes as proposals, so those are not recorded as approved.
- Approval evidence: **The task owner confirmed KeyT's delegated overall-lead authority.** Existing authorized acceptances remain in force; the supplied D-07 constraints are recorded as the task owner's disposition. No `WONT_FIX`/`DUPLICATE` outcome, 90/365-day retention period, or unsupported API convention is inferred as approved.
- Scope gate: DATN-413 is the Phase 1 contract task. Persistence/API, UI, and trigger implementation are separately scoped by DATN-444, DATN-448, and DATN-451 and are blocked by this contract. This document does not create or change application schemas, grants, endpoints, or runtime behavior.

This is the versioned J-01 contract and evidence package. It separates accepted rules, bounded technical choices, existing code that is not yet a contract, and the remaining choices for the officially delegated overall lead, KeyT. Jira `Done`, code presence, technical review, and PR merge do not decide open policy choices.

### Revision history

| Revision | Change |
|---|---|
| R0.1 | Clarify that DATN-63/64 and PR 28 are complete while broader SAG work may continue; keep SAG integration details open until its owner confirms the stable interface. |
| R0.2 | Add non-binding recommended defaults to make the Product/Security decision review concrete. No recommendation is selected policy. |
| R0.3 | Reconcile every J-01 criterion with Jira, current DATN-BE/FE source, and current SAG `main`; classify decisions, record the existing schema mismatch, and add an acceptance checklist with completion evidence and remaining approval blockers. |
| R0.4 | Refresh BE/FE source refs; verify that J-02/J-03/J-04 still own runtime work; record the exact PR/Jira review state and the corrected BE IAM E2E test on current `origin/main`. No Product/Security disposition is presumed. |
| R0.5 | Incorporate Jira #10255's authorized Product/Security/API disposition; record the exact remaining D-07, retention/deletion, reference create/read, and API/audit choices; correct PR #45's merged state. Updated 2026-10-19 to reflect the task owner's confirmation of KeyT's delegated authority. |
| R0.6 | Record the task owner's supplied KeyT D-07 resolution requirements; keep unapproved extra outcomes and proposal-only retention periods/API status codes explicit; update the revision-specific disposition and J-01 evidence. |

## Acceptance checklist (J-01)

| Jira criterion / completion evidence | Result | Evidence and limit |
|---|---|---|
| Gap fields, states, ownership, links, and actor/scope are explicit or recorded as decision blockers | **Met at contract level.** §§5–9.3 record accepted policy, D-07, and remaining retention/reference details. | Retention duration and exact API-specific error/read outcomes remain explicit implementation gates. |
| Insufficient-evidence and required-knowledge follow-up can create a gap without inventing a score | **Met at contract level.** Jira #10255 accepts explicit user submission for both paths and minimal stored context. | Retention period is still pending; no automatic overdue creation or scoring is allowed. |
| Human resolution is explicit; advanced scoring/autonomous crawl is excluded | **Met at contract level.** Human-only `OPEN → IN_PROGRESS → RESOLVED` is authorized. `RESOLVED` requires a note, resolver, timestamp, and a valid reference unless the note explains why references are absent. | `WONT_FIX` and `DUPLICATE` are not in MVP absent explicit acceptance. |
| Task/evidence references use owning APIs and cannot widen access | **Met as a contract invariant.** Owning APIs validate references; each use reauthorizes; references never grant access; unavailable authorization results cannot support sensitive actions. | Exact status/error behavior follows verified existing API conventions; stale/unreadable reference handling must not expose protected metadata. |
| Required completion evidence: versioned contract/state matrix, source-to-gap mapping, authorization/test scenario matrix | **Met in this package.** See §§3–4, 6–8. | Scenarios are acceptance oracles, not evidence of runtime test execution. J-01 does not implement J-02/J-03/J-04. |
| Expected result: approved human-owned workflow contract | **Partly met.** KeyT's authorized acceptances and the supplied D-07 decision are recorded. | Retention/deletion period and exact reference/API outcomes remain open; confirm those choices or explicitly accept the contract with these bounded implementation gates before Jira can be marked Done. |

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
| Required knowledge missing or overdue | Continuum product workflow / accepted MVP scope | Provide a visible follow-up action tied to the configured requirement; persist a DATN gap only after explicit human submission | No automatic record creation in MVP. The owning service must identify the authoritative requirement/review-date source and its existing overdue rule; no new score or threshold is invented here. |
| Assistant has insufficient authorized evidence | Assistant / accepted MVP scope and daily workflow | State insufficient evidence and offer a user-controlled report/follow-up action; persist only after explicit submit | Do not fabricate an answer. Do not convert inaccessible evidence into a disclosure or create a record before user submission. |
| Handover unresolved question | Handover / accepted MVP scope | Candidate source/reference for a gap, if Product confirms it is included in this workflow | The required source actions in DATN-413 name insufficient evidence and missing required knowledge; handover linkage is not yet an approved trigger for this contract. |

The Continuum record refers to a source only through its owning contract; the owning service remains responsible for source content and authorization. The contract must not expose SAG internals or treat link presence as an access grant. The accepted no-answer and missing/overdue paths do not require a SAG signal.

Keep the DATN human follow-up record distinct from SAG's internal scored-gap/question/research lifecycle. Do not reuse a SAG identifier as the DATN gap identifier or assume a direct foreign-key relationship. If integration needs correlation, define an opaque cross-system reference, its owning API, authorization checks, and lifecycle with the SAG owner.

## 4. Source-to-gap action mapping

| Trigger | Accepted product behavior | Candidate DATN action | Decision still required |
|---|---|---|---|
| Assistant cannot answer from authorized evidence | State insufficient evidence and offer a way to report a Knowledge Gap; never guess | An authorized actor can explicitly submit a report action that creates a human follow-up. This does not require the SAG quality model. | Jira #10255 accepts explicit submission and minimal context; retention/deletion details remain open. Full prompt/evidence-body retention is not assumed. |
| Required knowledge is missing | Missing required knowledge creates a visible follow-up/reminder | Surface the configured requirement as a human action source; create a gap only after explicit user submission. | No automatic record creation in MVP. The owning API/service must identify the authoritative requirement/coverage source and technical routing capabilities. |
| Required knowledge is overdue | Reminders for overdue required knowledge are in MVP | Surface the configured requirement/review date and allow explicit human submission; do not calculate a new freshness score. | No automatic record creation or invented threshold. The existing source owner confirms which overdue rule and data source are used. |
| Handover question remains unresolved | Handover records unresolved questions for human follow-up | Candidate link to the originating handover question/gap | Confirm whether handover creates/reuses a Knowledge Gap and which service owns the reference. |
| SAG emits a scored gap/reason | Current SAG code persists scored gaps and evidence-grounded questions internally; the registered HTTP routers do not expose a gap CRUD/source endpoint | **No DATN action in J-01.** Do not create or correlate a DATN gap from this internal SAG object. | A future integration needs a stable owner-approved SAG API/event, reference identity, and authorization contract. None was found in current `main`; this is a future integration blocker, not a J-01 blocker. |

## 5. Record contract inventory and legacy scaffold reconciliation

DATN-413 requires a versioned record/state contract. The backend source currently has a Mongo schema scaffold, but no gap application flow. Code presence is not approval. The J-01 contract therefore records the scaffold for the DATN-444 implementer and makes no schema change here.

| Existing field in `DATN-BE` `origin/main` | Current source meaning | J-01 disposition |
|---|---|---|
| `organizationId`, `projectId`, optional `teamId` | Scope identifiers | Keep Project as a required contract boundary. Team support is constrained by approved scope; optionality does not grant Project-wide visibility. Jira #10255 accepts Project-member visibility and same-Team visibility for Team-scoped records; no sibling-Team access is inferred. |
| `responsibilityCode`, `title`, `description` | Existing unvalidated business fields | `title`/`description` may implement the accepted editable short summary; source/reason are defined separately in #10255. KeyT decides exact length and whether `responsibilityCode` belongs in MVP. |
| `severity` (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`) | Existing required enum | Not the SAG score. Jira #10255 accepts that severity drives no MVP priority or automation. KeyT must decide whether the legacy field is omitted or retained as a human-only label; it must not affect ranking or automation. |
| `status` (`OPEN`, `IN_PROGRESS`, `RESOLVED`, `IGNORED`) | Existing required enum | Jira #10255 accepts human-driven `OPEN`/`IN_PROGRESS`/`RESOLVED` and excludes `IGNORED`, automatic resolution, and reopen in MVP. R0.6 defines a successful `RESOLVED` outcome with required note, human resolver, and timestamp; `IGNORED` remains excluded. |
| `assignedToUserId` | One assignee field | Supports an assignment candidate, but not a separate owner/reporter. Assignee is optional under #10255; KeyT must decide exact eligible targets, self-assignment, and reassignment details. |
| `resolvedByKnowledgeObjectId`, `resolvedAt` | Resolution link/time | Does not identify the human resolver. R0.6 requires `resolutionOutcome`, `resolutionNote`, `resolvedBy`, `resolvedAt`, and `evidenceReferences[]`; a human-readable note must explain an empty reference list. The S2 resolver grant is accepted. |
| timestamps/index | Mongoose timestamps; index by organization/project/status/severity | Existing persistence metadata only. Retention, audit event, and index changes belong in the approved DB/API design for DATN-444. |

The items below come from DATN-413's required scope. Rows distinguish accepted requirements from decisions that need KeyT's disposition; a missing runtime implementation is not itself a policy blocker. Jira #10255 adds authorized dispositions after R0.4; §9.3 is the current status and supersedes earlier open rows only where it explicitly records an acceptance or amendment.

| Concept | Contract need | Status / unresolved detail |
|---|---|---|
| Project scope | Every gap has one Project boundary | **Explicit in task and product model.** Project identity is required; current authorization is rechecked on each operation. Cross-Project references are denied. |
| Team scope | Enforce Team scope when a gap is Team-scoped | **Accepted by authorized disposition in Jira #10255.** Project gaps are visible to active Project members; Team gaps to active members of that Team unless an explicit scoped grant applies. No sibling-Team or role-title inference. |
| Reason | Explain why follow-up exists | **Conditionally accepted in Jira #10255.** Reasons are `INSUFFICIENT_EVIDENCE`, `REQUIRED_KNOWLEDGE_MISSING`, and `REQUIRED_KNOWLEDGE_OVERDUE`; severity does not drive MVP prioritization or automation. |
| Source/provenance | Identify what initiated the follow-up | **Conditionally accepted in Jira #10255.** Require a source kind; retain only validated opaque references. Assistant no-answer and explicit missing/overdue reports are supported; handover and SAG scored-gap links are not approved J-01 sources. |
| Description/context | Give a human enough context to act | **P2 accepted by authorized disposition.** Store an editable short summary, reason, source kind, reporter, and validated opaque references only. Do not copy protected prompts, answers, or evidence. Keep minimum business data while active; exact periods remain open in §9.3. |
| Evidence link | Optional reference to evidence | **Optional.** Owning API validates existence and current ACL; reauthorize on every read/use; no inherited access. Unavailable/stale links are never proof of resolution. Exact HTTP codes follow verified API convention. |
| Knowledge link | Optional reference to knowledge | **Optional per task.** Owning Knowledge API validates each reference and current ACL. Presence does not mean the linked knowledge is verified or readable; do not copy source content. |
| Task link | Optional reference to an internal task | **Optional per task.** Resolve through the Continuum Task API (not Jira sync); verify Project/Team scope and current access. A deleted/stale link remains unavailable and cannot authorize resolution. |
| Owner / assignee | Human accountability and routing | **Action baseline accepted by authorized disposition in Jira #10255.** Assignee remains optional. Creator may edit unresolved summary; assignee may update progress; appropriately scoped leaders may assign/reassign; assignee or scoped leader may resolve. Exact eligible assignee constraints remain to be decided. |
| Status | Track lifecycle | **Accepted by authorized disposition in Jira #10255.** Use user-driven `OPEN → IN_PROGRESS → RESOLVED`; no automatic resolution, `IGNORED`, or reopen behavior in MVP. |
| Resolution | Record explicit human outcome | **D-07 decided in R0.6.** Successful resolution uses outcome `RESOLVED` and requires a short note, human resolver, timestamp, and `evidenceReferences[]`. At least one valid reference is required unless the note explains why none exists. Do not add `WONT_FIX` or `DUPLICATE` without explicit acceptance. Automated resolution is excluded. |
| Retention/deletion | Limit how long business and audit data remain | **Proposal recorded; policy is not yet approved.** The supplied package recommends minimum data while active, deletion/anonymization after an approved trigger or valid deletion request, backup lifecycle alignment, and valid legal/security holds. No 90/365-day period or full deletion trigger is approved. |
| Audit / timestamps | Support accountability and change history | **Audit proposal only.** The supplied package recommends actor/action/time/object/outcome, safe reference/correlation identifiers, internal denial code, and avoiding summaries, credentials, tokens, or sensitive payloads in logs. DATN-422/audit owner must confirm fields, events, atomicity, and retention before runtime implementation. |

Existing schema names/enums are noted above but are not approved by J-01. R0.6 defines logical resolution payload fields; DATN-444 owns their storage/API mapping. This document does not prescribe a concrete schema migration, API path, error code, or index change.

## 6. Lifecycle decision matrix

This matrix states the operations the contract must cover. Jira #10255 accepts the lifecycle-state and action baseline; R0.6 closes D-07 and records the remaining retention and API-convention gates in §9.3.

| Operation | Minimum behavior to define | Open contract decision |
|---|---|---|
| Create | Persist only after explicit user submission for both no-answer and missing/overdue reports; bind Project and required fields; validate each supplied reference | This creation baseline is authorized in #10255. A nonexistent, inaccessible, or cross-scope reference is not valid evidence and never grants access. Reject/omit behavior and exact validation code follow the verified API convention; no protected target metadata may be returned. |
| List | Return only gaps visible to the caller in current Project/Team scope | Project-member and same-Team visibility are accepted by authorized disposition. Exact explicit-grant behavior must follow confirmed API/IAM implementation. |
| Detail | Return only fields and references allowed by resource/source ACL | Reauthorize each reference on every read/use. The supplied package proposes that a stale/unreadable reference not block reading an otherwise readable parent, and that owner-API uncertainty fail closed for sensitive dependent actions; no source content may be disclosed. |
| Update | Permit only selected mutable fields and authorized actors | Creator summary edit while unresolved, assignee progress update, and scoped-leader assignment are accepted; exact immutable fields remain to be specified. |
| Assign | Route to an eligible in-scope human | Scoped-leader assignment is accepted; exact eligible assignee types, membership, reassignment, and audit behavior need decision or technical confirmation. |
| Resolve | Human-driven transition to `RESOLVED`; record actor and explicit outcome | Require outcome `RESOLVED`, a short note, resolver, timestamp, and evidence-reference list. At least one valid reference is required unless the note explains why none exists. S2 authorizes the proposed resolver grant. |
| Reopen or withdraw | Not required by the acceptance criteria as written | Decide whether supported in MVP. Until decided, do not invent a transition or imply automatic reopen behavior. |

## 7. Authorization and reference safety matrix

The accepted authorization baseline is active membership, explicit scope, resource/source ACL, and deny precedence. Jira #10255 accepts Project-member visibility, same-Team visibility for Team-scoped gaps, and the proposed action grants. The task owner confirms KeyT is formally delegated overall decision authority across Product, Security, and API/Architecture, so no separate role approval is required. R0.6 prohibits protected metadata disclosure and requires current owner-API authorization; exact HTTP response codes remain tied to verified API convention. A `TEAM_LEADER` acts only in explicitly assigned Project/Team scope. Organization `ADMIN` and `PLATFORM_OPERATOR` receive no default confidential-content access. `SME`, `KNOWLEDGE_OWNER`, and `SUCCESSOR` are scoped assignments, not persistent roles.

| Action | Known guardrail | Decision required before implementation |
|---|---|---|
| Create/report | Persist only after explicit user submission for both no-answer and missing/overdue reports; bind to an authenticated actor and authorized Project/source context | This creation baseline is authorized in #10255. Validate references through the owning API. A reference that cannot be validated is not evidence; do not copy protected source content, and return no protected metadata to an unauthorized caller. Persist only the approved opaque reference fields and use existing validation/error conventions. |
| List/detail | Apply current membership, scope, and ACL; references cannot widen visibility | Project-member and same-Team visibility are accepted. Reauthorize each linked reference on every read/use. A readable gap can remain readable when a reference is stale/unavailable; never return source content the caller cannot access. |
| Update | Do not let an actor change Project/Team or source references to escape scope | Grants are accepted: creator edits unresolved summary, assignee updates progress, scoped leader assigns/reassigns. Exact mutable fields remain unspecified. |
| Assign | Target an eligible human in the gap's approved scope | Scoped-leader assignment is accepted; exact eligible assignee types, membership, reassignment, and audit behavior need decision or technical confirmation. Task assignment rules do not automatically transfer to gaps. |
| Resolve | Resolution is an explicit human action; preserve the human actor and outcome | D-07 requires successful outcome `RESOLVED`, a short note, resolver, timestamp, and evidence-reference list; an empty list requires a note explaining why no reference exists. S2 authorizes the proposed resolver grant. |
| Link evidence/knowledge/task | Validate through the owning API, require same authorized Project and applicable Team scope, reauthorize on every read/use, and do not copy protected content | The supplied package proposes that missing/stale/inaccessible/cross-scope refs never count as verified evidence, owner API outage fail closed for sensitive actions, and stale refs use `UNAVAILABLE` only if the receiving API supports it. |
| Cross-scope attempt | Deny; do not reveal protected object contents or use a link as a grant | Never disclose target content or protected metadata. Use `404` where the verified API convention conceals existence; use `403` only where safe acknowledgement is supported. Exact convention is a technical confirmation gate, not an invented status code. |

## 8. Authorization and behavior scenarios to specify

These are contract scenarios, not evidence that runtime tests have been run.

| ID | Scenario | Expected invariant |
|---|---|---|
| G-01 | Authorized member reports insufficient evidence from an in-scope assistant session | No answer is fabricated; the report action is available; any created record follows the approved confirmation rule and contains only permitted context. |
| G-02 | An authorized actor follows up on a missing required-knowledge item | The source requirement and Project scope are validated; a persistent gap is created only after explicit human submission; no score is required. |
| G-03 | An overdue requirement is reported | The configured source requirement/review date and its existing overdue rule are used; a persistent gap is created only after explicit human submission; no new freshness/conflict score is calculated. |
| G-04 | Actor creates a gap with an authorized evidence, knowledge, or internal task link in the same scope | Owning API validates the reference; every later read/use rechecks current ACL; ID possession does not grant access. |
| G-05 | Actor supplies a reference from another Project or Team | Deny without target content or protected metadata; use existing API convention for safe 403/404 behavior. |
| G-06 | Actor links a missing, stale, inaccessible, or owner-API-unavailable reference | Accepted invariant: do not copy or disclose protected source content. The supplied package proposes that these references cannot count as verified evidence or authorize sensitive actions, and that a readable parent may remain readable with `UNAVAILABLE` if supported. |
| G-07 | Organization Admin or Platform Operator lacks a separate Project membership/authorization | No default gap content access is granted. |
| G-08 | Team Leader acts outside the assigned Team/Project scope | Mutation and read are denied; sibling Team scope is not inferred. |
| G-09 | Unauthorized actor attempts list, detail, update, assignment, or resolution | Each action is independently checked; no action permission is inferred from another action or a role title. |
| G-10 | Authorized human resolves a gap | Record outcome `RESOLVED`, a short note, resolver and timestamp. Include at least one valid evidence/reference, or require the note to explain why none exists. Resolution alone does not silently verify knowledge or launch SAG research. |
| G-11 | Repeated assistant report or repeated missing-knowledge signal | Do not fuzzy-merge human submissions. Automatic retries require a stable idempotency key and defined retry behavior; otherwise no automated retry is assumed. |
| G-12 | Membership, Team assignment, ACL, or linked-object access changes after the gap was created | Subsequent reads and mutations re-check current authorization; stored references do not preserve revoked access. |

## 9. Decision register and blockers

| ID | Decision needed | Owner domain | Blocks |
|---|---|---|---|
| D-01 | Does insufficient evidence only offer a report, create a draft, or persist a gap after explicit user confirmation? Which assistant context can be retained? | KeyT (delegated overall decision authority) | Explicit user submission and minimal context are accepted in #10255. Retention lifetime remains in D-11. |
| D-02 | What is the authoritative source and overdue rule for missing/overdue follow-up? | KeyT (delegated overall decision authority) | Explicit user submission is accepted; downstream owner must identify the configured requirement/review-date source and overdue rule. No auto-create. |
| D-03 | How do Project-level and Team-level visibility interact? | KeyT (delegated overall decision authority) | Project-member and same-Team visibility are accepted by #10255; no separate Security approval is required. |
| D-04 | Which reason and source values are canonical? | KeyT (delegated overall decision authority) | Accepted values: `INSUFFICIENT_EVIDENCE`, `REQUIRED_KNOWLEDGE_MISSING`, `REQUIRED_KNOWLEDGE_OVERDUE`; one source kind; no score-driven priority/automation. |
| D-05 | Which fields are required or optional, and which are immutable? | KeyT (delegated overall decision authority) | Required/optional field set is accepted in #10255. Exact transport names and mutable-field enforcement belong in downstream API/UI contracts. |
| D-06 | Which scoped actors may create, view, update, assign, and resolve? | KeyT (delegated overall decision authority) | S1/S2 are accepted in #10255. Runtime must enforce active membership, current scope/resource ACL, and per-action grants. |
| D-07 | What resolution outcome vocabulary applies, and are notes/evidence required? | KeyT (delegated overall decision authority) | **Closed in R0.6:** successful resolution uses outcome `RESOLVED`, required short note, resolver and timestamp, and evidence reference(s) unless the note explains why none exists. Do not include `WONT_FIX`/`DUPLICATE` without explicit acceptance. |
| D-08 | Which owning APIs validate references, and what are the denial/audit conventions? | KeyT decides policy; owning service/audit owners provide technical evidence | SAG independence is accepted. Owning APIs are authoritative; identify actual services, routes, current-ACL behavior, safe status codes, audit events, and atomicity. Do not invent endpoints or behavior. |
| D-09 | What response and field visibility rules apply to missing, stale, inaccessible, or cross-scope references? | KeyT (delegated overall decision authority) | Accepted invariants: deny unauthorized/cross-scope access, disclose no protected metadata, do not infer privilege from a reference, and reauthorize. Fail-closed/stale-reference details in the supplied package remain proposals. Concrete create/read result and 403/404 convention must match verified APIs. |
| D-10 | What duplicate/replay behavior applies when the same source signal is submitted again? | KeyT (delegated overall decision authority) | No fuzzy merge and stable idempotency key for automatic retries are accepted in #10255. |
| D-11 | How long are gap business data and audit records retained and deleted? | KeyT (delegated overall decision authority) | The supplied package's minimization/deletion lifecycle is recorded as a proposal, not approved policy. Numeric periods/triggers are **not decided**; 90 days for resolved gap metadata and 365 days for audit are proposal-only. |

Jira #10255 contains authorized acceptances and the D-07 amendment against an R0.4 discussion. On 2026-10-19 the task owner confirmed KeyT's delegated decision authority. The task owner subsequently supplied a D-07 decision package; R0.6 records its unambiguous requirements against the contract revision. Proposal-only values and technical conventions remain identified as such. Technical service/audit owners provide implementation facts, not separate policy approval.

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
| Read/update/resolve | Check current membership, explicit Project/Team scope, and source ACL on every operation. Let a reporter update their own unresolved summary; let the assignee update progress; let an authorized scoped leader manage assignment. Resolve through a human with an approved scope grant. | Historical review candidate only. Jira #10255 accepts the proposed action grants; remaining mutable-field details are tracked in §9.3. Resolving a gap must not itself verify knowledge. |
| Optional links | Store typed opaque references and validate them through each owning API; enforce same Project and applicable Team scope; reauthorize when read. Do not use direct cross-service foreign keys or copy linked content into the gap. | Keeps data ownership with Knowledge, Evidence, Task, or SAG owners and prevents references from expanding access. |
| Duplicates | Do not merge records by fuzzy reason/text matching. Require a stable source-event key before automating retries; human submissions may remain separate until a merge policy is approved. | Avoids hiding distinct questions and keeps automation idempotency explicit. |
| Unauthorized references | Return no protected metadata and use the shared API error contract; Security/API owners select whether the external response conceals existence. | Preserves a consistent contract and leaves 403/404 behavior to the owning Security/API decision. |
| SAG correlation | Keep a DATN gap ID independent. If needed, use a separate opaque SAG source reference confirmed by the SAG owner; do not persist a SAG score or make a direct FK into SAG storage. | Allows the human follow-up contract to proceed while broader SAG interface work continues. |

This historical proposal table does not request separate Product/Security approvals for decisions already accepted in #10255. The current authorized dispositions and open choices are in §9.3; technical owners provide factual API/audit constraints, not a separate policy approval.

### 9.3 R0.6 disposition and closure gates

The task owner confirmed KeyT's delegated authority over Product, Security, and API/Architecture decisions. Jira comment **#10255** supplies the accepted baseline. The task owner then supplied KeyT's D-07 disposition package in this task; this revision records its explicit requirements while retaining proposal-only values as open. The final revision SHA is recorded in Jira after this document commit is created.

| Area | Authorized disposition / R0.6 contract |
|---|---|
| Product P1/P2, D-04/D-05, D-10, G-01–G-12 | Accepted in #10255: explicit user submission for both trigger families, minimal editable summary and validated opaque references, accepted reason/field baseline, no fuzzy merge, stable idempotency key before automatic retries, and all 12 scenarios as downstream acceptance oracles. |
| Lifecycle P3 / D-07 | **Decided in the supplied KeyT package:** keep user-driven `OPEN → IN_PROGRESS → RESOLVED`; no auto-resolution, `IGNORED`, or reopen. Successful outcome is `RESOLVED`, meaning required knowledge has been supplied or verified. Every resolve records `resolutionOutcome`, `resolutionNote`, `resolvedBy`, `resolvedAt`, and `evidenceReferences[]`. Require a valid reference, or require the note to explain why no reference exists. Do not add `WONT_FIX` or `DUPLICATE` without explicit acceptance; no refusal outcome has been approved. |
| Security S1/S2/S3 | Accepted baseline in #10255: active membership and exact Project/Team scope; action-specific permission; no privilege inferred from role title, sibling Team, or linked reference. Reauthorize each read/write/reference use. Never return protected metadata on denial. |
| Retention and deletion | **Proposal only:** minimize data, keep only required active business data, define deletion/anonymization triggers, minimize reporter data, separate audit data, align backup lifecycle, and honor valid holds. Exact business/audit schedules, reporter departure/erasure, Project/Team deletion, and operating ownership remain open. Suggested 90 days after resolution and 365 days after an audit event are **unapproved proposals**, not OWASP or internal policy. |
| References / S3 / G-05 / G-06 | Accepted invariants: owning API is authoritative; use current authorization and do not disclose protected metadata or grant access through a reference. The supplied package proposes detailed stale/unavailable and fail-closed behavior. Exact reject-versus-omit on create, omit-versus-fail on parent read, and HTTP status mapping must be confirmed against owning-API conventions; `404` is a concealment option and `403` only where safe acknowledgement is supported. `400`/`422`/`503` are not hard-coded. |
| API/audit and SAG boundary | D-08 SAG independence is accepted: no assumed endpoint, foreign key, or automatic SAG trigger. Audit fields, content exclusions, and event names from the supplied package are **proposals** pending DATN-422/audit-owner confirmation. Owning services must confirm validation/ACL, status/error conventions, event names, atomicity, and retention. |

#### D-07 resolution record

For the MVP's only approved successful outcome, `RESOLVED` means the required knowledge has been supplied or verified by an authorized human. A resolve operation records all of:

- `resolutionOutcome = RESOLVED`
- a concise `resolutionNote`
- `resolvedBy` and `resolvedAt`
- `evidenceReferences[]`, containing at least one valid reference unless `resolutionNote` explains why no reference is available

Do not copy source evidence into the note. Owning APIs validate each typed reference and reauthorize it on every later read/use. `WONT_FIX` and `DUPLICATE` are not MVP outcomes. If a later decision introduces any non-`RESOLVED` outcome, it must define `decisionReason` and actor requirements before runtime implementation; no such outcome is approved here.

#### Retention and deletion baseline

Apply data minimization separately to business records and audit records:

| Data | Accepted baseline or supplied proposal | Still unselected |
|---|---|---|
| Summary, reason/source metadata, resolution note, reporter identity | **Accepted:** P2 limits stored context to an editable short summary and permitted metadata/references; no protected prompt/answer/evidence copy. **Proposed:** keep minimum business data while active and delete/anonymize under a defined trigger. | Retention period/trigger, reporter departure/erasure, Project/Team deletion, and operational owner. |
| Typed evidence/reference | **Accepted:** retain opaque validated references; never copy source content or infer access from a reference. **Proposed:** store only type/ID plus any minimal status needed. | Whether a status is stored and how/when it is refreshed. |
| Audit | **Proposed:** separate audit purpose; record actor/action/time/object/outcome and safe reference/correlation identifiers; avoid summaries, credentials, tokens, and sensitive payloads; retain a deletion event without deleted content. | Fields, event names, atomicity, retention period, and audit operator; suggested 365 days is proposal-only. |
| Backups/restores | **Proposed:** align backup/restore lifecycle with approved deletion policy and honor valid legal/security holds. | Backup purge interval and restoration-time deletion reconciliation. |

The suggested 90 days after resolution for business metadata and 365 days after an audit event are not approved values and are not sourced from OWASP. The non-numeric lifecycle recommendations above are also proposals, not adopted policy. Until KeyT selects/cites a governing policy, the exact period remains `RETENTION_PERIOD_PENDING_POLICY_OWNER`.

#### Reference behavior and API convention boundary

| Condition | Accepted invariant or proposed handling | HTTP or transport choice |
|---|---|---|
| Malformed reference or missing required request field | Validate untrusted inputs; exact reject/omit handling for an optional reference is a downstream API choice. | Use existing API validation convention; `400`/`422` are not preselected. |
| Reference does not exist at create/update | **Accepted invariant:** it cannot be treated as valid evidence or grant access. The supplied package proposes rejecting it as evidence and not resolving on it. | Reject whole request vs omit invalid optional reference remains open; `422` is proposal-only. |
| Previously valid reference is now deleted/stale | The supplied package proposes keeping the gap, marking the reference unavailable, and requiring replacement or an explanatory resolution note before relying on it. | `UNAVAILABLE` response is conditional on API support; response code/shape follows existing convention. |
| Caller cannot read the referenced object | **Accepted invariant:** no protected source content/metadata is returned and reference knowledge grants no gap access. | Conceal with `404` or acknowledge with `403` only per verified API convention and safe-disclosure rule. |
| Cross-scope reference | **Accepted invariant:** deny with no target title, content, metadata, or actual scope. | `404` is a recommended default, not an approved system-wide convention. |
| Owning API unavailable or times out | The supplied package proposes failing closed for sensitive actions that depend on an unverified result. | `503` is proposal-only when the owning API is required to finish safely. |
| Parent gap readable but a link is stale/unreadable | The supplied package proposes that a reference failure not revoke access to a separately readable gap, and source content remains hidden. | Return an `UNAVAILABLE` marker only if the receiving API contract supports it; otherwise use its established behavior. Conceal an inaccessible parent under its own authorization rule. |

The accepted invariant is that owning APIs are authoritative, current authorization is rechecked, references do not widen access, and protected metadata is not disclosed. The additional stale/unavailable behavior in the supplied package is still proposed. Exact reject-versus-omit create behavior, omit-versus-fail parent-read behavior, and status codes must follow verified API conventions; do not invent an endpoint or error contract. The proposed audit event names `REFERENCE_VALIDATION_FAILED`, `ACCESS_DENIED`, `GAP_RESOLVED`, and `GAP_DELETED` remain subject to DATN-422/audit-owner confirmation.

#### Remaining explicit gates

1. **Retention periods and operational deletion:** KeyT must choose or cite the applicable approved schedule for gap business data and audit records, including trigger, reporter metadata treatment, Project/Team deletion, valid erasure, legal/security holds, backup purge/restore, and the operating owner. The proposed 90/365-day periods are not approved.
2. **Owning API facts:** the downstream API owners must identify which reference kinds are actually supported and confirm their validation/current-ACL behavior and error/status conventions. DATN-444/448/451 must not invent a SAG endpoint or assume a SAG foreign key.
3. **Runtime audit contract:** DATN-422/audit owner must confirm event names, atomicity, internal denial codes, and audit retention. The supplied event list is a proposal until confirmed.
4. **Revision traceability:** the R0.6 D-07 disposition and remaining gates are recorded in Jira comment #10260 and PR #47's current description against the pushed contract head. No separate Product/Security policy approver is required; only the explicitly open KeyT choices and technical facts remain.

These remaining implementation facts do not reopen the accepted SAG boundary or D-07. DATN-444/448/451 remain downstream; no runtime or schema behavior is changed by J-01.

## 10. Work completed and remaining gates

| Work item | Evidence completed | Remaining gate |
|---|---|---|
| DATN-413 scope/dependencies | Read full parent acceptance criteria, DATN-414/415, and linked DATN-444/448/451. DATN-63/64 are Done; DATN-444 (persistence/API), DATN-448 (UI), and DATN-451 (trigger integration) are downstream To Do items blocked by DATN-413. | No application code from those downstream tasks is included in J-01. |
| DATN-414 — separate SAG signals | Current SAG schema, quality/question services, research task model/planner, API router registry, principal assertion, current `main`, PR 28, and open PR list were inspected. The matrix now distinguishes internal SAG signals from the DATN human record and records that no SAG gap CRUD interface is published. | The owner must confirm any future event/API before a SAG reference is introduced. This does not block J-01. |
| DATN-415 — fields/ownership/resolution | Contract inventory, existing DATN backend scaffold, state candidates, actor/scope invariants, G-01–G-12, and D-01–D-11 disposition are recorded. Jira #10255 has KeyT's authorized baseline; the task owner's supplied D-07 decision is captured in R0.6. | Retention periods and operational delete/backup triggers remain open; API/audit owners must confirm actual technical conventions. |
| Runtime implementation survey | DATN-BE/FE current refs and relevant source were inspected. Backend has a gap schema/persistence index but no gap workflow; frontend has no gap UI. | Storage/API, UI, and assistant/coverage triggers belong to DATN-444/448/451, not J-01. No DB, BE, FE, SAG, or runtime behavior was changed. |
| Verification | The Document repository has no `package.json`, `Makefile`, or CI workflow defining lint/typecheck/unit/integration/E2E/build commands. Source searches were refreshed against current BE/FE `origin/main`. | G-scenarios are contract oracles, not executed J-01 application tests. Separate baseline checks and the latest-main BE E2E result are recorded in the Jira validation comment; they do not validate this documentation change. |

### Remaining decision-closure blockers

1. **KeyT:** the supplied disposition closes D-07. KeyT still needs to select or cite exact retention periods/triggers and operating ownership for business data, audit records, deletion, and backups. The 90/365-day figures remain proposals.
2. **Owning API/audit technical evidence:** identify supported reference owners and confirm validation, current-ACL, status/error, event/atomicity, and audit-retention conventions. This is factual implementation evidence, not separate Product/Security approval; DATN-422 remains To Do.
3. **J-01 disposition:** record the final revision-specific status after R0.6 review. Do not treat the PR merge itself as approval or mark DATN-413 Done while the expected approved-contract criterion remains unmet.

The contract evidence, accepted baseline, D-07, and SAG boundary are recorded. Full approval/readiness still has the explicit retention and API/audit gates listed above.

## 11. Current outcome

- **Contract evidence complete:** versioned contract, accepted-source map, SAG reuse boundary, DATN scaffold reconciliation, lifecycle matrix, authorization/reference matrix, 12 contract scenarios, and decision disposition register.
- **J-01 acceptance:** the versioned contract, source mapping, authorization/scenario matrices, SAG boundary evidence, and disposition register are present. KeyT's authority-backed #10255 decisions accept explicit user submission, minimal context, field/reason baseline, authorization baseline, and SAG independence. The supplied D-07 disposition is recorded in R0.6: `RESOLVED` requires a note, resolver, timestamp, and evidence reference unless the note explains the absence of a reference; `WONT_FIX` and `DUPLICATE` are not adopted. Retention periods and technical API/audit conventions remain open; the expected approved-and-fully-specified result is therefore not yet met.
- **SAG dependency:** DATN-63/64 and PR 28 are complete. Current SAG `main` has internal scored-gap/research persistence but no published gap CRUD API; broader unpushed team work cannot be ruled out. This does not block J-01, only future integration assumptions.
- **Implementation scope:** no DB, BE, FE, SAG, or runtime changes in J-01. Jira-linked J-02/J-03/J-04 own persistence/API, UI, and trigger integration. App baseline checks were run separately and are not DATN-413 implementation tests.
- **External state after R0.6 update:** DATN-413 and DATN-415 remain In Progress; DATN-414 is Done. PR #45 merged R0.4 at `95edc801a68da2d6a4c23efaaf83bbe7d3d42279`. PR #47 is open and Draft; GitHub reports no review submissions, inline review threads, or CI checks for its current head. Jira comment #10260 records the R0.6 D-07 disposition on DATN-413, and #10261 links the update from DATN-415. The required `code-review-and-quality` skill is unavailable in this environment, so the PR remains Draft. Retain both issues In Progress while the explicit retention/API/audit gates and required review are outstanding.
