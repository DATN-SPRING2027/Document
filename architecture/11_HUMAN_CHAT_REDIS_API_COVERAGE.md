# Chat người dùng — API và phạm vi Redis

> Nằm trong tài liệu kiến trúc tổng thể. Xem [Mục lục](README.md).

Đối chiếu route Chat, Gateway, Redis guard, cache và realtime từ `DATN-BE`. “Được Redis bao phủ” bao gồm rate limit của route nghiệp vụ; không đồng nghĩa mọi response đều được cache.

Ký hiệu `C = /api/v1/chat`, tương ứng `/api/backend/chat` từ trình duyệt và `/internal/chat` trong Chat service. **Tất cả route HTTP nghiệp vụ bên dưới** có `ChatTrafficGuard` dùng Redis để giới hạn request đọc/ghi theo actor và tổ chức. Mỗi route cũng có route chuyển tiếp ở Gateway. Redis còn được dùng theo mục đích riêng ở cột cuối; dấu “cache” không có nghĩa Redis là nguồn dữ liệu bền vững.

| Phương thức và đường dẫn sau `C` | Công dụng | Redis bổ sung |
| --- | --- | --- |
| `GET /candidates` | Tìm người cùng tổ chức | Cache ID ứng viên 15 giây, xác minh lại IAM, giới hạn search, đọc presence |
| `GET /conversations`; `GET /conversations/:conversationId` | Danh sách/tìm hội thoại, chi tiết (kèm `capabilities.dmAssistantEnabled`) | Cache repository 15 giây; presence cho direct |
| `POST /direct`; `POST /rooms` | Tạo direct/phòng | Tăng cache generation, giới hạn tạo; Pub/Sub thông báo |
| `PATCH /conversations/:id/room`; `POST /conversations/:id/members`; `DELETE /conversations/:id/members/:userId`; `POST /conversations/:id/leave` | Quản lý phòng | Tăng cache generation; Pub/Sub |
| `GET/PATCH /conversations/:id/preferences` | Đọc/sửa tùy chọn | Cache đọc 15 giây, tăng generation khi ghi |
| `GET/PUT /conversations/:id/draft` | Đọc/lưu bản nháp (kèm `assistantMention?: boolean`) | Cache và generation riêng theo actor/hội thoại |
| `POST /conversations/:id/ownership`; `PUT /conversations/:id/managers/:userId` | Chuyển chủ/quản lý phòng | Tăng cache generation; Pub/Sub |
| `GET /conversations/:id/messages` | Lịch sử cursor hoặc vùng quanh tin (`aroundMessageId`); làm giàu sống `sourceReferences[].status` (`ACTIVE`/`EDITED`/`DELETED`) và hydrate `assistantState` | Cache trang lịch sử ngắn hạn (10 giây) theo `history-version`; làm mới đồng thời `history-version` + `cache-generation` khi có sửa/xóa hoặc chuyển trạng thái job AI; vùng quanh tin kiểm tra membership rồi đọc repository |
| `GET /conversations/:id/messages/search`; `GET /messages/search` | Tìm trong hội thoại / toàn bộ hội thoại được phép (gồm tin AI đã đăng, đã làm giàu nguồn) | Cache repository 15 giây theo actor, truy vấn và generation |
| `GET /conversations/:id/library` | Ảnh/tài liệu/link/tin ghim (`PIN` gồm cả tin AI được ghim) | Cache repository 15 giây |
| `POST /conversations/:id/uploads`; `PUT /conversations/:id/uploads/:uploadId/content`; `POST /conversations/:id/uploads/:uploadId/complete` | Tạo, truyền và hoàn tất upload | Guard rate limit; metadata/byte ở Mongo và S3/R2, không lưu byte trong Redis |
| `GET /conversations/:id/attachments/:attachmentId/download-url` | URL ký sau kiểm tra membership | Cache URL ký 60 giây khi còn hiệu lực |
| `POST /conversations/:id/messages`; `PATCH/DELETE /conversations/:id/messages/:messageId` | Gửi (hỗ trợ `assistantMention` trên `DIRECT`), sửa/xóa (chặn sửa/xóa tin AI `403 CHAT_ASSISTANT_MESSAGE_IMMUTABLE`, `PATCH` từ chối `assistantMention` `422`) | Giới hạn gửi (`send:<org>:<user>`) + giới hạn riêng cho `@continuumAI` (`dm-assistant:<org>:<user>`, mặc định `15`/60s → `429 CHAT_ASSISTANT_RATE_LIMITED`); tăng đồng thời `history-version:<org>:<conv>` và `cache-generation:<org>`; Pub/Sub `message.*` và `assistant.status`; idempotency bền vững dựa trên Mongo unique key |
| `PUT/DELETE /conversations/:id/messages/:messageId/reactions/:emoji`; `PUT /conversations/:id/messages/:messageId/pin`; `POST /conversations/:id/forward` | Reaction, ghim, chuyển tiếp (chặn chuyển tiếp tin AI `422 CHAT_ASSISTANT_FORWARD_FORBIDDEN`) | Tăng `history-version` + `cache-generation`; Pub/Sub |
| `POST /conversations/:id/read`; `POST /conversations/:id/delivered`; `GET /conversations/:id/messages/:messageId/receipts` | Cursor đọc/nhận, chi tiết receipt | Ghi làm mới cache; receipt đọc từ cache; Pub/Sub thay đổi trạng thái |
| `GET /notifications`; `PUT /notifications/:notificationId/read` | Danh sách/đánh dấu thông báo (gồm thông báo tin AI đã đăng khi `notificationMode === 'ALL'`) | Cache danh sách; ghi tăng generation |
| `PUT /blocks/:userId`; `POST /reports` | Chặn/bỏ chặn, báo cáo | Guard rate limit; ghi tăng generation |
| `POST /ws-ticket` | Cấp ticket socket một lần | Lưu ticket TTL và consume nguyên tử trong Redis; giới hạn tần suất cấp |

Ngoài HTTP, WebSocket `subscribe`, `unsubscribe`, `presence.watch`, `typing`, `heartbeat` dùng Redis cho ticket/lease presence, Pub/Sub event giữa replica (gồm `message.*`, `conversation.*` và **`assistant.status`** phát riêng tới thành viên `ACTIVE` `[A, B]` và loại `requesterUserId` nếu bị thu hồi quyền IAM) và kiểm tra session revocation; membership vẫn được xác minh trước subscribe/typing/watch. Khi `ChatDmAssistantWorkerService` đăng câu trả lời AI hoặc hủy/lỗi job, worker gọi `ChatHistoryCacheInvalidator.invalidate(orgId, convId)` tăng đồng thời cả `<prefix>:chat:history-version:<orgId>:<convId>` và `<prefix>:chat:cache-generation:<orgId>` (TTL 24 giờ) để lần đọc kế tiếp không bao giờ trả `sourceReferences[].status` cũ. `GET /health` là endpoint kiểm tra sức khỏe, **không** thuộc tập route nghiệp vụ được `ChatTrafficGuard` bảo vệ. Redis bao phủ 100% route nghiệp vụ theo nghĩa rate limiting, **không phải 100% response được cache**. Một số cache miss có đường đọc MongoDB, nhưng khi Redis rate limit của guard không khả dụng, request HTTP nghiệp vụ cũng không đi tiếp. `INFRA_ENABLED=true` mới đăng ký Mongo repository và Redis cache wrapper; khi tắt, repository báo không khả dụng.

Nguồn đối chiếu Redis & Contract: `DATN_BE/src/services/chat/controllers/chat-redis-coverage.spec.ts`, `chat-traffic.guard.ts`, `src/services/chat/infrastructure/redis/chat-cache.repository.ts`, `redis.service.ts`, `src/services/chat/application/{chat.service,chat-history-cache,chat-realtime.service,chat-dm-assistant.worker}.ts`, `src/services/chat/infrastructure/chat.infrastructure.module.ts`, `DATN_BE/docs/openapi/chat-v1.openapi.json` (v`1.2.0`).
