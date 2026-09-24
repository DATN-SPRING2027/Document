# NHẬT KÝ VÀ QUY TẮC ĐÓNG GÓP TÀI LIỆU DỰ ÁN CONTINUUM AI

---

## ⚠️ QUY TẮC BẮT BUỘC DÀNH CHO AI AGENT

> **MỖI KHI BẮT ĐẦU PHIÊN LÀM VIỆC HOẶC NHẬN YÊU CẦU CẬP NHẬT TÀI LIỆU:**
> 
> AI phải hỏi: *"Bạn là ai trong 5 thành viên của nhóm?"*
> 1. **Phúc**
> 2. **Thắng**
> 3. **Danh**
> 4. **Tài**
> 5. **Tiên**
> 
> Sau khi xác định danh tính, AI mới thực hiện công việc và ghi tên người đó vào bảng nhật ký bên dưới.

---

## 1. NGUYÊN TẮC PHÂN CÔNG

Nhóm **không phân chia module cố định** cho từng người. Thay vào đó:
- Ai nhận task nào thì làm task đó **từ đầu tới cuối** (code + viết tài liệu).
- Khi nhận task, tra bảng trong [QUY_DINH_LUU_Y_KHI_LAM_REPORT.md](QUY_DINH_LUU_Y_KHI_LAM_REPORT.md) để biết task thuộc loại nào → mở đúng file nào để viết.

---

## 2. DANH SÁCH 5 THÀNH VIÊN

| STT | Thành viên | Folder cá nhân (viết nháp) |
| :---: | :--- | :--- |
| 1 | **Phúc** | [`members/phuc/`](members/phuc/) |
| 2 | **Thắng** | [`members/thang/`](members/thang/) |
| 3 | **Danh** | [`members/danh/`](members/danh/) |
| 4 | **Tài** | [`members/tai/`](members/tai/) |
| 5 | **Tiên** | [`members/tien/`](members/tien/) |

---

## 3. BẢNG NHẬT KÝ ĐÓNG GÓP TÀI LIỆU (DOCUMENT CONTRIBUTION LOG)

Mỗi khi có thay đổi về tài liệu, **phải thêm một dòng vào bảng dưới đây**:

| Ngày | Người thực hiện | Task đã làm | File / Mục tác động | Nội dung thay đổi | Bằng chứng (PR / Commit) | Trạng thái |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| 22/09/2026 | **Phúc** | Khởi tạo SRS | `Submit-Report/Report3_SRS.md` | Tạo khung đặc tả yêu cầu phần mềm | Commit trong repo | Approved |
| 23/09/2026 | **Phúc** | Vẽ sơ đồ hệ thống | `Output-DrawIo/` | Vẽ Context, Use Case, Screen Flow, ERD | 10 file `.drawio` | Approved |
| 24/09/2026 | **Phúc** | Thiết lập workspace tài liệu | `Technical-Writing-Document/` | Chuyển xưởng tự động hóa + tạo folder 5 thành viên + viết Workflow | Commit trong repo | Approved |
| *[Ngày]* | *[Phúc / Thắng / Danh / Tài / Tiên]* | *[Tên task đã làm]* | *[File tài liệu]* | *[Mô tả nội dung]* | *[Link PR hoặc Commit]* | *[Draft / Approved]* |

---

## 4. QUY TRÌNH KIỂM DUYỆT

1. Thành viên viết nháp trong `members/<tên>/`, khi xong chuyển nội dung sang file chính thức và mở PR.
2. Người quản lý tài liệu review PR trên GitHub, merge vào `main`.
3. Cập nhật trạng thái thành `Approved` trong bảng trên.
