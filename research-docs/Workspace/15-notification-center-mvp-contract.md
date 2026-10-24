# 15. Notification Center MVP — Architecture, Security, Schema & API Contract

- **Status:** Implemented (`DATN_BE` PR #93, `DATN_FE` PR #79)
- **Domain Scope:** Organization, Project, Work Task, Work Note, Chat Mention
- **Database:** MongoDB (`continuum_notification.notifications`)
- **Realtime Transport:** Socket.IO (`/ws/notifications`) + Redis Pub/Sub (`notification.realtime.v1`) + Polling Fallback (`30s`)
- **OpenAPI Spec:** [`contracts/notification-v1.openapi.json`](./contracts/notification-v1.openapi.json)

---

## 1. Mục tiêu & Phạm vi (Scope)

Notification Center MVP cung cấp trung tâm thông báo tập trung cho 5 phân hệ cốt lõi:

1. **Organization (`ORGANIZATION`)**
2. **Project (`PROJECT`)**
3. **Work Task (`TASK`)**
4. **Work Note (`WORK_NOTE`)**
5. **Chat (`CHAT`)**

Mọi thông báo tuân thủ nguyên tắc:
- Chỉ được tạo **sau khi business mutation thành công** (post-mutation side-effect, fail-safe, không làm rollback luồng nghiệp vụ chính nếu dịch vụ thông báo gặp sự cố tạm thời).
- **Không bypass Authorization (ACL)**: Kiểm tra quyền truy cập thực tế tại thời điểm đọc danh sách (`GET /api/v1/notifications`) và thời điểm điều hướng (`GET /api/v1/notifications/:id/resolve`).
- Hỗ trợ trạng thái `UNREAD` / `READ`, đếm số lượng chưa đọc (`unread-count`), đánh dấu đã đọc từng thông báo hoặc toàn bộ, realtime badge qua WebSocket/Redis và xử lý an toàn khi tài nguyên đích đã bị xóa hoặc thu hồi quyền.

---

## 2. Danh mục 13 Sự kiện Notification MVP

| # | Event Type (`type`) | Module (`module`) | Resource Type (`resourceType`) | Trigger & Nguồn phát sinh | Người nhận (`recipientId`) | Deep-link (`target.url`) |
|---|---|---|---|---|---|---|
| 1 | `ORGANIZATION_MEMBER_INVITED` | `ORGANIZATION` | `ORGANIZATION` | Quản trị viên gửi lời mời tham gia tổ chức (nếu email khớp tài khoản đã tồn tại) | User được mời | `/organizations` |
| 2 | `ORGANIZATION_MEMBER_ADDED` | `ORGANIZATION` | `ORGANIZATION` | Quản trị viên kích hoạt/thêm thành viên vào tổ chức (nếu user tự chấp nhận lời mời của chính mình: `actorId === recipientId` -> bị chặn bởi Rule 1) | Thành viên được thêm | `/organizations` |
| 3 | `ORGANIZATION_MEMBER_REMOVED` | `ORGANIZATION` | `ORGANIZATION` | Quản trị viên xóa/thu hồi tư cách thành viên khỏi tổ chức | Thành viên bị xóa | `/organizations` |
| 4 | `PROJECT_MEMBER_ADDED` | `PROJECT` | `PROJECT` | Thêm thành viên vào dự án | Thành viên được thêm | `/projects/:projectId` |
| 5 | `PROJECT_MEMBER_REMOVED` | `PROJECT` | `PROJECT` | Xóa thành viên khỏi dự án | Thành viên bị xóa | `/projects` |
| 6 | `PROJECT_LEADER_ASSIGNED` | `PROJECT` | `PROJECT` | Bổ nhiệm Project Leader cho dự án mới hoặc chưa có Leader | Project Leader mới | `/projects/:projectId` |
| 7 | `PROJECT_LEADER_CHANGED` | `PROJECT` | `PROJECT` | Chuyển giao vai trò Project Leader từ người cũ sang người mới | Leader mới (nhận `PROJECT_LEADER_CHANGED`/`ASSIGNED`) & Leader cũ (nhận `PROJECT_LEADER_REVOKED`) | `/projects/:projectId` |
| 8 | `PROJECT_LEADER_REVOKED` | `PROJECT` | `PROJECT` | Thu hồi vai trò Project Leader | Cựu Project Leader | `/projects/:projectId` |
| 9 | `TASK_ASSIGNED` | `TASK` | `TASK` | Giao việc (`assigneeIds`) khi tạo mới hoặc cập nhật Task | Các Assignee mới được thêm | `/projects/:projectId?taskId=:taskId` |
| 10 | `TASK_DEADLINE_APPROACHING` | `TASK` | `TASK` | Cron/Scheduler phát hiện Task chưa hoàn thành có `dueDate` trong vòng 24 giờ tới | Các Assignee hiện tại của Task | `/projects/:projectId?taskId=:taskId` |
| 11 | `TASK_DEADLINE_OVERDUE` | `TASK` | `TASK` | Cron/Scheduler phát hiện Task chưa hoàn thành đã quá hạn (`dueDate < now`) | Các Assignee hiện tại của Task | `/projects/:projectId?taskId=:taskId` |
| 12 | `WORK_NOTE_MENTION` | `WORK_NOTE` | `WORK_NOTE` | Nhắc tên (`@username` / `@email` / `mentionUserIds`) trong Work Note | Các User được nhắc tên (có quyền truy cập tổ chức/dự án chứa Note) | `/work-notes?noteId=:noteId` |
| 13 | `CHAT_MENTION` | `CHAT` | `CHAT` | Nhắc tên (`@username` / `@email` / `mentions`) trong tin nhắn hội thoại | Các thành viên `ACTIVE` của cuộc trò chuyện được nhắc tên | `/chat?conversationId=:conversationId` |

---

## 3. Các Quy tắc Nghiệp vụ & Bảo mật Cốt lõi (Business & Security Rules)

### Rule 1 — Không tự thông báo (No Self-Notification)
- Nếu `actorId` trùng với `recipientId` (`String(actorId) === String(recipientId)`), hệ thống **tuyệt đối không tạo thông báo** cho người đó.
- Áp dụng cho toàn bộ 13 sự kiện, bao gồm cả trường hợp người dùng tự chấp nhận lời mời vào tổ chức (`OrganizationInvitationService.acceptInvitation` truyền `actorId: actor.id`).

### Rule 2 — Chống trùng lặp & Idempotency (`eventKey`)
- Trong một sự kiện nghiệp vụ, danh sách `recipientIds` được chuẩn hóa và loại bỏ trùng lặp (`Set`) trước khi xử lý.
- Mỗi thông báo sinh ra có khóa định danh duy nhất theo từng người nhận `(recipientId, eventKey)` với unique sparse index `recipientId_1_eventKey_1`.
- Nếu cùng một sự kiện hoặc lịch quét deadline (`TASK_DEADLINE_APPROACHING`, `TASK_DEADLINE_OVERDUE`) chạy lặp lại trên cùng mốc `dueDate`, thao tác `updateOne({ recipientId, eventKey }, { $setOnInsert: ... }, { upsert: true })` đảm bảo chỉ tạo đúng **1 bản ghi duy nhất**.

### Rule 3 — Quét Deadline theo Cursor ổn định (Deterministic Cursor Pagination)
- `TaskDeadlineNotificationScheduler` quét các Task có hạn bằng con trỏ `_id` tăng dần (`_id: { $gt: lastCursorId }`, `.sort({ _id: 1 }).limit(200)`) lặp cho đến khi duyệt hết toàn bộ tập Task thỏa điều kiện.
- Ngăn chặn triệt để hiện tượng bỏ sót (starvation) các Task phía sau khi hệ thống có hơn 200 Task quá hạn.

### Rule 4 — Kiểm tra Quyền Truy cập Động (Live ACL Re-evaluation) & Ẩn Nội dung Nhạy cảm (Redaction)
- **Khi hiển thị danh sách (`GET /api/v1/notifications`)**:
  - `NotificationCenterRepository.sanitizeItemsForListing` kiểm tra trạng thái tồn tại và quyền truy cập hiện tại (`resolveTargetAccess`) đối với từng thông báo.
  - Nếu tài nguyên đích đã bị xóa (`RESOURCE_DELETED`) hoặc người nhận không còn quyền truy cập (`ACCESS_DENIED`), nội dung `message` (vốn có thể chứa tiêu đề Task mật, Work Note hoặc tên Project Private) sẽ được che lại thành `"Content is no longer available."` và `target.url` được chuyển về `"/notifications"`.
- **Khi người dùng bấm vào thông báo (`GET /api/v1/notifications/:id/resolve`)**:
  - Kiểm tra quyền sở hữu thông báo (`recipientId === actor.id`). Nếu của người khác -> trả về `403 NOTIFICATION_FORBIDDEN`.
  - Đánh giá lại quyền truy cập theo từng phân hệ:
    - `ORGANIZATION`: Với sự kiện `ORGANIZATION_MEMBER_REMOVED`, cho phép điều hướng về `/organizations`. Với các sự kiện khác, yêu cầu `organization_memberships.status === 'ACTIVE'`.
    - `PROJECT`: Với `PROJECT_MEMBER_REMOVED` / `PROJECT_LEADER_REVOKED`, điều hướng an toàn về `/projects`. Với các sự kiện khác, yêu cầu Project chưa bị xóa, `organization_memberships.status === 'ACTIVE'` và nếu Project là `PRIVATE` thì người dùng phải là `PROJECT_MEMBER` / `PROJECT_LEADER` hoặc `ORG_ADMIN` / `PLATFORM_OPERATOR`.
    - `TASK`: Yêu cầu Task chưa bị xóa (`deletedAt == null`, `isDeleted !== true`) và thỏa quyền truy cập vào Project chứa Task.
    - `WORK_NOTE`: Yêu cầu Work Note chưa bị xóa, người dùng thuộc `organization_memberships` (`ACTIVE`), và nếu Note có `visibility === 'PRIVATE'` thì chỉ tác giả hoặc người được liệt kê trong `mentionedUserIds` mới được xem.
    - `CHAT`: Yêu cầu hội thoại tồn tại, người dùng có `organization_memberships.status === 'ACTIVE'` tại tổ chức của hội thoại và trạng thái thành viên trong `chat_members` (hoặc `conversations.members`) phải là `ACTIVE` (từ chối `LEFT` hoặc `REMOVED`).

### Rule 5 — Xử lý Điều hướng An toàn trên Frontend (Safe Deep-Link & Retry UX)
- Khi người dùng click vào một thông báo trên `NotificationDropdown` hoặc trang `/notifications` (`NotificationsWorkspace`):
  1. Đánh dấu đã đọc (`PATCH /api/v1/notifications/:id/read`) nếu thông báo đang ở trạng thái `UNREAD`.
  2. Gọi `GET /api/v1/notifications/:id/resolve`.
  3. Nếu `available: true` -> điều hướng tới `url` được BE trả về.
  4. Nếu `available: false` (hoặc HTTP `403`/`404`/`410`) -> hiển thị hộp thoại an toàn (`Unavailable Target Dialog`) thông báo tài nguyên đã bị xóa hoặc không còn quyền truy cập và giữ người dùng ở lại trang an toàn.
  5. Nếu API `/resolve` gặp lỗi mạng hoặc lỗi máy chủ (`5xx`, timeout) -> **không tự ý điều hướng sang `target.url` chưa qua kiểm chứng ACL**; hiển thị cảnh báo lỗi kèm nút **Thử lại (`Retry`)** ngay tại giao diện.

---

## 4. Thiết kế Cơ sở Dữ liệu (`continuum_notification.notifications`)

### 4.1. Cấu trúc Document

```json
{
  "_id": "5f9efad3-8a29-4e92-9214-c9549c74264f",
  "recipientId": "usr_member_01",
  "recipientUserId": "usr_member_01",
  "actorId": "usr_leader_01",
  "actorName": "Alice Leader",
  "organizationId": "org_01",
  "projectId": "prj_01",
  "module": "TASK",
  "type": "TASK_ASSIGNED",
  "title": "New task assigned",
  "message": "Alice Leader assigned you to task \"Implement Notification MVP\" in Project Alpha.",
  "resourceType": "TASK",
  "resourceId": "tsk_01",
  "target": {
    "resourceType": "TASK",
    "resourceId": "tsk_01",
    "organizationId": "org_01",
    "projectId": "prj_01",
    "taskId": "tsk_01",
    "url": "/projects/prj_01?taskId=tsk_01"
  },
  "status": "UNREAD",
  "isRead": false,
  "readAt": null,
  "eventKey": "TASK_ASSIGNED:tsk_01:usr_member_01",
  "metadata": {
    "taskTitle": "Implement Notification MVP",
    "projectName": "Project Alpha"
  },
  "createdAt": "2026-10-24T04:00:00.000Z",
  "updatedAt": "2026-10-24T04:00:00.000Z"
}
```

### 4.2. Danh sách Index (`NOTIFICATION_PERSISTENCE`)

| Tên Index | Keys | Options | Mục đích |
|---|---|---|---|
| `recipientUserId_1_isRead_1_createdAt_1` | `{ recipientUserId: 1, isRead: 1, createdAt: 1 }` | `{}` | Tương thích ngược với schema lõi (`08_SVC_NOTIFICATION_SCHEMA.md`) |
| `createdAt_1` | `{ createdAt: 1 }` | `{ expireAfterSeconds: 7776000 }` | TTL Index tự động dọn dẹp thông báo sau 90 ngày (7.776.000 giây) |
| `recipientId_1_createdAt_-1` | `{ recipientId: 1, createdAt: -1 }` | `{}` | Truy vấn danh sách thông báo mới nhất theo người nhận |
| `recipientId_1_readAt_1_createdAt_-1` | `{ recipientId: 1, readAt: 1, createdAt: -1 }` | `{}` | Lọc thông báo chưa đọc (`unreadOnly=true`) và đếm `unread-count` |
| `recipientId_1_eventKey_1` | `{ recipientId: 1, eventKey: 1 }` | `{ unique: true, sparse: true }` | Chống nhân bản thông báo cho cùng một sự kiện (`sparse: true` để an toàn với bản ghi lịch sử chưa có `eventKey`) |

### 4.3. Tương thích Ngược, Migration & Kế hoạch Rollback

1. **Dual-field Read/Write ở tầng Repository (`NotificationCenterRepository`)**:
   - Khi ghi mới: luôn ghi đồng thời `recipientId` + `recipientUserId` và `status` + `isRead` + `readAt`.
   - Khi đọc/cập nhật: sử dụng bộ lọc tương thích `$or: [{ recipientId }, { recipientUserId: recipientId }]` và suy luận trạng thái đã đọc từ `readAt != null || status === 'READ' || isRead === true`.
2. **Script Migration / Backfill (`scripts/migrations/20261024-notification-mvp-backfill.mjs`)**:
   - Chế độ kiểm tra trước (Dry-run):
     ```bash
     node scripts/migrations/20261024-notification-mvp-backfill.mjs --dry-run
     ```
   - Chế độ thực thi (Apply):
     ```bash
     node scripts/migrations/20261024-notification-mvp-backfill.mjs --apply
     ```
   - Chức năng: Điền đầy đủ `recipientId` (từ `recipientUserId`), `recipientUserId` (từ `recipientId`), `eventKey` (`legacy:<_id>`), `status` (`READ`/`UNREAD`), `isRead`, `readAt`, `module`, `resourceType`, `resourceId`, `target`, và đồng bộ các index trên `continuum_notification.notifications`.
3. **Kế hoạch Rollback**:
   - Vì các trường cũ (`recipientUserId`, `isRead`, `createdAt`) và index `recipientUserId_1_isRead_1_createdAt_1` được giữ nguyên hoàn toàn, việc rollback code BE về bản trước không làm mất dữ liệu hay lỗi truy vấn.

---

## 5. Đặc tả REST API (`/api/v1/notifications`)

Tất cả các endpoint đều yêu cầu xác thực Bearer JWT (`Authorization: Bearer <accessToken>`). Chi tiết schema OpenAPI 3.0 được định nghĩa tại [`contracts/notification-v1.openapi.json`](./contracts/notification-v1.openapi.json).

### 5.1. `GET /api/v1/notifications`
Lấy danh sách thông báo của người dùng hiện tại (sắp xếp theo `createdAt DESC`, phân trang theo `cursor`).

- **Query Parameters:**
  - `cursor` (string, optional — con trỏ phân trang `nextCursor` từ trang trước)
  - `limit` (integer, default `20`, min `1`, max `100`)
  - `unreadOnly` (`"true"` | `"false"`, optional)
- **Response `200 OK`:**
  ```json
  {
    "items": [
      {
        "id": "5f9efad3-8a29-4e92-9214-c9549c74264f",
        "recipientId": "usr_member_01",
        "actorId": "usr_leader_01",
        "organizationId": "org_01",
        "projectId": "prj_01",
        "taskId": "tsk_01",
        "noteId": null,
        "conversationId": null,
        "type": "TASK_ASSIGNED",
        "title": "New task assigned",
        "message": "Alice Leader assigned you to task \"Implement Notification MVP\" in Project Alpha.",
        "target": {
          "kind": "TASK",
          "url": "/projects/prj_01?taskId=tsk_01",
          "organizationId": "org_01",
          "projectId": "prj_01",
          "taskId": "tsk_01",
          "noteId": null,
          "conversationId": null,
          "messageId": null
        },
        "readAt": null,
        "createdAt": "2026-10-24T04:00:00.000Z"
      }
    ],
    "nextCursor": null,
    "unreadCount": 1
  }
  ```

### 5.2. `GET /api/v1/notifications/unread-count`
Trả về tổng số thông báo chưa đọc của người dùng hiện tại.

- **Response `200 OK`:**
  ```json
  {
    "count": 3
  }
  ```

### 5.3. `PATCH /api/v1/notifications/:id/read`
Đánh dấu một thông báo là đã đọc (`readAt != null`). Idempotent: nếu gọi nhiều lần trên thông báo đã đọc vẫn trả về `200 OK` và giữ nguyên `readAt`.

- **Response `200 OK`:** Trả về `NotificationItem` đã cập nhật (`readAt` khác `null`).
- **Response `404 Not Found`:** Khi không tìm thấy thông báo hoặc thông báo không thuộc về người dùng hiện tại.

### 5.4. `PATCH /api/v1/notifications/read-all`
Đánh dấu toàn bộ thông báo chưa đọc của người dùng hiện tại thành đã đọc.

- **Response `200 OK`:**
  ```json
  {
    "updatedCount": 3,
    "readAt": "2026-10-24T04:05:00.000Z"
  }
  ```

### 5.5. `GET /api/v1/notifications/:id/resolve`
Kiểm tra sự tồn tại của tài nguyên đích và quyền truy cập hiện thời của người nhận trước khi điều hướng deep-link.

- **Response `200 OK` (Hợp lệ):**
  ```json
  {
    "available": true,
    "reason": "OK",
    "message": "Target is available",
    "target": {
      "kind": "TASK",
      "url": "/projects/prj_01?taskId=tsk_01",
      "organizationId": "org_01",
      "projectId": "prj_01",
      "taskId": "tsk_01",
      "noteId": null,
      "conversationId": null,
      "messageId": null
    }
  }
  ```
- **Response `200 OK` (Tài nguyên đã xóa hoặc mất quyền truy cập):**
  ```json
  {
    "available": false,
    "reason": "DELETED",
    "message": "This content is no longer available",
    "target": null
  }
  ```

---

## 6. Realtime WebSocket & Kiến trúc Frontend

### 6.1. Realtime Gateway (`/ws/notifications`)
- Khi người dùng đăng nhập, FE kết nối Socket.IO tới namespace `/ws/notifications` với JWT token, tự động tham gia room `user:<userId>`.
- Khi thông báo mới được tạo hoặc trạng thái đọc thay đổi, BE phát sự kiện qua Redis Pub/Sub (`notification.realtime.v1`) và đẩy xuống client qua 2 event:
  - `notification:new`: `{ notification, unreadCount }`
  - `notification:unread_count`: `{ unreadCount }`
- Trong trường hợp WebSocket bị ngắt kết nối, FE tự động duy trì cơ chế polling định kỳ mỗi `30s` để cập nhật `unreadCount`.

### 6.2. Các Thành phần Giao diện (`DATN_FE`)
- **`NotificationDropdown`** (`src/components/header/NotificationDropdown.tsx`):
  - Chuông thông báo trên Header kèm badge hiển thị số lượng chưa đọc (`unreadCount`).
  - Bộ lọc tab `All` / `Unread`, nút `Mark all as read`, danh sách thông báo rút gọn, trạng thái `Empty`, trạng thái lỗi khi `/resolve` thất bại kèm nút `Retry`, và Modal thông báo khi tài nguyên không còn khả dụng.
- **`NotificationsWorkspace`** (`src/components/notifications/NotificationsWorkspace.tsx`):
  - Trang trung tâm thông báo đầy đủ tại `/notifications` hỗ trợ phân trang, lọc `All` / `Unread`, đánh dấu đã đọc từng mục hoặc toàn bộ, điều hướng deep-link an toàn và đa ngôn ngữ (`vi` / `en`).
