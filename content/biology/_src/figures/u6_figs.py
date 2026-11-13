from figlib import *

# ---------------------------------------------------------------------------
def fastq():
    s = SVG(720, 360, "Anatomy of a FASTQ record (Phred+33)")
    s.text(16, 22, "One FASTQ record = 4 lines", size=13, bold=True)
    hdr = "@A00123:45:HV3KLDSXY:2:1101:12345:1000 1:N:0:ACGTACGT"
    seq = "GATTTGGGGTTCAAAGCAGTATCN"
    qual = "IIIIIHHHGGG???>;;5552+(#"
    assert len(seq) == len(qual) == 24
    x0, cw = 130, 22
    labs = ["1  header", "2  sequence", "3  separator", "4  quality"]
    ys = [56, 132, 160, 188]
    for l, y in zip(labs, ys): s.text(16, y, l, size=11.5, fill=GRAY)
    s.text(x0, 56, hdr, size=12.5, family=MONO, bold=True)
    # header parse
    parts = [("A00123", "instrument"), ("45", "run"), ("HV3KLDSXY", "flow cell"), ("2", "lane"), ("1101", "tile"), ("12345:1000", "x:y on tile")]
    s.text(x0, 76, "instrument : run : flow cell : lane : tile : x : y   read 1 : not filtered (N) : control : index", size=10, fill=GRAY)
    s.mono(x0, 132, seq, cw=cw, size=15, bold=True)
    s.mono(x0, 160, "+", cw=cw, size=15, bold=True)
    s.mono(x0, 188, qual, cw=cw, size=15, bold=True, fill=BLUE)
    for i, ch in enumerate(qual):
        q = ord(ch) - 33
        x = x0 + i * cw + cw / 2
        s.text(x, 208, str(q), size=10, anchor="middle", fill=GRAY)
    s.text(16, 208, "Q = ASCII − 33", size=10.5, fill=GRAY)
    s.text(x0 + 23 * cw + cw / 2 + 0, 100, "", size=1)
    s.text(x0 + 22 * cw + cw, 116 - 22, "", size=1)
    s.text(x0 + 24 * cw - 2, 104, "", size=1)
    s.text(x0 + 0, 108, "one base per character", size=10.5, fill=GRAY)
    s.text(x0 + 24 * cw, 108, "N = base not called (quality # = Q2)", size=10.5, fill=RED, anchor="end")
    # decode table
    y = 248
    s.text(16, y, "Phred+33 decoding: Q = −10·log10(P_error)", size=12.5, bold=True)
    rows = [("!", 0, "1 (no information)"), ("+", 10, "1 in 10"), ("5", 20, "1 in 100"), ("?", 30, "1 in 1,000"), ("I", 40, "1 in 10,000")]
    s.text(16, y + 24, "character", size=11, fill=GRAY); s.text(16, y + 44, "ASCII code", size=11, fill=GRAY)
    s.text(16, y + 64, "Q", size=11, fill=GRAY); s.text(16, y + 84, "P(base wrong)", size=11, fill=GRAY)
    for j, (ch, q, p) in enumerate(rows):
        x = 180 + j * 110
        s.text(x, y + 24, ch, size=15, anchor="middle", family=MONO, bold=True, fill=BLUE)
        s.text(x, y + 44, str(ord(ch)), size=11, anchor="middle")
        s.text(x, y + 64, str(q), size=11, anchor="middle", bold=(q == 30))
        s.text(x, y + 84, p, size=11, anchor="middle")
    s.rect(180 + 3 * 110 - 48, y + 8, 96, 84, stroke=GREEN, rx=4)
    s.text(180 + 3 * 110, y + 104, "Q30: the usual quality bar", size=10.5, anchor="middle", fill=GREEN)
    s.save("u6-fastq.svg")

# ---------------------------------------------------------------------------
def coordinates():
    s = SVG(720, 350, "0-based half-open vs 1-based closed coordinates")
    seq = "ACGTTGCAAC"
    x0, cw, y = 226, 40, 110
    s.text(16, 22, "The same three bases (GTT) in both coordinate systems", size=13, bold=True)
    # boundaries (0-based)
    s.text(16, y - 46, "0-based, half-open", size=12, bold=True, fill=BLUE)
    s.text(16, y - 32, "numbers the gaps between bases", size=10.5, fill=GRAY)
    for k in range(len(seq) + 1):
        x = x0 + k * cw
        s.line(x, y - 30, x, y - 20, stroke=BLUE)
        s.text(x, y - 36, str(k), size=11.5, anchor="middle", fill=BLUE, bold=True)
    hl = range(2, 5)
    for i, b in enumerate(seq):
        x = x0 + i * cw
        s.rect(x, y - 18, cw, 28, fill=GREEN_T if i in hl else "#fff", stroke=INK)
        s.mono(x, y + 2, b, cw=cw, size=16, bold=True)
        s.text(x + cw / 2, y + 30, str(i + 1), size=11.5, anchor="middle", fill=RED, bold=True)
    s.text(16, y + 24, "1-based, closed", size=12, bold=True, fill=RED)
    s.text(16, y + 38, "numbers the bases themselves", size=10.5, fill=GRAY)
    # brackets
    s.bracket(x0 + 2 * cw, x0 + 5 * cw, y - 56, up=True, fill=BLUE)
    s.text(x0 + 3.5 * cw, y - 64, "start 2 … end 5 (end excluded)", size=10.5, anchor="middle", fill=BLUE)
    s.bracket(x0 + 2 * cw + 3, x0 + 5 * cw - 3, y + 40, fill=RED)
    s.text(x0 + 3.5 * cw, y + 62, "positions 3 … 5 (both included)", size=10.5, anchor="middle", fill=RED)
    # table
    yt = 210
    rows = [("BED", "chr1  2  5", "0-based, half-open", BLUE),
            ("Python / numpy", "seq[2:5]", "0-based, half-open", BLUE),
            ("GTF / GFF", "chr1  3  5", "1-based, closed", RED),
            ("SAM, VCF (POS)", "POS = 3", "1-based (first base)", RED),
            ("samtools / browser", "chr1:3-5", "1-based, closed", RED)]
    s.text(16, yt, "Format", size=11.5, bold=True); s.text(200, yt, "writes these bases as", size=11.5, bold=True); s.text(400, yt, "convention", size=11.5, bold=True)
    for i, (f, w, c, col) in enumerate(rows):
        yy = yt + 22 + i * 20
        s.text(16, yy, f, size=11.5)
        s.text(200, yy, w, size=12, family=MONO, fill=col, bold=True)
        s.text(400, yy, c, size=11.5, fill=col)
    s.text(16, yt + 132, "Length = end − start in BED, but end − start + 1 in 1-based. To convert BED → 1-based: add 1 to start only.", size=11.5)
    s.save("u6-coordinates.svg")

# ---------------------------------------------------------------------------
def sam():
    ref = "CGATTACAGGTCCATGACCTAGGACT"   # reference starting at position 101
    REF0 = 101
    pos = 103
    R = ref[pos - REF0:]
    clip = "TT"
    m1 = list(R[0:6]); m1[3] = "C" if m1[3] != "C" else "G"   # one mismatch inside M
    ins = "G"
    m2 = R[6:11]
    m3 = R[13:17]
    read = clip.upper() + "".join(m1) + ins + m2 + m3
    cigar = "2S6M1I5M2D4M"
    s = SVG(720, 470, "A SAM alignment record")
    s.text(16, 22, "One SAM line: 11 tab-separated fields, then optional tags", size=13, bold=True)
    fields = [("QNAME", "read001"), ("FLAG", "99"), ("RNAME", "chr1"), ("POS", str(pos)), ("MAPQ", "60"), ("CIGAR", cigar),
              ("RNEXT", "="), ("PNEXT", "290"), ("TLEN", "205"), ("SEQ", read), ("QUAL", "IIIIIIIIIIIIIIII??"), ("tags", "NM:i:4")]
    assert len(read) == 18
    xs = [16, 88, 136, 190, 236, 284]
    for i, (k, v) in enumerate(fields[:6]):
        s.text(xs[i], 48, k, size=10.5, fill=GRAY, bold=True)
        s.text(xs[i], 66, v, size=12, family=MONO, bold=True, fill=RED if k in ("FLAG", "POS", "CIGAR") else INK)
    xs2 = [16, 76, 136, 190, 380, 560]
    for i, (k, v) in enumerate(fields[6:]):
        s.text(xs2[i], 92, k, size=10.5, fill=GRAY, bold=True)
        s.text(xs2[i], 110, v, size=12, family=MONO, bold=True)
    s.text(420, 48, "RNEXT/PNEXT/TLEN describe the mate;", size=10.5, fill=GRAY)
    s.text(420, 62, "\"=\" means same chromosome.", size=10.5, fill=GRAY)
    s.text(420, 76, "NM = edit distance to the reference.", size=10.5, fill=GRAY)
    # alignment picture
    y = 160
    s.text(16, y - 18, "The alignment that CIGAR describes", size=12.5, bold=True)
    cw = 17
    x0 = 120
    # columns: build aligned strings
    refrow, readrow = [], []
    refpos = []
    # soft clip columns (no reference)
    cols = []
    for c in clip: cols.append((" ", c, "S", None))
    rp = pos
    for i in range(6): cols.append((R[i], m1[i], "M", rp)); rp += 1
    cols.append(("-", ins, "I", None))
    for i in range(5): cols.append((R[6 + i], m2[i], "M", rp)); rp += 1
    for i in range(2): cols.append((R[11 + i], "-", "D", rp)); rp += 1
    for i in range(4): cols.append((R[13 + i], m3[i], "M", rp)); rp += 1
    # show reference context before
    pre = [(ref[pos - REF0 - 2 + k], pos - 2 + k) for k in range(2)]
    s.text(16, y + 4, "reference", size=11, fill=GRAY); s.text(16, y + 30, "read", size=11, fill=GRAY)
    s.text(16, y + 56, "CIGAR op", size=11, fill=GRAY)
    for j, (rb, qb, op, p) in enumerate(cols):
        x = x0 + j * cw
        if j < 2:
            s.mono(x, y + 4, pre[j][0], cw=cw, size=14, fill=LIGHT)
        else:
            s.mono(x, y + 4, rb, cw=cw, size=14, bold=True, fill=LIGHT if rb == "-" else INK)
        mism = op == "M" and rb != qb
        col = GRAY if op == "S" else (RED if (mism or op == "I") else INK)
        s.mono(x, y + 30, qb, cw=cw, size=14, bold=True, fill=col)
        s.text(x + cw / 2, y + 56, op, size=11, anchor="middle", family=MONO, fill=RED if op in "ID" else (GRAY if op == "S" else INK), bold=True)
        if op == "M" and not mism:
            s.line(x + cw / 2, y + 9, x + cw / 2, y + 17, stroke=LIGHT)
    s.text(x0 + 2 * cw + cw / 2, y - 2 - 10, "", size=1)
    # position labels
    s.line(x0 + 2 * cw + cw / 2, y - 22 + 8, x0 + 2 * cw + cw / 2, y - 10, stroke=RED)
    s.text(x0 + 2 * cw + cw / 2, y - 18 + 4, "", size=1)
    s.text(x0 + 2 * cw + cw / 2 + 4, y - 14 + 0, "", size=1)
    xend = x0 + len(cols) * cw + 12
    s.text(x0 + 2 * cw - 2, y - 2 - 0 - 14 + 0, "", size=1)
    s.text(xend, y + 4, f"POS = {pos}: first aligned reference base (1-based)", size=10.5, fill=RED)
    s.text(xend, y + 30, "gray = soft-clipped (in SEQ, not aligned)", size=10.5, fill=GRAY)
    s.text(xend, y + 44, "red = mismatch or inserted base", size=10.5, fill=RED)
    s.text(xend, y + 56 + 2, "2S 6M 1I 5M 2D 4M", size=11, family=MONO, bold=True)
    # mark POS column
    s.rect(x0 + 2 * cw, y - 12, cw, 50, stroke=RED, sw=1, rx=2, dash="2,2")
    # CIGAR legend
    yc = 262
    s.text(16, yc, "CIGAR operations", size=12.5, bold=True)
    ops = [("M", "aligned (match or mismatch)"), ("I", "insertion in the read"), ("D", "deletion from the read"),
           ("N", "skipped region (intron, RNA-seq)"), ("S", "soft clip (kept in SEQ)"), ("H", "hard clip (removed)")]
    for i, (o, d) in enumerate(ops):
        xx = 16 + (i % 2) * 260; yy = yc + 22 + (i // 2) * 18
        s.text(xx, yy, o, size=12, family=MONO, bold=True)
        s.text(xx + 18, yy, d, size=11)
    # FLAG decomposition
    xf = 540
    s.text(xf, yc, "FLAG 99 = sum of bits", size=12.5, bold=True)
    bits = [(1, "paired", True), (2, "proper pair", True), (4, "unmapped", False), (8, "mate unmapped", False),
            (16, "read reverse strand", False), (32, "mate reverse strand", True), (64, "first in pair", True),
            (128, "second in pair", False), (256, "secondary", False), (1024, "duplicate", False), (2048, "supplementary", False)]
    for i, (b, d, on) in enumerate(bits):
        yy = yc + 20 + i * 15
        s.text(xf + 30, yy, str(b), size=10.5, anchor="end", family=MONO, bold=on, fill=INK if on else LIGHT)
        s.text(xf + 38, yy, d, size=10.5, bold=on, fill=INK if on else LIGHT)
    s.text(xf, yc + 20 + 11 * 15 + 6, "1 + 2 + 32 + 64 = 99", size=11, family=MONO, bold=True, fill=RED)
    assert 1 + 2 + 32 + 64 == 99
    s.text(16, 360, "The read covers reference 103–119: 6 + 5 + 2 + 4 = 17 reference bases", size=11, fill=GRAY)
    s.text(16, 376, "(M, D and N consume reference; M, I and S consume read: 2+6+1+5+4 = 18 = SEQ length).", size=11, fill=GRAY)
    s.save("u6-sam.svg")
    return read, cols

# ---------------------------------------------------------------------------
def vcf():
    s = SVG(720, 352, "Anatomy of a VCF file")
    s.text(16, 22, "VCF: meta lines (##), a header line (#CHROM), then one variant per line", size=13, bold=True)
    meta = ["##fileformat=VCFv4.2", "##reference=GRCh38", "##INFO=<ID=DP,Number=1,Type=Integer,Description=\"Total depth\">",
            "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">"]
    for i, m in enumerate(meta):
        s.text(16, 46 + i * 16, m, size=11, family=MONO, fill=GRAY)
    cols = ["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT", "tumor", "normal"]
    xs = [16, 76, 160, 262, 304, 346, 392, 448, 524, 584, 646]
    recs = [["chr1", "1000100", ".", "G", "GT", "52", "PASS", "DP=31", "GT", "0/1", "0/0"],
            ["chr1", "1000200", ".", "CGC", "C", "47", "PASS", "DP=28", "GT", "0/1", "0/1"],
            ["chr7", "140753336", "rs113488022", "A", "T", "60", "PASS", "DP=40", "GT", "0/1", "0/0"],
            ["chr17", "7676154", "rs1042522", "G", "C", "99", "PASS", "DP=55", "GT", "1|1", "1|1"]]
    y = 128
    s.rect(12, y - 14, 696, 20, fill=GRAY_T, stroke="none")
    for x, c in zip(xs, cols): s.text(x, y, c, size=11, family=MONO, bold=True)
    for i, r in enumerate(recs):
        yy = y + 22 + i * 20
        for j, (x, v) in enumerate(zip(xs, r)):
            col = RED if j in (3, 4) else (BLUE if j in (9, 10) else INK)
            s.text(x, yy, v, size=11, family=MONO, fill=col, bold=j in (1, 3, 4, 9, 10))
    yb = y + 22 + 4 * 20 - 4
    s.bracket(16, 440, yb, "8 fixed columns", size=10.5)
    s.bracket(524, 704, yb, "FORMAT + one column per sample", size=10.5)
    yn = yb + 40
    notes = [("row 1", "insertion of T after position 1,000,100 (indels repeat the base before them)"),
             ("row 2", "deletion of GC after position 1,000,200"),
             ("row 3", "BRAF V600E on GRCh38 (+ strand: A>T); POS is 1-based"),
             ("row 4", "TP53 P72R; 1|1 = phased homozygous ALT. 0/0 ref/ref, 0/1 het, 1/1 hom ALT")]
    for i, (a, b) in enumerate(notes):
        s.text(16, yn + i * 17, a, size=11, bold=True)
        s.text(64, yn + i * 17, b, size=11)
    s.save("u6-vcf.svg")

# ---------------------------------------------------------------------------
def workflows():
    lanes = [("Bulk RNA-seq", [("extract RNA", "poly(A) select"), ("make cDNA", "reverse\ntranscriptase"), ("sequence", "FASTQ"),
                               ("align", "STAR → BAM\nor salmon"), ("count", "gene × sample\ncounts"), ("test", "DESeq2:\nlog2FC, FDR")]),
             ("scRNA-seq", [("droplets", "cell barcode\n+ UMI"), ("library", "cDNA"), ("sequence", "FASTQ"),
                            ("Cell Ranger", "or STARsolo\n→ BAM"), ("count", "cell × gene\n.h5ad"), ("analyze", "QC, cluster\n(scanpy)")]),
             ("ChIP-seq", [("crosslink", "shear\nchromatin"), ("pull down", "antibody to a\nTF or mark"), ("sequence", "FASTQ"),
                           ("align", "Bowtie2 / BWA\n→ BAM"), ("call peaks", "MACS2 vs.\ninput control"), ("peaks", "narrowPeak\n(BED)")]),
             ("ATAC-seq", [("nuclei", "isolate"), ("Tn5", "inserts adapters\ninto open DNA"), ("sequence", "FASTQ"),
                           ("align", "→ BAM"), ("call peaks", "MACS2"), ("peaks", "BED: open\nchromatin")])]
    lh = 72
    s = SVG(720, 48 + lh * len(lanes) + 30, "Sequencing assay workflows and the files they produce")
    s.text(16, 22, "From sample to file: four common assays", size=13, bold=True)
    bw, gap, x0 = 96, 6, 100
    s.text(x0 + bw + gap / 2, 42, "wet lab", size=10.5, fill=GRAY, italic=True, anchor="middle")
    s.text(x0 + 2.5 * (bw + gap) - gap / 2, 42, "sequencer", size=10.5, fill=GRAY, italic=True, anchor="middle")
    s.text(x0 + 4.5 * (bw + gap) - gap / 2, 42, "computation", size=10.5, fill=GRAY, italic=True, anchor="middle")
    for i, (name, steps) in enumerate(lanes):
        y = 50 + i * lh
        s.text(16, y + 34, name, size=12, bold=True)
        for j, (a, b) in enumerate(steps):
            x = x0 + j * (bw + gap)
            fill = GREEN_T if j < 2 else (GRAY_T if j == 2 else BLUE_T)
            s.rect(x, y + 4, bw, 58, fill=fill, stroke=RULE, rx=3)
            s.text(x + bw / 2, y + 22, a, size=11, anchor="middle", bold=True)
            for k, line in enumerate(b.split("\n")):
                s.text(x + bw / 2, y + 38 + k * 13, line, size=10, anchor="middle", fill=GRAY)
            if j: s.arrow(x - gap + 0.5, y + 33, x - 0.5, y + 33, sw=1, head=4)
    s.text(16, 48 + lh * len(lanes) + 18, "Green = wet lab, gray = sequencer, blue = computation. The FASTQ → BAM → table pattern is shared by almost every assay.", size=10.5, fill=GRAY)
    s.save("u6-workflows.svg")

# ---------------------------------------------------------------------------
def anndata():
    s = SVG(720, 420, "AnnData layout: cells × genes")
    s.text(16, 22, "AnnData (.h5ad): one object, aligned tables", size=13, bold=True)
    genes = ["CD3E", "MS4A1", "LYZ", "NKG7", "PPBP"]
    cells = ["AAACATACAACCAC-1", "AAACATTGAGCTAC-1", "AAACATTGATCAGC-1", "AAACCGTGCTTCCG-1", "AAACCGTGTATGCG-1"]
    X = [[2, 0, 0, 0, 0], [0, 4, 1, 0, 0], [1, 0, 0, 0, 0], [0, 0, 18, 0, 0], [0, 0, 0, 9, 0]]
    cw, rh = 52, 26
    mx, my = 300, 132   # matrix top-left
    # layers behind X
    for k in (2, 1):
        s.rect(mx + k * 8, my - k * 8, cw * 5, rh * 5, fill="#fff", stroke=LIGHT, dash="3,2")
    s.rect(mx, my, cw * 5, rh * 5, fill=BLUE_T, stroke=INK, sw=1.4)
    for i in range(5):
        for j in range(5):
            v = X[i][j]
            s.text(mx + j * cw + cw / 2, my + i * rh + 17, str(v) if v else "0", size=11.5, anchor="middle", fill=INK if v else LIGHT, family=MONO)
    s.text(mx + cw * 2.5, my + rh * 5 + 18, "adata.X", size=12, anchor="middle", family=MONO, bold=True)
    s.text(mx + cw * 2.5, my + rh * 5 + 33, "n_obs × n_vars, mostly zeros (sparse)", size=10.5, anchor="middle", fill=GRAY)
    # var on top
    vy = my - 64
    s.rect(mx, vy, cw * 5, 48, fill=GREEN_T, stroke=INK)
    for j, g in enumerate(genes):
        s.text(mx + j * cw + cw / 2, vy + 18, g, size=10.5, anchor="middle", bold=True)
        s.text(mx + j * cw + cw / 2, vy + 36, "ENSG…", size=9.5, anchor="middle", fill=GRAY, family=MONO)
    s.text(mx - 8, vy + 18, "var_names", size=10, anchor="end", fill=GRAY, family=MONO)
    s.text(mx - 8, vy + 36, "gene_ids", size=10, anchor="end", fill=GRAY, family=MONO)
    s.text(mx + cw * 2.5, vy - 8, "adata.var: one row per gene (columns of X)", size=11, anchor="middle", family=SANS, bold=True)
    # obs on left
    ox = 16
    s.rect(ox + 132, my, 140, rh * 5, fill=GREEN_T, stroke=INK)
    types = ["T cell", "B cell", "T cell", "monocyte", "NK cell"]
    donors = ["d1", "d1", "d2", "d2", "d1"]
    for i, c in enumerate(cells):
        s.text(ox + 128, my + i * rh + 17, c, size=9.5, anchor="end", family=MONO, fill=GRAY)
        s.text(ox + 140, my + i * rh + 17, types[i], size=10.5)
        s.text(ox + 218, my + i * rh + 17, donors[i], size=10.5)
    s.text(ox + 140, my - 6, "cell_type", size=10, family=MONO, fill=GRAY)
    s.text(ox + 218, my - 6, "donor", size=10, family=MONO, fill=GRAY)
    s.text(ox + 202, my + rh * 5 + 18, "adata.obs", size=12, anchor="middle", family=MONO, bold=True)
    s.text(ox + 202, my + rh * 5 + 33, "one row per cell (rows of X)", size=10.5, anchor="middle", fill=GRAY)
    s.text(ox + 70, my + rh * 5 + 18, "obs_names", size=10, anchor="middle", family=MONO, fill=GRAY)
    s.text(ox + 70, my + rh * 5 + 33, "(cell barcodes)", size=10, anchor="middle", fill=GRAY)
    # obsm on right
    rx = mx + cw * 5 + 30
    s.rect(rx, my, 56, rh * 5, fill=GRAY_T, stroke=INK)
    s.rect(rx + 62, my, 56, rh * 5, fill=GRAY_T, stroke=INK)
    s.text(rx + 28, my - 6, "X_pca", size=10, anchor="middle", family=MONO, fill=GRAY)
    s.text(rx + 90, my - 6, "X_umap", size=10, anchor="middle", family=MONO, fill=GRAY)
    s.text(rx + 28, my + 66, "50 cols", size=9.5, anchor="middle", fill=GRAY)
    s.text(rx + 90, my + 66, "2 cols", size=9.5, anchor="middle", fill=GRAY)
    s.text(rx + 59, my + rh * 5 + 18, "adata.obsm", size=12, anchor="middle", family=MONO, bold=True)
    s.text(rx + 59, my + rh * 5 + 33, "per-cell embeddings", size=10.5, anchor="middle", fill=GRAY)
    # uns
    s.rect(16, 328, 300, 28, fill="#fff", stroke=INK, dash="4,3")
    s.text(26, 347, "adata.uns", size=12, family=MONO, bold=True)
    s.text(110, 347, "everything else (colors, parameters)", size=10.5, fill=GRAY)
    s.text(16, 396, "Dashed sheets behind X = adata.layers: same shape as X, e.g. raw counts kept next to normalized values.", size=10.5, fill=GRAY)
    s.text(16, 380, "Rows of X, obs and obsm line up (cells); columns of X line up with rows of var (genes).", size=10.5, fill=INK)
    s.text(16, 412, "AnnData is cells × genes; 10x MTX files store genes × cells.", size=10.5, fill=RED)
    s.save("u6-anndata.svg")

if __name__ == "__main__":
    fastq(); coordinates(); sam(); vcf(); workflows(); anndata()
