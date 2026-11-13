import json, math, os, base64, io
from figlib import *
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
def amino_acids():
    groups = [("Hydrophobic", [("A", "Ala", "alanine"), ("V", "Val", "valine"), ("L", "Leu", "leucine"), ("I", "Ile", "isoleucine"), ("M", "Met", "methionine")], GRAY_T),
              ("Aromatic", [("F", "Phe", "phenylalanine"), ("W", "Trp", "tryptophan"), ("Y", "Tyr", "tyrosine")], GRAY_T),
              ("Polar, uncharged", [("S", "Ser", "serine"), ("T", "Thr", "threonine"), ("N", "Asn", "asparagine"), ("Q", "Gln", "glutamine")], GREEN_T),
              ("Positive (basic)", [("K", "Lys", "lysine"), ("R", "Arg", "arginine"), ("H", "His", "histidine")], BLUE_T),
              ("Negative (acidic)", [("D", "Asp", "aspartate"), ("E", "Glu", "glutamate")], RED_T),
              ("Special", [("G", "Gly", "glycine"), ("P", "Pro", "proline"), ("C", "Cys", "cysteine")], "#fff")]
    tricky = set("FYWKRDENQ")
    cw, chh, gap = 108, 44, 8
    x0 = 140
    s = SVG(720, 30 + len(groups) * (chh + gap) + 34, "The 20 amino acids grouped by side-chain chemistry")
    for i, (gname, aas, fill) in enumerate(groups):
        y = 20 + i * (chh + gap)
        s.text(16, y + chh / 2 + 5, gname, size=12.5, bold=True)
        for j, (one, three, name) in enumerate(aas):
            x = x0 + j * (cw + 6)
            s.rect(x, y, cw, chh, fill=fill, stroke=RULE, rx=3)
            s.text(x + 18, y + 30, one, size=24, anchor="middle", bold=True, fill=RED if one in tricky else INK)
            s.text(x + 36, y + 19, three, size=12.5, bold=True)
            s.text(x + 36, y + 34, name, size=10, fill=GRAY)
    y = 30 + len(groups) * (chh + gap) + 8
    s.text(16, y, "Red letters don't match the name's first letter: learn these (F Phe, W Trp, Y Tyr, N Asn, Q Gln, K Lys, R Arg, D Asp, E Glu).", size=11.5, fill=RED)
    s.save("u4-amino-acids.svg")

# ---------------------------------------------------------------------------
def structure_levels():
    s = SVG(720, 300, "Four levels of protein structure")
    W = 180
    heads = ["Primary", "Secondary", "Tertiary", "Quaternary"]
    subs = ["the sequence (N→C)", "local helices and strands", "the 3D fold of one chain", "several chains together"]
    for i, (h, sub) in enumerate(zip(heads, subs)):
        cx = i * W + W / 2
        s.text(cx, 22, h, size=13, bold=True, anchor="middle")
        s.text(cx, 38, sub, size=11, anchor="middle", fill=GRAY)
        if i: s.line(i * W, 12, i * W, 290, stroke=RULE)
    # primary: bead chain zigzag
    seq = "MEEPQSDPSVEP"
    for k, a in enumerate(seq):
        row, col = divmod(k, 4)
        x = 40 + (col if row % 2 == 0 else 3 - col) * 34
        y = 80 + row * 50
        s.circle(x, y, 12, fill=GREEN_T)
        s.text(x, y + 4, a, size=11, anchor="middle", bold=True)
        if k:
            pr, pc = divmod(k - 1, 4)
            px = 40 + (pc if pr % 2 == 0 else 3 - pc) * 34; py = 80 + pr * 50
            dx, dy = x - px, y - py; L = math.hypot(dx, dy)
            s.line(px + dx / L * 12, py + dy / L * 12, x - dx / L * 12, y - dy / L * 12, sw=1.2)
    s.text(28, 78, "", size=1)
    s.text(16, 84, "N", size=11, bold=True, anchor="end", fill=BLUE)
    s.text(142, 214, "… C", size=11, bold=True, fill=BLUE, anchor="middle")
    s.text(90, 276, "p53 begins MEEPQSDPSVEP…", size=10.5, anchor="middle", fill=GRAY)
    # secondary: helix (sine coil) + antiparallel and parallel sheets
    cx = W + 20
    pts = []
    for t in range(0, 121):
        x = cx + 10 + t * 1.15
        y = 82 + 14 * math.sin(t / 120 * 2 * math.pi * 3.6 / 1.0 * 0.83)
        pts.append((x, y))
    s.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), stroke=RED, sw=2.4)
    s.text(W + 90, 116, "α-helix: 3.6 residues per turn,", size=10.5, anchor="middle", fill=GRAY)
    s.text(W + 90, 129, "H-bond from residue i to i+4", size=10.5, anchor="middle", fill=GRAY)
    def strand(x1, x2, y, color=BLUE):
        s.rect(min(x1, x2) if x1 < x2 else x2 + 10, y - 5, abs(x2 - x1) - 10, 10, fill=color, stroke="none")
        if x2 > x1:
            s.poly([(x2, y), (x2 - 12, y - 10), (x2 - 12, y + 10)], fill=color)
        else:
            s.poly([(x2, y), (x2 + 12, y - 10), (x2 + 12, y + 10)], fill=color)
    strand(W + 20, W + 100, 160); strand(W + 100, W + 20, 184)
    for k in range(4):
        s.line(W + 34 + k * 18, 166, W + 34 + k * 18, 178, stroke=GRAY, dash="2,2")
    s.text(W + 140, 176, "anti-", size=10.5, anchor="middle", fill=GRAY); s.text(W + 140, 189, "parallel", size=10.5, anchor="middle", fill=GRAY)
    strand(W + 20, W + 100, 222); strand(W + 20, W + 100, 246)
    for k in range(4):
        s.line(W + 34 + k * 18, 228, W + 34 + k * 18, 240, stroke=GRAY, dash="2,2")
    s.text(W + 140, 238, "parallel", size=10.5, anchor="middle", fill=GRAY)
    s.text(W + 90, 276, "β-strands pair into β-sheets", size=10.5, anchor="middle", fill=GRAY)
    # tertiary: cartoon fold: helix + 3 strands + loops
    ox = 2 * W
    s.path(f"M{ox + 30},{80} C{ox + 10},{120} {ox + 60},{130} {ox + 40},{160}", stroke=GRAY, sw=1.5)
    hx = [(ox + 40, 160)]
    s.path(f"M{ox + 40},160 " + " ".join(f"L{ox + 40 + t * 1.0:.1f},{160 + 9 * math.sin(t / 9):.1f}" for t in range(0, 90)), stroke=RED, sw=2.4)
    s.path(f"M{ox + 130},160 C{ox + 170},170 {ox + 160},220 {ox + 130},226", stroke=GRAY, sw=1.5)
    strand(ox + 130, ox + 50, 226); 
    s.path(f"M{ox + 50},226 C{ox + 20},236 {ox + 20},250 {ox + 50},252", stroke=GRAY, sw=1.5)
    strand(ox + 50, ox + 130, 252)
    s.path(f"M{ox + 130},252 C{ox + 165},90 {ox + 140},80 {ox + 120},96", stroke=GRAY, sw=1.5)
    strand(ox + 120, ox + 60, 100)
    s.text(ox + 26, 76, "N", size=11, bold=True, fill=BLUE, anchor="middle")
    s.text(ox + 52, 104, "C", size=11, bold=True, fill=BLUE, anchor="end")
    s.text(ox + 90, 276, "hydrophobic side chains buried", size=10.5, anchor="middle", fill=GRAY)
    # quaternary: hemoglobin a2b2
    qx = 3 * W + 90
    blobs = [(-34, -30, "α1", GREEN_T), (34, -30, "β1", BLUE_T), (-34, 34, "β2", BLUE_T), (34, 34, "α2", GREEN_T)]
    for dx, dy, lab, f in blobs:
        s.raw(f'<ellipse cx="{qx + dx}" cy="{165 + dy}" rx="33" ry="30" fill="{f}" stroke="{INK}" stroke-width="1"/>')
        s.text(qx + dx, 170 + dy, lab, size=13, anchor="middle", bold=True)
    s.text(qx, 262, "hemoglobin: 2 α + 2 β chains", size=10.5, anchor="middle", fill=GRAY)
    s.text(qx, 276, "(α2β2 tetramer)", size=10.5, anchor="middle", fill=GRAY)
    s.save("u4-structure-levels.svg")

# ---------------------------------------------------------------------------
def domains():
    s = SVG(720, 350, "Domain architecture of EGFR and p53 (UniProt / Pfam coordinates)")
    def protein(y, L, x0, x1, feats, ticks, name, sub):
        sc = (x1 - x0) / L
        X = lambda r: x0 + (r - 1) * sc
        s.text(16, y - 46, name, size=13, bold=True)
        s.text(16 + tw(name, 13, True) * 1.12 + 8, y - 46, sub, size=11, fill=GRAY)
        s.line(X(1), y, X(L), y, sw=2)
        for (a, b, lab, fill, h, row) in feats:
            s.rect(X(a), y - h / 2, (b - a + 1) * sc, h, fill=fill, stroke=INK, rx=2)
            if lab:
                ly = y + h / 2 + 14 + row * 14 if row >= 0 else y - h / 2 - 6
                s.text((X(a) + X(b)) / 2, ly, lab, size=10.5, anchor="middle")
        for t in ticks:
            s.line(X(t), y + 30 + 18, X(t), y + 34 + 18, stroke=GRAY)
            s.text(X(t), y + 46 + 18, str(t), size=9.5, anchor="middle", fill=GRAY)
        s.line(X(1), y + 30 + 18, X(L), y + 30 + 18, stroke=LIGHT)
        return X
    feats = [(1, 24, "", RED_T, 12, 0),
             (57, 167, "L", BLUE_T, 20, 0), (185, 338, "CR (furin-like)", GRAY_T, 20, 0),
             (361, 480, "L", BLUE_T, 20, 0), (505, 636, "GF receptor IV", GRAY_T, 20, 0),
             (646, 668, "", INK, 26, 0), (712, 979, "protein kinase domain", GREEN_T, 20, 0)]
    X = protein(102, 1210, 40, 690, feats, [1, 200, 400, 600, 800, 1000, 1210], "EGFR", "UniProt P00533, 1,210 aa (a receptor tyrosine kinase)")
    s.text(X(12), 128, "signal", size=10, anchor="middle", fill=RED)
    s.text(X(12), 139, "peptide", size=10, anchor="middle", fill=RED)
    s.text(X(657), 80, "TM", size=10.5, anchor="middle", bold=True)
    # membrane band
    s.rect(X(646) - 4, 58, X(668) - X(646) + 8, 4, fill="none", stroke="none")
    s.text((X(25) + X(645)) / 2, 80, "outside the cell (ligand-binding)", size=10.5, anchor="middle", fill=GRAY)
    s.text((X(669) + X(1210)) / 2, 80, "inside the cell", size=10.5, anchor="middle", fill=GRAY)
    s.line(X(858), 114, X(858), 122, stroke=RED, sw=1.5); 
    s.text(X(858), 74, "", size=1)
    s.text(X(858) + 4, 135, "L858R", size=10, fill=RED, bold=True)

    feats = [(1, 44, "TAD", GRAY_T, 16, 0), (64, 92, "Pro-rich", GRAY_T, 12, 1),
             (102, 292, "DNA-binding domain", BLUE_T, 20, 0), (325, 356, "tet.", GRAY_T, 16, 0), (368, 387, "basic", GRAY_T, 12, 0)]
    X = protein(262, 393, 40, 690, feats, [1, 100, 200, 300, 393], "p53", "UniProt P04637, 393 aa (a transcription factor)")
    for r in (175, 248, 273):
        s.line(X(r), 250, X(r), 242, stroke=RED, sw=1.5)
        s.text(X(r), 236, f"R{r}", size=10, anchor="middle", fill=RED, bold=True)
    for a, b in [(50, 96), (282, 325), (351, 393)]:
        s.line(X(a), 248, X(b), 248, stroke=RED, sw=1, dash="3,2")
    s.text(X(351) - 6, 280, "", size=1)
    s.text(16, 342, "Drawn to scale within each protein. TM = transmembrane helix; TAD = transactivation; tet. = tetramerization; dashes = disordered (UniProt).", size=10.5, fill=GRAY)
    s.save("u4-domains.svg")

# ---------------------------------------------------------------------------
AFCOL = [(90, "#0053D6", "very high (>90)"), (70, "#65CBF3", "confident (70–90)"), (50, "#FFDB13", "low (50–70)"), (0, "#FF7D45", "very low (<50)")]
def afcol(p):
    for t, c, _ in AFCOL:
        if p > t: return c
    return AFCOL[-1][1]

def alphafold_p53():
    import numpy as np
    from PIL import Image
    d = json.load(open(os.path.join(HERE, "data", "af-p04637-ca.json")))
    ca = np.array(d["ca"]); pl = np.array(d["plddt"]); n = len(pl)
    s = SVG(720, 470, "AlphaFold model of human p53 (AF-P04637-F1), coloured by pLDDT, with its PAE matrix")
    # --- 3D trace: orient by PCA of the confident core so it fills the panel
    c = ca - ca.mean(0)
    u, sv, vt = np.linalg.svd(c - c.mean(0), full_matrices=False)
    R = vt
    p = c @ R.T
    xs, ys, zs = p[:, 0], p[:, 1], p[:, 2]
    W0, H0, ox, oy = 330, 300, 14, 46
    sc = min(W0 / (xs.max() - xs.min()), H0 / (ys.max() - ys.min()))
    X = ox + (xs - xs.min()) * sc + (W0 - (xs.max() - xs.min()) * sc) / 2
    Y = oy + (ys - ys.min()) * sc + (H0 - (ys.max() - ys.min()) * sc) / 2
    order = sorted(range(n - 1), key=lambda i: (zs[i] + zs[i + 1]))
    s.text(16, 22, "Predicted structure, coloured by pLDDT", size=13, bold=True)
    for i in order:
        z = (zs[i] + zs[i + 1]) / 2
        w = 2.2 + 2.2 * (z - zs.min()) / (zs.max() - zs.min())
        s.line(X[i], Y[i], X[i + 1], Y[i + 1], stroke="#fff", sw=w + 2.2)
        s.raw(f'<line x1="{X[i]:.1f}" y1="{Y[i]:.1f}" x2="{X[i+1]:.1f}" y2="{Y[i+1]:.1f}" stroke="{afcol(min(pl[i], pl[i+1]))}" stroke-width="{w:.1f}" stroke-linecap="round"/>')
    for idx, lab in [(0, "N"), (n - 1, "C")]:
        s.text(X[idx] + 6, Y[idx] - 6, lab, size=12, bold=True)
    # --- pLDDT per residue
    px0, px1, py0, py1 = 400, 700, 60, 150
    s.text(400, 22, "pLDDT per residue", size=13, bold=True)
    s.rect(px0, py0, px1 - px0, py1 - py0, stroke=RULE)
    for t in (50, 70, 90):
        yy = py1 - (t / 100) * (py1 - py0)
        s.line(px0, yy, px1, yy, stroke=RULE, dash="2,2")
        s.text(px0 - 4, yy + 3, str(t), size=9.5, anchor="end", fill=GRAY)
    xr = lambda r: px0 + (r - 1) / (n - 1) * (px1 - px0)
    for i in range(n - 1):
        s.line(xr(i + 1), py1 - pl[i] / 100 * (py1 - py0), xr(i + 2), py1 - pl[i + 1] / 100 * (py1 - py0), stroke=afcol(pl[i]), sw=1.6)
    # domain bar
    yb = py1 + 12
    s.line(px0, yb, px1, yb, stroke=GRAY)
    for a, b, lab in [(102, 292, "DNA-binding domain"), (325, 356, "tet.")]:
        s.rect(xr(a), yb - 5, xr(b) - xr(a), 10, fill=BLUE_T)
        s.text((xr(a) + xr(b)) / 2, yb + 18, lab, size=10, anchor="middle", fill=GRAY)
    for t in (1, 100, 200, 300, 393):
        s.text(xr(t), py0 - 5, str(t), size=9.5, anchor="middle", fill=GRAY)
    # legend
    ly = 212
    for k, (t, col, lab) in enumerate(AFCOL):
        xx = 400 + (k % 2) * 150; yy = ly + (k // 2) * 16
        s.rect(xx, yy - 9, 12, 10, fill=col, stroke="none")
        s.text(xx + 17, yy, lab, size=10.5)
    # --- PAE heatmap (embedded PNG; green-to-white as in AlphaFold DB)
    pae = np.asarray(Image.open(os.path.join(HERE, "data", "af-p04637-pae-x8.png")), dtype=float) / 8.0
    v = np.clip(pae / 30.0, 0, 1)[..., None]
    dark = np.array([15, 81, 34], float); light = np.array([255, 255, 255], float)
    rgb = (dark * (1 - v) + light * v).astype("uint8")
    im = Image.fromarray(rgb).resize((150, 150), Image.BILINEAR)
    buf = io.BytesIO(); im.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    hx, hy = 480, 268
    s.text(400, hy - 0, "", size=1)
    s.text(400, hy + 2, "PAE (Å)", size=12, bold=True)
    s.raw(f'<image x="{hx}" y="{hy - 8}" width="150" height="150" href="data:image/png;base64,{b64}"/>')
    s.rect(hx, hy - 8, 150, 150, stroke=RULE)
    s.text(hx - 4, hy + 2, "1", size=9, anchor="end", fill=GRAY); s.text(hx - 4, hy + 142, "393", size=9, anchor="end", fill=GRAY)
    s.text(hx + 75, hy + 156, "scored residue", size=10, anchor="middle", fill=GRAY)
    s.text(hx - 22, hy + 70, "aligned residue", size=10, anchor="middle", fill=GRAY, rotate=-90)
    # colour bar
    for k in range(30):
        vv = k / 29
        col = tuple(int(dark[j] * (1 - vv) + light[j] * vv) for j in range(3))
        s.rect(hx + 162, hy - 8 + k * 5, 10, 5, fill="#%02x%02x%02x" % col, stroke="none")
    s.rect(hx + 162, hy - 8, 10, 150, stroke=RULE)
    s.text(hx + 176, hy, "0", size=9.5, fill=GRAY); s.text(hx + 176, hy + 142, "30", size=9.5, fill=GRAY)
    s.text(hx + 75, hy + 170, "", size=1)
    # pointer to DBD block on the diagonal
    a = hx + (102 / 393) * 150; b = hx + (292 / 393) * 150
    s.rect(a, hy - 8 + (102 / 393) * 150, b - a, b - a, stroke=BLUE, sw=1.2, dash="3,2")
    s.text(16, 442, "N-terminal and C-terminal tails: low pLDDT (disordered). The DNA-binding domain: high pLDDT and a dark, low-error PAE block.", size=10.5, fill=GRAY)
    s.text(16, 458, "Source: AlphaFold DB AF-P04637-F1 (v6), CC-BY 4.0.", size=10.5, fill=GRAY)
    s.save("u4-alphafold-p53.svg")

# ---------------------------------------------------------------------------
def msa():
    seqs = [("human", "MKVLAEGTRDLW"), ("mouse", "MKVLSEGTRDLW"), ("chicken", "MRVLAEGSKELW"),
            ("frog", "MKILAEGSKELF"), ("fish", "MRVIGEGTRDVW"), ("fly", "MKVLSEGSKEIW")]
    s = SVG(720, 250, "A multiple sequence alignment: conservation and coevolution")
    s.text(16, 22, "Multiple sequence alignment (illustrative)", size=13, bold=True)
    cw = 22; x0 = 110; y0 = 56
    cons = 6  # G column
    co = (7, 8)  # T/S with R/K
    for j in range(12):
        s.text(x0 + j * cw + cw / 2, y0 - 12, str(j + 1), size=9.5, anchor="middle", fill=GRAY)
    s.rect(x0 + cons * cw, y0 - 6, cw, len(seqs) * 22 + 4, fill=GREEN_T, stroke="none")
    for c in co:
        s.rect(x0 + c * cw, y0 - 6, cw, len(seqs) * 22 + 4, fill=BLUE_T, stroke="none")
    for i, (sp, sq) in enumerate(seqs):
        y = y0 + 12 + i * 22
        s.text(x0 - 10, y, sp, size=11.5, anchor="end", fill=GRAY)
        s.mono(x0, y, sq, cw=cw, size=15, bold=True)
    yb = y0 + len(seqs) * 22 + 12
    s.text(x0 + cons * cw + cw / 2, yb, "conserved", size=11, anchor="middle", fill=GREEN)
    s.text(x0 + 8 * cw, yb + 14, "coevolving pair", size=11, anchor="middle", fill=BLUE)
    tx = 420
    s.text(tx, 52, "Column 7 never changes (always G):", size=11.5)
    s.text(tx, 67, "probably essential; mutations there", size=11.5)
    s.text(tx, 82, "are likely harmful.", size=11.5)
    s.text(tx, 110, "Columns 8 and 9 change together:", size=11.5)
    s.text(tx, 125, "T pairs with R and S pairs with K.", size=11.5)
    s.text(tx, 140, "Such pairs tend to touch in 3D,", size=11.5)
    s.text(tx, 155, "which is how MSAs reveal contacts.", size=11.5)
    s.text(16, 236, "Each row is a homolog from a different species; each column is one equivalent position.", size=11, fill=GRAY)
    s.save("u4-msa.svg")

if __name__ == "__main__":
    amino_acids(); structure_levels(); domains(); alphafold_p53(); msa()
