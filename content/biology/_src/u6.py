from common import build
import os
lesson = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"lessons","u6.md")).read()
from cards_u6 import cards
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
