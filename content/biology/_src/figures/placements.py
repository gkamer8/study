"""Where each figure goes in the lessons, with alt text and caption.

Each entry: (unit, anchor, file, alt, caption). The figure block is inserted after the
Markdown block (paragraph, list or table) that contains `anchor`. Run
`python3 placements.py` to (re)insert all figure blocks into lessons/uN.md; it first
removes any existing figure blocks, so it is idempotent.

Figure block format (one paragraph):
    ![alt](content/biology/figures/<file>)
    **Figure U.N.** caption
Captions and alt text may contain '_' inside words and '*' in alt text, so the site renderer
must handle images before emphasis and ignore intraword underscores (see README).
"""
import os, re
LESSONS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lessons")
BASE = "content/biology/figures/"

FIGS = [
# ---------------- Unit 1
(1, "you will compute it constantly", "u1-dna-strands.svg",
 "Left: three nucleotides of one DNA strand, each phosphate joining the 3' carbon of one sugar to the 5' carbon of the next, with a free phosphate at the 5' end and a free OH at the 3' end. Right: two antiparallel strands, top 5'-ATGCTTCA-3' paired with bottom 3'-TACGAAGT-5'; the bottom strand written 5' to 3' is TGAAGCAT, the reverse complement.",
 "Strand direction. Left: each phosphate links the 3' carbon of one sugar to the 5' carbon of the next, so a strand has a 5' end (free phosphate) and a 3' end (free OH). Right: the two strands run in opposite directions (antiparallel); dashes are hydrogen bonds, the weak attractions holding each base pair together (two for A–T, three for G–C). Notice that reading the bottom strand in its own 5'→3' direction gives the reverse complement of the top strand."),
(1, "inherited from the mother", "u1-karyotype.png",
 "Micrograph of the 46 chromosomes of a human male, stained to show light and dark bands and arranged in pairs numbered 1 to 22 by size, followed by X and Y.",
 "A human male karyotype: the chromosomes of one diploid cell, photographed during division, stained to show bands, and sorted into pairs. Notice the 22 autosome pairs, numbered roughly from largest to smallest, plus one X and one small Y; a female cell would have two X instead. The stripes are the cytogenetic bands used in names like 17p13.1. Image: National Human Genome Research Institute, public domain, via [Wikimedia Commons](https://commons.wikimedia.org/w/index.php?curid=583512); chromosome numbers added."),
(1, "Proteins do most of the work in cells", "u1-central-dogma.svg",
 "Flow diagram: in the nucleus, a gene's DNA is transcribed into pre-mRNA, which is spliced and given a cap and poly(A) tail to become mature mRNA; the mRNA is exported to the cytoplasm, where a ribosome reads codons to build a protein chain from N- to C-terminus.",
 "The central dogma in a human cell. Transcription and RNA processing happen in the nucleus; translation happens in the cytoplasm. Notice that the pre-mRNA still contains introns, while the mature mRNA is shorter and carries a 5' cap (circle) and a poly(A) tail. The ribosome reads the mRNA three bases (one codon) at a time, adding one amino acid per codon."),
(1, "Note that exon ≠ coding", "u1-gene-structure.svg",
 "Gene diagram: a distant enhancer and a promoter upstream of the transcription start site; four exons separated by three introns, each intron starting with GT and ending with AG; the start codon ATG in exon 1 and the stop codon in exon 4, followed by the AATAAA signal and the cleavage site. Below, the pre-mRNA, and the spliced mature mRNA with cap, 5' UTR, coding sequence, 3' UTR and poly(A) tail.",
 "Anatomy of a protein-coding gene, drawn the way genome browsers draw it: thick boxes are coding sequence (CDS), thin boxes are untranslated regions (UTR), lines are introns. Notice that exon 1 and exon 4 are partly UTR, so exon ≠ coding; that every intron begins with GT and ends with AG; and that the mature mRNA keeps only the exons, with a cap added at the 5' end and a poly(A) tail after the cleavage site."),
(1, "SpliceAI is the standard ML model", "u1-splicing.svg",
 "Top: sequence across an intron, CAG|GTAAGT at the exon 2 to intron boundary, a branch point A, a run of C and T, and CAG|GTC at the intron to exon 3 boundary, with the canonical GT and AG in red and HGVS positions c.88, c.88+1, c.88+2, c.89-2, c.89-1 and c.89 marked. Bottom: a five-exon gene and three isoforms: all exons, exon 3 skipped, and intron 4 retained.",
 "Splice sites and isoforms. Top: the donor (5' splice site) is the exon-to-intron junction and the acceptor (3' splice site) the intron-to-exon junction. Notice the near-invariant GT and AG (red); the branch point A and the pyrimidine-rich tract (mostly C and T) are weaker signals the spliceosome also uses. The HGVS c. labels (see Unit 2) show how intronic positions are counted from the nearest exon. Bottom: three isoforms of one gene; each gets its own transcript ID and may encode a different protein."),
(1, "with no stop in between", "u1-reading-frames.svg",
 "Top: the sequence ATGGAATGGCTGAAAGGTTAA read in three frames; frame 1 gives M E W L K G then stop, an open reading frame, while frames 2 and 3 give different amino acids. Bottom: the same sequence with a synonymous change GAA to GAG, a missense change GAA to AAA, a nonsense change TGG to TAG, a one-base deletion that shifts the frame, and a three-base deletion that removes one amino acid.",
 "Reading frames and variant types. Top: one sequence chopped into codons three ways; only frame 1, starting at ATG, gives an open reading frame (ORF). Bottom: changed bases in red, with the resulting protein. Notice that the synonymous change leaves the protein unchanged, the nonsense change truncates it, and deleting one base changes every later codon, while deleting three bases removes exactly one amino acid."),
(1, "with no stop in between", "u1-codon-table.svg",
 "The standard genetic code as a 4 by 4 grid of DNA codons: first base by row (T, C, A, G), second base by column, third base within each cell, each codon labelled with its amino acid's three-letter and one-letter code; ATG (Met) is highlighted as the start codon and TAA, TAG and TGA as stops.",
 "The standard genetic code, written in DNA letters (T instead of U) as it appears in genome and transcript files. Notice how often the third base doesn't matter (for example, every GCN codon is alanine): that is the wobble position, and it is why many single-base changes are synonymous."),
# ---------------- Unit 2
(2, "Indels: `c.5266dupC`", "u2-c-numbering.svg",
 "A transcript drawn as 5' UTR, coding exon 1, intron 1, coding exon 2 ending in the stop codon, and 3' UTR, with HGVS positions c.-14 and c.-1 in the 5' UTR, c.1 at the A of ATG, c.88 at the end of exon 1, c.88+1 and c.89-2 in the intron, c.89 at the start of exon 2, and c.*1 and c.*20 (asterisk prefix) in the 3' UTR.",
 "How HGVS c. positions are counted. Notice there is no c.0: numbering jumps from c.−1 to c.1 at the A of ATG. Intronic bases are named from the nearest exon edge (c.88+1, c.89−2), and 3' UTR bases are counted from the stop codon with an asterisk prefix (c.\\*1, c.\\*20)."),
(2, "TP53 lies on the minus strand", "u2-hgvs.svg",
 "The HGVS string NM_004333.6:c.1799T>A annotated part by part (RefSeq mRNA prefix, accession number, version, coding DNA prefix, position, reference base, new base), the protein form NP_004324.2:p.Val600Glu, the codon change GTG to GAG at codon 600, and the genomic form NC_000007.14:g.140753336A>T.",
 "BRAF V600E, the commonest BRAF mutation in melanoma, written at three levels. Notice that c.1799 is the middle base of codon 600 (codon n spans c.3n−2 to c.3n), so GTG (Val) becomes GAG (Glu). Because BRAF lies on the minus strand, the transcript's T>A is A>T on the genome's + strand, just like the TP53 example above."),
(2, "means protein-level resolution", "u2-hla.svg",
 "The allele name HLA-DRB1*15:01:01:01 split into gene, separator, field 1 (allele group), field 2 (specific protein), field 3 (silent change in coding region) and field 4 (change outside coding region).",
 "Reading an HLA allele name. Each colon-separated field adds resolution; fields 1 and 2 (red) fix the protein sequence, which is what “two-field” typing reports."),
(2, "usual training sets for protein language models", "u2-identifiers.svg",
 "Grid of TP53 identifiers: gene level HGNC symbol TP53 and HGNC:11998, NCBI Gene 7157, Ensembl ENSG00000141510; transcript level NM_000546.6 and ENST00000269305, marked as the MANE Select pair; protein level NP_000537.3, ENSP00000269305, UniProt P04637 (P53_HUMAN); structures PDB 1TUP and AlphaFold AF-P04637-F1.",
 "One gene, many identifiers. Each database has a gene, transcript and protein ID; arrows go from gene to transcript to protein. Notice that the RefSeq transcript NM_000546.6 and the Ensembl transcript ENST00000269305 are the MANE Select pair, so coordinates on either describe the same sequence. Version suffixes (.6) are omitted on Ensembl IDs here; strip them before joining tables."),
# ---------------- Unit 3
(3, "we downloaded X from Y", "u3-database-map.svg",
 "Table mapping common questions to databases: gene identity to NCBI Gene, Ensembl/GENCODE and HGNC; genome position to UCSC Genome Browser and Ensembl; protein function to UniProt and InterPro/Pfam; 3D structure to PDB and AlphaFold DB; expression to GTEx, Human Protein Atlas and CELLxGENE; variant frequency to gnomAD and dbSNP; disease to ClinVar and OMIM; tumor mutations to COSMIC, cBioPortal and TCGA; pathways to GO, KEGG, Reactome, STRING and BioGRID; paper data to GEO and SRA/ENA; dependencies and chemistry to DepMap, ChEMBL and PubChem; regulatory DNA to ENCODE.",
 "One question, one database. The first resource in each row (blue) is the usual first stop; the rest complement it. Use this as a lookup table when a methods section says “we downloaded X from Y”."),
(3, "BioProject** (PRJNA…)", "u3-geo-sra.svg",
 "Tree of accessions for one study: GEO series GSE150000 with samples GSM4500001 and GSM4500002; SRA study SRP260000 with experiments SRX8300001 and SRX8300002, which contain runs SRR11700001, SRR11700002 and SRR11700003; BioProject PRJNA630000 and BioSample SAMN14800001; dashed lines link the same study or sample across archives.",
 "How a paper's data accessions nest (IDs are made up but have the real formats). GEO holds processed tables and sample descriptions; SRA holds the raw reads. Notice that a GEO sample (GSM) corresponds to an SRA experiment (SRX), and the actual FASTQ files hang off runs (SRR), so that is the level you download."),
(3, "BioGRID / IntAct", "u3-go-dag.svg",
 "Fragment of the Gene Ontology graph: biological_process (GO:0008150) is the parent of cellular process (GO:0009987), whose children include cell death (GO:0008219) and signal transduction (GO:0007165); programmed cell death (GO:0012501) is a cell death, apoptotic process (GO:0006915) is a programmed cell death; apoptotic signaling pathway (GO:0097190) is a signal transduction and part of apoptotic process; intrinsic (GO:0097193) and extrinsic (GO:0097191) apoptotic signaling pathways are apoptotic signaling pathways.",
 "A small piece of the Gene Ontology, with real term IDs (from QuickGO). Arrows point from a more specific term to a more general one: solid for “is a”, dashed red for “part of”. Notice that apoptotic signaling pathway has two parents, which is why GO is a graph rather than a tree, and that a gene annotated to a specific term also counts for every ancestor in enrichment analysis."),
# ---------------- Unit 4
(4, "The letters to drill are", "u4-amino-acids.svg",
 "The 20 standard amino acids in six chemical groups (hydrophobic A V L I M; aromatic F W Y; polar uncharged S T N Q; positive K R H; negative D E; special G P C), each with one-letter code, three-letter code and full name; the letters F W Y N Q K R D E are red because they don't match the first letter of the name.",
 "The 20 amino acids grouped by side-chain chemistry, matching the table above. Notice the red one-letter codes: these are the ones you can't guess from the name, and they show up constantly in variant names such as R175H or V600E."),
(4, "while its central DNA-binding region is folded", "u4-structure-levels.svg",
 "Four panels: primary structure as a chain of lettered beads (the first residues of p53); secondary structure as an alpha-helix and as antiparallel and parallel beta-strand pairs; tertiary structure as a helix and strands packed into one fold; quaternary structure as hemoglobin's two alpha and two beta chains.",
 "Four levels of protein structure. Notice that secondary structure is local (a helix or a pair of strands), tertiary structure is the whole chain folded, and quaternary structure needs more than one chain. In β-sheets the arrows point N→C, which is how parallel and antiparallel pairing are defined. Schematic, not to scale."),
(4, "and the immunoglobulin (Ig) fold", "u4-domains.svg",
 "Two protein bars drawn to scale. EGFR, 1,210 residues: signal peptide, two receptor L domains and two cysteine-rich regions outside the cell, a transmembrane helix at 646 to 668, and a protein kinase domain at 712 to 979 with L858R marked. p53, 393 residues: transactivation domain, proline-rich region, DNA-binding domain at 102 to 292 with hotspots R175, R248 and R273, tetramerization domain and basic C-terminal region, with disordered stretches dashed.",
 "Domain architecture, from UniProt and Pfam coordinates. EGFR shows the receptor tyrosine kinase layout: ligand-binding domains outside the cell (L = receptor L domain, CR = furin-like cysteine-rich region), one transmembrane (TM) helix, and the kinase inside. p53's cancer hotspots all fall in its DNA-binding domain; the tetramerization domain lets four p53 chains assemble, and the dashed stretches are intrinsically disordered."),
(4, "even when each domain alone has high pLDDT", "u4-alphafold-p53.svg",
 "AlphaFold model of human p53 drawn as a backbone trace coloured by pLDDT: a compact dark-blue (very high confidence) DNA-binding domain and a small helical tetramerization region, with long orange (very low confidence) loops for the N- and C-terminal tails. Right: per-residue pLDDT plot above a domain bar, and the PAE matrix showing a dark, low-error square for residues about 95 to 290.",
 "A real AlphaFold prediction for human p53. Notice the three signals agree: the DNA-binding domain is dark blue in the structure, above 90 in the pLDDT plot, and a dark (low-error) square in the PAE matrix, while the disordered N- and C-terminal tails are mostly orange, below 50, and pale. Do not read the orange loops as real structure. Data: AlphaFold DB entry AF-P04637-F1 (model v6; Jumper et al. 2021, Varadi et al. 2024), CC-BY 4.0, [alphafold.ebi.ac.uk/entry/P04637](https://alphafold.ebi.ac.uk/entry/P04637); drawn for this site."),
(4, "less signal and worse predictions", "u4-msa.svg",
 "A six-sequence alignment of a 12-residue segment from human, mouse, chicken, frog, fish and fly; column 7 is always G (conserved), and columns 8 and 9 vary together, T with R or S with K (coevolving).",
 "The two signals in an MSA (an illustrative alignment, not a real protein). Notice column 7, which never changes (conservation), and columns 8 and 9, which change together: whenever position 8 is S, position 9 is K. Coevolving pairs like this tend to be in contact in 3D, which is the signal AlphaFold's MSA processing and DCA exploit."),
# ---------------- Unit 5
(5, "KRAS G12C inhibitors (sotorasib)", "u5-mapk.svg",
 "Pathway diagram: EGF binds a dimerized, autophosphorylated EGFR at the membrane; GRB2 binds the phosphotyrosines and brings SOS, a GEF, which loads GTP onto RAS; NF1, a GAP, helps RAS cut GTP back to GDP; RAS-GTP activates RAF, which phosphorylates MEK1/2, which phosphorylates ERK1/2; ERK enters the nucleus and switches on growth genes such as FOS and MYC. Red labels mark cancer mutations (EGFR L858R, KRAS G12/G13/Q61, BRAF V600E, NF1 loss) and gray bars mark drugs (osimertinib, sotorasib, vemurafenib, dabrafenib, trametinib).",
 "The RTK → RAS → MAPK cascade. Arrows mean activates, flat bars mean inhibits. Notice the RAS switch in the middle: SOS (a GEF) turns RAS on by loading GTP and NF1 (a GAP) turns it off, so KRAS mutations that block GTP cutting and loss of NF1 both leave RAS stuck on. Sotorasib binds KRAS G12C in its GDP (off) form and holds it there."),
(5, "PIK3CA cancer hotspots: E545K, H1047R", "u5-pi3k.svg",
 "Pathway diagram: an RTK activates PI3K, which converts the membrane lipid PIP2 to PIP3, while PTEN converts PIP3 back to PIP2; PIP3 recruits AKT, which PDK1 phosphorylates at T308 and mTORC2 at S473; AKT promotes cell survival and inhibits TSC1/TSC2, a GAP that inhibits RHEB; RHEB-GTP activates mTORC1, which is inhibited by AMPK and rapamycin; mTORC1 activates S6K and inhibits 4E-BP1, both leading to more protein synthesis and cell growth.",
 "The PI3K → AKT → mTOR pathway. Notice the two lipid arrows at the membrane: PI3K makes PIP3 and PTEN removes it, so activating PIK3CA mutations and PTEN loss have the same effect. Further down, two inhibitions in a row (AKT ⊣ TSC1/TSC2 ⊣ RHEB) add up to activation of mTORC1. mTORC1 boosts protein synthesis both by activating S6K and by switching off the translation brake 4E-BP1."),
(5, "losing both is not", "u5-p53.svg",
 "Diagram: double-strand breaks activate ATM then CHK2, and single-stranded DNA or stalled replication activates ATR then CHK1; these kinases phosphorylate p53. p53 induces p21 (CDKN1A), which turns off CDKs to pause the cell cycle or cause senescence, and BAX, PUMA and NOXA, which cause apoptosis. MDM2 ubiquitinates p53 for destruction by the proteasome, and p53 induces the MDM2 gene, forming a negative feedback loop.",
 "The p53 DNA-damage response. Notice the loop at the center: MDM2 destroys p53, and p53 switches on the MDM2 gene, so p53 normally stays scarce. Damage-activated kinases phosphorylate p53, which stops MDM2 binding it; p53 then builds up and turns on p21 (pause) or BAX, PUMA and NOXA (apoptosis)."),
(5, "Loss of **APC** starts most colorectal cancers", "u5-wnt.svg",
 "Two panels. Wnt off: the destruction complex (APC, AXIN, GSK3β, CK1) phosphorylates β-catenin, which is ubiquitinated and destroyed by the proteasome; target genes stay off. Wnt on: Wnt binds Frizzled and LRP5/6, the destruction complex is blocked, β-catenin builds up, enters the nucleus and joins TCF/LEF to turn on MYC, AXIN2 and LGR5.",
 "Wnt/β-catenin signaling off and on. Notice that the signal works by stopping destruction: without Wnt, β-catenin is made but immediately destroyed. Losing APC breaks the destruction complex, which is why APC-mutant colorectal tumors behave as if Wnt were always on."),
(5, "treat hormone-receptor-positive breast cancer", "u5-cell-cycle.svg",
 "Cell-cycle wheel running clockwise G1, S, G2, M, with G0 branching off G1; checkpoint bars at the G1/S boundary, the G2/M boundary and the spindle checkpoint within M; the restriction point late in G1. Side panel: cyclin D with CDK4/6 in G1, cyclin E with CDK2 at G1/S, cyclin A with CDK2 in S, cyclin B with CDK1 at G2/M; CDK4/6 phosphorylates and inhibits RB, which inhibits E2F, which turns on S-phase genes; p16 and palbociclib block CDK4/6.",
 "The cell cycle. Notice the order G1 → S → G2 → M and where the three checkpoints sit (red bars). The commitment step is a double inhibition: CDK4/6 inactivates RB, freeing E2F to switch on S-phase genes, which is why p16 loss or CDK4/6 drugs act right at the restriction point. Phase lengths are drawn roughly as in a typical dividing human cell; they vary."),
# ---------------- Unit 6
(6, "Characters encode Q + 33 as ASCII", "u6-fastq.svg",
 "A four-line FASTQ record: an Illumina header line starting with @, a 24-base sequence ending in N, a + separator line, and a quality line of characters such as I, H, G, ?, 5, + and #, each decoded below to its Phred score (40 down to 2). Below, a table decoding the characters !, +, 5, ? and I to ASCII codes 33, 43, 53, 63, 73, Phred scores 0, 10, 20, 30, 40, and error probabilities 1, 1 in 10, 1 in 100, 1 in 1,000 and 1 in 10,000.",
 "Anatomy of a FASTQ record. The header names the instrument, run, flow cell (the glass slide the reads were made on), lane, tile and position of the cluster, then the read number and sample index. Notice that line 4 has exactly one character per base and that quality falls toward the end of the read, as it typically does; the N at the end is a base the machine couldn't call, given quality # (Q2)."),
(6, "`50M1000N50M` = a read split", "u6-sam.svg",
 "A SAM record with fields QNAME read001, FLAG 99, RNAME chr1, POS 103, MAPQ 60, CIGAR 2S6M1I5M2D4M, RNEXT =, PNEXT 290, TLEN 205, an 18-base SEQ, QUAL and the tag NM:i:4, then the alignment it describes: two soft-clipped bases, six aligned bases including one mismatch, one inserted base, five aligned bases, two deleted reference bases and four aligned bases. A list of CIGAR operations and the FLAG bits, with 99 = 1 + 2 + 32 + 64 (paired, proper pair, mate reverse strand, first in pair).",
 "Reading one SAM record. Notice that POS is the first aligned reference base (1-based) and that soft-clipped bases are not counted in it; that M covers mismatches as well as matches; and that the FLAG is a sum of yes/no bits, here paired + proper pair + mate on the reverse strand + first read of the pair. NM:i:4 counts one mismatch, one inserted and two deleted bases."),
(6, "`chr1 100 . A AT` = insertion", "u6-vcf.svg",
 "A VCF excerpt: meta lines starting with ##, a #CHROM header row, and four variant rows with columns CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO, FORMAT and two sample columns (tumor and normal): an insertion G to GT at chr1:1000100, a deletion CGC to C at chr1:1000200, BRAF V600E as chr7:140753336 A to T (rs113488022), heterozygous in the tumor only, and TP53 P72R as chr17:7676154 G to C (rs1042522), phased homozygous in both samples.",
 "Anatomy of a VCF (GRCh38; the reference bases are real, the two indels are made-up examples). Notice that indels repeat the base before them in both REF and ALT, so POS points at that anchor base, and that the genotype columns use 0 for REF and 1 for ALT: the BRAF variant is 0/1 in the tumor and 0/0 in the normal sample, the signature of a somatic mutation."),
(6, "classic off-by-one bug", "u6-coordinates.svg",
 "The ten-base sequence ACGTTGCAAC with 0-based boundary numbers 0 to 10 above the gaps between bases and 1-based numbers 1 to 10 below each base; bases G T T are highlighted as BED interval 2 to 5, end excluded, and as 1-based positions 3 to 5, both included. A table lists BED and Python slices as 0-based half-open, and GTF/GFF, SAM/VCF POS and samtools or browser region strings as 1-based closed.",
 "The same three bases in both coordinate systems. Notice that 0-based half-open numbers the gaps between bases (like Python slicing), so BED chr1 2 5 and seq[2:5] both mean GTT, while 1-based systems number the bases themselves, giving 3–5. Converting BED to 1-based means adding 1 to the start and leaving the end unchanged."),
(6, "`adata.uns`: everything else", "u6-anndata.svg",
 "AnnData layout: a central matrix adata.X with five example cells as rows and five genes (CD3E, MS4A1, LYZ, NKG7, PPBP) as columns, mostly zeros; adata.obs to the left with one row per cell (cell barcode, cell type, donor); adata.var on top with one row per gene (symbol, Ensembl ID); adata.obsm to the right with per-cell embeddings X_pca and X_umap; dashed sheets behind X for adata.layers; and adata.uns for everything else.",
 "How an AnnData object fits together. Notice that everything is aligned to the matrix: rows of X, obs and obsm are the same cells in the same order, and columns of X are the rows of var. The counts are illustrative; real matrices have thousands of genes and are over 90% zeros, so they are stored sparse."),
(6, "DNase-seq is the older method", "u6-workflows.svg",
 "Four assay pipelines as rows of steps: bulk RNA-seq (extract RNA, make cDNA, sequence, align with STAR or salmon, count per gene, test with DESeq2); scRNA-seq (droplets with cell barcodes and UMIs, cDNA library, sequence, Cell Ranger or STARsolo, cell by gene counts in .h5ad, analyze); ChIP-seq (crosslink and shear, antibody pull-down, sequence, align, call peaks with MACS2 against an input control, narrowPeak); ATAC-seq (isolate nuclei, Tn5 tagmentation of open DNA, sequence, align, call peaks, BED).",
 "Four assays side by side, from wet lab (green) to sequencer (gray) to computation (blue). Notice the shared middle: every assay produces FASTQ reads that are then mapped to a reference (usually saved as BAM files); the assays differ in what is captured before sequencing and in the final table (gene counts, a cell × gene matrix, or peaks)."),
# ---------------- Unit 7
(7, "what evolution keeps (plausible sequences)", "u7-masked-marginal.svg",
 "The sequence MKTAYEAKQR with position 6 (wild type E) replaced by a mask token; a bar chart of the model's predicted probabilities at that position, E 0.42, D 0.18, Q 0.09, K 0.06 and smaller values; and the calculation score = log 0.06 minus log 0.42 = −1.95.",
 "Zero-shot scoring of the variant E6K with a masked language model (illustrative probabilities). Notice that the score compares only two bars, the mutant and the wild type, and is negative because the model rates K as less plausible than E at this position; ranking all variants by this score is what gets compared with DMS measurements."),
(7, "which Caduceus builds in", "u7-tokenization.svg",
 "Examples of tokenization: a protein as one token per amino acid between cls and eos tokens; DNA as a one-hot matrix with one column per base; DNA as overlapping 3-mers starting at every base; DNA as non-overlapping 6-mers; DNA as variable-length byte-pair-encoding pieces; a single cell as a ranked list of gene tokens (Geneformer); and a single cell as gene tokens with binned expression values (scGPT).",
 "What becomes a token. Notice that overlapping k-mers repeat most bases in neighboring tokens (the leak that lets a masked token be read off its neighbors), while non-overlapping and BPE tokens cover each base once. For single cells there is no natural order: Geneformer creates one by ranking genes, and scGPT instead attaches a binned value to each gene. Examples are illustrative."),
(7, "the model memorizes that one protein binds everything", "u7-splits.svg",
 "Three panels of training (light blue) and test (red) examples. Random split: test examples scattered across clusters of similar sequences, each with relatives in training. Clustered split: two whole clusters held out as test. Temporal split: examples placed along a 2014 to 2024 time axis, with everything after the cutoff in test.",
 "Three ways to split data. Notice that in the random split every test protein has a close relative in training, which inflates scores; the clustered split holds out whole clusters of homologs, so no test protein shares more than about 30% identity with a training protein, and the temporal split tests on data released after the training cutoff. The same idea applies to chromosomes, genes and donors."),
]

def strip(md):
    out = re.sub(r"\n\n!\[[^\]]*\]\(content/biology/figures/[^)]+\)\n\*\*Figure [^\n]*(?=\n|$)", "", md)
    return out

def insert(md, unit):
    md = strip(md)
    n = 0
    for (u, anchor, fn, alt, cap) in FIGS:
        if u != unit: continue
        n += 1
        i = md.find(anchor)
        assert i >= 0, (unit, anchor)
        j = md.find("\n\n", i)
        if j < 0: j = len(md)
        while md.startswith("\n\n![", j):          # keep figure order when two share an anchor
            k = md.find("\n\n", j + 2)
            j = k if k >= 0 else len(md)
        block = f"\n\n![{alt}]({BASE}{fn})\n**Figure {unit}.{n}.** {cap}"
        md = md[:j] + block + md[j:]
    # number figures in reading order
    cnt = iter(range(1, 100))
    md = re.sub(r"\*\*Figure \d+\.\d+\.\*\*", lambda m: f"**Figure {unit}.{next(cnt)}.**", md)
    return md

if __name__ == "__main__":
    for u in range(1, 8):
        p = os.path.join(LESSONS, f"u{u}.md")
        md = open(p).read()
        new = insert(md, u)
        open(p, "w").write(new)
        print(u, new.count("![") , "figures")
