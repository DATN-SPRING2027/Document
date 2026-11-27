# Continuum AI — Kiến Trúc Frontend Next.js (App Router)

> Nằm trong tài liệu kiến trúc tổng thể Continuum AI. Xem [Mục lục](README.md).
> **Cập nhật đồng bộ runtime (`2026-11-27` — `FE-UX-007`):** Tài liệu đã được đối soát khớp với kiến trúc thực tế của `DATN_FE` (Next.js 16 App Router, React 19, Tailwind CSS v4 + TailAdmin v2.4, `next-intl`, BFF `/api/backend/[...path]`, raw `three` + `three/examples/jsm/*`, raw WebSocket + SSE).

---

## 1. Lý do lựa chọn Next.js 16 (App Router) & Kiến trúc thực tế

Dự án sử dụng **Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS v4 (`@theme` tokens) và TailAdmin v2.4** cùng `next-intl` cho định tuyến đa ngôn ngữ (`[locale]`):

1. **Ranh giới Server Components (RSC) và Client Components rõ ràng:** `[locale]/layout.tsx`, trang root/route shells và `setRequestLocale` chạy trên server để nạp `next-intl` messages, metadata và font; trong khi shell tương tác (`AdminLayout`, `AppSidebar`, `AppHeader`) và các workspace giàu tương tác (`WorkWorkspace`, `ProjectDocumentsWorkspace`, `AiChatWorkspace`, `ChatWorkspace`, `KnowledgeUniverseWorkspace`, `PlatformConsole`) là Client Components (`"use client"`) được tách mã theo route và `next/dynamic` để tránh thổi phồng bundle ban đầu.
2. **Streaming Server-Sent Events (SSE) & Raw WebSocket:** Trợ lý hỏi đáp AI (`AiChatWorkspace`) tiêu thụ luồng SSE trực tiếp cho token streaming và trích dẫn; Chat nội bộ & Notification realtime dùng **raw WebSocket** với vé một lần (`ws-ticket`) từ backend (không dùng Socket.IO).
3. **Bảo mật Token với HttpOnly Cookies qua BFF `/api/backend/[...path]`:** Route Handler `src/app/api/backend/[...path]/route.ts` đóng vai trò **BFF (Backend-for-Frontend)** giữ Access/Refresh Token trong `HttpOnly` cookies, gắn CSRF token (`x-csrf-token`), `x-request-id`, `x-expected-organization-id`, và trả phản hồi `503` có cấu trúc khi backend tạm ngắt kết nối. Ngoài ra, `src/app/api/health/route.ts` cung cấp health probe độc lập cho container/K8s.
4. **Không cần Micro Frontend:** Feature-Driven Modular Architecture kết hợp App Router route-based code splitting và `next/dynamic({ ssr: false })` cho các module WebGL/3D nặng (Knowledge Universe, 3D Companion).

---

## 2. Cấu trúc thư mục thực tế của `DATN_FE` (Next.js 16 + TailAdmin v2.4)

```text
DATN_FE/
├── src/
│   ├── app/                                    # Next.js 16 App Router
│   │   ├── [locale]/                           # Đa ngôn ngữ (en / vi) qua next-intl (setRequestLocale)
│   │   │   ├── (admin)/                        # Authenticated Workspace Shell (AdminLayout)
│   │   │   │   ├── dashboard/                  # Organization Overview (Manager) / Member Workspace
│   │   │   │   ├── projects/                   # Projects Directory & [projectId] Workspace
│   │   │   │   │   └── [projectId]/            # Overview, Tasks/Sprints, Work Notes, Documents,
│   │   │   │   │                               # Work Reports, Members, Handover, Settings
│   │   │   │   ├── ai-chat/                    # Trợ lý AI Cited Chat (SSE streaming + citations)
│   │   │   │   ├── knowledge-universe/         # Vũ Trụ Tri Thức 3D (lazy-loaded raw Three.js)
│   │   │   │   ├── chat/                       # Team Chat (raw WebSocket + ws-ticket)
│   │   │   │   ├── organization/               # Manager Governance: Members, Invitations, Settings
│   │   │   │   └── platform/                   # Platform Operator Console V2 (Admin scope)
│   │   │   ├── (full-width-pages)/             # Auth (signin, signup, invite accept, 404/error)
│   │   │   ├── layout.tsx                      # Root Locale Server Layout (NextIntlClientProvider)
│   │   │   └── page.tsx                        # Landing / Entry routing
│   │   │
│   │   ├── api/                                # Route Handlers (BFF & Health)
│   │   │   ├── backend/[...path]/route.ts      # BFF Proxy: HttpOnly Cookies + CSRF + Org Context + 503 JSON
│   │   │   └── health/route.ts                 # Liveness/Readiness endpoint cho Docker/K8s
│   │   │
│   │   └── globals.css                         # Tailwind CSS v4 @theme tokens & logical utilities
│   │
│   ├── components/                             # UI & Domain Components
│   │   ├── ui/                                 # TailAdmin primitives (Button, Modal, Badge, Alert, Table)
│   │   ├── common/                             # Breadcrumb, ThemeToggle, LanguageSwitcher, Error states
│   │   ├── header/                             # AppHeader, NotificationDropdown, UserDropdown, Settings
│   │   ├── projects/                           # ProjectWorkspace, ProjectCard, Members, Settings
│   │   ├── work/                               # WorkWorkspace (Tasks, Sprints, Board, Timeline)
│   │   ├── work-notes/                         # Task Notes, Project Documents, Work Reports, SAG Pipeline
│   │   ├── ai-chat/                            # AiChatWorkspace, Citation Cards, Mind-Map drawer
│   │   ├── chat/                               # ChatWorkspace, Attachments, Realtime WS client
│   │   ├── knowledge-universe/                 # KnowledgeUniverseWorkspace (raw `three` + `three/examples/jsm/*`)
│   │   ├── organization-overview/              # OrganizationOverviewDashboard (Manager P0)
│   │   ├── organization-members/               # Membership & Invitation governance
│   │   ├── organization-settings/              # Allowlisted Organization Settings (CAS)
│   │   └── platform/                           # Platform Console V2 screens
│   │
│   ├── icons/                                  # Centralized SVG icon registry (`@/icons`)
│   ├── layout/                                 # AdminLayout, AppSidebar, AppHeader, SidebarFlyoutMenu
│   ├── lib/                                    # api-client, auth/org context helpers, i18n, formatting
│   ├── messages/                               # `en.json`, `vi.json` (next-intl)
│   ├── hooks/                                  # Custom React hooks (TanStack Query, WS, responsive)
│   └── stores/                                 # Zustand stores (Sidebar, lightweight client UI state)
```

---

## 3. Ranh giới Server Components vs Client Components

Để duy trì cân bằng giữa bảo mật, tốc độ tải trang và trải nghiệm tương tác thời gian thực:

### 3.1. Server Components (RSC)
* **Áp dụng cho:**
  - `src/app/[locale]/layout.tsx` và các route `page.tsx` wrappers: gọi `setRequestLocale(locale)`, nạp `next-intl` messages, cấu hình metadata/OpenGraph và truyền props tối giản xuống Client Workspace.
  - Route Handlers (`src/app/api/backend/[...path]/route.ts`, `src/app/api/health/route.ts`): chạy hoàn toàn phía Node.js server để che giấu URL backend nội bộ và giữ token trong `HttpOnly` cookies.

### 3.2. Client Components (`'use client'`)
* **Áp dụng cho Shell tương tác và Domain Workspaces:**
  - **Application Shell (`AdminLayout`, `AppSidebar`, `AppHeader`):** Quản lý trạng thái sidebar, Organization switcher, tìm kiếm project có debounce, và `NotificationDropdown` (tuân thủ RF-02: chỉ tải danh sách đầy đủ khi mở menu, poll nhẹ theo chu kỳ 30 giây).
  - **Trợ lý AI Cited Chat (`components/ai-chat/`):** Tiêu thụ SSE stream (`MESSAGE_DELTA`, grounding citations), lọc project scope theo active membership, và điều hướng tới bằng chứng.
  - **Team Chat & Realtime (`components/chat/`):** Kết nối **raw WebSocket** bằng `ws-ticket` một lần (không dùng Socket.IO), gửi tệp qua streaming attachment API.
  - **Vũ Trụ Tri Thức 3D (`components/knowledge-universe/`):** Lazy-load qua `next/dynamic({ ssr: false })` sử dụng raw **`three`** và **`three/examples/jsm/*`**; đảm bảo hủy `WebGLRenderer`, geometry, material và vòng lặp `requestAnimationFrame` sạch sẽ khi unmount, không dựng canvas WebGL chạy ngầm ở trang ngoài 3D (`FE-PERF-002`, `FE-PERF-011`).
  - **Capture & Task Workspaces (`components/work/`, `components/work-notes/`):** Form Task Note, upload Project Document (presigned flow + `ETag`/`If-Match`), Periodic Work Report và luồng phê duyệt tuân theo quyền trả về từ server.

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
      • Task list/detail/filter và mutation      • Trạng thái Modal, Popup trích dẫn
      • Hộp thư Verification Inbox              • Cờ bật/tắt Micro khi phỏng vấn Audio
      • Lịch sử phiên hỏi đáp Chat              • Draft ghi chú tạm thời trước khi gửi
      • Tự động Invalidate Cache khi            • Bộ lọc hiển thị task
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

## 5. Tích hợp TailAdmin Design System & Quy ước `DATN_FE`

Hệ thống sử dụng bộ giao diện **TailAdmin v2.4 (Tailwind CSS v4)** với các quy ước bắt buộc:
* **Tokens tập trung (`@theme` trong `globals.css`):** Dùng semantic tokens cho Light/Dark Mode (`bg-brand-500`, `text-gray-900 dark:text-white/90`, `border-gray-200 dark:border-gray-800`), tuyệt đối tránh hardcode màu HEX rải rác.
* **Typography & Tabular Numbers:** Font không chân hiện đại kết hợp `tabular-nums` cho mọi cột số liệu/KPI/bảng biểu.
* **Icon Registry (`@/icons`):** Mọi biểu tượng UI chrome đều đi qua `src/icons` (tránh inline `<svg>` trùng lặp).
* **CSS Logical Properties & `next-intl`:** Sử dụng `ms-`/`me-`/`ps-`/`pe-`/`start-`/`end-`/`border-s`/`border-e`/`text-start`/`text-end` thay cho các lớp vật lý trái/phải, đồng thời tách toàn bộ chuỗi hiển thị vào `src/messages/{en,vi}.json`.

---

## 6. Trực Quan Hóa Vũ Trụ Tri Thức 3D (Interactive 3D Knowledge Universe Canvas)

> ⭐ **ĐIỂM NHẤN CỐT LÕI (WOW FACTOR) CỦA ĐỒ ÁN TỐT NGHIỆP**:  
> Thay vì chỉ xem tri thức dưới dạng bảng phẳng, Continuum AI cung cấp trang **`/[locale]/knowledge-universe`** biến đồ thị tri thức dự án thành một **Vũ Trụ 3D tương tác thời gian thực** (Interactive 3D Galaxy Canvas).

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        3D KNOWLEDGE GALAXY CLIENT PIPELINE                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│   [ Next.js BFF /api/backend ] ──► [ NestJS ACL Scope Check ] ──► [ SAG Universe API ]  │
│                   │                                                                     │
│                   ▼                                                                     │
│   [ TanStack Query v5 Cache ] ──► Nạp Partitions (x,y,z,radius), Nodes & Relations      │
│                   │                                                                     │
│                   ▼                                                                     │
│   [ Raw Three.js WebGL Canvas (lazy-loaded via next/dynamic { ssr: false }) ]           │
│     ├── OrbitControls (`three/examples/jsm/controls/OrbitControls`)                     │
│     ├── EffectComposer / UnrealBloomPass (`three/examples/jsm/postprocessing/*`)        │
│     ├── Partition Nebulae & InstancedMesh Nodes                                         │
│     └── Raycaster & Smooth Camera Fly-To Transitions                                    │
│                   ▲                                                                     │
│                   │                                                                     │
│   [ Tương Tác 2 Chiều: Inspector Panel & Citation Focus ]                               │
│     • Click vào Node/Partition ──► Mở Inspector Panel hiển thị nội dung & bằng chứng    │
│     • Chọn Citation / Search   ──► Camera bay mượt tới tọa độ Node mục tiêu             │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.1. Kiến Trúc Kỹ Thuật 3D Canvas (Đồng bộ Runtime)
* **Thư viện thực tế trong `DATN_FE`:** Raw **`three`** kết hợp **`three/examples/jsm/*`** (`OrbitControls`, `EffectComposer`, `RenderPass`, `UnrealBloomPass`) — **không** sử dụng `@react-three/fiber` hay `@react-three/drei`.
* **Tối ưu hóa hiệu năng & vòng đời WebGL:**
  - Tải lười (code-split) toàn bộ thành phần 3D bằng `next/dynamic({ ssr: false })` để không đưa `three` vào bundle các trang dashboard/CRUD thông thường.
  - Loại bỏ WebGL canvas chạy ngầm khi người dùng không mở khu vực 3D (`FE-PERF-002`, `FE-PERF-011`) và `dispose()` đầy đủ renderer/geometry/material/listeners khi unmount để tránh rò rỉ GPU memory.
  - Dùng `THREE.InstancedMesh` để giảm draw calls và duy trì độ mượt tương tác trên laptop phổ thông.
