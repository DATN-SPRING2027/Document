"""Pillow-only report diagrams. Keeps report generation independent of matplotlib."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figs"
FIG_DIR.mkdir(parents=True, exist_ok=True)
W, H = 2200, 1350
BG = "#FFFFFF"
INK = "#19324D"
MUTED = "#536579"
BLUE = "#DCEBFA"
TEAL = "#D9F2EE"
GOLD = "#FFF0C9"
PURPLE = "#EAE2F5"
PALE = "#F3F6FA"
GREEN = "#DFF0D8"
ORANGE = "#FBE2D5"


def _font(size, bold=False):
    names = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def _canvas(title, subtitle=None):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((W // 2, 48), title, fill=INK, font=_font(46, True), anchor="mt")
    if subtitle:
        d.text((W // 2, 112), subtitle, fill=MUTED, font=_font(25), anchor="mt")
    return im, d


def _centered_text(draw, box, text, font, color=INK, spacing=8):
    x1, y1, x2, y2 = box
    lines = text.split("\n")
    heights = []
    widths = []
    for line in lines:
        b = draw.textbbox((0, 0), line, font=font)
        widths.append(b[2] - b[0])
        heights.append(b[3] - b[1])
    total = sum(heights) + spacing * (len(lines) - 1)
    y = y1 + (y2 - y1 - total) / 2
    for line, width, height in zip(lines, widths, heights):
        draw.text((x1 + (x2 - x1 - width) / 2, y), line, font=font, fill=color)
        y += height + spacing


def _box(draw, rect, text, fill=BLUE, font_size=25, radius=22, outline=INK, width=3):
    draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline, width=width)
    _centered_text(draw, rect, text, _font(font_size, True))


def _arrow(draw, start, end, color=INK, width=5, head=17):
    draw.line((start, end), fill=color, width=width)
    import math
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - head * math.cos(angle - 0.55), end[1] - head * math.sin(angle - 0.55))
    right = (end[0] - head * math.cos(angle + 0.55), end[1] - head * math.sin(angle + 0.55))
    draw.polygon((end, left, right), fill=color)


def _save(im, name):
    im.save(FIG_DIR / name, optimize=True)


def fig1_feature_map():
    im, d = _canvas("Continuum AI — Capability Map", "Governed knowledge continuity built around project work, verified knowledge, and scoped access")
    _box(d, (760, 180, 1440, 320), "CONTINUUM AI\nKnowledge continuity platform", TEAL, 34)

    groups = [
        (80, 440, 700, 1030, "Platform governance", PURPLE,
         ["Platform Operator", "Provision Organization", "Bootstrap first Admin", "Health and configuration"]),
        (790, 440, 1410, 1030, "Organization and work", BLUE,
         ["Organization Admin", "Organization users / roles / scopes", "Project from any ACTIVE member", "Project / Team scoped access"]),
        (1500, 440, 2120, 1030, "Knowledge continuity", GOLD,
         ["Continuum Task API", "Work Notes and evidence", "Human verification", "Evidence-grounded Q&A / handover"]),
    ]
    for x1, y1, x2, y2, title, fill, labels in groups:
        d.rounded_rectangle((x1, y1, x2, y2), radius=28, fill=PALE, outline="#AAB8C7", width=3)
        d.text(((x1 + x2) // 2, y1 + 25), title, font=_font(31, True), fill=INK, anchor="mt")
        gap = 22
        box_h = (y2 - y1 - 115 - gap * (len(labels) - 1)) // len(labels)
        for idx, label in enumerate(labels):
            top = y1 + 85 + idx * (box_h + gap)
            _box(d, (x1 + 38, top, x2 - 38, top + box_h), label, fill, 24, radius=16)
    for x in (390, 1100, 1810):
        _arrow(d, (x, 440), (1100, 326), color="#60758A", width=4, head=15)
    _box(d, (480, 1120, 1720, 1245), "Access is resolved from active membership + explicit Project / Team scope + content ACL", GREEN, 27)
    _save(im, "fig1_feature_map.png")


def fig2_core_loop():
    im, d = _canvas("Continuum AI — Knowledge Continuity Loop", "Task work becomes verified, permission-aware knowledge that supports a safe handover")
    top = [
        (90, 250, 540, 430, "1. Record work\nContinuum Task API", BLUE),
        (620, 250, 1070, 430, "2. Capture context\nWork Note / evidence", TEAL),
        (1150, 250, 1600, 430, "3. Review and verify\nHuman approval", GOLD),
        (1680, 250, 2130, 430, "4. Index eligible sources\nSAG retrieval", PURPLE),
    ]
    for x1, y1, x2, y2, label, fill in top:
        _box(d, (x1, y1, x2, y2), label, fill, 26)
    for i in range(3):
        _arrow(d, (top[i][2] + 12, 340), (top[i + 1][0] - 12, 340))
    bottom = [
        (1680, 710, 2130, 900, "5. Ask with evidence\nACL checked before answer", GREEN),
        (1150, 710, 1600, 900, "6. Prepare handover\nTask + verified knowledge", BLUE),
        (620, 710, 1070, 900, "7. Successor receives\nscoped context and actions", TEAL),
        (90, 710, 540, 900, "8. Learn and update\nWork continues in task", GOLD),
    ]
    for x1, y1, x2, y2, label, fill in bottom:
        _box(d, (x1, y1, x2, y2), label, fill, 25)
    for i in range(3):
        _arrow(d, (bottom[i][0] - 12, 805), (bottom[i + 1][2] + 12, 805))
    _arrow(d, (1905, 445), (1905, 695), color="#60758A")
    _arrow(d, (315, 695), (315, 445), color="#60758A")
    _box(d, (510, 1030, 1690, 1175), "Authorization is enforced at each step\n(read · review · retrieval · handover)", PALE, 26)
    _save(im, "fig2_core_loop.png")


def fig3_gantt():
    im, d = _canvas("Continuum AI — Delivery Plan", "Ten-week plan; exact dates and remaining team capacity should be confirmed by the project owner")
    x0, y0 = 570, 245
    col = 150
    row_h = 135
    names = ["Scope and requirements", "Organization / Project / ACL", "Continuum Task management", "Knowledge capture and review", "SAG retrieval and grounded Q&A", "Handover and integration", "Hardening and release"]
    phases = [(0, 1), (0, 4), (1, 5), (3, 6), (4, 8), (6, 9), (8, 10)]
    for week in range(10):
        x = x0 + week * col
        d.text((x + col // 2, y0 - 45), f"W{week + 1}", font=_font(22, True), fill=INK, anchor="mm")
        d.line((x, y0, x, y0 + row_h * len(names)), fill="#D9E0E7", width=2)
    d.line((x0 + 10 * col, y0, x0 + 10 * col, y0 + row_h * len(names)), fill="#D9E0E7", width=2)
    colors = [PURPLE, BLUE, TEAL, GOLD, GREEN, ORANGE, "#DDE4EF"]
    for idx, (name, (start, finish)) in enumerate(zip(names, phases)):
        y = y0 + idx * row_h
        d.text((x0 - 25, y + row_h // 2), name, font=_font(23, True), fill=INK, anchor="rm")
        d.line((x0, y + row_h, x0 + 10 * col, y + row_h), fill="#D9E0E7", width=2)
        bx1 = x0 + start * col + 9
        bx2 = x0 + finish * col - 9
        d.rounded_rectangle((bx1, y + 25, bx2, y + row_h - 25), radius=17, fill=colors[idx], outline=INK, width=2)
    d.text((x0, y0 + row_h * len(names) + 55), "Plan is a working sequence, not a verified progress report.", font=_font(24), fill=MUTED)
    _save(im, "fig3_schedule.png")


def fig4_git_flow():
    im, d = _canvas("Continuum AI — Delivery and Review Flow", "Task management is implemented in the existing BE / FE repositories with a clear backend service boundary")
    _box(d, (90, 280, 520, 470), "Continuum Task API\ncanonical task source", TEAL, 29)
    _box(d, (650, 280, 1050, 470), "Feature branch\nBE or FE repository", BLUE, 28)
    _arrow(d, (535, 375), (635, 375))
    lanes = [
        (1200, 170, "Backend PR", PURPLE),
        (1200, 400, "Frontend PR", GOLD),
        (1200, 630, "DB contract / migration review", GREEN),
    ]
    bus_x = 1900
    review_y = 970
    for x, y, label, fill in lanes:
        center_y = y + 80
        _box(d, (x, y, x + 620, y + 160), label, fill, 28)
        _arrow(d, (1065, 375), (1185, center_y), color="#60758A", width=4, head=14)
        d.line(((x + 620, center_y), (bus_x, center_y)), fill="#60758A", width=4)
    d.line(((bus_x, lanes[0][1] + 80), (bus_x, review_y)), fill="#60758A", width=4)
    d.line(((bus_x, lanes[-1][1] + 80), (bus_x, review_y)), fill="#60758A", width=4)
    _box(d, (1200, 890, 1820, 1040), "Review + CI\nAPI and ACL alignment", ORANGE, 27)
    _arrow(d, (bus_x, review_y), (1830, review_y), color="#60758A", width=4, head=14)
    _box(d, (1200, 1110, 1820, 1270), "Merge after human review\nRelease from main", TEAL, 27)
    _arrow(d, (1510, 1045), (1510, 1095))
    _save(im, "fig4_git_flow.png")
