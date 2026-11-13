from common import build
lesson = r"""
## How to think about signaling

Signaling pathways are information-processing circuits. A signal (growth factor, cytokine, DNA damage) activates a receptor or sensor. The receptor flips molecular switches, mostly **phosphorylation** by kinases and **GTP binding** by small GTPases. The cascade ends at transcription factors or effectors that change gene expression, metabolism, division or survival. **Negative feedback** is everywhere. Cancer is largely the story of these switches getting stuck: **oncogenes** are stuck-on accelerators (gain of function, usually one allele is enough) and **tumor suppressors** are broken brakes (loss of function, usually both alleles: Knudson's **two-hit** hypothesis).

Conventions in figures: arrows mean activation, flat-headed (⊣) lines mean inhibition. "p-ERK" or "pERK" means the phosphorylated (active) form. Western blots of phospho-proteins are the classic readout of pathway activity.

## RTK → RAS → MAPK

1. A growth factor (EGF) binds a **receptor tyrosine kinase** (EGFR/ERBB family, MET, ALK, etc.). Receptors dimerize and **autophosphorylate** tyrosines.
2. Adaptor **GRB2** binds the phosphotyrosines through its SH2 domain and recruits **SOS**, a **GEF** that swaps GDP for GTP on **RAS** (KRAS, NRAS, HRAS).
3. RAS-GTP activates **RAF** (ARAF/BRAF/CRAF), which phosphorylates **MEK1/2**, which phosphorylate **ERK1/2** (MAPK3/MAPK1). ERK enters the nucleus and drives proliferation genes (e.g., via FOS, MYC).
4. RAS turns itself off by hydrolyzing GTP, helped by **GAPs** such as **NF1**.

Cancer mutations: **KRAS G12/G13/Q61** impair GTP hydrolysis, locking RAS on (common in pancreatic, colorectal and lung cancers). **BRAF V600E** (melanoma, ~half of cases) makes BRAF constitutively active. **EGFR** L858R/exon 19 deletions occur in lung adenocarcinoma. Loss of NF1 removes the brake. Drugs: EGFR inhibitors (osimertinib), BRAF inhibitors (vemurafenib, dabrafenib), MEK inhibitors (trametinib), KRAS G12C inhibitors (sotorasib).

## PI3K → AKT → mTOR

RTKs also activate **PI3K** (catalytic subunit p110α is encoded by **PIK3CA**), which phosphorylates the membrane lipid **PIP2 → PIP3**. PIP3 recruits **AKT**, which is activated by phosphorylation at **T308 (by PDK1)** and **S473 (by mTORC2)**. AKT promotes survival and growth. It inhibits the **TSC1/TSC2** complex, freeing the small GTPase **RHEB** to activate **mTORC1**. mTORC1 phosphorylates **S6K** and **4E-BP1** to increase protein synthesis, and it integrates nutrient and energy signals (AMPK inhibits it). **PTEN** dephosphorylates PIP3 back to PIP2 and is a major tumor suppressor. **Rapamycin** inhibits mTORC1. PIK3CA hotspots: E545K, H1047R.

## p53 and the DNA damage response

- Sensors: **ATM** responds to double-strand breaks; **ATR** responds to single-stranded DNA and replication stress. They phosphorylate the checkpoint kinases **CHK2** and **CHK1** respectively, and both phosphorylate **p53** (e.g., Ser15).
- Normally p53 is kept low by **MDM2**, an E3 ubiquitin ligase that targets it for degradation. MDM2 is itself a p53 target gene, forming a negative feedback loop. Damage-induced phosphorylation blocks MDM2 binding, so p53 accumulates.
- p53 is a **transcription factor**. Its targets include **CDKN1A (p21)** for cell cycle arrest, **MDM2**, and pro-apoptotic **BAX**, **PUMA (BBC3)** and **NOXA (PMAIP1)**. Outcomes: arrest and repair, senescence, or apoptosis.
- **TP53** is the most frequently mutated gene in human cancer. Most mutations are missense in the DNA-binding domain (hotspots R175, R248, R273). Germline TP53 mutations cause **Li-Fraumeni syndrome**. BRCA1/BRCA2 work in homologous recombination repair; their loss sensitizes cells to **PARP inhibitors** (synthetic lethality).

## Wnt/β-catenin

Without Wnt, a **destruction complex** (APC, AXIN, GSK3β, CK1) phosphorylates **β-catenin (CTNNB1)**, which is then ubiquitinated and degraded. Wnt binds **Frizzled** plus **LRP5/6** co-receptors, the destruction complex is inhibited, and β-catenin accumulates, enters the nucleus, and partners with **TCF/LEF** to activate targets (MYC, AXIN2, LGR5). **APC** loss starts most colorectal cancers. Wnt also maintains stem cells.

## NF-κB

Inactive **NF-κB** dimers (classically **RELA/p65 + p50**) are held in the cytoplasm by **IκB**. Stimuli (TNF, IL-1, Toll-like receptors) activate the **IKK complex** (IKKα, IKKβ, NEMO), which phosphorylates IκBα, leading to its ubiquitination and degradation. NF-κB then enters the nucleus to drive inflammatory and survival genes. It is central to innate immunity and inflammation.

## JAK-STAT

Cytokine receptors (interferons, interleukins, EPO) lack intrinsic kinase activity. They associate with **JAKs** (JAK1, JAK2, JAK3, TYK2). Ligand binding activates JAKs, which phosphorylate the receptor and recruit **STATs**. STATs are phosphorylated, dimerize, and enter the nucleus as transcription factors. **SOCS** proteins provide negative feedback. **JAK2 V617F** drives myeloproliferative neoplasms; JAK inhibitors include ruxolitinib.

## Apoptosis

- **Intrinsic (mitochondrial)**: stress tips the balance in the **BCL-2 family**. BH3-only proteins (BIM, BID, PUMA, NOXA) override anti-apoptotic proteins (BCL-2, BCL-XL, MCL-1), letting **BAX/BAK** permeabilize the mitochondrial outer membrane (MOMP). **Cytochrome c** is released and forms the **apoptosome** with **APAF1**, which activates **caspase-9** and then executioner **caspases-3/7**. The BCL-2 inhibitor **venetoclax** exploits this.
- **Extrinsic**: death ligands (FASL, TNF, TRAIL) bind death receptors, which recruit **FADD** and activate **caspase-8**. Caspase-8 cleaves BID to link to the intrinsic path.
- Caspases are cysteine proteases that cleave after Asp. Cleaved caspase-3 and cleaved PARP are classic markers.

## Cell cycle

Phases: **G1 → S** (DNA replication) **→ G2 → M** (mitosis), with G0 for quiescent cells. Engines are **cyclin–CDK** pairs:
- **Cyclin D–CDK4/6** (G1): phosphorylates **RB**, releasing **E2F** TFs to transcribe S-phase genes. Passing the **restriction point** commits the cell to dividing.
- **Cyclin E–CDK2** (G1/S), **cyclin A–CDK2** (S), **cyclin B–CDK1** (G2/M).
- Brakes: **INK4** family (p16^INK4a, encoded by CDKN2A) inhibits CDK4/6. **CIP/KIP** family (p21, p27) inhibits CDK2/CDK1.
- Checkpoints: **G1/S** (DNA damage → p53 → p21), **G2/M** (damage → CHK1/2 → CDK1 held inactive), and the **spindle assembly checkpoint** (blocks anaphase via MAD2 inhibiting APC/C–CDC20 until all chromosomes are attached).
- CDK4/6 inhibitors: palbociclib, ribociclib, abemaciclib (in HR+ breast cancer).

## Oncogenes and tumor suppressors to know

**Oncogenes**: KRAS, NRAS, BRAF, EGFR, ERBB2 (HER2 amplification), PIK3CA, MYC (amplification), ABL1 (BCR-ABL fusion in CML, treated with imatinib), ALK fusions, CCND1, MDM2 amplification. **Tumor suppressors**: TP53, RB1, PTEN, APC, CDKN2A, BRCA1/2, NF1, VHL, SMAD4, ARID1A.

## How you'll see this in a paper

- "KRAS-mutant vs wild-type", "BRAF^V600E^ melanoma": stratification by driver.
- "Hallmark gene sets (MSigDB): E2F targets, G2M checkpoint, TNFA signaling via NFKB, P53 pathway": pathway activity scores in RNA-seq.
- "pERK/ERK ratio": MAPK activity readout.
- Perturbation models (e.g., predicting Perturb-seq responses) are often evaluated on whether they recover known pathway structure.
"""
cards = [
("recall","Oncogene vs tumor suppressor (mechanism and allele count)?","Oncogene: gain of function, usually one allele; TS: loss of function, usually both alleles (two-hit)",["cancer"]),
("recall","Knudson two-hit hypothesis?","Both alleles of a tumor suppressor must be inactivated (e.g., RB1)",["cancer"]),
("recall","Order the MAPK cascade from receptor.","RTK → GRB2 → SOS → RAS → RAF → MEK → ERK",["MAPK"]),
("recall","Role of SOS?","GEF that loads GTP onto RAS (activates it)",["MAPK"]),
("recall","Role of NF1?","RAS GAP: accelerates GTP hydrolysis (turns RAS off); tumor suppressor",["MAPK"]),
("recall","Why do KRAS G12 mutations activate RAS?","Impair GAP-stimulated GTP hydrolysis → RAS stuck in GTP-bound on state",["MAPK","cancer"]),
("recall","BRAF V600E is classically associated with which cancer?","Melanoma (~half of cases); also thyroid, colorectal",["MAPK","cancer"]),
("recall","Gene names for ERK1/ERK2?","MAPK3 / MAPK1",["MAPK","naming"]),
("recall","What does a GEF vs a GAP do for a small GTPase?","GEF: exchanges GDP→GTP (on); GAP: stimulates GTP hydrolysis (off)",["signaling"]),
("recall","What does PI3K produce?","PIP3 from PIP2 (phosphorylates the 3' position of the inositol ring)",["PI3K"]),
("recall","Which gene encodes PI3K p110α?","PIK3CA",["PI3K","naming"]),
("recall","Role of PTEN?","Lipid phosphatase converting PIP3 → PIP2; opposes PI3K; tumor suppressor",["PI3K"]),
("recall","AKT activating phosphorylation sites and kinases?","T308 by PDK1; S473 by mTORC2",["PI3K"]),
("recall","How does AKT activate mTORC1?","Inhibits TSC1/TSC2 → RHEB-GTP accumulates → activates mTORC1",["PI3K","mTOR"]),
("recall","Two classic mTORC1 substrates?","S6K and 4E-BP1",["mTOR"]),
("recall","Which drug inhibits mTORC1?","Rapamycin (sirolimus) and rapalogs",["mTOR","drugs"]),
("recall","PIK3CA hotspot mutations?","E545K (helical domain), H1047R (kinase domain)",["PI3K","cancer"]),
("recall","ATM vs ATR: what damage do they sense?","ATM: double-strand breaks; ATR: ssDNA / replication stress",["DDR"]),
("recall","Checkpoint kinases downstream of ATM and ATR?","ATM → CHK2; ATR → CHK1",["DDR"]),
("recall","What keeps p53 low in unstressed cells?","MDM2, an E3 ubiquitin ligase targeting p53 for degradation",["p53"]),
("recall","Why is the p53–MDM2 relationship a negative feedback loop?","p53 transcribes MDM2, which degrades p53",["p53"]),
("recall","Key p53 target genes?","CDKN1A (p21) arrest; MDM2 feedback; BAX, BBC3 (PUMA), PMAIP1 (NOXA) apoptosis",["p53"]),
("recall","Where do most TP53 cancer mutations fall?","Missense in the DNA-binding domain (hotspots R175, R248, R273)",["p53","cancer"]),
("recall","Germline TP53 mutation syndrome?","Li-Fraumeni syndrome",["p53"]),
("recall","Why are BRCA-deficient tumors sensitive to PARP inhibitors?","Synthetic lethality: HR repair loss + PARP inhibition → unrepaired lethal DNA damage",["DDR","drugs"]),
("recall","Wnt off state: what happens to β-catenin?","Destruction complex (APC, AXIN, GSK3β, CK1) phosphorylates it → ubiquitinated and degraded",["Wnt"]),
("recall","Wnt receptors?","Frizzled + LRP5/6 co-receptor",["Wnt"]),
("recall","Nuclear partners of β-catenin?","TCF/LEF transcription factors",["Wnt"]),
("recall","Which Wnt pathway gene is lost in most colorectal cancers?","APC",["Wnt","cancer"]),
("recall","How is NF-κB kept inactive?","Bound in cytoplasm by IκB",["NFkB"]),
("recall","What activates canonical NF-κB?","IKK complex (IKKα/β, NEMO) phosphorylates IκBα → degraded → RELA/p50 enters nucleus",["NFkB"]),
("recall","JAK-STAT signal flow?","Cytokine → receptor-associated JAK activation → STAT phosphorylation → dimerization → nucleus",["JAK-STAT"]),
("recall","Name the four JAKs.","JAK1, JAK2, JAK3, TYK2",["JAK-STAT"]),
("recall","JAK2 V617F causes?","Myeloproliferative neoplasms (e.g., polycythemia vera)",["JAK-STAT","cancer"]),
("recall","Negative feedback regulators of JAK-STAT?","SOCS proteins (also PIAS, phosphatases)",["JAK-STAT"]),
("recall","Intrinsic apoptosis core steps?","BH3-only activation → BAX/BAK MOMP → cytochrome c → APAF1 apoptosome → caspase-9 → caspase-3/7",["apoptosis"]),
("recall","Extrinsic apoptosis initiator caspase?","Caspase-8 (via death receptor → FADD)",["apoptosis"]),
("recall","Anti-apoptotic BCL-2 family members?","BCL-2, BCL-XL, MCL-1",["apoptosis"]),
("recall","Venetoclax target?","BCL-2 (a BH3 mimetic)",["apoptosis","drugs"]),
("recall","Classic apoptosis markers on a blot?","Cleaved caspase-3, cleaved PARP",["apoptosis"]),
("recall","Cyclin–CDK pairs by phase?","D–CDK4/6 (G1), E–CDK2 (G1/S), A–CDK2 (S), B–CDK1 (M)",["cell-cycle"]),
("recall","How does cyclin D–CDK4/6 drive S-phase entry?","Phosphorylates RB → releases E2F transcription factors",["cell-cycle"]),
("recall","INK4 vs CIP/KIP inhibitors?","INK4 (p16) inhibit CDK4/6; CIP/KIP (p21, p27) inhibit CDK2/CDK1",["cell-cycle"]),
("recall","Spindle assembly checkpoint mechanism?","Unattached kinetochores → MAD2 inhibits APC/C–CDC20 → anaphase blocked",["cell-cycle"]),
("recall","Examples of CDK4/6 inhibitors?","Palbociclib, ribociclib, abemaciclib",["cell-cycle","drugs"]),
("recall","BCR-ABL: what disease, what drug?","CML (Philadelphia chromosome t(9;22)); imatinib",["cancer","drugs"]),
("apply","A tumor has HER2 amplification. Which gene and drug class?","ERBB2; anti-HER2 therapy (e.g., trastuzumab)",["cancer"]),
("apply","RNA-seq shows high 'E2F targets' and 'G2M checkpoint' hallmark scores. Interpretation?","Highly proliferative samples / cycling cells",["cell-cycle","papers"]),
("apply","A KRAS G12D tumor: would an EGFR inhibitor alone likely work?","Unlikely: mutant RAS is downstream of EGFR and constitutively active",["MAPK","cancer"]),
]
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
