from common import build
lesson = r"""
## The genome as a data structure

The human nuclear genome is about **3.1 billion base pairs** (haploid), split across 22 autosomes plus X and Y, with a separate ~16.6 kb circular **mitochondrial genome** (chrM). Each cell has two copies of each autosome (diploid). DNA is double-stranded and antiparallel: one strand runs 5'→3', its complement runs the other way. Reference genomes store only one strand (the **forward/plus** strand); a gene can sit on either strand. TP53, for example, is on the minus strand of chromosome 17, so its mRNA is the reverse complement of the reference sequence there.

Only about **1.5%** of the genome codes for protein. GENCODE annotates roughly **20,000 protein-coding genes** and a larger number of non-coding genes (lncRNAs, microRNAs, snRNAs, pseudogenes), about 60,000 genes in total. The rest is introns, regulatory elements, repeats (about half the genome is transposon-derived, e.g. Alu and LINE-1 elements), and sequence of unclear function.

Chromosome positions are given either as coordinates (chr17:7,668,402) or as **cytogenetic bands**: 17p13.1 means chromosome 17, short arm (**p**), region 1, band 3, sub-band 1. The long arm is **q**.

## Anatomy of a protein-coding gene

Reading 5'→3' along the gene's own strand:

1. **Promoter**: sequence just upstream of the **transcription start site (TSS)** where RNA polymerase II and general transcription factors assemble. Many human promoters sit in **CpG islands**; some have a TATA box ~25–30 bp upstream of the TSS.
2. **Exons and introns**: the gene is transcribed into a pre-mRNA containing both. Introns are removed by **splicing**; exons are joined. Human genes average roughly 8–10 exons; introns are often far longer than exons.
3. **5' UTR**: the exonic sequence between the TSS and the start codon. Transcribed, not translated.
4. **Coding sequence (CDS)**: from the **start codon (ATG, methionine)** to a **stop codon (TAA, TAG, TGA)**. It can span many exons.
5. **3' UTR**: after the stop codon; contains microRNA binding sites and the **polyadenylation signal (AATAAA)**, after which the transcript is cleaved and a poly(A) tail added.

The mature mRNA also gets a **5' cap** (7-methylguanosine). Note the difference between exons and CDS: the first and last exons usually contain UTR sequence, so "exon" ≠ "coding".

**Enhancers** are regulatory elements that boost transcription and can sit tens to hundreds of kilobases away, upstream, downstream, or inside introns. They act by DNA looping, usually within **topologically associating domains (TADs)** bounded by CTCF and cohesin. **Transcription factors (TFs)** bind short motifs (6–12 bp) in promoters and enhancers. Most disease-associated GWAS variants fall in non-coding regions, frequently in enhancers, which is why genomics models (Enformer, Borzoi, AlphaGenome-style models) try to predict regulatory activity from sequence.

## Transcripts, isoforms, splicing

One gene usually produces **several transcripts (isoforms)** through alternative promoters, alternative splicing (exon skipping, alternative 5'/3' splice sites, intron retention, mutually exclusive exons), and alternative polyadenylation. Most multi-exon human genes are alternatively spliced. Databases pick a representative: **MANE Select** is the one transcript per protein-coding gene that NCBI RefSeq and Ensembl agreed to match exactly, and it is now the default for clinical variant reporting.

Introns nearly always start with **GT** and end with **AG** (GU…AG in RNA), with a **branch point** A and a **polypyrimidine tract** upstream of the 3' site. The **spliceosome** (snRNPs plus proteins) does the cutting. Variants at the ±1/±2 positions of an intron (canonical splice sites) usually break splicing. SpliceAI is the standard ML model for predicting this.

## Codons and reading frames

Translation reads the mRNA in non-overlapping triplets. There are 64 codons: 61 encode the 20 amino acids and 3 are stops. The code is **degenerate**: most amino acids have several codons, and the third position is often "wobble". Therefore:

- **Synonymous** (silent) variant: codon changes, amino acid doesn't.
- **Missense**: amino acid changes.
- **Nonsense**: creates a premature stop. Transcripts with a premature stop more than ~50 nt upstream of the last exon-exon junction are typically degraded by **nonsense-mediated decay (NMD)**.
- **Frameshift**: insertion or deletion not divisible by 3, scrambling everything downstream.
- **In-frame indel**: multiple of 3, adds/removes amino acids.

Any DNA sequence has **six possible reading frames** (three per strand). An **open reading frame (ORF)** is a stretch from ATG to stop with no internal stop. The start codon usually sits in a **Kozak context** (gccRccATGG).

## From protein to function

Ribosomes translate mRNA into a polypeptide N-terminus to C-terminus. Proteins destined for secretion or membranes carry an N-terminal **signal peptide** that is cleaved. **Post-translational modifications (PTMs)** then change activity, localization, or lifetime:

- **Phosphorylation** on Ser, Thr, Tyr by kinases (removed by phosphatases): the main currency of signaling.
- **Ubiquitination** on Lys by E3 ligases; K48-linked chains typically target proteins to the proteasome.
- **Acetylation** and **methylation** on Lys (and Arg for methylation), especially histone tails (H3K27ac, H3K4me3).
- **Glycosylation**: N-linked on Asn in the N-X-S/T motif (X ≠ Pro), O-linked on Ser/Thr.
- **Disulfide bonds** between Cys residues, typical of extracellular proteins.

## Not everything is protein-coding

Know these RNA classes: **mRNA**; **rRNA** and **tRNA** (translation machinery); **miRNA** (~22 nt, represses target mRNAs via 3' UTR); **lncRNA** (>200 nt, non-coding, e.g. XIST); **snRNA** (spliceosome). Pseudogenes are gene copies that lost function, which can confuse read mapping.

## How you'll see this in a paper

- "We used the canonical/MANE Select transcript": they picked one isoform per gene to define coordinates and protein sequence.
- "Variants were annotated with VEP as missense, synonymous, stop-gained, splice-donor…": these are the consequence categories above.
- "Input: 196 kb of sequence centered on the TSS" (Enformer): models need long context because enhancers are distal.
- "Reads were assigned to genes using GENCODE v44": the annotation version decides which exons count.
- Protein language models train on UniProt protein sequences, which are already translated and spliced; DNA models see introns, UTRs and intergenic sequence.
"""
cards = [
("recall","Roughly how large is the haploid human nuclear genome?","~3.1 billion base pairs (3.1 Gb)",["genome"]),
("recall","Approximately how many protein-coding genes do humans have?","~20,000 (≈19–20k in GENCODE)",["genome","genes"]),
("cloze","Only about ___% of the human genome is protein-coding sequence.","~1.5%",["genome"]),
("identify","Decode the cytogenetic band 17p13.1.","Chromosome 17, short arm (p), region 1, band 3, sub-band 1",["genome","coordinates"]),
("recall","p arm vs q arm?","p = short arm; q = long arm",["genome","coordinates"]),
("recall","What does a reference genome store regarding strands?","Only the forward (+) strand; minus-strand genes are read as the reverse complement",["genome","strand"]),
("recall","What is the TSS?","Transcription start site: first nucleotide transcribed into RNA",["gene-structure"]),
("recall","Order the parts of a mature protein-coding mRNA 5'→3'.","5' cap – 5' UTR – CDS (ATG…stop) – 3' UTR – poly(A) tail",["gene-structure","mRNA"]),
("apply","An exon contains both 5' UTR and the start codon. Is all of that exon 'coding'?","No. Exons ≠ CDS; first/last exons often contain UTR sequence that is not translated",["gene-structure"]),
("recall","What is a promoter?","Region at/just upstream of the TSS where RNA Pol II and general TFs assemble to start transcription",["regulation"]),
("recall","What is an enhancer and how does it act at a distance?","A TF-bound regulatory element that increases transcription; acts via DNA looping, often 10s–100s of kb away, usually within a TAD",["regulation"]),
("recall","What bounds TADs?","CTCF binding sites plus cohesin (loop extrusion)",["regulation","3D-genome"]),
("recall","What are CpG islands and where are they common?","CG-dinucleotide-rich stretches, typically unmethylated, found at many human promoters",["regulation"]),
("recall","Where do most GWAS hits fall?","Non-coding regions, often regulatory elements like enhancers",["regulation","genetics"]),
("cloze","Introns almost always begin with ___ and end with ___ (DNA).","GT … AG",["splicing"]),
("recall","What machine removes introns?","The spliceosome (snRNPs + proteins)",["splicing"]),
("recall","Name four types of alternative splicing.","Exon skipping, alternative 5'/3' splice sites, intron retention, mutually exclusive exons",["splicing","isoforms"]),
("recall","What is MANE Select?","One representative transcript per protein-coding gene, matched exactly between RefSeq and Ensembl; default for clinical reporting",["isoforms","annotation"]),
("recall","Gene vs transcript vs isoform?","Gene = locus; transcript = one RNA product of it; isoform = an alternative transcript (or the protein it encodes)",["isoforms"]),
("recall","Which ML model is the standard for predicting splice-altering variants?","SpliceAI",["splicing","ml"]),
("recall","How many codons are there and how many are stops?","64 codons; 3 stops (TAA, TAG, TGA); 61 sense codons for 20 amino acids",["genetic-code"]),
("recall","Standard start codon and its amino acid?","ATG (AUG in RNA) → methionine",["genetic-code"]),
("recall","Why are many third-position changes silent?","Code is degenerate; third (wobble) position often doesn't change the amino acid",["genetic-code"]),
("recall","How many reading frames does a double-stranded DNA sequence have?","Six: three on each strand",["genetic-code"]),
("recall","Define ORF.","Open reading frame: stretch from a start codon to a stop codon with no internal stop, in one frame",["genetic-code"]),
("apply","A 7-bp deletion lands in a CDS. Consequence class?","Frameshift (not divisible by 3) → downstream sequence scrambled, usually premature stop",["variants"]),
("apply","A 6-bp deletion in a CDS?","In-frame deletion: removes two amino acids, rest of protein intact",["variants"]),
("recall","Missense vs nonsense vs synonymous?","Missense: amino acid changes; nonsense: premature stop; synonymous: codon changes but amino acid doesn't",["variants"]),
("recall","What is NMD?","Nonsense-mediated decay: degradation of mRNAs with a premature stop (typically >~50 nt upstream of the last exon junction)",["variants","mRNA"]),
("apply","A premature stop codon is in the last exon. Is NMD likely?","Usually not; truncated protein may be made (NMD needs a downstream exon junction)",["variants"]),
("recall","What is the polyadenylation signal?","AATAAA (AAUAAA) in the 3' UTR, directing cleavage and poly(A) addition",["mRNA"]),
("recall","Where do microRNAs usually bind their targets?","3' UTR of the target mRNA",["regulation","RNA-classes"]),
("recall","What is a signal peptide?","N-terminal sequence targeting a protein to the secretory pathway/membrane; usually cleaved off",["PTM","proteins"]),
("recall","Which residues get phosphorylated?","Ser, Thr, Tyr (S/T/Y)",["PTM"]),
("recall","What does K48-linked polyubiquitin usually signal?","Degradation by the proteasome",["PTM"]),
("cloze","N-linked glycosylation occurs on Asn in the motif N-X-___ (X ≠ Pro).","S/T",["PTM"]),
("recall","Which amino acid forms disulfide bonds?","Cysteine",["PTM","proteins"]),
("recall","What is a lncRNA?","Long non-coding RNA, >200 nt, not translated (e.g., XIST)",["RNA-classes"]),
("recall","Why might pseudogenes confuse an analysis?","They resemble the parent gene, so reads can mis-map between them",["RNA-classes","data"]),
("apply","Why does Enformer use ~200 kb of input sequence?","Enhancers regulating a gene can lie far from its TSS; long context captures distal regulation",["regulation","ml"]),
("apply","A protein language model and a DNA language model: which sees introns?","The DNA model; PLMs train on translated protein sequences (introns already spliced out)",["ml"]),
("recall","How big is the human mitochondrial genome?","~16.6 kb circular (chrM), maternally inherited",["genome"]),
]
quiz = [
("Which segment of a mature mRNA is translated?",["5' UTR","Coding sequence (CDS)","3' UTR","Poly(A) tail"],1,"Only the CDS from start to stop codon is translated; UTRs are transcribed but not translated."),
("A variant changes GAA (Glu) to GAG (Glu). This is:",["Missense","Nonsense","Synonymous","Frameshift"],2,"Both codons encode glutamate, so the protein is unchanged."),
("A gene lies on the minus strand. Its mRNA sequence relative to the reference genome is:",["Identical to the reference","The reverse complement of the reference","The complement without reversal","Unrelated to the reference"],1,"Reference genomes store the plus strand; minus-strand transcripts are the reverse complement."),
("Which feature most commonly lies tens of kilobases from the gene it regulates?",["Promoter","Kozak sequence","Enhancer","Polyadenylation signal"],2,"Enhancers act through looping and can be far from the TSS."),
("What does MANE Select provide?",["A list of all isoforms of each gene","A single matched RefSeq/Ensembl transcript per protein-coding gene","The longest open reading frame","A database of splicing variants"],1,"MANE Select is one transcript per gene, identical in RefSeq and Ensembl."),
("A variant at the +1 position of an intron (the G of GT) most likely:",["Has no effect","Disrupts splicing","Creates a new start codon","Changes the polyadenylation site"],1,"The canonical GT donor dinucleotide is nearly invariant; changing it usually breaks splicing."),
("Roughly what fraction of the human genome encodes protein?",["~1.5%","~10%","~25%","~50%"],0,"About 1–2% is coding; about half the genome is repeat-derived."),
("Which is NOT a stop codon?",["TAA","TAG","TGA","TGG"],3,"TGG encodes tryptophan."),
("A premature stop codon in exon 3 of a 10-exon gene most likely leads to:",["A normal-length protein","Nonsense-mediated decay of the mRNA","Exon skipping only","Increased expression"],1,"Premature stops upstream of exon junctions trigger NMD."),
("A frameshift is caused by an indel whose length is:",["Exactly 3 bp","Any multiple of 3","Not a multiple of 3","Greater than 100 bp"],2,"Indels not divisible by 3 shift the reading frame."),
("Which PTM most directly targets a protein to the proteasome?",["N-linked glycosylation","K48-linked polyubiquitination","Tyrosine phosphorylation","Disulfide bond formation"],1,"K48-linked ubiquitin chains are the classical degradation signal."),
("A gene's 'isoforms' arise mainly from:",["Different chromosomes","Alternative promoters, splicing and polyadenylation","Codon degeneracy","Post-translational modification only"],1,"Alternative transcript processing creates multiple RNAs and proteins from one gene."),
("What does 'q' denote in a cytoband like 9q34?",["Short arm","Long arm","Centromere","Telomere"],1,"p is the short arm, q is the long arm."),
]
build(1,"central-dogma","Central dogma for practitioners","How genes are laid out in the genome, how they become transcripts and proteins, and which vocabulary (exons, UTRs, isoforms, reading frames, PTMs) shows up constantly in papers and data. This is the vocabulary everything else builds on.",lesson,cards,quiz)
