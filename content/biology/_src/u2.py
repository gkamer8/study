from common import build
lesson = r"""
## Why naming matters

Biology papers use one entity under many names: TP53, p53, *Trp53*, P04637, ENSG00000141510, Entrez Gene 7157 and HGNC:11998 all refer to the same human gene or its protein. If you can parse names and identifiers on sight, you can join datasets, find the right database entry, and catch errors such as a mouse gene symbol in a human analysis or a hg19 coordinate in a hg38 file.

## Human gene symbols (HGNC)

The **HUGO Gene Nomenclature Committee (HGNC)** approves one symbol per human gene. Symbols are **uppercase letters and Arabic numerals**, with no Greek letters (β-catenin's gene is **CTNNB1**, TGF-β1's is **TGFB1**). Each gene also has a stable ID (TP53 = **HGNC:11998**) and a descriptive name ("tumor protein p53").

Conventions:
- **Gene in italics, protein in roman type**: *TP53* is the gene, TP53 (or p53) the protein. Many papers ignore this, but careful ones follow it.
- **Family-based names with numbers**: *CYP2D6* = cytochrome P450, family 2, subfamily D, member 6. *SLC2A1* = solute carrier family 2 member 1 (the GLUT1 glucose transporter). *KRT*, *ZNF*, *HOX*, *OR* (olfactory receptor) and *HLA* work the same way.
- **Placeholder names**: *C9orf72* means "chromosome 9 open reading frame 72", a gene found before its function was known. *LINC01234*-style names are long intergenic non-coding RNAs. *FAM*##A means "family with sequence similarity".
- **Suffixes**: **P** + number = pseudogene (*PTENP1*); **-AS1** = antisense RNA; **MIR**## = microRNA gene (*MIR21*; the mature miRNA is written hsa-miR-21-5p).
- **Symbols change.** In 2020 HGNC renamed genes that Excel auto-converted to dates: SEPT1 → *SEPTIN1*, MARCH1 → *MARCHF1*. Old datasets still contain the old symbols, or mangled ones like "1-Sep". Always map through previous symbols and aliases, or better, use stable IDs.

**Protein names vs gene symbols.** Many proteins keep historical names. p53 is named for its apparent ~53 kDa size on a gel. HER2 is encoded by *ERBB2*, CD45 by *PTPRC*, Ki-67 by *MKI67*, GLUT1 by *SLC2A1*. One locus can encode several proteins: *CDKN2A* encodes **p16^INK4a** and **p14^ARF** from alternative first exons read in different frames.

## Other species

- **Mouse/rat**: only the first letter is capitalized, in italics: *Trp53*, *Kras*. Proteins are written all caps (TRP53). Alleles go in superscripts: *Kras^LSL-G12D^*, *Trp53^fl/fl^* (floxed, meaning loxP sites that Cre recombinase can excise).
- **Yeast (S. cerevisiae)**: three uppercase letters plus a number, italic, for the wild-type gene (*CDC28*). A lowercase symbol means a recessive mutant allele (*cdc28*). The protein is Cdc28 or Cdc28p. Systematic ORF names encode position: **YFL039C** (*ACT1*) = Yeast, chromosome F (6), Left arm, ORF 039, on the Crick strand (C; W = Watson).
- **Zebrafish**: all lowercase italic (*tp53*). **Drosophila**: names often come from mutant phenotypes (*white*, *hedgehog*).

## Immune genes: HLA alleles

**HLA-DRB1\*15:01** reads as: gene *HLA-DRB1*, then `*`, then **field 1 = allele group (15)**, then **field 2 = the specific HLA protein (01)**. Further fields mark synonymous coding differences (field 3) and non-coding differences (field 4). A suffix letter such as N means null (not expressed). "Two-field" or "four-digit" typing means the protein-level resolution.

## Variant notation

**rsIDs** (rs1042522) are dbSNP reference SNP cluster IDs. They name a *position plus its known alleles*, not one specific change, and they don't specify an assembly.

**HGVS** notation states a change relative to a specific reference sequence:

- `NM_000546.6:c.215C>G`: coding DNA reference. **c.1 is the A of the ATG start.** c.-14 lies in the 5' UTR, c.\*20 lies 20 nt after the stop codon in the 3' UTR, and c.88+1G>T is the first base of the intron after coding position 88 (c.89-2 is in the intron before c.89).
- `NP_000537.3:p.Pro72Arg` or `p.(P72R)`: protein. Parentheses mean the effect is predicted, not measured. `p.Arg196Ter` or `p.Arg196*` = nonsense. `p.Arg213ProfsTer8` = frameshift starting at Arg213, which becomes Pro, with a stop 8 codons later.
- `NC_000017.11:g.7676154G>C`: genomic. The accession version (.11) fixes the assembly.
- Also `n.` (non-coding RNA), `m.` (mitochondrial, e.g. m.3243A>G), `r.` (RNA).
- Indels: `c.5266dupC` (dup), `c.68_69delAG` (del), `delins`.

That example is one variant written three ways: TP53 c.215C>G = p.Pro72Arg = rs1042522, the common P72R polymorphism. The famous cancer hotspots are mostly given at protein level: **BRAF V600E** (c.1799T>A), **KRAS G12D** (c.35G>A), **EGFR L858R**.

## Identifier formats you must recognize

| Pattern | Source | Meaning |
|---|---|---|
| ENSG00000141510 | Ensembl | gene (ENST = transcript, ENSP = protein; ENSMUSG = mouse gene). A `.N` suffix is the version |
| NM_000546.6 | RefSeq | curated mRNA. NR_ = curated non-coding RNA; XM_/XR_ = predicted (computational) |
| NP_000537.3 | RefSeq | curated protein (XP_ = predicted) |
| NC_000017.11 | RefSeq | complete chromosome sequence (version = assembly; chr17 is .11 in GRCh38, .10 in GRCh37). NG_ = genomic region |
| P04637, A0A024R1R8 | UniProt | protein accession: 6 or 10 characters. P53_HUMAN is the entry *name* (mnemonic) |
| P04637-2 | UniProt | isoform 2 |
| 7157 | NCBI Gene (Entrez) | numeric gene ID |
| HGNC:11998 | HGNC | gene ID |
| 1TUP | PDB | 4-character structure ID that starts with a digit |
| AF-P04637-F1 | AlphaFold DB | predicted structure for UniProt P04637, fragment 1 |
| rs1042522 | dbSNP | variant cluster |
| 191170 | OMIM | 6-digit MIM number |

UniProt **Swiss-Prot** entries are manually reviewed; **TrEMBL** entries are unreviewed and automatically annotated, and they make up the large majority. UniRef50/90/100 cluster UniProt at those identity levels and are the usual training sets for protein language models.

## How you'll see this in a paper

- "We mapped Ensembl IDs to HGNC symbols using biomaRt": they are joining annotation sources. Version suffixes are often stripped first.
- Supplementary tables with "MARCH1" or "1-Mar": a sign of an Excel-mangled or pre-2020 symbol list.
- "p.R175H", "R248Q", "R273H": TP53 hotspot missense mutations in single-letter protein notation.
- "Trained on UniRef50 (release 2021_03)": UniProt clusters at 50% identity.
- A clinical paper reports "NM_000059.4:c.5946delT": a BRCA2 frameshift relative to a specific transcript version. The version number matters because exon numbering can change between versions.
"""
cards = [
("recall","Which body approves human gene symbols?","HGNC (HUGO Gene Nomenclature Committee)",["HGNC"]),
("recall","Format rules for HGNC symbols?","Uppercase Latin letters and Arabic numerals; no Greek letters (e.g., CTNNB1 for β-catenin)",["HGNC"]),
("recall","Typographic convention for gene vs protein?","Gene italic (TP53), protein roman (TP53/p53)",["conventions"]),
("identify","HGNC:11998","HGNC ID for TP53",["HGNC","identifiers"]),
("recall","What does the 53 in p53 refer to?","Apparent molecular weight ~53 kDa on SDS-PAGE",["protein-names"]),
("identify","Decode CYP2D6.","Cytochrome P450, family 2, subfamily D, member 6",["families"]),
("identify","SLC2A1 is better known as?","GLUT1 glucose transporter (solute carrier family 2 member 1)",["families","aliases"]),
("identify","What does C9orf72 mean?","Chromosome 9 open reading frame 72: placeholder name from before the function was known",["placeholders"]),
("identify","Gene symbol suffix 'P1', e.g., PTENP1?","Pseudogene 1 of PTEN",["suffixes"]),
("identify","Gene symbol suffix '-AS1'?","Antisense RNA 1 (non-coding transcript antisense to the named gene)",["suffixes"]),
("identify","LINC01234-style symbol?","Long intergenic non-protein-coding RNA",["suffixes"]),
("identify","MIR21 vs hsa-miR-21-5p?","MIR21 = microRNA gene; hsa-miR-21-5p = mature human miRNA from the 5' arm",["suffixes"]),
("recall","Why were SEPT1 and MARCH1 renamed in 2020?","Excel auto-converted them to dates; now SEPTIN1 and MARCHF1",["HGNC","data-hygiene"]),
("apply","You see '1-Mar' in a supplementary gene list. What happened?","Excel converted the symbol MARCH1 (now MARCHF1) to a date",["data-hygiene"]),
("identify","HER2 protein is encoded by which gene?","ERBB2",["aliases"]),
("identify","CD45 is encoded by which gene?","PTPRC",["aliases"]),
("identify","Ki-67 gene symbol?","MKI67",["aliases"]),
("recall","Which two proteins does CDKN2A encode?","p16INK4a and p14ARF (alternative first exons, different reading frames)",["genes"]),
("recall","Mouse gene symbol format (e.g., p53)?","First letter capitalized, italic: Trp53 (protein TRP53)",["species"]),
("identify","Kras^LSL-G12D^ in a mouse paper?","Kras allele with Lox-Stop-Lox cassette; Cre removes it to express G12D",["species","mouse-genetics"]),
("recall","What does 'fl/fl' mean on a mouse gene?","Homozygous floxed: both alleles flanked by loxP sites, deleted where Cre is expressed",["mouse-genetics"]),
("recall","Yeast: CDC28 vs cdc28 vs Cdc28p?","Wild-type gene / recessive mutant allele / protein",["species"]),
("identify","Decode YFL039C.","Yeast ORF: chromosome F (VI), left arm, ORF 39, Crick strand (this is ACT1)",["species"]),
("recall","Zebrafish gene symbol style?","All lowercase italic (tp53)",["species"]),
("identify","Decode HLA-DRB1*15:01.","Gene HLA-DRB1; allele group 15; specific protein 01",["HLA"]),
("recall","What do fields 3 and 4 of an HLA allele name encode?","3: synonymous coding differences; 4: non-coding (intron/UTR) differences",["HLA"]),
("recall","What is an rsID?","dbSNP Reference SNP cluster ID: a variant position plus known alleles, assembly-independent",["variants"]),
("recall","HGVS prefixes c., p., g., n., m.?","Coding DNA, protein, genomic, non-coding RNA, mitochondrial",["HGVS"]),
("recall","In HGVS c. numbering, what is c.1?","The A of the ATG start codon",["HGVS"]),
("identify","c.-14 vs c.*20?","14 nt upstream of the ATG (5' UTR) vs 20 nt after the stop codon (3' UTR)",["HGVS"]),
("identify","c.88+1G>T","Intronic: first base of the intron after coding position 88 (canonical splice donor)",["HGVS"]),
("identify","p.(Arg248Gln): what do the parentheses mean?","Protein change is predicted, not experimentally confirmed",["HGVS"]),
("identify","p.Arg213ProfsTer8","Frameshift: Arg213 becomes Pro; new reading frame ends at a stop 8 codons later",["HGVS"]),
("identify","p.Arg196Ter (or p.Arg196*)","Nonsense: Arg196 replaced by a stop codon",["HGVS"]),
("recall","BRAF V600E in HGVS (coding DNA)?","c.1799T>A, p.Val600Glu",["HGVS","cancer"]),
("identify","ENSG / ENST / ENSP","Ensembl gene / transcript / protein IDs (human)",["identifiers","Ensembl"]),
("identify","ENSMUSG00000059552","Ensembl mouse gene ID (prefix ENSMUSG)",["identifiers","Ensembl"]),
("identify","NM_ vs XM_","RefSeq curated mRNA vs computationally predicted mRNA",["identifiers","RefSeq"]),
("identify","NR_","RefSeq curated non-coding RNA",["identifiers","RefSeq"]),
("identify","NP_000537.3","RefSeq curated protein (TP53), version 3",["identifiers","RefSeq"]),
("identify","NC_000017.11","RefSeq complete chromosome 17 sequence, GRCh38 (.10 = GRCh37)",["identifiers","RefSeq"]),
("identify","P04637","UniProt accession for human p53",["identifiers","UniProt"]),
("identify","P53_HUMAN","UniProt entry name (mnemonic), not the stable accession",["identifiers","UniProt"]),
("identify","P04637-2","UniProt isoform 2 of P04637",["identifiers","UniProt"]),
("recall","UniProt accession lengths?","6 or 10 alphanumeric characters (e.g., P04637, A0A024R1R8)",["identifiers","UniProt"]),
("recall","Swiss-Prot vs TrEMBL?","Swiss-Prot: manually reviewed; TrEMBL: unreviewed, automatic (much larger)",["UniProt"]),
("identify","7157","NCBI Gene (Entrez) ID for TP53",["identifiers","NCBI"]),
("identify","1TUP","PDB structure ID (4 chars, starts with digit); p53 core domain bound to DNA",["identifiers","PDB"]),
("identify","AF-P04637-F1","AlphaFold DB model for UniProt P04637, fragment 1",["identifiers","AlphaFold"]),
("apply","A dataset's Ensembl IDs look like ENSG00000141510.18 but your lookup table has no versions. Fix?","Strip the .N version suffix before joining (accept that the version encodes the annotation release)",["data-hygiene"]),
("apply","Why report a variant against NM_000546.6 rather than just 'TP53'?","Coordinates depend on the exact transcript and version; different isoforms number differently",["HGVS"]),
]
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
build(2,"naming-conventions","Naming conventions and identifiers","How to read gene and protein names across species, HLA alleles, HGVS variant notation and rsIDs, and the identifier formats from Ensembl, RefSeq, UniProt, PDB and others. Parsing these on sight is what lets you join datasets and read methods sections.",lesson,cards,quiz)
