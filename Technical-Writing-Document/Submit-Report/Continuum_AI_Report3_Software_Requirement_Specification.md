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

---

# II. Software Requirement Specification

## 1. Product Overview

Continuum AI is an AI-powered platform designed to solve the critical problem of **knowledge loss** when team members leave a software project, change teams, or transfer responsibilities. Unlike traditional documentation tools, Continuum AI provides a structured workflow that captures, verifies, maintains, and transfers knowledge continuously throughout the project lifecycle.

The platform integrates with external tools like Jira Cloud for task synchronization, uses AI (Gemini/OpenAI) for intelligent knowledge extraction and evidence-grounded question answering, and supports a formal handover process with audio interviews and successor learning paths.

**Key capabilities:**
- Continuous daily knowledge capture with Jira integration
- Human-verified knowledge lifecycle (Proposed → Verified → Active)
- Permission-aware AI chat assistant with mandatory citations
- Structured handover workflow with gap analysis
- Role-based access control with 3 persistent roles

**Context Diagram:**

> *See Figure 1: Context Diagram (01_context_diagram.drawio)*

---

## 2. User Requirements

### 2.1 Actors

| # | Actor | Description |
|---|-------|-------------|
| 1 | **Admin** | Organization administrator responsible for managing users, projects, teams, role assignments, integration connectors (Jira), source ACL policies, and audit logs. Can grant the `project.create` capability to Team Leaders. Does not automatically have access to confidential project content. |
| 2 | **Team Leader** | Team leader responsible for managing assigned team workspaces, members, knowledge requirements, reviewing/approving knowledge in the Verification Inbox, initiating and managing handover workflows, and conducting audio interviews. Can create projects only if granted `project.create` by an Admin. Also contributes knowledge as a regular team member. |
| 3 | **Member** | Software engineer/contributor who creates daily work notes (What/How/Why), uploads documents, proposes knowledge objects, asks the AI assistant questions, reports knowledge gaps, and participates in handover as a successor. Access is limited to authorized resources within their team/project scope. |

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
| 09 | Create Organization | Admin | Allows admin to create a new organization with name, slug, and plan settings. |
| 10 | Create Project | Admin, Team Leader (with grant) | Allows creation of a new project within an organization. Team Leaders require explicit `project.create` capability grant from Admin. |
| 11 | View Project List | Admin, Team Leader, Member | Displays list of projects the user has membership in, with filtering and pagination. |
| 12 | View Project Detail | Admin, Team Leader, Member | Shows detailed project information including teams, members, and statistics. |
| 13 | Update Project | Admin, Team Leader | Allows updating project name, description, and status (ACTIVE/ARCHIVED). |
| 14 | Create Team | Admin, Team Leader | Creates a new team within an existing project with name and code. |
| 15 | Add Team Member | Admin, Team Leader | Adds a user to a team with specified role and scope. |
| 16 | Remove Team Member | Admin, Team Leader | Removes a user from a team (requires appropriate scope). |
| 17 | Assign Role | Admin | Assigns persistent roles (ADMIN, TEAM_LEADER, MEMBER) to users within the organization. |
| 18 | Grant project.create Capability | Admin | Grants the time-bounded, audited `project.create` capability to a specific Team Leader at organization scope. |
| 19 | Revoke Capability | Admin | Revokes a previously granted capability with audit trail. |
| 20 | Assign SME / Knowledge Owner | Admin, Team Leader | Assigns scoped SME or Knowledge Owner assignments to team members for specific domains/modules. |
| 21 | Configure Jira Connector | Admin | Sets up Jira Cloud integration with OAuth2/token credentials, project mapping, and webhook registration. |
| 22 | Sync Jira Issues | Admin, Team Leader | Triggers manual synchronization of Jira issues or views automatic sync status. |
| 23 | View Synced Jira Issues | Admin, Team Leader, Member | Displays Jira issues synchronized to the project with status, assignee, and metadata. |
| 24 | Create Daily Work Note | Team Leader, Member | Creates a structured daily work note with What/How/Why fields, optional Jira prefill, and evidence links. |
| 25 | Edit Work Note | Team Leader, Member | Edits a previously created work note (only own notes, before confirmation). |
| 26 | Confirm Work Note | Team Leader, Member | Author confirms the work note content, making it eligible for knowledge extraction. |
| 27 | View Work Note History | Team Leader, Member | Displays version history of a work note with immutable audit trail. |
| 28 | Propose Knowledge | Team Leader, Member | Creates a knowledge proposal from work notes, documents, or manual entry with evidence references. |
| 29 | View Verification Inbox | Team Leader, SME | Displays pending knowledge proposals requiring review within the user's authorized scope. |
| 30 | Verify/Reject Knowledge | Team Leader, SME | Reviews and approves or rejects a knowledge proposal with feedback. Uses ACID multi-document transaction. |
| 31 | View Knowledge Objects | Admin, Team Leader, Member | Browses verified knowledge objects with filtering by domain, status, owner, and date range. |
| 32 | View Knowledge Gaps | Admin, Team Leader, Member | Displays identified knowledge gaps from overdue reviews, insufficient AI responses, and missing coverage. |
| 33 | Supersede Knowledge | Team Leader, Knowledge Owner | Creates a new version of existing knowledge, moving the old version to SUPERSEDED status. |
| 34 | Create Chat Session | Admin, Team Leader, Member | Initiates a new AI chat session with project scope and permission-aware context. |
| 35 | Ask Question (with Citations) | Admin, Team Leader, Member | Sends a question to the AI assistant; receives an evidence-grounded answer with mandatory citations. If insufficient evidence, returns INSUFFICIENT_EVIDENCE. |
| 36 | Report Knowledge Gap | Admin, Team Leader, Member | Creates a knowledge gap report from an unanswered or insufficiently answered chat question. |
| 37 | View Chat History | Admin, Team Leader, Member | Browses previous chat sessions and messages with their citations and evidence references. |
| 38 | Initiate Handover | Admin, Team Leader | Starts a handover process when a member departs or transfers responsibility. Analyzes responsibilities, ownership, and gaps. |
| 39 | View Handover Package | Admin, Team Leader, Successor | Views the handover package including checklist, priorities, knowledge gaps, and unresolved questions. |
| 40 | Sign-off Handover Item | Team Leader, Admin | Confirms completion of a specific handover checklist item. |
| 41 | Audio Interview Recording | Team Leader | Conducts an audio interview via WebSocket streaming, which is stored in Cloudflare R2 and transcribed via Whisper API. |
| 42 | View Successor Learning Path | Member (Successor) | Views the auto-generated learning path tailored for the successor's onboarding scope. |
| 43 | Upload Document | Admin, Team Leader, Member | Uploads a document (PDF, DOCX, MD, TXT, Image) via presigned URL to Cloudflare R2 for ingestion. |
| 44 | View Documents | Admin, Team Leader, Member | Browses uploaded documents with metadata, ingestion status, and source ACL information. |
| 45 | View Ingestion Status | Admin, Team Leader, Member | Checks the progress of document OCR, chunking, and vector indexing. |
| 46 | Manage Source ACL | Admin, Team Leader | Configures access control lists for uploaded sources and documents. |
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
| 4 | Dashboard | Admin Dashboard | Overview of system statistics: total users, active projects, pending knowledge reviews, recent audit events, and system health indicators. |
| 5 | Dashboard | Team Leader Dashboard | Overview of team activity: pending verifications, knowledge gaps, handover status, recent work notes from team members, and daily note completion rates. |
| 6 | Dashboard | Member Dashboard | Personal overview: today's work note status, recent notifications, knowledge contribution stats, assigned handover items, and quick access to AI chat. |
| 7 | User Management | User List | Paginated table of all users with search, filter by status/role, and sorting. Admin can view user details, suspend/activate, or invite new users. |
| 8 | User Management | User Detail / Edit | Detailed user profile with role assignments, team memberships, capability grants, and activity history. |
| 9 | User Management | Invite User | Form to invite a new user by email with initial role assignment and team membership. |
| 10 | Organization | Organization Settings | View and edit organization name, slug, plan, and global settings. |
| 11 | Project Management | Project List | Grid or table of projects with name, code, status, team count, and member count. |
| 12 | Project Management | Project Detail | Detailed project view with teams, members, Jira connection status, and knowledge statistics. |
| 13 | Team Management | Team List | Table of teams within a project with member counts and leader assignment. |
| 14 | Team Management | Team Detail / Members | Team member list with roles, assignments (SME/Knowledge Owner), and activity status. |
| 15 | Role & Grant | Role & Grant Management | Interface to assign roles, grant/revoke `project.create` capabilities, and assign SME/Knowledge Owner scoped assignments. |
| 16 | Jira Integration | Jira Connector Config | Form to configure Jira Cloud connection with OAuth2/token, project mapping, and webhook URL. Shows sync status and last sync time. |
| 17 | Daily Capture | Work Notes List | Chronological list of work notes with status (Draft/Confirmed), date, and linked Jira issues. |
| 18 | Daily Capture | Create/Edit Work Note | Structured form with What/How/Why fields, Jira issue prefill, evidence links, and blocker/next-step fields. |
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

| Screen | Admin | Team Leader | Member |
|--------|-------|-------------|--------|
| Login | X | X | X |
| Forgot Password | X | X | X |
| Change Password | X | X | X |
| Admin Dashboard | X | | |
| Team Leader Dashboard | | X | |
| Member Dashboard | | | X |
| User List | X | | |
| User Detail / Edit | X | | |
| Invite User | X | | |
| Organization Settings | X | | |
| Project List | X | X | X |
| Project Detail | X | X | X |
| Team List | X | X | |
| Team Detail / Members | X | X | |
| Role & Grant Management | X | | |
| Jira Connector Config | X | | |
| Work Notes List | | X | X |
| Create/Edit Work Note | | X | X |
| Confirm Note | | X | X |
| Verification Inbox | | X (scoped) | |
| Knowledge Review Detail | | X (scoped) | |
| Knowledge Objects | X | X | X |
| Knowledge Gaps | X | X | X |
| AI Chat Assistant | X | X | X |
| Chat History | X | X | X |
| Handover Management | X | X | |
| Handover Package Detail | X | X | X (successor) |
| Audio Interview | | X | |
| Successor Learning Path | | | X (successor) |
| Documents Library | X | X | X |
| Upload Document | X | X | X |
| Ingestion Status | X | X | X |
| Notifications | X | X | X |
| Personal Profile | X | X | X |
| Edit Profile | X | X | X |
| Audit Logs | X | X (scoped) | |

#### 3.1.4 Non-Screen Functions

| # | Feature | System Function | Description |
|---|---------|-----------------|-------------|
| 1 | Authentication | JWT Token Validation | Background middleware that validates JWT access tokens on every API request, extracting scoped claims (userId, orgId, roles, projectIds). |
| 2 | Authentication | Token Blacklist Check | Redis-based check (<1ms) to verify that the token's JTI has not been invalidated by logout. |
| 3 | Authentication | Refresh Token Rotation | Automatic rotation of refresh tokens with reuse detection to prevent replay attacks. |
| 4 | Knowledge Capture | Daily Note Reminder | Cronjob at 17:30 that sends email reminders to team members who haven't confirmed their daily work note. |
| 5 | Knowledge Lifecycle | Knowledge Gap Scanner | Periodic scanner that identifies modules/domains with overdue reviews (exceeding `cadenceDays`) and creates knowledge gap records. |
| 6 | Knowledge Lifecycle | AI Knowledge Extraction | Background worker that extracts proposed knowledge objects from confirmed work notes and ingested documents using LLM. |
| 7 | Jira Integration | Webhook Processing | BullMQ worker that processes incoming Jira webhook events with idempotency deduplication (Redis SETNX). |
| 8 | Jira Integration | Reconciliation Cronjob | Scheduled job at 02:00 AM that reconciles missed webhook events by comparing local and remote Jira states. |
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
| 3 | projects | Represents a software project within an organization. Contains name, code, description, and status (ACTIVE/ARCHIVED). Created by a user with `project.create` grant. |
| 4 | teams | Represents a team within a project. Contains name, code, and references to organization and project. |
| 5 | work_notes | Represents a daily work note capturing What/How/Why, blockers, next steps, and evidence. Linked to author, project, team, and optionally to a Jira issue. Status: DRAFT or CONFIRMED. |
| 6 | knowledge_objects | Represents a verified knowledge item with title, domain, category, content, lifecycle status (PROPOSED → UNDER_REVIEW → VERIFIED → ACTIVE → SUPERSEDED → DEPRECATED), version tracking, validity period, and review cadence. |
| 7 | chat_sessions | Represents an AI chat conversation with user, project scope, title, status, and scope filter for permission-aware retrieval. |
| 8 | handovers | Represents a handover process with predecessor/successor users, project/team scope, status (INITIATED → IN_PROGRESS → COMPLETED), reason, and timeline. |
| 9 | sources | Represents an uploaded document/file with metadata (filename, mimeType, size), Cloudflare R2 object key, SHA-256 hash for deduplication, and uploader reference. |
| 10 | jira_issues | Represents a synchronized Jira issue with external ID, issue key, summary, status, assignee, priority, and connection/project references. |
| 11 | notifications | Represents an in-app or email notification with recipient, type, title, message, read status, and related resource reference. |
| 12 | audit_logs | Immutable audit trail recording actions, actors, resource types/IDs, metadata, and timestamps. Append-only for SOC2/ISO compliance. |

---

### 3.2 User Account & Authentication Management

#### 3.2.1 Login

**Function trigger:** User navigates to the login page and submits email and password.

**Function description:**

**Actors:** Admin, Team Leader, Member

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

**Actors:** Admin, Team Leader, Member

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

**Actors:** Admin, Team Leader, Member

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

**Function trigger:** Admin or Team Leader (with `project.create` grant) clicks "Create Project" button.

**Function description:**

**Actors:** Admin, Team Leader (with grant)

**Purpose:** Create a new software project within the organization for knowledge management.

**Data Processing:**
1. Validate project name and code uniqueness within organization.
2. If actor is Team Leader, verify `project.create` capability grant is active and not expired.
3. Create project record with organizationId, name, code, description, status=ACTIVE.
4. Create initial project membership for the creator.
5. Log project creation in audit trail.

**Screen layout:**

> *[Screenshot placeholder: Create Project Page]*

**Function Details:**

**Validation:**
- Project name must be 3-100 characters.
- Project code must be 2-10 uppercase alphanumeric characters, unique within the organization.
- Team Leader must have an active, non-expired `project.create` grant.

**Business Rules:**
- Team Leaders can only create projects if explicitly granted `project.create` at organization scope by an Admin.
- The creator is automatically added as a project member.
- Creating a project does not make the creator an Admin or grant access to other projects.
- The `project.create` grant usage is logged in the audit trail.

**Functionalities:**

**Normal case:**
1. User fills in project name, code, and description.
2. System validates data and checks permissions.
3. System creates the project and initial membership.
4. The system displays "Project created successfully."

**Abnormal case:**
1. If project code already exists: System shows error ("Project code already in use.")
2. If Team Leader lacks grant: System shows error ("You do not have permission to create projects. Request a project.create grant from your Admin.")
3. If grant expired: System shows error ("Your project.create grant has expired. Contact your Admin.")

---

#### 3.3.2 Manage Teams

**Function trigger:** Admin or Team Leader navigates to the team management page within a project.

**Function description:**

**Actors:** Admin, Team Leader

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
- User must have Admin role or be Team Leader within the project.

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

**Function trigger:** Admin or Team Leader clicks "Add Member" or "Remove" on the team member list.

**Function description:**

**Actors:** Admin, Team Leader

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
- Admin or Team Leader of the specific team required.

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

#### 3.3.4 Grant / Revoke project.create Capability

**Function trigger:** Admin navigates to the Role & Grant Management page and grants or revokes a capability.

**Function description:**

**Actors:** Admin

**Purpose:** Grant or revoke the `project.create` capability to a Team Leader at organization scope.

**Data Processing:**
1. Validate the target user is a Team Leader.
2. Create/update organization_capability_grant record with subject, capability code, validity period, and issuing Admin.
3. For revocation: mark the grant as revoked with reason.
4. Log the grant/revocation in audit trail.

**Screen layout:**

> *[Screenshot placeholder: Grant Management Page]*

**Function Details:**

**Validation:**
- Only Admin role can perform this action.
- Target user must have TEAM_LEADER role.
- Cannot self-grant (Admin cannot grant capabilities to themselves if they're also a Team Leader).
- Validity period must be in the future.

**Business Rules:**
- The `project.create` grant is explicit, revocable, time-bounded, and audited.
- A leader cannot self-grant it or pass it to another person.
- The capability evaluator checks subject, issuing Admin, organization, expiry/revocation, and explicit deny.
- No broad condition such as `role === "TEAM_LEADER"` may substitute for this check.
- Grant/revocation immediately affects the user's effective permissions.

**Functionalities:**

**Normal case:**
1. Admin selects a Team Leader and sets the capability validity period.
2. System creates the capability grant record.
3. The system displays "project.create capability granted to [user] until [date]."

**Abnormal case:**
1. If user is not a Team Leader: System shows error ("Capability can only be granted to Team Leaders.")
2. If grant already active: System shows error ("User already has an active project.create grant.")
3. If validity period in the past: System shows error ("Validity period must be in the future.")

---

### 3.4 Daily Knowledge Capture

#### 3.4.1 Create Daily Work Note

**Function trigger:** Team member clicks "New Work Note" or "Today's Note" from the dashboard.

**Function description:**

**Actors:** Team Leader, Member

**Purpose:** Capture structured daily work knowledge including what was done, how, why, blockers, and next steps.

**Data Processing:**
1. If a Jira issue is linked, prefill context fields (task/issue, status, assignee, dates).
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
- Jira data prefills context but the person confirms the note.
- Notes can be created without Jira linkage (manual capture is primary).
- Auto-save preserves drafts to prevent data loss.
- A reminder follows up on missing required daily notes at 17:30.
- Notes are scoped to the author's project/team.

**Functionalities:**

**Normal case:**
1. User selects a date and optionally links a Jira issue.
2. Jira context is prefilled if linked.
3. User fills in What/How/Why, blockers, next steps, and evidence.
4. System saves as DRAFT.
5. The system displays "Work note saved as draft."

**Abnormal case:**
1. If all fields empty: System shows error ("At least one content field is required.")
2. If Jira connection fails: System shows warning ("Jira prefill unavailable. You can still create the note manually.")
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

### 3.5 Jira Integration

#### 3.5.1 Connect Jira Cloud

**Function trigger:** Admin clicks "Configure Jira" in the integration settings.

**Function description:**

**Actors:** Admin

**Purpose:** Establish a project-scoped connection to Jira Cloud for issue synchronization.

**Data Processing:**
1. Validate Jira site URL and credentials (OAuth2 or API token).
2. Create `jira_connections` record with encrypted credentials.
3. Register webhook URL for issue/comment events.
4. Test connection by fetching project list from Jira API.
5. Map Jira projects to Continuum AI projects.

**Screen layout:**

> *[Screenshot placeholder: Jira Configuration Page]*

**Function Details:**

**Validation:**
- Jira site URL must be a valid Atlassian Cloud URL.
- Credentials must be valid and have sufficient Jira permissions.
- Webhook URL must be reachable from Jira Cloud.

**Business Rules:**
- Only Admin can configure Jira connections.
- Credentials are stored encrypted in the secret store, never in MongoDB or logs.
- Webhook payloads are treated as untrusted input.
- Connection testing is required before activation.
- Initial import reads permitted issues after connection is established.

**Functionalities:**

**Normal case:**
1. Admin enters Jira site URL and credentials.
2. System validates and tests the connection.
3. System registers webhook and maps projects.
4. The system displays "Jira connection established successfully."

**Abnormal case:**
1. If invalid credentials: System shows error ("Unable to authenticate with Jira. Please verify your credentials.")
2. If Jira site unreachable: System shows error ("Cannot reach the Jira site. Please check the URL.")
3. If webhook registration fails: System shows warning ("Connection established but webhook registration failed. Automatic sync may be delayed.")

---

#### 3.5.2 Manual Sync Trigger

**Function trigger:** Admin or Team Leader clicks "Sync Now" on the Jira integration page.

**Function description:**

**Actors:** Admin, Team Leader

**Purpose:** Manually trigger synchronization of Jira issues to catch any missed webhook events.

**Data Processing:**
1. Enqueue a reconciliation job to BullMQ `jira-sync-queue`.
2. Fetch issues from Jira Cloud API with latest changes.
3. Compare with local `jira_issues` records.
4. Perform idempotent upserts for new/changed issues.
5. Mark deleted/restricted issues as withdrawn from retrieval.

**Screen layout:**

> *[Screenshot placeholder: Jira Sync Page]*

**Function Details:**

**Validation:**
- Jira connection must be active and credentials valid.
- Only Admin or Team Leader of the mapped project.

**Business Rules:**
- Duplicate event delivery does not duplicate issues, notes, or knowledge objects.
- Idempotency uses Redis SETNX with key `jira:event:{eventId}` (TTL 86,400s).
- Issues that become restricted in Jira are immediately withdrawn from Continuum retrieval.
- Sync progress and errors are visible in the sync status dashboard.

**Functionalities:**

**Normal case:**
1. User clicks "Sync Now."
2. System enqueues a reconciliation job.
3. System processes the sync and shows progress.
4. The system displays "Sync completed. [N] issues updated."

**Abnormal case:**
1. If Jira connection expired: System shows error ("Jira connection credentials expired. Please re-authenticate.")
2. If rate limited by Jira API: System shows error ("Jira API rate limit reached. Sync will retry automatically.")

---

### 3.6 Knowledge Lifecycle

#### 3.6.1 Propose Knowledge

**Function trigger:** User clicks "Propose Knowledge" from the knowledge base page, or AI extraction generates a proposal.

**Function description:**

**Actors:** Admin, Team Leader, Member

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

**Actors:** Admin, Team Leader, Member

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

**Actors:** Admin, Team Leader, Member

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

**Function trigger:** Admin or Team Leader clicks "Initiate Handover" for a departing or transferring team member.

**Function description:**

**Actors:** Admin, Team Leader

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
- Initiator must have Admin role or be Team Leader of the member's team.
- A successor must be a valid, active member (if assigned).

**Business Rules:**
- Handover analyzes all responsibilities, ownership, evidence, coverage, freshness, and concentration.
- Missing or overdue knowledge creates follow-up items automatically.
- Handover checklist items are prioritized by risk and coverage.
- The departing member's status transitions to OFFBOARDING.
- Team Leader or Admin must confirm completion of the handover.

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

**Actors:** Admin, Team Leader, Member

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
- Source ACL defaults to team-scope but can be configured by Admin/Team Leader.
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
| **Jira Cloud** | REST v3 API + Webhooks | Issue and task synchronization for work note context prefill. |
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
- **Idempotency:** Jira webhook processing uses event ID deduplication to prevent data corruption.
- **Error Recovery:** Failed ingestion jobs retain original files and expose retry state.
- **Dead Letter Queue:** Failed async jobs (email, Jira sync, ingestion) are routed to DLQ for manual inspection.
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
- **RBAC:** Three persistent roles with explicit capability grants and scoped assignments.
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
| BR-07 | project.create Grant | The `project.create` capability requires explicit, audited Admin grant. Team Leader role alone never implies this capability. |
| BR-08 | Author-Confirmed Notes | Work notes only become knowledge sources after the author explicitly confirms them. |
| BR-09 | No Performance Scoring | Missing daily notes trigger follow-up reminders, NOT employee performance scoring. |
| BR-10 | Successor Cannot Self-Confirm | Handover completion requires Team Leader or Admin confirmation, not the successor. |

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
| PROJ-003 | "You do not have permission to create projects." | Error | Missing project.create grant |
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
