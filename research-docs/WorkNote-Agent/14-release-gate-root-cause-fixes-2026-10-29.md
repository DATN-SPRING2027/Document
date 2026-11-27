# WorkNote assessment: release-gate root causes and fixes

Date: 2026-10-29. Authority: the user requested investigation and fixes for the
unresolved gap classification, repeated questions and requirement-extraction
failures. This continues the unfinished BE/DOC assessment package, draft PRs109
and67. It does not authorize shared activation, merge or Atlas migration.

## Findings and implementation

| Root cause | Repair | Regression evidence |
|---|---|---|
| Promptv9 mostly described SCOPE/RESULT; IMPLEMENTATION/EVIDENCE boundaries were underspecified. | Promptv12 defines all six gap kinds, precedence and contrasting examples. Missing configuration selection is IMPLEMENTATION; context/results supporting a completion or test claim are EVIDENCE. | Live timezonev10/v11 and permissionv12 questions use the expected types. |
| An answered reply containing “no new information” was treated as novel author input; dropping its gap could falsely resolve it. | A narrow whole-reply classifier marks it as no new information, excludes it from progress and retains the gap as unknown. The original answer/disposition remains unchanged. | Failing-then-passing state regression; live permissionv12 turn2 has no question and noProgress1. |
| Gap identity included model classification, allowing kind changes to bypass the answer ledger. | Identity uses owner, normalized target and grounded non-answer anchors. Existing IDs are reused when matching prior gaps; different entities/anchors stay distinct. Requests include an explicit no-repeat ledger. | Regression changes kind and word order; existing auth/billing separation tests still pass. |
| The model paraphrased requirement.text despite the strict extractive protocol. | Server supplies exact authorized Task passages as extraction aids. Prompt copies the same passage into text/quote; compound criteria stay intact. Strict rejection of paraphrases and invented quotes is preserved. | The original malformed CSV output stays rejected; new CSVv12 turns parse and pass. |
| Completion fallback overwrote CONTRADICTORY with UNDETERMINED. | Explicit source-contradiction adequacy survives incomplete completion coverage. | State regression and live releasev12 turn2 remain contradiction/CONTRADICTORY with no automatic question. |
| A Task expectation not met was treated as contradictory author reports, preventing incident editing even when purpose adequacy was enough. | Coverage mismatch alone no longer selects the source-contradiction state. Explicit contradictory adequacy/unresolved contradiction gaps still stop the flow. | CSVv12 turn2 reaches ready_to_edit; its Editor proposal passes runtime guards. |
| Model confused claims.supportRelation and coverage.status enum vocabularies. | Separate enum instructions and a two-source contradiction example; each literal author statement can be FULL for provenance while the statements conflict overall. | v10/v11 failures preserved; v12 release parses without alias recovery. |
| Editor instruction asked for attribution/time without an author-provided timestamp. One output also used an empty message. | Editorv3 requires a nonempty message and prohibits invented dates. A narrow code guard rejects new ISO/slash dates absent from author inputs. | Invented-date regression fails before repair; actual author dates remain accepted. |
| Rubric excluded build/smoke terms present in the Task; its contradiction turn required another automatic question. | Versioned development-only errata adds those Task terms and aligns contradiction questioning with the approved stop policy. Wrong-gap expectations remain strict. | Unrelated questions still fail. Base corpus, splits and historical reports are untouched. |
| Runtime rubric checked adequacy/question but missed an adequate result whose state blocked rewrite. | Runtime grading now also checks rewrite availability and preservation of contradiction state. | Historical v11 CSV state discrepancy is explicitly recorded, not reclassified as a historical pass. |
| Cumulative budget rejection was normalized to a provider network error. | Preserve local phase-budget denial before HTTP in the evaluator. | Mock network remains uncalled after exhaustion; historical v12 Editor error is retained with a separate explanation. |

Later grounded correction can resolve a formerly unknown NOTE_AUTHOR gap only
when it targets that gap or supports all completion criteria; unrelated or
incomplete input cannot clear it. A note-author correction cannot resolve
TASK_REQUIREMENT_OWNER gaps. Original unknown/skipped answers are retained in
the private draft, not rewritten as successful facts.

The no-information classifier, gap fingerprints, quote/polarity and date guards
are conservative checks, not a general semantic verifier. Arbitrary paraphrases
and unsupported reasoning still require review. Question3/no-progress2 limits,
manual Apply/Save, private24h retention and authorization/CAS/lease checks remain.
No HTTP/storage schema, database migration, frontend file or dependency changed.

## Live development regression results

A new bounded phase was disclosed before calls. Phase gate-fix-20261029 used
exactly29 HTTP attempts,235158 reported tokens, zero unknown-usage attempts and
zero remaining calls. No exhausted ledger was reset. Previous phases remain
29/73953 and29/111387 calls/tokens. Across all three phases:87 calls/420498
reported tokens. Monetary cost is NOT_ESTABLISHED.

| Version | Actual HTTP | Analysis rubric passes | Editor proposals accepted |
|---|---:|---:|---:|
| v10 / Editorv2 |10|6/8 raw;6/8 recorded runtime|1/2 actual responses|
| v11 / Editorv3 |11|8/9 raw;8/9 recorded runtime*|2/2 actual responses|
| v12 / Editorv3 |8|7/7 raw and runtime|1/1 actual response|

*The v11 CSV adequacy passed but its contradiction state blocked rewrite. This
was a runtime-grader blind spot, now repaired; the recorded report is unchanged.

Finalv12 covers three repeated development scenarios: CSV2 turns, release2 turns,
permission3 turns. CSV reaches ready_to_edit; release stops in contradiction;
permission stops asking after no new information and becomes ready_to_edit after
a grounded correction. Timezone passed onv10 andv11; it was not rerun onv12.
The final permission Editor request was rejected before HTTP at the cumulative
budget cap. Its old XKIRO_NETWORK_ERROR label is explained separately and was
reproduced/fixed offline; no live retry occurred after exhaustion.

BE scripts/work-note-agent/assessment-gate-fix-2026-10-29.json records artifact
names, SHA256 hashes, original grades, state snapshots, versions and limitations.
Ignored .worknote-agent-evals contains synthetic raw reports and blank review
worksheets. Prompt examples were developed on development cases; no unseen
validation/holdout or full72 live run was performed. These results are not an
independent estimate of all-task accuracy.

Release gate remains NOT_PASSED and reviewerSemanticAssessment remains
NOT_ESTABLISHED. Both feature flags stay disabled by default. Independent semantic
review and frozen unseen evaluation are still required before shared activation.

## Delivery and verification

BE branch feat/DanhDEV-worknote-task-assessment-be-api continues from its existing
main base f41b57b; origin/main advanced to a856d9c during this follow-up. No unrelated
main changes were merged into this repair. DOC branch
docs/DanhDEV-worknote-task-assessment has base d9aa106. PR targets remain main.
Jira ID is still deferred by the user. No merge or team/Jira message is performed.

Final BE npm run check passed lint, typecheck, build,1712 unit tests (137 skipped)
and169 e2e tests (4 skipped). The focused assessment suite passed129 tests. Tests
first reproduced the affected failures before repairs; original red logs remain
local. The read-only final diff review found no further actionable introduced
defect after the owner-boundary and runtime-grader fixes. This is a self-review,
not independent semantic approval. Existing repository warnings remain outside
this repair's scope.

Backend and documentation changes are committed and pushed on the existing draft
branches at handoff. Companion FE/DB packages remain unchanged. No API server or
shared environment was activated by these changes. PR/Jira/reviewer follow-up
remains manual; the user will supply the Jira reference.
