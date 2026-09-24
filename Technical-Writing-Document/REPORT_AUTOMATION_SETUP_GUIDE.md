# HƯỚNG DẪN THIẾT LẬP VÀ VẬN HÀNH HỆ THỐNG TỰ ĐỘNG HÓA BÁO CÁO
*(Hệ thống Độc lập hoàn toàn trong Repository `Document` — Dành cho AI Agent và 5 Thành viên)*

---

## 1. MỤC TIÊU VÀ TỔNG QUAN HỆ THỐNG

Toàn bộ hệ thống quản lý tài liệu và xuất bản báo cáo tốt nghiệp của đồ án **Continuum AI** được đặt tập trung, độc lập 100% trong repository `Document`. 

Nhóm áp dụng phương pháp **Docs-as-Code (Tài liệu hóa bằng lập trình)**:
* **Nội dung đặc tả gốc:** Được viết và quản lý bằng **Markdown (`.md`)** tại `Submit-Report/`.
* **Sơ đồ kiến trúc & luồng:** Được thiết kế và lưu dạng XML tiêu chuẩn bằng **Draw.io (`.drawio`)** tại `Output-DrawIo/`.
* **Bộ máy tự động hóa (Engine):** Sử dụng các script Python trong `build/` (kết hợp `python-docx` và `docxtpl`) để tự động ráp nội dung, căn lề 15.9cm chuẩn mẫu trường, tô màu bảng biểu (`FFE8E1`), đánh số hình ảnh tự động và xuất bản trực tiếp ra file Word `.docx` hoàn chỉnh tại `Submit-Report/`.

---

## 2. CẤU TRÚC THƯ MỤC TRONG `Document/Technical-Writing-Document`

```
Document/Technical-Writing-Document/
├── README.md                                 # Mục lục và giới thiệu tổng quan
├── REPORT_AUTOMATION_SETUP_GUIDE.md          # Hướng dẫn setup và vận hành (File này)
├── DOCUMENT_CONTRIBUTION_LOG.md              # Quy tắc danh tính 5 người & Nhật ký đóng góp
├── Quy định lưu ý khi làm report.docx        # Quy chuẩn trình bày báo cáo của trường
│
├── build/                                    # BỘ MÁY TỰ ĐỘNG HÓA XUẤT BÁO CÁO
│   ├── docx_lib.py                           # Thư viện lõi điều khiển định dạng Word OpenXML
│   ├── diagrams.py                           # Tự động xuất hình ảnh từ sơ đồ
│   ├── build_report1.py                      # Script xuất Report 1 (Project Introduction)
│   ├── build_report2.py                      # Script xuất Report 2 (Project Management Plan)
│   └── figs/                                 # Kho hình ảnh chèn vào báo cáo
│
├── Output-DrawIo/                            # KHO SƠ ĐỒ CHUẨN (XML / .drawio)
│   ├── 01_context_diagram_dfd0_standard.drawio
│   ├── 02_usecase_overall.drawio
│   ├── 03_usecase_authentication.drawio
│   ├── 04_usecase_admin.drawio
│   ├── 05_usecase_team_leader.drawio
│   ├── 06_usecase_member.drawio
│   ├── 07_screenflow_admin.drawio
│   ├── 08_screenflow_team_leader.drawio
│   ├── 09_screenflow_member.drawio
│   └── 10_erd.drawio
│
├── Sample-Report/                            # TÀI LIỆU MẪU & CHECKLIST CHẤM ĐIỂM
│   ├── 1614_DN_SE_01_Report1_...docx         # Mẫu bìa, font, style chuẩn
│   ├── 1614_DN_SE_01_Report2_...docx
│   ├── ... (các mẫu từ Report 1 đến Report 7)
│   └── Checklist_CapstoneProjectReview1_2_3.xlsx # Bảng tiêu chí chấm Review 1, 2, 3
│
└── Submit-Report/                            # KHU VỰC CHỨA SẢN PHẨM HOÀN CHỈNH
    ├── Continuum_AI_Report1_Project_Introduction.docx
    ├── Continuum_AI_Report2_Project_Management_Plan.docx
    └── Continuum_AI_Report3_Software_Requirement_Specification.md
```

---

## 3. HƯỚNG DẪN THIẾT LẬP MÔI TRƯỜNG CHO 5 THÀNH VIÊN & AI

Chỉ cần cài đặt các thư viện Python một lần duy nhất trên máy:
```bash
pip install python-docx docxtpl openpyxl lxml
```
*(Nếu cần nghiên cứu thêm các module bóc tách tài liệu thông minh cho Module 3.9, cài thêm: `pip install docling markitdown`)*

---

## 4. QUY TRÌNH VẬN HÀNH DÀNH CHO AI VÀ THÀNH VIÊN

Khi nhận lệnh cập nhật tài liệu hoặc sinh file Word:

1. **Bước 1 — Xác định danh tính:** Hỏi người đang thực hiện là ai trong 5 thành viên (**Phúc, Thắng, Danh, Tài, Tiên**).
2. **Bước 2 — Cập nhật nội dung gốc:**
   * Cập nhật nội dung đặc tả tại `Submit-Report/Continuum_AI_Report3_Software_Requirement_Specification.md`.
   * Cập nhật hoặc tạo sơ đồ mới tại `Output-DrawIo/*.drawio`.
3. **Bước 3 — Chạy lệnh biên dịch ra Word:**
   Mở terminal tại thư mục `Document/Technical-Writing-Document/build` và chạy:
   ```bash
   # Build Report 1:
   python build_report1.py

   # Build Report 2:
   python build_report2.py
   ```
4. **Bước 4 — Kiểm tra file đầu ra & Ghi nhật ký:**
   * File Word `.docx` xuất bản sẽ nằm trực tiếp tại `Submit-Report/`.
   * Thêm một dòng ghi nhận công việc vào `DOCUMENT_CONTRIBUTION_LOG.md`.
