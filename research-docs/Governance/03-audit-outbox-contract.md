# [RESEARCH] Governance - Audit & Outbox Contract Baseline

**Ticket**: `DATN-17`  
**Assignee**: Nguyen Hong Phuc  
**Reporter**: danh2492004  
**Due Date**: Sep 26, 2026  
**Status**: Research Only (No coding, no configuration/dependency changes, no PR for implementation)  
**Target System**: DATN / Continuum AI Baseline  

---

## 1. Evidence Classification Standard (Truth Grading)

This research report strictly adheres to the project's evidence classification and truth grading standard:
- `[FACT / VERIFIED]`: Directly verified from existing source code in the repository (`DATN-BE`, `DATN-FE`).
- `[IMPLEMENTED]`: Executable behavior exists, is operational, and verifiable (not merely a schema, type definition, or interface).
- `[DESIGN / PROPOSED]`: Described in architecture documents, specifications, SRS, ADRs, or approved decisions, but not yet implemented in source code.
- `[PARTIAL]`: Supporting infrastructure/scaffolding exists (e.g., Mongoose schema, index declaration), but business logic or API layer is incomplete.
- `[GAP]`: Documented requirement exists in specifications but is completely absent from the current codebase.
- `[INFERENCE]`: Logical conclusion synthesized from multiple substantiated sources.
- `[UNKNOWN]`: Evidence is insufficient; no record found in documentation or source code.
- `[DECISION REQUIRED]`: Architectural discrepancies, unapproved matrices, or open policy points requiring team/lead consensus (unapproved contracts must not be invented).

---

## 2. Executive Summary

1. `[FACT]` / `[PARTIAL]` **Infrastructure Scaffolding Exists Across Services**: The backend persistence layer (`DATN-BE`) defines Mongoose schemas and service scaffolding for both Audit (`audit_logs` collection, `AuditService.append`) and Outbox (`outbox_events` collection, `OutboxService.append`) duplicated across multiple microservice infrastructure modules (`iam`, `lifecycle`, `jira`, `ingestion`, `notification`). In addition, `IdempotencyService` exists with a basic Redis `setIfAbsent` primitive.
2. `[GAP]` **Zero Event Production in Business Layer**: Crucially, neither `AuditService.append()` nor `OutboxService.append()` is invoked by any business controller, service, or mutation flow in `DATN-BE`. All current business logic (e.g., `/health`) produces zero audit logs or domain outbox events.
3. `[GAP]` **Transactional Outbox Guarantee Defect**: `OutboxService.append()` does not accept or pass a Mongoose `ClientSession`. Consequently, appending an outbox record cannot be executed within the same database transaction as the business aggregate update, breaking the core atomicity guarantee of the Transactional Outbox Pattern.
4. `[GAP]` **Missing Outbox Poller / Publisher Worker**: Although BullMQ and Redis connection helpers are registered in `DATN-BE`, there is no outbox dispatcher/publisher worker (polling or change-stream based) to transition outbox events from `PENDING` to `PUBLISHED` or dispatch them to downstream queues/subscribers.
5. `[GAP]` **Missing Standard Event Envelope Attributes**: The current `outboxSchema` lacks essential enterprise messaging fields: unique `eventId`, `schemaVersion`, `producerService`, `traceId`/`correlationId`, `retryCount`, and `nextRetryAt`.
6. `[GAP]` **Zero Sensitive-Data Masking / PII Exclusion**: Neither `AuditService` nor `OutboxService` implements sanitization hooks. Sensitive identity data (`passwordHash`, `twoFactorSecretEncrypted`, Bearer tokens, API credentials) could be inadvertently persisted into `metadata` or `payload` without an automated masking layer.

---

## 3. Scope & Focus

### 3.1. In Scope:
- **Audit Trail Contract**: Verification of authentication, user, project, member, team, role, and capability audit events (`audit_logs`).
- **Outbox Event Envelope**: Structure of domain events (`eventName`, `aggregateType`, `aggregateId`, `payload`, metadata).
- **Transactional Consistency**: Relationship between aggregate state mutations and outbox records within a single database transaction.
- **Idempotency & Deduplication**: Redis-based locking/deduplication (`IdempotencyService`), event deduplication keys, TTL, and consumer duplicate protection.
- **Retry & Failure Handling**: Outbox statuses (`PENDING`, `PUBLISHED`, `FAILED`), error tracking (`lastError`), retry backoff policies.
- **Consumer Boundaries**: Downstream worker boundaries, Redis/BullMQ event routing, and consumer isolation.
- **Sensitive Data Protections**: PII, credential, and secret exclusions from audit and event payloads.

### 3.2. Out of Scope:
- Modifying production backend code, writing queue dispatchers, or creating implementation PRs.
- Speculating on external Kafka/RabbitMQ brokers when specifications declare MongoDB + Redis/BullMQ.

---

## 4. Verified Requirements Checklist

| Requirement / Architectural Item | Source Evidence | Truth Grade | Current Codebase Finding & Status |
| :--- | :--- | :--- | :--- |
| **Dedicated Audit Log Collection (`audit_logs`)** | `10_AUDIT_AND_COMPLIANCE_SCHEMA.md`; `DATN-BE/.../mongodb.schemas.ts` | `[FACT]` / `[PARTIAL]` | Schema `auditSchema` declared in `iam` and `notification` modules. Connects to `AUDIT_DATABASE` (`continuum_audit`). `organizationId`, `projectId`, and `actorUserId` are optional strings. |
| **Immutable Audit Trail Guarantee** | `10_AUDIT...md` (Sec. 2.1) | `[DESIGN]` | Architecture specifies Append-Only audit trail without `updatedAt`. Current schema uses `{ timestamps: true }`, creating `updatedAt` field (`[MISMATCH]`). |
| **Audit Service Scaffolding** | `DATN-BE/.../audit/audit.service.ts` | `[FACT]` | `AuditService.append()` inserts directly into `audit_logs`. Zero callers exist in any business module. |
| **Audit Diff Payload (`before`/`after`)** | `10_AUDIT...md` (Sec. 2.1) | `[DESIGN]` / `[GAP]` | Architecture designs `diffPayload: { before?, after? }`. Code schema only contains unstructured `metadata: Schema.Types.Mixed`. |
| **Transactional Outbox Collection (`outbox_events`)** | `DATN-BE/.../mongodb.schemas.ts:6-23` | `[FACT]` | Fields: `eventName`, `aggregateType`, `aggregateId`, `payload`, `status` (`PENDING`, `PUBLISHED`, `FAILED`), `occurredAt`, `publishedAt`, `lastError`. |
| **Outbox Service Scaffolding** | `DATN-BE/.../outbox/outbox.service.ts` | `[FACT]` | `OutboxService.append()` performs `collection('outbox_events').insertOne(...)`. |
| **Transaction Atomicity (`ClientSession`)** | Enterprise Architecture / ADR | `[GAP]` | `OutboxService.append` does NOT receive a Mongoose `session`. Outbox write cannot be joined to aggregate transaction. |
| **Outbox Poller / Publisher Worker** | `03_SVC_JIRA_SCHEMA.md`; `01_SVC_IAM...` | `[GAP]` | No BullMQ worker or cron job processes `PENDING` outbox records. Records remain permanently `PENDING`. |
| **Redis Idempotency Helper** | `DATN-BE/.../redis/idempotency.service.ts` | `[FACT]` | `IdempotencyService.claim(key, ttlSeconds)` uses `redis.setIfAbsent(key, '1', ttlSeconds)`. Scaffolding only; zero callers in business controllers. |
| **Consumer Event Deduplication** | `03_DAILY_WORKFLOW_AND_JIRA_SYNC.md:54`; `SRS:972` | `[DESIGN]` / `[GAP]` | Architecture specifies Redis `SETNX` key `jira:event:{eventId}` (TTL 86,400s). No consumer implementation exists yet. |
| **Sensitive Data Redaction** | Security Policy / SOC 2 Baseline | `[GAP]` | No sanitization interceptor exists. Risk of leaking credentials or tokens into audit/outbox storage. |

---

## 5. Core Business Rules

### 5.1. Verified & Design Rules
1. **BR-AUD-01 (Append-Only Immutability)**: `[DESIGN]` Audit records in `audit_logs` must be strictly write-once, append-only. No HTTP endpoint or service method may expose update or delete operations on audit records.
2. **BR-AUD-02 (Mandatory Audit for Governance Mutations)**: `[DESIGN]` Every high-privilege mutation—including user authentication, role assignment, capability grant/revocation, project creation, and team membership modification—must emit an audit record containing actor, action, target resource, and timestamp.
3. **BR-OUT-01 (Transactional Consistency Guarantee)**: `[DESIGN]` An outbox event must be inserted within the exact same database transaction as the aggregate state change. If the transaction aborts, no outbox event is stored; if the aggregate persists, the outbox record is guaranteed to exist.
4. **BR-OUT-02 (At-Least-Once Delivery & Idempotency)**: `[DESIGN]` The outbox publisher guarantees at-least-once delivery to the message broker. Downstream consumers must be idempotent, deduplicating incoming events using `eventId` before executing side effects.
5. **BR-OUT-03 (Sensitive Data Exclusion)**: `[DESIGN]` Payloads emitted to `outbox_events` and `audit_logs` must exclude raw credentials, hashed passwords (`passwordHash`), two-factor secrets (`twoFactorSecretEncrypted`), and session tokens.

### 5.2. Open Rules & Discrepancies (`[UNKNOWN]` / `[DECISION REQUIRED]`)
- **BR-AUD-UN01**: Does `audit_logs` require an immutable database-level role (MongoDB user with write-only privilege, preventing database administrators from altering history)?
- **BR-OUT-UN01**: Should Outbox dispatching use a continuous MongoDB Change Stream worker or a scheduled BullMQ polling job (e.g., every 5 seconds)?
- **BR-OUT-UN02**: What is the dead-letter policy when an outbox event repeatedly fails to publish after max retry attempts (e.g., alert Slack/PagerDuty vs. dead-letter queue)?

---

## 6. Requirement ➔ Evidence ➔ Implementation ➔ Gap Matrix

| Architectural Layer | Requirement | Specification Evidence | Source Implementation | Technical Gap |
| :--- | :--- | :--- | :--- | :--- |
| **Audit Schema** | Standardized Audit Record Structure | `10_AUDIT...md` | `auditSchema` in `DATN-BE` | `[PARTIAL]` Lacks `diffPayload`, `ipAddress`, `userAgent`, and `actorEmail`. |
| **Audit Immutability** | Prevent Record Alteration | `10_AUDIT...md` | Mongoose schema with `timestamps: true` | `[GAP]` Generates `updatedAt`, which contradicts append-only immutability. |
| **Outbox Schema** | Transactional Outbox Table | `01_SVC_IAM...md` | `outboxSchema` in `DATN-BE` | `[PARTIAL]` Missing `eventId` (UUID), `traceId`, `producerService`, `retryCount`, `nextRetryAt`. |
| **Outbox Atomicity** | Atomic write with business aggregate | Microservice Pattern / ADR | `outbox.service.ts:16-22` | `[GAP]` `append()` does not receive Mongoose `ClientSession`. Cannot participate in transaction. |
| **Outbox Dispatcher** | Publish `PENDING` events to broker | `01_SVC_IAM...md:221` | None | `[GAP]` No worker or cron task reads and publishes `outbox_events`. |
| **Idempotency Primitive** | Atomic distributed lock / key reservation | `03_DAILY...md:54` | `IdempotencyService.claim` | `[PARTIAL]` Basic `setIfAbsent` exists, but lacks automatic release and consumer integration. |
| **Consumer Deduplication** | Ignore duplicate deliveries | `SPEC.md`, `SRS:972` | None | `[GAP]` No consumer middleware or decorator to enforce deduplication. |
| **Data Masking** | PII & Secret Redaction | `05_SECURITY...md` | None | `[GAP]` Raw objects passed to `payload` and `metadata` are unmasked. |

---

## 7. API, Data & Security Findings

### 7.1. Outbox Event Envelope Design vs. Current Code
Currently in `DATN-BE/src/services/*/infrastructure/mongodb/mongodb.schemas.ts`:
```typescript
// Current Code Schema
{
  eventName: { type: String, required: true, index: true },
  aggregateType: { type: String, required: true, index: true },
  aggregateId: { type: String, required: true, index: true },
  payload: { type: Schema.Types.Mixed, required: true },
  status: { type: String, enum: ['PENDING', 'PUBLISHED', 'FAILED'], default: 'PENDING', index: true },
  occurredAt: { type: Date, required: true, default: Date.now },
  publishedAt: Date,
  lastError: String,
}
```

**Proposed Standardized Enterprise Envelope (`[PROPOSED]`)**:
To support multi-service tracing, deduplication, and reliable retry, the outbox contract should be formalized as:
```typescript
export interface IOutboxEnvelope<T = Record<string, unknown>> {
  eventId: string;                   // UUID v4 - Unique event identifier for idempotency
  eventType: string;                  // e.g. "iam.user.registered", "iam.role.assigned"
  aggregateType: string;              // e.g. "User", "Project", "Team"
  aggregateId: string;                // String representation of Entity ObjectId
  producer: string;                  // e.g. "svc_iam", "svc_lifecycle"
  schemaVersion: string;              // e.g. "1.0.0"
  traceId?: string;                   // Correlation ID from HTTP x-request-id
  payload: T;                         // Sanitized domain data
  status: 'PENDING' | 'PUBLISHED' | 'FAILED';
  retryCount: number;                 // Starts at 0
  nextRetryAt?: Date;                // Exponential backoff timestamp
  occurredAt: Date;
  publishedAt?: Date;
  lastError?: string;
}
```

### 7.2. IAM Domain Events Catalog
Referencing `Document/database-design/01_SVC_IAM_SCHEMA.md` (Section 3), `svc_iam` defines four core outbox events:
1. `iam.user.registered`: Emitted upon user activation.
2. `iam.role.assigned`: Emitted when role is assigned/changed (invalidates Gateway permission caches).
3. `iam.capability.granted`: Emitted when `project.create` is granted to a Team Leader.
4. `iam.session.revoked`: Emitted upon user logout or session revocation.

### 7.3. Security & PII Exclusion Findings
- `DATN-BE` currently stores `passwordHash` and `twoFactorSecretEncrypted` in `users`.
- If a domain event `iam.user.updated` passes the raw user document to `OutboxService.append({ payload: userDoc })`, sensitive hashes and 2FA secrets would be written in plaintext to `outbox_events` and downstream logs.
- **Architectural Safeguard**: A strict DTO mapping or sanitization transform must strip sensitive fields before audit or outbox ingestion.

---

## 8. Frontend & Backend Mismatches & BFF Findings

1. **Audit Log Presentation**:
   - `[DESIGN]` TailAdmin specifications include an Audit Log View for Administrators.
   - `[GAP]` `DATN-FE` currently contains no audit log page, no `/audit` route, and no query hook for fetching audit events.
2. **Idempotency Keys from Client**:
   - `[DESIGN]` For critical state mutations (e.g., Jira issue sync, project creation), client requests can supply `X-Idempotency-Key`.
   - `[GAP]` Neither `DATN-FE/src/lib/api-client.ts` nor BFF proxy (`DATN-FE/src/lib/bff-proxy.ts`) currently generates or forwards `x-idempotency-key`.

---

## 9. Dependencies for Project & Team Authorization

The Governance Audit & Outbox system directly supports the access control and governance lifecycle:
1. **Audit as Compliance Anchor**: Changes to `role_assignments` and `organization_capability_grants` are legally and architecturally invalid without an accompanying audit record.
2. **Outbox as Cache Invalidation Mechanism**: When an `ADMIN` revokes a capability or role, an outbox event (`iam.role.assigned` / `iam.capability.revoked`) must notify the API Gateway and BFF cache to immediately invalidate existing JWT claims and permission caches.

---

## 10. UNKNOWN / DECISION REQUIRED

> [!IMPORTANT]
> The architectural decisions below are open points requiring team lead consensus. All suggestions are **exploratory and non-binding**.

| Decision ID | Open Architectural Question | Viable Options | Non-Binding Recommendation |
| :--- | :--- | :--- | :--- |
| **DEC-OUT-01** | **Outbox Dispatching Mechanism** | A. MongoDB Change Streams (real-time, requires Replica Set)<br>B. Polling worker via BullMQ / NestJS schedule | **Option B for MVP (Non-binding)**: A BullMQ scheduled poller (every 2-5 seconds) is easier to run locally in standalone Docker MongoDB without replica set configuration. |
| **DEC-OUT-02** | **Outbox Event Retention & Pruning** | A. Keep published events indefinitely<br>B. Delete published events immediately<br>C. TTL index pruning published events after 7 days | **Option C (Non-binding)**: MongoDB TTL index deleting records where `status = 'PUBLISHED'` after 7 days balances debugging traceability with storage efficiency. |
| **DEC-AUD-01** | **Audit Log Storage Strategy** | A. Co-located in same MongoDB instance under `continuum_audit`<br>B. Forwarded externally to CloudWatch / Datadog | **Option A (Non-binding)**: Maintain MongoDB `continuum_audit` for MVP, with immutable collection access rules. |

---

## 11. Implementation-Breakdown Recommendation

Following the mandatory multi-phase PR workflow defined in `Document/AI_WORKFLOW.md`:

```text
[1. DB PR] ────────► [2. BE PR] ────────► [3. FE PR]
```

### Phase 1: Database Branch & PR (`feat/Phuc-governance-audit-outbox-db`)
- Update `outboxSchema` across services to include `eventId` (unique index), `schemaVersion`, `producer`, `traceId`, `retryCount`, and `nextRetryAt`.
- Add TTL index for published outbox events (`publishedAt` + 7 days).
- Standardize `auditSchema`: remove `updatedAt` to ensure strict append-only immutability; add `actorEmail` and structured `diffPayload`.

### Phase 2: Backend Branch & PR (`feat/Phuc-governance-audit-outbox-be`)
- Refactor `OutboxService.append` and `AuditService.append` to accept optional `ClientSession` for transactional writes.
- Implement `OutboxPublisherWorker` using BullMQ to read `PENDING` outbox records and dispatch them to internal queues.
- Implement an outbound sanitization transform to strip PII and sensitive credentials before saving.
- Wire `AuditService` and `OutboxService` to core IAM mutations (`register`, `assignRole`, `grantCapability`).

### Phase 3: Frontend Branch & PR (`feat/Phuc-governance-audit-fe-ui`)
- Implement Audit Log Table view in TailAdmin admin panel.
- Add `x-idempotency-key` support to Next.js BFF proxy and `apiClient` for critical forms.
