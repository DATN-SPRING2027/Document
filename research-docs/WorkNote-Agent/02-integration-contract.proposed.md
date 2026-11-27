# Agent WorkNote — integration contract and data decisions (PROPOSED)

Historical first-milestone proposal. The user subsequently approved the concrete
local Task Note contract in [04](04-task-note-local-integration-contract.md).
Current implementation, explicit local exceptions and remaining rollout boundary
are recorded in [05](05-local-delivery-and-review.md). Approval is not attributed
to independent Product/Security/team reviewers. Statements below about unbuilt
prototype behavior describe that earlier milestone.

This is a review proposal, not approved OpenAPI, permission expansion, a migration
instruction or a claim that these endpoints exist. The prompt milestone adds no
HTTP routes. Review this document and the sibling proposed OpenAPI together.

## Pilot flow and authorization

The first application slice is Task Note. The future host resolves the actor from
the existing session, requires active Organization membership and current note
edit/create permission, resolves the Project and owning Task through their owning
APIs and verifies all IDs share that scope BEFORE any model call. Manager read
authority is not blanket rewrite authority. A Task Note edit/archive rule must
not be widened merely because an Agent endpoint is added.

The browser sends draft revision, operation, scope, instruction, a selection
quote/range and a full-note-context choice. It does not supply authoritative Task
metadata, permissions, arbitrary model IDs, system prompts or previous messages.
The server reconstructs history/answered/skipped questions from the scoped draft.
Descriptions/steps are source text, not system instructions. A model never chooses
the tenant, note, Task or selection anchor.

Create/load/update draft -> send Agent message -> ANSWER/CLARIFICATION_REQUIRED/
SUGGESTION_READY -> explicit Apply -> explicit canonical Save. The model never
performs Apply, Save, review, indexing, Task mutations or external tool calls.
Clarification UI opens after a user-initiated AI operation, not during typing or
autosave. A provider failure leaves draft and ordinary Save usable.

## Draft and suggestion semantics

- Revisions are server-generated monotonic integers. Expected revision is checked
  on draft update, message creation and Apply. Concurrent changes return 409.
- A request binds to exact title/body and revision. The response is stale if the
  draft changes while the model is running. Task-dependent rewrites also need an
  approved Task-context freshness policy before Apply.
- Selection offsets use UTF-16 code units, matching textarea selectionStart/end.
  Store quote and source snapshot/hash. Reject stale/ambiguous anchors; never find
  the nearest matching text or choose the first occurrence heuristically.
- Apply selection replaces only that range. Insert-after is a distinct explicit
  action in the proposed API; the current pure prototype supports replacement
  only. Scope expansion is a new user request. Title application is separately
  selected; a selection suggestion cannot change the title.
- Regenerate is a new operation with a new opaque ID, not an automatic retry of a
  completed response. Transport retries use the same operation identity/payload.
- Schema/JSON failures may get one explicit formatting-only repair in a future
  configuration, recorded separately from first-pass metrics. No repair is active
  in the delivered baseline. Semantic corruption is never silently repaired.
- A scoped stable operation ID/idempotency record must be defined for future
  draft/save/message POSTs. Provider replay is not business idempotency.
- The server controls model selection and token/context limits. No credential,
  reasoning content or system prompt enters FE responses. Errors are sanitized.

## Proposed persistence compatibility; requires a DB PR

This section proposes semantics only; it does not choose active collection names,
write a schema or execute migrations.

| Concern | Proposed behavior | Review still needed |
| --- | --- | --- |
| Freeform content | Add contentMarkdown and content schema version; retain structured legacy source values. | Exact schema/collection ownership and approved API revision. |
| Legacy backfill | Deterministic labeled concatenation of existing whatDone/howSolved/whyThisWay. Keep original fields; never use an LLM in migration. | Inventory, missing-field behavior, version backfill and rollback evidence. |
| Old clients | Continue legacy reads while protecting upgraded notes from lossy structured writes. Do not stuff freeform body into accomplishments and invent approach/reason. | Compatibility strategy and an explicit upgrade-required error for unsafe writes. |
| Raw input | User decision: keep only canonical after Save; explicitly confirm before deleting the before-rewrite original. | Exact revision-bound confirmation and atomic Save/cleanup contract. |
| Draft/chat | User decision: expire abandoned draft/chat after 24 hours of inactivity; delete chat on successful Save. Same ACL/deletion policy as owner note. | Activity definition, reset/delete semantics, enforcement and multi-device recovery. |
| Provenance | Applied-suggestion provider/model ID, prompt version/hash, source revision/hash, actor, time. No credential or chain-of-thought. | Exact metadata and audit policy. |
| Undo/restore | Editor undo changes draft; restoring a saved historical version creates a new version. | Task Note version semantics and contract changes. |
| Provider logs | Store diagnostic IDs/status/latency/usage, not raw real prompts/notes. | xKiro/upstream data-handling authorization before real content. |

Rollback must preserve newly written content. Disabling a feature is not permission
to drop fields/collections or downgrade freeform text to lossy legacy fields.
No historical migration may be edited. Migration approval, shared-DB execution,
application deployment and teammate PR merge are separate steps.

## User retention decisions recorded 2026-10-27

DanhDEV selected these exact policies in this task:

1. "Chỉ giữ canonical; xác nhận với người dùng trước khi xóa bản gốc".
2. Abandoned draft/chat expiry: "24 giờ" (24 hours without activity), in response
   to the proposal that chat is deleted on successful Save, otherwise with draft.

These resolve the product choices above; they do not approve an unreviewed schema,
new HTTP API or deletion of historical structured records. No deletion has run.

The proposed Save UI explains which before-rewrite original will be discarded and
asks for an explicit confirmation bound to the exact draft revision. Dismissing
or cancelling it performs neither destructive replacement nor original cleanup.
Apply alone is not this confirmation. Any subsequent edit invalidates it. A failed
Save retains recovery material until retry or the disclosed abandoned-draft expiry.
On successful Save, only canonical content enters note/version history; temporary
raw snapshots, conversation and unapplied suggestions are cleaned up. Historical
canonical versions remain governed by existing note history, not draft TTL.

For contract review, propose `expiresAt` in every draft response and refresh it on
successful author edits or explicit Agent conversation activity, not background
polling. Reads and Apply must reject expired drafts even before asynchronous TTL
cleanup runs. Canonical records must never share that expiry. The composer should
disclose the 24-hour abandoned-draft policy and expiry before the user relies on
recovery. These mechanics remain proposed until the concrete contract is reviewed.

## Canonical Save and other workflows

The existing Task Note API creates CONFIRMED records and retains its author/review
authority edit rules. A concrete freeform extension to the existing WorkNote
OpenAPI is required; the draft proposal does not invent a second confirmation
or approval workflow. Optimistic concurrency and save idempotency need review.

Project Documents keep their current freeform content/file versions and review.
Periodic Reports keep server-owned periods, cadence and review; a freeform body
must not silently remove existing required reporting semantics. Their integration
contracts follow after the Task Note pilot; shared UI does not mean shared records.

## SAG boundary

Task Note creation or rewrite does not make it official knowledge. Documents and
Reports retain source eligibility from their existing approval path. A downstream
consumer is not established by this package. Before SAG delivery, decide Task
Note eligibility, implement/verify idempotency by source/version, citations and
immediate access fencing on replacement/archive/revoke. Draft, chat, raw input,
unapplied/rejected suggestions and revoked content must not be indexed.

## Decisions required before runtime integration

1. Exact reviewed OpenAPI/freeform compatibility revision and Task-context fields.
2. Revision-bound deletion confirmation, expiry enforcement, conflict/deletion
   and quota mechanics. Raw-after-Save and 24-hour retention choices are recorded
   above and do not need to be asked again.
3. Model/account configuration and permission to send real content to gateway and
   upstream providers; synthetic evaluations do not grant this.
4. Task Note knowledge eligibility and the actual SAG consumer/revoke design.

No approval of these exact artifacts is inferred from permission to start the
overall plan. Backend AGENTS requires approved business contracts before wiring;
Document AI_WORKFLOW requires DB changes and migrations in a separate reviewed PR.
