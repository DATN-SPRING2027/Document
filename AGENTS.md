# DATN workspace instructions

## Project identity

This workspace belongs to the **DATN project**. It is not the TAMI ERP project.
Do not infer TAMI business domains, repositories, modules, architecture, paths,
database choices, UI libraries, API contracts, or naming conventions.

Some initial documents were copied from another project as workflow reference.
Project-specific statements from that source are not authoritative for DATN.
Only the current DATN source code, specifications, ADRs, and explicit user
instructions may define this project's architecture and behavior.

## Mandatory AI workflow

Before starting any task, read and follow
[`AI_WORKFLOW.md`](AI_WORKFLOW.md). It is the canonical workflow for Codex,
Antigravity/Gemini, Claude, Copilot, and other coding agents in this project.

The following rules are non-negotiable:

- Create a fresh branch for every task directly from the latest `origin/main`.
  Never code directly on `main`, and never reuse a completed branch.
- Keep database, backend, and frontend changes in separate branches and PRs.
  Entity/schema plus its new migration belong together in the DB PR.
- Never edit a historical migration. Assess existing data and add a new,
  idempotent migration/data script when required.
- AI may run `git push` for the current task branch after the intended files are
  verified and committed. Never push directly or force-push to `main`, approve,
  merge, auto-merge, or bypass branch protection.
- Target feature PRs only to `main`; return the PR URL for Jira and prepare the
  required team notification for every database change.
- Follow the verified DATN architecture, reuse before creating, validate
  untrusted input, protect secrets, and verify affected behavior before handoff.
- If `origin/main`, the task owner/name, or another required Git prerequisite is
  missing, stop before editing and report it. Do not invent a replacement.

Every handoff must state the current branch/base, changed scope, checks and
results, database/migration/data impact, commit and push status, confirmation
that no merge occurred, and the remaining PR/Jira/notification steps.

## Source-of-truth policy

`Document/` is currently the documentation repository for DATN. Application
repository names and backend/frontend boundaries are not declared by this file.
Before implementing application code, inspect the actual workspace and identify
the relevant repository from its own source, README, package/build files, local
`AGENTS.md`, and architecture documents.

- Do not invent repository paths or reuse paths from another project.
- Do not treat examples in workflow documents as the current implementation.
- When historical text conflicts with current DATN source, current production
  source and accepted DATN decisions take precedence.
- If two current DATN sources conflict, report the conflict and request a
  decision before changing behavior.

## Skill selection

Automatically select the smallest relevant installed skill for the request.
The user does not need to invoke a skill by name.

Prefer, when applicable:

- spec-driven-development and planning-and-task-breakdown for new or unclear
  features;
- frontend-ui-engineering for user-interface work;
- api-and-interface-design for public contracts and integrations;
- test-driven-development for behavior changes and bug fixes;
- browser-testing-with-devtools for browser runtime validation;
- find-docs for current framework/library documentation;
- code-review-and-quality and security-and-hardening before completion;
- the relevant repository or GitHub tooling for issues, PRs and CI.

Do not activate every skill for every task. Use only what the task requires.

## Architecture and technology rules

The approved proposal currently selects React, TypeScript and Vite for the
frontend; NestJS and TypeScript for the backend; and MongoDB with Mongoose as
the primary database. Agents must still verify the initialized DATN source and
report any conflict before making technology-specific changes.

- Follow the closest maintained production feature and its tests.
- Reuse existing components, services, schemas, DTOs, types and utilities before
  creating alternatives.
- Do not introduce a parallel architecture or dependency without a documented
  reason and the required approval.
- Apply MongoDB/Mongoose, Node.js, NestJS, React/Vite and TailAdmin guidance in
  line with the approved proposal and the actual DATN source.
- Record significant architecture decisions in the repository's established ADR
  format; do not import architecture decisions from TAMI or another project.

## Mandatory post-implementation review gate

After completing implementation intended for a pull request and running the
relevant checks, invoke the `code-review-and-quality` skill against the final
local diff or open PR before treating it as review-ready.

- Review correctness, tests, readability, verified DATN architecture, security,
  performance, migration/data impact and unintended scope changes as relevant.
- Report findings with severity, evidence, affected file/line and proposed fix.
- Stop after reporting review findings. Do not implement review-driven fixes,
  push, resolve comments or merge until the user explicitly approves the fixes.
- After approved fixes, rerun affected checks and review the resulting diff.
