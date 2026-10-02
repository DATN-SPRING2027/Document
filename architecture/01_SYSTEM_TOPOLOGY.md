# Continuum AI — Topo Hệ Thống & Phân Tầng Mạng (System Topology)

> Nằm trong tài liệu kiến trúc tổng thể Continuum AI. Xem [Mục lục](README.md).

---

## 1. Mô hình phân tầng mạng chuẩn TheSeniorDev

Kiến trúc Continuum AI tuân thủ nghiêm ngặt mô hình luồng giao thông ngang (**Horizontal Highway Pattern**):
Dữ liệu đi một chiều từ ngoài Internet vào Client ➔ Biên mạng Ingress ➔ API Gateway ➔ Mạng nội bộ khép kín (VPC Subnet) chứa các Domain Microservices ➔ Tầng lưu trữ phân tán, hàng đợi và AI Engine.

```
[ INTERNET CLIENTS ]           [ EXTERNAL SERVICES ]
  - Web Browser (Next.js)        - Cloudflare R2 Presigned Upload
  - WebSocket Audio Stream
           │                                    │
           ▼                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 1. TẦNG BIÊN MẠNG (EDGE & INGRESS LAYER)                               │
│   ├── Nginx Ingress Reverse Proxy (Port 80/443, SSL/TLS Termination)   │
│   ├── Origin Cloaking: Giấu toàn bộ IP thật của các container nội bộ   │
│   ├── WebSocket Upgrade Handler: Chuyển tiếp kết nối WSS cho Handover  │
│   └── File-transfer endpoints: Chỉ cấp URL R2 có thời hạn, theo ACL    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (SSL Offloaded - HTTP / gRPC)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. TẦNG CỔNG KIỂM SOÁT NGHIỆP VỤ (API GATEWAY)                        │
│   ├── Centralized JWT Validation & Scoped Claims Extraction            │
│   ├── Redis Token Blacklist Check: Kiểm tra trong <1ms khi Logout      │
│   ├── Distributed Rate Limiter: Thuật toán Token Bucket bảo vệ DDoS    │
│   ├── Pre-Retrieval Scoped ACL Guard: Tính toán P_eff trước khi định tuyến │
│   └── W3C Distributed Tracing Injection (Traceparent Header)          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (Internal Docker Network: `continuum-vpc`)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. VÙNG MẠNG NỘI BỘ BẢO MẬT (ISOLATED VPC SUBNET)                     │
│                                                                        │
│   [CỘT A: QUẢN TRỊ & THU THẬP]       [CỘT B: TRUY XUẤT & BÀN GIAO]     │
│   ├── svc_iam (Auth & 3 Roles)       ├── svc_chat (Assistant & RAG)    │
│   ├── svc_capture (Work Notes)       ├── svc_handover (Audio & Roadmaps)│
│   ├── svc_task (NestJS service)        ├── svc_ingestion (Upload)        │
│   ├── svc_lifecycle (Verify Inbox)   └── svc_ai_engine (SAG - FastAPI) │
│   └── svc_notification (Mail & WSS)                                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│ 4. IN-MEMORY & MESSAGE BROKER TIER   │  │ 5. PERSISTENCE STORAGE TIER  │
│   ├── Redis 7.2 Cluster              │  │   ├── MongoDB 7.0 (rs0)      │
│   │   • L2 Cache & SingleFlight Lock │  │   │   (3-Node Replica Set)   │
│   │   • Realtime Pub/Sub Channels    │  │   │   (Primary Data Truth)   │
│   └── BullMQ Distributed Queue       │  │   ├── LanceDB retrieval target│
│       • ingestion-queue              │  │   │   (Runtime verify)        │
│       • handover-queue               │  │   └── Cloudflare R2          │
│       • mail-queue                   │  │       (Private Object Store) │
│       • dlq-failed-jobs (DLQ)        │  └──────────────────────────────┘
└──────────────────────────────────────┘
```

---

## 2. Chi tiết các phân tầng

### 2.1. Biên mạng Nginx (Edge & Ingress)
* **TLS Termination & SSL Offloading:** Nginx giải mã SSL/TLS tại biên, truyền tải gói tin HTTP không mã hóa vào mạng Docker nội bộ (`continuum-vpc`), giúp giảm hơn **30% tải CPU** cho các backend container.
* **Gzip & Brotli Compression:** Nén tự động các tệp JavaScript, CSS và JSON phản hồi từ Next.js.
* **WebSocket Reverse Proxy:** Nâng cấp HTTP sang `Upgrade: websocket` để phục vụ phiên ghi âm phỏng vấn bàn giao trực tiếp tại `/ws/handover` và chuông thông báo realtime `/ws/notifications`.
* **Task service boundary:** Task là NestJS service chạy process/container riêng, với mã nguồn nằm trong repository DATN_BE hiện tại. Task đọc/ghi task canonical qua API nội bộ; chỉ Task sở hữu `tasks`/`task_events` trong logical database `continuum_task`. Không có Jira import/sync trong MVP. Work Note và Handover chỉ giữ logical `taskId` và gọi contract của Task service.

### 2.2. API Gateway & Kiểm soát truy hồi
* Nằm giữa Nginx và các Domain Services.
* Trích xuất `Authorization: Bearer <access_token>`, giải mã payload JWT chứa:
  $$\text{Payload} = \{\text{userId}, \text{orgId}, \text{roles}, \text{teamIds}, \text{jti}, \text{exp}\}$$
* **Pre-Retrieval Guard:** Kiểm tra quyền sơ bộ trước khi luồng dữ liệu tiến vào các service chuyên biệt, đảm bảo các request không hợp lệ bị ngắt ngay tại cửa sổ gateway với mã HTTP `401 Unauthorized` hoặc `403 Forbidden`.

### 2.3. Mạng nội bộ biệt lập (Isolated VPC Docker Network)
* Các domain services, Redis, MongoDB và SAG retrieval store cùng nằm trong mạng nội bộ riêng; task data chỉ được truy cập qua Task API. Task service sở hữu database logic `continuum_task` trên MongoDB replica set hiện có; không tạo repository hay MongoDB cluster vật lý mới. FE gọi BFF/Gateway; Gateway route nội bộ tới Task service. Capture, Handover và AI Engine dùng API/event contract, không truy cập trực tiếp database Task.
* **Không expose port bừa bãi ra Host:** Chỉ duy nhất port `80/443` của Nginx và port `3000` của Next.js (cho local dev) được publish ra ngoài máy chủ. Cổng MongoDB (`27017`), Redis (`6379`), BullMQ và FastAPI SAG (`8001`) hoàn toàn đóng kín, chỉ giao tiếp nội bộ qua DNS service name của Docker Compose (`http://svc_ai_engine:8001`, `mongodb://db_mongo:27017`).

---

## 3. Topo Docker Compose triển khai chuẩn

```yaml
version: '3.8'

networks:
  continuum-vpc:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16

services:
  # Edge Reverse Proxy
  ingress:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    networks:
      - continuum-vpc

  # Next.js Frontend
  frontend:
    build: ./frontend
    networks:
      - continuum-vpc

  # NestJS API Gateway — cùng backend image/source repository
  api-gateway:
    build: ./backend
    environment:
      - TASK_SERVICE_URL=http://task:3009
      - REDIS_HOST=redis
    networks:
      - continuum-vpc

  # Task microservice — source và build dùng chung repository DATN_BE
  task:
    build: ./backend
    command: node dist/services/task/main.js
    environment:
      - SERVICE_PORT=3009
      - MONGODB_URI=mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0
      - SERVICE_DATABASE=continuum_task
      - REDIS_HOST=redis
    expose:
      - "3009"
    networks:
      - continuum-vpc

  # SAG AI Engine (Python FastAPI)
  ai-engine:
    build: ./ai-service
    volumes:
    networks:
      - continuum-vpc

  # Redis Cluster & BullMQ
  redis:
    image: redis:7.2-alpine
    command: redis-server --appendonly yes
    networks:
      - continuum-vpc

  # MongoDB 3-Node Replica Set
  mongo1:
    image: mongo:7.0
    command: mongod --replSet rs0 --bind_ip_all
    networks:
      - continuum-vpc
```

---

> Đây là sơ đồ đích cho Task, không phải cấu hình đã triển khai. Nó theo mẫu hiện có của DATN_BE deployment: dùng chung image/build từ repository BE, chạy entrypoint riêng (dist/services/task/main.js), cấp SERVICE_PORT và SERVICE_DATABASE, chỉ expose trong mạng nội bộ. Gateway route qua TASK_SERVICE_URL tới HTTP prefix /internal; tên biến/port phải được chốt trong implementation PR.

## 4. Topo Kubernetes (K8s Production Topology)

Trong môi trường Staging và Production, hệ thống bắt buộc chuyển đổi sang mô hình **Cụm Kubernetes điều phối vi dịch vụ**. Toàn bộ cấu hình chi tiết về 5 Namespaces, Deployments, StatefulSets (MongoDB & Redis), Horizontal Pod Autoscaler (HPA theo BullMQ Queue length), NetworkPolicies Zero-Trust và Helm Charts được đặc tả chi tiết tại:

👉 [06_CONTAINER_ORCHESTRATION_K8S.md](06_CONTAINER_ORCHESTRATION_K8S.md)

