# Pre-implementation Research Baseline: Auth, Login & Session

**Ticket**: `DATN-13`  
**Assignee**: Nguyen Thi Thuy Tien  
**Due Date**: Sep 26, 2026  
**Status**: Research Only (No implementation, no code changes, no configuration/dependency changes)  
**Target System**: DATN / Continuum AI Baseline  

## 1. Scope
This document covers the current state of authentication, login workflows, token delivery mechanisms (Cookie vs Bearer), `/auth/me` endpoints, and the FE/BE contract for the Continuum AI / DATN project.
*Constraint:* RESEARCH ONLY — no coding, source/config/dependency changes, PRs, or implementation.
## 2. Verified Checklist
- [x] Analyzed `product_docs`, `docs/architecture`, `docs/adr`, `docs/decisions`, `docs/specs`, `Danh Chia Task`, `DATN-BE`, and `DATN-FE`
- [x] Reviewed `DATN-BE` OpenAPI spec (`iam-v1.openapi.json`)
- [x] Examined `DATN-BE` implementation code (IAM module)
- [x] Examined `DATN-FE` API client and BFF proxy implementation
- [x] Verified `DATN-FE` hooks (`useAuth.ts`, `useLoginMutation`)
- [x] Checked FE/BE contract alignment

## 3. Business Rules
| Rule | Source |
|---|---|
| **Role-based Authentication** | SRS (Login section) |
| **Brute-Force Prevention** (5 attempts/15 mins) | `05_SECURITY_AND_GOVERNANCE.md` |
| **Refresh Token Rotation & Reuse Detection** | `03_SERVICES_DEEP_DIVE.md`, `architecture_diagram.html` |
| **Token Delivery**: Tokens must use HttpOnly cookies | `DATN-FE/README.md`, `DATN-FE/AGENTS.md` |
| **Protected API Enforcement**: All endpoints except login/health require auth | SRS (CR-01) |

## 4. Requirement → Evidence → Implementation → Gap
| Requirement | Domain | Evidence | Current Implementation | Gap / Mismatch |
|---|---|---|---|---|
| **Login API** | API / Integration | `DATN-BE` OpenAPI (`/api/v1/auth/login`) | **None** in `DATN-BE` (`iam/controllers` is empty). | Implementation is entirely missing. |
| **Current User API** | API / FE UI | SPEC-002 defines `GET /api/v1/auth/me`. | FE `useAuth.ts` calls `/users/me`. BE OpenAPI and code omit this endpoint. | **Path Mismatch & Missing Endpoint**: FE must call `/api/v1/auth/me` and BE must implement it per SPEC-002. |
| **Token Storage** | Business Logic | SPEC-002/ADR-001 mandate `HttpOnly` cookies. | FE BFF proxies `Set-Cookie` blindly; BE OpenAPI returns tokens in JSON body (`AuthSession.tokens`). | **Critical Contract Mismatch**: If BE returns JSON, FE JS will receive tokens and violate the "No localStorage" rule. If BE sends cookies, OpenAPI is incorrect. |
| **Refresh/Logout Contract** | API / Integration | SPEC-002 defines refresh through `continuum_refresh` cookie and logout through cookies/Bearer. | BE OpenAPI (`/api/v1/auth/refresh`, `/api/v1/auth/logout`) expects `refreshToken` in JSON body. | **Critical Contract Mismatch**: OpenAPI violates SPEC-002 by requiring `refreshToken` in JSON payload rather than relying on cookies. |
| **Logout Response Conflict** | API | SPEC-002 specifies `200 OK` with `{ "status": "logged_out" }`. BE OpenAPI specifies `204 No Content`. | **None**. | **Unresolved Conflict**: Do not select a contract in this research task. Keep unresolved until an authorized decision is made. |
| **Protected-Route Errors** | Integration / E2E | Jira-required 401/403/409/422 behavior and protected-route/session behavior. | BE OpenAPI defines 401, 403, 409, 422 standard responses. | FE must intercept `401` globally to trigger session refresh workflows. |
| **Refresh Tokens** | Schema / API | BE OpenAPI (`/api/v1/auth/refresh`). | **None**. | Implementation is entirely missing. |

## 5. API/Contract Findings
- **Protected-Route Status Codes**: `[FACT / VERIFIED]` The OpenAPI defines standardized error responses for protected routes: `401 Unauthorized` (missing/expired session), `403 Forbidden` (lacks scope/permission), `409 Conflict` (resource state collision), and `422 ValidationFailed` (bad input). The FE must intercept `401` globally to trigger refresh workflows.
- **Logout Response Conflict & Empty Body Gap**: `[FACT / VERIFIED]` `DATN-BE` OpenAPI states `/api/v1/auth/logout` returns `204 No Content`. However, SPEC-002 section 2.3 explicitly specifies returning `200 OK` with `{ "status": "logged_out" }`. 

## 6. Data/Session Findings
- **Database Schema**: `[FACT / VERIFIED]` The database schema in `DATN-BE` includes `refresh_sessions` (with `tokenHash`, `userId`, `expiresAt`). The fields `familyId`, `revokedAt`, and `revokedReason` are documented/target fields but are missing from the current Mongoose schema implementation. Logic is unimplemented.

## 7. Security Findings
- **HttpOnly Boundary**: `[FACT / VERIFIED]` There is a severe implementation gap diverging from the SPEC-002/ADR-001 baseline. `DATN-FE` explicitly prohibits storing tokens in browser memory. However, `DATN-BE` is specified to return `TokenPair` in the JSON response, forcing frontend JavaScript to handle the raw tokens. The BFF `route.ts` is merely a dumb proxy; it does not intercept JSON tokens to inject them into `Set-Cookie` headers.
- **Brute-Force**: `[FACT / VERIFIED]` The 5 times/15 mins rate limiting is specified in architecture but unimplemented in code.

## 8. FE/BE Mismatches
- **API Naming / Path Mismatch**: `[FACT / VERIFIED]` SPEC-002 defines `GET /api/v1/auth/me`. `DATN-FE` expects `/users/me` to resolve the current session's profile, deviating from SPEC-002. `DATN-BE` OpenAPI does not declare `/api/v1/auth/me` endpoint.
- **Login/Refresh/Logout Contract**: `[FACT / VERIFIED]` The OpenAPI defines `LoginRequest` (email, password) and returns an `AuthSession` object with a `TokenPair` (accessToken, refreshToken, tokenType=Bearer) in the JSON body. Furthermore, OpenAPI requires `refreshToken` in JSON bodies for refresh/logout, while SPEC-002 explicitly defines refresh through the `continuum_refresh` cookie and logout through cookies or Bearer authentication.
- **Response Shape Mismatch**: `[FACT / VERIFIED]` `DATN-BE` OpenAPI defines `AuthSession` as nested with `tokens` and `user`. However, `DATN-FE` defines `AuthSession` (in `useAuth.ts`) as flat with `accessToken`, `tokenType`, and `expiresInSeconds`. Current FE auth tests (`useAuth.spec.tsx`) encode this stale, flat response shape.
- **Empty Body Gap**: `[FACT / VERIFIED]` Currently, the FE `apiClient` always parses successful responses with `response.json()`, which crashes on empty bodies like 204.

## 9. Dependencies
- `@aws-sdk/credential-provider-login` is present in BE, though possibly unrelated to user auth.
- `cookie`, `cookiejar`, `cookie-signature` are present in BE's lockfile, hinting at cookie capabilities.
- `tough-cookie` in FE.

## 10. UNKNOWN / DECISION REQUIRED
- **Logout Response Contract**: `[DECISION REQUIRED]` Resolve the explicit conflict between SPEC-002 section 2.3 (which mandates a `200 OK` JSON response `{ "status": "logged_out" }` for logout) and the current OpenAPI (which specifies `204 No Content`). Do not proceed with implementation until an authorized decision is made.
- **Service Prefixing**: `[UNKNOWN]` Will an API Gateway strip the `/api/v1` prefix in the future, or should `DATN-FE` unconditionally update its `apiClient` routes? (Note: For `Auth`, SPEC-002 is the accepted baseline, so we use `/api/v1/auth/*`).

## 11. Implementation-Breakdown Recommendation
*Note: DATN-13 is a RESEARCH ONLY task. Do not commence coding. Before coding, a dedicated Implementation Task must be identified/created with a bounded FE/BE scope, measurable acceptance criteria, edge cases, and dependencies.*

1. **Align with SPEC-002 Baseline**: `[DESIGN / PROPOSED]` Update BE OpenAPI and FE implementations to strictly follow SPEC-002/ADR-001 for HttpOnly BFF cookies, removing JSON-based refresh tokens.
2. **Contract Update**: `[DESIGN / PROPOSED]` Add `GET /api/v1/auth/me` to the `DATN-BE` OpenAPI spec per SPEC-002. Update the logout response based on the authorized decision (200 vs 204).
3. **Frontend Refactor**: `[DESIGN / PROPOSED]` Update FE `useAuth.ts` and auth tests to match the exact paths defined in SPEC-002 (`/api/v1/auth/me`), the nested `AuthSession` response shape, and implement global interceptors for 401/403 behaviors. Enhance `apiClient` to safely handle empty bodies if `204` is chosen.
4. **Backend Implementation**: `[DESIGN / PROPOSED]` Implement `AuthController` with endpoints: `/login`, `/refresh`, and `/logout`, writing session rows to `refresh_sessions` collection. Update the Mongoose schema to add the missing `familyId`, `revokedAt`, and `revokedReason` fields.
5. **Security Integration**: `[DESIGN / PROPOSED]` Implement Redis or in-memory Rate Limiter for the Brute-force constraint.
