from figlib import *

def chip(s, x, y, label, fill=BLUE_T, size=12, stroke=RULE):
    w = tw(label, size) * 1.12 + 16
    s.rect(x, y - 13, w, 22, fill=fill, stroke=stroke, rx=3)
    s.text(x + w / 2, y + 3, label, size=size, anchor="middle")
    return x + w + 6

def database_map():
    rows = [("What is this gene?", ["NCBI Gene", "Ensembl / GENCODE", "HGNC"]),
            ("What is at this genome position?", ["UCSC Genome Browser", "Ensembl"]),
            ("What is the protein's function and domains?", ["UniProt", "InterPro / Pfam"]),
            ("What does the protein look like in 3D?", ["PDB (measured)", "AlphaFold DB (predicted)"]),
            ("Where is the gene expressed?", ["GTEx", "Human Protein Atlas", "CELLxGENE"]),
            ("How common is this variant?", ["gnomAD", "dbSNP"]),
            ("Does this variant cause disease?", ["ClinVar", "OMIM"]),
            ("What is mutated in tumors?", ["COSMIC", "cBioPortal", "TCGA"]),
            ("Which pathways and interactions?", ["GO", "KEGG", "Reactome", "STRING", "BioGRID"]),
            ("Where are a paper's data?", ["GEO (processed)", "SRA / ENA (raw reads)"]),
            ("What do cells depend on, what binds it?", ["DepMap", "ChEMBL", "PubChem"]),
            ("Which DNA is regulatory?", ["ENCODE"])]
    rh = 30
    s = SVG(720, 40 + rh * len(rows) + 6, "A map from biological questions to databases")
    s.text(16, 22, "Question", size=12.5, bold=True); s.text(318, 22, "Go-to resources", size=12.5, bold=True)
    for i, (q, dbs) in enumerate(rows):
        y = 48 + i * rh
        if i % 2 == 0: s.rect(8, y - 16, 704, rh, fill="#fafafa", stroke="none")
        s.text(16, y + 3, q, size=12)
        s.arrow(296, y - 1, 312, y - 1, stroke=LIGHT, sw=1, head=5)
        x = 318
        for j, d in enumerate(dbs):
            x = chip(s, x, y, d, fill=BLUE_T if j == 0 else GRAY_T)
    s.save("u3-database-map.svg")

def geo_sra():
    s = SVG(720, 300, "How GEO and SRA accessions nest")
    s.text(16, 22, "One study, three linked ID systems (example IDs)", size=13, bold=True)
    cols = {"GEO (processed data)": 146, "SRA (raw reads)": 412, "BioProject / BioSample": 630}
    for k, x in cols.items(): s.text(x, 48, k, size=12, anchor="middle", bold=True, fill=GRAY)
    def node(x, y, lab, sub, fill=BLUE_T):
        w = 124
        s.rect(x - w / 2, y - 16, w, 34, fill=fill, stroke=INK, rx=3)
        s.text(x, y - 1, lab, size=12, anchor="middle", family=MONO, bold=True)
        s.text(x, y + 13, sub, size=10, anchor="middle", fill=GRAY)
    yS, yX, yR = 84, 160, 236
    node(146, yS, "GSE150000", "series = study")
    node(412, yS, "SRP260000", "study")
    node(630, yS, "PRJNA630000", "BioProject", fill=GRAY_T)
    gsms = [(80, "GSM4500001"), (212, "GSM4500002")]
    srxs = [(345, "SRX8300001"), (480, "SRX8300002")]
    for (x, l) in gsms: node(x, yX, l, "sample", fill=BLUE_T); s.line(146, yS + 18, x, yX - 16, stroke=GRAY)
    for (x, l) in srxs: node(x, yX, l, "experiment"); s.line(412, yS + 18, x, yX - 16, stroke=GRAY)
    node(630, yX, "SAMN14800001", "BioSample (+ SRS)", fill=GRAY_T)
    runs = [(290, "SRR11700001"), (420, "SRR11700002"), (560, "SRR11700003")]
    for (x, l), parent in zip(runs, [345, 345, 480]):
        node(x, yR, l, "run = FASTQ files", fill=GREEN_T); s.line(parent, yX + 18, x, yR - 16, stroke=GRAY)
    # cross links
    s.line(208, yS, 350, yS, stroke=BLUE, dash="4,3", sw=1.2)
    s.line(474, yS, 568, yS, stroke=BLUE, dash="4,3", sw=1.2)
    s.curve_arrow([(212, yX + 18), (278, yX + 46), (345, yX + 18)], stroke=BLUE, kind="none", dash="4,3")
    s.line(542, yX, 568, yX, stroke=BLUE, dash="4,3", sw=1.2)
    s.text(16, 284, "Dashed = the same entity in two archives. GEO holds processed tables; follow GSM → SRX → SRR to download reads.", size=11.5, fill=GRAY)
    s.save("u3-geo-sra.svg")

def go_dag():
    s = SVG(720, 330, "A fragment of the Gene Ontology graph")
    s.text(16, 22, "Gene Ontology: a directed acyclic graph (Biological Process fragment)", size=13, bold=True)
    N = {}
    def node(key, x, y, name, gid, hl=False):
        w = max(tw(name, 12) * 1.12, tw(gid, 10.5) * 1.12) + 20
        s.rect(x - w / 2, y - 16, w, 34, fill=GREEN_T if hl else "#fff", stroke=INK, rx=3)
        s.text(x, y - 1, name, size=12, anchor="middle", bold=hl)
        s.text(x, y + 13, gid, size=10.5, anchor="middle", fill=GRAY, family=MONO)
        N[key] = (x, y, w)
    node("bp", 360, 58, "biological_process", "GO:0008150")
    node("cp", 360, 118, "cellular process", "GO:0009987")
    node("cd", 200, 178, "cell death", "GO:0008219")
    node("st", 540, 178, "signal transduction", "GO:0007165")
    node("pcd", 200, 238, "programmed cell death", "GO:0012501")
    node("ap", 200, 298, "apoptotic process", "GO:0006915", hl=True)
    node("asp", 520, 248, "apoptotic signaling pathway", "GO:0097190")
    node("int", 430, 308, "intrinsic … pathway", "GO:0097193")
    node("ext", 620, 308, "extrinsic … pathway", "GO:0097191")
    def edge(child, parent, rel="is_a"):
        cx, cy, _ = N[child]; px, py, _ = N[parent]
        col = INK if rel == "is_a" else RED
        if cy > py:
            s.arrow(cx, cy - 17, px + (cx - px) * 0.25, py + 18, stroke=col, sw=1.1, head=6, dash=None if rel == "is_a" else "4,3")
        else:
            s.arrow(cx - N[child][2] / 2, cy, px + N[parent][2] / 2, py, stroke=col, sw=1.1, head=6, dash="4,3")
    edge("cp", "bp"); edge("cd", "cp"); edge("st", "cp"); edge("pcd", "cd"); edge("ap", "pcd")
    edge("asp", "st"); edge("int", "asp"); edge("ext", "asp")
    # part_of: apoptotic signaling pathway -> apoptotic process
    ax, ay, aw = N["asp"]; px, py, pw = N["ap"]
    s.arrow(ax - aw / 2, ay + 6, px + pw / 2, py - 4, stroke=RED, sw=1.1, head=6, dash="4,3")
    s.text(16, 58, "arrows point child → parent", size=11, fill=GRAY)
    s.line(16, 80, 40, 80); s.poly([(46, 80), (39, 77), (39, 83)]); s.text(52, 84, "is_a", size=11)
    s.line(16, 100, 40, 100, stroke=RED, dash="4,3"); s.poly([(46, 100), (39, 97), (39, 103)], fill=RED); s.text(52, 104, "part_of", size=11, fill=RED)
    s.text(16, 128, "A term can have", size=11, fill=GRAY); s.text(16, 142, "several parents;", size=11, fill=GRAY)
    s.text(16, 156, "genes annotated to", size=11, fill=GRAY); s.text(16, 170, "a term count for", size=11, fill=GRAY)
    s.text(16, 184, "all its ancestors.", size=11, fill=GRAY)
    s.save("u3-go-dag.svg")

if __name__ == "__main__":
    database_map(); geo_sra(); go_dag()
