# Continuum AI — Daily Work Capture and Internal Task Management

## Status and scope

- Status: Continuum Task Service is the canonical source for DATN task lifecycle. Its source code stays in the existing DATN_BE repository and its UI stays in DATN_FE; it is deployed as an independent NestJS service with its own logical MongoDB database `continuum_task`. Detailed task Use Cases and status/field values are in `Internal-Work-Management/12-continuum-task-management-use-cases.md` and remain under review.
- Date: 2026-10-01
- Scope: MVP for one software project with multiple teams.
- Authority: [MVP scope](01_MVP_SCOPE.md), [actors and permissions](02_ACTORS_ROLES_AND_PERMISSIONS.md).
- Filename note: This path is retained so existing references keep working; Jira task-source sync is not part of the current MVP.

## 1. Capture while work is happening

Every member, including Team Leaders, records lightweight knowledge during normal work. Manual capture remains available. A member may optionally link a Work Note to an internal Continuum task; the task provides work context but is not a substitute for what the person learned.

| Field | Source | Required intent |
| --- | --- | --- |
| Task title/ID, status, assignee, due date, link | Internal Continuum Task when selected | Identify the work and its current owner/state without copying a second task record; Mongo `ObjectId` remains canonical in the MVP. |
| What was done / outcome | Human confirms or edits | Record actual progress, not only task status. |
| How it was done: technique, commands, approach | Human | Capture tacit technical knowledge. |
| Why: trade-offs, decision, constraint | Human | Explain reasoning to the successor. |
| Blocker/risk, next step, person to ask | Human | Make unfinished work actionable. |
| Evidence (PR, commit, file, document) | Link through an authorized source or upload | Support verification and citation. |

Work Notes remain available without a task link. A reminder follows up on missing required notes/knowledge and can be snoozed or explained; it is not a performance or time-tracking score. A handover summary can use confirmed Work Notes and internal task context, but a human reviews it before sharing.

## 2. Internal task-management direction

1. Continuum Task Service stores and owns the DATN task lifecycle. It runs independently from the other NestJS services but is implemented in the existing DATN_BE repository; the browser UI remains in DATN_FE and calls through its BFF/Gateway. Jira is not the task source, task-sync connector, or actor in the current task-management Use Cases.
2. Proposed relationship: each task belongs to one project and optionally one team within that project; multi-project and multi-team tasks are outside the MVP. Role/assignment checks are applied on each Task API operation.
3. The proposed P0 slice includes create/list/detail/edit, Team Leader assignment, fixed status changes, basic search/filter, optional Work Note link, limited history and open-task context for handover. Kanban, task comments/files and dashboard/reporting are P1 or out of MVP. See `Internal-Work-Management/12-continuum-task-management-use-cases.md` for the decision proposals.
4. Users confirm Work Note content. Task status alone does not prove a procedure, root cause or decision is correct.
5. Task text and task status do not become verified Knowledge automatically. Knowledge proposals require evidence and scoped human review.
6. There is no Jira issue import, webhook sync, reconciliation or two-way task sync in this MVP. Any later Jira link/import is a separate decision and must not create a second writable source for the same task.
7. Only Work Notes/evidence that pass Continuum authorization and source-eligibility checks may flow to SAG retrieval/indexing. Task records/status/assignment remain in MongoDB and are not standalone SAG sources.

## 3. Handover path

1. A Team Leader starts a handover for a departing/transferring member or responsibility.
2. Continuum retrieves internal tasks in the affected project/team that are owned by that member, especially tasks that are not complete.
3. The Team Leader reviews the tasks returned by the Continuum Task API and chooses which tasks, linked Work Notes, permitted evidence and unresolved questions belong in the handover package; the system does not choose or assign tasks autonomously.
4. The authorized Team Leader assigns selected tasks to a scoped `SUCCESSOR` assignment. The Task API updates the task's canonical assignee to that successor; Handover stores `taskId`, recipient and acknowledgement state, not a mutable copy of task data. The successor sees only selected tasks and knowledge authorized for that handover/project/team scope.
5. The successor asks the cited assistant about the handover; the assistant distinguishes task status from verified knowledge and reports missing evidence/gaps.

Only `TODO`, `IN_PROGRESS` and `BLOCKED` tasks are assignment candidates by default. Completed tasks can be referenced as read-only context through eligible Work Notes/evidence but are not reassigned. The successor acknowledges the handover package; this does not create a second assignee field that can diverge from the Task API. Assignment/retry coordination uses an idempotent operation ID because Task and Handover own separate persistence boundaries.

The existing handover workflow remains the owner of readiness, successor questions and completion approval. The Task Service supplies work state and ownership; it does not replace the handover lifecycle.

## 4. Document and chat path

Manual upload supports PDF, DOCX, Markdown, TXT and images. Originals live in private Cloudflare R2 first; S3-compatible storage is an adapter/fallback, not a second mandatory deployment. MongoDB stores source metadata, ACL, checksum, object key and versions. Processing parses text, runs OCR where needed, chunks it and maps source versions/chunks to SAG's Event–Entity retrieval index. A failed job retains the original file and exposes retry state.

The core successor experience is an evidence-grounded chat over authorized, verified knowledge and permitted source material. Each answer shows traceable source/chunk, verification status and date. When evidence is inadequate, the assistant says so and offers a Knowledge Gap instead of guessing. Chat history must respect ACL changes; saved answers are not a permanent access grant.

## 5. Acceptance examples

- A member creates or updates an internal task within their permitted project/team scope and later finds it by basic search/filter.
- A linked internal task can prefill task context in a Work Note; the member supplies and confirms what/how/why and evidence. A Work Note links to zero or one task; a task may have many Work Notes.
- A task-linked Work Note stores only an optional logical `taskId` reference; it does not copy the task into SAG or replace canonical task data.
- A member can submit an unlinked manual Work Note when no task exists or linking is not useful.
- A task status transition records work progress but does not by itself create verified Knowledge.
- A handover shows authorized open tasks for the predecessor; a Team Leader reviews and assigns selected tasks/context to a scoped successor.
- SAG indexing accepts only author-confirmed Work Notes/evidence authorized for the relevant scope; task title, description, status and assignee are not indexed as independent sources. Current ACL is checked before retrieval/context construction; revoked sources are blocked immediately and de-indexed asynchronously.
- A successor or member outside the project/team/assignment scope cannot view tasks or linked evidence through search, notes, handover or chat.
- No Jira account, project, webhook, credential or Jira availability is required for task creation, update, capture or handover.
- An unsupported chat question produces an insufficient-evidence response and can become a gap.
- When a Team Leader requests a new project without `project.create`, the backend denies it; an Admin grant enables it only inside the granted organization and validity period.

## 6. Deferred work

Jira integration, external task import, GitHub/Drive/Confluence connectors, generic connector administration, configurable workflows, Kanban board, comments, attachments, mentions, watchers, advanced search, automation, dashboards and reporting are outside the current task P0 MVP. Add any external source only after a separate scope and permission decision; Continuum remains canonical for DATN task lifecycle.

Automated interview, interview-to-knowledge, advanced freshness/conflict detection, incident memory and automatic transfer analysis remain follow-up candidates. The evaluation dataset and permission-leak tests are not deferred.
