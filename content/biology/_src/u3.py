from common import build
import os
lesson = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"lessons","u3.md")).read()
from cards_u3 import cards
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
