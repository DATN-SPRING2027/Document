# Document / Work Report editor extension — locally approved contract

Status: user approved this contract and local integration before DB merge on
2026-10-28 in this task. Implementation in progress; no independent team review,
Atlas execution or production activation is claimed.
Extends Task Note contract 04 without changing its existing paths. Explicit user
approval covers the concrete public API/database contract and local integration.

## Source ownership and API

Capture owns the operational records in continuum_capture. The browser continues
through existing BFF/Gateway/session/CSRF; credentials stay server-side. Proposed
new root: `/api/v1/capture/projects/{projectId}/editor-drafts`.

POST root accepts exactly one of:

1. `{operationId, workflow:"PROJECT_DOCUMENT", documentId}` for an existing
   authorized editable document; or `{operationId, workflow:"PROJECT_DOCUMENT",
   documentType}` for a new document. documentType uses the existing DocumentType
   enum, not a new AI taxonomy. No Task is required or fabricated.
2. `{operationId, workflow:"WORK_REPORT", reportId}`. reportId must identify an
   existing server-materialized obligation owned by the caller. Organization,
   Project, report scope, member, period and cadence come from the server record;
   the client/model cannot choose or change them.

IDs: existing resource/Project ObjectIds and draft/operation UUIDs. Reject unknown
keys, cross-scope resources and incompatible field combinations with contract 04
error conventions. Authorization includes ACTIVE Organization membership and
the existing per-workflow editable-state and author/reviewer separation rules.

GET root accepts exactly workflow plus resourceId to resume, except a new
Document uses workflow plus documentType. Returns the latest unexpired owned
draft or JSON null. GET/PATCH/DELETE root/{draftId}, reset-chat, agent/messages,
suggestions/{suggestionId}/apply and save retain contract 04 operation, revision,
selection, bounds, idempotency, 24-hour retention and explicit confirmation rules.
DELETE is confirmed discard only; Save does not Submit or Review.

Draft view: id, workflow, resourceId (nullable for new Document), baseVersion,
revision, title, contentMarkdown, expiresAt, conversation, pendingQuestion,
suggestion, hasAppliedRewrite and server context. Server context contains
projectId and documentType for Documents; projectId, reportScope, periodStart,
periodEnd and dueAt for Reports. It contains no hidden Task, member directory,
other notes, attachment text, credentials or reasoning traces.

PATCH accepts operationId, expectedRevision, title and contentMarkdown only.
Document type and report identity are immutable for this editor session; changing
document taxonomy remains an existing authorized metadata operation. The provider
gets only workflow-appropriate authorized metadata and current source/ledger.
Output keeps the strict existing five-key Agent result contract.

Save accepts operationId, expectedRevision, discardOriginalConfirmed. It returns
the existing Document/Report response plus explicitly additive canonical fields
where necessary. Recheck current resource version/hash and edit authority. Commit
canonical version, provenance, audit, operation receipt and transient cleanup in
one MongoDB transaction. Reuse workflow validation/state transition logic under
one session; do not call independently committing legacy writes from inside an
editor transaction. A retry creates no second version.

## Canonical storage and compatibility

- Project Documents: map the editor body to existing
  project_document_versions.content. Preserve file references, review history and
  document type. Add optional rewrite provenance to versions in a separate DB PR.
  Editing APPROVED/REJECTED content creates the existing new DRAFT version;
  pending/review constraints follow the existing service. Attachment binaries
  are never rewritten, replaced or sent to AI by the editor.
- Work Reports: introduce title, contentMarkdown, contentSchemaVersion=2,
  currentVersionNumber and provenance, plus work_report_versions with unique
  reportId/versionNumber. Save permitted only in existing DRAFT, OVERDUE or
  CHANGES_REQUESTED states and for the obligated author. The editor neither
  creates a new reporting obligation nor allows Manager editing as its owner.
  Existing MEMBER/LEADER review and cadence restrictions stay unchanged.
- Draft schema: explicitly extend the existing owned transient draft schema with
  workflow/resource identity. taskId is required only for TASK_NOTE; resource
  identity is exclusive per workflow. Existing drafts lacking workflow are
  interpreted as TASK_NOTE. Scope/TTL indexes remain explicit. Do not weaken
  Task Note validation to accept missing Task IDs.
- Operation storage keeps content-free closed receipts after Save/Discard.
  Replay never reopens a closed draft or bypasses current read authority.
- Legacy report backfill deterministically labels accomplishments/approach/reason/
  blockers/nextSteps; never asks a model to infer missing data. Preserve historical
  data and report identity. Old report mutations must reject upgraded freeform
  content instead of silently dropping it. Rollback is read-compatible and
  feature-disabled; there is no lossless automatic reverse mapping.

Canonical history APIs are workflow-scoped and paginated (page 1+, pageSize
1..50). Restore creates a new version only when the existing workflow allows
editing; it never changes an approved report or self-approves any resource.
Original-deletion confirmation applies to transient pre-rewrite content;
previous canonical versions remain history. Reuse contract 04 length limits,
private/no-store responses, safe errors, per-actor quota and bounded timeouts.

## Acceptance and deployment order

Tests must prove source ACL, unchanged review/cadence/file behavior, no implicit
Task context, canonical-only retention, idempotent Save/Submit separation and
legacy compatibility. DB schema/backfill/index PR is reviewed first; BE/FE follow
the accepted contract and shared rollout order. The user explicitly approved local integration before DB merge for this contract
on 2026-10-28; this does not authorize shared rollout or merge.
SAG eligibility continues to use current approval/replacement/revocation events;
this editor contract does not activate indexing or redefine approved source ACL.

## Concrete local implementation details

Machine-readable transcription: `shared-editor-v1.local.openapi.json`. This is
contract 08's local implementation record, not independent Product/team approval.

- GET `editor-drafts/sources/{workflow}/{resourceId}/versions` uses page/pageSize.
- POST `editor-drafts/sources/{workflow}/{resourceId}/restore` requires exactly
  operationId, expectedVersion, versionNumber and expectedContentHash (64 lowercase
  SHA-256 hex characters). Draft views expose baseContentHash. This guards edits
  made through the legacy Document form which do not advance editor history.
- PUT `editor-drafts/sources/WORK_REPORT/{resourceId}/document-links` accepts exactly
  documentIds (0..30 unique Project Document ObjectIds). Recheck author, editable
  report state and each linked Document's current scoped read authority. It changes
  links only; canonical body/version, obligation and Submit remain separate.
- Document title Save limit is 240 UTF-16 code units, matching the existing model;
  Report title limit is 300, body limit 30,000. Patch can retain temporarily empty
  fields. Save requires nonblank title/body. Existing file-only Documents can have
  an empty legacy baseline snapshot without becoming a fabricated text note.
- Documents keep existing review-version numbering. Add editorVersionNumber plus
  project_document_editor_versions for immutable editor snapshots. A legacy form
  edit since the last snapshot is captured as an intervening canonical baseline
  before the next editor Save. Old canonical content remains historical; only
  transient raw rewrite/chat is removed after confirmed Save.
- work_report_versions and project_document_editor_versions have unique
  resource/version indexes and no TTL. canonicalResult stores the existing scoped
  response DTO for exact Save replay, never chat/raw rewrite credentials. Current
  read authority and permissions are rechecked when returning a replay.
- Schema/index rollout is separate from optional legacy Report backfill.
  `20261028-work-note-editor.mjs --apply` creates indexes only by default;
  `--backfill` explicitly opts into deterministic Report conversion. Blank
  obligations stay legacy until an author writes content. Backfill retains legacy
  fields; subsequent canonical Save rejects legacy body writes and stores only
  freeform body. No reverse lossy conversion is provided.
- Both WORKNOTE_EDITOR_ENABLED and WORKNOTE_SHARED_EDITOR_ENABLED must be true;
  NEXT_PUBLIC_WORKNOTE_SHARED_EDITOR_ENABLED exposes FE entry points only after
  the corresponding backend/storage rollout. All defaults remain false.


Scope clarification from user, 2026-10-28: defer SAG integration until the SAG
team is ready. Current acceptance covers rewrite/clarification and persistence
in the existing application MongoDB Capture connection. It does not require
SAG ingest/search or a SAG repository link. Existing source lifecycle events
remain unchanged; downstream canonical-v2 ingestion compatibility is future
SAG work, not a prerequisite to local editor Save.

Later execution authority,2026-10-28: the user approved the existing-Atlas
preparation and normal-workstation integration plan, including backup/restore
proof and indexes-only migration. See execution record10 for actual results.
This extends the previous local-only boundary for this scope, without merge,
production rollout, SAG activation or bulk legacy backfill authorization.
