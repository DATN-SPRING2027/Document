# CAPSTONE PROJECT REPORT

## Report 3 – Software Requirement Specification

**Project:** Continuum AI — AI-Powered Platform for Continuous Project Knowledge Capture, Verification and Handover

**Class:** [Class Code - TBD]

**Members:**
- [Member 1 - TBD]
- [Member 2 - TBD]
- [Member 3 - TBD]
- [Member 4 - TBD]

**Instructor:** [Instructor Name - TBD]

— DaNang, September 2026 —

> **Governance amendment — 2026-10-02:** This approved access model supersedes conflicting role and Project-create statements in this September report. `PLATFORM_OPERATOR` is a platform-scoped actor; it provisions Organizations, bootstraps the first Organization Admin, and monitors platform health/configuration, but receives no default Organization membership or internal-content access. `ADMIN` manages Organization users/membership, roles/scopes and Organization settings, but receives no default confidential-content access. `TEAM_LEADER` manages only explicitly assigned Project/Team scope. `MEMBER` works within active membership, assigned scope and resource ACL. `OrganizationMembership=ACTIVE` is authoritative for Organization Context. Any authenticated User with active membership in the trusted matching Organization may create a `PRIVATE` Project; no role or `project.create` grant is required, and the creator receives active Project Membership plus project-scoped `MEMBER` assignment. See the current [Actors, Roles & Permissions](../../research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md), [Organization and Workspace Access Contract Readiness](../../research-docs/Workspace/00-organization-and-access-contract-readiness.md) and the approved BE decision records for DEC-016 and Project Foundation. Detailed action-level permissions, invitation/lifecycle states and any retained non-Project-create capability grants remain subject to their own contract decisions.

---

## Table of Contents

- [I. Record of Changes](#i-record-of-changes)
- [II. Software Requirement Specification](#ii-software-requirement-specification)
  - [1. Product Overview](#1-product-overview)
  - [2. User Requirements](#2-user-requirements)
  - [3. Functional Requirements](#3-functional-requirements)
  - [4. Non-Functional Requirements](#4-non-functional-requirements)
  - [5. Requirement Appendix](#5-requirement-appendix)

---

# I. Record of Changes

*A - Added M - Modified D - Deleted

| Date | A/M/D | In charge | Change Description |
|------|-------|-----------|-------------------|
| 22/09/2026 | A | [Member 1] | Create the software requirement specification |
| 22/09/2026 | A | [All Members] | Add the system's entity relationship diagram |
| 22/09/2026 | A | [All Members] | Add use case diagrams and screen flows |
| 22/09/2026 | A | [All Members] | Add functional requirements for all modules |
| 02/10/2026 | M | [All Members] | Amend governance hierarchy, Organization Context, confidential-content boundary, and Project creation rule; this amendment supersedes conflicting grant-based Project requirements below |

---

# II. Software Requirement Specification

## 1. Product Overview

Continuum AI is an AI-powered platform designed to solve the critical problem of **knowledge loss** when team members leave a software project, change teams, or transfer responsibilities. Unlike traditional documentation tools, Continuum AI provides a structured workflow that captures, verifies, maintains, and transfers knowledge continuously throughout the project lifecycle.

Continuum owns the canonical task lifecycle through its Task API. Work Notes and handover workflows may reference a task by `taskId`; they do not synchronize their canonical tasks from Jira. The platform uses AI (Gemini/OpenAI) for knowledge extraction and evidence-grounded question answering, and supports handover workflows with audio interviews and successor learning paths.

**Key capabilities:**
- Continuous daily knowledge capture linked to Continuum-owned work context
- Human-verified knowledge lifecycle (Proposed → Verified → Active)
- Permission-aware AI chat assistant with mandatory citations
- Structured handover workflow with gap analysis
- Role-based access control with a separate platform operations actor and 3 Organization/Project roles

**Context Diagram:**

> *See Figure 1: Context Diagram (01_context_diagram.drawio)*

---

## 2. User Requirements

### 2.1 Actors

| # | Actor | Description |
|---|-------|-------------|
| 1 | **Platform Operator** | Platform-scoped operator who runs the platform, provisions Organizations, bootstraps the first Organization Admin, and monitors platform health/configuration. This actor is not an Organization role and has no default Organization membership or internal-content access. |
| 2 | **Admin** | Organization administrator who manages Organization Users/Memberships, assigns Organization roles/scopes, and manages Organization settings/policy. The role alone grants no Project/Team Membership and no confidential-content access. |
| 3 | **Team Leader** | Manages only explicitly assigned Project/Team scopes and the workflows delegated within those scopes. The role alone grants no access outside assigned scope and cannot self-expand its authority. Also contributes as a member where separately enrolled. |
| 4 | **Member** | Contributor who works within active Organization/Project/Team Membership, explicit scope and resource ACL. May capture work, contribute evidence and use knowledge workflows only for resources they are authorized to access. |

**Authorization rule:** Actor labels below identify possible workflow participants; they do not bypass active membership, assigned scope, resource ACL, lifecycle checks or explicit deny. An Admin or Platform Operator may access Project content only through a separate, explicit authorization path; the role itself does not provide it.

### 2.2 Use Cases

#### 2.2.1 Diagram(s)

##### 2.2.1.1: Overall Use-Case

> *See Figure 2: Overall Use Case Diagram (02_usecase_overall.drawio)*

##### 2.2.1.2: Authentication Use-Case

> *See Figure 3: Authentication Use Case (03_usecase_authentication.drawio)*

##### 2.2.1.3: Admin Use-Case

> *See Figure 4: Admin Use Case (04_usecase_admin.drawio)*

##### 2.2.1.4: Team Leader Use-Case

> *See Figure 5: Team Leader Use Case (05_usecase_team_leader.drawio)*

##### 2.2.1.5: Member Use-Case

> *See Figure 6: Member Use Case (06_usecase_member.drawio)*

#### 2.2.2 Descriptions

| ID | Use Case | Actors | Use Case Description |
|----|----------|--------|---------------------|
| 01 | Login | Admin, Team Leader, Member | Allows users to authenticate using email and password credentials to access the system. Creates JWT access token with scoped claims. |
| 02 | Logout | Admin, Team Leader, Member | Allows users to securely terminate their session by invalidating tokens and adding JTI to Redis blacklist. |
| 03 | Refresh Token | Admin, Team Leader, Member | Automatically refreshes expired access tokens using refresh token rotation with reuse detection. |
| 04 | Forgot Password | Admin, Team Leader, Member | Allows users to reset their password via email link when forgotten. Generates a time-limited reset token. |
| 05 | Change Password | Admin, Team Leader, Member | Allows authenticated users to update their password by providing current and new passwords. |
| 06 | Enable/Disable 2FA | Admin, Team Leader, Member | Allows users to enable or disable TOTP-based two-factor authentication for enhanced security. |
| 07 | View Personal Profile | Admin, Team Leader, Member | Allows users to view their personal profile information including name, email, avatar, and role assignments. |
| 08 | Edit Personal Profile | Admin, Team Leader, Member | Allows users to update their profile information such as full name and avatar. |
| 09 | Provision Organization and Bootstrap First Admin | Platform Operator | Provisions an Organization and bootstraps its first Admin. This does not grant the operator Organization membership or content access. |
| 10 | Create Project | Any authenticated User with active Organization Membership | Creates a `PRIVATE` Project in the matching trusted Organization Context. No role or `project.create` grant is required; creator bootstrap is defined in the Project Foundation decision. |
| 11 | View Project List | User with active Project Membership | Displays only Projects the user is authorized to discover, with filtering and pagination. |
| 12 | View Project Detail | User with active Project Membership and applicable ACL | Shows only Project details and content permitted by the user's scope and resource ACL. |
| 13 | Update Project | Team Leader assigned to that Project, within explicit scope | Allows permitted Project updates; role without assignment does not authorize the operation. |
| 14 | Create Team | Team Leader assigned to the Project, within explicit scope | Creates a Team within a Project when the applicable scope and policy authorize it. |
| 15 | Add Team Member | Authorized Team Leader within the Project/Team scope | Adds a member only when the applicable membership and delegation policy authorize the operation. |
| 16 | Remove Team Member | Authorized Team Leader within the Project/Team scope | Removes a member only when the applicable membership and delegation policy authorize the operation. |
| 17 | Assign Organization Role / Scope | Admin | Assigns Organization-level roles/scopes within Organization administration authority; Project/Team membership and content access remain separately governed. |
| 18 | Manage Organization Membership | Admin | Manages Organization membership lifecycle. Exact invitation, activation and removal transitions remain governed by the Organization Membership contract. |
| 19 | Revoke Capability | Admin | Revokes a previously granted capability with audit trail. |
| 20 | Assign SME / Knowledge Owner | Admin, Team Leader | Assigns scoped SME or Knowledge Owner assignments to team members for specific domains/modules. |
| 21 | Configure External Source Connector (Future) | Authorized Organization administrator | Third-party source connectors are outside the current task-management MVP and require a separate approved contract. Jira is not the canonical task source. |
| 22 | Manage Continuum Tasks | Authorized Project member / Team Leader in assigned scope | Proposed task-management use case; Continuum Task API is the canonical task source. Exact task actions and permission matrix remain subject to approval in the Task Use Cases document. |
| 23 | View Continuum Task | Task actor allowed by the approved Task policy | Proposed use case; shows only task details and history authorized by the Task API. No Jira issue synchronization is part of the current task-source decision. |
| 24 | Create Daily Work Note | Team Leader, Member | Creates a structured daily work note with What/How/Why fields, optional `taskId` link, and evidence links. |
| 25 | Edit Work Note | Team Leader, Member | Edits a previously created work note (only own notes, before confirmation). |
| 26 | Confirm Work Note | Team Leader, Member | Author confirms the work note content, making it eligible for knowledge extraction. |
| 27 | View Work Note History | Team Leader, Member | Displays version history of a work note with immutable audit trail. |
| 28 | Propose Knowledge | Team Leader, Member | Creates a knowledge proposal from work notes, documents, or manual entry with evidence references. |
| 29 | View Verification Inbox | Team Leader, SME | Displays pending knowledge proposals requiring review within the user's authorized scope. |
| 30 | Verify/Reject Knowledge | Team Leader, SME | Reviews and approves or rejects a knowledge proposal with feedback. Uses ACID multi-document transaction. |
| 31 | View Knowledge Objects | Project/Team member with applicable scope and source ACL | Browses only knowledge objects the actor is authorized to access. |
| 32 | View Knowledge Gaps | Project/Team member with applicable scope and source ACL | Displays only knowledge gaps within the actor's authorized scope. |
| 33 | Supersede Knowledge | Team Leader, Knowledge Owner | Creates a new version of existing knowledge, moving the old version to SUPERSEDED status. |
| 34 | Create Chat Session | Project/Team member with applicable scope and source ACL | Initiates a chat session in an authorized Project scope with permission-aware retrieval. |
| 35 | Ask Question (with Citations) | Project/Team member with applicable scope and source ACL | Receives evidence-grounded answers only from authorized evidence. If evidence is insufficient, returns `INSUFFICIENT_EVIDENCE`. |
| 36 | Report Knowledge Gap | Project/Team member with applicable scope and source ACL | Creates a gap report from an unanswered or insufficiently answered question in the authorized scope. |
| 37 | View Chat History | Session owner or separately authorized actor | Browses only chat history and citations the actor is permitted to access. |
| 38 | Initiate Handover | Team Leader assigned to the relevant Project/Team, or another explicitly scoped actor | Starts a handover within authorized scope when a member departs or transfers responsibility. |
| 39 | View Handover Package | Team Leader within scope, or assigned Successor | Views only the handover package and evidence authorized for that actor. |
| 40 | Sign-off Handover Item | Team Leader within assigned scope or explicitly authorized reviewer | Confirms an item only when explicitly authorized; Admin role alone is not sufficient. |
| 41 | Audio Interview Recording | Team Leader | Conducts an audio interview via WebSocket streaming, which is stored in Cloudflare R2 and transcribed via Whisper API. |
| 42 | View Successor Learning Path | Member (Successor) | Views the auto-generated learning path tailored for the successor's onboarding scope. |
| 43 | Upload Document | Project/Team member with applicable scope and upload policy | Uploads an authorized source via a time-limited upload URL for ingestion. |
| 44 | View Documents | Project/Team member with applicable scope and source ACL | Browses only documents authorized by membership, scope and ACL. |
| 45 | View Ingestion Status | Source owner or separately authorized actor | Checks processing status without exposing restricted source content. |
| 46 | Manage Source ACL | Authorized policy administrator or Team Leader within assigned scope | Configures source access policy within delegated scope. This does not itself grant access to the protected content. |
| 47 | View Notifications | Admin, Team Leader, Member | Displays in-app and email notifications including knowledge reviews, handover updates, and daily reminders. |
| 48 | Mark Notification as Read | Admin, Team Leader, Member | Marks one or more notifications as read. |
| 49 | Manage User Accounts | Admin | Views, creates, suspends, or activates user accounts. Includes invite flow for new users. |
| 50 | View Audit Logs | Admin, Team Leader (scoped) | Views immutable audit trail of system actions within authorized scope. |

---

## 3. Functional Requirements

### 3.1 System Functional Overview

#### 3.1.1 Screens Flow

##### 3.1.1.1 Screens Flow of Admin

> *See Figure 7: Screen Flow of Admin (07_screenflow_admin.drawio)*

##### 3.1.1.2 Screens Flow of Team Leader

> *See Figure 8: Screen Flow of Team Leader (08_screenflow_team_leader.drawio)*

##### 3.1.1.3 Screens Flow of Member

> *See Figure 9: Screen Flow of Member (09_screenflow_member.drawio)*

#### 3.1.2 Screen Descriptions

| # | Feature | Screen | Description |
|---|---------|--------|-------------|
| 1 | Authentication | Login | Screen for users to enter email and password. Supports all three roles. Redirects to role-specific dashboard after successful authentication. |
| 2 | Authentication | Forgot Password | Screen where users enter their registered email to receive a password reset link. |
| 3 | Authentication | Change Password | Screen for authenticated users to update their password by entering current and new passwords. |
| 4 | Dashboard | Admin Dashboard | Organization administration overview: Organization users/membership and policy events. It does not include Project content or platform health unless separately authorized. |
| 5 | Dashboard | Team Leader Dashboard | Overview of team activity: pending verifications, knowledge gaps, handover status, recent work notes from team members, and daily note completion rates. |
| 6 | Dashboard | Member Dashboard | Personal overview: today's work note status, recent notifications, knowledge contribution stats, assigned handover items, and quick access to AI chat. |
| 7 | User Management | User List | Paginated view of Organization membership and role/scope status. Admin can manage Organization membership within the approved lifecycle contract. |
| 8 | User Management | User Detail / Edit | Organization-scoped identity and role/scope details. Project content and activity are not exposed solely by the Admin role. |
| 9 | User Management | Invite User | Organization membership onboarding screen; invitation mechanism and status transitions remain to be decided. |
| 10 | Organization | Organization Settings | View and edit organization name, slug, plan, and global settings. |
| 11 | Project Management | Project List | Shows only Projects discoverable through the user's active Project Membership and access policy. |
| 12 | Project Management | Project Detail | Displays Project details only within the user's active Project/Team scope and resource ACL. |
| 13 | Team Management | Team List | Lists Teams only for Project/Team scopes the user is authorized to manage or view. |
| 14 | Team Management | Team Detail / Members | Shows membership and scoped assignments only to actors authorized for that Project/Team scope. |
| 15 | Role & Scope | Organization Role & Scope Management | Lets an Admin assign permitted Organization roles/scopes. It does not grant Project content access or make `project.create` a gate. |
| 16 | External Sources (Future) | Connector Configuration | Future connector configuration, only if a separate source integration is approved; this does not make an external system the task source. |
| 17 | Daily Capture | Work Notes List | Chronological list of work notes with status (Draft/Confirmed), date, and optional linked Continuum task. |
| 18 | Daily Capture | Create/Edit Work Note | Structured form with What/How/Why fields, optional Continuum `taskId`, evidence links, and blocker/next-step fields. |
| 19 | Daily Capture | Confirm Note | Confirmation dialog where the author reviews and confirms their work note content. |
| 20 | Knowledge | Verification Inbox | Queue of pending knowledge proposals for the reviewer's authorized scope. Shows title, domain, proposer, and submitted date. |
| 21 | Knowledge | Knowledge Review Detail | Detailed view of a knowledge proposal with content, evidence, proposer info, and approve/reject actions with feedback. |
| 22 | Knowledge | Knowledge Objects | Browsable list of verified knowledge with filters by domain, status, owner, and date range. |
| 23 | Knowledge | Knowledge Gaps | List of identified knowledge gaps with source (chat question, overdue review, missing coverage) and priority. |
| 24 | Chat | AI Chat Assistant | Chat interface for asking project knowledge questions. Shows responses with inline citations, evidence status, and 1-click gap reporting. |
| 25 | Chat | Chat History | List of previous chat sessions with last message preview and timestamp. |
| 26 | Handover | Handover Management | List of active and completed handover processes with status, predecessor/successor, and completion percentage. |
| 27 | Handover | Handover Package Detail | Detailed checklist of handover items with priority, status, sign-off tracking, and knowledge gap indicators. |
| 28 | Handover | Audio Interview | WebSocket-based audio recording interface for conducting handover interviews. Shows transcript after Whisper processing. |
| 29 | Handover | Successor Learning Path | Auto-generated learning path for successor with prioritized knowledge items, required readings, and progress tracking. |
| 30 | Documents | Documents Library | Grid/list of uploaded documents with file type, upload date, ingestion status, and source ACL info. |
| 31 | Documents | Upload Document | Drag-and-drop upload interface with file type validation (PDF, DOCX, MD, TXT, Image) and automatic presigned URL generation. |
| 32 | Documents | Ingestion Status | Progress tracking for document processing: upload → OCR → chunking → embedding → indexed. |
| 33 | Notifications | Notification Center | Chronological list of in-app notifications with read/unread status and action links. |
| 34 | Profile | Personal Profile | View personal information: name, email, avatar, role assignments, team memberships. |
| 35 | Profile | Edit Profile | Form to update full name, upload avatar, and manage 2FA settings. |
| 36 | Audit | Audit Logs | Searchable, filterable audit trail with action type, actor, resource, timestamp, and metadata. |

#### 3.1.3 Screen Authorization

An `X` below is only a role-eligible path, never authorization by role alone. Active Organization/Project/Team Membership, explicit scope, resource ACL, lifecycle state and explicit deny are still checked by the backend. Admin and Platform Operator do not gain confidential content access from their administrative/platform roles; an Admin who independently has Project membership and resource ACL acts under that separate authorization.

| Screen | Platform Operator | Admin | Team Leader | Member |
|--------|-------------------|-------|-------------|--------|
| Login / password / personal profile | X | X | X | X |
| Platform Operations Dashboard | X | | | |
| Provision Organization / Bootstrap First Admin | X | | | |
| Admin Dashboard (Organization administration only) | | X | | |
| Team Leader Dashboard | | | X (scoped) | |
| Member Dashboard | | | | X (scoped) |
| Organization User / Membership Management | | X | | |
| Organization Settings / Roles & Scopes | | X | | |
| Project List / Detail | | | X (scoped) | X (membership + ACL) |
| Team List / Detail / Membership | | | X (assigned scope) | X (membership + ACL) |
| Work Notes / Knowledge / Chat / Documents | | | X (scoped + ACL) | X (membership + ACL) |
| Verification Inbox / Knowledge Review | | | X (authorized reviewer) | X (only if separately assigned reviewer) |
| Handover Management | | | X (assigned scope) | X (assigned predecessor/successor scope) |
| Audio Interview | | | X (assigned scope) | |
| Successor Learning Path | | | | X (assigned successor scope) |
| Notifications / Personal Profile | X | X | X | X |
| Audit Logs | X (platform events only) | X (Organization administration events) | X (authorized scope only) | |

This table is a high-level screen map, not the final action-level permission matrix. Platform health/configuration and Organization content are separate data scopes.

#### 3.1.4 Non-Screen Functions

| # | Feature | System Function | Description |
|---|---------|-----------------|-------------|
| 1 | Authentication | JWT Token Validation | Background middleware that validates JWT access tokens on every API request, extracting scoped claims (userId, orgId, roles, projectIds). |
| 2 | Authentication | Token Blacklist Check | Redis-based check (<1ms) to verify that the token's JTI has not been invalidated by logout. |
| 3 | Authentication | Refresh Token Rotation | Automatic rotation of refresh tokens with reuse detection to prevent replay attacks. |
| 4 | Knowledge Capture | Daily Note Reminder | Cronjob at 17:30 that sends email reminders to team members who haven't confirmed their daily work note. |
| 5 | Knowledge Lifecycle | Knowledge Gap Scanner | Periodic scanner that identifies modules/domains with overdue reviews (exceeding `cadenceDays`) and creates knowledge gap records. |
| 6 | Knowledge Lifecycle | AI Knowledge Extraction | Background worker that extracts proposed knowledge objects from confirmed work notes and ingested documents using LLM. |
| 7 | Task Management | Task Lifecycle Events | Task service publishes only events defined by the approved Task API/event contract; this report does not prescribe event names or payloads. |
| 8 | Task Management | Task Event Consumption | Downstream services resolve tasks through Task API/event contracts and must not query Task collections directly. |
| 9 | Document Ingestion | OCR & Chunking Worker | Background worker that processes uploaded documents through OCR (MarkItDown/MinerU), chunks text, generates embeddings, and indexes into vector store. |
| 10 | Notification | Email Delivery Service | BullMQ consumer for `mail-queue` that sends transactional emails via SMTP/Resend for account activation, password reset, and knowledge alerts. |
| 11 | Notification | Real-time Push | Redis Pub/Sub channel (`user:notify:{userId}`) that pushes in-app notifications to connected WebSocket clients. |
| 12 | Handover | Audio Transcription Worker | Background worker that processes audio recordings from handover interviews through Whisper API for speech-to-text transcription. |
| 13 | Chat | Pre-Retrieval ACL Filter | Computes effective permissions ($P_{eff}$) before querying the vector database to prevent unauthorized knowledge leakage. |

#### 3.1.5 Entity Relationship Diagram

> *See Figure 10: Entity Relationship Diagram (10_erd.drawio)*

**Entities Description:**

| # | Entity | Description |
|---|--------|-------------|
| 1 | users | Represents a system user account with email, password hash (Bcrypt 12 rounds), full name, avatar, status (ACTIVE/SUSPENDED/PENDING_INVITE), and optional 2FA configuration. |
| 2 | organizations | Represents a top-level organization (multi-tenant) with name, slug, plan (FREE/ENTERPRISE), and settings. |
| 3 | projects | Represents a Project within an Organization. Created by any authenticated User with `OrganizationMembership=ACTIVE` in the matching trusted Organization Context; starts `PRIVATE`, with creator Project Membership and project-scoped `MEMBER` assignment bootstrapped atomically. |
| 4 | teams | Represents a team within a project. Contains name, code, and references to organization and project. |
| 5 | work_notes | Represents a daily work note capturing What/How/Why, blockers, next steps, and evidence. Linked to author, project and team, with an optional logical `taskId` reference to the Continuum Task API. Status: DRAFT or CONFIRMED. |
| 6 | knowledge_objects | Represents a verified knowledge item with title, domain, category, content, lifecycle status (PROPOSED → UNDER_REVIEW → VERIFIED → ACTIVE → SUPERSEDED → DEPRECATED), version tracking, validity period, and review cadence. |
| 7 | chat_sessions | Represents an AI chat conversation with user, project scope, title, status, and scope filter for permission-aware retrieval. |
| 8 | handovers | Represents a handover process with predecessor/successor users, project/team scope, status (INITIATED → IN_PROGRESS → COMPLETED), reason, and timeline. |
| 9 | sources | Represents an uploaded document/file with metadata (filename, mimeType, size), Cloudflare R2 object key, SHA-256 hash for deduplication, and uploader reference. |
| 10 | tasks | Canonical operational tasks owned by Continuum Task API and stored in MongoDB. Work Notes and handover flows may retain an optional logical `taskId`; SAG stores only permitted derived Work Note/evidence for retrieval. |
| 11 | notifications | Represents an in-app or email notification with recipient, type, title, message, read status, and related resource reference. |
| 12 | audit_logs | Immutable audit trail recording actions, actors, resource types/IDs, metadata, and timestamps. Append-only for SOC2/ISO compliance. |

---

### 3.2 User Account & Authentication Management

#### 3.2.1 Login

**Function trigger:** User navigates to the login page and submits email and password.

**Function description:**

**Actors:** Authenticated User (including Platform Operator)

**Purpose:** Allow users to authenticate and gain access to the system with JWT-based session management.

**Data Processing:**
1. Validate input fields (email format, non-empty password).
2. Verify credentials against stored user records (Bcrypt hash comparison, 12 rounds).
3. Check account status (must be ACTIVE, not SUSPENDED or PENDING_INVITE).
4. If 2FA is enabled, prompt for TOTP code and verify.
5. Generate JWT access token with scoped claims (userId, orgId, roles, projectIds).
6. Create refresh session record with token rotation support.

**Screen layout:**

> *[Screenshot placeholder: Login Page]*

**Function Details:**

**Validation:**
- Email must be in valid format and exist in the system.
- Password must not be empty and must match the stored password hash.
- Account status must be ACTIVE.
- If 2FA enabled, TOTP code must be valid and not expired.

**Business Rules:**
- JWT access token expires in 15 minutes.
- Refresh token expires in 7 days with automatic rotation.
- Failed login attempts are logged in audit trail.
- Token contains scoped claims: userId, organizationId, roles[], projectIds[].

**Functionalities:**

**Normal case:**
1. The user enters the correct email and password.
2. System authenticates credentials via Bcrypt comparison.
3. System generates JWT access token and refresh token.
4. The user is redirected to the role-specific dashboard with the message "Login successful."

**Abnormal case:**
1. If email not found: System shows error ("Account does not exist.")
2. If password is incorrect: System shows error ("Incorrect password.")
3. If account is SUSPENDED: System shows error ("Account has been suspended. Contact your administrator.")
4. If account is PENDING_INVITE: System shows error ("Please complete your account activation first.")
5. If 2FA code is invalid: System shows error ("Invalid two-factor authentication code.")

---

#### 3.2.2 Logout

**Function trigger:** Authenticated user clicks on the logout button.

**Function description:**

**Actors:** Authenticated User (including Platform Operator)

**Purpose:** Allow users to securely terminate their active session by invalidating tokens.

**Data Processing:**
1. Extract JTI (JWT ID) from the current access token.
2. Add JTI to Redis token blacklist with TTL matching token expiry.
3. Invalidate the refresh session in database.
4. Clear client-side token storage.

**Screen layout:**

> *[Screenshot placeholder: Logout confirmation]*

**Function Details:**

**Validation:**
- User must have an active, valid session.
- Token JTI must not already be blacklisted.

**Business Rules:**
- Once logged out, the token cannot be reused (Redis blacklist check <1ms).
- Users must re-enter credentials to access the system again.
- Refresh token is invalidated in the database to prevent reuse.
- Logout action is recorded in the audit trail.

**Functionalities:**

**Normal case:**
1. The user clicks the logout button.
2. System adds JTI to Redis blacklist.
3. System invalidates the refresh session.
4. The user is redirected to the login page with the message "Logout successful."

**Abnormal case:**
1. If no active session is found: System shows error ("No active session found.")
2. If token is already invalidated: System redirects to login page silently.

---

#### 3.2.3 Forgot Password

**Function trigger:** User clicks "Forgot password" on the login page and submits registered email.

**Function description:**

**Actors:** User with an account

**Purpose:** Allow users to reset their password securely when they forget it.

**Data Processing:**
1. Validate email format and check if it exists in the system.
2. Generate a secure password reset token with expiration (1 hour).
3. Send a reset link to the user's email via SMTP/Resend.
4. Log the password reset request in audit trail.

**Screen layout:**

> *[Screenshot placeholder: Forgot Password Page]*

**Function Details:**

**Validation:**
- Email must be in valid format.
- Email must exist in the system and account must be ACTIVE.
- Reset tokens must be valid and not expired.

**Business Rules:**
- Reset token expires in 1 hour.
- Only one active reset token per user at a time (previous tokens are invalidated).
- Password reset request is logged for auditing.
- Rate limiting: maximum 3 reset requests per email per hour.

**Functionalities:**

**Normal case:**
1. The user enters a registered email.
2. The system generates a secure reset token.
3. The system sends a reset link via email.
4. The user receives the message "Password reset link has been sent to your email."

**Abnormal case:**
1. If email not found: System shows generic message "If the email exists, a reset link has been sent." (prevents email enumeration)
2. If reset token expired: System shows error ("Reset link expired, please request again.")
3. If rate limit exceeded: System shows error ("Too many reset requests. Please try again later.")
4. If email service fails: System logs error and shows "Failed to send reset link. Please try again."

---

#### 3.2.4 Change Password

**Function trigger:** Authenticated user navigates to the change password page and submits current password along with a new password.

**Function description:**

**Actors:** Admin, Team Leader, Member

**Purpose:** Allow users who are logged in to update their password securely.

**Data Processing:**
1. Verify current password against stored hash.
2. Validate new password meets complexity requirements.
3. Validate new password matches confirmation.
4. Update password hash (Bcrypt 12 rounds) in database.
5. Invalidate all existing refresh sessions (force re-login on other devices).

**Screen layout:**

> *[Screenshot placeholder: Change Password Page]*

**Function Details:**

**Validation:**
- The current password must match the stored password hash.
- New password and confirmation must match.
- New password must meet complexity requirements (minimum 8 characters, at least 1 uppercase, 1 lowercase, 1 number, 1 special character).
- New password must differ from the current password.

**Business Rules:**
- Password change requires the user to be authenticated.
- Password is securely hashed using Bcrypt (12 rounds) before storage.
- All existing sessions are invalidated after password change (security best practice).
- Password change is logged in audit trail.

**Functionalities:**

**Normal case:**
1. The user provides the correct current password and a valid new password.
2. System verifies current password and validates the new password.
3. System updates the password hash in database.
4. System invalidates all existing sessions.
5. The system displays "Password changed successfully. Please log in again."

**Abnormal case:**
1. If current password incorrect: System shows error ("Current password is incorrect.")
2. If new passwords do not match: System shows error ("New password and confirmation do not match.")
3. If new password not strong enough: System shows error ("Password must contain at least 8 characters with uppercase, lowercase, number, and special character.")
4. If new password same as current: System shows error ("New password must be different from current password.")

---

#### 3.2.5 View Personal Profile

**Function trigger:** User clicks on profile avatar or "My Profile" menu item.

**Function description:**

**Actors:** Admin, Team Leader, Member

**Purpose:** Display the user's personal information, role assignments, and team memberships.

**Data Processing:**
1. Retrieve user data from database.
2. Fetch role assignments and team memberships.
3. Calculate contribution statistics (total work notes, knowledge objects proposed/verified).
4. Format data for display.

**Screen layout:**

> *[Screenshot placeholder: Personal Profile Page]*

**Function Details:**

**Validation:**
- User must be authenticated.

**Business Rules:**
- Users can only view their own profile (unless Admin viewing another user).
- Sensitive fields (passwordHash, 2FA secrets) are never exposed to the client.
- Contribution statistics are calculated from verified data only.

**Functionalities:**

**Normal case:**
1. The user navigates to their profile page.
2. System loads personal information, roles, and team memberships.
3. System displays contribution statistics.
4. User can see their full name, email, avatar, roles, and teams.

**Abnormal case:**
1. If session expired: Redirect to login page.

---

#### 3.2.6 Edit Personal Profile

**Function trigger:** User clicks "Edit" on their profile page.

**Function description:**

**Actors:** Admin, Team Leader, Member

**Purpose:** Allow users to update their personal information and avatar.

**Data Processing:**
1. Validate updated fields.
2. If avatar uploaded, generate presigned URL and upload to Cloudflare R2.
3. Update user record in database.
4. Log profile change in audit trail.

**Screen layout:**

> *[Screenshot placeholder: Edit Profile Page]*

**Function Details:**

**Validation:**
- Full name must not be empty and must be between 2-100 characters.
- Avatar file must be a valid image format (JPEG, PNG, WebP) and under 5MB.

**Business Rules:**
- Email cannot be changed through profile edit (security).
- Role and team assignments cannot be self-modified.
- Avatar is stored in Cloudflare R2 with public read access.
- Old avatar is retained for 30 days before deletion.

**Functionalities:**

**Normal case:**
1. The user updates their full name and/or avatar.
2. System validates the changes.
3. System updates the user record.
4. The system displays "Profile updated successfully."

**Abnormal case:**
1. If name is empty: System shows error ("Full name is required.")
2. If avatar file too large: System shows error ("Avatar must be under 5MB.")
3. If avatar format invalid: System shows error ("Only JPEG, PNG, and WebP formats are supported.")

---

### 3.3 Organization & Project Management

#### 3.3.1 Create Project

**Function trigger:** An authenticated user with an active Organization Membership in the selected trusted Organization Context clicks "Create Project".

**Function description:**

**Actors:** Any authenticated User with `OrganizationMembership=ACTIVE` in the matching trusted Organization Context

**Purpose:** Create a new software project within the organization for knowledge management.

**Data Processing:**
1. Validate the authenticated subject, trusted Organization Context and active Organization Membership.
2. Validate project name and code uniqueness within the Organization.
3. Create the Project with `visibility=PRIVATE` and its Organization reference.
4. In the same transaction, create the creator's `ACTIVE` Project Membership and project-scoped `MEMBER` RoleAssignment.
5. Record the existing project-create audit event with Project and bootstrap references.

**Screen layout:**

> *[Screenshot placeholder: Create Project Page]*

**Function Details:**

**Validation:**
- Project name must be 3-100 characters.
- Project code must be 2-10 uppercase alphanumeric characters, unique within the organization.
- The request's Organization Context must be established by an active Organization Membership and match the trusted Organization selected for creation.
- Project creation must not require an Admin, Team Leader or `project.create` grant.

**Business Rules:**
- Every newly created Project starts `PRIVATE`.
- The creator is atomically added as an active Project Member and receives only the project-scoped `MEMBER` assignment.
- Creation does not make the creator a Team Leader, Organization Admin, Project owner or Team, and grants no access to other Projects.
- Organization Admin and Platform Operator roles do not grant access to Project content; content checks remain membership/scope/ACL based.

**Functionalities:**

**Normal case:**
1. User fills in project name, code, and description.
2. System validates the trusted Organization Context and active Organization Membership, then validates the input.
3. System atomically creates the private Project, creator membership, scoped `MEMBER` assignment and audit event.
4. The system displays "Project created successfully."

**Abnormal case:**
1. If project code already exists: System shows error ("Project code already in use.")
2. If Organization Membership is missing/inactive or the trusted context does not match: deny the request and do not create any Project/bootstrap record.
3. If any transactional bootstrap write fails: roll back the Project and all associated membership/assignment/audit writes.

---

#### 3.3.2 Manage Teams

**Function trigger:** A Team Leader assigned to the Project scope navigates to its team management page.

**Function description:**

**Actors:** Team Leader assigned to the Project scope

**Purpose:** Create, view, and manage teams within a project.

**Data Processing:**
1. List all teams in the project with member counts.
2. For team creation: validate name/code uniqueness within the project.
3. Create team record linked to the organization and project.
4. Log team operations in audit trail.

**Screen layout:**

> *[Screenshot placeholder: Team Management Page]*

**Function Details:**

**Validation:**
- Team name must be 2-50 characters.
- Team code must be 2-20 uppercase alphanumeric characters, unique within the project.
- User must have an explicit Team Leader assignment in the Project scope or an explicitly delegated management permission. Organization Admin role alone is not sufficient.

**Business Rules:**
- Team Leaders can only manage teams within their assigned project scope.
- A team must have at least one Team Leader assigned.
- Deleting a team requires all members to be reassigned or removed first.
- Team operations are recorded in the audit trail.

**Functionalities:**

**Normal case:**
1. User views the list of teams in the project.
2. User clicks "Create Team" and fills in name and code.
3. System validates and creates the team.
4. The system displays "Team created successfully."

**Abnormal case:**
1. If team code already exists in project: System shows error ("Team code already in use within this project.")
2. If insufficient permissions: System shows error ("You do not have permission to manage teams in this project.")

---

#### 3.3.3 Add/Remove Team Members

**Function trigger:** A Team Leader assigned to the relevant Project/Team scope, or a separately authorized delegate, changes team membership.

**Function description:**

**Actors:** Team Leader assigned to the relevant Project/Team scope, or separately authorized delegate

**Purpose:** Manage team membership by adding or removing users.

**Data Processing:**
1. For adding: validate user exists and is not already a member.
2. Create team_membership record with role assignment.
3. For removing: validate the member is not the last Team Leader.
4. Remove team_membership record.
5. Invalidate affected user's session cache.
6. Log membership change in audit trail.

**Screen layout:**

> *[Screenshot placeholder: Team Members Page]*

**Function Details:**

**Validation:**
- User to be added must exist in the system and be ACTIVE.
- User must not already be a member of the team.
- Cannot remove the last Team Leader from a team.
- Explicit authorization in the relevant Project/Team scope is required; Organization Admin role alone is not sufficient.

**Business Rules:**
- Adding a member grants them access to team-scoped resources immediately.
- Removing a member revokes access and invalidates cached permissions.
- Membership changes are logged with before/after states.
- Team Leaders can only manage members within their delegated scope (no privilege escalation).

**Functionalities:**

**Normal case:**
1. User selects a user to add to the team.
2. System validates membership eligibility.
3. System creates the membership record.
4. The system displays "Member added successfully."

**Abnormal case:**
1. If user already a member: System shows error ("User is already a member of this team.")
2. If user not found: System shows error ("User not found.")
3. If removing last leader: System shows error ("Cannot remove the last Team Leader from a team.")

---

#### 3.3.4 Manage Organization Membership and Role/Scope Administration

**Function trigger:** An Organization Admin manages a user's Organization Membership or assigns an Organization-level role/scope through the Organization administration interface.

**Actors:** Admin

**Purpose:** Manage Organization membership and Organization-scoped role/scope assignments. This operation does not create Project Membership and does not grant Project content access by itself.

**Approved authorization boundary:**
- `OrganizationMembership` is the authoritative relationship between User and Organization; only `ACTIVE` establishes Organization Context.
- Admin authority is limited to Organization user/membership, Organization roles/scopes and Organization settings/policy.
- The exact invitation, activation, suspension, removal, role-transition and delegation workflows are not specified by this report and must follow the approved Organization Membership API contract.
- Assigning an Organization role does not silently create a Project/Team membership or grant access to confidential Project content.
- The former `project.create` grant workflow in this report is superseded. Project creation uses the separate active-membership rule in §3.3.1. This report does not decide whether remaining capability grants will be retained for other policies.

**Audit requirement:** Record the actor, subject, Organization, changed membership/assignment, scope, timestamp and reason where required by the final contract. Do not place sensitive content in audit metadata.

---

### 3.4 Daily Knowledge Capture

#### 3.4.1 Create Daily Work Note

**Function trigger:** Team member clicks "New Work Note" or "Today's Note" from the dashboard.

**Function description:**

**Actors:** Team Leader, Member

**Purpose:** Capture structured daily work knowledge including what was done, how, why, blockers, and next steps.

**Data Processing:**
1. If a Continuum task is linked, resolve its permitted context by `taskId` through the Task API.
2. Create work_note record with status=DRAFT.
3. Auto-save draft periodically.
4. Store evidence links (PR, commit, file references).

**Screen layout:**

> *[Screenshot placeholder: Create Work Note Page]*

**Function Details:**

**Validation:**
- At least one of What/How/Why fields must be filled.
- Evidence links must be valid URLs or file references.
- Date must be today or a recent past date (within 7 days).

**Business Rules:**
- Work notes start as DRAFT and must be explicitly confirmed by the author.
- Linked task data is contextual only; the author reviews and confirms the Work Note.
- Notes can be created without a task link (manual capture is supported).
- Auto-save preserves drafts to prevent data loss.
- A reminder follows up on missing required daily notes at 17:30.
- Notes are scoped to the author's project/team.

**Functionalities:**

**Normal case:**
1. User selects a date and optionally links a Continuum task.
2. Permitted task context is loaded through Task API if linked.
3. User fills in What/How/Why, blockers, next steps, and evidence.
4. System saves as DRAFT.
5. The system displays "Work note saved as draft."

**Abnormal case:**
1. If all fields empty: System shows error ("At least one content field is required.")
2. If task lookup fails: System shows a warning and allows the author to continue without task context, subject to final Work Note contract.
3. If auto-save fails: System shows warning ("Auto-save failed. Please save manually.")

---

#### 3.4.2 Confirm Work Note

**Function trigger:** Author clicks "Confirm" on a draft work note.

**Function description:**

**Actors:** Team Leader, Member

**Purpose:** Author confirms their work note content, making it eligible for knowledge extraction.

**Data Processing:**
1. Validate that the note has sufficient content.
2. Set `authorConfirmedAt` timestamp.
3. Update status from DRAFT to CONFIRMED.
4. Create an immutable version record in `work_note_versions`.
5. Trigger AI knowledge extraction pipeline (asynchronous).

**Screen layout:**

> *[Screenshot placeholder: Confirm Note Dialog]*

**Function Details:**

**Validation:**
- Only the author can confirm their own note.
- Note must have at least one filled content field.
- Note must be in DRAFT status.

**Business Rules:**
- Confirmation is irreversible — confirmed notes cannot return to DRAFT.
- Only the author themselves can confirm (no delegation).
- Confirmed notes are eligible for AI knowledge extraction.
- A version record is created for audit trail purposes.
- Confirmation timestamp is recorded (`authorConfirmedAt`).

**Functionalities:**

**Normal case:**
1. Author reviews the draft work note.
2. Author clicks "Confirm."
3. System updates status to CONFIRMED and records timestamp.
4. The system displays "Work note confirmed. It will now be processed for knowledge extraction."

**Abnormal case:**
1. If note already confirmed: System shows error ("This note has already been confirmed.")
2. If user is not the author: System shows error ("Only the author can confirm this note.")

---

### 3.5 Continuum Task Management

Continuum Task API is the canonical source for operational tasks. The Task service runs as a separate NestJS service within the existing backend repository and service topology and owns the logical MongoDB database `continuum_task`. This decision does not create a separate source repository or MongoDB cluster.

Work Notes and handover records may keep an optional logical `taskId` and resolve task data only through the Task API or its approved event contract. They must not query Task collections directly. Only permitted Work Notes and evidence flow into SAG retrieval/indexing; tasks themselves are not SAG knowledge sources. Jira issue synchronization is not part of the current task-source MVP.

The Task use cases, exact field/status lifecycle, role-action matrix, API payloads and event schemas remain subject to the dedicated Task Management contract and review. This report does not invent those details.

---

### 3.6 Knowledge Lifecycle

#### 3.6.1 Propose Knowledge

**Function trigger:** User clicks "Propose Knowledge" from the knowledge base page, or AI extraction generates a proposal.

**Function description:**

**Actors:** Project/Team member with applicable membership, scope and source ACL

**Purpose:** Create a knowledge proposal from evidence (work notes, documents, or manual entry) for human review.

**Data Processing:**
1. Validate knowledge content and required metadata (title, domain, category).
2. Attach evidence references (source documents, work notes, file links).
3. Create `knowledge_proposals` record with status=PROPOSED.
4. Identify appropriate reviewer based on domain/team scope.
5. Send notification to reviewer's Verification Inbox.

**Screen layout:**

> *[Screenshot placeholder: Propose Knowledge Page]*

**Function Details:**

**Validation:**
- Title must be 5-200 characters.
- Domain/category must be selected.
- At least one evidence reference must be attached.
- Content must not be empty.

**Business Rules:**
- All AI-generated proposals start as PROPOSED and require human review.
- The proposer cannot approve their own proposal (separation of duties).
- Evidence references must be accessible to the assigned reviewer.
- Proposals are scoped to the proposer's project/team.

**Functionalities:**

**Normal case:**
1. User fills in knowledge details and attaches evidence.
2. System creates the proposal and identifies the reviewer.
3. Reviewer is notified via Verification Inbox and email.
4. The system displays "Knowledge proposal submitted for review."

**Abnormal case:**
1. If no evidence attached: System shows error ("At least one evidence reference is required.")
2. If no eligible reviewer found: System shows warning ("No eligible reviewer found. Please contact your Team Leader.")

---

#### 3.6.2 Verify / Reject Knowledge

**Function trigger:** Reviewer clicks "Verify" or "Reject" on a knowledge proposal in the Verification Inbox.

**Function description:**

**Actors:** Team Leader (scoped), SME (assigned)

**Purpose:** Review and approve or reject a knowledge proposal after verifying evidence.

**Data Processing:**
1. Verify reviewer has authorization for the proposal's domain/scope.
2. For VERIFY: Create `knowledge_versions` record, update status to ACTIVE, record `knowledge_evidence`, log `knowledge_verifications` — all within a single Mongoose Transaction (ACID).
3. For REJECT: Update status to REJECTED with feedback, notify proposer.
4. If superseding, move old version to SUPERSEDED status within the same transaction.

**Screen layout:**

> *[Screenshot placeholder: Knowledge Review Detail Page]*

**Function Details:**

**Validation:**
- Reviewer must be authorized for the proposal's domain (SME or Team Leader of scope).
- Reviewer cannot approve their own proposal.
- Evidence must be accessible and valid.
- Feedback is required for rejection.

**Business Rules:**
- Verification uses ACID multi-document transactions to ensure consistency.
- Only authorized reviewers can verify/reject (Pre-Retrieval Scoped ACL).
- Rejected proposals can be revised and resubmitted.
- Verified knowledge immediately enters the retrieval index.
- Version history is immutable and auditable.

**Functionalities:**

**Normal case:**
1. Reviewer examines the proposal content and evidence.
2. Reviewer clicks "Verify" or "Reject" with optional feedback.
3. System processes the decision within a transaction.
4. Proposer is notified of the decision.
5. The system displays "Knowledge [verified/rejected] successfully."

**Abnormal case:**
1. If reviewer lacks scope: System shows error ("You are not authorized to review this knowledge proposal.")
2. If self-approval attempted: System shows error ("You cannot approve your own proposal.")
3. If transaction fails: System shows error ("Failed to process. Please try again.") and rolls back.

---

### 3.7 Chat & AI Assistant

#### 3.7.1 Ask Question (with Citations)

**Function trigger:** User types a question in the AI Chat Assistant and clicks "Send."

**Function description:**

**Actors:** Project/Team member with applicable membership, scope and source ACL

**Purpose:** Ask the AI assistant a question about project knowledge and receive an evidence-grounded answer with mandatory citations.

**Data Processing:**
1. Compute effective permissions ($P_{eff}$) for the user (Pre-Retrieval Scoped ACL).
2. Send scoped query to FastAPI SAG Engine for hybrid search (BM25 + vector).
3. Retrieve relevant chunks filtered by user's ACL.
4. Construct context with retrieved evidence for LLM.
5. Generate answer with mandatory citations (Document ID, Locator, Hash, Version).
6. If insufficient evidence: return INSUFFICIENT_EVIDENCE response.
7. Stream response to client via SSE.

**Screen layout:**

> *[Screenshot placeholder: AI Chat Interface]*

**Function Details:**

**Validation:**
- Question must not be empty and must be under 2000 characters.
- User must have active project membership.
- Session must have valid scope filter.

**Business Rules:**
- Every answer MUST include citations with Document ID, Locator, Hash, and Version.
- If evidence is insufficient, the system returns INSUFFICIENT_EVIDENCE and offers 1-click Knowledge Gap creation.
- Permission filtering happens BEFORE retrieval and context construction (Pre-Retrieval ACL).
- The system never fabricates answers without evidence (anti-hallucination policy).
- Chat history respects ACL changes — saved answers are not a permanent access grant.
- Answers include verification status and last verified date.

**Functionalities:**

**Normal case:**
1. User types a question about project knowledge.
2. System computes user's effective permissions.
3. System performs hybrid search with ACL filtering.
4. LLM generates an evidence-grounded answer with citations.
5. Response is streamed to the user with inline citation links.

**Abnormal case:**
1. If question is empty: System shows error ("Please enter a question.")
2. If insufficient evidence: System shows "I don't have enough evidence to answer this question. Would you like to report this as a Knowledge Gap?"
3. If SAG Engine unavailable: System shows error ("AI service is temporarily unavailable. Please try again later.")
4. If user has no project access: System shows error ("You do not have access to this project's knowledge base.")

---

#### 3.7.2 Report Knowledge Gap

**Function trigger:** User clicks "Report Gap" after receiving an INSUFFICIENT_EVIDENCE response or from the knowledge base page.

**Function description:**

**Actors:** Project/Team member with applicable membership, scope and source ACL

**Purpose:** Create a knowledge gap report for missing or inadequate knowledge.

**Data Processing:**
1. Create `knowledge_gaps` record with source (chat question, overdue review, or manual report).
2. Link to the chat message if originated from chat.
3. Assign priority based on domain and frequency.
4. Notify relevant Team Leader and Knowledge Owners.

**Screen layout:**

> *[Screenshot placeholder: Report Gap Dialog]*

**Function Details:**

**Validation:**
- Gap description must be 10-1000 characters.
- Domain/module must be selected.

**Business Rules:**
- Knowledge gaps are visible to all team members with appropriate scope.
- Gaps from chat questions are automatically linked to the original question.
- Gaps trigger follow-up actions and can be assigned to specific owners.
- Duplicate gap detection: system suggests similar existing gaps before creating new ones.

**Functionalities:**

**Normal case:**
1. User describes the knowledge gap and selects the domain.
2. System creates the gap record and notifies stakeholders.
3. The system displays "Knowledge gap reported successfully."

**Abnormal case:**
1. If description too short: System shows error ("Please provide a more detailed description of the knowledge gap.")
2. If similar gap exists: System shows "A similar gap already exists: [title]. Would you like to add your input to it?"

---

### 3.8 Handover Management

#### 3.8.1 Initiate Handover

**Function trigger:** A Team Leader assigned to the relevant Project/Team scope, or another actor with an explicit handover assignment, initiates handover for a departing or transferring member.

**Function description:**

**Actors:** Team Leader assigned to the relevant Project/Team scope; explicitly assigned predecessor/successor as applicable

**Purpose:** Start the handover process when a member departs or transfers responsibility.

**Data Processing:**
1. Analyze the departing member's responsibilities: owned modules, documents, knowledge objects, open tasks.
2. Identify knowledge gaps and areas of single-point-of-failure.
3. Generate a prioritized handover checklist.
4. Create `handovers` record with status=INITIATED.
5. Optionally assign a successor.

**Screen layout:**

> *[Screenshot placeholder: Initiate Handover Page]*

**Function Details:**

**Validation:**
- The departing member must be an active member of the project/team.
- Initiator must have the applicable Project/Team assignment and resource ACL. `ADMIN` or `PLATFORM_OPERATOR` role alone does not authorize viewing the handover's confidential content or initiating the Project workflow.
- A successor must be a valid, active member (if assigned).

**Business Rules:**
- Handover analyzes all responsibilities, ownership, evidence, coverage, freshness, and concentration.
- Missing or overdue knowledge creates follow-up items automatically.
- Handover checklist items are prioritized by risk and coverage.
- The departing member's status transitions to OFFBOARDING.
- Completion must be confirmed by a Team Leader in the assigned scope or another explicitly authorized reviewer. `ADMIN` role alone is not sufficient.

**Functionalities:**

**Normal case:**
1. Initiator selects the departing member and provides a reason.
2. System analyzes responsibilities and generates a prioritized checklist.
3. System creates the handover record.
4. The system displays "Handover initiated for [member]. [N] checklist items generated."

**Abnormal case:**
1. If member not found: System shows error ("Member not found in this team.")
2. If handover already active: System shows error ("An active handover already exists for this member.")

---

#### 3.8.2 Audio Interview Recording

**Function trigger:** Team Leader clicks "Start Interview" in the handover package.

**Function description:**

**Actors:** Team Leader

**Purpose:** Conduct and record an audio interview with the departing member for knowledge extraction.

**Data Processing:**
1. Establish WebSocket connection at `/ws/handover`.
2. Receive audio stream from client microphone.
3. Upload audio chunks to Cloudflare R2.
4. Upon completion, enqueue transcription job to `handover-queue`.
5. Process audio through Whisper API for speech-to-text.
6. Store transcript and extract proposed knowledge items.

**Screen layout:**

> *[Screenshot placeholder: Audio Interview Interface]*

**Function Details:**

**Validation:**
- User must have Team Leader role.
- Handover must be in INITIATED or IN_PROGRESS status.
- Audio format must be supported (WebM, WAV, MP3).

**Business Rules:**
- Audio recordings are stored in private Cloudflare R2 bucket.
- Transcription is processed asynchronously via Whisper API.
- Extracted knowledge items from the interview start as PROPOSED.
- Interview sessions are linked to the handover record.
- Both predecessor and successor can access the transcript.

**Functionalities:**

**Normal case:**
1. Team Leader starts the audio recording.
2. Audio is streamed via WebSocket and stored in R2.
3. Upon completion, transcription job is enqueued.
4. Transcript is available within minutes after processing.
5. The system displays "Interview recorded. Transcription in progress."

**Abnormal case:**
1. If microphone access denied: System shows error ("Microphone access is required for audio interview.")
2. If WebSocket connection lost: System shows error ("Connection lost. Recording has been saved up to the disconnection point.")
3. If Whisper API fails: System shows error ("Transcription failed. Audio recording is preserved for retry.")

---

### 3.9 Document & Ingestion

#### 3.9.1 Upload Document

**Function trigger:** User clicks "Upload" on the Documents Library page.

**Function description:**

**Actors:** Project/Team member with applicable membership, scope and upload policy

**Purpose:** Upload a document for processing, indexing, and inclusion in the knowledge retrieval system.

**Data Processing:**
1. Validate file type (PDF, DOCX, Markdown, TXT, Image) and size.
2. Calculate SHA-256 hash for deduplication check.
3. Generate presigned PUT URL for direct upload to Cloudflare R2.
4. Client uploads file directly to R2 (bypass backend for performance).
5. After upload completion, create `sources` record in database.
6. Create `ingestion_jobs` record and enqueue to BullMQ `ingestion-queue`.

**Screen layout:**

> *[Screenshot placeholder: Upload Document Page]*

**Function Details:**

**Validation:**
- File type must be one of: PDF, DOCX, MD, TXT, JPEG, PNG, WebP.
- Maximum file size: 50MB.
- SHA-256 hash must not match an existing document (deduplication).

**Business Rules:**
- Files are uploaded directly to Cloudflare R2 via presigned URL (server CPU is preserved).
- SHA-256 hash verification ensures no duplicate files.
- Metadata (filename, mimeType, size, hash, R2 key) is stored in MongoDB.
- Source ACL is enforced for each read and retrieval. Policy changes require an authorized policy administrator or scoped Team Leader; configuration access does not reveal the protected content.
- Ingestion pipeline starts automatically after upload confirmation.

**Functionalities:**

**Normal case:**
1. User selects or drags files to upload.
2. System validates file type and size.
3. System generates presigned URL and client uploads directly.
4. System creates source record and starts ingestion.
5. The system displays "Document uploaded. Processing started."

**Abnormal case:**
1. If file type unsupported: System shows error ("Unsupported file type. Please upload PDF, DOCX, MD, TXT, or Image files.")
2. If file too large: System shows error ("File exceeds the 50MB limit.")
3. If duplicate detected: System shows error ("This file has already been uploaded (SHA-256 match).")
4. If R2 upload fails: System shows error ("Upload failed. Please try again.")

---

### 3.10 Notifications

#### 3.10.1 View Notifications

**Function trigger:** User clicks the notification bell icon or navigates to the notification center.

**Function description:**

**Actors:** Admin, Team Leader, Member

**Purpose:** Display all notifications including knowledge review requests, handover updates, daily note reminders, and system alerts.

**Data Processing:**
1. Retrieve notifications for the user, ordered by timestamp (newest first).
2. Group by read/unread status.
3. Include action links for navigating to related resources.
4. Paginate results (20 per page).

**Screen layout:**

> *[Screenshot placeholder: Notification Center]*

**Function Details:**

**Validation:**
- User must be authenticated.

**Business Rules:**
- Notifications are delivered in real-time via WebSocket (Redis Pub/Sub).
- Notification types include: knowledge_review_requested, handover_initiated, daily_note_reminder, knowledge_verified, gap_reported, and system_alert.
- Unread count is displayed on the notification bell icon.
- Old notifications (>90 days) are archived.

**Functionalities:**

**Normal case:**
1. User clicks the notification bell.
2. System loads notifications sorted by date.
3. User sees unread notifications highlighted.
4. User can click a notification to navigate to the related resource.

**Abnormal case:**
1. If no notifications: System shows "No notifications yet."

#### 3.10.2 Mark Notification as Read

**Function trigger:** User clicks on a notification or clicks "Mark all as read."

**Function description:**

**Actors:** Admin, Team Leader, Member

**Purpose:** Mark notifications as read to clear unread indicators.

**Data Processing:**
1. Update `readAt` timestamp for the selected notification(s).
2. Recalculate unread count.
3. Update the notification badge in real-time.

**Functionalities:**

**Normal case:**
1. User clicks a notification or "Mark all as read."
2. System updates the read status.
3. Unread count is refreshed immediately.

---

## 4. Non-Functional Requirements

### 4.1 External Interfaces

#### 4.1.1 Database Interfaces

| Database | Technology | Purpose |
|----------|-----------|---------|
| **Primary Database** | MongoDB 7.0 (3-Node Replica Set) | Source of Truth for all business entities, lifecycle, permissions, and audit logs. Each microservice owns its dedicated database (Database-per-Service pattern). |
| **Vector Store** | LanceDB (Disk-backed IVF-PQ / HNSW) | Local vector index for semantic retrieval, embedded within the SAG AI Engine. |
| **SAG Post-Extraction Storage** | PostgreSQL 16 + pgvector | Stores chunks, events, entities, dynamic hyperedges, and vector embeddings for deep semantic queries. |
| **Cache & Session** | Redis 7.2 (In-Memory Cluster) | Distributed L2 cache, token blacklist (<1ms check), SingleFlight mutex, Pub/Sub for real-time notifications. |

#### 4.1.2 API Interfaces

| API | Technology | Purpose |
|-----|-----------|---------|
| **REST API** | NestJS with OpenAPI/Swagger | Primary API for all CRUD operations, authentication, and management. Base path: `/api/v1/`. |
| **WebSocket** | NestJS Gateway + Socket.IO | Real-time notifications (Redis Pub/Sub), audio streaming for handover interviews. |
| **SSE (Server-Sent Events)** | NestJS | Streaming AI chat responses with real-time token delivery. |
| **Internal API** | FastAPI (Python) with mTLS | SAG AI Engine endpoints for parsing, indexing, hybrid search, and LLM generation. |

#### 4.1.3 Frontend Interfaces

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Next.js** | 16 (App Router) | Hybrid rendering (SSR/SSG/Client Components), route handlers, streaming UI. |
| **React** | 19 | Component framework with Server Components and Concurrent Features. |
| **TailAdmin** | 2.4.0 | Dashboard UI design system with Tailwind CSS 4. |
| **TanStack Query** | v5 | Remote server state management with caching and optimistic UI. |
| **Zustand** | v5 | Lightweight shared client-only UI state. |
| **next-intl** | latest | Locale-aware routing for internationalization. |

#### 4.1.4 External Service Interfaces

| Service | Technology | Purpose |
|---------|-----------|---------|
| **Jira Cloud (Future / Not in MVP)** | REST v3 API + Webhooks | Not the task source; any third-party connector requires a separate approved scope and contract. |
| **Cloudflare R2** | S3-compatible API | Private object storage for uploaded documents, audio recordings, and OCR artifacts. |
| **LLM Providers** | Gemini 2.5 Flash/Pro, OpenAI, Whisper | AI inference, text generation, embedding, and speech-to-text transcription. |
| **Email** | SMTP / Resend API | Transactional email delivery for password resets, activation, and knowledge alerts. |

### 4.2 Quality Attributes

#### 4.2.1 Usability

- **Responsive Design:** The web application must be fully responsive across desktop, tablet, and mobile browsers.
- **Accessibility:** WCAG 2.1 Level AA compliance for all interactive elements.
- **Internationalization:** Support for at least English and Vietnamese via next-intl.
- **Loading States:** All async operations must show loading indicators with estimated completion time where applicable.
- **Error Messages:** All error messages must be user-friendly, actionable, and localized.
- **Onboarding:** New users receive a guided tour of key features on first login.
- **Dark Mode:** Support for system-preferred and user-toggled dark mode via TailAdmin.

#### 4.2.2 Reliability

- **Availability:** System uptime target of 99.5% during business hours.
- **Data Durability:** MongoDB 3-node replica set ensures data durability with automatic failover.
- **Transaction Integrity:** Knowledge verification uses ACID multi-document transactions.
- **Idempotency:** Asynchronous consumers deduplicate events according to the owning service's approved event contract.
- **Error Recovery:** Failed ingestion jobs retain original files and expose retry state.
- **Dead Letter Queue:** Failed asynchronous jobs are routed to a DLQ according to service-specific retry and recovery policies.
- **Backup:** Automated database backups with point-in-time recovery.

#### 4.2.3 Performance

- **API Response Time:** 95th percentile response time under 500ms for standard CRUD operations.
- **Token Blacklist Check:** Redis-based JWT validation under 1ms.
- **Chat Response:** Initial token streaming within 2 seconds for AI chat responses.
- **File Upload:** Direct-to-R2 upload via presigned URL to minimize backend CPU usage.
- **Pagination:** All list endpoints support pagination with configurable page size (default: 20, max: 100).
- **Caching:** Redis L2 cache with SingleFlight pattern to prevent thundering herd.
- **Indexing:** MongoDB compound indexes with `(organizationId, projectId)` prefix for efficient multi-tenant queries.

#### 4.2.4 Security

- **Authentication:** JWT-based with access token (15min) and refresh token rotation (7 days).
- **Password Storage:** Bcrypt 12 rounds for all password hashes.
- **Two-Factor Authentication:** Optional TOTP-based 2FA.
- **Pre-Retrieval ACL:** Permission filtering before vector database retrieval to prevent data leakage.
- **Authorization:** `PLATFORM_OPERATOR` is a separate platform-scoped actor. The three persistent Organization/Project roles are `ADMIN`, `TEAM_LEADER` and `MEMBER`; effective access also requires active membership, assigned scope, resource ACL and lifecycle checks. Admin and Platform Operator receive no default confidential-content access.
- **Rate Limiting:** API rate limiting to prevent abuse and brute-force attacks.
- **Race Condition Prevention:** Redis Redlock for distributed locking.
- **Input Validation:** Global input validation via NestJS pipes.
- **HTTP Security Headers:** Helmet.js for security headers (CSP, HSTS, X-Frame-Options).
- **Audit Trail:** Immutable, append-only audit log for SOC2/ISO compliance.
- **Zero Trust:** No role or assignment automatically bypasses a confidential source ACL.

---

## 5. Requirement Appendix

### 5.1 Business Rules

| # | Rule | Description |
|---|------|-------------|
| BR-01 | Human-in-the-loop | AI output remains PROPOSED until an authorized human verifies it. No AI-controlled permission grants or autonomous verification. |
| BR-02 | Pre-Retrieval ACL | Compute effective permissions BEFORE querying the vector database. Post-filtering after restricted content reaches the LLM is insufficient. |
| BR-03 | Evidence-Grounded Citations | Every AI answer must include citations (Document ID, Locator, Hash, Version). If insufficient evidence, return INSUFFICIENT_EVIDENCE. |
| BR-04 | Source of Truth | MongoDB is the single source of truth for business data. LanceDB/pgvector are retrieval indexes only. |
| BR-05 | Database-per-Service | Each bounded service owns its dedicated database. No cross-service JOINs or shared database connections. |
| BR-06 | Deny Takes Precedence | Explicit deny overrides all grants, roles, and assignments in the permission model. |
| BR-07 | Project Creation | Any authenticated User with `OrganizationMembership=ACTIVE` in the trusted matching Organization Context may create a `PRIVATE` Project. `project.create` is not required; creator Project Membership and project-scoped `MEMBER` assignment are bootstrapped atomically. |
| BR-08 | Author-Confirmed Notes | Work notes only become knowledge sources after the author explicitly confirms them. |
| BR-09 | No Performance Scoring | Missing daily notes trigger follow-up reminders, NOT employee performance scoring. |
| BR-10 | Scoped Handover Confirmation | A successor cannot self-confirm handover completion. Confirmation requires a Team Leader assigned to the relevant scope or another explicitly authorized reviewer; Admin authority alone does not grant it. |

### 5.2 Common Requirements

| # | Requirement | Description |
|---|-------------|-------------|
| CR-01 | Authentication | All API endpoints (except login and health check) require valid JWT authentication. |
| CR-02 | Multi-Tenancy | All business queries include `organizationId` and `projectId` scope filtering. |
| CR-03 | Pagination | All list endpoints support pagination with `page`, `limit`, and total count in response. |
| CR-04 | Sorting | All list endpoints support sorting by relevant fields with `sortBy` and `sortOrder` parameters. |
| CR-05 | Search | List endpoints support full-text search where applicable. |
| CR-06 | Validation | All input data is validated using NestJS class-validator decorators. |
| CR-07 | Error Handling | All errors return consistent JSON format: `{ statusCode, message, error, timestamp }`. |
| CR-08 | Audit Logging | All state-changing operations are logged in the immutable audit trail. |
| CR-09 | Timestamps | All entities include `createdAt` and `updatedAt` timestamps (UTC). |
| CR-10 | Soft Delete | Entities are soft-deleted where appropriate (status-based, not physical deletion). |

### 5.3 Application Messages List

| Code | Message | Type | Context |
|------|---------|------|---------|
| AUTH-001 | "Login successful." | Success | After successful authentication |
| AUTH-002 | "Account does not exist." | Error | Email not found during login |
| AUTH-003 | "Incorrect password." | Error | Password mismatch during login |
| AUTH-004 | "Account has been suspended." | Error | Suspended account login attempt |
| AUTH-005 | "Logout successful." | Success | After logout |
| AUTH-006 | "Password reset link has been sent." | Success | After forgot password request |
| AUTH-007 | "Password changed successfully." | Success | After password change |
| AUTH-008 | "Invalid two-factor authentication code." | Error | Wrong 2FA code |
| PROJ-001 | "Project created successfully." | Success | After project creation |
| PROJ-002 | "Project code already in use." | Error | Duplicate project code |
| PROJ-003 | "An active Organization Membership is required to create a project." | Error | Organization membership missing/inactive or trusted context mismatch |
| TEAM-001 | "Team created successfully." | Success | After team creation |
| TEAM-002 | "Member added successfully." | Success | After adding team member |
| TEAM-003 | "Cannot remove the last Team Leader." | Error | Removing last leader |
| NOTE-001 | "Work note saved as draft." | Success | After saving draft |
| NOTE-002 | "Work note confirmed." | Success | After confirming note |
| NOTE-003 | "Only the author can confirm this note." | Error | Non-author confirmation attempt |
| KNOW-001 | "Knowledge proposal submitted for review." | Success | After proposing knowledge |
| KNOW-002 | "Knowledge verified successfully." | Success | After verification |
| KNOW-003 | "Knowledge rejected." | Info | After rejection |
| KNOW-004 | "You are not authorized to review this proposal." | Error | Unauthorized review |
| CHAT-001 | "I don't have enough evidence to answer this question." | Info | Insufficient evidence |
| CHAT-002 | "Knowledge gap reported successfully." | Success | After gap report |
| HAND-001 | "Handover initiated." | Success | After handover initiation |
| HAND-002 | "Interview recorded. Transcription in progress." | Success | After audio interview |
| DOC-001 | "Document uploaded. Processing started." | Success | After document upload |
| DOC-002 | "Unsupported file type." | Error | Invalid file type |
| DOC-003 | "File exceeds the 50MB limit." | Error | File too large |
| DOC-004 | "This file has already been uploaded." | Error | Duplicate file |
| NOTIF-001 | "No notifications yet." | Info | Empty notification list |
| PROF-001 | "Profile updated successfully." | Success | After profile update |

### 5.4 Other Requirements

- **Browser Support:** Latest 2 versions of Chrome, Firefox, Safari, and Edge.
- **Deployment:** Kubernetes-based container orchestration with Helm v3 charts.
- **CI/CD:** GitHub Actions for automated testing, linting, and deployment.
- **Monitoring:** Structured logging and health check endpoints for observability.
- **Documentation:** Swagger/OpenAPI for API documentation when `SWAGGER_ENABLED=true`.
- **Delivery Timeline:** 10-week MVP scope as defined in the project specification.
