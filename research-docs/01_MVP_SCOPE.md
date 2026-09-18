# CONTINUUM AI MVP SCOPE

## Document status

- Project: Continuum AI
- Project type: Graduation project and team knowledge continuity system
- Version: 1.1
- Status: Accepted MVP baseline
- Last updated: 2026-09-18

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

- `PROJECT_MANAGER`: manages continuity across the project and multiple teams.
- `TEAM_LEADER`: manages knowledge requirements and handover inside assigned teams.
- `TEAM_MEMBER`: contributes, maintains, searches, and transfers knowledge related to assigned work.
- `PROJECT_ADMIN`: manages membership, connectors, permissions, sources, and technical configuration.

Scoped assignments and lifecycle states:

- `SUBJECT_MATTER_EXPERT`: expert assignment for a domain, module, process, or knowledge requirement.
- `KNOWLEDGE_OWNER`: accountability assignment for knowledge or a required knowledge area.
- `SUCCESSOR`: handover assignment for the person taking over a responsibility.
- `ONBOARDING`: membership state for an incoming member.
- `OFFBOARDING`: membership state for a departing or transferring member.

The canonical authorization model is defined in [02_ACTORS_ROLES_AND_PERMISSIONS.md](02_ACTORS_ROLES_AND_PERMISSIONS.md).

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

The system may extract candidates from project artifacts, but AI output remains `PROPOSED` until an authorized human verifies it.

## 5. Core MVP loop

```text
Active project work
      |
      v
Members and leaders create or update project knowledge
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
Coverage, freshness, ownership, and gap monitoring
      |
      v
Missing or overdue knowledge creates follow-up
      |
      v
Member departure or responsibility transfer
      |
      v
Coverage analysis and gap-driven AI interview
      |
      v
Verified handover package and successor learning path
      |
      v
Successor asks evidence-grounded questions and reports gaps
```

## 6. Mandatory MVP capabilities

### 6.1. Project and team management

- One software project containing multiple teams.
- Project membership and team membership.
- Persistent role assignments with project or team scope.
- SME, Knowledge Owner, and Successor assignments.
- Onboarding and offboarding membership states.

### 6.2. Continuous knowledge capture

- Manual structured knowledge entry.
- File upload and source management.
- Required knowledge templates by team, module, or process.
- AI extraction of Proposed Knowledge from authorized evidence.
- Reminders for missing, stale, overdue, or incomplete knowledge.
- Audit trail for contributions and changes.

### 6.3. Knowledge lifecycle

- Proposed, under-review, verified, active, superseded, deprecated, and rejected states.
- Version, validity interval, owner, reviewer, evidence, and review date.
- Human verification before organizational activation.
- Basic conflict and staleness handling.

### 6.4. Permission-aware assistant

- Search and question answering over authorized project knowledge.
- Answer, citations, status, owner, version, and last verified date.
- Permission filtering before retrieval and context construction.
- Explicit insufficient-evidence and unresolved-conflict responses.

### 6.5. Handover workflow

- Initiate departure or responsibility transfer for any leader or member.
- Analyze responsibilities, ownership, evidence, coverage, freshness, and concentration.
- Create required handover items and identify knowledge gaps.
- Generate gap-driven AI interview questions.
- Assign a successor and a scoped handover package.
- Track predecessor tasks, successor questions, unresolved gaps, and readiness.
- Require Team Leader or Project Manager confirmation before completion.

### 6.6. Evaluation

- A labeled dataset from one project scope.
- Expected answers and supporting evidence.
- Vector RAG, SAG, and Continuum validation baselines.
- Retrieval, answer, citation, permission, and handover metrics.
- Repeatable test runs with fixed model and retrieval configuration where possible.

## 7. Stretch goals

- Jira, GitHub, Google Drive, Confluence, or meeting-note connectors.
- Advanced conflict detection.
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
