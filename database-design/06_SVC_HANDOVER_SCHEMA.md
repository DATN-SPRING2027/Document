# Continuum AI — Schema Dịch Vụ Chuyển Giao & Kế Thừa Tri Thức
## (Handover & Knowledge Continuity Schema - svc_handover)

> **Database:** `continuum_handover` (MongoDB 7.0)  
> **Service sở hữu độc quyền:** `svc_handover`  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ (Bounded Context)

`svc_handover` xử lý bài toán sinh tử của doanh nghiệp: **Ngăn chặn việc mất mát tri thức cốt lõi khi nhân sự chủ chốt nghỉ việc.**

1. **Thực thể Trách nhiệm Độc lập (`responsibilities`):**
   - Trách nhiệm phụ trách một module/microservice/hệ thống là một thực thể độc lập tồn tại theo thời gian, không bao giờ gắn chết vào ID của một nhân sự cố định.
   - Bảng `responsibility_assignments` theo dõi lịch sử *"Ai nắm giữ module nào trong khoảng thời gian nào (`effectiveFrom` - `effectiveTo`)"*.
2. **Chiến dịch Chuyển giao Đa giai đoạn (`handovers` & `handover_items`):**
   - Không chuyển giao theo kiểu "bàn giao miệng". Mọi trách nhiệm đều được bẻ nhỏ thành danh sách công việc (`handover_items`).
   - **Xác nhận từ người kế nhiệm (`VERIFIED_BY_SUCCESSOR`):** Mục bàn giao chỉ được tính là hoàn tất khi người tiếp quản xác nhận đã nắm vững và chạy thử thành công.
3. **Phỏng vấn Bóc tách Tri thức Âm thanh (`interviews` & `interview_sessions`):**
   - Thu âm phỏng vấn bóc tách kinh nghiệm thực chiến của nhân sự sắp nghỉ việc, tải lên Cloudflare R2 và kích hoạt STT (Whisper) để chuyển hóa thành đề xuất tri thức.
4. **Lộ trình Kế thừa Cá nhân hóa (`learning_paths`):** Tạo ra checklist và lộ trình học tài liệu có hướng dẫn cho nhân sự mới.

---

## 2. Chi Tiết Schemas Mongoose (Database: `continuum_handover`)

### 2.1. `responsibilities` (Thực thể Trách nhiệm hệ thống)
```typescript
export interface IResponsibility {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  teamId?: Types.ObjectId;
  
  name: string;                      // VD: "Hệ thống Cổng Thanh Toán & Đối Soát"
  code: string;                      // VD: "RESP_PAYMENT_GATEWAY"
  description: string;
  criticality: 'LOW' | 'MEDIUM' | 'HIGH' | 'MISSION_CRITICAL';
  
  requiredDocumentationStatus: 'SATISFIED' | 'DEFICIENT';
  currentPrimaryOwnerId?: string;    // Logical Ref sang svc_iam.users._id
  
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(projectId, code)`: `{ unique: true }`
  - `(organizationId, projectId, criticality)`: `{ index: true }`

---

### 2.2. `responsibility_assignments` (Lịch sử phân công theo thời gian)
```typescript
export interface IResponsibilityAssignment {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  responsibilityId: Types.ObjectId;  // Ref sang responsibilities._id
  userId: string;                    // Logical Ref sang svc_iam.users._id
  
  assignmentType: 'PRIMARY_OWNER' | 'BACKUP_OWNER' | 'INTERN_LEARNER';
  effectiveFrom: Date;
  effectiveTo?: Date;                // Null nếu đang đảm nhiệm
  
  assignedBy: string;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(responsibilityId, effectiveFrom, effectiveTo)`: `{ index: true }`
  - `(userId, effectiveTo)`: `{ index: true }`

---

### 2.3. `handovers` (Chiến dịch bàn giao khi nhân sự rời đi)
```typescript
export interface IHandover {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  
  departingUserId: string;           // Kỹ sư sắp rời dự án
  targetCompletionDate: Date;
  
  status: 'PLANNED' | 'IN_PROGRESS' | 'READY_FOR_VERIFICATION' | 'COMPLETED' | 'OVERDUE';
  completionPercent: number;         // 0 -> 100%
  assignedLeaderId: string;          // Team Leader giám sát
  
  completedAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, projectId, departingUserId, status)`: `{ index: true }`
  - `(status, targetCompletionDate)`: `{ index: true }`

---

### 2.4. `handover_items` (Hạng mục công việc bàn giao chi tiết)
```typescript
export interface IHandoverItem {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  handoverId: Types.ObjectId;        // Ref sang handovers._id
  
  responsibilityId?: Types.ObjectId;
  knowledgeObjectId?: string;        // Logical Ref sang svc_lifecycle
  
  title: string;
  description: string;
  itemType: 'DOCUMENT' | 'CREDENTIAL_TRANSFER' | 'RUNBOOK_DEMO' | 'CODE_WALKTHROUGH';
  
  successorUserId: string;           // Người kế nhiệm tiếp nhận
  
  status: 'PENDING' | 'IN_PROGRESS' | 'SUBMITTED' | 'VERIFIED_BY_SUCCESSOR' | 'REJECTED';
  successorVerifiedAt?: Date;        // Xác nhận "Đã nắm vững"
  successorNotes?: string;
  
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(handoverId, status)`: `{ index: true }`
  - `(successorUserId, status)`: `{ index: true }`

---

### 2.5. `interviews` & `interview_sessions` (Phỏng vấn bóc tách tri thức âm thanh)
```typescript
export interface IInterview {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  handoverId?: Types.ObjectId;
  
  intervieweeUserId: string;         // Người được phỏng vấn
  interviewerUserId: string;         // Leader hoặc Trợ lý AI điều phối
  topic: string;
  
  status: 'SCHEDULED' | 'RECORDED' | 'TRANSCRIBED' | 'EXTRACTED_TO_PROPOSALS';
  createdAt: Date;
  updatedAt: Date;
}

export interface IInterviewSession {
  _id: Types.ObjectId;
  interviewId: Types.ObjectId;       // Ref sang interviews._id
  
  audioR2ObjectKey: string;          // File lưu trong Cloudflare R2
  audioDurationSeconds: number;
  mimeType: string;
  
  transcriptionStatus: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  transcriptText?: string;           // Văn bản bóc băng
  extractedKeyPoints: string[];      // Các ý quan trọng bóc tách được
  
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, projectId, status)`: `{ index: true }`
  - `(interviewId)`: `{ index: true }`

---

### 2.6. `learning_paths` & `follow_up_tasks` (Lộ trình học & Nhiệm vụ hậu bàn giao)
```typescript
export interface ILearningPathStep {
  stepOrder: number;
  knowledgeObjectId: string;
  estimatedMinutes: number;
  isMandatory: boolean;
  isCompleted: boolean;
  completedAt?: Date;
}

export interface ILearningPath {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  learnerUserId: string;
  handoverId?: Types.ObjectId;
  
  title: string;
  steps: ILearningPathStep[];
  status: 'ACTIVE' | 'COMPLETED';
  progressPercent: number;
  
  createdAt: Date;
  updatedAt: Date;
}

export interface IFollowUpTask {
  _id: Types.ObjectId;
  handoverId: Types.ObjectId;
  successorUserId: string;
  title: string;
  checkInMilestoneDays: 30 | 60 | 90; // Mốc kiểm tra sau 30, 60, 90 ngày
  dueDate: Date;
  isAcknowledged: boolean;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `learning_paths`: `(organizationId, projectId, learnerUserId, status)`: `{ index: true }`
  - `follow_up_tasks`: `(successorUserId, dueDate, isAcknowledged)`: `{ index: true }`

---

## 3. Giao Tiếp Sự Kiện (Domain Events)

- **Sự kiện xuất bản:**
  - `handover.campaign.started`: Thông báo cho Leader và người kế nhiệm bắt đầu chiến dịch.
  - `handover.item.verified`: Người kế nhiệm ký nhận một mục bàn giao.
  - `handover.interview.transcribed`: Khi hoàn tất bóc băng âm thanh, kích hoạt AI trích xuất đề xuất tri thức.
