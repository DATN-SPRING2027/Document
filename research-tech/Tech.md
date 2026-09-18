# Continuum AI Technology Stack and Architecture Decisions

## Document status

- Status: Accepted baseline
- Date: 2026-09-18
- Scope: Continuum AI graduation project MVP
- Purpose: Record the approved technology stack, service boundaries, frontend UI foundation, and implementation constraints before repository initialization, Jira backlog creation, and coding.

This document supplements the Continuum AI Graduation Project Specification v1.0. If a future implementation requires a conflicting technology or architectural pattern, the change must be recorded in a new Architecture Decision Record before adoption.

## Approved technology stack

| Layer | Approved technology | Responsibility |
| --- | --- | --- |
| Frontend | React, TypeScript, Vite | Web application and client-side composition |
| UI foundation | TailAdmin for React with Tailwind CSS | Dashboard shell, layouts, reusable visual components, and admin experience |
| Server state | TanStack Query | API queries, mutations, caching, invalidation, and request states |
| Local UI state | Zustand | Small client-only state that does not belong to the server cache |
| Core backend | Node.js, NestJS, TypeScript | Continuum domain logic, API, validation, permissions, workflows, and audit orchestration |
| Primary database | MongoDB with Mongoose | Organizational knowledge, users, permissions, versions, workflows, and audit records |
| Authentication | JWT access token, rotating refresh token, RBAC and resource ACL | Authentication, tenant scope, and authorization |
| Background jobs | Redis and BullMQ | Ingestion, OCR, extraction, indexing, retry, and scheduled review jobs |
| AI service | Python and FastAPI | SAG integration and AI pipeline execution |
| Retrieval engine | Pinned version of zleap-sag | Event and entity retrieval, semantic search, and source tracing |
| Initial vector storage | LanceDB through SAG | Retrieval index for the MVP |
| File storage | MinIO or an S3-compatible service | Original PDF, DOCX, source files, OCR output, and derived artifacts |
| LLM access | Provider-agnostic LLM Gateway | Extraction, interview planning, conflict analysis, and evidence-grounded answers |
| Embedding | Embedding provider configured through SAG | Semantic representation for retrieval |
| Parsing and OCR | SAG pipeline with explicitly selected MarkItDown or MinerU paths | Document normalization, parsing, and OCR |
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

The MVP uses four persistent human roles:

- `PROJECT_MANAGER`
- `TEAM_LEADER`
- `TEAM_MEMBER`
- `PROJECT_ADMIN`

`SUBJECT_MATTER_EXPERT`, `KNOWLEDGE_OWNER`, and `SUCCESSOR` are scoped assignments rather than unrestricted global roles. `ONBOARDING` and `OFFBOARDING` are membership lifecycle states. All members, including leaders, are responsible for contributing and maintaining project knowledge during normal work.

Effective permission is calculated from persistent role, project/team membership, scoped assignment, resource ACL, lifecycle state, and explicit deny. The canonical model and permission matrix are defined in [02_ACTORS_ROLES_AND_PERMISSIONS.md](../research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md).

## Service boundaries

```text
React and TailAdmin Web
          |
          v
NestJS Continuum Core API
    |          |             |
    v          v             v
 MongoDB   Redis BullMQ   MinIO or S3
    |
    +------ calls ------> FastAPI AI Service
                              |
                              v
                      zleap-sag and LanceDB
```

The following boundaries are mandatory:

- The frontend must call the Continuum NestJS API, not SAG directly.
- SAG and the FastAPI service return evidence, retrieval metadata, AI suggestions, or Proposed Knowledge.
- AI output must never write directly to MongoDB.
- NestJS validates input, permission scope, evidence references, and state transitions before persistence.
- Only authorized Continuum workflows may transition knowledge to VERIFIED or ACTIVE.
- MongoDB is the source of truth for Continuum domain state. LanceDB and SAG indexes are retrieval infrastructure, not organizational truth.

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

Expected primary collections include:

```text
organizations
users
projects
teams
project_memberships
team_memberships
roles
role_assignments
sme_assignments
knowledge_owner_assignments
handover_assignments
handovers
handover_items
sources
source_acls
documents
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
- Project Admin does not automatically receive permission to read confidential knowledge.
- Successor access is limited to the approved handover scope and does not clone all predecessor permissions.
- Resolve the allowed source and knowledge scope before retrieval.
- Restricted evidence must never be retrieved and then removed after it has already entered the LLM context.
- The backend is authoritative. Frontend route guards are only a user-experience layer.

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
- LanceDB is acceptable for the initial SAG deployment. A production storage change must not alter the Continuum domain contract.
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
- End-to-end tests cover upload, extraction, verification, cited answer, insufficient evidence, gap closure, and permission denial.
- Docker Compose starts MongoDB as a replica set and preserves MongoDB, Redis, object storage, and SAG data across restarts.

## Documentation consistency rule

All new Continuum AI documents, Jira tasks, UI specifications, and implementation plans must identify TailAdmin as the approved frontend UI foundation. References to shadcn/ui, Material UI, Ant Design, Chakra UI, Mantine, or another UI system are not authoritative for Continuum AI unless an accepted ADR explicitly introduces them.
