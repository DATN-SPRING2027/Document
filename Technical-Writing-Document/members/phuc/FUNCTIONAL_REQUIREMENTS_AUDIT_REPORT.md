# BÁO CÁO KIỂM CHỨNG VÀ ĐỐI CHIẾU YÊU CẦU CHỨC NĂNG (CONTINUUM AI)

> **Mục đích tài liệu:** Báo cáo kỹ thuật độc lập phục vụ rà soát phạm vi (Scope Review) sơ đồ *Functional Requirements* trước khi nghiệm thu và đưa vào báo cáo/slide tốt nghiệp. Tài liệu chỉ trích xuất dữ liệu thực tế từ codebase và hồ sơ đặc tả hiện hữu, tuân thủ nguyên tắc không tự suy diễn và không chỉnh sửa mã nguồn/sơ đồ trong lượt này.  
> **Người thực hiện rà soát:** Nguyễn Hồng Phúc  
> **Thời điểm rà soát:** 28/09/2026  
> **Dự án:** Continuum AI — Continuous Project Knowledge Capture, Verification and Handover  

---

## 1. CÁC NGUỒN DỮ LIỆU ĐÃ KIỂM TRA THỰC TẾ

| Loại nguồn | Đường dẫn tài liệu / Thư mục mã nguồn | Mục / Thành phần liên quan | Trạng thái tiếp cận |
| :--- | :--- | :--- | :--- |
| **Tài liệu đặc tả (SRS)** | `Phuc-NoteSite/Report-Project-Submit-To-Class/Submit-Report/Continuum_AI_Report3_Software_Requirement_Specification.md` | • Mục 2.1 (Actors)<br>• Mục 2.2.2 (Bảng 50 Use Cases/FRs)<br>• Mục 3.1.2 (36 Screen Descriptions)<br>• Mục 3.1.3 (Screen Authorization)<br>• Mục 3.1.4 (13 Non-Screen Functions)<br>• Mục 3.2+ (Mô tả chức năng chi tiết) | **Đã đọc toàn bộ.** Đây là nguồn sự thật (SSOT) về phạm vi nghiệp vụ cam kết với nhà trường. |
| **Tài liệu nghiên cứu quản trị** | `Document/research-docs/Governance/01-organization-context.md` | • Mục 1 (Evidence Classification Standard)<br>• Mục 2 (Executive Summary)<br>• Mục 4 (GAP Analysis về Multi-Tenant & Context) | **Đã đọc.** Nêu rõ mức độ hiện thực hóa thực tế của Organization/Multi-tenant trong code. |
| **Tài liệu hợp đồng Audit** | `Document/research-docs/Governance/03-audit-outbox-contract.md` | • Contract ghi nhận nhật ký kiểm toán (Audit Outbox Pattern) | **Đã đọc.** Khẳng định tính bất biến (append-only) của audit log. |
| **Sơ đồ Screen Flow tham chiếu** | `Phuc-NoteSite/Report-Project-Submit-To-Class/Output-DrawIo/` | • `07_screenflow_admin.drawio`<br>• `08_screenflow_team_leader.drawio`<br>• `09_screenflow_member.drawio` | **Đã kiểm tra cấu trúc XML.** Đối chiếu toàn bộ node màn hình với danh sách FR. |
| **Mã nguồn Backend (`DATN-BE`)** | `DATN-BE/src/services/` | • `iam/`: Auth, Org, Project, Team, Audit<br>• `capture/`: Work Notes (What/How/Why)<br>• `jira/`: Controller, Persistence, BullMQ queue<br>• `lifecycle/`: Verification, Knowledge objects<br>• `chat/`: Chat session, Citations, ACL filter<br>• `ingestion/`: Document processing, R2 presigned<br>• `handover/`: Persistence schemas (interviews, items)<br>• `notification/`: Mail consumer, Redis push | **Đã kiểm tra.** Đã phân biệt rõ giữa tầng Scaffolding (khung schema/model) và tầng Implementation (logic nghiệp vụ thực thi). |
| **Mã nguồn Frontend (`DATN-FE`)** | `DATN-FE/src/app/[locale]/` | • `(admin)/`: Profile, Layout, Tables, Forms | **Đã kiểm tra.** Đa phần là giao diện khung (Admin template), chưa tích hợp đầy đủ 50 endpoint. |

*Ghi chú về nguồn chưa tiếp cận:* Toàn bộ các tài liệu gốc đã được đọc trực tiếp từ hệ thống tệp local. Không có tài liệu nào bị thiếu đường dẫn.

---

## 2. KIỂM CHỨNG NHỮNG ĐIỂM NGHI VẤN KỸ THUẬT

Dưới đây là bảng đối chiếu chi tiết giữa **Nội dung hiển thị trên sơ đồ vừa vẽ**, **Bằng chứng tài liệu**, **Bằng chứng mã nguồn**, **Kết luận kỹ thuật** và **Các điểm chưa rõ**:

| Điểm nghi vấn | Nội dung thể hiện trên sơ đồ trước | Bằng chứng từ Tài liệu (SRS / Research Docs) | Bằng chứng từ Codebase (`DATN-BE`) | Kết luận thẩm định | Điểm còn chưa rõ / Cần lưu ý |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Cơ chế đồng bộ Jira** | *"Bi-directional Jira Issue Synchronization"* | **SRS dòng 125–127 & 268–269:**<br>• `FR-21`: Configure Jira Connector.<br>• `FR-22`: Sync Jira Issues (nhận issue từ Jira Cloud).<br>• `FR-23`: View Synced Jira Issues.<br>• `N-SF-7`: Webhook Processing (xử lý incoming webhook từ Jira).<br>• `N-SF-8`: Reconciliation Cronjob lúc 02:00 AM so sánh state local và remote.<br>• **Không có bất kỳ Use Case nào mô tả việc ghi ngược dữ liệu từ Continuum AI lên Jira.** | **`DATN-BE/src/services/jira`:**<br>• `persistence.ts`: Collections `jira_connections`, `jira_issues`, `jira_events`, `jira_sync_jobs`.<br>• `jira.service.ts`: Chỉ có phương thức skeleton `getHealth()`.<br>• Hàng đợi `jira-sync-queue` phục vụ pull/sync issue vào database local.<br>• **Không có HTTP client POST/PUT/PATCH nào ghi ngược task lên Jira API.** | ❌ **SAI LỆCH NGHIỆP VỤ:**<br>Jira chỉ là **đồng bộ một chiều (Inbound/Pull & Webhook)** từ Jira Cloud về Continuum AI để người dùng chọn task khi viết Daily Note.<br>**Tuyệt đối không phải đồng bộ hai chiều (Bi-directional).** | Sơ đồ trước tự suy diễn từ "đồng bộ thủ công + tự động" thành "đồng bộ 2 chiều". Cần sửa ngay thành **"Inbound Jira Issue Synchronization"**. |
| **2. Bản chất và định nghĩa của FR-44** | Bị bỏ sót trên sơ đồ cũ; sơ đồ mới ghi: *"Browse Uploaded Documents Library"* | **SRS dòng 148 (Mục 2.2.2):**<br>`\| 44 \| View Documents \| Admin, Team Leader, Member \| Browses uploaded documents with metadata, ingestion status, and source ACL information. \|`<br>**SRS dòng 209 (Mục 3.1.2):**<br>Screen #30: `Documents Library`. | **`DATN-BE/src/services/ingestion`:**<br>Schema collection `documents` và `sources` lưu trữ metadata file và đường dẫn Cloudflare R2 để người dùng xem danh sách tài liệu. | ✅ **ĐÚNG DANH TÁNH:**<br>`FR-44` là **"View Documents"**, phục vụ việc duyệt danh sách/thư viện tài liệu đã tải lên. Sơ đồ ban đầu bỏ sót mã này là một lỗi kỹ thuật. | Đã xác nhận vị trí chuẩn xác tại Mục 2.2.2 dòng 148. |
| **3. Vị trí của FR-37 (Chat History & Citations)** | Bị gộp/thiếu dòng riêng trên bản Slide Tổng quan | **SRS dòng 141 (Mục 2.2.2):**<br>`\| 37 \| View Chat History \| Admin, Team Leader, Member \| Browses previous chat sessions and messages with their citations and evidence references. \|` | **`DATN-BE/src/services/chat`:**<br>Collection `chat_sessions` và `chat_messages` lưu vết toàn bộ câu hỏi, câu trả lời và mảng citations liên quan. | ⚠️ **THIẾU SÓT TRÌNH BÀY:**<br>Bản slide tổng quan đã lược bỏ dòng FR-37 để nhét 2 dòng tài liệu (FR-43..46), khiến người xem tưởng rằng lịch sử hỏi đáp không được quản lý. | Cần đưa `View Chat History & Cited Evidence` thành một năng lực độc lập trong Module 4 trên cả 2 bản vẽ. |
| **4. Thuật ngữ "Milestone Sign-Off"** | *"Handover Package Checklist Review & Milestone Sign-Off"* | **SRS dòng 144 (Mục 2.2.2):**<br>`\| 40 \| Sign-off Handover Item \| Team Leader, Admin \| Confirms completion of a specific handover checklist item. \|` | **`DATN-BE/src/services/handover`:**<br>`persistence.ts` định nghĩa collection `handover_items` (gồm `handoverId`, `status: PENDING/SIGNED_OFF`), không có entity nào tên là "milestone". | ⚠️ **LỆCH THUẬT NGỮ:**<br>Tài liệu và code chỉ dùng khái niệm **"Handover Item" / "Checklist Item"**, không dùng khái niệm "Milestone" (Cột mốc dự án). | Cần chuẩn hóa về đúng tên nghiệp vụ: **"Sign-off Handover Checklist Items"**. |
| **5. Thuật ngữ "Multi-Tenant"** | *"Multi-Tenant Organization Settings"* | **SRS dòng 113 & 285:**<br>`FR-09`: Create Organization. Dòng 285: `organizations \| Represents a top-level organization (multi-tenant) with name, slug, plan...`<br>**Tài liệu nghiên cứu `01-organization-context.md`:**<br>Mục 2.1: Multi-tenant hiện mới ở mức `[PARTIAL]` Data Model Scaffolding (có trường `organizationId` trong DB nhưng chưa có Guard chặn chéo Tenant ở runtime). | **`DATN-BE/src/services/iam`:**<br>Entity `organizations` và `refresh_sessions` có `organizationId`. Chưa có Tenant Resolver Middleware ở tầng Gateway. | ⚠️ **CÓ CĂN CỨ THIẾT KẾ NHƯNG CHƯA HOÀN TẤT CODE:**<br>SRS có nêu "multi-tenant" ở cấp thiết kế ý niệm, nhưng triển khai thực tế chỉ là cấu hình Organization theo Tenant. | Giữ ở mức nghiệp vụ: **"Manage Organization Settings"**, tránh phô trương công nghệ runtime multi-tenancy. |
| **6. Thuật ngữ "Real-Time Audio Recording"** | *"Real-Time Audio Handover Interview Recording"* | **SRS dòng 145 & 207:**<br>`FR-41`: Audio Interview Recording qua WebSocket streaming lên R2, sau đó worker gọi Whisper API để bóc băng. | **`DATN-BE/src/services/handover`:**<br>Collection `interviews`, `interview_sessions` đã khai báo trong schema. Tầng WebSocket streaming chưa hoàn thiện thực thi. | ⚠️ **CĂN CỨ MỘT PHẦN:**<br>Tài liệu yêu cầu ghi âm qua WebSocket stream, nhưng việc trích xuất chữ (transcription) chạy bất đồng bộ qua hàng đợi, không phải AI dịch thời gian thực (real-time). | Dùng tên chính xác theo SRS: **"Record Audio Handover Interview"**. |
| **7. Định vị phân hệ Notifications** | Bị đặt nằm trong Module 5 (Structured Handover) | **SRS dòng 151–152 & 271–272:**<br>`FR-47`: View Notifications (báo lịch review tri thức, cập nhật handover, nhắc việc 17:30).<br>`FR-48`: Mark Notification as Read.<br>`N-SF-10..11`: Mail queue gửi email kích hoạt tài khoản, đổi mật khẩu, alert tri thức. | **`DATN-BE/src/services/notification`:**<br>Là một service độc lập (`notification.module.ts`), lắng nghe event từ IAM, Capture, Lifecycle, Handover. | ❌ **SAI LỆCH PHÂN NHÓM:**<br>Notifications là **dịch vụ dùng chung toàn hệ thống (Cross-cutting System Service)**, phục vụ cả Auth, Daily Note, Duyệt tri thức và Bàn giao; không phải tính năng con riêng của Handover. | Cần đưa Notifications về đúng vị trí tính năng hệ thống/dùng chung. |
| **8. Ý nghĩa quy chuẩn của mã `N-SF`** | Được gán nhãn `[Background]` | **SRS Mục 3.1.4 (Trang 10):**<br>Tiêu đề mục: `3.1.4 Non-Screen Functions`. Liệt kê 13 chức năng chạy ngầm (Middleware token, Redis blacklist check, Cronjob nhắc việc 17:30, BullMQ worker...). | Codebase có các thư mục riêng cho `workers/` và `queues/` phục vụ các tác vụ này. | ✅ **ĐÚNG ĐỊNH NGHĨA:**<br>`N-SF` là **Non-Screen Functions** (Chức năng không có màn hình trực tiếp). Đây là các Functional Requirements chạy ngầm của hệ thống, không phải NFR. | Đã được kiểm chứng chính xác từ Mục 3.1.4 của SRS. |
| **9. Nguồn xác định 50 FRs chính thức** | Tuyên bố 50 capabilities | **SRS Mục 2.2.2 (Descriptions):**<br>Bảng Use Case đánh số từ `01` đến `50`.<br>**SRS Mục 3.1.2:** Liệt kê 36 màn hình tương ứng. | Toàn bộ 50 use case này được ánh xạ vào các controller của 8 service trong `DATN-BE`. | ✅ **ĐÚNG NGUỒN SSOT:**<br>Con số 50 FRs được xác lập trực tiếp từ Mục 2.2.2 của SRS Report 3, không phải con số tự bịa đặt. | Nguồn chứng minh: `Continuum_AI_Report3_Software_Requirement_Specification.md`, lines 103–155. |

---

## 3. ĐÁNH GIÁ CÁC GÓP Ý TỪ PHÍA REVIEW ĐỘC LẬP

Dưới đây là đánh giá khách quan về các góp ý của bên review, chỉ rõ điểm nào đúng cần tiếp thu, điểm nào không phù hợp với dự án và điểm nào thiếu căn cứ:

### 1. Những góp ý ĐÚNG — Nên áp dụng 100%:
* **Góp ý loại bỏ "Bi-directional Jira Sync":** **Rất chính xác.** Tài liệu và code chỉ chứng minh luồng đọc (Inbound) issue từ Jira Cloud về để phục vụ viết Daily Note. Không có luồng ghi ngược. Cần sửa thành *"Inbound Jira Issue Synchronization"*.
* **Góp ý về sự biến mất của FR-44:** **Rất chính xác.** FR-44 (`View Documents`) có trong Mục 2.2.2 nhưng bị bỏ sót ở sơ đồ cũ. Việc phục hồi FR-44 là bắt buộc để đảm bảo đủ 50 FRs.
* **Góp ý về Notifications không thuộc riêng Handover:** **Rất chính xác.** Việc nhét Notifications vào hộp Handover chỉ để "cho vừa chỗ" là sai lệch cấu trúc hệ thống. Notification là thành phần Cross-cutting phục vụ toàn bộ các module.
* **Góp ý chuẩn hóa ngôn ngữ Verb + Object và bỏ Buzzword công nghệ:** **Rất chính xác.** Sơ đồ chức năng phải diễn đạt hành vi nghiệp vụ hệ thống cung cấp cho người dùng, không phải bản vẽ công nghệ backend (không cần phô diễn Bcrypt, Redis JTI, ACID, Presigned URL trên tên chức năng).

### 2. Những góp ý CHƯA CHÍNH XÁC hoặc KHÔNG PHÙ HỢP với Project:
* **Nghi vấn về mã `N-SF` có phải là Non-functional Requirements không:** **Bác bỏ nghi vấn này.** Đã có bằng chứng văn bản tại Mục 3.1.4 của SRS gốc: `N-SF` là viết tắt chính thức của **"Non-Screen Functions"** (Chức năng không có màn hình). Đây là quy ước nội bộ đã được giảng viên hướng dẫn chấp thuận trong cấu trúc đề cương Report 3.
* **Nghi vấn về con số "50 capabilities" có bị phóng đại không:** **Bác bỏ nghi vấn này.** Mục 2.2.2 của tài liệu SRS Report 3 liệt kê chính xác bảng 50 Use Cases từ ID 01 đến ID 50. Đây là cam kết phạm vi chính thức của nhóm nộp cho hội đồng chấm đồ án.
* **Yêu cầu ép mọi FR phải có màn hình tương ứng trên Screen Flow:** **Không phù hợp với bản chất phần mềm.** Trong 50 FRs:
  - Có các FR là hành động trong trang (ví dụ: `FR-03: Refresh Token` là cơ chế ngầm; `FR-40: Sign-off Handover Item` là nút bấm trong màn hình chi tiết; `FR-26: Confirm Note` là modal dialog).
  - Không thể ép quan hệ 1 FR = 1 màn hình lớn. Bảng phân tích Screen Flow của nhóm phản ánh đúng luồng màn hình điều hướng (Navigation Screen Flow).

---

## 4. BẢNG ĐỀ XUẤT THAY ĐỔI ĐỂ REVIEW VÀ PHÊ DUYỆT

Nếu bên review độc lập và nhóm thống nhất phương án điều chỉnh, dưới đây là danh sách toàn bộ các thay đổi dự kiến sẽ được cập nhật vào sơ đồ (Hiện tại chưa ghi đè file):

| # | Nội dung hiện tại (Trên sơ đồ cũ/bản nháp) | Nội dung đề xuất chuẩn hóa | Lý do điều chỉnh | Nguồn chứng minh cụ thể | Có thay đổi phạm vi nghiệp vụ cam kết không? |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **1** | `Bi-directional Jira Issue Synchronization & Viewing` | **Inbound Jira Issue Synchronization & Task Linking** | Hệ thống chỉ đọc issue từ Jira về qua Webhook/REST API để link vào Daily Note; không ghi ngược về Jira. | SRS lines 125–127; `DATN-BE/src/services/jira` không có write client. | ❌ Không (Làm rõ đúng bản chất thực tế). |
| **2** | Bỏ sót `FR-44` ở Module 4 | **Bổ sung tường minh: `FR-44: Browse Documents Library`** | Đảm bảo tính toàn vẹn 50 FRs, phục hồi chức năng xem thư viện tài liệu đã tải lên. | SRS line 148 (Mục 2.2.2); Screen #30 (Mục 3.1.2). | ❌ Không (Khôi phục yêu cầu đã cam kết trong SRS). |
| **3** | Omit dòng `FR-37` trên slide tổng quan | **Đưa `FR-37: View Chat History & Cited Evidence` lên slide** | Lịch sử chat và bằng chứng trích dẫn là tính năng cốt lõi của trợ lý AI Continuum, không được ẩn đi. | SRS line 141 (Mục 2.2.2); `DATN-BE/src/services/chat/persistence.ts`. | ❌ Không. |
| **4** | `Handover Package Checklist Review & Milestone Sign-Off` | **Handover Package Review & Checklist Item Sign-Off** | Bỏ chữ "Milestone" vì SRS và entity database chỉ quản lý theo `handover_items`, không có khái niệm milestone. | SRS line 144; `DATN-BE/src/services/handover/infrastructure/persistence.ts`. | ❌ Không (Chuẩn hóa thuật ngữ). |
| **5** | `Real-Time Audio Handover Interview Recording` | **Record Audio Handover Interview (WebSocket Stream)** | Việc ghi âm truyền qua WebSocket, nhưng bóc băng Whisper chạy worker bất đồng bộ, không phải dịch trực tiếp real-time. | SRS line 145 & line 273 (`N-SF-12 Audio Transcription Worker`). | ❌ Không (Chuẩn hóa thuật ngữ). |
| **6** | `Notification Center (FR-47, FR-48)` nằm trong Module Handover | **Đưa Notifications về thành phần dùng chung hệ thống (Cross-cutting) hoặc đặt nhãn [System-wide Service]** | Notifications phục vụ toàn bộ hệ thống (Auth, Capture, Review, Handover), không thuộc sở hữu riêng của Handover. | SRS line 151; `DATN-BE/src/services/notification` là module độc lập. | ❌ Không (Sắp xếp lại logic phân nhóm). |
| **7** | `Multi-Tenant Organization Settings Management` | **Organization Settings & Workspace Management** | Giảm thiểu từ khóa "Multi-Tenant" vì tầng code hiện mới scaffolding trường `organizationId`, chưa hoàn thiện runtime tenant isolation. | `Document/research-docs/Governance/01-organization-context.md` (Đánh giá GAP). | ❌ Không. |
| **8** | Chức năng kiểm toán ghi `Immutable System Audit Logs` | **View Scoped Audit Logs & Tamper-Evident Trail** | Phân biệt rõ quyền: Người dùng (Admin/Leader) thực hiện hành vi **Xem nhật ký (View Logs)**, hệ thống chạy ngầm việc **Ghi nhận bất biến (Tamper-evident Recording)**. | SRS line 154 (FR-50) & `03-audit-outbox-contract.md`. | ❌ Không. |

---

## 5. CÂU HỎI THỐNG NHẤT CẦN NHÓM VÀ BÊN REVIEW XÁC NHẬN

Trước khi tiến hành sửa file và kết xuất lại ảnh:

1. **Về vị trí của Notifications (FR-47, FR-48):** 
   - Nhóm muốn giữ Notifications ở Module 5 (với ghi chú rõ là phục vụ sự kiện bàn giao & toàn hệ thống)? 
   - Hay muốn tách Notifications thành một dải băng tiện ích dùng chung (Cross-Cutting Services) ở chân sơ đồ cùng với Audit Logs?
2. **Về phạm vi Audit Logs của Team Leader (FR-50):**
   - SRS Table 3.1.3 ghi Team Leader có quyền xem `Audit Logs (scoped)` theo team.
   - Nhưng Screen Flow `08_screenflow_team_leader.drawio` hiện không vẽ màn hình này.
   - Nhóm có đồng ý đánh dấu ký hiệu `▲ (Needs UI Confirmation)` cho quyền truy cập này trên sơ đồ để khớp với Screen Flow hiện tại không?

---
*Báo cáo kết thúc tại đây. Giữ nguyên hiện trạng tệp vẽ và mã nguồn cho đến khi có ý kiến phản hồi chính thức.*
