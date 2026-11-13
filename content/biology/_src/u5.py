from common import build
import os
lesson = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"lessons","u5.md")).read()
from cards_u5 import cards
quiz = [
("Which protein directly activates RAS by loading GTP?",["NF1","SOS","RAF","GRB2"],1,"SOS is the GEF; GRB2 is the adaptor; NF1 is a GAP."),
("PTEN loss leads to:",["Decreased PIP3","Increased PIP3 and AKT activity","Inactivation of mTORC1","Increased p53"],1,"PTEN converts PIP3 to PIP2; without it, PIP3 accumulates."),
("In unstressed cells, p53 is low mainly because of:",["ATM","MDM2-mediated degradation","p21","BAX"],1,"MDM2 ubiquitinates p53 for proteasomal degradation."),
("Which complex degrades β-catenin when Wnt is absent?",["IKK complex","Destruction complex (APC/AXIN/GSK3β/CK1)","Apoptosome","mTORC1"],1,"The destruction complex phosphorylates β-catenin for degradation."),
("Which event directly frees E2F to drive S-phase genes?",["p21 binding CDK2","RB phosphorylation by cyclin D–CDK4/6","Cyclin B degradation","MAD2 activation"],1,"Phosphorylated RB releases E2F."),
("Cytochrome c release from mitochondria leads to activation of:",["Caspase-8","Caspase-9 via the apoptosome","NF-κB","JAK2"],1,"Cytochrome c + APAF1 form the apoptosome activating caspase-9."),
("Which kinase primarily responds to double-strand breaks?",["ATR","ATM","CDK4","AKT"],1,"ATM senses DSBs; ATR senses ssDNA and replication stress."),
("Which is a tumor suppressor?",["MYC","PIK3CA","APC","ERBB2"],2,"APC is a tumor suppressor in the Wnt pathway; the others are oncogenes."),
("NF-κB is released when:",["IκB is phosphorylated and degraded","STATs dimerize","RB is phosphorylated","β-catenin is degraded"],0,"IKK phosphorylates IκB, leading to its degradation and NF-κB nuclear entry."),
("Which mutation is associated with myeloproliferative neoplasms?",["BRAF V600E","JAK2 V617F","KRAS G12C","EGFR L858R"],1,"JAK2 V617F constitutively activates JAK-STAT signaling."),
("The spindle assembly checkpoint prevents:",["Entry into S phase","Anaphase until all kinetochores are attached","DNA replication origin firing","Cytokinesis after anaphase"],1,"SAC inhibits APC/C–CDC20 until attachment is complete."),
("p21 (CDKN1A) is induced by p53 to:",["Promote apoptosis via MOMP","Inhibit CDKs and arrest the cell cycle","Degrade MDM2","Activate RAS"],1,"p21 is a CIP/KIP CDK inhibitor."),
("Rapamycin inhibits:",["PI3K","mTORC1","MEK","CDK4/6"],1,"Rapamycin with FKBP12 allosterically inhibits mTORC1."),
("Synthetic lethality with PARP inhibitors is exploited in tumors lacking:",["KRAS","BRCA1/2","MYC","EGFR"],1,"BRCA loss impairs homologous recombination; PARP inhibition is then lethal."),
("ERK1 and ERK2 correspond to which official gene symbols?",["MAP2K1/MAP2K2","MAPK3/MAPK1","MAPK8/MAPK9","RAF1/BRAF"],1,"ERK1 = MAPK3, ERK2 = MAPK1; MEK1/2 = MAP2K1/2; JNKs = MAPK8/9."),
]
build(5,"pathways","Key pathways and signaling","The canonical signaling circuits that show up constantly in biology and cancer papers: RTK-RAS-MAPK, PI3K-AKT-mTOR, p53 and DNA damage, Wnt, NF-κB, JAK-STAT, apoptosis, and the cell cycle, plus the main oncogenes and tumor suppressors and the drugs that target them.",lesson,cards,quiz)
