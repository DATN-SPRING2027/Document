# Chat người dùng — Tính năng đã nối FE–BE

> Nằm trong tài liệu kiến trúc tổng thể. Xem [Mục lục](README.md).

Đối chiếu mã nguồn `DATN-FE` và `DATN-BE` ngày 22/10/2026. “Đã nối” nghĩa là có UI/API client, Gateway, Chat controller/service và repository/storage tương ứng. Đây là kiểm kê mã nguồn, chưa phải biên bản kiểm thử toàn bộ môi trường triển khai.

## Hội thoại và thành viên

1. Xem danh sách direct/room trong tổ chức hiện tại, gồm tên, avatar, tin cuối, thời gian, số chưa đọc, dấu ghim và trạng thái online của chat 1–1.
2. Tải thêm hội thoại bằng cursor và lấy chi tiết hội thoại theo ID khi chưa có trong trang danh sách đã tải.
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
13. Sửa tin của mình, hiển thị dấu đã sửa; xóa mềm tin của mình với bước xác nhận.
14. Thả/bỏ reaction từ bộ emoji cho phép, hiển thị số reaction và trạng thái của mình.
15. Ghim/bỏ ghim tin và chuyển tiếp tin sang hội thoại khác, hiển thị nguồn chuyển tiếp.
16. Nhắc thành viên bằng `@` trong tin gửi hoặc sửa; BE kiểm tra người được nhắc thuộc hội thoại.
17. Lưu, nạp lại và xóa bản nháp theo người dùng/hội thoại sau khi gửi thành công.

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
29. Chặn/bỏ chặn người chat trực tiếp; báo cáo kèm lý do và tùy chọn ID tin.
30. BE xác thực session và `ACTIVE` organization membership qua IAM; kiểm tra membership hội thoại trước khi đọc/ghi/quản trị/tải tệp; Redis rate limit theo actor và tổ chức.

## Realtime và đồng bộ

31. Lấy WebSocket ticket một lần qua HTTP; server kiểm tra Origin, session và tổ chức khi mở socket.
32. Subscribe/unsubscribe hội thoại; nhận event tạo/sửa/xóa tin và thay đổi/xóa hội thoại.
33. Gửi/nhận typing; theo dõi presence có giới hạn liên hệ với snapshot và event thay đổi.
34. Nhận thay đổi read/delivered; dùng heartbeat và presence lease cho session online.
35. Reconnect với backoff và jitter; khi kết nối lại, FE đăng ký lại, làm mới query và tải bù lịch sử qua `syncMessages`, loại ID trùng.

Đối chiếu: `DATN-FE/src/lib/queries/chat/useChat.ts`, `features.ts`, `src/components/chat/ChatWorkspace.tsx`, `ChatTools.tsx`, `ChatDraftComposer.tsx`, `ChatAttachments.tsx`, `ChatNotifications.tsx`; `DATN-BE/src/gateway/gateway-chat.controller.ts`, `src/services/chat/controllers/chat.controller.ts`, `chat-features.controller.ts`, `chat-realtime.gateway.ts`, `src/services/chat/application/`, `src/services/chat/infrastructure/`.
