# Luồng chọn Organization sau khi đăng nhập

**Trạng thái:** Hành vi giao diện được Thang xác nhận ngày 2026-10-15.
**Phạm vi:** Đăng nhập người dùng sản phẩm Organization bằng mật khẩu hoặc Google.
**Phân biệt:** Đây là quyết định về thời điểm chọn workspace; không đổi điều
kiện membership hoặc quyền Platform.

## Quyết định

Sau khi xác thực thành công, ứng dụng luôn đưa người dùng sản phẩm Organization
đến màn hình chọn Organization, không phụ thuộc phương thức đăng nhập, số
Organization hoặc role của người dùng.

- Chưa có Organization đang ACTIVE: màn hình hiển thị trạng thái rỗng và nút
  tạo Organization.
- Có một Organization đang ACTIVE: vẫn hiển thị màn hình chọn với Organization
  đó và nút `Create Organization` để tạo thêm workspace.
- Có nhiều Organization đang ACTIVE: hiển thị toàn bộ Organization người dùng
  có quyền tham gia và vẫn cho phép tạo Organization mới.
- Người dùng chỉ thấy Organization có membership `ACTIVE`; role của họ không
  làm thay đổi danh sách. Role và permission vẫn được BE xác minh trong từng
  Organization.
- Chọn Organization sẽ được BE kiểm tra membership `ACTIVE` lần nữa trước khi
  cấp session theo Organization.
- Platform Operator đăng nhập qua luồng Platform riêng, không sử dụng màn hình
  chọn Organization này.

Hành vi này thay thế quy tắc đăng nhập cũ tự chọn Organization duy nhất và chỉ
yêu cầu chọn tường minh khi có nhiều Organization. Quy tắc cũ về việc chỉ
membership `ACTIVE` mới đủ điều kiện thiết lập Organization Context vẫn được
giữ nguyên. Nút tạo Organization luôn sẵn sàng ở màn hình chooser; tài khoản
tạo trở thành Organization `ADMIN` đầu tiên trong cùng giao dịch provisioning.
Không tạo membership hoặc role chỉ vì đăng nhập.

## Luồng BE/FE

1. FE gọi API đăng nhập mật khẩu hoặc bắt đầu Google OAuth qua BFF.
2. Khi không có Organization được yêu cầu rõ ràng, BE tạo session `ACCOUNT`
   không mang `organizationId` hoặc role. Việc xác thực account, trạng thái
   account, MFA và rate limit vẫn giữ nguyên.
3. FE mở `/select-organization` và gọi API liệt kê các Organization có
   membership `ACTIVE`.
4. Người dùng có thể tạo Organization dù danh sách hiện tại đang rỗng hay đã có
   Organization. BE tạo Organization, membership `ACTIVE` và role assignment
   `ADMIN` cho tài khoản tạo trong cùng giao dịch; FE chọn Organization mới sau
   khi tạo thành công.
5. Khi người dùng chọn, FE gọi API chọn Organization có CSRF token. BE xác minh
   session và membership đích rồi cấp session Organization-scoped.
6. FE tải workspace trong context mới.

## Acceptance

- Xác minh đăng nhập mật khẩu và Google đều đến màn hình chọn Organization.
- Xác minh tài khoản có 0, 1 và nhiều Organization đều mở đúng cùng màn hình.
- Xác minh một role Organization không làm ẩn Organization khác có membership
  `ACTIVE`.
- Xác minh membership không còn `ACTIVE` không thể được chọn để lấy context.
- Xác minh session Platform bị từ chối ở API Organization chooser.
- Xác minh tài khoản không có membership và tài khoản đã có Organization đều
  nhìn thấy hành động tạo Organization.
- Xác minh creator có membership `ACTIVE` và role `ADMIN` ở Organization vừa
  tạo trước khi FE chuyển vào workspace.

## Ảnh hưởng

- Cần triển khai đồng bộ contract BE và điều hướng FE.
- Không đổi schema, collection, index, migration hoặc dữ liệu.
- Không đổi ranh giới tenant, membership, permission hoặc Platform authority.
