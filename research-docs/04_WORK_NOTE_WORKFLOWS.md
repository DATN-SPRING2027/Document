# Work Note workflows

## Status and boundaries

Implementation is split across `DATN_BE`, `DATN_FE`, and this documentation repository. The BE implementation uses the Capture service and Gateway; the FE calls the project-scoped API through the application API client. MongoDB stores operational content in the Capture service database (`continuum_capture`). This document describes the delivered scope originally shipped on `2026-10-24` and synchronized with the active Capture -> Outbox -> SAG integration and Full-System Audit remediations on `2026-11-27`.

The three records (`Task Note`, `Project Document`, `Periodic Work Report`) have separate workflows and authorization rules. Project Documents support expanded file allowlists (PDF, DOCX, Office/Markdown/text/image types validated by magic bytes and SHA-256). Periodic Work Reports support both `MEMBER` and `LEADER` reporting scopes and produce due/overdue integration events. The existing Notification Center owns notification delivery, while `KnowledgeOutboxConsumer` in `DATN_BE` asynchronously streams approved sources to SAG (`POST /api/v1/projects/{projectId}/documents/upload`) and propagates `KNOWLEDGE_SOURCE_REVOKED` / `KNOWLEDGE_SOURCE_REPLACED` tombstones.

## Task Note

- Scope: an existing Task in the same Project. The Task Note API verifies the task through the Task API and stores only its task reference and structured note content.
- Content: title, accomplishments, approach, and reason. A Task Note is confirmed when created; no Leader review is required.
- Access: active Project members with access to the Task can read it; the same-Organization Manager exception below also permits reading after the Task scope check succeeds. The author and Project review authority may edit or archive a Task Note under the existing Project/Task scope checks; changes are audited. Task Notes have no approve/reject review transition.
- Knowledge: Task Notes do not automatically enter official AI knowledge.
- API: `GET|POST /api/v1/capture/projects/{projectId}/tasks/{taskId}/notes`; `PATCH|DELETE .../notes/{noteId}`. Project-wide list/detail routes are `GET .../work-notes` and `GET .../work-notes/{noteId}`.

## Project Document

- Scope: the Project. Project Documents are project-level records and do not reference a Task. Document types include MVP, database design, RSR, architecture, API specification, research, requirement, design, technical specification, and other.
- Lifecycle: `DRAFT` → `PENDING_REVIEW` → `APPROVED`, `CHANGES_REQUESTED`, or `REJECTED`; approved documents may be archived. Editing an approved or rejected document creates a new version while retaining prior content and review history.
- Permissions: members create/edit their documents and submit them. A Project role with review/configuration authority reviews documents. A current Organization Manager also has the explicitly approved same-Organization read/review exception below. The BE checks authority; FE permissions are only presentation hints.
- Storage: text, version metadata, and file metadata live in MongoDB. Originals are stored via the backend storage adapter (`STORAGE_MODE=r2|s3|local`, Cloudflare R2 in production; private local storage only in non-production/fallback). Presigned `upload-intent` and `confirm-upload` routes are strictly scoped to `(organizationId, projectId)` (`SEC-AUTH-002`) with full-file SHA-256 verification and magic-byte inspection. Optimistic concurrency uses `ETag` / `If-Match` CAS (`E2E-INT-012`).
- API: project-scoped list/create/detail/update and `submit`, `approve`, `request-changes`, `reject`, `archive`, `upload-intent`, `confirm-upload`, and `knowledge-sync` actions under `/api/v1/capture/projects/{projectId}/documents`.
- File API: `PUT|GET /api/v1/capture/projects/{projectId}/documents/{documentId}/file`; download responses preserve safe attachment headers (`Content-Disposition: attachment`, `X-Content-Type-Options: nosniff`).

## Manager review authority (decision 2026-10-25)

During the Member/Manager/Leader permission audit, the user explicitly confirmed:
“Có; Manager được đọc/review mọi Project trong Organization”. This records a
direct task decision, not an external PR approval or merge.

A current Organization Manager (technical `ADMIN`) with active Organization
membership may read/review the records enumerated below in any active
Project of that Organization, including Projects in which the Manager has no
Project Membership. Cross-Organization requests remain denied. Existing
author/reviewer separation, state-transition rules and audit requirements remain
applicable. This exception grants no Project Leader or Team authority and does
not redefine configuration, report scheduling, or unrelated content permissions.
The covered record types are:

| Record | Manager read/review exception | Existing constraints retained |
| --- | --- | --- |
| Task Note (`work_notes`) | Read across the current Organization's active Projects after the owning Task API validates the Task scope; no Project Membership prerequisite is added by Capture for a Manager. | No approve/reject workflow exists. Existing author/review-authority edit/archive rules remain unchanged; this decision creates no new mutation operation. |
| Project Document | Read document content, versions and authorized files; approve, request changes or reject submitted documents. | Server scope, author/reviewer separation, lifecycle and audit checks still apply. |
| Periodic Work Report | Read and review MEMBER and LEADER reports in the current Organization's active Projects. | Review requires a pending report and a different author; LEADER report review requires Manager authority. Member/Leader reporting obligations and schedule/configuration rules are unchanged. |

The per-record read/review rules include this scoped Manager exception. Other
confidential content and assistant retrieval do not inherit it. The current BE
behavior is retained; regression tests cover Manager Project resolution and
cross-Organization denial.

For Task validation, the current runtime authority is the Workspace Task API
activation accepted by Thang on 2026-10-22, recorded in
[`DATN-BE/AGENTS.md`](https://github.com/DATN-SPRING2027/DATN-BE/blob/026fca536f625430d66d07ed6b11ca27830b6e7a/AGENTS.md)
and the
[active Workspace Task contract](https://github.com/DATN-SPRING2027/DATN-BE/blob/026fca536f625430d66d07ed6b11ca27830b6e7a/docs/workspace/04-api-inventory.yaml).
Its G4 Manager exception permits current Organization `ADMIN` access to every
active Project's Tasks, including private Projects without Project Membership;
the IAM bridge checks active Organization Membership and a current scoped ADMIN
assignment before returning that authority. Capture's existing Task lookup
must use this owning Task authorization path, with matching Organization,
Project and Task identifiers. The older generic no-implicit-ADMIN Task rule in
the Internal Work Management baseline is superseded only for this active G4
Workspace slice; it remains applicable to other dormant/proposed slices. This
records the existing accepted path, not a new bypass or activation.

## Periodic Work Report

- Scope: active Project Members; Project Leaders are excluded from member reporting obligations.
- Required content: accomplishments, approach, reason. Optional content: blockers and next steps.
- Schedule: only `DAILY` (1 day), `EVERY_3_DAYS` (3 days), and `WEEKLY` (7 days). A schedule change affects future periods and does not rewrite existing reports.
- Period identity: each member has at most one report for a given Project and period, enforced by a unique MongoDB index. A scheduled job materializes obligations idempotently from the Project frequency timeline, without waiting for a member to open the report page. Periods that ended before membership began are skipped; schedule changes do not rewrite existing reports.
- Lifecycle: `DRAFT` → `PENDING_REVIEW` → `APPROVED`, `CHANGES_REQUESTED`, or `REJECTED`; overdue drafts may be updated and submitted. Changes-requested reports may be corrected and resubmitted.
- Review: the Project review authority, including the same-Organization Manager exception above, may approve, request changes, or reject MEMBER reports. LEADER reports require Manager review. Self-review is denied and changes/rejection require a comment.
- API: `/api/v1/capture/projects/{projectId}/work-reports` and `/work-report-settings`, including save, submit, review, and schedule operations.

## Authorization and event integration

- For user-initiated requests, BE resolves the authenticated session, Organization context, Project membership/role or the explicit Manager review exception, and Task scope from the owning IAM and Task APIs and does not trust a caller-supplied permission flag. For background report scheduling without a user session, the scheduled job uses IAM's read-only `ProjectReportRosterService` adapter.
- Project, document, report, and task-note identifiers are always queried with their Organization/Project scope to prevent cross-project IDOR.
- Document and report state transitions and outbox events are persisted together; the shared audit service records the corresponding actions. Approved documents and reports emit `KNOWLEDGE_SOURCE_APPROVED` with source type, source id, Project id, version, and approval time. Replacing an approved version and archiving a document emit `KNOWLEDGE_SOURCE_REPLACED` and `KNOWLEDGE_SOURCE_REVOKED`. Draft, pending, changes-requested, and rejected content is not emitted as approved knowledge.
- Review and schedule events include `DOCUMENT_APPROVED`, `DOCUMENT_CHANGES_REQUESTED`, `DOCUMENT_REJECTED`, `WORK_REPORT_APPROVED`, `WORK_REPORT_CHANGES_REQUESTED`, `WORK_REPORT_REJECTED`, `WORK_REPORT_DUE`, `WORK_REPORT_OVERDUE`, and `WORK_REPORT_FREQUENCY_CHANGED`.
- **Active SAG Knowledge Sync & Governance Rules (`2026-11-27` — `BE-LOGIC-001`, `BE-LOGIC-002`, `E2E-INT-001`, `E2E-INT-014`):**
  - `KnowledgeOutboxConsumer` consumes Capture outbox events (`KNOWLEDGE_SOURCE_APPROVED`, `KNOWLEDGE_SOURCE_REPLACED`, `KNOWLEDGE_SOURCE_REVOKED`) and streams approved content/file bytes to SAG `POST /api/v1/projects/{projectId}/documents/upload` (never `/ingest-object`; SAG has no direct R2 access per `adr-remove-laya-and-r2.md`).
  - **No self-approval bypass (`BE-LOGIC-001`):** `POST .../knowledge-sync` endpoints on Project Documents, Work Reports, and Task Notes are strictly restricted to re-enqueuing/retrying items that are **already `APPROVED`** (`assertReviewerCanReview` is enforced on every approval transition; an author can never use `/knowledge-sync` to auto-approve a `DRAFT` or `PENDING_REVIEW` record into SAG).
  - **Task Note schema & review governance (`BE-LOGIC-002`):** `work_notes` includes typed `provenance.review` and `knowledgeSync` fields/indexes; if a Task Note is enabled for governed SAG indexing, it enforces `assertReviewerCanReview` (distinct reviewer) and emits a durable `KNOWLEDGE_SOURCE_REVOKED` outbox event whenever edited or deleted after sync so stale/revoked content is removed from SAG.
  - **OpenAPI synchronization (`E2E-INT-014`):** All active Capture routes (including `upload-intent`, `confirm-upload`, `knowledge-sync`, `LEADER` report scope, expanded schedules/document types, and `ETag`/`If-Match` CAS headers) are synchronized with `DATN_BE/docs/openapi/work-note-v1.openapi.yaml`.

## Persistence and operational notes

Collections: existing `work_notes` (Task Notes), plus `project_documents`, `project_document_versions`, `work_reports`, and `work_report_settings`. The existing shared Capture outbox carries integration events. Indexes support Project/status/date listing, document version uniqueness, member-period uniqueness, and overdue scans.

The database branch adds schemas, persistence definitions, and an explicit migration planner. The migration defaults to dry-run and was not applied to a shared or production database. Before applying it locally, verify the target MongoDB URI and replica-set transaction support; rollback requires removing only the named Work Note indexes after confirming no dependent deployment uses them. Collection data is not dropped by this migration.

The FE exposes Task Notes from Task detail and project-level Task Note list/deep-link, plus separate Project Documents and Work Reports routes. It supports Task Note edit/archive, Project Document PDF/DOCX upload/download and version history, and server-authorized review actions. Loading, error, empty, validation, permission, and mutation states use the API results and server-returned permissions. The API contract is in `DATN_BE/docs/openapi/work-note-v1.openapi.yaml`.
