import math
from figlib import *

class Net:
    def __init__(self, s): self.s = s; self.n = {}
    def node(self, key, x, y, label, fill="#fff", w=None, h=28, size=12.5, bold=True, sub=None, stroke=INK, rx=4):
        if w is None: w = max(tw(label, size, bold), tw(sub or "", 10.5)) * 1.14 + 22
        if sub:
            h = max(h, 38)
        self.s.rect(x - w / 2, y - h / 2, w, h, fill=fill, stroke=stroke, rx=rx)
        if sub:
            self.s.text(x, y - 2, label, size=size, anchor="middle", bold=bold)
            self.s.text(x, y + 12, sub, size=10.5, anchor="middle", fill=GRAY)
        else:
            self.s.text(x, y + size * 0.36, label, size=size, anchor="middle", bold=bold)
        self.n[key] = (x, y, w, h)
    def edge_pt(self, key, tx, ty, pad=3):
        """Point on the node's border toward (tx,ty)."""
        x, y, w, h = self.n[key]
        dx, dy = tx - x, ty - y
        if dx == 0 and dy == 0: return x, y
        sx = (w / 2 + pad) / abs(dx) if dx else 1e9
        sy = (h / 2 + pad) / abs(dy) if dy else 1e9
        t = min(sx, sy)
        return x + dx * t, y + dy * t
    def link(self, a, b, kind="act", stroke=INK, sw=1.4, dash=None, label=None, lx=0, ly=0, lsize=10.5, lanchor="start", lfill=GRAY, off=(0, 0, 0, 0)):
        xa, ya = self.n[a][:2]; xb, yb = self.n[b][:2]
        xa += off[0]; ya += off[1]; xb += off[2]; yb += off[3]
        p1 = self.edge_pt(a, xb, yb, 2)
        p2 = self.edge_pt(b, xa, ya, 3 if kind == "act" else 4)
        p1 = (p1[0] + off[0], p1[1] + off[1]) if off[0] or off[1] else p1
        p2 = (p2[0] + off[2], p2[1] + off[3]) if off[2] or off[3] else p2
        self.s.arrow(p1[0], p1[1], p2[0], p2[1], stroke=stroke, sw=sw, kind=kind, dash=dash)
        if label:
            mx, my = (p1[0] + p2[0]) / 2 + lx, (p1[1] + p2[1]) / 2 + ly
            self.s.text(mx, my, label, size=lsize, anchor=lanchor, fill=lfill)

def membrane(s, y, x1=16, x2=704, label="plasma membrane"):
    s.rect(x1, y - 7, x2 - x1, 14, fill=GRAY_T, stroke="none")
    s.line(x1, y - 7, x2, y - 7, stroke=LIGHT); s.line(x1, y + 7, x2, y + 7, stroke=LIGHT)
    s.text(x2 - 4, y + 4, label, size=10, anchor="end", fill=GRAY, italic=True)

def legend(s, x, y):
    s.arrow(x, y, x + 26, y, sw=1.4); s.text(x + 32, y + 4, "activates", size=10.5, fill=GRAY)
    s.arrow(x + 100, y, x + 126, y, sw=1.4, kind="inh"); s.text(x + 134, y + 4, "inhibits", size=10.5, fill=GRAY)
    s.text(x + 196, y + 4, "red = cancer mutation", size=10.5, fill=RED)
    s.text(x + 330, y + 4, "gray bar = drug", size=10.5, fill=GRAY)

def drug(s, net, key, name, side="left", dy=0):
    x, y, w, h = net.n[key]
    if side == "left":
        x0 = x - w / 2 - 70
        s.arrow(x0, y + dy, x - w / 2 - 4, y + dy, stroke=GRAY, kind="inh", sw=1.4)
        s.text(x0 - 4, y + dy + 4, name, size=10.5, anchor="end", fill=GRAY, italic=True)
    else:
        x0 = x + w / 2 + 70
        s.arrow(x0, y + dy, x + w / 2 + 4, y + dy, stroke=GRAY, kind="inh", sw=1.4)
        s.text(x0 + 4, y + dy + 4, name, size=10.5, fill=GRAY, italic=True)

def mut(s, net, key, text, dx=10, dy=4):
    x, y, w, h = net.n[key]
    s.text(x + w / 2 + dx, y + dy, text, size=10.5, fill=RED, bold=True)

# ---------------------------------------------------------------------------
def mapk():
    s = SVG(720, 548, "RTK–RAS–MAPK signaling")
    net = Net(s)
    cx = 372
    s.text(16, 22, "RTK → RAS → MAPK: growth-factor signal to proliferation", size=13, bold=True)
    membrane(s, 92)
    # ligand + receptor dimer
    for dx in (-16, 16):
        s.rect(cx + dx - 9, 52, 18, 72, fill=BLUE_T, stroke=INK, rx=3)
    s.circle(cx, 46, 9, fill=GREEN_T); s.text(cx, 50, "", size=1)
    s.text(cx + 14, 44, "EGF", size=11, bold=True, fill=GREEN)
    for dx, yy in [(-30, 112), (30, 112)]:
        s.circle(cx + dx, yy, 7, fill="#fff", stroke=INK)
        s.text(cx + dx, yy + 3.5, "P", size=9, anchor="middle", bold=True)
    net.n["EGFR"] = (cx, 88, 50, 72)
    s.text(cx - 44, 70, "EGFR (an RTK), dimerized", size=11, anchor="end", bold=True)
    s.text(cx - 44, 84, "and autophosphorylated", size=10.5, anchor="end", fill=GRAY)
    net.node("GRB2", cx - 50, 160, "GRB2", sub="adaptor (SH2)")
    net.node("SOS", cx + 60, 160, "SOS", sub="GEF")
    s.line(cx - 30, 119, cx - 50, 141, stroke=INK, sw=1.4)
    s.line(cx - 50 + 32, 160, cx + 60 - 26, 160, stroke=INK, sw=1.4)
    net.node("RASd", cx - 80, 236, "RAS·GDP", sub="off", fill="#fff")
    net.node("RASt", cx + 80, 236, "RAS·GTP", sub="on", fill=BLUE_T)
    s.curve_arrow([(cx - 40, 224), (cx, 204), (cx + 38, 224)], sw=1.4)
    s.curve_arrow([(cx + 38, 250), (cx, 270), (cx - 40, 250)], sw=1.4)
    s.arrow(cx + 60, 180, cx + 4, 210, sw=1.2, stroke=INK)
    net.node("NF1", cx - 10, 296, "NF1", sub="GAP")
    s.arrow(cx - 10, 277, cx - 6, 264, sw=1.2)
    net.node("RAF", cx + 80, 330, "RAF", sub="ARAF, BRAF, CRAF", fill=BLUE_T)
    net.node("MEK", cx + 80, 388, "MEK1/2", fill=BLUE_T)
    net.node("ERK", cx + 80, 440, "ERK1/2", sub="MAPK3 / MAPK1", fill=BLUE_T)
    net.link("RASt", "RAF"); net.link("RAF", "MEK", label="P", lx=6, ly=4, lfill=INK); net.link("MEK", "ERK", label="P", lx=6, ly=4, lfill=INK)
    # nucleus
    s.path("M16,470 L704,470", stroke=LIGHT, dash="5,4")
    s.text(704, 466, "nucleus below", size=10, anchor="end", fill=GRAY, italic=True)
    net.node("TF", cx + 80, 496, "FOS, MYC … growth genes ON", fill=GREEN_T, size=12)
    net.link("ERK", "TF")
    # mutations
    mut(s, net, "EGFR", "", 0)
    s.text(cx + 44, 70, "EGFR L858R, exon 19 del.", size=10.5, fill=RED, bold=True)
    mut(s, net, "RASt", "KRAS G12 / G13 / Q61: stuck on")
    mut(s, net, "RAF", "BRAF V600E: always active")
    s.text(cx - 10 - 34, 300, "NF1 loss: brake removed", size=10.5, fill=RED, bold=True, anchor="end")
    # drugs
    drug(s, net, "RAF", "vemurafenib, dabrafenib", side="left")
    drug(s, net, "MEK", "trametinib", side="left")
    drug(s, net, "RASd", "sotorasib (KRAS G12C):", side="left", dy=-4)
    s.text(cx - 80 - 52 - 74, 248, "locks it in the off form", size=10.5, anchor="end", fill=GRAY, italic=True)
    s.arrow(cx - 44 - 70 - 30, 104, cx - 26, 104, stroke=GRAY, kind="inh", sw=1.4)
    s.text(cx - 44 - 70 - 34, 108, "osimertinib", size=10.5, anchor="end", fill=GRAY, italic=True)
    s.text(cx - 6, 196, "loads GTP", size=10, fill=GRAY, anchor="end")
    s.text(cx + 4, 284, "", size=1)
    legend(s, 16, 536)
    s.save("u5-mapk.svg")

# ---------------------------------------------------------------------------
def pi3k():
    s = SVG(720, 590, "PI3K–AKT–mTOR signaling")
    net = Net(s)
    s.text(16, 22, "PI3K → AKT → mTOR: growth and survival", size=13, bold=True)
    membrane(s, 78)
    # RTK
    for dx in (-12, 12):
        s.rect(110 + dx - 8, 44, 16, 66, fill=BLUE_T, stroke=INK, rx=3)
    s.text(110, 38, "RTK", size=11.5, anchor="middle", bold=True)
    net.n["RTK"] = (110, 77, 40, 66)
    net.node("PI3K", 210, 150, "PI3K", sub="p110α = PIK3CA", fill=BLUE_T)
    net.link("RTK", "PI3K")
    # lipids in membrane
    for x, lab in [(320, "PIP2"), (480, "PIP3")]:
        s.raw(f'<ellipse cx="{x}" cy="78" rx="28" ry="11" fill="#fff" stroke="{INK}"/>')
        s.text(x, 82, lab, size=11.5, anchor="middle", bold=True)
    net.n["PIP3"] = (480, 78, 56, 22)
    s.curve_arrow([(346, 70), (400, 42), (454, 70)], sw=1.4)
    s.curve_arrow([(454, 88), (400, 116), (346, 88)], sw=1.4)
    s.arrow(250, 140, 396, 52, sw=1.2)
    s.text(400, 36, "adds a phosphate", size=10, anchor="middle", fill=GRAY)
    net.node("PTEN", 400, 160, "PTEN", sub="lipid phosphatase", fill="#fff")
    s.arrow(400, 140, 400, 108, sw=1.2)
    s.text(400, 196, "PTEN loss", size=10.5, fill=RED, bold=True, anchor="middle")
    s.text(210 - 60, 196, "PIK3CA E545K, H1047R", size=10.5, fill=RED, bold=True, anchor="start")
    net.node("AKT", 540, 230, "AKT", sub="recruited by PIP3", fill=BLUE_T)
    net.link("PIP3", "AKT")
    net.node("PDK1", 380, 250, "PDK1", size=12)
    net.node("mTORC2", 680 - 20, 250, "mTORC2", size=12)
    net.link("PDK1", "AKT", label="T308", lx=-14, ly=-6, lfill=INK)
    net.link("mTORC2", "AKT", label="S473", lx=-8, ly=-8, lfill=INK)
    s.text(540 + 52, 214, "", size=1)
    net.node("SURV", 360, 316, "cell survival", fill=GREEN_T, size=11.5, bold=False)
    net.link("AKT", "SURV")
    net.node("TSC", 540, 316, "TSC1/TSC2", sub="GAP for RHEB")
    net.link("AKT", "TSC", kind="inh")
    net.node("RHEB", 540, 384, "RHEB·GTP", fill=BLUE_T)
    net.link("TSC", "RHEB", kind="inh")
    net.node("mTORC1", 540, 446, "mTORC1", fill=BLUE_T)
    net.link("RHEB", "mTORC1")
    net.node("AMPK", 380, 446, "AMPK", sub="low energy")
    net.link("AMPK", "mTORC1", kind="inh")
    drug(s, net, "mTORC1", "rapamycin", side="right")
    net.node("S6K", 460, 506, "S6K")
    net.node("4EBP", 620, 506, "4E-BP1")
    net.link("mTORC1", "S6K")
    net.link("mTORC1", "4EBP", kind="inh")
    s.text(540, 540, "", size=1)
    s.text(258, 510, "", size=1)
    net.node("PS", 300, 506, "protein synthesis, cell growth", fill=GREEN_T, size=11.5, bold=False)
    net.link("S6K", "PS")
    s.curve_arrow([(620, 520), (470, 572), (300, 522)], kind="inh", sw=1.2, stroke=INK)
    s.text(16, 548, "", size=1)
    legend(s, 16, 578)
    s.save("u5-pi3k.svg")

# ---------------------------------------------------------------------------
def p53():
    s = SVG(720, 400, "The p53 DNA-damage response and the MDM2 feedback loop")
    net = Net(s)
    s.text(16, 22, "p53: DNA damage → p53 → arrest or death, with MDM2 feedback", size=13, bold=True)
    # kinase group
    s.rect(16, 40, 330, 120, fill="#fafafa", stroke=LIGHT, rx=6, dash="4,3")
    net.node("DSB", 90, 72, "double-strand break", size=11, bold=False, w=136)
    net.node("ATM", 200, 72, "ATM", w=50); net.node("CHK2", 290, 72, "CHK2", w=60)
    net.node("SS", 90, 128, "ssDNA, stalled", size=11, bold=False, w=136, sub="replication")
    net.node("ATR", 200, 128, "ATR", w=50); net.node("CHK1", 290, 128, "CHK1", w=60)
    for a, b in [("DSB", "ATM"), ("ATM", "CHK2"), ("SS", "ATR"), ("ATR", "CHK1")]: net.link(a, b)
    s.text(180, 176, "sensor and checkpoint kinases (ATM, ATR, CHK1, CHK2)", size=10.5, anchor="middle", fill=GRAY)
    net.node("P53", 470, 100, "p53", sub="transcription factor", fill=BLUE_T, w=150, h=44, size=15)
    s.arrow(348, 100, 392, 100, sw=1.6)
    s.text(370, 88, "P", size=11, anchor="middle", bold=True)
    s.text(16, 196, "These kinases phosphorylate p53 (e.g. Ser15). Phosphorylated", size=10.5, fill=GRAY)
    s.text(16, 210, "p53 escapes MDM2, so p53 protein builds up.", size=10.5, fill=GRAY)
    net.node("MDM2", 470, 250, "MDM2", sub="E3 ubiquitin ligase", fill="#fff", w=150)
    # MDM2 -| p53 (left), p53 -> MDM2 gene (right)
    s.arrow(440, 230, 440, 124, kind="inh", sw=1.6)
    s.text(432, 170, "ubiquitinates p53", size=10.5, anchor="end", fill=INK)
    s.text(432, 183, "→ proteasome", size=10.5, anchor="end", fill=GRAY)
    s.arrow(500, 124, 500, 230, sw=1.6)
    s.text(508, 170, "induces the", size=10.5, fill=INK)
    s.text(508, 183, "MDM2 gene", size=10.5, fill=INK)
    s.text(470, 290, "negative feedback loop", size=10.5, anchor="middle", fill=GRAY, italic=True)
    # phospho blocks binding
    # targets
    net.node("P21", 640, 64, "p21", sub="CDKN1A", w=96)
    net.node("BAX", 640, 160, "BAX, PUMA, NOXA", size=11.5, w=130)
    s.arrow(546, 92, 590, 70, sw=1.4); s.arrow(546, 110, 574, 150, sw=1.4)
    s.text(640, 104, "CDKs off: cell-cycle", size=10.5, anchor="middle", fill=GREEN)
    s.text(640, 117, "pause or senescence", size=10.5, anchor="middle", fill=GREEN)
    s.text(640, 192, "apoptosis", size=10.5, anchor="middle", fill=GREEN)
    s.text(556, 66, "", size=1)
    # cancer
    s.text(16, 320, "In cancer:", size=11.5, bold=True)
    s.text(16, 338, "TP53 missense hotspots (R175, R248, R273) in the DNA-binding domain stop p53 from switching on its targets.", size=11, fill=RED)
    s.text(16, 354, "MDM2 amplification destroys p53 faster. Inherited TP53 mutation = Li-Fraumeni syndrome.", size=11, fill=RED)
    legend_simple(s, 16, 384)
    s.save("u5-p53.svg")

def legend_simple(s, x, y):
    s.arrow(x, y, x + 26, y, sw=1.4); s.text(x + 32, y + 4, "activates / induces", size=10.5, fill=GRAY)
    s.arrow(x + 150, y, x + 176, y, sw=1.4, kind="inh"); s.text(x + 184, y + 4, "inhibits / degrades", size=10.5, fill=GRAY)

# ---------------------------------------------------------------------------
def cell_cycle():
    s = SVG(720, 400, "The cell cycle, its cyclin–CDK drivers and checkpoints")
    s.text(16, 22, "The cell cycle: G1 → S → G2 → M", size=13, bold=True)
    cx, cy, R, T = 210, 210, 128, 34
    phases = [("G1", 0.42, "growth", GREEN_T), ("S", 0.30, "DNA copied", BLUE_T), ("G2", 0.18, "prepare", GREEN_T), ("M", 0.10, "mitosis", RED_T)]
    def pt(a, r):  # a in fractions of a turn, clockwise from 12 o'clock
        th = 2 * math.pi * a - math.pi / 2
        return cx + r * math.cos(th), cy + r * math.sin(th)
    a0 = 0
    bounds = []
    for name, f, sub, fill in phases:
        a1 = a0 + f
        r1, r2 = R - T / 2, R + T / 2
        p1 = pt(a0, r2); p2 = pt(a1, r2); p3 = pt(a1, r1); p4 = pt(a0, r1)
        large = 1 if f > 0.5 else 0
        d = (f"M{p1[0]:.1f},{p1[1]:.1f} A{r2},{r2} 0 {large} 1 {p2[0]:.1f},{p2[1]:.1f} "
             f"L{p3[0]:.1f},{p3[1]:.1f} A{r1},{r1} 0 {large} 0 {p4[0]:.1f},{p4[1]:.1f} Z")
        s.path(d, fill=fill, stroke=INK)
        m = pt((a0 + a1) / 2, R)
        s.text(m[0], m[1] + 5, name, size=14, anchor="middle", bold=True)
        mi = pt((a0 + a1) / 2, R - T / 2 - 16)
        s.text(mi[0], mi[1] + 4, sub, size=10.5, anchor="middle", fill=GRAY)
        bounds.append(a1)
        a0 = a1
    # clockwise arrow inside
    rr = R - T / 2 - 44
    pts = [pt(t / 100 * 0.85 + 0.05, rr) for t in range(0, 101)]
    s.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts[:-3]), stroke=LIGHT, sw=1.2)
    e = pts[-1]; b = pts[-4]
    s.arrow(b[0], b[1], e[0], e[1], stroke=LIGHT, sw=1.2, head=7)
    # checkpoints: bars across ring
    def bar(a, label, dx, dy, anchor="start"):
        po = pt(a, R + T / 2 + 6); pi_ = pt(a, R - T / 2 - 6)
        s.line(po[0], po[1], pi_[0], pi_[1], stroke=RED, sw=3)
        lp = pt(a, R + T / 2 + 14)
        s.text(lp[0] + dx, lp[1] + dy, label, size=10.5, anchor=anchor, fill=RED, bold=True)
    bar(0.42, "G1/S checkpoint", 0, 12, "end")
    bar(0.90, "G2/M checkpoint", -4, 0, "end")
    bar(0.978, "spindle checkpoint", 4, -6, "start")
    # restriction point
    rp = 0.33
    po = pt(rp, R + T / 2 + 4); pi_ = pt(rp, R - T / 2 - 4)
    s.line(po[0], po[1], pi_[0], pi_[1], stroke=INK, sw=1.5, dash="3,2")
    lp = pt(rp, R - T / 2 - 12)
    s.text(lp[0] - 2, lp[1] - 2, "restriction", size=10.5, fill=INK, anchor="end")
    s.text(lp[0] - 2, lp[1] + 11, "point", size=10.5, fill=INK, anchor="end")
    # G0
    g = pt(0.12, R + T / 2 + 54)
    s.circle(g[0], g[1], 20, fill="#fff", stroke=INK)
    s.text(g[0], g[1] + 5, "G0", size=13, anchor="middle", bold=True)
    s.text(g[0], g[1] + 34, "resting", size=10.5, anchor="middle", fill=GRAY)
    a1 = pt(0.08, R + T / 2 + 4); a2 = pt(0.11, R + T / 2 + 32)
    s.line(a1[0], a1[1], a2[0], a2[1], stroke=GRAY)
    # right panel: drivers
    x = 420
    s.text(x, 50, "Cyclin–CDK pairs that drive each step", size=12, bold=True)
    rows = [("G1", "cyclin D – CDK4/6"), ("G1/S", "cyclin E – CDK2"), ("S", "cyclin A – CDK2"), ("G2/M", "cyclin B – CDK1")]
    for i, (ph, pair) in enumerate(rows):
        s.text(x, 72 + i * 18, ph, size=11.5, bold=True)
        s.text(x + 48, 72 + i * 18, pair, size=11.5)
    # RB-E2F mini pathway
    y = 172
    s.text(x, y, "Commitment in G1", size=12, bold=True)
    net = Net(s)
    net.node("CDK46", x + 52, y + 30, "CDK4/6", size=11.5, w=74)
    net.node("RB", x + 150, y + 30, "RB", size=11.5, w=44)
    net.node("E2F", x + 232, y + 30, "E2F", size=11.5, w=50)
    net.link("CDK46", "RB", kind="inh"); net.link("RB", "E2F", kind="inh")
    s.text(x + 100, y + 22, "P", size=10, anchor="middle", bold=True)
    s.arrow(x + 258, y + 30, x + 278, y + 30, sw=1.2)
    s.text(x + 232, y + 58, "S-phase genes ON", size=10.5, anchor="middle", fill=GREEN)
    net.node("P16", x + 52, y + 84, "p16 (INK4)", size=11, w=84, bold=False)
    s.arrow(x + 52, y + 70, x + 52, y + 48, kind="inh", sw=1.3)
    s.text(x + 100, y + 88, "palbociclib also blocks CDK4/6", size=10.5, fill=GRAY, italic=True)
    s.text(x, y + 122, "p21 and p27 (CIP/KIP) block CDK2 and CDK1.", size=11)
    s.text(x, y + 142, "Checkpoints (red) halt the cycle: DNA damage", size=11, fill=RED)
    s.text(x, y + 156, "at G1/S and G2/M; unattached chromosomes", size=11, fill=RED)
    s.text(x, y + 170, "at the spindle checkpoint (before anaphase).", size=11, fill=RED)
    s.text(x, y + 196, "Phase lengths are typical, not fixed.", size=10.5, fill=GRAY)
    s.save("u5-cell-cycle.svg")

# ---------------------------------------------------------------------------
def wnt():
    s = SVG(720, 380, "Wnt/β-catenin signaling off and on")
    for k, (title, on) in enumerate([("Wnt OFF", False), ("Wnt ON", True)]):
        ox = k * 360
        net = Net(s)
        if k: s.line(360, 12, 360, 340, stroke=RULE)
        s.text(ox + 16, 22, title, size=13, bold=True)
        s.rect(ox + 16, 52, 328, 14, fill=GRAY_T, stroke="none")
        s.line(ox + 16, 52, ox + 344, 52, stroke=LIGHT); s.line(ox + 16, 66, ox + 344, 66, stroke=LIGHT)
        # receptors
        s.rect(ox + 140, 36, 18, 46, fill=BLUE_T, stroke=INK, rx=3)
        s.rect(ox + 164, 36, 14, 46, fill=GRAY_T, stroke=INK, rx=3)
        s.text(ox + 134, 46, "Frizzled", size=10.5, anchor="end")
        s.text(ox + 184, 46, "LRP5/6", size=10.5)
        if on:
            s.circle(ox + 159, 30, 8, fill=GREEN_T, stroke=INK)
            s.text(ox + 172, 22, "Wnt", size=11, bold=True, fill=GREEN)
        net.node("DC", ox + 110, 132, "destruction complex", sub="APC · AXIN · GSK3β · CK1", w=180, size=11.5)
        if on:
            s.arrow(ox + 159, 84, ox + 140, 110, kind="inh", sw=1.5)
            s.text(ox + 222, 104, "complex blocked", size=10.5, fill=GRAY)
            for j in range(4):
                s.circle(ox + 250 + (j % 2) * 26, 146 + (j // 2) * 24, 11, fill=BLUE_T)
                s.text(ox + 250 + (j % 2) * 26, 150 + (j // 2) * 24, "β", size=11, anchor="middle", bold=True)
            s.text(ox + 263, 196, "β-catenin builds up", size=10.5, anchor="middle")
            s.arrow(ox + 263, 204, ox + 263, 262, sw=1.5)
            s.text(ox + 271, 236, "enters nucleus", size=10.5, fill=GRAY)
        else:
            s.circle(ox + 270, 132, 11, fill=BLUE_T)
            s.text(ox + 270, 136, "β", size=11, anchor="middle", bold=True)
            s.text(ox + 270, 158, "β-catenin", size=10.5, anchor="middle")
            s.arrow(ox + 202, 132, ox + 255, 132, sw=1.4)
            s.text(ox + 228, 124, "P", size=10, anchor="middle", bold=True)
            s.arrow(ox + 270, 168, ox + 270, 206, sw=1.4)
            s.text(ox + 278, 192, "ubiquitin", size=10.5, fill=GRAY)
            net.node("PROT", ox + 270, 222, "proteasome", size=11, bold=False, w=90)
            s.text(ox + 270, 250, "destroyed", size=10.5, anchor="middle", fill=GRAY)
        # nucleus
        s.path(f"M{ox + 16},266 L{ox + 344},266", stroke=LIGHT, dash="5,4")
        s.text(ox + 340, 262, "nucleus", size=10, anchor="end", fill=GRAY, italic=True)
        s.line(ox + 30, 316, ox + 330, 316, stroke=INK, sw=2)
        s.rect(ox + 150, 292, 72, 22, fill=GRAY_T, stroke=INK, rx=3)
        s.text(ox + 186, 307, "TCF/LEF", size=11, anchor="middle", bold=True)
        if on:
            s.circle(ox + 236, 284, 11, fill=BLUE_T)
            s.text(ox + 236, 288, "β", size=11, anchor="middle", bold=True)
            s.text(ox + 186, 336, "MYC, AXIN2, LGR5 ON", size=11.5, anchor="middle", fill=GREEN, bold=True)
        else:
            s.text(ox + 186, 336, "target genes OFF", size=11.5, anchor="middle", fill=GRAY, bold=True)
        s.text(ox + 40, 310, "DNA", size=10, fill=GRAY)
    s.text(16, 368, "In colorectal cancer, APC loss breaks the destruction complex, so β-catenin builds up as if Wnt were always ON.", size=11, fill=RED)
    s.save("u5-wnt.svg")

if __name__ == "__main__":
    mapk(); pi3k(); p53(); cell_cycle(); wnt()
