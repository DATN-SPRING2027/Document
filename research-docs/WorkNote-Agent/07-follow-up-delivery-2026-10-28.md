> Historical local-phase record. Later user-authorized Atlas execution and Git delivery are recorded in [10-existing-atlas-execution-plan-2026-10-28.md](10-existing-atlas-execution-plan-2026-10-28.md). Earlier no-Atlas/uncommitted statements below describe that earlier phase.

# Agent WorkNote follow-up delivery — 2026-10-28

Authority: user requested implementation of the seven-step follow-up plan. This
continues the unfinished Agent WorkNote branches; it does not create a completed
replacement task, grant merge authority, run Atlas migration or activate shared
feature flags. Existing local-before-DB-merge and review-agent/fix permissions
remain applicable. All three origins were fetched; main remains at the recorded
BE 2325a8e, FE 5e001b3 and DOC d9aa106 bases. DB worktree remains separate.

## Scope implemented in this follow-up

- New 60-case v3 corpus with 30/10/20 splits and per-case accepted/prohibited
  behaviors. Existing corpora remain intact. Runtime prompt v0.3.2 is frozen;
  exact freeze hashes and bounded inference budget are in BE docs/work-note-agent.
- A synthetic human-review worksheet generator retains unanswered ratings and
  distinguishes provider failures/unattempted trials from semantic judgments.
  It cannot establish human acceptance automatically.
- Composer sources/scope disclosure reuses the existing approved Task detail API.
  It displays authorized Task title/description/status/checklist separately from
  author information, exact selected quote, and full-note context opt-in.
  It is a deterministic source preview, not an invented AI reasoning trace.
- Actual HTTP Gateway → Capture → authorization adapter → disposable MongoDB
  tests cover CSRF/session/scope denial, JSON-null resume, real Task projection,
  Apply, replay-safe Save and revoked session. IAM/Task HTTP responses and model
  are explicit fixtures; these tests do not certify a deployed IAM service.
- User started Docker. An owned loopback-only, disposable Redis 7.2 container
  is used for the opt-in transport suite, including real quota denial with
  independent ordinary Save. No shared Redis data is flushed.
- Review identified unbounded ioredis waiting when the quota store does not
  settle. WorkNote quota access now has a 1.5-second deadline and fails with 503
  before provider access. A pending Redis command can still consume a quota slot
  after reconnection; it cannot start late inference or mutate canonical content.
- Separate DB package adds a shared-Atlas operator wrapper with explicit host/DB,
  TLS and transaction checks, target confirmation and operator backup reference.
  Default dry-run makes no network call. The original loopback CLI is unchanged.
  No Atlas inspect/apply was executed and no backup was claimed verified.

## Evaluation status

The initial 30-case development batch completed 3 requests, all automatic passes,
then received three HTTP 500 failures and skipped 24 slots after its health gate.
A two-case follow-up completed/passed both. Resuming the remaining 25 development
cases completed/passed one, encountered HTTP 429 plus two HTTP 500 failures and
skipped 21. These are availability observations, not a model-quality pass rate.
Six outputs completed across 12 logical attempts; two failed cases were later
retried successfully. Six distinct cases have completed results; final aggregation
must retain both attempts and unique-case coverage. Qwen validation, holdout and
stability remain unattempted after provider availability failures.
The original 120-call budget is not a requirement to spend calls during failures.
No runtime model fallback or prompt tuning on held-out outputs occurred.

## Delivery boundaries

The user approved Document/Report contract 08 and local integration before DB merge
on 2026-10-28. The shared editor is now implemented in the separate BE/FE/DB scopes. SAG discovery
is recorded in 09; upstream is not assumed to be the deployed DATN fork.
Staging/Atlas application, shared feature activation, commit/push/PR and teammate
merge remain distinct actions. PRs/Jira/database notification are prepared only
after the applicable review and authorized Git delivery steps.

Final check counts, browser evidence and review findings are appended after the
frozen source gates complete. No independent review or production acceptance is
claimed by this record.

## Shared editor and current integration evidence

- Project Documents: freeform author editor with existing category, attachment,
  review states and immutable editor history alongside existing review versions.
- Work Reports: existing obligated author/period/cadence; freeform canonical text,
  metadata links/uploads preserved, legacy text writes rejected after upgrade,
  Save and Submit independent. No new obligation created by the Agent.
- Shared responses contain no Task identity; shared provider input forces task=null.
  Task routes reject shared drafts and shared routes reject Task drafts.
- Transaction tests cover stale Save/Restore, ownership denial, retained files,
  immutable baselines after legacy edits, original canonical Save replay, unchanged
  report text during link updates and legacy/freeform Submit compatibility.
- Isolated real AppModule smoke PASS: real IAM login + explicit organization
  selection, Workspace Task creation, autosave, real xKiro proposal, Apply,
  canonical Save/replay and independent Document Draft Save. This uses disposable
  Mongo and the owned loopback Redis container. Gateway is covered separately by
  the actual HTTP transport suite with explicit IAM/Task fixture replies.
- Full application smoke scaffolding applies current Workspace indexes only to its
  newly created disposable Mongo. It installs no new dependency and touches no
  configured Atlas URI. Default invocation makes no network call; production
  invocation is rejected. Temporary secrets/accounts are generated per run.

## Current model comparison (v3 / prompt v0.3.2)

Mistral ministral-14b was explicitly selected for comparison; runtime .env model
was not changed and there is no fallback switch. Development: 30/30 complete and
automatic pass; validation: 9/10 complete and automatic pass, one NETWORK_ERROR
on next-technical-004; holdout: 20/20 complete and automatic pass. Stability:
15 development cases across five categories repeated three times, 45/45 complete
and automatic pass. This is 104 completions /105 logical attempts, 59 unique
completed cases. Qwen's 6/12 completions remain separate. With one real AppModule
provider message and one browser Report grammar message, follow-up usage is 119 logical calls, within the 120-call budget.

Human semantic acceptance remains NOT_ESTABLISHED. In particular, grammar output
can propose title wording that needs review; passing automated checks does not
mean the proposed wording is appropriate. No prompt was tuned on held-out output.
Raw synthetic run reports and unanswered human review worksheets remain ignored
locally; sanitized aggregate is in BE docs/work-note-agent/evaluation-followup-2026-10-28.json.
The initial freeze hash used an unmatched serialization. It is retained unchanged
for audit; all actual v3 run records use the same runner template hash. This limits
byte-level pre-run freeze proof and is explicitly recorded in the aggregate.

## Review findings and fixes

Self-review with the user-approved review-agent substitution; not independent review.

- [P1, fixed] Shared autosave used the Task endpoint. A distinct shared-update
  regression failed before the fix, then passed; browser Document Save/reopen
  and canonical history were verified after correction.
- [P1, fixed] Quota access could wait indefinitely; bounded deadline now prevents
  late inference. Real Redis denial and normal Save are tested independently.
- [P2, fixed] Document DRAFT edits from the existing form could skip editor
  snapshots. Snapshot bridging preserves each intervening canonical baseline.
- [P2, fixed] String coercion allowed array document types; strict enum types and
  malformed HTTP coverage now reject them. Task/shared route boundaries are tested.
- Full checks exposed two existing fragile test paths: report-period count included
  another scope (now asserts MEMBER periods and join boundaries), and a WorkList
  toast timer survived unmount (now effect cleanup cancels it). Assertions are not
  suppressed. FE jsdom concurrency is bounded to two; async lookup timeout is 3s.

Review boundaries: synthetic fixtures do not certify deployed IAM/Gateway,
independent semantic review, actual SAG fork authorization, Atlas restore/backup,
or production readiness. Shared migration tools are prepared, never run on Atlas.

## Final verification and scoped handoff

User scope update 2026-10-28: keep persistence in the existing configured MongoDB
Capture database; DEFER SAG because its team is not ready. SAG repo discovery and
consumer integration are no longer completion gates for this editor delivery.
No application connection fallback/new database was introduced. The isolated
port3019 preview uses temporary Mongo and synthetic identity only; it is not
connected to the configured application/Atlas data or a real user session.

| Scope | Result |
| --- | --- |
| BE npm run check | PASS: lint (6 unsafe-supertest warnings), typecheck, safety25/reconciliation15, unit1563 passed/137 skipped, e2e168 passed/4 skipped, build |
| FE npm run check | PASS: lint/typecheck, 931 tests, build; no unhandled teardown error |
| DB npm run check | PASS: lint/typecheck, unit1502 passed/135 skipped, e2e168 passed/4 skipped, build |
| DB new migration/operator tests | 10/10 passed; actual disposable Mongo transactions, default no-network and unsafe-target rejection |
| Real Redis HTTP integration | 6/6 passed with explicit owned loopback Redis |
| App smoke safety | 2/2 passed; default no-network, production opt-in rejected |
| Real AppModule smoke | PASS on disposable Mongo/Redis with real IAM/Task/Capture/xKiro |
| Worksheet generator | 2/2 passed; all v3 sheets leave human ratings unanswered |
| Extra script lint | PASS for scripts/work-note-agent/*.ts |
| Shared OpenAPI | Parsed;9paths,49local references resolved, path parameters checked |
| Repository hygiene | diff --check clean,111 changed text files scanned, no actual xKiro key or merge markers found |

Skipped tests are existing opt-in suites; counts do not claim those tests ran.
One fixture-based suite uses the real Gateway transport; AppModule smoke uses the
monolith with real IAM. No independent review or deployed-environment acceptance.

Browser checks: Document Save/reopen + immutable history; Report grammar proposal
kept both “not tested” and unknown cause, explicit Apply/original-cleanup
confirmation, Save/reopen + v1/v2 history. Report mobile390px has document/dialog
width390px, no horizontal overflow; temporary viewport override reset. Evidence
is ignored locally under FE .worknote-agent-preview-evidence/: document-history-
20261028.jpg, report-history-20261028.jpg, report-mobile-20261028.jpg.

Branches/bases remain BE feat/DanhDEV-agent-worknote-be-api /2325a8e,
FE feat/DanhDEV-agent-worknote-fe-ui /5e001b3,
DB feat/DanhDEV-agent-worknote-db /2325a8e,
DOC docs/DanhDEV-agent-worknote /d9aa106. All changes are uncommitted/unpushed;
no PR, merge, Jira update or team notification sent. Separate DB review/PR and
rollout steps remain explicit Git/deployment actions, not an SAG dependency.

Changed source areas: BE work-note-agent draft/editor engine + controllers,
Gateway/config/WorkNotes compatibility, prompt/evaluation/smoke tooling;
FE WorkNote composer/chat/context/proposal/history/API plus existing Task,
Document and Report entry points and freeform read compatibility; DB Capture
schema/index inventory and new idempotent migration/operator scripts; DOC local
contracts, evaluation/review evidence, rollout runbook and deferred SAG record.
Canonical history has no TTL; draft/chat expires24h and is scrubbed after confirmed
Save. Atlas migrations/feature activation were not performed.

Configured target verified without logging credentials: Atlas SRV /continuum_capture.
Existing .env editor/Agent/shared flags are not enabled. Source persistence uses
that existing connection when normal runtime rollout is enabled. Local fixture
Save successes must not be described as writes to the user's Atlas database.
