# Pre-implementation Research Baseline: Refresh, Rotation & Sessions

**Ticket**: `DATN-14` (Inferred for this track)
**Status**: Research Only (No implementation, no code changes, no configuration/dependency changes)
**Target System**: DATN / Continuum AI Baseline

## 1. Scope
This document verifies the current state of refresh token workflows, session persistence, token hashing, token rotation, reuse detection, current/all-session revocation, expiry/TTL/indexes, concurrent sessions metadata, audit requirements, and FE refresh/logout/session restore behaviors.
*Constraint:* RESEARCH ONLY — no coding, source/config/dependency changes, PRs, or implementation.

## 2. Verified Checklist
- [x] Analyzed `product_docs`, `docs/architecture`, `docs/adr`, `docs/decisions`, `docs/specs`, `Danh Chia Task`, `DATN-BE`, and `DATN-FE`
- [x] Examined `DATN-BE` `refresh_sessions` Mongoose schema and `iam-v1.openapi.json`
- [x] Examined `DATN-FE` `useAuth.ts` and auth hooks for session restore/refresh logic
- [x] Compared leader requirements (SPEC-002, ADR-001)

## 3. Business Rules
| Rule | Source |
|---|---|
| **Session Rotation & One-time Use** | `iam-v1.openapi.json` |
| **Reuse Detection (Family Invalidation)** | `iam-v1.openapi.json` (returns 401 on reused revoked tokens) |
| **Session Metadata (IP, User Agent)** | `DATN-BE` schema |
| **HttpOnly BFF Cookies** | SPEC-002 / ADR-001 |

## 4. Requirement → Evidence → Implementation → Gap
| Requirement | Domain | Evidence | Current Implementation | Gap / Mismatch |
|---|---|---|---|---|
| **Refresh Token Rotation** | API / Business Logic | OpenAPI `/api/v1/auth/refresh` describes token rotation. | **None** | `[FACT]` Backend implementation is completely missing. |
| **Reuse Detection** | Schema / Business Logic | OpenAPI explicitly describes invalidating session family on token reuse. | `refresh_sessions` schema exists. | `[FACT]` Schema lacks `familyId` and `revokedReason`, making reuse chain tracking impossible. |
| **Session Expiry / TTL** | Schema | Tokens need automatic cleanup. | Schema has `expiresAt` field. | `[FACT]` No MongoDB TTL index defined for `expiresAt`. |
| **FE Refresh Behavior** | FE UI / Integration | FE needs to auto-refresh tokens upon expiration (401). | `useAuth.ts` defines login/logout/me only. | `[FACT]` `useAuth.ts` lacks any silent session restore or refresh mutation hook. |
| **All-Session Revoke** | API / Integration | Standard enterprise requirement (Logout from all devices). | OpenAPI only defines current-session `/logout`. | `[DECISION REQUIRED]` No endpoint for global revocation exists. |
| **Token Hashing** | Security / Schema | Tokens must not be stored in plaintext. | `refresh_sessions` has `tokenHash`. | `[PASS]` Schema field is present. (Logic pending). |

## 5. API/Contract Findings
- **Rotation & Reuse API**: `[FACT / VERIFIED]` The OpenAPI specifies that `/api/v1/auth/refresh` consumes a refresh token exactly once. Reusing a revoked token invalidates the entire session family. However, the backing schema is insufficiently modeled to support families.
- **Revocation API Constraints**: `[FACT / VERIFIED]` The OpenAPI `/api/v1/auth/logout` only revokes the presented current session. There is no API contract to retrieve a list of concurrent active sessions or to revoke them globally.

## 6. Data/Session Findings
- **TTL Indexes**: `[FACT / VERIFIED]` The Mongoose schema for `refresh_sessions` tracks `expiresAt` but completely omits a MongoDB TTL index (e.g. `{ expiresAt: 1 }, { expireAfterSeconds: 0 }`), risking infinite database bloat over time.
- **Schema Completeness**: `[FACT / VERIFIED]` The `refresh_sessions` collection tracks `tokenHash`, `ipAddress`, `userAgent`, and `isRevoked`. `[INFERENCE]` It is missing `familyId` (to group token chains), `revokedAt`, and `revokedReason`, which are strictly necessary for the reuse detection logic described in the API.

## 7. Security Findings
- **Concurrent Sessions & Audit**: `[INFERENCE]` The presence of `ipAddress` and `userAgent` fields suggests an intent to track and manage concurrent sessions. However, it is `[UNKNOWN]` if these lifecycle events must be explicitly logged to the `audit_logs` collection.
- **Cookie Delivery Mismatch**: `[FACT / VERIFIED]` As noted in the Auth baseline research, OpenAPI mandates JSON `refreshToken` bodies, breaking the SPEC-002 HttpOnly cookie boundary requirement.

## 8. FE/BE Mismatches
- **FE Refresh Client Missing**: `[FACT / VERIFIED]` `DATN-FE` `useAuth.ts` lacks a `useRefreshMutation` hook or a mechanism to handle silent session restoration on app initialization. The FE client is currently unaware of session rotation.

## 9. Dependencies
- **Mongoose**: Required for MongoDB TTL indexing on `DATN-BE`.
- **TanStack React Query**: Manages FE auth state, requires integration with Axios/Fetch interceptors for 401 refresh retries.

## 10. UNKNOWN / DECISION REQUIRED
- **Global Revocation**: `[DECISION REQUIRED]` Should the system support revoking all active sessions for a user (e.g., "logout from all devices" or concurrent session management view)?
- **Audit Logging Requirements**: `[DECISION REQUIRED]` Should refresh token rotation and revocation generate explicit entries in the `audit_logs` collection, given they represent security lifecycle events?

## 11. Implementation-Breakdown Recommendation
*Note: This is a RESEARCH ONLY task. Do not commence coding.*

1. **Schema Update**: `[DESIGN / PROPOSED]` Add `familyId` (String), `revokedAt` (Date), and `revokedReason` (String) to the `refresh_sessions` Mongoose schema. Add a MongoDB TTL index on the `expiresAt` field.
2. **BE Rotation Logic**: `[DESIGN / PROPOSED]` Implement the `/refresh` controller with strict one-time-use token hashing, family invalidation on reuse, and metadata (IP/UserAgent) capture.
3. **FE Refresh Client**: `[DESIGN / PROPOSED]` Implement a global 401 interceptor in the FE `apiClient` to silently call the refresh endpoint. Add a `useRefreshMutation` hook and update app initialization to support session restore.
4. **Audit Integration**: `[DESIGN / PROPOSED]` If required by PO, integrate session lifecycle events into the `audit_logs` outbox or service.
