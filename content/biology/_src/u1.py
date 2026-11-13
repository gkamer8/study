from common import build
import os
lesson = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"lessons","u1.md")).read()
from cards_u1 import cards, glossary_accept
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
build(1,"central-dogma","Central dogma for practitioners","How genes are laid out in the genome, how they become transcripts and proteins, and which vocabulary (exons, UTRs, isoforms, reading frames, PTMs) shows up constantly in papers and data. This is the vocabulary everything else builds on.",lesson,cards,quiz,glossary_accept)
