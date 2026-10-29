# Prompt-quality follow-up — 2026-10-29

Authority: the user explicitly requested further testing and prompt improvement
after the implementation pilot closed. Scope is the existing unfinished WorkNote
assessment package on BE feat/DanhDEV-worknote-task-assessment-be-api and DOC
docs/DanhDEV-worknote-task-assessment. These remain draft PRs109 and67; no merge,
DB/migration, FE changes, real-user note transmission or shared activation.

A separate maximum29-call follow-up phase was disclosed before provider work.
The initial29 calls /73953 tokens remain recorded unchanged. This follow-up used
29 additional HTTP attempts /111387 reported tokens; combined observed work is58
calls /185340 tokens across the two separately authorized phases, not a reset of
the original phase. Unknown usage count0; monetary cost is NOT_ESTABLISHED.
No calls remain in the follow-up phase. No model fallback, validation/holdout or
full72 live run was performed. Model remained mistralai/ministral-14b throughout.

## What changed

- Task Interpreter and Assessor/Questioner remain one analysis call, now promptv9.
  Five validated user/assistant examples cover QA on vague Tasks, honest progress
  with known limitations, missing scope, incident symptoms and explicit completion
  evidence. A server-owned per-purpose policy travels in the actual request so
  progress/QA do not accidentally become whole-Task acceptance reviews. AUTO first
  infers purpose; it does not preselect progress or completion requirements.
- Targeted correction now includes the prior claim/gap text and source anchors.
  Sending an opaque target ID alone had not told the model what it misunderstood.
- Editor is a separate proposal-only promptv2. It receives the whole body as
  source.text; the old null wholeNote context field and unrelated triage examples
  are omitted for this path. The general grammar/selection/document/report path
  stays compatible. All language, uncertainty and protected-fragment guards remain.
- Application and evaluator share request construction, masked preparation,
  provider settings, formatting handling and proposal acceptance. Assessed Editor
  retries are0, ordinary standalone editing retains1 retry. Analysis/Editor have
 8192/4096 output caps,30s deadlines and temperature0.1. No speculative xKiro JSON
  Schema support was enabled.
- A missing question options list may be recovered as[] under the existing opt-in
  formatting flag. No question text, facts, status, source or criteria are repaired.
  Reports distinguish raw/structurally recovered outputs. Strict parsers remain.
- State progress recognizes a new grounded, explicitly targeted correction. Novel
  off-topic/vague replies remain insufficient and question/no-progress ceilings stay.
- Coverage can cite a shorter exact excerpt inside a fully grounded author statement.
  This fixes a false PARTIAL downgrade on permission/timezone answers. Source ID,
  exact passage and polarity are still checked; cannot/can't and related English
  negations cannot be dropped to claim a positive result. This is not general NLI.
- A locked persistent per-phase budget reserves before HTTP and survives repeated
  CLI runs/processes. Failure/unknown usage retains its reservation; corrupt/stale
  state fails closed. Never reset it or invent another phase for extra budget.
  Explicit case selection stays inside the selected batch/split. Corpus labels
  and family splits were not edited to inflate results.

The prompting work consulted [Mistral prompting guidance](https://docs.mistral.ai/inference/prompting)
for explicit structured examples. [Mistral JSON-mode limitations](https://docs.mistral.ai/resources/known-limitations)
distinguish valid JSON from adherence to a schema. These are vendor design
references, not evidence that xKiro exposes custom structured-output capabilities.

## Observed results — do not read as release approval

| Observation | Result / limitation |
|---|---|
| Initial v6/Editorv1 |4 calls; raw Editor asked for a missing note despite source.text being present; schema failures |
| v7 |3 calls; format accepted but unnecessary questions/incorrect gap classifications remained |
| v8/Editorv2 |4 calls; first runtime-accepted proposal; progress-purpose over-questioning remained |
| v9 targeted QA + progress |4 calls; both raw/runtime assessments and both proposals passed |
| v9 broader/multi-turn batch |11 calls; useful incident/scope questions and accepted proposals, but one extractive requirement failure, wrong gap kinds, repeated questions and conservative runtime downgrades |
| v9 correction retest after excerpt fix |3 calls; final grounded correction passed raw and runtime adequacy; middle repeated question was suppressed by runtime; Editor was denied locally before HTTP at exhausted budget |

Total follow-up:29 calls. Current v9 observations cover14 analysis attempts,
13 parsed outputs and13/13 agreement with authored allowed adequacy sets. The
remaining attempt failed strict requirement extraction. Full automatic rubric
passes are only7/14, because question/gap/source-related failures remain. This is
not macro-F1, not independent human labels, and not an overall100% accuracy claim.
The scenarios were selected/repeated development cases, not independent samples.

Editorv2 had5 actual responses accepted by runtime proposal/fidelity guards across
four distinct cases. This means proposals were technically safe to offer, not
that a person applied them or that Task completion was independently verified.
No automatic Apply/Save occurred. Raw model repetition remains a prompt/model
limitation even when code suppresses a repeated question.

Current release gate remains NOT_PASSED; reviewerSemanticAssessment remains
NOT_ESTABLISHED. Both assessment feature flags stay defaultfalse. A larger frozen
calibration, unseen validation/holdout review and possibly a separately budgeted
model comparison are still needed before a dependable release claim.

## Evidence and reproduction

BE/scripts/work-note-agent/assessment-prompt-quality-2026-10-29.json records every
trial's artifact SHA, versions, actual calls/tokens and per-run failures. Private
local synthetic reports, raw response evidence and blank reviewer worksheets are
under ignored BE/.worknote-agent-evals. The persistent follow-up budget is
prompt-quality-20261029.budget.json. Neither it nor transcripts are committed.

Final analysis template SHA256 (system plus all examples):
`6a7a5f172ffa51c5ee6efc58f3bb732af9533fb02b12e31ed65336a93fd6af8a`.
The excerpt-guard regression fix preceded the final three calls; earlier recorded
runtime grades were preserved rather than retroactively rewritten.

Checks: final BE npm run check results are appended below. Relevant regressions
were first reproduced failing and then fixed: shared custom Editor input,
missing original correction target, correction incorrectly counted as no progress,
null whole-note ambiguity, valid evidence excerpts and negation preservation.
Read-only defect review found no further introduced issue after those fixes;
this is not independent human semantic approval. No package was added.

DB/FE and their earlier tests remain unchanged. Save, auth/CSRF/CAS/lease,24h private
retention and no-external-action boundaries remain covered by the existing suite.
The old frozen reports and implementation ledger stay intact. Further provider
work needs a separate explicitly authorized budget; this document grants none.


Final verification: BE npm run check passed lint, typecheck, build,1696 unit tests
(137 skipped) and169 e2e tests (4 skipped). No database or frontend file changed.
The follow-up is implementation/testing complete within its bounded budget, not
release-quality approved. Backend and documentation commits are pushed to their
existing draft branches; no merge or external team/Jira message is performed.
