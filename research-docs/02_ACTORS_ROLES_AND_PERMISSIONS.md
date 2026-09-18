# CONTINUUM AI — Actors, roles and permissions

## Document status

- Status: Accepted MVP authorization baseline
- Date: 2026-09-18
- Scope: One software project with multiple teams; organizational identity/capability layer only where needed to create a project

## 1. Decision

The three persistent **human roles** are `ADMIN`, `TEAM_LEADER` and `MEMBER`. `SME` (Subject Matter Expert), `KNOWLEDGE_OWNER` and `SUCCESSOR` are scoped, time-bounded **assignments**, not roles. `ONBOARDING` and `OFFBOARDING` are membership states, not roles. `PROJECT_MANAGER`, `PROJECT_ADMIN` and `TEAM_MEMBER` are superseded names and must not be used as new role codes.

An `ADMIN` grants the organization-level capability `project.create` separately to a `TEAM_LEADER`. Team leadership alone **never** implies this capability. The grant is explicit, revocable, time-bounded if appropriate, and audited. A leader cannot self-grant it or pass it to another person. An authorized leader may create a project, but that action does not make them an `ADMIN` or give access to other projects.

## 2. Scope and authorization

```text
Organization (ADMIN, explicit project.create capability grants)
  └── Project (membership and project policy)
       ├── Team A (TEAM_LEADER, MEMBER)
       └── Team B (TEAM_LEADER, MEMBER)
            └── Domain / resource ACL / temporary assignments
```

Effective access depends on active organization/project/team membership, persistent role, explicit capability grant, scoped assignment, resource/source ACL, lifecycle state, and explicit deny. **Deny takes precedence.** Authorization is enforced by NestJS before retrieval and again before passing a citation or snippet to the LLM. Client-side guards are only UX. No role or assignment automatically bypasses a confidential source ACL.

Role and assignment records need `organizationId`, subject, scope, `validFrom`, optional `validUntil`, `assignedBy` and audit reference. An expired/revoked grant has no effect. Cross-tenant or cross-project access must be explicitly authorized, not inferred from a matching email or title.

## 3. Human actors

### ADMIN

- Manages organization users, project/team membership, role assignments, scoped capability grants, integrations, source policies and audit.
- May create projects and assign leaders. May manage project/team configuration according to organization policy.
- May inspect technical status and metadata; **does not automatically read confidential content or verify knowledge**. Exceptional access, if implemented, requires a separately approved, reasoned and audited process.

### TEAM_LEADER

- Manages assigned project/team workspaces, members and knowledge requirements within granted scope; tracks who owns each domain/module; follows up on missing updates and reviews handover.
- May create teams and invite/add members **within an existing project only if project policy permits**. May grant ordinary member access within their scope, never a role/capability broader than their delegation, and never override source ACL.
- May create a **new project only if an ADMIN has granted `project.create` at organization scope**. On creation, project membership/initial team-leader assignment is established by an audited bootstrap policy; no implicit organization-admin rights follow.
- Can review/approve knowledge only within a policy-authorized team/domain scope and after evidence checks. Specialist verification should use an SME or Knowledge Owner assignment.

### MEMBER

- Contributes manual notes and documents, records what was done/how/why, maintains assigned knowledge, asks the assistant, flags gaps, and participates in transfer.
- Reads only resources permitted by active membership and ACL. Creating a note or uploading a source does not authorize self-verification or wider disclosure.

Every leader is also expected to contribute knowledge; contribution is not delegated solely to members.

## 4. Scoped assignments and lifecycle

| Assignment/state | Meaning | Permission effect |
| --- | --- | --- |
| `SME` | Expert for a specified domain/module/process/requirement and period | Can review/interview/verify claims **only in that scope**, subject to source ACL and approval policy. |
| `KNOWLEDGE_OWNER` | Accountable maintainer of a knowledge object or required knowledge area | Can maintain, request review, approve/reject or supersede in scope according to policy; does not gain all project data. |
| `SUCCESSOR` | Takes over a defined responsibility/handover package | Sees the approved package **and** only evidence allowed by its ACL; never inherits predecessor permissions. |
| `ONBOARDING` / `OFFBOARDING` | Membership lifecycle state | May narrow permitted actions or trigger checklists/reminders; neither is an RBAC role. |

Human review is required before AI-proposed knowledge becomes verified/active. The reviewer must be authorized for both the domain and evidence. A person should not approve their own sensitive proposal where separation of duties is required.

## 5. Permission matrix (baseline)

`Yes` always means “within active scope and ACL”; `Grant` means an explicit, audited capability/policy grant; `Assigned` means a matching scoped assignment.

| Action | ADMIN | TEAM_LEADER | MEMBER | Scoped assignment |
| --- | --- | --- | --- | --- |
| Create project | Yes | **Grant: `project.create` at organization scope** | No | No |
| Create team / add member in existing project | Yes | Grant by project policy, assigned project/team only | No | No |
| Assign persistent roles or `project.create` | Yes | No | No | No |
| Configure Jira/R2 connector or source ACL | Yes | Limited delegated project policy; no privilege escalation | No | No |
| Add manual work/task note; upload allowed source | Yes | Yes | Yes | No extra right |
| View authorized knowledge / ask chat | Yes | Yes | Yes | No ACL bypass |
| Propose knowledge or report gap | Yes | Yes | Yes | No extra right |
| Verify, reject or supersede knowledge | Not by admin role alone | Authorized team/domain policy | No by member role alone | `SME` / `KNOWLEDGE_OWNER` may authorize in scope |
| Assign knowledge owner/SME | Yes | Assigned team/domain policy | No | No |
| Initiate/confirm team handover | Yes | Assigned team | No | `SUCCESSOR` participates, cannot self-confirm |
| See audit | Organization security scope | Assigned team scope | Own activity where policy allows | No extra right |

## 6. Permission codes and enforcement

Minimum codes: `project.create`, `project.read`, `project.manage`, `team.create`, `team.member.add`, `role.assign`, `capability.grant`, `source.upload`, `source.manage_acl`, `integration.manage`, `jira.sync.read`, `work_note.create`, `work_note.edit_own`, `knowledge.read`, `knowledge.propose`, `knowledge.verify`, `knowledge.reject`, `knowledge.supersede`, `gap.report`, `handover.manage`, `audit.read`.

The capability evaluator must check subject, issuing ADMIN, organization, expiry/revocation and explicit deny for `project.create`. No broad condition such as `role === "TEAM_LEADER"` may substitute for this check. Project/team operations must check scope plus resource ACL. Permission changes invalidate affected sessions/caches as policy requires.

## 7. System actors and audit

The AI orchestrator, ingestion worker, Jira sync worker and scheduler use least-privilege service identities. They may parse, index, draft, suggest or remind, but may not grant access, verify organizational truth, or impersonate a human reviewer. Imported Jira text and files are untrusted input.

Audit at least: membership/role/assignment changes; `project.create` grants, revocations and use; project/team creation; Jira connection and sync failures; upload/source ACL changes; note edits; knowledge review/version changes; sensitive retrieval/chat access; handover approvals and waivers. Logs must avoid tokens, full prompts and document bodies. Missing daily notes trigger a follow-up, **not employee performance scoring**.

## 8. Scope exclusions

No enterprise-wide HR hierarchy, automatic disciplinary action, AI-controlled permission grants, automatic successor assignment, or blanket ADMIN access to confidential content in the 10-week MVP.
