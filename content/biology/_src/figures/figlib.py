"""Tiny SVG helper for the lesson figures.

Style: white background, thin dark strokes, at most three muted accents,
system sans-serif labels, monospace sequences placed one character at a time
(so annotations line up regardless of which monospace font the browser picks).
"""
import os, math
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "figures")

INK = "#222"; GRAY = "#666"; LIGHT = "#999"; RULE = "#ccc"
BLUE = "#3d6a9e"; RED = "#a8473a"; GREEN = "#4f7d47"
BLUE_T = "#e4ecf5"; RED_T = "#f5e4e0"; GREEN_T = "#e5eee2"; GRAY_T = "#f1f1f1"
SANS = "Helvetica Neue, Helvetica, Arial, Liberation Sans, sans-serif"
MONO = "Menlo, Consolas, DejaVu Sans Mono, Liberation Mono, monospace"

try:
    from PIL import ImageFont
    _FONTS = {}
    def _font(size, bold):
        key = (size, bold)
        if key not in _FONTS:
            fn = "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % ("Bold" if bold else "Regular")
            _FONTS[key] = ImageFont.truetype(fn, int(size * 10))
        return _FONTS[key]
    def tw(s, size=13, bold=False):
        return _font(size, bold).getlength(s) / 10.0
except Exception:  # fallback estimate
    def tw(s, size=13, bold=False):
        return len(s) * size * (0.6 if bold else 0.55)


class SVG:
    def __init__(self, w, h, title=""):
        self.w, self.h, self.title = w, h, title
        self.el = []

    # primitives -----------------------------------------------------------
    def raw(self, s): self.el.append(s)

    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=1, rx=0, dash=None, opacity=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{opacity}"' if opacity is not None else ""
        self.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def path(self, d, stroke=INK, sw=1, fill="none", dash=None):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dd} stroke-linejoin="round"/>')

    def poly(self, pts, fill=INK, stroke="none", sw=1):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.el.append(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def circle(self, cx, cy, r, fill="none", stroke=INK, sw=1):
        self.el.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=13, anchor="start", fill=INK, bold=False, italic=False, family=SANS, rotate=None):
        a = {"start": "start", "middle": "middle", "end": "end"}[anchor]
        wt = ' font-weight="bold"' if bold else ""
        it = ' font-style="italic"' if italic else ""
        rt = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate is not None else ""
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" text-anchor="{a}" fill="{fill}"{wt}{it}{rt}>{escape(s)}</text>')

    def rich(self, x, y, parts, size=13, anchor="start", family=SANS):
        """parts: list of (string, dict(fill=, bold=, italic=, sup=))"""
        a = {"start": "start", "middle": "middle", "end": "end"}[anchor]
        spans = []
        for s, st in parts:
            attrs = ""
            if st.get("fill"): attrs += f' fill="{st["fill"]}"'
            if st.get("bold"): attrs += ' font-weight="bold"'
            if st.get("italic"): attrs += ' font-style="italic"'
            if st.get("family"): attrs += f' font-family="{st["family"]}"'
            spans.append(f"<tspan{attrs}>{escape(s)}</tspan>")
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" text-anchor="{a}" fill="{INK}">{"".join(spans)}</text>')

    def mono(self, x, y, s, cw=11, size=14, fill=INK, bold=False, colors=None):
        """Monospace string, one character per cell of width cw; x = left edge of first cell.
        Returns list of cell centers."""
        xs = []
        for i, ch in enumerate(s):
            cx = x + cw * i + cw / 2
            xs.append(cx)
            if ch == " ": continue
            f = colors[i] if colors and colors[i] else fill
            self.text(cx, y, ch, size=size, anchor="middle", fill=f, bold=bold, family=MONO)
        return xs

    def arrow(self, x1, y1, x2, y2, stroke=INK, sw=1.3, head=7, kind="act", dash=None, gap=0):
        """kind: 'act' (filled arrowhead), 'inh' (flat bar), 'none'."""
        ang = math.atan2(y2 - y1, x2 - x1)
        x2 -= gap * math.cos(ang); y2 -= gap * math.sin(ang)
        if kind == "act":
            ex, ey = x2 - head * math.cos(ang) * 0.9, y2 - head * math.sin(ang) * 0.9
            self.line(x1, y1, ex, ey, stroke, sw, dash)
            a1, a2 = ang + math.radians(152), ang - math.radians(152)
            self.poly([(x2, y2), (x2 + head * math.cos(a1), y2 + head * math.sin(a1)),
                       (x2 + head * math.cos(a2), y2 + head * math.sin(a2))], fill=stroke)
        elif kind == "inh":
            self.line(x1, y1, x2, y2, stroke, sw, dash)
            px, py = -math.sin(ang), math.cos(ang)
            L = head * 0.95
            self.line(x2 - px * L, y2 - py * L, x2 + px * L, y2 + py * L, stroke, sw * 1.6)
        else:
            self.line(x1, y1, x2, y2, stroke, sw, dash)

    def curve_arrow(self, pts, stroke=INK, sw=1.3, head=7, kind="act", dash=None):
        """Quadratic bezier through control point: pts=[(x1,y1),(cx,cy),(x2,y2)]"""
        (x1, y1), (cx, cy), (x2, y2) = pts
        ang = math.atan2(y2 - cy, x2 - cx)
        if kind == "act":
            ex, ey = x2 - head * 0.9 * math.cos(ang), y2 - head * 0.9 * math.sin(ang)
        else:
            ex, ey = x2, y2
        self.path(f"M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}", stroke, sw, dash=dash)
        if kind == "act":
            a1, a2 = ang + math.radians(152), ang - math.radians(152)
            self.poly([(x2, y2), (x2 + head * math.cos(a1), y2 + head * math.sin(a1)),
                       (x2 + head * math.cos(a2), y2 + head * math.sin(a2))], fill=stroke)
        elif kind == "inh":
            px, py = -math.sin(ang), math.cos(ang)
            L = head * 0.95
            self.line(x2 - px * L, y2 - py * L, x2 + px * L, y2 + py * L, stroke, sw * 1.6)

    def box(self, x, y, w, h, label, fill="#fff", stroke=INK, size=13, bold=False, sw=1, rx=3, fill_text=INK, sub=None, subsize=11):
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx)
        if sub:
            self.text(x + w / 2, y + h / 2 - 2, label, size=size, anchor="middle", bold=bold, fill=fill_text)
            self.text(x + w / 2, y + h / 2 + subsize + 1, sub, size=subsize, anchor="middle", fill=GRAY)
        else:
            self.text(x + w / 2, y + h / 2 + size * 0.36, label, size=size, anchor="middle", bold=bold, fill=fill_text)

    def bracket(self, x1, x2, y, label=None, up=False, size=11, fill=GRAY, tick=5):
        t = -tick if up else tick
        self.path(f"M{x1:.1f},{y + t:.1f} L{x1:.1f},{y:.1f} L{x2:.1f},{y:.1f} L{x2:.1f},{y + t:.1f}", stroke=fill, sw=1)
        if label:
            ly = y - 5 if up else y + tick + size + 2
            self.text((x1 + x2) / 2, ly, label, size=size, anchor="middle", fill=fill)

    def save(self, name):
        os.makedirs(OUT, exist_ok=True)
        body = "\n".join(self.el)
        t = f"<title>{escape(self.title)}</title>\n" if self.title else ""
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
               f'viewBox="0 0 {self.w} {self.h}" role="img">\n{t}'
               f'<rect width="100%" height="100%" fill="#fff"/>\n{body}\n</svg>\n')
        with open(os.path.join(OUT, name), "w") as f:
            f.write(svg)
        return name
