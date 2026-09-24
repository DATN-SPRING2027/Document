# QUY ĐỊNH VÀ HƯỚNG DẪN VIẾT TÀI LIỆU KHI NHẬN TASK
*(Dành cho AI Agent và 5 Thành viên: Phúc, Thắng, Danh, Tài, Tiên)*

Tài liệu này quy định quy trình chuẩn để khi bất kỳ thành viên nào (hoặc AI hỗ trợ) nhận một task lập trình, sẽ biết chính xác **phải mở file nào, viết vào mục nào, và cần những bằng chứng gì**.

---

## 1. BẢNG TRA CỨU: LOẠI TASK $\rightarrow$ MỞ FILE NÀO ĐỂ VIẾT?

| Loại Task được giao | Ví dụ thực tế trong dự án Continuum AI | Mở File nào trong `Submit-Report/` hoặc `Sample-Report/`? | Mục cụ thể cần viết |
| :--- | :--- | :--- | :--- |
| **Loại 1: Task Tính năng / Nghiệp vụ**<br>*(Feature / Functional Task)*<br>$\rightarrow$ *Chiếm ~70% khối lượng* | • Làm tính năng Soạn thảo ghi chú (Daily Note)<br>• Làm tính năng Bàn giao (Handover)<br>• Làm tính năng Đăng nhập & Phân quyền RBAC | **1. Report 3 (SRS)**<br>`Continuum_AI_Report3_...md`<br><br>**2. Report 4 (SDD)**<br>`Report4_Software_Design_Document.docx`<br><br>**3. Report 5 (Test doc & Excel)**<br>`Report5_Test_Documentation.docx`<br>`Report5_Unit_Test.xlsx`<br><br>**4. Report 6 (User Guide)**<br>`Report6_Software_User_Guides.docx` | • **Report 3:** Viết mô tả Use Case, các bước thực hiện (Main flow, Alternative flow), vẽ và chèn sơ đồ Use Case / Screen Flow từ `Output-DrawIo/`.<br>• **Report 4:** Vẽ sơ đồ Class/Component, bổ sung thuộc tính bảng CSDL (MongoDB schema) và sơ đồ tuần tự (Sequence Diagram).<br>• **Report 5:** Viết các kịch bản kiểm thử (Test Cases) vào file Excel test.<br>• **Report 6:** Chụp ảnh màn hình giao diện thật và viết các bước hướng dẫn người dùng bấm nút. |
| **Loại 2: Task Kỹ thuật ngầm & Tích hợp**<br>*(Technical / Integration Task)* | • Tích hợp đồng bộ Jira Cloud qua Webhook<br>• Dựng luồng RAG Chatbot với Vector DB LanceDB<br>• Cài đặt Redis Cache & Hàng đợi BullMQ | **1. Report 3 (SRS)**<br><br>**2. Report 4 (SDD)**<br><br>**3. Report 5 (Unit Test)** | • **Report 3:** Viết vào mục "External Interface" (Giao tiếp với hệ thống bên ngoài) và Non-Functional Requirements (NFR).<br>• **Report 4:** Viết vào mục Kiến trúc hệ thống (System Architecture), luồng gọi API giữa các service, Security / Token flow.<br>• **Report 5:** Viết hàm Unit Test test logic tích hợp và ghi log vào `Report5_Unit_Test.xlsx`. |
| **Loại 3: Task Hạ tầng & DevOps**<br>*(DevOps & Infrastructure Task)* | • Viết Dockerfile & Docker Compose cho microservices<br>• Setup CI/CD tự động bằng GitHub Actions<br>• Cấu hình Reverse Proxy Nginx | **1. Report 2 (PMP)**<br>`Continuum_AI_Report2_...docx`<br><br>**2. Report 4 (SDD)**<br><br>**3. Report 6 (User Guide)** | • **Report 2:** Viết vào mục "Tools & Infrastructure" và "Configuration Management" (quy tắc nhánh Git Flow).<br>• **Report 4:** Vẽ sơ đồ Deployment Diagram (các container Docker, port mạng).<br>• **Report 6:** Viết phần "System Installation & Deployment Guide" (hướng dẫn tải source, chạy `docker-compose up -d`, thiết lập file `.env`). |
| **Loại 4: Task Nghiên cứu & Đánh giá AI**<br>*(R&D / Spike Task)* | • Thử nghiệm Prompt cho Gemini vs OpenAI<br>• Đo độ trễ và độ chính xác của RAG có trích dẫn<br>• Đo chi phí token khi tóm tắt văn bản | **1. Report 1 (Intro)**<br>`Continuum_AI_Report1_...docx`<br><br>**2. Report 4 (SDD)**<br><br>**3. Checklist Capstone**<br>`Checklist_Capstone...xlsx` | • **Report 1:** Viết vào mục So sánh giải pháp đề xuất vs giải pháp truyền thống.<br>• **Report 4:** Viết thuật toán xử lý dữ liệu và thiết kế RAG Pipeline.<br>• **Checklist:** Ghi số liệu đối chứng vào sheet `Rubric-AI-vi` (chứng minh mô hình có đo đạc, đánh giá định lượng). |
| **Loại 5: Task Sửa lỗi & Tối ưu**<br>*(Bug Fix & Refactoring Task)* | • Fix lỗi mất token khi reload trang<br>• Tối ưu tốc độ query tìm kiếm ghi chú<br>• Sửa lỗi giao diện vỡ trên màn hình nhỏ | **1. Report 5 (Test Report)**<br>`Report5_Test_Report.xlsx`<br><br>**2. Report 7 (Final Report)**<br>`Report7_Final_Project_Report.docx` | • **Report 5:** Ghi vào Sheet "Bug Tracking" trong file `Report5_Test_Report.xlsx` (Mô tả bug, nguyên nhân, trạng thái Fixed).<br>• **Report 7:** Viết vào mục "Khó khăn gặp phải & Bài học kinh nghiệm" (Lessons Learned) ở báo cáo tổng kết. |

---

## 2. QUY TRÌNH 4 BƯỚC: "LÀM XONG 1 TÍNH NĂNG THÌ VIẾT GÌ?"

Mỗi khi một thành viên nhận và code xong **1 Tính năng (Feature)**, hãy đi qua đúng 4 bước tương ứng:

1. **Trước khi code:** Mở `Submit-Report/Continuum_AI_Report3_Software_Requirement_Specification.md` viết mô tả Use Case + vẽ màn hình phác thảo trong `Output-DrawIo/`.
2. **Khi thiết kế code:** Mở `Report 4 (SDD)` điền schema bảng CSDL MongoDB và vẽ sơ đồ luồng gọi API (Sequence Diagram).
3. **Khi code xong:** Viết test cases tương ứng vào `Report 5 (Unit Test & Test Report.xlsx)`.
4. **Chuẩn bị đem nộp / demo:** Chụp 1–2 ảnh màn hình giao diện thật dán vào `Report 6 (User Guide)`.

---

## 3. QUY TẮC CẬP NHẬT NHẬT KÝ ĐÓNG GÓP
Sau khi hoàn tất việc viết tài liệu theo bảng trên:
* Người thực hiện (hoặc AI) phải ghi lại một dòng vào [DOCUMENT_CONTRIBUTION_LOG.md](DOCUMENT_CONTRIBUTION_LOG.md) gồm: Ngày, Tên người làm (Phúc / Thắng / Danh / Tài / Tiên), Tên file, Nội dung thay đổi, và Trạng thái kiểm duyệt.
