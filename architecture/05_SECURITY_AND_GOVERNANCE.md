# Continuum AI — Bảo Mật, Phân Quyền & Độ Tin Cậy (Security, ACL & Reliability)

> Nằm trong tài liệu kiến trúc tổng thể Continuum AI. Xem [Mục lục](README.md).

---

## 1. Mô hình phân quyền chuẩn mực (Authorization Model)

Continuum AI áp dụng mô hình phân quyền chặt chẽ kết hợp giữa **Role-Based Access Control (RBAC)** và **Attribute-Based Access Control (ABAC)**, tuân thủ tài liệu chuẩn [02_ACTORS_ROLES_AND_PERMISSIONS.md](../research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md).

```
┌────────────────────────────────────────────────────────────────────────┐
│                     MÔ HÌNH PHÂN QUYỀN 3 TẦNG                          │
│                                                                        │
│   [ 1. 3 ROLES CỐ ĐỊNH ]      [ 2. CAPABILITY GRANT ] [ 3. SCOPED ]    │
│   • ADMIN (Tổ chức)           • project.create        • SME            │
│   • TEAM_LEADER (Nhóm)          (Admin cấp riêng        • KNOWLEDGE_   │
│   • MEMBER (Thành viên)          cho Team Leader)         OWNER        │
│                                                       • SUCCESSOR      │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.1. 3 Persistent Roles cố định
1. **`ADMIN`:** Quản lý tài khoản, tổ chức và chính sách hệ thống. Quyền quản trị không tự cấp quyền đọc/sửa task hoặc tri thức bảo mật của dự án.
2. **`TEAM_LEADER`:** Quản lý các nhóm được phân công, duyệt tri thức trong Verification Inbox của nhóm, khởi tạo quy trình bàn giao (`HANDOVER`). **Quy tắc bất biến:** Team Leader **không** mặc định có quyền tạo Project mới.
3. **`MEMBER`:** Đóng góp ghi chú công việc hàng ngày, upload tài liệu, tìm kiếm tri thức trong phạm vi nhóm và tham gia quy trình chuyển giao.

### 1.2. Quyền tạo dự án riêng biệt (`project.create`)
* Quyền tạo dự án là một **Organization Capability Grant** độc lập. Chỉ khi Admin thực hiện thao tác cấp quyền trên bảng `organization_capability_grants`, Team Leader mới có thể tạo dự án mới. Thao tác này có thời hạn (`validUntil`) và có thể bị thu hồi (`revokedAt`).

### 1.3. Các vai trò phân công có phạm vi (Scoped Assignments)
* `SME` (Chuyên gia môn): Thẩm định tri thức trong phạm vi một module hoặc quy trình cụ thể.
* `KNOWLEDGE_OWNER`: Chịu trách nhiệm duy trì tính cập nhật của tri thức theo định kỳ.
* `SUCCESSOR`: Nhân sự kế nhiệm tiếp nhận gói bàn giao công việc khi có người rời đi.

---

## 2. Cơ chế lọc quyền trước truy xuất (Pre-Retrieval Scoped ACL)

Trong các hệ thống RAG thông thường, việc lọc quyền sau khi truy vấn (Post-retrieval filtering) thường dẫn đến rò rỉ dữ liệu hoặc trả về kết quả rỗng. Continuum AI thiết kế bộ lọc **Pre-Retrieval Scoped ACL** bắt buộc:

$$\mathbf{P_{\text{eff}}} = \left( P_{\text{user}} \cup P_{\text{teams}} \cup P_{\text{roles}} \right) \cap \text{SourceACL} \cap \text{Lifecycle}(\text{ACTIVE}) \setminus \text{ExplicitDeny}$$

```
[ User Query: "Mật khẩu deploy production là gì?" ]
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│ NestJS Pre-Retrieval Scoped ACL Resolver                     │
│ 1. Giải mã JWT lấy userId, teamIds, roles                    │
│ 2. Truy vấn MongoDB lấy source/evidence được phép xem         │
│ 3. Tạo filter theo source + tenant/project + ACL             │
└─────────────────────┬────────────────────────────────────────┘
                      │ (Gửi kèm truy vấn có Scoped Filter)
                      ▼
┌──────────────────────────────────────────────────────────────┐
│ FastAPI SAG Engine + retrieval index                          │
│ Chỉ tìm trong tập Work Note/evidence được phép!               │
└──────────────────────────────────────────────────────────────┘
```

* **Lợi ích an ninh:** Loại bỏ 100% rủi ro LLM đọc phải ngữ cảnh nhạy cảm vượt quyền của người dùng.

Task API dùng nguồn quyền Continuum/MongoDB cho mọi thao tác task. Đề xuất quyền task chi tiết nằm tại [permission baseline](../research-docs/02_ACTORS_ROLES_AND_PERMISSIONS.md): Member không tự giao task cho người khác; Team Leader giao/chuyển owner trong scope; Admin không có quyền đọc task chỉ vì là Admin; Successor chỉ đọc task được chọn/ủy quyền.

Task Service là process độc lập trong mạng nội bộ. Gateway/service caller phải được xác thực; Task Service tự kiểm tra tenant/project/team scope và quyền resource trên mỗi request, không tin actor ID hoặc quyền do browser/Agent tự gửi. Agent chỉ nhận context theo user được ủy quyền, rồi trả proposal qua API; người có quyền xác nhận mới được ghi mutation. Cơ chế service credential, identity propagation và secret rotation phải được đưa vào OpenAPI/deployment contract trước khi code Task được triển khai.

SAG chỉ nhận author-confirmed Work Note/evidence sau khi được phép lập chỉ mục và phải lọc theo quyền hiện hành trước retrieval; role allowlist đơn lẻ không thay thế organization/project/team scope hoặc source ACL. Khi nguồn bị thu hồi quyền, request retrieval kế tiếp phải bị chặn ngay; de-index/refresh chạy nền có thể retry nhưng không được cấp quyền dựa trên index cũ.

---

## 3. Bảo mật xác thực & Quản lý phiên (Authentication & Token Security)

```
[ Client ] ──(Gửi Refresh Token)──► [ svc_iam / auth.service ]
                                           │
                                ┌──────────┴──────────┐
                     (Token hợp lệ)         (Token đã từng dùng)
                                │                      │
                                ▼                      ▼
                    [ Cấp mới Access Token ]   [ PHÁT HIỆN TẤN CÔNG ]
                    [ Cấp mới Refresh Token ]  [ Thu hồi toàn bộ    ]
                    [ Cập nhật familyId ]      [ session gia đình!  ]
```

### 3.1. Refresh Token Rotation & Family Reuse Detection
* Refresh Token được mã hóa băm SHA-256 và lưu trong `refresh_sessions` cùng một định danh gia đình (`familyId`).
* Khi client dùng Refresh Token để xin cấp Access Token mới:
  - Token cũ bị đánh dấu `revokedAt: Date`.
  - Hệ thống sinh một Refresh Token mới thuộc cùng `familyId`.
* **Phát hiện tái sử dụng (Reuse Detection):** Nếu một Refresh Token đã thu hồi bị gửi lại (chứng tỏ token đã bị hacker sao chép trộm), hệ thống lập tức **hủy toàn bộ các session có cùng `familyId`**, buộc người dùng đăng nhập lại và gửi email cảnh báo an ninh.

### 3.2. Thu hồi Token tức thời qua Redis Blacklist (<1ms)
* Khi người dùng bấm Đăng xuất hoặc bị Leader chuyển sang trạng thái `OFFBOARDING`:
  - `jti` (JWT ID) của Access Token được ghi ngay vào Redis:
    `SET blacklist:{jti} 1 EX 900` (TTL bằng thời gian sống còn lại của token).
  - API Gateway kiểm tra Redis trong dưới **1ms** cho mỗi request. Nếu tồn tại trong Blacklist, request bị ngắt ngay lập tức với mã HTTP 401.

---

## 4. Kiến trúc Rate Limiting đa tầng (Multi-Tier Distributed Rate Limiting)

Hệ thống triển khai cơ chế giới hạn lưu lượng 3 lớp độc lập để phòng chống tấn công từ chối dịch vụ (DDoS), chống brute-force mật khẩu và bảo vệ ngân sách chi phí gọi LLM APIs:

```
[ INTERNET REQUESTS ]
          │
          ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 1: EDGE NGINX RATE LIMITING (IP-Based Leaky Bucket)               │
│ • limit_req_zone $binary_remote_addr zone=ip_edge:20m rate=50r/s       │
│ • Chặn flood gói tin TCP/HTTP tại biên mạng trước khi vào Backend      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 2: API GATEWAY TIERED LIMITING (Redis Sliding Window Log)         │
│ • Áp dụng theo Identity & Role trong JWT Token:                         │
│   - ADMIN: 300 req/phút                                                │
│   - TEAM_LEADER: 150 req/phút                                          │
│   - MEMBER: 60 req/phút                                                │
│   - Anonymous / Public: 20 req/phút (IP-based)                         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 3: PER-ROUTE CRITICAL QUOTAS (Bảo vệ tài nguyên đắt đỏ)          │
│ • POST /api/v1/auth/login: 5 lần sai / 15 phút (Chống Brute-Force)    │
│ • POST /api/v1/chat/.../messages: 15 câu hỏi / phút (Bảo vệ LLM Quota) │
│ • POST /api/v1/ingestion/upload: 10 files / giờ (Chống cạn dung lượng) │
│ • Task create/update/assign routes: quota theo user + project scope    │
└────────────────────────────────────────────────────────────────────────┘
```

### Response Headers chuẩn RFC 6585 & IETF:
Khi request bị giới hạn, hệ thống trả về HTTP `429 Too Many Requests` kèm các headers:
* `X-RateLimit-Limit`: Tổng quota được cấp trong chu kỳ.
* `X-RateLimit-Remaining`: Số lượng request còn lại.
* `X-RateLimit-Reset`: Thời điểm UNIX timestamp quota được hồi phục.
* `Retry-After`: Số giây client cần đợi trước khi gửi request tiếp theo.

---

## 5. Chiến lược xử lý Tương tranh & Race Conditions (Concurrency Control)

Trong một hệ thống tri thức đa người dùng, nhiều kịch bản tương tranh nguy hiểm có thể xảy ra nếu không được thiết kế kỹ thuật phòng vệ:

### 5.1. Kịch bản 1: Hai SME/Leaders cùng mở và duyệt/sửa 1 Knowledge Object cùng lúc
* **Rủi ro:** Người bấm sau sẽ ghi đè mất các chỉnh sửa hoặc quyết định kiểm chứng của người bấm trước (Lost Update Problem).
* **Giải pháp:** **Kiểm soát tương tranh lạc quan (Optimistic Concurrency Control - OCC)**.
  - Mỗi tài liệu `knowledge_objects` có một trường phiên bản tự tăng `versionNo` (hoặc `__v` trong Mongoose).
  - Khi Client gửi yêu cầu duyệt/sửa:
    ```json
    PUT /api/v1/lifecycle/proposals/:id/verify
    Headers: { "If-Match": "\"v12\"" }
    Body: { "decision": "VERIFIED", "expectedVersion": 12 }
    ```
  - Mongoose thực hiện câu lệnh Atomic Update có điều kiện:
    ```typescript
    const updated = await this.koModel.findOneAndUpdate(
      { _id: koId, versionNo: expectedVersion },
      { $set: { status: 'ACTIVE' }, $inc: { versionNo: 1 } },
      { new: true, session }
    );
    if (!updated) {
      throw new ConflictException("Tài liệu đã được chỉnh sửa bởi người khác. Vui lòng tải lại dữ liệu mới nhất.");
    }
    ```

### 5.2. Kịch bản 2: Tranh chấp bàn giao hoặc đổi người phụ trách Module
* **Rủi ro:** Khi 2 Admin/Leaders cùng thao tác phân công trách nhiệm (`responsibility_assignments`) cho cùng 1 module, dẫn đến việc module có 2 người chịu trách nhiệm chính (`PRIMARY`) cùng thời điểm.
* **Giải pháp:** **Khóa phân tán (Distributed Lock - Redis Mutex / Redlock)**.
  - Trước khi cập nhật khoảng hiệu lực của assignment, service bắt buộc phải xin Distributed Lock trong Redis:
    ```typescript
    const lockKey = `lock:responsibility:${responsibilityId}`;
    const fencingToken = crypto.randomUUID();
    const acquired = await this.redis.set(lockKey, fencingToken, 'NX', 'PX', 3000); // 3s TTL
    if (!acquired) {
      throw new ConflictException("Hệ thống đang xử lý phân công cho module này, vui lòng thử lại sau giây lát.");
    }
    try {
      // Thực thi ACID Mongoose Transaction: đóng assignment cũ, mở assignment mới
      await this.performAssignmentUpdate(session);
    } finally {
      // Giải phóng lock an toàn bằng Lua Script (chỉ xóa khi đúng fencingToken)
      await this.redis.eval(RELEASE_LOCK_LUA, 1, lockKey, fencingToken);
    }
    ```

### 5.3. Kịch bản 3: Hai người cập nhật cùng một task
* **Rủi ro:** Cập nhật đồng thời trạng thái/assignee có thể ghi đè một thay đổi khác hoặc tạo lịch sử không đúng thứ tự.
* **Kiểm soát cần có trong Task API:** Kiểm tra quyền và tenant/project scope ở mỗi mutation; xác định cơ chế chống lost update (ví dụ version check/optimistic concurrency) và idempotency cho retry trước khi chốt API contract. Đây là yêu cầu thiết kế còn cần đặc tả, không có Jira sync trong MVP.

### 5.4. Kịch bản 4: Hai người cùng tải lên cùng 1 tệp lớn (PDF/DOCX)
* **Rủi ro:** Lãng phí tài nguyên lưu trữ Cloudflare R2 và tốn tài nguyên worker OCR phân tách lại tài liệu đã tồn tại.
* **Giải pháp:** **Client-Side SHA-256 Pre-flight Verification**.
  - Trước khi yêu cầu Presigned URL, trình duyệt đọc hash SHA-256 của file bằng Web Crypto API và gửi lên `POST /api/v1/ingestion/check-hash`.
  - Nếu mã SHA-256 đã tồn tại trong `document_versions` của project, server trả về ngay Document ID hiện hữu và **từ chối cấp URL upload mới**.

### 5.5. Kịch bản 5: Cache Stampede (Hàng trăm user cùng hỏi câu hỏi RAG chưa cache)
* **Rủi ro:** Khi cache hết hạn hoặc câu hỏi mới xuất hiện trong giờ cao điểm, 100 request cùng ùa vào gọi LLM và Vector Database gây sập hệ thống (Cache Avalanche).
* **Giải pháp:** **SingleFlight Mutex Pattern**.
  - Chỉ duy nhất request đầu tiên được cấp quyền gọi FastAPI SAG Engine; 99 request còn lại đăng ký lắng nghe một Promise duy nhất đang chờ kết quả. Khi request đầu tiên hoàn tất và ghi vào Redis Cache, 99 request còn lại nhận ngay kết quả mà không chạm vào AI Engine.

---

## 6. Độ tin cậy & Khả năng chống chịu hệ thống (System Reliability)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CƠ CHẾ BẢO VỆ HỆ THỐNG                          │
│                                                                        │
│   ┌────────────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│   │ Multi-Tier Caching     │  │ Distributed    │  │ Circuit        │   │
│   │ (L1 Memory + L2 Redis) │  │ Locks (Redlock)│  │ Breaker (SaaS) │   │
│   ├────────────────────────┤  ├────────────────┤  ├────────────────┤   │
│   │ • L1 LRU (< 0.1ms)     │  │ • Fencing      │  │ • Bảo vệ gọi   │   │
│   │ • L2 Redis (< 2ms)     │  │   Tokens       │  │   SAG / Mail   │   │
│   │ • SingleFlight Mutex   │  │ • Chống Race   │  │ • Bảo vệ gọi   │   │
│   │   chống sập cache      │  │   Conditions   │  │   LLM Gateway  │   │
│   └────────────────────────┘  └────────────────┘  └────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

### 6.1. Caching 2 tầng (Multi-Tier Caching)
* **L1 Cache (In-Memory LRU trong Node.js):** Lưu thông tin tĩnh (Danh sách Roles, Capability Codes, Cấu hình Tenant), độ trễ phản hồi < 0.1ms.
* **L2 Cache (Redis Cluster 7.2):** Lưu kết quả Scoped Claims, kết quả tìm kiếm ngữ nghĩa tương tự.

### 6.2. Circuit Breaker 3 trạng thái (Bảo vệ tích hợp dịch vụ ngoài)
* Đặt tại cổng gọi sang **SAG, object storage, mail provider** và **LLM Gateway (Gemini/OpenAI)**:
  - **Trạng thái CLOSED:** Hoạt động bình thường.
  - **Trạng thái OPEN:** Khi tỷ lệ gọi lỗi vượt quá **50% trong 10 giây**, Circuit Breaker ngắt kết nối ngay lập tức, trả về thông báo lỗi thân thiện thay vì để hệ thống chờ timeout khiến toàn bộ worker bị treo.
  - **Trạng thái HALF-OPEN:** Sau 30 giây hồi phục, cho phép 10% lưu lượng thử nghiệm đi qua; nếu thành công thì đóng mạch về lại CLOSED.

