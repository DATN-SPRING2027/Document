> Scope update — user decision 2026-10-28: DEFERRED. The SAG team is not ready.
> WorkNote uses the application's existing configured MongoDB Capture connection.
> SAG integration and obtaining the DATN fork are not delivery blockers for the
> current rewrite/clarification/editor/Save scope. Keep the discovery below as
> historical preparation only; do not implement or activate ingestion now.

# SAG WorkNote boundary discovery — 2026-10-28

Status: evidence and unresolved integration inputs, not an approved consumer
contract or running SAG integration. No external data was uploaded and no public
repository was modified.

Local brief points to sag-laya-integration/SAG, which is not present under the
current DATN project workspace. Current BE has an external AiEngineModule and
provider-neutral HTTP adapter; status routing references project/document/version
paths. Capture emits KNOWLEDGE_SOURCE_APPROVED, KNOWLEDGE_SOURCE_REPLACED and
KNOWLEDGE_SOURCE_REVOKED. Emitting an event is not proof that a downstream
consumer has indexed or removed content.

The configured source documentation references public upstream Zleap-AI/SAG.
Read through the GitHub connector at exact main tree commit
`e68cdeb3a770ff9b35c90a516474e281d3c82a3a`:

- [documents.py](https://github.com/Zleap-AI/SAG/blob/e68cdeb3a770ff9b35c90a516474e281d3c82a3a/apps/api/sag_api/api/v1/documents.py)
  exposes source-scoped upload and `/sources/{source_id}/documents/ingest` text
  ingestion with user/connector dependencies and document processing jobs.
- [security.py](https://github.com/Zleap-AI/SAG/blob/e68cdeb3a770ff9b35c90a516474e281d3c82a3a/apps/api/sag_api/core/security.py)
  contains SAG password/JWT primitives. It is not evidence of DATN Organization/
  Project authorization or current WorkNote source eligibility.

Inference from these reads: upstream generic ingestion cannot be assumed to
implement the project-scoped version/status/ACL/revoke contract used by DATN's
adapter. The actual DATN SAG fork/revision/runtime and ownership must be identified
before writing a consumer or choosing its deployment target. No new vector store,
consumer queue, service token or public API is invented in this package.

Required concrete inputs: actual integration repository/path and deployed
revision, service-to-service authority and partition mapping, source/version
idempotency mapping, synchronous eligibility/revocation check, citation target
and replacement/de-index acknowledgment. Current Task Notes do not automatically
become official knowledge. Document/Report drafts, pending/rejected content and
raw/chat/proposals are never eligible.

Once those inputs exist, prepare an explicit contract and test approval→search,
duplicate events, out-of-order replacement, archive and immediate ACL revoke,
old citations and cross-Project denial before asserting SAG readiness.
