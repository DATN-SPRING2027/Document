# Continuum AI — Schema Dịch Vụ Định Danh & Phân Quyền
## (Identity & Access Management Schema - svc_iam)

> **Database:** `continuum_iam` (MongoDB 7.0)  
> **Service sở hữu độc quyền:** `svc_iam`  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ & Quyền Hạn (Bounded Context)

`svc_iam` là dịch vụ nền tảng chịu trách nhiệm về toàn bộ danh tính, cấu trúc doanh nghiệp và phân quyền:
1. **Quản lý Danh tính:** Tài khoản người dùng, băm mật khẩu Bcrypt (12 rounds), phiên đăng nhập an toàn với Refresh Token xoay vòng (Token Rotation) chống replay attack.
2. **Cấu trúc Tổ chức Đa Người Thuê (Multi-Tenant Hierarchy):** `organizations ➔ projects ➔ teams`.
3. **Mô hình 3 Vai Trò Cố Định (Fixed 3-Tier Roles):**
   - `ADMIN`: Quản trị viên toàn tổ chức.
   - `TEAM_LEADER`: Trưởng nhóm kỹ thuật/dự án.
   - `MEMBER`: Kỹ sư phần mềm đóng góp.
4. **Cấp quyền đặc biệt có kiểm toán (`organization_capability_grants`):** Quyền `project.create` được Admin cấp riêng cho Team Leader có thời hạn.
5. **Phân công chuyên môn lâm thời (Scoped Assignments):** `SME` (Chuyên gia nghiệp vụ) và `KNOWLEDGE_OWNER` (Người phụ trách module) có phạm vi theo từng domain/module cụ thể.

---

## 2. Chi Tiết Schemas Mongoose (Database: `continuum_iam`)

### 2.1. `users` (Tài khoản người dùng)
```typescript
export interface IUser {
  _id: Types.ObjectId;
  email: string;
  passwordHash: string;          // Bcrypt 12 rounds
  fullName: string;
  avatarUrl?: string;
  status: 'ACTIVE' | 'SUSPENDED' | 'PENDING_INVITE';
  
  // Xác thực hai lớp (2FA/TOTP) - Tùy chọn
  twoFactorEnabled: boolean;
  twoFactorSecretEncrypted?: string;
  
  lastLoginAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `email`: `{ unique: true, lowercase: true, trim: true }`
  - `(status, createdAt)`: `{ index: true }`

---

### 2.2. `organizations`, `projects`, `teams` (Cấu trúc tổ chức phân cấp)
```typescript
export interface IOrganization {
  _id: Types.ObjectId;
  name: string;
  slug: string;
  plan: 'FREE' | 'ENTERPRISE';
  settings?: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

export interface IProject {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  name: string;
  code: string;                  // VD: "CONT", "PAYMENT"
  description?: string;
  status: 'ACTIVE' | 'ARCHIVED';
  createdBy: Types.ObjectId;     // User tạo (Phải có grant 'project.create')
  createdAt: Date;
  updatedAt: Date;
}

export interface ITeam {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  name: string;
  code: string;                  // VD: "BACKEND", "MOBILE"
  description?: string;
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục:**
  - `organizations`: `slug` (unique)
  - `projects`: `(organizationId, code)` (unique)
  - `teams`: `(organizationId, projectId, code)` (unique)

---

### 2.3. `project_memberships` & `team_memberships` (Tư cách thành viên)
```typescript
export interface IProjectMembership {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  userId: Types.ObjectId;
  status: 'ACTIVE' | 'INACTIVE';
  joinedAt: Date;
}

export interface ITeamMembership {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  teamId: Types.ObjectId;
  userId: Types.ObjectId;
  joinedAt: Date;
}
```
* **Chỉ mục:**
  - `project_memberships`: `(projectId, userId)` (unique)
  - `team_memberships`: `(teamId, userId)` (unique)

---

### 2.4. `roles` & `role_assignments` (Hệ thống 3 Roles Tĩnh)
```typescript
export interface IRole {
  _id: Types.ObjectId;
  code: 'ADMIN' | 'TEAM_LEADER' | 'MEMBER';
  name: string;
  permissions: string[];         // Tập quyền hạt mịn chuẩn
  isSystem: boolean;
}

export interface IRoleAssignment {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId?: Types.ObjectId;
  userId: Types.ObjectId;
  roleId: Types.ObjectId;
  roleCode: 'ADMIN' | 'TEAM_LEADER' | 'MEMBER';
  assignedBy: Types.ObjectId;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `roles`: `code` (unique)
  - `role_assignments`: `(organizationId, projectId, userId)` (unique)

---

### 2.5. `organization_capability_grants` (Cấp quyền tạo dự án cho Team Leader)
```typescript
export interface IOrganizationCapabilityGrant {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  userId: Types.ObjectId;        // Phải là TEAM_LEADER
  capability: 'project.create';
  grantedBy: Types.ObjectId;     // ADMIN cấp
  reason: string;
  expiresAt?: Date;              // Thời hạn hiệu lực
  revokedAt?: Date;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(organizationId, userId, capability, revokedAt)`: `{ index: true }`

---

### 2.6. `refresh_sessions` (Quản lý phiên xoay vòng Refresh Token an toàn)
```typescript
export interface IRefreshSession {
  _id: Types.ObjectId;
  userId: Types.ObjectId;
  organizationId: Types.ObjectId;
  tokenHash: string;             // SHA-256 băm của refresh token
  ipAddress?: string;
  userAgent?: string;
  isRevoked: boolean;
  expiresAt: Date;               // Thường là 7 ngày
  createdAt: Date;
  updatedAt: Date;
}
```
* **Chỉ mục & TTL:**
  - `tokenHash`: `{ unique: true }`
  - `(userId, isRevoked, expiresAt)`: `{ index: true }`
  - `expiresAt`: `{ expireAfterSeconds: 0 }` (Tự động xóa phiên hết hạn)

---

### 2.7. `sme_assignments` & `knowledge_owner_assignments` (Phân công vai trò lâm thời)
```typescript
export interface ISmeAssignment {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  userId: Types.ObjectId;
  domainModule: string;          // VD: "CORE_PAYMENT", "AUTH_SECURITY"
  assignedBy: Types.ObjectId;
  effectiveFrom: Date;
  effectiveTo?: Date;
  createdAt: Date;
}

export interface IKnowledgeOwnerAssignment {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  projectId: Types.ObjectId;
  userId: Types.ObjectId;
  knowledgeObjectId?: Types.ObjectId;
  assignedBy: Types.ObjectId;
  effectiveFrom: Date;
  effectiveTo?: Date;
  createdAt: Date;
}
```
* **Chỉ mục:**
  - `(projectId, userId, domainModule)`: `{ index: true }`
  - `(knowledgeObjectId, effectiveTo)`: `{ index: true }`

---

## 3. Domain Events Do `svc_iam` Xuất Bản (Outbox Events)

Khi có thay đổi trạng thái danh tính, `svc_iam` bắn các sự kiện sau vào BullMQ/Redis:
- `iam.user.registered`: Khi tài khoản được kích hoạt.
- `iam.role.assigned`: Cập nhật vai trò (để cache phân quyền Gateway vô hiệu hóa ngay).
- `iam.capability.granted`: Khi Team Leader được cấp quyền tạo dự án.
- `iam.session.revoked`: Khi đăng xuất toàn bộ phiên.
