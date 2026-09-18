# Continuum AI — Database Design (MongoDB)

> Trạng thái: **Proposed / cần review trước khi tạo Mongoose schema**
>
> Phạm vi: MVP một software project, nhiều team; có thể mở rộng nhiều project/organization sau này.
>
> Nguồn chuẩn về nghiệp vụ/quyền: [MVP Scope](../research-docs/01_MVP_SCOPE.md), [Actors & Permissions](../research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md), [Tech Stack](../research-tech/Tech.md).

## 1. Mục tiêu và ranh giới lưu trữ

Thiết kế này phục vụ vòng lặp **ghi nhận kiến thức khi đang làm việc → kiểm chứng → theo dõi khoảng trống → chuyển giao cho người kế nhiệm**. Không thiết kế database như kho upload tài liệu và chatbot đơn thuần.

| Thành phần | Vai trò |
| --- | --- |
| MongoDB + Mongoose | Source of truth cho người dùng, project/team, quyền, trách nhiệm, tri thức, phiên bản, handover và audit. |
| Cloudflare R2 (ưu tiên), S3-compatible adapter dự phòng | Lưu file gốc, bản trích xuất và artifact lớn; MongoDB chỉ lưu metadata, object key, checksum, version. |
| SAG + LanceDB | Chỉ mục phục vụ retrieval; có thể tái tạo từ dữ liệu được phép trong MongoDB và file storage. Không phải nơi quyết định quyền hay trạng thái VERIFIED. |
| Redis + BullMQ | Queue/job runtime, retry và scheduling; MongoDB lưu trạng thái nghiệp vụ và tham chiếu job cần audit. |
| Evaluation dataset | Bộ câu hỏi, expected answer/citation và phiên bản dataset được quản lý riêng; không dùng câu trả lời của LLM làm ground truth. |

Mỗi document thuộc tenant phải có `organizationId`; document gắn project phải có `projectId`. `_id` dùng MongoDB ObjectId thống nhất trong các reference. Mọi thời gian lưu UTC, có `createdAt`/`updatedAt` và `createdBy`/`updatedBy` khi phù hợp. Mongoose validation không thay thế authorization ở service.

## 2. Mô hình quan hệ nghiệp vụ

`organization → project → team → memberships → user`

`organization → capability_grant(project.create) → TEAM_LEADER → project`

`Jira connection → Jira issue/revision → work note (human-confirmed) → knowledge proposal/evidence`

`project/team → responsibility → responsibility_assignment → user`

`responsibility → knowledge_requirement → knowledge_object → knowledge_version → knowledge_evidence → document_version/source`

`departing member/responsibility → handover → handover_item → successor assignment`

Điểm quan trọng: **trách nhiệm là thực thể độc lập**; assignment có khoảng hiệu lực để trả lời “ai nắm phần này vào thời điểm nào?”. Không suy ra lịch sử từ một `ownerId` hiện tại trên module. Tri thức có ID ổn định; nội dung đã công bố nằm trong version bất biến.

Quan hệ nhiều–nhiều hoặc tăng không giới hạn dùng collection tham chiếu (membership, evidence, owner, relation, handover item). Chỉ nhúng subdocument nhỏ, hữu hạn và thường được đọc cùng bản ghi cha (ví dụ cấu hình nhắc lại, summary progress). Không nhúng toàn bộ version/evidence/ACL vào một Knowledge Object.

## 3. Danh mục collection

Các collection đã nêu trong [Tech Stack](../research-tech/Tech.md) được giữ làm baseline. Bảng dưới mô tả thiết kế logic; tên/field/index cụ thể chỉ trở thành contract sau khi được review và triển khai ở DB PR.

| Nhóm | Collection | Mục đích và reference chính |
| --- | --- | --- |
| Tenant | `organizations`, `users`, `projects`, `teams` | Danh tính và cấu trúc project; team thuộc project. `users` chỉ lưu profile tối thiểu và password hash nếu dùng local auth. |
| Access | `project_memberships`, `team_memberships`, `roles`, `role_assignments` | Thành viên, vai trò cố định và phạm vi project/team. `roles` là catalog/permission mapping, không tự suy ra quyền từ tên role. |
| Capability | `organization_capability_grants` | Quyền `project.create` do ADMIN cấp riêng cho TEAM_LEADER, có hạn/thu hồi và audit. |
| Assignment | `sme_assignments`, `knowledge_owner_assignments`, `handover_assignments` | SME, Knowledge Owner, Successor theo scope và thời hạn; đây **không** phải persistent role. |
| Trách nhiệm | `responsibilities`, `responsibility_assignments`, `processes`, `knowledge_requirements` | Module/service/process và người chịu trách nhiệm theo thời gian; yêu cầu tri thức cần duy trì. Hai collection `responsibilities` và `responsibility_assignments` là **đề xuất bổ sung**. |
| Nguồn | `sources`, `source_acls`, `documents`, `document_versions`, `ingestion_jobs`, `sag_mappings` | Kết nối nguồn, quyền nguồn, metadata file, phiên bản file, ingestion và ánh xạ ID/chunk sang SAG. `document_versions` và `sag_mappings` là **đề xuất bổ sung**. |
| Jira & ghi chú | `jira_connections`, `jira_account_links`, `jira_issues`, `jira_events`, `jira_sync_jobs`, `work_notes`, `work_note_versions` | Đồng bộ task có idempotency và lịch sử; ghi chú do người xác nhận, tách khỏi dữ liệu Jira. |
| Chat | `chat_sessions`, `chat_messages` | Lưu lịch sử truy vấn/trả lời, citation reference và trạng thái insufficient-evidence theo policy retention. |
| Tri thức | `knowledge_objects`, `knowledge_proposals`, `knowledge_versions`, `knowledge_evidence` | Danh tính, bản nháp AI/human, snapshot được công bố, evidence có thể truy nguồn. `knowledge_proposals` là **đề xuất bổ sung**. |
| Quản trị tri thức | `knowledge_owners`, `knowledge_verifications`, `knowledge_relations`, `knowledge_gaps`, `knowledge_conflicts`, `interviews` | Owner, quyết định kiểm chứng, liên hệ, gap/conflict và câu hỏi phỏng vấn. |
| Chuyển giao | `handovers`, `handover_items`, `follow_up_tasks` | Quy trình chuyển giao, mục cần hoàn thành, nhắc/công việc phát sinh. `follow_up_tasks` là **đề xuất bổ sung**. |
| Bảo mật/audit | `resource_acls`, `refresh_sessions`, `audit_logs` | ACL cấp resource, refresh token đã băm, nhật ký bất biến. `resource_acls` và `refresh_sessions` là **đề xuất bổ sung**; có thể hợp nhất `resource_acls` với `source_acls` sau khi chốt policy. |

Không nhất thiết tạo mọi collection ở sprint đầu. Tuy nhiên không bỏ các quan hệ bắt buộc chỉ để giảm số collection; triển khai theo luồng end-to-end bên dưới. `roles` có thể là catalog seed tĩnh trong MongoDB hoặc constant trong code; cần chốt **một** nguồn chuẩn trước khi code để tránh drift.

## 4. Contract logic của các thực thể trọng tâm

Các field dưới đây là proposal, chưa phải Mongoose schema. Field `...Id` là reference; cùng tenant/project được kiểm tra khi ghi và khi đọc, không chỉ kiểm tra ObjectId tồn tại.

### 4.1. Membership và vai trò

| Collection | Field tối thiểu | Quy tắc |
| --- | --- | --- |
| `project_memberships` | `organizationId, projectId, userId, status, validFrom, validUntil` | `status`: ONBOARDING, ACTIVE, OFFBOARDING, ENDED. Lịch sử membership giữ lại; không xóa cứng khi rời project. |
| `team_memberships` | `organizationId, projectId, teamId, userId, status, validFrom, validUntil` | User phải có project membership hợp lệ; một user có thể thuộc nhiều team. |
| `role_assignments` | `organizationId, projectId?, teamId?, userId, roleCode, validFrom, validUntil, assignedBy` | Chỉ `ADMIN`, `TEAM_LEADER`, `MEMBER`; Admin ở org scope, Leader/Member theo project/team policy. Không cấp quyền qua role đã hết hạn. |
| `organization_capability_grants` | `organizationId, userId, capabilityCode, validFrom, validUntil?, revokedAt?, grantedBy` | `project.create` chỉ do Admin cấp cho Team Leader; tạo project cần kiểm tra grant còn hiệu lực và audit. |
| `sme_assignments` | `organizationId, projectId, userId, scopeType, scopeId, validFrom, validUntil` | SME chỉ trong domain/module/process/requirement được gán. |
| `knowledge_owner_assignments` | `organizationId, projectId, userId, scopeType, scopeId, validFrom, validUntil` | Người chịu trách nhiệm duy trì tri thức theo scope; khác quyền đọc mọi tài liệu. |

### 4.2. Trách nhiệm và yêu cầu tri thức

`responsibilities`: `organizationId, projectId, teamId?, code, title, type, description, criticality, status, parentResponsibilityId?`. `type` ban đầu nên giới hạn MODULE, SERVICE, PROCESS, OPERATION. Jira issue chỉ là evidence/context, không tạo responsibility cho từng issue.

`responsibility_assignments`: `organizationId, projectId, responsibilityId, userId, assignmentType, validFrom, validUntil, assignedBy`. `assignmentType` có thể là PRIMARY/BACKUP. Khi chuyển người phụ trách, đóng khoảng hiệu lực cũ và tạo assignment mới; không ghi đè lịch sử.

`knowledge_requirements`: `organizationId, projectId, teamId?, responsibilityId?, title, category, priority, cadenceDays?, dueAt?, status, ownerAssignmentId?`. Requirement xác định “phải có/update kiến thức nào” trong quá trình làm việc. Scheduler dùng nó để tạo gap/follow-up khi thiếu hoặc quá hạn; không tự thay đổi trạng thái VERIFIED.

### 4.3. Source, document và ingestion

`sources`: `organizationId, projectId, teamId?, type, externalRef?, name, status, ownerId, syncPolicy`. External connector/token không được lưu plaintext trong document.

`documents`: `organizationId, projectId, sourceId, title, currentVersionId?, sensitivity, status`. `document_versions`: `organizationId, projectId, documentId, versionNo, storageProvider, objectKey, sha256, mimeType, sizeBytes, uploadedBy, uploadedAt, parseStatus`. File bytes nằm ở private Cloudflare R2 trước (S3-compatible adapter dự phòng); không dùng MongoDB như file store.

`ingestion_jobs`: `organizationId, projectId, documentVersionId, operation, idempotencyKey, status, attemptCount, lastErrorCode?, startedAt?, finishedAt?`. Không lưu raw OCR text hoặc prompt chứa thông tin nhạy cảm trong lỗi/log. `sag_mappings` gắn `documentVersionId`/`sourceId` với `sagSourceId`, `sagDocumentId`, `sagChunkId`, `indexRevision`, `syncStatus`; giữ mapping khi re-index để citation vẫn tra được nguồn chuẩn.

`jira_connections` lưu `organizationId, projectId, jiraSiteId, externalProjectKey, status, credentialRef, lastReconciledAt` (không lưu token plaintext). `jira_account_links` ánh xạ user nội bộ với Jira account ID được phép. `jira_issues` lưu issue ID/key, revision, trạng thái, assignee, URL, ACL/sensitivity và bản nội dung đã chuẩn hóa. `jira_events` lưu khóa event/idempotency, loại sự kiện, issue ID, thời gian nhận/xử lý, trạng thái; `jira_sync_jobs` theo dõi backfill/reconciliation và lỗi. Unique key theo organization + connection + external ID/event để webhook lặp không sinh bản trùng.

`work_notes` lưu `organizationId, projectId, teamId?, authorId, workDate, jiraIssueId?, title, whatDone, howDone, why, blockers, nextSteps, evidenceRefs, status, confirmedAt?`. `work_note_versions` giữ lịch sử sửa có người và thời gian. Imported Jira fields là context riêng; chỉ note được author xác nhận mới tính vào báo cáo/handover. Note không có Jira vẫn hợp lệ.

`chat_sessions` và `chat_messages` lưu project/team/user scope, câu hỏi, answer status (ANSWERED/INSUFFICIENT_EVIDENCE), citation references và timestamps theo retention policy. Khi hiển thị lại phải kiểm tra ACL hiện tại; bản trả lời cũ không cấp quyền vĩnh viễn.

### 4.4. Knowledge object, proposal, version và evidence

| Collection | Field tối thiểu | Quy tắc |
| --- | --- | --- |
| `knowledge_objects` | `organizationId, projectId, teamId?, key, title, type, lifecycleStatus, currentVersionId?, sensitivity, reviewDueAt?, createdBy` | ID và `key` ổn định; status phản ánh trạng thái công bố hiện tại. Không đặt toàn bộ nội dung/version trong object. |
| `knowledge_proposals` | `organizationId, projectId, knowledgeObjectId?, proposedContent, proposerType, proposedBy?, modelRunRef?, status, createdAt` | AI/human draft ở PROPOSED/UNDER_REVIEW/REJECTED. Proposal không xuất hiện như tri thức VERIFIED trong RAG. |
| `knowledge_versions` | `organizationId, projectId, knowledgeObjectId, versionNo, content, summary, validityFrom?, validityUntil?, publishedAt, publishedBy, supersedesVersionId?` | Snapshot nội dung đã được phê duyệt; bất biến sau publish. Correction tạo version mới, không sửa bản cũ. |
| `knowledge_evidence` | `organizationId, projectId, knowledgeVersionId, sourceId, sourceType, sourceRevisionId, locator, quotedHash?, evidenceType` | Evidence trỏ đến **phiên bản** file, Jira issue/comment hoặc work note cụ thể. Citation phải resolve được hoặc báo mất nguồn. Không dùng `sagChunkId` đơn độc làm bằng chứng chuẩn. |
| `knowledge_verifications` | `organizationId, projectId, proposalId?, knowledgeVersionId?, reviewerId, decision, rationale?, decidedAt` | Chỉ người có quyền scope (Knowledge Owner/SME hoặc policy rõ ràng) được xác nhận. Lưu quyết định và audit. |

`knowledge_owners` là liên kết owner tới từng object/version nếu cần granularity nhỏ hơn `knowledge_owner_assignments`. Nếu cả hai được triển khai, phải quy định precedence và tránh hai “nguồn owner” mâu thuẫn. `knowledge_relations` nối hai object bằng loại quan hệ có kiểm soát; `knowledge_conflicts` ghi cặp claim/evidence cần giải quyết, không âm thầm lấy câu mới nhất làm đúng.

Vòng đời logic: `PROPOSED → UNDER_REVIEW → VERIFIED/ACTIVE → SUPERSEDED/DEPRECATED`; `REJECTED` là kết thúc của proposal. Phân biệt trạng thái proposal và trạng thái object/version trong schema thực tế; không dùng một enum duy nhất cho ba collection.

### 4.5. Handover, gap và follow-up

`handovers`: `organizationId, projectId, teamId?, departingUserId, responsibilityIds, status, initiatedBy, targetDate, completedAt?, waiverReason?`. Một handover có thể liên quan nhiều responsibility, nhưng `responsibilityIds` phải được giới hạn kích thước; nếu gói lớn thì dùng collection liên kết.

`handover_assignments`: `organizationId, projectId, handoverId, successorUserId, scope, validFrom, validUntil, assignedBy, status`. Successor chỉ được đọc phần gói chuyển giao **và** phần source/resource ACL cho phép; assignment không sao chép quyền của người rời đi.

`handover_items`: `organizationId, projectId, handoverId, responsibilityId?, knowledgeObjectId?, knowledgeVersionId?, requirementId?, type, status, ownerUserId?, dueAt?, completedAt?, verifiedBy?`. Item có thể là tài liệu cần cập nhật, phỏng vấn, checklist, câu hỏi mở, risk hoặc validation. Quyết định waiver phải lưu người phê duyệt/lý do trong audit.

`knowledge_gaps`: `organizationId, projectId, teamId?, responsibilityId?, requirementId?, knowledgeObjectId?, gapType, severity, detectedAt, status, resolvedAt?`. `follow_up_tasks`: `organizationId, projectId, gapId?, handoverItemId?, assigneeId, dueAt, status, reminderCount`. Cơ chế follow-up không được biến thành điểm đánh giá nhân sự.

### 4.6. Audit và phiên đăng nhập

`audit_logs`: `organizationId, projectId?, actorUserId?, action, resourceType, resourceId, outcome, occurredAt, correlationId, metadata`. Ghi role/ACL/membership change, verification, lifecycle, handover, truy cập nhạy cảm. Không lưu token, password, full prompt, nội dung file trong audit. Hạn chế sửa/xóa; chính sách retention cần được chốt.

`refresh_sessions`: `organizationId, userId, tokenHash, familyId, deviceId?, issuedAt, expiresAt, revokedAt?, reuseDetectedAt?`. Chỉ lưu hash của refresh token; rotation/reuse detection được xử lý trong NestJS. JWT access token ngắn hạn không cần lưu toàn bộ trong MongoDB.

## 5. Authorization và AI retrieval

Quyền hiệu lực = role còn hạn + project/team membership còn hiệu lực + capability grant/assignment đúng scope + source/resource ACL + lifecycle state − explicit deny. `ADMIN` quản lý cấu hình nhưng **không** mặc định đọc confidential knowledge; `TEAM_LEADER` và `MEMBER` chỉ xem nội dung phù hợp scope. `project.create` là grant cấp tổ chức do Admin cấp riêng, không gắn mặc định vào role Team Leader.

1. NestJS xác thực user và tính tập source/document/knowledge được phép **trước** khi gọi SAG.
2. Retrieval phải lọc theo tenant, project, ACL và trạng thái phiên bản đã công bố. Nếu SAG không hỗ trợ filter đủ mạnh, cần phân vùng index/adapter tương đương; post-filter đơn thuần không phải ranh giới bảo mật.
3. Sau retrieval, NestJS xác minh lại từng citation/reference theo ACL và phiên bản trước khi đưa nội dung vào LLM hoặc trả kết quả.
4. Nội dung file, OCR, prompt và output LLM là dữ liệu không tin cậy. AI chỉ tạo proposal; không tự nâng quyền, publish tri thức hoặc thay đổi handover.
5. Khi membership/ACL bị thu hồi, cache và retrieval index phải được vô hiệu hóa hoặc cập nhật theo policy; query tại nguồn vẫn từ chối ngay.

ACL inheritance: source/document đặt trần quyền cho knowledge được trích từ nó; Knowledge Object chỉ có thể siết chặt hơn, không nới rộng hơn evidence gốc nếu chưa có bước phân loại/duyệt riêng. Với nhiều evidence có ACL khác nhau, mặc định chọn tập quyền giao an toàn hoặc tách nội dung/citation; cần chốt rule cụ thể trước triển khai.

## 6. Index và ràng buộc đề xuất

Mọi index phải được xác nhận với query thật và `explain()` trước khi chốt. Dưới đây là baseline cho MVP, không phải lệnh migration.

| Collection | Index gợi ý | Mục đích |
| --- | --- | --- |
| `teams` | unique `(organizationId, projectId, code)` | Mã team trong project. |
| `project_memberships` | `(organizationId, projectId, userId, status)` | Kiểm tra quyền; nếu cần unique membership đang mở, dùng partial unique index với predicate trạng thái/`validUntil` rõ ràng. |
| `team_memberships` | `(organizationId, projectId, teamId, userId, status)` | Scope team. |
| `role_assignments` | `(organizationId, projectId, userId, roleCode, teamId, validUntil)` | Quyền còn hiệu lực; xử lý `teamId` null nhất quán. |
| `organization_capability_grants` | `(organizationId, userId, capabilityCode, revokedAt, validUntil)` | Kiểm tra grant `project.create` còn hiệu lực; unique grant mở cần policy rõ ràng. |
| `jira_issues` / `jira_events` | unique `(organizationId, connectionId, externalIssueId)`; unique `(organizationId, connectionId, eventKey)` | Đồng bộ có thể retry/lặp. |
| `work_notes` / `work_note_versions` | `(organizationId, projectId, authorId, workDate)`; unique `(workNoteId, versionNo)` | Ghi chú theo ngày/task và lịch sử chỉnh sửa. |
| `chat_messages` | `(organizationId, sessionId, createdAt)` | Lịch sử chat trong scope và retention. |
| `responsibilities` | unique `(organizationId, projectId, code)` | Business key ổn định. |
| `responsibility_assignments` | `(organizationId, projectId, responsibilityId, validUntil)` và `(organizationId, projectId, userId, validUntil)` | Người đang giữ trách nhiệm và lịch sử chuyển giao. |
| `knowledge_requirements` | `(organizationId, projectId, ownerAssignmentId, status, dueAt)` | Theo dõi thiếu/quá hạn. |
| `documents` / `document_versions` | `(organizationId, projectId, sourceId)`; unique `(documentId, versionNo)` | Nguồn và version file. |
| `knowledge_objects` / `knowledge_versions` | unique `(organizationId, projectId, key)`; unique `(knowledgeObjectId, versionNo)`; `(organizationId, projectId, lifecycleStatus, reviewDueAt)` | Resolve tri thức, version và freshness. |
| `knowledge_evidence` / `sag_mappings` | `(knowledgeVersionId, documentVersionId)`; `(organizationId, projectId, documentVersionId, indexRevision)` | Citation và re-index. |
| `handover_items` | `(organizationId, projectId, handoverId, status, dueAt)` | Progress/gap của gói. |
| `audit_logs` | `(organizationId, projectId, occurredAt)`; `(resourceType, resourceId, occurredAt)` | Điều tra theo thời gian/resource. |
| `ingestion_jobs` | unique `(organizationId, projectId, idempotencyKey)` | Chống tạo job trùng. |

Không tạo unique index trên `(userId, responsibilityId, validUntil)` một cách máy móc nếu `validUntil: null` xuất hiện nhiều bản; điều kiện “một assignment đang mở” cần được mô hình hóa rõ và kiểm thử concurrent write. Unique index không thay thế transaction/validation nghiệp vụ.

## 7. Transaction, nhất quán và cập nhật dữ liệu

- MongoDB trong Docker Compose phải chạy replica set để hỗ trợ multi-document transactions.
- Publish sau human verification: kiểm tra permission và evidence → tạo `knowledge_versions` mới → tạo `knowledge_evidence` → ghi `knowledge_verifications`/`audit_logs` → cập nhật `knowledge_objects.currentVersionId` và trạng thái trong **một transaction**. Dùng version number/conditional update để chống hai reviewer publish đè nhau.
- Đổi responsibility: đóng assignment cũ, tạo assignment mới, tạo/điều chỉnh handover và audit trong transaction phù hợp. Không xóa lịch sử.
- Upload R2 và gọi SAG không nằm trong MongoDB transaction. Dùng trạng thái PENDING/READY/FAILED, idempotency key, retry và reconciliation; chỉ công bố citation khi file/reference đã sẵn sàng.
- Dashboard coverage/freshness/concentration là read model có thể tính lại; không làm nguồn chuẩn thay cho collection nghiệp vụ.
- Mọi thay đổi Mongoose schema ảnh hưởng dữ liệu cũ cần script migration/backfill **mới, idempotent**, có kiểm tra và phương án phục hồi. Không sửa migration lịch sử.

## 8. Luồng truy vấn tối thiểu để kiểm chứng thiết kế

1. **Ai đang phụ trách module?** Tìm `responsibilities` theo project/code → `responsibility_assignments` còn hiệu lực → user/team, qua membership/ACL.
2. **Thiếu tri thức nào trước khi A rời đi?** Lấy assignment của A → `knowledge_requirements` → object/version còn hiệu lực và review date → `knowledge_gaps` → tạo `handover_items`.
3. **B được phép học gì?** Xác thực `handover_assignments` của B → lọc item theo project/team/scope → tính ACL từng knowledge/source → lấy published version và evidence → retrieval/citation.
4. **Câu trả lời AI có kiểm chứng được không?** Từ citation về `knowledge_evidence` → `document_versions`/source → quyền người hỏi → nội dung/locator/hash; nếu nguồn bị thu hồi, không hiển thị nội dung.
5. **Ai đã xác nhận nội dung tại thời điểm đó?** `knowledge_versions` → `knowledge_verifications` và `audit_logs`; bản cũ còn nguyên dù current version đã đổi.

## 9. Thứ tự triển khai MVP và quyết định còn mở

1. Tenant/project/team, user, membership, role, ACL và audit.
2. Manual work note và Jira issue sync (backfill/webhook/reconciliation), gắn task nhưng giữ tác giả xác nhận.
3. R2 source/document version/ingestion/mapping; knowledge proposal → verification → immutable version/evidence.
4. Chat/retrieval có ACL, citation, insufficient-evidence và dataset đánh giá.
5. Responsibility/assignment, gap/follow-up, handover/successor tối thiểu; dashboard derived. Phỏng vấn AI và phân tích transfer tự động là mở rộng sau vertical slice 10 tuần.

Cần review trước DB PR: (a) `roles` seed trong DB hay constant; (b) mô hình ACL thống nhất cho source/document/object và rule giao ACL nhiều evidence; (c) scope của `knowledge_owners` so với `knowledge_owner_assignments`; (d) cấu trúc content/locator chuẩn theo loại knowledge/source; (e) retention và backup cho file, audit, phiên đăng nhập; (f) volume/query mẫu để chốt index; (g) policy xử lý project/organization deletion; (h) dataset evaluation lưu ở repo/object storage nào và version hóa ra sao.

Tài liệu này **không** tạo collection, schema, index hoặc migration thực tế và không thay đổi dữ liệu. Khi triển khai, mỗi DB change đi trên branch/PR database riêng theo [AI workflow](../AI_WORKFLOW.md).

## Tài liệu tham khảo

- [MongoDB — Data Modeling: References](https://www.mongodb.com/docs/manual/data-modeling/referencing/)
- [MongoDB — Avoid Unbounded Arrays](https://www.mongodb.com/docs/manual/data-modeling/design-antipatterns/unbounded-arrays/)
- [MongoDB — Partial Indexes](https://www.mongodb.com/docs/manual/core/index-partial/)
- [MongoDB — Transactions](https://www.mongodb.com/docs/manual/core/transactions/)
