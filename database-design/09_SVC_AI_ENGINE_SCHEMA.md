# Continuum AI — Schema & Hợp Đồng Dữ Liệu Dịch Vụ Trí Tuệ Nhân Tạo
## (AI Engine, Model Routing & SAG Integration Schema - svc_ai_engine)

> **Database:** `continuum_ai_adapter` (MongoDB 7.0)  
> **Service sở hữu độc quyền:** `svc_ai_engine`  
> **Tầng lưu trữ dữ liệu sau extract (SAG Storage):** Xem chi tiết tại [11_SAG_STORAGE_SCHEMA.md](11_SAG_STORAGE_SCHEMA.md)  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ & Phân Định Trách Nhiệm (Bounded Context)

`svc_ai_engine` đóng vai trò là **Bộ điều phối Trí tuệ Nhân tạo (AI Orchestrator)** kiêm **Adapter kết nối subsystem lõi `zleap-sag`**:
1. **Phân định Rõ Ràng với Zleap-AI/SAG:**
   - Dữ liệu tri thức bóc tách (Chunks, Events, Entities, Vectors) được lưu trữ chuyên dụng trong `continuum_sag_storage` (Xem chi tiết tại [11_SAG_STORAGE_SCHEMA.md](11_SAG_STORAGE_SCHEMA.md)).
   - MongoDB của Continuum AI không lưu đè các quan hệ đồ thị hay vector nhị phân lớn này.
2. **Nhiệm vụ của `continuum_ai_adapter` trong MongoDB:**
   - Quản lý cấu hình Model LLM & Routing linh hoạt (`ai_model_configs`): Gemini, Claude, OpenAI, Local Ollama.
   - Quản lý các mẫu System Prompt có phiên bản (`ai_prompt_templates`) phục vụ trích xuất tri thức, bóc tách audio, tóm tắt.
   - Ghi nhật ký tiêu thụ Token và chi phí ước tính (`ai_task_executions`).
3. **Chuẩn hóa Hợp đồng API với SAG Engine (`zleap-sag` REST / Python Call):**
   - Định nghĩa chính xác cấu trúc DTO đầu vào/đầu ra khi gọi sang SAG.

---

## 2. Chi Tiết Schemas Mongoose (Database: `continuum_ai_adapter`)

### 2.1. `ai_model_configs` (Cấu hình Model & Định tuyến LLM)
Cho phép chuyển đổi linh hoạt nhà cung cấp LLM mà không cần redeploy code.

```typescript
export interface IAiModelConfig {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId?: Types.ObjectId;
  
  taskType: 'CHAT_REASONING' | 'PROPOSAL_GENERATION' | 'AUDIO_TRANSCRIPTION' | 'EMBEDDING';
  provider: 'GOOGLE_VERTEX' | 'OPENAI' | 'ANTHROPIC' | 'LOCAL_WHISPER';
  modelId: string;                   // VD: "gemini-1.5-flash", "gpt-4o-mini", "whisper-large-v3"
  
  parameters: {
    temperature: number;             // VD: 0.1 cho trích xuất, 0.7 cho chat
    maxTokens: number;
    topP?: number;
  };
  
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, taskType, isActive)`: `{ index: true }`

---

### 2.2. `ai_prompt_templates` (Kho System Prompt có phiên bản)
```typescript
export interface IAiPromptTemplate {
  _id: Types.ObjectId;
  promptCode: string;                // VD: "PROMPT_EXTRACT_KNOWLEDGE_FROM_NOTE"
  version: number;
  systemInstruction: string;         // System prompt quy định phong cách và định dạng JSON output
  userPromptTemplate: string;        // Mẫu input chứa placeholder {{whatDone}}, {{howSolved}}
  
  expectedOutputSchemaJson?: string; // JSON Schema dùng cho Structured Outputs
  isProductionReady: boolean;
  
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(promptCode, version)`: `{ unique: true }`

---

### 2.3. `ai_task_executions` (Nhật ký thực thi tác vụ AI & Chi phí Token)
```typescript
export interface IAiTaskExecution {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  
  taskType: 'PROPOSAL_GEN' | 'CHAT_INFERENCE' | 'AUDIO_STT';
  provider: string;
  modelUsed: string;
  
  tokensPrompt: number;
  tokensCompletion: number;
  costUsdEstimated: number;          // Chi phí USD ước tính theo giá token
  latencyMs: number;
  
  status: 'SUCCESS' | 'RATE_LIMITED' | 'ERROR';
  errorMessage?: string;
  
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, createdAt)`: `{ index: true }`
  - `(status, createdAt)`: `{ index: true }`

---

## 3. Hợp Đồng Dữ Liệu Gọi Sang Engine Zleap-AI/SAG (Data Contracts)

Đây là các Interface chuẩn (DTO) khi `svc_ai_engine` gọi vào Python API của `zleap-sag`:

### 3.1. Hợp đồng Nạp và Đánh chỉ mục (`SagIngestRequestDTO`)
```typescript
export interface ISagIngestRequestDTO {
  documentId: string;                // Map với Continuum document_version._id
  projectId: string;
  organizationId: string;
  fileR2Path: string;                // Link tải tệp từ Cloudflare R2
  parserMode: 'FAST_MARKITDOWN' | 'DEEP_MINERU';
  metadata: {
    title: string;
    confidentiality: string;
    allowedRoles: string[];          // Phục vụ Pre-retrieval ACL
  };
}
```

### 3.2. Hợp đồng Tìm kiếm Ngữ nghĩa & Đồ thị (`SagSearchRequestDTO`)
```typescript
export interface ISagSearchRequestDTO {
  query: string;
  projectId: string;
  organizationId: string;
  userEffectiveRoles: string[];      // Tập quyền hiệu lực của người hỏi
  searchMode: 'FAST_VECTOR' | 'PRECISE_DYNAMIC_HYPEREDGES';
  topK: number;
}
```

### 3.3. Hợp đồng Bằng chứng Trả về (`SagEvidenceResponseDTO`)
```typescript
export interface ISagEvidenceCandidate {
  sagChunkId: string;                // Chunk ID nội bộ của SAG
  sagEventId: string;                // Event ID đại diện cho chuỗi sự kiện
  textContent: string;               // Đoạn trích bằng chứng
  similarityScore: number;           // Điểm vector tương đồng
  matchedEntities: string[];         // Các thực thể được nối động bởi SAG
}

export interface ISagSearchResponseDTO {
  candidates: ISagEvidenceCandidate[];
  highestScore: number;
  totalCandidates: number;
}
```

---

## 4. Tóm Lược Tầng Lưu Trữ Sau Extract Của SAG (Post-Extraction Storage)
 
- Chi tiết toàn bộ các bảng cơ sở dữ liệu quan hệ (`data_source`, `kb_document`, `source_chunk`, `entity_type`, `entity`, `source_event`, `event_entity`) và kho vector PostgreSQL 16 + pgvector được đặc tả đầy đủ tại:  
  👉 **[11_SAG_STORAGE_SCHEMA.md](11_SAG_STORAGE_SCHEMA.md)**.
- **Tính chất Stateless và Tái tạo được 100%:** Khi cần (ví dụ nâng cấp model embedding hoặc sự cố ổ đĩa), Continuum AI chỉ cần gửi lệnh re-ingest toàn bộ `document_versions` và `knowledge_versions` từ MongoDB + Cloudflare R2 vào SAG.
