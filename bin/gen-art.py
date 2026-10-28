#!/usr/bin/env python3
"""为站点生成成套的抽象封面 / 详情图 / 头像 / favicon（纯 SVG，无外部依赖）。
替换成真实照片时，直接把同名文件换成 .jpg/.png 并改 front matter 里的路径即可。
"""
import os
import math

OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img"
)
os.makedirs(os.path.join(OUT, "work"), exist_ok=True)

# slug, 渐变色, 强调色, 图案
SERIES = [
    ("aosp-qa-platform",   ("#3B1E8C", "#E15A8C"), "#FFD9E8", "rings"),
    ("device-farm",        ("#0D042B", "#4A2FA8"), "#9B83FF", "dots"),
    ("ci-pipeline",        ("#2B1B5A", "#8B5CF6"), "#E7DBFF", "bars"),
    ("observability",      ("#102B3A", "#2E8BC0"), "#B8ECFF", "waves"),
    ("api-sandbox",        ("#3A2E6E", "#C58AF9"), "#F3E4FF", "mesh"),
    ("knowledge-automation", ("#101F3A", "#3F5BD8"), "#C8D4FF", "stripes"),
    ("flash-toolchain",    ("#1E2A47", "#5B7CFA"), "#D6E0FF", "bars"),
    ("log-search",         ("#2A1A33", "#B84FB0"), "#FFD6F5", "rings"),
]


def grain(idx):
    return (
        f'<filter id="g{idx}"><feTurbulence type="fractalNoise" baseFrequency="0.9" '
        f'numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/>'
        f'<feComponentTransfer><feFuncA type="linear" slope="0.16"/></feComponentTransfer>'
        f'</filter>'
    )


def motif(kind, w, h, accent):
    cx, cy = w * 0.5, h * 0.5
    if kind == "rings":
        out = []
        for i in range(9):
            r = w * (0.06 + i * 0.055)
            out.append(f'<circle cx="{cx:.0f}" cy="{cy*1.05:.0f}" r="{r:.0f}" fill="none" '
                       f'stroke="{accent}" stroke-opacity="{0.42 - i*0.035:.2f}" stroke-width="{2 if i%2 else 1}"/>')
        out.append(f'<circle cx="{cx*0.78:.0f}" cy="{cy*0.72:.0f}" r="{w*0.11:.0f}" fill="{accent}" fill-opacity="0.13"/>')
        return "".join(out)
    if kind == "dots":
        out = []
        step = w / 26
        for gx in range(26):
            for gy in range(int(h / step) + 1):
                x, y = gx * step, gy * step
                d = math.hypot(x - cx * 0.85, y - cy) / (w * 0.62)
                o = max(0.0, 0.55 - d * 0.55)
                if o <= 0.02:
                    continue
                r = max(1.2, 3.4 - d * 2.4)
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{accent}" fill-opacity="{o:.2f}"/>')
        return "".join(out)
    if kind == "bars":
        out = []
        n = 16
        bw = w / (n * 2.1)
        for i in range(n):
            x = w * 0.08 + i * (bw * 2.1)
            bh = h * (0.16 + 0.62 * abs(math.sin(i * 0.62 + 0.4)))
            out.append(f'<rect x="{x:.0f}" y="{h*0.82-bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" '
                       f'rx="{bw/2:.0f}" fill="{accent}" fill-opacity="{0.16 + (i % 4) * 0.09:.2f}"/>')
        return "".join(out)
    if kind == "waves":
        out = []
        for i in range(7):
            amp = h * (0.03 + i * 0.012)
            y0 = h * (0.34 + i * 0.085)
            pts = []
            for step in range(0, w + 20, 20):
                y = y0 + math.sin(step / w * math.pi * 3.2 + i * 0.7) * amp
                pts.append(f"{step},{y:.1f}")
            out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{accent}" '
                       f'stroke-opacity="{0.42 - i*0.045:.2f}" stroke-width="1.6"/>')
        return "".join(out)
    if kind == "mesh":
        out = []
        cols, rows = 10, 7
        pts = []
        for r in range(rows):
            row = []
            for c in range(cols):
                x = w * 0.1 + c * (w * 0.8 / (cols - 1))
                y = h * 0.16 + r * (h * 0.68 / (rows - 1))
                wob = math.sin(c * 0.9 + r * 0.6) * h * 0.026
                row.append((x, y + wob))
            pts.append(row)
        for r in range(rows - 1):
            for c in range(cols - 1):
                poly = " ".join(
                    f"{pts[rr][cc][0]:.0f},{pts[rr][cc][1]:.0f}"
                    for rr, cc in ((r, c), (r, c + 1), (r + 1, c + 1), (r + 1, c))
                )
                o = 0.05 + 0.11 * ((r + c) % 3) / 2
                out.append(f'<polygon points="{poly}" fill="{accent}" fill-opacity="{o:.2f}" '
                           f'stroke="{accent}" stroke-opacity="0.12" stroke-width="0.7"/>')
        return "".join(out)
    if kind == "stripes":
        out = [f'<g transform="rotate(-24 {cx} {cy})">']
        x = -w
        while x < w * 2:
            out.append(f'<rect x="{x:.0f}" y="{-h}" width="{w*0.012:.1f}" height="{h*3}" '
                       f'fill="{accent}" fill-opacity="0.14"/>')
            x += w * 0.045
        out.append("</g>")
        out.append(f'<circle cx="{w*0.74:.0f}" cy="{h*0.42:.0f}" r="{w*0.2:.0f}" fill="{accent}" fill-opacity="0.08"/>')
        return "".join(out)
    return ""


def cover(slug, colors, accent, kind, w=1600, h=1000, idx=0):
    (c1, c2) = colors
    label = slug.replace("-", " ").upper()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<defs>
  <linearGradient id="bg{idx}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>
  </linearGradient>
  <radialGradient id="halo{idx}" cx="0.72" cy="0.24" r="0.72">
    <stop offset="0" stop-color="{accent}" stop-opacity="0.30"/>
    <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
  </radialGradient>
  {grain(idx)}
</defs>
<rect width="{w}" height="{h}" fill="url(#bg{idx})"/>
<rect width="{w}" height="{h}" fill="url(#halo{idx})"/>
{motif(kind, w, h, accent)}
<rect width="{w}" height="{h}" fill="#fff" filter="url(#g{idx})" opacity="0.5"/>
<g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="{accent}">
  <text x="{w*0.055:.0f}" y="{h*0.945:.0f}" font-size="{h*0.021:.0f}" letter-spacing="{h*0.009:.0f}" opacity="0.6">JEKYLL · PORTFOLIO · {label}</text>
</g>
<text x="{w*0.94:.0f}" y="{h*0.95:.0f}" text-anchor="end" font-family="ui-sans-serif, Helvetica, Arial, sans-serif"
      font-size="{h*0.30:.0f}" font-weight="700" fill="none" stroke="{accent}" stroke-opacity="0.34"
      stroke-width="{h*0.002:.1f}" letter-spacing="-6">0{idx+1}</text>
</svg>
'''


def detail(slug, colors, accent, kind, w=1400, h=900, idx=0):
    (c1, c2) = colors
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<defs>
  <linearGradient id="db{idx}" x1="1" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{c2}"/><stop offset="1" stop-color="{c1}"/>
  </linearGradient>
  {grain(idx + 40)}
</defs>
<rect width="{w}" height="{h}" fill="url(#db{idx})"/>
{motif(kind, w, h, accent)}
<rect width="{w}" height="{h}" fill="#000" filter="url(#g{idx+40})" opacity="0.32"/>
</svg>
'''


for i, (slug, colors, accent, kind) in enumerate(SERIES):
    with open(os.path.join(OUT, "work", f"{slug}.svg"), "w") as f:
        f.write(cover(slug, colors, accent, kind, idx=i))
    for g in (1, 2):
        with open(os.path.join(OUT, "work", f"{slug}-{g}.svg"), "w") as f:
            f.write(detail(slug, colors, accent, kind, idx=i * 2 + g))

# ---- 头像（几何化肖像，不放真人照片）----
avatar = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="880" viewBox="0 0 800 880" role="img">
<defs>
  <linearGradient id="ab" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#1A0F3D"/><stop offset="0.55" stop-color="#4B2B9E"/><stop offset="1" stop-color="#C4468F"/>
  </linearGradient>
  <radialGradient id="al" cx="0.72" cy="0.18" r="0.8">
    <stop offset="0" stop-color="#9B83FF" stop-opacity="0.55"/><stop offset="1" stop-color="#9B83FF" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="af" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#F6F1FF" stop-opacity="0.95"/><stop offset="1" stop-color="#D8C8F7" stop-opacity="0.75"/>
  </linearGradient>
  <filter id="ag"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3"/>
    <feColorMatrix type="saturate" values="0"/>
    <feComponentTransfer><feFuncA type="linear" slope="0.13"/></feComponentTransfer></filter>
</defs>
<rect width="800" height="880" fill="url(#ab)"/>
<rect width="800" height="880" fill="url(#al)"/>
<g opacity="0.5">
  <circle cx="640" cy="150" r="180" fill="none" stroke="#FFD9E8" stroke-opacity="0.35"/>
  <circle cx="640" cy="150" r="250" fill="none" stroke="#FFD9E8" stroke-opacity="0.18"/>
  <circle cx="640" cy="150" r="320" fill="none" stroke="#FFD9E8" stroke-opacity="0.1"/>
</g>
<!-- 肩颈 -->
<path d="M120 880c0-150 125-232 280-232s280 82 280 232z" fill="url(#af)" opacity="0.28"/>
<!-- 头部 -->
<circle cx="400" cy="380" r="168" fill="url(#af)" opacity="0.30"/>
<circle cx="400" cy="380" r="168" fill="none" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="2"/>
<!-- 侧光 -->
<path d="M400 212a168 168 0 0 1 0 336 200 200 0 0 0 0-336z" fill="#FFD9E8" opacity="0.16"/>
<!-- 点阵 -->
<g fill="#FFD9E8" opacity="0.5">
  <circle cx="132" cy="618" r="3"/><circle cx="164" cy="618" r="3"/><circle cx="196" cy="618" r="3"/>
  <circle cx="132" cy="650" r="3"/><circle cx="164" cy="650" r="3"/><circle cx="196" cy="650" r="3"/>
  <circle cx="132" cy="682" r="3"/><circle cx="164" cy="682" r="3"/><circle cx="196" cy="682" r="3"/>
</g>
<rect width="800" height="880" fill="#fff" filter="url(#ag)" opacity="0.6"/>
</svg>
'''
with open(os.path.join(OUT, "avatar.svg"), "w") as f:
    f.write(avatar)

favicon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
<defs><linearGradient id="f" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#6C4CF1"/><stop offset="0.5" stop-color="#A147EE"/><stop offset="1" stop-color="#E15A8C"/>
</linearGradient></defs>
<rect width="64" height="64" rx="16" fill="url(#f)"/>
<text x="32" y="44" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="34"
      font-weight="700" fill="#fff" letter-spacing="-2">W</text>
</svg>
'''
with open(os.path.join(OUT, "favicon.svg"), "w") as f:
    f.write(favicon)

print("generated:", len(os.listdir(os.path.join(OUT, "work"))), "work images + avatar + favicon")
