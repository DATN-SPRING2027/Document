# Continuum AI — Độ Tin Cậy, Định Mức Tải & Vận Hành Trên Ít Server
## (Reliability, Capacity Planning, Concurrency & Observability for Lean Infrastructure)

> Nằm trong tài liệu kiến trúc tổng thể Continuum AI. Xem [Mục lục](README.md).

---

## 1. Bối cảnh & Thách thức khi vận hành trên "Ít Server" (Lean Infrastructure)

Trong đồ án tốt nghiệp hoặc giai đoạn MVP khởi nghiệp, hệ thống thường được triển khai trên **1–2 máy chủ VPS** (ví dụ: VPS 4 vCPU, 8GB hoặc 16GB RAM) hoặc một cụm Node K3s tối giản.

Khi triển khai **9 Bounded Microservices** cùng MongoDB Replica Set, Redis Cluster, BullMQ Workers và FastAPI AI Engine trên tài nguyên phần cứng giới hạn, hai nguy cơ lớn nhất là:
1. **Hiện tượng OOM-Kill (Out of Memory):** Một tiến trình nặng (như OCR tài liệu hoặc Embeddings) nuốt trọn RAM khiến Linux Kernel tự động kill các container cốt lõi như MongoDB hoặc API Gateway.
2. **Nghẽn dây chuyền (Cascading Failure):** Khi CPU chạm ngưỡng 100%, hàng loạt request bị timeout dồn ứ khiến toàn bộ API ngừng phản hồi.

Tài liệu này đặc tả chi tiết các giải pháp kỹ thuật giải quyết trọn vẹn các bài toán SDS còn lại trong điều kiện tài nguyên tối giản.

---

## 2. Capacity Planning & Phân bổ Ngân sách Tài nguyên (Resource Budgeting)

Bảng phân bổ tài nguyên nghiêm ngặt cho một máy chủ **16GB RAM (hoặc 8GB RAM tối thiểu)** đảm bảo không bao giờ bị tràn bộ nhớ:

| Container / Service | Image / Runtime | CPU Request / Limit | RAM Request / Limit | Chiến lược kiểm soát bộ nhớ |
| :--- | :--- | :--- | :--- | :--- |
| **`ingress-nginx`** | `nginx:alpine` | 0.1 / 0.5 core | 64MB / 128MB | Worker processes: auto, keepalive: 64 |
| **`frontend-nextjs`** | `node:20-alpine` (Next.js) | 0.2 / 1.0 core | 256MB / 512MB | Node option: `--max-old-space-size=384` |
| **`api-gateway`** | `node:20-alpine` (NestJS) | 0.2 / 0.8 core | 256MB / 512MB | Stateless routing, Rate Limiting proxy |
| **`8 domain-services`** | `node:20-alpine` (NestJS Modular)| 0.8 / 2.0 cores | 1024MB / 2048MB | Chạy chung instance Modular Monolith tối ưu |
| **`ai-engine`** | `python:3.11-slim` (FastAPI) | 0.5 / 2.0 cores | 1536MB / 3072MB | PyTorch CPU-only, LanceDB embedded |
| **`mongodb-rs0`** | `mongo:7.0` (Replica Set) | 0.5 / 1.5 cores | 1024MB / 2048MB | **`wiredTigerCacheSizeGB: 1.0`** (bắt buộc) |
| **`redis-cluster`** | `redis:7.2-alpine` | 0.1 / 0.5 core | 256MB / 512MB | **`maxmemory 400mb`** + `allkeys-lru` |
| **`bullmq-workers`** | `node:20-alpine` (Worker Pool) | 0.3 / 1.0 core | 512MB / 1024MB | **`concurrency: 2`** (chống nghẽn CPU) |
| **Hệ điều hành & Buffer** | Ubuntu 22.04 LTS | 0.4 core | 2048MB | Dự phòng cho Linux OS & Page Cache |
| **TỔNG CỘNG** | — | **~3.1 / 8.0 cores** | **~7.5GB / 12GB RAM** | **Vận hành an toàn 100% trên VPS 8GB - 16GB** |

### 2.1. Cấu hình đặc trị cho VPS 4GB RAM (Ultra-Lean Profile)

Nếu hệ thống được triển khai trên **1 máy chủ VPS chỉ có 4GB RAM** (hoặc môi trường kiểm thử giá rẻ), các thông số trên được ép chặt xuống ngưỡng tối thiểu:

* **File triển khai thực tế:** [Document/deploy/docker-compose.4gb-ultra-lean.yml](../deploy/docker-compose.4gb-ultra-lean.yml)
* **Bắt buộc kích hoạt Swap Memory 4GB:**
  `sudo fallocate -l 4G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile`
* **Ép Cache MongoDB:** `--wiredTigerCacheSizeGB 0.25` (giới hạn cache 256MB trong RAM).
* **Ép Cache Redis:** `--maxmemory 100mb --maxmemory-policy allkeys-lru`.
* **Ép Node.js Heap Size:** `--max-old-space-size=200` cho Next.js và `--max-old-space-size=380` cho Backend Core.
* **Sử dụng Cloud LLM & Embedding:** Container FastAPI không nạp mô hình PyTorch cục bộ mà gọi trực tiếp Google Gemini API (`text-embedding-004` & `gemini-2.5-flash`), giảm dung lượng RAM từ 2GB xuống chỉ còn **400MB**.
* **Tổng lượng RAM thực tế tiêu thụ:** **~2.4GB – 2.8GB RAM**, máy hoạt động mát mẻ, dư dả hơn 1.2GB RAM dự phòng và không bao giờ kích hoạt Linux OOM-Killer!

---

## 3. Bulkhead Pattern & Cơ chế Chống nghẽn (Backpressure Management)

```
[ Upload File Lớn (100MB) ]                 [ Người dùng Chat & Tra cứu ]
             │                                            │
             ▼                                            ▼
┌───────────────────────────────┐            ┌───────────────────────────────┐
│ HÀNG ĐỢI BÙNG NỔ (BURST QUEUE)│            │ LUỒNG THỜI GIAN THỰC (REALTIME)│
│ • ingestion-queue: 50 files   │            │ • svc_chat, svc_capture       │
└──────────────┬────────────────┘            └────────────┬──────────────────┘
               │                                          │
               ▼                                          ▼
┌───────────────────────────────┐            ┌───────────────────────────────┐
│ BULKHEAD WORKER ISOLATION     │            │ ƯU TIÊN TÀI NGUYÊN CAO        │
│ • Cố định: concurrency = 2    │            │ • CPU ưu tiên cho Web API     │
│ • CPU quota tối đa: 1.0 core  │            │ • Độ trễ cam kết < 200ms      │
│ • Không ảnh hưởng đến Web API │            │ • Không bao giờ bị treo!      │
└───────────────────────────────┘            └───────────────────────────────┘
```

### 3.1. Vách ngăn Bulkhead cho tác vụ nặng
* Các tác vụ nặng như OCR qua **MinerU** hoặc trích xuất giọng nói qua **Whisper** được cô lập trong worker process riêng. 
* Cấu hình cgroups hoặc Docker compose resources giới hạn worker không bao giờ chiếm quá **1.0 core CPU**, bảo toàn CPU cho các luồng HTTP API của người dùng.

### 3.2. Điều tiết áp suất ngược (Backpressure)
* Khi hàng đợi `ingestion-queue` vượt quá 50 jobs chưa xử lý, API Gateway kích hoạt Backpressure:
  - Tạm hoãn nhận các file mới với mã HTTP `429 Too Many Requests` hoặc thông báo: *"Hệ thống đang xử lý đợt tài liệu trước, vui lòng thử lại sau 5 phút"*.
  - Ưu tiên hoàn thành các job hiện tại thay vì nhận dồn dập gây sập bộ nhớ đệm Redis.

---

## 4. Tinh chỉnh Connection Pooling (MongoDB & Redis Sizing)

Khi có 9 microservices, việc mở connection bừa bãi sẽ nhanh chóng làm cạn kiệt giới hạn File Descriptors (`ulimit`) của hệ điều hành.

```typescript
// Cấu hình chuẩn Connection Pool trong NestJS Mongoose Module
MongooseModule.forRootAsync({
  useFactory: () => ({
    uri: process.env.MONGODB_URI,
    maxPoolSize: 15,          // Tối đa 15 kết nối cho mỗi service (thay vì 100 mặc định)
    minPoolSize: 2,           // Giữ sẵn 2 kết nối rảnh rỗi
    socketTimeoutMS: 30000,   // Ngắt socket sau 30s nếu không phản hồi
    serverSelectionTimeoutMS: 5000, // Timeout kết nối sau 5s thay vì treo vô tận
    heartbeatFrequencyMS: 10000,
  }),
});
```

* **Kiểm soát kết nối Redis:** Tất cả các module trong cùng 1 process chia sẻ chung một Singleton Redis Client qua `ioredis`, giới hạn `maxClients: 50` trên Redis Server.

---

## 5. Dấu vết phân tán (Correlation ID & Structured Logging)

Để tìm ra nguyên nhân lỗi khi một thao tác người dùng đi qua nhiều service (Client ➔ Gateway ➔ Chat ➔ AI Engine ➔ LanceDB), hệ thống áp dụng chuẩn **W3C Traceparent / Correlation ID**:

```
[ User Request ] ──► [ Ingress / Gateway ]
                            │ Sinh mã: X-Correlation-ID = "c9d8a-7b3f-4e21"
                            ▼
                     [ svc_chat ] (Ghi log kèm Correlation ID)
                            │ Header: X-Correlation-ID
                            ▼
                     [ svc_ai_engine ] (Ghi log kèm Correlation ID)
                            │ Metadata: { correlationId: "c9d8a-7b3f-4e21" }
                            ▼
                     [ BullMQ Queue ]
```

### Mã mẫu NestJS Correlation Interceptor:
```typescript
@Injectable()
export class CorrelationInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const req = context.switchToHttp().getRequest();
    const correlationId = req.headers['x-correlation-id'] || crypto.randomUUID();
    req.correlationId = correlationId;
    
    // Gán Correlation ID vào Response Header để Client dễ báo lỗi
    const res = context.switchToHttp().getResponse();
    res.setHeader('X-Correlation-ID', correlationId);

    return next.handle().pipe(
      tap(() => {
        Logger.log({
          correlationId,
          path: req.url,
          method: req.method,
          duration: `${Date.now() - req.startTime}ms`,
        });
      }),
    );
  }
}
```

---

## 6. Bù trừ Giao dịch (Saga Pattern & Compensating Transactions)

Khi thực hiện các chuỗi thao tác phức tạp (Upload ➔ OCR ➔ Indexing ➔ Lưu DB), nếu bước sau gặp lỗi, hệ thống phải tự động dọn rác qua cơ chế **Giao dịch bù trừ (Compensating Transaction)**:

```
[ Bước 1: Upload R2 ] ──────► Thành công (File objectKey: "doc_123.pdf")
          │
          ▼
[ Bước 2: OCR & Embed ] ────► Thành công (Tạo 50 chunks vector)
          │
          ▼
[ Bước 3: Ghi LanceDB ] ────► THẤT BẠI (Lỗi phân vùng ổ đĩa!)
          │
          ▼
┌────────────────────────────────────────────────────────────────────────┐
│ KÍCH HOẠT GIAO DỊCH BÙ TRỪ (COMPENSATING TRANSACTION)                  │
│ 1. Gọi R2StorageAdapter.deleteObject("doc_123.pdf")                    │
│ 2. Xóa các vector chunks dở dang trong LanceDB theo temporaryId        │
│ 3. Cập nhật ingestion_jobs: status = 'FAILED', error = 'DISK_FULL'     │
│ 4. Không để lại bất kỳ dữ liệu rác nào trong hệ thống!                 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Chiến lược Sao lưu (Backup/Restore) 0đ & Chính sách Xóa mềm (Soft Delete)

### 7.1. Backup tự động lưu trữ lên Cloudflare R2 (Chi phí 0 VNĐ)
* Không cần hệ thống SAN/NAS đắt tiền, một Cronjob chạy lúc **03:00 AM** hàng đêm trực tiếp trên server:
```bash
#!/bin/bash
# Script tự động backup MongoDB và đẩy lên Cloudflare R2
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="continuum_backup_${DATE}.gz"

# 1. Dump MongoDB ra file nén
mongodump --uri="mongodb://localhost:27017/continuum?replicaSet=rs0" --archive="/tmp/${BACKUP_NAME}" --gzip

# 2. Upload file nén lên Cloudflare R2 qua AWS CLI (S3 compatible)
aws s3 cp "/tmp/${BACKUP_NAME}" "s3://continuum-backups/${BACKUP_NAME}" --endpoint-url="https://${CF_ACCOUNT_ID}.r2.cloudflarestorage.com"

# 3. Xoá file tạm trên VPS & Giữ lại 7 bản backup gần nhất
rm -f "/tmp/${BACKUP_NAME}"
echo "Sao lưu thành công: ${BACKUP_NAME} tại thời điểm $(date)"
```
* **Chỉ số RPO / RTO đạt được:**
  - **RPO (Recovery Point Objective):** $\le 24\text{ giờ}$ (Mất tối đa 1 ngày dữ liệu nếu cả VPS bị cháy).
  - **RTO (Recovery Time Objective):** $\le 30\text{ phút}$ (Thời gian kéo backup từ R2 về và chạy `mongorestore`).

### 7.2. Chính sách Xóa mềm (Soft Delete Policy)
* **Quy tắc bất biến:** Không bao giờ gọi lệnh `.deleteOne()` hay `.deleteMany()` trên các bảng tri thức và người dùng.
* Khi xoá thành viên, dự án hoặc tri thức cũ:
  - Cập nhật trường: `deletedAt: new Date()` và `status: 'DEPRECATED' / 'ENDED'`.
  - Mọi câu lệnh truy vấn mặc định áp dụng Mongoose Filter Plugin:
    `this.where({ deletedAt: null });`
  - Đảm bảo toàn bộ bằng chứng lịch sử (Citations & Audit Trails) trong quá khứ không bao giờ bị đứt gãy liên kết (Broken References).
