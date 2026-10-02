# ADR-010: Deploy Task Management as a Service in the Existing Repositories

- **Status:** Accepted for service and repository boundaries
- **Date:** 2026-10-01
- **Decision owner:** Thang / Continuum AI project team
- **Scope:** Task service deployment, repository ownership, API/event integration, persistence ownership, audit, and Agent access
- **Supersedes:** The deployment and task-database placement portions of ADR-009. ADR-009 remains authoritative for the canonical task source, Jira exclusion, Work Note relationship, SAG eligibility boundary, and handover semantics.
- **Runtime status:** Accepted target, not included in the current active DATN-BE database inventory as of 2026-10-02. Provision `continuum_task` only with the Task service implementation and migration contract; see workspace ADR-003.

## Context

Continuum needs an owned task lifecycle that supports Work Note capture, knowledge verification, cited Q&A, and successor handover. The existing documentation branch had described Task as a module in the backend core and stored task collections in the shared operational database. The project’s microservice deployment pattern instead runs NestJS entrypoints as separate containers from one backend source repository, with service-owned MongoDB database names on the existing replica set.

The repository evidence is mixed: DATN_BE/docker-compose.microservices.yml defines a Gateway and independently started NestJS services, and src/services/service-bootstrap.ts starts both HTTP and Redis transports. However, DATN_BE/AGENTS.md and DATN_FE/AGENTS.md currently describe the backend as a modular monolith. The new Task service target must be reflected in those implementation guides before application code is changed.

## Decision

1. **Keep the current repository topology.** Do not create a separate ManageWork repository. Task backend source belongs in the existing DATN_BE repository; task screens and API client belong in the existing DATN_FE repository.
2. **Deploy Task as an independently runnable NestJS service.** Add a Task service entrypoint and container to the existing backend microservice deployment. It shares the DATN_BE build and repository but has its own process, configuration, health/readiness, logs, and service boundary. The frontend does not call the Task container directly.
3. **Route synchronous operations through the Gateway.** The frontend calls the existing BFF/API Gateway contract. The Gateway forwards task HTTP requests to the internal Task service. Work Note capture and Handover use the Task service contract for task validation, reads, and assignment commands. Service-to-service calls carry authenticated identity and correlation context; each service still enforces its own resource authorization.
4. **Use the existing NestJS hybrid service pattern.** The Task service uses the shared service bootstrap pattern: internal HTTP endpoints plus the existing Redis transport for message/event handling. Use synchronous HTTP for CRUD and assignment commands. Use events only for asynchronous consumers such as notifications or AI work.
5. **Give Task its own logical MongoDB database.** The Task service owns continuum_task on the existing MongoDB replica set and owns its collections, including tasks and append-only task_events. Do not create a new physical MongoDB cluster for the MVP. Reuse the existing Redis/BullMQ deployment with service-owned queue names rather than provisioning a separate Redis cluster.
6. **Keep cross-service data access behind contracts.** Capture and Handover store logical task IDs only; they do not read or write Task collections directly. Handover assignment is an idempotent Task API command with an operation ID and retry/compensation because Task and Handover do not share a database transaction.
7. **Separate audit history from event delivery.** Task mutations and their task_events record are written atomically in the Task database. If a mutation must publish an event, write an outbox record in the same transaction and relay it after commit. Consumers deduplicate by event ID. Audit records include actor type and identity, event/source, changed-field metadata, task version, timestamp, operation ID, and correlation ID. Do not persist full prompts or unrestricted raw AI context in the audit event.
8. **Integrate Agents through the Task contract.** The AI Engine may request authorized task context through an authenticated internal Task API. Agents may return a proposed rewrite or task change, but cannot write to Task storage directly. A user with permission confirms a proposal before the Task API commits it; the event records both the initiating user and the Agent/proposal identity.
9. **Do not change SAG storage in this decision.** Task records and lifecycle fields are not standalone SAG sources. Only eligible, authorized Work Notes and evidence follow the separately approved SAG ingestion and retrieval design.

## Service setup proposal

The intended source/deployment mapping is:

| Concern | Task target |
| --- | --- |
| Source repository | Existing DATN_BE |
| NestJS service entrypoint | src/services/task/main.ts |
| Runtime bootstrap | Existing bootstrapService(TaskModule) pattern |
| Internal HTTP port | Proposed 3009; confirm against the deployment port registry |
| Gateway configuration | TASK_SERVICE_URL=http://task:3009 |
| MongoDB logical database | continuum_task on the existing replica set |
| Task-owned collections | tasks, task_events, and outbox_events if reliable event publication is enabled |
| Internal HTTP route prefix | /internal per the existing shared NestJS service bootstrap |
| Async transport | Existing Redis/BullMQ infrastructure with Task-owned queue names |
| Frontend repository | Existing DATN_FE; browser requests use the BFF/Gateway contract |

The HTTP API contract, DTOs, response/error semantics, organization/project/team scope, and Agent authorization must be approved in OpenAPI before implementation. The port and queue names above are deployment proposals, not implemented configuration.

### Setup sequence against the existing NestJS pattern

1. Add the Task module and entrypoint under `DATN_BE/src/services/task/`; the entrypoint calls the existing `bootstrapService(TaskModule)`.
2. Reuse the shared backend build and service bootstrap. It starts internal HTTP and the existing Redis transporter; do not create a second backend repository or install a second platform stack.
3. Add a Task service definition to the backend deployment using the existing build, a dedicated command, `SERVICE_PORT`, and `SERVICE_DATABASE=continuum_task`. Keep its port internal; use the existing Mongo replica set and Redis.
4. Add Gateway configuration/controller for Task, modeled on the existing IAM proxy pattern. Forward authenticated user/scope and correlation context over an authenticated internal connection; do not expose the Task container to the browser.
5. Point the existing DATN_FE BFF/API client at the Gateway task routes. Capture and Handover call the Task contract for validation, reads and assignment. The AI Engine/Agent uses the same authorized contract and returns proposals; only a permitted human-confirmed command mutates task data.
6. Add readiness/health checks, structured logs, tracing IDs, bounded timeouts, retry/idempotency rules for cross-service commands, and database/outbox metrics. Final names and operational limits belong in the implementation contract.
7. Before code work, reconcile `DATN_BE/AGENTS.md` and `DATN_FE/AGENTS.md`, which currently describe a modular monolith, with the microservice deployment pattern evidenced by the source and Compose file.

The current Compose file still contains a Jira service entry while the task MVP excludes Jira sync. The implementation change should either remove that inactive deployment entry or document a remaining Jira use case before counting resources; Jira is not a dependency of Task.

## Alternatives considered

| Alternative | Pros | Cons | Decision |
| --- | --- | --- | --- |
| Task module in the same backend process | Lowest setup/deployment cost; simple local debugging and calls; fastest path if the deadline is the only concern | Shares release, scaling and failure boundaries with the core process; contradicts the existing independently launched NestJS service pattern and makes the Task boundary easier to bypass | Rejected for this target |
| Separate ManageWork backend/frontend repositories and service | Independent ownership, releases, CI pipelines and team autonomy | Adds repositories, CI, API versioning, access/configuration and cross-repo coordination; duplicates or adapts IAM/UI foundations; highest delivery and integration load without a separate team | Rejected |
| Existing DATN_BE/DATN_FE repositories, independently deployed Task service | Keeps current tooling, identity, UI and review workflow; Task keeps its own API, runtime, logical database, health/observability and release unit; supports Agents/Handover through explicit contracts and can be extracted later | Adds a container/process, internal network dependency, Gateway route, operational configuration and cross-service failure handling; the 6-week capacity needs a deliberately small P0 | Accepted |

For the current team and delivery window, the accepted option keeps the service boundary the microservice architecture expects while avoiding a new-repository integration project. It does not mean Task shares another service's database or runtime; it shares the backend repository/build and existing infrastructure only.

## Consequences and follow-up

- The Gateway needs a Task route and a protected internal upstream. The Task service must be reachable only inside the private service network.
- The Task service needs its own runtime configuration, MongoDB logical database, collection indexes, health/readiness checks, resource budget, dashboards/log fields, and deployment manifest.
- Task API availability becomes part of Work Note task linking and Handover assignment. Those flows need bounded timeouts, clear unavailable-service errors, idempotent retries, and no direct database fallback.
- A new service increases container, deployment, monitoring, and debugging work. Reusing the existing MongoDB replica set, Redis/BullMQ, Docker image build, Gateway, and repositories limits MVP overhead.
- The current BE/FE Agent guides still say modular monolith. Update those guides in the relevant application-repository PRs before implementing this architecture.
- Current compose/resource accounting must be reconciled as the Jira deployment is retired from the task MVP and the Task process is added.
- SAG engine references are inconsistent across the existing documentation (LanceDB in the technology/architecture overview, PostgreSQL + pgvector/Qdrant in storage/database design). Resolve that in a separate SAG decision; ADR-010 does not choose a vector engine.
- No application, schema, or migration code is changed by this documentation decision. If task data already exists in the former shared database when implementation begins, plan and verify an idempotent move into continuum_task before switching reads and writes.

## References

- [ADR-009: Continuum-owned task lifecycle](ADR-009-internal-task-source-and-mongodb.md)
- [Task-management Use Cases](../research-docs/Internal-Work-Management/12-continuum-task-management-use-cases.md)
- [NestJS Redis transporter](https://docs.nestjs.com/microservices/redis)
- [NestJS hybrid applications](https://docs.nestjs.com/faq/hybrid-application)
- Backend evidence: DATN_BE/src/services/service-bootstrap.ts, DATN_BE/src/gateway/gateway-iam.controller.ts, and DATN_BE/docker-compose.microservices.yml
