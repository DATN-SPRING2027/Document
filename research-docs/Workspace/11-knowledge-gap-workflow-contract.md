# DATN-413 — Human Knowledge Gap and Follow-up Contract

## Document status

- Revision: **R0.7, updated 2026-10-19 (Asia/Bangkok)**
- State: **R0.7 records KeyT's new revision-specific dispositions: D-07 resolution requirements; reject malformed references, references missing required fields, and nonexistent references on create/update; return an authorized gap with stale references marked `UNAVAILABLE`; fail closed when an owning API is unavailable for a dependent operation; and the minimum audit fields/content exclusion. The proposed 90-day gap and 365-day audit retention periods and backup purge policy remain explicitly unapproved. DATN-422/audit owner still confirms the concrete event schema, atomicity/retry, and actual retention convention.**
- Jira: [DATN-413](https://trankimthang0207.atlassian.net/browse/DATN-413)
- Related subtasks: [DATN-414](https://trankimthang0207.atlassian.net/browse/DATN-414), [DATN-415](https://trankimthang0207.atlassian.net/browse/DATN-415)
- Evidence base: Document `origin/main` at merged PR #45 commit `95edc801a68da2d6a4c23efaaf83bbe7d3d42279`; task-linked Jira records; DATN-BE `origin/main` at `9e3227925d01532b6e26336a77b38895392112b5`; DATN-FE `origin/main` at `217a9da38ca8db5334aeab51f2dea854a02844b1`; and SAG `main` at `ab27c61e90fb24ea0e73ea935f68baee36ba9942`, checked 2026-10-18.
- Decision evidence: Jira comment #10255 records KeyT's accepted/amended baseline; the task owner confirmed KeyT's delegated authority over Product, Security, and API/Architecture. R0.7 records the task owner's latest KeyT disposition package against this exact revision. The package expressly labels 90/365-day retention and backup purge as proposals, and leaves DATN-422 technical details for the audit owner; they are not represented as approvals.
- Approval evidence: **The task owner confirmed KeyT's delegated overall-lead authority.** D-07, reference behavior, and audit minimum are recorded as accepted. No 90/365-day retention period, backup deletion schedule, concrete audit event schema, or atomicity/retry convention is inferred as approved.
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
| R0.7 | Record KeyT's follow-up disposition for reference validation/read behavior, fail-closed verification, and minimum audit fields; retain 90/365-day retention and backup purge as unapproved proposals; defer concrete audit schema/atomicity/retry to DATN-422. |

## Acceptance checklist (J-01)

| Jira criterion / completion evidence | Result | Evidence and limit |
|---|---|---|
| Gap fields, states, ownership, links, and actor/scope are explicit or recorded as decision blockers | **Met at contract level.** §§5–9.3 record the accepted lifecycle, D-07, reference behavior, and bounded retention/audit gates. | 90/365-day retention and backup purge remain proposals requiring policy approval; concrete audit schema/atomicity/retry is assigned to DATN-422. |
| Insufficient-evidence and required-knowledge follow-up can create a gap without inventing a score | **Met at contract level.** Jira #10255 accepts explicit user submission for both paths and minimal stored context. | Retention period is still pending; no automatic overdue creation or scoring is allowed. |
| Human resolution is explicit; advanced scoring/autonomous crawl is excluded | **Met at contract level.** Human-only `OPEN → IN_PROGRESS → RESOLVED` is authorized. `RESOLVED` requires a note, resolver, timestamp, and a valid reference unless the note explains why references are absent. | `WONT_FIX` and `DUPLICATE` are not in MVP absent explicit acceptance. |
| Task/evidence references use owning APIs and cannot widen access | **Met at contract level.** R0.7 requires rejection of malformed, required-field-missing, and nonexistent references on create/update; stale references are marked `UNAVAILABLE` on a readable gap; owning APIs reauthorize and references never grant access. | Runtime must follow each owning API's existing validation/error conventions and must fail closed when reference verification is required but unavailable. |
| Required completion evidence: versioned contract/state matrix, source-to-gap mapping, authorization/test scenario matrix | **Met in this package.** See §§3–4, 6–8. | Scenarios are acceptance oracles, not evidence of runtime test execution. J-01 does not implement J-02/J-03/J-04. |
| Expected result: approved human-owned workflow contract | **Partly met.** KeyT's authorized workflow, lifecycle, reference, and audit-minimum decisions are recorded in R0.7. | Retention periods and backup purge are explicitly proposals, not policy; obtain the policy disposition. DATN-422's concrete audit schema/atomicity/retry details are downstream technical confirmations. |

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
| `status` (`OPEN`, `IN_PROGRESS`, `RESOLVED`, `IGNORED`) | Existing required enum | Jira #10255 accepts human-driven `OPEN`/`IN_PROGRESS`/`RESOLVED` and excludes `IGNORED`, automatic resolution, and reopen in MVP. R0.7 requires outcome `RESOLVED`, a note, human resolver, timestamp, and reference list; `IGNORED` remains excluded. |
| `assignedToUserId` | One assignee field | Supports an assignment candidate, but not a separate owner/reporter. Assignee is optional under #10255; KeyT must decide exact eligible targets, self-assignment, and reassignment details. |
| `resolvedByKnowledgeObjectId`, `resolvedAt` | Resolution link/time | Does not identify the human resolver. R0.7 requires `resolutionOutcome`, `resolutionNote`, `resolvedBy`, `resolvedAt`, and a reference list; a human-readable note must explain an empty list. The S2 resolver grant is accepted. |
| timestamps/index | Mongoose timestamps; index by organization/project/status/severity | Existing persistence metadata only. Retention, audit event, and index changes belong in the approved DB/API design for DATN-444. |

The items below come from DATN-413's required scope. Rows distinguish accepted requirements from decisions that need KeyT's disposition; a missing runtime implementation is not itself a policy blocker. Jira #10255 adds authorized dispositions after R0.4; §9.3 is the current status and supersedes earlier open rows only where it explicitly records an acceptance or amendment.

| Concept | Contract need | Status / unresolved detail |
|---|---|---|
| Project scope | Every gap has one Project boundary | **Explicit in task and product model.** Project identity is required; current authorization is rechecked on each operation. Cross-Project references are denied. |
| Team scope | Enforce Team scope when a gap is Team-scoped | **Accepted by authorized disposition in Jira #10255.** Project gaps are visible to active Project members; Team gaps to active members of that Team unless an explicit scoped grant applies. No sibling-Team or role-title inference. |
| Reason | Explain why follow-up exists | **Accepted in Jira #10255.** Reasons are `INSUFFICIENT_EVIDENCE`, `REQUIRED_KNOWLEDGE_MISSING`, and `REQUIRED_KNOWLEDGE_OVERDUE`; severity does not drive MVP prioritization or automation. |
| Source/provenance | Identify what initiated the follow-up | **Accepted in Jira #10255.** Require a source kind; retain only validated opaque references. Assistant no-answer and explicit missing/overdue reports are supported; handover and SAG scored-gap links are not approved J-01 sources. |
| Description/context | Give a human enough context to act | **P2 accepted by authorized disposition.** Store an editable short summary, reason, source kind, reporter, and validated opaque references only. Do not copy protected prompts, answers, or evidence. Keep minimum business data while active; exact periods remain open in §9.3. |
| Evidence link | Optional reference to evidence | **Optional.** Owning API validates existence and current ACL; malformed/missing-required or nonexistent references are rejected on create/update. Reauthorize on every read/use; no inherited access. A stale reference is returned as `UNAVAILABLE` when the caller can read the gap; stale links are never proof of resolution. |
| Knowledge link | Optional reference to knowledge | **Optional per task.** Owning Knowledge API validates each reference and current ACL. Malformed/missing-required or nonexistent references are rejected on create/update. Presence does not mean linked knowledge is verified or readable; do not copy source content. |
| Task link | Optional reference to an internal task | **Optional per task.** Resolve through the Continuum Task API (not Jira sync); verify Project/Team scope and current access. Malformed/missing-required or nonexistent references are rejected on create/update; a stale link is marked `UNAVAILABLE` on a readable gap and cannot authorize resolution. |
| Owner / assignee | Human accountability and routing | **Action baseline accepted by authorized disposition in Jira #10255.** Assignee remains optional. Creator may edit unresolved summary; assignee may update progress; appropriately scoped leaders may assign/reassign; assignee or scoped leader may resolve. Runtime must verify the target is active and in the gap's authorized scope. |
| Status | Track lifecycle | **Accepted by authorized disposition in Jira #10255.** Use user-driven `OPEN → IN_PROGRESS → RESOLVED`; no automatic resolution, `IGNORED`, or reopen behavior in MVP. |
| Resolution | Record explicit human outcome | **D-07 confirmed in R0.7.** Successful resolution uses only outcome `RESOLVED` in MVP and requires a resolution note, human resolver, timestamp, and evidence/reference list. At least one valid reference is required unless the note explains why none exists. Automated resolution and additional outcomes are excluded. |
| Retention/deletion | Limit how long business and audit data remain | **Proposed, not approved policy:** 90 days after resolution for gap content/reporter metadata and 365 days for audit records, plus a deletion/purge policy for backups. An authorized policy owner must approve the periods and backup behavior before implementation treats them as policy. |
| Audit / timestamps | Support accountability and change history | **Minimum accepted in R0.7:** audit actor/action/time/object/outcome/correlation ID, without sensitive content. DATN-422/audit owner confirms the concrete event schema, atomicity/retry behavior, and actual retention convention. |

Existing schema names/enums are noted above but are not approved by J-01. R0.7 defines logical resolution payload fields; DATN-444 owns their storage/API mapping. This document does not prescribe a concrete schema migration, API path, error code, or index change.

## 6. Lifecycle decision matrix

This matrix states the operations the contract must cover. Jira #10255 accepts the lifecycle-state and action baseline; R0.7 closes D-07 and the reference decisions while retaining the unapproved retention proposal and DATN-422 audit implementation details in §9.3.

| Operation | Minimum behavior to define | Open contract decision |
|---|---|---|
| Create | Persist only after explicit user submission for both no-answer and missing/overdue reports; bind Project and required fields; validate each supplied reference | This creation baseline is authorized in #10255. Reject malformed references, missing required fields, and references that do not exist. A reference never grants access; do not return protected target metadata. Validation status/body follow the owning API's established convention. |
| List | Return only gaps visible to the caller in current Project/Team scope | Project-member and same-Team visibility are accepted by authorized disposition. Exact explicit-grant behavior must follow confirmed API/IAM implementation. |
| Detail | Return only fields and references allowed by resource/source ACL | Authorize the gap first. If the caller can read it but a reference is stale, return the gap and mark that reference `UNAVAILABLE`; do not disclose protected source content. Reauthorize each reference on every read/use. If an owning API is unavailable, fail closed for any operation that depends on its verification. |
| Update | Permit only selected mutable fields and authorized actors | Creator summary edit while unresolved, assignee progress update, and scoped-leader assignment are accepted. Project/Team scope and source identity cannot be changed to escape authorization; enforce field-level grants in the runtime API. |
| Assign | Route to an eligible in-scope human | Scoped-leader assignment is accepted; target must be active in the gap's authorized Project/Team scope and verified through the existing membership/IAM convention. |
| Resolve | Human-driven transition to `RESOLVED`; record actor and explicit outcome | Require outcome `RESOLVED`, a short note, resolver, timestamp, and evidence-reference list. At least one valid reference is required unless the note explains why none exists. S2 authorizes the proposed resolver grant. |
| Reopen or withdraw | Not supported in MVP | Keep the accepted lifecycle at `OPEN → IN_PROGRESS → RESOLVED`; do not add reopen, withdrawal, or another terminal state without a new authorized disposition. |

## 7. Authorization and reference safety matrix

The accepted authorization baseline is active membership, explicit scope, resource/source ACL, and deny precedence. Jira #10255 accepts Project-member visibility, same-Team visibility for Team-scoped gaps, and the proposed action grants. The task owner confirms KeyT is formally delegated overall decision authority across Product, Security, and API/Architecture, so no separate role approval is required. R0.7 prohibits protected metadata disclosure and requires current owner-API authorization; use 404 to conceal existence when needed and 403 only where the established convention permits safe acknowledgement. A `TEAM_LEADER` acts only in explicitly assigned Project/Team scope. Organization `ADMIN` and `PLATFORM_OPERATOR` receive no default confidential-content access. `SME`, `KNOWLEDGE_OWNER`, and `SUCCESSOR` are scoped assignments, not persistent roles.

| Action | Accepted contract rule | Implementation note |
|---|---|---|
| Create/report | Persist only after explicit user submission for both no-answer and missing/overdue reports; bind to an authenticated actor and authorized Project/source context | Reject malformed references, missing required fields, and references that do not exist. Validate through owning API; fail closed if it is unavailable for required verification. Use existing validation/error conventions and return no protected metadata. |
| List/detail | Apply current membership, scope, and ACL; references cannot widen visibility | Project-member and same-Team visibility are accepted. Reauthorize each linked reference on every read/use. If the gap is readable but a reference is stale, return the gap and mark the reference `UNAVAILABLE`; never return protected source content. |
| Update | Do not let an actor change Project/Team or source references to escape scope | Grants are accepted: creator edits unresolved summary, assignee updates progress, scoped leader assigns/reassigns. Enforce field-level grants; Project/Team/source identity remains fixed. |
| Assign | Target an eligible human in the gap's approved scope | Scoped-leader assignment is accepted; verify the target is an active member of the gap's authorized scope using existing membership/IAM conventions. Task assignment rules do not automatically transfer to gaps. |
| Resolve | Resolution is an explicit human action; preserve the human actor and outcome | D-07 requires successful outcome `RESOLVED`, a short note, resolver, timestamp, and evidence-reference list; an empty list requires a note explaining why no reference exists. S2 authorizes the proposed resolver grant. |
| Link evidence/knowledge/task | Validate through the owning API, require same authorized Project and applicable Team scope, reauthorize on every read/use, and do not copy protected content | Reject malformed or nonexistent references on create/update. A stale reference on an otherwise readable gap is marked `UNAVAILABLE`; it is not evidence and cannot authorize sensitive actions. An owning-API outage fails closed for dependent verification. |
| Cross-scope attempt | Deny; do not reveal protected object contents or use a link as a grant | Never disclose target content or protected metadata. Default to `404` when concealing existence is needed; use `403` only where the existing convention supports safe acknowledgement. No status code is invented beyond that rule. |

## 8. Authorization and behavior scenarios to specify

These are contract scenarios, not evidence that runtime tests have been run.

| ID | Scenario | Expected invariant |
|---|---|---|
| G-01 | Authorized member reports insufficient evidence from an in-scope assistant session | No answer is fabricated; the report action is available; any created record follows the approved confirmation rule and contains only permitted context. |
| G-02 | An authorized actor follows up on a missing required-knowledge item | The source requirement and Project scope are validated; a persistent gap is created only after explicit human submission; no score is required. |
| G-03 | An overdue requirement is reported | The configured source requirement/review date and its existing overdue rule are used; a persistent gap is created only after explicit human submission; no new freshness/conflict score is calculated. |
| G-04 | Actor creates a gap with an authorized evidence, knowledge, or internal task link in the same scope | Owning API validates the reference; every later read/use rechecks current ACL; ID possession does not grant access. |
| G-05 | Actor supplies a reference from another Project or Team | Deny without target content/protected metadata; use `404` when hiding existence is needed, otherwise use `403` only if existing convention safely acknowledges access denial. |
| G-06 | Actor links a missing, stale, inaccessible, or owner-API-unavailable reference | Reject malformed/nonexistent references on create/update. If an authorized caller reads a gap with a now-stale reference, return the gap and mark that reference `UNAVAILABLE`. Do not disclose protected source metadata; fail closed when verification depends on an unavailable owner API. |
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
| D-07 | What resolution outcome vocabulary applies, and are notes/evidence required? | KeyT (delegated overall decision authority) | **Closed in R0.7:** only `RESOLVED` outcome; require note, resolver, timestamp, and reference list; an empty list requires an explanatory note. No other outcome is in MVP. |
| D-08 | Which owning APIs validate references, and what are the denial/audit conventions? | KeyT decides policy; owning service/audit owners provide technical evidence | SAG independence and reference behavior are accepted. Runtime uses actual owning-API routes/conventions. DATN-422/audit owner confirms concrete event schema, atomicity/retry, and actual retention convention. Do not invent endpoints or events. |
| D-09 | What response and field visibility rules apply to missing, stale, inaccessible, or cross-scope references? | KeyT (delegated overall decision authority) | **Closed in R0.7:** reject malformed/missing-required and nonexistent references on create/update; return an otherwise readable gap with stale references marked `UNAVAILABLE`; fail closed when owning API is unavailable for dependent verification; use 404 when concealing existence is needed and 403 only if existing conventions support safe acknowledgement. No protected metadata. |
| D-10 | What duplicate/replay behavior applies when the same source signal is submitted again? | KeyT (delegated overall decision authority) | No fuzzy merge and stable idempotency key for automatic retries are accepted in #10255. |
| D-11 | How long are gap business data and audit records retained and deleted? | KeyT (delegated overall decision authority) | **Open:** 90 days after resolution for gap content/reporter metadata and 365 days for audit records are proposals only; backup deletion/purge policy is required. No period or purge rule is approved as current policy. |

Jira #10255 contains authorized acceptances and the D-07 amendment against an R0.4 discussion. On 2026-10-19 the task owner confirmed KeyT's delegated decision authority. R0.7 records KeyT's latest D-07, reference, and audit-minimum dispositions against this revision. Retention periods remain proposals, and DATN-422/audit-owner confirmations are technical facts, not separate policy approval.

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

### 9.3 R0.7 disposition and closure gates

The task owner confirmed KeyT's delegated authority over Product, Security, and API/Architecture decisions. Jira comment **#10255** supplies the earlier accepted baseline. The latest KeyT package is recorded here against R0.7; its proposal-only retention terms and audit-owner technical confirmations remain clearly separated from accepted contract decisions.

| Area | Authorized disposition / R0.7 contract |
|---|---|
| Product P1/P2, D-04/D-05, D-10, G-01–G-12 | Accepted in #10255: explicit user submission for both trigger families, minimal editable summary and validated opaque references, accepted reason/field baseline, no fuzzy merge, stable idempotency key before automatic retries, and all 12 scenarios as downstream acceptance oracles. |
| Lifecycle P3 / D-07 | **Accepted:** keep user-driven `OPEN → IN_PROGRESS → RESOLVED`; only outcome `RESOLVED` is used in MVP. Each resolution requires a note, human resolver, timestamp, and evidence/reference list. If there is no reference, the note must explain why. No auto-resolution, `IGNORED`, reopen, `WONT_FIX`, or `DUPLICATE`. |
| Security S1/S2/S3 | Accepted baseline in #10255: active membership and exact Project/Team scope; action-specific permission; no privilege inferred from role title, sibling Team, or linked reference. Reauthorize each read/write/reference use. Never return protected metadata on denial. |
| References / S3 / G-05 / G-06 | **Accepted in R0.7:** reject malformed references, missing required fields, and nonexistent references on create/update; if a gap is readable but a reference is stale, return the gap and mark that reference `UNAVAILABLE`; fail closed when an owning API does not respond for an operation dependent on verifying its reference. Use `404` by default for out-of-scope resources where existence must be concealed; use `403` only where existing conventions allow safe acknowledgement. Do not disclose protected metadata. |
| Retention and deletion | **Proposal only, not policy:** 90 days after resolution for gap content/reporter metadata; 365 days for audit records; define a deletion/purge policy for backups. These periods and backup behavior still require policy approval. |
| Audit | **Accepted minimum:** actor, action, time, object, outcome, correlation ID; no sensitive content in audit records. DATN-422/audit owner must confirm concrete event schema, atomicity/retry semantics, and actual retention convention. No event names or retention values are invented by J-01. |
| API / SAG boundary | D-08 remains accepted: no assumed SAG endpoint, foreign key, or automatic SAG trigger. Reference resolution uses each owning API; no unstable SAG integration is assumed. |

#### D-07 resolution record

The only MVP resolution outcome is `RESOLVED`, meaning required knowledge was supplied or verified by an authorized human. Every resolve records:

- `resolutionOutcome = RESOLVED`
- a concise `resolutionNote`
- `resolvedBy` and `resolvedAt`
- an `evidenceReferences[]` / reference list; if it is empty, `resolutionNote` must explain why no reference exists

Do not copy source evidence into the note. Owning APIs validate references and current authorization. Additional outcomes or autonomous resolution are outside this MVP contract.

#### Retention and deletion disposition

| Data | KeyT disposition | Still requires policy approval / owner confirmation |
|---|---|---|
| Gap content and reporter metadata | Propose 90 days after resolution. This is **not an approved or existing policy**. | Approve or change the period; define treatment of unresolved gaps and the operating owner. |
| Audit records | Propose 365 days. This is **not an approved or existing policy**. | Approve or change the period; DATN-422/audit owner confirms the actual retention convention. |
| Backups/restores | Establish a deletion/purge policy for backups. | Define purge timing, restore-time reconciliation, and valid hold behavior in the applicable policy. |

These proposals are not sourced from or represented as an existing OWASP/internal schedule. Until the authorized policy owner approves the periods and backup behavior, runtime work must not treat them as policy. Data minimization and no-sensitive-content requirements remain in force.

#### Reference behavior

| Condition | Accepted behavior | Response boundary |
|---|---|---|
| Malformed reference or missing required field (including a required field of a typed reference) | Reject the request. | Use existing owning-API validation convention; J-01 does not invent a status code or body. |
| Reference does not exist on create/update | Reject the request; do not silently omit it or accept it as evidence. | Use existing owning-API validation convention. |
| Reference becomes stale/deleted | If the caller is authorized to read the gap, return the gap and mark the reference `UNAVAILABLE`; do not expose stale source content. | The stale reference does not make an otherwise readable parent gap unreadable. |
| Out-of-scope or unreadable resource | Do not return protected metadata. | Default to `404` when concealing existence is required; use `403` only if established API convention permits safe acknowledgement. |
| Owning API unavailable | Fail closed for any operation that depends on the owning API to verify a reference. | Follow existing transport/error convention; no status code is selected here. |

The owning API remains authoritative; recheck current authorization, and never let a reference widen access. This decision does not create a SAG endpoint, direct foreign key, or correlation contract.

#### Remaining explicit gates

1. **Retention policy approval:** the 90-day gap-content/reporter-metadata period, 365-day audit period, and backup purge policy are proposals only. Record an approval/change and its policy owner before runtime treats them as policy.
2. **DATN-422 audit implementation facts:** audit owner confirms event schema, atomicity/retry semantics, and actual retention convention. The accepted audit minimum is actor/action/time/object/outcome/correlation ID with no sensitive content.
3. **Runtime ownership:** DATN-444/448/451 implement persistence/API, UI, and triggers; they must follow this contract, respect existing owning-API validation/error conventions, and must not infer an unconfirmed SAG interface.
4. **Revision traceability:** record R0.7's exact commit in Jira and PR after committing. No separate Product/Security approval is required for the items accepted by the delegated KeyT; retention remains open because KeyT explicitly supplied it as a proposal for approval.

The open retention and audit implementation details do not reopen D-07, reference behavior, or the accepted SAG boundary. J-01 makes no runtime or schema change.

## 10. Work completed and remaining gates

| Work item | Evidence completed | Remaining gate |
|---|---|---|
| DATN-413 scope/dependencies | Read full parent acceptance criteria, DATN-414/415, and linked DATN-444/448/451. DATN-63/64 are Done; DATN-444 (persistence/API), DATN-448 (UI), and DATN-451 (trigger integration) are downstream To Do items blocked by DATN-413. | No application code from those downstream tasks is included in J-01. |
| DATN-414 — separate SAG signals | Current SAG schema, quality/question services, research task model/planner, API router registry, principal assertion, current `main`, PR 28, and open PR list were inspected. The matrix now distinguishes internal SAG signals from the DATN human record and records that no SAG gap CRUD interface is published. | The owner must confirm any future event/API before a SAG reference is introduced. This does not block J-01. |
| DATN-415 — fields/ownership/resolution | Contract inventory, existing DATN backend scaffold, state candidates, actor/scope invariants, G-01–G-12, and D-01–D-11 disposition are recorded. Jira #10255 and the latest KeyT disposition captured in R0.7 provide authority-backed lifecycle, reference, and audit-minimum decisions. | Retention periods and backup purge remain proposal-only; DATN-422/audit owner confirms event schema, atomicity/retry, and actual retention convention. |
| Runtime implementation survey | DATN-BE/FE current refs and relevant source were inspected. Backend has a gap schema/persistence index but no gap workflow; frontend has no gap UI. | Storage/API, UI, and assistant/coverage triggers belong to DATN-444/448/451, not J-01. No DB, BE, FE, SAG, or runtime behavior was changed. |
| Verification | The Document repository has no `package.json`, `Makefile`, or CI workflow defining lint/typecheck/unit/integration/E2E/build commands. Source searches were refreshed against current BE/FE `origin/main`. | G-scenarios are contract oracles, not executed J-01 application tests. Separate baseline checks and the latest-main BE E2E result are recorded in the Jira validation comment; they do not validate this documentation change. |

### Remaining decision-closure blockers

1. **Retention policy disposition:** KeyT's proposed 90-day retention after resolution for gap content/reporter metadata, 365 days for audit records, and a backup deletion/purge policy are not approvals or existing policy. Record the policy owner’s approve/change decision before treating those values as policy.
2. **DATN-422 audit implementation facts:** the audit owner must confirm the concrete event schema, atomicity/retry behavior, and actual retention convention. This does not reopen the accepted minimum audit fields or D-07/reference decisions.
3. **Review gate:** PR #47 has no submitted review or inline feedback and remains Draft while the repository-required review skill is unavailable. No application CI/test suite exists in this Document repository.

The accepted baseline, D-07, reference behavior, minimum audit fields, and SAG boundary are recorded in R0.7. The remaining policy proposal and audit-owner facts are explicit; J-01 stays In Progress until its expected approved-contract criterion and the review gate are satisfied.

## 11. Current outcome

- **Contract evidence complete:** versioned contract, accepted-source map, SAG reuse boundary, DATN scaffold reconciliation, lifecycle matrix, authorization/reference matrix, 12 contract scenarios, and decision disposition register.
- **J-01 acceptance:** the versioned contract, source mapping, authorization/scenario matrices, SAG boundary evidence, and disposition register are present. KeyT's authority-backed #10255 and R0.7 dispositions accept explicit user submission, minimal context, field/reason baseline, authorization baseline, human `OPEN → IN_PROGRESS → RESOLVED`, required resolution note/resolver/time/reference list, exact reference handling, and minimum audit fields. Retention periods and backup purge remain proposals; DATN-422 owns concrete audit schema/atomicity/retry/retention confirmation. The expected approved-contract result remains pending the retention policy disposition.
- **SAG dependency:** DATN-63/64 and PR 28 are complete. Current SAG `main` has internal scored-gap/research persistence but no published gap CRUD API; broader unpushed team work cannot be ruled out. This does not block J-01, only future integration assumptions.
- **Implementation scope:** no DB, BE, FE, SAG, or runtime changes in J-01. Jira-linked J-02/J-03/J-04 own persistence/API, UI, and trigger integration. App baseline checks were run separately and are not DATN-413 implementation tests.
- **External state after R0.7 update:** DATN-413 and DATN-415 remain In Progress; DATN-414 is Done. PR #45 merged R0.4 at `95edc801a68da2d6a4c23efaaf83bbe7d3d42279`. PR #47 is open and Draft; its previous GitHub snapshot had no review submissions, inline review threads, or CI checks. R0.7 updates the disposition for resolution, references, retention proposal, and audit minimum; Jira comments will link the exact new commit. The repository-required `code-review-and-quality` skill is unavailable in this environment; earlier manual documentation review found no actionable issue, but that does not satisfy the repository review gate. Keep both issues In Progress while the retention disposition and required review gate are outstanding.
