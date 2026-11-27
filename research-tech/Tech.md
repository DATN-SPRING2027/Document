# Continuum AI Technology Stack and Architecture Decisions

## Document status

- Status: Accepted baseline
- Date: 2026-09-18
- Scope: Continuum AI graduation project MVP
- Purpose: Record the approved technology stack, service boundaries, frontend UI foundation, and implementation constraints before implementation and backlog planning.

This document supplements the Continuum AI Graduation Project Specification v1.0. If a future implementation requires a conflicting technology or architectural pattern, the change must be recorded in a new Architecture Decision Record before adoption.

## Approved technology stack

| Layer | Approved technology | Responsibility |
| --- | --- | --- |
| Frontend | Next.js 16 (App Router), React 19, TypeScript | Web application, `[locale]` App Router BFF (`/api/backend/[...path]`), Server/Client boundaries, and SSE/WS streaming |
| UI foundation | TailAdmin v2.4 for Next.js / React with Tailwind CSS v4 (`@theme` tokens) | Dashboard shell, layouts, reusable visual components, and admin experience (with `@tanstack/react-table` / accessible dialog patterns built on TailAdmin styling) |
| Server state | TanStack Query v5 | API queries, mutations, caching, invalidation, and request states |
| Local UI state | Zustand v5 | Small client-only state that does not belong to the server cache |
| Core backend | Node.js 22, NestJS 11, TypeScript | Continuum domain logic, API, validation, permissions, workflows, and audit orchestration |
| Primary database | MongoDB 7.0 with Mongoose | Organizational knowledge, users, permissions, versions, workflows, tasks, and audit records |
| Authentication | JWT access token (HttpOnly cookies via BFF), rotating refresh token, CSRF, RBAC and resource ACL | Authentication, tenant scope, and authorization |
| Background jobs | Redis 7.2 (`noeviction`) and BullMQ (NestJS); in-process `InProcJobQueue` (SAG FastAPI) | NestJS queues (outbox/knowledge sync, mail, handover, schedules); SAG local ingestion jobs (SAG does not consume BullMQ directly) |
| AI service | Python 3.12 and FastAPI (`sag-laya-integration`) | SAG integration, deterministic indexing, hybrid search, citation grounding, and AI pipeline execution |
| Retrieval engine | Pinned `sag-laya-integration` (`zleap-sag` evolved runtime) | Canonical C99 DP chunking, Dense+BM25 hybrid search + RRF, Leiden routing tree, and source tracing |
| Vector & SAG relational storage | **Qdrant** (mandatory vector backend in prod) + **PostgreSQL 16** (`sag` schema for metadata/graph/routing tree; SQLite dev-only) | Retrieval index (1024-d Dense + native BM25 Sparse) and SAG relational metadata/ACL/version/graph store (supersedes initial LanceDB MVP baseline) |
| File storage | Backend: `STORAGE_MODE=r2\|s3\|local` (Cloudflare R2 first in prod; S3/local fallback); SAG: HTTP multipart stream from BE to local upload volume | Private originals (PDF, DOCX, Markdown, TXT, images) stored by BE; BE streams bytes to SAG `POST /api/v1/projects/{project_id}/documents/upload` (no R2-to-SAG direct ingest per `adr-remove-laya-and-r2.md`) |
| Task management | Continuum Task Workspace (NestJS) in `DATN_BE`; task UI/API client in `DATN_FE` | Active MongoDB logical database `continuum_task` (activated `2026-10-22`); pragmatically hosted inside `IamModule` via `TaskWorkspaceRepository` (`useDb('continuum_task')`) pending future standalone process split |
| LLM access | Provider-agnostic LLM Gateway | Extraction, interview planning, conflict analysis, and evidence-grounded answers |
| Embedding | Embedding provider configured through SAG | Semantic representation for retrieval |
| Parsing and OCR | SAG deterministic parser pipeline (`MarkItDown` / native PDF/DOCX/Office/OCR paths) | Document normalization, parsing, and OCR |
| API documentation | Swagger and OpenAPI | API contracts and generated client support |
| Local deployment | Docker Compose | Reproducible development and capstone deployment |
| Frontend testing | Vitest, React Testing Library, and Playwright | Unit, component, and browser end-to-end tests |
| Backend testing | Jest | NestJS unit and integration tests |
| AI testing | Pytest | SAG adapter, extraction, retrieval, and evaluation tests |
| CI and CD | GitHub Actions | Lint, typecheck, test, build, image creation, and controlled deployment |

## Frontend UI decision

### Decision

Continuum AI will use the React edition of [TailAdmin](https://tailadmin.com/) as the default visual and component foundation. TailAdmin is based on React, TypeScript, and Tailwind CSS and provides dashboard layouts, navigation shells, forms, tables, cards, charts, authentication pages, settings pages, and other administration patterns suitable for Continuum AI.

TailAdmin replaces shadcn/ui, Material UI, Ant Design, Chakra UI, Mantine, and unrelated component systems as the default UI reference for this project. A different component library may only be introduced after an explicit architecture decision and an assessment of visual consistency, accessibility, bundle impact, and maintenance cost.

### Usage rules

1. Follow the order **Reuse TailAdmin -> Extend TailAdmin -> Create a new component**.
2. Preserve TailAdmin's application shell, sidebar, header, page container, spacing, typography, color tokens, cards, tables, forms, modals, badges, alerts, tabs, pagination, and responsive behavior unless an approved product requirement requires a deviation.
3. Implement Continuum-specific domain components on top of TailAdmin patterns rather than introducing a parallel design system.
4. Keep server state in TanStack Query. Zustand must not duplicate API data or replace TanStack Query caching.
5. Keep pages thin. Domain behavior belongs in feature modules, hooks, API clients, schemas, and reusable components.
6. Every data-driven screen must handle loading, success, empty, error, unauthorized, and insufficient-evidence states where applicable.
7. TailAdmin is a UI template and design foundation, not the source of Continuum domain rules, authorization decisions, or backend behavior.
8. Before copying TailAdmin source into the repository, record the edition, release or commit, license, and any local modifications.

### Continuum screens that must follow TailAdmin

- Authentication and project selection
- Main application shell, sidebar, header, profile, and settings
- Knowledge search and AI assistant
- Source and document ingestion
- Knowledge Object list and detail
- Verification Center
- Knowledge gaps and conflicts
- AI Knowledge Interviewer
- Knowledge Continuity Dashboard
- Successor onboarding and member handover views
- Project, team, membership, role, assignment, permission, integration, and audit administration

## Actor and authorization model

The MVP uses three persistent Organization/Project human roles:

- `ADMIN`
- `TEAM_LEADER`
- `MEMBER`

`SME`, `KNOWLEDGE_OWNER`, and `SUCCESSOR` are scoped assignments rather than unrestricted global roles. `ONBOARDING` and `OFFBOARDING` are workflows, not Organization-context eligibility. A `TEAM_LEADER` manages only explicitly assigned Project/Team scope. Project creation follows active Organization Membership and trusted context, not the legacy `project.create` grant. All members, including leaders, are responsible for contributing and maintaining project knowledge during normal work.

`PLATFORM_OPERATOR` is a separate platform-scoped operations actor, not a fourth Organization role. It provisions Organizations, bootstraps the first Organization `ADMIN`, and operates audited Platform Console V2 workflows; it has no default Organization content access. Organization Membership is the authoritative User–Organization association. An authenticated User with `ACTIVE` Organization Membership may create a `PRIVATE` Project without a role or `project.create` grant; per the accepted `2026-10-20` [Project MVP contract V1](../research-docs/Workspace/13-project-mvp-contract-v1.md) (superseding the `2026-10-02` `MEMBER`-only bootstrap note), creation atomically adds an `ACTIVE` Project Membership and a project-scoped `TEAM_LEADER` RoleAssignment for the creator. Organization `ADMIN` (Manager) and Team Leader scopes remain distinct and explicitly enforced.

Effective permission is calculated from persistent role, project/team membership, scoped assignment, resource ACL, lifecycle state, and explicit deny. The canonical model and permission matrix are defined in [02_ACTORS_ROLES_AND_PERMISSIONS.md](../research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md).

## Service boundaries

```text
Next.js 16 + TailAdmin Web (BFF /api/backend)
          |
          v
NestJS Continuum Core API
    |          |             |
    v          v             v
 MongoDB   Redis BullMQ   Object Storage (STORAGE_MODE=r2|s3|local)
    |
    +--- HTTP multipart stream (/upload) & internal API ---> FastAPI SAG AI Service (InProcJobQueue)
                                                               |               |
                                                               v               v
                                                       PostgreSQL 16 (sag)   Qdrant (Dense+BM25)
```

The following boundaries are mandatory:

- The frontend must call the Continuum NestJS API (via Next.js BFF `/api/backend`), not SAG directly.
- SAG and the FastAPI service return evidence, retrieval metadata, AI suggestions, or Proposed Knowledge.
- AI output must never write directly to MongoDB.
- NestJS validates input, permission scope, evidence references, and state transitions before persistence.
- Only authorized Continuum workflows may transition knowledge to VERIFIED or ACTIVE.
- MongoDB is the source of truth for Continuum domain state. PostgreSQL 16 (`sag` schema) and Qdrant vector indexes are retrieval infrastructure, not organizational truth.

## MongoDB design constraints

MongoDB is approved for the MVP with the following conditions:

1. Use stable `knowledge_objects` records and separate immutable `knowledge_versions` records.
2. Use references for mutable many-to-many relationships such as evidence, owners, reviewers, permissions, processes, gaps, conflicts, incidents, and decisions.
3. Do not store the complete knowledge graph, version history, evidence, and ACL tree inside one deeply embedded document.
4. Run MongoDB as a replica set in Docker Compose so multi-document transactions are available.
5. Use a transaction when verification creates a version, supersedes the previous version, updates status, and writes an audit event.
6. Include `organizationId` or an equivalent tenant boundary in every tenant-owned collection and query.
7. Define compound indexes for tenant scope, status, owner, validity interval, review date, source mapping, and frequently used permission filters.
8. Treat denormalized dashboard and read models as derived data that can be rebuilt.
9. Add idempotent migration or backfill scripts when a Mongoose schema change affects existing documents.

The target catalog spans MongoDB-backed service databases rather than one shared database, consistent with workspace ADR-003/DEC-011. As of `2026-11-27`, active DATN-BE runtime databases include `continuum_iam`, `continuum_capture`, `continuum_task` (activated `2026-10-22` and pragmatically mounted inside `IamModule` via `useDb('continuum_task')` behind `TaskWorkspaceRepository`), `continuum_lifecycle`, `continuum_chat`, `continuum_handover`, `continuum_ingestion`, `continuum_notification`, `continuum_jira` (legacy runtime module pending retirement), and `continuum_audit`. `continuum_ai_adapter` remains a target schema without an active standalone BE runtime owner. See the `2026-11-27` Decision Amendment below for the Task Workspace monolith-placement ADR note.

Expected collections include:

```text
organizations
users
projects
teams
project_memberships
team_memberships
roles
role_assignments
organization_capability_grants
sme_assignments
knowledge_owner_assignments
handover_assignments
handovers
handover_items
sources
source_acls
documents
document_versions
tasks
task_events
work_notes
work_note_versions
chat_sessions
chat_messages
knowledge_objects
knowledge_versions
knowledge_evidence
knowledge_owners
knowledge_verifications
knowledge_relations
knowledge_gaps
knowledge_conflicts
processes
knowledge_requirements
interviews
audit_logs
ingestion_jobs
```

## Authentication and authorization constraints

- Use short-lived JWT access tokens.
- Rotate refresh tokens and store only a secure hash or equivalent protected representation.
- Support revocation and refresh-token reuse detection.
- RBAC alone is insufficient. Authorization must combine project/team membership, persistent role, scoped assignment, source ACL, document ACL, Knowledge Object scope, and membership lifecycle state.
- Admin does not automatically receive permission to read confidential knowledge.
- Successor access is limited to the approved handover scope and does not clone all predecessor permissions.
- Resolve the allowed source and knowledge scope before retrieval.
- Restricted evidence must never be retrieved and then removed after it has already entered the LLM context.
- The backend is authoritative. Frontend route guards are only a user-experience layer.
- Project creation requires authenticated active subject, trusted matching Organization Context, and `ACTIVE` Organization Membership; no role or `project.create` grant is required. The legacy grant schema is not removed by this policy change.

## Task, daily note, chat, and object-storage constraints

- Continuum Task Workspace is the canonical source for DATN task lifecycle and owns MongoDB logical database `continuum_task` on the existing replica set (activated `2026-10-22` with Gate G4 Manager Task governance). In the current capstone runtime, it is pragmatically mounted inside `IamModule` (`useDb('continuum_task')`) and isolated behind `TaskWorkspaceRepository`; standalone process extraction (`dist/services/task/main.js`) remains the documented microservices target (ADR-010).
- Under the `2026-10-24` Capture taxonomy, `Task Note` (`work_notes`) links to a validated Task in the caller's authorized organization/project/team scope, while `Project Document` (`project_documents`) and `Periodic Work Report` (`work_reports`) are project-level records.
- Only governed, authorized Capture records (`APPROVED` Project Documents / Work Reports, and any explicitly governed Task Notes passing `assertReviewerCanReview`) are emitted to the outbox and streamed by `KnowledgeOutboxConsumer` to SAG (`POST /api/v1/projects/{projectId}/documents/upload`). `/knowledge-sync` retries only already-`APPROVED` items and never bypasses review. Task records and fields are not standalone SAG sources; current ACL (`scope.isProjectMember === true` on `ACTIVE` projects) is checked before evidence enters answer context.
- In handover, the authorized Team Leader reads open tasks through the Task API, selects tasks and assigns them to the scoped successor. The Task API updates canonical assignee; Handover stores references and acknowledgement state. No successor inherits project-wide permission.
- Capture, Handover and Agents use authenticated Task API/event contracts; none access Task collections directly. Agents may return a task-change proposal, but a permitted human confirms before the Task Service commits it. Jira import, webhook sync and reconciliation are outside the MVP.
- Manual note entry is always available. The author confirms what/how/why and may correct the draft; task metadata is context, not verified organizational knowledge.
- Store original uploads in private Cloudflare R2 with a storage adapter so an S3-compatible alternative remains possible. MongoDB stores metadata, object key, checksum and ACL. Signed upload/download paths must be short-lived and permission-checked.
- Chat is the core successor interface. Every answer must be cited and permission-aware; an insufficient-evidence outcome must be explicit. Chat history cannot become a bypass after source access changes.
- See [Daily workflow and internal task management](../research-docs/03_DAILY_WORKFLOW_AND_JIRA_SYNC.md) and [ADR-010](ADR-010-task-service-in-existing-repositories.md).

## Queue and AI processing constraints

- BullMQ is owned by the Node.js and NestJS side.
- For the MVP, a NestJS BullMQ worker should call the FastAPI AI service through an authenticated internal API.
- The Python service should not consume BullMQ jobs directly unless a separate cross-language queue decision is approved.
- Jobs must support deterministic IDs or idempotency keys, retry limits, failure reasons, progress, timestamps, and dead-letter handling.
- A failed ingestion or extraction job must not delete the original source file.

## SAG and retrieval constraints

- Pin the SAG release or commit used by the project.
- Access SAG through a Continuum-owned adapter instead of leaking SAG-specific types throughout the domain code.
- Keep the mapping between Continuum source and document IDs and SAG source, document, job, and chunk references.
- SAG Event is a retrieval representation and must not be treated as a Continuum Knowledge Object.
- **PostgreSQL 16 (`sag` schema) + Qdrant** is the authoritative SAG production storage backend (superseding the initial LanceDB MVP baseline). Future storage changes must not alter the Continuum domain contract.
- Retrieval results must pass permission, status, version, validity, freshness, and conflict validation before answer generation.

## LLM decision gate

The exact LLM provider and model remain open. Before implementing production AI workflows, evaluate candidates using the project benchmark against:

- Vietnamese and English quality
- Structured JSON reliability
- Evidence grounding and citation behavior
- Context size
- Latency and availability
- Cost per evaluated query
- Privacy and data-processing constraints
- Compatibility with an OpenAI-style or project-defined gateway interface

Application code must depend on an internal LLM Gateway rather than provider-specific SDK types outside the infrastructure layer.

## Parser and OCR decision gate

Do not leave `SAG pipeline / MarkItDown / MinerU` as an unresolved runtime choice. Define a routing table by source type and document characteristics, for example native DOCX and text PDF versus scanned or layout-heavy PDF. Record fallback behavior, timeout, size limits, supported languages, and the artifacts retained for citation.

## Verification requirements before implementation

- The repository structure and service ownership are documented.
- TailAdmin edition, license, and pinned source version are recorded.
- MongoDB collections, references, indexes, transaction boundaries, and tenant fields are reviewed.
- API contracts between React, NestJS, and FastAPI are defined through OpenAPI.
- The LLM Gateway and SAG adapter interfaces are agreed before provider-specific implementation.
- Security tests confirm that unauthorized evidence never enters retrieval results or LLM context.
- End-to-end acceptance must cover task create/update/assignment, optional task-linked and unlinked Work Notes, authorized evidence indexing, extraction, verification, cited answer, insufficient evidence, handover task selection/assignment, and permission denial.
- Docker Compose starts MongoDB as a replica set and preserves MongoDB, Redis, and SAG data across restarts; R2 is accessed through testable object-storage configuration.

## Decision record — 2026-09-18

- Replaced four legacy role codes with `ADMIN`, `TEAM_LEADER`, and `MEMBER`; SME and Knowledge Owner remain scoped assignments.
- New project creation by a Team Leader requires an Admin-issued organization `project.create` grant.
- The original vertical slice assumed Jira-linked capture; the task-source decision was superseded by the 2026-10-01 ADR-009 amendment below.
- Selected Cloudflare R2 as the first object store, retaining an S3-compatible abstraction.

## Decision amendment — 2026-10-01

- Continuum owns the canonical task lifecycle; Jira task import, webhooks, reconciliation and two-way sync are outside the MVP. See [ADR-009](ADR-009-internal-task-source-and-mongodb.md).
- Task runs as an independently deployed NestJS service but source remains in DATN_BE; task UI/API client remains in DATN_FE. See [ADR-010](ADR-010-task-service-in-existing-repositories.md).
- Task Service owns `tasks`, `task_events` and an optional transactional outbox in logical MongoDB database `continuum_task`, using the existing replica set. This supersedes the earlier shared-database placement; it does not provision a new physical cluster.
- Work Notes may optionally reference a task; only authorized Work Notes/evidence are eligible for SAG indexing. Handover uses the Task API and does not become another writable task store.
- The Task decision does not change the SAG retrieval engine decision.

## Decision amendment — 2026-10-02

- Platform operations are separated from Organization administration: `PLATFORM_OPERATOR` provisions Organizations and bootstraps the first Organization Admin, without default access to Organization content.
- `OrganizationMembership` is the authoritative User–Organization relationship. Only `ACTIVE` membership establishes Organization Context; zero active memberships means no context, one is selected automatically, and multiple require explicit user selection validated by the backend. The HTTP transport contract still needs to be documented in OpenAPI.
- Any authenticated User with active Organization Membership can create a Project in that Organization. This supersedes the 2026-09-18 `project.create` grant gate for Project creation only. The new Project is private; its creator receives active Project Membership and the project-scoped `MEMBER` RoleAssignment, but not Team Leader/owner status.
- See the [Project Foundation decisions](../research-docs/Workspace/00-organization-and-access-contract-readiness.md) and the accepted Organization Membership decision DEC-016 in DATN_BE.

## Decision amendment — 2026-11-27 (Full-System Audit Synchronization)

- **SAG Storage & Vector Backend (supersedes initial LanceDB baseline):** `sag-laya-integration` runs on **Python 3.12 + FastAPI** with **PostgreSQL 16** (`sag` schema for metadata, ACL mappings, version lifecycle, knowledge graph, and Leiden routing tree; SQLite is strictly dev/test only) and **Qdrant** (mandatory vector backend in production, storing per-project 1024-d Dense + native BM25 Sparse hybrid collections). LanceDB and `pgvector` are not used in production runtime.
- **Storage ADR Split (`STORAGE_MODE=r2|s3|local` + BE-to-SAG HTTP upload):** NestJS (`DATN_BE`) owns object storage (`STORAGE_MODE=r2|s3|local`, Cloudflare R2 in production) for Capture Project Documents and Chat attachments. Per `sag-laya-integration` ADR (`adr-remove-laya-and-r2.md`), SAG does not connect directly to R2 or accept `/ingest-object`; instead, `KnowledgeOutboxConsumer` streams approved file bytes from BE to SAG `POST /api/v1/projects/{project_id}/documents/upload` onto SAG's local upload volume and schedules indexing via SAG's in-process `InProcJobQueue`.
- **Task Workspace Monolith Placement (pragmatic ADR note on ADR-010):** `continuum_task` was activated on `2026-10-22` with Gate G4 Manager Task governance (`TaskWorkspaceIamBridge`). In the current capstone deployment topology, Task Workspace is pragmatically hosted inside `IamModule` (`useDb('continuum_task')`) and isolated behind `TaskWorkspaceRepository` (consumed by Capture, Handover, and Notification Center without direct raw collection access). Extracting it into a standalone process (`dist/services/task/main.js`) remains the documented target split once microservices Gateway routing is enabled.
- **Capture 3-Type Taxonomy & Governed Sync (`2026-10-24` / `2026-10-25` / `2026-11-27`):** Capture separates `Task Note` (`work_notes`, linked to a validated Task), `Project Document` (`project_documents`), and `Work Report` (`work_reports`), with the `2026-10-25` Manager same-Organization read/review exception. Author/reviewer separation (`assertReviewerCanReview`) is mandatory on all reviewable artifacts; `/knowledge-sync` only retries already-`APPROVED` items and never acts as a self-approval shortcut.
- **Project Creator Role (`2026-10-20`):** Creating a Project grants the creator `ACTIVE` Project Membership + project-scoped `TEAM_LEADER` (superseding the `2026-10-02` `MEMBER`-only bootstrap text in line 261).
- **Frontend UI Foundation & Companion Patterns:** TailAdmin v2.4 + Tailwind CSS v4 (`@theme` tokens in `globals.css`) remains the authoritative visual design system; reusable data-table (`@tanstack/react-table`), command palette, drawer, and accessible dialog ergonomics are implemented on top of TailAdmin styling without introducing a conflicting design system.

## Documentation consistency rule

All new Continuum AI task work items, UI specifications, and implementation plans must identify TailAdmin as the approved frontend UI foundation. References to shadcn/ui, Material UI, Ant Design, Chakra UI, Mantine, or another UI system are not authoritative for Continuum AI unless an accepted ADR explicitly introduces them.
