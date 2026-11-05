# 20 — v26 Release-Gate Audit & Prompt Anti-Obsolescence Execution Report (2026-11-03)

## 1. Executive Summary

This report documents the end-to-end execution of the Work Note Agent Prompt Audit & Anti-Obsolescence Plan (v4) across backend (`DATN-BE`) and frontend (`DATN-FE`), resolving design decisions `G1`–`G7` and open points `O1`–`O6`.

The engineering effort focused on closing the model obsolescence loop, fixing parser rigidity, enforcing non-repudiation and prompt fingerprints, establishing rigorous synthetic corpora, tightening prompt instructions, and validating gate hygiene.

- **Backend Branch:** `feat/DanhDEV-worknote-prompt-audit-be-api`
- **Frontend Branch:** `feat/DanhDEV-worknote-prompt-audit-fe-ui`
- **Audit Date:** 2026-11-03
- **Project Lead Role:** Autonomous execution per instructions ("những gì cần chốt thì bạn tự chốt vì tôi cho bạn là project lead").

---

## 2. Baseline Audit (Phase 0) & Offline Replay Tooling

1. **v25 Baseline Re-audit:**
   - Captured in `scripts/work-note-agent/assessment-plan-v3-release-gate-v25-2026-11-03.json` and documented in `19-v25-release-gate-audit-2026-11-03.md`.
   - Recorded `criticalErrors: 2 (raw) / 1 (runtime)`, `adequacyMacroF1: 0.8561 (raw) / 0.8450 (runtime)`, `CONTRADICTORY n=3`.
2. **Offline Replay Tool:**
   - Created `scripts/work-note-agent/assessment-release-replay.ts` to replay recorded raw responses through parsers, rubrics, and runtime state machines without spending LLM tokens.
   - Confirmed on v25 baseline: 88 analysis turns and 50 editor turns replayed deterministically.

---

## 3. Engineering Foundations & Guards (Phase 1)

### 3.1 D10b: Empty `changeSummary` for Identical Text
- **Backend:** In `work-note-agent.ts`, parser allows `changeSummary: []` if and only if restored `replacementText` is identical to the original target (under exact line ending `\r\n`->`\n` and Unicode NFC normalization for `operation !== 'title'`). If text is altered but `changeSummary` is empty, parser rejects with `REWRITE_EMPTY_CHANGE_SUMMARY` (`AgentValidationError`, code `INVALID_OUTPUT`).
- **Frontend:** In `WorkNoteProposal.tsx`, empty `changeSummary` when replacement equals original displays localized notice *"Nội dung ghi chú đã tối ưu, không có thay đổi nào cần thực hiện."*
- **Tests:** Full unit test coverage in `work-note-agent.spec.ts` and `WorkNoteProposal.spec.tsx`.

### 3.2 D10a: Contiguous Clause Substring Claim Parser (F15)
- **Parser Logic:** In `work-note-assessment.polarity.ts` and `work-note-assessment.protocol.ts`, a claim is accepted as `FULL` support when it is a unique, contiguous, clause-bounded literal substring of its cited quote under strict NFC normalization.
- **Invariants Preserved:**
  - Strict polarity and negation preservation: claims that drop negation words, invert completion status, or alter conditionality are never promoted.
  - No fragmented or cross-source claiming: claims concatenated from disparate parts remain `PARTIAL`.
- **Adversarial Test Suite:** 5 test categories (dropped negation, completion status inversion, semantic alteration by truncation, insufficient context, discontinuous phrase stitching) in `work-note-assessment.polarity.spec.ts` (85/85 tests passed).
- **Offline Baseline Verification:** Replaying v25 baseline promoted 2 valid compound claims to `FULL` without increasing any critical errors (`claimsPromotedToFull: 2`, `criticalErrorsIncreased: false`).

### 3.3 D9: Quality Gate Hygiene & Resumability
- In `scripts/work-note-agent/assessment-quality-gate.ts`:
  - Added sample size `n` per adequacy class (`CONTRADICTORY`, `INSUFFICIENT`, `SUFFICIENT`).
  - Added `lowSampleClasses` tracking and `lowSampleWarning` if any class has `n < 8`.
  - Added `provisional: true` and `releaseStatus: 'PROVISIONAL_INCOMPLETE_STAGE'` when execution is stopped early with remaining cases.
  - Added `partitionResumableStageScenarios` and `mergeResumedStageRows` to support atomic resumption on transport/rate-limit interruptions without restarting from scratch or duplicating runs.

### 3.4 D1: Prompt Fingerprint Non-Repudiation Guard
- Generated `prompt-fingerprints.json` across 14 distinct prompt surfaces (including all rewrite operations, assessment, assessor, split, and editor).
- Created `scripts/work-note-agent/update-prompt-fingerprints.ts`.
- Integrated guard into test suite `work-note-prompt-fingerprint.spec.ts`, verifying that any undocumented prompt alteration fails CI immediately.

### 3.5 D2: Validated Config Guard
- Implemented `src/services/capture/application/work-note-agent/validated-config.guard.ts`:
  - **Warn before PASS:** When zero configs have passed, requests proceed with `validatedConfig: false` and a warning log.
  - **Block after PASS:** Once >= 1 config passes, unvalidated configurations are blocked with `WORKNOTE_AGENT_UNAVAILABLE`.
- Wired into `WorkNoteAgentModel`, provenance reporting, and state schema validation (`traceKeys` updated in `work-note-assessment-state.validation.ts`).

### 3.6 D6: Privacy-Safe Feedback Telemetry
- Implemented `work-note-feedback-telemetry.ts` and MongoDB persistence (`WorkNoteFeedbackPersistenceService`).
- Created `scripts/work-note-agent/feedback-report.ts` for aggregated feedback inspection.

### 3.7 Five Synthetic Corpora Authored & Validated
1. `cases-assessment-v6-release.json`: 60 scenarios (20 validation + 40 holdout, 88 analysis turns, 14 `CONTRADICTORY` turns, 10 in holdout satisfying `n >= 8`).
2. `cases-assessment-dev-v26.json`: 10 targeted development scenarios for mechanism verification (L1–L5).
3. `cases-assessment-history-v1.json`: 18 scenarios (6 dev + 6 val + 6 holdout, 9 families × 2 contrastive pairs).
4. `cases-rewrite-workflows-v1.json`: 32 cases (16 `PROJECT_DOCUMENT` + 16 `WORK_REPORT`).
5. `cases-editor-nochange-v1.json`: 12 cases (6 clean + 6 dense numeric notes).

---

## 4. Prompt Engineering v26 (Phase 2)

1. **Rubric Synchronization & PROGRESS Conflict (2.1):**
   - Interpolated `formatAllowedBlockingNeedsLines()` directly from `PURPOSE_RUBRIC_TABLE` into prompts (`work-note-assessment.prompt.ts`, `work-note-assessment-split.ts`).
   - Comment in `rubric.ts` updated to "14".
   - Enforced that for purpose `PROGRESS`, `HISTORICAL_CONFLICT` is `BLOCKING` only for genuine `SELF` conflicts with current anchor.
2. **QA Observed Behavior Rule (2.2, F14):**
   - Tightened `PURPOSE_RUBRIC_TABLE.QA` and prompts: executing a test without reporting observed behavior is `NEEDS_AUTHOR_INPUT` (`test_result.behavior`).
   - Added `qaMissingObservedResult` few-shot example.
   - Reinforced that unrun scenarios must not be emitted as blocking gaps when another scenario has observed outcomes.
3. **CONTRADICTORY Few-Shot & Multi-Turn Grounding (2.3):**
   - Authored new `criteriaViolationContradictoryExample` (direct 512KB vs <=64KB violation -> `CONTRADICTORY` with `nextQuestion: null`).
   - Reinforced in prompt instructions that each claim must cite the exact `sourceId` containing it.
4. **Purpose Reset Gap Sanitization (2.4, F16):**
   - In `work-note-assessment.state.ts`, non-allowed blocking needs are normalized to `OPTIONAL` upon purpose reset or when `noteAdequacy === 'ENOUGH_FOR_PURPOSE'`, and `rawHasBlocking` respects `isAllowedBlockingGap`.
5. **Prompt Version Bumps & Fingerprint Lock (2.5):**
   - `ASSESSMENT_PROMPT_VERSION = 'task-note-assessment/2026-11-03.v26'`
   - `TASK_ASSESSOR_PROMPT_VERSION = 'task-note-assessor/2026-11-03.v3'`
   - `SPLIT_ASSESSMENT_PROMPT_VERSION = 'task-note-assessment-split/2026-11-03.v3'`
   - `ASSESSMENT_EDITOR_INSTRUCTION_VERSION = 'task-note-editor/2026-11-03.v5'`
   - Re-hashed and locked in `prompt-fingerprints.json`.
6. **Live Dev-v26 Verification (2.6):**
   - 6 scenarios evaluated in batch `plan-v4-dev-26-20261103`: 3 scenarios passed automated checks (`dev26-l1-compound-multianswer-a`, `dev26-l2-reset-purpose-b`, `dev26-l4-criteria-violation-a`), while 3 surfaced expected or intermediate prompt issues:
     - `dev26-l1-compound-multianswer-b` (turn 2): `REQUIRED_QUESTION_MISSING` (model concluded without asking clarification).
     - `dev26-l2-reset-purpose-a` (turn 1): `QUESTION_GAP_KIND` (model emitted incorrect gap kind for question).
     - `dev26-l4-criteria-violation-b` (turn 1): runtime `NOTE_ADEQUACY` (model evaluated as `UNDETERMINED` instead of expected).
   - Scenarios `dev26-l3-qa-action-only-a/b` and `dev26-l5-history-conflict-a/b` were verified in separate focused runs (`plan-v4-dev-22c-20261103`, etc.).

---

## 5. Release Gate v26 Execution & Hygiene (Phase 3)

### 5.1 Manifest Freeze (3.1)
- **Manifest Path:** `.worknote-agent-evals/plan-v4-release60-v26-20261103.freeze-manifest.json`
- **Manifest Hash:** `1ca18bec34bf2f11484ef465b179597ea49daaaca9778d13ca19e00ed2e50478`
- **Files Frozen:** 22 files (14 prompt/pipeline surfaces + 6 security surfaces + quality gate + v6 corpus).
- **Post-Review Restoration:** Restoration was verified against all 22 frozen hashes before further fixes. The subsequent v27 candidate intentionally differs; the v26 manifest and checkpoints remain immutable historical evidence.

### 5.2 Validation Stage Live Results (3.2) — `FAILED_AUTOMATED_GATE`
- **Status:** **`FAILED_AUTOMATED_GATE`** (`automatedGatePassed: false`).
- **Scenarios Evaluated:** 20/20 completed (28 turns, 10 editor calls).
- **Runtime Metrics vs Required Thresholds:**

| Metric | Raw Model | Post-Guard Runtime | Gate Threshold | Result |
|---|---:|---:|---:|:---:|
| **Critical Errors** | 1 (falseSufficient) | **0** | 0 | **PASS** (Runtime) |
| **Adequacy Macro-F1** | 0.9262 | **0.9552** | ≥ 0.90 | **PASS** |
| — CONTRADICTORY F1 (`n=5`) | 1.0000 | 1.0000 | — | *Low-sample* |
| — INSUFFICIENT F1 (`n=11`) | 0.9091 | 0.9565 | — | — |
| — SUFFICIENT F1 (`n=12`) | 0.8696 | 0.9091 | — | — |
| **Question Recall** | 0.8750 | **0.8750** | ≥ 0.90 | ❌ **FAIL** |
| **Question Precision** | 0.8750 | **0.8750** | ≥ 0.90 | ❌ **FAIL** |
| **Answer Usage Accuracy** | 0.8750 | **0.8750** | ≥ 0.95 | ❌ **FAIL** |
| **First-Pass Format Validity** | 0.9643 | **0.9643** | ≥ 0.98 | ❌ **FAIL** |
| **Source Reference Validity** | 1.0000 | **1.0000** | 1.0000 | **PASS** |
| **Editor Acceptance** | 10/10 (1.000) | **10/10 (1.000)** | ≥ 0.95 | **PASS** |

> [!CAUTION]
> The Validation Stage **did not pass** the automated technical gate due to shortfalls in Question Recall (0.875 < 0.90), Answer Usage (0.875 < 0.95), and Format Validity (0.9643 < 0.98). While Adequacy Macro-F1 (0.9552) and runtime critical errors (0) met thresholds, the gate strictly requires all technical criteria to pass.

### 5.3 Holdout Stage Live Execution (3.3) — `PROVISIONAL_INCOMPLETE_STAGE` & Substantive Failures
- **Status:** **`PROVISIONAL_INCOMPLETE_STAGE`** (`provisional: true`, `automatedGatePassed: false`).
- **Scenarios Evaluated Live:** 32 of 40 completed (38 turns, 11 editor calls). Exactly 8 cases remain un-evaluated due to provider daily quota.
- **Runtime Metrics on Completed 32 Holdout Cases:**

| Metric | Raw Model | Post-Guard Runtime | Gate Threshold | Result |
|---|---:|---:|---:|:---:|
| **Critical Errors** | 3 (falseSufficient) | **3 (falseSufficient)** | 0 | ❌ **CRITICAL FAIL** |
| **Adequacy Macro-F1** | 0.8493 | **0.8002** | ≥ 0.90 | ❌ **FAIL** |
| — CONTRADICTORY F1 (`n=10`) | 0.9474 | 0.9474 | — | Strong |
| — INSUFFICIENT F1 (`n=15`) | 0.7857 | 0.7333 | — | Deficient |
| — SUFFICIENT F1 (`n=13`) | 0.8148 | 0.7200 | — | Deficient |
| **Question Recall** | 0.7500 | **0.7500** | ≥ 0.90 | ❌ **FAIL** |
| **Question Precision** | 0.9000 | **0.9000** | ≥ 0.90 | **PASS** |
| **Answer Usage Accuracy** | 0.6667 | **0.6667** | ≥ 0.95 | ❌ **FAIL** |
| **First-Pass Format Validity** | 0.9474 | **0.9474** | ≥ 0.98 | ❌ **FAIL** |
| **Source Reference Validity** | 1.0000 | **1.0000** | 1.0000 | **PASS** |
| **Editor Acceptance** | 11/11 (1.000) | **11/11 (1.000)** | ≥ 0.95 | **PASS** |

> [!IMPORTANT]
> **Substantive Gate Outcome**: Even if all 8 remaining holdout scenarios were to execute with 100% precision, the **3 recorded falseSufficient critical errors mathematically guarantee that Holdout will FAIL the automated gate** (threshold is strictly 0 critical errors). The release gate is failing on model accuracy and question recall, not merely paused due to provider rate-limits.

- **Provider Quota Interruption:**
  - After 88 total HTTP attempts across validation and holdout, xKiro returned HTTP 429 (`x-ratelimit-scope: free`, `x-ratelimit-window: day`, `retry-after: 65737`).
  - Exactly 8 remaining scenarios were cleanly captured in `remainingCaseIds`:
    `["v6-tenant-quota-banner-a", "v6-tenant-quota-banner-b", "v6-iban-checksum-validator-a", "v6-iban-checksum-validator-b", "v6-webhook-retry-jitter-a", "v6-webhook-retry-jitter-b", "v6-opensearch-ilm-rollover-a", "v6-opensearch-ilm-rollover-b"]`.
  - Checkpoint cleanly preserved in `.worknote-agent-evals/plan-v4-release60-v26-20261103.holdout-rows.json`.

### 5.4 Blinded Human Review & Adjudication (3.4) — `NOT_ESTABLISHED`
- In strict adherence to scientific integrity, `reviewerSemanticAssessment` remains `'NOT_ESTABLISHED'`.
- **Status:** **Chưa thực hiện** (Pending completion of holdout run and formal human reviewer evaluation). No human ratings have been fabricated.

### 5.5 Validated Config Guard State (3.5) — Blocked
- Policy: Warning mode before any PASS; blocking mode after PASS.
- Because both Validation (`FAILED_AUTOMATED_GATE`) and Holdout (`PROVISIONAL_INCOMPLETE_STAGE` with 3 critical errors) failed automated thresholds, **no entry has been added to `validated-configs.json`**.
- The system remains in warning mode (`validatedConfig: false`), correctly rejecting promotion of unvalidated configurations.

---

## 6. Phase 4 Unproven Feature Measurements & Diagnostics

1. **History Corpus (`cases-assessment-history-v1.json`):**
   - 18 scenarios authored to measure `history.conflict`, `OUTDATED_INFO`, `SUPERSEDED`, and parent/child boundary conditions.
   - Quality gate validator `validateHistoryAssessmentCorpus` passes 100%.
2. **Workflow Separation (`cases-rewrite-workflows-v1.json`):**
   - 32 cases (`PROJECT_DOCUMENT` and `WORK_REPORT`) authored and verified.
   - Diagnostic metrics (`clarificationFP`, `clarificationFN`, `polarityFailure`, `emptyChangeSummaryAccepted`) integrated into `evaluation.ts`.
3. **Editor No-Change Corpus (`cases-editor-nochange-v1.json`):**
   - 12 cases testing clean and dense numeric notes against D10b parser rules.
   - Validated against `validateAgentInput`.

---

## 7. System Verification & Clean Build

| Component | Test Suite | Result |
| --- | --- | --- |
| **Backend Unit Tests** | `npm test` (Jest) | **218 passed**, 2166 tests passed (0 failures) |
| **Backend Lint** | `npm run lint` (ESLint) | **0 errors**, 6 warnings |
| **Backend Scripts Lint** | `npx eslint "scripts/work-note-agent/*.ts"` | **0 errors**, 0 warnings |
| **Backend Typecheck** | `npm run typecheck` (`tsc --noEmit`) | **0 errors** |
| **Backend Build** | `npm run build` (`nest build`) | **Successfully built** |
| **Frontend Unit Tests** | `npm test` (Vitest) | **181 passed**, 1257 tests passed (0 failures) |
| **Frontend Lint** | `npm run lint` (ESLint) | **0 errors**, 6 warnings |
| **Frontend Typecheck** | `npm run typecheck` (`tsc --noEmit`) | **0 errors** |
| **Frontend Production Build** | `npm run build` (`next build`) | **Successfully compiled** (109 static pages) |

---

## 8. Git Status & Next Steps

- **BE Branch:** `feat/DanhDEV-worknote-prompt-audit-be-api`
- **FE Branch:** `feat/DanhDEV-worknote-prompt-audit-fe-ui`
- **Documentation Branch:** `docs/DanhDEV-worknote-task-assessment`

**Historical v26 resume only (not for current v27 candidate):**
Run the single resume command:
```bash
npx ts-node --transpile-only --project tsconfig.json scripts/work-note-agent/assessment-release-gate-run.ts holdout plan-v4-release60-v26-20261103 --corpus=v6
```
Only the exact frozen v26 snapshot may resume these 8 scenarios. Completing this run cannot erase the 3 recorded critical errors and does not authorize an entry in `validated-configs.json`. The current working tree is a v27 candidate and must use a separate development and release evaluation with unseen holdout data. Promotion requires automated PASS plus blinded human review.


## 9. Review correction — 2026-11-03

The clean-build results in section 7 are historical, not a certification of later working-tree bytes. Restoring v26 reintroduced TS2339 and formatting failures. The correction adds the missing predicate type, formats affected files, and introduces an unvalidated v27 prompt candidate with a contradiction safety guard. No claim of live v27 PASS is made. TTL migration tests use a disposable MongoDB instance; database-target application remains pending.

Validation of review fixes (2026-11-03): `npm run check` exit 0; lint 0 errors / 6 existing warnings; typecheck and build pass; unit 218 suites / 2168 tests pass (15 suites / 137 tests skipped); e2e 19 suites / 176 tests pass (2 suites / 4 tests skipped). TTL disposable-Mongo tests 2/2 pass. Replay v25: 88 analysis / 50 editor, no increase in critical errors. All 14 current prompt fingerprints match. Live v27 quality remains unverified; v26 remains FAILED. No migration applied to the target database, no commit/push/merge performed in this correction.

---

## 10. Subsequent Iteration & Unseen Release Gate v37 (`v7` Corpus) — 2026-11-05

Following the v26 failure analysis, prompt and deterministic state/protocol guards were iteratively refined through development corpus `dev-v30` (34 scenarios, 37/37 turns PASS, `Macro-F1 = 0.9910`, `0` critical errors) up to:
- Analysis prompt version: `task-note-assessment/2026-11-05.v34`
- Split prompt version: `task-note-assessment-split/2026-11-05.v5`
- Editor instruction version: `task-note-editor/2026-11-05.v6`

An unseen 60-case synthetic release corpus (`scripts/work-note-agent/cases-assessment-v7-release.json`, `--corpus=v7`, 20 validation + 40 holdout scenarios, 88 analysis turns) was authored and frozen under phase `plan-v4-release60-v37-20261105` (`manifestHash = 42d0d6cb818dc3604cb5f62c45540b0f907469e355017e112c11726872e3385a`, LF-normalized SHA-256 across all 71 frozen files).

| Runtime Metric (`postGuardRuntime`) | Validation (20 cases / 28 turns) | Holdout (40 cases / 60 turns) | Combined Release-60 (60 cases / 88 turns) | Threshold | Status |
|---|---:|---:|---:|---:|:---:|
| **Critical errors** (`fabrication` / `polarityInversion` / `falseSufficient`) | **0** (`0/0/0`) | **0** (`0/0/0`) | **0** (`0/0/0`) | `= 0` | **PASS** |
| **Accepted source reference validity** | **1.0000** (`212/212`) | **1.0000** (`435/435`) | **1.0000** (`647/647`) | `= 1.00` | **PASS** |
| **Adequacy Macro-F1** | **1.0000** | **1.0000** | **1.0000** | `>= 0.90` | **PASS** |
| **Question precision** | **1.0000** (`6/6`) | **1.0000** (`16/16`) | **1.0000** (`22/22`) | `>= 0.90` | **PASS** |
| **Question recall** | **1.0000** (`6/6`) | **1.0000** (`16/16`) | **1.0000** (`22/22`) | `>= 0.90` | **PASS** |
| **Answer usage accuracy** | **1.0000** (`8/8`) | **1.0000** (`20/20`) | **1.0000** (`28/28`) | `>= 0.95` | **PASS** |
| **First-pass format validity** | **1.0000** (`28/28`) | **1.0000** (`60/60`) | **1.0000** (`88/88`) | `>= 0.98` | **PASS** |
| **Editor acceptance** | **1.0000** (`10/10`) | **1.0000** (`18/18`) | **1.0000** (`28/28`) | `>= 0.95` | **PASS** |
| **Workflow completion** | **1.0000** (`28/28`) | **1.0000** (`60/60`) | **1.0000** (`88/88`) | `= 1.00` | **PASS** |
| **`automatedGatePassed`** | **`true`** | **`true`** | **`true`** | `true` | **PASS** |

- **Report artifact:** `scripts/work-note-agent/assessment-plan-v4-release60-v37-20261105-release-gate.json`
- **Blinded human review status:** `reviewerSemanticAssessment: "NOT_ESTABLISHED"`, `releaseStatus: "AWAITING_BLINDED_HUMAN_REVIEW"` (`.worknote-agent-evals/plan-v4-release60-v37-20261105.blinded-worksheet.json` and `.sealed-key.json` generated for 60 transcripts). `validated-configs.json` remains in warn-only mode (`entries: []`) until human blinded review is completed.
