from html import escape
from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "Output-DrawIo" / "02_usecase_overall.drawio"

ACTOR_STYLE = (
    "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
    "outlineConnect=0;fillColor=none;strokeColor=#000000;fontColor=#000000;"
    "fontStyle=1;fontSize=12;fontFamily=Helvetica;"
)
USE_CASE_STYLE = (
    "ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
    "strokeWidth=1.5;fontColor=#000000;fontSize=11;fontFamily=Helvetica;"
)
LEFT_ASSOCIATION_STYLE = (
    "endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.2;"
    "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
)
RIGHT_ASSOCIATION_STYLE = (
    "endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.2;"
    "exitX=0;exitY=0.5;entryX=1;entryY=0.5;"
)
USER_LEFT_ASSOCIATION_STYLE = (
    "endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.2;"
    "exitX=0.2;exitY=1;entryX=1;entryY=0.5;"
)
USER_RIGHT_ASSOCIATION_STYLE = (
    "endArrow=none;html=1;strokeColor=#000000;strokeWidth=1.2;"
    "exitX=0.8;exitY=1;entryX=0;entryY=0.5;"
)
GENERATION_STYLE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
    "endArrow=block;endFill=0;html=1;strokeColor=#000000;strokeWidth=1.3;"
)


def value_xml(value: str) -> str:
    return escape(value, quote=True).replace("\n", "&#xa;")


def vertex(cell_id: str, value: str, style: str, x: int, y: int, width: int, height: int) -> str:
    return (
        f'        <mxCell id="{cell_id}" parent="1" style="{style}" '
        f'value="{value_xml(value)}" vertex="1">\n'
        f'          <mxGeometry height="{height}" width="{width}" x="{x}" y="{y}" as="geometry" />\n'
        "        </mxCell>\n"
    )


def edge(
    cell_id: str,
    source: str,
    target: str,
    style: str,
    points: tuple[tuple[int, int], ...] = (),
) -> str:
    if points:
        point_xml = "\n".join(
            f'              <mxPoint x="{x}" y="{y}" />' for x, y in points
        )
        geometry = (
            '          <mxGeometry relative="1" as="geometry">\n'
            "            <Array as=\"points\">\n"
            f"{point_xml}\n"
            "            </Array>\n"
            "          </mxGeometry>\n"
        )
    else:
        geometry = '          <mxGeometry relative="1" as="geometry" />\n'
    return (
        f'        <mxCell id="{cell_id}" edge="1" parent="1" source="{source}" '
        f'style="{style}" target="{target}">\n'
        f"{geometry}"
        "        </mxCell>\n"
    )


def build_document() -> str:
    cells: list[str] = []
    cells.append(
        vertex(
            "title",
            "Overall Use Case Diagram — Continuum AI\nBilateral Architecture Layout",
            "text;html=1;fontSize=14;align=center;verticalAlign=middle;fillColor=none;"
            "strokeColor=none;fontColor=#111827;fontFamily=Helvetica;",
            420,
            0,
            700,
            40,
        )
    )
    cells.append(
        vertex(
            "boundary",
            "Continuum AI System",
            "rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;"
            "fontColor=#000000;strokeWidth=2;verticalAlign=top;align=center;"
            "fontFamily=Helvetica;",
            150,
            120,
            1300,
            900,
        )
    )

    cells.extend(
        [
            vertex("actor-user", "User", ACTOR_STYLE, 775, 45, 50, 70),
            vertex("actor-admin", "Admin", ACTOR_STYLE, 45, 300, 50, 70),
            vertex("actor-leader", "Team Leader", ACTOR_STYLE, 45, 760, 50, 70),
            vertex("actor-member", "Member", ACTOR_STYLE, 1500, 430, 50, 70),
        ]
    )

    cells.extend(
        [
            vertex("uc-login", "Sign In / Sign Out", USE_CASE_STYLE, 610, 155, 200, 50),
            vertex("uc-profile", "Manage Profile & 2FA", USE_CASE_STYLE, 860, 155, 220, 50),
            vertex("uc-org", "Manage Organizations\n& Projects", USE_CASE_STYLE, 210, 250, 220, 55),
            vertex("uc-teams", "Manage Teams\n& Members", USE_CASE_STYLE, 210, 330, 220, 55),
            vertex("uc-jira", "Configure Jira Connector", USE_CASE_STYLE, 210, 410, 220, 50),
            vertex("uc-acl", "Manage Source ACL Policies", USE_CASE_STYLE, 210, 490, 220, 50),
            vertex("uc-audit", "View Audit Logs", USE_CASE_STYLE, 210, 570, 220, 50),
            vertex("uc-leader-workspace", "Manage Team Workspace", USE_CASE_STYLE, 500, 620, 230, 50),
            vertex("uc-create-project", "Create Project", USE_CASE_STYLE, 500, 680, 230, 50),
            vertex("uc-leader-notes", "Manage Daily Work Notes", USE_CASE_STYLE, 500, 740, 230, 50),
            vertex("uc-verify", "Review Verification Inbox", USE_CASE_STYLE, 500, 800, 230, 50),
            vertex("uc-handover", "Manage Handover Workflows", USE_CASE_STYLE, 500, 860, 230, 50),
            vertex("uc-interview", "Conduct Audio Interview", USE_CASE_STYLE, 500, 920, 230, 50),
            vertex("uc-notes", "Capture Daily Work Notes", USE_CASE_STYLE, 1040, 280, 230, 50),
            vertex("uc-upload", "Upload Documents\n& Sources", USE_CASE_STYLE, 1040, 360, 230, 50),
            vertex("uc-propose", "Create Knowledge\nProposal", USE_CASE_STYLE, 1040, 440, 230, 50),
            vertex("uc-ask-ai", "Ask AI Assistant\n(with Citations)", USE_CASE_STYLE, 1040, 520, 230, 55),
            vertex("uc-successor", "Participate in Handover\nLearning", USE_CASE_STYLE, 1040, 605, 230, 55),
        ]
    )

    cells.extend(
        [
            edge("gen-admin", "actor-admin", "actor-user", GENERATION_STYLE, ((130, 125), (740, 125))),
            edge("gen-leader", "actor-leader", "actor-user", GENERATION_STYLE, ((130, 105), (740, 105))),
            edge("gen-member", "actor-member", "actor-user", GENERATION_STYLE, ((1470, 95), (850, 95))),
            edge("assoc-u-login", "actor-user", "uc-login", USER_LEFT_ASSOCIATION_STYLE),
            edge("assoc-u-profile", "actor-user", "uc-profile", USER_RIGHT_ASSOCIATION_STYLE),
            edge("assoc-a-org", "actor-admin", "uc-org", LEFT_ASSOCIATION_STYLE),
            edge("assoc-a-teams", "actor-admin", "uc-teams", LEFT_ASSOCIATION_STYLE),
            edge("assoc-a-jira", "actor-admin", "uc-jira", LEFT_ASSOCIATION_STYLE),
            edge("assoc-a-acl", "actor-admin", "uc-acl", LEFT_ASSOCIATION_STYLE),
            edge("assoc-a-audit", "actor-admin", "uc-audit", LEFT_ASSOCIATION_STYLE),
            edge("assoc-l-workspace", "actor-leader", "uc-leader-workspace", LEFT_ASSOCIATION_STYLE),
            edge("assoc-l-project", "actor-leader", "uc-create-project", LEFT_ASSOCIATION_STYLE),
            edge("assoc-l-notes", "actor-leader", "uc-leader-notes", LEFT_ASSOCIATION_STYLE),
            edge("assoc-l-verify", "actor-leader", "uc-verify", LEFT_ASSOCIATION_STYLE),
            edge("assoc-l-handover", "actor-leader", "uc-handover", LEFT_ASSOCIATION_STYLE),
            edge("assoc-l-interview", "actor-leader", "uc-interview", LEFT_ASSOCIATION_STYLE),
            edge("assoc-m-notes", "actor-member", "uc-notes", RIGHT_ASSOCIATION_STYLE),
            edge("assoc-m-upload", "actor-member", "uc-upload", RIGHT_ASSOCIATION_STYLE),
            edge("assoc-m-propose", "actor-member", "uc-propose", RIGHT_ASSOCIATION_STYLE),
            edge("assoc-m-ai", "actor-member", "uc-ask-ai", RIGHT_ASSOCIATION_STYLE),
            edge("assoc-m-successor", "actor-member", "uc-successor", RIGHT_ASSOCIATION_STYLE),
        ]
    )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<mxfile host="app.diagrams.net" agent="Codex">\n'
        '  <diagram id="usecase-overall" name="Overall Use Case">\n'
        '    <mxGraphModel dx="1400" dy="1000" grid="1" gridSize="10" guides="1" '
        'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
        'pageWidth="1600" pageHeight="1150" math="0" shadow="0">\n'
        '      <root>\n'
        '        <mxCell id="0" />\n'
        '        <mxCell id="1" parent="0" />\n'
        + "".join(cells)
        + '      </root>\n'
        '    </mxGraphModel>\n'
        '  </diagram>\n'
        '</mxfile>\n'
    )


def main() -> None:
    with TARGET.open("r", encoding="utf-8", newline="") as handle:
        current = handle.read()
    if 'id="uc-leader-workspace"' in current:
        print("Rebuilding updated diagram")
    with TARGET.open("w", encoding="utf-8", newline="") as handle:
        handle.write(build_document())
    print("Updated overall use case diagram")


if __name__ == "__main__":
    main()
