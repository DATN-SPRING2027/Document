# Task Note assessment v1 — concrete implementation contract

Date:2026-10-29, UTC+7. Owner: DanhDEV. Status: implementation authorized by the
user's latest instruction to implement plan v2 autonomously, including local
integration before DB merge and self-review fixes within scope. This records
implementation authority, not independent Product/Security/team approval or
semantic acceptance. No merge, production deployment or automatic external
communication is authorized by this record. The earlier plan-only state is
superseded for this implementation package.

Machine contract: [task-note-assessment-v1.openapi.json](task-note-assessment-v1.openapi.json).
Source implementation: BE work-note-assessment.types/protocol/service/controller,
FE composer and API client. This contract adds Task Note assessment only; existing
provider rewrite result retains its strict five-key object; the existing HTTP
AgentResponse also carries server-owned sourceRevision. The HTTP shape is unchanged. Project Document/Work Report
assessment, Project glossary/profile, selected additional sources and SAG are
deferred P1.1 work, not implicitly activated.

## Purpose and three independent axes

- Task clarity: CLEAR/PARTIAL/INSUFFICIENT based on the available requirement source.
- Note adequacy: ENOUGH_FOR_PURPOSE/NEEDS_AUTHOR_INPUT/UNDETERMINED/CONTRADICTORY.
- Claim support: FULL/PARTIAL/CONTRADICTED/RELATED_ONLY/INSUFFICIENT plus explicit
  AUTHOR_REPORTED or NOT_INDEPENDENTLY_VERIFIED status. No Task-completed field.

Purpose input: AUTO, PROGRESS, INCIDENT, DECISION, HANDOVER, COMPLETION, QA, OTHER.
AUTO lets analysis suggest purpose; an author can correct/reset it. A progress or
QA note may be adequate without proving the entire Task complete. Requirements
cannot be invented to fill an empty Task description/checklist. An author's
clarification does not silently edit the official Task requirement.

Three logical roles are Task Interpreter, Assessor/Questioner and Editor. The
default workflow combines the first two in one bounded analysis call; Editor is
a second call only on an explicit rewrite request with a usable fresh assessment.
Grammar/typo keeps its existing light path. Orchestrator is BE code, not an LLM
planner with action permissions. Three-call/critic variants remain evaluation
experiments; no majority vote establishes truth.

## HTTP envelope and operations

Prefix `/api/v1/capture/projects/{projectId}/work-note-drafts/{draftId}/agent/assessments`.
Reuse current session/bearer, active Organization/Project/Task checks, draft owner,
CSRF for cookie writes, private/no-store response cache, request IDs and structured
errors. Task/context/model/prompt/author identity supplied by a client are not
authority. Request bodies reject unknown keys.

All operations below return200 on success. Creation requires operationId UUID and
expectedRevision positive draft content revision. Optional purpose defaults toAUTO
when absent/null. Every existing-assessment
mutation additionally needs expectedAssessmentRevision positive. Draft/assessment
IDs are server owned; an in-flight provisional analyzing view may have revision0
on GET and cannot be mutated with expectedAssessmentRevision0.

| POST suffix | Additional input | Result |
|---|---|---|
| empty | purpose | AssessmentView |
| /{assessmentId}/replies | gapId, questionId, disposition, answer only when answered | Updated AssessmentView |
| /{assessmentId}/rewrite | none | Existing compatible AgentResponse/proposal; no Apply or Save |
| /{assessmentId}/corrections | targetClaimOrGapId, correctionText | Reassessed AssessmentView |
| /{assessmentId}/reset | newPurpose, carryAnswerIds | New assessment context; only explicitly selected answers carried |
| /{assessmentId}/validate-author | none | AssessmentView with author validation signal |
| /{assessmentId}/feedback | category | AssessmentView with transient feedback signal |

Answer/correction text limit2000 UTF-16 code units. carryAnswerIds is bounded20.
Reply disposition answered requires a nonblank answer; unknown/skipped contain no
answer and never count as resolved facts. Feedback category is one of
UNNECESSARY_QUESTION, MISSING_QUESTION, WRONG_SOURCE, FALSE_SUFFICIENT; keep the
last20 events, without treating a click as semantic acceptance.

Existing GET draft/resume exposes optional assessment; an old draft without it
still opens/saves. Only one question is active at a time; new assessment replies
do not ambiguously continue pendingQuestion from rewrite message v1. Ordinary
Save does not require assessment or provider availability.

## AssessmentView

Required fields are schemaVersion=task-note-assessment/v1, id, revision,
sourceRevision, taskContextHash, answerLedgerHash, purpose, state, contextManifest,
taskUnderstanding, claims, coverage, gaps, nextQuestion, taskContextStatus,
noteAdequacy, counters, allowedActions, answers, authorValidated,
reviewerSemanticAssessment, signals, createdAt, expiresAt, trace, promptVersion,
model. Optional feedback stores category/at events only.

- contextManifest: acquisitionStatus LOADED/INVALID/UNAVAILABLE/PARTIAL; sources
  have id, kind TASK/NOTE/ANSWER, label, text, version, loadStatus and
  includedInRequest; sourceCatalogVersion1. Manifest is backend created.
- taskUnderstanding: objective, scope, requirements with server IDs and references,
  and unknowns. Interpretation is not authority to invent acceptance criteria.
- claims: id/text/sourceRefs, TASK_REQUIREMENT or AUTHOR_REPORT origin,
  supportRelation and verificationStatus. Source requirements are not actual results.
- coverage: requirementId plus SUPPORTED/PARTIAL/NOT_REPORTED/CONTRADICTORY/UNKNOWN
  and sourceRefs. SUPPORTED is a claim-support assessment, not independent proof.
- gaps: id, kind SCOPE/IMPLEMENTATION/RESULT/EVIDENCE/CONTRADICTION/PURPOSE,
  target, BLOCKING/OPTIONAL impact, NOTE_AUTHOR/TASK_REQUIREMENT_OWNER owner,
  open/answered/unknown/skipped status and sourceRefs.
- nextQuestion: null or server id/gapId, text, reason and at most4 options.
- answers: server id/gapId, stable target, disposition, optional answer, purpose,
  taskContextHash. No implicit cross-purpose/cross-Task transfer.
- counters: questionCount and noProgress. Code owns bounded questioning, pause
  and available UI actions; the model cannot authorize new routes/tools.

State vocabulary: analyzing, waiting_for_answer, missing_context, contradiction,
ready_to_edit, stale, paused, error. Source retrieval errors stay technical errors;
they are not converted into authored Task requirements being absent. Context/output
budget overflow cannot produce a false conclusion of full Task coverage.

## Sources, support and conservative validation

The default catalog contains only the linked authorized Task title/description/
status/checklist, current note title/body and current private answers. Task detail
comes from Task API, not FE facts. A link in a note is an unverified supplied link;
the system does not fetch its destination or inspect code/PR/CI/SAG automatically.

Each source reference contains sourceId and an exact quote (max2000). The parser
requires the referenced source be loaded/included and the returned quote occur exactly. An unambiguous capitalization-only variation may be resolved back to the exact source passage; no word, punctuation or negation repair is allowed.
Requirements must be grounded in Task text except Task status. AUTHOR_REPORT
claims reference NOTE/ANSWER only; Task requirements cannot serve as proof a
result happened. FULL uses conservative extractive matching; non-exact full claims
are downgraded. Explicit polarity/uncertainty guards reject certain unsafe changes.

This is not a general entailment model or ALCE-level semantic guarantee. Exact
quote checks prove provenance, not that arbitrary reasoning or coverage is correct.
Groundedness, adequacy and question quality still require independent rubric
review. reviewerSemanticAssessment and signals.reviewerSemanticAssessment remain
NOT_ESTABLISHED; authorValidated, proposalApplied, saved and feedback are separate
usage signals, not independent confirmation.

Model-output bounds:50 requirements,40 claims,50 coverage entries,8 gaps,
8 references per item,12 unknowns,4 options of at most300 characters. Objective,
scope, claim/requirement text max2000; question text/reason max1000; gap target
max160. Serialized model payload max65000 characters; raw model output max100000
characters, with provider token/deadline limits enforced separately. No silent
criteria truncation is permitted.

## Freshness, question lifecycle and replay

Assessment is bound to draft content revision, current Task hash, purpose and
answer ledger hash. Task/note/answer/purpose changes make prior assessment stale;
Apply changes content and cannot leave a prior adequacy badge presented as current.
Every assessment mutation resolves current authorization and compares both revision
tokens. A question/reply must target the current open server gap/question. Unknown
or skipped gaps are not automatically asked again under paraphrased wording.
Correction targets an existing claim/gap and remains author input, not Task edits.
Reset carries no old answers unless selected IDs remain eligible under context.

Reuse existing draft inference lease, actor quota and operation receipts across
message/analysis/rewrite. Identical operation replay does not call the provider or
append a second answer. Changed payload under the same ID conflicts. Errors preserve
the editor and ordinary Save; an invalid/stale result is never silently applied.

## Retention, data ownership and migration

Only private `work_note_agent_drafts.state.assessment` is added. Its answers, gaps,
source text, feedback and metadata trace remain private to the draft owner. No new
canonical note/document/report/history field or SAG index is introduced. New fields
still belong to a separate DB review package.

The user-authorized v2 limit is an absolute maximum24h from original draft.createdAt,
not another24h after activity. BE caps and enforces reads/writes independently of
Mongo TTL. Save/Discard cleans assessment/source-bearing operations with draft/chat.
Content-free closed replay receipts also record independent saved/proposalApplied/authorValidated usage flags, never semantic acceptance. They have their separately bounded24h policy; they
contain no raw note/chat/assessment quotes. Historical04/08 inactivity statements
do not override this newly authorized private-state policy.

Trace is metadata only: phase, reasonCode, at, optional durationMs/promptTokens/
completionTokens/httpAttempts. Keep at most40 events, within private retention.
No hidden reasoning, full prompts, raw bodies or source quotes in telemetry/closed
receipts. Source-bearing developer traces are not retained beyond draft policy.

NEW DB migration20261029-work-note-assessment.mjs is bounded, expiry-only and local
guarded with offline default. It preserves canonical data, verifies existing exact
TTL indexes, clamps extended draft/assessment clocks and legacy receipts. Legacy raw
operations may lack createdAt: an associated draft provides an upper bound; orphan
operations with no trustworthy creation time expire at migration time. This policy
can shorten legacy replay availability but does not modify canonical text/history.
Invalid timestamps require manual inventory, not fabricated creation dates. No old
migration is edited. No Atlas execution is claimed by this contract.

## Verification and delivery record

New API/parser/source/state/permission/replay/retention tests, adversarial and
multi-turn corpus, UI tests and authenticated integration are recorded separately
as they finish. Passing structural tests does not establish human semantic quality.
Live inference has an explicit batch budget; no model fallback or speculative
provider JSON Schema support. xKiro JSON object mode plus local validation remains
the verified compatibility baseline. Assessment calls use the new
WORKNOTE_ASSESSMENT_ENABLED flag in addition to the existing editor gate;
AI-powered operations also require WORKNOTE_AGENT_ENABLED and server provider
configuration. Metadata-only author validation/feedback do not invoke the model.

DB/BE/FE/DOC have separate branches/PRs. Local-before-merge implementation was
explicitly authorized for this package; normal teammate review/merge order remains.
No auto-merge, production rollout, Jira/team message or SAG activation is implied.

Current package verification (2026-10-29): DB migration 3/3 disposable Mongo tests;
new and legacy schema 8/8 tests. The final frozen-source DB full check passed
lint, type-check and build, with 1512 unit tests passed / 135 skipped and
169 e2e tests passed / 4 skipped, including feedback/provisional storage guards.
OpenAPI JSON parses, all local references resolve, the legacy proposal reference
resolves, and15 positive/negative request/response fixtures passed structural AJV
validation. These are structural/data-safety checks, not semantic acceptance.
Runtime controller/validation synchronization includes7 POST routes, UUID question
and carry-answer IDs, unique carry IDs max20, feedback max20 and trace max40.
No migration was applied to Atlas or an existing application database by this
package agent. Root delivery owns final integration tests, commits/PRs and results.


Implementation review refinements: gap fingerprints include meaningful target entities
and grounded quote/source anchors, so separate authentication and billing tests do
not collide. No-progress uses conservative reply novelty/relevance and hash-only
coverage high-water trace metadata; regression/oscillation is not improvement.
This lexical guard is not semantic verification; short valid replies or synonyms
without common tokens can be conservatively treated as no progress. All author
choices, manual editing and Save remain available. Final inference completion
requires the same assessment ID/revision and a live lease, preventing delayed
results from overwriting concurrent feedback. Failed/expired inference can be reset.


Prompt-quality follow-up: see13-prompt-quality-follow-up-2026-10-29.md. No public
HTTP or storage contract changed. Internal model requests now carry a server-owned
purpose policy, validated conversation examples and the original targeted claim/gap
for corrections. Analysis can explicitly recover only a missing empty question
options array, behind the existing formatting-recovery flag; strict citation and
branch validation still runs afterward. Coverage quotes can be shorter excerpts
inside a fully grounded author statement, while dropping negation remains denied.

Release-gate repair details are recorded in14-release-gate-root-cause-fixes-2026-10-29.md.
Internal request extraction passages and the no-repeat ledger do not add HTTP or
storage fields. A literal no-new-information reply retains an unresolved gap and
cannot count as progress. Gap classification is not its identity. Source
contradiction is distinct from an actual result failing a desired Task criterion;
the latter alone does not block an otherwise adequate incident note from editing.
Only grounded new author corrections can resolve relevant author-owned gaps;
they cannot resolve official Task requirement-owner gaps or alter Task authority.
The new assessed Editor prompt/input/parser/guard are shared with evaluation;
ordinary standalone editing retains its existing behavior. No Apply/Save permission,
TTL, Organization boundary, external source or SAG behavior changed.
