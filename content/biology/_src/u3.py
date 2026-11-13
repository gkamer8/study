from common import build
lesson = r"""
## The mental model: one question, one database

Most biological lookups answer one of a few questions: *what is this gene?*, *what does its protein look like?*, *where and when is it expressed?*, *what variants exist and do they matter?*, *what does it interact with?*, or *where is the raw data?* Each has a canonical resource. Learn the mapping and you'll always know where to look, and what a paper means by "we downloaded X from Y".

## Genes and genomes

- **NCBI Gene**: one page per gene with a numeric ID (TP53 = 7157), a summary, aliases, RefSeq transcripts, and links out. It is a good first stop for *"what is this gene?"*.
- **Ensembl** (EMBL-EBI): genome annotation for hundreds of vertebrates. It holds gene, transcript and protein models (ENSG/ENST/ENSP), comparative genomics (orthologs, paralogs), the **VEP** variant annotator, and **BioMart** for bulk ID conversion. **GENCODE** is the human/mouse annotation set behind Ensembl's human and mouse gene models.
- **UCSC Genome Browser**: a visual genome browser built on assembly coordinates (hg19, hg38). Its tracks stack genes, conservation, ENCODE regulatory data, repeats, and variants at any locus. Tools include the **Table Browser** for downloads and **liftOver** for converting coordinates between assemblies. Use it to answer *"what's at chr7:140,753,336?"*.
- **HGNC**: the authority on approved human gene symbols, previous symbols and aliases.

## Proteins and structures

- **UniProt** (UniProtKB): the reference for protein sequences and function. Each entry has a curated function summary, domains, PTM sites, isoforms, disease variants, and cross-references. Swiss-Prot entries are reviewed; TrEMBL entries are unreviewed. **UniRef** clusters (UniRef50/90/100) are standard pretraining sets for protein language models.
- **PDB** (RCSB PDB in the US, PDBe in Europe, PDBj in Japan; together wwPDB): experimentally determined 3D structures from X-ray crystallography, cryo-EM and NMR. It holds roughly a couple of hundred thousand entries, each with a 4-character ID. It answers *"is there an experimental structure, at what resolution, bound to what?"*.
- **AlphaFold DB** (DeepMind + EMBL-EBI): predicted structures for more than 200 million UniProt sequences, colored by pLDDT, with PAE plots. IDs look like AF-P04637-F1.
- **InterPro / Pfam**: protein families and domains. Pfam (PF00069 = protein kinase domain) is now served through the InterPro website. These answer *"what domains does this protein have?"*.

## Expression

- **GTEx** (Genotype-Tissue Expression): bulk RNA-seq across ~50 tissues from roughly 1,000 post-mortem donors, plus **eQTLs** (variants associated with expression levels). It answers *"in which normal tissues is this gene expressed, and which variants change its expression?"*.
- **Human Protein Atlas**: protein and RNA expression by tissue, cell type and subcellular location, with antibody staining images.
- **CELLxGENE** (CZI): curated single-cell datasets and the Census, tens of millions of cells in a standard AnnData schema. It is a common pretraining source for single-cell foundation models.
- **GEO** (Gene Expression Omnibus, NCBI): the archive for processed functional-genomics data such as expression matrices and peak files. Accessions: **GSE** (series/study), **GSM** (sample), **GPL** (platform), GDS (curated dataset).
- **SRA** (Sequence Read Archive): raw sequencing reads. Accessions: **SRP** study, **SRX** experiment, **SRS** sample, **SRR** run (the files you download). ENA (ERR…) and DDBJ (DRR…) mirror it as part of INSDC. Related IDs: **BioProject** (PRJNA…) and **BioSample** (SAMN…).

## Variants and disease

- **dbSNP**: catalog of short variants and their rsIDs.
- **gnomAD** (Genome Aggregation Database): allele frequencies from hundreds of thousands of exomes and genomes (v4 ≈ 800k individuals), broken down by genetic ancestry. It also provides **gene constraint** scores: pLI and **LOEUF** (loss-of-function observed/expected upper bound fraction; low = intolerant of loss of function). It answers *"how common is this variant in the general population?"*. A variant seen in many healthy people is unlikely to cause severe dominant disease.
- **ClinVar**: submitted clinical interpretations. Labels are pathogenic, likely pathogenic, **VUS** (uncertain significance), likely benign, benign, with a review-status star rating. Accessions: VCV (variant), RCV (variant-condition), SCV (submission). It is the standard benchmark source for variant-effect predictors.
- **OMIM**: curated catalog of Mendelian genes and phenotypes with 6-digit MIM numbers. Prefix symbols: `*` gene, `#` phenotype with known molecular basis, `%` phenotype with unknown basis, `+` gene and phenotype combined.
- **COSMIC**, **cBioPortal**, **TCGA**: somatic mutations in cancer and multi-omic tumor cohorts.
- **GWAS Catalog**: published trait-variant associations.

## Function, pathways and interactions

- **Gene Ontology (GO)**: a controlled vocabulary in three aspects: **Molecular Function**, **Biological Process**, **Cellular Component**. Terms are GO:0006915 ("apoptotic process") style, arranged in a DAG. Annotations carry evidence codes; IEA marks automatic electronic annotation, the weakest kind. GO is used in **enrichment analysis**.
- **KEGG**: pathway maps (hsa04010 = human MAPK signaling) plus metabolism; gene IDs look like hsa:7157.
- **Reactome**: open, curated, hierarchical pathway database (R-HSA-…). Often used with KEGG and MSigDB for gene-set enrichment.
- **STRING**: protein-protein *association* networks that combine experiments, co-expression, text mining and genomic context into a combined confidence score (0–1, shown as 0–1000 in files). Not every edge is a physical interaction.
- **BioGRID / IntAct**: curated experimental interactions.

## Perturbation and chemistry

- **DepMap**: CRISPR knockout screens across ~1,000+ cancer cell lines. Gene effect (Chronos) scores show which genes cells depend on.
- **ChEMBL**: bioactive molecules and assay data (CHEMBL25 = aspirin). **PubChem**: chemical structures.
- **ENCODE**: functional-genomics experiments (ChIP-seq, ATAC/DNase, RNA-seq) and candidate cis-regulatory elements (cCREs). It is a main training source for sequence-to-function models.

## How you'll see this in a paper

- "Data are available at GEO under accession GSE123456": processed matrices are there, and the raw FASTQs are linked through SRA (SRR runs).
- "Variants with gnomAD AF > 0.01 were treated as benign": a frequency filter.
- "Evaluated on ClinVar missense variants (≥1 star) not in the training set": standard variant-effect benchmarking. Check for circularity.
- "GO enrichment (FDR < 0.05) revealed…": gene-set over-representation, usually against a background list.
- "Structures were taken from AlphaFold DB where no PDB entry existed."
"""
cards = [
("recall","NCBI Gene: what question does it answer?","'What is this gene?' Summary, aliases, numeric Gene ID, RefSeq links",["NCBI"]),
("recall","Ensembl: main offerings?","Genome annotation (ENSG/ENST/ENSP), orthologs/paralogs, VEP, BioMart",["Ensembl"]),
("recall","What is GENCODE?","The human/mouse gene annotation set underlying Ensembl gene models",["Ensembl","annotation"]),
("recall","What is VEP?","Ensembl's Variant Effect Predictor: annotates variant consequences (missense, splice, etc.)",["Ensembl","variants"]),
("recall","What is BioMart used for?","Bulk queries and ID conversion (e.g., ENSG → HGNC symbol)",["Ensembl"]),
("recall","UCSC Genome Browser: what question does it answer?","'What's at this locus?' Coordinate-based tracks: genes, conservation, regulation, variants",["UCSC"]),
("recall","What does liftOver do?","Converts coordinates between genome assemblies (e.g., hg19 → hg38)",["UCSC","assemblies"]),
("recall","UniProt: what question does it answer?","'What does this protein do?' Sequence, function, domains, PTMs, isoforms, variants",["UniProt"]),
("recall","What are UniRef50/90/100?","UniProt sequences clustered at 50/90/100% identity; common PLM training sets",["UniProt","ml"]),
("recall","PDB: what does it contain?","Experimentally determined 3D structures (X-ray, cryo-EM, NMR)",["PDB"]),
("recall","What is wwPDB?","Worldwide PDB consortium: RCSB PDB (US), PDBe (EU), PDBj (Japan), and others",["PDB"]),
("recall","AlphaFold DB: what does it contain?","Predicted structures for >200M UniProt sequences, with pLDDT and PAE",["AlphaFold"]),
("recall","Pfam and InterPro: what question?","'What domains/families is this protein in?' Pfam is now accessed via InterPro",["domains"]),
("recall","GTEx: what question does it answer?","'Where is this gene expressed in normal tissues, and which variants affect expression (eQTLs)?'",["GTEx","expression"]),
("recall","What is an eQTL?","A genetic variant associated with expression level of a gene",["GTEx","genetics"]),
("recall","CELLxGENE: what is it?","CZI's curated single-cell data portal and Census; standard schema, common scFM pretraining source",["single-cell"]),
("recall","GEO vs SRA?","GEO: processed functional-genomics data and metadata; SRA: raw sequencing reads",["GEO","SRA"]),
("identify","GSE / GSM / GPL","GEO series (study) / sample / platform",["GEO","identifiers"]),
("identify","SRP / SRX / SRS / SRR","SRA study / experiment / sample / run (downloadable read files)",["SRA","identifiers"]),
("identify","ERR1234567 or DRR…","Run accessions from ENA (E) or DDBJ (D), INSDC mirrors of SRA",["SRA","identifiers"]),
("identify","PRJNA123456 / SAMN01234567","NCBI BioProject / BioSample accessions",["identifiers"]),
("recall","gnomAD: what question does it answer?","'How common is this variant in the general population (by ancestry)?' Also gene constraint",["gnomAD","variants"]),
("recall","What does a low LOEUF mean?","Gene has fewer loss-of-function variants than expected → intolerant to LoF (constrained)",["gnomAD"]),
("apply","A candidate 'disease' variant has allele frequency 5% in gnomAD. Implication for a rare severe dominant disorder?","Very unlikely causal; too common in the general population",["gnomAD","variants"]),
("recall","ClinVar: what does it hold?","Submitted clinical interpretations of variants (P/LP/VUS/LB/B) with review stars",["ClinVar"]),
("identify","VCV / RCV / SCV","ClinVar variant / variant-condition record / individual submission",["ClinVar","identifiers"]),
("recall","What is a VUS?","Variant of uncertain significance",["ClinVar"]),
("recall","OMIM: what is it?","Curated catalog of Mendelian genes and phenotypes (6-digit MIM numbers)",["OMIM"]),
("identify","OMIM prefix # vs *","# = phenotype with known molecular basis; * = gene",["OMIM"]),
("recall","dbSNP?","NCBI's catalog of short variants; issues rsIDs",["variants"]),
("recall","COSMIC / cBioPortal / TCGA?","Cancer somatic mutation catalog / tumor cohort explorer / The Cancer Genome Atlas multi-omic data",["cancer"]),
("recall","Three aspects of GO?","Molecular Function, Biological Process, Cellular Component",["GO"]),
("identify","GO:0006915","Gene Ontology term 'apoptotic process'",["GO","identifiers"]),
("recall","GO evidence code IEA?","Inferred from Electronic Annotation: automatic, unreviewed (weakest)",["GO"]),
("identify","hsa04010","KEGG pathway: human MAPK signaling",["KEGG","identifiers"]),
("identify","hsa:7157","KEGG gene ID for human TP53 (uses NCBI Gene ID)",["KEGG","identifiers"]),
("identify","R-HSA-109581","Reactome pathway ID (human): Apoptosis; R-HSA- prefix",["Reactome","identifiers"]),
("recall","STRING: what do edges represent?","Functional associations (experiments, co-expression, text mining, etc.), with a combined confidence score, not necessarily physical binding",["STRING"]),
("recall","DepMap: what question?","'Which genes do cancer cell lines depend on?' Genome-wide CRISPR screen gene effect scores",["DepMap"]),
("recall","ENCODE?","Consortium functional-genomics data (ChIP-seq, DNase/ATAC, RNA-seq) and candidate cis-regulatory elements",["ENCODE"]),
("identify","CHEMBL25","ChEMBL compound ID (aspirin)",["ChEMBL","identifiers"]),
("apply","You need raw FASTQs for a paper that lists GSE123456. Path?","GEO series → linked SRA project → download SRR runs (e.g., with SRA Toolkit)",["GEO","SRA"]),
("apply","You want to know if a protein has an experimental structure bound to a drug. Where?","PDB (RCSB/PDBe), searched by UniProt accession",["PDB"]),
("apply","You want which tissues express a gene at the protein level, with images.","Human Protein Atlas",["expression"]),
]
quiz = [
("You want to know how frequent a missense variant is among healthy people of different ancestries. Best resource?",["ClinVar","gnomAD","OMIM","PDB"],1,"gnomAD aggregates population allele frequencies by ancestry."),
("An SRR accession refers to:",["A GEO sample","A sequencing run (raw reads)","A study","A BioProject"],1,"SRR = run; the downloadable reads."),
("Which resource provides tissue-level expression and eQTLs from post-mortem donors?",["GTEx","ENCODE","STRING","KEGG"],0,"GTEx = Genotype-Tissue Expression."),
("Which is NOT one of the three GO aspects?",["Molecular Function","Biological Process","Cellular Component","Pathway Topology"],3,"GO has MF, BP and CC."),
("STRING edges primarily represent:",["Only crystal-structure contacts","Functional associations from multiple evidence types","Genetic linkage","Transcription factor binding"],1,"STRING integrates experiments, co-expression, text mining, and more."),
("A variant is labeled 'VUS' in ClinVar. This means:",["Validated as pathogenic","Uncertain significance","Very unusual somatic","Variant under selection"],1,"VUS = variant of uncertain significance."),
("Which tool converts genomic coordinates from hg19 to hg38?",["BLAST","liftOver","VEP","BioMart"],1,"UCSC liftOver (or CrossMap) converts between assemblies."),
("Pfam domain annotations are now accessed through:",["UniProt only","InterPro","PDB","KEGG"],1,"The Pfam website was retired and its data are served via InterPro."),
("A paper's single-cell foundation model pretraining corpus most likely came from:",["CELLxGENE Census","ClinVar","OMIM","PDB"],0,"CELLxGENE provides large standardized single-cell datasets."),
("Low LOEUF for a gene indicates:",["High expression","Tolerance to loss-of-function","Intolerance to loss-of-function","Many pathogenic ClinVar entries"],2,"Fewer observed LoF variants than expected means constraint."),
("Where are predicted structures with per-residue pLDDT for most UniProt proteins found?",["PDB","AlphaFold DB","Reactome","GEO"],1,"AlphaFold DB hosts >200M predictions."),
("OMIM entry prefixed with '#' denotes:",["A gene","A phenotype with known molecular basis","A phenotype with unknown basis","A withdrawn entry"],1,"# = phenotype with known molecular basis; * = gene; % = unknown basis."),
("Which database would you use to find which genes are essential across cancer cell lines?",["DepMap","gnomAD","GTEx","ChEMBL"],0,"DepMap aggregates CRISPR knockout screens across cell lines."),
("Which resource issues rsIDs?",["ClinVar","dbSNP","Ensembl","HGNC"],1,"dbSNP assigns Reference SNP (rs) IDs."),
]
build(3,"databases","Databases and where to find things","A map from biological questions to the canonical database that answers them: genes, proteins and structures, expression, variants and disease, pathways and interactions, and raw data archives. Includes the accession formats you'll see in data-availability statements.",lesson,cards,quiz)
