# WorkNote Assessment Plan v3 — Delivery, Architecture Pilot & Frozen Release Gate (2026-10-29)

Authority: Project Lead autonomous design & implementation under Plan v3 (`v14` baseline preserved; zero HTTP/OpenAPI/MongoDB wire schema breakage; `WORKNOTE_ASSESSMENT_ENABLED` and `NEXT_PUBLIC_WORKNOTE_ASSESSMENT_ENABLED` remain `false` by default).

## 1. Three Independent Conclusions & Purpose Rubric (Plan v3 §1)

Implemented in `DATN-BE/src/services/capture/application/work-note-agent/work-note-assessment.rubric.ts` and rendered as three independent columns in `DATN-FE/src/components/work-notes/WorkNoteAssessmentEvidence.tsx`:

| Conclusion | Runtime / UI Field | Question Answered |
|---|---|---|
| **Task clarity** | `taskContextStatus` (`CLEAR` / `PARTIAL` / `INSUFFICIENT`) | Does the Task specify clear objective, scope, and criteria? |
| **Note adequacy** | `noteAdequacy` (`ENOUGH_FOR_PURPOSE` / `NEEDS_AUTHOR_INPUT` / `UNDETERMINED` / `CONTRADICTORY`) | Is the note sufficient for its **current purpose**? |
| **Task completion** | Derived `deriveTaskCompletionStatus(...)` (`REPORTED_MET` / `INCOMPLETE_OR_PARTIAL` / `NOT_ESTABLISHED` / `CONTRADICTED`) | Does author-reported evidence cover all Task criteria? |

### Purpose Decision Matrix (`PURPOSE_RUBRIC_TABLE`)

| Purpose | Required for `ENOUGH_FOR_PURPOSE` | Explicitly Forbidden Over-asking |
|---|---|---|
| `PROGRESS` | Concrete completed/in-progress part + relevant known limitations | Full Task completion, testing of unfinished/untested parts |
| `DECISION` | Chosen option/decision + rationale or governing constraint | Implementation proof, deployment, or operating runbook |
| `INCIDENT` | Observed symptom + affected situation/scope | Root cause or fix when the author explicitly does not know yet |
| `QA` | Tested action, tested scope, and observed result | Testing of other untested parts outside the reported QA scope |
| `HANDOVER` | Current state + operational info/steps needed by receiver | Receiver read-confirmation unless required by Task criteria |
| `COMPLETION` | Clear Task criteria + author-reported results covering every criterion | Extra acceptance gates invented beyond authored Task criteria |

## 2. Shared Application Pipeline & App-Evaluator Parity (Plan v3 §2)

`DATN-BE/src/services/capture/application/work-note-agent/work-note-assessment.pipeline.ts` unifies:
- Source construction & authorization manifest (`buildAssessmentSources`, `computeAssessmentTaskHash`)
- Initial, reply, targeted correction, and purpose-reset input builders (`prepareInitialAssessmentInput`, `prepareReplyAssessmentInput`, `prepareCorrectionAssessmentInput`, `prepareResetAssessmentInput`)
- Combined (`A`) and Split (`B`) model execution (`executeAssessmentModelCall`)
- Deterministic state assembly (`finalizeAssessmentTurn` -> `assembleAssessment`)
- Runtime Editor request construction and protected-range/limitation validation (`executeAssessmentEditorTurn` -> `buildAssessmentEditorInput` + `assertAssessmentEditorProposal`)

Both `WorkNoteAssessmentService` (HTTP runtime) and `scripts/work-note-agent/assessment-run.ts` (evaluation harness) execute through this identical pipeline, verified by `work-note-assessment.parity.spec.ts`.

## 3. Narrowed Agent Roles & Closed Gap Taxonomy (Plan v3 §3)

- **Roles**:
  1. `Task Interpreter` (`work-note-assessment-split.ts` / `taskUnderstanding` contract): extracts Task objective, scope, literal requirements, and Task unknowns without judging note adequacy.
  2. `Assessor / Questioner` (`work-note-assessment.prompt.ts` + `work-note-assessment.state.ts`): extracts grounded `AUTHOR_REPORT` claims, requirement coverage, normalized gaps, adequacy, and at most one necessary question.
  3. `Editor` (`work-note-assessment-editor.ts` `task-note-editor/2026-10-29.v4`): edits author prose only when `canRequestAssessmentRewrite(view)` holds, preserving explicit limitations/negations and protected fragments without inventing gap answers.
- **Closed 12-Code Internal Information-Need Taxonomy (`ASSESSMENT_NEED_CODES`)**:
  - `scope.completed_part`, `test_context.actor`, `test_result.behavior`, `implementation.data_source`, `implementation.mechanism`, `decision.choice`, `decision.rationale`, `handover.operating_steps`, `handover.next_steps`, `incident.symptom`, `incident.impact_scope`, `contradiction.conflict`.
- **Stable Server-Owned Gap Identity**:
  - Gaps receive `gap-<needCode>-<hash16>` (anchored on normalized need, owner, and Task/contradiction scope rather than surface wording or `kind`), with `gapMatchesId` backward-compatibility for legacy 24-hex IDs and zero MongoDB/OpenAPI wire schema changes (`additionalProperties: false` preserved).

## 4. Architecture Screening Pilot Within Hard 29-Call Cap (Plan v3 §4)

Executed on `mistralai/ministral-14b` (`retries = 0`) and sealed in `DATN-BE/scripts/work-note-agent/assessment-plan-v3-pilot-2026-10-29.json` (`.worknote-agent-evals/plan-v3-arch-pilot-20261029.budget.json` = `29/29` HTTP attempts: `8` Variant A + `16` Variant B + `2` Editor smoke + `3` reserve diagnostic):

| Variant | HTTP Calls | Scenario Passes | Critical Errors | Editor Smoke | Latency / Cost Verdict |
|---|---:|---:|---:|---:|---|
| **A (`combined`)** | 8 | **6 / 8** (`75%`) | **0** | **2 / 2** (`100%`) | **Selected & locked** (`1x` analysis call/turn, more stable) |
| **B (`split`)** | 16 | 4 / 8 (`50%`) | **0** | — | Rejected (`2x` HTTP cost without accuracy gain on `ministral-14b`) |

## 5. Deterministic Guards, UI & Application Lifecycle Verification (Plan v3 §§5, 8)

- **Deterministic Runtime Guards (`work-note-assessment.state.ts`)**:
  - Questions must bind to an open `BLOCKING` gap necessary for the active purpose.
  - Inconsistent model output (`ENOUGH_FOR_PURPOSE` alongside any `BLOCKING` gap or non-null `nextQuestion`) downgrades deterministically to `noteAdequacy = 'UNDETERMINED'`, `state = 'missing_context'`, `reasonCode = 'INCONSISTENT_MODEL_OUTPUT'` with manual editing enabled — never auto-Apply, auto-Save, or false sufficient.
  - Answered, `unknown`, or `skipped` `needCode`s cannot be re-asked under paraphrased wording or changed `kind`.
  - Hard ceiling of `3` questions and `2` no-progress turns (`paused`).
  - Targeted corrections update author understanding without mutating Task requirements; Editor `v4` safely allows author-corrected prose numbers while keeping inline code, fences, URLs, and explicit `protectedRanges` immutable.
  - Purpose change starts a fresh session with controlled answer carry; Task/note/permission changes mark assessments stale (`409 ASSESSMENT_STALE`).
- **Offline Replay vs Historical Baseline**:
  - `npx ts-node scripts/work-note-agent/assessment-replay.ts`: `observedSteps: 110`, `stateMismatches: 0`, `regressed: []`, `improved: 7` (`27 -> 34` scenarios).
- **Full Repository Checks & Isolated Full-Stack E2E Smoke**:
  - `DATN-FE`: `npm run check` **PASSED** (`0` lint/type errors, `142/142` suites, `975/975` tests, Next.js production build green).
  - `DATN-BE`: `npm run check` **PASSED** (`0` lint errors, `0` typecheck errors, safety suites `PASS`, `187` unit suites / `1807` unit tests `PASS`, `17` E2E suites / `169` E2E tests `PASS`, `nest build` green).
  - `DATN-BE`: `scripts/work-note-agent/application-smoke.mjs` **PASSED** across all 8 full-stack stages (`REAL_MEMBER_LOGIN` -> `REAL_TASK_CREATION` -> `TASK_NOTE_AUTOSAVE` -> `TASK_NOTE_ASSESSMENT_AND_REWRITE` -> `TASK_NOTE_ASSESSMENT_STALE_AND_UNKNOWN_FALLBACK` -> `REAL_XKIRO_PROPOSAL` -> `CANONICAL_SAVE_AND_REPLAY` -> `SHARED_DOCUMENT_SAVE`) on disposable `MongoMemoryReplSet` + real loopback Redis.

## 6. Corpus Reclassification, Unseen 60-Case Release Corpus & Freeze Manifest (Plan v3 §§6–7)

- **80 Observed Cases Reclassified as Regression**: `cases-assessment-v3.json` (`72` cases) + `cases-assessment-v4-cross-domain.json` (`8` cases) = `80` regression cases (`112` analysis turns + `80` Editor max = `192` baseline calls). Legacy ledger `.worknote-agent-evals/cross-domain-20261029.budget.json` preserved untouched at `166/176`.
- **60 New Unseen Cases (`DATN-BE/scripts/work-note-agent/cases-assessment-v5-release.json`)**:
  - `30` disjoint task families × `2` contrastive variants (`A` vs `B`), zero family overlap between `validation` (`20` cases / `10` families) and `holdout` (`40` cases / `20` families).
  - Exact turn structure: `40` 1-turn + `12` 2-turn + `8` 3-turn = `88` analysis turns + `60` Editor max = `148` baseline calls; includes `unknown`, `skip`, `correction`, purpose reset, negation, and prompt injection scenarios.
  - **Holdout Integrity**: Zero post-holdout edits permitted — manifest locked before touching `holdout` (`2/40` `holdout` scenarios executed and checkpointed at `100%` pass before daily `HTTP 429`; remaining `38` unseen scenarios queued under immutable `manifestHash`).
- **Frozen Release Configuration (`plan-v3-release60-v24-20261030.freeze-manifest.json`)**:
  - Model: `mistralai/ministral-14b` | Architecture: `combined` | Retries: `0`
  - Assessment Prompt: `task-note-assessment/2026-10-30.v24` | Editor Prompt: `task-note-editor/2026-10-29.v4`
  - Provider Timeout & Lease Alignment: `85s` analysis (`95s` DB lease) / `60s` Editor (`70s` DB lease)
  - Manifest SHA256: `6aff57c3aa303e3c3b87597cb230036c5a05b4141190d2d09600c0434673c5d9`

## 7. Live Validation 100% Gate Pass, Holdout Checkpoint & Next Steps

- **Full `20 / 20` `validation` Automated Gate — PASSED (`100.0%` / `1.0000` across every metric on BOTH `rawModelOutput` and `postGuardRuntime`)**:
  - Locked in `.worknote-agent-evals/plan-v3-release60-v24-20261030.validation-rows.json` (`47` HTTP attempts, `358,358` tokens, `0` unknown-usage attempts):
    - **Accepted source references valid**: **`176 / 176` (`100.0%` PASS)**
    - **Critical errors** (fabrication, polarity inversion, false sufficient): **`0 / 30` (`0` PASS)** on both `rawModelOutput` and `postGuardRuntime`
    - **Adequacy macro-F1**: **`1.0000` (`100.0%` across `SUFFICIENT`, `INSUFFICIENT`, `CONTRADICTORY` — PASS)** on both `rawModelOutput` and `postGuardRuntime`
    - **Question precision & recall**: **`1.0000` (`TP = 7, FP = 0, FN = 0, TN = 23` — PASS)** on both `rawModelOutput` and `postGuardRuntime`
    - **Answer usage accuracy**: **`10 / 10` (`100.0%` PASS)** on both `rawModelOutput` and `postGuardRuntime`
    - **First-pass format validity**: **`30 / 30` (`100.0%` PASS)**
    - **Editor proposal acceptance**: **`17 / 17` (`100.0%` PASS)**
- **Manifest-Locked `holdout` Checkpoint (`assessment-release-gate-run.ts`)**:
  - Immediately after `20/20` `validation` passed `100%`, unseen `holdout` began under the identical frozen manifest (`6aff57c3aa303e3c3b87597cb230036c5a05b4141190d2d09600c0434673c5d9`).
  - The first **`2 / 40` `holdout` scenarios (`2/2` analysis + `1/1` Editor)** completed at **`100.0%` pass** (`11/11` valid source refs, `0` critical errors, `1/1` Editor accepted) before Key #3 hit xKiro's `~500k–520k` daily `free`-model token limit (`139,826 + 358,358 + 22,667 = 520,851` tokens -> `XKIRO_HTTP_ERROR_429`).
  - Current checkpoint in `plan-v3-release60-v24-20261030`: **`20 / 20` `validation` scenarios COMPLETE (`100.0%` pass), `2 / 40` `holdout` scenarios locked (`100.0%` pass), `38` `holdout` scenarios remaining (`56` analysis turns + `~21` Editor turns ≈ `77` calls ≈ `585k` tokens)**.
- **Release Gate Status**: Remains **`AWAITING_HOLDOUT_COMPLETION_AND_BLINDED_HUMAN_REVIEW`** (`reviewerSemanticAssessment: 'NOT_ESTABLISHED'`) pending:
  1. Resuming ONLY the remaining `38` frozen `holdout` scenarios after daily xKiro quota reset (`07:00 GMT+7` / `00:00 UTC`) or key rotation (zero code/prompt changes permitted):
     - `npx ts-node scripts/work-note-agent/assessment-release-gate-run.ts holdout plan-v3-release60-v24-20261030`
  2. Completing blinded human transcript review on `.worknote-agent-evals/plan-v3-release60-v24-20261030.blinded-worksheet.json` and adjudication via `adjudicateBlindedReviews(...)` in `scripts/work-note-agent/assessment-quality-gate.ts`.

