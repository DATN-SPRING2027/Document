# Continuum AI — Schema Dịch Vụ Thông Báo & Gửi Email
## (Notification & Email Dispatcher Schema - svc_notification)

> **Database:** `continuum_notification` (MongoDB 7.0)  
> **Service sở hữu độc quyền:** `svc_notification`  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ (Bounded Context)

`svc_notification` là trung tâm điều phối mọi luồng thông điệp từ hệ thống đến người dùng:
1. **Thông Báo In-App Thời Gian Thực (WebSocket / SSE):**
   - Đẩy thông báo ngay lập tức lên giao diện chuông thông báo khi có yêu cầu kiểm chứng (Verification Request), cảnh báo hạn bàn giao (Handover Due), hoặc phát hiện khoảng trống tri thức mới.
   - Cơ chế tự động dọn dẹp (TTL Index 90 ngày) để database không bị phình to vô hạn.
2. **Email Giao Dịch Đáng Tin Cậy (Transactional Email via Resend / SMTP):**
   - Định dạng mẫu email chuẩn hóa (`notification_templates`) dùng engine Liquid/Handlebars.
   - Lưu nhật ký gửi email chi tiết (`email_delivery_logs`), theo dõi tỷ lệ thành công, lỗi trả về (Bounced/Failed) và Message ID từ nhà cung cấp để gỡ lỗi.
3. **Cấu Hình Nhận Tin Theo Người Dùng (`notification_preferences`):**
   - Cho phép người dùng bật/tắt từng loại thông báo hoặc chọn nhận gom tin (Digest) thay vì nhận tức thì từng email làm phiền.

---

## 2. Chi Tiết Schemas Mongoose (Database: `continuum_notification`)

### 2.1. `notifications` (Thông báo In-App người dùng)
```typescript
export interface INotification {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId?: Types.ObjectId;
  recipientUserId: string;           // Logical Ref sang svc_iam.users._id
  
  type: 
    | 'VERIFICATION_REQUEST'         // Có đề xuất tri thức mới cần duyệt
    | 'VERIFICATION_APPROVED'        // Đề xuất đã được duyệt ban hành
    | 'VERIFICATION_REJECTED'        // Đề xuất bị từ chối
    | 'HANDOVER_ASSIGNED'            // Được giao quyền tiếp quản trách nhiệm
    | 'HANDOVER_DUE_REMINDER'        // Nhắc nhở hạn chót bàn giao
    | 'KNOWLEDGE_GAP_DETECTED'       // Phát hiện khoảng trống tri thức mới
    | 'KNOWLEDGE_CONFLICT_ALERT';    // Phát hiện mâu thuẫn tài liệu
    
  title: string;
  body: string;
  actionUrl: string;                 // Đường dẫn chuyển hướng khi bấm vào
  
  isRead: boolean;
  readAt?: Date;
  
  createdAt: Date;
}
```
* **Chỉ mục & TTL:**
  - `(recipientUserId, isRead, createdAt)`: `{ index: true }`
  - `createdAt`: `{ expireAfterSeconds: 7776000 }` (Tự động xóa sau 90 ngày)

---

### 2.2. `notification_preferences` (Tùy chọn nhận thông báo của người dùng)
```typescript
export interface INotificationPreference {
  _id: Types.ObjectId;
  userId: string;                    // Logical Ref sang svc_iam.users._id
  organizationId: Types.ObjectId;
  
  emailEnabled: boolean;
  inAppEnabled: boolean;
  
  // Tùy chọn chi tiết theo loại sự kiện
  notifyOnVerificationRequest: boolean;
  notifyOnVerificationDecision: boolean;
  notifyOnHandoverDue: boolean;
  notifyOnKnowledgeGap: boolean;
  
  emailFrequency: 'INSTANT' | 'DAILY_DIGEST' | 'WEEKLY_DIGEST' | 'OFF';
  
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(userId, organizationId)`: `{ unique: true }`

---

### 2.3. `notification_templates` (Mẫu giao diện thông báo & Email)
```typescript
export interface INotificationTemplate {
  _id: Types.ObjectId;
  templateCode: string;              // VD: "TPL_VERIFICATION_REQUEST"
  channel: 'IN_APP' | 'EMAIL';
  subjectTemplate?: string;          // "Continuum AI: Đề xuất tri thức mới cần bạn kiểm chứng"
  bodyTemplate: string;              // Template cú pháp Handlebars/Liquid
  variablesRequired: string[];       // ["userName", "proposalTitle", "actionUrl"]
  isSystem: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(templateCode, channel)`: `{ unique: true }`

---

### 2.4. `email_delivery_logs` (Nhật ký gửi Email giao dịch)
```typescript
export interface IEmailDeliveryLog {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  recipientEmail: string;
  recipientUserId?: string;
  
  templateCode: string;
  subject: string;
  deliveryStatus: 'QUEUED' | 'SENT' | 'DELIVERED' | 'BOUNCED' | 'FAILED';
  
  provider: 'RESEND' | 'SENDGRID' | 'SMTP';
  providerMessageId?: string;        // ID từ Resend / SendGrid để tra soát
  attempts: number;
  errorMessage?: string;
  
  sentAt?: Date;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(recipientEmail, createdAt)`: `{ index: true }`
  - `(deliveryStatus, createdAt)`: `{ index: true }`

---

## 3. Lắng Nghe Sự Kiện Hệ Thống (Domain Events Consumed)

`svc_notification` lắng nghe các sự kiện từ toàn bộ hệ sinh thái để bắn thông báo:
- `lifecycle.verification.requested` ➔ Gửi mail & in-app cho SME / Team Leader.
- `lifecycle.knowledge.published` ➔ Báo cho tác giả đề xuất tri thức đã được thông qua.
- `handover.campaign.started` ➔ Gửi thông báo lộ trình bàn giao cho người kế nhiệm.
- `jira.connection.status_changed` ➔ Cảnh báo Admin nếu webhook Jira bị ngắt kết nối.
