# Agent WorkNote — prompt and evaluation protocol

Status: experimental design/implementation record; no production acceptance.

Later implementation and frozen v0.3 / development v0.3.1 evidence:
[delivery 05](05-local-delivery-and-review.md), [evaluation 06](06-v03-evaluation.md).

## External product patterns and their limits

Microsoft Word documents selection-based Rewrite with Replace, Insert below and
Regenerate. Notion AI documents grammar/style edits and accept/discard/try-again.
Gemini Docs documents selected-text refinement and acceptance/rejection. These
public interaction patterns support human review of suggestions. They do not
reveal those products' private system prompts, safety guarantees or architecture.

- https://support.microsoft.com/en-us/word/copilot/edit-rewrite-content
- https://www.notion.com/help/notion-ai-faqs
- https://support.google.com/docs/answer/13447609
- https://www.anthropic.com/research/effective-context-engineering-for-ai-agents
- https://platform.claude.com/docs/en/test-and-evaluate/develop-tests

Sources were checked on 2026-10-27. Their content is external evidence, not DATN
product authority or permission to disclose project data.

## Prompt design

Five layers: standing system policy, operation policy, bounded source context,
diverse synthetic demonstrations and exact output shape. Operations are grammar,
clarify, shorten, restructure, tone, handover, title and custom. Outcomes are
ANSWER, CLARIFICATION_REQUIRED and SUGGESTION_READY. One important clarification
per turn; no routine checklist. Unsupported assertions are not manufactured to
satisfy an instruction.

Task context describes requirements and recorded status, not completed work.
DONE/checklist flags do not prove test/deployment success. Task descriptions and
notes remain untrusted source text even when fetched through an authorized API.
Clarification answers belong to the current draft. Assistant suggestions that
were not applied are never factual evidence. A skipped question remains unknown.

The Agent is invoked by an explicit user request. Typing/autosave does not trigger
unsolicited LLM transmission. Chat opens automatically only when that requested
operation produces a necessary clarification. Source language is independent of
the UI language. Keep polarity, conditions, numbers, evidence and uncertainty.

Selection context defaults to the selected text and at most 320 UTF-16 units on
each side; whole-note context requires an explicit setting. Model output never
selects range offsets, revision, IDs, permissions or the Apply target. The host
binds each proposal to the exact source snapshot. The current prototype masks
fenced/inline code, URLs, marker-like literals and explicit log ranges, including
partial selections inside a protected source range. This is not a complete
detector for arbitrary unfenced code/log, and does not prove semantic fidelity.

## Dataset and grading

120 authored synthetic requests: grammar 20, protected text 20, style 15, Task
context 20, selection 15, conversation 20, adversarial 10. Fixed stratified splits
are development 70, validation 25, holdout 25. Inputs contain no real WorkNote,
production identifier, credential or personal data.

Use development cases for tuning. Freeze prompt changes before validation and
holdout. Preserve prompt snapshots and record template/corpus hashes. A repeated
holdout after tuning becomes regression evidence, not a new independent test.
Phrase rules have false positives: required/forbidden words are not a substitute
for semantic review. Mark each model result manual-review-required until a
reviewer checks source fidelity, language, scope, hallucination, unnecessary
questions and usefulness. Do not use text equality for the entire rewrite.

Proposed promotion targets: first-pass valid shape at least 99% on an appropriately
sized sample; all proposals exposed to Apply must pass deterministic boundary
checks; no observed critical corruption of facts/polarity in the reviewed final
sample; at least 95% of clearly formal editing requests proceed without needless
questions. Report clarification precision/recall, latency P50/P95, token usage and
cost separately. These are targets, not achieved results or statistical guarantees.

## xKiro-specific protocol

Use one dialect initially: Chat Completions, full vendor/model ID, explicit token
budget and request deadline. The public catalog is not filtered by entitlement.
JSON mode enforcement varies and can be silently ignored. Validate syntax, exact
branch structure and protected content independently. Reject truncated responses.
Do not log/expose reasoning blocks. Streaming/format repair are not part of the
first evaluator and must not silently change first-pass metrics.

xKiro documents short-lived replay of identical blocking requests. Independent
trials use distinct opaque evaluation identities; an HTTP retry retains identical
bytes. Regenerate is a new intentional request. Do not count cached results as
independent stability trials. Record availability failures rather than repeatedly
retrying authentication/entitlement errors.

The privacy policy forwards prompts to model providers and describes limited
diagnostic exceptions. This does not establish upstream retention or permission
to send real notes. The current evaluator loads only its bundled synthetic corpus.

- https://docs.xkiro.com/api/chat-completions/
- https://docs.xkiro.com/guides/structured-output/
- https://docs.xkiro.com/api/idempotency/
- https://docs.xkiro.com/api/list-models/
- https://docs.xkiro.com/guides/reasoning/
- https://xkiro.com/privacy

## Baseline iteration record

v0.1 was run on development cases only. Observed failure types included incorrect
SUGGESTED_READY enum spelling, missing question.options, unnecessary questions,
translation into the system prompt's language, removing uncertainty while
shortening, and replacing protected markers with source fragments.

v0.2 clarifies the exact enum and required fields, keeps replacements in source
language, adds an English example and a protected-fragment example, and explicitly
preserves uncertainty and existing next-step scope. It does not embed testcase
IDs or alter policy for holdout cases. v0.1 is retained in the BE prompt archive.
See the evaluation record for measured outcomes; this description is not a claim
that v0.2 has resolved every failure.
