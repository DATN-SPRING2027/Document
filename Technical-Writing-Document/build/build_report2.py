"""Report 2 - Project Management Plan (Continuum AI).

Only content that exists in Document/, DATN-BE or DATN-FE is written. Anything without a source is left as a
highlighted [TBD] placeholder.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_lib import Report, refresh_with_word  # noqa: E402
import diagrams  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(HERE), "Submit-Report")
FIG = os.path.join(HERE, "figs")
OUT = os.path.join(OUT_DIR, "Continuum_AI_Report2_Project_Management_Plan.docx")
TBD = "[[TBD]]"

# WBS grouped by feature; items come from the functional requirements (FR-01..FR-24) and MVP scope.
WBS = [
    ("Feature 1: Identity, Access & Project Management", [
        "Authentication and session (JWT access token, rotating refresh token)",
        "Three-role RBAC and scoped assignments (SME, Knowledge Owner, Successor)",
        "Project, team and membership management; onboarding/offboarding states",
        "`project.create` capability grant (issue, revoke, expire, audit)",
        "Effective-permission evaluation and source/resource ACL",
    ]),
    ("Feature 2: Knowledge Capture", [
        "Manual structured knowledge entry and required-knowledge templates",
        "Daily / task notes (what, how, why, blockers, next steps)",
        "Reminders for missing or overdue notes and required knowledge",
    ]),
    ("Feature 3: Jira Cloud Integration", [
        "Connection and Jira-project mapping",
        "Backfill of issues, comments and status",
        "Idempotent webhook updates",
        "Reconciliation and sync-failure handling",
    ]),
    ("Feature 4: Source Upload & Ingestion", [
        "File upload (PDF, DOCX, Markdown, TXT, image) and Cloudflare R2 storage",
        "Parsing / OCR / chunking with job retry and status",
        "SAG indexing, source trace and search adapter",
    ]),
    ("Feature 5: AI Extraction & Knowledge Lifecycle", [
        "Proposed Knowledge extraction with evidence (structured schema)",
        "Knowledge verification (approve, edit, reject, request clarification)",
        "Versioning, supersede / deprecate and validity interval",
    ]),
    ("Feature 6: Permission-aware Assistant", [
        "Permission-aware retrieval, cited answer and verification status/date",
        "Insufficient-evidence response",
        "Gap detection and follow-up",
    ]),
    ("Feature 7: Handover", [
        "Member handover: scoped checklist, successor assignment, readiness confirmation",
        "Successor onboarding: scoped handover package and cited assistant",
    ]),
    ("Feature 8: Audit & Administration", [
        "Audit log (technical, security and project/team scope)",
    ]),
    ("Feature 9: Evaluation & Benchmark", [
        "Labeled benchmark dataset and question set",
        "Baselines (vector RAG, SAG, Continuum) and ablation",
        "Retrieval, answer, security and performance metrics",
    ]),
    ("Testing & Quality Assurance", [
        "Unit, integration, end-to-end, AI evaluation, security, performance and reliability testing",
    ]),
    ("DevOps & Deployment", [
        "CI (GitHub Actions) and reproducible Docker Compose deployment",
    ]),
    ("Documentation & Reports", [
        "Proposal / SRS / SDD / backlog and demo plan (based on the baseline specification)",
        "Architecture, data model, API contract, test plan and benchmark dataset documents",
    ]),
]


def wbs_rows():
    rows, groups = [], []
    for gi, (title, items) in enumerate(WBS, 1):
        groups.append(len(rows))
        rows.append([f"{gi}", title, "", TBD])
        for ii, name in enumerate(items, 1):
            rows.append([f"{gi}.{ii}", name, TBD, TBD])
    rows.append(["", "Total Estimated Effort (man-days)", "", TBD])
    return rows, groups


def build():
    diagrams.fig3_gantt()
    diagrams.fig4_git_flow()
    r = Report("Report 2 – Project Management Plan", "– [Location], September 2026 –",
               "Continuum AI – Knowledge Continuity Platform")
    r.footer("Continuum AI – Report 2: Project Management Plan")
    r.toc()
    r.page_break()
    r.record_of_changes([
        ("21/09/2026", "A", TBD, "Init version"),
        ("21/09/2026", "A", TBD, "Add scope, objectives, risks, process, quality, deliverables and configuration management"),
    ])

    r.h1("II. Project Management Plan", page_break=True)
    r.para("Highlighted [TBD] markers indicate information that is not available in the project documents "
           "(Document, DATN-BE, DATN-FE) and must be provided by the team.", size=10, italic=True)

    # ------------------------------------------------------------------ 1
    r.h2("1. Overview")
    r.h3("1.1 Scope & Estimation")
    r.para("The scope follows the accepted Continuum AI MVP baseline (10-week vertical slice). The work breakdown "
           "structure below groups the work by feature, based on the functional requirements. Complexity and "
           "estimated effort (man-days) are not defined in the source documents.", align="justify")
    rows, groups = wbs_rows()
    r.table(["#", "WBS Item", "Complexity", "Est. Effort (man-days)"], rows, [1.3, 9.6, 2.2, 2.8],
            group_rows=set(groups), center_cols=(0, 2, 3), total_row=True)

    r.h3("1.2 Project Objectives")
    r.para("Continuum AI addresses knowledge inheritance when a leader or member leaves a software project, changes "
           "team or transfers responsibility. The core hypothesis is that a project team can reduce knowledge loss "
           "and successor time-to-information by continuously capturing, verifying, maintaining and transferring "
           "member knowledge through a structured workflow and an evidence-grounded RAG assistant.", align="justify")
    r.label("Success criteria")
    r.bullets([
        "At least one end-to-end flow runs on real data: source document → SAG index → Proposed Knowledge → human "
        "verification → Verified Knowledge → AI answer with citation.",
        "A benchmark compares at least a vector-RAG baseline, SAG and the Continuum validation pipeline.",
        "Unauthorized evidence leakage is zero in the security test suite; restricted evidence is not sent to the LLM.",
        "When evidence is missing, outdated or unverified, the system returns an insufficient-evidence result instead of "
        "inventing an answer.",
        "Missing or overdue required knowledge creates a visible follow-up action.",
        "A member departure produces a prioritized handover plan based on real gaps; a successor receives a scoped "
        "handover package and can ask cited questions.",
        "The benchmark reports retrieval and answer quality against labeled expected outputs, and the handover "
        "evaluation measures time-to-information, answer correctness or unresolved gaps.",
        "Architecture, data model, API contract, test plan and benchmark dataset documents exist, and deployment is "
        "reproducible with Docker.",
    ])
    r.label("Measurable targets defined in the specification")
    r.table(["Area", "Target"], [
        ["Retrieval latency", "p95 < 2 s for normal retrieval in the benchmark environment (LLM generation latency measured separately)"],
        ["Normal AI response", "2–8 s; complex multi-hop / graph queries may target 5–15 s"],
        ["Unauthorized evidence leakage", "0 in the security test suite"],
        ["Citation", "Every factual answer has evidence or an explicit insufficient-evidence result"],
        ["Automatic verification", "AI cannot set VERIFIED/ACTIVE or resolve a critical conflict on its own"],
        ["Job reliability", "Ingestion/extraction supports retry, status tracking, idempotency and failure reason"],
    ], [4.4, 11.5])
    r.note("These are technical targets of the project, not results already achieved; final results must be measured "
           "on the team’s benchmark.")
    r.para(f"Quality-by-stage targets (review / unit / integration / system coverage and defect limits), milestone "
           f"timeliness and allocated effort per activity: {TBD} – not defined in the source documents.", after=6)

    r.h3("1.3 Project Risks")
    r.para("Risks and mitigations are taken from the specification’s risk register. The possibility rating is not "
           "defined in the source documents.", size=10, italic=True, after=4)
    risks = [
        ("Scope is too large", "The core flow is not completed",
         "- Lock P0 features; advanced onboarding/offboarding is a stretch goal\n- Demonstrate 4–5 flows instead of every module"),
        ("SAG upstream changes", "The integration breaks",
         "- Pin the SAG commit/tag\n- Keep an adapter boundary and integration tests\n- Fork only if required"),
        ("AI extraction is wrong", "Knowledge quality is poor",
         "- Structured schema and evidence requirement\n- Human review\n- Acceptance metrics"),
        ("Hallucination", "Loss of trust",
         "- Evidence-only answer policy\n- Insufficient-evidence state\n- Citation tests"),
        ("Permission leak", "Serious security failure",
         "- Pre-retrieval ACL and tenant/source scope\n- Negative security tests"),
        ("Dataset has no ground truth", "Effectiveness cannot be proven",
         "- Create the golden dataset early\n- Label it manually\n- Compare with baselines"),
        ("LLM cost or availability", "Demo is unstable",
         "- Provider abstraction\n- Cached evaluation\n- Local/mock fallback for non-AI paths"),
        ("Contribution unclear because open source is reused", "The committee rates the team’s part lower",
         "- SAG vs Continuum contribution table\n- Commit history, ADRs and benchmark\n- Domain features built by the team"),
        ("Graph / entity duplicates", "Retrieval noise",
         "- Normalization and de-duplication\n- Namespace/type rules\n- Evaluate failure cases"),
        ("Sensitive real data", "Privacy / compliance risk",
         "- Synthetic or anonymized capstone dataset\n- Retention and access policy"),
    ]
    r.table(["#", "Risk Description", "Impact", "Possibility", "Response Plans"],
            [[str(i), a, b, TBD, c] for i, (a, b, c) in enumerate(risks, 1)],
            [0.8, 3.9, 3.2, 1.9, 6.1], center_cols=(0, 3))

    # ------------------------------------------------------------------ 2
    r.h2("2. Management Approach")
    r.h3("2.1 Project Process")
    r.para("The project is delivered as a 10-week plan in six phases (Figure 1). P0 is the vertical-slice foundation "
           "with real data; P1 features are accepted only when P0 is stable.", align="justify")
    r.table(["Phase", "Week", "Deliverables"], [
        ["P0 – Foundation", "1", "Scope/actor decisions, DB/API contracts, dataset design, Docker baseline and module ownership"],
        ["P1 – Access & project", "2–3", "Auth, 3 roles, `project.create` grant, project/team membership, ACL and audit"],
        ["P2 – Capture & integration", "3–5", "Manual note, Jira backfill/webhook/reconciliation, R2 upload, parse/OCR/job status"],
        ["P3 – Knowledge lifecycle", "5–7", "SAG index/trace, Proposed Knowledge, human verification, immutable version/evidence"],
        ["P4 – Chat & handover", "7–8", "Permission-aware chat with citation and insufficient evidence, gap, scoped handover checklist"],
        ["P5 – Evaluation & hardening", "9–10", "Dataset benchmark, leak tests, failure analysis, bug fixes, reproducible demo and report"],
    ], [4.3, 1.6, 10.0], center_cols=(1,))
    r.figure(os.path.join(FIG, "fig3_schedule.png"), 15.8, "Delivery phases over the 10-week plan.")
    r.para("Every task follows the workflow defined in AI_WORKFLOW.md: receive the Jira task, read the rules and "
           "architecture, create a new branch from the latest `origin/main`, implement, test locally, commit, push, "
           "open a pull request into `main`, link it to Jira, get review and approval, and merge by an authorized "
           "teammate (Figure 2, section 6.2). API behavior is contract-first: request, response, error, scope, pagination "
           "and streaming semantics are approved in OpenAPI before implementation.", align="justify")
    r.para(f"Development methodology (for example Scrum), iteration length and ceremonies: {TBD} – not defined in the "
           f"source documents.", after=6)

    r.h3("2.2 Quality Management")
    r.label("Testing strategy")
    r.table(["Test level", "Scope", "Examples"], [
        ["Unit", "Domain rules, validation, mapping, risk formula", "Cannot verify without reviewer; validity overlap; permission scope builder"],
        ["Integration", "Core API ↔ MongoDB ↔ SAG ↔ LLM mock", "Ingest mapping, search adapter, citation trace"],
        ["E2E", "User flows on UI/API", "Upload → verify → ask; gap → follow-up → resolve"],
        ["AI evaluation", "Golden dataset and judge rubric / human review", "Retrieval recall, faithfulness, extraction accuracy"],
        ["Security", "Auth/RBAC/ACL, prompt injection, data leakage", "Finance source inaccessible to Sales; malicious document cannot override system policy"],
        ["Performance", "Load, retrieval, ingestion", "Concurrent queries, large document batch"],
        ["Reliability", "Failure injection", "SAG down, LLM down, job retry, duplicate ingestion"],
    ], [2.6, 5.8, 7.5])
    r.label("Quality Assurance Approach")
    r.bullets([
        "**Reviewing:** every change goes through a pull request. Backend review covers architecture, logic, security, "
        "validation, error handling, performance and database query; frontend review covers UI/UX, component "
        "structure, state, API handling, reuse, responsive behavior and accessibility; database review covers schema, "
        "index, migration, backward compatibility and data-loss risk.",
        "**Tools:** Jest (backend), Vitest and React Testing Library (frontend), Playwright (browser end-to-end), "
        "Pytest (AI service).",
        "**Quality gates:** backend `npm run check` runs lint, typecheck, unit tests, e2e tests and build; frontend "
        "`npm run check` runs lint, typecheck, tests and build. GitHub Actions CI checks run on pull requests.",
        "**Rules:** write a failing test before adding behavior; treat files, webhooks, Jira data, user input and AI "
        "output as untrusted; permission filtering happens before evidence is sent to the AI engine.",
    ])
    r.label("Quality Metrics (from the evaluation methodology)")
    r.table(["Group", "Metrics"], [
        ["Retrieval", "Recall@5, Recall@10, MRR, Precision@K; supporting-evidence recall for multi-hop questions"],
        ["Answer", "Correctness, faithfulness/groundedness, citation correctness and completeness, answer relevance"],
        ["Extraction", "Knowledge Object precision/recall, entity F1, relationship F1, human acceptance/edit/reject rate"],
        ["Gap / Conflict", "Precision/recall or review acceptance rate for candidate gaps and conflicts"],
        ["Security", "Unauthorized evidence leakage rate (target 0)"],
        ["Performance", "Retrieval p50/p95, total response time, ingestion throughput, job failure rate"],
        ["Cost", "Tokens per query, model calls per query"],
        ["Business proxy", "Time-to-information, expert interruption proxy, knowledge coverage change"],
    ], [3.4, 12.5])

    r.h3("2.3 Training Plan")
    r.para(f"No training plan is defined in the source documents. {TBD}", after=4)
    r.table(["Training Area", "Participants", "When, Duration", "Waiver Criteria"],
            [[TBD, TBD, TBD, TBD] for _ in range(3)], [6.4, 3.4, 3.2, 2.9])

    # ------------------------------------------------------------------ 3
    r.h2("3. Project Deliverables")
    r.para("Due dates use the relative weeks of the 10-week plan; calendar dates are not defined in the source "
           "documents.", size=10, italic=True, after=4)
    r.table(["#", "Deliverable", "Due", "Notes"], [
        ["1", "Foundation: scope and actor decisions, DB/API contracts, dataset design, Docker baseline", "Week 1",
         "MVP scope and actor/role model are accepted baselines; backend repository has CI checks and the IAM v1 OpenAPI contract; frontend is bootstrapped from TailAdmin (repository history)"],
        ["2", "Access & project: auth, 3 roles, `project.create` grant, membership, ACL, audit", "Week 2–3", ""],
        ["3", "Capture & integration: manual note, Jira sync, R2 upload, parse/OCR/job status", "Week 3–5", ""],
        ["4", "Knowledge lifecycle: SAG index/trace, Proposed Knowledge, human verification, versions", "Week 5–7", ""],
        ["5", "Chat & handover: permission-aware chat with citations, gaps, handover checklist", "Week 7–8", ""],
        ["6", "Evaluation & hardening: dataset benchmark, leak tests, failure analysis, reproducible demo and report", "Week 9–10", ""],
        ["7", "Documents: architecture, data model, API contract, test plan, benchmark dataset", "Throughout", "Required by the project success criteria"],
        ["8", "Demo scenarios D1–D5 (verified search, multi-hop memory, gap closure, permission, offboarding risk)", "Week 10", "Defense demo scenarios in the specification"],
    ], [0.9, 7.4, 2.0, 5.6], center_cols=(0, 2))

    # ------------------------------------------------------------------ 4
    r.h2("4. Responsibility Assignments")
    r.para("The specification defines five workstreams by role. Assignment of team members and the D/R/S/I matrix are "
           "not defined in the source documents.", size=10, italic=True, after=4)
    r.table(["Workstream", "Scope (from the specification)", "Assigned member(s)"], [
        ["Product / BA", "SRS, use cases, acceptance criteria, benchmark questions, demo narrative", TBD],
        ["Backend", "Domain model, RBAC, workflow, audit, APIs, database", TBD],
        ["AI / Retrieval", "SAG adapter, benchmark, extraction, prompt/schema, evaluation", TBD],
        ["Frontend", "Search/assistant, review center, interview, dashboard, admin", TBD],
        ["DevOps / QA", "Docker, CI, test data, observability, load/security/e2e testing", TBD],
    ], [3.2, 9.0, 3.7])

    # ------------------------------------------------------------------ 5
    r.h2("5. Project Communications")
    r.table(["Communication Item", "Who / Target", "Purpose", "When, Frequency", "Type, Tool, Method(s)"], [
        ["Task tracking", "All team members", "Backlog, status and PR links per task", "Continuous", "Jira"],
        ["Pull request review", "Developers, teammate reviewers", "Code review, approval before merge", "Per pull request", "GitHub pull requests"],
        ["Database change notice", "All team members", "Announce collection/field/index/migration changes and data impact", "Per database change", "Team chat, standard [DATABASE CHANGE] template"],
        ["Team meetings", TBD, TBD, TBD, TBD],
        ["Meetings with lecturer", TBD, TBD, TBD, TBD],
    ], [3.4, 3.0, 4.6, 2.4, 2.5])

    # ------------------------------------------------------------------ 6
    r.h2("6. Configuration Management")
    r.h3("6.1 Document Management")
    r.para("Project documents are versioned as Markdown in the `Document` repository, the canonical source for the "
           "specification, architecture and database design. The backend and frontend repositories keep their task plans "
           "and specifications under `docs/` and `tasks/`. The folder structure of the `Document` repository is:",
           align="justify")
    r.table(["Folder", "Meaning"], [
        ["research-docs", "MVP scope, actors/roles/permissions, daily workflow and Jira sync, and the Graduation Project Specification."],
        ["research-tech", "Approved technology stack and architecture decisions."],
        ["architecture", "System architecture: topology, frontend, services, storage/messaging/AI, security, orchestration, reliability."],
        ["database-design", "Schema documents for each service and the schema catalogue."],
        ["deploy", "Docker Compose files, Kubernetes manifests and backup scripts."],
        ["diagram", "Interactive architecture diagram."],
        [".agents", "Project rules for AI coding agents (workflow and frozen core specifications)."],
        ["Root files", "README, AGENTS.md and AI_WORKFLOW.md (mandatory workflow), and per-tool instruction files."],
    ], [3.4, 12.5])

    r.h3("6.2 Source Code Management")
    r.label("Source Code Management Strategy")
    r.bullets([
        "**Repository structure:** separate repositories under the GitHub organization `DATN-SPRING2027`.",
        "**Branching:** every task uses a new branch created from the latest `origin/main`; no direct or force pushes "
        "to `main`; feature branches open pull requests into `main` only.",
        "**Branch names:** `feat/<Name>-<task>-be-api` (backend), `feat/<Name>-<task>-fe-ui` (frontend), "
        "`feat/<Name>-<task>-db` (database); `fix/` or `chore/` prefixes for bugs and chores when the team or Jira requires.",
        "**Separation of concerns:** database, backend and frontend changes use separate branches and pull requests "
        "(Figure 2).",
        "**Commit standards:** atomic commits following Conventional Commits (for example `feat:`, `fix:`, `docs:`, `ci:`).",
        "**Code review:** merge only after teammate approval, with no unresolved change requests or conflicts and with "
        "passing CI, build and tests.",
        "**Database changes:** any schema, index, enum, default, reference or validation change is a database change "
        "with its own pull request and a new, idempotent migration script; committed migrations are never edited; the "
        "team is notified using the standard template.",
        "**Secrets:** no secrets, tokens or populated `.env` files are committed; only safe placeholders in `.env.example`.",
    ])
    r.label("Repositories")
    r.table(["Repository", "Content", "Main technology"], [
        ["Document", "Specification, architecture, database design, deployment references, workflow rules", "Markdown, YAML"],
        ["DATN-BE", "Continuum `backend-core` modular monolith with eight domain boundaries: iam, capture, jira, lifecycle, chat, handover, ingestion, notification; OpenAPI contracts", "NestJS, TypeScript, Jest, Swagger"],
        ["DATN-FE", "Web application built on TailAdmin (dashboard shell, knowledge, assistant, verification, handover, administration screens)", "Next.js 16, React 19, Tailwind CSS, TanStack Query, Vitest"],
        ["AI service", f"FastAPI service integrating a pinned SAG version behind `integrations/ai-engine`; repository not present in the workspace: {TBD}", "Python, FastAPI, Pytest"],
    ], [3.0, 8.6, 4.3])
    r.figure(os.path.join(FIG, "fig4_git_flow.png"), 15.8,
             "Task delivery flow: Jira task, new branch, separate DB/BE/FE pull requests and review gate.")

    r.h3("6.3 Tools & Infrastructures")
    r.table(["Category", "Tools / Infrastructure"], [
        ["**Technology**", "Next.js (App Router), React, TypeScript (Frontend); Node.js, NestJS, TypeScript (Backend); Python, FastAPI (AI service)"],
        ["**Database and storage**", "MongoDB with Mongoose (source of truth), LanceDB via SAG (initial retrieval index), Redis, Cloudflare R2 (S3-compatible adapter as fallback)"],
        ["**AI / Retrieval**", "Pinned zleap-sag, provider-agnostic LLM Gateway, SAG pipeline with MarkItDown or MinerU for parsing and OCR"],
        ["**Background jobs**", "Redis and BullMQ"],
        ["**Integrations**", "Jira Cloud REST API, webhooks and reconciliation"],
        ["**UI foundation**", "TailAdmin (Next.js edition, MIT license) with Tailwind CSS; TanStack Query and Zustand for state"],
        ["**Testing**", "Jest, Vitest, React Testing Library, Playwright, Pytest"],
        ["**API documentation**", "Swagger and OpenAPI"],
        ["**Version control**", "Git and GitHub (source code and documents)"],
        ["**Project management**", "Jira"],
        ["**CI/CD**", "GitHub Actions"],
        ["**Deployment**", "Docker Compose; Kubernetes manifests are kept in `Document/deploy/k8s`"],
    ], [4.2, 11.7])

    os.makedirs(OUT_DIR, exist_ok=True)
    r.save(OUT, "Continuum AI – Report 2 – Project Management Plan")
    pages = refresh_with_word(OUT, os.path.join(HERE, "preview_report2.pdf"))
    print("saved", OUT, "pages:", pages)


if __name__ == "__main__":
    build()
