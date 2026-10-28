# Agent WorkNote — local Task Note delivery and review

Date: 2026-10-27 (Asia/Bangkok). Scope: the user-approved Task Note pilot in
[contract 04](04-task-note-local-integration-contract.md). The user explicitly
authorized local integration before DB merge and using the installed
`review-agent` skill with permission to fix findings in this task. This is a
self-review record, not teammate approval, production sign-off or a merge.

## Implemented local flow

Open/resume private draft → title + freeform body → autosave → explicit Agent
request → direct answer, one clarification or proposal → preview/edit/regenerate/
dismiss → explicit Apply or Insert after → undo/redo → explicit canonical Save.
Save also works without AI. Applied rewrites require confirmation before their
before-rewrite original is discarded. Saved canonical history can be paged and
restored as a new version. Existing Task Note confirmation and edit authority
remain unchanged. Project Documents, Reports and SAG eligibility are unchanged.

Draft/chat expiry is 24 hours of author inactivity; reads and provider failures
do not refresh it. Queries reject expired drafts before asynchronous TTL cleanup.
Canonical text/version, audit and cleanup are transactional. Temporary payloads
are removed on Save/Discard; content-free closed-operation receipts retain only
scope, opaque operation/payload hashes, outcome IDs/version and expiry so a
retried old create cannot resurrect a closed draft. They contain no transcript,
replacement text, before-rewrite original, credential or reasoning content.

The backend resolves current Project/Task/Organization authority before provider
access and rechecks before accepting results/Apply/Save. Exact revision, source
snapshot and UTF-16 quote/range bind proposals. Task requirements/status do not
prove work was done. Quota-store failure fails closed for Agent requests while
ordinary Save remains independent. No browser model/system prompt/Task metadata
is accepted as authoritative input. Current Task fields are projected through the
existing authorization adapter; no acceptance-criteria field was invented.

## Branch and repository separation

| Package | Branch | Base | Owned change |
| --- | --- | --- | --- |
| DB | feat/DanhDEV-agent-worknote-db | BE origin/main 2325a8e | Capture schemas, collection/index inventory, new migration and migration tests. Worktree: E:/DATN/worktrees/agent-worknote-db. |
| BE | feat/DanhDEV-agent-worknote-be-api | origin/main 2325a8e | Prompt/boundary/client/evaluation, service/controller/Gateway/config, compatibility/search and tests. No DB schema/migration files copied into this branch. |
| FE | feat/DanhDEV-agent-worknote-fe-ui | origin/main 5e001b3 | Composer, chat/proposal/history, query/API integration, canonical rendering, English copy and tests. Current routing supports English only. |
| DOC | docs/DanhDEV-agent-worknote | origin/main d9aa106 | Brief, research, contracts, evaluation and delivery/review evidence. |

No commit, push, PR, Jira update, external message, deployment or merge has been
performed. No migration was executed on Atlas. Existing application database
configuration was not changed. The additive migration was tested on disposable
loopback MongoDB replica sets. The local preview uses its own temporary database;
it does not substitute a new local database for the user's configured application.

## Feature activation and reviewable preview

The application code is registered but defaults off:
`WORKNOTE_EDITOR_ENABLED=false`, `WORKNOTE_AGENT_ENABLED=false`,
`WORKNOTE_AGENT_FORMATTING_RECOVERY=false`; FE:
`NEXT_PUBLIC_WORKNOTE_EDITOR_ENABLED=false`. Runtime Agent additionally requires
the server-only xKiro credential and explicit model ID. Only the fixed HTTPS
xKiro endpoint is used. Storage checks require both exact expiry TTL indexes and
unique note/version indexing before enabling editor operations.

Local browser preview uses the real composer, controller, draft/Apply/Save service,
temporary MongoDB and real xKiro client, with a clearly synthetic fixture identity
and local quota fixture. It does not certify integration with live IAM/Atlas,
production Redis, deployment ingress or SAG. Fixture code is not imported by
application modules, refuses production and binds to loopback only.

BE (PowerShell):

```powershell
$env:WORKNOTE_AGENT_LOCAL_PREVIEW='true'
$env:WORKNOTE_AGENT_DB_PACKAGE='E:/DATN/worktrees/agent-worknote-db'
node -r ts-node/register scripts/work-note-agent/local-preview.ts
```

FE (separate terminal):

```powershell
$env:WORKNOTE_AGENT_LOCAL_PREVIEW='true'
node scripts/work-note-agent-preview.mjs
```

Open http://127.0.0.1:3019/. Generated preview files and screenshots are ignored;
they are excluded from application lint/type checking. The production component
and script sources remain checked. No dependency was installed.

## Review findings addressed

Read set: all new Task Note Agent sources, tests, DB schema/index/migration diff,
existing Capture permissions/Task projection, Work Notes compatibility/search,
Gateway forwarding, FE BFF/API, composer state/preview/chat/history and fixtures.

| Priority | Finding and fix | Evidence |
| --- | --- | --- |
| P1 | Deleting operation records after Save allowed replayed create to recreate a draft. Replace payloads with content-free closed receipts and reject old create replay. | Persisted workflow test first reproduced resurrection; replay regression now checks no draft is recreated. |
| P1 | Version-2 Mongoose records could omit canonical body/version after legacy requirements became conditional. Make canonical body/version conditionally required. | Schema test first failed and now validates missing-body and missing-version errors. |
| P2 | Nest returned an empty body for absent resume data, breaking FE JSON parsing. Explicitly serialize JSON null. | Browser reproduction; HTTP content-type/body regression. |
| P2 | A legacy note without timestamps needed exact source binding; a Manager edit must not rename its author. Store source hash and preserve original author identity/name fallback. | Legacy concurrency/author preservation test. |
| P2 | Server-side search omitted new canonical content. Include contentMarkdown without removing legacy search. | Existing Mongo workflow regression first failed to find canonical body. |
| P2 | Latest Agent answer metadata could replace provenance of an already applied proposal. Separate pending-suggestion metadata from applied provenance and retain exact source hash/revision. | Code read of message/Apply/Save path; source-bound Apply tests. |
| P2 | Cross-Project operation reuse could surface a duplicate-key error. Compare the scoped actor's operation payload before inserting. | Cross-Project reuse regression checks 409. |
| P2 | Deadline errors were indistinguishable from generic transport failure. Preserve a sanitized TIMEOUT classification and map to 504; quota-store failure maps to 503. | Client timeout and persisted workflow failure tests. |
| P2 | Browser textareas normalize CRLF to LF, so raw UTF-16 ranges could point at the wrong text and ordinary edits could alter technical line endings. Map DOM ranges to raw source and preserve untouched line endings when reconciling edits. | Three source helper tests and exact-selection component regression; used in both editor and edited proposal. |
| P2 | Identical autosaves could refresh abandoned draft retention. Keep revision/expiry unchanged for no-op content and align operation expiry with the draft. | Persisted no-op autosave/expiry regression. |
| P2 | Invalid or stale selection/context input could surface as a server failure. Validate anchors before quota/provider use and map bounded core validation to 422, stale anchors to 409. | Service validation/error regressions. |
| P2 | Generic Retry only persisted text after an Agent timeout. Retry the actual failed operation; discard the old retry action when editing clears the error, so a later autosave retry cannot send an old Agent request. Regenerate/retry clarification also opens chat. | Browser reproduction; two regression tests first failed, then passed. |
| P3 | A prompt example encouraged explanations about internal masking. v0.3.2 changes that example to “keep code unchanged” and directs summaries to describe content changes. | Browser-observed summary; archived prompt diff. This prompt change has no new independent holdout certification. |

Final scoped self-review found no remaining actionable defect in the reviewed
Task Note local diff after these fixes. This is not independent review or formal
team approval. Provider availability, semantic review and live deployment-system
integration remain the limitations listed below and in evaluation 06.

## Final verification

Full checks and the real-provider smoke use the final frozen application source:

| Package | Required full check | Result |
| --- | --- | --- |
| BE | npm run check | Pass: lint, type-check, safety checks, 165 unit suites / 1,549 tests, 16 e2e suites / 168 tests, build. 15 unit suites / 136 tests and 2 e2e suites / 4 tests skipped by their existing/opt-in gates. |
| FE | npm run check | Pass: lint, type-check, 132 test files / 922 tests, build. |
| DB | npm run check | Pass: lint, type-check, safety checks, 158 unit suites / 1,501 tests, 16 e2e suites / 168 tests, build. 14 unit suites / 135 tests and 2 e2e suites / 4 tests skipped. |
| DB migration | plan + disposable replica-set tests | Pass: 3 tests. No shared database access. |
| BE real xKiro HTTP | explicit work-note-agent.live | Pass: 1 test on final source (prompt v0.3.2); 9.144 s suite. Default checks skip paid/network inference. |
| DOC contract | YAML parse + recursive local-reference resolution | Pass: 8 paths, 11 operations, 47 local references; not a formal OpenAPI semantic validator. |

The copied brief matches original SHA-256
`07e138c00b38d93a234117154d4be6ccdccc80726aa476febb09fea9daffd332`.
Configured-key leak scanning across all modified/new nonignored files in the four
packages found zero occurrences. Logs and raw synthetic reports are ignored.
No `.env` credential or production source data is in the change set.

New/changed file groups: BE `src/services/capture/application/work-note-agent/`,
`infrastructure/ai/`, controller/Gateway/config/module/WorkNotes compatibility,
`scripts/work-note-agent/` and prompt/evaluation docs; FE
`src/components/work-notes/WorkNote{Composer,Proposal,AgentChat,History}*`,
`useWorkNoteComposer`, `textarea-source`, API client, existing TaskNotesPanel /
WorkNotesWorkspace / query types, English messages and fixture tooling; DB schema,
persistence index inventory, new migration/planner/tests; DOC this research folder.
Generated preview/evidence paths are ignored and excluded from application checks.

## Browser evidence

Observed on the disposable fixture: server-backed resume/create and autosave;
real xKiro grammar proposal with original editor unchanged; explicit Apply;
Undo/Redo; cancelling deletion confirmation; closing/reopening with draft intact;
dark mode; mobile 390×844; tablet 768×1024 without horizontal overflow;
confirmation focus wraps back to Keep editing; Confirm and save returns a visible
success state. Screenshots are under FE/.worknote-agent-preview-evidence/.
This was keyboard/DOM/visual inspection, not a physical screen-reader audit.

## Remaining delivery boundary

Prepare and review the DB/BE/FE PRs separately, then coordinate DB-first rollout
and feature flags. Shared migration, production activation and teammate merge
still need their own authorization/review. The user-approved exception covers
local integration, not these actions. Do not claim the entire original brief
complete: Document/Report composer integration and official knowledge retrieval,
citations/replacement/revoke require their own contracts and actual SAG evidence.
