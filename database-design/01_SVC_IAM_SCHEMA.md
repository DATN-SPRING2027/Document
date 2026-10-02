# Continuum AI — Schema Dịch Vụ Định Danh & Phân Quyền
## (Identity & Access Management Schema - svc_iam)

> **Database:** `continuum_iam` (MongoDB 7.0)  
> **Service sở hữu độc quyền:** `svc_iam`  
> Nằm trong bộ tài liệu thiết kế Database Microservices Continuum AI. Xem [Mục lục](README.md).

---

## 1. Ranh Giới Nghiệp Vụ & Quyền Hạn (Bounded Context)

> **Governance contract update — 2026-10-02:** `PLATFORM_OPERATOR` is platform-scoped and separate from the Organization roles. `OrganizationMembership` is the authoritative User–Organization relationship, and only `ACTIVE` establishes Organization Context (BE DEC-016). Any authenticated User with active membership in trusted matching context may create a `PRIVATE` Project; the creator receives active ProjectMembership and project-scoped `MEMBER` RoleAssignment atomically. Project creation does not require the legacy `project.create` grant. This is a documentation-level target contract; confirm the implementation/schema and handle any database changes in a separate DB review.

`svc_iam` là dịch vụ nền tảng chịu trách nhiệm về toàn bộ danh tính, cấu trúc doanh nghiệp và phân quyền:
1. **Quản lý Danh tính:** Tài khoản người dùng, băm mật khẩu Bcrypt (12 rounds), phiên đăng nhập an toàn với Refresh Token xoay vòng (Token Rotation) chống replay attack.
2. **Cấu trúc Tổ chức Đa Người Thuê (Multi-Tenant Hierarchy):** `organizations ➔ projects ➔ teams`.
3. **Mô hình role và actor:**
   - `PLATFORM_OPERATOR`: actor vận hành nền tảng; provision Organization và bootstrap Admin đầu tiên; không có mặc định đọc Organization content.
   - `ADMIN`: quản lý User/membership, role/scope và Organization; không mặc định đọc nội dung confidential.
   - `TEAM_LEADER`: quản lý đúng Project/Team scope được gán.
   - `MEMBER`: tham gia theo membership, scope và ACL.
   - Ba role Organization/Project là `ADMIN`, `TEAM_LEADER`, `MEMBER`; `PLATFORM_OPERATOR` không phải role thứ tư trong Organization.
4. **Organization Membership:** `OrganizationMembership` là nguồn chuẩn User–Organization; trạng thái `ACTIVE` duy nhất tạo Organization Context. Unique pair `(organizationId, userId)`; trạng thái được chốt là `PENDING_INVITE`, `ACTIVE`, `SUSPENDED`, `REMOVED`.
5. **Capability grants:** `organization_capability_grants` là schema riêng. Grant `project.create` không còn là điều kiện tạo Project; quyết định này không tự xóa collection hay chốt chính sách cho capability khác.
6. **Phân công chuyên môn lâm thời (Scoped Assignments):** `SME` (Chuyên gia nghiệp vụ) và `KNOWLEDGE_OWNER` (Người phụ trách module) có phạm vi theo từng domain/module cụ thể.

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

// Organization membership and User account status are separate concepts.
export interface IOrganizationMembership {
  organizationId: Types.ObjectId;
  userId: Types.ObjectId;
  status: 'PENDING_INVITE' | 'ACTIVE' | 'SUSPENDED' | 'REMOVED';
}

export interface IProject {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  name: string;
  code: string;                  // VD: "CONT", "PAYMENT"
  description?: string;
  status: 'ACTIVE' | 'ARCHIVED';
  createdBy: Types.ObjectId;     // Provenance only; creator bootstrap is Project MEMBER, not owner/Team Leader
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
  - `organization_memberships`: `(organizationId, userId)` (unique)
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

### 2.5. `organization_capability_grants` (Capability grants — Project-create grant is not required)
```typescript
export interface IOrganizationCapabilityGrant {
  _id: Types.ObjectId;
  organizationId: Types.ObjectId;
  userId: Types.ObjectId;        // Subject of an existing capability grant
  capability: 'project.create'; // Legacy schema value; not a Project-create authorization gate
  grantedBy: Types.ObjectId;     // Issuer recorded for audit
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
