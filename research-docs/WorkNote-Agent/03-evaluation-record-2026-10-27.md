# WorkNote Agent — xKiro evaluation record

Historical initial prompt milestone (v0.1/v0.2). Statements below about absent
runtime/unchanged FE describe that milestone. Current implementation and later
evaluation are recorded in [delivery 05](05-local-delivery-and-review.md) and
[evaluation 06](06-v03-evaluation.md).

Recorded 2026-10-27. Scope: prompt, pure validation/Apply helpers and a synthetic
evaluation harness. The full WorkNote feature is not implemented. No model has
passed semantic acceptance; independent human review remains required.

## Reproducible inputs and artifacts

BE branch `feat/DanhDEV-agent-worknote-be-api`, base `2325a8e`; DOC branch
`docs/DanhDEV-agent-worknote`, base `d9aa106`. FE remains unchanged on
`feat/DanhDEV-agent-worknote-fe-ui`, base `5e001b3`.

BE sources:

- `src/services/capture/application/work-note-agent/`: prompt, protected fragments,
  strict result parsing, exact snapshot binding and pure draft replacement.
- `src/services/capture/infrastructure/ai/work-note-xkiro.client.ts`: explicitly
  constructed xKiro client; no CaptureModule or Gateway registration.
- `scripts/work-note-agent/`: 120-case corpus, scorer and bounded opt-in runner.
- `docs/work-note-agent/prompts/`: archived v0.1 and v0.2 prompt templates.
- `docs/work-note-agent/evaluation-summary.json`: sanitized aggregate of all 14
  report-producing runs, including failed availability pilots. No prompts,
  credentials, real notes or response bodies are included in that aggregate.

Raw synthetic responses and test logs remain in ignored `.worknote-agent-evals/`.
Each aggregate entry names its local raw artifact and run ID. An unavailable
catalog ID is rejected before inference and therefore has no completion report.

Corpus `worknote-eval/2026-10-27.v1`: development 70, validation 25, holdout 25;
grammar 20, protected fragments 20, style 15, Task context 20, selection 15,
conversation 20, adversarial 10. All notes/Task metadata are synthetic.

Prompt `worknote-rewrite/2026-10-27.v0.2` was frozen before validation and holdout.
All final baseline and stability runs have these same SHA-256 values:

```text
promptTemplateHash f616de1b77da29c6280e57e4c61219c28dc227d7609644863dcc850cde2881d2
corpusHash         3c73a5fbf3ecba6aee89561f21fea6d25b5f81d9c81a0573679985188baca933
```

The earlier English-negative phrase oracle was corrected before the full v0.1
baseline to accept "haven't" / "have not" as well as "not". Historical pilot
reports predate hash recording; missing hashes are left unknown. No prompt was
changed after viewing holdout results.

## Frozen v0.2 baseline

One trial per case/model; concurrency 2, max output 2,048 tokens, total request
deadline 30 seconds; JSON mode requested; no explicit reasoning level, schema
repair call or model fallback. Independent trials have distinct opaque `user`
IDs; transport retries preserve identical bytes.

| Requested model | Split | JSON syntax | Strict boundary accepted | Automated rules passed | p50 / p95 latency |
| --- | --- | --- | --- | --- | --- |
| mistralai/ministral-14b | Development | 70/70 | 69/70 | 58/70 | 1,746 / 2,643 ms |
| mistralai/ministral-14b | Validation | 25/25 | 25/25 | 23/25 | 1,880 / 2,447 ms |
| mistralai/ministral-14b | Holdout | 25/25 | 23/25 | 17/25 | 1,603 / 2,804 ms |
| qwen/qwen3.7-flash:free | Development | 70/70 | 67/70 | 66/70 | 4,593 / 6,046 ms |
| qwen/qwen3.7-flash:free | Validation | 25/25 | 23/25 | 21/25 | 4,733 / 6,827 ms |
| qwen/qwen3.7-flash:free | Holdout | 25/25 | 23/25 | 20/25 | 4,493 / 5,121 ms |

Latency is successful-completion latency from the client. No provider errors
occurred in these six runs. Across 120 cases, automated passes were 98 for
Mistral and 107 for Qwen; this combined total includes development and is not an
independent generalization estimate. All six reports have list-price estimate
$0 for these catalog entries; this is not an invoice or future-price guarantee.
Requested/reported IDs do not independently verify the actual upstream route.

For comparison, v0.1 development scored Mistral 53/70 (boundary 57/70) and Qwen
60/70 (boundary 61/70). v0.2 improved the development result after adding clearer
required-field examples, source-language and uncertainty instructions. This
comparison does not establish that those changes individually caused improvement.

## Availability and stability observations

Haiku 4.5 and 5.5 each returned HTTP 403 on the first tested request. Their batches
stopped; the cause/entitlement was not independently established. MiniMax M2.7
completed 3/5 pilot requests, with 2 network/deadline failures and 2/3 completed
responses passing automated rules. Its known-completed-usage list-price estimate
was about $0.0031821; failed-request usage is unknown. `z-ai/glm-5.3` was absent
from the fetched catalog and was rejected before an inference request.

A targeted v0.2 Qwen stability check used five development cases, three fresh
trials each: grammar-002 2/3, protected-007 3/3, style-006 2/3, task-context-009
1/3, conversation-003 3/3. Total 11/15 automated passes, 13/15 strict-boundary
acceptance, 15/15 JSON syntax, no provider errors; p50/p95 4,921/6,151 ms.
This is an intentionally selected error/stability probe, not a representative
overall score or a new independent holdout.

## Failure interpretation

These are developer observations, not independent human acceptance:

- **Shape:** Qwen sometimes omitted required top-level `questions` and
  `uncertainties` despite valid JSON, including conversation-016/020 holdout.
  The parser rejects such output. JSON mode alone is insufficient.
- **Unsupported claim:** Mistral task-context-011 development inferred completed
  work from the Task despite contrary note content. Requirements/status cannot
  be treated as evidence of work performed.
- **Meaning/language:** Mistral protected-003 omitted unknown-cause wording;
  style-006/conversation-006 translated English and invented next steps;
  grammar-017 holdout translated an English source. Selection-015 lost explicit
  uncertainty about a decision. Prompt instructions do not guarantee fidelity.
- **Technical literal:** Both models changed `0.5%` to `0,5%` in protected-018
  holdout. The numeric value may be equivalent, but exact technical text was
  required. Existing protection does not cover every number or unfenced log.
- **Operation choice:** Some models returned ANSWER/no edit on an expected
  rewrite, or asked for clarification where the oracle expected a refusal to
  invent facts (task-context-018). Such failures do not necessarily mean a
  fabricated claim; inspect meaning before classifying severity.
- **Oracle limits:** A synonym such as "giữ nguyên" instead of "không đổi", or
  an unchecked Test checklist instead of literal "chưa", can trigger phrase
  failures despite acceptable meaning. Scores are transparent heuristics.

Current decision: keep both models as exploratory baselines. Qwen has the better
holdout automated score in this dataset, Mistral lower latency; neither is
selected as an accepted production WorkNote model. Do not silently fill missing
fields and count the result as first-pass schema success.

## Checks and remaining work

BE `npm run check` exited 0: lint/typecheck, reconciliation safety (15 tests),
dev-db-smoke safety (25 tests), unit (161 suites/1,518 tests passed;
14 suites/135 tests skipped), e2e (16 suites/168 tests passed;
2 suites/4 tests skipped), and Nest build. New focused tests: 19 passed in four
suites. Script sources were separately ESLint-checked because repository lint
targets src/test. Dry-run prepared all 120 cases without network access.
`git diff --check` passed. Proposed YAML parsed and local references resolved;
this was not full OpenAPI semantic validation.

No DB/schema/migration, runtime route, FE screen or SAG change was made; no commit,
push or merge was performed. PR/Jira steps remain pending. The repository requires
the `code-review-and-quality` skill for the final review gate; that skill was
not found in the available catalog, local skills or workspace search. The gate
is therefore unfulfilled; passing checks do not imply review-ready status.

Next iteration should separately evaluate strict structured-output support or one
bounded formatting-only repair (report first-pass and repaired results apart),
language/uncertainty and technical-literal guards, and a human meaning-preservation
rubric. These are proposed improvements, not delivered behavior. Any tuning after
this holdout inspection needs a fresh independent holdout before acceptance.

The user selected canonical-only retention, confirmation before original deletion,
and 24-hour abandoned draft/chat expiry; see the updated
[integration proposal](02-integration-contract.proposed.md). Concrete API/schema,
compatibility, authorization, confirmation and expiry mechanics still require
review under BE AGENTS and DOC AI_WORKFLOW before runtime integration.
