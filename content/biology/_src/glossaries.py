# Replaces the "### Key terms" block at the top of each lesson. One term per bullet; the
# definition must point to exactly one term and must not contain the term itself.
G = {}
G[1] = """
- **Nucleotide**: one building block of DNA or RNA: a sugar, a phosphate group, and a base (A, C, G, T; U replaces T in RNA).
- **Base pair (bp)**: two bases on opposite DNA strands held together (A with T, G with C); also the unit of DNA length (1 kb = 1,000 of them).
- **Strand**: one continuous chain of nucleotides; DNA has two wound into a double helix.
- **5' end**: the end of a nucleic-acid chain carrying a free phosphate; sequences are written starting from it ("upstream").
- **3' end**: the end of a nucleic-acid chain carrying a free hydroxyl group, where polymerases add new nucleotides ("downstream").
- **Antiparallel**: describes the two DNA strands running in opposite directions.
- **Reverse complement**: the sequence of the opposite strand, read in its own 5'→3' direction (complement every base, then reverse the order).
- **Chromosome**: one long DNA molecule plus its packaging proteins; humans have 23 kinds.
- **Genome**: all the DNA of an organism.
- **Haploid**: having one copy of each chromosome (n), like eggs and sperm.
- **Diploid**: having two copies of each chromosome (2n), like most human cells.
- **Autosome**: any of the numbered human chromosomes 1–22 (not X or Y).
- **Sex chromosome**: X or Y.
- **Gene**: a stretch of DNA that is copied into a functional RNA (and often then into a protein).
- **Locus**: a specific position or region in the genome.
- **Allele**: one version of the sequence at a given position in the genome.
- **Homozygous**: carrying two identical versions of the sequence at a position.
- **Heterozygous**: carrying two different versions of the sequence at a position.
- **Transcription**: copying DNA into RNA.
- **Translation**: building a protein by reading an mRNA template.
- **mRNA**: the processed RNA copy of a gene that ribosomes read to make protein ("messenger").
- **Ribosome**: the molecular machine that reads mRNA and builds protein.
- **Amino acid**: one of the 20 building blocks of proteins.
- **Codon**: three consecutive nucleotides that specify one amino acid or a stop.
- **Exon**: a segment of a gene that is kept in the mature mRNA.
- **Intron**: a segment of a gene that is cut out of the RNA before it is used.
- **Splicing**: removing introns from RNA and joining the remaining segments.
- **UTR**: a stretch at either end of an mRNA that is not turned into protein.
- **CDS**: the part of an mRNA that is translated, from start codon to stop codon.
- **Promoter**: DNA at the start of a gene where RNA polymerase assembles.
- **Enhancer**: a regulatory DNA element that boosts a gene's transcription, often from far away.
- **Transcription factor (TF)**: a protein that binds a specific short DNA motif to turn genes up or down.
- **Transcript**: any single RNA molecule produced from a gene.
- **Isoform**: one of several alternative RNA (or protein) versions made from the same gene.
- **Reading frame**: the way a sequence is chopped into consecutive codons.
- **Variant**: any difference from the reference sequence.
- **SNP**: a single-base difference that is common in the population.
- **PTM**: a chemical change made to a protein after it has been built.
"""
G[2] = """
- **Gene symbol**: the short official name of a gene, e.g. TP53.
- **Ortholog**: the corresponding gene in a different species (human TP53 ↔ mouse Trp53).
- **Paralog**: a related gene in the same species that arose by duplication (e.g. KRAS and NRAS).
- **Gene family**: a group of related genes named with a shared root plus numbers or letters.
- **Pseudogene**: a broken, non-functional copy of a gene.
- **Antisense RNA**: an RNA transcribed from the opposite strand of another gene.
- **Kilodalton (kDa)**: a unit of molecular mass equal to 1,000 Da; an average amino acid is ~0.11 of these.
- **Knockout**: an organism (or cell) in which a gene has been deliberately deleted or disabled.
- **Floxed**: describes a gene flanked by loxP sites, so it can be deleted wherever Cre is active.
- **Cre**: the recombinase enzyme that deletes DNA lying between two loxP sites.
- **HLA**: the highly variable human immune genes that display protein fragments to T cells.
- **Germline**: describes a variant that is inherited and present in every cell of the body.
- **Somatic**: describes a variant acquired in some cells during life, e.g. in a tumor.
- **Reference sequence**: the specific stored sequence record that variant coordinates are counted against.
- **Accession**: a database's stable identifier for a record.
- **Version**: the number after the dot in an accession, which increments when the stored sequence changes.
- **Assembly**: one released edition of a reference genome, e.g. GRCh38.
- **HGVS**: the standard notation for describing variants (c., p., g. prefixes).
- **rsID**: a dbSNP identifier for a known variant position.
- **Hotspot**: a position mutated unusually often in cancer.
- **Canonical isoform**: the transcript or protein version a database treats as the default.
"""
G[3] = """
- **Annotation**: labels on raw sequence marking where genes, exons and other features are and what they do.
- **Accession**: a database's stable ID for a record (see Unit 2).
- **Reference genome**: the standard genome sequence that coordinates refer to, e.g. hg38 (see Unit 6).
- **Track**: one row of data drawn along genome coordinates in a browser.
- **Ortholog**: the same gene in another species (see Unit 2).
- **Paralog**: a related gene in the same species, from duplication (see Unit 2).
- **Expression**: how much RNA or protein a gene produces in a sample.
- **eQTL**: a genetic variant associated with how strongly a gene is expressed.
- **Allele frequency (AF)**: the fraction of chromosomes in a population carrying a particular variant version.
- **Exome sequencing**: sequencing only the protein-coding exons (~1–2% of the genome).
- **Whole-genome sequencing (WGS)**: sequencing all of an individual's DNA.
- **Mendelian disease**: a disease caused mainly by variants in a single gene.
- **Pathogenic**: clinical label meaning disease-causing.
- **Benign**: clinical label meaning harmless.
- **Loss-of-function (LoF)**: describes a variant that destroys the gene product (nonsense, frameshift, splice-site).
- **Constraint**: how strongly natural selection removes damaging variants from a gene.
- **X-ray crystallography**: determining a 3D structure from how a protein crystal diffracts radiation.
- **Cryo-EM**: determining a 3D structure by electron microscopy of flash-frozen samples.
- **NMR**: determining a 3D structure from magnetic resonance of molecules in solution.
- **Domain**: an independently folding unit of a protein (see Unit 4).
- **Pathway**: a set of molecules acting in sequence to carry out a process (see Unit 5).
- **Ontology**: a controlled vocabulary whose terms have defined relationships to each other.
- **Enrichment analysis**: testing whether a gene list contains more members of some category than chance predicts.
- **Cell line**: cells that grow indefinitely in the lab, often derived from a tumor.
- **Raw data**: the sequencer's original reads, before any processing.
- **Processed data**: tables derived from reads, such as gene counts or peak calls.
"""
G[4] = """
- **Amino acid**: a protein building block: a shared backbone part plus a distinctive side chain.
- **Side chain (R group)**: the variable part of an amino acid that gives it its chemistry.
- **Peptide bond**: the link joining one amino acid's carboxyl group to the next one's amino group.
- **Residue**: one amino acid within a protein chain, e.g. "position 175".
- **Backbone**: the repeating chain of atoms formed by peptide bonds, excluding side chains.
- **N-terminus**: the start of a protein chain, with a free amino group.
- **C-terminus**: the end of a protein chain, with a free carboxyl group.
- **Polypeptide**: an unbranched chain of amino acids.
- **Hydrophobic**: "water-fearing"; describes oily side chains buried inside proteins and membranes.
- **Polar**: "water-loving"; describes side chains that interact with water.
- **Charged**: carrying a net positive or negative charge at the cell's near-neutral pH.
- **Hydrogen bond**: a weak attraction between an H atom on N or O and another N or O; holds helices and sheets together.
- **Fold**: the overall 3D arrangement of a protein chain.
- **Domain**: a compact, independently folding unit of a protein.
- **Homolog**: a protein or gene related to another by common ancestry.
- **MSA**: many related sequences lined up position by position, so each column is an equivalent position.
- **Ångström (Å)**: 10⁻¹⁰ m; bonded atoms are ~1–2 of these apart.
- **Enzyme**: a protein that speeds up a chemical reaction.
- **Substrate**: the molecule an enzyme acts on.
- **Active site**: the pocket where an enzyme's reaction happens.
- **Ligand**: any molecule that binds a protein, such as a hormone or drug.
- **Receptor**: a protein that binds a signal and relays it, often spanning the membrane.
- **Transmembrane (TM)**: crossing the cell membrane.
- **ATP**: the cell's energy currency and the phosphate donor for kinases.
- **Antibody**: an immune protein that binds one specific target molecule.
- **Antigen**: the target molecule an antibody binds.
- **Inhibitor**: a molecule (often a drug) that blocks a protein's activity.
"""
G[5] = """
- **Signaling pathway**: a chain of molecules passing a message from a signal to a response inside the cell.
- **Ligand**: a signal molecule that binds a receptor.
- **Receptor**: a protein that binds a signal molecule and relays its message.
- **Growth factor**: a protein signal telling cells to grow and divide.
- **Cytokine**: a protein signal coordinating immune responses.
- **Kinase**: an enzyme that adds a phosphate group to a protein.
- **Phosphatase**: an enzyme that removes a phosphate group from a protein.
- **Phosphorylation**: the addition of a phosphate group (written p-ERK or pS473).
- **GTPase**: a protein switch that is ON when bound to GTP and OFF after cutting it to GDP.
- **GEF**: a protein that switches a small GTPase ON by swapping its GDP for GTP.
- **GAP**: a protein that switches a small GTPase OFF by speeding up its GTP hydrolysis.
- **Adaptor**: a protein without enzyme activity that links other proteins together.
- **Dimerization**: two proteins pairing up.
- **Transcription factor (TF)**: a protein that binds DNA to turn genes on or off (see Unit 1).
- **Target gene**: a gene whose transcription a given TF controls.
- **E3 ubiquitin ligase**: an enzyme that attaches the small "destroy me" tag protein to specific targets.
- **Proteasome**: the cellular machine that shreds tagged proteins.
- **Negative feedback**: a pathway's output switching off its own input.
- **Proliferation**: cells dividing and multiplying in number.
- **Oncogene**: a gene whose overactivity (gain of function) drives cancer.
- **Tumor suppressor**: a gene whose loss of function drives cancer.
- **Amplification**: extra copies of a gene in the genome.
- **Fusion gene**: two genes joined into one by a chromosome rearrangement.
- **Apoptosis**: programmed, orderly cell suicide.
- **Caspase**: a protein-cutting enzyme that executes programmed cell death.
- **Mitochondria**: the cell's energy-producing compartments, also central to programmed cell death.
- **Cell cycle**: the sequence of phases by which a cell copies its DNA and divides.
- **Mitosis**: the division step in which duplicated chromosomes separate.
- **Checkpoint**: a control point that halts division if something is wrong.
- **Cyclin**: a regulatory protein whose level rises and falls through division phases, activating a partner kinase.
- **CDK**: the kinase that is switched on by binding a cyclin.
- **Synthetic lethality**: losing either of two genes is survivable, but losing both kills the cell.
- **Western blot**: a lab assay that detects a specific protein (or phospho-form) with antibodies after gel separation.
"""
G[6] = """
- **Sequencing**: reading the order of bases in DNA or RNA molecules.
- **Read**: one sequenced fragment, typically 50–300 bases on Illumina machines.
- **Paired-end**: describes reading both ends of each DNA fragment, giving two linked reads (R1, R2).
- **Library**: the prepared pool of adapter-tagged DNA fragments loaded onto the sequencer.
- **PCR**: a reaction that copies DNA many times, creating duplicates of each molecule.
- **Reference genome**: the standard genome sequence that reads are compared against.
- **Genome build**: one released edition of the reference genome, e.g. GRCh38.
- **Alignment**: finding where each read came from in the reference.
- **Coverage**: how many reads overlap a given position.
- **Genotype**: which alleles an individual carries at a locus.
- **Phased**: describes genotypes where it is known which alleles sit together on the same chromosome copy.
- **Interval**: a region given as chromosome, start and end.
- **0-based**: coordinate convention in which the first base of a chromosome is numbered zero.
- **1-based**: coordinate convention in which the first base of a chromosome is numbered one.
- **cDNA**: DNA copied from RNA by reverse transcriptase.
- **Normalization**: rescaling counts so that samples are comparable.
- **Fold change**: the ratio of expression between two conditions, usually reported on a log2 scale.
- **FDR**: the expected fraction of false positives among results called significant.
- **Cell barcode**: a short tag identifying which cell a read came from.
- **UMI**: a short random tag identifying which original molecule a read came from.
- **Sparse matrix**: a matrix that is mostly zeros, stored efficiently.
- **Batch effect**: technical differences between samples processed at different times, places or ways.
- **Peak**: a genomic region with many more reads than background.
- **Nucleosome**: ~147 bp of DNA wrapped around a histone protein core.
- **Histone mark**: a chemical tag on the proteins DNA wraps around that signals chromatin state, e.g. H3K27ac.
- **CRISPR-Cas9**: a programmable DNA-cutting system steered by a short RNA.
- **sgRNA**: the short RNA that points Cas9 at its target sequence.
- **Lentivirus**: a virus used to insert genes permanently into cells' genomes.
- **MOI**: the average number of viruses delivered per cell.
- **Mass spectrometry**: a technique measuring the mass-to-charge ratio (m/z) of ionized molecules.
- **Peptide**: a short piece of protein.
"""
G[7] = """
- **Benchmark**: a fixed dataset plus metric used to compare methods.
- **Zero-shot**: making predictions for a task without training on any of its labels.
- **Fine-tuning**: further training a pretrained model on task labels.
- **Probing**: training a small model on top of a frozen model's embeddings.
- **Embedding**: a model's internal vector representation of an input, such as a protein or a cell.
- **Masked language model (MLM)**: a model trained to fill in hidden tokens (ESM-2, DNABERT).
- **Autoregressive model**: a model that predicts each next token from the previous ones (ProGen, Evo).
- **Log-likelihood**: the log probability a model assigns to a sequence or token.
- **Token**: the unit a model reads.
- **Tokenization**: how raw data is split into the units a model reads.
- **k-mer**: a substring of length k, e.g. 6 bases.
- **One-hot encoding**: representing each base as a vector with a single 1 (A = 1000, C = 0100…).
- **Context length**: how much sequence a model sees at once.
- **Fitness**: how well a protein variant performs a measured function.
- **DMS**: measuring the fitness of thousands of variants of one protein in a single experiment.
- **Variant effect prediction (VEP)**: predicting whether a sequence change is harmful.
- **Sequence identity**: the percentage of aligned positions where two sequences share the same residue.
- **Homolog**: a sequence related to another by common ancestry (see Unit 4).
- **Data leakage**: test examples too similar to training examples, which inflates scores.
- **Held-out**: deliberately kept out of training for testing.
- **Foundation model**: a large model pretrained on broad data and adapted to many tasks.
- **Perturbation**: an experimental change to cells (gene knockout, drug) whose effect is measured.
- **Spearman's ρ**: correlation between two rankings, from −1 to 1.
- **Contact**: two residues close together in 3D, typically under 8 Å apart.
"""
if __name__ == "__main__":
    import re
    for n, block in G.items():
        p = f"lessons/u{n}.md"
        s = open(p).read()
        i = s.index("### Key terms")
        j = s.index("\n## ", i)
        s = s[:i] + "### Key terms\n" + block.rstrip() + "\n" + s[j:]
        open(p, "w").write(s)
        print(p, len(block.strip().splitlines()), "terms")
