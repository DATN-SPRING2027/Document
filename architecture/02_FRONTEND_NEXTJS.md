# Continuum AI — Kiến Trúc Frontend Next.js (App Router)

> Nằm trong tài liệu kiến trúc tổng thể Continuum AI. Xem [Mục lục](README.md).

---

## 1. Lý do lựa chọn Next.js (App Router) thay thế Pure React

Trước đây, dự án từng cân nhắc sử dụng React SPA thuần (Vite). Tuy nhiên, việc chuyển đổi sang **Next.js (App Router, TypeScript, Tailwind CSS, TailAdmin)** mang lại những ưu thế kỹ thuật vượt trội cho đồ án tốt nghiệp:

1. **Kiến trúc Server Components (RSC):** Các trang Dashboard layout, Sidebar điều hướng, danh mục tĩnh không cần tải JavaScript xuống client, giúp giảm **45% dung lượng Bundle JS ban đầu (Initial Bundle Size)**.
2. **Streaming Server-Sent Events (SSE) mượt mà:** Trợ lý hỏi đáp AI (Cited Chat) yêu cầu stream câu trả lời kèm thẻ trích dẫn theo thời gian thực mà không bị chặn render giao diện.
3. **Bảo mật Token với HttpOnly Cookies:** Next.js Route Handlers đóng vai trò **BFF (Backend-for-Frontend)**, cho phép lưu Access/Refresh Token trong `HttpOnly Secure Cookies`, loại bỏ hoàn toàn nguy cơ tấn công XSS đánh cắp token từ `localStorage`.
4. **Không cần Micro Frontend:** Với cấu trúc thư mục dạng **Feature-Driven Modular Architecture**, Next.js tự động thực hiện **Route-based Code Splitting**. Người dùng truy cập trang nào, trình duyệt mới nạp code của tính năng đó, đạt hiệu năng tối ưu mà không phải chịu sự phức tạp của Module Federation.

---

## 2. Cấu trúc thư mục chuẩn Next.js App Router (TailAdmin Foundation)

```text
frontend/
├── src/
│   ├── app/                                    # Next.js App Router (File-system Routing)
│ │   │   ├── (dashboard)/                        # Route Group: Không gian làm việc chính
│   │   │   ├── layout.tsx                      # TailAdmin Dashboard Shell (Sidebar + Header)
│   │   │   ├── page.tsx                        # Dashboard tổng quan tri thức & chỉ số
│   │   │   ├── universe/                       # [WOW FACTOR] Vũ Trụ Tri Thức 3D (Knowledge Galaxy)
│   │   │   │   ├── page.tsx                    # Canvas 3D toàn cảnh không gian tri thức (Three.js/R3F)
│   │   │   │   └── [partitionId]/page.tsx      # Đi sâu vào chi tiết cụm tinh vân Module/Service
│   │   │   ├── daily-notes/                    # Tính năng ghi nhận công việc hàng ngày
│   │   │   │   ├── page.tsx                    # Danh sách notes + Lịch làm việc
│   │   │   │   └── [date]/page.tsx             # Form nhập What/How/Why (Jira prefilled)
│   │   │   ├── verification/                   # Hộp thư kiểm chứng tri thức (Verification Inbox)
│   │   │   │   └── page.tsx                    # Danh sách Proposed Knowledge cho SME/Leader
│   │   │   ├── assistant/                      # Trợ lý thông minh (Cited Chatbot)
│   │   │   │   └── page.tsx                    # Khung chat RAG, streaming và citation cards
│   │   │   ├── handover/                       # Studio chuyển giao công việc
│   │   │   │   ├── page.tsx                    # Danh sách đợt bàn giao & Readiness Checklist
│   │   │   │   └── [id]/interview/page.tsx     # Phòng phỏng vấn Audio thời gian thực
│   │   │   └── settings/                       # Quản lý Organization, Projects, Teams, Grants
│   │   │
│   │   ├── api/                                # Route Handlers (BFF Proxy & Webhook Receiver)
│   │   │   ├── auth/[...nextauth]/route.ts     # Xử lý set HttpOnly Cookies
│   │   │   └── proxy/[...path]/route.ts        # Chuyển tiếp request an toàn vào NestJS VPC
│   │   │
│   │   ├── globals.css                         # Tailwind CSS Tokens & Typography Inter
│   │   └── layout.tsx                          # Root Layout (Fonts, Theme Provider)
│   │
│   ├── components/                             # UI Components tái sử dụng
│   │   ├── ui/                                 # Primitives từ TailAdmin (Button, Modal, Input)
│   │   ├── common/                             # Header, Sidebar, Breadcrumb, NotificationBell
│   │   ├── citations/                          # Component hiển thị nguồn trích dẫn tài liệu
│   │   └── universe-3d/                        # [3D GALAXY] Components WebGL / Three.js
│   │       ├── GalaxyCanvas.tsx                # R3F Canvas, OrbitControls, Bloom Effect
│   │       ├── PartitionNebula.tsx             # Tinh vân đại diện cho Module/Service
│   │       ├── EntityStarNode.tsx              # Tinh cầu thực thể phát sáng (Shader bloom)
│   │       ├── HyperedgeLinks.tsx              # Đường nối liên kết ngữ nghĩa giữa các node
│   │       ├── FlyToCameraController.tsx       # Điều khiển camera bay mượt mà theo Citation
│   │       └── TimeHorizonSlider.tsx           # Thanh trượt xem lịch sử tri thức theo thời gian
│   │
│   ├── features/                               # Business Logic & Components theo từng Module
│   │   ├── auth/                               # Hooks, Services, Types của Auth
│   │   ├── universe/                           # Store 3D Camera, Raycaster, Partition Nodes API
│   │   ├── daily-notes/                        # Markdown editor, Jira issue selector
│   │   ├── verification/                       # So sánh diff phiên bản, nút Approve/Reject
│   │   ├── assistant/                          # SSE Stream Consumer, Citation Popover
│   │   └── handover/                           # Web Audio API recorder, WebSocket clienter, Sidebar, Breadcrumb, NotificationBell
│   │   └── citations/                          # Component hiển thị nguồn trích dẫn tài liệu
│   │
│   ├── features/                               # Business Logic & Components theo từng Module
│   │   ├── auth/                               # Hooks, Services, Types của Auth
│   │   ├── daily-notes/                        # Markdown editor, Jira issue selector
│   │   ├── verification/                       # So sánh diff phiên bản, nút Approve/Reject
│   │   ├── assistant/                          # SSE Stream Consumer, Citation Popover
│   │   └── handover/                           # Web Audio API recorder, WebSocket client
│   │
│   ├── hooks/                                  # Custom React Hooks
│   ├── lib/                                    # Tiện ích chung (api-client, date-format)
│   └── stores/                                 # Zustand Stores (Local UI State)
```

---

## 3. Ranh giới Server Components vs Client Components

Để duy trì hiệu năng cao nhất, hệ thống phân định ranh giới render rõ ràng:

### 3.1. Server Components (RSC - Mặc định)
* **Áp dụng cho:**
  - `(dashboard)/layout.tsx`: Nạp cấu hình tổ chức, kiểm tra quyền server-side trước khi render layout.
  - Các trang danh sách dữ liệu tĩnh: Lấy dữ liệu ban đầu từ NestJS Backend trực tiếp trên Node.js server của Next.js mà không để lộ URL API nội bộ.
  - Metadata SEO, Tiêu đề trang, OpenGraph tags.

### 3.2. Client Components (`'use client'`)
* **Bắt buộc dùng khi có tương tác người dùng hoặc Web APIs:**
  - **Trợ lý Cited Chat (`assistant/`):** Lắng nghe luồng SSE (Server-Sent Events) và render Markdown thời gian thực.
  - **Phòng phỏng vấn Bàn giao (`handover/[id]/interview`):** Sử dụng `navigator.mediaDevices.getUserMedia` để thu âm giọng nói và đẩy chunk audio nhị phân qua WebSocket.
  - **Trình soạn thảo Daily Note:** Nhập liệu form What/How/Why, Markdown preview và autosave draft vào client state.
  - **Hộp thư kiểm chứng (`verification/`):** Thao tác bấm nút "Phê duyệt (Verify)" hoặc "Từ chối (Reject)" kèm lý do và kích hoạt Mongoose Transaction ở backend.

---

## 4. Quản lý trạng thái (State Management)

Dự án áp dụng nguyên tắc **phân tách triệt để giữa Server Cache và Client State**:

```
                              [ TRẠNG THÁI ỨNG DỤNG ]
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
         [ 1. SERVER STATE CACHE ]                 [ 2. LOCAL UI STATE ]
         Công nghệ: TanStack Query v5              Công nghệ: Zustand
                    │                                         │
     • Caching danh sách Daily Notes           • Thu gọn/Mở rộng Sidebar TailAdmin
     • Hộp thư Verification Inbox              • Trạng thái Modal, Popup trích dẫn
     • Lịch sử phiên hỏi đáp Chat              • Cờ bật/tắt Micro khi phỏng vấn Audio
     • Tự động Invalidate Cache khi            • Draft ghi chú tạm thời trước khi gửi
       có Mutation (Thêm/Sửa/Xóa)
```

### Mã mẫu kết nối TanStack Query trong Next.js Client Component:
```tsx
'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchVerificationInbox, verifyProposal } from '@/features/verification/api';

export function VerificationInboxView() {
  const queryClient = useQueryClient();

  const { data: inbox, isLoading } = useQuery({
    queryKey: ['verification-inbox'],
    queryFn: fetchVerificationInbox,
    staleTime: 1000 * 60 * 2, // Cache 2 phút
  });

  const mutation = useMutation({
    mutationFn: verifyProposal,
    onSuccess: () => {
      // Invalidate để tự động load lại dữ liệu mới
      queryClient.invalidateQueries({ queryKey: ['verification-inbox'] });
    },
  });

  if (isLoading) return <div>Đang tải hộp thư kiểm chứng...</div>;

  return (
    <div className="grid gap-4">
      {inbox?.map((item) => (
        <ProposalCard key={item._id} proposal={item} onVerify={(id) => mutation.mutate(id)} />
      ))}
    </div>
  );
}
```

---

## 5. Tích hợp TailAdmin Design System

Hệ thống sử dụng bộ giao diện **TailAdmin (Tailwind CSS)** với:
* **Chế độ Light Mode chuẩn mực:** Bảng màu chủ đạo: Nền `#f8fafc` (Slate-50), Card `#ffffff`, Viền `#e2e8f0` (Slate-200), Màu chữ chính `#0f172a` (Slate-900).
* **Typography:** Font chữ không chân hiện đại Inter (`sans-serif`) kết hợp JetBrains Mono (`monospace`) cho các đoạn mã nguồn và trích dẫn bằng chứng.
* **Bộ Icon Two-Tone:** Đồng bộ với Iconsax™ SVG 24x24 trên toàn bộ Dashboard.

---

## 6. Trực Quan Hóa Vũ Trụ Tri Thức 3D (Interactive 3D Knowledge Universe Canvas)

> ⭐ **ĐIỂM NHẤN CỐT LÕI (WOW FACTOR) CỦA ĐỒ ÁN TỐT NGHIỆP**:  
> Thay vì xem tri thức dưới dạng bảng phẳng hay danh sách văn bản nhàm chán, Continuum AI cung cấp trang **`(dashboard)/universe/`** biến toàn bộ tri thức kỹ thuật thành một **Vũ Trụ 3D tương tác thời gian thực** (Interactive 3D Galaxy Canvas).

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        3D KNOWLEDGE GALAXY CLIENT PIPELINE                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│   [ Backend NestJS / BFF Proxy ] ──(GET /api/v1/universe/overview/active)               │
│                   │                                                                     │
│                   ▼                                                                     │
│   [ TanStack Query v5 Cache ] ──► Nạp Partitions (x,y,z,radius), Stars & Hyperedges    │
│                   │                                                                     │
│                   ▼                                                                     │
│   [ React Three Fiber (R3F) Canvas ]                                                    │
│     ├── <CameraControls />        : Tự do xoay (Orbit), Zoom, Pan trong không gian 3D   │
│     ├── <PostProcessing />        : Hiệu ứng Phát Sáng Tinh Vân (UnrealBloomPass)       │
│     ├── <PartitionNebula />       : Đám mây tinh vân bao bọc từng Module/Service        │
│     ├── <InstancedMesh Stars />   : Render hàng chục nghìn thực thể với hiệu năng 60 FPS│
│     └── <HyperedgeLinks />        : Dây liên kết siêu cạnh (CatmullRomCurve3 Glowing)   │
│                   ▲                                                                     │
│                   │                                                                     │
│   [ Tương Tác 2 Chiều: Raycaster & Cited Chat Integration ]                             │
│     • Click vào Star/Nebula  ──► Mở Inspector Panel bên phải hiển thị Markdown & Bằng chứng│
│     • Bấm Citation ở Chatbot ──► Camera tự động bay (Fly-to Tween) zoom thẳng vào Node! │
│     • Kéo Time Slider        ──► Hoạt cảnh các tinh cầu sinh ra theo lịch sử dự án     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.1. Kiến Trúc Kỹ Thuật 3D Canvas
* **Thư viện chủ đạo:** `@react-three/fiber`, `@react-three/drei`, `three-stdlib`, `@react-three/postprocessing`.
* **Tối ưu hóa hiệu năng (Rendering Optimization):**
  - Sử dụng `THREE.InstancedMesh` để gom hàng nghìn nốt Thực thể (`Entity`) vào một lệnh vẽ (Single Draw Call), duy trì **60 FPS** ổn định trên cả laptop phổ thông không card rời.
  - Sử dụng `LOD (Level of Detail)`: Ở góc nhìn toàn cảnh xa, hiển thị cụm Tinh vân (`universe_partitions`); khi người dùng zoom lại gần, các nốt Thực thể con (`entity`) và Sự kiện (`source_event`) mới dần xuất hiện và phát sáng.
* **Fly-to Camera Tweening:** Khi người dùng tra cứu tài liệu ở trang Trợ lý AI (`/assistant`) và nhấp vào một thẻ trích dẫn Citation, hệ thống kích hoạt hook `useUniverseStore.getState().flyTo(nodeCoordinates)`: Camera 3D sẽ lướt mượt mà qua các tinh vân và cố định góc nhìn vào chính xác nốt tri thức đó, tạo cảm giác trực quan và gây ấn tượng mạnh mẽ cho Hội đồng chấm đồ án.
