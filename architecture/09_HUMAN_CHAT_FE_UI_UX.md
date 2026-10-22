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

12. Gom các tin liên tiếp cùng người gửi thành nhóm; chỉ hiện tên người gửi và thời gian ở vị trí cần thiết; căn bubble theo phía người gửi.
13. Hiển thị nhãn đã sửa, tin đã xóa, tin được ghim, nguồn chuyển tiếp và phần trích dẫn reply; nhấn trích dẫn để đi tới tin gốc.
14. Toolbar thao tác tin hiện khi hover/focus trên desktop; menu được đặt gần nút mở, giới hạn trong viewport và đóng khi click ngoài, cuộn, resize hoặc Escape.
15. Sửa tin ngay trong bubble; xác nhận trước khi xóa; chọn emoji reaction và bấm lại reaction đã có để bỏ.
16. Hiển thị delivered/seen của tin mình gửi và số người đã nhận/đọc; thời gian hiển thị theo locale của trình duyệt.

## Soạn tin và media

17. Ô nhập nhiều dòng tự tăng chiều cao; Enter gửi, Shift+Enter xuống dòng; nút gửi bị khóa khi không có nội dung/tệp hoặc đang gửi.
18. Gợi ý `@` từ danh sách thành viên đã tải, giới hạn số gợi ý; hiện trích dẫn khi trả lời và có nút hủy reply.
19. Chọn nhiều tệp; hiển thị thumbnail ảnh bằng object URL, tên tệp, dung lượng và nút bỏ từng tệp; giải phóng object URL khi bỏ/gửi/rời composer.
20. Kiểm tra sơ bộ số lượng, kích thước và loại tệp trước upload; giữ `clientMessageId`/upload ID cho cùng lần gửi khi retry.
21. Nhận diện URL HTTP(S), tránh URL có username/password, render anchor mở tab mới với `rel="noopener noreferrer"`; hiện tối đa ba thẻ link chỉ gồm tên miền/đường dẫn. Không có tải metadata website.
22. Ảnh đã gửi được render trong bubble từ URL ký do BE trả; tài liệu hiển thị tên/dung lượng và thao tác mở/tải; hiện trạng thái đang tải hoặc lỗi khi URL không lấy được.

## Realtime và thông báo phía trình duyệt

23. Hiển thị typing của một, hai hoặc nhiều người; tự xóa trạng thái typing khi không nhận cập nhật tiếp.
24. Cập nhật TanStack Query cache khi nhận event, loại tin trùng ID, làm mới phần dữ liệu cần thiết và hiển thị kết nối/đang kết nối lại.
25. Thông báo hệ điều hành chỉ hiện khi đã cấp quyền, tab không ở foreground và có thông báo mới; nội dung lock screen chỉ dùng tên người gửi, không đưa thân tin lên đó.

Các thành phần này nằm chủ yếu trong `DATN-FE/src/components/chat/ChatWorkspace.tsx`, `ChatMessageBubble.tsx`, `ChatComposer.tsx`, `ChatSearchResults.tsx`, `HighlightedText.tsx`, `MessageContent.tsx`, `message-layout.ts` và `ChatNotifications.tsx`.
