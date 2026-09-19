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
