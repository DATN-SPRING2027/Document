# Continuum AI — Schema Dịch Vụ Hỏi Đáp Tri Thức Có Dẫn Chứng
## (Cited Assistant & Chat Schema - svc_chat)

> **Database:** `continuum_chat` (MongoDB 7.0)  
> **Service sở hữu độc quyền:** `svc_chat`  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ (Bounded Context)

`svc_chat` là dịch vụ giao tiếp thông minh giữa thành viên dự án và kho tri thức hệ thống:
1. **Hỏi Đáp Bắt Buộc Dẫn Chứng (Strict Citations Enforced):** Không cho phép mô hình LLM chém gió vô căn cứ. Mọi câu trả lời bắt buộc phải đính kèm mảng `citations` chỉ rõ trích đoạn lấy từ tài liệu/tri thức nào, phiên bản bao nhiêu.
2. **Xử lý Khi Không Đủ Bằng Chứng (`INSUFFICIENT_EVIDENCE`):** Nếu độ tương đồng truy xuất từ SAG Engine dưới ngưỡng an toàn (VD: `< 0.65`), hệ thống chủ động thông báo *"Không tìm thấy đủ bằng chứng kiểm chứng để trả lời câu hỏi này"* và gắn cờ log để đội ngũ kỹ thuật bổ sung tài liệu.
3. **Nhật ký Đánh giá & RAG Tuning (`query_logs`, `retrieval_logs`):** Lưu trữ toàn bộ dữ liệu truy vấn và phản hồi của người dùng (Thumbs Up/Down) để phục vụ đo lường và tinh chỉnh Prompt/Rerank.

---

## 2. Chi Tiết Schemas Mongoose (Database: `continuum_chat`)

### 2.1. `chat_sessions` (Phiên hội thoại hỏi đáp)
```typescript
export interface IChatSession {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  userId: string;                    // Logical Ref sang svc_iam.users._id
  
  title: string;                     // Tiêu đề phiên (VD: "Tìm hiểu cơ chế Webhook Retry")
  contextScope: 'PROJECT' | 'TEAM' | 'MODULE';
  targetTeamId?: Types.ObjectId;
  
  status: 'ACTIVE' | 'ARCHIVED';
  messageCount: number;
  lastMessageAt: Date;
  
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, projectId, userId, status, lastMessageAt)`: `{ index: true }`

---

### 2.2. `chat_messages` (Tin nhắn & Dẫn chứng bằng chứng)
```typescript
export interface IChatCitation {
  knowledgeObjectId: string;         // Logical Ref sang svc_lifecycle.knowledge_objects
  versionNumber: number;             // Phiên bản được trích xuất
  title: string;                     // Tiêu đề tri thức
  excerpt: string;                   // Đoạn văn trích dẫn trực tiếp
  confidenceScore: number;           // Điểm số tương đồng (0.00 -> 1.00)
}

export interface IChatMessage {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  chatSessionId: Types.ObjectId;     // Ref sang chat_sessions._id
  
  role: 'USER' | 'ASSISTANT' | 'SYSTEM';
  content: string;
  
  // Trạng thái xử lý của trợ lý
  status: 'COMPLETED' | 'INSUFFICIENT_EVIDENCE' | 'FAILED';
  
  // Bắt buộc đối với tin nhắn của ASSISTANT
  citations: IChatCitation[];
  
  // Siêu dữ liệu đo lường hiệu năng
  retrievalLatencyMs?: number;
  llmLatencyMs?: number;
  tokensPrompt?: number;
  tokensCompletion?: number;
  modelName?: string;                // "gemini-1.5-flash", "gpt-4o-mini"
  
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(chatSessionId, createdAt)`: `{ index: true }`
  - `(organizationId, projectId, status, createdAt)`: `{ index: true }`

---

### 2.3. `chat_feedbacks` (Phản hồi đánh giá của lập trình viên)
```typescript
export interface IChatFeedback {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  messageId: Types.ObjectId;         // Ref sang chat_messages._id
  userId: string;
  
  rating: 'THUMBS_UP' | 'THUMBS_DOWN';
  reasonCategory?: 'INACCURATE' | 'OUTDATED' | 'IRRELEVANT_CITATION' | 'INCOMPLETE';
  userCorrectionText?: string;       // Gợi ý sửa của lập trình viên
  
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(messageId, userId)`: `{ unique: true }`
  - `(organizationId, rating, createdAt)`: `{ index: true }`

---

### 2.4. `query_logs` & `retrieval_logs` (Nhật ký truy vấn & Độ phủ tìm kiếm)
```typescript
export interface IQueryLog {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  userId: string;
  userQuery: string;
  normalizedQuery: string;
  
  hasInsufficientEvidence: boolean;  // Cờ nhận biết cần bổ sung tài liệu
  intentDetected?: string;
  
  createdAt: Date;
}

export interface IRetrievalLog {
  _id: Types.ObjectId;
  queryLogId: Types.ObjectId;
  vectorTopK: number;
  highestSimilarityScore: number;
  lowestSimilarityScore: number;
  sagCandidateChunkIds: string[];    // ID các chunk do SAG Engine trả về
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, projectId, hasInsufficientEvidence, createdAt)`: `{ index: true }`
  - `(queryLogId)`: `{ index: true }`

---

## 3. Giao Tiếp Sự Kiện (Domain Events)

- **Sự kiện xuất bản:**
  - `chat.insufficient_evidence.flagged`: Bắn sự kiện khi có câu hỏi không tìm thấy tài liệu, giúp `svc_lifecycle` cân nhắc tạo một `knowledge_gap` tự động.
  - `chat.query.completed`: Phục vụ thống kê số lượng câu hỏi và tần suất tra cứu tài liệu theo team.

---

## 4. Schema Human Chat & Trợ Lý 1–1 `@continuumAI` (Active Runtime — `continuum_chat`)

> **Đồng bộ runtime (`28/11/2026`):** Đối chiếu trực tiếp với `DATN_BE/src/services/chat/infrastructure/persistence.ts`, `mongodb/mongodb.schemas.ts` và migration `20261128-chat-dm-assistant-schema` (`DATN-BE#158` merged `main` tại `31e1dcf` từ `4a19f83`; Chat BE `DATN-BE#159` tại `50955a1`). Các collection dưới đây nằm trong cùng database `continuum_chat` nhưng tách biệt hoàn toàn với nhóm Cited Assistant (`chat_sessions`/`chat_messages`) ở Mục 2. Xem thêm kiến trúc runtime tại [10_HUMAN_CHAT_RUNTIME_ARCHITECTURE.md](../architecture/10_HUMAN_CHAT_RUNTIME_ARCHITECTURE.md).

Hằng số định danh tác giả AI trong Human Chat 1–1:
- `CONTINUUM_AI_SENDER_ID = 'assistant:continuum_ai'` (không phải 24-hex ObjectId nên không thể trùng `userId` người thật)
- `CONTINUUM_AI_DISPLAY_NAME = 'Continuum AI'`
- `CONTINUUM_AI_HANDLE = 'continuumAI'`

### 4.1. `chat_conversations` (Hội thoại `DIRECT` & `ROOM`)

```typescript
export interface IChatConversation {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  type: 'DIRECT' | 'ROOM';
  directKey?: string;               // <orgId_hex>:<sorted_userId_1>:<sorted_userId_2> (unique, sparse)
  creationKey?: string;             // idempotency từ clientRoomId (unique, sparse)
  title?: string;                   // maxlength 80
  createdBy: string;
  lastMessageAt: Date | null;
  lastMessageId: Types.ObjectId | null;
  lastMessagePreview: string;       // AI reply: ('Continuum AI: ' + content).slice(0, 180)
  lastMessageSenderId: string | null;
  membershipVersion: number;        // default 0
  contextRevision?: number;         // int >= 0 (logical default 0); $inc: 1 khi sửa/xóa tin người trong DIRECT, setBlock (block/unblock) DIRECT & Step 5a worker commit
  status: 'ACTIVE' | 'ARCHIVED';
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:** `{ directKey: 1 }` (`unique`, `sparse`), `{ creationKey: 1 }` (`unique`, `sparse`), `{ organizationId: 1, status: 1, lastMessageAt: -1, _id: -1 }`.

### 4.2. `chat_members` (Thành viên hội thoại, cursor đọc/nhận & bản nháp)

```typescript
export interface IChatMember {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  conversationId: Types.ObjectId;
  userId: string;
  displayName: string;
  searchLabel: string;
  avatarUrl: string | null;
  role: 'OWNER' | 'MANAGER' | 'MEMBER';
  status: 'ACTIVE' | 'LEFT';
  lastReadMessageId: Types.ObjectId | null;
  lastReadAt: Date | null;
  readRecordedAt: Date | null;
  lastDeliveredMessageId: Types.ObjectId | null;
  lastDeliveredAt: Date | null;
  deliveredRecordedAt: Date | null;
  notificationMode: 'ALL' | 'MENTIONS' | 'NONE';
  isPinned: boolean;
  isArchived: boolean;
  markedUnread: boolean;
  draft: string;                    // maxlength 8000
  draftMentionUserIds: string[];
  draftAssistantMention?: boolean;  // default false — giữ trạng thái @continuumAI giữa Full Chat và Mini Chat
  draftUpdatedAt: Date | null;
  joinedAt: Date;
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:** `{ conversationId: 1, userId: 1 }` (`unique`), `{ userId: 1, organizationId: 1, status: 1, conversationId: 1 }`.

### 4.3. `chat_conversation_messages` (Tin nhắn người dùng & tin AI `@continuumAI`)

Tương thích ngược 100% với tin cũ chưa có các trường AI (không cần backfill). Trong Mongoose (`mongodb.schemas.ts`), mọi trường tùy chọn dành riêng cho AI đều khai báo **`default: undefined`** (đặc biệt `sourceReferences` không được mặc định thành `[]`) để tin người dùng luôn khớp nhánh Human của `$jsonSchema` validator (`validationLevel: 'moderate'`, `validationAction: 'error'`).

```typescript
export interface IChatAssistantSourceReference {
  refId: string;                    // ^M[1-9][0-9]{0,2}$
  messageId: Types.ObjectId;
  senderName: string;               // 1..120
  createdAt: Date;
  sourceEditedAt: Date | null;
  sourceVersion: number;            // int >= 0 — đối chiếu sống khi đọc (không lưu status tĩnh trong DB)
  quoteSnippet: string;             // 0..200 (trả '' khi nguồn bị DELETED lúc đọc)
}

export interface IChatConversationMessage {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  conversationId: Types.ObjectId;
  senderId: string;                 // 'assistant:continuum_ai' khi authorType === 'ASSISTANT'
  senderName: string;               // 'Continuum AI' khi authorType === 'ASSISTANT'
  senderAvatarUrl: string | null;
  clientMessageId: string;          // 'assistant:<triggerMessageId>' cho tin AI
  content: string;                  // maxlength 8000
  mentionUserIds: string[];
  links: string[];
  isPinned: boolean;
  forwardedFrom?: { senderName: string };
  forwardSourceId?: Types.ObjectId;
  forwardSourceConversationId?: Types.ObjectId;
  editedAt: Date | null;
  deletedAt: Date | null;
  reactions: Array<{ emoji: '👍' | '❤️' | '😂' | '😮' | '😢' | '🙏'; userIds: string[] }>;
  replyToMessageId: Types.ObjectId | null;
  attachments: Array<{
    id: string;
    name: string;
    contentType: string;
    size: number;
    kind: 'IMAGE' | 'DOCUMENT';
    provider: 'S3' | 'R2';
    objectKey: string;
  }>;

  // Trường additive phục vụ @continuumAI (100% tương thích tin cũ)
  contentVersion?: number;          // int >= 0 (logical default 0); $inc: 1 khi sửa hoặc xóa thật lần đầu
  authorType?: 'USER' | 'ASSISTANT';
  assistantMention?: {              // chỉ trên tin USER gọi @continuumAI
    handle: 'continuumAI';
    query: string;                  // 1..2000
    timezone: string;               // 1..64 IANA
  };
  triggerMessageId?: Types.ObjectId; // bắt buộc trên ASSISTANT, cấm trên USER
  assistantStatus?: 'PENDING' | 'COMPLETED' | 'INSUFFICIENT_EVIDENCE' | 'CANCELLED' | 'FAILED'; // v1 posted dùng COMPLETED | INSUFFICIENT_EVIDENCE
  assistantFailureCode?: 'SOURCE_CHANGED' | 'TRIGGER_DELETED' | 'ACCESS_REVOKED' | 'SERVICE_UNAVAILABLE' | 'TIMEOUT' | 'INVALID_MODEL_OUTPUT' | null;
  assistantMeta?: {
    handle: 'continuumAI';
    queryMode: 'TIME_WINDOW' | 'KEYWORD' | 'HYBRID';
    partialCoverage: boolean;
    coverageNote: string | null;    // <= 500
    model: string | null;           // <= 120
    promptTokens?: number | null;
    completionTokens?: number | null;
  };
  sourceReferences?: IChatAssistantSourceReference[]; // bắt buộc trên ASSISTANT (0..20), cấm trên USER

  createdAt: Date;
  updatedAt: Date;
}
```
* **Ràng buộc `$jsonSchema` (`moderate`, `oneOf`):**
  1. **Nhánh Human/Legacy:** `authorType` vắng mặt hoặc `'USER'`; `triggerMessageId` vắng mặt hoặc `null`; `senderId !== 'assistant:continuum_ai'`; vắng mặt `sourceReferences`, `assistantStatus`, `assistantMeta`, `assistantFailureCode`.
  2. **Nhánh Assistant:** `authorType === 'ASSISTANT'`, `senderId === 'assistant:continuum_ai'`, bắt buộc `triggerMessageId` (`objectId`), `assistantStatus` và mảng `sourceReferences` (`<= 20` phần tử); `assistantMention` vắng mặt hoặc `null`.

### 4.4. `chat_assistant_jobs` (Hàng đợi Outbox & Lease bền vững cho `@continuumAI`)

Áp dụng `$jsonSchema` mức **`validationLevel: 'strict'`**, `validationAction: 'error'`. Không lưu lịch sử chat hay trích đoạn ngữ cảnh trong document job; `failureReason` và `metrics` chỉ chứa mã/chỉ số vận hành an toàn.

```typescript
export interface IChatAssistantJob {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  conversationId: Types.ObjectId;
  triggerMessageId: Types.ObjectId; // unique — chống tạo trùng job
  requesterUserId: string;          // ^[a-fA-F0-9]{24}$
  requesterDisplayName: string;     // 1..120
  handle: 'continuumAI';
  query: string;                    // 1..2000
  timezone: string;                 // 1..64 IANA (default 'Asia/Ho_Chi_Minh')
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'INSUFFICIENT_EVIDENCE' | 'CANCELLED' | 'FAILED';
  failureCode: 'SOURCE_CHANGED' | 'TRIGGER_DELETED' | 'ACCESS_REVOKED' | 'SERVICE_UNAVAILABLE' | 'TIMEOUT' | 'INVALID_MODEL_OUTPUT' | null;
  failureReason: string | null;     // <= 300, cấm nội dung tin nhắn hoặc secret
  attempts: number;                 // int >= 0 (default 0)
  maxAttempts: number;              // int 1..5 (default 3)
  nextAttemptAt: Date;
  lockedBy: string | null;          // <= 160 (<host>:<pid>:<uuid>)
  lockedUntil: Date | null;         // lease mặc định 60s, gia hạn mỗi 15s
  responseMessageId: Types.ObjectId | null;
  metrics: {
    queryMode: 'TIME_WINDOW' | 'KEYWORD' | 'HYBRID' | null;
    retrievalPath: string | null;   // <= 64 (VD: ATLAS_SEARCH, ATLAS_SEARCH_THEN_MONGO_TEXT, ...)
    candidateCount: number | null;
    sentSnippetCount: number | null;
    citedCount: number | null;
    partialCoverage: boolean | null;
    retrievalLatencyMs: number | null;
    sagLatencyMs: number | null;
    totalLatencyMs: number | null;
  } | null;
  completedAt: Date | null;
  createdAt: Date;
  updatedAt: Date;
}
```

### 4.5. Các collection phụ trợ Human Chat khác trong `continuum_chat`

- `chat_uploads`: metadata tải tệp S3/R2 (`uploadId` unique, `expiresAt` TTL index `expireAfterSeconds: 0`).
- `chat_notifications`: thông báo tin mới (gồm tin AI đã đăng với `senderName: 'Continuum AI'` cho thành viên có `notificationMode === 'ALL'`; unique `{ organizationId: 1, userId: 1, messageId: 1 }`).
- `chat_blocks`: chặn trực tiếp 1–1 (`{ organizationId: 1, userId: 1, targetId: 1 }` unique + `{ organizationId: 1, targetId: 1, userId: 1 }`).
- `chat_reports`: báo cáo vi phạm (`{ organizationId: 1, status: 1, createdAt: -1, _id: -1 }`).

### 4.6. 6 Index Additive mới & Migration `20261128-chat-dm-assistant-schema`

| Collection | Tên Index | Key | Options | Mục đích |
| --- | --- | --- | --- | --- |
| `chat_conversation_messages` | `chat_messages_assistant_trigger_unique` | `{ conversationId: 1, triggerMessageId: 1 }` | `unique: true`, `partialFilterExpression: { authorType: 'ASSISTANT', triggerMessageId: { $type: 'objectId' } }` | Ràng buộc cứng tối đa 1 tin AI cho mỗi `triggerMessageId` (`0 B` trên tin người dùng cũ). |
| `chat_conversation_messages` | `chat_messages_assistant_source_refs_idx` | `{ conversationId: 1, 'sourceReferences.messageId': 1 }` | `partialFilterExpression: { authorType: 'ASSISTANT' }` | Tra cứu nhanh các tin AI trích dẫn một nguồn cụ thể (`0 B` trên tin người dùng cũ). |
| `chat_assistant_jobs` | `chat_assistant_jobs_trigger_unique` | `{ triggerMessageId: 1 }` | `unique: true` | Chống tạo trùng job khi retry/replay `clientMessageId`. |
| `chat_assistant_jobs` | `chat_assistant_jobs_claim_idx` | `{ status: 1, nextAttemptAt: 1, lockedUntil: 1, createdAt: 1, _id: 1 }` | — | Claim FIFO & thu hồi job hết hạn lease. |
| `chat_assistant_jobs` | `chat_assistant_jobs_conv_trigger_idx` | `{ organizationId: 1, conversationId: 1, triggerMessageId: 1 }` | — | Hydrate `assistantState` theo lô trong `mapMessages`. |
| `chat_assistant_jobs` | `chat_assistant_jobs_conv_status_created_idx` | `{ organizationId: 1, conversationId: 1, status: 1, createdAt: -1 }` | — | Thống kê/giám sát job theo hội thoại. |

- **Index hiện hữu được bảo toàn tuyệt đối:** `{ conversationId: 1, createdAt: -1, _id: -1 }`, `{ conversationId: 1, content: 'text' }` (`chat_message_text_search` / `conversationId_1_content_text` trên Atlas dev), `{ conversationId: 1, senderId: 1, clientMessageId: 1 }` (unique), `chat_messages_pinned_partial`, `chat_messages_attachments_kind_partial` và Atlas Search `chat_search_v1`.
- **Migration (`DATN_BE/scripts/migrations/20261128-chat-dm-assistant-schema.{mjs,plan.mjs,plan.test.mjs,mongodb.test.mjs,README.md}`):**
  - Chỉ bổ sung (`rewriteDocuments: false`), chạy mặc định ở chế độ dry-run xuất JSON kèm `reportSha256`; `--apply` yêu cầu `--expected-report-sha256` (thêm `--allow-shared-database` + `CHAT_MIGRATION_CONFIRM_DATABASE=continuum_chat` cho Atlas/shared) và idempotent khi chạy lặp.
  - **Rollback 2 tầng:** (1) Tức thời không chạm DB bằng `CHAT_DM_ASSISTANT_ENABLED=false` và `CHAT_DM_ASSISTANT_WORKER_ENABLED=false`; (2) Rollback schema/index qua `--rollback-plan` → `--rollback` (từ chối nếu còn job `PENDING`/`PROCESSING`, chỉ gỡ validator do migration quản lý và drop đúng 6 index additive mới, bảo toàn toàn bộ dữ liệu và index human chat).
