# Integration Hub Research

**Trạng thái:** Hypothesis research; không chốt connector list, event contract hay architecture.

## Vì sao cần xem xét integration

Brief đặt Jira, Confluence, GitHub, Drive, Slack/Teams và Calendar cạnh nhau. `[INFERENCE]` Chúng có thể là các system-of-record chuyên biệt, không nhất thiết là “fragmentation” cần gom toàn bộ dữ liệu vào một database. Một internal layer có thể liên kết/điều phối mà không thay thế hệ thống nguồn.

`[DOCUMENTED]` Continuum MVP yêu cầu Jira Cloud task-context sync theo product research: initial import, webhooks, dedup/reconcile, retry/idempotency và revoke inaccessible content; manual capture vẫn primary. Connectors ngoài Jira hiện là stretch/future trong tài liệu MVP hiện hữu. Điều này KHÔNG phê duyệt Integration Hub tổng quát cho mọi tool.

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
| Task | Jira hoặc future internal platform | Canonical ownership, write-back, tombstone, reconciliation |
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

- `[DOCUMENTED]` Jira sync is in Continuum MVP product research.
- `[FACT]` Current source contains Jira-related schemas/queue scaffolding, but evidence reviewed does not establish a complete Jira Cloud API, OAuth, webhook, reconciliation or end-to-end user flow. Schema/scaffold ≠ working integration.
- `[DOCUMENTED]` Architecture target is Browser → Next.js BFF → NestJS monolith; MongoDB 7.0/shared `continuum_db` is operational SoT; LanceDB is auxiliary retrieval. See accepted DEC-011/013/014/015 and SPEC-001/003/004/005.
- `[FACT]` Current source search found no active LanceDB runtime dependency in BE; this is a target-vs-source implementation gap, not grounds to alter the accepted decision.
- `[UNKNOWN]` Provider credentials, tenants, rate limits, event subscription, service ownership and real connector behavior are not proven by repo scaffolding.

## External API references (examples only)

[Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/); [Linear webhooks](https://linear.app/developers/webhooks); [ClickUp API](https://developer.clickup.com/docs/Getting%20Started); [Asana webhooks](https://developers.asana.com/docs/webhooks-guide); [monday GraphQL API](https://developer.monday.com/api-reference/docs/basics); [Azure DevOps service hooks](https://learn.microsoft.com/en-us/azure/devops/service-hooks/services/webhooks?view=azure-devops). API availability does not mean connector completeness or permission equivalence.

## Decision questions

`[DECISION REQUIRED]` Which providers are in scope, what is source of truth per data class, read vs write, freshness SLA, ACL semantics, retention/deletion, supported identity mapping, and who owns connector operations? No broad connector hub should be inferred from one Jira integration requirement.
