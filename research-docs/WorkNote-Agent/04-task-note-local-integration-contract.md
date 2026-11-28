# Task Note Agent — concrete local integration package

Status: user-approved for local implementation/testing on 2026-10-27; not
independently reviewed or deployed. DanhDEV explicitly approved this contract,
local integration before DB PR merge, and using the installed review-agent skill
with permission to fix findings within this task. No approval by another owner
or authority is claimed. Extends
the draft OpenAPI proposal. Task Note pilot only; Documents/Reports and SAG keep
their current workflow and are not claimed complete by the pilot.

## Runtime contract

All operations use the existing Capture/BFF authentication and CSRF envelope.
Resolve current ACTIVE Organization membership, Project and Task server-side
before reading a draft or making a provider call. A private draft is accessible
only to its owner; existing note edit authority is checked again before Save.
Client Task context/history/model/system prompt are never accepted as authority.
All bodies reject unknown keys. JSON responses use private/no-store caching.

Prefix: `/api/v1/capture/projects/{projectId}/work-note-drafts`.
IDs: existing ObjectIds for Project/Task/note; UUID for draft/operation/suggestion.
Each mutation carries a stable operationId and expectedRevision where applicable.
Reusing an ID with a different payload returns 409; identical replay returns its
recorded result without another version or model call. No streaming in the pilot.

| Operation | Input | Result |
| --- | --- | --- |
| POST prefix | operationId, taskId, optional noteId | New private draft from empty content or current authorized canonical note; revision 1. |
| GET prefix?taskId=&noteId= | Scoped task and optional note to resume | Latest unexpired owned draft or null; no TTL refresh. |
| GET prefix/{draftId} | Path only | Current owned draft or 404. |
| PATCH prefix/{draftId} | operationId, expectedRevision, title, contentMarkdown | CAS autosave; actual changes increment revision and invalidate suggestions/confirmation. Identical content does not extend inactivity expiry. |
| POST prefix/{draftId}/agent/messages | operationId, expectedRevision, operation, scope, instruction, includeWholeNoteContext, optional selection and question reply | ANSWER, one clarification, or bound suggestion; no Apply/Save. |
| POST prefix/{draftId}/agent/suggestions/{suggestionId}/apply | operationId, expectedRevision, action, applyTitle | CAS draft update only. action: replace_body, replace_selection, insert_after, replace_title. |
| POST prefix/{draftId}/reset-chat | operationId, expectedRevision | Clear chat/questions/suggestions; retain current editor content. |
| DELETE prefix/{draftId} | expectedRevision, discardConfirmed=true | Explicitly discard owned draft; no canonical mutation. |
| POST prefix/{draftId}/save | operationId, expectedRevision, discardOriginalConfirmed | Atomic canonical Save/version + transient draft cleanup + content-free replay receipt. |
| GET /tasks/{taskId}/notes/{noteId}/versions | page 1+, pageSize 1..50 | Authorized canonical versions, newest first; no raw/chat/proposals. |
| POST /tasks/{taskId}/notes/{noteId}/restore | operationId, expectedVersion, versionNumber | Restore a canonical historical snapshot as a new canonical version; never overwrite history. |

Draft response: id, taskId, optional noteId, baseNoteVersion, revision, title,
contentMarkdown, expiresAt, conversation, pendingQuestion, suggestion,
hasAppliedRewrite. Conversation is capped at 20 turns; provider history at 8.
Title <=300 UTF-16 units, body <=30000, instruction/answer <=2000. Model IDs are
server configuration only. Selection is exact UTF-16 start/end/quote; title
operations cannot use selection. A reply references the current server question
ID and has answered+nonblank answer or skipped+no answer, never both.

Apply requires the stored source revision/hash/selection to match. Full-note
expansion requires a new request. Insert-after adds text at the stored selection
end; it never chooses a nearby occurrence. Edited suggestions must be edited in
the draft by the author, not sent to Apply as trusted provider output. Concurrent
editor changes while inference runs make the response stale (409); it cannot be
stored as applicable. Task context is resolved again on each message; if its hash
changes before Apply, regenerate a Task-dependent suggestion.

Save works without AI. If a rewrite was applied and the current body/title differs
from its before-rewrite source, require explicit original-deletion confirmation
bound to the expected draft revision. Cancelling does not Save or delete raw.
Use MongoDB transactions for canonical write/version, receipt and cleanup; a
failure leaves recovery material. Existing Task Note lifecycle remains CONFIRMED.
Saved canonical history is retained; raw input/chat/unapplied suggestions are not.

Abandoned draft expires 24 hours after successful author edit/conversation/Apply;
GET/polling and provider failures do not refresh it. Enforce expiry in queries,
independently of asynchronous MongoDB TTL cleanup. Canonical history has no TTL.
After Save, replay receipts contain only scope, actor, operation/payload hashes,
note ID and saved version; they expire after 24 hours and contain no note text.
No replay may bypass current access checks or reveal a now-inaccessible note.

Errors retain the existing `{code,message,details,requestId}` envelope: 401 no
session, 403 denied operation/CSRF, 404 absent/inaccessible/expired scoped resource,
409 stale revision/anchor/Task or operation reuse, 422 invalid input/confirmation
required, 429 quota, 502 invalid provider output, 503 disabled/unavailable, 504
deadline. No raw provider response or credential is exposed. Proposed limits:
one in-flight inference per owned draft, 20 message turns/draft, 10 inference
requests/minute/actor; a distributed runtime requires a shared quota lease.

## Persistence and compatibility package

Owner/database: Capture / continuum_capture. DB branch:
`feat/DanhDEV-agent-worknote-db`, starting from BE origin/main `2325a8e`.
Additive canonical fields: contentMarkdown, contentSchemaVersion=2,
currentVersionNumber, provenance (provider/model/prompt/source hash, actor/time).
Do not store credentials, full prompts or chain-of-thought. Legacy structured
fields remain readable; legacy writes cannot overwrite an upgraded freeform note
(409 NOTE_EDITOR_UPGRADE_REQUIRED). The upgraded client uses the draft Save API.

New owned draft collection stores revision-bound transient content/conversation,
pending question and server-owned suggestions, scope/actor and expiresAt. A
separate operation collection holds transient idempotency payloads and replaces
them with content-free closed receipts after Save/Discard, preventing stale create
replay from resurrecting a draft. Add owner/scope/resume indexes, exact expiresAt TTL indexes and
unique scoped operation keys. Canonical work_note_versions remains durable.

Migration: new idempotent script, dry-run default, explicit DB/target guard,
bounded scan. Convert old fields by deterministic labeled concatenation, never
LLM inference; preserve whitespace within each field. Backfill only records
missing a freeform schema version, preserving legacy source values. Seed an
initial canonical version if absent; reject conflicting existing versions rather
than overwriting them. On the first upgraded Save, preserve the prior canonical
version, then remove obsolete structured fields from the current record after
confirmation. Never remove historical canonical versions under draft retention.
Rollback disables the new UI/API without dropping new content, versions or
collections; downgrading freeform text into What/How/Why is not supported.

No shared Atlas migration, deployment, commit, push or merge is included in
local implementation/testing authorization. Database PR review/merge and final
runtime activation remain distinct from tests.
