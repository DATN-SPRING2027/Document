# PHẢN HỒI KIỂM CHỨNG KỸ THUẬT & TRÍCH XUẤT NGUỒN GỐC (CONTINUUM AI)

> **Mục đích:** Tài liệu trích xuất trực tiếp từ hồ sơ gốc (SRS Report 3, Architecture Docs và Source Code DATN-BE) để chuyển giao cho bên review độc lập.  
> **Nguyên tắc:** Phân biệt rạch ròi giữa yêu cầu ghi trong tài liệu (SSOT), hiện trạng trong mã nguồn, và các điểm mâu thuẫn cần nhóm thống nhất. Không sửa file mã nguồn hay sơ đồ trong lượt này.  
> **Ngày lập:** 28/09/2026  
> **Người thực hiện:** Nguyễn Hồng Phúc  

---

## 1. TRÍCH NGUYÊN VĂN SRS VỀ FR-22, FR-40, FR-44 VÀ ĐỊNH NGHĨA N-SF

**Nguồn:** `Phuc-NoteSite/Report-Project-Submit-To-Class/Submit-Report/Continuum_AI_Report3_Software_Requirement_Specification.md`

### 1.1. FR-22 (Mục 2.2.2 Descriptions — Dòng 126)
```markdown
| 22 | Sync Jira Issues | Admin, Team Leader | Triggers manual synchronization of Jira issues or views automatic sync status. |
```

### 1.2. FR-40 (Mục 2.2.2 Descriptions — Dòng 144)
```markdown
| 40 | Sign-off Handover Item | Team Leader, Admin | Confirms completion of a specific handover checklist item. |
```

### 1.3. FR-44 (Mục 2.2.2 Descriptions — Dòng 148 & Mục 3.1.2 — Dòng 209)
* **Tại Mục 2.2.2 (Dòng 148):**
```markdown
| 44 | View Documents | Admin, Team Leader, Member | Browses uploaded documents with metadata, ingestion status, and source ACL information. |
```
* **Tại Mục 3.1.2 Screen Descriptions (Dòng 209 — Screen #30):**
```markdown
| 30 | Documents | Documents Library | Grid/list of uploaded documents with file type, upload date, ingestion status, and source ACL info. |
```

### 1.4. Định nghĩa N-SF (Mục 3.1.4 — Dòng 258–261)
* **Tiêu đề và cấu trúc bảng nguyên văn:**
```markdown
#### 3.1.4 Non-Screen Functions

| # | Feature | System Function | Description |
|---|---------|-----------------|-------------|
```
* **Bản chất xác thực:** `N-SF` là tên viết tắt chính thức của **Non-Screen Functions** (Các chức năng nghiệp vụ cấp hệ thống chạy ngầm, không có giao diện tương tác trực tiếp). Bao gồm 13 tác vụ: Token validation middleware, Redis JTI check, Refresh token rotation, Cronjob nhắc việc 17:30, Gap scanner, AI extraction worker, Webhook processing, 02:00 AM reconciliation cronjob, Document OCR worker, Email consumer, WebSocket push, Whisper transcription worker, Pre-retrieval ACL filter.  
* **Khẳng định:** Đây là **Functional Requirements (Yêu cầu chức năng ngầm)**, tuyệt đối **không phải** Non-Functional Requirements (NFR).

---

## 2. XÁC MINH CƠ CHẾ ĐỒNG BỘ JIRA (INBOUND HAY BI-DIRECTIONAL?)

### 2.1. Kết luận kỹ thuật
Hệ thống **CHỈ THỰC HIỆN ĐỒNG BỘ MỘT CHIỀU VÀO (INBOUND ONLY)** từ Jira Cloud về cơ sở dữ liệu của Continuum AI để phục vụ việc trích xuất và chọn task khi viết Daily Work Note. **Không có bất kỳ cơ chế hay chức năng nào ghi ngược/cập nhật dữ liệu từ Continuum AI lên Jira.**

### 2.2. Bằng chứng tài liệu (SRS Report 3)
* **Dòng 268 (`N-SF-7`):**
  > `BullMQ worker that processes incoming Jira webhook events with idempotency deduplication (Redis SETNX).`  
  *(Chỉ tiếp nhận và xử lý incoming payload từ webhook do Jira bắn sang).*
* **Dòng 269 (`N-SF-8`):**
  > `Scheduled job at 02:00 AM that reconciles missed webhook events by comparing local and remote Jira states.`  
  *(Chạy quét định kỳ đối soát đọc trạng thái).*
* Toàn bộ tài liệu SRS **không có bất kỳ Use Case nào** cho phép tạo issue mới, sửa mô tả, chuyển trạng thái hay ghi comment ngược về Jira Cloud.

### 2.3. Bằng chứng mã nguồn (`DATN-BE`)
1. **Schema lưu trữ issue chỉ ở dạng Snapshot đọc:**  
   *Tệp:* `DATN-BE/src/services/jira/infrastructure/mongodb/mongodb.schemas.ts` (Dòng 70–98):
   ```typescript
   jira_issues: new Schema(
     {
       organizationId: { type: Schema.Types.ObjectId, required: true },
       projectId: { type: Schema.Types.ObjectId, required: true },
       jiraConnectionId: { type: Schema.Types.ObjectId, required: true },
       issueId: { type: String, required: true },
       issueKey: { type: String, required: true },
       summary: { type: String, required: true },
       descriptionText: String,
       status: { type: String, required: true },
       lastSyncedAt: { type: Date, required: true },
     },
     { collection: 'jira_issues', timestamps: true, strict: true },
   )
   ```
2. **Work Note chỉ lưu khóa tham chiếu, không phát sinh mutation lên Jira:**  
   *Tệp:* `DATN-BE/src/services/capture/infrastructure/mongodb/mongodb.schemas.ts` (Dòng 46–47):
   ```typescript
   jiraIssueId: String,
   jiraIssueKey: String,
   ```
3. **Mã nguồn Service thực thi hiện thời:**  
   *Tệp:* `DATN-BE/src/services/jira/application/jira.service.ts` (Dòng 1–10):
   ```typescript
   import { Injectable } from '@nestjs/common';
   import { HealthResponse } from '../../../health/health.response';

   @Injectable()
   export class JiraApplicationService {
     getHealth(): HealthResponse {
       return { status: 'ok' };
     }
   }
   ```
   *Nhận định:* Tầng service chưa có logic HTTP Client (`Axios`/`HttpService`) nào thực hiện lệnh `POST`, `PUT`, `PATCH` tới REST API của Atlassian Jira. Việc gán nhãn "Bi-directional" trước đây là suy diễn không có căn cứ.

---

## 3. LÀM RÕ VIỆC FR-28 VÀ FR-29 CÙNG GẮN SCREEN #20

### 3.1. Kết luận
Đây là **LỖI MAPPING (TYPO)** trong bảng tổng hợp trước đó, **không phải hai chức năng dùng chung một màn hình**.

### 3.2. Căn cứ từ tài liệu gốc SRS
* **Bảng Screen Descriptions (Mục 3.1.2 — Dòng 199–201):**
  - **Screen #20:** Duy nhất là `Verification Inbox` (Mô tả: *"Queue of pending knowledge proposals for the reviewer's authorized scope"*). Màn hình này dành cho người kiểm duyệt (`FR-29`).
  - **Screen #21:** `Knowledge Review Detail` (`FR-30`).
  - **Screen #22:** `Knowledge Objects` (`FR-31`).
  - **Không hề có màn hình độc lập nào tên là "Propose Form" được đánh số #20.**
* **Đối chiếu Screen Flow:**
  - Trong `09_screenflow_member.drawio` (Dòng 43), `FR-28 (Propose Knowledge Object)` là form phụ/dialog (`s-propose`) mở ra từ màn hình `Knowledge Base` (Screen #22) hoặc trích xuất từ `Work Note`.
  - Trong `08_screenflow_team_leader.drawio` (Dòng 22), `Verification Inbox` (`s-inbox`) là màn hình danh sách hàng đợi duyệt độc lập của Leader (`FR-29`).

---

## 4. VỊ TRÍ TRUY CẬP JIRA SYNC (LEADER) VÀ XEM JIRA ISSUES (ADMIN)

Đây là một **ĐIỂM HỞ NGHIỆP VỤ / MÂU THUẪN (GAP)** giữa bảng phân quyền Use Case (Mục 2.2.2) và thiết kế giao diện (Mục 3.1.2, 3.1.3 & Screen Flow):

### 4.1. Team Leader kích hoạt Jira Sync tại đâu?
* **Mục 2.2.2 (Dòng 126):** Khai báo `FR-22 (Sync Jira Issues)` cho phép cả `Admin, Team Leader`.
* **Mục 3.1.3 Screen Authorization (Dòng 236):** Màn hình `Jira Connector Config` (Screen #16) **chỉ có dấu X cho Admin**, cột Team Leader để trống.
* **Screen Flow `08_screenflow_team_leader.drawio`:** Hoàn toàn **không có** node màn hình hay nút bấm nào tên là Jira Sync.
* **Kết luận:** *Hiện tại chưa có điểm truy cập giao diện (UI Entry Point) để Team Leader kích hoạt Jira Sync.*

### 4.2. Admin xem Jira Issues ở đâu?
* **Mục 2.2.2 (Dòng 127):** Khai báo `FR-23 (View Synced Jira Issues)` dành cho `Admin, Team Leader, Member`.
* **Mục 3.1.2 & 3.1.3:** Screen #16 (`Jira Connector Config`) chỉ hiển thị *"sync status and last sync time"*, không hiển thị bảng danh sách issue. Danh sách issue thực tế chỉ xuất hiện trong form viết Daily Note (Screen #18), nhưng Admin lại không được cấp quyền truy cập màn hình Daily Note (Dòng 237).
* **Kết luận:** *Hiện tại không có màn hình chuyên biệt nào để Admin duyệt xem toàn bộ các Jira issues đã đồng bộ.*

---

## 5. Ý NGHĨA THỰC SỰ CỦA NHÃN "CONFIRMED" TRONG FILE ĐẶC TẢ

### 5.1. Bản chất của nhãn `CONFIRMED`
Nhãn `CONFIRMED` trong file `FUNCTIONAL_REQUIREMENTS_SPEC.md` vừa tạo chỉ có ý nghĩa:
> **"SCOPE CONFIRMED IN SRS (REPORT 3)"**  
> (Chức năng này đã được định nghĩa chính thức trong hồ sơ đặc tả yêu cầu SRS của nhóm nộp nhà trường, không phải tính năng tự biên dịch hoặc đề xuất thêm ngoài phạm vi).

### 5.2. Phân định với hiện trạng mã nguồn thực tế
Theo chuẩn phân loại mức độ bằng chứng tại tài liệu nghiên cứu của project (`Document/research-docs/Governance/01-organization-context.md`, Mục 1 Dòng 11–21), hiện trạng của 50 FRs được chia thành các mức:

1. **`[IMPLEMENTED]` (Đã có logic nghiệp vụ):**
   - Các phân hệ `iam` (Authentication JWT, Password reset, 2FA, Profile), `capture` (Work note draft/confirm/history), `chat` (Chat session, citations logic cơ bản).
2. **`[PARTIAL / SCAFFOLDING]` (Mới có khung sườn Database / Queue, chưa có logic API):**
   - Phân hệ `jira` (đã có schema `jira_issues`, `jira_connections`, queue `jira-sync-queue`, nhưng service mới có `getHealth()`).
   - Phân hệ `handover` (đã có schema `handovers`, `handover_items`, `interviews`, nhưng service mới có `getHealth()`).
3. **`[GAP]` (Chưa triển khai mã nguồn):**
   - Giao diện kích hoạt Jira Sync cho Leader; Giao diện xem Jira issues cho Admin.
4. **`[VERIFIED AT RUNTIME]` (Đã chạy kiểm thử tự động đạt):**
   - **CHƯA ĐẠT** đối với toàn bộ 50 FRs (Chưa có bộ test tích hợp end-to-end hoàn chỉnh).

---
*Tài liệu lập xong để chuyển bên review độc lập.*
