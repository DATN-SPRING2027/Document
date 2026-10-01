# ManageWork Codebase Assessment for DATN Task Management

**Status:** Draft for team review. This assessment records repository evidence and a delivery proposal; it does not approve a product-scope or architecture change.

**Evidence date:** 2026-10-01.

**Reviewed snapshots:** `ManageWork@748520c`, `DATN_BE@f5530d8`, `DATN_FE@c57c014`; each checkout was clean on `main` when inspected.
**Purpose:** Answer whether ManageWork already contains a Jira-like task-management implementation, how it compares with DATN, and what could reasonably fit into the remaining six weeks.

## Executive Summary

- `[OBSERVED]` ManageWork contains a real task-management slice: authenticated task APIs, task/project views, Kanban/week/month UI, status and priority, assignees and dates, comments, subtasks, dependencies, tags, time tracking, attachments, recurring tasks, activity, and notifications. This is evidence that code exists; it is not a production-readiness or end-to-end quality certification.
- `[OBSERVED]` DATN does not currently expose an internal task-management feature. Its Jira and Capture backend controllers reviewed here expose health endpoints only. The frontend has daily work-note query/mutation hooks and an optional Jira issue key, but no task board, task CRUD pages, or task API integration was found in the reviewed source.
- `[OBSERVED]` ManageWork is not a drop-in match for DATN. ManageWork uses Express/JavaScript, PostgreSQL, React/Vite, and React Router. DATN uses NestJS/TypeScript, MongoDB/Mongoose, and Next.js/React. ManageWork is useful as a behavior and UX reference; DATN implementation should follow the existing DATN stack and authorization model.
- `[PROPOSAL]` With six weeks left, target a deliberately small task-management slice, not Jira feature parity. A project-scoped task list, basic task lifecycle, assignee, priority/due date, limited change history, filters, work-note linking, and a handover view of open tasks would be a plausible ceiling if other scope is reduced accordingly. A simple Kanban board is optional if time allows.
- `[DECIDED — 2026-10-01]` The user confirmed that Continuum will own DATN task management and Jira will not be the task source. The detailed use case, status and field set remains under review in `12-continuum-task-management-use-cases.md`.

## Evidence and Scope

This is a codebase inventory based on the snapshots listed above. It identifies routes, UI modules, and schemas present in source. It does not establish that every path is currently reachable in a deployed environment, that all flows work together, or that performance/security requirements have been met. No tests or migrations were run as part of this read-only assessment.

Repository references below are relative to each named checkout:

- `ManageWork`: `my-fullstack-app/backend/...` and `my-fullstack-app/frontend/...`
- `DATN_BE`: `src/services/...`
- `DATN_FE`: `src/lib/...`

## ManageWork Task-Management Inventory

| Capability | Evidence in `ManageWork@748520c` | Assessment |
|---|---|---|
| Task create/read/update/delete, search, status update, reorder | `my-fullstack-app/backend/src/modules/tasks/task.routes.js`, `task.controller.js`, `task.model.js`, `task.validation.js` | Core task API is present and guarded by auth middleware and request validation on the main routes. |
| Task board and calendar views | `my-fullstack-app/frontend/src/pages/tasks/MyTasks.jsx`, `features/calendar/KanBanView.jsx`, `WeekView.jsx`, `MonthView.jsx` | UI supports a Kanban default plus week/month views, search, filtering, and status/reorder actions. |
| Task attributes | `task.validation.js`, `task.model.js`, `backend/src/shared/migrations/001_init_schema.sql` | Title, description, status, priority, dates, project, creator/assignee, recurring metadata, and order are represented. Statuses include `todo`, `in_progress`, `review`, `on_hold`, `done`, `cancelled`; priorities include `low`, `medium`, `high`, `urgent`. |
| Task detail and collaboration | `frontend/src/features/tasks/TaskDetail.jsx`, `TaskComments.jsx`, `TaskActivity.jsx`, backend `comment.routes.js`, `activity/` | Comment and activity-related modules exist. |
| Subtasks and dependencies | backend `subtask.routes.js`, `task_dependency.routes.js`; frontend `SubtaskList.jsx`, `DependencyManager.jsx` | Separate APIs and UI components are present. |
| Tags, time logs, files | backend `tag.routes.js`, `time-tracking/timeEntry.routes.js`; frontend `TagManager.jsx`, `TimeLog.jsx`, `AttachmentManager.jsx` | Feature modules exist; this inventory does not verify storage, permission edge cases, or operational behavior. |
| Recurrence, templates, notifications | backend `tasks/models/recurringTask.model.js`, `tasks/automation.service.js`, `notifications/`; frontend `TaskTemplates.jsx`, recurrence components | Supporting modules/components are present. Their full workflow coverage was not audited. |

No implementation for epics, sprint planning, story points, release management, or configurable workflows was found in the reviewed task routes/UI. Treat these as unverified or absent from the inspected task scope, not as a claim about every file in the repository.

### Quality and Maintenance Caveats

- The ManageWork backend `package.json` test command is a placeholder that exits with an error; the frontend package has no test script. The code inventory therefore does not demonstrate automated task-module coverage.
- ManageWork's `backend/src/shared/migrations/001_init_schema.sql` begins by dropping existing tables, including `tasks`, `projects`, and related tables. **Do not run or copy this initializer into DATN.** It is destructive and belongs only to its own setup context.
- The task feature spans many modules. Reusing individual patterns is more realistic than porting the application wholesale.

## Stack Compatibility

| Layer | ManageWork | DATN | Implication |
|---|---|---|---|
| Backend | Express 5, JavaScript, PostgreSQL via `pg`, Redis, JWT, Socket.IO | NestJS 11, TypeScript, MongoDB/Mongoose, Redis/BullMQ | Port task behavior into Nest modules/services/DTOs and the DATN persistence/auth patterns. Do not adopt the PostgreSQL schema by default. |
| Frontend | React 18, Vite, React Router, JavaScript, Zustand 4, Tailwind 4 | Next.js 16 App Router, React 19, TypeScript, Tailwind 4, TailAdmin, TanStack Query, Zustand 5 | Recreate the necessary interaction in existing Next.js routes/components and use current API/query conventions. |
| Reusable value | Domain fields, route/use-case examples, board/detail interaction patterns | Existing product architecture and shared components | Reuse as a design reference after mapping behavior to DATN actors, project/team scope, and permissions. |

The matching use of React and Tailwind does not make ManageWork components directly reusable: routing, language, state, UI conventions, data contracts, and backend persistence differ. A wholesale copy would introduce a parallel architecture and duplicate product decisions.

## DATN Current-State Gap

At `DATN_BE@f5530d8`, `src/services/jira/controllers/jira.controller.ts` and `src/services/capture/controllers/capture.controller.ts` each expose a `health` GET/message handler only. Schemas, modules, queues, and persistence scaffolding elsewhere in these services do not establish task CRUD or a Jira sync flow.

At `DATN_FE@c57c014`, `src/lib/queries/capture/useCapture.ts` provides daily work-note reads and saves, with `jiraIssueKey` as an optional field. The reviewed FE source contains no task board or task lifecycle page/API integration.

This leaves a distinction for product scope:

1. The earlier baseline referenced Jira issue/comment/status sync. The user selected Continuum Task API + MongoDB as canonical; ADR-009 and the affected MVP, workflow, Tech, Architecture and database-design documents now reflect that decision.
2. Building an internal task system is a larger capability than storing a Jira issue key on a work note; the reviewed use case proposal therefore constrains it to capture and handover needs.
3. The remaining decisions are the detailed P0/P1 use cases, exact fields/statuses and any Kanban requirement, not whether Jira remains task-authoritative.

## Candidate Six-Week Slice

`[PROPOSAL]` Constrain the first internal task release to supporting the DATN project and its knowledge/handover flow. This schedule assumes a small team and that competing work is explicitly cut or deferred; it is not a commitment that full Jira parity fits in six weeks.

| Week | Candidate outcome |
|---|---|
| 1 | Confirm the remaining P0 use cases, task/project/team relationship, task permissions, status/field set, API contract, and fit with the accepted MVP. Continuum ownership and MongoDB persistence are already decided. Produce a reviewed schema/API proposal before implementation. |
| 2 | Implement the approved task persistence change and any required new migration/backfill on a fresh database branch/PR. Review and merge the DB contract before dependent application work. |
| 3 | On a fresh backend branch from updated `main`, implement project-scoped create/list/detail/update/status/assignment APIs using DATN conventions, scoped authorization, and validation. |
| 4 | On a fresh frontend branch from updated `main`, implement the task list/detail with create/edit, status changes, loading/empty/error states, and core filters. Add a simple Kanban board only if capacity remains. |
| 5 | Integrate BE/FE, connect work notes to internal tasks, show open tasks during handover, and add limited change history. Add representative automated checks and fix cross-module issues. |
| 6 | Stabilize the complete demo path and permissions, run required BE/FE checks, update MVP/spec docs, and prepare final project evidence. Defer secondary features if the core flow is unstable. |

This sequence follows the DATN workflow for separate database, backend, and frontend branches/PRs. Review and merge time is a schedule dependency; if it consumes the integration window, reduce the feature slice rather than combining the deliverables into one branch.

### Suggested First-Release Boundary

**Include:** project-scoped tasks; title/description; small fixed status and priority sets; assignee; due date; task list; create/edit/detail; status transition; search/filter by project, status, assignee, and due date; task-to-work-note link; open-task context in handover; limited change history; authorization appropriate to DATN. A simple task identifier and Kanban view are optional design choices.

**Defer unless required by the validated use case:** configurable workflows, sprints/epics/roadmaps, dependency graph, recurring tasks, templates, time tracking, rich attachments, automation builder, advanced notifications, realtime collaboration, analytics dashboards, and broad Jira import/migration.

Comments and activity should be treated as separate choices: add them only if task handover/context continuity needs them and there is enough time to secure and validate access correctly.

## Product Decisions to Resolve

1. **Task scope:** The internal source decision is recorded; review the P0/P1 list, exact fields/statuses and Kanban priority in `12-continuum-task-management-use-cases.md`.
2. **Entity ownership:** Confirm whether each task belongs to one project and optionally a team, and how it relates to Work Notes, knowledge records and handover items.
3. **Authorization/audit:** Confirm which project/team actors can create, assign, view, edit, transition or cancel tasks and which changes are shown in task history.
4. **Delivery scope:** Six weeks supports a constrained task flow, not broad Jira parity. Reduce other deliverables explicitly if required.
5. **Technical alignment:** ADR-009 and the affected Tech, Architecture, workflow, and database-design documents record Continuum Task API + MongoDB as canonical, with Jira task sync out of MVP. Field-level schema/API, permission approval, transaction/history details and source/deployment verification for the accepted LanceDB target still need completion before implementation.

## Recommendation

`[PROPOSAL]` Use ManageWork to learn from its task lifecycle, Kanban interactions, task detail, and supporting feature boundaries. Keep DATN's NestJS/TypeScript + MongoDB and Next.js/TypeScript + TailAdmin architecture. The task-source decision is now internal Continuum Task; define a narrow, project-scoped contract from the pending Use Case review. For a six-week deadline, prioritize a reliable task lifecycle that directly supports capture and handover; defer Jira-scale planning, configurability, automation, and collaboration features.

The internal task-source direction and cross-document boundary are recorded. Before implementation, finish the detailed Use Case review and approve the Task API/field-level schema, permissions and history contract. LanceDB is the accepted SAG retrieval target for MVP (DEC-015/SPEC-005); verify actual SAG source/deployment integration. PostgreSQL + pgvector/Qdrant material is an alternative/future-scale design, not an unresolved engine choice.

## Database, Configuration, and Security Impact

This document change has no database, runtime configuration, secret, or application-code impact. Any eventual task schema/model/collection/field/index/reference change is a database change under DATN workflow and requires its own database branch/PR, backward-compatibility review, migration/data plan, and rollback considerations. No ManageWork migration should be executed against DATN.

## Sources Reviewed

- `ManageWork@748520c`: task routes/validation/model, subtask/dependency/comment/tag/time-tracking/activity/notification modules, task UI, package manifests, and SQL schema/migrations.
- `DATN_BE@f5530d8`: Jira and Capture service controllers/modules and backend manifest.
- `DATN_FE@c57c014`: capture query hooks and frontend manifest.
- `Document`: `research-docs/01_MVP_SCOPE.md`, `research-docs/Internal-Work-Management/10-master-strategic-research.md`, workspace/repository workflow instructions.
