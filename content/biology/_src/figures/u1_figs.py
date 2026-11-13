import math, os
from figlib import *

COMP = {"A": "T", "T": "A", "G": "C", "C": "G"}
def revcomp(s): return "".join(COMP[c] for c in reversed(s))

# ---------------------------------------------------------------------------
def dna_strands():
    s = SVG(720, 360, "DNA strand direction, base pairing and reverse complement")
    # ---- left panel: backbone chemistry of one strand
    s.text(20, 22, "One strand, chemically", size=13, bold=True)
    bases = ["A", "T", "G"]
    r = 20
    prev_c3 = None
    for i, b in enumerate(bases):
        cx, cy = 92, 92 + i * 92
        ang = {"O": -90, "C1": -18, "C2": 54, "C3": 126, "C4": 198}
        V = {k: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for k, a in ang.items()}
        c5 = (V["C4"][0] - 12, V["C4"][1] - 24)
        P = (c5[0], c5[1] - 22)
        # bond C3' (previous) -> P
        if prev_c3:
            s.line(prev_c3[0], prev_c3[1], P[0], P[1] + 8, stroke=INK, sw=1.2)
        s.line(P[0], P[1] + 8, c5[0], c5[1], sw=1.2)
        s.line(c5[0], c5[1], V["C4"][0], V["C4"][1], sw=1.2)
        s.poly([V[k] for k in ["O", "C1", "C2", "C3", "C4"]], fill="#fff", stroke=INK, sw=1.2)
        s.text(V["O"][0], V["O"][1] - 3, "O", size=9, anchor="middle", fill=GRAY)
        s.circle(P[0], P[1], 8, fill=GRAY_T, stroke=INK)
        s.text(P[0], P[1] + 3.5, "P", size=10, anchor="middle")
        s.text(c5[0] - 5, c5[1] + 4, "5'", size=10, anchor="end", fill=BLUE, bold=True)
        s.text(V["C3"][0] - 5, V["C3"][1] + 9, "3'", size=10, anchor="end", fill=RED, bold=True)
        s.text(V["C1"][0] + 2, V["C1"][1] - 5, "1'", size=9, fill=GRAY)
        # base
        s.line(V["C1"][0], V["C1"][1], V["C1"][0] + 22, V["C1"][1], sw=1.2)
        s.rect(V["C1"][0] + 22, V["C1"][1] - 11, 24, 22, fill=BLUE_T, stroke=INK)
        s.text(V["C1"][0] + 34, V["C1"][1] + 5, b, size=13, anchor="middle", bold=True)
        prev_c3 = V["C3"]
        if i == 0:
            s.text(P[0] - 13, P[1] + 4, "5' end", size=11, anchor="end", fill=BLUE, bold=True)
    s.line(prev_c3[0], prev_c3[1], prev_c3[0] - 6, prev_c3[1] + 16, sw=1.2)
    s.text(prev_c3[0] - 6, prev_c3[1] + 29, "OH", size=10, anchor="middle")
    s.text(prev_c3[0] - 20, prev_c3[1] + 29, "3' end", size=11, anchor="end", fill=RED, bold=True)
    s.arrow(178, 52, 178, 300, stroke=GRAY, sw=1)
    s.text(186, 180, "5'→3'", size=11, fill=GRAY, rotate=90)
    s.text(20, 345, "Phosphate links the 3' carbon of one sugar", size=10.5, fill=GRAY)
    s.text(20, 358 - 0, "to the 5' carbon of the next.", size=10.5, fill=GRAY)

    # ---- right panel: double strand ladder
    X0 = 258
    s.line(X0 - 18, 10, X0 - 18, 350, stroke=RULE)
    s.text(X0, 22, "Two antiparallel strands", size=13, bold=True)
    top = "ATGCTTCA"
    bot = "".join(COMP[c] for c in top)
    sp, x1 = 44, 312
    yt, yb = 62, 162
    s.arrow(x1 - 22, yt, x1 + sp * 7 + 30, yt, sw=2, head=9)
    s.arrow(x1 + sp * 7 + 22, yb, x1 - 30, yb, sw=2, head=9)
    s.text(x1 - 32, yt + 5, "5'", size=14, anchor="end", bold=True, fill=BLUE)
    s.text(x1 + sp * 7 + 38, yt + 5, "3'", size=14, bold=True, fill=RED)
    s.text(x1 - 38, yb + 5, "3'", size=14, anchor="end", bold=True, fill=RED)
    s.text(x1 + sp * 7 + 32, yb + 5, "5'", size=14, bold=True, fill=BLUE)
    for i, (a, b) in enumerate(zip(top, bot)):
        x = x1 + i * sp
        s.line(x, yt, x, yt + 14, sw=1.2)
        s.line(x, yb, x, yb - 14, sw=1.2)
        s.rect(x - 12, yt + 14, 24, 22, fill=BLUE_T)
        s.rect(x - 12, yb - 36, 24, 22, fill=GREEN_T)
        s.mono(x - 6, yt + 30, a, cw=12, size=14, bold=True)
        s.mono(x - 6, yb - 20, b, cw=12, size=14, bold=True)
        nh = 2 if a in "AT" else 3
        for k in range(nh):
            dx = (k - (nh - 1) / 2) * 6
            s.line(x + dx, yt + 38, x + dx, yb - 38, stroke=GRAY, sw=1, dash="2,2")
    s.text(x1 + sp * 7 + 30, yb + 22, "dashes = hydrogen bonds (A–T 2, G–C 3)", size=10.5, fill=GRAY, anchor="end")
    s.text(x1 - 60, yt - 12, "top strand (+)", size=10.5, fill=GRAY)
    s.text(x1 - 60, yb + 22, "bottom strand (−)", size=10.5, fill=GRAY)

    # worked example
    y = 230
    rows = [("Top strand, 5'→3':", "5'-" + top + "-3'", INK),
            ("Bottom strand as drawn:", "3'-" + bot + "-5'", INK),
            ("Bottom written 5'→3':", "5'-" + revcomp(top) + "-3'", RED)]
    for j, (lab, seq, col) in enumerate(rows):
        s.text(X0, y + j * 26, lab, size=12)
        e1, core, e2 = seq[:3], seq[3:-3], seq[-3:]
        s.text(X0 + 165, y + j * 26, e1[:2], size=12, fill=col, bold=True)
        s.mono(X0 + 182, y + j * 26, core, cw=11, size=14, fill=col, bold=(j == 2))
        s.text(X0 + 186 + 11 * len(core), y + j * 26, e2[1:], size=12, fill=col, bold=True)
    s.text(X0, y + 3 * 26 + 2, "= reverse complement of the top strand: complement each base, then reverse.", size=11.5, fill=RED)
    s.text(X0, y + 3 * 26 + 22, "Genome files store only the + strand; a − strand gene's RNA is its reverse complement.", size=10.5, fill=GRAY)
    s.save("u1-dna-strands.svg")

# ---------------------------------------------------------------------------
CODE = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
B = "TCAG"
AA3 = dict(F="Phe", L="Leu", S="Ser", Y="Tyr", C="Cys", W="Trp", P="Pro", H="His", Q="Gln", R="Arg",
           I="Ile", M="Met", T="Thr", N="Asn", K="Lys", V="Val", A="Ala", D="Asp", E="Glu", G="Gly")
AA3["*"] = "Stop"
def codon_aa(c): return CODE[B.index(c[0]) * 16 + B.index(c[1]) * 4 + B.index(c[2])]
def translate(s): return "".join(codon_aa(s[i:i + 3]) for i in range(0, len(s) - 2, 3))

def codon_table():
    cw, rh = 150, 21
    x0, y0 = 62, 58
    H = y0 + 4 * (4 * rh + 8) + 46
    s = SVG(720, H, "The standard genetic code (DNA codons)")
    s.text(x0 + 300, 22, "Second base", size=12, anchor="middle", bold=True)
    s.text(18, y0 + 2 * (4 * rh + 8), "First base", size=12, anchor="middle", bold=True, rotate=-90)
    s.text(x0 + 4 * cw + 30, y0 + 2 * (4 * rh + 8), "Third base", size=12, anchor="middle", bold=True, rotate=90)
    for j, b2 in enumerate(B):
        s.text(x0 + j * cw + cw / 2, 44, b2, size=14, anchor="middle", bold=True, family=MONO)
    for i, b1 in enumerate(B):
        yb = y0 + i * (4 * rh + 8)
        s.text(x0 - 18, yb + 2 * rh + 5, b1, size=14, anchor="middle", bold=True, family=MONO)
        for j, b2 in enumerate(B):
            xb = x0 + j * cw
            s.rect(xb + 2, yb, cw - 4, 4 * rh, stroke=RULE)
            for k, b3 in enumerate(B):
                c = b1 + b2 + b3
                a = codon_aa(c)
                y = yb + k * rh
                if a == "*":
                    s.rect(xb + 3, y + 1, cw - 6, rh - 2, fill=RED_T, stroke="none")
                elif c == "ATG":
                    s.rect(xb + 3, y + 1, cw - 6, rh - 2, fill=GREEN_T, stroke="none")
                s.mono(xb + 10, y + 15, c, cw=9.5, size=13, bold=True)
                col = RED if a == "*" else (GREEN if c == "ATG" else INK)
                s.text(xb + 54, y + 15, AA3[a], size=12.5, fill=col)
                s.text(xb + 92, y + 15, ("stop" if a == "*" else a) if a != "*" else "", size=12.5, fill=col, bold=True)
                if a != "*":
                    s.text(xb + 92, y + 15, "", size=1)
                if c == "ATG":
                    s.text(xb + cw - 8, y + 15, "start", size=10.5, anchor="end", fill=GREEN)
                if a == "*":
                    s.text(xb + 92, y + 15, "", size=1)
            for k, b3 in enumerate(B):
                if j == 3:
                    s.text(x0 + 4 * cw + 12, yb + k * rh + 15, b3, size=12, anchor="middle", family=MONO, fill=GRAY)
    yl = H - 20
    s.rect(x0, yl - 11, 14, 14, fill=GREEN_T, stroke="none")
    s.text(x0 + 20, yl, "ATG = Met, the usual start codon", size=11.5)
    s.rect(x0 + 250, yl - 11, 14, 14, fill=RED_T, stroke="none")
    s.text(x0 + 270, yl, "TAA, TAG, TGA = stop (written * or Ter)", size=11.5)
    s.save("u1-codon-table.svg")

# ---------------------------------------------------------------------------
def reading_frames():
    seq = "ATGGAATGGCTGAAAGGTTAA"
    s = SVG(720, 400, "Reading frames and variant types")
    cw = 17
    x0 = 150
    s.text(16, 22, "Three reading frames of one strand", size=13, bold=True)
    s.text(16, 50, "sequence", size=12, fill=GRAY)
    s.mono(x0, 50, seq, cw=cw, size=15, bold=True)
    for f in range(3):
        y = 76 + f * 30
        s.text(16, y + 4, f"frame {f + 1}" + (" (from ATG)" if f == 0 else ""), size=12, fill=GRAY)
        k = f
        while k + 3 <= len(seq):
            xa, xb = x0 + k * cw + 2, x0 + (k + 3) * cw - 2
            aa = codon_aa(seq[k:k + 3])
            col = RED if aa == "*" else (GREEN if seq[k:k + 3] == "ATG" else INK)
            s.path(f"M{xa:.1f},{y - 12} L{xa:.1f},{y - 8} L{xb:.1f},{y - 8} L{xb:.1f},{y - 12}", stroke=LIGHT)
            s.text((xa + xb) / 2, y + 6, aa if aa != "*" else "stop", size=12.5, anchor="middle", fill=col, bold=(f == 0))
            k += 3
    s.text(x0 + len(seq) * cw + 14, 82, "M E W L K G stop: an ORF", size=11.5, fill=GREEN)
    s.text(x0 + len(seq) * cw + 14, 112, "other frames: unrelated", size=11.5, fill=GRAY)
    s.text(x0 + len(seq) * cw + 14, 126, "amino acids", size=11.5, fill=GRAY)

    # ---- variant types
    yv = 190
    s.line(16, yv - 22, 704, yv - 22, stroke=RULE)
    s.text(16, yv, "Variant types (frame 1)", size=13, bold=True)
    ref = seq
    rows = [("reference", ref, None, ""),
            ("synonymous", ref[:3] + "GAG" + ref[6:], [5], "GAA→GAG: still Glu"),
            ("missense", ref[:3] + "AAA" + ref[6:], [3], "GAA→AAA: Glu→Lys"),
            ("nonsense", ref[:6] + "TAG" + ref[9:], [7], "TGG→TAG: early stop"),
            ("frameshift", ref[:3] + ref[4:], [3], "−1 bp: new frame, early stop"),
            ("in-frame deletion", ref[:3] + ref[6:], [3], "−3 bp: one Glu lost")]
    for r, (lab, sq, pos, note) in enumerate(rows):
        y = yv + 26 + r * 30
        s.text(16, y, lab, size=12, fill=GRAY if r else INK, bold=(r == 0))
        # codon-separated display
        xx = x0
        prot = translate(sq)
        for k in range(0, len(sq), 3):
            cod = sq[k:k + 3]
            cols = []
            for t in range(len(cod)):
                gi = k + t
                cols.append(RED if pos and gi in pos and lab not in ("frameshift", "in-frame deletion") else None)
            s.mono(xx, y, cod, cw=10.5, size=14, colors=cols, bold=True)
            xx += 3 * 10.5 + 6
        if lab in ("frameshift", "in-frame deletion"):
            # caret where bases were removed
            xc = x0 + 3 * 10.5 + 3
            s.poly([(xc - 4, y - 19), (xc + 4, y - 19), (xc, y - 13)], fill=RED)
        # protein
        px = x0 + 7 * (3 * 10.5 + 6) + 4
        out = []
        for i, a in enumerate(prot):
            out.append(a)
            if a == "*": break
        ptxt = " ".join("stop" if a == "*" else a for a in out)
        refp = translate(ref)
        s.text(px, y, ptxt, size=12.5, family=SANS, bold=True, fill=INK if r == 0 else RED if ptxt.replace(" ", "") != " ".join(refp).replace(" ", "").replace("*", "stop") else INK)
        s.text(704, y, note, size=11, anchor="end", fill=GRAY)
    s.save("u1-reading-frames.svg")

# ---------------------------------------------------------------------------
def exon(s, x1, x2, y, kind="cds", fill=BLUE_T):
    """UCSC-style: CDS thick, UTR thin."""
    h = 18 if kind == "cds" else 9
    s.rect(x1, y - h / 2, x2 - x1, h, fill=fill if kind == "cds" else "#fff", stroke=INK, sw=1)

def gene_structure():
    s = SVG(720, 372, "Anatomy of a protein-coding gene and its mRNA")
    # exon layout: (start, end, segments[(x1,x2,kind)])
    ex = [(160, 215, [(160, 188, "utr"), (188, 215, "cds")]),
          (300, 345, [(300, 345, "cds")]),
          (420, 468, [(420, 468, "cds")]),
          (540, 650, [(540, 572, "cds"), (572, 650, "utr")])]
    # --- genomic DNA
    y = 74
    s.text(16, 20, "Genomic DNA (gene on the + strand, 5'→3' left to right)", size=13, bold=True)
    s.line(16, y, 704, y, stroke=INK, sw=1)
    s.text(10, y + 4, "", size=1)
    # enhancer far away
    s.rect(28, y - 8, 40, 16, fill=GREEN_T, stroke=GREEN)
    s.text(48, y + 26, "enhancer", size=11, anchor="middle", fill=GREEN)
    s.text(16, y + 39, "(often 10s–100s kb away)", size=10, fill=GRAY)
    for xb in (88, 94):
        s.line(xb - 3, y + 8, xb + 3, y - 8, stroke=INK, sw=1.2)
    s.rect(84, y - 2, 13, 4, fill="#fff", stroke="none")
    s.line(84, y - 2, 84, y - 2, stroke="none")
    # promoter
    s.rect(112, y - 8, 46, 16, fill=GRAY_T, stroke=GRAY, dash="3,2")
    s.text(135, y + 26, "promoter", size=11, anchor="middle", fill=GRAY)
    # TSS bent arrow
    s.path(f"M160,{y - 9} L160,{y - 26} L184,{y - 26}", stroke=INK, sw=1.3)
    s.poly([(190, y - 26), (183, y - 30), (183, y - 22)], fill=INK)
    s.text(160, y - 31, "TSS", size=11, anchor="middle")
    for i, (a, b, segs) in enumerate(ex):
        for (x1, x2, k) in segs: exon(s, x1, x2, y, k)
        s.text((a + b) / 2, y - 14, f"exon {i + 1}", size=11, anchor="middle", fill=GRAY)
    # intron labels with GT...AG
    for i in range(3):
        a, b = ex[i][1], ex[i + 1][0]
        s.text(a + 3, y - 4, "GT", size=10, family=MONO, bold=True, fill=BLUE)
        s.text(b - 3, y - 4, "AG", size=10, family=MONO, bold=True, fill=BLUE, anchor="end")
        s.text((a + b) / 2, y + 18, f"intron {i + 1}", size=11, anchor="middle", fill=GRAY)
    s.text(188, y + 24, "ATG", size=10, family=MONO, bold=True, fill=GREEN, anchor="middle")
    s.line(188, y + 10, 188, y + 14, stroke=GREEN)
    s.text(572, y + 24, "stop", size=10, bold=True, fill=RED, anchor="middle")
    s.line(572, y + 10, 572, y + 14, stroke=RED)
    s.text(622, y + 24, "AATAAA", size=10, family=MONO, bold=True, fill=GRAY, anchor="middle")
    s.line(622, y + 5, 622, y + 14, stroke=GRAY)
    s.line(650, y - 12, 650, y + 12, stroke=INK, dash="2,2")
    s.text(654, y + 24, "cleavage", size=10, fill=GRAY)

    # --- pre-mRNA
    y2 = 172
    s.text(16, y2 - 26, "pre-mRNA (transcription copies everything from TSS to cleavage site)", size=13, bold=True)
    s.line(160, y2, 650, y2, stroke=INK)
    for (a, b, segs) in ex:
        for (x1, x2, k) in segs: exon(s, x1, x2, y2, k)
    s.text(152, y2 + 4, "5'", size=12, anchor="end", bold=True)
    s.text(658, y2 + 4, "3'", size=12, bold=True)
    for i in range(3):
        a, b = ex[i][1], ex[i + 1][0]
        s.text((a + b) / 2, y2 - 6, "GU…AG", size=10, family=MONO, anchor="middle", fill=BLUE)

    # --- mature mRNA
    y3 = 268
    s.text(16, y3 - 46, "Mature mRNA (introns spliced out, 5' cap and poly(A) tail added)", size=13, bold=True)
    mx = 200
    pos = []
    for (a, b, segs) in ex:
        L = b - a
        pos.append((mx, mx + L))
        for (x1, x2, k) in segs: exon(s, mx + (x1 - a), mx + (x2 - a), y3, k)
        mx += L
    for (a, b, segs), (m1, m2) in zip(ex, pos):
        s.line(a, y2 + 10, m1, y3 - 10, stroke=LIGHT, dash="2,3")
        s.line(b, y2 + 10, m2, y3 - 10, stroke=LIGHT, dash="2,3")
    s.circle(190, y3, 8, fill=GRAY_T)
    s.text(190, y3 + 3.5, "cap", size=7.5, anchor="middle")
    s.text(176, y3 + 4, "5'", size=12, anchor="end", bold=True)
    s.text(mx + 4, y3 + 4, "AAAAAA…", size=12, family=MONO, bold=True)
    s.text(mx + 80, y3 + 4, "3'", size=12, bold=True)
    cds1 = pos[0][0] + 28; cds2 = pos[3][0] + 32
    s.text(cds1, y3 - 14, "AUG", size=10, family=MONO, bold=True, fill=GREEN, anchor="middle")
    s.text(cds2, y3 - 14, "stop", size=10, bold=True, fill=RED, anchor="middle")
    yb = y3 + 16
    s.bracket(pos[0][0], cds1 - 1, yb)
    s.text(pos[0][0] - 4, yb + 18, "5' UTR", size=11, anchor="end", fill=GRAY)
    s.bracket(cds1 + 1, cds2 - 1, yb, "CDS: translated into protein", size=11, fill=INK)
    s.bracket(cds2 + 1, pos[3][1], yb, "3' UTR", size=11)
    s.bracket(pos[3][1] + 2, mx + 60, yb, "poly(A) tail", size=11)
    # legend
    yl = 354
    exon(s, 16, 40, yl - 4, "cds"); s.text(46, yl, "coding exon part (CDS)", size=11)
    exon(s, 190, 214, yl - 4, "utr"); s.text(220, yl, "untranslated exon part (UTR)", size=11)
    s.line(400, yl - 4, 424, yl - 4); s.text(430, yl, "intron", size=11)
    s.text(490, yl, "Not to scale: introns are usually far longer.", size=11, fill=GRAY)
    s.save("u1-gene-structure.svg")

# ---------------------------------------------------------------------------
def splicing():
    s = SVG(720, 404, "Splice sites and alternative splicing")
    s.text(16, 20, "Splice sites at one intron (DNA letters; the RNA has U for T)", size=13, bold=True)
    # exon | GTAAGT .... A .... YYYYYYY N C AG | exon
    left = "CAG"; donor = "GTAAGT"; mid1 = "………"; bp = "A"; mid2 = "……"; ppt = "TTTTCTTTCC"; acc = "CAG"; right = "GTC"
    cw = 13
    x = 110; y = 92
    s.rect(x - 8, y - 20, len(left) * cw + 8, 28, fill=BLUE_T, stroke=INK)
    s.mono(x, y, left, cw=cw, size=15, bold=True)
    xs_left = x
    x += len(left) * cw
    xd = x
    s.mono(x, y, donor, cw=cw, size=15, bold=True, colors=[RED, RED] + [None] * 4)
    x += len(donor) * cw
    s.text(x + 30, y, "………", size=15, anchor="middle", fill=GRAY)
    x += 60
    xbp = x
    s.mono(x, y, bp, cw=cw, size=15, bold=True, fill=GREEN)
    x += cw
    s.text(x + 22, y, "……", size=15, anchor="middle", fill=GRAY)
    x += 44
    xp = x
    s.mono(x, y, ppt, cw=cw, size=15)
    x += len(ppt) * cw
    s.mono(x, y, "C" + "AG", cw=cw, size=15, bold=True, colors=[None, RED, RED])
    xa = x + cw
    x += 3 * cw
    s.rect(x, y - 20, len(right) * cw + 8, 28, fill=BLUE_T, stroke=INK)
    s.mono(x, y, right, cw=cw, size=15, bold=True)
    # labels
    s.text(xs_left + len(left) * cw / 2 - 4, y - 26, "exon 2", size=11, anchor="middle", fill=GRAY)
    s.text(x + len(right) * cw / 2 + 4, y - 26, "exon 3", size=11, anchor="middle", fill=GRAY)
    s.bracket(xd, xa + 2 * cw, y - 40, "intron 2 (removed by splicing)", up=True, size=11)
    yy = y + 22
    s.text(xd + cw, yy, "donor (5' splice site)", size=11, anchor="middle", fill=RED)
    s.text(xbp + cw / 2, yy, "branch point", size=11, anchor="middle", fill=GREEN)
    s.text(xp + len(ppt) * cw / 2, y - 24, "pyrimidine-rich tract", size=11, anchor="middle", fill=GRAY)
    s.text(xa + cw, yy, "acceptor (3' splice site)", size=11, anchor="middle", fill=RED)
    # HGVS-style positions, rotated under each base
    yh = y + 40
    s.text(16, yh + 4, "c. numbering", size=11, fill=GRAY)
    marks = [(xd - cw / 2, "c.88", INK), (xd + cw / 2, "c.88+1", RED), (xd + 1.5 * cw, "c.88+2", RED),
             (xa + cw / 2, "c.89−2", RED), (xa + 1.5 * cw, "c.89−1", RED), (xa + 2.5 * cw, "c.89", INK)]
    for j, (mx_, lab, col) in enumerate(marks):
        grp_c = marks[1][0] if j < 3 else marks[4][0]
        lx = grp_c + ((j % 3) - 1) * 50
        s.line(mx_, yh - 10, lx, yh + 2, stroke=LIGHT)
        s.text(lx, yh + 14, lab, size=10.5, family=MONO, fill=col, anchor="middle")
    s.text(16, yh + 44, "The GT and AG (red) are nearly invariant; variants there (±1, ±2) usually break splicing.", size=11.5)

    # --- isoforms
    y0 = 224
    s.line(16, y0 - 18, 704, y0 - 18, stroke=RULE)
    s.text(16, y0, "One gene, several isoforms (as a genome browser draws them)", size=13, bold=True)
    exs = [(120, 165), (215, 250), (300, 330), (380, 420), (490, 560)]
    def model(yy, keep, retain=None, label="", note="", fill=BLUE_T):
        s.text(16, yy + 4, label, size=12, fill=INK)
        ks = [exs[i] for i in keep]
        s.line(ks[0][0], yy, ks[-1][1], yy, stroke=INK)
        for i in keep:
            a, b = exs[i]; s.rect(a, yy - 8, b - a, 16, fill=fill)
        if retain is not None:
            a = exs[retain][1]; b = exs[retain + 1][0]
            s.rect(a, yy - 8, b - a, 16, fill=RED_T, stroke=INK)
        # chevrons on introns
        for (a, b), (c, d) in zip(ks, ks[1:]):
            if retain is not None and a == exs[retain][0]: continue
            m = (b + c) / 2
            s.path(f"M{m - 3},{yy - 3} L{m + 2},{yy} L{m - 3},{yy + 3}", stroke=GRAY)
        s.text(578, yy + 4, note, size=11, fill=GRAY)
    model(y0 + 34, range(5), label="gene", note="exons 1–5", fill=GRAY_T)
    for i, (a, b) in enumerate(exs):
        s.text((a + b) / 2, y0 + 20, str(i + 1), size=10.5, anchor="middle", fill=GRAY)
    model(y0 + 74, [0, 1, 2, 3, 4], label="isoform 1", note="all exons")
    model(y0 + 108, [0, 1, 3, 4], label="isoform 2", note="exon 3 skipped")
    model(y0 + 142, [0, 1, 2, 3, 4], retain=3, label="isoform 3", note="intron 4 kept")
    s.text(16, y0 + 172, "Each isoform gets its own transcript ID (ENST…, NM_…) and may encode a different protein.", size=11.5, fill=GRAY)
    s.save("u1-splicing.svg")

# ---------------------------------------------------------------------------
def central_dogma():
    s = SVG(720, 404, "The central dogma: DNA to RNA to protein")
    s.rect(8, 8, 704, 238, fill="none", stroke=LIGHT, rx=10, dash="5,4")
    s.text(700, 26, "nucleus", size=12, anchor="end", fill=GRAY, italic=True)
    s.text(700, 266, "cytoplasm", size=12, anchor="end", fill=GRAY, italic=True)
    ex = [(250, 290), (350, 380), (430, 470), (530, 580)]
    LX = 24; GX = 250
    # DNA
    y = 46
    s.text(LX, y + 4, "DNA", size=13, bold=True)
    s.line(200, y - 5, 640, y - 5, sw=1.5); s.line(200, y + 5, 640, y + 5, sw=1.5)
    for i, (a, b) in enumerate(ex):
        s.rect(a, y - 8, b - a, 16, fill=BLUE_T)
    s.text(205, y - 13, "gene: exons (boxes) and introns", size=10.5, fill=GRAY)
    # arrow transcription
    s.arrow(110, y + 16, 110, y + 56, sw=1.3)
    s.text(122, y + 32, "transcription", size=12, bold=True)
    s.text(122, y + 46, "RNA polymerase II copies the gene", size=11, fill=GRAY)
    # pre-mRNA
    y = 132
    s.text(LX, y + 4, "pre-mRNA", size=13, bold=True)
    s.line(250, y, 580, y, sw=1.5)
    for (a, b) in ex: s.rect(a, y - 7, b - a, 14, fill=BLUE_T)
    s.text(242, y + 4, "5'", size=11, anchor="end"); s.text(586, y + 4, "3'", size=11)
    s.arrow(110, y + 16, 110, y + 56, sw=1.3)
    s.text(122, y + 32, "processing", size=12, bold=True)
    s.text(122, y + 46, "splicing removes introns; 5' cap and poly(A) tail added", size=11, fill=GRAY)
    # mRNA
    y = 218
    s.text(LX, y + 4, "mature mRNA", size=13, bold=True)
    x = 250
    for (a, b) in ex:
        s.rect(x, y - 7, b - a, 14, fill=BLUE_T); x += b - a
    s.circle(242, y, 6, fill=GRAY_T)
    s.text(x + 4, y + 4, "AAAA", size=11, family=MONO, bold=True)
    s.arrow(110, y + 16, 110, y + 56, sw=1.3)
    s.text(122, y + 45, "export to the cytoplasm", size=11, fill=GRAY)
    # translation
    y = 300
    s.text(LX, y + 4, "translation", size=13, bold=True)
    seq = "AUGGAAUGGCUGAAA"
    s.line(220, y + 10, 520, y + 10, sw=1)
    s.mono(250, y + 4, seq, cw=12, size=13)
    for k in range(0, 15, 3):
        s.path(f"M{250 + k * 12 + 2},{y + 14} L{250 + k * 12 + 2},{y + 18} L{250 + (k + 3) * 12 - 2},{y + 18} L{250 + (k + 3) * 12 - 2},{y + 14}", stroke=LIGHT)
    s.text(232, y + 4, "5'", size=11, anchor="end"); s.text(436, y + 4, "… 3'", size=11)
    s.raw(f'<ellipse cx="{250 + 7.5 * 12:.1f}" cy="{y - 2}" rx="56" ry="24" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    s.text(250 + 7.5 * 12, y - 30, "ribosome reads codons 5'→3'", size=11, anchor="middle", fill=GRAY)
    s.text(122, y + 40, "", size=1)
    s.arrow(110, y + 16, 110, y + 56, sw=1.3)
    s.text(122, y + 32, "one amino acid per codon: M, E, W, L, K …", size=11, fill=GRAY)
    # protein
    y = 384
    s.text(LX, y + 4, "protein", size=13, bold=True)
    aas = "MEWLK"
    for i, a in enumerate(aas):
        cx = 262 + i * 30
        if i: s.line(cx - 21, y, cx - 9, y, sw=1.2)
        s.circle(cx, y, 9, fill=GREEN_T, stroke=INK)
        s.text(cx, y + 4, a, size=11, anchor="middle", bold=True)
    s.text(392, y + 4, "…", size=13)
    s.text(242, y + 4, "N", size=11, anchor="end", bold=True)
    s.text(410, y + 4, "C", size=11, bold=True)
    s.text(428, y + 4, "then folds; may get PTMs (e.g. phosphorylation)", size=11, fill=GRAY)
    s.save("u1-central-dogma.svg")


def karyotype():
    """NHGRI karyotype (public domain) with chromosome numbers added."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "nhgri-karyotype-orig.png")).convert("L")
    im.thumbnail((1000, 1000))
    W, H = im.size
    pad = 0
    can = Image.new("L", (W, H + 10), 255)
    can.paste(im, (0, 0))
    d = ImageDraw.Draw(can)
    f = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 22)
    labels = {  # x-center, y (below pair) in the 1000-px image
        "1": (80, 192), "2": (210, 192), "3": (360, 192), "4": (705, 192), "5": (850, 192),
        "6": (75, 362), "7": (215, 362), "8": (355, 362), "9": (493, 362), "10": (633, 362), "11": (778, 362), "12": (922, 362),
        "13": (75, 545), "14": (220, 545), "15": (355, 545), "16": (633, 545), "17": (782, 545), "18": (928, 545),
        "19": (215, 728), "20": (352, 728), "21": (636, 728), "22": (785, 728), "X  Y": (928, 728),
    }
    for t, (x, y) in labels.items():
        w = d.textlength(t, font=f)
        d.text((x - w / 2, y), t, fill=40, font=f)
    out = os.path.join(OUT, "u1-karyotype.png")
    can.save(out, optimize=True)
    return out

if __name__ == "__main__":
    dna_strands(); codon_table(); reading_frames(); gene_structure(); splicing(); central_dogma(); karyotype()
