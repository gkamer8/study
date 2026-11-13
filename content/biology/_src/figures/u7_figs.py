import math, random
from figlib import *

def splits():
    s = SVG(720, 320, "Random, sequence-identity clustered and temporal splits")
    clusters = [(60, 90), (150, 80), (100, 160), (175, 165), (55, 225), (150, 235)]
    rng = random.Random(3)
    pts = []
    for ci, (cx, cy) in enumerate(clusters):
        for k in range(3):
            a = 2 * math.pi * k / 3 + ci
            pts.append((ci, cx + 14 * math.cos(a), cy + 14 * math.sin(a)))
    def dot(x, y, test):
        if test: s.circle(x, y, 6, fill=RED, stroke=RED)
        else: s.circle(x, y, 6, fill=BLUE_T, stroke=BLUE)
    titles = [("Random split", "test proteins have close", "relatives in training: leaky"),
              ("Clustered split (<30% identity)", "whole homolog clusters go", "to test: honest"),
              ("Temporal split", "train before a date,", "test after it (CASP-style)")]
    for p, (t, a, b) in enumerate(titles):
        ox = p * 240
        if p: s.line(ox, 12, ox, 258, stroke=RULE)
        s.text(ox + 16, 22, t, size=12.5, bold=True)
        s.text(ox + 16, 272, a, size=10.5, fill=GRAY); s.text(ox + 16, 286, b, size=10.5, fill=GRAY)
    # random
    random_test = {1, 5, 9, 13, 15}
    for p in (0, 1):
        ox = p * 240
        for ci, (cx, cy) in enumerate(clusters):
            s.circle(ox + cx, cy, 25, fill="none", stroke=LIGHT, sw=1)
        for i, (ci, x, y) in enumerate(pts):
            test = (i in random_test) if p == 0 else (ci in (1, 4))
            dot(ox + x, y, test)
    # temporal
    ox = 480
    years = list(range(2014, 2025))
    ax0, ax1, ay = ox + 20, ox + 220, 230
    s.line(ax0, ay, ax1, ay, stroke=INK)
    for k, yv in enumerate(years[::2]):
        x = ax0 + (yv - 2014) / 10 * (ax1 - ax0)
        s.line(x, ay, x, ay + 4); s.text(x, ay + 16, str(yv), size=9.5, anchor="middle", fill=GRAY)
    cut = ax0 + (2021.5 - 2014) / 10 * (ax1 - ax0)
    s.line(cut, 44, cut, ay, stroke=INK, dash="4,3")
    s.text(cut, 40, "cutoff", size=10, anchor="middle")
    for i in range(18):
        yr = 2014 + rng.random() * 10
        x = ax0 + (yr - 2014) / 10 * (ax1 - ax0)
        y = 60 + rng.random() * 150
        if abs(x - cut) < 12:                      # keep every point clearly on one side
            x = cut + (12 if x > cut else -12)
        dot(x, y, x > cut)
    s.text(ox + 20, 250, "", size=1)
    # legend
    s.circle(22, 306, 6, fill=BLUE_T, stroke=BLUE); s.text(34, 310, "training example", size=10.5)
    s.circle(160, 306, 6, fill=RED, stroke=RED); s.text(172, 310, "test example", size=10.5)
    s.circle(276, 306, 10, fill="none", stroke=LIGHT); s.text(292, 310, "cluster of homologs (similar sequences)", size=10.5)
    s.save("u7-splits.svg")

def tokenization():
    s = SVG(720, 524, "How proteins, DNA and single cells are tokenized")
    s.text(16, 22, "What becomes a token", size=13, bold=True)
    def tok(x, y, t, fill=BLUE_T, size=12, family=MONO, w=None):
        w = w or max(22, tw(t, size) * (1.25 if family == MONO else 1.12) + 10)
        s.rect(x, y - 15, w, 22, fill=fill, stroke=RULE, rx=3)
        s.text(x + w / 2, y + 1, t, size=size, anchor="middle", family=family, bold=True)
        return x + w + 4
    X0 = 222
    # protein
    y = 54
    s.text(16, y, "Protein (ESM-2)", size=12, bold=True); s.text(16, y + 14, "one token per amino acid", size=10.5, fill=GRAY)
    x = X0
    x = tok(x, y, "<cls>", fill=GRAY_T)
    for c in "MKTAYIAKQR": x = tok(x, y, c)
    x = tok(x, y, "<eos>", fill=GRAY_T)
    # DNA one-hot
    y = 112
    seq = "ACGTTA"
    s.text(16, y, "DNA, one-hot", size=12, bold=True); s.text(16, y + 14, "Enformer, Borzoi; single-base", size=10.5, fill=GRAY)
    s.text(16, y + 28, "tokens in HyenaDNA, Evo", size=10.5, fill=GRAY)
    cw = 24
    for j, b in enumerate(seq):
        s.text(X0 + 30 + j * cw + cw / 2, y - 2, b, size=12, anchor="middle", family=MONO, bold=True)
    for i, base in enumerate("ACGT"):
        s.text(X0 + 20, y + 16 + i * 16, base, size=10.5, anchor="end", family=MONO, fill=GRAY)
        for j, b in enumerate(seq):
            v = 1 if b == base else 0
            s.rect(X0 + 30 + j * cw, y + 4 + i * 16, cw, 16, fill=BLUE_T if v else "#fff", stroke=RULE)
            s.text(X0 + 30 + j * cw + cw / 2, y + 16 + i * 16, str(v), size=10, anchor="middle", family=MONO, fill=INK if v else LIGHT)
    s.text(X0 + 30 + 6 * cw + 14, y + 40, "each base = a 4-dim vector with a single 1", size=10.5, fill=GRAY)
    # overlapping kmers
    y = 210
    seq = "ACGTTAGC"
    s.text(16, y, "DNA, overlapping 3-mers", size=12, bold=True); s.text(16, y + 14, "DNABERT (k = 3–6)", size=10.5, fill=GRAY)
    cw3 = 16
    s.mono(X0, y, seq, cw=cw3, size=13, bold=True)
    for k in range(len(seq) - 2):
        tok(X0 + k * cw3 + 1, y + 24 + (k % 3) * 24, seq[k:k + 3], w=3 * cw3 - 2, size=11)
    s.text(X0 + 8 * cw3 + 14, y + 48, "one token starts at every base; neighbors share 2 of 3 bases", size=10.5, fill=GRAY)
    # nonoverlapping 6-mers
    y = 318
    seq = "ACGTTAGCCATG"
    s.text(16, y, "DNA, non-overlapping 6-mers", size=12, bold=True); s.text(16, y + 14, "Nucleotide Transformer", size=10.5, fill=GRAY)
    x = tok(X0, y, seq[:6]); x = tok(x, y, seq[6:])
    # BPE
    y = 362
    s.text(16, y, "DNA, byte-pair encoding", size=12, bold=True); s.text(16, y + 14, "DNABERT-2; learned pieces", size=10.5, fill=GRAY)
    x = X0
    for t in ["ACG", "TTAGC", "CATG", "GA", "TTTT"]: x = tok(x, y, t)
    s.text(x + 6, y + 1, "(illustrative; pieces vary in length)", size=10.5, fill=GRAY)
    # single cell
    y = 412
    s.text(16, y, "Single cell (Geneformer)", size=12, bold=True); s.text(16, y + 14, "genes ranked by expression", size=10.5, fill=GRAY)
    s.text(16, y + 28, "relative to the corpus; values dropped", size=10.5, fill=GRAY)
    x = X0
    for g in ["LYZ", "S100A9", "CD14", "FCN1", "VCAN", "…"]: x = tok(x, y, g, fill=GREEN_T, family=SANS, size=11.5)
    s.text(x + 4, y + 1, "first = highest relative expression", size=10.5, fill=GRAY)
    y = 470
    s.text(16, y, "Single cell (scGPT)", size=12, bold=True); s.text(16, y + 14, "gene token + binned value", size=10.5, fill=GRAY)
    x = X0
    for g, b in [("LYZ", "bin 5"), ("CD14", "bin 3"), ("FCN1", "bin 2"), ("CD3E", "bin 0")]:
        x0 = x
        x = tok(x, y, g, fill=GREEN_T, family=SANS, size=11.5, w=56)
        s.text(x0 + 28, y + 20, b, size=10, anchor="middle", fill=GRAY)
    s.text(16, 516, "Illustrative inputs. Sequence models also add special tokens (start, end, mask); context length limits how much sequence fits.", size=10.5, fill=GRAY)
    s.save("u7-tokenization.svg")

def masked_marginal():
    s = SVG(720, 300, "Zero-shot variant scoring with a masked protein language model")
    s.text(16, 22, "Masked-marginal scoring of the variant E6K (illustrative numbers)", size=13, bold=True)
    seq = "MKTAYEAKQR"
    x0, cw, y = 40, 26, 64
    for i, c in enumerate(seq):
        t = "<mask>" if i == 5 else c
        w = 58 if i == 5 else cw - 2
        xx = x0 + i * cw + (0 if i <= 5 else 34)
        s.rect(xx, y - 16, w, 24, fill=RED_T if i == 5 else BLUE_T, stroke=RULE, rx=3)
        s.text(xx + w / 2, y + 1, t, size=12, anchor="middle", family=MONO, bold=True)
        s.text(xx + w / 2, y + 22, str(i + 1), size=9.5, anchor="middle", fill=GRAY)
    s.text(x0 + 11 * cw + 50, y + 1, "hide position 6 (wild type E)", size=11, fill=GRAY)
    # probability bars
    probs = {"E": 0.42, "D": 0.18, "Q": 0.09, "K": 0.06, "A": 0.05, "S": 0.05, "R": 0.04, "N": 0.03, "T": 0.02, "G": 0.02}
    rest = 1 - sum(probs.values())
    bx, by, bh = 60, 120, 110
    s.text(16, by - 8, "model's predicted distribution at position 6", size=11.5, bold=True)
    keys = list(probs) + ["other 10"]
    vals = list(probs.values()) + [rest]
    for k, (a, p) in enumerate(zip(keys, vals)):
        x = bx + k * 34
        h = p / 0.45 * bh
        col = BLUE if a == "E" else (RED if a == "K" else LIGHT)
        s.rect(x, by + bh - h + 10, 22, h, fill=col, stroke="none")
        s.text(x + 11, by + bh + 26, a, size=11 if len(a) == 1 else 9.5, anchor="middle", family=MONO if len(a) == 1 else SANS, bold=len(a) == 1)
        s.text(x + 11, by + bh - h + 4, f"{p:.2f}", size=9.5, anchor="middle", fill=GRAY)
    s.line(bx - 6, by + bh + 10, bx + len(keys) * 34, by + bh + 10, stroke=INK)
    # score
    sx = 470
    sc = math.log(probs["K"]) - math.log(probs["E"])
    s.text(sx, 130, "score = log p(mutant) − log p(wild type)", size=12, bold=True)
    s.text(sx, 154, f"= log {probs['K']:.2f} − log {probs['E']:.2f}", size=12, family=SANS)
    s.text(sx, 178, f"= −{abs(sc):.2f}   (natural log)", size=12, fill=RED, bold=True)
    s.text(sx, 210, "Negative: the model finds K less", size=11, fill=GRAY)
    s.text(sx, 224, "plausible than E here, so it predicts", size=11, fill=GRAY)
    s.text(sx, 238, "the mutation is likely damaging.", size=11, fill=GRAY)
    s.text(16, 290, "Benchmarks (ProteinGym) compare such scores with measured DMS fitness using Spearman's ρ, per assay.", size=10.5, fill=GRAY)
    s.save("u7-masked-marginal.svg")
    return sc

if __name__ == "__main__":
    splits(); tokenization(); print(masked_marginal())
