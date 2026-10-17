# Email/password account registration and verification

**Status:** Approved by Thang on 2026-10-17. Implementation is in separate FE, BE and DB pull requests; approval of the product contract does not mean the feature is deployed or operationally accepted.

## Context

The earlier authentication research treated the existence of a sign-up form and the `PENDING_INVITE` membership state as competing evidence for public registration versus invite-only onboarding. Those facts describe different boundaries: an account identity can exist without access to an Organization.

## Decision

Allow public email/password account registration with email verification. The person submits a name and email and receives a generic acknowledgement. An eligible address receives a single-use verification link valid for 30 minutes. After opening the link, the person chooses a password; the account is created or linked only after the verification and password update commit.

The flow may create a new User or attach a password credential to an eligible active Google-only User with the same normalized email. It does not alter an existing password account, suspended/ineligible account or conflicting Google subject. Account creation does not create an Organization, Organization Membership, RoleAssignment, Platform authority or authenticated session. The user signs in normally after verification.

The verification token is high-entropy, stored as a digest, and carried in the URL fragment so it is not sent in the initial HTTP request. The FE removes the fragment before requesting a password. Responses do not disclose whether the email exists or whether delivery succeeded. An uncommitted verification that loses its claim remains retryable; an expired, consumed or ineligible token is terminal.

Organization invitations remain a distinct access-grant flow. Account registration alone never activates membership or bypasses the current membership, invitation, session and authorization rules. This decision does not approve general self-service Organization administration.

## Implementation contract and readiness

The detailed request/response/error contract, token/rate-limit rules, database design and rollout prerequisites are documented in the owning BE and DB proposals. Current implementation review links:

- [FE PR #30](https://github.com/DATN-SPRING2027/DATN-FE/pull/30)
- [DB PR #46](https://github.com/DATN-SPRING2027/DATN-BE/pull/46)
- [BE PR #47](https://github.com/DATN-SPRING2027/DATN-BE/pull/47)

These PRs remain subject to review, CI and human merge. Operational acceptance still requires the reviewed database migration to be applied, email delivery configuration, and a verified end-to-end flow. Do not mark a broader onboarding or membership work package ready solely because this account-registration policy is approved.

## Consequences

- Update the [Workspace decision register](00-organization-and-access-contract-readiness.md#6-cross-document-decision-register) and authentication research to distinguish account registration from Organization invitation and membership.
- Keep FE, BE and DB changes in separate branches and PRs; the DB migration and schema/index contract are reviewed in the DB PR.
- Keep public responses generic to prevent account enumeration; rate-limit requests and verification attempts.
- Preserve existing membership and authorization gates. A verified account is not an Organization member or Platform operator.
