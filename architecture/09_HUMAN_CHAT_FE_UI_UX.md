# Chat người dùng — Tính năng UI/UX tại FE

> Nằm trong tài liệu kiến trúc tổng thể. Xem [Mục lục](README.md).

Các xử lý giao diện này không cần API riêng. Dữ liệu hội thoại, tin nhắn và quyền hiển thị vẫn đến từ backend.

## Bố cục, trạng thái và trợ năng

1. Bố cục hai cột danh sách/hội thoại trên màn hình rộng; màn hình nhỏ chuyển giữa danh sách và hội thoại với nút quay lại.
2. Chế độ sáng/tối; avatar ảnh với fallback chữ khi thiếu URL hoặc ảnh lỗi; màu và vị trí bubble phân biệt tin của mình và người khác.
3. Tên hội thoại có thể xuống hai dòng; hiển thị preview tin cuối, thời gian, badge chưa đọc, trạng thái online và kết nối WebSocket.
4. Skeleton cho danh sách và lịch sử; trạng thái trống, lỗi, đang tải, nút thử lại; vô hiệu hóa nút trong lúc thao tác gửi/sửa/xóa.
5. Dialog và panel cạnh có tiêu đề, focus khi mở, giữ Tab trong panel, Escape/đóng và trả focus về nút kích hoạt; modal có nền mờ vừa phải.
6. Nhãn ẩn cho ô nhập/nút icon, `aria-live` cho kết quả tìm kiếm, `aria-pressed` cho bộ lọc/reaction và dấu focus khi dùng bàn phím.

## Danh sách, tìm kiếm và điều hướng

7. Debounce 250 ms cho ô tìm người, hội thoại và tin nhắn trước khi gọi API; ô tìm kiếm không tự duyệt toàn bộ dữ liệu đã tải để giả làm kết quả server.
8. Trạng thái chọn hội thoại, mở trực tiếp hội thoại/tin từ URL query hoặc thông báo, quay về lịch sử mới nhất khi đang xem vùng quanh tin cũ.
9. Cuộn đến tin được chọn, focus và tô vòng sáng trong thời gian ngắn; giữ vị trí viewport khi nạp lịch sử cũ ở đầu danh sách.
10. Highlight từ khóa kết quả tìm kiếm theo nhiều từ, không dấu và không phân biệt hoa/thường; rút gọn preview dài, có nút mở ngữ cảnh tin gốc.
11. Hiển thị loading/empty/error/tải thêm riêng cho kết quả tìm kiếm, thư viện chia sẻ, hội thoại lưu trữ và danh sách chuyển tiếp.

## Bubble và thao tác tin

12. Gom các tin liên tiếp cùng người gửi thành nhóm; chỉ hiện tên người gửi và thời gian ở vị trí cần thiết; căn bubble theo phía người gửi. Tin AI (`authorType: 'ASSISTANT'`) không bao giờ gộp nhóm với tin người (`sameMessageGroup` trả `false`) và luôn hiển thị nhãn/card **Continuum AI** tách biệt ở cả Full Chat và Mini Chat.
13. Hiển thị nhãn đã sửa, tin đã xóa, tin được ghim, nguồn chuyển tiếp và phần trích dẫn reply; nhấn trích dẫn để đi tới tin gốc. Với tin AI (`AssistantMessageCard`, `AssistantMarkdownContent`), render nội dung markdown có cấu trúc trong thẻ editorial nền trắng nâng tầng kèm dải nhấn thương hiệu bên mép dẫn và badge trích dẫn inline `[M#]`; danh sách tin nguồn được **thu gọn mặc định sau nút pill/icon dropdown** (`Tin nguồn (N)` / `Sources (N)`, mở rộng khi bấm hoặc đóng bằng `Escape`, kèm chấm báo khi có nguồn thay đổi): bên trong dropdown, `ACTIVE` bấm nhảy tới tin gốc (`aroundMessageId`), `EDITED` gắn nhãn **Tin nguồn đã sửa** và vẫn mở bản hiện tại, `DELETED` gắn nhãn **Tin nguồn đã xóa** và vô hiệu hóa nút bấm.
14. Toolbar thao tác tin hiện khi hover/focus trên desktop; menu được đặt gần nút mở, giới hạn trong viewport và đóng khi click ngoài, cuộn, resize hoặc Escape. Trên tin AI, ẩn các hành động không hợp lệ (`Sửa`, `Xóa`, `Chuyển tiếp`, `Xem đã nhận/đọc`) và giữ `Reaction`, `Trả lời`, `Ghim`, `Báo cáo`.
15. Sửa tin ngay trong bubble; xác nhận trước khi xóa; chọn emoji reaction và bấm lại reaction đã có để bỏ. Dưới tin người dùng đã gọi `@continuumAI`, hiển thị pill suy nghĩ gọn kèm **3 dấu chấm uốn lượn** (`cu-ai-wave-dot`, tôn trọng `prefers-reduced-motion`) cho `PENDING`/`PROCESSING`, cùng thẻ trạng thái tách biệt cho `CANCELLED` (`SOURCE_CHANGED`, `ACCESS_REVOKED`), `FAILED` (`SERVICE_UNAVAILABLE`/`TIMEOUT`/`INVALID_MODEL_OUTPUT`) kèm nút thử lại câu hỏi (dùng `clientMessageId` ổn định theo từng tin gọi xuyên suốt lỗi mạng, chỉ xoay vòng sau HTTP `201`, và giữ nguyên `replyToMessageId` gốc của tin gọi mà không kế thừa hay xóa nháp reply đang mở trong ô soạn); câu trả lời `INSUFFICIENT_EVIDENCE` hiển thị nhãn thiếu căn cứ và gợi ý hỏi cụ thể hơn.
16. Hiển thị delivered/seen của tin mình gửi và số người đã nhận/đọc; thời gian hiển thị theo locale của trình duyệt.

## Soạn tin và media

17. Ô nhập nhiều dòng tự tăng chiều cao; Enter gửi, Shift+Enter xuống dòng; nút gửi bị khóa khi không có nội dung/tệp hoặc đang gửi; kiểm tra `isComposing` (`compositionstart`/`compositionend`) để phím Enter không cắt dở dấu bộ gõ tiếng Việt (Telex/VNI).
18. Gợi ý `@` từ danh sách thành viên đã tải, giới hạn số gợi ý; trong hội thoại `DIRECT` có `capabilities.dmAssistantEnabled === true` (tính thống nhất trên cả Full Chat và Mini Chat bằng `resolveFreshDmAssistantCapability` theo độ tươi `dataUpdatedAt` giữa query `detail` đang bật và `list`, ưu tiên `list` khi `detail` bị tắt/cũ hơn, xử lý fail-closed `false` khi mốc thời gian bằng nhau/không rõ, và tự invalidate `conversations` + `conversation` khi nhận `CHAT_AI_NOT_ENABLED`), bổ sung mục **`@continuumAI`** hỗ trợ điều hướng bàn phím (`ArrowUp`/`ArrowDown` tự `scrollIntoView({ block: 'nearest' })` tới mục đang chọn, `Enter`/`Tab`/`Escape`), đồng bộ trạng thái `assistantMention` qua draft giữa Full Chat và Mini Chat, và bảo toàn `clientMessageId` theo fingerprint khi gửi lại sau lỗi mạng; hiện trích dẫn khi trả lời và có nút hủy reply.
19. Chọn nhiều tệp; hiển thị thumbnail ảnh bằng object URL, tên tệp, dung lượng và nút bỏ từng tệp; giải phóng object URL khi bỏ/gửi/rời composer.
20. Kiểm tra sơ bộ số lượng, kích thước và loại tệp trước upload; giữ `clientMessageId`/upload ID cho cùng lần gửi khi retry.
21. Nhận diện URL HTTP(S), tránh URL có username/password, render anchor mở tab mới với `rel="noopener noreferrer"`; hiện tối đa ba thẻ link chỉ gồm tên miền/đường dẫn. Không có tải metadata website.
22. Ảnh đã gửi được render trong bubble từ URL ký do BE trả; tài liệu hiển thị tên/dung lượng và thao tác mở/tải; hiện trạng thái đang tải hoặc lỗi khi URL không lấy được.

## Realtime và thông báo phía trình duyệt

23. Hiển thị typing của một, hai hoặc nhiều người; tự xóa trạng thái typing khi không nhận cập nhật tiếp.
24. Cập nhật TanStack Query cache khi nhận event (`message.*`, `conversation.*`, `assistant.status`), loại tin trùng ID, áp dụng hàm dùng chung `mergeMessage` đơn điệu trên cả Full Chat và Mini Chat — giữ ưu thế tombstone xóa (không cho phản hồi `POST`/WS/refetch đến trễ hồi sinh nội dung đã xóa và luôn xóa sạch `assistantState: undefined` trên tin gọi đã xóa), giữ ưu thế bản sửa mới hơn theo `contentVersion`/`editedAt`, kết hợp `mergeAssistantState` đơn điệu (`PENDING < PROCESSING < TERMINAL`) kèm tombstone guard (LRU 256 / TTL 5 phút) để sự kiện trễ không bao giờ kéo lùi trạng thái đã kết thúc; gọi `invalidateConversationMessageQueries` (phủ cả `messages`, `context`, `toolsSearch` và `toolsLibrary` của `ChatTools`) khi tin nguồn bị sửa/xóa để cập nhật ngay trạng thái chip nguồn trên Full Chat, bảng tìm kiếm/ghim và Mini Chat, đồng thời hiển thị kết nối/đang kết nối lại.
25. Thông báo hệ điều hành chỉ hiện khi đã cấp quyền, tab không ở foreground và có thông báo mới; nội dung lock screen chỉ dùng tên người gửi, không đưa thân tin lên đó.

Các thành phần này nằm chủ yếu trong `DATN_FE` (`08894a9`): `src/lib/queries/chat/{useChat,features,assistant-state}.ts`, `src/components/chat/{ChatWorkspace,ChatTools,ChatMessageBubble,AssistantMessageCard,AssistantMarkdownContent,assistant-utils,ChatComposer,ChatDraftComposer,ChatSearchResults,HighlightedText,MessageContent,message-layout,ChatNotifications}.tsx` và `src/components/chat/floating/{FloatingChatDock,MiniChatWindow,useFloatingChatRealtime,chat-shared-helpers}.ts(x)`.
