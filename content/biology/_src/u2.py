from common import build
import os
lesson = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"lessons","u2.md")).read()
from cards_u2 import cards, glossary_accept
quiz = [
("Which is the correct HGNC symbol for the β-catenin gene?",["β-CAT","CTNNB1","Ctnnb1","CATNB"],1,"HGNC symbols avoid Greek letters; CTNNB1 = catenin beta 1. Ctnnb1 is the mouse style."),
("In NM_000546.6:c.215C>G, what does c.215 refer to?",["Position 215 of chromosome 17","Position 215 counting from the A of the ATG start codon","Amino acid 215","Position 215 from the transcription start site"],1,"c. numbering starts at the A of the start codon (c.1)."),
("Which identifier is a UniProt accession?",["ENSP00000269305","NP_000537","P04637","1TUP"],2,"P04637 follows the UniProt 6-character accession format. ENSP is Ensembl protein, NP_ is RefSeq protein, 1TUP is PDB."),
("What does the XM_ prefix indicate?",["Curated mRNA","Predicted mRNA from automated annotation","Mitochondrial transcript","Chromosome sequence"],1,"X-prefixed RefSeq records are computational predictions; N-prefixed ones are curated."),
("HLA-A*02:01: the '02' is the:",["Specific protein","Allele group","Synonymous variant field","Exon number"],1,"Field 1 is the allele group, field 2 the specific protein."),
("A mouse paper writes 'Trp53'. The corresponding human gene symbol is:",["TRP53","P53","TP53","Tp53"],2,"Mouse Trp53 is the ortholog of human TP53; mouse uses first-letter capitalization."),
("p.Arg175His could also be written as:",["R175H","H175R","c.175G>A","rs175"],0,"Single-letter protein shorthand: R (Arg) → H (His) at position 175."),
("Which HGVS prefix denotes a genomic coordinate?",["c.","g.","p.","r."],1,"g. = genomic reference (e.g., relative to NC_ accession)."),
("Why did HGNC rename SEPT1 to SEPTIN1?",["Discovery of a new function","Conflict with mouse nomenclature","Spreadsheet software converted it into a date","Greek letters were removed"],2,"Excel autoconversion corrupted gene lists; HGNC renamed affected symbols in 2020."),
("What does the version in NC_000017.11 tell you?",["The gene count","Which assembly the chromosome sequence belongs to (GRCh38)","The chromosome arm","Number of isoforms"],1,"NC_ version numbers change with assembly; chr17 is .10 in GRCh37 and .11 in GRCh38."),
("Which statement about rsIDs is TRUE?",["They specify one exact alt allele and assembly","They identify a variant cluster at a position, independent of assembly","They are issued by UniProt","They only describe protein changes"],1,"dbSNP rsIDs name a locus plus its known alleles; coordinates come from mapping to an assembly."),
("Yeast systematic name YAL001C: 'C' means:",["Centromere","Coding","Crick strand","Chromosome C"],2,"W/C indicate Watson or Crick strand; the third letter is the chromosome arm (L/R)."),
("Which HGNC symbol indicates a pseudogene?",["PTENP1","PTEN-AS1","MIR21","LINC00473"],0,"A 'P' + number suffix marks a pseudogene."),
("Which database's IDs look like ENSG00000141510?",["NCBI RefSeq","Ensembl","UniProt","HGNC"],1,"ENS + species code + feature type (G/T/P) + 11 digits."),
]
build(2,"naming-conventions","Naming conventions and identifiers","How to read gene and protein names across species, HLA alleles, HGVS variant notation and rsIDs, and the identifier formats from Ensembl, RefSeq, UniProt, PDB and others. Parsing these on sight is what lets you join datasets and read methods sections.",lesson,cards,quiz,glossary_accept)
