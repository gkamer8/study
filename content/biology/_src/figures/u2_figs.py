from figlib import *

def annotated(s, x, y, parts, cw=13, size=17, label_dy=26):
    """parts: list of (text, label, color). Draw monospace string with a bracket+label under each labeled part.
    Labels alternate between two rows to avoid collisions. Returns x end."""
    cur = x
    row = 0
    spans = []
    for t, lab, col in parts:
        s.mono(cur, y, t, cw=cw, size=size, bold=True, fill=col or INK)
        spans.append((cur, cur + len(t) * cw, lab, col))
        cur += len(t) * cw
    return cur, spans

def label_spans(s, spans, y, rows=(16, 38, 60), size=11, pad=10):
    """Greedy: put each label in the first row where it does not overlap earlier labels."""
    placed = {i: [] for i in range(len(rows))}
    for (a, b, lab, col) in spans:
        if not lab: continue
        c = (a + b) / 2
        w = max(tw(l, size) for l in lab.split("\n")) * 1.15
        for r in range(len(rows)):
            if all(c + w / 2 + pad < x1 or c - w / 2 - pad > x2 for x1, x2 in placed[r]):
                break
        placed[r].append((c - w / 2, c + w / 2))
        dy = rows[r]
        s.bracket(a + 1, b - 1, y + 6)
        s.line(c, y + 11, c, y + dy, stroke=LIGHT)
        for k, l in enumerate(lab.split("\n")):
            s.text(c, y + dy + 12 + k * 13, l, size=size, anchor="middle", fill=col or GRAY)

def fan_labels(s, spans, y, xs, dy=40, size=11):
    """Labels spread at fixed x positions, angled leader lines from each span."""
    k = 0
    for (a, b, lab, col) in spans:
        if not lab: continue
        c = (a + b) / 2
        lx = xs[k]; k += 1
        s.bracket(a + 1, b - 1, y + 6)
        s.line(c, y + 11, lx, y + dy - 4, stroke=LIGHT)
        for j, l in enumerate(lab.split("\n")):
            s.text(lx, y + dy + 8 + j * 14, l, size=size, anchor="middle", fill=col or GRAY, bold=(j == 0 and "\n" in lab))

def label_rows(s, spans, rows, y, size=11):
    """rows: list aligned with labeled spans; 0,1 = below; -1 = above."""
    k = 0
    for (a, b, lab, col) in spans:
        if not lab: continue
        r = rows[k]; k += 1
        c = (a + b) / 2
        if r >= 0:
            dy = (16, 38)[r]
            s.bracket(a + 1, b - 1, y + 6)
            s.line(c, y + 11, c, y + dy, stroke=LIGHT)
            s.text(c, y + dy + 12, lab, size=size, anchor="middle", fill=col or GRAY)
        else:
            s.bracket(a + 1, b - 1, y - 17, up=True)
            s.line(c, y - 22, c, y - 26, stroke=LIGHT)
            s.text(c, y - 30, lab, size=size, anchor="middle", fill=col or GRAY)

def hgvs():
    s = SVG(720, 462, "Anatomy of an HGVS variant description (BRAF V600E)")
    s.text(16, 22, "Transcript level (c.): what most papers and reports quote", size=13, bold=True)
    parts = [("NM_", "RefSeq mRNA", BLUE), ("004333", "accession number", None), (".6", "version", BLUE), (":", None, LIGHT),
             ("c.", "coding DNA", RED), ("1799", "position", None), ("T", "ref base", None), (">", None, LIGHT), ("A", "new base", RED)]
    end, spans = annotated(s, 40, 84, parts)
    label_rows(s, spans, [0, -1, 0, -1, 0, -1, 0], 84)
    s.text(end + 16, 84, "c.1 = the A of the ATG start codon", size=11.5, fill=GRAY)

    y = 218
    s.text(16, y - 46, "Protein level (p.)", size=13, bold=True)
    parts = [("NP_", "RefSeq protein", BLUE), ("004324", "accession number", None), (".2", "version", BLUE), (":", None, LIGHT),
             ("p.", "protein", RED), ("Val", "ref amino acid", None), ("600", "position", None), ("Glu", "new amino acid", RED)]
    end, spans = annotated(s, 40, y + 10, parts)
    label_rows(s, spans, [0, -1, 0, 1, -1, 0, 1], y + 10)
    s.text(end + 16, y + 10, "short form: p.V600E", size=12, fill=INK)

    y = 340
    s.text(16, y - 22, "How the two connect: codon 600 = c.1798–c.1800", size=13, bold=True)
    cw = 15
    x = 40
    for i, (b, n) in enumerate(zip("GTG", [1798, 1799, 1800])):
        s.mono(x + i * cw, y + 8, b, cw=cw, size=17, bold=True, fill=RED if i == 1 else INK)
    s.text(x + 3 * cw + 10, y + 8, "Val", size=13)
    s.arrow(x + 3 * cw + 40, y + 3, x + 3 * cw + 78, y + 3)
    x2 = x + 3 * cw + 90
    for i, b in enumerate("GAG"):
        s.mono(x2 + i * cw, y + 8, b, cw=cw, size=17, bold=True, fill=RED if i == 1 else INK)
    s.text(x2 + 3 * cw + 10, y + 8, "Glu", size=13, fill=RED)
    s.text(x + 1.5 * cw, y + 28, "c.1799 is the middle base of codon 600 (codon n spans c.3n−2 to c.3n)", size=11.5, fill=GRAY)

    y = 410
    s.text(16, y - 14, "Genome level (g.)", size=13, bold=True)
    parts = [("NC_", None, BLUE), ("000007", None, None), (".14", None, BLUE), (":", None, LIGHT), ("g.", None, RED),
             ("140753336", None, None), ("A", None, None), (">", None, LIGHT), ("T", None, RED)]
    end, spans = annotated(s, 40, y + 12, parts, size=15, cw=11.5)
    s.text(end + 14, y + 12, "chromosome 7, GRCh38 (.14 = this build)", size=11.5, fill=GRAY)
    s.text(40, y + 36, "BRAF lies on the minus strand, so T>A on the transcript is A>T on the genome's + strand.", size=11.5)
    s.save("u2-hgvs.svg")

# ---------------------------------------------------------------------------
def c_numbering():
    s = SVG(720, 222, "HGVS c. numbering along a transcript")
    y = 92
    s.text(16, 22, "c. coordinates along a gene (positions count on the transcript, not the genome)", size=13, bold=True)
    # layout x
    utr5 = (48, 150); cds1 = (150, 290); intr = (290, 440); cds2 = (440, 570); utr3 = (570, 680)
    s.line(utr5[0], y, utr3[1], y)
    s.rect(utr5[0], y - 5, utr5[1] - utr5[0], 10, fill="#fff")
    s.rect(cds1[0], y - 10, cds1[1] - cds1[0], 20, fill=BLUE_T)
    s.rect(cds2[0], y - 10, cds2[1] - cds2[0], 20, fill=BLUE_T)
    s.rect(cds2[1], y - 5, utr3[1] - cds2[1], 10, fill="#fff")
    s.text((utr5[0] + utr5[1]) / 2, y - 18, "5' UTR", size=11, anchor="middle", fill=GRAY)
    s.text((cds1[0] + cds1[1]) / 2, y - 18, "exon 1 (CDS part)", size=11, anchor="middle", fill=GRAY)
    s.text((intr[0] + intr[1]) / 2, y - 18, "intron 1", size=11, anchor="middle", fill=GRAY)
    s.text((cds2[0] + cds2[1]) / 2, y - 18, "exon 2 (CDS part)", size=11, anchor="middle", fill=GRAY)
    s.text((utr3[0] + utr3[1]) / 2, y - 18, "3' UTR", size=11, anchor="middle", fill=GRAY)
    s.text(42, y + 4, "5'", size=12, anchor="end", bold=True); s.text(690, y + 4, "3'", size=12, bold=True)
    # stop codon region
    s.rect(cds2[1] - 18, y - 10, 18, 20, fill=RED_T)
    s.text(cds2[1] - 9, y - 34, "stop", size=11, anchor="middle", fill=RED)
    ticks = [(60, "c.−14", INK, 60), (148, "c.−1", INK, 120), (152, "c.1", GREEN, 180), (288, "c.88", INK, 260),
             (292, "c.88+1", RED, 322), (436, "c.89−2", RED, 404), (442, "c.89", INK, 470),
             (572, "c.*1", INK, 592), (650, "c.*20", INK, 652)]
    for x, lab, col, lx in ticks:
        lc = col if col != INK else GRAY
        s.line(x, y + 11, x, y + 15, stroke=lc)
        s.line(x, y + 15, lx, y + 27, stroke=LIGHT)
        s.text(lx, y + 40, lab, size=11, anchor="middle", family=MONO, fill=col)
    s.text(152, y - 34, "ATG", size=11, anchor="middle", family=MONO, bold=True, fill=GREEN)
    yt = 168
    lines = ["c.1 is the A of ATG; bases before it are negative (c.−1 is the base just before; there is no c.0).",
             "Intronic bases count from the nearest exon edge: +N after an exon's last base, −N before the next exon's first.",
             "After the stop codon the count restarts with *: c.*1 is the first 3' UTR base."]
    for i, t in enumerate(lines):
        s.text(16, yt + i * 19, t, size=11.5, fill=INK if i == 0 else INK)
    s.save("u2-c-numbering.svg")

# ---------------------------------------------------------------------------
def identifiers():
    s = SVG(720, 300, "TP53 identifiers across databases")
    cols = [("Gene", 150), ("Transcript (RNA)", 350), ("Protein", 550)]
    s.text(16, 22, "One gene, many IDs: TP53 (human)", size=13, bold=True)
    for name, x in cols:
        s.text(x, 50, name, size=12.5, anchor="middle", bold=True)
    rows = [("HGNC", ["TP53  ·  HGNC:11998", "", ""]),
            ("NCBI", ["Gene ID 7157", "NM_000546.6", "NP_000537.3"]),
            ("Ensembl", ["ENSG00000141510", "ENST00000269305", "ENSP00000269305"]),
            ("UniProt", ["", "", "P04637  (P53_HUMAN)"]),
            ("Structures", ["", "", "PDB 1TUP  ·  AF-P04637-F1"])]
    for i, (src, vals) in enumerate(rows):
        y = 84 + i * 36
        s.text(16, y + 4, src, size=12, fill=GRAY, bold=True)
        for (name, x), v in zip(cols, vals):
            if not v: continue
            w = max(150, tw(v, 12) * 1.12 + 20)
            s.rect(x - w / 2, y - 13, w, 24, fill=BLUE_T if src in ("NCBI", "Ensembl") else GRAY_T, stroke=RULE, rx=3)
            s.text(x, y + 4, v, size=12, anchor="middle", family=MONO if src not in ("HGNC",) else MONO)
        if src in ("NCBI", "Ensembl"):
            s.arrow(150 + 82, y, 350 - 82, y, stroke=LIGHT, sw=1, head=6)
            s.arrow(350 + 82, y, 550 - 82, y, stroke=LIGHT, sw=1, head=6)
    # MANE Select pair
    for yy in (120, 156):
        s.rect(350 - 77, yy - 15, 154, 28, fill="none", stroke=GREEN, sw=1.5, rx=4)
    s.text(350, 186, "MANE Select pair", size=11, anchor="middle", fill=GREEN, bold=True)
    s.text(16, 272, "NM_000546.6 and ENST00000269305 are the MANE Select pair: the same transcript sequence in both databases.", size=11.5, fill=GREEN)
    s.text(16, 290, "Gene → transcript → protein is one-to-many: TP53 has several transcripts; P04637-2 etc. are its other protein isoforms.", size=11.5, fill=GRAY)
    s.save("u2-identifiers.svg")

# ---------------------------------------------------------------------------
def hla():
    s = SVG(720, 190, "Reading an HLA allele name")
    parts = [("HLA-DRB1", "gene", None), ("*", "separator", GRAY), ("15", "field 1\nallele group", RED), (":", None, LIGHT),
             ("01", "field 2\nspecific protein", RED), (":", None, LIGHT), ("01", "field 3\nsilent change\nin coding region", BLUE),
             (":", None, LIGHT), ("01", "field 4\nchange outside\ncoding region", BLUE)]
    s.text(16, 22, "HLA allele names: each field adds resolution", size=13, bold=True)
    end, spans = annotated(s, 210, 62, parts, cw=15, size=19)
    fan_labels(s, spans, 62, [90, 200, 315, 430, 545, 660], dy=44)
    s.text(16, 182, "“Two-field” typing (HLA-DRB1*15:01) fixes the protein. A trailing N (e.g. …:01N) marks a null allele that is not expressed.", size=11.5, fill=GRAY)
    s.save("u2-hla.svg")

if __name__ == "__main__":
    hgvs(); c_numbering(); identifiers(); hla()
