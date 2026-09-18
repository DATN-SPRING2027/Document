# CONTINUUM AI ACTORS ROLES AND PERMISSIONS

## Document status

- Status: Accepted MVP baseline
- Date: 2026-09-18
- Scope: Knowledge continuity and handover for one software project with multiple teams
- Purpose: Define actors, persistent roles, temporary assignments, lifecycle states, authorization scopes, and the MVP permission matrix.

## 1. Authorization principle

Continuum AI does not determine access from a single role name. An authorization decision is calculated from:

```text
Effective permission
= persistent project role
+ project and team membership scope
+ explicit knowledge or handover assignment
+ source and resource ACL
+ membership lifecycle state
- explicit deny
```

Rules:

1. A user can hold more than one role in the same project.
2. Every role assignment has a scope such as project, team, module, process, or knowledge resource.
3. Explicit deny overrides inherited allow.
4. Source and document ACLs are inherited by extracted knowledge unless an authorized owner applies a stricter policy.
5. Authorization is enforced before retrieval. Restricted evidence must never enter the LLM context.
6. Frontend route guards improve user experience but never replace backend authorization.
7. Administrative access does not automatically grant permission to read confidential knowledge.

## 2. Project and team structure

```text
Software Project
|
+-- Project Manager
+-- Project Administrator
|
+-- Team A
|   +-- Team Leader
|   +-- Team Members
|
+-- Team B
    +-- Team Leader
    +-- Team Members
```

A project can contain multiple teams. A team can have one or more leaders and multiple members. Knowledge is primarily scoped to a project and may be further restricted to a team, module, process, role, or explicit user list.

## 3. Persistent human roles

### 3.1. PROJECT_MANAGER

The Project Manager is the actor responsible for continuity across the whole project and its teams.

Main responsibilities:

- Create and maintain the project-level knowledge continuity policy.
- View project-wide coverage, gaps, freshness, concentration, and handover progress within allowed ACLs.
- Initiate a handover when a leader or member leaves or changes responsibility.
- Assign or approve a successor.
- Coordinate handover across multiple teams.
- Escalate unresolved gaps and overdue reviews.
- Approve an explicit waiver when a required handover item cannot be completed.
- Review project-level audit and evaluation reports.

Restrictions:

- Project Manager access remains subject to confidential resource ACLs.
- The Project Manager must not verify specialized knowledge without an appropriate owner or SME assignment, except through an audited emergency policy.

### 3.2. TEAM_LEADER

The Team Leader is responsible for knowledge continuity inside an assigned team.

Main responsibilities:

- Define required knowledge for the team, modules, and recurring processes.
- Assign Knowledge Owners and SME reviewers.
- Monitor missing, outdated, conflicting, or concentrated knowledge.
- Review team-level Proposed Knowledge when authorized.
- Initiate and manage handover for team members.
- Propose or assign a successor within project policy.
- Confirm whether a handover package is ready for transfer.
- Follow up when required knowledge has not been updated.

Restrictions:

- Team Leader authority is limited to assigned teams and resources.
- A Team Leader cannot access another team's restricted knowledge without an explicit grant.

### 3.3. TEAM_MEMBER

Every project member is both a knowledge consumer and a knowledge contributor. Knowledge capture is not limited to leaders.

Main responsibilities:

- Search and ask questions over authorized project knowledge.
- Create or update knowledge related to assigned work.
- Record decisions, procedures, incidents, lessons learned, known issues, workarounds, dependencies, and ownership changes.
- Review AI-extracted claims originating from the member's work.
- Report outdated, incorrect, missing, or conflicting knowledge.
- Participate in scheduled knowledge reviews and AI interviews.
- Complete assigned handover items when leaving or changing responsibilities.

Restrictions:

- Members can only access knowledge allowed by project membership, team scope, role scope, and resource ACL.
- A member cannot activate or verify organizational knowledge solely because they created it.

### 3.4. PROJECT_ADMIN

The Project Administrator manages the technical configuration of Continuum AI for the project.

Main responsibilities:

- Manage project membership, team membership, and persistent role assignments.
- Configure connectors, data sources, ingestion settings, and retention policies.
- Manage permission policies and resource ACLs.
- View technical job status, connector errors, and security audit events.
- Revoke sessions or service credentials according to policy.

Restrictions:

- Project Administrator is not a default Knowledge Owner or SME.
- Technical administration does not grant automatic access to confidential source content.
- Administrative override, when allowed, must require a reason and produce an audit event.

### 3.5. PROJECT_MANAGER versus PROJECT_ADMIN

| Question | PROJECT_MANAGER | PROJECT_ADMIN |
| --- | --- | --- |
| Primary responsibility | Owns project continuity and handover outcomes across teams. | Operates access, integrations, ingestion, and security configuration for the project. |
| Typical decisions | Which knowledge is required, which gap is urgent, who takes over, and whether a handover is complete or needs a documented waiver. | Who has project/team membership and configured roles, which source connector runs, and which access policy is applied. |
| Knowledge content | Reads only content allowed by resource ACL; does not automatically verify specialized claims. | Reads metadata and technical status by default, not confidential content or business knowledge. |
| Handover | Initiates and coordinates handover, assigns or approves a successor, and accepts project-level risk. | Supports access setup and audit; does not decide whether knowledge has been transferred successfully. |

Example: when a Team Leader leaves, the Project Manager selects a successor and approves the transfer plan. The Project Admin sets up the successor's project/team access and keeps the configuration and audit trail correct. Neither role alone bypasses source ACL or becomes a Knowledge Owner/SME.

## 4. Assignments and lifecycle states

The following concepts affect permissions but are not global hierarchical roles.

### 4.1. SUBJECT_MATTER_EXPERT assignment

An SME assignment states that a user can review a specified domain, module, process, or knowledge requirement.

```text
SME assignment
- userId
- projectId
- teamId optional
- scopeType
- scopeId
- validFrom
- validUntil optional
- assignedBy
```

An SME may answer gaps, participate in AI interviews, review conflicts, and verify knowledge only inside the assigned scope.

### 4.2. KNOWLEDGE_OWNER assignment

A Knowledge Owner assignment identifies accountability for a Knowledge Object, requirement, process, module, or source.

The owner can:

- Review, edit, approve, reject, deprecate, or supersede knowledge in scope.
- Assign reviewers.
- Set review intervals.
- Resolve conflicts with evidence and an audit reason.

Ownership must not be inferred only from document authorship or job title.

### 4.3. SUCCESSOR assignment

A Successor is a member assigned to take over a responsibility, module, process, or position from another member.

The assignment grants access only to the approved handover scope and does not automatically grant all permissions held by the departing member.

```text
Successor assignment
- handoverId
- predecessorId
- successorId
- responsibilityScope
- accessScope
- assignedBy
- validFrom
- reviewAt optional
```

The successor can view the assigned handover package, follow the recommended knowledge path, ask scoped questions, and report unresolved gaps.

### 4.4. ONBOARDING MEMBER state

An onboarding member is a `TEAM_MEMBER` whose membership state is `ONBOARDING`. This state enables an onboarding or takeover plan but does not create a separate RBAC role.

### 4.5. DEPARTING MEMBER state

A departing member is a `TEAM_MEMBER` or `TEAM_LEADER` whose membership state is `OFFBOARDING`.

The state triggers:

- Responsibility and ownership analysis.
- Knowledge coverage analysis.
- Required handover items.
- Gap-driven AI interview.
- Successor assignment and handover progress tracking.

The departing member retains only the access necessary to complete work and handover until the configured end date. Access is revoked or reduced automatically when the membership ends.

## 5. System actors

### 5.1. AI_ORCHESTRATOR

The AI Orchestrator may extract, classify, summarize, detect gaps, propose interview questions, and generate evidence-grounded answers. It cannot:

- Grant permissions.
- Mark knowledge VERIFIED or ACTIVE.
- Resolve a critical conflict by itself.
- Assign a successor by itself.
- Read evidence outside the authorization scope supplied by the backend.

### 5.2. INGESTION_WORKER

The ingestion worker processes authorized sources, parses documents, creates retrieval indexes, and records job status. It uses a service account with minimum permissions and cannot impersonate a human reviewer.

### 5.3. SCHEDULER_AND_REMINDER

The scheduler detects overdue knowledge, missing required artifacts, incomplete handover items, and review deadlines. It creates notifications or follow-up tasks but does not punish or score employees.

## 6. MVP permission matrix

Legend: `Yes` means allowed within scope, `Assigned` requires an explicit assignment, `Limited` means metadata or authorized scope only, and `No` means denied by default.

| Action | Project Manager | Team Leader | Team Member | Project Admin | SME assignment | Owner assignment | Successor assignment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| View authorized knowledge | Yes | Yes | Yes | Limited | Assigned | Assigned | Assigned |
| Ask AI over authorized evidence | Yes | Yes | Yes | Limited | Assigned | Assigned | Assigned |
| Propose knowledge | Yes | Yes | Yes | No | Assigned | Assigned | No |
| Update own draft or proposed knowledge | Yes | Yes | Yes | No | Assigned | Assigned | No |
| Verify or reject knowledge | Limited | Yes | No | No | Assigned | Assigned | No |
| Deprecate or supersede knowledge | Limited | Yes | No | No | Assigned | Assigned | No |
| Resolve a knowledge conflict | Limited | Yes | No | No | Assigned | Assigned | No |
| Define required team knowledge | Limited | Yes | No | No | Consulted | Assigned | No |
| Report a gap or outdated item | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Initiate team-member handover | Yes | Yes | No | No | No | No | No |
| Initiate team-leader handover | Yes | No | No | No | No | No | No |
| Assign successor | Yes | Yes | No | No | No | No | No |
| View handover package | Yes | Yes | Limited | Limited | Assigned | Assigned | Assigned |
| Complete handover items | No | Yes | Yes | No | Assigned | Assigned | Yes |
| Confirm handover readiness | Yes | Yes | No | No | Consulted | Consulted | No |
| View continuity dashboard | Project | Team | Own or limited | Technical | Assigned | Assigned | Own handover |
| Manage members and persistent roles | Limited | No | No | Yes | No | No | No |
| Manage connectors and source ACL | No | No | No | Yes | No | No | No |
| View audit logs | Project | Team | Own actions | Security and technical | Assigned | Assigned | Own handover |

Every `Limited`, `Project`, `Team`, `Assigned`, and `Own` cell still requires backend evaluation of the resource ACL.

## 7. Required permission codes

```text
project.read
project.manage_continuity
project.view_continuity

team.read
team.manage_knowledge_requirements
team.manage_handover

knowledge.read
knowledge.propose
knowledge.edit_proposed
knowledge.verify
knowledge.reject
knowledge.deprecate
knowledge.supersede
knowledge.resolve_conflict

gap.read
gap.report
gap.assign
gap.resolve

interview.participate
interview.manage
interview.read_transcript

handover.initiate
handover.assign_successor
handover.read
handover.complete_item
handover.confirm_ready
handover.waive_requirement

source.create
source.ingest
source.manage_acl

member.manage
role.assign
audit.read
integration.manage
```

Backend policies must check permission codes and scope. Application code must not rely on broad conditions such as `role === "ADMIN"` for sensitive actions.

## 8. Required knowledge contribution by actor

| Actor | Required ongoing contribution |
| --- | --- |
| Project Manager | Project decisions, cross-team dependencies, milestones, major risks, responsibility changes, and handover approvals |
| Team Leader | Team processes, module ownership, operating procedures, required knowledge, unresolved gaps, review schedules, and successor recommendations |
| Team Member | Work decisions, implementation notes, incidents, lessons learned, known issues, workarounds, dependencies, and current responsibility status |
| Knowledge Owner | Verified versions, validity dates, evidence, review results, supersession reasons, and conflict decisions |
| SME assignee | Expert review, gap answers, interview claims, exceptions, warnings, and evidence-backed clarifications |
| Successor assignee | Questions, unresolved gaps, learning progress, takeover confirmation, and post-handover corrections |

## 9. Audit requirements

The system must audit at least:

- Persistent role assignment and removal.
- SME, Knowledge Owner, and Successor assignment changes.
- Membership lifecycle changes.
- Permission and ACL changes.
- Handover initiation, waiver, confirmation, and completion.
- Knowledge verification, rejection, deprecation, supersession, and conflict resolution.
- Access to sensitive knowledge and interview transcripts.
- Administrative overrides and their reasons.

## 10. MVP exclusions

The MVP does not include:

- Enterprise-wide HR role management.
- Employee performance scoring.
- Automatic disciplinary actions for missing knowledge updates.
- AI-controlled permission grants.
- Automatic successor assignment without human approval.
- Global administrator access to all confidential content by default.
