# Continuum AI — Schema Dịch Vụ Vòng Đời & Kiểm Chứng Tri Thức
## (Knowledge Lifecycle, Verification & Evidence Schema - svc_lifecycle)

> **Database:** `continuum_lifecycle` (MongoDB 7.0)  
> **Service sở hữu độc quyền:** `svc_lifecycle`  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ (Bounded Context)

`svc_lifecycle` là **"Trái tim nghiệp vụ"** của Continuum AI, chịu trách nhiệm quản lý vòng đời tri thức từ khi còn là đề xuất nháp đến khi trở thành chân lý được kiểm chứng:
1. **Đối tượng Tri thức Có Định Danh Ổn Định (`knowledge_objects`):** ID không đổi, quản lý trạng thái hiện tại (`DRAFT`, `IN_REVIEW`, `VERIFIED`, `DEPRECATED`, `OBSOLETE`).
2. **Nội dung Công bố Bất Biến (`knowledge_versions`):** Mọi sự thay đổi đều tạo ra một version mới tuần tự (`v1 → v2`), tuyệt đối không UPDATE đè lên version cũ đã kiểm chứng.
3. **Truy nguyên Bằng chứng Tuyệt đối (`knowledge_evidence`):** Mỗi khẳng định tri thức đều liên kết trực tiếp với đoạn trích từ file PDF tài liệu, ghi chú tác giả hoặc issue Jira.
4. **Hộp thư Kiểm chứng (Verification Inbox):** Nơi Team Leader / SME duyệt đề xuất tri thức bằng giao dịch ACID đa tài liệu.
5. **Giám sát Khoảng trống & Mâu thuẫn:** Tự động ghi nhận `knowledge_gaps` và `knowledge_conflicts`.

---

## 2. Chi Tiết Schemas Mongoose (Database: `continuum_lifecycle`)

### 2.1. `knowledge_objects` (Đối tượng tri thức gốc)
```typescript
export interface IKnowledgeObject {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  teamId?: Types.ObjectId;
  
  title: string;
  slug: string;                      // URL slug (VD: "redis-webhook-idempotency")
  type: 'ARCHITECTURE_DECISION' | 'RUNBOOK' | 'BUSINESS_RULE' | 'API_CONTRACT' | 'TROUBLESHOOTING';
  
  status: 'DRAFT' | 'IN_REVIEW' | 'VERIFIED' | 'DEPRECATED' | 'OBSOLETE';
  
  currentVersionId?: Types.ObjectId; // Ref sang knowledge_versions._id
  currentVersionNumber: number;      // Phiên bản hiện tại (VD: 1, 2)
  
  ownerUserId: string;               // Logical Ref sang svc_iam.users._id
  smeUserId?: string;                // Logical Ref chuyên gia thẩm định
  
  tags: string[];
  confidentiality: 'INTERNAL' | 'RESTRICTED' | 'PUBLIC';
  
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, projectId, slug)`: `{ unique: true }`
  - `(organizationId, projectId, status, updatedAt)`: `{ index: true }`
  - `(organizationId, projectId, ownerUserId)`: `{ index: true }`
  - `(organizationId, projectId, tags)`: `{ index: true }`

---

### 2.2. `knowledge_proposals` (Đề xuất tri thức trong Verification Inbox)
```typescript
export interface IKnowledgeProposal {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  teamId?: Types.ObjectId;
  
  proposalType: 'CREATE_NEW' | 'UPDATE_EXISTING';
  targetKnowledgeObjectId?: Types.ObjectId;
  
  title: string;
  proposedContentMarkdown: string;
  category: 'ARCHITECTURE_DECISION' | 'RUNBOOK' | 'BUSINESS_RULE' | 'API_CONTRACT' | 'TROUBLESHOOTING';
  tags: string[];
  
  // Nguồn gốc đề xuất (Provenance)
  sourceType: 'WORK_NOTE' | 'JIRA_ISSUE' | 'DOCUMENT' | 'AUDIO_INTERVIEW' | 'HUMAN_DIRECT';
  sourceRefId: string;               // ID từ service nguồn (workNoteId, documentVersionId...)
  suggestedByUserId?: string;        // Null nếu do Trợ lý AI tự động trích xuất
  
  // Trạng thái thẩm định
  reviewStatus: 'PENDING' | 'APPROVED' | 'REJECTED' | 'REQUEST_CHANGES';
  reviewerUserId?: string;           // Leader hoặc SME duyệt
  reviewNotes?: string;
  reviewedAt?: Date;
  
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, projectId, reviewStatus, createdAt)`: `{ index: true }`
  - `(sourceType, sourceRefId)`: `{ index: true }`

---

### 2.3. `knowledge_versions` (Phiên bản tri thức bất biến - Immutable Snapshots)
```typescript
export interface IKnowledgeVersion {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  knowledgeObjectId: Types.ObjectId; // Ref sang knowledge_objects._id
  
  versionNumber: number;             // 1, 2, 3...
  title: string;
  contentMarkdown: string;           // Toàn văn nội dung tri thức đã duyệt
  summary?: string;
  
  supersedesVersionId?: Types.ObjectId; // Phiên bản trước bị thay thế
  changeLog?: string;
  
  evidenceIds: Types.ObjectId[];     // Ref sang knowledge_evidence._id
  
  publishedBy: string;               // User ID của Leader/SME duyệt ban hành
  publishedAt: Date;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(knowledgeObjectId, versionNumber)`: `{ unique: true }`
  - `(organizationId, projectId, publishedAt)`: `{ index: true }`

---

### 2.4. `knowledge_evidence` (Bằng chứng & Đoạn trích dẫn kiểm chứng)
```typescript
export interface IKnowledgeEvidence {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  knowledgeObjectId: Types.ObjectId;
  knowledgeVersionId?: Types.ObjectId;
  
  evidenceType: 'DOCUMENT_VERSION' | 'WORK_NOTE' | 'JIRA_ISSUE' | 'AUDIO_TRANSCRIPT' | 'GIT_COMMIT';
  sourceRefId: string;               // ID liên kết logic
  sourceUri?: string;                // URL hoặc R2 S3 Key
  
  excerpt: string;                   // Đoạn trích dẫn trực tiếp làm chứng cứ
  confidenceScore?: number;          // 0.00 -> 1.00
  
  verifiedByUserId: string;
  verifiedAt: Date;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(knowledgeObjectId, knowledgeVersionId)`: `{ index: true }`
  - `(evidenceType, sourceRefId)`: `{ index: true }`

---

### 2.5. `knowledge_verifications` (Nhật ký quyết định thẩm định - Audit Trail)
```typescript
export interface IKnowledgeVerification {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  knowledgeObjectId: Types.ObjectId;
  proposalId?: Types.ObjectId;
  
  decision: 'VERIFIED' | 'REJECTED' | 'REQUEST_CHANGE';
  decisionByUserId: string;
  decisionRole: 'SME' | 'TEAM_LEADER' | 'ADMIN';
  comments: string;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(knowledgeObjectId, createdAt)`: `{ index: true }`
  - `(decisionByUserId, createdAt)`: `{ index: true }`

---

### 2.6. `knowledge_gaps` & `knowledge_conflicts` (Khoảng trống & Mâu thuẫn)
```typescript
export interface IKnowledgeGap {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  teamId?: Types.ObjectId;
  
  responsibilityCode?: string;       // Logical Ref sang svc_handover
  title: string;
  description: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  status: 'OPEN' | 'IN_PROGRESS' | 'RESOLVED' | 'IGNORED';
  
  assignedToUserId?: string;
  resolvedByKnowledgeObjectId?: Types.ObjectId;
  resolvedAt?: Date;
  
  createdAt: Date;
  updatedAt: Date;
}

export interface IKnowledgeConflict {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  
  knowledgeObjectIdA: Types.ObjectId;
  knowledgeObjectIdB: Types.ObjectId;
  description: string;
  status: 'UNRESOLVED' | 'RESOLVED';
  
  resolvedByUserId?: string;
  resolutionSummary?: string;
  resolvedAt?: Date;
  
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `knowledge_gaps`: `(organizationId, projectId, status, severity)`: `{ index: true }`
  - `knowledge_conflicts`: `(organizationId, projectId, status)`: `{ index: true }`

---

### 2.7. `knowledge_relations` (Đồ thị quan hệ nghiệp vụ giữa các tri thức)
```typescript
export interface IKnowledgeRelation {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  
  sourceKnowledgeObjectId: Types.ObjectId;
  targetKnowledgeObjectId: Types.ObjectId;
  relationType: 'DEPENDS_ON' | 'EXTENDS' | 'SUPERSEDES' | 'RELATED_TO';
  
  createdBy: string;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(sourceKnowledgeObjectId, targetKnowledgeObjectId, relationType)`: `{ unique: true }`

---

## 3. Giao Dịch Đa Tài Liệu ACID Khi Phê Duyệt Tri Thức

```typescript
// Giao dịch ACID chuẩn trong Mongoose Session của svc_lifecycle
const session = await mongoose.startSession();
session.startTransaction();
try {
  // 1. Cập nhật Proposal sang APPROVED
  await KnowledgeProposal.updateOne(
    { _id: proposalId, reviewStatus: 'PENDING' },
    { $set: { reviewStatus: 'APPROVED', reviewerUserId, reviewedAt: new Date() } },
    { session }
  );

  // 2. Tạo bản ghi bất biến KnowledgeVersion
  const [newVersion] = await KnowledgeVersion.create([{
    organizationId,
    projectId,
    knowledgeObjectId,
    versionNumber: nextVersionNumber,
    title: proposal.title,
    contentMarkdown: proposal.proposedContentMarkdown,
    supersedesVersionId: currentVersionId,
    evidenceIds,
    publishedBy: reviewerUserId,
    publishedAt: new Date()
  }], { session });

  // 3. Cập nhật KnowledgeObject trỏ tới Version mới và đặt VERIFIED
  await KnowledgeObject.updateOne(
    { _id: knowledgeObjectId },
    { $set: { currentVersionId: newVersion._id, currentVersionNumber: nextVersionNumber, status: 'VERIFIED' } },
    { session }
  );

  // 4. Ghi nhận quyết định thẩm định
  await KnowledgeVerification.create([{
    organizationId, projectId, knowledgeObjectId, proposalId,
    decision: 'VERIFIED', decisionByUserId: reviewerUserId, decisionRole: 'SME',
    comments: 'Đã thẩm định chuẩn xác.'
  }], { session });

  await session.commitTransaction();

  // 5. Bắn Domain Event để SAG Engine lập chỉ mục Vector
  await eventBus.publish('lifecycle.knowledge.published', {
    knowledgeObjectId,
    versionId: newVersion._id,
    organizationId,
    projectId,
    contentMarkdown: newVersion.contentMarkdown
  });
} catch (error) {
  await session.abortTransaction();
  throw error;
} finally {
  session.endSession();
}
```
