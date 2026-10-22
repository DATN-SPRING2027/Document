# Chat người dùng — Kiến trúc realtime và khả năng mở rộng đang triển khai

> Nằm trong tài liệu kiến trúc tổng thể. Xem [Mục lục](README.md). Danh mục [tính năng FE–BE](08_HUMAN_CHAT_FE_BE_FEATURES.md) và [API/Redis](11_HUMAN_CHAT_REDIS_API_COVERAGE.md) được tách riêng.

Tài liệu này đối chiếu **mã chạy hiện tại** của Chat người với người trong `DATN-BE`/`DATN-FE` (22/10/2026). Đây là hệ thống `DIRECT`/`ROOM` trong một Organization; không phải Cited Assistant/RAG Chat ở các chương kiến trúc cũ. Mục tiêu của cách tổ chức hiện tại là giữ tin bền vững trong MongoDB, dùng WebSocket để báo thay đổi nhanh, và cho phép nhiều Chat replica phục vụ các kết nối đồng thời qua Redis. Mã nguồn chưa cung cấp benchmark hay SLO để khẳng định một mức tải cụ thể.

## 1. Topology thực tế và ranh giới service

```mermaid
flowchart LR
    FE[Next.js Chat UI<br/>TanStack Query] -->|HTTP command/query| BFF[Next.js BFF<br/>/api/backend/chat]
    BFF --> GW[NestJS Gateway<br/>/api/v1/chat]
    GW -->|HTTP /internal/chat| CH[Chat service replica 1..N]
    FE -->|WSS /internal/chat/ws<br/>qua Nginx/Ingress| CH
    CH -->|xác thực actor và candidate| IAM[IAM service]
    CH -->|message, member, conversation| MG[(MongoDB<br/>continuum_chat)]
    CH <-->|ticket, rate limit, cache,<br/>presence lease, Pub/Sub| RD[(Redis)]
    CH -->|ảnh| S3[(AWS S3)]
    CH -->|tài liệu| R2[(Cloudflare R2)]
```

`services/chat/main.ts` khởi động một NestJS process riêng trên port cấu hình; `ChatModule` gồm HTTP controllers, `ChatRealtimeGateway`, application services và infrastructure. Gateway chỉ forward 38 route Chat; nó không giữ message hoặc WebSocket session. BFF dùng cookie/session của ứng dụng và forward HTTP. Nginx Compose và Helm Ingress định tuyến riêng `/internal/chat/ws` thẳng tới Chat, tránh đưa từng WebSocket frame qua Next.js BFF/Gateway. Upload byte đi qua BFF → Gateway → Chat theo stream. Trong Helm hiện `services.chat.replicas: 1` mặc định; kiến trúc hỗ trợ chia kết nối ra nhiều replica nhưng mặc định triển khai **chưa chứng minh tải nhiều replica**. Nguồn: `DATN-BE/src/services/chat/main.ts`, `chat.module.ts`, `src/gateway/gateway-chat.controller.ts`, `nginx/nginx.conf`, `charts/continuum-ai/templates/gateway-deployment.yaml`, `charts/continuum-ai/values.yaml`; `DATN-FE/src/app/api/backend/[...path]/route.ts` và `src/app/api/backend/forward.ts`.

## 2. Hai đường dữ liệu có vai trò khác nhau

| Đường | Trách nhiệm | Tính chất |
| --- | --- | --- |
| HTTP qua BFF/Gateway | Tạo hội thoại, gửi/sửa/xóa tin, upload, mark read/delivered, search, history, ticket | Có phản hồi HTTP sau xử lý server; kết quả bền vững ghi MongoDB. |
| WebSocket trực tiếp tới Chat | Báo message/conversation event, typing, presence, trạng thái đọc/nhận | Độ trễ thấp, có thể mất event khi socket/Redis Pub/Sub gián đoạn; không phải nguồn sự thật. |
| HTTP history sau reconnect | Tải lại trang tin và danh sách hội thoại, đối chiếu tin đang hiển thị | Bù những event realtime đã bỏ lỡ từ MongoDB; FE loại tin trùng theo ID. |

FE không gửi message bền vững bằng WebSocket. `ChatWorkspace` lấy ticket qua HTTP, mở socket, nghe event để cập nhật/invalidate TanStack Query, và sau frame `connected` làm mới query Chat. `useChat.ts` tải latest page rồi đi lùi bằng cursor đến tin cũ nhất đang hiển thị để hòa giải cả tin mới, tin sửa/xóa khi offline. Đây là cơ chế phục hồi event mất; không có queue chứa mọi frame WebSocket cho từng client. Nguồn: `DATN-FE/src/components/chat/ChatWorkspace.tsx`, `src/lib/queries/chat/useChat.ts`.

## 3. Gửi tin: độ bền trước, fan-out sau

```mermaid
sequenceDiagram
    participant U as FE
    participant G as BFF/Gateway
    participant C as Chat API
    participant I as IAM
    participant M as MongoDB
    participant R as Redis Pub/Sub
    participant S as Chat replica có người nhận
    U->>G: POST message + clientMessageId
    G->>C: forward request
    C->>I: xác thực actor/Organization ACTIVE
    C->>M: kiểm tra membership, ghi message
    M-->>C: insert/transaction thành công
    C->>R: publish message.created
    R-->>S: cùng event ở các replica
    S-->>U: socket của người nhận online nhận event
    C-->>U: HTTP ACK với message đã lưu
```

Chat xác minh actor qua IAM, member của conversation và block policy trước khi gửi. Message văn bản thường dùng insert với MongoDB write concern `majority`, timeout 5 giây, rồi cập nhật summary tin cuối có điều kiện theo thời gian/ID. Gửi có tệp hoặc reply dùng MongoDB transaction để xác minh/tiêu thụ upload `READY`, kiểm tra reply target, insert message và cập nhật summary nguyên tử. Unique index `{conversationId, senderId, clientMessageId}` chống ghi trùng; cùng ID với payload khác trả conflict. Direct dùng unique `directKey`; room dùng `creationKey` từ `clientRoomId`. HTTP ACK gắn với kết quả ghi, **không đợi** người nhận online hay xác nhận WebSocket. Nguồn: `application/chat.service.ts`, `infrastructure/mongodb/mongo-chat.repository.ts`, `infrastructure/persistence.ts`.

Sau ghi, `ChatRealtimeService.publishConversationEvent()` publish vào một Redis channel chung (`<BULLMQ_PREFIX>:chat:events:v1`, prefix mặc định `continuum`). Lỗi publish bị bắt để tin đã lưu vẫn đọc được. Do đó Redis Pub/Sub ở đây là kênh tín hiệu **at-most-once**, không phải log replay bền vững. `OutboxService` có provider trong module nhưng các lệnh gửi Chat hiện không ghi outbox để replay realtime; `CHAT_QUEUES` hiện là mảng rỗng. Không nên mô tả đường gửi này là BullMQ queue, Kafka hay outbox delivery. Nguồn: `application/chat-realtime.service.ts`, `infrastructure/chat.infrastructure.module.ts`, `infrastructure/persistence.ts`.

## 4. Fan-out nhiều replica: đang làm gì và chi phí thực

Mỗi Chat process giữ các map **cục bộ**: socket theo `(organizationId,userId)`, socket theo conversation đã subscribe, presence watcher và trạng thái session. Redis Pub/Sub chuyển event đến **mọi** Chat replica đang subscribe channel chung. Mỗi replica sau đó chỉ gửi message/conversation event tới socket cục bộ của `recipientIds`; typing chỉ tới socket đã subscribe conversation; presence chỉ tới watcher đủ điều kiện. Không cần sticky session để message đi tới người dùng ở replica khác vì mỗi replica nhận cùng envelope. Khi socket bị đóng, map cục bộ được dọn và client reconnect tới replica sẵn có.

Chi phí hiện tại gần đúng là `số event × số Chat replica` cho việc nhận/lọc envelope nội bộ, cộng `số socket người nhận online` cho fan-out thực. Một room có `R` message/giây và `K` recipient online vẫn cần xấp xỉ `R × K` lần gửi socket; Redis không làm chi phí này biến mất. Thiết kế phù hợp khi replica và room chưa quá lớn, nhưng global Pub/Sub sẽ tăng tải Redis/network/CPU trên **mọi** replica khi traffic tăng. Chưa có node-targeted routing, consistent hashing, shard theo conversation hay relay chuyên biệt. Nguồn: `application/chat-realtime.service.ts` (`publish`, `receive`, `userSockets`, `conversationSockets`, `presenceWatchers`).

## 5. Kết nối, backpressure, typing và presence

- Ticket WebSocket được cấp qua HTTP, ngẫu nhiên 32 byte, TTL tối đa 30 giây, lưu Redis và consume một lần bằng Lua. Ticket đi trong `Sec-WebSocket-Protocol`, không nằm trong query URL. Handshake so khớp token hash/actor/organization với IAM và ticket; `Origin` phải nằm trong `CHAT_ALLOWED_ORIGINS`.
- Gateway dùng NestJS `ws` adapter. Frame tối đa 16 KiB, không bật WebSocket compression. Client có `bufferedAmount > 256 KiB` bị đóng với mã `1013` để tránh queue gửi tăng không giới hạn.
- Mỗi 20 giây server ping socket, kiểm tra token hết hạn/Redis revoke, và revalidate IAM theo cache tối đa 60 giây. Socket không pong hoặc session không còn hợp lệ bị đóng.
- Presence là Redis sorted set lease theo từng session/device, TTL logic 75 giây. User online khi còn lease hợp lệ; heartbeat/pong gia hạn lease, không ghi MongoDB. Presence watch chỉ chấp nhận tối đa 100 user ID và BE thu hẹp về direct contacts có quyền, không broadcast online của cả tổ chức. Watcher nhận snapshot rồi nhận thay đổi; khi lease hết, vòng ping đọc lại trạng thái để phát offline.
- Typing là event tạm, không ghi MongoDB. Server throttle typing-start mỗi socket trong 400 ms; FE tự hết trạng thái typing sau 2,5 giây nếu không có cập nhật.

Nguồn: `controllers/chat-realtime.gateway.ts`, `application/chat-realtime.service.ts`, `application/chat.service.ts`, `infrastructure/redis/redis.service.ts`, `DATN-FE/src/components/chat/ChatWorkspace.tsx`.

## 6. MongoDB và Redis hỗ trợ chịu tải như thế nào

MongoDB database `continuum_chat` sở hữu các collection người dùng `chat_conversations`, `chat_members`, `chat_conversation_messages`, `chat_uploads`, `chat_notifications`, `chat_blocks`, `chat_reports`. `chat_sessions`/`chat_messages` là dữ liệu Cited Assistant riêng, không phải human message timeline. Room member là document riêng, tránh mảng thành viên tăng vô hạn trong conversation. Member lưu `lastDeliveredMessageId/At` và `lastReadMessageId/At` dạng cursor; không tạo một receipt document cho từng cặp message–recipient. Các index quan trọng: unique direct/creation key, unique `(conversationId,userId)`, timeline `(conversationId,createdAt desc,_id desc)`, unique message idempotency key và TTL cho upload metadata. Lịch sử phân trang bằng `(createdAt,_id)` nên không dùng `skip/offset` trên lịch sử dài. Nguồn: `infrastructure/persistence.ts`, `infrastructure/mongodb/mongodb.schemas.ts`, `mongo-chat.repository.ts`.

Redis giữ rate limit cho **mọi route HTTP nghiệp vụ** Chat, ticket một lần, presence lease và Pub/Sub. Repository cache wrapper giữ một số kết quả đọc 15 giây theo actor/organization, tham số và generation; trước cache hit vẫn kiểm tra membership phù hợp. Trang history còn có cache-aside riêng 10 giây theo actor/conversation/cursor và history version. Mutation tăng generation để tránh phục vụ trang cũ. Cache không thay thế MongoDB. Tuy nhiên `ChatTrafficGuard` cần Redis để cho request đi tiếp: cache history có nhánh fallback Mongo khi Redis lỗi, nhưng ở mức HTTP toàn route có thể không tới nhánh đó nếu rate limit guard không dùng được. Đây là giới hạn availability hiện tại, không nên mô tả là Chat HTTP hoạt động đầy đủ khi Redis outage. Nguồn: `controllers/chat-traffic.guard.ts`, `infrastructure/redis/chat-cache.repository.ts`, `application/chat.service.ts`.

Search tên/hội thoại dùng MongoDB Search autocomplete theo tiền tố từ và chuẩn hóa dấu; email dùng range tiền tố theo index; nội dung tin dùng MongoDB Search text với tenant/conversation/sender/date filter. Search across còn lookup membership trước khi trả kết quả. Đây là đường tìm kiếm riêng, không quét `%keyword%` hai đầu trên mọi message. Nguồn: `src/common/search/indexed-search.ts`, IAM candidate search, `mongo-chat.repository.ts`, `mongo-chat-features.ts`.

## 7. Media và tác động lên đường nóng

Ảnh dùng AWS S3, tài liệu dùng Cloudflare R2 qua adapter SDK. FE tạo upload record, stream byte qua BFF/Gateway/Chat; Chat giới hạn số byte theo metadata đã khai, ghi object, `HEAD` xác minh kích thước/MIME khi complete, rồi message tham chiếu upload ID. Download cần kiểm tra membership trước khi cấp signed GET URL 5 phút; ảnh `inline`, tài liệu `attachment`. URL ký được cache ngắn hạn trong Redis. Đường upload đi qua hai HTTP hop có thể tiêu thụ băng thông/connection của BFF và Gateway; Nginx tắt request buffering cho route upload. Đây là cân nhắc tải riêng với fan-out tin nhắn. Nguồn: `application/chat.service.ts`, `infrastructure/storage/s3.storage.ts`, `r2.storage.ts`, Gateway forwarder, FE BFF route, `nginx/nginx.conf`.

## 8. Hành vi khi lỗi và giới hạn mở rộng hiện tại

| Tình huống | Hành vi có trong code | Giới hạn |
| --- | --- | --- |
| Client/socket mất kết nối | FE reconnect backoff + jitter, đăng ký lại, refetch và đồng bộ history. | Event Pub/Sub trong lúc offline không được replay; phải lấy từ MongoDB. |
| Chat process chết | Socket trên process đó mất; presence lease hết hạn và client nối lại. | Chuyển online/offline có thể trễ tới khi lease được phát hiện hết hạn. |
| Redis Pub/Sub publish lỗi sau khi ghi tin | Lỗi bị bắt, message vẫn tồn tại và HTTP có thể trả kết quả. | Người nhận có thể không nhận event tức thời; bù qua HTTP. |
| Redis rate limit/ticket/presence không khả dụng | Guard/ticket/presence phụ thuộc Redis; readiness probe Redis báo không sẵn sàng. | Không thể tuyên bố toàn bộ Chat tiếp tục hoạt động khi Redis outage. |
| MongoDB ghi lỗi | Không có ACK thành công cho tin mới; FE có thể retry cùng ID. | Không có message bền vững để replay nếu MongoDB chưa commit. |
| Socket người nhận chậm | Đóng khi send buffer vượt 256 KiB. | Người nhận phải reconnect và tải bù history. |
| Một room quá nóng hoặc tăng nhiều replica | Mọi replica nhận mọi event từ channel chung rồi lọc; socket fan-out vẫn tỷ lệ số người nhận. | Chưa có node-directed channel, room shard hoặc benchmark công bố. |

Mã hiện có đã đặt nền cho scale ngang bằng service process riêng, ingress WSS trực tiếp, Redis cross-replica và persistence không phụ thuộc socket. **Nó chưa chứng minh chịu tải cao bằng số liệu.** Trước khi nâng replica/room limit cần đo đồng thời: active sockets/replica, memory/socket, event-loop lag, p95/p99 HTTP send→ACK, Mongo majority latency, Redis publish/subscriber lag, event/s theo room, recipient fan-out, reconnect storm và tỷ lệ tải bù. Chỉ khi channel chung hoặc socket fan-out đo được là nút thắt mới có cơ sở tách WebSocket worker/relay hay định tuyến event theo node/conversation; các thành phần đó **chưa được triển khai**.

`DATN-BE/src/services/chat/ARCHITECTURE.md` là tài liệu thiết kế có vài đoạn cũ (ví dụ upload signed PUT trực tiếp và search chuỗi con). Khi khác với code đang chạy, các file runtime nêu ở từng mục trên là nguồn cho tài liệu hiện trạng này. Không có thay đổi application code hay topology triển khai trong tài liệu này.

## 9. Công nghệ và cơ chế đang dùng để bảo đảm chất lượng

Bảng này phân biệt **công nghệ đã có trong đường chạy Chat** với tác dụng thực tế của nó. Phiên bản phụ thuộc được khai báo trong `DATN-BE/package.json` và `DATN-FE/package.json`; cấu hình triển khai có trong Compose/Helm. Một dependency xuất hiện trong manifest chưa có nghĩa Chat đang dùng nó trên đường gửi tin.

| Thuộc tính chất lượng | Công nghệ/cơ chế đang dùng | Tác dụng trong Chat và bằng chứng mã nguồn |
| --- | --- | --- |
| Phân tách trách nhiệm | NestJS 11, TypeScript, module/controller/application service/repository, entrypoint Chat riêng | Gateway forward HTTP; Chat sở hữu business logic, WebSocket và `continuum_chat`. Có thể triển khai/điều chỉnh Chat độc lập với UI. `chat.module.ts`, `main.ts`, `gateway-chat.controller.ts`. |
| Độ bền và tính nhất quán | MongoDB replica set, Mongoose 8, unique/compound/TTL indexes, transaction, majority write concern | Tin nhắn được ghi trước khi phát event; retry dùng unique key; room và tin có file/reply dùng transaction; cursor tránh `skip` lớn. `mongo-chat.repository.ts`, `persistence.ts`, `mongodb.schemas.ts`. |
| Realtime ngang replica | NestJS `@nestjs/platform-ws`/`ws`, Nginx hoặc Kubernetes Ingress WebSocket Upgrade, Redis Pub/Sub qua ioredis | Socket đi thẳng tới Chat; một event được chuyển tới các Chat replica rồi lọc theo socket cục bộ. `service-bootstrap.ts`, `chat-realtime.gateway.ts`, `chat-realtime.service.ts`, `nginx/nginx.conf`, Helm ingress. |
| Bảo vệ bộ nhớ và lưu lượng | `ws` max payload 16 KiB, tắt compression, giới hạn send buffer 256 KiB, Redis rate limit theo actor, phân trang cursor | Chặn frame quá lớn, client quá chậm, request dồn dập và lịch sử trả không giới hạn. `chat-realtime.gateway.ts`, `chat-realtime.service.ts`, `chat-traffic.guard.ts`, `chat.service.ts`. |
| Phục hồi kết nối | WebSocket heartbeat, Redis presence lease, ticket dùng một lần, FE reconnect với backoff/jitter, TanStack Query refetch và `syncMessages` | Mất socket không làm mất message đã lưu; FE đồng bộ từ MongoDB qua HTTP sau reconnect. `chat-realtime.service.ts`, `ChatWorkspace.tsx`, `useChat.ts`. |
| Cô lập tenant và session | IAM service, active Organization Membership, conversation membership, Origin allowlist, token hash/ticket binding, kiểm tra session định kỳ | Chat lấy actor từ IAM; kiểm tra quyền trước cache/history/socket subscribe/download. `chat-iam.client.ts`, `chat-realtime.gateway.ts`, repository Chat. |
| Search có kiểm soát | MongoDB Search index `chat_search_v1`, autocomplete theo tiền tố từ, text search, B-tree prefix cho email | Tìm nhiều từ/không dấu, lọc organization/member và phân trang; không dùng wildcard hai đầu để quét collection. `src/common/search/indexed-search.ts`, Chat/IAM search repositories. |
| Media riêng tư | AWS SDK S3 client/presigner cho ảnh và R2 S3-compatible client cho tài liệu; upload stream có kiểm tra byte và `HEAD` | Bucket không cần public-read; Chat xác minh membership trước signed GET URL, kiểm tra metadata trước gắn file vào tin. `s3.storage.ts`, `r2.storage.ts`, `chat.service.ts`. |
| Trạng thái FE | Next.js 16, React 19, TanStack Query 5, TypeScript | Query/mutation và invalidation tách khỏi local UI state; nhận event xong làm mới dữ liệu, hiển thị loading/error/retry. `useChat.ts`, `features.ts`, `ChatWorkspace.tsx`. |
| Contract và kiểm thử | `docs/openapi/chat-v1.openapi.json`; Jest ở BE, Vitest/React Testing Library ở FE; ESLint và TypeScript check | Có contract route và test cho service, repository, Redis cache/route guard, realtime, composer, workspace, tìm kiếm/highlight. `package.json` hai repo, các file `*.spec.ts(x)`. Đây là khả năng kiểm thử trong repo, không phải bằng chứng load test đã đạt. |
| Health và triển khai | Readiness probe MongoDB/Redis; Docker Compose microservices; Helm Deployment/Service/Ingress | `/internal/health/ready` kiểm tra dependency, chỉ trả HTTP 200 khi cả MongoDB và Redis sẵn sàng. Compose chạy Chat riêng trên port 3005; Helm cấu hình replica nhưng mặc định là 1. `service-bootstrap.ts`, `service-readiness.ts`, `docker-compose.microservices.yml`, Helm chart. |

### Ranh giới chất lượng chưa được chứng minh hoặc chưa nối vào Chat

- `CHAT_QUEUES` đang rỗng: BullMQ có trong dependency/module infrastructure nhưng **không** phân phối message hoặc fan-out Chat hiện tại. `OutboxService` cũng chưa được gọi từ đường gửi tin, nên không có replay bền vững cho Pub/Sub event.
- `MetricsModule` đang được import trong Gateway, **không** thấy import trong `ChatModule`; chưa có metric Chat chuyên biệt trong mã được rà như số socket/replica, fan-out mỗi room, Redis subscriber lag, event-loop lag hoặc p99 send→ACK. Health/readiness không thay thế đo tải.
- Test Jest/Vitest xác minh logic và component, nhưng tài liệu này chưa thấy load test cho nhiều replica, room nóng, reconnect storm hay sự cố Redis/Mongo trong cấu hình giống production. Không suy ra thông lượng hoặc số kết nối tối đa từ package version.
- Manifest Helm cho phép tăng `services.chat.replicas`; muốn tuyên bố chịu tải cao cần chạy benchmark và theo dõi đồng thời độ trễ Mongo majority, CPU/memory Chat, Redis Pub/Sub, socket buffer và tốc độ đồng bộ sau reconnect.
