#!/usr/bin/env python3
"""Build the theme-aware SVG cards used by the ghiata profile README.

Every card is drawn twice: ``*-day.svg`` and ``*-night.svg``.  The README
selects the right variant with ``<picture><source media="(prefers-color-scheme: ...)">``,
so GitHub handles the switch without JavaScript or CSS.

Usage: python scripts/build_assets.py
No third-party dependencies.
"""

from __future__ import annotations

import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

SERIF = "Newsreader, 'Iowan Old Style', Georgia, 'Times New Roman', serif"
SANS = "'Instrument Sans', ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif"
MONO = "'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

DAY = {
    "card": "#FBF9F5",
    "ink": "#1D1A17",
    "ink2": "#3B352F",
    "muted": "#6F665C",
    "dim": "#A0968A",
    "line": "#E7E0D6",
    "line2": "#D9D0C3",
    "human": "#B9572F",
    "human_soft": "#F3DFD3",
    "agent": "#4D7563",
    "agent_soft": "#DDE8E1",
    "spore": "#C48A2C",
    "on_accent": "#FFFFFF",
}

NIGHT = {
    "card": "#211D19",
    "ink": "#F5F1EA",
    "ink2": "#D9D2C7",
    "muted": "#A79C8E",
    "dim": "#7A7166",
    "line": "#3A342C",
    "line2": "#4A4238",
    "human": "#E08A62",
    "human_soft": "#3A2A22",
    "agent": "#86B39D",
    "agent_soft": "#23332B",
    "spore": "#E0B15C",
    "on_accent": "#16130F",
}


def text(
    x,
    y,
    value,
    size,
    fill,
    family=SANS,
    weight=400,
    anchor="start",
    spacing=None,
    opacity=None,
):
    attrs = [
        f'x="{x:.1f}"',
        f'y="{y:.1f}"',
        f'font-family="{family}"',
        f'font-size="{size}"',
        f'font-weight="{weight}"',
        f'fill="{fill}"',
        f'text-anchor="{anchor}"',
    ]
    if spacing is not None:
        attrs.append(f'letter-spacing="{spacing}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    return f'  <text {" ".join(attrs)}>{escape(value)}</text>'


def frame(p, width, height, radius=18):
    return (
        f'  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" '
        f'rx="{radius}" fill="{p["card"]}" stroke="{p["line2"]}" stroke-width="1.5"/>'
    )


def write_svg(name, width, height, body):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" height="100%">\n' + "\n".join(body) + "\n</svg>\n"
    )
    path = ASSETS / name
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    return path


# ---------------------------------------------------------------------------
# hero
# ---------------------------------------------------------------------------


def hero(p):
    width, height = 880, 250
    body = [frame(p, width, height)]

    body.append(text(34, 41, "ENGINEERING LEADER  ·  AMSTERDAM", 10.5, p["muted"], MONO, 500, spacing=1.6))
    body.append(text(32, 101, "Stefan Ghiata", 58, p["ink"], SERIF, 500))
    body.append(text(34, 137, "Fifteen years of software that had to be right:", 15, p["ink2"], SANS, 500))
    body.append(text(34, 159, "Banking, insurance, hosting. Now AI with humans in the loop.", 15, p["ink2"], SANS, 500))

    stats = [
        ("15+", "YEARS SHIPPING", p["human"], 34),
        ("8", "YRS LEADING", p["agent"], 196),
        ("DNB · EU", "COMPLIANCE", p["spore"], 340),
    ]
    for value, label, colour, x in stats:
        body.append(
            f'  <text x="{x}" y="207" font-family="{MONO}" font-size="10" '
            f'letter-spacing="0.8" fill="{p["muted"]}">'
            f'<tspan fill="{colour}" font-weight="700">{escape(value)}</tspan> {label}</text>'
        )
    for x in (180, 318):
        body.append(f'  <circle cx="{x}" cy="203.5" r="1.4" fill="{p["line2"]}"/>')

    # The loop: six stages around a human checkpoint.
    cx, cy, radius = 705.0, 125.0, 72.0
    body.append(
        f'  <g>\n'
        f'    <circle cx="{cx}" cy="{cy}" r="88" fill="none" stroke="{p["line"]}" '
        f'stroke-width="1" stroke-dasharray="2 7"/>\n'
        f'    <animateTransform attributeName="transform" type="rotate" '
        f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="60s" repeatCount="indefinite"/>\n'
        f'  </g>'
    )
    body.append(f'  <circle cx="{cx}" cy="{cy}" r="39" fill="none" stroke="{p["line2"]}" stroke-width="1" stroke-dasharray="1.5 5"/>')
    body.append(f'  <circle cx="{cx}" cy="{cy}" r="39" fill="{p["card"]}" opacity="0.55"/>')

    stages = [
        (270, "PLAN", p["spore"]),
        (330, "BUILD", p["agent"]),
        (30, "CHECK", p["agent"]),
        (90, "REVIEW", p["human"]),
        (150, "PREVIEW", p["spore"]),
        (210, "DEPLOY", p["agent"]),
    ]
    for angle, label, colour in stages:
        a = math.radians(angle)
        x = cx + radius * math.cos(a)
        y = cy + radius * math.sin(a)
        if label == "REVIEW":
            body.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="none" stroke="{colour}" stroke-width="1.2" opacity="0.55"/>')
            body.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="4.6" fill="{colour}"/>')
        else:
            body.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{colour}"/>')

        lx = cx + (radius + 15) * math.cos(a)
        ly = cy + (radius + 15) * math.sin(a) + 3
        if angle == 270:
            anchor, ly = "middle", cy - radius - 15
        elif angle == 90:
            anchor, ly = "middle", cy + radius + 21
        elif 0 < angle < 180:
            anchor = "start"
        else:
            anchor = "end"
        body.append(text(lx, ly, label, 8, p["muted"], MONO, 600, anchor=anchor, spacing=0.9))

    body.append(text(cx, cy + 1, "HUMAN", 17, p["ink"], SERIF, 500, anchor="middle"))
    body.append(text(cx, cy + 15, "IN THE LOOP", 7, p["human"], MONO, 700, anchor="middle", spacing=1.1))

    return width, height, body


# ---------------------------------------------------------------------------
# navigation pills
# ---------------------------------------------------------------------------


def nav(p, key, label, value, colour):
    height = 30
    label_width = 44
    width = int(label_width + 6.35 * len(value) + 18)
    body = [
        f'  <rect x="1" y="1" width="{width - 2}" height="28" rx="8" fill="{p["card"]}" stroke="{p["line2"]}" stroke-width="1.2"/>',
        f'  <path d="M 8,1 H {label_width} V 29 H 8 A 7,7 0 0 1 1,22 V 8 A 7,7 0 0 1 8,1 Z" fill="{colour}"/>',
        text(label_width / 2, 19, label, 9.5, p["on_accent"], MONO, 700, anchor="middle", spacing=0.8),
        text(label_width + (width - label_width) / 2, 19, value, 10, p["ink2"], MONO, 500, anchor="middle"),
    ]
    return width, height, body


# ---------------------------------------------------------------------------
# pillars
# ---------------------------------------------------------------------------


def people_icon(colour):
    return (
        f'  <g transform="translate(20,18)" fill="none" stroke="{colour}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round">\n'
        f'    <circle cx="11" cy="8" r="4.4"/>\n'
        f'    <path d="M3 22c1.4-5.1 4.3-7.6 8-7.6s6.6 2.5 8 7.6"/>\n'
        f'    <circle cx="22.5" cy="11" r="3.4"/>\n'
        f'    <path d="M19.5 21.5c.9-3.7 2.9-5.6 5.8-5.6 2.4 0 4.1 1.3 5 4.1"/>\n'
        f'  </g>'
    )


def agents_icon(colour):
    return (
        f'  <g transform="translate(20,18)" fill="none" stroke="{colour}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round">\n'
        f'    <rect x="2.5" y="7" width="23" height="19" rx="5"/>\n'
        f'    <circle cx="10" cy="16" r="1.7" fill="{colour}" stroke="none"/>\n'
        f'    <circle cx="18" cy="16" r="1.7" fill="{colour}" stroke="none"/>\n'
        f'    <path d="M10.5 21.5h7"/>\n'
        f'    <path d="M14 7V2.5"/>\n'
        f'    <circle cx="14" cy="2" r="1.3" fill="{colour}" stroke="none"/>\n'
        f'  </g>'
    )


def guardrails_icon(colour):
    return (
        f'  <g transform="translate(20,18)" fill="none" stroke="{colour}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round">\n'
        f'    <path d="M14 2.5l10 3.7v8.1c0 5.9-4.4 9.4-10 11.6-5.6-2.2-10-5.7-10-11.6V6.2z"/>\n'
        f'    <path d="M9.3 14.4l3.1 3.1 5.8-6.4"/>\n'
        f'  </g>'
    )


def pillar_card(p, number, icon, title, lines, tag, colour):
    width, height = 280, 164
    body = [frame(p, width, height, 14), icon(colour)]
    body.append(text(260, 26, number, 8.5, p["dim"], MONO, 600, anchor="end", spacing=1))
    body.append(text(20, 84, title, 22, p["ink"], SERIF, 500))
    for i, line in enumerate(lines):
        body.append(text(20, 110 + i * 17, line, 12.3, p["ink2"], SANS, 500))
    body.append(text(20, 150, tag, 8.2, colour, MONO, 700, spacing=1.1))
    return body


PILLARS = [
    ("01", people_icon, "People first", ["Hiring, mentoring and ownership.", "Teams grow with the tools."], "HIRING · MENTORING", "human"),
    ("02", agents_icon, "Agents with boundaries", ["Scoped tasks, least privilege,", "sandboxes, human review."], "CLAUDE · MCP · SANDBOX", "agent"),
    ("03", guardrails_icon, "Guardrails that scale", ["Previews, tests, audits and", "small, reversible steps."], "CI/CD · IaC · DNB/EU", "spore"),
]


def pillars(p):
    """Three cards on one 880px strip, for the desktop README."""
    body = []
    for i, (number, icon, title, lines, tag, key) in enumerate(PILLARS):
        x = 8 + i * 292
        body.append(f'  <g transform="translate({x},0)">')
        body.extend(pillar_card(p, number, icon, title, lines, tag, p[key]))
        body.append("  </g>")
    return 880, 164, body


def pillars_mobile(p):
    """The same three cards stacked, for narrow viewports."""
    width = 360
    body = []
    for i, (number, icon, title, lines, tag, key) in enumerate(PILLARS):
        y = 12 + i * 116
        body.append(f'  <g transform="translate(12,{y})">')
        body.append(frame(p, 336, 104, 14))
        body.append(icon(p[key]))
        body.append(text(316, 26, number, 8.5, p["dim"], MONO, 600, anchor="end", spacing=1))
        body.append(text(58, 42, title, 20, p["ink"], SERIF, 500))
        for j, line in enumerate(lines):
            body.append(text(58, 64 + j * 16, line, 11.5, p["ink2"], SANS, 500))
        body.append(text(58, 96, tag, 7.6, p[key], MONO, 700, spacing=0.9))
        body.append("  </g>")
    return width, 360, body



# ---------------------------------------------------------------------------
# career
# ---------------------------------------------------------------------------


ROLES = [
    ("2021–now", "Managing Engineer", "Nationale-Nederlanden · people, architecture, delivery", "HEAD → main"),
    ("2018–2021", "Technical Lead", "Nationale-Nederlanden · Vue, Node.js, AWS, CloudFormation", ""),
    ("2018–2019", "Software Engineer", "ING · Angular, Spring, Kafka, credit-card lifecycle", ""),
    ("2014–2018", "Software Engineer", "ABN AMRO via Capgemini · corporate banking, iDEAL, PSD2", ""),
    ("2010–2014", "Web Developer", "1&1 Internet, Bucharest · help center, fraud & abuse tooling", "tag: v1.0"),
]


def career(p):
    width, height = 880, 330
    body = [frame(p, width, height)]

    body.append(text(30, 36, "CAREER  ·  GIT LOG --GRAPH", 10.5, p["muted"], MONO, 500, spacing=1.6))
    body.append(text(850, 36, "AMSTERDAM  ·  NL", 9.5, p["dim"], MONO, 500, anchor="end", spacing=1.2))

    line_x = 104
    first_y = 82
    step = 44
    last_y = first_y + step * (len(ROLES) - 1)
    body.append(
        f'  <line x1="{line_x}" y1="{first_y - 8}" x2="{line_x}" y2="{last_y}" '
        f'stroke="{p["line2"]}" stroke-width="1.5"/>'
    )

    for i, (dates, role, detail, tag) in enumerate(ROLES):
        y = first_y + i * step
        colour = p["human"] if i == 0 else p["card"]
        stroke = p["human"] if i == 0 else p["muted"]
        body.append(text(88, y - 1, dates, 9.5, p["muted"] if i else p["ink2"], MONO, 600, anchor="end"))
        if i == 0:
            body.append(f'  <circle cx="{line_x}" cy="{y - 5}" r="8" fill="none" stroke="{p["human"]}" stroke-width="1.1" opacity="0.55"/>')
            body.append(f'  <circle cx="{line_x}" cy="{y - 5}" r="4.6" fill="{p["human"]}"/>')
        else:
            body.append(f'  <circle cx="{line_x}" cy="{y - 5}" r="4.4" fill="{colour}" stroke="{stroke}" stroke-width="1.5"/>')
        body.append(text(122, y, role, 16.5, p["ink"], SERIF, 500))
        body.append(text(122, y + 19, detail, 11.3, p["muted"], SANS, 500))
        if tag:
            tag_colour = p["human"] if i == 0 else p["dim"]
            body.append(text(850, y - 1, tag, 9, tag_colour, MONO, 600, anchor="end", spacing=0.6))

    body.append(f'  <line x1="30" y1="292" x2="850" y2="292" stroke="{p["line"]}" stroke-width="1"/>')
    body.append(text(30, 312, "2004–2010", 9.5, p["dim"], MONO, 600))
    body.append(text(122, 312, "BSc Informatics  ·  MSc E-Commerce  ·  ASE Bucharest", 9.5, p["dim"], MONO, 500))
    return width, height, body


MOBILE_ROLES = [
    ("2021–now", "Managing Engineer", ["Nationale-Nederlanden · people,", "architecture, delivery"], True),
    ("2018–2021", "Technical Lead", ["Nationale-Nederlanden · Vue, Node.js,", "AWS, CloudFormation"], False),
    ("2018–2019", "Software Engineer", ["ING · Angular, Spring, Kafka,", "credit-card lifecycle"], False),
    ("2014–2018", "Software Engineer", ["ABN AMRO via Capgemini · corporate", "banking, iDEAL, PSD2"], False),
    ("2010–2014", "Web Developer", ["1&1 Internet, Bucharest · help center,", "fraud & abuse tooling"], False),
]


def career_mobile(p):
    """A 360px-wide career card that stays readable on phones."""
    width, height = 360, 430
    body = [frame(p, width, height)]
    body.append(text(18, 32, "CAREER  ·  GIT LOG --GRAPH", 9, p["muted"], MONO, 500, spacing=1.1))

    line_x = 28
    first_y = 64
    step = 68
    last_y = first_y + step * (len(MOBILE_ROLES) - 1)
    body.append(
        f'  <line x1="{line_x}" y1="{first_y - 8}" x2="{line_x}" y2="{last_y + 36}" '
        f'stroke="{p["line2"]}" stroke-width="1.5"/>'
    )

    for i, (dates, role, details, current) in enumerate(MOBILE_ROLES):
        y = first_y + i * step
        body.append(text(44, y - 8, dates, 8.5, p["muted"] if not current else p["ink2"], MONO, 600))
        if current:
            body.append(f'  <circle cx="{line_x}" cy="{y}" r="7.5" fill="none" stroke="{p["human"]}" stroke-width="1.1" opacity="0.55"/>')
            body.append(f'  <circle cx="{line_x}" cy="{y}" r="4.4" fill="{p["human"]}"/>')
            body.append(text(342, y - 8, "HEAD → main", 8, p["human"], MONO, 600, anchor="end"))
        else:
            body.append(f'  <circle cx="{line_x}" cy="{y}" r="4" fill="{p["card"]}" stroke="{p["muted"]}" stroke-width="1.4"/>')
        body.append(text(44, y + 8, role, 15.5, p["ink"], SERIF, 500))
        body.append(text(44, y + 23, details[0], 10.5, p["muted"], SANS, 500))
        body.append(text(44, y + 37, details[1], 10.5, p["muted"], SANS, 500))

    body.append(f'  <line x1="18" y1="392" x2="342" y2="392" stroke="{p["line"]}" stroke-width="1"/>')
    body.append(text(18, 412, "2004–2010 · BSc Informatics · MSc E-Commerce · ASE Bucharest", 8.8, p["dim"], MONO, 500))
    return width, height, body


# ---------------------------------------------------------------------------


def main():
    ASSETS.mkdir(exist_ok=True)
    cards = {
        "hero": hero,
        "career": career,
        "career-mobile": career_mobile,
        "pillars": pillars,
        "pillars-mobile": pillars_mobile,
    }

    for name, build in cards.items():
        for mode, palette in (("day", DAY), ("night", NIGHT)):
            width, height, body = build(palette)
            path = write_svg(f"{name}-{mode}.svg", width, height, body)
            print(f"wrote {path.relative_to(ROOT)}")

    links = [
        ("site", "WEB", "ghiata.com", DAY["human"]),
        ("github", "GIT", "github.com/ghiata", DAY["agent"]),
        ("linkedin", "IN", "linkedin.com/in/stefan-g", DAY["spore"]),
        ("email", "MAIL", "stefan@ghiata.com", DAY["muted"]),
    ]
    for mode, palette in (("day", DAY), ("night", NIGHT)):
        for key, label, value, accent in links:
            colour = accent if mode == "day" else {
                "site": palette["human"],
                "github": palette["agent"],
                "linkedin": palette["spore"],
                "email": palette["muted"],
            }[key]
            width, height, body = nav(palette, key, label, value, colour)
            path = write_svg(f"nav-{key}-{mode}.svg", width, height, body)
            print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
