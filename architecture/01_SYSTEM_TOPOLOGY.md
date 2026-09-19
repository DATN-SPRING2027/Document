# Continuum AI — Topo Hệ Thống & Phân Tầng Mạng (System Topology)

> Nằm trong tài liệu kiến trúc tổng thể Continuum AI. Xem [Mục lục](README.md).

---

## 1. Mô hình phân tầng mạng chuẩn TheSeniorDev

Kiến trúc Continuum AI tuân thủ nghiêm ngặt mô hình luồng giao thông ngang (**Horizontal Highway Pattern**):
Dữ liệu đi một chiều từ ngoài Internet vào Client ➔ Biên mạng Ingress ➔ API Gateway ➔ Mạng nội bộ khép kín (VPC Subnet) chứa các Domain Microservices ➔ Tầng lưu trữ phân tán, hàng đợi và AI Engine.

```
[ INTERNET CLIENTS ]           [ EXTERNAL SAAS ]
  - Web Browser (Next.js)        - Atlassian Jira Cloud Webhook
  - WebSocket Audio Stream       - Cloudflare R2 Presigned Upload
           │                                    │
           ▼                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 1. TẦNG BIÊN MẠNG (EDGE & INGRESS LAYER)                               │
│   ├── Nginx Ingress Reverse Proxy (Port 80/443, SSL/TLS Termination)   │
│   ├── Origin Cloaking: Giấu toàn bộ IP thật của các container nội bộ   │
│   ├── WebSocket Upgrade Handler: Chuyển tiếp kết nối WSS cho Handover  │
│   └── Webhook Endpoint: Tiếp nhận Jira Webhooks có đối soát chữ ký     │
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
│   ├── svc_capture (Daily Worklogs)   ├── svc_handover (Audio & Roadmaps)│
│   ├── svc_jira (Jira Sync Connector) ├── svc_ingestion (Upload Coord)  │
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
│   └── BullMQ Distributed Queue       │  │   ├── LanceDB Vector Store   │
│       • ingestion-queue              │  │   │   (Disk-backed Index)    │
│       • jira-sync-queue              │  │   └── Cloudflare R2          │
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
* **Webhook Signature Verification:** Kiểm tra chữ ký HMAC `X-Hub-Signature-256` trước khi định tuyến request webhook của Jira vào hệ thống.

### 2.2. API Gateway & Kiểm soát truy hồi
* Nằm giữa Nginx và các Domain Services.
* Trích xuất `Authorization: Bearer <access_token>`, giải mã payload JWT chứa:
  $$\text{Payload} = \{\text{userId}, \text{orgId}, \text{roles}, \text{teamIds}, \text{jti}, \text{exp}\}$$
* **Pre-Retrieval Guard:** Kiểm tra quyền sơ bộ trước khi luồng dữ liệu tiến vào các service chuyên biệt, đảm bảo các request không hợp lệ bị ngắt ngay tại cửa sổ gateway với mã HTTP `401 Unauthorized` hoặc `403 Forbidden`.

### 2.3. Mạng nội bộ biệt lập (Isolated VPC Docker Network)
* Toàn bộ 9 microservices, Redis, MongoDB và LanceDB cùng nằm trong một mạng bridge riêng biệt: `continuum-net` (Subnet: `172.28.0.0/16`).
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

  # NestJS Core Backend (Chứa các Domain Services)
  backend:
    build: ./backend
    environment:
      - MONGODB_URI=mongodb://mongo1:27017,mongo2:27017,mongo3:27017/continuum?replicaSet=rs0
      - REDIS_HOST=redis
      - SAG_AI_URL=http://ai-engine:8001
    networks:
      - continuum-vpc

  # SAG AI Engine (Python FastAPI)
  ai-engine:
    build: ./ai-service
    volumes:
      - lancedb-data:/app/data/lancedb
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

## 4. Topo Kubernetes (K8s Production Topology)

Trong môi trường Staging và Production, hệ thống bắt buộc chuyển đổi sang mô hình **Cụm Kubernetes điều phối vi dịch vụ**. Toàn bộ cấu hình chi tiết về 5 Namespaces, Deployments, StatefulSets (MongoDB & Redis), Horizontal Pod Autoscaler (HPA theo BullMQ Queue length), NetworkPolicies Zero-Trust và Helm Charts được đặc tả chi tiết tại:

👉 [06_CONTAINER_ORCHESTRATION_K8S.md](06_CONTAINER_ORCHESTRATION_K8S.md)

