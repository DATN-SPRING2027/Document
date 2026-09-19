# Continuum AI — Schema Dịch Vụ Tích Hợp Jira Cloud
## (Jira Connector Service Schema - svc_jira)

> **Database:** `continuum_jira` (MongoDB 7.0)  
> **Service sở hữu độc quyền:** `svc_jira`  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ & Cơ Chế Khử Trùng Lặp (Bounded Context)

`svc_jira` chịu trách nhiệm toàn bộ việc kết nối, đồng bộ dữ liệu và tiếp nhận Webhook từ hệ sinh thái Atlassian Jira Cloud:
1. **Quản lý Kết nối & Bảo mật Token:** Lưu trữ thông tin kết nối OAuth 2.0 3LO (3-Legged OAuth) hoặc API Token của Jira. Khóa bí mật và Access Token bắt buộc phải được mã hóa chuẩn **AES-256-GCM** trước khi lưu vào DB.
2. **Xử lý Webhook Khử Trùng Lặp Tuyệt Đối (Idempotency):** Jira Cloud có thể gửi lại cùng một webhook nhiều lần khi có sự cố mạng. `svc_jira` sử dụng Redis Distributed Lock với lệnh `SETNX jira:event:{eventId} 1 EX 86400` để đảm bảo mỗi sự kiện chỉ được xử lý đúng 1 lần duy nhất.
3. **Bản sao Dữ liệu Tối giản (Mirrored Issues):** Lưu trữ thông tin task của Jira để phục vụ trích xuất tri thức, không sao chép toàn bộ rác dữ liệu không cần thiết.

---

## 2. Chi Tiết Schemas Mongoose (Database: `continuum_jira`)

### 2.1. `jira_connections` (Cấu hình kết nối Jira Cloud theo Dự án)
```typescript
export interface IJiraConnection {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  
  atlassianSiteId: string;           // Cloud Site ID từ Atlassian
  atlassianUrl: string;              // VD: "https://mycompany.atlassian.net"
  authType: 'OAUTH2' | 'API_TOKEN';
  
  // Thông tin xác thực mã hóa AES-256-GCM
  credentialsEncrypted: string;
  webhookSecret: string;             // Secret đối soát chữ ký HMAC SHA-256
  
  status: 'CONNECTED' | 'EXPIRED' | 'REVOKED';
  lastSyncAt?: Date;
  createdBy: Types.ObjectId;
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, projectId)`: `{ unique: true }`
  - `atlassianSiteId`: `{ index: true }`

---

### 2.2. `jira_account_links` (Ánh xạ tài khoản Jira với User Continuum)
```typescript
export interface IJiraAccountLink {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  userId: string;                    // Logical Ref sang svc_iam.users._id
  atlassianAccountId: string;        // ID người dùng trên Jira Cloud
  jiraDisplayName: string;
  jiraEmail?: string;
  isVerified: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, userId)`: `{ unique: true }`
  - `(organizationId, atlassianAccountId)`: `{ unique: true }`

---

### 2.3. `jira_issues` (Bản sao Issue Task Jira)
```typescript
export interface IJiraIssue {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  jiraConnectionId: Types.ObjectId;
  
  issueId: string;                   // ID dạng số của Jira (VD: "10045")
  issueKey: string;                  // Khóa task (VD: "CONT-142")
  summary: string;
  descriptionText?: string;          // Trích xuất text thuần từ ADF/Markdown
  
  issueType: 'STORY' | 'BUG' | 'TASK' | 'EPIC' | 'SUBTASK';
  status: string;                    // Tên trạng thái Jira ("In Progress", "Done"...)
  statusCategory: 'TO_DO' | 'IN_PROGRESS' | 'DONE';
  
  assigneeAtlassianId?: string;
  reporterAtlassianId?: string;
  labels: string[];
  components: string[];
  storyPoints?: number;
  
  resolvedAt?: Date;
  lastSyncedAt: Date;
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(projectId, issueKey)`: `{ unique: true }`
  - `(organizationId, projectId, statusCategory)`: `{ index: true }`
  - `(organizationId, assigneeAtlassianId)`: `{ index: true }`

---

### 2.4. `jira_events` (Nhật ký Webhook & Audit Replay)
Lưu trữ toàn văn payload sự kiện nhận được từ webhook của Jira để hỗ trợ phân tích lỗi và phát lại (replay) sự kiện khi worker gặp sự cố.

```typescript
export interface IJiraEvent {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  
  eventId: string;                   // Khóa duy nhất của webhook từ Atlassian
  eventType: string;                 // VD: "jira:issue_updated"
  issueKey: string;
  payload: Record<string, any>;      // Toàn bộ JSON gốc từ Atlassian
  
  processingStatus: 'PENDING' | 'PROCESSED' | 'FAILED' | 'IGNORED';
  errorMessage?: string;
  processedAt?: Date;
  receivedAt: Date;
}
```
* **Chỉ mục & TTL:**
  - `(organizationId, eventId)`: `{ unique: true }`
  - `(processingStatus, receivedAt)`: `{ index: true }`
  - `receivedAt`: `{ expireAfterSeconds: 2592000 }` (Tự động xóa sau 30 ngày)

---

### 2.5. `jira_sync_jobs` (Theo dõi tiến trình đồng bộ hàng loạt - Batch Sync)
Quản lý các đợt đồng bộ dữ liệu lịch sử (Historical Backfill) khi người dùng mới kết nối một dự án Jira vào Continuum AI.

```typescript
export interface IJiraSyncJob {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  connectionId: Types.ObjectId;
  
  jqlQuery: string;                  // Câu truy vấn JQL được dùng
  totalIssuesFound: number;
  issuesSyncedCount: number;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED';
  
  startedAt?: Date;
  completedAt?: Date;
  errorLog?: string[];
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(projectId, status, createdAt)`: `{ index: true }`

---

## 3. Quy Trình Nhận Webhook & Phát Domain Events

```
Jira Cloud ──► POST /api/v1/jira/webhook
                     │
                     ├── 1. Kiểm tra HMAC SHA-256 Signature
                     ├── 2. Redis SETNX jira:event:{eventId} (Khử trùng lặp)
                     ├── 3. Ghi bản ghi vào `jira_events`
                     ├── 4. Cập nhật `jira_issues`
                     └── 5. Xuất bản Domain Event: `jira.issue.synced`
```
- **Sự kiện xuất bản:**
  - `jira.issue.synced`: Bắn sang BullMQ để `svc_capture` gợi ý ghi chú công việc cho developer.
  - `jira.connection.status_changed`: Bắn thông báo cảnh báo nếu token Jira bị thu hồi (Revoked).
