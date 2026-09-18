# SKILL.md — DATN project index

This file is the workspace-level index for AI agents working on DATN. Read it
before starting work, then load only the skills relevant to the task.

## Mandatory workflow entry point

Read and apply [`AI_WORKFLOW.md`](AI_WORKFLOW.md) before every task. In
particular: create one new branch per task from the latest `origin/main`; keep
DB/BE/FE work in separate branches and PRs; never modify an old migration;
push only the verified, committed current task branch; never push directly or
force-push to `main`, approve, or merge; target feature PRs to `main`; link
the PR in Jira; notify the team about database changes; and complete the
required verification and handoff checklist. These project rules override a
generic Git recommendation when they conflict.

## Project identity and available boundary

```text
F:\LEARN KÌ 8\ĐATN\
└── Document\               # DATN documentation repository
```

This is a new DATN project, not TAMI ERP. Backend and frontend repository names,
business modules, frameworks, database technology and production architecture
are not defined in this index. Discover them from the actual DATN workspace and
its current documentation before implementing code. Never copy or infer TAMI
paths, domains, source maps or API contracts.

## Source-of-truth rules

1. `Document/` is the canonical location currently available for DATN workflow,
   requirements, research, specifications and architecture notes.
2. Current DATN production source and accepted decisions override copied or
   historical examples.
3. A workflow example does not establish the DATN technology stack.
4. Do not invent missing backend/frontend repository names or directory layouts.
5. When an application repository is added, follow its local `AGENTS.md`, README,
   build configuration, architecture documents and maintained source patterns.

## Skill routing

Use installed skills according to the current task rather than assuming a
project-specific legacy skill exists:

- UI/page/component work: `frontend-ui-engineering`.
- API or public type contract: `api-and-interface-design`.
- Behavior change or bug fix: `test-driven-development`.
- Git/branch/PR workflow: `git-workflow-and-versioning`.
- Documentation or architecture decisions: `documentation-and-adrs`.
- Current framework/library behavior: `find-docs`.
- Final change review: `code-review-and-quality`.
- Security-sensitive code: `security-and-hardening`.

Use the minimum set needed for the request.

## Non-negotiable delivery rules

1. Read current DATN documentation and source before changing implementation.
2. Keep one focused concern per branch, PR and commit.
3. Do not add packages without a clear reason and required approval.
4. Reuse current contracts and abstractions instead of redefining them.
5. Run the relevant tests, typecheck/build, lint and formatting checks.
6. Do not silently stage, modify or overwrite unrelated work.
7. Push only the verified, committed current task branch. Never push directly
   or force-push to `main`, approve, merge, auto-merge, or bypass protection.
