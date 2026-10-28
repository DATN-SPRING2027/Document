# Agent WorkNote — scope, baseline and delivery

Date: 2026-10-27. Owner: DanhDEV. Status: prompt evaluation implemented; the user
subsequently approved local Task Note integration under contract 04. Current
implementation/review/rollout status is in
[delivery record 05](05-local-delivery-and-review.md).

The user first requested research/planning only, then explicitly asked to execute
that plan and configured a local xKiro key for testing. This authorizes the
implementation/evaluation work, not a retrospective Product/Security approval of
new API/database/retention contracts. No external messages, Jira updates, push,
merge or deployment are included in this work.

The supplied brief is preserved as
[26-work-note-agent-rewrite-brief.md](26-work-note-agent-rewrite-brief.md), SHA-256
`07E138C00B38D93A234117154D4BE6CCDCCC80726AA476FEBB09FEA9DAFFD332`.
Its opening status remains unchanged: product/coder brief, not an approved OpenAPI,
database decision or SAG integration approval.

## Source snapshot and corrections to the brief

- BE base: `2325a8e`, branch `feat/DanhDEV-agent-worknote-be-api`.
- FE base: `5e001b3`, branch `feat/DanhDEV-agent-worknote-fe-ui`.
- Document base: `d9aa106`, branch `docs/DanhDEV-agent-worknote`.
- The existing WorkNote APIs are live source, not only a local FE preview.
  Task Note inputs use `title/accomplishments/approach/reason`; Capture persists
  their content into `whatDone/howSolved/whyThisWay`. Project Documents already
  have a freeform `content`. Work Reports retain structured content and review.
- Task Notes become CONFIRMED on create and have no Leader approval transition.
  They do not automatically enter official AI knowledge. Document/Report review
  is unchanged. See [the current workflow](../04_WORK_NOTE_WORKFLOWS.md).
- Task model contains description/status/steps. Capture's current authorization
  adapter retains Task key/title; a future authorized context projection must be
  designed rather than inventing an `acceptanceCriteria` field.
- Task Note FE draft recovery in the existing panel is session memory; it does
  not prove durable backend autosave. Existing Document/Report drafts are distinct.
- The current SAG HTTP adapter has an explicit path allowlist. Replacing its
  base URL with xKiro is not an implementation of the rewrite adapter.
- The existing AI Chat screen synthesizes local responses; it does not establish
  real WorkNote rewrite, retrieval or source eligibility.
- The current workflow documents integration outbox events, not a verified SAG
  consumer, citation correctness or immediate revoke enforcement.

## Delivered by the first milestone

In BE: versioned prompt policy and operation presets; bounded source/Task/history
assembly; exact protected fragment restoration; strict three-branch model output;
server-bound suggestion metadata and pure stale-safe draft replacement; explicit
xKiro client with deadline/retry handling; 120 synthetic cases with fixed
70/25/25 splits; offline tests, a no-network dry-run and an opt-in live evaluator.

At the first milestone the implementation was NOT registered in CaptureModule/Gateway. No WorkNote route,
schema, migration, lifecycle, UI, real note, shared database or SAG source changes
are part of that milestone. Its contract is internal experimental TypeScript,
not an approved public business API. Pure Apply is not persistence or permission.

The evaluation record must distinguish provider availability, schema compliance,
automated phrase rules, protection failures and semantic review. It must not call
an automated pass a verified fact, independent review or production readiness.

## Remaining work packages and exit conditions

1. Freeze a tested prompt/model configuration and inspect semantic failures with
   a human rubric. Keep development tuning separate from validation/holdout.
2. Review the concrete [integration proposal](02-integration-contract.proposed.md)
   and compatibility strategy. The user chose canonical-only retention with
   confirmation before original deletion and 24-hour abandoned draft/chat expiry.
   Approve exact OpenAPI/schema
   revisions before exposing APIs or changing persistence.
3. DB PR: additive freeform content, version snapshots, draft/session persistence
   and deterministic legacy backfill, with dry-run/rollback and data checks.
   Do not run a migration against a shared database implicitly.
4. BE PR: authorized draft/message/context/proposal operations, immutable source
   binding, concurrency, quotas and errors. Preserve current confirmation/review.
5. FE PR: large composer, two input fields, chat/selection, preview/diff, explicit
   Apply/Save, undo/redo, autosave recovery, accessibility and localization.
6. Reuse the editor for Documents and Reports only through their own contracts
   and permissions. Do not combine their state machines.
7. SAG package: decide eligibility, implement/verify the consumer, canonical
   provenance, version replacement, archive/revoke and retrieval evaluation.

These are feature completion gates. The prompt milestone alone does not satisfy
all acceptance criteria in the original brief.

The local Task Note implementation now registers guarded routes and adds the
composer, durable drafts/conversation, versioning and explicit Save. Application
flags default off; the DB package remains a separate branch. This advances work
packages 2–5 locally without asserting a shared rollout, teammate merge or SAG
completion. See record 05 for checks, boundaries and review findings addressed.
