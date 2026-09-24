# WORKFLOW VIẾT TÀI LIỆU ĐỒ ÁN CONTINUUM AI

---

## TỔNG QUAN

```
① Nhận Task
     │
② Tra bảng QUY_DINH_LUU_Y_KHI_LAM_REPORT.md
     │  → Biết task thuộc Loại nào (1–5)
     │  → Biết phải viết vào file nào trong 7 Reports
     │
③ Viết nháp vào folder cá nhân (members/<tên>/)
     │
④ Chuyển nội dung sang file chính thức + Mở PR
     │
⑤ PM Review & Merge
     │
⑥ Chạy script xuất Word (nếu cần)
     │
⑦ Ghi nhật ký vào DOCUMENT_CONTRIBUTION_LOG.md
```

---

## CHI TIẾT TỪNG BƯỚC

### ① Nhận Task
- Bạn nhận một task từ Jira / GitHub Project / nhóm chat.
- Xác nhận mình là ai: **Phúc / Thắng / Danh / Tài / Tiên**.

### ② Tra bảng QUY_DINH để biết viết vào đâu
Mở [QUY_DINH_LUU_Y_KHI_LAM_REPORT.md](QUY_DINH_LUU_Y_KHI_LAM_REPORT.md) và xác định:

| Task thuộc loại... | Thì viết vào... |
| :--- | :--- |
| **Loại 1:** Task Tính năng (Feature) | Report 3 (SRS) + Report 4 (SDD) + Report 5 (Test) + Report 6 (User Guide) |
| **Loại 2:** Task Kỹ thuật & Tích hợp | Report 3 (External Interface) + Report 4 (Architecture) + Report 5 (Unit Test) |
| **Loại 3:** Task Hạ tầng & DevOps | Report 2 (PMP Tools) + Report 4 (Deployment) + Report 6 (Install Guide) |
| **Loại 4:** Task Nghiên cứu AI | Report 1 (Intro) + Report 4 (Algorithm) + Checklist (Rubric AI) |
| **Loại 5:** Task Sửa lỗi & Tối ưu | Report 5 (Bug Tracking) + Report 7 (Lessons Learned) |

### ③ Viết nháp vào folder cá nhân
Mỗi người có folder riêng tại `members/`:
```
members/
├── phuc/
├── thang/
├── danh/
├── tai/
└── tien/
```
Đặt bản nháp, ảnh chụp, ghi chú nghiên cứu vào folder cá nhân của mình.

### ④ Chuyển nội dung sang file chính thức + Mở PR
Khi bản nháp đã ổn:
1. Tạo nhánh Git: `git checkout -b doc/<tên>-<mô-tả-ngắn>`
2. Chuyển nội dung vào đúng file chính thức:

| Nội dung | File đích | Thư mục |
| :--- | :--- | :--- |
| Use Case, Luồng nghiệp vụ | `Continuum_AI_Report3_...md` | `Submit-Report/` |
| Sơ đồ Context, Use Case, Screen Flow, ERD | `*.drawio` | `Output-DrawIo/` |
| Thiết kế kiến trúc, CSDL | Report 4 `.docx` | `Submit-Report/` |
| Test Case, Bug Tracking | Report 5 `.xlsx` | `Submit-Report/` |
| Hướng dẫn sử dụng | Report 6 `.docx` | `Submit-Report/` |

3. Push và mở Pull Request trên GitHub.

### ⑤ PM Review & Merge
Người quản lý tài liệu kiểm tra:
- Nội dung có khớp với bảng tra cứu QUY_DINH không?
- Định dạng Markdown / bảng biểu có chuẩn không?
- Sơ đồ Draw.io có giữ đúng style chung không?

Ổn → Merge. Cần sửa → Comment trên PR.

### ⑥ Xuất Word (khi cần nộp bài)
```bash
cd Document/Technical-Writing-Document/build/
python build_report1.py    # Report 1
python build_report2.py    # Report 2
```
File `.docx` xuất tại `Submit-Report/`.

### ⑦ Ghi nhật ký đóng góp
Thêm một dòng vào [DOCUMENT_CONTRIBUTION_LOG.md](DOCUMENT_CONTRIBUTION_LOG.md):
```
| [Ngày] | [Tên] | [Task đã làm] | [File tác động] | [Nội dung] | [PR/Commit] | [Trạng thái] |
```

---

## CẤU TRÚC THƯ MỤC

```
Document/Technical-Writing-Document/
│
├── README.md                                  # Mục lục tổng quan
├── WORKFLOW.md                                # Quy trình làm việc (File này)
├── QUY_DINH_LUU_Y_KHI_LAM_REPORT.md         # Bảng tra cứu Task → File
├── REPORT_AUTOMATION_SETUP_GUIDE.md           # Hướng dẫn setup script Python
├── DOCUMENT_CONTRIBUTION_LOG.md               # Nhật ký đóng góp
│
├── members/                                   # Folder cá nhân 5 thành viên
│   ├── phuc/
│   ├── thang/
│   ├── danh/
│   ├── tai/
│   └── tien/
│
├── build/                                     # Script tự động xuất Word
├── Output-DrawIo/                             # Kho sơ đồ Draw.io
├── Sample-Report/                             # File mẫu & Checklist
└── Submit-Report/                             # File nộp bài chính thức
```
