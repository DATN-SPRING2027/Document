# 19 — v25 Release-Gate Baseline Audit & v26 Remediation Record (2026-11-03)

## 1. Frozen v25 Baseline Measurement (`plan-v3-release60-v25-20261103`)

- **Analysis Prompt Version:** `task-note-assessment/2026-11-02.v25`
- **Editor Instruction Version:** `task-note-editor/2026-10-29.v4`
- **Model / Architecture:** `mistralai/ministral-14b` (`combined`, `retries: 0`)
- **Expanded Freeze Manifest (14 files):** `2a252f2de53d2add0e2807f3f2ca5937b83cc1d8631df5bd6b8138849f6682bb`
- **Corpus:** `task-note-assessment-release60/2026-10-29.v5` (20 validation + 40 holdout = 60 scenarios; 88 analysis turns)
- **Consumed Phase Budget:** `142 / 148` HTTP attempts, `1,108,718` provider-reported tokens (`1,223,287` accounted reservation tokens; `3` unknown-usage attempts)
- **Summary Artifact:** `DATN-BE/scripts/work-note-agent/assessment-plan-v3-release-gate-v25-2026-11-03.json`

### Gate Metrics Summary

| Metric | Threshold | Validation (20) | Holdout (40) Raw / Runtime | Combined (60) Raw / Runtime |
| --- | --- | --- | --- | --- |
| Source Reference Validity | `1.00` | `176/176 (1.000)` | `322/322 (1.000)` | `498/498 (1.000)` |
| Critical Errors (`falseSufficient`) | `0` | `0` | **`2 / 1`** (FAIL) | **`2 / 1`** (FAIL) |
| Adequacy Macro-F1 | `>= 0.90` | `1.000` | **`0.8561 / 0.8450`** (FAIL) | `0.9116 / 0.9037` |
| — `CONTRADICTORY` sample count | — | `n = 1` (`tp=1`) | `n = 2` (`tp=1, fn=1`) | `n = 3` (`tp=2, fn=1`) |
| Question Precision / Recall | `>= 0.90` | `1.000 / 1.000` | `0.9333 / 0.9333` | `0.9545 / 0.9545` |
| Answer Usage Accuracy | `>= 0.95` | `10/10 (1.000)` | `18/18 / 16/18 (0.8889)` (FAIL) | `28/28 / 26/28 (0.9286)` (FAIL) |
| First-Pass Format Validity | `>= 0.98` | `30/30 (1.000)` | `58/58 (1.000)` | `88/88 (1.000)` |
| Assessment Editor Acceptance | — | `17/17` | `31/33` | `48/50` |
| **Automated Gate Decision** | — | **PASS** | **FAILED_AUTOMATED_GATE** | **FAILED_AUTOMATED_GATE** |
| **Semantic Review Status** | — | `NOT_ESTABLISHED` | `NOT_ESTABLISHED` | `NOT_ESTABLISHED` |

## 2. Holdout Failure Taxonomy (Observed Categories — Never Copied into Prompts)

1. **L1 (Compound clause excerpt + cross-source quote mismatch on correction turn):** Model emitted two claims on a compound sentence; one was a contiguous clause substring of the cited turn-3 quote, while the other reused turn-2 wording while citing turn-3's quote, triggering deterministic `PARTIAL` -> `UNDETERMINED` fallback.
2. **L2 (Residual `BLOCKING` gap after purpose reset to `PROGRESS`):** Model returned `ENOUGH_FOR_PURPOSE` alongside a leftover `BLOCKING` gap for an unstarted item, caught by `rawInconsistentEnough` -> `UNDETERMINED`.
3. **L3 (`QA` `falseSufficient` without observed test outcome):** Author only stated a test scenario was executed without reporting any observed result; model returned `ENOUGH_FOR_PURPOSE` instead of `NEEDS_AUTHOR_INPUT` (`test_result.behavior`).
4. **L4 (`COMPLETION` `CONTRADICTORY` false negative):** Author reported runtime behavior directly opposite to a mandatory Task requirement; model returned `NEEDS_AUTHOR_INPUT` instead of `CONTRADICTORY`.
5. **L5 (`PROGRESS` raw `ENOUGH_FOR_PURPOSE` after `unknown` reply):** Runtime guard caught and downgraded to `UNDETERMINED`.
6. **L6 (Editor `REWRITE_PROTECTED_CONTENT_CHANGED`):** Model decoded a `__WN_PROTECTED_...__` marker; rejected by `restoreText`.
7. **L7 (Editor `REWRITE_INVALID_OUTPUT` on no-op edit):** Note required no changes; model returned identical `replacementText` and `changeSummary: []`, rejected by `parseAgentResult` requiring `changeSummary.length > 0`.

## 3. Approved Engineering Decisions (G1–G7 & Project Lead O1–O6)

- **G2 / D10a:** Accept `claim.text` as `FULL` when it is a unique contiguous clause-bounded literal substring of its cited `sourceRefs.quote` under strict NFC normalization, preserving all polarity, negation, condition, uncertainty, and adverse-outcome guards. Cross-source mismatched claims remain `PARTIAL` (O1: fail-safe parser + explicit citation rule in v26).
- **G3 / D2:** `validated-configs.json` warns (`validatedConfig: false`) while zero `PASS` entries exist for a surface, and blocks unvalidated `{model, architecture, promptVersion, providerPolicy}` combinations with `WORKNOTE_AGENT_UNAVAILABLE` once >= 1 `PASS` entry exists (O5: no silent model/config fallback).
- **G4 / D10b:** Allow `changeSummary: []` only when restored `replacementText` equals the original target under exact `\r\n`->`\n` + NFC normalization (`operation !== 'title'`); otherwise reject with `REWRITE_EMPTY_CHANGE_SUMMARY` (`INVALID_OUTPUT`, O4: no silent LLM retry).
- **G5 / D4:** Keep `cases-assessment-v5-release.json` immutable; author `cases-assessment-v6-release.json` with >= 12 `CONTRADICTORY` turns (O6: 60-case release shape) plus `cases-assessment-history-v1.json` with a dedicated history validator.
- **G6 / D3:** Generate purpose rubric prompt sections from `PURPOSE_RUBRIC_TABLE`; allow `history.conflict` as `BLOCKING` on `PROGRESS` only for genuine `SELF` conflicts with current anchor (O3: `PARENT`/`CHILD`/`LINKED` `DECISION` conflicts normalized to `OPTIONAL`, never `BLOCKING`).
- **G7 / D11:** Add `workflow` support (`TASK_NOTE`, `PROJECT_DOCUMENT`, `WORK_REPORT`) to rewrite evaluation harness and measure empirically before creating workflow-specific policies.

