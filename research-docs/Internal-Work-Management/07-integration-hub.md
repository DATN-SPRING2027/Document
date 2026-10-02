# Integration Hub Research

**Trạng thái:** Hypothesis research; không chốt connector list, event contract hay architecture.

> **Decision amendment — 2026-10-02:** Continuum owns the canonical task lifecycle in the MVP through its Task API/Task Service. The service runs separately but its source remains in the existing `DATN_BE` repository, and it owns task data in MongoDB `continuum_task`. Jira is not the task source and Jira import, webhooks, sync and reconciliation are outside the task MVP. This research remains relevant only to optional external-source integrations; it does not reopen the approved task-source decision. See [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md), [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md) and [Task Management Use Cases](12-continuum-task-management-use-cases.md).

## Vì sao cần xem xét integration

Brief đặt Jira, Confluence, GitHub, Drive, Slack/Teams và Calendar cạnh nhau. `[INFERENCE]` Chúng có thể là các system-of-record chuyên biệt, không nhất thiết là “fragmentation” cần gom toàn bộ dữ liệu vào một database. Một internal layer có thể liên kết/điều phối mà không thay thế hệ thống nguồn.

`[SUPERSEDED]` The earlier Jira task-context sync framing is no longer current: Continuum's Task API is canonical, and Jira is not part of the task-management MVP. For a separately approved future connector, link/read-only/event/import patterns still need source ownership, ACL, deletion and reconciliation decisions. This does not approve a general Integration Hub.

## Integration patterns cần phân biệt

| Pattern | Khi phù hợp | Rủi ro/unknown |
|---|---|---|
| Link out | Giữ dữ liệu canonical ở source, lưu URI/ID | Link rot, quyền source không được kiểm tra trong app |
| Read-only metadata sync | Cần tìm/roll-up nhẹ, không sửa source | Staleness, field mapping, deletion propagation |
| Event/webhook sync | Cần cập nhật gần thời gian thực | Retry, duplicate, ordering, delivery gap, reconciliation |
| Periodic import | Source webhook không đủ/tốn kém | Latency, rate limits, snapshot semantics |
| Bidirectional write | Có lý do cụ thể và ownership rõ | Conflict, loop, permissions, destructive writes, audit |

`[PROPOSAL]` Ưu tiên nghiên cứu read/link hoặc read-only sync trước bidirectional mutation; đây không phải architecture decision.

## System-of-record/ACL matrix to decide

| Data class | Source candidates | Quy tắc cần chốt |
|---|---|---|
| User identity | Continuum/IdP/Atlassian/GitHub | Identity mapping, deactivation, duplicate account |
| Task | Continuum Task API (canonical in MVP); Jira only a possible future external source | Any external import/link contract, field mapping, ownership, deletion and ACL propagation; must not create a second writable task source |
| Code/PR | GitHub | Visibility, repo install scope, deleted/private repo behavior |
| Docs/files | Drive/Confluence | Content vs link only, inherited ACL, version/deletion |
| Discussion | Slack/Teams | Consent/retention, channel ACL, event volume |
| Calendar/meeting | Calendar provider | PII boundaries, consent, timezone, event cancellation |
| Verified knowledge | Continuum | Human verification, provenance, project/team ACL |

## Minimum correctness concerns

- Identity mapping stable, explicit and auditable; no email-only guess if accounts can change.
- Webhook signature/authentication, source and tenant scoping, replay defense.
- Idempotency key and dedup strategy; retry/backoff with bounded poison-message handling.
- Ordering/version rules; out-of-order and deletion/revocation handling.
- Reconciliation job compares authoritative source and local projection; observable lag/errors.
- ACL propagation and permission re-check at read/retrieval time; no unauthorized content in LLM prompts, logs, caches or analytics.
- Data minimization, retention, export/delete, secret rotation and audit boundaries.

These are research checklist items, not claims that a generic Integration Hub is already implemented.

## Current DATN evidence vs target

- `[APPROVED TARGET]` Continuum Task API/Task Service is the canonical task source for the MVP; Jira task import/sync is excluded.
- `[FACT]` Current source contains Jira-related schemas/queue scaffolding, but this is legacy implementation evidence and does not make Jira an active task source or establish a complete Jira Cloud API, OAuth, webhook, reconciliation or end-to-end user flow. Schema/scaffold ≠ working integration.
- `[DOCUMENTED]` Architecture target is Browser → Next.js BFF → NestJS services; operational data uses MongoDB 7 on the existing replica set, with Task Service owning logical database `continuum_task`; LanceDB is auxiliary retrieval. See accepted DEC-011/013/014/015, [ADR-009](../../research-tech/ADR-009-internal-task-source-and-mongodb.md), [ADR-010](../../research-tech/ADR-010-task-service-in-existing-repositories.md) and SPEC-001/003/004/005.
- `[FACT]` Current source search found no active LanceDB runtime dependency in BE; this is a target-vs-source implementation gap, not grounds to alter the accepted decision.
- `[UNKNOWN]` Provider credentials, tenants, rate limits, event subscription, service ownership and real connector behavior are not proven by repo scaffolding.

## External API references (examples only)

[Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/); [Linear webhooks](https://linear.app/developers/webhooks); [ClickUp API](https://developer.clickup.com/docs/Getting%20Started); [Asana webhooks](https://developers.asana.com/docs/webhooks-guide); [monday GraphQL API](https://developer.monday.com/api-reference/docs/basics); [Azure DevOps service hooks](https://learn.microsoft.com/en-us/azure/devops/service-hooks/services/webhooks?view=azure-devops). API availability does not mean connector completeness or permission equivalence.

## Decision questions

`[DECISION REQUIRED — FUTURE CONNECTORS]` Which external providers, if any, are in scope; whether each is link-only/read-only; freshness, ACL, retention/deletion, identity mapping and operational ownership. The approved task source is not an open question: Continuum Task API remains canonical for MVP tasks. No broad connector hub is approved.
