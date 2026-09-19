# Quy Tắc Nghiêm Ngặt: Đóng Băng Tài Liệu Cốt Lõi (Strict Core Specs Freeze)

> **Mức độ ưu tiên:** CRITICAL (Bắt buộc tuân thủ tuyệt đối đối với tất cả Agent và Lập trình viên)  
> **Phạm vi bảo vệ:** Ba thư mục kỹ thuật nền tảng của dự án DATN:
> 1. `Document/architecture/` (Kiến trúc hệ thống, Topologies, Services, Storage, Security, K8s, Observability)
> 2. `Document/database-design/` (Toàn bộ 11 bộ schema độc lập: `01_SVC_IAM` đến `11_SAG_STORAGE`)
> 3. `Document/deploy/` (Cấu hình triển khai Docker Compose, Kubernetes, Helm, CI/CD Scripts)

---

## 1. Nguyên Tắc Cốt Lõi: Đóng Băng & Bất Biến (Frozen Baseline)

1. **Cực kỳ hạn chế thay đổi (Strictly Minimal Changes):**
   - Ba thư mục `architecture/`, `database-design/`, và `deploy/` là **"Hiến pháp kỹ thuật" (Ground Truth)** đã được khảo sát, chuẩn hóa, phân tách microservices và nghiệm thu kỹ lưỡng.
   - Nguyên tắc vận hành: **GẦN NHƯ KHÔNG ĐƯỢC PHÉP SỬA (Virtually Read-Only by Default)**.

2. **Cấm tự ý suy đoán và sửa đổi (Zero Spec Drift):**
   - Tuyệt đối KHÔNG được tự ý chỉnh sửa, định dạng lại, xóa bớt, gộp file, hoặc thay đổi các quyết định công nghệ trong 3 thư mục này khi đang thực hiện các task thông thường (coding, bug fixing, refactoring, viết prompt, tạo test case, v.v.).
   - Tuyệt đối KHÔNG sửa đổi tài liệu thiết kế database để "hợp thức hóa" mã nguồn viết sai. Mã nguồn backend/frontend/worker bắt buộc phải tuân thủ và thích ứng với tài liệu, không làm ngược lại.

---

## 2. Quy Trình Ngoại Lệ Bắt Buộc (Exception Approval Workflow)

Chỉ được phép sửa đổi bất kỳ tệp tin nào trong 3 thư mục trên khi và chỉ khi thỏa mãn **toàn bộ** các điều kiện sau:

1. **Có yêu cầu trực tiếp và rõ ràng từ Người Dùng:**
   - Người dùng chỉ định đích danh file và nội dung cần chỉnh sửa trong yêu cầu (prompt).
2. **Dừng lại để đánh giá tác động liên đới (Stop & Assess Impact):**
   - Trước khi sửa, Agent phải giải trình rõ: Vì sao cần sửa? Sửa những dòng nào? Tác động liên đới đến các Service khác và các Schema khác ra sao?
3. **Người dùng xác nhận chấp thuận (Explicit Confirmation):**
   - Phải có sự đồng ý xác nhận rõ ràng của người dùng trước khi thực hiện ghi đè hoặc sửa đổi nội dung.

---

## 3. Ràng Buộc Triển Khai Mã Nguồn (Implementation Constraints)

- **Backend (NestJS / Python FastAPI):**
  - Mọi Controller, Service, DTO, Mongoose Schema, TypeORM / Drizzle / Prisma Entity, và SQL queries phải ánh xạ chính xác 1:1 theo đúng các trường, kiểu dữ liệu, quan hệ khóa ngoại (FK), và chỉ mục (Index) đã định nghĩa trong `database-design/`.
- **Frontend (Next.js 14 App Router):**
  - Mọi route, component (đặc biệt là 3D Universe Canvas Three.js), state management (TanStack Query, Zustand) phải tuân thủ chuẩn `architecture/02_FRONTEND_NEXTJS.md`.
- **DevOps & Infrastructure:**
  - Mọi kịch bản container, ports, environment variables, volumes phải khớp chuẩn với `deploy/` và `architecture/01_SYSTEM_TOPOLOGY.md`.
