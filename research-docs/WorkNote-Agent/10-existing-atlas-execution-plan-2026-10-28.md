# Existing Atlas integration and Git delivery — execution plan

Owner DanhDEV. User authorized planning plus execution on2026-10-28 after the
six-step proposal, including existing Atlas preparation/backup/migration, real
application integration and separate Git commits/PRs. This supersedes the earlier
local-only action boundary for this execution scope, without authorizing any
merge, production deployment or SAG work. User will update Jira separately.
Existing unfinished Task branches are continued, not replaced. No unrelated edit
is discarded. Secrets and populated .env stay local and out of every commit.

## Ordered work and evidence

1. Refresh origins and defect-first self-review using the user-approved
   review-agent substitute. FE origin/main advanced to aa9e03c; preserve WorkNote
   edits, commit reviewed current work, merge origin/main into this feature branch
   and resolve translations without losing either feature. BE/DB base2325a8e,
   DOC based9aa106 unchanged. Run affected checks after updating.
2. Read-only Atlas inventory for the Capture collections only. Record counts,
   index readiness and bounded legacy candidates; never print text, identities,
   credentials or URI. Back up the affected Capture scope to a protected local
   artifact; prove restore on a newly created disposable local Mongo. Retain the
   backup and sanitized proof. No shared write before successful restore proof.
3. Review the exact migration plan against that inventory; prefer required
   indexes and preserve live records. Run idempotent, bounded migrations against
   the configured existing Capture database only; Report backfill remains optional
   and is not needed to use on-demand author Save. Re-inspect and prove repeatability.
4. Run normal BE/FE entrypoints locally against the existing configured Atlas
   connection and Redis. Enable only this workstation's WorkNote flags and select
   an explicitly documented xKiro pilot model. Preserve all unrelated .env values,
   the existing key and Mongo connection. Use real IAM login/Project authority;
   never redirect the synthetic fixture or fabricate a session for shared data.
5. Verify normal application Task Note, Document and Report flows with synthetic
   test text, real login and persistence after reopen. Confirm Save/Submit
   separation, history/restore, permission denial, AI failure with independent
   Save and24h cleanup configuration. If human sign-in is required, prepare the
   concrete running screen and request only that user action; continue independent
   Git/review work. Record actual versus fixture-backed coverage accurately.
6. Run relevant lint/typecheck/test/build and final self-review. Commit/push only
   intended files on separate DB/BE/FE/DOC branches; open PRs to main, attach them,
   do not merge or auto-merge. Update this execution record with hashes/results,
   backup location, migration impact, URLs and remaining human acceptance.

## Acceptance

- Normal editor uses existing continuum_capture persistence with real authorization.
- Preview3019 remains disposable; it is never used as an authenticated Atlas client.
- Current canonical content/history preserved; transient originals removed only
  after confirmation; abandoned drafts/chat expire after24h.
- xKiro outputs remain explicit proposals. Existing test results are not independent
  human semantic acceptance. SAG remains deferred, and Jira is user-owned.
- Database/schema, backend, frontend and documentation have separate review scopes.

Execution status: authenticated Task Note, Document and Report Save acceptance passed; final delivery is recorded below.

## Execution results — 2026-10-28

### Database preparation

- Verified a Capture-only archive by restoring it into an owned, loopback-only
  disposable MongoDB instance. All 10 original collection counts and BSON content
  hashes matched. Backup remains protected outside Git at
  E:/DATN/audit-output/agent-worknote-atlas-20261028/capture.archive.gz.
- Archive SHA-256:
  e3d387f9dc4ae3a6a5257e16aeaef45b545d576bd2ccf5d00712a54fe1cc11e0.
- Tested bounded legacy conversion on the disposable clone only, then restored
  the original archive again and proved indexes-only migration preserves content.
- Applied and replayed both shared wrappers on the existing configured Atlas
  continuum_capture database, without --backfill. All 10 pre-existing collection
  content hashes were unchanged immediately after migration. No bulk Task Note
  or Work Report conversion ran on Atlas. Further edits to executed migrations
  are prohibited; follow-up schema changes need new migration files.
- DB draft PR: https://github.com/DATN-SPRING2027/DATN-BE/pull/104;
  commits 37bcb01 and bd252c9, base2325a8e.

### Actual application acceptance

Normal FE localhost:3000 and legacy-monolith API localhost:3001 use real IAM,
Task authorization, existing Atlas configuration and Redis. Only workstation
flags were enabled; repository defaults remain off. The stale FE local API base
3002 was corrected to3001. The existing API key and Mongo URI were preserved;
populated configuration backups remain protected and uncommitted.

The user authenticated and identified BE-2 / Activity / Task notes / New note as
where notes are written. The actual browser acceptance used synthetic text with
an explicit QA title, never a progress assertion about the real task:

1. Grammar proposal through xKiro mistralai/ministral-14b; original content
   remained unchanged before Apply.
2. A missing implementation detail produced CLARIFICATION_REQUIRED and one
   precise question. This response had no answer options: the UI offered free
   text, unknown and skip. Synthetic author details were provided in response.
3. The next proposal incorporated the supplied answer, preserving both unknown
   timeout cause and the statement that network-loss behavior was untested.
4. Explicit Apply, confirmed canonical Save and page reload succeeded on Atlas.
   A plain edit created v2. Restore of v1 created a new canonical v3, retaining
   v1/v2 snapshots; no existing version was overwritten.
5. Browser-native window.confirm blocked automated interaction. Restore now uses
   the existing in-app alertdialog with focus containment and explicit confirm;
   cancellation causes no restore request. Regression test failed first and
   passed after the fix; normal browser cancellation and Restore both succeeded.
6. Read-only final DB proof: canonical version3, history[1,2,3], v3 body equalsv1,
   v2 retains its distinct marker, six original work_notes are BSON-identical,
   zero remaining QA drafts, canonical contains no chat/raw rewrite original,
   uncertainty retained, and expiry TTL index exists.

Three real xKiro calls in this acceptance phase are separate from the earlier
119-call follow-up evaluation/smoke budget. No prompt tuning used these outputs.
The QA note remains visibly labelled in the user's project; the existing Test
note was preserved. Private evidence, IDs and screenshots stay outside Git.
24h expiry is validated by configuration/index plus forced-expiry automated
coverage, not a 24-hour wall-clock observation. No actual provider outage or
second human account was fabricated; failure/denial coverage uses the explicit
HTTP fixtures and isolated real-Redis suites recorded in07.

### Verification and review

- BE npm run check: lint/typecheck/build passed;1563 unit pass/137 skipped,
  168 e2e pass/4 skipped.
- DB npm run check: lint/typecheck/build passed;1502 unit pass/135 skipped,
  168 e2e pass/4 skipped;10 migration/operator tests passed.
- FE merged current main aa9e03c without conflicts. Initial full check passed
  952 tests/140 files; final Restore regression check is recorded below after
  completion. Composer targeted suite:12/12 passed.
- User-approved review-agent substitute was used for defect-first self-review,
  not independent review. Final Restore diff had no qualifying findings.
- No dependencies added, no secrets committed, no merge or auto-merge performed.
- BE draft PR https://github.com/DATN-SPRING2027/DATN-BE/pull/105 (ac4c30a,
  base2325a8e). FE draft PR https://github.com/DATN-SPRING2027/DATN-FE/pull/99
  (initial320972c, main mergec6954e7, baseaa9e03c; Restore follow-up recorded below).

Independent human semantic acceptance remains NOT_ESTABLISHED. Review worksheets
are unanswered. SAG is deferred by the user. Jira is user-owned. Draft PRs still
need teammate review and the normal DB-first merge order.

### Prepared team notification — not sent

[DATABASE CHANGE]
Collection/Entity: WorkNote draft/operation/history, Project Document editor
history, Work Report freeform/history collections and indexes.
Change:24h transient draft expiry, immutable canonical version uniqueness,
revision/idempotency support, freeform editor fields. Capture backup/restore
verified; existing Atlas indexes applied/replayed without bulk backfill.
Impact: existing records preserved by migration; on-demand author Save uses the
new canonical schema. Rollback disables workstation feature flags; immutable
history and protected Capture archive are retained for recovery assessment.
DB PR: https://github.com/DATN-SPRING2027/DATN-BE/pull/104
BE PR: https://github.com/DATN-SPRING2027/DATN-BE/pull/105
FE PR: https://github.com/DATN-SPRING2027/DATN-FE/pull/99
Jira: owner will supply. No merge requested or performed. No SAG rollout.

Final FE check:953 tests across140 files passed; lint/typecheck/build passed.
Restore follow-up commit55bf8b8 pushed to FE PR99. BE evidence follow-up634eb98
pushed to BE PR105. No remaining qualifying findings in the Restore self-review.

A new, explicitly labelled QA Project Document was saved without AI or review:
Draft status, editorVersion1, one immutable editor snapshot, content verified in
project_document_versions, all137 original Project Documents BSON-identical.
This proves independent Save uses the configured Atlas connection. No existing
approved Document was edited; no Report obligation was created by the Agent.

Actual Work Report acceptance also passed on the signed-in user's blank current
Leader obligation (2026-10-26 to2026-11-02). The Member tab correctly offered no
current writable obligation; switching to the existing Leader scope exposed the
user's own period. No cadence, assignment, role, period or obligation was created
or changed by the Agent. Ordinary Save wrote explicitly labelled synthetic QA
text as freeform schema2/version1, statusDRAFT, one immutable snapshot and no
submittedAt. Read-only proof matches the displayed period and the Task QA author;
zero remaining Report drafts. All46 reports in the original backup are unchanged.
The writable current obligation was generated by normal application scheduling
after the backup and was visibly blank before QA Save; it was not present in the
archive. Permission/failure/replay matrix coverage remains as recorded in07.

Browser hard-reload initially showed the SSR session shell while the in-app
browser was in the background. Making the page visible allowed normal hydration
and authenticated navigation; no authentication bypass or account change was
used. Both the checked production build and normal dev server were started as
local verification; final running entrypoints are recorded in the handoff.

Final source scan:112 changed text files, no configured-secret matches; both
OpenAPI JSON/YAML parse successfully; original brief SHA256 remains
07e138c00b38d93a234117154d4be6ccdccc80726aa476febb09fea9daffd332.

Final handoff source heads:DB2ae0b74 (base2325a8e), BE772267c
(base2325a8e), FE55bf8b8 (main baseaa9e03c), DOC branch
docs/DanhDEV-agent-worknote (based9aa106; commit/PR returned at handoff).
All source heads are pushed to their task branches. No main branch was modified.
Normal app remains running at localhost:3000 (checked Next production build)
and API localhost:3001 (legacy monolith), connected to existing Atlas/Redis.
The additional restore-proof Mongo clone is stopped only after all read-only
comparisons complete; protected archive/evidence remain available. The original
brief's Markdown hard-break whitespace is preserved byte-for-byte; diff whitespace
checks pass for all authored docs excluding that unchanged source attachment.
Final local review found no additional actionable defect; this is self-review,
not an independent approval. No merge, Jira update or team notification sent.
