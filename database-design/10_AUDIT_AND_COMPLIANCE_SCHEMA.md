# Continuum AI — Schema Dịch Vụ Kiểm Toán & Tuân Thủ Bảo Mật
## (Cross-Cutting Audit Trail & Compliance Schema - continuum_audit)

> **Database:** `continuum_audit` (MongoDB 7.0)  
> **Phạm vi:** Toàn hệ thống (Cross-Cutting Concern)  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ (Bounded Context)

`continuum_audit` là kho lưu trữ nhật ký độc lập, bất biến (Append-Only) phục vụ:
1. **Truy Vết An Ninh & Trách Nhiệm Giải Trình:** Ghi lại mọi hành động làm thay đổi trạng thái quan trọng (Ai, đã làm gì, vào thời điểm nào, từ địa chỉ IP nào, trạng thái dữ liệu trước và sau khi đổi ra sao).
2. **Tuân Thủ Tiêu Chuẩn Bảo Mật Doanh Nghiệp (SOC 2, ISO 27001):**
   - Đảm bảo tính toàn vẹn của dữ liệu tri thức, phát hiện các trường hợp xóa mềm bất thường hoặc thay đổi quyền hạn trái phép.
3. **Chính Sách Lưu Trữ & Tự Động Xóa (Data Retention Policy):** Quy định thời gian lưu trữ tối thiểu của nhật ký kiểm toán (thường là 365 ngày) và cơ chế dọn dẹp an toàn.

---

## 2. Chi Tiết Schemas Mongoose (Database: `continuum_audit`)

### 2.1. `audit_logs` (Nhật ký kiểm toán bất biến - Immutable Audit Trail)
```typescript
export interface IAuditLog {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId?: Types.ObjectId;
  
  actorUserId?: string;              // Null nếu là tác vụ ngầm SYSTEM
  actorEmail?: string;
  actorRole?: string;
  
  action: 
    | 'USER_LOGIN'
    | 'USER_LOGOUT'
    | 'ROLE_ASSIGNED'
    | 'CAPABILITY_GRANTED'
    | 'CAPABILITY_REVOKED'
    | 'KNOWLEDGE_PROPOSAL_CREATED'
    | 'KNOWLEDGE_VERIFIED'
    | 'KNOWLEDGE_DEPRECATED'
    | 'HANDOVER_INITIATED'
    | 'HANDOVER_ITEM_VERIFIED'
    | 'DOCUMENT_UPLOADED'
    | 'DOCUMENT_DELETED';
    
  targetResource: string;            // Tên collection/table (VD: "knowledge_versions")
  targetResourceId: string;          // ID bản ghi bị tác động
  
  // Dữ liệu chi tiết trước và sau khi thay đổi (Diff Payload)
  diffPayload?: {
    before?: Record<string, any>;
    after?: Record<string, any>;
  };
  
  ipAddress?: string;
  userAgent?: string;
  
  createdAt: Date;                   // Bất biến, KHÔNG CÓ updatedAt
}
```
* **Chỉ mục:**
  - `(organizationId, projectId, createdAt)`: `{ index: true }`
  - `(actorUserId, createdAt)`: `{ index: true }`
  - `(targetResource, targetResourceId)`: `{ index: true }`

---

### 2.2. `compliance_reports` (Báo cáo tuân thủ định kỳ)
Lưu lại kết quả rà soát tự động hàng tuần/tháng về mức độ tuân thủ tri thức của dự án.

```typescript
export interface IComplianceReport {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  
  reportPeriod: string;              // VD: "2026-W38", "2026-09"
  totalResponsibilitiesCount: number;
  unassignedResponsibilitiesCount: number;
  unfulfilledRequirementsCount: number;
  openKnowledgeGapsCount: number;
  complianceScorePercent: number;    // 0 -> 100%
  
  generatedAt: Date;
  summaryFindings: string[];
}
```
* **Chỉ mục:**
  - `(organizationId, projectId, reportPeriod)`: `{ unique: true }`

---

### 2.3. `data_retention_policies` (Chính sách lưu trữ và dọn rác)
```typescript
export interface IDataRetentionPolicy {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  
  resourceType: 'AUDIT_LOGS' | 'CHAT_MESSAGES' | 'TEMP_DRAFTS' | 'JIRA_EVENTS';
  retentionDays: number;             // VD: audit_logs = 365, chat_messages = 90
  isAutoDeleteEnabled: boolean;
  
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, resourceType)`: `{ unique: true }`
