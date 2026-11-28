# Chat người dùng — Tính năng đã nối FE–BE

> Nằm trong tài liệu kiến trúc tổng thể. Xem [Mục lục](README.md).

Đối chiếu mã nguồn `DATN_FE`, `DATN_BE` và `sag-laya-integration` ngày `28/11/2026` (đồng bộ thêm tính năng `@continuumAI` trong Chat 1–1; OpenAPI Chat v`1.2.0`). “Đã nối” nghĩa là có UI/API client, Gateway, Chat controller/service, SAG internal endpoint và repository/storage tương ứng. Đây là kiểm kê mã nguồn, chưa phải biên bản kiểm thử toàn bộ môi trường triển khai.

## Hội thoại và thành viên

1. Xem danh sách direct/room trong tổ chức hiện tại, gồm tên, avatar, tin cuối, thời gian, số chưa đọc, dấu ghim, trạng thái online của chat 1–1 và khả năng trợ lý (`capabilities.dmAssistantEnabled` ở root `ConversationPage` và trên từng `Conversation` `DIRECT`).
2. Tải thêm hội thoại bằng cursor và lấy chi tiết hội thoại theo ID (`GET /conversations/:conversationId`, kèm `capabilities.dmAssistantEnabled`) khi chưa có trong trang danh sách đã tải.
3. Tìm hội thoại theo tên trên server; xem danh sách lưu trữ, tải thêm và khôi phục hội thoại đã lưu trữ.
4. Tìm thành viên `ACTIVE` cùng tổ chức theo tên nhiều từ, không dấu hoặc tiền tố email; xem trạng thái online trong kết quả.
5. Bắt đầu chat 1–1; cùng một cặp trong tổ chức mở lại hội thoại cũ.
6. Tạo phòng với tên, thành viên được chọn và `clientRoomId` để retry không nhân đôi; tối đa 50 người gồm người tạo.
7. Xem danh sách thành viên/vai trò, đổi tên phòng, thêm nhiều người, xóa thành viên và rời phòng.
8. Chủ phòng bật/tắt quyền quản lý cho thành viên và chuyển quyền sở hữu.
9. Ghim/bỏ ghim hội thoại, lưu trữ/khôi phục, đánh dấu chưa đọc, chọn thông báo tất cả/chỉ khi được nhắc/tắt.

## Tin nhắn

10. Tải lịch sử mới nhất và trang cũ bằng cursor; lấy vùng lịch sử quanh một tin để mở tin gốc.
11. Gửi văn bản hoặc tin chỉ có tệp; dùng `clientMessageId` để retry không tạo bản ghi trùng.
12. Trả lời kèm trích dẫn trong cùng hội thoại, hiển thị người/nội dung gốc và mở tin gốc.
13. Sửa tin của mình, hiển thị dấu đã sửa; xóa mềm tin của mình với bước xác nhận. Tin AI (`authorType: 'ASSISTANT'`) bất biến: thành viên sửa/xóa nhận `403 CHAT_ASSISTANT_MESSAGE_IMMUTABLE` (người ngoài nhận `404`), đồng thời sửa/xóa tin người dùng trong `DIRECT` tăng `contentVersion` và `contextRevision` nguyên tử (`deleteMessage` lặp lại trên tin đã xóa là NOOP).
14. Thả/bỏ reaction từ bộ emoji cho phép, hiển thị số reaction và trạng thái của mình (hỗ trợ cả tin người và tin AI).
15. Ghim/bỏ ghim tin (hỗ trợ cả tin AI trong `library?kind=PIN`) và chuyển tiếp tin người dùng sang hội thoại khác, hiển thị nguồn chuyển tiếp; chặn chuyển tiếp trực tiếp tin AI (`422 CHAT_ASSISTANT_FORWARD_FORBIDDEN`).
16. Nhắc thành viên bằng `@` trong tin gửi hoặc sửa; BE kiểm tra người được nhắc thuộc hội thoại. Riêng mention trợ lý `@continuumAI` tách khỏi `mentionUserIds` và chỉ hợp lệ khi tạo tin mới (`POST`) trên hội thoại `DIRECT`.
17. Lưu, nạp lại và xóa bản nháp theo người dùng/hội thoại sau khi gửi thành công (`GET/PUT /draft` hỗ trợ thêm cờ tùy chọn `assistantMention?: boolean` lưu trong `chat_members.draftAssistantMention` để đồng bộ giữa Full Chat và Mini Chat).

## Tìm kiếm và thư viện

18. Tìm tin trong hội thoại hiện tại, phân trang kết quả, mở ngữ cảnh và cuộn đến tin gốc.
19. Tìm nâng cao trên các hội thoại được phép; tùy chọn giới hạn ở hội thoại đang mở.
20. Lọc theo người gửi, khoảng ngày và loại ảnh/tài liệu/link; tải thêm kết quả bằng cursor.
21. Duyệt thư viện chia sẻ theo ảnh, tài liệu, link, tin ghim; mở tin từ thư viện.
22. BE dùng MongoDB Search autocomplete cho tên/hội thoại, B-tree prefix cho email và text search cho tin; giới hạn theo tổ chức/quyền, không dùng `%...%` hai đầu.

## Media và link

23. Chọn tối đa 10 tệp JPEG/PNG/WebP/GIF, PDF/TXT/CSV/DOCX/XLSX/PPTX; FE kiểm tra sơ bộ, BE xác minh loại/kích thước/upload record.
24. Tạo upload, truyền byte qua BFF/Gateway tới Chat rồi hoàn tất upload; ảnh vào S3, tài liệu vào R2; gửi upload ID cùng tin.
25. BE kiểm tra membership rồi cấp URL có chữ ký ngắn hạn; FE xem ảnh trong bubble, mở/tải tệp và làm mới URL theo thời hạn.
26. URL HTTP(S) trong tin được lưu như văn bản; FE tạo liên kết và thẻ tên miền/đường dẫn. Chưa có API lấy metadata/ảnh Open Graph.

## Trạng thái, thông báo và an toàn

27. Ghi delivered/read cursor; hiển thị đã nhận/đã xem, số người nhận/đọc và bảng receipt theo tin.
28. Xem thông báo Chat có phân trang/số chưa đọc, đánh dấu đã đọc và mở đúng tin từ thông báo.
29. Chặn/bỏ chặn người chat trực tiếp (`setBlock` tăng nguyên tử `chat_conversations.contextRevision` trên hội thoại `DIRECT` để khóa race với worker AI); báo cáo kèm lý do và tùy chọn ID tin.
30. BE xác thực session và `ACTIVE` organization membership qua IAM; kiểm tra membership hội thoại trước khi đọc/ghi/quản trị/tải tệp; Redis rate limit theo actor và tổ chức.

## Realtime và đồng bộ

31. Lấy WebSocket ticket một lần qua HTTP; server kiểm tra Origin, session và tổ chức khi mở socket.
32. Subscribe/unsubscribe hội thoại; nhận event tạo/sửa/xóa tin (`message.created`/`updated`/`deleted`), thay đổi/xóa hội thoại và trạng thái xử lý trợ lý DM **`assistant.status`** chỉ phát tới tập người nhận đã qua lọc `isActiveOrganizationMember(orgId, uid)` (thống nhất với `message.created` và `chat_notifications`), đồng thời `ChatRealtimeService` xác minh lại `(orgId, userId)`, `expiresAt` và `sessionValidations` trước khi đẩy frame ra socket.
33. Gửi/nhận typing; theo dõi presence có giới hạn liên hệ với snapshot và event thay đổi.
34. Nhận thay đổi read/delivered; dùng heartbeat và presence lease cho session online.
35. Reconnect với backoff và jitter; khi kết nối lại, FE đăng ký lại, làm mới query và tải bù lịch sử qua `syncMessages`, loại ID trùng.

## Trợ lý `@continuumAI` trong chat 1–1 (DM Grounded Assistant)

36. **Khám phá khả năng triển khai an toàn (`capabilities.dmAssistantEnabled`):** `GET /conversations` (cấp trang và từng hội thoại) cùng `GET /conversations/:conversationId` trả `capabilities.dmAssistantEnabled = true` chỉ khi hội thoại là `DIRECT`, `CHAT_DM_ASSISTANT_ENABLED=true` và cấu hình đủ `SAG_API_BASE_URL` + `SAG_BFF_SERVICE_TOKEN` (tách khỏi `CHAT_DM_ASSISTANT_WORKER_ENABLED` cho mô hình split API/worker pod; đã nối đầy đủ env parity trên Compose & Helm với mặc định tắt `false`). FE ưu tiên `capabilities.dmAssistantEnabled` từ chi tiết hội thoại tươi (`GET /conversations/:conversationId`) trước bản danh sách cache và lập tức làm mới query hội thoại khi nhận `503 CHAT_AI_NOT_ENABLED`.
37. **Gửi mention có cấu trúc & chống lặp:** `POST /conversations/:conversationId/messages` chấp nhận trường tùy chọn `assistantMention: { handle: 'continuumAI', query?, timezone? }` (chỉ `DIRECT` → `422 CHAT_ASSISTANT_DIRECT_ONLY` với `ROOM`; chỉ tạo mới → `PATCH` trả `422 CHAT_VALIDATION_FAILED`; câu hỏi `1..2000` ký tự → `422 CHAT_ASSISTANT_QUERY_INVALID`; tính năng tắt → `503 CHAT_AI_NOT_ENABLED`; hạn mức riêng `15` lượt/60s → `429 CHAT_ASSISTANT_RATE_LIMITED`). Ghi tin gọi và job `chat_assistant_jobs` trong 1 transaction; replay cùng `clientMessageId` so khớp cả `assistantMention` (`409 CHAT_IDEMPOTENCY_CONFLICT` nếu khác); nút thử lại trên FE giữ ổn định `clientMessageId` theo từng tin gọi xuyên suốt lỗi mạng và bảo toàn `replyToMessageId` gốc của tin gọi mà không ghi đè hay kế thừa nháp reply hiện tại.
38. **Truy xuất 2 chế độ & tổng hợp chỉ trong phạm vi DM:** `DmAssistantRetrievalService` chỉ lấy tin văn bản chưa xóa của người dùng (`authorType != 'ASSISTANT'`) trong đúng `(organizationId, conversationId)` theo `TIME_WINDOW`, `KEYWORD` (Atlas Search `chat_search_v1` → fallback `$text` → fallback quét không dấu tối đa `500` tin, bổ sung lân cận `±2`) hoặc `HYBRID` (mở rộng lân cận dùng `scopedFilter` để bảo toàn tuyệt đối cửa sổ thời gian yêu cầu; tối đa `80` tin / `24.000` ký tự), rồi gọi SAG stateless `POST /api/v1/internal/dm-assistant/answer` có ASGI middleware chặn trước khi parse JSON (`X-SAG-BFF-Service-Token`, 3 header 24-hex, giới hạn `64 KiB` → `413 payload_too_large`), chuẩn RFC 3339/UTC (`Z`), kiểm chứng 1 JSON object + inline `[M#]` (`502`), mẫu `INSUFFICIENT_EVIDENCE` tất định và làm sạch lỗi `422`/`503 llm_unavailable`.
39. **Chống race condition & kiểm tra quyền fail-closed trước khi đăng:** `ChatDmAssistantWorkerService` lọc **mọi người nhận ứng viên** qua `MongoChatOrgMembershipChecker.isActiveOrganizationMember(orgId, uid)` trên từng lượt thử, chạy kiểm tra tuần tự `chat_members`, `chat_blocks` (được đồng bộ bởi `setBlock` tăng nguyên tử `contextRevision`), phiên bản tin gọi và toàn bộ tin ngữ cảnh trên cùng `ClientSession` (0 `Promise.all` chung session), chặn cứng tổng số lượt thực thi transaction ở `MAX_COMMIT_TX_ATTEMPTS = 3` (`CommitConflictExhaustedError`), khóa lạc quan `contextRevision` (Step 5a) và cập nhật đơn điệu `lastMessage*` theo khóa kép `(createdAt, _id)` (Step 5b). Nếu nguồn/tin gọi đổi hoặc bị chặn/mất quyền trước khi đăng → hủy job `CANCELLED` (`SOURCE_CHANGED`, `TRIGGER_DELETED`, `ACCESS_REVOKED`), không đăng tin AI và chỉ phát tán tới người nhận còn quyền IAM.
40. **Thẻ câu trả lời Continuum AI & trạng thái nguồn sống (Authoritative Cache Re-Enrichment):** BE làm giàu theo lô `sourceReferences[].status` (`ACTIVE`, `EDITED`, `DELETED` với `quoteSnippet: ''`) và `assistantMeta.sourceState` mỗi khi đọc, đồng thời hydrate `assistantState` lên tin gọi; trên mọi Redis cache hit (`listMessages`, `messagesAround`, `searchMessages`, `library`, `searchAcross`) có tin AI kèm `sourceReferences` hoặc `assistantState` `PENDING`/`PROCESSING`, BE chạy `reconcileCachedMessages` đọc thẩm quyền từ MongoDB để loại bỏ cửa sổ cache cũ. FE hiển thị `AssistantMessageCard` + `AssistantMarkdownContent` ở cả Full Chat và Mini Chat với trích dẫn `[M#]` bấm nhảy qua `aroundMessageId`, gắn nhãn **Tin nguồn đã sửa** (vẫn mở bản hiện tại) hoặc **Tin nguồn đã xóa** (vô hiệu hóa liên kết), và dùng `mergeAssistantState` đơn điệu + tombstone guard để tách biệt bền vững `PENDING`/`PROCESSING`, `INSUFFICIENT_EVIDENCE`, `CANCELLED` (`SOURCE_CHANGED`/`ACCESS_REVOKED`) và `FAILED` (`SERVICE_UNAVAILABLE`/`TIMEOUT`/`INVALID_MODEL_OUTPUT`).
41. **Bất biến tin AI & đồng bộ cache realtime:** Tin AI đã đăng không thể sửa/xóa (`403 CHAT_ASSISTANT_MESSAGE_IMMUTABLE`) và không thể chuyển tiếp trực tiếp ở v1 (`422 CHAT_ASSISTANT_FORWARD_FORBIDDEN`); vẫn hỗ trợ reaction, reply, pin, report và tìm kiếm chat (người dùng). Cả `ChatWorkspace`, `ChatTools` lẫn `useFloatingChatRealtime`/`MiniChatWindow` lắng nghe `assistant.status` và gọi `invalidateConversationMessageQueries` (phủ `messages`, `context`, `toolsSearch` và `toolsLibrary`) khi nhận `message.updated`/`message.deleted` hoặc sửa/xóa cục bộ.

Đối chiếu: `DATN_FE` (`1170bfc`: `src/lib/queries/chat/{useChat,features,assistant-state}.ts`, `src/components/chat/{ChatWorkspace,ChatTools,ChatDraftComposer,ChatComposer,ChatMessageBubble,AssistantMessageCard,AssistantMarkdownContent,assistant-utils,ChatAttachments,ChatNotifications}.tsx`, `src/components/chat/floating/{FloatingChatDock,MiniChatWindow,useFloatingChatRealtime,chat-shared-helpers}.ts(x)`); `DATN_BE` (DB `31e1dcf` từ `4a19f83`, Chat BE `50955a1`: `src/gateway/gateway-chat.controller.ts`, `src/integrations/ai-engine/http-ai-engine.client.ts`, `src/services/chat/controllers/{chat,chat-features}.controller.ts`, `chat-realtime.gateway.ts`, `src/services/chat/application/{chat,chat-features,chat-realtime,chat-history-cache,chat-dm-assistant.types,chat-dm-assistant-retrieval.service,chat-dm-assistant.worker}.ts`, `src/services/chat/infrastructure/{persistence,redis/chat-cache.repository,mongodb/mongodb.schemas,mongodb/mongo-chat.repository,mongodb/mongo-chat-features,mongodb/mongo-chat-org-membership.checker}.ts`, `docker-compose.microservices.yml`, `charts/continuum-ai/`, `DATN_BE/docs/openapi/chat-v1.openapi.json` v`1.2.0`); `sag-laya-integration` (`8b59296`: `SAG/apps/api/sag_api/{main.py,api/v1/dm_assistant.py,schemas/dm_assistant.py,services/dm_assistant_service.py,generation/llm.py}`, `SAG/docs/openapi/sag-api.openapi.json`); `Dataset` (`f4513a4`: `continuum-dm-ai-dataset/`).
