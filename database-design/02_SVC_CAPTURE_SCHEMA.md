# Continuum AI — Schema Dịch Vụ Ghi Nhận Công Việc
## (Work Capture & Notes Schema - svc_capture)

> **Database:** `continuum_capture` (MongoDB 7.0)  
> **Service sở hữu độc quyền:** `svc_capture`  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ (Bounded Context)

`svc_capture` giải quyết bài toán cốt lõi: **Thu thập tri thức ngầm (Tacit Knowledge) của kỹ sư ngay khi họ đang viết code và sửa lỗi.**

1. **Cấu trúc 3 thành phần bắt buộc (What - How - Why):**
   - `whatDone`: Công việc cụ thể đã làm.
   - `howSolved`: Chi tiết kỹ thuật, thuật toán, thư viện được sử dụng để giải quyết.
   - `whyThisWay`: Lý do chọn giải pháp này (So sánh giải pháp khác, đánh đổi kỹ thuật - Trade-offs).
2. **Quy tắc vàng Author-Confirmed:**
   - Mọi ghi chú tự gõ hoặc do AI gợi ý từ Jira/Git đều ở trạng thái `DRAFT`.
   - **Chỉ khi chính tác giả bấm nút xác nhận** (`authorConfirmedAt != null`), ghi chú mới chuyển sang `CONFIRMED` và đủ điều kiện để đưa vào Hộp thư kiểm chứng tri thức.
3. **Định nghĩa Yêu cầu Tri thức (`knowledge_requirements`):** Đặt ra các tiêu chuẩn tài liệu tối thiểu cho từng module phần mềm.

---

## 2. Chi Tiết Schemas Mongoose (Database: `continuum_capture`)

### 2.1. `work_notes` (Ghi chú công việc chính)
```typescript
export interface IWorkNote {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  teamId?: Types.ObjectId;
  authorUserId: Types.ObjectId;      // Logical Ref sang svc_iam.users._id
  
  // Liên kết ngữ cảnh công việc
  jiraIssueId?: string;             // Logical Ref ID từ svc_jira (dạng string/ObjectId)
  jiraIssueKey?: string;            // Khóa hiển thị (VD: "CONT-142")
  gitCommitHash?: string;           // Mã băm Git commit liên quan
  
  title: string;
  whatDone: string;
  howSolved: string;
  whyThisWay: string;
  
  // Kiểm soát trạng thái xác nhận
  status: 'DRAFT' | 'CONFIRMED' | 'ARCHIVED';
  authorConfirmedAt?: Date;         // Điểm chặn bắt buộc
  
  tags: string[];                   // ["cache", "redis", "concurrency"]
  timeSpentMinutes?: number;
  
  // Liên kết vòng đời
  promotedToProposalId?: string;    // Logical Ref sang svc_lifecycle.knowledge_proposals
  
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, projectId, status, createdAt)`: `{ index: true }`
  - `(authorUserId, status, createdAt)`: `{ index: true }`
  - `(projectId, jiraIssueKey)`: `{ index: true }`

---

### 2.2. `work_note_versions` (Lịch sử chỉnh sửa ghi chú)
Lưu trữ ảnh chụp mỗi lần chỉnh sửa trước và sau khi xác nhận.

```typescript
export interface IWorkNoteVersion {
  _id: Types.ObjectId;
  workNoteId: Types.ObjectId;        // Ref sang work_notes._id
  versionNumber: number;
  title: string;
  whatDone: string;
  howSolved: string;
  whyThisWay: string;
  editedByUserId: Types.ObjectId;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(workNoteId, versionNumber)`: `{ unique: true }`

---

### 2.3. `capture_drafts` (Bản thảo tự động lưu - Autosave Buffer)
Tránh mất dữ liệu khi lập trình viên đang gõ dở trên giao diện web.

```typescript
export interface ICaptureDraft {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  userId: Types.ObjectId;
  contextKey: string;                // VD: "jira_issue_CONT-142" hoặc "scratchpad"
  draftContent: {
    title?: string;
    whatDone?: string;
    howSolved?: string;
    whyThisWay?: string;
    tags?: string[];
  };
  lastSavedAt: Date;
}
```
* **Chỉ mục & TTL:**
  - `(userId, contextKey)`: `{ unique: true }`
  - `lastSavedAt`: `{ expireAfterSeconds: 604800 }` (Tự dọn sau 7 ngày nếu không dùng)

---

### 2.4. `work_note_templates` (Mẫu ghi chú chuẩn hóa theo chuyên môn)
Giúp kỹ sư Frontend, Backend, DevOps có khung sườn gõ chuẩn ngay từ đầu.

```typescript
export interface IWorkNoteTemplate {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId?: Types.ObjectId;
  name: string;                      // VD: "Mẫu ghi chú xử lý Bug Production"
  roleScope: 'FRONTEND' | 'BACKEND' | 'DEVOPS' | 'QA' | 'GENERAL';
  defaultWhatDonePrompt: string;
  defaultHowSolvedPrompt: string;
  defaultWhyThisWayPrompt: string;
  suggestedTags: string[];
  isDefault: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, roleScope)`: `{ index: true }`

---

### 2.5. `knowledge_requirements` (Đặc tả yêu cầu tri thức bắt buộc)
Danh mục các chủ đề kỹ thuật mà một nhóm hoặc module bắt buộc phải có tài liệu.

```typescript
export interface IKnowledgeRequirement {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  teamId?: Types.ObjectId;
  responsibilityCode?: string;       // Logical Ref sang svc_handover.responsibilities
  
  title: string;                     // VD: "Cơ chế xoay vòng Refresh Token an toàn"
  category: 'ARCHITECTURE' | 'DEPLOYMENT' | 'RUNBOOK' | 'SECURITY' | 'API_CONTRACT';
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  status: 'UNFULFILLED' | 'PARTIALLY_FULFILLED' | 'FULFILLED';
  
  fulfilledByKnowledgeObjectId?: string; // Logical Ref sang svc_lifecycle
  
  createdBy: Types.ObjectId;
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, projectId, status)`: `{ index: true }`
  - `(projectId, responsibilityCode)`: `{ index: true }`

---

## 3. Giao Tiếp Sự Kiện (Domain Events)

- **Sự kiện xuất bản (Published Events):**
  - `capture.note.confirmed`: Phát ra khi tác giả bấm xác nhận ghi chú. Payload chứa toàn văn What/How/Why. Consumer là `svc_lifecycle` để đưa vào Hộp thư kiểm chứng.
  - `capture.requirement.created`: Phát ra khi có yêu cầu tri thức mới được tạo.
- **Sự kiện lắng nghe (Consumed Events):**
  - `jira.issue.synced`: Nhận thông tin task Jira vừa đồng bộ để tự động gợi ý ngữ cảnh cho lập trình viên.
