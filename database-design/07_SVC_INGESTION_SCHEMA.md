# Continuum AI — Schema Dịch Vụ Nạp & Xử Lý Tài Liệu
## (Document Ingestion & SAG Bridge Schema - svc_ingestion)

> **Database:** `continuum_ingestion` (MongoDB 7.0)  
> **Service sở hữu độc quyền:** `svc_ingestion`  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ (Bounded Context)

`svc_ingestion` là cửa ngõ tiếp nhận, chuẩn hóa và điều phối nạp dữ liệu phi cấu trúc vào hệ thống:
1. **Quản lý Tệp Đám Mây (Cloudflare R2 Object Storage):**
   - Áp dụng cơ chế **Direct Presigned PUT URL**: Client tải trực tiếp tệp PDF/DOCX lên Cloudflare R2 bucket private, backend không tốn RAM đệm file nhị phân.
   - MongoDB chỉ lưu trữ siêu dữ liệu (Metadata, R2 Object Key, MIME type, dung lượng tệp).
2. **Khử Trùng Lặp Tệp Cấp Độ Dự Án (Deduplication via SHA-256):**
   - Tính toán mã băm `checksumSha256` của tệp. Nếu tệp giống hệt đã tồn tại trong dự án, hệ thống từ chối nạp trùng để tiết kiệm chi phí lưu trữ và chỉ mục.
3. **Điều phối Hàng Đợi OCR & Bóc Tách (Parser Coordination):**
   - Tạo tác vụ xử lý bất đồng bộ (`ingestion_jobs`) đẩy vào BullMQ để Router gọi MarkItDown hoặc MinerU tùy thuộc độ phức tạp của định dạng tệp.
4. **Cầu Nối Ánh Xạ SAG Engine (`sag_mappings`):**
   - Lưu trữ bản đồ liên kết 1-1 giữa ID phiên bản tài liệu của Continuum với Document ID và Chunk ID do thư viện `zleap-sag` sinh ra.

---

## 2. Chi Tiết Schemas Mongoose (Database: `continuum_ingestion`)

### 2.1. `documents` (Tệp tài liệu gốc)
```typescript
export interface IDocument {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  
  fileName: string;                  // Tên file gốc (VD: "Software_Architecture_Doc_v2.pdf")
  mimeType: string;                  // "application/pdf", "text/markdown", ...
  fileSizeBytes: number;
  
  // Khử trùng lặp tệp (Deduplication)
  checksumSha256: string;            // Băm SHA-256 nội dung file
  
  sourceType: 'LOCAL_UPLOAD' | 'GOOGLE_DRIVE' | 'CONFLUENCE' | 'GIT_REPO';
  r2ObjectKey: string;               // Đường dẫn trong Cloudflare R2
  
  uploadedBy: string;                // Logical Ref sang svc_iam.users._id
  currentVersionNumber: number;
  
  status: 'ACTIVE' | 'ARCHIVED';
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(projectId, checksumSha256)`: `{ unique: true }` — Ngăn trùng file cùng dự án
  - `(organizationId, projectId, status, createdAt)`: `{ index: true }`

---

### 2.2. `document_versions` (Phiên bản nội dung tệp & Kết quả Parser)
```typescript
export interface IDocumentVersion {
  _id: Types.ObjectId;
  documentId: Types.ObjectId;        // Ref sang documents._id
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  
  versionNumber: number;
  r2ObjectKey: string;
  
  // Tiến trình Parser / OCR
  parseStatus: 'QUEUED' | 'EXTRACTING' | 'EXTRACTED' | 'FAILED';
  parserUsed?: 'MARKITDOWN' | 'MINERU';
  pageCount?: number;
  extractedTextLength?: number;
  rawTextR2Key?: string;             // Lưu text bóc tách trên R2 nếu quá giới hạn 16MB MongoDB
  
  errorMessage?: string;
  parsedAt?: Date;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(documentId, versionNumber)`: `{ unique: true }`
  - `(organizationId, projectId, parseStatus)`: `{ index: true }`

---

### 2.3. `ingestion_jobs` (Theo dõi hàng đợi tác vụ bóc tách tài liệu)
```typescript
export interface IIngestionJob {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  documentId: Types.ObjectId;
  documentVersionId: Types.ObjectId;
  
  jobType: 'PARSE_DOCUMENT' | 'AUDIO_TRANSCRIPTION' | 'SAG_INDEXING';
  bullMqJobId: string;
  
  status: 'WAITING' | 'ACTIVE' | 'COMPLETED' | 'FAILED' | 'RETRYING';
  progressPercent: number;           // 0 -> 100%
  attemptsCount: number;
  maxRetries: number;
  
  startedAt?: Date;
  completedAt?: Date;
  errorMessage?: string;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, projectId, status)`: `{ index: true }`
  - `bullMqJobId`: `{ index: true }`

---

### 2.4. `sag_mappings` (Cầu nối ánh xạ Continuum ⟷ Zleap-AI/SAG)
Đây là bảng cốt lõi liên kết giữa Domain Data của Continuum AI và Engine SAG nội bộ (Xem chi tiết kiến trúc và bảng lưu trữ sau extract tại [11_SAG_STORAGE_SCHEMA.md](11_SAG_STORAGE_SCHEMA.md)).

```typescript
export interface ISagMapping {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  
  sourceType: 'KNOWLEDGE_VERSION' | 'DOCUMENT_VERSION' | 'WORK_NOTE';
  sourceRecordId: string;            // ID trong MongoDB của Continuum (dạng string/ObjectId)
  
  // Định danh nội bộ do zleap-sag sinh ra
  sagDocumentId: string;             // Document ID trong SAG
  sagChunkId: string;                // Chunk ID do SAG sinh ra
  sagEventId?: string;               // Event ID do SAG trích xuất
  
  chunkIndex: number;                // Thứ tự đoạn
  charStartOffset: number;
  charEndOffset: number;
  
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(sourceType, sourceRecordId, chunkIndex)`: `{ unique: true }`
  - `sagChunkId`: `{ unique: true }` — Phục vụ tra cứu siêu tốc khi SAG trả về citations

---

### 2.5. `file_upload_tickets` (Vé cấp quyền Presigned Upload tạm thời)
```typescript
export interface IFileUploadTicket {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  userId: string;
  fileName: string;
  fileSizeBytes: number;
  mimeType: string;
  checksumSha256: string;
  
  presignedPutUrl: string;           // URL upload trực tiếp lên Cloudflare R2
  r2ObjectKey: string;
  isUsed: boolean;
  expiresAt: Date;                   // Thường là 15 phút
  createdAt: Date;
}
```
* **Chỉ mục & TTL:**
  - `expiresAt`: `{ expireAfterSeconds: 0 }` (Tự xóa vé hết hạn)

---

## 3. Giao Tiếp Sự Kiện (Domain Events)

- **Sự kiện xuất bản:**
  - `ingestion.document.uploaded`: Kích hoạt BullMQ worker bóc tách tệp.
  - `ingestion.document.parsed`: Thông báo hoàn tất OCR, sẵn sàng đẩy sang SAG Engine.
  - `ingestion.sag.mapped`: Đã lưu thành công ánh xạ chunk ID với SAG.
