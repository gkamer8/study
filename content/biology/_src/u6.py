from common import build
lesson = r"""
## Sequence files

**FASTA**: a header line starting with `>`, then sequence lines. It is used for references, proteins and transcripts. UniProt headers look like `>sp|P04637|P53_HUMAN Cellular tumor antigen p53 OS=Homo sapiens OX=9606 GN=TP53 …`, where `sp` = Swiss-Prot (`tr` = TrEMBL) and OX is the NCBI taxonomy ID (9606 = human, 10090 = mouse).

**FASTQ**: raw reads, **4 lines per record**:
```
@read_id
ACGTTGCA...
+
IIIIHHG#...
```
Line 4 holds per-base quality as ASCII characters. **Phred score Q = −10·log10(P_error)**: Q10 = 1 in 10 errors, Q20 = 1%, **Q30 = 0.1%** (the usual quality bar), Q40 = 0.01%. Modern encoding is **Phred+33**: character = chr(Q+33), so `!` = Q0, `+` = Q10, `5` = Q20, `?` = Q30, `I` = Q40. Paired-end runs produce `_R1`/`_R2` files from the two ends of each fragment.

## Alignments: SAM/BAM/CRAM

Aligners map reads to a reference. DNA aligners include BWA-MEM and Bowtie2; RNA aligners are splice-aware (STAR, HISAT2). Output is **SAM** (text), **BAM** (compressed binary, indexed by `.bai` after coordinate sorting), or **CRAM** (compressed relative to the reference, so smaller, but you need the exact reference to decode). Each SAM line has **11 mandatory fields**: QNAME, **FLAG**, RNAME, **POS** (1-based leftmost), **MAPQ**, **CIGAR**, RNEXT, PNEXT, TLEN, SEQ, QUAL, followed by optional tags (NM:i:, MD:Z:, and cell-barcode tags like CB:Z: in single-cell data).

- **FLAG** is a bitfield: 1 paired, 2 proper pair, **4 unmapped**, **16 reverse strand**, 256 secondary, **1024 PCR/optical duplicate**, 2048 supplementary (split/chimeric).
- **CIGAR** describes the alignment: `M` match/mismatch, `I` insertion, `D` deletion, **`N` skipped region (an intron in RNA-seq)**, `S` soft clip, `H` hard clip. Example: `50M1000N50M` is a spliced read.
- **MAPQ** = Phred-scaled confidence that the mapping position is correct. MAPQ 0 usually means a multi-mapper.

## Variants: VCF

**VCF** columns: CHROM, POS (1-based), ID (rsID), REF, ALT, QUAL, FILTER (PASS), INFO (key=value pairs such as AF, DP, or annotations), FORMAT, then one column per sample. Genotypes: `0/0` hom-ref, `0/1` het, `1/1` hom-alt; `|` means phased (`0|1`). gVCFs also record non-variant blocks. Indels are left-aligned, and REF includes the preceding base: `chr1 100 . A AT` is an insertion of T.

## Intervals and annotations: BED and GTF/GFF

**BED**: `chrom start end [name score strand …]`, **0-based, half-open**. `chr1 0 100` means the first 100 bases (1-based positions 1–100). Used for peaks, target regions and blacklists. narrowPeak (from MACS) is an extended BED.

**GTF/GFF3**: gene annotation with **9 columns**: seqname, source, feature (gene/transcript/exon/CDS/UTR/start_codon), **start, end (1-based, inclusive)**, score, strand, frame, attributes. GTF attributes look like `gene_id "ENSG…"; transcript_id "ENST…";`. GFF3 uses `ID=…;Parent=…`. GENCODE and Ensembl distribute GTFs that quantification tools consume.

The **off-by-one** trap between BED (0-based) and VCF/GTF/SAM (1-based) causes real bugs.

## Reference genome builds

- **GRCh37 ≈ hg19** (2009) and **GRCh38 ≈ hg38** (2013). GRC names come from the Genome Reference Consortium; hg names come from UCSC. They contain the same sequence for the primary chromosomes, but UCSC uses `chr1` naming while GRC/Ensembl uses `1`, and the mitochondrial sequence differed in hg19 (chrM) vs GRCh37 (MT, the rCRS).
- Coordinates **differ between builds**: BRAF V600E is chr7:140,453,136 in hg19 and chr7:140,753,336 in hg38. Convert with liftOver or CrossMap, and never mix builds.
- **T2T-CHM13** (2022) is the first gap-free human assembly. GRCh38 is still the default in most pipelines. Mouse builds: mm10 (GRCm38), mm39 (GRCm39).
- Annotation versions (GENCODE vXX / Ensembl release) are separate from the assembly. Report both.

## Bulk RNA-seq

Workflow: extract RNA, enrich poly(A) or deplete rRNA, make cDNA, sequence, then either align (STAR) and count reads per gene (featureCounts/HTSeq), or **pseudoalign** (salmon, kallisto) to transcripts. Units:
- **Raw counts**: integers. Required by **DESeq2/edgeR**, which model counts with a negative binomial distribution.
- **CPM**: counts per million (depth only).
- **RPKM/FPKM**: normalize by depth, then by gene length (per kb). Values are not comparable across samples because the totals differ.
- **TPM**: normalize by length first, then scale so each sample sums to 1,000,000. Better for within-sample comparison. Neither TPM nor FPKM replaces proper DE normalization.
- Differential expression reports **log2 fold change** and **BH-adjusted p-values (FDR)**, often shown as volcano plots.

## Single-cell RNA-seq

Droplet platforms (10x Genomics Chromium) tag every transcript with a **cell barcode** (which cell) and a **UMI** (unique molecular identifier, which original molecule). Counting unique UMIs per gene removes PCR duplicates. Cell Ranger (or STARsolo, alevin-fry) outputs a sparse **cell-by-gene count matrix**. 10x MTX files are genes × cells, while **AnnData (.h5ad)**, the scanpy/Python standard, is **cells × genes**:
- `adata.X`: the matrix, rows = cells (obs) and columns = genes (var)
- `adata.obs`: per-cell metadata (cell type, donor, batch, QC)
- `adata.var`: per-gene metadata (Ensembl ID, symbol, highly_variable)
- `adata.obsm`: embeddings (X_pca, X_umap); `adata.layers`: alternative matrices (e.g., raw counts); `adata.uns`: unstructured metadata

Standard processing: QC (remove cells with few genes or high **mitochondrial read fraction**, and remove doublets), `normalize_total` + `log1p`, highly variable genes, PCA, kNN graph, **Leiden** clustering, **UMAP** for visualization, then annotate cell types with marker genes. Batch effects are corrected with Harmony or scVI. Data are very sparse (mostly zeros). R users use Seurat objects.

## Chromatin assays

- **ChIP-seq**: crosslink, fragment, immunoprecipitate with an antibody against a TF or histone mark, then sequence. Peaks are called with MACS2/3 against an input control. Marks: **H3K4me3** active promoters, **H3K27ac** active enhancers and promoters, **H3K4me1** enhancers, **H3K27me3** Polycomb repression, **H3K36me3** transcribed gene bodies, **H3K9me3** heterochromatin. CUT&RUN and CUT&Tag are lower-input alternatives.
- **ATAC-seq**: hyperactive **Tn5 transposase** inserts adapters into **open chromatin**, giving a map of accessibility. scATAC-seq does this per cell. DNase-seq is the older equivalent.
- **Hi-C**: 3D contact maps (TADs, loops).

## CRISPR screens

A **pooled** library of sgRNAs (typically 4–10 per gene, e.g. Brunello) is delivered by lentivirus at low MOI (about one guide per cell). Cells are selected (proliferation, drug, FACS sort), and guides are counted by sequencing. **Depleted** guides mark genes required under the condition (essential genes drop out). Enriched guides mark resistance genes. Analysis uses MAGeCK, BAGEL, or Chronos (DepMap). Variants: knockout (Cas9), **CRISPRi** (dCas9-KRAB, repression), **CRISPRa** (activation), base and prime editing screens. **Perturb-seq** pairs perturbations with scRNA-seq readouts, a major dataset type for perturbation-prediction models.

## Mass-spectrometry proteomics

In **bottom-up** proteomics, proteins are digested with **trypsin** (which cleaves after K/R, not before P), peptides are separated by liquid chromatography, and they are analyzed by tandem MS (**LC-MS/MS**). Spectra are matched to peptides from a protein database, and FDR is controlled with a **target-decoy** approach. Acquisition modes are **DDA** (data-dependent, picks top precursors) and **DIA** (data-independent, more reproducible). Quantification uses label-free methods (LFQ) or isobaric tags (**TMT**). Tools: MaxQuant, DIA-NN, FragPipe. Repository: PRIDE. Phosphoproteomics adds enrichment of phosphopeptides.

## How you'll see this in a paper

- "Reads were aligned to GRCh38 with STAR (GENCODE v38) and quantified with salmon": build, annotation and quantifier.
- "Cells with <200 genes or >20% mitochondrial reads were removed": standard scRNA-seq QC.
- "Peaks were called with MACS2 (q < 0.01)" and "ATAC peaks overlapping the ENCODE blacklist were excluded".
- Genomics models: "one-hot encoded 131 kb sequences predicting coverage tracks from ENCODE/FANTOM".
"""
cards = [
("recall","FASTA header starts with which character?","'>'",["FASTA"]),
("identify",">sp|P04637|P53_HUMAN … OX=9606 GN=TP53","UniProt Swiss-Prot FASTA header: accession, entry name, taxon ID 9606 (human), gene name",["FASTA","UniProt"]),
("recall","NCBI taxonomy IDs for human and mouse?","9606 (human), 10090 (mouse)",["identifiers"]),
("recall","Four lines of a FASTQ record?","@id; sequence; '+'; quality string",["FASTQ"]),
("recall","Phred quality formula?","Q = −10·log10(P_error)",["FASTQ"]),
("recall","Error probability at Q20 and Q30?","Q20 = 1%; Q30 = 0.1%",["FASTQ"]),
("recall","Phred+33: what are '!' and 'I'?","'!' = Q0; 'I' = Q40",["FASTQ"]),
("recall","SAM vs BAM vs CRAM?","SAM text; BAM compressed binary; CRAM reference-based compression (needs the reference)",["SAM"]),
("recall","Is SAM POS 0- or 1-based?","1-based (leftmost mapped base)",["SAM","coordinates"]),
("identify","SAM FLAG 4 / 16 / 1024","Unmapped / reverse strand / duplicate",["SAM"]),
("identify","SAM FLAG 256 vs 2048","Secondary alignment vs supplementary (split/chimeric) alignment",["SAM"]),
("identify","CIGAR 50M1000N50M","Spliced read: 50 aligned, 1000-bp intron skipped, 50 aligned",["SAM","RNA-seq"]),
("identify","CIGAR S vs H","Soft clip (bases kept in SEQ) vs hard clip (bases removed)",["SAM"]),
("recall","What does MAPQ 0 usually indicate?","Multi-mapping read (position ambiguous)",["SAM"]),
("recall","VCF fixed columns?","CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO (+ FORMAT and samples)",["VCF"]),
("identify","Genotypes 0/1 vs 0|1 vs 1/1","Het unphased / het phased / homozygous alt",["VCF"]),
("recall","BED coordinate system?","0-based, half-open",["BED","coordinates"]),
("apply","BED line 'chr1 99 100' covers which 1-based position?","Position 100 (one base)",["BED","coordinates"]),
("recall","GTF/GFF coordinate system?","1-based, inclusive (start and end)",["GTF","coordinates"]),
("recall","GTF vs GFF3 attribute style?","GTF: gene_id \"…\"; transcript_id \"…\";  GFF3: ID=…;Parent=…",["GTF"]),
("recall","GRCh37 and GRCh38 correspond to which UCSC names?","hg19 and hg38",["assemblies"]),
("recall","Chromosome naming difference UCSC vs Ensembl?","UCSC 'chr1', 'chrM'; Ensembl/GRC '1', 'MT'",["assemblies"]),
("apply","A VCF in hg19 and a BED in hg38. What must you do before intersecting?","Lift one over to the other build (liftOver/CrossMap)",["assemblies"]),
("recall","What is T2T-CHM13?","First complete gap-free human genome assembly (2022)",["assemblies"]),
("recall","Mouse current assemblies?","mm10 (GRCm38) and mm39 (GRCm39)",["assemblies"]),
("recall","Which tools pseudoalign RNA-seq reads?","salmon, kallisto",["RNA-seq"]),
("recall","What input do DESeq2/edgeR require?","Raw integer counts (negative binomial models)",["RNA-seq"]),
("recall","TPM vs FPKM order of operations?","TPM: length first, then depth (sums to 1e6); FPKM: depth first, then length",["RNA-seq"]),
("recall","Why is TPM preferred over FPKM for comparing samples?","TPM sums to the same total in every sample; FPKM totals vary",["RNA-seq"]),
("recall","What is a UMI?","Unique molecular identifier: random barcode tagging each original molecule to collapse PCR duplicates",["single-cell"]),
("recall","Cell barcode vs UMI?","Barcode: which cell/droplet; UMI: which molecule",["single-cell"]),
("recall","AnnData X orientation?","Cells (obs) × genes (var)",["single-cell","AnnData"]),
("identify","adata.obs / adata.var / adata.obsm / adata.layers","Cell metadata / gene metadata / embeddings (PCA, UMAP) / alternative matrices (e.g., raw counts)",["AnnData"]),
("recall","Why remove cells with high mitochondrial read fraction?","Indicates damaged/dying cells (cytoplasmic mRNA lost)",["single-cell"]),
("recall","Standard scanpy pipeline?","QC → normalize_total → log1p → HVGs → PCA → neighbors → Leiden → UMAP",["single-cell"]),
("recall","What is a doublet?","A droplet containing two cells, giving a mixed profile",["single-cell"]),
("recall","H3K4me3 marks…?","Active promoters",["ChIP-seq"]),
("recall","H3K27ac marks…?","Active enhancers and promoters",["ChIP-seq"]),
("recall","H3K27me3 marks…?","Polycomb-repressed chromatin",["ChIP-seq"]),
("recall","H3K36me3 marks…?","Bodies of actively transcribed genes",["ChIP-seq"]),
("recall","Standard ChIP-seq peak caller?","MACS2/MACS3",["ChIP-seq"]),
("recall","ATAC-seq measures what, using which enzyme?","Chromatin accessibility; Tn5 transposase",["ATAC-seq"]),
("recall","Pooled CRISPR KO screen readout?","sgRNA abundance by sequencing before vs after selection",["CRISPR"]),
("apply","Guides for gene X are strongly depleted after 3 weeks of growth. Interpretation?","Gene X is required for proliferation (essential/fitness gene)",["CRISPR"]),
("recall","CRISPRi vs CRISPRa?","dCas9-KRAB represses; dCas9-activator (e.g., VP64/VPR) activates; no DNA cut",["CRISPR"]),
("recall","What is Perturb-seq?","Pooled CRISPR perturbations with single-cell RNA-seq readout",["CRISPR","single-cell"]),
("recall","Trypsin cleavage rule?","After K or R, not before P",["proteomics"]),
("recall","DDA vs DIA?","DDA: selects top precursors for MS2; DIA: fragments all precursors in m/z windows (more reproducible)",["proteomics"]),
("recall","How is FDR controlled in peptide identification?","Target-decoy search (reversed/shuffled decoy database)",["proteomics"]),
("recall","What is TMT?","Tandem mass tag: isobaric labels for multiplexed quantification",["proteomics"]),
]
quiz = [
("A FASTQ quality character 'I' under Phred+33 encodes:",["Q30","Q40","Q20","Q73"],1,"ord('I') = 73; 73 − 33 = 40."),
("A BED entry 'chr2 1000 1005' covers which 1-based positions?",["1000–1005","1001–1005","1000–1004","1001–1006"],1,"BED is 0-based half-open: start+1 to end in 1-based coordinates."),
("Which CIGAR operation indicates an intron in an RNA-seq alignment?",["D","I","N","S"],2,"N = skipped region from the reference."),
("Which quantity sums to 1,000,000 in every sample?",["FPKM","RPKM","TPM","Raw counts"],2,"TPM normalizes for length first, then scales to 1e6."),
("DESeq2 should be given:",["TPM","Log-normalized values","Raw integer counts","FPKM"],2,"Its negative binomial model expects raw counts."),
("In AnnData, adata.X rows correspond to:",["Genes","Cells","Batches","Clusters"],1,"AnnData is obs × var = cells × genes."),
("Purpose of UMIs in scRNA-seq:",["Identify the cell of origin","Collapse PCR duplicates of the same molecule","Mark the gene strand","Indicate read quality"],1,"Each original molecule gets a UMI; duplicates share it."),
("A SAM FLAG of 16 means:",["Unmapped","Read mapped to reverse strand","PCR duplicate","Secondary alignment"],1,"Bit 0x10 = reverse complemented."),
("Which histone mark best indicates active enhancers?",["H3K27me3","H3K9me3","H3K27ac","H3K36me3"],2,"H3K27ac marks active enhancers and promoters."),
("ATAC-seq primarily measures:",["DNA methylation","Chromatin accessibility","Protein-DNA binding of a specific TF","3D contacts"],1,"Tn5 inserts into open chromatin."),
("hg19 corresponds to:",["GRCh38","GRCh37","T2T-CHM13","GRCm39"],1,"UCSC hg19 ≈ GRC GRCh37."),
("In a VCF, '0|1' denotes:",["Unphased heterozygote","Phased heterozygote","Homozygous reference","Missing genotype"],1,"'|' indicates phased genotypes."),
("Trypsin cleaves peptide bonds:",["After K/R, not before P","Before D/E","After aromatic residues","At random"],0,"This predictable rule enables database search."),
("In a pooled CRISPR knockout proliferation screen, essential genes show:",["Enriched guides","Depleted guides","No change","Increased UMIs"],1,"Cells losing essential genes drop out, so their guides decline."),
("CRAM files differ from BAM mainly by:",["Being text","Compressing relative to a reference sequence","Storing only unmapped reads","Lacking quality scores entirely"],1,"CRAM stores differences from the reference and needs it to decode."),
("A single-cell QC step removes cells with >20% mitochondrial reads because they are likely:",["Doublets","Damaged or dying cells","Highly proliferative","Immune cells"],1,"Damaged cells lose cytoplasmic mRNA, inflating the mitochondrial fraction."),
]
build(6,"data-formats-experiments","Data formats and experiments","The file formats (FASTA, FASTQ, SAM/BAM/CRAM, VCF, BED, GTF/GFF, h5ad) and coordinate conventions you'll handle, the reference genome builds, and how the main assays work: bulk and single-cell RNA-seq, ChIP-seq, ATAC-seq, CRISPR screens, and mass-spec proteomics.",lesson,cards,quiz)
