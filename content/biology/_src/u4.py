from common import build
import os
lesson = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"lessons","u4.md")).read()
from cards_u4 import cards
quiz = [
("In a sequence, which letter denotes lysine?",["L","K","Y","I"],1,"K = Lys; L = Leu, Y = Tyr, I = Ile."),
("A residue with pLDDT 42 in an AlphaFold model most likely:",["Is highly accurate","Lies in a disordered or unconfident region","Is a catalytic residue","Is in a β-sheet"],1,"pLDDT < 50 is very low confidence, often indicating disorder."),
("PAE between two domains is high while each domain's pLDDT is high. Conclusion?",["Both domains are wrong","Relative placement of the domains is uncertain","The protein is disordered","The MSA was empty"],1,"PAE reports inter-residue positional confidence, so it captures domain orientation."),
("Which residue is most likely to disrupt an α-helix if introduced?",["Alanine","Leucine","Proline","Glutamate"],2,"Proline's ring constrains the backbone and lacks an amide H, breaking helices."),
("Coevolution in an MSA is mainly used to infer:",["Expression level","Residue-residue contacts","Post-translational modifications","Subcellular location"],1,"Covarying positions tend to be in spatial contact."),
("Which amino acids can be phosphorylated by protein kinases?",["S, T, Y","K, R, H","D, E","G, P, C"],0,"Ser/Thr kinases and Tyr kinases."),
("Which family has seven transmembrane helices?",["Receptor tyrosine kinases","GPCRs","Nuclear receptors","Immunoglobulins"],1,"GPCRs = 7TM receptors."),
("The antibody region most responsible for antigen-binding diversity is:",["Fc","CDR-H3","Hinge","Constant light domain"],1,"CDR-H3 is the most variable loop and usually central to binding."),
("A TM-score of 0.3 between a prediction and the true structure suggests:",["Same fold","Different fold / largely incorrect","Atomic accuracy","Identical sequence"],1,"TM-score > 0.5 generally indicates the same fold; ~0.3 is close to random."),
("Pfam represents protein families primarily as:",["3D structures","Profile HMMs","Pathway diagrams","k-mer counts"],1,"Pfam builds profile HMMs from curated seed alignments."),
("Which is a sign that a protein will be hard for MSA-based structure prediction?",["Many homologs","Low Neff / few homologs","High pLDDT","Presence of a kinase domain"],1,"Shallow MSAs provide little coevolutionary signal."),
("Which pair is both negatively charged?",["K and R","D and E","N and Q","S and T"],1,"Aspartate (D) and glutamate (E) are acidic."),
("Where are pLDDT values stored in AlphaFold PDB files?",["Occupancy column","B-factor column","Header remarks only","Chain ID"],1,"AlphaFold writes pLDDT into the B-factor field."),
("Most clinically used kinase inhibitors are:",["Allosteric activators","ATP-competitive","Covalent DNA binders","GPCR agonists"],1,"Most target the ATP pocket; some are covalent (e.g., osimertinib binds Cys797) but still in the ATP site."),
]
build(4,"proteins","Proteins: sequence, structure, families","Amino acid one-letter codes by chemistry, levels of protein structure, domains and the databases that catalog them, AlphaFold confidence metrics (pLDDT, PAE, ipTM), MSAs and coevolution, and the protein families you'll meet most often in papers.",lesson,cards,quiz)
