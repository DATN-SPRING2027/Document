# Continuum AI — Daily knowledge capture and Jira sync

## Status and scope

- Status: Accepted workflow direction; field-level Jira mapping and OAuth/admin setup remain implementation decisions.
- Date: 2026-09-18
- Scope: 10-week MVP, one software project with multiple teams.
- Authority: [MVP scope](01_MVP_SCOPE.md), [actors and permissions](02_ACTORS_ROLES_AND_PERMISSIONS.md).

## 1. Capture while work is happening

The product cannot wait until a leader or member leaves. Every member, including Team Leaders, records lightweight knowledge during normal work. **Manual capture remains available and primary**; Jira is a source of task context and can reduce repetitive reporting, not a substitute for what a person learned.

End-of-day or task-update note, scoped to project/team/domain and optionally linked to a Jira issue:

| Field | Source | Required intent |
| --- | --- | --- |
| Task/issue, status, assignee, dates, link | Prefill from authorized Jira issue when linked | Trace work without retyping it. |
| What was done / outcome | Human confirms or edits | Record actual progress, not just issue status. |
| How it was done: technique, commands, approach | Human | Capture tacit technical knowledge. |
| Why: trade-offs, decision, constraint | Human | Explain reasoning to the successor. |
| Blocker/risk, next step, person to ask | Human | Make unfinished work actionable. |
| Evidence (PR, commit, file, issue comment, document) | Link or upload | Support verification and citation. |

Use a short draft with optional detail; allow notes without Jira. A reminder follows up on missing required updates and can be snoozed/explained. It is not a performance or time-tracking score. A report or handover summary can be drafted from confirmed notes and Jira context, but the author reviews it before sharing.

## 2. Jira Cloud integration (MVP)

1. An `ADMIN` configures a project-scoped connection and Jira project mapping with least-privilege credentials. Secrets live in a secret store/environment, not MongoDB or logs. Team Leaders can request or manage only delegated mappings.
2. Initial import reads permitted issues, descriptions, status, assignee, relevant changelog and comments. Store stable external IDs, source URL, timestamps, source permissions and sanitized text/metadata needed for citations. Do not assume every Jira field is visible to every Continuum user.
3. Webhooks enqueue issue/comment changes for near-real-time sync. Verify authenticity as supported by the selected Jira connection mode; treat payloads as untrusted. Use event IDs or deterministic hashes for deduplication, idempotent upserts, retries and dead-letter status.
4. Scheduled reconciliation catches missed/out-of-order webhook events, deleted/restricted issues and credential failures. Preserve source revision/history needed to explain a citation, but withdraw inaccessible content from retrieval immediately.
5. A note links to the Jira issue but remains a separate, author-confirmed record. A Jira status transition alone is not proof that a procedure, root cause or decision is correct.
6. Ingestion may propose Knowledge Objects from approved sources; every proposal starts `PROPOSED` and needs scoped human review before becoming official.

Jira content must pass Continuum project/team membership **and** applicable Jira/source ACL before it is indexed for a user or put into an LLM context. Index partitioning or prefiltering must enforce the boundary; post-filtering after a restricted chunk reached the LLM is insufficient. Revoke access promptly on Jira permission changes.

## 3. Document and chat path

Manual upload supports PDF, DOCX, Markdown, TXT and images. Originals live in **private Cloudflare R2** first; S3-compatible storage is an adapter/fallback, not a second mandatory deployment. MongoDB stores source metadata, ACL, checksum, object key and versions. Processing parses text, runs OCR where needed, chunks it and maps source versions/chunks to SAG's Event–Entity retrieval index. A failed job retains the original file and exposes retry state.

The core successor experience is an evidence-grounded **chat** over authorized, verified knowledge and permitted source material. Each answer shows traceable source/chunk, verification status and date. When evidence is inadequate, the assistant says so and offers a Knowledge Gap instead of guessing. Chat history must respect ACL changes; saved answers are not a permanent access grant.

## 4. Acceptance examples

- A member without Jira can submit a manual task note and later find it by project/team/domain.
- A linked Jira issue prepopulates context, while the member supplies how/why and confirms the note.
- Duplicate/out-of-order webhook delivery does not duplicate an issue, note or Knowledge Object.
- A private Jira issue or R2 document never appears in another team's retrieval context or citation.
- A report draft distinguishes imported task metadata from human-authored and AI-proposed text.
- An unsupported chat question produces an insufficient-evidence response and can become a gap.
- When a Team Leader requests a new project without `project.create`, the backend denies it; an Admin grant enables it only inside the granted organization and validity period.

## 5. Deferred work

MCP servers for other internal apps are an extension after Jira. They require a per-source connector, authentication, allowlisted tools/resources, ACL mapping and audit; MCP does not bypass Continuum authorization. Automated interview, interview-to-knowledge, advanced freshness/conflict detection, incident memory and automatic transfer analysis remain follow-up candidates. The evaluation dataset and permission-leak tests are **not** deferred.

References: [Jira Cloud issues API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/), [Jira webhooks](https://developer.atlassian.com/cloud/jira/platform/webhooks/), [Cloudflare R2 uploads](https://developers.cloudflare.com/r2/objects/upload-objects/), [MCP resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources).
