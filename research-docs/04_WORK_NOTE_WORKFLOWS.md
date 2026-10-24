# Work Note workflows

## Status and boundaries

Implementation is split across `DATN_BE`, `DATN_FE-main`, and this documentation repository. The BE implementation uses the Capture service and Gateway; the FE calls the project-scoped API through the application API client. MongoDB stores operational content in the Capture service database. This document describes the delivered scope as of 2026-10-24.

The three records have separate workflows and authorization rules. General unlinked daily notes, document file uploads, a notification center, and changes to SAG retrieval are not part of this implementation.

## Task Note

- Scope: an existing Task in the same Project. The Task Note API verifies the task through the Task API and stores only its task reference and structured note content.
- Content: title, accomplishments, approach, and reason. A Task Note is confirmed when created; no Leader review is required.
- Access: active Project members with access to the Task can read it. The API checks Project and Task scope on every list/detail/create operation.
- Knowledge: Task Notes do not automatically enter official AI knowledge.
- API: `GET|POST /api/v1/capture/projects/{projectId}/tasks/{taskId}/notes`; `GET .../notes/{noteId}`. Project-wide Task Note listing is `GET .../work-notes`.

## Project Document

- Scope: the Project, with optional Task association. Document types include MVP, database design, RSR, architecture, API specification, research, requirement, design, technical specification, and other.
- Lifecycle: `DRAFT` → `PENDING_REVIEW` → `APPROVED`, `CHANGES_REQUESTED`, or `REJECTED`; approved documents may be archived. Editing an approved or rejected document creates a new version while retaining prior content and review history.
- Permissions: members create/edit their documents and submit them. A project role with review/configuration authority reviews documents. The BE checks that authority; FE permissions are only presentation hints.
- Storage: structured text content and version metadata live in MongoDB. This workflow does not upload or store document files.
- API: project-scoped list/create/detail/update and `submit`, `approve`, `request-changes`, `reject`, `archive` actions under `/api/v1/capture/projects/{projectId}/documents`.

## Periodic Work Report

- Scope: active Project Members; Project Leaders are excluded from member reporting obligations.
- Required content: accomplishments, approach, reason. Optional content: blockers and next steps.
- Schedule: only `DAILY` (1 day), `EVERY_3_DAYS` (3 days), and `WEEKLY` (7 days). A schedule change affects future periods and does not rewrite existing reports.
- Period identity: each member has at most one report for a given Project and period, enforced by a unique MongoDB index. Obligations are materialized idempotently from the Project frequency timeline.
- Lifecycle: `DRAFT` → `PENDING_REVIEW` → `APPROVED`, `CHANGES_REQUESTED`, or `REJECTED`; overdue drafts may be updated and submitted. Changes-requested reports may be corrected and resubmitted.
- Review: only the Project review authority may approve, request changes, or reject; changes/rejection require a comment.
- API: `/api/v1/capture/projects/{projectId}/work-reports` and `/work-report-settings`, including save, submit, review, and schedule operations.

## Authorization and event integration

- BE resolves the authenticated session, Organization context, Project membership/role, and Task scope from the owning IAM and Task APIs. It does not trust a caller-supplied permission flag or access their databases directly.
- Project, document, report, and task-note identifiers are always queried with their Organization/Project scope to prevent cross-project IDOR.
- Document and report state transitions and outbox events are persisted together; the shared audit service records the corresponding actions. Approved documents and reports emit `KNOWLEDGE_SOURCE_APPROVED` with source type, source id, Project id, version, and approval time. Draft, pending, changes-requested, and rejected content is not emitted as approved knowledge.
- Review and schedule events include `DOCUMENT_APPROVED`, `DOCUMENT_CHANGES_REQUESTED`, `DOCUMENT_REJECTED`, `WORK_REPORT_APPROVED`, `WORK_REPORT_CHANGES_REQUESTED`, `WORK_REPORT_REJECTED`, `WORK_REPORT_DUE`, `WORK_REPORT_OVERDUE`, and `REPORT_FREQUENCY_CHANGED`.
- These are integration events, not a notification center. Notification delivery remains owned by the notification system. No embedding, vector store, or retrieval pipeline is built here.

## Persistence and operational notes

Collections: existing `work_notes` (Task Notes), plus `project_documents`, `project_document_versions`, `work_reports`, and `work_report_settings`. The existing shared Capture outbox carries integration events. Indexes support Project/status/date listing, document version uniqueness, member-period uniqueness, and overdue scans.

The database branch adds schemas, persistence definitions, and an explicit migration planner. The migration defaults to dry-run and was not applied to a shared or production database. Before applying it locally, verify the target MongoDB URI and replica-set transaction support; rollback requires removing only the named Work Note indexes after confirming no dependent deployment uses them. Collection data is not dropped by this migration.

The FE exposes Task Notes from Task detail, and separate Project Documents and Work Reports routes. It renders API results, query loading/error/empty states, mutation feedback, and server-returned permissions. The API contract is in `DATN_BE/docs/openapi/work-note-v1.openapi.yaml`.
