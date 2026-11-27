# Task-aware WorkNote assessment delivery — 2026-10-29

Implementation is delivered for review; release quality is not approved. Authority
is the user's explicit autonomous implementation request for plan v2. Database,
backend, frontend and documentation remain separate PRs; nothing was merged or
activated on Atlas/shared environments. Existing SAG integration remains deferred.

## Implemented behavior and evidence

| # | Requirement | Delivery / verification |
|---|---|---|
| 1 | Task understanding | Authorized Task title/description/status/checklist, objective/scope and extracted criteria |
| 2 | Active sources | Server-built manifest, source versions, loaded/included status and inspectable text |
| 3 | Context diagnostics | Missing authored criteria separated from malformed/unavailable Task acquisition; no provider call on invalid context |
| 4 | Citation validity | Loaded/included source ID and exact source passage checked; capitalization-only canonicalization is unambiguous and returns exact source text |
| 5 | Semantic support | FULL/PARTIAL/CONTRADICTED/RELATED_ONLY/INSUFFICIENT; negation and requirement-versus-result guards; model/rubric judgment remains fallible |
| 6 | Verification level | Author report and Task requirement are separate; no TOOL_VERIFIED or independently verified completion |
| 7 | Purpose and coverage | QA/progress may be adequate without Task completion; completion needs clear criteria and supported coverage |
| 8 | Bounded questions | One active question, three-question ceiling, two no-progress turns, unknown/skip suppression and manual continuation |
| 9 | State machine | Analyzing, waiting_for_answer, missing_context, contradiction, ready_to_edit, stale, paused, error controlled by code |
| 10 | Corrections / reset | Claim/gap-targeted author supplement; explicit new session and selected eligible answer carry; no Task mutation |
| 11 | Concurrency / access | Current authorization, CSRF/private cache, dual revision CAS, shared quota/lease, scoped idempotency and stale replay rejection |
| 12 | Independent outcomes | Proposal, explicit Apply, author validation, technical Save and independent review remain separate signals |
| 13 | Privacy | Private assessment/answers/corrections/feedback/trace bounded by absolute24h, cleaned on Save/Discard; canonical text/history preserved |
| 14 | Evaluation / economics | Frozen72 synthetic scenarios,36/12/24 family split,48/16/8 turn distribution; actual aggregate development pilot cap29 HTTP attempts |

No automatic sending, Jira creation, Apply, Save, memory learning, web/repository
retrieval, Project glossary or SAG activation was added. Ordinary Save remains
independent of assessment/provider availability. Flags WORKNOTE_ASSESSMENT_ENABLED
and NEXT_PUBLIC_WORKNOTE_ASSESSMENT_ENABLED default false.

## Verification

DB: final full lint/typecheck/build passed;1512 unit and169 e2e tests passed;
8 assessment storage checks and3 disposable Mongo expiry migration tests passed.
OpenAPI:7 POST routes,20 schemas and15 positive/negative fixtures validated.

FE: full lint/typecheck/build passed with142 suites/973 tests. After final UI race
fixes,33 focused tests, lint/typecheck and production build passed again. Review
fixed stale409 badges, dismissed proposal reopening and answer-buffer leakage.

BE: full npm check passed lint/typecheck/build,1678 unit tests (137 skipped) and169 e2e tests (4 skipped). After the final timestamp-less legacy receipt lifetime guard,159 focused WorkNote regression tests passed (2 skipped); lint/typecheck were rerun. The final production build includes that guard.

Browser at http://127.0.0.1:3019/ uses a clearly labeled deterministic provider,
real editor/assessment HTTP services and disposable local MongoDB. Verified:
question -> unknown -> new QA session without carry -> targeted correction ->
author-validation signal -> proposal without content mutation -> explicit Apply ->
stale assessment -> confirmation -> Save. Original uncertainty was retained.
This is application lifecycle evidence, not xKiro quality or real author approval.
Screenshots are local ignored artifacts under FE/.worknote-agent-preview-evidence:
assessment-ready-20261029.png and assessment-save-success-20261029.png.
The ordinary authenticated app remains http://localhost:3000/; assessment is off.

## Live development pilot and release decision

Model: mistralai/ministral-14b. All29 actual HTTP attempts across development runs
and one diagnostic are counted, including failed calls. Reported total tokens:
73953; unknown usage attempts:0. Monetary cost is NOT_ESTABLISHED, not zero.
No fallback model, validation/holdout inference, or full176-call run was performed.
No provider calls remain within this phase's29-attempt ceiling.

Initial development runs failed strict schema/source checks and exposed unnecessary
questions. Prompt versions were tuned only on development: explicit enum/object
schemas, extractive quotes, empty-source handling, vague Task titles versus criteria,
and QA/progress adequacy versus incident clarification. Final prompt:
task-note-assessment/2026-10-29.v5; system prompt SHA256
`ddf585f7fb49d16c796dea75a65da4225c8ba8a0b427b51b59f91fd67425b247`.
Corpus SHA256
`1f86e0207b2554948b04148f45cb01462910b52ddeac79d92197c63530f9e1d9`.

Final10-call development run:7 assessment outputs passed automated rubrics;
2 Editor outputs passed the strict protocol parser;1 Editor output failed validation. Harness Editor uses restructure rather than runtime custom, a different instruction/gap context, no formatting recovery, zero retries and8192 output tokens rather than runtime4096. Its parser accepts more status branches than runtime proposal generation. These outputs are protocol observations, not runtime proposal acceptance; README records all parity limits.
A subsequent Editor request was denied before network access by the exhausted cap;
remaining scenarios were skipped. This is neither12 complete pilot scenarios nor
72 live scenarios, and automated passes are not human semantic acceptance.
Quality gate remains NOT_PASSED; reviewerSemanticAssessment=NOT_ESTABLISHED.
Do not infer adequacy from Apply/Save, silence or positive feedback.

The versioned operator ledger and ignored synthetic reports/blank review worksheets
remain in BE/scripts/work-note-agent and BE/.worknote-agent-evals respectively.
Do not tune on holdout. Further live calibration requires a separately authorized
budget, independent transcript review and a newly frozen release evaluation.
Conservative lexical progress/fidelity checks can reject valid paraphrases; they
do not establish general entailment or reproduce the ALCE benchmark.

## Review, rollback and handoff

Read-only review-agent was the user-approved substitute. Identified source polarity,
gap identity, stale replay, expired-lease completion, malformed acquisition and UI
race findings were fixed with regression tests. No operational raw-note logs,
long-term learning store or new package dependency was introduced.

Rollback: leave both assessment flags false; existing editor, grammar and Save
continue. Private state expires and can be discarded through existing explicit
workflow. DB migration is offline dry-run by default and expiry-only; expiry
shortening cannot restore already-expired private text. Do not run Atlas migration
or remove TTL indexes as rollback. No existing migration was edited.

PRs: DB https://github.com/DATN-SPRING2027/DATN-BE/pull/108; FE https://github.com/DATN-SPRING2027/DATN-FE/pull/101. BE https://github.com/DATN-SPRING2027/DATN-BE/pull/109. This delivery is carried by the companion DOC draft PR. Jira identifier remains
for DanhDEV to add; DB/team notification remains an unsent draft.

Final source snapshots: DB a159b5e; BE897add0; FE c079968. Final source lint and typecheck passed after the regression guard; six pre-existing legacy test lint warnings remain, zero lint errors.

work-note-assessment.protocol.ts SHA256: `19d9c5eb4881c0dcf4f9271ec3a63068e4558e18482df7d6de7c95d26338056f`.

work-note-assessment.state.ts SHA256: `0e8115aab9ba43b455f5437d30c6f9d582d176800d5ca127990e0f56c2db7c0e`.
