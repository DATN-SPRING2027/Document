# WorkNote Agent — v0.3 evaluation and subsequent revisions

Recorded 2026-10-27. All inputs are authored synthetic data. Requested/reported
model IDs identify the gateway request, not independently verified upstream
routing. Automated checks do not establish semantic acceptance or replace human
review. See [local delivery](05-local-delivery-and-review.md) for runtime scope.

## Inputs and freeze boundary

The original 120-case corpus (70/25/25) and v0.1/v0.2 availability/quality trials
are historical evidence in [record 03](03-evaluation-record-2026-10-27.md).
The newer `scripts/work-note-agent/cases-v2.json` contains 42 separately authored
cases, split 21 development / 7 validation / 14 holdout. Seven categories cover
language/uncertainty, technical literals, Task fidelity, selection, necessary
clarification, skipped clarification and adversarial unsupported assertions.
These are developer-authored tests, not an independent benchmark.

The v0.3 standing prompt was frozen before running these validation/holdout
splits. It separates Task requirements from evidence of completed work, retains
source language and uncertainty, limits clarification to one necessary question,
tracks answered/skipped questions and requires exact output branches. Protected
technical fragments are masked/restored deterministically; there are no tools,
chain-of-thought outputs, automatic Apply/Save or model repair calls.

v0.3.1 retains that standing prompt text and fixes deterministic masking of signs
and embedded-digit identifiers such as `-0.5%`, `+1.25ms` and `p95Latency`.
That pipeline change happened after v0.3 holdout observations. The subsequent
v0.3.1 development rerun is not a new independent holdout; archived v0.3 scores
must not be presented as holdout certification of the current pipeline.

v0.3.2 subsequently changes one few-shot summary and the explanation policy after
browser review exposed a summary referring to internal masking. It asks for
natural explanations of content changes and uses “keep code unchanged” in the
example. No new independent holdout has been run for v0.3.2. Archived scores below
retain their exact original prompt versions and do not establish semantic
acceptance for this latest copy refinement.

Prompt snapshots v0.1/v0.2/v0.3/v0.3.1/v0.3.2 and exact prompt/corpus hashes are in BE
`docs/work-note-agent/`. The sanitized `evaluation-summary.json` records 21 runs,
including failed availability pilots, configurations and failure IDs. Ignored raw
synthetic artifacts are local only; the aggregate includes no full outputs,
prompts, credentials or real notes.

## Frozen v0.3 results on the new corpus

| Gateway model ID | Split | Planned/completed | First-pass automated | After explicit empty-array recovery |
| --- | --- | --- | --- | --- |
| qwen/qwen3.7-flash:free | Development | 21/21 | 20/21 | 21/21 |
| qwen/qwen3.7-flash:free | Validation | 7/7 | 7/7 | 7/7 |
| qwen/qwen3.7-flash:free | Holdout | 14/14 | 13/14 | 14/14 |
| mistralai/ministral-14b | Development | 21/21 | 19/21 | 19/21 |
| mistralai/ministral-14b | Validation | 7/7 | 6/7 | 6/7 |
| mistralai/ministral-14b | Holdout | 14/14 | 13/14 | 13/14 |

Qwen totals: 40/42 first-pass; 42/42 after two explicit deterministic recoveries.
The two responses omitted empty arrays (`fresh-task-002`, `fresh-selection-005`).
Recovery may add only missing empty questions/uncertainties/options arrays; it
cannot infer a status, change prose or repair invalid JSON. Strict branch and
protected-fragment checks run afterward. It is opt-in, separately counted and
default off in the registered runtime. CLI success still uses first-pass scores.

Mistral totals: 38/42. Three strict-output failures (`fresh-technical-003`,
`fresh-clarification-004`, `fresh-technical-005`) and one phrase-rule failure
(`fresh-selection-002`). A phrase-rule failure alone does not prove semantic
corruption. All 42 responses per model had valid JSON syntax; valid JSON alone
does not imply valid contract shape or preserved meaning.

Successful holdout latency p50/p95: Qwen 4,944/6,785 ms; Mistral 1,962/5,487 ms.
These are small observed samples through this account/gateway, not a universal
model ranking or availability guarantee. No provider errors occurred in these
six v0.3 split runs.

## v0.3.1 development stability and HTTP smoke

Four development cases × two independent trials planned eight calls. Six
completed and passed; two `fresh-technical-003` calls timed out at the 30-second
deadline. Overall planned pass is 6/8; completed-only pass is 6/6. No formatting
recovery was needed. Successful p50/p95 was 12,050/27,267 ms; attempted p95
30,020 ms. Usage for failed requests is unknown. This remains an availability
limitation; the free route is not production-accepted.

On final application source with prompt v0.3.2, the opt-in real-provider HTTP smoke
passed (one test, 9.144 s suite duration): create/autosave → real xKiro proposal
→ explicit Apply → Save without original-deletion confirmation rejected →
confirmed Save accepted → transient content absent. It uses disposable MongoDB,
synthetic authority/quota fixtures and the actual controller/service/model/client.
It does not certify live IAM, Atlas, Redis, Gateway ingress or SAG integration.

Independent trials use distinct opaque `user` values; transport retries preserve
identical request bytes to respect provider idempotency. There is no automatic
model fallback. Logs exclude note/prompt bodies and provider reasoning.

## Acceptance status

Semantic acceptance: **NOT_ESTABLISHED**. Human review must inspect meaning,
negation, uncertainty, technical identifiers, question necessity, language and
useful editing. Exact-pattern masking does not detect every possible unfenced
log/code/identifier. Production configuration still needs an explicitly accepted
model, provider policy review for real data and operational timeout/quota checks.
Provider failures preserve the draft and do not prevent ordinary canonical Save.

The final browser v0.3.2 grammar sample corrected the typo and retained “not yet
tested” without exposing masking in its summary. Its summary also said it added a
comma that was already in the source. This is a concrete minor explanation-quality
limitation, further reason to retain Before/After and explicit author review;
neither a successful smoke test nor a revised prompt proves perfect summaries.

Official references checked for this implementation are recorded in protocol 01
and BE `scripts/work-note-agent/README.md`; no private competitor prompt is
claimed to have been researched or reproduced.
