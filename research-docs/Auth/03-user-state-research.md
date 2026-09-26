# Pre-implementation Research Baseline: User State & Password Flows

**Ticket**: `DATN-21` (Inferred for this track)
**Assignee**: Nguyen Thi Thuy Tien
**Status**: Research Only (No implementation, no code changes, no configuration/dependency changes)
**Target System**: DATN / Continuum AI Baseline

## 1. Scope
This document verifies the current state of user creation, invite/resend invitation workflows, activate/disable/update/soft delete mechanisms, status transitions, email normalization/uniqueness, last-admin protection, invitation expiry, password change/reset, profile relationships, and FE login/protected-route/error/loading states.
*Constraint:* RESEARCH ONLY — no coding, source/config/dependency changes, PRs, or implementation.

## 2. Verified Checklist
- [x] Analyzed `product_docs`, `docs/architecture`, `docs/adr`, `docs/decisions`, `docs/specs`, `Danh Chia Task`, `DATN-BE`, and `DATN-FE`
- [x] Examined `DATN-BE` `users` Mongoose schema and `iam-v1.openapi.json`
- [x] Examined `DATN-FE` components (`SignUpForm`, `SignInForm`) and auth hooks for password/invite states
- [x] Compared user schema status values against OpenAPI contracts

## 3. Business Rules
| Rule | Source |
|---|---|
| **User Status Transitions** | `iam-v1.openapi.json` (`ACTIVE`, `SUSPENDED`, `PENDING_INVITE`) |
| **Email Normalization** | `DATN-BE` Schema (`lowercase: true, trim: true`) |
| **Organization Roles** | `DATN-BE` Schema (`ADMIN`, `TEAM_LEADER`, `MEMBER`) |
| **Last-Admin Protection** | `[INFERENCE]` Standard B2B requirement to prevent organization lockout |

## 4. Requirement → Evidence → Implementation → Gap
| Requirement | Domain | Evidence | Current Implementation | Gap / Mismatch |
|---|---|---|---|---|
| **User Invite Workflow** | API / Business Logic | Schema has `PENDING_INVITE` status. | No API endpoints exist for `/invite` or `/resend`. | `[FACT]` Backend completely lacks invite endpoints and invitation logic. |
| **Invite Expiry & Secure Activation** | Schema / Security | Invites must expire securely. | `users` schema exists. | `[FACT]` Schema lacks `inviteToken`, `invitedBy`, and `inviteExpiresAt`. |
| **Password Change/Reset** | API / FE UI | FE `SignInForm.tsx` has `/reset-password` link. | No backend API or schema fields for reset. | `[FACT]` Missing `/password/reset` API, missing `resetToken` in schema, missing FE hooks. |
| **Status Transitions (Activate/Suspend)** | API / Business Logic | OpenAPI has `PATCH /api/v1/iam/users/{userId}` for status. | Controller not implemented. | `[FACT]` Status can be updated via PATCH, but activation from `PENDING_INVITE` needs a secure token flow. |
| **Profile Update** | API / Business Logic | OpenAPI `PATCH` allows updating mutable profile fields. | Controller not implemented. | `[FACT]` API exists in spec but lacks backend execution logic. |
| **Email Normalization** | Schema | Emails must be standardized. | Schema sets `lowercase: true, trim: true`. | `[PASS]` Normalization is handled natively by Mongoose. |
| **Email Uniqueness** | Schema | Users must not duplicate emails. | Schema lacks inline `unique: true`. | `[UNKNOWN]` Depends on external index definitions which were not verified as present. |
| **Last-Admin Protection** | Business Logic | Cannot suspend the only Admin. | No business logic implemented. | `[FACT]` No safeguard prevents an Admin from suspending themselves or being suspended by another, locking the org. |
| **Soft Delete** | API / Schema | Deleted users shouldn't break foreign keys. | OpenAPI has no `DELETE` user endpoint. | `[DECISION REQUIRED]` Does the system support soft delete, or is `SUSPENDED` the only terminal state? |
| **FE Login States** | FE UI | Login forms must display loading and error feedback. | `SignInForm.tsx` is completely static. | `[FACT]` No `isLoading` or `isError` bindings; the form doesn't even call `useLoginMutation`. |
| **Protected Routes** | FE Integration | Private pages must redirect unauthenticated users. | No `AuthGuard` or middleware found. | `[FACT]` Complete absence of protected-route enforcement in FE. |
| **E2E Test Coverage** | E2E | Auth flows require full E2E testing. | No Cypress/Playwright tests exist. | `[FACT]` Complete lack of E2E coverage for login, invite, and password flows. |

## 5. API/Contract Findings
- **Missing Invite Contracts**: `[FACT / VERIFIED]` The `iam-v1.openapi.json` defines a `GET` and `PATCH` for users, but explicitly lacks endpoints for creating users (`POST /users`), inviting users, or activating invitations.
- **Missing Password Contracts**: `[FACT / VERIFIED]` There are no OpenAPI definitions for changing passwords (authenticated) or resetting passwords (unauthenticated).

## 6. Data/Schema Findings
- **Missing Token Tracking**: `[FACT / VERIFIED]` The `users` collection lacks temporary token fields required for asynchronous workflows (e.g., `resetPasswordToken`, `resetPasswordExpires`, `invitationToken`, `invitationExpires`).
- **Profile Relationship**: `[FACT / VERIFIED]` The `users` collection tracks basic profile data (`fullName`, `avatarUrl`). FE relies on a `/users/me` (or `/api/v1/auth/me`) endpoint to fetch this, which is currently documented as a gap in the Auth baseline.

## 7. Security Findings
- **Last-Admin Lockout Risk**: `[INFERENCE]` Because the schema supports `ADMIN` roles and a `SUSPENDED` status, allowing arbitrary `PATCH` updates without a "last-admin" validation check creates a severe risk of locking an entire organization out of the system.
- **Password Hashing**: `[PASS]` The schema correctly stores `passwordHash` rather than plaintext passwords.

## 8. FE Architecture & Mismatches
- **Signup vs Invite Flow**: `[FACT / VERIFIED]` `DATN-FE` has a `SignUpForm.tsx` component, implying self-registration. However, the backend OpenAPI and schema (`PENDING_INVITE`) heavily imply an invitation-only B2B flow. `[DECISION REQUIRED]` Which flow is the intended product requirement?
- **Password Reset UI**: `[FACT / VERIFIED]` FE has UI linking to `/reset-password`, but there are no corresponding backend APIs or FE data-fetching hooks (`useResetPasswordMutation`) to support it.
- **Static Auth UI**: `[FACT / VERIFIED]` The current `SignInForm` is a pure visual mock. It does not bind to the `useLoginMutation` hook, lacks `onSubmit` handling, and completely omits `isLoading` (spinners) and `isError` (validation/server error) visual feedback states.
- **Missing Protected Routes**: `[FACT / VERIFIED]` There are no `AuthGuard` components or Next.js middleware configured to redirect unauthenticated users away from private dashboard routes.

## 9. Dependencies
- **Mongoose**: Manages user schema and email normalization.
- **Email Provider (e.g., SendGrid/AWS SES)**: Missing architectural dependency for sending invite and password reset emails.

## 10. UNKNOWN / DECISION REQUIRED
- **Self-Registration vs Invitation-Only**: `[DECISION REQUIRED]` Does the system allow public self-registration (as implied by FE `SignUpForm`), or is it strictly invite-only by Organization Admins (as implied by BE `PENDING_INVITE`)?
- **Soft Delete**: `[DECISION REQUIRED]` Should we implement a Soft Delete (e.g., `isDeleted` flag) or is moving a user to `SUSPENDED` status sufficient for offboarding?
- **Email Uniqueness Constraint**: `[DECISION REQUIRED]` Must verify if the database explicitly enforces a unique index on the `email` field per organization (or globally).

## 11. Implementation-Breakdown Recommendation
*Note: This is a RESEARCH ONLY task. Do not commence coding.*

1. **Schema Expansion Task**: `[DESIGN / PROPOSED]` Add `inviteToken`, `inviteExpiresAt`, `resetToken`, and `resetTokenExpiresAt` to the Mongoose `users` schema. Add a global/org-level unique index on `email`.
2. **API Contract Task**: `[DESIGN / PROPOSED]` Update OpenAPI to include `/api/v1/iam/users/invite`, `/api/v1/iam/users/activate`, and password reset endpoints.
3. **Business Logic Task (BE)**: `[DESIGN / PROPOSED]` Implement controllers with Last-Admin protection on suspend/role-change actions, and integrate an email service interface for sending tokens.
4. **FE State Task**: `[DESIGN / PROPOSED]` Create `useInviteMutation`, `useActivateMutation`, and `usePasswordResetMutation` hooks in `DATN-FE`, and bind them to the respective UI forms with proper loading/error states.
