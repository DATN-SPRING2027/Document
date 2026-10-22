# Chat người dùng — API và phạm vi Redis

> Nằm trong tài liệu kiến trúc tổng thể. Xem [Mục lục](README.md).

Đối chiếu route Chat, Gateway, Redis guard, cache và realtime từ `DATN-BE`. “Được Redis bao phủ” bao gồm rate limit của route nghiệp vụ; không đồng nghĩa mọi response đều được cache.

Ký hiệu `C = /api/v1/chat`, tương ứng `/api/backend/chat` từ trình duyệt và `/internal/chat` trong Chat service. **Tất cả route HTTP nghiệp vụ bên dưới** có `ChatTrafficGuard` dùng Redis để giới hạn request đọc/ghi theo actor và tổ chức. Mỗi route cũng có route chuyển tiếp ở Gateway. Redis còn được dùng theo mục đích riêng ở cột cuối; dấu “cache” không có nghĩa Redis là nguồn dữ liệu bền vững.

| Phương thức và đường dẫn sau `C` | Công dụng | Redis bổ sung |
| --- | --- | --- |
| `GET /candidates` | Tìm người cùng tổ chức | Cache ID ứng viên 15 giây, xác minh lại IAM, giới hạn search, đọc presence |
| `GET /conversations`; `GET /conversations/:conversationId` | Danh sách/tìm hội thoại, chi tiết | Cache repository 15 giây; presence cho direct |
| `POST /direct`; `POST /rooms` | Tạo direct/phòng | Tăng cache generation, giới hạn tạo; Pub/Sub thông báo |
| `PATCH /conversations/:id/room`; `POST /conversations/:id/members`; `DELETE /conversations/:id/members/:userId`; `POST /conversations/:id/leave` | Quản lý phòng | Tăng cache generation; Pub/Sub |
| `GET/PATCH /conversations/:id/preferences` | Đọc/sửa tùy chọn | Cache đọc 15 giây, tăng generation khi ghi |
| `GET/PUT /conversations/:id/draft` | Đọc/lưu bản nháp | Cache và generation riêng theo actor/hội thoại |
| `POST /conversations/:id/ownership`; `PUT /conversations/:id/managers/:userId` | Chuyển chủ/quản lý phòng | Tăng cache generation; Pub/Sub |
| `GET /conversations/:id/messages` | Lịch sử cursor hoặc vùng quanh tin | Cache trang lịch sử ngắn hạn; generation khi nội dung đổi; vùng quanh tin kiểm tra membership rồi đọc repository |
| `GET /conversations/:id/messages/search`; `GET /messages/search` | Tìm trong hội thoại / toàn bộ hội thoại được phép | Cache repository 15 giây theo actor, truy vấn và generation |
| `GET /conversations/:id/library` | Ảnh/tài liệu/link/tin ghim | Cache repository 15 giây |
| `POST /conversations/:id/uploads`; `PUT /conversations/:id/uploads/:uploadId/content`; `POST /conversations/:id/uploads/:uploadId/complete` | Tạo, truyền và hoàn tất upload | Guard rate limit; metadata/byte ở Mongo và S3/R2, không lưu byte trong Redis |
| `GET /conversations/:id/attachments/:attachmentId/download-url` | URL ký sau kiểm tra membership | Cache URL ký 60 giây khi còn hiệu lực |
| `POST /conversations/:id/messages`; `PATCH/DELETE /conversations/:id/messages/:messageId` | Gửi/sửa/xóa | Giới hạn gửi, tăng history/cache generation, Pub/Sub; idempotency bền vững dựa trên Mongo unique key |
| `PUT/DELETE /conversations/:id/messages/:messageId/reactions/:emoji`; `PUT /conversations/:id/messages/:messageId/pin`; `POST /conversations/:id/forward` | Reaction, ghim, chuyển tiếp | Tăng history/cache generation; Pub/Sub |
| `POST /conversations/:id/read`; `POST /conversations/:id/delivered`; `GET /conversations/:id/messages/:messageId/receipts` | Cursor đọc/nhận, chi tiết receipt | Ghi làm mới cache; receipt đọc từ cache; Pub/Sub thay đổi trạng thái |
| `GET /notifications`; `PUT /notifications/:notificationId/read` | Danh sách/đánh dấu thông báo | Cache danh sách; ghi tăng generation |
| `PUT /blocks/:userId`; `POST /reports` | Chặn/bỏ chặn, báo cáo | Guard rate limit; ghi tăng generation |
| `POST /ws-ticket` | Cấp ticket socket một lần | Lưu ticket TTL và consume nguyên tử trong Redis; giới hạn tần suất cấp |

Ngoài HTTP, WebSocket `subscribe`, `unsubscribe`, `presence.watch`, `typing`, `heartbeat` dùng Redis cho ticket/lease presence, Pub/Sub event giữa replica và kiểm tra session revocation; membership vẫn được xác minh trước subscribe/typing/watch. `GET /health` là endpoint kiểm tra sức khỏe, **không** thuộc tập route nghiệp vụ được `ChatTrafficGuard` bảo vệ. Redis bao phủ 100% route nghiệp vụ theo nghĩa rate limiting, **không phải 100% response được cache**. Một số cache miss có đường đọc MongoDB, nhưng khi Redis rate limit của guard không khả dụng, request HTTP nghiệp vụ cũng không đi tiếp. `INFRA_ENABLED=true` mới đăng ký Mongo repository và Redis cache wrapper; khi tắt, repository báo không khả dụng.

Nguồn đối chiếu Redis: `DATN-BE/src/services/chat/controllers/chat-redis-coverage.spec.ts`, `chat-traffic.guard.ts`, `src/services/chat/infrastructure/redis/chat-cache.repository.ts`, `redis.service.ts`, `src/services/chat/application/chat.service.ts`, `chat-realtime.service.ts`, `src/services/chat/infrastructure/chat.infrastructure.module.ts`.
