#!/usr/bin/env python3
"""Generate dark.svg / light.svg -- the terminal profile card for erroldmell0."""

import html
from PIL import Image, ImageFilter, ImageOps

W, H = 1180, 586
COLS, ROWS = 93, 58
CELL_W, CELL_H = 4.892, 7.55   # monospace cell at font-size 7.4px
ASCII_X, ASCII_W = 25, 455     # left panel text box
CROP = (48, 212, 802, 1010)   # head, glasses, beak and scarf knot -- skips the body
BLUR = 0.0                     # >0 only helps noisy photos; flat art wants none
CUTOFF = 1                     # autocontrast percentile clipped at each end
RAMP = "@8%#mnesoa*+=-:.  "  # dark -> light

PROMPT = "errol@dmello ~ % whoami --verbose"
HEAD = "errol@dmello"
LEFT_PANEL = "AVATAR.ASCII"
RIGHT_PANEL = "PROFILE.INFO"
STATUS = "ONLINE"

# Panel contents. Keep this at 25 rows or fewer and values at 48 chars or fewer,
# or the text runs past the panel. "__head__", "__blank__" and "__section__"
# are layout rows rather than fields.
LINES = [
    ("__head__", None),
    ("Name", "Errol D\u2019mello"),
    ("Role", "Computer Engineering Student"),
    ("Tagline", "I Solve. I Build. I Learn."),
    ("Problems", "600+ DSA problems solved"),
    ("__blank__", None),
    ("__section__", "College"),
    ("Institute", "Dwarkadas J. Sanghvi College of Engineering"),
    ("Degree", "B.Tech Computer Engg. + Honours in DS"),
    ("CGPA", "9.25  (Aug 2023 \u2013 Present)"),
    ("Location", "Mumbai, Maharashtra, India"),
    ("__blank__", None),
    ("__section__", "Tech Stack"),
    ("Languages", "Java, Python, JavaScript, C"),
    ("Frontend", "React.js, HTML, CSS, Tailwind, Bootstrap"),
    ("Backend", "Node.js, Express.js"),
    ("Databases", "MongoDB, Mongoose, MySQL"),
    ("Tools", "Git, GitHub, Postman"),
    ("Concepts", "DSA, OOP, Machine Learning"),
    ("__blank__", None),
    ("__section__", "Connect"),
    ("Email", "erroldmello2005@gmail.com"),
    ("Portfolio", "errol-dmello.vercel.app"),
    ("LinkedIn", "linkedin.com/in/errol-dmell0"),
    ("GitHub", "github.com/erroldmell0"),
]

DOT_COL = 27      # every value starts on column 28
FONT = 14.0       # info-panel type size
CHARW = FONT * 0.6
STEP = 19.0       # baseline-to-baseline in the info panel


def ascii_art(path):
    im = Image.open(path).convert("L").crop(CROP)
    # pick a column count that renders the crop without stretching it
    cols = min(COLS, max(20, round(ROWS * CELL_H / CELL_W * im.width / im.height)))
    if BLUR:
        im = im.filter(ImageFilter.GaussianBlur(BLUR))
    im = ImageOps.autocontrast(im, cutoff=CUTOFF)
    im = im.resize((cols, ROWS), Image.LANCZOS)
    px = im.load()
    n = len(RAMP) - 1
    rows = [
        "".join(RAMP[int(px[x, y] / 255 * n)] for x in range(cols))
        for y in range(ROWS)
    ]
    width = cols * CELL_W
    return rows, ASCII_X + (ASCII_W - width) / 2, width


THEMES = {
    "dark": dict(
        bg0="#0B1120", bg1="#050816", panel="#0B1120", panel_op="0.35",
        ascii_a="#38BDF8", ascii_b="#22D3EE", ascii_c="#60A5FA",
        b0="#22C55E", b1="#10B981", b2="#34D399",
        key="#4ADE80", value="#FFFFFF", cc="#1E3A2F", head="#22C55E",
        accent="#34D399", term="#86EFAC",
        ptitle="#22C55E", ptitle2="#38BDF8", cursor="#22C55E",
        status="#4ADE80", scanline="#7DD3FC", scanline_op="0.05", beam="#22C55E", beam_hi="#86EFAC",
        titlebar_op="0.85",
    ),
    "light": dict(
        bg0="#F8FAFC", bg1="#E2E8F0", panel="#FFFFFF", panel_op="0.55",
        ascii_a="#047857", ascii_b="#0F766E", ascii_c="#059669",
        b0="#059669", b1="#0D9488", b2="#10B981",
        key="#0D9488", value="#0F172A", cc="#CBD5E1", head="#059669",
        accent="#059669", term="#0D9488",
        ptitle="#059669", ptitle2="#0EA5E9", cursor="#059669",
        status="#059669", scanline="#0EA5E9", scanline_op="0.04", beam="#059669", beam_hi="#34D399",
        titlebar_op="0.75",
    ),
}


def build(theme_name, art, ax, aw):
    t = THEMES[theme_name]
    e = html.escape
    out = []
    A = out.append

    A('<?xml version="1.0" encoding="UTF-8"?>')
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    A("<defs>")
    A(f'''  <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{t['ascii_a']}">
      <animate attributeName="stop-color" values="{t['ascii_a']};{t['ascii_b']};{t['ascii_c']};{t['ascii_a']}" dur="8s" repeatCount="indefinite"/>
    </stop>
    <stop offset="100%" stop-color="{t['ascii_b']}">
      <animate attributeName="stop-color" values="{t['ascii_b']};{t['ascii_c']};{t['ascii_a']};{t['ascii_b']}" dur="8s" repeatCount="indefinite"/>
    </stop>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{t['b0']}"/>
    <stop offset="50%" stop-color="{t['b1']}"/>
    <stop offset="100%" stop-color="{t['b2']}"/>
  </linearGradient>
  <radialGradient id="bgGlow" cx="30%" cy="20%" r="80%">
    <stop offset="0%" stop-color="{t['bg0']}"/>
    <stop offset="100%" stop-color="{t['bg1']}"/>
  </radialGradient>
  <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{t['beam']}" stop-opacity="0"/>
    <stop offset="45%" stop-color="{t['beam']}" stop-opacity="0.06"/>
    <stop offset="50%" stop-color="{t['beam_hi']}" stop-opacity="0.55"/>
    <stop offset="55%" stop-color="{t['beam']}" stop-opacity="0.06"/>
    <stop offset="100%" stop-color="{t['b1']}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="{t['scanline']}" opacity="{t['scanline_op']}"/>
  </pattern>
''')

    A(f'''  <style>
    .ascii  {{ font-family: 'Courier New', Consolas, monospace; font-size: 7.4px; fill: url(#asciiGrad); letter-spacing: -0.2px; }}
    .key    {{ font-family: 'Courier New', Consolas, monospace; font-size: {FONT:.0f}px; fill: {t['key']}; font-weight: bold; }}
    .value  {{ font-family: 'Courier New', Consolas, monospace; font-size: {FONT:.0f}px; fill: {t['value']}; font-weight: 500; }}
    .cc     {{ font-family: 'Courier New', Consolas, monospace; font-size: {FONT:.0f}px; fill: {t['cc']}; }}
    .head   {{ font-family: 'Courier New', Consolas, monospace; font-size: {FONT + 2:.0f}px; fill: {t['head']}; font-weight: bold; }}
    .accent {{ font-family: 'Courier New', Consolas, monospace; font-size: {FONT:.0f}px; fill: {t['accent']}; font-weight: bold; }}
    text, tspan {{ white-space: pre; }}
    .term-label {{ font-family: 'Courier New', Consolas, monospace; font-size: 12px; fill: {t['term']}; letter-spacing: 0.5px; opacity: 0.8; }}
    .scan-label {{ font-family: 'Courier New', Consolas, monospace; font-size: 10px; fill: {t['status']}; letter-spacing: 1px; }}
    .panel-title       {{ font-family: 'Courier New', Consolas, monospace; font-size: 11px; fill: {t['ptitle']}; letter-spacing: 2px; opacity: 0.85; }}
    .panel-title-blue  {{ font-family: 'Courier New', Consolas, monospace; font-size: 11px; fill: {t['ptitle2']}; letter-spacing: 2px; opacity: 0.85; }}
    .cursor-blink {{ fill: {t['cursor']}; }}
  </style>''')
    A("</defs>")
    A("")
    A(f'<rect width="{W}" height="{H}" rx="18" fill="url(#bgGlow)"/>')
    A(f'<rect width="{W}" height="{H}" rx="18" fill="url(#scanlines)"/>')
    A("")

    # title bar
    A(f'''<g id="titlebar">
  <rect x="3" y="3" width="1174" height="34" rx="16" fill="{t['panel']}" fill-opacity="{t['titlebar_op']}"/>
  <circle cx="24" cy="20" r="5" fill="#EF4444"><animate attributeName="opacity" values="1;0.55;1" dur="4s" repeatCount="indefinite"/></circle>
  <circle cx="42" cy="20" r="5" fill="#F59E0B"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.3s" repeatCount="indefinite"/></circle>
  <circle cx="60" cy="20" r="5" fill="#10B981"><animate attributeName="opacity" values="1;0.55;1" dur="4s" begin="0.6s" repeatCount="indefinite"/></circle>
  <text x="590" y="25" text-anchor="middle" class="term-label">{e(PROMPT)}</text>
  <circle cx="1070" cy="20" r="4" fill="{t['status']}">
    <animate attributeName="opacity" values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/>
  </circle>
  <text x="1080" y="24" class="scan-label">{STATUS}</text>
</g>''')
    A("")
    A('<g transform="translate(0,44)">')
    A(f'  <rect x="14" y="18" width="488" height="490" rx="14" fill="{t["panel"]}" fill-opacity="{t["panel_op"]}" stroke="url(#borderGrad)" stroke-width="1" opacity="0.35"/>')
    A(f'  <rect x="508" y="8" width="655" height="518" rx="14" fill="{t["panel"]}" fill-opacity="{t["panel_op"]}" stroke="url(#borderGrad)" stroke-width="1" opacity="0.35"/>')
    A(f'  <text x="30" y="14" class="panel-title-blue">{LEFT_PANEL}</text>')
    A(f'  <text x="524" y="6" class="panel-title">{RIGHT_PANEL}</text>')
    A("")

    # ascii portrait
    A('  <g>')
    A('  <text x="30" y="0" class="ascii">')
    for i, row in enumerate(art):
        y = 40 + i * 7.55
        A(f'<tspan x="{ax:.1f}" y="{y:.2f}" textLength="{aw:.1f}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{e(row)}</tspan>')
    A("  </text>")
    A("  </g>")
    A("")

    # info panel
    rule = " -" + "—" * 44 + "-—-"
    for i, (key, val) in enumerate(LINES):
        ty = 42 if i == 0 else 66 + (i - 1) * STEP
        A(f'  <g><text x="520" y="0" fill="{t["value"]}">', )
        if key == "__head__":
            body = f'<tspan x="520" y="{ty:.1f}" class="head">{e(HEAD)}</tspan><tspan class="cc">{e(rule)}</tspan>'
        elif key == "__blank__":
            body = f'<tspan x="520" y="{ty:.1f}" class="cc">. </tspan>'
        elif key == "__section__":
            body = (f'<tspan x="520" y="{ty:.1f}" class="accent">- {e(val)}</tspan>'
                    f'<tspan class="cc">{e(rule)}</tspan>')
        else:
            dots = "." * max(1, DOT_COL - len(key) - 4)
            parts = key.split(".")
            keyspan = '<tspan class="cc">.</tspan>'.join(
                f'<tspan class="key">{e(p)}</tspan>' for p in parts)
            body = (f'<tspan x="520" y="{ty:.1f}" class="cc">. </tspan>{keyspan}'
                    f'<tspan class="cc">: {dots} </tspan>'
                    f'<tspan class="value">{e(val)}</tspan>')
        out[-1] = out[-1] + body + "</text></g>"
    A("")

    last = LINES[-1][1]
    # sit just after the last value, not in that row's dot leaders
    cx = 520 + (DOT_COL + 1 + len(last) + 1) * CHARW
    cy = 66 + (len(LINES) - 2) * STEP
    A(f'''  <rect x="{cx:.1f}" y="{cy - 12:.1f}" width="{CHARW:.1f}" height="{FONT:.0f}" class="cursor-blink" opacity="0.9"/>''')
    A("</g>")
    A("")
    A(f'''<rect x="0" y="-70" width="{W}" height="70" fill="url(#scanGrad)" opacity="0.7" style="mix-blend-mode:screen">
  <animateTransform attributeName="transform" type="translate" from="0 -70" to="0 630" dur="4.2s" repeatCount="indefinite"/>
</rect>''')
    A(f'''<rect x="3" y="3" width="1174" height="580" rx="16" fill="none" stroke="url(#borderGrad)" stroke-width="2" opacity="0.8">
  <animate attributeName="opacity" values="0.5;0.95;0.5" dur="3.2s" repeatCount="indefinite"/>
</rect>''')
    A("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    art, ax, aw = ascii_art("avatar.png")
    for name in ("dark", "light"):
        with open(f"{name}.svg", "w") as fh:
            fh.write(build(name, art, ax, aw))
        print(f"wrote {name}.svg")
