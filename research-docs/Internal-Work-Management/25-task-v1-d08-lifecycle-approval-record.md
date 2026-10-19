# DATN-100 — D-13-R6 D-08 Lifecycle Approval Record

- **Decision date:** 2026-10-19 (Asia/Bangkok).
- **Decision maker:** The requester, who identified themself as the Project Leader and decision maker for this task.
- **Authority scope:** The requester selected the D-13 recommended lifecycle bundle and confirmed authority for the Product, Security, and Architecture decisions in that bundle.
- **Source revision:** [D-13-R6](23-task-v1-api-lifecycle-decisions-d13.md), Document `main` blob `2de31568004b619db9037144d39fe0edb8a24ff3` (18/10/2026).
- **Approval evidence:** The user's explicit response in the DATN-100 Codex task conversation: “Duyệt bundle D-13 (Recommended)”, in response to the bundled decision request naming the Product, Security, and Architecture authority scope.
- **Evidence limitation:** The authority and identity are requester-asserted in that conversation; this record does not claim independent identity verification or approval by any other person.

## Approved D-08 lifecycle scope

The following D-13-R6 proposal is approved for the backend lifecycle command in DATN-100 only:

1. States are `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, and `CANCELLED`; a new task starts in `TODO`.
2. Enable T02 (`TODO → IN_PROGRESS`), T05 (`TODO → CANCELLED`), T08 (`IN_PROGRESS → BLOCKED`), T09 (`IN_PROGRESS → DONE`), T10 (`IN_PROGRESS → CANCELLED`), T12 (`BLOCKED → IN_PROGRESS`), T15 (`BLOCKED → CANCELLED`), and T17 (`DONE → IN_PROGRESS`).
3. Reject the other 17 T01–T25 cells. In particular, self-transitions and all exits from `CANCELLED` remain forbidden.
4. Apply the D-13-R6 transition actor guards: work transitions require the assignee, `TEAM_LEADER`, or `ADMIN`; cancellation and reopen require the creator, `TEAM_LEADER`, or `ADMIN`. The transition command also requires a trusted active Project-member context. Team-derived access and membership-revocation effects remain outside this approval.
5. Require a reason of at least five characters for `BLOCK`, `CANCEL`, `RESUME`, and `REOPEN`; `START` and `COMPLETE` may omit a reason.
6. Require `expectedVersion`; accept a mutation only when it matches the stored version, increment version once on commit, and report stale or invalid transitions as conflicts without changing Task state or history.
7. Persist the status change, resulting version, completion timestamp effect, and one allowlisted `TASK_STATUS_TRANSITIONED` event atomically. Set `completedAt` on `DONE` and clear it on `REOPEN`. Do not persist a whole-Task snapshot in the event.
8. Require a UUID v4 operation ID on the dormant status command and use the D-13-R6 idempotency proposal in §3.7: actor/Project-scoped key, canonical command fingerprint, 24-hour replay window, mismatch rejection, in-flight conflict, and same-key resolution after an uncertain commit. An exact replay must not increment version or append another event. This does not decide public HTTP behavior for an omitted idempotency key.

The persistence fields approved for this slice are limited to `status` (with the five-state enum and `TODO` default), nullable `completedAt` (server-derived), and nullable `assigneeId` (used only by the `START` actor guard). This does not approve assignment mutation or the other D-13 extension fields.

## Explicit boundaries

- This approval does not enable a public or internal HTTP route, Gateway adapter, production caller, or Task runtime activation. DATN-100 implements the dormant lifecycle command and its persistence behavior only.
- It does not approve Task create/read API expansion, metadata or assignment mutation, history read APIs, Team-derived permissions, membership-revocation automation, Organization persistence, outbox/event delivery, Work Note or Handover integration, or delete/archive/restore.
- Other D-13-R6 gates remain open unless covered by this exact D-08 scope. DATN-373 is not represented as globally approved or complete by this record.

## Implementation and verification gates

- The database schema and an idempotent migration must be delivered in a DB branch/PR separate from backend business logic.
- No shared or production database is modified by this approval or by local verification.
- Transition tests must cover every enabled and forbidden matrix cell, actor/reason guards, stale and concurrent updates, idempotent replay/mismatch, atomic event persistence, and unchanged state/history on rejection.
- The DB PR must be reviewed and merged into `main` before a dependent BE PR is based on the updated `origin/main`.
