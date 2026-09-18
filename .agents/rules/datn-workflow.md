# DATN mandatory workflow

This workspace belongs to DATN, not TAMI ERP. Never infer TAMI repositories,
domains, modules, architecture, paths or technology choices.

Always read and follow `/AI_WORKFLOW.md` and `/AGENTS.md` before editing.

- One new task means one new branch created from the latest `origin/main`.
- Never work directly on `main`.
- Separate database, backend, and frontend work into dedicated branches/PRs.
- Treat every schema/model/migration/index/data change as a database change.
- Never edit a historical migration; add a new migration or idempotent data
  script and prepare the required team notification.
- Push only the verified, committed current task branch. Never push directly or
  force-push to `main`, approve, merge, auto-merge, or bypass protection.
- Open feature PRs only into `main`, then hand the PR URL back for Jira.
- Follow the verified DATN production architecture; reuse before creating.
- Apply framework/database/UI-specific guidance only after confirming DATN uses
  that technology.
- Validate untrusted input, protect secrets, and verify affected behavior.
- Report the required handoff checklist from `AI_WORKFLOW.md`.

If `origin/main` or required task identity is unavailable, stop before editing
and report the blocker. Do not invent a base branch, owner, Jira ticket,
reviewer, repository path or application architecture.
