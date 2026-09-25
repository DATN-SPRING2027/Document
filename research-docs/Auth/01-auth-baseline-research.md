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
- [x] Analyzed `product_docs`, `docs/architecture`, `docs/database-design`, `docs/research-docs`
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

| Requirement | Evidence | Current Implementation | Gap / Mismatch |
|---|---|---|---|
| **Login API** | `DATN-BE` OpenAPI (`/api/v1/auth/login`) | **None** in `DATN-BE` (`iam/controllers` is empty). | Implementation is entirely missing. |
| **Current User API** | FE `useAuth.ts` expects `/users/me`. | **None** in BE OpenAPI and code. | Missing endpoint in OpenAPI & code. |
| **Token Storage** | FE docs mandate `HttpOnly` cookies. | FE BFF proxies `Set-Cookie` blindly; BE OpenAPI returns tokens in JSON body (`AuthSession.tokens`). | **Critical Contract Mismatch**: If BE returns JSON, FE JS will receive tokens and violate the "No localStorage" rule. If BE sends cookies, OpenAPI is incorrect. |
| **API Path Prefix** | BE OpenAPI groups users under `/api/v1/iam/users`. | FE `useAuth` calls `apiClient("/users/me")`, which BFF routes to `/api/v1/users/me`. | **Path Mismatch**: FE omits `/iam` from the path. |
| **Refresh Tokens** | BE OpenAPI (`/api/v1/auth/refresh`). | **None**. | Implementation is entirely missing. |

## 5. API/Contract Findings
- **API Naming / Path Mismatch**: 
  - `DATN-FE` expects `/users/me` to resolve the current session's profile.
  - `DATN-BE` OpenAPI does not declare a `me` endpoint. It only defines `/api/v1/iam/users/{userId}`.
  - `DATN-FE` API client calls lack the `/iam` service prefix, whereas `DATN-BE` OpenAPI specifies it for user resources.
- **Login Contract**: The OpenAPI defines `LoginRequest` (email, password) and returns an `AuthSession` object with a `TokenPair` (accessToken, refreshToken, tokenType=Bearer) in the JSON body.
- **Data/Session Findings**: The database schema in `DATN-BE` includes `refresh_sessions` (with `tokenHash`, `familyId`, `userId`, `expiresAt`) intended for Secure Session Rotation and Reuse Detection, but the logic is unimplemented.

## 6. Security Findings
- **HttpOnly Boundary**: There is a severe conflict between the architecture documentation and the API specification. `DATN-FE` explicitly prohibits storing tokens in browser memory. However, `DATN-BE` is specified to return `TokenPair` in the JSON response, forcing frontend JavaScript to handle the raw tokens. The BFF `route.ts` is merely a dumb proxy; it does not intercept JSON tokens to inject them into `Set-Cookie` headers.
- **Brute-Force**: The 5 times/15 mins rate limiting is specified in architecture but unimplemented in code.

## 7. Dependencies
- `@aws-sdk/credential-provider-login` is present in BE, though possibly unrelated to user auth.
- `cookie`, `cookiejar`, `cookie-signature` are present in BE's lockfile, hinting at cookie capabilities.
- `tough-cookie` in FE.

## 8. UNKNOWN / DECISION REQUIRED
- **Token Delivery Mechanism**: Will the Backend natively set `HttpOnly` cookies and rely on the FE/BFF to forward them, or will the BFF intercept the `AuthSession` JSON response to set the cookie? 
- **Endpoint Design**: Should `/users/me` be added to `DATN-BE` OpenAPI, or will the FE parse the JWT to get `userId` and call `/api/v1/iam/users/{userId}`? (The former is standard).
- **Service Prefixing**: Should `DATN-FE` update its `apiClient` routes to include the `/iam/` prefix (e.g., `/iam/users/me`), or will an API Gateway strip it?

## 9. Implementation-Breakdown Recommendation
1. **Decision Gate**: Resolve the HttpOnly vs JSON Bearer token discrepancy. Recommendation: Backend handles Bearer authentication natively, but the Login endpoint returns `Set-Cookie` headers directly, which the Next.js BFF seamlessly proxies.
2. **Contract Update**: Add `/api/v1/auth/me` or `/api/v1/iam/users/me` to the `DATN-BE` OpenAPI spec.
3. **Frontend Refactor**: Update FE `useAuth.ts` to match the exact paths defined in BE (with correct `/iam` prefixes).
4. **Backend Implementation**: Implement `AuthController` with endpoints: `/login`, `/refresh`, and `/logout`, writing session rows to `refresh_sessions` collection.
5. **Security Integration**: Implement Redis or in-memory Rate Limiter for the Brute-force constraint.
