"""Figures for the Continuum AI capstone reports (matplotlib, white background, black outlines like the sample)."""
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)
plt.rcParams["font.family"] = "Arial"

FILL_HUB = "#FFE8E1"
FILL_BOX = "#FFFFFF"
FILL_ALT = "#EAF1FB"
EDGE = "#000000"


def box(ax, cx, cy, w, h, text, fill=FILL_BOX, fs=10, bold=False):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=fill, ec=EDGE, lw=1.1))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal",
            linespacing=1.25)


def arrow(ax, p, q, style="-|>", ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=13, lw=1.2, color=EDGE,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))


def fig1_feature_map():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 13.2)
    ax.axis("off")
    hub = (11, 6.6)
    box(ax, *hub, 4.2, 1.7, "Continuum AI\nplatform", FILL_HUB, 12, True)
    W = 5.4
    top = [
        ("Access & Governance", 4.0,
         ["3 roles + scoped assignments", "project.create grant (audited)", "Audit trail"]),
        ("Knowledge Capture", 11.0,
         ["Manual & daily/task notes", "Jira Cloud sync", "File upload (PDF, DOCX, MD, TXT, image)"]),
        ("AI Extraction", 18.0,
         ["SAG retrieval + evidence", "Proposed Knowledge", "Provider-agnostic LLM Gateway"]),
    ]
    bottom = [
        ("Lifecycle & Verification", 4.0,
         ["Version / validity / owner", "Human verification", "Gap & coverage tracking"]),
        ("Permission-aware Assistant", 11.0,
         ["Pre-retrieval ACL", "Cited answers", "Insufficient-evidence reply"]),
        ("Handover & Successor", 18.0,
         ["Departure / transfer checklist", "Scoped handover package", "Successor questions"]),
    ]
    for label, x, leaves in top:
        y = 9.0
        box(ax, x, y, W, 1.1, label, FILL_ALT, 10.5, True)
        for i, t in enumerate(leaves):
            box(ax, x, y + 1.15 + 0.68 * (len(leaves) - 1 - i), W + 0.9, 0.52, t, FILL_BOX, 8.6)
        ax.plot([x, hub[0] + (x - hub[0]) * 0.2], [y - 0.55, hub[1] + 0.85], color=EDGE, lw=1.2)
    for label, x, leaves in bottom:
        y = 4.2
        box(ax, x, y, W, 1.1, label, FILL_ALT, 10.5, True)
        for i, t in enumerate(leaves):
            box(ax, x, y - 1.15 - 0.68 * i, W + 0.9, 0.52, t, FILL_BOX, 8.6)
        ax.plot([x, hub[0] + (x - hub[0]) * 0.2], [y + 0.55, hub[1] - 0.85], color=EDGE, lw=1.2)
    ax.text(11, 0.2, "Evaluation & benchmark: retrieval, answer, citation, permission and handover metrics",
            ha="center", va="center", fontsize=9, style="italic")
    fig.savefig(os.path.join(OUT, "fig1_feature_map.png"), dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2_core_loop():
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 9.2)
    ax.axis("off")
    top = [("Active project work", "notes, Jira tasks,\nuploaded sources"),
           ("Ingestion & indexing", "parse / OCR /\nSAG retrieval index"),
           ("AI proposes\nknowledge", "PROPOSED + evidence\n(never auto-verified)"),
           ("Human verification", "Owner / scoped SME\nVERIFIED -> ACTIVE")]
    bot = [("Gap & coverage\nmonitoring", "missing / overdue\nknowledge follow-up"),
           ("Departure or\nresponsibility transfer", "handover checklist,\nunresolved questions"),
           ("Scoped handover\npackage", "successor + learning path"),
           ("Cited Q&A", "permission-aware,\ninsufficient-evidence aware")]
    xs = [3.0, 8.3, 13.6, 19.0]
    for i, ((t, s), x) in enumerate(zip(top, xs)):
        box(ax, x, 7.2, 4.4, 1.9, "", FILL_ALT)
        ax.text(x, 7.55, t, ha="center", va="center", fontsize=10, fontweight="bold", linespacing=1.15)
        ax.text(x, 6.65, s, ha="center", va="center", fontsize=8.3, linespacing=1.2)
        if i:
            arrow(ax, (xs[i - 1] + 2.2, 7.2), (x - 2.2, 7.2))
    # bottom row runs right-to-left so the loop closes back to the first box
    bxs = [19.0, 13.6, 8.3, 3.0]
    for i, ((t, s), x) in enumerate(zip(bot, bxs)):
        box(ax, x, 2.2, 4.4, 1.9, "", FILL_HUB if i == 3 else "#FFFFFF")
        ax.text(x, 2.55, t, ha="center", va="center", fontsize=10, fontweight="bold", linespacing=1.15)
        ax.text(x, 1.65, s, ha="center", va="center", fontsize=8.3, linespacing=1.2)
        if i:
            arrow(ax, (bxs[i - 1] - 2.2, 2.2), (x + 2.2, 2.2))
    arrow(ax, (19.0, 6.25), (19.0, 3.15))
    arrow(ax, (3.0, 3.15), (3.0, 6.25), ls="--")
    ax.text(3.25, 4.7, "new knowledge and gaps\nfeed the next cycle", fontsize=8, style="italic", va="center")
    fig.savefig(os.path.join(OUT, "fig2_core_loop.png"), dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig3_gantt():
    phases = [
        ("P0 Foundation", 1, 1, "Scope/actors, DB & API contracts, dataset design, Docker baseline"),
        ("P1 Access & project", 2, 3, "Auth, 3 roles, project.create grant, membership, ACL, audit"),
        ("P2 Capture & integration", 3, 5, "Manual/daily notes, Jira sync, R2 upload, parse/OCR jobs"),
        ("P3 Knowledge lifecycle", 5, 7, "SAG index/trace, Proposed Knowledge, verification, versions"),
        ("P4 Chat & handover", 7, 8, "Permission-aware chat, gaps, handover checklist"),
        ("P5 Evaluation & hardening", 9, 10, "Benchmark, leak tests, failure analysis, demo, report"),
    ]
    colors = ["#8FAADC", "#F4B183", "#A9D18E", "#FFD966", "#C9A0DC", "#9DC3E6"]
    fig, ax = plt.subplots(figsize=(11, 3.9))
    for i, (name, s, e, _) in enumerate(phases):
        y = len(phases) - 1 - i
        ax.barh(y, e - s + 1, left=s - 1, height=0.62, color=colors[i], edgecolor="black", lw=1)
        ax.text(s - 1 + (e - s + 1) / 2, y, f"Wk {s}" if s == e else f"Wk {s}-{e}", ha="center", va="center", fontsize=8.5)
    ax.set_yticks(range(len(phases)))
    ax.set_yticklabels([p[0] for p in phases][::-1], fontsize=9.5)
    ax.set_xticks([i + 0.5 for i in range(10)])
    ax.set_xticklabels([f"W{i + 1}" for i in range(10)], fontsize=9)
    ax.set_xlim(0, 10)
    ax.set_xticks(range(11), minor=True)
    ax.grid(axis="x", which="minor", color="#BBBBBB", lw=0.6)
    ax.tick_params(axis="x", which="minor", length=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig(os.path.join(OUT, "fig3_schedule.png"), dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig4_git_flow():
    fig, ax = plt.subplots(figsize=(11, 4.3))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 8.6)
    ax.axis("off")
    rows = [("DB PR", "schema / migration\n(feat/<Name>-<task>-db)", 3.2),
            ("BE PR", "controller / service / DTO\n(feat/<Name>-<task>-be-api)", 3.2),
            ("FE PR", "UI / API integration\n(feat/<Name>-<task>-fe-ui)", 3.2)]
    box(ax, 2.2, 4.3, 3.8, 1.7, "Jira task\n(ticket key)", FILL_ALT, 9.5, True)
    box(ax, 7.0, 4.3, 4.2, 1.7, "New branch from\nlatest origin/main", FILL_BOX, 9.5)
    arrow(ax, (4.1, 4.3), (4.9, 4.3))
    ys = [7.0, 4.3, 1.6]
    for (t, s, _), y in zip(rows, ys):
        box(ax, 13.0, y, 5.0, 1.7, "", FILL_BOX)
        ax.text(13.0, y + 0.42, t, ha="center", va="center", fontsize=10, fontweight="bold")
        ax.text(13.0, y - 0.32, s, ha="center", va="center", fontsize=8.2, linespacing=1.2)
        arrow(ax, (9.1, 4.3), (10.5, y), rad=0.0)
        arrow(ax, (15.5, y), (17.6, 4.3 + (y - 4.3) * 0.25))
    box(ax, 19.6, 4.3, 3.9, 3.0, "", FILL_HUB)
    ax.text(19.6, 5.15, "Review gate", ha="center", va="center", fontsize=10, fontweight="bold")
    ax.text(19.6, 3.75, "CI: lint, typecheck,\ntests, build\nhuman approval\nmerge by teammate", ha="center",
            va="center", fontsize=8.2, linespacing=1.25)
    fig.savefig(os.path.join(OUT, "fig4_git_flow.png"), dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig1_feature_map()
    fig2_core_loop()
    fig3_gantt()
    fig4_git_flow()
    print("figures written to", OUT)
