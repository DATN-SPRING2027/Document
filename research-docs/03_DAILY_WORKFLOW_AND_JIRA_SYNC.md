# Continuum AI — Daily Work Capture and Internal Task Management

## Status and scope

- Status: Continuum Task Service is the canonical source for DATN task lifecycle. Its source code stays in the existing DATN_BE repository and its UI stays in DATN_FE; it is deployed as an independent NestJS service with its own logical MongoDB database `continuum_task`. Detailed task Use Cases and status/field values are in `Internal-Work-Management/12-continuum-task-management-use-cases.md` and remain under review.
- Date: 2026-10-01
- Scope: MVP for one software project with multiple teams.
- Authority: [MVP scope](01_MVP_SCOPE.md), [actors and permissions](02_ACTORS_ROLES_AND_PERMISSIONS.md).
- Filename note: This path is retained so existing references keep working; Jira task-source sync is not part of the current MVP.

## 1. Capture while work is happening

Every member, including Team Leaders, records work through the approved Work Note taxonomy. There are exactly three types:

- **Task Note**: a task-specific note, approach, or reason. `taskId` is required; each Task can have zero or more Task Notes.
- **Project Document**: project-level material such as an MVP, database design, RSR, specification, architecture note, or documentation. A Task is not required. The Leader reviews and approves it before it becomes approved knowledge.
- **Periodic Work Report**: a member's report of project work for one reporting period. The Leader configures a cadence of 1 day, 3 days, or 7 days (no more than one week). Reports require Leader review and approval.

There is no generic Project Work Note or unlinked manual Work Note type. Task metadata can provide context for a Task Note, but the member confirms its content and supplies what/how/why, blockers, next steps, and evidence.

| Field | Source | Required intent |
| --- | --- | --- |
| Task title/ID, status, assignee, due date, link | Internal Continuum Task | Identify the work and its current owner/state without copying a second task record; Mongo `ObjectId` remains canonical in the MVP. A Task Note must reference this Task. |
| What was done / outcome | Human confirms or edits | Record actual progress, not only task status. |
| How it was done: technique, commands, approach | Human | Capture tacit technical knowledge. |
| Why: trade-offs, decision, constraint | Human | Explain reasoning to the successor. |
| Blocker/risk, next step, person to ask | Human | Make unfinished work actionable. |
| Evidence (PR, commit, file, document) | Link through an authorized source or upload | Support verification and citation. |

Periodic report obligations and due reminders are generated from the project cadence and active membership, independently of whether a member opens the report page. The first eligible obligation is the cadence period containing or following the membership start; periods that ended before the member joined are skipped. Reminders are not a performance or time-tracking score. A handover summary can use eligible Task Notes, approved Project Documents, and internal task context, but a human reviews it before sharing.

## 2. Internal task-management direction

1. Continuum Task Service stores and owns the DATN task lifecycle. It runs independently from the other NestJS services but is implemented in the existing DATN_BE repository; the browser UI remains in DATN_FE and calls through its BFF/Gateway. Jira is not the task source, task-sync connector, or actor in the current task-management Use Cases.
2. Proposed relationship: each task belongs to one project and optionally one team within that project; multi-project and multi-team tasks are outside the MVP. Role/assignment checks are applied on each Task API operation.
3. The proposed P0 slice includes create/list/detail/edit, Team Leader assignment, fixed status changes, basic search/filter, Task Note integration (with required `taskId`), limited history and open-task context for handover. Kanban, task comments/files and dashboard/reporting are P1 or out of MVP. See `Internal-Work-Management/12-continuum-task-management-use-cases.md` for the decision proposals.
4. Users confirm Task Note content. Task status alone does not prove a procedure, root cause or decision is correct.
5. Task text and task status do not become verified Knowledge automatically. Knowledge proposals require evidence and scoped human review.
6. There is no Jira issue import, webhook sync, reconciliation or two-way task sync in this MVP. Any later Jira link/import is a separate decision and must not create a second writable source for the same task.
7. Only eligible Task Notes and Leader-approved Project Documents/Periodic Work Reports that pass Continuum authorization and source-eligibility checks may flow to SAG retrieval/indexing. Task records/status/assignment remain in MongoDB and are not standalone SAG sources.

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
- A linked internal task can provide context for a Task Note; the member supplies and confirms what/how/why and evidence. Every Task Note has one required logical `taskId`; a task may have many Task Notes.
- Task Notes do not copy the Task into SAG or replace canonical Task data.
- A member can create a Project Document without a Task and submit it to the Leader review workflow. Periodic Work Reports follow the configured 1/3/7-day cadence and the same Leader review/approval requirement.
- A task status transition records work progress but does not by itself create verified Knowledge.
- A handover shows authorized open tasks for the predecessor; a Team Leader reviews and assigns selected tasks/context to a scoped successor.
- SAG indexing accepts only eligible Task Notes and Leader-approved Project Documents/Periodic Work Reports authorized for the relevant scope; task title, description, status and assignee are not indexed as independent sources. Current ACL is checked before retrieval/context construction; revoked sources are blocked immediately and de-indexed asynchronously.
- A successor or member outside the project/team/assignment scope cannot view tasks or linked evidence through search, notes, handover or chat.
- No Jira account, project, webhook, credential or Jira availability is required for task creation, update, capture or handover.
- An unsupported chat question produces an insufficient-evidence response and can become a gap.
- Any authenticated User with `ACTIVE` Organization Membership in the trusted matching Organization Context may create a `PRIVATE` Project. The creator receives an active Project Membership and a Project-scoped `TEAM_LEADER` RoleAssignment in the same transaction; no Organization role or `project.create` grant is required. This follows the accepted BE Project Foundation decisions.

## 6. Deferred work

Jira integration, external task import, GitHub/Drive/Confluence connectors, generic connector administration, configurable workflows, Kanban board, comments, attachments, mentions, watchers, advanced search, automation, dashboards and reporting are outside the current task P0 MVP. Add any external source only after a separate scope and permission decision; Continuum remains canonical for DATN task lifecycle.

Automated interview, interview-to-knowledge, advanced freshness/conflict detection, incident memory and automatic transfer analysis remain follow-up candidates. The evaluation dataset and permission-leak tests are not deferred.
