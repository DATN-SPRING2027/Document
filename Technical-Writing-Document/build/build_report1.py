"""Report 1 - Project Introduction (Continuum AI). Content is distilled from Document/, DATN-BE and DATN-FE."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_lib import Report, refresh_with_word  # noqa: E402
import diagrams  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(HERE), "Submit-Report")
FIG = os.path.join(HERE, "figs")
OUT = os.path.join(OUT_DIR, "Continuum_AI_Report1_Project_Introduction.docx")


def build():
    diagrams.fig1_feature_map()
    diagrams.fig2_core_loop()
    r = Report("Report 1 – Project Introduction", "– [Location], September 2026 –",
               "Continuum AI – Knowledge Continuity Platform")
    r.footer("Continuum AI – Report 1: Project Introduction")
    r.toc()
    r.page_break()
    r.record_of_changes([
        ("21/09/2026", "A", "[[TBD]]", "Create the project introduction document"),
        ("21/09/2026", "A", "[[TBD]]", "Add content for II.1, II.2, II.3, II.4, II.5"),
        ("21/09/2026", "A", "[[TBD]]", "Add the project scope & limitations (II.6)"),
    ])

    # ------------------------------------------------------------------ II
    r.h1("II. Project Introduction", page_break=True)

    r.h2("1. Overview")
    r.h3("1.1 Project Information")
    r.bullets([
        "Project name: Building an AI-powered knowledge continuity and handover platform for multi-team software "
        "projects using Next.js, NestJS, and SAG-based retrieval",
        "Project code: Continuum AI",
        "Group name: [[TBD]]",
        "Software type: Web application (Next.js), backend API (NestJS modular monolith), AI retrieval service "
        "(FastAPI + SAG)",
    ])
    r.h3("1.2 Project Team")
    r.table(["Full Name", "Role", "Email", "Mobile"], [
        ["[[Lecturer name]]", "Lecturer", "[[email]]", "[[phone]]"],
        ["[[Full name]]", "Leader", "[[email]]", "[[phone]]"],
        ["[[Full name]]", "Member", "[[email]]", "[[phone]]"],
        ["[[Full name]]", "Member", "[[email]]", "[[phone]]"],
        ["[[Full name]]", "Member", "[[email]]", "[[phone]]"],
    ], [4.2, 2.4, 5.6, 3.7])

    # ---- 2
    r.h2("2. Product Background")
    r.para("In a software project, the knowledge needed to keep the work running lives in many places at once: "
           "design decisions in chat threads, procedures in wikis, task history in Jira, and—most importantly—in the "
           "heads of a few experienced people. When a team leader or member leaves the project, moves to another team, "
           "or hands over a responsibility, the code and documents usually remain, but the reasoning behind decisions, "
           "the workarounds, the incident lessons, and the operating know-how do not. The successor is then left to work out "
           "what is current, what is risky, and who is accountable.", align="justify")
    r.para("Existing tools only partly help. Wikis and drives store files but cannot tell which page is still true or "
           "which process has no documented owner. “Chat with your documents” assistants retrieve text that looks "
           "similar to a question, yet similarity does not mean the text is current, verified, or that the asking user "
           "is allowed to see it. Knowledge capture is also usually postponed until the day someone announces their "
           "departure, when it is already too late.", align="justify")
    r.label("Key user groups:")
    r.bullets([
        "**Administrators (ADMIN):** manage users, projects, teams, roles, connectors and source policies at "
        "organization scope, and control audit—without automatic access to confidential content.",
        "**Team Leaders (TEAM_LEADER):** lead assigned teams, track who owns each domain or module, follow up on missing "
        "knowledge, and review handovers. Creating a new project requires an explicit, audited `project.create` grant "
        "from an Admin.",
        "**Members (MEMBER):** record what they did and why during normal work, upload sources, maintain assigned "
        "knowledge, ask the assistant, and flag knowledge gaps.",
        "**SMEs and Knowledge Owners (scoped assignments):** verify, reject or supersede knowledge inside a domain, "
        "module or process they are accountable for.",
        "**Successors (scoped assignment):** receive a scoped handover package and ask evidence-grounded questions "
        "to become productive quickly, without inheriting the predecessor’s permissions.",
    ])
    r.para("Continuum AI addresses this gap with a continuous loop rather than a one-off migration. Members and leaders "
           "capture knowledge while the project is running—through manual notes, short daily or task notes, uploaded "
           "documents, and task context imported from Jira Cloud. The system indexes these sources with a "
           "retrieval engine (SAG) and lets AI propose structured knowledge together with its evidence. AI output "
           "always stays in the PROPOSED state until an authorized human verifies it, after which it becomes "
           "versioned, owned, time-bounded organizational knowledge. Missing or overdue knowledge creates visible "
           "follow-up work. When a person leaves or transfers, the system analyses their responsibilities and gaps, "
           "produces a focused handover checklist, and gives the successor a permission-aware assistant that answers "
           "with citations—or states that evidence is insufficient instead of inventing an answer.",
           align="justify", before=4)
    r.figure(os.path.join(FIG, "fig2_core_loop.png"), 15.8,
             "Core loop of Continuum AI: capture, verify, monitor, hand over, and ask with citations.")
    r.label("In summary, Continuum AI was conceived to eliminate:")
    r.bullets([
        "Knowledge loss when people leave, change teams or transfer responsibilities.",
        "Uncertainty about which knowledge is current, verified, owned and still valid.",
        "Unsafe AI answers that use outdated, unverified or unauthorized evidence, or that are not traceable to a source.",
        "Slow, interruption-heavy takeovers that depend on the predecessor’s remaining time.",
    ])
    r.para("By combining continuous capture, human-verified knowledge lifecycle, permission-aware retrieval and a "
           "structured handover workflow in one platform, Continuum AI keeps a project’s know-how usable even when the "
           "people change.", align="justify", before=4)

    # ---- 3
    r.h2("3. Existing Systems")
    r.para("Continuum AI is not meant to compete with file storage or with generic chatbots. Its technical gap is the "
           "link between retrieval and organizational truth management: a chunk that is semantically similar to a "
           "question is not necessarily current, verified, permitted for the user, or the policy in force. The table "
           "compares the approaches a team could use today.", align="justify")
    r.table(["Approach", "Strengths", "Limitation for knowledge continuity"], [
        ["Document management / Drive / Wiki", "Storage, permissions, file versions, collaboration.",
         "Does not structure knowledge by itself; hard to tell which process lacks knowledge; tacit knowledge stays "
         "with people."],
        ["Vector RAG", "Fast semantic chunk search; easy to deploy.",
         "Similarity does not mean current truth; weak on multi-hop and relationships; no owner, validity, "
         "verification or conflict management."],
        ["Traditional GraphRAG", "Models relations and supports traversal.",
         "Graph building, entity resolution and incremental maintenance can be costly; still needs a lifecycle and "
         "truth layer at the application level."],
        ["SAG (Zleap-AI)", "Event–entity indexing; semantic + relational retrieval in one pipeline; source tracing.",
         "Oriented to knowledge-base retrieval; does not replace the knowledge object, verification, lifecycle, "
         "continuity-risk and enterprise permission model."],
        ["**Continuum AI**", "Retrieval + knowledge lifecycle + human verification + continuity workflow.",
         "More complex than a RAG chatbot; requires serious AI, permission and data-quality evaluation."],
    ], [3.4, 5.2, 7.3])
    r.para("[[TBD: named competitor products with their actors, main features, advantages and disadvantages – "
           "no competitor research is available in the source documents]]", after=8)

    # ---- 4
    r.h2("4. Business Opportunity")
    r.para("[[TBD: Market Trends and Fit – no market research is available in the source documents]]", after=8)
    r.label("Solving Key Problems")
    r.bullets([
        "**Knowledge loss on departure or transfer:** knowledge is captured continuously during normal work and "
        "gaps are surfaced early, not on the last day.",
        "**Untrustworthy answers:** every factual answer carries citations, status, owner, version and last-verified "
        "date, or an explicit insufficient-evidence reply.",
        "**Unauthorized exposure:** permission filtering happens before retrieval and again before evidence is passed "
        "to the language model.",
        "**Slow takeover:** a scoped handover package, a checklist of real gaps and a cited assistant shorten the "
        "successor’s time-to-information.",
    ])
    r.label("Key Features and Benefits")
    r.table(["Feature", "Benefit"], [
        ["**Continuous Knowledge Capture**", "Manual and daily notes plus Jira-linked context reduce reporting effort "
                                             "while keeping the author in control of what is recorded."],
        ["**AI-Proposed, Human-Verified Knowledge**", "AI drafts structured knowledge with evidence; only authorized "
                                                      "people can make it verified and active."],
        ["**Permission-aware Assistant**", "Cited answers over authorized knowledge; refuses unsupported, outdated or "
                                           "unauthorized requests."],
        ["**Gap and Coverage Monitoring**", "Missing or overdue knowledge becomes visible follow-up work—not employee scoring."],
        ["**Scoped Handover Workflow**", "Focused checklist, unresolved questions and successor package based on real gaps."],
        ["**Audit and Governance**", "Traceable changes to roles, grants, sources, reviews and handover approvals."],
    ], [5.4, 10.5])
    r.para("[[TBD: Market Needs and Opportunities – no market research is available in the source documents]]", after=8)

    # ---- 5
    r.h2("5. Software Product Vision")
    r.para("For software project teams—administrators, team leaders, members and successors—who need to keep project "
           "knowledge alive when people join, leave or change responsibility, Continuum AI is a knowledge continuity "
           "platform that turns everyday notes, documents and task context into verified, traceable and reusable "
           "project knowledge. Unlike document storage and generic “chat with your files” tools, Continuum AI "
           "manages the whole knowledge lifecycle: it requires human verification before knowledge becomes "
           "authoritative, enforces permissions before retrieval, and guides a scoped handover to the successor.",
           align="justify")
    r.label("Continuum AI empowers users with:")
    r.bullets([
        "**Continuous capture:** structured knowledge entries, daily/task notes and Jira Cloud sync, with files "
        "(PDF, DOCX, Markdown, TXT, images) stored privately.",
        "**Evidence-based AI extraction:** proposed knowledge that always points back to its source evidence.",
        "**Human verification and lifecycle:** proposed, under-review, verified, active, superseded, deprecated and "
        "rejected states with version, validity, owner and reviewer.",
        "**Permission-aware assistant:** cited answers, a clear insufficient-evidence response, and a way to report a "
        "knowledge gap.",
        "**Handover workflow:** responsibility and gap analysis, checklists, unresolved questions, scoped successor "
        "package and readiness tracking.",
        "**Audit and evaluation:** an audit trail of important actions and a labeled benchmark that measures retrieval, "
        "answer, citation, permission and handover quality.",
    ])
    r.para("By uniting capture, verification, retrieval, permissions and handover in one web platform, Continuum AI "
           "helps a project keep its operating knowledge when its people change.", align="justify", before=4)

    # ---- 6
    r.h2("6. Project Scope & Limitations")
    r.para("The Continuum AI MVP demonstrates the full knowledge continuity loop for one software project that contains "
           "several teams. It is designed as a 10-week vertical slice: an Admin configures the project, teams and grants; "
           "members add manual or Jira-linked notes and documents; files are processed and indexed; AI proposes "
           "knowledge for human review; and a successor asks the cited assistant with permission checks. Dataset-based "
           "evaluation is required. This section lists the features of the initial release and the limitations that "
           "set realistic expectations and help manage change requests.", align="justify")
    r.h3("6.1 Major Features")
    feats = [
        ("FE-01", "Project, Team and Role Management with three persistent roles (ADMIN, TEAM_LEADER, MEMBER), scoped "
                  "SME / Knowledge Owner / Successor assignments, onboarding/offboarding states and an audited "
                  "`project.create` grant."),
        ("FE-02", "Continuous Knowledge Capture through structured knowledge entries, short daily/task notes, "
                  "required-knowledge templates and reminders for missing or overdue notes."),
        ("FE-03", "Jira Cloud Sync: initial import, webhook updates, de-duplication and reconciliation of issues, "
                  "comments and status, with the author confirming the resulting note."),
        ("FE-04", "Source Upload and Ingestion for PDF, DOCX, Markdown, TXT and image files, with private originals in "
                  "Cloudflare R2, metadata in MongoDB, parsing/OCR jobs and status tracking."),
        ("FE-05", "AI Knowledge Extraction using SAG retrieval and a provider-agnostic LLM Gateway to produce "
                  "PROPOSED knowledge with supporting evidence."),
        ("FE-06", "Knowledge Lifecycle and Human Verification (proposed → under review → verified → active → "
                  "superseded / deprecated / rejected) with version, validity interval, owner, reviewer and review date."),
        ("FE-07", "Permission-aware Assistant: search and question answering with citations, status, owner, version and "
                  "last-verified date; permission filtering before retrieval; insufficient-evidence response and "
                  "knowledge-gap reporting."),
        ("FE-08", "Knowledge Gap and Coverage Monitoring that turns missing or overdue required knowledge into "
                  "visible follow-up actions (no employee performance scoring)."),
        ("FE-09", "Handover Workflow: initiate departure or responsibility transfer, analyse responsibilities and gaps, "
                  "create handover items, assign a successor, track unresolved questions and confirm completion."),
        ("FE-10", "Audit Trail and Governance for membership, role and capability changes, source ACL changes, "
                  "Jira sync failures, knowledge reviews, sensitive retrieval and handover approvals."),
        ("FE-11", "Evaluation and Benchmark: a labeled dataset, versioned baselines (vector RAG, SAG, Continuum) and "
                  "retrieval, answer, citation, permission and handover metrics."),
    ]
    for code, text in feats:
        r.para(f"**{code}**: {text}", align="justify", after=4)
    r.figure(os.path.join(FIG, "fig1_feature_map.png"), 15.8, "Overview of Continuum AI capabilities.")
    r.h3("6.2 Limitations & Exclusions")
    lims = [
        ("LI-01", "The MVP covers one software project with multiple teams; enterprise-wide knowledge management, HR "
                  "hierarchy and Learning Management System features are excluded."),
        ("LI-02", "Only Jira Cloud is integrated as a task source. GitHub, Google Drive, Confluence, MCP-based and "
                  "meeting-note connectors are stretch goals."),
        ("LI-03", "AI-generated interview questions and interview-to-knowledge conversion are stretch capabilities; the "
                  "MVP records unresolved questions for human follow-up."),
        ("LI-04", "AI output is never verified automatically: knowledge stays PROPOSED until an authorized human verifies "
                  "it, and successors are never assigned automatically."),
        ("LI-05", "Continuity and coverage signals are decision-support only. Employee performance scoring and "
                  "automatic restructuring are out of scope."),
        ("LI-06", "Automated conflict detection, advanced freshness scoring, incident memory and temporal graph "
                  "visualization are later phases."),
        ("LI-07", "No fine-tuning of a dedicated LLM; models are accessed through a provider-agnostic gateway, and "
                  "model updates can change output unless versions are pinned."),
        ("LI-08", "Extraction quality depends on source quality and human review; the benchmark uses a synthetic or "
                  "anonymized dataset from one project scope, so results may not generalize to every domain or language."),
        ("LI-09", "Production-grade SSO (SAML/OIDC), DLP and compliance integrations are not included; the capstone "
                  "deployment is reproducible with Docker Compose."),
        ("LI-10", "The frontend calls only the Continuum backend API; it never calls the SAG service directly, and "
                  "AI output is not written to the database without backend validation."),
    ]
    for code, text in lims:
        r.para(f"**{code}**: {text}", align="justify", after=4)

    os.makedirs(OUT_DIR, exist_ok=True)
    r.save(OUT, "Continuum AI – Report 1 – Project Introduction")
    pages = refresh_with_word(OUT, os.path.join(HERE, "preview_report1.pdf"))
    print("saved", OUT, "pages:", pages)


if __name__ == "__main__":
    build()
