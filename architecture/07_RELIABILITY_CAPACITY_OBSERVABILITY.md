# Continuum AI — Độ Tin Cậy, Định Mức Tải & Vận Hành Trên Ít Server
## (Reliability, Capacity Planning, Concurrency & Observability for Lean Infrastructure)

> Nằm trong tài liệu kiến trúc tổng thể Continuum AI. Xem [Mục lục](README.md).

---

## 1. Bối cảnh & Thách thức khi vận hành trên "Ít Server" (Lean Infrastructure)

Trong đồ án tốt nghiệp hoặc giai đoạn MVP khởi nghiệp, hệ thống thường được triển khai trên **1–2 máy chủ VPS** (ví dụ: VPS 4 vCPU, 8GB hoặc 16GB RAM) hoặc một cụm Node K3s tối giản.

Khi triển khai các Bounded Services độc lập (Task cũng chạy process/container riêng trong source DATN_BE hiện tại) cùng MongoDB Replica Set, Redis, BullMQ Workers và FastAPI AI Engine trên tài nguyên phần cứng giới hạn, hai nguy cơ lớn nhất là:
1. **Hiện tượng OOM-Kill (Out of Memory):** Một tiến trình nặng (như OCR tài liệu hoặc Embeddings) nuốt trọn RAM khiến Linux Kernel tự động kill các container cốt lõi như MongoDB hoặc API Gateway.
2. **Nghẽn dây chuyền (Cascading Failure):** Khi CPU chạm ngưỡng 100%, hàng loạt request bị timeout dồn ứ khiến toàn bộ API ngừng phản hồi.

Tài liệu này đặc tả chi tiết các giải pháp kỹ thuật giải quyết trọn vẹn các bài toán SDS còn lại trong điều kiện tài nguyên tối giản.

---

## 2. Capacity Planning & Phân bổ Ngân sách Tài nguyên (Resource Budgeting)

Bảng phân bổ tài nguyên nghiêm ngặt cho một máy chủ **16GB RAM (hoặc 8GB RAM tối thiểu)** đảm bảo không bao giờ bị tràn bộ nhớ:

| Container / Service | Image / Runtime | CPU Request / Limit | RAM Request / Limit | Chiến lược kiểm soát bộ nhớ |
| :--- | :--- | :--- | :--- | :--- |
| **`ingress-nginx`** | `nginx:alpine` | 0.1 / 0.5 core | 64MB / 128MB | Worker processes: auto, keepalive: 64 |
| **`frontend-nextjs`** | `node:22-alpine` (Next.js 16) | 0.2 / 1.0 core | 256MB / 512MB | Node option: `--max-old-space-size=384` |
| **`api-gateway`** | `node:22-alpine` (NestJS 11) | 0.2 / 0.8 core | 256MB / 512MB | Stateless routing, Rate Limiting proxy |
| **`8 NestJS domain services`** | `node:22-alpine` (NestJS 11; shared BE source/build, separate service processes)| 0.8 / 2.0 cores aggregate | 1024MB / 2048MB aggregate | Mỗi service có entrypoint/config/health riêng (`/api/v1/health`, `/api/v1/health/ready`); Task dùng chung build nhưng chạy process riêng. Tách ngân sách theo đo đạc khi triển khai |
| **`ai-engine` (SAG API)** | `python:3.12-slim` (FastAPI + `uv`) | 0.5 / 2.0 cores | 1536MB / 3072MB | PostgreSQL 16 (`sag`) + Qdrant Cloud/Server; single-replica MVP (`InProcJobQueue`) |
| **`sag-postgres`** | `postgres:16-alpine` | 0.25 / 1.0 core | 512MB / 1024MB | Lưu trữ metadata, phiên bản, ACL, đồ thị tri thức và cây Leiden của SAG |
| **`mongodb-rs0`** | `mongo:7.0` (Replica Set) | 0.5 / 1.5 cores | 1024MB / 2048MB | **`wiredTigerCacheSizeGB: 1.0`** (bắt buộc) |
| **`redis-cluster`** | `redis:7.2-alpine` | 0.1 / 0.5 core | 256MB / 512MB | **`maxmemory 400mb`** + **`noeviction`** + **`appendonly yes`** (bắt buộc cho BullMQ) |
| **`bullmq-workers`** | `node:22-alpine` (Worker Pool) | 0.3 / 1.0 core | 512MB / 1024MB | **`concurrency: 2`** (chống nghẽn CPU) |
| **Hệ điều hành & Buffer** | Ubuntu 22.04 LTS | 0.4 core | 2048MB | Dự phòng cho Linux OS & Page Cache |
| **TỔNG CỘNG** | — | **~3.1 / 8.0 cores** | **~7.5GB / 12GB RAM** | **Vận hành an toàn 100% trên VPS 8GB - 16GB** |

### 2.1. Cấu hình đặc trị cho VPS 4GB RAM (Ultra-Lean Profile)

Nếu hệ thống được triển khai trên **1 máy chủ VPS chỉ có 4GB RAM** (hoặc môi trường kiểm thử giá rẻ), các thông số trên được ép chặt xuống ngưỡng tối thiểu:

* **File triển khai thực tế:** [Document/deploy/docker-compose.4gb-ultra-lean.yml](../deploy/docker-compose.4gb-ultra-lean.yml)
* **Bắt buộc kích hoạt Swap Memory 4GB:**
  `sudo fallocate -l 4G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile`
* **Ép Cache MongoDB:** `--wiredTigerCacheSizeGB 0.25` (giới hạn cache 256MB trong RAM).
* **Ép Cache Redis:** `--maxmemory 128mb --maxmemory-policy noeviction --appendonly yes` (không dùng `allkeys-lru` để tránh BullMQ mất job/lock).
* **Ép Node.js Heap Size:** `--max-old-space-size=256` cho Next.js và `--max-old-space-size=384` cho Backend Core.
* **Sử dụng Cloud LLM, Embedding & Qdrant:** Container FastAPI SAG (Python 3.12) không nạp mô hình trọng số lớn cục bộ mà gọi Cloud Embedding/LLM và **Qdrant Cloud**, kết hợp `postgres:16-alpine` cục bộ.
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

Khi có nhiều service process kết nối cùng MongoDB/Redis, việc mở connection bừa bãi sẽ nhanh chóng làm cạn kiệt giới hạn File Descriptors (`ulimit`) của hệ điều hành.

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

Để tìm ra nguyên nhân lỗi khi một thao tác người dùng đi qua nhiều service (Client ➔ Gateway ➔ Domain Service ➔ SAG AI Engine ➔ PG16 / Qdrant), hệ thống áp dụng chuẩn **W3C Traceparent / `X-Request-Id` & `X-Correlation-ID`** (kèm xác thực ký tự an toàn `^[A-Za-z0-9._-]{1,128}$` chống log injection):

```
[ User Request ] ──► [ Ingress / Gateway ] ──► [ Task Service / MongoDB ]
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
[ Bước 1: Lưu File BE (R2/Local) ] ──► Thành công (File objectKey + SHA-256)
          │
          ▼
[ Bước 2: Outbox -> SAG /upload ] ──► Parse & Embed -> PostgreSQL 16 (DocumentVersion staging)
          │
          ▼
[ Bước 3: Upsert Qdrant (<=128/batch) ] ──► THẤT BẠI (Lỗi mạng / Qdrant)
          │
          ▼
┌────────────────────────────────────────────────────────────────────────┐
│ KÍCH HOẠT GIAO DỊCH BÙ TRỪ (COMPENSATING TRANSACTION)                  │
│ 1. Rollback điểm vector theo `document_version_id` trong Qdrant        │
│ 2. Giữ nguyên phiên bản `v1` đang `SEARCH_READY` (không clobber `v1`)  │
│ 3. Cập nhật `knowledgeSync.status = 'FAILED'` và retry qua Outbox      │
│ 4. Không để lại điểm vector mồ côi hoặc dữ liệu split-brain!           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Chiến lược Sao lưu (Backup/Restore) 0đ & Chính sách Xóa mềm (Soft Delete)

### 7.1. Backup tự động toàn bộ 3 kho dữ liệu lên Cloudflare R2 (`INFRA-006`, cập nhật 2026-11-27)
Continuum AI vận hành **3 kho dữ liệu bền vững độc lập**; mọi kịch bản Disaster Recovery **bắt buộc** sao lưu đồng bộ cả 3 kho (không bao giờ truyền hậu tố `/continuum` vào `mongodump`, vì hệ thống dùng kiến trúc database-per-service gồm 10 DB riêng: `continuum_iam`, `continuum_capture`, `continuum_task`, `continuum_handover`, `continuum_chat`, `continuum_notification`, `continuum_audit`, `continuum_jira`, `continuum_ingestion`, `continuum_lifecycle`):

| Kho dữ liệu | Script chuẩn hóa | Tần suất (UTC) | Cơ chế nhất quán & xác minh | Chính sách lưu giữ (Retention) |
| :--- | :--- | :--- | :--- | :--- |
| **MongoDB 7.0** *(toàn bộ 10 service DBs)* | [`deploy/scripts/backup-mongodb-r2.sh`](../deploy/scripts/backup-mongodb-r2.sh) | `03:00` hằng ngày | `mongodump --oplog --archive=... --gzip` (URI **không** có `/<db>`), `gzip -t`, `sha256sum` tải kèm lên R2 | Tự động xóa bản cũ hơn `BACKUP_RETENTION_DAYS=7` ngày trên R2 |
| **PostgreSQL 16** *(SAG `sag` schema)* | [`deploy/scripts/backup-postgres-r2.sh`](../deploy/scripts/backup-postgres-r2.sh) | `03:15` hằng ngày | `pg_dump --format=custom --compress=9`, kiểm tra mục lục `pg_restore --list`, `sha256sum` tải kèm lên R2 | Tự động xóa bản cũ hơn `7` ngày trên R2 |
| **Qdrant** *(per-project vector collections)* | [`deploy/scripts/backup-qdrant-r2.sh`](../deploy/scripts/backup-qdrant-r2.sh) | `03:30` hằng ngày | Gọi Qdrant Snapshot API cho từng collection (`search_units_*`, `routing_tree_*`, `session_units_*`), `sha256sum`, xóa snapshot tạm trên node sau khi tải lên R2 | Cấu hình R2 Bucket Lifecycle Rule `7` ngày cho tiền tố `qdrant/` |

* **Diễn tập phục hồi (Restore Drill & Verification Gate):**
  - Định kỳ hằng tháng (hoặc trong staging CI trước release), kéo bản mới nhất từ R2, kiểm tra khớp `sha256sum -c`, chạy `mongorestore --archive=... --gzip --oplogReplay --dryRun` (xác nhận đủ 10 DB `continuum_*`), chạy `pg_restore --list` / khôi phục thử vào instance PG16 staging, và xác minh khôi phục ít nhất 1 snapshot Qdrant.
* **An toàn chuỗi cung ứng & CI/SCA (`DEP-005`, `INFRA-010`):**
  - Tất cả 5 repository (`DATN_FE`, `DATN_BE`, `sag-laya-integration`, `Document`, `Dataset`) duy trì `.github/dependabot.yml` kiểm tra cập nhật hằng tuần và chạy kiểm định tự động trên cả `push: [main]` lẫn `pull_request` (`npm audit --audit-level=high` cho Node/TS, `pip-audit` cho Python 3.12, kiểm tra YAML/OpenAPI/shell cho `Document`).
* **Chỉ số RPO / RTO mục tiêu (khi cả 3 cronjob & restore drill hoạt động):**
  - **RPO (Recovery Point Objective):** $\le 24\text{ giờ}$ (có thể rút ngắn bằng oplog/WAL archiving khi lên production quy mô lớn).
  - **RTO (Recovery Time Objective):** $\le 30\text{ phút}$ cho MongoDB + PostgreSQL 16 + Qdrant snapshot restore.

### 7.2. Chính sách Xóa mềm (Soft Delete Policy)
* **Quy tắc bất biến:** Không bao giờ gọi lệnh `.deleteOne()` hay `.deleteMany()` trên các bảng tri thức và người dùng.
* Khi xoá thành viên, dự án hoặc tri thức cũ:
  - Cập nhật trường: `deletedAt: new Date()` và `status: 'DEPRECATED' / 'ENDED'`.
  - Mọi câu lệnh truy vấn mặc định áp dụng Mongoose Filter Plugin:
    `this.where({ deletedAt: null });`
  - Đảm bảo toàn bộ bằng chứng lịch sử (Citations & Audit Trails) trong quá khứ không bao giờ bị đứt gãy liên kết (Broken References).
