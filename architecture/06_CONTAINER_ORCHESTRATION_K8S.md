# Continuum AI — Điều Phối Container Kubernetes (Kubernetes Orchestration)

> Nằm trong tài liệu kiến trúc tổng thể Continuum AI. Xem [Mục lục](README.md).

---

## 1. Tại sao Microservices phải vận hành trên Kubernetes (K8s)?

Khi hệ thống được phân tách thành **9 Bounded Services** kèm các Worker bất đồng bộ, MongoDB Replica Set và Redis Cluster, việc quản lý bằng Docker Compose đơn lẻ chỉ phù hợp cho môi trường máy cục bộ của lập trình viên (Local Development). 

Trong môi trường kiểm thử (Staging) và vận hành sản phẩm (Production), **Kubernetes (K8s)** là nền tảng bắt buộc để giải quyết:
1. **Tự phục hồi (Self-Healing):** Tự động khởi động lại Pod bị crash, tự thay thế Pod khi Node vật lý gặp sự cố phần cứng.
2. **Cân bằng tải nội bộ & Service Discovery:** DNS nội bộ (`http://svc-iam.continuum-core.svc.cluster.local:3000`) tự động định tuyến traffic đến các Pods khỏe mạnh mà không cần cấu hình IP thủ công.
3. **Tự động co giãn (Auto-Scaling - HPA):** Tự động nhân bản số lượng Pod xử lý từ 2 lên 10 khi có đợt tải cao (nhiều người upload tài liệu hoặc nhiều dev cùng xác nhận Daily Worklog).
4. **Cập nhật không gián đoạn (Zero-Downtime Rolling Updates):** Triển khai phiên bản code mới mà người dùng không bị mất kết nối hay gặp lỗi gián đoạn dịch vụ.

### 1.1. Có phải hệ thống luôn luôn bắt buộc dùng Kubernetes nguyên khối?

**Câu trả lời chuẩn kiến trúc:** Kubernetes là **chuẩn mực điều phối vi dịch vụ**, nhưng việc lựa chọn phiên bản Kubernetes nào phụ thuộc hoàn toàn vào quy mô hạ tầng phần cứng:

| Môi trường | Công nghệ điều phối tối ưu | Mức tiêu thụ RAM của bộ máy điều phối | Đánh giá & Khuyến nghị thực tiễn |
| :--- | :--- | :--- | :--- |
| **Production Doanh nghiệp** (Cụm Cloud Multi-Nodes: AWS EKS, GCP GKE) | **Kubernetes Chuẩn (Full K8s)** | ~1.5GB – 2GB RAM cho Control Plane | Áp dụng khi có nhiều máy chủ vật lý, cần autoscaling liên node và tích hợp dịch vụ Cloud Provider. |
| **Production Tối Giản / 1 Máy chủ VPS** (VPS 4GB – 8GB RAM) | **K3s (Lightweight Kubernetes - CNCF Certified)** | **~350MB – 512MB RAM** (Rất nhẹ) | **GIẢI PHÁP HOÀN HẢO:** K3s do Rancher phát triển, được Cloud Native Computing Foundation (CNCF) chứng nhận chuẩn K8s 100%. Toàn bộ file cấu hình `yaml` trong thư mục `deploy/k8s/` của dự án **chạy trực tiếp trên K3s** mà không cần thay đổi bất kỳ dòng mã nào. |
| **Local Development** (Máy tính cá nhân của lập trình viên) | **Docker Compose** | **~50MB RAM** | Giúp lập trình viên khởi động nhanh toàn bộ 9 services trong 10 giây bằng lệnh `docker compose up -d` mà không cần cài đặt cụm cluster phức tạp. |

> 💡 **Khẳng định kiến trúc:** Dự án thiết kế **Thống nhất 100% về chuẩn Kubernetes (K8s API)**. Khi chạy trên cụm máy chủ lớn, hệ thống chạy trên K8s chuẩn; khi chạy trên 1 VPS 4GB RAM tiết kiệm chi phí, hệ thống chạy trên **K3s** hoặc **Docker Compose Ultra-Lean**. Cả hai đều dùng chung Docker Images và chung biến môi trường!

---

## 2. Kiến trúc phân vùng Cụm (Kubernetes Cluster Topology)

Hệ thống phân chia không gian làm việc thành **5 Namespaces độc lập** nhằm thực thi nguyên tắc phòng thủ theo chiều sâu (Defense-in-Depth):

```
┌────────────────────────────────────────────────────────────────────────┐
│                   KUBERNETES CLUSTER (CONTINUUM AI)                    │
│                                                                        │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ Namespace: continuum-ingress                                   │   │
│   │ • Nginx Ingress Controller (LoadBalancer Service, Port 80/443) │   │
│   │ • Cert-Manager (Tự động cấp & gia hạn SSL Let's Encrypt)       │   │
│   └───────────────────────────────┬────────────────────────────────┘   │
│                                   │                                    │
│                                   ▼                                    │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ Namespace: continuum-core (Business Workloads)                 │   │
│   │ • Frontend Next.js Deploy (2-4 Replicas)                       │   │
│   │ • API Gateway Deploy (3 Replicas)                              │   │
│   │ • 8 NestJS Domain Services Deploy (2 Replicas mỗi service)     │   │
│   │ • BullMQ Worker Deployments (ingestion-worker, mail-worker)    │   │
│   └───────────────────────┬────────────────────────┬───────────────┘   │
│                           │                        │                   │
│                           ▼                        ▼                   │
│   ┌───────────────────────────────┐ ┌──────────────────────────────┐   │
│   │ Namespace: continuum-ai       │ │ Namespace: continuum-data    │   │
│   │ • FastAPI SAG Engine Deploy   │ │ • MongoDB StatefulSet (3 Pods│   │
│   │   (2-6 Replicas với HPA)      │ │   với PVC NVMe StorageClass) │   │
│   │ • MinerU OCR Worker Pods      │ │ • Redis Cluster StatefulSet  │   │
│   │ • LanceDB Persistent Volume   │ │   (Primary - Replica)        │   │
│   └───────────────────────────────┘ └──────────────────────────────┘   │
│                                                                        │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ Namespace: continuum-monitoring (Observability)                │   │
│   │ • OpenTelemetry Collector Pods • Prometheus & Grafana • Loki   │   │
│   └────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Quản lý Workloads: Deployments vs StatefulSets

### 3.1. Nhóm Dịch vụ Không trạng thái (Stateless Services) ➔ `Deployment`
Áp dụng cho Frontend Next.js, API Gateway, các NestJS Domain Services và BullMQ Workers.

* **Chiến lược RollingUpdate không gián đoạn:**
  ```yaml
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%         # Cho phép tạo vượt 25% pod mới trước khi xoá pod cũ
      maxUnavailable: 0     # Không bao giờ để số pod sẵn sàng thấp hơn cấu hình
  ```
* **Mẫu cấu hình Deployment của `svc_chat`:**
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: svc-chat-deployment
    namespace: continuum-core
  spec:
    replicas: 2
    selector:
      matchLabels:
        app: svc-chat
    template:
      metadata:
        labels:
          app: svc-chat
      spec:
        containers:
          - name: svc-chat
            image: continuum/svc-chat:v2.1.0
            ports:
              - containerPort: 3000
            resources:
              requests:
                cpu: "250m"
                memory: "512Mi"
              limits:
                cpu: "1000m"
                memory: "1024Mi"
            envFrom:
              - configMapRef:
                  name: continuum-common-config
              - secretRef:
                  name: continuum-secrets
            livenessProbe:
              httpGet:
                path: /healthz
                port: 3000
              initialDelaySeconds: 15
              periodSeconds: 10
            readinessProbe:
              httpGet:
                path: /ready
                port: 3000
              initialDelaySeconds: 5
              periodSeconds: 5
            lifecycle:
              preStop:
                exec:
                  command: ["/bin/sh", "-c", "sleep 10"] # Chờ drain connection
  ```

### 3.2. Nhóm Dịch vụ Có trạng thái (Stateful Services) ➔ `StatefulSet`
Áp dụng cho MongoDB Replica Set 3 nodes và cụm Redis.

* **Định danh mạng cố định:** Các pod có tên tuần tự (`mongo-0`, `mongo-1`, `mongo-2`) và địa chỉ DNS ổn định (`mongo-0.mongo-headless.continuum-data.svc.cluster.local`).
* **Volume Claim Templates (Gắn ổ đĩa riêng biệt):** Mỗi pod MongoDB được cấp riêng một PersistentVolume SSD NVMe dung lượng 50GB qua `StorageClass: fast-ssd`. Khi pod bị xoá hoặc chuyển Node, dữ liệu ổ cứng vẫn giữ nguyên và tự động gắn lại.

---

## 4. Cơ chế Tự động Co giãn Quy mô (Horizontal Pod Autoscaler - HPA)

Hệ thống kết hợp co giãn theo chỉ số tài nguyên tiêu chuẩn và chỉ số nghiệp vụ thời gian thực (Custom Metrics via Prometheus Adapter):

```
                                    ┌────────────────────────┐
                                    │ Prometheus Metric:     │
                                    │ bullmq_waiting_jobs    │
                                    └───────────┬────────────┘
                                                │
                                                ▼
┌──────────────────────┐  (Queue > 50 jobs) ┌────────────────────────┐
│ Metrics Server       ├───────────────────►│ K8s HPA Controller     │
│ (CPU > 75%)          │                    └───────────┬────────────┘
└──────────────────────┘                                │
                                                        ▼
                                    ┌────────────────────────┐
                                    │ Scale Ingestion Workers│
                                    │ từ 2 ➔ 8 Pods tức thời!│
                                    └────────────────────────┘
```

### 4.1. HPA theo chỉ số CPU & RAM cho Web APIs
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: svc-chat-hpa
  namespace: continuum-core
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: svc-chat-deployment
  minReplicas: 2
  maxReplicas: 8
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 75
```

### 4.2. HPA theo Độ dài Hàng đợi BullMQ (Custom Queue Metrics)
* Khi người dùng tải lên hàng loạt tài liệu lớn, số lượng job chờ trong `ingestion-queue` tăng vọt. Thay vì để người dùng chờ lâu, K8s tự động tăng số lượng Pods bóc tách tài liệu từ 2 lên tối đa 10 pods:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ingestion-worker-hpa
  namespace: continuum-core
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ingestion-worker-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: External
      external:
        metric:
          name: bullmq_queue_waiting_jobs
          selector:
            matchLabels:
              queue_name: "ingestion-queue"
        target:
          type: AverageValue
          averageValue: 20 # Mỗi worker gánh 20 jobs, vượt quá thì scale thêm
```

---

## 5. Probes & Vòng đời Pod (Zero-Downtime Lifecycle)

Nhằm triệt tiêu tình trạng "Pod chưa nạp xong kết nối Database đã nhận request" (gây lỗi 502/500 cho người dùng), K8s cấu hình nghiêm ngặt 3 loại Probes:

| Loại Probe | Mục đích | Hành động khi thất bại |
| :--- | :--- | :--- |
| **Startup Probe** | Kiểm tra Pod đã nạp xong code và khởi động server chưa. Cho phép NestJS/Python nạp models trong tối đa 60 giây. | Chờ tiếp, chưa kích hoạt liveness/readiness. |
| **Readiness Probe** (`/ready`) | Kiểm tra kết nối MongoDB, Redis, LanceDB có thông suốt không. | Ngắt traffic: Ingress lập tức không chuyển request vào Pod này cho đến khi sẵn sàng. |
| **Liveness Probe** (`/healthz`) | Kiểm tra tiến trình có bị deadlock, rò rỉ bộ nhớ (OOM) hay đơ loop không. | Tự động **Kill và Restart** pod mới thay thế. |

### Cơ chế Tắt an toàn (Graceful Shutdown):
Khi có lệnh cập nhật phiên bản mới:
1. K8s gửi tín hiệu `SIGTERM` tới ứng dụng.
2. `preStop` hook tạm dừng 10 giây để Ingress Router rút Pod ra khỏi bảng định tuyến.
3. NestJS đóng kết nối nhận request mới, hoàn tất nốt các HTTP requests hoặc BullMQ job đang xử lý dở trong tối đa 30 giây (`terminationGracePeriodSeconds: 30`).
4. Đóng kết nối Database MongoDB và Redis an toàn rồi mới kết thúc tiến trình.

---

## 6. Chính sách Cách ly Mạng (Zero-Trust Network Policies)

Mặc định trong Kubernetes, tất cả các Pod ở mọi namespace đều có thể gửi gói tin tới nhau. Continuum AI áp dụng **NetworkPolicy** để thiết lập tường lửa nội bộ:

* **Quy tắc 1:** Chỉ duy nhất các Pod có nhãn `app: api-gateway` và `app: frontend` mới được nhận traffic từ Ingress Controller.
* **Quy tắc 2:** Các `domain-services` chỉ được gọi ra MongoDB (`port 27017`) và Redis (`port 6379`), hoàn toàn không được giao tiếp chéo trái phép.
* **Quy tắc 3:** Database MongoDB và Redis chỉ chấp nhận kết nối từ các Pod trong namespace `continuum-core` và `continuum-ai`, chặn hoàn toàn truy cập từ bên ngoài.

---

## 7. Cấu trúc đóng gói Helm Chart chuẩn (`charts/continuum-ai/`)

Để tự động hóa triển khai trên mọi môi trường (Minikube, K3s, AWS EKS, GCP GKE), toàn bộ cấu hình Kubernetes được đóng gói dưới dạng **Helm Chart v3**:

```text
charts/continuum-ai/
├── Chart.yaml                          # Siêu dữ liệu Helm Chart (name, version, appVersion)
├── values.yaml                         # Cấu hình biến mặc định (replicas, image tags, resources)
├── values-staging.yaml                 # Cấu hình tối ưu chi phí cho Staging (1 replica, CPU thấp)
├── values-production.yaml              # Cấu hình chịu tải cao cho Production (Multi-replicas, HPA)
└── templates/
    ├── _helpers.tpl                    # Template macros tái sử dụng tên, labels
    ├── ingress.yaml                    # Cấu hình Nginx Ingress & TLS Let's Encrypt
    ├── frontend-deployment.yaml        # Workload Next.js App Router
    ├── backend-deployments.yaml        # Workloads 8 NestJS Domain Services
    ├── ai-engine-deployment.yaml       # Workload FastAPI SAG Engine & LanceDB PVC
    ├── worker-deployments.yaml         # Workloads BullMQ Processors
    ├── hpa.yaml                        # Bộ cấu hình Horizontal Pod Autoscaler
    ├── network-policies.yaml           # Bộ tường lửa cách ly Pods
    ├── configmaps.yaml                 # Biến môi trường không nhạy cảm
    └── secrets.yaml                    # Khóa bí mật JWT, DB Credentials mã hóa
```

* **Lệnh triển khai một dòng lệnh:**
  ```bash
  helm upgrade --install continuum-ai ./charts/continuum-ai -f ./charts/continuum-ai/values-production.yaml --namespace continuum-core --create-namespace
  ```
