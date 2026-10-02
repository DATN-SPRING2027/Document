# CONTINUUM AI MVP SCOPE

## Document status

- Project: Continuum AI
- Project type: Graduation project and team knowledge continuity system
- Version: 1.3
- Status: Accepted MVP baseline
- Last updated: 2026-10-01

## 1. Purpose

Continuum AI addresses knowledge inheritance when a leader or member leaves a software project, changes team, or transfers responsibility. The MVP focuses on one software project with multiple teams rather than an enterprise-wide knowledge platform.

The system must provide more value than storing a large collection of documents. It must help the successor understand:

- What the team and predecessor have done.
- Why important decisions were made.
- What is currently active, incomplete, risky, or outdated.
- Which procedures, incidents, workarounds, dependencies, and responsibilities matter for the takeover.
- What knowledge is still missing before the predecessor leaves.

## 2. Core hypothesis

> A project team can reduce knowledge loss and successor time-to-information by continuously capturing, verifying, maintaining, and transferring member knowledge through a structured workflow and an evidence-grounded RAG assistant.

Knowledge capture begins while the project is active. The system must not wait until a member announces departure.

## 3. MVP actors

Persistent roles:

- `PLATFORM_OPERATOR`: platform-level operations actor that provisions Organizations, bootstraps the first Organization Admin, and monitors system health/configuration. This actor is not an Organization role and has no default access to Organization content.
- `ADMIN`: manages Users and Organization Memberships, assigns roles/scopes, and manages Organization settings/policy. The role alone does not grant Project Membership, Team Leader scope, or access to confidential Project content; Project/Team operations require the applicable explicit scope and policy.
- `TEAM_LEADER`: leads assigned Projects/Teams and their knowledge workflow. The assignment scope must be explicit; the role alone grants no access outside that scope.
- `MEMBER`: contributes notes/documents and maintains, searches, and transfers knowledge related to assigned work.

Scoped assignments and lifecycle states:

- `SME`: expert assignment for a domain, module, process, or knowledge requirement.
- `KNOWLEDGE_OWNER`: accountability assignment for knowledge or a required knowledge area.
- `SUCCESSOR`: handover assignment for the person taking over a responsibility.
- `ONBOARDING`: membership state for an incoming member.
- `OFFBOARDING`: membership state for a departing or transferring member.

The canonical authorization model is defined in [02_ACTORS_ROLES_AND_PERMISSIONS.md](02_ACTORS_ROLES_AND_PERMISSIONS.md).

Organization membership, not an Organization-level RoleAssignment, is the authoritative association between a User and an Organization. Only an `ACTIVE` Organization Membership establishes Organization Context. An authenticated User with that active membership may create a Project in the trusted Organization; `project.create` is not required for this operation. Creation makes the Project `PRIVATE` and atomically gives the creator an `ACTIVE` Project Membership plus project-scoped `MEMBER` assignment. See [Organization and Workspace Access Contract Readiness](Workspace/00-organization-and-access-contract-readiness.md).

## 4. Required ongoing knowledge input

All team members, not only leaders, contribute knowledge during normal project operation. The MVP supports at least:

- Project and technical decisions with rationale.
- Module and responsibility ownership.
- Setup, deployment, recovery, and operating procedures.
- Incidents, root causes, resolutions, and lessons learned.
- Known issues, warnings, exceptions, and workarounds.
- Internal and external dependencies.
- Current status, unfinished work, risks, and open questions.
- Knowledge source, evidence, owner, reviewer, version, validity, and review date.
- Handover notes and successor questions.
- Task-linked daily notes: what was done, how/why, blockers, next steps, and evidence. Internal Continuum task data can prefill task context, but the person confirms the note.

The system may extract candidates from project artifacts, but AI output remains `PROPOSED` until an authorized human verifies it.

## 5. Core MVP loop

```text
Active project work
      |
      v
Members and leaders manage internal project tasks, create notes, upload sources, and confirm task-linked work context
      |
      v
Source ingestion and SAG retrieval indexing
      |
      v
AI extracts Proposed Knowledge with evidence
      |
      v
Owner or scoped SME verifies knowledge
      |
      v
Coverage, ownership, and basic gap monitoring
      |
      v
Missing or overdue knowledge creates follow-up
      |
      v
Member departure or responsibility transfer
      |
      v
Focused handover checklist and unresolved questions
      |
      v
Scoped handover summary and successor learning path
      |
      v
Successor asks evidence-grounded questions and reports gaps
```

## 6. Mandatory MVP capabilities

### 6.1. Project and team management

- One software project containing multiple teams.
- Project membership and team membership.
- Three persistent Organization/Project roles (`ADMIN`, `TEAM_LEADER`, `MEMBER`), plus the separate platform-scoped `PLATFORM_OPERATOR`; Organization, Project and Team memberships determine scope. Project creation requires authenticated active Organization Membership, not a `project.create` grant.
- SME, Knowledge Owner, and Successor assignments.
- Onboarding and offboarding membership states.
- Project, Team and membership use-case flows are proposed in [Project, Team and Membership Use Cases](Workspace/05-project-team-access-use-cases.md); unresolved lifecycle and permission details remain subject to review.
- Organization context, Organization membership gaps, cross-document access decisions, and the readiness gates for implementation are tracked in [Organization and Workspace Access Contract Readiness](Workspace/00-organization-and-access-contract-readiness.md). This register does not expand the accepted one-Project MVP boundary or approve unresolved multi-Organization behavior.

### 6.2. Continuous knowledge capture

- Continuum's internal Task Service is the canonical source for DATN task lifecycle. It has an independent process/deployment built from the existing DATN_BE source and owns logical MongoDB database `continuum_task`; Jira is not a task source or MVP task-sync connector. See [ADR-009](../research-tech/ADR-009-internal-task-source-and-mongodb.md) and [ADR-010](../research-tech/ADR-010-task-service-in-existing-repositories.md).
- Task MVP proposal: create/list/detail/edit, assign by Team Leader, fixed status transition, basic search/filter, limited history, optional Work Note link, and open-task handover. A task belongs to one project and at most one team; Kanban is P1. Field/status/permission details remain proposed, pending user review in [Task-management Use Cases](Internal-Work-Management/12-continuum-task-management-use-cases.md).
- Manual structured knowledge entry and short daily/task notes remain available. A Work Note may optionally reference an internal task by `taskId`; task metadata can prefill context, but the member confirms the note and supplies what/how/why, blockers, next steps and evidence.
- File upload (PDF, DOCX, Markdown, TXT, image) and source management; Cloudflare R2 stores originals, MongoDB stores metadata.
- Required knowledge templates by team, module, or process.
- AI extraction of Proposed Knowledge from authorized evidence.
- Only author-confirmed Work Notes and evidence allowed by source policy/ACL may be submitted to SAG for retrieval/indexing. Task records and fields (including title, description, status and assignee) remain in MongoDB and are not indexed as an independent SAG source.
- Reminders for missing/overdue work notes and required knowledge; no employee scoring.
- Audit trail for contributions and changes.

### 6.3. Knowledge lifecycle

- Proposed, under-review, verified, active, superseded, deprecated, and rejected states.
- Version, validity interval, owner, reviewer, evidence, and review date.
- Human verification before organizational activation.
- Basic status and review date; automated conflict detection and advanced freshness scoring are later phases.

### 6.4. Permission-aware assistant

- Search and question answering over authorized project knowledge.
- Answer, citations, status, owner, version, and last verified date.
- Permission filtering before retrieval and context construction.
- Explicit insufficient-evidence response and a way to report a Knowledge Gap; no fabricated answer.

### 6.5. Handover workflow

- Initiate departure or responsibility transfer for any leader or member.
- Analyze responsibilities, ownership, evidence, coverage, freshness, and concentration.
- Create required handover items and identify knowledge gaps.
- Record unresolved questions for a human follow-up; automated AI interviewing is a stretch capability.
- Assign a successor and a scoped handover package.
- An authorized Team Leader reads open-task candidates from the Continuum Task API, selects tasks, and assigns them to a scoped successor. The Task API updates the canonical assignee; Handover stores the `taskId` and its own acknowledgement/readiness state. Successor access is limited to the selected tasks and permitted evidence, not the entire project.
- Track task references, successor questions, unresolved gaps, and readiness.
- Require the Team Leader assigned to the handover's Project/Team scope, or another explicitly authorized reviewer, to confirm completion. Organization Admin role alone does not grant access to the confidential handover package or approval action.

### 6.6. Evaluation

- A labeled dataset from one project scope.
- Expected answers and supporting evidence.
- At least a versioned retrieval/answer baseline and Continuum result; SAG ablation where feasible.
- Retrieval, answer, citation, permission, and handover metrics.
- Repeatable test runs with fixed model and retrieval configuration where possible.

## 7. Stretch goals

- GitHub, Google Drive, Confluence, MCP-based internal app connectors, Jira import/linking, or meeting-note connectors; these are future/stretch integrations and are not task sources in the MVP.
- AI-generated interview questions and interview-to-Proposed-Knowledge conversion.
- Advanced conflict detection.
- Advanced freshness scoring, incident memory, and automated employee-transfer analysis.
- Personalized onboarding beyond the assigned handover scope.
- Temporal graph visualization.
- Cross-project knowledge transfer.
- Additional local LLM and reranker experiments.

## 8. Out of scope

- Enterprise-wide knowledge management.
- Full HR or Learning Management System.
- Employee performance scoring.
- Automatic organizational restructuring.
- Autonomous policy modification.
- Automatic successor assignment without human approval.
- AI verification of organizational truth without an authorized human.
- Full business process management.
- Fine-tuning a dedicated enterprise LLM in the MVP.

## 9. Success criteria

The MVP is successful when it demonstrates:

1. Every project member can contribute and maintain authorized knowledge.
2. Missing or overdue required knowledge creates a visible follow-up action.
3. A member departure produces a prioritized handover plan based on real gaps.
4. A successor receives a scoped handover package and can ask cited questions.
5. The system refuses unsupported, outdated, conflicting, or unauthorized answers.
6. Unauthorized evidence leakage is zero in the security test suite.
7. The benchmark reports retrieval and answer quality against labeled expected outputs.
8. The handover evaluation measures time-to-information, answer correctness, unresolved gaps, or equivalent takeover outcomes.

## 10. Delivery boundary: 10 weeks

The demonstrable vertical slice is: a `PLATFORM_OPERATOR` provisions the Organization and first Admin; the Admin manages Organization users, membership and scoped assignments; any authenticated active Organization member can create a private Project and becomes its initial `MEMBER`; assigned Team Leaders manage their Project/Team scope; members manage internal tasks and add manual or task-linked Work Notes/documents; files are processed/indexed; AI proposes knowledge for human review; and a successor uses a scoped handover package and cited chat assistant with permission checks. Dataset-based evaluation is required. Do not treat every possible dashboard, connector, interview, or enterprise workflow as mandatory in this period. See [Daily work capture and internal task management](03_DAILY_WORKFLOW_AND_JIRA_SYNC.md).
